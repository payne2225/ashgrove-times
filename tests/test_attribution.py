"""Topsail has no thermometer. A printed water temperature says whose it is.

Two gates share the rule: the Times' retired On the Water block
(_check_fishing_entry, still validated for the archive) and Sports &
Sportsman's water section (_sm_check_water). Both are date-scoped to the
station that was current when the line was printed, because the archive
credits Wrightsville Beach through 2026-08-12 and that was right at the time.
"""

from __future__ import annotations

import config
import validate_edition as v

TOPSAIL = config.FISHING_WATERS["topsail"]
STATION = config.TOPSAIL_TEMP_STATION_NAME  # "Beaufort" as of 2026-09-02
TODAY = "2026-09-02"


def _fishing(temp_f: float | None = 84.2) -> dict:
    topsail: dict = {
        "water": TOPSAIL,
        "tides": [{
            "station": "Hampstead", "station_id": "8657813", "side": "sound",
            "events": [
                {"type": "low", "time_local": "12:53 AM", "height_ft": 1.0},
                {"type": "high", "time_local": "6:39 AM", "height_ft": 3.2},
                {"type": "low", "time_local": "12:50 PM", "height_ft": 0.5},
                {"type": "high", "time_local": "7:16 PM", "height_ft": 4.0},
            ],
        }],
        "read": "Fish the moving water either side of high at 6:39 AM and "
                "7:16 PM in the sound.",
    }
    if temp_f is not None:
        topsail["water_temp"] = {
            "water_temp_f": temp_f, "station": STATION,
            "miles_away": config.TOPSAIL_TEMP_MILES,
            "bearing": config.TOPSAIL_TEMP_BEARING,
        }
    return {"date": TODAY, "generated_at": f"{TODAY}T05:40:00-04:00",
            "williams": None, "ohio": [], "topsail": topsail, "errors": []}


def _entry(line: str) -> dict:
    return {"water": TOPSAIL, "line": line, "source": "NOAA CO-OPS 8657813"}


def _credit_errors(line: str, fishing: dict, date: str = TODAY) -> list[str]:
    errors = v._check_fishing_entry(_entry(line), "fishing[1]", fishing, date)
    return [e for e in errors if "credit" in e]


# ------------------------------------------------- the Times' fishing line

def test_no_temperature_needs_no_credit():
    line = "Sound highs 6:39 a.m. and 7:16 p.m. at Hampstead."
    assert _credit_errors(line, _fishing(temp_f=None)) == []


def test_uncredited_temperature_is_an_error():
    line = "Sound highs 6:39 a.m. and 7:16 p.m.; water 84.2F."
    errors = _credit_errors(line, _fishing())
    assert len(errors) == 1
    assert STATION in errors[0]


def test_credited_current_station_is_clean():
    line = (f"Sound highs 6:39 a.m. and 7:16 p.m.; water 84.2F at {STATION}, "
            f"{config.TOPSAIL_TEMP_MILES} miles up the coast.")
    assert _credit_errors(line, _fishing()) == []


def test_credited_wrong_station_is_an_error():
    line = "Sound highs 6:39 a.m. and 7:16 p.m.; water 84.2F at Wilmington."
    errors = _credit_errors(line, _fishing())
    assert len(errors) == 1 and STATION in errors[0]


def test_bare_number_next_to_a_water_word_counts_as_a_temperature():
    # The old guard wanted a trailing F, so "water 84" published the borrowed
    # reading as Topsail's own.
    line = "Sound highs 6:39 a.m. and 7:16 p.m.; water 84 and warm."
    assert len(_credit_errors(line, _fishing())) == 1


def test_credit_is_scoped_to_the_station_of_the_day():
    """An August 5 line credits Wrightsville Beach and is right to.

    Eight archived editions failed today's validator on this until the
    contract tests found it on 2026-09-02.
    """
    prior = config.TOPSAIL_TEMP_PRIOR_STATION_NAME
    before = config.TOPSAIL_TEMP_STATION_CHANGED_ON
    line = f"Ocean highs 12:14 AM and 1:02 PM; water 83.3F at {prior}, 25 mi up the coast."
    old = _fishing(temp_f=83.3)
    old["topsail"]["water_temp"]["station"] = prior
    assert _credit_errors(line, old, "2026-08-05") == []
    # The same line printed after the change credits a station that no
    # longer reports, and fails.
    assert len(_credit_errors(line, old, before)) == 1


# ------------------------------------- Sports & Sportsman's water section

def _water_section(**topsail_fields) -> dict:
    entry = {"water": "Topsail Sound", "near": "New Topsail Inlet",
             "reading": "Sound highs 6:39 AM and 7:16 PM at Hampstead.",
             "read": "Fish the moving water either side of high at 6:39 AM "
                     "and 7:16 PM in the sound.",
             "working": "Tide first: the ebb off the morning high is the window.",
             "source": "NOAA CO-OPS 8657813"}
    entry.update(topsail_fields)
    return {"id": "water", "label": "On the Water", "waters": [entry]}


def _sm_credit_errors(section: dict) -> list[str]:
    errors, _ = v._sm_check_water(section, _fishing())
    return [e for e in errors if "credit" in e]


def test_sportsman_working_field_is_excluded_from_the_temperature_scan():
    """`working` is prose full of numbers and is NOT read for a temperature.

    "an 85% waxing gibbous" reads as a temperature to the bare-number
    heuristic — and very nearly is one, since the water read 85F the same
    morning. A reading goes in a reading field; the prose is left alone.
    """
    section = _water_section(
        working="An 85% waxing gibbous is two nights from full, and tarpon "
                "to 110 pounds are in the surf; the water is warm.")
    assert _sm_credit_errors(section) == []


def test_sportsman_reading_field_is_scanned_and_uncredited_fails():
    section = _water_section(
        reading="Sound highs 6:39 AM and 7:16 PM at Hampstead; water 84.2F.")
    errors = _sm_credit_errors(section)
    assert len(errors) == 1 and STATION in errors[0]


def test_sportsman_credit_anywhere_in_the_entry_counts():
    # The reading carries the number; the credit sits in `working`. Honest.
    section = _water_section(
        reading="Sound highs 6:39 AM and 7:16 PM at Hampstead; water 84.2F.",
        working=f"Water 84.2F at {STATION}, {config.TOPSAIL_TEMP_MILES} "
                "miles up the coast — a warm-water pattern.")
    assert _sm_credit_errors(section) == []
