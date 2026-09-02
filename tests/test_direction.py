"""Who won the ball game — the prose has to point the same way as `result`.

Twice in three days the sports desk read a table right and stated the
relationship backwards ("Pirates blanked 1-0 by the Padres" when Pittsburgh
won). Every number was real, so every byte-match check passed it. These are
the eight phrasings the 2026-08-26 fix was verified against, kept as tests
so the reader can never quietly regress to the naive pattern that reads the
passive-with-score-interposed as an active win.
"""

from __future__ import annotations

import pytest

import validate_edition as v

PIRATES, PADRES = "Pittsburgh Pirates", "San Diego Padres"


@pytest.mark.parametrize(
    "text, winner, loser, expected",
    [
        # 1. The headline that shipped, with the winner written down honestly:
        #    the passive with the SCORE between the verb and the "by".
        ("Pirates blanked 1-0 by the Padres a night after winning in 12",
         PIRATES, PADRES, "loser"),
        # 2. The corrected headline.
        ("Pirates shut out the Padres 1-0 a night after winning in 12",
         PIRATES, PADRES, "winner"),
        # 3. Both teams by CITY, loss verb, subject is the loser — agrees.
        ("Pittsburgh fell to San Diego 3-0 to even the series",
         PADRES, PIRATES, "winner"),
        # 4. Active win verb, subject is the winner — agrees.
        ("Padres blank the Pirates 3-0 to even the series",
         PADRES, PIRATES, "winner"),
        # 5. "lost to" with the nickname on one side and the city on the other.
        ("The Reds lost to San Francisco 5-4 in ten innings",
         "San Francisco Giants", "Cincinnati Reds", "winner"),
        # 6. City vs nickname, active verb, winner as subject.
        ("Pittsburgh edged the Padres 2-1 behind seven strong innings",
         PIRATES, PADRES, "winner"),
        # 7. Shared words dropped: a New York/New York game must not resolve
        #    both sides to "new york". Passive, score interposed, agreeing.
        ("Mets topped 4-2 by the Yankees in the Bronx",
         "New York Yankees", "New York Mets", "winner"),
        # 8. No recognised verb at all: a preview, not a report. None, never
        #    an error — this looks for a contradiction, not a sentence shape.
        ("Pirates and Padres open a three-game set Friday at PNC Park",
         PIRATES, PADRES, None),
    ],
)
def test_result_direction(text, winner, loser, expected):
    assert v._sm_result_direction(text, winner, loser) == expected


def test_direction_needs_both_teams_named():
    # Only one side appears: nothing to compare, so stay silent.
    assert v._sm_result_direction("Pirates win 1-0", PIRATES, PADRES) is None


def _brief(headline: str, result: dict | None = None) -> dict:
    brief = {"headline": headline, "summary": "", "source": "MLB.com",
             "url": "https://www.mlb.com/"}
    if result is not None:
        brief["result"] = result
    return brief


def test_contradiction_is_an_error():
    brief = _brief("Pirates blanked 1-0 by the Padres",
                   {"winner": PIRATES, "loser": PADRES, "score": "1-0"})
    errors = v._sm_check_result(brief, "teams.briefs[0]", "2026-08-27")
    assert len(errors) == 1
    assert "LOST" in errors[0]


def test_agreement_is_clean():
    brief = _brief("Pirates shut out the Padres 1-0",
                   {"winner": PIRATES, "loser": PADRES, "score": "1-0"})
    assert v._sm_check_result(brief, "teams.briefs[0]", "2026-08-27") == []


def test_score_without_result_is_date_scoped():
    """The `result` field became required on SM_RESULT_REQUIRED_FROM."""
    brief = _brief("Pirates shut out the Padres 1-0")
    before = v._sm_check_result(brief, "p", "2026-08-26")
    after = v._sm_check_result(brief, "p", "2026-08-27")
    assert before == []
    assert len(after) == 1 and "`result`" in after[0]


def test_score_is_written_winner_first():
    brief = _brief("Pirates shut out the Padres",
                   {"winner": PIRATES, "loser": PADRES, "score": "0-1"})
    errors = v._sm_check_result(brief, "p", "2026-08-27")
    assert any("WINNER FIRST" in e for e in errors)


def test_level_score_needs_a_draw_note():
    brief = _brief("Tottenham and Arsenal share the points",
                   {"winner": "Tottenham", "loser": "Arsenal", "score": "1-1"})
    errors = v._sm_check_result(brief, "p", "2026-08-27")
    assert any("draw" in e for e in errors)
    brief["result"]["note"] = "draw; Tottenham advance on penalties"
    assert v._sm_check_result(brief, "p", "2026-08-27") == []
