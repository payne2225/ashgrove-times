"""wait_for_briefing.py: publish once, right behind Jim, on the Eastern date."""

from __future__ import annotations

import datetime as dt

import wait_for_briefing as w


def _et(hh: int, mm: int, day: int = 5) -> dt.datetime:
    return dt.datetime(2026, 10, day, hh, mm)


def test_a_published_page_stops_every_later_fire():
    assert w.decide(_et(8, 17), page_exists=True, briefing_exists=True) == w.DONE
    assert w.decide(_et(6, 17), page_exists=True, briefing_exists=False) == w.DONE


def test_before_ten_past_seven_is_too_early_whatever_is_on_disk():
    # 6:17 EST is the winter first fire; Jim has not posted, let alone archived.
    assert w.decide(_et(6, 17), page_exists=False, briefing_exists=False) == w.EARLY
    assert w.decide(_et(7, 9), page_exists=False, briefing_exists=True) == w.EARLY


def test_ready_only_when_todays_briefing_exists():
    assert w.decide(_et(7, 17), page_exists=False, briefing_exists=True) == w.READY
    assert w.decide(_et(7, 17), page_exists=False, briefing_exists=False) == w.WAITING


class _Clock:
    def __init__(self, start: dt.datetime):
        self.t = start

    def now(self) -> dt.datetime:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.t += dt.timedelta(seconds=seconds)


def test_wait_returns_ready_when_the_archive_lands_mid_poll():
    clock = _Clock(_et(7, 17))
    landed = _et(7, 21)
    pulls = []

    def exists(path: str) -> bool:
        if path.endswith("2026-10-05.md"):
            return clock.now() >= landed
        return False

    status, date = w.wait("wm", minutes=9, now=clock.now, sleep=clock.sleep,
                          pull_fn=pulls.append, exists=exists, site_root="site")
    assert (status, date) == (w.READY, "2026-10-05")
    assert clock.now() == landed and len(pulls) == 4


def test_wait_gives_up_after_its_minutes_and_says_waiting():
    clock = _Clock(_et(7, 17))
    status, _ = w.wait("wm", minutes=9, now=clock.now, sleep=clock.sleep,
                       pull_fn=lambda _: None, exists=lambda _: False, site_root="site")
    assert status == w.WAITING
    assert clock.now() - _et(7, 17) <= dt.timedelta(minutes=10)


def test_yesterdays_briefing_is_never_todays():
    clock = _Clock(_et(7, 30))
    status, date = w.wait("wm", minutes=0, now=clock.now, sleep=clock.sleep,
                          pull_fn=lambda _: None,
                          exists=lambda p: p.endswith("2026-10-04.md"), site_root="site")
    assert (status, date) == (w.WAITING, "2026-10-05")


def test_cron_fires_land_where_the_docstring_says():
    # 17 11,12,13 * * * on both sides of the 2026-11-01 change.
    from hold_until import eastern_now
    utc = dt.timezone.utc
    summer = [eastern_now(dt.datetime(2026, 10, 31, h, 17, tzinfo=utc)).strftime("%H:%M")
              for h in (11, 12, 13)]
    winter = [eastern_now(dt.datetime(2026, 11, 1, h, 17, tzinfo=utc)).strftime("%H:%M")
              for h in (11, 12, 13)]
    assert summer == ["07:17", "08:17", "09:17"]
    assert winter == ["06:17", "07:17", "08:17"]


def test_pull_sees_a_new_briefing_from_a_detached_checkout(tmp_path):
    # 2026-10-08: the sandbox cloned weatherman onto a detached HEAD, where
    # `git pull` fails, so two nine-minute waits never saw a briefing that
    # had been on origin/main since 7:32 ET. The page went up at 8:29.
    import subprocess

    def git(*args, cwd):
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t",
                        "-c", "commit.gpgsign=false", *args],
                       cwd=cwd, check=True, capture_output=True)

    origin, seed, checkout = tmp_path / "origin.git", tmp_path / "seed", tmp_path / "weatherman"
    git("init", "-q", "--bare", "-b", "main", str(origin), cwd=tmp_path)
    git("clone", "-q", str(origin), str(seed), cwd=tmp_path)
    (seed / "briefings").mkdir()
    (seed / "briefings" / "2026-10-07.md").write_text("yesterday")
    git("add", "-A", cwd=seed)
    git("commit", "-q", "-m", "Briefing 2026-10-07", cwd=seed)
    git("push", "-q", "origin", "HEAD:main", cwd=seed)

    git("clone", "-q", str(origin), str(checkout), cwd=tmp_path)
    git("checkout", "-q", "--detach", cwd=checkout)  # how the sandbox lands

    (seed / "briefings" / "2026-10-08.md").write_text("today")
    git("add", "-A", cwd=seed)
    git("commit", "-q", "-m", "Briefing 2026-10-08", cwd=seed)
    git("push", "-q", "origin", "HEAD:main", cwd=seed)

    assert not (checkout / "briefings" / "2026-10-08.md").exists()
    w.pull(str(checkout))
    assert (checkout / "briefings" / "2026-10-08.md").read_text() == "today"
