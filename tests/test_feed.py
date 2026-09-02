"""site/feed.xml and the back-issues page, built from the same archive.

The feed is one item per edition — dated permalink, dek as description,
7:00 ET pubDate — written by write_site every morning and by --all. The
archive page carries the same two nav rows every other page has.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET

import config
import render_edition as r

ENTRIES = [
    {"date": "2026-09-02", "number": 29, "volume": "I",
     "headline": "U.S. widens strikes on Iran; Tehran answers at bases in three countries",
     "dek": "Iran says one strike hit a wedding near the Strait of Hormuz, killing at least 5."},
    {"date": "2026-08-27", "number": 23, "volume": "I",
     "headline": "A headline with an ampersand & a <tag>", "dek": ""},
    {"date": "2026-11-02", "number": 90, "volume": "I",
     "headline": "Standard time", "dek": "After the clocks change."},
]


def _parsed(entries=ENTRIES):
    return ET.fromstring(r.render_feed_xml(entries).encode("utf-8"))


def test_feed_is_well_formed_rss_with_one_item_per_edition():
    root = _parsed()
    assert root.tag == "rss" and root.get("version") == "2.0"
    channel = root.find("channel")
    assert channel is not None
    assert len(channel.findall("item")) == len(ENTRIES)


def test_channel_links_home_and_items_link_dated_pages():
    channel = _parsed().find("channel")
    assert channel.findtext("link") == config.home_url()
    first = channel.findall("item")[0]
    assert first.findtext("link") == config.page_url("2026-09-02")
    assert first.findtext("guid") == config.page_url("2026-09-02")
    assert first.findtext("title").startswith("No. 29 ")
    assert first.findtext("description") == ENTRIES[0]["dek"]


def test_missing_dek_falls_back_to_the_headline_and_escapes():
    items = _parsed().find("channel").findall("item")
    assert items[1].findtext("description") == "A headline with an ampersand & a <tag>"
    # It survived a round trip through an XML parser, so it was escaped.


def test_pubdate_is_seven_et_on_both_sides_of_the_clock_change():
    items = _parsed().find("channel").findall("item")
    assert items[0].findtext("pubDate") == "Wed, 02 Sep 2026 07:00:00 -0400"
    assert items[2].findtext("pubDate") == "Mon, 02 Nov 2026 07:00:00 -0500"


def test_empty_archive_is_still_a_valid_feed():
    channel = _parsed([]).find("channel")
    assert channel.findall("item") == []
    assert channel.find("lastBuildDate") is None


def test_archive_page_carries_both_nav_rows_and_the_feed():
    html_out = r.render_archive_html(ENTRIES[:2])
    assert html_out.count('class="paper-nav"') == 1
    assert html_out.count('class="paper-nav paper-nav-foot"') == 1
    assert 'href="home.html"' in html_out
    assert 'href="sportsman/"' in html_out and 'href="weather/"' in html_out
    assert 'href="feed.xml"' in html_out


def test_print_stylesheet_hides_the_screen_furniture():
    blocks = r.load_blocks()
    style = r._extract_style(blocks["PAGE"])
    printed = style.split("@media print", 1)[1]
    assert ".paper-nav, .rule-anchor { display: none; }" in printed
