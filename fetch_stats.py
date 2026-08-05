"""Fetch the market numbers under the lead story — or honestly fetch nothing.

The paper posts pre-market ET, so the strip prints the PREVIOUS CLOSE and is
labeled that way. Every entry carries the exact strings the edition JSON must
copy verbatim: validate_edition.py byte-matches `label` and `value` against
this file, and a stat_strip entry that is not in here is a hard failure. That
is the whole point — decoration degrades to nothing, never to a remembered
number.

Source ladder, verified live from this machine (2026-08-04):
    Yahoo v8 chart  query1.finance.yahoo.com/v8/finance/chart/^GSPC   -> 200
    CoinGecko       api.coingecko.com/api/v3/simple/price             -> 200
    (stooq's CSV endpoint 404s on every symbol — do not add it back)

Yahoo is the index source and CoinGecko adds Bitcoin; they are independent,
so one dying still yields a partial strip. If both die the file is written
with an empty `entries` list and both renderers omit the strip band.

    python fetch_stats.py [--out out/stats.json]

Always exits 0 and always writes the file — a stat strip is decoration, and
decoration may never be able to stop the paper.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

import config

try:
    import requests
except ImportError:  # pragma: no cover - bare sandbox without pip
    requests = None

TIMEOUT = 15
MAX_STALE_TRADING_DAYS = 4

YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=10d&interval=1d"
COINGECKO_PRICE = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true"
)

# Short labels — the strip is a band under the lead, not a table.
YAHOO_SYMBOLS = [
    {"symbol": "^GSPC", "label": "S&P 500"},
    {"symbol": "^DJI", "label": "Dow"},
    {"symbol": "^IXIC", "label": "Nasdaq"},
]

HEADERS = {"User-Agent": config.USER_AGENT, "Accept": "application/json"}


def _get_json(url: str) -> dict:
    """GET JSON through requests, or stdlib urllib when pip never happened."""
    if requests is not None:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _direction(pct: float) -> str:
    if pct > 0.005:
        return "up"
    if pct < -0.005:
        return "down"
    return "flat"


def _trading_days_between(older: dt.date, newer: dt.date) -> int:
    """Weekday count between two dates — close enough for a staleness gate."""
    if older >= newer:
        return 0
    days = 0
    cursor = older
    while cursor < newer and days <= 60:
        cursor += dt.timedelta(days=1)
        if cursor.weekday() < 5:
            days += 1
    return days


def _fetch_index(spec: dict, errors: list[str]) -> dict | None:
    """One index's previous close and its move off the session before it.

    Yahoo's daily series includes today's bar once the session opens, so the
    bar dated today (in exchange time) is dropped: pre-market, "previous
    close" has to mean the last COMPLETED session.
    """
    url = YAHOO_CHART.format(symbol=urllib.parse.quote(spec["symbol"], safe=""))
    try:
        payload = _get_json(url)
        result = payload["chart"]["result"][0]
        meta = result["meta"]
        timestamps = result["timestamp"]
        closes = result["indicators"]["quote"][0]["close"]
    except Exception as exc:  # noqa: BLE001 - any failure means skip this symbol
        errors.append(f"yahoo:{spec['symbol']}: {type(exc).__name__}: {exc}")
        return None

    offset = int(meta.get("gmtoffset") or 0)
    today_exchange = (
        dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=offset)
    ).date()

    bars: list[tuple[dt.date, float]] = []
    for ts, close in zip(timestamps, closes):
        if ts is None or close is None:
            continue
        day = (
            dt.datetime.fromtimestamp(ts, dt.timezone.utc)
            + dt.timedelta(seconds=offset)
        ).date()
        if day >= today_exchange:
            continue
        bars.append((day, float(close)))

    if len(bars) < 2:
        errors.append(f"yahoo:{spec['symbol']}: fewer than 2 completed sessions")
        return None

    as_of, close = bars[-1]
    _, prior = bars[-2]
    stale = _trading_days_between(as_of, today_exchange)
    if stale > MAX_STALE_TRADING_DAYS:
        errors.append(
            f"yahoo:{spec['symbol']}: last close {as_of} is {stale} trading days old"
        )
        return None

    pct = ((close - prior) / prior * 100) if prior else 0.0
    return {
        "label": spec["label"],
        "value": f"{close:,.2f}",
        "change": f"{pct:+.2f}%",
        "direction": _direction(pct),
        "symbol": spec["symbol"],
        "source": "Yahoo Finance",
        "as_of": as_of.isoformat(),
        "as_of_label": "prev close",
    }


def _fetch_bitcoin(errors: list[str]) -> dict | None:
    try:
        payload = _get_json(COINGECKO_PRICE)
        coin = payload["bitcoin"]
        price = float(coin["usd"])
        pct = float(coin.get("usd_24h_change") or 0.0)
        updated = int(coin.get("last_updated_at") or 0)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"coingecko: {type(exc).__name__}: {exc}")
        return None

    as_of = (
        dt.datetime.fromtimestamp(updated, dt.timezone.utc).date()
        if updated
        else dt.datetime.now(dt.timezone.utc).date()
    )
    return {
        "label": "Bitcoin",
        "value": f"${price:,.0f}",
        "change": f"{pct:+.2f}%",
        "direction": _direction(pct),
        "symbol": "BTC-USD",
        "source": "CoinGecko",
        "as_of": as_of.isoformat(),
        "as_of_label": "24h",
    }


def fetch() -> dict:
    """The whole ladder. Never raises; an empty `entries` list is a valid day."""
    errors: list[str] = []
    entries = []
    for spec in YAHOO_SYMBOLS:
        entry = _fetch_index(spec, errors)
        if entry:
            entries.append(entry)
    bitcoin = _fetch_bitcoin(errors)
    if bitcoin:
        entries.append(bitcoin)

    return {
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "entries": entries[: config.STAT_STRIP_MAX],
        "errors": errors,
    }


def main() -> int:
    config.use_utf8_stdio()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=config.STATS_PATH,
                        help="where to write the stats blob")
    args = parser.parse_args()

    blob = fetch()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(blob, f, indent=2, ensure_ascii=False)
        f.write("\n")

    labels = ", ".join(e["label"] for e in blob["entries"]) or "none"
    print(f"OK: wrote {args.out} — {len(blob['entries'])} entr"
          f"{'y' if len(blob['entries']) == 1 else 'ies'} ({labels})")
    for err in blob["errors"]:
        print(f"WARN: {err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
