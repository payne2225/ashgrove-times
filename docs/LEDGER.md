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
| **2026-11-03** | **General-election matchups set by Tuesday's primaries** | Minnesota Senate: **Peggy Flanagan (D) v Michele Tafoya (R)**. Minnesota governor: **Amy Klobuchar (D) v Lisa Demuth (R)**. Wisconsin governor: **David Crowley (D) v Tom Tiffany (R)**. Connecticut 1st: **Luke Bronin (D)**. NPR. Ran as No. 8's lead; do not re-run the primary results, the news now is the campaigns |
| **date not established** | **South Carolina Republican Senate runoff** | Sen. **Darline Graham** (Trump-endorsed) finished first with about a third of the vote and advanced against Rep. **Ralph Norman**; NPR notes two thirds of Republicans voted for Norman or Rep. Russell Fry. **The runoff date was not in the piece the paper opened — find and record it before covering** |
| 2026-10-20 | **NBA season opens** | Knicks raise their first banner since 1973 against Philadelphia; Thunder at Spurs; Celtics-Pistons. Knicks-Spurs Finals rematch **Dec. 25**, NBA Cup final **Dec. 11**. CBS Sports. Ran as No. 8's second Sports brief; spent until the season actually starts |
| 2026-08-08 | **Aki basho tickets go on sale** | Confirmed on the JSA's own English page (`sumo.or.jp/En/`) and printed as No. 2's sumo brief. Do not re-run this fact; it is spent |
| 2026-08-08 | Chelsea play AC Milan in Jakarta | Preseason friendly. A followed club, so it is a legitimate football brief if anything happens in it |
| **2026-08-10** | **Nucor Apple Grove site reopens (or does not) after the threat closure** | The mill site closes Monday over a written threat naming that date; FBI, State Police and the Mason County sheriff investigating, sheriff's security posted 10 days. WV MetroNews. A reopening, an arrest, or a second closure is a `huntington_cabell` line or a statewide brief. **2026-08-10: the date arrived and nothing new was reported.** Searched at 6 a.m. ET across MetroNews, WSAZ, Herald-Dispatch, WCHS and the Gazette-Mail; every result was still the Aug. 7 closure announcement, so it was **deliberately not re-run** — the closure taking effect is the same fact No. 4 already printed. The paper posts before the work day, so any Monday development lands in **Tuesday's** edition. **Row stays open:** watch for an arrest, a reopening, a second closure, or the sheriff's 10-day detail ending about **Aug. 17**. **2026-08-11: searched again; the only new line anywhere is that no incident was reported as of Monday afternoon**, carried inside the same Aug. 7 closure stories. Not a brief. The mill is a **$4B** project testing equipment now, with production ramping through 2027-28 |
| **2026-08-12** | **Total solar eclipse over Greenland, Iceland, northern Spain and a corner of Portugal** | Ran as No. 7's first Sci/Tech brief on the eve. The shadow enters Galicia about 19:27 and leaves the Balearics about 20:35; totality nowhere exceeds 1 minute 48 seconds; first in mainland Spain since **April 15, 1912** and first in mainland Europe since 1999. Euronews. **The follow-up is what was actually seen** — cloud, crowds, the ESA and NASA observations. **2026-08-12: it could NOT run in No. 8 and the previous ledger line was wrong to promise it.** Totality reaches Galicia about 19:27 local, roughly **1:30 p.m. ET** — six hours after this paper posts. A 7 a.m. ET edition can never carry a same-day European afternoon event. **It belongs in No. 9 (Aug. 13)**, and Euronews' Aug. 12 preview (eyewear shortages, corona observations from Spain and Iceland) was deliberately not re-run as a second preview. Spain's next two are **Aug. 2, 2027** and **Jan. 26, 2028** |
| **2026-08-24** | **Huntington Public Safety Committee takes up both Flock ordinances** | Mayor Patrick Farrell's ordinance (data access, retention, audits, criminal penalties) and Councilwoman Tia Rumbaugh's graduated-penalty ordinance were introduced Monday Aug. 10 and referred to committee. City Attorney Scott Damron says **no contract has been signed**; the original Sept. 1 implementation date is now uncertain. WSAZ, WV MetroNews. Ran as No. 7's `huntington_cabell` line |
| 2026-08-12 | **WAFCON semifinals** | Malawi v Algeria in Casablanca, Morocco v Cameroon in Rabat. All four have already qualified for the 2027 World Cup in Brazil. Al Jazeera. Ran as No. 6's third Sports brief; the semifinals are the follow-up, and the final is the week after |
| 2026-08-13 | **Peoples Cartage town hall, Parkersburg** | Independent testing results from the warehouse fire. WTAP. A `mid_ohio_valley` line that night or the morning after |
| 2026-08-21 | **Premier League 2026-27 opens** | Confirmed via ESPN's fixtures piece. Until then the football beat is transfers and friendlies only, and a quiet football day is the expected outcome, not a failure |
| **2026-08-31** | **Aki banzuke (rankings) released** | The next genuine sumo news after the ticket date, and the natural moment the Aki dates get confirmed by a citable outlet. Do not print it before it happens |
| 2026-09-10 | WV charter board bylaws vote | Postponed from Aug. 6. WV MetroNews. Small, but it is the follow-up to today's statewide brief |
| 2026-10-02 | DUA filing deadline, Lewis and Upshur | Claims close; benefits run to Feb. 6, 2027. West Virginia Watch |
| 2026-08-13 | **Hope Scholarship first payments** | $5,435.62 each to 25,000+ students, two days ahead of schedule. WV MetroNews. Ran as No. 5's first statewide brief; the news on the day is whether the money actually lands |
| 2026-08-15 | Italy's Schengen suspension with Spain runs to at least this date | Rome said it expects another crossing attempt. Spain's counter-controls run to Sept. 7. Euronews |
| ~2026-09-02 | **FEMA appeal window closes on the Boone/Logan denial** | WVEMD had 30 days from Aug. 3 to file more documentation; Morrisey is appealing. WV MetroNews |
| 2026-09-07 | Spain's border controls on Italian travellers expire | Euronews |
| 2027-01-01 | **WVU Medicine/Fulton County Medical Center closing** | Non-binding LOI signed April 2026; needs regulatory approval. WV MetroNews. Ran as No. 5's second statewide brief — do not re-run before the close |
| 2026-09-13 → 2026-09-27 | **Aki basho (Tokyo)** — *derived, still unconfirmed* | Second-Sunday estimate from `config.basho_window(2026, 9)`. 2026-08-06: the only sources carrying Sept. 13–27 at Ryogoku Kokugikan were ticket-reseller and travel sites, which this paper does not cite. **2026-08-07 and 2026-08-09: searched again, same result both mornings** — travel and ticket-reseller sites only, and `sumo.or.jp/EnHonbashoTopics/banzuke_topics/` now returns a Japanese URL-error page rather than banzuke content. Try Kyodo, Japan Times or NHK at the **Aug. 31 banzuke release**, which is when a citable outlet will have to print the dates. Confirm before covering. During a basho, sumo usually wins the Sports lead |
| 2026-11-08 → 2026-11-22 | **Kyushu basho (Fukuoka)** — *derived, unconfirmed* | Same derivation. Note it opens the week after the cron switch above |

## 3. Open threads

- **midwest-primaries-2026** — 2026-08-12: **resolved, and it led No. 8.** Six states voted Aug. 11.
  **Minnesota**: Lt. Gov. **Peggy Flanagan**, 46, beat Rep. **Angie Craig** for the DFL Senate nod with
  Sanders and Warren endorsements against Craig's fundraising edge, and faces Republican **Michele
  Tafoya**, a former sports broadcaster, in November; **Amy Klobuchar** took the Democratic governor
  primary; House Speaker **Lisa Demuth** beat Trump-endorsed **Mike Lindell** on the Republican side.
  **Wisconsin**: Milwaukee County Executive **David Crowley** edged democratic socialist state Rep.
  **Francesca Hong**, who had led earlier polling; **Tom Tiffany** took the GOP nomination. **Connecticut**:
  **Luke Bronin**, 47, unseated 14-term Rep. **John Larson**, 78. **South Carolina**: **Darline Graham** to a
  runoff with **Ralph Norman**. NPR's four-takeaways piece is the spine. **Alabama** also voted (Trump-endorsed
  **Rhett Marques**), and **Vermont** voted, which is what finally gave the away desk a line. **Thread closes;
  November is a new story.**
- **colombia-earthquake** — 2026-08-12: **moved and ran as No. 8's first World brief, not the lead** — a second
  straight front page on the same disaster loses to a fresh six-state primary night. **The toll is disputed
  between two readable outlets and the paper printed the floor:** NPR (Aug. 12, 1:13 a.m. ET) has **181 dead,
  2,595 injured, 195 missing** officially with a civilian database near **4,000** missing; **Euronews (1:58 a.m.
  ET) has 216 dead** and says authorities revised after Cali corrected its numbers. Printed as **"at least 181"**
  attributed, which stays true under both, per the Thailand and Nizhnekamsk precedent. **The magnitude is also
  disputed — NPR 7.4 (as No. 7 printed), Euronews 7.6 — and was dropped from the brief entirely.** Euronews adds
  a 36-hour rescue of **Daniela Largo** in Pereira, a partial collapse at **Hospital Universitario del Valle**,
  dome damage at the **Cathedral of Manizales**, and **EUR 2M** from the EU on top of the US **$15.5M**.
  **Re-check the toll before citing it; expect it to keep moving.**
- **water-system-cyberattacks** — 2026-08-12: **moved and ran as No. 8's first U.S. brief**, five days after it
  last appeared (No. 2, Aug. 6). The FBI has now confirmed attacks in **at least seven states**; **more than 30
  Minnesota systems** were hit **July 26-28**, including **Braham**, where a pump failure threatened supply for
  **1,700** people, and **Maple Plain**; also Clayton County, Ga. (brief boil-water advisory), New Jersey,
  Michigan, Pennsylvania and Vermont. **No official US attribution**; an anonymous expert told NPR of
  intelligence linking it to the **IRGC**, and DHS/CISA had updated an April advisory days before. **Jake Braun**
  (former acting principal deputy national cyber director): "It appears this is a shot across the bow from Iran."
  **Rob Lee** (Dragos) quoted. No contamination anywhere. NPR. **News again on a formal attribution or a
  contaminated system.**
- **gilman-release** — 2026-08-12: new, ran as No. 8's second U.S. brief. **Robert Gilman**, 32, a former Marine
  and Massachusetts teacher detained in **2022** after being removed from a train, sentenced to 3.5 years and
  extended twice to **10** for assaults in custody, was released and flown to **Andrews Air Force Base**, then to
  a military hospital in Texas. **Trump announced it after speaking with Putin and said Russia asked for no one
  in return.** He had been hospitalised with a feeding tube since early July after 47 days in what NPR calls a
  dissociative stupor. **Rubio**: "we are still seeking the immediate return of all other unjustly detained
  Americans." NPR. **Thread closes unless another American is released.**
- **zimbabwe-ferry** — 2026-08-12: new, ran as No. 8's second World brief. An overloaded ferry capsized on **Lake
  Kariba** Tuesday: **114 registered adults plus 5 crew** on a vessel rated for **90**, with children below
  ticketing age possibly aboard, so the paper wrote **"at least 119."** **At least 15 dead, 27 missing, 77
  rescued** onto an island. Zimbabwe's **Civil Protection Unit** recommended it be declared a disaster; an
  underwater search team deployed. PBS NewsHour, carrying AP. **News again on a recovered toll or an inquiry.**
- **putin-shadow-fleet** — 2026-08-12: new, ran as No. 8's third World brief. Putin, aboard the cruiser **Varyag**
  at naval drills off **Sakhalin** on Wednesday, called European interceptions of sanctioned Russian oil tankers
  "piracy and banditry" and said "we will be forced to respond in kind," anywhere Moscow "deems necessary."
  Context: EU sanctions approved last month let member states sell seized cargo, and Swedish court documents show
  Stockholm transferring a seized ship suspected of carrying grain from occupied Ukraine to Kyiv. Euronews.
  **News again on an actual seizure of a European vessel.**
- **wv-storms-flooding** — 2026-08-12: new, ran as No. 8's first statewide brief **and it is the live WV thread.**
  Tuesday evening storm lines brought flash flood warnings for **Kanawha, Roane, Jackson, Mason and Putnam**
  counties (extended to 6:15 p.m.); **Appalachian Power counted about 20,500 customers out by 9 p.m.**, worst in
  Charleston, Hico and Hamlin, with restoration estimated 11 p.m. Wednesday. **Nitro Fire Department ran water
  rescues on Heizer Creek Road** in Putnam. Kanawha Homeland Security director **C.W. Sigman** and Point Pleasant
  Mayor **Amber Tatterson** ("We're out there with brooms trying to sweep it outside") quoted. WCHS separately had
  a flash flood warning for **Clay and Jackson**, Fairplain flooding, and Ohio Gov. **Mike DeWine** warning of
  flooding "certainly through Thursday." **This is the same system as No. 8's third U.S. brief (CBS: ~991,000 out
  across Illinois, Indiana, Ohio and Kentucky, two dead) — deliberately run in both sections because the WV
  detail and the four-state total are different stories.** **News again on a fresh round, a WV death, or a
  multi-day outage; more storms were forecast.**
- **kanawha-storm-death** — 2026-08-12: ran as the `putnam_kanawha` line, and it is **a separate MetroNews story
  from the storm brief above, not the same story twice** — a tree fell on a motorcyclist at **Pinch**, near
  Heartland Lane and Rutledge Road, about **8 p.m. Tuesday**, bringing down power lines that ignited. Kanawha
  County Sheriff's Office investigating; **no identity released** and the paper named nobody. WV MetroNews.
  A cause finding is a follow-up line; nothing else is.
- **peia-finances** — 2026-08-12: new, ran as No. 8's second statewide brief. Director **Brent Wolfingbarger**
  told the **Joint Standing Committee on Insurance and PEIA** at August interims that the plan is **$67M ahead of
  FY2026 projections**, on a projected **$345M** year-end reserve, on lower medical and drug claims and higher
  investment returns, and that premiums would likely rise **less than the 3%** previously anticipated. Sen.
  **Robbie Morris (R-Randolph)** called it "probably some of the best news that's come out of this committee in
  quite a while." WV MetroNews. **News again at the PEIA Finance Board's rate-setting, which is where the actual
  premium number gets decided.**
- **vermont-primary** — 2026-08-12: **the away desk ran for the first time in six editions.** Vermont voted
  Aug. 11: **Amanda Janoo** won the Democratic nomination for governor, **Molly Gray** the lieutenant governor
  primary, and **Gerald Malloy** the Republican US House nomination against incumbent **Becca Balint**. Vermont
  Public, using AP for statewide and the Secretary of State for county races. **The Bennington-district Senate
  primary the last three editions were waiting for was NOT obtainable** — Vermont Public prints only contested
  statewide races and points to `electionresults.vermont.gov`; **VTDigger 403s this crawler**, which is new and
  worth knowing. **If the Bennington seat matters, the Secretary of State's results site is the route.**
- **ucsd-microglia** — 2026-08-12: new, ran in Sci/Tech. UC San Diego researchers reported in **Immunity**
  (Aug. 11) that overburdened **lysosomes** in **microglia** activate the **MITF/TFE** protein family as a master
  genetic switch, flipping the cells into a state that first protects and then damages the brain — a pathway
  shared by **Sanfilippo syndrome type A (MPS IIIA)**, a childhood dementia, and **Alzheimer's**. First author
  **Christopher Balak**; senior author **Christopher Glass**, professor of cellular and molecular medicine. Mouse
  models plus human Alzheimer's tissue; NIH and NSF funded. `source` names the institution, same convention as
  Nos. 4-7. News again on a drug candidate aimed at the lysosomal pathway.
- **mosquito-species** — 2026-08-12: new, ran in Sci/Tech, and **it is two days old (Euronews, Aug. 10) — the
  oldest thing in the edition.** Florida International University tested **119** volunteers in Miami against
  **Aedes aegypti**, **Aedes albopictus** and **Culex quinquefasciatus** and found no one highly attractive to all
  three; published in **iScience**. **Kaylee Marrero** lead, **Matthew DeGennaro** senior. Run because Sci/Tech
  had nothing dated Aug. 11-12 that opened. Thread closes.
- **vikings-qb** — 2026-08-12: ran as No. 8's first Sports brief. **Kyler Murray**, 29, signed in March after his
  Arizona release, beat out 2024 first-rounder **J.J. McCarthy** two weeks into camp; **Kevin O'Connell**
  announced it Tuesday. Preseason opener Saturday v the Giants. NFL.com. Thread closes.

- **colombia-earthquake** — 2026-08-11: **led No. 7.** Magnitude **7.4** near **San Jose del
  Palmar**, Choco department, about **250 miles west of Bogota**, shortly after **7:30 a.m.
  Monday**; **132 dead and 570 injured**, Colombia's strongest this century. At least **21
  aftershocks** within hours. NBC News: ~**5,000 homes** damaged or destroyed, **three
  hospitals collapsed**, 18 more affected, **39 schools**, **seven airports** shut (Cali,
  Pereira, Manizales, Quibdo, Armenia, Cartago, Buenaventura). President **Abelardo de la
  Espriella**, sworn in three days earlier, declared a state of emergency; **Cali** imposed a
  nighttime curfew. US pledged **$15.5M**; El Salvador, Mexico, Chile, Israel, Ecuador and
  France also offered. Cross-checked Al Jazeera, NBC News and Euronews. **Three numbers were
  deliberately not printed:** the injured count is **570 (Al Jazeera, Euronews) against 700
  (NBC)** so the twice-supported figure ran; the **missing** count ranged from **188 (NBC) to
  1,400+ (Al Jazeera)** and was dropped entirely; and the depth is **107 km (Al Jazeera) vs
  110 km (Euronews)**, dropped. **Expect the toll to move — re-check before citing it.**
- **vaccine-schedule-eo** — 2026-08-11: new, ran as No. 7's first U.S. brief, and it is the
  movement on `measles-35-year-high`. Trump signed an executive order **Aug. 10** moving
  **RSV and hepatitis A and B** to high-risk children only, splitting **MMR** into three
  separate shots spaced across visits, and giving **HHS 90 days** to reassess sequencing and
  timing; he tied it to autism, which the reporting calls debunked. **The count of vaccines
  is disputed and was not printed:** NPR has **17 to 11**, NBC has **18 to 11**; only the
  **11** is common, and the headline was rewritten to avoid a number the cited CBS piece does
  not carry. American Academy of Pediatrics called it "disheartening" and "dangerous"; Sen.
  **Bill Cassidy**, a physician, broke with it. A January 2026 CDC schedule change was
  already blocked by a judge. CBS News. **News again on the first lawsuit or an ACIP move.**
- **noaa-july-record** — 2026-08-11: new, ran as No. 7's second U.S. brief, and it is the US
  counterpart to `copernicus-july-2026`. NOAA put the contiguous US July average at
  **76.89F**, **0.125F** above the **July 1936** Dust Bowl record, in records back to
  **1895**; nighttime lows beat their record by **0.7F** and were the main driver; every
  Lower 48 state ran at least **1F** above its 20th-century average. **Russ Vose**, chief of
  monitoring at NOAA NCEI, quoted. PBS NewsHour. News again at the August report, early
  September, or a named attribution study.
- **midwest-primaries-2026** — 2026-08-11: new, ran as No. 7's third U.S. brief on the
  morning of the vote. **Minnesota** DFL Senate: Lt. Gov. **Peggy Flanagan** (Sanders and
  Warren endorsements) v Rep. **Angie Craig** (fundraising edge); MN GOP governor: **Mike
  Lindell** leading after a Trump endorsement, over **Kendall Qualls** and Speaker **Lisa
  Demuth**. **Wisconsin** Democratic governor: state Rep. **Francesca Hong** (Democratic
  Socialist) leading **David Crowley**; **Tom Tiffany** effectively unopposed on the GOP
  side. NPR. **Connecticut, Vermont and partial Alabama also voted Aug. 11** — Alabama's is a
  rescheduled second primary after May redistricting. **The results are No. 8's brief, and
  Vermont's Bennington County Senate race is the away desk's first live hook in a week.**
- **assad-death-sentence** — 2026-08-11: new, ran as No. 7's first World brief. A Syrian
  court sentenced **Bashar al-Assad** and his brother **Maher** to death **in absentia** for
  war crimes and crimes against humanity over the 14-year conflict; their maternal cousin
  **Atef Najib**, a former brigadier general who ran Political Security in **Daraa** and was
  convicted of leading the **2011** crackdown, was tried in person and drew the same
  sentence. Both brothers fled to **Russia** in December 2024 when forces under interim
  President **Ahmed al-Sharaa** took Damascus. Euronews, which flagged the piece as still
  updating. **Re-check the story before following it; news again on an extradition request
  or further verdicts.**
- **hormuz-reopening** — 2026-08-11: **moved, and it is the movement this ledger has been
  waiting for since Aug. 9 — a US answer to the six conditions.** Trump, at the White House
  Monday, answered Tehran's reparations demand with a counterclaim: "We're going to ask for
  money for the damage they've done over a 50-year period," naming the **17** sailors killed
  on the **USS Cole** in October 2000, US combat deaths, and damages in Lebanon, Syria,
  Yemen and Gaza, and asserting **52,000** killed in Iran in recent months. Iran's foreign
  ministry spokesman **Esmaeil Baghaei** said the Oman corridor talks are "progressing
  smoothly and constructively" with shipping route maps agreed and technical issues open.
  MarineTraffic crossings: **15 Friday, 11 Saturday, 6 Sunday**. Al Jazeera. Other outlets
  put oil **5%** higher on the day; **not printed**, because the Al Jazeera piece the paper
  actually opened carries no price. **News again on a signed corridor deal or an Iranian
  answer to the counterclaim.**
- **zaporizhzhia-nk-missiles** — 2026-08-11: new, ran as No. 7's third World brief and it
  supersedes `nizhnekamsk-strike` as the live Ukraine thread. Overnight strikes on
  **Zaporizhzhia** killed **six** and wounded **19**; **three** more died in Dnipropetrovsk
  region; Kyiv also hit. **Zelenskyy said the city was struck with North Korean ballistic
  missiles, Zircons and guided bombs** — printed as his claim, not as fact — and said it is
  "the first time they cannot wage war without supplements from North Korea." He warned
  Monday of **30,000-50,000** more North Korean troops. Russia's MoD said it hit
  "military-industrial enterprises and transport-logistics centres" and did not address the
  North Korean weapons. Euronews. **News again on independent confirmation of the missile
  type, or the troop deployment.**
- **wv-overdose-decline** — 2026-08-11: new, ran as No. 7's first statewide brief. **Dr.
  Stephen Loyd**, director of the Office of Drug Control Policy, told the **Joint Standing
  Committee on Health** at August interims that overdose deaths are down **41.6% from
  pre-pandemic levels** and neonatal abstinence syndrome down **44.2%**, while WV rates
  remain about **2.5 times the national average** (the state had the nation's highest rate in
  2021). **136,276** naloxone kits distributed; nearly **6 million** fewer opioid doses
  prescribed in 2025 than 2024, about **11%** down across all **55** counties. Senate Health
  Chairman **Brian Helton (R-Raleigh)** cautioned against celebrating early. WV MetroNews.
  **News again on the next annual count or a funding decision.**
- **wv-child-fatality-report** — 2026-08-11: new, ran as No. 7's second statewide brief and
  it is a live oversight thread. The Child and Incident Review Team's report to lawmakers
  covered **29 child deaths reviewed January through April** (32 incidents total) in what
  **Del. Adam Burkhammer (R-Lewis)** called three bullet points; **Del. Kayla Young
  (D-Kanawha)**: "We mandated what information has to be included in this report, and they're
  just not doing it." **Del. Margitta Mazzocchi (R-Logan)** pressed on school suicide
  prevention. **Kendra Boley Rogers**, deputy commissioner of the Bureau for Social Services,
  said she was "not prepared to speak to that today." WSAZ's own investigative piece. **News
  again on a revised report or a bill; this pairs with `dohs-out-of-state-placements`.**
- **wv-flock-plate-readers** — 2026-08-11: **moved to Huntington, exactly as No. 6 predicted,
  and ran as the `huntington_cabell` line rather than a second statewide brief.** Council
  introduced **two** ordinances Monday night: Mayor **Patrick Farrell**'s (data access
  guidelines, retention, audits, criminal penalties for misuse) and Councilwoman **Tia
  Rumbaugh**'s (graduated penalties for repeat abuse). Farrell: "Nobody wants to live in a
  surveillance state," and he noted camera-issued traffic tickets are already illegal in WV;
  he cited **40 pounds** of fentanyl seized over 19 months. Councilwomen **Sarah Walling**
  and **Holly Smith Mount** objected to the pace. Chairman **Mike Shockley** said the
  contract will not proceed until ground rules exist; City Attorney **Scott Damron** said
  **nothing is signed**. The **$2.1M** contract passed **6-4** in July. **Both ordinances go
  to the Public Safety Committee Aug. 24** (above). WSAZ and WV MetroNews. The statehouse
  half is unchanged: **Del. Patrick Lucas (R-Cabell)** files a bill in January.
- **nicholas-storm-outages** — 2026-08-11: ran as the `nicholas_webster` line. Monday's
  storms left more than **4,000** Appalachian Power customers out across central and southern
  WV, **just over 2,000 of them in Nicholas County**, the most of any county; the story
  carried no restoration estimate. WSAZ had First Alert Weather Days running **Aug. 10
  through Thursday**. WV MetroNews. **A multi-day outage or a second round makes it news
  again; a clean restoration does not.** Note the cabin region is on this line for the first
  time in the run.
- **bridgewater-retires** — 2026-08-11: new, ran as No. 7's first Sports brief. **Teddy
  Bridgewater** retired at **33** after **11** seasons; Detroit put him on the reserve/retired
  list **Sunday** and signed **Josh Dobbs**, 31, to a one-year deal worth **$1.425M** with
  **$475,000** guaranteed. Career: **15,182** passing yards, **75** TDs, **47** INTs over
  **83** games and **65** starts for Minnesota, New Orleans, Carolina, Denver, Detroit and
  Tampa Bay; in 2019 he went 5-0 filling in for Drew Brees. Dan Campbell quoted. CBS Sports.
  Thread closes; not a running story.
- **wvu-defense-rebuild** — 2026-08-11: new, ran as No. 7's second Sports brief and it is the
  live WVU camp thread now. WVU allowed **30.8** points a game in 2025, **112th** nationally,
  and **36.2** in Big 12 play, giving up **445+** yards a game in conference. Senior
  linebacker **Ben Cutter** (6-0, 228) is the **only** returner among the team's top 17
  tacklers from 2025; DC **Zac Alley**: "We were boom or bust last year." WV MetroNews.
  **`wvu-qb-battle` is still open and still unresolved** — Rodriguez held a media
  availability Monday Aug. 10 and again did not name a starter between Scotty Fox Jr. and
  Michael Hawkins Jr., as he also declined to at Big 12 Media Days on July 8. **Fan Day is
  Aug. 28.**
- **eclipse-2026** — 2026-08-11: new, ran in Sci/Tech. See the Aug. 12 forward-dated row for
  the detail. Sourced to **Euronews** after `science.nasa.gov`'s eclipse page **404'd** and
  `esa.int` **403'd**; phys.org had the fullest write-up (ESA director **Carole Mundell**
  quoted, **60+** high-altitude balloons from Spain and Iceland, a NASA plane chasing at
  **460 mph**) but reads like syndicated wire copy, so it was not cited. **Those details are
  available if the follow-up needs them and a byline can be established.**
- **saturn-cusp** — 2026-08-11: new, ran in Sci/Tech. **Lancaster University** researchers —
  **Dr. Licia Ray**, **Dr. Sarah Badman** and **Dr. Chris Arridge** — used **Cassini** data
  from **2004 to 2010** to show Saturn's magnetospheric cusp sits typically between **13:00
  and 15:00** local time and sometimes toward 20:00, not near noon as at Earth, dragged round
  by the planet's **10.7-hour** rotation and plasma from **Enceladus**. Published in **Nature
  Communications**; read via ScienceDaily's reproduction dated **Aug. 10**, with `source`
  naming the institution, same convention as Nos. 4, 5 and 6. `nature.com` redirects to an
  auth wall and cannot be opened. News again on an aurora result built on it.
- **typhoon-dolphin** — 2026-08-10: **led the paper on its third day in it, and
  the lead was the movement, not the setup.** Landfall near **Yuhuan**, Zhejiang,
  late Sunday as a typhoon, sustained winds **151 kph**. A central Shanghai
  station measured **nearly 313 mm** in the 24 hours to 7 a.m. Monday, the city's
  heaviest 24-hour total in **more than 150 years** of records; another city
  station measured nearly 400 mm. **1M+ evacuated** — 900,000+ in Wenzhou,
  **215,600** in Shanghai by Sunday evening, ~99,000 in Fujian. Zhejiang averaged
  **173 mm** Friday evening to Monday morning, beating Lekima and Bavi. Weakened
  to a tropical storm Monday morning; rain forecast into Anhui, Jiangsu, Henan
  and Hubei through Wednesday, Beijing Tuesday-Thursday, some areas 200-400 mm.
  Read on Al Jazeera and the Irish Times (crediting the Guardian). **No death
  toll ran, on purpose:** neither readable outlet carried one, Gulf News had "30"
  with no corroboration, and Al Jazeera reported a nine-year-old missing in the
  sea at Wenling. **Re-check the toll before citing it and expect it to move.**
  News again on a confirmed toll, Beijing flooding, or the rain totals inland.
- **interlochen-abuse-report** — 2026-08-10: new, ran as No. 6's first U.S.
  brief. Independent review by Sanghavi Law Office, hired by Interlochen Center
  for the Arts in 2024: **~70 allegations of sexual abuse by nearly 50 adults**,
  **1950s to the 2010s**. Jeffrey Epstein, an alumnus and benefactor, and
  Ghislaine Maxwell are in it; NPR previously reported Epstein recruited two
  teenagers on campus. Three former staff and one former trustee named; **Thomas
  Clower** is the only one still living (2005 misdemeanor plea, ~60 days). School
  says it is "fundamentally different"; names went to local law enforcement and a
  counseling fund was set up. NPR. **News again on a charging decision or a
  civil suit.**
- **measles-35-year-high** — 2026-08-10: new, ran as No. 6's second U.S. brief.
  NIH Director **Jay Bhattacharya** on CBS's *Face the Nation* Aug. 9 said
  parents should vaccinate children against measles and that he vaccinated his
  own; measles at its **highest level in 35 years**; only **10 states** hit the
  **95%** kindergarten coverage needed for herd immunity in 2024-25. He did not
  criticize RFK Jr. directly. CBS News. **The angle to watch is a public split
  between NIH and HHS**, or a case count with a number attached — CBS printed
  none, so no count was published.
- **netanyahu-gaza-plan** — 2026-08-10: new, ran as No. 6's first World brief.
  Netanyahu told his Cabinet Aug. 9 the military "will not carry out any
  withdrawal until Hamas is genuinely disarmed," explicitly rejecting **the
  15-point document**, while saying talks with Washington continue. Israeli
  forces hold more than half of Gaza. Hamas's Bassem Naim expects mediators to
  pressure him; Netanyahu faces **Oct. 27 elections**. PBS NewsHour. News again
  on a US response, a revised plan, or a first withdrawal step.
- **nizhnekamsk-strike** — 2026-08-10: new, ran as No. 6's second World brief.
  Ukrainian drones hit **Nizhnekamsk**, Tatarstan, an oil and petrochemical hub
  of 240,000 more than **1,000 km** from the border; Tatarstan authorities said
  **12 killed, 39 wounded**. Russia's MoD claimed **456** drones downed
  overnight; Ukraine's air force reported 126 Russian drones back. Five killed by
  artillery at **Bugaivka**, Kharkiv region, one in Belgorod, one in Kherson.
  Euronews. **The toll is disputed — CNN and NBC had 13, Euronews and NPR 12**,
  so it printed as "at least 12" per the disputed-number rule. News again on a
  refinery-output effect or a confirmed toll.
- **copernicus-july-2026** — 2026-08-10: new, ran as No. 6's third World brief,
  **sourced to Copernicus's own bulletin page rather than to wire paraphrase.**
  July 2026 was the **joint-second warmest July globally**, tied with July 2024;
  **Western Europe had its warmest June-July on record.** Euronews's write-up of
  the same bulletin adds figures the paper did not print: 21.62C Western European
  June-July mean, France 3.8C above the 1991-2020 normal, ~900M people in their
  hottest July (~120M Europeans, ~400M Africans in the Sahel), global July 1.47C
  above pre-industrial, 42,000 ha burned in France with 220,000+ evacuated.
  Samantha Burgess (ECMWF) quoted there. **Those are available if this needs a
  second day.** News again at the August bulletin, early September.
- **wv-flock-plate-readers** — 2026-08-10: new, ran as No. 6's first statewide
  brief and it is **the live WV policy thread.** At Sunday's August interims a
  committee heard **Kevin Kane** (Flock Safety government affairs) and **Alasdair
  Whitney** (Institute for Justice), who argued officers can search people's
  whereabouts **15,000 times a day** without a warrant. **Del. Patrick Lucas
  (R-Cabell)** will introduce a bill "on day one" in January; **Del. Ryan
  Browning (R-Wayne)**: the hearing "raises more concerns than actually giving us
  answers"; **Del. Evan Hansen (D-Monongalia)** also drafting. **Huntington has a
  $2.1M Flock contract.** WSAZ (their own investigative piece) and WV MetroNews
  both covered it. **Note the overlap trap:** the Herald-Dispatch had a Huntington
  City Council public-safety committee taking up its own AI-camera and
  plate-reader ordinance **Monday**, which would have been the same story twice
  in one section, so no `huntington_cabell` line ran. **That ordinance is
  Tuesday's regional line if the committee acted.**
- **dohs-out-of-state-placements** — 2026-08-10: new, ran as No. 6's second
  statewide brief. **Christina Mullins**, DoHS deputy secretary for mental health
  and substance use disorders, told the **Joint Standing Committee on Finance**
  on Aug. 9 that out-of-state child placements are "financially unsustainable" at
  **$142,000 per child**; a **BDO** audit released **May 2026** found **$68.6M**
  in possible annual savings. The **PATH** system has cost **$300M+** and runs on
  a **40-year-old mainframe** backend — outages, slow loads, manual work — with a
  cloud migration projected to save **$7.2M a year**. WV MetroNews. News again on
  a procurement decision or a placement count, which the story did not give.
- **kanawha-water-mains** — 2026-08-10: ran as the `putnam_kanawha` line. West
  Virginia American Water made emergency repairs on **four** main breaks over the
  weekend: Nitro (Holly-to-Center, 8:45 a.m. Sat., with police reporting street
  flooding; Washington Ave., 10 a.m. Sun.), St. Albans (Lore/Hill, 9 a.m. Sat.)
  and Kanawha City (Rt. 61 to Venable SE, before 9:30 a.m. Sun.). No boil-water
  advisory and no customer count reported. WV MetroNews. **A fifth break or an
  advisory makes it news again; a clean week does not.**
- **don-nelson-death** — 2026-08-10: ran as No. 6's first Sports brief. Died
  **Sunday morning**, aged **86**; family statement. Retired **2010** as the
  NBA's winningest coach with **1,335** regular-season wins, since passed by
  Gregg Popovich (1,390); five titles as a **Boston Celtics** player; three-time
  Coach of the Year; Hall of Fame **2012**; coached Milwaukee, Golden State, New
  York and Dallas; "Nellie Ball." Cross-checked CBS News and Al Jazeera. **Note
  Al Jazeera's page said "Sunday, August 10" — internally contradictory, since
  Aug. 10 is Monday — so the paper wrote "Sunday morning" and no date.** Thread
  closes after any memorial; not a running story.
- **followed-clubs-final-friendlies** — 2026-08-10: ran as the football brief.
  **Liverpool 2-3 Monaco at Anfield, Aug. 9**, Isak 16', Wirtz 29', then Golovin
  44' pen, Biereth 56', Brunner 88' — **Andoni Iraola's first Anfield game in
  charge**, and the second time in pre-season Liverpool led by two and lost
  (4-2 to Leeds in Chicago). **Chelsea 3-3 at Johor Darul Ta'zim**, Sultan
  Ibrahim Stadium, Delap 42' and 62' both penalties, Glauder own goal 89'; Arif
  Aiman 14', Arribas 65', Bergson 86' — Chelsea's tour closer under Xabi Alonso.
  Both read on Sky Sports. **Liverpool took the headline over Chelsea on the
  what-actually-happened test, not the supporter tiebreak** — a home defeat on a
  new manager's Anfield bow outranks a tour draw. **Premier League opens Aug.
  21**, so Tuesday-through-Thursday football is transfers only.
- **wafcon-2026** — 2026-08-10: new, ran as No. 6's third Sports brief.
  **Cameroon 1-0 Nigeria** in Casablanca, **Myriam Nyadjou** free kick 19', ending
  the **10-time** champions' reign and only Cameroon's second win in 14 WAFCON
  meetings with them; Oshoala came on and could not equalise. **Malawi 2-1
  Ghana** in Rabat. All four semifinalists are through to the **2027 World Cup in
  Brazil**; losing quarterfinalists get playoff routes. Al Jazeera. Semifinals
  **Aug. 12** (above).
- **voyager2-power** — 2026-08-10: new, ran in Sci/Tech **and supplied the
  drawing.** JPL engineers ran a manoeuvre nicknamed the **"Big Bang"** —
  shutting down power-hungry components simultaneously while switching to
  lower-power alternatives and holding spacecraft temperature — expected to keep
  the nearly-50-year-old probe's **three remaining instruments** running **at
  least one more year**. The RTGs lose about **4 watts a year**. NASA JPL, read
  via ScienceDaily's reproduction; `source` names JPL, same convention as No. 4
  and No. 5. News again at the next instrument shutdown or a loss of contact.
- **kimsuky-offline-ai** — 2026-08-10: new, ran in Sci/Tech. South Korean firm
  **Genians** reported the North Korean state-backed **Kimsuky** group using
  **offline** large language models (Ollama, GPT4All, Msty — chosen to run
  without internet and evade detection) to generate decoy documents for
  spear-phishing at military, diplomatic and academic targets. Elliptic's figure
  of **$2B+** in crypto stolen in the first nine months of 2025 is context in the
  same piece, not printed. Al Jazeera. News again on an attributed breach.
- **hormuz-reopening** — 2026-08-10: **deliberately not run for the second time
  in the run, and the reason is worth keeping.** Brent October futures were up
  more than 1% at **$84.11**, ~16% since the war opened in late February; only
  **8-15 vessels** a day crossed Aug. 4-6 against ~130 before the conflict.
  Araghchi repeated that sanctions relief and reparations come first; Trump told
  CBS the US is "semi-negotiating" and signalled economic pressure over a new
  offensive; **Mohsen Rezaei** has replaced Zolghadr atop the Supreme National
  Security Council; Iran's parliament approved "general outlines" barring
  vessels of "hostile countries" until compensation; the Iran-Oman interim
  corridor is still in final stages. Al Jazeera, PBS NewsHour, CBS. **A price
  move and a restated demand are not movement** — No. 5 already led on the six
  conditions. It is news again on a signed corridor deal, a US answer to the
  conditions, or the 60-day window lapsing, **which is due about now.** The
  leadership change at the SNSC is the freshest genuinely new fact and would
  carry a brief on its own if it is still unrun.
- **hormuz-reopening** — 2026-08-09: **moved hard, and led No. 5.** Iran's
  Supreme National Security Council, via secretary Mohammad Bagher Zolghadr
  (also an IRGC commander), said the strait will not reopen until the US
  "corrects its behavior" and set **six conditions**: an end to US threats, a
  permanent halt to attacks on Iran and its allies in Lebanon, Palestine, Yemen
  and Iraq, lifting the naval blockade and withdrawing from Iranian waters,
  compensation for two wars, an end to sanctions, and unconditional release of
  frozen assets. **That is broader than the June 17 MoU and recasts phased,
  reciprocal steps as preconditions** — Al Jazeera's own framing, and the point
  of the story. Simultaneously Iran and Oman have nearly settled a corridor
  plan: inbound through Iranian waters, outbound through Omani waters, interim
  60 days. Araghchi called it "very close"; Pezeshkian said "now is the best
  time for an agreement." US position (Al Jazeera, citing Reuters) ties lifting
  the port blockade to restored unimpeded shipping — reciprocal, not
  conditional. Cross-checked on NBC News and CSMonitor; NBC adds an **ADNOC
  vessel hit by an Iranian missile early Saturday**, one crew member killed and
  20 wounded across a dozen-plus ADNOC ships since February. Al Jazeera also
  reported Brent near **$83**, the rial at 1.85M/dollar, Tehran's exchange +2%.
  **The 60-day negotiating window ends in about a week (CSMonitor).** News again
  on a signed arrangement, a US answer to the six conditions, or the window
  lapsing.
- **typhoon-dolphin** — 2026-08-09: **ran as a World brief for the second day,
  and it moved.** Red alert (China's most severe) issued Sunday morning;
  ~500,000 moved, including 390,000 from Taizhou, 30,000+ from Shanghai and
  99,000 in Fujian; **1,600+ flights cancelled**, ~1,400 of them at Shanghai's
  two airports and 270 at Hangzhou; 200+ ferry routes suspended; 250-500mm
  forecast for central and eastern Zhejiang; sustained winds to 162 km/h.
  Okinawa: seven injured, 50,000+ buildings cut off. Landfall was expected
  **overnight Sunday into Monday** near Yuhuan/Wenling — *some outlets were
  already reporting landfall Sunday morning and the paper deliberately wrote
  "nears landfall" instead, following the source it had actually opened.*
  Al Jazeera. **Monday's follow-up is the toll and the rain totals.**
- **bc-wildfires** — 2026-08-09: new, ran as a World brief. Premier David Eby
  declared a provincial state of emergency Saturday; 100+ fires, nearly half out
  of control; **20,000+ evacuated**, Summerland (~12,000) and Peachland (~8,000)
  ordered out; the Bald Range fire grew to ~50 sq km in hours. PBS NewsHour.
  **This is the Okanagan, not Prince George** — checked, and Kirsten's region is
  not named in the coverage, which is why it ran in World and not on the away
  desk. If it reaches the north, it becomes a `prince_george` away line.
- **spain-italy-ceuta** — 2026-08-09: new, ran as a World brief. Spain's
  retaliatory border controls on Italian travellers began at midnight Saturday
  and run to **Sept. 7**; Italy's own checks started **Aug. 1** and hold to at
  least **Aug. 15**. Rome: "Italy does not accept ultimatums." Trigger was
  **72,000** migrants arriving at Ceuta from Morocco in late July; 1,342
  children remain, many unaccompanied. Euronews. News again on an EU Commission
  intervention or either side standing down.
- **hope-scholarship-2026** — 2026-08-09: new, ran as No. 5's first statewide
  brief. 25,000+ students approved for 2026-27 out of nearly 29,000 started
  applications; **$5,435.62** each; 1,485 providers; first quarterly payments
  **Aug. 13**, two days early. All K-12 students are now eligible. Treasurer
  Larry Pack quoted. WV MetroNews. Partial-award deadlines run Sept. 15 (75%),
  Nov. 30 (50%) and Feb. 28, 2027 (25%) — those are the next hooks.
- **wvu-medicine-fulton** — 2026-08-09: new, ran as No. 5's second statewide
  brief. WVU Health System will acquire **Fulton County Medical Center**,
  McConnellsburg, Pa. — 21 critical-access beds, a 67-bed nursing home, 415+
  employees — investing up to **$17M over seven years**. LOI April 2026, close
  targeted **Jan. 1, 2027**. Follows the five Independence Health System
  hospitals. WV MetroNews. **Do not re-run before the close.**
- **meta-nm-child-safety** — 2026-08-09: ran as a U.S. brief. Judge Bryan
  Biedscheid ordered **$567M** into an abatement fund on top of March's $375M
  jury award (**$942M** total), plus New Mexico-only safeguards: 90-hour monthly
  cap for under-18s, hidden like counts by default, AI chatbot limits, stronger
  age verification, adult-messaging restrictions. **$420M** of the fund is for
  youth treatment. Meta will appeal and has no implementation deadline.
  PBS NewsHour. News again on the appeal or a second state copying the order.
- **graham-sanctions-act** — 2026-08-09: ran as a U.S. brief. Senate passed the
  Russia and Iran sanctions bill **86-11** on Aug. 7, named for the late Sen.
  Lindsey Graham (died July 2026). Sanctions top Russian officials, extends Iran
  sanctions, authorizes tariffs up to 100% on major buyers of Russian energy.
  **Must still clear the House**, where Speaker Johnson supports it and some
  Democrats object to the tariff authority. NPR. News again on a House vote.
- **jalapeno-salmonella** — 2026-08-09: ran as a U.S. brief. **345 sick as of
  Aug. 5 across 27+ states, 36 hospitalized**, Minnesota worst at 110; USDA FSIS
  public health alert Saturday naming 18 recalled products; peppers from
  Sinaloa, Mexico, via Coast Citrus. FSIS expects more downstream products.
  CBS News. **A rising count or a death makes it news again — re-check the
  number before citing it.**
- **wpbl-first-season** — 2026-08-09: ran as a Sports brief. The Women's
  Professional Baseball League debuted Saturday before a sold-out crowd at Robin
  Roberts Stadium, Springfield, Ill.; four clubs (NY Heights, LA Queens, Boston
  Hunters, SF Firebells); six-week inaugural season played centrally in
  Springfield; fifth women's pro league in US history. NPR.
- **chelsea-preseason** — 2026-08-09: ran as the football brief. **Chelsea 3-0
  AC Milan** in Jakarta, Aug. 8: Joao Pedro 45+2' (glancing home a Caicedo
  corner) and 46', Caicedo 50'. Read on AC Milan's own match report, which is
  where the minutes came from. Milan's last friendly is **Aug. 15 v Man United
  in Wroclaw**. **Premier League opens Aug. 21** — until then football is
  friendlies and transfers, and a quiet football day is expected.
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
- **wv-flood-aid** — 2026-08-08: **moved again and led the notebook.** FEMA
  approved **Individual Assistance for Ritchie and Pleasants** for the July
  storms (Auburn, in Ritchie, took the worst of it), announced by Morrisey on
  Friday — so two of the five pending counties are decided, and **Pleasants was
  the one this ledger was watching.** Separately FEMA **denied** IA and Hazard
  Mitigation for **Boone and Logan** for the **June 22-23** flooding; WVEMD has
  **30 days from Aug. 3** to submit more documentation and Morrisey is appealing.
  **Barbour, Doddridge and Harrison are still pending.** WV MetroNews. News again
  on any of those three, or on the Boone/Logan appeal outcome (~Sept. 2).
  Prior state, 2026-08-07: **ran as that day's first statewide brief.** Disaster Unemployment Assistance opened for **Lewis and Upshur**
  (the two counties that already had the $4.5M) covering job losses from the
  Jul. 21–22 storms, tornadoes, flooding, landslides and mudslides; claims file
  by **Oct. 2**, benefits payable to **Feb. 6, 2027**. West Virginia Watch.
  The other **five counties are still pending federal review**, Pleasants among
  them (three EF2 tornadoes, 5 homes destroyed, 13 badly damaged); Morrisey
  asked for seven in all. News again when any of the five is decided — that is
  the bigger story and it has not happened yet.
- **mecca-defence-pact** — 2026-08-08: today's lead. Saudi Arabia, Turkey and
  Pakistan signed the Makkah Joint Defense Agreement in Mecca on Aug. 7 — an
  armed attack on one is an attack on all. Signed by Mohammed bin Salman,
  Erdogan and Sharif; Pakistani army chief Asim Munir present. Saudi deputy
  minister Rayed Krimly said it is not a military axis, not sectarian, not tied
  to nuclear ambitions. Cross-checked on Al Jazeera, CBS and the OIC's own joint
  statement (`una-oic.org`), which is the primary text. Backdrop is the US-Israel
  war on Iran that opened **Feb. 28** and repeated strikes on Saudi territory.
  **No official Iranian government response yet — an Iranian MP dismissed it.**
  News again on a Tehran statement, a ratification, or a fourth state joining;
  the joint statement carries no accession clause, which is worth watching.
- **nucor-apple-grove-threat** — 2026-08-08: ran as a statewide brief. Written
  threat naming **Aug. 10**; Nucor closes the Apple Grove site that day; ~500
  employees plus several hundred contractors; FBI, State Police and Mason County
  sheriff investigating; sheriff's security for 10 days and a private firm hired.
  Site is commissioning systems now, production targeted for **2027**.
  WV MetroNews. **This is the crew's own corridor** — follow Monday.
- **blanche-confirmed-ag** — 2026-08-08: ran as a U.S. brief. Senate confirmed
  Todd Blanche **50-49** early Saturday; Collins and Murkowski the only
  Republican no votes, McConnell absent, Cassidy the deciding yes after a Friday
  floor speech. NPR. Note he appeared as *acting* AG in the Colombia inauguration
  delegation the same week. News again on his first major DOJ action.
- **july-jobs-report** — 2026-08-08: ran as a U.S. brief. Payrolls **-23,000**,
  unemployment **4.1%**, participation **61.4%**, May and June revised down a
  combined **103,000**, wages +3.2% year over year. BLS release read directly.
  Next print is the August report in early September; the Fed angle is the
  follow-up.
- **typhoon-dolphin** — 2026-08-08: ran as a World brief. Hit Okinawa Aug. 7 —
  five injured, 14,000 buildings without power, ANA and JAL regional flights
  cancelled. Landfall expected **late Sunday to early Monday** between Zhoushan
  (Zhejiang) and Fuding (Fujian); Zhejiang at top alert, 162 ferry routes
  suspended, Ningbo airport suspending Sunday flights; eastern Zhejiang could
  take **600 mm**. The Jakarta Post. **Landfall is Sunday — this is Monday's
  story with a real toll attached.**
- **colombia-de-la-espriella** — 2026-08-08: ran as a World brief. Abelardo de
  la Espriella inaugurated Aug. 7 in Cali (moved from Bogota), after a razor-thin
  June runoff over Ivan Cepeda; "mano dura" platform, hard line on
  narcotraffickers. Trump endorsed him; the US delegation included then-acting
  AG Todd Blanche. Outgoing president Petro alleged fraud without evidence.
  PBS NewsHour. News again on a first policy move or a US security agreement.
- **sudan-education** — 2026-08-08: ran as a World brief, distinct from
  `sudan-el-obeid`. UN Deputy Secretary-General Amina Mohammed told an informal
  Security Council session Friday that **8M+** children are out of school on the
  war's **1,210th** day; five of every six children in Darfur out of school;
  67+ attacks on schools and 154 instances of military use of schools since
  2024; more than half of teachers unpaid. Al Jazeera.
- **wvu-hall-of-fame-2026** — 2026-08-08: ran as a Sports brief. Seven named
  Friday — Beilein, Buchanan, Fowlkes, Holmes, Kasich, Lawrence, Turnbull.
  Beilein went 104-60 at WVU 2003-07. **Induction Oct. 10 before the Arizona
  game** — that is the next news, not before.
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

### 2026-08-12 — No. 8
- lead: midwest-primaries-2026 (the results; six states)
- us: water-system-cyberattacks, gilman-release, midwest-storm-outages
- world: colombia-earthquake (toll, disputed), zimbabwe-ferry, putin-shadow-fleet
- wv statewide: wv-storms-flooding, peia-finances
- wv regional: putnam_kanawha — kanawha-storm-death
- wv away: **vermont — vermont-primary. First away line since No. 1, ending a five-edition drought**
- sports: vikings-qb, nba-schedule-release
- scitech: ucsd-microglia, mosquito-species
- huntington_cabell: **no line** — the day's Cabell-Mason news was Point Pleasant street flooding, which is the
  statewide storm brief and would have been the same story twice in one section. The ACLU-WV suit against
  Huntington and Mayor Farrell over the **$2.1M** Flock contract surfaced in search but is **dated July 16**
  (petition for writ of mandamus, Cabell County Circuit Court, for resident Gregory Jimison, alleging meetings
  structured to dodge a quorum) — **old, and deliberately not run. Do not let it resurface as new tomorrow**
- mid_ohio_valley, nicholas_webster, summers_new_river: **no line** — searched; Parkersburg had a Grand Central
  Mall roof leak in the same storms and a 2023-fire civil case consolidation, Nicholas/Webster had the **same
  mobile screening unit** (Aug. 12-14) that has been standing there for a week, Summers/New River nothing
- **fishing: both waters, and the Williams turned over.** **767 cfs and rising, 3.42 ft**, against **61.5 cfs**
  24 hours earlier — a **12x** rise from Tuesday's storms, and the fetcher's own read is "blown out. Stay on the
  bank." That is the first blown-out reading of the run, after a week between 63 and 90 cfs
- **sumo: sat out, sixth day running.** Off-basho, full dedicated search. The only August items are the **Aug. 7**
  resignation of Izutsu Oyakata (former Akiseyama, 41) and Juryo promotions (Tanji, Tokifudo, Nabatame) — both
  carried **only by sumostats.com**, which this paper does not cite; the Japan Times has nothing newer than its
  **Aug. 5** jungyo feature; `tachiai.org` now **403s** this crawler, which is new. **Aug. 31 banzuke remains the
  hook.** Correct edition per Ian's rule
- **football: searched, nothing dated.** No matchweek; the season opens **Aug. 21**. Sky Sports' window page lists
  Chelsea (Henderson, Welbeck), Liverpool (Jacquet, Munoz, Araujo, and Salah released) and Tottenham (Tonali
  **£100m** club record, Fernandes, van Hecke) but **carries no dates**, and the Tonali deal traces to **July 6**.
  The validator's in-season warning fired and was cleared by search
- **stocking: silent no-op.** Nothing named the Williams, the Cranberry or the Summersville tailwater — and at 767
  cfs it would not have mattered
- **BUDGET, for tomorrow:** the validator projected **5,749** and the post shipped **5,963**, so it **split into
  two messages**. The projection does not count the `--page-url` content line or the second embed header.
  **Write to 5,600, not to the 5,800 hard ceiling, whenever a page url is being passed.**
- **Do not re-run tomorrow without movement:** the primary results (**November is the story now**); the water-system
  hacks (**a formal attribution is the news**); Gilman; the ferry; Putin's threat (**an actual seizure is the
  news**); the PEIA testimony; the Vermont statewide results. **Two exceptions that should run: what the eclipse
  actually looked like — it is TODAY at ~1:30 p.m. ET, after No. 8 posted, so it is No. 9's — and the Colombia
  toll, which is still moving. Also live: Hope Scholarship payments landed Aug. 13, the Peoples Cartage town hall
  is Aug. 13, and WV storms were forecast to continue.**

### 2026-08-11 — No. 7
- lead: colombia-earthquake
- us: vaccine-schedule-eo, noaa-july-record, midwest-primaries-2026
- world: assad-death-sentence, hormuz-reopening (Trump's counterclaim),
  zaporizhzhia-nk-missiles
- wv statewide: wv-overdose-decline, wv-child-fatality-report
- wv regional: huntington_cabell — wv-flock-plate-readers (the Huntington ordinances);
  nicholas_webster — nicholas-storm-outages
- wv away: **none, fifth straight edition** — Vermont's only fresh Bennington items were the
  three-way Democratic primary for the county Senate seat and a library whale feature, and
  **the primary was Aug. 11 itself**, so it is a scheduled event this morning and a result
  tomorrow; Prince George had nothing; Topsail was carried by its fishing line. **Vermont is
  the away desk's best hook in a week and it lands in No. 8**
- sports: bridgewater-retires, wvu-defense-rebuild
- scitech: eclipse-2026, saturn-cusp
- mid_ohio_valley, summers_new_river, putnam_kanawha: **no line** — searched; Parkersburg's
  freshest were Sunday I-77 crashes plus weekend items already a day old (Brewfest, the
  Lancaster Street sewer repair, a 7th Street warrant), Summers/New River had nothing, and
  Kanawha's candidates were a skatepark closure for the Fort Hill Bridge job and a log-cabin
  relocation — neither worth the slot when the notebook was already at budget
- **fishing: both waters.** Williams **90 cfs and rising, 1.58 ft**, up from 74.4 cfs a day
  earlier — the first rising reading of the run, after Monday's storms
- **sumo: sat out, fifth day running.** Off-basho, full dedicated search. The only August
  item with a real byline is **The Japan Times' Aug. 5 feature on the summer jungyo**
  (regional tour) — 28 event days in 27 locations, opening in Gifu Aug. 2, a single rest day
  **Aug. 17**, finishing in Sendai — and at six days old it is not a brief. Aki dates and the
  Aug. 31 banzuke are **still** carried only by travel and ticket-reseller sites. **Aug. 31
  remains the hook.** Correct edition per Ian's rule
- **football: searched, nothing.** No matchweek; the season opens **Aug. 21**. Chelsea's
  Palestra signing was early July and Henderson's is undated on the club's own page;
  Liverpool's Jacquet unveiling and Tottenham's Vuskovic sale to Brighton had no readable
  Aug. 10-11 report. The validator's in-season warning fired and was cleared by search
- **stocking: silent no-op.** WVDNR publishes no advance schedule and posts stockings only
  after the fact; nothing named the Williams, the Cranberry or the Summersville tailwater
- **Do not re-run tomorrow without movement:** the vaccine order itself (**the first lawsuit
  is the news**); the NOAA July figure; the Assad verdict (an extradition request is the
  news); Trump's counterclaim (Tehran's answer is the news); the Loyd testimony; the child
  fatality report; the Huntington ordinances (**Aug. 24 committee is the news**); the Nicholas
  outages; Bridgewater; the WVU defense. **Two exceptions that should run: the primary
  results, including Vermont, and what the eclipse actually looked like.**

### 2026-08-10 — No. 6
- lead: typhoon-dolphin (third day in the story, led on landfall and the
  150-year Shanghai rain record)
- us: interlochen-abuse-report, measles-35-year-high
- world: netanyahu-gaza-plan, nizhnekamsk-strike, copernicus-july-2026
- wv statewide: wv-flock-plate-readers, dohs-out-of-state-placements
- wv regional: putnam_kanawha — kanawha-water-mains
- wv away: **none, fourth straight edition** — Vermont's only Bennington item was
  the Aug. 8 library whale feature (already passed over once) and its primary is
  Aug. 11, which is a scheduled event and not news; Prince George had nothing
  (the 80-year-old who died evacuating is **Summerland, in the Okanagan**, not
  the north); Topsail's freshest items were Aug. 6-7 (Pender water-hookup
  refunds, a raid lawsuit) and it was carried by its fishing line
- sports: don-nelson-death, followed-clubs-final-friendlies, wafcon-2026
- scitech: voyager2-power, kimsuky-offline-ai
- huntington_cabell: **no line** — the Herald-Dispatch's Monday Huntington
  AI-camera/plate-reader ordinance would have duplicated the Flock statewide
  brief, and the rest of Cabell was Aug. 7 or older (VFD radios, CommuniCare
  groundbreaking). **The ordinance is Tuesday's line if the committee acted.**
- mid_ohio_valley, nicholas_webster, summers_new_river: **no line** — searched;
  Parkersburg's freshest was Aug. 7 (firemen's convention, a sewer collapse),
  Nicholas/Webster had the **same three forward-dated items for the fourth
  morning running** (Aug. 12-14 mobile screening, Aug. 23 checkpoint, Aug. 30 lake
  cleanup), Summers/New River had nothing newer than June
- **fishing: both waters.** Williams back after yesterday's USGS outage and
  **at the run's low, 63 cfs and falling, 1.4 ft, from 93.8 cfs a day earlier**
- **sumo: sat out, fourth day running.** Off-basho, full dedicated search. Only
  August items are the **Jul. 30** purse increase (spent by No. 2) and the
  **Jul. 27** Yokozuna Deliberation Council request to Onosato and Hoshoryu —
  both too old. Search text asserted Sept. 13-27 and an Aug. 31 banzuke but the
  carriers are still **sumostats/grandsumotournament/travel sites**, which this
  paper does not cite. **Aug. 31 remains the hook.** Correct edition per Ian's rule
- **stocking: silent no-op.** WVDNR publishes no advance schedule and August
  stockings are flow-dependent; nothing named the Williams, Cranberry or
  Summersville tailwater
- **Do not re-run tomorrow without movement:** the Interlochen report (a charging
  decision is the news); Bhattacharya's interview; the Netanyahu rejection (a US
  answer is the news); the Nizhnekamsk strike (a confirmed toll or refinery
  effect); the Copernicus July bulletin (August's lands early September); the
  Flock hearing (a Huntington council vote or a filed bill is the news); the DoHS
  testimony; Don Nelson; the two friendlies (**Aug. 21 opener is the news**);
  Voyager 2. **WAFCON is the exception — semifinals Aug. 12 and it should run.**

### 2026-08-09 — No. 5
- lead: hormuz-six-conditions
- us: graham-sanctions-act, meta-nm-child-safety, jalapeno-salmonella
- world: typhoon-dolphin, bc-wildfires, spain-italy-ceuta
- wv statewide: hope-scholarship-2026, wvu-medicine-fulton
- wv regional: putnam_kanawha — buffalo-crossing-collision
- wv away: **none** — Vermont's only fresh item was a library summer-reading
  feature (VTDigger, Aug. 8), Prince George had nothing, Topsail was carried by
  its fishing line. Third straight edition with an empty away desk
- sports: chelsea-preseason, wpbl-first-season
- scitech: hillsborough-meteorite, sun-microvortices, exercise-dose-heart
- huntington_cabell: **line written, sourced, opened, and cut for budget**
  (Milton water-line replacement, WCHS) — see `docs/FAILURES.md`. It was also
  the weakest thing in the notebook: an announcement about 2027, not an event
- mid_ohio_valley, nicholas_webster, summers_new_river: **no line** — searched;
  Parkersburg had festivals and a two-day-old SWAT warrant already cut once,
  Nicholas/Webster had the same forward-dated items as Friday (Aug. 23
  checkpoint, Aug. 30 lake cleanup), Summers/New River had nothing at all
- **fishing: Williams omitted, USGS 503.** Topsail only. First Williams omission
  of the run — see `docs/FAILURES.md`
- **sumo: sat out, third day running.** Off-basho, full dedicated search. The
  Aki dates are *still* carried only by travel and ticket-reseller sites; Japan
  Times' basho-schedule page now returns **402** and `sumo.or.jp/En/` shows a
  September banner with no dates on it. **Aug. 31 banzuke is the next real
  hook.** Correct edition per Ian's rule
- **Do not re-run tomorrow without movement:** the six conditions themselves (a
  US answer or a signed corridor deal is the news); the Senate sanctions vote
  (the House is the news); the Meta order (the appeal is the news); the Hope
  Scholarship approval (Aug. 13 payment day is the news); the WVU Medicine LOI
  (Jan. 1 close); the WPBL opening day; the Chelsea friendly. **Typhoon Dolphin
  is the exception — Monday has a real toll attached and it should run.**

### 2026-08-08 — No. 4
- lead: mecca-defence-pact
- us: blanche-confirmed-ag, july-jobs-report, ice-bodycam-policy
- world: typhoon-dolphin, colombia-de-la-espriella, sudan-education
- wv statewide: wv-flood-aid (FEMA: Ritchie/Pleasants in, Boone/Logan denied),
  nucor-apple-grove-threat
- wv regional: putnam_kanawha — kanawha-deputy-federal-custody
- wv away: **none** — Vermont had a live candidate (three Democrats running for
  the Bennington County sheriff's seat, Brattleboro Reformer, Aug. 7) that was
  **not opened**, so it did not run; Prince George had nothing; Topsail carried
  by its fishing line
- sports: wvu-hall-of-fame-2026, chelsea-milan-jakarta
- scitech: ucla-phonon-focusing, sunlight-entanglement, teen-cannabis-cognition
- huntington_cabell: **no line** — the day's corridor story (Nucor at Apple
  Grove) ran as a statewide brief, and the only other candidate 403'd
- mid_ohio_valley: **line written, sourced, and cut for budget** (Parkersburg
  SWAT warrant, WTAP) — see `docs/FAILURES.md`
- nicholas_webster, summers_new_river: **no line** — searched, nothing but
  forward-dated events (an Aug. 23 DUI checkpoint, an Aug. 30 lake cleanup, a
  mobile screening unit). Standing events are not news; correct outcome
- **sumo: sat out, second day running.** Off-basho, dedicated search run. The
  Aug. 8 Aki ticket on-sale date **arrived today and is still spent** — No. 2
  printed it and it must not be re-run. Correct edition per Ian's rule
- **Do not re-run tomorrow without movement:** the pact signing itself (a Tehran
  response or a ratification is the news); the Blanche vote; the July jobs print;
  the Hall of Fame class (Oct. 10 is the news); the Chelsea-Milan friendly, whose
  **result was not knowable at press time — kickoff was 7 a.m. ET, and a Sunday
  brief should carry the score, not the fixture**

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
- **2026-08-08** — No. 4. Validator projected **6,603** on the first pass, the
  worst overshoot yet, and the paper still shipped a full 3-brief U.S. and World
  at **5,775** — the cost was one sourced notebook line and a lot of tightening.
  Three things for the next shift:

  **1. The foreground-post failure repeated, and the real cause was the clock,
  not the runner.** `post_discord.py` was launched in the foreground again and
  killed mid-hold. But the reason it was launched that way is that this desk had
  drifted into believing it was past 7:00 — elapsed research *felt* like 75
  minutes when it was 23. Between 6:02 and 6:25 the clock was never re-read.
  Yesterday's ledger says both halves of this ("run it detached", "read the
  clock, do not feel it") and both were still got wrong. **`index.json` caught it
  a second time.** That gate is now the only thing standing between this mistake
  and a lost paper; treat `TZ=America/New_York date` as mandatory before any
  decision that depends on the hour.

  **2. Poll-Pages-before-posting worked again and should stay the default.** The
  permalink was 404 twice and went **200 about 25 seconds after the push**, so
  `--page-url` shipped in the original message and `--backfill-link` was not
  needed. Second edition running to do it that way.

  **3. The lead was a genuinely multi-sourced foreign story and the primary text
  was reachable.** Al Jazeera and CBS both opened, and the OIC's own joint
  statement at `una-oic.org` carried the operative clause verbatim — better than
  either. **When a summit produces a communique, look for the issuing body's own
  English page before settling for wire paraphrase.** Reuters/AP/BBC/Guardian
  were never needed and are still blocked.

  **4. The paper split into two messages and the validator did not see it
  coming.** Projected 5,795, sent **6,009** — a 214-char gap the projection does
  not model, on a run that passed `--page-url`. Four rounds of tightening were
  spent chasing a ceiling that was already 200 chars too generous. Until someone
  measures where the delta comes from, **budget to ~5,550 projected when the
  permalink ships in the original post.** See `docs/FAILURES.md`.

  Also noted: `wowktv.com` 403'd (new; WSAZ and MetroNews both fine today), and
  the sci/tech section ran three university/journal releases read via
  ScienceDaily's reproductions — `source` names the institution that did the
  work, which is what the facts trace to.
- **2026-08-09** — No. 5 posted at **07:00:05 ET**, one message, **5,636** embed
  chars, hero attached, permalink in the original post, `degraded: []`. Four
  things for the next shift:

  **1. The +214 budget mystery is smaller than it looked: today it was +107.**
  Validator projected **5,529**, `post_discord.py` sent **5,636**, both with
  `--page-url`. Yesterday the same pair was 5,795 → 6,009 (+214). So the delta
  is **not a constant**, and treating 214 as one is what cost No. 4 four rounds
  of pointless tightening. Two data points say it scales with something —
  probably per-embed chrome, since No. 4 carried more notebook lines. Working
  rule until someone diffs the payloads properly: **budget to ~5,550 projected
  and expect roughly +2% at send.** Today that landed a comfortable single
  message with 164 chars of headroom.

  **2. Launching the post detached worked the first time, and the clock was
  read five times.** No repeat of the No. 3/No. 4 foreground-timeout failure.
  The hold reported "waited 34 min to post at 07:00 ET" and delivered on the
  second. `TZ=America/New_York date` was run before every decision that
  depended on the hour — and it mattered, because at 6:22 this desk again *felt*
  later than it was. **Read the clock; do not feel it.** Third edition running
  where that sentence is the lesson.

  **3. Re-read every brief against its fetched source while the hold sleeps.**
  Three snippet-derived clauses were caught that way today, one day after the
  same class of error was caught the same way (`docs/FAILURES.md`). The hold is
  ~35 minutes of free time and this is the highest-value thing to spend it on.
  It cost two kill-and-relaunch cycles of the held post, which is cheap and
  safe: nothing had posted, `index.json` was empty both times, and the payload
  is frozen when the process starts — **so editing the JSON after launch does
  nothing; you must relaunch.**

  **4. Poll-Pages-before-posting is now 3-for-3.** The permalink went 200 about
  **10 seconds** after the push, so `--page-url` shipped in the original message
  and `--backfill-link` was never needed. Keep it the default.
  Also noted: `westvirginiawatch.com` **403'd** (new — it opened fine on Aug. 7);
  `herald-dispatch.com` returned **429** on its recent-news index; `seti.org` and
  `japantimes.co.jp` both refused (403/402), so the meteorite and sun briefs were
  read via ScienceDaily's reproductions with `source` naming the institution that
  did the work, same as No. 4. Both WV statewide briefs came from **WV MetroNews**
  — acceptable at two, but a third would have broken the three-bylines rule, and
  no other WV outlet had a statewide story worth the slot on a Saturday.
- **2026-08-10** — No. 6 posted at **07:00:08 ET**, one message, **5,578** embed
  chars, hero attached, permalink in the original post, `degraded: []`. (The
  ledger body below was committed at 06:33 while the post was still holding, with
  a delivery-pending marker; this line replaced it once `index.json` recorded
  `posted: true`, message **1536328261359894674**. Committing the ledger before
  delivery is a deviation from §10 — done only because a clean working tree was
  required at that moment — and the marker was the safeguard. Prefer the §10
  order when nothing forces the issue.) Five things for the next shift:

  **1. The first draft projected 7,206 against a 5,800 ceiling — the worst
  overshoot of the run — and the fix cost three sourced briefs.** 15 briefs plus
  a three-paragraph lead has never fit and the arithmetic was knowable *before*
  drafting. The ladder in §5 also could not help the way it is written: it says
  notebook lines go before wire briefs, but the notebook was already down to
  **one regional line and no away line**, so every rung available was a wire
  brief. **Decide the shape first — about 12 briefs when the notebook is lean —
  and write to it.** Landed at 5,471 projected. The lead going from three
  paragraphs to two is free under the contract and should be the first move, not
  the last.

  **2. The hold re-read caught something for the third consecutive morning.**
  Two WV briefs had drifted from their fetched text: an invented plural
  ("finance committees" for the Joint Standing Committee on Finance) and a
  paraphrase that moved a delegate's "concerns" to "questions." Milder than
  Aug. 8's and Aug. 9's inventions, but the same surface and the same catch.
  **Treat the re-read as a required step of the run, not a use of spare time.**
  One kill-and-relaunch, `index.json` verified empty first.

  **3. Poll-Pages-before-posting is 4-for-4, and today it was the fastest yet:
  200 on the first attempt, roughly one minute after the push.** The permalink
  shipped in the original message and `--backfill-link` was not needed. Content
  was verified, not just the status code — a 200 on a stale cache would look
  identical.

  **4. Read the clock, do not feel it — fourth morning this is the lesson, and
  the first where it was worth real money.** At what felt like 6:38 it was
  actually 6:16, so there was time to install `cairosvg` and **rasterise the
  drawing to look at it before shipping**, which no previous run has done. That
  is now cheap and repeatable: `currentColor` and `var(--parchment, …)` have to
  be substituted for literals first or CairoSVG throws on the `var()`.

  **5. The projection-to-send delta is +107 for the second morning running, and
  the No. 4 outlier is explained.** No. 5: 5,529 → 5,636. No. 6: **5,471 →
  5,578.** Both **exactly +107**, both one message, both with `--page-url`.
  No. 4's +214 is 2 × 107 — and No. 4 **split into two messages**. So the delta
  is not mysterious and not proportional to notebook size as No. 5's note
  guessed: it looks like a **fixed ~107 chars of per-message chrome**. Working
  rule for the next shift: **projected + 107 × (expected messages)**, so a
  single-message paper can safely be budgeted to about **5,690 projected**
  rather than the cautious 5,550 that has been used for three days. That is
  ~140 chars of headroom recovered, which is most of a notebook line. Confirm it
  once more before relying on it; three points is not a law.

  Also noted: two sections ran on two outlets rather than three (World was PBS,
  Euronews and **Copernicus's own bulletin page** — going to the primary for the
  climate story was what got a third byline in, and it is the better source
  anyway); `thisisanfield.com` **403'd** and `espn.com/soccer/match` returned
  empty markdown twice, so Sky Sports carried both friendlies; `wvpublic.org/news`
  served content two months stale and is not usable as a front page right now.
- **2026-08-11** — No. 7 posted at **07:00:08 ET**, one message, **5,728** embed chars, hero
  attached, permalink in the original post, `degraded: []`, message
  **1536690648453873750**. The hold reported "waited 33 min to post at 07:00 ET."
  *(The body below was committed at 06:32 while the post was still holding, with a
  delivery-pending marker, because a stop hook required a clean working tree — the same
  deviation from §10 that No. 6 recorded, and the marker was again the safeguard. Prefer the
  §10 order when nothing forces the issue.)* Seven things for the next shift:

  **1. THE CLONE CAME UP IN DETACHED HEAD, AND `git push -u origin main` FAILED IN A WAY THAT
  LOOKED LIKE A STALE REMOTE.** `git pull` in step 1 errored with "specify which branch";
  `git pull --rebase origin main` then said "Already up to date" and everything looked fine.
  It was not: `HEAD` was detached at `origin/main` and the local `main` branch still pointed
  at **71d0c7d, 25 commits behind**. So the commit landed on a detached HEAD, and the push
  tried to send the *stale branch* and was rejected as non-fast-forward. Two `git pull
  --rebase` attempts did nothing because the rebase target was already current. The fix is
  three seconds once you see it: `git branch -f main HEAD && git checkout main && git push -u
  origin main`. **Run `git status -sb` as part of step 1, before anything else** — "## HEAD
  (no branch)" is the whole diagnosis, and a non-fast-forward at 6:20 with a paper to ship is
  exactly when this is most expensive to work out from first principles.

  **2. The first draft projected 6,201 against a 5,600 target — and the notebook was not the
  problem.** Twelve briefs, a two-paragraph lead, a lean notebook (2 statewide, 2 regional,
  no away, 2 fishing): the shape was right and it still ran 600 over, because **the summaries
  were written at 150-190 characters instead of 110-130**. Tightening all fifteen of them,
  cutting nothing, took it to **5,581** with no brief lost. No. 6's lesson was "decide the
  shape first"; this morning's is the other half — **the shape being right does not save you
  if the prose is written to the cap.** Write the summary at 120 on the first pass.

  **3. The hold re-read caught three real sourcing errors on its fourth consecutive morning,
  and one of them was in a HEADLINE, which is a new surface.** (a) The lead U.S. headline read
  "Trump orders childhood vaccine list cut to 11" while the cited CBS piece **never carries a
  number** — the 11 came from NPR and NBC, which themselves disagree on the old figure (17 v
  18). A headline sourced to an article that does not support it is the same defect as an
  invented summary and is easier to miss, because the re-read instinct is to check summaries.
  Rewritten to "Trump orders fewer recommended childhood vaccines," which the CBS piece does
  support. (b) The lead dek said "Cali and Pereira imposed curfews" — taken from a **Euronews
  headline** on the index page, never opened. Opening the body confirmed **Cali only**. (c) A
  Wisconsin summary said Hong "leads the Wisconsin governor field" when she leads only the
  **Democratic** field. Also a milder antecedent slip that hung the 2.5x overdose rate on
  neonatal abstinence syndrome. **Check headlines and deks against the cited article, not
  just summaries.**

  **4. Four disputed numbers were dropped or downgraded in one edition — the most yet — and
  the rule held every time.** Injured in Colombia: **570** (Al Jazeera, Euronews) v **700**
  (NBC), so the twice-supported figure ran. Missing: **188** (NBC) v **1,400+** (Al Jazeera),
  dropped entirely. Quake depth: **107 km** v **110 km**, dropped. Vaccines cut from **17**
  or **18**, dropped and the headline rewritten. None of the four cost the reader anything;
  all four were tempting.

  **5. Poll-Pages-before-posting is 5-for-5, and this was the fastest yet: 200 on the first
  attempt, about four seconds after the push.** Content was verified, not just the status
  code — the headline and "No. 7" were both grepped out of the served HTML. The permalink
  shipped in the original message; `--backfill-link` was not needed.

  **6. Rasterising the drawing before shipping is now worth doing twice.** First pass: the
  tide flats read as two rounded hills and the channel stopped in mid-water. Flattening the
  flats' profiles into shallow scalloped sheets, running the channel all the way to the
  horizon, moving the marker piling onto the channel lip and deleting two oyster clumps that
  came out as eggs fixed it, in about six minutes. `pip install cairosvg`, substitute
  `currentColor` and the `var(--parchment, …)` for literals, render, look. **The subject was
  rung 3 but a new one — Topsail Sound at the afternoon low of -0.2 ft**, drawn from the
  fetcher's own tide table, chosen over a fourth Williams River so the standing subject does
  not become wallpaper. The other sound/river readings are still there for future mornings.

  **7. The +107 rule is now four for four, and it is safe to rely on.** Projected **5,621**,
  sent **5,728** — exactly **+107** again, one message, `--page-url` in the original post.
  No. 5: 5,529 → 5,636. No. 6: 5,471 → 5,578. No. 4, which split, was 5,795 → 6,009, or
  2 × 107. **It is fixed per-message chrome, not proportional to anything.** No. 6 asked for
  one more data point before trusting it; this is that point. **Budget a single-message paper
  to about 5,690 projected** and stop tightening below that — three of the last four mornings
  spent rounds of prose-trimming buying headroom that was never needed. Today's 5,621 left
  72 chars of the ceiling unused, which is most of an away line.

  Also noted: `westvirginiawatch.com` **403'd** again (third morning running);
  `science.nasa.gov`'s eclipse page **404'd**, `esa.int` **403'd**, `nature.com` redirects to
  an auth wall, `espn.com` returned **empty markdown** for both the latest-news index and a
  story page, and `wvusports.com/news` **404'd** — so ESPN and the university's own site are
  both currently unusable and CBS Sports carried the NFL brief. `wsaz.com`, `wvmetronews.com`,
  `euronews.com`, `aljazeera.com`, `npr.org`, `pbs.org`, `cbsnews.com`, `cbssports.com` and
  `sciencedaily.com` all opened cleanly. U.S. ran on two outlets rather than three (NPR twice,
  PBS once) and World likewise (Euronews twice, Al Jazeera once); acceptable at two, but both
  sections were one byline short of the standard.
