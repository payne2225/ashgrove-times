"""Fetch MLB standings for the followed clubs — or honestly fetch nothing.

Both sports errors Pat caught were "half right": every number was real and
every number was in the source, but the RELATIONSHIP between them was
stated backwards — "second-place Pittsburgh" when the Pirates were fourth,
"18.5 clear of" when 18.5 was Pittsburgh's deficit. `result` fixed the
direction of a game report. Standings were still typed by hand from a
table, and a table read with the eye on the wrong row passes every check
that only asks whether the number exists.

So the standings block gets the stat-strip rule. This script writes
`out/standings.json` and validate_edition.py byte-matches every record,
games-back figure and ordinal the sports desk prints for an MLB club
against it. A standings line whose numbers are not in this file is a hard
failure, from 2026-09-03.

Source: MLB's public Stats API, keyless, which answered from the routine's
sandbox first try on 2026-08-24 and 08-26 (it is where both fixes were
verified):

    https://statsapi.mlb.com/api/v1/standings?leagueId=103,104&season=<y>&date=<d>

Every club in the DIVISION of each followed MLB team is written, not only
the followed club: a brief that says the Brewers lead the Central by six
names a team the desk does not follow, and that number needs a source too.
MLS and the Premier League are out of scope here — no keyless source with a
stable shape was found — and instructions/sportsman.md says so rather than
half-doing it.

    python fetch_standings.py [--date YYYY-MM-DD] [--out out/standings.json]

Always exits 0 and always writes the file; with no data it writes an empty
`teams` map and the validator then refuses any MLB standings line, which is
the correct outcome — thin beats invented.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request

import config

try:
    import requests
except ImportError:  # pragma: no cover - bare sandbox without pip
    requests = None

TIMEOUT = 20
STATSAPI = ("https://statsapi.mlb.com/api/v1/standings"
            "?leagueId=103,104&season={season}&date={date}"
            "&standingsTypes=regularSeason&hydrate=team,division,league")
# `hydrate=team` is not optional: without it each row's `team` is an id and
# a link, no name, and the build matches nothing (found on the first run).
SOURCE = "MLB Stats API"
HEADERS = {"User-Agent": config.USER_AGENT, "Accept": "application/json"}

ORDINALS = ("first", "second", "third", "fourth", "fifth", "sixth",
            "seventh", "eighth", "ninth", "tenth")


def _get_json(url: str) -> dict:
    if requests is not None:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _gb(value: object) -> str | None:
    """The API writes '-' for a leader and '18.5' otherwise; keep the text."""
    if value in (None, "", "-"):
        return None
    return str(value)


def _int(value: object) -> int | None:
    try:
        return int(str(value))
    except (TypeError, ValueError):
        return None


def team_record(rec: dict, division: str, size: int) -> dict:
    """One club's row, in the exact strings the desk may print."""
    wins, losses = _int(rec.get("wins")), _int(rec.get("losses"))
    rank = _int(rec.get("divisionRank"))
    streak = (rec.get("streak") or {}).get("streakCode")
    out = {
        "division": division,
        "wins": wins,
        "losses": losses,
        "record": f"{wins}-{losses}" if wins is not None and losses is not None else None,
        "division_rank": rank,
        "division_rank_word": ORDINALS[rank - 1] if rank and rank <= len(ORDINALS) else None,
        "division_size": size,
        "is_last": bool(rank and rank == size),
        "games_back": _gb(rec.get("divisionGamesBack") or rec.get("gamesBack")),
        "wild_card_games_back": _gb(rec.get("wildCardGamesBack")),
        "wild_card_rank": _int(rec.get("wildCardRank")),
        "league_rank": _int(rec.get("leagueRank")),
        "streak": streak,
        "division_leader": bool(rec.get("divisionLeader")),
    }
    return out


def build(date_iso: str, errors: list[str]) -> dict:
    season = date_iso[:4]
    followed = {t["name"] for t in config.followed_teams("MLB")}
    teams: dict[str, dict] = {}
    try:
        data = _get_json(STATSAPI.format(season=season, date=date_iso))
    except (OSError, ValueError, urllib.error.URLError) as exc:
        errors.append(f"{SOURCE}: {type(exc).__name__}: {exc}")
        data = {}
    except Exception as exc:  # noqa: BLE001 - requests raises its own family
        errors.append(f"{SOURCE}: {type(exc).__name__}: {exc}")
        data = {}

    for group in data.get("records") or []:
        rows = group.get("teamRecords") or []
        names = {(r.get("team") or {}).get("name") for r in rows}
        if not names & followed:
            continue
        division = ((group.get("division") or {}).get("name")
                    or f"division {(group.get('division') or {}).get('id')}")
        division = division.replace("American League", "AL").replace("National League", "NL")
        for row in rows:
            name = (row.get("team") or {}).get("name")
            if not name:
                continue
            record = team_record(row, division, len(rows))
            record["followed"] = name in followed
            record["league"] = "MLB"
            teams[name] = record

    missing = sorted(followed - set(teams))
    if missing and not errors:
        errors.append(f"{SOURCE}: no standings row for {', '.join(missing)}")

    return {
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "date": date_iso,
        "season": season,
        "source": SOURCE,
        "source_url": "https://www.mlb.com/standings",
        "teams": teams,
        "errors": errors,
    }


def summary(data: dict) -> str:
    lines = []
    for name, t in sorted(data.get("teams", {}).items(),
                          key=lambda kv: (kv[1].get("division") or "", kv[1].get("division_rank") or 0)):
        flag = "*" if t.get("followed") else " "
        gb = t.get("games_back") or "-"
        wc = t.get("wild_card_games_back") or "-"
        lines.append(f"{flag} {name:<22} {t.get('record') or '?':>7}  "
                     f"{t.get('division') or '':<10} #{t.get('division_rank')}  "
                     f"GB {gb:>4}  WC {wc:>4}  {t.get('streak') or ''}")
    for err in data.get("errors") or []:
        lines.append(f"! {err}")
    return "\n".join(lines) or "(no standings)"


def main() -> int:
    config.use_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--date", default=None,
                        help="standings as of this date (default: today, Eastern)")
    parser.add_argument("--out", default=config.STANDINGS_PATH)
    parser.add_argument("--pretty", action="store_true", help="print a table too")
    args = parser.parse_args()

    date_iso = args.date or config.now_et().strftime("%Y-%m-%d")
    errors: list[str] = []
    data = build(date_iso, errors)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    count = len(data["teams"])
    followed = sum(1 for t in data["teams"].values() if t.get("followed"))
    print(f"OK: wrote {args.out} ({count} clubs, {followed} followed, "
          f"{len(errors)} source error{'' if len(errors) == 1 else 's'})")
    if args.pretty or errors:
        print(summary(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
