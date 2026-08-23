#!/usr/bin/env python3
"""TZ-10 Stage B — calibrate DAY_RANGE_ABNORMAL from the data.binance.vision archive.

One-shot, MANUAL. Deliberately NOT wired into bench.yml: it is a calibration
run, not a control, and it needs the external archive plus a warm cache that
the gate is specifically built to avoid.

What it measures
----------------
For every coin-day in the archive: the day's high/low range divided by the
range a driftless walk would have produced over the same day, using the
trailing 90-day hourly volatility the bot itself would have published on that
day. The pooled 90th percentile of that distribution is the constant.

What it does NOT do
-------------------
It does not implement the measure. `dayRangeRatio` and `sigmaDay` are CUT OUT
of index.html at runtime and executed by node (inv. 21, inv. 38(1)); there is
no second implementation of the formula here, in Python or anywhere else.
Likewise `volatility` is not computed here: it comes from main.py's own metric
block through backtest_bench.CdBuilder, the same path backtest_bench.py uses.

The rule, registered by the TZ BEFORE the number was known (inv. 23)
-------------------------------------------------------------------
    DAY_RANGE_ABNORMAL = the pooled 90th percentile, rounded to two decimals,
    taken as-is. Never moved to make any particular date fire or not fire.
    If it lands below 1.60 or above 4.00 the stage is BLOCKED and reported
    without a production change.

This script enforces that window itself and exits non-zero outside it, so the
number cannot be quietly nudged by whoever runs it.

Usage
-----
    python3 bench/exhaustion_calib.py --years 3            # the calibration run
    python3 bench/exhaustion_calib.py --selftest           # offline, no network
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import backtest_bench as bb          # noqa: E402  (path set above)

HTML = os.path.join(ROOT, "index.html")
BOT = os.path.join(ROOT, "main.py")

# The window the TZ registered in advance. Not tunable, deliberately: a value
# outside it means the pipeline is broken, and the answer is a new TZ.
WINDOW_LO, WINDOW_HI = 1.60, 4.00

# dayRangeRatio calls both of these. Cutting them out is the point of the file.
JS_CUT = ["has", "sigmaDay", "dayRangeRatio"]

JS_DRIVER = r"""
'use strict';
var fs = require('fs');
__EXTRACTED__
var job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var out = [];
for (var i = 0; i < job.length; i++) {
    var j = job[i];
    out.push(dayRangeRatio(j[0], j[1], j[2], j[3]));
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
"""


def extract_js(html_path, names=JS_CUT):
    """Cut the named production functions out of index.html by brace matching.

    Uses backtest_bench's own scanner so there is one implementation of the
    cut in the repository, not two."""
    import re
    src = open(html_path, encoding="utf-8").read()
    out = []
    for name in names:
        m = re.search(r"\nfunction\s+" + name + r"\s*\(", src)
        if not m:
            raise SystemExit("index.html has no function " + name)
        b = src.index("{", m.end())
        out.append(src[m.start() + 1:bb._skip_to_matching_brace(src, b)])
    return "\n".join(out)


def ratios_via_node(jobs, js):
    """Run the extracted production function over every (hi, lo, cur, vol).

    One node process for the whole job: the formula is the production one,
    the batching is ours."""
    if not jobs:
        return []
    d = tempfile.mkdtemp(prefix="exh_")
    jsf = os.path.join(d, "driver.js")
    inf = os.path.join(d, "in.json")
    outf = os.path.join(d, "out.json")
    open(jsf, "w", encoding="utf-8").write(JS_DRIVER.replace("__EXTRACTED__", js))
    json.dump(jobs, open(inf, "w"))
    p = subprocess.run(["node", jsf, inf, outf], capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stdout[-4000:])
        print(p.stderr[-4000:], file=sys.stderr)
        raise SystemExit("node failed")
    res = json.load(open(outf))
    for f in (jsf, inf, outf):
        os.unlink(f)
    os.rmdir(d)
    if len(res) != len(jobs):
        raise SystemExit("node returned %d results for %d jobs" % (len(res), len(jobs)))
    return res


def spot_universe(html_path):
    """The 25 spot pairs of tokens[].

    The three fut:true assets are excluded BY DECLARATION (System Map §3.14,
    inv. 41), not because a host did or did not answer for them."""
    toks = bb.tokens_from_html(html_path)
    spot = [t for t in toks if not t.get("fut")]
    fut = [t for t in toks if t.get("fut")]
    return spot, fut


def coin_days(doc, builder):
    """Every complete UTC day of one coin as (hi, lo, cur, vol).

    prices/hl carry END-of-hour stamps (backtest_bench._series_from_rows), so a
    candle stamped t covers [t - 1h, t) and UTC day D owns the stamps
    (D_start, D_start + 24h]. Only days with all 24 candles are used: a partial
    day has a partial range and would understate it.

    vol is main.py's own trailing 90-day hourly volatility at the day's last
    candle — the same path backtest_bench.py uses, not a second formula."""
    prices = doc.get("prices") or []
    hl = doc.get("hl") or []
    if not hl:
        return [], "no hl in cache (refetch: cache key v4 carries high/low)"
    vols = doc.get("volumes") or []
    pts = [p[0] for p in prices]
    vts = [v[0] for v in vols] if vols else None

    by_ts = {}
    for i, p in enumerate(prices):
        by_ts[p[0]] = i
    days = {}
    for row in hl:
        ts = row[0]
        d = (ts - 1) // bb.DAY_MS
        days.setdefault(d, []).append(row)

    out = []
    for d in sorted(days):
        rows = days[d]
        if len(rows) != 24:
            continue                     # partial day: not a day
        last_ts = max(r[0] for r in rows)
        i = by_ts.get(last_ts)
        if i is None:
            continue
        cd = builder.build(prices, vols, i, pts, vts)
        if not cd:
            continue                     # < 90 days of trailing history yet
        vol = cd.get("volatility")
        hi = max(r[1] for r in rows)
        lo = min(r[2] for r in rows)
        cur = prices[i][1]
        out.append((hi, lo, cur, vol))
    return out, ""


def deciles(vals):
    """p0..p100 in tens. Linear interpolation, numpy's default — stated so the
    number is reproducible by anyone re-running this."""
    a = np.asarray(vals, float)
    return [(q, float(np.percentile(a, q))) for q in range(0, 101, 10)]


def report(vals, per_coin, skipped):
    n = len(vals)
    print("\n=== Pooled distribution ===")
    print("  coins contributing : %d" % len(per_coin))
    print("  coin-days pooled n : %d" % n)
    if skipped:
        print("  coins skipped      : %s" % ", ".join(skipped))
    if n == 0:
        raise SystemExit("BLOCKED: zero coin-days pooled — a calibration over "
                         "nothing is not a calibration (inv. 22).")
    print("\n  %-6s %10s" % ("pct", "ratio"))
    for q, v in deciles(vals):
        print("  p%-5d %10.4f" % (q, v))
    a = np.asarray(vals, float)
    print("\n  mean               : %.4f" % float(a.mean()))
    print("  median (p50)       : %.4f" % float(np.percentile(a, 50)))
    raw = float(np.percentile(a, 90))
    val = round(raw, 2)
    print("\n=== 90th percentile ===")
    print("  raw                : %.6f" % raw)
    print("  rounded to 2 dp    : %.2f" % val)
    print("\n  per-coin n and p90:")
    for sym in sorted(per_coin):
        cv = np.asarray(per_coin[sym], float)
        print("    %-8s n=%5d  p90=%.4f  p50=%.4f"
              % (sym, len(cv), float(np.percentile(cv, 90)), float(np.percentile(cv, 50))))
    print("\n=== Registered rule (inv. 23) ===")
    print("  window             : %.2f .. %.2f (registered before the number)"
          % (WINDOW_LO, WINDOW_HI))
    if val < WINDOW_LO or val > WINDOW_HI:
        print("  verdict            : BLOCKED — outside the window.")
        print("\nDAY_RANGE_ABNORMAL is NOT adopted. Stage C makes no production")
        print("change. A threshold outside the window means the measure is not")
        print("measuring what TZ-10 claims: the answer is a new TZ, not a nudge.")
        return val, False
    print("  verdict            : in window")
    print("\nDAY_RANGE_ABNORMAL = %.2f" % val)
    print("Taken as-is. Not moved to make 2026-08-22 fire, not moved to make any")
    print("other date fire or not fire, and never retuned afterwards.")
    return val, True


def run(years, source):
    spot, fut = spot_universe(HTML)
    print("Universe: %d spot of %d declared tokens (fut:true excluded by "
          "declaration, inv. 41): %s" % (len(spot), len(spot) + len(fut),
                                         ", ".join(t["name"] for t in fut)))
    js = extract_js(HTML)
    print("Cut out of index.html: %s" % ", ".join(JS_CUT))

    want = set(t["name"] for t in spot)
    have = set()
    if os.path.isdir(bb.CACHE):
        have = set(f[:-5] for f in os.listdir(bb.CACHE)
                   if f.endswith(".json") and not f.startswith("_"))
    if not want.issubset(have):
        print("\nCache incomplete (%d of %d) — the archive is needed."
              % (len(want & have), len(want)))
        # Probe before downloading so a closed host reports itself as a
        # blocker instead of surfacing as a stack trace 25 pairs later.
        # inv. 24: only data.binance.vision / data-api.binance.vision answer
        # from a runner, and neither answers at all from behind an egress
        # policy that denies them.
        print("Source availability:")
        alive = bb.probe(verbose=True)
        if source not in alive:
            print("\nBLOCKED: '%s' does not answer from this host, and the "
                  "cache is cold." % source)
            print("The calibration cannot run without the archive. This is an "
                  "environment blocker,")
            print("not a defect in the measure: run it where "
                  "data.binance.vision is reachable.")
            return 2
        bb.fetch_prices(HTML, BOT, years=years, source=source)

    builder = bb.CdBuilder(BOT)
    cache = bb.load_cache(keep_btc=True)
    pooled, per_coin, skipped = [], {}, []
    for t in spot:
        sym = t["name"]
        doc = cache.get(sym)
        if not doc:
            skipped.append(sym + " (not in cache)")
            continue
        days, why = coin_days(doc, builder)
        if not days:
            skipped.append(sym + (" (" + why + ")" if why else " (no complete days)"))
            continue
        vals = [r for r in ratios_via_node(days, js) if r is not None]
        if not vals:
            skipped.append(sym + " (every day returned null)")
            continue
        per_coin[sym] = vals
        pooled += vals
        print("  %-8s coin-days %5d  usable %5d" % (sym, len(days), len(vals)))

    val, ok = report(pooled, per_coin, skipped)
    return 0 if ok else 1


def selftest():
    """Offline proof that the pipeline is wired correctly, with no network.

    A synthetic coin whose every day has a known constant ratio: if the cut,
    the node hop, the day grouping and the percentile all work, the pooled
    p90 is that constant. Does not touch data.binance.vision and does not
    substitute for the calibration run."""
    print("=== Stage B self-test (offline) ===")
    js = extract_js(HTML)
    checks = fails = 0

    def eq(name, got, want, tol=1e-12):
        nonlocal checks, fails
        checks += 1
        ok = (got is None and want is None) or (
            got is not None and want is not None and abs(got - want) <= tol)
        if not ok:
            fails += 1
            print("  FAIL %s: got %r want %r" % (name, got, want))

    # 1. The cut really produced the production function, and node runs it.
    got = ratios_via_node([[110.0, 100.0, 105.0, 0.01]], js)[0]
    want = (110.0 - 100.0) / (105.0 * 0.01 * (24 ** 0.5) * ((8 / np.pi) ** 0.5))
    eq("node runs the extracted dayRangeRatio", got, want)

    # 2. Nulls survive the JSON hop as nulls, never as zeros.
    nulls = ratios_via_node([[110.0, 100.0, 105.0, 0.0],
                             [110.0, 100.0, 0.0, 0.01],
                             [100.0, 100.0, 105.0, 0.01],
                             [90.0, 100.0, 105.0, 0.01]], js)
    for i, v in enumerate(nulls):
        eq("null case %d" % i, v, None)

    # 3. Day grouping: 24 end-of-hour stamps make one day, 23 make none.
    class FakeBuilder(object):
        def build(self, prices, vols, i, pts=None, vts=None):
            return {"volatility": 0.01}

    def synth(n_days, per_day=24, day0=20000):
        prices, hl = [], []
        for d in range(n_days):
            for h in range(per_day):
                ts = (day0 + d) * bb.DAY_MS + (h + 1) * bb.HOUR_MS
                prices.append([ts, 100.0])
                hl.append([ts, 110.0, 100.0])
        return {"prices": prices, "hl": hl, "volumes": []}

    days, _ = coin_days(synth(5), FakeBuilder())
    eq("5 complete days -> 5", float(len(days)), 5.0)
    days, _ = coin_days(synth(5, per_day=23), FakeBuilder())
    eq("partial days -> 0", float(len(days)), 0.0)
    days, why = coin_days({"prices": [], "hl": []}, FakeBuilder())
    eq("no hl -> 0", float(len(days)), 0.0)
    checks += 1
    if not why:
        fails += 1
        print("  FAIL missing hl must explain itself")

    # 4. End to end: a constant-ratio coin pools to that constant at every pct.
    days, _ = coin_days(synth(40), FakeBuilder())
    vals = [r for r in ratios_via_node(days, js) if r is not None]
    eq("40 days pooled", float(len(vals)), 40.0)
    const = (110.0 - 100.0) / (100.0 * 0.01 * (24 ** 0.5) * ((8 / np.pi) ** 0.5))
    eq("p90 of a constant series", float(np.percentile(np.asarray(vals), 90)), const)

    # 5. The window gate refuses a value it must refuse.
    checks += 1
    if not (WINDOW_LO <= 2.5 <= WINDOW_HI) or (WINDOW_LO <= 0.5 <= WINDOW_HI):
        fails += 1
        print("  FAIL window gate does not bracket as registered")

    print("\n--- checks: %d  fails: %d ---" % (checks, fails))
    if checks == 0:
        print("FAIL self-test verified nothing")
        return 1
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--years", type=float, default=3.0,
                    help="archive depth in years (default 3)")
    ap.add_argument("--source", default="vision",
                    help="backtest_bench source id (default vision)")
    ap.add_argument("--selftest", action="store_true",
                    help="offline wiring proof, no network")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    return run(a.years, a.source)


if __name__ == "__main__":
    sys.exit(main())
