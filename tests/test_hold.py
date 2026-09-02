"""hold_until.py on both sides of the November clock change.

The weather-page cron is `10 12 * * *` UTC: 8:10 ET on daylight time and
7:10 ET on standard time, five minutes before Jim posts. The routine holds
to 7:45 ET before it looks for his archived briefing, and the hold has to
compute the SAME Eastern time in February as in August.
"""

from __future__ import annotations

import datetime as dt

import config
import hold_until as h


def _utc(iso: str) -> dt.datetime:
    return dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))


def test_dst_boundary_is_2026_11_01():
    assert config.is_eastern_dst("2026-10-31") is True
    assert config.is_eastern_dst("2026-11-01") is False
    assert config.is_eastern_dst("2027-03-14") is True
    assert config.is_eastern_dst("2027-03-13") is False


def test_eastern_now_on_both_sides_of_the_change():
    # The cron's 12:10 UTC instant, the day before and the day after.
    assert h.eastern_now(_utc("2026-10-31T12:10:00Z")) == dt.datetime(2026, 10, 31, 8, 10)
    assert h.eastern_now(_utc("2026-11-01T12:10:00Z")) == dt.datetime(2026, 11, 1, 7, 10)


def test_eastern_date_decides_the_offset_after_utc_midnight():
    # 03:00 UTC on Nov 2 is still Nov 1 in the East, and Nov 1 is standard
    # time: 22:00 ET, not 23:00.
    assert h.eastern_now(_utc("2026-11-02T03:00:00Z")) == dt.datetime(2026, 11, 1, 22, 0)


def test_daylight_time_cron_needs_no_hold():
    wait, why = h.seconds_until("07:45", _utc("2026-10-31T12:10:00Z"))
    assert wait == 0.0
    assert "already passed" in why


def test_standard_time_cron_holds_thirty_five_minutes():
    wait, why = h.seconds_until("07:45", _utc("2026-11-01T12:10:00Z"))
    assert wait == 35 * 60
    assert "holding 35 min" in why


def test_release_instant_is_the_same_eastern_time_all_year():
    # Whatever the UTC instant, the hold releases at 7:45 ET.
    for iso in ("2026-10-31T12:10:00Z", "2026-11-01T12:10:00Z", "2027-01-15T12:10:00Z"):
        start = _utc(iso)
        wait, _ = h.seconds_until("07:45", start)
        released = h.eastern_now(start + dt.timedelta(seconds=wait))
        assert (released.hour, released.minute) in {(7, 45), (8, 10)}, iso
        if wait:
            assert (released.hour, released.minute) == (7, 45)


def test_a_far_target_is_a_misconfigured_cron_not_a_hold():
    wait, why = h.seconds_until("07:45", _utc("2026-11-01T05:00:00Z"))  # 00:00 ET
    assert wait == 0.0
    assert "misconfigured cron" in why


def test_garbage_target_does_not_hold():
    wait, why = h.seconds_until("seven forty-five", _utc("2026-11-01T12:10:00Z"))
    assert wait == 0.0 and "could not parse" in why


def test_times_digest_hold_is_unaffected_by_the_change():
    # The papers wake at 09:30 UTC: 5:30 EDT, 4:30 EST. Either way the digest
    # is held to 7:00 ET; only the head start grows.
    summer, _ = h.seconds_until("07:00", _utc("2026-10-31T09:30:00Z"))
    winter, _ = h.seconds_until("07:00", _utc("2026-11-01T09:30:00Z"))
    assert summer == 90 * 60
    assert winter == 150 * 60
