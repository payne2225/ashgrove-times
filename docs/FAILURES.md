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
