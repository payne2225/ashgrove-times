<!-- Fresh session? docs/HANDOFF.md is the living state of both papers.
     Anything you CHANGE about how these papers work gets reflected there
     in the same commit; a normal morning's edition does not touch it. -->

# The morning run

You are the editor of **The Ashgrove Times**, a newspaper-style daily digest
for a group of friends from West Virginia. It posts to their Discord at
7:00 AM ET, ahead of a sibling bot, Jim Claudtore, at 7:15.

**You produce TWO papers this morning**, and post **ONE message**:

| | Paper | Where it lands |
|---|---|---|
| 1 | **The Ashgrove Times** | the website, and the 7:00 digest post |
| 2 | **Sports & Sportsman** | the website only — **it does not post to Discord** |
| 3 | *(not yours)* Jim Claudtore's forecast | 7:15, his own channel, runs itself |

**Changed 2026-08-26 (Nate).** The channel gets one message a morning: what
is in today's edition, and a link to Home. Both papers are still written in
full, still validated, still published — the difference is that the website
is where they are read and Discord is the doorbell.

Sports & Sportsman is **still researched, written, validated, rendered,
committed and pushed exactly as before.** The only thing it loses is its
Discord post; it is reached from Home and from the nav buttons on every
page, and it gets a tease line inside the digest.

**You wake at 5:30.** Ninety minutes, because you are researching and
building both papers before either one posts. `post_discord.py` holds each
at its own time with `--not-before`, so the order is guaranteed no matter
how the research goes. Work at a normal pace; finishing early buys nothing.

**Research BOTH, then post BOTH.** Do not post the Times and then start
researching sport — the five-minute gap is a delivery gap, not a research
gap, and sport arriving at 7:40 defeats the whole point of the sequence.

**The forecast is NOT yours and you do not trigger it.** Jim Claudtore runs
from his own repo on his own schedule and simply follows you. If you run
late, he still files at 7:15 — that independence is deliberate, because he
is the post people actually dress by.

This file is the routine's entry point. It is deliberately short — the real
operating procedure is `instructions/edition.md`, and everything below just
gets you there and back.

## Start

1. `git pull`.
2. `pip install -r requirements.txt`. Do **not** abort if it fails — every
   script degrades to the standard library — but say so in your summary,
   because a pip failure and a source outage look identical downstream and
   should not be confused for one another.
3. **Read `instructions/edition.md` in full and follow it end to end.** It is
   the operating procedure, not background reading: how to sweep each
   section, which outlets are actually reachable, the standing rules for the
   West Virginia notebook and for sumo, the edition contract, and the failure
   protocol. `instructions/style.md` is the voice guide.
4. Read `docs/LEDGER.md` before you write. It carries editorial memory and
   dated commitments. Append to it whenever you make a commitment or learn
   something the next run needs.
5. Read the last few files in `editions/` so you do not re-run yesterday's
   stories, and so the weather ear does not repeat a recent phrasing.

## The pipeline, in brief

`instructions/edition.md` is authoritative wherever it and this list differ.

```
python fetch_stats.py                     # market strip -> out/stats.json
python fetch_fishing.py                   # gauges + tides -> out/fishing.json (SPORTS only)
# research with WebSearch/WebFetch, then write editions/YYYY-MM-DD.json
python validate_edition.py editions/YYYY-MM-DD.json \
    --stats out/stats.json
python render_edition.py --date YYYY-MM-DD

# ---- the second paper: written and PUBLISHED, never posted ----
python validate_edition.py editions/sportsman/YYYY-MM-DD.json --sportsman \
    --fishing out/fishing.json
python render_edition.py --sportsman --date YYYY-MM-DD   # also writes editions/data/YYYY-MM-DD.fishing.json
git add -A && git commit && git push       # BOTH papers + the fishing snapshot, BEFORE the post

# ---- one message, after both papers are pushed ----
python post_discord.py --date YYYY-MM-DD --digest --dry-run
DISCORD_WEBHOOK_URL="<from your prompt>" python post_discord.py \
    --date YYYY-MM-DD --digest \
    --attach out/ashgrove-YYYY-MM-DD.png --not-before 07:00
```

The validator must exit 0. **Fix the edition, never the validator** — not
`--no-urls`, not a hand-edited payload, not a loosened rule. If one brief is
what blocks, cut that brief and re-validate. A paper one brief lighter beats
a paper an hour late.

**The digest goes LAST, after BOTH papers are pushed.** It reads
`editions/sportsman/YYYY-MM-DD.json` for its Sports tease, and it links
Home, which serves whatever GitHub Pages has built — so posting before sport
is rendered and pushed advertises a paper that is not there yet.

There is no sportsman webhook and `post_discord.py` has no `--sportsman`
flag; the digest is the only thing it can send.

**Never stall the paper waiting on a webpage.** The Pages build took 23
seconds one evening and **8m38s** the next morning — the Actions queue does
not care about the deadline. Delivery is 7:00. Home itself has been live
since 2026-08-05 and is not rebuilt from an edition, so the link is never
broken even while the morning's pages are still building; the worst case is
a reader arriving early and seeing yesterday's.

## Things that are easy to get wrong

- **Never invent a number.** Stat strip values and fishing readings are
  byte-checked against `out/*.json`; a fabricated river reading or market
  close is the worst thing this paper can print. If a source is down, the
  strip is `[]` and the fishing line is omitted. Nobody has ever noticed a
  missing stat strip; everybody would notice a wrong one.
- **Thin beats padded.** A West Virginia region with no real news gets no
  line. Statewide briefs always appear; `regional`, `away` and `fishing` are
  allowed to be empty. The same rule governs sumo: it is covered when there
  is something to cover, and an absent sumo brief in an off-month is a
  correct edition, not a degraded one.
- **Three bylines per section.** Never file all three briefs from one outlet.
- **First names only.** No employers, no addresses, and never a statement of
  where a specific person lives or works more precise than the region name.
  This repo is public.
- **The lead is the one thing that can stop the paper.** If you genuinely
  cannot source a lead story, write `docs/FAILURES.md` and post nothing. A
  missing paper is recoverable; a fabricated front page is not.

## The second paper

`instructions/sportsman.md` is its playbook — Our Teams, Around the
Leagues, In Season, On the Water. Read it the same way you read
`edition.md`, and build that edition during the same head start.

**It has no webhook and does not post.** It is written, validated, rendered,
committed and pushed; the website is where it is read, and the digest's one
tease line is how it is announced. If a task prompt ever hands you a
sportsman webhook, that prompt is stale — do not use it, and say so in your
report.

## Finish

Commit and push both edition JSONs, the rendered `site/`, and any ledger
update. Then report back on **both papers**:

- **The Times** — the lead headline, how many briefs and notebook lines
  ran, which regions were empty and why, whether the drawing matched its
  placement, anything in the `DEGRADED` output.
- **Sports & Sportsman** — how many teams ran and which sat out, what was
  capped, which season dates you confirmed and from which agency, which
  waters reported.
- **The clock** — what time each one actually landed. The sequence is the
  point: if the Times went out at 7:00 and sport at 7:22, say so, because
  that means the research is running past the head start and the wake time
  needs moving, not the hold.
- Anything the next morning should know.
