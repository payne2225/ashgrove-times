"""morning_gate.py: one 5:30 ET start a day, on both sides of both clock changes."""

from __future__ import annotations

import datetime as dt
import json
import subprocess

import pytest

import config
import morning_gate as m
from hold_until import eastern_now

UTC = dt.timezone.utc

# The four mornings either side of the two changes this design was built for.
SUMMER_SIDE = ("2026-10-31", "2027-03-14")
WINTER_SIDE = ("2026-11-01", "2027-03-13")


def _fire(date_iso: str, hour: int, late_minutes: int = 0) -> dt.datetime:
    y, mo, d = (int(p) for p in date_iso.split("-"))
    return dt.datetime(y, mo, d, hour, 30, tzinfo=UTC) + dt.timedelta(minutes=late_minutes)


@pytest.mark.parametrize("late", [0, 13, 25])   # the scheduler starts 0-25 min late
def test_exactly_one_fire_builds_each_morning(late):
    for date_iso in SUMMER_SIDE + WINTER_SIDE:
        first = m.decide(eastern_now(_fire(date_iso, 9, late)), None)
        claim = json.dumps({"date": date_iso})
        second_unclaimed = m.decide(eastern_now(_fire(date_iso, 10, late)), None)
        second_claimed = m.decide(eastern_now(_fire(date_iso, 10, late)), claim)
        if date_iso in SUMMER_SIDE:
            assert (first, second_claimed) == (m.GO, m.DONE)
        else:
            assert (first, second_unclaimed) == (m.EARLY, m.GO)


def test_the_paper_starts_at_530_all_year():
    for date_iso in SUMMER_SIDE + WINTER_SIDE:
        assert config.wake_minutes_et(date_iso) == 5 * 60 + 30
        assert config.head_start_minutes(date_iso) == 90
        assert config.cron_for(date_iso) == "30 9,10 * * *"
        assert config.weather_gap_minutes(date_iso) == 15


def test_yesterdays_claim_does_not_stop_today():
    now = eastern_now(_fire("2026-10-14", 9, 13))
    assert m.decide(now, json.dumps({"date": "2026-10-13"})) == m.GO
    assert m.decide(now, "not json") == m.GO


def test_the_wake_is_655_eastern_on_both_sides():
    for date_iso, utc_hour in (("2026-10-31", 10), ("2026-11-01", 11),
                               ("2027-03-13", 11), ("2027-03-14", 10)):
        y, mo, d = (int(p) for p in date_iso.split("-"))
        status, when, interim = m.wake_target(dt.datetime(y, mo, d, utc_hour, 15, tzinfo=UTC))
        assert (status, interim) == ("WAKE", False)
        assert when == dt.datetime(y, mo, d, utc_hour, 55, tzinfo=UTC)
        assert eastern_now(when).strftime("%H:%M") == "06:55"


def test_a_far_wake_is_an_interim_and_a_near_one_is_now():
    early = dt.datetime(2026, 10, 14, 9, 45, tzinfo=UTC)          # 5:45 AM EDT
    status, when, interim = m.wake_target(early)
    assert status == "WAKE" and interim and when == early + dt.timedelta(minutes=65)
    # 5:50 is 65 minutes out: one wake, straight to 6:55.
    assert m.wake_target(dt.datetime(2026, 10, 14, 9, 50, tzinfo=UTC))[2] is False
    assert "INTERIM" in m.wake_line(early)
    late = dt.datetime(2026, 10, 14, 10, 54, tzinfo=UTC)          # 6:54 AM EDT
    assert m.wake_target(late)[0] == "NOW"
    assert m.wake_line(late).startswith("NOW:")
    line = m.wake_line(dt.datetime(2026, 10, 14, 10, 15, tzinfo=UTC))
    assert line == "WAKE 6:55 AM ET = 2026-10-14T10:55:00Z (in 2400 s)"


# ------------------------------------------------------------------ against real git

def _git(*args, cwd):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                    "-c", "commit.gpgsign=false", *args],
                   cwd=cwd, check=True, capture_output=True)


@pytest.fixture
def clones(tmp_path):
    origin = tmp_path / "origin.git"
    _git("init", "-q", "--bare", "-b", "main", str(origin), cwd=tmp_path)
    seed = tmp_path / "seed"
    _git("clone", "-q", str(origin), str(seed), cwd=tmp_path)
    (seed / "editions").mkdir()
    (seed / "editions" / "claim.json").write_text('{"date": "2026-10-13"}\n', encoding="utf-8")
    _git("add", "-A", cwd=seed)
    _git("commit", "-q", "-m", "seed", cwd=seed)
    _git("push", "-q", "origin", "HEAD:main", cwd=seed)
    out = []
    for name in ("first", "second"):
        path = tmp_path / name
        _git("clone", "-q", str(origin), str(path), cwd=tmp_path)
        _git("config", "user.name", "t", cwd=path)
        _git("config", "user.email", "t@t", cwd=path)
        _git("config", "commit.gpgsign", "false", cwd=path)
        _git("checkout", "-q", "--detach", cwd=path)       # how the sandbox lands
        out.append(path)
    return out


def test_the_first_fire_claims_and_the_second_stops(clones):
    first, second = (str(p) for p in clones)
    status, date_iso, _ = m.gate(first, _fire("2026-10-14", 9, 13), sleep=lambda s: None)
    assert (status, date_iso) == (m.GO, "2026-10-14")
    saved = json.loads((clones[0] / "editions" / "claim.json").read_text(encoding="utf-8"))
    assert saved["date"] == "2026-10-14" and saved["started_et"] == "5:43 AM ET"
    status, _, detail = m.gate(second, _fire("2026-10-14", 10, 4), sleep=lambda s: None)
    assert status == m.DONE and "5:43 AM ET" in detail


def test_a_race_for_the_claim_has_one_winner(clones, monkeypatch):
    first, second = (str(p) for p in clones)
    real_git = m._git
    raced = []

    def git(repo, *args, **kwargs):
        if args[:1] == ("push",) and repo == first and not raced:
            raced.append(True)        # the other fire's claim lands first
            assert m.gate(second, _fire("2026-10-14", 9, 14), sleep=lambda s: None)[0] == m.GO
        return real_git(repo, *args, **kwargs)

    monkeypatch.setattr(m, "_git", git)
    assert m.gate(first, _fire("2026-10-14", 9, 14), sleep=lambda s: None)[0] == m.DONE


def test_an_early_fire_never_touches_git(tmp_path):
    status, _, _ = m.gate(str(tmp_path / "no-repo-here"), _fire("2026-11-02", 9, 20))
    assert status == m.EARLY


def _failing_fetch(real_git, fail_times):
    calls = []

    def git(repo, *args, **kwargs):
        if args[:1] == ("fetch",) and len(calls) < fail_times:
            calls.append(True)
            raise m.GitError("git fetch: The requested URL returned error: 502")
        return real_git(repo, *args, **kwargs)
    return git


def test_a_github_blip_on_the_fetch_is_ridden_out(clones, monkeypatch):
    monkeypatch.setattr(m, "_git", _failing_fetch(m._git, fail_times=2))
    status, _, _ = m.gate(str(clones[0]), _fire("2026-10-14", 9, 13), sleep=lambda s: None)
    assert status == m.GO


def test_with_origin_down_a_checkout_that_has_the_claim_stops(clones, monkeypatch):
    first, second = (str(p) for p in clones)
    assert m.gate(first, _fire("2026-10-14", 9, 13), sleep=lambda s: None)[0] == m.GO
    # The 6:30 fire's sandbox clones origin when it starts, claim included.
    _git("fetch", "-q", "origin", "main", cwd=second)
    _git("checkout", "-q", "--detach", "FETCH_HEAD", cwd=second)
    monkeypatch.setattr(m, "_git", _failing_fetch(m._git, fail_times=99))
    status, _, detail = m.gate(second, _fire("2026-10-14", 10, 9), sleep=lambda s: None)
    assert status == m.DONE and "origin did not answer" in detail


def test_with_origin_down_and_no_claim_it_is_a_git_error(clones, monkeypatch):
    monkeypatch.setattr(m, "_git", _failing_fetch(m._git, fail_times=99))
    with pytest.raises(m.GitError):
        m.gate(str(clones[0]), _fire("2026-10-14", 9, 13), sleep=lambda s: None)
