#!/usr/bin/env python3
"""The payload writer (TZ-54 B2): analyst/live.json from fapi.binance.com in the
Shortcut's schema, proved by the unmodified gate, committed and pushed to main.

    writer.py --tree <dir>

Prints one line and never a value. Exit 0 pushed · 3 gate refused · 4 read or
build failed · 5 push failed twice (a commit or a rebase that fails is the same
class: the payload did not reach main).
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

FAPI = "https://fapi.binance.com"
TICKER_URL = FAPI + "/fapi/v1/ticker/24hr"
PREMIUM_URL = FAPI + "/fapi/v1/premiumIndex"
OI_URL = FAPI + "/fapi/v1/openInterest?symbol=%s"
COMMIT_MESSAGE = "analyst: live.json (vps)"
PAYLOAD = "analyst/live.json"
GATE = "analyst/live-gate.sh"

# TZ-54 §12.6's derivation, read on 01.10.2026 against the committed payload
# (31 of 31 rows per admitted candidate; report A5). Keys in the order c's rows carry them.
MAPPING = (
    ("chg", "ticker", "priceChangePercent"),
    ("fr", "premiumIndex", "lastFundingRate"),
    ("h", "ticker", "highPrice"),
    ("l", "ticker", "lowPrice"),
    ("mark", "premiumIndex", "markPrice"),
    ("oi", "openInterest", "openInterest"),
    ("p", "ticker", "lastPrice"),
    ("qv", "ticker", "quoteVolume"),
)


class BuildError(Exception):
    pass


def fetch_json(url):
    """One GET with urllib, 20 s timeout, no header added (rule 3)."""
    with urllib.request.urlopen(url, timeout=common.HTTP_TIMEOUT_S) as resp:
        body = resp.read()
    return json.loads(body)


def payload_symbols(tree):
    """BTCUSDT followed by tokens[].s in tokens[] order."""
    return ["BTCUSDT"] + [row["s"] for row in common.read_tokens(os.path.join(tree, "index.html"))]


def build_payload(ticker_rows, premium_rows, oi_by_symbol, symbols, ts):
    """Top-level keys exactly c, n, src, ts, x. A symbol missing from any source
    raises: no payload at all, never a partial row."""
    if not isinstance(ticker_rows, list) or not isinstance(premium_rows, list):
        raise BuildError("a bulk source is not an array")
    sources = {
        "ticker": {row.get("symbol"): row for row in ticker_rows if isinstance(row, dict)},
        "premiumIndex": {row.get("symbol"): row for row in premium_rows if isinstance(row, dict)},
        "openInterest": oi_by_symbol,
    }
    c = []
    for symbol in symbols:
        row = {}
        for field, source, key in MAPPING:
            record = sources[source].get(symbol)
            if not isinstance(record, dict) or not isinstance(record.get(key), str):
                raise BuildError("%s: %s.%s absent" % (symbol, source, key))
            row[field] = record[key]
        row["s"] = symbol
        c.append(row)
    return {"c": c, "n": len(c), "src": "fapi", "ts": ts, "x": ticker_rows}


def read_sources(symbols):
    """The bulk ticker, the bulk premiumIndex, and openInterest per c symbol,
    one at a time. ts is the moment the bulk ticker response completed."""
    ticker = fetch_json(TICKER_URL)
    ts = common.utc_now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    premium = fetch_json(PREMIUM_URL)
    oi = {}
    for symbol in symbols:
        doc = fetch_json(OI_URL % symbol)
        if not isinstance(doc, dict) or doc.get("symbol") != symbol:
            raise BuildError("%s: openInterest answered for another symbol" % symbol)
        oi[symbol] = doc
    return ticker, premium, oi, ts


def write_payload(tree, payload):
    common.atomic_write(os.path.join(tree, PAYLOAD), payload, mode=0o644)


def run_gate(tree):
    """The gate exactly as its usage line invokes it: no argument, in the tree."""
    return subprocess.run([os.path.join(".", GATE)], cwd=tree,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def git(tree, *args):
    return subprocess.run(["git", "-C", tree] + list(args),
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode


def git_out(tree, *args):
    return subprocess.run(["git", "-C", tree] + list(args), capture_output=True, text=True).stdout.strip()


def restore(tree):
    git(tree, "checkout", "HEAD", "--", PAYLOAD)


def publish(tree):
    """Commit and push; one rejection → pull --rebase and push again; a rebase
    conflict → abort it and drop the writer's commit. Returns (committed, pushed)."""
    base = git_out(tree, "rev-parse", "HEAD")
    if git(tree, "commit", "-q", "-m", COMMIT_MESSAGE, "--", PAYLOAD) != 0:
        restore(tree)
        return False, False
    if git(tree, "push", "-q", "origin", "HEAD:main") == 0:
        return True, True
    if git(tree, "pull", "-q", "--rebase", "origin", "main") != 0:
        git(tree, "rebase", "--abort")
        git(tree, "reset", "-q", "--hard", base)
        return True, False
    if git(tree, "push", "-q", "origin", "HEAD:main") == 0:
        return True, True
    git(tree, "reset", "-q", "--hard", "HEAD~1")
    return True, False


def main(argv=None):
    parser = argparse.ArgumentParser(description="write analyst/live.json from fapi.binance.com")
    parser.add_argument("--tree", required=True)
    args = parser.parse_args(argv)
    tree = os.path.abspath(args.tree)
    state = {"gate_exit": "-", "committed": "no", "pushed": "no", "rows_c": 0, "rows_x": 0}

    def report(code):
        print("writer: gate_exit=%s committed=%s pushed=%s rows_c=%d rows_x=%d"
              % (state["gate_exit"], state["committed"], state["pushed"], state["rows_c"], state["rows_x"]),
              flush=True)
        return code

    try:
        symbols = payload_symbols(tree)
        ticker, premium, oi, ts = read_sources(symbols)
        payload = build_payload(ticker, premium, oi, symbols, ts)
        state["rows_c"], state["rows_x"] = len(payload["c"]), len(payload["x"])
        write_payload(tree, payload)
    except Exception:
        restore(tree)
        return report(4)
    gate_exit = run_gate(tree)
    state["gate_exit"] = gate_exit
    if gate_exit != 0:
        restore(tree)
        return report(3)
    committed, pushed = publish(tree)
    state["committed"] = "yes" if committed else "no"
    state["pushed"] = "yes" if pushed else "no"
    return report(0 if pushed else 5)


if __name__ == "__main__":
    sys.exit(main())
