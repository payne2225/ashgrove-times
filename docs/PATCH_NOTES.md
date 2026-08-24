# Patch Notes — The Ashgrove Times

Running changelog. Dated entries, newest first. Touched only when
behavior changes, not every edition — the per-day record lives in
`editions/index.json`, and degraded runs go in `docs/FAILURES.md`.

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
