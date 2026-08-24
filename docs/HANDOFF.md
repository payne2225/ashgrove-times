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

Last updated: **2026-08-24**

---

## 1. What this is

Three daily posts to the friends' Discord (Ashgrove Gaming), plus a
public website. Two repos:

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
| 5:30 | Wake, research BOTH papers before either posts | Times |
| 7:00 | **The News Desk** posts | Times |
| 7:05 | **Sports & Sportsman** posts | same routine |
| 7:15 | **Jim Claudtore's briefing** posts | weatherman |
| 8:00 | Watchdog — silent unless something failed | watchdog |
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

**DST is handled for the briefing only.** `post_discord.py --at` holds
Jim to 7:15 ET, so his slot survives the time change. The other crons are
still raw UTC and will each shift an hour on **2026-11-01** — the papers
to 4:30 ET, the weather page to 7:10, the report card to 17:00. Either
move them that week or give them the same hold.

## 4. The website

`https://payne2225.github.io/ashgrove-times/` — the **Newsstand**, a
static hand-kept page (`site/index.html`) that the renderer must never
write. It links the three sections:

| Section | URL | Written by |
|---|---|---|
| The News Desk | `/today.html` and `/editions/<date>.html` | `render_edition.py` |
| Sports & Sportsman | `/sportsman/` | `render_edition.py --sportsman` |
| The Weather Claude | `/weather/` | `render_edition.py --weather` |

Every section page carries THE ASHGROVE TIMES as a family banner above
its own masthead, plus nav buttons (Home and the other two sections)
**twice — under the masthead and again at the foot of the page** (Nate,
2026-08-24). A reader finishes at the bottom, which is where the decision to
read the next section gets made; the top row alone made that a scroll back
up. Both rows come from `_nav_html()` in `render_edition.py`, so they cannot
drift apart.
Pages build via GitHub Actions with **unbounded lag** — 23 seconds to 9
minutes observed. Post on time, backfill the link when the build lands.

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
