# Full pass — work order for the next session

**Written 2026-09-02.** Nate: *"we're going to go ahead and do a full pass to
fix everything."* This is the order of work, the specifics, and the traps.
It is a WORK ORDER, not the living state — that is `docs/HANDOFF.md`, and
you read it first, in full, before this.

The review this comes from: [Ashgrove Blue Pencil](https://claude.ai/code/artifact/af4cdd32-d0b0-472e-88fb-8be5389c4300)
(private artifact; the substance is all repeated here so you do not need it).

## The one rule that governs the whole pass

**The routine runs at 5:30 ET every morning off `main`.** Every commit you
push must leave `main` in a state that routine can run. In practice:

- Any change to the edition CONTRACT (validator rules, section shapes, new
  required fields) is **date-scoped to tomorrow** — `since`, `*_REQUIRED_FROM`,
  `WV_SUBHEADS_CHANGED_ON` are the existing patterns in `config.py`. Today's
  edition already shipped under today's rules and must keep validating.
- Any change to `instructions/*.md` is live at the next 5:30. Write it as
  the desk will read it at 5:30 with no context.
- Push after every item. Do not batch the pass into one commit.
- `docs/HANDOFF.md` is updated **in the same commit** as any change to how
  the papers work. `docs/PATCH_NOTES.md` gets a dated entry per item.

## Already done — do not redo

- All six routines on `claude-fable-5-1` (2026-09-02).
- Routine prompts are thin pointers; the Times and watchdog prompts were
  rewritten 2026-09-02 and restate no rules.
- Alert watcher heartbeat (`last_run_utc`, `--heartbeat`) and the watchdog
  reads it (2026-08-30).
- Digest post, sections flow, anchors, Canada tiers, Vacation Hotspots,
  never-empty blocks, `result` on sports briefs, source links in new tabs,
  tide table under the Topsail line — all live. See `docs/PATCH_NOTES.md`.

## The pass, in order

Order is dependency-driven: tests protect everything after them; the
snapshot makes re-rendering safe before anything re-renders.

### 1. Tests — `tests/` with pytest

**Why:** `validate_edition.py` is 3,405 lines, every gate the paper has, and
has zero tests. Every change to it in the last fortnight was verified by
hand in a terminal. A shell-escaping bug wrote eighteen literal backspace
characters into it and was caught only because a regex stopped matching.

**Do:**
- `tests/test_direction.py` — the eight result-direction cases (passive
  with score interposed, city-vs-nickname, "fell to", "lost to", no-verb →
  None). They are in the 2026-08-26 commit message and in
  `_sm_result_direction`'s docstring.
- `tests/test_attribution.py` — the four Topsail water-temperature cases
  (no temp, uncredited, credited Beaufort, credited wrong station) and the
  `working`-field exclusion.
- `tests/test_standings.py` — the ordinal contradiction ("second-place
  Pittsburgh" vs a standings line saying fourth) and the games-back reuse
  advisory.
- `tests/test_contracts.py` — one committed fixture edition per contract
  date (2026-08-05, 08-15, 08-25, 08-26, 08-27) that must validate with
  `--no-urls` and with a matching `out/`-style stats/fishing fixture, so
  the archive can never be silently invalidated again. Use real editions
  from `editions/` copied into `tests/fixtures/`; strip nothing.
- `tests/test_notebook.py` — never-empty away/hotspots with and without
  the note; promoted region refused after the date, accepted before.
- `tests/test_digest.py` — `build_digest_payload` on a fixture: one
  message, under 2,000 chars, links `home.html`, reading order matches
  `config.sections_in_reading_order`.
- Add a `test` job to `.github/workflows/pages.yml` that runs before
  deploy. A red validator blocks a deploy.

**Verify:** `pytest -q` green; push; confirm the Actions run is green.

### 2. Make the archive safe to re-render

**Why:** `render_edition.py::_tide_table_html` reads `out/fishing.json`
LIVE while everything else on a page comes from the edition JSON. Twice in
one week that typeset the wrong day's tides into a published page. The
guard that now stops it also means NO layout change ever reaches a back
issue — the archive still wears the grid that was replaced on 08-26.

**Do:**
- When the sports edition is written (the routine's step, see
  `instructions/sportsman.md`), the routine copies `out/fishing.json` to
  `editions/data/<date>.fishing.json` and commits it with the edition.
  Add that line to `sportsman.md` and `routine.md`.
- `_tide_table_html(date)` reads `editions/data/<date>.fishing.json`
  first; falls back to `out/fishing.json` ONLY when the dated file is
  absent AND the live file's date matches (today's behaviour, for the
  transition). The date guard stays.
- Backfill: for every existing sports edition, there is no snapshot, so
  those archive pages keep their committed HTML. Do not re-render them.
  From tomorrow forward the snapshot exists.
- Add `render_edition.py --all` that re-renders every Times page (no live
  reads there) and every sports/weather page that HAS a snapshot, and
  refuses the rest by name. Run it once so the Times archive takes the
  flowed layout and the nav-foot.

**Verify:** re-render 2026-09-02 sport with the snapshot, diff the tide
times against the routine's commit (they must be identical). `--all` on a
clean tree changes only Times pages and reports the sports pages it
skipped.

### 3. Retire the full-embed Discord path

**Why:** thirteen functions in `post_discord.py` serve a posting model that
ended 2026-08-26, and live instructions still point at them. Dead code with
a signpost is a trap for a 5:30 reader.

**Delete:** `build_within_budget`, `split_payloads`, `render_text_edition`,
`split_message`, `_post_text_edition`, `backfill_page_url`,
`_run_backfill`, `build_sportsman_payload`, `_sm_masthead_line`,
`_inside_line`, `tail_link_text`, `_tail_link`, `trim_order`, the
`--split/--text/--backfill-link/--sportsman/--page-url` flags, and
`WV_EXTRA_TRIM_ORDER` / `WV_EXTRA_FLOOR` / `NEVER_TRIM`.
**Keep:** `build_payload` ONLY if `_exact_measure` in the validator still
needs it for the proportion advisory (it does — keep it, and say so in its
docstring), `build_digest_payload`, `send_message`, `write_payload_file`,
the ledger/idempotency code, `clamp_payload`, `validate_payload`.
**Config:** `PREFER_SPLIT_OVER_TRIM`, `EMBED_HARD` as a *ceiling* (it is now
only a proportion guide — rename to make that true, or fold into
`EDITION_*`), `CHUNK_LIMIT`. Remove `DISCORD_SPORTSMAN_WEBHOOK_URL` from
`.env.example`.
**Docs:** `instructions/edition.md` §9 "The old full-embed path" and §9.5,
`instructions/sportsman.md` §5's retired commands, README.

**Verify:** tests green; `post_discord.py --date <today> --digest --dry-run`
byte-identical output before and after; `validate_edition.py` on today's
edition unchanged.

### 4. DST holds — before 1 November

**Why:** five of six crons are raw UTC. On 2026-11-01 the weather page
moves to 7:10 ET, five minutes before Jim posts; it survives on its
twenty-minute wait by a margin of minutes, all winter.

**Do:** give every routine the ET hold the briefing has. `post_discord.py
--not-before HH:MM` already converts ET and sleeps. For the weather page,
add a "do not look for the briefing before 7:45 ET" wait to
`instructions/weatherpage.md` (a `python -c` sleep against `config`'s DST
arithmetic is enough). The papers already hold to 7:00. The watchdog and
report card need nothing but their times documented in ET in
`docs/HANDOFF.md` §2–3 — they are fine an hour early.

**Verify:** run the weather-page wait logic with a fake clock on both
sides of the change. Update the HANDOFF table and delete the DST open item.

### 5. Watchdog — the two blind spots

**Do:** two checks in `weatherman/instructions/watchdog.md`:
`ashgrove-times/editions/index.json` → yesterday's record has
`posted: true`; and `ashgrove-times/site/weather/<yesterday>.html` exists.
The watchdog prompt already defers entirely to that file. Do not touch the
prompt.

### 6. Webhooks out of prompt text

**Do:** move `DISCORD_WEBHOOK_URL` (Times) and the weatherman webhook into
each routine's `environment_variables` via `RemoteTrigger update` — send
the FULL `job_config` back with only the change, as the 09-02 model move
did; a partial `job_config` may wipe the rest. Confirm the sandbox actually
sees the variable by reading a run log before removing it from the prompt.
Then **Nate deletes the sports webhook in Discord** — it is retired and
has been copied into too many places to keep. Ask him; do not assume.

### 7. Standings byte-match

**Why:** both sports errors Pat caught were "half right" — real numbers,
wrong relationship. `result` fixed direction. Standings are still typed by
hand. `https://statsapi.mlb.com/api/v1/standings?leagueId=104&season=2026&date=<date>`
answered from the sandbox first try (see the 08-24 and 08-26 fixes).

**Do:** `fetch_standings.py` → `out/standings.json` for every followed MLB
team (`config.FOLLOWED_TEAMS`, league MLB): W, L, division rank, GB,
wild-card GB. Snapshot it into `editions/data/<date>.standings.json` like
the water. Validator: every W-L, games-back and ordinal printed in a
`teams.standings` line or any brief naming that team must be a value the
fetcher wrote — the stat-strip rule. Date-scope to tomorrow. MLS/EPL
standings are out of scope unless a keyless source is found; say so in the
instructions rather than half-doing it.

### 8. RSS feed + archive nav

**Do:** `site/feed.xml` written by `write_site` from `editions/index.json`
(title, dated permalink, dek as description, pubDate). Link it from
`home.html` with `<link rel="alternate" type="application/rss+xml">`.
Give `archive.html` the same nav rows every other page has (both rows;
the `ARCHIVE_PAGE` block needs `{{NAV}}` and `{{NAV_FOOT}}`).

### 9. Date-word gate on the 14-day window

**Do:** every `away` and `hotspots` item must contain a day reference — a
weekday name, `Mon`–`Sun`, `Aug. N`, "last week", "this morning",
"yesterday", "on the Nth". Validator error, date-scoped to tomorrow, with
the list of accepted forms in the message. Add the rule to
`edition.md` §"A block that never runs empty" step 1.

### 10. Small marks

- `site/home.html`: the Sports & Sportsman card says "Every morning at
  7:05 ET" — it is web-only and published before 7:00. Say so.
- `templates/broadsheet.html` `@media print`: hide `.paper-nav` and
  `.rule-anchor`.
- Ask Nate to ask Ian, once, which WV outlets he trusts. The list in
  `edition.md` has been "provisional" since August.

### 11. Alert watcher cost — ASK FIRST

Forty-eight fires a day on the top model, nearly all a deterministic diff
that stops. Option: keep the half-hourly cron but run `check_alerts.py`
alone, and when it finds new alerts, `RemoteTrigger run` a second Fable
routine that writes and posts. Words stay on the top tier; quiet runs cost
a script. Cost: a second routine to keep in step. **This changes the
routine roster and Nate has hit Fable quota before — put the trade-off to
him and do nothing without a yes.**

### 12. Weatherman grader — separate pass, optional

`weatherman/verify.py`, `instructions/report-card.md` and `briefing.md`
were not reviewed. "Grade inflation is the one unforgivable failure" has no
test behind it. Same treatment as item 1 if time allows; otherwise write
the gap into `docs/HANDOFF.md` §9 and stop.

## Traps this pass will meet

- **Writing Python through a Bash heredoc mangles backslashes.** `\b`
  became a literal backspace, `\n` became a real newline inside a string,
  `\d` lost its escape — repeatedly, in this exact codebase. Use the
  `Write`/`Edit` tools for anything with an escape sequence, and after any
  bulk edit run the control-character scan that is in the 08-26 commit
  history (`sum(1 for c in s if c in '\b\f\v\a')` over every `.py`).
- **The validator mutates its input.** The dead-link scrubber writes the
  edition back with `url: null`. Validating an archived edition without
  `--no-urls` changes it. Always `--no-urls` for anything not today's.
- **Local `out/` is stale.** `out/stats.json` and `out/fishing.json` on a
  dev machine are whatever was last fetched; byte-match errors against
  them are noise, not signal. Gauges drift within a day, so even a fresh
  fetch fails honest lines written at 5:30. Judge contract errors only.
- **`git pull --rebase` before every item.** The routine commits several
  times a day and you WILL conflict on `site/*.html`. Take the routine's
  page (`git checkout --ours` during a rebase), then re-render.
- **Never re-render a page whose data file you have not verified.** Until
  item 2 lands, diff the tide table against the routine's commit after
  any sports re-render. Item 2 makes this go away; that is why it is early.
- **Routine updates send the full `job_config`.** See item 6.
- **Commit messages are long and say why** — Wes reads them. Attribution:
  `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

## Done means

Items 1–10 landed and pushed, each with a PATCH_NOTES entry and the
HANDOFF updated in the same commit; item 11 put to Nate with the trade-off
and left at his answer; item 12 either done or written into HANDOFF §9 as
open. The last commit of the pass deletes this file's "The pass, in order"
section and leaves a one-paragraph summary pointing at PATCH_NOTES —
a work order that is finished should not look like one that is pending.
