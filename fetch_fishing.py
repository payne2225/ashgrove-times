"""Fishing conditions for the waters the crew actually fishes.

Cowen (the cabin) sits on the Williams River; Topsail Beach is surf and
sound; the Ohio runs past Apple Grove through R.C. Byrd Locks and Dam.
Each gets a hard-data report every morning so the paper can carry a fishing
line that is measured rather than vibes.

    python fetch_fishing.py                 # -> out/fishing.json
    python fetch_fishing.py --pretty        # also print a human summary

Sources, all free and keyless:
  - USGS instantaneous values for the Williams River at Dyer (03186500):
    discharge, stage, and water temperature when the gauge reports it.
  - NOAA CO-OPS tide predictions for the two stations that bracket New
    Topsail Inlet, plus water temperature from Wrightsville Beach.
  - USGS stage for the two Ohio River gauges bracketing R.C. Byrd Locks and
    Dam. The dam's own tailwater is Corps data and is NOT reachable; see
    OHIO_GAUGES for what was checked.

Deliberately NOT fetched: the WVDNR trout-stocking list. As of 2026-08-05
wvdnr.gov serves an EXPIRED TLS certificate, so fetching it means disabling
certificate verification, which is not worth a stocking line. The daily
routine web-searches stocking instead and says nothing when it finds
nothing - see instructions/edition.md. Do not "fix" this by passing
verify=False.

Every network call is individually guarded: one dead source degrades that
one reading to null and records why. This script does not raise on a source
outage, and it never substitutes a plausible number for a missing one.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.parse
import urllib.request

try:
    import requests
except ImportError:  # pragma: no cover - bare sandbox without pip
    requests = None

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover - Python < 3.9
    ZoneInfo = None  # type: ignore[assignment]

UA = {"User-Agent": "AshgroveTimes/1.0 (+https://github.com/payne2225/ashgrove-times)"}
TIMEOUT = 25

# Windows consoles default to cp1252, which raises on any non-ASCII a data
# source hands back. Done inline rather than via config.use_utf8_stdio() so
# this stays runnable standalone with no project imports.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # pragma: no cover - non-TTY or <3.7
        pass

# THE OHIO RIVER, and what could not be had.
#
# Trav asked for "the downstream gauge of the Robby C locks and dam" — the
# R.C. Byrd Locks and Dam at Gallipolis Ferry, the crew's home water.
# Checked, and it is NOT AVAILABLE: USGS gauges no Ohio River site at Byrd
# on either the West Virginia or the Ohio list (it does gauge some dams —
# Hannibal has upper and lower sites — just not this one), and the Corps,
# who operate the dam and publish its tailwater, serve a certificate this
# pipeline will not accept, the same wall WVDNR put up.
#
# So the paper prints the two USGS gauges that BRACKET the dam and says so.
# Point Pleasant is 14 river miles above it, Huntington below it. That is an
# honest answer to the question rather than a silent substitution, and if
# Trav wants the tailwater specifically it needs a source we do not have yet.
OHIO_GAUGES = [
    {"key": "ohio_point_pleasant", "site": "03201500",
     "water": "Ohio River at Point Pleasant",
     "note": "14 miles above R.C. Byrd Locks and Dam — the pool side"},
    {"key": "ohio_huntington", "site": "03206000",
     "water": "Ohio River at Huntington",
     "note": "below R.C. Byrd Locks and Dam"},
]

WILLIAMS_GAUGE = "03186500"
WILLIAMS_LABEL = "Williams River at Dyer"

# WHERE THE CREW ACTUALLY FISHES (Nate, 2026-08-06): in the SOUND, about two
# nautical miles north of New Topsail Inlet. They report that the inlet runs
# roughly an hour ahead of their spot, and that Hampstead is about on par with
# it. That makes Hampstead the primary read, not a footnote -- it is inside
# the same body of water, up the ICWW on the same side of the island.
#
# The oceanfront station is kept as the SURF read only. It is genuinely
# different water: it leads the backwater by over an hour, so quoting it for a
# sound trip would put someone on the water at the wrong stage of the tide.
# Order matters here -- `primary` is what the notebook line leads with.
TOPSAIL_TIDE_STATIONS = [
    {"id": "8657813", "name": "Hampstead", "side": "sound", "primary": True,
     "note": "inside the ICWW/Topsail Sound, about on par with where the crew "
             "fishes two nautical miles north of New Topsail Inlet"},
    {"id": "8657419", "name": "Ocean City Beach pier", "side": "ocean",
     "primary": False,
     "note": "oceanfront, 11 mi along the open coast - the surf read, and it "
             "runs well ahead of the sound"},
]
# 8657419 does not offer water temperature; Wrightsville Beach is the nearest
# station that does. It is 25 miles SOUTHWEST down the coast, not up it.
# Attributed honestly rather than passed off as Topsail's own.
TOPSAIL_TEMP_STATION = {"id": "8658163", "name": "Wrightsville Beach",
                        "miles_away": 25, "bearing": "down the coast"}


def get(url: str, params: dict) -> dict:
    """GET JSON through requests, or stdlib urllib when pip never happened.

    Both endpoints are keyless GET+JSON, so the fallback is exact rather than
    degraded. Without it a failed `pip install` reads downstream as a USGS or
    NOAA outage, which is the wrong thing to go debugging at 7am.
    """
    if requests is not None:
        resp = requests.get(url, params=params, headers=UA, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{query}", headers=UA)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def safe(fn, label: str, errors: list):
    """Run a fetch, converting any failure into a recorded error + None."""
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 - one bad source must not end the run
        errors.append(f"{label}: {type(exc).__name__}: {exc}")
        return None


def local_today(tz: str = "America/New_York") -> dt.datetime:
    now = dt.datetime.now(dt.timezone.utc)
    if ZoneInfo is not None:
        try:
            return now.astimezone(ZoneInfo(tz))
        except Exception:  # noqa: BLE001
            pass
    return now


# ------------------------------------------------------------ Williams River

def trout_read(flow_cfs: float | None, temp_f: float | None) -> str | None:
    """Plain-english wadeability + whether the fish should be left alone.

    Water temperature outranks flow: warm water kills released trout even
    when the wading is pleasant, so it is checked first and stated bluntly.
    """
    if temp_f is not None:
        if temp_f >= 70:
            return (f"Water is {temp_f:.0f}F - too warm to fish for trout. "
                    "Released fish die at these temperatures. Leave them alone.")
        if temp_f >= 67:
            return (f"Water is {temp_f:.0f}F - marginal. Fish early, keep "
                    "fights short, or go find a bass.")
    if flow_cfs is None:
        return None
    if flow_cfs < 40:
        return (f"{flow_cfs:.0f} cfs - low and clear. Wading is easy and the "
                "fish can see you coming. Long leaders, short casts.")
    if flow_cfs < 200:
        return f"{flow_cfs:.0f} cfs - prime wading water."
    if flow_cfs < 500:
        return f"{flow_cfs:.0f} cfs - pushy. Wadeable at the edges, not across."
    return f"{flow_cfs:.0f} cfs - blown out. Stay on the bank."


def ohio_read(stage_ft: float | None, trend: str | None) -> str | None:
    """A stage reading turned into something a bank fisherman can use.

    Pool stage on the Ohio is not wadeability — it is whether the bank is
    fishable, how much current is moving, and whether the river is carrying
    mud. Thresholds are for the Byrd pool, which normally sits near 23-26 ft.
    """
    if stage_ft is None:
        return None
    moving = f" and {trend}" if trend in ("rising", "falling") else ""
    if stage_ft < 22:
        return (f"{stage_ft:.1f} ft{moving} — low and clear. Banks are wide "
                "open and the fish are holding to structure.")
    if stage_ft < 27:
        return f"{stage_ft:.1f} ft{moving} — normal pool. Ordinary bank access."
    if stage_ft < 34:
        return (f"{stage_ft:.1f} ft{moving} — up and pushing. Expect colour "
                "and current; fish the slack behind anything solid.")
    return (f"{stage_ft:.1f} ft{moving} — high water. Banks are going under "
            "and the river is carrying debris.")


def fetch_ohio(errors: list) -> list:
    """Stage and trend at the two gauges bracketing R.C. Byrd Locks and Dam."""
    out = []
    for gauge in OHIO_GAUGES:
        def _fetch(gauge=gauge):
            data = get("https://waterservices.usgs.gov/nwis/iv/",
                       {"format": "json", "sites": gauge["site"],
                        "parameterCd": "00065,00060", "period": "P2D"})
            rec: dict = {"water": gauge["water"], "site": gauge["site"],
                         "note": gauge["note"]}
            names = {"00065": "stage_ft", "00060": "discharge_cfs"}
            for series in data["value"]["timeSeries"]:
                code = series["variable"]["variableCode"][0]["value"]
                vals = [v for v in series["values"][0]["value"]
                        if v.get("value") not in (None, "", "-999999")]
                if not vals or code not in names:
                    continue
                key = names[code]
                rec[key] = float(vals[-1]["value"])
                rec[key + "_at"] = vals[-1]["dateTime"]
                if len(vals) > 1:
                    first = float(vals[0]["value"])
                    rec[key + "_24h_ago"] = first
                    delta = rec[key] - first
                    rec[key + "_trend"] = (
                        "rising" if delta > 0.25 else
                        "falling" if delta < -0.25 else "steady")
            rec["read"] = ohio_read(rec.get("stage_ft"), rec.get("stage_ft_trend"))
            return rec

        res = safe(_fetch, f"usgs:{gauge['key']}", errors)
        if res:
            out.append(res)
    return out


def fetch_williams(errors: list) -> dict | None:
    """Flow, stage, and temperature with a 24-hour trend, from USGS."""
    def _fetch():
        data = get("https://waterservices.usgs.gov/nwis/iv/",
                   {"format": "json", "sites": WILLIAMS_GAUGE,
                    "parameterCd": "00060,00065,00010", "period": "P2D"})
        out: dict = {"water": "Williams River (Cowen)",
                     "gauge": WILLIAMS_LABEL, "site": WILLIAMS_GAUGE}
        names = {"00060": "discharge_cfs", "00065": "stage_ft",
                 "00010": "water_temp_c"}
        for series in data["value"]["timeSeries"]:
            code = series["variable"]["variableCode"][0]["value"]
            vals = [v for v in series["values"][0]["value"]
                    if v.get("value") not in (None, "", "-999999")]
            if not vals or code not in names:
                continue
            key = names[code]
            out[key] = float(vals[-1]["value"])
            out[key + "_at"] = vals[-1]["dateTime"]
            if len(vals) > 1:
                first = float(vals[0]["value"])
                out[key + "_24h_ago"] = first
                delta = out[key] - first
                out[key + "_trend"] = (
                    "rising" if delta > abs(first) * 0.05
                    else "falling" if delta < -abs(first) * 0.05
                    else "steady")
        if "water_temp_c" in out:
            out["water_temp_f"] = round(out["water_temp_c"] * 9 / 5 + 32, 1)
        out["read"] = trout_read(out.get("discharge_cfs"),
                                 out.get("water_temp_f"))
        return out

    return safe(_fetch, "usgs:williams", errors)


# -------------------------------------------------------------- Topsail Beach

def _pick_tide_cycle(events: list[dict], today: "dt.date") -> list[dict]:
    """The full 2-high/2-low cycle centred on today, spillover included.

    Nate, 2026-08-19: always the complete daily table, even when one of the
    four events lands late the day before or early the day after — a lunar
    day runs ~24h50m, so on many calendar days only three events fall
    inside midnight-to-midnight and the missing one is exactly the one a
    trip plan needs. From three days of predictions, take the window of
    four consecutive events (they alternate H/L by nature) whose centre
    sits closest to today's noon, and tag anything outside today with its
    weekday so nobody reads a Wednesday tide as Thursday's.
    """
    if len(events) < 4:
        return events
    noon = dt.datetime.combine(today, dt.time(12, 0))
    best, best_gap = events[:4], None
    for i in range(len(events) - 3):
        window = events[i:i + 4]
        centre = window[0]["_when"] + (window[3]["_when"] - window[0]["_when"]) / 2
        gap = abs((centre - noon).total_seconds())
        if best_gap is None or gap < best_gap:
            best, best_gap = window, gap
    return best


def fetch_topsail_tides(stamp: str, errors: list) -> list:
    """The full daily tide cycle at both stations bracketing the inlet."""
    today = dt.datetime.strptime(stamp, "%Y%m%d").date()
    begin = (today - dt.timedelta(days=1)).strftime("%Y%m%d")
    end = (today + dt.timedelta(days=1)).strftime("%Y%m%d")
    out = []
    for st in TOPSAIL_TIDE_STATIONS:
        def _fetch(st=st):
            data = get(
                "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter",
                # datum and interval=hilo are BOTH mandatory here - without
                # hilo the API 400s and blames the datum, misleadingly.
                {"product": "predictions", "application": "ashgrove-times",
                 "begin_date": begin, "end_date": end, "datum": "MLLW",
                 "station": st["id"], "time_zone": "lst_ldt",
                 "units": "english", "interval": "hilo", "format": "json"})
            # NOAA answers 200 with an error body, so raise_for_status() never
            # fires - checking this key is the only real guard.
            if "error" in data:
                raise RuntimeError(f"NOAA: {data['error'].get('message','').strip()}")
            events = []
            for p in data.get("predictions", []):
                t = dt.datetime.strptime(p["t"], "%Y-%m-%d %H:%M")
                events.append({
                    "type": "high" if p["type"] == "H" else "low",
                    # Platform-independent 12-hour format (no %-I / %#I).
                    "time_local": t.strftime("%I:%M %p").lstrip("0"),
                    "height_ft": round(float(p["v"]), 1),
                    "_when": t,
                })
            events = _pick_tide_cycle(events, today)
            for event in events:
                when = event.pop("_when")
                if when.date() != today:
                    # Spillover carries its weekday so a Wednesday tide can
                    # never be read as Thursday's.
                    event["day"] = when.strftime("%a")
                    event["time_local"] += f" ({event['day']})"
            return {"station": st["name"], "station_id": st["id"],
                    "side": st["side"], "note": st["note"], "events": events}

        res = safe(_fetch, f"noaa-tides:{st['id']}", errors)
        if res:
            out.append(res)
    return out


def fetch_topsail_water_temp(errors: list) -> dict | None:
    def _fetch():
        data = get(
            "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter",
            {"product": "water_temperature", "application": "ashgrove-times",
             "date": "latest", "station": TOPSAIL_TEMP_STATION["id"],
             "units": "english", "time_zone": "lst_ldt", "format": "json"})
        if "error" in data or not data.get("data"):
            raise RuntimeError("NOAA: no water temperature returned")
        latest = data["data"][-1]
        return {"water_temp_f": round(float(latest["v"]), 1),
                "observed_at": latest["t"],
                "station": TOPSAIL_TEMP_STATION["name"],
                "miles_away": TOPSAIL_TEMP_STATION["miles_away"],
                "bearing": TOPSAIL_TEMP_STATION["bearing"]}

    return safe(_fetch, "noaa-temp", errors)


def moon_phase(now_utc: "dt.datetime") -> dict:
    """Approximate phase + illumination, good to about a day.

    Ported from Jim Claudtore's fetch_weather.py on 2026-08-21, when the
    Topsail report moved to Sports & Sportsman. A fishing fact, not
    decoration: new and full moons mean spring tides (bigger swings, harder
    inlet current), quarters mean neap.
    """
    import math
    ref = dt.datetime(2000, 1, 6, 18, 14, tzinfo=dt.timezone.utc)
    synodic = 29.53058867
    age = ((now_utc - ref).total_seconds() / 86400.0) % synodic
    frac = age / synodic
    illum = round((1 - math.cos(2 * math.pi * frac)) / 2 * 100)
    names = [(0.22, "waxing crescent"), (0.28, "first quarter"),
             (0.47, "waxing gibbous"), (0.53, "full moon"),
             (0.72, "waning gibbous"), (0.78, "last quarter"),
             (0.97, "waning crescent"), (1.01, "new moon")]
    name = "new moon" if frac < 0.03 else next(n for cut, n in names if frac <= cut)
    return {"phase": name, "illumination_pct": illum, "age_days": round(age, 1)}


def fetch_topsail(stamp: str, errors: list) -> dict | None:
    tides = fetch_topsail_tides(stamp, errors)
    temp = fetch_topsail_water_temp(errors)
    if not tides and not temp:
        return None
    out: dict = {"water": "Topsail Beach (surf and sound)", "tides": tides,
                 "moon": moon_phase(dt.datetime.now(dt.timezone.utc))}
    if temp:
        out["water_temp"] = temp
    # Lead the read with the SOUND. The crew fishes the backwater, and the
    # oceanfront station runs over an hour ahead of it -- quoting the surf
    # would send someone out on the wrong stage of the tide.
    sound = next((t for t in tides if t["side"] == "sound"), None)
    if sound and sound["events"]:
        highs = [e["time_local"] for e in sound["events"] if e["type"] == "high"]
        if highs:
            out["read"] = ("Fish the moving water either side of high at "
                           + " and ".join(highs) + " in the sound.")
    return out


# ---------------------------------------------------------------------- main

def build(errors: list) -> dict:
    now = local_today()
    return {
        "generated_at": now.isoformat(timespec="seconds"),
        "date": now.strftime("%Y-%m-%d"),
        "williams": fetch_williams(errors),
        "ohio": fetch_ohio(errors),
        "topsail": fetch_topsail(now.strftime("%Y%m%d"), errors),
        "errors": errors,
    }


def summarize(data: dict) -> str:
    lines = []
    w = data.get("williams")
    if w:
        bits = []
        if w.get("discharge_cfs") is not None:
            bits.append(f"{w['discharge_cfs']:.0f} cfs ({w.get('discharge_cfs_trend','?')})")
        if w.get("stage_ft") is not None:
            bits.append(f"{w['stage_ft']:.2f} ft")
        if w.get("water_temp_f") is not None:
            bits.append(f"{w['water_temp_f']:.0f}F")
        lines.append(f"Williams River: {', '.join(bits) or 'no readings'}")
        if w.get("read"):
            lines.append(f"  {w['read']}")
    else:
        lines.append("Williams River: unavailable")

    for o in data.get("ohio") or []:
        bits = []
        if o.get("stage_ft") is not None:
            bits.append(f"{o['stage_ft']:.1f} ft ({o.get('stage_ft_trend','?')})")
        if o.get("discharge_cfs") is not None:
            bits.append(f"{o['discharge_cfs']:,.0f} cfs")
        lines.append(f"{o['water']}: {', '.join(bits) or 'no readings'}")
        lines.append(f"  {o['note']}")
        if o.get("read"):
            lines.append(f"  {o['read']}")

    t = data.get("topsail")
    if t:
        for st in t.get("tides", []):
            ev = "  ".join(f"{e['type'][0].upper()} {e['time_local']} "
                           f"{e['height_ft']}ft" for e in st["events"])
            role = 'where you fish' if st.get('side') == 'sound' else 'surf'
            lines.append(f"Topsail {st['side']} ({st['station']}, {role}): {ev}")
        if t.get("water_temp"):
            wt = t["water_temp"]
            lines.append(f"  Water {wt['water_temp_f']}F "
                         f"(at {wt['station']}, {wt['miles_away']} mi "
                         f"{wt.get('bearing', 'away')})")
    else:
        lines.append("Topsail: unavailable")

    for e in data.get("errors", []):
        lines.append(f"  ! {e}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=os.path.join("out", "fishing.json"))
    parser.add_argument("--pretty", action="store_true",
                        help="print a human-readable summary as well")
    args = parser.parse_args()

    errors: list = []
    data = build(errors)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    if args.pretty:
        print(summarize(data))

    got = sum(1 for k in ("williams", "topsail") if data.get(k)) + len(data.get("ohio") or [])
    print(f"OK: wrote {args.out} ({got} waters, {len(errors)} source errors)")
    # Both waters dead is worth a non-zero exit; the caller decides whether a
    # fishing line is load-bearing enough to hold the paper.
    return 0 if got else 1


if __name__ == "__main__":
    sys.exit(main())
