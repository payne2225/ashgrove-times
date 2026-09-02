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

# The paper lands ahead of Jim Claudtore's 7:15 file, so the edition
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
# 5:30 rather than 6:00 since 2026-08-14: the routine now researches and
# builds TWO papers in the head start, the Times and Sports & Sportsman, so
# that both can be posted the moment their hold expires. Measured research
# for the Times alone was 37 minutes; ninety minutes covers both without
# either being rushed.
POST_CRON_UTC = "30 9 * * *"            # daylight time (Mar-Nov) -> 5:30 AM EDT
POST_CRON_UTC_STANDARD = "30 10 * * *"  # standard time (Nov-Mar) -> 5:30 AM EST

# THE MORNING SEQUENCE. Nate, 2026-08-14: the Times first, then Sports, then
# the weather — in that order, in succession.
#
# The order is achieved by STAGGERED HOLDS rather than by chaining, and that
# is deliberate. Jim Claudtore runs from his own repo on his own routine and
# is the post people actually dress by; making him wait on the newspaper
# finishing would turn every newspaper hang into a missing forecast. The two
# papers share a repo and a routine, so their order is guaranteed by
# construction; the forecast keeps its independence and simply follows.
#
# Both editions are researched BEFORE either is posted, so the gap between
# them is a delivery gap, not a research gap.
POST_TARGET_ET = "07:00"          # The Ashgrove Times
SPORTSMAN_TARGET_ET = "07:05"     # Sports & Sportsman, five minutes later
WEATHER_TIME_ET_SEQUENCE = "7:15" # Jim Claudtore, unchanged and uncoupled
WEATHER_BOT = "Jim Claudtore"
WEATHER_TIME_ET = "7:15"

WEATHER_EAR_MAX_CHARS = 90

# A pool, not a string: an ear that reads identically every morning stops
# being a pointer and becomes furniture. Every line names the 7:15 slot,
# which is the only part the reader actually needs — and NO line states the
# gap in minutes, because the gap depends on which cron is installed and
# whether the clocks have changed. Name the time, never the interval.
WEATHER_EAR_LINES = [
    "Jim Claudtore files the forecast at 7:15.",
    "Weather follows at 7:15 — Jim Claudtore has the day's sky.",
    "Look for the forecast at 7:15, from the weather desk.",
    "The weather desk reports at 7:15.",
    "Next edition of the sky: Jim Claudtore, 7:15.",
    "Forecast at 7:15 — read this, then dress for it.",
    "Jim Claudtore posts the outlook at 7:15.",
    "Jim Claudtore files at 7:15, after this edition.",
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
        "id": "scitech",
        "label": "Science & Technology",
        "emoji": "\U0001F52C",
        "color": _color("7C6640"),
        "order": 5,
        "standing": False,
        "trim_priority": 4,
    },
    # Added 2026-08-25 (Nate). Two standing sections the paper had been
    # covering by accident or not at all.
    #
    # British Columbia is Kirsten's. It was a single Away Desk sentence
    # sharing a sub-block with Wes's Vermont, which is not coverage of a
    # place somebody actually lives. It gets briefs like anywhere else, and
    # the Away Desk line for Prince George is retired so that no town is
    # covered twice on the same page.
    # Upgraded from "British Columbia" to a three-tier beat 2026-08-26
    # (Nate). One province was too narrow to fill honestly every morning and
    # too wide to be about anywhere in particular. National, provincial and
    # local each get their own block, so the section always has somewhere to
    # go and Kirsten's own city never gets crowded out by Vancouver.
    {
        "id": "bc",
        "label": "Canada",
        "emoji": "\U0001F341",
        "color": _color("6B3B2E"),
        "order": 4,
        "standing": True,
        "trim_priority": 6,
        "since": "2026-08-26",
    },
    # Artificial Intelligence, standing and top-level rather than a block
    # inside Science & Technology, because it had been quietly eating
    # Sci/Tech's slots — telescopes and medicine losing to model releases.
    # Both get their own room now.
    {
        "id": "ai",
        "label": "Artificial Intelligence",
        "emoji": "\U0001F916",
        "color": _color("3F4A5A"),
        "order": 6,
        "standing": True,
        "trim_priority": 5,
        "since": "2026-08-26",
    },
]

SECTION_IDS = [s["id"] for s in SECTIONS]

# The Canada section's three tiers, printed in this order: local first,
# because the section exists for somebody who lives in Prince George, and a
# national-first ordering would bury her city under Ottawa every morning.
# The West Virginia notebook makes the same choice in the other direction
# and for the same reason — it leads with the state because the readers are
# in it.
CANADA_TIERS = [
    {
        "tier": "prince_george",
        "label": "Prince George",
        "note": "the city itself and the surrounding north — Nechako, Fraser, "
                "the Cariboo, Lheidli T'enneh",
        "outlets": ["CKPG Today", "Prince George Citizen",
                    "CBC Daybreak North", "My PG Now"],
    },
    {
        "tier": "bc",
        "label": "British Columbia",
        "note": "the province: Victoria, the Interior, the coast, wildfire "
                "service, and Vancouver when it is genuinely provincial news",
        "outlets": ["CBC British Columbia", "Vancouver Sun", "CTV Vancouver",
                    "Global BC"],
    },
    {
        "tier": "canada",
        "label": "Across Canada",
        "note": "the country: Ottawa, the other provinces, national economy, "
                "anything a Canadian would call national news",
        "outlets": ["CBC News", "Global News", "CTV News", "The Globe and Mail",
                    "National Post"],
    },
]

CANADA_TIER_IDS = [t["tier"] for t in CANADA_TIERS]
_CANADA_TIERS_BY_ID = {t["tier"]: t for t in CANADA_TIERS}


def canada_tier(tier: str) -> dict:
    """A Canada-section tier by id. Raises KeyError on an unknown one."""
    try:
        return _CANADA_TIERS_BY_ID[tier]
    except KeyError:
        raise KeyError(
            f"unknown tier {tier!r}; known: {', '.join(CANADA_TIER_IDS)}"
        ) from None


# Every tier files, from this date. Dated forward one day so the desk reads
# the instructions before the gate closes, and so today's edition — written
# when the section was still one province — stays valid as what it was.
CANADA_TIERS_REQUIRED_FROM = "2026-08-27"

# Sections set BELOW the flowed wire columns, at the full measure, rather
# than inside them. West Virginia has always sat here — it is the local
# anchor and its boxed notebook is wide content. British Columbia joined it
# 2026-08-26 (Nate), and the pairing is the point: these are the two
# sections about places somebody in the group actually lives, so they read
# together at the foot of the page rather than B.C. being one more column
# of wire.
#
# It lives in config because it is the page's READING ORDER, and more than
# the renderer needs to know it — the Discord digest's table of contents
# lists sections in the order a reader will meet them on the page, and a
# contents list that disagrees with the page is worse than none.
ANCHOR_SECTION_IDS = ("wv", "bc")


def sections_in_reading_order(date: str | None = None) -> list[dict]:
    """Section metadata in the order the PAGE presents it, not config order."""
    live = sections_for(date)
    wires = [s for s in live if s["id"] not in ANCHOR_SECTION_IDS]
    anchors = [s for s in live if s["id"] in ANCHOR_SECTION_IDS]
    return wires + anchors

# Sections the Times used to carry. Nate retired Sports on 2026-08-15, the
# day Sports & Sportsman shipped — sport now has its own paper, and the
# freed budget goes to a fourth brief in each wire section. The metadata
# stays here so the eleven editions that legitimately carry a sports
# section keep validating and rendering; a retired id is legal in any
# edition dated on or before its retirement date and illegal after.
RETIRED_SECTIONS = {
    "sports": {
        "retired_after": "2026-08-15",
        "meta": {
            "id": "sports",
            "label": "Sports",
            "emoji": "🏆",
            "color": _color("6B5636"),
            "order": 4,
            "standing": True,
            "trim_priority": 1,
        },
    },
}


# A section that started mid-run carries `since`. Without it, adding
# British Columbia on 2026-08-25 would have made every edition back to
# 2026-08-05 invalid for not containing a section that did not exist when
# it was published. RETIRED_SECTIONS is the same idea pointing backwards.
SECTION_START_KEY = "since"


def sections_for(date: str | None) -> list[dict]:
    """The section contract as of a date — the archive keeps its shape."""
    live = [
        s for s in SECTIONS
        if not (date and s.get(SECTION_START_KEY)
                and date < s[SECTION_START_KEY])
    ]
    for retired in RETIRED_SECTIONS.values():
        if date and date <= retired["retired_after"]:
            live.append(retired["meta"])
    return sorted(live, key=lambda s: s["order"])

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
    """Display metadata for a section id, including retired ones.

    Retired sections resolve so the ARCHIVE keeps rendering — eleven
    editions legitimately carry a sports section. A truly unknown id is
    still a bug and still raises.
    """
    try:
        return _SECTIONS_BY_ID[sid]
    except KeyError:
        pass
    retired = RETIRED_SECTIONS.get(sid)
    if retired:
        return retired["meta"]
    raise KeyError(
        f"unknown section id {sid!r}; expected one of {SECTION_IDS} "
        f"or retired {sorted(RETIRED_SECTIONS)}"
    )


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

# A region that outgrew a one-sentence Away Desk line and was given its own
# home in the paper (Nate, 2026-08-25). It stays in REGIONS because the
# roster is still true — somebody still lives there and those are still the
# right outlets — but it no longer files a notebook line, because covering
# the same town twice on one page is worse than covering it once properly.
# The value is where the coverage went, and the validator prints it.
PROMOTED_REGION_IDS = {
    "prince_george": "the British Columbia section",
    "topsail": "the notebook's Vacation Hotspots block",
}

AWAY_REGION_IDS = [r["region_id"] for r in REGIONS
                   if r["is_away"] and r["region_id"] not in PROMOTED_REGION_IDS]

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
# Re-derived 2026-08-15 when Sports moved to its own paper: the freed 750
# went to the three wire sections, which now target FOUR briefs each
# (4 x ~245 = ~980). Same 5,600 total against the 5,800 the trimmer watches.
EMBED_BUDGET = {
    "lead": 900,
    "us": 1000,
    "world": 1000,
    "wv": 2600,
    "bc": 900,
    "scitech": 1000,
    "ai": 900,
    "chrome": 200,   # the closing footer: kicker + sources_note + weather ear
}

EMBED_BUDGET_TOTAL = sum(EMBED_BUDGET.values())

# What EMBED_BUDGET now means (2026-08-25). It used to be a DELIVERY budget:
# the paper went to Discord as embeds and Discord counts 6,000 characters a
# message, so every allocation above was really a share of that ceiling. The
# paper no longer posts that way — one digest message links the website — so
# these numbers stopped being a limit and became an EDITORIAL guide: roughly
# how long each section should run before it is out of proportion with the
# rest of the page.
#
# That is why the totals below are advisory in both directions. Nothing
# truncates an over-long section any more; a validator note is the entire
# consequence, and a genuinely big news day is allowed to run long.
EDITION_TARGET_CHARS = EMBED_BUDGET_TOTAL
EDITION_LONG_CHARS = int(EMBED_BUDGET_TOTAL * 1.3)


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
    "hotspots": "Vacation Hotspots",
}

# Retired from the News Desk 2026-08-25. "On the Water" carried gauge and
# tide READINGS — 179 cfs, high at 5:48 — which is instrument data, and the
# water has belonged to Sports & Sportsman since 2026-08-21. Printing it in
# both papers was the last of that overlap. The block keeps its place in
# the notebook and changes what it is FOR: news from the two places this
# crew actually goes, which is a thing no other section covers.
WV_RETIRED_SUBHEADS = {"fishing": "On the Water"}
WV_SUBHEADS_CHANGED_ON = "2026-08-26"


# Every sub-block label the notebook has ever had, live or retired. Code
# that RENDERS an archived edition looks up here; code that tells the desk
# what to WRITE uses wv_subheads_for(date). Iterating both "hotspots" and
# "fishing" and skipping the empty one costs nothing and means no renderer
# needs to know today's date to draw a 2026-08-10 page correctly.
WV_ALL_SUBHEAD_KEYS = ("regional", "away", "hotspots", "fishing")


def wv_subhead(key: str) -> str:
    """The label for any notebook sub-block, retired ones included."""
    if key in WV_SUBHEADS:
        return WV_SUBHEADS[key]
    if key in WV_RETIRED_SUBHEADS:
        return WV_RETIRED_SUBHEADS[key]
    raise KeyError(
        f"unknown notebook sub-block {key!r}; known: "
        f"{', '.join(WV_ALL_SUBHEAD_KEYS)}"
    )


def wv_subheads_for(date: str | None) -> dict:
    """The notebook's sub-blocks as of a date — the archive keeps its shape."""
    if date and date < WV_SUBHEADS_CHANGED_ON:
        out = {"regional": WV_SUBHEADS["regional"], "away": WV_SUBHEADS["away"]}
        out.update(WV_RETIRED_SUBHEADS)
        return out
    return dict(WV_SUBHEADS)


# The two places the crew leaves home for. NOT a fishing report and NOT a
# weather report — both of those have their own homes — but what is going
# ON in the town: a road closed, a festival, a pier reopening, a zoning
# fight, an ordinance, a business that mattered to somebody.
HOTSPOTS = [
    {
        "hotspot_id": "cabin",
        "place": "Webster County & Cowen",
        "towns": ["Cowen", "Webster Springs", "Camden-on-Gauley",
                  "Cherry River", "Summersville"],
        "outlets": ["The Webster Echo", "WV MetroNews", "The Register-Herald",
                    "Nicholas Chronicle"],
        "note": "the cabin. Summersville only when the story reaches Cowen — "
                "otherwise it belongs to the Nicholas & Webster regional line",
    },
    {
        "hotspot_id": "topsail",
        "place": "Topsail Island & the coast",
        "towns": ["Topsail Beach", "Surf City", "North Topsail Beach",
                  "Hampstead", "Sneads Ferry"],
        "outlets": ["WECT", "Wilmington StarNews", "The Pender-Topsail Post",
                    "WWAY", "Jacksonville Daily News"],
        "note": "the beach. Wilmington ONLY when the story is genuinely big — "
                "a port strike or a hurricane, not a restaurant opening",
    },
]

HOTSPOT_IDS = [h["hotspot_id"] for h in HOTSPOTS]
_HOTSPOTS_BY_ID = {h["hotspot_id"]: h for h in HOTSPOTS}


def hotspot_by_id(hid: str) -> dict:
    """A hotspot definition by id. Raises KeyError on an unknown id."""
    try:
        return _HOTSPOTS_BY_ID[hid]
    except KeyError:
        raise KeyError(
            f"unknown hotspot_id {hid!r}; known: {', '.join(HOTSPOT_IDS)}"
        ) from None


# One line each, same register as a regional line but allowed a little more
# room: these are places nobody in the group reads a local paper for, so the
# line has to carry enough context to land cold.
# These two blocks FILE EVERY MORNING (Nate, 2026-08-26, after both ran zero
# on their first day): "ALWAYS give us content. If it's a few days old
# that's fine, but there is always stuff to report. Always."
#
# This does not loosen the never-invent rule — it widens the window and the
# search, which is a different thing. A county and a barrier island always
# have something going on; a fourteen-day window plus the government bodies
# that meet on a schedule is what makes that reliably true. The validator
# refuses an empty block unless the edition carries a note naming what was
# actually searched, so it can never again go missing quietly.
NOTEBOOK_ALWAYS_FILLS = ("away", "hotspots")
NOTEBOOK_EMPTY_NOTE_KEYS = {"away": "away_note", "hotspots": "hotspots_note"}
NOTEBOOK_LOOKBACK_DAYS = 14

HOTSPOT_MAX = len(HOTSPOTS)
HOTSPOT_ITEM_TARGET_CHARS = 130
HOTSPOT_ITEM_MAX_CHARS = 170

# Raised 2026-08-25 (Nate: "the West Virginia section is pretty skimpy").
# Two statewide briefs and six notebook lines was never an editorial
# judgement — it was the Discord embed budget, which the paper no longer
# posts against. West Virginia is the reason this paper exists and it was
# the smallest thing on the page.
WV_BRIEFS_TARGET = 4      # statewide items
WV_BRIEFS_MAX = 6

# Regional and away entries are ONE SENTENCE — still. The ceiling went up
# with the budget (110 to 150) because 110 characters could not carry a
# story that needed a "because" clause, and the line came out reading like
# a headline with the news removed. It is NOT permission to write a brief
# here: a notebook line is a pointer, and a region with a real story to
# tell should be filing a statewide brief instead.
WV_ITEM_TARGET_CHARS = 150
WV_ITEM_MAX_CHARS = 190
WV_PLACE_MAX_CHARS = 48
WV_REGIONAL_MAX = len(WV_REGION_IDS)
WV_AWAY_MAX = len(AWAY_REGION_IDS)


def wv_away_max_for(date: str | None) -> int:
    """How many Away Desk lines an edition dated `date` may carry.

    Date-scoped, because the cap is the size of the away roster and the
    roster shrank: Prince George and Topsail were promoted out of the
    notebook on WV_SUBHEADS_CHANGED_ON, and an edition published before
    that legitimately carried all three. Found 2026-09-02 when the first
    contract tests were written — the 2026-08-05 edition had been failing
    today's validator on this rule since 2026-08-26, unnoticed, because
    nothing re-validated the archive. WV_AWAY_MAX stays as the live value
    for the code that tells the desk what to write today.
    """
    if date and date < WV_SUBHEADS_CHANGED_ON:
        return len(AWAY_REGION_IDS) + len(PROMOTED_REGION_IDS)
    return WV_AWAY_MAX

# Every region CAN file; on a normal morning about six lines total is what
# the WV allocation actually pays for. This is a target, never a gate — a
# real eighth item beats an artificial cap, and nothing may drop genuine
# news to hit a number.
WV_NOTEBOOK_LINES_TARGET = 9

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

# Topsail has no water-temperature station of its own, so the reading is
# borrowed and the line has to say whose it is. This block is the ONE place
# that identity lives: fetch_fishing.py fetches by it and validate_edition.py
# gates on it, so a station change is these five lines and nothing else.
#
# Changed 2026-08-24 (Nate): Wrightsville Beach (8658163) went dark. Not a
# hiccup — NOAA dropped `water_temperature` from the station's own product
# list, and the datagetter refuses `latest` and a 72-hour range alike. Six
# failures in one stretch and three more Aug. 22-24, all correctly omitted
# rather than guessed. Beaufort is farther than Wilmington (8658120, ~30 mi)
# but Wilmington is Cape Fear RIVER water at the state port and read 2F
# warmer the day they were compared; Beaufort is estuarine, which is the
# water the crew actually fishes. Distance and bearing are great-circle from
# their spot two nautical miles north of New Topsail Inlet.
TOPSAIL_TEMP_STATION_ID = "8656483"
TOPSAIL_TEMP_STATION_NAME = "Beaufort"  # what a printed line must credit
TOPSAIL_TEMP_STATION_LABEL = "Beaufort, Duke Marine Lab"  # NOAA's own name
TOPSAIL_TEMP_MILES = 60
TOPSAIL_TEMP_BEARING = "up the coast"

# The archive credits the station that was current WHEN IT WAS PRINTED.
# Editions through 2026-08-12 credit Wrightsville Beach, which was correct
# then; the first Beaufort line printed 2026-08-25. A validator that demands
# today's station of an August 5 line rewrites history, and it did — eight
# archived editions and editions/_fixture.json failed on exactly this until
# the contract tests caught it on 2026-09-02. The next station change adds a
# row here, and the gate keeps every printed line honest to its own day.
TOPSAIL_TEMP_STATION_CHANGED_ON = "2026-08-25"
TOPSAIL_TEMP_PRIOR_STATION_NAME = "Wrightsville Beach"


def topsail_temp_station_name_for(date: str | None) -> str:
    """The station a Topsail temperature line dated `date` must credit."""
    if date and date < TOPSAIL_TEMP_STATION_CHANGED_ON:
        return TOPSAIL_TEMP_PRIOR_STATION_NAME
    return TOPSAIL_TEMP_STATION_NAME

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

# A sports brief that reports a game carries `result` — winner, loser,
# score — from this date. Added after TWO reversed results in three days
# (2026-08-24 "18.5 clear of second-place Pittsburgh" when Pittsburgh was
# fourth and 18.5 back; 2026-08-26 "Pirates blanked 1-0 by the Padres" when
# Pittsburgh won the shutout). Both printed only real numbers, so every
# byte-match check passed them: what was wrong was the DIRECTION, and
# direction was living in a verb where nothing could check it.
#
# Dated forward one day so the desk reads the instructions before the gate
# closes, and so the archive stays valid as the paper it actually was.
SM_RESULT_REQUIRED_FROM = "2026-08-27"
SUMO_LEADS_SPORTS_IN_BASHO = True
SUMO_BASHO_DAYS = 15
SUMO_BASHO_MONTHS = [1, 3, 5, 7, 9, 11]
SUMO_KEYWORDS = (
    "sumo", "basho", "yokozuna", "ozeki", "sekiwake", "komusubi", "maegashira",
    "banzuke", "makuuchi", "juryo", "sekitori", "kyujo", "heya", "kachi-koshi",
    "make-koshi", "yusho", "honbasho", "rikishi", "oyakata", "dohyo",
)


# ---------------------------------------------------------------- artwork
#
# THE SKETCH ARTIST. Nate's idea, 2026-08-06: rather than republish a wire
# photograph, look at it and DRAW it — the way a courtroom artist works in a
# room where cameras are not allowed.
#
# That is not a workaround, it is the actual fix. An original drawing made
# after viewing a photograph is a new work; a halftoned copy of that
# photograph is the photograph. The source image is fetched, looked at, and
# discarded. It is never stored, never committed, never republished.
#
# The rules below are what keep that true MECHANICALLY rather than on
# trust. A drawing that has quietly become a traced or embedded photo fails
# them: raster payloads and external references are rejected outright, and
# an autotrace betrays itself by path count — a hand-drawn scene runs to
# dozens of paths, a traced photograph to thousands.
ART_ENABLED = True
ART_DIR_NAME = "art"
ART_MAX_BYTES = 60_000
ART_MAX_PATHS = 400          # ~4x a detailed hand drawing, ~1% of an autotrace
ART_MIN_ALT_CHARS = 40
ART_CAPTION_MAX_CHARS = 140
# The credit line must say BOTH that it is a drawing and what it was drawn
# from. "Sketched from an NPR photograph" is the shape.
ART_CREDIT_PREFIX = "Sketched from"
# Tags and attributes that would smuggle a bitmap back in.
ART_FORBIDDEN_TAGS = ("image", "foreignObject", "script", "iframe", "use")
ART_FORBIDDEN_PATTERNS = ("data:", "http://", "https://", "xlink:href")
# Nate, 2026-08-07: at least one drawing every day.
#
# The danger in a daily art quota is the same as a daily sumo quota — it
# pressures the paper to manufacture something on a day that has nothing.
# The way out is that "nothing to draw" is almost never true, because the
# paper already carries subjects that are drawable from ITS OWN measured
# data: the Williams River at this morning's gauge height, the Topsail
# sound at today's tide, a dohyo during a basho. Those are honest on the
# thinnest news day of the year.
#
# So the requirement stands, and the ladder below is what makes it keepable
# without inventing anything. A missing drawing is still never allowed to
# stop the paper — it is a loud note, not a failed edition.
ART_REQUIRED_DAILY = True
ART_MAX_PER_EDITION = 1

# Rungs, in order. The routine takes the highest one it can draw honestly.
ART_SUBJECT_LADDER = (
    "the lead story's own scene, if it is drawable under the rules",
    "any other story in today's paper with a drawable scene",
    "a standing subject drawn from today's measured data — the Williams "
    "River at its gauge height, the Topsail sound at today's tide",
    "a place or object central to a West Virginia story",
)


# WHERE THE DRAWING SITS. This was the flaw in the first version: art lived
# at `lead.art`, so it rendered under the lead headline no matter what it
# actually depicted — while the subject ladder explicitly allowed drawing
# something else. Readers got the Williams River captioned beneath a
# Saudi-Turkey-Pakistan defence pact, and a Michigan polling place beneath a
# story about tariff refunds.
#
# A drawing now declares what it illustrates and is rendered THERE. A river
# belongs in the Mountaineer State Notebook beside the fishing line; a
# rocket belongs in Science & Technology. Nothing sits under a headline it
# has nothing to do with.
ART_PLACEMENT_LEAD = "lead"


def art_placements() -> tuple[str, ...]:
    """Legal values for `art.placement`: the lead, or any section id."""
    return (ART_PLACEMENT_LEAD,) + tuple(s["id"] for s in SECTIONS)


def art_path(date: str, placement: str = ART_PLACEMENT_LEAD) -> str:
    """Repo-relative path for an edition's drawing.

    The placement is in the FILENAME so a stray file can never be silently
    attached to the wrong story.
    """
    return f"{ART_DIR_NAME}/{date}-{placement}.svg"


# English Premier League — requested in the channel on 2026-08-06 by a
# reader, with the shape specified: "emphasis on news from the teams we
# like, general from the rest of the league." Same discipline as sumo: a
# standing daily SEARCH in season, never a standing daily HEADLINE. Nothing
# may fail an edition for a missing football brief.
#
# Answered 2026-08-06. FIRST NAMES ONLY, per the rule at the top of this
# file — the Discord handles they gave are not recorded anywhere in this
# repo, because it is public.
#
# Chelsea carries two of the readership; every club here carries at least
# one. That is the emphasis order when a day has more football than room.
PREMIER_LEAGUE_REQUIRED_DAILY = False

# ============================== THE TEAMS ==============================
#
# THE ONE PLACE the paper records who the readers follow, across every
# sport. Nate, 2026-08-14: "let's start with these teams but have the
# ability to add more" — so adding one is a single line here and nothing
# else changes. The Premier League helpers below are DERIVED from this
# table rather than keeping their own copy, because two lists of the same
# clubs is exactly the drift this project has been bitten by before.
#
# `aliases` are what a headline actually says. A match report reads "Spurs
# hold Chelsea" or "the Bucs dropped two", never the formal club name, and
# a team the paper cannot recognise is a team it cannot prioritise.
#
# `supporters` is FIRST NAMES ONLY and may be empty: the Ohio Valley teams
# are followed by the group broadly rather than by one person. Where it is
# filled it decides emphasis when a day has more news than room.
#
# TO ADD A TEAM: copy a line. Nothing else.
# TWO NAMES IN HERE MEAN TWO DIFFERENT TEAMS, and both are load-bearing:
#
#   "Spurs" — Tottenham in football, San Antonio in basketball. Both are
#             followed, both are what headlines actually call them, and
#             neither alias can be deleted without losing real matches.
#   "Bucs"  — the Pirates here, but the Buccaneers to an NFL desk, and the
#             NFL is now in scope.
#
# `find_team(text, league=...)` is the resolution: pass the league you are
# reading and the collision disappears. Without a hint both candidates come
# back, which is correct — guessing would be worse. Do not "tidy" these by
# dropping an alias.
#
# "Reds" is Cincinnati, settled by Nate 2026-08-14. Liverpool keeps no
# colour alias at all rather than fight for it.
FOLLOWED_TEAMS = [
    # Ian is the HEAD COACH here (Nate, 2026-08-22), which makes Hannan the
    # only team on this list the paper has a man inside. Fixtures come from
    # his own schedule doc, mirrored at reference/hannan-soccer-2026.json;
    # results are printed only when an outside source has them.
    {"league": "Prep", "name": "Hannan",
     "aliases": ("Hannan High", "Golden Wave"), "supporters": ["Ian"]},

    {"league": "NCAA", "name": "West Virginia",
     "aliases": ("WVU", "Mountaineers"), "supporters": []},
    {"league": "NCAA", "name": "Marshall",
     "aliases": ("Thundering Herd", "the Herd"), "supporters": []},
    # NOT aliased to bare "Ohio": that substring also matches Ohio State,
    # which this paper does not follow and whose fans would notice.
    {"league": "NCAA", "name": "Ohio University",
     "aliases": ("Ohio Bobcats", "Bobcats"), "supporters": []},

    {"league": "Premier League", "name": "Chelsea",
     "aliases": ("the Blues",), "supporters": ["Trav", "Ian"]},
    {"league": "Premier League", "name": "Tottenham",
     "aliases": ("Spurs", "Tottenham Hotspur"), "supporters": ["Nate"]},
    {"league": "Premier League", "name": "Liverpool",
     "aliases": (), "supporters": ["Pat"]},

    {"league": "MLS", "name": "Columbus Crew",
     "aliases": ("the Crew",), "supporters": []},
    {"league": "MLS", "name": "FC Cincinnati",
     "aliases": ("FC Cincy", "Cincy"), "supporters": []},

    {"league": "MLB", "name": "Cincinnati Reds",
     "aliases": ("Reds",), "supporters": []},
    {"league": "MLB", "name": "Pittsburgh Pirates",
     "aliases": ("Pirates", "Bucs"), "supporters": []},

    {"league": "NBA", "name": "San Antonio Spurs",
     "aliases": ("Spurs", "San Antonio"), "supporters": []},

    {"league": "NFL", "name": "Cleveland Browns",
     "aliases": ("Browns",), "supporters": []},
    {"league": "NFL", "name": "Cincinnati Bengals",
     "aliases": ("Bengals",), "supporters": []},

    # National team, not a league — "Soccer" keeps it out of the Premier
    # League's per-league cap and search plan.
    {"league": "Soccer", "name": "USMNT",
     "aliases": ("U.S. men's national team", "US men's national team",
                 "United States men's national team"), "supporters": []},
]


def followed_teams(league: str | None = None) -> list[dict]:
    """Every followed team, or just one league's.

    Ordered by how many of the readership follow each, then by name — that
    is the tiebreak when a day has more team news than the section has room.
    """
    teams = [t for t in FOLLOWED_TEAMS
             if league is None or t["league"].lower() == league.lower()]
    return sorted(teams, key=lambda t: (-len(t.get("supporters") or []), t["name"]))


def followed_leagues() -> list[str]:
    """Leagues the paper follows, in the order they appear above."""
    seen: list[str] = []
    for team in FOLLOWED_TEAMS:
        if team["league"] not in seen:
            seen.append(team["league"])
    return seen


def team_names(team: dict) -> tuple[str, ...]:
    """Everything a headline might call this team: the name and its aliases."""
    return (team["name"],) + tuple(team.get("aliases") or ())


def find_team(text: str, league: str | None = None) -> list[dict]:
    """Followed teams named anywhere in `text`, by name OR alias.

    PASS THE LEAGUE when you know it. Two aliases in this table are real
    collisions — "Spurs" is Tottenham to a football desk and San Antonio to
    a basketball one, "Bucs" is the Pirates here and the Buccaneers to the
    NFL — and the league hint is what resolves them.

    Without a hint every candidate comes back. That is deliberate: a silent
    wrong guess would put a basketball result under a football club.
    """
    low = (text or "").lower()
    pool = [t for t in FOLLOWED_TEAMS
            if league is None or t["league"].lower() == league.lower()]
    return [t for t in pool if any(n.lower() in low for n in team_names(t))]


def ambiguous_aliases() -> dict[str, list[str]]:
    """Aliases that name more than one followed team, and who claims them.

    Exists so the collisions are discoverable rather than folklore — a
    reviewer can print this instead of rediscovering the Spurs problem.
    """
    seen: dict[str, list[str]] = {}
    for team in FOLLOWED_TEAMS:
        for name in team_names(team):
            seen.setdefault(name.lower(), []).append(
                f"{team['name']} ({team['league']})")
    return {alias: owners for alias, owners in seen.items() if len(owners) > 1}


# Derived, never hand-maintained — see the note above about two lists.
PREMIER_LEAGUE_SUPPORTERS = {
    t["name"]: list(t["supporters"])
    for t in FOLLOWED_TEAMS if t["league"] == "Premier League"
}
PREMIER_LEAGUE_FOLLOWED_CLUBS: list[str] = list(PREMIER_LEAGUE_SUPPORTERS)
# August through May. Confirm real fixture dates by search — the season's
# first and last matchweeks move year to year and this is only the envelope.
PREMIER_LEAGUE_MONTHS = [8, 9, 10, 11, 12, 1, 2, 3, 4, 5]
PREMIER_LEAGUE_KEYWORDS = (
    "premier league", "matchweek", "epl", "fixture", "clean sheet",
    "brace", "hat-trick", "xg", "relegation", "transfer window",
    "deadline day", "derby", "sacked", "on loan",
)

# Detection only — used to recognise that a brief IS about football, which
# jargon alone misses: a match report reads "Liverpool beat Arsenal 2-1"
# and contains none of the words above. Distinct from FOLLOWED_CLUBS, which
# is about whose news gets the emphasis.
#
# Short forms are deliberately omitted where they collide with ordinary
# English or with other sports — "United", "City", "Wolves", "Palace",
# "Forest", "Villa", "Brighton" — since a false positive here silences a
# real advisory. The full names below are unambiguous.
PREMIER_LEAGUE_CLUBS = (
    "arsenal", "aston villa", "bournemouth", "brentford",
    "brighton & hove albion", "brighton and hove albion", "burnley",
    "chelsea", "crystal palace", "everton", "fulham", "ipswich town",
    "leeds united", "leicester city", "liverpool", "manchester city",
    "manchester united", "man city", "man united", "man utd",
    "newcastle united", "nottingham forest", "sheffield united",
    "southampton", "sunderland", "tottenham", "spurs", "west ham",
    "wolverhampton",
)


def is_premier_league_season(month: int) -> bool:
    """True in a month the Premier League is normally playing."""
    return month in PREMIER_LEAGUE_MONTHS


def followed_clubs() -> list[str]:
    """The clubs the group actually supports, most-supported first.

    Empty would be a legitimate state, not a misconfiguration: it would mean
    general league coverage rather than an invented allegiance. It is not
    empty any more.
    """
    return sorted(PREMIER_LEAGUE_FOLLOWED_CLUBS,
                  key=lambda c: (-len(PREMIER_LEAGUE_SUPPORTERS.get(c, [])), c))


def club_supporters(club: str) -> list[str]:
    """First names of the readers who support a club, or [] if nobody does."""
    for name, people in PREMIER_LEAGUE_SUPPORTERS.items():
        if name.lower() == (club or "").lower():
            return list(people)
    return []


def is_house_derby(text: str) -> list[str]:
    """Followed clubs named in the same text — two or more means a derby.

    Tottenham, Chelsea and Liverpool all play each other twice a season, so
    several times a year one fixture is a result half this readership wanted
    and half did not. The paper covers it straight and names both, rather
    than reporting it from one side's point of view.
    """
    low = (text or "").lower()
    hits = [c for c in PREMIER_LEAGUE_FOLLOWED_CLUBS if c.lower() in low]
    if "Tottenham" in PREMIER_LEAGUE_FOLLOWED_CLUBS and "spurs" in low \
            and "Tottenham" not in hits:
        hits.append("Tottenham")
    return hits if len(hits) > 1 else []


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


def home_url() -> str:
    """The page the daily Discord post links, and the nav's Home button.

    home.html rather than the bare root: the root is a redirect stub, and a
    link that resolves in one hop unfurls in Discord without a round trip.
    """
    return f"{PAGES_BASE_URL}/home.html"


def page_url(date: str) -> str:
    """Permalink for a dated edition. Always link the DATED url, never `/`."""
    return f"{PAGES_BASE_URL}/editions/{date}.html"


def sportsman_page_url(date: str) -> str:
    """Permalink for a dated Sports & Sportsman edition."""
    return f"{PAGES_BASE_URL}/sportsman/{date}.html"


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


# =====================================================================
#                      SPORTS & SPORTSMAN
# =====================================================================
#
# A SECOND DAILY EDITION, posted to its own channel. Nate proposed it in
# the channel on 2026-08-14 and named it 2026-08-14: the paper's sports
# desk was only ever getting a couple of headlines, and the Topsail fishing
# report was making Jim Claudtore's briefing too long. Both problems have
# the same answer — give sport and the outdoors their own paper.
#
# It reuses this module, the renderer, the poster and the ledger discipline
# wholesale. What it does NOT share is the channel or the webhook.
SPORTSMAN_MASTHEAD = "SPORTS & SPORTSMAN"
SPORTSMAN_TAGLINE = "The Ashgrove Times"
SPORTSMAN_WEBHOOK_ENV = "DISCORD_SPORTSMAN_WEBHOOK_URL"

SPORTSMAN_SECTIONS = [
    {"id": "teams", "label": "Our Teams", "emoji": "\U0001F3DF",
     "order": 1, "standing": True, "trim_priority": 5,
     "note": "the followed teams, most-supported first. Never empty in season."},
    {"id": "leagues", "label": "Around the Leagues", "emoji": "\U0001F4F0",
     "order": 2, "standing": False, "trim_priority": 1,
     "note": "everything else worth knowing, capped per league so one "
             "does not eat the section"},
    {"id": "seasons", "label": "In Season", "emoji": "\U0001F343",
     "order": 3, "standing": True, "trim_priority": 4,
     "note": "what is coming in, at its prime, and going out"},
    {"id": "water", "label": "On the Water", "emoji": "\U0001F41F",
     "order": 4, "standing": True, "trim_priority": 5,
     "note": "gauges, what is biting, and what is working"},
]

# Stories per league in `leagues`, so one busy league cannot crowd out the
# rest. `teams` is not capped by this — a followed team always gets its say.
# Raised 2 -> 3 on 2026-08-17 after Nate called the sport half skimpy; an
# in-season league also earns a daily ROUNDUP brief (the day across MLB in
# one paragraph), which is reporting, not a scoreboard.
SPORTSMAN_MAX_PER_LEAGUE = 3

# The two standing blocks that keep Our Teams from running thin on a quiet
# day, added 2026-08-17. Standings and fixtures are INSTRUMENT READINGS,
# like the river gauges: always true, always current, never padding. A
# Monday with two games still answers "where do we stand and when do we
# play next" for every in-season team.
SPORTSMAN_STANDINGS_LABEL = "Where they stand"
SPORTSMAN_UPCOMING_LABEL = "The week ahead"

# ------------------------------------------------------------- the outdoors
#
# THE AGENCIES ARE THE ONLY AUTHORITY. Seasons, bag limits and size limits
# change every year, vary by zone and weapon, and are the one thing in this
# whole project where being wrong has consequences beyond embarrassment:
# somebody could hunt or keep a fish out of season on the paper's say-so.
#
# So this table holds STRUCTURE ONLY — which species the readers care about
# and which agency governs them. It deliberately holds NO DATES. The routine
# looks the current dates up every time it prints one, cites the agency, and
# links it. A season date in this file would be stale within a year and
# nobody would notice until it was wrong.
SPORTSMAN_AGENCIES = {
    "WV": {"name": "West Virginia DNR", "short": "WVDNR",
           "site": "wvdnr.gov",
           # Same expired certificate that keeps the trout-stocking list out
           # of fetch_fishing.py — the site cannot be fetched. Solved a
           # better way: Nate supplied the official pamphlet and page IV is
           # transcribed into the reference file below, which is the primary
           # source rather than a search result. IT EXPIRES — see
           # WV_SEASONS_VALID_THROUGH.
           "fetchable": False,
           "reference": "reference/wv-hunting-2026-27.json"},
    # NC SPLITS ITS COASTAL WATERS BETWEEN TWO AGENCIES and the crew fishes
    # on the side most people do not reach for. Topsail Sound is COASTAL
    # water, so red drum, speckled trout and flounder are governed by the
    # Division of Marine Fisheries — NOT by the NCWRC inland digest, whose
    # fishing sections are mountain trout and warmwater species. Quoting an
    # inland creel limit at a saltwater fish is a different agency's rule.
    # See reference/nc-waters-jurisdiction.md.
    "NC": {"name": "North Carolina Division of Marine Fisheries",
           "short": "NCDMF", "site": "deq.nc.gov",
           # Reachable, verified 2026-08-14 — which is exactly why NC needs
           # no transcribed file and West Virginia did.
           "fetchable": True,
           "governs": "coastal waters, including Topsail Sound",
           "reference": "reference/nc-waters-jurisdiction.md"},
    "NC_INLAND": {"name": "North Carolina Wildlife Resources Commission",
                  "short": "NCWRC", "site": "ncwildlife.gov",
                  "fetchable": True,
                  "governs": "inland waters, and licensing in joint waters",
                  "note": "NOT the source for Topsail limits"},
}

# What the crew actually hunts and fishes for, by state. Order is roughly
# the order the year runs.
# The licence year the transcribed WV table covers. On or after this date
# the reference file is DANGEROUS, not merely stale: seasons move annually
# and a hunter could act on a date that no longer holds. Anything printing a
# WV season date checks this first.
WV_SEASONS_REFERENCE = "reference/wv-hunting-2026-27.json"
WV_SEASONS_VALID_THROUGH = "2027-06-30"


def wv_seasons_current(date: str | None = None) -> bool:
    """False once the transcribed WV regulations have expired."""
    return (date or _today_iso()) <= WV_SEASONS_VALID_THROUGH


SPORTSMAN_SPECIES = {
    "WV": ("trout", "black bass", "walleye", "musky", "catfish", "crappie",
           "whitetail deer", "black bear", "wild turkey", "squirrel",
           "grouse", "waterfowl"),
    "NC": ("red drum", "speckled trout", "flounder", "bluefish", "king "
           "mackerel", "spanish mackerel", "cobia", "sheepshead"),
}

# The waters the paper reports on, tied to the gauges fetch_fishing.py
# already pulls. `structure` and `forage` are what a lure recommendation
# has to be grounded in — Pat asked for setups that work on THESE waters,
# not generic advice.
SPORTSMAN_WATERS = [
    {"key": "williams", "name": "Williams River", "near": "Cowen",
     "state": "WV", "kind": "freestone trout stream",
     "structure": "pocket water, plunge pools, undercut banks",
     "forage": "caddis, stoneflies, sculpin"},
    {"key": "ohio", "name": "Ohio River", "near": "R.C. Byrd Locks and Dam",
     "state": "WV", "kind": "big-river pool and tailwater",
     "structure": "wing dams, riprap, the lock wall, barge cuts",
     "forage": "shad, skipjack, crawfish"},
    {"key": "topsail", "name": "Topsail Sound", "near": "New Topsail Inlet",
     "state": "NC", "kind": "backwater sound and marsh",
     "structure": "oyster bars, grass edges, dock lights, the ICWW channel",
     "forage": "mud minnows, shrimp, finger mullet"},
]


def sportsman_section_by_id(section_id: str) -> dict:
    """Metadata for one Sports & Sportsman section. Raises on an unknown id."""
    for section in SPORTSMAN_SECTIONS:
        if section["id"] == section_id:
            return section
    raise KeyError(f"unknown Sports & Sportsman section: {section_id!r}")


def water_by_key(key: str) -> dict | None:
    """The water a fishing line is about, or None."""
    for water in SPORTSMAN_WATERS:
        if water["key"] == key:
            return water
    return None
