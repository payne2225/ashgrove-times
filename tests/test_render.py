"""The sports page's one live read, and the snapshot that tames it.

Twice in one week re-rendering a sports page typeset another day's tides
into it, because _tide_table_html read out/fishing.json live. Since
2026-09-02 the morning render freezes that file to
editions/data/<date>.fishing.json and the table reads the snapshot first;
the live file is used only when no snapshot exists AND it carries the page's
own date. Everything else renders no table at all.
"""

from __future__ import annotations

import json
import os

import pytest

import render_edition as r


def _fishing(date: str, high: str) -> dict:
    return {
        "generated_at": f"{date}T05:40:00-04:00", "date": date,
        "williams": None, "ohio": [],
        "topsail": {
            "water": "Topsail Beach (surf and sound)",
            "tides": [{
                "station": "Hampstead", "station_id": "8657813", "side": "sound",
                "events": [
                    {"type": "low", "time_local": "1:39 AM", "height_ft": 0.9},
                    {"type": "high", "time_local": high, "height_ft": 3.3},
                    {"type": "low", "time_local": "1:40 PM", "height_ft": 0.5},
                    {"type": "high", "time_local": "7:59 PM", "height_ft": 4.1},
                ],
            }],
        },
        "errors": [],
    }


@pytest.fixture
def dirs(tmp_path, monkeypatch):
    data_dir = tmp_path / "data"
    out_dir = tmp_path / "out"
    data_dir.mkdir()
    out_dir.mkdir()
    monkeypatch.setattr(r, "DATA_DIR", str(data_dir))
    monkeypatch.setattr(r, "OUT_DIR", str(out_dir))
    monkeypatch.setattr(r, "LIVE_FISHING_PATH", str(out_dir / "fishing.json"))
    return data_dir, out_dir


def _put(path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def test_snapshot_wins_over_the_live_file(dirs):
    data_dir, out_dir = dirs
    _put(data_dir / "2026-08-26.fishing.json", _fishing("2026-08-26", "7:27 AM"))
    _put(out_dir / "fishing.json", _fishing("2026-09-02", "11:11 AM"))
    table = r._tide_table_html("2026-08-26")
    assert "7:27 AM" in table
    assert "11:11 AM" not in table


def test_live_file_is_used_only_on_its_own_day(dirs):
    _, out_dir = dirs
    _put(out_dir / "fishing.json", _fishing("2026-09-02", "11:11 AM"))
    assert "11:11 AM" in r._tide_table_html("2026-09-02")


def test_live_file_from_another_day_renders_no_table(dirs, capsys):
    _, out_dir = dirs
    _put(out_dir / "fishing.json", _fishing("2026-09-02", "11:11 AM"))
    assert r._tide_table_html("2026-08-26") == ""
    assert "tide table omitted" in capsys.readouterr().err


def test_no_data_at_all_renders_no_table(dirs):
    assert r._tide_table_html("2026-09-02") == ""


def test_snapshot_is_frozen_byte_for_byte_from_a_matching_live_file(dirs):
    data_dir, out_dir = dirs
    _put(out_dir / "fishing.json", _fishing("2026-09-02", "11:11 AM"))
    path = r.ensure_fishing_snapshot("2026-09-02")
    assert path == str(data_dir / "2026-09-02.fishing.json")
    with open(path, "rb") as a, open(out_dir / "fishing.json", "rb") as b:
        assert a.read() == b.read()


def test_snapshot_refuses_another_days_water(dirs, capsys):
    data_dir, out_dir = dirs
    _put(out_dir / "fishing.json", _fishing("2026-09-01", "11:11 AM"))
    assert r.ensure_fishing_snapshot("2026-09-02") is None
    assert not os.path.exists(data_dir / "2026-09-02.fishing.json")
    assert "no snapshot written" in capsys.readouterr().err


def test_snapshot_is_never_overwritten(dirs):
    data_dir, out_dir = dirs
    _put(data_dir / "2026-09-02.fishing.json", _fishing("2026-09-02", "7:27 AM"))
    _put(out_dir / "fishing.json", _fishing("2026-09-02", "11:11 AM"))
    r.ensure_fishing_snapshot("2026-09-02")
    with open(data_dir / "2026-09-02.fishing.json", encoding="utf-8") as f:
        assert "7:27 AM" in f.read()


def test_snapshot_without_a_live_file_is_none(dirs):
    assert r.ensure_fishing_snapshot("2026-09-02") is None
