"""The one morning message: what is in the paper, and where it is.

Since 2026-08-25 the channel gets a doorbell, not the paper. The digest must
stay ONE message, fit comfortably inside Discord's limits, link Home (which
reaches all three papers) rather than a dated permalink, and list sections
in the order a reader meets them on the page.
"""

from __future__ import annotations

import re

import config
import post_discord

DATE = "2026-08-27"
LABEL_RE = re.compile(r"\*\*(.+?)\*\*")


def _payload(fixture_edition, fixture_sportsman) -> dict:
    return post_discord.build_digest_payload(
        fixture_edition(DATE), config.home_url(),
        sportsman=fixture_sportsman(DATE), image_filename="ashgrove.png")


def _text_length(payload: dict) -> int:
    total = len(payload.get("content") or "")
    for embed in payload["embeds"]:
        total += len(embed.get("title") or "") + len(embed.get("description") or "")
        total += len((embed.get("footer") or {}).get("text") or "")
    return total


def test_digest_is_one_message_with_one_embed(fixture_edition, fixture_sportsman):
    payload = _payload(fixture_edition, fixture_sportsman)
    assert len(payload["embeds"]) == 1
    assert post_discord.validate_payload(payload) == []


def test_digest_is_short(fixture_edition, fixture_sportsman):
    payload = _payload(fixture_edition, fixture_sportsman)
    assert _text_length(payload) < 2000
    assert len(payload["content"]) <= config.CONTENT_LIMIT


def test_digest_links_home_not_the_dated_edition(fixture_edition, fixture_sportsman):
    payload = _payload(fixture_edition, fixture_sportsman)
    home = config.home_url()
    assert home.endswith("/home.html")
    assert home in payload["content"]
    assert payload["embeds"][0]["url"] == home
    assert home in payload["embeds"][0]["description"]
    assert config.page_url(DATE) not in payload["content"]
    assert config.page_url(DATE) not in payload["embeds"][0]["description"]


def test_digest_lists_sections_in_page_reading_order(fixture_edition, fixture_sportsman):
    edition = fixture_edition(DATE)
    payload = _payload(fixture_edition, fixture_sportsman)
    description = payload["embeds"][0]["description"]
    inside = description.split("__**Inside today**__", 1)[1]
    listed = [m.group(1) for m in LABEL_RE.finditer(inside)
              if m.group(1) != "Sports & Sportsman"]

    present = {s["id"] for s in edition["sections"]
               if any(b.get("headline") for b in s.get("briefs") or [])}
    expected = [meta["label"] for meta in config.sections_in_reading_order(DATE)
                if meta["id"] in present][:post_discord.DIGEST_MAX_INSIDE]
    assert listed == expected
    # The anchors — West Virginia and Canada — come last, as on the page.
    anchor_labels = [meta["label"] for meta in config.sections_for(DATE)
                     if meta["id"] in config.ANCHOR_SECTION_IDS]
    assert listed[-len(anchor_labels):] == anchor_labels


def test_digest_carries_the_sports_tease(fixture_edition, fixture_sportsman):
    payload = _payload(fixture_edition, fixture_sportsman)
    assert "**Sports & Sportsman**" in payload["embeds"][0]["description"]


def test_digest_without_a_url_has_no_link(fixture_edition):
    payload = post_discord.build_digest_payload(fixture_edition(DATE), None)
    assert "url" not in payload["embeds"][0]
    assert "http" not in payload["content"]
