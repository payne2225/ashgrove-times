"""Wait for Jim's archived briefing, then say whether to typeset it.

    python wait_for_briefing.py --weatherman ../weatherman

The weather-page routine fires three times a morning on a raw UTC cron,
`17 11,12,13 * * *`: 7:17, 8:17 and 9:17 ET on daylight time, 6:17, 7:17
and 8:17 ET on standard time. The first fire after Jim archives publishes
the page; every later fire finds it already published and stops. That puts
the page on the site a few minutes behind Jim's 7:15 post instead of an
hour behind it, which is what readers kept noticing (Pat, 2026-10-03 and
2026-10-04: "sports and news is today but weather is yesterday"). The old
routine woke once at 8:10 ET and the page landed between 8:12 and 8:39.

Three fires replace a long hold on purpose. A cloud routine's single tool
call cannot sleep for half an hour, and the 2026-09-02 design asked the
winter routine to sleep 35 minutes before it looked. Now no call waits
more than `--minutes` (default 9), and the next fire is the retry.

Prints ONE status line on stdout and exits with its code:

    READY <date> <path>   0   today's briefing is here: render it
    DONE <date>           10  site/weather/<date>.html already exists: stop
    EARLY <date>          11  before 7:10 ET, Jim cannot have archived: stop
    WAITING <date>        12  not here after --minutes: run this once more,
                              or stop and let the next fire take it

The date is always the EASTERN date, so a briefing from yesterday can never
be published under today's.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
import time

import config
from hold_until import eastern_now

HERE = os.path.dirname(os.path.abspath(__file__))
EARLIEST = dt.time(7, 10)  # Jim posts at 7:15 ET and archives after he posts.

READY, DONE, EARLY, WAITING = "READY", "DONE", "EARLY", "WAITING"
EXIT_CODES = {READY: 0, DONE: 10, EARLY: 11, WAITING: 12}


def decide(now_et: dt.datetime, page_exists: bool, briefing_exists: bool) -> str:
    """What a fire should do right now. Pure; the loop below supplies the facts."""
    if page_exists:
        return DONE
    if now_et.time() < EARLIEST:
        return EARLY
    return READY if briefing_exists else WAITING


def briefing_path(weatherman: str, date: str) -> str:
    return os.path.join(weatherman, "briefings", f"{date}.md")


def page_path(date: str, site_root: str = HERE) -> str:
    return os.path.join(site_root, "site", "weather", f"{date}.html")


def pull(weatherman: str) -> None:
    """Best effort. A failed pull just means the next look sees the same tree."""
    subprocess.run(["git", "-C", weatherman, "pull", "--rebase", "-q"],
                   check=False, capture_output=True, timeout=120)


def wait(weatherman: str, minutes: float, interval: float = 60.0,
         now=eastern_now, sleep=time.sleep, pull_fn=pull,
         exists=os.path.exists, site_root: str = HERE) -> tuple[str, str]:
    """Poll for today's briefing for up to `minutes`. Returns (status, date)."""
    start = now()
    date = start.strftime("%Y-%m-%d")
    deadline = start + dt.timedelta(minutes=minutes)
    while True:
        status = decide(now(), exists(page_path(date, site_root)),
                        exists(briefing_path(weatherman, date)))
        if status != WAITING or now() >= deadline:
            return status, date
        sleep(interval)
        pull_fn(weatherman)


def main() -> int:
    config.use_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--weatherman", default=os.path.join(HERE, "..", "weatherman"),
                        help="path to the weatherman checkout (default ../weatherman)")
    parser.add_argument("--minutes", type=float, default=9.0,
                        help="longest this call waits for the briefing (default 9)")
    args = parser.parse_args()

    pull(args.weatherman)
    status, date = wait(args.weatherman, args.minutes)
    detail = f" {briefing_path(args.weatherman, date)}" if status == READY else ""
    print(f"{status} {date}{detail}")
    print(f"wait_for_briefing: {status} at {eastern_now():%H:%M} ET", file=sys.stderr)
    return EXIT_CODES[status]


if __name__ == "__main__":
    sys.exit(main())
