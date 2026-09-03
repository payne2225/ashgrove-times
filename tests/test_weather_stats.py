"""The weather page's numbers table, built from Jim's numbers line.

Since 2026-09-03 every location block in the briefing opens with a line Jim
copies from weatherman/briefing_stats.py. On the page that line becomes a
table above the prose; in a stack, one row per bold-prefixed place.
"""

from __future__ import annotations

import render_edition as r

LINE = "H: 95° / L: 73° · feels 103° at 2–3 PM · Hum 35% · rain 2% · AQI 97"


def test_the_line_parses_into_cells():
    row = r._wx_stats_row(LINE)
    assert row == {"place": "", "high": "95°", "low": "73°", "feels": "103° at 2–3 PM",
                   "rh": "35%", "rain": "2%", "aqi": "97"}


def test_prefixed_and_celsius_and_missing_segments():
    row = r._wx_stats_row("**Apple Grove** H: 21°C / L: 12°C · feels 19°C at 2 PM · Hum 80% · rain 84%")
    assert row["place"] == "Apple Grove" and row["high"] == "21°C" and row["aqi"] == ""
    assert r._wx_stats_row("H: — / L: 67° · Hum 50%")["high"] == "—"


def test_prose_is_not_a_stats_line():
    assert r._wx_stats_row("Highs near 95 with a feels-like of 103 by 2 PM.") is None
    assert r._wx_stats_row("Nothing fires before dark.") is None


def test_section_renders_the_table_above_the_prose():
    body = ("### 📍 Apple Grove — Nate & Ian\n" + LINE + "\n"
            "Nothing fires before dark. Hurricane tops the house by two.\n")
    doc = r._wx_parse(body)
    html_out = r._wx_section_html(r.load_blocks(), doc["sections"][0])
    assert html_out.count('<table class="wx-stats">') == 1
    assert html_out.index("wx-stats") < html_out.index("Nothing fires")
    assert "<th>Feels like</th>" in html_out and "<td>103° at 2–3 PM</td>" in html_out
    assert "<th>Place</th>" not in html_out
    assert "H: 95°" not in html_out          # the line is the table, not a paragraph


def test_a_stack_gets_one_row_per_place():
    body = ("### 📍 Apple Grove — Nate & Ian\n### 📍 Huntington — Trav\n"
            "**Apple Grove** H: 95° / L: 73° · feels 103° at 2–3 PM · Hum 35% · rain 2% · AQI 97\n"
            "**Huntington** H: 98° / L: 74° · feels 106° at 2 PM · Hum 33% · rain 2% · AQI 88\n"
            "One shared read for the river.\n")
    doc = r._wx_parse(body)
    html_out = r._wx_section_html(r.load_blocks(), doc["sections"][0])
    assert html_out.count("<tr>") == 3
    assert "<th>Place</th>" in html_out
    assert "<td>Apple Grove</td>" in html_out and "<td>Huntington</td>" in html_out
    assert "shared read" in html_out


def test_a_briefing_without_the_line_renders_as_before():
    body = "### 📍 Parkersburg — Pat\n95°F, humidity 46%, feels-like 101°F at 2 PM.\n"
    html_out = r._wx_section_html(r.load_blocks(), r._wx_parse(body)["sections"][0])
    assert "wx-stats" not in html_out and "<p>" in html_out


def test_the_whole_page_still_renders_with_the_table():
    md = ("---\ndate: 2026-09-03\n---\n# ☀️ Thursday, Sept. 3\n## Heat peaks\n\n"
          "### 📍 Apple Grove — Nate & Ian\n" + LINE + "\nThe read.\n\n"
          "> 🎯 **Confidence:** high\n-# NWS · Open-Meteo\n")
    page = r.render_weather_html("2026-09-03", md)
    assert 'class="wx-stats"' in page and "The read." in page
