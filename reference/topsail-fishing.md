<!-- Ported verbatim from weatherman/instructions/topsail-fishing.md on
     2026-08-21, when Nate moved the whole Topsail beach-and-inlet report
     from Jim Claudtore's briefing into Sports & Sportsman. Jim's copy
     stays where it is; THIS copy is the one the S&S routine reads, since
     the morning routine only has the ashgrove-times repo checked out. -->

# Topsail Beach / New Topsail Inlet — Fishing Reference

Standing knowledge so the daily briefing doesn't re-research the basics
every morning. Researched and adversarially verified 2026-08-05.
Live conditions still come from the report sources below — this file is
the frame, not the news.

## Where to get the actual report (in this order)

**1. Fisherman's Post — Topsail/Sneads Ferry (PRIMARY).**
Feed: `https://www.fishermanspost.com/category/fishing-reports/topsail-sneads-ferry/feed/`
Take `item[0]`, read its `<pubDate>` as the authoritative publish date,
follow its `<link>`, fetch that article, extract the per-shop blocks —
East Coast Sports, Native Son, Spring Tide, Carolina Flats, Plan 9
Charters, South End Adventures — and **especially the Jolly Roger Pier
and Surf City Pier paragraphs**, which are the most valuable
hyper-local content in the whole pipeline (they name actual fish
caught off the actual piers).

Do NOT construct slugs like `/topsail-sneads-ferry-{month}-{year}/`.
The feed distinguishes "not published yet" from "the naming changed";
a guessed slug 404 cannot.

**2. Coastal Angler (SECONDARY / fallback).**
`https://coastalanglermag.com/author/coastalnc/feed/` — filter item
titles starting with "Topsail", take the newest. Use as a second
independent voice or when the Fisherman's Post edition is late. Do not
use `/tag/topsail/feed/`; it returns 200 with zero items.

**3. WebSearch — DISCOVERY ONLY, NEVER A SOURCE OF FACT.**
Testing found WebSearch confidently surfacing "current" conditions
that traced back to pages from **2010 and 2007**. So: search only to
find candidate URLs, then fetch the page and require a machine-readable
date (JSON-LD `datePublished`, `article:published_time`, or
`og:updated_time`) **within 21 days**. No date found = REJECT. Never
text-parse a date out of body copy to rescue a source.

## The honesty rule that matters most

**These reports are MONTHLY, not daily.** Compute the age in days from
`pubDate` on every run and say it out loud: "monthly report, published
Aug 3 — 2 days old." **Never render a monthly report as today's
conditions.** Only the NOAA tide data may be presented as current. If
no source passes the date gate, say the report's stale or missing and
fall back to the seasonal calendar below, clearly labeled as the
season's pattern rather than a live report.

## Where they actually fish (ground truth, 2026-08-05)

Nate: **the sound roughly 2 nautical miles north of New Topsail Inlet**,
up toward Kings Creek / Banks Channel — inside the island, not the
oceanfront. They've observed their tide running about an hour behind
the inlet, and that checks out against the data.

So the briefing **leads with the sound (Hampstead) times** — their
water — and gives the ocean/inlet times as the familiar reference.

**The lag is not uniform**, and this is the useful part: comparing the
two stations, **highs run ~70–75 min behind the inlet, lows ~95–100
min**. A shallow sound drains slower than it fills. Practical
consequence: the falling-tide window at their spot is *longer* than a
flat "add an hour" implies — and since red drum want the last of the
fall, that stretched ebb is exactly the window they care about. The
`lag_summary` entry in the tide data computes both numbers fresh each
day rather than assuming.

## Tide stage is the whole game

New Topsail Inlet is the funnel that drains and refills every marsh and
bay from the south end of the island up toward Surf City. Huge volumes
of water — and bait — move through on every tide change. **Slack water
at the inlet is dead water; never plan to fish it at slack high or
slack low.** Local guide framing: "It's all about catching that window
of moving water. The fishing can go from zero to 60 in seconds."

- **Red drum — last of the falling tide.** The strongest tide
  preference on the island: falling water pulls shrimp and baitfish out
  of the marsh grass into creek channels where drum ambush them. Fan-
  cast cut menhaden a couple feet off the channel edge. Secondary
  window: high tide, when drum push into flooded grass and dock flats.
- **Flounder — moving water against structure**, either direction.
  Ambush feeders on current seams: bridge pilings, inlet channel edges,
  creek mouths.
- **Speckled trout — any moving tide, but time of day wins in summer.**
  Dawn and dusk override tide stage in August heat. Topwater at first
  light, popping cork with live shrimp to locate fish.
- **Tarpon — falling tide, low light.**
- **Spanish mackerel / bluefish — calm mornings, bait pods tight to the
  beach.** Look for diving birds; Gotcha plugs and metal jigs.
- **Sheepshead — tight to structure**, any moving water: pilings,
  oyster beds, barnacles, fiddler crabs.

**Moon ties in:** new and full moons = spring tides (bigger swings,
harder current through the inlet, more bait moving); quarter moons =
neap tides (gentler). `astro.moon` in the data feeds this directly.

## Seasonal calendar (what's targetable when)

| Month | Running |
|---|---|
| Jan | Speckled trout, red drum (winter schools), black drum, sporadic sea mullet |
| Feb | Red drum (schooled), black drum |
| Mar | Sea mullet/whiting arrive, black drum, red drum, first bluefish |
| Apr | Sea mullet, pompano arriving, bluefish, black drum, red drum, trout, Spanish (late) |
| May | Cobia (opens May 1), Spanish, king mackerel starting, pompano, sheepshead |
| Jun | Cobia peak, Spanish, kings, sheepshead, pompano, red drum, first tarpon |
| Jul | Tarpon arrive on the full moon, Spanish, kings, sheepshead, pompano, trout |
| **Aug** | **Red drum (excellent), Spanish, bluefish, trout, sheepshead, sea mullet/whiting, black drum, kings, tarpon (peak), pompano** |
| Sep | Bull red drum, spot run begins, Spanish, kings, trout, sea mullet |
| Oct | Spot (peak run), red drum, trout, bluefish, sea mullet, black drum |
| Nov | Red drum, speckled trout (prime), bluefish, spot, sea mullet, blow toads |
| Dec | Speckled trout, red drum, black drum, sea mullet tapering |

## Regulations worth not getting wrong

Rules change — **if a briefing states a limit or a season, it must come
from that run's fetched report or a current NCDMF check, not from this
file's memory.** As of the 2026-08-05 research:

- **Flounder — catch-and-release ONLY** for most of the year; the 2026
  harvest window was Sept 1–14 only. This is the one people get wrong;
  never imply flounder are in the cooler outside that window.
- **Speckled trout** — harvest reopened July 1, 2026 after the February
  cold-stun closure. 14–20" slot, 3/day.
- **Red drum** — 18–27" slot, 1/day, harvest must be reported.
- **Sheepshead** — 10" fork length, 10/day.
- **Spanish mackerel** — 12" fork length, 15/day. **Bluefish** — no
  minimum, 5/day. **Sea mullet** — no size or creel limit.
- **Tarpon** — release only.

When in doubt, say "check current NCDMF regs" rather than stating a
number you aren't sure of. Nobody wants a citation because a weather
bot was confident.
