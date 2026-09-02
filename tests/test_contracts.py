"""The archive can never be silently invalidated again.

One committed edition per contract date, run through the real gate the way
the routine runs it — as a subprocess, with the flags it would use — and
each must still exit 0. The dates are the days the contract changed:

  2026-08-05  the first edition: Sports still a Times section, three-region
              Away Desk, On the Water crediting Wrightsville Beach
  2026-08-15  Sports retired to its own paper (the retired_after boundary)
  2026-08-25  the last On the Water; first Beaufort credit
  2026-08-26  Canada + AI sections, Vacation Hotspots, never-empty blocks
  2026-08-27  Canada tiers required, `result` required on sports briefs

Every fixture ships its own out/-style stats and fishing file, reconstructed
from what the edition printed, because the live out/ files are gitignored and
stale on any machine but the routine's. `--no-urls` because the dead-link
scrubber otherwise MUTATES its input, and because CI has no business
probing forty newspaper URLs at 5:30.

When these tests found the archive on 2026-09-02, eight editions and
editions/_fixture.json were already failing on two un-date-scoped rules.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

from conftest import FIXTURES, ROOT

TIMES_DATES = ["2026-08-05", "2026-08-15", "2026-08-25", "2026-08-26", "2026-08-27"]
SPORTSMAN_DATES = ["2026-08-15", "2026-08-25", "2026-08-26", "2026-08-27"]


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, os.path.join(ROOT, "validate_edition.py"), *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120,
    )


@pytest.mark.parametrize("date", TIMES_DATES)
def test_times_edition_still_validates(date):
    result = _run(
        os.path.join(FIXTURES, f"{date}.json"),
        "--no-urls", "--no-write",
        "--stats", os.path.join(FIXTURES, f"{date}.stats.json"),
        "--fishing", os.path.join(FIXTURES, f"{date}.fishing.json"),
    )
    assert result.returncode == 0, result.stderr
    assert "OK:" in result.stdout


@pytest.mark.parametrize("date", SPORTSMAN_DATES)
def test_sportsman_edition_still_validates(date):
    result = _run(
        os.path.join(FIXTURES, "sportsman", f"{date}.json"),
        "--sportsman", "--no-urls", "--no-write",
        "--fishing", os.path.join(FIXTURES, f"{date}.fishing.json"),
    )
    assert result.returncode == 0, result.stderr
    assert "OK:" in result.stdout


def test_fixture_edition_still_validates():
    """editions/_fixture.json is the executable worst case for layout and
    budget; it is dated 2026-01-15 and must validate under that date's
    contract, not today's."""
    result = _run(os.path.join(ROOT, "editions", "_fixture.json"),
                  "--no-urls", "--no-write", "--no-stats", "--no-fishing")
    assert result.returncode == 0, result.stderr


def test_thin_fixture_still_validates():
    result = _run(os.path.join(ROOT, "editions", "_fixture_thin.json"),
                  "--no-urls", "--no-write", "--no-stats", "--no-fishing")
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("date", TIMES_DATES)
def test_fixture_matches_the_committed_edition(date):
    """A fixture is a copy of the archive, stripped of nothing. If the
    archive edition changes (a dead url scrubbed, a correction), copy it
    over again rather than letting the two drift."""
    with open(os.path.join(FIXTURES, f"{date}.json"), "rb") as f:
        fixture = f.read()
    with open(os.path.join(ROOT, "editions", f"{date}.json"), "rb") as f:
        committed = f.read()
    assert fixture == committed, f"tests/fixtures/{date}.json is behind editions/"
