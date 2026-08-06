"""Deliver one Ashgrove Times edition to Discord as a single webhook message.

`editions/YYYY-MM-DD.json` is the ONLY input. The payload is built here and
never hand-authored, so the daily routine's one creative act is writing the
edition file — everything in this module is deterministic and re-runnable with
no model in the loop.

The morning post carries three surfaces at once, sent as multipart/form-data
to `{webhook}?wait=true` (form shape per Discord's "Uploading Files" reference:
a `payload_json` part plus `files[n]` parts, wired to the payload's
`attachments` array by matching `id` to `n`):

    content  — the masthead line, plus the Pages permalink when it is live
    embeds   — LEAD + the five standing sections; the actual readable paper
    files[0] — the 1200x630 hero card, referenced by the lead embed as
               attachment://ashgrove-YYYY-MM-DD.png

West Virginia is not a wire section. Its embed is the Mountaineer State
Notebook and carries four parts: statewide briefs in the description, then
Regional Roundup / Away Desk / Fishing Report as embed fields, in that order.
The weather ear — the pointer to Claude the Weatherman's 7:15 forecast — is the
last thing in the message, in the final embed's footer.

The image tier is strictly ADDITIVE: drop `attachments` and the lead embed's
`image` block and the remaining JSON is a complete, readable paper. That
property is what makes every rung below still ship an edition.

    python post_discord.py --date 2026-08-04 --dry-run
    python post_discord.py --date 2026-08-04 --attach out/ashgrove-2026-08-04.png

FALLBACKS, in the order they fire: hero missing -> assets/masthead-fallback.png
-> no image at all (plain application/json POST of the same JSON) -> no Pages
link -> drop the notebook's roster names -> drop notebook lines to the floor
(away, then regional, then fishing) -> trim trailing briefs -> surrender the
notebook floor -> split into FRONT PAGE / INSIDE -> plain-text edition ->
429/5xx retries. Only a dead webhook (401/403/404) or an unreadable edition
file stops delivery outright.

An edition already recorded `posted` in `editions/index.json` is skipped, so a
routine retry can never double-post; `--force` overrides. The ledger row is
rewritten after EVERY successful send, not once at the end, so a run that dies
on message 2 of 3 leaves `messages_sent` behind and the next run resumes at
message 3 instead of putting the front page in the channel twice.

Nothing this module prints, appends to docs/FAILURES.md or writes to the ledger
can carry the webhook token: the webhook URL *is* the credential and `requests`
puts it inside its transport exceptions, so every such string goes through
_scrub() first. The repo may be public.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid

import config

try:
    import requests
except ImportError:  # delivery must not depend on pip having succeeded
    requests = None

# Discord's per-object caps. The 6000 total (config.EMBED_TOTAL_LIMIT) is the
# SUM of title + description + field.name + field.value + footer.text +
# author.name across every embed in one message; url and image.url are free.
TITLE_LIMIT = 256
DESCRIPTION_LIMIT = 4096
FIELD_VALUE_LIMIT = 1024
FIELD_COUNT_LIMIT = 25
FOOTER_LIMIT = 2048
AUTHOR_LIMIT = 256
EMBED_COUNT_LIMIT = 10
ATTACHMENT_COUNT_LIMIT = 10
ATTACHMENT_DESC_LIMIT = 1024

MIN_BRIEFS_PER_SECTION = 1
NEVER_TRIM = ("wv",)
FALLBACK_TRIM_ORDER = ("scitech", "world", "us", "sports")
FRONT_PAGE_SECTIONS = ("us", "world")

# The West Virginia notebook. `briefs` is statewide and behaves like every
# other section; these three are the local anchor Ian asked for and are the
# only arrays in the whole edition that may legally be empty. The order is
# fixed here; the visible subheads come from config so the broadsheet, the
# hero card and this embed all print the same words.
WV_SECTION_ID = "wv"
WV_FIELD_KEYS = ("regional", "away", "fishing")
# Optional content yields to confirmed content: three briefs a section is a
# settled editorial requirement, these arrays are explicitly optional. Away
# goes first because it is the least West Virginian; fishing goes last because
# it is two lines and the most distinctive thing in the paper.
WV_EXTRA_TRIM_ORDER = ("away", "regional", "fishing")

# ...but not to nothing on the first squeeze. config.EMBED_BUDGET closes only
# if a brief costs headline + summary + source NAME; the masked link this
# module actually sends spends its whole url too, measured at 62 chars a brief
# and 924 across fifteen. That overage has to land somewhere, and unfloored it
# lands entirely on the notebook — which would delete Ian's local anchor every
# single morning. This floor costs ~325 chars and is surrendered only after
# every trimmable section is already down to a single brief.
WV_EXTRA_FLOOR = {"away": 0, "regional": 1, "fishing": 1}

IMAGE_EXTENSIONS = (".png", ".webp", ".jpg", ".jpeg", ".gif")
MIME_TYPES = {
    ".png": "image/png",
    ".webp": "image/webp",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
}
DIRECTION_MARKS = {"up": "▲", "down": "▼"}
FLAT_MARK = "•"

HTTP_TIMEOUT = 30
RATE_LIMIT_ATTEMPTS = 5
SERVER_ERROR_ATTEMPTS = 3
LONG_RETRY_WAIT = 600  # one last try ~10 min out; still a morning post


class Result:
    """Outcome of one webhook POST, including the status a caller must branch on."""

    def __init__(self, ok: bool, status: int, message_id: str | None, detail: str = ""):
        self.ok = ok
        self.status = status
        self.message_id = message_id
        self.detail = detail


# --------------------------------------------------------------------------
# paths, env, small text helpers
# --------------------------------------------------------------------------


def _repo(*parts: str) -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), *parts)


def load_env_webhook(var: str) -> str | None:
    """Read a webhook URL from the environment or the local gitignored .env."""
    if os.getenv(var):
        return os.environ[var]
    env_path = _repo(".env")
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith(f"{var}="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'") or None
    return None


# The webhook URL *is* the credential — anyone holding it can post to the
# channel — and `requests` puts the full request URL inside several of its
# exception strings ("HTTPSConnectionPool(host=...): Max retries exceeded with
# url: /api/webhooks/<id>/<token>?wait=true"). Those strings get printed to
# stderr, appended to docs/FAILURES.md and written into editions/index.json,
# all three of which land in routine logs or a repo that may go PUBLIC. So
# nothing derived from a transport error reaches any of them unscrubbed.
REDACTION = "<webhook-token-redacted>"
WEBHOOK_PATH_RE = re.compile(r"(/api/webhooks/)(\d+)/[\w.-]+")
_WEBHOOK_HINT: str | None = None


def remember_webhook(url: str | None) -> None:
    """Register the live webhook so _scrub() can redact it without an argument.

    Set once, as soon as the URL is resolved, so that every later print/log
    path is covered even where the URL is not in scope (log_failures, the
    ledger write). Belt and braces on top of the pattern match below.
    """
    global _WEBHOOK_HINT
    _WEBHOOK_HINT = url or None


def _scrub(text: object, webhook_url: str | None = None) -> str:
    """Redact any webhook URL or bare token from a string bound for a log.

    Two independent passes, because either alone has a gap: the literal-URL
    replacement catches a token that appears without its /api/webhooks/ prefix,
    and the pattern catches a webhook this process never held (a stale one in
    an edition file, a second webhook in a wrapped exception).
    """
    if text is None:
        return ""
    out = str(text)
    for url in (webhook_url, _WEBHOOK_HINT):
        if not url:
            continue
        url = url.strip()
        if url and url in out:
            out = out.replace(url, REDACTION)
        if "/api/webhooks/" not in url:
            continue  # not a webhook URL; do not redact arbitrary substrings
        token = url.rstrip("/").rsplit("/", 1)[-1].split("?", 1)[0]
        if len(token) >= 8 and token in out:
            out = out.replace(token, REDACTION)
    return WEBHOOK_PATH_RE.sub(rf"\1\2/{REDACTION}", out)


def _clip(text: str | None, limit: int) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def _color(value: object) -> int:
    """Accept an int or a #rrggbb string. Hex is converted here, never by hand."""
    if isinstance(value, int):
        return value
    return int(str(value).lstrip("#"), 16)


def _long_date(iso_date: str) -> str:
    day = dt.date.fromisoformat(iso_date)
    return f"{day.strftime('%A, %B')} {day.day}, {day.year}"


def _utc_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _section_content(edition: dict, section_id: str) -> dict:
    """The edition's own section dict (content), not config's display metadata."""
    for section in edition.get("sections") or []:
        if section.get("id") == section_id:
            return section
    return {}


def _briefs_for(edition: dict, section_id: str) -> list[dict]:
    """The live briefs list for a section, so trimming can pop in place."""
    section = _section_content(edition, section_id)
    if not section:
        return []
    briefs = section.setdefault("briefs", [])
    return briefs if isinstance(briefs, list) else []


def _wv_entries(edition: dict, key: str) -> list[dict]:
    """The live regional/away/fishing list, so the trimmer can pop in place."""
    section = _section_content(edition, WV_SECTION_ID)
    if not section:
        return []
    entries = section.setdefault(key, [])
    return entries if isinstance(entries, list) else []


def _has_content(edition: dict, section_id: str) -> bool:
    """True when a section would produce a non-empty embed.

    West Virginia can carry the notebook with no statewide briefs, so an
    emptiness test on `briefs` alone would silently drop the whole section.
    """
    if _briefs_for(edition, section_id):
        return True
    if section_id != WV_SECTION_ID:
        return False
    return any(_wv_entries(edition, key) for key in WV_FIELD_KEYS)


def _present_sections(edition: dict) -> list[str]:
    """Section ids that get an embed, in display order."""
    return [
        s["id"]
        for s in sorted(config.SECTIONS, key=lambda s: s["order"])
        if _has_content(edition, s["id"])
    ]


# --------------------------------------------------------------------------
# payload construction
# --------------------------------------------------------------------------


def _stat_strip_line(entries: list[dict]) -> str:
    """Ticker line for the lead embed. Direction becomes a mark, never a color."""
    cells = []
    for entry in entries[:6]:
        mark = DIRECTION_MARKS.get(str(entry.get("direction") or "").lower(), FLAT_MARK)
        change = str(entry.get("change") or "").strip()
        text = f"{entry.get('label', '')} {entry.get('value', '')} {mark}".strip()
        if change:
            text = f"{text} {change}"
        cells.append(f"`{text}`")
    return "  ·  ".join(cells)


def _source_tail(item: dict) -> str:
    """` · [Outlet](url)` when both exist, ` · Outlet` when only the name does.

    Masked links render inside embeds only — the text-mode renderer uses bare
    angle-bracketed URLs instead.
    """
    source = (item.get("source") or "").strip()
    url = (item.get("url") or "").strip()
    if source and url:
        return f" · [{source}]({url})"
    if source:
        return f" · {source}"
    return ""


def _brief_block(brief: dict) -> str:
    """One brief: bold headline, summary, then the source."""
    headline = _clip(brief.get("headline"), TITLE_LIMIT)
    summary = (brief.get("summary") or "").strip()
    return f"**{headline}**\n{summary}{_source_tail(brief)}".strip()


def _people_tag(entry: dict) -> str:
    """`(Trav, Justin)` — first names only. There are no user ids in this repo."""
    people = [str(p).strip() for p in (entry.get("people") or []) if str(p).strip()]
    return f" ({', '.join(people)})" if people else ""


def _notebook_line(entry: dict) -> str:
    """One place, one sentence, one source — the whole regional/away format.

    Deliberately one line and not a brief block: Nate's instruction was lean,
    and a two-line entry per town is how a phone screen loses the section.
    """
    place = str(entry.get("place") or entry.get("region_id") or "").strip()
    item = str(entry.get("item") or "").strip()
    if not (place or item):
        return ""
    head = f"**{place}{_people_tag(entry)}**" if place else ""
    body = f"{head} — {item}" if head and item else (head or item)
    return f"{body}{_source_tail(entry)}".strip()


def _fishing_line(entry: dict) -> str:
    """`**Williams River (Cowen)** — 110 cfs and falling. · USGS 03186500`

    The source string is whatever fetch_fishing.py attributed the reading to,
    printed verbatim: the Topsail water temperature is Wrightsville Beach's,
    25 miles away, and this line is where that stays honest.
    """
    water = str(entry.get("water") or "").strip()
    line = str(entry.get("line") or "").strip()
    if not (water or line):
        return ""
    source = str(entry.get("source") or "").strip()
    tail = f" · {source}" if source else ""
    body = f"**{water}** — {line}" if water and line else (f"**{water}**" if water else line)
    return f"{body}{tail}".strip()


def _notebook_field(
    name: str, lines: list[str], max_fields: int = FIELD_COUNT_LIMIT
) -> tuple[list[dict], list[str]]:
    """Pack lines into as MANY non-inline fields as it takes to keep them all.

    Returns (fields, dropped_lines). The old version packed one field and
    popped from the tail until it fit 1024, silently — and Discord's per-field
    cap binds long before the 6000-char message cap does, so a notebook with
    five regional lines lost content inside a message that still had 1,300
    chars of headroom. That deleted exactly the West Virginia local anchor the
    paper exists to carry, and said nothing.

    Continuation fields are cheap: an embed may carry 25 of them and each costs
    only its own name against the 6000 budget. So the notebook SPLITS rather
    than drops, which hands the overflow to the one place that already knows
    how to shed notebook lines out loud — build_within_budget()'s documented
    WV_EXTRA_TRIM_ORDER ladder, which reports every line it takes.

    Dropping here is the last resort and only happens if max_fields runs out.
    Whatever it drops it returns, and no caller is allowed to discard that.

    inline is False on purpose: a one-sentence item in a three-across column
    wraps to four lines on a phone.
    """
    kept = [line for line in lines if line]
    if max_fields < 1:
        return [], kept
    fields: list[dict] = []
    dropped: list[str] = []
    current: list[str] = []

    def flush() -> None:
        if current:
            title = name if not fields else f"{name} (cont.)"
            fields.append({"name": title, "value": "\n".join(current), "inline": False})

    for index, line in enumerate(kept):
        # A single line over the cap is a content bug, not an overflow; clip it
        # so one runaway sentence cannot cost the lines behind it.
        line = _clip(line, FIELD_VALUE_LIMIT)
        if current and len("\n".join(current + [line])) > FIELD_VALUE_LIMIT:
            if len(fields) + 1 >= max_fields:
                dropped.extend(kept[index:])
                break
            flush()
            current = [line]
        else:
            current.append(line)
    flush()
    return fields, dropped


# Which notebook part keeps its fields when the 25-field budget cannot seat
# them all: the exact reverse of WV_EXTRA_TRIM_ORDER, so a squeeze here sheds
# the same part a squeeze in build_within_budget() would — away first, then
# regional, and the fishing report last.
WV_FIELD_KEEP_ORDER = tuple(reversed(WV_EXTRA_TRIM_ORDER)) + tuple(
    k for k in WV_FIELD_KEYS if k not in WV_EXTRA_TRIM_ORDER
)


def _wv_fields(edition: dict) -> tuple[list[dict], list[str]]:
    """The notebook's parts, in display order, empties skipped.

    Returns (fields, notes). Notes are non-empty only when the 25-field embed
    budget itself ran out — every caller must surface them, because a lost
    notebook line that is visible only in docs/FAILURES.md is the exact defect
    this function used to have.
    """
    rendered: dict[str, list[str]] = {}
    for key in WV_FIELD_KEYS:
        entries = [e for e in _wv_entries(edition, key) if isinstance(e, dict)]
        if not entries:
            continue
        render = _fishing_line if key == "fishing" else _notebook_line
        lines = [line for line in (render(e) for e in entries) if line]
        if lines:
            rendered[key] = lines

    # Allocate fields by keep-priority, then emit in display order.
    packed: dict[str, list[dict]] = {}
    notes: dict[str, str] = {}
    used = 0
    for key in WV_FIELD_KEEP_ORDER:
        lines = rendered.get(key)
        if not lines:
            continue
        remaining = FIELD_COUNT_LIMIT - used
        if remaining <= 0:
            # Never emit a 26th field: Discord 400s the whole message and the
            # paper vanishes over a line that was optional to begin with.
            fields_for_key, dropped = [], list(lines)
        else:
            fields_for_key, dropped = _notebook_field(config.WV_SUBHEADS[key], lines, remaining)
        packed[key] = fields_for_key
        used += len(fields_for_key)
        if dropped:
            notes[key] = (
                f"West Virginia notebook: dropped {len(dropped)} of {len(lines)} {key} "
                f"line(s) - out of embed fields ({FIELD_COUNT_LIMIT} max)"
            )

    fields = [field for key in WV_FIELD_KEYS for field in packed.get(key, [])]
    return fields, [notes[key] for key in WV_FIELD_KEYS if key in notes]


def weather_ear(edition: dict) -> str:
    """The pointer to Claude the Weatherman's 7:15 forecast.

    The edition file writes the day's wording; a file written without one
    falls back to config's dated rotation, so the ear is never one frozen
    string and a rerun of a date reproduces the same paper.
    """
    written = str(edition.get("weather_ear") or "").strip()
    return written or config.weather_ear(edition.get("edition_date"))


def _lead_embed(edition: dict, image_filename: str | None, page_url: str | None) -> dict:
    lead = edition.get("lead") or {}
    blocks: list[str] = []
    if lead.get("dek"):
        blocks.append(f"*{lead['dek'].strip()}*")
    blocks.extend(p.strip() for p in (lead.get("body") or []) if (p or "").strip())
    strip = _stat_strip_line(lead.get("stat_strip") or [])
    if strip:
        blocks.append(strip)

    embed: dict = {
        "title": _clip(lead.get("headline"), TITLE_LIMIT),
        "description": _clip("\n\n".join(blocks), DESCRIPTION_LIMIT),
        "color": _color(config.PALETTE["ink"]),
        "author": {"name": _clip(lead.get("byline") or config.BYLINE, AUTHOR_LIMIT)},
    }
    if page_url:
        embed["url"] = page_url
    if image_filename:
        embed["image"] = {"url": f"attachment://{image_filename}"}
    return embed


def _section_title(edition: dict, section: dict) -> str:
    """`🏔️ West Virginia — Mountaineer State Notebook`, plain label elsewhere.

    The broadsheet marks West Virginia with a bordered, tinted box instead of
    the two-column brief layout. Discord has no box, so the distinction has to
    be carried by the title — WV must not read as one more wire section.
    """
    title = f"{section.get('emoji', '')} {section['label']}".strip()
    if section["id"] != WV_SECTION_ID:
        return _clip(title, TITLE_LIMIT)
    notebook = str(
        _section_content(edition, WV_SECTION_ID).get("notebook_title")
        or config.WV_NOTEBOOK_TITLE
    ).strip()
    return _clip(f"{title} — {notebook}" if notebook else title, TITLE_LIMIT)


def _section_embed(
    edition: dict, section: dict, page_url: str | None, notes: list[str] | None = None
) -> dict:
    briefs = _briefs_for(edition, section["id"])
    embed: dict = {
        "title": _section_title(edition, section),
        "description": _clip("\n\n".join(_brief_block(b) for b in briefs), DESCRIPTION_LIMIT),
        "color": _color(section["color"]),
    }
    if section["id"] == WV_SECTION_ID:
        fields, field_notes = _wv_fields(edition)
        if fields:
            embed["fields"] = fields
        if notes is not None:
            notes.extend(field_notes)
    if not embed["description"]:
        # An empty description is a Discord 400; fields alone are legal.
        embed.pop("description")
    if page_url:
        # Distinct urls per embed: Discord merges embeds that share one url.
        embed["url"] = f"{page_url}#{section['id']}"
    return embed


def _masthead_line(edition: dict, page_url: str | None) -> str:
    folio = (
        f"No. {edition.get('edition_number', '?')} · "
        f"Vol. {edition.get('volume', 'I')} · "
        f"{_long_date(edition['edition_date'])}"
    )
    lines = [f"\U0001f4f0  **{config.MASTHEAD}** — *{config.TAGLINE}*", f"-# {folio}"]
    if page_url:
        # A bare url under the folio reads as a footnote and gets ignored —
        # it has to say what it is. Discord does NOT render masked links in
        # message content (only inside embeds), so the label is plain text
        # above the url rather than [text](url). Angle brackets still
        # suppress the auto-unfurl: the hero card is the picture here, and a
        # second preview card competing with it makes the post look cluttered.
        lines.append(
            "\U0001f4d6  **Read the full edition on the web** — the whole "
            "paper, set as a proper broadsheet:"
        )
        lines.append(f"<{page_url}>")
    return _clip("\n".join(lines), config.CONTENT_LIMIT)


def _inside_line(page_url: str | None) -> str:
    """Content line for the second message of a split.

    Anyone scrolling in mid-morning may see only this one, so it repeats the
    permalink rather than assuming they read the front page. Shared with the
    link backfill so an edited message matches a freshly posted one.
    """
    line = f"-# **{config.MASTHEAD}** · Inside"
    if page_url:
        line += f"\n\U0001f4d6  **Full edition on the web:** <{page_url}>"
    return line


def _closing_footer(edition: dict) -> dict | None:
    """Kicker, colophon, then the weather ear — the last line of the message.

    The ear rides the final embed's footer rather than top-level `content`
    because `content` renders ABOVE the embeds: a pointer to something that
    happens fifteen minutes later belongs at the bottom of the paper, in the
    small grey type, which is where a real weather ear lives anyway.
    """
    bits = [
        str(b).strip()
        for b in (edition.get("kicker"), edition.get("sources_note"), weather_ear(edition))
        if b and str(b).strip()
    ]
    if not bits:
        return None
    return {"text": _clip(" · ".join(bits), FOOTER_LIMIT)}


def build_payload(
    edition: dict,
    image_filename: str | None = None,
    page_url: str | None = None,
    notes: list[str] | None = None,
) -> dict:
    """Build the full six-embed message from an edition dict.

    Passing image_filename=None or page_url=None yields the same payload minus
    the attachment wiring / the links — no other code path changes.

    Pass `notes` to receive any degradation the build itself performed — today
    that is only a notebook line the field budget could not seat. Callers that
    deliver (rather than measure) MUST pass it: a dropped notebook line has to
    reach main()'s `degraded` list, the ledger, and docs/FAILURES.md.
    """
    present = _present_sections(edition)
    embeds = [_lead_embed(edition, image_filename, page_url)]
    for section in sorted(config.SECTIONS, key=lambda s: s["order"]):
        if section["id"] not in present:
            continue  # a wholly empty embed is a Discord 400; ship the rest
        embeds.append(_section_embed(edition, section, page_url, notes))

    footer = _closing_footer(edition)
    if footer and embeds:
        embeds[-1]["footer"] = footer

    payload: dict = {"content": _masthead_line(edition, page_url), "embeds": embeds}
    if image_filename:
        payload["attachments"] = [
            {
                "id": 0,
                "filename": image_filename,
                "description": _clip(
                    (edition.get("lead") or {}).get("headline"), ATTACHMENT_DESC_LIMIT
                ),
            }
        ]
    return payload


def _finalize(payload: dict) -> dict:
    """Stamp identity and ping policy — the only place either is decided."""
    final = dict(payload)
    final["username"] = config.WEBHOOK_USERNAME
    final.setdefault("allowed_mentions", {"parse": ["users"]})
    return final


# --------------------------------------------------------------------------
# budget: measure, trim, split, clamp
# --------------------------------------------------------------------------


def embed_text_length(embeds: list[dict]) -> int:
    """Chars Discord counts against the 6000 cap across one message's embeds."""
    total = 0
    for embed in embeds:
        total += len(embed.get("title") or "")
        total += len(embed.get("description") or "")
        total += len((embed.get("footer") or {}).get("text") or "")
        total += len((embed.get("author") or {}).get("name") or "")
        for field in embed.get("fields") or []:
            total += len(field.get("name") or "") + len(field.get("value") or "")
    return total


def trim_order() -> list[str]:
    """Section ids in the order trailing briefs get dropped, highest priority first.

    config.SECTIONS carries the declarative trim_priority; West Virginia is
    excluded outright and every section floors at one brief, so no section can
    be emptied by trimming.
    """
    ranked = [
        s
        for s in config.SECTIONS
        if s["id"] not in NEVER_TRIM and int(s.get("trim_priority", 0) or 0) > 0
    ]
    if not ranked:
        return list(FALLBACK_TRIM_ORDER)
    ranked.sort(key=lambda s: (-int(s["trim_priority"]), s["order"]))
    return [s["id"] for s in ranked]


def _strip_people(edition: dict) -> int:
    """Drop the roster parentheticals from the notebook. Returns entries changed.

    First rung of the ladder because it is the only one that costs no news:
    the place names stay, the sentences stay, only "(Trav, Justin)" goes.
    """
    changed = 0
    for key in ("regional", "away"):
        for entry in _wv_entries(edition, key):
            if isinstance(entry, dict) and entry.pop("people", None):
                changed += 1
    return changed


def build_within_budget(
    edition: dict,
    image_filename: str | None,
    page_url: str | None,
) -> tuple[dict, dict, list[str]]:
    """Shrink the message until the embeds fit EMBED_HARD, in five rungs.

    1. drop the notebook's roster names — costs no news at all
    2. drop notebook lines down to WV_EXTRA_FLOOR: away, then regional, then
       fishing, tail-first within each
    3. drop trailing briefs round-robin over config's trim_priority
    4. surrender the notebook floor
    5. give up and let the caller split

    Rungs 1-2 precede rung 3 because `regional`, `away` and `fishing` are the
    only optional arrays in the contract while three briefs a section is
    settled editorial policy. West Virginia's STATEWIDE briefs are in
    NEVER_TRIM and are unreachable by rung 3, so the notebook can lose every
    extra line and the section still runs its full statewide report.

    Returns (possibly trimmed edition copy, payload, notes). The lead is never
    touched and no section is ever emptied.
    """
    working = copy.deepcopy(edition)
    # field_notes is rebuilt from scratch on every build so it always describes
    # the payload actually being returned, never a superseded attempt.
    field_notes: list[str] = []
    payload = build_payload(working, image_filename, page_url, field_notes)
    if embed_text_length(payload["embeds"]) <= config.EMBED_HARD:
        return working, payload, list(field_notes)

    notes: list[str] = []
    dropped: dict[str, int] = {}
    cut: dict[str, int] = {}

    def rebuild() -> bool:
        nonlocal payload
        field_notes.clear()
        payload = build_payload(working, image_filename, page_url, field_notes)
        return embed_text_length(payload["embeds"]) <= config.EMBED_HARD

    def summary() -> list[str]:
        out = list(notes) + list(field_notes)
        if cut:
            detail = ", ".join(f"{count} {key}" for key, count in cut.items())
            out.append(f"trimmed {sum(cut.values())} West Virginia notebook line(s): {detail}")
        if dropped:
            detail = ", ".join(f"{count} from {sid}" for sid, count in dropped.items())
            out.append(f"trimmed {sum(dropped.values())} brief(s) to fit the embed budget: {detail}")
        return out

    def trim_notebook(floors: dict[str, int]) -> bool:
        for key in WV_EXTRA_TRIM_ORDER:
            entries = _wv_entries(working, key)
            while len(entries) > floors.get(key, 0):
                entries.pop()
                cut[key] = cut.get(key, 0) + 1
                if rebuild():
                    return True
        return False

    if _strip_people(working):
        notes.append("dropped the West Virginia notebook's roster names to fit the budget")
        if rebuild():
            return working, payload, summary()

    if trim_notebook(WV_EXTRA_FLOOR):
        return working, payload, summary()

    order = trim_order()
    while True:
        dropped_any = False
        for section_id in order:
            briefs = _briefs_for(working, section_id)
            if len(briefs) <= MIN_BRIEFS_PER_SECTION:
                continue
            briefs.pop()
            dropped[section_id] = dropped.get(section_id, 0) + 1
            dropped_any = True
            if rebuild():
                return working, payload, summary()
        if not dropped_any:
            break

    trim_notebook({})
    return working, payload, summary()


def split_payloads(
    edition: dict,
    image_filename: str | None,
    page_url: str | None,
    notes: list[str] | None = None,
) -> list[dict]:
    """FRONT PAGE (lead + hero + U.S. + World) and INSIDE (WV + Sports + SciTech).

    Two messages a second apart, each with its own fresh 6000-char budget.
    """
    payload = build_payload(edition, image_filename, page_url, notes)
    embeds = payload["embeds"]
    # Partition by section id, not by index — a skipped section would shift a
    # slice. _present_sections is the same predicate build_payload used, so a
    # WV embed carrying only notebook fields still pairs with its id.
    paired = list(zip(_present_sections(edition), embeds[1:]))
    front_embeds = [embeds[0]] + [e for sid, e in paired if sid in FRONT_PAGE_SECTIONS]
    inside_embeds = [e for sid, e in paired if sid not in FRONT_PAGE_SECTIONS]
    if not inside_embeds:
        return [payload]

    footer = _closing_footer(edition)
    for embed in embeds:
        embed.pop("footer", None)
    if footer:
        inside_embeds[-1]["footer"] = footer

    front: dict = {"content": payload["content"], "embeds": front_embeds}
    if "attachments" in payload:
        front["attachments"] = payload["attachments"]

    inside: dict = {"content": _inside_line(page_url), "embeds": inside_embeds}
    return [front, inside]


def clamp_payload(payload: dict, limit: int | None = None) -> list[str]:
    """Last-resort size clamp: shorten descriptions from the back until it fits.

    Only reached when trimming and splitting both fall short. The lead embed is
    clipped only if it alone is still over.
    """
    limit = config.EMBED_HARD if limit is None else limit
    notes: list[str] = []
    embeds = payload.get("embeds") or []
    for index in range(len(embeds) - 1, -1, -1):
        total = embed_text_length(embeds)
        if total <= limit:
            break
        description = embeds[index].get("description") or ""
        keep = max(len(description) - (total - limit), 40)
        if not description or keep >= len(description):
            continue
        embeds[index]["description"] = _clip(description, keep)
        notes.append(f"clamped embed[{index}] description to fit the {limit}-char budget")
    return notes


def validate_payload(payload: dict) -> list[str]:
    """Return a list of Discord-limit violations (empty = OK).

    This is the refusal gate: an over-limit payload is never handed to the API
    to 400 — the failure is named here instead.
    """
    problems: list[str] = []

    content = payload.get("content") or ""
    if len(content) > config.CONTENT_LIMIT:
        problems.append(f"content is {len(content)} chars (limit {config.CONTENT_LIMIT})")

    embeds = payload.get("embeds") or []
    if not embeds and not content:
        problems.append("payload has neither content nor embeds")
    if len(embeds) > EMBED_COUNT_LIMIT:
        problems.append(f"{len(embeds)} embeds (limit {EMBED_COUNT_LIMIT})")

    referenced: set[str] = set()
    for i, embed in enumerate(embeds):
        title = embed.get("title") or ""
        description = embed.get("description") or ""
        if len(title) > TITLE_LIMIT:
            problems.append(f"embed[{i}].title {len(title)} chars (limit {TITLE_LIMIT})")
        if len(description) > DESCRIPTION_LIMIT:
            problems.append(
                f"embed[{i}].description {len(description)} chars (limit {DESCRIPTION_LIMIT})"
            )
        if not (title or description or embed.get("fields") or embed.get("image")):
            problems.append(f"embed[{i}] is empty")
        fields = embed.get("fields") or []
        if len(fields) > FIELD_COUNT_LIMIT:
            problems.append(f"embed[{i}] has {len(fields)} fields (limit {FIELD_COUNT_LIMIT})")
        for j, field in enumerate(fields):
            if not (field.get("name") or "").strip():
                problems.append(f"embed[{i}].fields[{j}].name is empty")
            if not (field.get("value") or "").strip():
                problems.append(f"embed[{i}].fields[{j}].value is empty")
            if len(field.get("name", "")) > TITLE_LIMIT:
                problems.append(f"embed[{i}].fields[{j}].name over {TITLE_LIMIT}")
            if len(field.get("value", "")) > FIELD_VALUE_LIMIT:
                problems.append(
                    f"embed[{i}].fields[{j}].value {len(field['value'])} chars "
                    f"(limit {FIELD_VALUE_LIMIT})"
                )
        if len((embed.get("footer") or {}).get("text") or "") > FOOTER_LIMIT:
            problems.append(f"embed[{i}].footer.text over {FOOTER_LIMIT}")
        if len((embed.get("author") or {}).get("name") or "") > AUTHOR_LIMIT:
            problems.append(f"embed[{i}].author.name over {AUTHOR_LIMIT}")
        image_url = (embed.get("image") or {}).get("url") or ""
        if image_url.startswith("attachment://"):
            referenced.add(image_url[len("attachment://") :])

    total = embed_text_length(embeds)
    if total > config.EMBED_TOTAL_LIMIT:
        problems.append(f"embed text totals {total} chars (limit {config.EMBED_TOTAL_LIMIT})")

    attachments = payload.get("attachments") or []
    if len(attachments) > ATTACHMENT_COUNT_LIMIT:
        problems.append(f"{len(attachments)} attachments (limit {ATTACHMENT_COUNT_LIMIT})")
    filenames = set()
    for i, attachment in enumerate(attachments):
        if not isinstance(attachment.get("id"), int):
            problems.append(f"attachments[{i}].id must be the int matching files[n]")
        if not attachment.get("filename"):
            problems.append(f"attachments[{i}] has no filename")
        if len(attachment.get("description") or "") > ATTACHMENT_DESC_LIMIT:
            problems.append(f"attachments[{i}].description over {ATTACHMENT_DESC_LIMIT}")
        filenames.add(attachment.get("filename"))
    for missing in referenced - filenames:
        problems.append(f"embed references attachment://{missing} with no matching attachment")

    return problems


# --------------------------------------------------------------------------
# plain-text edition (the shape-independent last rung)
# --------------------------------------------------------------------------


def render_text_edition(edition: dict) -> str:
    """The paper as plain Discord markdown — no embeds, no masked links, no tables."""
    lead = edition.get("lead") or {}
    folio = (
        f"For the Fellers · No. {edition.get('edition_number', '?')} · "
        f"Vol. {edition.get('volume', 'I')} · {_long_date(edition['edition_date'])}"
    )
    blocks = [f"# \U0001f4f0 {config.MASTHEAD}\n-# {folio}"]

    headline = (lead.get("headline") or "").strip()
    if headline:
        opener = f"## {headline}"
        if lead.get("dek"):
            opener += f"\n*{lead['dek'].strip()}*"
        blocks.append(opener)
    blocks.extend(p.strip() for p in (lead.get("body") or []) if (p or "").strip())
    strip = _stat_strip_line(lead.get("stat_strip") or [])
    if strip:
        blocks.append(f"-# {strip}")

    present = _present_sections(edition)
    for section in sorted(config.SECTIONS, key=lambda s: s["order"]):
        if section["id"] not in present:
            continue
        blocks.append(f"## {_section_title(edition, section)}".strip())
        for brief in _briefs_for(edition, section["id"]):
            lines = [f"**{(brief.get('headline') or '').strip()}**"]
            summary = (brief.get("summary") or "").strip()
            if summary:
                lines.append(summary)
            source, url = (brief.get("source") or "").strip(), (brief.get("url") or "").strip()
            if source and url:
                lines.append(f"-# {source} <{url}>")
            elif source:
                lines.append(f"-# {source}")
            blocks.append("\n".join(lines))
        if section["id"] == WV_SECTION_ID:
            blocks.extend(_text_notebook_blocks(edition))

    for closer in (edition.get("kicker"), edition.get("sources_note"), weather_ear(edition)):
        if closer:
            blocks.append(f"-# {str(closer).strip()}")
    return "\n\n".join(blocks)


def _text_notebook_blocks(edition: dict) -> list[str]:
    """The notebook's three optional parts in plain markdown, one block each.

    Same content as the embed fields, with the masked links unwound into bare
    angle-bracketed urls — `[AP](url)` is inert outside an embed.
    """
    blocks: list[str] = []
    for key in WV_FIELD_KEYS:
        entries = [e for e in _wv_entries(edition, key) if isinstance(e, dict)]
        if not entries:
            continue
        lines = [f"### {config.WV_SUBHEADS[key]}"]
        for entry in entries:
            if key == "fishing":
                water = str(entry.get("water") or "").strip()
                line = str(entry.get("line") or "").strip()
                source = str(entry.get("source") or "").strip()
                text = f"**{water}** — {line}" if water and line else (water or line)
                lines.append(f"{text} · {source}" if source else text)
                continue
            place = str(entry.get("place") or entry.get("region_id") or "").strip()
            item = str(entry.get("item") or "").strip()
            text = f"**{place}{_people_tag(entry)}** — {item}" if place and item else (place or item)
            source, url = (entry.get("source") or "").strip(), (entry.get("url") or "").strip()
            if source and url:
                text = f"{text} · {source} <{url}>"
            elif source:
                text = f"{text} · {source}"
            lines.append(text)
        blocks.append("\n".join(lines))
    return blocks


def split_message(text: str, limit: int = config.CHUNK_LIMIT) -> list[str]:
    """Split on paragraph boundaries so no chunk exceeds Discord's content limit."""
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current = ""
    for para in paragraphs:
        while len(para) > limit:
            cut = para.rfind("\n", 0, limit)
            cut = cut if cut > 0 else limit
            piece, para = para[:cut], para[cut:].lstrip("\n")
            if current:
                chunks.append(current)
                current = ""
            chunks.append(piece)
        candidate = f"{current}\n\n{para}" if current else para
        if len(candidate) > limit:
            chunks.append(current)
            current = para
        else:
            current = candidate
    if current.strip():
        chunks.append(current)
    return chunks


# --------------------------------------------------------------------------
# transport
# --------------------------------------------------------------------------


def _wait_url(webhook_url: str) -> str:
    """?wait=true makes Discord return the created message, so we can log its id."""
    joiner = "&" if "?" in webhook_url else "?"
    return f"{webhook_url}{joiner}wait=true"


def build_multipart(payload: dict, filename: str, file_bytes: bytes) -> tuple[bytes, str]:
    """Assemble the exact multipart/form-data body Discord documents.

    payload_json holds the JSON body; files[0] holds the image; the payload's
    attachments[0].id == 0 is what binds them together.
    """
    boundary = f"----AshgroveTimes{uuid.uuid4().hex}"
    extension = os.path.splitext(filename)[1].lower()
    mime = MIME_TYPES.get(extension, "application/octet-stream")
    dash = f"--{boundary}\r\n".encode()

    body = bytearray()
    body += dash
    body += b'Content-Disposition: form-data; name="payload_json"\r\n'
    body += b"Content-Type: application/json\r\n\r\n"
    body += json.dumps(payload, ensure_ascii=False).encode("utf-8")
    body += b"\r\n"
    body += dash
    body += f'Content-Disposition: form-data; name="files[0]"; filename="{filename}"\r\n'.encode()
    body += f"Content-Type: {mime}\r\n\r\n".encode()
    body += file_bytes
    body += b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    return bytes(body), f"multipart/form-data; boundary={boundary}"


def _http_post(url: str, body: bytes, content_type: str) -> tuple[int, dict | None, dict]:
    """POST raw bytes. Status 0 means the request never completed.

    Uses requests when importable and stdlib urllib when it is not, so delivery
    never depends on pip succeeding in the sandbox.
    """
    headers = {"Content-Type": content_type, "User-Agent": config.USER_AGENT}
    if requests is not None:
        try:
            response = requests.post(url, data=body, headers=headers, timeout=HTTP_TIMEOUT)
        # requests embeds the full request URL — token and all — in most of its
        # transport exceptions, so the string is scrubbed before it can be
        # returned, let alone printed. `url` here already carries ?wait=true.
        except Exception as exc:  # transport failure, not an HTTP status
            return 0, {"_error": _scrub(exc, url)}, {}
        try:
            parsed = response.json()
        except ValueError:
            parsed = None
        return response.status_code, parsed, dict(response.headers)

    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            raw = response.read()
            return response.status, _parse_json(raw), dict(response.headers)
    except urllib.error.HTTPError as exc:
        return exc.code, _parse_json(exc.read()), dict(exc.headers or {})
    except Exception as exc:
        # urllib's URLError repr can carry the full url too.
        return 0, {"_error": _scrub(exc, url)}, {}


def _parse_json(raw: bytes) -> dict | None:
    try:
        return json.loads(raw.decode("utf-8")) if raw else None
    except (ValueError, UnicodeDecodeError):
        return None


def _http_json(method: str, url: str, payload: dict | None = None) -> tuple[int, dict | None]:
    """GET or PATCH JSON. Used only for editing messages already sent.

    Separate from _http_post because that one carries multipart bodies and
    retry logic this does not need. Same scrubbing discipline: the url is the
    credential, so no exception string escapes unredacted.
    """
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"User-Agent": config.USER_AGENT}
    if body is not None:
        headers["Content-Type"] = "application/json"

    if requests is not None:
        try:
            response = requests.request(method, url, data=body, headers=headers,
                                        timeout=HTTP_TIMEOUT)
        except Exception as exc:
            return 0, {"_error": _scrub(exc, url)}
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, None

    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT) as response:
            return response.status, _parse_json(response.read())
    except urllib.error.HTTPError as exc:
        return exc.code, _parse_json(exc.read())
    except Exception as exc:
        return 0, {"_error": _scrub(exc, url)}


def page_is_live(page_url: str) -> bool:
    """True when the permalink actually serves. A 404 means Pages has not
    finished publishing this edition yet; anything else (403, timeout) is
    treated as not-yet rather than as proof of life."""
    status, _ = _http_json("GET", page_url)
    return status == 200


def backfill_page_url(
    webhook_url: str,
    edition: dict,
    page_url: str,
    message_ids: list[str],
    image_filename: str | None,
) -> tuple[bool, list[str]]:
    """Add the permalink to messages that were already posted without it.

    GitHub Pages build lag is unbounded in practice — measured at 23s one
    evening and 8m38s the next morning, because the Actions queue does not
    care about our 7:00 deadline. Waiting for it before posting would push
    the paper past the Weatherman it is supposed to precede. So the paper
    goes out on time linkless and the link is patched in when the page is
    genuinely live, which readers see as a normal Discord edit.

    Rebuilds the payload exactly as a linked post would have been, then
    carries over each live embed's resolved image url: after posting, Discord
    has rewritten `attachment://x.png` to a CDN link, and sending the
    original attachment:// form back on an edit drops the hero card.
    `attachments` is deliberately never sent — omitting it retains what is
    already on the message.
    """
    notes: list[str] = []

    # CONTENT ONLY, deliberately. Rebuilding the embeds to carry section
    # anchors would grow the payload by the length of every url, which can
    # tip a one-message edition over the ceiling and make the trim ladder cut
    # briefs that are ALREADY PUBLISHED. A backfill must only ever add. The
    # content line is also where the link is actually legible.
    if len(message_ids) == 1:
        contents = [_masthead_line(edition, page_url)]
    elif len(message_ids) == 2:
        contents = [_masthead_line(edition, page_url), _inside_line(page_url)]
    else:
        notes.append(
            f"backfill skipped: {len(message_ids)} messages recorded, which is "
            "neither the one-message nor the split shape"
        )
        return False, notes

    for message_id, content in zip(message_ids, contents):
        status, _ = _http_json(
            "PATCH", f"{webhook_url}/messages/{message_id}", {"content": content})
        if status not in (200, 204):
            notes.append(f"backfill: edit failed on {message_id} (HTTP {status})")
            return False, notes

    notes.append(f"permalink added to {len(message_ids)} message(s) after the Pages build finished")
    return True, notes


def _retry_after_seconds(data: dict | None, headers: dict, default: float = 5.0) -> float:
    if isinstance(data, dict) and data.get("retry_after") is not None:
        try:
            return min(float(data["retry_after"]), 60.0)
        except (TypeError, ValueError):
            pass
    header = headers.get("Retry-After") or headers.get("retry-after")
    try:
        return min(float(header), 60.0)
    except (TypeError, ValueError):
        return default


def send_message(
    webhook_url: str,
    payload: dict,
    attachment: tuple[str, bytes] | None = None,
    long_retry: bool = True,
) -> Result:
    """POST one message, honoring 429 retry_after and backing off on 5xx.

    4xx other than 429 returns immediately — the caller decides whether a 400
    means "fall through to text mode" or a 401/404 means "the webhook is dead".
    """
    final = _finalize(payload)
    if attachment:
        filename, file_bytes = attachment
        body, content_type = build_multipart(final, filename, file_bytes)
    else:
        body = json.dumps(final, ensure_ascii=False).encode("utf-8")
        content_type = "application/json"

    url = _wait_url(webhook_url)
    rate_limited = 0
    server_errors = 0
    long_retry_used = not long_retry

    while True:
        status, data, headers = _http_post(url, body, content_type)
        if 200 <= status < 300:
            message_id = str(data.get("id")) if isinstance(data, dict) and data.get("id") else None
            return Result(True, status, message_id)

        if status == 429 and rate_limited < RATE_LIMIT_ATTEMPTS:
            rate_limited += 1
            wait = _retry_after_seconds(data, headers)
            print(f"WARN: rate limited, waiting {wait:.1f}s", file=sys.stderr)
            time.sleep(wait)
            continue

        if status == 0 or status >= 500:
            if server_errors < SERVER_ERROR_ATTEMPTS:
                server_errors += 1
                wait = 2**server_errors
                print(f"WARN: webhook returned {status}, retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if not long_retry_used:
                long_retry_used = True
                print(
                    f"WARN: webhook still {status}; one final attempt in {LONG_RETRY_WAIT}s",
                    file=sys.stderr,
                )
                time.sleep(LONG_RETRY_WAIT)
                continue

        detail = ""
        if isinstance(data, dict):
            detail = data.get("_error") or json.dumps(data, ensure_ascii=False)[:400]
        # Second pass with the real webhook in scope: Result.detail is printed
        # and logged by every caller, so it leaves here already safe.
        return Result(False, status, None, _scrub(detail, webhook_url))


# --------------------------------------------------------------------------
# edition, ledger, degraded-path log
# --------------------------------------------------------------------------


def load_edition(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _index_path() -> str:
    return _repo("editions", "index.json")


def load_index() -> dict:
    try:
        with open(_index_path(), encoding="utf-8") as f:
            index = json.load(f)
    except (OSError, ValueError):
        return {"volume": "I", "editions": []}
    index.setdefault("volume", "I")
    index.setdefault("editions", [])
    return index


def find_record(index: dict, date: str) -> dict | None:
    for record in index.get("editions") or []:
        if record.get("date") == date:
            return record
    return None


def _run_backfill(args, edition: dict) -> int:
    """`--backfill-link`: wait out the Pages build, then add the permalink.

    Idempotent and safe to run twice — a row that already carries a page_url
    is left alone, and nothing here can post a new message.
    """
    if not config.PAGES_ENABLED:
        print("SKIP: PAGES_ENABLED is False, nothing to link", file=sys.stderr)
        return 0

    row = find_record(load_index(), args.date)
    if not row or not row.get("posted"):
        print(f"ERROR: no posted edition recorded for {args.date}", file=sys.stderr)
        return 1
    if row.get("page_url"):
        print(f"OK: {args.date} already carries its permalink; nothing to do")
        return 0

    message_ids = list(row.get("message_ids") or [])
    if not message_ids:
        print(f"ERROR: no message ids recorded for {args.date}", file=sys.stderr)
        return 1

    page_url = args.page_url or config.page_url(args.date)
    deadline = time.monotonic() + max(0, args.backfill_wait)
    attempt = 0
    while True:
        if page_is_live(page_url):
            break
        if time.monotonic() >= deadline:
            print(
                f"GAVE UP: {page_url} still not serving after "
                f"{args.backfill_wait}s - the edition stays linkless",
                file=sys.stderr,
            )
            log_failures(args.date, [f"backfill gave up after {args.backfill_wait}s"])
            return 1
        attempt += 1
        # Long-ish, evenly spaced: this is a build queue, not a flaky request,
        # and nobody is waiting on the answer.
        time.sleep(min(30, 10 * attempt))

    if args.dry_run:
        print(f"DRY RUN: {page_url} is live; would edit {len(message_ids)} message(s)")
        return 0

    var = "DISCORD_TEST_WEBHOOK_URL" if args.test else "DISCORD_WEBHOOK_URL"
    webhook_url = load_env_webhook(var)
    if not webhook_url:
        print(f"ERROR: {var} not set (env or .env)", file=sys.stderr)
        return 1
    remember_webhook(webhook_url)  # nothing printed past here carries the token

    image_filename = row.get("hero") and f"ashgrove-{args.date}.png" or None
    ok, notes = backfill_page_url(
        webhook_url, edition, page_url, message_ids, image_filename)
    for note in notes:
        print(("OK: " if ok else "WARN: ") + _scrub(note), file=sys.stderr if not ok else sys.stdout)
    if not ok:
        log_failures(args.date, notes)
        return 1

    record_edition(args.date, {"date": args.date, "page_url": page_url,
                               "link_backfilled": True})
    print(f"OK: permalink added to {args.date} ({len(message_ids)} message(s))")
    return 0


def record_edition(date: str, record: dict) -> None:
    """Append or update this date's ledger row. This module is its only writer.

    editions/index.json is committed and may go public with the repo, so the
    degraded notes are scrubbed here rather than trusting every caller.
    """
    record = dict(record)
    if isinstance(record.get("degraded"), list):
        record["degraded"] = [_scrub(note) for note in record["degraded"]]
    index = load_index()
    existing = find_record(index, date)
    if existing:
        existing.update(record)
    else:
        index["editions"].append(record)
    index["editions"].sort(key=lambda r: r.get("date", ""))
    os.makedirs(os.path.dirname(_index_path()), exist_ok=True)
    with open(_index_path(), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write("\n")


def log_failures(date: str, notes: list[str]) -> None:
    """One dated line per degraded path, so slow quality drift stays visible."""
    if not notes:
        return
    path = _repo("docs", "FAILURES.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    new_file = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if new_file:
            f.write("# Degraded paths\n\nAppend-only. One line per degraded path taken.\n\n")
        for note in notes:
            # docs/FAILURES.md is committed; a transport error quoted into a
            # note must never carry the webhook token into the repo.
            f.write(f"- {_utc_stamp()} · {date} · post_discord: {_scrub(note)}\n")


def write_payload_file(date: str, messages: list[dict]) -> str:
    """Persist the exact JSON body sent, so a failed run is still recoverable."""
    path = _repo("out", f"{date}.payload.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    finalized = [_finalize(m) for m in messages]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(finalized[0] if len(finalized) == 1 else finalized, f, indent=2,
                  ensure_ascii=False)
        f.write("\n")
    return path


def resolve_attachment(date: str, requested: str | None) -> tuple[tuple[str, bytes] | None, list[str]]:
    """Hero card, else the committed masthead banner, else nothing.

    The filename sent is always derived from --date, never from the input
    path's basename, because the lead embed's attachment:// url is built from
    the same derivation.
    """
    notes: list[str] = []
    hero_path = requested or _repo("out", f"ashgrove-{date}.png")
    extension = os.path.splitext(hero_path)[1].lower()
    extension = extension if extension in IMAGE_EXTENSIONS else ".png"
    filename = f"ashgrove-{date}{extension}"

    for index, path in enumerate((hero_path, _repo("assets", "masthead-fallback.png"))):
        if not path or not os.path.exists(path):
            continue
        with open(path, "rb") as f:
            data = f.read()
        if len(data) > config.ATTACH_BYTE_BUDGET:
            notes.append(
                f"{os.path.basename(path)} is {len(data)} bytes "
                f"(budget {config.ATTACH_BYTE_BUDGET}) - not attached"
            )
            continue
        if index:
            notes.append("hero card unavailable; attached the static masthead banner")
            filename = f"ashgrove-{date}.png"
        return (filename, data), notes

    notes.append("no image attached; posting embeds only")
    return None, notes


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _post_text_edition(
    webhook_url: str,
    chunks: list[str],
    long_retry: bool,
    on_sent=None,
) -> tuple[list[str], str | None]:
    """Rung 7: ugly, unmistakably still the paper, delivered.

    `on_sent(count, message_id)` fires after EACH chunk lands so the caller can
    write the ledger row before the next one is attempted. Chunk 4 of 5 failing
    must not leave chunks 1-3 unrecorded and therefore re-postable.
    """
    ids: list[str] = []
    for i, chunk in enumerate(chunks):
        result = send_message(webhook_url, {"content": chunk}, long_retry=long_retry)
        if not result.ok:
            return ids, f"text mode failed with HTTP {result.status}: {_scrub(result.detail)}"
        if result.message_id:
            ids.append(result.message_id)
        if on_sent:
            on_sent(i + 1, result.message_id)
        if i < len(chunks) - 1:
            time.sleep(1)
    return ids, None


def _force_utf8_console() -> None:
    """Windows consoles default to cp1252 and would crash --dry-run on the emoji."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def main() -> int:
    _force_utf8_console()
    parser = argparse.ArgumentParser(description="Post one Ashgrove Times edition to Discord.")
    parser.add_argument("--date", required=True, help="edition date, YYYY-MM-DD")
    parser.add_argument("--edition", help="edition JSON (default editions/<date>.json)")
    parser.add_argument("--attach", help="hero PNG (default out/ashgrove-<date>.png)")
    parser.add_argument("--page-url", help="verified GitHub Pages permalink for this edition")
    parser.add_argument("--test", action="store_true", help="post to DISCORD_TEST_WEBHOOK_URL")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the exact payload and post nothing")
    parser.add_argument("--no-image", action="store_true", help="send the embeds with no attachment")
    parser.add_argument("--text", action="store_true",
                        help="post the plain-text edition instead of embeds")
    parser.add_argument("--split", action="store_true",
                        help="on an oversized edition, split into FRONT PAGE "
                             "and INSIDE rather than trimming news to fit one "
                             "message (see config.PREFER_SPLIT_OVER_TRIM)")
    parser.add_argument("--backfill-link", action="store_true",
                        help="post nothing; wait for the Pages build and add "
                             "the permalink to the edition already posted for "
                             "--date. Run this after posting when the page was "
                             "not live in time.")
    parser.add_argument("--backfill-wait", type=int, default=config.PAGES_BACKFILL_WAIT_SECONDS,
                        help="seconds to wait for the Pages build during "
                             "--backfill-link (default %(default)s)")
    parser.add_argument("--force", action="store_true",
                        help="post even if this date is already recorded as posted")
    args = parser.parse_args()

    try:
        dt.date.fromisoformat(args.date)
    except ValueError:
        print(f"ERROR: --date {args.date!r} is not YYYY-MM-DD", file=sys.stderr)
        return 1

    edition_path = args.edition or _repo("editions", f"{args.date}.json")
    try:
        edition = load_edition(edition_path)
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot read edition {edition_path}: {exc}", file=sys.stderr)
        return 1
    if edition.get("edition_date") != args.date:
        print(
            f"ERROR: {edition_path} is dated {edition.get('edition_date')!r}, not {args.date!r}",
            file=sys.stderr,
        )
        return 1

    if args.backfill_link:
        return _run_backfill(args, edition)

    if not args.dry_run and not args.force:
        prior = find_record(load_index(), args.date)
        if prior and prior.get("posted"):
            print(
                f"SKIP: edition {args.date} already posted "
                f"(message {prior.get('message_id')}) - use --force to repost"
            )
            return 0

    degraded: list[str] = []
    attachment: tuple[str, bytes] | None = None
    if args.no_image or args.text:
        degraded.append("image suppressed by flag")
    else:
        attachment, notes = resolve_attachment(args.date, args.attach)
        degraded.extend(notes)

    page_url = args.page_url if (config.PAGES_ENABLED and args.page_url) else None
    if args.page_url and not config.PAGES_ENABLED:
        degraded.append("PAGES_ENABLED is False; permalink omitted")
    elif config.PAGES_ENABLED and not args.page_url:
        degraded.append("no verified page url; posting without links")

    image_filename = attachment[0] if attachment else None
    text_mode = args.text
    messages: list[dict] = []

    if not text_mode:
        # Trimming to fit ONE message costs news; splitting into two costs
        # only a second post. On a full day the trimmer eats the West
        # Virginia notebook first, which is the section the readers actually
        # showed up for — so when the untrimmed edition will not fit, try the
        # split BEFORE reaching for the scissors. Each half then gets its own
        # fresh budget and usually needs no trimming at all.
        prefer_split = args.split or getattr(config, "PREFER_SPLIT_OVER_TRIM", False)
        untrimmed = build_payload(edition, image_filename, page_url)
        oversized = embed_text_length(untrimmed["embeds"]) > config.EMBED_HARD

        if prefer_split and oversized:
            split_notes: list[str] = []
            messages = split_payloads(edition, image_filename, page_url, split_notes)
            degraded.append("split into FRONT PAGE and INSIDE messages to keep the notebook whole")
            degraded.extend(n for n in split_notes if n not in degraded)
        else:
            working, payload, trim_notes = build_within_budget(
                edition, image_filename, page_url)
            degraded.extend(trim_notes)
            if embed_text_length(payload["embeds"]) > config.EMBED_HARD:
                split_notes = []
                messages = split_payloads(working, image_filename, page_url, split_notes)
                degraded.append("split into FRONT PAGE and INSIDE messages")
                # The split rebuilds the same edition, so its notebook notes
                # repeat what build_within_budget already reported. Keep once.
                degraded.extend(n for n in split_notes if n not in degraded)
            else:
                messages = [payload]
        for message in messages:
            degraded.extend(clamp_payload(message))

        problems: list[str] = []
        for i, message in enumerate(messages):
            problems.extend(f"message[{i}]: {p}" for p in validate_payload(message))
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            print("ERROR: embed payload refused; falling back to text mode", file=sys.stderr)
            degraded.append("embed payload failed validation; posted as text")
            text_mode = True
            attachment, image_filename = None, None

    if text_mode:
        chunks = split_message(render_text_edition(edition))
        messages = [{"content": chunk} for chunk in chunks]
        problems = []
        for i, message in enumerate(messages):
            problems.extend(f"message[{i}]: {p}" for p in validate_payload(message))
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}", file=sys.stderr)
            return 1

    payload_file = write_payload_file(args.date, messages)

    if args.dry_run:
        for i, message in enumerate(messages, 1):
            print(f"--- message {i} of {len(messages)} ---")
            print(json.dumps(_finalize(message), indent=2, ensure_ascii=False))
        if attachment:
            print(f"--- attachment: {attachment[0]} ({len(attachment[1])} bytes) ---")
        else:
            print("--- attachment: none ---")
        for message in messages:
            print(f"embed chars: {embed_text_length(message.get('embeds') or [])}", file=sys.stderr)
        print(f"payload written to {payload_file}", file=sys.stderr)
        for note in degraded:
            print(f"DEGRADED: {note}", file=sys.stderr)
        return 0

    var = "DISCORD_TEST_WEBHOOK_URL" if args.test else "DISCORD_WEBHOOK_URL"
    webhook_url = load_env_webhook(var)
    if not webhook_url:
        print(f"ERROR: {var} not set (env or .env)", file=sys.stderr)
        return 1
    remember_webhook(webhook_url)  # nothing printed or logged past here carries the token

    long_retry = not args.test
    embed_chars = sum(embed_text_length(m.get("embeds") or []) for m in messages)
    delivery_mode = "text" if text_mode else "embeds"
    message_ids: list[str] = []
    sent = 0

    def save(posted: bool) -> None:
        """Write the ledger row for exactly what is in the channel right now.

        Called after EVERY successful send, not once at the end. A run that
        dies on message 2 of 3 used to return 1 with no row at all, so the next
        run saw `posted: False`, re-sent message 1, and the group read the front
        page twice. `messages_sent` + `mode` + `message_count` is what a re-run
        needs to resume instead of repeat.
        """
        record_edition(
            args.date,
            {
                "date": args.date,
                "number": edition.get("edition_number"),
                "posted": posted,
                "message_id": message_ids[0] if message_ids else None,
                "message_ids": list(message_ids),
                "messages_sent": sent,
                "message_count": len(messages),
                "mode": delivery_mode,
                "page_url": page_url,
                "hero": bool(attachment) and not text_mode,
                "embed_chars": 0 if text_mode else embed_chars,
                "degraded": degraded,
            },
        )

    # Resume or refuse, using the incremental row a previous run left behind.
    prior = find_record(load_index(), args.date)
    prior_sent = int((prior or {}).get("messages_sent") or 0)
    if prior and prior_sent and not args.force:
        prior_ids = [str(m) for m in (prior.get("message_ids") or []) if m]
        same_run = (
            prior.get("mode") == delivery_mode
            and int(prior.get("message_count") or 0) == len(messages)
        )
        if same_run and prior_sent >= len(messages):
            print(
                f"SKIP: edition {args.date} is already fully delivered "
                f"({prior_sent} {delivery_mode} message(s): "
                f"{', '.join(prior_ids) or 'ids unrecorded'}) - use --force to repost"
            )
            message_ids, sent = prior_ids, prior_sent
            save(posted=True)  # heal a row whose final write never landed
            return 0
        if same_run:
            sent, message_ids = prior_sent, prior_ids
            note = (
                f"resumed a partial delivery: {sent} of {len(messages)} {delivery_mode} "
                f"message(s) were already in the channel"
            )
            degraded.append(note)
            print(f"WARN: {note}", file=sys.stderr)
        else:
            print(
                f"ERROR: {args.date} has a partial delivery in the ledger - {prior_sent} of "
                f"{prior.get('message_count')} {prior.get('mode')} message(s) already sent "
                f"({', '.join(prior_ids) or 'ids unrecorded'}) - but this run would send "
                f"{len(messages)} {delivery_mode} message(s), so they cannot be matched up. "
                f"Delete the messages in Discord and re-run with --force, or fix the row in "
                f"editions/index.json.",
                file=sys.stderr,
            )
            log_failures(
                args.date,
                degraded
                + [
                    f"refused: {prior_sent} {prior.get('mode')} message(s) already sent for "
                    f"this date do not match this run's {len(messages)} {delivery_mode} message(s)"
                ],
            )
            return 1

    for i, message in enumerate(messages):
        if i < sent:
            continue  # already in the channel; never post it twice
        file_part = attachment if (i == 0 and message.get("attachments")) else None
        result = send_message(webhook_url, message, file_part, long_retry=long_retry)
        if not result.ok:
            detail = _scrub(result.detail)
            print(f"ERROR: HTTP {result.status} from webhook: {detail}", file=sys.stderr)
            if result.status == 400 and not text_mode:
                degraded.append(f"Discord rejected the embeds (400); posted as text: {detail[:120]}")
                if sent:
                    degraded.append(
                        f"{sent} embed message(s) were already in the channel when Discord "
                        f"400'd; the text edition follows them"
                    )
                chunks = split_message(render_text_edition(edition))
                text_mode = True
                delivery_mode = "text"
                messages = [{"content": chunk} for chunk in chunks]
                sent = 0

                def text_progress(count: int, message_id: str | None) -> None:
                    nonlocal sent
                    sent = count
                    if message_id:
                        message_ids.append(message_id)
                    save(posted=False)

                ids, failure = _post_text_edition(
                    webhook_url, chunks, long_retry, on_sent=text_progress
                )
                if failure:
                    print(f"ERROR: {failure}", file=sys.stderr)
                    save(posted=False)
                    log_failures(args.date, degraded + [failure])
                    return 1
                if not message_ids:
                    message_ids = ids
                break
            save(posted=False)
            log_failures(args.date, degraded + [f"delivery failed with HTTP {result.status}"])
            return 1
        if result.message_id:
            message_ids.append(result.message_id)
        sent = i + 1
        save(posted=False)
        if i < len(messages) - 1:
            time.sleep(1)

    save(posted=True)
    log_failures(args.date, degraded)

    where = "TEST channel" if args.test else "live channel"
    mode = "text mode" if text_mode else f"{len(messages)} message(s), {embed_chars} embed chars"
    hero = attachment[0] if (attachment and not text_mode) else "none"
    print(
        f"OK: Edition No. {edition.get('edition_number')} - {args.date} posted to {where} "
        f"({mode}, hero {hero}, link {'yes' if page_url else 'no'}); payload at {payload_file}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
