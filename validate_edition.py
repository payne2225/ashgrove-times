"""The hard gate between what Claude wrote and what the group reads.

An edition JSON is the routine's only creative output; everything downstream
is deterministic. So this is the one place that can catch a fabricated market
number, a section the model quietly dropped, a `[headline here]` stub, or a
brief so long it would blow a Discord field. Non-zero exit means the pipeline
stops — a missing paper is recoverable, a wrong one is not.

    python validate_edition.py editions/2026-08-05.json --stats out/stats.json
    python validate_edition.py editions/_fixture.json --no-urls --no-stats

Exit 0 = clean, exit 1 = fail. Problems print as `ERROR: ...` on stderr;
non-fatal advisories print as `WARN: ...` and only fail the run under
`--strict`.

Five rules here are load-bearing and worth stating plainly:

1. STAT TRUTH. A stat_strip entry may exist only if its label AND value
   byte-match an entry in out/stats.json, and that file must be no older
   than the edition it is published under. Numbers the model "remembers" —
   or yesterday's numbers reprinted under today's date — are the single
   most damaging failure this paper can ship, so they are a hard error, not
   a warning.
2. LINKS NEVER FAIL AN EDITION, AND ARE NEVER DELETED ON A GUESS. Only a
   real 404 is a dead link, and only a 404 is STRIPPED from the brief — the
   brief keeps its source name — and the strip is logged. 403 and 405 count
   as ALIVE: paywalls and a restricted sandbox both produce 403s. A
   connection-level failure is INCONCLUSIVE and never strips anything: the
   small regional outlets the West Virginia notebook runs on are exactly
   the hosts a restricted sandbox refuses, and a live link deleted from the
   committed edition is worse than a dead one left in.
3. FISHING TRUTH. A fishing line may name only a water fetch_fishing.py
   actually reports, and only on a day that fetcher got a reading. A source
   that failed produces no line — never an invented one. EVERY NUMBER the
   line prints has to be a number that fetcher wrote for that water, and
   when the Williams gauge reads warm enough to kill released trout the
   line has to say so. A Topsail water temperature has to credit
   Wrightsville Beach, 25 miles away, because that is where the number
   comes from — in any form it is printed, not just "83F".
4. THE WEST VIRGINIA NOTEBOOK IS ONE SENTENCE PER REGION. `regional` and
   `away` items are pointers, not briefs. Region ids must exist in
   config.REGIONS, away entries must be flagged is_away there, and all
   three sub-arrays are optional — a thin day is legal, padding is not.
5. SUMO IS NOT A DAILY QUOTA. Ian settled it: sumo gets covered when there
   is something to cover. Nothing here fails an edition for its absence,
   and off-basho months do not even advise.

Importable:
    validate(edition, stats=None, check_urls=True, fishing=None) -> list[str]
    advisories(edition, stats=None, fishing=None) -> list[str]
    strip_dead_urls(edition) -> list[str]
    estimate_embed_chars(edition) -> int
    sentence_count(text) -> int
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

import config


def _repo(*parts: str) -> str:
    """Absolute path inside the repo, whatever the caller's cwd is."""
    return os.path.join(config.PROJECT_ROOT, *parts)

try:  # requests is in requirements.txt, but delivery must never need pip
    import requests
except ImportError:  # pragma: no cover - exercised only in a bare sandbox
    requests = None

try:  # the poster is the authority on what Discord actually counts
    import post_discord
except ImportError:  # pragma: no cover - shape checks must still run alone
    post_discord = None

# ------------------------------------------------------------ contract shape

TOP_KEYS = {
    "edition_date", "edition_number", "volume", "lead", "sections",
    "weather_ear", "kicker", "sources_note",
}
# Optional: present only on the days the paper ran a drawing.
TOP_OPTIONAL_KEYS = {"art"}
LEAD_KEYS = {"headline", "dek", "byline", "body", "stat_strip"}
# `art` used to live here. It moved to the TOP LEVEL so a drawing can be
# placed with the story it depicts instead of always under the lead.
LEAD_OPTIONAL_KEYS: set[str] = set()
SECTION_KEYS = {"id", "label", "briefs"}
# West Virginia is the only section with a shape of its own: Ian's .wv-box
# instead of the two-column brief layout, and three optional sub-arrays.
WV_SECTION_KEYS = SECTION_KEYS | {"notebook_title", "regional", "away", "fishing"}
BRIEF_KEYS = {"headline", "summary", "source", "url"}
REGION_ITEM_KEYS = {"region_id", "place", "people", "item", "source", "url"}
REGION_ITEM_REQUIRED = {"region_id", "place", "people", "item", "source"}
FISHING_KEYS = {"water", "line", "source", "url"}
FISHING_REQUIRED = {"water", "line", "source"}
STAT_KEYS = {"label", "value", "change", "direction"}
DIRECTIONS = {"up", "down", "flat"}


def _section_keys(sid: str) -> set:
    return WV_SECTION_KEYS if sid == "wv" else SECTION_KEYS

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATED_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.json$")
LEADING_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
# "82.8F", "71 F", "68 degrees F" — a water temperature in a fishing line.
# Kept because it is the unambiguous form; it is NOT the trigger for the
# Topsail attribution guard any more — see _temperature_mentioned(), which
# also catches "83 degrees", "83°" and "low 80s".
TEMP_F_RE = re.compile(r"\d{2,3}(?:\.\d)?\s*(?:°\s*|degrees?\s*)?F\b")

# A temperature in the copy, in every form the house voice actually writes:
# "83F", "83 F", "83.1 degrees F", "83°", "83 degrees", "low 80s".
TEMP_SHAPE_RE = re.compile(
    r"\d{2,3}(?:\.\d+)?\s*(?:[°º]\s*)?(?:degrees?\s*|deg\.?\s*)?F\b"
    r"|\d{2,3}(?:\.\d+)?\s*[°º]"
    r"|\d{2,3}(?:\.\d+)?\s*degrees?\b"
    r"|\b(?:low|mid|high|upper)[-\s]?\d{2}s\b",
    re.I,
)
# Words that make a nearby bare number a water reading rather than a tide
# height or a distance: "water 83", "temp 83", "the sound is 83".
WATER_WORD_RE = re.compile(
    r"\b(?:water|temp|temperature|surf|ocean|sound|sea|inlet|swimming)\b", re.I
)
# A standalone 2-3 digit number, not part of a decimal or a clock time.
BARE_NUMBER_RE = re.compile(r"(?<![\d.:])\d{2,3}(?:\.\d+)?(?![\d:])")
# What a number is measuring, when it says so. None of these are degrees.
NON_TEMP_UNIT_RE = re.compile(
    r"\s*(?:ft\b|feet\b|foot\b|in\b|inch\w*|cfs\b|mi\b|miles?\b|min\w*|hr\w*|"
    r"hours?\b|%|am\b|pm\b|a\.m\.|p\.m\.|knots?\b|kt\b|mph\b|degrees? *[NSEW]\b)",
    re.I,
)
# How close a number has to sit to a water word to be read as a temperature.
TEMP_PROXIMITY_CHARS = 40

# A clock time, with the meridiem when the copy bothers to print one.
CLOCK_RE = re.compile(r"\b(\d{1,2}):(\d{2})\s*(a\.?m\.?|p\.?m\.?)?", re.I)
# A number as printed: 1.68, 108, 1,240.5
NUMBER_RE = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")

# Keys in out/fishing.json whose STRING values are fetcher-written prose or
# identifiers about a water, and whose digits a fishing line may therefore
# quote back. Every other string in that file is a timestamp or a label, and
# a timestamp's digits are not publishable numbers.
FISHING_TEXT_KEYS = {"read", "note", "site", "station_id"}

# fetch_fishing.trout_read() calls the Williams marginal at 67F and states
# outright above 70F that released fish die. That warning is the one piece of
# advice this paper is allowed to give, so an edition line that quotes the
# flow and drops the temperature is a hard error, not a style note.
WILLIAMS_TROUT_MARGINAL_F = 67
WILLIAMS_TROUT_WARN_F = 70
# Cues in the FETCHER's own read string, in case the thresholds move.
FETCHER_WARN_CUES = (
    "too warm", "leave them alone", "marginal", "die at these", "keep fights short",
)
# Cues that count as the edition line having carried the warning.
LINE_WARN_CUES = (
    "too warm", "too hot", "leave them alone", "leave the trout", "leave the fish",
    "die", "dies", "kill", "lethal", "marginal", "warm water", "no trout",
    "don't fish", "do not fish", "keep fights short", "find a bass", "stress",
)

# Stubs the model leaves behind when it runs out of sourced material. Kept
# tight on purpose: a false positive here blocks a real morning paper.
PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b"),
    re.compile(r"\bTBD\b"),
    re.compile(r"\bFIXME\b"),
    re.compile(r"\bXXX+\b"),
    re.compile(r"lorem ipsum", re.I),
    re.compile(r"\bplaceholder\b", re.I),
    re.compile(r"\bexample\.(?:com|org|net)\b", re.I),
    re.compile(
        r"\[[^\]]*\b(?:here|todo|tbd|insert|headline|summary|name|link|url|text)\b[^\]]*\]",
        re.I,
    ),
    re.compile(r"<[^>]*\b(?:here|insert|your)\b[^>]*>", re.I),
]

PLACEHOLDER_HOSTS = {"example.com", "example.org", "example.net", "localhost"}

# The repo is public and the paper pings nobody, so a Discord mention or a
# raw snowflake reaching the edition JSON is a hard stop rather than a
# style note. First names are the only identity the copy ever carries.
# The third flag is "also check url values". A bare snowflake is exempt
# there because a publisher's article id can be 17+ digits and a false
# positive would block a real morning paper.
PRIVACY_PATTERNS = [
    (re.compile(r"<@[!&]?\d+>"), "a Discord mention", True),
    (re.compile(r"(?<!\d)\d{17,20}(?!\d)"), "a Discord user id", False),
    (re.compile(r"@everyone|@here", re.I), "an everyone/here ping", True),
]

# The edition JSON is content only — emoji live in config.SECTIONS and never
# reach the broadsheet, which cannot draw them anyway.
EMOJI_RANGES = (
    (0x1F000, 0x1FAFF),
    (0x2600, 0x27BF),
    (0x2B00, 0x2BFF),
    (0xFE0F, 0xFE0F),
)

URL_TIMEOUT = 6
ALIVE_STATUSES = {403, 405}     # paywalls and sandbox egress look like this
DEAD_STATUSES = {404}           # the ONLY verdict that strips a url
HEAD_RETRY_STATUSES = {400, 404, 405, 501}  # servers that mishandle HEAD

# Big, boring origins used only to answer "is anything reachable from here?"
# before an `unreachable` verdict is reported as if it meant something. They
# never appear in an edition and nothing is stripped on their account.
CONTROL_PROBE_URLS = (
    "https://www.cloudflare.com/",
    "https://www.wikipedia.org/",
    "https://www.google.com/",
)

# Periods a newswire uses that are not sentence ends. Without these,
# "Gov. Morrisey signed it." counts as two sentences and the one-sentence
# rule rejects a perfectly good regional line.
_ABBREVIATIONS = (
    "u.s.", "u.k.", "w.va.", "d.c.", "a.m.", "p.m.", "e.g.", "i.e.",
    "st.", "mt.", "ft.", "rd.", "ave.", "no.", "vs.", "approx.",
    "mr.", "mrs.", "ms.", "dr.", "gov.", "sen.", "rep.", "gen.", "lt.",
    "sgt.", "col.", "capt.", "jr.", "sr.", "co.", "inc.", "dept.",
    "univ.", "assn.", "est.",
    # Months. A daily paper writes a date in almost every notebook line,
    # and AP style abbreviates all but March through July.
    "jan.", "feb.", "aug.", "sept.", "sep.", "oct.", "nov.", "dec.",
    # Ranks and offices beyond the ones above — military honors and
    # obituaries turn up on the away desk more than you would guess, and
    # "Coun." is standard for a Canadian councillor (Prince George).
    "pfc.", "pvt.", "cpl.", "spc.", "maj.", "adm.", "cmdr.", "cpt.",
    "coun.", "prof.", "atty.", "supt.", "det.", "ofc.", "cmte.",
    # Places and corporate forms.
    "ala.", "ariz.", "ark.", "calif.", "colo.", "conn.", "fla.", "ga.",
    "ill.", "ind.", "kan.", "ky.", "la.", "md.", "mass.", "mich.",
    "minn.", "miss.", "mo.", "mont.", "neb.", "nev.", "n.c.", "n.d.",
    "n.h.", "n.j.", "n.m.", "n.y.", "okla.", "ore.", "pa.", "r.i.",
    "s.c.", "s.d.", "tenn.", "tex.", "vt.", "va.", "wash.", "wis.",
    "wyo.", "corp.", "ltd.", "bros.", "b.c.",
)


def sentence_count(text: str) -> int:
    """Sentences in `text`, tolerant of abbreviations, initials and decimals.

    Used by the one-sentence rule on West Virginia regional/away items, so
    a false positive here blocks a real line. It is deliberately lenient:
    it undercounts before it overcounts.
    """
    masked = (text or "").strip()
    if not masked:
        return 0
    for abbr in _ABBREVIATIONS:
        masked = re.sub(
            r"(?<![A-Za-z])" + re.escape(abbr), abbr.replace(".", ""),
            masked, flags=re.I,
        )
    masked = re.sub(r"\b([A-Za-z])\.", r"\1", masked)  # J. R. Smith
    masked = re.sub(r"(\d)\.(\d)", r"\1\2", masked)  # 3.9 ft
    return len([p for p in re.split(r"[.!?]+(?:\s+|$)", masked) if p.strip()])


# ------------------------------------------------------------------ helpers


def _norm(text: str) -> str:
    """Casefolded, whitespace-collapsed form for equality comparisons."""
    return re.sub(r"\s+", " ", text or "").strip().casefold()


def _is_str(value: object) -> bool:
    return isinstance(value, str)


def _nonempty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _briefs_of(edition: dict) -> list[tuple[str, dict]]:
    """Every brief in the edition as (path, brief) pairs."""
    out: list[tuple[str, dict]] = []
    sections = edition.get("sections")
    if not isinstance(sections, list):
        return out
    for i, section in enumerate(sections):
        if not isinstance(section, dict):
            continue
        briefs = section.get("briefs")
        if not isinstance(briefs, list):
            continue
        for j, brief in enumerate(briefs):
            if isinstance(brief, dict):
                out.append((f"sections[{i}].briefs[{j}]", brief))
    return out


def _wv_section(edition: dict) -> tuple[int, dict] | tuple[None, None]:
    """The West Virginia section and its index, or (None, None)."""
    sections = edition.get("sections")
    if not isinstance(sections, list):
        return None, None
    for i, section in enumerate(sections):
        if isinstance(section, dict) and section.get("id") == "wv":
            return i, section
    return None, None


def _wv_items_of(edition: dict) -> list[tuple[str, dict]]:
    """Every regional/away/fishing entry in the notebook as (path, entry)."""
    index, section = _wv_section(edition)
    if section is None:
        return []
    out: list[tuple[str, dict]] = []
    for key in ("regional", "away", "fishing"):
        entries = section.get(key)
        if not isinstance(entries, list):
            continue
        for j, entry in enumerate(entries):
            if isinstance(entry, dict):
                out.append((f"sections[{index}].{key}[{j}]", entry))
    return out


def _linked_items_of(edition: dict) -> list[tuple[str, dict]]:
    """Everything in the edition that may carry a `url`: briefs + notebook."""
    return _briefs_of(edition) + _wv_items_of(edition)


def _iter_strings(node: object, path: str = ""):
    """Walk every string in the document, yielding (path, text)."""
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else str(key)
            yield from _iter_strings(value, child)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _iter_strings(value, f"{path}[{i}]")


# ------------------------------------------------ Discord budget estimation

# The numbers below are what the routine reads before it decides whether to
# tighten copy, so they have to be the numbers Discord will actually count.
# When post_discord is importable they are MEASURED, not estimated: the same
# build_payload() that ships is run against a deep copy and its embeds are
# totalled. That matters because the poster sends masked source links —
# ` · [WSAZ](https://...)` — and a url spends every one of its characters
# against the 6000 ceiling. The pure-text approximation further down omits
# them and under-reports a full edition by roughly 700 chars, which is the
# difference between "tighten a summary now" and "the trimmer quietly deletes
# the West Virginia notebook at post time".
#
# The approximation survives as a fallback for the shape-only case (a bare
# checkout without post_discord, or an edition too malformed to build).


def _exact_measure(edition: dict) -> dict | None:
    """Measure the real payload: {'sizes': {key: chars}, 'total': chars}.

    Returns None when post_discord is unavailable or the edition is too
    broken to build, so every caller keeps a working fallback. The edition is
    deep-copied first: build_payload() setdefault()s empty notebook arrays
    into the section it is handed, and the validator may write its argument
    back to disk.
    """
    if post_discord is None or not isinstance(edition, dict):
        return None
    try:
        working = copy.deepcopy(edition)
        embeds = post_discord.build_payload(working, None, None).get("embeds") or []
        present = post_discord._present_sections(working)
    except Exception:  # a malformed edition is the shape checks' problem
        return None
    if not embeds:
        return None

    sizes: dict[str, int] = {}
    chrome = 0
    for i, embed in enumerate(embeds):
        footer = len((embed.get("footer") or {}).get("text") or "")
        chrome += footer
        key = "lead" if i == 0 else (
            present[i - 1] if i - 1 < len(present) else f"embed{i}"
        )
        sizes[key] = sizes.get(key, 0) + post_discord.embed_text_length([embed]) - footer
    sizes["chrome"] = chrome
    return {"sizes": sizes, "total": post_discord.embed_text_length(embeds)}


# These mirror the shape post_discord.py builds. They are an ESTIMATE — the
# poster's own validate_payload() is authoritative — but they are close
# enough to catch a brief that could never fit in an embed field.


def _brief_block(brief: dict) -> str:
    head = brief.get("headline") if _is_str(brief.get("headline")) else ""
    summary = brief.get("summary") if _is_str(brief.get("summary")) else ""
    source = brief.get("source") if _is_str(brief.get("source")) else ""
    return f"**{head}**\n{summary}\n-# {source}"


def _notebook_line(entry: dict, label_key: str) -> str:
    """One regional, away, or fishing line: place in bold, one sentence, source."""
    place = entry.get(label_key) if _is_str(entry.get(label_key)) else ""
    text_key = "line" if label_key == "water" else "item"
    text = entry.get(text_key) if _is_str(entry.get(text_key)) else ""
    source = entry.get("source") if _is_str(entry.get("source")) else ""
    return f"**{place}** {text} -# {source}"


def _notebook_extras_block(section: dict) -> str:
    """The roundups under the West Virginia statewide briefs.

    Ian's .wv-box has no Discord equivalent, so the embed carries the box's
    sub-heads as text — the notebook has to read as the local anchor there
    too, not as three more wire items.
    """
    if section.get("id") != "wv":
        return ""
    chunks: list[str] = []
    for key, label_key in (("regional", "place"), ("away", "place"),
                           ("fishing", "water")):
        entries = section.get(key)
        if not isinstance(entries, list) or not entries:
            continue
        lines = [_notebook_line(e, label_key) for e in entries if isinstance(e, dict)]
        if not lines:
            continue
        chunks.append(f"**{config.WV_SUBHEADS[key]}**")
        chunks.extend(lines)
    return "\n".join(chunks)


def _section_block(section: dict) -> str:
    briefs = section.get("briefs")
    briefs = briefs if isinstance(briefs, list) else []
    parts: list[str] = []
    if section.get("id") == "wv":
        title = section.get("notebook_title") or config.WV_NOTEBOOK_TITLE
        parts.append(f"**{title}**")
    parts += [_brief_block(b) for b in briefs if isinstance(b, dict)]
    extras = _notebook_extras_block(section)
    if extras:
        parts.append(extras)
    return "\n\n".join(parts)


def _stat_line(stat_strip: object) -> str:
    if not isinstance(stat_strip, list) or not stat_strip:
        return ""
    parts = []
    for entry in stat_strip:
        if not isinstance(entry, dict):
            continue
        label = entry.get("label") or ""
        value = entry.get("value") or ""
        change = entry.get("change") or ""
        parts.append(f"{label} {value} {change}".strip())
    return " · ".join(parts)


def _lead_block(edition: dict) -> str:
    lead = edition.get("lead")
    if not isinstance(lead, dict):
        return ""
    chunks = []
    if _nonempty_str(lead.get("dek")):
        chunks.append(f"*{lead['dek']}*")
    body = lead.get("body")
    if isinstance(body, list):
        chunks.extend(p for p in body if _is_str(p))
    stats = _stat_line(lead.get("stat_strip"))
    if stats:
        chunks.append(stats)
    byline = lead.get("byline")
    if _nonempty_str(byline):
        chunks.append(f"-# {byline}")
    return "\n\n".join(chunks)


def estimate_embed_chars(edition: dict) -> int:
    """Total embed text for one message (Discord caps at 6000).

    Measured off the real payload when post_discord is importable — masked
    source links included — and approximated otherwise.
    """
    if not isinstance(edition, dict):
        return 0
    measured = _exact_measure(edition)
    if measured is not None:
        return measured["total"]
    lead = edition.get("lead") if isinstance(edition.get("lead"), dict) else {}
    total = len(lead.get("headline") or "") + len(_lead_block(edition))
    sections = edition.get("sections")
    if isinstance(sections, list):
        for section in sections:
            if not isinstance(section, dict):
                continue
            try:
                emoji = config.section_by_id(section.get("id"))["emoji"]
            except KeyError:
                emoji = ""
            title = f"{emoji} {section.get('label') or ''}".strip()
            total += len(title) + len(_section_block(section))
    total += len(edition.get("sources_note") or "")
    total += len(edition.get("kicker") or "")
    total += len(edition.get("weather_ear") or "")
    return total


def _section_title(section: dict) -> str:
    try:
        emoji = config.section_by_id(section.get("id"))["emoji"]
    except KeyError:
        emoji = ""
    return f"{emoji} {section.get('label') or ''}".strip()


def section_chars(edition: dict) -> dict[str, int]:
    """Embed chars per section id, plus 'lead' and 'chrome'.

    The keys line up with config.EMBED_BUDGET so a section over its
    allocation can be named instead of the whole message being called fat.
    'chrome' is the closing footer — kicker, colophon and weather ear —
    because that is the one run of text the poster does not file under a
    section. Measured off the real payload when post_discord is importable.
    """
    measured = _exact_measure(edition)
    if measured is not None:
        return measured["sizes"]
    lead = edition.get("lead") if isinstance(edition.get("lead"), dict) else {}
    out = {"lead": len(lead.get("headline") or "") + len(_lead_block(edition))}
    sections = edition.get("sections")
    if isinstance(sections, list):
        for section in sections:
            if not isinstance(section, dict) or not _is_str(section.get("id")):
                continue
            out[section["id"]] = (
                len(_section_title(section)) + len(_section_block(section))
            )
    out["chrome"] = (
        len(edition.get("sources_note") or "")
        + len(edition.get("kicker") or "")
        + len(edition.get("weather_ear") or "")
    )
    return out


def irreducible_chars(edition: dict) -> int:
    """Projected chars after the deepest trim post_discord.py can perform.

    The trim path drops trailing BRIEFS; it cannot shrink the lead and is
    assumed not to gut the West Virginia notebook, which is the whole point
    of the section. So this is lead + one brief per section + the notebook
    intact. If THAT does not fit one message, no trim saves it and the copy
    has to come down — which is a hard error, not an advisory.
    """
    if not isinstance(edition, dict):
        return 0

    floored = copy.deepcopy(edition)
    sections = floored.get("sections")
    if isinstance(sections, list):
        for section in sections:
            if isinstance(section, dict) and isinstance(section.get("briefs"), list):
                section["briefs"] = section["briefs"][:config.BRIEFS_MIN]
    measured = _exact_measure(floored)
    if measured is not None:
        return measured["total"]

    lead = edition.get("lead") if isinstance(edition.get("lead"), dict) else {}
    total = len(lead.get("headline") or "") + len(_lead_block(edition))
    sections = edition.get("sections")
    if isinstance(sections, list):
        for section in sections:
            if not isinstance(section, dict):
                continue
            briefs = section.get("briefs")
            first = briefs[:config.BRIEFS_MIN] if isinstance(briefs, list) else []
            floor = dict(section, briefs=first)
            total += len(_section_title(section)) + len(_section_block(floor))
    total += len(edition.get("sources_note") or "")
    total += len(edition.get("kicker") or "")
    total += len(edition.get("weather_ear") or "")
    return total


# ------------------------------------------------------------- field checks


def _check_top_level(edition: dict) -> list[str]:
    errors: list[str] = []
    missing = TOP_KEYS - set(edition)
    if missing:
        errors.append(f"missing top-level key(s): {', '.join(sorted(missing))}")
    unknown = set(edition) - TOP_KEYS - TOP_OPTIONAL_KEYS
    if unknown:
        errors.append(
            f"unknown top-level key(s): {', '.join(sorted(unknown))} "
            "(the edition contract is frozen)"
        )

    date = edition.get("edition_date")
    if not _is_str(date) or not ISO_DATE_RE.match(date):
        errors.append(f"edition_date must be ISO YYYY-MM-DD, got {date!r}")

    number = edition.get("edition_number")
    if not isinstance(number, int) or isinstance(number, bool) or number < 1:
        errors.append(f"edition_number must be a positive int, got {number!r}")

    if not _nonempty_str(edition.get("volume")):
        errors.append("volume must be a non-empty string")

    kicker = edition.get("kicker")
    if kicker is not None and not _is_str(kicker):
        errors.append("kicker must be a string or null")

    if not _nonempty_str(edition.get("sources_note")):
        errors.append("sources_note must be a non-empty string")

    errors += _check_weather_ear(edition.get("weather_ear"))
    errors += _check_art(edition)
    return errors


def _check_weather_ear(ear: object) -> list[str]:
    """The pointer to Claude the Weatherman's 7:15 forecast.

    A newspaper's weather ear is a pointer, not a plug: short, and useless
    if it does not carry the time. The wording rotates day to day (the pool
    is config.WEATHER_EAR_LINES) so only the time is enforced.

    NULL IS LEGAL. instructions/edition.md authorises `"weather_ear": null`
    on a day the Weatherman is known to be down, and render_edition.py and
    post_discord.py both already omit the line rather than break. Failing
    the gate over a missing pointer would mean no paper at all that
    morning, which is the exact failure the whole fallback ladder exists to
    prevent — so an absent ear is an advisory (see _weather_ear_advisory),
    never an error.
    """
    errors: list[str] = []
    if ear is None:
        return errors
    if not _is_str(ear):
        errors.append(
            "weather_ear must be a string or null (null only when the "
            f"{config.WEATHER_BOT} is known to be down)"
        )
        return errors
    if not ear.strip():
        # Same standing as null: the pointer is missing, the paper still runs.
        return errors

    if len(ear) > config.WEATHER_EAR_MAX_CHARS:
        errors.append(
            f"weather_ear is {len(ear)} chars "
            f"(max {config.WEATHER_EAR_MAX_CHARS}) — it is an ear, not an ad"
        )
    if config.WEATHER_TIME_ET not in ear:
        errors.append(
            f"weather_ear must name the {config.WEATHER_TIME_ET} slot — "
            f"{config.WEATHER_BOT} files then, and the time is the whole point"
        )
    if sentence_count(ear) > 2:
        errors.append("weather_ear runs past two sentences")
    return errors


def _check_lead(lead: object) -> list[str]:
    if not isinstance(lead, dict):
        return ["lead must be an object"]

    errors: list[str] = []
    missing = LEAD_KEYS - set(lead)
    if missing:
        errors.append(f"lead missing key(s): {', '.join(sorted(missing))}")
    unknown = set(lead) - LEAD_KEYS - LEAD_OPTIONAL_KEYS
    if unknown:
        errors.append(f"lead has unknown key(s): {', '.join(sorted(unknown))}")

    headline = lead.get("headline")
    if not _nonempty_str(headline):
        errors.append("lead.headline must be a non-empty string")
    elif len(headline) > config.EMBED_TITLE_LIMIT:
        errors.append(
            f"lead.headline is {len(headline)} chars "
            f"(embed title limit {config.EMBED_TITLE_LIMIT})"
        )

    dek = lead.get("dek")
    if dek is not None and not _is_str(dek):
        errors.append("lead.dek must be a string or null")

    if not _nonempty_str(lead.get("byline")):
        errors.append("lead.byline must be a non-empty string")

    body = lead.get("body")
    if not isinstance(body, list):
        errors.append("lead.body must be a list of paragraphs")
    else:
        if not config.LEAD_BODY_MIN <= len(body) <= config.LEAD_BODY_MAX:
            errors.append(
                f"lead.body has {len(body)} paragraph(s); the contract is "
                f"{config.LEAD_BODY_MIN}-{config.LEAD_BODY_MAX}"
            )
        for i, para in enumerate(body):
            if not _nonempty_str(para):
                errors.append(f"lead.body[{i}] must be a non-empty string")

    if not isinstance(lead.get("stat_strip"), list):
        errors.append("lead.stat_strip must be a list (empty is fine)")
    return errors


def _data_date(record: object, *keys: str) -> str | None:
    """The ISO date a fetcher stamped on its output file, if it stamped one.

    Both fetchers write a timestamp (`fetched_at`, `generated_at`) and
    fetch_fishing.py also writes a plain `date`. Only the leading YYYY-MM-DD
    is read, so a UTC stamp and an Eastern stamp compare the same way — the
    question is never "which hour", it is "is this yesterday's file".
    """
    if not isinstance(record, dict):
        return None
    for key in keys:
        value = record.get(key)
        if _is_str(value):
            match = LEADING_DATE_RE.match(value.strip())
            if match:
                return match.group(1)
    return None


def _check_stat_strip(
    lead: object, stats: dict | None, edition_date: object = None
) -> list[str]:
    if not isinstance(lead, dict):
        return []
    strip = lead.get("stat_strip")
    if not isinstance(strip, list):
        return []

    errors: list[str] = []
    if len(strip) > config.STAT_STRIP_MAX:
        errors.append(
            f"stat_strip has {len(strip)} entries (max {config.STAT_STRIP_MAX})"
        )

    for i, entry in enumerate(strip):
        path = f"stat_strip[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{path} must be an object")
            continue
        unknown = set(entry) - STAT_KEYS
        if unknown:
            errors.append(f"{path} has unknown key(s): {', '.join(sorted(unknown))}")
        if not _nonempty_str(entry.get("label")):
            errors.append(f"{path}.label must be a non-empty string")
        if not _nonempty_str(entry.get("value")):
            errors.append(f"{path}.value must be a non-empty string")
        change = entry.get("change")
        if change is not None and not _is_str(change):
            errors.append(f"{path}.change must be a string or null")
        direction = entry.get("direction")
        if direction is not None and direction not in DIRECTIONS:
            errors.append(
                f"{path}.direction must be one of {sorted(DIRECTIONS)}, got {direction!r}"
            )

    if stats is None:
        return errors

    # A byte-match against a stale file is not a truth check. If fetch_stats.py
    # was skipped or 503'd, yesterday's closes match perfectly and publish
    # under today's date, which is the fabrication this gate exists to stop.
    fetched = _data_date(stats, "fetched_at", "date")
    if strip and _is_str(edition_date) and fetched and fetched < edition_date:
        errors.append(
            f"out/stats.json was fetched {fetched} but the edition is dated "
            f"{edition_date} — yesterday's numbers byte-match and would ship "
            "under today's date; re-run fetch_stats.py"
        )

    entries = stats.get("entries") if isinstance(stats, dict) else None
    entries = entries if isinstance(entries, list) else []
    if not entries and strip:
        errors.append(
            f"stat_strip has {len(strip)} entries but out/stats.json has none — "
            "it must be [] (no source, no numbers)"
        )
        return errors

    by_label: dict[str, list[dict]] = {}
    for entry in entries:
        if isinstance(entry, dict) and _is_str(entry.get("label")):
            by_label.setdefault(_norm(entry["label"]), []).append(entry)

    for i, entry in enumerate(strip):
        if not isinstance(entry, dict) or not _is_str(entry.get("label")):
            continue
        path = f"stat_strip[{i}]"
        candidates = by_label.get(_norm(entry["label"]))
        if not candidates:
            known = ", ".join(sorted(e["label"] for e in entries
                                     if isinstance(e, dict) and _is_str(e.get("label"))))
            errors.append(
                f"{path}.label {entry['label']!r} is not in out/stats.json "
                f"(available: {known or 'none'}) — no invented numbers"
            )
            continue
        matched = next(
            (c for c in candidates if c.get("value") == entry.get("value")), None
        )
        if matched is None:
            errors.append(
                f"{path}.value {entry.get('value')!r} does not byte-match "
                f"out/stats.json ({entry['label']} = "
                f"{candidates[0].get('value')!r})"
            )
            continue
        if (
            _is_str(entry.get("change"))
            and _is_str(matched.get("change"))
            and entry["change"] != matched["change"]
        ):
            errors.append(
                f"{path}.change {entry['change']!r} does not match "
                f"out/stats.json ({matched['change']!r})"
            )
        if (
            entry.get("direction")
            and matched.get("direction")
            and entry["direction"] != matched["direction"]
        ):
            errors.append(
                f"{path}.direction {entry['direction']!r} does not match "
                f"out/stats.json ({matched['direction']!r})"
            )
    return errors


def _check_brief(brief: object, path: str) -> list[str]:
    if not isinstance(brief, dict):
        return [f"{path} must be an object"]

    errors: list[str] = []
    missing = BRIEF_KEYS - set(brief)
    if missing:
        errors.append(f"{path} missing key(s): {', '.join(sorted(missing))}")
    unknown = set(brief) - BRIEF_KEYS
    if unknown:
        errors.append(f"{path} has unknown key(s): {', '.join(sorted(unknown))}")

    if not _nonempty_str(brief.get("headline")):
        errors.append(f"{path}.headline must be a non-empty string")
    if not _nonempty_str(brief.get("summary")):
        errors.append(f"{path}.summary must be a non-empty string")
    if not _nonempty_str(brief.get("source")):
        errors.append(f"{path}.source must be a non-empty string")

    url = brief.get("url")
    if url is not None and not _is_str(url):
        errors.append(f"{path}.url must be a string or null")

    block = len(_brief_block(brief))
    if block > config.EMBED_FIELD_VALUE_LIMIT:
        errors.append(
            f"{path} renders to {block} chars "
            f"(embed field limit {config.EMBED_FIELD_VALUE_LIMIT}) — cut the summary"
        )
    return errors


def _check_region_item(entry: object, path: str, want_away: bool) -> list[str]:
    """One regional or away line. ONE SENTENCE, a real region, real people."""
    if not isinstance(entry, dict):
        return [f"{path} must be an object"]

    errors: list[str] = []
    missing = REGION_ITEM_REQUIRED - set(entry)
    if missing:
        errors.append(f"{path} missing key(s): {', '.join(sorted(missing))}")
    unknown = set(entry) - REGION_ITEM_KEYS
    if unknown:
        errors.append(f"{path} has unknown key(s): {', '.join(sorted(unknown))}")

    region = None
    rid = entry.get("region_id")
    if not _nonempty_str(rid):
        errors.append(f"{path}.region_id must be a non-empty string")
    else:
        try:
            region = config.region_by_id(rid)
        except KeyError:
            expected = config.AWAY_REGION_IDS if want_away else config.WV_REGION_IDS
            errors.append(
                f"{path}.region_id {rid!r} is not in config.REGIONS "
                f"(expected one of {expected})"
            )

    if region is not None:
        if bool(region["is_away"]) != want_away:
            desk = "away" if want_away else "regional"
            other = "regional" if want_away else "away"
            errors.append(
                f"{path}.region_id {rid!r} has is_away={region['is_away']} in "
                f"config.REGIONS but sits in the {desk} array — move it to {other}"
            )
        if entry.get("place") != region["place"]:
            errors.append(
                f"{path}.place is {entry.get('place')!r}, expected "
                f"{region['place']!r} — config.REGIONS is the one source of truth"
            )

    people = entry.get("people")
    if not isinstance(people, list):
        errors.append(f"{path}.people must be a list (empty is fine)")
    else:
        for k, name in enumerate(people):
            if not _nonempty_str(name):
                errors.append(f"{path}.people[{k}] must be a non-empty string")
            elif region is not None and name not in region["people"]:
                errors.append(
                    f"{path}.people[{k}] {name!r} is not attached to "
                    f"{rid!r} in config.REGIONS (has {region['people']}) — "
                    "first names from the config, never invented ones"
                )

    item = entry.get("item")
    if not _nonempty_str(item):
        errors.append(f"{path}.item must be a non-empty string")
    else:
        if len(item) > config.WV_ITEM_MAX_CHARS:
            errors.append(
                f"{path}.item is {len(item)} chars "
                f"(max {config.WV_ITEM_MAX_CHARS}) — a regional line is one "
                "sentence, not a brief"
            )
        count = sentence_count(item)
        if count > 1:
            errors.append(
                f"{path}.item runs {count} sentences; the notebook is ONE "
                "sentence per region — cut it or drop the region"
            )
        if "\n" in item:
            errors.append(f"{path}.item must be a single line")

    if not _nonempty_str(entry.get("source")):
        errors.append(f"{path}.source must be a non-empty string")

    url = entry.get("url")
    if url is not None and not _is_str(url):
        errors.append(f"{path}.url must be a string or null")
    return errors


# ------------------------------------------- fishing numbers, traced to file

# The stat strip byte-matches every value it prints against out/stats.json,
# and a mismatch there is the worst single thing this paper can print. A
# fishing line prints numbers too — cfs, stage, water temperature, tide times
# — and it gets exactly the same treatment: every numeric token in `line` has
# to be a number fetch_fishing.py wrote for THAT water. "310 cfs and rising —
# blown out" over a gauge reading 108 and falling is the same fabrication as
# an invented Nasdaq close, just quieter.


def _to_float(token: str) -> float | None:
    try:
        return float(token.replace(",", ""))
    except (TypeError, ValueError):
        return None


def _decimals(token: str) -> int:
    return len(token.split(".", 1)[1]) if "." in token else 0


def _meridiem(raw: object) -> str | None:
    """'a.m.' / 'PM' -> 'am' / 'pm'. None when the copy did not say."""
    if not _is_str(raw) or not raw:
        return None
    return raw[0].lower() + "m"


def _clock_tokens(text: str) -> list[tuple[str, str | None]]:
    """Every clock time in `text` as (H:MM, meridiem-or-None), 24h stripped."""
    out: list[tuple[str, str | None]] = []
    for hour, minute, mer in CLOCK_RE.findall(text or ""):
        out.append((f"{int(hour)}:{minute}", _meridiem(mer)))
    return out


def _number_tokens(text: str) -> list[str]:
    """Every number in `text`, with clock times masked out first."""
    return NUMBER_RE.findall(CLOCK_RE.sub(" ", text or ""))


def _fishing_values(record: object) -> tuple[set[float], dict[str, set[str]]]:
    """Every number and clock time fetch_fishing.py wrote for one water.

    Numbers come from the record's numeric leaves (discharge_cfs, stage_ft,
    water_temp_f, tide height_ft, miles_away, the 24h-ago values) plus the
    digits inside the fetcher's own prose keys — its `read` line already
    prints "108 cfs" for 108.0 and a station `note` carries "11 mi" and "75
    min", and quoting those back is quoting the file.
    """
    numbers: set[float] = set()
    times: dict[str, set[str]] = {}

    def remember_clock(text: str) -> None:
        for stamp, mer in _clock_tokens(text):
            bucket = times.setdefault(stamp, set())
            if mer:
                bucket.add(mer)

    def walk(node: object, key: str | None = None) -> None:
        if isinstance(node, bool):
            return
        if isinstance(node, (int, float)):
            numbers.add(float(node))
        elif isinstance(node, str):
            if key == "time_local":
                remember_clock(node)
            elif key in FISHING_TEXT_KEYS:
                remember_clock(node)
                for token in _number_tokens(node):
                    value = _to_float(token)
                    if value is not None:
                        numbers.add(value)
        elif isinstance(node, dict):
            for child_key, value in node.items():
                walk(value, child_key)
        elif isinstance(node, list):
            for value in node:
                walk(value, key)

    walk(record)
    return numbers, times


def _number_is_sourced(token: str, values: set[float]) -> bool:
    """True when `token` is one of `values`, at the token's own precision.

    fetch_fishing.py rounds in its own read line — "108 cfs" for 108.0,
    "83F" for 83.1 — so a line quoting the rounded form is still quoting the
    file. "82.9" against a fetched 83.1 is not, and that is the case this
    exists to catch.
    """
    value = _to_float(token)
    if value is None:
        return False
    places = _decimals(token)
    return any(round(known, places) == round(value, places) for known in values)


def _check_fishing_numbers(line: str, record: object, path: str) -> list[str]:
    """Every cfs, stage, temperature and tide time in `line`, traced to file."""
    numbers, times = _fishing_values(record)
    errors: list[str] = []

    for stamp, mer in _clock_tokens(line):
        known = times.get(stamp)
        if known is None:
            errors.append(
                f"{path}.line prints the time {stamp} but out/fishing.json has "
                "no such tide time for this water — the times come from the file"
            )
        elif mer and known and mer not in known:
            errors.append(
                f"{path}.line prints {stamp} {mer} but out/fishing.json has that "
                f"tide at {stamp} {sorted(known)[0]}"
            )

    for token in _number_tokens(line):
        if not _number_is_sourced(token, numbers):
            errors.append(
                f"{path}.line prints {token} but out/fishing.json has no such "
                "reading for this water (it carries "
                f"{', '.join(_format_known(numbers))}) — a fishing line may "
                "print only numbers the fetcher measured"
            )
    return errors


def _format_known(numbers: set[float]) -> list[str]:
    """The fetched numbers, shortest-first, for an error message."""
    ordered = sorted(numbers)
    return [f"{n:g}" for n in ordered[:8]] + (["..."] if len(ordered) > 8 else [])


def _temperature_mentioned(line: str) -> bool:
    """True when `line` prints something shaped like a water temperature.

    The old guard required a literal trailing F, so "water 83 degrees",
    "water temp 83°" and "low 80s" all published Wrightsville's reading as
    Topsail's own. This fires on any temperature-shaped token, and on a bare
    two-or-three-digit number sitting next to a water word with no unit of
    its own — while still ignoring "3.9 ft", "1:02 p.m." and "25 miles".
    """
    if not _is_str(line):
        return False
    if TEMP_SHAPE_RE.search(line):
        return True
    for water in WATER_WORD_RE.finditer(line):
        low = water.start() - TEMP_PROXIMITY_CHARS
        high = water.end() + TEMP_PROXIMITY_CHARS
        for number in BARE_NUMBER_RE.finditer(line):
            if not low <= number.start() <= high:
                continue
            if NON_TEMP_UNIT_RE.match(line, number.end()):
                continue
            return True
    return False


def _fetched_water_temp(record: object) -> float | None:
    """The water temperature fetch_fishing.py recorded for a water, if any."""
    if not isinstance(record, dict):
        return None
    for candidate in (record, record.get("water_temp")):
        if isinstance(candidate, dict):
            value = candidate.get("water_temp_f")
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return float(value)
    return None


def _check_trout_warning(line: str, record: object, path: str) -> list[str]:
    """Warm water kills released trout, and the line has to say so.

    fetch_fishing.trout_read() puts the temperature first and states it
    bluntly above 70F precisely because it outranks flow. A line that quotes
    the flow, calls it prime wading water and drops the warning is worse
    than no fishing line at all — it is the one place this paper gives
    advice, and it would be giving the wrong one.
    """
    if not isinstance(record, dict) or not _is_str(line):
        return []
    temp = _fetched_water_temp(record)
    read = record.get("read") if _is_str(record.get("read")) else ""
    warned = (temp is not None and temp >= WILLIAMS_TROUT_MARGINAL_F) or any(
        cue in read.lower() for cue in FETCHER_WARN_CUES
    )
    if not warned:
        return []

    low = line.lower()
    carries_cue = any(cue in low for cue in LINE_WARN_CUES)
    carries_temp = temp is None or any(
        _number_is_sourced(token, {temp}) for token in _number_tokens(line)
    )
    if carries_cue and carries_temp:
        return []

    missing = []
    if not carries_temp:
        missing.append(f"the {temp:g}F reading")
    if not carries_cue:
        missing.append("what it means for the fish")
    return [
        f"{path}.line omits {' and '.join(missing)} — out/fishing.json reads "
        f"{read.strip() or f'{temp:g}F'!r}, and released trout die above "
        f"{WILLIAMS_TROUT_WARN_F}F; the warning outranks the flow and is not "
        "optional"
    ]


def _check_fishing_entry(entry: object, path: str, fishing: dict | None) -> list[str]:
    """One fishing line. Measured, attributed, and never for a dead source."""
    if not isinstance(entry, dict):
        return [f"{path} must be an object"]

    errors: list[str] = []
    missing = FISHING_REQUIRED - set(entry)
    if missing:
        errors.append(f"{path} missing key(s): {', '.join(sorted(missing))}")
    unknown = set(entry) - FISHING_KEYS
    if unknown:
        errors.append(f"{path} has unknown key(s): {', '.join(sorted(unknown))}")

    water = entry.get("water")
    key = None
    if not _nonempty_str(water):
        errors.append(f"{path}.water must be a non-empty string")
    else:
        key = next(
            (k for k, name in config.FISHING_WATERS.items() if name == water), None
        )
        if key is None:
            errors.append(
                f"{path}.water {water!r} is not a water fetch_fishing.py "
                f"reports (expected one of "
                f"{sorted(config.FISHING_WATERS.values())})"
            )

    line = entry.get("line")
    if not _nonempty_str(line):
        errors.append(f"{path}.line must be a non-empty string")
    elif len(line) > config.WV_FISHING_LINE_MAX_CHARS:
        errors.append(
            f"{path}.line is {len(line)} chars "
            f"(max {config.WV_FISHING_LINE_MAX_CHARS})"
        )

    if not _nonempty_str(entry.get("source")):
        errors.append(f"{path}.source must be a non-empty string")

    url = entry.get("url")
    if url is not None and not _is_str(url):
        errors.append(f"{path}.url must be a string or null")

    record = fishing.get(key) if isinstance(fishing, dict) and key else None

    # Topsail has no thermometer of its own. Printing the Wrightsville
    # reading as if it were Topsail's is the fishing report's version of a
    # fabricated stat, so it is a hard error rather than a style note. The
    # trigger is any temperature-shaped token — "83F", "83 degrees", "83°",
    # "low 80s" — or the fetched reading appearing in the line in any form.
    if key == "topsail" and _is_str(line):
        prints_temp = _temperature_mentioned(line)
        fetched = _fetched_water_temp(record)
        if not prints_temp and fetched is not None:
            prints_temp = any(
                _number_is_sourced(token, {fetched})
                for token in _number_tokens(line)
            )
        if prints_temp:
            credited = config.TOPSAIL_TEMP_STATION_NAME.lower()
            haystack = f"{line} {entry.get('source') or ''}".lower()
            if credited not in haystack:
                errors.append(
                    f"{path} prints a water temperature but does not credit "
                    f"{config.TOPSAIL_TEMP_STATION_NAME} — the reading comes from "
                    f"{config.TOPSAIL_TEMP_MILES} miles away and has to say so"
                )

    if fishing is not None and key is not None and not record:
        errors.append(
            f"{path} reports {water!r} but out/fishing.json has no reading "
            "for it — when a source fails the line is omitted, never invented"
        )
    elif record and _is_str(line):
        # Same rule as the stat strip: every number printed traces to the file.
        errors += _check_fishing_numbers(line, record, path)
        if key == "williams":
            errors += _check_trout_warning(line, record, path)
    return errors


def _check_notebook(
    section: dict, index: int, fishing: dict | None, edition_date: object = None
) -> list[str]:
    """The four-part West Virginia notebook: statewide, regional, away, fishing.

    All three sub-arrays are OPTIONAL and may be empty — only regions with
    genuine news get a line, and a thin day is a legal day.
    """
    errors: list[str] = []
    path = f"sections[{index}]"

    title = section.get("notebook_title")
    if not _nonempty_str(title):
        errors.append(
            f"{path}.notebook_title must be {config.WV_NOTEBOOK_TITLE!r}"
        )
    elif title != config.WV_NOTEBOOK_TITLE:
        errors.append(
            f"{path}.notebook_title is {title!r}, expected "
            f"{config.WV_NOTEBOOK_TITLE!r}"
        )

    for key, want_away, cap in (
        ("regional", False, config.WV_REGIONAL_MAX),
        ("away", True, config.WV_AWAY_MAX),
    ):
        entries = section.get(key)
        if entries is None:
            continue
        if not isinstance(entries, list):
            errors.append(f"{path}.{key} must be a list (empty is fine)")
            continue
        if len(entries) > cap:
            errors.append(
                f"{path}.{key} has {len(entries)} entries (max {cap}, one per "
                "region) — one region cannot file twice"
            )
        seen: dict[str, str] = {}
        for j, entry in enumerate(entries):
            item_path = f"{path}.{key}[{j}]"
            errors += _check_region_item(entry, item_path, want_away)
            rid = entry.get("region_id") if isinstance(entry, dict) else None
            if _is_str(rid):
                if rid in seen:
                    errors.append(
                        f"{item_path}.region_id {rid!r} duplicates {seen[rid]}"
                    )
                else:
                    seen[rid] = item_path

    fishing_entries = section.get("fishing")
    if fishing_entries is not None:
        if not isinstance(fishing_entries, list):
            errors.append(f"{path}.fishing must be a list (empty is fine)")
        else:
            if len(fishing_entries) > config.WV_FISHING_MAX:
                errors.append(
                    f"{path}.fishing has {len(fishing_entries)} entries "
                    f"(max {config.WV_FISHING_MAX} — two waters)"
                )
            # Yesterday's gauge reading traces to the file perfectly. Checked
            # once here rather than per line, since it condemns all of them.
            generated = _data_date(fishing, "date", "generated_at")
            if (
                fishing_entries
                and _is_str(edition_date)
                and generated
                and generated < edition_date
            ):
                errors.append(
                    f"{path}.fishing runs off out/fishing.json from {generated} "
                    f"but the edition is dated {edition_date} — a skipped or "
                    "failed fetch republishes yesterday's water; re-run "
                    "fetch_fishing.py"
                )
            waters: dict[str, str] = {}
            for j, entry in enumerate(fishing_entries):
                item_path = f"{path}.fishing[{j}]"
                errors += _check_fishing_entry(entry, item_path, fishing)
                water = entry.get("water") if isinstance(entry, dict) else None
                if _is_str(water):
                    if water in waters:
                        errors.append(
                            f"{item_path}.water {water!r} duplicates {waters[water]}"
                        )
                    else:
                        waters[water] = item_path
    return errors


def _check_sections(
    sections: object, fishing: dict | None = None, edition_date: object = None
) -> list[str]:
    if not isinstance(sections, list):
        return ["sections must be a list"]

    errors: list[str] = []
    # The contract as of THIS edition's date: Sports was retired 2026-08-15
    # when it moved to its own paper, and the archive keeps its shape.
    expected_sections = config.sections_for(
        edition_date if isinstance(edition_date, str) else None)
    expected_ids = [s["id"] for s in expected_sections]
    if len(sections) != len(expected_sections):
        errors.append(
            f"expected exactly {len(expected_sections)} sections "
            f"({', '.join(expected_ids)}), got {len(sections)}"
        )

    for i, expected in enumerate(expected_sections):
        if i >= len(sections):
            errors.append(f"sections[{i}] is missing (expected id {expected['id']!r})")
            continue
        section = sections[i]
        if not isinstance(section, dict):
            errors.append(f"sections[{i}] must be an object")
            continue

        unknown = set(section) - _section_keys(expected["id"])
        if unknown:
            errors.append(
                f"sections[{i}] has unknown key(s): {', '.join(sorted(unknown))}"
            )
        if expected["id"] == "wv":
            errors += _check_notebook(section, i, fishing, edition_date)
        if section.get("id") != expected["id"]:
            errors.append(
                f"sections[{i}].id is {section.get('id')!r}, expected "
                f"{expected['id']!r} — section order is fixed"
            )
        if section.get("label") != expected["label"]:
            errors.append(
                f"sections[{i}].label is {section.get('label')!r}, expected "
                f"{expected['label']!r}"
            )

        briefs = section.get("briefs")
        sid = section.get("id") or expected["id"]
        if not isinstance(briefs, list):
            errors.append(f"sections[{i}].briefs must be a list")
            continue
        if len(briefs) < config.BRIEFS_MIN:
            standing = " (standing section — it runs even on a dead news day)" \
                if expected["standing"] else ""
            errors.append(f"section {sid!r} has no briefs{standing}")
        for j, brief in enumerate(briefs):
            errors.extend(_check_brief(brief, f"sections[{i}].briefs[{j}]"))

    extra = sections[len(expected_sections):]
    for k, section in enumerate(extra, start=len(expected_sections)):
        sid = section.get("id") if isinstance(section, dict) else section
        errors.append(f"sections[{k}] is unexpected (id {sid!r})")
    return errors


def _check_hygiene(edition: dict) -> list[str]:
    errors: list[str] = []
    for path, text in _iter_strings(edition):
        for pattern in PLACEHOLDER_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(
                    f"{path} contains placeholder text {match.group(0)!r}"
                )
                break
        is_url = path.endswith(".url")
        for pattern, what, in_urls in PRIVACY_PATTERNS:
            if is_url and not in_urls:
                continue
            match = pattern.search(text)
            if match:
                errors.append(
                    f"{path} contains {what} ({match.group(0)!r}) — the repo is "
                    "public and the paper pings nobody; first names only"
                )
                break
        for char in text:
            code = ord(char)
            if any(lo <= code <= hi for lo, hi in EMOJI_RANGES):
                errors.append(
                    f"{path} contains emoji U+{code:04X} — the edition JSON is "
                    "content only (emoji live in config.SECTIONS)"
                )
                break
    return errors


def _check_urls_wellformed(edition: dict) -> list[str]:
    errors: list[str] = []
    for path, brief in _linked_items_of(edition):
        url = brief.get("url")
        if url is None or not _is_str(url):
            continue
        if url != url.strip() or re.search(r"\s", url):
            errors.append(f"{path}.url contains whitespace")
            continue
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            errors.append(f"{path}.url must be http(s), got {url!r}")
            continue
        host = (parsed.hostname or "").lower()
        if not host or "." not in host:
            errors.append(f"{path}.url has no valid host: {url!r}")
        elif host in PLACEHOLDER_HOSTS or host.endswith(".example.com"):
            errors.append(f"{path}.url is a placeholder host: {url!r}")
    return errors


def _check_duplicates(edition: dict) -> list[str]:
    errors: list[str] = []
    lead = edition.get("lead")
    lead_headline = _norm(lead.get("headline", "")) if isinstance(lead, dict) else ""

    seen_headlines: dict[str, str] = {}
    seen_urls: dict[str, str] = {}
    for path, brief in _briefs_of(edition):
        headline = _norm(brief.get("headline", "")) if _is_str(brief.get("headline")) else ""
        if headline:
            if headline == lead_headline:
                errors.append(f"{path}.headline duplicates the lead headline")
            elif headline in seen_headlines:
                errors.append(
                    f"{path}.headline duplicates {seen_headlines[headline]}"
                )
            else:
                seen_headlines[headline] = path
        url = brief.get("url")
        if _is_str(url) and url:
            if url in seen_urls:
                errors.append(f"{path}.url duplicates {seen_urls[url]}")
            else:
                seen_urls[url] = path

    # A regional line that restates a statewide brief is padding wearing a
    # place name, which is exactly what the roundup must not become.
    seen_items: dict[str, str] = {}
    for path, entry in _wv_items_of(edition):
        url = entry.get("url")
        if _is_str(url) and url:
            if url in seen_urls:
                errors.append(f"{path}.url duplicates {seen_urls[url]}")
            else:
                seen_urls[url] = path
        item = _norm(entry.get("item", "")) if _is_str(entry.get("item")) else ""
        if not item:
            continue
        if item in seen_items:
            errors.append(f"{path}.item duplicates {seen_items[item]}")
        elif item in seen_headlines:
            errors.append(
                f"{path}.item repeats {seen_headlines[item]} — a region line "
                "must add news, not restate a statewide brief"
            )
        else:
            seen_items[item] = path
    return errors


def _check_budgets(edition: dict) -> list[str]:
    """Only the ceilings a trim cannot fix. Total overage is post_discord's job."""
    errors: list[str] = []
    lead_block = len(_lead_block(edition))
    if lead_block > config.EMBED_DESC_LIMIT:
        errors.append(
            f"lead renders to {lead_block} chars "
            f"(embed description limit {config.EMBED_DESC_LIMIT})"
        )
    sections = edition.get("sections")
    if isinstance(sections, list):
        for i, section in enumerate(sections):
            if not isinstance(section, dict):
                continue
            size = len(_section_block(section))
            if size > config.EMBED_DESC_LIMIT:
                errors.append(
                    f"section {section.get('id')!r} renders to {size} chars "
                    f"(embed description limit {config.EMBED_DESC_LIMIT})"
                )

    floor = irreducible_chars(edition)
    if floor > config.EMBED_HARD:
        errors.append(
            f"even trimmed to {config.BRIEFS_MIN} brief per section the message "
            f"projects to {floor} chars (hard {config.EMBED_HARD}) — no trim can "
            "fix this; shorten the lead or the West Virginia notebook"
        )
    return errors


# ------------------------------------------------------------ url liveness


def _probe_url(url: str) -> str:
    """HEAD-then-GET one url. Returns alive | dead | unreachable | unknown."""
    status = _http_status(url, method="HEAD")
    if status is None or status in HEAD_RETRY_STATUSES:
        retried = _http_status(url, method="GET")
        if retried is not None or status is None:
            status = retried

    if status is None:
        return "unknown"
    if status == "unreachable":
        return "unreachable"
    if isinstance(status, int):
        if 200 <= status < 400 or status in ALIVE_STATUSES:
            return "alive"
        if status in DEAD_STATUSES:
            return "dead"
    return "unknown"


def _http_status(url: str, method: str) -> int | str | None:
    """Status code, the string 'unreachable', or None when it could not be read."""
    headers = {"User-Agent": config.USER_AGENT}
    if requests is not None:
        try:
            resp = requests.request(
                method, url, headers=headers, timeout=URL_TIMEOUT,
                allow_redirects=True, stream=True,
            )
            code = resp.status_code
            resp.close()
            return code
        except requests.exceptions.ConnectionError:
            return "unreachable"
        except requests.exceptions.RequestException:
            return None
    try:
        req = urllib.request.Request(url, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=URL_TIMEOUT) as resp:
            return resp.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except urllib.error.URLError as exc:
        if isinstance(exc.reason, (socket.gaierror, ConnectionRefusedError)):
            return "unreachable"
        return None
    except (OSError, ValueError):
        return None


def _control_probe() -> bool:
    """True when a known-good origin answers at all from wherever this runs.

    An `unreachable` verdict means one of two very different things: the host
    is gone, or this sandbox refuses to reach it. Neither one ever strips a
    url, but only the first is worth telling the desk about — so nothing is
    reported on a connection-level verdict until something reachable proves
    the network itself is up.
    """
    for url in CONTROL_PROBE_URLS:
        if _http_status(url, method="HEAD") not in (None, "unreachable"):
            return True
    return False


def strip_dead_urls(edition: dict) -> list[str]:
    """Remove provably dead urls in place. Returns one note per url acted on.

    ONLY A 404 STRIPS. The brief keeps its `source` name so the reader still
    knows who reported it, and the strip is logged.

    A connection-level failure is INCONCLUSIVE and never strips anything.
    wvmetronews.com, herald-dispatch.com and wsaz.com — the small regional
    outlets the West Virginia notebook depends on — are precisely the hosts a
    restricted sandbox refuses while ap.org and reuters.com sail through, and
    deleting a live link from the committed edition on that evidence is a
    silent, permanent, invisible loss. Those urls are reported instead, and
    only once a control probe shows anything at all is reachable from here.
    No note from this path ever starts with "stripped", which is what keeps
    the CLI from rewriting the edition file over a connection failure.
    """
    briefs = [
        (path, brief) for path, brief in _linked_items_of(edition)
        if _is_str(brief.get("url")) and brief["url"]
    ]
    if not briefs:
        return []

    verdicts = [(path, brief, _probe_url(brief["url"])) for path, brief in briefs]

    notes: list[str] = []
    for path, brief, verdict in verdicts:
        if verdict == "dead":
            notes.append(f"stripped dead url (404) from {path}: {brief['url']}")
            brief["url"] = None

    unreachable = [(path, brief) for path, brief, v in verdicts if v == "unreachable"]
    if not unreachable:
        return notes

    if _control_probe():
        for path, brief in unreachable:
            notes.append(
                f"{path}.url did not connect while a control origin answered: "
                f"{brief['url']} — INCONCLUSIVE, nothing stripped; check it by "
                "hand before trusting the link"
            )
    else:
        notes.append(
            f"{len(unreachable)} url(s) did not connect and no control origin "
            "answered either — this is egress, not dead links; nothing stripped"
        )
    return notes


# ------------------------------------------------------------- public entry


def validate(
    edition: dict,
    stats: dict | None = None,
    check_urls: bool = True,
    fishing: dict | None = None,
) -> list[str]:
    """Return fatal contract violations. An empty list means the edition ships.

    `stats` is the parsed out/stats.json and `fishing` the parsed
    out/fishing.json; None skips that cross-check entirely (importers that
    only care about shape). `check_urls=True` also strips provably dead
    links from `edition` in place — see strip_dead_urls.
    """
    if not isinstance(edition, dict):
        return ["edition is not a JSON object"]

    edition_date = edition.get("edition_date")
    errors: list[str] = []
    errors += _check_top_level(edition)
    errors += _check_lead(edition.get("lead"))
    errors += _check_stat_strip(edition.get("lead"), stats, edition_date)
    errors += _check_sections(edition.get("sections"), fishing, edition_date)
    errors += _check_hygiene(edition)
    errors += _check_urls_wellformed(edition)
    errors += _check_duplicates(edition)
    errors += _check_budgets(edition)

    if check_urls:
        strip_dead_urls(edition)
    return errors


def advisories(
    edition: dict, stats: dict | None = None, fishing: dict | None = None
) -> list[str]:
    """Non-fatal notes: thin sections, sumo, budget pressure, an idle notebook."""
    if not isinstance(edition, dict):
        return []

    notes: list[str] = []
    sections = edition.get("sections")
    if isinstance(sections, list):
        for section in sections:
            if not isinstance(section, dict):
                continue
            briefs = section.get("briefs")
            if not isinstance(briefs, list):
                continue
            sid = section.get("id")
            if sid == "wv":
                if len(briefs) > config.WV_BRIEFS_MAX:
                    notes.append(
                        f"section 'wv' has {len(briefs)} statewide briefs "
                        f"(target {config.WV_BRIEFS_TARGET}, max "
                        f"{config.WV_BRIEFS_MAX}) — the notebook needs the room"
                    )
                continue
            if 0 < len(briefs) < 2:
                notes.append(
                    f"section {sid!r} runs {len(briefs)} brief — thin day; say so in the kicker"
                )
            if len(briefs) > config.BRIEFS_MAX:
                notes.append(
                    f"section {sid!r} has {len(briefs)} briefs "
                    f"(target {config.BRIEFS_TARGET}, max {config.BRIEFS_MAX}) — "
                    "the trim path will drop the tail"
                )

    for path, brief in _briefs_of(edition):
        headline = brief.get("headline")
        if _is_str(headline) and len(headline) > config.HEADLINE_TARGET_CHARS * 2:
            notes.append(
                f"{path}.headline is {len(headline)} chars "
                f"(target ~{config.HEADLINE_TARGET_CHARS})"
            )
        summary = brief.get("summary")
        if not _is_str(summary):
            continue
        if len(summary) > config.SUMMARY_WARN_CHARS:
            notes.append(
                f"{path}.summary is {len(summary)} chars "
                f"(target ~{config.SUMMARY_TARGET_CHARS})"
            )
        if sentence_count(summary) > 3:
            notes.append(f"{path}.summary runs past 3 sentences")

    for path, entry in _wv_items_of(edition):
        item = entry.get("item")
        if _is_str(item) and len(item) > config.WV_ITEM_TARGET_CHARS:
            notes.append(
                f"{path}.item is {len(item)} chars "
                f"(target ~{config.WV_ITEM_TARGET_CHARS})"
            )

    missing_urls = sum(
        1 for _, brief in _briefs_of(edition) if not _is_str(brief.get("url"))
    )
    if missing_urls:
        notes.append(f"{missing_urls} brief(s) have no url — readers cannot follow them")

    notes += _weather_ear_advisory(edition)
    notes += _notebook_advisory(edition, fishing)
    notes += _sumo_advisory(edition)
    notes += _football_advisory(edition)
    notes += _art_advisory(edition)
    notes += _budget_advisory(edition)
    return notes


def _weather_ear_advisory(edition: dict) -> list[str]:
    """A missing ear is a degraded morning, not a failed one.

    The contract allows `"weather_ear": null` when the Weatherman is down.
    That is worth saying out loud in the run log — it is the difference
    between "the routine forgot" and "the 7:15 slot is empty today" — but
    it never holds the paper.
    """
    if "weather_ear" not in edition:
        return []
    ear = edition.get("weather_ear")
    if ear is None or (_is_str(ear) and not ear.strip()):
        return [
            f"weather_ear is null — the paper ships without the "
            f"{config.WEATHER_TIME_ET} pointer (correct only when "
            f"{config.WEATHER_BOT} is known to be down)"
        ]
    return []


def _budget_advisory(edition: dict) -> list[str]:
    """Which line of config.EMBED_BUDGET the edition overspent, and by how much."""
    notes: list[str] = []
    if config.EMBED_BUDGET_TOTAL > config.EMBED_TARGET:
        notes.append(
            f"config.EMBED_BUDGET sums to {config.EMBED_BUDGET_TOTAL} but "
            f"EMBED_TARGET is {config.EMBED_TARGET} — the allocation no longer "
            "closes; fix config.py, not the edition"
        )

    for key, size in section_chars(edition).items():
        allocation = config.embed_budget(key)
        if allocation and size > allocation:
            notes.append(
                f"{key} projects to {size} chars against its {allocation} "
                "allocation (config.EMBED_BUDGET)"
            )

    total = estimate_embed_chars(edition)
    if total > config.EMBED_HARD:
        notes.append(
            f"embed text projects to ~{total} chars (hard {config.EMBED_HARD}) — "
            "post_discord.py will trim briefs"
        )
    elif total > config.EMBED_TARGET:
        notes.append(
            f"embed text projects to ~{total} chars (target {config.EMBED_TARGET})"
        )
    return notes


def _notebook_advisory(edition: dict, fishing: dict | None) -> list[str]:
    """The notebook is allowed to be thin — but a silently idle one is worth saying."""
    index, section = _wv_section(edition)
    if section is None:
        return []

    notes: list[str] = []
    counts = {
        key: len(section[key])
        for key in ("regional", "away", "fishing")
        if isinstance(section.get(key), list)
    }
    if not any(counts.values()):
        notes.append(
            "the West Virginia notebook ran statewide briefs only — no regional, "
            "away, or fishing lines (legal, but say it in the kicker if it repeats)"
        )
    lines = sum(counts.values())
    if lines > config.WV_NOTEBOOK_LINES_TARGET:
        notes.append(
            f"the notebook runs {lines} lines (target "
            f"{config.WV_NOTEBOOK_LINES_TARGET}) — over what the wv allocation "
            "pays for, so the trim path will take briefs from the wire sections"
        )

    if fishing is None:
        return notes

    reported = {
        entry.get("water")
        for _, entry in _wv_items_of(edition)
        if isinstance(entry, dict) and _is_str(entry.get("water"))
    }
    for key, name in config.FISHING_WATERS.items():
        if fishing.get(key) and name not in reported:
            notes.append(
                f"out/fishing.json has a reading for {name} that the notebook "
                "did not use"
            )
    for error in fishing.get("errors") or []:
        notes.append(f"fishing source degraded: {error}")
    return notes


def _sumo_advisory(edition: dict) -> list[str]:
    """Ian's rule: covered when there is something to cover, not a daily quota.

    So this NEVER fires off-basho — "no sumo news in August" is the honest
    answer, not a gap. During a tournament it fires twice over: once if sumo
    is missing entirely, once if it is present but not leading Sports, since
    a running basho is usually the biggest thing on the sports wire.
    """
    sections = edition.get("sections")
    if not isinstance(sections, list):
        return []
    sports = next(
        (s for s in sections if isinstance(s, dict) and s.get("id") == "sports"), None
    )
    if not sports:
        return []
    briefs = sports.get("briefs")
    if not isinstance(briefs, list) or not briefs:
        return []

    def is_sumo(brief: object) -> bool:
        if not isinstance(brief, dict):
            return False
        text = f"{brief.get('headline', '')} {brief.get('summary', '')}".lower()
        return any(word in text for word in config.SUMO_KEYWORDS)

    date = edition.get("edition_date")
    in_basho = config.is_basho_window(date) if _is_str(date) else False
    covered = any(is_sumo(b) for b in briefs)

    if not in_basho:
        return []
    if not covered:
        return [
            f"no sumo brief in Sports and {date} falls inside a "
            f"{config.SUMO_BASHO_DAYS}-day basho window — tournament coverage "
            "should exist; confirm the dates by search"
        ]
    if config.SUMO_LEADS_SPORTS_IN_BASHO and not is_sumo(briefs[0]):
        return [
            "sumo is covered but not leading Sports during a basho — during a "
            "tournament it usually wins the sports lead"
        ]
    return []


def _check_art(edition: dict) -> list[str]:
    """The drawing is a DRAWING. Hard errors, not advisories.

    A sketch made from looking at a photograph is an original work. A traced
    or embedded copy of that photograph is the photograph, published on a
    public site without a licence. Nothing here can tell good art from bad,
    but these checks can tell a drawing from a laundered bitmap, and that is
    the distinction that actually matters.

    No art at all is always legal. Most mornings will have none.
    """
    errors: list[str] = []
    art = edition.get("art")
    if art is None:
        return []
    if not isinstance(art, dict):
        return ["art must be an object or absent"]

    placement = art.get("placement")
    legal = config.art_placements()
    if not _nonempty_str(placement) or placement not in legal:
        errors.append(
            f"art.placement must be one of {', '.join(legal)} — a drawing is "
            "rendered WITH the story it depicts, and one that does not say "
            "what it illustrates ends up under a headline it has nothing to "
            "do with"
        )
        placement = config.ART_PLACEMENT_LEAD

    # A drawing of a section's story may not claim to be the lead art.
    if placement != config.ART_PLACEMENT_LEAD:
        present = {s.get("id") for s in (edition.get("sections") or [])
                   if isinstance(s, dict)}
        if placement not in present:
            errors.append(
                f"art.placement is {placement!r} but this edition has no such "
                "section to hang it on"
            )

    date = edition.get("edition_date")
    expected = config.art_path(date, placement) if _is_str(date) else None
    path = art.get("file")
    if not _nonempty_str(path):
        return ["art.file must name the drawing, e.g. " + (expected or "art/DATE-lead.svg")]
    if expected and path not in (expected, os.path.basename(expected)):
        errors.append(f"art.file is {path!r}; this edition's drawing belongs at {expected}")

    full = _repo(config.ART_DIR_NAME, os.path.basename(path))
    if not os.path.exists(full):
        return errors + [f"art.file {path!r} does not exist"]

    size = os.path.getsize(full)
    if size > config.ART_MAX_BYTES:
        errors.append(
            f"art is {size:,} bytes (max {config.ART_MAX_BYTES:,}) — a hand "
            "drawing is small; this is the size of a traced photograph"
        )

    raw = open(full, encoding="utf-8", errors="replace").read()

    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(raw)
    except Exception as exc:  # noqa: BLE001
        return errors + [f"art does not parse as XML: {exc}"]

    if not root.tag.endswith("svg"):
        errors.append("art root element must be <svg>")
    if not root.get("viewBox"):
        errors.append("art <svg> needs a viewBox so it scales")

    alt = (root.get("aria-label") or "").strip()
    if len(alt) < config.ART_MIN_ALT_CHARS:
        errors.append(
            f"art needs an aria-label describing the scene "
            f"(at least {config.ART_MIN_ALT_CHARS} chars); a drawing nobody can "
            "see is worse than no drawing"
        )

    # THE LAUNDERING CHECKS.
    lowered = raw.lower()
    for tag in config.ART_FORBIDDEN_TAGS:
        if f"<{tag.lower()}" in lowered:
            errors.append(
                f"art contains <{tag}> — the drawing must be vector marks "
                "only, never an embedded or referenced bitmap"
            )
    # Scan for external payloads with the XML namespace declarations removed:
    # `xmlns="http://www.w3.org/2000/svg"` is mandatory on every SVG ever
    # written and is not a reference to anything. Checking the raw text
    # flagged it on the first real drawing.
    scannable = re.sub(r'\sxmlns(:\w+)?="[^"]*"', " ", lowered)
    for pattern in config.ART_FORBIDDEN_PATTERNS:
        if pattern in scannable:
            errors.append(
                f"art references {pattern!r} — a drawing has no external "
                "or encoded payload; this is how a photograph sneaks back in"
            )
    # And belt-and-braces: no linking attribute at all, whatever it points to.
    if re.search(r'\s(?:href|src)\s*=', scannable):
        errors.append(
            "art has an href/src attribute — every mark must be drawn in "
            "the file, never loaded from somewhere else"
        )

    paths = lowered.count("<path") + lowered.count("<polyline") + lowered.count("<polygon")
    if paths > config.ART_MAX_PATHS:
        errors.append(
            f"art has {paths} path elements (max {config.ART_MAX_PATHS}) — "
            "that is an autotrace of a photograph, not a drawing"
        )
    if paths == 0:
        errors.append("art has no drawn paths")

    caption = art.get("caption")
    if not _nonempty_str(caption):
        errors.append("art.caption must say what the drawing shows")
    elif len(caption) > config.ART_CAPTION_MAX_CHARS:
        errors.append(
            f"art.caption is {len(caption)} chars "
            f"(max {config.ART_CAPTION_MAX_CHARS})"
        )

    credit = art.get("credit")
    if not _nonempty_str(credit):
        errors.append(
            "art.credit is required — the paper says out loud that this "
            f"is a drawing and what it was drawn from, e.g. "
            f"'{config.ART_CREDIT_PREFIX} an NPR photograph'"
        )
    elif not credit.strip().lower().startswith(config.ART_CREDIT_PREFIX.lower()):
        errors.append(
            f"art.credit must begin {config.ART_CREDIT_PREFIX!r} so a "
            "reader is never left thinking this is a photograph"
        )
    return errors


def _art_advisory(edition: dict) -> list[str]:
    """Nate asked for a drawing every day (2026-08-07). Advisory, not a gate.

    Deliberately not a hard error. Refusing to publish a finished newspaper
    over a missing illustration would be the tail wagging the dog, and a
    quota that can fail the build rewards drawing something bad to clear it.
    The note is loud instead, and `instructions/edition.md` 4.5 gives a
    ladder that always ends somewhere honest — the Williams River at this
    morning's gauge height is drawable on the deadest news day of the year.
    """
    if not getattr(config, "ART_REQUIRED_DAILY", False):
        return []
    if edition.get("art") is not None:
        return []
    return [
        "no drawing in this edition and the paper runs one a day — work down "
        "the subject ladder in instructions/edition.md 4.5 before giving up; "
        "if you genuinely could not draw one, say so and log docs/FAILURES.md"
    ]


def _football_advisory(edition: dict) -> list[str]:
    """Advisory only. A missing football brief NEVER fails an edition.

    Same contract as sumo: the Premier League is a standing daily search in
    season, not a standing daily headline. Most matches fall on the weekend,
    so a quiet Wednesday with no football is an ordinary edition. The point
    of this note is the opposite failure — a reader asked for this section
    and a run that quietly stopped searching for it would look identical to
    a run that searched and found nothing.
    """
    sports = next(
        (s for s in (edition.get("sections") or [])
         if isinstance(s, dict) and s.get("id") == "sports"),
        None,
    )
    if not sports:
        return []
    briefs = sports.get("briefs")
    if not isinstance(briefs, list) or not briefs:
        return []

    date = edition.get("edition_date")
    parsed = config._parse_iso(date) if _is_str(date) else None
    if not parsed or not config.is_premier_league_season(parsed[1]):
        return []

    text = " ".join(
        f"{b.get('headline', '')} {b.get('summary', '')}".lower()
        for b in briefs if isinstance(b, dict)
    )
    clubs = [c.lower() for c in config.followed_clubs()]
    # Jargon OR a club name. A match report says "Liverpool beat Arsenal
    # 2-1" and contains no league vocabulary at all.
    signals = config.PREMIER_LEAGUE_KEYWORDS + config.PREMIER_LEAGUE_CLUBS
    if any(word in text for word in signals):
        # Covered. If the group has named clubs, nudge toward the emphasis
        # they actually asked for rather than a generic league round-up.
        if clubs and not any(c in text for c in clubs):
            return [
                "Premier League is covered but none of "
                f"{', '.join(config.followed_clubs())} is named — the request "
                "was emphasis on the clubs they follow, general on the rest"
            ]
        return []

    note = (f"no Premier League brief in Sports and {date} is in season "
            "(Aug-May) — a quiet midweek is fine, but confirm you searched")
    if not clubs:
        note += "; config.PREMIER_LEAGUE_FOLLOWED_CLUBS is still empty, so ask"
    return [note]


# --------------------------------------------------------------------- CLI


def _load_json(path: str) -> tuple[dict | None, str | None]:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f), None
    except FileNotFoundError:
        return None, f"{path} does not exist"
    except ValueError as exc:
        return None, f"{path} is not valid JSON: {exc}"
    except OSError as exc:
        return None, f"{path} could not be read: {exc}"


def _resolve_stats(
    explicit: str | None, skip: bool = False, dated: bool = False
) -> tuple[dict | None, list[str], list[str]]:
    """Explicit --stats is a hard gate; the implicit default is soft.

    Returns (stats, notes, errors). For a DATED edition — a real morning
    paper, not a fixture — an absent or unreadable out/stats.json is a hard
    ERROR rather than a note: there is nothing to byte-match against, so the
    stat strip would ship unverified under a real date, which is exactly the
    failure the truth check exists to prevent. Fixtures are undated and
    already pass --no-stats.
    """
    if skip:
        return None, ["--no-stats: stat_strip values are NOT verified"], []

    gate = (
        "a dated edition's stat_strip cannot ship unverified — run "
        "fetch_stats.py, or pass --no-stats if this is a fixture"
    )
    if explicit:
        stats, problem = _load_json(explicit)
        if problem:
            if dated:
                return None, [], [f"{problem} — {gate}"]
            return {"entries": []}, [
                f"{problem} — treating stats as empty, so stat_strip must be []"
            ], []
        return stats, [], []
    if os.path.exists(config.STATS_PATH):
        stats, problem = _load_json(config.STATS_PATH)
        if problem:
            if dated:
                return None, [], [f"{problem} — {gate}"]
            return None, [f"{problem} — stat_strip not cross-checked"], []
        return stats, [], []
    if dated:
        return None, [], [f"{config.STATS_PATH} does not exist — {gate}"]
    return None, [
        f"{config.STATS_PATH} missing — stat_strip NOT cross-checked "
        "(run fetch_stats.py before the real gate)"
    ], []


def _resolve_fishing(explicit: str | None, skip: bool = False) -> tuple[dict | None, list[str]]:
    """Same shape as _resolve_stats: explicit is a hard gate, implicit is soft.

    A missing file means fishing lines go unverified, not that they are
    banned — fetch_fishing.py is allowed to have not run.
    """
    if skip:
        return None, ["--no-fishing: fishing lines are NOT verified"]
    target = explicit or config.FISHING_PATH
    if explicit or os.path.exists(config.FISHING_PATH):
        fishing, problem = _load_json(target)
        if problem:
            if explicit:
                return {}, [
                    f"{problem} — treating fishing data as empty, so any "
                    "fishing line is unsourced"
                ]
            return None, [f"{problem} — fishing lines not cross-checked"]
        return fishing, []
    return None, [
        f"{config.FISHING_PATH} missing — fishing lines NOT cross-checked "
        "(run fetch_fishing.py before the real gate)"
    ]


def _check_ledger(edition: dict, date: str) -> tuple[list[str], list[str]]:
    """Cross-check edition_number against editions/index.json."""
    errors: list[str] = []
    notes: list[str] = []
    index = config.load_index()
    number = edition.get("edition_number")
    record = config.edition_record(date, index)

    for entry in index.get("editions", []):
        if (
            isinstance(entry, dict)
            and entry.get("number") == number
            and entry.get("date") != date
        ):
            errors.append(
                f"edition_number {number} is already used by {entry.get('date')}"
            )
            break

    if record:
        if record.get("number") != number:
            errors.append(
                f"edition_number {number} disagrees with the ledger "
                f"({record.get('number')} for {date})"
            )
        if record.get("posted"):
            notes.append(
                f"{date} is already marked posted — post_discord.py will refuse "
                "without --force"
            )
    else:
        expected = config.next_edition_number(index)
        if number != expected:
            notes.append(
                f"edition_number {number} is not the ledger's next number ({expected})"
            )
    return errors, notes


# --------------------------------------------------- Sports & Sportsman

# The second paper's contract. Kept apart from the newspaper checks for the
# same reason the poster keeps a separate builder: the two papers share a
# voice and a truth standard but not a shape, and one validator serving both
# would weaken each. The instructions in instructions/sportsman.md are the
# spec these checks enforce.

SM_TOP_KEYS = {"edition_date", "edition_number", "volume", "sections",
               "kicker", "sources_note"}
SM_SECTION_ORDER = ("teams", "leagues", "seasons", "water")
SM_SEASON_BUCKETS = ("coming_in", "prime", "going_out")
SM_NUMBER_RE = re.compile(r"\d+:\d+|\d+(?:\.\d+)?")
SM_MONTH_DAY_RE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?\s+(\d{1,2})\b")
SM_MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
             "jul": 7, "aug": 8, "sep": 9, "sept": 9, "oct": 10,
             "nov": 11, "dec": 12}


def _sm_briefs(section: dict, path: str) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    briefs = section.get("briefs")
    if not isinstance(briefs, list):
        return [], [f"{path}.briefs must be a list"]
    out = []
    for i, brief in enumerate(briefs):
        where = f"{path}.briefs[{i}]"
        if not isinstance(brief, dict):
            errors.append(f"{where} must be an object")
            continue
        for key in ("headline", "summary", "source"):
            if not _nonempty_str(brief.get(key)):
                errors.append(f"{where}.{key} must be a non-empty string")
        out.append(brief)
    return out, errors


def _sm_check_teams(section: dict) -> tuple[list[str], list[str]]:
    """Every followed team is covered or accounted for — the section's job."""
    errors: list[str] = []
    notes: list[str] = []
    briefs, brief_errors = _sm_briefs(section, "teams")
    errors += brief_errors

    # Coverage counts only UNAMBIGUOUS matches. "Spurs" in a football brief
    # would otherwise mark San Antonio covered too, and then collide with a
    # perfectly correct sat_out entry — which is exactly what happened on
    # the first edition validated.
    ambiguous = set(config.ambiguous_aliases())
    covered: set[str] = set()
    for brief in briefs:
        text = f"{brief.get('headline', '')} {brief.get('summary', '')}"
        low = text.lower()
        for team in config.find_team(text):
            plain = [n for n in config.team_names(team)
                     if n.lower() in low and n.lower() not in ambiguous]
            if plain:
                covered.add(team["name"])

    sat_out = section.get("sat_out")
    accounted: set[str] = set()
    known = {t["name"] for t in config.FOLLOWED_TEAMS}
    if sat_out is not None:
        if not isinstance(sat_out, list):
            errors.append("teams.sat_out must be a list")
        else:
            for i, entry in enumerate(sat_out):
                if not isinstance(entry, dict):
                    errors.append(f"teams.sat_out[{i}] must be an object")
                    continue
                name = entry.get("team")
                if name not in known:
                    errors.append(
                        f"teams.sat_out[{i}].team {name!r} is not in "
                        "config.FOLLOWED_TEAMS")
                elif not _nonempty_str(entry.get("reason")):
                    errors.append(f"teams.sat_out[{i}].reason is required — "
                                  "a team sits out for a stated reason")
                else:
                    accounted.add(name)

    instrumented: set[str] = set()
    # The standing blocks: optional, but every entry names a followed team
    # and carries its reading. Standings and fixtures also count as
    # accounting for a team — a club with no game but a standings line is
    # not missing from the paper.
    for key, required in (("standings", "line"), ("upcoming", "fixture")):
        entries = section.get(key)
        if entries is None:
            continue
        if not isinstance(entries, list):
            errors.append(f"teams.{key} must be a list")
            continue
        for i, entry in enumerate(entries):
            where = f"teams.{key}[{i}]"
            if not isinstance(entry, dict):
                errors.append(f"{where} must be an object")
                continue
            team = entry.get("team")
            if not _nonempty_str(team) or not config.find_team(str(team)):
                errors.append(f"{where}.team {team!r} is not a followed team")
            elif not _nonempty_str(entry.get(required)):
                errors.append(f"{where}.{required} is required")
            else:
                for match in config.find_team(str(team)):
                    instrumented.add(match["name"])

    both = covered & accounted
    if both:
        errors.append(
            "teams listed as sat_out but also covered in a brief: "
            + ", ".join(sorted(both)))
    missing = known - covered - accounted - instrumented
    if missing:
        notes.append(
            "followed teams neither covered nor in sat_out: "
            + ", ".join(sorted(missing))
            + " — every team is covered or accounted for, by name")
    return errors, notes


def _sm_check_seasons(section: dict, date: str | None) -> tuple[list[str], list[str]]:
    """Season dates and limits: the one place being wrong has consequences.

    WV entries are checked against the transcribed pamphlet — including its
    expiry, after which the reference is dangerous rather than stale. NC
    entries must be cited to Marine Fisheries with a link, because Topsail
    is coastal water and NC dates are looked up live.
    """
    errors: list[str] = []
    notes: list[str] = []

    reference = None
    try:
        with open(_repo(*config.WV_SEASONS_REFERENCE.split("/")),
                  encoding="utf-8") as f:
            reference = json.load(f)
    except (OSError, ValueError):
        notes.append("WV seasons reference file unreadable — WV entries "
                     "checked for citation only")

    wv_current = config.wv_seasons_current(date) if _is_str(date) else True

    def check_entry(entry: object, where: str) -> None:
        if not isinstance(entry, dict):
            errors.append(f"{where} must be an object")
            return
        state = entry.get("state")
        if state not in ("WV", "NC"):
            errors.append(f"{where}.state must be 'WV' or 'NC'")
            return
        if not _nonempty_str(entry.get("species")):
            errors.append(f"{where}.species is required — a limit with no "
                          "animal attached is unreadable")
        if not _nonempty_str(entry.get("item")):
            errors.append(f"{where}.item must be a non-empty string")
            return
        source = str(entry.get("source") or "")
        if state == "WV":
            if "WVDNR" not in source:
                errors.append(f"{where}.source must cite WVDNR")
            if not wv_current:
                errors.append(
                    f"{where}: the transcribed WV regulations expired "
                    f"{config.WV_SEASONS_VALID_THROUGH} — print no WV date "
                    "until the reference file is replaced")
            elif reference:
                _sm_check_wv_dates(entry, where, reference, errors, notes)
        else:
            if "NCDMF" not in source and "Marine Fisheries" not in source:
                errors.append(
                    f"{where}.source must cite NCDMF — Topsail is coastal "
                    "water and the inland digest does not govern it")
            if not _nonempty_str(entry.get("url")):
                errors.append(f"{where}.url is required — NC limits are "
                              "looked up live and linked")

    for bucket in SM_SEASON_BUCKETS:
        entries = section.get(bucket)
        if entries is None:
            continue
        if not isinstance(entries, list):
            errors.append(f"seasons.{bucket} must be a list")
            continue
        for i, entry in enumerate(entries):
            check_entry(entry, f"seasons.{bucket}[{i}]")
    for i, note in enumerate(section.get("notes") or []):
        if isinstance(note, dict) and note.get("item"):
            continue
        errors.append(f"seasons.notes[{i}] must be an object with an item")
    return errors, notes


def _sm_check_wv_dates(entry: dict, where: str, reference: dict,
                       errors: list[str], notes: list[str]) -> None:
    """Any explicit date in a WV entry must exist in the pamphlet table."""
    species = str(entry.get("species") or "").lower()
    rows = [row for row in reference.get("seasons", [])
            if species and (species in row.get("species", "").lower()
                            or row.get("species", "").lower() in species)]
    if not rows:
        notes.append(f"{where}: species {entry.get('species')!r} not found "
                     "in the WV reference table — confirm it by hand")
        return
    boundaries: set[tuple[int, int]] = set()
    for row in rows:
        for window in row.get("windows") or []:
            for iso in window:
                boundaries.add((int(iso[5:7]), int(iso[8:10])))
    text = f"{entry.get('dates', '')} {entry.get('item', '')}"
    for month_name, day in SM_MONTH_DAY_RE.findall(text):
        claimed = (SM_MONTHS[month_name.lower()[:4].rstrip(".")], int(day))
        if claimed not in boundaries:
            errors.append(
                f"{where} claims {month_name} {day} but no "
                f"{entry.get('species')} window in the WV reference opens or "
                "closes that day — a season date that contradicts the "
                "pamphlet may not print")


def _sm_check_water(section: dict, fishing: dict | None) -> tuple[list[str], list[str]]:
    """Gauge lines trace to out/fishing.json, same rule as the stat strip."""
    errors: list[str] = []
    notes: list[str] = []
    waters = section.get("waters")
    if not isinstance(waters, list) or not waters:
        return ["water.waters must be a non-empty list"], []
    if fishing is None:
        notes.append("no fishing data supplied — water lines checked for "
                     "shape only")

    records: list[tuple[str, str]] = []
    if fishing:
        for key in ("williams", "topsail"):
            record = fishing.get(key)
            if record:
                records.append((str(record.get("water", key)),
                                json.dumps(record)))
        for record in fishing.get("ohio") or []:
            records.append((str(record.get("water", "")), json.dumps(record)))

    for i, entry in enumerate(waters):
        where = f"water.waters[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{where} must be an object")
            continue
        name = str(entry.get("water") or entry.get("name") or "")
        line = str(entry.get("line") or entry.get("read") or "")
        if not name or not line:
            errors.append(f"{where} needs both a water and a line")
            continue
        if not fishing:
            continue
        # Best word-overlap match, not substring: the edition says "Topsail
        # Sound" while the fetcher says "Topsail Beach (surf and sound)",
        # and both Ohio gauges share "Ohio River" — scoring picks Point
        # Pleasant vs Huntington by their distinguishing words.
        def score(rec_name: str) -> int:
            rec_words = set(re.findall(r"[a-z]+", rec_name.lower()))
            ours = set(re.findall(r"[a-z]+", name.lower()))
            return len(rec_words & ours - {"river", "at", "the", "and"})
        best = max((score(rec_name) for rec_name, _ in records), default=0)
        matches = [blob for rec_name, blob in records
                   if best and score(rec_name) == best]
        if not matches:
            errors.append(f"{where}.water {name!r} matches nothing in "
                          "out/fishing.json — a water the fetcher did not "
                          "report gets no line")
            continue
        haystack = " ".join(matches)
        for token in SM_NUMBER_RE.findall(line):
            if token in haystack:
                continue
            # Whole-number quotes of decimal readings are honest rounding.
            if "." not in token and ":" not in token:
                if re.search(rf"\b{token}\.\d", haystack):
                    continue
            errors.append(
                f"{where}.line prints {token} but out/fishing.json has no "
                f"such reading for {name} — same rule as the stat strip")
        if re.search(r"\d{2,3}(?:\.\d)?\s*(?:°|degrees?|deg|F\b)", line) \
                and "topsail" in name.lower() \
                and "wrightsville" not in line.lower():
            errors.append(
                f"{where}: a Topsail water temperature must credit "
                "Wrightsville Beach — the reading is measured 25 miles away")
    return errors, notes


def validate_sportsman(edition: dict, fishing: dict | None) -> tuple[list[str], list[str]]:
    """The whole Sports & Sportsman gate: (errors, advisories)."""
    errors: list[str] = []
    notes: list[str] = []

    missing = SM_TOP_KEYS - set(edition)
    if missing:
        errors.append(f"missing top-level key(s): {', '.join(sorted(missing))}")
    unknown = set(edition) - SM_TOP_KEYS
    if unknown:
        errors.append(f"unknown top-level key(s): {', '.join(sorted(unknown))}"
                      " (the sportsman contract is its own, not the Times')")

    number = edition.get("edition_number")
    if not isinstance(number, int) or number < 1:
        errors.append("edition_number must be a positive integer")

    sections = edition.get("sections")
    if not isinstance(sections, list):
        return errors + ["sections must be a list"], notes
    ids = [s.get("id") for s in sections if isinstance(s, dict)]
    if tuple(ids) != SM_SECTION_ORDER:
        errors.append(
            f"sections must be exactly {list(SM_SECTION_ORDER)} in order, "
            f"got {ids}")
        return errors, notes
    by_id = {s["id"]: s for s in sections if isinstance(s, dict)}

    team_errors, team_notes = _sm_check_teams(by_id["teams"])
    errors += team_errors
    notes += team_notes

    _, league_errors = _sm_briefs(by_id["leagues"], "leagues")
    errors += league_errors

    season_errors, season_notes = _sm_check_seasons(
        by_id["seasons"], edition.get("edition_date"))
    errors += season_errors
    notes += season_notes

    water_errors, water_notes = _sm_check_water(by_id["water"], fishing)
    errors += water_errors
    notes += water_notes

    # Sumo advisory, inherited from the Times when Sports moved here: a
    # basho in progress should be visible somewhere in the sport pages.
    date = edition.get("edition_date")
    if _is_str(date) and config.is_basho_window(date):
        text = " ".join(
            f"{b.get('headline', '')} {b.get('summary', '')}"
            for sid in ("teams", "leagues")
            for b in (by_id.get(sid, {}).get("briefs") or [])
            if isinstance(b, dict)).lower()
        if not any(word in text for word in config.SUMO_KEYWORDS):
            notes.append(
                f"{date} falls inside a basho window and no sumo appears in "
                "Our Teams or Around the Leagues — tournament coverage "
                "should exist; confirm the dates by search")

    # Exact size, measured off the real payload builder — never estimated.
    try:
        import post_discord
        payload = post_discord.build_sportsman_payload(copy.deepcopy(edition))
        chars = post_discord.embed_text_length(payload["embeds"])
        if chars > 6000:
            errors.append(f"embeds measure {chars} chars — over Discord's "
                          "6000 ceiling")
        elif chars > 5600:
            notes.append(f"embeds measure {chars} chars — close to the 6000 "
                         "ceiling")
    except Exception as exc:  # noqa: BLE001 — measurement, not delivery
        notes.append(f"could not measure the payload ({exc}); size unchecked")

    return errors, notes


def main() -> int:
    config.use_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="editions/YYYY-MM-DD.json")
    stats_group = parser.add_mutually_exclusive_group()
    stats_group.add_argument("--stats",
                             help="out/stats.json for the stat-strip truth check")
    stats_group.add_argument("--no-stats", action="store_true",
                             help="skip the stat-strip truth check (fixtures only)")
    fishing_group = parser.add_mutually_exclusive_group()
    fishing_group.add_argument("--fishing",
                               help="out/fishing.json for the fishing-line check")
    fishing_group.add_argument("--no-fishing", action="store_true",
                               help="skip the fishing-line check (fixtures only)")
    parser.add_argument("--sportsman", action="store_true",
                        help="validate a Sports & Sportsman edition against "
                             "its own contract instead of the newspaper's")
    parser.add_argument("--no-urls", action="store_true",
                        help="skip url liveness checks (offline)")
    parser.add_argument("--strict", action="store_true",
                        help="treat advisories as failures")
    parser.add_argument("--no-write", action="store_true",
                        help="never rewrite the edition file after stripping urls")
    parser.add_argument("--quiet", action="store_true",
                        help="suppress the OK summary line")
    args = parser.parse_args()

    edition, problem = _load_json(args.path)
    if problem:
        print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    if not isinstance(edition, dict):
        print("ERROR: edition is not a JSON object", file=sys.stderr)
        return 1

    errors: list[str] = []
    notes: list[str] = []

    if args.sportsman:
        fishing, fishing_notes = _resolve_fishing(
            args.fishing, skip=args.no_fishing)
        notes += fishing_notes
        sm_errors, sm_notes = validate_sportsman(edition, fishing)
        errors += sm_errors
        notes += sm_notes
        basename = os.path.basename(args.path)
        dated = DATED_FILE_RE.match(basename)
        if dated and edition.get("edition_date") != dated.group(1):
            errors.append(
                f"edition_date {edition.get('edition_date')!r} does not "
                f"match the filename {basename}")
        for note in notes:
            print(f"WARN: {note}", file=sys.stderr)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        if errors:
            print(f"FAILED: {len(errors)} error(s)", file=sys.stderr)
            return 1
        if not args.quiet:
            sections = {s.get("id"): s for s in edition.get("sections") or []}
            briefs = sum(len(sections.get(k, {}).get("briefs") or [])
                         for k in ("teams", "leagues"))
            print(f"OK: {args.path} — Sports & Sportsman No. "
                  f"{edition.get('edition_number')}, {briefs} briefs, "
                  f"{len(sections.get('water', {}).get('waters') or [])} waters")
        return 0

    # Resolved first: a dated edition is a real morning paper, and the
    # fetched-data gates are stricter for one than they are for a fixture.
    basename = os.path.basename(args.path)
    dated = DATED_FILE_RE.match(basename)

    stats, stat_notes, stat_errors = _resolve_stats(
        args.stats, skip=args.no_stats, dated=bool(dated)
    )
    notes += stat_notes
    errors += stat_errors

    fishing, fishing_notes = _resolve_fishing(args.fishing, skip=args.no_fishing)
    notes += fishing_notes

    if dated and edition.get("edition_date") != dated.group(1):
        errors.append(
            f"edition_date {edition.get('edition_date')!r} does not match the "
            f"filename {basename}"
        )
    if dated:
        ledger_errors, ledger_notes = _check_ledger(edition, dated.group(1))
        errors += ledger_errors
        notes += ledger_notes

    stripped: list[str] = []
    if not args.no_urls:
        stripped = strip_dead_urls(edition)
        notes += stripped

    errors += validate(edition, stats=stats, check_urls=False, fishing=fishing)
    notes += advisories(edition, stats=stats, fishing=fishing)

    # Only ever rewrite a real dated edition; fixtures stay byte-stable.
    if stripped and dated and not args.no_write:
        rewrote = any(n.startswith("stripped") for n in stripped)
        if rewrote:
            with open(args.path, "w", encoding="utf-8", newline="\n") as f:
                json.dump(edition, f, indent=2, ensure_ascii=False)
                f.write("\n")
            notes.append(f"rewrote {args.path} without the dead url(s)")

    for note in notes:
        print(f"WARN: {note}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1
    if args.strict and notes:
        print(f"FAILED: {len(notes)} advisory(ies) under --strict", file=sys.stderr)
        return 1

    if not args.quiet:
        briefs = len(_briefs_of(edition))
        lead = edition.get("lead") or {}
        stat_count = len(lead.get("stat_strip") or [])
        notebook = len(_wv_items_of(edition))
        print(
            f"OK: {args.path} — Edition No. {edition.get('edition_number')}, "
            f"{briefs} briefs across {len(edition.get('sections') or [])} sections, "
            f"{notebook} notebook line{'' if notebook == 1 else 's'}, "
            f"{stat_count} stat entr{'y' if stat_count == 1 else 'ies'}, "
            f"~{estimate_embed_chars(edition)} embed chars"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
