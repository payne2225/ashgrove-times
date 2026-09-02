"""MLB standings are byte-matched against the fetcher's table.

Both sports errors Pat caught were real numbers in the wrong relationship,
typed by hand. From SM_STANDINGS_REQUIRED_FROM every record, games-back
figure and ordinal printed for an MLB club must be a value fetch_standings.py
wrote. The table here is the shape fetch_standings.build() produces, with
the 2026-08-24 numbers: Milwaukee 81-50 leading, Pittsburgh fourth, 18.5 back.
"""

from __future__ import annotations

import config
import validate_edition as v

BEFORE = "2026-09-02"
AFTER = "2026-09-03"
assert BEFORE < config.SM_STANDINGS_REQUIRED_FROM <= AFTER


def _row(name, wins, losses, rank, gb, wc, size=5, followed=False):
    words = ("first", "second", "third", "fourth", "fifth")
    return {
        "division": "NL Central", "wins": wins, "losses": losses,
        "record": f"{wins}-{losses}", "division_rank": rank,
        "division_rank_word": words[rank - 1], "division_size": size,
        "is_last": rank == size, "games_back": gb, "wild_card_games_back": wc,
        "wild_card_rank": None, "league_rank": None, "streak": "W1",
        "division_leader": rank == 1, "followed": followed, "league": "MLB",
    }


STANDINGS = {
    "date": "2026-08-24", "source": "MLB Stats API",
    "teams": {
        "Milwaukee Brewers": _row("Milwaukee Brewers", 81, 50, 1, None, None),
        "Chicago Cubs": _row("Chicago Cubs", 75, 56, 2, "6.0", None),
        "St. Louis Cardinals": _row("St. Louis Cardinals", 66, 66, 3, "15.5", "3.0"),
        "Pittsburgh Pirates": _row("Pittsburgh Pirates", 63, 69, 4, "18.5", "6.5", followed=True),
        "Cincinnati Reds": _row("Cincinnati Reds", 62, 69, 5, "19.0", "7.0", followed=True),
    },
    "errors": [],
}


def _teams(*lines):
    return {"standings": [{"team": t, "line": l, "source": "MLB.com", "url": "https://www.mlb.com/standings"}
                          for t, l in lines]}


def _edition(teams, briefs=()):
    return {"sections": [
        {"id": "teams", "label": "Our Teams", "briefs": [], **teams},
        {"id": "leagues", "label": "Around the Leagues",
         "briefs": [{"headline": h, "summary": s, "source": "MLB.com", "url": "https://www.mlb.com/"}
                    for h, s in briefs]},
    ]}


def _check(teams, briefs=(), standings=STANDINGS, date=AFTER):
    edition = _edition(teams, briefs)
    return v._sm_check_standings_numbers(edition, teams, standings, date)


# ------------------------------------------------------ the standings block

def test_honest_line_passes():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back and 6.5 out of a wild card"),
                   ("Cincinnati Reds", "62-69, last in the NL Central, 19 back"))
    errors, notes = _check(teams)
    assert errors == [] and notes == []


def test_wrong_ordinal_fails():
    teams = _teams(("Pittsburgh Pirates", "63-69, second in the NL Central, 18.5 back"))
    errors, _ = _check(teams)
    assert len(errors) == 1 and "second" in errors[0] and "fourth" in errors[0]


def test_wrong_games_back_fails_as_an_unsourced_number():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 16.5 back"))
    errors, _ = _check(teams)
    assert len(errors) == 1 and "16.5" in errors[0] and "same rule as the stat strip" in errors[0]


def test_reversed_record_is_named_as_such():
    teams = _teams(("Pittsburgh Pirates", "69-63, fourth in the NL Central, 18.5 back"))
    errors, _ = _check(teams)
    assert any("wins first" in e for e in errors)


def test_stale_record_fails():
    teams = _teams(("Pittsburgh Pirates", "64-69, fourth in the NL Central, 18.5 back"))
    errors, _ = _check(teams)
    assert any("64" in e for e in errors)


def test_last_is_checked_against_division_size():
    teams = _teams(("Pittsburgh Pirates", "63-69, last in the NL Central, 18.5 back"))
    errors, _ = _check(teams)
    assert len(errors) == 1 and "last" in errors[0]


def test_non_mlb_lines_are_left_alone():
    teams = _teams(("FC Cincinnati", "31 points from 21 matches, sixth in the Eastern Conference"),
                   ("Chelsea", "9 points from 3, second in the table"))
    assert _check(teams) == ([], [])


def test_followed_club_missing_from_the_file_fails():
    standings = {"teams": {k: val for k, val in STANDINGS["teams"].items() if k != "Cincinnati Reds"}}
    teams = _teams(("Cincinnati Reds", "62-69, last in the NL Central, 19 back"))
    errors, _ = _check(teams, standings=standings)
    assert len(errors) == 1 and "not in the standings file" in errors[0]


# ------------------------------------------------------------- date scope

def test_no_data_is_an_error_only_from_the_date():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back"))
    assert _check(teams, standings=None, date=BEFORE) == ([], [])
    errors, _ = _check(teams, standings=None, date=AFTER)
    assert len(errors) == 1 and "fetch_standings.py" in errors[0]


def test_before_the_date_even_a_contradicting_table_is_ignored():
    """An archived edition is judged as the paper it was; a table fetched on
    a later day is another day's table."""
    teams = _teams(("Pittsburgh Pirates", "70-60, first in the NL Central"))
    assert _check(teams, date=BEFORE) == ([], [])
    assert _check(teams, standings={"teams": {}}, date=BEFORE) == ([], [])


def test_no_data_and_no_mlb_lines_is_fine_after_the_date():
    teams = _teams(("Chelsea", "9 points from 3, second in the table"))
    assert _check(teams, standings=None, date=AFTER) == ([], [])


def test_an_empty_table_after_the_date_fails():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back"))
    errors, _ = _check(teams, standings={"teams": {}, "errors": ["down"]}, date=AFTER)
    assert len(errors) == 1 and "fetcher failed" in errors[0]


# --------------------------------------------------------------- the briefs

def test_the_08_24_miss_is_caught_at_the_source():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back"))
    briefs = (("Milwaukee still lead by 18.5",
               "The Brewers hold the NL Central at 81-50, 18.5 clear of second-place Pittsburgh."),)
    errors, notes = _check(teams, briefs)
    # The summary's ordinal contradicts the table: an error.
    assert any("second-place" in e and "fourth" in e for e in errors)
    # The headline names one club, Milwaukee, and prints a figure that is
    # not theirs: an advisory asking whose it is.
    assert any("18.5" in n and "Milwaukee Brewers" in n for n in notes)


def test_a_correct_brief_is_clean():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back"))
    briefs = (("Brewers lead the Central by six", "Milwaukee are 81-50; the Cubs sit 6.0 back."),)
    errors, notes = _check(teams, briefs)
    assert errors == []
    # Two clubs named in the summary: ambiguous, so no advisory either.
    assert notes == []


def test_scores_are_not_mistaken_for_records():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back"))
    briefs = (("Pirates shut out the Padres 1-0", "Pittsburgh won 1-0 and 3-2 in twelve the night before."),
              # The slugfest that tripped a lower threshold on the first dry run.
              ("Pirates outslug the Rockies 13-12 in Denver", "Pittsburgh needed eleven innings."))
    errors, _ = _check(teams, briefs)
    assert errors == []


def test_a_bengals_score_is_never_the_reds_record():
    """"Cincinnati" is three followed clubs; only one is in the table."""
    teams = _teams(("Cincinnati Reds", "62-69, last in the NL Central, 19 back"))
    briefs = (("Bengals fall 31-28 in Cincinnati", "The Cincinnati Bengals lost late."),
              ("FC Cincinnati sit sixth", "Second-place Cincinnati? No — sixth in the East after a 40-31 aggregate."),)
    errors, notes = _check(teams, briefs)
    assert errors == [] and notes == []


def test_a_wrong_record_in_a_brief_fails():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back"))
    briefs = (("Pirates fall to 62-70", "Pittsburgh dropped a fourth straight."),)
    errors, _ = _check(teams, briefs)
    assert len(errors) == 1 and "62-70" in errors[0] and "63-69" in errors[0]


def test_ambiguous_subject_stays_silent():
    teams = _teams(("Pittsburgh Pirates", "63-69, fourth in the NL Central, 18.5 back"))
    # "Cincinnati" alone could be the Reds or FC Cincinnati; the file only
    # has the Reds, so it resolves — but "Pittsburgh and Cincinnati" is two.
    briefs = (("Pittsburgh and Cincinnati both lost", "Second-place nobody."),)
    errors, notes = _check(teams, briefs)
    assert errors == [] and notes == []
