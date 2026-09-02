"""post_discord.py's command line, dry-run only — nothing here touches Discord.

The routine's exact invocation is `--date <d> --digest --attach <png>
--not-before 07:00`; this runs the same entry point on a committed fixture
with --dry-run and --no-image and reads the payload it prints. It exists
because main() is the one function the tests could not otherwise reach, and
it was rewritten from scratch when the full-embed path was retired.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

from conftest import FIXTURES, ROOT

import config

DATE = "2026-08-27"


def _run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, os.path.join(ROOT, "post_discord.py"), *args],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120,
    )


@pytest.fixture(scope="module")
def dry_run():
    return _run("--date", DATE, "--edition", os.path.join(FIXTURES, f"{DATE}.json"),
                "--digest-sportsman", os.path.join(FIXTURES, "sportsman", f"{DATE}.json"),
                "--digest", "--dry-run", "--no-image")


def _payload(result: subprocess.CompletedProcess) -> dict:
    body = result.stdout.split("--- message 1 of 1 ---", 1)[1]
    body = body.split("--- attachment:", 1)[0]
    return json.loads(body)


def test_dry_run_exits_clean(dry_run):
    assert dry_run.returncode == 0, dry_run.stderr
    assert "--- message 1 of 1 ---" in dry_run.stdout
    assert "--- attachment: none ---" in dry_run.stdout


def test_dry_run_is_one_digest_linking_home(dry_run):
    payload = _payload(dry_run)
    assert payload["username"] == config.WEBHOOK_USERNAME
    assert len(payload["embeds"]) == 1
    assert payload["embeds"][0]["url"] == config.home_url()
    assert "Sports & Sportsman" in payload["embeds"][0]["description"]
    assert "attachments" not in payload


def test_dry_run_reports_and_writes_nothing_to_the_ledger(dry_run):
    assert "DEGRADED: image suppressed by flag" in dry_run.stderr
    assert "payload written to" in dry_run.stderr
    # --dry-run must never post or mark the ledger; the fixture date is a
    # real archived edition and its row must stay exactly as the routine
    # left it.
    record = config.edition_record(DATE)
    assert record and record.get("posted") is True


def test_the_digest_flag_is_optional():
    result = _run("--date", DATE, "--edition", os.path.join(FIXTURES, f"{DATE}.json"),
                  "--dry-run", "--no-image")
    assert result.returncode == 0, result.stderr
    assert "--- message 1 of 1 ---" in result.stdout


@pytest.mark.parametrize("flag", ["--text", "--split", "--sportsman", "--backfill-link", "--page-url"])
def test_retired_flags_are_gone(flag):
    args = ["--date", DATE, "--dry-run", flag]
    if flag == "--page-url":
        args.append("https://example.invalid/")
    result = _run(*args)
    assert result.returncode == 2
    assert "unrecognized arguments" in result.stderr
