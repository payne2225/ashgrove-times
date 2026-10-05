# The weather page — publishing Jim Claudtore to the Newsstand

A small, separate morning job: take the briefing Jim Claudtore has already
posted and archived, and typeset it onto the Times site at
`site/weather/<date>.html` (plus `site/weather/index.html` as the stable
bookmark). That is the whole job.

**THE BOUNDARY — set 2026-08-18, amended 2026-08-22.** Nate has folded
The Weather Claude into the Times session, so the boundary now has two
halves:

- **The interactive session owns both repos.** Working with Nate, it may
  develop weatherman directly — playbooks, config, scripts, routines,
  commits and pushes. Things the channel *experiences* (post times, the
  persona, the format, who gets pinged) still need his say-so first.
- **THIS ROUTINE STAYS READ-ONLY, unchanged.** It is unattended, it runs
  while everyone is asleep, and it has no reason to write to weatherman:
  it READS that repo and writes ONLY to ashgrove-times. Never commit to
  the weatherman repo, never edit its files, never touch its routines,
  never post to Discord — Jim already posted; this is typesetting, not
  delivery. An unattended job holding write access to a live publishing
  repo is how a broken 7:15 post happens with nobody awake to catch it.

## Steps

1. Both repos are checked out: `ashgrove-times` and `weatherman`. Find
   them; `git pull --rebase` in each.
2. **Wait for Jim's archive**, from the ashgrove-times checkout:

   ```
   python wait_for_briefing.py --weatherman ../weatherman
   ```

   (Adjust the path to wherever the weatherman checkout landed.) It pulls
   weatherman once a minute for up to nine minutes and prints ONE line.
   Do what the line says:

   - `READY <date> <path>`: render that path under that date (step 5).
   - `DONE <date>`: today's page is already published by an earlier
     fire. **Stop and report "already published".** Do not re-render.
   - `EARLY <date>`: it is before 7:10 ET, so Jim has not posted yet. Stop
     and report it; a later fire this morning publishes the page.
   - `WAITING <date>`: not archived yet. Run the same command ONE more
     time. If it says `WAITING` again, stop and report it; the next fire
     an hour later is the retry.

   **Why three fires and no long hold** (2026-10-04): your cron is
   `17 11,12,13 * * *` UTC, which is 7:17, 8:17 and 9:17 ET in summer and
   6:17, 7:17 and 8:17 ET from 2026-11-01. The first fire after Jim
   archives publishes, a couple of minutes behind his 7:15 post; every
   other fire is a `DONE` or an `EARLY` and costs nothing. The old single
   8:10 fire put the page up an hour after the channel had the forecast,
   and readers noticed. Do not time any of this yourself; the script does
   the Eastern-time arithmetic.
3. The date the script printed is today's **Eastern** date and the only
   date you may publish. The briefing is `weatherman/briefings/<date>.md`.
4. **Never publish an older briefing under today's date**, and never
   improvise a forecast. A missing weather page costs little; Jim's post
   is already in the channel.
5. Render, from the ashgrove-times checkout:

   ```
   python render_edition.py --weather ../weatherman/briefings/<date>.md \
       --date <date>
   ```

   (Adjust the relative path to wherever the weatherman checkout landed.)

   The renderer strips the frontmatter and **scrubs every Discord ping**;
   it refuses to render if any user id survives, because this site is
   public. If it refuses, report it — do not work around the guard.
6. Commit and push **ashgrove-times only**. The push publishes the page
   via Pages.
7. Report: which date published, and nothing else needed.
