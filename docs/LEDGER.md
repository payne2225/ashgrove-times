# The Ashgrove Times — Editorial Ledger

**This is the paper's memory between mornings.** The routine has no other.
Each run starts a fresh context, so anything a previous edition knew and did
not write down here is gone: which stories are still moving, what the paper
already promised to follow, and what it printed yesterday so it does not
print it again today.

`instructions/edition.md` makes reading this file **step 2 of every run**,
before any research. It is read at the top of the run and written at the
bottom (§10), only after a successful post.

## The contract

| | |
|---|---|
| **Who writes it** | The daily routine, by hand, in step 10. Nothing else — no script touches this file |
| **When** | After a successful post, never before |
| **What it is not** | Not the delivery ledger. Edition numbers, `posted` flags and message ids live in `editions/index.json`, which `post_discord.py` owns. Not the failure log either — degraded paths go in `docs/FAILURES.md` |
| **Tone** | Notes to the next shift. Flat, dated, specific. No prose |

Four sections, all four maintained every run:

1. **Standing commitments** — dated things that must happen, including
   things outside this repo. Rows are opened once and closed only when the
   work is actually done. **A routine may not close a row it cannot
   verify** — if the date has passed and the thing did not happen, leave it
   open, report it, and log a line in `docs/FAILURES.md`.
2. **Forward-dated events** — dates the paper has committed to cover:
   verdicts, launch windows, elections, the next basho.
3. **Open threads** — running stories, each with the state it was left in.
   A thread only earns a brief tomorrow if it *moved*.
4. **Recently covered** — the dedupe list. Slugs from roughly the last
   seven editions; older rows get deleted, not archived.

---

## 1. Standing commitments

| Due | What | State |
|---|---|---|
| **2026-11-01** | **Switch the routine's cron to `0 12 * * *`.** EDT ends at 2 AM that Sunday. The cron is UTC-fixed, so `0 11 * * *` becomes **6:00 AM ET** — the paper lands 75 minutes ahead of the Weatherman's 7:15 instead of 15, on the first day of a basho month. `config.POST_CRON_UTC_STANDARD` is the value; `config.cron_for(date)` says which one belongs on any date | **OPEN** |
| **2027-03-14** | **Switch the routine's cron back to `0 11 * * *`.** EDT resumes at 2 AM that Sunday; leaving the winter cron installed lands the paper at 8:00 AM ET, *after* the forecast it points at | **OPEN** |
| **Before 2026-09-13** | **Confirm the September (Aki) basho's real dates by search** and record them below. `config.basho_window()` derives Sep 13–27 from the second-Sunday rule; that is an estimate the validator uses to decide how loudly to advise, never a fact the paper may print. The Japan Sumo Association publishes the schedule — confirm it there or at a wire outlet | **OPEN** |
| Open-ended | **Ian's answer on the WV outlet list.** `instructions/edition.md` marks the list provisional. When he answers, the playbook is edited and the answer is recorded here | **OPEN — unasked** |

## 2. Forward-dated events

| Date | Event | Note |
|---|---|---|
| 2026-09-13 → 2026-09-27 | **Aki basho (Tokyo)** — *derived, unconfirmed* | Second-Sunday estimate from `config.basho_window(2026, 9)`. Confirm before covering. During a basho, sumo usually wins the Sports lead |
| 2026-11-08 → 2026-11-22 | **Kyushu basho (Fukuoka)** — *derived, unconfirmed* | Same derivation. Note it opens the week after the cron switch above |

## 3. Open threads

- **hormuz-reopening** — 2026-08-05: Iran and Oman agreed route coordinates;
  a joint statement was "under final review" and Bessent said a deal could
  land within a day or two. PBS NewsHour / Euronews. News again the moment
  the statement is signed, the strait actually reopens, or the fee dispute
  (Tehran wants service fees, Washington refuses) breaks either way. This was
  No. 1's lead — follow it.
- **greenbrier-500m** — 2026-08-05: Kennedy Lewis financing expected to close
  **by Aug. 7**, with a debtholder payoff and Lottery Commission approval of
  the casino license still unsettled. WV MetroNews. Check on the 7th.
- **wv-flood-aid** — 2026-08-05: $4.5M Individual Assistance approved for
  Upshur and Lewis after the July 21 flooding; FEMA still weighing **five
  other counties**. WV MetroNews. News again when those five are decided.
- **wvu-qb-battle** — 2026-08-05: camp opened with no starter named between
  Scotty Fox Jr. and Michael Hawkins Jr. WVU Athletics. Resolves before the
  opener; local readers care.
- **peoples-cartage-fire** — 2026-08-05: independent testing results to be
  presented at a Parkersburg town hall **Aug. 13**. WTAP. Follow that night.
- **congo-ebola** — 2026-08-05: 1,707 dead of 3,802 cases, Ituri ~90% of
  infections, WHO accelerating trials. Al Jazeera. A fast-moving toll —
  re-check the count before citing it again, and note other outlets lag.

<!-- Format, one bullet each:
- **slug** — one line of where the story stands, dated. Outlet. What would
  make it news again.
-->

## 4. Recently covered

### 2026-08-05 — No. 1
- lead: hormuz-reopening
- us: cdc-director-confirmed, epstein-banks-wyden-report, zyn-fda-label
- world: kyiv-barrage, congo-ebola, brazil-ambassador-visa
- wv statewide: wv-flood-aid, greenbrier-500m
- wv regional: huntington_cabell — cabell-middle-school-sports;
  putnam_kanawha — poca-stadium; mid_ohio_valley — peoples-cartage-fire;
  summers_new_river — pritt-withdraws
- wv away: vermont — bennington-pow-remains; prince_george — pg-mayor-race;
  topsail — pender-nonprofit-review
- sports: wvu-camp-opens, sumo-purse-doubled, bears-wright-extension
- scitech: covid-latent-viruses, tesla-nhtsa-probe, spain-fire-attribution
- nicholas_webster: **no line** — nothing genuine surfaced. Correct outcome.

<!-- Format, newest first. Prune anything older than ~7 editions.
### YYYY-MM-DD — No. N
- lead: slug
- us: slug, slug, slug
- world: slug, slug, slug
- wv statewide: slug, slug
- wv regional: region_id — slug
- sports: slug, slug, slug
- scitech: slug, slug, slug
-->

---

## History

- **2026-08-05** — File created. Nothing has posted; the sections above are
  empty on purpose rather than seeded with invented history. Seeded the two
  daylight-saving cron switches and the basho-date confirmation as standing
  commitments.
