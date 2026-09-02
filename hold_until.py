"""Sleep until an Eastern wall-clock time, whatever UTC the sandbox is on.

    python hold_until.py 07:45

The cloud routines fire on raw UTC crons, and five of the six are not held
to an Eastern time the way Jim Claudtore's briefing is (`post_discord.py
--at` in the weatherman repo) or the Times digest is (`post_discord.py
--not-before`). On 2026-11-01 every unheld cron slides an hour earlier in
Eastern terms. For most of them that is harmless — a watchdog at 8:00
instead of 9:00 is still a watchdog — but the weather-page routine's
`10 12 * * *` becomes 7:10 ET, FIVE MINUTES BEFORE Jim posts at 7:15, and
its twenty-minute search for his archived briefing would give up before he
had archived it. All winter. This script is the fix: the routine calls it
before it looks, and the look happens at the same Eastern time in February
as in August.

Same DST arithmetic as config.now_et(), so this and the crons can never
disagree about which side of the changeover a morning is on. The guards
are the same as post_discord's hold: a target already past is not an
error (the routine ran late; proceed now), and a target more than three
hours away is a misconfigured cron, not patience (proceed now, loudly).

`--fake-now 2026-11-01T11:50:00Z --dry-run` prints what the hold WOULD do
from a given UTC instant and exits, which is how tests/test_hold.py checks
both sides of the change without waiting for November.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
import time

import config

MAX_HOLD_SECONDS = 3 * 3600


def eastern_now(now_utc: dt.datetime | None = None) -> dt.datetime:
    """Naive Eastern wall-clock time for a UTC instant (default: now).

    The offset is looked up on the EASTERN date, not the UTC one: between
    midnight and 5 a.m. Eastern the two dates differ, and on the changeover
    Sunday that is exactly the window that matters.
    """
    utc = now_utc or dt.datetime.now(dt.timezone.utc)
    if utc.tzinfo is None:
        utc = utc.replace(tzinfo=dt.timezone.utc)
    provisional = utc - dt.timedelta(hours=config.et_utc_offset_hours(utc.strftime("%Y-%m-%d")))
    offset = config.et_utc_offset_hours(provisional.strftime("%Y-%m-%d"))
    return (utc - dt.timedelta(hours=offset)).replace(tzinfo=None)


def seconds_until(target: str, now_utc: dt.datetime | None = None) -> tuple[float, str]:
    """(seconds to wait, why). Zero seconds when there is nothing to wait for."""
    try:
        hour, minute = (int(part) for part in target.split(":", 1))
        goal_time = dt.time(hour, minute)
    except (TypeError, ValueError):
        return 0.0, f"could not parse {target!r} as HH:MM; not holding"
    now = eastern_now(now_utc)
    goal = now.replace(hour=goal_time.hour, minute=goal_time.minute,
                       second=0, microsecond=0)
    wait = (goal - now).total_seconds()
    stamp = f"{now:%Y-%m-%d %H:%M} ET"
    if wait <= 0:
        return 0.0, f"it is {stamp}; {target} ET already passed, proceeding now"
    if wait > MAX_HOLD_SECONDS:
        return 0.0, (f"it is {stamp}; {target} ET is {wait / 3600:.1f}h away — "
                     "that is a misconfigured cron, not a hold; proceeding now")
    return wait, f"it is {stamp}; holding {wait / 60:.0f} min until {target} ET"


def main() -> int:
    config.use_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("target", metavar="HH:MM", help="Eastern wall-clock time to wait for")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would happen and do not sleep")
    parser.add_argument("--fake-now", metavar="ISO_UTC", default=None,
                        help="pretend it is this UTC instant (e.g. 2026-11-01T11:50:00Z)")
    args = parser.parse_args()

    now_utc = None
    if args.fake_now:
        now_utc = dt.datetime.fromisoformat(args.fake_now.replace("Z", "+00:00"))
    wait, why = seconds_until(args.target, now_utc)
    print(f"hold_until: {why}", file=sys.stderr)
    if wait and not args.dry_run:
        time.sleep(wait)
        print(f"hold_until: released at {eastern_now():%H:%M} ET", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
