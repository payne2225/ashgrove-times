<!-- Fresh session? docs/HANDOFF.md is the living state of both papers.
     Anything you CHANGE about how these papers work gets reflected there
     in the same commit; a normal morning's edition does not touch it. -->

# The morning run

You are the editor of **The Ashgrove Times**, a newspaper-style daily digest
for a group of friends from West Virginia, and since 2026-10-14 you also run
the desk that writes **Jim Claudtore's** weather briefing. Two posts reach
the friends' Discord from this session every morning, each in its own
channel with its own webhook:

| | What | Where it lands | When |
|---|---|---|---|
| 1 | **The Ashgrove Times** | the website, and the digest post | 7:00 ET |
| 2 | **Sports & Sportsman** | the website only, **never Discord** | with the Times |
| 3 | **Jim Claudtore's briefing** | his channel, and the weather page | 7:15 ET |

**Changed 2026-10-13 (Nate).** Jim used to be his own 7:00 routine. The
scheduler started it 6 to 20 minutes late and the writing took 13 to 27, so
he posted between 7:25 and 7:43 against a 7:15 slot, and the weather page
behind him later still. Now a desk you spawn writes him at about 5:45, the
page goes up from that draft, and you post him at 7:15 from the same wake
that posts the digest. His old routine is a **standby** that fires at 7:32
and posts only what nobody has (weatherman `instructions/standby.md`).

**Changed 2026-08-26 (Nate).** The channel gets one Times message a morning:
what is in today's edition, and a link to Home. Both papers are written in
full, validated and published; the website is where they are read and
Discord is the doorbell.

This file is the routine's entry point. The real operating procedures are
`instructions/edition.md` (the Times), `instructions/sportsman.md` (Sports &
Sportsman) and weatherman's `instructions/briefing.md` (Jim, written by his
desk, not by you). This file says how the morning fits together.

## The clock, the same Eastern times all year

| ET | What happens |
|---|---|
| 5:30 (+0 to 25 min) | the fire; `morning_gate.py` says GO; Jim's desk spawns at once |
| about 5:45 to 6:00 | both papers built, validated, rendered and pushed |
| about 6:00 to 6:15 | Jim's desk reports; his draft and the weather page are pushed |
| then | `morning_gate.py wake`, one `send_later`, and the first turn ends |
| 6:55 (+about 1 min) | **the wake**: claim Jim, hold the digest |
| 7:00 | the digest posts |
| 7:08 | the refresh looks for anything new since Jim wrote |
| 7:15 | Jim posts; the post is recorded; the record commit; the report |

**Daylight saving needs nothing from you.** The cron is `30 9,10 * * *`
UTC all year, so the routine fires twice every morning:

| | 09:30 UTC | 10:30 UTC |
|---|---|---|
| Summer (EDT, March to November) | 5:30 AM: **GO** | 6:30 AM: **DONE** |
| Winter (EST, November to March) | 4:30 AM: **EARLY** | 5:30 AM: **GO** |

`morning_gate.py` decides each fire, and every hold (7:00, 7:08, 7:15) is
made by a script reading the Eastern clock. Do not time anything yourself,
and do not edit the routine: the cron is Nate's. In summer the 6:30 fire is
also the backup: if the 5:30 fire never started, it finds no claim and
builds the papers itself, late.

## 1. The gate: your first command

Two checkouts are here, and the session starts in their parent,
`/home/user`: **`/home/user/ashgrove-times`** and
**`/home/user/weatherman`** (seen 2026-10-13; if they are not there, find
them, and use their real paths everywhere below). **Start every Bash
command with `cd /home/user/<checkout> &&`**, as every command in this file
does: a desk or a wake can leave the shell in either checkout (the
2026-10-13 rehearsal woke in ashgrove-times, not `/home/user`), and a
command run in the wrong one fails, or worse, commits there. Before
anything else:

```
cd /home/user/ashgrove-times && python morning_gate.py
```

It prints ONE line:

- **`GO`**: this fire builds today's papers. Its claim is already pushed.
- **`DONE`**: an earlier fire has today. **Stop now** and report the line.
- **`EARLY`**: the winter 4:30 fire. **Stop now** and report the line.
- **`GIT ERROR`**: carry on as GO, and say so in your report.

**Do not `git pull` either one.** The sandbox lands on a detached HEAD most
mornings, where a bare `git pull` fails; the gate has already moved this
checkout onto origin/main. When edition.md says to pull and push, use
`git pull --rebase origin main` and `git push origin HEAD:main`, which work
on a branch and on a detached HEAD alike.

`cd /home/user/ashgrove-times && python -m pip install -q -r requirements.txt`. Do not
abort if it fails; every script degrades to the standard library. Say so in
your summary, because a pip failure and a source outage look identical
downstream.

## 2. Spawn Jim's desk, before your own research

With the Agent tool, in the background, before you read anything else.
Give it exactly this prompt, with the date filled in (and the path, if
the checkout landed somewhere else):

> You are Jim Claudtore's desk this morning, <Weekday, Month D, YYYY>. Work
> in the weatherman checkout at /home/user/weatherman, and start every Bash
> command with `cd /home/user/weatherman &&`. Read `instructions/briefing.md` in
> full and follow it as the DESK: §0 to §2, then the DRAFT archive in §4,
> ending with `python refresh_check.py --basis` and `python jim_gate.py
> check` printing `DRAFT OK`. Do NOT post to Discord, do NOT commit, do NOT
> push, and do not touch the ashgrove-times checkout. Your final message:
> the `DRAFT` line, the highest risk, the alert count, and any fetch error
> you could not recover.

The desk gets no webhook and needs none. Jim's voice, format, callouts and
honesty rules are all in briefing.md; **do not rewrite his briefing**, and
do not hand his desk any of the Times' rules.

**Never end a turn while a desk is still working.** Ending the turn can
release the sandbox, and a desk dies with it. If you have nothing left to
do, wait in the foreground (`sleep 60` in a Bash call, then look again).

If the desk fails or reports anything but `DRAFT OK`, spawn it once more
with the same prompt plus one line saying what went wrong. If the second
one fails too, leave Jim to the standby: no draft, no weather page from
you, and say so in your report. If his desk has still not reported at 7:30
ET, stop waiting for it; the standby writes him from 7:32.

## 3. Build both papers

**Read `instructions/edition.md` in full and follow it**, then
`instructions/sportsman.md` the same way. They are the operating procedure,
not background reading. `instructions/style.md` is the voice guide; read
`docs/LEDGER.md` before you write, and the last few files in `editions/`.

**Research BOTH, then post.** Do not post the Times and then start on
sport; the digest goes LAST, after BOTH papers are pushed. It reads
`editions/sportsman/YYYY-MM-DD.json` for its Sports tease and links Home,
so posting before sport is pushed advertises a paper that is not there yet.

Every command in edition.md and sportsman.md runs in
`/home/user/ashgrove-times`: start each Bash call with
`cd /home/user/ashgrove-times &&`. The pipeline in brief (edition.md is
authoritative where they differ):

```
cd /home/user/ashgrove-times              # every line below runs here
python fetch_stats.py                     # market strip -> out/stats.json
python fetch_fishing.py                   # gauges + tides -> out/fishing.json (SPORTS only)
python fetch_standings.py                 # MLB standings -> out/standings.json (SPORTS only)
# research, then write editions/YYYY-MM-DD.json
python validate_edition.py editions/YYYY-MM-DD.json --stats out/stats.json
python render_edition.py --date YYYY-MM-DD

# ---- the second paper: written and PUBLISHED, never posted ----
python validate_edition.py editions/sportsman/YYYY-MM-DD.json --sportsman \
    --fishing out/fishing.json --standings out/standings.json
python render_edition.py --sportsman --date YYYY-MM-DD

git add editions/ art/ site/ && git commit -m "..." \
    && git pull --rebase origin main && git push origin HEAD:main
```

The validator must exit 0. **Fix the edition, never the validator**: not
`--no-urls`, not a hand-edited payload, not a loosened rule. If one brief is
what blocks, cut it and re-validate.

There is no sportsman webhook and `post_discord.py` has no `--sportsman`
flag; the digest is the only thing it can send.

## 4. Jim's draft and the weather page

When Jim's desk reports `DRAFT OK`:

```
cd /home/user/weatherman && python jim_gate.py draft --push
```

It must print `DRAFTED`. That puts the draft on origin/main for a standby
in another sandbox to find; it is the only way anything of yours reaches
the weatherman repo. On `GIT ERROR` run it again, up to three times. Then
the weather page:

```
cd /home/user/ashgrove-times && python render_edition.py \
    --weather ../weatherman/briefings/YYYY-MM-DD.md --date YYYY-MM-DD
cd /home/user/ashgrove-times && git add site/weather \
    && git commit -m "Weather page for YYYY-MM-DD" \
    && git pull --rebase origin main && git push origin HEAD:main
```

The renderer strips the frontmatter and scrubs every Discord ping; it
refuses to render if any user id survives, because the site is public. If
it refuses, report it and do not work around the guard. The page going up
at about 6:15, ahead of Jim's post, is the point: Pat kept finding the
Times and sport on today and the weather on yesterday.

## 5. The wake

When both papers are pushed and Jim's draft is handled (or handed to the
standby):

```
cd /home/user/ashgrove-times && python morning_gate.py wake
```

- **`WAKE <time> ET = <UTC> (in N s)`**: call `send_later` (the
  Claude_Code_Remote tool) with `at` set to that UTC instant and this
  message: `WAKE YYYY-MM-DD: do §6, "The wake steps", in instructions/routine.md.`
  Then end your turn, provided no desk is still working. Never hold a post
  in the background: a background process dies with the sandbox, which is
  why the digest's old background hold failed nine mornings in twelve.
- **`... INTERIM ...`**: the same, and when that wake arrives, run
  `python morning_gate.py wake` again instead of the wake steps.
- **`NOW`**: it is 6:53 or later. Do the wake steps now, in this turn.

If you are woken and every wake step is already done, say so and stop.

## 6. The wake steps

You come back in the same sandbox or a fresh one (any background process is
gone), with both checkouts as you left them and the shell in either one.
Run every command below exactly as written, `cd` included. Your prompt
holds two webhooks; **each goes only to its own repo's
script**, and each script refuses the other's with exit 3 before it posts
anything:

- `TIMES_WEBHOOK` → `ashgrove-times/post_discord.py`, the digest
- `JIM_WEBHOOK` → `weatherman/post_discord.py`, Jim's briefing

Exit 12 from any command below means it held as long as one call may
(nine minutes) and did nothing yet: **run the same command again**.

1. **Claim Jim**:

   ```
   cd /home/user/weatherman && python jim_gate.py claim --by supervisor --push
   ```

   Only `CLAIMED` posts Jim. On `POSTED` or `TAKEN` someone else has him;
   on `NODRAFT` there is no draft on origin and the standby writes him from
   7:32; on `GIT ERROR` run it again, up to three times. Anything but
   `CLAIMED` in the end: **skip steps 3 to 5**, and say which line you got.
   Posting without the claim is how the channel gets Jim twice.

2. **The digest**, edition.md §9:

   ```
   cd /home/user/ashgrove-times && DISCORD_WEBHOOK_URL="<TIMES_WEBHOOK>" \
       python post_discord.py --date YYYY-MM-DD --digest \
       --attach out/ashgrove-YYYY-MM-DD.png --not-before 07:00
   ```

   `--attach assets/masthead-fallback.png` if the hero render failed.
   Confirm `OK: ... digest posted`. Never pass `--force`.

3. **The refresh**:

   ```
   cd /home/user/weatherman && python refresh_check.py --check --apply --not-before 07:08
   ```

   It holds to 7:08 and prints `REFRESH UNCHANGED`, `REFRESH AMENDED` with
   the update line it put under Jim's dek, or `REFRESH UNAVAILABLE`. Carry
   on whatever it says: Jim posts either way.

4. **Jim**:

   ```
   cd /home/user/weatherman && DISCORD_WEBHOOK_URL="<JIM_WEBHOOK>" \
       python post_discord.py --file briefing.txt --at
   ```

   It holds to 7:15 ET and must print `OK: posted`.

5. **Record Jim's post**, straight after:

   ```
   cd /home/user/weatherman && python jim_gate.py posted --by supervisor --push
   ```

   It must print `MARKED`. On `GIT ERROR` run it again, up to three times;
   this record is what tells the standby and the watchdog that Jim went
   out, so a failure here is the first thing in your report.

6. **The weather page again**: the same two commands as §4. The archive now holds the text exactly as posted, any
   refresh line included; if git says there is nothing to commit, the 6:15
   page already matches.

7. **The record**, edition.md §10, in `/home/user/ashgrove-times`, and its
   commit with `git pull --rebase origin main && git push origin HEAD:main`.

Jim's draft can land late. **The digest never waits for Jim**: if his desk
is still working when the wake steps start, do step 2 on time, and steps 1
and 3 to 6 once `draft --push` has printed `DRAFTED`. A post after 7:15 goes
out at once.

## Boundaries

- **The weatherman repo is written only by `jim_gate.py`**, and only
  `briefings/<date>.md`. Never commit, push or edit anything else there,
  never touch its routines, and never commit `briefing.txt`, `data.json`
  or a webhook. Nate set this boundary when he moved Jim's desk in here on
  2026-10-13; it replaces the old rule that this session never wrote to
  weatherman at all.
- **Webhooks live only in your prompt.** Never write one to a file, commit
  one, or echo one in your output or a commit message.
- **Never post a paper with the other's webhook**, never post Jim without
  `CLAIMED`, and never post Sports & Sportsman at all.
- Nothing about the channel changes without Nate: post times, Jim's voice
  and format, who gets pinged.

## Things that are easy to get wrong

- **Never invent a number.** Stat strip values and fishing readings are
  byte-checked against `out/*.json`; if a source is down, the strip is `[]`
  and the fishing line is omitted. Nobody has noticed a missing stat strip;
  everybody would notice a wrong one.
- **Thin beats padded.** A West Virginia region with no real news gets no
  line. Statewide briefs always appear; `regional`, `away` and `fishing` may
  be empty. Sumo is covered when there is something to cover.
- **Three bylines per section.** Never file all three briefs from one outlet.
- **First names only.** No employers, no addresses, nothing more precise
  about where someone lives or works than the region name. This repo is
  public.
- **The lead is the one thing that can stop the paper.** If you genuinely
  cannot source a lead story, write `docs/FAILURES.md` and post no digest.
  Jim still posts: his desk does not depend on yours.
- **Never stall the paper waiting on a webpage.** The Pages build has taken
  23 seconds one evening and 8m38s the next morning. Home has been live
  since 2026-08-05 and is not rebuilt from an edition, so the digest's link
  is never broken.

## The second paper

`instructions/sportsman.md` is its playbook: Our Teams, Around the Leagues,
In Season, On the Water. Build it in the same head start. **It has no
webhook and does not post.** If a prompt ever hands you a sportsman webhook,
that prompt is stale: do not use it, and say so in your report.

## Report

When the record is pushed, report on all three:

- **The Times**: the lead headline; how many briefs and notebook lines ran,
  with any empty block and why; the Canada tiers; whether the drawing
  matched its placement; anything in the `DEGRADED` output.
- **Sports & Sportsman**: which teams ran and which sat out, what was
  capped, which season dates you confirmed and from which agency, which
  waters reported.
- **Jim**: the desk's `DRAFT` line and when it reported, the `claim` line,
  the `REFRESH` line, when he posted, and the `MARKED` line.
- **The clock**: the gate line and the time of the first command; when each
  paper was pushed; when the weather page went up; when the wake arrived;
  **what time the digest and Jim actually landed.**
- Anything the next morning should know.
