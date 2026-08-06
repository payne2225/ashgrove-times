"""Display metadata, budgets, and paths for The Ashgrove Times.

The edition JSON is CONTENT ONLY. Every emoji, color, label, ordering rule,
font, and byte budget lives here instead, so the one artifact the daily
routine writes by hand stays a plain content document that survives a
redesign. If a renderer or the poster needs to know how something *looks*,
it imports it from this module.

Colors are computed with `int(hex, 16)` at import. Ian's handoff states
`#3E3221 -> 3419169`, which is wrong (0x3E3221 = 4076065; 3419169 is
0x342C21) — hand-converted decimals are banned for exactly that reason.

There are deliberately NO Discord user IDs in this repo: it is public, and
the paper never pings anybody. The crew appears in REGIONS by FIRST NAME
ONLY — no ids, no ZIPs, no addresses, ever. The same rule binds the source
code, not just the rendered paper: no employer, no workplace, no private
property tied to a stretch of river. A comment nobody renders is still
published the moment the repo is.

Nothing here touches the network or writes a file at import. Path constants
are plain `str` so `os.path.join`, f-strings, and `+` all behave.
"""

from __future__ import annotations

import datetime
import json
import os
import sys

# Sent to USGS, NOAA, Yahoo, CoinGecko and Discord on every request. It
# identifies the PROJECT, never a person: a contact address here is a
# personal address published to four third parties and to anyone who reads
# the repo. USGS and NOAA both accept a UA without one.
USER_AGENT = "ashgrove-times/1.0 (+https://github.com/payne2225/ashgrove-times)"

# ---------------------------------------------------------------- identity

MASTHEAD = "THE ASHGROVE TIMES"
TAGLINE = "For the Fellers"
WEBHOOK_USERNAME = "The Ashgrove Times"
BYLINE = "Wire Reports"
SOURCES_NOTE = "Compiled from wire reports"
VOLUME = "I"
FIRST_EDITION_DATE = "2026-08-05"

# ------------------------------------------------------- publication window

# The paper lands ahead of Claude the Weatherman's 7:15 file, so the edition
# carries a WEATHER EAR — the small boxed pointer a real front page runs
# beside the masthead.
#
# THE CRON IS UTC-FIXED AND THE ET POST TIME THEREFORE MOVES WITH DAYLIGHT
# SAVING. `0 11 * * *` is 7:00 AM EDT and 6:00 AM EST, so leaving it alone
# through the winter lands the paper 75 minutes ahead of the forecast while
# every "fifteen minutes" phrasing in the repo keeps claiming 15. That is
# why the cron has TWO settings and a dated switch — the commitment lives in
# docs/LEDGER.md — and why nothing hard-codes the gap in words: it is
# derived per date by weather_gap_minutes() / weather_gap_words().
POST_TIME_ET = "7:00 AM ET"   # the TARGET, which both crons are aimed at
POST_TIME_24H = "07:00"
# THE ROUTINE WAKES AT 6:00, NOT 7:00. Measured 2026-08-06: research +
# render + push took 37 minutes, so a 7:00 wake put the paper in the channel
# at 7:41 — 26 minutes AFTER the Weatherman it is supposed to precede, while
# its own ear promised the forecast was still coming. Waking early and
# holding the post until 7:00 (`--not-before`) fixes the ordering, and the
# hold doubles as the GitHub Pages build window so the permalink is live.
#
# A full hour, not the 37 minutes measured: research time varies with the
# news, a slow wire day is exactly when the paper most needs the room, and
# arriving early costs nothing because delivery is held either way.
POST_CRON_UTC = "0 10 * * *"           # daylight time (Mar-Nov) -> 6:00 AM EDT
POST_CRON_UTC_STANDARD = "0 11 * * *"  # standard time (Nov-Mar) -> 6:00 AM EST

# The wall-clock ET time the paper is due in the channel. The routine may
# finish early; it may not post early.
POST_TARGET_ET = "07:00"
WEATHER_BOT = "Claude the Weatherman"
WEATHER_TIME_ET = "7:15"

WEATHER_EAR_MAX_CHARS = 90

# A pool, not a string: an ear that reads identically every morning stops
# being a pointer and becomes furniture. Every line names the 7:15 slot,
# which is the only part the reader actually needs — and NO line states the
# gap in minutes, because the gap depends on which cron is installed and
# whether the clocks have changed. Name the time, never the interval.
WEATHER_EAR_LINES = [
    "Claude the Weatherman files the forecast at 7:15.",
    "Weather follows at 7:15 — the Weatherman has the day's sky.",
    "Look for the forecast at 7:15, from the weather desk.",
    "The weather desk reports at 7:15.",
    "Next edition of the sky: Claude the Weatherman, 7:15.",
    "Forecast at 7:15 — read this, then dress for it.",
    "Claude the Weatherman posts the outlook at 7:15.",
    "The Weatherman files at 7:15, after this edition.",
]


def weather_ear(date: str | None = None) -> str:
    """A weather-ear line, rotated by date so consecutive days differ.

    Deterministic: the same date always yields the same line, so a rerun of
    a day reproduces the same paper.
    """
    digits = "".join(ch for ch in (date or "") if ch.isdigit())
    if not digits:
        return WEATHER_EAR_LINES[0]
    return WEATHER_EAR_LINES[int(digits) % len(WEATHER_EAR_LINES)]


# ------------------------------------------- daylight saving and the gap

# US Eastern is computed here by plain calendar arithmetic — second Sunday
# in March through the first Sunday in November — instead of zoneinfo,
# because zoneinfo needs the `tzdata` package on Windows and Nate's manual
# fallback runs happen on Windows. Nothing in this repo may depend on a
# third-party tz database to know what time the paper landed.


def _parse_iso(date: str | None) -> tuple[int, int, int] | None:
    """(year, month, day) from a YYYY-MM-DD string, or None if unusable."""
    if not isinstance(date, str) or len(date) < 10:
        return None
    try:
        return int(date[0:4]), int(date[5:7]), int(date[8:10])
    except ValueError:
        return None


def _today_iso() -> str:
    """Local calendar date. Called at runtime only, never at import."""
    return datetime.date.today().isoformat()


def _nth_sunday(year: int, month: int, n: int) -> int:
    """Day-of-month of the nth Sunday (n=1 is the first)."""
    first_weekday = datetime.date(year, month, 1).weekday()  # Mon=0 .. Sun=6
    first_sunday = 1 + (6 - first_weekday) % 7
    return first_sunday + 7 * (n - 1)


def is_eastern_dst(date: str | None = None) -> bool:
    """True when US Eastern is on daylight time (EDT) on an ISO date.

    Boundary days resolve for the 6-7 AM hour this paper cares about, which
    is after the 2 AM changeover in both directions.
    """
    parsed = _parse_iso(date or _today_iso())
    if parsed is None:
        return True
    year, month, day = parsed
    if month < 3 or month > 11:
        return False
    if 4 <= month <= 10:
        return True
    if month == 3:
        return day >= _nth_sunday(year, 3, 2)
    return day < _nth_sunday(year, 11, 1)


def et_utc_offset_hours(date: str | None = None) -> int:
    """Hours behind UTC that Eastern runs on a date: 4 (EDT) or 5 (EST)."""
    return 4 if is_eastern_dst(date) else 5


def cron_for(date: str | None = None) -> str:
    """The UTC cron that actually wakes the routine at 6:00 AM ET on a date.

    Two settings, one target. Installing the wrong one does not break the
    paper — it slides it an hour and silently widens the weather gap.
    """
    return POST_CRON_UTC if is_eastern_dst(date) else POST_CRON_UTC_STANDARD


def now_et() -> datetime.datetime:
    """Wall-clock Eastern time, as a naive datetime.

    The cloud sandbox runs on UTC, so anything that reasons about "7:00 in
    the morning" has to convert explicitly. Reading the local clock there
    would put the paper out five hours early — or, for a delivery hold,
    conclude the target had already passed and skip the wait entirely.

    Derived from the same DST rule as the cron rather than zoneinfo, so the
    two can never disagree about which side of the changeover a date is on.
    """
    utc = datetime.datetime.now(datetime.timezone.utc)
    return (utc - datetime.timedelta(hours=et_utc_offset_hours())).replace(tzinfo=None)


def _cron_minutes_utc(cron: str) -> int:
    """Minutes past midnight UTC that a `M H * * *` cron fires."""
    fields = cron.split()
    return int(fields[1]) * 60 + int(fields[0])


def _time_minutes(hhmm: str) -> int:
    """'7:15' -> 435. Bare clock string, no meridiem."""
    hour, _, minute = hhmm.partition(":")
    return int(hour) * 60 + int(minute or 0)


def wake_minutes_et(date: str | None = None, cron: str | None = None) -> int:
    """Minutes past midnight ET at which the INSTALLED cron actually fires.

    Pass the cron that is really in the routine. The default is the module's
    daylight-time setting, which is the whole point of the check: if nobody
    switched it in November this returns 300 (5:00 AM), not 360.
    """
    utc = _cron_minutes_utc(cron or POST_CRON_UTC)
    return (utc - et_utc_offset_hours(date) * 60) % (24 * 60)


def post_minutes_et(date: str | None = None, cron: str | None = None) -> int:
    """Minutes past midnight ET at which the paper actually reaches readers.

    This is the DELIVERY time, not the wake time. `post_discord.py
    --not-before` holds the post at POST_TARGET_ET however early the routine
    woke, so the cron no longer decides when readers get their paper — it
    only decides how much head start the research gets.

    The one case where the cron still moves delivery is a run that overshoots
    the target, which the poster reports for itself rather than predicting
    here.
    """
    return _time_minutes(POST_TARGET_ET)


def head_start_minutes(date: str | None = None, cron: str | None = None) -> int:
    """Minutes between waking and the delivery target. 60 when correct.

    This, not the reader-facing gap, is what a missed daylight-saving switch
    actually costs — `--not-before` pins delivery either way. The two
    failures are not symmetric:

      * Missing the NOVEMBER switch wakes the routine at 5:00 and hands it a
        120-minute head start. Wasteful, invisible to readers, harmless.
      * Missing the MARCH switch wakes it at 7:00, a head start of ZERO. The
        hold is already past on arrival, so the paper posts whenever the
        research happens to finish — roughly 40 minutes late, after the
        forecast it points at.

    So <= 0 is the alarming direction, not merely "not 60".
    """
    return _time_minutes(POST_TARGET_ET) - wake_minutes_et(date, cron)


def weather_gap_minutes(date: str | None = None, cron: str | None = None) -> int:
    """Minutes between the paper landing and the 7:15 forecast.

    15 whenever the routine finishes before its delivery target, which is
    the normal case now that delivery is held rather than left to the cron.
    Derived, never asserted — the number in the prose has to come from here
    or not be written at all.
    """
    return _time_minutes(WEATHER_TIME_ET) - post_minutes_et(date, cron)


_GAP_WORDS = {
    15: "fifteen minutes",
    30: "half an hour",
    45: "forty-five minutes",
    60: "an hour",
    75: "an hour and a quarter",
}


def weather_gap_words(date: str | None = None, cron: str | None = None) -> str:
    """The gap as English, derived. Use this instead of typing 'fifteen'."""
    minutes = weather_gap_minutes(date, cron)
    return _GAP_WORDS.get(minutes, f"{minutes} minutes")


# Dated commitments this module cannot enforce on its own; docs/LEDGER.md
# carries them as forward-dated rows and the routine reads it every morning.
CRON_SWITCH_DATES = {
    "2026-11-01": POST_CRON_UTC_STANDARD,  # EDT ends; 11:00 UTC becomes 6 AM ET
    "2027-03-14": POST_CRON_UTC,           # EDT resumes; 12:00 UTC becomes 8 AM ET
}


# ------------------------------------------------------------------ colors


def _color(hex6: str) -> int:
    """Hex string -> the decimal int a Discord embed wants."""
    return int(hex6.lstrip("#"), 16)


def _rgb(hex6: str) -> tuple[int, int, int]:
    """Hex string -> an (r, g, b) tuple Pillow wants."""
    h = hex6.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# Ian's settled tokens: parchment field, near-black ink, muted gold-brown.
PALETTE = {
    "parchment": "#f4f0e6",
    "parchment_alt": "#e9e4d8",
    "ink": "#1c1a16",
    "ink_soft": "#4a453c",
    "accent": "#8a6d3f",
    "rule": "#3e3221",
}

PALETTE_RGB = {name: _rgb(value) for name, value in PALETTE.items()}


def rgb(name: str) -> tuple[int, int, int]:
    """Palette color as an (r, g, b) tuple for Pillow."""
    return PALETTE_RGB[name]


# ---------------------------------------------------------------- sections

# `order` is display order (the lead is 0). `standing` marks the two
# sections Ian declared non-negotiable — they run even on a dead news day
# and are never emptied by the trim path. `trim_priority` is the drop order
# when a payload is over budget: HIGHER trims first, 0 means never trimmed.
SECTIONS = [
    {
        "id": "us",
        "label": "U.S.",
        "emoji": "\U0001F1FA\U0001F1F8",
        "color": _color("3E3221"),
        "order": 1,
        "standing": False,
        "trim_priority": 2,
    },
    {
        "id": "world",
        "label": "World",
        "emoji": "\U0001F30D",
        "color": _color("4A3C28"),
        "order": 2,
        "standing": False,
        "trim_priority": 3,
    },
    {
        "id": "wv",
        "label": "West Virginia",
        "emoji": "\U0001F3D4\uFE0F",
        "color": _color("57462C"),
        "order": 3,
        "standing": True,
        "trim_priority": 0,
    },
    {
        "id": "sports",
        "label": "Sports",
        "emoji": "\U0001F3C6",
        "color": _color("6B5636"),
        "order": 4,
        "standing": True,
        "trim_priority": 1,
    },
    {
        "id": "scitech",
        "label": "Science & Technology",
        "emoji": "\U0001F52C",
        "color": _color("7C6640"),
        "order": 5,
        "standing": False,
        "trim_priority": 4,
    },
]

SECTION_IDS = [s["id"] for s in SECTIONS]

# The lead is not a section (it has its own shape in the edition JSON) but
# it needs the same display metadata for its embed.
LEAD = {
    "id": "lead",
    "label": "Lead Story",
    "emoji": "\U0001F5DE\uFE0F",
    "color": _color("1C1A16"),
    "order": 0,
}

LEAD_COLOR = LEAD["color"]

_SECTIONS_BY_ID = {s["id"]: s for s in SECTIONS}


def section_by_id(sid: str) -> dict:
    """Display metadata for a section id. Raises KeyError on an unknown id.

    Unknown ids are a bug, not a runtime condition — the five ids are frozen.
    """
    try:
        return _SECTIONS_BY_ID[sid]
    except KeyError:
        raise KeyError(
            f"unknown section id {sid!r}; expected one of {SECTION_IDS}"
        ) from None


def trim_order() -> list[str]:
    """Section ids in the order the trim path drops briefs (never-trim omitted)."""
    trimmable = [s for s in SECTIONS if s["trim_priority"] > 0]
    trimmable.sort(key=lambda s: -s["trim_priority"])
    return [s["id"] for s in trimmable]


# --------------------------------------------------------------- the regions

# The West Virginia notebook is the local anchor of the paper, so it runs a
# regional roundup across the crew's actual towns instead of a second wire
# section. The towns come from the sibling weatherman project; they are
# GROUPED INTO REAL MEDIA MARKETS here rather than emitted one line per
# hamlet, because Lesage has no daily news of its own and a line per town is
# how a paper starts inventing one.
#
# `is_away` splits the notebook's two roundups: False -> the WV regional
# roundup, True -> the away desk for out-of-state crew. `outlets` is a
# starting point for the search, NOT an attribution whitelist — attribute
# whatever you actually read.
#
# FIRST NAMES ONLY. No ids, no ZIPs, no addresses: this repo goes public.
# `note` is an editorial hint about the REGION and nothing finer — it may
# never say where a specific person works or lives, or tie private property
# to a named stretch of water. The region label is as precise as this repo
# ever gets about a person, in source exactly as much as in print.
REGIONS = [
    {
        "region_id": "huntington_cabell",
        "place": "Huntington & the Cabell-Mason corridor",
        "people": ["Trav", "Justin", "Nate", "Ian"],
        "towns": ["Huntington", "Lesage", "Apple Grove", "Point Pleasant"],
        "is_away": False,
        "outlets": ["WSAZ", "The Herald-Dispatch", "WOWK"],
    },
    {
        "region_id": "putnam_kanawha",
        "place": "Putnam / Kanawha - Charleston",
        "people": ["Nate"],
        "towns": ["Hurricane", "Charleston", "Teays Valley"],
        "is_away": False,
        "outlets": ["WV MetroNews", "WCHS", "Charleston Gazette-Mail"],
        "note": "Nate's work region",
    },
    {
        "region_id": "mid_ohio_valley",
        "place": "Mid-Ohio Valley / Parkersburg",
        "people": ["Pat"],
        "towns": ["Parkersburg", "Vienna", "Ravenswood"],
        "is_away": False,
        "outlets": ["Parkersburg News and Sentinel", "WTAP"],
    },
    {
        "region_id": "nicholas_webster",
        "place": "Nicholas & Webster / Summersville - Cowen",
        "people": ["Clayton"],
        "towns": ["Summersville", "Cowen", "Webster Springs"],
        "is_away": False,
        "outlets": ["WV MetroNews", "The Register-Herald"],
        "note": "the cabin region",
    },
    {
        "region_id": "summers_new_river",
        "place": "Summers / Hinton & the New River",
        "people": ["Greg"],
        "towns": ["Hinton", "Sandstone"],
        "is_away": False,
        "outlets": ["The Register-Herald", "WVVA"],
    },
    {
        "region_id": "vermont",
        "place": "North Bennington, VT",
        "people": ["Wes"],
        "towns": ["North Bennington", "Bennington"],
        "is_away": True,
        "outlets": ["Bennington Banner", "VTDigger"],
    },
    {
        "region_id": "prince_george",
        "place": "Prince George, BC",
        "people": ["Kirsten"],
        "towns": ["Prince George"],
        "is_away": True,
        "outlets": ["Prince George Citizen", "CBC British Columbia"],
    },
    {
        "region_id": "topsail",
        "place": "Topsail Beach, NC",
        "people": [],
        "towns": ["Topsail Beach", "Surf City"],
        "is_away": True,
        "outlets": ["WECT", "Wilmington StarNews"],
        "note": "the beach place",
    },
]

REGION_IDS = [r["region_id"] for r in REGIONS]
WV_REGION_IDS = [r["region_id"] for r in REGIONS if not r["is_away"]]
AWAY_REGION_IDS = [r["region_id"] for r in REGIONS if r["is_away"]]

_REGIONS_BY_ID = {r["region_id"]: r for r in REGIONS}


def region_by_id(rid: str) -> dict:
    """A region definition by id. Raises KeyError on an unknown id."""
    try:
        return _REGIONS_BY_ID[rid]
    except KeyError:
        raise KeyError(
            f"unknown region_id {rid!r}; expected one of {REGION_IDS}"
        ) from None


def wv_regions() -> list[dict]:
    """The five in-state regions, in display order."""
    return [r for r in REGIONS if not r["is_away"]]


def away_regions() -> list[dict]:
    """The away desk: crew who are out of state but still in the paper."""
    return [r for r in REGIONS if r["is_away"]]


# ------------------------------------------------------------ discord budgets

# Discord's real ceilings. EMBED_TOTAL_LIMIT is the SUM of title +
# description + field.name + field.value + footer.text + author.name across
# EVERY embed in one message; embed.url and image.url are not counted.
EMBED_TOTAL_LIMIT = 6000
EMBED_TARGET = 5600   # aim here
EMBED_HARD = 5800     # trim above here, leaving headroom for Discord's count

# What to do when a full day will not fit ONE message. Trimming costs news;
# splitting costs a second post. Measured on the 2026-08-05 edition: trimming
# to fit dropped 7 of 9 notebook lines and 3 briefs, while splitting kept
# everything (front page ~3,400 chars, inside ~5,300, both under the ceiling).
# The West Virginia notebook is what these readers showed up for, so the
# scissors are the wrong default. Set False to prefer one trimmed message.
PREFER_SPLIT_OVER_TRIM = True
CONTENT_LIMIT = 2000  # top-level content, hard-capped regardless of Nitro
CHUNK_LIMIT = 1900    # text-mode split size, leaves room for a chunk marker
EMBED_TITLE_LIMIT = 256
EMBED_DESC_LIMIT = 4096
EMBED_FIELD_VALUE_LIMIT = 1024
EMBED_FIELD_COUNT_LIMIT = 25
EMBED_COUNT_LIMIT = 10
ATTACH_BYTE_BUDGET = 7_000_000  # free-tier ceiling is 10 MB; stay well under
ATTACH_COUNT_LIMIT = 10

# Only user mentions ever ping, and the paper adds none of its own.
ALLOWED_MENTIONS = {"parse": ["users"]}

# ---------------------------------------------------------------- editorial

LEAD_BODY_MIN = 2
LEAD_BODY_MAX = 3
STAT_STRIP_MAX = 6
BRIEFS_MIN = 1            # a section may never be empty
BRIEFS_TARGET = 3
BRIEFS_MAX = 4            # more than this and the budget stops closing
STANDING_MIN_BRIEFS = 1   # wv and sports survive at one brief
HEADLINE_TARGET_CHARS = 58
# Derived from EMBED_BUDGET above, not preferred: a wire section's 750 buys
# three briefs at ~245 each once the masked source link is paid for.
SUMMARY_TARGET_CHARS = 140
SUMMARY_WARN_CHARS = 210

# EMBED_BUDGET is how 5600 chars are actually spent. It exists because
# "three briefs a section" and "an expanded West Virginia notebook" only
# both fit if somebody writes down who gets what — without it the trim path
# silently decides, and it decides by deleting Science & Technology.
#
# THE URL IS PART OF THE BRIEF. post_discord.py sends masked source links —
# ` · [WSAZ](https://www.wsaz.com/)` — and Discord counts every character of
# that url against the 6000. An allocation derived from headline + summary +
# outlet name alone under-reports a full edition by around 700 chars, which
# is exactly how the notebook used to get eaten at post time. These numbers
# are measured off a real payload, url markup included:
#
#   brief          ~245 = 55 headline + 130 summary + outlet + url + markup
#   wire section    ~740 = 12 title + three briefs + the blank lines between
#   notebook line  ~195 regional/away (place, roster, sentence, source, url)
#                  ~130 fishing (no url printed — the source is the station)
#   lead           ~875 = headline, dek, three paragraphs, ticker, byline
#   chrome          ~180 = kicker + colophon + weather ear, in one footer
#
# West Virginia gets twice a wire section because it carries four parts, and
# it is the section this paper exists to run. Its line assumes the playbook's
# own rule: when regional, away AND fishing are all filing, statewide runs
# TWO briefs, not three. Three statewide plus a full notebook is ~1710 and
# will (correctly) be named by the validator as the thing to cut.
#
# This allocation describes a TYPICAL day. The hard guarantee that the paper
# always fits one message is separate and lives in
# validate_edition.irreducible_chars(): even trimmed to one brief a section,
# with the fattest legal notebook still intact, the message must fit.
#
# validate_edition.py reports any section over its line. Sum == EMBED_TARGET.
EMBED_BUDGET = {
    "lead": 900,
    "us": 750,
    "world": 750,
    "wv": 1500,
    "sports": 750,
    "scitech": 750,
    "chrome": 200,   # the closing footer: kicker + sources_note + weather ear
}

EMBED_BUDGET_TOTAL = sum(EMBED_BUDGET.values())


def embed_budget(key: str) -> int:
    """The char allocation for a section id, 'lead', or 'chrome'."""
    return EMBED_BUDGET.get(key, 0)


# ----------------------------------------- the West Virginia notebook

# WV does not run the two-column brief layout the wire sections use. It
# runs Ian's .wv-box: bordered, tinted, titled. That distinction is the
# whole point — it makes West Virginia read as the local anchor of the
# paper rather than another wire section — and it carries into the HTML,
# the Discord embed, and any Pillow card.
#
# Four parts, in this order: statewide briefs (always), a regional roundup
# over REGIONS, an away desk, then fishing. Only regions with GENUINE news
# get a line. Thin is legal; padding is not.
WV_NOTEBOOK_TITLE = "Mountaineer State Notebook"
WV_SUBHEADS = {
    "regional": "Around the State",
    "away": "The Away Desk",
    "fishing": "On the Water",
}

WV_BRIEFS_TARGET = 2      # statewide items; 3 only when the notebook is lean
WV_BRIEFS_MAX = 3

# Regional and away entries are ONE SENTENCE. Not a brief, not two clauses
# stapled together — the ceiling is what keeps the notebook from eating the
# rest of the paper.
WV_ITEM_TARGET_CHARS = 110
WV_ITEM_MAX_CHARS = 140
WV_PLACE_MAX_CHARS = 48
WV_REGIONAL_MAX = len(WV_REGION_IDS)
WV_AWAY_MAX = len(AWAY_REGION_IDS)

# Every region CAN file; on a normal morning about six lines total is what
# the WV allocation actually pays for. This is a target, never a gate — a
# real eighth item beats an artificial cap, and nothing may drop genuine
# news to hit a number.
WV_NOTEBOOK_LINES_TARGET = 6

# Fishing lines carry measured numbers, so they get a little more room than
# a regional sentence and are allowed to run past one sentence.
WV_FISHING_MAX = 2
WV_FISHING_LINE_MAX_CHARS = 180

# The two waters fetch_fishing.py reports, keyed as it keys them. A fishing
# entry naming any other water is invented.
FISHING_WATERS = {
    "williams": "Williams River (Cowen)",
    "topsail": "Topsail Beach (surf and sound)",
}

# Topsail has no water-temperature station of its own. The reading comes
# from Wrightsville Beach, 25 miles down the coast, and any line that
# prints a Topsail water temperature has to say so.
TOPSAIL_TEMP_STATION_NAME = "Wrightsville Beach"
TOPSAIL_TEMP_MILES = 25

# Not fetched, on purpose: wvdnr.gov serves an EXPIRED TLS certificate, so
# trout stocking is a web-search item in the playbook with a silent no-op
# when nothing turns up. Never a fetch, never verify=False.
WVDNR_STOCKING_IS_SEARCH_ONLY = True

# Sumo, settled by Ian: covered when there is something to cover, NOT a
# headline every day regardless. During a basho it should usually win the
# sports lead; off-months a one-line note is the honest version of "no sumo
# news" and its absence is not an error. SUMO_REQUIRED_DAILY stays False —
# nothing may fail an edition for a missing sumo brief.
SUMO_REQUIRED_DAILY = False
SUMO_LEADS_SPORTS_IN_BASHO = True
SUMO_BASHO_DAYS = 15
SUMO_BASHO_MONTHS = [1, 3, 5, 7, 9, 11]
SUMO_KEYWORDS = (
    "sumo", "basho", "yokozuna", "ozeki", "sekiwake", "komusubi", "maegashira",
    "banzuke", "makuuchi", "juryo", "sekitori", "kyujo", "heya", "kachi-koshi",
    "make-koshi", "yusho", "honbasho", "rikishi", "oyakata", "dohyo",
)


def is_basho_month(month: int) -> bool:
    """True in a Grand Sumo tournament month (Jan/Mar/May/Jul/Sep/Nov)."""
    return month in SUMO_BASHO_MONTHS


def basho_window(year: int, month: int) -> tuple[int, int] | None:
    """(first day, last day) of the basho in a month, or None if there is none.

    A honbasho opens on the SECOND SUNDAY and runs SUMO_BASHO_DAYS days, so
    the window is exactly 15 days wide — the same 15 the validator's
    advisory says out loud. The second Sunday falls on the 8th through the
    14th, so the window never spills into the next month.
    """
    if not is_basho_month(month):
        return None
    start = _nth_sunday(year, month, 2)
    return start, start + SUMO_BASHO_DAYS - 1


def is_basho_window(date: str) -> bool:
    """Is a Grand Sumo tournament running on this ISO date?

    Derived from the second-Sunday rule rather than a padded envelope: an
    envelope that stays True for six days after the tournament ends tells
    the routine to go find coverage that does not exist, and the cheapest
    way to clear that note is to invent a sumo line. The JSA does shift a
    basho occasionally (venue and holiday conflicts), so this decides how
    loudly the validator ADVISES and never what gets published — confirm the
    real dates by search, and put them in docs/LEDGER.md.
    """
    parsed = _parse_iso(date)
    if parsed is None:
        return False
    year, month, day = parsed
    window = basho_window(year, month)
    if window is None:
        return False
    return window[0] <= day <= window[1]


# -------------------------------------------------------------------- paths

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
EDITIONS_DIR = os.path.join(PROJECT_ROOT, "editions")
SITE_DIR = os.path.join(PROJECT_ROOT, "site")
SITE_EDITIONS_DIR = os.path.join(SITE_DIR, "editions")
OUT_DIR = os.path.join(PROJECT_ROOT, "out")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
FONT_DIR = os.path.join(ASSETS_DIR, "fonts")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

INDEX_PATH = os.path.join(EDITIONS_DIR, "index.json")
FIXTURE_PATH = os.path.join(EDITIONS_DIR, "_fixture.json")
STATS_PATH = os.path.join(OUT_DIR, "stats.json")
FISHING_PATH = os.path.join(OUT_DIR, "fishing.json")
TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, "broadsheet.html")
MASTHEAD_FALLBACK_PNG = os.path.join(ASSETS_DIR, "masthead-fallback.png")
SITE_INDEX_PATH = os.path.join(SITE_DIR, "index.html")
SITE_ARCHIVE_PATH = os.path.join(SITE_DIR, "archive.html")


def edition_path(date: str) -> str:
    """The committed content file for a date: editions/YYYY-MM-DD.json."""
    return os.path.join(EDITIONS_DIR, f"{date}.json")


def site_edition_path(date: str) -> str:
    """The published broadsheet for a date: site/editions/YYYY-MM-DD.html."""
    return os.path.join(SITE_EDITIONS_DIR, f"{date}.html")


def hero_filename(date: str) -> str:
    """The attachment filename. Frozen — the multipart wiring depends on it."""
    return f"ashgrove-{date}.png"


def hero_path(date: str) -> str:
    """Where render_edition.py writes the hero card: out/ashgrove-DATE.png."""
    return os.path.join(OUT_DIR, hero_filename(date))


def payload_path(date: str) -> str:
    """Where post_discord.py dumps the exact bytes it sent."""
    return os.path.join(OUT_DIR, f"{date}.payload.json")


def font_path(key: str) -> str:
    """Absolute path to a vendored TTF by role key."""
    return FONTS[key]


# --------------------------------------------------------------------- fonts

# Static instances only — variable axes are baked offline with fontTools,
# which is never a runtime dependency. Note the upstream google/fonts path
# is `OldStandard-*`, not `OldStandardTT-*`.
FONT_FILENAMES = {
    "headline": "PlayfairDisplay-Bold.ttf",
    "headline_black": "PlayfairDisplay-Black.ttf",
    "body": "SourceSerif4-Regular.ttf",
    "body_semibold": "SourceSerif4-Semibold.ttf",
    "body_italic": "SourceSerif4-Italic.ttf",
    "masthead": "OldStandard-Regular.ttf",
}

FONTS = {key: os.path.join(FONT_DIR, name) for key, name in FONT_FILENAMES.items()}

# The VIEWER's browser fetches these, never the sandbox — the HTML edition
# links them and falls back to a local serif stack.
GOOGLE_FONTS_HREF = (
    "https://fonts.googleapis.com/css2"
    "?family=Old+Standard+TT:ital,wght@0,400;0,700;1,400"
    "&family=Playfair+Display:ital,wght@0,700;0,900;1,700"
    "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400"
    "&display=swap"
)
FONT_STACK_MASTHEAD = "'Old Standard TT', 'Playfair Display', Georgia, serif"
FONT_STACK_HEADLINE = (
    "'Playfair Display', 'Old Standard TT', Georgia, 'Times New Roman', serif"
)
FONT_STACK_BODY = "'Source Serif 4', Georgia, 'Times New Roman', serif"

HERO_SIZE = (1200, 630)  # 1.91:1 — Discord shows an attachment at ~550px wide

# ------------------------------------------------------------------- hosting

# Activated 2026-08-05: payne2225/ashgrove-times is public and Pages builds
# from .github/workflows/pages.yml. Everything downstream is conditional on
# this one flag — set it False and the paper still posts, just without the
# permalink line and with every embed.url dropped.
PAGES_ENABLED = True
PAGES_BASE_URL = "https://payne2225.github.io/ashgrove-times"
# How long to wait for the Pages build BEFORE posting. Deliberately short:
# the paper is due at 7:00 and the Weatherman follows at 7:15, so a late
# paper costs more than a late link.
PAGES_WAIT_SECONDS = 120

# How long to keep waiting AFTER posting, to patch the permalink in.
# Measured builds: 23s one evening, 8m38s the next morning — the Actions
# queue does not care about our deadline, so this window is generous. The
# paper is already out; nobody is waiting on this.
PAGES_BACKFILL_WAIT_SECONDS = 900


def page_url(date: str) -> str:
    """Permalink for a dated edition. Always link the DATED url, never `/`."""
    return f"{PAGES_BASE_URL}/editions/{date}.html"


# ------------------------------------------------------------------- ledger

# editions/index.json is the authority for monotonic edition numbers and the
# idempotency gate. post_discord.py is its ONLY writer at runtime; everything
# here is read-only and never raises on a missing or corrupt file.

EMPTY_INDEX = {"volume": VOLUME, "editions": []}


def load_index(path: str | None = None) -> dict:
    """Read editions/index.json, or an empty ledger if it is missing/corrupt."""
    target = path or INDEX_PATH
    try:
        with open(target, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return dict(EMPTY_INDEX, editions=[])
    if not isinstance(data, dict) or not isinstance(data.get("editions"), list):
        return dict(EMPTY_INDEX, editions=[])
    return data


def next_edition_number(index: dict | None = None) -> int:
    """max(number) + 1 across the ledger. Computed, never guessed."""
    idx = index if index is not None else load_index()
    numbers = [
        e["number"]
        for e in idx.get("editions", [])
        if isinstance(e, dict) and isinstance(e.get("number"), int)
    ]
    return max(numbers) + 1 if numbers else 1


def edition_record(date: str, index: dict | None = None) -> dict | None:
    """The ledger record for a date, or None."""
    idx = index if index is not None else load_index()
    for entry in idx.get("editions", []):
        if isinstance(entry, dict) and entry.get("date") == date:
            return entry
    return None


def is_posted(date: str, index: dict | None = None) -> bool:
    """The idempotency gate: True once a date has been delivered."""
    record = edition_record(date, index)
    return bool(record and record.get("posted"))


# -------------------------------------------------------------------- stdio


def use_utf8_stdio() -> None:
    """Make stdout/stderr survive em dashes on a cp1252 Windows console.

    Every CLI here should call this first: a UnicodeEncodeError while
    PRINTING would fail a run that actually succeeded, and Nate's manual
    fallback runs happen on Windows.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
