"""Every away and hotspots line says WHEN, from NOTEBOOK_DATE_WORD_REQUIRED_FROM.

The blocks run a fourteen-day window; the window is honest only because a
reader can never mistake last week's item for this morning's.
"""

from __future__ import annotations

import pytest

import config
import validate_edition as v

BEFORE = "2026-09-02"
AFTER = "2026-09-03"
assert BEFORE < config.NOTEBOOK_DATE_WORD_REQUIRED_FROM <= AFTER


@pytest.mark.parametrize("item", [
    "The select board set a hearing on the water rate for Monday.",
    "The town reopened the sound-side kayak launch Friday.",
    "Council approved the parkade repairs on Tue., 5-2.",
    "The county commission met Aug. 28 and tabled the levy.",
    "Surf City's council meets September 1 on the beach-access ordinance.",
    "Sept. 9 is the courthouse annex hearing.",
    "A water main broke yesterday on Main Street.",
    "The pier reopened this morning after the storm repairs.",
    "The library's fall hours start this week.",
    "Bennington's school board voted last week to keep the bus routes.",
    "The fire department held its pancake breakfast over the weekend.",
    "NCDOT finished the N.C. 50 resurfacing earlier this month.",
    "The bridge closure runs through the 14th.",
    "A boil-water notice has stood since the 28th.",
    "Crews worked overnight to clear the culvert.",
])
def test_accepted_forms(item):
    assert v._has_date_word(item)


@pytest.mark.parametrize("item", [
    "The select board set a hearing on the water rate.",
    "The pier reopened after the storm repairs.",
    "Crews sat on the culvert job for a month.",          # "sat" is a verb
    "A sunny forecast for the fair, and the sun set behind the ridge.",  # "sun" is weather, not Sun.
    "The march on the courthouse drew forty people.",     # "mar" is not March
    "The 9th Street bridge is out.",                      # a street, not a date
])
def test_refused_forms(item):
    assert not v._has_date_word(item)


VERMONT = {"region_id": "vermont", "place": "North Bennington, VT", "people": ["Wes"],
           "item": "The select board set a hearing on the water rate.", "source": "Bennington Banner"}
CABIN = {"hotspot_id": "cabin", "place": "Webster County & Cowen",
         "item": "The county commission set its meeting for the courthouse annex.",
         "source": "Webster County Commission"}


def test_undated_lines_fail_from_the_date():
    assert v._check_date_word(VERMONT, "p", BEFORE) == []
    errors = v._check_date_word(VERMONT, "p", AFTER)
    assert len(errors) == 1
    assert "no day reference" in errors[0] and '"yesterday"' in errors[0]


def test_dated_lines_pass():
    dated = dict(CABIN, item=CABIN["item"] + " on Tuesday.")
    assert v._check_date_word(dated, "p", AFTER) == []


def test_notebook_wires_the_check_for_away_and_hotspots_only():
    section = {"id": "wv", "label": "West Virginia", "notebook_title": config.WV_NOTEBOOK_TITLE,
               "briefs": [], "regional": [
                   {"region_id": "huntington_cabell", "place": "Huntington & the Cabell-Mason corridor",
                    "people": ["Trav"], "item": "The council passed the budget.", "source": "WSAZ"}],
               "away": [VERMONT], "hotspots": [CABIN]}
    errors = [e for e in v._check_notebook(section, 2, None, AFTER) if "no day reference" in e]
    assert len(errors) == 2
    assert any(".away[0]" in e for e in errors) and any(".hotspots[0]" in e for e in errors)
    assert not any(".regional" in e for e in errors)
    # Before the date the same section is clean on this rule.
    assert [e for e in v._check_notebook(section, 2, None, BEFORE) if "no day reference" in e] == []
