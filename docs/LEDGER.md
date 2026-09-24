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
| **Before 2026-09-13** | **Confirm the September (Aki) basho's real dates by search** and record them below. `config.basho_window()` derives Sep 13–27 from the second-Sunday rule; that is an estimate the validator uses to decide how loudly to advise, never a fact the paper may print. The Japan Sumo Association publishes the schedule — confirm it there or at a wire outlet | **DONE 2026-09-12** — Jiji Press (Sept. 12) reports the dohyo-matsuri at Ryogoku Kokugikan the day before the Aki basho opens Sunday, Sept. 13; Sankei carried the Day 1 torikumi on Sept. 11. The derived Sept. 13-27 window stands confirmed at its opening end |
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

| Open-ended | **Second morning under the digest contract, and it held again.** Both papers researched, written, validated, rendered and pushed by **5:56 a.m. ET**, 26 minutes after the 5:30 wake; Pages built both dated pages inside a minute. The digest launched in background at 5:55 with `--not-before`, **held 65 minutes and landed at 7:00:09 ET** — one message, 1,016 embed chars, hero attached, message `1542488853393182744`. Sport published to the web at 5:56 and was teased inside the digest. The clock was read, not estimated | |

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

## 2026-08-28 — No. 24 (Times) and No. 14 (Sports & Sportsman)

| Open-ended | **Third morning under the digest contract.** Both papers researched, written, validated, rendered and pushed by **5:56 a.m. ET**, 26 minutes after the 5:30 wake; Pages built both dated pages inside two minutes of the push — fast enough that the digest launched at 5:58 **with a verified `--page-url` for the first time since the digest began**, so the index record carries the permalink instead of the standing "no verified page url" degraded line. Held for 7:00 with `--not-before` | |
| Open-ended | **The sandbox checked out a DETACHED HEAD again — second morning running.** Caught at session start this time per yesterday's note, fixed before the pull with `git checkout -B main HEAD` + upstream re-set while HEAD matched origin/main's tip. This now looks structural to the environment, not a one-off. **Check `git status` first every morning** | **OPEN — recurring** |
| Open-ended | **The stored schedule prompt is still a day behind — third morning.** It again instructed TWO Discord posts (7:00 Times, 7:05 sport with the sportsman webhook). routine.md governed; one digest went out, sport published to the web only. Still worth Nate updating the stored prompt | **OPEN — for Nate** |
| Open-ended | **Webster County came up genuinely empty for Vacation Hotspots** after the full ladder (Webster Echo /news 404s though the domain answers; county site static; WOAY, WV Explorer, MetroNews, school and DOT sweeps). The block filed on Topsail alone (Surf City parking RFP, posted Aug. 18) — one place is the stated minimum and the block is not empty, so no FAILURES line. Cowen filed yesterday (Gauley season); if it comes up empty again tomorrow, work the ladder harder and say so | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **Nepal barrier lake — the follow-up IS tomorrow's likely lead** | Led No. 24: 469 dead/977 missing (Nepal PM's office, Friday), 3/558 Tibet, ~2M m³ impounded with 3M more coming inside three days. A burst, a drainage, or the toll are all movement. ~90 Americans unaccounted (NPR); no confirmed American deaths as of Thursday |
| **2026-08-29** | **Bessent's named bank — "by week's end" expires TODAY and nothing came** | Searched again this morning: still unannounced. If Saturday passes empty, the broken deadline is itself the brief |
| **2026-08-31** | **Aki banzuke Monday — FIFTEENTH morning the Sept. 13-27 dates are uncited; r/Sumo unreachable a SIXTH** | JSA English site: September tickets sold out, still no dates posted. No. 14's sumo line pegged the countdown to Monday's banzuke at three days. Hoshoryu surgery report still unprinted |
| **open** | **Hannan now owes TWO results: Calvary (Aug. 25, fourth morning) and St. Mary's (Thursday night)** | MaxPreps lists both fixtures unscored ("Report Score"). The teams note said so in print again. Next: at Roane Tue Sept. 1 6:30, home v Logan Thu Sept. 3 6:00. Never the schedule, never assumed |
| **open** | **Marshall-Wright State (Aug. 23) uncited a SIXTH morning** | herdzone still renders title-only, even the /schedule/text variant. The 3-2 exists only in snippets and stays unprinted |
| **open** | **WVU women at Princeton (Thu) — result to chase tomorrow** | No. 7 WVU played 7 p.m. Thursday; nothing citable by 6 a.m. Try wvusports recap, Dominion Post, goprincetontigers news page. The men opened at UNC Greensboro Friday night — both results are Saturday material |
| **2026-08-30** | **Roman Space Telescope launch 7:26 a.m. ET Sunday; NFL cutdown 6 p.m. ET Sunday** | Sunday's paper posts before liftoff; the launch result and cut-down casualties are Monday's briefs. Bengals closed preseason at Philadelphia Friday night — result is Saturday's teams line |
| **2026-08-29** | **WV gun bear opens TODAY (Saturday), selected counties** | Ran as No. 14's coming-in with the no-county-list caveat, file checked against valid_through 2027-06-30 |
| **2026-09-01** | **NC flounder opens Tuesday — FF-27-2026 reconfirmed on deq.nc.gov this morning** | One/day, 15-inch minimum. Tuesday's On the Water lead writes itself |
| **2026-10-05** | **Quebec election — NEW thread** | Fréchette dissolved the legislature Thursday; 39-day campaign, CAQ after 8 years, trade war central. Ran as No. 24's Canada-tier brief (CTV) |
| **open** | **Anthropic-Nscale $45B at Monarch (Mason County) — NEW thread, and it is a HOME-REGION story** | Bloomberg-reported Thursday, Nscale declined comment: formal confirmation is the follow-up; first capacity late 2027; E&Y jobs study (6,000/700) and $105M tax projections are already circulating (MetroNews). Ran as No. 24's first WV brief |
| **open** | **King Harald thread CLOSES — he died Friday 6:35 a.m. Oslo time** | Ran as No. 24's World lead brief. Follow-ups: Haakon's council of state and regnal name, the funeral date |
| **2026-09-08** | **Canada's counter-tariffs take effect; MARL testimony date** | Both stand. B.C.'s wildfire state of emergency ENDED Thursday, two days early (ran as bc-tier brief) — the Aug. 29 expiry row closes |

### Open threads

- **nepal-barrier-lake** — see forward-dated row; the lake is the live story now.
- **operation-economic-outcast** — the named bank is now overdue; Araghchi's "pressure doesn't work" after the Qatar PM's Tehran visit ran as No. 24's Hormuz brief (Euronews). Qatar's phased-corridor plan is movement to watch.
- **kenscoff-hostages** — moved: Thursday's near-silent police presser ran (AP via Korea Times). The hostages' fate is still the thread.
- **zambia-mundubile** — NEW: treason questioning, warn-and-caution statements recorded; formal charges or release is next (Al Jazeera).
- **lisa-cook-firing** — NEW/revived: her lawyers' letter answered the second removal attempt; the White House's next move or a filing is the trigger.
- **greenbrier-justice-morrisey** — the feud ran statewide; watch for an actual governor's-race declaration behind it.
- **huntington-vacated-residences** — not run today; Sept. 9 DoubleTree deadline stands.
- **marl-psc** — ruling still pending, not run.
- **meta-settlement-approval** — judicial approval watch, not run.
- **akers-ethics-case** — RESOLVED and closed: Supreme Court dismissed Wednesday, ran statewide.
- **prince-george-plane-crash** — quiet; TSB report stays the trigger. PG tier used the Ancient Forest centre opening instead.

### Covered slugs, 2026-08-28

`nepal-toll-469-barrier-lake`, `cook-second-ouster-letter`, `ice-july-record-noncriminal`, `artemis-ii-space-medal`,
`ed-accreditation-nprm-comment`, `king-harald-dies-89`, `kenscoff-police-presser`, `qatar-pm-tehran-hormuz`,
`zambia-mundubile-treason`, `anthropic-nscale-45b-monarch`, `greenbrier-justice-morrisey-feud`, `akers-case-dismissed`,
`yeager-lightning-damage`, `holcomb-murder-charge`, `vt-veterans-home-vandalism`, `surf-city-goldsboro-rfp`,
`ancient-forest-centre-opens`, `bc-emergency-ends-early`, `quebec-oct5-campaign`, `mtg-i2-ariane6-gto`,
`washu-pain-brake`, `hubble-lkh-merger`, `wsu-grcop42-ai-print`, `alberta-ai-town-halls`,
`browns-patriots-37-13`, `brewers-mets-8-2-lead-7`, `aki-banzuke-three-days`

## 2026-08-29 — No. 25 (Times) and No. 15 (Sports & Sportsman)

| Open-ended | **Fourth morning under the digest contract.** Both papers researched, written, validated, rendered and pushed by **6:01 a.m. ET**, 31 minutes after the 5:30 wake; Pages built both dated pages inside 20 seconds of the push, so the digest launched in background at 6:01 with a verified `--page-url` and `--not-before 07:00`. **The backgrounded process then DIED during the hold** (zero-byte log, no record, nothing sent) and the 7:02 verification wake re-posted in the foreground: **the digest landed at 7:04:19, four minutes late** (message 1543577101381148694). New standing rule: in this sandbox a nohup'd hold does not survive session idle — tomorrow, schedule the wake for ~6:58 and post in the FOREGROUND from it, or verify at 6:59, not 7:02. No detached HEAD this morning — the checkout came up clean on `main`, breaking the two-morning streak; still worth a `git status` first every day | |
| Open-ended | **The stored schedule prompt is still a day behind — fourth morning.** It again instructed TWO Discord posts (7:00 Times, 7:05 sport with `DISCORD_SPORTSMAN_WEBHOOK_URL` and `--sportsman`), and it also said to follow routine.md end to end. routine.md governed; one digest went out, sport published to the web only, the sportsman webhook untouched. Still worth Nate updating the stored prompt to the digest contract | **OPEN — for Nate** |
| Open-ended | **Hannan's two owed results finally posted, at MaxPreps.** The Aug. 25 opener printed as a 2-1 Calvary win at Ashton and Thursday at St. Marys printed as a **7-0 Hannan win** — the program's first of the fall, led No. 15's Our Teams with `result` carried. Both scores from MaxPreps, neither from the schedule file. The Calvary/St. Mary's watch rows CLOSE | |
| Open-ended | **Webster County empty a SECOND morning for Vacation Hotspots** after the full ladder again (Echo blocked, Chronicle stale since May, county sites static, MetroNews/Register-Herald/WOAY sweeps, DOT search, WV Explorer — its Gauley-season item ran Aug. 27 and is spent). Topsail filed (Pender school board on Topsail Middle, WECT), so the block was not empty and no FAILURES line — but a third straight empty Webster morning should go to Nate as a sourcing gap, not just a quiet county | **watch** |
| Open-ended | **Four search-result traps dodged in one morning.** (1) A "Summersville considers goose mitigation" item is WV Watch from AUGUST 2025; (2) the Kennedy/Maynard verdict surfacing under Friday's date is from MAY; (3) an NBER "no AI productivity impact" survey offered as Friday news is a FEBRUARY paper; (4) "Marshall outscored... Tyler" is Marshall, TEXAS high school football. All caught by opening pages and reading dates. The WVU men's 2-2 at UNC Greensboro headline could NOT be dated (WBOY/WTRF 403) against an identical 2022-24 scoreline with the same scorers, so it did not print | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **Nepal barrier lake still the lead** | No. 25 led with the rescue RESUMING after the overflow pause: 626 dead (Nepal police), 7 Tibet, 2,426 missing Nepal side (517 foreign), 554 Tibet, per Saturday's Al Jazeera. Byers: dam "highly unstable," gradual drainage the best outcome. The toll, the lake, and any confirmed American deaths are tomorrow's numbers — re-check everything before reprinting |
| **2026-08-28** | **Bessent's named bank LANDED — the watch row closes** | Banque Misr's UAE branches, Friday: proposed rule severing U.S. correspondent access (30-day comment), plus OFAC designations on Bank Melli's Dubai branch manager and a Hong Kong launderer. Ran as No. 25's second World brief (AP via KSAT). Follow-ups: the rule finalizing, Egypt's reaction |
| **2026-08-30** | **Roman launches 7:26 a.m. TOMORROW — go for launch, 60% weather** | LRR completed Friday; backup window Monday 7:22. Ran as No. 25's fourth Sci/Tech brief. **The launch result is Monday's brief**, and Sunday's paper posts 26 minutes before liftoff |
| **2026-08-30** | **NFL cutdown 6 p.m. ET TOMORROW** | Bengals closed preseason 30-13 in Philadelphia (No. 15's teams brief); Browns done Thursday. Cut casualties are Monday's teams material |
| **2026-08-31** | **Aki banzuke MONDAY — SIXTEENTH morning the Sept. 13-27 dates are uncited; r/Sumo unreachable a SEVENTH** | JSA English page: tickets sold out, no dates, museum item Aug. 28. No. 15 pegged the countdown at two days. Monday should force the dates, the new rankings, and the Hoshoryu knee story into citable print |
| **2026-09-01** | **NC flounder opens Tuesday (FF-27-2026, reconfirmed on deq.nc.gov again today)** | One/day, 15-inch minimum, hook-and-line and gig, mandatory harvest reporting. Tuesday's On the Water lead |
| **2026-09-01** | **Hannan at Roane, Spencer, 6:30 — first match with a record to report (1-1)** | Wednesday's paper carries the result IF an outside outlet has it; MaxPreps now demonstrably updates for Hannan, check it first |
| **2026-09-03** | **Talwani preliminary-injunction hearing on the USPS mail-ballot rule** | The 14-day TRO ran as No. 25's second U.S. brief (Reuters via The Daily Record). The hearing outcome is Thursday's brief |
| **2026-09-05** | **College football opens for all three: WVU v Coastal Carolina (noon, home), Marshall at Penn State (3:30, FS1, first-ever trip), Ohio at Nebraska** | WVU and Marshall ran in No. 15's week ahead with ET times; Ohio's kickoff time still unconfirmed, so it stayed in sat_out |
| **2026-09-02** | **Webster County Commission meets (first Wednesday)** | The reliable rung for the empty cabin block — check for an agenda or minutes |
| **2026-08-30** | **Crew v New England and FC Cincinnati v Nashville results (both played Saturday night)** | Both were week-ahead entries with ET times; results are Sunday's teams material. MLS standings ran unchanged (FOX Sports) since neither had played since the last table |

### Open threads

- **nepal-barrier-lake** — the lead again; see forward-dated row.
- **operation-economic-outcast** — the named bank landed (Banque Misr). Thread continues on the rule's 30-day comment window and Iran's "economic terrorism" response.
- **kenscoff-hostages** — moved: Haitians demanding answers, complicity-or-negligence investigation opened (Haitian Times). The hostages' fate is still the thread.
- **nigeria-borgu** — moved: IGP Disu deployed a rescue team under AIG Olaiya with DSS and military components; bishops decried (This Day). Rescues or a confirmed count is next.
- **norway-succession** — Haakon VIII named, procession Friday evening, mourning until the funeral; the funeral date is the next brief.
- **venezuela-oil-deal** — NEW: 65B barrels/17 fields, 55% effective output, 100-year rights (NPR). Congressional reaction, the unnamed operator, and any production reality are follow-ups.
- **usps-mail-ballot-rule** — TRO through ~Sept. 11, hearing Sept. 3.
- **anthropic-pentagon-ruling** — NEW: Judge Lin ordered the designation rescinded; an appeal is the next move to watch.
- **bc-conservative-exodus** — Day and Wat make five exits under Findlay; caucus turmoil ongoing (Global News). Findlay's survival is the thread.
- **us-canada-trade-war** — Carney rebuffed the Lake America rename (Time); counter-tariffs effective Sept. 8.
- **huntington-vacated-residences** — moved: reclassification ended the eviction notices, do-not-enter signs instead, violations unfixed (MetroNews regional line). Sept. 9 DoubleTree deadline stands.
- **bluefield-state** — NEW: Martin fired, Deeb acting, third-party audit ordered (WVPB). The audit's findings are the follow-up.
- **marl-psc** — ruling still pending, not run.
- **meta-settlement-approval** — judicial approval watch, not run.
- **wvu-mens-soccer** — played UNCG Friday; result uncited (WBOY 403) — chase Sunday. Women's Princeton match outcome also unestablished.
- **marshall-wright-state** — uncited a seventh morning; likely dead as news, drop unless it surfaces alongside fresher Marshall soccer coverage.

### Covered slugs, 2026-08-29

`nepal-rescue-resumes-633`, `venezuela-oil-65b-55pct`, `usps-talwani-tro`, `park-pardon-hochul`,
`lake-ontario-rename-eo`, `haakon-viii-regnal`, `banque-misr-uae-sanction`, `kenscoff-answers-demanded`,
`borgu-rescue-team`, `ohio-county-correctional-closes`, `snap-hot-food-waiver-four`, `bluefield-state-martin-fired`,
`martinsburg-thousand-year-rain`, `huntington-reclassification-evictions`, `gessel-kanawha-seat`,
`bennington-pfoa-class-action`, `topsail-middle-school-future`, `pg-election-signs`, `bc-conservatives-day-wat`,
`carney-lake-ontario-rebuff`, `prosthe6-eye-drops`, `curiosity-1km-panorama`, `betelgeuse-companion-image`,
`roman-go-for-launch`, `anthropic-pentagon-ruling`, `ai-cyber-letter-100`, `hannan-st-marys-7-0`,
`hannan-calvary-1-2`, `reds-cubs-10-8`, `pirates-cardinals-1-4`, `bengals-eagles-30-13`,
`brewers-rangers-6-1`, `aki-banzuke-two-days`

## 2026-08-30 — No. 26 (Times) and No. 16 (Sports & Sportsman)

| Open-ended | **Fifth morning under the digest contract.** Both papers researched, written, validated, rendered and pushed by **5:59 a.m. ET**, 29 minutes after the 5:30 wake; Pages built both dated pages inside 20 seconds, so the digest launched in background at 6:01 with a verified `--page-url` and `--not-before 07:00`. **The backgrounded process then DIED during the hold** (zero-byte log, no record, nothing sent) and the 7:02 verification wake re-posted in the foreground: **the digest landed at 7:04:19, four minutes late** (message 1543577101381148694). New standing rule: in this sandbox a nohup'd hold does not survive session idle — tomorrow, schedule the wake for ~6:58 and post in the FOREGROUND from it, or verify at 6:59, not 7:02. The sandbox checked out a **detached HEAD again — third occurrence** (Aug 27, 28, 30); caught at session start per the standing note and fixed with `git checkout -B main HEAD` while HEAD matched origin/main. Check `git status` first, every morning | **OPEN — recurring** |
| Open-ended | **The stored schedule prompt is still the two-post version — fifth morning.** It again instructed a 7:00 Times post and a 7:05 sportsman post with `DISCORD_SPORTSMAN_WEBHOOK_URL`; it also says to follow routine.md end to end, so the repo governed: one digest, sport to the web only, the sportsman webhook untouched | **OPEN — for Nate** |
| Open-ended | **Webster County FILED for Vacation Hotspots** after two empty mornings — Gauley Fest (Sept. 17-20, Summersville, river releases planned) via WV Explorer's Aug. 26 piece, a distinct fact from the spent season-opener item. Topsail filed on the town's 9/11 25th-anniversary walk (posted Aug. 21). The Webster sourcing gap flagged Aug. 29 still stands — the Echo is blocked, the county sites are static — but the ladder produced today |  |
| Open-ended | **Three stale-content traps dodged.** (1) A ScienceDaily item dated Aug. 29 on melatonin and heart failure traces to AHA **Scientific Sessions 2025** — nine months old, re-dated; not run. (2) A search summary offered "Cardinals 4-1" for Saturday's Pirates game — that was FRIDAY's score; the CBS box says the **Pirates won 6-2** Saturday. (3) A "WVU 2-2 UNCG" result surfaced from **2024**. All caught by opening pages and reading dates; the CBS box's post-game records (67-71) also disagreed with MLB.com's own standings (66-71) — the standings block printed the league's table and the brief printed no record | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **Nepal: new-flood warnings are now the live story** | No. 26 led with NDRRMA's Sunday warning after China reported increased upstream flow; combined toll 750+ (Euronews: Nepal 734 dead/2,498 missing, China 16/546). The barrier lake largely drained. Re-check every number before reprinting |
| **2026-08-31** | **Roman Space Telescope launch RESULT — Monday's brief** | Window opened 7:26 this morning, 26 minutes after the paper; ran as today's kicker, not a brief. Backup window was Monday 7:22 |
| **2026-08-31** | **Aki banzuke lands MONDAY — SEVENTEENTH morning the Sept. 13-27 dates are uncited; r/Sumo unreachable an EIGHTH** | JSA English page: sold out, no dates, museum item Aug. 28. Monday's sweep is the big one: the new rankings, the confirmed dates, and the Hoshoryu knee story should all reach citable print. Japan Times served 402 on Aug. 25; try JSA, NHK, Kyodo, Nippon.com |
| **2026-08-31** | **NFL cutdown results — Browns and Bengals cuts are Monday's teams material** | Deadline 6 p.m. ET tonight, waivers 1 p.m. Monday; both teams ran as sat_out with the deadline named |
| **2026-08-31** | **Three results land Monday:** Chelsea-Brighton (today 9 a.m.), Crew-New England (moved to today 4:30 — the Saturday slot was vacated), WVU women at Army (today 1 p.m.), Marshall women at UT Martin (tonight 8) | The Crew move is why no Crew result ran today |
| **2026-09-01** | **NC flounder opens Tuesday, Sept. 1-14** | Reconfirmed TODAY on deq.nc.gov via the Aug. 24 carcass-donation release, which also gave the season's END date (Sept. 14) and the science-donation program — Tuesday's On the Water lead |
| **2026-09-02** | **Hannan at Roane result — Wednesday, outside outlet only** | Tuesday 6:30 at Spencer, first match with a record (1-1) to defend. MaxPreps demonstrably updates for Hannan; check it first |
| **open** | **WVU men's 1-1 at UNC Greensboro uncited a SECOND morning** | ESPN's listing shows the final; the page renders empty to this pipeline and WBOY 403s. It waits for an openable dated source, or dies quietly |
| **open** | **Milton-Culloden annexation** | The commission says no petition has been filed; a formal application triggers published notice and a hearing. Ran as today's Cabell line |
| **open** | **Fundamental Data appeal to the WV Supreme Court** | The Intermediate Court dismissal ran statewide today; the groups' next filing is the follow-up |

### Open threads

- **nepal-flood** — led again; see forward-dated row.
- **kenscoff-hostages** — moved: 13 released (UNICEF), ~37 still held. The remaining hostages are the thread.
- **marshall-wright-state** — DROPPED as dead per the Aug. 29 note; Marshall soccer coverage has moved on to fresher results (both road draws ran today via the Herald-Dispatch).
- **iceland-eu** — the No vote ran; the two-year shelf makes this a closed thread unless the government wobbles.
- **us-canada-trade-war** — not run today; Sept. 8 counter-tariffs stand.
- **marl-psc** / **meta-settlement-approval** — still pending, not run.
- **hoshoryu-aki-doubt** — Monday's banzuke should force it.

### Covered slugs, 2026-08-30

`nepal-new-flood-warnings-750`, `wise-deportation-speech-ruling`, `afghan-car-deportation-flight`,
`medicare-glp1-bridge-catch`, `measles-rfk-shapiro-clash`, `kyiv-bucha-care-home-37`, `iceland-eu-no-52`,
`kenscoff-13-released`, `mv-latuf-freed-14-pirates`, `morgantown-flock-abduction`, `fundamental-data-appeals-tossed`,
`oceana-belchers-cleanup`, `milton-culloden-annexation`, `nitro-elementary-vandalism`, `rend-trail-20m-restoration`,
`north-bennington-mechanic-culvert`, `gauley-fest-sept17`, `topsail-911-walk`, `endako-alert-lifted`,
`fraser-sockeye-collapse`, `canada-5m-nepal-aid`, `cosmic-acceleration-stands`, `pilbara-natural-hydrogen`,
`science-advisory-panels-cut`, `goodfire-silico`, `cerebras-hot-chips-cs6`, `tottenham-newcastle-0-2`,
`liverpool-forest-2-2`, `reds-cubs-5-17-pca`, `pirates-cardinals-6-2`, `fcc-nashville-0-4`,
`marshall-soccer-road-draws`, `nfl-cutdown-sunday`, `aki-banzuke-one-day`

## 2026-08-31 — No. 27 (Times) and No. 17 (Sports & Sportsman)

| Open-ended | **Sixth morning under the digest contract, and the near-deadline-wake fix WORKED.** Both papers researched, written, validated, rendered and pushed by **5:59:57 a.m. ET**, 30 minutes after the 5:30 wake; Pages built both dated pages inside ~30 seconds. Instead of a backgrounded hold (which died mid-sleep Aug 29 AND Aug 30), a `send_later` wake was armed for 6:56 and the digest ran in the FOREGROUND from it with `--not-before 07:00` — held 3 minutes and **landed at 7:00:03 ET** (message 1543938405413691422, 999 embed chars, hero attached, verified page-url, zero degraded). **Keep this pattern: build early, push, arm a ~6:56 wake, post foreground** | **standing practice** |
| Open-ended | **The stored schedule prompt is still the two-post version — sixth morning.** It again instructed a 7:00 Times post and a 7:05 sportsman post with `DISCORD_SPORTSMAN_WEBHOOK_URL`; it also says to follow routine.md end to end, so the repo governed: one digest, sport to the web only, the sportsman webhook untouched | **OPEN — for Nate** |
| Open-ended | **Detached HEAD at session start again — fourth occurrence** (Aug 27, 28, 30, 31). Caught first thing per the standing note; `git checkout main` + `git pull origin main` while HEAD matched origin/main fixed it before any work | **OPEN — recurring** |
| Open-ended | **Fisherman's Post feed 403'd for the first time** (`/category/fishing-reports/topsail-sneads-ferry/feed/`); the Coastal Angler fallback answered and its Topsail monthly (published Aug. 1, labeled a month old) carried the What's-running block. Also newly blocked this morning: Prince George Citizen local-news page (403 — was readable), westvirginiawatch.com front (403), CBC article pages (403), FRED series pages (403), and Bennington Banner articles 404 unless fetched with the full `article_<uuid>.html` slug (search surfaces it) | **watch** |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **U.S.-Iran exchange of fire is the live lead** | No. 27 led with CENTCOM's Sunday strike on two Larak Island launchers (mine-laying, per Capt. Tim Hawkins) and Iran's dawn-Monday ballistic answer at King Hussein and Al-Azraq in Jordan — 8 intercepted, no injuries, MQ-9 claimed downed, UAE denied an Al Minhad hit. Follow-ups: battle-damage assessments, further retaliation, oil/shipping reaction, the House reconciliation package funding the war |
| **2026-09-01** | **Canada by-election RESULTS — tomorrow's Canada-tier brief** | North Vancouver-Capilano (Caley v. Curran, closest), Beaches-East York, Chicoutimi-Le Fjord ran today; Liberals at 170, majority at 172 |
| **open** | **Nepal: 903 recovered/4,247 missing Nepal side, 16/546 Tibet, 85 Americans unaccounted** (ABC, Monday) | Numbers still moving; re-check everything before reprinting |
| **2026-09-09** | **King Harald's funeral, Oslo Cathedral 1 p.m.** | Ran as a World brief (AFP via Express Tribune). CAUTION: the brief pairs Haakon's parliamentary oath and the start of public viewing on "Tuesday" as the wire copy did, but the wire did not name the date — establish whether that Tuesday is Sept. 1 or Sept. 8 before referencing either again |
| **2026-09-01** | **NC flounder OPENS TODAY (Sept. 1-14)** | Tuesday's On the Water lead writes itself; note the NCDMF bag-limit TABLE still shows last year's closure — cite the season notice, not the table |
| **2026-09-02** | **Hannan at Roane result — outside outlet only** | Tonight 6:30 at Spencer, record 1-1. MaxPreps updates for Hannan; check it first. Thursday: home v. Logan, 6 p.m. |
| **open** | **Marshall women at UT Martin (Sunday 8 p.m.) ended uncited** — chase Tuesday at herdzone recap/Herald-Dispatch; **WVU men's 1-1 at UNCG uncited a THIRD morning** — likely dies quietly |
| **2026-08-31** | **Aki banzuke IS OUT and CITED (JSA English site opened): Onosato E yokozuna, Hoshoryu W, ozeki Kirishima/Kotozakura/Aonishiki, all Tokyo sessions sold out.** But the **tournament dates are STILL uncited — eighteenth morning** — the JSA English pages post no schedule; the paper printed "derived Sept. 13, formally unconfirmed" again. r/Sumo unreachable a NINTH. Hoshoryu's entry/readiness is the open question — his knee surgery remains unprinted for want of a citable outlet |
| **2026-09-07** | **WV gun bear first window closes** (selected counties, list not in the summary table) |
| **2026-09-05** | **College football: WVU v. Coastal Carolina (noon), Marshall at Penn State (3:30, first-ever trip), Ohio at Nebraska (noon, FS1); squirrel youth weekend Sept. 5-6** |
| **2026-09-08** | **Canada counter-tariffs effective; MARL testimony** — both stand. **Sept. 9**: DoubleTree housing for displaced Marshall students runs out |

### Open threads

- **us-iran-larak-jordan** — new, the lead; see forward-dated row.
- **nepal-flood** — moved to a World brief (toll past 900); the lead spot went to Iran.
- **kenscoff-hostages** — moved: Luckson Jean/UNICEF release mechanics + Paraison's negligence-or-complicity probe ran (Haitian Times). 50+ still held.
- **norway-succession** — funeral Sept. 9 ran; the oath/viewing date question above.
- **venezuela-oil-deal** — moved: NPR's experts-skeptical piece ran as a U.S. brief; congressional fight continues.
- **us-canada-trade-war / lake-america** — moved: Google's U.S.-users rename ran (PBS). Sept. 8 tariffs stand.
- **colorado-river-cuts** — NEW: 27% AZ cut through 2028, up to 40% later (NPR). Two-year reviews through 2036 are the follow-ups.
- **usps-mail-ballot-rule** — hearing Sept. 3, not run today.
- **nitro-elementary** — moved: possible playground closure ran as the Kanawha line; whether it closed is a natural follow.
- **marl-psc / meta-settlement-approval / putnam-google-datacenter / anthropic-nscale-45b-monarch** — pending, not run.
- **hoshoryu-aki-doubt** — banzuke did NOT force it into citable print; still open.

### Covered slugs, 2026-08-31

`us-iran-larak-jordan-exchange`, `venezuela-oil-experts-skeptical`, `house-cr-sept30`, `colorado-river-az-27pct`,
`google-lake-america-rename`, `nepal-toll-919`, `russia-energy-strike-threat-myla-38`, `harald-funeral-sept9`,
`kenscoff-luckson-jean-probe`, `wvff-50m-overdose-day`, `chamber-child-care-summit`, `wvsl-kickoff-recovery`,
`mason-youth-league-lights`, `nitro-playground-closure-warning`, `vt-defend-the-guard-letter`, `surf-city-backflow-rfp`,
`cnc-entrepreneur-mentorship`, `highway1-fraser-canyon-reopens`, `canada-byelections-aug31`, `roman-launch-success`,
`car-t-rheumatoid-remission`, `uti-misdiagnosis-study`, `anthropic-automated-alignment`, `latenight-deepfakes`,
`chelsea-brighton-4-3`, `reds-cubs-7-5`, `pirates-cardinals-5-4`, `crew-revolution-1-3`,
`wvu-women-army-2-1`, `browns-initial-53`, `bengals-initial-53`, `aki-banzuke-published`

## 2026-09-01 — No. 28 (Times) and No. 18 (Sports & Sportsman)

| Open-ended | **Seventh morning under the digest contract, and the fastest build yet.** Both papers researched (four parallel research agents plus the sports desk in-session), written, validated, rendered and pushed by **5:53 a.m. ET**, 21 minutes after the 5:30 wake; Pages built both dated pages inside ~20 seconds. The near-deadline-wake pattern worked a second straight day: `send_later` armed for 6:56, digest posted in the FOREGROUND with `--not-before 07:00` and a verified `--page-url`, **landed 7:00:03 ET** (message 1544300793149005894, 1,043 embed chars, hero attached, zero degraded). Keep the pattern | **standing practice** |
| Open-ended | **The stored schedule prompt is still the two-post version — seventh morning.** It again instructed a 7:00 Times post and a 7:05 sportsman post with `DISCORD_SPORTSMAN_WEBHOOK_URL`; it also says to follow routine.md end to end, so the repo governed: one digest, sport to the web only, the sportsman webhook untouched | **OPEN — for Nate** |
| Open-ended | **Detached HEAD at session start again — fifth occurrence** (Aug 27, 28, 30, 31, Sept 1). Caught first thing; `git checkout -B main HEAD` + upstream re-set while HEAD matched origin/main fixed it before any work | **OPEN — recurring** |
| Open-ended | **Fisherman's Post feed ANSWERS again** via the `http://www.` variant after Monday's 403 — the August Topsail monthly (published Aug. 3, labeled a month old) carried What's-running. Newly blocked or still blocked this morning: Japan Times (402), NBC News article pages (403), The Hill (403), Herald-Dispatch article fetch (429 rate-limit), nsnews/energeticcity/CBC/My PG Now article pages (403), wvusports and herdzone render title-only, JSA `EnTicket/year_schedule` URL errors out | **watch** |
| Open-ended | **Date traps dodged: five in one morning.** (1) A Newsweek "Trump posts Kharg AI images" story surfacing as fresh is from JULY 26 — he has posted Kharg imagery before; the Aug. 31 Forbes piece is the one that ran. (2) The year-old Summersville geese story circulated again. (3) A Bennington "listening session" item is from Oct. 2025. (4) "US Navy bans DeepSeek" in Sept. 1 roundups is recycled January 2025. (5) A "cancer glycocalyx" item in Aug. 31 roundups is an Aug. 7 paper. All caught by opening pages and reading dates | |
| Open-ended | **Validator caught a direction bug before it shipped.** The Reds brief headline "Reds shut out 5-0 as the Padres pull even" tripped the result-verb check; rewritten winner-first ("Padres blank the Reds 5-0"). The `result` gate is earning its keep | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-02** | **Hannan at Roane result — tonight 6:30 at Spencer, record 1-1** | Outside outlet only, MaxPreps first. Thursday: home v. Logan, 6 p.m. Monday's Ashton fixture was a GIRLS match, outside the beat — noted in print |
| **2026-09-02** | **Marshall men host George Mason tonight; the women's UT Martin result is uncited a THIRD morning** | herdzone/ESPN/goracers all render empty or silent — the UT Martin thread likely dies quietly |
| **2026-09-06** | **WVU women host Marshall Sunday, 7 p.m., Morgantown (Gold Rush/alumni night)** | Confirmed via wvusports promotional-slate search result; the page itself renders title-only and the H-D schedules article 429'd — find an openable source before it runs in The week ahead |
| **2026-09-01** | **Norway: Haakon VIII's parliamentary oath WAS today at 11:00 GMT; lying in state runs through Sept. 8, funeral Sept. 9** (Reuters via Internazionale, opened) | The Aug. 31 "Tuesday" ambiguity resolves to Sept. 1. Not run today — World was full; tomorrow can carry the oath as done |
| **October** | **Davis sentencing in the Tupac case** (NPR) | Today's lead; faces up to life |
| **open** | **Driscoll successor watch; Grand Canyon follow-ups** (1 still missing, Phantom Ranch closed indefinitely, waterline ~40% destroyed, ~2 weeks of water reserves) | |
| **2026-09-03** | **Talwani preliminary-injunction hearing, USPS mail-ballot rule** | Thursday's U.S. brief |
| **2026-09-07** | **WV gun bear first window closes (selected counties); NC flounder closes Sept. 14** | Squirrel youth Sept. 5-6; bear youth Sept. 12-13; squirrel general opens Sept. 12 |
| **2026-09-08** | **Canada counter-tariffs effective; MARL testimony — and MARL's PSC ruling now sought pushed to May 22, 2027** | The delay request itself ran statewide today |
| **2026-09-09** | **Croft Road variance back before PG council; King Harald's funeral; DoubleTree housing deadline** | Three separate threads, same date |
| **2026-09-13** | **Aki basho derived opening — dates STILL uncited a NINETEENTH morning; r/Sumo unreachable a TENTH** | JSA posts banzuke and sold-out notices, no schedule. Hoshoryu's entry is still the open question |
| **open** | **Liberals now govern with 173 seats; Cubs within 7 of Milwaukee; Sony/Warner v. Anthropic and Apple v. OpenAI filings; EU ChatGPT VLOSE compliance due January 2027** | All ran today; all have natural follow-ups |
| **2026-09-09** | **Webster County Fair, Sept. 9-12 at Camp Caesar** — tomorrow's natural cabin line if the ladder is thin; Bergoo Bash ran today | Also: no agenda posted for tomorrow's Sept. 2 county commission meeting as of this morning |

### Open threads

- **tupac-davis-verdict** — new, led No. 28; sentencing October.
- **us-iran-larak-jordan** — moved: the Kharg AI-video post ran as the World brief; sanctions-pivot signals and Brent above $90 are the next beats.
- **nepal-flood** — 987 dead/3,916 missing Nepal side after reconciliation, 16/546 Tibet, ~500 tunnel workers; re-check every number daily.
- **kenscoff-hostages** — funerals ran; dozens still held.
- **kyiv-barrage** — sixth night ran; Ust-Luga port drone damage unprinted, watch for corroboration.
- **nitro-elementary** — suspect identified ran as the Kanawha line; whether the playground closed Monday is still unconfirmed.
- **marl-psc** — moved (delay request); ruling date now itself in play.
- **bc-conservative-exodus** — seventh MLA (Warbus) ran as the bc tier; caucus survival still the thread.
- **putnam-google-datacenter / meta-settlement-approval / anthropic-nscale-45b-monarch** — pending, not run.
- **wvu-mens-soccer / marshall-wright-state** — both dead as news unless fresh citable coverage appears.

### Covered slugs, 2026-09-01

`tupac-davis-guilty`, `driscoll-steps-down`, `grand-canyon-flood-2-dead`, `scotus-ballroom-continue`,
`kharg-ai-videos`, `nepal-toll-1000-reconciled`, `kyiv-sixth-night-12`, `kenscoff-funerals-4`,
`marl-delay-may2027`, `kirkpatrick-sworn-in`, `america250-2-2m`, `mason-standoff-arrest`,
`nitro-vandalism-suspect`, `wood-poll-workers-275`, `bennington-power-outage`, `bergoo-bash-sept5`,
`pender-1354-homes`, `croft-road-deadlock`, `bc-seventh-mla-warbus`, `liberals-sweep-173`,
`roman-first-burn`, `thylacine-skull-bite`, `freshwater-swimming-trial`, `eu-chatgpt-vlose`,
`sony-warner-anthropic-suit`, `apple-openai-evidence`, `padres-reds-5-0`, `cubs-brewers-17-3`,
`browns-claim-pride`, `bengals-claim-hinton`, `messi-international-retirement`, `aki-countdown-12-days`,
`flounder-opens-sept1`

## 2026-09-02 — No. 29 (Times) and No. 19 (Sports & Sportsman)

| Open-ended | **Eighth morning under the digest contract, on the standing pattern, and the cleanest clock yet.** Both papers researched (five parallel research agents), written, validated, rendered and pushed by **5:55 a.m. ET**, 25 minutes after the 5:30 wake; Pages served both dated pages 200 inside ~15 seconds. `send_later` armed for 6:56, digest posted in the FOREGROUND with `--not-before 07:00` and a verified `--page-url`, held 3 minutes and **landed at 7:00:04 ET** (message 1544663181576769537, 1,045 embed chars, hero attached, zero degraded). Keep the pattern | **standing practice** |
| Open-ended | **The stored schedule prompt is still the two-post version — eighth morning.** It again instructed a 7:00 Times post and a 7:05 sportsman post with `DISCORD_SPORTSMAN_WEBHOOK_URL`; it also says to follow routine.md end to end, so the repo governed: one digest, sport to the web only, the sportsman webhook untouched | **OPEN — for Nate** |
| Open-ended | **Detached HEAD at session start again — sixth occurrence** (Aug 27, 28, 30, 31, Sept 1, 2). The opening `git pull` failed with the "not currently on a branch" symptom; caught, `git checkout -B main HEAD` + upstream re-set while HEAD matched origin/main. Check `git status` first, every morning | **OPEN — recurring** |
| Open-ended | **The 19-morning Aki-basho date drought is OVER — via the venue, not the JSA.** `ryogokukokugikan.com`'s own schedule page carries **Sept. 13-27, Ryogoku Kokugikan** and is openable; the JSA English schedule pages still error out and r/Sumo is now refused outright (11th morning). **Hoshoryu's knee surgery finally reached citable print** (Furansumo, Sept. 1, from Tatsunami stable's own posts: resumed shiko, down 15 kg, entry undecided) and ran as a leagues brief. A Wakatakakage full-Aki kyujo circulates only in sumostats.com's aggregation of Japanese dailies — left UNPRINTED for want of an openable origin; confirm at NHK/Kyodo/Nippon.com before the basho | **watch** |
| Open-ended | **Hannan's Tuesday match at Roane went unreported AND is missing from both teams' MaxPreps schedules**, which now list the meeting Sept. 24 at Ashton — rescheduling is plausible but unconfirmed, so the paper said only that no score was published. Thursday: home v. Logan, 6 p.m. Chase both threads | **OPEN** |
| Open-ended | **Five traps dodged, one dispute ducked, one date conflict adjudicated.** (1) A "Fort Randolph fire" in Mason County search results is from DECEMBER 2025. (2) A Summersville murder-suicide is from FEBRUARY. (3) The Dominion Post's NextEra-asks-77-day-delay piece is YESTERDAY'S MARL brief in new clothes — not rerun. (4) WTAP and WCHS name DIFFERENT BRIDGES (Pond Creek/Rt. 68 vs. Ritchie/Ravenswood) for what looks like the same $1,600-a-day delay story — mid-Ohio Valley line skipped rather than guess. (5) The Webster County Fair: aggregator statefairtimes.com says Sept. 2-5, the county tourism site says **Sept. 9-12 at Camp Caesar** with session times — the local source printed, but a same-week check would not hurt | |
| Open-ended | **Source status shifted hard this morning.** NEWLY BLOCKED: **wvmetronews.com** (Cloudflare loader on every article — cost the Bluefield sewer hearing and Business Summit preview), WV Watch article pages (403, not just the front), **northtopsailbeachnc.gov** (403 — was a verified fetcher), Ars Technica (refused), CNBC (403), kyivpost (403), old.reddit r/Sumo (refused). Rate-limited: register-herald and herald-dispatch (CNHI 429s). Reliable this cycle: WSAZ, WTAP, WCHS, Dominion Post, Parkersburg News & Sentinel, Lootpress, Bennington Banner (full `article_<uuid>` slugs), Port City Daily, surfcitync.gov, webstercountytourism.com, deq.nc.gov, Fisherman's Post (September Topsail monthly PUBLISHED Sept. 1 — one day old, freshest ever) | **watch** |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **U.S.-Iran is the lead again and widening** | No. 29 led with Tuesday's multi-site U.S. strikes and Iran's missile/drone answer at bases in Jordan, Bahrain and Kuwait; Iranian officials claim a wedding strike in Kuhestak (5+ dead, AJ verified the location). Battle-damage, further retaliation, Brent (settled $92.31) and Hormuz transits (107/week) are tomorrow's numbers |
| **2026-09-03** | **Talwani preliminary-injunction hearing on the USPS mail-ballot rule — TOMORROW** | Ran as a U.S. brief with the whistleblower disclosure; the ruling is Thursday/Friday's brief |
| **2026-09-03** | **Hannan home v. Logan, 6 p.m. at Ashton** | Result Friday, outside outlet only; MaxPreps first |
| **2026-09-05** | **College football opens: WVU v. Coastal Carolina (noon, TNT), Marshall at No. 18 Penn State (3:30, FS1), Ohio at Nebraska (noon ET, FS1 — kickoff finally confirmed via huskers.com)** | All three ran in the week ahead. Squirrel youth weekend Sept. 5-6 |
| **2026-09-06** | **WVU women host Marshall, 7 p.m., Dick Dlesk (Dominion Post — openable at last)** | Both followed teams; Sunday's result is Monday's line |
| **2026-09-07** | **WV gun bear first window closes (selected counties)** | Ran in going-out with the no-county-list caveat again |
| **2026-09-08** | **Canada counter-tariffs effective (ran inside the Carney brief); MARL testimony date now moot — schedule moved (see 09-01)** | |
| **2026-09-09** | **King Harald's funeral; DoubleTree deadline; Croft Road at PG council; Webster County Fair opens (through Sept. 12, Camp Caesar)** | Fair ran as today's cabin line |
| **2026-09-13** | **Aki basho OPENS — dates now CITED (Sept. 13-27, ryogokukokugikan.com)** | Countdown is over; the open questions are Hoshoryu's entry and the unprinted Wakatakakage kyujo |
| **2026-09-14** | **NC flounder window closes** | Day two ran in prime today |
| **2026-09-17** | **NCDMF kingfishes scoping meeting, Wilmington (period through Sept. 30); Gauley Fest opens (through Sept. 20)** | |
| **2026-09-26** | **Abbotsford-Mission byelection — Findlay's survival test (ran as bc tier); USMNT-Peru friendly, Orlando** | |

### Open threads

- **us-iran-hormuz** — the lead; wedding-strike verification, Aqaba claim (U.S. denies) and oil are live.
- **nepal-flood** — 1,114 dead / 3,916 missing Nepal side (NDRRMA, Wednesday); ran as a World brief. Tibet count still Sept. 1 vintage.
- **germany-russia-leipzig** — NEW: consulate closure by Sept. 18, EU listings push; Moscow threatens consequences.
- **zambia-mundubile** — moved: Hichilema sworn in with Mundubile jailed; formal case detail (18 accused) is the follow-up.
- **putnam-google-datacenter** — MOVED at last: treasurer's $100M/yr tax analysis ran as the WV lead brief.
- **fundamental-data-appeal** — moved: opponents refiling at the state Supreme Court; the filing itself is next.
- **bc-conservative-exodus** — moved: Findlay stakes leadership on Sept. 26.
- **usps-mail-ballot** — hearing tomorrow.
- **kenscoff-hostages / nigeria-borgu** — no movement found today.
- **hoshoryu-aki-entry / wakatakakage-kyujo** — see watch row.
- **edouard** — landfall ran; dissipation expected tonight, flooding follow-ups only if notable.
- **marl-psc / meta-settlement-approval / anthropic-nscale-45b-monarch / milton-culloden / nitro-elementary / bluefield-state** — pending, not run (the Dominion Post MARL piece was yesterday's news).

### Covered slugs, 2026-09-02

`us-iran-strikes-wedding-kuhestak`, `house-cr-dec11-passes`, `usps-whistleblower-portal`, `oil-brent-9231-hormuz-107`,
`edouard-johnson-bayou`, `nepal-toll-1114`, `germany-russia-leipzig-consulate`, `zambia-hichilema-sworn`,
`gaza-strikes-5-ceasefire`, `treasurer-datacenter-100m`, `ridgeline-supreme-court-refile`, `chamber-90th-summit`,
`huntington-floodwall-exercises`, `kanawha-grand-jury`, `rend-trail-groundbreaking`, `vt-veterans-home-911-25th`,
`webster-fair-sept9-12`, `surf-city-appraiser-rfp`, `williston-floating-island`, `findlay-abbotsford-mission`,
`carney-wiped-out-subsidiaries`, `roman-antenna-coronagraph`, `snake-embryo-rightward`, `gluex-two-structures`,
`crew13-oxidizer-leak`, `eu-ai-office-rfis-carolina`, `fsb-bailey-frontier-cyber`, `chelsea-enzo-city-125m`,
`spurs-adarabioyo-mudryk`, `liverpool-brughmans-loanback`, `reds-padres-4-3`, `pirates-giants-13-12`,
`marshall-gmu-3-3`, `aki-dates-cited-sept13-27`, `hoshoryu-surgery-in-print`, `flounder-day-two`,
`topsail-shellfish-reopen-pa42`

## 2026-09-03 — No. 30 (Times) and No. 20 (Sports & Sportsman)

| Open-ended | **Ninth morning under the digest contract, first under the three new gates, and all three passed on the first try.** Both papers researched (five parallel research agents), written, validated, rendered and pushed by **5:49 a.m. ET**, 19 minutes after the 5:30 wake; Pages served both dated pages 200 inside ~35 seconds. The MLB standings byte-match took "68-72, fourth in the NL Central, 19 back" straight from `out/standings.json` with no cut; the date-word gate passed every away and hotspots line as written; the standings snapshot froze beside the fishing one in `editions/data/`. `send_later` armed for 6:56, digest posted in the FOREGROUND with `--not-before 07:00` and a verified `--page-url`, **landed at 7:00:01 ET** (message 1545025569341579366, 1044 embed chars, hero attached, zero degraded). Keep the pattern | **standing practice** |
| Open-ended | **The stored schedule prompt is now the thin pointer** (2026-09-02 rewrite): it named routine.md as authoritative, handed over ONE webhook, and said Sports & Sportsman does not post. First morning with no stale two-post instruction to override. Detached HEAD at session start again — seventh occurrence (Aug 27, 28, 30, 31, Sept 1, 2, 3); `git checkout main` + `git reset --hard origin/main` while HEAD matched origin/main fixed it before any work | **OPEN — recurring** |
| Open-ended | **The `result` gate caught two SCORE-SHAPED strings that were not scores**: "lost 45-7 at Georgia" (last year's opener, in the Marshall preview) and "30-40 cm" (Wakatakakage's incision) both tripped "prints a score but has no result". Rewritten as "a 38-point loss" and "30 to 40 centimeters". Worth knowing: any `\d+-\d+` in a sports brief needs a `result` or a rewrite, even a measurement | |
| Open-ended | **Sumo finally cites Japanese origins directly.** Sanspo, Hochi and Nikkan Sports refuse the pipeline, but **Daily Sports (`daily.co.jp`) and Chunichi (`chunichi.co.jp`) OPENED** — the Wakatakakage full-Aki kyujo (compartment syndrome, four surgeries, juryo in November) ran on Daily Sports and the Hoshoryu "unclear until the last moment" line on Chunichi, both found through Sumostats' English digests, which link every Japanese daily and are now the working sumo wire. r/Sumo, NHK and Kyodo unreachable again (12th morning for r/Sumo) | **watch** |
| Open-ended | **Lead art fell to rung 2 for a stated reason.** The Al Jazeera lead photographs were Trump at the Resolute Desk (a face) and the bombed Kuhestak wedding courtyard (aftermath of violence) — both out under §4.5. Drew Hubble's polar view of Saturn's south-pole decagon instead, placed in Science & Technology, credited to NASA. Not a FAILURES line | |
| Open-ended | **Source status this morning.** NEWLY OPENED: **wvmetronews.com** (the Marshall-Penn State preview fetched clean — first time since the Cloudflare block), northtopsailbeachnc.gov (answered again), daily.co.jp, chunichi.co.jp, herald-dispatch article pages (two loaded, one 429). STILL BLOCKED: WOWK (every page), WV Watch, sanspo/hochi/nikkansports, NPR article pages (503 x4 across desks), The Verge, Axios, Forbes, openai.com/index, mlb.com team schedule pages (406 — `mlb.com/scores/YYYY-MM-DD` renders), ESPN schedule pages (empty), MLS club sites (JS shells — tqlstadium.com gives ET kickoffs, FOX renders UTC). Fisherman's Post September Topsail monthly (published Sept. 1) opened via the direct slug | **watch** |
| Open-ended | **Six date traps dodged.** (1) The Kyiv Independent "502 drones" story in Sept. 3 roundups is from Sept. 3, **2025**. (2) A Buenos Aires Times obituary is 2025. (3) Kris Warner's Webster courthouse tour is 2025. (4) The Bennington Banner road-construction list is Aug. 29, **2025**. (5) visitwebsterwv.com and wvstateparks.com carry 2025 and 2023 Holly River festival dates — only webstercountytourism.com has 2026's Sept. 5-6. (6) Two ScienceDaily items (sitting/cancer, Devonian scorpion) are July papers re-dated. All caught by opening pages and reading dates | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **U.S.-Iran is the lead a third straight morning and still widening** | No. 30 led with Iran's overnight strikes on Ahmad al-Jaber (Kuwait) and Al Minhad (UAE), Iran's 18-dead toll, the Red Crescent's ICC request over Kuhestak, Iran's claim of fresh Hormuz mines and Trump's "anytime we want." Tomorrow: Kuwait/UAE damage, any U.S. answer, Brent (~$95), the Sept. 26 UNSC sanctions-panel vote France plans. Health ministry later put wounded at 142 (AJ) — the paper used the minister's 108 |
| **2026-09-03** | **Talwani preliminary-injunction hearing on the USPS mail-ballot rule — TODAY, not run** | No ruling by press time; the hearing itself was a curtain-raiser already printed Wednesday. Friday's U.S. brief if she rules; NC starts mailing ballots Friday |
| **2026-09-03** | **Pacific Islands Forum communique on China's missile test** | Ran as the Oceania brief while the retreat was still closing — the outcome (condemnation or not) is tomorrow's follow |
| **2026-09-04** | **Hannan v. Logan RESULT (tonight 6 p.m., Ashton) — outside outlet only; MaxPreps does not even list the fixture** | Also: Roane (Sept. 1) still unreported on both MaxPreps pages. Check MaxPreps and Logan's page first |
| **2026-09-04** | **Hoshoryu at (or absent from) the YDC joint practice — his Aki entry signal** | Chunichi: "unclear until the last moment. I want to participate." Wakatakakage's kyujo is now PRINTED (Daily Sports) |
| **2026-09-04** | **Liverpool at Ipswich, 3 p.m. ET; Reds open at Milwaukee 6:10 p.m. ET; Pirates finish v. Giants TODAY 12:35 p.m. ET** | Friday's teams material |
| **2026-09-05** | **College football opens: WVU v. Coastal Carolina (noon, TNT), Marshall at No. 18 Penn State (3:30, FS1), Ohio at Nebraska (noon, FS1); Tottenham at Forest 10 a.m. ET; FC Cincinnati v. D.C. United and Crew v. Colorado 7:30 p.m. ET; Holly River State Park Festival Sept. 5-6; squirrel youth weekend** | The Crew kickoff is FOX's UTC slot converted — an ET-labeled page would be better |
| **2026-09-06** | **Chelsea at Arsenal 11:30 a.m. ET; WVU women host Marshall 7 p.m.** | |
| **2026-09-07** | **WV gun bear first window closes (selected counties)** | Ran in going-out with the no-county-list caveat |
| **2026-09-08** | **Canada counter-tariffs effective; Beth Burns sworn in to the Pender commission** | |
| **2026-09-09** | **Webster County Fair opens (through Sept. 12); King Harald's funeral; DoubleTree deadline; Croft Road at PG council; Liverpool v. Atletico 3 p.m. ET; Hannan v. Point JV; NFL opens (Seahawks host New England, 8:20 p.m. ET)** | |
| **2026-09-13** | **Aki basho opens (through Sept. 27); Bengals v. Buccaneers 1 p.m. ET; Browns at Jacksonville; Hannan-Westside is Sept. 10 at Shawnee (Institute)** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m.; Bennington option-tax meetings Sept. 14 and 28 ahead of the Nov. 3 vote** | |
| **2026-09-17** | **NCDMF kingfishes meeting, Wilmington; Gauley Fest opens** | |
| **2026-09-21** | **Black Diamond Power status hearing, PSC** | Ran statewide today |
| **2026-09-26** | **Abbotsford-Mission byelection; USMNT-Peru; WV archery deer/bear and boar archery open** | |
| **mid-October** | **Pender commissioners vote on the 930-home Sidbury Road rezoning** | Ran as today's Topsail line |
| **2026-11-17** | **Maduro immunity arguments before Judge Hellerstein; trial June 1, 2027** | |

### Open threads

- **us-iran-hormuz** — led a third day; see forward-dated row.
- **nepal-flood** — 1,252 dead / 4,216 missing (NDRRMA, Thursday noon, via Kathmandu Post); the missing count is fluctuating (4,858 a day earlier) — always "at least".
- **malta-fenech-acquittal** — NEW; RSF/ECPMF reaction ran; an appeal is only in snippets, unprinted.
- **pacific-forum-china-missile** — NEW; outcome pending.
- **nigeria-us-troops-withdraw** — NEW; no date.
- **wooton-medical** — NEW; no condition update by press time; the court's calendar through Sept. 23 is affected.
- **mammoth-solar-cannelton** — NEW; PSC sited it Nov. 2025; construction 2027.
- **black-diamond-power** — NEW; Sept. 21 hearing.
- **fy28-flat-budgets** — NEW; income-tax trigger not met.
- **bc-conservative-exodus** — moved: ninth MLA, chief of staff Delaney out, RCMP questioned Paton (Globe) — the Paton item is unprinted and is tomorrow's bc tier if it moves.
- **google-adtech-remedy** — NEW; opinion sealed 14 days, judgment due in 30.
- **maduro-immunity** — NEW; Nov. 17.
- **edouard** — aftermath ran (East Texas flooding); remnant low dissipates today.
- **openai-astra-critical / doj-fair-use-brief / tumbler-ridge-37-suits** — all NEW.
- **hoshoryu-aki-entry** — Friday's YDC practice; **wakatakakage-kyujo** — CLOSED, printed.
- **hannan-roane / hannan-logan** — both results owed.
- **usps-mail-ballot** — ruling pending after today's hearing.
- **kenscoff-hostages / zambia / norway** — dead today per the World desk.
- **marl-psc / meta-settlement-approval / putnam-google-datacenter / nitro-elementary / milton-culloden / bluefield-state / fundamental-data-appeal** — pending, not run.

### Covered slugs, 2026-09-03

`iran-strikes-kuwait-uae-bases`, `edouard-east-texas-21-inches`, `google-adtech-no-breakup`, `beige-book-modest-datacenters`,
`maduro-immunity-motion`, `nepal-toll-1252`, `malta-fenech-acquitted`, `pacific-forum-china-missile`, `nigeria-us-troops-withdraw`,
`wooton-medical-incident`, `mammoth-solar-cannelton-350m`, `fy28-flat-budgets-46m`, `black-diamond-no-deal`,
`huntington-marshall-houses-reinspect`, `putnam-us35-safety-review`, `parkersburg-recycling-fee-3`, `rocket-boys-pipestem-riley`,
`bennington-bridge-6-complete`, `holly-river-festival-sept5-6`, `pender-930-homes-denied`, `pg-wich-homicide`, `lyn-hall-northern-health`,
`bc-ninth-mla-delaney-resigns`, `gas-tax-holiday-jan31`, `saturn-south-decagon`, `venetoclax-siv-reservoir`, `galaxies-hydrogen-star-formation`,
`alzheimers-cd8-lymph-nodes`, `openai-astra-critical-cyber`, `doj-openai-fair-use-brief`, `tumbler-ridge-37-suits`,
`reds-padres-7-3`, `giants-pirates-5-4-10`, `chelsea-camara-monaco-collapse`, `marshall-gibson-penn-state`, `bengals-stewart-pads`,
`wvu-depth-chart-or`, `wakatakakage-aki-kyujo`, `hoshoryu-last-minute`, `brewers-cubs-9-5`, `nba-clippers-ballmer-suspended`,
`flounder-day-three`, `kingfish-scoping-tonight`

## 2026-09-04 — No. 31 (Times) and No. 21 (Sports & Sportsman)

| Open-ended | **Tenth morning under the digest contract.** Six parallel research agents (lead/U.S./World, WV notebook, Canada, Sci/AI, sports teams and leagues, outdoors). The Times was validated, rendered and pushed at **5:46 a.m. ET** and Sports at **5:49**, 19 minutes after the 5:30 wake; Pages served both dated pages 200 by 5:49:28. `send_later` armed for 6:56, digest posted in the FOREGROUND with `--not-before 07:00`, held 3 minutes and **landed at 7:00:01 ET** (1,029 embed chars, hero attached, Home link, zero degraded). Keep the pattern | **standing practice** |
| Open-ended | **Detached HEAD at session start again — eighth occurrence** (Aug 27, 28, 30, 31, Sept 1, 2, 3, 4). `git checkout main` while HEAD matched origin/main fixed it before any work. The stored prompt is the thin pointer (second morning) and handed over one webhook only | **OPEN — recurring** |
| Open-ended | **Lead art drew the lead for the first time in a week — rung 1.** France 24's live-page og:image was tankers off Bandar Abbas (no people, no damage); drawn as three vessels at anchor, placed on the lead. The CBS live-blog image was hospital casualties and was not drawn | |
| Open-ended | **`reference/topsail-fishing.md` had a WRONG sheepshead limit** (10" FL, 10/day, from the Aug. 5 research). NCDMF's limits page effective Sept. 2, 2026 says **14" TL, 5/day**. Corrected in the reference file this morning; the paper never printed the old figure. The regs block in that file is memory, not a source — it says so itself — but a wrong memory is worth fixing | **done** |
| Open-ended | **Source status.** NEWLY BLOCKED: **Prince George Citizen (403 on every path — was reliable)**, My PG Now, CBC, Castanet, Energeticcity (all 403), Politico homepage (refused), Houston Public Media (403), Nature.com (login wall on every article), Space.com (membership shell), USACE Huntington (503), sponichi.co.jp (refused; its text was read on Yahoo Japan article pages), chunichi sumo section (404), football.london and Liverpool Echo (refused), Point Pleasant Register (503), Al Jazeera Sept. 4 Iran liveblog (header only). OPENED: wvmetronews (clean, second straight day), WSAZ, WTAP, WCHS, WVPB, WOAY, Hinton News, Register-Herald (once), Bennington Banner, Port City Daily, WECT, surfcitync.gov, northtopsailbeachnc.gov, topsailbeachnc.gov, webstercountytourism.com, CKPG, CHEK, Global, CP24, CKOM, news.gov.bc.ca, deq.nc.gov (news + limits page; the proclamation PDFs cannot be text-extracted here — cite the DMF releases and the limits page instead), fishermanspost.com (September Topsail monthly, Sept. 1), coastalanglermag.com, api.weather.gov, fs.usda.gov, Okinawa Times (Kyodo copy), Yahoo Japan (Sponichi/Nikkan copy), sumostats, sumo.or.jp/En, CBS box scores/previews, mlb.com/scores, Sky Sports, FOX Sports, liverpoolfc.com, columbuscrew.com, fccincinnati.com, bengals.com, clevelandbrowns.com, Athens Messenger, MaxPreps, Dominion Post. NOTE: CBS and FOX schedule pages render kickoff times in UTC to this fetcher — convert, and confirm home/away from the CBS preview slug (MIL@CIN exists; the mlb.com scores page mislabeled the Reds as the road team) | **watch** |
| Open-ended | **Traps dodged.** (1) chelseafc.com served a STALE 2024-25 "Maresca confirms goalkeeper" article as if current — Chelsea's head coach is Xabi Alonso per Sky; (2) a search-snippet "Forest have won the last four meetings" claim was never on a page and was not printed; (3) three ScienceDaily items dated Sept. 3 were March, July and August papers; (4) commerce.wv.gov's dove release is the 2024-25 one; (5) TechCrunch and Google differ on WeatherNext 3's rain-forecast improvement (60% vs "up to 50%") — the item was left out rather than pick a number; (6) the ISRO mission page still carries an Aug. 29 date header for Friday's launch — The Tribune's dated story ran instead | |
| Open-ended | **The `result` gate caught nothing today because the desk pre-empted it**: Onosato's "10-5" and Kirishima's "10-6" practice tallies and Liverpool's "2-2 draws" were written as words before validation. Any `\d+-\d+` in a sports brief is a score to the validator | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **U.S.-Iran led a FOURTH straight morning, on the diplomatic and economic side**: Vance's no-talks-until-shipping-stops line and his "not a war" framing, Kuwait's interceptions, UAE's denial, Brent $95.67, Hormuz at 102 transits a day (Lloyd's List via CBS), record diesel $5.85 (AAA). Iran's toll unchanged at 18. Tomorrow: any U.S. answer, South Korea's Hormuz decision, the wedding-strike investigation, Sept. 26 UNSC vote | |
| **2026-09-04** | **August jobs report (BLS) is due this morning; not in the paper** | Saturday's U.S. brief if it moves markets |
| **2026-09-08** | **Justice Jackson's deadline for responses to the DOJ's Supreme Court application on the USPS mail-ballot rule (Tuesday); Canada counter-tariffs effective** | Talwani has still not ruled on the injunction; USPS says the portal is usable "sometime next week" |
| **2026-09-05** | **College football opens: WVU v. Coastal Carolina (noon, TNT, Pat White's No. 5 retired 11:45), Marshall at No. 18 Penn State (3:30, FS1), Ohio at Nebraska (noon, FS1, Poulos starting); Tottenham at Forest 10 a.m. ET; Crew v. Colorado and FCC v. D.C. United 7:30 p.m. ET; Reds v. Brewers and Pirates v. Angels series (both HOME; weekend times unconfirmed on a readable page); squirrel youth weekend; Lilly Mountaineers at Jerry Run 7 p.m.** | Saturday's whole sports paper |
| **2026-09-06** | **Chelsea at Arsenal 11:30 a.m. ET; No. 7 WVU women host Marshall 7 p.m.** | |
| **2026-09-07** | **WV gun bear first window closes (selected counties)** | Ran in going-out with the no-county-list caveat |
| **2026-09-09** | **NFL Kickoff, Patriots at Seahawks 8:20 p.m. ET; Hannan v. Point JV 6 p.m.; Crew at D.C. United and FCC at Philadelphia 7:30 p.m. ET; Webster County Fair opens (through Sept. 12); Croft Road at PG council; King Harald's funeral; DoubleTree deadline** | |
| **2026-09-10** | **Hannan v. Westside at Shawnee (Institute); Surf City Shoreline & Resiliency Committee 9 a.m.** | |
| **2026-09-11** | **Topsail Beach 9/11 remembrance walk 8:30 a.m.; Vermont Veterans Home 25th-anniversary ceremony** | |
| **2026-09-13** | **Aki basho opens (through Sept. 27); Bengals v. Buccaneers 1 p.m. ET; Browns at Jacksonville 1 p.m. ET; North Bennington Village Block Party noon-2** | Hoshoryu's entry is still "uncertain until right before the tournament" (Sponichi via Yahoo Japan) after Friday's YDC practice — he did shiko and pushing drills, no bouts |
| **2026-09-14** | **NC flounder closes 11:59 p.m. (ran in going-out today); Bennington option-tax meetings Sept. 14 and 28** | |
| **2026-09-17** | **NCDMF kingfishes meeting, Wilmington (comments to Sept. 30); Gauley Fest opens** | Thursday's Morehead City meeting outcome was NOT reported anywhere readable |
| **2026-09-21** | **Black Diamond Power status hearing, PSC** | |
| **2026-09-26** | **Abbotsford-Mission byelection; USMNT-Peru; WV archery deer/bear and boar archery open** | |
| **2026-10-16** | **Public hearing on the $15M Hampstead freestanding ED (ran as today's Topsail line)** | Target opening June 2029 |
| **2026-11-15** | **Snowbirds' final CT-114 display at the Grey Cup, Calgary** (Global) | Not run today; a Canada brief when it nears |
| **2027-01-31** | **Walbran blockade injunction runs to this date** | Ran as a bc brief |

### Open threads

- **us-iran-hormuz** — led a fourth day (Vance no-talks line); see forward-dated row.
- **nepal-flood** — 1,287 dead / ~5,083 missing (NDRRMA Friday noon; the missing figure now includes unidentified recovered bodies — say so every time); two Trishuli 3A workers rescued after nine days; 557 of that project's workers still missing (AJ).
- **missouri-map-blocked** — NEW; AG Hanaway to petition SCOTUS.
- **usps-mail-ballot** — moved: DOJ went to SCOTUS; responses due Tuesday; no Talwani ruling.
- **treasury-race-admissions-rule** — NEW; comment period follows.
- **pacific-forum-china-missile** — CLOSED with the communique (24-hour notice ask; Nauru dissent).
- **vw-100k-cuts** — NEW; four German plants phased out from 2031.
- **uber-nigeria-uganda** — NEW.
- **mason-starwood-datacenter-12b** — NEW, the WV lead; Starwood says it funds its own infrastructure; the state's certification is the only official act so far. The NScale Monarch and Putnam Google threads are separate.
- **wooton-medical** — CLOSED: back at work Thursday; arguments to be rescheduled.
- **brooke-principal-cameras** — NEW; superintendent action unconfirmed (snippets only).
- **vape-safety-act-suit** — NEW; injunction motion pending.
- **kanawha-flood-buyout** — NEW; applications to Sept. 30.
- **pond-creek-bridge** — moved (partial reopening); DOH says done Sept. 12. WCHS names a different bridge for the fines story — still unreconciled.
- **hampstead-freestanding-ed** — NEW; Oct. 16 hearing.
- **bennington-pfas-nsf-7-9m** — NEW.
- **north-coast-transmission-line** — NEW (groundbreaking in PG); First Nations co-ownership agreements due by end of 2026; funding figures differ by outlet ($3.9B combined fed-prov is CP/CKPG/province; Black Press says $3.5B federal) — the paper used $3.9B combined.
- **bc-conservative-exodus** — moved: Eby says NDP won't court the nine; Findlay called a caucus meeting (CTV, unreadable); Giddens (PG-Mackenzie) staying and calling for a "bigger tent" (CKPG, unprinted, a PG brief if it moves).
- **walbran-injunction** — NEW.
- **ontario-byelections** — CLOSED (PCs and NDP held).
- **via-rail-313-cars** — NEW; no delivery timeline.
- **eby-openai-tumbler-ridge** — Eby called OpenAI's mediation exit "inexcusable" and said B.C. intends to join the suits (CP24) — UNPRINTED today (AI section was full); tomorrow's bc or AI brief if it moves. CP's count is "30 new lawsuits"; the desk's is 37 total (30 new + 7 earlier) — consistent.
- **isro-gslv-f17 / bepicolombo-mtm-separation / pig-kidney-271-days / nagoya-nanoribbon** — all NEW; BepiColombo orbit insertion Nov. 21.
- **crew-13** — no movement; no new date.
- **nvidia-hugging-face-12-9b / uk-parliament-ai-text-15pct / kaist-safeql** — all NEW.
- **google-weathernext-3** — UNPRINTED (conflicting improvement figure); a brief if an independent evaluation appears.
- **hoshoryu-aki-entry** — moved (YDC practice, no bouts, "uncertain until right before"); decision by Sept. 12. **kirishima-tsunatori** — NEW: 10 of 16 in practice, Hakkaku unimpressed.
- **hannan-logan / hannan-roane** — BOTH results still owed; MaxPreps lists neither match. Point Pleasant Register 503. Try WSAZ/WOWK high-school pages and Logan's MaxPreps again Saturday.
- **marshall-women-murray-state (Thu) / wvu-men-akron (Thu, possibly weather no-contest)** — both uncited; likely die quietly.
- **liverpool-nguessan / spurs-richarlison-omitted / crew-zaroury / fcc-malatini-doudera / spurs-dazn / ohio-poulos-starter / wvu-white-out-pat-white** — all ran or noted today.
- **kingfish-scoping** — Morehead City outcome unreported; Wilmington Sept. 17.
- **jolthead-porgy-record** — ran in the seasons note.
- **marl-psc / meta-settlement-approval / putnam-google-datacenter / nitro-elementary / milton-culloden / bluefield-state / fundamental-data-appeal / black-diamond-power / justice-2028-run (MetroNews interview, unprinted) / kenscoff-hostages / malta-fenech / maduro-immunity** — pending, not run.

### Covered slugs, 2026-09-04

`vance-no-iran-talks-shipping`, `missouri-map-blocked`, `doj-scotus-mail-ballot`, `treasury-race-admissions-501c3`, `steinem-dies-92`,
`nepal-toll-1287-tunnel-rescue`, `pacific-forum-24h-notice`, `vw-50k-more-cuts`, `uber-exits-nigeria-uganda`,
`mason-starwood-datacenter-12b`, `wooton-back-at-work`, `brooke-principal-cameras`, `vape-safety-act-suit`,
`cabell-ems-sim-lab`, `kanawha-flood-buyout-2m`, `pond-creek-bridge-partial`, `summers-deputies-sworn`,
`bennington-college-pfas-7-9m`, `lilly-mountaineers-jerry-run-sept5`, `hampstead-freestanding-ed-15m`,
`north-coast-line-groundbreaking-pg`, `eby-wont-court-defectors`, `walbran-injunction-2028`, `ontario-byelections-held`, `via-rail-313-cars-4-7b`,
`isro-gslv-f17-eos05`, `bepicolombo-mtm-separation`, `pig-kidney-271-days-lancet`, `nagoya-switchable-nanoribbon`,
`nvidia-hugging-face-12-9b`, `uk-parliament-ai-text-15pct`, `kaist-safeql-87pct`,
`liverpool-barcola-ipswich-nguessan`, `spurs-richarlison-omitted`, `pirates-giants-5-2`, `wvu-white-out-pat-white-no5`,
`ohio-poulos-starter`, `bengals-weekend-off-chase-higgins`, `crew-zaroury-loan`, `hoshoryu-ydc-practice-no-bouts`,
`kirishima-tsunatori-10-of-16`, `cubs-brewers-2-1-pca-39`, `nfl-kickoff-patriots-seahawks`,
`flounder-day-four-going-out`, `red-drum-slot`, `seatrout-slot`, `squirrel-youth-sept5-6`, `bear-youth-sept12-13`, `bear-gun-closes-sept7`,
`jolthead-porgy-record`, `tea-creek-bridge-williams`

## 2026-09-05 — No. 32 (Times) and No. 22 (Sports & Sportsman)

| Open-ended | **Eleventh morning under the digest contract.** Seven parallel research agents (lead/U.S./World, WV notebook, Canada, Sci/AI, Our Teams, Around the Leagues + sumo, outdoors/water). Both papers validated, rendered and pushed at **5:51 a.m. ET**, 21 minutes after the 5:30 wake; Pages served both dated pages 200 at 5:51:37, about 30 seconds after the push. `send_later` armed for 6:56, digest to post in the FOREGROUND with `--not-before 07:00`. No detached HEAD this morning — the clone came up on `main` matching `origin/main` (first clean start since Aug. 26). `config.head_start_minutes` reads 90 against the 5:30 wake; `edition.md` §0 still says "should be 60" from the 6:00 era and is stale on that one number | **standing practice** |
| Open-ended | **Lead art fell to rung 2 for a stated reason.** The envoy story's photographs are Witkoff and Kushner at a lectern and a Putin/Zelenskyy composite — faces, out under §4.5. Drew Bennu from the OSIRIS-REx mosaic on phys.org (the Sci/Tech Nature Communications brief), placed in Science & Technology; the PBS ballot-carton image was the other candidate and is a close-up of boxes, not a scene. Generated from a seeded Python script (162 path elements, 30 KB) — crude, but a rubble pile with a limb and a terminator. Not a FAILURES line | |
| Open-ended | **The NC hunting-season gate.** The validator refuses any NC `seasons` entry whose source is not NCDMF/Marine Fisheries, so NCWRC dates (dove opened TODAY Sept. 5, teal Sept. 10-19 east of U.S. 17, archery deer Sept. 12) ran in the seasons `note`, attributed to the Wildlife Resources Commission, not as bucket entries. That is the validator doing what it was written to do for Topsail fish; if NC hunting is wanted as entries, the rule needs a hunting carve-out and that is Nate's call, not the desk's. WV dove dates are now printable: the West Virginia Daily News (`wvdn.com/200186/`, July 14) carries the DNR release — Sept. 1-Oct. 11, Nov. 2-15, Dec. 7-Jan. 10, 15/day, HIP required; ran in the note today | **OPEN — for Nate** |
| Open-ended | **Yesterday's sumo attribution may be off.** No. 21 credited Hakkaku's "hips are still too high" to Kirishima (Nikkan). Today's desk read Nikkan's Sept. 4 12:28 JST piece and found that line said of ONOSATO ("he'll probably struggle this tournament too"); Hakkaku's Kirishima line was "lacks forward drive... must take strong sumo, not skilful sumo." Not re-verified against the exact page No. 21 cited; a correction is warranted only if someone opens that page and confirms | **watch** |
| Open-ended | **Hannan schedule mismatch worth asking Ian.** Roane County's MaxPreps page shows Roane home to Webster County on Sept. 2 and at Tyler on Sept. 3 — no Sept. 1 match with Hannan — and Logan's shows no Sept. 3 fixture. Both of Ian's fixtures remain unreported anywhere; the paper printed only that no score was published. Roane is due at Ashton Sept. 24 on both his doc and Roane's page | **OPEN** |
| Open-ended | **Source status.** NEWLY BLOCKED: **wvmetronews.com** (403 on every path, after two clean mornings), Prince George Citizen, My PG Now, CBC, Castanet (all 403 again), National Post, CTV article bodies (index only), Japan Times sumo (402), USACE Huntington (503), USACE Great Lakes news (403), NIH and NOAA news indexes (403), science.org, journals.aps.org, politico.eu, wvnews.com, jdnews.com, topsailvoice.com (503), bennington.edu (403), Athlon, WBOY, Point Pleasant Register (503, third day). OPENED: PBS, CBS, Al Jazeera articles (liveblogs header-only), Euronews, Kathmandu Post, Africanews, ABC Australia, KSHB, SCOTUSblog, BLS, WSAZ, WTAP, WCHS, WVPB, WVVA, WOAY, Lootpress, Dominion Post, News & Sentinel, Intelligencer, West Virginia Record (now at legalnewsline.com/west-virginia-record/), Herald-Dispatch (2 loads), Bennington Banner, Pender County CivicAlerts, WECT, WWAY, Port City Daily, surfcitync.gov, northtopsailbeachnc.gov/news, webstercountytourism.com, wvstateparks.com, americanwhitewater.org, CKPG, CHEK (after 429s), Global, CP24, CJME, news.gov.bc.ca, StatCan, TechCrunch, The Register, Gizmodo, phys.org, EurekAlert, UCR/MIT/NASA, anthropic.com, collusion.wiki, deq.nc.gov (limits, releases, PA-45 PDF), ncwildlife.gov PDFs (media/5176 and the at-a-glance sheet — the HTML season pages 404), fishermanspost.com, coastalanglermag.com, api.weather.gov, fs.usda.gov, wvdn.com, wvexplorer.com, outdoorlife.com, Kumanichi (kumanichi.com — NEW, Kyodo sumo copy without a paywall), daily.co.jp, Yahoo Japan article pages, sumostats, ryogokukokugikan.com, sumo.or.jp/En, CBS box scores (doubleheader nightcap slug is `_2`), CBS wild-card standings (`/mlb/standings/wildcard/` — the only wild-card table that loads), mlb.com/scores (until it 406'd mid-run), Sky Sports, FOX schedules/standings (UTC times — convert), liverpoolfc.com, tottenhamhotspur.com articles, chelseafc.com article (undated — corroborated by a dated Sky video), fccincinnati.com, bengals.com, clevelandbrowns.com, MaxPreps, Logan Banner, Athens Messenger, SI, ussoccer.com, gostanford.com | **watch** |
| Open-ended | **Traps dodged.** (1) ScienceDaily "Stanford seafood reverses aging" is a 2022 Frontiers paper from XJTLU. (2) EurekAlert 1142356 is dated Sept. 5 for a July 22 paper. (3) Sports Hochi "Aonishiki to hospital" is May 6. (4) Kyodo "Atamifuji 7 straight" is Aug. 24. (5) SI's Penn State preview and two MLS previews date Saturday as "Sept. 6." (6) commerce.wv.gov's dove release is 2024-25; gazette-mail Gauley dates are 2023; aceraft.com shows 2025. (7) Port City Daily printed the Abbey Nature Preserve grant as $50,000; WECT, WWAY and the county say $500,000 — cited the county. (8) The B.C. TFL 30 prior cut (~412,000) was back-calculated by the fetcher, not on the page — printed only 340,000 and 17.6%. (9) Al Jazeera's envoy page was summarized as "Sept. 7-8" — CBS and Euronews say Saturday/Sunday. (10) Gold and Blue Nation "scoreless draw with Akron" hits are 2025 and 2021. (11) The Belleville incest verdict was "last week" despite a Sept. 4 dateline. (12) WVPB's Distance Run summary said "Saturday, September 6" | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **Witkoff and Kushner in Moscow today, Kyiv Sunday** — the lead; Zelenskyy's strike pause holds while they are in Moscow | Sunday's lead if Kyiv produces anything; U.S.-Iran dropped to a U.S. brief (Trump "small potatoes," Pickaxe Mountain threat, Tasnim's Kharg tanker claim unconfirmed by CENTCOM) after four mornings leading |
| **2026-09-06** | **Chelsea at Arsenal 11:30 a.m. ET; Reds-Brewers finale 12:10; Pirates-Angels finale 1:35 (Skenes); WVU women v. Marshall 7 p.m.; Starlink 15-24 from Vandenberg NET 6:59 a.m. EDT; Aonishiki's Nagoya yusho parade (Nikkan, unread); Red Dress march to Lheidli T'enneh Memorial Park** | Saturday's results are Sunday's teams section: Spurs at Forest, WVU-Coastal, Ohio-Nebraska, Marshall-Penn State, Crew-Colorado, FCC-D.C., Reds, Pirates |
| **2026-09-07** | **Missouri: responses due on Hanaway's SCOTUS application (she asked for a ruling Monday); Reds at Dodgers 9:10 p.m. ET; Pirates off; Aonishiki resumes bouts; WV gun bear first window closes; Canada Labour Day; NTB offices closed** | |
| **2026-09-08** | **Missouri ballot deadline; Justice Jackson's USPS response deadline; Canada counter-tariffs effective; UNBC classes begin; Reds at Dodgers (time unread); Pirates at White Sox (time unread); North Bennington trustees 7 p.m.** | |
| **2026-09-09** | **NFL Kickoff; King Harald's funeral 1 p.m. Oslo; Hannan v. Point JV 6 p.m.; Crew at D.C. and FCC at Philadelphia 7:30; Webster County Fair opens (through 12th); Holly River farm-to-table 5:30; Croft Road VP2026-29 at PG council** | |
| **2026-09-10** | **Hannan v. Westside at Shawnee, Institute, 6 p.m.; NC September teal opens (east of U.S. 17, through Sept. 19); Guyandotte floodwall gate exercise; Surf City Shoreline committee 9 a.m.** | |
| **2026-09-11** | **Hoshoryu's Aki entry decided at the JSA bout-drawing meeting (morning JST = Thursday evening ET); U.S. CPI; Gauley season releases begin (through Oct. 18); Reds at Brewers and Pirates at Cubs (times unread); Topsail 9/11 walk 8:30** | |
| **2026-09-12** | **WV squirrel general and NC archery deer open; WV youth bear weekend (12-13); WVU v. UT Martin 1 p.m., Ohio v. Jacksonville State 6, Marshall v. MTSU 7 (all ESPN+); Liverpool v. Fulham 10 a.m., Spurs v. Everton 12:30; Crew v. Red Bulls and FCC v. Charlotte 7:30; Pond Creek Bridge due finished** | |
| **2026-09-13** | **Aki basho opens (through 27th); Bengals v. Bucs and Browns at Jaguars 1 p.m. ET; Bennington option-tax survey closes** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m.; Brooke principal's preliminary hearing; Bennington Select Board option-tax session; ESA FLEX/Sentinel-3C on Vega-C VV30 (9:21 p.m. EDT)** | FLEX is a Sept. 15 Sci/Tech brief |
| **2026-09-16** | **Fed meeting (hike odds near 60% after the jobs report); Lake Paran septic workshop, North Bennington, noon** | |
| **2026-09-17** | **Gauley Fest opens (through 20th); NCDMF kingfishes meeting, Wilmington** | |
| **2026-09-21** | **Black Diamond Power PSC hearing; D-SNAP applications open in Lewis, Pleasants, Ritchie, Upshur (through 25th)** | |
| **2026-09-23** | **Pender resiliency-plan comment window closes; Tumbler Ridge ChatGPT case-management conference (Judge Schulman — from a law-firm summary, unverified); Uber Nigeria/Uganda help center closes** | |
| **2026-09-26** | **Abbotsford-Mission byelection; USMNT-Peru 4:30 p.m. ET Orlando; WV archery deer/bear open; Chelsea at Brentford is Sept. 18** | |
| **2026-09-29** | **Clancy status hearing (mistrial declared Friday, PBS)** | Not run today; a U.S. brief if a retrial decision comes |
| **2026-10-05** | **B.C. legislature returns; the Milobar party aims to be registered by then; Bennington special meeting on the option tax (vote Nov. 3)** | |
| **2026-12-02** | **SCOTUS argues the AR-15 ban cases (Viramontes / Grant); Dec. 8 RNC v. Mi Familia Vota** | Not run today (SCOTUSblog) |

### Open threads

- **witkoff-kushner-moscow-kyiv** — NEW, the lead; Kyiv stop Sunday.
- **us-iran-hormuz** — dropped to a brief after four leads; Kharg tanker report (Tasnim) unconfirmed; polygraphs of ~50 Joint Staff (AJ citing NYT) unprinted; Brent $96.90 Friday (Fortune).
- **usps-mail-ballot** — MOVED: Talwani preliminary injunction Friday; 1st Circuit appeal promised; SCOTUS responses Tuesday.
- **missouri-map** — MOVED: Hanaway's emergency application; responses Monday, ballot deadline Tuesday.
- **august-jobs-162k** — ran; CPI Sept. 11, Fed Sept. 16.
- **nepal-flood** — 1,342 dead / 4,886 missing, now NEPAL POLICE at 8 a.m. daily via the Kathmandu Post (not the NDRRMA); Saturday's piece did not say whether the missing count includes unidentified bodies — attribute that caveat to Friday's NDRRMA figure only.
- **sara-duterte-warrant** — NEW; Philstar/NPR snippets say she posted bail Saturday (unverified).
- **reform-uk-donations-sting** — NEW; Met referral.
- **guinea-landfill** — NEW (funeral peg).
- **milei-falklands / clancy-mistrial / scotus-dec-ar15 / germany-grid-sabotage / unga-equal-earth-map** — read, not run.
- **brooke-cameras** — MOVED: three suits, suspension, Sept. 14 hearing. **ruby-memorial-cameras-class-action** — NEW (WV Record, Sept. 1 filing), unprinted, a statewide brief when it moves.
- **mason-starwood-datacenter** — MOVED: reaction and the HB 2014 request.
- **rhtp-first-awards** — NEW. **chamber-summit** — panels ran (GOP economic panel); the childcare HB 4191 panel (News & Sentinel) is unprinted.
- **justice-2028-run** — Justice "100 percent" considering (Lootpress/WOAY, Thursday), still unprinted; a brief if he decides.
- **milton-culloden** — MOVED (regional line: "early stages," no petition).
- **wayne-ai-threats / dsnap-four-counties / wood-assessor / belle-fire / hinton-apartments** — ran or noted.
- **hannan-roane / hannan-logan** — still owed; schedule mismatch (see table).
- **wvu-men-akron / marshall-women-murray-state** — Thursday results never found; the Sunday women's match may reveal Marshall's record.
- **hoshoryu-aki-entry** — MOVED: hospital Saturday, decision Sept. 11. **atamifuji-ozeki-run** — NEW (needs 12). **kirishima-tsunatori** — degeiko from Sept. 5 (Sponichi), a Sept. 9 Onosato rematch is sumostats-only, unconfirmed. **shindo-57kg-recruit** — read, not run.
- **liverpool-iraola-first-win / spurs-maddison-out / chelsea-caicedo / reds-brewers-10-7 / pirates-angels-1-0 / ohio-nebraska / marshall-penn-state / fcc-dc-united** — ran.
- **hof-voting-overhaul / guardians-double-walkoff / miami-mensah** — ran in leagues.
- **bc-new-party-milobar** — MOVED: five MLAs, registration before Oct. 5; Findlay's caucus meeting outcome unreported; Paton/RCMP last moved Sept. 1. **giddens-bigger-tent** — read (CKPG), not run.
- **brink-pg-cuts / tfl30-cut** — NEW, ran. **pg-council-race** (Pears, Klassen) — a roundup line on a thin day. **pg-college-heights-gunfire** — read, not run.
- **statcan-august-jobs / fca-ei-maternity** — NEW, ran. **jazz-flight-attendants-strike-mandate / zahid-arson-charge / vpd-dosanjh-fraud / surrey-treatment-facility / duncan-gala-vista / victoria-transit-mediation** — read, not run.
- **eby-join-openai-suits** — ran (AI section) as the Tumbler Ridge movement.
- **openai-agents-dsewiki / anthropic-flt-lean** — NEW, ran. **wayve-uber-london / weathernext-3-leaderboard** — read, not run (WeatherNext still has no independent evaluation readable).
- **ucr-kamchatka-gps / katalyst-link-swift / mit-cellular-self-reporting / bennu-1-pascal** — ran. **manchester-magic-angle / betelgeuse-alma / cicadas-50-yards / mercury-graphite-crust / x59-mach-1-2 / hubble-n44** — alternates, unprinted.
- **crew-13** — no new date. **esa-flex-sept14** — NEW forward item.
- **blue-catfish-record-harmon / gauley-season-sept11 / wv-dove-dates / nc-dove-teal-archery / dmf-fmp-review / topsail-shellfish-pa45** — ran in the seasons and water notes.
- **kingfish-scoping** — Wilmington Sept. 17. **summersville-drawdown** — USACE unreachable again.
- **fr86-williams-river-road** — closure posted to end Aug. 31, still listed; ran in the Williams note.
- **marl-psc / meta-settlement-approval / putnam-google-datacenter / nitro-elementary / bluefield-state / fundamental-data-appeal / black-diamond-power / pond-creek-bridge / mammoth-solar / vape-safety-act-suit / wooton / kenscoff-hostages / malta-fenech / maduro-immunity / pacific-forum / nigeria-us-troops / king-harald-funeral** — pending, no movement found.

### Covered slugs, 2026-09-05

`witkoff-kushner-moscow-kyiv-peace-proposal`, `talwani-injunction-usps-mail-ballot-rule`, `august-jobs-162k-hike-odds`, `missouri-hanaway-scotus-emergency-application`,
`trump-small-potatoes-pickaxe-mountain`, `nepal-toll-1342-police-4886-missing`, `sara-duterte-arrest-warrant-grave-threats`, `reform-uk-aides-suspended-donations-sting`,
`guinea-conakry-landfill-36-buried`, `brooke-cameras-three-suits-class-action`, `mason-starwood-reaction-hb2014`, `rhtp-first-awards-2-4m`, `chamber-gop-panel-sb1-pers`,
`milton-annexation-early-stages`, `belle-witcher-creek-fire`, `wood-assessor-shortfall-two-thirds`, `hinton-new-river-grocery-apartments`,
`vt-purple-heart-duverney`, `bergoo-bash-sept5`, `pender-abbey-preserve-500k`,
`brink-pg-fingerjoint-85-to-30`, `tfl30-aac-340k-cut-17pct`, `bc-new-party-five-mlas-milobar`, `statcan-august-jobs-minus-42k`, `fca-ei-maternity-charter`,
`ucr-asperity-gps-kamchatka-grl`, `katalyst-link-swift-12km-boost-dropped`, `mit-cellular-self-reporting-cell`, `bennu-1-pascal-coffee-nature-comms`,
`openai-agents-dsewiki-18000-posts`, `anthropic-claude-flt-lean-13m-lines`, `eby-province-join-tumbler-ridge-suits`,
`chelsea-arsenal-caicedo-decision`, `liverpool-isak-brace-ipswich-2-0-barcola-debut`, `spurs-forest-maddison-out-savio-back`, `brewers-reds-10-7-pratt-triple`,
`pirates-angels-1-0-jones-ninth-shutout`, `ohio-nebraska-keys-poulos-colandrea`, `marshall-penn-state-campbell-debut-gibson`, `fcc-dc-united-home-form-noonan`,
`hoshoryu-hospital-decision-sept11`, `atamifuji-ozeki-run-hakkaku-praise`, `guardians-double-walkoff-wildcard`, `hof-voting-overhaul-belichick`, `miami-mensah-five-td-stanford`,
`squirrel-general-sept12`, `bear-youth-sept12-13`, `squirrel-youth-today`, `spanish-mackerel-limits`, `flounder-day-five-fmp-review`, `bear-gun-closes-sept7`,
`nc-dove-opens-sept5`, `wv-dove-dates-wvdn`, `wv-blue-catfish-record-harmon`, `gauley-season-sept11`, `fr86-williams-river-road`, `topsail-shellfish-reopen-pa45`, `topsail-heat-advisory-rip-moderate`

## 2026-09-06 — No. 33 (Times) and No. 23 (Sports & Sportsman)

| Open-ended | **Twelfth morning under the digest contract.** Seven parallel research agents (lead/U.S./World, WV notebook, Canada, Sci/AI, Our Teams, Around the Leagues + sumo, outdoors/water). Both papers validated, rendered and pushed at **5:50 a.m. ET**, 20 minutes after the 5:30 wake; Pages served both dated pages 200 at 5:51:07, 33 seconds after the push. `send_later` armed for 6:56, digest posted in the FOREGROUND with `--not-before 07:00`, held 3 minutes and **landed at 7:00:01 ET** (message 1546112732066226187, 1,013 embed chars, hero attached, Home link, zero degraded). **Detached HEAD at session start again — ninth occurrence** (Aug 27, 28, 30, 31, Sept 1, 2, 3, 4, 6; clean on the 5th); `git checkout main` while HEAD matched origin/main, then `git pull --rebase`, fixed it before any work. `config.head_start_minutes` reads 90 against the 5:30 wake; `edition.md` §0 still says "should be 60" | **standing practice / OPEN — recurring** |
| Open-ended | **Lead art drew the lead — rung 1, second time in three days.** The AP photo on ABC's wire story is the Bandar Abbas anchorage (Sept. 4: ships at anchor, a motorboat, a swimmer); Friday's drawing was the same anchorage as three vessels close up, so today's is the wide view — a hazy horizon strung with seven hulls, an open boat crossing mid-water with its wake, chop in the foreground. Generated from a seeded Python script (176 paths, 25 KB), figures as two contour loops, no faces. The NBC image was CENTCOM strike footage and was not drawn | |
| Open-ended | **The lead is U.S.-Iran again, on the fifth day out of six** — the desk chose the tanker strikes and IRGC missile fire over the Moscow envoy meeting because the Kremlin produced only "a number of ideas" and no outcome; Witkoff/Kushner ran as the Europe brief (Euronews, Sunday 8:07 CEST). Two readable outlets disagreed on Labor Day gas ($4.14 CBS/AAA vs $4.15 KBB) — the number came OUT of the lead and the KBB brief carries its own figure attributed to KBB | |
| Open-ended | **Two WV lines were cut on my own second read.** (1) The desk filed the Wood County incest verdict as "Friday"; WTAP's Sept. 4 piece says "last week's verdict" — the same trap yesterday's desk logged — so Mid-Ohio Valley ran nothing. (2) Blenko's fall collection (Herald-Dispatch) is a product release, not news; Huntington ran Marshall's Direct Admit expansion to Rock Hill High instead. Notebook: 4 statewide, 2 regional (huntington_cabell, putnam_kanawha), away 1, hotspots 2 — five lines, the thinnest since the 26th. Nicholas/Webster has now run NO regional line for three mornings (WOAY last item Sept. 1; Register-Herald 429; nicholascountywv.org news page is lorem-ipsum placeholders; Nicholas Chronicle stale since May). **The Webster County Fair's Sept. 9 opening is STILL unconfirmed on any opened page** (webstercountytourism.com 404 on every path today; fairsandfestivals.net shows 2013 dates) — do not print the date until a page says it | **watch** |
| Open-ended | **Sumo: Aonishiki's Nagoya yusho parade was rained out Sunday** (Nikkan via Yahoo Japan, 2:02 p.m. JST; Ajigawa stable; no makeup, basho a week out). No Sunday Hoshoryu item anywhere; the Sept. 11 bout-drawing decision stands. The desk also filed Hakkaku's "hips still too high" line said of ONOSATO (Tokyo Sports, Sept. 4, 10 of 15 at the soken) — held as two-day-old and already-run material, but it is a second Japanese source corroborating yesterday's note that No. 21 (Sept. 4) mis-attributed that line to Kirishima. Correction still warranted only against the exact page No. 21 cited. r/Sumo unreachable a 14th morning | **watch** |
| Open-ended | **Sports results all read from line scores**: WVU 31-24 Coastal (onside kick recovered), Penn State 45-0 Marshall, Nebraska 49-21 Ohio, Reds 5-3 Brewers, Angels 6-1 Pirates, Forest 0-0 Spurs (first point, still no goal), Crew 3-0 Rapids, FCC-D.C. POSTPONED (weather, no makeup date). `out/standings.json` (88-55 / 81-62 / 71-72 / 70-73 / 68-74, Cubs 7.0 back) matched mlb.com/standings exactly. First 0-0 draw through the `result` gate: `{winner: Forest, loser: Spurs, score: "0-0", note: "draw"}` validated clean. Hannan: Roane (Sept. 1) and Logan (Sept. 3) STILL unreported by anyone; ran as a brief saying so plus the standings line | |
| Open-ended | **wvdnr.gov FETCHED from here this morning** (National Hunting and Fishing Day page, press index, fishing page) — first time; the expired-certificate block may have cleared. Not yet relied on for a season date (the transcribed pamphlet remains the WV source); if it holds for a week, it is worth saying so in `sportsman.md`. Cobia limits NOT printed: the DMF limits page defers to proclamation FF-4-2026 (PDF unreadable) and the DEQ cobia page 403s. Bluefish trap: the DMF table says 5/day but footnote M caps private anglers at 3 — printed both. NWS river IDs for the Ohio are POPW2 (Point Pleasant) and HNTW2 (Huntington); PTPW2 404s and HNNW2 is the New River at Hawks Nest | **watch** |
| Open-ended | **Williams River jumped from 48.8 to 171 cfs overnight** after Saturday-morning storms that drew a severe thunderstorm warning for Richwood, Camden-on-Gauley, Craigsville and the Cranberry area (NWS Charleston 8:43 a.m.; hail at Craigsville, outages in Richwood). No measured basin total was published by press time (Sunday RVA/HYD issue about 9:30-11 a.m.); the water block says so. The Ohio's Saturday-morning NWS forecasts (issued before the rain) now sit below the observed stages at both gauges — printed as "above the forecast", not as a new forecast | |
| Open-ended | **Source status.** NEWLY OPENED: **wvdnr.gov**, Charleston Gazette-Mail (Justice article, no paywall), Times West Virginian, Mountain State Spotlight, Quesnel Cariboo Observer, frequencynews.ca (CFUR), NBC News (three articles), Kelley Blue Book, MPR News, Anadolu, Yahoo Sports/Yahoo Japan article pages (Nikkan, Tokyo Sports, Sponichi, AP, Evening Standard copy), Bleacher Report, WV Sports Nation, Ironton Tribune, philasportswire, api.water.noaa.gov NWPS gauges, eRegulations NC migratory digest, ABC News wire pages and live blog. STILL/NEWLY BLOCKED: wvmetronews.com (403, second day), WV Watch, WOWK, WVNS, wvgop.org, Register-Herald (429 after one load), WV Record article pages (429 x3 — Ruby Memorial class action still unopened), VTDigger (category 404), topsailbeachnc.gov news (404), webstercountytourism.com (404 all paths), CBC, Prince George Citizen, My PG Now, UNBC newsroom, Rocky Mountain Goat, Toronto Star, CNBC, The Hill, NPR (503), Ars Technica (403 both sections), aanda.org (403), ersnet.org, CBS scoreboards (fetch size), ESPN game pages (empty), mlb.com/reds/schedule (406), columbuscrew.com and mlssoccer.com (JS shells), pressherald, detroitnews (402), cnn (451), USACE Huntington (503) and LRD (403), deq.nc.gov DMF news and proclamation indexes (404), DEQ cobia page (403) | **watch** |
| Open-ended | **Traps dodged.** (1) Dec. 2025 Witkoff/Putin "five-hour meeting" items in the Moscow search. (2) Al Jazeera's tanker summary garbled disabled-vs-destroyed; resolved on NBC and the ABC live blog (Downy and Stark 1 disabled, Kylo destroyed). (3) AP's early Indonesia figures (33 flights, morning closure) superseded by Al Jazeera's 301 flights and 5:30 p.m. (4) City of Prince George's Red Dress page is the 2024 listing; used CFUR's Sept. 3 piece. (5) Intelligencer's undated "2 dead in flash floods" box is the July Buckhannon event. (6) WOAY's "youth seasons" story is Aug. 26, 2025. (7) AW's Upper Gauley page lists Sept. 17 as "next release", conflicting with the Sept. 11 opener — schedule cited to WV Explorer and the Gauley Fest page. (8) Starlink 15-24 slipped to 10:26 a.m. EDT and had not flown — not briefed. (9) Seattle Times/Newsday suit was filed Friday, not Saturday as TechCrunch's dateline implies. (10) A stale chelseafc.com Maresca article again; Alonso is the coach. (11) Search garbled the Crew's W-L-D order — no record printed. (12) Cam Cook's 142 yards existed only in a snippet — printed the 72-yard run from the opened page | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **open** | **U.S.-Iran led a FIFTH morning of six**: CENTCOM's three tankers (Downy, Stark 1 disabled; Kylo destroyed), IRGC ballistic missiles at a carrier and destroyer (evaded), Iran's 2:53 a.m. ET claim of hitting an unmanned U.S. vessel (unconfirmed by CENTCOM), Brent above $95. Tomorrow: any U.S. confirmation, oil's Sunday-evening open, AAA's Labor Day number, South Korea, the Sept. 26 UNSC vote | |
| **2026-09-06** | **Witkoff and Kushner in Kyiv TODAY after three hours with Putin** ("a number of ideas"; capital strikes paused through Monday) — Monday's lead if Kyiv produces anything; **Chelsea at Arsenal 11:30 a.m. ET; Reds-Brewers 12:10; Pirates-Angels 1:35 (Skenes); WVU women v. Marshall 7 p.m.; Red Dress stand PG 11 a.m. PT; Notre Dame-Wisconsin 7:30 p.m. ET; Starlink 15-24 10:26 a.m. EDT** | |
| **2026-09-07** | **Hurricane Lowell passes west of Kauai Monday night (Cat 4, 145 mph, up to 10 in. rain)**; Missouri responses due on Hanaway's SCOTUS application; Reds at Dodgers 9:10 p.m. ET; WV gun bear first window closes (selected counties); Canada Labour Day; Bennington Labor Day | |
| **2026-09-08** | **Missouri ballot deadline; USPS mail-ballot SCOTUS responses; New Hampshire primary; Canada counter-tariffs on $27.6B effective 12:01 a.m.; UNBC classes; North Bennington trustees 7 p.m.; Pirates at White Sox 7:40 p.m. ET; Reds at Dodgers 10:10** | |
| **2026-09-09** | **NFL Kickoff (Patriots at Seahawks 8:20 p.m. ET); RNC Dallas Sept. 9-10; King Harald's funeral; Hannan v. Point JV 6 p.m.; Liverpool v. Atletico 3 p.m. ET; Crew at D.C. and FCC at Philadelphia 7:30; Holly River farm-to-table 5:30 (ran as today's cabin line); Webster County Fair opening STILL UNCONFIRMED on any opened page; Croft Road at PG council** | |
| **2026-09-10** | **Hannan v. Westside at Shawnee 6 p.m.; NC September teal opens (east of U.S. 17, 6/day, through 19th); Surf City Shoreline committee 9 a.m.; Guyandotte floodwall exercise; Pirates at White Sox finale** | |
| **2026-09-11** | **Hoshoryu's Aki entry decided (JSA bout-drawing meeting); U.S. CPI; Gauley season opens (22 release days through Oct. 18); Nature Wonder Weekend opens (North Bend, through 13th); Cops for Cancer Tour de North leaves Fort St. John; Topsail 9/11 walk 8:30; Pirates at Cubs 2:20 p.m. ET; Reds at Brewers 7:45** | |
| **2026-09-12** | **WV squirrel general opens; WV youth bear weekend (12-13); WVU v. UT Martin 1 p.m., Ohio v. Jacksonville State 6, Marshall v. MTSU 7; Liverpool v. Fulham 10 a.m. ET, Spurs v. Everton 12:30; Crew v. Red Bulls and FCC v. Charlotte 7:30; Pond Creek Bridge due finished** | |
| **2026-09-13** | **Aki basho opens (through 27th); Bengals v. Bucs and Browns at Jaguars 1 p.m. ET; WVDNR elk tours begin (Chief Logan Lodge); Carnifex Ferry reenactment 1 p.m.; North Bennington Block Party; Bennington option-tax survey closes (171 responses as of Friday — ran as today's away line); Reds at Brewers and Pirates at Cubs finales** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m.; Brooke principal's preliminary hearing; Bennington Select Board option-tax session; ESA FLEX/Sentinel-3C on Vega-C** | |
| **2026-09-15** | **Hannan v. Parkersburg Catholic, Ashton 6 p.m.; Cops for Cancer riders at PG detachment 4:30 p.m.; Fed meeting Sept. 15-16** | |
| **2026-09-17** | **Gauley Fest opens (through 20th, 6 a.m. releases 18-20); NCDMF kingfishes meeting, Wilmington 6-8 p.m. (comments to Sept. 30)** | |
| **2026-09-19** | **WVDNR National Hunting and Fishing Day, Stonewall Resort, 9-6 ($10 adults)** — from wvdnr.gov, which OPENED today | |
| **2026-09-22** | **Quesnel council; BC Housing shelter deadline Sept. 23** | |
| **2026-09-26** | **Abbotsford-Mission byelection; USMNT-Peru; WV archery deer/bear and boar archery open** | |
| **2026-09-29** | **Clancy status hearing** | |
| **2026-10-05** | **B.C. legislature returns; Milobar party registration target** | |

### Open threads

- **us-iran-tankers-hormuz** — led a fifth day; IRGC unmanned-vessel claim unconfirmed; polygraph probe (CBS, sources) ran as a U.S. brief.
- **witkoff-kushner-kyiv** — Kyiv stop today; strike pause through Monday; Kremlin "confident" of taking the rest of the east (unprinted).
- **hurricane-lowell-hawaii** — NEW; closest approach Monday night.
- **weaponization-fund-disclosure** — NEW (magistrate judge, Virginia, Friday).
- **labor-day-gas-record** — ran (KBB $4.15; CBS/AAA $4.14 — disputed figure kept out of the lead).
- **anak-krakatau-jakarta** — NEW; two more eruptions Sunday; closure may extend.
- **kinshasa-wedding-fire-22** — NEW. **colombia-ocana-drone-3** — NEW.
- **duterte-bail** — now VERIFIED (AP via ABC, 360,000 pesos Saturday); unprinted, an alternate.
- **kennedy-center-ceiling / winona-ransomware** — read, not run.
- **nepal-flood** — no new figure Sunday (1,342 / 4,886 stands).
- **justice-2028-run** — RAN (Gazette-Mail; Thursday remarks, Morrisey's "20 months" reply).
- **wvsom-record-class / wayne-ai-threats-911 / child-snap-4000** — NEW, ran. **marshall-direct-admit-rock-hill** — regional line. **park-place-skechers-menards** — regional line.
- **wood-county-incest-verdict** — CUT (verdict "last week", not Friday). **blenko-fall** — cut (product release).
- **ruby-memorial-cameras-class-action** — WV Record article pages 429 x3; retry Monday. **belle-fire-fatality** — the Belle fire now has one death (WSAZ) — a line if it moves. **webster-county-fair-2026** — date UNCONFIRMED; find an opened page before Wednesday (WVU Extension Webster, the fair's own account).
- **bennington-option-tax** — MOVED (171 responses; closes Sept. 13; Select Board Sept. 14). **powers-market-new-owner** — read, not run (Banner Aug. 31).
- **holly-river-farm-to-table / south-topsail-classroom** — hotspot lines. **surf-city-csrm-appraisal-rfp / pender-springer-ncacc** — read, not run.
- **red-dress-pg-10-years / quesnel-shelter-funding / squamish-hiker-found / bc-burned-timber-salvage / quebec-courts-ai** — NEW, ran. **cops-for-cancer-pg-sept15 / oliver-jail-secure-care / whistler-bear-attack / salmo-iio-shooting / mccrystal-matterhorn** — alternates, unprinted.
- **american-cheetah-dna / betelgeuse-alma-hotspot / copd-air-pollution-ers / lund-nanowire-led** — NEW, ran. **roman-coronagraph-on / hachimoji-polymerase / x59-mach-1-2** — alternates.
- **seattle-times-newsday-v-openai / openai-dsewiki-confirmation / wayve-uber-london-paid** — NEW, ran. **gemini-shasta-hikers / ascii-smuggling-2-37m / nyt-v-openai-final-briefs** — alternates; Stein ruling "in coming weeks".
- **chelsea-arsenal-caicedo / spurs-forest-0-0 / reds-brewers-5-3 / crew-rapids-3-0 / fcc-dc-postponed / psu-marshall-45-0 / nebraska-ohio-49-21 / angels-pirates-6-1 / wvu-coastal-31-24** — ran. **fcc-dc-makeup-date** — owed.
- **hannan-roane / hannan-logan** — still owed; the schedule mismatch with Roane's and Logan's MaxPreps pages stands.
- **aonishiki-parade-rained-out** — ran. **hoshoryu-aki-entry** — no movement; Sept. 11. **onosato-hips-hakkaku** — read (Tokyo Sports Sept. 4), held; corroborates the No. 21 mis-attribution note. **asasuiryu-stitches** — sumostats-only.
- **guardians-jays-wildcard-tie / michigan-wmu-hail-mary / pitt-heintschel-7-td** — ran. **oregon-boise-scare / auburn-baylor-lagway** — read, not run.
- **flounder-day-six / red-drum-slot / seatrout-slot / black-drum / bluefish-footnote-m / king-mackerel-coming / squirrel-youth-ends / bear-gun-closes-sept7 / squirrel-general / bear-youth** — ran. **cobia** — NOT printed (unreadable proclamation). **jolthead-porgy-record** — ran Sept. 4's note, not repeated.
- **nhf-day-sept19 / elk-tours-sept13 / nature-wonder-weekend / gauley-season / kingfish-scoping** — seasons note.
- **williams-171-storm-rise / fr86-still-posted / tea-creek-bridge / ohio-above-forecast** — water block. **summersville-drawdown / rc-byrd-locks** — USACE unreachable again.
- **marl-psc / meta-settlement-approval / putnam-google-datacenter / nitro-elementary / bluefield-state / fundamental-data-appeal / black-diamond-power / pond-creek-bridge / mammoth-solar / vape-safety-act-suit / brooke-cameras / mason-starwood / kenscoff-hostages / malta-fenech / maduro-immunity / pacific-forum / nigeria-us-troops / king-harald-funeral / missouri-map / usps-mail-ballot / bc-new-party-milobar / crew-13** — pending, no movement found.

### Covered slugs, 2026-09-06

`us-hits-three-iranian-tankers-irgc-missiles`, `hurricane-lowell-hawaii-cat4`, `pentagon-leak-polygraphs-cbs`, `weaponization-fund-designer-disclosure`, `labor-day-gas-above-4-first-time`,
`witkoff-kushner-kyiv-after-putin-3h`, `anak-krakatau-jakarta-airport-301`, `kinshasa-wedding-fire-22`, `colombia-ocana-drone-3-soldiers`,
`justice-weighing-2028-morrisey-20-months`, `wvsom-record-79-in-state`, `wayne-ai-hoax-threats-911`, `child-snap-down-4000`,
`marshall-direct-admit-rock-hill`, `south-charleston-park-place-skechers-7brew-menards`, `bennington-option-tax-171-responses`, `holly-river-farm-to-table-sept9`, `south-topsail-classroom-reopened`,
`red-dress-pg-10-years-lheidli`, `quesnel-winter-shelter-funding`, `squamish-hiker-found-six-days`, `bc-burned-timber-salvage-5pct`, `quebec-courts-bar-generative-ai`,
`american-cheetah-puma-cousin-current-biology`, `betelgeuse-alma-hotspot-aa`, `copd-air-pollution-children-ers`, `lund-branched-nanowire-led-nano-research`,
`seattle-times-newsday-sue-openai-microsoft`, `openai-confirms-dsewiki-disclosure-framework`, `wayve-uber-london-paid-rides`,
`chelsea-arsenal-caicedo-doubt`, `hannan-roane-logan-unreported`, `spurs-forest-0-0-first-point`, `reds-brewers-5-3-mclain`, `crew-rapids-3-0-streak-ends`, `fcc-dc-postponed`, `psu-marshall-45-0-campbell`, `nebraska-ohio-49-21`, `angels-pirates-6-1-kikuchi`, `wvu-coastal-31-24-onside`,
`aonishiki-parade-rained-out`, `guardians-tigers-6-0-wildcard-tie`, `michigan-wmu-13-12-hail-mary`, `pitt-heintschel-seven-td-59-14`,
`squirrel-general-sept12`, `bear-youth-sept12-13`, `king-mackerel-coming`, `red-drum-slot`, `seatrout-slot`, `black-drum-limits`, `bluefish-footnote-m`, `flounder-day-six`, `squirrel-youth-ends-today`, `bear-gun-closes-sept7`,
`nc-teal-dove-goose-digest`, `wv-dove-wvdn`, `kingfish-scoping-sept17`, `nhf-day-sept19-stonewall`, `elk-tours-sept13`, `nature-wonder-weekend`, `gauley-season-sept11-fest`, `williams-171-storm-rise`, `fr86-alert-still-posted`, `tea-creek-bridge`, `ohio-above-nws-forecast`, `topsail-fp-sept1-five-days`, `topsail-rip-low-no-advisories`

## 2026-09-07 — No. 34 (Times) and No. 24 (Sports & Sportsman)

| Open-ended | **Thirteenth morning under the digest contract.** Seven parallel research agents (lead/U.S./World, WV notebook, Canada, Sci/AI, Our Teams, Around the Leagues + sumo, outdoors/water). Both papers validated, rendered and pushed at **5:53 a.m. ET** (commit 3e54461), 23 minutes after the 5:30 wake; Pages served both dated pages 200 at 5:53:42, about 30 seconds after the push. Digest dry-run 1,037 embed chars. `send_later` armed for 6:56, digest posted in the FOREGROUND with `--not-before 07:00`, held 2 minutes and **landed at 7:00:04 ET** (message 1546475120195801208, 1,037 embed chars, hero attached, Home link, zero degraded). **Detached HEAD at session start again — tenth occurrence**; `git checkout main` while HEAD matched origin/main fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **Lead art drew the lead — rung 1, third time in four days.** The Getty photo on ABC's story is the Prime Air 767 at rest beyond the runway end at MIA, tail fin above the perimeter fence and box trucks on the road outside. Drawn as that scene from a seeded Python script (237 paths, 20 KB): no people, no flames, faint scorch hatching on the rear fuselage only, which the story establishes. The other lead-candidate images (a press-conference still; AfD flags) were not drawn | |
| Open-ended | **The lead moved off U.S.-Iran after five days of six**: the MIA cargo-jet overrun (five dead, NTSB briefs Monday) led; CENTCOM's "total lie" denial of Iran's unmanned-vessel claim ran as a U.S. brief (CBS live blog). Two outlets disagreed on whether the dead included the pilots (NBC yes, CBS Miami unconfirmed) — printed both, attributed. AfD's 43.8% Saxony-Anhalt result was the World lead (Al Jazeera preliminary official figure; NBC's earlier projection said ~44/18.5 — the official figure was used). Cape Verde bus crash is Africanews-only and attributed | |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, mid_ohio_valley, nicholas_webster, summers_new_river), away 1, hotspots 2 — seven lines.** Nicholas/Webster ran for the first time in four mornings on WOAY's overnight Potato Festival announcement (Sept. 11-12, Summersville) — a preview, flagged by the desk, run because an announcement is an event and the region had been dark. Putnam/Kanawha ran no line because both Kanawha items (Belle fire death, Marmet festival) went statewide; the I-79 crash was the fifth candidate and the cap is four. **The Webster County Fair FINALLY printed a date — Sept. 9-12 at Camp Caesar — attributed to the carnival operator's own events page (Gambill Amusements) with a 2026 festival guide agreeing; statefairtimes.com's "Sept. 2-5" looked stale and was not used.** If a Webster County reader says otherwise, that is the row to correct. Away line: the Route 67A roundabout (Banner Aug. 31); Powers Market and the Sept. 11 ceremony are the alternates | **watch** |
| Open-ended | **Sumo: real news, not the countdown.** Onosato went 16-4 in 20 bouts against Kotozakura at Monday's Nishonoseki joint practice in Matsudo (Sports Hochi/Nikkan via Yahoo Japan, 1:37 p.m. JST); Kirishima 13-2 at Isenoumi on Sunday (Sponichi). **Correction owed to No. 22 (Sept. 5): Kyodo's Saturday report places Hoshoryu's hospital visit on SATURDAY Sept. 5, not Friday** — printed in today's leagues note; no Sunday/Monday Hoshoryu item anywhere; decision at the Sept. 11 bout-drawing meeting. r/Sumo unreachable a 15th morning | **watch** |
| Open-ended | **Sports results all read from box scores**: Arsenal 2-1 Chelsea (Caicedo not in squad), Reds 12-8 Brewers, Pirates 1-0 Angels (Skenes' first win since July 19), WVU 1-0 Marshall women's soccer (both followed, written straight), Guardians 3-2 Tigers in 10, Braves 5-4 Phillies, Notre Dame 41-13 Wisconsin, Ole Miss 41-38 Louisville. `out/standings.json` (88-56 / 81-63 / 72-72 / 71-73 / 69-74, Cubs 7.0 back) byte-matched. **The result-direction gate fired three times on honest copy** (the sumo 16-4 and 13-2 practice tallies, "pulls away from", and a headline/summary pair where the loser was named first in the headline and "beat" appeared in the summary) — all fixed in the copy, none was a wrong direction. **FC Cincinnati at Philadelphia Wednesday: FOX Sports says 7:45 p.m. ET; the club's postponement page said 7:30 on Sunday and carried no time Monday — printed FOX's 7:45 and said so in the note.** Hannan: Roane (Sept. 1) and Logan (Sept. 3) STILL unreported by anyone; sat_out, with the fixtures in the week ahead | |
| Open-ended | **fetch_fishing.py's "24h ago" and trend are read against a 48-hour window, not 24 hours.** The Williams crested at 208 cfs at 11:30 p.m. Saturday and was 166 at 5:45 a.m. Sunday; today's file says 103 cfs, `discharge_cfs_24h_ago: 48.8`, `trend: rising`. The 48.8 is Saturday 5:45 a.m. — the FIRST reading in the fetcher's `period=P2D` request (`out[key + "_24h_ago"] = first`), so the trend flag compares against two days ago and says "rising" for a river that has halved since Sunday morning. Yesterday's "53.7 a day earlier" was the same artifact. **Today's water line prints the flow and stage from the file and says "receding" in prose, with no unsourced number; the fetcher was not edited (the playbook forbids it in the routine).** A five-line fix for Nate: take the reading nearest 24 hours before the latest, not the first in the window. Logged in FAILURES.md | **OPEN — for Nate** |
| Open-ended | **Outdoors: wvdnr.gov opened a second day** (news index newest July 29; the 2026-27 migratory PDF is image-only, so teal/early goose still unquoted; dove from the July 14 release). NCDMF proclamation PDFs opened for the first time: FF-27-2026 (flounder Sept. 1-14, one fish, 15 in.) and FF-4-2026 (cobia: May 1-Dec. 31, 36 in. FL, one per person, one per private vessel from July 1) — cobia printed for the first time. DMF's Sept. 4 FMP review (flounder "early signs of recovery") folded into the flounder line. NWS Wilmington Beach Hazards Statement for Pender through 8 p.m. Monday (longshore current), rip risk high Tuesday; NHC: no Atlantic cyclones. Elk tours: WVDNR page says Sept. 6, Lootpress Aug. 28 says Sept. 13 — neither printed | **watch** |
| Open-ended | **Source status.** NEWLY OPENED: Honolulu Star-Advertiser, HI-EMA, Fox 4 Dallas, AAA Newsroom, Africanews, Anadolu briefing, ESA image pages, Isar Aerospace, Space.com via Yahoo, MedicalXpress, The Register, Sports Hochi/Sponichi via Yahoo Japan, NWA Democrat-Gazette (AP), Bleacher Report, Sky Sports F1, 100 Mile Free Press, CFJC Today, CP24, Globe and Mail, CHEK, WVVA, Lootpress, WOAY, Mountain State Spotlight, Register-Herald index, villagenorthbennington.org, benningtonvt.org (bennington.org is a parked domain), topsailbeachnc.gov news (opened today), gambillamusements.com, NCDMF proclamation PDFs, NPS Gauley page, Monongahela alerts page, NWPS gauges, NWS RLX/ILM products. BLOCKED: wvmetronews.com (403, third day), West Virginia Watch, WOWK, WVNS, WBOY, wvnews.com, Prince George Citizen, My PG Now, CBC, Castanet, National Post, Japan Times (402), Kyodo English, NHK World, Mainichi, sumo.or.jp EnSumoNews (404), usopen.org (503), USACE Huntington (503), science.org, ersnet.org, The Verge, Wired, Politico, Courthouse News, WVU Extension Webster, webstercountytourism.com, UPI, Jakarta Globe, KHON2 | **watch** |
| Open-ended | **Traps dodged.** (1) Sunday was the U.S. Open fourth round, not the men's final (that is Sept. 13) — the desk's own brief had it wrong and the agent corrected it. (2) AP Top 25 not released Sunday (Tuesday, after Labor Day games). (3) HI-EMA's "50 miles SSW of Lihue" is a typo for 500 — not printed. (4) Garlic Town (Bennington, Sept. 5) has no page confirming it happened — not written as done. (5) WOAY places Brush Creek Falls in Oak Hill, Lootpress in Bluefield — no town printed. (6) Two Webster County Fair sites are Nebraska's and Iowa's. (7) Isar says five CubeSats plus an experiment, ESA says six — no count printed. (8) WV Sports Nation's "6-0-0" is the all-time series vs Marshall, not the season record. (9) WCHS's "Saturday, September 13" for Marshall-MTSU is a Sunday; FOX has Sept. 12. (10) Bluefish table 5/day vs footnote M 3/day private — both printed. (11) The Star-Advertiser/NBC gas figure dispute stays out ($4.14 AAA vs $4.15 KBB) | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-07** | **NTSB briefing on the MIA cargo-jet overrun (Homendy, Monday); Marmet Labor Day parade 10 a.m. (Cecil Roberts expected); Hurricane Lowell passes west of Kauai Monday night as Cat 1-2; Missouri map responses due; Reds at Dodgers 9:10 p.m. ET; WV bear gun first window closes (selected counties); Beach Hazards Statement for Pender to 8 p.m.** | |
| **2026-09-08** | **WV Supreme Court hears the two "deliberate indifference" jail-death cases (Mountain State Spotlight); Parkersburg council final readings on the $25.7M PFAS filtration project and the $3 recycling charge; Canada counter-tariffs 12:01 a.m.; New Hampshire primary; AP Top 25; Quebec cabinet met Monday 6 p.m. on tariffs; North Bennington trustees 7 p.m.; UNBC classes; Pirates at White Sox 7:40; Reds at Dodgers 10:10; Liverpool pre-Atletico presser 8 a.m. ET** | |
| **2026-09-09** | **Webster County Fair opens at Camp Caesar (Sept. 9-12, per Gambill Amusements); RNC Dallas Sept. 9-10 (Vance night one, Trump night two); NFL Kickoff Patriots at Seahawks 8:20 p.m. ET; Hannan v. Point JV 6 p.m.; Liverpool v. Atletico and Chelsea v. Leeds (Carabao Cup) 3 p.m. ET; Crew at D.C. 7:30, FCC at Philadelphia 7:45 (FOX; club said 7:30); Reds at Dodgers 10:10; Holly River farm-to-table 5:30; King Harald's funeral; PG council Croft Road** | |
| **2026-09-10** | **Hannan v. Westside at Shawnee 6 p.m.; NC September teal opens (east of U.S. 17, 6/day, to the 19th); Surf City Shoreline & Resiliency Committee and Planning Board; Pirates at White Sox finale; WV charter board bylaws vote** | |
| **2026-09-11** | **Hoshoryu's Aki entry decided (JSA bout-drawing meeting); Nicholas County Potato Festival opens (Sept. 11-12, Summersville); Gauley season opens (Sept. 11-14, 18-21, 25-28, Oct. 2-5, 9-12, 17-18); Prince George nominations close; Bennington 9/11 ceremony 8:25 a.m. at the Vermont Veterans' Home; Topsail Beach 9/11 walk 8:30; Cops for Cancer leaves Fort St. John; U.S. CPI; Pirates at Cubs 2:20; Reds at Brewers 7:45** | |
| **2026-09-12** | **WV squirrel general opens; WV youth bear weekend (12-13); Nitro Boomtown Day (parade 10 a.m.); WVU v. UT Martin 1 p.m., Ohio v. Jacksonville State 6, Marshall v. MTSU 7; Chelsea v. Hull and Liverpool v. Fulham 10 a.m. ET, Spurs v. Everton 12:30; Crew v. Red Bulls and FCC v. Charlotte 7:30; Reds at Brewers 7:10; Pirates at Cubs 2:20** | |
| **2026-09-13** | **Aki basho opens (through the 27th); U.S. Open men's final; Bengals v. Bucs and Browns at Jaguars 1 p.m. ET; WVU women v. UConn 1 p.m.; Carnifex Ferry "Thunder on the Gauley" 1 p.m.; Bennington option-tax survey closes; Reds at Brewers 2:10; Pirates at Cubs 2:20** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m. (FF-27-2026); Reds v. Dodgers at GABP 6:40; Bennington Select Board option-tax session; ESA FLEX/Sentinel-3C on Vega-C** | |
| **2026-09-15** | **Huntington $10 special-event parking begins (first use Sept. 26); Cops for Cancer at PG detachment 4:30 p.m.; Hannan v. Parkersburg Catholic 6 p.m.; Fed meeting Sept. 15-16** | |
| **2026-09-17** | **Gauley Fest opens (through the 20th); NCDMF kingfishes meeting, Wilmington, 6-8 p.m.; Hannan at Westside (Beckley YMCA) 6 p.m.** | |
| **2026-09-18** | **Federal comment deadline on the West Coast oil pipeline (Victoria's objection); Chelsea at Brentford 3 p.m. ET** | |
| **2026-09-19** | **WV bear gun second window opens (Sept. 19-25, selected counties); WVDNR National Hunting and Fishing Day, Stonewall Resort, 9-6** | |
| **2026-09-26** | **Marshall home game (first $10 parking day); USMNT-Peru 4:30 p.m. ET; WV archery deer/bear and boar archery open** | |
| **2026-10-02** | **Surf City CSRM appraisal RFP proposals due 5 p.m.; DUA filing deadline Lewis/Upshur** | |
| **2026-10-17** | **Prince George civic election (advance voting Oct. 7, 8, 14, 15)** | |
| **2026-11-01** | **Parkersburg CVB president Mark Lewis retires (interim Autumn Henthorn)** | |

### Open threads

- **mia-prime-air-overrun** — NEW, led; NTSB briefing Monday; the pilots-among-the-dead question (NBC vs CBS Miami) is tomorrow's first check.
- **us-iran** — CENTCOM "total lie" denial ran as a U.S. brief; Wright "always open" to talks; 92 vessels redirected under the blockade (Anadolu, unprinted). **witkoff-kushner-kyiv** — "substantive," no deal; trilateral talks "soon" (ABC, unprinted alternate). **afd-saxony-anhalt-43-8** — ran; coalition math is the follow-up. **hurricane-lowell-kauai** — ran (refuge areas); Monday-night passage is tomorrow's line. **usps-mail-ballot-scotus-third** — ran. **rnc-dallas-preview** — ran. **nepal-mourning-900-workers** — ran. **lebanon-nabatieh-strikes-4** — ran (Anadolu counts 7). **cape-verde-bus-25** — ran. **anak-krakatau** — moved (closure to 6 p.m. Monday, 1,558 flights) but unprinted; **gaza-strikes-sunday / yemen-hais** — alternates.
- **wv-jail-deaths-deliberate-indifference** — ran; Tuesday's argument is the follow-up. **bluefield-state-brush-creek-falls** — ran; name and cause not released. **belle-fire-death** — ran (Gazette-Mail detail). **marmet-labor-day** — ran; parade today. **huntington-event-parking** — regional. **parkersburg-pfas-25-7m** — regional; Tuesday vote is the follow-up. **potato-festival-sept11-12** — regional. **thurmond-buildings** — regional. **boone-kuhn-f250 / fort-henry-days / ruby-memorial-class-action (filed Sept. 1, WV Record via Legal Newsline)** — alternates, unprinted. **cvb-lewis-retires** — unprinted.
- **route-67a-roundabout** — away line. **powers-market-new-owner / bennington-911-ceremony** — alternates. **webster-county-fair-sept9-12** — hotspot, attributed to Gambill Amusements. **surf-city-csrm-appraisal-rfp** — hotspot. **topsail-beach-911-walk / surf-city-shoreline-sept10** — alternates.
- **pg-mayoral-field-7 / fort-st-james-cat-in-the-hat / victoria-pipeline-objection / whistler-bear-attack / canada-counter-tariffs-sept8 / cape-breton-flood-death** — ran. **tour-de-north-sept15 / big-bar-fires-held / salmo-iio / sechelt-seawatch-fire / rcmp-name-tags / winnipeg-sikh-graffiti / georgina-lightning / jazz-aviation-strike-mandate** — alternates.
- **isar-spectrum-orbit / copper-chains-4000 / cadd522-menopause-mice / starlink-15-24-flew** — ran. **core-mantle-map / smoking-loneliness-ers / indonesia-peat-fires / x59-25th-flight / pulsar-glitches / jaist-anode / tyrosine-lifespan / kyoto-dark-matter** — alternates.
- **anthropic-settlement-disputes / chatbots-sleep-apnea-ers / thailand-datacenter-pause** — ran. **minnesota-nudification-xai (Sept. 4 ruling) / nhtsa-cybercab-audit / arizona-chatbot-misinformation** — alternates; **nyt-v-openai** — no ruling yet.
- **arsenal-chelsea-2-1 / spurs-scoreless-1974 / liverpool-hughes-steps-down / reds-brewers-12-8 / pirates-angels-1-0-skenes / wvu-marshall-1-0-derby / wvu-wiley-knee / bengals-stewart-doubtful** — ran. **crew-zaroury / fcc-makeup-date / browns-monken-debut / usmnt-roster** — sat out. **hannan-roane / hannan-logan** — still owed.
- **onosato-16-4-rengo / kirishima-13-2-isenoumi** — ran. **hoshoryu-hospital-saturday-not-friday** — correction noted in the leagues note. **guardians-walkoff-wildcard / braves-acuna-1000 / notre-dame-wisconsin-41-13 / ole-miss-louisville-41-38 / us-open-r16 / antonelli-monza** — ran. **nascar-bell-southern-500 / marlins-cubs-pca-40 / washington-apple-cup / patriots-injuries** — alternates.
- **flounder-day-seven / red-drum / seatrout / black-drum / cobia-ff-4-2026 / squirrel-sept12 / bear-youth / bear-gun-second-window / bear-gun-closes-today** — ran. **gauley-season / nc-teal / wv-dove / nhf-day / carnifex-ferry / jolthead-porgy / kingfishes / bluefish-footnote-m / elk-tours-date-conflict** — seasons note. **williams-receding-208-crest / fr86-tea-creek / ohio-forecast / topsail-fp-sept1-six-days / pender-beach-hazards / nhc-quiet** — water block.
- **fetch-fishing-24h-window-bug** — NEW, for Nate. **detached-head-tenth** — recurring.

### Covered slugs, 2026-09-07

`mia-prime-air-767-overrun-5-dead`, `kauai-parks-closed-refuge-areas-lowell`, `usps-mail-ballot-third-scotus-application`, `centcom-total-lie-unmanned-vessel`, `rnc-dallas-sept-9-10-preview`,
`afd-saxony-anhalt-43-8-39-of-83`, `nepal-day-of-mourning-500-trapped`, `lebanon-nabatieh-strikes-4-dead`, `cape-verde-fogo-bus-25`,
`wv-jail-deaths-deliberate-indifference-scotus`, `bluefield-state-student-brush-creek-falls`, `belle-witcher-creek-fire-death`, `marmet-labor-day-festival-blair-mountain`,
`huntington-10-event-parking-sept15`, `parkersburg-pfas-filtration-25-7m-tuesday`, `nicholas-potato-festival-sept11-12`, `thurmond-buildings-demolition`, `route-67a-roundabout-vtrans-survey`, `webster-county-fair-sept9-12-gambill`, `surf-city-csrm-appraisal-rfp`,
`pg-seven-mayoral-candidates`, `fort-st-james-cat-in-the-hat-ai`, `victoria-council-pipeline-objection`, `whistler-conflict-lake-bear-attack`, `canada-counter-tariffs-27-6b-sept8`, `cape-breton-flood-death-200mm`,
`isar-spectrum-orbit-andoya`, `copper-phthalocyanine-4000-atom-chains`, `cadd522-menopause-mice-uea`, `starlink-15-24-vandenberg-sunday`,
`anthropic-settlement-publisher-claims`, `chatbots-sleep-apnea-64pct-ers`, `thailand-datacenter-pause`,
`arsenal-chelsea-2-1-rogers`, `spurs-three-scoreless-1974`, `liverpool-hughes-steps-down`, `reds-brewers-12-8-de-la-cruz`, `pirates-angels-1-0-skenes-davis`, `wvu-marshall-1-0-wilson-derby`, `wvu-wiley-knee-carted`, `bengals-stewart-back-practice`,
`onosato-16-of-20-kotozakura`, `kirishima-13-of-15-isenoumi`, `guardians-tigers-3-2-10th-wildcard-lead`, `braves-phillies-5-4-acuna-1000`, `notre-dame-wisconsin-41-13-lambeau`, `ole-miss-louisville-41-38-carneiro`, `us-open-r16-alcaraz-sabalenka`, `antonelli-monza-from-19th`,
`squirrel-sept12`, `bear-youth-sept12-13`, `bear-gun-second-window-sept19-25`, `red-drum-slot`, `seatrout-slot`, `black-drum-limits`, `cobia-ff-4-2026`, `flounder-day-seven-fmp-review`, `bear-gun-closes-sept7`,
`gauley-season-sept11-nps`, `nc-teal-sept10-19`, `wv-dove-july14-release`, `nhf-day-sept19`, `carnifex-ferry-sept13`, `jolthead-porgy-record`, `kingfishes-sept17`, `bluefish-footnote-m`, `williams-receding-from-crest`, `fr86-tea-creek-alerts`, `ohio-tracking-forecast`, `topsail-fp-sept1-six-days`, `pender-beach-hazards-longshore`, `nhc-no-atlantic-cyclones`

## 2026-09-08 — No. 35 (Times) and No. 25 (Sports & Sportsman)

| Open-ended | **Fourteenth morning under the digest contract.** Eight parallel research agents (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Around the Leagues + sumo, outdoors/water); every one of them exhausted the 200-call WebSearch budget near the end, so late checks were fetch-only. Both papers validated, rendered and pushed at **5:55 a.m. ET** (commit 90c82a5), 25 minutes after the 5:30 wake; Pages served both dated pages 200 at 5:56:03, about 40 seconds after the push. Digest dry-run 1,172 embed chars. `send_later` armed for 6:56 to post in the FOREGROUND with `--not-before 07:00`. **Detached HEAD at session start again — eleventh occurrence**; `git checkout -B main origin/main` while HEAD matched origin/main fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **USGS was 503 on all three gauges at 5:32 and came back piecemeal.** Point Pleasant answered at 5:37, the Williams at 5:38, all three together only on the fourth try of a retry loop at 5:41:42 — and a single re-run at 5:40 then dropped a water again, so the working copy was re-fetched in a loop until "0 source errors" and NOT touched afterwards. The `discharge_cfs_24h_ago: 166.0` in today's file is the same 48-hour-window artifact logged yesterday (166 was Sunday 5:45 a.m.); the water line says "Sunday morning's post-storm reading of 166 cfs," which is what it actually is. If USGS is flaky tomorrow, loop the fetcher until all waters report BEFORE writing, and never re-run it after validating | **watch — the 24h-window bug is still Nate's** |
| Open-ended | **Lead art drew the lead — rung 1, fourth time in five days.** Hawaii News Now's og:image is the enhanced-infrared satellite frame with Lowell's core over Niihau and Kauai; drawn from a seeded Python script as a spiral of cloud bands with the island chain as simple outlines (310 paths, 41 KB), checked by rasterizing the SVG with the sandbox's headless Chromium (`/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --screenshot`), which is the first time a drawing was actually LOOKED AT before shipping. The first pass read as concentric rings and 446 paths; the fix was open log-spiral arms and a gauss-packed core. The NHC cone graphic was the alternate and was not drawn | **worth keeping: rasterize the art before committing** |
| Open-ended | **The lead was Lowell's overnight pass** — CPHC Advisory 49 (11 p.m. HST = 5 a.m. ET), Star-Advertiser 11:33 p.m. update, HI-EMA 9 p.m., Kauai County releases. No injuries in any opened source; HNN's Makaha "three people overcome by waves" video was unverified and NOT printed. The MIA NTSB briefing moved (van with seven cleaners + SUV, pilot survived with minor injuries per CBS Miami — which contradicts NBC's Sunday "two pilots among the dead"; printed CBS's Monday briefing account, attributed). Iran's "restricted zone" ran as the World lead (Al Jazeera explainer); the "new Kermanshah strikes" in a search summary were the Sept. 1-2 story and were NOT printed. Kyiv two dead came via Euronews after Al Jazeera would have been three of four World bylines. Acton: charge level conflicts (Vindicator "felony" vs. others silent) — printed "two assault counts" with no level | |
| Open-ended | **Notebook: 3 statewide, 3 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley), away 1, hotspots 2 — six lines.** Statewide dropped to three because the jail-death argument (today, 10 a.m.) had not MOVED since yesterday's brief and went to the kicker instead, and Bluefield State/Justice-2028 had no development. Nicholas-Webster ran no regional line because the Bergoo ATV crash (two dead Saturday, WCHS) is the cabin hotspot and a story runs once; Summers had nothing within 48 hours (Hinton News newest Sept. 2). **Webster County Fair (Sept. 9-12, Gambill) could not be confirmed at a second source — campcaesar.info 503 twice.** Away: U.S. 7 closure Sept. 19-Oct. 3 (Banner Sept. 6); alternates the 9/11 ceremony Friday 8:25 a.m. and the North Bennington block party Sept. 13. Topsail: backyard-hens vote Wednesday 5 p.m. (Port City Daily agenda); alternates the 9/11 walk Friday 8:30 and Pender Fire/EMS 52 short | **watch** |
| Open-ended | **Canada 2/2/2.** College Heights gunfire (PG Daily News, incident Sept. 4 — dated in the line), Tour de North (CKPG); two CHEK-carried Tyee investigations for B.C. (Tyee's own pages 403); countertariffs took effect + Trump's Bombardier post (both Globe). Alternates: Croft Road variance Wednesday (city notice says "Monday, September 9" — a typo), Dan Pears council filing, Carney's Banff cabinet forum Sept. 10-11 (PMO), QS $20 minimum wage (Noovo), Brink 85→32 jobs detail | |
| Open-ended | **Sumo: real news two days running.** Hoshoryu practiced Tuesday at Tatsunami without a brace, "much better," decides by Friday morning's bout-drawing meeting (Kyodo via Yahoo Japan, 17:26 JST); Aonishiki took his first bouts since July at Ajigawa (Jiji via Yahoo, 17:16 JST). **The YDC soken was FRIDAY Sept. 4, not this week** — the desk's premise was wrong and the agent corrected it. Kirishima's Monday 12-1 vs. Fujinokawa reached us only through an aggregator (Sponichi/Sanspo blocked) and is in the note as unconfirmed, not in a brief. r/Sumo unreachable a 16th morning | **watch — Hoshoryu's call is Friday Sept. 11** |
| Open-ended | **Sports results all read from box scores**: Dodgers 6-3 Reds (Hernandez 3-run HR; Hayes two errors on return), Phillies 1-0 Braves (Luzardo's first CG/SHO, 12 K), Brewers 4-3 Cubs, Orioles 6-4 Guardians (A's walked off Toronto; Cleveland still a game up), Zheng d. Swiatek 7-5 6-3 (fourth round, NOT quarterfinals). `out/standings.json` (89-56 / 81-64 / 72-73 / 71-73 / 69-75) byte-matched. **The result-direction gate fired four times on honest copy**: FCC's "4-1-1 midweek" and the Pirates' "71-73" read as scores (reworded), the tennis set score had to be "2-0" with the games in `note`, and the direction check took two rewrites because it resolves each team to its FIRST mention (the headline) and then reads the summary's verb against it — so "Zheng beats Swiatek" in the headline plus "Zheng ... beat" in the summary read as Swiatek winning. The fix that works: keep ONE win-verb form across headline and summary, and avoid a second "beat"/"won" later in the paragraph | **worth telling Nate: the heuristic's first-mention rule punishes a headline-plus-summary that both name the winner first** |
| Open-ended | **Corrections to the desk's own briefing sheet, from the Our Teams agent**: Liverpool's manager is **Andoni Iraola** (appointed June; Slot was sacked this summer — Sky and Football Today), and Marshall's coach is **Tony Gibson** (the "Campbell" is Penn State's). Neither error reached print; both are in today's teams note. FOX Sports schedule pages render kickoffs in UTC — every FOX-derived time was converted and cross-checked. FCC's Wednesday kickoff is settled at 7:45 p.m. ET by the club's own tune-in page. **MaxPreps has now DROPPED Hannan's Sept. 1 Roane and Sept. 3 Logan fixtures** (shows Roane Sept. 24 home, Logan Oct. 13 away, record 1-1) — whether they were moved or never played is a question for Ian, and the paper prints no result | **OPEN — ask Ian** |
| Open-ended | **Outdoors: the DNR's 2026-27 migratory bird summary opened with a TEXT LAYER for the first time** (`Pub_Regs_MigBird2026_DNR_WILD_Rdr_Sprds_ADA.pdf`): no WV September teal season exists; early Canada geese Sept. 1-13 (5/day aggregate) ran as going-out and youth waterfowl Sept. 19 as coming-in, both cited to the PDF (the validator noted both species are absent from the hunting-pamphlet table, which is expected). **Elk tours resolved: Sept. 13** — the wvdnr.gov page carrying Sept. 6 is LAST YEAR's release (dated Aug. 25, 2025). NCDMF: no new proclamation Sept. 4-8; FF-37-2026 (commercial flounder, Sept. 3, signed by interim director Michael S. Loeffler — Rawls signed FF-27 in June) opens pound nets Sept. 15. NWS ILM: HIGH rip current risk for Pender today; NHC quiet 7 days. NPS Gauley-season URL is now 404; the whitewater page (updated Aug. 26) carries the release dates | **watch — a director change at DMF may be news** |
| Open-ended | **Source status.** NEWLY OPENED: CPHC HFOTCPCP4 advisory text, Kauai County releases, Hawaii News Now, CBS Miami NTSB story, Fox19, Vindicator, KCUR, France24 live-news, Al-Monitor, Euronews my-europe, Times of Israel liveblog, Jakarta Post, Africanews, GEOMAR, Nagoya University, Whitehead/EurekAlert, Arena.ai leaderboard, MPR News, University of Arizona News, Electrek, Prince George Daily News, Caledonia Courier, CHEK/Tyee LJI pieces, Noovo, PMO releases, Athens Messenger, Bengals.com, clevelandbrowns.com, fccincinnati.com, columbuscrew.com, NBC Sports soccer, Football Today, WTA/ATP news pages, Kyodo and Jiji via Yahoo Japan, NWPS API (HNTW2 only), NWS ILM CFW/SRF, Fisherman's Post, Coastal Angler, NCDMF proclamation index. BLOCKED: CNN (451), The Hill (403), NPR (503 x3), WMUR, openai.com (403), nhtsa.gov (403), Nature news (cookie wall), Ars Technica, dw.com, thetyee.ca article pages, myprincegeorgenow, princegeorge.ca agendas, unbc.ca, chl.ca, cleveland.com, ESPN pages (JS-only), wvusports/herdzone/ohiobobcats news (404), campcaesar.info (503), pendertopsailpost.com (DNS), USACE Huntington (503), wvmetronews.com, WOWK, WVNS, WBOY, wvnews.com, sponichi/sanspo/nikkan/hochi originals, Japan Times (402), Kyodo English, NHK World, Mainichi, r/Sumo | **watch** |
| Open-ended | **Traps dodged.** (1) "New U.S. strikes on Kermanshah" in a search summary were Sept. 1-2. (2) Search summaries dated the Reds-Dodgers game Sept. 8; the box score is Sept. 7. (3) HNN's CMS `published_time` of Aug. 30 is a placeholder. (4) HI-EMA "50 miles SSW" typo again. (5) Gut-bacteria continents (May), tadalafil/glaucoma (Aug. 4), "Pac-Man" enzyme (Sept. 2), fractons (August), 21M cancers (July), urolithin A (Aug. 22) all surfaced as "Sept. 7 science" and were not run. (6) Andersen v. Stability AI "trial starts Sept. 8" is unverified (a tracker says April 2027). (7) OpenAI's "3.1 agent-days per human day" is a 403'd blog post. (8) City of Prince George's notice says "Monday, September 9" — it is a Wednesday. (9) Acton's charge level conflicts between outlets. (10) NBC's "two pilots among the dead" vs. CBS Miami's Monday "pilot survived" — printed the NTSB-briefing account, attributed. (11) Local 12 put Bengals-Bucs "in Tampa"; Bengals.com says Paycor | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-08** | **Lowell weakens to a 70 mph tropical storm late Tuesday, moving away northwest; CPHC 2 a.m. HST advisory = 8 a.m. ET; NTSB's second MIA briefing; New Hampshire primary (polls close 7-8 p.m.); Havas court appearance (Mahoning County); WV Supreme Court jail-death arguments 10 a.m.; Parkersburg council PFAS vote; Topsail Beach hens vote Wednesday 5 p.m.; North Bennington trustees 7 p.m.; Pirates at White Sox 7:40 (Chandler v. Burke); Reds at Dodgers 10:10 (Lodolo v. Skubal); U.S. Open QFs Alcaraz-Shelton, Sabalenka-Noskova; Aki basho five days out** | |
| **2026-09-09** | **Progress 96 launches from Baikonur 12:15 p.m. EDT (NASA), docks Sept. 11 2:37 p.m.; Webster County Fair opens at Camp Caesar (per Gambill; unconfirmed elsewhere); RNC Dallas opens; NFL Kickoff Patriots at Seahawks 8:20 p.m.; PG council, Croft Road variance 6 p.m.; Chelsea v. Leeds and Liverpool v. Atletico 3 p.m. ET; Hannan v. Point JV 6 p.m.; Crew at D.C. 7:30, FCC at Philadelphia 7:45** | |
| **2026-09-10** | **Carney cabinet forum in Banff (10-11); Hannan v. Westside at Shawnee 6 p.m.; NC teal opens (NCWRC); Surf City Shoreline & Resiliency 9 a.m.; WV charter board bylaws vote** | |
| **2026-09-11** | **Hoshoryu's Aki entry decided at the bout-drawing meeting; Gauley season opens; Tour de North leaves Fort St. John; PG nominations close; Bennington 9/11 ceremony 8:25 a.m., Topsail Beach walk 8:30; Nicholas County Potato Festival; Pirates at Cubs 2:20; Reds at Brewers 7:45** | |
| **2026-09-12** | **WV squirrel opens, youth bear weekend; WVU v. UT Martin 1, Ohio v. Jacksonville State 6, Marshall v. MTSU 7; Chelsea v. Hull and Liverpool v. Fulham 10 a.m., Spurs v. Everton 12:30; Crew v. Red Bulls and FCC v. Charlotte 7:30** | |
| **2026-09-13** | **Aki basho opens; WV early Canada goose closes; first Chief Logan elk tour (DNR release Aug. 28); North Bennington block party noon-2; Bengals v. Bucs and Browns at Jaguars 1 p.m.; U.S. Open men's final** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m.; Reds v. Dodgers at GABP 6:40; ESA FLEX/Sentinel-3C** | |
| **2026-09-15** | **NCDMF FF-37-2026 opens northern pound nets; Tour de North PG block party 4:30-6:30; Huntington event parking begins; Hannan v. Parkersburg Catholic; Fed meeting 15-16** | |
| **2026-09-18** | **Federal comment deadline on the West Coast pipeline; Punta Cana trip ends (weatherman prune)** | |
| **2026-09-19** | **WV bear gun second window (19-25, selected counties); WV youth waterfowl day; NHF Day at Stonewall 9-6; U.S. 7 Bennington-Arlington closure begins (to Oct. 3)** | |
| **2026-09-21** | **House of Commons returns** | |
| **2026-09-24** | **Hannan v. Roane at Ashton (per MaxPreps AND the coach's doc)** | |
| **2026-09-25** | **Marshall homecoming parade, Joe Chrest grand marshal** | |
| **2026-09-26** | **USMNT-Peru 4:30 p.m. ET; WV archery deer/bear/boar open** | |
| **2026-10-17** | **Prince George civic election** | |
| **2026-10-28** | **Bank of Canada decision (unconfirmed, snippet only)** | |

### Open threads

- **hurricane-lowell-kauai-pass** — led; Tuesday's damage tally, outages and any injuries are the follow-up; the "70 mph by late Tuesday" forecast is CPHC's. **mia-prime-air-ntsb-van-suv** — ran; the pilots question (NBC vs CBS Miami) is still not reconciled by the NTSB on the record. **acton-canfield-havas** — ran; court Tuesday. **nh-primary** — ran as a preview; results Wednesday. **diesel-record-5-90** — ran. **iran-restricted-zone** — ran; the actual declaration and the Oman corridor maps are "in coming days." **kyiv-strikes-pause-ends** — ran (Euronews). **jakarta-airports-reopen** — ran. **egypt-khalifa-death-sentence** — ran. **bosnia-mladic-burial-recall / eu-blasts-serbia / greenland-eu-200m / lebanon-kfar-reman-12 / houthi-saudi-73 / bolivia-viacha-9 / saxony-anhalt-coalition / ukraine-prosecutor-resigns** — alternates, unprinted.
- **kanawha-falls-biohazard-psc** — ran. **pleasants-bankruptcy-conflict** — ran; Nov. 18 sale hearing. **marmet-roberts-blizzard** — ran. **wv-jail-deaths** — kicker only; Tuesday's argument is the follow-up. **bluefield-state** — no name or cause yet. **chrest-grand-marshal / cobb-79 / wood-county-107-bills** — regional. **uc-labor-day-service / brooke-high-three-suits / justice-2028 / coalfields-expressway / wooton-bench** — alternates. **bergoo-atv-two-dead** — cabin hotspot; names not released. **topsail-beach-hens-wednesday** — hotspot. **us-7-culvert-closure** — away.
- **college-heights-gunfire / tour-de-north / bc-workers-138 / seniors-one-rent-hike / countertariffs-in-effect / trump-bombardier** — ran. **croft-road-variance / pears-council / carney-banff / qs-20-minimum / brink-85-to-32 / bc-conservatives-funding (Tyee, 403)** — alternates.
- **svalbard-methane / acorn-worm / jan-mayen-permafrost-quake / black-hole-hair-nagoya** — ran. **cohesin-domains / cyclic-polymer-bioplastic / progress-96-wednesday** — alternates.
- **gpt6-astra-webdev-arena / minnesota-xai-ruling / whitehead-iris** — ran. **arizona-chatbot-misinformation / nhtsa-cybercab-audit / openai-3-1-agent-days (403) / andersen-v-stability (unverified)** — alternates.
- **caicedo-too-early / de-zerbi-medics / stewart-practices / dodgers-reds-6-3 / monken-captains / fcc-745-wednesday / gibson-explosives / hauser-35-minutes / pirates-bethancourt / wiley-out-for-season** — ran. **liverpool (Iraola; no item) / crew / spurs / usmnt / hannan** — sat out. **hannan-roane-logan-dropped-from-maxpreps** — NEW, for Ian.
- **hoshoryu-tatsunami-tuesday / aonishiki-first-bouts** — ran. **kirishima-12-1-fujinokawa (aggregator only) / kotozakura-14-5-sept6 / soken-sept4** — leagues note. **phillies-luzardo-1-0 / brewers-cubs-4-3 / orioles-guardians-6-4 / zheng-swiatek** — ran. **falcons-tua-week1 / cowboys-smith-ir** — alternates.
- **squirrel-sept12 / bear-youth / bear-gun-second / youth-waterfowl-sept19 / red-drum / seatrout / black-drum / spanish-mackerel / flounder-day-eight / early-canada-goose-closes** — ran. **migratory-summary-readable / no-wv-teal / elk-tours-sept13-resolved / nhf-day / gauley / dmf-fmp-review / ff-37-2026 / bluefish-footnote** — seasons note. **williams-71-falling / fr86-tea-creek / huntington-nwps-forecast / topsail-fp-sept1-week-old / pender-high-rip / nhc-quiet** — water block.
- **usgs-503-then-piecemeal** — NEW; the fetch-loop-then-freeze practice is in the row above. **fetch-fishing-24h-window-bug** — still for Nate. **detached-head-eleventh** — recurring.

### Covered slugs, 2026-09-08

`lowell-kauai-overnight-pass-84-mph`, `ntsb-mia-van-seven-cleaners-suv`, `acton-canfield-havas-court`, `nh-primary-pappas-manzur-sununu-brown`, `diesel-record-5-90-aaa`,
`iran-restricted-zone-blockade-line`, `kyiv-strikes-two-dead-pause-ends`, `jakarta-airports-reopen-krakatau`, `egypt-khalifa-death-sentence-upheld`,
`kanawha-falls-biohazard-dep-suit-psc`, `pleasants-bankruptcy-conflict-deferred`, `marmet-roberts-blizzard-70-years`,
`chrest-marshall-grand-marshal-sept25`, `ron-cobb-79-south-hills`, `wood-county-107-properties-no-bills`, `us-7-bennington-arlington-closure-sept19`, `bergoo-atv-crash-two-dead`, `topsail-beach-hens-vote-wednesday`,
`pg-college-heights-shots-sept4`, `tour-de-north-sept11-17`, `tyee-138-workers-died`, `seniors-advocate-levitt-6000`, `countertariffs-take-effect-28b`, `trump-bombardier-ban-vow`,
`svalbard-glacier-methane-425x`, `acorn-worm-half-cells-rewired`, `jan-mayen-quake-permafrost-pnas`, `black-hole-hair-ringdown-nagoya`,
`gpt6-astra-webdev-1797-vs-1762`, `minnesota-nudification-xai-frank`, `whitehead-iris-signaling`,
`caicedo-too-early-leeds-doubtful`, `de-zerbi-forwards-medics-merson`, `bengals-stewart-practices-golden`, `dodgers-reds-6-3-hernandez`, `browns-monken-rotating-captains`, `fcc-philadelphia-745-settled`, `marshall-gibson-explosives`, `ohio-hauser-35-minutes`, `pirates-bethancourt-outright`, `wvu-wiley-out-for-season`,
`hoshoryu-tatsunami-no-brace-decides-friday`, `aonishiki-first-bouts-ajigawa`, `phillies-braves-1-0-luzardo-12k`, `brewers-cubs-4-3-chourio`, `orioles-guardians-6-4-mayo`, `zheng-swiatek-r16`,
`squirrel-sept12`, `bear-youth-sept12-13`, `bear-gun-second-window-sept19-25`, `youth-waterfowl-sept19`, `red-drum-slot`, `seatrout-slot`, `black-drum-limits`, `spanish-mackerel-12-15`, `flounder-day-eight-ff-37`, `early-canada-goose-closes-sept13`,
`migbird-summary-readable-no-teal`, `elk-tours-sept13-resolved`, `nhf-day-sept19`, `gauley-season-sept11-nps`, `dmf-fmp-review-flounder-red-drum`, `ff-37-2026-pound-nets`, `bluefish-footnote-m`, `williams-71-cfs-falling`, `fr86-tea-creek-alerts`, `huntington-nwps-25-9`, `topsail-fp-sept1-week-old`, `pender-high-rip-current`, `nhc-no-formation-7-days`

## 2026-09-09 — No. 36 (Times) and No. 26 (Sports & Sportsman)

| Open-ended | **Fifteenth morning under the digest contract.** Eight parallel research desks again (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Around the Leagues + sumo, outdoors/water), all filed between 5:38 and 5:45 a.m. ET without exhausting a search budget. Both papers validated, rendered and pushed at **5:47 a.m. ET** (commit 56b05f0), 17 minutes after the 5:30 wake; Pages served both dated pages 200 at 5:48:25, about 40 seconds after the push. Digest dry-run 1,045 embed chars. The 6:56 `send_later` wake ran the post in the foreground; `--not-before` held 3 minutes and **the digest landed at 7:00:02 a.m. ET** (message 1547199895880990752, 1,045 embed chars, hero attached, degraded []). **Detached HEAD at session start again — twelfth occurrence**; `git checkout main && git pull origin main` (20 behind) fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **All three fetchers were clean on the first try**: stats 4 entries, `fetch_fishing.py` 0 source errors at 5:33:07 (no retry loop needed), standings 5 clubs. The file was not touched after validation. The 24h-ago values were sane today (Williams 101 → 54.9) | |
| Open-ended | **Lead art drew the lead — rung 1, fifth time in six days.** NBC's og:image is a hazy seascape: three anchored cargo ships as silhouettes on the right horizon, a small open boat with two figures crossing lower left. Drawn from a seeded Python script (375 paths, 32 KB), rasterized with headless Chromium and looked at before committing. Caption had to be cut twice to clear the 140-char cap (170, then 141) | **worth keeping: rasterize before committing** |
| Open-ended | **The lead was the U.S.-Iran escalation**: CENTCOM's strikes on five IRGC-linked tankers (Kaviz, Charminar, Horizon 1, Riesco, Derya) and Iran's overnight missiles at Al Azraq in Jordan and two destroyers; Jordan 20 engaged, 18 destroyed. Cross-checked NBC (updated 1:53 a.m. ET), Al Jazeera, CBS live page; centcom.mil 403. IRGC "significant damage" claims attributed; NBC og:title's "sinks" not used (CENTCOM: destroyed/inoperable). The World desk had the same story as its Middle East brief and swapped to Israel's U.K.-consulate order. **Kyiv's "large overnight attack, five dead" in a Euronews bulletin was the Sept. 7-8 attack, not a new one** — the toll rising 2 → 5 ran as the movement, cited to Kyiv Independent | |
| Open-ended | **Notebook: 4 statewide, 3 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley), away 1, hotspots 2 — six lines.** Statewide: jail-death argument (WCHS — the only outlet with post-argument copy; the Gazette-Mail piece is the Sept. 6 Spotlight preview), Parkersburg 6-3 recycling charge + PFAS financing (News and Sentinel, moved from a regional line), nuclear-campus MOU (WTAP, opened by the editor to avoid two WCHS bylines), Pack on the Hope Scholarship suit (Dominion Post; the suit itself, filed Sept. 4, has never run). Nicholas-Webster and Summers empty (WOAY Nicholas tag tops out Aug. 27; Hinton News Aug. 6). Away: 12-year federal sentence for the Bennington County drug-ring leader (Banner); alternates Powers Market new owner (Aug. 31), village water commissioners 11 a.m. today. Cabin: Bergoo UTV victims named (WSAZ; names printed as the outlet had them). Topsail: Corps draft EIS for North Topsail Beach's inlet plan, comment to Oct. 19, hearing Sept. 22 (WECT, corroborated by Coastal Review). **Webster County Fair still has no second source** (visitwebsterwv.com shows 2024 dates, campcaesar.info 503 again, WVU Extension 403) | **watch** |
| Open-ended | **Canada 2/2/2.** Yu's re-election launch with the city page now listing EIGHT mayoral candidates (CKPG); Cariboo night-hunting fines (Quesnel Observer); St. Mary's residential school demolition (Mission City Record via the Observer's Black Press copy); Eby's border signs (CHEK/CP); Trump's five orders banning Canadian alcohol, dairy, motorcycles from Sept. 29 (Global/CP); China's disclosure of Sept. 4 defence talks (Noovo/CP). **Council did not meet Monday (Labour Day); the Croft Road variance is on TONIGHT's Wednesday 6 p.m. Pacific agenda.** Blocked: PG Citizen 403 x2, CBC 403, Castanet, Times Colonist, National Post; CTV article bodies did not load. Alternates: Gitksen West Secondary opening in Gitwangak, Sechelt Seawatch fires, 30 more Tumbler Ridge suits v. OpenAI, StatCan Q2 registrations, Banff cabinet forum Thu-Fri, Alberta referendum business letter | |
| Open-ended | **Sumo: two Wednesday-JST briefs.** Kirishima 19 of 21 at the Tokitsukaze joint practice (Kyodo via Yahoo Japan), 7 of 8 v. Fujinokawa; Onosato 11 of 20 v. Hiradoumi at Sakaigawa (Sponichi) with Aonishiki 15-0 v. a sandanme wrestler (Nikkan). **No Wednesday practice report on Hoshoryu by 6 p.m. JST**; decision by Friday's bout-drawing meeting. Takayasu "will compete" (Hochi) alternate. JSA English site: no kyujo, sold out. **r/Sumo: the fetch tool refuses old.reddit.com outright — 17th morning without it.** The validator's score regex reads practice tallies ("19-2", "11-9") as game scores; they were rewritten as "19 of 21" | **watch — Hoshoryu's call is Friday Sept. 11** |
| Open-ended | **Sports results all read from box scores**: Dodgers 3-2 Reds (Skubal 7 1/3, De La Cruz's 25th; Lowder v. Yamamoto tonight 10:10), Pirates 9-3 White Sox (Chandler 6 IP 8 K, 18 hits; Bachar v. Martin 7:40), Brewers 4-3 Cubs in 10, Guardians 9-5 Orioles, Villa 3-2 Brugge, City 2-0 Porto (Haaland ties Aguero's 36), Shelton d. Alcaraz in five (3:33 a.m. ET finish), Sabalenka d. Noskova. `out/standings.json` (90-56 / 81-65 / 72-73 / 72-74 / 69-76) byte-matched; **the Pirates are THIRD now**, ahead of St. Louis. **The direction gate fired 7 times on honest copy**: Marshall's "45-0", Ohio's "6-8 receiver", Kirishima "19-2", Onosato "11-9", LSU "51-10"/"16-0" all read as game scores needing `result`; and both tennis briefs failed until the summaries dropped "beat" entirely — the heuristic iterates verbs in TUPLE order, so a summary "beat" is found before a headline "beats", and the subject it resolves is the loser named last in the headline. **Fix that works: headline carries the win verb, summary uses none of the listed verbs** ("came through five sets against") | **worth telling Nate: the tuple-order verb search** |
| Open-ended | **Ledger correction: the NFL Kickoff game is WEDNESDAY, Sept. 9** (Patriots at Seahawks, 8:20 p.m. ET, NBC — NFL.com and both club sites), not Thursday as this ledger had it since Sept. 7; 49ers-Rams in Melbourne is Thursday 8:35 p.m. ET. **Liverpool v. Tottenham Carabao Cup (house derby)**: FOX and Sky say Tue Sept. 15 3 p.m. ET at Anfield, liverpoolfc.com says Thu Sept. 17 — withheld from the week ahead until confirmed. Chelsea: Caicedo and Palestra out for Leeds tonight, Colwill fit (club site). Bengals: nothing on Stewart Tuesday; first injury report Wednesday. Hannan: Point JV tonight 6 p.m. at Ashton; MaxPreps still 1-1 with Roane/Logan absent — **still a question for Ian** | **OPEN — ask Ian** |
| Open-ended | **Outdoors: the moon line was WRONG yesterday and the prompt repeated it.** USNO: new moon 03:27 UTC Sept. 11 = **11:27 p.m. ET Thursday Sept. 10**. A 7% (or yesterday's 13%) waning crescent is two days from new — spring tides building, not neap. Today's Topsail block says springs building; yesterday's page said "13%, so neap tides" and is logged in FAILURES. Also: the DNR migratory-bird PDF opened again (TLS verified); **NC teal does not run** — the only NCWRC table that opened is headed 2025-26; NCDMF proclamation index shows nothing Sept. 7-9 (the working URL is `/fisheries-management-proclamations`, the two older slugs 404); **new Sept. 8 Forest Service closure of FR 76, Cranberry River Road, through Nov. 20**; Gauley releases confirmed on NPS `whitewater.htm`; elk tours Sept. 13 (Lootpress; wvdnr.gov's page is the 2025 release, same trap); NHF Day Sept. 19 at Stonewall (national observance is Sept. 26 — do not merge). Charleston's 10.92 in. August was its wettest on record (RLX). NWS HNTW2: **WebFetch summarized an August dataset; curl of the same endpoint returned the current forecast** — use curl for NWPS. USACE Huntington timed out twice | **watch** |
| Open-ended | **Source status.** NEWLY OPENED: SCOTUSblog, CBS Boston, Civil Beat, Kauai Now, Local10, WVXU, Texas Tribune, Citizen Digital (Kenya), newsinenglish.no, Moscow Times, Kyiv Independent, Coastal Review, Caledonia Courier, Mission City Record (via Quesnel Observer), pm.gc.ca, statcan Daily, cisa.gov, scientificamerican.com, fortune.com, science.nasa.gov, vims.edu, kobe-u.ac.jp, WOUB, Seahawks.com, Patriots.com, atptour.com news, Sky match reports, USNO moon API, fs.usda.gov alerts, americanwhitewater.org event page. BLOCKED: centcom.mil (403), wng.org, cnbc.com (403), usnews.com (503), WV Watch homepage (403), Ukrainska Pravda (403), CourtListener (403), Yorkshire Post, On3, Prince George Citizen, CBC, Castanet, Times Colonist, National Post, CTV bodies, timeanddate.com (403), gauleyfest subdomain (403), old.reddit.com (tool refusal), USACE Huntington (timeout), wvmetronews/WOWK/WVNS/WBOY/wvnews, campcaesar.info (503), sponichi/sanspo originals, Japan Times, NHK, Mainichi | **watch** |
| Open-ended | **Traps dodged.** (1) Euronews "large overnight attack on Kyiv, five dead" was Sept. 7-8's attack with a higher toll. (2) Jordanian "eight intercepts over Amman" in snippets vs the official 20/18. (3) NBC og:title "sinks" vs CENTCOM "destroyed". (4) Webster County Fair "returns Sept. 9" snippet came off a 2024 page. (5) Bluefield State student's name in snippets while WVVA says the university withheld it — not run. (6) Banner "trustees question lease" is May 2025. (7) City of PG "Monday, September 9" notice — the meeting is Wednesday. (8) Oxford "quantum gravity" result is Aug. 28/Sept. 2; Kobe immune-tracking is a July 30 paper; a fetch rendered Amazon warming "0.21 C annually" (page: per decade); VIMS index said 89,395 acres, body 89,385. (9) ATP results page parsed with Alcaraz and Michelsen as winners — the ATP article, CBS and WTA all say Shelton and Tiafoe. (10) Sky's UCL index showed Brugge 1-3; report and results say 3-2. (11) A snippet had Burke at 0.2 IP; the box says 1 1/3. (12) FOX's Reds schedule repeats Lodolo v. Skubal for Sept. 14 — stale. (13) Sky's Liverpool fixtures page carried a 2025 header and listed Atletico away. (14) "7% crescent = neap" in the desk's own prompt | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-09** | **NFL Kickoff Patriots at Seahawks 8:20 p.m. ET (NBC) — WEDNESDAY, corrected; Progress 96 launches 12:15 p.m. EDT, docks Friday 2:37 p.m.; RNC Dallas opens, Trump 9 p.m.; Prince George council 6 p.m. Pacific (Croft Road variance); Topsail Beach hens vote 5 p.m.; Chelsea v. Leeds and Liverpool v. Atletico 3 p.m. ET; Hannan v. Point JV 6 p.m.; Crew at D.C. 7:30, FCC at Philadelphia 7:45; Pirates at White Sox 7:40 (Bachar v. Martin); Reds at Dodgers 10:10 (Lowder v. Yamamoto); King Harald's funeral 7 a.m. ET; NTSB interviews the MIA pilots; Bengals' first Week 1 injury report; front into WV this evening** | |
| **2026-09-10** | **49ers-Rams in Melbourne 8:35 p.m. ET; Carney cabinet forum in Banff (10-11); Hannan v. Westside at Shawnee 6 p.m.; Surf City Shoreline & Resiliency 9 a.m. and Planning Board; WV charter board bylaws vote; new moon 11:27 p.m. ET; flash-flood concern WV Thursday into Friday; U.S. Open women's semifinals (Sabalenka-Pegula)** | |
| **2026-09-11** | **Hoshoryu's Aki entry decided at the bout-drawing meeting; Gauley season opens; PG nominations close 4 p.m.; Tour de North leaves Fort St. John; Bennington 9/11 ceremony 8:25 a.m., Topsail Beach walk 8:30; Nicholas County Potato Festival; North Bennington water commissioners' agenda follow-up; Pirates at Cubs 2:20 (Ashcraft); Reds at Brewers 7:45 (Abbott v. Drohan); U.S. Open men's semifinals (Shelton-Tiafoe)** | |
| **2026-09-12** | **WV squirrel opens, youth bear weekend; WVU v. UT Martin 1, Ohio v. Jacksonville State 6, Marshall v. MTSU 7; Chelsea v. Hull and Liverpool v. Fulham 10 a.m., Spurs v. Everton 12:30; Crew v. Red Bulls and FCC v. Charlotte 7:30; Pirates at Cubs 2:20 (Skenes); Reds at Brewers 7:10** | |
| **2026-09-13** | **Aki basho opens; WV early Canada goose closes; first Chief Logan elk tour; North Bennington block party; Bengals v. Bucs and Browns at Jaguars 1 p.m.; U.S. Open men's final** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m.; Reds v. Dodgers at GABP 6:40; Bennington Select Board option-tax session; ESA FLEX/Sentinel-3C** | |
| **2026-09-15** | **Liverpool v. Tottenham Carabao Cup — DATE UNCONFIRMED (FOX/Sky Sept. 15, club Sept. 17); NCDMF FF-37-2026 pound nets open; Huntington event parking begins; Hannan v. Parkersburg Catholic 6 p.m.; Pirates v. Brewers 6:40; Reds v. Dodgers 6:40; Fed meeting 15-16** | |
| **2026-09-16** | **Crew v. Orlando City, U.S. Open Cup, 7 p.m. ET; North Bennington Planning Commission** | |
| **2026-09-17** | **Gauley Fest opens (through the 20th); NCDMF kingfishes meeting; Hannan at Westside (Beckley YMCA)** | |
| **2026-09-19** | **WV bear gun second window (19-25, selected counties); WV youth waterfowl day; NHF Day at Stonewall 9-6; U.S. 7 Bennington-Arlington closure begins** | |
| **2026-09-22** | **Army Corps hearing on the North Topsail Beach draft EIS, 6 p.m., Town Hall; Hannan at Calvary** | |
| **2026-09-26** | **USMNT-Peru 4:30 p.m. ET; WV archery deer/bear/boar open; national NHF Day** | |
| **2026-09-29** | **Trump's Canadian alcohol/dairy/motorcycle bans take effect; Putnam commission takes up the data-center resolution; Hannan at Roane** | |
| **2026-10-17** | **Prince George civic election** | |
| **2026-10-19** | **Corps comment deadline on the North Topsail Beach draft EIS; Alberta separation referendum** | |
| **2026-11-20** | **FR 76 Cranberry River Road closure ends** | |

### Open threads

- **us-iran-tankers-jordan** — led; today's follow-ups are the Gulf exclusion-zone declaration, any confirmed damage to the destroyers, Brent above $100. **lowell-kauai-33000-out** — ran; restoration timeline (transmission two days, distribution by week's end). **nh-primary-results** — ran; done. **missouri-map-kavanaugh** — ran. **mia-ntsb-brakes-reversers** — ran; pilot interviews Wednesday, CVR readout after. **marshals-79-children-ohio / rnc-dallas-trump-9pm** — alternates.
- **israel-uk-consulate** — ran. **kyiv-toll-five** — ran (movement). **kenya-foreign-traders** — ran. **indonesia-fire-emissions** — ran. **renoir-theft / king-harald-funeral / rubio-colombia / novorossiysk-four-dead** — alternates.
- **wv-jail-deaths-argued** — ran; opinion weeks or months. **parkersburg-recycling-pfas-passed** — ran. **nuclear-campus-mou** — ran. **hope-scholarship-mingo-suit** — ran (the suit itself is still unprinted as its own brief). **morrisey-crime-overdose-2025 / lewis-county-school-jacksons-mill / wvu-fraternities** — alternates. **point-pleasant-poda-rejected / st-albans-howitzer / wood-boe-stadium-delay** — regional. **huntington-house-reinspections / putnam-data-center-sept29** — alternates. **bennington-drug-ring-12-years** — away. **powers-market / nb-water-commissioners** — alternates. **bergoo-utv-names** — cabin; closed. **ntb-corps-draft-eis** — topsail; hearing Sept. 22. **surf-city-backflow-rfp / topsail-911-walk** — alternates.
- **pg-yu-relaunch-eight / cariboo-night-hunting-fines / st-marys-demolition / eby-border-signs / trump-canada-bans-sept29 / china-canada-defence-talks** — ran. **gitwangak-school / school-zone-enforcement / mccrory / sechelt-fires / tumbler-ridge-openai-suits / burnaby-stray-bullet / statcan-vehicles / banff-forum / alberta-referendum-business** — alternates.
- **hubble-webb-tnos / amazon-extremes / chesapeake-sav / lions-hyenas** — ran. **progress-96 / tokyo-qldpc / kobe-structural-color** — alternates.
- **cisa-distillation-six-firms / openai-navier-stokes-buckmaster / reading-dday-ai** — ran. **claude-session-key-theft / andon-vending-bench / alphagenome-atlas / andersen-v-stability (still unverified)** — alternates.
- **chelsea-caicedo-palestra-out / iraola-first-ucl / dodgers-reds-3-2 / pirates-white-sox-9-3 / browns-depth-chart / wvu-close-to-vest / marshall-gibson-derail / ohio-hauser-jsu** — ran. **spurs-pl / bengals / fcc / crew / spurs-nba / usmnt / hannan** — sat out. **liverpool-spurs-cup-date** — OPEN. **hannan-roane-logan** — still owed, for Ian.
- **kirishima-19-of-21 / onosato-11-of-20-aonishiki-15-0** — ran. **takayasu-thigh** — alternate. **brewers-cubs-4-3-10inn / guardians-orioles-9-5 / nfl-kickoff-wednesday / villa-city-madrid / shelton-alcaraz / sabalenka-noskova / ap-poll-lsu-8** — ran. **gonzalez-135m-reported / haaland-record / astros-phillies** — alternates.
- **squirrel-sept12 / bear-youth / bear-gun-second / youth-waterfowl-sept19 / archery-sept26 / red-drum / black-drum / spanish / sheepshead-pattern / flounder-day-nine / early-goose-closes** — ran. **no-nc-teal-2026-table / fr76-cranberry-closure / gauley / gauley-fest / elk-tours / nhf-day / wettest-august** — seasons note. **williams-55-falling / rlx-front-tonight / huntington-nwps / topsail-fp-sept1-eight-days / pender-moderate-rip / nhc-quiet / new-moon-thursday** — water block.
- **moon-phase-neap-error-0908** — NEW, logged in FAILURES. **direction-gate-tuple-order** — NEW, for Nate. **fetch-fishing-24h-window-bug** — still for Nate (did not bite today). **detached-head-twelfth** — recurring.

### Covered slugs, 2026-09-09

`us-destroys-five-iranian-tankers-jordan-missiles`, `lowell-kauai-33000-without-power`, `nh-primary-sununu-pappas-win`, `kavanaugh-denies-missouri-map`, `ntsb-mia-no-speed-brakes-reversers`,
`israel-orders-uk-consulate-closed`, `kyiv-toll-rises-to-five`, `kenya-knchr-foreign-trader-crackdown`, `indonesia-fires-lead-world-emissions`,
`wv-jail-deaths-argued-tuesday`, `parkersburg-3-recycling-pfas-financing-passed`, `morrisey-nuclear-campus-mou-sixth-state`, `pack-defend-hope-scholarship-mingo-suit`,
`point-pleasant-poda-voted-down`, `st-albans-howitzer-roadside-park`, `wood-boe-phs-stadium-delay-3-2`, `bennington-drug-ring-12-years-rutland`, `bergoo-utv-victims-named`, `north-topsail-corps-draft-eis-oct19`,
`pg-yu-relaunch-eight-candidates`, `cariboo-night-hunting-fines-5750`, `st-marys-mission-residential-school-demolition`, `eby-border-signs-51st-state`, `trump-bans-canadian-alcohol-dairy-motorcycles-sept29`, `china-canada-defence-talks-sept4`,
`hubble-webb-27-tnos-colors`, `amazon-extremes-0-75c-decade-lancaster`, `chesapeake-sav-89385-acres`, `lions-hyenas-gps-collars-frontiers`,
`cisa-aa26-251a-distillation-six-firms`, `openai-navier-stokes-buckmaster`, `reading-ai-dday-forecast-weather`,
`chelsea-caicedo-palestra-out-leeds`, `iraola-first-ucl-night-atletico`, `dodgers-reds-3-2-skubal`, `pirates-white-sox-9-3-chandler-18-hits`, `browns-week1-depth-chart`, `wvu-rodriguez-close-to-vest`, `marshall-gibson-not-derail`, `ohio-hauser-jsu-creel-johnson`,
`kirishima-19-of-21-joint-practice`, `onosato-11-of-20-aonishiki-15-0`, `brewers-cubs-4-3-10-innings`, `guardians-orioles-9-5-bazzana`, `nfl-kickoff-wednesday-henderson-out`, `villa-brugge-3-2-city-porto-2-0`, `shelton-alcaraz-five-sets-333am`, `sabalenka-noskova-two-tiebreaks`, `ap-poll-lsu-8-michigan-out`,
`squirrel-sept12`, `bear-youth-sept12-13`, `bear-gun-second-window-sept19-25`, `youth-waterfowl-sept19`, `archery-deer-bear-sept26`, `red-drum-slot`, `black-drum-limits`, `spanish-mackerel-12-15`, `sheepshead-14-5-pattern`, `flounder-day-nine-ff-27`, `early-canada-goose-closes-sept13`,
`migbird-summary-reread`, `no-nc-teal-2026-table`, `fr76-cranberry-road-closure-nov20`, `gauley-season-sept11-nps`, `gauley-fest-sept17-20`, `elk-tours-sept13`, `nhf-day-sept19-stonewall`, `charleston-wettest-august`, `williams-55-cfs-falling`, `rlx-front-tonight-flash-flood-thu-fri`, `huntington-nwps-26-0`, `topsail-fp-sept1-eight-days`, `pender-moderate-rip`, `nhc-no-formation-7-days`, `new-moon-thursday-1127pm`

## 2026-09-10 — No. 37 (Times) and No. 27 (Sports & Sportsman)

| Open-ended | **Sixteenth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), all filed between 5:40 and 5:47 a.m. ET. Both papers validated, rendered and pushed at **5:48:55 a.m. ET** (commit 684dcb3), 19 minutes after the 5:30 wake. Pages was still 404 on both dated pages two minutes after the push and served the Times page 200 by 5:54 (about five minutes), both pages by 6:53. Digest dry-run 1,184 embed chars, hero attached. The 6:52 `send_later` wake ran the post in the foreground; `--not-before` held 7 minutes and **the digest landed at 7:00:01 a.m. ET** (message 1547562283821961230, 1,184 embed chars, hero attached, degraded []). **Detached HEAD at session start again — thirteenth occurrence**; `git checkout main && git pull origin main` fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **All three fetchers clean on the first try**: stats 4 entries, `fetch_fishing.py` 0 source errors at 5:32:40, standings 5 clubs (Pirates 73-73 third, Reds 69-77 fifth). The 24h-ago values were sane (Williams 69.9 → 47.6) | |
| Open-ended | **Lead art drew the lead — rung 1, sixth time in seven days.** PBS's og:image (a Reuters frame) is Trump on the Dallas stage pointing at a bleacher of supporters holding small flags, many in cowboy hats, stars on the stage skirt. Drawn from a seeded Python script as the same stage seen FROM BEHIND the podium — a dark-suited figure with his back to the viewer, no face — 340 paths, 48 KB, rasterized with headless Chromium and looked at before committing; the first pass was 1,517 paths / 158 KB and had the crowd showing through the figure until parchment masks went under the podium and the speaker. Crude but reads | **worth keeping: one path per crowd figure, masks for occlusion** |
| Open-ended | **The lead was Trump's Dallas speech**: the $5,000 "Trump dividend" if the GOP holds both chambers (PBS, CBS, NPR — NPR only via curl with a browser UA, WebFetch 503s) plus his Andrews remark that the Iran war "is going to end immediately after the election" (Al Jazeera, The National) and Brent's $100.19 close (Al Jazeera). CBS's $1T+ cost estimate and NPR's vote-buying note attributed. The "closed above $100 for the first time since May" phrasing in search results conflicts with AJ's "highest since July 24" — used AJ's own figure. The Al Azraq aircraft-damage report (eight F-15s, an A-10) is single-chain (The National / JPost) and did not run; the IRGC destroyer-damage claim is unconfirmed | |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley, summers_new_river), away 1, hotspots 2 — seven lines.** Statewide: Ascend WV $2.4M health-care recruiting (WCHS, announced in Hurricane), Operation Coal Country 59 arrests (WSAZ), Weld's locker-room-filming felony bill after the Brooke principal's arrest (Herald-Dispatch), WVU re-recognizing three fraternities (Gazette-Mail, which OPENED today). Nicholas-Webster empty (WOAY tag tops out Aug. 27; Chronicle stale; Hinton News Aug. 6). Away: Putnam Block Phase 2 design review Tuesday (Banner). **Cabin: the Webster County Fair finally has a second source** — Webster County Tourism's events page lists Sept. 9 3:30 p.m. through Sept. 12 4:30 p.m. at Camp Caesar; the Town of Cowen page confirms the venue with no dates. Topsail: the hens vote was Wednesday and no outcome was posted by 6 a.m. (Port City Daily Sept. 7 preview says 5 p.m., the town's agenda page says 6 p.m.); ran the Friday 8:30 a.m. 9/11 walk from the town's own notice. **A flash flood warning for northern Mason County (Point Pleasant, Leon, Henderson) was extended at 5:39 a.m. to 8:15 a.m. on 3-4 inches of rain** — left to Jim; it is in the Sports water block for the Point Pleasant gauge | **watch: hens outcome, charter board bylaws (8 a.m. Thursday), Mason County flooding damage** |
| Open-ended | **Canada 2/2/2.** PG council backs a forestry/wildfire public inquiry (CKPG, 10:40 p.m. PT; no vote tally given); nominations close Friday 4 p.m. with a 25-year-old mayoral candidate (My PG Now — WebFetch 403, curl with a Safari UA works); 15 forestry groups' "breaking point" letter (CHEK/CP); Labour Day crossings down 49% (Langley Advance Times via Quesnel Observer); Zelenskyy-Carney in Calgary Thursday morning then Banff (Global/CP); Saddle Lake Cree Nation defying Alberta's trans-youth law (Globe). **Croft Road variance outcome NOT found** — CKPG's only council story was the inquiry vote; PG Citizen snippets say the July 6 motion failed 4-4 (unverified). Blocked: Prince George Daily News does not resolve, city site bot-check, UNBC 403, pm.gc.ca template only | **watch — Croft Road** |
| Open-ended | **Sumo: Hoshoryu missed practice Wednesday AND Thursday** for medical appointments, no bouts since July 29 surgery; Tatsunami says shiko and butsukari only; decision at Friday morning's bout-drawing meeting (Thursday evening ET); Chunichi calls entry "extremely difficult" (Kyodo, Chunichi via Yahoo Japan). Kirishima won 19 of 24 Thursday at Arashio after 19 of 21 Wednesday (Hochi, Sankei). Aonishiki 15 of 15 v. a sandanme stablemate, no sekitori sparring before Sunday (Nikkan). **JSA English pages all returned URL errors** — no kyujo list yet. r/Sumo still refused. Practice tallies written as "won X of Y" to dodge the score regex | **watch — Hoshoryu's call lands Thursday evening ET; tomorrow leads with it** |
| Open-ended | **Sports results all from box scores/club reports**: Chelsea 6-3 Leeds from 0-2 down (Palmer 2, Neto, Welbeck 2, Barco; Rogers four assists), Liverpool 2-1 Atletico (Szoboszlai, Mac Allister), Dodgers 14-1 Reds (Yamamoto 10 K; De La Cruz five straight games), Pirates 4-2 White Sox (Eisert W, Montgomery S11; Pirates at .500, 73-73, THIRD), Union 5-0 FCC (Nwobodo red 16'; Damiani hat trick), D.C. 2-1 Crew (Baribo 2), Seahawks 13-10 Patriots (Maye 3 INT in Q4; Darnold hip), Brewers 8-6 Cubs, Phillies 11-7 Astros (Schwarber slam, 44th), Arsenal 1-0 Napoli. **Liverpool v. Tottenham Carabao Cup date RESOLVED: Tuesday Sept. 15, 8 p.m. BST / 3 p.m. ET at Anfield** — the club moved it from Sept. 16 on Aug. 31 and Spurs' Sept. 4 ticket notice agrees; runs in the week ahead for both. Bengals: Chase, Higgins, Stewart all FULL on the first report (bengals.com). Browns: nobody out. USMNT roster Sept. 17 (ussoccer.com). Hannan: no outside source has Wednesday's Point JV result; Westside tonight at Shawnee. The direction gate fired twice on the WVU brief for "42-7" and then "1-1" records — both removed | |
| Open-ended | **Outdoors: NWS Huntington forecast was reissued Wednesday 10:25 a.m.** and now has a rise to a 26.8-ft crest Saturday morning (yesterday's edition said it had not been reissued); read via curl on the NWPS API. New Forest Service closure order posted Sept. 9: **FR 19 (Dolly Sods) Sept. 14-25**. NPS letter to Gauley boaters (Aug. 24): Tailwaters Campground closed Sept. 11-28. USACE Huntington: certificate-name mismatch on curl, third day with no Corps notice. NCDMF proclamation index URL moved to `/about/divisions/marine-fisheries/rules-proclamations-and-size-and-bag-limits/fisheries-management-proclamations` and the served list was partial (15 entries, FF-27 absent) — say "nothing new found." Fisherman's Post and Coastal Angler both still Sept. 1 (nine days). Waterspout risk today LOW (yesterday's note said moderate for Thursday). New moon 11:27 p.m. ET tonight — spring tides, written as such | **watch** |
| Open-ended | **Progress 96 did NOT launch Wednesday** — postponed to NET Sept. 16 (trackers cite a Soyuz third-stage issue; NASA's Sept. 3 advisory is unchanged and no NASA/Roscosmos statement was found). Not run; the ledger's Sept. 11 docking row is withdrawn. **August CPI is Friday Sept. 11, 8:30 a.m.** (BLS schedule page opened). Massachusetts data-center EO signing day is ambiguous (Globe URL Sept. 8, State House News Sept. 9) — written without a day | |
| Open-ended | **Source status.** NEWLY OPENED: Charleston Gazette-Mail, JNS, The National, Rio Times, Lethbridge Herald (CP), Caledonia Courier, Field Level Media, BVM Sports, D.C. United site, Philadelphia Inquirer, NBC Sports UCL blog, Copernicus, MPS, Manchester, Greenfield Recorder, SpacePolicyOnline, KPBS (NPR/AP copy), WLRN, NHPR, Weirton Daily Times, Webster County Tourism, Town of Cowen. BLOCKED: The Hill (403), CNN (451), NewsNation, UPI, state.gov, mass.gov, openai.com, Ars Technica, Politico, nasaspaceflight, WV Watch /news index (article pages untested), WTRF, northtopsailbeachnc.gov/news (403 today), visitwebsterwv.com (bot wall), postandvoice.com and jdnews.com (DNS), Prince George Daily News (DNS), ESPN game pages (empty), mlb.com scores/standings (406), wvusports.com and herdzone.com (empty shells), Herald-Dispatch (429 on one article), Dawgs By Nature, Athlon, On3, sumo.or.jp English pages, usopen.org (503), old.reddit.com (tool refusal), NPR via WebFetch (503; curl works) | **watch** |
| Open-ended | **Traps dodged.** (1) "Brent closed above $100 for the first time since May" (search) vs AJ's "highest since July 24." (2) Boston Globe "12 years" vs CBS "eight years" for a governor losing a primary — used CBS. (3) A search summary said John Harbaugh was fired Sept. 9 — he was fired in January. (4) Camden Chat said the Blue Jays and Rangers won; the scoreboard shows both lost. (5) NBC's UCL blog credited Ferran Torres to both Barcelona and PSG — Barcelona's fourth scorer left unnamed. (6) Space.com's "impossible black hole merger" is an Aug. 25 paper; Chalmers "1,000x faster" is Aug. 3. (7) The Andersen v. Stability "Sept. 8 trial" remains unverified. (8) News and Sentinel's Marietta page says "Monday, September 9" — Sept. 9 was Tuesday. (9) Point Pleasant's MaxPreps lists Wednesday's Hannan match as varsity; the coach's file says JV. (10) Al Azraq aircraft-damage figures are a single reporting chain. (11) Rays record 86-58 (SB Nation) vs 87-58 (CBS standings) — neither printed | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-10** | **Hoshoryu's entry decided at Friday morning's JST bout-drawing meeting (Thursday evening ET); U.S. Open women's semifinals Sabalenka-Pegula and Rybakina-Gauff (Ashe, evening); 49ers-Rams in Melbourne 8:35 p.m. ET; RNC Dallas closes with Trump and Vance; ECB rate decision; WV charter school board bylaws/FY28 budget vote 8 a.m. (virtual); Hannan v. Westside at Shawnee 6 p.m.; Pirates at White Sox 7:40 (Jones v. Smith); Zelenskyy-Carney in Calgary then Banff; PG open-burning ban lifts noon Pacific in Vanderhoof/Fort St. James; new moon 11:27 p.m. ET; Mason County flash flood warning to 8:15 a.m.** | |
| **2026-09-11** | **August CPI 8:30 a.m.; Gauley season opens (releases 11-14); PG nominations close 4 p.m. Pacific; Tour de North leaves Fort St. John; Bennington 9/11 ceremony 8:25 a.m., Topsail Beach walk 8:30, Dawson College ceremony; Nicholas County Potato Festival; U.S. Open men's semis Shelton-Tiafoe, Zverev-Khachanov; Pirates at Cubs 2:20 (Ashcraft v. Imanaga); Reds at Brewers 7:45 (Abbott v. Drohan); Tailwaters Campground closes through Sept. 28; Kelly Rogers' resignation effective** | |
| **2026-09-12** | **WV squirrel opens, youth bear weekend; Webster County Fair closes 4:30 p.m.; WVU v. UT Martin 1, Ohio v. Jacksonville State 6, Marshall v. MTSU 7; Chelsea v. Hull and Liverpool v. Fulham 10 a.m., Spurs v. Everton 12:30; Crew v. Red Bulls and FCC v. Charlotte 7:30; Pirates at Cubs 2:20 (Skenes v. Holmes); Reds at Brewers 7:10 (Singer v. May); PG Ukrainian Festival and Parkinson SuperWalk** | |
| **2026-09-13** | **Aki basho opens; WV early Canada goose closes; first Chief Logan elk tour; North Bennington block party; Bengals v. Bucs and Browns at Jaguars 1 p.m.; Reds at Brewers 2:10 (Harrison v. Burns); Pirates at Cubs 2:20 (Chandler v. Boyd); U.S. Open men's final** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m.; FR 19 Dolly Sods closure begins (to Sept. 25); Reds v. Dodgers at GABP 6:40 (Lodolo v. Skubal); Bennington Select Board option-tax session; StatCan August CPI; ESA FLEX/Sentinel-3C** | |
| **2026-09-15** | **Liverpool v. Tottenham Carabao Cup third round, Anfield, 3 p.m. ET — CONFIRMED (house derby); NCDMF FF-37-2026 pound nets open; Huntington event parking begins; Hannan v. Parkersburg Catholic 6 p.m.; Pirates v. Brewers 6:40 (Gasser v. TBA); Reds v. Dodgers 6:40 (Lowder v. Yamamoto); Fed meeting 15-16** | |
| **2026-09-16** | **Progress 96 launch NET (reported, unofficial); Crew v. Orlando City, Open Cup semifinal, 7 p.m. ET; Reds v. Dodgers 6:40 (Abbott v. Snell); Pirates v. Brewers 6:40 (Jones v. Misiorowski); U.K. formal extradition request for the Tates due; Carabao Cup round-four draw (snippet only); North Bennington Planning Commission** | |
| **2026-09-17** | **USMNT roster named (Pochettino); Gauley Fest opens (through the 20th); NCDMF kingfishes meeting; Hannan at Westside (Beckley YMCA)** | |
| **2026-09-19** | **WV bear gun second window (19-25, selected counties); WV youth waterfowl day; NHF Day at Stonewall 9-6; U.S. 7 Bennington-Arlington closure begins** | |
| **2026-09-22** | **Army Corps hearing on the North Topsail Beach draft EIS, 6 p.m., Town Hall; Hannan at Calvary** | |
| **2026-09-26** | **USMNT-Peru, Orlando; WV archery deer/bear/boar open; national NHF Day; B.C. Conservatives' Abbotsford-Mission byelection** | |
| **2026-09-28** | **PSC public hearing on HB 2014 power requirements, 9:30 a.m., Charleston (intent to participate by Sept. 18, comments by Sept. 23)** | |
| **2026-09-29** | **Trump's Canadian alcohol/dairy/motorcycle bans take effect; Putnam commission data-center resolution; Hannan at Roane; USMNT-Chile, St. Louis** | |
| **2026-10-02** | **Surf City beach-nourishment appraisal RFP due 5 p.m.** | |
| **2026-10-17** | **Prince George civic election; HalloHinton at Camp Summers (also Oct. 23-24)** | |
| **2026-10-19** | **Corps comment deadline on the North Topsail Beach draft EIS; Alberta separation referendum** | |
| **2026-10-25** | **Serbia snap parliamentary election** | |
| **2026-10-31** | **Gambia's promised 24 MW plant deadline; WV second youth waterfowl day** | |
| **2026-11-20** | **FR 76 Cranberry River Road closure ends** | |
| **2027-03-08** | **SBA drought loan deadline, 25 WV counties incl. Webster and Summers** | |

### Open threads

- **trump-5000-dividend-war-after-election** — led; follow-ups are tonight's closing speech with Vance, any Treasury/Congress reaction, and gas prices. **brent-100-19** — in the lead. **al-azraq-aircraft-damage (single chain) / irgc-destroyer-claim / sirik-projectiles / gulf-exclusion-zone (still "coming days" since Sept. 6)** — alternates. **ri-mckee-ousted** — ran. **tate-bail-denied** — ran; U.K. request due Sept. 16. **ntsb-cvr-too-fast** — ran. **osers-rogers-resigns** — ran. **rubio-los-tiguerones / florida-netflix-suit / apple-iphone-duo / charlotte-officer-shot / cpi-friday** — alternates.
- **philippines-june-aster-fire** — ran; toll is live. **serbia-vucic-oct25** — ran. **gambia-blackouts-barrow** — ran. **netanyahu-hermon** — ran. **yemen-houthi-saudi-mecca-pact / zelensky-plane-drone-moldova / brazil-stf-police-chief / tooro-succession / bangladesh-measles-1000 / novy-urengoy-strike / slovenia-embassy-protest / ceuta-cni-warning / king-harald-buried / rubio-ecuador-45m / nigeria-boko-haram-ceasefire (reported only) / haaretz-mbz-suit / beit-lahiya-four** — alternates.
- **ascend-wv-healthcare-2-4m / operation-coal-country-59 / weld-locker-room-felony / wvu-three-fraternities** — ran. **charter-board-bylaws-thursday** — kicker; outcome tomorrow. **medicaid-school-health / sba-drought-25-counties / data-center-accountability-project (regional) / broadband-council-bead / psc-hb2014-sept28 / clay-county-dui-father / raleigh-bus-rollover / teacher-of-year-presley** — alternates. **mason-leon-fatal-fire / parkersburg-7th-street-camden-clark / hallohinton** — regional. **hadco-spec-building / ck-elementary-mold / northcott-october / vienna-johns-manville-1m / mount-hope-rv-park** — alternates. **putnam-block-phase-2** — away. **svsu-enrollment / bennington-9-11-friday / shaftsbury-theft / nb-water-commissioners (no outcome)** — alternates. **webster-county-fair-second-source** — cabin; closed. **topsail-9-11-walk** — topsail. **topsail-hens-vote (no outcome) / surf-city-batts-addendum / pender-burns-appeal** — alternates. **mason-flash-flood-warning** — Jim's, and in the water block.
- **pg-forestry-inquiry / pg-olson-25-nominations-friday / bc-forestry-breaking-point / border-crossings-49 / zelenskyy-carney-calgary / saddle-lake-defiance** — ran. **croft-road (no outcome) / canada-post-suspicious-package / burning-ban-lifted / open-waters-solar-450k / surrey-police-collisions-review / burnaby-cho-family / okanagan-wine-ban / findlay-caucus-28 / victoria-taxi-12k / stamp-falls / army-reorg-thursday / iranian-vp-son-contracts (reported) / distillers-ban / dawson-20 / children-first-online-harms** — alternates.
- **copernicus-august-joint-hottest / chandra-84-hypersoft / feedbacks-20-30-erl / seattle-coyotes-9x** — ran. **progress-96-postponed-sept16 / uchicago-feature-interference / wyoteuthis-belemnite / mps-1947-superflare / nagoya-fish-equilibrium** — alternates.
- **anthropic-fourth-incident-metr / healey-data-center-eo / christiano-openai-board** — ran. **coxon-quits-anthropic / ramp-ai-spend-stall / suno-v6-licensed / claude-session-key-theft (Sept. 8) / edge-extension-reviews / andersen-v-stability (still unverified)** — alternates.
- **chelsea-6-3-leeds / liverpool-2-1-atletico-iraola / dodgers-14-1-reds-sweep / pirates-4-2-white-sox-500 / union-5-0-fcc-nwobodo-red / dc-2-1-crew-baribo / bengals-report-all-full / browns-report / wvu-rodriguez-staff-meeting / usmnt-roster-sept17** — ran. **spurs-mudryk-6-8-weeks (aggregators only) / marshall-mtsu-preview / ohio / spurs-nba / hannan-point-jv-unreported** — sat out. **liverpool-spurs-cup-sept15** — RESOLVED. **hannan-roane-logan** — still owed, for Ian.
- **hoshoryu-no-practice-two-days-friday-decision / kirishima-19-of-24** — ran. **aonishiki-15-of-15** — leagues note. **seahawks-13-10-patriots / brewers-8-6-cubs / phillies-11-7-astros-schwarber-slam / arsenal-1-0-napoli-ucl-roundup / us-open-women-semis-thursday** — ran. **rays-braves-7-2 / orioles-guardians-9-5 / mets-15-14 / bowers-meniscus / mayfield-165m / gonzalez-135m** — note or alternates.
- **squirrel-sept12 / bear-youth / bear-gun-second / youth-waterfowl-sept19 / archery-sept26 / red-drum / seatrout-pattern / spanish-bluefish-footnote / black-drum / flounder-day-ten / early-goose-closes-sunday** — ran. **gauley-opens-friday / tailwaters-closed / fr19-dolly-sods-sept14 / fr76 / dmf-index-moved-partial / stocking-none / elk-tours / nhf-day** — seasons note. **williams-48-falling / rlx-front-flash-flood / mason-ffw-point-pleasant / huntington-nwps-reissued-26-8-crest / usace-cert-mismatch / topsail-fp-nine-days / pender-moderate-rip / nhc-quiet / new-moon-tonight-springs** — water block.
- **direction-gate-record-regex** — the WVU brief lost "42-7" and "1-1" to it; records in prose trip the score gate — for Nate, with the tuple-order note. **fetch-fishing-24h-window-bug** — still for Nate (did not bite). **detached-head-thirteenth** — recurring.

### Covered slugs, 2026-09-10

`trump-5000-dividend-war-ends-after-election-brent-100`, `foulkes-ousts-mckee-ri-primary`, `tate-brothers-bail-denied-miami`, `ntsb-cvr-pilot-warned-too-fast`, `osers-kelly-rogers-resigns-hhs-move`,
`philippines-june-aster-ferry-fire-5-dead-87-missing`, `vucic-dissolves-parliament-oct25`, `gambia-barrow-blackouts-pledge`, `netanyahu-mount-hermon-syria-condemns`,
`ascend-wv-2-4m-health-workers-hurricane`, `operation-coal-country-59-arrests`, `weld-locker-room-filming-felony-brooke`, `wvu-recognizes-three-fraternities-burch`,
`mason-leon-route-62-fatal-fire`, `putnam-united-data-center-accountability-project`, `parkersburg-7th-street-camden-clark-east-tower`, `hallohinton-oct17-oct23-24`, `putnam-block-phase-2-design-review`, `webster-county-fair-camp-caesar-sept9-12`, `topsail-beach-9-11-walk-friday`,
`pg-council-forestry-wildfire-inquiry`, `pg-nominations-friday-olson-25`, `bc-forestry-15-groups-breaking-point`, `bc-washington-labour-day-crossings-49`, `zelenskyy-carney-calgary-banff`, `saddle-lake-cree-defies-alberta-trans-law`,
`copernicus-august-2026-joint-hottest-1-65c`, `chandra-84-hypersoft-x-ray-sources`, `feedbacks-20-30-percent-erl`, `seattle-coyotes-9x-density`,
`anthropic-fourth-cyber-incident-metr`, `healey-data-center-executive-order-25mw`, `christiano-openai-foundation-board`,
`chelsea-6-3-leeds-carabao`, `liverpool-2-1-atletico-iraola-first-ucl`, `dodgers-14-1-reds-sweep-de-la-cruz-five`, `pirates-4-2-white-sox-73-73`, `union-5-0-fcc-nwobodo-red`, `dc-2-1-crew-baribo`, `bengals-week1-report-chase-higgins-stewart-full`, `browns-week1-report-nobody-out`, `wvu-rodriguez-staff-meeting-pissed-off`, `usmnt-pochettino-fresh-start-roster-sept17`,
`hoshoryu-skips-practice-two-days-decision-friday`, `kirishima-19-of-24-arashio`, `seahawks-13-10-patriots-maye-3-int`, `brewers-8-6-cubs-yelich`, `phillies-11-7-astros-schwarber-slam-44`, `arsenal-1-0-napoli-odegaard-25-goals`, `us-open-women-semis-thursday-top-four`,
`squirrel-sept12`, `bear-youth-sept12-13`, `bear-gun-second-window-sept19-25`, `youth-waterfowl-sept19`, `archery-deer-bear-sept26`, `red-drum-slot`, `seatrout-slot-pattern`, `spanish-mackerel-12-15-bluefish-3`, `black-drum-limits`, `flounder-day-ten-ff-27`, `early-canada-goose-closes-sept13`,
`gauley-season-opens-friday-tailwaters-closed`, `fr19-dolly-sods-closure-sept14-25`, `fr76-cranberry-closure-nov20`, `dmf-index-moved-partial`, `stocking-none`, `elk-tours-sept13`, `nhf-day-sept19-stonewall`, `williams-48-cfs-falling`, `rlx-front-flash-flood-thu-fri`, `mason-county-flash-flood-warning-815`, `huntington-nwps-26-8-crest-saturday`, `usace-huntington-cert-mismatch`, `topsail-fp-sept1-nine-days`, `pender-moderate-rip-low-waterspout`, `nhc-no-formation-7-days`, `new-moon-tonight-spring-tides`

## 2026-09-11 — No. 38 (Times) and No. 28 (Sports & Sportsman)

| Open-ended | **Seventeenth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), all filed between 5:39 and 5:44 a.m. ET. Both papers validated, rendered and pushed at **5:45:19 a.m. ET** (commit 237d9b5), 15 minutes after the 5:30 wake. Digest dry-run 1,125 embed chars, hero attached. The 6:53 `send_later` wake ran the post in the foreground; `--not-before` held 6 minutes and **the digest landed at 7:00:01 a.m. ET** (1,125 embed chars, hero attached, degraded []). Pages served both dated pages 200 by 5:47, about two minutes after the push. **Detached HEAD at session start again — fourteenth occurrence**; `git checkout main && git reset --hard origin/main` fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **All three fetchers clean on the first try**: stats 4 entries, `fetch_fishing.py` 0 source errors at 5:32:46 (Williams 44.2 cfs falling from 54.9; Point Pleasant 25.68 ft rising from 24.72; Huntington 28.54 ft rising from 26.41, the fetcher's own "up and pushing" read), standings 5 clubs (Pirates 74-73 third, 17.0 back, 4.5 out of a wild card; Reds 69-77 fifth). The 24h-ago values were sane | |
| Open-ended | **`editions/sportsman/index.json` stops at No. 11 (2026-08-25)** because only `post_discord.py` ever appended to it and the sports post retired. The playbook still says to compute the sports number from that index; computing it that way gave **No. 12** this morning and the assembly script had to take the max across `editions/sportsman/*.json` instead (28). `instructions/sportsman.md` §0 should say so, or the renderer should append to the index; not changed by the routine | **for Nate — a rule that says one thing and a file that does another** |
| Open-ended | **Lead art fell to rung 2 for the first time in eight days, and the placement moved to `wv`.** Every photograph of the lead — Al Jazeera's (a fighter shouldering an RPG launcher, Sanaa rally), France 24's and NPR's (armed men with rifles, faces to camera) — is weapons and identifiable faces, which the ladder refuses. Drew WCHS's Point Pleasant frame instead: a loading-dock doorway in a block wall above standing floodwater, the figure a faceless contour on the threshold, a utility pole, the door reflected. Seeded Python script, 324 paths, 29 KB, rasterized with headless Chromium and looked at before committing; the first pass was 502 paths and the block joints had to thin. Crude but reads as a flooded street | **worth keeping: a weapons-first lead photo is not a rung-1 subject** |
| Open-ended | **The lead was the Houthi seizure of Mocha** (Al Jazeera; cross-checked AP via PBS and France 24), with Friday morning's landing on Mayyun Island (France 24/AFP, 11:21 Paris) folded into the headline, dek and third paragraph, and the World desk's Mayyun brief swapped for the Pavlohrad mall strike so the story ran once. Saba's 40 strikes attributed; France 24's "64 in 24 hours" not used. Bukavu toll: Al Jazeera's headline and Radio Okapi say 29 children, Kanyuka's breakdown totals 24 — printed "at least 29 people... included 19 girls and five boys," the article's own form. CBS's A-10/eight F-15s report ran as CBS's own sourcing now that it is a second independent chain after The National/JPost | |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley, nicholas_webster), away 1, hotspots 2 — seven lines.** Statewide: Point Pleasant flooding aftermath (WCHS, with WSAZ's road list; WOWK's "30+ 911 calls" NOT used because WOWK is behind a HUMAN challenge), Armstrong 500-mile/5,000-home fiber (MetroNews), Logan Elementary will not reopen (WSAZ), charter board border-county tuition (News and Sentinel — the bylaws/FY28 budget outcomes are NOT in its account). **Summers empty** (WVVA's newest Summers item Aug. 19). Away: SVUESD names Foster to the Act 170 merger study (Banner). **Cabin: The Webster Echo (webconews.com) OPENED via curl with a Safari UA** — homepage and ledes readable, bodies paywalled; ran the Sept. 8 courthouse smoke evacuation. Topsail: NTB Fire and Rescue's 110-floor stair climb Friday 8:46 a.m. (WECT); northtopsailbeachnc.gov/news opened again (403 yesterday). **Hens vote outcome still not posted anywhere** (WECT, Port City Daily, town site) | **watch: hens outcome (third morning), Brooke County suits (WV Record 429), jail-death ruling** |
| Open-ended | **Canada 2/2/2.** Croft Road CLOSED — council approved the variance Wednesday, Yu, Sampson and Skakun voting no, no tally given (CKPG); Elev8 names six incumbents to campaign against (CKPG); Portland Canal terminal at Stewart opened (CBC, Sept. 9, written "this week"); Surrey arena demolition (CBC); Carney–Zelenskyy 100-year pact (CBC; the Globe's "one-third of drones" and $350M figures not in the CBC piece and not used); Carney will not fund the federalist side of the Oct. 19 referendum (Globe). **CBC article pages 403 on WebFetch today; curl with the Safari UA works.** PG Citizen is a Cloudflare JS wall but `princegeorgecitizen.com/rss/local-news` serves a full feed. Skakun's FedEx Boundary Road lease claim is a single councillor's account — not run | **watch — FedEx/airport confirmation; nominations closed 4 p.m. PT Friday, final slate tomorrow** |
| Open-ended | **Sumo: Hoshoryu WITHDREW** from the Aki basho at Friday morning's bout-drawing meeting — third straight basho out, 10th overall, first day-one withdrawal of his career; Tatsunami: "could not get him to a state where he can put out his strength" (Sponichi, Jiji). Onosato the lone yokozuna. Day 1: Onosato v. Daieisho, Kirishima v. Kotoshoho, Aonishiki v. Kotoeiho (Sankei). Kyujo list: Wakatakakage (July surgery; a full absence at M12 means juryo in November) and Wakanosho (Hochi). JSA kyujo page 404/500; Japan Times paywalled after the lede; r/Sumo empty shell. Kyushu basho opens Nov. 8, Fukuoka Kokusai Center (Hochi) | **the basho opens Sunday; tomorrow carries the Day 1 preview, Sunday's paper the first results** |
| Open-ended | **Sports results all from box scores**: Pirates 2-0 White Sox (Jones 7 IP 1 H 8 K, Cruz HR 18, Montgomery S12, sweep, four straight; "in Chicago" because CBS says Guaranteed Rate Field and yesterday's paper said Rate Field), 49ers 27-7 Rams at the MCG (crowd 100,021), Braves 3-1 Rays, Astros 2-1 Phillies (Cam Smith 9th-inning HR), Sabalenka d. Pegula 7-5 6-2, Rybakina d. Gauff 3-6 6-4 6-4 (No. 1 Monday, ending Sabalenka's 99-week run; final Saturday). Bengals: Turner added limited, Stewart to limited, Chase/Higgins full. Browns: Jenkins DNP (back). Tottenham: Sky's own reporter on Mudryk six to eight weeks, Richarlison and Maddison back — attributed to Sky, no injury type printed. **FOX changed the Friday probables from yesterday: Dotel (not Ashcraft) for the Pirates, May (not Drohan) for the Brewers.** Hannan: no outside source has Thursday's Westside result or Wednesday's Point JV; a search summary served a 4-2 Hannan-Westside result from Oct. 9, 2025 — not this match | **hannan-westside / hannan-point-jv — still owed, for Ian** |
| Open-ended | **Outdoors: all four waters reported.** NWPS Huntington forecast issued 4:10 p.m. Thursday: crest 29.8 ft at 2 a.m., 29.0 at 8 a.m., 27.5 by 8 p.m., 26.1 Monday; NWPS observed 28.62 at 5 a.m. vs the fetcher's USGS 28.54 — only the fetcher's number printed. RLX 5:24 a.m. discussion raises flash-flood concern for Saturday. ILM surf zone: rip LOW (was moderate), waterspout moderate (was low), heat index 103. NHC quiet. New moon 11:27 p.m. ET Thursday (USNO) — springs, written as such. NCDMF: FF-27-2026 opened in full via the limits page's direct link (flounder closes Sept. 14 11:59 p.m.); the proclamation index rendered one header line. WVDNR migratory bird PDF re-read (early goose closes Sept. 13; youth waterfowl Sept. 19/Oct. 31; regular goose Oct. 3). Fisherman's Post still Sept. 1 (ten days). Elk tour and NHF Day dates could not be re-confirmed on a DNR page (news-releases 404) and are flagged in the note | **watch — Saturday's rain on the Williams and the Ohio; wvdnr.gov/news-releases/ 404** |
| Open-ended | **Sci/Tech and AI.** USSF-153 from Vandenberg 11:42 a.m. ET Thursday, B1081's 27th flight (Spaceflight Now; Space.com's "B1801" is a typo); Sanger Nature Genetics chemo/clone paper; DLR Mercury contraction (GRL); Mount Sinai WTC responders (Nature Communications, on the anniversary). AI: Anthropic's September threat report naming Alibaba (151M exchanges), Moonshot and DeepSeek — the movement on Tuesday's NSA/FBI/CISA brief, labeled the company's own figures; GreyNoise-traced PaperCut campaign on Codex/DeepSeek agents, 395 orgs (The Register); Schmitz/CAIF/GovAI "agentic flooding," 84 cases (TechCrunch). **Progress 96 is now TBD** per Spaceflight Now; Crew-13 delayed from Sept. 12, TBD | |
| Open-ended | **Source status.** NEWLY OPENED: The Webster Echo (curl + Safari UA, ledes only), northtopsailbeachnc.gov/news, Kyiv Independent, jiji.com, Sponichi/Sankei/Hochi via Yahoo Japan, The Register (curl), Space.com (curl only), nature.com article pages (curl), EurekAlert, Spaceflight Now, NPS Gauley page, FS Monongahela alerts, deq.nc.gov limits page and FF-27 PDF, api.weather.gov, NWPS HNTW2, princegeorgecitizen.com RSS. BLOCKED: WOWK and WBOY (HUMAN challenge), WV Record/legalnewsline (429), DW, CNBC, Washington Times, Quartz, science.org/news, The Verge (tool refusal), Courthouse News, MIT Tech Review (JS shell), Mount Sinai and UTHealth newsrooms, CBC via WebFetch (403; curl works), PG Citizen article pages (JS wall), PBS Mocha page (my guessed URL 404 — the desk's PBS read was a different URL), ESPN pages (empty), Japan Times via WebFetch (402), sumo.or.jp kyujo (404/500), old.reddit.com (empty shell), tottenhamhotspur.com/news and chelseafc.com/en/news (empty shells), NPR via WebFetch (503; curl works), wvdnr.gov/news-releases/ (404) | **watch** |
| Open-ended | **Traps dodged.** (1) Search summaries said "Rays 7, Braves 1," "Phillies 2, Astros 1" and "Brewers 4, Cubs 3 (10)" — the boxes show Braves 3-1, Astros 2-1, and neither Milwaukee nor Chicago played. (2) A summary said Putnam's board "voted unanimously Wednesday" on a superintendent — that vote was May 27. (3) A summary dated the Wood County warehouse fire Sept. 10; WCHS's page is July 5. (4) Bukavu 29 vs 24 (above). (5) Pavlohrad 4 vs 5 dead — Kyiv Independent's body says five, its URL slug four. (6) Hong Kong: France 24 said one judge, NPR/HKFP a three-judge panel — wrote "a national security court." (7) Sahrawi eligible: 70,000–120,000 (AJ) vs ~80,000 (Euronews) — the cited outlet's figure only. (8) PPI "highest of 2026" not on the BLS page — omitted. (9) Nature's "star sensitive to Sgr A* spin" is Aug. 19; UQ dark-energy preprint is Sept. 4. (10) MetroNews "10,000 homes" is the all-programs figure; Armstrong's own is 5,000 — both stated as such. (11) Hannan 4-2 Westside is an October 2025 result. (12) Croft Road: three no votes named, no tally — did not infer 6-3 | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-11** | **August CPI 8:30 a.m.; Trump at the Pentagon and Vance at Ground Zero for 9/11; Gauley releases 11-14; PG nominations closed 4 p.m. PT; Potato Festival, Summersville (11-12); NTB stair climb 8:46 a.m., Bennington Veterans Home ceremony; Toensing leaves DOJ; Parker Solar Probe telemetry downlink; U.S. Open men's semis; Pirates at Cubs 2:20 (Dotel v. Imanaga); Reds at Brewers 7:45 (Abbott v. May)** | |
| **2026-09-12** | **U.S. Open women's final, Sabalenka v. Rybakina; WV squirrel opens, youth bear weekend; Webster County Fair closes 4:30; WVU v. UT Martin 1, Ohio v. Jacksonville State 6, Marshall v. MTSU 7; Chelsea v. Hull and Liverpool v. Fulham 10 a.m., Spurs v. Everton 12:30; Pirates at Cubs 2:20 (Skenes v. Holmes); Reds at Brewers 7:10 (Singer v. Harrison); Crew v. Red Bulls and FCC v. Charlotte 7:30** | |
| **2026-09-13** | **Aki basho Day 1 (Onosato v. Daieisho, Kirishima v. Kotoshoho); Sweden general election; WV early Canada goose closes; Falcon 9 / O3b mPOWER; North Bennington block party; Bengals v. Bucs and Browns at Jaguars 1 p.m.; Reds at Brewers 2:10 (Drohan); Pirates at Cubs 2:20; U.S. Open men's final** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m. (FF-27); FR 19 Dolly Sods closure begins; Rybakina No. 1; Vega-C Sentinel-3C/FLEX (14/15); Reds v. Dodgers 6:40; Bennington Select Board option-tax session** | |
| **2026-09-15** | **Liverpool v. Tottenham, Carabao Cup, Anfield, 3 p.m. ET (house derby); Fed meeting (15-16); Hannan v. Parkersburg Catholic 6 p.m.; Pirates v. Brewers and Reds v. Dodgers 6:40** | |
| **2026-09-16** | **U.K. formal Tate extradition request due; Crew v. Orlando City, Open Cup semifinal, 7 p.m.; Progress 96 TBD (was NET 16th)** | |
| **2026-09-17** | **USMNT roster; Pirates v. Brewers 12:35 p.m., Reds v. Dodgers 12:40 (Singer v. Glasnow); Hannan at Westside 6 p.m.; Gauley Fest opens** | |
| **2026-09-18** | **Chelsea at Brentford 3 p.m. ET; Pirates v. Royals and Reds v. Cubs 6:40; Gauley releases 18-21** | |
| **2026-09-19** | **WV bear gun second window (19-25, selected counties); youth waterfowl day; Spurs v. Villa 7:30 a.m. ET; Norfolk & Southern at Jerry Run, Cleveland WV, 7 p.m.; U.S. 7 Bennington closure begins; Asian Games open (to Oct. 4)** | |
| **2026-09-20** | **Bournemouth v. Liverpool 9 a.m. ET** | |
| **2026-09-21** | **House of Commons returns** | |
| **2026-09-30** | **Surf City cross-connection RFP due 2 p.m.** | |
| **2026-10-03** | **WV regular goose season opens (first split, to Oct. 18)** | |
| **2026-10-05** | **Quebec election** | |
| **2026-10-12** | **Schmitz "agentic flooding" paper at AAAI AIES (12-14)** | |
| **2026-10-15** | **Act 170 merger-study group's first meeting due before this date (Bennington)** | |
| **2026-11-03** | **Kanawha excess-levy vote; Logan County SBA pitch in November (date TBD)** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka Kokusai Center** | |

### Open threads

- **houthis-mocha-mayyun-bab-al-mandeb** — led; follow-ups are the UNSC outcome, Saudi strikes on Mocha airport, shipping/insurance reaction, Brent. **cpi-august / trump-pentagon-9-11 / vance-ground-zero / digenova-toensing-doj / first-circuit-usps-ballot-rule / denver-lulac-ice-polls / kimmel-talarico-youtube** — alternates. **gop-convention-close / missouri-map-2022-lines / ppi-august / a10-f15-jordan (CBS second chain)** — ran.
- **pavlohrad-mall-strike-5 / bukavu-school-fire-29 / hk-vigil-sentences / spain-sahrawi-citizenship** — ran. **coron-ferry (5 dead, 86 missing) / iaea-iran-unsc-referral (Wednesday) / sweden-election-sunday / bonino-obit / putin-india-brics** — alternates.
- **point-pleasant-flooding-6-8-inches / armstrong-fiber-500-miles / logan-elementary-not-reopening / charter-board-border-tuition** — ran. **charter-bylaws-fy28-outcome (not reported) / nscale-site-flooded-again / brooke-suits (429) / jail-death-ruling (none)** — alternates. **hadco-spec-building / kanawha-levy-town-hall / wood-peoples-cartage-289k / potato-festival** — regional. **svuesd-foster-act-170** — away. **webster-courthouse-smoke / ntb-stair-climb** — hotspots. **topsail-hens (no outcome, third morning) / vermont-veterans-home-9-11 / surf-city-rfps** — alternates.
- **croft-road (CLOSED, approved) / elev8-six-incumbents / stewart-portland-canal-terminal / surrey-arena-demolition / carney-zelenskyy-100-year / carney-no-federalist-funding** — ran. **fedex-boundary-road (single councillor) / army-reorg-edmonton / delta-doctor-28100 / skakun-eighth-term / pg-final-slate** — alternates.
- **ussf-153 / sanger-chemo-clones / mercury-shrinkage-dlr / wtc-responders-heat** — ran. **parker-perihelion-29 / uthealth-vanderbilt-protein-signatures / link-swift / crew-13-tbd / progress-96-tbd** — alternates.
- **anthropic-alibaba-151m-distillation / papercut-ai-agents-395 / agentic-flooding-84** — ran. **coxon / ramp / suno-v6 / andersen-v-stability (unverified)** — alternates.
- **pirates-2-0-white-sox-sweep / bengals-report-turner / browns-jenkins-dnp / spurs-mudryk-sky / wvu-alley-contain / marshall-gibson-never-recovered** — ran. **reds-idle / chelsea / liverpool / hannan / crew / fcc / ohio / spurs-nba / usmnt** — sat out. **hannan-westside / hannan-point-jv / hannan-roane-logan** — still owed.
- **hoshoryu-kyujo-third-straight / day-1-torikumi / wakatakakage-wakanosho-kyujo / 49ers-27-7-rams-melbourne / braves-3-1-rays / astros-2-1-phillies / sabalenka-rybakina-final** — ran.
- **squirrel-sept12 / youth-bear / bear-gun-second / youth-waterfowl / archery-sept26 / red-drum / seatrout / spanish / black-drum / sheepshead / flounder-day-11 / early-goose-closes-sunday** — ran. **gauley-opens-today / fr19 / fr76 / dmf-index-header-only / stocking-none / elk-nhf-unconfirmed** — seasons note. **williams-44-falling / rlx-saturday-flash-flood / point-pleasant-25-68-rising / huntington-28-54-crest-29-8 / ilm-rip-low-waterspout-moderate / nhc-quiet / new-moon-springs / topsail-fp-ten-days** — water block.
- **sportsman-index-stale-no-12** — for Nate. **fetch-fishing-24h-window-bug** — still for Nate (did not bite). **direction-gate-record-regex** — for Nate. **detached-head-fourteenth** — recurring.

### Covered slugs, 2026-09-11

`houthis-seize-mocha-mayyun-island-bab-al-mandeb`, `vance-trump-close-dallas-convention`, `scotus-rejects-missouri-map-2022-lines`, `ppi-august-0-4-diesel-24`, `cbs-a10-wing-eight-f15s-jordan`,
`pavlohrad-mall-strike-5-dead-67`, `bukavu-school-fire-29`, `hong-kong-vigil-organizers-sentenced`, `spain-sahrawi-citizenship-168-31`,
`point-pleasant-floods-6-8-inches-mason-schools`, `armstrong-fiber-500-miles-5000-homes`, `logan-elementary-will-not-reopen`, `charter-board-border-county-tuition`,
`hadco-spec-building-huntington`, `kanawha-levy-town-hall-nitro`, `wood-county-peoples-cartage-289k`, `potato-festival-summersville-56th`, `svuesd-foster-act-170`, `webster-courthouse-smoke-motor`, `ntb-fire-stair-climb-846`,
`pg-croft-road-variance-approved`, `elev8-six-incumbents`, `stewart-portland-canal-terminal-opens`, `surrey-arena-demolition-360m`, `carney-zelenskyy-100-year-pact-drones`, `carney-no-federalist-funding-referendum`,
`ussf-153-vandenberg-b1081-27`, `sanger-chemo-clones-nature-genetics`, `mercury-shrunk-10-30-dlr`, `wtc-responders-heat-frailty-ptsd`,
`anthropic-alibaba-151m-distillation`, `papercut-ai-agents-395-orgs`, `agentic-flooding-84-cases`,
`pirates-2-0-white-sox-jones-sweep`, `bengals-report-turner-limited`, `browns-jenkins-dnp-back`, `spurs-mudryk-6-8-weeks-sky`, `wvu-alley-40-pressures-contain`, `marshall-gibson-never-recovered`,
`hoshoryu-kyujo-aki-third-straight`, `aki-day-1-torikumi-onosato-daieisho`, `wakatakakage-wakanosho-kyujo`, `49ers-27-7-rams-mcg-100021`, `braves-3-1-rays-al-east-three`, `astros-2-1-phillies-cam-smith`, `sabalenka-rybakina-us-open-final-no-1`,
`squirrel-sept12`, `bear-youth-sept12-13`, `bear-gun-second-window-sept19-25`, `youth-waterfowl-sept19`, `archery-deer-bear-sept26`, `red-drum-slot`, `seatrout-slot`, `spanish-mackerel-12-15`, `black-drum-limits`, `sheepshead-14-5`, `flounder-day-eleven-ff-27`, `early-canada-goose-closes-sept13`,
`gauley-opens-today-releases`, `fr19-dolly-sods-sept14-25`, `fr76-cranberry`, `dmf-index-header-only`, `stocking-none`, `williams-44-cfs-falling`, `rlx-saturday-flash-flood-concern`, `point-pleasant-25-68-rising`, `huntington-28-54-rising-crest-29-8`, `ilm-rip-low-waterspout-moderate-heat-103`, `nhc-no-formation-7-days`, `new-moon-thursday-spring-tides`, `topsail-fp-sept1-ten-days`

## 2026-09-12 — No. 39 (Times) and No. 29 (Sports & Sportsman)

| Open-ended | **Eighteenth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), all filed between 5:38 and 5:45 a.m. ET. Both papers validated, rendered and pushed at **5:48 a.m. ET** (commit 0261fdb), 18 minutes after the 5:30 wake. Digest dry-run 1,068 embed chars, hero attached. The 6:52 `send_later` wake ran the post in the foreground; `--not-before` held 7 minutes and **the digest landed at 7:00:02 a.m. ET** (message 1548287059083530244, 1,068 embed chars, hero attached, degraded []). Pages served both dated pages 200 at 5:48:45, about 40 seconds after the push. **Detached HEAD at session start again — fifteenth occurrence**; `git checkout main && git pull origin main` fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **All three fetchers clean on the first try**: stats 4 entries (all up), `fetch_fishing.py` 0 source errors at 5:33 (Williams 54.9 cfs RISING from 44.2 after Friday's showers; Point Pleasant 24.69 ft falling from 25.68; Huntington 26.59 ft, fetcher says rising, NWPS trace flat 26.59-26.79 from 1:15 to 5 a.m. — the crest came and went, and the water block says so against the flag), standings 5 clubs (Pirates 74-74 third, 18.0 back, 5.5 out; Reds 69-78 fifth, 22.5 back, 10.0 out). **`out/fishing.json`'s 24h-ago fields again did not match Friday's printed readings** (Williams 47.6, PP 25.33, Huntington 25.92); the copy compared to Friday's printed numbers | **fetch-fishing-24h-window-bug — still for Nate** |
| Open-ended | **The lead was the Houthi story again, on its movement**: the full Red Sea coast and Mayyun taken Friday, Saudi Arabia suspending the East-West pipeline after drone attacks, crude closing above $100 (Al Jazeera primary; AP via NPR, NBC, PBS NewsHour, Times of Israel cross-checks). The World desk's Saudi-pipeline brief was swapped for its Nigeria alternate so the pipeline ran once. Numbers dropped on disagreement: $108 oil (Drop Site, unopened), diesel $6.06 vs "above $6", displaced 46,000 vs 44,000, PBS's 10% vs AP's 12% of goods (AP's, attributed). CPI: 3.4% y/y, +0.4% m/m, gasoline +27.4% y/y from bls.gov directly; PBS's "largest Cyclospora outbreak in U.S. history" not on the CDC page and not used | |
| Open-ended | **Art: RUNG 1, `placement: lead`.** Al Jazeera's lead photograph is a NASA satellite view of Bab al-Mandeb — a map-like scene, no faces, no weapons. Drew it freehand from a coordinate script (101 paths, 15 KB), rasterized with headless Chromium (`--window-size=800,620` and crop; at 800x500 the window clips the bottom of the frame) and looked at it before committing: the Yemen shore and cape, Djibouti's shore and headland, Mayyun with its lagoon, drift lines for water, sparse hatch for desert. Reads as the strait. First rung-1 drawing since Sept. 10 | **a satellite frame is a drawable lead photo — remember it** |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley, nicholas_webster), away 1, hotspots 2 — seven lines.** Statewide: Wood County Chemours PFAS class action, filed Sept. 4, reported Sept. 12 (News and Sentinel; no dollar figure in the story); Trump signs S. 858, the Woody Williams Medal of Honor monument bill, Thursday (Dominion Post; WCHS's "Thursday, Sept. 11" is self-contradictory and the Post gives two cities, so no city printed); CAIR asks WV police to investigate a Facebook threat listing mosques and a South Charleston school (WCHS); AG probes card-fraud complaints around a Cross Lanes Kroger (WSAZ — "dozens" is Del. Shamblin's count, attributed). **Summers empty** (Hinton News nothing since Aug. 6). Regional: DEP to investigate Nscale runoff flooding a Mason County yard a second time (WSAZ) — the only Point Pleasant flood movement found, no damage total or declaration anywhere; Capitol Connector to bid within weeks (WCHS, figures the city chief of staff's); Morrisey at Parkersburg High for Mary Lou Hague (N&S); Carnifex Ferry 165th reenactment Sunday 1 p.m. (WOAY). Away: U.S. 7 full closure Bennington-Arlington Sept. 19-Oct. 3 (Banner). Cabin: new Cowen VFD firehouse could break ground in spring (Webster Echo, Sept. 8, lede via curl). Topsail: Hughes Road at Center Drive closed Friday 9 a.m. to Monday 6 a.m. for a culvert (WECT). **WV MetroNews served a Cloudflare challenge to WebFetch, curl and /feed/ all morning — no MetroNews byline in either paper.** WV Watch RSS opens, article pages do not (lost the Senate Health chair death-penalty story). Webster County Fair closing-day line NOT printed: no openable page says it closes today. **Hens vote: fourth morning with no posted outcome; topsailbeachnc.gov root and news path both 404** | **watch: MetroNews challenge page; hens outcome; Point Pleasant damage totals; Brooke suits (WV Record 429)** |
| Open-ended | **Canada 2/2/2.** PG final slate: nine for mayor, 19 for council, withdrawals close Sept. 18, vote Oct. 17 (CKPG; My PG Now and the Citizen's RSS headlines agree); Fort St. John gang sweep, 26 arrests, northern gang team to launch in PG this year (CBC); Teresa Wat gives the unnamed ex-Conservative party a sixth seat (CHEK); B.C. judge stays an extradition over DEA conduct, April 1 ruling posted this week (CBC, said so); Alberta's $4M referendum ad campaign (CBC); Stellantis-Roshel Brampton MOU, Unifor contract ends Sept. 20 (Global). **FedEx/Boundary Road: the Citizen posted "Ontario company targets FedEx facility" at 22:41 UTC Friday but the page is a JS wall and no second outlet has it — a snippet says Dancor Construction, 40,000 sq ft on nine acres at 2157 Boundary Rd., November groundbreaking. NOT printed; retry Sunday.** Citizen RSS served headlines only today; CBC section indexes 403, RSS + curl article pages work; My PG Now curl only; CTV renders nav only | **watch — FedEx/Boundary Road confirmation** |
| Open-ended | **Sumo, eve of the Aki basho.** Jiji (Sept. 12): dohyo-matsuri held Saturday, Aonishiki receiving his July yusho portrait says he aims for the championship; Nikkan Sports via Yahoo Japan: judging chief Asakayama on Kirishima's tsunatori — "not just about winning," content must match results, no numeric target stated by anyone (Tokyo Sports' Sept. 4 YDC remark held as eight days old); Hochi: Tatsunami says Hoshoryu lost nearly 10 kg with appetite loss and insomnia, fifth kyujo in 10 basho as yokozuna. r/Sumo's .rss feed works (old.reddit is an empty shell) — leads only. Kyodo /news/sumo, NHK World sumo tag and nippon.com sumo index all 404. **Day 1 is Sunday: Sunday's paper carries the first results** | **Kirishima day 2 v. new komusubi Hakunofuji** |
| Open-ended | **Sports results all from line scores**: Cubs 12-2 Pirates (Imanaga W 10-10, Dotel L 1-5, Bregman HR 25, Reynolds HR 17; CBS box); Brewers 20-0 Reds (Mitchell grand slam, Abbott 2 IP 9 H 8 R; CBS box, 23 hits, largest clinch-day margin per MLB.com); Rays 3-1 Astros on Caminero's 40th, walk-off, first clinch (MLB.com); Shelton d. Tiafoe 4-6 6-3 6-3 7-5, meets Zverev Sunday (CBS); Zverev d. Khachanov 6-3 7-6(7) 7-6(6) (Tennis Majors, in the desk notes only); Missouri 38-21 Kansas (FOX box); Tua out, Cooper Rush starts at Pittsburgh (NFL.com); Kawhi trade still on hold (CBS). Ohtani to the 15-day IL, backdated to Sept. 8, eligible Sept. 23 — Yahoo/FOS said the 10th, MLB.com/NBC/Jiji the 11th, printed the 11th. **The validator's direction gate misread the Shelton brief because the headline's "beats Tiafoe" precedes the summary's "beat," so the last team named before the summary verb was Tiafoe; rewriting the summary without a listed verb ("won ... against") cleared it. It also flagged "1-1"/"(1-0)" college RECORDS as scores in three previews — rewrote them in words.** Our Teams: Stewart doubtful, Turner a go, Chase rested (Bengals.com — Dexter Lawrence II DNP with no reason, not printed); Jenkins out, rookie Barber starts (Browns); Alonso on Joao Pedro (Sky); Gakpo doubt (LFC); De Zerbi via GiveMeSport (Sky's item video-only); WVU (Dominion Post), Marshall (Herald-Dispatch), Ohio (WOUB), FCC without Evander (club). **Sky's "Caicedo out of Hull game as Neto signs new contract" headline had no readable body — NOT printed.** Hannan: fourth morning with no Westside or Point JV result anywhere (Point Pleasant Register 503) | **hannan-westside / hannan-point-jv — still owed, for Ian** |
| Open-ended | **Outdoors: all four waters reported.** Williams up 10.7 cfs overnight, first rise in a week — advice moved to a 9-foot leader and pupa/soft-hackle in the pocket water. Flood Watch for Webster, Mason and Cabell noon to 1 a.m. Sunday (RLX, 1:58 a.m.). ILM surf zone 5:35 a.m.: rip LOW both days, waterspout moderate. NHC quiet. New moon 11:27 p.m. ET Thursday (USNO) — springs. Water 83.3F at Beaufort. Fisherman's Post still Sept. 1 (11 days). **The WVDNR migratory bird PDF downloaded WITH certificate verification today (HTTP 200) and was read with PyMuPDF (pypdf is broken here); dove first segment through Oct. 11 at 15/45 printed for the first time; the early-goose bag garbled in extraction, not printed.** The validator matched "Mourning dove" to the pamphlet's combined migratory row and refused its dates — printed as species "Dove, first segment" so it falls to the confirm-by-hand warning like the goose and youth-waterfowl rows do. NCDMF bluefish footnote M read for the first time: 3/day private, 5/day for-hire. FF-27 re-read: flounder closes 11:59 p.m. Monday, Day 12 of 14. NCDMF proclamation index first page tops out at FF-24 and omits FF-27, so "nothing newer" is not a complete check. NCZ108 is Coastal New Hanover, not Pender; Pender's coastal zone is NCZ106 | **watch — Saturday's Flood Watch on the Williams; Sunday's Ohio forecast reissue** |
| Open-ended | **Sci/Tech and AI.** Murcia cell-therapy osteoporosis trial, Cell (Nature news, no control group, said so); IMpower030 EFS 62.8 v 34.9 months, missed significance (EurekAlert/WCLC Seoul); Rocket Lab GAO protest of the $700M MTN award (Space.com); Mount Sinai Sst-Chodl sleep neurons, Nature (Newswise; mountsinai.org 403). AI: 25 Fields medalists' letter, OpenAI drops Caltech sponsorship (TechCrunch — movement on Sept. 9's Navier-Stokes brief); Stop Rogue AI Act + Cruz bill after Coxon's exit (Al Jazeera; Coxon quit Sept. 8, bill Sept. 9, peg is the Sept. 11 piece, worded "after"); HarvestBench 0.4%-98.8% kill rates (The Register, preprint claims labeled). Falcon 9 / O3b mPOWER expected Sept. 13 | |
| Open-ended | **Source status.** NEWLY BLOCKED: **WV MetroNews** (Cloudflare challenge on every path, first time), WVNS (HUMAN challenge), WV Watch article pages, topsailbeachnc.gov (404 root and news), National Post, Ars Technica (tool refusal), CTV article bodies. STILL OPEN via curl+Safari UA: NPR, CBC, My PG Now, Space.com, nature.com, Newswise, The Register, The Webster Echo (ledes), Jiji, Hochi, Yahoo Japan mirrors. r/Sumo .rss works. wvdnr.gov migratory PDF fetched with verification today (the site root still fails). Kyodo/NHK/nippon.com sumo indexes 404 | **watch — is MetroNews back tomorrow?** |
| Open-ended | **Traps dodged.** (1) The FedEx/Boundary Road snippet with specific square footage — page never opened, not printed. (2) WCHS dated the Medal of Honor signing "Thursday, Sept. 11" — Sept. 11 is Friday; printed "Thursday" only. (3) Ohtani IL date 10th v 11th — took the three-source date. (4) Coron missing 54 (CBS) v 53 (Philstar) — cited outlet's figure. (5) A Sky index headline (Caicedo/Neto) with no body — not printed. (6) Yahoo Japan search snippets on Kirishima's "target" — no outlet states a number, none printed. (7) Search snippet "Webster County Fair Sept. 9-12" — unopenable, not printed. (8) WV bear gun-season bag numbers in the table row v the file's own warning — deferred to pamphlet pages. (9) Fetcher's "rising" flag at Huntington against a flat NWPS trace — printed the fetcher's string, explained the trace | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-12** | **U.S. Open women's final Sabalenka v. Rybakina; Chelsea v. Hull and Liverpool v. Fulham 10 a.m. ET, Spurs v. Everton 12:30; WVU v. UT Martin 1; Pirates at Cubs 2:20 (Skenes v. Holmes); Ohio v. Jacksonville State 6; Marshall v. MTSU 7; Reds at Brewers 7:10 (Singer v. Harrison); Crew v. Red Bulls and FCC v. Charlotte 7:30; Flood Watch Webster/Mason/Cabell noon-1 a.m.; Survive the 55 hike on Topsail through Sunday; Webster County Fair's last day (unconfirmed by an opened page)** | |
| **2026-09-13** | **Aki basho Day 1 (Onosato v. Daieisho, Kirishima v. Kotoshoho, Aonishiki v. Kotoeiho); Sweden votes; BRICS New Delhi closes; U.S. Open men's final Shelton v. Zverev; WV early Canada goose closes; youth bear weekend ends; Carnifex Ferry reenactment 1 p.m.; North Bennington block party; Falcon 9 / O3b mPOWER; Bengals v. Bucs and Browns at Jaguars 1 p.m.; Reds at Brewers 2:10, Pirates at Cubs 2:20; Kirishima v. Hakunofuji Day 2 (Monday's paper)** | |
| **2026-09-14** | **NC flounder closes 11:59 p.m. (FF-27); Iran-Gulf states meeting in Oman on Hormuz shipping; FR 19 Dolly Sods closure begins; Bennington Select Board 6 p.m.; Reds v. Dodgers 6:40 (Lodolo v. Skubal); Hughes Road reopens 6 a.m.** | |
| **2026-09-15** | **Liverpool v. Tottenham, Carabao Cup, Anfield, 3 p.m. ET (house derby); Hannan v. Parkersburg Catholic 6 p.m. at Ashton; Pirates v. Brewers and Reds v. Dodgers 6:40; FOMC opens (decision Wednesday)** | |
| **2026-09-16** | **FOMC decision; U.K. formal Tate extradition request due; Crew v. Orlando City, Open Cup semifinal, 7 p.m.; North Bennington Planning Commission 7 p.m.** | |
| **2026-09-17** | **USMNT roster; Pirates v. Brewers 12:35, Reds v. Dodgers 12:40 (Singer v. Glasnow); Hannan at Westside 6 p.m.; Gauley Fest opens** | |
| **2026-09-18** | **PG candidate withdrawal deadline; Chelsea at Brentford 3 p.m. ET; Pirates v. Royals (Skenes v. Dobnak) and Reds v. Cubs (Burns v. Holmes) 6:40; Gauley releases 18-21** | |
| **2026-09-19** | **U.S. 7 full closure Bennington-Arlington begins 7 a.m. (to Oct. 3); WV bear gun second window (19-25, selected counties); youth waterfowl day; NRG ranger talks (19-20); Spurs v. Villa 7:30 a.m. ET; Marshall at Missouri State 6:30, Ohio at South Alabama 7, WVU v. Virginia in Charlotte 7:30; Crew at Montreal 7:30** | |
| **2026-09-20** | **Unifor-Stellantis contract expires 11:59 p.m.; Bournemouth v. Liverpool 9 a.m. ET; NFL Week 2** | |
| **2026-09-23** | **Ohtani eligible to return** | |
| **2026-09-24** | **Trump-Xi summit (Haaretz)** | |
| **2026-09-26** | **WV archery/crossbow deer and bear open** | |
| **2026-10-01** | **Cabell County Clerk Scott Caserta retires; Pumpkin Festival Milton (1-4)** | |
| **2026-10-02** | **Surf City appraisal RFP due** | |
| **2026-10-03** | **WV regular goose season opens (to Oct. 18); U.S. 7 closure ends** | |
| **2026-10-05** | **Quebec election** | |
| **2026-10-07** | **PG advance voting (7, 8, 14, 15); general vote Oct. 17** | |
| **2026-10-11** | **WV dove first segment closes** | |
| **2026-10-14** | **September CPI** | |
| **2026-10-19** | **Alberta referendum** | |
| **2026-10-27** | **Israeli election** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka Kokusai Center** | |
| **2028-12-31** | **NASA Mars Telecommunications Network delivery deadline** | |

### Open threads

- **houthis-red-sea-coast-saudi-pipeline** — led again on the movement; follow-ups are the Oman meeting Monday, the pipeline restart, shipping/insurance, Brent, the UNSC. **cpi-august-3-4 / digenova-resigns / first-circuit-usps-ballots / cyclospora-over** — ran. **anthropic-houthi-users-blocked / trump-pentagon-9-11 / graham-sanctions-bill** — alternates.
- **coron-ferry-toll-35 / sweden-votes-sunday / odesa-mass-strike-11 / nigeria-suspends-sa-visits** — ran. **saudi-pipeline (folded into lead) / brics-new-delhi / guatemala-terrorism-charges-dismissed / iaea-iran (no movement) / serbia** — alternates.
- **chemours-pfas-class-action / medal-of-honor-bill-signed / cair-mosque-threats / cross-lanes-card-fraud** — ran. **wv-watch-death-penalty-child-sex-crimes (page would not open) / point-pleasant-damage-totals (none) / brooke-suits (429)** — alternates. **nscale-runoff-dep / capitol-connector-bid / hague-parkersburg-high / carnifex-ferry-165** — regional. **us-7-closure-sept-19** — away. **cowen-firehouse-spring / hughes-road-culvert** — hotspots. **bennington-cruiser-struck / bennington-meetings-week / survive-the-55 / caserta-retires-oct-1 / topsail-hens (no outcome, fourth morning) / webster-fair-closes (unconfirmed)** — alternates.
- **pg-final-slate-nine-19 / fort-st-john-sweep-26 / wat-sixth-seat / dea-extradition-stay / alberta-4m-ads / stellantis-roshel-brampton** — ran. **fedex-boundary-road (Citizen only, JS wall) / valleyview-dip-2027 / sd57-17-trustees / haida-gwaii-911 / carney-banff / scc-sentencing-deadlines** — alternates.
- **murcia-cell-therapy-osteoporosis / impower030-efs / rocket-lab-gao-protest / sst-chodl-sleep-neurons** — ran. **nsf-frontier-initiatives / superionic-ice / tmu-stec** — alternates.
- **fields-medalists-letter-openai-caltech / stop-rogue-ai-act-cruz / harvestbench** — ran. **deepseek-v4-1-flash / tuc-workplace-ai** — alternates.
- **cubs-12-2-pirates / brewers-20-0-reds / bengals-stewart-doubtful / browns-jenkins-out-barber / chelsea-alonso-joao-pedro / liverpool-gakpo-doubt / spurs-de-zerbi-maddison / wvu-two-win-start / marshall-payne / ohio-jsu-rematch / fcc-without-evander** — ran. **crew / hannan / spurs-nba / usmnt** — sat out. **hannan-westside / hannan-point-jv** — still owed. **caicedo-neto (no body)** — not printed.
- **aki-eve-dohyo-matsuri / kirishima-criteria-asakayama / hoshoryu-10kg-hochi / rays-clinch-caminero-40 / brewers-clinch-20-0 / ohtani-il / shelton-tiafoe / tua-out-rush / kawhi-hold / missouri-38-21-kansas** — ran. **zverev-khachanov / braves-6-5-phillies-11 / padres-fifth-straight / dodgers-eighth-straight / cardinals-white-sox-half-game / yankees-6-4-mets** — held for cap.
- **squirrel-opens-today / youth-bear-weekend / bear-gun-sept19 / archery-sept26 / youth-waterfowl-footnote-b / dove-first-segment / red-drum / seatrout / spanish / bluefish-footnote-m / black-drum / sheepshead / early-goose-closes-tomorrow / flounder-day-12** — ran. **gauley-day-2 / fr19 / fr76 / dmf-index-tops-at-ff24 / stocking-none** — seasons note. **williams-55-rising / flood-watch-webster-mason-cabell / point-pleasant-24-69-falling / huntington-26-59-flat / ilm-rip-low / nhc-quiet / new-moon-springs / topsail-fp-11-days** — water block.
- **sportsman-index-stale-no-12** — for Nate. **fetch-fishing-24h-window-bug** — still for Nate (did not bite; the copy compared to Friday's printed numbers). **direction-gate-headline-order / direction-gate-record-regex** — for Nate: the gate reads headline+summary as one text and takes the first LISTED verb, not the first in the text; and it reads a college record as a score. **metronews-cloudflare-challenge** — new. **detached-head-fifteenth** — recurring.

### Covered slugs, 2026-09-12

`houthis-seize-red-sea-coast-saudi-pipeline-shut`, `digenova-resigns-grand-conspiracy-probe`, `first-circuit-keeps-usps-ballot-block`, `cpi-august-3-4-gasoline-27-4`, `cyclospora-lettuce-outbreak-over-12883`,
`coron-ferry-toll-35`, `sweden-votes-sunday-sd-cabinet-posts`, `russian-strikes-kill-11-odesa`, `nigeria-suspends-south-africa-visits`,
`wood-county-chemours-pfas-class-action`, `trump-signs-woody-williams-monument-bill`, `cair-wv-mosque-threats`, `ag-cross-lanes-card-fraud`,
`nscale-runoff-dep-mason-second-time`, `capitol-connector-bid-weeks`, `morrisey-parkersburg-high-hague`, `carnifex-ferry-165th-reenactment`, `us-7-closure-bennington-arlington-sept-19`, `cowen-vfd-firehouse-spring`, `hughes-road-center-drive-culvert`,
`pg-nine-mayor-19-council-slate`, `fort-st-john-gang-sweep-26`, `teresa-wat-sixth-seat`, `bc-judge-stays-extradition-dea`, `alberta-4m-referendum-ads`, `stellantis-roshel-brampton-mou`,
`murcia-cell-therapy-osteoporosis-cell`, `impower030-efs-62-8`, `rocket-lab-gao-protest-mtn`, `sst-chodl-sleep-neurons-nature`,
`fields-medalists-letter-openai-caltech`, `stop-rogue-ai-act-cruz-bill`, `harvestbench-kill-rates`,
`cubs-12-2-pirates-bregman`, `brewers-20-0-reds-abbott`, `bengals-stewart-doubtful-turner-go`, `browns-jenkins-out-barber-starts`, `chelsea-alonso-joao-pedro-haaland`, `liverpool-gakpo-doubt-fulham`, `spurs-de-zerbi-maddison-back`, `wvu-two-win-start-ut-martin`, `marshall-payne-eight-catches`, `ohio-jsu-cure-bowl-rematch`, `fcc-evander-suspended-charlotte`,
`aki-eve-dohyo-matsuri-aonishiki`, `kirishima-tsunatori-asakayama-content`, `hoshoryu-10kg-tatsunami`, `rays-clinch-caminero-40-walkoff`, `brewers-clinch-20-0-largest-margin`, `ohtani-15-day-il-biceps`, `shelton-tiafoe-four-sets-final`, `tua-out-cooper-rush-starts`, `kawhi-trade-hold-clippers`, `missouri-38-21-kansas-border-war`,
`squirrel-opens-today`, `youth-bear-weekend-sept12-13`, `bear-gun-sept19-25`, `archery-sept26`, `youth-waterfowl-sept19-oct31-footnote-b`, `dove-first-segment-oct11-15-45`, `red-drum-slot`, `seatrout-slot`, `spanish-12-15`, `bluefish-footnote-m-3-5`, `black-drum-limits`, `sheepshead-14-5`, `early-goose-closes-sept13`, `flounder-day-12-ff-27`,
`gauley-day-2-releases`, `fr19-dolly-sods-sept14`, `fr76-cranberry`, `dmf-index-tops-ff24`, `stocking-none`, `williams-55-rising-first-rise`, `flood-watch-webster-mason-cabell`, `point-pleasant-24-69-falling`, `huntington-26-59-flat-crest-passed`, `ilm-rip-low-waterspout-moderate`, `nhc-no-formation-7-days`, `new-moon-thursday-springs`, `topsail-fp-sept1-eleven-days`

## 2026-09-13 — No. 40 (Times) and No. 30 (Sports & Sportsman)

| Open-ended | **Nineteenth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), launched 5:35, filed between 5:52 and 6:03 a.m. ET. Both papers validated, rendered and pushed at **5:58 a.m. ET** (commit 1f5d06e), 28 minutes after the 5:30 wake. Digest dry-run 1,070 embed chars, hero attached. The 6:52 `send_later` wake ran the post in the foreground; `--not-before` held 7 minutes and **the digest landed at 7:00:02 a.m. ET** (message 1548649448047911064, 1,070 embed chars, hero attached, degraded []). Pages served both dated pages 200 at 5:59:29, 32 seconds after the push. **Detached HEAD at session start again — sixteenth occurrence**; `git checkout main && git pull` fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **USGS was down at the 5:33 fetch (503 on all three gauges) and back by 5:37**; `fetch_fishing.py` re-ran clean before any water copy was written, 4 waters, 0 source errors. Stats 4 entries (indices up, Bitcoin down); standings 5 clubs (Pirates 74-75 third, 19.0 back, 6.5 out; Reds 69-79 fifth, 23.5 back, 11.0 out). **The fetcher's 24h-ago field was the 48-hour artifact on all three USGS gauges, and at Huntington it flipped the direction: flag and `read` said "falling" against Friday's 28.55 while the trace rose 1.10 ft since 5 p.m. Saturday (26.59 Sat 5 a.m. -> 27.69 Sun 5 a.m.) with an NWS crest of 28.7 forecast Monday afternoon.** The paper printed `reading` "27.69 feet, rising." and shortened the fetcher's `read` to drop "and falling"; the note says why. Williams 54.9 cfs / 1.34 ft identical to Saturday's 5:15 reading (flag "rising" against Friday's 45.3) — printed "flat". Point Pleasant 25.65 up 0.96 from Saturday's 24.69 (flag "steady" against Friday). The validator does not check trend words, only numbers | **fetch-fishing-24h-window-bug — still for Nate, and it now bites on DIRECTION, not just the comparison figure** |
| Open-ended | **The lead moved off the pipeline to the strait**: an Iranian cargo ship struck off Qeshm about 5 a.m. local Sunday, one crew member killed (Euronews primary, Qeshm governor Amir Teymouri named; AP via Local10/KSAT syndication, Al Jazeera liveblog and Times of Israel cross-checks), plus the Houthis' claimed strike on the Sharurah base in Najran and the Jazan mosque damage (Al Jazeera), the Oman meeting Monday and Bahrain's refusal (Al Jazeera Sept. 12). Numbers dropped on disagreement: wounded on the ship 3 (AP roundup, Euronews, ToI) v 4 (AP standalone, AJ); Oman venue Muscat v Salalah; Yemen displaced 46,000 (UN via NBC) v 76,000 (IOM via AJ). Second-choice lead was Iraq seizing the Maysan launch platform (AJ) — carried nowhere today; **the pipeline itself had no restart reported anywhere opened by 6 a.m.** Trump's Dublin "war ends after the midterms" remark exists only on CNBC (403) — not printed | **watch: pipeline restart; Oman meeting outcome Monday; UNSC** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** Euronews' og:image is an AFP frame of commercial ships anchored in haze off Bandar Abbas with two small motorboats crossing the foreground — no faces, no weapons. Drawn freehand (about 70 paths): a coastal tanker alone at left, three vessels clustered at right, broken drift lines for the sea, two boats with wakes, the two standing figures as contours with circle heads. Rasterized with headless Chromium and looked at before committing; reads as ships at anchor. The Aug. 14 drawing was the same subject (ships at anchor in haze) from an Al Jazeera photo — drawn differently, more ships, boats instead of a tug. Second rung-1 drawing in a row | |
| Open-ended | **Notebook: 4 statewide, 3 regional (huntington_cabell, putnam_kanawha, nicholas_webster), away 1, hotspots 2 — six lines.** Statewide: WVU BOG approves the $156M Milan Puskar west tower and extends Benson to June 2032 (WV News, Friday meeting); no-party ballots up 74% in the closed May primary (West Virginia Watch reporting, opened via the Gazette-Mail reprint — source says WV Watch, URL is the reprint because WV Watch article pages sat behind Cloudflare); Saturday storms close four Wood County roads and NWS life-threatening flood warnings for east Kanawha/Clay (WTAP + WSAZ — this took the mid_ohio_valley slot, so Wood ran no regional line); Helton's death-penalty bill (WV Watch canonical URL, body read via the WVNews reprint). Held: PSC staff urging rejection of MARL (Sept. 8 testimony, Gazette-Mail/WV News Sept. 10-11) and DOJ's appeal of the voter-data dismissal (WV Record, Sept. 9 notice). Regional: Cabell commission's $16,000 for the Pumpkin Festival Oct. 1-4 (Herald-Dispatch, Thursday meeting — at the edge of the window); Hurricane basement fire Friday night, 19 firefighters (WSAZ); Gauley season opened Friday with the first Summersville release (Herald-Dispatch; placed regional, not cabin, per the Summersville rule). **Summers empty** — Hinton News nothing local since Sept. 9 records column; a WVNS Route 3 crash story (Friday) 403'd unopened. Away: North Bennington Village Block Party TODAY noon-2 on the Park-McCullough grounds (Banner Sept. 2 + parkmccullough.org). Cabin: Wide Spot BBQ back after four years (Webster Echo Sept. 8, lede via curl). Topsail: USACE draft EIS for New River Inlet shore protection, NTB north end, hearing Sept. 22, comments to Oct. 19 (town site + the SAW-2016-02091 public notice PDF). **WV MetroNews Cloudflare challenge: second morning. WV Watch article pages now behind Cloudflare too (RSS works; Gazette-Mail and WVNews reprints open). webconews.com answers again (200 + RSS) — edition.md §3a's "blocked" note is stale. topsailbeachnc.gov answers WITHOUT www; www. 404s. Hens vote: FIFTH morning, the 9-9 meeting has agenda + video but no minutes and an empty board-actions column** | **watch: MetroNews/WV Watch challenge pages; hens outcome; Point Pleasant damage totals (none); MARL ruling; Nate should update §3a for webconews and the topsailbeachnc.gov no-www quirk** |
| Open-ended | **Canada 2/2/2.** PG: Mavrik Turnbull celebration of life at CN Centre, 100-200 attended (My PG Now; CBC BC preview agrees on the July 6 death and the foundation; duration "21-month" v "two-year" dropped); Quesnel three-way mayoral race, Oakes v Paull v Waters, 18 for council (CKPG). BC: BC Housing's HIFIS homeless database kept from municipalities since 2016 (CHEK's own reporting, "reported"); Qualicum Beach Primrose Medical Centre opening Nov. 2 (CHEK; mayor's surname spelled two ways in the piece, not printed). Canada: George Chuvalo dies at 89 on his birthday (CBC; CP via CKPG agrees on 73-18-2, never knocked down); Trump in Dublin says Canada "wants to make a deal very badly" (Global). **FedEx/Boundary Road: STILL unconfirmed — the Citizen article 403s to curl and WebFetch, CKPG and My PG Now site searches return nothing. Not printed a second morning.** Alternates: Carrier's mayoral platform, SD57 17 trustee candidates, Chetwynd Hillside Manor 46 displaced, Toronto abducted-children conference Sept. 28-29 (Anand), Carney investment summit Mon-Tue then Liverpool/Strasbourg | **watch — FedEx/Boundary Road confirmation; Carney-Burnham Tuesday** |
| Open-ended | **Sumo, Aki Day 1 — results printed from Kyodo, Yomiuri and Sports Hochi via Yahoo Japan, cross-checked against each other; the JSA's own results pages still read "information will be posted" at 5:45 a.m. ET.** Onosato hatakikomi over Daieisho ("barely" per Kyodo and Yomiuri); Kirishima uwatenage over Kotoshoho; Kotozakura yorikiri over Takayasu; Aonishiki yorikiri over Kotoeiho; Atamifuji (ozeki bid) yorikiri over Gonoyama; new sekiwake Fujinokawa over Yoshinofuji; new komusubi Hakunofuji LOST to Churanoumi (美ノ海 — reading is the desk's, confirm on the JSA English page). Day 2: Kirishima v Hakunofuji, Onosato v Kotoshoho (Kyodo torikumi story Sept. 11). Kyujo at juryo and above exactly three: Hoshoryu, Wakatakakage, Wakanosho. Jiji Sept. 13: JSA released the medical certificates — Hoshoryu right-knee MCL, ~3 weeks rehab; Wakatakakage ~2 months; Wakanosho ~4 weeks. Held: ex-komusubi Futagodake dies at 82 (Jiji); four recruits pass the exam, maezumo from Day 3 (Jiji). **r/Sumo: old.reddit .rss and HTML both returned the interstitial today, WebFetch refused — NOT consulted; Yahoo Japan search was the lead-finder instead.** nikkansports.com, hochi.news, NHK: WebFetch refused | **Kirishima v Hakunofuji Day 2 (Monday's paper); Onosato v Kotoshoho** |
| Open-ended | **Our Teams: 12 briefs, all results from box scores or match reports.** Chelsea 2-2 Hull (Rogers 7', Belloumi 28' 34', Joao Pedro 66'; Sky; Alonso: 20th straight PL match conceding); Liverpool 0-0 Fulham (club report; Munoz bar, Gakpo back as a 60' sub); Spurs 0-0 Everton (Sky; 0 goals in 4, 17th — the 18-3 shot count is from ESPN/Sky headlines only, printed "two shots on target"); WVU 52-7 UT Martin (Dominion Post; Hawkins 155 pass/96 rush — WV Sports Nation's 123/91 conflicts, DP+AP figures used); Marshall 28-26 MTSU (Herald-Dispatch; record 1-1 per FOX, an H-D fetch reading "1-0" ignored); Ohio 29-27 JSU in FOUR OT (CBS line score OT4 column; one CBS sentence says third — line score used); Red Bulls 1-0 Crew (Donkor 89'; VAVEL USA cited because columbuscrew.com's index was stale and the Red Bulls index had no minute); FCC 3-3 Charlotte (Local 12/AP; club report URL could not be isolated); Brewers 13-9 Reds (Singer 4 IP 8 ER 5 BB; CBS box); Cubs 4-3 Pirates (Skenes 7 IP 2 ER, Soto L; Busch, Ramirez HR; CBS box); Browns elevate Watson and Ross; Bengals elevate Giles-Harris and Hudson. **Sunday Reds probable CHANGED: Burns v Gasser, not Drohan (CBS preview + FOX).** Standings: Chelsea 7 pts 4th, Liverpool 6 pts 6th, Spurs 2 pts 17th (Sky 9:19 UK); FCC 32 pts EIGHTH (down from 7th), Crew 23 pts 13th (FOX). Sat out: Hannan (fifth morning with no Westside/Point JV result — MaxPreps, Westside's page, Point Pleasant Register 503, MetroNews 403, WVSSAC, Facebook shell), Spurs, USMNT (roster date NOT confirmed on ussoccer.com; Chile friendly Sept. 29 St. Louis). Week ahead through Sept. 20 incl. NFL Week 2 (Bengals at Houston, Browns at Tampa Bay, both 1 p.m. CBS), Bournemouth v Liverpool Sun 9 a.m. ET, FCC at Houston Sat 8:30 p.m. ET | **hannan-westside / hannan-point-jv — still owed, for Ian; NFL results Monday** |
| Open-ended | **Leagues: 13 briefs.** MLB: Braves 12-2 Phillies (lead six; ESPN/AP), Mets 12-2 Yankees (Lindor 2 HR incl. grand slam, Cole 5 ER; four behind the Rays who beat Houston 3-2), White Sox 6-5 Cardinals (Grichuk 9th; lead Cleveland by 1.5; MLB.com) — records for non-followed clubs deliberately written in words, not "88-61", to stay clear of the score regex. Held: Betts' 10,000th LA-era Dodgers homer in a 4-3 LOSS to Miami; Mariners 19-1 A's. Tennis: Rybakina d. Sabalenka 6-4 5-7 6-2 (ESPN/AP and CBS story agree; CBS live blog said 6-3 — two stories over one blog), No. 1 Monday; Shelton v Zverev today 2 p.m. ET (ATP). CFB: Texas 24-23 Ohio State (largest 4th-quarter comeback v an AP No. 1 per Sportradar; Manning 196 v 195 yards not printed), Oklahoma State 39-31 Oregon (FOX box confirms 39-31; a snippet said 36-31); held Michigan 17-10 Oklahoma. NFL: Stroud/Texans table talks (NFL.com, two named reporters); Kraft 4yr/$75M and Mayer 3yr/$45M (CBS); held Harbaugh's Giants debut v Dallas SNF, Rush back spasms. EPL: Arsenal 2-0 Sunderland (Raya penalty save, Guimaraes, Saka pen; City at United 11:30 a.m. ET). **The direction gate refused the Texas brief twice: with no "Texas" in the summary, the last team named before "beat" (in "comeback to beat an AP No. 1") was Ohio State from the headline. Fixed by naming Texas in the summary and writing "comeback against"** | **direction-gate-headline-order — for Nate (third occurrence)** |
| Open-ended | **Outdoors: all four waters.** Williams flat at 54.9/1.34 (flood watch did not verify — peak 56.2 cfs Sat 3-7 p.m. while Braxton/Lewis took 3.5-6.5 in); Point Pleasant 25.65 up a foot, NWS POPW2 forecast crest 26.6 tonight-Monday (correction: NWS DOES carry a Point Pleasant forecast point); Huntington 27.69 RISING to a 28.7 crest Monday afternoon (HNTW2). Mason: two flood warnings to 8 a.m., high water on Country Club and Letart roads at 8:20 p.m.; Cabell: watch only, no warning, no LSR; Webster: warning to 8:30 a.m. names Falls Mills (Braxton). ILM surf zone 2:31 a.m.: rip MODERATE today and Monday (was low Saturday), waterspout moderate, heat index 101/104. NHC: one central-Atlantic trough, 0%/20%. Moon: fetcher age 1.5 days — printed "a day and a half past new" and NO new-moon clock time, because the fetcher's age puts new moon ~5:30 p.m. Friday while Saturday's paper printed USNO's Thursday 11:27 p.m. ET; the desk did not open USNO today. **Resolve before printing a time again.** Fisherman's Post still Sept. 1 (12 days). **NWPS carries GALW2, "Ohio River at R C Byrd Lock," observed 20.74 ft at 5 a.m., forecast crest 24.9 Monday — different datum, no USGS id, not in fishing.json, so not printed, but it may be the tailwater the playbook says is unavailable.** Seasons: early Canada goose bag RESOLVED as 5/15 in aggregate (merged cell, 200-dpi render); bear gun 1/2/2 in the table row but deferred to pamphlet pages again; NCDMF index now runs to FF-38 (FF-36/37/38 all commercial flounder; FF-37 opens the commercial season 12:01 a.m. Tuesday, the morning after the recreational one closes; both September proclamations signed by Interim Director Michael S. Loeffler, where FF-27 was Kathy B. Rawls); flounder Day 13 of 14, Monday last day; Gauley note attributed to the NPS page, not "the Corps" (Corps 503) | **watch — Huntington crest Monday; Mason warnings; GALW2 for the fetcher; NCDMF director change; USNO moon time** |
| Open-ended | **Sci/Tech and AI.** MAVERICK/SWOG S1827 MRI v PCI, HR 0.60, presented Sunday in Seoul (EurekAlert; "presented," no journal); Flinders placoderm bite modes, Sci Reports (Phys.org, posted ~4:30 a.m.); UCL Lauca Caldera Andes uplift ~2.5 cm/century, Sci Advances Friday (EurekAlert); Penn EFEMP1 retinal disease, JAMA Ophthalmology Friday (Penn Medicine). Held: HARMONi-2 ivonescimab OS 30.8 v 22.6 (Akeso-sponsored; presentation date disputed Sept. 13 v 15), NSF Frontier Initiatives letter (Nature, Wednesday), EVOKE-03 miss. **O3b mPOWER F did NOT fly Saturday — Falcon 9 scheduled TODAY 2:49 p.m. EDT, SLC-40, backup Monday (Spaceflight Now); Vega-C Sentinel-3C/FLEX Monday 9:21 p.m. EDT.** AI: Amodei "We Must Pace the Frontier" essay (TechCrunch; essay opened via curl; Altman's "we will do the same" via TechCrunch; labeled a company statement); NM Supreme Court contempt for Aarons, $5,000, Wednesday (Ars via curl); RubyGems/OpenAI agents (Gulf News relaying WSJ, primary report rubyhack.ai opened; "hundreds" used, "2,000+" snippet not; OpenAI and RubyGems statements both carried). Held: Nvidia-Groq DOJ (Register relaying NYT), DeepSeek V4.1 Flash (763B v 552B disputed), TUC letter | **watch — O3b mPOWER launch result; Amodei essay reaction; HARMONi-2 oral Sept. 15** |
| Open-ended | **Source status.** NEWLY BLOCKED: West Virginia Watch article pages (Cloudflare; RSS fine), WVNS (403), PG Citizen article pages (403 both ways), old.reddit r/Sumo (interstitial on .rss too), NPR (WebFetch 503; curl 200), Rappler/Inquirer/Kyiv Post/ABC Australia/Ukrainska Pravda (403), CNBC/The Hill/UPI (403), usopen.org (503), science.org (403), Corps LRH (503), wvusports.com and ohiobobcats.com (403/title-only), columbuscrew.com news index stale. STILL BLOCKED: WV MetroNews (Cloudflare, second morning), WOWK. BACK: webconews.com (200 + RSS), USGS (after 5:37). OPEN via curl+Safari UA: DW, RNZ, Ars Technica, Nature news, Space.com bodies, darioamodei.com, The Register, CBC/CHEK/Global/CKPG/My PG Now, Gazette-Mail, WV News, Herald-Dispatch, WSAZ, WTAP, Bennington Banner, Park-McCullough, NTB town site + PDF, Surf City news flash, topsailbeachnc.gov (no www) | **watch — MetroNews/WV Watch; r/Sumo route** |
| Open-ended | **Traps dodged.** (1) Investopedia's Fed-hike preview existed only as a Yahoo syndication — held rather than link an aggregator. (2) AP's Hormuz story was read only through Local10/KSAT syndication — Euronews made primary, AP not put in a source field. (3) The Coron ferry toll doubled to 76 (AJ, Philstar, RNZ) but Indonesia's 243-aboard sinking was the Asia brief under one-per-region — Coron carried in the ledger, not the paper. (4) FedEx/Boundary Road snippet, second morning, not printed. (5) Webster County Fair "ended Saturday" — the Echo's Aug. 23 lede gives Sept. 9-12 but no post-fair page exists; BBQ line ran instead. (6) Topsail Beach's Friday south-end rules post was readable only as a summary — not printed because the rules themselves were not read. (7) Ohtani/Sayin-style digit disputes (Manning 196/195, Rybakina 6-4/6-3, Oklahoma State 39/36) resolved by two stories over one, or dropped. (8) Vanuatu ferry: direction of travel disputed (RNZ v AJ) and AJ misdated it — held. (9) Kraft "10 months after" was desk arithmetic — printed "after a torn ACL last season". (10) Hannan roster date "Sept. 17" for the USMNT could not be re-confirmed — not repeated | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-13** | **Aki Day 1 (ran); Sweden polls close 2 p.m. ET; U.S. Open men's final Shelton v. Zverev 2 p.m. ET; Bengals v. Bucs and Browns at Jaguars 1 p.m.; Reds at Brewers 2:10 (Burns v. Gasser), Pirates at Cubs 2:20 (Chandler v. Boyd); Giants-Cowboys 8:20 p.m. NBC (Harbaugh debut); Man City at Man United 11:30 a.m. ET; Falcon 9 / O3b mPOWER F 2:49 p.m. EDT (backup Monday); North Bennington block party noon-2; Lucas Fire red flag warning to 11 a.m. Monday; WV early Canada goose and youth bear close tonight; Lower Saxony local elections** | |
| **2026-09-14** | **Iran hosts Gulf ministers in Oman on Hormuz (Bahrain out); Aki Day 2 Kirishima v. Hakunofuji, Onosato v. Kotoshoho; NC flounder last day (closes 11:59 p.m.); FF-37 commercial flounder opens 12:01 a.m. Tuesday; Huntington crest 28.7 ft forecast Monday afternoon; Vega-C Sentinel-3C/FLEX 9:21 p.m. EDT; FR 19 Dolly Sods closure begins; Benson State of the University 3 p.m.; Canada Investment Summit opens Toronto (14-15); Reds v. Dodgers 6:40 (Lodolo v. Skubal); Bennington Select Board 6 p.m.; Chiefs MNF (Mahomes cleared)** | |
| **2026-09-15** | **Liverpool v. Tottenham, Carabao Cup, Anfield, 3 p.m. ET (house derby); Hannan v. Parkersburg Catholic 6 p.m. Ashton; Pirates v. Brewers and Reds v. Dodgers 6:40; FOMC opens; HARMONi-2 oral in Seoul; Carney meets Burnham in Liverpool** | |
| **2026-09-16** | **FOMC decision; Crew v. Orlando City, Open Cup semifinal, 7 p.m.; Reds v. Dodgers, Pirates v. Brewers 6:40; Carney addresses the European Parliament (State of the EU, Strasbourg)** | |
| **2026-09-17** | **Gauley Fest opens 8 a.m. Summersville (to noon Sept. 20); Hannan at Westside 6 p.m. Beckley YMCA; Pirates v. Brewers 12:35, Reds v. Dodgers 12:40 (Singer v. Snell)** | |
| **2026-09-18** | **PG and Quesnel candidate withdrawal deadline 4 p.m.; Chelsea at Brentford 3 p.m. ET; Reds v. Cubs (Burns v. Holmes), Pirates v. Royals (Skenes v. Dobnak) 6:40; Gauley releases 18-21** | |
| **2026-09-19** | **U.S. 7 full closure Bennington-Arlington begins (to Oct. 3); WV bear gun second window opens (19-25, selected counties); WV youth waterfowl day; Spurs v. Villa 7:30 a.m. ET; Marshall at Missouri State 6:30, Ohio at South Alabama 7, WVU v. No. 25 Virginia in Charlotte 7:30; Crew at Montreal 7:30, FCC at Houston 8:30** | |
| **2026-09-20** | **Bournemouth v. Liverpool 9 a.m. ET; NFL Week 2: Bengals at Houston, Browns at Tampa Bay, 1 p.m. CBS; Pirates v. Royals 1:35, Reds v. Cubs 1:40; Unifor-Stellantis contract expires 11:59 p.m.** | |
| **2026-09-22** | **North Topsail Beach public hearing on the USACE New River Inlet draft EIS, 6 p.m. Town Hall (comments to Oct. 19); Hannan at Calvary 6 p.m. (venue unconfirmed)** | |
| **2026-09-24** | **Trump-Xi summit; Hannan v. Roane 6 p.m. Ashton** | |
| **2026-09-26** | **WV archery/crossbow deer and bear open** | |
| **2026-09-28** | **Toronto conference on abducted Ukrainian children (28-29), Canada/Ukraine/Norway** | |
| **2026-09-29** | **USMNT v. Chile, St. Louis, 8 p.m. ET; Hannan at Roane 6:30** | |
| **2026-10-01** | **Pumpkin Festival, Milton (1-4); Cabell County Clerk Caserta retires** | |
| **2026-10-02** | **Surf City appraisal RFP due** | |
| **2026-10-03** | **WV regular goose and duck seasons open (goose to Oct. 18, ducks to Oct. 11); U.S. 7 closure ends** | |
| **2026-10-11** | **WV dove first segment closes** | |
| **2026-10-14** | **Topsail Beach board's next regular meeting (hens minutes?)** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18)** | |
| **2026-10-19** | **Alberta referendum; USACE draft EIS comment deadline (NTB)** | |
| **2026-11-02** | **Primrose Medical Centre opens, Qualicum Beach** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |

### Open threads

- **hormuz-ship-strike-houthi-saudi-base** — led; follow-ups are the Oman meeting Monday, the East-West pipeline (still shut, no restart reported), the ship's identity and the wounded count, Saudi response, Brent Monday. **iraq-seizes-maysan-launch-platform / yemenis-flee-to-djibouti-1400 / bahrain-skips-oman (folded into lead) / brics-new-delhi-declaration** — alternates.
- **fema-illston-ruling / alien-terrorist-court-first-deportation / lucas-fire-4008 / trump-dublin-irish-unity** — ran. **fed-hike-preview-86pct (Investopedia via Yahoo only) / measles-3294 / usps-ballots-scotus (no movement)** — alternates. FOMC Wednesday is the next U.S. peg.
- **ukraine-kyiv-warsaw-train-drone / indonesia-ferry-virgo-transport-8 / chile-pitrufquen-fire-16 / congo-ebola-7022** — ran. **coron-ferry-toll-76 (MOVED, not printed under one-per-region) / germany-anti-afd-150000 / vanuatu-ferry-matui / sweden-votes (result tonight — Monday's World lead candidate)** — alternates.
- **wvu-stadium-tower-benson / no-party-ballots-74pct / wood-roads-flood-warnings / helton-death-penalty** — ran. **psc-staff-marl-rejection / doj-voter-data-appeal / harrison-cage-abuse (WSAZ via WDTV) / point-pleasant-damage-totals (none)** — alternates. **cabell-pumpkin-festival-16k / hurricane-basement-fire / gauley-season-opens** — regional. **ntb-block-party-today** — away. **wide-spot-bbq / ntb-draft-eis-new-river-inlet** — hotspots. **bennington-cruiser-struck-dui / bennington-drug-ring-12-years / webster-fair-sept-9-12 / holly-river-festival / gauley-fest-sept-17 (Summersville) / topsail-beach-south-end-rules (unread) / surf-city-batts-addendum / topsail-hens (fifth morning) / wvns-route-3-crash (403)** — alternates.
- **mavrik-turnbull-cn-centre / quesnel-three-way-mayor / bc-housing-hifis / qualicum-primrose-clinic / chuvalo-dies-89 / trump-canada-deal-badly** — ran. **carrier-platform / sd57-17-trustees / chetwynd-hillside-manor / south-cariboo-rollover / iio-slingshot / cormorant-cruise-airlift / floor-crossers-repay / ukraine-children-toronto / carney-summit-europe / childhood-cancer-15m / alberta-turnout / oil-windfall-analysis / fedex-boundary-road (unconfirmed, second morning)** — alternates.
- **maverick-mri-vs-pci / placoderm-two-bites / lauca-caldera-andes / efemp1-eye-disease** — ran. **harmoni-2-os / nsf-frontier-initiatives / o3b-mpower-today / evoke-03 / nasa-ibm-lunar-model** — alternates.
- **amodei-pace-the-frontier / nm-court-chatgpt-contempt / openai-agents-rubygems** — ran. **nvidia-groq-doj / deepseek-v4-1-flash / tuc-ai-negotiation** — alternates.
- **chelsea-2-2-hull / liverpool-0-0-fulham / spurs-0-0-everton / wvu-52-7 / marshall-28-26 / ohio-29-27-4ot / red-bulls-1-0-crew / fcc-3-3-charlotte / brewers-13-9-reds / cubs-4-3-pirates / browns-elevate / bengals-elevate** — ran. **hannan / spurs-nba / usmnt** — sat out. **hannan-westside / hannan-point-jv** — still owed.
- **aki-day1-onosato-kirishima / aki-day1-aonishiki-hakunofuji / hoshoryu-diagnosis / braves-12-2 / mets-12-2-yankees / white-sox-6-5 / rybakina-title / shelton-zverev-preview / texas-24-23-osu / okstate-39-31-oregon / stroud-tabled / kraft-mayer / arsenal-2-0** — ran. **futagodake-dies / new-recruits / betts-10000 / mariners-19-1 / michigan-17-10 / harbaugh-giants / rush-spasms-mahomes** — held for cap.
- **youth-waterfowl-sept19 / bear-gun-sept19 / archery-sept26 / squirrel-day-2 / dove-first-segment / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead / youth-bear-closes / early-goose-closes-5-15 / flounder-day-13** — ran. **gauley-day-3 / ff-36-37-38-commercial / loeffler-interim-director / stocking-none / rails-snipe** — seasons note. **williams-flat / point-pleasant-up-a-foot / huntington-rising-crest-monday / mason-warnings / cabell-no-warning / ilm-rip-moderate / nhc-20pct / moon-1-5-days / galw2-tailwater** — water block.
- **sportsman-index-stale-no-12** — for Nate (No. 30 computed from the edition files, as No. 29 was). **fetch-fishing-24h-window-bug** — for Nate, now flipping direction at Huntington. **direction-gate-headline-order** — for Nate, third occurrence. **metronews-cloudflare-challenge** — second morning. **wv-watch-cloudflare** — new. **detached-head-sixteenth** — recurring.

### Covered slugs, 2026-09-13

`hormuz-ship-strike-qeshm-houthis-sharurah`, `fema-illston-ruling`, `alien-terrorist-court-first-deportation`, `lucas-fire-4008-acres`, `trump-dublin-irish-unity`,
`kyiv-warsaw-train-drone-453`, `indonesia-ferry-virgo-transport-8-243`, `chile-nursing-home-fire-16`, `congo-ebola-7022`,
`wvu-156m-stadium-tower-benson-2032`, `no-party-ballots-74pct`, `wood-county-roads-flood-warnings`, `helton-death-penalty-bill`,
`cabell-pumpkin-festival-16k`, `hurricane-basement-fire-19`, `gauley-season-opens-summersville`, `ntb-block-party-today`, `wide-spot-bbq-returns`, `ntb-draft-eis-new-river-inlet`,
`mavrik-turnbull-cn-centre`, `quesnel-three-way-mayor-oakes`, `bc-housing-hifis-database`, `qualicum-primrose-clinic`, `chuvalo-dies-89`, `trump-canada-deal-very-badly`,
`maverick-mri-vs-pci`, `placoderm-two-bite-modes`, `lauca-caldera-andes-uplift`, `efemp1-retinal-disease`,
`amodei-pace-the-frontier`, `nm-court-chatgpt-contempt`, `openai-agents-rubygems`,
`chelsea-2-2-hull-belloumi`, `liverpool-0-0-fulham`, `tottenham-0-0-everton-goalless`, `wvu-52-7-ut-martin`, `marshall-28-26-mtsu`, `ohio-29-27-jsu-4ot`, `red-bulls-1-0-crew-donkor`, `fcc-3-3-charlotte-denkey`, `brewers-13-9-reds-singer`, `cubs-4-3-pirates-skenes`, `browns-elevate-watson-ross`, `bengals-elevate-giles-harris-hudson`,
`aki-day1-onosato-kirishima`, `aki-day1-aonishiki-hakunofuji`, `hoshoryu-mcl-3-weeks`, `braves-12-2-phillies`, `mets-12-2-yankees-lindor`, `white-sox-6-5-cardinals-grichuk`, `rybakina-us-open-title`, `shelton-zverev-final-preview`, `texas-24-23-ohio-state`, `oklahoma-state-39-31-oregon`, `stroud-texans-table-talks`, `kraft-75m-mayer-45m`, `arsenal-2-0-sunderland`,
`youth-waterfowl-sept19`, `bear-gun-sept19-25`, `archery-sept26`, `squirrel-day-2`, `dove-first-segment-day-13`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish`, `black-drum-sheepshead`, `youth-bear-closes-tonight`, `early-goose-closes-5-15-aggregate`, `flounder-day-13-ff-27`,
`gauley-day-3`, `ff-38-commercial`, `stocking-none`, `williams-54-9-flat`, `point-pleasant-25-65-up`, `huntington-27-69-rising-crest-monday`, `mason-flood-warnings-8am`, `ilm-rip-moderate`, `nhc-20pct-central-atlantic`, `moon-1-5-days-springs`, `topsail-fp-sept1-twelve-days`

## 2026-09-14 — No. 41 (Times) and No. 31 (Sports & Sportsman)

| Open-ended | **Twentieth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), launched 5:35, filed between 5:38 and 5:45 a.m. ET. Both papers validated, rendered and pushed at **5:48 a.m. ET** (commit 6c65479), 18 minutes after the 5:30 wake. Digest dry-run 1,081 embed chars, hero attached. Pages served both dated pages 200 at 5:48:52, about 40 seconds after the push. The 6:52 `send_later` wake ran the post in the foreground; `--not-before` held 7 minutes and **the digest landed at 7:00:01 a.m. ET** (message 1549011836068823060, 1,081 embed chars, hero attached, degraded []). **Detached HEAD at session start again — seventeenth occurrence**; `git checkout main && git pull origin main` fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **All three fetchers clean at 5:33** (stats 4 entries, all up; fishing 4 waters 0 errors; standings 5 clubs: Pirates 75-75 third 18.0 back 6.5 out, Reds 70-79 fifth 22.5 back 11.0 out). **The Williams more than tripled overnight**: 189.0 cfs / 2.04 ft at 5:15 against 54.9 / 1.34 Sunday, crest 270 cfs / 2.32 ft at 5:30 p.m. Sunday per the USGS trace, falling 6-8 cfs an hour. Today the fetcher's 24h-ago field happened to equal Sunday's 5:15 reading, so its comparison was right for once; at Point Pleasant (25.58, 24h-ago 24.7 = Saturday) and Huntington (26.94, 24h-ago 26.58 = Saturday) it was the 48-hour artifact again, and both "rising" flags were printed with the trace's direction and a note saying so. **Huntington crested Sunday 9:15 a.m. at 27.91, a foot under the NWS 28.7 forecast; NWPS still carried a 28.6 crest for this afternoon at 8:41 p.m. Sunday.** Point Pleasant forecast revised down to a 25.6 crest | **fetch-fishing-24h-window-bug — still for Nate** |
| Open-ended | **The lead moved to Sweden**: centre-left 176-173 at 94% counted (Euronews primary, Al Jazeera and Irish Times cross-checks); SD share 17.6 v 17.5 dropped, Moderates 19.9 v 19.8 dropped; late ballots from Wednesday, final by end of week. Second choice was the Oman postponement of Monday's Iran-Gulf Salalah meeting (AP via Al Jazeera) — ran as the World Middle East brief instead; Iran's foreign ministry told a ToI liveblog Saudi Arabia asked for the delay (not printed). **Saudi East-West pipeline still shut**, no restart reported (PBS/AP Sept. 12 read). Trump at Doonbeg: "war ends right after the midterms" (ABC via KVIA) — held; his Zelenskyy-diesel remark ran as the Europe brief (Kyiv Independent) | **watch: Sweden final count; the pipeline; Oman new date; FOMC Wednesday 2 p.m. ET** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** Euronews' og:image is a polling-station photo of Andersson between two cardboard voting booths in a school gym with a climbing wall and net behind. Drawn freehand (about 60 paths): two VALSEDLAR booths on folding tables, the wall of slats and net, the voter as a plain contour with no facial detail, caption says "a voter". Rasterized with headless Chromium and looked at. Third rung-1 drawing in a row | |
| Open-ended | **Notebook: 3 statewide, 2 regional (huntington_cabell, putnam_kanawha), away 1, hotspots 2 — five lines.** Statewide: Devine strangulation arrest (WV News; WSAZ corroborates); September interims day 1, water/flood briefings (News and Sentinel); PSC staff v MARL (Gazette-Mail, testimony Sept. 8, labeled). **Cut by the editor: the WV desk refiled CAIR mosque threats (WCHS) — it ran Sept. 12 — and a mid_ohio_valley line that was Sunday's Wood County roads statewide brief verbatim.** Regional: Huntington council votes tonight on the police-tech guardrail ordinance + $1.58M paving (Herald-Dispatch); St. Albans animal cruelty charges (WCHS). **Empty: mid_ohio_valley (dup), nicholas_webster (only a Sept. 10 Carnifex preview; Potato Festival never opened), summers_new_river (Hinton News newest local Aug. 6; WVNS Route 3 item 403).** Away: Bennington drug/gun ring supervisor 12 years, Sept. 8 (Banner); a second away line (Select Board tonight 6, Planning Commission Wed 7) was cut because the validator allows ONE away entry per region — instructions/style.md's "at most two away lines" is stale against the validator. Cabin: Holly River festival Sept. 5-6 (Echo Sept. 8, lede only — Echo bodies are paywalled past the lede). Topsail: Topsail Beach south-end preserve rules, Friday (town site, read this time). **Webster County Commission now meets ONCE a month, third Wednesday 9 a.m. (Echo, May 23) — edition.md §3a's "1st and 3rd Wednesday" is stale; next is Sept. 16.** Alternates: Huntington motorcycle death 2 a.m. Monday (WSAZ, developing); Cabell BOE Tuesday 4:30; Mingo Hope Scholarship suit (Sept. 4, out of window); NextEra MARL delay to May 2027; hens vote SIXTH morning no result | **watch: Devine charge; Huntington council result; Sept. 16 Webster commission; hens** |
| Open-ended | **Canada 2/2/2.** PG: council in-principle support for Bird's inland-port proposal (My PG Now); Chantyman B.C. Medal of Good Citizenship after the 700-km March with Arch (CKPG). Held: Blazers 3-1 Cougars preseason, Active Transportation Plan. BC: two rescued off Tsawwassen (CBC/CP); Alert Bay totem pole down (CHEK). Held: Coast Mountain Bus tentative deal; Fraser sockeye forecast cut 8M to 3M (CHEK). Canada: Carney investment summit $1T target (Global/CP); exports to China +30% H1 (CBC). Held: Carney "unique alliance" not EU membership (CBC); Unifor pauses Stellantis talks (union statement only). **FedEx/Boundary Road: third morning unconfirmed, Citizen 403** | **watch — Carney-Burnham Tuesday, Strasbourg Wednesday; Unifor-Stellantis Sept. 20; sockeye** |
| Open-ended | **Sumo, Aki Day 2 — from Sponichi and Sports Hochi via Yahoo Japan; JSA English page still "information will be posted", Kyodo 404, Japan Times 402, r/Sumo interstitial.** Onosato oshidashi over Kotoshoho; Kirishima yoridaoshi over Hakunofuji; Aonishiki over Takayasu; Kotozakura over Yoshinofuji; Atamifuji over Churanoumi (2-0); Daieisho 0-2 (lost to Gonoyama); Fujinokawa 1-1 (lost to Kotoeiho). Futagodake obit ran (Jiji, died Sept. 10, 82). Held: four recruits pass, maezumo from Day 3 (Jiji). **Day 3 torikumi not published anywhere opened by 5:55.** Note: "2-0"/"0-2"/"1-1" records in sumo briefs trip the score gate — write them in words | **Day 3 results Tuesday; Onosato/Kirishima 3-0?** |
| Open-ended | **Our Teams: 6 briefs.** Bengals 33-27 Bucs (four takeaways, Knight strip-sack TD; CBS box); Jaguars 34-10 Browns (Lawrence 4 TD, Watson 16/22; club recap — CBS slug is CLE@JAC not JAX); Reds 4-3 Brewers (Suarez 24th HR, Pagan 23rd save; CBS box); Pirates 4-3 Cubs (Chandler W, Montgomery 13th save; CBS box); Liverpool v Spurs Carabao Cup preview, straight down the middle (club fixture page); Crew Open Cup semi preview (club). Standings: Chelsea 7 pts FIFTH (was 4th), Liverpool 6 pts SEVENTH (was 6th), Spurs 2 pts 17th (Sky 9:17 p.m. UK Sunday); FCC 32 pts NINTH (was 8th), Crew 23 pts 13th (FOX); Bengals 1-0, Browns 0-1. Sat out: Chelsea, Hannan (SIXTH morning without Westside/Point JV — MaxPreps' Westside page now shows "Date TBA vs Hannan", which suggests Sept. 10 was not played, no source says so), FCC, WVU, Marshall, Ohio, Spurs, USMNT (roster due Sept. 17 for Peru Sept. 26 / Chile Sept. 29). **Tottenham cannot be in sat_out when named in the Liverpool brief — the validator counts find_team matches in brief text as coverage** | **hannan-westside / hannan-point-jv — still owed; Carabao Cup result Wednesday's paper** |
| Open-ended | **Leagues: 12 briefs.** Sumo 3; NFL: Giants 28-20 Cowboys (Harbaugh debut, AP via WSLS), Bears 59-37 Panthers (NFL.com), Vikings 39-22 Packers/Murray concussion (NFL.com); MLB: Yankees 2-0 Mets (magic number 1), Phillies 9-4 Braves (lead 5), Marlins 6-4 Dodgers + Padres sweep — all three from the KNBR/thesportsleader roundup, wire origin unidentified; Zverev d. Shelton 6-3 7-6(2) 5-7 6-2 (CBS); AP Top 25: Texas No. 1, OSU 6th, Oregon 21st, Virginia 25th (AP via KSAT); City 1-0 United, Foden red, Haaland VAR goal (PA via ESPN). Held: Cardinals 3-1 White Sox; Bears-Panthers 96 pts record (unopened); Chiefs MNF tonight. **Direction gate: a summary with three scores in it reads as the named team losing — one score per brief, others in words** | **direction-gate-multi-score — for Nate (fourth wording issue)** |
| Open-ended | **Outdoors: all four waters.** Williams 189/2.04 falling off a 270 crest — "wadeable at the edges and tailouts, not the pockets"; Point Pleasant 25.58 rising since midnight, forecast crest 25.6 today; Huntington 26.94 flat/falling, crest passed; Topsail springs easing, sound 62 min behind the inlet on highs, ILM rip LOW today / MODERATE Tuesday, NHC 0/30% far Atlantic. No WV or NC alerts at 5:36. Seasons: **NC recreational flounder LAST DAY, closes 11:59 p.m. (FF-27), FF-37 commercial opens 12:01 a.m. Tuesday**; early goose closed Sunday (going_out once, drop tomorrow); youth waterfowl + bear gun window Sept. 19 (5 days); archery Sept. 26 (12); regular goose Oct. 3 (19); squirrel Day 3; dove Day 14. **NPS Gauley pages 404 both URLs — release windows are yesterday's read**; MNF alerts moved to fs.usda.gov/r09/monongahela/alerts (FR 86-Williams River closure July 17 seen, FR 76 not found); NCDMF proclamation index 404 at yesterday's address; Corps cert failure; USNO not opened; **trout stocking search not run** (September; silence expected) | **watch — Gauley release page address; FF-27 close; Day 3 sumo; Tuesday rip risk** |
| Open-ended | **Sci/Tech and AI.** O3b mPOWER F FLEW Sunday 2:49 p.m. EDT, 700th Falcon, 400th SLC-40 orbital launch (Spaceflight Now); Vega-C VV30 Sentinel-3C/FLEX tonight 9:21 p.m. EDT (ESA); Sanger pneumococcus serotypes/pollution, Nature Microbiology (EurekAlert); NSF Frontier Initiatives letter, $1B via anonymous staff (Nature, curl). AI: Trump/Johnson/Sacks dismiss Amodei's pace call (NPR); Gartner "not enterprise grade", 86% of CIOs (Register). Held: primordial helium 0.5% (Phys.org, five ApJ papers), Chariklo rings (Space.com), Mammoth Site dating, wildfire smoke birds, **HARMONi-2 oral is Sept. 15 in Seoul (Akeso release; OS 30.8 v 22.6, HR 0.73)**, METR departures (NBC, Sept. 10), Obama AI remarks, Nvidia-Groq | **watch — Vega-C result; HARMONi-2 independent report Tuesday; USSF-259 Sept. 15 9 p.m. EDT** |
| Open-ended | **Source status.** OPEN via curl+Safari UA: Euronews, Al Jazeera, Irish Times, ToI liveblog, CBS SF, Spokesman (Bloomberg copy), Yahoo Finance, Block Club Chicago, KVIA, Kyiv Independent, Malay Mail (AFP), Agencia Brasil, NPR (curl; WebFetch 503), Gazette-Mail, WV News, Herald-Dispatch, WSAZ, WTAP, WCHS, WOAY, News and Sentinel, WV Record, Hinton News, WVVA, Bennington Banner, topsailbeachnc.gov (no www), NTB, Surf City alerts, webconews.com (ledes only), CKPG, My PG Now (curl), CBC (curl), CHEK, Global, Spaceflight Now, ESA, EurekAlert, Phys.org, Nature (curl), Register, TechCrunch, NBC, CBS Sports boxes, clevelandbrowns.com, bengals.com, liverpoolfc.com, columbuscrew.com, Sky table, FOX schedules, MaxPreps, Yahoo Japan (Sponichi/Hochi), Jiji (curl), USGS, NWPS, api.weather.gov, ILM SRF, NHC, NCDMF limits + FF-27, WVDNR migratory PDF. BLOCKED: dw.com, CBC 403 on WebFetch, CNN 451, Lake County News 403, PG Citizen 403, Vancouver Sun, WV MetroNews (front 200 but only HS scores rendered — not retried), benningtonvt.org agenda pages ("page has moved"), WECT site search empty, chelseafc.com news empty, ESPN scoreboards empty, Japan Times 402, Kyodo 404, JSA results pages empty, r/Sumo interstitial, NPS Gauley 404, Corps cert, NCDMF proclamation index 404 | **watch — MetroNews; NPS Gauley address; benningtonvt.org agendas** |
| Open-ended | **Traps dodged.** (1) CAIR mosque threats refiled by the WV desk two days after it ran — cut. (2) Wood County roads (WTAP, Sunday's statewide brief) refiled as a regional line — cut. (3) Second Vermont away line (meetings) — cut for the validator's one-per-region rule. (4) SD 17.6 v 17.5, Moderates 19.9 v 19.8 — dropped. (5) Bears-Panthers "96 points a record" only in a search summary — not printed. (6) FedEx/Boundary Road third morning — not printed. (7) Potato Festival and Carnifex "held" only in snippets — not printed. (8) Yankees/Dodgers clinch claims in search summaries — not printed. (9) Crew "1-0 win May 20" and sumo "2-0" records tripped the score gate — reworded, not the gate. (10) Trump "war ends after the midterms" — single-outlet presidential claim, held | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-14** | **EPA power-plant carbon repeal expected at the G20 energy meeting, Houston (Bloomberg report); Huntington City Council 7:30 p.m. (guardrail ordinance, paving); Bennington Select Board 6 p.m.; Reds v. Dodgers 6:40 (Lodolo v. Skubal); Chiefs MNF; Vega-C VV30 9:21 p.m. EDT; NC flounder closes 11:59 p.m.; Canada Investment Summit Toronto (14-15); Iraola presser 7 a.m. ET** | |
| **2026-09-15** | **Aki Day 3 (maezumo begins); Liverpool v. Tottenham, Carabao Cup, 3 p.m. ET (house derby); Hannan v. Parkersburg Catholic 6 p.m. Ashton; Cabell BOE 4:30; FOMC opens; HARMONi-2 oral, Seoul; Carney-Burnham Liverpool; USSF-259 Vandenberg 9 p.m. EDT; FF-37 commercial flounder opens 12:01 a.m.; Pirates v. Brewers, Reds v. Dodgers 6:40; ILM rip MODERATE** | |
| **2026-09-16** | **FOMC decision 2 p.m. ET, Warsh 2:30; Sweden late ballots counted; Crew v. Orlando City Open Cup semi 7 p.m.; Webster County Commission 9 a.m. (monthly, third Wednesday); North Bennington Planning Commission 7 p.m.; Carney at the European Parliament; Reds v. Dodgers, Pirates v. Brewers 6:40** | |
| **2026-09-17** | **USMNT roster (Peru Sept. 26, Chile Sept. 29); Gauley Fest opens 8 a.m. Summersville; Hannan at Westside 6 p.m. Beckley YMCA; Pirates v. Brewers 12:35, Reds v. Dodgers 12:40 (Singer v. Snell)** | |
| **2026-09-18** | **Sweden final result expected by end of week; PG/Quesnel withdrawal deadline; Chelsea at Brentford 3 p.m. ET; Reds v. Cubs (Burns v. Holmes), Pirates v. Royals (Skenes v. Dobnak) 6:40; Gauley releases 18-21** | |
| **2026-09-19** | **U.S. 7 closure Bennington-Arlington begins (to Oct. 3); WV youth waterfowl day; WV bear gun second window (19-25, selected counties); Spurs v. Villa 7:30 a.m. ET; Marshall at Missouri State 6:30, Ohio at South Alabama 7, WVU v. No. 25 Virginia in Charlotte 7:30; Crew at Montreal 7:30, FCC at Houston 8:30** | |
| **2026-09-20** | **Bournemouth v. Liverpool 9 a.m. ET; NFL Week 2: Bengals at Houston, Browns at Tampa Bay, 1 p.m.; Pirates v. Royals 1:35, Reds v. Cubs 1:40; Unifor-Stellantis contract expires 11:59 p.m.; Macron in Saint-Pierre-et-Miquelon** | |
| **2026-09-22** | **NTB public hearing on the USACE New River Inlet draft EIS, 6 p.m.; Hannan at Calvary 6 p.m. (venue unconfirmed)** | |
| **2026-09-24** | **Trump-Xi summit; Hannan v. Roane 6 p.m. Ashton** | |
| **2026-09-26** | **WV archery/crossbow deer and bear open; USMNT v. Peru** | |
| **2026-09-28** | **Toronto conference on abducted Ukrainian children (28-29)** | |
| **2026-09-29** | **USMNT v. Chile, St. Louis, 8 p.m. ET; Hannan at Roane 6:30** | |
| **2026-10-01** | **Pumpkin Festival, Milton (1-4); Cabell County Clerk Caserta retires** | |
| **2026-10-03** | **WV regular goose (to Oct. 18) and duck (to Oct. 11) seasons open; U.S. 7 closure ends** | |
| **2026-10-11** | **WV dove first segment closes** | |
| **2026-10-14** | **Topsail Beach board's next regular meeting (hens minutes?)** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18)** | |
| **2026-10-19** | **Alberta referendum; USACE draft EIS comment deadline** | |
| **2026-10-21** | **U.S. Open Cup final (Crew or Orlando host, v. Colorado or St. Louis)** | |
| **2026-11-02** | **Primrose Medical Centre opens, Qualicum Beach** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |
| **2027-05-22** | **PSC decision date on MARL if NextEra's delay is granted (hearings Jan. 11-18)** | |

### Open threads

- **sweden-centre-left-176-173** — led; follow-ups are the late-ballot count from Wednesday, the final result, Andersson's coalition. **oman-postpones-salalah / hormuz-ship-strike (Sunday's lead) / saudi-pipeline-still-shut / trump-midterms-war-remark** — alternates and the Middle East thread.
- **epa-carbon-repeal-bloomberg / fed-hike-odds-80 / lucas-fire-25pct / humboldt-park-shooting** — ran. **trump-campaign-return (NPR 503) / puerto-rico-fomb (Sept. 2)** — alternates. FOMC Wednesday is the U.S. peg.
- **indonesia-ferry-129-missing / trump-zelenskyy-diesel / tooro-king-burial / oman-postpones** — ran. **syria-fuel-protests / sao-paulo-collapse-7 / niger-army-chief / lower-saxony-cdu (no readable outlet) / brics-declaration (no readable outlet)** — alternates.
- **devine-strangulation / interims-water-flood / psc-staff-marl** — ran. **cair-mosque-threats (ran Sept. 12; refiled, cut) / mingo-hope-suit / nextera-marl-delay / harrison-cage-abuse / doj-voter-data-appeal** — alternates. **huntington-council-guardrail / st-albans-animal-cruelty** — regional. **bennington-drug-ring-12-years** — away. **holly-river-festival / topsail-beach-south-end-rules** — hotspots. **huntington-motorcycle-death / cabell-boe-tuesday / bennington-meetings-week / cvfd-softball (undated) / webster-commission-monthly / carnifex-held? / topsail-hens (sixth morning)** — alternates.
- **pg-inland-port / chantyman-medal / tsawwassen-rescue / alert-bay-totem / carney-summit-1t / exports-china-30pct** — ran. **blazers-cougars / active-transportation-plan / coast-mountain-bus / fraser-sockeye-3m / carney-eu-alliance / unifor-stellantis-pause / fedex-boundary-road (third morning)** — alternates.
- **o3b-mpower-flew / vega-c-tonight / pneumococcus-serotypes / nsf-frontier-letter** — ran. **helium-0-5pct / chariklo-rings / mammoth-site / smoke-birds / harmoni-2-sept-15** — alternates.
- **trump-dismisses-amodei / gartner-not-enterprise-grade** — ran. **metr-departures / obama-ai / register-capture-column / nvidia-groq** — alternates.
- **bengals-33-27 / jaguars-34-10-browns / reds-4-3-brewers / pirates-4-3-cubs / liverpool-spurs-preview / crew-open-cup-preview** — ran. **chelsea / hannan / fcc / wvu / marshall / ohio / spurs-nba / usmnt** — sat out. **hannan-westside / hannan-point-jv** — still owed.
- **aki-day2-onosato-kirishima / aki-day2-atamifuji / futagodake-dies / giants-28-20 / bears-59-37 / vikings-39-22-murray / yankees-2-0 / phillies-9-4 / marlins-6-4-padres / zverev-title / ap-top25-texas / city-1-0-united** — ran. **recruits-maezumo / cardinals-3-1 / bears-panthers-record / chiefs-mnf** — held.
- **youth-waterfowl-sept19 / bear-gun-sept19 / archery-sept26 / regular-goose-oct3 / squirrel-day-3 / dove-day-14 / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead / flounder-LAST-DAY / early-goose-closed** — ran. **gauley-last-day-window-1 (NPS 404) / fr86-williams / stocking-not-searched** — seasons note. **williams-189-falling-270-crest / point-pleasant-25-58 / huntington-26-94-crest-passed / ilm-rip-low-then-moderate / nhc-30pct / moon-2-5-days** — water block.
- **sportsman-index-stale-no-12** — for Nate (No. 31 computed from the edition files). **fetch-fishing-24h-window-bug** — for Nate. **direction-gate-multi-score / direction-gate-record-regex (sumo 2-0)** — for Nate. **style-md-two-away-lines-vs-validator-one** — for Nate: style.md says at most two away lines, the validator refuses a second `vermont` entry. **edition-md-webster-commission-schedule** — for Nate: monthly, third Wednesday. **detached-head-seventeenth** — recurring.

### Covered slugs, 2026-09-14

`sweden-centre-left-176-173-andersson`, `epa-carbon-repeal-bloomberg-g20-houston`, `fed-hike-odds-80pct-wednesday`, `lucas-fire-4109-25pct`, `humboldt-park-shooting-1-6`,
`oman-postpones-salalah-hormuz-talks`, `indonesia-ferry-129-missing-6-dead`, `trump-zelenskyy-stop-diesel-strikes`, `tooro-king-oyo-burial-succession`,
`wvu-devine-strangulation-arrest`, `september-interims-water-1b-flood`, `psc-staff-marl-no-benefit`,
`huntington-council-guardrail-paving-1-58m`, `st-albans-animal-cruelty-dogs`, `bennington-drug-gun-ring-12-years`, `holly-river-festival-sept-5-6`, `topsail-beach-south-end-preserve-rules`,
`pg-council-inland-port-bird`, `chantyman-medal-march-with-arch`, `tsawwassen-fishing-vessel-2-rescued`, `alert-bay-totem-pole-down`, `carney-investment-summit-1t`, `canada-china-exports-30pct-h1`,
`spacex-700th-falcon-o3b-mpower-complete`, `vega-c-sentinel-3c-flex-tonight`, `sanger-pneumococcus-serotypes-pollution`, `nsf-frontier-initiatives-letter-1b`,
`trump-johnson-dismiss-ai-slowdown`, `gartner-ai-vendors-not-enterprise-grade`,
`bengals-33-27-bucs-four-takeaways`, `jaguars-34-10-browns-monken-debut`, `reds-4-3-brewers-suarez-24`, `pirates-4-3-cubs-chandler`, `liverpool-tottenham-carabao-preview`, `crew-orlando-open-cup-semi-preview`,
`aki-day2-onosato-kirishima-unbeaten`, `aki-day2-atamifuji-daieisho-0-2`, `futagodake-dies-82`, `giants-28-20-cowboys-harbaugh-dart`, `bears-59-37-panthers-williams`, `vikings-39-22-packers-murray-concussion`, `yankees-2-0-mets-magic-1`, `phillies-9-4-braves-lead-5`, `marlins-6-4-dodgers-padres-sweep`, `zverev-us-open-title-shelton`, `ap-top25-texas-no1-osu-6-oregon-21`, `man-city-1-0-united-haaland-foden-red`,
`youth-waterfowl-sept19`, `bear-gun-sept19-25`, `archery-sept26`, `regular-goose-oct3-splits`, `squirrel-day-3`, `dove-day-14-rails-snipe`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish`, `black-drum-sheepshead`, `flounder-last-day-ff-27`, `early-goose-closed-sunday`,
`gauley-window-1-last-day-nps-404`, `fr86-williams-closure`, `williams-189-falling-270-crest`, `point-pleasant-25-58-rising-since-midnight`, `huntington-26-94-crest-passed-27-91`, `no-wv-nc-alerts`, `ilm-rip-low-moderate-tuesday`, `nhc-30pct-east-of-bermuda`, `moon-2-5-days-springs-easing`, `topsail-fp-sept1-thirteen-days`

## 2026-09-15 — No. 42 (Times) and No. 32 (Sports & Sportsman)

| Open-ended | **Twenty-first morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), launched 5:37, filed between 5:41 and 5:47 a.m. ET. The Times validated, rendered and pushed at **5:46 a.m. ET** (commit 10080fa); Sports & Sportsman at **5:48 a.m. ET** (commit 8ac1500), 18 minutes after the 5:30 wake. Digest dry-run 1,058 embed chars, hero attached (80 KB). Pages served the Times page 200 at 5:48:43 and the sportsman page 200 at 5:49:15, about 45 seconds after its push. The 6:52 `send_later` wake ran the post in the foreground; `--not-before` held 7 minutes and **the digest landed at 7:00:01 a.m. ET** (message 1549374222370086974, 1058 embed chars, hero attached, degraded []). **Detached HEAD at session start again — eighteenth occurrence**; `git checkout main && git pull origin main` fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **Setup: `pip install -r requirements.txt` timed out TWICE on files.pythonhosted.org (Pillow), succeeded on a third try with `--timeout 60`; requests was already present.** Not a source outage, a PyPI read timeout — say so if the hero ever fails on a morning pip gives up. **USGS was 503 on Williams and Huntington at the 5:33 fetch** (Point Pleasant and NOAA answered); `fetch_fishing.py` re-ran clean at 5:37, 4 waters, 0 errors, and nothing was written from the first run. Stats 4 entries (all four down: S&P 7,619.98 -0.48%, Dow 52,421.20 -0.29%, Nasdaq 26,186.41 -0.56%, Bitcoin $76,882 -1.23%); standings 5 clubs (Pirates 75-75 third, 18.0 back, 7.0 out; Reds 70-80 fifth, 23.0 back, 12.0 out) | **fetch-fishing-24h-window-bug — still for Nate** (all three USGS 24h-ago fields were Sunday 5:45 a.m. again) |
| Open-ended | **The lead is the Supreme Court's Monday-night order blocking the Postal Service mail-ballot rules for the midterms** — the movement on the "USPS mail-ballot appeals" thread. NBC primary; CBS, Al Jazeera, AP via PBS and Votebeat cross-checks, all opened. Dropped on disagreement: the vote split (NBC "appeared 7-2", CBS "not disclosed" — body says Alito and Thomas dissented), Talwani's first-block month (June v August — "late August"). Second choice was NATO's first drone shootdown over Lithuania (Euronews + Kyiv Independent) — ran as the Europe brief. **Sweden: no movement, still 176-173, late ballots from Wednesday, Bloomberg headline says final result Thursday** — not printed. EPA's power-plant repeal was FINALIZED Monday in Houston (NBC + EPA release) — ran as the first U.S. brief | **watch: Sweden final Thursday; FOMC Wednesday 2 p.m. ET; CLARITY Act cloture Tuesday 2:15 p.m.; Saudi-Houthi escalation** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** NBC's og:image is a close-up of hands fanning purple "Return Envelope" mail ballots — hands, which the ladder says to avoid — so the drawing is after CBS's og:image instead (a video still of an official ballot drop box from below, flag stripes on its face, a hand feeding an envelope into the slot; credit "Sketched from a CBS News photograph"). Drawn freehand (55 paths): the box as a tall trapezoid, a star canton, six sweeping stripe bands with hatching, the stainless slot hood, the envelope halfway in, the hand and sleeve as a plain contour, OFFICIAL in block capitals cropped by the frame. Rasterized with headless Chromium and looked at twice; lettering shrunk and the hand simplified on the second pass. Fourth rung-1 drawing in a row | |
| Open-ended | **Notebook: 4 statewide, 3 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley), away 1, hotspots 2 — six lines.** Statewide: Huntington council passes the Flock guardrail ordinance 7-2, seven-day retention, $2.1M contract unsigned (WSAZ, Sept. 15 — the Monday-night RESULT; the $1.58M paving vote result was in no opened story); Morrisey's major-disaster request for Fayette, Harrison, Kanawha, sent Sunday, 600+ homes, 22 destroyed (WCHS); Raylee's Law compromise at Monday interims (Dominion Post); Underwood Smith scholarship, 42 graduates, 82% high-needs (WVPB). Regional: Kroger Marketplace deal at 5th Ave and 24th St, told to council Monday night (WSAZ); I-64 Fort Hill Bridge overnight lane and ramp closures 8 p.m.-6 a.m. (WCHS — WSAZ and WCHS disagree on the exact nights, so "overnight this week"); Wood County five $75K site-readiness grants + PowerFlo 120 jobs at the old Hino plant (WTAP). **Empty: nicholas_webster (Echo's Sept. 14 batch covers Sept. 5-12; Nicholas Chronicle front still May; Gauley Fest is Thursday — preview), summers_new_river (Hinton News Sept. 14 items are statewide reprints; Register-Herald and WOAY nothing Sept. 13-15).** Away: Lake Paran 13th stone-skipping festival Saturday Sept. 19, 1-7 p.m. (Banner, Sept. 12). Cabin: Red Oak Fire Tower on Bishop Knob, between Cowen and Richwood, open for overnight stays (Echo, Sept. 14, lede). Topsail: Surf City e-bike / multi-use path focus group Sept. 28, 6-8 p.m., Hampstead (WECT, Sept. 14). Held: Devine not-guilty plea + Sept. 23 prelim (Sept. 13 reporting, not new); Marquee Cinemas closing (WSAZ 404 both ways, nowhere else); Mason County flood damage assessment; Wayside Farms Road collapse; Bennington cruiser hit Thursday night; Beech Street closed this week; EDA offer on 50+ acres at Big Ditch Lake; Bergoo UTV deaths (Echo lede says "Saturday evening" but the release dates it Sept. 5 — trap); NTB website relaunch Sept. 16; hens vote SEVENTH morning no result. **The Webster Echo answers again (200, ledes only)** | **watch: Devine prelim Sept. 23; Webster commission Wed 9 a.m. (no agenda posted); FEMA answer on the disaster request; Kroger timeline; hens** |
| Open-ended | **Canada 2/2/2.** PG: Major Crime Unit probes the death of a 77-year-old in Fort St. James, BC Spruce Road, 2:40 a.m. Monday, "targeted" (CKPG; My PG Now and CBC agree); Osisko approves the full Cariboo gold mine build near Wells, 30 months, first pour early 2029, 613 peak / 525 permanent (My PG Now — outlet says "Osisko Gold", tags say Osisko Development, so "Osisko" alone). BC: deficit forecast up $450M to $13.8B, wildfire $614M over (CHEK; CBC "nearly half-billion" consistent; $306M royalty-error figure dropped, CBC frames it as $1.5B/$800M over five years); seventh MLA (Donegal Wilson) joins Milobar's unnamed party (CBC/CP). Canada: new U.S. 50% tariffs on 110 goods in effect after midnight Tuesday, 10 items lifted (CBC); Alberta NDP takes Calgary-Shaw by 582 (CBC; CP "more than 500"). Held: McLeod Lake community forest offer; Cumberland guilty plea; TD $150B / Bell $52B summit pledges; inflation held at 3% in August (StatCan); Cougars 0-for preseason, Peyton Shore trade, opener Friday v Penticton; Quebec leaders' debate 8 p.m. ET tonight. **FedEx/Boundary Road: FOURTH morning, no readable outlet — not printed** | **watch — Strasbourg Wednesday; Unifor-Stellantis Sept. 20; Cougars opener Friday; FSJ homicide** |
| Open-ended | **Sumo, Aki Day 3 — Kyodo, Sponichi and Sports Hochi via Yahoo Japan, Nikkan Sports direct; JSA results pages still "information will be posted" in both languages; NHK behind a consent wall.** Three-and-oh: Onosato (oshidashi over Kotoeimine), Aonishiki (over Kotoshoho), Kotozakura (hatakikomi over Daieisho). **Kirishima's yokozuna run took its first loss — hikiotoshi by East M2 Takayasu, 36. Atamifuji's ozeki run took its first loss — tsukiotoshi by Takanosho.** Fujinokawa two-and-one; Hakunofuji and Daieisho winless. No kinboshi, no new top-division kyujo (JSA absence page at /ResultData/absence/ works). Maezumo began (18-year-old Hawaii-raised debutant, held). **Day 4 (Nikkan): Onosato v Takayasu, Kirishima v Kotoeimine, Aonishiki v Hakunofuji, Fujinokawa v Kotoshoho, Atamifuji v Fujiryoga.** Records written in words throughout; no `result` on sumo briefs | **Day 4 results Wednesday; three leaders — who falls first?** |
| Open-ended | **Our Teams: 5 briefs.** Liverpool-Tottenham Carabao Cup team news, straight down the middle (club team-news page; De Zerbi presser page confirms Tonali, Porro, Kulusevski, Richarlison out, Udogie back); Taylor's "pretty clean" Monday update (Cincy Jungle — read via Yahoo syndication, cincyjungle.com 403); **Dodgers 4-1 Reds** (CBS box: Skubal 7 IP 0 R 9 K, Lodolo 4 R in 7, Tucker/Hernandez HR, De La Cruz solo in the 9th; LA clinches a 14th straight postseason); Monken keeps Watson as starter, Sampson knee (club News & Notes); Rodriguez says Strachan could debut v Virginia (SI). Standings: Chelsea 7 pts SIXTH (was 5th), Liverpool 6 pts EIGHTH (was 7th), Spurs 2 pts 17th (Sky, read Sept. 15); FCC 32 pts ninth, Crew 23 pts 13th (FOX); Bengals 1-0, Browns 0-1; WVU 2-0 unranked (Virginia No. 25); Marshall 1-1; Ohio 1-1; Hannan 1-1 per MaxPreps. Sat out: Chelsea, Hannan (SEVENTH morning without Westside/Point JV — Westside's MaxPreps page lists both Hannan matches unplayed; Point Pleasant's varsity page has no Hannan match; Register 503 twice; MetroNews 403 even with a Safari UA), Crew, FCC, Marshall, Ohio, Pirates (off Monday), Spurs (no camp dates found), USMNT (roster due Sept. 17). **Pirates probables changed: Bachar Tue, Jones v Henderson Wed, May Thu, Wacha Sun** | **hannan-westside / hannan-point-jv — still owed; Carabao Cup result + Hannan v Parkersburg Catholic tonight for Wednesday's paper** |
| Open-ended | **Leagues: 12 briefs.** Sumo 3; NFL: Chiefs 31-10 Broncos MNF (Walker 23 for 173, Mahomes 15 of 27; CBS box, ESPN line score confirms), Murray in concussion protocol day-to-day (AP via MPR); MLB: Yankees clinch with 8-3 at Minnesota, sealed by Detroit over Toronto (CBS box) — **first draft "Yankees clinch ... as Toronto loses" tripped the direction gate; reworded to "Yankees beat the Twins 8-3 ... and clinch" and "by Detroit's win over Toronto"**; Dodgers 14th straight, tying Atlanta 1991-2005 (MLB.com, Reds score left to Our Teams); Cubs 7-3 Braves, Crow-Armstrong 42nd, half-game over idle Phillies for top WC, Padres 2.5 up, White Sox 1.5 up (CBS box + MLB standings 12:58 a.m.); PL: Leeds 4-1 Newcastle, third (NBC); Arsenal at Ipswich Carabao Cup 3 p.m. ET (Arsenal.com); CFB: FSU fires AD Alford, Warwick interim (ESPN); NBA: Kawhi to Toronto completed, $30M fine, Ballmer one year, five firsts (AP via ClickOrlando). Held: other cup ties (fan site only), Lawrence Frank six-month suspension (Hoops Rumors only), maezumo debutant | **direction-gate — the word "loses" in a headline about the OTHER team reads as the named team losing** |
| Open-ended | **Outdoors: all four waters.** Williams 106.0 cfs / 1.67 ft FALLING off the 270 crest (Sunday 5:30 p.m.), 189 Monday 5 a.m., 106 from 4:45 to 5:15 today, ~3 cfs/hr; fetcher "rising" is the 48-hour artifact (its 56.2/1.35 is Sunday 5:45 a.m.) — noted, trace direction printed; no gauge temperature. Point Pleasant 25.76 STEADY (flag agrees), NWS 25.6 by 8 a.m., 24.6 Saturday. **Huntington 28.28 — the second rise DID arrive: 26.85 at 12:30 a.m. Monday, crest 28.50 at 6:30 p.m. Monday (within a tenth of the NWS 28.6, later than "afternoon"), 28.16-28.28 from 3 to 5 a.m., easing; NWS 28.2 by 2 p.m., 26.4 Wednesday morning.** Topsail: all four sound events with the "(Mon)" tag, surf table, 83.5F Beaufort, moon 14% / 3.5 days (springs easing toward first quarter; "neap" not used); sound flood 5:50-12:05, ebb 12:05-6:31, lag 67 min on the high; **Beach Hazards Statement Coastal Pender 6 a.m.-8 p.m., ILM rip MODERATE, surf 2-4, NE 15 g 21, strong N-to-S longshore current** (Coastal Flood Advisory noon-3 is New Hanover, not Pender); NHC 0%/40% well ESE of Bermuda. No WV alert. Seasons: youth waterfowl + bear gun Sept. 19 (4 days); archery Sept. 26 (11); regular goose Oct. 3 (18); squirrel Day 4; dove Day 15, 26 left; **NC recreational flounder CLOSED as of 12:01 a.m., ran once as going_out — drop tomorrow**; FF-37 commercial clause sourced to the NCDMF July 16 release (FF-37 itself could not be opened); early goose dropped. **NPS Gauley page ANSWERS at nps.gov/gari/planyourvisit/whitewater.htm (updated Aug. 26): Sept. 11-14, 18-21, 25-28, Oct. 2-5, 9-12, 17-18** — yesterday's 404 was a different address, still 404. Gauley Fest confirmed on the AW event page, Sept. 17 8 a.m. to Sept. 20 noon. **WVDNR migratory bird PDF answered 200 over HTTPS with no cert failure.** Stocking search silent. WV reference file valid through 2027-06-30 | **watch — second Gauley window Friday; Huntington fall to 26.4 Wed; flounder line drops; Tuesday rip** |
| Open-ended | **Sci/Tech and AI.** Vega-C VV30 FLEW 9:21 p.m. EDT Monday, both satellites deployed, signals acquired (Spaceflight Now; ESA release N° 50-2026); ATLAS Z-boson-pair entanglement, PRL (EurekAlert/Oxford); UCSF 253-electrode speech+gesture BCI, two participants, Nature Neuroscience (Nature news — a wire summary said three; Nature's text says two); Yunnan underwater perovskite cell, 35%, 99.6% after 40 days, Joule (Ars). AI: UK JCHR calls for an AI bill and single regulator (Register); Trump calls the slowdown push a "hoax" on speaker with Huang at All-In (TechCrunch — movement on Monday's brief); AbbVie/Astex fine-tune OpenFold3 on 20,167 proprietary structures, blog post not peer-reviewed (Nature). Held: Flinders pre-1788 population 2.22M (Nature Human Behaviour — EurekAlert, strong swap); Meink confirms weapons in orbit; **HARMONi-2 was presented Sept. 13, not 15** (IASLC; OS 30.8 v 22.6, HR 0.73, sponsor data); USSF-259 tonight 9 p.m.-1 a.m. ET (KEYT); UCSD Marines anti-NMDAR1; Microsoft model conduct code; Chen Yixin AI article + CAC framework; iLands Mastodon agent spam; Musk drops Apple, keeps OpenAI | **watch — USSF-259 result; Flinders paper; FOMC** |
| Open-ended | **Source status.** OPEN: NBC, CBS, Al Jazeera, PBS, Votebeat, Erie News Now, Euronews, France24, Malay Mail (AFP), Kyiv Independent, Philstar, Nikkei Asia, Agencia Brasil, ToI liveblog, WSAZ, WCHS (+ Network), Dominion Post, WVPB, WTAP, News and Sentinel, Herald-Dispatch, Hinton News, Register-Herald, governor.wv.gov, legislature blog, Bennington Banner, VTDigger, NTB news, Surf City civicalerts, topsailbeachnc.gov, WECT, **The Webster Echo (200, ledes)**, webstercounty.wv.gov, CKPG, My PG Now, CBC (curl), CHEK, Spaceflight Now, ESA, EurekAlert, Nature, Ars, Register, TechCrunch, CBS boxes, ESPN box (curl), MLB.com, liverpoolfc.com, tottenhamhotspur.com, clevelandbrowns.com, Sky table, FOX schedules, MaxPreps, SI/WVU, Yahoo Japan (Kyodo/Sponichi/Hochi), Nikkan Sports, JSA absence page, Arsenal.com, NBC Sports, ESPN (FSU), AP via MPR/ClickOrlando, USGS (after 5:37), NWPS, api.weather.gov, ILM SRF, NHC, NCDMF limits, **NPS whitewater.htm**, **WVDNR migratory PDF (200)**, AW Gauley Fest event page. BLOCKED: NPR (WebFetch 503, curl chrome only), Politico, abc27, pa.gov newsroom, NHK World + NHK sumo (consent wall), Al Jazeera liveblog bodies, WV MetroNews (Cloudflare, fourth morning), WV News (refused), WOWK/WVNS, WV Watch article pages, NTB /meetings 403, Nicholas Chronicle (stale), PG Citizen, Vancouver Sun, science.org, Phys.org (today), cincyjungle.com, mydailyregister.com (503/TLS), wvusports/ohiobobcats, Herdzone, chelseafc.com, Sky fixture pages 404, EFL fixtures (JS), Japan Times, JSA results pages, Corps Huntington (cert), NCDMF proclamation index (only five 2026 rows), FF-37, AW gauleyfest article | **watch — MetroNews; Webster Echo staying up; FF-37** |
| Open-ended | **Traps dodged.** (1) NBC's lead photo was hands — drawn after CBS's drop-box still instead. (2) Yankees "as Toronto loses" headline tripped the direction gate — reworded, not the gate. (3) SCOTUS vote split 7-2 v undisclosed — dropped. (4) Pentagon IG aircraft counts (7 v 12 KC-135) — dropped. (5) Visa rule effective date Sept. 15 v 16 — "this week". (6) EPA "signed" only in a snippet — "announced". (7) Bergoo UTV "Saturday evening" lede v Sept. 5 release date — not printed. (8) Devine plea traced to Sept. 13 — not refiled. (9) Osisko Gold v Osisko Development — "Osisko". (10) BC $306M royalty error v CBC's five-year framing — dropped. (11) BCI three v two participants — Nature's two. (12) HARMONi-2 date Sept. 13 v 15 — held. (13) FedEx/Boundary Road fourth morning — not printed. (14) Coast Mountain Bus deal Sept. 12/13 — out of window. (15) Fort Hill Bridge nights disagree — "overnight this week" | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-15** | **Aki Day 3 (ran); Liverpool v. Tottenham Carabao Cup 3 p.m. ET (house derby) and Arsenal at Ipswich 3 p.m.; Hannan v. Parkersburg Catholic 6 p.m. Ashton; Cabell BOE 4:30; CLARITY Act cloture 2:15 p.m. ET; FOMC opens; Quebec leaders' debate 8 p.m. ET; USSF-259 Vandenberg 9 p.m.-1 a.m. ET; Reds v. Dodgers (Lowder v. Yamamoto), Pirates v. Brewers (Bachar v. Misiorowski) 6:40; ILM rip MODERATE, Beach Hazards to 8 p.m.; new U.S. 50% tariffs on 110 Canadian goods in effect** | |
| **2026-09-16** | **FOMC decision 2 p.m. ET; Aki Day 4 (Onosato v. Takayasu, Kirishima v. Kotoeimine); Sweden late ballots counted; Crew v. Orlando City Open Cup semi 7 p.m.; Webster County Commission 9 a.m. (no agenda posted); North Bennington Planning Commission 7 p.m.; Carney at the European Parliament; NTB website relaunch; Rwanda-DRC Geneva talks (16-17); Reds v. Dodgers (Abbott), Pirates v. Brewers (Jones v. Henderson) 6:40; Huntington forecast 26.4 ft by morning** | |
| **2026-09-17** | **USMNT roster; Gauley Fest opens 8 a.m. Summersville (to noon Sept. 20); Hannan at Westside 6 p.m. Beckley YMCA; Pirates v. Brewers 12:35 (May), Reds v. Dodgers 12:40 (Singer v. Snell)** | |
| **2026-09-18** | **Sweden final result (Bloomberg: Thursday, i.e. 17th, or by end of week); second Gauley release window opens (18-21, NPS page confirmed); PG/Quesnel withdrawal deadline; Chelsea at Brentford 3 p.m. ET; Reds v. Cubs (Burns v. Holmes), Pirates v. Royals (Skenes v. Dobnak) 6:40; Cougars season opener v. Penticton, CN Centre** | |
| **2026-09-19** | **Lake Paran stone-skipping festival 1-7 p.m., North Bennington; U.S. 7 closure Bennington-Arlington begins (to Oct. 3); WV youth waterfowl day; WV bear gun second window (19-25, selected counties); Spurs v. Villa 7:30 a.m. ET; Marshall at Missouri State 6:30, Ohio at South Alabama 7, WVU v. No. 25 Virginia in Charlotte 7:30; Crew at Montreal 7:30, FCC at Houston 8:30; Reds v. Cubs (Lodolo v. Boyd), Pirates v. Royals (Chandler v. Cameron) 6:40** | |
| **2026-09-20** | **Bournemouth v. Liverpool 9 a.m. ET; NFL Week 2: Bengals at Houston, Browns at Tampa Bay, 1 p.m.; Pirates v. Royals 1:35 (Wacha), Reds v. Cubs 1:40 (Lowder v. Peterson); Unifor-Stellantis contract expires 11:59 p.m.; Gauley Fest closes noon** | |
| **2026-09-22** | **NTB public hearing on the USACE New River Inlet draft EIS, 6 p.m.; Hannan at Calvary 6 p.m. (venue unconfirmed)** | |
| **2026-09-23** | **Devine preliminary hearing (per Sept. 13 reporting)** | |
| **2026-09-24** | **Trump-Xi summit; Hannan v. Roane 6 p.m. Ashton; Calgary-Shaw official results** | |
| **2026-09-26** | **WV archery/crossbow deer and bear open; USMNT v. Peru** | |
| **2026-09-28** | **Surf City e-bike / multi-use path focus group 6-8 p.m., Hampstead; Toronto conference on abducted Ukrainian children (28-29)** | |
| **2026-09-29** | **USMNT v. Chile, St. Louis, 8 p.m. ET; Hannan at Roane 6:30** | |
| **2026-10-01** | **Pumpkin Festival, Milton (1-4); Cabell County Clerk Caserta retires** | |
| **2026-10-03** | **WV regular goose (to Oct. 18) and duck (to Oct. 11) seasons open; U.S. 7 closure ends** | |
| **2026-10-11** | **WV dove first segment closes** | |
| **2026-10-14** | **Topsail Beach board's next regular meeting (hens minutes?)** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18)** | |
| **2026-10-19** | **Alberta referendum; USACE draft EIS comment deadline** | |
| **2026-10-21** | **U.S. Open Cup final (Crew or Orlando host, v. Colorado or St. Louis)** | |
| **2026-11-02** | **Primrose Medical Centre opens, Qualicum Beach** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |
| **2027-05-22** | **PSC decision date on MARL if NextEra's delay is granted (hearings Jan. 11-18)** | |

### Open threads

- **scotus-blocks-usps-mail-ballot-rules** — led; follow-ups are the Talwani and D.C. cases on the merits, any USPS response, state implementation. **nato-lithuania-drone-shootdown / saudi-strikes-yemen-13-wounded / sweden-176-173 (no movement; Thursday) / houthi-hanish-islands / kyiv-drone-1-dead** — Europe/Middle East threads.
- **epa-carbon-repeal-finalized / pentagon-ig-iran-war-33-4b / saylor-blocks-visa-cap / pa-measles-693** — ran. **mcconnell-return / vance-870k-ppp-borrowers / brickell-drill-rig-collapse / kennedy-center-fiscal-collapse / clarity-act-cloture** — alternates. FOMC Wednesday is the U.S. peg.
- **dangote-1-6b-ipo / venezuela-g20-houston / prabowo-fires-purbaya (cut for four) / ukraine-dismisses-kravchenko / barmm-first-vote / rwanda-drc-geneva / russian-frigate-flares-danish-helicopter / rezaei-rejects-talks** — alternates.
- **huntington-flock-guardrails-7-2 / morrisey-disaster-request-3-counties / raylees-law-compromise / underwood-smith-42** — ran. **morrisey-epa-statement / devine-plea-sept-23 / marquee-cinemas-404 / mingo-hope-suit / nextera-marl-delay** — alternates. **kroger-marketplace-huntington / i-64-fort-hill-closures / wood-county-site-grants-powerflo** — regional. **lake-paran-stone-skipping-sept-19** — away. **red-oak-fire-tower-stays / surf-city-ebike-focus-group-sept-28** — hotspots. **mason-flood-damage-assessment / wayside-farms-road / bennington-cruiser-hit / beech-street-closed / big-ditch-lake-eda / bergoo-utv-sept-5 / ntb-website-sept-16 / topsail-hens (seventh morning) / webster-commission-wed** — alternates.
- **fsj-homicide-77 / osisko-cariboo-full-build / bc-deficit-13-8b / seventh-mla-milobar / us-tariffs-110-goods / calgary-shaw-ndp-582** — ran. **mcleod-lake-forest / cumberland-guilty-plea / summit-td-bell-pledges / inflation-3pct-august / cougars-shore-trade-opener-friday / quebec-debate / fedex-boundary-road (fourth morning)** — alternates.
- **vega-c-vv30-flew / atlas-z-entanglement / ucsf-bci-speech-gesture / underwater-perovskite** — ran. **flinders-2-22m / meink-orbital-weapons / harmoni-2-sept-13 / ussf-259-tonight / ucsd-marines-nmdar1** — alternates.
- **uk-jchr-ai-bill / trump-hoax-huang-all-in / openfold3-proprietary-data** — ran. **microsoft-model-conduct / chen-yixin-cac / ilands-mastodon-spam / musk-drops-apple** — alternates.
- **liverpool-spurs-team-news / taylor-pretty-clean / dodgers-4-1-reds-clinch / monken-keeps-watson / strachan-could-debut** — ran. **chelsea / hannan / crew / fcc / marshall / ohio / pirates-off / spurs-nba / usmnt** — sat out. **hannan-westside / hannan-point-jv** — still owed.
- **aki-day3-onosato-aonishiki-kotozakura-3-0 / aki-day3-kirishima-atamifuji-first-loss / aki-day4-card / chiefs-31-10-broncos / murray-protocol / yankees-clinch-8-3 / dodgers-14th-straight / cubs-7-3-braves-pca-42 / leeds-4-1-newcastle / arsenal-ipswich-cup / fsu-fires-alford / kawhi-trade-complete** — ran. **maezumo-debutant / other-cup-ties / lawrence-frank-suspension** — held.
- **youth-waterfowl-sept19 / bear-gun-sept19-25 / archery-sept26 / regular-goose-oct3 / squirrel-day-4 / dove-day-15 / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead / flounder-CLOSED-ff-27** — ran. **gauley-window-2-friday-nps-confirmed / gauley-fest-thu / fr86-williams / stocking-none** — seasons note. **williams-106-falling / point-pleasant-25-76-steady / huntington-28-28-crest-28-50 / beach-hazards-pender / ilm-rip-moderate / nhc-40pct / moon-3-5-days** — water block.
- **sportsman-index-stale-no-12** — for Nate (No. 32 computed from the edition files). **fetch-fishing-24h-window-bug** — for Nate. **direction-gate-other-team-loses** — for Nate (fifth wording issue: "as Toronto loses"). **style-md-two-away-lines-vs-validator-one / edition-md-webster-commission-schedule / edition-md-nps-gauley-address (whitewater.htm works)** — for Nate. **pip-pythonhosted-timeout** — noted. **detached-head-eighteenth** — recurring.

### Covered slugs, 2026-09-15

`scotus-blocks-usps-mail-ballot-rules-midterms`, `epa-finalizes-carbon-repeal-houston`, `pentagon-ig-iran-war-33-4b-munitions`, `saylor-blocks-dhs-visa-four-year-cap`, `pa-measles-693-third-death-review`,
`nato-lithuania-first-drone-shootdown`, `saudi-strikes-yemen-houthis-13-wounded`, `dangote-1-6b-ipo-lagos`, `venezuela-g20-energy-houston`,
`huntington-flock-guardrails-7-2`, `morrisey-disaster-request-fayette-harrison-kanawha`, `raylees-law-compromise-interims`, `underwood-smith-42-graduates`,
`kroger-marketplace-5th-24th`, `i-64-fort-hill-bridge-overnight-closures`, `wood-county-five-75k-grants-powerflo-120`, `lake-paran-stone-skipping-sept-19`, `red-oak-fire-tower-overnight-stays`, `surf-city-ebike-focus-group-sept-28`,
`fort-st-james-homicide-77`, `osisko-cariboo-mine-full-build`, `bc-deficit-13-8b-wildfire-614m`, `seventh-mla-milobar-party-wilson`, `us-50pct-tariffs-110-canadian-goods`, `calgary-shaw-ndp-582`,
`vega-c-vv30-flex-sentinel-3c-flew`, `atlas-z-boson-entanglement-prl`, `ucsf-bci-speech-gesture-nature-neuro`, `yunnan-underwater-perovskite-joule`,
`uk-jchr-ai-bill-single-regulator`, `trump-ai-slowdown-hoax-huang`, `openfold3-abbvie-astex-proprietary`,
`liverpool-tottenham-carabao-team-news`, `taylor-bengals-pretty-clean`, `dodgers-4-1-reds-skubal-clinch`, `monken-watson-starter-tampa`, `wvu-strachan-could-debut-virginia`,
`aki-day3-onosato-aonishiki-kotozakura-unbeaten`, `aki-day3-kirishima-takayasu-atamifuji-takanosho`, `aki-day4-onosato-takayasu`, `chiefs-31-10-broncos-walker-173`, `murray-concussion-protocol`, `yankees-8-3-twins-clinch`, `dodgers-14th-straight-ties-braves`, `cubs-7-3-braves-pca-42-top-wc`, `leeds-4-1-newcastle-third`, `arsenal-ipswich-carabao-preview`, `fsu-fires-alford-warwick-interim`, `kawhi-raptors-trade-complete-penalties`,
`youth-waterfowl-sept19`, `bear-gun-sept19-25`, `archery-sept26`, `regular-goose-oct3-splits`, `squirrel-day-4`, `dove-day-15-rails-snipe`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish`, `black-drum-sheepshead`, `flounder-closed-ff-27`,
`gauley-window-2-sept-18-21-nps`, `gauley-fest-sept-17-20`, `fr86-williams-closure`, `stocking-none`, `williams-106-falling-off-270`, `point-pleasant-25-76-steady`, `huntington-28-28-crest-28-50-monday`, `no-wv-alerts`, `beach-hazards-pender-longshore`, `ilm-rip-moderate-2-4`, `nhc-40pct-ese-bermuda`, `moon-3-5-days-springs-easing`, `topsail-fp-sept1-fourteen-days`

## 2026-09-16 — No. 43 (Times) and No. 33 (Sports & Sportsman)

| Open-ended | **Twenty-second morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), launched 5:35, filed between 5:38 and 5:46 a.m. ET. The Times validated, rendered and pushed at **5:47 a.m. ET** (commit 6e5f0b4); Sports & Sportsman in the same push (commit 7255ad7), 17 minutes after the 5:30 wake. Digest dry-run 1,017 embed chars, hero attached (80 KB). The 6:50 `send_later` wake fired at 6:50:46, the post ran in the foreground from 6:51, `--not-before` held 9 minutes and **the digest landed at 7:00:01 a.m. ET** (1,017 embed chars, hero attached, degraded []). Pages served both dated pages 200 at 5:48:25, about 40 seconds after the push. **Detached HEAD at session start again — nineteenth occurrence**; `git checkout main && git pull origin main` fixed it (15 commits behind) before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **Setup: pip installed Pillow on the first try. USGS was 503 on BOTH Ohio gauges at the 5:32 fetch** (Williams and NOAA answered); `fetch_fishing.py` re-ran clean at 5:33, 4 waters, 0 errors, and nothing was written from the first run. Stats 4 entries (all four down: S&P 7,585.73 -0.45%, Dow 52,093.11 -0.63%, Nasdaq 25,981.57 -0.78%, Bitcoin $75,785 -1.42%); standings 5 clubs (Pirates 75-76 third, 19.0 back, 7.0 out; Reds 70-81 fifth, 24.0 back, 12.0 out; Brewers 94-57 clinched) | **fetch-fishing-24h-window-bug — still for Nate** (all three USGS 24h-ago fields were Monday 5:45 a.m.) |
| Open-ended | **The lead is the Senate's 49-50 cloture failure on the CLARITY Act** — the watch-list item from Tuesday 2:15 p.m. NPR primary (curl; WebFetch 503), cross-checked at PBS NewsHour, the Senate Daily Press official tally, CoinDesk (bitcoin $75,850, -4.2%, attributed) and Gallego's release. GOP no votes Collins, Hawley, Moran, Tillis (Tillis switched to enter a motion to reconsider); a CNBC snippet saying 50-49 with Paul was never opened and was disregarded. **Second choice, run as the first U.S. brief: the NBC4/Telemundo 52 news helicopter crash in Chatsworth, LA, ~7 p.m. PT Tuesday, 3 dead** (NBC News; ABC7 and AP via WLOS cross-checks) — bus-crash deaths (2 v 3) and heli hospitalizations (1 v 2) disagree across outlets and were dropped. The World desk's Mecca drone (Saudi coalition says it downed a Houthi drone bound for Mecca; Houthis deny and claim an F-15) ran as the Middle East brief. **Sweden: no movement, 176-173, final Thursday** — not printed | **watch: FOMC today 2 p.m. ET (~90% hike priced, CME); Sweden final Thursday; CLARITY motion to reconsider; College Sports Act on the floor Wed 10 a.m.; Massie's Hegseth impeachment articles** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** NPR's og:image is a Getty file photo of a dozen novelty bitcoin tokens heaped on a brushed-metal table at a low angle — pure geometry, no people. PBS's og:image (a pile of mixed crypto coins with a Shiba Inu face) was viewed too and passed over. Drawn as a generated line drawing (`scratchpad/draw.py`, 88 paths): twelve ellipses in perspective with rim, inner ring, dotted ring, dashed code rows, a bold B with the two bars and a relief offset, stacked edges, brushed-metal arcs behind, and occlusion computed by dropping back-coin points inside front coins. First pass was 117 KB from dense sampling and the validator refused it; thinned to 51 KB. Rasterized with headless Chromium and looked at twice. Fifth rung-1 drawing in a row | |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley, summers_new_river), away 1, hotspots 2 — seven lines.** Statewide: FirstEnergy at Joint Energy on aging coal plants, $500M in five years (WCHS); tax collections $46.1M / 5.8% over estimate, $838.3M in two months (News and Sentinel); DOT to add prime contractors to its dashboard, no timeline (WSAZ); Benson's WVU Express direct admission for Monongalia and Kanawha seniors (News and Sentinel). Regional: Icon Cinemas takes the Marquee at Pullman Square Oct. 1, $6M remodel (Herald-Dispatch — this is the Marquee closing story that 404'd Tuesday); Putnam data-center resolution to the commission Sept. 29 (WCHS); Parkersburg finance committee 4-0 on $668,142 for housing (N&S); **Pipestem's first Oktoberfest Oct. 16-18 (WOAY, Sept. 14) — the first Summers line since the Sept. 12 edition; an announcement, at the edge of the 48-hour window.** **Empty: nicholas_webster** (WOAY Nicholas tag latest Sept. 10 Carnifex reenactment, ran Sept. 13; WOWK 403; Register-Herald nothing Sept. 15-16; Nicholas Chronicle stale; WCHS Summersville topic page years old). Away: North Bennington joins a national PFAS class action (Banner, Tuesday). Cabin: Webster County EDA voted Sept. 8 to offer on 50-plus DNR acres near Big Ditch Lake for an RV park (Echo, Sept. 14 lede). Topsail: NTB website relaunches today (town notice, Sept. 14). Held: $582K DNA-lab grant; citizen-only voting amendment (both WCHS); WVU $90M Health Sciences building (Dominion Post — same Sept. 11 BOG meeting as the Sept. 13 brief); Logan Elementary closure (WSAZ); SBA Pleasants tornado loans (WTAP); Gino's West Side closure; LUCAS screening Oct. 13-14; Bennington Select Board option-tax debate (Monday); grand jury indicted 12 (Sept. 9); Surf City JH Batts addendum (Sept. 9). **FEMA has not answered Morrisey's request; hens vote EIGHTH morning no result; no Webster commission agenda posted for today's 9 a.m.** | **watch: FEMA answer; Devine prelim Sept. 23; Putnam commission Sept. 29; Parkersburg full council Sept. 22; hens** |
| Open-ended | **Canada 2/2/2.** PG: nine mayoral candidates, most in B.C., Yu among them, 19 for eight council seats (CBC); axe attack on a downtown security guard, 1100 block of 3rd Avenue, Sunday 9 p.m., minor hand injuries (CKPG). BC: court strikes the rural-service rule for foreign-trained doctors, Kahlon to revise (CBC); Harbour Air buys Pacific Coastal, 59 aircraft, 25 communities, 900 staff, no price (CHEK; CBC/CP 40+19 consistent). Canada: von der Leyen offers Canada "first associate member" status in Strasbourg, Carney addresses MEPs Thursday (CP via iNFOnews; CKPG CP roundup and Global preview corroborate); rivals target Fréchette's record in the first Quebec debate, vote Oct. 5 (CP via Medicine Hat News). Held: substation break-in 60 km north of PG, one airlifted critical (CBC); Carney opens four airports to private investment (CBC); gun groups' Tumbler Ridge letter (CP via CKPG); McLeod Lake community forest (news.gov.bc.ca refused — never opened). **My PG Now 403 on both domains today** | **watch — Carney's speech Thursday; second Quebec debate tonight; Unifor-Stellantis Sept. 20; Cougars opener Friday; FSJ homicide; PG vote Oct. 17** |
| Open-ended | **Sumo, Aki Day 4 — Sports Hochi (via excite), Kyodo data via dmenu Sports and Sportsnavi; JSA results pages still empty; NHK consent wall; r/Sumo returned a login shell (blocked).** **Takayasu (M2, 36) thrust down Onosato by tsukitaoshi for a seventh kinboshi; Kotozakura (uwatenage over Gonoyama) is the sole unbeaten at four-and-oh.** Aonishiki lost to new komusubi Hakunofuji (first win in seven meetings); Kirishima (over Kotoeimine) and Atamifuji (over Fujiryoga) three-and-one; Fujinokawa two-and-two; Yoshinofuji winless. No new makuuchi kyujo (JSA absence page). **Day 5: Onosato v Yoshinofuji, Kotozakura v Mitoumi, Aonishiki v Gonoyama, Kirishima v Takanosho, Atamifuji v Daieisho.** Records in words; no `result` on sumo briefs | **Day 5 results Thursday; Kotozakura alone in front** |
| Open-ended | **Our Teams: 8 briefs.** **Hannan: MaxPreps posts Parkersburg Catholic 7-2 at Ashton, record 1-2 — the first Hannan result any outside source has carried since Aug. 27; MaxPreps has DROPPED the Sept. 9 Point JV and Sept. 10 Westside fixtures from the schedule entirely, so those results are owed an eighth morning and may never publish.** Liverpool 3-1 Tottenham, Carabao Cup third round, straight down the middle in two briefs (LFC report: Mac Allister 21', Gakpo early second half, Gallagher, Szoboszlai stoppage time, 60,169; Sky for De Zerbi's "need a click"; LFC's 46' for Gakpo was a misread, Sky/NBC 54', so no minute printed); **Dodgers 4-0 Reds** (Yamamoto one-hitter, CBS box, LA nine straight over Cincinnati); Browns put Sampson on IR, sign McLaughlin (club); FCC waives Miazga, loans Jimenez to Fluminense (club); **Brewers 5-1 Pirates, Milwaukee clinches the NL Central when the Cubs lost ~50 minutes later** (CBS box); Rodriguez: Talley 1-2 weeks, Thomas hearing Thursday (SI). Standings: MLB byte-matched; PL unchanged (Sky, no league games); FCC 32 pts ninth, Crew 23 pts 13th (FOX); Bengals 1-0, Browns 0-1; WVU 2-0, Marshall 1-1, Ohio 1-1; Hannan 1-2 per MaxPreps. Upcoming 27 lines Sept. 16-23, ET throughout; FOX schedule pages print UTC-looking times, cross-checked against the MLB Stats API. Sat out: Chelsea (training absences only on fan sites), Bengals (day off), Crew (preview ran Monday), Marshall, Ohio, Spurs (camps open Sept. 29 per NBA.com key dates), USMNT (roster Thursday) | **Carabao fourth-round draw Wednesday; Crew-Orlando result; USMNT roster; NFL Wednesday injury reports; Thomas hearing** |
| Open-ended | **Leagues: 9 briefs** (Pacheco back surgery, a Monday item, dropped by the editor). Sumo 3; MLB: Guardians 7-6 White Sox walk-off, half-game back (CBS box); **Braves 6-3 Cubs hands Milwaukee the division** — first headline "Braves rally past the Cubs" tripped the direction gate because "rally past" is not a win verb and the next verb ("Washington beat") read Chicago as its subject; reworded to "Braves beat the Cubs"; the "Padres' eight-game winning streak" clause was cut because the CBS line was ambiguous; **the CBS ATL@CHC box-score URL was STRIPPED by the validator as a 404** (logged); Rays 2-1 Athletics on Caminero's 41st (CBS box); Carabao: Arsenal 4-2 Ipswich, Dowman 16 (Sky); Fulham 3-2 West Ham, Peterborough on pens (Sky); Vanderbilt names Curtis starter (CBS — "2-0" tripped the score regex without a `result`, reworded to words). Held: Murray protocol (no movement), Lawrence Frank suspension, Tigers 10-1 | **direction-gate — a non-listed win verb ("rally past") lets the NEXT verb pick the subject** |
| Open-ended | **Outdoors: all four waters.** Williams 72.9 cfs / 1.47 ft FALLING, clean recession (105 at 5:45 a.m. Tuesday), flag agrees; no gauge temperature. Point Pleasant 24.62, down 1.14 in 24h, FALLING, flag agrees, under the NWPS forecast curve. **Huntington 27.33 — crested 28.59 at 1:30 p.m. Tuesday (a second crest above Monday's 28.50) and fell 1.26 ft since; the fetcher's RISING flag is the 48-hour artifact again and the note says so.** Topsail: all four sound events inside today (no spillover tags), 81.1F Beaufort, moon 22% / 4.5 days easing toward first quarter; sound lag 70 min on the high; red drum ebb window 5:15-7:20 p.m.; **Beach Hazards Statement Coastal Pender 6 a.m.-8 p.m., moderate rip, NE 10, surf 1-2**; NHC one trough east of Bermuda 10%/30%. **Only WV product: a heat Special Weather Statement to 3 p.m., lowland counties Mason/Cabell to Kanawha/Braxton, not Webster.** Seasons: youth waterfowl + bear gun Sept. 19 (3 days); archery Sept. 26 (10); regular goose Oct. 3 (17); squirrel Day 5; dove day 16, 25 left; **going_out EMPTY — flounder dropped as closed, nothing else closes within two weeks**; Gauley window Friday (NPS page), Gauley Fest Thursday (AW page; Eventbrite hours disagree, hours dropped); Mon NF alerts nothing new; stocking silent; WV reference valid through 2027-06-30 | **watch — Gauley window Friday; Huntington toward 26 by Thursday; Thursday storms at Cowen 11-3** |
| Open-ended | **Sci/Tech and AI.** SpaceX scrubbed USSF-259 before fueling, backup 9 p.m. ET tonight (Spaceflight Now); Flinders 2.22M pre-1788 population, Nature Human Behaviour (Phys.org, Sept. 15); NASA activates Roman's Wide Field Instrument Sept. 11, images early 2027 (NASA blog); Mass General Brigham ties Epstein-Barr activity to MS relapses, 114 patients, Nature Medicine (EurekAlert, source set to the institution). AI: CAC AI Safety Governance Framework 3.0, released Monday (Register); OpenAI says it has held safety talks with Anthropic and Google for weeks, Altman commits to outside evaluators — OpenAI's own claim, labeled (TechCrunch); iLands agent email spam, 70,000 agents / 1.6M messages from iLands' own site (404 Media). Held: City of Hope pancreatic blood test 87%; UC Davis $41/ton heat-labor cost; XENONnT 17 keV neutrinos (preprint); Congo Ebola 7,258 cases (CIDRAP); Sanders/Casar superintelligence-ban bill next week (NPR); Microsoft model conduct code and Musk-Apple dismissal (both Monday) | **watch — USSF-259 tonight; Sanders bill; Ratepayer Protection Act data-center vote** |
| Open-ended | **Source status.** OPEN: NPR (curl only), PBS, Senate Daily Press, CoinDesk, NBC, ABC7, AP via WLOS/Boston.com/Local 10, CBS, Al Jazeera, Kyiv Independent, Euronews, France24, Times of Israel, Arab News, Nikkei, WSAZ, WCHS, News and Sentinel, Dominion Post (front only), WVPB, WTAP, Herald-Dispatch, Hinton News, Register-Herald, WOAY, Bennington Banner, NTB news, Surf City civicalerts, topsailbeachnc.gov, **The Webster Echo (200, ledes)**, webstercounty.wv.gov (no agendas at all), CKPG, CBC (curl), CHEK, Global, iNFOnews/Medicine Hat News (CP), Spaceflight Now, Phys.org, NASA, EurekAlert, Science News, CIDRAP, Register, TechCrunch, 404 Media, MacRumors, CBS boxes, MLB.com, liverpoolfc.com (curl), Sky, NBC Sports, FOX schedules, MLB Stats API, MaxPreps, SI/WVU, clevelandbrowns.com, fccincinnati.com, Sports Hochi via excite, dmenu Sports, Sportsnavi, Nikkan (curl), JSA absence page, USGS (after 5:33), NWPS, api.weather.gov, ILM SRF, NHC, NCDMF limits, NPS whitewater.htm, AW Gauley Fest, WVDNR migratory PDF, Fisherman's Post feed. BLOCKED: CNBC, Axios, KTLA, KOSU, DW, NHK, **WV MetroNews (fifth morning)**, governor.wv.gov release list (404), WV Watch (403 today), WOWK, Nicholas Chronicle (stale), VTDigger search, WECT search, Port City Daily search, topsailpost.com (DNS), **My PG Now (403 both domains)**, news.gov.bc.ca, PG Citizen, Vancouver Sun, nature.com, New Scientist, Ars (search), science.org, Caixin, r/Sumo (login shell), JSA results pages, ESPN soccer pages, tottenhamhotspur.com, chelseafc.com, On3, Herdzone, ohiobobcats, wvusports, nba.com/spurs, ussoccer (index only), Corps Huntington (cert) | **watch — MetroNews; My PG Now; r/Sumo** |
| Open-ended | **Traps dodged.** (1) CNBC's 50-49/Paul tally from a snippet — not used. (2) LA bus-crash dead 2 v 3, heli hospitalized 1 v 2, scene distance — dropped. (3) LFC 46' Gakpo misread — no minute. (4) "Braves rally past" — direction gate; reworded. (5) Padres streak clause ambiguous in CBS — cut. (6) Vanderbilt "2-0" as a score — words. (7) Gauley Fest hours, AW v Eventbrite — dates only. (8) BOG Health Sciences building overlaps the Sept. 13 brief — held. (9) McLeod Lake forest never opened — not filed. (10) Harbour Air fleet 59 v 40+19 — consistent, printed 59. (11) Pipestem Oktoberfest is an announcement at the 48-hour edge — printed with the outlet's date, flagged here. (12) Hannan 7-2 is MaxPreps only — attributed in the headline and the summary, not stated flat | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-16** | **FOMC 2 p.m. ET (~90% hike priced); Aki Day 4 (ran); Carabao fourth-round draw; Crew v. Orlando City Open Cup semi 7 p.m.; USSF-259 backup 9 p.m. ET; College Sports Act on the Senate floor 10 a.m.; second Quebec debate; Webster County Commission 9 a.m. (no agenda); NTB website relaunch (ran); Reds v. Dodgers (Abbott v. Snell), Pirates v. Brewers (Jones v. Henderson) 6:40; Beach Hazards Coastal Pender to 8 p.m.** | |
| **2026-09-17** | **Aki Day 5 (Onosato v. Yoshinofuji, Kotozakura v. Mitoumi); Sweden final result; Carney addresses the European Parliament; USMNT roster; WVU's Thomas hearing; Gauley Fest opens, Summersville (to Sept. 20); Hannan at Westside 6 p.m. Beckley YMCA; Pirates v. Brewers 12:35, Reds v. Dodgers 12:40; storms at Cowen 11-3** | |
| **2026-09-18** | **Second Gauley release window (18-21); Chelsea at Brentford 3 p.m. ET; Reds v. Cubs (Burns v. Holmes), Pirates v. Royals (Skenes v. Dobnak) 6:40; Cougars opener v. Penticton** | |
| **2026-09-19** | **WV youth waterfowl day; bear gun second window (19-25, selected counties); Lake Paran stone-skipping 1-7 p.m.; U.S. 7 closure begins; Spurs v. Villa 7:30 a.m. ET; Marshall at Missouri State 6:30, Ohio at South Alabama 7, WVU v. No. 25 Virginia in Charlotte 7:30; Crew at Montreal 7:30, FCC at Houston 8:30** | |
| **2026-09-20** | **Bournemouth v. Liverpool 9 a.m. ET; Bengals at Houston, Browns at Tampa Bay 1 p.m.; Pirates v. Royals 1:35 (Bachar v. Wacha), Reds v. Cubs 1:40; Unifor-Stellantis expires 11:59 p.m.; Gauley Fest closes** | |
| **2026-09-22** | **Hannan at Calvary 6 p.m. (venue unconfirmed); Parkersburg full council on the $668,142 housing money; NTB hearing on the New River Inlet draft EIS 6 p.m.; Reds at Braves 7:15, Pirates v. Cardinals 6:40** | |
| **2026-09-23** | **Devine preliminary hearing; third Quebec debate** | |
| **2026-09-26** | **WV archery/crossbow deer and bear open; USMNT v. Peru** | |
| **2026-09-28** | **NBA media day; Surf City e-bike focus group 6-8 p.m., Hampstead** | |
| **2026-09-29** | **Putnam County Commission takes up the data-center resolution; NBA camps open; Hannan at Roane 6:30; USMNT v. Chile 8 p.m. ET** | |
| **2026-10-01** | **Icon Cinemas takes over the Marquee at Pullman Square** | |
| **2026-10-03** | **WV regular goose and duck seasons open** | |
| **2026-10-05** | **Quebec general election** | |
| **2026-10-16** | **Pipestem State Park's first Oktoberfest (16-18)** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18)** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |

### Open threads

- **senate-blocks-clarity-act-49-50** — led; the motion to reconsider, ethics-clause talks, and any renewed vote are the follow-ups. **la-news-helicopter-crash-3-dead** — U.S. brief; NTSB cause is the follow-up. **college-sports-act-cloture-74-24 / saab-guilty-plea-195m / fed-hike-preview-90pct** — ran. **dhs-oig-alligator-cages / kennedy-center-closure-cooper-ruling / massie-hegseth-impeachment / byrne-confirmed-52-45 / patel-hearing / cbo-iran-war-38b** — alternates.
- **saudi-downs-houthi-drone-mecca / nikopol-bus-strike-5-dead / sudan-gold-mine-collapse-60 / hong-kong-five-year-plan** — ran. **sweden-176-173 (final Thursday) / indonesia-ferry / rwanda-drc-geneva / gaza-collapse-toll / seoul-north-korea-award** — alternates.
- **wv-coal-plants-joint-energy / tax-collections-46-1m-over / dot-dashboard-contractors / wvu-express-direct-admission** — ran. **dna-lab-582k / citizen-voting-amendment / bog-health-sciences-90m / logan-elementary-closure / sba-pleasants-loans** — alternates. **icon-cinemas-marquee-oct-1 / putnam-data-center-resolution-sept-29 / parkersburg-668k-housing / pipestem-oktoberfest** — regional. **north-bennington-pfas-class-action** — away. **webster-eda-big-ditch-rv-park / ntb-website-relaunch** — hotspots. **fema-answer-morrisey / hens-vote (eighth morning) / webster-commission-no-agenda / gino-west-side / lucas-oct-13 / bennington-option-tax** — alternates.
- **pg-nine-mayoral-candidates / pg-axe-attack-security-guard / bc-court-foreign-doctors-rural-rule / harbour-air-pacific-coastal / von-der-leyen-associate-member / quebec-debate-frechette** — ran. **substation-break-in-airlift / carney-airports-private / tumbler-ridge-gun-letter / mcleod-lake-forest (never opened) / fsj-homicide / cougars-opener-friday** — alternates.
- **ussf-259-scrub / flinders-2-22m / roman-wfi-activated / ebv-ms-relapses** — ran. **city-of-hope-pancreatic-87 / uc-davis-41-per-ton / xenonnt-17kev / congo-ebola-7258** — alternates.
- **cac-framework-3-0 / openai-safety-talks-lehane / ilands-agent-spam** — ran. **sanders-casar-superintelligence-ban / microsoft-conduct-code / musk-drops-apple** — alternates.
- **hannan-7-2-parkersburg-catholic-maxpreps / liverpool-3-1-tottenham-carabao / de-zerbi-need-a-click / dodgers-4-0-reds-yamamoto / browns-sampson-ir-mclaughlin / fcc-miazga-waived-jimenez-loan / brewers-5-1-pirates-clinch / wvu-talley-thomas-hearing** — ran. **chelsea / bengals / crew / marshall / ohio / spurs / usmnt** — sat out. **hannan-westside / hannan-point-jv** — still owed; MaxPreps has removed both fixtures.
- **aki-day4-takayasu-kinboshi-onosato / aki-day4-kotozakura-sole-unbeaten / aki-day4-hakunofuji-aonishiki / aki-day5-card / guardians-7-6-white-sox / braves-6-3-cubs-milwaukee-clinch / rays-2-1-athletics-caminero-41 / arsenal-4-2-ipswich-dowman / fulham-3-2-west-ham / vanderbilt-curtis-starter** — ran. **pacheco-back-surgery (dropped) / tigers-10-1 / murray-protocol / lawrence-frank** — held.
- **youth-waterfowl-sept19 / bear-gun-sept19-25 / archery-sept26 / regular-goose-oct3 / squirrel-day-5 / dove-day-16 / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead** — ran; **going_out empty**. **gauley-window-2-friday / gauley-fest-thu / stocking-none / mon-nf-nothing-new** — seasons note. **williams-72-9-falling / point-pleasant-24-62-falling / huntington-27-33-off-28-59-crest / heat-sws-lowlands / beach-hazards-pender / nhc-10-30 / moon-4-5-days** — water block.
- **sportsman-index-stale-no-12** — for Nate (No. 33 computed from the edition files). **fetch-fishing-24h-window-bug** — for Nate (Huntington flag wrong again). **direction-gate-rally-past** — for Nate ("rally past" is not in the win-verb list, so the next verb picked the subject). **cbs-boxscore-atl-chc-404-stripped** — noted. **detached-head-nineteenth** — recurring.

### Covered slugs, 2026-09-16

`senate-blocks-clarity-act-49-50`, `la-news-helicopter-crash-chatsworth-3-dead`, `college-sports-act-cloture-74-24`, `saab-guilty-plea-miami-195m`, `fed-hike-preview-90pct-cme`,
`saudi-downs-houthi-drone-mecca`, `nikopol-bus-drone-strike-5-dead`, `sudan-al-zaraa-gold-mine-collapse-60`, `hong-kong-lee-five-year-plan`,
`wv-coal-plants-joint-energy-firstenergy-500m`, `wv-tax-collections-46-1m-over-estimate`, `wvdot-dashboard-contractor-names`, `wvu-express-direct-admission-benson`,
`icon-cinemas-marquee-pullman-oct-1`, `putnam-data-center-resolution-sept-29`, `parkersburg-finance-668k-housing`, `pipestem-first-oktoberfest-oct-16-18`, `north-bennington-pfas-class-action`, `webster-eda-big-ditch-lake-rv-park`, `ntb-website-relaunch-sept-16`,
`pg-nine-mayoral-candidates`, `pg-axe-attack-security-guard-3rd-ave`, `bc-court-strikes-foreign-doctors-rural-rule`, `harbour-air-buys-pacific-coastal`, `von-der-leyen-canada-associate-member`, `quebec-first-debate-frechette`,
`spacex-ussf-259-scrub-backup-wed`, `flinders-1788-population-2-22m`, `nasa-roman-wfi-activated`, `mgb-ebv-ms-relapses-nature-medicine`,
`cac-ai-safety-framework-3-0`, `openai-safety-talks-anthropic-google-lehane`, `ilands-agent-email-spam-404-media`,
`hannan-parkersburg-catholic-7-2-maxpreps`, `liverpool-3-1-tottenham-carabao-third-round`, `de-zerbi-need-a-click`, `dodgers-4-0-reds-yamamoto-one-hitter`, `browns-sampson-ir-mclaughlin-signed`, `fcc-miazga-waived-jimenez-fluminense`, `brewers-5-1-pirates-nl-central-clinch`, `wvu-talley-thomas-hearing-thursday`,
`aki-day4-takayasu-kinboshi-onosato-3-1`, `aki-day4-kotozakura-4-0-sole-unbeaten`, `aki-day4-hakunofuji-beats-aonishiki`, `aki-day5-card-onosato-yoshinofuji`, `guardians-7-6-white-sox-walk-off`, `braves-6-3-cubs-milwaukee-clinches`, `rays-2-1-athletics-caminero-41`, `arsenal-4-2-ipswich-dowman-brace`, `fulham-3-2-west-ham-peterborough-pens`, `vanderbilt-curtis-starter`,
`youth-waterfowl-sept19`, `bear-gun-sept19-25`, `archery-sept26`, `regular-goose-oct3-splits`, `squirrel-day-5`, `dove-day-16-rails-snipe`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish`, `black-drum-sheepshead`,
`gauley-window-2-sept-18-21-nps`, `gauley-fest-sept-17-20`, `stocking-none`, `williams-72-9-falling`, `point-pleasant-24-62-falling`, `huntington-27-33-off-28-59-crest`, `heat-sws-lowland-counties`, `beach-hazards-pender-moderate-rip`, `nhc-10-30-east-of-bermuda`, `moon-4-5-days-easing-to-neap`, `topsail-fp-sept1-fifteen-days`

## 2026-09-17 — No. 44 (Times) and No. 34 (Sports & Sportsman)

| Open-ended | **Twenty-third morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), launched 5:38, filed between 5:41 and 5:49 a.m. ET. The Times validated, rendered and pushed at **5:50 a.m. ET** (commit d75ad68); Sports & Sportsman in the same push (commit 3e6ca2d), 20 minutes after the 5:30 wake. Digest dry-run 1,084 embed chars, hero attached (77 KB). The 6:50 `send_later` wake fired at 6:50:51, the post ran in the foreground from 6:51, `--not-before` held 9 minutes and **the digest landed at 7:00:02 a.m. ET** (message 1550098999594319922, 1,084 embed chars, hero attached, degraded []). Pages was 404 on both dated pages for five minutes and served both 200 at 5:55:35, about five and a half minutes after the push — the longest build lag since the digest contract began. **Detached HEAD at session start again — twentieth occurrence**; `git checkout main && git pull origin main` fixed it before any work. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **Setup: pip installed Pillow on the first try. All three fetchers clean on the first run** — stats 4 entries (S&P 7,551.81 -0.45%, Dow 51,461.90 -1.21%, Nasdaq 25,978.43 -0.01%, Bitcoin $76,610 +1.06%); fishing 4 waters, 0 errors; standings 5 clubs (Pirates 75-77 third, 20.0 back, 8.0 out; Reds 71-81 fifth, 24.0 back, 12.0 out). **The fetcher's Point Pleasant "falling" flag compares against Tuesday 5:45 a.m. and is wrong for the day** — the pool bottomed 24.38 at 8 a.m. Wednesday and is up 0.30 in 24 hours; the water block prints the file's numbers and the trace's direction, and says so | **fetch-fishing-24h-window-bug — still for Nate** |
| Open-ended | **The lead is the Fed's quarter-point hike to 3.75%-4%, 12-0, the first since 2023, with Chair Kevin Warsh (took over in May) at the podium.** Fed statement (primary), NBC (curl and WebFetch), NPR (curl), Al Jazeera, PBS (AP). Warsh's "plain fact" quote from NBC/PBS; August CPI 3.4% and the projections (one more hike on average this year, none in 2027) from NPR; Trump's "1% or less" post and retained confidence from Al Jazeera; the Dow's 630-point fall from NBC (a CNBC snippet saying the S&P closed UP was never opened and was disregarded — NBC's 5:03 p.m. close says down 0.4%). U.S.: Johnson recesses the House, sidelining Massie's Hegseth impeachment (AP via PBS); Russia sanctions bill to Trump 262-159 (NPR); Sharifullah 20 years, Abbey Gate (AP via NBC); Navajo Nation flash flood, 3 dead near Newcomb (AP via ABC). World: Ukraine strikes 10 dead in five oblasts (Kyiv Independent); Thaci 25 years at the Kosovo Specialist Chambers (AP via NPR); Gaza City al-Saada collapse, 21 per Civil Defence, IDF denial (Al Jazeera, ToI liveblog); **Sudan al-Zara toll to 82 — movement on yesterday's 60** (AP via NBC). **Sweden final result NOT out** — val.se says the weekend; provisional 176-173 stands | **watch: Sweden final (weekend); CLARITY reconsider; College Sports Act final passage; Trump-Xi summit ~Sept. 24; House Iran war-powers 220-204 (Tuesday, held); Rwanda-DRC Geneva outcome** |
| Open-ended | **Art: RUNG 1, `placement: lead`, drawn around the person.** NBC's og:image and NPR's Getty frame are both tight portraits of Warsh at the lectern — a face, so undrawable — with two gold-fringed flags (U.S. at left, the Board of Governors' seal banner at right) against a dark curtain and gooseneck microphones. Drawn as the scene without the man (`scratchpad/draw.py`, 252 paths, 28 KB): draped U.S. flag on a pole, the Board banner with concentric seal rings, radial dashes for the lettering, a ring of stars and a simple eagle contour, fringe ticks on both free edges, faint curtain folds, and the lectern top with two microphones. Rasterized with headless Chromium and looked at twice; the caption says the flags, the credit names NBC and NPR. Sixth rung-1 drawing in a row | |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley, nicholas_webster), away 1, hotspots 2 — seven lines.** Statewide: Preservati on closed-loop data centers and water, HB 2014 rules hearing Sept. 28 (WCHS); PSC approves WVAW's $13M purchase of three Fayette PSDs (WVPB); foster care 5,700 from 7,000-plus in 2020, Helton (WCHS); Fitch A+ to AA- on lottery bonds (WTAP). Regional: two former Cabell candidates convicted of false swearing, sentencing Oct. 23 (WSAZ); Kanawha parks board adds five miles to Hatfield-McCoy at Tornado (WSAZ); Wood County PFAS class action v. Chemours, Washington Works landfill (WTAP); **Gauley Fest opens today in Summersville — first nicholas_webster line since Sept. 13** (American Whitewater). **Empty: summers_new_river** (Hinton News Sept. 16 = courthouse records and legal notices; WOAY Summers tag newest is the Oct. 13 LUCAS stop; WVVA nothing since Sept. 9; Register-Herald nothing; WVNS 403). Away: U.S. 7 closes Exit 2 to Exit 3 from 7 a.m. Saturday to Oct. 3 (Banner). Cabin: grand jury indicts 12, Sept. 9 (Echo, Monday). Topsail: Pender County's $500,000 PARTF grant for the Abbey Nature Preserve trailhead, Sept. 4 (county posting) — **Topsail was thin: NTB nothing since the relaunch, Topsail Beach nothing since Sept. 11, Surf City's Sept. 9 addendum is the fallback.** Held: Marshall fifth-year judge (Herald-Dispatch, Sept. 15); DNA grant $582,174 (WCHS); Caserta retiring Oct. 1, commission votes Sept. 24 (H-D); WISH Academy forum Sept. 25 (WVPB); Remington Place 37 lots in Winfield (WSAZ); Vienna parental leave (WTAP); Bennington drug bust 5 arrests (Banner); option-tax survey $1.8M (Banner); Bergoo UTV crash 2 dead Sept. 5 (Echo); Webster Memorial associate administrator (Echo). **FEMA still has not answered Morrisey's Kanawha/Fayette/Harrison request; hens vote NINTH morning no result.** **MetroNews 403 sixth morning; The Webster Echo answered (WebFetch); Gazette-Mail answered via curl** | **watch: FEMA answer; Caserta seat Sept. 24; Devine prelim Sept. 23; HB 2014 rules Sept. 28; Putnam commission Sept. 29; hens** |
| Open-ended | **Canada 2/2/2.** PG: UHNBC helipad demand at UBCM, Sampson (CKPG); Fort St. James — Dayna Monk's May 31 death now suspicious, second this week, 114 km west (CBC). BC: Eby names Cheryl Oates campaign manager, Elections B.C. prepping (CBC); Rattee says the Conservative caucus is "deeply divided," Findlay byelection Sept. 26 (CHEK). Canada: Trump's memorandum stripping Canadian goods from $280B-a-year federal procurement (CP via CHEK); Carney at the European Parliament after Trump's "hostile act" warning (Global) — **the speech was in progress at 5:39 a.m. ET when the desk filed; no text was available, and the brief says only what Trump said and when the address was set.** Held: Scott not seeking re-election; Northern Lights wildlife rescue v. Omineca biologists; Quesnel Front Street stabbing; PG-Vancouver public rail ask; Cobb runs in Williams Lake; Tumbler Ridge gun-groups letter; Eby 1M more with a doctor; 11 ex-AGs on treaties; Unifor asks Ottawa to block the Brampton sale (Sept. 20 deadline); second Quebec debate (sovereignty; third Sept. 23); Canada applies to the JEF; $150M to LawZero; Point Lepreau off-line; Pearson gold-heist charges dropped. **My PG Now answered today (newest Sept. 14); PG Citizen still 403; news.gov.bc.ca timeout** | **watch — Carney speech text; N.L. Churchill River vote Thursday; Unifor-Stellantis Sept. 20; Findlay byelection Sept. 26; Cougars opener Friday; PG vote Oct. 17** |
| Open-ended | **Sumo, Aki Day 5 — Sportsnavi torikumi table, Kyodo via dmenu, Sports Hochi and Kyodo and Nikkan copies on Yahoo Japan (curl, full text); Japan Times 402; r/Sumo not tried.** **Mitoumi (M, 33) pushed out Kotozakura — no unbeaten man left; nine share the lead at four-and-one** (Onosato, Kotozakura, Kirishima, Atamifuji, Mitoumi among them). Onosato forced out winless Yoshinofuji; Kirishima sent out Takanosho (who had won their last four); Atamifuji pushed out Daieisho; Aonishiki pushed down by Gonoyama, three-and-two; Fujinokawa pushed out Hakunofuji, three-and-two. Kyujo: Hoshoryu, Wakatakakage, Wakanokatsu. **Day 6: Onosato v Gonoyama, Kotozakura v Takanosho, Aonishiki v Fujinokawa, Kirishima v Yoshinofuji, Atamifuji v Kotoshoho.** Records in words; no `result` on sumo briefs | **Day 6 results Friday; nine-way tie** |
| Open-ended | **Our Teams: 9 briefs.** Carabao fourth-round draw — **Liverpool v Chelsea, a house-derby pairing, written as one brief under Chelsea with Liverpool's 3-1 over Tottenham as the `result`**, which also covers Tottenham (the validator refused Tottenham in sat_out for that reason); Burrow limited, back, "I'll do what it takes" (bengals.com); **Reds 6-2 Dodgers, Snell out after one inning with groin tightness, De La Cruz 28th** (CBS box); Teven Jenkins DNP (CBS injury report); **Crew 2-1 Orlando City, U.S. Open Cup final v. St. Louis City Oct. 21 in Columbus, first since 2010** (ussoccer.com); Del Rio-Wilson expected back (H-D, Thursday); Hauser on South Alabama's 423 rushing yards (The Post); **Brewers 5-4 Pirates, Yelich's two-run double off Mlodzinski in the seventh** (CBS box; "Brewers edge" was reworded to "beat" because bare "edge" is not in the win-verb list); Rodriguez on Strachan's possible debut, Talley 1-2 weeks, Thomas hearing Thursday (Dominion Post). Marshall's "1-1" tripped the score regex and became words. Standings: MLB byte-matched (both moved); PL unchanged; FCC 32 ninth, Crew 23 13th; Bengals 1-0 T-2nd, Browns 0-1 4th; WVU 2-0, Marshall 1-1, Ohio 1-1; Hannan 1-2 per MaxPreps. Upcoming 27 lines Sept. 17-24, all MLB from the Stats API (UTC converted), Hannan v. Roane Sept. 24 added. Sat out: FCC, Spurs (nba.com/spurs answered today), USMNT (roster due Thursday, not posted by 5:50), Hannan (at Westside tonight; Point JV and Westside results still owed, ninth morning). **chelseafc.com, tottenhamhotspur.com, ohiobobcats.com answered curl today** | **Hannan-Westside result Friday; USMNT roster; Thomas hearing; Carney speech; Man City v Norwich 2:30 p.m. ET** |
| Open-ended | **Leagues: 11 briefs.** Sumo 3; MLB: Guardians 6-3 White Sox, sole AL Central lead, first since July 3 (CBS box); **Cubs 8-4 Braves, Crow-Armstrong 43 and 44, LH franchise record** (CBS box — the Padres/Arizona 3.5 clause was cut to keep the brief clear of the standings gate); Twins 5-4 Yankees in 13, 17 strikeouts (CBS box). NFL: Darnold out, Lock starts (NFL.com — the 13-10 prior-week score was dropped rather than carry a second `result`); Murray limited in protocol, Wentz if not cleared (NBC/PFT). Carabao: Brighton 3-2 Man Utd from 2-0 down, Carrick (Sky); Everton 1-0 Wolves, Villa 3-1 Coventry, Fleetwood 1-0 Sheffield United (Sky results). NCAA: FBS Oversight Committee says the clock error decided Michigan 13-12 WMU, no authority to overturn (CBS). Held: Orioles 7-1 Mets; Padres 9-3 Rockies (Salas); Belichick WSJ interview; Jordan Mason IR. No Champions League this week (matchday 1 was Sept. 8-10) | **direction-gate — bare "edge" is a noun to the gate; "edged" is the verb** |
| Open-ended | **Outdoors: all four waters.** Williams 58.8 cfs / 1.37 ft FALLING (105 → 72.9 → 58.8 at this hour over three mornings), flag agrees; no gauge temperature. **Point Pleasant 24.92 — the fetcher's falling flag is the 48-hour artifact: the pool bottomed 24.38 at 8 a.m. Wednesday, climbed to 25.30 at 5:30 p.m. and has eased 0.38 since, up 0.30 in 24 hours; direction printed from the trace.** Huntington 26.48, down 0.85 in 24 hours, flag agrees, though it rose half a foot overnight inside the fall. Both Ohio gauges run 0.5-0.8 ft over the NWPS Wednesday-morning forecast. Topsail: all four sound events inside today (H 1:09 AM 3.2, L 7:13 AM 0.9, H 1:43 PM 4.0, L 8:11 PM 1.3), 80.6F Beaufort, moon 31% / 5.5 days, waxing toward first quarter; **no Beach Hazards for Coastal Pender today** (first since Monday), ILM rip risk LOW, surf ~2 ft; NHC AL98 east of Bermuda now 40%/40%, nothing near the Carolinas; **Fisherman's Post still Sept. 1, 16 days old.** Seasons: youth waterfowl Sept. 19 (2 days); bear gun Sept. 19-25 selected counties; archery Sept. 26 (9); regular goose Oct. 3 (16); squirrel Day 6; dove day 17, 24 left; **going_out empty**; Gauley Fest opens today (AW event page; the two AW pages disagree on Thursday hours, none printed); second Gauley window Sept. 18-21 (NPS page, updated Aug. 26); Mon NF alerts nothing since Sept. 14; stocking silent; migratory bird PDF opened and read fresh (PyMuPDF; pypdf is broken here); WV reference valid through 2027-06-30. **NCDMF footnote C text did not surface in today's parse, so the over-27-inch drum clause was dropped.** **Coastal Pender is NCZ106, not NCZ108 (New Hanover)** | **watch — Gauley window Friday; NCZ106 for Pender; Day 6** |
| Open-ended | **Sci/Tech and AI.** USSF-259 flew at 9:07 p.m. ET Wednesday, B1097's 13th (Spaceflight Now); LRO's McGetchin crater, 728 ft, once-a-century, two Science Advances papers (NASA); Mount Sinai wildfire smoke 4% of PM2.5 / 17% of risk, 414,016 patients, Lancet Oncology + Nature Communications (EurekAlert); BASE antiprotons trucked 5 miles, stored a month, Nature (Phys.org). AI: Ratepayer Protection Act 417-3 (NBC); OpenAI's six new misalignment reports (Register); Wesleyan's 164 AI-made political ads, 31 states (NPR, Wednesday). Held: Stanford levetiracetam DMG (EurekAlert); WWA Nepal attribution; WMO 1,400 gigatons; City of Hope 87% (Medical Xpress); UC Davis $41/ton; Congo Ebola 7,258 (CIDRAP, Sept. 15); Irregular's self-modifying Qwen agent (Register); Pittman's noon deadline for the X/SpaceXAI-Apple settlement (9to5Mac). **Sanders/Casar superintelligence bill: NOT introduced; Sanders said Sept. 15 it comes "next week."** nature.com, science.org, Ars, Politico, thehill, congress.gov blocked | **watch — Sanders/Casar bill week of Sept. 21; Pittman deadline noon today; Man City-Norwich** |
| Open-ended | **Source status.** OPEN: federalreserve.gov, NBC, NPR (curl), PBS, Al Jazeera, ABC wire, CBS, Kyiv Independent, Euronews (WebFetch), France24, Times of Israel, NASA, Spaceflight Now, EurekAlert, Phys.org, Medical Xpress, CIDRAP (curl+UA), Register, 9to5Mac, WSAZ, WCHS, WTAP, WVPB, WVVA, Herald-Dispatch, Dominion Post (article URLs), Hinton News, Register-Herald (front), WOAY (tags), Gazette-Mail (curl), legislature blog, **The Webster Echo (WebFetch)**, Bennington Banner (/news/), village and town of Bennington, American Whitewater, Pender County alerts, Surf City civicalerts, Topsail Beach news, NTB /CivicAlerts.aspx, CKPG, CBC (curl), CHEK, Global, iNFOnews (CP), **My PG Now (curl)**, Sportsnavi, dmenu Sports, Yahoo Japan article copies, excite/Hochi, CBS boxes, MLB.com, MLB Stats API, ussoccer.com, bengals.com, Sky, NFL.com, NBC/PFT, The Post Athens (/section/sports), **chelseafc.com, tottenhamhotspur.com, nba.com/spurs, ohiobobcats.com (curl)**, MaxPreps, USGS, NWPS, api.weather.gov, ILM SRF, NHC, NCDMF, NPS whitewater.htm, AW, WVDNR MigBird PDF (curl), Fisherman's Post feed (WebFetch only). BLOCKED: CNBC, Axios, CNN, DW, Nikkei (paywall after lede), NHK, Japan Times (402), nature.com, science.org, Ars, Politico, thehill, congress.gov, cityofhope.org, **WV MetroNews (sixth morning)**, WV Watch, WV News, WVNS, WOWK, postandvoice.com (DNS), jdnews/starnews (search), NTB /news and /meetings (404 since the relaunch), Nicholas Chronicle (stale), VTDigger (nothing since Aug. 27), PG Citizen, news.gov.bc.ca (timeout), sd57, RCMP BC, CTV bodies, Euronews (curl 406), UEFA, worldfootball, SI (500), Point Pleasant Register (503), Herdzone, Dawgs By Nature, Athlon, gauleyfest.org (TLS), fishermanspost.com (curl), Corps Huntington (not tried) | **watch — MetroNews; NTB paths after the relaunch; r/Sumo** |
| Open-ended | **Traps dodged.** (1) CNBC's "S&P up 0.4%" snippet v. NBC's close — NBC, attributed. (2) Powell is not the chair; Warsh is — every outlet agreed. (3) Carney's speech in progress at filing — printed only what was set. (4) Sweden final not out — not printed. (5) France24's "late Tuesday" v. AP's Sunday start on the Sudan mine — AP. (6) "Brewers edge" — direction gate, reworded. (7) Marshall "1-1" as a score — words. (8) Tottenham in sat_out while the draw brief named the 3-1 — removed from sat_out. (9) Darnold's 13-10 prior-week score — dropped rather than a second `result`. (10) Cubs' Padres/Arizona 3.5 clause — cut near the standings gate. (11) Point Pleasant flag wrong — trace direction printed, said so. (12) NCDMF footnote C text not on today's parse — clause dropped. (13) Gauley Fest Thursday hours disagree across AW pages — none printed. (14) Cabin line ran 183 chars — cut to 156. (15) Art caption 207 chars — cut to 133. (16) Desk JSON carried `&amp;` in URLs and place strings — rebuilt from config and plain strings | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-17** | **Aki Day 5 (ran); Carney addresses the European Parliament (in progress at press); Pittman's noon deadline on the X/SpaceXAI-Apple settlement; N.L. legislature votes on the Churchill River deal; USMNT roster; WVU's Thomas hearing; Gauley Fest opens (to Sept. 20); Hannan at Westside 6 p.m. Beckley YMCA; Pirates v. Brewers 12:35, Reds v. Dodgers 12:40; Man City v. Norwich 2:30 p.m. ET** | |
| **2026-09-18** | **Aki Day 6 (Onosato v. Gonoyama, Kotozakura v. Takanosho); second Gauley release window (18-21); Chelsea at Brentford 3 p.m. ET; Reds v. Cubs, Pirates v. Royals 6:40; Cougars opener** | |
| **2026-09-19** | **U.S. 7 closes Exit 2-Exit 3, Bennington (to Oct. 3); WV youth waterfowl day; bear gun second window (19-25, selected counties); Lake Paran stone-skipping; Spurs v. Villa 7:30 a.m. ET; Marshall at Missouri State 6:30, Ohio at South Alabama 7, WVU v. No. 25 Virginia in Charlotte 7:30; Crew at Montreal 7:30, FCC at Houston 8:30** | |
| **2026-09-20** | **Bournemouth v. Liverpool 9 a.m. ET; Bengals at Houston, Browns at Tampa Bay 1 p.m.; Pirates v. Royals 1:35, Reds v. Cubs 1:40; Unifor-Stellantis expires 11:59 p.m.; Gauley Fest closes; Sweden final count expected over the weekend** | |
| **2026-09-22** | **Hannan at Calvary 6 p.m. (venue unconfirmed); Parkersburg full council; NTB New River Inlet EIS hearing 6 p.m.; Reds at Braves 7:15, Pirates v. Cardinals 6:40** | |
| **2026-09-23** | **Devine preliminary hearing; third Quebec debate** | |
| **2026-09-24** | **Cabell commission votes on the clerk's seat (Caserta retires Oct. 1); Hannan v. Roane at Ashton 6 p.m.; Trump-Xi summit window (NPR, unnamed sources)** | |
| **2026-09-26** | **WV archery/crossbow deer and bear open; USMNT v. Peru; Findlay byelection** | |
| **2026-09-28** | **HB 2014 data-center rules hearing; NBA media day; Surf City e-bike focus group 6-8 p.m.** | |
| **2026-09-29** | **Putnam County Commission on the data-center resolution; NBA camps open; Hannan at Roane 6:30; USMNT v. Chile 8 p.m. ET** | |
| **2026-10-03** | **WV regular goose and duck seasons open; U.S. 7 reopens** | |
| **2026-10-05** | **Quebec general election** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18)** | |
| **2026-10-21** | **U.S. Open Cup final, Crew v. St. Louis City, Columbus** | |
| **2026-10-23** | **Cabell false-swearing sentencing** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |

### Open threads

- **fed-hike-3-75-4-warsh** — led; the next meeting, the projections and any Trump move on Warsh are the follow-ups. **johnson-recess-hegseth-impeachment / russia-sanctions-262-159 / sharifullah-20-years / navajo-flood-3-dead** — ran. **saphier-surgeon-general-hearing / russian-operatives-indictment / leon-black-contempt / iran-war-powers-220-204 / trump-xi-summit** — alternates.
- **ukraine-strikes-10-dead / thaci-25-years / gaza-al-saada-collapse-21 / sudan-mine-toll-82** — ran. **sweden-final (weekend) / india-tariff-warning / falklands-oil-halt / yemen-mocha / israel-morocco-embassies / syria-alawite-sentences / seoul-kaesong-award / drc-ebola-tedros** — alternates.
- **wv-data-centers-water-preservati / psc-wvaw-fayette-13m / foster-care-5700 / fitch-lottery-bonds-aa-minus** — ran. **marshall-fifth-year-judge / dna-grant-582k / caserta-retires / wish-academy-forum / remington-place / vienna-parental-leave** — alternates. **cabell-false-swearing-convictions / hatfield-mccoy-tornado-40-miles / chemours-pfas-class-action / gauley-fest-opens** — regional. **us-7-closure-sept-19** — away. **webster-grand-jury-12 / pender-partf-500k** — hotspots. **fema-answer-morrisey / hens-vote (ninth morning) / bennington-drug-bust / option-tax-survey / bergoo-utv / webster-memorial-administrator** — alternates.
- **uhnbc-helipad-ubcm / fsj-monk-death-suspicious / eby-oates-campaign / rattee-caucus-divided / trump-procurement-memorandum / carney-european-parliament** — ran. **scott-not-running / northern-lights-omineca / quesnel-stabbing / pg-vancouver-rail / cobb-williams-lake / tumbler-ridge-letter / eby-doctors-1m / ex-ags-treaties / unifor-brampton / quebec-second-debate / canada-jef / lawzero-150m / point-lepreau / pearson-heist-charges** — alternates.
- **ussf-259-launched / lro-mcgetchin-crater / mount-sinai-wildfire-smoke / base-antiprotons-trucked** — ran. **stanford-levetiracetam-dmg / wwa-nepal / wmo-1400-gigatons / city-of-hope-87 / uc-davis-41 / congo-ebola-7258** — alternates.
- **ratepayer-protection-act-417-3 / openai-six-misalignment-reports / wesleyan-164-ai-ads** — ran. **irregular-qwen-self-modify / pittman-apple-deadline / sanders-casar-bill (not introduced)** — alternates.
- **carabao-draw-liverpool-chelsea / burrow-limited-back / reds-6-2-dodgers-snell / browns-teven-jenkins-dnp / crew-2-1-orlando-open-cup-final / marshall-del-rio-wilson-back / ohio-hauser-south-alabama / brewers-5-4-pirates-yelich / wvu-strachan-debut** — ran. **fcc / spurs / usmnt / hannan** — sat out. **hannan-westside / hannan-point-jv** — still owed; tonight's Westside result is Friday's item.
- **aki-day5-mitoumi-kotozakura / aki-day5-onosato-kirishima-atamifuji / aki-day6-card / guardians-6-3-white-sox-sole-lead / cubs-8-4-braves-pca-44 / twins-5-4-yankees-13 / darnold-out-lock / murray-limited / brighton-3-2-man-utd / everton-1-0-wolves-roundup / ncaa-michigan-clock-error** — ran. **orioles-7-1-mets / padres-9-3-rockies-salas / belichick-wsj / mason-ir** — held.
- **youth-waterfowl-sept19 / bear-gun-sept19-25 / archery-sept26 / regular-goose-oct3 / squirrel-day-6 / dove-day-17 / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead** — ran; **going_out empty**. **gauley-window-2-friday / gauley-fest-opens / stocking-none / mon-nf-nothing-new** — seasons note. **williams-58-8-falling / point-pleasant-24-92-flag-wrong / huntington-26-48-falling / no-beach-hazards / nhc-al98-40-40 / moon-5-5-days** — water block.
- **sportsman-index-stale-no-12** — for Nate (No. 34 computed from the edition files). **fetch-fishing-24h-window-bug** — for Nate (Point Pleasant flag wrong today). **direction-gate-bare-edge** — for Nate. **ncz106-pender** — for tomorrow's outdoors brief. **detached-head-twentieth** — recurring.

### Covered slugs, 2026-09-17

`fed-hike-quarter-point-3-75-4-warsh-12-0`, `johnson-recess-house-hegseth-impeachment`, `russia-sanctions-bill-house-262-159`, `sharifullah-20-years-abbey-gate`, `navajo-nation-flash-flood-3-dead-newcomb`,
`ukraine-strikes-10-dead-five-oblasts`, `thaci-25-years-kosovo-chambers`, `gaza-city-al-saada-collapse-21`, `sudan-al-zara-mine-toll-82`,
`wv-data-centers-water-preservati-hb2014`, `psc-wvaw-fayette-three-psds-13m`, `wv-foster-care-5700-helton`, `fitch-wv-lottery-bonds-aa-minus`,
`cabell-former-candidates-false-swearing`, `hatfield-mccoy-tornado-five-miles`, `wood-county-chemours-pfas-class-action`, `gauley-fest-opens-summersville`, `us-7-closure-bennington-sept-19-oct-3`, `webster-grand-jury-indicts-12-sept-9`, `pender-partf-500k-abbey-preserve`,
`uhnbc-helipad-ubcm-sampson`, `fsj-dayna-monk-death-suspicious`, `eby-oates-campaign-manager`, `rattee-conservative-caucus-divided`, `trump-memorandum-canadian-goods-procurement`, `carney-european-parliament-trump-hostile-act`,
`spacex-ussf-259-launched-b1097`, `lro-mcgetchin-crater-728-ft`, `mount-sinai-wildfire-smoke-lancet-oncology`, `base-antiprotons-trucked-cern`,
`ratepayer-protection-act-417-3`, `openai-six-misalignment-reports-register`, `wesleyan-164-ai-political-ads`,
`carabao-fourth-round-liverpool-chelsea`, `burrow-limited-back-houston`, `reds-6-2-dodgers-snell-groin`, `browns-teven-jenkins-dnp`, `crew-2-1-orlando-open-cup-final-oct-21`, `marshall-del-rio-wilson-expected-back`, `ohio-hauser-south-alabama-run`, `brewers-5-4-pirates-yelich-double`, `wvu-strachan-possible-debut`,
`aki-day5-mitoumi-beats-kotozakura-nine-tied`, `aki-day5-onosato-kirishima-atamifuji-win-aonishiki-loses`, `aki-day6-card-onosato-gonoyama`, `guardians-6-3-white-sox-sole-lead`, `cubs-8-4-braves-crow-armstrong-44`, `twins-5-4-yankees-13-innings`, `seahawks-darnold-out-lock-starts`, `vikings-murray-limited-protocol`, `brighton-3-2-man-utd-carabao`, `everton-1-0-wolves-villa-fleetwood`, `ncaa-michigan-wmu-clock-error`,
`youth-waterfowl-sept19`, `bear-gun-sept19-25`, `archery-sept26`, `regular-goose-oct3-splits`, `squirrel-day-6`, `dove-day-17-rails-snipe`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish`, `black-drum-sheepshead`,
`gauley-window-2-sept-18-21-nps`, `gauley-fest-sept-17-20`, `stocking-none`, `williams-58-8-falling`, `point-pleasant-24-92-flag-wrong-up-0-30`, `huntington-26-48-falling`, `no-beach-hazards-pender`, `nhc-al98-40-40`, `moon-5-5-days-waxing`, `topsail-fp-sept1-sixteen-days`

## 2026-09-18 — No. 45 (Times) and No. 35 (Sports & Sportsman)

| Open-ended | **Twenty-fourth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water), launched 5:35, filed between 5:38 and 5:46 a.m. ET. The Times validated at 5:46 (art caption twice over 140 chars, cut), Sports & Sportsman at 5:47 after three gate hits (Marshall's "28-26" in a non-game brief, the White Sox and Mets records read as the Cubs' by the standings gate — all reworded to words), both rendered and **pushed at 5:47:47 a.m. ET** (commit f30a750), 18 minutes after the 5:30 wake. Digest dry-run 1,085 embed chars, hero attached (81 KB). The 6:50 `send_later` wake was armed at 5:37 (trig_017qjhkZySqdM31FScvAkNTL) to run the post in the foreground with `--not-before 07:00`. **Detached HEAD at session start again — twenty-first occurrence**; `git reset --hard origin/main` on main fixed it. `config.head_start_minutes` reads 90 | **standing practice / OPEN — recurring** |
| Open-ended | **Setup: pip installed Pillow on the first try. All three fetchers clean on the first run** — stats 4 entries (S&P 7,637.76 +1.14%, Dow 51,778.04 +0.61%, Nasdaq 26,418.30 +1.69%, Bitcoin $78,096 +1.92%); fishing 4 waters, 0 errors; standings 5 clubs (Pirates 76-77 third, 19.0 back, 8.0 out; Reds 71-82 fifth, 24.0 back, 13.0 out). **The fetcher's 48-hour "24h ago" artifact is present on all three USGS gauges (Wednesday 5:45 a.m.) but every direction flag happens to agree with the true 24-hour trace today**; the water block names the Wednesday comparison points and the Thursday deltas | **fetch-fishing-24h-window-bug — still for Nate** |
| Open-ended | **The lead is the U.N. fact-finding mission's "reasonable grounds" finding that the U.S. committed war crimes in the Feb. 28 Minab school and Lamerd strikes, 178 civilians, White House "unserious nonsense."** AP via NPR (curl; NPR WebFetch 503 twice), Al Jazeera, CBS live updates. 168 school dead is Iranian state media's figure and labeled; CENTCOM's Lamerd denial carried; report to the Human Rights Council Monday. Held: NBC's Pentagon-weighs-25,000-troop Europe cut (one outlet, unnamed officials); Trump's "big decision" line (Axios-sourced, blocked). U.S.: Schroyer ICE nomination withdrawn (AP via NPR); Alsheikh 60 years in L.A. (Al Jazeera — age and hometown dropped, snippet-only); stocks rally and oil under $100 a day after the hike (NBC); Texas Guard F-16 down near Grawn, Mich., pilot ejected (ABC). World: Russia's three-day Duma vote, Yabloko barred (Kyiv Independent); IRGC says it hit a Togo-flagged tanker in Hormuz, UKMTO confirms a hit, no ship name anywhere (Times of Israel liveblog); 37 mining suspects dead in a Minna cell, cause contested and attributed (AFP via France24); Banga, South Cotabato school shooting, 3 dead (Al Jazeera). **Sweden final still not out (weekend); Rwanda-DRC Geneva no outcome; Sudan toll still 82** | **watch: Sweden final; HRC presentation Monday; Russia Duma result Sunday/Monday; BOJ 1.25% hike (held, date needed corroboration); Haiti Kenscoff report; Trump-Xi ~Sept. 24; Rwanda-DRC** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** NPR's og:image (AP, Vahid Salemi) is a Tehran street: a sculpted fist rising from a stylized feather over a ring of triangular flags on a plinth, a tarpaulin fence strung with lantern bulbs, a metal wall of small posters, young trees, apartment and office blocks and a cell tower at left, three motorcyclists in the foreground. Drawn as `scratchpad/draw.py` (379 paths, 42 KB) with the riders as faceless silhouettes and the posters as blank rectangles. **Chromium headless clipped the raster at row 412 twice while the SVG ran to 493 — cairosvg (pip) rendered it whole; use cairosvg to look at drawings, not the chrome screenshot flag.** Seventh rung-1 drawing in a row | |
| Open-ended | **Notebook: 4 statewide, 3 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley), away 1, hotspots 2 — six lines.** Statewide: Morrisey's Mason County state of emergency, 900 cubic yards of bank within two feet of a rail line near Point Pleasant, 30-day order Thursday (WCHS; WSAZ same); Black Diamond Utilities formed July 2 at Black Diamond Power's Mullens address ahead of Monday's PSC receivership hearing (WVVA); PSC final approval of the $11.4M Olcott waterline, ~110 Kanawha homes, bids October (WSAZ); McMahon at the Woody Williams Center in Barboursville, a dozen protesters (Herald-Dispatch). Regional: Milton Hope Gas bills $670 to $1,000-plus, estimated readings (WCHS); Kanawha sheriff's $2M training-center groundbreaking at Camp Virgil Tate (WSAZ); Wood County assessor audit, ~$357,000 shortfall, no theft (WTAP). **Empty: nicholas_webster** (Register-Herald, WVVA, Hinton News, Echo front — nothing dated beyond Gauley Fest, which ran yesterday) **and summers_new_river** (Hinton News courthouse records and reprints only). Away: North Bennington trustees adopted the short-term-rental enforcement policy last week, $100 registration by July 1 (Banner, Sept. 16). Cabin: **the desk first filed the Red Oak Fire Tower line, which was the 09-15 cabin line — caught at the editor's desk and swapped** for the Webster County Fair, Sept. 9-12 at Camp Caesar with its first ATV rodeo (Echo, Monday). Topsail: NTB public hearing Tuesday 6 p.m. on the Corps draft EIS for New River Inlet shore protection, comments to Oct. 19 (town civicalert, Sept. 8). Held: Huntington Flock ordinance approved Sept. 14 (too old); Parkersburg Holiday Hills sinkhole (no incident date); Bennington drug bust, option-tax survey; Bergoo UTV crash; Webster Memorial administrator; Surf City JH Batts addendum; Pender immunization clinic Sept. 22; DNA grant, Caserta, WISH forum, Remington Place, Vienna leave, Marshall judge. **FEMA still unanswered (Gazette-Mail Sunday committee piece); hens vote tenth morning no result.** MetroNews 403 seventh morning; Topsail Beach town news 404 today; Gazette-Mail via curl | **watch: FEMA answer; Black Diamond PSC hearing Monday; NTB EIS hearing Tuesday; Devine prelim Sept. 23; Caserta seat Sept. 24; HB 2014 rules Sept. 28; Putnam commission Sept. 29; hens** |
| Open-ended | **Canada 2/2/2.** PG: TSB says the Aug. 20 Foothills Boulevard King Air crash probe could take 450 days, one engine loss cited (CBC); Gary Jamieson runs for RDFFG Area F as Kevin Dunphy retires after 18 years (CKPG). BC: Conservative president says ex-executive director Elaine Allan hired a private investigator on about a dozen people including four MLAs, Findlay says no knowledge (CBC; CHEK says 14 — CBC's figure used, attributed); B.C. adopts "PCT" as the time-zone code ahead of no fall-back, Manitoba permanent daylight time the same day (CHEK). Canada: **Carney moved** — told the European Parliament Canada and Europe are "not fair-weather allies," Parliament will vote on the final alliance, Canada-EU summit Montreal Oct. 29-30 (CP via CHEK; Global transcript); **N.L. Churchill River vote moved** — passed Thursday night, all 20 PCs plus independent Joyce for, 15 Liberals, 2 NDP and Russell against, Innu Nation asked for a no (CBC NL; the 21-18 in the headline is the sum of CBC's stated breakdown). Held: UHNBC helipad rooftop $50M v. ground $5M (promotable); Findlay "not going anywhere," Ipsos 35%; Eby UBCM speech today; Fort St. John/Fort Nelson timber reviews; Unifor-Stellantis impasse; Alberta 509,000 mail ballots; Nackawic mill 228 layoffs; spotted lanternfly first Canada detection. **My PG Now back to Cloudflare 403; iNFOnews stub; CBC via RSS + article curl** | **watch — Eby UBCM speech; Unifor-Stellantis Sept. 20; Findlay byelection Sept. 26; PG vote Oct. 17; Canada-EU summit Oct. 29-30** |
| Open-ended | **Sumo, Aki Day 6 — JSA English leaders page (sumo.or.jp), Sports Nippon/Nikkan/Hochi copies on Yahoo Japan, Sportsnavi Day 7 card; r/Sumo login-walled, JSA torikumi pages JS-only.** **Seven share the lead at five-and-one: Onosato, Kotozakura, Atamifuji, Churanoumi, Asanoyama, Ura, Toshinofuji; nobody unbeaten.** Onosato slapped down Gonoyama; Kotozakura thrust out Takanosho; **Kirishima thrown by winless Yoshinofuji, four-and-two; Aonishiki forced out by Fujinokawa, third straight loss, three-and-three.** Kyujo: Hoshoryu, Wakatakakage, Wakanokatsu. **Day 7: Aonishiki v Atamifuji, Onosato v Churanoumi, Kotozakura v Fujiryoga, Kirishima v Gonoyama, Fujinokawa v Daieisho, Toshinofuji v Oho.** **CORRECTION for the record: yesterday's No. 34 named the maegashira who beat Kotozakura on Day 5 "Mitoumi"; 美ノ海 is Churanoumi (JSA English page). Logged in FAILURES.** Records in words; no `result` on sumo briefs | **Day 7 results Saturday; seven-way tie** |
| Open-ended | **Our Teams: 9 briefs, 5 outlets.** Alonso rules nobody out for Brentford tonight (chelseafc.com, Thursday presser); Burrow limited a second day, Perine out (bengals.com); **Dodgers 8-2 Reds, Singer 7 runs** (CBS box, Stats API gamePk 824464); Tyson Campbell misses Browns practice, ankle (Buccaneers' club report, PFT corroborated); FCC sign 16-year-old GK Connor Dale as a Homegrown (club); Del Rio-Wilson and Bausley back atop Marshall's depth chart (H-D via curl after a 429) — **"28-26" in a non-game brief tripped the result gate, reworded to "two-point win"**; **Pirates 7-4 Brewers, five-run second** (CBS box, gamePk 823334); Pochettino names 28 for Peru and Chile (ussoccer.com, posted Thursday); WVU defense v. Virginia's line averaging 24 years and 11,000 snaps (Dominion Post). Standings: MLB byte-matched; PL unchanged (Chelsea 7 sixth, Liverpool 6 eighth, Spurs 2 17th); Bengals 1-0 "listed second, level with Baltimore and Pittsburgh" (CBS order); Browns 0-1 fourth; FCC 32 ninth, Crew 23 13th; WVU 2-0, Marshall 1-1, Ohio 1-1; Hannan 1-2 per MaxPreps. Upcoming 27 lines Sept. 18-25, MLB from the Stats API. **Fox Sports rendered every kickoff in UTC this morning** (WVU "11:30 PM ET") — college times from CBS Sports and the H-D, MLS from Fox converted. Sat out: Hannan (no outside score for Westside; **MaxPreps now lists a Sept. 21 Westside-at-Hannan 6:30 match not in the coach's doc — not printed; worth asking Ian**), Liverpool (Iraola presser 8:30 a.m. ET), Tottenham (site JS-only), Crew (Crew 2 signing only), Ohio (ohiobobcats.com 403), Spurs (offseason). **Thomas hearing outcome unreported anywhere; Chambers hearing Sept. 24 (SI snippet, not opened)** | **Hannan-Westside result; Sept. 21 MaxPreps fixture question for Ian; Thomas hearing; Chelsea at Brentford 3 p.m. ET** |
| Open-ended | **Leagues: 9 briefs.** Sumo 3; NFL: **Bills 41-31 Lions opening the new Highmark Stadium**, Allen 3+2 TDs, Cook 135, Goff 327/4 (CBS box; NFL.com's "27-7 halftime" conflicted with the box, no halftime score printed); DJ Moore shoulder + Jordan Mason IR (NFL.com). MLB: **White Sox 3-1 Tigers, even with the idle Guardians** (CBS box — "78-75" cut at the editor's desk because the standings gate read "Chicago" as the Cubs); Phillies 3-0 Mets, Nola 7 IP, tied with the Cubs for the top NL wild card (CBS box — the 85-68/69-84 records cut for the same gate). Europa League matchday 1: Palace 4-0 Lech, Bournemouth 2-1 at Sociedad, Ferencvaros 3-1 at Celtic (Sky, curl; **no followed club in Europe Thursday** — a snippet claiming Liverpool v Lech was wrong). NCAA: Pitt 27-13 Syracuse, Angeli benched (SI, answered today). Held: Belichick WSJ; Orioles-Mets, Padres-Rockies (Wednesday); Red Sox 4-3 Rangers; Sunderland 1-0 AZ (fan site only); Dickerson IR | **standings-gate — any "Chicago" + record reads as the Cubs; keep records out of Leagues briefs** |
| Open-ended | **Outdoors: all four waters.** Williams 56.2 cfs / 1.35 ft FALLING, back at its pre-rain base (58.8 → 56.2 at this hour), flag agrees; no gauge temperature. Point Pleasant 25.03 RISING, up 0.11 in 24 hours off a 24.57 low at 9 p.m., on the NWPS curve; Huntington 26.05 FALLING, down 0.43, the low of the two-day trace, 0.3-0.4 under its curve. Topsail: all four sound events inside today (H 1:56 AM 3.2, L 8:02 AM 0.9, H 2:31 PM 4.0, L 9:03 PM 1.4), 81.1F Beaufort, **moon first quarter, 41%, 6.5 days — neaps**; no NWS alerts in NC, Coastal Pender (NCZ106) rip LOW, surf 1-3 ft; **NHC AL98 down to 10/10, "increasingly unlikely"**; WV's only product a 5:08 Special Weather Statement for a storm line through Mason/Jackson/Wood/Putnam to 6 a.m. **Fisherman's Post still Sept. 1, 17 days old.** Seasons: youth waterfowl tomorrow (1 day); bear gun Sept. 19-25 selected counties; archery Sept. 26 (8); regular goose/duck Oct. 3 (15, kept at the edge); squirrel Day 7; dove Day 18, 23 left; **going_out empty** with the note explaining why; Gauley Fest Day 2 and the second release window (18-21) from AW and NPS; Mon NF alerts page moved to `/r09/monongahela/alerts`, nothing since Sept. 14; stocking silent; migratory PDF downloaded with verification at 5:39 and read with PyMuPDF (pip-installed this morning); WV reference valid through 2027-06-30. **The NCDMF limits URL in the desk prompt 404s; the `rules-proclamations-and-size-and-bag-limits` path works** | **watch — Gauley window through Monday; youth waterfowl Saturday; Day 7** |
| Open-ended | **Sci/Tech and AI.** LATA trial, two-month HIV shots 1% v. 6% rebound at 96 weeks, 476 adolescents, Lancet (Medical Xpress); Leopardus tilcayo, first new wildcat species in a century, Current Biology (Phys.org); Stanford quantum jump in sound, Science (Phys.org); NASA picks Falcon 9 Bandwagon for StarBurst, NET 2028 (NASA). AI: **Pittman moved** — reviewed the X/SpaceXAI-Apple settlement in camera, denied OpenAI access, more time for summary judgment (9to5Mac); Air's Plugin4Shell SHA-pinning bypass in Claude Code, Codex, Gemini CLI, Copilot, two patched, attributed to the firm (Register); unsealed NYT v. OpenAI filings, Hecht's 2023 "largest theft of labor" memo (TechCrunch). Held: Hinton at Sanders' private Hill briefing (NBC, ready swap); **Sanders/Casar bill still not introduced**; FAA SMART $875M (secondhand); Anthropic "Claude builds successor" (vendor claim); Crusoe $3.9B (funding). NPR tech and world sections 503 | **watch — Sanders/Casar bill week of Sept. 21; HRC Monday** |
| Open-ended | **Source status.** OPEN: NBC, NPR (curl only; WebFetch 503), PBS, Al Jazeera, ABC (301 to abcnews.com), CBS, Kyiv Independent, Euronews (WebFetch), France24, Times of Israel, NASA, Spaceflight Now, EurekAlert browse, Phys.org, Medical Xpress, Register, TechCrunch, 9to5Mac, 404 Media, WSAZ, WCHS, WTAP, WVPB, WVVA, Herald-Dispatch (curl after 429), Dominion Post, Hinton News, Register-Herald front, WOAY tags, Gazette-Mail (curl), The Webster Echo (WebFetch), Bennington Banner, American Whitewater, Pender County, Surf City civicalerts, NTB /CivicAlerts.aspx and /m/newsflash, CKPG, CBC (RSS + article curl), CHEK, Global, Sportsnavi, Yahoo Japan copies, **sumo.or.jp English leaders page**, CBS boxes, MLB Stats API, ussoccer.com, bengals.com, buccaneers.com, chelseafc.com, liverpoolfc.com, nba.com/spurs, Sky (curl), NFL.com, NBC/PFT, **SI (answered today)**, MaxPreps, USGS, NWPS, api.weather.gov, ILM SRF, NHC, NCDMF, NPS, WVDNR MigBird PDF (curl, verified), Fisherman's Post feed (WebFetch). BLOCKED: **WV MetroNews (seventh morning)**, Topsail Beach news (404 today), My PG Now (Cloudflare 403 again), iNFOnews (stub), PG Citizen, EurekAlert search (404), CIDRAP topic page (nav only), NPR world/tech sections (503), Daily Orange (403), old.reddit r/Sumo (login wall), JSA torikumi (JS), ESPN, tottenhamhotspur.com (JS), ohiobobcats.com (403), wvillustrated.com (DNS), mydailyregister.com (000), Fox Sports (answers but times in UTC) | **watch — MetroNews; Fox UTC times; r/Sumo** |
| Open-ended | **Traps dodged.** (1) Cabin line was the 09-15 fire-tower rerun — swapped. (2) "Mitoumi" is Churanoumi — corrected today, logged. (3) Al Jazeera's Sept. 18 UTC stamp on the Alsheikh sentencing — DOJ/AP say Thursday. (4) 178 is the mission's total, 168 Iranian state media's — both labeled. (5) No ship name in the Hormuz strike — none written. (6) Nigeria cause of death contested — both attributed. (7) BOJ hike copy dated the decision to a Thursday — held. (8) Fox kickoff times in UTC — CBS/H-D used. (9) Snippet said Liverpool v Lech — false. (10) Guardians "won Thursday" snippet — idle. (11) NFL.com halftime v. CBS box — none printed. (12) Marshall 28-26 in a depth-chart brief — words. (13) White Sox/Mets records read as the Cubs' by the gate — cut. (14) Art caption 168 and 142 chars — cut to 133. (15) NCDMF URL 404 — yesterday's path. (16) MaxPreps' Sept. 21 Hannan fixture not in Ian's doc — not printed | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-18** | **Aki Day 6 (ran); Chelsea at Brentford 3 p.m. ET; Reds v. Cubs, Pirates v. Royals 6:40; second Gauley window opens (18-21); Eby UBCM speech; Iraola presser 8:30 a.m. ET; Russia Duma vote opens (to Sunday)** | |
| **2026-09-19** | **Aki Day 7 (Aonishiki v. Atamifuji, Onosato v. Churanoumi); WV youth waterfowl day; bear gun second window (19-25, selected counties); U.S. 7 closes Exit 2-3 Bennington (to Oct. 3); Lake Paran stone-skipping; Spurs v. Villa 7:30 a.m. ET; Marshall at Missouri State 6:30, Ohio at South Alabama 7, WVU v. No. 25 Virginia 7:30; Crew at Montreal 7:30, FCC at Houston 8:30** | |
| **2026-09-20** | **Bournemouth v. Liverpool 9 a.m. ET; Bengals at Houston, Browns at Tampa Bay 1 p.m.; Pirates v. Royals 1:35, Reds v. Cubs 1:40; Unifor-Stellantis 11:59 p.m.; Gauley Fest closes; Russia Duma vote closes; Sweden final count expected** | |
| **2026-09-21** | **U.N. mission presents its Iran report to the Human Rights Council, Geneva; PSC Black Diamond Power receivership hearing; MaxPreps lists Westside at Hannan 6:30 (NOT in the coach's doc — confirm)** | |
| **2026-09-22** | **NTB public hearing on the New River Inlet draft EIS, 6 p.m. (comments to Oct. 19); Hannan at Calvary 6 p.m. (venue unconfirmed); Parkersburg full council; Pender immunization clinic; Reds at Braves 7:15, Pirates v. Cardinals 6:40** | |
| **2026-09-23** | **Devine preliminary hearing; third Quebec debate** | |
| **2026-09-24** | **Cabell commission votes on the clerk's seat; Hannan v. Roane at Ashton 6 p.m.; WVU Chambers eligibility hearing (SI snippet); Trump-Xi summit window** | |
| **2026-09-26** | **WV archery/crossbow deer and bear open; USMNT v. Peru; Findlay byelection** | |
| **2026-09-28** | **HB 2014 data-center rules hearing; NBA media day; Surf City e-bike focus group 6-8 p.m.** | |
| **2026-09-29** | **Putnam County Commission on the data-center resolution; NBA camps open; Hannan at Roane 6:30; USMNT v. Chile 8 p.m. ET** | |
| **2026-10-03** | **WV regular goose and duck seasons open; U.S. 7 reopens** | |
| **2026-10-05** | **Quebec general election** | |
| **2026-10-17** | **PG and Quesnel civic elections, RDFFG Area F; WV bear youth second window (17-18)** | |
| **2026-10-21** | **U.S. Open Cup final, Crew v. St. Louis City, Columbus** | |
| **2026-10-23** | **Cabell false-swearing sentencing** | |
| **2026-10-29** | **Canada-EU summit, Montreal (29-30)** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |

### Open threads

- **un-mission-iran-war-crimes-178** — led; the HRC presentation Monday and any Pentagon inquiry release are the follow-ups. **schroyer-ice-withdrawn / alsheikh-60-years / stocks-rally-oil-under-100 / texas-f16-michigan** — ran. **pentagon-europe-25000 / trump-big-decision-iran / iranian-unga-visas / saudi-f35-24-3b** — alternates.
- **russia-duma-vote-yabloko / irgc-togo-tanker-hormuz / minna-custody-37-dead / banga-school-shooting-3** — ran. **sweden-final (weekend) / lecornu-54b-cut / ceuta-migrants / boj-1-25 / haiti-kenscoff-164 / rwanda-drc-geneva / sudan-mine-82** — alternates.
- **mason-county-emergency-levee-slide / black-diamond-utilities-psc / olcott-waterline-11-4m / mcmahon-woody-williams** — ran. **huntington-flock-approved / holiday-hills-sinkhole / dna-grant / caserta / wish-forum / remington-place / vienna-leave / marshall-judge** — alternates. **milton-hope-gas-bills / kanawha-sheriff-training-center / wood-assessor-audit** — regional. **north-bennington-str-policy** — away. **webster-county-fair-atv-rodeo / ntb-eis-hearing-sept-22** — hotspots. **fema-answer / hens (tenth morning) / bennington-drug-bust / option-tax / bergoo-utv / webster-memorial / red-oak-fire-tower (RAN 09-15, do not re-run)** — alternates.
- **tsb-pg-crash-450-days / jamieson-area-f / bc-conservatives-private-investigator / bc-pct-time-zone / carney-eu-parliament-vote / nl-churchill-vote-passed** — ran. **uhnbc-helipad-costs / findlay-ipsos-35 / eby-ubcm / timber-reviews / unifor-stellantis / alberta-mail-ballots / nackawic-228 / spotted-lanternfly** — alternates.
- **lata-hiv-shots / leopardus-tilcayo / stanford-quantum-jump-sound / starburst-falcon-9** — ran. **hinton-sanders-briefing / faa-smart / sanders-casar-bill (not introduced)** — alternates.
- **pittman-settlement-in-camera / plugin4shell / hecht-memo-nyt-openai** — ran.
- **alonso-brentford-squad / burrow-limited-perine / dodgers-8-2-reds-singer / browns-tyson-campbell / fcc-connor-dale / marshall-depth-chart / pirates-7-4-brewers / usmnt-28-roster / wvu-virginia-line** — ran. **hannan / liverpool / tottenham / crew / ohio / spurs** — sat out. **hannan-westside / hannan-point-jv / hannan-sept-21-maxpreps** — owed.
- **aki-day6-seven-tied / aki-day6-kirishima-aonishiki-lose / aki-day7-card / bills-41-31-lions-highmark / moore-shoulder-mason-ir / white-sox-3-1-tigers-even / phillies-3-0-mets-nola / europa-md1-palace-bournemouth / pitt-27-13-syracuse** — ran. **belichick-wsj / red-sox-4-3-rangers / padres-9-2-rockies / dickerson-ir** — held.
- **youth-waterfowl-sept19 / bear-gun-sept19-25 / archery-sept26 / goose-duck-oct3 / squirrel-day-7 / dove-day-18 / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead** — ran; **going_out empty**. **gauley-window-2-open / gauley-fest-day-2 / stocking-none / mon-nf-alerts-moved** — seasons note. **williams-56-2-falling / point-pleasant-25-03-rising / huntington-26-05-falling / no-nc-alerts / nhc-al98-10-10 / moon-first-quarter** — water block.
- **sportsman-index-stale-no-12** — for Nate (No. 35 computed from the edition files). **fetch-fishing-24h-window-bug** — for Nate (flags right today by luck). **standings-gate-chicago** — for Nate (any "Chicago" + record reads as the Cubs). **mitoumi-churanoumi-correction** — logged. **detached-head-twenty-first** — recurring.

### Covered slugs, 2026-09-18

`un-mission-reasonable-grounds-us-war-crimes-iran-178`, `trump-withdraws-schroyer-ice`, `alsheikh-60-years-adra-torture`, `stocks-rally-oil-under-100-after-hike`, `texas-guard-f16-crash-grawn-michigan`,
`russia-duma-three-day-vote-yabloko-barred`, `irgc-togo-tanker-hormuz-ukmto`, `nigeria-minna-custody-37-dead`, `philippines-banga-school-shooting-3`,
`morrisey-mason-county-emergency-levee-slide-rail`, `black-diamond-utilities-mullens-psc-hearing`, `psc-olcott-waterline-11-4m`, `mcmahon-woody-williams-center-protest`,
`milton-hope-gas-bills-estimated`, `kanawha-sheriff-training-center-camp-virgil-tate`, `wood-county-assessor-audit-357k`, `north-bennington-str-enforcement-policy`, `webster-county-fair-sept-9-12-atv-rodeo`, `ntb-new-river-inlet-eis-hearing-sept-22`,
`tsb-prince-george-crash-probe-450-days`, `jamieson-rdffg-area-f-dunphy`, `bc-conservatives-allan-private-investigator`, `bc-pct-time-zone-code`, `carney-eu-parliament-alliance-vote`, `nl-churchill-river-vote-passed-21-18`,
`lata-hiv-two-month-shots-lancet`, `leopardus-tilcayo-new-wildcat`, `stanford-quantum-jump-sound-science`, `nasa-starburst-falcon-9-bandwagon`,
`pittman-x-apple-settlement-in-camera-openai`, `air-plugin4shell-coding-agents`, `hecht-memo-largest-theft-of-labor-unsealed`,
`alonso-nobody-ruled-out-brentford`, `burrow-limited-second-day-perine-out`, `dodgers-8-2-reds-singer-7-runs`, `browns-tyson-campbell-ankle`, `fcc-connor-dale-homegrown`, `marshall-del-rio-wilson-bausley-depth-chart`, `pirates-7-4-brewers-five-run-second`, `usmnt-28-roster-peru-chile`, `wvu-virginia-line-24-years-11000-snaps`,
`aki-day6-seven-share-lead-five-one`, `aki-day6-kirishima-yoshinofuji-aonishiki-fujinokawa`, `aki-day7-card-aonishiki-atamifuji`, `bills-41-31-lions-highmark-opener`, `bills-dj-moore-shoulder-vikings-mason-ir`, `white-sox-3-1-tigers-even-guardians`, `phillies-3-0-mets-nola-wild-card`, `europa-md1-palace-4-0-lech-bournemouth`, `pitt-27-13-syracuse-angeli-benched`,
`youth-waterfowl-sept19`, `bear-gun-sept19-25`, `archery-sept26`, `goose-duck-oct3`, `squirrel-day-7`, `dove-day-18`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish`, `black-drum-sheepshead`,
`gauley-window-2-sept-18-21`, `gauley-fest-day-2`, `stocking-none`, `williams-56-2-falling`, `point-pleasant-25-03-rising`, `huntington-26-05-falling`, `no-nc-alerts-pender-low-rip`, `nhc-al98-10-10`, `moon-first-quarter-neap`, `topsail-fp-sept1-seventeen-days`

## 2026-09-20 — No. 46 (Times) and No. 36 (Sports & Sportsman)

| Open-ended | **Twenty-fifth morning under the digest contract, and the first after a two-day hole.** `editions/index.json` has no 2026-09-18 record and no 2026-09-19 anything: No. 45 and S&S No. 35 were built, validated, rendered and pushed on 09-18 (commits f30a750, a671431), the 6:50 `send_later` wake fired (trigger last_run SUCCEEDED at 10:51 UTC) and nothing followed it — no "Posted No. 45" commit, no index record, no weather-page commit that day either — and the 09-19 routine never ran at all. Whether the 09-18 digest reached Discord is unverifiable from here. Today's kicker carries the gap in one line. **Edition numbers were computed from the edition files (No. 46, S&S No. 36), not from the index (which says 45)**, because No. 45 is already published on the site and in the archive under that number; the validator warns and does not fail. Eight parallel desks launched 5:40, filed 5:42-5:54 a.m. ET; Times validated 5:44, S&S 5:50 after one gate pass (six leagues briefs and the Crew brief tripped the result-verb reader — it takes the FIRST listed verb in the whole text and the team whose FIRST mention is latest before it, so a second win verb in the summary flips a correct headline; one verb per game brief, loser named after it), both pushed **5:50:22 a.m. ET** (commit 86f83b5). Digest dry-run 1,080 embed chars, hero 86 KB. `config.head_start_minutes` reads 90 | **standing practice — the post is run in the FOREGROUND from this session with `hold_until.py` chunks, with a 7:04 `send_later` as backup only** |
| Open-ended | **Setup: pip installed Pillow first try; cairosvg pip-installed for viewing the drawing. All three fetchers clean** — stats 4 entries (S&P 7,650.50 +0.17%, Dow 51,682.64 -0.18%, Nasdaq 26,522.54 +0.39%, Bitcoin $80,349 -1.22%); fishing 4 waters, 0 errors; standings 5 clubs (Pirates 78-77 third, 19.0 back, 7.0 out; Reds 72-83 fifth, 25.0 back, 13.0 out). **The fetcher's comparison points landed on Saturday 9 p.m. readings this morning and every direction flag agrees with the two-day trace** — no 24h-window artifact to correct today | **fetch-fishing-24h-window-bug — still for Nate** |
| Open-ended | **The lead is the White House barring CNN, MS NOW and Politico** — Secret Service disabled or took the three correspondents' passes Saturday morning, a day after Trump announced it; NBC (primary), CBS (the 8 a.m. detail), Al Jazeera; PBS carries AP. Held: the U.S. Caribbean boat strike, 4 dead (CBS); the antitrust suit alleging AI labs agreed to slow development (AP via PBS); Iran conditions via Qatar ran in World instead. U.S.: Trump's "AI Force" and czar (Al Jazeera); 1st Circuit third-country deportation ruling (CBS); all 50 states in the Medicaid drug-pricing model, $529B a White House estimate (AP via PBS); wildfires 8.5M acres, most since 1983 (CBS). World: Kohat police compound attack, 31 per a police official via AFP, earlier counts 15 and 21 (France 24); Iran's conditions sent via Qatar, Rezaei to Al Jazeera; RNDDH's 164 for Kenscoff (Haitian Times); Moscow's largest drone attack, Russian-side figures only (France 24 live page). **Russia's Duma count due after 1800 GMT tonight; Sweden's final count was Thursday, 176-173, Andersson forming a government — not run, outside window; BOJ 1.25% confirmed Friday Sept. 18 (Al Jazeera), still an alternate** | **watch: Duma result; HRC presentation of the Iran report Monday; Iran-U.S. reply; AP press-pass case; Trump Gulf leaders Tuesday** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** NBC's og:image is the West Wing entrance from the drive: the flat-roofed portico on square columns, glass double doors under a fanlight, two ball topiaries in square planters, a Marine at attention beside the door, a long clipped boxwood hedge, a broadcast camera on a tall tripod with hanging cables dominating the right foreground, a folding music stand on the asphalt, the EEOB with rows of windows and a vertical flag behind an iron fence. `scratchpad/draw.py`, 156 paths, 38 KB, guard and the fence-walker as featureless contours. **First pass came out at 779 paths and 69 KB — texture strokes folded into single multi-subpath elements got it under both caps without losing a mark; do that from the start.** Eighth rung-1 drawing in a row | |
| Open-ended | **Notebook: 4 statewide, 3 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley), away 1, hotspots 2 — six lines.** Statewide: legislative audit of the former arts agency, two funds over-encumbered by up to $2M, 72 grants unaccounted for, hearing Sept. 14, story Friday (WV Watch via its RSS — the site 403s WebFetch, the feed carries full text); $15M Educational Opportunity Centers grant for WV READY at all nine CTCs (WVVA); $6.3M Buffalo Bridge interchange, Routes 869 and 817, 37 crashes since 2019 (WSAZ); Capito co-sponsoring the Protect College Sports Act (WVPB). Regional: retired Judge Christopher Chiles died, per the Cabell prosecutor's statement (WSAZ, no date of death given — line hangs on the statement); Clean Seas pyrolysis forum Tuesday 6-8 at Belle Town Hall (WV Watch); Wood County grand jury, 96 indicted incl. a murder charge (News and Sentinel). **Empty: nicholas_webster** (Echo's newest posts Sept. 14 and all deduped or older; Chronicle still May; WOAY/WVVA/R-H nothing dated) **and summers_new_river** (Hinton News 503 twice, connection reset on curl; nothing elsewhere). Away: the Bennington drug-and-gun ring supervisor, 22, sentenced Sept. 8 in Rutland to 12 years (Banner) — the desk's first choice was a Sept. 2 preview of the Sept. 13 block party, swapped at the editor's desk for a post-event fact. Cabin: Dalila Miller named associate administrator at Webster Memorial after Dempsey left Aug. 31 (Echo, Sept. 14 — the `webster-memorial` alternate, now run). Topsail: Haywood life sentence for the 2022 Surf City hemp-shop killing, Friday (WECT) | **alternates: NB DRB meets Wednesday Sept. 23; Webster Springs junior firefighters' stair climb Sept. 11; Topsail High sophomore struck on U.S. 17 Thursday (stable); Surf City Batts path Segment 5 addendum Sept. 9; four Kanawha deputies sworn Thursday; Huntington Middle/Southside diesel-odor closure Friday; Caserta retiring Oct. 1 (H-D, undated page); Huntington Flock ordinance** |
| Open-ended | **Canada 2/2/2.** PG: rail alliance's $600K corridor-study ask at UBCM, Klassen for co-governance (CKPG); $700K year-round Rainbow Park washroom (CKPG). BC: **Conservatives expel Rustad, Rattee and Halford** — clerk's office Sept. 18, Rattee says 10 MLAs want Findlay out, Rustad presser Monday in Victoria (CBC); **Eby at UBCM** — Oct. 1 PST extension to professional services deferred, B.C.-built ferries, no election call (CBC). Canada: Hajdu's Labour Code bill to curb Section 107, due this week (CP via CKPG); Highwood UCP first of 22 associations seeking a Smith leadership review (CBC Calgary). Held: Penticton councillor guilty, seat vacant; Carney's Building Canada Strong Act; **Unifor-Stellantis deadline 11:59 p.m. tonight — latest copy Thursday**; Hotel Eldorado mediation offer; PG council candidate profiles (Radloff, Krause, Brennan). **My PG Now and PG Citizen 403; CHEK, CTV, Castanet, National Post not searched for time** | **watch — Unifor-Stellantis outcome Monday; Rustad presser Monday; Findlay byelection Sept. 26; Building Canada Strong Act tabling** |
| Open-ended | **Sumo, Aki Days 7-8 — JSA English leaders page and the torikumiAjax JSON behind the torikumi pages (the HTML renders empty without JS); Japan Times, Kyodo, NHK, Sportsnavi and r/Sumo not attempted for time.** **Onosato alone at seven and one after Day 8** (yorikiri over Takanosho); Day 8 Hakunofuji (1-6 arriving) oshidashi over Kotozakura, Churanoumi oshitaoshi over Kirishima, Aonishiki over Daieisho, Atamifuji over Kotoeiho, Fujinokawa over Takayasu, Toshinofuji over juryo visitor Mitakeumi. Day 7: Onosato over Churanoumi, Kotozakura over Fujiryoga, Aonishiki yorikiri over Atamifuji (skid ended), Kirishima tottari over Gonoyama, Shodai over Ura, Fujiseiun over Asanoyama, Oho over Toshinofuji, Fujinokawa over Daieisho. Chasers at six and two: Kotozakura, Atamifuji, Fujinokawa, Churanoumi, Asanoyama, Ura, Kinbozan, Toshinofuji; Kirishima and Aonishiki five and three. No kinboshi this basho. **The JSA absence page lists the East Maegashira 16 absentee as Wakanosho, not "Wakanokatsu" as the 09-18 ledger wrote — Wakanosho used today.** Day 9: Kotozakura v Fujinokawa (only chaser-v-chaser bout), Onosato v Fujiryoga, Churanoumi v Roga, Aonishiki v Yoshinofuji, Kirishima v Daieisho, Atamifuji v Takayasu. Records in words; no `result` on sumo briefs | **Day 9 results Monday; Onosato alone** |
| Open-ended | **Our Teams: 14 briefs, 9 outlets (Sky, Liverpool FC, Bengals, MLB Stats API, Browns, ESPN's site.api feed, Herald-Dispatch).** Brentford 3-0 Chelsea Friday (Anthony 61, Thiago 83, Carvalho 90+); Villa 3-2 Spurs on van Hecke's 98th-minute goal; Liverpool preview at Bournemouth 9 a.m. ET (Iraola quoted as Liverpool's manager on the club site); Burrow full practice, questionable; **Reds 6-4 Cubs Friday, Cubs 5-2 Reds Saturday; Pirates 8-5 and 6-5 Royals** (all Stats API decisions); Jenkins out, Campbell questionable; **Crew 2-0 at Montreal**; **FCC 2-2 at Houston**, Denkey 90+7 pen; **Marshall 30-24 at Missouri State** (H-D, headline only through curl — score from ESPN's feed); **South Alabama 41-36 Ohio**; **WVU 38-27 Virginia in Charlotte**. Standings: MLB byte-matched; PL from ESPN's standings feed — Chelsea 7 ninth (5), Liverpool 6 10th (4), Spurs 2 19th (5) — **Sky's table and premierleague.com rendered no rows to curl this morning; ESPN's site is blocked but site.api.espn.com answers**; FCC 33 ninth, Crew 26 13th; Bengals 1-0, Browns 0-1; WVU 3-0, Marshall 2-1, Ohio 1-2; Hannan 1-2 per MaxPreps. Upcoming 17 lines Sept. 20-27 incl. Hannan Sept. 22 at Calvary and Sept. 24 v Roane from the doc. **Chelsea's and Tottenham's next fixtures could not be confirmed (both out of the League Cup; Chelsea-Liverpool fourth round Oct. 28) — said so in the section note.** Sat out: Hannan (still no score for Sept. 17 at Westside; MaxPreps lists no such match on either page and still shows Westside at Hannan Monday Sept. 21 6:30 — **worth asking Ian**), Spurs, USMNT | **hannan-westside-score / hannan-sept-21-maxpreps — owed; Chelsea/Spurs fixtures — find a source that renders (premierleague.com API? club sites)** |
| Open-ended | **Leagues: 9 briefs.** Sumo 3; MLB: Mets 10-3 Phillies (Painter L), Guardians 12-6 A's (Cecconi W, a game up on the White Sox who beat Detroit 3-1 again), Padres 7-6 Marlins in 10 (Morgan W) — all from the Stats API day schedule with linescore and decisions; PL: Brighton 3-0 Arsenal (Arsenal's first loss, Brighton third), Coventry 1-0 at Forest (first points), Newcastle 2-1 Hull and Everton 1-0 Ipswich (Sky results page via curl). **No college football beyond the followed teams and no NFL brief**: CBS Sports' scoreboard came back as a 13 MB JS bundle and ESPN is blocked; SI and NBC not opened in time. **The standings feed marks Milwaukee as clinched but gives no date — not headlined.** Skubal listed as the Dodgers' winning pitcher, unchecked, not named | **standings-gate — records kept out of Leagues briefs again; a CFB roundup needs SI/NBC opened early** |
| Open-ended | **Outdoors: all four waters, and the morning's story is rain.** Williams **90.4 cfs / 1.58 ft RISING** from a 56.2 low at 9 p.m. Saturday, up hour by hour to the 5:15 reading, no crest yet, under a **Flash Flood Warning for Webster and Nicholas (and six more counties) until 8:45 a.m.**, one of five in WV at press time; the fetcher's "prime wading water" printed as written and the block says why it is not. Point Pleasant 25.56 rising, Huntington 26.31 rising; NWPS Huntington crest 27.1 ft about 8 a.m. Tuesday from a Saturday 10:18 a.m. forecast that predates the rain; **NWPS Point Pleasant gauge id would not resolve (PTPW2 and variants) — no crest printed.** Topsail: all four sound events inside today (H 3:30 AM 3.2, L 9:48 AM 0.9, H 4:11 PM 4.0, L 10:44 PM 1.3), 80.4F Beaufort, **moon waxing gibbous 62%, 8.5 days — springs building**; zero NC alerts, rip LOW through Wednesday, surf 1-3, TD Six near the Azores and no Atlantic formation expected for seven days. **Fisherman's Post still Sept. 1, 19 days old.** Seasons: **going_out has a row for the first time since the flounder closure — bear gun second window closes Friday Sept. 25, selected counties**; archery deer/bear/boar Sept. 26 (6 days); ducks and geese Oct. 3 (13) confirmed again from the migratory PDF (wvdnr.gov served it 200 over curl — the expired-cert note may be stale for that path); squirrel Day 9; dove Day 20, 21 left; **NCDMF footnote M re-read this morning: bluefish 3/day private, 5/day for-hire**; flounder closed since Sept. 15 in the note. Gauley: window 2 ends Monday, window 3 Sept. 25-28 (riverscout.app citing USACE — USACE 503, NPS 404, AW served the wrong river); Gauley Fest closes today. Mon NF nothing past Sept. 14. Stocking silent | **watch — Williams crest and the Webster warning; Gauley window 3 Friday; NWPS Point Pleasant id; Fisherman's Post October report** |
| Open-ended | **Sci/Tech and AI.** XRISM stellar wind onto GX 301-2, Science Advances (NASA); Y-chromosome loss gradient in 405 men, JCI Insight (Phys.org); Ervebo trial v. Bundibugyo, 20,000 health workers, Medical Xpress/AFP text dated "Saturday" — ran as Sept. 19; NASA's three more SpaceX crew flights, $946M (NASA). AI: Hacktron used Claude to reach OpenAI staff accounts, $6,500 bounty (TechCrunch); Census working paper CES-26-56, 5 points employment and 13% pay (census.gov); BAN's AI e-waste 395-617M tonnes (Register). Held: AI-fabricated report nearly triggering a U.S. operation on a Chinese ship (CNN 451, TechCrunch secondhand); Gemini breaching three firms in Irregular's tests; graphene Floquet state (Nature Physics); Progress 96 docked; Florida dengue death. **Nature (login redirect), Science (403), Ars, Verge, CNN blocked; Sanders/Casar bill still not introduced** | **watch — Sanders/Casar bill; Anthropic's response on Hacktron; CNN ship story if a readable outlet carries it** |
| Open-ended | **Source status.** OPEN: NBC, CBS, Al Jazeera, PBS, France 24, Haitian Times, Times of Israel liveblog, NASA, Phys.org, Medical Xpress, EurekAlert browse, Spaceflight Now, Register, TechCrunch, 404 Media, census.gov, WSAZ, WCHS, WVVA, WVPB, WOAY, Register-Herald, News and Sentinel, WV Watch (RSS only), Mountain State Spotlight, Gazette-Mail (curl), Herald-Dispatch (curl, no dates), Webster Echo (WebFetch and curl today), WECT, Pender/NTB/Surf City CivicAlerts, Bennington Banner article pages, VTDigger, village and town sites, CKPG, CBC (RSS + article curl), Global, JSA leaders + torikumiAjax + absence pages, MLB Stats API, site.api.espn.com (scoreboard and standings), Sky results (curl), MaxPreps, bengals.com, clevelandbrowns.com, liverpoolfc.com, ussoccer.com, USGS, NWPS (Huntington), api.weather.gov, ILM SRF, NHC, NCDMF, wvdnr.gov PDF, Fisherman's Post feed, Coastal Angler feed, fs.usda.gov alerts, riverscout.app, WV Explorer. BLOCKED: Politico, The Hill (403), NPR (curl gave no article links today), DW, Reuters/AP/BBC/Guardian (not tried), Nature, Science, Ars, Verge, CNN (451), WOWK (403), Dominion Post (404), WVU Today (403), Hinton News (503/reset), MetroNews (not tried, eighth morning), My PG Now, PG Citizen, Sky table/fixtures and premierleague.com (no rows), mlssoccer.com scores (404), chelseafc.com (header only), herdzone/wvusports (no content), ESPN site, CBS Sports scoreboard (JS bundle), USACE Summersville (503), NPS Gauley (404), American Whitewater Gauley URL (wrong page), NWPS Point Pleasant id | **watch — MetroNews; a PL fixtures source; NWPS PTPW2** |
| Open-ended | **Traps dodged.** (1) Away line was a Sept. 2 preview of a Sept. 13 event — swapped for a post-event sentencing. (2) Result-verb gate on six briefs with two win verbs — one verb per brief. (3) "Ukraine sends record drone swarm" headline on Russian-side figures — reworded to what Moscow reported. (4) Medical Xpress "Saturday, Sept. 20" — dated Sept. 19. (5) Skubal as Dodgers' winner unverified — not named. (6) Brewers clinch with no date — not headlined. (7) Boar's Feb. 5-7 window in the deer/bear row tripped the pamphlet gate — removed. (8) Bluefish 3/5 split confirmed on the page before printing. (9) Wakanokatsu/Wakanosho — JSA spelling used. (10) MaxPreps' Sept. 21 Hannan fixture — still not printed. (11) 779-path drawing — folded to 156. (12) Edition number from the files, not the stale index | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-20** | **Duma count after 1800 GMT; Unifor-Stellantis 11:59 p.m. ET; Bournemouth v Liverpool 9 a.m. ET; Bengals at Houston, Browns at Tampa Bay 1 p.m.; Pirates v Royals 1:35, Reds v Cubs 1:40; Gauley Fest closes; Aki Day 8 (ran)** | |
| **2026-09-21** | **Aki Day 9 (Kotozakura v Fujinokawa, Onosato v Fujiryoga); U.N. mission presents its Iran report to the HRC, Geneva; PSC Black Diamond receivership hearing; Rustad presser, Victoria; Gauley window 2 ends; MaxPreps' unconfirmed Westside at Hannan 6:30** | |
| **2026-09-22** | **Hannan at Calvary 6 p.m. (venue unconfirmed); NTB draft EIS hearing 6 p.m.; Belle pyrolysis forum 6-8 p.m.; Parkersburg full council; Reds at Braves 7:15, Pirates v Cardinals 6:40; Huntington NWPS crest 27.1 ft ~8 a.m.; Trump meets Gulf leaders, New York** | |
| **2026-09-23** | **Devine preliminary hearing; third Quebec debate; North Bennington DRB** | |
| **2026-09-24** | **Cabell commission on the clerk's seat; Hannan v Roane at Ashton 6 p.m.; Pirates v Cardinals 12:35** | |
| **2026-09-25** | **WV bear gun second window closes (selected counties); Gauley window 3 opens (25-28); Reds at Blue Jays, Pirates at Tigers** | |
| **2026-09-26** | **WV archery/crossbow deer, bear and boar open; USMNT v Peru 4:30 p.m. ET Orlando; Findlay byelection; Ohio v Stonehill 3:30, Marshall v Gardner-Webb 3:30, WVU v Oklahoma State 7; FCC at Montreal 7:30** | |
| **2026-09-27** | **Aki senshuraku; Crew v Inter Miami 7 p.m. ET** | |
| **2026-09-28** | **HB 2014 data-center rules hearing; NBA media day; Surf City e-bike focus group 6-8 p.m.** | |
| **2026-09-29** | **Putnam County Commission on the data-center resolution; NBA camps open; Hannan at Roane 6:30; USMNT v Chile 8 p.m. ET** | |
| **2026-10-03** | **WV regular goose and duck seasons open; U.S. 7 reopens** | |
| **2026-10-11** | **WV dove first segment closes** | |
| **2026-10-19** | **Alberta referendum** | |
| **2026-10-28** | **Carabao Cup fourth round, Liverpool v Chelsea, Anfield** | |
| **2026-10-31** | **WV second youth waterfowl day** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |

### Open threads

- **white-house-press-ban-cnn-msnow-politico** — led; the AP pass case, any court filing by the three outlets, and the WHCA response are the follow-ups. **trump-ai-force-czar / first-circuit-third-country / medicaid-50-states-529b / wildfires-8-5m-acres** — ran. **caribbean-boat-strike-4 / ai-labs-antitrust-suit** — alternates.
- **kohat-police-lines-31 / iran-conditions-via-qatar / kenscoff-164-rnddh / moscow-largest-drone-attack** — ran. **duma-result (tonight) / moscow-e-voting-cyberattack / boj-1-25-friday / houthi-missile-riyadh / sweden-andersson-forming** — alternates.
- **arts-agency-audit / wv-ready-15m / buffalo-bridge-interchange / capito-college-sports-act** — ran. **chiles-death / belle-pyrolysis-forum / wood-grand-jury-96** — regional. **bennington-drug-ring-12-years** — away. **webster-memorial-miller / surf-city-hemp-shop-life** — hotspots. **nb-drb-sept-23 / webster-stair-climb / topsail-high-student / batts-segment-5-addendum / kanawha-deputies / huntington-diesel-closure / caserta-retiring / huntington-flock / red-oak-fire-tower (RAN 09-15) / webster-county-fair (RAN 09-18)** — alternates.
- **pg-rail-alliance-600k / rainbow-park-washroom / bc-conservatives-expel-three / eby-ubcm-pst-deferred / hajdu-labour-bill-107 / highwood-ucp-smith-review** — ran. **penticton-councillor-guilty / building-canada-strong-act / unifor-stellantis (tonight) / eldorado-mediation / pg-council-profiles / uhnbc-helipad / findlay-ipsos-35** — alternates.
- **xrism-gx301-2 / y-chromosome-loss-gradient / ervebo-bundibugyo-trial / nasa-spacex-three-crew-flights** — ran. **graphene-floquet / progress-96 / florida-dengue-death** — alternates.
- **hacktron-claude-openai / census-ces-26-56 / ban-ai-e-waste** — ran. **ai-report-chinese-ship (CNN 451) / gemini-irregular-breaches / sanders-casar-bill (not introduced)** — alternates.
- **brentford-3-0-chelsea / villa-3-2-spurs-van-hecke / liverpool-bournemouth-preview / burrow-questionable-full-practice / reds-6-4-cubs / cubs-5-2-reds / browns-jenkins-out-campbell-q / crew-2-0-montreal / fcc-2-2-houston-denkey / marshall-30-24-missouri-state / south-alabama-41-36-ohio / pirates-8-5-royals / pirates-6-5-royals / wvu-38-27-virginia** — ran. **hannan / spurs / usmnt** — sat out. **hannan-westside-score / hannan-sept-21-maxpreps / chelsea-spurs-next-fixtures** — owed.
- **aki-day8-onosato-alone-7-1 / aki-day8-hakunofuji-kotozakura / aki-day9-card / mets-10-3-phillies / guardians-12-6-athletics / padres-7-6-marlins-10 / brighton-3-0-arsenal / coventry-1-0-forest / newcastle-2-1-hull-everton-1-0-ipswich** — ran. **cfb-saturday-roundup / brewers-clinch-date / nfl-weekend-moves** — held.
- **bear-gun-going-out-sept25 / archery-sept26 / ducks-oct3 / geese-oct3 / squirrel-day-9 / dove-day-20 / red-drum / seatrout / spanish-bluefish-footnote-m / black-drum-sheepshead** — ran. **gauley-window-2-ends-monday / gauley-window-3-sept-25-28 / gauley-fest-closes / mon-nf-sept-14 / stocking-none / flounder-closed-sept-15** — seasons note. **williams-90-4-rising-flash-flood / point-pleasant-25-56-rising / huntington-26-31-rising-crest-27-1-tue / no-nc-alerts-rip-low / td-six-azores / moon-waxing-gibbous-springs** — water block.
- **digest-09-18-unrecorded / no-edition-09-19** — logged in FAILURES; for Nate. **edition-number-from-files-46-36** — for Nate (index says 45; sportsman index still stops at 11). **fetch-fishing-24h-window-bug** — for Nate. **standings-gate-chicago** — for Nate. **result-verb-gate-first-verb-first-mention** — behaviour noted above, not a bug to fix today. **wakanokatsu-wakanosho** — JSA spelling adopted.

### Covered slugs, 2026-09-20

`white-house-bars-cnn-msnow-politico-passes-disabled`, `trump-ai-force-ai-czar-truth-social`, `first-circuit-third-country-deportation-notice`, `medicaid-drug-pricing-model-all-50-states-529b`, `wildfires-8-5m-acres-forest-service-shortages`,
`kohat-old-police-lines-attack-31`, `iran-conditions-end-war-via-qatar-rezaei`, `haiti-rnddh-kenscoff-164`, `moscow-largest-drone-attack-duma-vote-ends`,
`legislative-audit-former-arts-agency-72-grants`, `wv-ready-15m-educational-opportunity-centers`, `buffalo-bridge-interchange-6-3m-routes-869-817`, `capito-protect-college-sports-act`,
`chiles-former-judge-prosecutor-dies`, `belle-clean-seas-pyrolysis-forum-tuesday`, `wood-grand-jury-96-indicted-murder-charge`, `bennington-drug-gun-ring-supervisor-12-years-sept-8`, `webster-memorial-miller-associate-administrator`, `surf-city-hemp-shop-killing-life-sentence`,
`pg-rail-alliance-600k-ubcm`, `pg-rainbow-park-700k-washroom`, `bc-conservatives-expel-rustad-rattee-halford`, `eby-ubcm-pst-deferred-ferries`, `hajdu-labour-code-section-107-bill`, `highwood-ucp-smith-leadership-review`,
`xrism-gx-301-2-stellar-wind-science-advances`, `y-chromosome-loss-tumor-gradient-jci-insight`, `who-msf-ervebo-bundibugyo-trial-20000`, `nasa-spacex-crew-15-16-17-946m`,
`hacktron-claude-openai-forum-breach-6500`, `census-ces-26-56-ai-exposed-graduates-13pct`, `ban-ai-e-waste-395-617m-tonnes`,
`brentford-3-0-chelsea-anthony-thiago-carvalho`, `villa-3-2-spurs-van-hecke-98th`, `liverpool-bournemouth-preview-iraola`, `burrow-questionable-full-practice-houston`, `reds-6-4-cubs-aguiar-pagan`, `cubs-5-2-reds-boyd-lodolo`, `browns-jenkins-out-campbell-questionable-tampa`, `crew-2-0-montreal-farsi-mendez`, `fcc-2-2-houston-denkey-90-7-pen`, `marshall-30-24-missouri-state`, `south-alabama-41-36-ohio`, `pirates-8-5-royals-15-hits`, `pirates-6-5-royals-weaver-montgomery`, `wvu-38-27-virginia-charlotte`,
`aki-day8-onosato-alone-seven-one`, `aki-day8-hakunofuji-over-kotozakura-churanoumi-over-kirishima`, `aki-day9-card-kotozakura-fujinokawa`, `mets-10-3-phillies-painter`, `guardians-12-6-athletics-cecconi`, `padres-7-6-marlins-10-innings-morgan`, `brighton-3-0-arsenal-first-loss`, `coventry-1-0-forest-first-points`, `newcastle-2-1-hull-everton-1-0-ipswich`,
`bear-gun-second-window-closes-sept-25`, `archery-deer-bear-boar-sept-26`, `ducks-coots-mergansers-oct-3`, `geese-oct-3`, `squirrel-day-9`, `dove-day-20-rails-snipe`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish-footnote-m-3-5`, `black-drum-sheepshead`,
`gauley-window-2-ends-sept-21-window-3-sept-25-28`, `gauley-fest-closes`, `mon-nf-nothing-past-sept-14`, `stocking-none`, `flounder-closed-since-sept-15`, `williams-90-4-rising-flash-flood-warning`, `point-pleasant-25-56-rising-no-nwps-id`, `huntington-26-31-rising-crest-27-1-tuesday`, `no-nc-alerts-rip-low-td-six-azores`, `moon-waxing-gibbous-62-springs-building`, `topsail-fp-sept-1-nineteen-days`

**Post record, 2026-09-20.** The digest for No. 46 posted at **7:00:00 a.m. ET** exactly, held 8 minutes by `--not-before 07:00` from a 6:52 foreground start (message 1551186161618260081, 1,080 embed chars, hero attached, `degraded: []`). Both papers were live on Pages by 6:02 (dated Times and Sports pages both 200), twelve minutes after the 5:50 push. Sports & Sportsman No. 36 was published with the Times and not posted, per the standing rule. The 7:04 backup `send_later` wake was deleted after the record landed. The session was held in the foreground with `hold_until.py` in nine-minute windows from 5:53 to 6:52 rather than idled to a wake, because the 09-18 wake fired into a session that never completed the post.


## 2026-09-21 — No. 47 (Times) and No. 37 (Sports & Sportsman)

| Open-ended | **Twenty-sixth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water) launched 5:35 and filed 5:37-5:44 a.m. ET. Times validated 5:46 on the second pass (the WV desk filed two away lines; the validator allows one — the Sept. 15 drug-bust line was cut, the Select Board vote kept), Sports & Sportsman clean on the first pass (three "species not in the WV reference table" WARNs for the migratory-bird rows, as every morning since the PDF was adopted). HEAD was detached from main at session start again — twenty-second occurrence; `git checkout main && git pull` fixed it. `config.head_start_minutes` reads 90 | **standing practice — post run in the FOREGROUND with `hold_until.py` chunks, backup `send_later` at 7:04** |
| Open-ended | **Setup: pip installed Pillow first try; cairosvg pip-installed for viewing the drawing. All three fetchers clean** — stats 4 entries (S&P 7,650.50 +0.17%, Dow 51,682.64 -0.18%, Nasdaq 26,522.54 +0.39% — all still the Sept. 18 close, markets were shut Saturday and Sunday; Bitcoin $84,458 +5.10%); fishing 4 waters, 0 errors; standings 5 clubs (Pirates 79-77 third, 19.0 back, 7.0 out, W4; Reds 72-84 fifth, 26.0 back, 14.0 out, L2). **The fetcher's "24h ago" comparison is again the two-day window's first point (Saturday 5:45 a.m., 47 hours back) on all three USGS gauges;** its rising flags match the true 24-hour change on all three but not the morning on the Williams (receding since a 4 p.m. Sunday crest of 1,560 cfs) or Huntington (flat off a 10:15 p.m. bump). The water block prints the file's numbers and says which direction is which | **fetch-fishing-24h-window-bug — still for Nate** |
| Open-ended | **The lead is the Duma result: United Russia 355 of 450 seats, a record, per CEC chief Pamfilova Monday with 95%+ counted.** Al Jazeera primary (its "what we know" piece: 57.86% of the list vote at 90.43% counted; turnout just under 57%; most anti-war candidates barred, Yabloko candidates who did run feared for their freedom — so the lead says "most anti-war candidates were barred", NOT "Yabloko barred", which the 09-18 brief said and which AJ's copy does not support as a blanket fact); cross-checked Euronews (355, prior record 343, turnout "above 59%"), France 24 live, Kyiv Independent, AP via PBS (no OSCE observers). **Turnout conflict (57 v 59) dropped rather than split.** Drone-attack toll differed by outlet (2 v 3 in the Moscow region) — no toll printed. Final results "unlikely before Friday" per TASS via AJ. U.S.: ICE shoots a Venezuelan DoorDash driver in Austin, Sunday (NBC; CBS and AJ concur); Cassidy on Face the Nation on vaccines and measles (CBS); Trump's D.C. arch as a drone and sniper base (CBS); Bessent's AI-incident notification proposal to He Lifeng, New York Sunday (AJ). World: Iran's military says the U.S. is preparing new strikes (AJ); Kabul says Pakistani air raids killed 3 in Kunar (AJ — Taliban toll, attributed); Haiti extradites 18 Moise suspects (AP via PBS); seven Ethiopian armed groups form an "Alliance for Survival" (AJ). **AJ's Pakistan copy puts Kohat at "at least 21" against the 31 the paper ran Sunday from France 24/AFP — neither figure re-run.** Held: NBC poll (55% say Trump hurt the economy); ICC sanctions (WSJ/Reuters via AJ, unnamed officials); NBC's Russian spy-plot indictment (subscriber-gated); HRC presentation of the Iran report had no readable result by 5:40 | **watch: HRC Iran report; final Duma results Friday; Iran-U.S.; ICC sanctions; Trump-Gulf leaders Tuesday; Trump-Xi ~Sept. 24** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** Al Jazeera's og:image is an AP photograph (Sunday, St. Petersburg): a polling station in an old hall — two blue curtained voting booths on thin tube frames with the double-headed-eagle crest, a mural of eighteenth-century figures across the back wall with a sail and a wall lamp, a man in a long coat stepping out of one booth with ballot papers, a woman out of the other, a police officer sprawled on a slatted bench at left, a small girl in a puffer jacket with an umbrella in the right foreground, parquet floor. `scratchpad/draw.py`, 274 paths, 40 KB; four real faces in the photo, none drawn; the painted figures' heads are blank ovals. Ninth rung-1 drawing in a row. Viewed with cairosvg | |
| Open-ended | **Notebook: 4 statewide, 1 regional (huntington_cabell), away 1, hotspots 2 — four lines.** Statewide: Culture Center closing the State Museum, gift shop and Fagan theater ahead of 2027 renovations, up to $150M in bonds (News and Sentinel, Monday); ex-TC Energy director Urbanczyk's $3M payment in the Alberta suit over the Charleston lease (Gazette-Mail via curl, Saturday); Sunday's 20-plus-county flash flood warnings north of I-64, no damage reported that morning (WSAZ); AEP/FirstEnergy opposing PJM governance reform at the Sept. 15 committee (Gazette-Mail via curl, Friday). Regional: a 27-year-old motorcyclist killed about 2 a.m. Monday on Jefferson Avenue, Huntington (Herald-Dispatch via curl, city release). **Cut at the editor's desk: the Clay Center interim-CEO line (Thursday — outside the 48-hour rule).** Empty: putnam_kanawha after that cut (the I-79 Elkview work-zone fatal was Friday 11:30 p.m., WCHS Saturday — held as over 48 hours, and the WCHS index no longer lists it); mid_ohio_valley (WTAP fundraiser and festival look-back only; N&S local page's only Wood item ran statewide); nicholas_webster (Register-Herald newest Sept. 18, WOAY/WVVA nothing, Echo Sept. 14 all used or deduped; **no readable outlet reported Sunday flood impacts in Webster or Nicholas — searches returned only NWS warning mirrors**); summers_new_river (Hinton News answered once, stops at Aug. 30). Away: Bennington Select Board 3-1 vote on $24,000/yr Old Bennington winter maintenance (Banner, Sept. 18). Cabin: Webster EDA voted Sept. 8 to offer on 50+ acres of DNR land near Big Ditch Lake for an RV park (Echo, Sept. 14 — not previously run). Topsail: Topsail High sophomore hit crossing U.S. 17 Thursday, stable (WECT, Sept. 18). **No readable outlet reported Sunday flood damage, rescues, closures or deaths anywhere in WV as of 5:41; the only flood story opened was WSAZ's Sunday-morning warnings piece. The WCHS "severe flooding" search hit was July 22 — dodged.** Alternates: Bennington drug bust Sept. 15 (cut for the one-line rule); option-tax discussion Sept. 15; NB DRB Wednesday; Bergoo UTV crash Sept. 5 (Echo); junior firefighters' stair climb; NTB website relaunch Sept. 16; Onslow man charged with threatening a Pender commissioner (WECT Sept. 18, not opened); Helton death-penalty bill (Sept. 15, too old); Black Diamond PSC hearing today, no new preview; FEMA still unanswered. MetroNews not tried (ninth morning) | **watch: Monday flood-damage reporting (Mason/Jackson/Wood warnings ran to 12:30); Black Diamond hearing outcome; NTB EIS hearing Tuesday 6 p.m.; Belle pyrolysis forum Tuesday; Devine prelim Sept. 23; Caserta seat Sept. 24; HB 2014 Sept. 28; Putnam commission Sept. 29; FEMA; hens** |
| Open-ended | **Canada 1/2/3.** PG: Radloff runs for council on the tax base and downtown safety (CKPG, Friday — labeled; CKPG's weekend output was all sports, UNBC newest Sept. 11, RDFFG/City pages undated, SD57 103 bytes). BC: **Findlay resigned Sunday** as Conservative leader, under four months in, hours after a 14th MLA left caucus, still the Sept. 26 Abbotsford-Mission candidate (CBC); **the board named Cariboo-Chilcotin MLA Lorne Doerkson interim leader** hours later, NDP caucus met late Sunday (CP via CKPG, stamped Monday 1 a.m., written as Sunday). Canada: Belleville synagogue shooting Sunday 7:10 p.m. on Yom Kippur, officer and man wounded, SIU probing (AP via CBC); Parliament resumes Monday with a 173-seat Liberal majority, six vacancies, NDP at five (CP via CKPG); Poilievre's "28th state" rally in Brantford (CP via CHEK). Held: Unifor-Stellantis — **no outcome on any readable outlet by 5:43 (CBC Windsor feed, Global, unifor.org all stop at Thursday)**; Rustad presser is Monday Pacific — tomorrow's; Hajdu bill not tabled; Carney-Norway Arctic (alternate); Hepner (folded into the Findlay brief; CP says 13 exits, CBC 14 — each attributed, not merged). My PG Now 403 | **watch — Unifor-Stellantis outcome; Rustad presser; Doerkson's first day; Findlay byelection Sept. 26; Quebec debate Sept. 23; PG vote Oct. 17** |
| Open-ended | **Sumo, Aki Day 9 — JSA English leaders page, torikumiAjax JSON for Days 9 and 10, absence page (all curl).** **Onosato alone at eight and one** (hikiotoshi over Fujiryoga); chasers at seven and two: Atamifuji, Fujinokawa, Churanoumi, Kinbozan. **Kotozakura out of the chase** — thrown by Fujinokawa (uwatenage) in the only chaser-v-chaser bout, six and three; Daieisho pulled down Kirishima; Takanosho pulled down Asanoyama; Oshoma slapped down Ura. Day 10: Onosato v Hakunofuji, Kotozakura v Atamifuji, Aonishiki v Churanoumi, Fujinokawa v Takanosho, Kinbozan v Toshinofuji. Kyujo unchanged (Hoshoryu, Wakatakakage, Wakanosho — the last carried from the absence page as read Sept. 18). Every shikona checked against the JSA JSON's `shikona_eng`. Kinbozan's Day 9 win confirmed only by his record on the leaders page. Records in words; no `result` on sumo briefs | **Day 10 results Tuesday; Onosato alone by one** |
| Open-ended | **Our Teams: 6 briefs, 4 outlets.** Liverpool 1-0 at Bournemouth, Isak 57' (ESPN eng.1 scoreboard; liverpoolfc.com headline agrees); **Bengals 20-6 at Houston**, Chase two TDs, Higgins 5-95 (AP via CBS box); **Cubs 9-1 Reds**, Peterson W, Lowder L (Stats API); **Browns 23-19 at Tampa Bay**, Watson 24/30/238, 2:12 lightning delay (AP via CBS box); **Pirates 4-3 Royals, sweep, fourth straight**, Mlodzinski W (Stats API); WVU unranked in Sunday's AP poll, 93 points in others receiving votes (ESPN rankings feed). Standings: MLB byte-matched; PL from ESPN's feed — Liverpool sixth/9, Chelsea 10th/7, Spurs 20th/2; NFL Bengals 2-0 (at Pittsburgh Sunday 1 p.m.), Browns 1-1 (v Carolina Sunday 1 p.m.); FCC 33 ninth, Crew 26 13th; WVU 3-0, Marshall 2-1, Ohio 1-2; Hannan 1-2 per MaxPreps. Upcoming 14 lines Sept. 22-27, MLB from the Stats API (UTC converted). **No Premier League fixtures Sept. 26-28 — the FIFA window (USMNT v Peru Sept. 26, Chile Sept. 29)**; Chelsea and Spurs carried by standings only (chelseafc.com empty, tottenhamhotspur.com nav-only, Sky results a stub). Sat out: Hannan (still no Sept. 17 Westside score; MaxPreps still lists Westside at Hannan TONIGHT 6:30, not in Ian's doc — not printed; **fourth morning owed — ask Ian**), Spurs (nba.com/spurs rendered nothing; media day Sept. 28 unconfirmed), USMNT. ESPN's "Reliant Stadium" venue label ignored — "in Houston" written | **hannan-westside-score / hannan-sept-21-maxpreps — owed; Chelsea/Spurs Monday news source** |
| Open-ended | **Leagues: 11 briefs (12 filed; the desk's Cubs-Reds brief was cut as a duplicate of Our Teams').** Sumo 3; NFL 3: Chiefs 33-30 OT Colts on Butker's 40-yarder, Mahomes 382/3 (PFT, read in full); Cowboys 37-20 Commanders, Daniels' dislocated left elbow, "no fracture" is Quinn's (PFT); Saints 24-17 at Baltimore with Shough (ESPN JSON). MLB 2: Phillies 7-2 Mets, Sanchez W, still no clinch (Stats API); Guardians 1-0 Athletics, a game up on the White Sox (Stats API — "one-game" from the feed's 1.0, no record printed). PL 2: City 5-3 Sunderland, five for five, three clear of Arsenal; United 1-1 Fulham and Leeds 0-0 Palace (Sky results via curl). CFB 1: AP poll — Ole Miss to No. 4, Texas A&M down 14 to 23rd (ESPN rankings feed). Held: MLS Sunday (only Miami 2-2 San Diego); Saturday CFB results beyond the poll (SI/NBC not opened); division clinches (feed flags without dates) | **standings-gate — records kept out of Leagues briefs; a CFB roundup still needs SI/NBC opened early** |
| Open-ended | **Outdoors: all four waters, and the story is the Williams.** **Williams 750.0 cfs / 3.39 ft at 5:15, "blown out. Stay on the bank." — crest 1,560 cfs / 4.52 ft at 4 p.m. Sunday per the USGS two-day trace, receding since (950 at midnight, 755 at 5:00)**; the fetcher's "rising" is against Saturday 5:45 a.m.'s 58.8; the true 24-hour mark was 90.4. Flood Watch until noon over Webster and Nicholas; no warning on the Williams basin at 5:38. Point Pleasant 25.97 rising, up 0.7 ft in the two hours after 2:45 a.m., three Flood Warnings on Mason/Jackson/Wood until 10:45-12:30; PTPW2 404 again, no crest. Huntington 28.53 rising, flat off a 28.83 bump at 10:15 p.m.; NWPS HNTW2 (issued 11:13 a.m. Sunday, pre-rain) crest 30.8 ft about 2 a.m. Tuesday, action 48. Topsail: all four sound events inside today (H 4:21 AM 3.2, L 10:42 AM 0.8, H 5:03 PM 4.0, L 11:31 PM 1.2), 80.6F Beaufort, **moon waxing gibbous 72%, 9.5 days — springs building to the full moon Sept. 26 16:49 UT (USNO API; timeanddate 403)**; no NC alerts, rip LOW, surf ~2 ft, HIGH rip Friday on a north wind; **NHC: TS Fay near the Azores, no Atlantic formation in 7 days. Fisherman's Post and Coastal Angler both still Sept. 1, 20 days old.** Seasons: archery deer/bear/boar Sept. 26 (5 days); ducks/coots/mergansers and geese Oct. 3 (12) from the migratory PDF (downloaded, PyMuPDF); bear gun third window Oct. 3-9 (12, selected counties); squirrel Day 10; dove Day 21; going_out: bear gun second window closes Friday. **Gauley release windows NOT re-confirmed: riverscout 404 on every path, USACE cert failure, NPS 404** — the note says so and does not repeat Sunday's dates as confirmed. MNF nothing after Sept. 14; stocking silent (the wvdnr.gov trout-stocking URL redirects to a Feb. 2023 Bear Rock Lakes notice). WV reference valid through 2027-06-30 | **watch — Williams recession (300-500 band a day or two out); Huntington crest Tuesday 2 a.m.; Gauley window 3 Sept. 25-28 needs a source that answers; Fisherman's Post October report; HIGH rip Friday at Topsail** |
| Open-ended | **Sci/Tech and AI.** Ice sheets lost 12.5 trillion tons 1972-2023, ~3.1 cm sea level, Scientific Data, Northumbria-led (Phys.org); stalled gut microbiome triples type 1 diabetes risk, 887 children, Nature Metabolism, Mass General Brigham (Medical Xpress); newborn attention sex differences, 130 infants, Biology of Sex Differences, Cambridge (EurekAlert); Progress 96 docked Saturday 9:44 a.m. EDT, 2.8 tons, a week late (Spaceflight Now; NASA "approximately three tons" — SFN's figure used with SFN the source). AI: Google confirms Gemini agents reached three real firms in Irregular's May sandbox test (Register, own reporting; TechCrunch corroborates); subscribers' antitrust class action v Anthropic/OpenAI/Google/SpaceXAI over the Sept. 12 slowdown, **filed Friday, AP published Saturday — run labeled "Friday" as the 48-hour dead-beat exception (Sunday's held alternate, never run)**. Held: Sanders/Casar bill still "to introduce" per Sanders' own release (a Washington Examiner snippet said "introduced" — wrong); Anthropic response on Hacktron (none); CNN ship story (no readable outlet with own reporting); VUB fire-weather, UGA flatworm, MIT senescence barcode (swap-ready). OPB's fetch dated the suit "Friday, Sept. 20" — Sept. 20 was Sunday; PBS/AP date used | **watch — Sanders/Casar bill; NYT v OpenAI; Trump-Xi AI-incident channel** |
| Open-ended | **Source status.** OPEN: NBC, CBS, Al Jazeera, PBS, Euronews (WebFetch), France 24, Kyiv Independent, Haitian Times, NASA, Phys.org, Medical Xpress, EurekAlert browse, Spaceflight Now, Register, TechCrunch, 404 Media, 9to5Mac, OPB, TechXplore, sanders.senate.gov, WSAZ, WCHS, WTAP, WVVA, WOAY, Register-Herald, News and Sentinel, WV Watch RSS, Gazette-Mail (curl), Herald-Dispatch (curl), Webster Echo (WebFetch), Hinton News (once, stale), WECT, NTB/Surf City/Pender flashes, Bennington Banner article pages (`/local-news/` index 404, `/news/` works), CKPG, CBC (RSS + curl), CHEK, Global (feed and article), UNBC, JSA leaders/torikumiAjax/absence, ESPN JSON (scoreboards, standings, rankings), MLB Stats API, Sky results (curl, stub at times), MaxPreps, liverpoolfc.com, ussoccer.com, NBC/PFT, CBS box scores (AP copy), USGS, NWPS HNTW2, api.weather.gov, ILM SRF, NHC, NCDMF, USNO phases API, wvdnr.gov PDF (curl), Fisherman's Post and Coastal Angler feeds, fs.usda.gov alerts. BLOCKED: Reuters/AP/BBC/Guardian (not tried), Politico, The Hill, CNN, Nature, Science, Ars, Verge, Wired (fetch refused), MIT Tech Review (no list), NPR (curl gave one summary line), WV MetroNews (not tried, ninth morning), WOWK, WVU Today, Dominion Post, My PG Now (403), PG Citizen (not tried), princegeorge.ca (rendered nothing), chelseafc.com (empty), tottenhamhotspur.com (nav only), nba.com/spurs (no headlines), bengals.com/clevelandbrowns.com (0 bytes without a UA), ESPN site, riverscout.app (404 all paths), USACE Huntington (cert), NPS Gauley (404), NWPS PTPW2 (404), timeanddate (403), Corps Huntington District (cert) | **watch — MetroNews; a Gauley release source; PL club sites on a Monday** |
| Open-ended | **Traps dodged.** (1) "Yabloko barred" — AJ says Yabloko candidates ran; "most anti-war candidates barred" written instead. (2) Turnout 57 v 59 — dropped. (3) Drone toll 2 v 3 — dropped. (4) Euronews rendered "Sunday, September 22" — weekday only. (5) AJ's Kohat "at least 21" v Sunday's 31 — neither re-run. (6) Cyclospora lettuce search hit was Aug. 27; NBC's mail-ballot live blog was Sept. 3 — both dodged. (7) WCHS "severe flooding" hit was July 22. (8) Clay Center line was Thursday — cut. (9) Two away lines — the validator allows one; cut to one. (10) CP 13 v CBC 14 exits — attributed separately. (11) CP's Doerkson story stamped Monday — appointment was Sunday. (12) OPB dated the AI suit "Friday, Sept. 20" — Sept. 20 is Sunday. (13) Washington Examiner "introduced" v Sanders' "to introduce". (14) Leagues desk duplicated the Cubs-Reds result — cut. (15) ESPN's "Reliant Stadium" — "in Houston". (16) ESPN's Daniels recap headline — confirmed in Quinn's quotes. (17) Fetcher's 47-hour "24h ago" on all three gauges — both directions printed. (18) wvdnr.gov stocking URL redirects to a 2023 notice — nothing printed. (19) Gauley dates unconfirmable today — not repeated as confirmed. (20) MaxPreps' Sept. 21 Hannan fixture — still not printed | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-21** | **Aki Day 9 (ran); Duma preliminary result (led); HRC presentation of the Iran report, Geneva (no readable result by 5:40); PSC Black Diamond receivership hearing; Rustad presser, Victoria (Pacific afternoon — tomorrow's); Parliament resumes in Ottawa; MaxPreps' unconfirmed Westside at Hannan 6:30; Huntington NWPS 30.4 ft by 2 p.m.** | |
| **2026-09-22** | **Aki Day 10 (Onosato v Hakunofuji, Kotozakura v Atamifuji); Hannan at Calvary 6 p.m. (venue unconfirmed); NTB draft EIS hearing 6 p.m.; Belle pyrolysis forum 6-8 p.m.; Parkersburg full council; Reds at Braves 7:15, Pirates v Cardinals 6:40; Huntington NWPS crest 30.8 ft ~2 a.m.; Trump meets Gulf leaders, New York** | |
| **2026-09-23** | **Devine preliminary hearing; third Quebec debate; North Bennington DRB** | |
| **2026-09-24** | **Cabell commission on the clerk's seat; Hannan v Roane at Ashton 6 p.m.; Pirates v Cardinals 12:35; Trump-Xi window** | |
| **2026-09-25** | **WV bear gun second window closes (selected counties); Gauley window 3 (25-28, unconfirmed today); final Duma results expected (TASS via AJ); Reds at Blue Jays, Pirates at Tigers; HIGH rip risk at Topsail (ILM)** | |
| **2026-09-26** | **WV archery/crossbow deer, bear and boar open; full moon 16:49 UT; USMNT v Peru 4:30 p.m. ET Orlando; Findlay byelection, Abbotsford-Mission; Ohio v Stonehill 3:30, Marshall v Gardner-Webb 3:30, WVU v Oklahoma State 7; FCC at Montreal 7:30; USSF-385 launch** | |
| **2026-09-27** | **Aki senshuraku; Bengals at Pittsburgh 1 p.m., Browns v Carolina 1 p.m.; Crew v Inter Miami 7 p.m. ET** | |
| **2026-09-28** | **HB 2014 data-center rules hearing; NBA media day (unconfirmed for the Spurs); Surf City e-bike focus group 6-8 p.m.; Sweden's Andersson reports** | |
| **2026-09-29** | **Putnam County Commission on the data-center resolution; Hannan at Roane 6:30; USMNT v Chile 8 p.m. ET** | |
| **2026-09-30** | **NC flounder possession closure ends (limits page)** | |
| **2026-10-03** | **WV regular goose and duck seasons open; bear gun third window (3-9); U.S. 7 reopens** | |
| **2026-10-05** | **Quebec general election** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18); woodcock opens** | |
| **2026-10-19** | **Alberta referendum** | |
| **2026-10-28** | **Carabao Cup fourth round, Liverpool v Chelsea, Anfield** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |

### Open threads

- **united-russia-355-duma-record** — led; final results Friday, Western reaction and any Yabloko prosecution are the follow-ups. **ice-shoots-doordash-driver-austin / cassidy-vaccines-measles / trump-arch-drone-sniper-base / bessent-ai-incident-alerts-china** — ran. **nbc-poll-55-economy / icc-sanctions-reports / russian-spy-plot-indictment / hrc-iran-report** — alternates.
- **iran-military-us-preparing-strikes / kabul-pakistani-raids-kunar-3 / haiti-18-extradited-moise / ethiopia-seven-groups-alliance** — ran. **kohat-toll-21-v-31 / sweden-andersson-sept-28 / boj / sudan / imran-khan-sister** — alternates.
- **culture-center-closing-150m / urbanczyk-3m-tc-energy / flash-flood-warnings-20-counties / aep-firstenergy-pjm-reform** — ran. **huntington-motorcyclist-jefferson-ave** — regional. **bennington-select-board-old-bennington-24k** — away. **webster-eda-big-ditch-rv-park / topsail-high-student-us-17** — hotspots. **clay-center-gillispie (Thursday, cut) / i-79-elkview-fatal (Friday, held) / bennington-drug-bust-sept-15 (cut, one-line rule) / option-tax / nb-drb-sept-23 / bergoo-utv / stair-climb / ntb-website / pender-commissioner-threat / helton-death-penalty / black-diamond-hearing / fema** — alternates. **red-oak-fire-tower (RAN 09-15) / webster-county-fair (RAN 09-18) / webster-memorial-miller (RAN 09-20)** — do not re-run.
- **radloff-pg-council / findlay-resigns / doerkson-interim / belleville-synagogue-shooting / parliament-resumes-173 / poilievre-28th-state** — ran. **hepner-exit / carney-store-arctic / unifor-stellantis (outcome unknown) / rustad-presser / hajdu-bill / building-canada-strong** — alternates.
- **ice-sheets-12-5-trillion / gut-microbiome-t1d / newborn-attention-cambridge / progress-96-docked** — ran. **vub-fire-weather / uga-flatworm / mit-senescence-barcode** — alternates.
- **gemini-irregular-three-firms / ai-labs-antitrust-class-action** — ran. **sanders-casar-bill (not introduced) / hacktron-anthropic-response / cnn-ship-report** — alternates.
- **liverpool-1-0-bournemouth-isak / bengals-20-6-texans-chase / cubs-9-1-reds / browns-23-19-buccaneers-watson / pirates-4-3-royals-sweep / wvu-unranked-93-points** — ran. **hannan / spurs / usmnt** — sat out. **hannan-westside-score / hannan-sept-21-maxpreps / chelsea-spurs-monday-news** — owed.
- **aki-day9-onosato-alone-8-1 / aki-day9-fujinokawa-throws-kotozakura / aki-day10-card / chiefs-33-30-colts-ot / cowboys-37-20-commanders-daniels-elbow / saints-24-17-ravens / phillies-7-2-mets / guardians-1-0-athletics / city-5-3-sunderland / united-1-1-fulham-leeds-0-0-palace / ap-poll-ole-miss-4-texas-am-23** — ran. **mls-sunday / cfb-saturday-roundup / clinch-dates** — held.
- **archery-sept26 / ducks-oct3 / geese-oct3 / bear-gun-oct3-9 / squirrel-day-10 / dove-day-21 / red-drum / seatrout / spanish-bluefish-footnote-m / black-drum-sheepshead / bear-gun-going-out-sept25** — ran. **flounder-closed-through-sept-30 / gauley-unconfirmed / mon-nf-sept-14 / stocking-none** — seasons note. **williams-750-receding-crest-1560 / point-pleasant-25-97-rising-warnings / huntington-28-53-crest-30-8-tue / no-nc-alerts-rip-high-friday / ts-fay-azores / moon-72-springs-full-sept-26** — water block.
- **sportsman-index-stale-no-11** — for Nate (No. 37 computed from the edition files). **fetch-fishing-24h-window-bug** — for Nate. **standings-gate-chicago** — for Nate. **detached-head-twenty-second** — recurring. **gauley-source** — riverscout/USACE/NPS all failed today.

### Covered slugs, 2026-09-21

`united-russia-355-of-450-duma-record-pamfilova`, `ice-shoots-venezuelan-doordash-driver-austin`, `cassidy-radical-honesty-vaccines-measles`, `trump-arch-drone-sniper-base-truth-social`, `bessent-ai-incident-notification-he-lifeng`,
`iran-khatam-al-anbiya-us-preparing-strikes`, `kabul-pakistani-air-raids-kunar-3-dead`, `haiti-extradites-18-moise-suspects-badio`, `ethiopia-seven-armed-groups-alliance-for-survival`,
`culture-center-state-museum-closing-150m-bonds`, `urbanczyk-3m-tc-energy-charleston-lease`, `wsaz-flash-flood-warnings-20-counties-sunday`, `aep-firstenergy-oppose-pjm-governance-reform`,
`huntington-motorcyclist-27-jefferson-avenue`, `bennington-select-board-old-bennington-winter-24k`, `webster-eda-big-ditch-lake-rv-park-offer`, `topsail-high-sophomore-hit-us-17-stable`,
`radloff-pg-council-tax-base-40m`, `findlay-resigns-bc-conservative-leader-14-exits`, `doerkson-interim-bc-conservative-leader`, `belleville-synagogue-shooting-officer-siu`, `parliament-resumes-liberal-173-ndp-5`, `poilievre-never-eu-28th-state-brantford`,
`ice-sheets-12-5-trillion-tons-scientific-data`, `gut-microbiome-plateau-t1d-nature-metabolism`, `cambridge-newborn-attention-sex-differences`, `progress-96-docks-poisk-week-late`,
`google-gemini-agents-irregular-three-firms`, `subscribers-antitrust-suit-four-ai-labs-slowdown`,
`liverpool-1-0-bournemouth-isak-57`, `bengals-20-6-texans-chase-two-tds`, `cubs-9-1-reds-peterson-lowder`, `browns-23-19-buccaneers-watson-whiteheart`, `pirates-4-3-royals-sweep-mlodzinski`, `wvu-unranked-ap-poll-93-points`,
`aki-day9-onosato-alone-eight-one`, `aki-day9-fujinokawa-uwatenage-kotozakura`, `aki-day10-card-onosato-hakunofuji`, `chiefs-33-30-colts-ot-butker`, `cowboys-37-20-commanders-daniels-elbow`, `saints-24-17-ravens-shough`, `phillies-7-2-mets-sanchez`, `guardians-1-0-athletics-williams`, `man-city-5-3-sunderland-five-for-five`, `united-1-1-fulham-leeds-0-0-palace`, `ap-poll-ole-miss-fourth-texas-am-23rd`,
`archery-deer-bear-boar-sept-26`, `ducks-coots-mergansers-oct-3`, `geese-oct-3`, `bear-gun-third-window-oct-3-9`, `squirrel-day-10`, `dove-day-21`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish-footnote-m`, `black-drum-sheepshead`, `bear-gun-second-window-closes-sept-25`,
`flounder-closed-through-sept-30`, `gauley-unconfirmed-today`, `mon-nf-sept-14`, `stocking-none-2023-redirect`, `williams-750-receding-crest-1560-sunday`, `point-pleasant-25-97-rising-three-warnings`, `huntington-28-53-crest-30-8-tuesday`, `no-nc-alerts-rip-high-friday`, `ts-fay-azores-no-formation`, `moon-72-springs-full-sept-26`, `topsail-fp-sept-1-twenty-days`

**Post record, 2026-09-21.** The digest for No. 47 posted at **7:00:01 a.m. ET**, held 8 minutes by `--not-before 07:00` from a 6:52 foreground start (message 1551548549504827462, 1098 embed chars, hero attached, `degraded: []`). Both papers were live on Pages by 5:56 (dated Times and Sports pages both 200), six minutes after the 5:50 push. Sports & Sportsman No. 37 was published with the Times and not posted, per the standing rule. The 7:04 backup `send_later` wake (trig_011ic7s8iyDb7fD22E7mvVh1) was deleted after the record landed. The session was held in the foreground with `hold_until.py` in nine-minute windows from 5:50 to 6:52 rather than idled to a wake, as on 09-20. Unifor-Stellantis was re-checked at 6:00 (CBC Windsor and business feeds): no outcome reported.

## 2026-09-22 — No. 48 (Times) and No. 38 (Sports & Sportsman)

| Open-ended | **Twenty-seventh morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water) launched 5:37 and filed 5:40-5:49 a.m. ET. Times validated 5:48 on the second pass (first pass failed only on the not-yet-drawn art file); Sports & Sportsman validated 5:50 on the second pass (first pass: "2-0 Bengals", "1-1 Browns" and a "32-46 start" read as scores without `result` — rewritten in words; and the deer-and-bear archery entry's "farther out" clause named the Oct. 10 fall turkey date, which the validator checks against the species named — cut). Both pages were 200 on Pages 30 seconds after the 5:50 push. HEAD was detached from main at session start again — twenty-third occurrence; `git checkout main && git pull` fixed it. `config.head_start_minutes` reads 90. **A desk left three curl scratch files (`art_downs.txt`, `art_kudus.txt`, `art_mex.txt`) in the repo root and `git add -A` committed them; removed in 7af0271 two minutes later.** Desk prompts tomorrow should say: write scratch ONLY to the session scratchpad, never the repo | **standing practice — post run in the FOREGROUND with `hold_until.py` chunks, backup `send_later` at 7:04; add the scratch-path rule to every desk prompt** |
| Open-ended | **Setup: pip installed Pillow first try; cairosvg pip-installed for viewing the drawing. Stats 4 entries (S&P 7,764.70 +1.49%, Dow 52,048.83 +0.71%, Nasdaq 27,122.09 +2.26% — the Monday close; Bitcoin $85,877 +1.70%). Standings 5 clubs, 0 errors (Pirates 79-77 third, 19.0 back, 7.0 out, W4; Reds 72-84 fifth, 26.0 back, 14.0 out, L2 — neither played Monday). USGS returned 503 on all three gauges at the 5:33 fishing fetch; a background retry loop cleared it on the second try at 5:35 — 4 waters, 0 errors.** The fetcher's "24h ago" comparison is again the two-day window's first point (Sunday 5:45 a.m., 47.5 hours back) on all three gauges; on the Williams the "rising" flag is wrong on both the day (down 168 cfs) and the morning (receding since the 4 p.m. Sunday crest); on the two Ohio gauges it happens to be right. Fifth logged instance | **fetch-fishing-24h-window-bug — still for Nate** |
| Open-ended | **The lead is the FAA outage: flights into Newark, Teterboro, Philadelphia, LaGuardia and Kennedy halted for much of Monday after a data circuit at the Philadelphia approach facility failed and an NJ Transit crew on the Delco Lead project cut the backup fiber about 9:45 a.m.** CBS New York primary (updated 11:40 p.m.), NBC New York and NBC News cross-checks (619 Newark and 197 Philadelphia cancellations by 6 p.m. per FlightAware via NBC; Flightradar24 no Newark landings 9:40 a.m. to after 5:20 p.m.). Duffy's all-clear time differed (NBC NY "just after 6", NBC News "about 5") — written "Monday evening". Cable-cut location differed (NJ Transit v Bedford) — NJ Transit's, attributed. Amtrak's "NJ Transit property" line cut for length. Held as lead candidates: Trump-Gulf leaders (today, not Monday); Xi state visit Sept. 23-25 (CGTN only — not run); NYT report that Trump called off Houthi strikes with bombs loading (NYT via Jerusalem Post, single-source — held). U.S.: CNN/MS NOW/Politico suit over the press ban, Judge Kelly hearing Wednesday (NBC — the 09-20 lead moved forward); Trump-Mamdani at Gracie Mansion on Sunnyside Yard (ABC7); Yosemite Dome Fire helicopter crash, two contractor pilots dead Sunday (ABC); Bessent's Sept. 23 Iranian-airline cutoff (The National — CNBC and Al Arabiya blocked; AJ has the same). World: Typhoon Dujuan, four dead per NHK (AJ); German state votes Sunday — AfD 38.2% in Mecklenburg, Linke 25.7% in Berlin (Euronews, AJ concurs); Hurricane Polo 150 mph at 3 a.m. CST (NHC advisory 7 — primary); Houthis v Yemeni forces in the Kahboub Mountains, WHO 674 dead since Aug. 6 (AJ; ToI's "150 in two days" is a different window — not merged). Held: UK's first Rwanda genocide charge (CPS primary — swap-ready); EU sanctions renewal deadline (Kyiv Independent); China expels Zhang Youxia (AJ) | **watch: FAA outage cause/NJ Transit findings; Kelly hearing Wednesday; Xi visit Sept. 23-25; final Duma results Friday; Polo landfall track; EU sanctions outcome; Trump-Gulf/UNGA speech** |
| Open-ended | **Art: RUNG 1, `placement: lead`.** CBS New York's og:image is a Getty photograph of the Newark apron: a United widebody taxiing left before the lower Manhattan skyline with One WTC, a narrowbody beyond, an Allied Aviation fuel tanker (309) hosed to a regional jet parked nose-on at gate 113, a jet bridge with a dark hood. No people in the photograph. `scratchpad/draw.py`, 317 paths, 31 KB; viewed with cairosvg, one revision (fuselage taper, skyline moved above the fuselage line, gate sign shifted clear). Tenth rung-1 drawing in a row | |
| Open-ended | **Notebook: 4 statewide, 3 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley), away 1, hotspots 2 — six lines.** Statewide: PSC orders Black Diamond and Appalachian Power into 10-day sale talks, no receiver (MetroNews, Monday — the hearing outcome); grand jury indicts Noel Devine, arraignment Wednesday replaces the preliminary hearing (MetroNews); Morrisey's record $9.4B tourism figure, 78.4M visitors (WSAZ); Kanawha judge approves the $9.1M State Police hidden-camera class settlement, signed Sept. 16 (Gazette-Mail, dated). **WV MetroNews ANSWERS — first use in ten mornings** (curl -A on the front, WebFetch on articles). Regional: Overstreet murder trial opens in Cabell (WSAZ); Hurricane Middle School scaled back over budget (WSAZ, Tuesday a.m.); Wood County high water on Core Road, Harris Highway, slides on Pond Creek and Lee Creek roads Monday (News and Sentinel). Empty: nicholas_webster (WOAY newest Sept. 10; Webster items went to the cabin block) and summers_new_river (Hinton News stops Aug. 30; WVVA/Register-Herald nothing). Away: Act 250 coordinator's Sept. 15 jurisdictional opinion on the 157-unit Monument Place project in the old Energizer plant (Banner, Monday). Cabin: county commission 2-1 on Sept. 16 for $10,000 to the Cowen VFD's new firehouse (Echo, Monday). Topsail: Pender commissioners' Monday agenda in Hampstead carried a public hearing on rezoning 32 acres in Topsail Township for a wastewater plant (Port City Daily — an agenda preview, written as such; the WECT cyberstalking-charge line was the desk's first choice and was set aside as not a beach-week fact). **No WV Mason/Cabell flood-damage story was found Monday; the Ohio-corridor damage was Meigs County, Ohio.** Alternates: MetroNews flood watch extended to 28 counties, Lewis County 800 without power (held — third MetroNews URL); CSX 1,100 furloughs (WCHS, union-only); Dunbar Toll Bridge head-on, two dead (WSAZ — Gazette-Mail said one; not run); Caserta retiring Oct. 1 (Sept. 16; live Thursday with the commission vote); Campbells Creek residents (no official); Bennington five-arrest drug bust Sept. 15; Shaftsbury barracks planning; Webster BOE vape K-9 Sept. 14 and Camden water records (Echo, paywalled past the lede); NTB new website Sept. 16. **northtopsailbeachnc.gov relaunched Sept. 16: `/news` and `/meetings` now 404, `/m/newsflash` works** — edition.md §3a needs that URL updated | **watch: Kelly/Devine Wednesday; Caserta seat Thursday; Black Diamond 10-day timeline (Oct. 1); HB 2014 Sept. 28; Putnam commission Sept. 29; Cowen firehouse; flood watch through Wednesday 8 a.m.** |
| Open-ended | **Canada 2/2/2.** PG: $9.2M Red Rock weigh-scale rebuild by Dec. 2027 (CKPG); hospital district presses for an on-site UHNBC helipad, $20-30M (CKPG). BC: Rustad and four others rejoin the Conservative caucus Monday under Doerkson, who meets reporters in Richmond today (CKPG; CBC names Halford, McInnis, Hepner, Rattee); B.C. and SD59 sue OpenAI in California over the Feb. 10 Tumbler Ridge shooting (CBC BC). Canada: C-39 Building Canada Strong Act tabled Monday (CBC); Belleville police name Sean Ward, 29, and Const. Jeff Smith (CBC — shot counts CP 30 v CBC 20 bullet holes, neither run). Held: PG advance voting Oct. 7-15 with nine mayoral candidates (CKPG — a third PG brief if wanted); Tilbury LNG approval; Federal Court refuses to strike the youth climate suit (Friday ruling); Smith on the separation ads. Unifor-Stellantis: still nothing newer than Sept. 17 on CBC Windsor. PG Citizen 403 on curl and WebFetch | **watch — Doerkson in Richmond; Findlay byelection Sept. 26; Quebec debate Wednesday; PG advance polls Oct. 7; C-39 second reading; OpenAI response** |
| Open-ended | **Sumo, Aki Day 10 — JSA leaders page, torikumi JSON Days 10 and 11, absence page.** **Onosato alone at nine and one** (yorikiri over Hakunofuji); Atamifuji, Fujinokawa, Kinbozan at eight and two; **Atamifuji beat Kotozakura (oshidashi), Fujiryoga beat Kirishima (5-5), Aonishiki beat Churanoumi** (out of the chase at 7-3). No new kyujo. Day 11: Onosato v Fujinokawa, Kirishima v Atamifuji, Kotozakura v Roga, Kinbozan v Asanoyama, Aonishiki v Takanosho. Kagayaki 10-0 in juryo (not run). r/Sumo served only the interstitial; Japan Times had no Day 10 story — kimarite from the JSA feed. Every shikona checked against the JSA English feed | **Day 11 results Wednesday; Onosato v Fujinokawa is the bout** |
| Open-ended | **Our Teams: 4 briefs, 4 outlets — a Tuesday with no followed team in action Monday.** Bengals' Golden on to Pittsburgh (bengals.com, Monday); Monken turns the Browns to the Carolina opener (clevelandbrowns.com, Monday); Mac Allister on his Liverpool future (ESPN, Monday); Downs replaces Pepi on the USMNT roster (U.S. Soccer, Sunday 7 p.m. — not run Monday). Standings 13 (MLB byte-matched; PL/MLS/NFL from ESPN feeds; WVU 3-0 with 93 AP and 55 coaches points; Hannan 1-2 per MaxPreps). Upcoming 14 lines Sept. 22-27. **No Premier League fixtures Sept. 22-28 (international window per ESPN) and ESPN's Carabao Cup feed returned no ties Sept. 22-24** — Chelsea and Spurs carried by standings only. Sat out: Spurs (media day Sept. 28 still unconfirmed; ESPN lists the first preseason game Oct. 8 v Atlanta). **Hannan: fifth morning with no Sept. 17 Westside score; MaxPreps' Sept. 21 Westside-at-Hannan listing shows no score on either page — not printed; ask Ian.** wvusports.com, herdzone.com, ohiobobcats.com, big12sports.com, sunbeltsports.org all served sub-1KB bot pages — no Rodriguez/Marshall/Ohio presser or weekly awards read. Alternates: Kudus withdraws from Ghana (ESPN, body did not render); Crew 2/Higuain referees' complaint (Sunday) | **hannan-westside-score / hannan-sept-21-maxpreps — owed; conference weekly awards need a source that renders** |
| Open-ended | **Leagues: 8 briefs.** Sumo 3; NFL 2: Rams 28-6 Giants, Stafford 327/4, Adams 195, Donald back after 981 days (PFT); Dart sprained-MCL report, MRI Tuesday (PFT, NFL Network attributed). MLB 2: Orioles 4-3 Blue Jays, Cleveland a game up with a magic number of six (Stats API); Red Sox clinched Sunday on the Astros' loss (CBS, dated Sunday — the 48-hour exception). CFB 1: LSU's Spears out for the season (CBS, "citing sources"). Held: Tigers 9-2 Nationals, Giants 5-2 Twins; Rangers a game up on Houston; Kagayaki 10-0. **ESPN's site.api scoreboards returned Akamai "Access Denied" to the Leagues desk and worked for the Teams desk with curl's default UA** — note the UA in tomorrow's prompt | **standings-gate — no NL Central figure in Leagues; Carabao Cup results Wednesday** |
| Open-ended | **Outdoors: all four waters, and the story is the Ohio.** **Huntington 33.36 ft at 5 a.m., rising — up 4.83 on the day, past Sunday's 30.8 forecast crest at 4 p.m. Monday; NWPS (issued 12:10 a.m.) now crests it at 35.6 ft at 2 p.m. TODAY, holding through 8 p.m., no flooding category, action 48.** Point Pleasant 28.79 rising, up 2.82; Flood Warning on Mason/Jackson/Wood until 9 a.m. ("significant flooding continues, numerous roads closed"); Flood Watch reissued 2:11 a.m. through 8 a.m. Wednesday over Cabell, Mason, Putnam, Kanawha, Nicholas, Webster and ~35 more zones. Williams 582 cfs / 3.08 ft, receding ~100 cfs a day from the 1,560 crest; the 300-500 seam band is Wednesday-Thursday at that rate. Gauley above Belva 2,860 cfs at 5 a.m. on rain (Tuesday is not a listed release day). Topsail: sound H 5:15 AM 3.3, L 11:34 AM 0.7, H 5:55 PM 4.0, L 12:17 AM (Wed) 1.0; 81.0F Beaufort; moon 81%, 10.5 days, full Sept. 26 16:49 UT; no NC alerts, rip LOW today, MODERATE Wednesday, **HIGH Thursday-Saturday** (3-6 ft Thursday on a north wind ~20); NHC: Fay near the Azores, an African wave 0/30%. **Fisherman's Post and Coastal Angler still Sept. 1, 21 days old.** Seasons: archery deer/bear/boar Sept. 26 (4 days); ducks/coots/mergansers Oct. 3-11 and geese Oct. 3-18 from the migratory PDF (re-downloaded, PyMuPDF); bear gun third window Oct. 3-9; squirrel Day 11; dove Day 22; going_out: bear gun second window closes Friday. NC limits re-copied from the NCDMF page (effective Sept. 2); flounder CLOSED through Sept. 30 re-confirmed. **Gauley window Sept. 25-28 still unconfirmed from the operating agency: USACE cert failure, NPS 404, AW 404; riverscout.app lists Friday Sept. 25 as Day 9 (2,800 cfs, 7-3) but calls its own 2026 schedule unverified; WV Explorer's Aug. 26 story has six weekends from Sept. 11 without itemizing them** — printed as reported | **watch — Huntington crest 2 p.m. today, 35.4 at 2 a.m. Wednesday; Williams into the 300-500 band; HIGH rip Thursday-Saturday at Topsail; Fisherman's Post October report; a Gauley source; flood watch through Wednesday 8 a.m.** |
| Open-ended | **Sci/Tech and AI.** Pulsar J1740+1000's 42-light-year X-ray tail from Einstein Probe explains LHAASO's orphan gamma rays, Science China (Phys.org); Perseverance SuperCam finds three wetting episodes across 185 Margin Unit targets, Purdue-led, Communications Earth & Environment (NASA); stopping GLP-1s raises cardiovascular risk 22% at two years in 333,687 veterans, WashU, BMJ Medicine (Science Daily); Super Heavy B21 at the Starbase pad for Flight 14, NET Sept. 28 pending an FAA license change, 26 Starlink V3s (Spaceflight Now). AI: Newsom signs seven data-center water and power bills (Register); OpenAI's nine-mathematician IAS advisory group and its own "100-plus open problems" claim, attributed as the company's (TechCrunch — the Navier-Stokes claim deliberately left out); UN scientific panel says safeguards lag capabilities, citing the July OpenAI/Hugging Face incident (AFP via TechXplore). Held: gentoo penguins split into four species (Science Daily, second SD URL); FDA approves Ionis' Zanvastro for Alexander disease (no journal, no date on page); Roman telescope camera power-up; EU A-to-G data-center energy label (AFP); Amazon blocks Meta's Muse agent. Sanders/Casar bill still not introduced per sanders.senate.gov | **watch — Starship Flight 14 Sept. 28; Sanders/Casar bill; EU energy label; 20-country AI oversight declaration (AJ, UNGA)** |
| Open-ended | **Source status.** OPEN: CBS (NY and national), NBC (NY and national), ABC (7NY and national), Al Jazeera, Euronews, NHC, Times of Israel, Jerusalem Post, Kyiv Independent, CPS (UK), The National (UAE), NASA, Phys.org, Science Daily, Medical Xpress, TechXplore, EurekAlert, Spaceflight Now, Register, TechCrunch, 404 Media, sanders.senate.gov, CIDRAP, **WV MetroNews (first time)**, WSAZ, WCHS, WTAP, WVVA, WOAY, Register-Herald, News and Sentinel, WV Watch RSS, Gazette-Mail (curl), Herald-Dispatch (curl), Webster Echo (WebFetch, paywalled past the lede), Hinton News (stale), WECT, Port City Daily, Pender civicalerts, Surf City civicalerts, NTB `/m/newsflash`, Bennington Banner, CKPG, CBC (RSS + articles), CHEK, JSA leaders/torikumi/absence, ESPN JSON (default curl UA only), MLB Stats API, MaxPreps, bengals.com and clevelandbrowns.com (with a UA), ESPN.com article pages, ussoccer.com, NBC/PFT, CBS Sports, USGS, NWPS HNTW2, api.weather.gov, ILM SRF, NHC, NCDMF, USNO, wvdnr.gov migratory PDF (curl), Fisherman's Post and Coastal Angler feeds, fs.usda.gov alerts, riverscout.app, wvexplorer.com. BLOCKED: Reuters/AP/BBC/Guardian (not tried), CNN (451), CNBC, Al Arabiya, usnews.com (503), NPR Up First (503), OHCHR (403), Axios (403), PG Citizen (403), My PG Now, Express-News (stale), nba.com/spurs (empty), wvusports/herdzone/ohiobobcats/big12sports/sunbeltsports (bot pages), old.reddit.com/r/Sumo (interstitial), Japan Times (no Day 10 story), Sky Carabao page (404), si.com CFB (404), USACE Huntington (cert), NPS Gauley (404), AW calendar (404), NWPS PTPW2 (404), northtopsailbeachnc.gov `/news` and `/meetings` (404 since the Sept. 16 relaunch), topsailbeachnc.gov news (404) | **watch — MetroNews (now open); a Gauley source; college athletics sites need a rendering path** |
| Open-ended | **Traps dodged.** (1) Duffy's all-clear time 5 v 6 p.m. — "Monday evening". (2) Cable-cut location NJ Transit v Bedford — attributed. (3) ABC7's summarizer labeled the Mamdani meeting "Monday, September 22" — datePublished says Sept. 21. (4) NHC's EP3 refresh URL served Post-Tropical Marie from Sept. 8 — rejected; Polo is EP2. (5) UN News Iran-mission story is Sept. 17 — held. (6) Witkoff/Kushner Kyiv trip surfaced by search was Sept. 6. (7) Yemen toll windows (WHO 674 since Aug. 6 v ToI 150 in two days) — only WHO, attributed. (8) Gazette-Mail FEMA request is Sept. 15 and about August. (9) Pender commissioners met Monday, not tonight — written as an agenda item. (10) Meigs County flood damage is Ohio — no WV Mason line manufactured. (11) Bennington bust "Tuesday" = Sept. 15. (12) Belleville shot counts CP 30 v CBC 20 — neither. (13) Rustad's "95 per cent" is his estimate — not laundered. (14) Kirishima "yokozuna run" — 5-5, not written as a run. (15) "2-0 Bengals" read as a score by the validator — words. (16) Fall turkey Oct. 10 inside the deer-bear archery entry — cut. (17) Fetcher's "rising" on a Williams down 168 cfs — both printed, labeled. (18) Sunday's 30.8 Huntington crest passed Monday — the new NWPS forecast printed, not the stale one. (19) riverscout's Sept. 25 release — reported, with its own "unverified" caveat. (20) Gauley 2,860 cfs on a non-release day — rain, not a release. (21) OpenAI's Navier-Stokes claim — left out. (22) The MNF venue — PFT does not name it, so neither does the brief. (23) Xi visit dates — CGTN only, not run. (24) Three curl scratch files committed by `git add -A` — removed in the next commit | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-22** | **Aki Day 10 (ran); Hannan at Calvary 6 p.m. (venue unconfirmed); Huntington NWPS crest 35.6 ft at 2 p.m.; Doerkson meets reporters in Richmond; Trump-Gulf leaders and the UNGA speech; Bessent's Iranian-airline cutoff from Wednesday; Belle pyrolysis forum 6-8 p.m.; NTB draft EIS hearing 6 p.m.** | |
| **2026-09-23** | **Devine arraignment (replaces the preliminary hearing); Judge Kelly's hearing on the press-ban suit; Xi state visit opens (CGTN — unconfirmed); third Quebec debate; North Bennington DRB; Carabao Cup third round; Dart MRI result; Aki Day 11 (Onosato v Fujinokawa)** | |
| **2026-09-24** | **Cabell commission on Caserta's seat; Hannan v Roane at Ashton 6 p.m.; Pirates v Cardinals 12:35** | |
| **2026-09-25** | **WV bear gun second window closes (selected counties); Gauley Day 9 per riverscout (unconfirmed); final Duma results expected; Reds at Blue Jays, Pirates at Tigers; HIGH rip risk at Topsail Thursday-Saturday (ILM)** | |
| **2026-09-26** | **WV archery/crossbow deer, bear and boar open; full moon 16:49 UT; USMNT v Peru 4:30 p.m. ET Orlando; Findlay byelection, Abbotsford-Mission; Ohio v Stonehill 3:30, Marshall v Gardner-Webb 3:30, WVU v Oklahoma State 7; FCC at Montreal 7:30; USSF-385 launch** | |
| **2026-09-27** | **Aki senshuraku; Bengals at Pittsburgh 1 p.m., Browns v Carolina 1 p.m.; Crew v Inter Miami 7 p.m. ET** | |
| **2026-09-28** | **Starship Flight 14 NET (pending FAA); HB 2014 data-center rules hearing; NBA media day (unconfirmed for the Spurs); Surf City e-bike focus group 6-8 p.m.; Sweden's Andersson reports** | |
| **2026-09-29** | **Putnam County Commission on the data-center resolution; Hannan at Roane 6:30; USMNT v Chile 8 p.m. ET** | |
| **2026-09-30** | **NC flounder possession closure ends (limits page)** | |
| **2026-10-01** | **Black Diamond/Appalachian Power 10-day timeline due at the PSC; Caserta retires; Hannan at Buffalo 5 p.m.** | |
| **2026-10-03** | **WV regular goose and duck seasons open; bear gun third window (3-9)** | |
| **2026-10-07** | **Prince George advance polls open (Oct. 7, 8, 14, 15)** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18); woodcock and grouse open** | |
| **2026-10-28** | **Carabao Cup fourth round, Liverpool v Chelsea, Anfield; Pender cyberstalking court date** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |

### Open threads

- **faa-fiber-cut-five-airports** — led; NJ Transit/FAA findings and Wednesday's Kelly hearing are the follow-ups. **cnn-politico-msnow-suit / trump-mamdani-gracie / yosemite-helicopter-2-dead / bessent-iranian-airlines-sept-23** — ran. **icc-sanctions / xi-visit-sept-23-25 (CGTN only) / nih-grant-veto-draft / doj-handgun-18-20 (Sept. 18) / houthi-strikes-called-off (NYT report)** — alternates.
- **typhoon-dujuan-japan-4 / germany-afd-mecklenburg-linke-berlin / hurricane-polo-cat-4-mexico / yemen-kahboub-who-674** — ran. **uk-rwanda-genocide-charge-cps / eu-sanctions-deadline-latvia / china-expels-zhang-youxia** — alternates.
- **psc-black-diamond-sale-talks / devine-grand-jury-indictment / morrisey-tourism-9-4b / wvsp-hidden-camera-9-1m** — ran. **overstreet-trial-cabell / hurricane-middle-scaled-back / wood-county-high-water-core-road** — regional. **monument-place-act-250** — away. **cowen-vfd-10000 / pender-topsail-township-wastewater-rezoning** — hotspots. **flood-watch-28-counties-lewis / csx-1100-furloughs / dunbar-toll-bridge-2-dead / caserta-retires-oct-1 / campbells-creek / bennington-drug-bust-sept-15 / shaftsbury-barracks / webster-vape-k9 / camden-water-records / ntb-website-sept-16 / onslow-cyberstalking-pender-commissioner** — alternates. **big-ditch-rv-park (RAN 09-21) / webster-memorial-miller (RAN 09-20) / webster-county-fair (RAN 09-18)** — do not re-run.
- **red-rock-weigh-scale-9-2m / uhnbc-helipad / rustad-rejoins-caucus / bc-sues-openai-tumbler-ridge / c-39-building-canada-strong / belleville-suspect-named** — ran. **pg-advance-voting-nine-mayoral / tilbury-lng / youth-climate-suit-ruling / smith-separation-ads / unifor-stellantis (still no outcome)** — alternates.
- **pulsar-x-ray-tail-einstein-probe / perseverance-three-wettings / glp-1-stopping-heart-risk / starship-flight-14-pad** — ran. **gentoo-four-species / zanvastro-alexander-disease / roman-camera** — alternates.
- **newsom-seven-data-center-bills / openai-math-panel-100-problems / un-ai-panel-safeguards** — ran. **eu-data-center-energy-label / amazon-blocks-meta-muse / sanders-casar-bill (not introduced)** — alternates.
- **bengals-golden-on-to-pittsburgh / browns-monken-carolina / mac-allister-liverpool-future / usmnt-downs-replaces-pepi** — ran. **spurs** — sat out. **hannan-westside-score / hannan-sept-21-maxpreps / kudus-ghana-withdrawal / crew-2-higuain-referees** — owed or held.
- **aki-day10-onosato-9-1 / aki-day10-atamifuji-beats-kotozakura / aki-day11-card / rams-28-6-giants / dart-mcl-report / orioles-4-3-blue-jays-cleveland-magic-6 / red-sox-clinch-sunday / lsu-spears-acl** — ran. **tigers-9-2-nationals / giants-5-2-twins / kagayaki-10-0** — held.
- **archery-sept26 / ducks-oct3 / geese-oct3 / bear-gun-oct3-9 / squirrel-day-11 / dove-day-22 / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead / bear-gun-going-out-sept25** — ran. **flounder-closed-through-sept-30 / gauley-reported-not-confirmed / mon-nf-sept-14 / stocking-none** — seasons note. **williams-582-receding / point-pleasant-28-79-rising-warning / huntington-33-36-crest-35-6-today / no-nc-alerts-rip-high-thu-sat / ts-fay-azores / moon-81-springs-full-sept-26** — water block.
- **sportsman-index-stale-no-11** — for Nate (No. 38 computed from the edition files). **fetch-fishing-24h-window-bug** — for Nate, fifth instance. **detached-head-twenty-third** — recurring. **desk-scratch-files-in-repo-root** — new; add the scratch-path rule to desk prompts. **ntb-website-urls-changed** — edition.md §3a needs `/m/newsflash`.

### Covered slugs, 2026-09-22

`faa-fiber-cut-newark-teterboro-phl-jfk-lga-monday`, `cnn-msnow-politico-sue-press-ban-kelly-wednesday`, `trump-mamdani-gracie-mansion-sunnyside-yard`, `yosemite-dome-fire-helicopter-two-pilots`, `bessent-iranian-airlines-shut-down-sept-23`,
`typhoon-dujuan-japan-four-dead-nhk`, `afd-38-2-mecklenburg-linke-25-7-berlin`, `hurricane-polo-150-mph-zihuatanejo`, `houthis-kahboub-mountains-who-674`,
`psc-black-diamond-appalachian-power-sale-talks-10-days`, `devine-grand-jury-indictment-arraignment-wednesday`, `morrisey-tourism-9-4b-78-4m-visitors`, `wvsp-hidden-camera-9-1m-settlement-ballard`,
`overstreet-trial-opens-cabell`, `hurricane-middle-school-scaled-back`, `wood-county-high-water-core-road-harris-highway`, `monument-place-act-250-exemption-sept-15`, `webster-commission-cowen-vfd-10000`, `pender-topsail-township-wastewater-rezoning-hearing`,
`red-rock-weigh-scale-9-2m-idl`, `uhnbc-helipad-hospital-district-20-30m`, `rustad-four-mlas-rejoin-caucus-doerkson`, `bc-sd59-sue-openai-tumbler-ridge`, `c-39-building-canada-strong-act-tabled`, `belleville-suspect-ward-officer-smith`,
`pulsar-j1740-42-light-year-tail-einstein-probe`, `perseverance-margin-unit-three-wettings`, `glp-1-discontinuation-22pct-bmj-medicine`, `super-heavy-b21-pad-flight-14-sept-28`,
`newsom-seven-data-center-bills`, `openai-math-advisory-group-ias-100-problems`, `un-ai-panel-safeguards-lag-hugging-face`,
`bengals-golden-on-to-pittsburgh`, `browns-monken-home-opener-carolina`, `mac-allister-no-firm-decision-liverpool`, `usmnt-downs-added-pepi-withdrawn`,
`aki-day10-onosato-alone-nine-one-yorikiri`, `aki-day10-atamifuji-oshidashi-kotozakura-kirishima-5-5`, `aki-day11-card-onosato-fujinokawa`, `rams-28-6-giants-stafford-adams-195`, `giants-dart-mcl-mri-tuesday`, `orioles-4-3-blue-jays-cleveland-magic-six`, `red-sox-clinch-sunday-astros-loss`, `lsu-spears-acl-season`,
`archery-deer-bear-boar-sept-26-four-days`, `ducks-coots-mergansers-oct-3-11`, `geese-oct-3-18`, `bear-gun-third-window-oct-3-9`, `squirrel-day-11`, `dove-day-22`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish-footnote-m`, `black-drum-sheepshead`, `bear-gun-second-window-closes-sept-25`,
`flounder-closed-through-sept-30`, `gauley-reported-not-confirmed-riverscout-day-9`, `mon-nf-sept-14`, `stocking-none`, `williams-582-receding-from-1560`, `point-pleasant-28-79-rising-mason-warning`, `huntington-33-36-nwps-crest-35-6-2pm`, `no-nc-alerts-rip-high-thu-sat`, `ts-fay-azores-african-wave-30`, `moon-81-springs-full-sept-26`, `topsail-fp-sept-1-twenty-one-days`

**Post record, 2026-09-22.** The digest for No. 48 posted at **7:00:01 a.m. ET**, held 8 minutes by `--not-before 07:00` from a 6:52 foreground start (message 1551910939056545863, 1087 embed chars, hero attached, `degraded: []`). Both papers were live on Pages at 5:51, 30 seconds after the 5:50 push. Sports & Sportsman No. 38 was published with the Times and not posted, per the standing rule. The 7:04 backup `send_later` wake (trig_014s1EBx2nfi34D39F1RwSPW) was deleted after the record landed. The session was held in the foreground with `hold_until.py` in nine-minute windows from 5:54 to 6:52, as on 09-21.

## 2026-09-23 — No. 49 (Times) and No. 39 (Sports & Sportsman)

| Open-ended | **Twenty-eighth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water) launched 5:47 from a shared `DESK_BRIEF.md` in the session scratchpad (the scratch-path rule and the blocked/open source lists in one file every desk reads first) and filed 5:49-5:57 a.m. ET. Times validated 6:01 on the third pass (first: art file not yet drawn; second: art caption 162 chars against a 140 cap — the cap is not in edition.md §4.5, only in the validator); Sports & Sportsman validated 5:59 on the FIRST pass, warnings only (the three migratory-bird species names are not in the WV reference table, as every morning). Both pages were 200 on Pages at 6:04:48, about 40 seconds after the 6:04 push. HEAD was detached from main at session start again — twenty-fourth occurrence; `git checkout main && git pull origin main` fixed it. `config.head_start_minutes` reads 90. `git status` was run before `git add -A`; nothing stray | **standing practice — post run in the FOREGROUND with `hold_until.py` chunks, backup `send_later` at 7:04** |
| Open-ended | **Setup: pip installed Pillow first try; cairosvg pip-installed for viewing the drawing. Stats: 4 entries but the three indices were STILL Monday's close at 5:43, 5:48 and 5:58 (Yahoo's Sept. 22 bar has a null close; `regularMarketTime` stuck at 3:09 p.m. Tuesday) — `stat_strip` ran `[]`, logged in FAILURES.** Standings 5 clubs, 0 errors (Pirates 80-77 third, 18.0 back, 7.0 out, W5; Reds 73-84 fifth, 25.0 back, 14.0 out, W1). Fishing 4 waters, 0 errors on the first try at 5:43. The fetcher's "24h ago" comparison is the two-day window's first point on all three gauges and every flag is wrong on the morning's direction — sixth logged instance | **fetch-fishing-24h-window-bug — still for Nate; stats-yahoo-stale-close — new, watch Thursday** |
| Open-ended | **The lead is Trump's U.N. speech and the overnight U.S.-Iran talks: "deal or annihilate," then about three hours of mediated talks by Witkoff and Kushner, Pezeshkian arriving to speak Wednesday.** CBS primary (Watson, 7:38 p.m.), NBC cross-check (3:15 a.m.), ABC and Al Jazeera for the talks and Iran's armed-forces response; Rezaei's Hormuz conditions from the CBS live blog. Held: Xi's Thursday visit (CBS in passing, CGTN detail only), Trump-Zelenskyy (went to World), Shield of the Americas pact (alternate). U.S.: DOJ filing before Kelly's Wednesday hearing (NBC — the press-ban thread moved); 17,500 refugee slots primarily for Afrikaners (CBS); diesel record $6.52 on the Iran swings (NBC); FBI investigating a possible FBIjobs.gov breach (ABC, sourced). Alternates: ICE officer in Austin wore no body camera (NBC); Marist generic ballot 53-41 (PBS); Utah letter carrier charged over 300 ballots (CBS); Missouri map emergency appeal. World: Polo peaked 175 mph, 155 at 3 a.m. Wednesday, core offshore (NHC advisory 11 — the search summary said "Category 5 early Wednesday"; the advisory said Category 4); Kiir dissolves South Sudan's government before the Dec. 22 vote (AJ); Sri Lanka Easter-bombing convictions, 15 (AJ — AFP says 220-year sentences followed; AJ's page stopped at conviction, so did the brief); Zelenskyy's energy-ceasefire offer after Trump (Kyiv Independent). Alternates: Durban homestead 11 dead; Turgutlu school shooting 11 hurt; Shield of the Americas; Libya El Sharara pipeline | **watch: Pezeshkian speech; second U.S.-Iran round; Kelly ruling; Xi visit Thursday; Polo; Morocco vote results; final Duma results Friday; Greenland deal signing (Euronews page dated oddly)** |
| Open-ended | **Art: RUNG 1, `placement: lead`, with the speaker LEFT OUT.** Both lead photographs (CBS: AP/Seth Wenig; ABC: Smialowski/Pool/AFP via Getty) are a face at the rostrum, which may not be drawn. Drawn instead: the General Assembly rostrum itself from the ABC frame — the staggered serpentine slabs, the lectern with rail and two crossed microphone stalks, the control box, the U.N. emblem in gold on the black marble front cropped by the frame, hatched dark to separate it from the wall. `scratchpad/draw.py`, 287 paths, 29 KB; one revision (front hatching, calmer veining). Eleventh rung-1 drawing in a row; the aria-label and the SVG comment both say the speaker is not drawn | |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley, summers_new_river), away 1, hotspots 2 — seven lines.** Statewide: crane malfunction kills a worker at the I-79 bridge site, Marion-Monongalia line (WSAZ; the headline said "vehicle accident," the State Police update said crane — MetroNews agreed); Mullican Flooring closing Ronceverte, 70 jobs, WARN notices Monday (MetroNews); justices hear the de Soto vacated-seat case (MetroNews; the News and Sentinel dated it Sept. 23, three outlets said Tuesday); state school board v HB 2755 rule-review law (News and Sentinel). Regional: Huntington police charge a 20-year-old in the Sept. 17 31st Street shooting (MetroNews); a Richmond Elementary aide and a Dunbar Middle sixth-grader die in separate South Charleston crashes Monday (MetroNews — WSAZ's page 403); Route 50 eastbound guardrail crash closed two lanes Tuesday (WTAP — thin, but Tuesday's and sourced); Summers grand jury indicts a Pipestem man on 21 counts (Hinton News — **Summers files for the first time since Sept. 18**). **Nicholas-Webster empty a FOURTH morning**: WOAY, Register-Herald, WVVA, Hinton News, Nicholas Chronicle (May), nicholascountywv.org, WCHS Summersville, two searches; the Webster items went to the cabin block. Away: BCRC adopts the Act 181 regional plan Sept. 17 — projects of 50 or fewer homes in North Bennington skip Act 250 (Banner). Cabin: Woo-Hoo LLC tells the commission Sept. 16 it is prepared to sue over a ~$160,000 property-tax dispute (Echo, Monday). Topsail: Monday's Pender commission meeting collapsed without a quorum, two of four members absent, four public hearings and a $1.2M water contract delayed (Port City Daily) — **so the Topsail Township wastewater rezoning hearing No. 48 printed as Monday's agenda almost certainly did not happen; PCD does not name the four hearings, so the line stops at that**. Alternates: Caserta's seat Thursday (H-D); Camden water works receivership issues (Echo); Corps terminal-groin recommendation at New River Inlet, comments to Oct. 19 (WWAY, undated); Bennington cruiser struck Sept. 11 (Banner); PSC on Gauley River PSD (Fayette — MetroNews). Devine's arraignment is today; nothing moved by 5:52. No Black Diamond movement. No WV Huntington-crest road or lock story found; WSAZ's Tuesday flood coverage was Ohio-side | **watch: Devine arraignment result; Kelly; Caserta seat Thursday; Black Diamond Oct. 1; HB 2014 Sept. 28; Putnam commission Sept. 29; Pender commission quorum (next meeting); NTB DEIS hearing report; Nicholas-Webster needs a working source** |
| Open-ended | **Canada 2/2/2, and the story is a snap B.C. election: Eby dissolved the House Tuesday for Saturday, Oct. 24, one week after the Oct. 17 civic vote.** PG: RCMP link four masked robberies of vape and cannabis stores Sept. 6-19 (CKPG); civic candidates Polillo and Bell say the provincial vote will drown out the local race — nine mayoral, 18 council candidates (CKPG). BC: Eby's call, $83M-$84M cost per Doerkson (Global — WebFetch got the body, curl only comments); Squamish council rejects the $142M Woodfibre LNG tax deal 5-2 (CBC BC). Canada: Belleville suspect Sean Ward died Monday night in Kingston, SIU (CBC); Carney defends C-39's strike-ending clause against the CLC (CBC). Alternates: Modi December visit and the India trade deal by the G20 (CBC); Doerkson "united," three NDP ministers not running (CP via CKPG); McLaren's tax-freeze council bid (CKPG); four mayors object to the election date (CBC BC). **The Findlay byelection Sept. 26 is presumably moot with the House dissolved — confirm before mentioning it again.** WebFetch on CBC 403s; curl with a Chrome UA works. PG Citizen 403 | **watch — Elections BC nominations for the three PG ridings; Quebec third debate tonight (CBC Montreal); OpenAI response; Unifor-Stellantis; PG advance polls Oct. 7** |
| Open-ended | **Sumo, Aki Day 11 (WEDNESDAY Sept. 23 in Tokyo — the desk prompt had called it Tuesday; the JSA header corrected it) — JSA leaders, torikumiAjax Days 11 and 12, absence page.** **Onosato alone at 10-1** (yorikiri over Fujinokawa); all three 8-2 chasers lost — Kirishima beat Atamifuji (yorikiri, hours after the Japan Times wrote his yokozuna bid off), Asanoyama beat Kinbozan, Kotozakura threw Roga (uwatenage); six at 8-3 (Aonishiki, Atamifuji, Fujinokawa, Churanoumi, Asanoyama, Kinbozan). No kinboshi, no new kyujo (absence page still "as of Sept. 17"). Day 12: Onosato v Atamifuji, Asanoyama v Churanoumi, Aonishiki v Kinbozan, Kirishima v Fujinokawa, Kotozakura v Oshoma. r/Sumo not retried (interstitial); Japan Times readable to the lede only. Every shikona checked against the JSA English feed | **Day 12 results Thursday; Onosato v Atamifuji is the bout; a 10-1 leader two clear with four days left** |
| Open-ended | **Our Teams: 12 briefs, 8 outlets, nothing sat out — every followed team in a brief, a standings line or a fixture.** Reds beat the Braves 4-0 (Williamson 6 IP, three solo homers — Stats API line score); Pirates beat the Cardinals 2-0 (Jones 7 IP 1 H 9 K, fifth straight, W5 in the file); Marshall men's soccer 2-1 Eastern Illinois, Romberg 85th minute (MetroNews); WVU men's soccer 1-0 Duquesne, Walker 85th, fourth straight (MetroNews) — the two schools meet Sunday in the Mountain State Derby, kickoff uncited so not in `upcoming`; **Hannan: MaxPreps now posts the Westside match as a 5-1 Hannan win, record 2-2, dated MONDAY Sept. 21 at Ashton with "final score provided by J. Hughes" (user-submitted), while the coach's schedule had Westside at Beckley Sept. 17 — printed as "in a match MaxPreps dates Monday," attributed throughout; Westside's page agrees on the score. ASK IAN which date and venue is right and fix `reference/hannan-soccer-2026.json` (both repos)**; Tuesday's Calvary Baptist match (MaxPreps puts the school in Hurricane) had no score on either page at 5:50. Bengals: Dax Hill's 10 tackles and four PDs a first for a club cornerback (bengals.com); Browns sign Barnes, Boston a Rookie of the Week nominee (clevelandbrowns.com); Estevao at a Brazil presser on his Chelsea minutes (ESPN); Robertson on Liverpool after Jota's death (ESPN, The Overlap); Ohio's Hauser on Stonehill (Athens Messenger — first use); Spurs' Paris and Manchester games sold out (ESPN); U.S. Soccer to honor Ream before Chile Sept. 29 (ussoccer.com). Standings 13 (MLB byte-matched; PL/MLS/NFL from ESPN feeds; Hannan 2-2 per MaxPreps). Upcoming 15 lines Sept. 23-29; the MLB regular season ends Sunday. No PL fixtures to Oct. 3 (international window); ESPN's Carabao Cup feed shows the third round was Sept. 15-17 (Liverpool 3-1 Tottenham) — **the ledger's "Carabao Cup third round Wednesday" row was wrong; the fourth round is Oct. 28.** ESPN JSON: default curl UA, `--compressed`, single dates only (ranges return empty) | **hannan-westside-date-venue — ASK IAN; hannan-calvary-score — owed; Mountain State Derby kickoff Sunday — find a time** |
| Open-ended | **Leagues: 9 briefs.** Sumo 3; NFL 2: Dart could miss the season, possible surgery (NFL Network via ESPN, attributed), Winston starts; Jets sign Levis to the practice squad, Daniels to specialists, Mariota starts (ESPN). MLB 3: Guardians 3-2 Red Sox, sixth straight, magic number five (Stats API — Houston's feed magic number of 1 while tied with Texas was rejected as impossible and not printed); Astros 7-0 Mariners to catch Texas at 78-79; Phillies 6-4 Brewers with the Cubs and Padres losing to level the NL wild cards (no NL Central record, GB or ordinal printed — the Cubs' 8-2 loss score deliberately omitted). CFB 1: Sanders removes several Colorado players for conduct (ESPN). Held: Rays-Yankees doubleheader split, Toronto-Baltimore rainout to a 1:35 Wednesday makeup, Colorado's 100th loss, Packers/Falcons injury notes read only as feed summaries. Sky's Carabao results page 404 | **standings-gate — no NL Central figure in Leagues; Guardians clinch watch; Dart surgery decision** |
| Open-ended | **Outdoors: all four waters, and the Ohio has turned.** **Williams 1,450 cfs / 4.39 ft at 5:15, receding from a NEW crest of 2,610 cfs and 5.69 ft at 9:30 p.m. Tuesday** (a thousand over Sunday's), about 100 cfs an hour and slowing; the 300-500 seam band is the weekend at the earliest. **Point Pleasant 26.09, back to pool, down 2.70 on the day** from a 28.91 crest at 8:30 a.m. Tuesday (flagged "steady"). **Huntington 31.94, crested 33.97 (USGS) / 34.05 (NWPS) at 2:15 p.m. Tuesday, 1.55 ft under the 35.6 forecast No. 38 printed**; the 9:34 p.m. NWPS forecast has 32.3 at 8 a.m. today falling to 27.0 Sunday night, no flooding category. The 8 a.m. Wednesday Flood Watch is gone; the only WV product is a new watch to 10 p.m. on nine southern zones, none of the crew's. Gauley above Belva has held 2,770-3,290 cfs since 4 p.m. Monday and the dam gauge stepped up in discrete jumps — the shape of a release, not stated as one; riverscout lists Friday Sept. 25 (7-3, 2,800) as Day 9, still unconfirmed from the Corps or NPS. Topsail: sound L 12:17 AM 1.0, H 6:09 AM 3.5, L 12:24 PM 0.7, H 6:42 PM 4.1; 79.5F Beaufort; moon 89%, 11.6 days, full Sept. 26 16:49 UT (USNO); **Beach Hazards Statement on Coastal Pender today, moderate rip and a longshore current; HIGH Thursday-Saturday, 3-6 ft Thursday-Friday on a north wind ~20**; NHC: one African wave 20/40%, Fay gone from the outlook. **Fisherman's Post and Coastal Angler still Sept. 1, 22 days old.** Seasons: archery deer/bear/boar Sept. 26 (three days); ducks/coots/mergansers and geese Oct. 3 and bear gun third window Oct. 3-9 (ten days); **crow Oct. 1 added (eight days)**; squirrel Day 12; dove Day 23; going out: bear gun second window closes Friday (two days). NC limits re-copied from the NCDMF page (effective Sept. 2); flounder closed through Sept. 30 re-confirmed. Migratory PDF re-downloaded and read (PyMuPDF) | **watch — Williams into the 300-500 band; HIGH rip Thursday-Saturday at Topsail; Gauley Friday; Fisherman's Post October report; a Corps or NPS source for the Gauley** |
| Open-ended | **Sci/Tech and AI.** Seven meta-analyses, 3M-plus participants, no causal acetaminophen-autism/ADHD link, Santiago de Compostela, DMCN (Medical Xpress); heat-wave season 39 days longer 1979-2023, CAS, Nature Climate Change (Phys.org); NASA sets Crew-13 for 11:10 a.m. EDT Oct. 1, crew to KSC Sept. 26 (NASA blog); olive ridley nests at Seal Beach and Huntington Beach, NOAA's first West Coast sea-turtle nesting (ABC7 LA — no fisheries.noaa.gov page found). AI: Anthropic's Opus 5.5 (20% cheaper, "matches Fable on most tasks") and OpenAI's GPT-6 Sol and Luna hours apart — every claim attributed to its maker, the AFP piece has no independent benchmark (AFP via TechXplore); Meta routes Muse agent calls to human call-center workers in testing (404 Media, internal comms, Meta statement); a 510(k) triage algorithm would cut FDA device recalls 32.9%, IU/Harvard, Management Science (Medical Xpress). Held: Beta Pictoris b auroral radio bursts (preprint); Lake Powell record low 3,517.24 ft (Science Daily); the 63C amoeba (looks like a re-announcement of a Dec. 2025 Nature paper — held); OpenAI's global-standards call and Altman's UNSC briefing (AFP); OpenAI training contractors fired for using AI (404 Media, second URL). Sanders/Casar bill was introduced Sept. 3 — stale, retire the thread. EurekAlert returned a 118-byte page; The Register's AI index gave no article links | **watch — Crew-13 FRR and crew arrival Sept. 26; Starship Flight 14 NET Sept. 28 (no license yet); Sonnet 5.5/Haiku 5.5 "in the coming weeks"; Altman at the UNSC** |
| Open-ended | **Source status.** OPEN: CBS, NBC, ABC (7NY, LA, national), Al Jazeera, Euronews, DW (top page), PBS, Kyiv Independent, The National, NHC (advisory and archive), NASA, Phys.org/TechXplore/Medical Xpress (WebFetch; curl gets a challenge page), Science Daily, CIDRAP, 404 Media (RSS), TechCrunch, sanders.senate.gov, WV MetroNews (second morning), WSAZ (one 403 page), WCHS, WTAP, WVVA, WOAY, Register-Herald, News and Sentinel, WV Watch RSS, Gazette-Mail, Herald-Dispatch, Hinton News (current again — Sept. 22), Webster Echo (WebFetch, lede), WECT, WWAY, Port City Daily, Pender and Surf City civicalerts, NTB `/m/newsflash`, Bennington Banner, CKPG, CBC (curl with a Chrome UA; WebFetch 403), Global News (WebFetch only), CTV front, JSA leaders/torikumiAjax/absence, Japan Times (lede), ESPN JSON (default UA, `--compressed`, single dates), ESPN.com articles, MLB Stats API, MaxPreps (both schools' pages), bengals.com and clevelandbrowns.com (browser UA), ussoccer.com, Athens Messenger (first use), NBC/PFT front, CBS Sports, USGS IV, NWPS HNTW2 stageflow and gauge page, api.weather.gov (WV and NC), ILM SRF, NHC TWO, USNO phases, wvdnr.gov migratory PDF (curl), NCDMF, Fisherman's Post feed (default curl UA — a browser UA drew a Cloudflare block), Coastal Angler feed, riverscout.app. BLOCKED: Reuters/AP/BBC/Guardian (not tried), France 24 and NHK World fronts (641 bytes), Times of Israel (interstitial), CNN, PG Citizen (403), My PG Now, princegeorge.ca, EurekAlert (118 bytes), The Register AI index (no links), old.reddit.com/r/Sumo (not retried), Sky Carabao results (404), Sky Sports otherwise fine, nba.com/spurs, wvusports/herdzone/ohiobobcats (bot pages), USACE Huntington (cert), NPS Gauley (404), NWPS PTPW2 (404), northtopsailbeachnc.gov `/news` and `/meetings` (404 — edition.md §3a updated today), topsailbeachnc.gov news (404), Nicholas Chronicle (stale, May) | **watch — a Nicholas County source; CBC needs a Chrome UA on curl; France 24/NHK fronts need a different path** |
| Open-ended | **Traps dodged.** (1) The WebFetch summarizer stamped Wednesday as "Sept. 24/25" on NBC, CBS, ABC and CP pages — every brief says "Wednesday," the calendar says Sept. 23. (2) Polo "Category 5 early Wednesday" in a search summary v 155 mph/Category 4 in advisory 11 — the advisory. (3) Sri Lanka sentencing (AFP) not on AJ's page — stopped at conviction. (4) Greenland deal page dated Sept. 22 with a "Sept. 24" signing — held. (5) WSAZ's I-79 "vehicle accident" headline v the State Police crane update — the release. (6) News and Sentinel's "Sept. 23" Supreme Court date v three outlets' Tuesday — Tuesday. (7) Clagett candidate story is Berkeley, not Wood. (8) Gauley River PSD is Fayette, not Nicholas-Webster. (9) Pender rezoning hearing printed Monday as an agenda item — the meeting had no quorum; today's line says so without naming the hearings PCD does not name. (10) Robberies "approximately four" suspects — "about four." (11) Belleville "stable" is the SIU's word. (12) Aki Day 11 is Wednesday in Tokyo, not Tuesday as the prompt said. (13) Houston's impossible magic number of 1 — not printed. (14) The Cubs' loss score in an NL-wild-card brief — omitted (NL Central). (15) Hannan's MaxPreps date and venue disagree with the coach's file — attributed to MaxPreps, not asserted. (16) "16-5 in shots" and soccer records kept out of the WVU/Marshall briefs so no digit pair reads as a second score. (17) Ohio's coach quoted with a typo ("tin at QB") — paraphrased. (18) The 63C amoeba re-announcement — held. (19) Anthropic/OpenAI claims — each attributed to its maker, this desk's own maker included. (20) Stats: Monday's close under Wednesday's masthead — strip ran empty. (21) Fetcher flags wrong on all three gauges — printed as the fetcher's, directions as the traces'. (22) Both lead photographs are a face — the rostrum drawn without the speaker. (23) Art caption cap of 140 is only in the validator — cut twice. (24) The ledger's "Carabao Cup third round Wednesday" row was wrong; the round was Sept. 15-17 | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-23** | **Aki Day 11 (ran, Wednesday in Tokyo); Pezeshkian addresses the U.N.; Kelly's hearing on the press-ban suit; Devine arraignment; Quebec third debate; Toronto-Baltimore makeup 1:35 p.m. ET; Reds at Braves 7:15, Pirates v Cardinals 6:40; Beach Hazards Statement Coastal Pender to 8 p.m.** | |
| **2026-09-24** | **Aki Day 12 (Onosato v Atamifuji); Cabell commission on Caserta's seat; Hannan v Roane at Ashton 6 p.m.; Pirates v Cardinals 12:35; Reds at Braves 7:15; Xi state visit (CBS in passing); HIGH rip risk at Topsail Thursday-Saturday** | |
| **2026-09-25** | **WV bear gun second window closes (selected counties); Gauley Day 9 per riverscout 7-3 at 2,800 (unconfirmed); final Duma results expected; Reds at Blue Jays 7:07, Pirates at Tigers 6:40** | |
| **2026-09-26** | **WV archery/crossbow deer, bear and boar open; full moon 16:49 UT; Crew-13 crew arrives at KSC; USMNT v Peru 4:30 p.m. ET Orlando; Ohio v Stonehill 3:30, Marshall v Gardner-Webb 3:30, WVU v Oklahoma State 7; FCC at Montreal 7:30; Findlay byelection presumably moot (House dissolved) — confirm** | |
| **2026-09-27** | **Aki senshuraku; MLB regular season ends (Reds at Toronto 3:07, Pirates at Detroit 3:10); Bengals at Pittsburgh 1 p.m., Browns v Carolina 1 p.m.; Crew v Inter Miami 7 p.m. ET; WVU at Marshall men's soccer (Mountain State Derby, time uncited)** | |
| **2026-09-28** | **Starship Flight 14 NET (no license yet); HB 2014 data-center rules hearing; NBA media day (Spurs unconfirmed); Surf City e-bike focus group 6-8 p.m.** | |
| **2026-09-29** | **Putnam County Commission on the data-center resolution; Hannan at Roane, Spencer, 6:30; USMNT v Chile 8 p.m. ET St. Louis, Ream honored** | |
| **2026-09-30** | **NC flounder possession closure ends (limits page)** | |
| **2026-10-01** | **Black Diamond/Appalachian Power 10-day timeline due at the PSC; Caserta retires; Hannan at Buffalo 5 p.m.; WV crow season opens; Crew-13 launch 11:10 a.m. EDT, docking ~8 p.m.** | |
| **2026-10-03** | **WV regular goose and duck seasons open; bear gun third window (3-9); Premier League resumes** | |
| **2026-10-07** | **Prince George advance polls open (Oct. 7, 8, 14, 15)** | |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18); woodcock and grouse open** | |
| **2026-10-24** | **B.C. snap provincial election (called Sept. 22)** | |
| **2026-10-28** | **Carabao Cup fourth round, Liverpool v Chelsea, Anfield; Pender cyberstalking court date** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |
| **2026-12-22** | **South Sudan's first national election** | |

### Open threads

- **trump-unga-annihilate-iran-talks** — led; Pezeshkian's speech and a second round are the follow-ups. **doj-press-ban-privilege-filing / refugee-17500-afrikaners / diesel-record-6-52 / fbi-jobs-breach** — ran. **ice-austin-no-body-camera / marist-generic-ballot / utah-letter-carrier-ballots / missouri-map-appeal / xi-visit-thursday (CGTN detail only) / shield-of-the-americas** — alternates.
- **polo-175-peak-cat-4 / kiir-dissolves-south-sudan / sri-lanka-easter-convictions-15 / zelenskyy-energy-ceasefire-trump** — ran. **durban-homestead-11 / turgutlu-school-shooting-11 / libya-el-sharara-pipeline / greenland-deal-signing / morocco-vote** — alternates.
- **i-79-crane-death / mullican-ronceverte-70-jobs / de-soto-seat-supreme-court / hb-2755-school-board-supreme-court** — ran. **huntington-31st-street-charge / kanawha-aide-student-crashes / route-50-guardrail-lanes / summers-pipestem-21-counts** — regional. **bcrc-act-181-plan** — away. **woo-hoo-tax-dispute-webster / pender-commission-no-quorum** — hotspots. **caserta-seat-thursday / camden-water-receivership / ntb-terminal-groin-corps / bennington-cruiser-struck / gauley-river-psd-fayette / devine-arraignment (today) / black-diamond-oct-1 / csx-furloughs (stale)** — alternates or owed. **cowen-vfd-10000 (RAN 09-22) / big-ditch-rv-park (RAN 09-21) / webster-memorial-miller (RAN 09-20) / pender-wastewater-rezoning (RAN 09-22 — no quorum, corrected today)** — do not re-run.
- **pg-vape-cannabis-robberies / pg-candidates-snap-vote / eby-snap-election-oct-24 / squamish-rejects-woodfibre-142m / belleville-suspect-died / carney-defends-c-39-strike-clause** — ran. **modi-december-visit / doerkson-united-ndp-ministers-out / mclaren-council-tax-freeze / bc-mayors-object-election-date / findlay-byelection (moot?) / unifor-stellantis (still nothing) / openai-bc-response** — alternates or owed.
- **acetaminophen-no-causal-link / heat-wave-season-39-days / crew-13-oct-1-11-10 / olive-ridley-west-coast-first** — ran. **beta-pictoris-b-radio / lake-powell-record-low / amoeba-63c (re-announcement?)** — alternates.
- **anthropic-opus-5-5-openai-gpt-6-sol-luna / meta-muse-human-call-center / fda-510k-triage-recalls** — ran. **openai-global-standards-unsc / openai-contractors-fired-ai / argonne-molten-salt-ai** — alternates. **sanders-casar-bill** — introduced Sept. 3; retire.
- **reds-4-0-braves / pirates-2-0-cardinals-w5 / marshall-msoc-2-1-eiu / wvu-msoc-1-0-duquesne / hannan-5-1-westside-maxpreps-monday / bengals-hill-record / browns-barnes-boston / estevao-chelsea / robertson-jota / ohio-hauser-stonehill / spurs-europe-sold-out / usmnt-ream-honor** — ran. **hannan-westside-date-venue (ASK IAN) / hannan-calvary-score / mountain-state-derby-kickoff / lfc-reds-roundtable / bengals-scouting-report** — owed or held.
- **aki-day11-onosato-10-1 / aki-day11-chasers-fall / aki-day12-card / dart-possible-season-surgery / jets-levis-daniels / guardians-3-2-red-sox-magic-5 / astros-7-0-mariners-tie-texas / phillies-6-4-brewers-wild-cards-level / sanders-colorado-dismissals** — ran. **rays-yankees-split / toronto-baltimore-rainout / rockies-100th-loss / packers-falcons-injuries** — held.
- **archery-sept26-three-days / ducks-oct3 / geese-oct3 / bear-gun-oct3-9 / crow-oct1 / squirrel-day-12 / dove-day-23 / red-drum / seatrout / spanish-bluefish / black-drum-sheepshead / bear-gun-going-out-sept25** — ran. **flounder-closed-through-sept-30 / gauley-reported-not-confirmed / stocking-none** — seasons note. **williams-1450-receding-from-2610 / point-pleasant-26-09-pool-down-2-70 / huntington-31-94-crested-33-97-under-forecast / beach-hazards-pender-rip-high-thu-sat / african-wave-20-40 / moon-89-springs-full-sept-26** — water block.
- **stats-yahoo-stale-close** — new, for Nate: the strip ran empty. **sportsman-index-stale-no-11** — for Nate. **fetch-fishing-24h-window-bug** — for Nate, sixth instance. **detached-head-twenty-fourth** — recurring. **art-caption-140-cap** — validator-only rule; edition.md §4.5 should say it. **ntb-website-urls-changed** — edition.md §3a updated today.

### Covered slugs, 2026-09-23

`trump-unga-deal-or-annihilate-witkoff-kushner-talks`, `doj-white-house-access-privilege-kelly-hearing`, `refugee-17500-primarily-afrikaners-500m`, `diesel-record-6-52-brent-iran-swings`, `fbi-jobs-site-breach-investigation`,
`polo-175-mph-peak-155-cat-4-offshore`, `kiir-dissolves-south-sudan-government-dec-22`, `sri-lanka-easter-bombings-15-convicted`, `zelenskyy-energy-ceasefire-offer-after-trump`,
`i-79-bridge-crane-malfunction-worker-dead`, `mullican-flooring-ronceverte-closing-70`, `justices-de-soto-vacated-seat-moot`, `school-board-hb-2755-rule-review-veto`,
`huntington-31st-street-shooting-charge`, `south-charleston-crashes-aide-student`, `route-50-eastbound-guardrail-two-lanes`, `summers-grand-jury-pipestem-21-counts`, `bcrc-act-181-regional-plan-north-bennington-act-250`, `webster-woo-hoo-tax-dispute-suit`, `pender-commission-no-quorum-four-hearings-1-2m`,
`pg-rcmp-four-vape-cannabis-robberies`, `pg-candidates-snap-election-turnout`, `eby-snap-election-oct-24-83m`, `squamish-rejects-woodfibre-lng-142m`, `belleville-ward-died-siu`, `carney-c-39-strike-clause-clc`,
`acetaminophen-autism-adhd-no-causal-link-dmcn`, `heat-wave-season-39-days-longer-ncc`, `crew-13-oct-1-11-10-edt`, `olive-ridley-seal-beach-huntington-beach-first`,
`anthropic-opus-5-5-openai-gpt-6-sol-luna`, `meta-muse-calls-human-call-center-404`, `fda-510k-triage-recalls-32-9`,
`estevao-chelsea-brazil-presser`, `hannan-5-1-westside-maxpreps-monday-2-2`, `robertson-liverpool-jota-overlap`, `bengals-hill-10-tackles-four-pd-first`, `reds-4-0-braves-williamson-three-homers`, `browns-barnes-practice-squad-boston-nominee`, `marshall-msoc-2-1-eastern-illinois-romberg`, `ohio-hauser-stonehill-missed-tackles`, `pirates-2-0-cardinals-jones-one-hit-w5`, `spurs-paris-manchester-sold-out`, `usmnt-ream-honored-chile-st-louis`, `wvu-msoc-1-0-duquesne-walker-fourth-straight`,
`aki-day11-onosato-10-1-yorikiri-fujinokawa`, `aki-day11-kirishima-beats-atamifuji-chasers-fall`, `aki-day12-card-onosato-atamifuji`, `dart-possible-season-ending-surgery-nfl-network`, `jets-levis-practice-squad-daniels-specialists`, `guardians-3-2-red-sox-sixth-straight-magic-5`, `astros-7-0-mariners-tie-texas-78-79`, `phillies-6-4-brewers-nl-wild-cards-level`, `sanders-colorado-removes-players-conduct`,
`archery-deer-bear-boar-sept-26-three-days`, `ducks-coots-mergansers-oct-3-11`, `geese-oct-3-18`, `bear-gun-third-window-oct-3-9`, `crow-oct-1-eight-days`, `squirrel-day-12`, `dove-day-23`, `red-drum-slot`, `seatrout-slot`, `spanish-bluefish-footnote-m`, `black-drum-sheepshead`, `bear-gun-second-window-closes-sept-25`,
`flounder-closed-through-sept-30`, `gauley-riverscout-day-9-unconfirmed-belva-plateau`, `stocking-none`, `williams-1450-receding-crest-2610`, `point-pleasant-26-09-pool-down-2-70`, `huntington-31-94-crested-33-97-under-35-6`, `beach-hazards-pender-moderate-rip-high-thu-sat`, `african-wave-20-40-fay-gone`, `moon-89-springs-full-sept-26`, `topsail-fp-sept-1-twenty-two-days`

**Post record, 2026-09-23.** The digest for No. 49 posted at **7:00:01 a.m. ET**, held 8 minutes by `--not-before 07:00` from a 6:52 foreground start (message 1552273325991010344, 1089 embed chars, hero attached, `degraded: []`). Both papers were live on Pages at 6:04:48, about 40 seconds after the 6:04 push. Sports & Sportsman No. 39 was published with the Times and not posted, per the standing rule. The 7:04 backup `send_later` wake (trig_011B3V1Gfd7tQPf4QuXe1PBo) was deleted after the record landed. The session was held in the foreground with `hold_until.py` in nine-minute windows from 6:08 to 6:52, as on 09-21 and 09-22.

## 2026-09-24 — No. 50 (Times) and No. 40 (Sports & Sportsman)

| Open-ended | **Twenty-ninth morning under the digest contract.** Eight parallel research desks (lead+U.S., World, WV notebook, Canada, Sci/AI, Our Teams, Leagues + sumo, outdoors/water) launched 5:46 from a shared `desk_common.md` in the session scratchpad and filed 5:48-6:00 a.m. ET (Our Teams last, at 5:58; WV at 5:57). Times validated 5:57 on the second pass (first pass: the Parkersburg line's "Go! Retail" exclamation point read as a second sentence — reworded); Sports & Sportsman validated 6:01 on the second pass (first pass: sumo records "11-1", "9-3", "6-6" and the NFL "0-2"/"(1-1)" read as scores without `result` — rewritten in words). Both papers pushed 6:00 (32a46ee). HEAD was detached from main at session start again — twenty-fifth occurrence; `git checkout main && git pull origin main` fixed it. `config.head_start_minutes` reads 90. `git status` was run before `git add -A`; nothing stray | **standing practice — post run in the FOREGROUND with `hold_until.py` chunks, backup `send_later` at 7:04 (trig_01V9BuVJidT7pvxVjJScAxrz)** |
| Open-ended | **Setup: pip installed Pillow first try; cairosvg pip-installed for viewing the drawing. Stats: 4 entries, all three indices at WEDNESDAY's close (`as_of: 2026-09-23`) on the first try at 5:43 — Yahoo's stale-bar problem of 09-23 cleared on its own; strip ran all four.** Standings 5 clubs, 0 errors (Pirates 80-78 third, 19.0 back, 7.0 out, L1; Reds 73-85 fifth, 26.0 back, 14.0 out, L1). **Fishing: USGS 503 on Williams and Point Pleasant at the 5:43 fetch; a 20-second retry loop cleared it on the second try at 5:45 (4 waters, 0 errors) before anything was written** — third morning in nine (09-16, 09-22, today). The fetcher's "24h ago" comparison is again the two-day window's first point on all three gauges — seventh logged instance | **fetch-fishing-24h-window-bug — still for Nate; stats-yahoo-stale-close — cleared today, keep watching; usgs-first-fetch-503 — three of nine mornings** |
| Open-ended | **The lead is Xi's state visit: Trump met him on the tarmac at Andrews Wednesday evening (red carpet, honor guard, B-1 flyover), Bessent extended the Busan trade truce from Nov. 10 to Jan. 10, arrival ceremony and state dinner Thursday.** ABC wire primary, Al Jazeera and NPR (curl; WebFetch 503) cross-checks. Tied with Judge Kelly's overnight TRO ordering CNN, MS NOW and Politico's passes restored — that led U.S. instead (Al Jazeera; NBC alternate). Pezeshkian's U.N. speech (NBC, 1:42 p.m. Wednesday) was not run: no second Iran round was scheduled. U.S.: Kelly TRO (AJ); 10-year yield 5.13% highest since 2007, Brent over $103 after Barr (NBC); Missouri map at the Supreme Court a third time (ABC — NBC's summarizer said "supporters" filed; ABC's text says opponents); ICE officer in Austin had a body camera and did not wear it (NBC, two DHS officials). Polo (regained Category 5, 160 mph, advisory 15) went to World, not U.S. World: Polo (NHC — Euronews still said Cat 4, stale); Israel's Central Elections Committee bars Ra'am and the Joint List from the Oct. 27 vote, Supreme Court reviews next week (AJ); Russian strikes kill 16 across Ukraine, 282 drones (Kyiv Independent); PAM leads Morocco with 97 of 395 seats, turnout 38% (The National — AJ dated it "Thursday, Sept. 23"). Alternates: Albanese says an OpenAI agent breached a health statistics site (Euronews); Ukraine sends two North Korean POWs to Seoul (AJ); habeas hearing Sept. 30 for Garces Perez (CBS) | **watch: Xi state dinner tonight, National Archives Friday, rare-earths truce talks; Kelly's 14-day TRO and any appeal; Missouri map ruling; Israel Supreme Court on the Arab lists next week; Polo; jobless claims 8:30** |
| Open-ended | **Art: RUNG 1, `placement: lead`, with BOTH principals LEFT OUT.** Both lead photographs (AJ: AP two-shot; ABC: AP wide shot) are two faces walking the carpet, which may not be drawn. Drawn instead from the ABC frame: the fuselage across the top, the open door hatched dark, the red-carpeted airstair on its truck, the honor guard as two ranks of six contour figures (cap, head oval with no features, tunic, rifle with bayonet), and the empty carpet between them converging on the stair. `scratchpad/draw.py`, 392 paths (first pass 511 — over the 400 cap; hatching and a seventh figure cut), 38.7 KB. Twelfth rung-1 drawing in a row; the aria-label and the SVG comment both say the two presidents are not drawn | **art-caption-140-cap — caption is 139; edition.md §4.5 still should say it** |
| Open-ended | **Notebook: 4 statewide, 4 regional (huntington_cabell, putnam_kanawha, mid_ohio_valley, summers_new_river), away 1, hotspots 2 — seven lines.** Statewide: Morrisey flood emergency in Boone and Lincoln, water rescues (WSAZ, late Wednesday); PSC opens the Hope Gas 4% leak-repair rate hearing, $4.37 a month, 1,460 leaks (MetroNews); justices weigh whether courts can hear the 33-congregation Methodist property fight (MetroNews); Harpers Ferry woman, 55, charged with murder and arson in the Sept. 30, 2025 fire (WTAP). Regional: Chris Chiles, three decades a Cabell prosecutor and nine years a circuit judge, died this week (MetroNews); Clay County man faces three malicious-wounding counts after a Dutch Ridge Road stabbing near Clendenin (WSAZ); Toys R Us opening in October at Grand Central Mall (WTAP — thin, but Wednesday's and sourced); **Summers: the superseding indictment, 394 counts, 59 women, 11 years (MetroNews) — the movement on yesterday's 21-count line, which was the 2022 indictment; ages disagree (Hinton News 30, MetroNews 34), so no age printed**. **Nicholas-Webster empty a FIFTH morning**: WOAY tag (Sept. 10 newest), WCHS topics, Register-Herald, WVVA, lootpress, Nicholas Chronicle (May), nicholascountywv.org, summersvillewv.org, Nicholas schools, DOH; WVNS/WOWK county pages 403. Away: MMA tanker separated from its cab on Route 9 in Woodford Monday, road closed into Wednesday night (Banner). Cabin: Webster BOE approved middle-school girls softball Sept. 14 (Echo, Sept. 21 — webconews now answers curl with a Chrome UA to the lede). Topsail: Surf City RFQ Sept. 23 for a solid-waste enterprise fund and five-year rate model, due Nov. 16 (Surf City newsflash). Alternates: HMDA sells Coal Exchange lot to C-MAK Towers $360,000 (H-D); Overstreet trial day 3; United Bank 125-job Charleston ops center (MetroNews); Camden water works update Sept. 16 (Echo); U.S. 421 main break dismissed seven Pender schools Tuesday (none on the island); House Democrats' Kitchen Table Tour (MetroNews — WebFetch dated it "Sept. 25"; article says Wednesday). Devine arraignment: no result found anywhere (magistrate listed "waived") — nothing printed. Caserta seat: the commission meets today, after press | **watch: Caserta replacement (Cabell commission today); Devine; Boone/Lincoln flood damage; Hope Gas hearing continues; Black Diamond Oct. 1; HB 2014 Sept. 28; Putnam commission Sept. 29; Nicholas-Webster still needs a working source** |
| Open-ended | **Canada 2/2/2.** PG: council defers the Civic Core arena/theatre choice to Nov. 30, past the Oct. 17 election, four councillors opposed (CKPG — no vote day in the article, so "this week"); RCMP arrest one suspect Tuesday in the four vape/cannabis robberies (CKPG — the movement on 09-23). BC: Rustad (Nechako Lakes) will not run Oct. 24, Bailey the fourth Eby minister out (CBC); multiple structure fires in Boston Bar early Tuesday, 10-plus hours, no count or cause (CBC). Canada: Quebec's final leaders' debate Wednesday night, immigration caps 45,000-70,000, Oct. 5 vote (CBC); Carney told the NYT he studied U.S. military action as an "extreme tail risk" (Global). Alternates: Foothills Crossing 199 rentals (CKPG); Bailey's own exit (Global); Kenneth Law sentencing hearing, 14 suicides, continues Thursday (CBC). Findlay byelection status NOT confirmed — still unmentioned. CBC via curl Chrome UA; Global WebFetch only; CTV article bodies do not render | **watch — Elections BC nominations for the PG ridings; Kenneth Law sentencing; Quebec Oct. 5; PG advance polls Oct. 7; Civic Core Nov. 30** |
| Open-ended | **Sumo, Aki Day 12 (THURSDAY Sept. 24 in Tokyo) — JSA leaders, torikumiAjax Days 12 and 13 (POST to `/EnHonbashoMain/torikumiAjax/1/{day}/`, basho_id 637, cookie `mc=CatAndMouseGame`; the HTML tables are empty without JS), absence page at `/EnHonbashoMain/absence/`.** **Onosato 11-1**, shitatedashinage over Atamifuji; Fujinokawa oshitaoshi over Kirishima (6-6); Aonishiki yorikiri over Kinbozan; Asanoyama yorikiri over Churanoumi; Kotozakura oshidashi over Oshoma (8-4). **Kotoshoho went kyujo Day 12** (Fujiryoga by default). Chasers at 9-3: Aonishiki, Fujinokawa, Asanoyama — Onosato leads by two with three days left. Day 13: Onosato v Kirishima, Aonishiki v Kotozakura, Atamifuji v Asanoyama, Churanoumi v Fujinokawa. Japan Times Day 11 column lede only (paywall; curl browser UA works, WebFetch 402). r/Sumo not attempted. Records in briefs rewritten in words after the score gate fired | **Day 13 results Friday; Onosato v Kirishima; a two-bout lead with three days left — a Day 14 clinch is possible if the chasers lose** |
| Open-ended | **Our Teams: 7 briefs, 5 outlets, Spurs sat out (offseason; ESPN team page blank).** Reds lost 3-2 in 10 at Atlanta (Abbott two solo homers in 7 IP — Olson and Riley; Brito HR; Banfield tied it; Dubón single off Mey in the 10th; Suter W — box score gamePk 824868 verified by the editor); Pirates lost 5-1 to St. Louis (Wetherholt three hits; Lowe's 34th off Liberatore; gamePk 823327 verified). **Hannan LOST 3-1 at Calvary Baptist Tuesday per MaxPreps (posted Wednesday), record 2-3 as MaxPreps posts it; hosts Roane at Ashton tonight 6 p.m. ET** — the digest tease carries it because Hannan files first by config order. WVU: Jacorey Thomas eligible by preliminary injunction, Krahe/Ball/Bray limited (MetroNews notebook); Marshall: Gibson "get clean" before Homecoming v Gardner-Webb, Pennington starts for GWU (MetroNews); Bengals: Iosivas to IR, Burrow off the report, Allen and Hill DNP (bengals.com); Browns: Szmyt AFC special teams player of the week, Jenkins DNP, Ross to the PS (clevelandbrowns.com). Standings 13 (MLB byte-matched; PL/MLS/NFL ESPN feeds; polls still Week 4, Sept. 20; Hannan per MaxPreps). Upcoming 18 lines Sept. 24-Oct. 1, including the Mountain State Derby Sunday 7:15 p.m. ET at Hoops Family Field (MetroNews; ESPN's feed says 7:10). **ESPN's PL fixture feed says the league resumes Oct. 10-11, not Oct. 3 as the ledger's Oct. 3 row said — Chelsea v Bournemouth Oct. 10 10 a.m. ET, Spurs at Man United 12:30, Liverpool v Man City Oct. 11 11:30 a.m. ET.** No PL/MLS/USMNT/Spurs brief: no news read | **hannan-westside-date-venue — STILL ASK IAN; hannan-roane-result — owed Friday; PL resumes Oct. 10 (fix the Oct. 3 row); Ohio v Stonehill Saturday** |
| Open-ended | **Leagues: 9 briefs.** Sumo 3; MLB 3: Mariners 6-5 Astros in 10, AL West tied at 78-80 with Texas, Houston holds the tiebreaker (AP via ESPN — the feed's magic number of 1 for a tied team rejected again); Orioles 4-2 Blue Jays eliminates the defending AL champions, nightcap also 4-2, Baltimore one loss from out (AP via ESPN); Padres 5-1 Dodgers, top NL wild card alone, Phillies lost to Milwaukee, Cubs lost (no NL Central figure printed). NFL 2: Harbaugh says Dart has knee surgery and misses the regular season, ACL intact, meniscus/MCL/PCL per sources (ESPN); Penix returns as the Falcons visit Green Bay tonight 8:15 p.m. ET on Prime (AP via ESPN). WNBA 1: Dream 83-65 Liberty clinches the No. 4 seed, playoffs open Sunday (ESPN). Held: Red Sox 1-0 Guardians (magic number 4); Mets 7-2 Rangers; Commanders on Daniels, no timeline; Sounders 2-0 RSL; Rockies 101 losses. ESPN articles: default-UA curl works, Chrome UA gets a 202 challenge, WebFetch empty | **Guardians clinch watch (4); AL West three-way finish; Dart timeline; WNBA playoffs Sunday** |
| Open-ended | **Outdoors: all four waters after the 5:45 retry.** **Williams 755 cfs / 3.40 ft at 5:15, off the 2,610 crest (9:30 p.m. Tuesday), down 695 on the day, but UP 34 cfs from a 721 low at 3 a.m.** — the fetcher's "rising" (against 572 at 6 a.m. Tuesday) is wrong on the day and right on the last two hours by accident; no WV product active to explain the uptick. **Point Pleasant 25.98, back to pool, bottomed 25.35 Wednesday evening and rising a tenth an hour** (flagged "falling"); the Gauley above Belva crested 8,330 cfs at 3:45 p.m. Wednesday and read 4,410 at 5. **Huntington 28.73, down 3.21 on the day from the 33.97 crest, the window's low** (flagged "falling" — right both ways); NWPS 9:56 p.m. forecast carries a 29.7 bump Friday morning, no flood category. Topsail: sound L 1:03 AM 0.9, H 6:59 AM 3.7, L 1:16 PM 0.7, H 7:26 PM 4.1, all inside Thursday; 76.8F Beaufort; moon 95%, 12.6 days, full Saturday 16:49 UT (USNO); **Rip Current Statement HIGH through 8 p.m. and a 5-8 a.m. Coastal Flood Advisory on Coastal Pender; 3-6 ft surf on a north wind ~20**; NHC: TS Fay near the Azores, a Cabo Verde low 60/60, nothing toward the Carolinas. **Fisherman's Post and Coastal Angler still Sept. 1, 23 days old — no October report.** Seasons: archery deer/bear/boar Saturday (two days); ducks/geese Oct. 3 and bear gun third window (nine days); crow Oct. 1 (seven); squirrel Day 13; dove Day 24; going out: bear gun second window closes TOMORROW. NC limits re-copied (effective Sept. 2); flounder closed through Sept. 30. Gauley: riverscout's 2026 page (June 14) lists Sept. 25-28 among 22 days at 2,800; WV Explorer (Aug. 26) says 22 days Sept. 11-Oct. 18 — reported, not confirmed; Corps cert fails, AW calendar 404, NPS blocked. Migratory PDF re-downloaded and read (PyMuPDF; the scaup line rendered to an image). Stocking: nothing found | **watch — Williams uptick (was it rain?); Point Pleasant rising; Gauley Friday; Fisherman's Post October; HIGH rip through Saturday; bear gun closes Friday** |
| Open-ended | **Sci/Tech and AI.** Arctic sea ice minimum 1.78M sq mi Sept. 12, tied 10th-lowest (NASA/NSIDC); Webb finds C, O and Si escaping galaxies at 500M years, Arizona, Nature Astronomy (Phys.org); Ship 41 on Booster 21, Flight 14 targeted 8:15 a.m. ET Monday pending FAA (Spaceflight Now — first use); longer REM sleep linked to lower risk of 83 diseases, 95,559 UK Biobank, PLOS Medicine, observational (Science Daily). AI: Altman and Amodei at the UNSC Wednesday, Kratsios rejects international oversight (AFP via TechXplore); Anthropic says 950 Claude agents screened 200,000 phage genes to a CRISPR-like system — preprint, company claim, Zhang quote (Phys.org/AFP; TechCrunch notes Stanford found a similar system); Gallup/Microsoft: 68% of daily U.S. AI users worried, 37 countries (TechCrunch). Held: fly magnetic-field lifespan (Medical Xpress); GLP-1 nutrient deficiencies in children (Science Daily); Croatia Artemis Accords; OpenAI contractors fired (404 Media, Sept. 22); Argonne molten-salt (ANS). Lake Powell and the 63C amoeba still held; Beta Pic b not published. Ars Technica refused the fetch; Nature news listing redirects to auth; FAA Starship page 403 | **watch — FAA license for Flight 14 (Monday 8:15 a.m. ET); Crew-13 crew arrival Saturday; Altman/Amodei follow-ups** |
| Open-ended | **Source status.** OPEN: ABC (wire), Al Jazeera, NBC, CBS, NPR (curl only; WebFetch 503), Euronews, Kyiv Independent, The National, NHC advisory text, NASA science pages, Spaceflight Now, Phys.org/TechXplore/Medical Xpress (WebFetch; curl 429), Science Daily, TechCrunch, 404 Media RSS, WSAZ, WV MetroNews, WTAP, Herald-Dispatch (front; sports 429/404), Hinton News (paywalled notices), Bennington Banner, VTDigger, Webster Echo (curl Chrome UA, lede), Surf City and NTB newsflash, Pender civicalerts, WECT, WWAY, Port City Daily, CKPG (WebFetch), CBC (curl Chrome UA), Global (WebFetch), CTV front, JSA leaders/torikumiAjax/absence, Japan Times (curl browser UA, lede), MLB Stats API, ESPN JSON (default UA) and ESPN articles (default-UA curl), MaxPreps, bengals.com, clevelandbrowns.com, ussoccer.com stories, Athens Messenger, Sky Sports, USGS IV, NWPS HNTW2, api.weather.gov, ILM SRF, NHC TWO, USNO, wvdnr.gov migratory PDF (curl), NCDMF, Fisherman's Post feed (default UA), Coastal Angler feed. BLOCKED: Reuters/AP/BBC/Guardian (not tried), DW (search crawler), The Hill (403), PBS (Pezeshkian page was 2024's; Xi page 404), Politico search, Ars Technica, Nature news listing, FAA Starship, EurekAlert, PG Citizen, My PG Now, princegeorge.ca, CTV article bodies, WVNS/WOWK county pages, Gold and Blue Nation (403), ESPN Chelsea/Spurs team pages (blank), ussoccer schedule (404), Crew/FCC news (JS shells), USACE Huntington (cert), AW Gauley calendar (404), NPS Gauley, NWPS PTPW2, riverscout Gauley page ("Redirecting"), old.reddit r/Sumo (not tried) | **watch — a Nicholas County source; PBS returns stale pages on politician-name searches** |
| Open-ended | **Traps dodged.** (1) The WebFetch summarizer stamped Wednesday as "Sept. 24/25" on the AFP UNSC piece, the Kitchen Table Tour and CP pages — every brief says "Wednesday." (2) Polo: Euronews "weakened to Cat 4" v NHC advisory 15's 160 mph Cat 5 — the advisory. (3) Morocco: AJ "Thursday, Sept. 23" — the calendar. (4) Missouri: NBC's "supporters filed" v ABC's text — opponents. (5) PBS served the 2024 Pezeshkian speech — discarded. (6) A search summary put a Summersville Lake campground ribbon-cutting on Sept. 18, 2026; the release is May 2025. (7) Pipestem man's age differs between outlets — omitted. (8) The stabbing suspect: WSAZ's update says caught, MetroNews's earlier version says search ongoing — "faces," not "charged." (9) Devine: no arraignment result anywhere — nothing printed. (10) Kotoshoho absent Day 12 read off the JSA absence page, not a fan site. (11) Houston's magic number of 1 while tied — rejected again. (12) Toronto-Baltimore both games 4-2 — only game 1 carries `result`. (13) WNBA "Thursday's finales" quoted only as the article states. (14) "Dubon" v the feed's "Dubón" — verified by accent search, not assumed missing. (15) Sumo and NFL records read as scores by the gate — written in words. (16) PL resumes Oct. 10, not Oct. 3 — the ledger row was wrong. (17) Derby kickoff 7:15 (MetroNews) v 7:10 (ESPN) — MetroNews, ESPN noted. (18) Anthropic's biology claim — attributed to the company and labeled a preprint, this desk's own maker included. (19) Both lead photographs are faces — the cordon drawn without the principals. (20) Fetcher flags: Williams "rising" right only on the last two hours, Point Pleasant "falling" wrong on the morning — printed as the fetcher's, directions as the traces'. (21) The Leagues desk's note said the JSA pages were read "about 8:30 a.m. ET" at 5:54 — corrected to "this morning" before validation | |

### Forward-dated events added or moved

| Date | Event | Note |
|---|---|---|
| **2026-09-24** | **Aki Day 12 (ran); Xi arrival ceremony and state dinner; Cabell commission on Caserta's seat; Hannan v Roane at Ashton 6 p.m.; Pirates v Cardinals 12:35; Reds at Braves 7:15; Falcons at Packers 8:15 p.m. ET; Kenneth Law sentencing hearing continues; Rip Current Statement HIGH Coastal Pender to 8 p.m.** | |
| **2026-09-25** | **Aki Day 13 (Onosato v Kirishima); Xi at the National Archives; WV bear gun second window closes (selected counties); Gauley release per riverscout (unconfirmed); Ohio at Huntington forecast bump to 29.7; Reds at Blue Jays 7:07, Pirates at Tigers 6:40** | |
| **2026-09-26** | **WV archery/crossbow deer, bear and boar open; full moon 16:49 UT; Crew-13 crew arrives at KSC; USMNT v Peru 4:30 p.m. ET Orlando; Ohio v Stonehill 3:30, Marshall v Gardner-Webb 3:30 (Homecoming), WVU v Oklahoma State 7; FCC at Montreal 7:30** | |
| **2026-09-27** | **Aki senshuraku; MLB regular season ends (Reds at Toronto 3:07, Pirates at Detroit 3:10); Bengals at Pittsburgh 1 p.m., Browns v Carolina 1 p.m.; Crew v Inter Miami 7 p.m. ET; WVU at Marshall men's soccer, Mountain State Derby, Hoops Family Field, 7:15 p.m. ET (MetroNews; ESPN says 7:10); WNBA playoffs open** | |
| **2026-09-28** | **Starship Flight 14 NET 8:15 a.m. ET (no FAA license as of Wednesday); HB 2014 data-center rules hearing; Surf City e-bike focus group 6-8 p.m.** | |
| **2026-09-29** | **Putnam County Commission on the data-center resolution; Hannan at Roane, Spencer, 6:30; USMNT v Chile 8 p.m. ET St. Louis, Ream honored** | |
| **2026-09-30** | **NC flounder possession closure ends (limits page); habeas hearing for Garces Perez (CBS)** | |
| **2026-10-01** | **Black Diamond/Appalachian Power timeline due at the PSC; Caserta retires; Hannan at Buffalo 5 p.m.; WV crow season opens; Crew-13 launch 11:10 a.m. EDT** | |
| **2026-10-03** | **WV regular goose and duck seasons open; bear gun third window (3-9)** | |
| **2026-10-05** | **Quebec election** | |
| **2026-10-07** | **Prince George advance polls open (Oct. 7, 8, 14, 15)** | |
| **2026-10-10** | **Premier League resumes (ESPN feed): Chelsea v Bournemouth 10 a.m. ET, Tottenham at Manchester United 12:30 p.m. ET; Liverpool v Manchester City Oct. 11, 11:30 a.m. ET** | replaces the Oct. 3 row |
| **2026-10-17** | **PG and Quesnel civic elections; WV bear youth second window (17-18); woodcock, grouse and raccoon hunting open** | |
| **2026-10-21** | **U.S. Open Cup final, Crew v St. Louis City, Columbus** | |
| **2026-10-24** | **B.C. snap provincial election** | |
| **2026-10-27** | **Israeli election** | |
| **2026-10-28** | **Carabao Cup fourth round, Liverpool v Chelsea, Anfield** | |
| **2026-11-08** | **Kyushu basho opens, Fukuoka** | |
| **2026-11-16** | **Surf City solid-waste enterprise fund RFQ submittals due** | |
| **2026-11-30** | **Prince George council's deferred Civic Core arena decision** | |
| **2026-12-22** | **South Sudan's first national election** | |

### Open threads

- **xi-state-visit-tarmac-truce-jan-10** — led; the state dinner tonight, Archives Friday, rare-earths truce talks are the follow-ups. **kelly-tro-press-passes-restored / treasury-5-13-oil-103-barr / missouri-map-third-time / ice-austin-no-body-camera** — ran. **garces-perez-habeas-sept-30 / pezeshkian-un-speech / fed-barr-hikes** — alternates.
- **polo-cat-5-again-160 / israel-bars-arab-lists / russia-strikes-16-dead-282-drones / morocco-pam-97-seats** — ran. **albanese-openai-health-breach / ukraine-nk-pows-to-seoul / sri-lanka-220-year-sentences (only on unlisted outlets)** — alternates.
- **morrisey-boone-lincoln-flood-emergency / hope-gas-psc-leak-hearing / methodist-property-supreme-court / harpers-ferry-murder-arson** — ran. **chiles-died / clendenin-dutch-ridge-stabbing / toys-r-us-grand-central / summers-superseding-394-counts** — regional. **route-9-woodford-mma-tanker** — away. **webster-boe-middle-school-softball / surf-city-solid-waste-rfq** — hotspots. **hmda-coal-exchange-lot / overstreet-trial / united-bank-charleston-ops / camden-water-sept-16 / pender-421-main-break / kitchen-table-tour / caserta-seat-today / devine-arraignment (no result) / black-diamond-oct-1** — alternates or owed. **woo-hoo-tax-dispute (RAN 09-23) / cowen-vfd-10000 (09-22) / big-ditch-rv-park (09-21) / pender-no-quorum (09-23) / bcrc-act-181 (09-23)** — do not re-run.
- **pg-civic-core-deferred-nov-30 / pg-robbery-arrest / rustad-not-running-bailey-fourth / boston-bar-fires / quebec-final-debate / carney-nyt-tail-risk** — ran. **foothills-crossing-199 / bailey-exit / kenneth-law-sentencing / findlay-byelection (still unconfirmed) / unifor-stellantis (nothing)** — alternates or owed.
- **arctic-sea-ice-10th-lowest / webb-metals-500m-years / starship-stacked-flight-14 / rem-sleep-83-diseases** — ran. **fly-magnetic-lifespan / glp-1-children-deficiencies / croatia-artemis / lake-powell / amoeba-63c / beta-pic-b** — held.
- **altman-amodei-unsc / anthropic-crispr-like-agents-preprint / gallup-68-daily-users-worried** — ran. **openai-contractors-fired / argonne-molten-salt** — alternates.
- **reds-3-2-braves-10 / pirates-5-1-cardinals / hannan-3-1-calvary-2-3 / wvu-thomas-injunction / marshall-gibson-get-clean / bengals-iosivas-ir-burrow / browns-szmyt-week** — ran. **hannan-westside-date-venue (ASK IAN) / hannan-roane-result (owed Friday) / pl-resumes-oct-10 / palmer-england-withdrawal (Sept. 21, stale) / open-cup-final-oct-21** — owed or held.
- **aki-day12-onosato-11-1 / aki-day12-fujinokawa-kirishima-kotoshoho-kyujo / aki-day13-card / mariners-6-5-astros-al-west-tied / orioles-4-2-jays-eliminated / padres-5-1-dodgers-top-wild-card / dart-surgery-regular-season / penix-returns-tnf / dream-83-65-liberty-no-4** — ran. **red-sox-1-0-guardians-magic-4 / mets-7-2-rangers / commanders-daniels / sounders-2-0-rsl / rockies-101** — held.
- **archery-sept26-two-days / boar-archery / ducks-oct3 / geese-oct3 / bear-gun-oct3-9 / crow-oct1 / squirrel-day-13 / dove-day-24 / red-drum / seatrout / spanish-bluefish-kings / black-drum-sheepshead / bear-gun-closes-tomorrow** — ran. **flounder-closed-through-sept-30 / gauley-reported-not-confirmed / stocking-none** — seasons note. **williams-755-uptick-from-721 / point-pleasant-25-98-rising / huntington-28-73-window-low-29-7-bump / rip-high-pender-coastal-flood-advisory / fay-azores-cabo-verde-60 / moon-95-two-days-to-full** — water block.
- **stats-yahoo-stale-close** — cleared today. **usgs-first-fetch-503** — third of nine mornings; the retry loop works. **sportsman-index-stale-no-11** — for Nate. **fetch-fishing-24h-window-bug** — for Nate, seventh instance. **detached-head-twenty-fifth** — recurring. **art-caption-140-cap** — validator-only rule. **pl-oct-3-row-wrong** — corrected above.

### Covered slugs, 2026-09-24

`xi-state-visit-andrews-tarmac-trade-truce-jan-10`, `kelly-tro-restores-cnn-ms-now-politico`, `treasury-10-year-5-13-brent-103-barr`, `missouri-map-supreme-court-third-time`, `ice-austin-officer-no-body-camera-worn`,
`polo-regains-cat-5-160-mph-advisory-15`, `israel-cec-bars-raam-joint-list-oct-27`, `russia-strikes-16-dead-282-drones-kyiv-maternity`, `morocco-pam-97-of-395-turnout-38`,
`morrisey-flood-emergency-boone-lincoln`, `psc-hope-gas-4-percent-leak-repair-hearing`, `justices-methodist-33-congregations-property`, `harpers-ferry-woman-murder-arson-2025-fire`,
`chiles-cabell-prosecutor-judge-died`, `clendenin-dutch-ridge-stabbing-three-counts`, `toys-r-us-grand-central-mall-october`, `summers-superseding-indictment-394-counts-59-women`, `route-9-woodford-mma-tanker-closure`, `webster-boe-middle-school-girls-softball-sept-14`, `surf-city-solid-waste-enterprise-fund-rfq-nov-16`,
`pg-civic-core-deferred-nov-30`, `pg-rcmp-arrest-one-robbery-suspect`, `rustad-not-running-bailey-fourth-minister`, `boston-bar-multiple-fires`, `quebec-final-debate-immigration-caps`, `carney-nyt-extreme-tail-risk`,
`arctic-sea-ice-1-78m-tied-10th-lowest`, `webb-metals-escaping-galaxies-500m-years`, `starship-ship-41-booster-21-flight-14-monday`, `rem-sleep-83-diseases-plos-medicine`,
`altman-amodei-unsc-standards-kratsios`, `anthropic-950-agents-crispr-like-preprint`, `gallup-microsoft-68-daily-users-worried`,
`hannan-3-1-calvary-baptist-2-3-roane-tonight`, `reds-3-2-braves-10-innings-dubon`, `pirates-5-1-cardinals-lowe-34th`, `wvu-jacorey-thomas-injunction-eligible`, `marshall-gibson-get-clean-homecoming`, `bengals-iosivas-ir-burrow-off-report`, `browns-szmyt-afc-special-teams-week`,
`aki-day12-onosato-11-1-shitatedashinage-atamifuji`, `aki-day12-fujinokawa-kirishima-kotoshoho-kyujo`, `aki-day13-card-onosato-kirishima`, `mariners-6-5-astros-10-al-west-tied-78-80`, `orioles-4-2-blue-jays-eliminated`, `padres-5-1-dodgers-top-nl-wild-card`, `dart-surgery-misses-regular-season-harbaugh`, `penix-returns-falcons-packers-tnf`, `dream-83-65-liberty-no-4-seed`,
`archery-deer-bear-sept-26-two-days`, `boar-archery-sept-26`, `ducks-coots-mergansers-oct-3`, `geese-oct-3-18`, `bear-gun-third-window-oct-3-9`, `crow-oct-1-seven-days`, `squirrel-day-13`, `dove-day-24`, `red-drum-slot-ebb-to-1-16`, `seatrout-slot-dock-lights`, `spanish-bluefish-kings-footnote-m-surf-3-6`, `black-drum-sheepshead`, `bear-gun-second-window-closes-sept-25`,
`flounder-closed-through-sept-30`, `gauley-sept-25-28-reported-not-confirmed`, `stocking-none`, `williams-755-uptick-from-721-crest-2610`, `point-pleasant-25-98-rising-from-25-35`, `huntington-28-73-window-low-forecast-29-7-friday`, `rip-current-high-pender-coastal-flood-advisory`, `fay-azores-cabo-verde-60-60`, `moon-95-two-days-to-full-sept-26`, `topsail-fp-sept-1-twenty-three-days`

**Post record, 2026-09-24.** The digest for No. 50 posted at **7:00:01 a.m. ET**, held 3 minutes by `--not-before 07:00` from a 6:57 foreground start (message 1552635713420398703, 1103 embed chars, hero attached, `degraded: []`). Both papers were live on Pages at 6:00:36, about 40 seconds after the 6:00 push. Sports & Sportsman No. 40 was published with the Times and not posted, per the standing rule. The 7:04 backup `send_later` wake (trig_01V9BuVJidT7pvxVjJScAxrz) was deleted after the record landed. The session was held in the foreground with `hold_until.py` in nine-minute windows from 6:03 to 6:57, as on 09-21 through 09-23.
