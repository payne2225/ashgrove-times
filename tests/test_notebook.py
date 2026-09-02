"""The West Virginia notebook's date-scoped rules.

The Away Desk and Vacation Hotspots file EVERY morning from 2026-08-26
(Nate: "there is always stuff to report. Always."); an empty block needs a
note naming what was searched. Prince George and Topsail were promoted out
of the notebook the same day, and an edition dated before that legitimately
carried them.
"""

from __future__ import annotations

import config
import validate_edition as v

BEFORE = "2026-08-20"            # before WV_SUBHEADS_CHANGED_ON
AFTER = "2026-08-27"             # after it
assert BEFORE < config.WV_SUBHEADS_CHANGED_ON <= AFTER

BRIEF = {"headline": "Legislature returns for a two-day interim session",
         "summary": "Lawmakers meet Monday in Charleston.",
         "source": "WV MetroNews", "url": "https://wvmetronews.com/"}

VERMONT = {"region_id": "vermont", "place": "North Bennington, VT",
           "people": ["Wes"],
           "item": "The select board set a Sept. 8 hearing on the water rate.",
           "source": "Bennington Banner"}
PRINCE_GEORGE = {"region_id": "prince_george", "place": "Prince George, BC",
                 "people": ["Kirsten"],
                 "item": "Council approved the downtown parkade repairs Monday.",
                 "source": "Prince George Citizen"}
TOPSAIL = {"region_id": "topsail", "place": "Topsail Beach, NC",
           "people": [],
           "item": "The town reopened the sound-side kayak launch Friday.",
           "source": "WECT"}
CABIN = {"hotspot_id": "cabin", "place": "Webster County & Cowen",
         "item": "The county commission set its Sept. 9 meeting for the courthouse annex.",
         "source": "Webster County Commission"}


def _section(**fields) -> dict:
    section = {"id": "wv", "label": "West Virginia",
               "notebook_title": config.WV_NOTEBOOK_TITLE,
               "briefs": [BRIEF], "regional": [], "away": [], "hotspots": []}
    section.update(fields)
    return section


def _empty_block_errors(section: dict, date: str) -> list[str]:
    return [e for e in v._check_notebook(section, 2, None, date)
            if "runs EVERY morning" in e]


def test_empty_away_and_hotspots_fail_after_the_date():
    errors = _empty_block_errors(_section(), AFTER)
    assert len(errors) == 2
    assert any(".away is empty" in e for e in errors)
    assert any(".hotspots is empty" in e for e in errors)


def test_a_note_naming_the_search_is_the_only_escape():
    section = _section(
        away_note="Searched VTDigger and the Bennington Banner, then the "
                  "select board and school district postings, 14 days.",
        hotspots_note="Searched WECT, Port City Daily, the Surf City and North "
                      "Topsail alerts pages and the Webster County commission.")
    assert _empty_block_errors(section, AFTER) == []


def test_a_filled_block_needs_no_note():
    section = _section(away=[VERMONT], hotspots=[CABIN])
    assert _empty_block_errors(section, AFTER) == []


def test_empty_blocks_were_legal_before_the_date():
    assert _empty_block_errors(_section(), BEFORE) == []


def _promoted_errors(section: dict, date: str) -> list[str]:
    return [e for e in v._check_notebook(section, 2, None, date)
            if "promoted out of the notebook" in e]


def test_promoted_region_is_refused_after_the_date():
    section = _section(away=[VERMONT, PRINCE_GEORGE], hotspots=[CABIN])
    errors = _promoted_errors(section, AFTER)
    assert len(errors) == 1
    assert "prince_george" in errors[0]
    assert "British Columbia" in errors[0]


def test_promoted_region_is_accepted_before_the_date():
    # The 2026-08-23 edition really did file a Prince George line.
    section = _section(away=[PRINCE_GEORGE])
    assert _promoted_errors(section, BEFORE) == []


def _cap_errors(section: dict, date: str) -> list[str]:
    return [e for e in v._check_notebook(section, 2, None, date)
            if "one region cannot file twice" in e]


def test_away_cap_follows_the_roster_of_the_day():
    """Three away regions before the promotions, one after."""
    three = _section(away=[VERMONT, PRINCE_GEORGE, TOPSAIL])
    assert _cap_errors(three, BEFORE) == []
    assert len(_cap_errors(three, AFTER)) == 1
    assert config.wv_away_max_for(BEFORE) == 3
    assert config.wv_away_max_for(AFTER) == 1
    assert config.wv_away_max_for(None) == config.WV_AWAY_MAX


def test_retired_fishing_block_is_refused_after_the_date():
    fishing = [{"water": config.FISHING_WATERS["williams"],
                "line": "99 cfs and falling - prime wading water.",
                "source": "USGS 03186500"}]
    errors = [e for e in v._check_notebook(_section(fishing=fishing), 2, None, AFTER)
              if "retired from the News Desk" in e]
    assert len(errors) == 1
    errors = [e for e in v._check_notebook(_section(fishing=fishing), 2, None, BEFORE)
              if "retired from the News Desk" in e]
    assert errors == []
