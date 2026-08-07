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
| **2026-11-01** | **Switch the routine's cron to `0 11 * * *`.** EDT ends at 2 AM that Sunday. The cron is UTC-fixed, so `0 10 * * *` becomes a **5:00 AM ET** wake — a 120-minute head start instead of 60. **This is the harmless direction:** `--not-before 07:00` still delivers at 7:00, so readers see nothing; the routine just idles an extra hour. `config.head_start_minutes(date)` reports it, `config.POST_CRON_UTC_STANDARD` is the value, `config.cron_for(date)` says which belongs on a date. Worth fixing, not worth alarm | **OPEN** |
| **2027-03-14** | **Switch the routine's cron back to `0 10 * * *`.** EDT resumes at 2 AM that Sunday. **This is the dangerous direction:** leaving the winter cron installed wakes the routine at **7:00 ET**, a head start of ZERO. The delivery hold is already past on arrival, so the paper posts whenever the research finishes — roughly 40 minutes late, after the forecast it points at. `config.head_start_minutes()` returns 0 or less; the playbook logs a `FAILURES.md` line when it does | **OPEN** |
| **Before 2026-09-13** | **Confirm the September (Aki) basho's real dates by search** and record them below. `config.basho_window()` derives Sep 13–27 from the second-Sunday rule; that is an estimate the validator uses to decide how loudly to advise, never a fact the paper may print. The Japan Sumo Association publishes the schedule — confirm it there or at a wire outlet | **OPEN** |
| Open-ended | **Ian's answer on the WV outlet list.** `instructions/edition.md` marks the list provisional. When he answers, the playbook is edited and the answer is recorded here | **OPEN — unasked** |
| 2026-08-06 | **Premier League clubs, answered the same day it was asked.** A reader asked for football in Sports and specified the shape himself: *"emphasis on news from the teams we like, general from the rest of the league."* The allegiances: **Chelsea** (Trav, Ian), **Tottenham** (Nate), **Liverpool** (Pat) — in `config.PREMIER_LEAGUE_SUPPORTERS`, first names only, handles deliberately not recorded because the repo is public. All three meet twice a season, so several times a year one fixture is a house derby; `config.is_house_derby()` catches it and the playbook says to write those straight down the middle | **CLOSED** |
| Open-ended | **Pages build lag exceeds any sane pre-post poll.** 2026-08-06: `editions/2026-08-06.html` 404'd for the full 120s window so the link was omitted; it returned 200 about 9 minutes after the push (measured build **8m38s**, versus 23s the evening before). Pages is healthy — this is Actions queue lag, not an outage, so do **not** set `PAGES_ENABLED = False`. **RESOLVED 2026-08-06:** the paper no longer waits on it. `python post_discord.py --date YYYY-MM-DD --backfill-link` posts nothing, waits out the build (up to 15 min), and edits the permalink into the message already sent; `instructions/edition.md` §9.5 makes that step 9.5 whenever step 8 times out. It edits content only, never embeds, so it can never trim a published brief. No. 2 was backfilled by hand and now carries its link | **CLOSED** |

## 2. Forward-dated events

| Date | Event | Note |
|---|---|---|
| 2026-08-08 | **Aki basho tickets go on sale** | Confirmed on the JSA's own English page (`sumo.or.jp/En/`) and printed as No. 2's sumo brief. Do not re-run this fact; it is spent |
| 2026-08-08 | Chelsea play AC Milan in Jakarta | Preseason friendly. A followed club, so it is a legitimate football brief if anything happens in it |
| 2026-08-13 | **Peoples Cartage town hall, Parkersburg** | Independent testing results from the warehouse fire. WTAP. A `mid_ohio_valley` line that night or the morning after |
| 2026-08-21 | **Premier League 2026-27 opens** | Confirmed via ESPN's fixtures piece. Until then the football beat is transfers and friendlies only, and a quiet football day is the expected outcome, not a failure |
| **2026-08-31** | **Aki banzuke (rankings) released** | The next genuine sumo news after the ticket date, and the natural moment the Aki dates get confirmed by a citable outlet. Do not print it before it happens |
| 2026-09-10 | WV charter board bylaws vote | Postponed from Aug. 6. WV MetroNews. Small, but it is the follow-up to today's statewide brief |
| 2026-10-02 | DUA filing deadline, Lewis and Upshur | Claims close; benefits run to Feb. 6, 2027. West Virginia Watch |
| 2026-09-13 → 2026-09-27 | **Aki basho (Tokyo)** — *derived, still unconfirmed* | Second-Sunday estimate from `config.basho_window(2026, 9)`. 2026-08-06: the only sources carrying Sept. 13–27 at Ryogoku Kokugikan were ticket-reseller and travel sites, which this paper does not cite. **2026-08-07: searched again, same result** — travel sites only, and `sumo.or.jp/EnHonbashoTopics/banzuke_topics/` now returns a Japanese URL-error page rather than banzuke content. Try Kyodo, Japan Times or NHK at the **Aug. 31 banzuke release**, which is when a citable outlet will have to print the dates. Confirm before covering. During a basho, sumo usually wins the Sports lead |
| 2026-11-08 → 2026-11-22 | **Kyushu basho (Fukuoka)** — *derived, unconfirmed* | Same derivation. Note it opens the week after the cron switch above |

## 3. Open threads

- **hormuz-reopening** — 2026-08-06: still unsigned. Trump said a deal could
  land Aug. 5 or 6 and it did not; the draft is reported to be awaiting
  Khamenei's sign-off, and the service-fee dispute is unresolved. Al Jazeera /
  Washington Post. **Deliberately not run today — "no breakthrough" is a
  non-event, not news.** It is news again the moment the statement is signed
  or the strait actually reopens. Was No. 1's lead.
- **tariff-refunds** — 2026-08-06: today's lead. CBP has refunded ~$100B of the
  ~$165B collected under the IEEPA duties the Supreme Court voided 6-3 in
  February; ~$29B still under review, ~$1.6B unpayable for missing bank
  details, 330,000+ importers claiming ~$127B with interest. Euronews. News
  again when the review balance clears or a court rules on the interest rate.
- **greenbrier-500m** — 2026-08-07: **the lawyers' own closing date arrived and
  nothing was reported.** Searched this morning; the freshest items are still
  July (the "not merely a loan but a joint venture" filing of Jul. 27) plus an
  Aug. 6 MetroNews piece on property owners writing to Judge Volk objecting to
  current management. No confirmation the Kennedy Lewis financing actually
  closed. **Not run — a missed deadline is only news once someone reports it.**
  Check again 2026-08-08: either it closed and that is a statewide brief, or it
  slipped again and the slip is the story.
- **wv-flood-aid** — 2026-08-07: **moved, and ran as today's first statewide
  brief.** Disaster Unemployment Assistance opened for **Lewis and Upshur**
  (the two counties that already had the $4.5M) covering job losses from the
  Jul. 21–22 storms, tornadoes, flooding, landslides and mudslides; claims file
  by **Oct. 2**, benefits payable to **Feb. 6, 2027**. West Virginia Watch.
  The other **five counties are still pending federal review**, Pleasants among
  them (three EF2 tornadoes, 5 homes destroyed, 13 badly damaged); Morrisey
  asked for seven in all. News again when any of the five is decided — that is
  the bigger story and it has not happened yet.
- **wvu-qb-battle** — 2026-08-05: camp opened with no starter named between
  Scotty Fox Jr. and Michael Hawkins Jr. WVU Athletics. Resolves before the
  opener; local readers care.
- **peoples-cartage-fire** — 2026-08-05: independent testing results to be
  presented at a Parkersburg town hall **Aug. 13**. WTAP. Follow that night.
- **congo-ebola** — 2026-08-05: 1,707 dead of 3,802 cases, Ituri ~90% of
  infections, WHO accelerating trials. Al Jazeera. A fast-moving toll —
  re-check the count before citing it again, and note other outlets lag.
- **fauci-contempt** — 2026-08-07: **the vote happened and ran as a U.S. brief.**
  The Senate Homeland Security Committee voted along party lines to hold Fauci
  in contempt; the resolution directs Vance to certify it to the U.S. attorney
  for D.C., and DOJ decides whether to prosecute. NPR notes a full-Senate
  contempt finding would need 60 votes. **The tally is deliberately not in the
  paper:** outlets disagreed (8-7 in one account, 8-5 in another) and neither
  NPR nor PBS printed a number, so the disputed figure was dropped per the
  playbook rather than split. News again on a DOJ charging decision.
- **pleasants-power-ch11** — 2026-08-06: Omnis Pleasants filed Chapter 11 in
  Delaware in late July over $70M in debt; the ownership group is moving to
  dismiss it as a bad-faith filing after the independent manager refused a
  $75.64M payoff. WTAP. Cut from today's notebook for characters, not for
  sourcing — run it when the court rules.
- **wv-clothing-vouchers** — 2026-08-06: Morrisey said $5.45M, 49.5% of School
  Clothing Allowance funds, came out as ATM cash last year and promised
  legislative changes. WV MetroNews; WSAZ is investigating separately. News
  again when a bill or an audit appears.
- **spokane-fires** — 2026-08-07: still not run, third day running. The Spokane
  arrest is stale, but the **statewide** picture has grown a lot: Washington
  DSHS put it at 15+ uncontained large fires over 425,000 acres, and NPR ran an
  Aug. 7 feature on firefighter deaths this season. **The blocker is sourcing,
  not news** — the acreage lives on a state agency updates page and the readable
  outlet stories (CBS, NBC) are the Aug. 3–4 Spokane ones. A wire piece with
  current statewide numbers makes this a U.S. brief immediately.
- **birthright-citizenship-eos** — 2026-08-07: today's lead. Two orders signed
  Aug. 6 — one narrowing eligibility (alien enemies, foreign terrorist orgs,
  agents of foreign governments, parents who obtained status by fraud), one
  restricting birth-tourism visas; ~26,000 of ~3.5M annual US births are
  estimated as birth tourism. Follows the June **6-3** SCOTUS rejection of the
  first order. NBC News / NPR / PBS. ACLU said it expects them to fail. **News
  again the moment the first suit is filed or a judge enjoins them** — that is
  near-certain and it is the follow-up, not a re-run of the signing.
- **thailand-school-shooting** — 2026-08-07: ran as a World brief. A teenage
  student killed his grandparents, then opened fire at Debsirin Nonthaburi
  School outside Bangkok; **the toll was moving all morning** — NPR's police
  spokesperson had 6 dead, Al Jazeera reported authorities revising to 5 with 23
  hurt, and officials disagreed on whether the shooter died at the scene or in
  hospital. Printed as "at least 5," attributed, per the disputed-number rule.
  **Re-check the confirmed toll before citing it again.**
- **sudan-el-obeid** — 2026-08-07: ran as a World brief. City of ~500,000 in
  North Kordofan under RSF siege; 100,000+ displaced sheltering there, cholera
  spreading, at least 59,000 killed nationally since 2023. NPR. Slow-moving; a
  fresh brief needs a siege break, a named offensive, or a new UN figure.
- **uganda-gaza-force** — 2026-08-07: ran as a World brief. Uganda's parliament
  approved a UPDF contingent for the 20,000-strong International Stabilization
  Force; Morocco, Indonesia, Kazakhstan, Kosovo and Albania also committed, and
  deployment waits on the phased Israeli withdrawal. NBC News. **News again when
  the first troops actually deploy**, which is the real milestone.
- **csx-south-charleston** — 2026-08-07: ran as the `putnam_kanawha` line.
  Seventeen cars of a corn train derailed near Central Avenue about 9:49 a.m.
  Thursday; no injuries, no hazardous cargo. CSX said the cause would take
  several days and full track restoration several more. WVPB. **A cause finding
  is a follow-up line; a clean re-opening is not.**
- **magnetar-birefringence** — 2026-08-07: ran in Sci/Tech. IXPE, NICER and
  Parkes measured polarization of magnetar 1E 1547-5408 far above expectation —
  evidence for vacuum birefringence, predicted in 1936. Nature; NASA. **Written
  as evidence, not proof, on purpose:** NASA itself says further observations
  must confirm it, and an independent April 2026 analysis of the same IXPE data
  argued the geometry does not make it compelling. Do not upgrade the claim
  without a new observation.
- **wv-charter-rules** — 2026-08-07: ran as a statewide brief. The board is
  writing bylaws for two new statutory paths — converting closing rural schools
  to in-person charters, and "charter micro schools" tied to colleges — with no
  micro-school applications yet. Eight charter schools operate statewide.
  WV MetroNews. Bylaws vote **Sept. 10**.

<!-- Format, one bullet each:
- **slug** — one line of where the story stands, dated. Outlet. What would
  make it news again.
-->

## 4. Recently covered

### 2026-08-07 — No. 3
- lead: birthright-citizenship-eos
- us: fauci-contempt, head-start-deregulation
- world: thailand-school-shooting, uganda-gaza-force, sudan-el-obeid
- wv statewide: wv-flood-aid (DUA for Lewis/Upshur), wv-charter-rules
- wv regional: huntington_cabell — barboursville-nursing-center;
  putnam_kanawha — csx-south-charleston
- wv away: **none** — nothing searched clean, and Topsail was already carried
  by its fishing line
- sports: mudryk-returns, jonathan-taylor-extension
- scitech: magnetar-birefringence, infant-analgesic-trial
- mid_ohio_valley, nicholas_webster, summers_new_river: **no line**
- **sumo: sat out.** Off-basho, searched properly, nothing new — the Aug. 8
  ticket date was spent by No. 2 and the Aug. 31 banzuke has not happened.
  Correct edition per Ian's rule, not a degraded one
- **Do not re-run tomorrow without movement:** the birthright signing itself
  (the lawsuit is the news); the Fauci committee vote (DOJ's decision is the
  news); the Barboursville groundbreaking; the DUA opening

### 2026-08-06 — No. 2
- lead: tariff-refunds
- us: michigan-senate-primary, water-system-cyberattacks, fauci-contempt
- world: ukraine-refinery-strikes, north-korea-missile, cjng-reward
- wv statewide: wv-clothing-vouchers, black-lung-niosh
- wv regional: huntington_cabell — huntington-fatal-fire;
  putnam_kanawha — google-buffalo-community-fund
- wv away: **none** — vermont line written and cut for budget; prince_george
  had only a repeat of yesterday's mayor race; topsail covered by fishing
- sports: fifa-infantino-backed, aaron-donald-workout, sumo-aki-tickets
- scitech: falcon9-moon-impact, moderna-mrna-flu-approval, west-nile-europe
- mid_ohio_valley, nicholas_webster, summers_new_river: **no line**
- **Do not re-run tomorrow without movement:** the Aki ticket on-sale date is
  spent; the black lung NIOSH figures are spent; the Google Buffalo fund is
  spent

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
- **2026-08-06** — No. 2 posted, one message, 5,570 embed chars. First run to
  fit in a single Discord message; No. 1 ran 8,587 and split. What it cost:
  two sourced notebook lines. **The budget note for tomorrow is that a full
  14-brief paper plus a full notebook does not fit.** Source URLs are ~100
  characters each and are unshrinkable, so the arithmetic is roughly 14 briefs
  = 5,300 before the notebook gets anything. Write summaries at 90–110, not
  150, and decide the notebook's shape *before* drafting rather than cutting
  clean lines at the end. Pages did not serve the permalink; logged and opened
  as a standing commitment.
- **2026-08-07** — No. 3 posted at **07:00:11 ET**, one message, 5,694 embed
  chars, hero attached, permalink included in the original post, `degraded: []`.
  Three things the next shift should take from it:

  **1. Run `post_discord.py --not-before` in the BACKGROUND.** The first attempt
  was launched as an ordinary foreground command and the 2-minute tool timeout
  killed it mid-sleep at 6:17. Nothing posted and nothing was recorded, so it
  was recoverable — but only because `index.json` was checked before retrying
  rather than blindly re-running. `--not-before 07:00` legitimately sleeps up to
  the full head start; the flag needs a runner that tolerates ~40 minutes.

  **2. Do not trust a felt sense of the clock — read it.** The research finished
  around 6:17, but this desk had convinced itself it was running ~20 minutes
  late and started trimming corners against a deadline that was still 40 minutes
  away. `TZ=America/New_York date` is one call and it settles it. The head start
  is real; the whole point is that it does not need to be raced.

  **3. Because there was time, Pages was polled BEFORE posting rather than
  after.** It went 200 in ~10 seconds, so the permalink shipped in the original
  message and `--backfill-link` was never needed — the first edition to manage
  that. Worth making the default whenever the run finishes early: poll first,
  and keep the backfill for genuinely late mornings.

  Budget held: validator projected 6,077 on the first pass, prose was tightened
  to 5,694, and the post-time trimmer never engaged. Two-brief sections in U.S.,
  Sports and Sci/Tech were the honest cost of that ceiling, not thin research.
