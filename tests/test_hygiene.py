"""Source hygiene that has bitten this codebase before.

A shell-escaping bug once wrote eighteen literal backspace characters into
validate_edition.py where "\\b" word boundaries belonged, and a latent one
predating that had silently disabled the no-colon branch of the ET check for
weeks. A regex that stops matching is the only symptom, and it can take a
fortnight to notice. This test is the scan from the 2026-08-26 commit, run
every time.
"""

from __future__ import annotations

import os

import pytest

from conftest import ROOT

CONTROL = "\b\f\v\a\x00"


def _python_files() -> list[str]:
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "out", "site"}]
        out += [os.path.join(base, f) for f in files if f.endswith(".py")]
    return sorted(out)


@pytest.mark.parametrize("path", _python_files(), ids=lambda p: os.path.relpath(p, ROOT))
def test_no_control_characters(path):
    with open(path, encoding="utf-8") as f:
        source = f.read()
    bad = [(i + 1, repr(c)) for i, line in enumerate(source.splitlines())
           for c in line if c in CONTROL]
    assert not bad, f"{os.path.relpath(path, ROOT)} carries raw control characters at {bad[:5]}"


def test_no_webhook_urls_in_the_repo():
    """The repo is PUBLIC. A webhook lives in a prompt or a gitignored .env."""
    hits = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "out", "site", "assets"}]
        for name in files:
            if name == ".env" or not name.endswith((".py", ".md", ".json", ".yml", ".txt", ".html")):
                continue
            path = os.path.join(base, name)
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except (OSError, UnicodeDecodeError):
                continue
            if "discord.com/api/webhooks/" in text and "/api/webhooks/" in text:
                for line in text.splitlines():
                    if "discord.com/api/webhooks/" in line and any(ch.isdigit() for ch in line.split("webhooks/", 1)[1][:3]):
                        hits.append(os.path.relpath(path, ROOT))
                        break
    assert hits == [], f"live-looking webhook URLs in {hits}"
