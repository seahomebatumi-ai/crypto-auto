#!/usr/bin/env python3
"""The exchangeInfo watcher (TZ-54 B5, TZ-57 B3): Binance Futures' dated listing
state, polled every 900 s and compared with the stored snapshot.

Alerts only (TZ-57): a change reaches the owner as an alert and he decides
whether to press the button; this program requests no run.

    exchange.py [--once] [--state-dir <dir>]      default /var/lib/crypto-auto

The first poll stores a baseline and alerts nothing. --once polls once and
prints counts.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import date, datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

URL = "https://fapi.binance.com/fapi/v1/exchangeInfo"
POLL_S = 900
NO_DELIVERY = date(2100, 12, 25)          # TZ-53 C5: a deliveryDate on this UTC date means none
SNAPSHOT = "exchange-snapshot.json"
PERPETUALS = "perpetuals.json"


def fetch_info():
    with urllib.request.urlopen(URL, timeout=common.HTTP_TIMEOUT_S) as resp:
        return json.loads(resp.read())


def utc_date(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).date()


def snapshot(info):
    """Per USDT symbol: [status, contractType, deliveryDate or None, onboardDate]."""
    out = {}
    for row in info.get("symbols", []):
        if not isinstance(row, dict) or row.get("quoteAsset") != "USDT":
            continue
        delivery = row.get("deliveryDate")
        if not isinstance(delivery, int) or utc_date(delivery) == NO_DELIVERY:
            delivery = None
        out[row.get("symbol")] = [row.get("status"), row.get("contractType"), delivery, row.get("onboardDate")]
    return out


def perpetuals(info):
    """TRADING PERPETUAL USDT symbols: the base with a leading run of digits
    removed (1000PEPE → PEPE) and the full symbol, which keeps it."""
    out = []
    for row in info.get("symbols", []):
        if (isinstance(row, dict) and row.get("quoteAsset") == "USDT" and row.get("contractType") == "PERPETUAL"
                and row.get("status") == "TRADING"):
            out.append({"base": re.sub(r"^[0-9]+", "", row.get("baseAsset", "")), "symbol": row.get("symbol")})
    return sorted(out, key=lambda r: (r["base"], r["symbol"]))


def changes(prev, cur, list_symbols):
    """Rows of TZ-54 B5's table, split by list symbol and any other symbol."""
    out = {"new_perpetual": ([], []), "delivery_set": ([], []), "status_changed": ([], [])}
    for symbol, (status, ctype, delivery, _onboard) in sorted(cur.items()):
        side = 0 if symbol in list_symbols else 1
        if symbol not in prev:
            if ctype == "PERPETUAL":
                out["new_perpetual"][side].append(symbol)
            continue
        old_status, _old_type, old_delivery, _old_onboard = prev[symbol]
        if delivery is not None and delivery != old_delivery:
            out["delivery_set"][side].append(symbol)
        if status != old_status:
            out["status_changed"][side].append((symbol, old_status, status))
    return out


def act(found, cur):
    """Alerts by TZ-54 B5's table, without a run request (TZ-57). Returns the
    number of alerts."""
    alerts = 0
    for symbol in found["new_perpetual"][1]:
        common.write_outbox("alert", common.A2.format(symbol=symbol))
        alerts += 1
    for side in (0, 1):
        for symbol in found["delivery_set"][side]:
            if side == 1 and cur[symbol][1] != "PERPETUAL":
                continue
            text = common.A3.format(symbol=symbol, ddmmyyyy=utc_date(cur[symbol][2]).strftime("%d.%m.%Y"))
            common.write_outbox("alert", text)
            alerts += 1
    for symbol, old, new in found["status_changed"][0]:
        common.write_outbox("alert", common.A4.format(symbol=symbol, old=old, new=new))
        alerts += 1
    return alerts


def poll(state_dir):
    info = fetch_info()
    cur = snapshot(info)
    list_symbols = {"BTCUSDT"} | {row["s"] for row in common.read_tokens()}
    path = os.path.join(state_dir, SNAPSHOT)
    try:
        with open(path, encoding="utf-8") as fh:
            prev = json.load(fh)["symbols"]
        baseline = False
    except (OSError, ValueError, KeyError):
        prev, baseline = None, True
    found = changes(prev, cur, list_symbols) if not baseline else changes(cur, cur, list_symbols)
    alerts = 0 if baseline else act(found, cur)
    common.atomic_write(path, {"ts": common.utc_now().strftime("%Y-%m-%dT%H:%M:%SZ"), "symbols": cur})
    perps = perpetuals(info)
    common.atomic_write(os.path.join(state_dir, PERPETUALS), perps)
    common.log("exchange: symbols=%d usdt=%d trading_perpetuals=%d baseline=%s "
               "new_perpetual=list:%d/other:%d delivery_set=list:%d/other:%d status_changed=list:%d/other:%d "
               "alerts=%d"
               % (len(info.get("symbols", [])), len(cur), len(perps), "yes" if baseline else "no",
                  len(found["new_perpetual"][0]), len(found["new_perpetual"][1]),
                  len(found["delivery_set"][0]), len(found["delivery_set"][1]),
                  len(found["status_changed"][0]), len(found["status_changed"][1]), alerts))


def main(argv=None):
    parser = argparse.ArgumentParser(description="the exchangeInfo watcher")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--state-dir", default=common.STATE_DIR)
    args = parser.parse_args(argv)
    if args.once:
        poll(args.state_dir)
        return 0
    while True:
        started = time.monotonic()
        try:
            poll(args.state_dir)
        except Exception as exc:
            common.log("exchange: poll failed (%s)" % exc.__class__.__name__)
        time.sleep(max(1.0, POLL_S - (time.monotonic() - started)))


if __name__ == "__main__":
    sys.exit(main())
