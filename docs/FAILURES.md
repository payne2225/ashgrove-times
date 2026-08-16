# The Ashgrove Times — Degraded-path log

**Append-only.** One dated line every time the pipeline took a rung below
the top of the delivery ladder. Nothing here is ever edited or deleted —
this file exists so slow quality drift is *visible* instead of silent. Three
stripped URLs in a week is a sourcing problem; three fishing omissions in a
week is a fetcher problem. Neither is visible from one morning's run log.

`instructions/edition.md` §10 makes writing this step 3 of the record phase,
and the failure protocol at the bottom of that file appends here too.

## The contract

| | |
|---|---|
| **Who writes it** | The daily routine, by hand. No script touches this file |
| **When** | Any run that degraded — including a run that aborted and posted nothing |
| **Nothing degraded?** | Write nothing. An empty morning leaves no line |
| **Format** | `- **YYYY-MM-DD** — *rung* — what happened, what shipped instead.` One line. Flat |

**What counts as degraded** (the ladder in `README.md`, rungs 2–13):

- hero render failed → masthead fallback attached
- no image attached at all
- Pages push or poll failed, or the permalink was omitted
- the trim path dropped a brief, or the message had to split
- a URL failed its liveness check and was stripped
- a section ran thin (2 briefs, or 1)
- a fishing water was omitted because its source failed
- `stat_strip` shipped empty
- the webhook needed a retry, `--text` mode, or the stdlib multipart path
- the paper did not ship at all
- **a standing commitment in `docs/LEDGER.md` came due and was not done** —
  the daylight-saving cron switch is the one that will actually happen

**What does NOT count**, and must not be logged:

- **No sumo brief on an off-basho day.** Ian's rule is that sumo is covered
  when there is something to cover. An absent sumo brief on a dead August
  Tuesday is the correct edition, not a degraded one.
- A region with no news, or an empty `regional` / `away` array. Thin is the
  designed outcome, not a fault.
- `PAGES_ENABLED = False`. That is the shipped configuration, not an outage.

---

## Log

*No entries. Nothing has posted yet.*

<!-- Newest at the BOTTOM — this file is read as a chronology.
- **2026-08-06** — *rung 2* — hero render failed (Pillow raised on the stat
  strip); posted with assets/masthead-fallback.png. Six embeds intact.
-->
- 2026-08-05T21:59:44Z · 2026-08-05 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- 2026-08-06T11:39:47Z · 2026-08-06 · post_discord: no verified page url; posting without links
- **2026-08-06** — *Pages* — the dated permalink was still 404 after 120s of polling; posted embeds-only with no --page-url. Push landed at 80f5deb.
- **2026-08-06** — *trim* — the notebook was cut to fit the embed budget before posting: mid_ohio_valley (Pleasants Power Station Ch. 11 dismissal motion, WTAP) and the vermont away line (South Burlington youth center, VTDigger) both cleared the bar and were dropped for characters, not for sourcing. Shipped at 5,570 in one message.
- **2026-08-06** — *Pages, follow-up* — the permalink came up 200 about 10–12 min after the push, well outside the 120s poll. The link was correctly omitted from the post; the page is live and linked from the archive. Build lag, not an outage.

- 2026-08-06T17:08:32Z · 2026-08-06 · post_discord: backfill skipped: the edition now builds 2 message(s) but 1 were posted — refusing to guess which is which
- **2026-08-07** — *sourcing* — **wvmetronews.com began serving a bot-verification
  interstitial to WebFetch.** Three Aug. 6 articles (the Barboursville
  groundbreaking, the Valley Link transmission-line meeting, the Hope Gas rate
  case) returned only "Please wait while your request is being verified" instead
  of copy. The section index at `/news/` still renders headlines and one-line
  blurbs, which is exactly the trap — enough to write from, not enough to have
  *read*. Nothing was written from those blurbs. The two stories that ran were
  re-sourced to outlets that opened (WSAZ for Barboursville, WVPB for the CSX
  derailment) and the statewide DUA brief went to West Virginia Watch. The one
  MetroNews brief that shipped (charter board) was fetched successfully earlier
  in the run, before the interstitial appeared. **MetroNews is the playbook's
  first-listed WV outlet; if this persists, the provisional list needs WSAZ,
  WVPB and West Virginia Watch promoted ahead of it.**
- **2026-08-07** — *thin* — U.S., Sports and Science & Technology each ran **two
  briefs** instead of three. Not a research shortfall: the validator projected
  6,077 chars on the first pass against a 5,800 ceiling, and holding the lead,
  a 3-brief World and a 2-line notebook meant the wire sections absorbed the
  cut. Sumo sitting out is *not* part of this entry — that was correct and is
  excluded by policy.
- **2026-08-07** — *no url* — the infant analgesic brief (PIPPA Tamariki trial,
  The Lancet Child & Adolescent Health) shipped with `url: null`. The trial name,
  design, cohort and endpoints were corroborated across several secondary
  reports but no canonical publisher URL was opened, so the link was omitted
  rather than pointed at an aggregator. Source name only, per contract.
- **2026-08-07** — *near-miss, no reader impact* — the first `post_discord.py`
  run was launched in the foreground and **killed by a 2-minute command timeout
  while `--not-before 07:00` was still sleeping** (launched 6:17, hold ran to
  7:00). Nothing posted; `editions/index.json` had no row, which is how it was
  caught before a blind retry. Relaunched detached and it delivered at 07:00:11.
  Logged because the failure mode is silent: a killed hold looks identical to a
  crashed post, and only the index distinguishes them.
- **2026-08-08** — *trim* — the validator projected **6,603** chars on the first
  pass against the 5,800 ceiling. Prose was tightened across the lead and all
  four wire sections, and the trim ladder was walked one rung: the
  `mid_ohio_valley` line (Parkersburg SWAT drug warrant, 7th Street, three
  arrested, WTAP, Aug. 7) **cleared the bar and was dropped for characters, not
  for sourcing.** Shipped at 5,795. The away desk was already empty, so the
  regional line was the first thing on the ladder that existed.
- **2026-08-08** — *sourcing* — `wowktv.com` returned **403** to WebFetch on the
  Cabell County $4.5M emergency-communications upgrade, the only clean
  `huntington_cabell` candidate that was not already running as a statewide
  brief. A search snippet carried enough detail to write from and was
  deliberately not used. The region ran no line. Note MetroNews opened fine all
  morning today — yesterday's bot-verification interstitial did not reappear.
- **2026-08-08** — *near-miss, no reader impact, RECURRENCE of the 2026-08-07
  entry below* — `post_discord.py` was again launched in the **foreground** and
  killed by the command timeout while `--not-before 07:00` slept (launched
  ~6:15, 10-minute timeout, hold ran to 7:00). Nothing posted; `index.json` had
  no row, which is again how it was caught before a blind retry. Relaunched
  detached. **Root cause was not the runner but the clock:** this desk had
  accumulated a felt sense that the run was past 7:00 and never re-read
  `TZ=America/New_York date` between 6:02 and 6:25, so a sleeping hold was
  misread as a hung post. The ledger's own 2026-08-07 lessons 1 and 2 say
  exactly this. **Launch the post detached, first time, every time.**
- **2026-08-08** — *caught before publication, not a shipped defect* — the
  Sports football brief was drafted with the clause "before Xabi Alonso's first
  league season," a manager attribution that came **only from a search-result
  snippet of a site that was never opened.** Caught while the delivery hold was
  sleeping. `chelseafc.com` opened and confirmed the date, the venue and
  "the fourth match date during the pre-season preparations" — but does **not**
  name a head coach, so the clause was cut rather than kept. The brief was
  re-sourced from `tempo.co`/ESPN listings to Chelsea's own page. Logged because
  the near-miss is instructive: the snippet was fluent, specific and plausible,
  which is exactly the failure mode the "never write from a snippet" rule exists
  for, and it survived one full validate-and-render cycle before being caught.
- 2026-08-08T11:00:03Z · 2026-08-08 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- **2026-08-08** — *split* — the edition posted as **two messages** (FRONT PAGE +
  INSIDE) to keep the notebook whole. First split since No. 1. **The cause is a
  measurement gap worth fixing:** `validate_edition.py` projected **5,795** chars
  against its 5,800 ceiling and the paper was tightened four separate times to
  get under that number — but `post_discord.py` reported **6,009** actually sent.
  A **214-char** delta the validator does not model. The run passed
  `--page-url`, so the permalink content line is the obvious suspect, but that
  URL is only ~66 chars and the rest is unaccounted for; **do not treat 214 as a
  confirmed constant until someone diffs a `--page-url` payload against a bare
  one.** Practical rule for tomorrow: when passing `--page-url`, treat the real
  budget as **~5,550 projected**, not 5,795, or expect the split. Nothing was
  lost — splitting preserves every brief, which is why the script prefers it to
  trimming — but a one-message paper is the standing goal.
- **2026-08-09** — *fishing omission* — USGS 03186500 (Williams River at Cowen)
  returned **503** on the only fetch, so `williams` was `null` and the notebook
  ran **one** fishing line, Topsail only. No line was written for the Williams
  and no reading was carried forward. Routine per the failure protocol, logged
  because a run of these is a fetcher problem rather than a morning's bad luck:
  this is the **first** Williams omission in five editions (Nos. 2, 3 and 4 all
  carried a flow). Side effect worth noting for the sketch desk: the rung-3 art
  fallback lost its usual subject, so the drawing came off **rung 1** instead.
- **2026-08-09** — *budget trim* — one sourced, opened `huntington_cabell` line
  (Milton's water-line replacement and Kilgore Creek tank, phase one starting
  2027, WCHS) was **written and cut** to hold the embed budget, along with a
  round of tightening across the lead and eight summaries. Validator projected
  **6,217** on the first pass; the cut and the tightening brought it to 5,529.
  The line was the weakest thing in the notebook anyway — it is an announcement
  about next year, not an event inside 48 hours — so the cut ladder took the
  right rung first. The notebook ran one regional line and no away line.
- **2026-08-09** — *thin section* — Sports ran **two** briefs (Chelsea's 3-0
  friendly, the WPBL debut). Off-basho sumo sat out for the third straight day
  after a full dedicated search, and WVU/Marshall had only practice reports. Per
  Ian's rule the absent sumo brief is not itself a degraded path; the two-brief
  section is, and it is logged as one.
- **2026-08-09** — *three near-misses, caught before publication, RECURRENCE of
  the 2026-08-08 snippet entry* — three clauses drafted from **search-result
  snippets of pages that were never opened** survived a full validate-and-render
  cycle and were caught during the delivery hold, on a deliberate re-read of
  every brief against the source actually fetched. (1) Sports said Caicedo
  "volleyed" his goal — AC Milan's own match report, the page read, gives the
  minute and no volley; the word came from a Yahoo/heavy.com snippet. (2) U.S.
  said "The House returns in September" and "sanctions Putin, oligarchs and
  state firms" — NPR's article says only that it must clear the House and that
  it sanctions top Russian officials. (3) Sci/Tech rounded BMJ's ">30%" to
  "30%". All three were re-written to the fetched text, the edition was
  re-validated, re-rendered and re-pushed, and the held post was killed and
  relaunched twice (nothing had posted; `index.json` was empty both times).
  **The pattern is now two days running and it is the same pattern:** the
  snippet is fluent and specific, it reads like something you fetched, and
  nothing downstream can catch it. The only defence that has worked twice is
  re-reading the draft against the fetched sources while the hold sleeps —
  make it a standing step, not a lucky habit.
- **2026-08-10** — *budget trim, three briefs and one lead paragraph cut* — the
  first full draft projected **7,206** chars against the 5,800 ceiling, the
  worst overshoot of the run so far, because it carried 15 briefs plus a
  three-paragraph lead. The cut ladder was worked in order and stopped as soon
  as it was under: the lead went from three paragraphs to two (the contract
  allows either), the **third WV statewide brief** was dropped (Hope Gas's 7%
  purchased-gas filing with the PSC, WV MetroNews — written, sourced, opened),
  the **third Sci/Tech brief** was dropped (Lancaster University on Saturn's
  magnetospheric cusp, *Nature Communications* — written, sourced, opened), and
  finally the **third U.S. brief** was dropped (the National Indian Gaming
  Commission's seven-month vacancy, PBS NewsHour — written, sourced, opened).
  Landed at **5,471**. Note the ladder in `edition.md` §5 says notebook lines go
  before wire briefs, and here there was only **one** regional line and **no**
  away line to give — the notebook was already lean, so the pressure fell
  entirely on the wire sections. **The real lesson is upstream of the ladder:**
  15 briefs plus a 3-paragraph lead plus a notebook has never fit and the
  arithmetic was knowable before drafting. Decide the brief count *first* —
  roughly 12 briefs with a lean notebook — rather than writing 15 and cutting 3.
- **2026-08-10** — *thin sections* — U.S. and Sci/Tech each ran **two** briefs,
  and WV statewide ran **two**. All three were budget cuts, not thin research;
  the dropped items are named in the entry above. Sports ran without sumo for a
  fourth straight day after a full dedicated search, which per Ian's rule is not
  itself a degraded path.
- **2026-08-10** — *two fidelity drifts, caught before publication, THIRD DAY
  RUNNING for this class of error* — the re-read-against-source pass during the
  delivery hold caught two WV statewide briefs that had drifted from their
  fetched text. (1) The DoHS brief said the deputy secretary told "finance
  committees" — WV MetroNews names one body, the **Joint Standing Committee on
  Finance**, and the plural was invented. (2) The Flock brief said the
  presentation "raised more questions than answers" — Del. Ryan Browning's
  reported words are "more concerns than actually giving us answers," so the
  paraphrase was moved back onto "concerns." Both were fixed, the edition was
  re-validated and re-rendered, the corrections were pushed, and the held post
  was killed and relaunched once (nothing had posted; `index.json` had no
  2026-08-10 row when it was checked). Milder than the Aug. 8 and Aug. 9
  entries — no invented number, no unopened page — but the same failure surface,
  and the same pass caught it. **Three for three: the hold re-read is now the
  single most productive step in the run.**
- **2026-08-12** — *budget overspend, tightened by hand rather than by the trimmer* —
  the first draft projected **6,131** chars against the 5,600 target and the 5,800
  hard ceiling, which would have had `post_discord.py` silently drop the back of
  Sci/Tech. Three tightening passes brought it to **5,749** with every brief and
  both notebook lines intact. **The overspend was in the lead (1,193 against a 900
  allocation), not the notebook** — the playbook's cut ladder starts at the away
  line, but cutting the away desk would have paid for a bloated front page, so the
  lead body was cut back instead and the notebook kept its regional and away lines.
  Worth saying plainly: the ladder assumes the notebook is the overspender, and
  today it was not.
- **2026-08-12** — *thin sections* — Sports and Sci/Tech each ran **two** briefs.
  Sports: sumo sat out for a sixth day (off-basho, full dedicated search, only
  sumostats-carried items) and football had nothing dated before the Aug. 21 opener
  — both correct per Ian's rule, not failures — which left two general briefs.
  Sci/Tech: nothing published Aug. 11-12 opened cleanly. `nature.com` redirects to
  an auth wall, `arstechnica.com` is blocked outright to this crawler, ScienceDaily
  had nothing newer than Aug. 10, and CIDRAP nothing newer than Aug. 3, so the
  section ran one Aug. 11 item and one **two-day-old** Aug. 10 item.
- **2026-08-12** — *four source-fidelity corrections, caught in the delivery-hold
  re-read, FIFTH TIME this pass has paid for itself* — (1) the dek said Trump's
  endorsements "carried South Carolina," but NPR reports his pick finished first
  with about a third of the vote and only advanced to a runoff, with two thirds
  voting for other candidates; the dek was replaced with the November matchup.
  (2) "three suspected tornadoes" became "at least three," which is what CBS wrote.
  (3) The ferry brief attributed the passenger count to Zimbabwe's Civil Protection
  Unit when PBS attributes it across several bodies, and stated 119 aboard when PBS
  notes children below ticketing age may not be counted — changed to "officials
  said at least 119," and the headline to "killing at least 15." (4) The mosquito
  brief said "researchers" where the institution, Florida International University,
  was available and is the paper's convention. **All four were overstatement, not
  invention — the same failure surface as Aug. 8-10.** Corrections were validated,
  re-rendered and pushed, and the held post was killed and relaunched once;
  `editions/index.json` had no 2026-08-12 row when it was checked, so nothing had
  shipped.
- **2026-08-12** — *away-desk sourcing gap* — `vtdigger.org` now returns **403** to
  this crawler, and the Bennington-district Senate primary that three editions have
  been waiting on is not published by Vermont Public, which prints only contested
  statewide races. The away line ran on Vermont's statewide results instead. The
  route to county-level Vermont results is `electionresults.vermont.gov`.
- 2026-08-12T11:00:03Z · 2026-08-12 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- **2026-08-12** — *split into two messages, and the validator's projection is why* —
  the edition posted at **07:00:02** as **two** messages (FRONT PAGE / INSIDE) at
  **5,963** actual embed chars, against the **5,749** the validator projected. The
  gap is about **215 chars** and it is systematic: `validate_edition.py` projects the
  embed text but the shipped payload also carries the `--page-url` content line and
  the second embed's header once it splits. **So a projection of 5,749 — comfortably
  under the 5,800 hard ceiling — still split.** No brief was lost; the split is the
  designed behaviour and keeps the notebook whole. **The lesson for tomorrow: treat
  5,600 as the real ceiling, not 5,800, whenever `--page-url` is being passed.**
  Nos. 1 and 4 split at 8,587 and 6,009 actual; No. 4's is the near neighbour of
  today's and points at the same threshold.
- **2026-08-13** — *budget trim, one notebook line* — the `huntington_cabell` line was
  written, opened and sourced (U.S. marshals arrested a 20-year-old Detroit man in
  Huntington Tuesday, charged in a November homicide there; WSAZ) and **cut for
  characters**, because the first complete draft projected **6,306** against the
  **5,600** working ceiling No. 8 established. The Mid-Ohio Valley line was kept over
  it: the Peoples Cartage testing result is the follow-up this ledger had been
  waiting for since Aug. 5, and the arrest was the weaker of the two. Regional ran
  at one line; away ran empty. After the cut and a second tightening pass the
  edition projected **5,412**.
- **2026-08-13** — *fishing source degraded, no water temperature* — `fetch_fishing.py`
  exited 0 with both waters, but NOAA returned no water temperature
  (`noaa-temp: RuntimeError: NOAA: no water temperature returned`), so the Topsail
  line ran **tides only** and the Wrightsville Beach attribution clause did not
  appear. Sound highs and heights are the fetcher's own numbers. Nothing was
  estimated and no temperature was carried forward from yesterday's 78.8F.
- **2026-08-13** — *run mechanics, not a reader-visible degradation, but read this
  before tomorrow* — the first `post_discord.py` launch was killed at 5 minutes by
  the shell's own foreground timeout while it was still sleeping out
  `--not-before 07:00`. **Nothing had posted** (`editions/index.json` had no
  2026-08-13 row, checked), so there was no double-paper risk, but the lesson is
  mechanical: the hold can sleep for up to an hour, which is longer than a
  foreground command may live. **Launch the post as a background process.** The
  same run then also mis-estimated its own elapsed wall time — it read 6:23 ET when
  the model believed it was 7:38 — so a clock check is the only trustworthy answer
  to "am I late." It was not late.
- **2026-08-14** — *budget trim, one notebook line and one wire brief* — the first
  complete draft of No. 10 projected **7,776** against the **5,600** working ceiling,
  and the overspend was mostly URL cost: the Ames Goldsmith story's MetroNews URL is
  **140** characters, the two Herald-Dispatch URLs **148** and **133**, the NPR Taiwan
  URL **130**, and the two brightsurf science URLs about **100** each. Cut in the
  playbook's order: away was already empty, so the weakest **regional** line went
  first — the `huntington_cabell` entry on the Nick Joe Rahall II Bridge closing
  nightly 10 p.m. to 5 a.m. Aug. 18-21 for its annual inspection (Herald-Dispatch),
  written, opened and sourced, and genuinely the most marginal item in the notebook
  because a scheduled routine inspection is not an event. Statewide was already at
  two, so the next cut had to come from the wire: the **third U.S. brief** went, the
  NTSB's finding that bird remains and metal fatigue at the fan-blade root caused the
  July 10 Ryanair engine failure over Greece (CBS News) — the oldest incident in the
  edition. After both cuts and two tightening passes the edition projected **5,616**.
  **That is 16 over target and the second morning running that the notebook's source
  links, not its prose, are what blow the budget.** Two Cabell lines cut in two days.
- **2026-08-14** — *fishing source degraded, no water temperature, second day running* —
  `fetch_fishing.py` exited 0 with both waters and the same NOAA error as yesterday
  (`noaa-temp: RuntimeError: NOAA: no water temperature returned`), so the Topsail
  line again ran **tides only** with no Wrightsville Beach attribution clause. Nothing
  estimated, nothing carried forward. **Two consecutive days is no longer a blip —
  if it repeats a third time the station itself is worth checking.**
- **2026-08-14** — *source reachability* — `wvmetronews.com` served this crawler a
  "please wait while your request is being verified" interstitial on **three** article
  fetches (Clean-Seas air permit, WVU soccer opener, and a retry of the same) while the
  site's **homepage and two earlier article fetches went through normally**. It is
  intermittent, not a block. **One brief was lost to it**: the WVU men's soccer opener
  (2-0 over Dayton) could not be opened, so Sports ran the Marshall women's opener from
  WSAZ instead rather than write from a headline. Also new: **`france24.com` returned
  HTTP 403**, which is the first time this run has seen France 24 refuse.
- **2026-08-14** — *run mechanics, repeat of yesterday's line, and it should stop
  repeating* — `post_discord.py` was launched in the **foreground** and was killed at
  the 2-minute shell timeout while sleeping out `--not-before 07:00`. Nothing had
  posted (`editions/index.json` had no 2026-08-14 row, checked before relaunching), so
  again no double-paper risk. **This is the identical mistake logged on 2026-08-13**,
  and the identical companion mistake came with it: the run believed it was 7:30 ET
  when a clock check said **6:29**. The paper was never late either morning. The fix
  is mechanical and now written in the ledger's standing commitments: **launch the post
  in the background on the first attempt, and never estimate elapsed time — read the
  clock.**
- **2026-08-15** — *the second paper cannot ship: the pipeline flag does not exist* — This
  was the morning **Sports & Sportsman** was scheduled to run its first edition, and it
  could not. `instructions/routine.md` and `instructions/sportsman.md` both document
  `python validate_edition.py <path> --sportsman`, `python render_edition.py --sportsman`
  and `python post_discord.py --sportsman`. **No such flag exists in any of the three
  scripts** — `grep -ci sportsman` returns **0** for `validate_edition.py`,
  `render_edition.py` and `post_discord.py`. What *does* exist is the whole surrounding
  layer: `config.py` carries 16 sportsman references (masthead, tagline,
  `SPORTSMAN_SECTIONS`, `SPORTSMAN_WATERS`, `SPORTSMAN_AGENCIES`, `SPORTSMAN_MAX_PER_LEAGUE`,
  `SPORTSMAN_TARGET_ET` 07:05, `SPORTSMAN_WEBHOOK_ENV`), `fetch_fishing.py` already reports
  all four sportsman waters, both reference files are transcribed, and
  `editions/sportsman/index.json` exists as an empty ledger. Commit `ca5293d` ("Sports &
  Sportsman goes live tomorrow") shipped the identity, data and playbook and **never
  shipped the pipeline**. There is no branch and no PR carrying it — `origin/main` is the
  only ref and the PR list is empty. **Nothing was posted to the sportsman channel.** The
  webhook was supplied and is fine; the destination was never the problem. Hand-building a
  Discord payload was refused deliberately: `instructions/edition.md` forbids hand-edited
  payloads and hand-written HTML in as many words, and a channel's first-ever message is
  the worst possible place to improvise a format that no validator has ever checked.
  **`editions/sportsman/2026-08-15.json` is written, researched and committed** as Vol. I
  No. 1 to the contract in `instructions/sportsman.md`, so it can ship unchanged the
  morning the flag lands. Its fishing numbers were hand-checked against `out/fishing.json`
  in the absence of a validator and all four waters match.
- **2026-08-15** — *source reachability* — `deq.nc.gov`'s size-and-bag-limits page serves the
  table as **HTML at the canonical URL but as an unreadable PDF at the `/open` variant**, and
  the flounder proclamation `FF-27-2026` is PDF-only and could not be read — so the fall
  flounder opening date was **not printed**, only the closure that DMF's own HTML table
  states. `med.stanford.edu` opened but `news.stanford.edu` **403'd**; `sdss.org` opened;
  `espn.com` returned **empty markdown** for three separate pages (MLB scoreboard, two team
  schedule pages, the confirmed-transfers story), which is the second morning running that
  ESPN has been unusable. `herdzone.com` returned title-only markdown. `cbssports.com`
  exceeded the 10 MB fetch limit on its scoreboard. `mlb.com/scores` opened cleanly twice and
  is what the baseball lines rest on.
- **2026-08-15** — *aggregator caught contradicting the primary source* — a radio-station
  "sports daily digest" had **"Reds 9-8 over the White Sox"** for Aug. 14 while
  `mlb.com/scores/2026-08-14` had **Reds 1-0 over Miami** and, separately, White Sox 9,
  Tigers 5 — the digest had merged two games. MLB.com was re-opened and confirmed the same
  line twice, and the digest's NFL preseason scores were **dropped entirely** rather than
  carried on the same source's word. Worth remembering: that class of site is exactly where a
  fabricated-looking number enters a paper that is otherwise careful.
- 2026-08-15T16:20:10Z · 2026-08-15 · post_discord: no verified page url; posting without links
- **2026-08-16** — *budget trim, taken deliberately at the desk* — the edition came in at
  **~7,169 projected embed chars against the 5,800 the trimmer watches**, the largest
  overshoot yet, because four wire sections of four briefs each cost far more in **URL
  characters** than `instructions/style.md`'s ~40-char worked example assumes (the PBS,
  MetroNews and Al Jazeera links used today run **78-116 chars apiece**). The §5 cut ladder
  was walked in order: the **away line** (Prince George, BC Conservative leader's visit —
  researched, opened and sourced to CKPG Today) was dropped first, then summaries were
  tightened throughout, and finally **one World brief** (Australia's November gun buyback,
  Al Jazeera) was cut to land at **5,774**. Cutting a brief at the desk is worse than not
  needing to, and better than letting `post_discord.py` silently drop the last Sci/Tech
  brief at 7:00. **The structural note for whoever tunes this: at four briefs a section,
  the per-brief cost is nearer 285 chars than the 245 the style book budgets, so a full
  four-by-four edition does not fit and something gets cut every morning until either the
  budget or the target brief count moves.**
- **2026-08-16** — *fishing source degraded* — NOAA returned **no water temperature** for the
  Wrightsville Beach gauge (`noaa-temp: NOAA: no water temperature returned`), so both papers
  carried Topsail **tides only** and said so rather than reaching for yesterday's reading.
  Williams, both Ohio gauges and the Hampstead sound station all reported normally.
- **2026-08-16** — *sources that would not open* — `qcnews.com` and `washingtonpost.com`
  **403'd** and `africa.espn.com` and `columbuscrew.com` returned title-only markdown, so the
  **Columbus Crew's 3-1 loss at Charlotte could not be sourced from any article this desk
  could read** and the Crew was moved to `sat_out` with that as the stated reason, rather
  than written from two agreeing search snippets. **FC Cincinnati v Orlando City** likewise
  had no confirmable final score. `espn.com` was unusable for a **third** consecutive
  morning. `mlb.com/scores` and `premierleague.com` opened cleanly and carry the results.
