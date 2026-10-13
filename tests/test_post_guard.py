"""post_discord.py: the digest goes out only on the Times webhook, and a long
hold is chunked so no single cloud tool call outlives its ten minutes."""

from __future__ import annotations

import datetime as dt
import os
import subprocess
import sys

from conftest import FIXTURES, ROOT

import post_discord as pd

# Split so tests/test_hygiene.py's live-webhook scan never mistakes it.
OTHER = "https://discord.com/api/webhooks/" + "424242/not-a-real-token"


def test_any_other_webhook_is_refused_without_echoing_it():
    problem = pd.webhook_problem(OTHER)
    assert "not the Times webhook" in problem
    assert "424242" not in problem and "not-a-real-token" not in problem
    assert pd.webhook_problem("https://example.com/hook") is not None


def test_a_dry_run_with_the_wrong_webhook_exits_3_and_sends_nothing(tmp_path):
    env = dict(os.environ, DISCORD_WEBHOOK_URL=OTHER)
    done = subprocess.run(
        [sys.executable, os.path.join(ROOT, "post_discord.py"), "--date", "2026-08-27",
         "--edition", os.path.join(FIXTURES, "2026-08-27.json"),
         "--digest-sportsman", os.path.join(FIXTURES, "sportsman", "2026-08-27.json"),
         "--digest", "--dry-run", "--no-image"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=120, env=env)
    assert done.returncode == pd.WRONG_WEBHOOK_EXIT
    assert "not the Times webhook" in done.stderr
    assert "--- message 1 of 1 ---" not in done.stdout


class _Clock:
    def __init__(self, start):
        self.t = start
        self.slept = []

    def now(self):
        return self.t

    def sleep(self, seconds):
        self.slept.append(seconds)
        self.t += dt.timedelta(seconds=seconds)


def test_a_long_hold_is_chunked_and_still_lands_at_seven():
    clock = _Clock(dt.datetime(2026, 10, 14, 6, 45))
    results = [pd._hold_until("07:00", 540, now=clock.now, sleep=clock.sleep)
               for _ in range(2)]
    assert [ready for _, _, ready in results] == [False, True]
    assert "Nothing was sent" in results[0][1]
    assert clock.now() == dt.datetime(2026, 10, 14, 7, 0)
    assert max(clock.slept) <= 540


def test_the_usual_wake_holds_in_one_call():
    clock = _Clock(dt.datetime(2026, 10, 14, 6, 57))
    held, _, ready = pd._hold_until("07:00", 540, now=clock.now, sleep=clock.sleep)
    assert held and ready and clock.slept == [180]
    late = _Clock(dt.datetime(2026, 10, 14, 7, 4))
    assert pd._hold_until("07:00", 540, now=late.now, sleep=late.sleep)[2] is True
    assert late.slept == []
