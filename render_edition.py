"""Render one edition JSON into the broadsheet HTML and the Discord hero card.

Two outputs, deliberately unequal in importance:

  site/editions/YYYY-MM-DD.html   the full paper, published to GitHub Pages.
                                  Fills templates/broadsheet.html - the only
                                  place the visual language lives.
  out/ashgrove-YYYY-MM-DD.png     a 1200x630 hero card drawn with Pillow and
                                  the vendored OFL fonts. Fully offline: no
                                  browser, no network, no system font, no
                                  system library beyond what Pillow's wheel
                                  already bundles.

The hero is 1.91:1 rather than a full page because Discord scales an attached
image to roughly 550px wide. A full broadsheet at that width puts body type at
about 10px - unreadable without a tap, and once the reader is tapping, the
hosted HTML beats a raster on every axis. So the card carries only what stays
legible small: masthead, rules, folio, the weather ear, the lead headline, a
drop-capped excerpt, the byline, and the stat strip.

The card is decoration. The embeds are the paper. Every failure in here is
therefore SOFT: render_hero_png returns False instead of raising, and main()
exits 2 - HTML written, no PNG - so the pipeline keeps going and post_discord
falls back to the committed masthead banner.

    python render_edition.py --date 2026-08-04
    python render_edition.py --fixture          # offline layout regression
    python render_edition.py --date ... --no-png

Exit codes: 0 both written, 2 HTML written but PNG failed (soft), 1 HTML
failed (hard).
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import traceback
from urllib.parse import urlsplit

import config

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(HERE, "templates", "broadsheet.html")
EDITIONS_DIR = os.path.join(HERE, "editions")
SITE_DIR = os.path.join(HERE, "site")
OUT_DIR = os.path.join(HERE, "out")

# The strip is compiled before the opening bell and may mix prior closes with
# 24h spot prices, so the standing note describes when the paper was made, not
# what each number is. Anything stronger would be a claim the data cannot back.
STATS_NOTE = "Market data compiled before the opening bell"
TOP_RIGHT = "Price: Free"
ARCHIVE_TEXT = "Back issues"
EAR_LABEL = "Weather"

# The notebook's four parts. NOTEBOOK_TITLE is only the fallback - the edition
# may carry its own `notebook_title`. The three sub-head labels come from
# config.WV_SUBHEADS so the broadsheet, the Discord embed and the validator
# all print the same words; the literals here are only a floor for a config
# that predates the constant.
NOTEBOOK_TITLE = getattr(config, "WV_NOTEBOOK_TITLE", "Mountaineer State Notebook")
_SUBHEADS = getattr(config, "WV_SUBHEADS", {}) or {}
REGIONAL_LABEL = _SUBHEADS.get("regional", "Around the State")
AWAY_LABEL = _SUBHEADS.get("away", "The Away Desk")
HOTSPOTS_LABEL = _SUBHEADS.get("hotspots", "Vacation Hotspots")
# Retired from this paper 2026-08-25, kept so archived pages still draw the
# block they were published with.
FISHING_LABEL = getattr(config, "WV_RETIRED_SUBHEADS", {}).get(
    "fishing", "On the Water")

MONTHS = ("January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December")
DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
        "Sunday")

_DATED_JSON = re.compile(r"^(\d{4}-\d{2}-\d{2})\.json$")
_BLOCK_RE = re.compile(r"<!--\{BLOCK:(\w+)\}-->(.*?)<!--\{/BLOCK:\1\}-->", re.S)
_TOKEN_RE = re.compile(r"\{\{(\w+)\}\}")


# --------------------------------------------------------------------------
# template plumbing
# --------------------------------------------------------------------------

def load_blocks(path: str = TEMPLATE_PATH) -> dict[str, str]:
    """Split the template into its named fragments."""
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    blocks = {name: body.strip("\n") for name, body in _BLOCK_RE.findall(raw)}
    if "PAGE" not in blocks:
        raise ValueError(f"{path} has no PAGE block")
    return blocks


def fill(template: str, values: dict[str, str]) -> str:
    """Substitute {{TOKEN}}s. An unknown token is a bug, not a blank."""
    def sub(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            raise KeyError(f"template token {{{{{key}}}}} has no value")
        return values[key]
    return _TOKEN_RE.sub(sub, template)


# --------------------------------------------------------------------------
# text hygiene - content comes from web search, so assume hostile
# --------------------------------------------------------------------------

def esc(text: object) -> str:
    """Escape for HTML text and attributes alike."""
    return html.escape(_norm(text), quote=True)


def _norm(text: object) -> str:
    return re.sub(r"\s+", " ", str(text if text is not None else "")).strip()


def safe_url(url: object) -> str | None:
    """Allow only http(s) links through - never javascript:, data:, file:."""
    candidate = _norm(url)
    if not candidate:
        return None
    parts = urlsplit(candidate)
    if parts.scheme.lower() not in ("http", "https") or not parts.netloc:
        return None
    return candidate


def long_date(iso: str) -> str:
    day = dt.date.fromisoformat(iso)
    return f"{DAYS[day.weekday()]}, {MONTHS[day.month - 1]} {day.day}, {day.year}"


def _section_label(section: dict) -> str:
    """Display metadata lives in config; the JSON label is only a fallback."""
    meta = config.section_by_id(section.get("id", "")) or {}
    return meta.get("label") or section.get("label") or section.get("id", "")


def _people_phrase(people: object) -> str:
    """["Trav", "Justin", "Nate"] -> "Trav, Justin and Nate"."""
    names = [_norm(p) for p in (people or []) if _norm(p)]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return f"{', '.join(names[:-1])} and {names[-1]}"


def _region_meta() -> dict[str, dict]:
    """region_id -> its definition in config.REGIONS, keyed for enrichment.

    config.REGIONS is the shared source of truth for place names, who lives
    there, and the order the roundup runs in; the edition JSON may repeat any
    of it but never has to. Read through getattr so a renderer still works
    against a config that predates the constant.
    """
    meta: dict[str, dict] = {}
    for index, region in enumerate(getattr(config, "REGIONS", ()) or ()):
        if not isinstance(region, dict):
            continue
        region_id = _norm(region.get("region_id") or region.get("id"))
        if region_id:
            meta[region_id] = dict(region, _order=index)
    return meta


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

# ------------------------------------------------- family banner and nav

# The section names, settled by Nate 2026-08-21. The WHOLE publication is
# The Ashgrove Times — every page carries that as a banner above its own
# section masthead. "News desk" is the standard two-word form.
FAMILY_NAME = "The Ashgrove Times"
NEWSDESK_NAME = "THE NEWS DESK"
WEATHER_NAME = "THE WEATHER CLAUDE"

_NAV_TARGETS = (
    # home.html, not index.html: the button has said Home since 2026-08-21
    # and as of 2026-08-25 so does the page and the url. site/index.html is
    # a redirect kept only so a bare / still resolves.
    ("newsstand", "Home", "home.html"),
    ("news", "The News Desk", "today.html"),
    ("sportsman", "Sports &amp; Sportsman", "sportsman/"),
    ("weather", "The Weather Claude", "weather/"),
)


def _family_line() -> str:
    return f'<div class="family-line">{esc(FAMILY_NAME)}</div>'


def _nav_html(current: str, root: str, foot: bool = False) -> str:
    """Buttons to every other section plus Home.

    `root` is the relative path back to the site root, exactly as
    render_html already uses it — "" from a root-level page, "../" from a
    dated page one directory down.

    Every page carries the same buttons TWICE, under the masthead and again
    at the very bottom (Nate, 2026-08-24). A reader finishes a page at the
    bottom, which is exactly where the decision to read the next section
    gets made; sending them back up to the masthead to act on it is the
    kind of small friction that ends a reading session. The foot copy is
    the same links in the same order — a reader who learned the row at the
    top should not have to re-read it at the bottom.
    """
    buttons = [
        f'<a href="{root}{href}">{label}</a>'
        for key, label, href in _NAV_TARGETS if key != current
    ]
    classes = "paper-nav paper-nav-foot" if foot else "paper-nav"
    label = ' aria-label="Sections, repeated"' if foot else ' aria-label="Sections"'
    return f'<nav class="{classes}"{label}>' + "".join(buttons) + "</nav>"


def _tide_table_html(date_iso: str | None = None) -> str:
    """Today's full tide cycle as a real table, straight from the fetcher.

    Reads out/fishing.json rather than the edition: the table is instrument
    data, the same standing as the gauges, and going through the fetcher's
    own file means no hand can mistype a tide. Absent or tide-less data
    renders nothing — a missing table beats a stale one.

    THE DATE IS CHECKED, since 2026-08-26. This function reads a live file
    while every other part of the page comes from the edition JSON, so
    re-rendering a page with an old fishing.json silently typesets the wrong
    day's tides into it — which is exactly what happened when the
    2026-08-26 sports page was re-rendered to correct a headline and went
    out carrying 2026-08-21's tide times. Nothing else on the page could
    have revealed it. A mismatched file now renders no table at all, and
    says so on stderr rather than quietly.
    """
    try:
        with open(os.path.join(OUT_DIR, "fishing.json"), encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return ""
    fetched = data.get("date") or (data.get("generated_at") or "")[:10]
    if date_iso and fetched and fetched != date_iso:
        print(
            f"WARN: out/fishing.json is dated {fetched} but this page is "
            f"{date_iso} — tide table omitted rather than printing the wrong "
            "day's water; re-run fetch_fishing.py",
            file=sys.stderr,
        )
        return ""
    tides = (data.get("topsail") or {}).get("tides") or []
    rows = []
    for station in tides:
        events = station.get("events") or []
        if len(events) < 4:
            continue
        side = "Sound (where you fish)" if station.get("side") == "sound" \
            else "Ocean (surf)"
        cells = "".join(
            f"<td>{esc(e.get('time_local'))}<br>"
            f"{esc(e.get('height_ft'))} ft</td>" for e in events[:4])
        rows.append(f"<tr><td>{esc(side)}</td>{cells}</tr>")
    if not rows:
        return ""
    heads = "".join(
        f"<th>{esc(e.get('type', '').title())}</th>"
        for e in (tides[0].get("events") or [])[:4])
    return (
        '<table class="tide-table">'
        "<caption>Topsail tides — the full day</caption>"
        f"<tr><th>Water</th>{heads}</tr>" + "".join(rows) + "</table>")


def render_html(edition: dict, root: str = "../") -> str:
    """Fill the broadsheet template for one edition.

    `root` is the relative path back to the site root, so the same renderer
    produces both site/editions/<date>.html ("../") and the site/index.html
    copy that makes "/" a stable today's-paper bookmark ("").
    """
    blocks = load_blocks()
    lead = edition.get("lead") or {}
    date_iso = edition["edition_date"]
    dateline = long_date(date_iso)
    headline = _norm(lead.get("headline"))

    dek = _norm(lead.get("dek"))
    dek_html = fill(blocks["DEK"], {"DEK": esc(dek)}) if dek else ""

    ear = _norm(edition.get("weather_ear"))
    ear_html = fill(blocks["WEATHER_EAR"], {
        "EAR_LABEL": esc(EAR_LABEL),
        "EAR": esc(ear),
    }) if ear else ""

    description = f"{headline} {dek}".strip() or config.TAGLINE
    lead_art = _art_html(blocks, _art_for(edition, config.ART_PLACEMENT_LEAD))
    sections_html, wire_count = _sections_html(
        blocks, edition.get("sections") or [], edition)

    values = {
        "PAGE_CLASS": "",
        "PAGE_TITLE": esc(f"{config.MASTHEAD} — {dateline}"),
        "META_DESCRIPTION": esc(description[:300]),
        "FAMILY_LINE": _family_line(),
        "NAV": _nav_html("news", root),
        "NAV_FOOT": _nav_html("news", root, foot=True),
        "MASTHEAD": esc(NEWSDESK_NAME),
        "TAGLINE": esc(config.TAGLINE),
        "TOP_LEFT": esc(folio_left(edition)),
        "TOP_MID": esc(dateline),
        "TOP_RIGHT": esc(TOP_RIGHT),
        "WEATHER_EAR": ear_html,
        "LEAD_HEADLINE": esc(headline),
        "LEAD_DEK": dek_html,
        "LEAD_BYLINE": esc(f"By {lead.get('byline') or config.BYLINE}"),
        "LEAD_ART": lead_art,
        "LEAD_BLOCK_CLASS": _lead_block_class(lead_art),
        "LEAD_BODY": _lead_body_html(blocks, lead.get("body") or []),
        "STAT_STRIP": _stat_strip_html(blocks, lead.get("stat_strip") or []),
        "SECTIONS": sections_html,
        "SECTIONS_STYLE": _sections_style(wire_count),
        "KICKER": _kicker_html(blocks, edition.get("kicker")),
        "SOURCES_NOTE": esc(edition.get("sources_note")
                            or "Compiled from wire reports"),
        "ARCHIVE_LINK": fill(blocks["ARCHIVE_LINK"], {
            "HREF": esc(f"{root}archive.html"),
            "TEXT": esc(ARCHIVE_TEXT),
        }),
    }
    return fill(blocks["PAGE"], values) + "\n"


def folio_left(edition: dict) -> str:
    return f"Vol. {edition.get('volume') or 'I'} — No. {edition.get('edition_number', '')}".strip()


def _art_for(edition: dict, placement: str) -> dict | None:
    """The edition's drawing, but only if it belongs in `placement`.

    A drawing declares what it illustrates. Rendering it anywhere else is
    the bug this function exists to prevent: art used to hang off the lead
    unconditionally, so a river drawn from a gauge reading appeared under a
    foreign-policy headline as though it illustrated it.
    """
    art = edition.get("art")
    if not isinstance(art, dict):
        return None
    if (art.get("placement") or config.ART_PLACEMENT_LEAD) != placement:
        return None
    return art


def _lead_block_class(lead_art: str) -> str:
    """Classes for the lead block, which layout depends on entirely.

    At desktop widths the block is a two-column grid — drawing at roughly a
    third of the measure, story beside it. With no drawing the story became
    the FIRST grid child and inherited that narrow column, leaving three
    quarters of a 1,420px page empty beside eight lines of type. It read
    fine on a phone, where the grid does not apply, which is why it went a
    while unnoticed (Pat, 2026-08-24: "there is a ton of white space").

    Art placement is an editorial choice made fresh every morning — the
    2026-08-24 drawing went to Science & Technology — so "no drawing today"
    is a normal day, not an edge case, and the page has to be correct on it.
    """
    return "lead-block with-art" if lead_art.strip() else "lead-block no-art"


def _art_html(blocks: dict[str, str], art: object) -> str:
    """Inline the day's drawing, or nothing at all on the days there is none.

    The SVG is inlined rather than linked so the page stays self-contained
    and so the marks inherit `currentColor` — that is what makes the drawing
    read as ink on the paper instead of an image pasted onto it.

    Inlined markup is NOT escaped, which would normally be a hole. It is
    safe here for one reason: validate_edition.py has already refused any
    file containing <script>, <foreignObject>, <use>, href/src, or a data:
    payload, and the pipeline will not render an edition that failed
    validation. If that check is ever weakened, this becomes an injection
    point — they are load-bearing for each other.
    """
    if not isinstance(art, dict):
        return ""
    name = os.path.basename(str(art.get("file") or ""))
    if not name:
        return ""
    path = os.path.join(config.PROJECT_ROOT, config.ART_DIR_NAME, name)
    try:
        svg = open(path, encoding="utf-8").read().strip()
    except OSError:
        return ""
    # Drop any XML prolog; this is being inlined into HTML, not served.
    if svg.startswith("<?xml"):
        svg = svg[svg.index("?>") + 2:].lstrip()
    return fill(blocks["ART"], {
        "ART_SVG": svg,
        "ART_CAPTION": esc(str(art.get("caption") or "")),
        "ART_CREDIT": esc(str(art.get("credit") or "")),
    })


def _lead_body_html(blocks: dict[str, str], paragraphs: list) -> str:
    """Lead paragraphs, the first one drop-capped.

    The cap is an explicit span rather than ::first-letter so it renders the
    same in the email-grade engines some phones still use for previews.
    """
    body = [_norm(p) for p in paragraphs]
    body = [p for p in body if p]
    if not body:
        return ""
    first, rest = body[0], body[1:]
    out = [fill(blocks["DROP_PARA"], {
        "FIRST_LETTER": esc(first[0]),
        "REST": esc(first[1:]),
    })]
    out += [f"<p>{esc(p)}</p>" for p in rest]
    return "".join(out)


def _stat_strip_html(blocks: dict[str, str], entries: list) -> str:
    if not entries:
        return ""
    cells = []
    for entry in entries:
        direction = _norm(entry.get("direction")).lower()
        arrow = ""
        if direction in ("up", "down", "flat"):
            arrow = fill(blocks["ARROW"], {"DIRECTION": direction})
        cells.append(fill(blocks["STAT_CELL"], {
            "LABEL": esc(entry.get("label")),
            "VALUE": esc(entry.get("value")),
            "ARROW": arrow,
            "CHANGE": esc(entry.get("change")),
        }))
    return fill(blocks["STAT_STRIP"], {
        "STAT_CELLS": "".join(cells),
        "STATS_NOTE": esc(STATS_NOTE),
    })


# Which sections sit below the flow rather than in it. Defined in config,
# because the Discord digest lists sections in the order a reader meets them
# on the page and must not drift from this.
ANCHOR_SECTION_IDS = config.ANCHOR_SECTION_IDS


def wire_flow(sections: list[str]) -> str:
    """Wrap the wire sections in the container their copy flows through.

    The West Virginia notebook is deliberately NOT in here. It is the one
    section that spans the full measure, and a spanning element inside a
    multi-column flow splits it — which is what made the grid the right
    answer the first time this page was laid out. Kept outside, as a
    sibling block below the flow, both work.
    """
    return ('<div class="wire-flow">' + "\n  "
            + ("\n\n  ").join(sections)
            + "\n  </div>")


def _sections_style(wire_count: int) -> str:
    """Tell the stylesheet how many wire columns there actually are.

    The desktop grid was written `repeat(4, 1fr)` for "the four beats", but
    only THREE of config.SECTIONS are wire sections — West Virginia is the
    fourth and it spans the whole measure on its own row. The grid therefore
    always carried one empty track, which at 1,600px is a quarter of the
    front page standing blank from the section labels down to the notebook,
    on every desktop edition since the layout was written (Pat, 2026-08-24).

    Counted from what RENDERED, not from config: a section with no briefs
    renders nothing, and on that morning the page should close up to two
    columns rather than hold a gap open for news that does not exist.
    """
    # The wire sections FLOW through these columns rather than being placed
    # in a grid (2026-08-26). The grid put each section in its own cell and
    # made every row as tall as its tallest member, so on 2026-08-26's paper
    # — U.S. 524px, World 637px, Sci/Tech 901px — 28% of the section area
    # was white, and the second row was worse. Flowing means copy runs down
    # column one and continues into column two, the browser evens the
    # bottoms, and no arrangement of uneven sections can leave a hole.
    # Measured on that same edition: the section block went 1917px -> 999px
    # and the page 3093px -> 2653px, with nothing added or removed.
    #
    # Sports & Sportsman has laid out this way since it launched, which is
    # why that page never had this problem. The original objection to it
    # here — that `column-span: all` splits a flow and strands columns — is
    # answered by keeping the notebook OUT of the flow entirely: it is a
    # sibling block below, not a spanning child.
    count = max(1, wire_count)
    cols = 1 if count == 1 else (2 if count == 2 else 3)
    return f' style="--wire-cols: {cols}"'


def _sections_html(blocks: dict[str, str], sections: list, edition: dict) -> tuple[str, int]:
    by_id = {s.get("id"): s for s in sections}
    ordered = [by_id[m["id"]] for m in config.SECTIONS if m["id"] in by_id]
    ordered += [s for s in sections if s.get("id") not in
                {m["id"] for m in config.SECTIONS}]

    wires: list[str] = []
    anchors: list[str] = []
    for section in ordered:
        sid = section.get("id")
        rendered = (_wv_section_html(blocks, section, edition) if sid == "wv"
                    else _wire_section_html(
                        blocks, section, edition,
                        anchor=sid in ANCHOR_SECTION_IDS))
        if not rendered:
            continue
        (anchors if sid in ANCHOR_SECTION_IDS else wires).append(rendered)
    wire = len(wires)

    out: list[str] = []
    if wires:
        out.append(wire_flow(wires))
        if anchors:
            # The wire columns end on a ragged edge, and without a rule the
            # notebook reads as one more thing the last column ran into
            # (Nate, 2026-08-26). This is the only horizontal rule inside
            # the page body; the masthead's pair is chrome.
            out.append('<hr class="rule-anchor">')
    out += anchors
    return ("\n\n  ".join(out), wire)


def _wire_section_html(blocks: dict[str, str], section: dict, edition: dict,
                       anchor: bool = False) -> str:
    """A wire section. `anchor` places it below the flow at full measure.

    An anchored section is the same markup with one extra class, so its
    briefs can run across the page in their own columns rather than down a
    single 417px one — a full-measure section set in one column would run
    85-character lines, which is the opposite of the problem being solved.
    """
    briefs = [_brief_html(blocks, b) for b in (section.get("briefs") or [])]
    briefs = [b for b in briefs if b]
    if not briefs:
        return ""
    html = fill(blocks["SECTION"], {
        "SECTION_LABEL": esc(_section_label(section)),
        "BRIEFS": _art_html(blocks, _art_for(edition, section.get("id", ""))) + "".join(briefs),
    })
    if anchor:
        html = html.replace('class="sec sec-wire"',
                            'class="sec sec-wire sec-anchor"', 1)
    return html


def _wv_section_html(blocks: dict[str, str], section: dict, edition: dict) -> str:
    """West Virginia in the box, four parts, none of them required.

    The notebook is the paper's local anchor, so it never takes the two-column
    brief layout the wire sections use. Regional and away lines are single
    sentences and the fishing report closes the box.
    """
    briefs = [_brief_html(blocks, b) for b in (section.get("briefs") or [])]
    briefs = [b for b in briefs if b]
    regional = _roundup_html(blocks, section.get("regional"),
                             REGIONAL_LABEL, "wv-regional")
    away = _roundup_html(blocks, section.get("away"), AWAY_LABEL, "wv-away")
    # The block that closes the box. Since 2026-08-25 it is Vacation
    # Hotspots — news from Cowen and Topsail — and before that it was the
    # water report. An edition has one or the other, never both, so this
    # renders whichever it was published with and no page needs to know
    # today's date to draw an old one correctly.
    closing = (_hotspots_html(blocks, section.get("hotspots"))
               or _fishing_html(blocks, section.get("fishing")))
    if not (briefs or regional or away or closing):
        return ""
    return fill(blocks["WV_SECTION"], {
        "SECTION_LABEL": esc(_section_label(section)),
        "ART": _art_html(blocks, _art_for(edition, "wv")),
        "NOTEBOOK_TITLE": esc(section.get("notebook_title") or NOTEBOOK_TITLE),
        "BRIEFS": "".join(briefs),
        "REGIONAL": regional,
        "AWAY": away,
        "CLOSING_BLOCK": closing,
    })


def _roundup_html(blocks: dict[str, str], entries: object, label: str,
                  block_class: str) -> str:
    """One line per region that actually had news. A thin day renders nothing.

    Rows sort into config.REGIONS order so the roundup reads the same way every
    morning; anything the constant does not know keeps its position in the JSON.
    """
    meta = _region_meta()
    rows: list[tuple[int, str]] = []
    for entry in (entries or []):
        if not isinstance(entry, dict):
            continue
        item = _norm(entry.get("item"))
        if not item:
            continue
        definition = meta.get(_norm(entry.get("region_id")), {})
        place = _norm(entry.get("place")) or _norm(definition.get("place"))
        people = _people_phrase(entry.get("people") or definition.get("people"))
        if place:
            dateline = fill(blocks["ROUNDUP_DATELINE"], {
                "PLACE": esc(place),
                "PEOPLE": (fill(blocks["ROUNDUP_PEOPLE"], {"PEOPLE": esc(people)})
                           if people else ""),
            })
        else:
            dateline = ""
        rows.append((definition.get("_order", 10_000), fill(blocks["ROUNDUP_ITEM"], {
            "DATELINE": dateline,
            "ITEM": esc(item),
            "SOURCE": _source_html(blocks, entry),
        })))
    if not rows:
        return ""
    rows.sort(key=lambda row: row[0])
    return fill(blocks["WV_BLOCK"], {
        "BLOCK_CLASS": esc(block_class),
        "BLOCK_LABEL": esc(label),
        "ITEMS": "".join(row[1] for row in rows),
    })


def _hotspots_html(blocks: dict[str, str], entries: object) -> str:
    """Cowen and Topsail — the two places this crew goes. News, not water.

    Rows sort into config.HOTSPOTS order so the block reads the same way
    every morning. There is no `people` tag: nobody lives in these towns,
    which is the whole reason the block is called what it is called.
    """
    order = {h["hotspot_id"]: i for i, h in enumerate(config.HOTSPOTS)}
    rows: list[tuple[int, str]] = []
    for entry in (entries or []):
        if not isinstance(entry, dict):
            continue
        item = _norm(entry.get("item"))
        place = _norm(entry.get("place"))
        if not (item and place):
            continue
        rows.append((
            order.get(entry.get("hotspot_id"), len(order)),
            fill(blocks["ROUNDUP_ITEM"], {
                "DATELINE": fill(blocks["ROUNDUP_DATELINE"], {
                    "PLACE": esc(place),
                    "PEOPLE": "",
                }),
                "ITEM": esc(item),
                "SOURCE": _source_html(blocks, entry),
            }),
        ))
    if not rows:
        return ""
    rows.sort(key=lambda row: row[0])
    return fill(blocks["WV_BLOCK"], {
        "BLOCK_CLASS": esc("wv-hotspots"),
        "BLOCK_LABEL": esc(HOTSPOTS_LABEL),
        "ITEMS": "".join(html for _, html in rows),
    })


def _fishing_html(blocks: dict[str, str], entries: object) -> str:
    """Williams River and Topsail. A water with no reading is simply absent."""
    items = []
    for entry in (entries or []):
        if not isinstance(entry, dict):
            continue
        line = _norm(entry.get("line"))
        water = _norm(entry.get("water"))
        if not (line and water):
            continue
        items.append(fill(blocks["FISHING_ITEM"], {
            "WATER": esc(water),
            "LINE": esc(line),
            "SOURCE": _source_html(blocks, entry),
        }))
    if not items:
        return ""
    return fill(blocks["WV_BLOCK"], {
        "BLOCK_CLASS": esc("wv-fishing"),
        "BLOCK_LABEL": esc(FISHING_LABEL),
        "ITEMS": "".join(items),
    })


def _source_html(blocks: dict[str, str], entry: dict) -> str:
    source = _norm(entry.get("source"))
    if not source:
        return ""
    url = safe_url(entry.get("url"))
    if url:
        return fill(blocks["SOURCE_LINK"],
                    {"URL": esc(url), "SOURCE": esc(source)})
    return fill(blocks["SOURCE_PLAIN"], {"SOURCE": esc(source)})


def _brief_html(blocks: dict[str, str], brief: dict) -> str:
    headline = _norm(brief.get("headline"))
    if not headline:
        return ""
    return fill(blocks["BRIEF"], {
        "HEADLINE": esc(headline),
        "SUMMARY": esc(brief.get("summary")),
        "SOURCE": _source_html(blocks, brief),
    })


def _kicker_html(blocks: dict[str, str], kicker: object) -> str:
    text = _norm(kicker)
    return fill(blocks["KICKER"], {"KICKER": esc(text)}) if text else ""


# --------------------------------------------------------------------------
# archive + index
# --------------------------------------------------------------------------

def archive_entries(editions_dir: str | None = None,
                    site_dir: str | None = None) -> list[dict]:
    """Every dated edition JSON that has a rendered page, newest first.

    Reads the committed archive rather than editions/index.json so a back
    issue still lists even if the ledger write failed, and skips any edition
    whose page is missing so the archive never links to a 404.
    """
    editions_dir = editions_dir or EDITIONS_DIR
    site_dir = site_dir or SITE_DIR
    entries = []
    for name in sorted(os.listdir(editions_dir), reverse=True):
        match = _DATED_JSON.match(name)
        if not match:
            continue
        date_iso = match.group(1)
        if not os.path.exists(os.path.join(site_dir, "editions", f"{date_iso}.html")):
            continue
        try:
            with open(os.path.join(editions_dir, name), encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError):
            continue
        entries.append({
            "date": date_iso,
            "number": data.get("edition_number"),
            "volume": data.get("volume") or "I",
            "headline": _norm((data.get("lead") or {}).get("headline")),
        })
    return entries


def render_archive_html(entries: list[dict]) -> str:
    """The back-issue index at site/archive.html."""
    blocks = load_blocks()
    page_style = _extract_style(blocks["PAGE"])

    rows = []
    for entry in entries:
        number = entry.get("number")
        label = f"No. {number} · {long_date(entry['date'])}" if number \
            else long_date(entry["date"])
        rows.append(fill(blocks["ARCHIVE_ROW"], {
            "NUMBER": esc(label),
            "HREF": esc(f"editions/{entry['date']}.html"),
            "HEADLINE": esc(entry["headline"] or "Edition"),
        }))
    issues = "\n    ".join(rows) if rows else blocks["ARCHIVE_EMPTY"]

    newest = entries[0]["date"] if entries else None
    return fill(blocks["ARCHIVE_PAGE"], {
        "PAGE_TITLE": esc(f"{config.MASTHEAD} — Back issues"),
        "META_DESCRIPTION": esc(f"Back issues of {config.MASTHEAD}."),
        "STYLE": page_style,
        "MASTHEAD": esc(config.MASTHEAD),
        "TAGLINE": esc(config.TAGLINE),
        "TOP_LEFT": esc(ARCHIVE_TEXT),
        "TOP_MID": esc(long_date(newest) if newest else ""),
        "TOP_RIGHT": esc(TOP_RIGHT),
        "ISSUES": issues,
        "SOURCES_NOTE": esc("Compiled from wire reports"),
        "HOME_HREF": esc("today.html"),
    }) + "\n"


def _extract_style(page_block: str) -> str:
    """Reuse the PAGE block's CSS so the archive cannot drift from the paper."""
    match = re.search(r"<style>(.*?)</style>", page_block, re.S)
    if not match:
        raise ValueError("PAGE block has no <style> to share with the archive")
    return match.group(1)


def write_site(edition: dict, out_path: str) -> None:
    """Write the dated edition page, the "/" copy, and the archive."""
    _ensure_dir(out_path)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_html(edition))

    # site/home.html is the STATIC Home page (Pat's bookmark, reaching all
    # three papers, and the page the daily Discord post links) and the
    # renderer must NEVER write it — nor site/index.html, which is now a
    # redirect to it so a bare / still resolves. Today's Times lives at
    # today.html, same stable-bookmark behaviour, one level in.
    index_path = os.path.join(SITE_DIR, "today.html")
    _ensure_dir(index_path)
    with open(index_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_html(edition, root=""))

    archive_path = os.path.join(SITE_DIR, "archive.html")
    with open(archive_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(render_archive_html(archive_entries()))


def _ensure_dir(path: str) -> None:
    directory = os.path.dirname(os.path.abspath(path))
    if directory:
        os.makedirs(directory, exist_ok=True)


# --------------------------------------------------------------------------
# hero card
# --------------------------------------------------------------------------

MARGIN = 56
RULE_GAP = 26

# Pillow draws .notdef boxes for anything the vendored serifs lack, so hero
# text is filtered to the ranges those fonts actually cover. The HTML keeps
# the original characters - the viewer's browser has fonts for them.
_HERO_OK = (
    (0x20, 0x24F),      # ASCII, Latin-1, Latin Extended-A/B
    (0x2B0, 0x2FF),     # spacing modifiers
    (0x2000, 0x206F),   # general punctuation: dashes, curly quotes, ellipsis
    (0x20A0, 0x20BF),   # currency
)


def _hero_text(text: object) -> str:
    kept = [c for c in _norm(text)
            if any(lo <= ord(c) <= hi for lo, hi in _HERO_OK)]
    return re.sub(r"\s+", " ", "".join(kept)).strip()


def _rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _mix(a: tuple[int, int, int], b: tuple[int, int, int],
         t: float) -> tuple[int, int, int]:
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))  # type: ignore[return-value]


def _font_path(filename: str) -> str:
    """Resolve a frozen font filename.

    config.FONTS may key on roles or on filenames; the FILENAMES are what the
    cross-component contract freezes, so they are what this matches on.
    """
    candidates = []
    fonts = getattr(config, "FONTS", {}) or {}
    for value in fonts.values():
        if isinstance(value, str) and os.path.basename(value) == filename:
            candidates.append(value if os.path.isabs(value)
                              else os.path.join(HERE, value))
    font_dir = getattr(config, "FONT_DIR", "") or ""
    if font_dir:
        candidates.append(font_dir if os.path.isabs(font_dir)
                          else os.path.join(HERE, font_dir))
        candidates[-1] = os.path.join(candidates[-1], filename)
    candidates.append(os.path.join(HERE, "assets", "fonts", filename))
    for path in candidates:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"vendored font not found: {filename}")


class _Faces:
    """Lazily loaded, size-cached font faces."""

    def __init__(self) -> None:
        from PIL import ImageFont
        self._truetype = ImageFont.truetype
        self._cache: dict[tuple[str, int], object] = {}

    def get(self, filename: str, size: int):
        key = (filename, size)
        if key not in self._cache:
            self._cache[key] = self._truetype(_font_path(filename), size)
        return self._cache[key]

    def display(self, size: int):
        return self.get("PlayfairDisplay-Black.ttf", size)

    def body(self, size: int):
        return self.get("SourceSerif4-Regular.ttf", size)

    def strong(self, size: int):
        return self.get("SourceSerif4-Semibold.ttf", size)

    def alt(self, size: int):
        return self.get("OldStandard-Regular.ttf", size)

    def italic(self, size: int):
        return self.get("SourceSerif4-Italic.ttf", size)


def _wrap(draw, text: str, font, width: float) -> list[str]:
    """Greedy wrap; a single word wider than the column is hard-split."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        while draw.textlength(word, font=font) > width and len(word) > 1:
            cut = len(word)
            while cut > 1 and draw.textlength(word[:cut], font=font) > width:
                cut -= 1
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:cut])
            word = word[cut:]
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=font) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def _fit(draw, text: str, loader, width: float, max_lines: int,
         lo: int, hi: int) -> tuple[object, list[str]]:
    """Largest point size whose wrap fits in max_lines. Binary search."""
    best = (loader(lo), _wrap(draw, text, loader(lo), width))
    while lo <= hi:
        mid = (lo + hi) // 2
        font = loader(mid)
        lines = _wrap(draw, text, font, width)
        if len(lines) <= max_lines:
            best = (font, lines)
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def _tracked_width(draw, text: str, font, tracking: float) -> float:
    if not text:
        return 0.0
    return sum(draw.textlength(c, font=font) for c in text) \
        + tracking * (len(text) - 1)


def _draw_tracked(draw, xy: tuple[float, float], text: str, font,
                  fill_color, tracking: float) -> None:
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=font, fill=fill_color, anchor="ls")
        x += draw.textlength(char, font=font) + tracking


def _triangle(draw, cx: float, baseline: float, size: float, direction: str,
              color) -> None:
    """Stat direction as a polygon - the vendored serifs have no arrow glyphs,
    and a missing glyph renders as a tofu box."""
    half = size / 2
    top = baseline - size
    if direction == "up":
        draw.polygon([(cx, top), (cx - half, baseline), (cx + half, baseline)],
                     fill=color)
    elif direction == "down":
        draw.polygon([(cx, baseline), (cx - half, top), (cx + half, top)],
                     fill=color)
    else:
        draw.rectangle([cx - half, baseline - size * 0.62,
                        cx + half, baseline - size * 0.38], fill=color)


def _headline_block(font, lines: list[str]) -> int:
    """Vertical space a drawn headline actually occupies, from lead_top.

    One leading per line PLUS the drop to the first baseline, which is what
    `_render_hero` adds before it draws line one.
    """
    return round(font.size * 0.78) + len(lines) * round(font.size * 1.06)


def render_hero_png(edition: dict, out_path: str) -> bool:
    """Draw the 1200x630 hero card. Returns False on any failure, never raises.

    Decoration must never take the paper down with it, so every exception in
    here - missing Pillow, missing font, arithmetic that walks off the canvas -
    resolves to False and the caller attaches the committed fallback banner.
    """
    try:
        return _render_hero(edition, out_path)
    except Exception:
        print("ERROR: hero render failed", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return False


def _render_hero(edition: dict, out_path: str) -> bool:
    from PIL import Image, ImageDraw

    width, height = getattr(config, "HERO_SIZE", (1200, 630))
    palette = config.PALETTE
    ink = _rgb(palette["ink"])
    parchment = _rgb(palette["parchment"])
    parchment_alt = _rgb(palette["parchment_alt"])
    accent = _rgb(palette["accent"])
    rule = _mix(parchment_alt, ink, 0.32)
    soft_ink = _mix(ink, parchment, 0.22)

    faces = _Faces()
    image = Image.new("RGB", (width, height), parchment)
    draw = ImageDraw.Draw(image)
    inner = width - 2 * MARGIN

    lead = edition.get("lead") or {}
    stats = [s for s in (lead.get("stat_strip") or []) if _norm(s.get("value"))]

    # --- masthead -------------------------------------------------------
    mast_text = _hero_text(config.MASTHEAD).upper()
    mast_font, _ = _fit(draw, mast_text, faces.display, inner, 1, 40, 92)
    y = 92
    draw.text((width / 2, y), mast_text, font=mast_font, fill=ink, anchor="ms")

    tag_font = faces.alt(21)
    tag_text = _hero_text(config.TAGLINE).upper()
    tag_track = 9.0
    tag_width = _tracked_width(draw, tag_text, tag_font, tag_track)
    y += 34
    _draw_tracked(draw, ((width - tag_width) / 2, y), tag_text, tag_font,
                  accent, tag_track)

    y += 22
    draw.rectangle([MARGIN, y, width - MARGIN, y + 3], fill=ink)
    draw.rectangle([MARGIN, y + 8, width - MARGIN, y + 9], fill=ink)

    # --- folio ----------------------------------------------------------
    y += 36
    folio_font = faces.alt(19)
    folio_track = 3.0
    left = _hero_text(folio_left(edition)).upper()
    right = _hero_text(long_date(edition["edition_date"])).upper()
    left_width = _tracked_width(draw, left, folio_font, folio_track)
    right_width = _tracked_width(draw, right, folio_font, folio_track)
    _draw_tracked(draw, (MARGIN, y), left, folio_font, ink, folio_track)
    _draw_tracked(draw, (width - MARGIN - right_width, y), right, folio_font,
                  ink, folio_track)

    # The ear rides free in the folio band when the dateline leaves room;
    # otherwise it takes its own line below the rule and the lead gives up
    # 24px for it. It is never squeezed against the masthead.
    ear = _hero_text(edition.get("weather_ear"))
    gap = 48
    room = 2 * min(width / 2 - (MARGIN + left_width),
                   (width - MARGIN - right_width) - width / 2) - gap
    placed = bool(ear) and _draw_weather_ear(draw, faces, ear, y, width, room,
                                             soft_ink, (18, 16))

    y += 12
    draw.rectangle([MARGIN, y, width - MARGIN, y + 1], fill=ink)

    if ear and not placed:
        y += 24
        _draw_weather_ear(draw, faces, ear, y, width, inner, soft_ink,
                          (18, 16, 14))

    # --- vertical budget ------------------------------------------------
    band_height = 84
    bottom = height - 26
    stats_top = bottom - band_height if stats else bottom
    lead_top = y + 30
    available = stats_top - 22 - lead_top

    byline_height = 30
    excerpt_leading = 29
    min_excerpt = excerpt_leading * 2

    # --- lead headline --------------------------------------------------
    # The block is measured from lead_top, so it costs the first baseline's
    # drop (0.78 em) ON TOP of one leading per line. Counting only the lines
    # under-measures a big headline by most of a point size, and the rows it
    # quietly borrows are the excerpt's - a short headline sets large, the
    # excerpt fails its `rows >= 2` test, and the card silently loses its
    # drop cap with a hole where the copy should be.
    headline = _hero_text(lead.get("headline")) or _hero_text(config.MASTHEAD)
    head_budget = available - byline_height - min_excerpt
    head_font = None
    head_lines: list[str] = []
    for max_lines in (2, 3):
        head_font, head_lines = _fit(draw, headline, faces.display, inner,
                                     max_lines, 30, 74)
        if _headline_block(head_font, head_lines) <= head_budget:
            break

    # Still over: step the size down until it fits. Rewrapping smaller can
    # add a line and still win, because leading shrinks with it.
    size = head_font.size
    while size > 30 and _headline_block(head_font, head_lines) > head_budget:
        size -= 2
        head_font = faces.display(size)
        head_lines = _wrap(draw, headline, head_font, inner)

    leading = round(head_font.size * 1.06)
    if _headline_block(head_font, head_lines) > head_budget:
        room = head_budget - round(head_font.size * 0.78)
        head_lines = head_lines[:max(1, room // leading)]

    y = lead_top + round(head_font.size * 0.78)
    for line in head_lines:
        draw.text((width / 2, y), line, font=head_font, fill=ink, anchor="ms")
        y += leading
    y += 6

    # --- byline ---------------------------------------------------------
    byline_font = faces.strong(16)
    byline = _hero_text(f"By {lead.get('byline') or config.BYLINE}").upper()
    byline_track = 4.5
    byline_width = _tracked_width(draw, byline, byline_font, byline_track)
    _draw_tracked(draw, ((width - byline_width) / 2, y), byline, byline_font,
                  accent, byline_track)
    hair = (width - byline_width) / 2 - 22
    draw.rectangle([MARGIN + 40, y - 5, hair, y - 4], fill=rule)
    draw.rectangle([width - hair, y - 5, width - MARGIN - 40, y - 4], fill=rule)
    y += 26

    # --- drop-capped excerpt, two columns -------------------------------
    excerpt_room = stats_top - 22 - y
    rows = int(excerpt_room // excerpt_leading)
    if rows >= 2:
        _draw_excerpt(draw, faces, lead, y, rows, width, inner, excerpt_leading,
                      ink, soft_ink, rule)

    # --- stat strip -----------------------------------------------------
    if stats:
        _draw_stats(draw, faces, stats[:6], stats_top, band_height, width,
                    ink, accent, parchment_alt, rule)

    _ensure_dir(out_path)
    image.save(out_path, format="PNG", optimize=True)
    return _fit_byte_budget(image, out_path)


def _draw_weather_ear(draw, faces: _Faces, ear: str, baseline: float,
                      width: int, room: float, color,
                      sizes: tuple[int, ...]) -> bool:
    """Set the 7:15 pointer centered on one line, largest size that fits.

    Returns False rather than wrapping or truncating: at the ~550px Discord
    renders the card, a two-line ear reads as body copy and a clipped one
    reads as a bug.
    """
    for size in sizes:
        font = faces.italic(size)
        if draw.textlength(ear, font=font) <= room:
            draw.text((width / 2, baseline), ear, font=font, fill=color,
                      anchor="ms")
            return True
    return False


def _draw_excerpt(draw, faces: _Faces, lead: dict, top: float, rows: int,
                  width: int, inner: int, leading: int, ink, soft_ink,
                  rule) -> None:
    paragraphs = [_hero_text(p) for p in (lead.get("body") or [])]
    text = " ".join(p for p in paragraphs if p)
    if not text:
        return

    gutter = 44
    col_width = (inner - gutter) / 2
    body_font = faces.body(20)
    cap_font = faces.display(52)

    # A drop cap needs lines to wrap around it; on a stub of a lead it just
    # looks like a stranded letter, so it only appears once there are two.
    if len(_wrap(draw, text, body_font, col_width)) < 2:
        draw.text((MARGIN, top + leading - 8), text, font=body_font,
                  fill=soft_ink, anchor="ls")
        return

    first, rest = text[0], text[1:]
    cap_width = draw.textlength(first, font=cap_font) + 9
    cap_rows = 2

    indented = _wrap(draw, rest, body_font, col_width - cap_width)[:cap_rows]
    consumed = " ".join(indented)
    remainder = rest[len(consumed):].lstrip() if consumed else rest
    flowed = _wrap(draw, remainder, body_font, col_width)

    lines = [(line, True) for line in indented] + [(line, False) for line in flowed]
    total = min(len(lines), rows * 2)
    truncated = total < len(lines)
    lines = lines[:total]
    if truncated and lines:
        line, was_indented = lines[-1]
        lines[-1] = (line.rstrip(" .,;:") + "…", was_indented)

    left_count = min(rows, (total + 1) // 2)
    columns = (lines[:left_count], lines[left_count:])

    baseline = top + leading - 8
    draw.text((MARGIN - 2, baseline + leading * (cap_rows - 1) + 2), first,
              font=cap_font, fill=ink, anchor="ls")

    for index, column in enumerate(columns):
        x = MARGIN + index * (col_width + gutter)
        cy = baseline
        for line, was_indented in column:
            offset = cap_width if (was_indented and index == 0) else 0
            draw.text((x + offset, cy), line, font=body_font, fill=soft_ink,
                      anchor="ls")
            cy += leading

    if columns[1]:
        rule_x = MARGIN + col_width + gutter / 2
        tallest = max(len(columns[0]), len(columns[1]))
        draw.rectangle([rule_x, top - 2, rule_x + 1,
                        top + leading * tallest - 4], fill=rule)


def _draw_stats(draw, faces: _Faces, stats: list, top: float, band: int,
                width: int, ink, accent, parchment_alt, rule) -> None:
    draw.rectangle([MARGIN, top, width - MARGIN, top + band], fill=parchment_alt)
    draw.rectangle([MARGIN, top, width - MARGIN, top + 2], fill=ink)
    draw.rectangle([MARGIN, top + band - 2, width - MARGIN, top + band], fill=ink)

    label_font = faces.strong(15)
    value_font = faces.strong(24)
    change_font = faces.body(17)
    cell = (width - 2 * MARGIN) / len(stats)

    for index, stat in enumerate(stats):
        cx = MARGIN + cell * index + cell / 2
        label = _hero_text(stat.get("label")).upper()
        track = 2.6
        label_width = _tracked_width(draw, label, label_font, track)
        _draw_tracked(draw, (cx - label_width / 2, top + 26), label, label_font,
                      accent, track)

        draw.text((cx, top + 52), _hero_text(stat.get("value")),
                  font=value_font, fill=ink, anchor="ms")

        change = _hero_text(stat.get("change"))
        direction = _norm(stat.get("direction")).lower()
        if change:
            change_width = draw.textlength(change, font=change_font)
            marker = 11 if direction in ("up", "down", "flat") else 0
            gap = 6 if marker else 0
            start = cx - (change_width + marker + gap) / 2
            if marker:
                _triangle(draw, start + marker / 2, top + 74, marker, direction,
                          ink)
            draw.text((start + marker + gap, top + 74), change,
                      font=change_font, fill=ink, anchor="ls")

        if index:
            x = MARGIN + cell * index
            draw.rectangle([x, top + 12, x + 1, top + band - 12], fill=rule)


def _fit_byte_budget(image, out_path: str) -> bool:
    """Keep the attachment under the message budget.

    Quantizing beats a WebP re-encode here: the card is flat parchment and a
    few ink tones, so a palette costs nothing visually, and the attachment
    filename is frozen as .png across three components.
    """
    from PIL import Image

    budget = getattr(config, "ATTACH_BYTE_BUDGET", 7_000_000)
    if os.path.getsize(out_path) <= budget:
        return True
    image.convert("P", palette=Image.Palette.ADAPTIVE, colors=128).save(
        out_path, format="PNG", optimize=True)
    if os.path.getsize(out_path) <= budget:
        return True
    print(f"ERROR: hero PNG is {os.path.getsize(out_path)} bytes "
          f"(budget {budget})", file=sys.stderr)
    return False


def render_fallback_banner(out_path: str) -> bool:
    """Draw assets/masthead-fallback.png - dateless, rendered once, committed.

    Attached in place of the hero whenever render_hero_png fails, so the post
    keeps its newspaper identity even when rendering is broken.
    """
    try:
        from PIL import Image, ImageDraw

        width, height = getattr(config, "HERO_SIZE", (1200, 630))
        palette = config.PALETTE
        ink = _rgb(palette["ink"])
        parchment = _rgb(palette["parchment"])
        accent = _rgb(palette["accent"])

        faces = _Faces()
        image = Image.new("RGB", (width, height), parchment)
        draw = ImageDraw.Draw(image)
        inner = width - 2 * MARGIN

        mast = _hero_text(config.MASTHEAD).upper()
        font, _ = _fit(draw, mast, faces.display, inner, 1, 40, 96)
        middle = height / 2
        draw.text((width / 2, middle), mast, font=font, fill=ink, anchor="ms")

        tag_font = faces.alt(24)
        tag = _hero_text(config.TAGLINE).upper()
        track = 11.0
        tag_width = _tracked_width(draw, tag, tag_font, track)
        _draw_tracked(draw, ((width - tag_width) / 2, middle + 44), tag,
                      tag_font, accent, track)

        for offset, thickness in ((-96, 3), (-86, 1), (78, 1), (88, 3)):
            y = middle + offset
            draw.rectangle([MARGIN, y, width - MARGIN, y + thickness], fill=ink)

        note_font = faces.alt(19)
        note = _hero_text("Morning Edition").upper()
        note_width = _tracked_width(draw, note, note_font, 4.0)
        _draw_tracked(draw, ((width - note_width) / 2, middle + 124), note,
                      note_font, ink, 4.0)

        _ensure_dir(out_path)
        image.save(out_path, format="PNG", optimize=True)
        return True
    except Exception:
        print("ERROR: fallback banner render failed", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return False


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

# --------------------------------------------------- Sports & Sportsman

def _sm_roundup_item(blocks: dict[str, str], head: str, item: str,
                     entry: dict) -> str:
    """One notebook-style line: bold head, sentence, source."""
    dateline = fill(blocks["ROUNDUP_DATELINE"], {
        "PLACE": esc(head), "PEOPLE": "",
    }) if head else ""
    return fill(blocks["ROUNDUP_ITEM"], {
        "DATELINE": dateline,
        "ITEM": esc(item),
        "SOURCE": _source_html(blocks, entry),
    })


def _sm_seasons_html(blocks: dict[str, str], section: dict) -> str:
    """In Season grouped BY STATE — WV and NC never intermingle.

    Nate, 2026-08-15: two agencies, two licences, and a reader skimming a
    mixed list can carry an NC limit to a WV creek. One state, one block;
    the bucket (Coming in / Prime / Going out) rides each line's head.
    """
    groups = []
    for state, state_label in (("WV", "West Virginia"),
                               ("NC", "North Carolina")):
        items = []
        for key, label in (("coming_in", "Coming in"), ("prime", "Prime"),
                           ("going_out", "Going out")):
            for entry in (section.get(key) or []):
                if not isinstance(entry, dict) or entry.get("state") != state:
                    continue
                item = _norm(entry.get("item") or entry.get("text"))
                if not item:
                    continue
                head = _norm(entry.get("species"))
                if head and entry.get("method"):
                    head += f" ({_norm(entry['method'])})"
                if head and entry.get("dates"):
                    head += f", {_norm(entry['dates'])}"
                head = f"{label} · {head}" if head else label
                items.append(_sm_roundup_item(blocks, head, item, entry))
        for entry in (section.get("notes") or []):
            if isinstance(entry, dict) and entry.get("state") == state                     and _norm(entry.get("item")):
                items.append(_sm_roundup_item(blocks, "", _norm(entry["item"]),
                                              entry))
        if items:
            groups.append(fill(blocks["WV_BLOCK"], {
                "BLOCK_CLASS": "sm-seasons",
                "BLOCK_LABEL": esc(state_label),
                "ITEMS": "".join(items),
            }))
    stray = [entry for entry in (section.get("notes") or [])
             if isinstance(entry, dict) and _norm(entry.get("item"))
             and entry.get("state") not in ("WV", "NC")]
    if stray:
        groups.append(fill(blocks["WV_BLOCK"], {
            "BLOCK_CLASS": "sm-seasons",
            "BLOCK_LABEL": "Also",
            "ITEMS": "".join(_sm_roundup_item(blocks, "", _norm(e["item"]), e)
                              for e in stray),
        }))
    return "".join(groups)


def render_sportsman_html(edition: dict) -> str:
    """The Sports & Sportsman page, from the same template and tokens.

    Reuses the broadsheet PAGE shell with the lead apparatus left empty —
    this paper has no lead story, no stat strip, no weather ear and no
    drawing, and an empty div costs nothing. What it has renders through
    the same blocks the notebook already uses, so it inherits Ian's design
    without a second stylesheet to keep in sync.
    """
    blocks = load_blocks()
    date_iso = edition["edition_date"]
    dateline = long_date(date_iso)
    by_id = {s.get("id"): s for s in (edition.get("sections") or [])}

    parts = []
    for section_id in ("teams", "leagues"):
        section = by_id.get(section_id)
        if not section:
            continue
        briefs = [_brief_html(blocks, b) for b in (section.get("briefs") or [])]
        body = "".join(b for b in briefs if b)
        if section_id == "teams":
            # The standing blocks: standings and fixtures, instrument
            # readings that keep a quiet Monday from reading skimpy.
            for key, label, fmt in (
                    ("standings", config.SPORTSMAN_STANDINGS_LABEL,
                     lambda e: (e.get("team"), _norm(e.get("line")))),
                    ("upcoming", config.SPORTSMAN_UPCOMING_LABEL,
                     lambda e: (e.get("team"),
                                _norm(e.get("fixture"))
                                + (f", {_norm(e['when'])}" if e.get("when")
                                   else "")))):
                items = []
                for entry in (section.get(key) or []):
                    if not isinstance(entry, dict):
                        continue
                    head, text = fmt(entry)
                    if head and text:
                        items.append(_sm_roundup_item(blocks, _norm(head),
                                                      text, entry))
                if items:
                    body += fill(blocks["WV_BLOCK"], {
                        "BLOCK_CLASS": "sm-teams",
                        "BLOCK_LABEL": esc(label),
                        "ITEMS": "".join(items),
                    })
        if body:
            parts.append(fill(blocks["SECTION"], {
                "SECTION_LABEL": esc(_norm(section.get("label")) or section_id),
                "BRIEFS": body,
            }))

    seasons = by_id.get("seasons")
    if seasons:
        body = _sm_seasons_html(blocks, seasons)
        if body:
            parts.append(fill(blocks["SECTION"], {
                "SECTION_LABEL": esc(_norm(seasons.get("label")) or "In Season"),
                "BRIEFS": body,
            }))

    water = by_id.get("water")
    if water:
        import post_discord as _pd
        grouped: dict[str, list[str]] = {}
        for entry in (water.get("waters") or []):
            if not isinstance(entry, dict):
                continue
            name = _norm(entry.get("water") or entry.get("name"))
            bits = [b for b in (_norm(entry.get("reading")),
                                _norm(entry.get("read") or entry.get("line")),
                                _norm(entry.get("working"))) if b]
            seen, body = set(), []
            for bit in bits:
                if bit not in seen:
                    body.append(bit)
                    seen.add(bit)
            if not (name and body):
                continue
            grouped.setdefault(_pd._water_state(name), []).append(
                _sm_roundup_item(blocks, name, " ".join(body), entry))
        water_groups = []
        for state, state_label in (("WV", "West Virginia"),
                                   ("NC", "North Carolina"),
                                   ("", "Elsewhere")):
            if grouped.get(state):
                water_groups.append(fill(blocks["WV_BLOCK"], {
                    "BLOCK_CLASS": "sm-water",
                    "BLOCK_LABEL": esc(state_label),
                    "ITEMS": "".join(grouped[state]),
                }))
        if water_groups:
            parts.append(fill(blocks["SECTION"], {
                "SECTION_LABEL": esc(_norm(water.get("label")) or "On the Water"),
                "BRIEFS": (_tide_table_html(edition.get("edition_date"))
                           + "".join(water_groups)),
            }))

    folio = (f"Vol. {edition.get('volume', 'I')} — "
             f"No. {edition.get('edition_number', '?')}")
    values = {
        "PAGE_CLASS": "sportsman",
        "PAGE_TITLE": esc(f"{config.SPORTSMAN_MASTHEAD} — {dateline}"),
        "META_DESCRIPTION": esc(
            f"Sports & Sportsman for {dateline} — teams, seasons and the "
            "morning's gauges."),
        "FAMILY_LINE": _family_line(),
        "NAV": _nav_html("sportsman", "../"),
        "NAV_FOOT": _nav_html("sportsman", "../", foot=True),
        "MASTHEAD": esc(config.SPORTSMAN_MASTHEAD),
        "TAGLINE": esc("For the Fellers"),
        "TOP_LEFT": esc(folio),
        "TOP_MID": esc(dateline),
        "TOP_RIGHT": esc(TOP_RIGHT),
        "WEATHER_EAR": "",
        "LEAD_HEADLINE": "",
        "LEAD_DEK": "",
        "LEAD_BYLINE": "",
        "LEAD_ART": "",
        "LEAD_BLOCK_CLASS": _lead_block_class(""),
        "SECTIONS_STYLE": "",
        "LEAD_BODY": "",
        "STAT_STRIP": "",
        "SECTIONS": "\n\n  ".join(parts),
        "KICKER": _kicker_html(blocks, edition.get("kicker")),
        "SOURCES_NOTE": esc(_norm(edition.get("sources_note"))
                            or "Compiled from wire reports"),
        "ARCHIVE_LINK": "",
    }
    return fill(blocks["PAGE"], values)


def write_sportsman_site(edition: dict) -> list[str]:
    """site/sportsman/<date>.html plus index.html as the stable bookmark."""
    html = render_sportsman_html(edition)
    directory = os.path.join(config.SITE_DIR, "sportsman")
    os.makedirs(directory, exist_ok=True)
    dated = os.path.join(directory, f"{edition['edition_date']}.html")
    written = []
    for path in (dated, os.path.join(directory, "index.html")):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html)
        written.append(path)
    return written


# ----------------------------------------------------------- weather page

# Jim Claudtore's briefing, typeset. The Times READS the weatherman's
# already-published briefing markdown and renders it into the house chrome;
# nothing in the weatherman repo or routine is touched — that is Nate's
# explicit boundary (2026-08-18: "don't change anything about The Weather
# Claude without my consent").

WEATHER_PING_RE = re.compile(r"\s*<@!?\d+>")
WEATHER_SNOWFLAKE_RE = re.compile(r"\d{17,19}")


def _weather_body(markdown: str) -> str:
    """The briefing minus its frontmatter, with every Discord ping scrubbed.

    THE SCRUB IS LOAD-BEARING. The briefing pings people by Discord user id
    (`<@272...>`), and this repo is PUBLIC — an id may never reach the
    rendered page. Verified after conversion, not assumed: any surviving
    17-19 digit run refuses the render.
    """
    body = markdown
    if body.startswith("---"):
        end = body.find("\n---", 3)
        if end != -1:
            body = body[end + 4:]
    return WEATHER_PING_RE.sub("", body).strip()


# ------------------------------------------------ the weather page, typeset

# Nate, 2026-08-25: "make the newspaper weather page look like the other
# newspaper pages." It had been a transcript — one 760px column of Jim's
# Discord message with the emoji headers, the bullet lists and the "-#"
# small-text markers still in it. It read as a chat log somebody had pasted
# into a nice font.
#
# The briefing's markdown is not arbitrary; it is a stable dialect Jim
# writes every morning, so it maps cleanly onto the paper's own furniture:
#
#   # <day>              -> the page headline
#   ## <dek>             -> the dek under it
#   ### <place - person> -> a section label, the same black chip the wire
#                           sections use. Consecutive ### with no body
#                           between them are a STACK sharing one report, and
#                           they become one section with a combined label.
#   - <item>             -> the notebook's roundup list
#   > <text>             -> a boxed feature, the way the notebook is boxed
#   -# <text>            -> the colophon under the page
#
# Emoji are stripped from headings. They are how a Discord post signals a
# heading; a newspaper has type for that, and the black label chip is the
# paper's own answer to the same problem. NOTHING here touches what Jim
# posts to the channel — this module only ever reads his archived markdown.

_WX_HEADING_EMOJI = re.compile(
    "^[" 
    "\U0001F300-\U0001FAFF"   # pictographs, symbols, flags
    "\u2600-\u27BF"           # the older miscellaneous ranges
    "\uFE0F\u200D\u20E3"    # variation selector, ZWJ, keycap
    "]+[ \t]*"
)


def _wx_strip_emoji(text: str) -> str:
    """Drop the leading emoji a Discord heading uses as its bullet."""
    previous = None
    while previous != text:
        previous = text
        text = _WX_HEADING_EMOJI.sub("", text).lstrip()
    return text.strip()


def _wx_inline(text: str) -> str:
    """Escape, then re-apply the only two inline marks Jim uses."""
    out = esc(text)
    out = re.sub(r"[*][*](.+?)[*][*]", r"<b>\1</b>", out)
    out = re.sub(r"(?<![*])[*](?![*])(.+?)(?<![*])[*](?![*])",
                 r"<i>\1</i>", out)
    return out


def _wx_parse(body: str) -> dict:
    """The briefing as a document: day, dek, sections, boxes, notes.

    A section is {"labels": [...], "blocks": [("p", text) | ("ul", [items])]}.
    Stacked headings are collected into `labels` together because that is
    what they mean — three towns under one shared forecast, which Jim writes
    when the weather does not respect a county line.
    """
    doc = {"day": "", "dek": "", "sections": [], "boxes": [], "notes": []}
    current: dict | None = None
    pending_labels: list[str] = []
    list_buffer: list[str] = []

    def flush_list():
        nonlocal list_buffer
        if list_buffer and current is not None:
            current["blocks"].append(("ul", list_buffer))
        list_buffer = []

    def open_section():
        nonlocal current, pending_labels
        current = {"labels": pending_labels, "blocks": []}
        doc["sections"].append(current)
        pending_labels = []

    for raw in body.split("\n"):
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_list()
            continue

        if stripped.startswith("-# "):
            flush_list()
            doc["notes"].append(stripped[3:].strip())
            continue
        if stripped.startswith("> "):
            flush_list()
            doc["boxes"].append(_wx_strip_emoji(stripped[2:]))
            continue
        if stripped.startswith("### "):
            flush_list()
            pending_labels.append(_wx_strip_emoji(stripped[4:]))
            current = None       # body after the LAST of a stack opens it
            continue
        if stripped.startswith("## "):
            doc["dek"] = _wx_strip_emoji(stripped[3:])
            continue
        if stripped.startswith("# "):
            doc["day"] = _wx_strip_emoji(stripped[2:])
            continue

        if current is None:
            if not pending_labels:
                # Prose before any heading: rare, but it is still the day's
                # report and dropping it would be the worst kind of quiet.
                pending_labels = []
            open_section()

        if stripped.startswith("- "):
            list_buffer.append(stripped[2:].strip())
        else:
            flush_list()
            current["blocks"].append(("p", stripped))

    flush_list()
    if pending_labels:                     # trailing headings with no body
        doc["sections"].append({"labels": pending_labels, "blocks": []})
    return doc


def _wx_section_html(blocks: dict[str, str], section: dict) -> str:
    """One location report as a wire section: label chip, then prose."""
    label = " · ".join(l for l in section["labels"] if l)
    parts: list[str] = []
    for kind, payload in section["blocks"]:
        if kind == "p":
            parts.append(f"<p>{_wx_inline(payload)}</p>")
        else:
            items = "".join(f"<li>{_wx_inline(i)}</li>" for i in payload)
            parts.append(f'<ul class="roundup wx-roundup">{items}</ul>')
    if not parts:
        # A heading with nothing under it is not a section. Stacked headings
        # are merged into the one that HAS the body, so this only happens on
        # a trailing heading, and an empty label chip on the page is worse
        # than the heading simply not appearing.
        return ""
    if not label:
        # Prose before the first heading — Jim's scene-setter on some
        # mornings. It is real copy and it runs, but it gets no label chip,
        # because an empty chip reads as a rendering fault.
        return ('<section class="sec sec-wire wx-standfirst">'
                + "".join(parts) + "</section>")
    return fill(blocks["SECTION"], {
        "SECTION_LABEL": esc(label),
        "BRIEFS": "".join(parts),
    })


def _wx_box_html(boxes: list[str]) -> str:
    """Jim's confidence note, boxed the way the notebook is boxed."""
    if not boxes:
        return ""
    paragraphs = "".join(f"<p>{_wx_inline(b)}</p>" for b in boxes if b.strip())
    if not paragraphs:
        return ""
    return (
        '<section class="sec sec-wv wx-confidence">'
        '<div class="wv-box">' + paragraphs + "</div></section>"
    )


def render_weather_html(date_iso: str, briefing_md: str) -> str:
    """Jim's briefing, typeset as a newspaper page rather than a transcript.

    Same chrome as the other two papers: family banner, masthead, nav, a
    headline and dek, location reports as wire sections across the measure,
    Jim's confidence note as a boxed feature, and his small-text lines as
    the colophon. `PAGE_CLASS` is now just "weather" — it used to borrow
    "sportsman" for that page's flowed columns, which is what kept the whole
    briefing in one 760px stripe down the middle of a 1,600px page.
    """
    blocks = load_blocks()
    body = _weather_body(briefing_md)
    survivors = WEATHER_SNOWFLAKE_RE.findall(body)
    if survivors:
        raise ValueError(
            f"briefing still carries {len(survivors)} Discord id(s) after "
            "the scrub — refusing to render to a public page")
    dateline = long_date(date_iso)
    doc = _wx_parse(body)

    rendered = [_wx_section_html(blocks, sec) for sec in doc["sections"]]
    rendered = [html for html in rendered if html]
    # Same flow as the front page: Jim writes half a dozen short reports of
    # wildly different lengths, which is precisely the shape a grid strands.
    parts = [wire_flow(rendered)] if rendered else []
    box = _wx_box_html(doc["boxes"])
    if box:
        parts.append(box)

    # The colophon carries Jim's own small-text lines — the sunset, the
    # shared air-quality note, the source list — because that is exactly
    # what a colophon is, and they were rendering as literal "-#" before.
    note_bits = [esc(n) for n in doc["notes"] if n.strip()]
    sources_note = ("  ".join(note_bits) if note_bits
                    else esc("Filed to the channel at 7:15 ET by Jim Claudtore"))

    headline = doc["day"] or f"The forecast, {dateline}"
    dek_html = (fill(blocks["DEK"], {"DEK": esc(doc["dek"])})
                if doc["dek"] else "")

    values = {
        "PAGE_CLASS": "weather",
        "PAGE_TITLE": esc(f"The Weather Claude — {dateline}"),
        "META_DESCRIPTION": esc(
            doc["dek"] or f"Jim Claudtore's forecast for {dateline}.")[:300],
        "FAMILY_LINE": _family_line(),
        "NAV": _nav_html("weather", "../"),
        "NAV_FOOT": _nav_html("weather", "../", foot=True),
        "MASTHEAD": esc(WEATHER_NAME),
        "TAGLINE": esc("with Jim Claudtore, filed at 7:15 ET"),
        "TOP_LEFT": esc("The Forecast"),
        "TOP_MID": esc(dateline),
        "TOP_RIGHT": esc(TOP_RIGHT),
        "WEATHER_EAR": "",
        "LEAD_HEADLINE": esc(headline),
        "LEAD_DEK": dek_html,
        "LEAD_BYLINE": esc("By Jim Claudtore"),
        "LEAD_ART": "",
        "LEAD_BLOCK_CLASS": _lead_block_class(""),
        "SECTIONS_STYLE": _sections_style(len(rendered)),
        "LEAD_BODY": "",
        "STAT_STRIP": "",
        "SECTIONS": "\n\n  ".join(parts),
        "KICKER": "",
        "SOURCES_NOTE": sources_note,
        "ARCHIVE_LINK": "",
    }
    return fill(blocks["PAGE"], values)


def write_weather_site(date_iso: str, briefing_md: str) -> list[str]:
    """site/weather/<date>.html plus index.html as the stable bookmark."""
    html_out = render_weather_html(date_iso, briefing_md)
    directory = os.path.join(SITE_DIR, "weather")
    os.makedirs(directory, exist_ok=True)
    written = []
    for path in (os.path.join(directory, f"{date_iso}.html"),
                 os.path.join(directory, "index.html")):
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(html_out)
        written.append(path)
    return written


def main() -> int:
    # A UnicodeEncodeError while PRINTING would fail a render that succeeded;
    # Nate's manual fallback runs happen on a cp1252 Windows console.
    config.use_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--date", help="edition date, YYYY-MM-DD")
    parser.add_argument("--edition", help="path to the edition JSON")
    parser.add_argument("--out", help="path for the broadsheet HTML")
    parser.add_argument("--png", help="path for the hero card")
    parser.add_argument("--no-png", action="store_true",
                        help="skip the hero card, write HTML only")
    parser.add_argument("--sportsman", action="store_true",
                        help="render a Sports & Sportsman edition to "
                             "site/sportsman/ (no hero card)")
    parser.add_argument("--weather", metavar="BRIEFING_MD",
                        help="render a Jim Claudtore briefing markdown file "
                             "to site/weather/ (requires --date)")
    parser.add_argument("--fixture", action="store_true",
                        help="render editions/_fixture.json to out/ only")
    parser.add_argument("--make-fallback", action="store_true",
                        help="redraw assets/masthead-fallback.png and exit")
    args = parser.parse_args()

    if args.weather:
        if not args.date:
            print("ERROR: --weather needs --date", file=sys.stderr)
            return 1
        try:
            with open(args.weather, encoding="utf-8") as f:
                briefing = f.read()
        except OSError as exc:
            print(f"ERROR: cannot read briefing: {exc}", file=sys.stderr)
            return 1
        try:
            for path in write_weather_site(args.date, briefing):
                print(f"OK: wrote {path}")
        except ValueError as exc:
            # The id-scrub guard. Publishing wins nothing if it leaks a ping.
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1
        return 0

    if args.make_fallback:
        target = args.png or os.path.join(HERE, "assets", "masthead-fallback.png")
        if not render_fallback_banner(target):
            return 1
        print(f"OK: wrote {target}")
        return 0

    try:
        if args.sportsman and not args.edition:
            if not args.date:
                print("ERROR: --sportsman needs --date", file=sys.stderr)
                return 1
            edition_path = os.path.join(
                EDITIONS_DIR, "sportsman", f"{args.date}.json")
        else:
            edition_path = args.edition or (
            os.path.join(EDITIONS_DIR, "_fixture.json") if args.fixture
            else os.path.join(EDITIONS_DIR, f"{args.date}.json"))
        if not args.fixture and not args.date and not args.edition:
            print("ERROR: --date is required (or use --fixture)", file=sys.stderr)
            return 1
        with open(edition_path, encoding="utf-8") as f:
            edition = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"ERROR: cannot read edition: {exc}", file=sys.stderr)
        return 1

    date_iso = args.date or edition.get("edition_date")
    if not date_iso:
        print("ERROR: edition has no edition_date", file=sys.stderr)
        return 1
    if args.date and edition.get("edition_date") != args.date:
        print(f"ERROR: --date {args.date} does not match edition_date "
              f"{edition.get('edition_date')}", file=sys.stderr)
        return 1

    if args.sportsman:
        # No hero card and no newspaper site index — this paper's whole
        # visual output is its page under site/sportsman/.
        written = write_sportsman_site(edition)
        for path in written:
            print(f"OK: wrote {path}")
        return 0

    # The fixture is a layout regression test, not a news day: it renders to
    # gitignored out/ and never touches the published site or the archive.
    if args.fixture:
        html_path = args.out or os.path.join(OUT_DIR, "fixture.html")
        png_path = args.png or os.path.join(OUT_DIR, "fixture.png")
    else:
        html_path = args.out or os.path.join(SITE_DIR, "editions", f"{date_iso}.html")
        png_path = args.png or os.path.join(OUT_DIR, f"ashgrove-{date_iso}.png")

    # Publishing means three files: the dated page, the "/" copy, and the
    # archive. An explicit --out is a request for ONE file somewhere else —
    # a preview, a diff, a thin-day regression — and must never repoint
    # site/index.html at an edition that is not today's paper.
    publish = not args.fixture and not args.out

    try:
        if publish:
            write_site(edition, html_path)
        else:
            _ensure_dir(html_path)
            with open(html_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(render_html(edition))
    except Exception as exc:
        print(f"ERROR: HTML render failed: {exc}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return 1
    print(f"OK: wrote {html_path}")

    if args.no_png:
        return 0
    if not render_hero_png(edition, png_path):
        print("WARN: hero card not written; post_discord will attach the "
              "fallback banner", file=sys.stderr)
        return 2
    print(f"OK: wrote {png_path} ({os.path.getsize(png_path)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
