"""Shared plumbing for the Times' tests.

Everything here is OFFLINE. The routine runs these before every deploy, and
a test that reached for the network would turn a flaky source into a
blocked paper. The two data files the validator cross-checks against
(out/stats.json, out/fishing.json) are gitignored and stale on any dev
machine, so each contract fixture ships its own copy under tests/fixtures/.
"""

from __future__ import annotations

import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURES = os.path.join(ROOT, "tests", "fixtures")

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def load_fixture(*parts: str) -> dict:
    with open(os.path.join(FIXTURES, *parts), encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fixture_edition():
    """A loader for a committed Times edition copy: fixture_edition('2026-08-27')."""
    return lambda date: load_fixture(f"{date}.json")


@pytest.fixture
def fixture_sportsman():
    """A loader for a committed Sports & Sportsman copy."""
    return lambda date: load_fixture("sportsman", f"{date}.json")
