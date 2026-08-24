# The Ashgrove Times

> **Picking this up fresh? Read [`docs/HANDOFF.md`](docs/HANDOFF.md)
> first.** It is the living state of both papers — the schedule, the
> routines, the boundaries, and what is still open. Keep it current: if
> you change something here or in the weatherman repo, update that file
> in the same commit.

A newspaper-styled daily news digest for the friends' Discord channel —
masthead, drop cap, section rules, stat strip. Five sections every
morning: a lead story, then U.S., World, West Virginia, and Science &
Technology — **four briefs per wire section** since Sports retired to its
own paper, Sports & Sportsman, on 2026-08-16 (sumo and the Premier League
moved with it; see `instructions/sportsman.md`). Content is researched
fresh by web search each day, never pulled from a static feed.

West Virginia is not another wire section. It is the paper's local anchor:
a boxed **Mountaineer State Notebook** carrying statewide briefs, a
one-sentence roundup of the crew's own regions, an away desk for the
members who live out of state, and a fishing report for the two waters
they actually fish. See [The West Virginia notebook](#the-west-virginia-notebook).

Handed off from Ian, who prototyped it as a single self-contained HTML
artifact. His original brief is preserved at `docs/HANDOFF-FROM-IAN.md`.
His **real template arrived 2026-08-05** as `docs/IAN-TEMPLATE.html` and is
now the **design authority**: `templates/broadsheet.html` matches its
structure and tokens, and where any reconstruction disagreed with it, the
template won. Neither of those two files is ever edited — they are inputs.

Runs as a scheduled cloud Claude Code routine every morning (**7:00 AM
ET**), posting via a Discord webhook, and signs off with a pointer to
Jim Claudtore's 7:15 forecast — the *weather ear*. Same
architecture as `weatherman` and `odds-ev-finder`: no servers,
prompt-as-markdown in `instructions/`, secrets passed via the routine's
task prompt (never committed).

**Nothing has shipped yet.** No webhook, no GitHub remote, no first
edition — see [Still open](#still-open).

## What actually lands in the channel

One message. Three surfaces at once:

1. a top-level `content` masthead line (and the permalink, when the web
   tier is on), closing with the **weather ear** — one short line telling
   the channel the forecast lands at 7:15,
2. **five embeds** — LEAD, U.S., World, West Virginia, Science &
   Technology — which are the readable paper and are always complete. The
   West Virginia embed carries the notebook: statewide briefs, then the
   regional roundup, the away desk, and the fishing lines as fields,
3. one attached **1200x630 hero card PNG** (parchment, masthead, rules,
   lead headline, drop cap, byline, stat strip) rendered in-sandbox by
   Pillow from vendored fonts.

The embeds are primary; the PNG is identity. The hero is *strictly
additive* — drop the `attachments` array and the lead embed's `image`
block and you get a byte-identical JSON POST that is still a complete
newspaper. That property is the backbone of the whole fallback ladder.

Nothing arrives as a second message. Nothing arrives late.

## Pieces

| File | What |
|---|---|
| `config.py` | Section metadata (id/label/emoji/color/order/standing/trim_priority), `REGIONS` (the WV regions + away desk, with first names attached), palette, masthead strings, every Discord budget constant, `PAGES_ENABLED`, font paths, `SUMO_BASHO_MONTHS`, `section_by_id()` |
| `fetch_stats.py` | Stat-strip numbers: Yahoo v8 chart -> CoinGecko -> empty. Always exits 0, always writes `out/stats.json` |
| `fetch_fishing.py` | The two fishing waters: USGS gauge for the Williams River at Cowen, NOAA CO-OPS tides + water temp for Topsail. Writes `out/fishing.json`. Every source individually guarded — one outage nulls one reading and records why |
| `validate_edition.py` | The hard gate — schema, section order, standing sections, stat-strip truth check, WV notebook shape, placeholder detection, Discord budgets, URL liveness |
| `render_edition.py` | `render_html()` -> `site/editions/YYYY-MM-DD.html`; `render_hero_png()` -> `out/ashgrove-YYYY-MM-DD.png` (Pillow, fully offline) |
| `post_discord.py` | Payload build, pre-send refusal gate, deterministic trim, split, text mode, multipart POST, ledger append |
| `templates/broadsheet.html` | The one place visual language lives. Token substitution, no template engine. Matches `docs/IAN-TEMPLATE.html`, including the `.wv-box` treatment |
| `assets/fonts/` | Vendored OFL TTFs (static instances) — what makes the hero render work with no network |
| `assets/masthead-fallback.png` | Static banner attached when the hero render fails |
| `editions/YYYY-MM-DD.json` | The canonical content contract — the ONLY interface between components |
| `editions/_fixture.json` | Committed worst-case edition; catches layout and budget regressions offline |
| `editions/index.json` | Delivery ledger — edition numbers, `posted` flags, message ids, degraded paths |
| `instructions/edition.md` | The daily playbook the cloud routine follows end to end |
| `instructions/style.md` | Voice: AP-style, terse, no fluff. Separated so tone tunes without touching the pipeline |
| `docs/LEDGER.md` | Editorial memory — open threads, forward-dated events, recently-covered slugs |
| `docs/FAILURES.md` | Append-only degraded-path log |
| `docs/RUNBOOK.md` | "No paper in the channel at 7am" decision tree |
| `docs/PATCH_NOTES.md` | Running changelog |
| `docs/HANDOFF-FROM-IAN.md` | Ian's original brief. Preserved as-is, never edited |
| `docs/IAN-TEMPLATE.html` | Ian's real template (2026-08-05). **The design authority.** Structure and tokens only, no content. Never edited |

## Data flow

```
  WebSearch (Claude, in the routine)   fetch_stats.py   fetch_fishing.py
              |                               |                |
              |                               v                v
              |                        out/stats.json   out/fishing.json
              |                               |                |
              +---------> editions/YYYY-MM-DD.json <-----------+
                                        |   stat values byte-matched;
                                        |   fishing lines trace to the file
                       +----------------+----------------+
                       |                                 |
                       v                                 v
              validate_edition.py                render_edition.py
              (exit 1 = STOP)                     |            |
                                                  v            v
                                   site/editions/*.html   out/ashgrove-*.png
                                                  |            |
                                          git push |            |
                                                  v            v
                                          GitHub Pages   post_discord.py
                                                  \            /
                                                   \          v
                                                    +--> Discord webhook
                                                              |
                                                              v
                                                     editions/index.json
```

The edition JSON is content only — no emoji, no colors, no display
metadata, ever. Everything downstream of the write step is deterministic
Python that Nate can re-run with no model in the loop.

## The West Virginia notebook

Ian's template gives West Virginia its own treatment — `.wv-box`: a 2px
`#1c1a16` border, an `#ede7d6` tint, and a **Mountaineer State Notebook**
title in 20px 900-weight Playfair — instead of the two-column brief layout
every other section uses. That distinction is doing work: it makes WV read
as the local anchor of the paper rather than another wire section. It
survives into the HTML and into any Pillow-drawn WV card.

Nate expanded the notebook on 2026-08-05. It now has **four parts**, and
only the first is mandatory:

| Part | What | Shape |
|---|---|---|
| Statewide | 2–3 real WV items | normal briefs — headline + summary + source |
| Regional | the crew's own markets | **one sentence each**, only where there is genuine news |
| Away desk | crew who live out of state | **one sentence each**, same rule |
| Fishing | the two waters they fish | one line per water, from `out/fishing.json` |

**Lean is a hard instruction.** Regional and away items are one sentence,
not briefs. A day where three regions have nothing is a normal day, and
the honest version is three fewer lines.

### The regions

Taken from the sibling `weatherman` project's `LOCATIONS` and grouped into
real WV media markets, because Lesage has no daily news of its own and a
line per hamlet is how a paper starts inventing. They live in `config.py`
as `REGIONS` so the playbook and the renderers share one source of truth.

| `region_id` | Place | Who |
|---|---|---|
| `huntington_cabell` | Huntington & the Cabell-Mason corridor | Trav, Justin, Nate, Ian |
| `putnam_kanawha` | Putnam / Kanawha — Charleston | Nate (work) |
| `mid_ohio_valley` | Mid-Ohio Valley / Parkersburg | Pat |
| `nicholas_webster` | Nicholas & Webster / Summersville — Cowen | Clayton, and the cabin |
| `summers_new_river` | Summers / Hinton & the New River | Greg |

Away desk — out of state, still crew:

| `region_id` | Place | Who |
|---|---|---|
| `vermont` | North Bennington, VT | Wes |
| `british_columbia` | Prince George, BC | Kirsten |
| `topsail` | Topsail Beach, NC | the beach place |

**First names only, ever.** No Discord user IDs, no addresses, no ZIP
codes anywhere in this repo — it is going public for Pages, and the ping
policy is no-ping. (`weatherman`'s config has ZIPs and coordinates; they
stay there.)

### Fishing

`python fetch_fishing.py` writes `out/fishing.json` before the edition is
written. Two waters, both keyless and free:

- **Williams River (Cowen)** — USGS instantaneous values at gauge
  `03186500`, *Williams River at Dyer*: discharge, stage, and water
  temperature when the gauge reports it, each with a 24-hour trend. The
  fetcher's own `read` string states wadeability, and water temperature
  outranks flow — above 70°F it says to leave the trout alone.
- **Topsail Beach** — NOAA CO-OPS tide predictions from the two stations
  that bracket New Topsail Inlet (`8657419` Ocean City Beach pier, ocean;
  `8657813` Hampstead, sound — they disagree by ~75 minutes and are
  reported separately, never averaged), plus water temperature from
  `8656483` **Beaufort, Duke Marine Lab, 60 miles up the coast** (since
  2026-08-24 — NOAA dropped the product from `8658163` Wrightsville Beach,
  which had held the job until then).

That last attribution is not optional: the Topsail water temperature is
the borrowed station's and must be labeled as the borrowed station's.
**When a source fails, the line is omitted** — the fetcher records the
error and never substitutes a plausible number. USGS 503s happen; a morning with only the
Topsail line is a correct morning.

WVDNR's trout-stocking page serves an **expired TLS certificate**, so
stocking is a web-search item in the playbook with a silent no-op
fallback, never a fetch. Do not "fix" that with `verify=False`.

### The contract addition

Every other section keeps the plain `{"briefs": [...]}` shape. Only `wv`
gains fields, and all three new arrays are optional and may be empty:

```json
{"id": "wv", "label": "West Virginia",
 "notebook_title": "Mountaineer State Notebook",
 "briefs":   [ {"headline": "...", "summary": "...", "source": "...", "url": "..."} ],
 "regional": [ {"region_id": "huntington_cabell",
                "place": "Huntington & the Cabell-Mason corridor",
                "people": ["Trav", "Justin", "Nate", "Ian"],
                "item": "ONE sentence.", "source": "WSAZ", "url": "https://..."} ],
 "away":     [ {"region_id": "vermont", "place": "North Bennington, VT",
                "people": ["Wes"], "item": "ONE sentence.",
                "source": "...", "url": "..."} ],
 "fishing":  [ {"water": "Williams River (Cowen)",
                "line": "110 cfs and falling - prime wading water.",
                "source": "USGS 03186500"} ]}
```

The edition also carries a top-level `"weather_ear"` string alongside
`kicker` and `sources_note`.

## The weather ear

The paper posts at 7:00 AM ET; Jim Claudtore posts the forecast to
the same channel at 7:15. A newspaper already has the right convention for
that pointer — the **weather ear**, the small boxed item beside the
masthead — so that is what it is.

It appears in the `.top-bar` area of the HTML, as the closing line of the
Discord post, and on the hero PNG when it fits without crowding the
masthead. It is written fresh each day into `edition.weather_ear`:
**vary the wording**, keep it short, and make it read like a newspaper
pointer rather than an ad. "Jim Claudtore files the forecast at
7:15" is the shape, not the frozen string.

## Local dry run

```
pip install -r requirements.txt

python fetch_stats.py                                    # -> out/stats.json
python fetch_fishing.py --pretty                         # -> out/fishing.json
# a Claude session writes editions/2026-08-05.json to the contract
python validate_edition.py editions/2026-08-05.json --stats out/stats.json
python render_edition.py --date 2026-08-05               # -> site/ html + out/ png
python post_discord.py --date 2026-08-05 \
    --attach out/ashgrove-2026-08-05.png --dry-run       # prints exact payload
python post_discord.py --date 2026-08-05 \
    --attach out/ashgrove-2026-08-05.png --test          # posts to test webhook
```

`--pretty` prints a human summary of both waters plus any source errors —
the fastest way to see whether a missing fishing line is an outage or an
editorial choice.

Regression-test layout and budgets without burning a news day — the
fixture is a deliberate worst case (absurd headlines, 6 stat entries, 4
briefs a section, one null url, and a fully loaded WV notebook: statewide
briefs plus every region, the whole away desk, and both fishing lines):

```
python render_edition.py --fixture
python post_discord.py --date 2026-08-05 --edition editions/_fixture.json --dry-run
```

Useful flags: `--no-urls` (skip liveness checks when offline),
`--no-image` (prove the JSON-only path), `--text` (prove the markdown
fallback), `--force` (override the already-posted gate).

### Exit codes

| Script | 0 | 1 | 2 |
|---|---|---|---|
| `fetch_stats.py` | always (writes a file even on total failure) | — | — |
| `fetch_fishing.py` | at least one water read | both waters dead (file still written) | — |
| `validate_edition.py` | clean | one or more `ERROR:` lines on stderr | — |
| `render_edition.py` | HTML + PNG written | HTML failed (hard) | HTML fine, PNG failed (soft — pipeline continues) |
| `post_discord.py` | posted | refused or failed | — |

## Discord webhook setup

**The webhook does not exist yet.** Nothing has ever posted. Creating it
is step one of going live.

Channel Settings -> Integrations -> Webhooks -> New Webhook -> Copy
Webhook URL. A webhook is per-channel: it can only ever post to that one
channel, which is what makes it safe to hand to a cloud run.

Put it in a local `.env` (gitignored, see `.env.example`):

```
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
DISCORD_TEST_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

The cloud routine never reads `.env` — it gets the URL from its task
prompt. Nothing else in this project is a secret.

**No pings.** There are no Discord user IDs anywhere in this repo and
there is no daily mention. `allowed_mentions` is `{"parse": ["users"]}`,
and the paper mentions nobody, so nothing notifies. That is deliberate:
the repo is public.

## Hosting the full broadsheet

GitHub Pages, publishing `site/` from a public `payne2225/ashgrove-times`
repo via `.github/workflows/pages.yml`.

```
https://payne2225.github.io/ashgrove-times/                       today's paper
https://payne2225.github.io/ashgrove-times/editions/2026-08-05.html  dated permalink
https://payne2225.github.io/ashgrove-times/archive.html            back issues
```

The Discord post always links the **dated** URL so old posts stay
correct. The routine pushes *before* it posts, then polls the URL for a
200 (max 120s) — a link that 404s for the first reader is worse than no
link at all, so a failed poll just omits the line.

Publishing from `site/` and not `/docs` is deliberate: `docs/` holds
Ian's handoff and the runbook, and those must not become web pages.

### Why the repo is public

Free-plan Pages only publishes from a public repo, and Nate chose public
on 2026-08-05 to get the web tier. That makes every file here
world-readable, which is why the privacy rules are enforced in code and
not just documented: the webhook lives only in a gitignored `.env` and
the routine's task prompt, there are no Discord user IDs, ZIPs, street
addresses, or employer names anywhere in the tree, people appear by first
name only, and `regional`/`away` rosters are validated against
`config.REGIONS` so no other name can enter an edition.

**Re-run that sweep before adding anything to this repo.** The audit that
caught the last round found a personal email in a `User-Agent` header and
two `note` fields locating where a specific person works and where the
cabin sits — none of it rendered anywhere, so no one reviewing the
published site would have seen it. Source is what going public exposes.

`PAGES_ENABLED` remains the single kill switch. Set it `False` and
`build_payload()` omits the permalink line and drops every `embed.url`;
no other code path changes, and the paper still posts.

## Activation status

Settled on 2026-08-05, in the order the blockers fell:

1. ✅ **Discord webhook.** Nate supplied it; it resolves to a webhook named
   `newspaper` in **its own channel**, separate from Claude the
   Weatherman's. Stored in the gitignored `.env`; the cloud routine gets
   it from its task prompt instead. Never commit it.
2. ✅ **GitHub repo.** `payne2225/ashgrove-times`, **public**, default
   branch `main`.
3. ✅ **`PAGES_ENABLED = True`.** Pages builds from
   `.github/workflows/pages.yml` (`build_type: workflow`) and serves at
   `https://payne2225.github.io/ashgrove-times/`. The first deploy fires
   on the first push that writes `site/index.html`.

### Still open

4. **The WV outlet list is unconfirmed by Ian.** The named outlets in
   `instructions/edition.md` (MetroNews, WV Watch, Mountain State
   Spotlight, WVPB, WSAZ/WOWK/WCHS, Herald-Dispatch, News and Sentinel,
   Gazette-Mail, and the regional dailies) are Claude's list, not Ian's.
   The regional roundup leans on them hardest, since a market line is
   only as good as the local paper behind it. Worth one message to Ian —
   especially for Nicholas/Webster and Summers, the two thinnest markets.

## The delivery ladder, in one glance

The group always gets a readable edition. Each rung degrades one thing
and keeps the paper:

| # | When | What still ships |
|---|---|---|
| 1 | Everything green | Masthead line + 6 embeds + hero PNG + permalink |
| 2 | Hero render failed | Same message, `assets/masthead-fallback.png` instead |
| 3 | No image at all | Byte-identical JSON POST, no picture. Invisible to everyone but the log |
| 4 | Pages down or disabled | All content, no links |
| 5 | Over 5800 chars | Trim last brief: scitech, world, us, sports, round-robin. Lead never trimmed |
| 6 | Still over | Split: FRONT PAGE (lead + US + World), INSIDE (WV + Sports + SciTech), 1s apart |
| 7 | Discord 400s the embeds | `--text` mode: plain markdown, chunked at 1900 |
| 8 | 429 / 5xx | Honor `retry_after`; 3 backoff attempts, then one more after 10 min |
| 9 | `requests` unimportable | Hand-built multipart over stdlib `urllib.request` |
| 10 | Webhook dead / routine never fired | JSON + HTML are already committed; Nate posts from his PC |
| 11 | A section has no news | 2 briefs, or one honest roundup. WV and Sports always appear |
| 12 | All stat sources down | `stat_strip: []` and both renderers omit the band. Never a placeholder number |
| 13 | Lead cannot be sourced at all | **Nothing ships.** Write `docs/FAILURES.md` and abort |

Rung 13 is the only place the pipeline is allowed to publish nothing. A
missing paper is recoverable; a fabricated front page is not.

The same rule runs one level down inside the WV notebook: `regional`,
`away`, and `fishing` are optional arrays, and a region with no news gets
no line rather than a manufactured one. Statewide briefs always appear. A
fishing water whose source failed is omitted, never estimated — the reason
is in `out/fishing.json` under `errors`.

## The routine

Cloud Claude Code, **Opus**, daily at **7:00 AM ET** — 15 minutes ahead of
Jim Claudtore's 7:15 slot, which the paper points at with the
weather ear instead of pretending it does not exist. Cron is UTC-fixed
(`0 11 * * *`), so it drifts to 6:00 AM ET when standard time returns in
November.

The routine follows `instructions/edition.md` verbatim: pull, read the
ledger, hit the idempotency gate, research section by section, fetch stats
and fishing, write the edition JSON, validate, render, push, wait for
Pages, post, record, report.

Two research rules it does not get to reinterpret:

- **Sumo gets its own dedicated search every day, basho month or not — but
  it only gets a brief when there is something to cover.** Ian settled
  this: a banzuke, a promotion, or a retirement line is enough. During a
  tournament (odd months — Jan, Mar, May, Jul, Sep, Nov, 15 days each)
  sumo should usually *win* the sports lead, because that is when things
  are happening. Off-months, a one-line note is the honest version of "no
  sumo news," and manufacturing a headline to fill the slot is the failure
  mode, not the fix.
- **Three briefs per section.** Ian confirmed it. That is the number that
  takes the clean single-message win instead of forcing a two-message
  split.

Its only creative output is the edition JSON. Everything else is code.

## KILL SWITCH

- **Stop tomorrow's paper:** pause or delete the scheduled cloud routine.
  That is the real off switch — nothing else runs on a timer.
- **Stop it posting at all, right now:** delete the webhook in Discord
  (Channel Settings -> Integrations -> Webhooks). Every code path 404s
  and logs; nothing else in the repo can reach the channel.
- **Stop only the web tier:** `PAGES_ENABLED = False` in `config.py`.
  Posts keep going out, minus the permalink and embed links.
- **Stop only the picture:** run with `--no-image`. Same complete paper.
- **Accidental double post:** cannot happen. The idempotency gate reads
  `editions/index.json` and refuses a date already marked `posted: true`
  unless `--force` is passed.

To ship a missed day by hand from Nate's PC:

```
python post_discord.py --date 2026-08-05 --attach out/ashgrove-2026-08-05.png
```

`docs/RUNBOOK.md` has the full 7am decision tree.

## Traps (do not relearn these)

- **Discord `content` is hard-capped at 2000 chars** regardless of Nitro.
  The 6000-char embed cap is the **sum** of title + description + field
  names + field values + footer + author **across all embeds in the
  message**. `embed.url` and `image.url` are not counted — clickable
  titles are free.
- **Mentions only ping from top-level `content`.** Embed text renders
  `<@id>` and never notifies.
- **Masked links `[AP](url)` render inside embeds only.** In `content`,
  use a bare URL in angle brackets `<https://...>` to suppress unfurling.
- **Ian's handoff decimal color is wrong.** It states `#3E3221 ->
  3419169`; `0x3E3221` is actually `4076065` (`3419169` is `0x342C21`).
  `config.py` computes colors with `int(hex, 16)` at import. Never
  hand-convert.
- **stooq is dead** — every CSV symbol 404s. Verified. The ladder is
  Yahoo `v8/finance/chart` -> CoinGecko `simple/price` -> empty.
- **WVDNR serves an expired TLS certificate.** The trout-stocking list is
  therefore a web-search item in the playbook with a silent no-op
  fallback, never a fetch. Reaching it means `verify=False`, which is not
  worth a stocking line.
- **The Topsail water temperature is borrowed**, currently Beaufort's, 60
  miles up the coast — station `8657419` has no temperature sensor. It
  ships with the station name and distance attached. Printing it as
  Topsail's own water temperature is a fabrication, just a quiet one. The
  station is not permanent: Wrightsville Beach held the job until NOAA
  retired its thermometer in August 2026, and six mornings ran without a
  temperature before anybody asked why. `config.TOPSAIL_TEMP_*` is the one
  place that identity lives; the fetcher and the validator both read it.
- **The two Topsail tide stations are not interchangeable.** Ocean City
  Beach pier is open coast; Hampstead is behind the island and lags by
  roughly 75 minutes. Both are reported and labeled; averaging them
  produces a number that is true nowhere.
- **NOAA answers 200 with an error body**, so `raise_for_status()` never
  fires — `fetch_fishing.py` checks for an `error` key instead. USGS
  returns real 503s during maintenance; that is a normal degraded morning
  and the Williams line simply does not run.
- **WeasyPrint has had no PNG output since v53** (Cairo replaced by
  pydyf, PDF only). Playwright wants a ~160 MB Chromium download from a
  CDN the restricted sandbox may 403. `wkhtmltoimage` is a dead apt
  binary. Pillow ships self-contained manylinux wheels with FreeType
  bundled — that is why the hero is Pillow.
- **Discord scales an attached image to roughly 550px wide.** A full
  broadsheet page renders as unreadable 10px body type. Hence 1200x630 at
  1.91:1, which is legible at exactly the size Discord actually shows.
- **The cloud sandbox is restricted** — no SMTP, egress-403s many hosts,
  no system browser, no guaranteed heavy binaries. Prefer stdlib +
  `requests`. Treat a 403 as ALIVE during URL liveness checks; paywalls
  and sandbox egress produce the same status.
- **No emoji in any render.** Pillow cannot draw color emoji and the
  broadsheet does not want them. Stat-strip arrows are drawn as polygons,
  not glyphs — the vendored serif TTFs have no arrow characters and a
  miss renders as tofu. Emoji appear only in Discord embed titles.
- **Never a line per hamlet.** The regional roundup is grouped into media
  markets on purpose: Lesage and Apple Grove have no daily news of their
  own, and a template that demands a line per town is a template that
  teaches the model to invent one. Regions come from `config.REGIONS`, and
  a region with nothing gets nothing.
- **Sumo is not a daily headline requirement.** The validator must not
  demand one — Ian's rule is "sumo gets covered when there's something to
  cover." The daily *search* is still mandatory; the daily *brief* is not.
- **Never fabricate.** A `stat_strip` value may exist only if it
  byte-matches `out/stats.json`, and a fishing line may exist only if
  `out/fishing.json` carries the reading behind it. A thin section runs 2
  briefs and the kicker says so.
