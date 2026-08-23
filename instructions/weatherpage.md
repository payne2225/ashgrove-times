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
2. Today's **Eastern** date is the edition date. The briefing is
   `weatherman/briefings/<date>.md`. Jim archives and pushes it shortly
   after his 7:15 post, usually by about 7:45.
3. **If today's file is not there yet:** wait two minutes, pull again, up
   to about twenty minutes. If it never appears, STOP and say so —
   **never publish an older briefing under today's date**, and never
   improvise a forecast. A missing weather page costs nothing; Jim's post
   is already in the channel.
4. Render, from the ashgrove-times checkout:

   ```
   python render_edition.py --weather ../weatherman/briefings/<date>.md \
       --date <date>
   ```

   (Adjust the relative path to wherever the weatherman checkout landed.)

   The renderer strips the frontmatter and **scrubs every Discord ping**;
   it refuses to render if any user id survives, because this site is
   public. If it refuses, report it — do not work around the guard.
5. Commit and push **ashgrove-times only**. The push publishes the page
   via Pages.
6. Report: which date published, and nothing else needed.
