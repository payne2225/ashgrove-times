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
- 2026-08-16T11:00:03Z · 2026-08-16 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- **2026-08-16** — *edition split into two messages* — the Times posted as **2 messages**
  (`split into FRONT PAGE and INSIDE messages to keep the notebook whole`), the second time
  this has happened after No. 8 on 2026-08-12. Worth noting precisely: the desk trimmed to
  **5,774** projected chars against the 5,800 ceiling, but the delivered payload measured
  **5,988** because `--page-url` adds its link line *after* the validator's projection. **The
  validator's number is not the number the splitter sees — budget roughly 200 chars of
  headroom for the permalink, or a paper trimmed to just under the line still splits.** No
  brief was dropped and the notebook stayed whole, so this is cosmetic, not a content loss.
- **2026-08-17** — *edition split into two messages, third occurrence* — the Times projected
  **5,906** chars against the 5,800 ceiling and the dry run confirmed the split before it was
  sent (`split into FRONT PAGE and INSIDE messages to keep the notebook whole`), after No. 8
  and No. 12. The desk tightened every summary toward the low end of the target and **cut one
  wire brief** (a Colombia tariff-request brief, the weakest World item and the fourth day the
  Colombia quake would have appeared) and still could not reach the line. **Yesterday's
  headroom note held and is now confirmed twice over.** The structural cause is the four-brief
  wire sections plus long `sciencedaily.com` and `pbs.org` URLs: at four briefs a section runs
  ~1,200 against a 1,000 allocation no matter how short the prose is. **This is a budget
  arithmetic problem, not a discipline problem — `config.EMBED_BUDGET` and the four-brief
  target cannot both be met, and one of them needs changing.** No brief was dropped by the
  trimmer and the notebook stayed whole.
- **2026-08-17** — *fishing source degraded, second consecutive morning* — NOAA again returned
  **no water temperature** for the Wrightsville Beach gauge (`noaa-temp: NOAA: no water
  temperature returned`), so both papers carried Topsail **tides only**. Williams, both Ohio
  gauges and the Hampstead sound station reported normally.
- **2026-08-17** — *sources that would not open* — the **Marshall v Ohio women's soccer result
  could not be sourced** (both are followed teams and the ledger had committed to it):
  `herdzone.com` returned **title-only markdown** on both the schedule page and the preview,
  and `herdzone.com/news/` **404'd**; `espn.com` soccer scoreboards and `mlssoccer.com/scores`
  were unusable for a **fourth** consecutive morning; `premierleague.com/en/news` returned
  navigation only, so the Arsenal-City Community Shield score ran as one attributed clause
  inside the Rodri brief rather than as its own item. Both teams moved to `sat_out` with the
  reason stated. `mlb.com/scores`, `mlb.com/standings` and Al Jazeera opened cleanly.
- **2026-08-17** — *stale search results nearly printed as today's news* — searches for West
  Virginia flooding returned, mixed in with live copy and undated in the result list, the
  **July 21-23 Upshur/Lewis disaster** (2 dead, National Guard, all 55 counties) and a **2022**
  WCHS story reporting a state of emergency in Kanawha and Fayette. The 2022 piece was caught
  only because it named **Gov. Jim Justice**, who has not been governor since 2025. **No state
  of emergency was printed, because none could be confirmed for Sunday's storms.** The lesson
  is the one the paper already knows and nearly missed anyway: open the article and read its
  dateline before believing a search summary, especially when the search terms name a recurring
  kind of event.
- 2026-08-17T11:00:03Z · 2026-08-17 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- **2026-08-18** — *WV MetroNews became unreadable to this crawler.* Every
  `wvmetronews.com` article fetched this morning returned the Cloudflare interstitial
  ("One moment, please... Please wait while your request is being verified") instead of
  copy — including the two stories the West Virginia sweep most wanted:
  **"Goodwin declares State of Emergency in Charleston after devastating flooding"** and
  **"Morrisey: flood recovery transitioning in Lewis County."** Both were reachable in
  search summaries only. **Neither was printed from a snippet.** The Charleston mayoral
  state of emergency therefore did **not** run at all, and the Lewis County story ran
  instead from **West Virginia Public Broadcasting**, which was fetched and read in full.
  This is the paper's best statewide daily going dark; if it holds tomorrow, the
  provisional outlet list in `instructions/edition.md` is effectively one outlet shorter.
  `wowktv.com` also returned **403** on both attempts. WCHS, WVPB, WSAZ, West Virginia
  Watch (403 on one article), the Herald-Dispatch and the Parkersburg News and Sentinel
  all opened normally.
- **2026-08-18** — *budget trim, and the four-brief target lost again.* The edition first
  projected **6,526** against the 5,600 target. The cut ladder ran to the bottom: the
  **away line went** (Bennington's Battle Day parade, written and sourced), then the
  **weakest regional line** (Marshall's fall semester opening, `huntington_cabell`), then
  every summary was tightened toward the low end — and it was still over, so a **wire
  brief was dropped**: Science & Technology ran **three** instead of four, losing a
  University of Arizona item on Webb's "little red dots" (the weakest of the four, its
  journal paper dated July 29). Final projection **5,662**, single message, nothing taken
  by the trimmer. **This is the fourth edition in seven to hit the wall** and it is the
  same arithmetic `docs/LEDGER.md` has flagged twice for Nate: four briefs at ~320 chars
  each against a 1,000-char allocation cannot fit.
- **2026-08-18** — *fishing source degraded, third consecutive morning* — NOAA again
  returned **no water temperature** for the Wrightsville Beach gauge, so both papers
  carried Topsail **tides only**. Williams and both Ohio gauges reported normally.
- **2026-08-18** — *MLS standings unobtainable, so two followed teams sat out* —
  `mlssoccer.com/standings`, its conference variant, `fccincinnati.com/standings` and
  ESPN's MLS pages all returned navigation markup with no table, for a **fifth**
  consecutive morning. A search summary put **FC Cincinnati first in the Eastern
  Conference on 52 points and Columbus Crew sixth on 45**, sourced to aggregators this
  paper does not cite. **Neither number was printed.** Both clubs are in season and both
  went to `sat_out` saying so. Premier League, MLB and NFL fixtures all sourced cleanly.
- **2026-08-19** — *budget trim, and the four-brief target lost for a fifth time in eight
  editions.* The edition first projected **7,213** against the 5,800 ceiling — the worst
  overshoot yet, because this morning's stories sat on unusually long URLs (two
  Herald-Dispatch article slugs at **138** and **145** characters each, an NPR slug at
  **121**). The cut ladder ran to the bottom and past it: the **away desk was already
  empty**, then the **weakest regional line went** (the Wood County assessor's **$357,000**
  projected shortfall, `mid_ohio_valley`, written, opened and sourced from the Parkersburg
  News and Sentinel), then every summary was tightened — and it was still ~1,400 over, so
  **three wire briefs were dropped**: U.S. lost the **Meta child-safety trial opening** in
  Oakland, World lost **UK inflation at a four-month high of 2.9%**, and Science &
  Technology lost the **University of La Laguna Theban tomb** find. All three were written,
  opened and sourced. U.S., World and Sci/Tech each ran **three**. Final projection
  **5,565**, single message. **This is the same arithmetic `docs/LEDGER.md` has now flagged
  for Nate four times: four briefs cannot fit a 1,000-character allocation when a brief
  costs its whole URL.**
- **2026-08-19** — *the sportsman calendar could not print a season date it had confirmed.*
  WVDNR's **2026-27 migratory bird regulations** were found and read — dove **Sept. 1 -
  Oct. 11** (first of three segments), daily 15 / possession 45, shooting hours noon to
  sunset on Sept. 1; snipe **Sept. 1 - Dec. 16**, daily 8; sora and Virginia rail **Sept. 1
  - Nov. 9**, daily 10 — confirmed on **two independently dated 2026 outlets** (West
  Virginia Daily News, **July 14, 2026**; the Parsons Advocate, **July 21, 2026**), which is
  the standard `instructions/sportsman.md` sets. **It still could not run.**
  `validate_edition.py` cross-checks every WV season date against
  `reference/wv-hunting-2026-27.json`, and migratory birds are **deliberately absent** from
  that table — the file says so itself — so the validator raised four hard errors on dates
  that are correct. **The entries were cut rather than routed around the check**, and the
  In Season notes now say the regulations exist and where they live, without a date.
  **This is a gap for Nate, not a source failure:** the reference file needs a migratory
  bird section, or the validator needs to know those dates live in a separate publication.
  Note also that WVDNR issued them in **July**, not August as the ledger expected, so the
  desk missed them for four editions.
- **2026-08-19** — *two followed teams' fixtures ran without times.* Marshall travel to
  **High Point** and West Virginia host **Penn State** on Thursday. Penn State's own
  schedule confirmed the date and Morgantown, and WTRF confirmed WVU's August card, but
  **no page this desk could open stated a kick-off time** for either — `herdzone.com` and
  `wvusports.com` both returned title-only markup, and `therealwv.com` **403**s. Search
  summaries offered 4 p.m. and 7 p.m.; **neither was printed.** Both teams went to
  `sat_out` saying exactly that.
- **2026-08-19** — *fishing source degraded, fourth consecutive morning* — NOAA again
  returned **no water temperature** for the Wrightsville Beach gauge, so both papers
  carried Topsail **tides only**. Williams and both Ohio gauges reported normally.
- **2026-08-19** — *no away line, second morning running.* Vermont searched (the Bennington
  Battle Day parade is a standing annual event, already ruled out on Aug. 14) and Prince
  George searched (a Fire Rescue media release on Barr Road, a Fraser River swim relay
  arrival, a pool closure and a traffic-pattern change — nothing dated hard enough for a
  line). Topsail is carried by its fishing line. `away: []` and the kicker says so.
- **2026-08-20** — *budget trim, two cuts before the gate would pass.* No. 16 projected
  **6,144** against the 5,800 ceiling on the first validate, with `wv` alone at **2,071**
  against its 1,500 allocation. Two cuts, in the playbook's order: the **`huntington_cabell`**
  regional line went (Treasurer Larry Pack presenting Cabell County schools an unclaimed
  property check for $42,869.04, The Herald-Dispatch — real, opened, sourced, and the
  weakest of the three), and the **`putnam_kanawha` line's URL was set to `null`**, a
  165-character Herald-Dispatch slug, keeping the reporting and the outlet name while
  spending nothing on the link. Final projection **5,496**. **The cause is URL length, not
  prose** — the fifth consecutive morning this row has been written, and the arithmetic has
  not changed since 08-17.
- **2026-08-20** — *fishing source degraded, fifth consecutive morning* — NOAA again
  returned **no water temperature** for the Wrightsville Beach gauge, so both papers carried
  Topsail **tides only**. Williams and both Ohio gauges reported normally.
- **2026-08-20** — *no away line, third morning running.* Vermont searched (nothing dated
  inside 48 hours on VTDigger or the Bennington Banner), Prince George searched (council
  non-profit funding deferred to a future meeting, a Canfor Leisure Pool closure Aug. 17 -
  Sept. 6, a draft-horse title and a missing-person notice last seen Aug. 7 — none of it
  news inside the window). Topsail is carried by its fishing line. `away: []`.
- **2026-08-20** — *`validate_edition.py --sportsman` does not credit `upcoming` fixtures.*
  The advisory named **Chelsea, Tottenham, Liverpool, Cleveland Browns and Cincinnati
  Bengals** as "neither covered nor in sat_out" while all five carried cited, ET-converted
  fixture lines in `upcoming`. `instructions/sportsman.md` says plainly that "a team with a
  standings or fixture line counts as accounted for — it does not also need a brief or a
  sat_out entry," so the validator credits `briefs`, `standings` and `sat_out` but not
  `upcoming`. Advisory only, so the edition shipped unchanged; putting five clubs with
  Friday-to-Monday fixtures into `sat_out` would have been the false statement. **A code
  fix for Nate.**
- **2026-08-20** — *the clone was in detached HEAD and local `main` was stale.* `git push`
  was rejected non-fast-forward; `git status -sb` read `## HEAD (no branch)` and local
  `main` sat at `c376454`, two commits behind `origin/main` at `8089c3a`, while the work
  was committed on the detached head at `a813241`. Fixed with `git branch -f main a813241
  && git checkout main && git push -u origin main`, a clean fast-forward from `8089c3a`
  with no history discarded. **Cost about a minute.** The routine's `git pull` in
  `instructions/routine.md` step 1 also fails on a detached head ("Please specify which
  branch you want to merge with") and needs `git pull --rebase origin main` — worth the
  playbook saying so.

- **2026-08-21** — *the clone was in detached HEAD again, second morning running.* Same
  shape as 2026-08-20: `git pull` in `instructions/routine.md` step 1 failed with "Please
  specify which branch you want to merge with," and `git checkout main` aborted because the
  work was uncommitted. Local `main` and the detached head were both at `80b56a8`, so
  nothing was behind this time and no history was at risk. Fixed the same way —
  `git branch -f main dbf5b44 && git checkout main && git push -u origin main`, a clean
  fast-forward. **Two mornings in a row means this is the clone's normal state, not an
  accident.** The playbook's step 1 should read `git pull --rebase origin main`, and the
  commit step should expect a detached head.
- **2026-08-21** — *budget trim: one regional line and one lead paragraph cut.* The first
  pass projected **6,691** against the 5,800 ceiling. Cut, in this order: the lead's third
  paragraph (Bessent's buyback and the mortgage/auto/housing-starts tail, folded into
  paragraph two); every brief summary tightened toward the low end of target; and the
  `huntington_cabell` line — the Sanitary Board closing the 20th Street underpass Wednesday
  9 a.m. to 4:30 p.m. for pump work, written, opened and sourced to The Herald-Dispatch,
  then cut. That is **four separate mornings** a Cabell line has been written and cut for
  budget (Aug. 13, 14, and now 21). Shipped at **5,574 projected**. The Herald-Dispatch's
  article URLs run ~140 characters, which is most of what that line cost.
- **2026-08-21** — *NOAA returned no water temperature for a fifth straight morning.*
  `noaa-temp: RuntimeError: NOAA: no water temperature returned` for the Wrightsville Beach
  gauge, so both papers carried Topsail **tides only**. Williams and both Ohio gauges
  reported normally. Five mornings is no longer a blip — worth Nate checking whether the
  station is retired.
- **2026-08-21** — *r/Sumo could not be reached, so half the daily sumo sweep did not run.*
  `instructions/sportsman.md` requires BOTH r/Sumo and the Japanese press every day.
  `old.reddit.com/r/Sumo/` returned "unable to fetch from old.reddit.com" from this
  pipeline — a tool-level block, not a 403 from Reddit. The Japanese-press half ran
  normally (JSA English pages fetched, Kyodo/NHK searched). Lead-finding only was lost, not
  a citable source, so nothing printed is affected. **Note it if it repeats.**
- **2026-08-21** — *`validate_edition.py --sportsman` still does not credit `upcoming`
  fixtures.* Identical advisory to 2026-08-20, naming **Chelsea, Tottenham, Liverpool,
  Cleveland Browns and Cincinnati Bengals** while all five carried cited, ET-converted
  fixture lines. The warning even contradicts itself in its own text ("neither covered nor
  in sat_out: ... — every team is covered or accounted for, by name"). Advisory only;
  shipped unchanged. **Second occurrence of a code fix already logged for Nate.**
- **2026-08-21** — *`herdzone.com` opened headline-only for the third time.* Both the
  Aug. 16 "Contest With Ohio Postponed" story and the women's soccer schedule page returned
  a title and no body. The postponement is therefore reported in the Our Teams note as a
  fixture this desk could not read past the headline, and **no result or reason was
  printed**. Marshall's own athletics site is effectively unreadable to this pipeline; the
  High Point athletics site opened in full and carried the match report used instead.
- **2026-08-22** — *The four-brief wire target broke the embed budget again, and this time a
  real brief was cut for it.* The first honest draft of No. 18 projected **7,299** against
  the 5,800 ceiling — the worst overshoot logged. Tightening every summary to the low end
  of target and cutting the lead to two paragraphs got it to **6,094**, still over. The
  **U.S. section was dropped to three briefs**, losing a sourced TikTok/COPPA settlement
  brief (Euronews, $400M), and four more summaries were shortened, to reach **5,783**.
  Shipped as one message. This is the *third* consecutive escalation of the row already open
  for Nate: three briefs was the old target and four does not fit. **The section that gave
  is U.S., chosen by this desk rather than by the trimmer at post time.**
- **2026-08-22** — *A regional line shipped with `url: null` for budget, not for sourcing.*
  The `huntington_cabell` line (Synthesis Health into Marshall's Med-Tech building) was
  opened and read at The Herald-Dispatch, but that outlet's article URL is **185 characters**
  and the notebook was 218 over its 1,500 allocation. The `source` name stands; the link was
  dropped. Same root cause as the Aug. 21 Cabell cut — **Herald-Dispatch URLs are the single
  most expensive item in the notebook** and the fourth time in ten days a Cabell line has
  been damaged by it.
- **2026-08-22** — *NOAA returned no water temperature for a sixth straight morning.*
  `noaa-temp: RuntimeError: NOAA: no water temperature returned` for Wrightsville Beach.
  Both papers carried Topsail **tides only**; the Times fishing line omits the temperature
  rather than naming an unattributed one. Williams and both Ohio gauges reported normally.
  **Six mornings. This is not a blip and the station should be presumed retired until Nate
  checks it.**
- **2026-08-22** — *r/Sumo unreachable for a second straight morning.* `old.reddit.com/r/Sumo/`
  returned "unable to fetch from old.reddit.com" — the same tool-level block as Aug. 21, not
  a Reddit 403. Only the Japanese-press half of the required daily sweep ran (JSA English
  pages fetched, Aki dates searched). Lead-finding only was lost; nothing printed is
  affected. **Second occurrence — the sweep is now reliably half a sweep.**
- **2026-08-22** — *`validate_edition.py --sportsman` still does not credit `upcoming`
  fixtures.* Third identical advisory (Aug. 20, 21, 22), naming **Chelsea, Tottenham,
  Liverpool, Cleveland Browns and Cincinnati Bengals** while all five carried cited,
  ET-converted fixture lines, and again contradicting itself in its own text. Advisory only;
  shipped unchanged. **Third occurrence of a code fix already logged for Nate.**
- **2026-08-22** — *Both papers write the same payload file.* `post_discord.py --dry-run`
  wrote `out/2026-08-22.payload.json` for the Times and then the sportsman dry run
  **overwrote the same path**. The payloads are the record of what shipped, so on any morning
  both papers post, the Times payload is lost. Harmless to delivery, but it defeats the
  "settled by a file, not a memory" guarantee. **The sportsman payload wants its own name.**
- **2026-08-22** — *VTDigger returned 403, so Vermont could not be swept.* The away desk ran
  empty: Vermont unreachable, Prince George had nothing past the plane crash No. 17 already
  carried, and Topsail is covered by the fishing line. An empty away desk is a legal edition,
  but Vermont was **not searched**, it was **blocked**, and that is a different thing.
- 2026-08-22T11:00:03Z · 2026-08-22 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- **2026-08-22** — *The Times split into two messages anyway, at 5,997 actual against 5,783
  projected.* After cutting a wire brief and tightening eight summaries to clear the 5,800
  ceiling, the validator projected **5,783** — and `post_discord.py` reported **5,997** at
  post time, splitting into FRONT PAGE and INSIDE "to keep the notebook whole." The **214-char
  gap is the `--page-url` permalink**, which the validator's projection does not count. So the
  desk was tightening against a number that is structurally ~200 low whenever the link goes
  out, which is every morning Pages is green. **The cut wire brief bought nothing.** Fourth
  split in eleven editions (Nos. 8, 12, 13, 18). **Either the validator should add the page-url
  cost to its projection, or the ceiling it advises against should drop by ~250** — this is the
  concrete, fixable half of the four-brief budget row already open for Nate.
- 2026-08-23T11:00:04Z · 2026-08-23 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- 2026-08-23 — *No Topsail water temperature for a second straight morning.* `fetch_fishing.py`
  logged `noaa-temp: NOAA: no water temperature returned`; both papers ran tides without a
  temperature line, per the omit-on-failure rule.
- 2026-08-23 — *The Japan Times sumo desk now returns HTTP 402.* It is the named citable
  English outlet for sumo, and its absence had a cost this morning: r/Sumo (answering for the
  first time since Aug. 19) carried a report that Yokozuna Hoshoryu had late-July knee surgery
  and is doubtful for the Aki basho, and no outlet this pipeline can open and cite carries it —
  NHK World, Kyodo English and Mainichi English are all unfetchable, and the sumo-stats sites
  that do carry it are synthesizers this paper does not cite. **The report was deliberately not
  printed.** The Aug. 31 banzuke coverage will force a citable outlet to say it.
- 2026-08-23 — *A written, sourced `mid_ohio_valley` line was cut for budget* (trees down in
  Wood and Washington counties after Saturday's storms, WTAP) — the weakest line went per the
  cut ladder when the projection ran 6,009 against 5,800. The Times still split at 6,223 actual;
  the ~214-char projection gap is again the `--page-url` permalink, per the row logged 2026-08-22.
- 2026-08-24T11:00:04Z · 2026-08-24 · post_discord: split into FRONT PAGE and INSIDE messages to keep the notebook whole
- 2026-08-24 — *No Topsail water temperature for a THIRD straight morning.* `fetch_fishing.py`
  logged `noaa-temp: NOAA: no water temperature returned`; both papers ran tides without a
  temperature line, per the omit-on-failure rule. Three mornings is starting to look like the
  NOAA product moved rather than hiccupped — worth a look at the station/product id.
- 2026-08-24 — *r/Sumo was unfetchable outright* — the fetch tool refuses `old.reddit.com` in this
  environment ("unable to fetch from old.reddit.com"), which is different from the API 403 the
  playbook works around. The daily sumo sweep ran on the JSA's pages and searches only, and the
  Hoshoryu report stayed unprinted a second morning. If this recurs the playbook's fan-wire step
  needs an alternate route.
