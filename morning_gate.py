"""The 5:30 ET start, on both sides of the clock change, and the 6:55 wake.

    python morning_gate.py         # the routine's FIRST command
    python morning_gate.py wake    # the last thing before ending the first turn

THE GATE. The routine's cron is `30 9,10 * * *` UTC all year, so it fires
twice every morning and this decides each fire:

                     09:30 UTC          10:30 UTC
    EDT (Mar-Nov)    5:30 AM  GO        6:30 AM  DONE
    EST (Nov-Mar)    4:30 AM  EARLY     5:30 AM  GO

It prints ONE line and exits with its code:

    GO <date>       0   this fire builds today's papers; the claim is pushed
    DONE <date>    10   an earlier fire already claimed today: stop now
    EARLY <date>   11   before 5:15 ET (the winter 4:30 fire): stop now
    GIT ERROR       1   the claim could not be read or pushed: carry on as GO
                        and say so in the report (a fire that cannot reach
                        GitHub cannot publish either, so there is no second
                        paper to collide with)

The claim is `editions/claim.json`, committed on top of a fresh fetch of
origin/main and pushed straight there. Git refuses a push that is not a
fast-forward, so two fires racing for the same morning cannot both win.

THE WAKE. The digest posts at 7:00 and Jim Claudtore at 7:15, both held,
from a send_later wake at 6:55 ET. This prints when to set it:

    WAKE 6:55 AM ET = 2026-10-14T10:55:00Z (in 2513 s)
    WAKE 6:40 AM ET = ... INTERIM ...   more than 65 minutes away: set it
                                        for the time shown, and on waking
                                        run `morning_gate.py wake` again
    NOW                                 6:53 or later: do the wake steps
                                        now, in this turn

The longest send_later on record is 68 minutes (2026-10-13: set at 5:50 for
6:58, delivered at 6:59), so no single wake is asked to go further than 65.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import secrets
import subprocess
import sys
import tempfile
import time

import config
from hold_until import eastern_now

HERE = os.path.dirname(os.path.abspath(__file__))
CLAIM_REL = "editions/claim.json"
LONGEST_WAKE = dt.timedelta(minutes=65)
WAKE_NOW_WITHIN = dt.timedelta(minutes=2)

GO, DONE, EARLY, GIT_ERROR = "GO", "DONE", "EARLY", "GIT ERROR"
EXIT_CODES = {GO: 0, DONE: 10, EARLY: 11, GIT_ERROR: 1}


class GitError(RuntimeError):
    pass


def _clock(when_et: dt.datetime) -> str:
    hour = when_et.hour % 12 or 12
    return f"{hour}:{when_et.minute:02d} {'AM' if when_et.hour < 12 else 'PM'}"


def _hhmm(text: str) -> dt.time:
    hour, minute = (int(p) for p in text.split(":"))
    return dt.time(hour, minute)


# ------------------------------------------------------------------ decisions

def decide(now_et: dt.datetime, claim_text: str | None) -> str:
    """GO, DONE or EARLY for a fire at `now_et`, given origin's claim file."""
    if now_et.time() < _hhmm(config.GATE_OPENS_ET):
        return EARLY
    try:
        claimed = json.loads(claim_text).get("date") if claim_text else None
    except (ValueError, AttributeError):
        claimed = None
    return DONE if claimed == now_et.strftime("%Y-%m-%d") else GO


def claim_text(now_utc: dt.datetime, now_et: dt.datetime) -> str:
    # The token keeps two claims made in the same second from being the same
    # commit: git would accept the second push as a no-op and both would win.
    return json.dumps({
        "date": now_et.strftime("%Y-%m-%d"),
        "claimed_at": now_utc.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "started_et": f"{_clock(now_et)} ET",
        "token": secrets.token_hex(4),
    }, indent=1) + "\n"


def wake_target(now_utc: dt.datetime) -> tuple[str, dt.datetime | None, bool]:
    """('NOW', None, False) or ('WAKE', utc_instant, interim)."""
    now_et = eastern_now(now_utc)
    date_iso = now_et.strftime("%Y-%m-%d")
    goal_et = dt.datetime.combine(now_et.date(), _hhmm(config.WAKE_ET))
    goal = (goal_et + dt.timedelta(hours=config.et_utc_offset_hours(date_iso))).replace(
        tzinfo=dt.timezone.utc)
    left = goal - now_utc
    if left <= WAKE_NOW_WITHIN:
        return "NOW", None, False
    if left > LONGEST_WAKE:
        return "WAKE", now_utc + LONGEST_WAKE, True
    return "WAKE", goal, False


def wake_line(now_utc: dt.datetime) -> str:
    status, when, interim = wake_target(now_utc)
    if status == "NOW":
        return (f"NOW: it is {_clock(eastern_now(now_utc))} ET and the {config.WAKE_ET} "
                "wake has come. Do the wake steps now, in this turn.")
    seconds = int((when - now_utc).total_seconds())
    line = (f"WAKE {_clock(eastern_now(when))} ET = "
            f"{when.strftime('%Y-%m-%dT%H:%M:%SZ')} (in {seconds} s)")
    if interim:
        line += (f" INTERIM: {config.WAKE_ET} ET is more than 65 minutes away. Set this "
                 "wake, and when it arrives run `python morning_gate.py wake` again.")
    return line


# ------------------------------------------------------------------ git

def _git(repo: str, *args: str, data: bytes | None = None, env: dict | None = None,
         check: bool = True) -> subprocess.CompletedProcess:
    done = subprocess.run(["git", "-C", repo, *args], input=data, capture_output=True,
                          env=env, timeout=120)
    if check and done.returncode != 0:
        message = (done.stderr or done.stdout).decode("utf-8", "replace").strip()
        raise GitError(f"git {args[0]}: {message[:300]}")
    return done


def _out(done: subprocess.CompletedProcess) -> str:
    return done.stdout.decode("utf-8", "replace").strip()


def _fetch(repo: str, attempts: int = 3, sleep=time.sleep) -> str:
    """origin/main's commit, riding out a GitHub blip of a few seconds."""
    for attempt in range(attempts):
        try:
            _git(repo, "fetch", "-q", "origin", "main")
            break
        except (GitError, subprocess.TimeoutExpired):
            if attempt == attempts - 1:
                raise
            sleep(5 * (attempt + 1))
    return _out(_git(repo, "rev-parse", "FETCH_HEAD"))


def _show(repo: str, rev: str, rel: str) -> str | None:
    if _git(repo, "cat-file", "-e", f"{rev}:{rel}", check=False).returncode != 0:
        return None
    return _git(repo, "cat-file", "blob", f"{rev}:{rel}").stdout.decode("utf-8")


def _identity(repo: str) -> dict:
    env = dict(os.environ)
    if not _out(_git(repo, "config", "user.email", check=False)):
        for key, value in (("GIT_AUTHOR_NAME", "Claude"), ("GIT_COMMITTER_NAME", "Claude"),
                           ("GIT_AUTHOR_EMAIL", "noreply@anthropic.com"),
                           ("GIT_COMMITTER_EMAIL", "noreply@anthropic.com")):
            env.setdefault(key, value)
    return env


def _commit_file(repo: str, base: str, rel: str, content: str, message: str) -> str:
    """A commit on top of `base` changing only `rel`. Touches no checkout."""
    blob = _out(_git(repo, "hash-object", "-w", "--stdin", data=content.encode("utf-8")))
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index"))
        _git(repo, "read-tree", base, env=env)
        _git(repo, "update-index", "--add", "--cacheinfo", f"100644,{blob},{rel}", env=env)
        tree = _out(_git(repo, "write-tree", env=env))
    return _out(_git(repo, "commit-tree", tree, "-p", base, "-m", message, env=_identity(repo)))


def _sync(repo: str, rel: str, commit: str, content: str) -> None:
    """Bring a clean checkout onto the pushed commit; else just write the file."""
    path = os.path.join(repo, *rel.split("/"))
    status = _out(_git(repo, "status", "--porcelain", "--untracked-files=no", check=False))
    dirty = [line[3:].strip() for line in status.splitlines() if line.strip()]
    if all(p == rel for p in dirty):
        if _git(repo, "ls-files", "--error-unmatch", rel, check=False).returncode == 0:
            _git(repo, "checkout", "-q", "--", rel, check=False)
        elif os.path.exists(path):
            os.remove(path)
        on_branch = _git(repo, "symbolic-ref", "-q", "HEAD", check=False).returncode == 0
        moved = (_git(repo, "merge", "-q", "--ff-only", commit, check=False) if on_branch
                 else _git(repo, "checkout", "-q", "--detach", commit, check=False))
        if moved.returncode == 0 and os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                if f.read() == content:
                    return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def gate(root: str, now_utc: dt.datetime, sleep=time.sleep, attempts: int = 6) -> tuple[str, str, str]:
    """(status, date, detail) for this fire; pushes the claim on GO."""
    now_et = eastern_now(now_utc)
    date_iso = now_et.strftime("%Y-%m-%d")
    if decide(now_et, None) == EARLY:
        return EARLY, date_iso, (f"it is {_clock(now_et)} ET; the paper starts at the "
                                 "5:30 fire. Stop now.")
    for attempt in range(attempts):
        try:
            base = _fetch(root, sleep=sleep)
        except (GitError, subprocess.TimeoutExpired):
            # The sandbox cloned origin when this fire started, so a claim
            # the 5:30 fire pushed is already on disk. Reading it keeps a
            # summer 6:30 fire from building a second paper on a bad fetch.
            local = _show(root, "HEAD", CLAIM_REL)
            if decide(now_et, local) == DONE:
                started = json.loads(local).get("started_et") or "an earlier fire"
                return DONE, date_iso, (f"the {started} fire already has today's papers "
                                        "(read from this checkout; origin did not answer). "
                                        "Stop now.")
            raise
        current = _show(root, base, CLAIM_REL)
        if decide(now_et, current) == DONE:
            started = (json.loads(current).get("started_et") or "an earlier fire")
            return DONE, date_iso, f"the {started} fire already has today's papers. Stop now."
        text = claim_text(now_utc, now_et)
        commit = _commit_file(root, base, CLAIM_REL, text,
                              f"Claim {date_iso}: the {_clock(now_et)} ET fire builds today's papers")
        if _git(root, "push", "-q", "origin", f"{commit}:refs/heads/main",
                check=False).returncode == 0:
            _sync(root, CLAIM_REL, commit, text)
            return GO, date_iso, f"the {_clock(now_et)} ET fire builds today's papers"
        sleep(min(5 * (attempt + 1), 30))
    raise GitError(f"origin/main refused the claim {attempts} times")


def main(argv: list[str] | None = None) -> int:
    config.use_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", nargs="?", choices=("gate", "wake"), default="gate")
    parser.add_argument("--root", default=HERE, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    now_utc = dt.datetime.now(dt.timezone.utc)

    if args.command == "wake":
        line = wake_line(now_utc)
        print(line)
        return 0
    try:
        status, date_iso, detail = gate(args.root, now_utc)
    except (GitError, subprocess.TimeoutExpired) as exc:
        print(f"{GIT_ERROR} {eastern_now(now_utc):%Y-%m-%d}: {exc}. Carry on as GO "
              "and say so in your report.")
        return EXIT_CODES[GIT_ERROR]
    print(f"{status} {date_iso}: {detail}")
    return EXIT_CODES[status]


if __name__ == "__main__":
    sys.exit(main())
