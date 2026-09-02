"""Post the one morning message — the digest — for an Ashgrove Times edition.

`editions/YYYY-MM-DD.json` is the ONLY input. The payload is built here and
never hand-authored, so the daily routine's one creative act is writing the
edition file — everything in this module is deterministic and re-runnable with
no model in the loop.

Since 2026-08-25 the channel gets a doorbell, not the paper (Nate: "let's
just have one post that links to the index page"). The message is ONE embed
— the lead headline and dek, a contents list of the sections with their top
headlines, a Sports & Sportsman tease, and a link to Home — sent as
multipart/form-data to `{webhook}?wait=true` with the hero card as files[0].
Nothing in it can approach Discord's 6,000-character ceiling, so there is no
trim ladder, no split and no text mode: the thirteen functions that served
the full-embed paper were deleted on 2026-09-02, a fortnight after the last
one ran, because dead code with a signpost is a trap for a 5:30 reader.

    python post_discord.py --date 2026-09-02 --digest --dry-run
    python post_discord.py --date 2026-09-02 --digest \
        --attach out/ashgrove-2026-09-02.png --not-before 07:00

What survives of the old path is build_payload(), the six-embed builder,
because validate_edition._exact_measure() weighs each section off it — with
the masked source links — to give the desk its proportion advisory. It is
never sent. Its docstring says so.

FALLBACKS, in the order they fire: hero missing -> assets/masthead-fallback.png
-> no image at all (plain application/json POST of the same JSON) -> no Home
link -> 429/5xx retries. Only a dead webhook (401/403/404) or an unreadable
edition file stops delivery outright.

An edition already recorded `posted` in `editions/index.json` is skipped, so a
routine retry can never double-post; `--force` overrides. The ledger row is
written after the send, and `--not-before HH:MM` holds delivery to an
Eastern wall-clock time so the routine can wake early and still post at
seven.

Nothing this module prints, appends to docs/FAILURES.md or writes to the ledger
can carry the webhook token: the webhook URL *is* the credential and `requests`
puts it inside its transport exceptions, so every such string goes through
_scrub() first. The repo IS public.
"""

from __future__ import annotations

import argparse
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

# The West Virginia notebook, as build_payload() measures it. `briefs` is
# statewide and behaves like every other section; the sub-blocks are the
# local anchor Ian asked for and are the only arrays in the whole edition
# that may legally be empty. The order is fixed here; the visible subheads
# come from config so the broadsheet and this measurement use the same words.
WV_SECTION_ID = "wv"
WV_FIELD_KEYS = config.WV_ALL_SUBHEAD_KEYS

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


def _is_text(value: object) -> bool:
    """A non-empty string, whitespace not counting as content."""
    return isinstance(value, str) and bool(value.strip())


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
    printed verbatim: the Topsail water temperature is borrowed from a
    station 60 miles up the coast, and this line is where that stays honest.
    Never restate the station here — config.TOPSAIL_TEMP_* names it, and it
    has already changed once.
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
    than drops. (The trim ladder that used to take the overflow from here was
    retired with the full-embed post on 2026-09-02; this builder now only
    measures, and a measurement that dropped lines would under-read.)

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

    # Seat the parts in display order. The 25-field cap is Discord's and the
    # measurement keeps honouring it so the sizes stay those of a message
    # that could actually be sent.
    packed: dict[str, list[dict]] = {}
    notes: dict[str, str] = {}
    used = 0
    for key in WV_FIELD_KEYS:
        lines = rendered.get(key)
        if not lines:
            continue
        remaining = FIELD_COUNT_LIMIT - used
        if remaining <= 0:
            # Never emit a 26th field: Discord 400s the whole message and the
            # paper vanishes over a line that was optional to begin with.
            fields_for_key, dropped = [], list(lines)
        else:
            fields_for_key, dropped = _notebook_field(config.wv_subhead(key), lines, remaining)
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


# --------------------------------------------------- the daily digest post

# Nate, 2026-08-25: stop posting the whole paper to Discord. One message a
# morning in #the-ashgrove-times that says what is in today's edition and
# links the Home page; the reader goes to the website for the paper itself.
# Sports & Sportsman stops posting to Discord ENTIRELY — Home links it, and
# so do the nav buttons on every page, so a second post was a second
# notification for the same trip.
#
# What this buys, beyond a quieter channel: the paper stops being written
# against a 6,000-character ceiling. Four splits in eleven editions, a
# sourced wire brief cut for budget on 2026-08-22, a West Virginia notebook
# capped at six lines because that is what the embed paid for — all of that
# was Discord's shape pressing on the journalism. The website has no such
# limit and never did.
#
# The digest links HOME, not the dated edition. Home carries all three
# sections and always points at today, so one link reaches the whole paper;
# a dated permalink would reach one third of it.

DIGEST_MAX_INSIDE = 8       # section lines in the "Inside" list
DIGEST_TEASE_CHARS = 88     # per line, before the ellipsis


def _digest_tease(section: dict) -> str:
    """The first brief's headline, clipped, or "" for an empty section."""
    briefs = section.get("briefs") if isinstance(section, dict) else None
    if not isinstance(briefs, list):
        return ""
    for brief in briefs:
        if isinstance(brief, dict) and _is_text(brief.get("headline")):
            return _clip(str(brief["headline"]).strip(), DIGEST_TEASE_CHARS)
    return ""


def _digest_inside(edition: dict) -> list[str]:
    """One line per section that actually ran, label then its top headline."""
    lines: list[str] = []
    sections = edition.get("sections")
    if not isinstance(sections, list):
        return lines
    by_id = {s.get("id"): s for s in sections if isinstance(s, dict)}
    # Page reading order, not config order: the notebook and British
    # Columbia are set below the wire columns, so that is where a reader
    # meets them and that is where a contents list should put them.
    for meta in config.sections_in_reading_order(edition.get("edition_date")):
        section = by_id.get(meta["id"])
        if not section:
            continue
        tease = _digest_tease(section)
        if not tease:
            continue
        lines.append(f"{meta['emoji']}  **{meta['label']}** — {tease}")
        if len(lines) >= DIGEST_MAX_INSIDE:
            break
    return lines


def build_digest_payload(
    edition: dict,
    index_url: str | None,
    sportsman: dict | None = None,
    image_filename: str | None = None,
) -> dict:
    """The single morning message: what is in the paper, and where it is.

    ONE message, always — there is nothing here that can grow to 6,000
    characters, which is the entire point of the change. The lead headline
    is the embed title and carries the link; the section list underneath is
    a table of contents, not a summary, and deliberately does not try to be
    a substitute for reading the paper.
    """
    dek = edition.get("lead", {}).get("dek") if isinstance(
        edition.get("lead"), dict) else None
    lead = edition.get("lead") if isinstance(edition.get("lead"), dict) else {}

    body: list[str] = []
    if _is_text(dek):
        body.append(f"*{_scrub(str(dek).strip())}*")

    inside = _digest_inside(edition)
    if inside:
        body.append("")
        body.append("__**Inside today**__")
        body.extend(inside)

    if isinstance(sportsman, dict):
        tease = _sm_digest_tease(sportsman)
        if tease:
            body.append("")
            body.append(f"🏟  **Sports & Sportsman** — {tease}")

    if index_url:
        body.append("")
        body.append(f"📖  [Read today's paper]({index_url})")

    embed: dict = {
        "title": _clip(_scrub(str(lead.get("headline") or config.MASTHEAD)),
                       config.EMBED_TITLE_LIMIT),
        "description": _clip("\n".join(body), DESCRIPTION_LIMIT),
        "color": config.LEAD_COLOR,
    }
    if index_url:
        embed["url"] = index_url
    footer = _closing_footer(edition)
    if footer:
        embed["footer"] = footer
    if image_filename:
        embed["image"] = {"url": f"attachment://{image_filename}"}

    payload: dict = {
        "content": _digest_content_line(edition, index_url),
        "embeds": [embed],
    }
    if image_filename:
        payload["attachments"] = [{"id": 0, "filename": image_filename}]
    return payload


def _digest_content_line(edition: dict, index_url: str | None) -> str:
    """The line above the embed: masthead, folio, and the plain link."""
    folio = (
        f"No. {edition.get('edition_number', '?')} · "
        f"Vol. {edition.get('volume', 'I')} · "
        f"{_long_date(edition.get('edition_date') or '')}"
    )
    lines = [f"📰  **{config.MASTHEAD}** — *{config.TAGLINE}*",
             f"-# {folio}"]
    if index_url:
        lines.append(f"<{index_url}>")
    return _clip("\n".join(lines), config.CONTENT_LIMIT)


def _sm_digest_tease(sportsman: dict) -> str:
    """Sports & Sportsman's top line, for the one post that mentions it."""
    sections = sportsman.get("sections")
    if not isinstance(sections, list):
        return ""
    for section in sections:
        if not isinstance(section, dict):
            continue
        for brief in (section.get("briefs") or []):
            if isinstance(brief, dict) and _is_text(brief.get("headline")):
                return _clip(str(brief["headline"]).strip(), DIGEST_TEASE_CHARS)
    return ""


def build_payload(
    edition: dict,
    image_filename: str | None = None,
    page_url: str | None = None,
    notes: list[str] | None = None,
) -> dict:
    """Build the full six-embed paper from an edition dict. NEVER SENT.

    This is the one survivor of the full-embed delivery path retired on
    2026-09-02, and it is kept for exactly one caller:
    validate_edition._exact_measure(), which weighs every section off the
    real embed it would have been — masked source links included — to give
    the desk its proportion advisory. Approximating those sizes under-read a
    full edition by ~700 chars, which is the difference between "tighten a
    summary" and silently losing the notebook, so the measurement stays on
    the real builder. If a second caller ever appears, it is a question for
    Nate: nothing posts the whole paper to Discord any more.

    Passing image_filename=None or page_url=None yields the same payload minus
    the attachment wiring / the links — no other code path changes. Pass
    `notes` to receive a notebook line the 25-field cap could not seat.
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


def clamp_payload(payload: dict, limit: int | None = None) -> list[str]:
    """Last-resort size clamp: shorten descriptions from the back until it fits.

    A digest runs about a thousand characters, so this has never fired on
    one; it stays because validate_payload() refuses anything over the limit
    and a clamp that says what it did beats a refusal with nothing sent.
    """
    limit = config.EMBED_TOTAL_LIMIT if limit is None else limit
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
    """The Times' delivery ledger — the idempotency gate reads this row.

    editions/sportsman/index.json still exists as the record of the eleven
    mornings Sports & Sportsman posted (2026-08-15 to 08-25); nothing
    writes it any more, because that paper no longer posts.
    """
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


def _hold_until(target: str | None) -> tuple[bool, str | None]:
    """Sleep until `target` (HH:MM Eastern) so delivery lands at a fixed hour.

    The routine wakes early because the research is slow and variable —
    37 minutes one morning — but readers should get their paper at the same
    time every day, and the paper has to precede the 7:15 forecast it points
    at. So the work starts early and the POST waits.

    Returns (held, note). A target already past is not an error: the run was
    simply slower than the head start, and the paper goes out immediately.
    """
    if not target:
        return False, None
    try:
        hour, minute = (int(part) for part in target.split(":", 1))
        goal_time = dt.time(hour, minute)
    except (TypeError, ValueError):
        return False, f"could not parse --not-before {target!r}; posting now"

    now = config.now_et() if hasattr(config, "now_et") else dt.datetime.now()
    goal = now.replace(hour=goal_time.hour, minute=goal_time.minute,
                       second=0, microsecond=0)
    wait = (goal - now).total_seconds()
    if wait <= 0:
        return False, (f"--not-before {target} already passed "
                       f"({now.strftime('%H:%M')}); posting now")
    # A head start measured in hours means a misconfigured cron, not patience.
    if wait > 3 * 3600:
        return False, (f"--not-before {target} is {wait / 3600:.1f}h away; "
                       "that is not a delivery hold, posting now")
    time.sleep(wait)
    return True, f"waited {wait / 60:.0f} min to post at {target} ET"


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
    """Persist the exact JSON body sent, so any argument about what shipped
    is settled by a file rather than by somebody's memory of it."""
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


def _force_utf8_console() -> None:
    """Windows consoles default to cp1252 and would crash --dry-run on the emoji."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass



def main() -> int:
    _force_utf8_console()
    parser = argparse.ArgumentParser(
        description="Post the one-message digest for an Ashgrove Times edition.")
    parser.add_argument("--date", required=True, help="edition date, YYYY-MM-DD")
    parser.add_argument("--edition", help="edition JSON (default editions/<date>.json)")
    parser.add_argument("--attach", help="hero PNG (default out/ashgrove-<date>.png)")
    parser.add_argument("--test", action="store_true", help="post to DISCORD_TEST_WEBHOOK_URL")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the exact payload and post nothing")
    parser.add_argument("--no-image", action="store_true",
                        help="send the digest with no attachment")
    parser.add_argument("--not-before", metavar="HH:MM", default=None,
                        help="hold the post until this ET wall-clock time "
                             "(e.g. 07:00). The routine wakes early to do the "
                             "research; this is what keeps delivery at a "
                             "consistent hour. Ignored if the time has passed.")
    parser.add_argument("--digest", action="store_true",
                        help="accepted for the routine's command line; the "
                             "digest is the only message this script sends, "
                             "with or without the flag (since 2026-09-02)")
    parser.add_argument("--digest-sportsman", metavar="PATH", default=None,
                        help="Sports & Sportsman edition JSON to tease inside "
                             "the digest (default editions/sportsman/<date>."
                             "json when it exists). That paper does not post "
                             "to Discord; this line is how it is announced.")
    parser.add_argument("--index-url", default=None,
                        help="Home url the digest links (default "
                             "config.home_url()). HOME, not the dated "
                             "edition: it reaches all three sections.")
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
    if args.no_image:
        degraded.append("image suppressed by flag")
    else:
        attachment, notes = resolve_attachment(args.date, args.attach)
        degraded.extend(notes)
    image_filename = attachment[0] if attachment else None

    # One message, always. Nothing in a digest can reach 6,000 chars, so
    # there is no trim ladder, no split, and no budget to write against.
    sm_path = args.digest_sportsman or _repo(
        "editions", "sportsman", f"{args.date}.json")
    sportsman_edition = None
    if os.path.exists(sm_path):
        try:
            sportsman_edition = load_edition(sm_path)
        except (OSError, ValueError) as exc:
            degraded.append(
                f"could not read {os.path.basename(sm_path)} for the "
                f"digest tease ({exc}); posting without it")
    else:
        degraded.append(
            "no Sports & Sportsman edition found for the digest tease")
    index_url = args.index_url or (
        config.home_url() if config.PAGES_ENABLED else None)
    if not index_url:
        degraded.append("PAGES_ENABLED is False; digest posted without its link")
    payload = build_digest_payload(
        edition, index_url, sportsman_edition, image_filename)
    degraded.extend(clamp_payload(payload))

    problems = validate_payload(payload)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        print("ERROR: digest payload refused; nothing sent", file=sys.stderr)
        log_failures(args.date, degraded + ["digest payload failed validation; nothing sent"])
        return 1

    payload_file = write_payload_file(args.date, [payload])

    if args.dry_run:
        print("--- message 1 of 1 ---")
        print(json.dumps(_finalize(payload), indent=2, ensure_ascii=False))
        if attachment:
            print(f"--- attachment: {attachment[0]} ({len(attachment[1])} bytes) ---")
        else:
            print("--- attachment: none ---")
        print(f"embed chars: {embed_text_length(payload.get('embeds') or [])}", file=sys.stderr)
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

    held, hold_note = _hold_until(args.not_before)
    if hold_note:
        print(f"{'HELD' if held else 'WARN'}: {hold_note}", file=sys.stderr)
        if not held:
            degraded.append(hold_note)

    embed_chars = embed_text_length(payload.get("embeds") or [])
    message_ids: list[str] = []

    def save(posted: bool) -> None:
        """The ledger row for exactly what is in the channel right now.

        Same keys the full-embed path wrote, so the watchdog and anything
        else reading editions/index.json sees one shape across the archive.
        """
        record_edition(
            args.date,
            {
                "date": args.date,
                "number": edition.get("edition_number"),
                "posted": posted,
                "message_id": message_ids[0] if message_ids else None,
                "message_ids": list(message_ids),
                "messages_sent": len(message_ids),
                "message_count": 1,
                "mode": "embeds",
                "page_url": index_url,
                "hero": bool(attachment),
                "embed_chars": embed_chars,
                "degraded": degraded,
            },
        )

    result = send_message(webhook_url, payload, attachment, long_retry=not args.test)
    if not result.ok:
        detail = _scrub(result.detail)
        print(f"ERROR: HTTP {result.status} from webhook: {detail}", file=sys.stderr)
        save(posted=False)
        log_failures(args.date, degraded + [f"delivery failed with HTTP {result.status}: {detail[:120]}"])
        return 1
    if result.message_id:
        message_ids.append(result.message_id)
    save(posted=True)
    log_failures(args.date, degraded)

    where = "TEST channel" if args.test else "live channel"
    hero = attachment[0] if attachment else "none"
    print(
        f"OK: Edition No. {edition.get('edition_number')} - {args.date} digest posted to "
        f"{where} ({embed_chars} embed chars, hero {hero}, "
        f"link {'yes' if index_url else 'no'}); payload at {payload_file}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
