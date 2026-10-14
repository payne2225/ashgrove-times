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

Last updated: **2026-10-13**

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
drives everything. Since 2026-10-14 that includes the unattended 5:30
session, which writes Jim's briefing through a desk and posts him; the
narrow limit on what it may write in weatherman is in section 5.

## 2. The morning

**Rebuilt 2026-10-13, live from 2026-10-14 (Nate: "build it and plan for
DST hour changes").** One session, the Times routine, now runs all three:
it spawns a desk that writes Jim's briefing while it builds both papers,
and it posts the digest and Jim from one wake. Every time below is Eastern
and is the same all year.

| ET, all year | What | Who |
|---|---|---|
| fires 5:30 (+0 to 25 min) | `morning_gate.py` says GO; **Jim's desk spawns**; both papers researched and PUBLISHED | Times |
| about 6:00 to 6:15 | Jim's draft pushed to weatherman; **the weather page goes up from it** | Times |
| 6:55 | a `send_later` wake: claim Jim, hold the digest | Times |
| **7:00, held** | **The digest posts**: one message, what is in today's edition and a link to Home | Times |
| 7:08, held | refresh: a NEW warning, watch or SPC raise since Jim wrote goes under his dek | Times |
| **7:15, held** | **Jim Claudtore's briefing posts**; the post is recorded; the page re-rendered | Times |
| 7:32, 8:32, 9:32 (winter 7:32, 8:32) | **Standby**: posts Jim only if nobody has; almost every fire is one `DONE` | weatherman |
| every :30 | Alert watcher, silent unless something NEW | weatherman |
| 9:00 / 8:00 | Watchdog, silent unless something failed | watchdog |
| Sun 18:00 / 17:00 | Weekly report card | weatherman |

**"Held" means a script holds to the Eastern clock**: the digest by
`post_discord.py --not-before 07:00`, the refresh by `refresh_check.py
--not-before 07:08`, Jim by his `post_discord.py --at`. Each call holds
nine minutes at most and exits 12, having done nothing, when more is left;
the session runs it again. **Nothing holds in the background any more**:
the Times' old `setsid nohup` hold died with the container on nine mornings
in twelve, and the session now ends its first turn with a `send_later` and
does every post in the foreground of the wake.

**Why** (2026-10-04 to 10-13, measured): Jim posted between 7:25 and 7:43
every morning against his 7:15 slot. His own routine fired at 7:00 ET, the
scheduler started it 6 to 20 minutes late, and he wrote for 13 to 27. The
weather page, typeset after his archive, trailed him. From 2026-11-01 his
UTC cron would have meant 6:00 EST and a 30-to-55-minute hold that no cloud
tool call survives. Written at 5:45, he waits for his slot instead.

**What is still independent.** The digest never waits for Jim: if his
desk is late, the digest posts at 7:00 and Jim whenever his draft lands. A
paper that cannot find a lead posts no digest, and Jim still posts. If the
session dies outright, the standby posts Jim from 7:32 (late, but never
missing and never twice); nothing re-posts a lost digest, and the watchdog
reports it the next morning.

**Jim is posted once, by a lock in his archive.** `briefings/<date>.md`
is written at about 6:00 with `posted_at: pending`; whoever posts first
CLAIMS it on origin/main (`jim_gate.py`, git refuses a second push that is
not a fast-forward), and `posted` stamps the time afterwards. A claim lasts
30 minutes and never lapses before 7:45 ET, so the standby waits out a live
one and takes over a dead one. The watchdog and the report card read a
`pending` archive as a briefing that never reached the channel.

## 3. Live routines

All in environment `env_01HRBGRSDmfX7Vur76oE8Lkh`, all on
**`claude-fable-5-1`** (moved from `claude-fable-5` on 2026-09-02, verified
against the live configs; the model is the only field that changed).
Webhooks live only in task prompts and in gitignored `.env` files — never
in a repo. **Moving them into the routines' `environment_variables` was
tried on 2026-09-02 and is blocked by the API:** `RemoteTrigger update`
accepts `environment_variables` under `job_config.ccr`, at the top level
and under `job_config` without error and stores none of them (the stored
`session_request.environment_variables` stays `{}`); the one shape that
targets that field, `session_request`, is rejected for lacking a `worker`
object the API does not document. A diagnostic run of the alert watcher
(14:33 UTC) confirmed the sandbox sees no such variable. So the prompt text
IS the credential store until the API grows the field — one more reason
the prompts are thin and never committed. The sports webhook has no
consumer left in code and should be deleted in Discord.

**Routine prompts are thin pointers, not rulebooks** (2026-09-02). Each
prompt names the instruction file, says that file is AUTHORITATIVE, and
restates no rules. Two stale copies had already bitten: the Times prompt
still said "post TWO papers" and handed over the retired sportsman webhook a
week after the digest replaced both, and the watchdog prompt inlined the old
`alerts_state.json` mtime check right after telling itself to follow
`watchdog.md` — the direct cause of the 2026-08-30 false alarm. A rule
written in two places drifts; tune behaviour in `instructions/`, never in
the prompt. **The one deliberate exception** (2026-09-02): the alert
watcher's prompt carries its gate command — `check_alerts.py --heartbeat`,
stop on `0 new` — verbatim, because the saving is precisely not opening
the playbook on a quiet run. `weatherman/instructions/alerts.md` §0 has the
same command and says the two must change together.

| Routine | ID | Cron (UTC) |
|---|---|---|
| Ashgrove Times + Sports & Sportsman + Jim | `trig_01EMUikWUwB5GLE9GzGAPefb` | `30 9,10 * * *` |
| Weatherman Standby (was Daily Briefing) | `trig_01GeSVSait6X3Dwam8tkMycj` | `32 11,12,13 * * *` |
| Weatherman Alert Watcher | `trig_01AxyXnGTWwT4vXKWTv6w7Uq` | `30 * * * *` |
| Weatherman Weekly Report Card | `trig_01GTwkNWUrDkwMPi1XNx8MxZ` | `0 22 * * 0` |
| Weatherman Watchdog | `trig_01THzxTGHkdRgJWJwBZwjKQX` | `0 13 * * *` |
| Ashgrove Weather Page | `trig_01MEbyaBjFYcU4v9pERM4Paa` | **disabled** 2026-10-14, kept for rollback |

**The Times routine checks out both repos and carries two webhooks**
(2026-10-14): `TIMES_WEBHOOK` for ashgrove-times' `post_discord.py` and
`JIM_WEBHOOK` for weatherman's. Each script checks the webhook's ID before
it holds or posts (the Times compares a SHA-256 of it, so the public repo
never holds the ID; weatherman compares `config.WEBHOOK_ID`) and exits 3,
sending nothing, when handed the other one. Its prompt carries its gate
command, `python morning_gate.py`, stop on `DONE` or `EARLY`, verbatim:
the second thin-prompt exception, for the same reason as the watcher's.
The standby's prompt carries `python jim_gate.py standby` the same way.

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

**The watchdog checks six things** (2026-09-02): yesterday's briefing, the
watcher heartbeat, Monday's scorecard, yesterday's two edition files,
yesterday's `posted: true` in `editions/index.json` (an edition can be
published in full and still never reach the channel), and yesterday's
`site/weather/<date>.html`. All in `weatherman/instructions/watchdog.md`.

**DST needs nobody, in either direction** (2026-10-13). The crons stay
raw UTC on purpose: moving them twice a year is a chore that gets
forgotten, and code that computes Eastern time from the date is not. The
Times fires twice, at 09:30 and 10:30 UTC, and `morning_gate.py` lets one
build: 5:30 EDT and 6:30 EDT (`DONE`, or the backup if 5:30 never started)
in summer, 4:30 EST (`EARLY`) and 5:30 EST in winter. Its claim is
`editions/claim.json`, pushed to origin/main. The standby's 6:32 winter
fire is `EARLY` the same way, and every post is held to an Eastern time.
The clock is the US rule itself (second Sunday of March, first Sunday of
November) in `eastern.py` and `config.py`, not the sandbox's tz database,
and both test suites run 2026-10-31, 11-01, 2027-03-13 and 03-14. The old
"switch the Times cron on 2026-11-01" ledger row is superseded.

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
PROPORTION, and nothing truncates a long section any more. **The code that
posted the whole paper is gone** (2026-09-02): the trim ladder, the split,
text mode, the sportsman post and the link backfill were deleted from
`post_discord.py`, which now sends the digest and nothing else.
`build_payload()` survives only because the validator weighs sections off
it for that proportion advisory; its docstring says so.

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
| Back issues | `/archive.html` | `write_site` (both nav rows, like every page, since 2026-09-02) |
| RSS | `/feed.xml` | `write_site` — one item per Times edition, dated permalink, dek, 7:00 ET pubDate; Home's `<head>` advertises it (2026-09-02) |

**Type (2026-09-03).** Playfair Display is for what is set large or black:
masthead, lead headline, drop cap, section chips. Small mixed-case headlines
(brief heads, the back-issue list, stat-strip figures) use the `--headline`
token — Source Serif 4 at 600 — because Playfair's hairlines vanish at 16px
on a screen. Add a new small headline to the page and it takes `--headline`,
not `--display`.

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
Jim posts**; the renderer only ever reads his archived markdown. **Numbers
first, then the read** (Nate, 2026-09-03): every location block in the
briefing now opens with a numbers line Jim copies from
`weatherman/briefing_stats.py` — `H: 95° / L: 73° · feels 103° at 2–3 PM ·
Hum 35% · rain 2% · AQI 97` — and the page renders each such line as a table
above the prose (`_wx_stats_row`; one row per bold-prefixed place in a
stack). Channel and site show the same numbers by construction, because
both come from the fetcher and neither is retyped.

Every section page carries THE ASHGROVE TIMES as a family banner above
its own masthead, plus nav buttons (Home and the other two sections)
**twice — under the masthead and again at the foot of the page** (Nate,
2026-08-24). A reader finishes at the bottom, which is where the decision to
read the next section gets made; the top row alone made that a scroll back
up. Both rows come from `_nav_html()` in `render_edition.py`, so they cannot
drift apart.
**The weather page goes up before Jim posts** (2026-10-14). Pat, from
2026-10-03: *"sports and news is today but weather is yesterday."* The page
used to be typeset after Jim archived, by its own routine, and trailed his
post by minutes to an hour. Now the Times session renders it from his draft
at about 6:15 and again after the 7:15 post, so it carries any refresh line
and the text exactly as posted; the standby renders it when it posts him
instead. The Weather Page routine and `wait_for_briefing.py` are dormant,
kept for rollback (`instructions/weatherpage.md` says what to fix first).
The page's tagline still says Jim files at 7:15, which labels the slot.
Pages build via GitHub Actions with **unbounded lag** — 23 seconds to 9
minutes observed. Post on time, backfill the link when the build lands.

**The archive is safe to re-render — with `render_edition.py --all`, and
only that way** (2026-09-02). The sports page's tide table is the one live
read on any page; it now reads `editions/data/<date>.fishing.json` first,
which `render_edition.py --sportsman` freezes from `out/fishing.json` the
first time it renders a day's page and the routine commits with the
edition. The live file is used only when no snapshot exists AND it carries
the page's own date — the morning render itself. `--all` re-renders every
Times page (nothing live there), every sports page that HAS a snapshot,
every weather page whose briefing is in the `../weatherman` checkout, and
**refuses the rest by name**. Sports pages from before 2026-09-03 have no
snapshot and keep their committed HTML for good; do not hand-render one.
`today.html` and the index bookmarks are written from the newest edition
only. The Times archive was re-rendered once on 2026-09-02 and took the
flowed layout and the foot nav.

## 5. The one boundary left

**The unattended Times session writes exactly one thing in weatherman**:
`briefings/<date>.md`, and only through `jim_gate.py` (`draft`, `claim`,
`posted`, each a single-file commit pushed to origin/main). It never
commits anything else there, never edits a playbook or a script, never
touches a routine. Nate drew this line on 2026-10-13 when he moved Jim's
desk into the 5:30 session; it replaces the older rule that no unattended
job wrote to weatherman at all. The desk itself never commits, pushes or
posts. The interactive session may still develop weatherman freely.

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
  **MLB standings are byte-matched too** (from 2026-09-03):
  `fetch_standings.py` writes `out/standings.json` from MLB's keyless Stats
  API, `render_edition.py --sportsman` freezes it to
  `editions/data/<date>.standings.json`, and the validator refuses a record,
  games-back figure or ordinal — in the block or in any brief naming one MLB
  club — that is not in the file. MLS and the Premier League are not covered
  (no keyless source) and the instructions say so.
- **The away desk and Vacation Hotspots run EVERY morning** (Nate,
  2026-08-26: *"ALWAYS give us content... there is always stuff to
  report"*). Fourteen-day window; work the search ladder — local outlets,
  then the bodies that meet on a schedule (council, commission, school,
  DOT), then social media as a LEAD. An official account posting about
  itself IS citable; anybody else is a lead to confirm elsewhere. The
  validator refuses an empty block without a note naming what was searched,
  and (from 2026-09-03) an away or hotspots line with no day reference —
  the fourteen-day window is honest only because every line says when.
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
   If his time moves, `instructions/edition.md`, `instructions/routine.md`
   and weatherman's `post_discord.py` (`TARGET_ET`) all change together.
2. **Topsail is split** (2026-08-21): the **weather** is Jim's, the
   **water** — tides, moon, what's running — belongs to Sports &
   Sportsman. `reference/topsail-fishing.md` lives HERE only; the
   weatherman copy was deleted 2026-08-23 to stop the drift.
3. **Jim himself** (2026-10-14) — the Times session spawns his desk,
   pushes his draft, renders his page and posts him; `jim_gate.py` and
   `refresh_check.py` live in weatherman, `morning_gate.py` here. A change
   to his flow touches `instructions/routine.md` here and `briefing.md`,
   `standby.md`, `watchdog.md` and `report-card.md` there. See §2 and §5.
4. **Hannan soccer** — `reference/hannan-soccer-2026.json` exists in
   BOTH repos, because each routine checks out only its own. Correct
   one, correct the other.
5. **Punta Cana — DORMANT.** The Sept. 12–18 trip moved to April 2027
   (Pat, via Nate, 2026-09-09). The machinery stays in weatherman
   (`tropics.py`, the briefing's Atlantic section, the watcher's NHC
   triggers) and is switched on by a `tropics_watch` block on the
   `punta_cana` location in `weatherman/config.py`; the comment there is
   the re-arm recipe. Nothing runs while the block is absent.
6. **Ohio Bobcats home games** (Pat, via Nate, 2026-09-09). Weatherman
   only: `athens_oh` location, `reference/ohio-football-2026.json` (six
   home games from ESPN's schedule API), a `bobcats` block in `data.json`,
   and a briefing section that exists only on home-game days. Sports &
   Sportsman already follows Ohio for results; its fixtures file is not
   mirrored here yet — if the sports desk starts using one, mirror it
   the way Hannan's is.

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

- **The new morning starts 2026-10-14 — read its first reports.** The
  first one (2026-10-14) ran clean: digest 7:00:01, Jim 7:15:03, every
  standby fire `DONE` (PATCH_NOTES has the clock). Built
  2026-10-13 (§2). Check, on the first few mornings: the gate line; when
  Jim's desk reported and the weather page went up; that the wake arrived
  near 6:56; the digest at 7:00 and Jim at 7:15; `MARKED`; and that every
  standby fire said `DONE`. The first winter morning is **2026-11-01**: the
  4:30 fire must say `EARLY`, the 5:30 fire `GO`, and the standby's 6:32
  fire `EARLY`. Rollback, if it misbehaves: Times cron back to
  `30 9 * * *` with the old prompt, Jim's routine back to `0 11 * * *`
  with his old prompt (both in weatherman `docs/ROLLBACK-2026-10-14.md`,
  webhooks redacted), the Weather Page routine re-enabled, and this
  commit's instructions reverted. Not
  built, on purpose: a standby for the digest. If the session dies, the
  watchdog says so the next morning and Nate decides.

- **The 2026-09-02 full pass landed items 1–10** (tests, snapshots and
  `--all`, the retired embed path, DST holds, watchdog checks, standings
  byte-match, RSS, the date-word gate, the small marks). Its work order,
  `docs/HANDOFF-FULL-PASS-2026-09-02.md`, is now a summary; the detail is
  in `docs/PATCH_NOTES.md` under 2026-09-02. **Three threads it left open:**
  - **Item 6, webhooks out of prompt text — blocked by the API** (§3).
    Nate deleted the sports webhook in Discord on 2026-09-02; nothing is
    left of it anywhere.
  - **Item 11, the alert watcher's cost — DONE 2026-09-02** (Nate: "do it").
    The routine's prompt now opens with the gate command
    (`check_alerts.py --heartbeat`) and a quiet run ends on its OK line
    without opening the playbook; only a run with something new reads
    `weatherman/instructions/alerts.md`. No second routine. The gate is the
    one rule stated in both the prompt and the playbook, by design.
  - **Item 12, the weatherman grader has no tests.** `weatherman/verify.py`,
    `instructions/report-card.md` and `briefing.md` were not reviewed;
    "grade inflation is the one unforgivable failure" has nothing behind it
    but the prompt. Same treatment as item 1 when there is a session for it:
    pytest over `verify.py`'s scoring with a fixture week, and a test that a
    card whose grades exceed its own bust list is refused.
- **The three 2026-09-03 gates** (MLB standings byte-match, the date-word
  rule, the standings snapshot) passed on their first morning and every
  morning since; nothing to watch there any more.
- **Saturday 2026-09-12 is the first Bobcats home game** under the new
  weatherman section (§7 item 6): Jacksonville State, 6 p.m. at Peden.
  Read that morning's briefing — the section should exist only that day,
  lead with the kickoff window, and tag Pat. The Oct. 10 and Oct. 24
  kickoffs are TBD in `weatherman/reference/ohio-football-2026.json`
  until ESPN posts them; re-fetch the file when they do. Verified
  2026-09-09 afternoon: `bobcats_games()` returns `today: null` for the
  9th and the Jacksonville State game for the 12th, ESPN's live feed still
  says 6:00 p.m. ET, weatherman's 23 tests pass. **Thursday 2026-09-10 is
  the first briefing with `athens_oh` in `data.json`** — read it and
  confirm it says nothing about Athens or the Bobcats on a non-game day.
  The alert watcher polls `athens_oh` every half hour like any other
  location, so a significant NWS alert at Peden would post on a weekday
  with nobody tagged; that matches how the other unoccupied special
  locations already behave, and Nate has not been asked whether he wants
  it.
- **Punta Cana re-arm** when Pat sends April 2027 dates: the recipe is the
  comment on the `punta_cana` location in `weatherman/config.py`, plus a
  `travel.json` trip.
- **The weather page shows numbers first** since 2026-09-03 (§4) and small
  headlines left Playfair the same day; the back issues still wear the old
  type until someone runs `render_edition.py --all`, which is safe and
  changes only what the template changed.

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
4. **Run `pytest -q` before pushing anything that touches a `.py`** (since
   2026-09-02). The suite is offline and takes seconds; CI runs it as a
   gate in front of every deploy, so a red test blocks the morning's pages.
   `tests/test_contracts.py` holds one committed edition per contract date
   (08-05, 08-15, 08-25, 08-26, 08-27) with its own stats and fishing file
   under `tests/fixtures/` — **any change to the validator must leave those
   green**, and that is how a rule that is not date-scoped gets caught. If
   an archived edition in `editions/` is legitimately corrected, copy it
   over its fixture again; the test compares them byte for byte.
5. Log notable changes in `docs/PATCH_NOTES.md` (weatherman keeps its
   own) and dated operational facts in `docs/LEDGER.md`.
6. **Update this file in the same commit.**
