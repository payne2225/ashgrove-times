# HANDOFF — the living state of both papers

**This file is the running handoff. It is never written from scratch and
never goes stale, because updating it is part of finishing work here.**
A fresh session reads this file and starts working. Nate should never
have to ask anyone to write a handoff again.

> **If you changed anything in either repo, update this file in the same
> commit.** Not a changelog — that is `docs/PATCH_NOTES.md` and
> `docs/LEDGER.md`. This file is only ever *the current truth*: what
> exists now, what is decided, what is open. Delete what stopped being
> true rather than appending to it.

Last updated: **2026-08-26**

---

## 1. What this is

**Two daily Discord posts and a website** (changed 2026-08-25 — it was three
posts and the papers themselves went to the channel). Two repos:

| Repo | Visibility | Holds |
|---|---|---|
| `payne2225/ashgrove-times` | **PUBLIC** | The News Desk, Sports & Sportsman, the website, the weather-page renderer |
| `payne2225/weatherman` | private | Jim Claudtore — the briefing, the alert watcher, the report card |

Local: `C:\Users\payne\Projects\ashgrove-times` and `...\weatherman`.

**The Times session owns both repos** (Nate, 2026-08-22). One session
drives everything. The one carve-out is in section 5.

## 2. The morning

| ET | What | Routine |
|---|---|---|
| 5:30 | Wake, research and PUBLISH both papers | Times |
| 7:00 | **The digest posts** — one message, what is in today's edition and a link to Home | Times |
| 7:15 | **Jim Claudtore's briefing** posts | weatherman |
| 9:00 | Watchdog — silent unless something failed | watchdog |
| 8:10 | Weather page typeset onto the site | weather-page |
| every :30 | Alert watcher — silent unless something NEW | weatherman |
| Sun 18:00 | Weekly report card | weatherman |

Jim is deliberately **independent**: if the papers run late he still
files at 7:15. He is the post people actually dress by. Do not couple
his schedule to theirs.

## 3. Live routines

All in environment `env_01HRBGRSDmfX7Vur76oE8Lkh`, all on
**`claude-fable-5`** (aligned 2026-08-23). Webhooks live only in task
prompts and in gitignored `.env` files — never in a repo.

| Routine | ID | Cron (UTC) |
|---|---|---|
| Ashgrove Times + Sports & Sportsman | `trig_01EMUikWUwB5GLE9GzGAPefb` | `30 9 * * *` |
| Weatherman Daily Briefing | `trig_01GeSVSait6X3Dwam8tkMycj` | `0 11 * * *` |
| Weatherman Alert Watcher | `trig_01AxyXnGTWwT4vXKWTv6w7Uq` | `30 * * * *` |
| Weatherman Weekly Report Card | `trig_01GTwkNWUrDkwMPi1XNx8MxZ` | `0 22 * * 0` |
| Weatherman Watchdog | `trig_01THzxTGHkdRgJWJwBZwjKQX` | `0 13 * * *` |
| Ashgrove Weather Page | `trig_01MEbyaBjFYcU4v9pERM4Paa` | `10 12 * * *` |

The watchdog row said 8:00 until 2026-08-30; its cron is `0 13 * * *` UTC,
which is 9:00 ET on daylight time — the table had been quietly an hour out.
Observed posting at 9:11.

**The alert watcher has a HEARTBEAT** (2026-08-30). It stamps `last_run_utc`
in `weatherman/alerts_state.json` on every run and commits it when the
committed stamp is over 3 hours old; the watchdog reads that field with a
6-hour window. **Never judge that routine by the file's date or by
`updated_at_utc`** — the state file is only written when the set of active
alerts CHANGES, so a quiet spell looks exactly like a dead routine. That is
precisely what happened on 2026-08-30: the watchdog reported the watcher
dead for three days while it was firing every half hour and succeeding.

**DST is handled for the briefing only.** `post_discord.py --at` holds
Jim to 7:15 ET, so his slot survives the time change. The other crons are
still raw UTC and will each shift an hour on **2026-11-01** — the papers
to 4:30 ET, the weather page to 7:10, the report card to 17:00. Either
move them that week or give them the same hold.

## 3.5 The channel gets a doorbell, not the paper (2026-08-25)

Nate: *"let's actually stop trying to post the full Times to Discord. Let's
just have one post that links to the index page."*

- **#the-ashgrove-times** — ONE message a morning: masthead line, the lead
  headline and dek, a line per section with its top headline, a Sports &
  Sportsman tease, and a link to **Home**. `post_discord.py --digest`.
- **#the-weather-claude** — unchanged. Jim posts exactly as he always has.
- **#sports-and-sportsman** — **retired.** That paper is still written,
  validated, rendered and pushed every morning; it just is not posted. Home
  and the nav buttons reach it.

**What this bought the journalism, which is the part worth protecting:** the
6,000-character embed ceiling is gone. Four of eleven editions had split in
two; a sourced wire brief was cut for budget on 2026-08-22; the West
Virginia notebook was capped at six lines because that is what the embed
paid for. `EMBED_BUDGET` still exists but it is now an editorial guide to
PROPORTION, and nothing truncates a long section any more.

**The digest links Home, not the dated edition** — Home reaches all three
papers, a permalink reaches a third of one. There is nothing to backfill.

## 3.6 What the paper carries (2026-08-26)

Two new standing sections and a rebuilt notebook, all live from the
2026-08-26 edition; `config.sections_for(date)` and
`config.WV_SUBHEADS_CHANGED_ON` date-scope every one of these so the archive
still validates as the paper it was.

- **Canada** (section id still `bc`) — Kirsten's. Was one Away Desk sentence
  sharing a block with Wes's Vermont; then a British Columbia wire section;
  since 2026-08-26 a **three-tier** section set below the notebook at full
  measure. Every brief carries a `tier` — `prince_george`, `bc`, `canada` —
  and **all three file** from 2026-08-27. Local column first, on purpose:
  the section exists for somebody who lives in Prince George. The
  `prince_george` Away Desk line is **retired and refused by the validator**.
- **Artificial Intelligence** — was eating Science & Technology's slots.
  Now top-level, 2–3 briefs, and a model release is only a brief when
  something is measured.
- **West Virginia got bigger.** 3–5 statewide briefs (was 2–3), ~9 notebook
  lines (was 6), 150 chars a line (was 110). Those old numbers were the
  embed budget, never an editorial judgement.
- **"On the Water" → "Vacation Hotspots"** (`fishing` → `hotspots`). It
  carries NEWS from the two places the crew goes — Webster County/Cowen and
  Topsail Island/the coast — not gauge readings. The water belongs to Sports
  & Sportsman and this was the last of that overlap. `topsail` is promoted
  out of the Away Desk too.

Vermont is now the only Away Desk region.

## 4. The website

`https://payne2225.github.io/ashgrove-times/home.html` — **Home**, a static
hand-kept page (`site/home.html`) that the renderer must never write. It was
called The Newsstand until 2026-08-25, while the nav button that reached it
had said Home since 2026-08-21. `site/index.html` is now a redirect to it so
a bare `/` still resolves, and it carries the same `<title>` and
`<meta description>` so a link to the root still unfurls correctly in
Discord. **Home's title and description are what the channel sees every
morning** — they are the shop window, not housekeeping. It links:

| Section | URL | Written by |
|---|---|---|
| The News Desk | `/today.html` and `/editions/<date>.html` | `render_edition.py` |
| Sports & Sportsman | `/sportsman/` | `render_edition.py --sportsman` |
| The Weather Claude | `/weather/` | `render_edition.py --weather` |

**Page layout (2026-08-26).** The wire sections FLOW through balanced
columns — a grid stranded 28% of the section area as white. Two sections do
not flow: **West Virginia and British Columbia are anchors**, set at the
full measure below the columns and separated from them by the page's one
horizontal rule. `config.ANCHOR_SECTION_IDS` and
`sections_in_reading_order()` are the single source of that order, because
the Discord digest's contents list follows it too. **A spanning element must
never go inside `.wire-flow`** — that splits a multi-column flow and strands
columns, which is why this was a grid the first time.

**The weather page was rebuilt 2026-08-25** to set as a newspaper rather
than as a pasted Discord transcript: headline and dek from Jim's `#`/`##`
lines, each location report a wire section with a black label chip, stacked
headings combined into one section, his `>` confidence note as a boxed
feature, and his `-#` small-text lines as the colophon. Emoji are stripped
from headings — a newspaper has type for that. **None of this touches what
Jim posts**; the renderer only ever reads his archived markdown.

Every section page carries THE ASHGROVE TIMES as a family banner above
its own masthead, plus nav buttons (Home and the other two sections)
**twice — under the masthead and again at the foot of the page** (Nate,
2026-08-24). A reader finishes at the bottom, which is where the decision to
read the next section gets made; the top row alone made that a scroll back
up. Both rows come from `_nav_html()` in `render_edition.py`, so they cannot
drift apart.
Pages build via GitHub Actions with **unbounded lag** — 23 seconds to 9
minutes observed. Post on time, backfill the link when the build lands.

**Never bulk re-render the archive.** `_tide_table_html()` reads the current
`out/fishing.json`, so re-rendering an old dated page typesets TODAY's tides
into it. A layout change reaches `today.html` and everything rendered after
it; the back issues keep the layout they were published with, which is the
correct trade.

## 5. The one boundary left

`instructions/weatherpage.md` holds it. The interactive session may
develop weatherman freely. **The unattended 8:10 weather-page routine
stays read-only in weatherman** — it reads, it writes only to
ashgrove-times, it never posts. An unattended job with write access to a
live publishing repo is how a broken 7:15 post happens with nobody awake
to catch it.

**Ask Nate before changing anything the channel experiences**: post
times, a persona or name, the format, who gets pinged.

## 6. Standing rules that cost something to learn

- **Direction is a fact too.** Twice in three days the sports desk read a
  table right and stated the relationship backwards — "second-place
  Pittsburgh" when they were fourth (2026-08-24), "Pirates blanked by the
  Padres" when Pittsburgh won (2026-08-26). Both printed only real numbers,
  so every byte-match check passed them. A game report now carries
  `result: {winner, loser, score}` and the validator checks the prose's verb
  against it. **Half right is the signature of this bug** — when a brief
  states a relationship, check the relationship, not just the numbers.
- **The away desk and Vacation Hotspots run EVERY morning** (Nate,
  2026-08-26: *"ALWAYS give us content... there is always stuff to
  report"*). Fourteen-day window; work the search ladder — local outlets,
  then the bodies that meet on a schedule (council, commission, school,
  DOT), then social media as a LEAD. An official account posting about
  itself IS citable; anybody else is a lead to confirm elsewhere. The
  validator refuses an empty block without a note naming what was searched.
  Verified-fetchable sources are listed in `instructions/edition.md` §3a —
  Webster County's own outlets are 403 from the routine's environment.
- **Never invent a fact.** Thin is allowed; fabricated ends the project.
  A season date, bag limit or size limit is looked up TODAY, cited and
  linked, or not printed — someone could hunt or keep a fish out of
  season on this paper's say-so.
- **Every printed time carries ET.** ET alone or both zones, never a
  foreign zone alone. The validator enforces it on fixtures.
- **The Times repo is PUBLIC**: no webhooks, no Discord user ids, no
  addresses, no employer names. People appear by first name only. The
  weather-page renderer refuses to render if a ping id survives its scrub.
- **Two webhooks, two channels** — never post one paper with the other's.
- **Only scheduled routines post to Discord.** Ad hoc posting needs Nate
  to ask, and a redo gets a full rewrite, never a near-verbatim repost.
- **Jim's honesty rules** (`weatherman/instructions/briefing.md`):
  humidity as a number, named geography, no raw SPC codes, callouts
  earned rather than templated, and grade-inflation on the report card
  is the one unforgivable failure mode.
- **Justin, Wes and Greg are never tagged.** **Kirsten gets no coping
  advice, ever** — numbers and relief windows only.
- **There is a standing running gag in the briefing** whose rules live in
  the private weatherman playbook, deliberately not written down here —
  this repo is public and the people it involves can read it. Read
  `weatherman/instructions/briefing.md` before touching Jim's voice.

## 7. Where the two projects touch

1. **The weather ear** — the Times masthead points at Jim's 7:15 slot.
   If his time moves, `instructions/edition.md` and `instructions/
   routine.md` both go stale.
2. **Topsail is split** (2026-08-21): the **weather** is Jim's, the
   **water** — tides, moon, what's running — belongs to Sports &
   Sportsman. `reference/topsail-fishing.md` lives HERE only; the
   weatherman copy was deleted 2026-08-23 to stop the drift.
3. **The weather page** — the 8:10 routine reads Jim's archived briefing
   and typesets it. See section 5.
4. **Hannan soccer** — `reference/hannan-soccer-2026.json` exists in
   BOTH repos, because each routine checks out only its own. Correct
   one, correct the other.

## 8. Ian coaches Hannan

Ian is the **head coach of Hannan High School boys varsity soccer**,
Aug 25 – Oct 15. The schedule file is **authoritative for fixtures** (it
came from him) and **never for results** — a score is printed only when
an outside source has it and can be cited. Ian reads the paper.

- Sports & Sportsman: a standing beat in season; fixtures in The week
  ahead.
- Jim: on a match day, Ian's callout leads with kickoff-hour weather.
  Lightning is a safety line, not a joke — WVSSAC stops play for it and
  Ian is the one making that call. Home matches are at Ashton (Apple
  Grove's numbers are fair, and say so); away matches use the venue
  town's own forecast.

## 9. Open items

- **The Topsail water temperature moved stations — watch it this week.**
  NOAA dropped the `water_temperature` product from **8658163 Wrightsville
  Beach** outright (its own metadata no longer lists it; the datagetter
  refuses `latest` and a 72-hour range alike), which is what the nine
  omitted temperature lines through Aug. 24 actually were. Nate chose
  **8656483, Beaufort, Duke Marine Lab** — 60 miles up the coast, estuarine,
  the closest match in water TYPE to the sound the crew fishes. Wilmington
  (8658120) is nearer at ~30 miles but is Cape Fear RIVER water at the port
  and read 2F warmer the day the three were compared. First reading back:
  **85.1F, 2026-08-24 13:54**, zero source errors. **The station identity
  now lives in `config.TOPSAIL_TEMP_*` and NOWHERE else** — the fetcher
  imports it and the validator gates on it, so the next retirement is five
  lines. **Confirm the line actually prints tomorrow morning.**
- **DST on the four un-held crons** — due before 2026-11-01 (section 3).
- **Report card commitments** from the backfilled Aug 09–15 card: model
  QPF over about two inches is a ceiling stated as a range, and the
  Huntington warm bias gets checked every morning rather than
  remembered. The next card must say plainly whether they held.
- **Stale trips** in `weatherman/travel.json` (fair week, cabin weekend)
  — date-gated and inert, but pruning keeps the file readable.
- **Ian never answered** which WV outlets to trust; the notebook's
  source list is still provisional.

## 10. How to work here safely

1. `git pull --rebase` in both repos first — the routines commit several
   times a day and you WILL hit conflicts otherwise.
2. Tune behaviour by editing markdown in `instructions/`, not code. The
   next run picks it up; there is no deploy step.
3. Validate before shipping: `python validate_edition.py <file>
   [--sportsman]`. It is a hard gate and it is usually right.
4. Log notable changes in `docs/PATCH_NOTES.md` (weatherman keeps its
   own) and dated operational facts in `docs/LEDGER.md`.
5. **Update this file in the same commit.**
