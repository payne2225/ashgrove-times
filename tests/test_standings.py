"""No brief may contradict the standings block printed in the same edition.

No. 10 (2026-08-24) said "18.5 clear of second-place Pittsburgh" while its
own teams block said Pittsburgh was FOURTH and 18.5 BACK. Two printed
ordinals for one team cannot both be true, so that is an error; a games-back
figure on the wrong team is an advisory, because two divisions can honestly
produce the same half-game number.
"""

from __future__ import annotations

import validate_edition as v

TEAMS = {
    "standings": [
        {"team": "Pittsburgh Pirates",
         "line": "63-69, fourth in the NL Central, 18.5 back and 6.5 out of a wild card",
         "source": "MLB.com", "url": "https://www.mlb.com/standings"},
        {"team": "Cincinnati Reds",
         "line": "62-69, last in the NL Central, 19.0 back",
         "source": "MLB.com", "url": "https://www.mlb.com/standings"},
    ],
}


def _edition(headline: str, summary: str) -> dict:
    return {"sections": [
        {"id": "teams", "label": "Our Teams", "briefs": [], "standings": TEAMS["standings"]},
        {"id": "leagues", "label": "Around the Leagues", "briefs": [
            {"headline": headline, "summary": summary,
             "source": "MLB.com", "url": "https://www.mlb.com/"}]},
    ]}


def test_the_08_24_miss_is_caught_both_ways():
    edition = _edition(
        "Milwaukee still lead by 18.5",
        "The Brewers hold the NL Central at 81-50, 18.5 clear of second-place Pittsburgh.")
    errors, notes = v._sm_check_standings_agreement(edition, TEAMS)
    # The summary's ordinal contradicts the block: a hard error.
    assert len(errors) == 1
    assert "second-place" in errors[0] and "fourth" in errors[0]
    assert "Pittsburgh Pirates" in errors[0]
    # The headline prints Pittsburgh's deficit as Milwaukee's lead, alone in
    # its field: an advisory asking whose figure it is.
    assert len(notes) == 1
    assert "headline" in notes[0] and "18.5" in notes[0]
    assert "Pittsburgh Pirates" in notes[0]


def test_agreeing_ordinal_is_clean():
    edition = _edition(
        "Pirates drop a fourth straight",
        "Fourth-place Pittsburgh sit 18.5 back after another quiet night.")
    errors, notes = v._sm_check_standings_agreement(edition, TEAMS)
    assert errors == []
    # 18.5 is Pittsburgh's own figure and Pittsburgh is named in the field.
    assert notes == []


def test_games_back_advisory_runs_per_field():
    """A headline is read alone — the summary naming the team does not save it."""
    edition = _edition(
        "Brewers cruise, 18.5 clear",
        "Pittsburgh are 18.5 back and fading.")
    errors, notes = v._sm_check_standings_agreement(edition, TEAMS)
    assert errors == []
    assert len(notes) == 1 and ".headline" in notes[0]


def test_last_only_compares_with_itself():
    # "last" and "fifth" may or may not agree depending on the division's
    # size; the gate never guesses.
    edition = _edition("Reds lose again", "Fifth-place Cincinnati fell again.")
    errors, _ = v._sm_check_standings_agreement(edition, TEAMS)
    assert errors == []


def test_ambiguous_subject_stays_silent():
    """This desk follows the Reds AND FC Cincinnati: "Cincinnati" alone is
    ambiguous when both sit in the block, and the gate says nothing."""
    teams = {"standings": TEAMS["standings"] + [
        {"team": "FC Cincinnati",
         "line": "31 points from 21 matches, sixth in the Eastern Conference",
         "source": "Fox Sports", "url": "https://www.foxsports.com/"}]}
    edition = _edition("Cincinnati slide", "Second-place Cincinnati lost.")
    errors, _ = v._sm_check_standings_agreement(edition, teams)
    assert errors == []


def test_no_standings_block_means_no_check():
    edition = _edition("Milwaukee still lead by 18.5", "second-place Pittsburgh")
    assert v._sm_check_standings_agreement(edition, {}) == ([], [])
