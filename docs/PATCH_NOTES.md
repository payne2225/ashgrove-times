# Patch Notes — The Ashgrove Times

Running changelog. Dated entries, newest first. Touched only when
behavior changes, not every edition — the per-day record lives in
`editions/index.json`, and degraded runs go in `docs/FAILURES.md`.

## 2026-09-02 — the archive is safe to re-render

Full-pass item 2. The sports page's tide table was the one live read on any
page — `_tide_table_html()` read `out/fishing.json`, gitignored and
overwritten by every fetch — and twice in a week that typeset another day's
tides into a published page. The date guard that stopped it (08-26) also
meant no layout change could ever reach a back issue: the whole archive
still wore the grid the flowed layout replaced.

- **`editions/data/<date>.fishing.json`** — `render_edition.py --sportsman`
  now freezes `out/fishing.json` beside the edition the first time it
  renders a day's page (`ensure_fishing_snapshot`; bytes copied, never
  re-serialised, never overwritten, and only when the live file carries the
  day's own date). The routine's `git add -A` commits it with the edition.
  `sportsman.md` §4 and §5 and `routine.md` say so.
- **The tide table reads the snapshot first.** The live file is used only
  when there is no snapshot AND its date matches the page — the morning
  render itself. Any other combination renders no table and says so.
- **`render_edition.py --all`** re-renders every Times page (nothing live
  there), every sports page that HAS a snapshot, and every weather page
  whose briefing sits in the `../weatherman` checkout (`--weatherman DIR`),
  and **refuses the rest by name**. `today.html` and the index bookmarks are
  written from the newest edition only; the archive index is rebuilt once.
- **Run once.** 29 Times pages and 15 weather pages re-rendered; all 19
  sports pages skipped by name, as they must be — no snapshot exists before
  2026-09-03, and those pages keep their committed HTML for good. The 21
  Times back issues from 08-05 to 08-25 took the flowed columns, the anchor
  rule and the foot nav; the pages from 08-26 on re-rendered byte-identical,
  which is the determinism check. Weather pages 08-19 to 08-25 took the
  08-25 newspaper layout.
- **Verified** against today's paper: a fresh fetch (dated 2026-09-02)
  re-rendered the 09-02 sports page with a tide table byte-identical to the
  routine's committed page, on the fallback path and again through a
  snapshot. That snapshot was then deleted — a 10 a.m. fetch is not the
  5:30 water the validator checked, and a snapshot is only ever the day's
  own file. `tests/test_render.py` covers all four branches.

## 2026-09-02 — the validator gets tests, and the tests find the archive broken

Full-pass item 1 (`docs/HANDOFF-FULL-PASS-2026-09-02.md`). `validate_edition.py`
was 3,405 lines of every rule the paper has, verified by hand in a terminal
after each change. Now `tests/` runs offline under pytest — 74 tests — and
`.github/workflows/pages.yml` runs them as a `test` job the deploy depends
on. **A red validator blocks a deploy.** The workflow now triggers on every
push to main rather than only `site/**`, so a validator change is tested
even when no page moved; the deploy after a docs-only push republishes the
same site, which is idempotent.

- `tests/test_direction.py` — the eight result-direction phrasings from the
  08-26 fix, plus `_sm_check_result`'s score and date-scoping rules.
- `tests/test_attribution.py` — Topsail water temperature: no temp,
  uncredited, credited, credited to the wrong station, the bare-number
  heuristic, the date scope; and Sports & Sportsman's `working`-field
  exclusion ("an 85% waxing gibbous" is not a temperature).
- `tests/test_standings.py` — the 08-24 ordinal contradiction and the
  games-back advisory, per field, with "last" and the ambiguous-Cincinnati
  silence.
- `tests/test_contracts.py` — one committed edition per contract date
  (08-05, 08-15, 08-25, 08-26, 08-27, plus the four sportsman editions and
  both fixtures) run through the CLI exactly as the routine runs it, each
  with its own `out/`-style stats and fishing file under `tests/fixtures/`,
  reconstructed from what the edition printed. A fixture must be
  byte-identical to its `editions/` original, so the two cannot drift.
- `tests/test_notebook.py` — never-empty away/hotspots with and without the
  note, promoted regions refused after 08-26 and accepted before, the away
  cap, the retired fishing block.
- `tests/test_digest.py` — one message, under 2,000 chars, links Home not
  the dated page, sections in `config.sections_in_reading_order`.
- `tests/test_hygiene.py` — the control-character scan from the 08-26
  commit over every `.py`, and a live-webhook scan over the public repo.

**The first run found the archive already broken.** Eight editions
(2026-08-05 through 08-12) and `editions/_fixture.json` had been failing
today's validator since 2026-08-26, unnoticed, on two rules that were never
date-scoped:

- The Away Desk cap was `len(AWAY_REGION_IDS)`, which fell from three to one
  when Prince George and Topsail were promoted; the 08-05 edition carried
  all three and was right to. `config.wv_away_max_for(date)` now returns
  the roster of the day.
- The Topsail credit demanded "Beaufort" of lines that printed Wrightsville
  Beach when Wrightsville Beach was the station.
  `config.TOPSAIL_TEMP_STATION_CHANGED_ON = "2026-08-25"` and
  `TOPSAIL_TEMP_PRIOR_STATION_NAME` record the change;
  `topsail_temp_station_name_for(date)` is what both gates ask.

Neither change touches what today's edition must do. The whole archive —
29 Times editions, 19 sportsman editions, both fixtures — validates offline.

**Also found by the tests:** the bare present tense was missing from the
direction reader's verb list, so "Padres blank the Pirates 3-0" (08-27)
was never read at all. `blank`, `hold off`, `overcome` and `outlast` are
added. `sweep`, `rout` and `defeat` were tried and **rejected** — "to avoid
the sweep" in the archived 08-27 Reds brief is a noun, the reader takes the
first listed verb it finds, and the contract test failed on it immediately.
That is the test suite paying for itself on its first afternoon.

## 2026-08-24 — the paper is checked against its own standings block

No. 10 printed "the Brewers hold the NL Central at 81-50, 18.5 clear of
second-place Pittsburgh" under a headline saying Milwaukee "still lead by
18.5." Pittsburgh was FOURTH and 18.5 BACK; Milwaukee led second-place
Chicago by six. Verified against MLB's stats API: MIL 81-50, CHC 75-56 (6.0),
STL 66-66 (15.5), PIT 63-69 (18.5), CIN 62-69 (19.0). Pat caught it in the
channel.

What makes it a fixable defect rather than a bad morning is that the SAME
EDITION had it right. The teams section carried "Pittsburgh Pirates: 63-69,
fourth in the NL Central, 18.5 back." The paper printed a fact and its
contradiction in two places a reader can see at once, and that is something
a validator can be asked to notice.

- **`_sm_check_standings_agreement()`** reads every brief in the edition
  against the standings block. A brief calling a team "second-place" when
  the block says fourth is a **hard error** — two printed ordinals for one
  team cannot both be true. A games-back figure appearing on a team the
  block does not give it to is an **advisory**, because two divisions can
  honestly produce the same half-game number; it asks rather than fails.
  Both halves of this miss are caught: the summary by the error, the
  headline by the advisory.
- **Subjects match on word overlap, not the alias table.** A brief names a
  club by its CITY — "second-place Pittsburgh" — and the alias table has
  "Pirates" and "Bucs", not "Pittsburgh". Adding city aliases would collide
  on their own terms: this desk follows the Cincinnati Reds AND FC
  Cincinnati. An ambiguous subject returns None and the gate stays silent,
  which is the right behaviour for a check whose whole claim is that it only
  fires on a contradiction provable from the paper's own words.
- **The games-back advisory runs per FIELD.** A headline is read alone, so
  "Milwaukee still lead by 18.5" answers for itself even though the summary
  two clauses later does name Pittsburgh.
- Twelve past editions re-validated: zero false positives.
- `instructions/sportsman.md` gets the rule in the desk's own words — a
  games-back figure is one team's deficit and never another's lead, and a
  leader's margin is the games-back of the row directly underneath.

**A latent `\b` was a literal backspace character.** While checking the new
regexes for the escaping problem that produced them, `[ap]\.?m\b` in
`_sm_check_teams` turned out to carry a raw 0x08 instead of a word boundary
— and it predates this session. The no-colon branch of the ET check could
therefore never match, so "Saturday, 3 p.m. BST" sailed through the gate
written to stop exactly that; only the colon form was ever caught, which is
why the Aug. 18 "17:30 BST" miss looked like the check working. Repaired,
both forms tested, and the whole repo scanned for the same corruption.


## 2026-09-01 — the tide table sits with the water it is about

Nate, pointing an arrow from one to the other: *"Can you make it so these
are together please?"*

"Topsail tides — the full day" headed the whole On the Water section, which
put it above three West Virginia river gauges and left the Topsail Sound
line it actually supports several inches below it. The table now follows the
North Carolina block, so the prose that quotes a couple of the times sits
directly above the table that carries all of them.

After the block rather than inside it: the block's items are `<li>` in a
`<ul>`, and a `<table>` is not a list item. A table with no North Carolina
block to attach to still runs, at the foot of the section — it is measured
data, and dropping it silently would be worse than setting it loose.

**The date guard added on 2026-08-26 caught its author.** Working from a
screenshot, the first render targeted 2026-08-30 while `out/fishing.json`
had moved on to 09-01, and `_tide_table_html()` refused to typeset the wrong
day's water — exactly the mistake it was written for, one week later, by the
same hand. The Aug 30 archive page was restored and today's rendered
instead, with the tide times diffed against the routine's own commit
(11:30 PM / 5:57 AM / 12:07 PM, identical).


## 2026-08-26 — source links open in a new tab

Nate: clicking a source navigated away from the edition. A citation is a
place you go to check something and then come back from, so it opens in a
new tab now — `target="_blank"` on the `SOURCE_LINK` block, which is the one
place in the template that emits an outbound link.

**Only outbound links.** The nav buttons, "Back issues" and the archive rows
are all inside the paper and stay in the same tab: a reader moving between
the three sections should not collect a tab every time they do it.

`rel="noopener"` was already on that block and is what makes
`target="_blank"` safe; `nofollow` stays because a wire brief is a citation,
not an endorsement.

Audited across the whole site after re-rendering — 68 outbound links, all
opening in a new tab, and not one internal link doing so.


## 2026-08-26 — a rule under the columns, and B.C. moves down beside the notebook

Two of Nate's, on the flowed layout he had just approved.

**A rule between the wire columns and the anchor sections.** A column bottom
is a ragged edge, so without one the notebook read as one more thing the
last column happened to run into. `.rule-anchor` is the only horizontal rule
inside the page body — the masthead's pair is chrome — and it lives in the
BASE stylesheet rather than a breakpoint, because the sections stack on a
phone and the break still needs saying there.

**British Columbia sits below West Virginia now.** It was one more column of
wire; it is now an anchor section at the full measure, directly under the
notebook. The pairing is the point — these are the two sections about places
somebody in the group actually lives, and they read together at the foot of
the page. Its briefs run in three columns of their own, because a
full-measure section set in one column would put 85 characters on a line,
which is the problem the reflow just solved.

`config.ANCHOR_SECTION_IDS` and `config.sections_in_reading_order()` hold
this, not the renderer, for one reason: **the Discord digest lists sections
in the order a reader will meet them on the page**, and a contents list that
disagrees with the page is worse than no contents list. The digest now reads
U.S., World, Science & Technology, Artificial Intelligence, West Virginia,
British Columbia — which is the page.


## 2026-08-26 — the wire sections flow instead of being placed

Pat: *"Good info, but lots and lots of unused space."* He was right, and it
was structural rather than a shortage of news.

The wire sections were in a CSS grid, one section per cell, and a grid row
is as tall as its tallest member. On that morning's paper: U.S. 524px, World
637px, Science & Technology 901px — **641px of dead column in the first row
alone**, and a second row where a double-width Artificial Intelligence cell
stood 260px empty. Measured across the whole block: **28% of the section
area was white** (491,677 of 1,755,631 px²).

Filling that with more briefs would have been the wrong fix. To close a
ragged row by content you have to grow every section up to whatever the
tallest happens to be, and the tallest changes every morning — that is a
recipe for padding, in a paper whose whole discipline is not padding.

So the sections **flow** now. Copy runs down column one and continues into
column two; the browser evens the bottoms; no arrangement of uneven sections
can leave a hole. Same content, same day, nothing added or cut:

| | Grid | Flowed |
|---|---|---|
| Section block | 1,917px | **999px** |
| Whole page | 3,093px | **2,653px** |
| Wasted area | 28% | **none** |

The original objection to multi-column here was real, and it is answered
rather than ignored: a `column-span: all` child splits a flow and strands
columns, which is what happened the first time this page was laid out. The
notebook is therefore not in the flow at all — it is a sibling block below
it, and nothing inside the flow spans. Sports & Sportsman has set this way
since it launched, which is why that page never had the problem.

**The trade-off, stated plainly:** sections no longer sit in tidy vertical
blocks. World can begin in column one and finish at the top of column two.
That is how a broadsheet reads and it is the price of the space; each brief
carries its own bold headline, so nothing becomes hard to follow.

The weather page got the same treatment — half a dozen reports of wildly
different lengths is precisely the shape a grid strands — and shed two
rendering artifacts with it: an empty label chip above Jim's scene-setting
paragraph, and an em-dash placeholder under a heading with no body.

Yesterday's last-section-spanning rule is gone. It patched the symptom.


## 2026-08-25 — the channel gets a doorbell; the paper gets its space back

Nate: *"let's actually stop trying to post the full Times to Discord. Let's
just have one post that links to the index page."*

- **`post_discord.py --digest`** builds ONE message: masthead line, the lead
  headline and dek, a line per section with its top headline, a Sports &
  Sportsman tease read from that paper's own JSON, and a link to Home.
  Measured on 2026-08-24's edition: **821 characters.** There is no trim
  ladder, no split and no budget, because nothing in a table of contents can
  reach 6,000 characters.
- **#sports-and-sportsman is retired.** That paper is still researched,
  written, validated, rendered and pushed every morning — it just is not
  posted. `instructions/sportsman.md` says so in a box, because the risk of
  this change is a desk that quietly gets lazier once the notification goes
  away.
- **#the-weather-claude is untouched.** Jim posts exactly as he always has.
- **The full-embed path still exists** and the instructions say plainly that
  the routine does not use it and neither should the desk.

What this is really about is the journalism. Four of eleven editions had
split in two. A written, sourced wire brief was cut for budget on
2026-08-22. The West Virginia notebook — the reason this paper exists — was
capped at six lines because that is what a 1,500-character embed allocation
paid for. None of that was an editorial judgement; it was a chat app's shape
pressing on the paper. So:

- **`EMBED_HARD` stops being a gate.** The hard error in `_check_budgets`
  ("even trimmed to one brief per section this will not fit") is gone —
  there is no ceiling to fail against and no trimmer waiting to eat the
  notebook. `_budget_advisory` now speaks about PROPORTION, fires at 1.35×
  a section's guide, and never fails an edition.
- `EDITION_TARGET_CHARS` / `EDITION_LONG_CHARS` replace the delivery ceiling
  with an editorial one. A long paper on a big day is allowed.

**Home, and `/home.html`.** The landing page called itself "The Newsstand"
while the nav button that reached it had said "Home" since 2026-08-21, and
its Discord unfurl advertised two papers when there are three. It is now
Home, at `home.html`, with a description that names all three and says when
they file. `site/index.html` became a redirect carrying the same title and
description, so a bare `/` still resolves AND still unfurls correctly.


## 2026-08-25 — the weather page is typeset, not pasted

Nate: *"make the newspaper weather page look like the other newspaper
pages."* It had been one 760px column of Jim's Discord message with the
emoji headers, the bullet lists and the literal `-#` small-text markers
still in it — a chat log in a nice font, stranding two thirds of a desktop
page.

Jim's markdown is a stable dialect, so it maps onto the paper's own
furniture rather than needing a general parser:

| Briefing | Page |
|---|---|
| `# <day>` | the headline |
| `## <dek>` | the dek |
| `### <place — person>` | a section label, the same black chip the wire sections use |
| consecutive `###` with no body | ONE section, labels joined — that is what a stack MEANS: three towns sharing one forecast |
| `- <item>` | the notebook's roundup list |
| `> <text>` | a boxed feature, the way the notebook is boxed |
| `-# <text>` | the colophon |

Emoji are stripped from headings: they are how a Discord post signals a
heading, and a newspaper has type for that. `PAGE_CLASS` dropped
`"sportsman"` — the page had been borrowing that paper's flowed columns,
which is what kept the whole briefing in one stripe down the middle.

**Nothing here touches what Jim posts to the channel.** This module only
ever reads his archived markdown, and the read-only boundary in
`instructions/weatherpage.md` is unchanged.


## 2026-08-26 — British Columbia, Artificial Intelligence, and a bigger notebook

All live from the 2026-08-26 edition. Every one of these is date-scoped so
the archive still validates as the paper it actually was: `sections_for()`
learned a `since` key (the mirror of `RETIRED_SECTIONS`), and
`WV_SUBHEADS_CHANGED_ON` gates the notebook changes.

- **British Columbia** — Kirsten's, and a standing section. It had been one
  sentence on the Away Desk sharing a sub-block with Wes's Vermont, which is
  not coverage of a place somebody actually lives. The `prince_george` Away
  Desk line is retired and the validator refuses it by name, pointing at
  where the coverage went: the same town in two places on one page is worse
  than one place done properly.
- **Artificial Intelligence** — top-level rather than a block inside Science
  & Technology, which it had been quietly eating; telescopes and medicine
  were losing slots to model releases. The instructions are blunt that a
  model release is a brief only when something is measured, because the
  failure mode of an AI section is a product-launch feed.
- **West Virginia got bigger**: 3–5 statewide briefs (was 2–3), ~9 notebook
  lines (was 6), 150 characters a line (was 110). Nate called it skimpy and
  he was right — those numbers were the embed budget, not a judgement about
  West Virginia.
- **"On the Water" → "Vacation Hotspots"** (`fishing` → `hotspots`). It
  carried gauge readings and tide times, which are instrument data, and the
  water has belonged to Sports & Sportsman since 2026-08-21 — this was the
  last of that overlap. It now carries NEWS from Webster County/Cowen and
  Topsail Island/the coast, with Wilmington allowed only when the story is
  genuinely big. `topsail` is promoted out of the Away Desk too, leaving
  Vermont as its only region.

**Layout.** Five wire sections across a 1,490px measure would be 274px a
column, so past four the page wraps to three wide columns over two rows —
and the last section widens to fill whatever the last row would otherwise
leave empty, which is the same hole this file complained about yesterday.


## 2026-08-24 — the desktop front page stops leaving a quarter of itself blank

Pat: "the pages look really good on mobile, but some of us read them on
desktop and it looks bad. There is a ton of white space." Two separate
layout bugs, both invisible on a phone because both live in `min-width`
media queries.

- **The lead block was a grid sized for a drawing that was not there.**
  `.lead-block` is `grid-template-columns: minmax(240px, 27%) 1fr` at
  desktop — art at a third of the measure, story beside it. With no art the
  STORY became the first grid child, inherited the 27% art column, and left
  three quarters of a 1,420px page white beside eight lines of type. Art
  placement is an editorial choice made fresh each morning and the drawing
  goes to another section more often than not — **six of the last eight
  editions**, so most desktop front pages have looked like this. The grid is
  now scoped to `.lead-block.with-art`; without art the lead runs the full
  measure at two columns (1024px+) and three (1320px+). Three, not four,
  even at 1,600px: the lead runs about 700 characters and a fourth column
  would set it three lines deep and read as a caption.
- **The sections grid was `repeat(4, 1fr)` with only three wire sections.**
  The comment said "the four beats", but the fourth is West Virginia, and
  the notebook spans the whole measure on its own row — so the fourth track
  was always empty, a quarter of the page blank from the section labels all
  the way down to the notebook, on every desktop edition since the layout
  was written. The renderer now counts what actually RENDERED and passes it
  as `--wire-cols`, so a morning where a section comes up empty closes to
  two columns instead of holding a gap open for news that does not exist.

Verified with headless screenshots at 1600, 1440, 1280 and 1100 desktop and
390 mobile: mobile is byte-for-byte the same layout, the with-art lead is
unchanged, and the front page is ~300px shorter.

**Past editions were deliberately NOT re-rendered.** `_tide_table_html()`
reads the CURRENT `out/fishing.json`, so re-rendering an August 20th page
today would typeset today's tides into it. The archive keeps the old layout
rather than gaining today's water.




Nate: the reading flow is top to bottom, and then you want the next section —
but the only way to it was back up at the masthead. Every rendered page now
carries the same buttons again below the colophon, ruled off so it reads as
the end of the paper rather than as more paper. Both rows are built by the
same `_nav_html()`, which grew a `foot=True` that only changes the class and
the aria-label, so the links can never drift apart. `{{NAV_FOOT}}` is a
required template token like every other, and `fill()` raises on a missing
one — a renderer that forgot a page would fail loudly rather than ship a
page with half the navigation.

Covers all four page shapes off the PAGE block: `today.html`, dated
`editions/`, `sportsman/`, `weather/`. **`site/archive.html` is deliberately
untouched** — it has never carried the nav row at ALL, top or bottom, and
giving it only a foot copy would be a stranger page than it is now. Its
"Today's edition" footer link still gets a reader out.


## 2026-08-24 — three advisories the desk had been logging for weeks

Nothing editorial changed. These are three defects the morning routine found,
wrote down in `docs/FAILURES.md`, worked around, and then hit again the next
day — the whole point of that file is that somebody eventually reads it.

- **The budget projection was ~107 characters low, every single morning.**
  Same bug as 2026-08-05's masked-source-link miss, one seam over:
  `_exact_measure()` built the payload with `page_url=None`, so it never
  counted the "Read the full edition on the web" line that `--page-url`
  appends to the last embed's description — 107 chars Discord counts exactly
  like copy. Against an `EMBED_HARD` of 5,800 that is the difference between
  safe and split. On **2026-08-22** the desk cut a written, sourced wire
  brief to reach a projected **5,783**, and the paper split anyway at a real
  **5,890**; the cut bought nothing. Four splits in eleven editions (Nos. 8,
  12, 13, 18) were read against the same low number. The validator now
  measures with the permalink `instructions/routine.md` actually passes
  (`config.page_url` / `config.sportsman_page_url`, skipped when
  `PAGES_ENABLED` is False), and re-measuring 2026-08-22 gives 5,890 on the
  nose. `post_discord.tail_link_text()` was split out of `_tail_link()` so
  there is one definition of that line rather than two.
- **The permalink gets its own `section_chars` key, not a section's.** It
  rides the LAST embed, so a naive tally billed it to whichever section ran
  last and reported that section over its allocation for a cost no editing
  can reach. It is not `chrome` either — chrome's 200 is the closing footer,
  which the desk *can* shorten. `permalink` has no line in
  `config.EMBED_BUDGET` on purpose: it is paid out of the 200 of headroom
  `EMBED_HARD` already leaves above `EMBED_TARGET`, so it counts in the total
  and is never something a person can be told to tighten.
- **`--sportsman` never credited `upcoming` fixtures.** The comment said
  "Standings and fixtures also count as accounting for a team" and the code
  said otherwise: `instrumented.add()` sat in an `else` branch only
  `standings` could reach, so a club with a cited, ET-converted fixture line
  was still reported missing. Identical advisories ran **2026-08-20, 21 and
  22** naming Chelsea, Tottenham, Liverpool, the Browns and the Bengals while
  all five carried fixtures — a note that contradicted itself in its own
  text. Fixed by hoisting the instrumentation out of the branch. Re-running
  Aug. 20-24 now names only **Hannan**, which was genuinely uncovered before
  its season opened, and stripping `upcoming` from an edition brings the
  advisory straight back.
- **The Topsail water temperature came back, from a different station.**
  Nine mornings of `noaa-temp: no water temperature returned` were not an
  outage: NOAA removed the `water_temperature` product from **8658163
  Wrightsville Beach** entirely, and the station's own metadata no longer
  lists it. Nate picked **8656483, Beaufort, Duke Marine Lab** — 60 miles up
  the coast and estuarine, over the nearer Wilmington (8658120, ~30 miles)
  because Wilmington is Cape Fear River water at the state port and read 2F
  warmer the day the three were compared. First reading back: 85.1F, zero
  source errors. The station now lives in `config.TOPSAIL_TEMP_*` and
  nowhere else — `fetch_fishing.py` imports it instead of restating it, and
  the validator's attribution gate reads the same constants, so a fetcher
  that disagreed with the gate can no longer fail every edition it feeds.
- **The sportsman attribution gate was checking the wrong field.** It read
  `entry["line"] or entry["read"]` — the advice sentence — while this paper
  puts the tide table and the temperature in `reading`. An uncredited water
  temperature walked straight past it. It now reads every reading field, and
  uses the same `_temperature_mentioned()` guard the Times uses on the same
  water rather than the weaker trailing-F regex, so "water 85 degrees"
  fails like "85F" does. `working` stays excluded on purpose: it is prose,
  and 2026-08-24's entry alone carries "an 85% waxing gibbous" and "tarpon
  to 110 pounds" — the bare-number heuristic reads the first as a
  temperature, which it very nearly is, since the water read 85F that
  morning. A reading goes in a reading field.
- **The two papers no longer overwrite each other's payload file.** Both
  wrote `out/<date>.payload.json`, and since they post five minutes apart the
  sportsman run destroyed the Times' record of what shipped on every morning
  both papers ran. Sports & Sportsman now writes
  `out/<date>.sportsman.payload.json`. Harmless to delivery, but "the run is
  settled by a file, not by somebody's memory" was not true while it lasted.

## 2026-08-05 — first end-to-end run: seam fixes

The revision round above was written by five parallel passes that never ran
the pipeline together. This is the integration pass: fishing fetched live,
`editions/2026-08-05.json` hand-authored to the extended contract, then
validate → render → `post_discord --dry-run` run to convergence. Nothing was
posted; no webhook exists.

- **The budget gate was lying by ~700 characters.** `estimate_embed_chars()`
  priced a brief as `-# Source` while `post_discord.py` actually sends
  ` · [Source](https://…)`, and Discord counts every character of that url.
  On the first real edition the validator reported 5,608 chars and blessed
  it; the poster then measured 6,310, blew `EMBED_HARD`, and silently
  deleted the away desk and two of three regional lines — Ian's local anchor,
  gone every morning, visible only in `FAILURES.md`. `estimate_embed_chars`,
  `section_chars` and `irreducible_chars` now MEASURE the real payload
  (`post_discord.build_payload` on a deep copy) and fall back to the old
  approximation only when the poster cannot be imported or the edition is too
  malformed to build.
- **`config.EMBED_BUDGET` re-derived against that measurement**, url markup
  included: lead 900, wire sections 750, wv 1,500, chrome 200 (the closing
  footer). `SUMMARY_TARGET_CHARS` 160 → 140 and `HEADLINE_TARGET_CHARS` 60 →
  58 follow from the same arithmetic, and `instructions/style.md`'s length
  table and notebook table were corrected to numbers that actually close.
  The old targets could not fit one message and said they could.
- **`config.REGIONS` said `kanawha_putnam`; both docs said `putnam_kanawha`.**
  Config now matches the docs and the printed place name.
- **The broadsheet's notebook sub-heads were hardcoded** in
  `render_edition.py` ("Around the Region" / "Away Desk" / "Fishing Report")
  while the embed and the validator read `config.WV_SUBHEADS` ("Around the
  State" / "The Away Desk" / "On the Water"). The renderer now reads config,
  so all three surfaces print the same words.
- **`render_edition.py --edition X --out Y` republished the site root.**
  Rendering a fixture to `out/` also overwrote `site/index.html` and
  `site/archive.html`, repointing "today's paper" at a fixture. An explicit
  `--out` now writes exactly one file; only a default-path render publishes.
- **The hero card lost its drop cap on short headlines.** The headline's
  height check counted one leading per line but not the drop to the first
  baseline, so a big two-line headline quietly borrowed the excerpt's rows,
  the `rows >= 2` test failed, and the card printed a hole. Measured with
  `_headline_block()` and the size steps down until it fits.
- **`editions/_fixture.json` was stale** against the extended contract — no
  `weather_ear`, no `notebook_title` — so the validate command in
  `validate_edition.py`'s own docstring failed. Fixed, and given a full
  notebook (4 regional, 2 away, 2 fishing — the playbook's ceilings) so the
  layout regression covers the whole box.
- **`editions/_fixture_thin.json` added:** the legal thin day — empty
  `regional`/`away`/`fishing`, `kicker: null`, `stat_strip: []`, one brief a
  section. Validates, renders (no strip band, no kicker, `.wv-box` still
  boxed), and dry-runs to 1,775 embed chars in one message.
- **The playbook's Topsail fishing example used `"Topsail Beach"`**, which is
  not a `config.FISHING_WATERS` value and would have failed validation on the
  first real morning. Corrected, with a line saying `water` is copied
  verbatim from the config.

Measured on the fixture edition (15 briefs, full notebook, 4 stat entries):
**5,699 embed chars** in a single message, 301 under Discord's 6,000, no
trimming, no split, no stripped urls, hero attached at 80,041 bytes.

Correction to the entry below: the cloud routine's cron is `0 11 * * *` UTC
(**7:00 AM ET**), not 6:45 — `config.POST_CRON_UTC`.

## 2026-08-05 — Ian's template, the WV notebook, fishing, 7:00 ET

Revision round on the day-old pipeline. Ian sent his real HTML template
and answered the two open questions; Nate expanded West Virginia and moved
the post time. No architecture changed — one webhook message, six embeds,
one Pillow hero, the same fallback ladder.

- **`docs/IAN-TEMPLATE.html` is now the design authority.** Ian's actual
  artifact source, not a reconstruction, and it supersedes any earlier
  guess. `templates/broadsheet.html` matches its structure and tokens: the
  `.top-bar` row (Vol./No. — date — "Price: Free"), 58px Old Standard TT
  masthead, italic tagline, 4px double rule over a thin rule,
  `.section-label` (900-weight Playfair on `#1c1a16` with `#f4f0e6` text
  and 0.12em tracking), `.columns` with a 1px `#c9c2ac` column rule, the
  46px `.drop` cap, the `.stat-strip` band bordered top and bottom, and
  `.footer-note`. The file is an input and is never edited.
- **`.wv-box` is load-bearing, and Ian said so explicitly.** West Virginia
  does NOT use the two-column brief layout every other section uses: it
  gets a 2px `#1c1a16` border, an `#ede7d6` tint, and a "Mountaineer State
  Notebook" title in 20px 900-weight Playfair. The distinction is what
  makes WV read as the paper's local anchor rather than another wire
  section, and it carries into the HTML and into any Pillow WV card.
- **The WV notebook now has four parts** (Nate): statewide briefs, a
  regional roundup across the crew's own markets, an away desk for the
  out-of-state crew, and a fishing report. Statewide always appears;
  `regional`, `away`, and `fishing` are optional arrays and a thin day is
  legal. **Regional and away items are ONE SENTENCE**, not briefs — "lean"
  was a hard instruction, and the padding failure mode is the one to fear.
- **Regions live in `config.REGIONS`,** derived from the sibling
  `weatherman` project's `LOCATIONS` and grouped into real media markets:
  Huntington & the Cabell-Mason corridor, Putnam/Kanawha—Charleston,
  Mid-Ohio Valley/Parkersburg, Nicholas & Webster/Summersville—Cowen, and
  Summers/Hinton & the New River; away desk = North Bennington VT, Prince
  George BC, Topsail Beach NC. Grouping is deliberate: Lesage has no daily
  news of its own, and a schema that demands a line per hamlet teaches the
  model to invent one. Only regions with genuine news get a line.
- **People are first names only.** No Discord user IDs, no addresses, no
  ZIP codes — `weatherman` keeps those, this repo does not. Same reason as
  the no-ping rule: this repo is going public for Pages.
- **`fetch_fishing.py` added** and wired into the WV notebook. USGS
  instantaneous values at gauge `03186500` (Williams River at Dyer) for
  the cabin water — discharge, stage, temperature, each with a 24-hour
  trend and a wadeability read where water temperature outranks flow.
  NOAA CO-OPS tide predictions from the two stations bracketing New
  Topsail Inlet (`8657419` ocean, `8657813` sound — they disagree by ~75
  minutes, so both are reported and neither is averaged away), plus water
  temperature from `8658163` Wrightsville Beach. Writes `out/fishing.json`;
  exit 1 only if both waters are dead.
- **Topsail's water temperature is Wrightsville's,** 25 miles up the
  coast, and ships with the station name and distance attached. Passing it
  off as Topsail's own would be a fabrication, just a quiet one.
- **Two source traps found live:** NOAA answers `200` with an error body,
  so `raise_for_status()` never fires and the `error` key is the only real
  guard; and WVDNR serves an **expired TLS certificate**, so trout
  stocking is a web-search item in the playbook with a silent no-op
  fallback, never a fetch. Do not "fix" the latter with `verify=False`.
  (USGS also 503'd during today's test run — that is a normal degraded
  morning: the Williams line is omitted, never estimated.)
- **Post time moved 6:45 -> 7:00 AM ET** (`0 11 * * *` UTC; drifts to 6:00
  ET in November), and the paper now points at Claude the Weatherman's
  7:15 forecast instead of just dodging it. The pointer uses the
  newspaper convention that already exists for this — the **weather ear**,
  the small boxed item beside the masthead. It lives in the `.top-bar`
  area of the HTML, closes the Discord post, and rides the hero PNG when
  it fits. The wording is written fresh each day into
  `edition.weather_ear`; it is a rotating line, not a frozen string.
- **Sumo rule settled by Ian:** "sumo gets covered when there's something
  to cover," not a headline a day regardless. The daily dedicated search
  stays mandatory; the daily brief does not, so the validator no longer
  demands one. During a basho (odd months — Jan, Mar, May, Jul, Sep, Nov,
  15 days each) sumo should usually win the sports lead. Off-months, a
  one-line banzuke/promotion/retirement note is the honest version of "no
  sumo news."
- **Three briefs per section confirmed by Ian.** Takes the clean
  single-message win rather than engineering a two-message split.
- **Contract extended in exactly one place.** The `wv` section gains
  `notebook_title`, `regional`, `away`, and `fishing`; the edition gains a
  top-level `weather_ear`. Every other section keeps the plain
  `{"briefs": [...]}` shape, so nothing downstream had to learn a second
  section schema.

**Not yet done:** the Discord webhook still does not exist, so nothing has
ever posted; the GitHub remote still does not exist and `PAGES_ENABLED`
stays `False`; the cloud routine (Opus, `0 11 * * *` UTC = 7:00 AM ET) has
not been created; the WV outlet list is still Claude's, unconfirmed by
Ian — worth one message, especially for the Nicholas/Webster and Summers
markets the regional roundup leans on.

## 2026-08-04 — Initial build

Scaffolded from `docs/HANDOFF-FROM-IAN.md` on the `weatherman` /
`odds-ev-finder` pattern: no servers, prompt-as-markdown in
`instructions/`, secrets via the routine's task prompt.

- **Delivery shape decided:** ONE webhook message per morning, posted as
  multipart to `{webhook}?wait=true` — a `content` masthead line, six
  embeds (LEAD + U.S. + World + WV + Sports + SciTech), and a 1200x630
  hero PNG attached as `ashgrove-YYYY-MM-DD.png`. Embeds are the
  readable paper; the image is identity. The hero is strictly additive:
  drop `attachments` and the lead embed's `image` block and the same
  bytes POST as plain JSON, still a complete newspaper.
- **`editions/YYYY-MM-DD.json` is the only interface.** Content only —
  no emoji, no colors, no display metadata. Section metadata lives in
  `config.py`. Dates always resolved from `TZ=America/New_York date`,
  never a session stamp.
- **Pipeline:** `fetch_stats.py` -> Claude writes the edition JSON ->
  `validate_edition.py` (hard gate) -> `render_edition.py` (HTML + hero)
  -> git push -> Pages poll -> `post_discord.py` -> ledger update. The
  model's only creative output is the JSON; everything after it is
  deterministic Python Nate can re-run with no model in the loop.
- **Renderer choice settled by verification, not preference:** WeasyPrint
  removed PNG output at v53 (Cairo -> pydyf, PDF only), Playwright needs
  a ~160 MB Chromium download from a CDN the restricted sandbox may 403,
  `wkhtmltoimage` is a dead apt binary. Pillow ships self-contained
  manylinux wheels with FreeType bundled. Fonts vendored as static OFL
  instances in `assets/fonts/` so the hero renders fully offline.
- **Hero scope is a 1.91:1 card, not a full page.** Discord scales an
  attached image to roughly 550px wide, which turns broadsheet body type
  into ~10px mush. 1200x630 is legible at exactly the size Discord shows;
  anyone wanting the full broadsheet taps the Pages link, where the text
  is selectable and the sources are live.
- **Stat sources verified from this machine today:** Yahoo
  `query1.finance.yahoo.com/v8/finance/chart/^GSPC` 200, CoinGecko
  `simple/price` 200, **stooq 404 on every CSV symbol**. The ladder is
  Yahoo -> CoinGecko -> empty. Stooq is not to be built on.
- **Stat-strip truth rule:** a `stat_strip` value may exist only if it
  byte-matches an entry in `out/stats.json`. No stats means `[]` and both
  renderers omit the band entirely. Hallucinated market numbers are a
  hard validation failure.
- **Fixed Ian's color math:** the handoff states `#3E3221 -> 3419169`,
  which is wrong (`0x3E3221` = 4076065; 3419169 is `0x342C21`).
  `config.py` computes every color with `int(hex, 16)` at import.
- **URL liveness semantics:** 200-399 plus 403 and 405 all count ALIVE —
  paywalls and restricted-sandbox egress produce identical 403s. Only DNS
  failure, connection refused, and 404 strip a link, and a stripped link
  never fails the edition; the brief keeps its source name.
- **13-rung fallback ladder** implemented across the scripts, ending at
  the one rung that ships nothing: if the lead story cannot be sourced at
  all, abort and write `FAILURES.md`. A missing paper is recoverable; a
  fabricated front page is not.
- **Operational memory:** `editions/index.json` (edition numbers,
  `posted` flags, message ids, degraded paths — also the idempotency
  gate against double-posting on a retry), `docs/LEDGER.md` (open
  threads, forward-dated events, covered slugs for dedupe),
  `docs/FAILURES.md` (append-only degraded-path log).
- **`editions/_fixture.json`** committed as an executable worst case —
  absurd headlines, 6 stat entries, 4 briefs a section, one null url — so
  layout and budget regressions are caught offline instead of on a live
  news day.
- **No pings, no user IDs anywhere in the repo.** The repo is going
  public for free-plan GitHub Pages, so the mention surface is empty by
  construction, not by policy.
- **`PAGES_ENABLED` ships `False`.** The git dir has zero commits and no
  remote, so the web tier cannot be live yet. Every dependent path is
  already conditional on that one flag — `build_payload()` omits the
  permalink and drops `embed.url`, nothing else changes. Flip it once
  `payne2225/ashgrove-times` exists and Pages is green.

**Not yet done:** create the GitHub remote and enable Pages; create the
cloud routine (Opus, `45 10 * * *` UTC = 6:45 AM ET, 30 minutes ahead of
Claude the Weatherman so the two never collide); first live edition.
