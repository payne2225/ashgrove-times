# Handoff: The Ashgrove Times → Discord Daily Dashboard

**From:** Ian (via Claude)
**To:** Nate's Claude
**Goal:** Turn a working newspaper-style news digest into an automated daily post in our Discord server, shared with the whole friend group.

---

## 1. What this project is

"The Ashgrove Times" (tagline: *"For the Fellers"*) is a newspaper-styled daily news digest — currently a single self-contained HTML artifact generated fresh each day. It has five sections, in this order:

1. **Lead story** — top headline of the day, 2–3 paragraphs, with a small stat strip (market numbers or similar) underneath
2. **U.S. Section**
3. **World Section**
4. **West Virginia Section** (local/regional news — this group has a WV connection, so it's a standing section, not optional)
5. **Sports Section** (must include sumo news whenever available — standing requirement, not a one-off)
6. **Science & Technology Section**

Each section is a set of short "brief" items: a bolded headline + 1–3 sentence summary. Sourced via web search each time it's built, not from a static feed.

The end goal here is: **every day, a fresh edition gets posted automatically into a Discord channel** so the whole friend group sees it without anyone having to ask for it.

---

## 2. Current state (what's already built)

A working HTML version exists as a Claude artifact — single-file HTML/CSS, no JS, styled like a broadsheet front page (serif fonts, drop cap on the lead, column rules, masthead). This is **the design reference**. Nate's Claude should treat the visual language as settled and focus on (a) automating content generation and (b) delivering it to Discord, not redesigning it.

### Design tokens (carry these over)
- Masthead: "THE ASHGROVE TIMES", tagline "For the Fellers"
- Fonts: Playfair Display (headlines/masthead), Source Serif 4 (body), Old Standard TT (masthead alt)
- Palette: parchment background (`#f4f0e6` / `#e9e4d8`), near-black ink (`#1c1a16`), muted gold-brown accents
- Section labels: black background, cream text, small caps, letter-spaced
- Two-column brief layout with vertical rule between columns
- Stat strip (market-style numbers) under the lead story when relevant

Full HTML/CSS is available on request — Ian can paste the current artifact source into the thread for Nate's Claude to copy directly.

---

## 3. What needs to be built

### 3.1 Content generation
A daily job that:
- Gathers news across the five fixed sections (lead + US + World + WV + Sports w/ sumo + Sci/Tech)
- Writes it in the Ashgrove Times voice/format (headline + short brief, AP-style, no fluff)
- Outputs it in a format suitable for posting to Discord — **this likely means producing both:**
  - A **Discord-native message** (embeds, since Discord doesn't render full HTML) for the actual channel post
  - Optionally, a rendered image or hosted webpage version of the full "newspaper" for people who want the full broadsheet experience (linked from the Discord post)

### 3.2 Discord delivery
- Use a **Discord Incoming Webhook** (simplest path — no bot hosting required) posted to a designated channel
- Discord webhooks accept JSON with `embeds` — use one embed per section (Discord embeds support title/description/fields), or a summary embed + link out to a hosted full version
- Discord embed limits to design around: 6000 char total, 256 char title, 4096 char description, 25 fields per embed, 10 embeds per message

### 3.3 Scheduling
- Needs to run once daily (Ian didn't specify time — worth asking him, or defaulting to a morning ET post)
- Options: a scheduled Claude Code / Claude Cowork job, a cron job hitting a small script, or a simple serverless function (e.g., a scheduled Lambda/Cloud Function) that calls the webhook

### 3.4 Hosting the full "paper" (optional but nice-to-have)
- If the group wants the full broadsheet visual (not just a Discord embed), the HTML file needs somewhere to live — e.g., a simple static host (GitHub Pages, Vercel, Netlify) regenerated daily, with the Discord post linking to today's edition

---

## 4. Open questions for Nate to resolve with Ian (don't guess on these)

1. What time should the daily post go out?
2. Does the group want just Discord embeds, or also a hosted full-HTML version linked from the post?
3. Who owns/hosts the Discord webhook URL — does Nate already have a bot/webhook set up in the server, or does one need to be created?
4. Any preference on which model/tool does the daily content generation (Claude API call on a schedule vs. a Claude Code job)?
5. Confirm standing section requirements are correct: WV section and sumo-inclusive Sports section should always appear, even on light-news days — worth double checking this is still wanted long-term vs. just for this run.

---

## 5. Suggested first steps for Nate's Claude

1. Ask Ian (or Nate) for the Discord webhook URL for the target channel (or help create one: Server Settings → Integrations → Webhooks → New Webhook)
2. Get the current HTML artifact source from Ian to use as the design reference
3. Prototype a single manual post first — hand-build one day's content, format it as a Discord embed payload, POST it to the webhook, confirm it looks right
4. Once formatting is validated, wrap the content-generation step (web search + section drafting) into a repeatable script/prompt
5. Add scheduling last, once the manual pipeline works end-to-end

---

## 6. Example Discord webhook POST (reference for prototyping)

```bash
curl -X POST "$DISCORD_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "The Ashgrove Times",
    "embeds": [
      {
        "title": "🗞️ The Ashgrove Times — For the Fellers",
        "description": "**[Lead headline here]**\n\nShort lead summary paragraph...",
        "color": 3419169,
        "fields": [
          { "name": "🇺🇸 U.S.", "value": "- Headline one\n- Headline two", "inline": false },
          { "name": "🌍 World", "value": "- Headline one\n- Headline two", "inline": false },
          { "name": "🏔️ West Virginia", "value": "- Headline one\n- Headline two", "inline": false },
          { "name": "🏆 Sports", "value": "- Sumo headline\n- Headline two", "inline": false },
          { "name": "🔬 Science & Tech", "value": "- Headline one\n- Headline two", "inline": false }
        ],
        "footer": { "text": "Compiled from wire reports · Today's edition" }
      }
    ]
  }'
```

Note: `color` is a decimal int of a hex color (e.g. `#3E3221` → `3419169`) — worth matching to the parchment/ink palette above.

---

*End of handoff. Nate's Claude should feel free to ask Ian directly for the HTML source or any of the open questions above rather than guessing.*

