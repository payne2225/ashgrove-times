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
| Open-ended | **Pages build lag exceeds any sane pre-post poll.** 2026-08-06: `editions/2026-08-06.html` 404'd for the full 120s window so the link was omitted; it returned 200 about 9 minutes after the push (measured build **8m38s**, versus 23s the evening before). Pages is healthy — this is Actions queue lag, not an outage, so do **not** set `PAGES_ENABLED = False`. **RESOLVED 2026-08-06:** the paper no longer waits on it. `python post_discord.py --date YYYY-MM-DD --backfill-link` posts nothing, waits out the build (up to 15 min), and edits the permalink into the message already sent; `instructions/edition.md` §9.5 makes that step 9.5 whenever step 8 times out. It edits content only, never embeds, so it can never trim a published brief. No. 2 was backfilled by hand and now carries its link | **CLOSED** || Open-ended | **Launch `post_discord.py` in the background, and read the clock rather than estimating it.** Logged as a failure twice now, **2026-08-13 and 2026-08-14**, in identical form: the post was started in the foreground, `--not-before 07:00` slept, and the shell killed the command at its own timeout. Nothing posted either morning and `editions/index.json` proved it, so the cost is wasted minutes and a scare, not a lost paper. The companion error both mornings was believing the run was late — 6:23 ET read as 7:38 on the 13th, 6:29 ET read as 7:30 on the 14th. **The hold can sleep the better part of an hour, which is longer than a foreground command may live.** Neither paper was late | **OPEN — third occurrence would mean this row is not being read. 2026-08-15: launched in the background on the first attempt and the clock was read, not estimated — the row is being read** |
| Open-ended | **THE `--sportsman` PIPELINE DOES NOT EXIST, AND IT BLOCKS THE SECOND PAPER.** `instructions/routine.md` and `instructions/sportsman.md` both document `validate_edition.py --sportsman`, `render_edition.py --sportsman` and `post_discord.py --sportsman`. `grep -ci sportsman` returns **0** in all three scripts. `config.py` has all 16 sportsman definitions, `fetch_fishing.py` already reports all four sportsman waters, both reference files are transcribed and `editions/sportsman/index.json` exists — commit `ca5293d` shipped everything *except* the pipeline. No branch, no PR. **2026-08-15: the first edition was researched and written to `editions/sportsman/2026-08-15.json` and could not be validated, rendered or posted.** Building the pipeline is a code change for Nate, not something the morning routine should improvise at 5:30 a.m.; hand-building a payload is forbidden by `instructions/edition.md` and was refused. **RESOLVED 2026-08-16.** The flag landed. `grep -ci sportsman` now returns **11 in `validate_edition.py`, 21 in `render_edition.py`, 32 in `post_discord.py`**, and No. 1 posted on **2026-08-15** (message `1538220774954115096`, link backfilled). No. 2 validated clean on the first pass, rendered, and posted today. The edition JSON written on the 15th shipped as promised | **CLOSED** |


| 2026-08-15 | **Sports retired from the Times.** Nate's call once Sports & Sportsman shipped. Wire sections (U.S., World, Sci/Tech) now target FOUR briefs; sumo and the Premier League rules moved to `instructions/sportsman.md`. The archive keeps its shape via `config.RETIRED_SECTIONS` — do not add a sports section to any Times edition dated 2026-08-16 or later | **CLOSED** |
| Open-ended | **The routine's stored prompt says Sports & Sportsman is on its first edition, and it is not.** The 2026-08-16 prompt read "THIS IS SPORTS & SPORTSMAN'S FIRST EDITION. It is Vol. I, No. 1 of that paper" — but it also said to **number it from its own ledger**, and `editions/sportsman/index.json` already carried **No. 1, posted 2026-08-15**, message `1538220774954115096`. `config.next_edition_number()` returned **2** and **2 is what shipped**, per `instructions/edition.md`'s "compute it, never guess it." The prompt was evidently written before the 15th's run succeeded and has not been updated. **Harmless this once because the ledger is authoritative and the instruction to use it was explicit — but a prompt that hard-codes an edition number will eventually contradict the ledger in the dangerous direction. Worth Nate editing the stored prompt** | **OPEN — for Nate** |
| Open-ended | **Head start is now 90 minutes and the clock was read, not estimated.** `config.head_start_minutes('2026-08-16')` returns **90** and `config.cron_for()` returns `30 9 * * *`, which is the cron actually installed — the 5:30 ET wake for two papers. Neither daylight-saving row below has come due. **Noted because the desk again caught itself estimating the time rather than reading it** (mid-run it believed it was 6:45 ET when `TZ=America/New_York date` said **5:43**), the same error logged on 2026-08-13 and 2026-08-14. The fix that worked was running `date` before every scheduling decision instead of counting tool calls | **OPEN — read the clock, do not estimate it** |

| Open-ended | **The stored prompt still says Sports & Sportsman is on its first edition. Third morning running.** The 2026-08-17 prompt again read "THIS IS SPORTS & SPORTSMAN'S FIRST EDITION. It is Vol. I, No. 1 of that paper," and again also said to **number it from its own ledger**. `editions/sportsman/index.json` carried **No. 1 (Aug. 15)** and **No. 2 (Aug. 16)**, both posted, so **No. 3 is what shipped**, per "compute it, never guess it." Harmless a second time for the same reason as the first — the ledger is authoritative and the instruction to use it is explicit — but the row was already flagged on 2026-08-16 as something for Nate to edit and it has not been edited. **The prompt also asks for "the extra care a first issue deserves," which is now advice attached to the wrong edition** | **OPEN — for Nate, second reminder** |
| Open-ended | **The four-brief wire target and `config.EMBED_BUDGET` cannot both be satisfied.** No. 13 projected **5,906** against the 5,800 ceiling *after* every summary was cut to the low end of target and *after* a real wire brief was dropped, and it still split into two messages — the third split in six editions (Nos. 8, 12, 13). U.S. and Sci/Tech each project ~1,200 against a **1,000** allocation with four briefs, because a brief costs its whole URL and `sciencedaily.com` and `pbs.org` links run 60-110 chars each. **This is arithmetic, not discipline: either the wire target goes back to three, or the per-section allocations go up, or splitting stops being logged as degraded and becomes the normal shape.** A code and config decision for Nate | **OPEN — for Nate** |
| Open-ended | **The clock was read, not estimated — but only after 40 minutes of estimating it.** `config.head_start_minutes('2026-08-17')` returned **90** and `config.cron_for()` returned `30 9 * * *`, the cron actually installed; neither daylight-saving row has come due. **Noted because the desk again drifted into estimating: mid-research it believed it was 6:25 ET when `TZ=America/New_York date` said 5:39** — the same error logged on 2026-08-13, 08-14 and 08-16. The drift was always in the same direction, believing the run later than it was, which is the direction that makes a desk cut research short. **The fix that works is running `date` before every scheduling judgment, not counting tool calls** | **OPEN — read the clock, do not estimate it** |

| Open-ended | **The stored prompt still says Sports & Sportsman is on its first edition. Fourth morning.** The 2026-08-21 prompt again read "THIS IS SPORTS & SPORTSMAN'S FIRST EDITION. It is Vol. I, No. 1 of that paper," and again also said to **number it from its own ledger**. `editions/sportsman/index.json` carried **Nos. 1 through 6, all posted** (Aug. 15-20), so **No. 7 is what shipped**, per "compute it, never guess it." Flagged on 2026-08-16 and again on 2026-08-17 and it has not been edited. The prompt's "take the extra care a first issue deserves" is now four days of advice attached to the wrong edition. **OPEN — for Nate, third reminder** |
| Open-ended | **Head start was 90 and the clock was read, not estimated — cleanly this time.** `config.head_start_minutes('2026-08-21')` returned **90** and `config.cron_for()` returned `30 9 * * *`, the cron actually installed. Neither daylight-saving row has come due. **`TZ=America/New_York date` was run before every scheduling decision and there was no drift in either direction**, which breaks the run of estimation errors logged on 2026-08-13, 08-14, 08-16 and 08-17. The whole run — both papers researched, written, validated, rendered, committed and pushed — finished at **5:52 a.m. ET, 22 minutes after the 5:30 wake**, leaving 68 minutes of hold. **The head start is not the constraint it was; if anything it is now generous** |

## 2. Forward-dated events

| Date | Event | Note |
|---|---|---|
| **2026-11-03** | **General-election matchups set by Tuesday's primaries** | Minnesota Senate: **Peggy Flanagan (D) v Michele Tafoya (R)**. Minnesota governor: **Amy Klobuchar (D) v Lisa Demuth (R)**. Wisconsin governor: **David Crowley (D) v Tom Tiffany (R)**. Connecticut 1st: **Luke Bronin (D)**. NPR. Ran as No. 8's lead; do not re-run the primary results, the news now is the campaigns |
| **date not established** | **South Carolina Republican Senate runoff** | Sen. **Darline Graham** (Trump-endorsed) finished first with about a third of the vote and advanced against Rep. **Ralph Norman**; NPR notes two thirds of Republicans voted for Norman or Rep. Russell Fry. **The runoff date was not in the piece the paper opened — find and record it before covering** |
| 2026-10-20 | **NBA season opens** | Knicks raise their first banner since 1973 against Philadelphia; Thunder at Spurs; Celtics-Pistons. Knicks-Spurs Finals rematch **Dec. 25**, NBA Cup final **Dec. 11**. CBS Sports. Ran as No. 8's second Sports brief; spent until the season actually starts |
| 2026-08-08 | **Aki basho tickets go on sale** | Confirmed on the JSA's own English page (`sumo.or.jp/En/`) and printed as No. 2's sumo brief. Do not re-run this fact; it is spent |
| 2026-08-08 | Chelsea play AC Milan in Jakarta | Preseason friendly. A followed club, so it is a legitimate football brief if anything happens in it |
| **2026-08-10** | **Nucor Apple Grove site reopens (or does not) after the threat closure** | The mill site closes Monday over a written threat naming that date; FBI, State Police and the Mason County sheriff investigating, sheriff's security posted 10 days. WV MetroNews. A reopening, an arrest, or a second closure is a `huntington_cabell` line or a statewide brief. **2026-08-10: the date arrived and nothing new was reported.** Searched at 6 a.m. ET across MetroNews, WSAZ, Herald-Dispatch, WCHS and the Gazette-Mail; every result was still the Aug. 7 closure announcement, so it was **deliberately not re-run** — the closure taking effect is the same fact No. 4 already printed. The paper posts before the work day, so any Monday development lands in **Tuesday's** edition. **Row stays open:** watch for an arrest, a reopening, a second closure, or the sheriff's 10-day detail ending about **Aug. 17**. **2026-08-11: searched again; the only new line anywhere is that no incident was reported as of Monday afternoon**, carried inside the same Aug. 7 closure stories. Not a brief. The mill is a **$4B** project testing equipment now, with production ramping through 2027-28. **2026-08-13: nothing on MetroNews' or WSAZ's news indexes for Aug. 12-13 mentions Nucor or Apple Grove.** The sheriff's 10-day detail should be ending about **Aug. 17** — that is the next thing to check |
| **2026-08-12** | **Total solar eclipse over Greenland, Iceland, northern Spain and a corner of Portugal** | Ran as No. 7's first Sci/Tech brief on the eve. The shadow enters Galicia about 19:27 and leaves the Balearics about 20:35; totality nowhere exceeds 1 minute 48 seconds; first in mainland Spain since **April 15, 1912** and first in mainland Europe since 1999. Euronews. **The follow-up is what was actually seen** — cloud, crowds, the ESA and NASA observations. **2026-08-12: it could NOT run in No. 8 and the previous ledger line was wrong to promise it.** Totality reaches Galicia about 19:27 local, roughly **1:30 p.m. ET** — six hours after this paper posts. A 7 a.m. ET edition can never carry a same-day European afternoon event. **It belongs in No. 9 (Aug. 13)**, and Euronews' Aug. 12 preview (eyewear shortages, corona observations from Spain and Iceland) was deliberately not re-run as a second preview. Spain's next two are **Aug. 2, 2027** and **Jan. 26, 2028** |
| **2026-08-24** | **Huntington Public Safety Committee takes up both Flock ordinances** | Mayor Patrick Farrell's ordinance (data access, retention, audits, criminal penalties) and Councilwoman Tia Rumbaugh's graduated-penalty ordinance were introduced Monday Aug. 10 and referred to committee. City Attorney Scott Damron says **no contract has been signed**; the original Sept. 1 implementation date is now uncertain. WSAZ, WV MetroNews. Ran as No. 7's `huntington_cabell` line |
| 2026-08-12 | **WAFCON semifinals** | Malawi v Algeria in Casablanca, Morocco v Cameroon in Rabat. All four have already qualified for the 2027 World Cup in Brazil. Al Jazeera. Ran as No. 6's third Sports brief; the semifinals are the follow-up, and the final is the week after. **2026-08-13: played, and ran as No. 9's first Sports brief — Malawi 3-1 Algeria, Cameroon past Morocco on penalties. Spent** |
| **2026-08-16** | **WAFCON final: Malawi v Cameroon** | Sunday. Malawi are ranked 153rd and in their first WAFCON; Cameroon knocked out 10-time champions Nigeria in the quarterfinals. Al Jazeera. **This is Monday's Sports brief** |
| 2026-08-13 | **Peoples Cartage town hall, Parkersburg** | Independent testing results from the warehouse fire. WTAP. A `mid_ohio_valley` line that night or the morning after. **2026-08-13: the testing results came out the evening before the town hall and ran as No. 9's `mid_ohio_valley` line** (WVDA/WVDEP: nothing above federal action levels, some samples above state screening thresholds). **The town hall itself is still tonight — anything said there is tomorrow's line, and the results themselves are spent** |
| 2026-08-21 | **Premier League 2026-27 opens** | Confirmed via ESPN's fixtures piece. Until then the football beat is transfers and friendlies only, and a quiet football day is the expected outcome, not a failure |
| **2026-08-31** | **Aki banzuke (rankings) released** | The next genuine sumo news after the ticket date, and the natural moment the Aki dates get confirmed by a citable outlet. Do not print it before it happens |
| 2026-09-10 | WV charter board bylaws vote | Postponed from Aug. 6. WV MetroNews. Small, but it is the follow-up to today's statewide brief |
| 2026-10-02 | DUA filing deadline, Lewis and Upshur | Claims close; benefits run to Feb. 6, 2027. West Virginia Watch |
| 2026-08-13 | **Hope Scholarship first payments** | $5,435.62 each to 25,000+ students, two days ahead of schedule. WV MetroNews. Ran as No. 5's first statewide brief; the news on the day is whether the money actually lands. **2026-08-13: deliberately not re-run.** Searched at 6 a.m. ET; the only thing carrying today's date is the same **Aug. 8** announcement No. 5 already printed, and a 7 a.m. paper cannot report whether deposits landed. **A problem with the payments would be a brief; a clean deposit is not. Row closes unless something breaks** |
| 2026-08-15 | Italy's Schengen suspension with Spain runs to at least this date | Rome said it expects another crossing attempt. Spain's counter-controls run to Sept. 7. Euronews |
| ~2026-09-02 | **FEMA appeal window closes on the Boone/Logan denial** | WVEMD had 30 days from Aug. 3 to file more documentation; Morrisey is appealing. WV MetroNews |
| 2026-09-07 | Spain's border controls on Italian travellers expire | Euronews |
| 2027-01-01 | **WVU Medicine/Fulton County Medical Center closing** | Non-binding LOI signed April 2026; needs regulatory approval. WV MetroNews. Ran as No. 5's second statewide brief — do not re-run before the close |
| 2026-09-13 → 2026-09-27 | **Aki basho (Tokyo)** — *derived, still unconfirmed* | Second-Sunday estimate from `config.basho_window(2026, 9)`. 2026-08-06: the only sources carrying Sept. 13–27 at Ryogoku Kokugikan were ticket-reseller and travel sites, which this paper does not cite. **2026-08-07 and 2026-08-09: searched again, same result both mornings** — travel and ticket-reseller sites only, and `sumo.or.jp/EnHonbashoTopics/banzuke_topics/` now returns a Japanese URL-error page rather than banzuke content. Try Kyodo, Japan Times or NHK at the **Aug. 31 banzuke release**, which is when a citable outlet will have to print the dates. Confirm before covering. During a basho, sumo usually wins the Sports lead |
| 2026-11-08 → 2026-11-22 | **Kyushu basho (Fukuoka)** — *derived, unconfirmed* | Same derivation. Note it opens the week after the cron switch above || **2026-08-15** | **Greenbrier refinancing target close; casino closure follows** | The Justice family told U.S. District Court it will shut the casino and lay off about **90** people so a **$500M** Kennedy Lewis Investment Management loan can close, retiring roughly **$300M** in first-lien debt and handing KLIM **51%** control; delay was costing about **$145,000 a day** in interest. The **Lottery Commission** put Greenbrier Hotel Corp. on **financial watch June 30** and has not cleared the ownership change; acting director **David Bradley** called the closure threat, made without notice, "deeply concerning." Conference call **Aug. 19**, regular meeting **Aug. 26**. Note the two readable outlets disagree on the filing day (MetroNews Thursday, Herald-Dispatch "late-night Wednesday") and on whether the Volk deadline is Friday the 14th or the 15th, **so no filing date and no closing date were printed.** WV MetroNews, The Herald-Dispatch. Ran as No. 10's second statewide brief. **An actual closure, a layoff notice, or a Lottery vote is the news** |
| **~2026-08-28** | **Scott Smith returns to Parkersburg for a second round of testing** | The independent tester told Thursday's town hall he would be back **in two weeks** and would keep testing until no further contaminants turn up. WTAP. A `mid_ohio_valley` line when he reports |
| **2026-08-18 → 2026-08-21** | **Nick Joe Rahall II Bridge nightly closures, Huntington to South Point** | 10 p.m. to 5 a.m., both directions, annual routine in-service safety inspection; the story named no inspecting agency and no detour. The Herald-Dispatch. **Written, opened and sourced as the `huntington_cabell` line and cut for budget** (`docs/FAILURES.md`). It is a scheduled routine inspection, so it is only a line at all on a thin Cabell morning — do not resurface it as fresh news after Aug. 21 |
| **Nov-Dec 2026** | **FIFA intercontinental playoffs for the 2027 Women's World Cup** | South Africa and Ghana carry Africa's two places into them, against teams from Asia, Oceania and South America. Al Jazeera. Ran in No. 10's Sports |


| **2026-08-16** | **Marshall host Ohio, and both are followed teams** | Women's soccer, 7 p.m. at Hoops Family Field. Marshall opened 3-1 over Morehead State; Ohio is the other side. Marshall Athletics. Ran in Sports & Sportsman No. 1 — **this is the sportsman paper's version of a house derby and it was written straight down the middle.** The result is Monday's line |
| **2026-08-17** | **Wood County Commission votes on the Lubeck PSD rate increase** | 9:45 a.m. Monday, on a proposed **30%** water and **14%** sewer increase; about 25 people came to Thursday's hearing and the PSD serves over 4,900 customers. Parkersburg News and Sentinel. Ran as No. 11's only regional line — **the vote is the follow-up** |
| **2026-08-29** | **WV gun bear season opens in selected counties** | Aug. 29 - Sept. 7, season limit 2, daily 1. **The county list is NOT in the pamphlet's summary table**, so no county was named. WVDNR via `reference/wv-hunting-2026-27.json`. Ran as Sports & Sportsman No. 1's only "coming in" entry |
| **2026-09-12** | **WV squirrel opens, the first general season of the year** | Youth weekend Sept. 5-6, then Sept. 12 - Feb. 28, daily 6. WVDNR reference file. Until then West Virginia has nothing open but year-round species, which is why the sportsman calendar is thin in August |
| **August 2026** | **WVDNR migratory bird regulations publish** | Goose, duck, dove, woodcock and snipe dates are **not** in the hunting summary table and come from a separate publication issued in August; HIP registration required. Watch for it — it is the next thing that fills the sportsman calendar |

| **2026-08-17** | **Marshall v Ohio women's soccer result** | Played 7 p.m. Sunday at Hoops Family Field, both sides followed. Previewed in Sports & Sportsman No. 1 and deliberately **not re-run in No. 2** because the match had not kicked off when the paper posted. **The result is Monday's Our Teams line** |
| **2026-08-21** | **Premier League 2026-27 opens** | Confirmed again on `premierleague.com` this morning. Chelsea closed pre-season 3-1 over Real Sociedad, Tottenham 3-0 over Hoffenheim; Arsenal met Manchester City in the Community Shield at Cardiff on Aug. 16. From Friday the football beat is results, not friendlies |
| **2026-08-26** | **WV Lottery Commission votes on the new Greenbrier board** | The $500M Kennedy Lewis joint venture **closed** Aug. 14, KLIM taking **51%**; the 90-job casino stays open and unapproved board members must stay "insulated from casino operations" until the vote. Acting director **David Bradley** is disappointed the deal leaves ~**$3M** in DEP mining penalties unresolved; a **$47M** First Guaranty suit and a ~**$35M** coal judgment also remain. WV MetroNews. Ran as No. 12's second statewide brief |
| **2026-08-24** | **Huntington council takes up the Flock ordinances** | Mayor **Patrick Farrell** presented his guardrails to the Public Safety Committee **Aug. 14**: retention cut to **seven days** (from 30, following a Flock policy change), misuse penalties and access controls. Councilwoman **Tia Rumbaugh** still wants stricter criminal penalties. **Final text was due for release Aug. 21** ahead of the Aug. 24 council meeting. WSAZ. Ran as No. 12's `huntington_cabell` line |
| **2026-08-31** | **Aki banzuke (rankings) released** | Unchanged and now the load-bearing date: searched again this morning and the **Sept. 13-27 Aki dates are still carried only by ticket resellers, travel sites and fan databases**, which this paper does not cite. That is **four separate mornings** the JSA and the wires have failed to produce a citable schedule. The banzuke release is the moment Kyodo, Japan Times or NHK must print it. **Sumo sat out No. 2 on those grounds, which is the correct edition under Ian's rule, not a miss** |
| **~2026-12-2027** | **Carter Memorial (Fort Hill) bridge rehab, I-64 Charleston** | **$74M** deck replacement, the first since the early 1970s, on a bridge carrying about **100,000 vehicles a day**. Triton Construction. Crossovers and median barrier work **Aug-Nov 2026**, deck replacement late winter/early spring 2027, completion **December 2027**. DOH spokesman **Brent Walker** quoted. WV MetroNews. Ran as No. 12's `putnam_kanawha` line — **the lane switch is the next line, not the prep work** |

| **2026-08-18** | **Wood County Commission vote on the Lubeck PSD rate increase** | The vote was set for **9:45 a.m. Monday Aug. 17** on a proposed **30%** water and **14%** sewer increase — a 3,000-gallon bill going from **$34.35 to $44.73**. **This paper posts at 7 a.m., so the vote had not happened and no `mid_ohio_valley` line ran.** Parkersburg News and Sentinel. Separately, **Martin has announced his retirement from Lubeck PSD**, which was not run because its date could not be pinned inside 48 hours. **The outcome is Tuesday's regional line** |
| **2026-08-18** | **Marshall v Ohio women's soccer, STILL OWED** | Played 7 p.m. **Sunday Aug. 16** at Hoops Family Field, both sides followed — the sportsman paper's house derby. Previewed in S&S No. 1, held out of No. 2 because it had not kicked off, and **held out of No. 3 because no outlet this desk could open had posted a result by 5:45 a.m. Monday** (`herdzone.com` title-only and its `/news/` index 404). **This is the second morning the ledger has carried this row unresolved. Try `therealwv.com`, WSAZ and the Ohio athletics site, not just herdzone** |
| **~2026-08-17** | **Nucor Apple Grove sheriff's detail ends** | The 10-day security detail posted after the Aug. 7 threat closure was due to end about today. **Not searched this morning** — the flooding took the West Virginia sweep — so this is carried forward unchecked rather than reported as quiet. Check it tomorrow |
| **2026-08-21** | **Premier League 2026-27 opens** | Unchanged. **Arsenal beat Manchester City 3-0 in the Community Shield on Sunday**, carried as one attributed clause inside the Rodri brief because `premierleague.com/en/news` returned navigation only and no readable match report could be opened |
| **~2026-08-24** | **Rodri's move to Barcelona completes** | City accepted **65.4M pounds ($88.47M)**; the 30-year-old **2024 Ballon d'Or** winner agreed a **four-year** deal and was expected at Barcelona "the following week." He missed the Community Shield after **minor back surgery** and returned to training Friday. Al Jazeera, citing Sky Sports. Ran in S&S No. 3's Around the Leagues. **The completed transfer, or a collapse, is the news** |

| **2026-08-31** | **Aki banzuke (rankings) released** | Unchanged and still the load-bearing date. Searched again this morning: the **Sept. 13-27 Aki dates are still carried only by ticket resellers, travel sites and fan databases**, which this paper does not cite — an **eighth** straight morning. `sumo.or.jp/En/` was fetched and its newest item is still the **Aug. 5** museum-calendar update; the September page says only that every day is sold out. The banzuke release is the moment Kyodo, NHK or the Japan Times must print the dates. **The countdown ran as S&S No. 7's sumo line, pegged to the banzuke at 10 days out rather than to the basho at 23, so it is a different sentence from No. 6's** |
| **2026-08-16 — RESOLVED** | **Marshall v Ohio women's soccer, the house derby this paper owed since No. 1** | **It was never played. `herdzone.com` carries "Herd Women's Soccer's Contest With Ohio Postponed," dated Aug. 16 — postponed for thunderstorms in the Huntington area, no makeup date scheduled.** The story would open only to its headline, as herdzone always does for this pipeline, so **no result, reason or makeup date was printed as fact**; S&S No. 7's Our Teams note reports it as a fixture the desk could not read past the headline. **The row that sat open across Nos. 2, 3 and 4 waiting for a result was waiting for a match that did not happen.** Watch the Marshall schedule for a makeup date |
| **2026-09-08** | **Direct testimony due in the MARL transmission line case** | PSC staff moved **Aug. 19** to toll the case at least 60 days or dismiss it, saying five route changes NextEra filed **July 30** give three newly affected landowners **39 days**. The line is **107.5 miles at 500 kilovolts**, Dunkard Township, Pa. to Gore, Va. **Note the two readable outlets disagree on the West Virginia counties — WVPB lists Monongalia, Preston, Mineral and Hampshire; WV MetroNews adds Jefferson — so no county count was printed.** Route changes add about **$1M**. Evidentiary hearing late October. WV Public Broadcasting. Ran as No. 17's first statewide brief. **The commission's ruling on the motion is the news** |
| **open** | **Bluefield State University Board of Governors emergency session** | Met **Thursday evening Aug. 20** in closed session on a notice giving the purpose as **"Imminent Substantial harm to the institution,"** and announced nothing afterward. The administration said it "have not been provided information regarding the purpose of the meeting beyond what appears in the public notice." President **Dr. Darrin Martin** has led the school since November 2024 and previously worked to restore its standing with the Higher Learning Commission after a critical 2023 governance report. WV MetroNews. Ran as No. 17's second statewide brief. **Whatever the board was meeting about is the news** |
| **2026-09-04** | **Kanawha County curbside flood debris pickup ends** | Runs **Aug. 24 to Sept. 4** in the unincorporated county — Campbells Creek, Cabin Creek, Rutledge Road and Cross Lanes — for construction debris, flood-damaged furniture, appliances, vegetative debris and household hazardous materials, placed on the public right-of-way; crews will not enter private property. WSAZ. Ran as No. 17's `putnam_kanawha` line |
| **~2026-08-22** | **FEMA mobile centre in Ritchie County closes** | Open daily from 7 a.m. in **Auburn** through Saturday evening, for residents hit by **July's** flooding. Sheriff **Bryan Davis** is pressing people to apply — "You're not obligated to pay anything. It's a grant" — and says many eligible residents are still reluctant. WV MetroNews. Ran as No. 17's `mid_ohio_valley` line. **Note this is the JULY flood, not the Aug. 16 one** |
| **2026-08-26** | **20th Street underpass closes, Huntington** | Wednesday, 9 a.m. to 4:30 p.m., Huntington Sanitary Board work on the pumps under the roadway; no detour given. The Herald-Dispatch. **Written, opened, sourced and CUT FOR BUDGET** — the fourth Cabell line to be cut this way. Only a line at all on a thin Cabell morning |
| **open** | **Transportation Safety Board investigation, Prince George plane crash** | A **Beech King Air 200** with **eight aboard** left Prince George Airport about 11 a.m. Thursday for the Kemess Creek area and made an emergency landing on **Foothills Boulevard** just north of North Nechako Road about **2:18 p.m.**, hitting vehicles. **One person in a ground vehicle was killed and two were hospitalized; nobody aboard the aircraft was reported hurt.** TSB investigators were due Friday morning. CKPG Today. Ran as No. 17's away line — **the first away line since Aug. 12** and the first from Prince George since No. 1. **A cause finding is the news** |
| **2026-09-01 → 2026-09-14** | **NC recreational southern flounder season** | One fish per person per day, **15-inch** minimum, hook and line and gig only, coastal and joint waters, under proclamation **FF-27-2026**. Closed and unlawful to possess until then. NCDMF, confirmed on `deq.nc.gov` this morning. Ran as S&S No. 7's "coming in" |
| **2026-09-05 → 2026-09-06** | **WV youth squirrel weekend, then the general season Sept. 12** | Youth daily 6, possession 12, season limit 12 (pamphlet page 40); the general gray, black, albino and fox squirrel season runs **Sept. 12 - Feb. 28** at a daily 6 and possession 24. WVDNR via `reference/wv-hunting-2026-27.json`, `valid_through` **2027-06-30** checked against the edition date. Ran as S&S No. 7's second "coming in" |

## 3. Open threads

- **wv-flooding-aug16** — 2026-08-17: **new, and it is the live WV thread.** A training axis of
  thunderstorms sat over south-central West Virginia through Sunday, peaking at **11.8 inches
  near Eskdale**, with **6 to 10+ inches** on the Eskdale-Kincaid-Oak Hill-Cunard-Danese line and
  3 to 6 from Charleston through Marmet and Montgomery; rates ran **1.5 to 2.5 inches an hour**.
  **Fayette, Kanawha and Raleigh** took the damage: **U.S. 60 at Kanawha Falls** hit by high
  water, rock and mud, the **Fayette County Animal Shelter access bridge destroyed** near
  Beckwith, **CSX washouts between Pratt and Montgomery**, Turnpike washouts and mudslides, high
  water in homes at **Pax and Mount Hope**, and an eastbound **Amtrak** train stopped near Pratt
  and reversed to Charleston. **Dozens of swift-water rescues in Charleston from about 8:30 p.m.,
  easing by 10:30** — Garrison Ave., Rutledge Rd., Valley Rd. at Swarthmore, Green and Stockton,
  Campbells Creek Dr., with **Elk Twomile Creek** out of its banks and pavement reportedly gone at
  Chandler Dr. and Arnold St. NWS flash flood warning for Kanawha ran to **5:15 a.m. Monday**. WV
  MetroNews and The Herald-Dispatch. **NO deaths, injuries or state of emergency were reported by
  any outlet this desk could open, and none was printed** — see `docs/FAILURES.md` for the 2022
  and July 2026 stories that search results tried to pass off as this one. **A damage estimate, a
  declaration, a death, or a WVDOH road-reopening list is the news.**
- **williams-river-flood** — 2026-08-17: the gauge is the story's second half. USGS 03186500 read
  **4620 cfs and 7.55 feet at 5:15 a.m.**, against **179 cfs and 2.00 feet** 24 hours earlier — a
  26-fold rise. The fetcher's verdict is **"blown out. Stay on the bank."** Both papers carried
  it, and it was **today's drawing** (`art/2026-08-17-wv.svg`, placement `wv`), deliberately drawn
  as the flood counterpart to the **2026-08-15** low-water sketch of the same reach at 179 cfs.
  **The Ohio bracketed the dam rising too: Point Pleasant 27.96 ft, Huntington 30.75 ft, both up
  nearly three feet in a day.** Watch the recession — the Williams dropping back under about 300
  cfs is when the sportsman paper has wadeable water again.
- **gaza-road-map** — 2026-08-17: **new, and it led No. 13.** **Jared Kushner** met Hamas chief
  **Khalil al-Hayya** in **Cairo** on Sunday for **more than two hours**, with envoy **Steve
  Witkoff** and Egyptian, Qatari and Turkish officials, seeking Hamas's commitment to a
  **15-point** U.S. road map. The plan: Hamas hands weapons to a **Palestinian technocratic
  committee**, Israeli forces halt attacks and withdraw, an international force separates them.
  Hamas wants Israel back to the **"yellow line"** before a **14-day** negotiating period opens,
  and has linked heavy weapons to Palestinian statehood, which Israel rejects. **Israeli forces
  control about 60% of Gaza.** **Netanyahu rejected the road map last week** — "will not withdraw
  from any position in Gaza until Hamas has been completely disarmed" — and meets Kushner, **Tony
  Blair** and Board of Peace director **Nickolay Mladenov** on **Monday**. Saudi Arabia, the UAE,
  Jordan, Pakistan and Indonesia issued a joint statement blaming Israel for obstructing the
  effort. NPR cross-checked against PBS NewsHour and Euronews. **NPR dates the meeting Sunday
  Aug. 16 and PBS's copy says Aug. 15; Aug. 16 is the Sunday, so the brief said "Sunday" and
  printed no hard date.** **Monday's meeting is the news.**
- **midwest-flooding-2026** — 2026-08-17: **moved and ran again as No. 13's first U.S. brief.**
  Indiana's toll is now **at least 7** (from 5 in No. 12), per state homeland security
  spokesperson **Liz Woods**: a **4-year-old** killed by a tree through his bedroom in Jennings
  County, cyclist **James Briar**, 31, in Henry County, **Matthew Morey**, 19, from the
  Mississinewa, **Stephanie Sallee**, 58, in a Delaware County cornfield. **Trump approved
  federal disaster assistance**, which is the movement the ledger was waiting on. **350+
  evacuations**, nearly **130,000** without power; Indianapolis Mayor **Joe Hogsett** called it
  the worst in 30 years. PBS NewsHour. **Thread closes unless the toll moves again.**
- **meta-addiction-trial** — 2026-08-17: new, ran as No. 13's second U.S. brief. **California,
  Colorado, Kentucky and New Jersey** v Meta before **Judge Yvonne Gonzalez Rogers**, N.D. Cal.
  in **Oakland**, ~**6 weeks**, seeking up to **$1.4 trillion** and product changes over designed
  addictiveness and COPPA violations. Meta calls the claims "unsubstantiated." Meta lost a **$6M**
  Los Angeles verdict and a **$567M** New Mexico judgment in 2026. NPR. **Note: NPR's copy says
  "Tuesday, August 17," but Aug. 17 is a Monday, so the brief said "this week."** **A verdict or
  an early ruling is the news.**
- **lake-powell-record-low** — 2026-08-17: new, ran in No. 13's U.S. section. **3,519.91 feet**
  Saturday, below the **April 2023** record, down **20+ feet** since January and about **30 feet**
  above the elevation at which **Glen Canyon Dam** stops generating. **40M+ people** across seven
  states; Powell and Mead's combined storage is at levels last seen **May 1957**. Reclamation
  proposed a **10-year** plan in July with cuts for Arizona, California and Nevada; the seven
  states have not agreed. PBS NewsHour. **News again on an agreement or on the turbine threshold.**
- **korea-exercises-cut** — 2026-08-17: new, ran in No. 13's U.S. section. Trump told Defense
  Secretary **Pete Hegseth** to "substantially reduce" joint drills, announced on social media
  Sunday, calling them costly and a signal "totally inappropriate and hostile," and said North
  Korea has been "unthreatening and respectful." **Ulchi Freedom Shield** was to run **11 days**
  with **18,000** South Korean troops. North Korea threatened "stern steps" on Friday. He halted
  the same drills in **2018**. NPR, also PBS. **Seoul's response is the news.**
- **messina-art-heist** — 2026-08-17: new, led No. 13's World section. Thieves cut perimeter
  fencing and an armoured case at the **MuMe** museum in **Messina, Sicily** about **9:50 p.m.
  Sunday**, during **Ferragosto** and the Vara procession, taking a double-sided **Antonello da
  Messina** panel (1465-74) and three sections of the **San Gregorio Polyptych** (1473) and
  leaving the Saint Benedict and Saint Gregory panels behind. Up to **80M euros ($93M)**. Director
  **Marisa Mercurio**: "We are devastated by what happened." Al Jazeera. **An arrest or a recovery
  is the news.**
- **zambia-election-2026** — 2026-08-17: new, ran in No. 13's World section. **Hakainde
  Hichilema** (UPND) had nearly **59%** of votes counted, **Brian Mundubile** (NRPUP) about a
  third; **50%+** avoids a runoff and final results are due within days. The opposition says armed
  personnel entered Mundubile's Lusaka home Friday night, firing and wounding an MP. **EU
  observers**: "competitive but skewed towards the incumbent," citing "heavy bias in state media";
  a polling agent was killed near Lusaka on election day and counting was suspended six hours.
  Al Jazeera. **The declared result is the news.**
- **bihar-temple-deaths** — 2026-08-17: new, ran in No. 13's World section. An electric pole fell
  at the **Ashok Dham** temple in **Lakhisarai, Bihar**, during **Shravan**, electrocuting
  worshippers and setting off a crush: **at least 7 dead**, more than a dozen hospitalized. Police
  officer **Shivam Kumar** quoted; Chief Minister **Samrat Choudhary** called it "extremely
  tragic." Euronews, also Al Jazeera. **A cause finding is the news.** Thread closes otherwise.
- **wv-pratt-whitney-bridgeport** — 2026-08-17: new, ran as No. 13's second statewide brief.
  **Pratt & Whitney Canada** took a **nine-year, $1B** contract to overhaul **PT6A-68** engines for
  the military's **T-6** trainers at **North Central West Virginia Airport, Bridgeport** (Harrison
  County), where about **500** people work. Senior director **Anthony Hinton** said most of the
  engines were built at Bridgeport in the late 1990s and early 2000s. Engines overhaul every **5
  years or 4,500 flight hours**; ~**25,000** of ~**67,000** built remain in service. Mechanics come
  through **Pierpont Community and Technical College** on airport grounds. WV MetroNews. **A
  hiring number is the news.**
- **digoxin-heart-failure** — 2026-08-17: new, ran in Sci/Tech. **University Medical Center
  Groningen** (**Dirk Jan van Veldhuisen**, **Kevin Damman**, **Peter van der Meer**): **1,000**
  patients across **43** Dutch centres, ~3 years, low-dose digoxin cut heart-failure admissions
  **25%**; cardiovascular death and worsening fell **19%** but not significantly alone, significant
  in a three-study meta-analysis. Under **10 cents a day**. *Nature Medicine* and *JAMA*, presented
  at ESC Heart Failure in Barcelona. `source` names the institution, the convention since No. 4.
  **News again if guidelines change.**
- **baryon-junction** — 2026-08-17: new, ran in Sci/Tech. **Brookhaven National Laboratory**, STAR
  detector at **RHIC** (2000 to early 2026): about **twice as many baryons** as expected emerging
  perpendicular to the beams, evidence a **Y-shaped gluon "baryon junction"** carries baryon number
  rather than the three valence quarks. **Zhangbu Xu** quoted. *Science* 393(6812):727. **News again
  on a confirmation at another collider.**
- **graphene-flexoelectricity** — 2026-08-17: new, ran in Sci/Tech. **Rice University**
  (**Pulickel Ajayan**, lead author **Sathvik Ajay Iyengar**), with Sussex and Penn State: wrinkles
  curved at **sub-nanometre** radius polarise graphene **100,000 to 10 million times** more strongly
  than larger flexoelectric systems, and **sharpness matters more than height**. *Advanced Materials*,
  DOI 10.1002/adma.202518224. **News again on a device.**
- **covid-viral-reactivation** — 2026-08-17: new, ran in Sci/Tech. **Boston Children's Hospital**
  (**Dr. Ofer Levy**) with 14 institutions: **1,154** patients at **20** hospitals, **200,000+**
  samples, **11** viruses reactivating within **40 days** of hospitalisation — Epstein-Barr, herpes
  simplex 1, cytomegalovirus, and **Anelloviridae**, which tracked most strongly with long COVID and
  lasting disability. **Inflammation, not immunosuppression**, appeared to be the trigger, which
  overturns the prevailing assumption. *Nature*, August 2026. **News again on a treatment target.**

- **flores-quake-2026** — 2026-08-16: **led No. 12**, its second front page in two days and it
  moved hard. **51 dead** (from 20 when No. 11 led on it, and 47 on NPR's Saturday copy),
  **36 seriously injured, 77 slightly**, about **5,000 displaced**, **341 aftershocks**.
  Magnitude **7.7** at **5:58 a.m.** local Saturday, **68 km NNW of Ende**, depth **10 km**
  (USGS). **157 houses flattened**, ~**1,300** damaged; tsunami warning issued and lifted, a
  **1.61 m** wave at Riung. **3,500+** military and police, three helicopters, one rescue
  vessel; a state of emergency was under consideration. A 1992 quake in the same waters killed
  **2,500+**. Al Jazeera (Aug. 16) cross-checked against NPR and PBS (both Aug. 15, both at
  47). **Al Jazeera's later figures ran and were attributed to it by name.** Expect the toll to
  keep moving — re-check before citing.
- **uss-lincoln-deployment** — 2026-08-16: **finally ran**, as No. 12's third U.S. brief, after
  being held on 2026-08-14 for being the same theatre as the Hormuz lead. The hook is Trump's
  answer Friday to whether the deployment ran too long: **"not nearly long enough."** Now
  **nine months**. Crew families quoted by NPR on food shortages and plumbing failures;
  **Karen Bramlett**, a sailor's grandmother, said he "needs to be ashamed of himself."
  Acting Navy Secretary **Hung Cao** cited Iran and acknowledged "a small number of mental
  health cases." **Sen. Ruben Gallego** wants a bipartisan oversight visit. NPR. **News again
  on the George Washington actually relieving her, or on a congressional visit.**
- **midwest-flooding-2026** — 2026-08-16: new, ran as No. 12's second U.S. brief. **At least
  five dead in Indiana** — a boy killed by a falling tree, a woman swept away driving into
  floodwater, a teen missing since Wednesday. **11+ inches in two days**; the **White River
  crested above 24 feet at Anderson and Noblesville, past the 1913 record**. **350+
  evacuations** in Delaware County, **95 people and 45 pets** rescued Saturday. Gov. **Mike
  Braun** said Trump intended to approve his federal request. PBS NewsHour. **NPR's earlier
  copy named West Virginia among the affected states but PBS's did not, and no WV detail was
  obtainable, so the notebook did not carry it.** News again on the declaration or a WV impact.
- **private-sector-cyberops** — 2026-08-16: new, ran as No. 12's fourth U.S. brief. A
  presidential memorandum, **"Expanding Capabilities to Combat Transnational Cyber-Enabled
  Crime,"** issued **Aug. 14**, lets vetted companies access and disrupt networks of designated
  foreign groups. Companies contract with **DOJ or DHS**, undergo vetting and post a **$1M**
  performance bond; **DOJ and DHS have two months** to settle the legal questions. It does not
  authorise attacks on foreign governments. **Paul Rosenzweig** called it "a bad idea";
  **Joshua Steinman** defended the targets as organised crime. NPR. **The first contract award,
  or the first lawsuit, is the news.**
- **lebanon-truce-strikes** — 2026-08-16: new, led No. 12's World section. Israeli strikes on
  **Ansar** (seven killed, three of them children) and **Deir al-Zahrani** (four killed, 17
  wounded) killed **11** Saturday, the deadliest day since the **June 20** truce. Israel said
  it hit Hezbollah infrastructure in response to actions against its soldiers; Netanyahu's
  office said Hezbollah wounded three soldiers. Lebanese PM **Nawaf Salam** said the Ansar dead
  "are not military infrastructure." PBS NewsHour, carrying AP. **News again on a truce
  collapse or a Lebanese diplomatic step.**
- **hungary-bus-crash** — 2026-08-16: new, ran as No. 12's second World brief. A
  **Polish-registered coach** with **57 passengers and two drivers**, Serbia to Poland,
  overturned into a ditch on the **M3 near Mezokeresztes**, ~140 km east of Budapest, about
  **1 a.m. Sunday**. **12 dead** (11 at the scene, one in hospital), **10 seriously** and
  **37 slightly** injured. Police said the driver **likely fell asleep** and detained him.
  Hungary's deadliest road accident since **2003**. Euronews. **A finding from the
  investigation is the only thing that makes it news again.**
- **ukraine-long-range-strikes** — 2026-08-16: new, ran as No. 12's third World brief. Ukraine
  sent about **600 drones** at Moscow; Mayor **Sergei Sobyanin** said **201** were destroyed
  over the region and an **83-year-old man** was killed in Moscow Oblast. Russian strikes hit
  Kyiv and **Kryvyi Rih**, killing a woman and wounding six; three dead in Rostov. A Spanish
  **F-18** on NATO duty downed a drone over Romania, the **fourth** such incident in 2026. UN
  data put July's Ukrainian civilian casualties at **437 killed, 2,610 injured**, the worst
  since 2022. Al Jazeera. **Live.**
- **camc-hernia-settlement** — 2026-08-16: new, ran as No. 12's first statewide brief **and it
  is the live WV thread.** **Charleston Area Medical Center** settled a class action for
  **$40M** covering **more than 4,000** patients given unnecessary hernia repairs during
  bariatric surgery. Filed **April 2025**; the two surgeons named, **Robert Shin** and
  **Samuel Rossi**, no longer work there. Plaintiffs' counsel **Ben Salango** and **Dante
  diTrapano**. Administered by Rust Consulting. WV MetroNews. **Court approval, or a per-patient
  figure, is the news.**
- **reactor-antineutrinos** — 2026-08-16: new, ran in Sci/Tech. **Max-Planck-Institut fuer
  Kernphysik** (**Anthony Onillon**, **Thierry Lasserre**) and the **Double Chooz**
  collaboration detected antineutrinos from a **shut-down** reactor for the first time: ~**100
  candidate events** over **17.2 days** with both Chooz units offline, from decay in the cores
  and spent-fuel pools, in a 30-cubic-metre scintillator **400 m** away. *Physical Review
  Letters* 137(6). Points at shutdown verification and spent-fuel accounting. `source` names the
  institution, the convention since No. 4.
- **quantum-heat-engine** — 2026-08-16: new, ran in Sci/Tech. **Aalto University** (**Mikko
  Moettoenen**, first author **Tuomas Uusnaekki**) ran the first cyclic **quantum heat engine**
  in superconducting circuits — a transmon qubit, a resonator and a quantum refrigerator
  completing repeated **Otto cycles** near absolute zero. *Nature Communications* 17(1). The
  point is cutting the microwave cabling large quantum machines need; Finland targets **1,000
  logical qubits by 2035**. News again on an autonomous version.
- **haplodiploidy-overturned** — 2026-08-16: new, ran in Sci/Tech. **Arizona State University**
  (**Sachin Suresh**, **Timothy Linksvayer**) tested the **60-year-old haplodiploidy
  hypothesis** across nearly **69,000** insect species and found it predicts eusociality only
  within **aculeate Hymenoptera** — ants, bees and stinging wasps — pointing instead at
  stingers and nesting behaviour. *Current Biology* 36(15). Thread closes unless contested.
- **osaka-mosasaur** — 2026-08-16: new, ran in Sci/Tech. **Okayama University of Science**
  (**Shoji Hayashi**, **Yasuaki Takano**) identified four unrecognised mosasaur bones collected
  at **Sobura, Kaizuka City, Osaka, in 1990-92** and left in rock ~**30 years**, including the
  **first premaxilla confirmed in a Japanese specimen**; horn-like projections on the
  basisphenoid suggest a possible new species. Presented **June 27, 2026** to the
  Palaeontological Society of Japan. **Presented, not yet peer-reviewed — written as a
  presentation, not a study.**


- **hormuz-reopening** — 2026-08-14: **moved hard and led No. 10, its third front page** (it also led
  Nos. 1 and 5). Two **ADNOC** vessels were attacked crossing the strait **Thursday evening** — no injuries,
  ADNOC said the situation was "brought under control" — the **second attack on the company's ships in days**
  (the previous was Saturday) and the **15th since February**. The **UAE foreign ministry** called Iran's use
  of the strait as economic coercion **"piracy"** and a **"direct threat to the stability of the region"**;
  **Iran did not comment**, and no group claimed it. The rhetorical half: Trump posted **Wednesday** that the
  US has **"total control"** of the strait, that the naval blockade is **"A WALL OF STEEL"** and **"I THINK WE
  WILL KEEP IT!"**; **Ebrahim Zolfaghari**, spokesman for Iran's central military command, said the waterway is
  under **"the complete management and control of the Islamic Republic"**; Basij commander **Hossein Taeb** and
  FM **Abbas Araghchi** ("worse than fake news is fake intelligence") said the same. The **Persian Gulf Strait
  Authority** said the strait stays blocked until Iran's conditions are met. Numbers, from CBS: **8 transits
  Tuesday**, the fewest since **Aug. 5**, against a **10-day average near 12**; WTI about **$81**; national
  average gasoline **$4.07** against **$3.16** a year ago. Cross-checked on **Al Jazeera, Euronews and CBS
  News**. **`france24.com` 403s this crawler now — it carried the same story and could not be opened.**
  **News again on a signed Oman corridor deal, a US answer to the conditions, or a vessel actually seized.**
- **uss-lincoln-deployment** — 2026-08-14: **searched, read, and deliberately not run**, but it is the piece
  of the Hormuz story most likely to be tomorrow's brief. The Pacific carrier **USS George Washington** left
  Da Nang and is in the **Strait of Malacca** bound for the Middle East to relieve the **USS Abraham Lincoln**,
  which has been at sea **260+ consecutive days** — deployed **Nov. 21** from San Diego, in theatre since
  January, held past a May return. Reported supply shortages, mental-health concerns (the Navy denies a rise in
  suicidal ideation), a sailor overboard in early August, recovered. **Pete Hegseth** says conditions were
  "completely misrepresented"; **Sen. Richard Blumenthal** has written to the Navy and **Sen. Ruben Gallego**
  called conditions "not just disgusting; it's dangerous" and proposed a bipartisan oversight visit. The move
  leaves the Pacific without a carrier. NPR, carrying AP; CBS has the senators' letter separately. **Held
  because the lead was already Hormuz and this is the same theatre** — it is a clean U.S. brief the moment the
  lead moves elsewhere.
- **harvard-antisemitism-suit** — 2026-08-14: new, led No. 10's U.S. section. **U.S. District Judge Richard G.
  Stearns** in Boston dismissed the administration's Title VI suit, finding the incidents **"too isolated and
  episodic"** to show a persistent civil rights violation; the case rested on **2023-24** events plus a few
  from **March 2025**. The government had sought to claw back **billions** in research grants awarded since
  October 2023. Assistant Attorney General **Harmeet Dhillon**: "We disagree with the ruling and are assessing
  next steps." A separate ruling ordered **$2.6B** in Harvard funding restored, calling antisemitism concerns a
  "smokescreen." NPR. **An appeal is the news.**
- **same-day-executions** — 2026-08-14: **closed, and the follow-up No. 9 promised was carried.** All three
  went ahead **Thursday** by lethal injection: Oklahoma at **10:13 a.m. CT**, Tennessee **30 minutes** later,
  Alabama that **evening** — the first same-day trio since **Jan. 7, 2010**. **21 executions** nationally so
  far in 2026 with nearly a dozen scheduled; **Florida alone has 12**, more than every other state combined;
  47 people were executed in 2025 across 11 states, the most since 2009. CBS News. **The three men's names and
  the victims' details were deliberately left out again**, as in No. 9. Thread closes.
- **europe-wildfires-2026** — 2026-08-14: new, ran as No. 10's first World brief. About **1,800** people left
  **Gey**, Germany, near the Belgian border, and **525** villagers the **Landes** in France, where a fire has
  run **1,100 hectares since Thursday** and come within **2 km** of Luglon; **500 firefighters and six
  aircraft** are on it. **14 hospitalized in Split**, Croatia, **seven** in life-threatening condition; chief
  fire commander **Slavko Tucakovic**: "We have had an extremely difficult night." Thousands more evacuated in
  Croatia and Greece. About **500,000 hectares** have burned across the EU this summer. Al Jazeera. **News
  again on a death, a national emergency declaration, or an EU civil-protection deployment.**
- **farage-clacton** — 2026-08-14: new, ran as No. 10's second World brief. Farage retook **Clacton**
  **22,239** to **9,455** for the satirist **Count Binface**, on **44%** turnout against **59%** at the 2024
  general election, in a by-election the main parties **boycotted** — 34 candidates, mostly independents and
  fringe parties. He had resigned the seat in **July** while under investigation over an unreported **5 million
  pound** cryptocurrency donation from an overseas billionaire; **that inquiry is the live thread, not the
  result.** Al Jazeera. **News again on a finding in the donation inquiry.**
- **taiwan-han-kuang** — 2026-08-14: new, ran as No. 10's third World brief. Carriers cut mobile data to
  **256 Kbps** for **30 minutes** Thursday in **Taipei and six other places** during the **Han Kuang**
  exercises, alongside metro air-raid drills and hospital relocation drills; **18 Chinese warplanes and 11 navy
  ships** operated around Taiwan between Wednesday and Thursday. President **Lai Ching-te**: "We ask for your
  understanding and support, as this is a necessary drill." This year's drills pull in civilians and local
  government for the first time. NPR. **News again when the exercise ends or on a Chinese response.**
- **ames-goldsmith-h2s** — 2026-08-14: new, ran as No. 10's first statewide brief **and it is the live WV
  thread.** The **U.S. Chemical Safety Board** said workers decommissioning **Ames Goldsmith Catalyst
  Refiners** at **Institute** were **not required to wear respirators and were never given personal gas
  monitors**; the four respirators on site carried filters that **would not have stopped hydrogen sulfide**.
  On **April 22** workers pumped about **80 gallons** of A-50 calcium chloride solution, **275 gallons** of
  M-2000A sodium trithiocarbonate solution and then dilute nitric acid into one tank, releasing H2S: **two
  dead**, one critical who survived, **four** more seriously hurt, **22** decontaminated on site and **18**
  transported. CSB chair **Steve Owens** quoted. WV MetroNews; WSAZ carried it separately. **The investigation
  is open — a final report, a citation, or an OSHA action is the news.**
- **greenbrier-casino** — 2026-08-14: new, ran as No. 10's second statewide brief. See the **Aug. 15**
  forward-dated row for the full detail and for the two dating conflicts between outlets. **The IRS has filed
  federal tax liens totalling over $12M** against Greenbrier entities and an **Omni Hotels** affiliate holding
  **$289M** in purchased loans is seeking a receiver — neither printed, both available. **Live.**
- **peoples-cartage-fire** — 2026-08-14: **moved again and ran as the `mid_ohio_valley` line for the second
  morning running.** At Thursday's town hall independent tester **Scott Smith** said the July fire's plume
  reached **10,000 feet** across at least a **35-mile radius**, against **2,800 feet** at East Palestine, and
  that four classes of contaminant have been tested so far — **metals, dioxins, PFAS and semi-volatile organic
  compounds**. Residents reported burns from touching plants and sudden illness. **He is an independent tester,
  not an agency, and the line attributed the plume figures to him rather than stating them flat** — the state's
  own WVDA/WVDEP findings, which No. 9 printed, said nothing above federal action levels and some samples above
  state screening thresholds. WTAP. **He returns in about two weeks.**
- **nigeria-womens-world-cup** — 2026-08-14: new, led No. 10's Sports. **South Africa 2-1 Nigeria** (**Thembi
  Kgatlana** 56', captain **Refiloe Jane** 77'; **Christy Ucheibe** penalty) and **Ghana 2-1 Ivory Coast**
  (**Princess Marfo**, then **Josephine Bonsu** 72' from the spot after a VAR handball) take Africa's two
  intercontinental playoff places. **Nigeria will miss a Women's World Cup for the first time since the
  tournament began in 1991.** Ghana are chasing a first appearance since 2007. Al Jazeera. **This is a
  different competition from the WAFCON final** — Cameroon, Malawi, Morocco and Algeria are already qualified
  directly. Playoffs are November-December.
- **swiatek-canadian-open** — 2026-08-14: new, ran in Sports. **6-2, 6-3** over **Rybakina** in Toronto — her
  **first title of the season**, first at this event, and it moves her back into the **top five** from **No.
  8**. Rybakina had **12 unforced errors in the first set** and blamed fatigue from three extra hours on court.
  Al Jazeera. Thread closes; the US Open is the next hook.
- **marshall-women-soccer** — 2026-08-14: new, ran in Sports as the local anchor after the WVU men's soccer
  opener could not be opened (see `docs/FAILURES.md`). **Marshall 3-1 Morehead State** at Huntington Thursday,
  **Luana Gusmao** twice inside seven minutes (28', 35'), **Hannah Carter** off a corner for Morehead,
  **Delfina Lombardo** the third. **The Herd host Ohio Sunday at 7 p.m.** WSAZ. Not a running thread.
- **oist-hibernation-memory** — 2026-08-14: new, ran in Sci/Tech. **Okinawa Institute of Science and
  Technology** (Prof. **Kazumasa Tanaka**, Dr. **Yu-Ju Lin**), with Tsukuba, ExCELLS and NIPS, induced
  artificial hibernation in mice and imaged synapses by correlative light and electron microscopy: **more than
  half of hippocampal synapses disappeared** and memory held or improved, which points at **engram
  architecture** — clustered patterns — rather than synaptic strength. *Science*. `source` names the
  institution, the convention since No. 4. News again on a mammalian-torpor or clinical follow-up.
- **petm-forest-canopy** — 2026-08-14: new, ran in Sci/Tech. **Natural History Museum of Los Angeles County**
  (Dr. **Regan Dunn**, La Brea Tar Pits) with **Ellen Currano** (Wyoming) measured **leaf area index from
  fossil leaf cuticle for the first time**, using epidermal cell aspect ratios, on coal and lignite from
  Wyoming's **Hanna Basin**: canopy cover declined **56 million years ago** through the **Paleocene-Eocene
  Thermal Maximum**, with plants moving north, more erosion and a disrupted water cycle. Today's carbon release
  runs **an order of magnitude faster**. *Science*. News again on a second basin or a modern-forest application.
- **phage-mutation-hotspots** — 2026-08-14: new, ran in Sci/Tech. **Michigan State** (**Jasper Gomez**,
  **Christopher Waters**, **Jeffrey Barrick**) found repetitive DNA in phage **T2**'s *agt* gene acting as a
  contingency locus, mutating **thousands of times faster** than the rest of the genome; moving cholera's
  antiviral genes into *E. coli* showed phages routing around the defence within hours. Waters: "they are using
  these mutation hotspots to make a zoo." *Nature Microbiology*. Relevant to phage therapy. News again on a
  therapeutic result.

- **eclipse-2026** — 2026-08-13: **closed, and it led No. 9.** Totality crossed slivers of Greenland,
  Iceland, northern Spain and Portugal Wednesday evening, the first visible from **mainland Spain since
  1912**. Maximum totality was **under 2 1/2 minutes off Iceland's west coast** and about **a minute** by
  the time the shadow reached Iberia near sunset; Oviedo had close to **1 minute 48 seconds** (Euronews).
  Spain ran **350 official viewing areas**, deployed about **33,500 officers** and expected at least a
  **half-million extra visitors**; glasses sold out at pharmacies and temperatures topped **95 F**.
  **Cloudless over Spain and Portugal, overcast over much of Iceland**, sun **90%+** obscured in Britain.
  NPR, cross-checked on Euronews and PBS's photo set. **Spain's next two are Aug. 2, 2027 and Jan. 26,
  2028. Thread closes.**
- **colombia-earthquake** — 2026-08-13: **moved again and ran as No. 9's first World brief.** **265 dead**,
  attributed in the brief to President **Abelardo de la Espriella** speaking Wednesday evening, with
  **nearly 500 officially missing**. **This time the number is not disputed** — NPR, Al Jazeera and France
  24 all carry 265, which is the first day of this story that three readable outlets agree. Al Jazeera adds
  **3,500+ wounded**, **9,550+ homes destroyed**, **Pereira 83 dead and Cali 74**, a civilian database near
  **4,100** missing, **130 aftershocks**, **25,800+ families** affected, and that the search has entered
  what officials call its **"final phase."** Those are available if it needs a fourth day. **Still moving —
  re-check before citing.**
- **qusra-settler-siege** — 2026-08-13: new, ran as No. 9's second World brief. Settlers besieged
  Palestinian homes in **Qusra** from **Sunday**, throwing stones and cutting off food and water; US
  Ambassador **Mike Huckabee** called it a **"horrific act of terror"** — the paper's headline says "act of
  terror" and attributes it to the ambassador. Israeli troops evacuated **two members of an American
  Palestinian family** Thursday morning, dismantled **two** outposts and detained **one** Israeli; a mosque
  in the village was burned in a separate recent attack. NPR. **News again on charges, or on a US action
  beyond the statement.**
- **putin-kuril-visit** — 2026-08-13: new, ran as No. 9's third World brief. Putin visited **Iturup**
  (Etorofu), largest and southernmost of the Kurils, on Thursday — **his first visit** — after naval drills
  off **Sakhalin**, touring a fish plant, a hospital and a school and saying Russia is "not threatening
  Japan." PM **Sanae Takaichi** called it **"absolutely unacceptable"**; FM **Toshimitsu Motegi** called the
  islands "an inherent part of Japan's territory." The USSR took them in **1945**, deporting about
  **17,000** Japanese residents. Al Jazeera. **News again on a Japanese diplomatic step.**
- **longview-mine-co** — 2026-08-13: new, ran as No. 9's first statewide brief **and it is the live WV
  thread.** Monitors detected high carbon monoxide about **2:15 a.m. Wednesday** at **Allegheny Met's**
  Longview Mine at **Volga**, Barbour County; all miners evacuated with **no injuries**, and state and
  federal agencies responded. The company said it is working toward "safely resuming operations." The story
  **carried no miner count**, so none was printed. WV MetroNews. **News again on a cause finding, a
  citation, or the mine restarting.**
- **wv-assessment-scores** — 2026-08-13: new, ran as No. 9's second statewide brief. Assessment director
  **Vaughn Rhudy** told the state board that 2026 proficiency meets or exceeds **2019** overall: math
  **39.4%** against 38.7% in 2019, reading at or above 2019 across grades, **science flat**, and **grade 11
  reading down to 51% from 55%** — which Rhudy attributed to a national SAT School Day drop. Grade 11 math
  is **21%**, science **23.6%**, CTE occupational **70%**. Superintendent **Michele Blatt** pointed to a
  new middle-school initiative. WV MetroNews. **News again on the middle-school plan or county-level data.**
- **peoples-cartage-fire** — 2026-08-13: **moved and ran as the `mid_ohio_valley` line, eight days after
  this ledger first flagged the Aug. 13 town hall.** WVDA and WVDEP, with Peoples Cartage and federal
  agencies, analyzed **hundreds** of soil and water samples plus produce, vegetation and honey: **no
  combustion-related compounds in water**, low concentrations in some soil, residuals in produce
  "considerably below" health-concern levels, **nothing above federal action levels but some above state
  screening thresholds** — and the line printed both halves of that, not just the reassuring half. WVDA
  says no further measures are needed now. WV MetroNews. **The town hall itself is tonight, Aug. 13 — that
  is tomorrow's line if anything is said there.**
- **july-cpi** — 2026-08-13: new, ran as No. 9's first U.S. brief. Consumer prices **+0.1%** in July,
  **3.4%** year over year, down from **3.5%**, against a wage-growth pace of **3.2%**; gasoline **-2.9%**
  to a **$4.03** national average, shelter about **two thirds** of the monthly rise, food away from home
  **+0.3%**. Brent near **$90**. NBC News; CNBC's write-up (which **403s** this crawler) put September
  hike odds at **42%** on CME FedWatch. **NBC's own wage sentence is internally contradictory — "average
  hourly earnings dropped 0.2% year-over-year" alongside a 3.2% pace — so only the 3.2% ran.** News again
  at the August print in early September.
- **leavitt-departure** — 2026-08-13: new, ran as No. 9's second U.S. brief. **Karoline Leavitt**, 28,
  is leaving as White House press secretary; Trump announced it Wednesday on social media and said she will
  be "one of my top outside advisors." She cited her two young children and had recently returned from
  maternity leave. **No successor named.** PBS NewsHour. **A named replacement is the news.**
- **same-day-executions** — 2026-08-13: new, ran as No. 9's third U.S. brief. Tennessee, Alabama and
  Oklahoma each set an execution for **Thursday**, the first such convergence since **Jan. 7, 2010**
  (Louisiana, Ohio, Texas). **Eleven** states executed prisoners in 2025; six would have done so in 2026 if
  these proceed. NPR, also carried by Al Jazeera. **The victims' details were deliberately left out.**
  **Whether they were carried out is the follow-up.**
- **wafcon-2026** — 2026-08-13: **moved and ran as No. 9's first Sports brief.** **Malawi 3-1 Algeria** in
  Casablanca — **Tabitha Chawinga** twice, **Temwa Chawinga** in stoppage time, **Ikram Adjabi** for
  Algeria, with red cards for Algeria's **Morgane Belkhiter** (23') and Malawi's **Rose Kadzere**. **Cameroon
  beat Morocco on penalties after 0-0** before **19,000+** at Moulay Al Hassan Stadium. Malawi are ranked
  **153rd** and are in their **first** WAFCON. Al Jazeera. **The final is Sunday and is Monday's brief.**
- **messi-return-leon** — 2026-08-13: new, ran as No. 9's second Sports brief. **Leon 3-2 Inter Miami**
  knocked the 2023 champions out of the Leagues Cup; **Daniel Arcila** scored in the **50th and 83rd**,
  **Juan Pablo Dominguez** also for Leon, **Yannick Bright** and **Daniel Pinter** (42') for Miami.
  **Messi came on at halftime to a loud ovation at Nu Stadium**, his first appearance since his father
  **Jorge** died Saturday at **68**, hours after posting that he has doubts about how long he keeps
  playing. CBS News. **A retirement statement is the only thing that makes this news again.**
- **starlink-thermosphere** — 2026-08-13: new, ran in Sci/Tech. **Kyoto University** (corresponding author
  **Mamoru Yamamoto**) applied tomography to orbital-drag data from about **1,200** Starlink satellites at
  **482 km** to produce the first two-dimensional latitude-longitude density map of the thermosphere near
  **500 km**, consistent with ESA's **SWARM** satellites. *Earth, Planets and Space*, read via
  ScienceDaily; `source` names the institution, the convention since No. 4. News again on a collision-risk
  application.
- **webb-lion-nebula** — 2026-08-13: new, ran in Sci/Tech. JWST NIRCam and MIRI images of **NGC 2392**,
  the Lion Nebula, show dust concentrations and ionized gas around the central **white dwarf**; the shell
  is expected to disperse in about **10,000 years**. ESA/Webb release, image processing by **A. Pagan**
  (STScI), read via ScienceDaily. **No peer-reviewed paper is attached to it**, so it was written as an
  observation release, not a study.

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

- **treasury-yields-2026** — 2026-08-21: **new, and it led No. 17.** The **30-year Treasury
  bond** reached **5.3%** this week, its highest since **2007**, against **1.7%** in 2021.
  **David Lynch**, global economics correspondent for The Washington Post, told PBS NewsHour
  that companies have borrowed about **$500 billion** this year for AI infrastructure,
  competing with governments for scarce capital, and that the national debt passed
  **$40 trillion** this week — double a decade ago. Treasury Secretary **Scott Bessent**
  said **Wednesday Aug. 19** the government would increase buybacks of long-dated debt and
  expected yields to fall; stocks fell again **Thursday** as that relief faded.
  **30-year mortgages past 6.6% and heading toward 7%; auto loans following; housing starts
  down last month.** PBS NewsHour, cross-checked against Yahoo Finance (read).
  **`cnbc.com` and `thestreet.com` both 403 this crawler**, so the exact index point moves
  were not printed in the body — the stat strip carries the percentages from
  `out/stats.json`. **Fed Chair Kevin Warsh speaks at Jackson Hole next week; that is the
  news.**
- **uss-lincoln-deployment** — 2026-08-21: **it finally moved and the thread CLOSES.** The
  carrier has **left the Middle East** after **nine months**, about **three weeks** from San
  Diego with roughly **5,000** sailors and Marines; the Japan-based **USS George Washington**
  has arrived to relieve her. She sailed **Nov. 21, 2025**. CBS News. NPR ran a companion
  piece the same morning on the psychology of long deployments — **Armen Kurdian**, **Jack
  Stuster**, **Dr. Phillip Hunt** — against Acting Navy Secretary **Hung Cao** calling the
  coverage "dishonest" and Hegseth calling the conditions reports "overstated"; **that half
  was not printed**, because the news is the departure. Ran as No. 17's first U.S. brief.
  **News again only on the homecoming or a congressional inquiry.**
- **flock-backlash-2026** — 2026-08-21: **new, ran as No. 17's second U.S. brief, and it is
  the national half of a story this paper already carries locally.** NPR counted vandalism
  of Flock plate readers in **at least 36 states** and **100+ cities** that have switched
  cameras off or cancelled contracts; **5,000+** agencies use Flock and there are
  **130,000+** AI plate readers on U.S. streets. **Clare Garvie** (NYU Policing Project),
  **Jay Stanley** (ACLU) and Flock CEO **Garrett Langley** quoted; **25,000+** registered for
  DeFlock's National Week of Action. **NPR's piece does not mention West Virginia or
  Huntington.** The Herald-Dispatch separately carried "Flock announces changes amid
  backlash" on Aug. 20 — **not run, because the national brief covers it and the Huntington
  ordinance is its own forward-dated row (Aug. 24)**. Careful not to run all three at once.
- **congo-ebola** — 2026-08-21: **moved and ran as No. 17's lead World brief, its third
  appearance** (Nos. 1 and 11 before it). **2,476 dead of 5,208 confirmed cases**, a
  **47.5%** fatality rate reaching **70%** in harder-to-reach parts of North Kivu — up from
  **2,100 of 4,600** when No. 11 ran it. The movement is the vaccine: Congo gets **70,000
  Ervebo doses**, **20,000** into a **Phase 3 trial** of whether it works against
  **Bundibugyo** and **50,000** for frontline and health workers. Ervebo is licensed only
  for the Ebola virus strain; WHO says early lab and animal data suggest some protection.
  **Tedros Adhanom Ghebreyesus** called it "an important example of global solidarity in
  action." Transmission is believed to have started in the mining town of **Mongbwalu** as
  early as **February**; declared **May 15**; spreading about **three times faster** than the
  2014-16 West African epidemic. PBS NewsHour. **A trial result is the news.**
- **e1-settlement** — 2026-08-21: new, ran in No. 17's World section. Israel opened tenders
  for **more than 1,200** housing units in the **E1** project, of **at least 3,400** total
  across about **12 square kilometres**, connecting occupied East Jerusalem to **Maale
  Adumim** and cutting the West Bank's link to East Jerusalem. The **UK, France, Germany,
  Italy, the Netherlands, Canada and Norway** issued a joint statement calling it
  "unacceptable" and warning of "legal and reputational consequences," urging Israel to
  retract. Egypt's foreign ministry, Malaysian PM **Anwar Ibrahim** and the UN spokesperson
  also objected. Al Jazeera. **An Israeli response, or a named consequence, is the news.**
- **berlin-arms-cache** — 2026-08-21: new, ran in No. 17's World section. German security
  authorities found a professionally set-up depot holding **two live firearms** in a
  **Brandenburg** forest near Berlin. The **BfV** believes it is a Russian "dead letterbox"
  and suspects the weapons were for agents conducting "kinetic operations." **Sinan Selen**,
  head of the domestic service, has previously warned of assassinations targeting defence
  industry managers, exiled opposition figures and Ukraine supporters. **No arrests.** The
  Russian embassy did not answer; Moscow has called similar accusations conspiracy theories.
  Reported by NDR, WDR and Süddeutsche Zeitung, carried by Euronews. **An arrest is the news.**
- **wv-flood-recovery-aug16** — 2026-08-21: the Aug. 16 flooding thread has moved from rescue
  to **recovery bureaucracy**, which is where it stops being a lead and becomes notebook
  lines. Kanawha County debris pickup **Aug. 24 - Sept. 4**; **United Way of Central West
  Virginia** (president **Margaret O'Neal**, brought in by Charleston Mayor **Amy Shuler
  Goodwin**) ran about **150 sandwiches** Monday and Tuesday and is taking donations, with
  **WV 211** as the assistance line — **searched, opened and judged too soft for a line**.
  Also open on MetroNews and not run: Harrison County urging flood victims to log damage,
  Mount Hope recovering from creek high water. WV MetroNews, WSAZ. **A damage total, a
  federal declaration, or a WVDOH reopening list is what makes it a brief again.**
- **colorectal-screening-sweden** — 2026-08-21: new, ran in Sci/Tech. **Karolinska
  Institutet** and **Umeå University**, led by **Johannes Blom**: the Stockholm-Gotland
  programme, **376,511** participants, up to **14 years**, **1,668** colorectal cancer
  deaths in follow-up. Taking part cut mortality risk **43%**; being merely invited cut it
  **26%**. Stool test for occult blood, positive results to colonoscopy. *JAMA Network Open*,
  August 2026. `source` names the institution, the convention since No. 4.
- **grand-canyon-escarpment** — 2026-08-21: new, ran in Sci/Tech **and was nearly the
  drawing**. **University of Southampton** (lead author Prof. **Thomas Gernon**) with GFZ
  Helmholtz, Potsdam and Illinois Urbana-Champaign: a **~1 km** high "Great Escarpment of
  Laurentia," formed about **800 million years ago** in the breakup of **Rodinia**, stripped
  up to **8 km** of rock and exposed the canyon's basement about a billion years before the
  Colorado River — an explanation for the **Great Unconformity**. Spanned thousands of km
  across Arizona, Utah, Idaho, Wyoming, Colorado, Texas, Oklahoma, Arkansas, Missouri and
  Illinois. *Geology*, 2026. **A good rung-2 art subject if the lead is ever undrawable.**
- **quantum-droplets-monash** — 2026-08-21: new, ran in Sci/Tech. **Monash University**
  (PhD candidate **Sam Foster**, Assoc. Prof. **Jesper Levinsen**, Prof. **Meera Parish**)
  with Heidelberg: bosons and fermions in a resonant mixture can balance attraction against
  fermion pressure into a self-bound droplet, and the theory now extends to **strong**
  interactions where earlier work handled only weak ones. Says existing ultracold-atom labs
  could make one. *Physical Review Letters* 137(7), Aug. 21, 2026. **News again on an actual
  droplet in a lab.**

## 4. Recently covered

### 2026-08-21 — No. 17, and Sports & Sportsman No. 7
- lead: **treasury-yields-2026** — the 30-year bond at 5.3%, its highest since 2007, and
  mortgages past 6.6%. **RUNG 1 ART, and it was handed to the desk:** PBS's `og:image` for
  the piece is the entrance to the U.S. Department of the Treasury — three doors, two bronze
  roundels, an inscribed frieze and a broad flight of steps. No people, no faces, pure
  geometry. Drawn as `art/2026-08-21-lead.svg`, `placement: lead`, and it renders with the
  lead, before the U.S. section. **Only the second rung-1 drawing in a week; the lesson is
  to fetch the lead's og:image before assuming the lead is undrawable, because a building
  facade is the single most reliable subject on the list.**
- us: uss-lincoln-deployment (**it moved and the thread closes**), flock-backlash-2026,
  ca-14-special-election (**Aisha Wahab, first Afghan American in Congress, beat Melissa
  Hernandez; they meet again in November**)
- world: congo-ebola (**third appearance, and the vaccine is the movement**), e1-settlement,
  berlin-arms-cache
- wv statewide: marl-transmission-psc (**WV Public Broadcasting, deliberately not MetroNews,
  for source diversity — and the two disagree on the county list, so no count was printed**),
  bluefield-state-emergency-session
- wv regional: putnam_kanawha — kanawha-debris-pickup; mid_ohio_valley — ritchie-fema-centre
- wv away: **prince_george — pg-plane-crash. The first away line since Aug. 12, ending an
  eight-edition drought.** `ckpgtoday.ca` opened cleanly and is confirmed readable; **CBC's
  BC page 403s this crawler**, so CKPG is the Prince George outlet that works
- huntington_cabell: **line written, opened, sourced and CUT FOR BUDGET — fourth time.** The
  20th Street underpass closure. See `docs/FAILURES.md`
- nicholas_webster, summers_new_river: **no line.** Nicholas/Webster is on the **same three
  standing items** it has carried since Aug. 12 (the Aug. 23 DUI checkpoint, the Aug. 30 lake
  cleanup, the LUCAS screening unit); Summers/New River had nothing newer than a Bridge Day
  vendor announcement for **Oct. 17**. **Summers has now run dry every morning of this
  paper's life**
- scitech: colorectal-screening-sweden, grand-canyon-escarpment, quantum-droplets-monash.
  **All three came through ScienceDaily but `source` names the institution**, which is the
  convention and which also satisfies three bylines. `nature.com/news` now **303s to
  `idp.nature.com`** and needs an account; **`arstechnica.com` is unreachable from this
  pipeline entirely** — both are new losses worth remembering
- **fishing: both waters. Williams 350 cfs and falling, 2.55 ft**, against **755 cfs** 24
  hours earlier. The fetcher's read ran nearly verbatim: "pushy. Wadeable at the edges, not
  across." **No NOAA water temperature for a fifth morning**, so Topsail ran tides only
- **stocking: silent no-op.** Nothing named the Williams, the Cranberry or the Summersville
  tailwater. `wvdnr.gov` not fetched (expired certificate)
- **BUDGET: first pass projected 6,691; shipped at 5,574 projected.** Cut the lead's third
  paragraph, tightened every summary, and cut the Cabell line. **Then a second measurement
  showed 5,333 and the `mid_ohio_valley` line was put BACK** — worth recording, because the
  ladder is easy to over-apply: cut to the number, re-measure, and restore what fits
- **S&S No. 7 — teams that ran:** West Virginia (women's soccer, 2-1 over No. 23 Penn State,
  first win over them since 2017), Marshall (0-4 at High Point, Sabba Haghgoo hat trick),
  Cincinnati Reds (10-9 to St. Louis after a six-run third). **Sat out:** Ohio University,
  San Antonio Spurs, USMNT. **Accounted for by standings or fixtures:** Pirates, FC
  Cincinnati, Columbus Crew, Browns, Bengals, Chelsea, Tottenham, Liverpool
- **S&S — the football season starts tonight.** Arsenal v Coventry, 3 p.m. ET Friday.
  Liverpool open under **Andoni Iraola** and Chelsea under **Xabi Alonso** — both new
  managers, and **the first morning this paper has had a reason to say so**. From tomorrow
  the football beat is results, not fixtures. **Tottenham at Brentford Sat 12:30 p.m. ET,
  Liverpool at Newcastle Sun 11:30 a.m. ET, Chelsea at Fulham Mon 3 p.m. ET** — all three
  ET-converted from BST at plus five, all cited to Sky Sports because **`espn.com`'s fixtures
  story and `premierleague.com` both returned empty to this crawler this morning**
- **Do not re-run tomorrow without movement:** the USS Lincoln (**closed — only the
  homecoming**); Wahab; the E1 statement (**an Israeli response is the news**); the Berlin
  cache (**an arrest**); the Ebola doses (**a trial result**); the three science papers; the
  Kanawha debris schedule; the Ritchie FEMA centre. **The ones that should run: the WVU
  women against Duquesne Sunday 1 p.m.; the Premier League results from Saturday, which are
  the first of the season; and the Bluefield State board, whose emergency session announced
  nothing and is the most interesting unanswered question in the state this morning.**

### 2026-08-14 — No. 10
- lead: **hormuz-reopening**, its third front page — two ADNOC vessels attacked Thursday evening, the UAE
  calling it piracy, against Trump's "total control" claim and Iran's rejection of it. **Rung 1 art**, the
  second morning running: ships at anchor in haze with a tug standing by, drawn after looking at the Getty
  photograph on Al Jazeera's page — no coastline in the frame, which is why the drawing has none
- us: harvard-antisemitism-suit, same-day-executions (**the follow-up, and it closes**)
- world: europe-wildfires-2026, farage-clacton, taiwan-han-kuang
- wv statewide: ames-goldsmith-h2s, greenbrier-casino
- wv regional: mid_ohio_valley — peoples-cartage-fire, **second morning running, and a different fact each
  time** (Aug. 13 the state's sample results, Aug. 14 the independent tester's plume figures at the town hall)
- wv away: **none.** Vermont searched — Battle Day weekend Aug. 13-16 and the Hemmings Cruise-In, both standing
  events, no news; Prince George searched — the BCNE fair and two municipal-election campaign launches ahead of
  the **Oct. 17** vote, nothing dated hard enough for a line; Topsail carried by its fishing line
- sports: nigeria-womens-world-cup, swiatek-canadian-open, marshall-women-soccer
- scitech: oist-hibernation-memory, petm-forest-canopy, phage-mutation-hotspots
- huntington_cabell: **line written, opened, sourced and CUT FOR BUDGET for the second day running** — the
  Rahall Bridge nightly inspection closures. See `docs/FAILURES.md` and the Aug. 18-21 forward-dated row
- putnam_kanawha: **line written and cut** — Kanawha County Schools starting the **Signs of Suicide** program
  and student **Hope Squads** at George Washington, Herbert Hoover, Nitro and Riverside this fall, staff and
  parent training in September (WSAZ). **It pairs with `wv-child-fatality-report`, where Del. Margitta
  Mazzocchi pressed on school suicide prevention — worth running on a thinner morning**
- nicholas_webster, summers_new_river: **no line.** Nicholas/Webster is on the **same standing WVU LUCAS mobile
  lung-screening item for the sixth morning running** (Aug. 12-14); Summers/New River still has nothing newer
  than the NRGRDA director's June departure. **Summers has now run dry every morning of this paper's life**
- **fishing: both waters, and the Williams is dropping fast off the storm crest.** **208 cfs and falling,
  2.11 ft**, against **732 cfs** 24 hours earlier and No. 9's **335**. The fetcher's read ran nearly verbatim:
  "pushy. Wadeable at the edges, not across." **No water temperature from NOAA for the second day**, so Topsail
  ran tides only
- **sumo: sat out, eighth day.** Off-basho, two dedicated searches plus a fetch of the JSA's own English site,
  whose newest item is an **Aug. 5** museum-calendar update. The genuinely interesting fact — **Atamifuji's
  ozeki promotion run at Aki after 9 wins in May and 12 in July as sekiwake** — is carried **only** by
  sumostats, substacks and travel sites; `japantimes.co.jp` still **402s**. **Aki dates and the Aug. 31 banzuke
  are still uncitable**, ninth morning. Correct edition per Ian's rule
- **football: searched, nothing dated.** The clubs' business is real but stale: Liverpool's **Ronald Araujo**
  loan from Barcelona (option to buy about **47.14M pounds**, no loan fee) was announced **Aug. 10** and is
  four days old; Chelsea have spent about **408M euros** on 11 signings and Tottenham about **260M** plus frees.
  **Season opens Aug. 21** — the validator's in-season warning is expected until then
- **stocking: silent no-op.** Searched; nothing named the Williams, the Cranberry or the Summersville
  tailwater. `wvdnr.gov` not fetched (expired certificate)
- **BUDGET: 5,616 projected, 5,723 ACTUAL, single message, nothing trimmed.** **Write this number down:**
  the shipped payload ran **107 characters ABOVE** the validator's projection, because `--page-url` adds a
  content line the projection does not count. No. 8's note had the gap running the other way; **with
  `--page-url` being passed, assume the projection UNDERSTATES by about 100 and treat 5,600 projected as
  roughly 5,700 shipped.** That is still clear of the 5,800 ceiling, but a 5,750 projection would not be.
  Today's 5,616 was reached only after cutting a notebook line AND a wire brief.** The overspend is
  **URL cost, not prose** — see `docs/FAILURES.md` for the character counts. **This is the structural problem
  to solve, not a one-off:** the WV and science outlets this paper relies on publish 100-150 character URLs
- **Do not re-run tomorrow without movement:** the executions (**carried out; closed**); Harvard (**an appeal
  is the news**); Farage (**the donation inquiry is the news, not the result**); Swiatek; the Taiwan drill; the
  CSB findings; the Peoples Cartage plume figures. **The ones that should run: the WAFCON final Malawi v
  Cameroon on Sunday, which is Monday's Sports brief and has been promised since No. 6; the Greenbrier, whose
  refinancing was targeted to close Aug. 15; and the USS Lincoln relief, which is a finished U.S. brief sitting
  in the open threads above.**

### 2026-08-13 — No. 9
- lead: **eclipse-2026, the follow-up No. 8 could not carry** — what was actually seen, not the preview.
  Rung 1 art for the first time since No. 5: the crescent behind a church cupola, drawn after looking at
  the AP photograph on NPR's page (Vidigulfo, near Pavia, northern Italy, outside the path of totality)
- us: july-cpi, leavitt-departure, same-day-executions
- world: colombia-earthquake (**265, and cross-checked this time**), qusra-settler-siege, putin-kuril-visit
- wv statewide: longview-mine-co, wv-assessment-scores
- wv regional: mid_ohio_valley — peoples-cartage-testing
- wv away: **none.** Vermont searched (only the Battle Day schedule and an Aug. 11 update on a July
  shooting); Prince George searched (pool maintenance and the Oct. 17 local election, nothing dated);
  Topsail carried by its fishing line
- sports: wafcon-2026 (**final set**), messi-return-leon
- scitech: starlink-thermosphere, webb-lion-nebula
- huntington_cabell: **line written, opened, sourced and CUT FOR BUDGET** — see `docs/FAILURES.md`
- nicholas_webster, summers_new_river, putnam_kanawha: **no line** — Nicholas/Webster is on the **same
  three standing items for the fifth morning running** (Aug. 12-14 mobile screening, Aug. 23 checkpoint,
  Aug. 30 lake cleanup); Summers/New River had nothing newer than June beyond the NRGRDA director's June
  departure; Kanawha's only new item was MetroNews' **"biker killed by live electrical cable,"** which is
  **the same Pinch death No. 8 already ran** as its `putnam_kanawha` line, refined — not a second story
- **fishing: both waters, and the Williams is falling back off Tuesday's crest.** **335 cfs and rising,
  2.51 ft**, against **95.6 cfs** 24 hours earlier — but note that reading sits *below* No. 8's **767 cfs**,
  so the storm water is on its way out even though the fetcher's 24-hour comparison says "rising."
  The fetcher's read ran verbatim: "pushy. Wadeable at the edges, not across"
- **sumo: sat out, seventh day.** Off-basho, two dedicated searches. **`japantimes.co.jp` now returns HTTP
  402 to this crawler, which is new** — the Aug. 5 jungyo feature is no longer even openable. Aki dates and
  the Aug. 31 banzuke are **still** carried only by ticket-reseller and travel sites. **The kicker
  deliberately did not print Aug. 31**, because that date is not yet citable; it said only that sumo sat
  out. **Aug. 31 remains the hook.** Correct edition per Ian's rule
- **football: searched, nothing dated, and one near-miss worth recording.** A "done deals for 12 August"
  aggregator listed **Andy Robertson, Liverpool to Tottenham on a free** — two followed clubs at once, which
  would have been an automatic brief. **Sky Sports dates that announcement June 5, 2026.** It is ten weeks
  old. **Do not let it resurface as new.** Season opens Aug. 21
- **stocking: silent no-op.** Searched; WVDNR publishes after the fact and nothing named the Williams, the
  Cranberry or the Summersville tailwater. `wvdnr.gov` was not fetched (expired certificate)
- **BUDGET:** validator projected **5,412** after two tightening passes, against No. 8's measured
  projection-to-actual gap of about **215**. Aiming at 5,400-5,500 is what keeps this a single message
- **Do not re-run tomorrow without movement:** the eclipse (**it is over; the next is Aug. 2, 2027**); the
  July CPI print (**the August one lands early September**); Leavitt (**a named successor is the news**);
  the executions (**whether they were carried out is the news**); the Kuril visit (a Russian or Japanese
  follow-up is the news); the mine evacuation (**a cause finding or a resumption is the news**); the
  assessment scores; the Peoples Cartage testing (**the Aug. 13 town hall itself is tonight — that is
  tomorrow's line**); Malawi-Cameroon (**the final is Sunday and should run Monday**); Messi. **The one
  exception that should run: the Colombia toll, which is still moving, and the search is now in what
  officials call its final phase.**

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
  hook.** Correct edition per Ian's rule. **2026-08-13: `japantimes.co.jp` now returns HTTP 402 as well, so
  the Japan Times sumo section is no longer openable either — the readable-source list for sumo is down to
  NHK, Kyodo and the JSA's own English pages**
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

---

### 2026-08-15 — No. 11, and Sports & Sportsman No. 1 (written, not posted)

- **flores-earthquake** — new, led No. 11. **Magnitude 7.7** off **Flores**, Indonesia at
  **5:58 a.m.** local Saturday, **68 km north-northwest of Ende** at **10 km** depth (USGS).
  **At least 20 dead, six injured**, per **Fathur Rahman**, head of the Maumere search and
  rescue agency. **Eight bodies from a landslide at Reok village**; buildings down across
  **Sikka, West Manggarai and East Manggarai** regencies; landslides in **Ende regency cut the
  Trans-Flores highway**, the **700 km** road spanning the island; about **2,000** villagers in
  **Nagekeo** regency in shelters. **BMKG** issued a tsunami warning and lifted it after no
  significant sea-level change. Aftershocks **6.1, 5.9, 5.6** within 30 minutes. USGS estimated
  **500,000+** felt very strong shaking. Cross-checked **Al Jazeera** and **NPR/AP**. Al Jazeera
  has "two trapped under rubble in Maumere" where NPR has "two missing in a landslide" — **that
  detail was dropped rather than reconciled.** **Toll will move; re-check before citing.**
- **mangione-federal-plea** — new, No. 11's first U.S. brief. Pleaded guilty **Friday** in
  Manhattan federal court to **two stalking counts** in the Dec. 4, 2024 killing of
  UnitedHealthcare CEO **Brian Thompson**; two counts including murder by firearm, which carried
  the death penalty, were **dismissed earlier this year** and prosecutors will not appeal.
  **Sentencing Dec. 18**; no parole in the federal system and 85% of any sentence must be served.
  Defence counsel **Karen Friedman Agnifilo** immediately moved to dismiss the **state** case on
  New York double-jeopardy grounds; **that state trial is set for September and is the news.**
  CBS News.
- **white-house-ballroom** — new, No. 11's second U.S. brief. DOJ asked the **Supreme Court**
  on Aug. 14 to stay a **D.C. Circuit** injunction of **Aug. 7** halting the **$400M** East Wing
  ballroom unless Congress approves it; the panel wrote that "whether or not a massive ballroom
  should be constructed is for Congress to decide." **Work stops Aug. 21** absent a stay. Suit
  brought by the **National Trust for Historic Preservation** in December. Al Jazeera.
  **A ruling on the stay is the news.**
- **haitian-tps-ohio** — new, No. 11's third U.S. brief and the Ohio Valley angle on it.
  Haitians in **Springfield, Ohio** who lost **Temporary Protected Status** in July have been
  summoned to an ICE facility to be fitted with **ankle monitors**; **ICE has not said why**.
  **Viles Dorsainvil**, executive director of the Haitian Support Center, is the named source.
  NPR via WYSO, Aug. 13. **News again on a removal, or on an ICE explanation.**
- **drc-ebola** — new, No. 11's first World brief. **4,600+ confirmed cases, at least 2,100
  dead**, **Bundibugyo** strain — a variant with **no approved vaccine or therapeutic** that
  kills 25-50%. Began February, declared May, eastern Congo around **Bunia**, a new province
  added Aug. 13. **Tedros Adhanom Ghebreyesus**: "It's already the second biggest Ebola epidemic
  on record. And it's moving faster than any previous Ebola outbreak." **Dr. Anne Rimoin**
  (UCLA) quoted. PBS NewsHour. **The 2014-16 West African outbreak killed 11,000+ — that is the
  benchmark it is being measured against.** Live and moving.
- **europe-wildfires-2026** — **moved and ran again as No. 11's second World brief**, one day
  after No. 10 carried it, because the ledger's own trigger fired: **a death.** A charred body
  was found at **Omis**, Croatia; **40** treated at Split with **at least seven** serious;
  **2,000** left coastal villages; fire chief **Slavko Tucakovic** called it "one of the worst in
  Croatia's history." Also **19 hospitalised and 20-30 homes destroyed at Stourbridge** in the
  West Midlands (MP **Cat Eccles**), **1,800** evacuated at **Gey**, Germany, **525** from
  **Luglon** in the **Landes** where **1,100 hectares** have burned since Thursday with **500
  firefighters and six aircraft**, and **300+** taken off the beach by boat at **Siviri**,
  Greece. **500,000 hectares** EU-wide this year. Al Jazeera. **News again on a national
  emergency declaration or an EU civil-protection deployment.**
- **hormuz-reopening** — **moved and ran as No. 11's third World brief**, its fourth appearance.
  Trump, in **New York on Friday**: "After we finish defeating Iran, which is being very badly
  defeated, pretty soon I'll be declaring the Hormuz Strait a territory of the United States."
  Iran's deputy foreign minister for legal and international affairs **Kazem Gharibabadi**: the
  strait "cannot be taken over by a tweet, nor by an aircraft carrier, nor by issuing a decree."
  Al Jazeera adds the war began **Feb. 28**, a ceasefire memorandum was signed **June 17** and
  both sides claimed violations by month's end; **Scott Bessent** signalled new economic
  measures; a late-July **Quinnipiac** poll had **60%** of US voters opposed to military action.
  **News again on an actual declaration, an Oman corridor deal, or a seizure.**
- **wv-storm-emergency** — new, No. 11's first statewide brief **and the live WV thread.**
  Morrisey extended the **July 21** storm State of Emergency in **12** counties — Barbour,
  Doddridge, Harrison, Lewis, Pendleton, Pleasants, Randolph, Ritchie, Tucker, Tyler, Upshur and
  Wetzel — **through Sept. 19**, while it **expires Aug. 20 in 43 others**. About **1,300 Upshur
  homes**, roughly **10%** of the county, were hit. Federal disaster declarations cover
  **Upshur, Lewis, Ritchie and Pleasants**; recovery centres open at **Weston and Buckhannon**;
  county EM director **Steve Wykoff** says most residents have finished debris removal. WV
  MetroNews. **News again on the Aug. 20 expiry in the other 43, or a new declaration.**
- **greenbrier-casino** — **moved and ran as No. 11's second statewide brief**, the ledger's
  Aug. 15 forward-dated row arriving. Lottery acting director **David Bradley** released a
  letter Friday replying to Justice counsel **Steve Ruby**: approval of the new key members
  "remains pending and cannot be completed without a properly noticed meeting and vote of the
  Commission," and the casino **could keep operating** if the Justice side supplies "a sufficient
  plan that appropriately walls off the holding company." About **90** jobs are at stake and
  employees have **WARN** notices with a 60-day pay-and-benefits period. **Bradley told counsel
  on July 10** the review was unlikely to finish before the **Aug. 26** regular meeting. WSAZ.
  **The outlets still disagree on the filing day and the Volk deadline, so no filing date has
  ever been printed.** **An actual closure, or the Aug. 26 vote, is the news.**
- **lubeck-psd-rates** — new, and it is **the only regional line No. 11 could source.** About
  **25** people came to Thursday's Wood County Commission hearing on Lubeck PSD's proposed **30%**
  water and **14%** sewer increase; the district serves **over 4,900** customers including six
  industrial ones. **Kevin Watkins** (Thrasher Group) said the plant "is almost at capacity";
  Commissioner **Jimmy Colombo** and Commission President **Blair Couch** ("I have never heard
  from anyone who said their water is bad or undrinkable") pushed back; PSD manager **Rocky
  McConnell** quoted. Parkersburg News and Sentinel. **Vote 9:45 a.m. Monday, Aug. 17.**
- **wvu-women-soccer** — new, ran in No. 11's Sports and in Sports & Sportsman No. 1.
  **No. 20 West Virginia 2-0 Dayton** at **Dick Dlesk Soccer Stadium** Thursday — **Sophia
  Nickel at 45:54**, 54 seconds into the second half, and a Dayton **own goal at 63:00** off a
  **Maya Leoni** corner. Coach **Nikki Izzo-Brown**: "First game, you hope for 90 minutes of
  perfection. The good thing is we won in 45 min." First of **10** home matches. WV MetroNews.
  **Note this was corrected mid-run: it is the WOMEN's team. The men open Aug. 20 at Charlotte** —
  and `docs/FAILURES.md` records that the men's opener was the brief lost to MetroNews'
  interstitial on 2026-08-14, so the two are easy to confuse. Do not repeat the mix-up.
- **sumo-off-basho** — the daily sumo search ran and **found something for the first time in
  days**, from the JSA's own English page rather than a reseller: the **summer regional tour
  (jungyo) is at Akita** on Aug. 15, and the **September Tokyo tournament is listed sold out on
  every date**. No. 2 printed the Aug. 8 on-sale date; **the sellout is the new fact, not a
  re-run of that one.** **`sumo.or.jp/En/` still does not print the Aki dates** — Sept 13-27
  remains **derived and unconfirmed**, carried only by ticket and travel sites this paper will
  not cite. **The Aug. 31 banzuke release is still the moment a citable outlet must print them.**
- **mlb-aug-14** — Reds **1-0** over Miami (**Chase Burns** to **14-2, 2.47**; **Sandy
  Alcantara** to 13-7) and Pirates **8-4** over Boston (**Bubba Chandler** to 6-8; **Jake
  Bennett** to 7-6), from **mlb.com/scores**, opened twice. Also Cubs 3-0 Cardinals and Astros
  10-7 Mariners in 10. **`docs/FAILURES.md` records an aggregator that had the Reds beating the
  White Sox 9-8 the same day — it had merged two games.** Primary source won.
- **hunter-greene-surgery** — **searched, real, and deliberately NOT run.** Reds ace **Hunter
  Greene** had a **second Tommy John surgery** Wednesday, ending 2026 and likely all of 2027.
  Every route to it failed: `mlb.com`'s own article returned **HTTP 406** and the rest were
  aggregators. **It would have been the strongest Reds line in Sports & Sportsman No. 1 and was
  dropped rather than written from a search snippet.** **Open it tomorrow and run it** — it is
  still news a week from now.
- **premier-league-preseason** — all three followed clubs are in their **final friendlies**
  before the **Aug. 21** opener: Chelsea beat **AC Milan 3-0** Aug. 8 and drew **3-3** with Johor
  Darul Ta'zim Aug. 9, and host **Real Sociedad** Aug. 15; Tottenham drew **1-1** with Getafe and
  take **Hoffenheim** Aug. 15 and 16; Liverpool lost **3-2** to Monaco Aug. 9 and meet **Como**
  Aug. 16. premierleague.com. **The ledger's Aug. 8 Chelsea-Milan row is now spent.**
  **The Aug. 21 opening weekend is the first real football of the season for both papers.**
- **nc-coastal-limits** — confirmed **today** off NCDMF's own HTML table and printed in Sports &
  Sportsman No. 1: **flounder CLOSED and unlawful to possess**; **red drum** 18-27 in. TL, 1/day,
  no gigging or spearing; **spotted seatrout** 14-20 in. slot with one over 26 in., 3/day;
  **sheepshead** 14 in., 5/day. **The fall flounder opening was NOT printed**: the only dates
  available were **NCWRC's** (the inland agency, wrong water) and DMF proclamation
  **FF-27-2026**, which is **PDF-only and unreadable to this pipeline**. The DMF page that works
  is the canonical one, **not** the `/open` variant, which serves a PDF. **Re-confirm the limits
  each time; do not carry these forward from this ledger.**
- **stanford-brain-immunity** — new, ran in No. 11's Sci/Tech. Stanford (**Julia Belk** first
  author, **Siddhartha Jaiswal** senior, **Howard Chang** co-senior) traced somatic mutations in
  paired blood and post-mortem brain tissue and found blood immune cells crossing into the brain
  from **middle age** and becoming **microglia**, overturning the assumption that microglia are a
  self-sustaining population set at birth. **Absent in mice and non-human primates** — a human
  feature. *Nature*, **Aug. 14**. `source` names the institution, the convention since No. 4.
- **estrogen-dementia** — new, ran in No. 11's Sci/Tech. Across **21,462** women, estrogen-only
  menopausal hormone therapy users had **39%** lower odds of a dementia diagnosis and **35%**
  lower odds of Alzheimer's pathology at autopsy. **Neurology**, **Aug. 12**; senior author
  **Hadi Hosseini**. **The authors' own limitation — association, not causation — ran in the
  brief**, because this is exactly the kind of health finding a reader acts on.
- **double-chooz-antineutrinos** — **written and then cut for budget and age.** The Double Chooz
  collaboration measured residual antineutrinos from a shut-down reactor at **Chooz**, France —
  about **100** candidate events over **17.2 days** with both cores off, **Physical Review
  Letters, Aug. 4**, quoted **Anthony Onillon** and **Thierry Lasserre** (MPIK). At 11 days it
  was the oldest thing in the paper and it lost the third Sci/Tech slot. **Spent — do not run it
  next week as if it were new.**

**Run notes for tomorrow.** `config.head_start_minutes('2026-08-15')` returns **90**, not 60,
and that is **correct now** — the two-paper morning moved the wake to **5:30** and
`config.cron_for()` returns `30 9 * * *` to match. The edition.md text that says the head start
"should be 60" predates the second paper; it is not a daylight-saving fault and needs no
`FAILURES.md` line. **The 90 minutes were genuinely needed**: research ran about 20 minutes and
the two papers were built inside it with room left, but only because the sportsman paper never
reached validation, rendering or posting. **When the pipeline exists, budget for those three
steps on top.** Also: an early clock-check is worth doing on purpose — this run spent its first
twenty minutes believing it was far later than it was, and nearly shipped a thinner Times
because of it. Read the clock before deciding anything is late.

---

## 2026-08-18 — No. 14 and Sports & Sportsman No. 4

| Open-ended | **WV MetroNews is behind a bot check and this is a source outage, not a story shortage.** Every `wvmetronews.com` fetch this morning returned the Cloudflare verification interstitial. The paper's best statewide daily is currently unreadable to this crawler, and it cost a real story: **Charleston Mayor Amy Shuler Goodwin declared a municipal State of Emergency after Sunday's flooding**, carried by MetroNews and by nobody else this desk could open, so **it did not run**. WCHS, WVPB, WSAZ, the Herald-Dispatch and the Parkersburg News and Sentinel all opened normally and carried the edition. `wowktv.com` 403s. **If MetroNews is still walled tomorrow, that is the fact to report, and West Virginia Watch and WVPB become the statehouse spine** | **OPEN — check MetroNews first thing** |
| Open-ended | **The stored prompt still says Sports & Sportsman is on its first edition. Fourth morning running.** Today's prompt again read "THIS IS SPORTS & SPORTSMAN'S FIRST EDITION. It is Vol. I, No. 1 of that paper," and again also said to **number it from its own ledger**. `editions/sportsman/index.json` carried Nos. 1, 2 and 3, all posted, so **No. 4 is what shipped**. Flagged for Nate on 08-16 and again on 08-17; still unedited. The "extra care a first issue deserves" line is now three editions out of date | **OPEN — for Nate, third reminder** |
| Open-ended | **The clock was read, not estimated — and the drift happened anyway, early.** `config.head_start_minutes('2026-08-18')` returned **90** and `config.cron_for()` returned `30 9 * * *`, the cron actually installed; neither daylight-saving row has come due. **Mid-research the desk believed it was 6:11 ET when `TZ=America/New_York date` said 5:41** — a 30-minute overestimate, the same direction and the same error logged on 08-13, 08-14, 08-16 and 08-17. It was caught by running `date` before a scheduling decision rather than counting tool calls, which is the fix that keeps working. **Both papers were built, validated, rendered and pushed by 5:50, seventy minutes before the first hold released** | **OPEN — read the clock, do not estimate it** |

### Forward-dated rows closed today

| **2026-08-18** | **Marshall v Ohio women's soccer — CLOSED, and the answer is that it was never played.** The row sat open three mornings because no outlet would give a result. `herdzone.com` published **"Herd Women's Soccer's Contest With Ohio Postponed"** on Aug. 16: **thunderstorms in the Huntington area** called the match off before kickoff. It ran as Sports & Sportsman No. 4's third Our Teams brief, covering both followed sides. Marshall next play **Thursday at High Point**. No make-up date was announced. **The lesson for the next owed result: search for the postponement, not only for the score** | **CLOSED** |
| **2026-08-18** | **Wood County Commission voted on the Lubeck PSD increase — CLOSED.** Commissioners **Jim Hamric, Jimmy Colombo and Blair Couch** approved a two-phase rise unanimously Monday, well under the **30% water / 14% sewer** originally sought: **18% water and 8% sewer in September**, then **12.22% water and 6.03% sewer** a year later, both calculated on current rates rather than compounded. The district serves about **4,900** customers and cited treatment chemicals going from **$65 to $245 a barrel** in five years; Couch asked for a progress report in six months. Parkersburg News and Sentinel. Ran as No. 14's only regional line. **Martin's retirement from the PSD is still unpinned and still unrun** | **CLOSED** |

### Standing rows checked and left open

- **Nucor Apple Grove sheriff's detail (~Aug. 17).** Searched this morning across MetroNews (walled), WSAZ, the Herald-Dispatch, WCHS and the Gazette-Mail. **Nothing dated past the Aug. 7 closure announcement** — no arrest, no reopening, no second closure, and no report of the 10-day detail ending. Carried forward, unresolved, for the second morning.
- **Aki basho dates, still unconfirmed — fifth morning.** Searched again. The **Sept. 13-27 Ryogoku Kokugikan** dates remain available only from ticket resellers, travel sites and fan databases, which this paper does not cite. **Sumo sat out Sports & Sportsman for a fourth straight edition**, which is the correct edition under Ian's rule and not a miss. The **Aug. 31 banzuke release** is still the load-bearing date.
- **The four-brief wire target versus `config.EMBED_BUDGET`.** Hit the wall again — see `docs/FAILURES.md`. Sci/Tech ran three.

## Open threads — 2026-08-18

- **iran-mou-expiry** — **new, and it led No. 14.** The **60-day** deadline in the **June 17, 14-point** U.S.-Iran memorandum expired **Monday** with no talks under way. Terms: ceasefire on all fronts, U.S. naval blockade lifted within 30 days, sanctions relief and frozen funds released, **$300B** reconstruction, Iran to clear mines from the Strait of Hormuz and permit 60 days of safe passage, and no nuclear weapons. It broke on **Article 5** — Iran required vessels to hug its own coast, the U.S. and Oman favoured the other route, and Iran fired on ships taking it. Timeline: **June 25** the *Ever Lovely* struck; **June 27** U.S. retaliatory strikes; **July 7** Trump declared it "over"; mid-July strikes on what Tehran called civilian infrastructure killed about **50**. **Esmaeil Baghaei** (Iranian foreign ministry): no talks were ever initiated because of "gross and widespread violation" by the U.S. **Joey Hood**, former acting director of the Office of Iranian Affairs, called it "doomed to fail" and "very poorly written." Iran wants the blockade lifted, U.S. forces withdrawn and reparations for damage since **Feb. 28**; Trump wants Iran to pay reparations instead. **Pakistan** (spokesman **Tahir Andrabi**) is trying to revive talks: "We are not closing the chapter." Al Jazeera cross-checked against PBS NewsHour. **An extension, a Pakistani-brokered meeting, or a vessel seized is the news.**
- **gaza-road-map** — **moved and is now a World brief, not the lead.** Kushner's meetings with Netanyahu and Hamas **closed without significant movement**. Netanyahu's office called Monday's hours-long meeting "deep and constructive" and both sides agreed **no reconstruction before Hamas fully disarms**; an Israeli official said the first step is Hamas handing weapons over under American military supervision. **Working groups on disarmament and public health** were set up, and Kushner told Fox News weapons removal could begin "in as little as 30 days." Netanyahu, seeking re-election in **October**, still rejects the 15-point plan Hamas accepted. Foreign ministers of **eight** nations including Turkey, Egypt and Saudi Arabia condemned the rejection as "an explicit refusal." Euronews. **A working-group result or an Israeli signature is the news.**
- **wv-flooding-aug16** — **moved, and it now has a death.** A **woman drowned in the Pax area of Fayette County** when her vehicle was swept away during Sunday's flash flooding — the first fatality; No. 13 correctly printed none because none had been reported. The **Kanawha County Commission** is asking residents to file the **WVEMD Weather Damage Survey** (`emd.wv.gov/disastersurvey`), which is explicitly **not** an aid application. The **Kanawha-Charleston Health Department** is offering free hepatitis A and tetanus shots to flood victims. Two homes on **Fourth Avenue in Montgomery** lost their back yards to a wall collapse. WCHS, WVPB, WSAZ. **NOT PRINTED and still owed: Charleston's municipal State of Emergency, declared by Mayor Amy Shuler Goodwin** — MetroNews alone had it and MetroNews would not open. **A damage total, a federal declaration, or a second outlet on the city emergency is the news.**
- **wv-july-flood-recovery** — **new, ran as No. 14's second statewide brief.** Gov. **Patrick Morrisey** advanced **$400,000** from the **Civil Contingent Fund** Monday to move **Robert L. Bland Middle School** in Weston and its roughly **400** students to **WVU Jackson's Mill** for the year, rather than run the year virtually; in-person classes resume **after Labor Day**. The school was damaged in the **July 21** storms. The state expects FEMA reimbursement. **Lewis and Upshur** received major disaster declarations **Aug. 4**; **782** residents had registered for Individual Assistance with over **$3.1M** approved. West Virginia Public Broadcasting. **A FEMA reimbursement figure or a second school is the news.**
- **williams-river-flood** — **receding, then rising again.** USGS 03186500 read **1270 cfs and 4.15 feet at 5:15 a.m.**, down from **4620 cfs / 7.55 ft** yesterday but **up from 150 cfs / 1.88 ft** 24 hours ago and trending **rising**. Still "blown out. Stay on the bank." **The Ohio moved harder than the Williams: Point Pleasant 30.77 ft (from 25.17), Huntington 35.04 ft (from 27.34) — up nearly eight feet in a day, the biggest single-day move either gauge has made this month.** Both papers carried it and it was the Times kicker. **Watch for the Williams back under about 300 cfs; that is when the sportsman paper has wadeable water again.**
- **fbi-headquarters-move** — new, led No. 14's U.S. section. **U.S. District Judge Theodore Chuang** (D. Md.) blocked the relocation to the **Ronald Reagan Building**, finding in a **47-page** opinion that diverting the funding and cancelling the 2023 **Greenbelt, Maryland** plan was "arbitrary and capricious and not in accordance with law." Maryland sued in **November** over more than **$323M** Congress had designated. Maryland AG **Anthony G. Brown** said the court "cleared the path back to Greenbelt"; an FBI spokesperson said the court "chosen to impermissibly intervene for political reasons." CBS News. **An appeal is the news.**
- **mangione-double-jeopardy** — new, ran in No. 14's U.S. section. **Judge Gregory Carro** cancelled the **Sept. 8** state murder trial indefinitely while the defence argues double jeopardy after Mangione's **federal guilty plea** to stalking charges last week. Manhattan DA **Alvin Bragg**'s office has until **Oct. 9** to respond; hearing **Dec. 10**; federal sentencing **Dec. 18**. New York's double-jeopardy protections are unusually strong. **NPR and PBS copy both say "Tuesday, August 17," which is a Monday, so the brief said "Monday" and printed no date** — the same dating slip the ledger logged on 08-17. PBS NewsHour. **A ruling on the motion is the news.**
- **nfa-lapse** — new, ran in No. 14's U.S. section. **Judge James Wesley Hendrix** (N.D. Tex.) invalidated core parts of the **1934 National Firearms Act**, holding that Congress zeroing out the **$200** transfer and making tax in the 2025 One Big Beautiful Bill Act "eliminated the constitutional basis" for registering suppressors and short-barrelled rifles. **It binds only the plaintiffs** — Gun Owners of America and the Silencer Shop Foundation — across more than a dozen states. DOJ let the one-week emergency-appeal window pass and has over a month for a standard appeal. **Erich Pratt** of GOA called it "truly one of the greatest Second Amendment victories in the last 100 years." Parallel cases run in **Missouri and Kentucky**. NPR. **A DOJ appeal or a nationwide extension is the news.**
- **uss-lincoln-deployment** — **moved for the third time and ran again.** **Sen. Mark Kelly** (D-Ariz.), a former Navy combat pilot on Armed Services, told NPR's Morning Edition he wants a formal investigation of conditions aboard, recounting a sailor's grandmother saying her grandson had lost **20 to 25 pounds**. He and others want a **bipartisan congressional delegation** aboard. The carrier is now **nine months** out; the **USS George Washington** is to relieve her. NPR. **The delegation actually going, or the relief happening, is the news.**
- **flores-quake-2026** — **moved again: toll 68**, from 51 when it led No. 12. More than **200** injured, **1,576 aftershocks** by Monday, a **14-day** provincial emergency. **PBS and Al Jazeera disagree on displacement (about 19,000 vs 12,800) and homes damaged (4,500+ vs 1,300+), so neither number was printed** — the granular-figure rule. Both agree on magnitude **7.7**, **10 km** depth, Saturday morning, East Nusa Tenggara. Indonesia marked its **81st Independence Day** two days after. A **1992** Flores quake killed about **2,500**. PBS NewsHour. **Expect the toll to keep moving; re-check before citing.**
- **zambia-election-2026** — **CLOSED. Declared.** Electoral commission chair **Mwangala Zaloumis** declared **Hakainde Hichilema** re-elected on **Tuesday** with **61.4%** to **Brian Mundubile**'s **38%**, on about **5 million** votes. It was Hichilema's **seventh** presidential bid. **11 people including opposition figures were arrested** over the election-night armed raid, and counting was suspended over violence against polling staff. EU observers: the vote "took place in an environment that limited fundamental freedoms." Al Jazeera. **Thread closes unless the result is challenged in court.**
- **europe-drought-2026** — new, ran in No. 14's World section. The European Commission's **Joint Research Centre** reported **record lows on the Loire, Po, Rhine and Danube**. About **half** of Europe's land area is in drought, **9%** at alert level. The **Rhine at Cologne** hit **68 cm** on Saturday, one centimetre under the **October 2018** record; shipping halted at the **Kaub** bottleneck and vessels ran light. England had **6.5mm** of July rain, **10%** of average and its driest July since **1836**. Al Jazeera's Open Source Unit, from SkySat imagery. **A navigation closure or an EU response is the news.**
- **iss-z1-spacewalk** — new, ran in Sci/Tech **and it was today's drawing** (`art/2026-08-18-scitech.svg`, placement `scitech` — the first non-`wv`, non-`lead` placement since Aug. 10, and it beat falling to the river a third time in four days). NASA's **Anil Menon** and ESA's **Sophie Adenot**, Expedition 75, set spacesuits to battery at **8:35 a.m. ET Tuesday** for a planned **six-and-a-half-hour** walk to swap a high-speed data antenna on the **Z1 truss** for a spare from an external stowage platform. **Jack Hathaway** and commander **Jessica Meir** run Canadarm2 from inside; Menon rides the arm, Adenot stays tethered. NASA. **Whether it completed, and in what time, is tomorrow's line.**
- **vacuum-birefringence** — new, ran in Sci/Tech. **Swinburne University of Technology** (**Dr. Marcus Lower**; Stewart et al.) found X-ray polarization from magnetar **1E 1547.0-5408** matching **vacuum birefringence**, the effect **Werner Heisenberg** predicted about 90 years ago in which virtual particles in empty space bend light. Polarization degrees of **40%** and **80%** in different emission cones, from NASA's **IXPE**, **NICER**, and CSIRO's **Murriyang** (Parkes) radio telescope, analysed on the **Ngarrgu Tindebeek** supercomputer. *Nature*, **Aug. 18**, DOI 10.1038/s41586-026-10859-z. `source` names the institution, the convention since No. 4. **News again on a second magnetar.**
- **in-planta-proteomics** — new, ran in Sci/Tech. **North Carolina State University** (**Anna-Katharina Garrell**, **Manuel Kleiner**): **seven** corn-root bacterial species shifted **thousands of proteins** on contact with living roots versus lab culture — some becoming mobile, others attaching and going still, with secretion systems and phosphate solubilisation switching on. Garrell: "what you find in the lab is not necessarily what's going to be happening in the real environment." *mSystems*, **Aug. 17**, DOI 10.1128/msystems.00371-26. **Thread closes unless contested.**
- **premier-league-opening** — the football beat turns live Friday. **Arsenal v Coventry City** opens the season **Friday**; **Brentford v Tottenham** Saturday, **Newcastle v Liverpool** Sunday, **Fulham v Chelsea** Monday. Confirmed on `premierleague.com`'s own 380-fixture list, which opened cleanly when the club and match pages did not. **British kick-off times were printed as British times and labelled BST, because the fixture list publishes them that way and this desk will not convert a time it cannot cite.** From Friday, Our Teams carries results.

### Delivery, 2026-08-18

Both papers landed **exactly on their holds**: the Times at **7:00** (No. 14, message `1539227363357884470`, 1 message, 5,769 embed chars, hero attached, link live) and Sports & Sportsman at **7:05** (No. 4, message `1539228620575215710`, 1 message, 4,013 chars, link live). **`degraded` is empty on both records** — no split, no missing link, no trimmed brief. `post_discord.py` reported holds of **70** and **75** minutes, which is the head start working as designed: both papers were finished, validated, rendered and pushed by **5:50**, and both permalinks went green **45 seconds** after the push, so both posts carried `--page-url` at launch and no backfill was needed. **The research is not outrunning the head start; it finished with 70 minutes to spare.**

## 2026-08-19 — No. 15 and Sports & Sportsman No. 5

| Open-ended | **WV MetroNews is READABLE again, and it immediately paid.** Yesterday's row logged every `wvmetronews.com` fetch returning the Cloudflare interstitial. **This morning the wall was down on the first attempt**, and MetroNews carried the day's biggest West Virginia story — **Morrisey's state of emergency in all 55 counties** — which led the notebook, plus the Sugar Creek flood detail that became the `putnam_kanawha` line. **The outage was transient, roughly 24 hours. Do not narrow the outlet list on the strength of one bad morning**, and keep checking it first | **CLOSED — transient, one morning** |
| Open-ended | **The stored prompt still says Sports & Sportsman is on its first edition. Fifth morning running.** Today's prompt again read "THIS IS SPORTS & SPORTSMAN'S FIRST EDITION. It is Vol. I, No. 1 of that paper," and again also said to **number it from its own ledger**. `editions/sportsman/index.json` carried Nos. 1-4, all posted, so **No. 5 is what shipped**. Flagged for Nate on 08-16, 08-17 and 08-18; still unedited. The "extra care a first issue deserves" line is now four editions out of date | **OPEN — for Nate, fourth reminder** |
| Open-ended | **`validate_edition.py` cannot pass a correct WV migratory bird date, and that is now blocking real content.** The 2026-27 dove, snipe and rail seasons were confirmed this morning from two independently dated 2026 outlets and **still could not print**, because the validator checks every WV season date against `reference/wv-hunting-2026-27.json` and migratory birds are deliberately not in that table. See `docs/FAILURES.md`. **The fix is a code or reference change for Nate — a migratory bird section in the reference file, or a validator that knows those dates live in a separate publication.** The desk cut the entries rather than working around the gate, which is the right call but costs the reader the one WV season date that actually opens next month | **OPEN — for Nate** |
| Open-ended | **The four-brief wire target versus `config.EMBED_BUDGET`, fourth flag.** No. 15 projected **7,213** against 5,800 before cuts — the worst yet — and needed **three wire briefs plus a regional line** cut to reach 5,565. The cause is URL length, not prose: two Herald-Dispatch slugs cost **138** and **145** characters each. **U.S., World and Sci/Tech all ran three.** This is arithmetic and it has not changed since it was first logged on 08-17 | **OPEN — for Nate** |
| Open-ended | **The clock was read, not estimated, and this time there was no drift.** `config.head_start_minutes('2026-08-19')` returned **90** and `config.cron_for()` returned `30 9 * * *`, the cron actually installed; neither daylight-saving row has come due. `date` was run before every scheduling decision. **Both papers were researched, written, validated, rendered and pushed by 5:51 ET** — sixty-nine minutes before the first hold released — and **both permalinks went green within about 60 seconds of the push**, so both posts carried `--page-url` at launch and no backfill should be needed. **Delivery times are recorded below once both holds released** | **OPEN — read the clock, do not estimate it** |

### Forward-dated rows closed today

| **2026-08-19** | **WVDNR migratory bird regulations — PUBLISHED, and earlier than this ledger expected.** The row said they were "issued in August." They were issued in **July**: the West Virginia Daily News carried them **July 14** and the Parsons Advocate **July 21**, both explicitly 2026-27. Dove **Sept. 1 - Oct. 11 / Nov. 2-15 / Dec. 7 - Jan. 10**, daily 15, possession 45, shooting hours noon to sunset on Sept. 1; woodcock **Oct. 17 - Nov. 21** and **Nov. 30 - Dec. 8**, daily 3; Wilson's snipe **Sept. 1 - Dec. 16**, daily 8; sora and Virginia rail **Sept. 1 - Nov. 9**, daily 10. HIP registration required. **These dates are recorded here but were NOT printed** — see the validator row above. **The desk missed them for four editions because it was waiting for August** | **CLOSED — recorded, not printed** |

### Standing rows checked and left open

- **Aki basho dates, still unconfirmed — sixth morning.** Searched again and fetched the JSA's own English pages. Nothing there is dated later than an **Aug. 5** museum-calendar notice. The Sept. 13-27 Ryogoku Kokugikan dates remain available only from ticket resellers, travel sites and fan databases, which this paper does not cite. **One new primary-source fact did turn up: the JSA's page says September is sold out on every day** — carried in the Around the Leagues note, not as a brief. **Sumo sat out for a fifth straight edition**, correct under Ian's rule. The **Aug. 31 banzuke release** is still the load-bearing date.
- **Nucor Apple Grove sheriff's detail (~Aug. 17).** Not separately searched this morning; the statewide flooding emergency took the West Virginia sweep. Carried forward unchecked for a third morning.
- **MLS standings — RESOLVED, and yesterday's numbers were the wrong ones.** `docs/FAILURES.md` logged on 08-18 that a search summary put **FC Cincinnati first on 52 points and Columbus sixth on 45**, sourced to aggregators, and correctly refused to print them. **Those figures were wrong.** Three independent sources this morning — Fox Sports, 365scores and Wikipedia's 2026 MLS season table — agree exactly: **FC Cincinnati sixth, 27 points from 19 matches; Columbus Crew 11th, 20 points from 19**; Nashville lead on 43. The paper printed points and matches played only, and deliberately **not** the W-D-L triple, because Fox renders it in a different order from Wikipedia and MLS convention is W-L-D. **The lesson: three-way agreement is what cleared this, and refusing the two-source aggregator number a day earlier was right.**

## Open threads — 2026-08-19

- **florida-primaries-2026** — **new, and it led No. 15.** Rep. **Byron Donalds** took the Republican nomination for governor with **47.8%** against **Jay Collins** (25.2%) and **James Fishback** (10.5%), 99% counted; **David Jolly**, a former Republican, took the Democratic nomination with **61%** to **Dayna Foster**'s 15.1% and **Dotie Joseph**'s 9.6%. **Ashley Moody** (R) and **Angie Nixon** (D, over **Alex Vindman**) contest the Senate seat. **Ron DeSantis** is term-limited. Cook rates the governor's race **Solid R**. Percentages from NBC News, matchups cross-checked on WUSF and CBS News. **The campaigns are the news now, not the primary.**
- **wv-flooding-aug16** — **moved hard and is the live WV thread.** **Morrisey declared a state of emergency in all 55 counties on Tuesday**, covering storms Sunday through Tuesday and running **30 days**; the separate **July 21** declaration for 12 counties was extended to **Sept. 19**. The Fayette County drowning remains the only death reported. On **Sugar Creek Road in Charleston**, water rose about **twelve feet into homes in under ten minutes**, leaving five inches of mud in basements, vehicles submerged and culverts washed out. WV MetroNews. **A damage total, a federal declaration request, or a WVDOH reopening list is the news.**
- **wv-school-funding-suit** — **new, ran as No. 15's second statewide brief.** The **ACLU of West Virginia** filed a **notice of intent to sue** on **Aug. 17** on behalf of **Lincoln County** students, naming AG **J.B. McCuskey**, Speaker **Roger Hanshaw**, Senate President **Randy Smith**, Auditor **Mark Hunt**, Tax Commissioner **Matthew Irby**, Treasurer **Larry Pack**, the Department and Board of Education and the School Building Authority. The claim is that chronic underfunding violates the state constitution's **"thorough and efficient"** guarantee. Board President **Paul Hardesty**: "I am not really surprised... I have repeatedly asked for help with the current outdated school aid funding formula." ACLU-WV legal director **Aubrey Sparks**: Lincoln County students get "a lower quality education than what their parents and their grandparents received." Roots in **Pauley v. Kelly** and the **1982 Recht** decision. The Herald-Dispatch. **The suit actually being filed is the news.**
- **thurmond-demolition** — **new, and it was today's drawing** (`art/2026-08-19-wv.svg`, placement `wv`). **Thurmond**, population **six** — four of whom are the town government — voted **Aug. 11** to seek pro bono counsel for a temporary restraining order against the **National Park Service**, which plans to demolish **17** deteriorating structures in New River Gorge National Park, **14** of them in Thurmond or nearby **Dun Glen**, plus the **Prince General Store** on the National Register. Demolition is tentatively set for **winter**; NPS says stabilising them costs too much and some are unsafe. Council member **Tighe Bullock** said demolition "would cause irreparable harm to Thurmond." The Herald-Dispatch. **This is the first `summers_new_river` line in the paper's life** — the region had run dry every previous morning. **A restraining order, or a demolition date, is the news.**
- **abc-fcc-suit** — new, led No. 15's U.S. section. **ABC and The Walt Disney Co.** sued the **FCC** in federal court **Tuesday**, alleging retaliation for news coverage, **Jimmy Kimmel**'s monologues and *The View*. The FCC put all **eight** ABC-owned stations through early licence-renewal review years ahead of schedule. Chairman **Brendan Carr** said no licensing decision has been made and that "Disney seems a little jumpy right now." ABC paid **$16M** in December 2024 to settle Trump's defamation suit over **George Stephanopoulos**. NPR, also PBS NewsHour. **An FCC licensing decision, or a ruling, is the news.**
- **canada-tariff-pause** — new, ran in No. 15's U.S. section. Trump paused **50%** tariffs on about **$20B** of Canadian goods — roughly **5%** of Canada's exports to the US — for **three days**, hours before a **12:01 a.m. Wednesday** start, saying on Truth Social there is "a DEAL!" Ottawa agreed to drop measures Washington calls discriminatory against US **alcohol, dairy and motor vehicles**; goods range from hockey sticks to tongue depressors. PM **Mark Carney** cited "substantial progress" with work remaining. CBS News, also NPR and Al Jazeera. **Whether the three days produce a signed deal is the news — it expires this weekend.**
- **roadless-rule** — new, ran in No. 15's U.S. section. The **Department of Agriculture** moved to rescind the **2001 roadless rule**, opening tens of millions of acres from **Alaska to Florida** to roads and logging, with heaviest effect in **Montana, Utah and Wyoming**. Comment runs to **Sept. 21**. Secretary **Brooke Rollins**: "It's time to turn the page on the failed roadless rule." Utah Gov. **Spencer Cox** backed it; **Drew Caputo** of Earthjustice called the rule "the most important land protection measure of the last 60 years"; **Steve Ellis** of Taxpayers for Common Sense cited a **$6B** road maintenance backlog. NPR. **A final rule or a lawsuit is the news.**
- **uae-iran-embargo** — **new, led No. 15's World section, and it is the Hormuz thread's fifth month.** The **UAE foreign ministry** halted **all** trade, commercial exchange and financial transactions with Iran **indefinitely** on Wednesday, after its defence ministry said it detected **two ballistic missiles** launched from Iran on Tuesday, one landing inside territorial waters. Iran's **Esmaeil Baghaei** called it "baseless" and a **"false flag operation."** Retired US general **Mark Kimmitt** said Dubai supplies about **a third** of Iran's annual imports and the embargo may bite harder than US sanctions. Al Jazeera. **Related and NOT run for want of a region slot: Trump ruled out extending the expired ceasefire and threatened Oman.** **An Iranian counter-measure, or a vessel seized, is the news.**
- **liberia-deportees** — new, ran in No. 15's World section. **Liberia** agreed to accept up to **1,200** third-country deportees from the US over **one year**, the first **20** arriving **Thursday**. Information Minister **Jerolinmek Piah** called it "entirely humanitarian"; Justice Minister **Natu Oswald Tweh** said most had immigration violations. The US will help fund the programme. Immigration lawyers call third-country removals a loophole around asylum protections. NPR. **The first arrivals, or a legal challenge, is the news.**
- **kolkata-hotel-fire** — new, ran in No. 15's World section. At least **nine** died, including a child, and **six** were injured in a fire early **Wednesday** in a Kolkata building housing several hotels; **five** fire engines responded and victims were found in bathrooms, per fire services director **Anuj Sharma**. Some victims are believed to be **Bangladeshi** nationals travelling for medical treatment. **A second West Bengal hotel fire on Monday killed at least seven.** Euronews. **A cause finding is the news.**
- **iss-z1-spacewalk** — **CLOSED on the question No. 14 asked, and it reopens on a date.** The spacewalk ran **6 hours 23 minutes**, ending **2:52 p.m. EDT** Tuesday. **Anil Menon** and **Sophie Adenot** removed the failed Space-to-Ground antenna and tied it down on the truss but **ran out of time to install the spare**, needing longer than expected to disconnect cables and loosen bolts. **Installation moves to a spacewalk on Aug. 25.** It was the station's **282nd**; Adenot is the **first French woman to spacewalk**. NASA. **Aug. 25 is the follow-up.**
- **wuerzburg-nanorobots** — new, ran in Sci/Tech. **Julius-Maximilians-Universitaet Wuerzburg** (**Bert Hecht**, lead experimentalist **Jin Qin**): plasmonic nanoantennas absorb light of a given colour and helicity and re-emit it directionally, so **photon recoil** drives devices **under a micrometre** across — about **50 times** thinner than a hair — with polarisation steering them through fast 90-degree turns. They captured, carried and released bacteria on command. *Nature Communications* **17(1)**, Aug. 18, DOI 10.1038/s41467-026-70685-9. `source` names the institution, the convention since No. 4.
- **dccb-kidney-risk** — new, ran in Sci/Tech. The **European Renal Association** (**Dr. Timna Agur**) reported at its **63rd Congress** on **Aug. 18** that among **31,031** adults with type 2 diabetes, the **12,172** taking dihydropyridine calcium-channel blockers had a **33%** greater risk of a major adverse kidney event (RR **1.33**, 95% CI **1.03-1.73**) over a median **3.5** years. **Observational, and written as a presentation rather than a peer-reviewed study**, the convention set by the Osaka mosasaur item. **A randomised trial is the news.**
- **premier-league-opening** — the beat turns live **Friday**. **Arsenal v Coventry City** Friday; **Brentford v Tottenham** Saturday **17:30 BST / 12:30 p.m. ET**; **Newcastle v Liverpool** Sunday **16:30 BST / 11:30 a.m. ET**; **Fulham v Chelsea** Monday **20:00 BST / 3 p.m. ET**. Confirmed on `premierleague.com`'s own 380-fixture page. **All three British times were converted to ET this morning and printed ET-first with BST alongside**, which is what `instructions/sportsman.md` asks for and what No. 4 could not do. **From Friday, Our Teams carries results.**
- **NOT RUN, written and cut for budget:** the **Meta child-safety trial** opening statements in Oakland (California, Colorado, Kentucky and New Jersey, up to **$1.4 trillion** sought, 25 more states to follow); **UK inflation** at a four-month high of **2.9%** on a **13%** energy cap rise; the **University of La Laguna** Theban Tomb 209 find (**16** mummies and a mummified dog, 25th Dynasty into Ptolemaic, *Frontiers in Environmental Archaeology*, Aug. 19); and the **Wood County assessor's $357,000** projected shortfall. **All four are legitimate and all four are stale tomorrow unless they move.**

### Delivery, 2026-08-19

Both papers landed **exactly on their holds**: the Times at **7:00** (No. 15, message `1539589753790402677`, 1 message, **5,672** embed chars, hero attached, link live) and Sports & Sportsman at **7:05** (No. 5, message `1539591011007733857`, 1 message, **4,125** chars, link live). **`degraded` is empty on both records** — no split, no missing link, nothing taken by the trimmer. `post_discord.py` reported holds of **64** and **69** minutes: both papers were researched, written, validated, rendered and pushed by **5:51 ET**, sixty-nine minutes before the first hold released, and **both permalinks went green about 60 seconds after the push**, so both posts carried `--page-url` at launch and no backfill was needed. **The research is not outrunning the head start** — it finished with over an hour to spare, the same as yesterday.

**The projection understates by ~107 characters again.** The Times projected **5,565** and shipped **5,672**, because `--page-url` adds a content line the projection does not count. That is the third consecutive morning the gap has been almost exactly 100, so the rule of thumb holds: **treat a 5,600 projection as roughly 5,700 shipped.**

**One operational note worth keeping.** The two posters were first launched as harness background tasks, which carry a **10-minute** timeout — far shorter than the **64- and 69-minute** holds, and they would have been reaped before either paper posted. This is the same shape as the failures logged on **2026-08-13** and **2026-08-14**, where a foreground post was killed by a shell timeout. **The fix that worked was relaunching both with `setsid nohup ... &` so they reparent to PID 1 and no tool timeout can touch them**, verified by checking `PPID` was 1 before walking away. Note also that `pkill -f "post_discord.py --date ..."` **matches the agent's own shell** and killed it mid-command; kill by PID instead.

## 2026-08-20 — No. 16 and Sports & Sportsman No. 6

| Open-ended | **The stored prompt still says Sports & Sportsman is on its first edition. Sixth morning running.** Today's prompt again read "THIS IS SPORTS & SPORTSMAN'S FIRST EDITION. It is Vol. I, No. 1 of that paper," and again also said to **number it from its own ledger**. `editions/sportsman/index.json` carried Nos. 1-5, all posted, so **No. 6 is what shipped**. Flagged for Nate on 08-16, 08-17, 08-18 and 08-19; still unedited. The "extra care a first issue deserves" line is now five editions out of date | **OPEN — for Nate, fifth reminder** |
| Open-ended | **`validate_edition.py --sportsman` does not credit `upcoming` fixtures against followed-team coverage.** It warned that Chelsea, Tottenham, Liverpool, the Browns and the Bengals were "neither covered nor in sat_out" while all five carried cited, ET-converted fixture lines in `upcoming`. `instructions/sportsman.md` says a fixture line counts as accounted for. Advisory only — the edition shipped unchanged rather than filing five clubs with weekend fixtures as sitting out. See `docs/FAILURES.md` | **OPEN — for Nate, new today** |
| Open-ended | **The four-brief wire target versus `config.EMBED_BUDGET`, fifth flag.** No. 16 projected **6,144** against 5,800 before cuts and needed a regional line dropped and a 165-character Herald-Dispatch URL nulled to reach **5,496**. `wv` alone came in at **2,071** against its 1,500. **U.S., World and Sci/Tech all ran three, not four.** Unchanged since 08-17 | **OPEN — for Nate** |
| Open-ended | **The clone arrives in detached HEAD and `git pull` fails on it.** `instructions/routine.md` step 1 says `git pull`; on a detached head that returns "Please specify which branch you want to merge with." Local `main` was also two commits stale, so the first `git push` was rejected non-fast-forward. Recovered with `git branch -f main <commit> && git checkout main && git push -u origin main`. **Worth the playbook saying `git pull --rebase origin main` and checking `git status -sb` before committing** | **OPEN — for Nate, new today** |
| Open-ended | **The clock was read, not estimated, and there was no drift.** `config.head_start_minutes('2026-08-20')` returned **90** and `config.cron_for()` returned `30 9 * * *`, the cron actually installed; neither daylight-saving row has come due. `date` was run before every scheduling decision. Both papers were researched, written, validated, rendered and pushed by **5:51 ET**, and both permalinks went green **90 seconds** after the push, so both posts carried `--page-url` at launch. Both posters were launched **`setsid nohup`** on the first attempt and `PPID` was verified as 1 before walking away — the fix recorded on 08-19 was read and applied | **OPEN — read the clock, do not estimate it** |

### Standing rows checked and left open

- **Aki basho dates, still unconfirmed — seventh morning.** Searched again and fetched the JSA's own English pages. The Sept. 13-27 dates at Ryogoku Kokugikan remain available only from ticket resellers, travel sites and fan databases. `sumostats.com`, which carries a story on the Aki juryo promotions, **403s** to this crawler, and `old.reddit.com/r/Sumo/` is now refused outright by the fetch tool — so **the r/Sumo leg of Nate's 08-19 sourcing instruction could not be run today**. The **Aug. 31 banzuke release** is still the load-bearing date.
- **Sumo RAN today, for the first time since Nate's 08-18 override.** Nos. 2-5 all sat it out. No. 6 carries the countdown floor as a proper brief in Around the Leagues — "Aki basho is 24 days out and still unconfirmed" — sourced to the **Japan Sumo Association** for the two facts its own page supports (no September schedule published, every day sold out), with the **Sept. 13 opening explicitly labelled as derived from the second-Sunday rule**. That is what the floor is for and it should run every morning from here.
- **Nucor Apple Grove sheriff's detail (~Aug. 17).** Not searched this morning; the WV sweep went to the Pritt indictment and the water announcement. Carried forward unchecked for a fourth morning.
- **Juryo promotions for Aki — recorded, NOT printed.** The JSA's banzuke compilation meeting on **July 29** promoted **Tanji** (Arashio, 20) and **Tokifudo** (Tokitsukaze, 22) to shin-juryo and returned **Nabatame** (Futagoyama, 24) after a knee injury. Carried by `sumostats.com` (403) and `furansumo.com`; **no outlet this desk could open has it**, and it is three weeks old regardless. If a citable outlet picks it up at the Aug. 31 banzuke, it is a brief.

## Open threads — 2026-08-20

- **kyiv-barrage-aug20** — **new, and it led No. 16.** A Russian ballistic missile barrage on Kyiv overnight killed **at least 12** and wounded **33**; Euronews carried 12, **Al Jazeera put the toll at 13**, and both agree on 33 wounded, so **12 is what was printed** under the two-outlet rule. Strikes hit **Sviatoshynskyi, Solomianskyi and Shevchenkivskyi**; a **nine-story** residential block collapsed and caught fire with people trapped at a second, per Mayor **Vitali Klitschko** on Telegram; a **children's hospital** was damaged, **two fuel facilities** were struck and parts of two districts lost power. Parliament confirmed **Yevhenii Khmara** as defense minister the day before, **312-2**. **A revised toll, or the energy-infrastructure campaign Al Jazeera flagged for winter, is the news.**
- **us-debt-40t** — new, led No. 16's U.S. section. The national debt passed **$40 trillion** Wednesday, **five months** after $39 trillion and five months after $38 trillion in October 2025. **Margaret Spellings** of the Bipartisan Policy Center called the path "plainly unsustainable"; the BPC expects the **$41.1 trillion** statutory limit to be reached between late 2026 and mid-2027. PBS NewsHour, citing AP. **NPR's companion piece** — 30-year yields at their highest since **2007**, mortgages near **6.67%**, **$3 billion a day** in interest — was **not run**, because it is the same story from the other end. **The debt-ceiling fight is the news.**
- **ice-grievances** — new, ran in No. 16's U.S. section. NPR found ICE's detention grievance process "barely operational": a 2024 ACLU study of California facilities found **71%** of **485** grievances rejected or deemed unfounded and **8%** decided for the detainee. The **Immigration Detention Ombudsman closed in May 2026**; the Office for Civil Rights and Civil Liberties fell from about **150** staff to a handful in 2025, halting over **500** investigations. **Chris Brundage**, former deputy ombudsman: "It's a patchwork system that has never worked as intended." DHS declined specific questions. **A congressional inquiry, or a court order, is the news.**
- **carlisle-midair** — new, ran in No. 16's U.S. section. A **Cessna 150** struck a Pennsylvania State Police **Bell 407** hovering for training at **Carlisle Airport**, Cumberland County, about **7 p.m. Wednesday**. The Cessna pilot, believed the sole occupant, died; both troopers had minor injuries. Acting Commissioner Lt. Col. **George Bivens** said the Cessna "veered hard to the right at the last moment." **NTSB** leading, FAA assisting. CBS News. **The NTSB preliminary is the news.**
- **iran-economic-operation** — **new, led No. 16's World section, and it is the Hormuz thread's sixth month.** Trump announced on Truth Social what he called the "MOST CRUSHING ECONOMIC OPERATION EVER TAKEN AGAINST ANY COUNTRY," promising "Economic Warfare and Isolation on an unprecedented scale" and threatening "TREMENDOUS Economic Consequences" for any nation whose banks, businesses, airports or government entities help Iran. It extends **Operation Economic Fury**, running since February, which already carries oil, shipping and financial sanctions and a naval blockade of Iranian ports. Foreign Minister **Abbas Araghchi** called it "economic terrorism." Al Jazeera notes enforcement against **China's independent refineries** and overland trade with Turkey, Iraq and Central Asia is the hard part. **A designated entity, or a Chinese refinery sanctioned, is the news.**
- **nk-missile-aug20** — new, ran in No. 16's World section. Japan's prime minister's office reported a suspected ballistic launch off North Korea's east coast **Thursday**, a day after Seoul and Washington cut the scope of the **11-day Ulchi Freedom Shield** exercises on Trump's order. **Kim Yo Jong** had already rejected the gesture: "The provocative, aggressive nature of the drills won't change even though their duration and size were reduced." NPR. **A South Korean or Japanese assessment of range and type is the news.**
- **car-mine-collapse** — new, ran in No. 16's World section. Tunnels collapsed **Tuesday** at an artisanal gold mine at **Zamboye village**, about **50km** from **Baboua** in western Central African Republic near the Cameroon border. Red Cross volunteer **Gervais Ganagoroh** said **more than 100 bodies** had been recovered, corroborated by a local mining association official; others remain buried. The Baboua public prosecutor blamed "the collapse of several underground tunnels." City official **Bertrand Be Yangue**: "Finding them alive would be a miracle." Al Jazeera. **A confirmed final toll is the news.**
- **swift-reentry** — **new, and it was today's drawing** (`art/2026-08-20-scitech.svg`, placement `scitech`). NASA and **Katalyst Space Technologies** called off the **$30M** attempt to boost the **Neil Gehrels Swift Observatory** after Katalyst's **Link** craft, launched early July, spun uncontrollably and never recovered its pointing. Swift launched in **2004** on a two-year mission, ran more than two decades on gamma-ray bursts, had its instruments switched off earlier in 2026 to slow the descent, and is at **216 miles** falling about **5 miles a month** — **186 miles by October**, reentry later this year. Administrator **Jared Isaacman**: "This is not the outcome we were working toward, but it does not change why this mission was worth attempting." CBS News. **A reentry date, or a debris assessment, is the news.**
- **change-7** — new, ran in No. 16's Sci/Tech. The **Chang'e-7** probe and its **Long March-5 Y14** were moved vertically to the pad at **Wenchang**, Hainan, on **Wednesday**. An orbiter, lander, rover and a **hopping probe** will survey the lunar south pole for water ice in permanently shadowed craters, targeting the illuminated rim of **Shackleton** crater. China Manned Space Agency via CGTN; **SpaceNews and Science both 403'd**, so the state agency's own announcement is the source and is attributed as such. Reporting elsewhere puts the window as early as **Aug. 24**, which the CMSA page does not state and which was **not printed**. **The launch itself is the news.**
- **theban-tomb-209** — new, ran in No. 16's Sci/Tech, and it is the item **written and cut for budget on 08-19** finally getting in. **University of La Laguna** researchers led by **Dr. Jared Carballo-Perez** found **16** mummified individuals, a **mummified dog** placed on top of a man and a woman, and a disturbed deposit of at least four more in chamber three of **TT 209**, built in the **25th Dynasty (754-656 BCE)** and used into the **Ptolemaic** period. The finding is a shift from single coffined burials to dense stacked deposits. *Frontiers in Environmental Archaeology*, Aug. 18.
- **wv-water-145m** — **new, led the notebook.** Morrisey committed at least **$145 million** to water and wastewater infrastructure at a **Beckley** news conference **Wednesday**, after a two-day southern listening tour through **Wayne, McDowell, Mingo and Wyoming** counties. With public, private and federal match it could leverage about **$450 million** more and puts the state on track past **$1 billion** in total projects. The **Clean, Clear Water Strategy** partners Marshall, WVU and the **11** regional planning and development councils on grant-writing help, with **60-day** project reviews. WV Public Broadcasting. **A named project list, or the first awards, is the news.**
- **pritt-indictment** — **new, ran as the notebook's second statewide brief.** A federal grand jury indicted **David Elliott Pritt**, 36, former Fayette County social studies teacher and member of the House of Delegates, on **three felony counts** including sexual exploitation of a child, coercion of a minor and witness tampering, over conduct alleged in **Fayette County** from **2024**. He was arrested **July 22**, resigned from the legislature, withdrew from the election, and was terminated by Fayette County Schools. WV MetroNews; The Herald-Dispatch carried it too. **An arraignment or a plea is the news.**
- **charleston-i64-crash** — new, ran as the `putnam_kanawha` line **with its URL nulled for budget**. A southbound semitruck's load shifted at **mile marker 100** on **Interstate 64/77** in downtown Charleston about **5:45 a.m. Wednesday**; it crossed a concrete barrier and fell into a WVDOT equipment lot below, downing power lines. The driver was ejected and the passenger extricated by Charleston Fire; both were critical. The CPD Crash Investigation Unit is investigating. The Herald-Dispatch.
- **criss-write-in** — ran as the `mid_ohio_valley` line, and it is the **fresh angle on a 10-day-old filing**. **Charles Hartzog** (R, 23, who beat Criss **688-423** in May), **Dennis V. Rempel** (D) and **Stephen Thomas Smith** (L) all said Wednesday they are unconcerned by House Finance chairman **Vernon Criss**'s write-in bid, filed **Aug. 10** after the closed primary shut out unaffiliated voters. Hartzog: "I'm not worried about him winning." Parkersburg News and Sentinel. **November is the news.**
- **wvu-penn-state-soccer** — **new, led Our Teams and is tonight.** No. **22** WVU host No. **23** Penn State in women's soccer, **Thursday 7 p.m. ET** at Dick Dlesk, Morgantown. WVU opened **2-0** over Dayton; Penn State are **0-1-1** after drawing **2-2** with then-No. 2 Notre Dame. Penn State lead the series **15-7-3** and have won the last **six**, unbeaten in nine. Coach **Nikki Izzo-Brown** quoted. WV MetroNews. **The result is Friday's Our Teams line.**
- **NOT RUN, searched and honestly empty:** `nicholas_webster` (a Summersville DUI checkpoint scheduled Aug. 23 and an Aug. 30 lake clean-up — both future standing events, not news) and `summers_new_river` (a WV Hive booth at Bridge Day in October — not news). **Willie Akers**, the WVU basketball figure, **died Tuesday at 89** and was carried by MetroNews; it was not run because both statewide slots went to the water money and the Pritt indictment, and it is stale tomorrow. Also not run: the **Bridgeport/Harrison County** flood damage assessment (**98** assessments done, **2.25 inches in 25 minutes** Monday, FEMA threshold undecided, Tim Curry quoted) — Harrison is outside the five regions and it lost the statewide slot; **Portugal's face-covering law**, signed by President **Antonio Jose Seguro** on Tuesday with fines of **150 to 3,000 euros** (Euronews, opened and sourced) — cut because the CAR mine collapse took the third World slot and Europe already had the lead.

### Delivery, 2026-08-20

Both papers landed **exactly on their holds**: the Times at **7:00** (No. 16, message `1539952139097477204`, 1 message, **5,603** embed chars, hero attached, link live) and Sports & Sportsman at **7:05** (No. 6, message `1539953397602459713`, 1 message, **4,931** chars, link live). **`degraded` is empty on both records** — no split, no missing link, nothing taken by the trimmer, no backfill needed. `post_discord.py` reported holds of **67** and **72** minutes.

**The projection understates by ~107 characters, fourth consecutive morning, and the rule of thumb is now solid.** The Times projected **5,496** and shipped **5,603** (+107); Sports & Sportsman projected **4,823** and shipped **4,931** (+108). Both gaps are `--page-url`'s content line, which the projection does not count. **Treat a 5,600 projection as roughly 5,710 shipped**, and note this cuts the usable projection ceiling to about **5,690** if 5,800 is the real limit.

**The research is not outrunning the head start.** Both papers were researched, written, validated, rendered and pushed by **5:51 ET** — 69 minutes before the first hold released — and both permalinks went green **about 90 seconds** after the push, so both posts carried `--page-url` at launch. The 5:30 wake is correct and does not need moving. Research ran roughly **5:32 to 5:50** for both papers together, the fastest of the two-paper mornings so far, helped by MetroNews, the Herald-Dispatch, NPR, PBS, Al Jazeera, Euronews and CBS all opening on the first attempt.

**Both posters were launched `setsid nohup` on the first attempt and `PPID` was verified as 1 before walking away.** The 08-19 row's fix was read and applied. Note for the next shift: a harness `Monitor` task is capped at **30 minutes** even when a longer timeout is requested, which is shorter than a 67-minute hold — a backgrounded `until [ "$(ps -eo args | grep -c '[p]ost_discord.py --')" -eq 0 ]; do sleep 20; done` waiter is what survived the wait and reported both exits.

---

## 2026-08-22 — No. 18 (Times) and No. 8 (Sports & Sportsman)

| Open-ended | **The stored prompt still says Sports & Sportsman is on its first edition. FIFTH morning.** The 2026-08-22 prompt again read "THIS IS SPORTS & SPORTSMAN'S FIRST EDITION. It is Vol. I, No. 1 of that paper," and again also said to **number it from its own ledger**. `editions/sportsman/index.json` carried **Nos. 1 through 7, all posted** (Aug. 15-21), so **No. 8 is what shipped**, per "compute it, never guess it." Flagged on 2026-08-16, 08-17 and 08-21 and still not edited. The prompt's "take the extra care a first issue deserves" is now five days of advice attached to the wrong edition | **OPEN — for Nate, fourth reminder** |
| Open-ended | **Head start was 90 and the clock was read, not estimated — cleanly, second morning running.** `config.head_start_minutes('2026-08-22')` returned **90** and `config.cron_for()` returned `30 9 * * *`, the cron actually installed. Neither daylight-saving row has come due. `TZ=America/New_York date` was run before every scheduling decision. **Both papers were researched, written, validated, rendered, committed and pushed by 5:53 a.m. ET, 23 minutes after the 5:30 wake** — and Pages went green in **11 seconds**, so both posts carried their permalinks with no backfill. The head start is comfortably generous at 90 minutes | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-08-24** | **U.S.-Canada tariff retaliation takes shape** | Talks collapsed Friday night and **50% tariffs on about $20bn** in Canadian goods took effect at midnight — hockey sticks, building materials, liquors, some clothing. **Carney suspended negotiations, recalled negotiators to Ottawa** and said Canada will match "dollar for dollar." **Greer** said Canada declined to finalize a deal reached earlier in the week; the U.S. had offered cuts on steel, aluminum, autos, lumber. **Provincial bans on American alcohol** were a sticking point. Duties imposed under **Section 338, Tariff Act of 1930**, so legal challenges are expected. NPR cross-checked against NBC News. **Led No. 18. What Canada actually imposes, and the first lawsuit, are the news** |
| **2026-08-31** | **Aki banzuke (rankings) released** | Unchanged and still the load-bearing date. Searched again: the **Sept. 13-27 Aki dates are carried only by ticket resellers, travel sites and fan databases** — a **ninth** straight morning. `sumo.or.jp/En/` fetched; newest English item is still the **Aug. 5** museum-calendar update and the September page says only that every day is sold out. The countdown ran as S&S No. 8's sumo line pegged to the **banzuke at nine days out**, a different sentence from No. 7's ten |
| **2026-08-24** | **Huntington council takes up the Flock ordinances** | Unchanged from No. 12/No. 17. Separately, **residents launched a ballot initiative Aug. 20 to ban surveillance tech in Huntington** (The Herald-Dispatch) — written and **not run**, at 48 hours old on a morning the Cabell line went to Synthesis Health. **If the ordinance vote moves Monday, the initiative is the second half of that story** |
| **summer 2027** | **Synthesis Health takes Marshall's Med-Tech building** | Radiology-AI firm moving into the **IDEA District**; CEO **Murray A. Reicher** expects **200 to 300 jobs in Huntington over five years**. Construction starts summer 2027. Partners named: LG NOVA, Aurion Capital, IRC Holdings, the state, Marshall. The Herald-Dispatch. Ran as No. 18's `huntington_cabell` line, **link dropped for budget**. **A hiring number or a groundbreaking is the news** |
| **open** | **Parkersburg municipal services garage replacement** | **Rep. Riley Moore** presented **$1M** in Community Project Funding Friday for a **55-year-old** garage Mayor **Tom Joyce** says cannot house the city's larger equipment. Joyce: the $1M "is a great start, but it's not going to be enough to complete." No total cost or timeline yet. WTAP. Ran as No. 18's `mid_ohio_valley` line. **A total project cost is the news** |
| **open** | **Four dead in the Charleston interstate crash** | Single vehicle, eastbound at the **I-77/I-64 split** about **10:52 p.m. Friday**, into the median wall and off into the **Martin Marietta yard** below near Pennsylvania Avenue. **Names not released**; Charleston police investigating. **Second median incident at that spot in a week** — a tractor-trailer went over the wall Wednesday and both occupants survived. **Note WSAZ carried "at least 2 dead" against MetroNews' four; the later, more complete MetroNews figure ran and WSAZ's was not averaged in.** WV MetroNews. Led No. 18's notebook. **Names, a cause, or a barrier review is the news** |
| **open** | **Pentagon fires the Stars and Stripes masthead** | Editor-in-chief **Erik Slavin**, Middle East reporter **Lara Korte** and publisher **Max Lederer** got separation notices Friday for insubordination after a CBS interview on editorial independence. Navy Capt. **William Urban** had been installed as military deputy to the publisher without notice. National Press Club president **Mark Schoeff Jr.** called it "another brazen attempt by the Pentagon to dictate coverage." PBS NewsHour. Ran in No. 18's U.S. **A reinstatement, a suit, or the next editor is the news** |
| **2026-09-01 → 2026-09-14** | **NC recreational southern flounder season** | Unchanged and now **ten days out**. One fish per person per day, **15-inch** minimum, hook and line and gig only, coastal and joint waters, proclamation **FF-27-2026**, every kept fish reported. Confirmed today on the **NCDEQ** press release. Ran as S&S No. 8's "coming in" |
| **2026-08-29 → 2026-09-07** | **WV gun bear season, selected counties** | **Seven days out.** Daily 1, possession 2, season limit 2; **the county list is not in the pamphlet's summary table so no county was named**, and deer/bear bag limits sit on pages 33-39. WVDNR via `reference/wv-hunting-2026-27.json`, `valid_through` **2027-06-30** checked against the edition date. Ran as S&S No. 8's first "coming in" |
| **2026-08-23 → 2026-08-24** | **Premier League matchweek 1, all three followed clubs** | Season opened Friday: **Arsenal 3-0 Coventry** (Havertz, Saka, Odegaard; Coventry back after 25 years). **Tottenham at Brentford Sat. 12:30 p.m. ET**, **Liverpool at Newcastle Sun. 11:30 a.m. ET** (confirmed on Newcastle's own site), **Chelsea at Fulham Mon. 3 p.m. ET**. From Monday the football beat is results. **Note: a fixtures-page fetch contradicted itself, listing Newcastle v Liverpool in matchweek 1 and then claiming Liverpool's opener was Aug. 29 v Nottingham Forest; the club's own page settled it and the Aug. 29 claim was discarded** |
| **2026-08-22** | **Both NFL clubs at home in preseason week two** | **Browns v Buffalo 1 p.m. ET** at Huntington Bank Field (confirmed on clevelandbrowns.com), **Bengals v Chicago 7 p.m. ET** (NFL.com). **A search result claimed Browns-Bengals met each other today; the primary schedules disproved it and it was discarded.** Ran as S&S No. 8's fixtures — **the results are Sunday's Our Teams lines** |

### Open threads

- **williams-river-recession** — 2026-08-22: the flood is nearly out. USGS 03186500 read **258 cfs and
  2.28 feet at 5:15 a.m.**, off **446 cfs** 24 hours earlier and off **4620 cfs** at the Aug. 17 peak.
  The fetcher's verdict is **"258 cfs - pushy. Wadeable at the edges, not across."** Both papers carried
  it, and it was **today's drawing** (`art/2026-08-22-wv.svg`, placement `wv`) — deliberately the third
  picture of the same reach: the **2026-08-15** low-water sketch at 179 cfs, the **2026-08-17** blown-out
  one at 4620, and today's water back inside its banks with the flood's drift line still hung on the
  trees. **The Ohio is splitting: Point Pleasant steady at 25.97 ft (pool), Huntington 30.43 ft and
  falling, still 4.5 ft above the pool side.** Watch for the Williams under about 200 cfs — that is
  wadeable water and the end of this thread.
- **us-canada-trade-war** — 2026-08-22: **new, and it led No. 18.** See the forward-dated row above.
  This is the movement on the thread No. 15 opened as "Trump pauses 50% Canada tariffs for three days";
  the pause ran out and the tariffs landed. **Live.**
- **somalia-aid-cuts** — 2026-08-22: new, ran in No. 18's World. UNICEF (**James Elder**: "This is the
  wrong moment to retreat"): a **32%** jump in severe acute malnutrition admissions in the first half of
  2026, nutrition funding down **more than 80%**, **200+** facilities closed and up to **618** at risk,
  nearly **1.9 million** children projected malnourished, ~**1 million** under five at risk of losing
  services. Somalia was excluded from a **$2bn** U.S. humanitarian pledge. Drought displaced ~**500,000**
  Jan-April on top of **3.3 million**. A record El Nino is forecast to bring flooding. Al Jazeera.
  **News again on the El Nino flooding or on restored funding.**
- **ceuta-border-crisis** — 2026-08-22: new, ran in No. 18's World. **18 unidentified men** buried Friday
  in the enclave's Muslim cemetery, **numbered graves** for later identification, Islamic rites. From the
  late-July mass crossing: **72,000+** crossed from Morocco, **90+** died, the deadliest incident on
  Spain's border; **5,000-10,000** migrants remain. Cemetery director **Said Mohammed** quoted; the
  **Moroccan Association for Human Rights** called it "a new human tragedy" and wants burials suspended
  pending repatriation. Separately Spain **rejected Morocco's call for sovereignty talks** on Ceuta and
  Melilla. Euronews. **Identifications, repatriations, or the sovereignty dispute are the news.**
- **lebanon-economy** — 2026-08-22: new, ran in No. 18's World. World Bank projects a **6.4%** contraction
  in 2026 against **4.2%** growth last year, from fighting that began in **March**; inflation to **17.5%**.
  Parliament passed bank-resolution amendments, welcomed by the IMF, which will resume technical meetings
  in Beirut. Former economy minister **Alain Hakim** quoted. Al Jazeera. **The IMF's assessment is the news.**
- **borneo-fire-season** — 2026-08-22: new, ran in No. 18's World. **154,000+** hotspots by **Aug. 11**
  (up 60% from July), **48,889 hectares** burned across six priority provinces by Aug. 9, **28,680** of it
  West Kalimantan; visibility down to **1-10 metres** in places. Sarawak's API passed **200** on Aug. 12
  and **Kuching was the world's most polluted major city** on Aug. 11; six schools moved online. **48,000**
  personnel and **35** aircraft deployed against BNPB's lowest budget in 15 years (**491bn rupiah**).
  **12 detained** for arson and illegal land clearing. An **81%** chance of a "very strong" El Nino by
  Oct-Dec. Mongabay. **Live, and it is the same El Nino driving the Somalia thread.**
- **scotus-ballroom** — 2026-08-22: new, ran in No. 18's U.S. The Court **stayed the injunction** against
  the **90,000-square-foot** East Wing addition; **Chief Justice John Roberts** signed the brief order.
  The **National Trust for Historic Preservation** sued and argues letting construction proceed ends the
  case in practice. **NPR's own copy carries both $250M and "at least $300M" for the cost, so no cost
  figure was printed** — the square footage ran instead. **A merits ruling is the news.**
- **alaska-radar-crash** — 2026-08-22: new, ran in No. 18's U.S. A civilian-contracted charter left
  Anchorage and went down Thursday afternoon on approach to the **Cape Newenham Long Range Radar Site**,
  ~**450 miles west**; **all 8 aboard died**, two pilots and six passengers. **NTSB** investigating
  (**Clint Johnson**, Alaska chief); **Lt. Gen. Robert Davis** quoted. NPR. **A cause finding is the news.**
- **sprint-exerkines** — 2026-08-22: new, ran in Sci/Tech. **Rockefeller University** (**Luke Olsen**):
  six **30-second** sprints changed nearly **a quarter** of measured blood proteins and **200+**
  metabolites against **under 0.25%** for 90 minutes of moderate cycling; **32 of 33** proteins tied to
  lower disease risk moved with sprinting versus three. Cross-referenced against **53,000+** UK Biobank
  participants. *Cell Reports Medicine*, DOI 10.1016/j.xcrm.2026.102988.
- **queen-bee-offloading** — 2026-08-22: new, ran in Sci/Tech. **University of California, Davis**
  (**Sascha Nicklisch**, **Angela Encerrado-Manriquez**, with LLNL's **Bruce Buchholz**): nanocolonies of
  one queen and 60 workers fed radiolabelled **methyl parathion**. Workers filtered **95%** on day one and
  **86%** by day 10; queens laying **1,500-2,000 eggs a day** offload the rest into them. *Current Biology*
  36(15):3734, DOI 10.1016/j.cub.2026.06.022.
- **teeth-pancreatic-survival** — 2026-08-22: new, ran in Sci/Tech. **Hiroshima University**
  (**Kenichiro Uemura**): **339** consecutive radical pancreatectomies **2014-2022**; **21+** natural
  teeth gave median overall survival **60.7 months** against **39.1**. Chewing function itself was **not**
  independently associated, which is the interesting part — Uemura reads it as lifelong inflammation,
  frailty and nutrition. Single-centre, Japanese cohort. *Journal of Hepato-Biliary-Pancreatic Sciences*,
  DOI 10.1002/jhbp.70113. **Needs multicentre validation before it moves again.**
- **light-ion-nuclear-shapes** — 2026-08-22: new, ran in Sci/Tech. **CERN**, **CMS** detector: oxygen-oxygen
  and neon-neon collisions at **5.36 TeV** per nucleon pair show significant elliptic and triangular flow,
  with neon-20's stronger elliptic signal fitting a **bowling-pin** shape against oxygen-16's **tetrahedron**.
  **Triangular-flow measurements did not match predictions** and the collaboration says so. *Physical Review
  Letters* (2026). **News again on the triangular-flow discrepancy resolving.**

### Retired this morning

- **prince-george-plane-crash** — searched again; the only movement is Foothills Boulevard reopening
  Friday evening and a paramedic count (**10 assessed, 2 transported**). No TSB cause finding. **Not run;
  the away desk went empty rather than re-report No. 17's line.** Row stays in forward-dated events until
  the TSB reports.
- **marshall-ohio-womens-soccer** — stays closed. It was postponed Aug. 16 and no makeup date has appeared.

### Covered slugs, 2026-08-22

`us-canada-tariffs-50`, `scotus-ballroom-stay`, `alaska-radar-crash-8`, `stars-and-stripes-firings`,
`somalia-child-malnutrition`, `ceuta-18-burials`, `lebanon-world-bank-6-4`, `borneo-haze-sarawak`,
`charleston-i77-crash-4`, `wv-canvass-5-percent`, `synthesis-health-idea-district`,
`parkersburg-garage-1m`, `sprint-exerkines`, `queen-bee-pesticide-eggs`, `teeth-pancreatic-survival`,
`cms-oxygen-neon-shapes`, `reds-arizona-9-0`, `pirates-dodgers-10th`, `arsenal-coventry-3-0`,
`mlb-brewers-80-49`, `aki-banzuke-nine-days`
| 2026-08-23 | Weatherman Watchdog live (trig_01THzxTGHkdRgJWJwBZwjKQX, 8:00 ET daily) — posts only on failure |
| 2026-08-23 | All five routines now claude-fable-5; Jim wakes 7:00 ET and holds to 7:15 with post_discord --at, so DST no longer inverts the morning |

## 2026-08-23 — No. 19 (Times) and No. 9 (Sports & Sportsman)

| Open-ended | **The stored prompt was fixed.** The 2026-08-23 prompt no longer claims Sports & Sportsman is on its first edition — it describes the two-paper 7:00/7:05 morning, carries the Hannan soccer rules, and the ledger numbering ran unopposed (No. 9 shipped from `editions/sportsman/index.json`). The four-morning-old row for Nate about the first-edition line can be considered answered | **CLOSED — observed fixed** |
| Open-ended | **Head start 90, clock read not estimated, both papers held from the background.** `config.head_start_minutes('2026-08-23')` = 90, `config.cron_for()` = `30 9 * * *` (installed). Both papers researched, written, validated, rendered and pushed by **6:03 a.m. ET**, 33 minutes after the 5:30 wake. Posts launched in background at 6:03 with `--not-before`; the Times **held 57 minutes and landed 7:00:04**, sport **held 62 and landed 7:05:04**. The sequence held exactly as designed | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-08** | **Canada's retaliatory tariffs take effect** | Carney, Saturday in Ottawa: steel, dairy, appliances, farm equipment, paper, electronics, matched "dollar for dollar"; "We take this step reluctantly." Greer says no new talks planned; Trump posted Canada "wants the benefits of being a State, without being one." NPR cross-checked against Al Jazeera. **Led No. 19.** The imposition itself, a climb-down, or the first Section 338 lawsuit is the news |
| **2026-08-31** | **Aki banzuke — now the sumo desk's forcing date** | Dates uncited by the JSA a TENTH morning. **And a real story is waiting on it: r/Sumo (answering for the first time since Aug. 19) carried a report that Yokozuna Hoshoryu had right-knee surgery in late July and is doubtful for the Aki basho.** Japan Times is paywalled (402), NHK/Kyodo/Mainichi English unfetchable, sumo-stats sites are synthesizers — **so it was NOT printed** (`docs/FAILURES.md`). At the banzuke, a yokozuna kyujo will be citable somewhere; check that day |
| **2026-08-25** | **Hannan open at home to Calvary, 5 p.m. ET at Ashton** | First fixtures the paper has carried from `reference/hannan-soccer-2026.json` (also Thu Aug. 27 at St. Mary's, 6:30). Ran in No. 9's week ahead. **Tuesday's result is Wednesday's line and comes ONLY from an outside outlet** — WVSSAC, Point Pleasant Register, MetroNews, a school or county post. Never from the schedule |
| **open** | **I-64/77 split safety review** | WVDOT (spokesman Brent Walker) says it is weighing anti-skid surfacing, rumble strips, speed reduction and warning lights after the fourth barrier crash there since 2022; walls are 1970s-built and meet federal standards. WSAZ. Ran as No. 19's second statewide brief — the movement on the four-dead crash thread. Victim names, a cause, or an actual installation is the news |
| **2026-08-23** | **Liverpool at Newcastle, 11:30 a.m. ET today; Chelsea at Fulham Monday 3 p.m. ET** | Both confirmed on Sky Sports today (note: Newcastle's own match page misread as 15:30 UK on one fetch; Sky's "kick-off is 4.30pm" settled it at 11:30 ET). **Results are Monday's and Tuesday's Our Teams lines.** Spurs lost the opener 3-0 at Brentford and Hull beat Manchester United 2-0 — both ran today, spent |
| **2026-08-23** | **WVU women's soccer host Duquesne, 1 p.m. ET** | Closes the opening homestand; ran in No. 9's week ahead (WV Sports Nation). The result is Monday's line |
| **2026-08-20** | **Marshall men's soccer won their opener 2-1 over Fairfield** | Adam N'Goran, last-second, No. 17 ranking (herdzone.com, found today). **Never printed — the result predates this desk finding it and is now three days old.** Do not run it as fresh; it can ride as one clause the next time Marshall soccer makes news |
| **2026-09-01 → 09-14** | NC flounder season | Reconfirmed today on the NCDEQ release (FF-27-2026); ran as No. 9's "coming in" at nine days out. NCDMF limits page (effective July 1, 2026) reconfirmed for the prime block |
| **2026-08-29** | WV gun bear, selected counties | Six days out in No. 9; county list still not in the pamphlet summary, so still unnamed |

### Open threads

- **williams-river-recession** — 242 cfs and falling at 5:15 a.m. (off 346), 2.23 ft; "pushy, wadeable
  at the edges." Both papers carried it. Under ~200 cfs is wading water and the end of this thread —
  possibly tomorrow. The Ohio keeps converging: Point Pleasant 24.98 ft (pool), Huntington 27.77 and
  falling, 2.8 ft apart.
- **us-canada-trade-war** — see the Sept. 8 row. Live and leading.
- **charleston-i77-crash** — moved to the WVDOT review row above. Names still unreleased; the Kanawha
  River body (No. 19's regional line) is a separate, unidentified case with the medical examiner.
- **prince-george-plane-crash** — the engine-power finding (RCMP/TSB, via Global News) ran as No. 19's
  away line, the desk's first Prince George line since No. 17. The TSB's actual report stays the trigger.
- **hoshoryu-aki-doubt** — NEW, unprinted, waiting on a citable source. See the Aug. 31 row.
- **wv-storm-emergency** — quiet today; Weston got a surplus street sweeper for flood cleanup (MetroNews,
  Aug. 22) — small, not run, available as a Lewis-adjacent statewide clause if the thread needs it.

### Covered slugs, 2026-08-23

`canada-retaliation-sept8`, `visa-ban-voided`, `colorado-river-cuts-2028`, `alex-jones-1-5m`,
`tiktok-coppa-400m`, `middlesbrough-wrong-way-7`, `iran-sanctions-enemy`, `kazakhstan-unicameral-vote`,
`ibaraki-quake-37`, `clay-county-crash-2`, `wvdot-split-review`, `kanawha-river-body`,
`pg-engine-power`, `black-holes-spin-flares`, `jwst-hidden-mass`, `greenland-shark-eyes`,
`vitamin-d-cognition-54`, `reds-11-5-arizona`, `pirates-dodgers-4-3`, `browns-bills-31-7`,
`bengals-bears-27-9`, `brentford-spurs-3-0`, `nashville-crew-3-2`, `fcc-seattle-1-1`,
`hull-united-2-0`, `brewers-81-49`, `aki-banzuke-eight-days`, `hannan-calvary-preview`

## 2026-08-24 — No. 20 (Times) and No. 10 (Sports & Sportsman)

| Open-ended | **Head start 90, clock read not estimated, both papers held from the background.** `config.head_start_minutes('2026-08-24')` = 90, `config.cron_for()` = `30 9 * * *` (installed). Both papers researched, written, validated, rendered and pushed by **5:54 a.m. ET**, 24 minutes after the 5:30 wake. Posts launched in background at 5:55 with `--not-before`; the Times **held 65 minutes and landed 7:00**, sport **held 70 and landed 7:05:04**. The sequence held exactly as designed | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-08-24** | **Bessent's Iran sanctions press conference, this afternoon** | The "economic D-Day" rollout ran in No. 20's U.S. **The two readable outlets disagreed on the presser's time and even its date (Euronews 7 p.m. CET Monday; Al Jazeera 17:00 GMT "Aug. 26"), so neither was printed.** What is actually announced — secondary sanctions on buyers of Iranian oil, China at ~90% of purchases — is Tuesday's follow-up |
| **open** | **Hawk Fire, Reno — NEW THREAD, led No. 20** | 15,000+ acres, 0% contained Sunday evening, 42,000 evacuated with 45,000 more warned, six hurt, human-caused per a Truckee Meadows battalion chief; Lombardo emergency, Guard helicopters and 60 troops. NPR, cross-checked against AP syndication (WSLS). **Containment, damage counts, or a cause finding is the news** |
| **2026-08-24/25** | **Tropical Storm Moke over the Big Island through Monday** | Up to 15 inches forecast a week after Lala's 30+; Green requested a presidential emergency declaration. NPR. The flooding it actually delivers is Tuesday's line |
| **2026-08-25** | **Huntington Flock ordinance vote outcome** | Council met tonight (7:30) on Farrell's revised ordinance; opponents canvassed all nine districts over the weekend for a ballot ban. Ran as No. 20's `huntington_cabell` line. **The vote is Tuesday's line** |
| **2026-08-25** | **Hannan open at home to Calvary, 5 p.m. at Ashton** | Ran again in No. 10's week ahead with Thursday at St. Mary's. **Wednesday's line is the result and comes ONLY from an outside outlet** — never from the schedule |
| **2026-08-26** | **Lottery Commission votes on the Greenbrier board** | First Guaranty's **$52.3M** judgment ask (2020 Main Street loan, delinquent since Dec. 2023, ~$20,626/day interest accruing) ran as No. 20's second statewide brief, Herald-Dispatch, **link dropped for budget**. The vote is Wednesday's brief |
| **2026-08-30** | **Roman Space Telescope launches, 7:26 a.m. ET, Falcon Heavy, LC-39A** | Confirmed on NASA's own countdown page — flight readiness review complete, eight months early. Ran in No. 20's Sci/Tech and as today's drawing. **The launch is Sunday's news; this paper posts 26 minutes before liftoff** |
| **2026-08-31** | **Aki banzuke — ELEVENTH morning the Sept. 13-27 dates are uncited by the JSA** | And the first morning **r/Sumo was unfetchable from this environment entirely** (`old.reddit.com` refused, not a 403 — the fetch tool declines the domain). The sweep ran on the JSA and searches only; the **Hoshoryu knee-surgery report stays unprinted** for want of a citable outlet. The countdown ran as No. 10's sumo line at seven days, with the JSA's own all-days-sold-out line as the second fact |

### Open threads

- **williams-river-recession — CLOSED.** USGS 03186500 read **179 cfs and 2.00 feet at 5:15 a.m.**, first
  reading under 200 since the Aug. 16 flood; the fetcher's verdict is **"prime wading water"** and it ran
  in both papers and as the Times kicker. The thread opened Aug. 17 at 4,620 cfs and ends here, eight days
  later. The Ohio is still converging behind it: Point Pleasant 25.06 (pool), Huntington 27.79 and falling.
- **hawk-fire-reno** — new, led No. 20. See the forward-dated row.
- **us-canada-trade-war** — quiet Sunday; nothing ran. NPR carries Carney saying Canada is "at war" with
  the U.S. if the thread needs a reopening line before the Sept. 8 tariffs.
- **hoshoryu-aki-doubt** — still unprinted, still waiting on a citable outlet; the banzuke should force it.
- **charleston-i77-crash** — victim names still unreleased; not searched this morning, the WV sweep went
  to McCuskey, the Greenbrier and Flock. Check names and the WVDOT review Tuesday.

### Covered slugs, 2026-08-24

`hawk-fire-reno-42k`, `moke-hawaii-15in`, `grayson-dies-prison`, `iran-econ-dday-presser`,
`pacific-drugboat-2`, `conakry-landfill-30`, `hassoun-life-sentence`, `kyiv-coalition-300-interceptors`,
`kazakhstan-adilet-71`, `mccuskey-opioid-redirect`, `first-guaranty-52m-greenbrier`,
`flock-canvass-council`, `vt-vets-home-vandalism`, `roman-launch-aug30`, `apoe4-nell2-reversible`,
`ucsd-dna-initiator`, `multilingual-brain-aging`, `newcastle-liverpool-2-2`, `reds-dbacks-3-5`,
`pirates-dodgers-0-4-sweep`, `wvu-duquesne-2-0`, `mancity-brighton-mw1-close`, `brewers-braves-4-2`,
`aki-banzuke-seven-days`

## 2026-08-25 — No. 21 (Times) and No. 11 (Sports & Sportsman)

| Open-ended | **Head start 90, posts launched in background, both papers held to their slots.** Researched, written, validated, rendered and pushed by 6:26 a.m.; posts launched 5:52 with `--not-before`. The Times **held 68 minutes and landed 7:00:0x** (two messages, split as designed); sport **held 73 and landed 7:05:07**. Pages built in ~30 seconds, so both posts carried their permalink from the start — no backfill needed | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **~2026-08-28** | **Bessent's promised bank sanction** | Operation Economic Outcast led No. 21: nearly 60 entities/vessels sanctioned, secondary sanctions widened to digital assets, tech, gold, aviation, shipping; Bessent said a **major financial institution** doing Iran business will be sanctioned **by week's end**. That named bank is the follow-up. NPR, CBS |
| **2026-08-25** | **Talwani deadline on the mail-voting order, 5:30 p.m. ET today** | SCOTUS paused her June ruling for 23 states + D.C. (ran in No. 21). The administration appeals to the 1st Circuit if she does not pause her own ruling by today's deadline; a separate USPS injunction still stands. NPR |
| **2026-08-26** | **Hannan's opener result — ONLY from an outside outlet** | Played Calvary at Ashton tonight, 5 p.m. Wednesday's line is the result from WVSSAC, the Point Pleasant Register, MetroNews or a school/county post — never the schedule, never assumed |
| **open** | **Marshall women's soccer v Wright State (Sun Aug 23) STILL uncited** | A 3-2 Marshall win surfaced ONLY in search snippets; herdzone and wsuraiders both render title-only to this pipeline. Sat out No. 11 on those grounds. Try WCHS, Herald-Dispatch, WMUL (marshall.edu/wmul) tomorrow |
| **open** | **Flock ordinance second reading, next Huntington council meeting** | Advanced Monday; Rumbaugh's misdemeanor amendment failed 6-4, her discrimination-language amendment passed 10-0; contract still unsigned; retention now seven days. Ran as No. 21's `huntington_cabell` line. WV MetroNews |
| **open** | **PSC ruling on the MARL delay-or-dismiss motion** | The WV Energy Users Group joined the call to pause; opposition letters 6,757 to 152. Sept. 8 testimony date may move. Ran as No. 21's second statewide brief. WV MetroNews |
| **open** | **NYT response to the $9.25M Spears verdict** | Ran as No. 21's first statewide brief. Alabama's damages cap trims the award by more than $2M (CBS); an appeal is the likely next move |
| **2026-08-30** | **NFL cutdown, 6 p.m. ET Sunday** | 53-man rosters due; waivers 1 p.m. Monday. Browns close preseason v New England Thursday, Bengals at Philadelphia Friday. Ran in No. 11's leagues and week ahead. Bengals.com |
| **2026-08-29/30** | **PL matchweek two, all three clubs at home... two of them** | Liverpool v Forest Sat 7:30 a.m. ET, Tottenham v Newcastle Sat 12:30 p.m. ET, Chelsea v Brighton Sun 9 a.m. ET; Tottenham first at Charlton in the League Cup Wed 2:45 p.m. ET. Sky Sports |
| **2026-08-31** | **Aki banzuke — TWELFTH morning the Sept. 13-27 dates are uncited** | r/Sumo unreachable a third straight morning; Japan Times sumo desk now returns 402. The countdown ran as No. 11's sumo line at six days |

### Open threads

- **operation-economic-outcast** — announced, led No. 21. Next: the named bank, and any "seismic" Iranian response.
- **hawk-fire-reno** — moved: 27% contained, 32 homes destroyed, evacuations eased 42,000 → 23,000. Ran in No. 21's U.S. Containment and cause next.
- **us-canada-trade-war** — not run today. Ontario's premier attacked Trump Monday ("bully", "dictator"); Sept. 8 is the tariff date.
- **hoshoryu-aki-doubt** — still unprinted for want of a citable outlet; the banzuke should force it Monday.
- **charleston-i77-crash** — victims named (ran as No. 21's `putnam_kanawha` line, all four Raleigh County, 20-21). WVDOT's review of the elevated split continues.
- **topsail-water-temp — RESOLVED.** The Beaufort station returned **83.3F** this morning, the first temperature since NOAA dropped it at Wrightsville; the 2026-08-24 station change in `config.TOPSAIL_TEMP_*` works. Both papers carried it.
- **vtdigger-403** — second occurrence (first 2026-08-22): the homepage 403'd, Vermont went unswept, and the away desk ran empty.

### Covered slugs, 2026-08-25

`operation-economic-outcast`, `scotus-mail-voting-pause`, `hawk-fire-27pct`, `asylum-visa-revocation-200k`,
`bahrain-navy-families-limbo`, `pomas-tornado-31`, `colombia-immigration-raids`, `pakistan-iran-talks-tehran`,
`indonesia-peatland-fires`, `spears-nyt-9-25m`, `marl-delay-energy-users`, `flock-second-reading`,
`i77-victims-named`, `wood-assessor-cuts`, `ocean-sst-record-21-1c`, `moon-microbes-goddard`,
`supercentenarian-cd4`, `depression-neurogenesis-atlas`, `chelsea-fulham-3-2-alonso`, `reds-giants-0-5`,
`pirates-padres-3-2-12inn`, `nfl-cutdown-aug30`, `aki-banzuke-six-days`

## 2026-08-26 — No. 22 (Times) and No. 12 (Sports & Sportsman)

| Open-ended | **First morning under the digest contract, and it held.** One message, Times webhook only; Sports & Sportsman written, validated, rendered and pushed with no post of its own, teased inside the digest. Both papers researched, written, validated, rendered and pushed by **6:00 a.m. ET**, 30 minutes after the 5:30 wake; the digest launched in background at 6:05 with `--not-before 07:00`. Pages built both dated pages inside a minute of the push. The clock was read, not estimated | |
| Open-ended | **The new sections filled honestly on day one.** British Columbia debuted at three briefs (two CKPG Today, one Global News — Prince George first, per the playbook) and Artificial Intelligence at two (IEEE Spectrum, Euronews) after a thin genuine AI wire; the notebook ran four statewide and three regional lines, with away, hotspots both empty and the kicker saying so. Nothing was padded to fill the new space | |
| **For Nate** | **The WV migratory bird summary needs transcribing into `reference/`.** The 2026-27 summary is published (WV Explorer, July 14) and the ledger's watch row resolved — but the validator rightly refused the dove dates because the pamphlet table carries `migratory: true` with **no windows**, and `wvdnr.gov` still serves an expired certificate so the agency PDF cannot be fetched from here. The In Season entry ran DATELESS, announcing the publication and the HIP requirement only. Until the migratory summary is transcribed the way the hunting pamphlet was, no WV dove/goose/woodcock date can print | **OPEN** |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **~2026-08-28** | **Bessent's named bank sanction** | Still unannounced Tuesday. The follow-up stands |
| **2026-08-26** | **Lottery Commission Greenbrier vote is TODAY** | Meeting is after this paper posts; **the outcome is Thursday's brief** |
| **open** | **Hannan-Calvary result STILL OWED** | Played Tuesday 5 p.m. at Ashton per the coach's schedule. By 6 a.m. Wednesday NO outside outlet had a score — MaxPreps shows the fixture unscored on both teams' pages, and searches at the Point Pleasant Register and WVSSAC surfaced nothing. The teams note said so in print. **Thursday they play at St. Mary's, 6:30**; check for the Calvary result alongside it. Never the schedule, never assumed |
| **open** | **Marshall-Wright State (Aug. 23) STILL uncited — fourth morning** | herdzone and wsuraiders render title-only; WMUL's archive stops at the Aug. 20 preview. The 3-2 scoreline exists only in search snippets and stays unprinted. Try WCHS and the Herald-Dispatch sport pages directly tomorrow |
| **2026-08-31** | **Aki banzuke — THIRTEENTH morning the Sept. 13-27 dates are uncited, and r/Sumo unreachable a FOURTH** | JSA's English site still shows only the museum calendar and sold-out notices. The countdown ran in No. 12 pegged to Monday's banzuke. **Hoshoryu's knee-surgery report stays unprinted** for want of a citable outlet; the banzuke should force it |
| **2026-08-30** | **Roman Space Telescope launch, 7:26 a.m. ET Sunday** | Unchanged; Sunday's paper posts 26 minutes before liftoff |
| **2026-08-30** | **NFL cutdown, 6 p.m. ET Sunday** | Browns close preseason v New England Thursday 8 ET, Bengals at Philadelphia Friday 8 ET — both in No. 12's week ahead |
| **2026-11-03** | **South Carolina Senate: Graham v Andrews** | The runoff resolved — **Darline Graham beat Ralph Norman Tuesday** with Trump's backing, ran as No. 22's first U.S. brief. The old "runoff date not established" row closes here. Annie Andrews, pediatrician, is the Democratic nominee |
| **~2026-09-24** | **DMV contract cancellation takes effect; rebid follows** | AstreaX's $63.5M award pulled after lawmakers asked why Tyler Technologies' $30M bid lost; DOT plans a narrower rebid. WSAZ and MetroNews both carried it; WSAZ's investigation prompted the interim questions. The rebid's shape is the follow-up |
| **2026-08-27** | **Tottenham at Charlton, League Cup second round, 2:45 p.m. ET today** | The result is Thursday's Our Teams line |
| **2026-09-01** | **NC flounder opens (six days), WV gun bear Saturday (three)** | Both reconfirmed today — flounder on the NCDEQ release (FF-27-2026), bear from the reference file, county list still unnamed because the pamphlet table has none |

### Open threads

- **dolly-parton-dies** — led No. 22, with the WV angle (50,000 Imagination Library children, the 2022 Clay
  Center visit) as the notebook's first statewide brief. Arrangements, the Dollywood succession and the
  Imagination Library's future are the follow-ups.
- **operation-economic-outcast** — the named bank "by week's end" is the trigger. Iran-Oman agreed a
  seven-mile temporary Hormuz corridor Wednesday (No. 22's fourth World brief) — the first movement on the
  route dispute that broke the June memorandum; technical talks on a permanent lane follow.
- **hawk-fire-reno** — 85% contained, 47 homes, ~5,000 still out. A cause finding or full containment
  probably closes the thread.
- **us-canada-trade-war** — Eby's non-tariff push (no U.S. travel, the $12B fighter-jet buy, Westshore
  thermal coal) ran as the BC section's third brief. Sept. 8 tariffs stand.
- **huntington-vacated-residences** — six properties, ~40 students in a downtown hotel; permanent housing
  and the buildings' fate are next. Separate from the Flock thread, whose second reading is at the next
  council meeting.
- **putnam-google-datacenter** — Putnam United's resolution heard for three hours; commissioners say HB 2014
  leaves them nothing. A legislative move in Charleston would be the next line.
- **marl-psc** — ruling on the delay-or-dismiss motion still pending.
- **prince-george-plane-crash** — quiet; the TSB report stays the trigger. BC's section debut used Bird's
  caucus exit, the Nechako hatchery and Eby instead.
- **wvu-mens-soccer** — 1-1 after the 1-0 home opener win; at UNC-Greensboro Friday.

### Covered slugs, 2026-08-26

`dolly-parton-dies-80`, `graham-runoff-win`, `talwani-violation-rule-publishes`, `hawk-fire-85pct`,
`power-shutoffs-million-august`, `kenscoff-raid-47`, `pims-nursery-fire-14`, `pomas-tornado-39-injured`,
`iran-oman-hormuz-corridor`, `dolly-wv-imagination-50k`, `dmv-contract-canceled-63m`,
`hazelton-bop-smith-resigns`, `kanawha-field-transfusion`, `marshall-frat-houses-vacated`,
`putnam-google-resolution`, `parkersburg-grants-water`, `bird-independent-mla`, `nechako-hatchery-38m`,
`eby-non-tariff`, `shingrix-dementia-24pct`, `petermann-ice-island`, `chromosome-highways`,
`gravity-clusters-cmb`, `delft-llm-robotaxi`, `ox-alpha-openrouter`, `wvu-st-bonaventure-1-0`,
`reds-giants-1-3`, `pirates-padres-0-1`, `baleba-united-70m`, `mets-brewers-10inn`, `aki-banzuke-five-days`

## 2026-08-27 — No. 23 (Times) and No. 13 (Sports & Sportsman)

| Open-ended | **Both never-empty blocks filed on their second morning.** The away desk ran the Bennington resort-permit appeal (Aug. 11, dated in print — 16 days, just past the 14-day window, taken over an empty block per Nate's ALWAYS-content rule) and Vacation Hotspots ran both places: Gauley season Sept. 11 (WV Explorer, published Aug. 26) for the cabin, and Surf City's JH Batts path segment-5 bid (posted Aug. 3, updated Aug. 25, bids due Oct. 12) for Topsail — the second item the 08-26 ladder verification found, printed a day later. `surfcitync.gov/civicalerts` and `northtopsailbeachnc.gov/news` both still answer | |
| Open-ended | **The sandbox checked out a DETACHED HEAD this morning.** `git status` read "HEAD detached from refs/heads/main" from session start, and the routine's opening `git pull` failed silently ("not currently on a branch") without anyone noticing until the push. HEAD was origin/main's tip plus nothing, so `git checkout -B main HEAD && git push -u origin main` fixed it cleanly — but a morning where origin had moved overnight would have needed an actual rebase. **Check `git status` FIRST tomorrow, before the pull** | **OPEN — for tomorrow's desk** |
| Open-ended | **The stored schedule prompt is a day behind the routine — again.** This morning's trigger prompt still instructs TWO Discord posts (the Times at 7:00, Sports & Sportsman at 7:05 with `DISCORD_SPORTSMAN_WEBHOOK_URL` and `--sportsman`), but `instructions/routine.md` was changed 2026-08-26 (Nate) to ONE digest message with sport publishing to the website only. The prompt itself says to follow routine.md end to end, so the repo governed and one digest went out — but this is the same stored-prompt drift the "first edition" rows logged four times in August. **Worth Nate updating the stored prompt to match the digest contract** | **OPEN — for Nate** |
| Open-ended | **Two search-result traps dodged in one morning, same shape as the Woodchopping Festival.** (1) A search summary offered "the state wants to test 90 wells in southern Bennington for PFAS" as this week's news — the page is from OCTOBER 2023. (2) Another presented Putnam County's superintendent vote as "Wednesday evening" — the vote was MAY 27. Both were caught only by opening the page and reading the date on it. The regional line ran the McCuskey/Kanawha Hope Scholarship letter (WV Watch, Aug. 25) instead | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **Nepal glacial flood — the toll is moving fast** | Led No. 23 at "at least 160" (PBS; NPR's later copy had 162 in Nepal alone) with ~400 missing in Nepal and 558 reported missing in Tibet by Chinese state media. The numbers WILL move — re-check before citing any of today's figures tomorrow. Follow-ups: the toll, the foreign nationals (47 Americans), India/China rescue help, the ICIMOD early-warning angle |
| **~court approval** | **Meta settlement: $17B/51 states (NPR), WV share $114M+ (MetroNews)** | Ran as No. 23's first U.S. brief and third WV statewide brief. The meta-addiction-trial thread CLOSES — settled midway through the Oakland trial's second week. NPR said "up to $17 billion," others $18B with Texas's separate deal; the paper printed NPR's figure and did not mix totals. Follow-up: judicial approval, and whether YouTube/TikTok settle (triggers another $5B) |
| **2026-08-28** | **Bessent's named bank sanction — still unannounced Thursday** | "By week's end" expires tomorrow. Searched again this morning: nothing. The row stands one more day |
| **2026-08-30** | **Roman Space Telescope launch, 7:26 a.m. ET Sunday** | Ran as No. 23's third Sci/Tech brief (encapsulated Aug. 21, nine months early). Sunday's paper posts 26 minutes before liftoff — the launch RESULT is Monday's brief |
| **2026-08-30** | **NFL cutdown 6 p.m. Sunday; Browns close preseason TONIGHT, Bengals Friday** | Both finales in No. 13's week ahead. Cut-down casualties are Monday's teams material |
| **2026-08-29** | **WV gun bear opens Saturday, selected counties** | Ran in No. 13's coming-in with the no-county-list caveat, reference file checked against valid_through 2027-06-30 |
| **2026-09-01** | **NC flounder opens Tuesday (FF-27-2026, reconfirmed on deq.nc.gov today)** | One fish/day, 15-inch minimum. The On the Water block tied it to the sound report's "flounder everywhere" line — opening-day is Tuesday's natural On the Water lead |
| **2026-08-31** | **Aki banzuke Monday — FOURTEENTH morning the Sept. 13-27 dates are uncited, r/Sumo unreachable a FIFTH** | JSA English page still shows only the Aug. 5 museum item and sold-out notices. No. 13's sumo line pegged the countdown to the banzuke at four days. Hoshoryu surgery report still unprinted for want of a citable outlet — Monday should force everything |
| **open** | **Hannan-Calvary result STILL OWED, third morning; Hannan play at St. Mary's TONIGHT 6:30** | MaxPreps still shows the Aug. 25 fixture unscored ("Overall 0-0"); searches at the Point Pleasant Register and WVSSAC surfaced nothing. The teams note said so in print again. Friday's line is tonight's result from an outside outlet — never the schedule, never assumed |
| **open** | **Marshall-Wright State (Aug. 23) STILL uncited — FIFTH morning, and a trap in it** | A search this morning served Marshall's 2-1 win over Wright State WITH scorers — from AUGUST 2025 (herdzone news/2025/8/27). The 2026 result exists only as a 3-2 snippet. Do not let the dated-2025 recap masquerade as the missing result |
| **2026-08-29** | **Provincial state of emergency in B.C. expires Saturday** | Bald Range at 25,021 ha ran as the BC tier brief (Today in BC, Aug. 23 — the freshest openable). Renewal or lapse of the emergency is Saturday's news; a fresher fire update should be sought daily while orders stand |
| **2026-09-08** | **Canada's 700-product counter-tariffs take effect** | The list ran as No. 23's Canada brief (Global News). The effective date is a standing follow-up |
| **~2026-09-09** | **DoubleTree housing for displaced Marshall students runs out** | Today's huntington_cabell line. What happens to the ~40 students after Sept. 9 is the follow-up; WSAZ Investigates is inside the inspection reports |
| **2026-10-11** | **Eagle Horizon separations take effect, Boone County** | 71 jobs, WARN notice, no reason given (WSAZ). Ran statewide. A reason, a buyer, or the date arriving is the news |

### Open threads

- **nepal-glacial-flood** — new, led No. 23. See forward-dated row; the toll and the missing counts are the live numbers.
- **operation-economic-outcast** — the tanker disabled Monday off Musandam ran as No. 23's Hormuz brief (Maritime Executive; IMO: 68 incidents, 20 seafarers dead in six months). The named bank is still owed by week's end.
- **king-harald-health** — new. Palace: "extremely serious," Haakon regent. The succession, if it comes, is a lead candidate.
- **kenscoff-raid** — moved: Izo 2's hostage video and the UN's church-compound detail ran as the World lead brief. The hostages' fate is the thread.
- **nigeria-borgu-kidnapping** — new: manhunt ordered, toll 40+, up-to-500 abduction figure unverified. A confirmed abduction count or rescues is the news.
- **greenbrier-lottery** — RESOLVED and the thread closes: license approved Wednesday, KLIM 51%/three seats under chairman Lloyd Charles Nathan, Jill Justice on the board. Ran statewide.
- **huntington-vacated-residences** — moved: DoubleTree through Sept. 9 ran as the Cabell line. Sept. 9 is the next trigger.
- **hawk-fire-reno** — not run today; containment was 85% Tuesday. A cause finding or full containment closes it.
- **us-canada-trade-war** — the counter-tariff list ran (Canada tier). Sept. 8 stands.
- **putnam-google-datacenter** — not run; the PG brief's data-centre echo is coincidence, not movement. A legislative move in Charleston is the trigger.
- **marl-psc** — ruling still pending, not run.
- **wvu-mens-soccer** — 1-1, at UNC-Greensboro Friday; result is Saturday's line if citable.

### Covered slugs, 2026-08-27

`nepal-glacial-flood-160`, `meta-17b-settlement`, `pa-measles-deaths-first-2026`, `ice-virginia-maryland-1300`,
`spacex-starbase-louisiana-100b`, `kenscoff-hostage-video`, `nigeria-borgu-manhunt`, `hormuz-tanker-disabled-musandam`,
`king-harald-extremely-serious`, `greenbrier-license-approved`, `eagle-horizon-boone-71`, `wv-meta-share-114m`,
`marshall-students-doubletree`, `kanawha-hope-letter-reword`, `bennington-resort-appeal`, `gauley-season-sept11`,
`surf-city-path-seg5-bid`, `pg-infrastructure-data-centres`, `bald-range-25021-holds`, `canada-tariff-list-700`,
`mars-south-interior-molten`, `jurassic-katydid-ultrasound`, `roman-fairing-sunday`, `ucl-ai-brain-surgery`,
`mturk-closes-sept30`, `openai-jalapeno-per-watt`, `tottenham-charlton-5-1`, `reds-giants-10-9`,
`pirates-padres-0-3`, `brewers-mets-8-1-lead-6-5`, `aki-banzuke-four-days`
