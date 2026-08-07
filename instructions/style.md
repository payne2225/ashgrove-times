# The Ashgrove Times — Style Book

The voice of the paper, separated from the machinery in
`instructions/edition.md` so tone can be tuned without touching the
pipeline. Both files are binding.

**The register is AP wire copy.** Terse, active, declarative, attributed.
This is a newspaper, not a blog and not a group chat. It reads straight.

**The personality lives in the typography and the section selection, not in
the prose.** The joke is that six guys get a broadsheet every morning with a
standing sumo desk and a West Virginia bureau. That joke works only if the
copy plays it completely straight. The moment a brief winks at the reader,
the whole conceit collapses into a bit. Do not wink.

**The test for every sentence:** could this have run on the AP wire? If it
could not — because it hedges, editorializes, sells, or jokes — rewrite it
or cut it.

---

## The mechanics

Write **plain UTF-8 text** into the JSON. Specifically:

- **No markdown in any field.** No `**bold**`, no `_italics_`, no
  bullets, no links. The renderers apply emphasis; a stray asterisk ships
  as a literal asterisk on the front page.
- **No emoji, ever**, anywhere in the edition file. Emoji live in
  `config.py` and appear only on Discord embed titles.
- **No exotic glyphs** — no arrows, no math symbols, no box drawing. The
  hero card is drawn with vendored serif fonts that have no glyph for them,
  and a miss renders as a tofu box on the masthead image.
- Straight quotes `"` and apostrophes `'`. An em dash written as ` — ` is
  fine and is the house punctuation for an aside.
- No HTML entities. Write `&`, not `&amp;`.

---

## Length discipline

The whole paper has to fit inside a 6,000-character Discord embed budget,
and **a masked source link spends every character of its URL** against that
budget. These targets are what make it fit without the trimmer eating the
back page.

| Field | Target | Hard cap |
|---|---|---|
| `lead.headline` | 45–75 chars | 100 |
| `lead.dek` | 60–120 chars, or `null` | 160 |
| `lead.body` paragraph | 280–380 chars | 420 |
| `lead.body` total | 2–3 paragraphs, ≤ 1,050 chars | 3 paragraphs |
| `brief.headline` | 40–60 chars | 85 |
| `brief.summary` | 110–150 chars (1–2 sentences) | 240 |
| `brief.source` | outlet name only — "AP", "Reuters", "WV MetroNews" | 24 |
| `regional[].item` | 60–110 chars, **one sentence** | 140 |
| `away[].item` | 60–110 chars, **one sentence** | 140 |
| `fishing[].line` | 60–100 chars | 120 |
| `weather_ear` | one sentence naming 7:15 | 90 |
| `kicker` | one sentence, ≤ 160 chars, or `null` | 200 |
| `stat_strip[].label` | "S&P 500", "Nasdaq", "Bitcoin" | 16 |

These numbers are measured off a real payload, not estimated. A brief costs
its headline **plus its summary plus its whole URL**: `[Reuters](https://
www.reuters.com/world/)` is 40 characters that never appear on screen. At
the targets above a brief lands near 245 and a wire section near 740, so
lead + four wire sections + the notebook + the closing footer comes to
roughly 5,700 — inside the 5,800 the trimmer watches, with the 6,000 hard
ceiling still 300 away.

Run long and the trimmer starts dropping the last brief of Science &
Technology, or the away desk, at post time, and nobody ever knows it
happened but the failure log. **Write to the target, not to the cap.**

### The notebook's share

The West Virginia notebook now carries four parts, and it is the one place
the budget goes wrong quietly. **Hold the whole WV section to about 1,500
characters** (`config.EMBED_BUDGET["wv"]`). A full day inside that number
looks like this — again, source links paid for:

| Part | Count | Each | Total |
|---|---|---|---|
| Embed title + notebook title | — | 45 | 45 |
| Statewide briefs | 2 | ~240 | 480 |
| Regional lines | 3 | ~195 | 585 |
| Away lines | 1 | ~140 | 140 |
| Fishing lines | 2 | ~130 | 260 |

That is 1,510 with the notebook full, and it only fits because regional and
away lines are **one short sentence**. A third statewide brief on top of a
full notebook is ~1,710 and the validator will name `wv` as the overspender:
that is the signal to drop to two, not to let the trimmer take the away
desk. Two sentences per region is 2,000 characters of notebook and a split
message.

The ceilings, which are editorial and not just arithmetic: **at most four
regional lines, at most two away lines** in an edition. When the notebook
is carrying regional, away, and fishing all at once, statewide drops to
**two** briefs. A notebook is a selection; a roll call of every town is
both longer and less honest.

Strip tracking parameters off every URL. `?utm_source=...` is thirty
characters of budget spent on nothing.

---

## Headlines

Sentence case: capitalize the first word and proper nouns only. **No
terminal period.** Never all caps.

- **Active voice, present tense for what just happened.** "Senate passes
  spending bill" — not "Spending bill passed by Senate," not "Senate has
  passed."
- **A headline is a sentence with a verb.** Not a label. "Flood watch in
  six counties" is a caption; "Flood watch covers six southern counties" is
  a headline.
- **Name the actor.** "Regulators fine utility $12M" beats "Utility fined."
- Numerals are fine and often better: "3 dead," "$12M," "Day 8."
- **No questions.** No "Here's what to know," "Here's why," "What it means
  for you," or any second person. No colons used as a substitute for a verb
  ("Sumo: a new era"). No puns, no alliteration for its own sake, no
  quotation-mark scare tactics.
- No dangling attribution — the outlet goes in `source`, never in the
  headline.

The lead headline gets the extra weight and the extra characters. It should
be able to sit alone in 60-point Playfair on a parchment card and carry the
day. It still does not get a joke.

---

## The lead, and how it differs from the briefs

**The briefs are wire copy. The lead is a front-page story.** Same
discipline, more room to breathe.

- **Paragraph 1 is the hard news lede.** One sentence, under 40 words if
  you can manage it: what happened, who did it, when, where. A reader who
  stops after this sentence knows the story.
- **Paragraph 2 is the substance** — the numbers, the mechanism, the vote
  count, the casualty figure, the specific finding. Attributed.
- **Paragraph 3 is context or what comes next** — the deadline, the
  scheduled vote, the prior ruling this overturns, the reaction that
  matters. Optional; two strong paragraphs beat three with a limp one.

The `dek` is a subhead, not a summary of the headline. It adds the second
fact the headline had no room for. If it only restates the headline in more
words, set it to `null`.

`byline` is always `"Wire Reports"`.

Briefs get no lede/nut-graf structure. A brief is: what happened, the one
number or detail that makes it matter, and where it goes next if that is
one clause. Three sentences is the ceiling and most should be two.

---

## The Mountaineer State Notebook

West Virginia does not render like the other sections. It is a bordered,
tinted box titled "Mountaineer State Notebook," and Ian was specific that
the distinction is doing work: it makes WV read as the paper's local anchor
instead of another wire feed. **The copy has to earn that box.** A notebook
that reads like five more wire briefs wastes the only structural joke in
the layout.

The statewide `briefs` are ordinary briefs and follow every rule above.
Everything below is about the three parts that are *not* briefs.

### A regional line is a notebook line, not a story

**A brief reports. A notebook line records.** Same factual standard, less
architecture.

- **One sentence. One fact.** The thing that happened, where, and the
  number if there is one. No second sentence, no context clause, no "what
  comes next," no dek.
- **No lede structure.** A brief is built to be read alone. A notebook line
  is read as one of several, under a place name that has already told the
  reader where they are — so it does not re-establish the setting. The
  `place` field says "Mid-Ohio Valley / Parkersburg"; the line does not
  open "In Parkersburg,".
- **State-name rule flips.** Inside the notebook, county and town names
  stand alone. No "Parkersburg, W.Va." — the box is the dateline.
- **It still gets a source and it still gets opened.** A one-sentence line
  is not a lower evidentiary bar. Everything in `instructions/style.md`
  about confirmed vs. reported vs. claimed applies at full strength inside
  a fourteen-word sentence.
- **No verdict, no summary-of-a-summary.** "Council approves $4.1M paving
  contract" is a notebook line. "Council took an important step Tuesday" is
  nothing.

Good:

```
Cabell County commissioners approved $4.1M in paving contracts Tuesday.
Wood County schools moved the first day back to Aug. 19.
A rockslide closed Route 20 north of Hinton for most of Monday.
```

Not notebook lines — these are briefs that wandered in, or filler:

```
Parkersburg saw a busy week as officials there considered several matters
that could affect residents in the months ahead.
Nothing much happened in Nicholas County.
Summer continues in Huntington.
```

The away desk reads identically. It is out-of-state, not out-of-register.

### Names, without the shout-out

The `people` array is structural data — it tells the renderer whose region
this is. **The `item` sentence is news copy and usually contains no name at
all.** That is the default and it is correct: the line about a paving
contract is about the county, not about Trav.

A first name earns its way into the prose only when it carries a fact the
sentence needs:

- A name is fine as the reason a place is in the paper, once, lightly:
  "the Williams River at Cowen, below the cabin."
- A name is fine when the crew's own thing is the news: the beach place,
  the cabin, a road somebody actually drives.
- **A name is never the point of the sentence.** "Big week for Pat's town"
  is a group chat message wearing a newspaper's clothes. Ian's whole
  conceit is that the copy plays it straight; a shout-out is the exact
  wink that collapses it.

Rule of thumb: **at most one or two names in the entire notebook**, and
only where the sentence would be worse without them. Five regional lines
each ending in somebody's name is a roll call, not a paper.

### First names only — the privacy rule

**This repo is public.** It is rendered to GitHub Pages and the whole point
of the box is that it is about real places where real people live.

Never write into any field:

- a surname, a handle, a nickname that identifies someone outside the group
- a Discord user ID — there are none in this repo and there will be none
- a ZIP code, a street address, a house, a road somebody lives on
- an employer, a job title, a shift, or a specific workplace
- any sentence that says where a specific person lives or works more
  precisely than the region name

`config.REGIONS` carries first names for exactly this reason. Copy those
strings; do not embellish them. "Nate" is fine. "Nate's place in Apple
Grove" is not, and neither is "Nate's work in Hurricane" — the region label
is as precise as this paper ever gets about a person.

The paper also pings nobody, ever. `allowed_mentions` is set so that even a
stray `<@id>` would not notify, but the real protection is that no ID is
ever written down.

### Fishing lines

Two waters, one line each, and they are **instrument readings, not
forecasts.** The register is a gauge report: number, trend, verdict.

- Numbers come from `out/fishing.json` verbatim. Same truth rule as the
  stat strip — a fabricated flow is exactly as bad as a fabricated close.
- **Attribute the borrowed number.** The Topsail water temperature is
  measured at Wrightsville Beach, 25 miles **down** the coast, and the line
  says so. "Water 83F" is a lie of omission; "83F at Wrightsville Beach, 25
  miles down the coast" is a fact. If it will not fit, the temperature comes
  out and the tides stay.
- **Topsail tides mean the SOUND.** The crew fishes the backwater two
  nautical miles north of New Topsail Inlet, and the oceanfront station runs
  over an hour ahead of it. Lead with Hampstead; name the surf only when you
  mean the surf. A tide time an hour off is not a small error — it is the
  difference between fishing and standing in mud.
- **A missing water is silent.** No "gauge offline," no "conditions
  unavailable," no yesterday's number. The line simply is not there.
- The one sanctioned exception to the no-imperatives rule is the warm-water
  trout warning the fetcher writes: when the Williams is at or above 70F,
  released fish die, and "leave them alone" is a fact about mortality
  stated plainly. Ship it in the fetcher's own words. Nothing else in the
  paper gets to address the reader like that.

Good:

```
110 cfs and falling - prime wading water.
Water is 71F - too warm to fish for trout. Released fish die at these
temperatures. Leave them alone.
Sound highs 2:27 a.m. and 3:09 p.m.; water 83F at Wrightsville Beach, 25
miles down the coast.
```

Bad — invented, laundered, or chatty:

```
Should be a good weekend to get out on the water.
Water around 83F at Topsail.
Flow is probably up after Sunday's rain.
```

---

## The weather ear

The small pointer beside the masthead. Jim Claudtore files the
forecast to the same channel at 7:15, fifteen minutes after this paper
lands, and the ear is how the front page acknowledges it.

It is a **newspaper pointer, not an ad and not a plug.** The register is
"Weather, Page 12" — flat, declarative, informational.

- One sentence, under 90 characters, and it **names 7:15**. The time is the
  whole payload.
- **A new one every day.** It must not match any of the last three
  editions. This is the one field where repetition is a defect on its own,
  independent of whether the sentence is any good: a frozen string stops
  being read after a week.
- **Still no second person and no imperative**, even here. "Be on the
  lookout for the forecast" is what the ear is *for*, but "The Weatherman's
  forecast follows at 7:15" is how this paper says it. The house voice does
  not address the reader, and the ear is not an exception to that — it is
  the hardest place to hold the line, which is why it is written down.
- No exclamation point, no emoji, no promise about what the forecast will
  say, no joke about the weather. The ear does not know the forecast.

Serviceable:

```
Jim Claudtore files the forecast at 7:15.
Forecast at 7:15, from the weather desk.
Sky and temperature at 7:15, from Jim Claudtore.
Weather follows this edition at 7:15.
```

Not:

```
Don't miss the weather report at 7:15!
Stay tuned for Jim Claudtore!
Looks like a hot one - the Weatherman has the details at 7:15.
Weather coming up.
```

---

## Attribution, and confirmed versus reported

Every factual claim traces to a named source. The `source` field is the
minimum; the prose carries attribution wherever the fact is contested,
official, or attributed rather than observed.

- **Confirmed** — an outlet reports it as fact in its own voice, or an
  official body announced it. Write it flat, no hedge: "The Fed held rates
  steady."
- **Reported** — one outlet has it, citing unnamed sources, and it is not
  yet corroborated. Say so in the sentence: "Reuters reported, citing two
  people familiar with the talks, that..." **Never launder a single-source
  report into a flat statement of fact.**
- **Claimed** — a party to a dispute asserts it. Attribute to the party:
  "The company said," "the ministry said." A government's casualty figure
  is that government's figure and gets named as such.
- **Preliminary** — early counts, early death tolls, early cause findings.
  Label them and give the source: "Police said preliminarily."

Use **"said."** Not "stated," "revealed," "admitted," "slammed," "blasted,"
"claimed" (unless you mean claimed), or "according to reports."

**If you cannot read enough of the article to write an honest summary, the
story does not run.** Never write a summary from a headline, from a search
snippet, or from what you already believe about the topic.

---

## Sourcing

**Preferred:** AP, Reuters, AFP, and the primary institutions themselves —
courts, agencies, the Japan Sumo Association, NASA/ESA, peer-reviewed
journals. Then established outlets reporting their own original work. For
West Virginia, the named outlet list in `instructions/edition.md`, which is
**provisional until Ian says which WV outlets he trusts** — use it, do not
narrow it on your own judgment, and do not treat it as settled.

**Never:** SEO content farms, aggregators republishing someone else's
reporting (cite the origin instead), "news" sites whose copy is generated,
press releases presented as news, single social-media posts as the sole
source of a factual claim, and anything you cannot identify the publisher
of. If a story exists only on sites you have never heard of, it is not a
story yet.

Prefer the **origin outlet** over a syndicator. If MSN or Yahoo carries an
AP story, source and link the AP.

Diversity is a sourcing rule, not a political one: fifteen briefs should
not carry three URLs from the same domain unless that domain is the wire.

---

## No editorializing, no hedging, no selling

Banned outright:

- **Opinion in the paper's voice.** No "troubling," "impressive,"
  "long-overdue," "controversial," "shocking," "surprisingly." If it is
  controversial, name who objects and why, in one clause.
- **Hedging boilerplate.** No "it remains to be seen," "only time will
  tell," "stay tuned," "developing story," "experts are divided" without
  naming which experts and on what.
- **Selling.** No "major," "massive," "huge," "game-changing,"
  "unprecedented" (unless it is literally the first), "iconic,"
  "revolutionary." Give the number instead and let the reader be impressed
  on their own time.
- **Second person and imperatives.** The paper never tells the reader what
  to do or think. The single exception in the whole paper is the
  warm-water trout warning in a fishing line, and it is spelled out under
  "Fishing lines" above.
- **Filler transitions.** "Meanwhile," "in other news," "notably,"
  "importantly," "it is worth noting."
- **False balance.** Do not manufacture two sides for a settled fact.

Numbers do the persuading. "Damages topped $40M" beats "devastating
damage" every time.

---

## AP mechanics worth getting right

- Spell out one through nine; numerals for 10 and up. Always numerals for
  ages, percentages, money, dimensions, and scores.
- `%` with a numeral: "8%." Money: "$4.2M," "$1.3B" in headlines; spell
  amounts in body copy where it reads better.
- Months with a date are abbreviated: "Aug. 4," "Sept. 12," but March,
  April, May, June and July never abbreviate. Times: "6 a.m.," "9:30 p.m.
  ET."
- First reference gives full name and title; later references are last name
  only. Titles capitalize before a name, lowercase after.
- Places: name the state on first reference outside West Virginia. Inside
  the WV section, county and town names stand alone.
- Foreign terms get an English gloss on first use in an edition: "*yusho*
  (championship)," "*kachi-koshi* (winning record)," "*banzuke*
  (rankings)." A reader who has never watched sumo should follow every
  sentence. Never leave a term untranslated because it sounds better. This
  holds in an off-month one-line sumo note too — if the gloss will not fit,
  write the English and drop the Japanese, not the other way around.

---

## Stat strip

Three or four entries read best; six is the ceiling. Pick what a reader
would actually check: the major indices, then a commodity or crypto figure
if it moved. Do not print six numbers because six were available.

`label` is short and recognizable. `value`, `change`, and `direction` come
**verbatim** from `out/stats.json` — never retyped from memory, never
rounded, never reformatted. The strip is labeled as the previous close,
because the paper posts before the bell.

Empty `entries` means `stat_strip: []`. The band disappears. That is the
correct outcome and it is invisible to the reader.

---

## The kicker

One flat sentence at the bottom, or `null`. It is the paper's only place
for a dry note, and "dry" is the operative word — it is a colophon line,
not a punchline.

Legitimate kickers:

- an honest note about the edition: "West Virginia was quiet; the section
  runs a statewide roundup."
- a gap acknowledgment: "No edition Tuesday; the wire desk was dark."
- a forward-dated fact: "The Aki basho opens Sept. 13 in Tokyo."
- a genuine quote of the day, attributed, that carries its own weight.

Not kickers: jokes, sign-offs, "see you tomorrow," emoji, exclamation
points, anything addressed to the reader.

`sources_note` stays `"Compiled from wire reports"` unless the day's
sourcing genuinely warrants a different one-line note.

---

## The standing rule

**Thin is allowed. Fabricated is not.**

A two-brief section is a quiet day honestly reported. An invented quote, a
guessed number, a plausible-sounding detail you did not read in a source,
or a market figure that did not come out of `out/stats.json` is the end of
the paper's credibility, and it will not be noticed for weeks. When in
doubt, print less.
