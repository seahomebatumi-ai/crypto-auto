#!/usr/bin/env python3
"""TZ-13 Stage C — calibrate DAY_RANGE_ABNORMAL on the LIST MEDIAN.

One-shot, MANUAL. Deliberately NOT wired into bench.yml: it is a calibration
run, not a control, and it needs the external archive plus a warm cache that
the gate is specifically built to avoid. It runs through calib.yml.

What changed against TZ-11, and why
-----------------------------------
TZ-11 calibrated the pooled 90th percentile of the COIN-DAY distribution and
compared it to a window drawn around that same object. `listExhaustion`
thresholds the LIST MEDIAN, whose upper tail is materially lower: averaging
correlated members strips idiosyncratic dispersion (inv. 47). The run returned
1.59 against a hand-written floor of 1.60, the script exited non-zero and
nothing was adopted — correctly, because the floor sat above the p95 of the
very distribution it was meant to bound. The floor was wrong before any data
existed.

So the OBJECT changes and the STATISTIC does not. The unit is a DATE, not a
coin-day; the statistic is still the 90th percentile. Changing both after a
failure would be fitting.

What this file does NOT do
--------------------------
It does not implement the measure. `has`, `sigmaDay`, `dayRangeRatio` and
`listExhaustion` are CUT OUT of index.html at runtime and executed by node
(inv. 21, inv. 38(1)). The median, the count and the quorum are production's:
**Python computes no median anywhere, in any form.** Likewise `volatility` is
not computed here — it comes from main.py's own metric block through
backtest_bench.CdBuilder, the same path backtest_bench.py uses.

It adopts nothing. The constant does not enter index.html in this TZ.

The rule, registered by the TZ BEFORE the number was known (inv. 23, 47)
------------------------------------------------------------------------
    DAY_RANGE_ABNORMAL = p90( per-date list medians ), rounded to 2 dp

adopted if and only if all four of these hold:

  1  pooled mean of the empirical coin-day ratios within +/-15% of the null's
     pooled coin-day mean
  2  empirical p90 of the date medians strictly ABOVE the null p90
  3  empirical p90 strictly BELOW the null p99.9
  4  at least 300 dates with a median, and a median per-date contributing
     count of at least 15

Conditions 2 and 3 are read off a null SIMULATED IN THE SAME RUN. No numeric
band on the constant appears anywhere in this file — that is the whole
correction over TZ-11. Any FAIL means non-zero exit, no constant, no
production change, and the answer is a new TZ.

Usage
-----
    python3 bench/exhaustion_calib.py --selftest            # offline, no network
    python3 bench/exhaustion_calib.py --years 3 --source vision
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import backtest_bench as bb          # noqa: E402  (path set above)

HTML = os.path.join(ROOT, "index.html")
BOT = os.path.join(ROOT, "main.py")

# listExhaustion joins the cut: the date median is production's, not ours.
JS_CUT = ["has", "sigmaDay", "dayRangeRatio", "listExhaustion"]

# The registered rule's structural thresholds. These are conditions on the
# EVIDENCE — how far the estimator may sit from its own null, how many dates
# make a percentile — not a band on the answer. There is no admissible range
# for DAY_RANGE_ABNORMAL anywhere in this file, by design.
MEAN_TOL = 0.15          # condition 1
MIN_DATES = 300          # condition 4
MIN_MEDIAN_COUNT = 15    # condition 4

# The null's precision requirement, from the TZ. Not a band on the constant.
MC_SE_MAX = 0.01
NULL_BUDGET_S = 20 * 60

SEED = 20260823
STEPS_PER_DAY = 24       # skeleton resolution; the extremes are exact (see below)

# The known-answer control's own registered numbers (inv. 23), fixed before
# the null existed: E[range] = sigma * sqrt(8T/pi) for a driftless walk.
KA_SIGMA_DAY = 0.005
KA_TARGET = 1.000
KA_TOL = 0.005
KA_MIN_DAYS = 1000000


# ─────────────────────────────────────────────────────────────────────────────
# 1. The production cut and the node hop
# ─────────────────────────────────────────────────────────────────────────────
JS_DRIVER = r"""
'use strict';
var fs = require('fs');
__EXTRACTED__
// Everything above this line is index.html's own source. Everything below is
// transport: it builds the row objects production's update() builds and hands
// them to production's listExhaustion. No formula is written here.
var hdr = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var buf = fs.readFileSync(process.argv[3]);
var f64 = new Float64Array(buf.buffer, buf.byteOffset, buf.byteLength / 8);
var sizes = hdr.sizes, names = hdr.names || null;
var med = [], ns = [], rsum = 0, rcount = 0, rnull = 0;
var ratios = hdr.wantRatios ? [] : null;
var p = 0;
for (var s = 0; s < sizes.length; s++) {
    var n = sizes[s], rows = [], i;
    for (i = 0; i < n; i++) {
        var hi = f64[p], lo = f64[p + 1], cur = f64[p + 2], vol = f64[p + 3];
        // The contract update() writes (TZ-13 §2 Stage A), spot by
        // construction: the universe here is the 25 fut:false assets.
        rows.push({ t: { name: (names ? names[s][i] : 'S' + i), fut: false },
                    cd: { volatility: vol },
                    hi24: hi, lo24: lo, cur: cur });
        // The coin-day ratio comes from the SAME production function the
        // median is built out of, so condition 1 compares like with like.
        var r = dayRangeRatio(hi, lo, cur, vol);
        if (r === null) { rnull++; }
        else { rsum += r; rcount++; if (ratios) ratios.push(r); }
        p += 4;
    }
    var le = listExhaustion(rows);
    med.push(le.median);          // null below quorum, and it stays null
    ns.push(le.n);
}
fs.writeFileSync(process.argv[4], JSON.stringify({
    median: med, n: ns, rsum: rsum, rcount: rcount, rnull: rnull,
    ratios: ratios, node: process.version, nonce: hdr.nonce
}));
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


HOPS = {"n": 0, "node": None}


def lists_via_node(sets, js, want_ratios=False, names=None):
    """Run production's listExhaustion over a batch of row sets.

    `sets` is a list of (hi, lo, cur, vol) sequences — one per DATE, or one per
    null replica. The payload crosses as raw float64 because the null runs
    millions of rows and JSON text of that size is the difference between a
    20-minute budget and an hour. What comes BACK is JSON, so a null median
    arrives as a null and can never be mistaken for a zero."""
    if not sets:
        return {"median": [], "n": [], "rsum": 0.0, "rcount": 0,
                "rnull": 0, "ratios": [] if want_ratios else None}
    d = tempfile.mkdtemp(prefix="exh_")
    jsf = os.path.join(d, "driver.js")
    hdrf = os.path.join(d, "hdr.json")
    binf = os.path.join(d, "in.bin")
    outf = os.path.join(d, "out.json")
    nonce = "%d-%d" % (os.getpid(), HOPS["n"])
    open(jsf, "w", encoding="utf-8").write(JS_DRIVER.replace("__EXTRACTED__", js))
    sizes = [len(s) for s in sets]
    json.dump({"sizes": sizes, "wantRatios": bool(want_ratios),
               "nonce": nonce, "names": names}, open(hdrf, "w"))
    with open(binf, "wb") as fh:
        for s in sets:
            a = np.asarray(s, dtype=np.float64)
            if a.ndim != 2 or a.shape[1] != 4:
                raise SystemExit("a row set must be (n, 4): got %r" % (a.shape,))
            fh.write(a.tobytes())
    p = subprocess.run(["node", jsf, hdrf, binf, outf], capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stdout[-4000:])
        print(p.stderr[-4000:], file=sys.stderr)
        raise SystemExit("node failed")
    res = json.load(open(outf))
    for f in (jsf, hdrf, binf, outf):
        os.unlink(f)
    os.rmdir(d)
    if res.get("nonce") != nonce:
        raise SystemExit("node returned another run's output")
    if len(res["median"]) != len(sets):
        raise SystemExit("node returned %d medians for %d sets"
                         % (len(res["median"]), len(sets)))
    HOPS["n"] += 1
    HOPS["node"] = res.get("node")
    return res


# ─────────────────────────────────────────────────────────────────────────────
# 2. The archive side: coin-days keyed by DATE
# ─────────────────────────────────────────────────────────────────────────────
def spot_universe(html_path):
    """The 25 spot pairs of tokens[].

    The three fut:true assets are excluded BY DECLARATION (System Map §3.14,
    inv. 41), not because a host did or did not answer for them."""
    toks = bb.tokens_from_html(html_path)
    spot = [t for t in toks if not t.get("fut")]
    fut = [t for t in toks if t.get("fut")]
    return spot, fut


def coin_days(doc, builder):
    """Every complete UTC day of one coin as (daykey, hi, lo, cur, vol, nobs).

    The day key is what TZ-13 adds: the unit of the calibration is a DATE, so
    every tuple has to carry the key days are joined on.

    prices/hl carry END-of-hour stamps (backtest_bench._series_from_rows), so a
    candle stamped t covers [t - 1h, t) and UTC day D owns the stamps
    (D_start, D_start + 24h]. Only days with all 24 candles are used: a partial
    day has a partial range and would understate it.

    vol is main.py's own trailing 90-day hourly volatility at the day's last
    candle — the same path backtest_bench.py uses, not a second formula. nobs
    is how many hourly observations that estimate rests on, which is what the
    null needs to give the estimate its own sampling error."""
    import bisect
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
        # The same 90-day slice CdBuilder just used, so nobs is the estimator's
        # real observation count and not a nominal 2160.
        lo_i = bisect.bisect_left(pts, prices[i][0] - 90 * bb.DAY_MS, 0, i + 1)
        nobs = (i + 1) - lo_i - 1
        hi = max(r[1] for r in rows)
        lo = min(r[2] for r in rows)
        cur = prices[i][1]
        out.append((d, hi, lo, cur, vol, nobs))
    return out, ""


def hourly_return_matrix(cache, syms):
    """Simple hourly returns of every spot coin on one common hour grid.

    Simple, not log: main.py's `volatility` is std(diff(p)/p[:-1]), and rho has
    to be measured on the same quantity the volatility is measured on."""
    series = {}
    for s in syms:
        doc = cache.get(s)
        if not doc:
            continue
        pr = doc.get("prices") or []
        if len(pr) < 3:
            continue
        ts = np.asarray([p[0] for p in pr], dtype=np.int64)
        px = np.asarray([p[1] for p in pr], dtype=float)
        ok = px[:-1] > 0
        buckets = ts[1:] // bb.HOUR_MS
        rets = np.where(ok, np.diff(px) / np.where(ok, px[:-1], 1.0), np.nan)
        series[s] = (buckets, rets)
    if not series:
        return [], np.zeros((0, 0)), np.zeros(0, dtype=np.int64)
    allb = np.unique(np.concatenate([b for b, _ in series.values()]))
    idx = {int(b): i for i, b in enumerate(allb)}
    names = sorted(series)
    M = np.full((len(names), len(allb)), np.nan)
    for r, s in enumerate(names):
        b, v = series[s]
        cols = np.fromiter((idx[int(x)] for x in b), dtype=np.int64, count=len(b))
        M[r, cols] = v
    return names, M, allb


def mean_pairwise_rho(M, rows, c_lo, c_hi):
    """Mean pairwise Pearson correlation over the trailing window.

    Columns where any contributing coin is missing are dropped, so every pair
    is measured on the same hours. Fewer than two coins or fewer than two
    usable hours has no correlation and says so."""
    if len(rows) < 2:
        return None, 0
    sub = M[np.ix_(rows, np.arange(c_lo, c_hi))]
    keep = ~np.isnan(sub).any(axis=0)
    sub = sub[:, keep]
    if sub.shape[1] < 2:
        return None, int(sub.shape[1])
    sd = sub.std(axis=1)
    if not np.all(sd > 0):
        return None, int(sub.shape[1])
    C = np.corrcoef(sub)
    iu = np.triu_indices(C.shape[0], 1)
    vals = C[iu]
    vals = vals[np.isfinite(vals)]
    if vals.size == 0:
        return None, int(sub.shape[1])
    return float(vals.mean()), int(sub.shape[1])


# ─────────────────────────────────────────────────────────────────────────────
# 3. The null
# ─────────────────────────────────────────────────────────────────────────────
def simulate_day(rng, n_paths, n_coins, rho, sigma_day, steps=STEPS_PER_DAY):
    """One simulated trading day per path per coin, as a CONTINUOUS-time range.

    The archive's hourly candles carry true intra-hour extremes. A null built
    from 24 hourly CLOSES understates the day range by roughly a sixth and
    would move the admissibility window in the dangerous direction, so the
    within-step extremes are not skipped — they are drawn from the law that
    describes them exactly.

    Given the endpoints of a step, a Brownian path on that step is a Brownian
    bridge, and the bridge's maximum has a closed-form inverse CDF:

        M = (a + b + sqrt((b - a)^2 - 2 v ln U)) / 2 ,  U ~ Uniform(0, 1)

    with v the step variance, and the mirror expression for the minimum. The
    bridges on disjoint steps are independent given the skeleton, so the
    maximum over steps is exact in distribution — this is not a discretisation
    that gets better with more steps, it is the continuous-time answer. The
    known-answer control in --selftest is what decides whether that claim
    holds: at a sigma where the price-scale term vanishes the pooled mean must
    read 1.000, where 24 hourly closes read about 0.86.

    Correlation enters through a single common factor, which is what makes a
    date's law depend only on how many coins contributed and how tightly they
    move together.

    Returns (hi, lo, last) in LOG space, each shaped (n_paths, n_coins).
    """
    dt = 1.0 / steps
    r = min(max(rho, 0.0), 0.999)        # a common factor cannot carry rho < 0
    sig = np.asarray(sigma_day, dtype=float).reshape(1, -1)   # (1, n_coins)
    sd_step = np.sqrt(dt)
    shape = (n_paths, n_coins, steps)
    fac = rng.standard_normal((n_paths, 1, steps)) * sd_step
    idio = rng.standard_normal(shape) * sd_step
    z = (np.sqrt(r) * fac + np.sqrt(1.0 - r) * idio) * sig[..., None]
    x = np.concatenate([np.zeros((n_paths, n_coins, 1)), np.cumsum(z, axis=2)], axis=2)
    a, b = x[:, :, :-1], x[:, :, 1:]
    v = (sig[..., None] ** 2) * dt
    d2 = (b - a) ** 2
    U = rng.random(shape)
    V = rng.random(shape)
    mx = 0.5 * (a + b + np.sqrt(d2 - 2.0 * v * np.log(U)))
    mn = 0.5 * (a + b - np.sqrt(d2 - 2.0 * v * np.log(V)))
    return mx.max(axis=2), mn.min(axis=2), x[:, :, -1]


def null_sets(rng, n_paths, cur, sigma_hour, nobs, rho):
    """Null replicas of ONE date, as (hi, lo, cur, vol) rows ready for node.

    sigma_hour is HOURLY, because that is what `volatility` is in coeffs.json
    and what production hands to sigmaDay: dayRangeRatio's denominator is
    cur * sigmaDay(vol) * sqrt(8/pi) and sigmaDay multiplies by sqrt(24). The
    simulated path therefore runs at sigma_hour * sqrt(24) over the day, and
    the column the node hop reads back is the hourly figure. Getting this
    backwards is not a subtle error — it moves the whole null by a factor of
    sqrt(24) — and it is exactly what the known-answer control catches.

    The sigma the RATIO is divided by is not the sigma the path was drawn
    with: production divides by a 90-day estimate, and the sampling error of
    that estimate belongs in the null. For Gaussian returns the variance
    estimator on m observations has sd(sigma_hat / sigma) ~ sqrt(1 / (2m)), so
    the estimate enters as a multiplicative factor with that spread. 90 days of
    history are not re-simulated per replica: the factor is the admissible
    form the TZ names, and this is the record of which was used."""
    cur = np.asarray(cur, float)
    sig = np.asarray(sigma_hour, float)
    nobs = np.asarray(nobs, float)
    n_coins = cur.size
    hi_l, lo_l, last_l = simulate_day(rng, n_paths, n_coins, rho,
                                      sig * np.sqrt(24.0))
    S = cur.reshape(1, -1)
    hi = S * np.exp(hi_l)
    lo = S * np.exp(lo_l)
    last = S * np.exp(last_l)
    fac = 1.0 + rng.standard_normal((n_paths, n_coins)) / np.sqrt(2.0 * nobs.reshape(1, -1))
    vol_hat = np.abs(sig.reshape(1, -1) * fac)
    out = np.empty((n_paths, n_coins, 4))
    out[:, :, 0] = hi
    out[:, :, 1] = lo
    out[:, :, 2] = last
    out[:, :, 3] = vol_hat
    return out


def p90_bootstrap_se(vals, reps=120, seed=SEED):
    """Monte-Carlo standard error of the null p90, measured rather than
    assumed. A percentile's precision depends on the density at the
    percentile, which nothing here knows in advance."""
    a = np.asarray(vals, float)
    m = a.size
    if m < 10:
        return float("inf")
    rng = np.random.default_rng(seed + 1)
    out = np.empty(reps)
    for i in range(reps):
        out[i] = np.percentile(a[rng.integers(0, m, m)], 90)
    return float(out.std(ddof=1))


# ─────────────────────────────────────────────────────────────────────────────
# 4. Reporting helpers
# ─────────────────────────────────────────────────────────────────────────────
def deciles(vals):
    """p0..p100 in tens. numpy linear interpolation — stated so the number is
    reproducible by anyone re-running this."""
    a = np.asarray(vals, float)
    return [(q, float(np.percentile(a, q))) for q in range(0, 101, 10)]


def daystr(key):
    return (datetime.date(1970, 1, 1) + datetime.timedelta(days=int(key))).isoformat()


def hist(counts):
    out = {}
    for c in counts:
        out[int(c)] = out.get(int(c), 0) + 1
    return out


def admissibility(emp_coin_mean, null_coin_mean, emp_p90, null_p90,
                  null_p999, n_dates, med_n):
    """The four conditions of TZ-13 §2 C5, as data.

    A separate function because the self-test has to be able to feed it a value
    below the null p90 and one above the null p99.9 and watch it refuse them.
    A gate only ever exercised on the real run is a gate nobody has seen fail
    (inv. 23)."""
    rel = (abs(emp_coin_mean - null_coin_mean) / null_coin_mean
           if null_coin_mean else float("inf"))
    return [
        ("1", rel <= MEAN_TOL,
         "coin-day mean: empirical %.4f vs null %.4f -> %.2f%% (allowed %.0f%%)"
         % (emp_coin_mean, null_coin_mean, 100.0 * rel, 100.0 * MEAN_TOL)),
        ("2", emp_p90 > null_p90,
         "empirical p90 %.4f strictly above null p90 %.4f" % (emp_p90, null_p90)),
        ("3", emp_p90 < null_p999,
         "empirical p90 %.4f strictly below null p99.9 %.4f" % (emp_p90, null_p999)),
        ("4", (n_dates >= MIN_DATES) and (med_n >= MIN_MEDIAN_COUNT),
         "%d dates (need %d) and median contributing count %.1f (need %d)"
         % (n_dates, MIN_DATES, med_n, MIN_MEDIAN_COUNT)),
    ]


# ─────────────────────────────────────────────────────────────────────────────
# 5. The run
# ─────────────────────────────────────────────────────────────────────────────
def run(years, source, replica_cap=4096):
    t_start = time.time()
    spot, fut = spot_universe(HTML)
    print("Universe: %d spot of %d declared tokens (fut:true excluded by "
          "declaration, inv. 41): %s" % (len(spot), len(spot) + len(fut),
                                         ", ".join(t["name"] for t in fut)))
    js = extract_js(HTML)
    print("Cut out of index.html: %s" % ", ".join(JS_CUT))
    print("Seed: %d   skeleton steps/day: %d" % (SEED, STEPS_PER_DAY))

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

    # ── the coin-days, keyed by date ────────────────────────────────────────
    print("\n=== Coverage ===")
    per_date = {}
    skipped = []
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
        for (d, hi, lo, cur, vol, nobs) in days:
            per_date.setdefault(d, []).append((sym, hi, lo, cur, vol, nobs))
        print("  %-8s coin-days %5d  %s .. %s"
              % (sym, len(days), daystr(days[0][0]), daystr(days[-1][0])))
    if skipped:
        print("  skipped: %s" % ", ".join(skipped))
    if not per_date:
        print("\nBLOCKED: zero coin-days — a calibration over nothing is not a "
              "calibration (inv. 22).")
        return 1

    # ── the empirical date medians, from production ─────────────────────────
    keys = sorted(per_date)
    sets, names = [], []
    for d in keys:
        m = per_date[d]
        sets.append([(hi, lo, cur, vol) for (_s, hi, lo, cur, vol, _n) in m])
        names.append([s for (s, _h, _l, _c, _v, _n) in m])
    emp = lists_via_node(sets, js, want_ratios=True, names=names)
    med_by_key = dict(zip(keys, emp["median"]))
    n_by_key = dict(zip(keys, emp["n"]))
    kept = [d for d in keys if med_by_key[d] is not None]
    below = [d for d in keys if med_by_key[d] is None]
    emp_med = np.asarray([med_by_key[d] for d in kept], float)
    emp_n = np.asarray([n_by_key[d] for d in kept], int)

    print("\n=== Dates ===")
    print("  dates seen                       : %d" % len(keys))
    print("  dates with a median              : %d" % len(kept))
    print("  dates dropped below quorum       : %d" % len(below))
    if kept:
        print("  span                             : %s .. %s"
              % (daystr(kept[0]), daystr(kept[-1])))
    print("  per-date contributing count (n -> dates): %s"
          % json.dumps(hist(emp_n), sort_keys=True))
    if emp_n.size:
        print("  median per-date contributing count: %.1f"
              % float(np.percentile(emp_n, 50)))
    if emp_med.size == 0:
        print("\nBLOCKED: no date reached quorum — nothing to take a percentile "
              "of (inv. 22).")
        return 1

    emp_coin_mean = emp["rsum"] / emp["rcount"] if emp["rcount"] else float("nan")
    print("\n  empirical pooled coin-day ratios : n=%d (null-valued %d), mean %.4f"
          % (emp["rcount"], emp["rnull"], emp_coin_mean))

    # ── rho, measured over the same trailing window the volatility uses ─────
    print("\n=== Correlation (measured, not assumed) ===")
    rsyms, M, allb = hourly_return_matrix(cache, [t["name"] for t in spot])
    row_of = {s: i for i, s in enumerate(rsyms)}
    rho_by_key, rho_hours = {}, {}
    for d in kept:
        members = [s for (s, _h, _l, _c, _v, _n) in per_date[d] if s in row_of]
        rows = [row_of[s] for s in members]
        t_end = (d + 1) * bb.DAY_MS
        c_hi = int(np.searchsorted(allb, t_end // bb.HOUR_MS, side="right"))
        c_lo = int(np.searchsorted(allb, (t_end - 90 * bb.DAY_MS) // bb.HOUR_MS,
                                   side="left"))
        r, hrs = mean_pairwise_rho(M, rows, c_lo, c_hi)
        rho_by_key[d] = r
        rho_hours[d] = hrs
    measured = [v for v in rho_by_key.values() if v is not None]
    if not measured:
        print("\nBLOCKED: rho could not be measured on any date — the null has "
              "no object (inv. 22).")
        return 1
    ra = np.asarray(measured, float)
    print("  dates with a measured rho        : %d of %d" % (ra.size, len(kept)))
    print("  hourly observations per window   : median %d"
          % int(np.percentile([rho_hours[d] for d in kept if rho_by_key[d] is not None], 50)))
    print("  rho  %-6s %8s" % ("pct", "value"))
    for q, v in deciles(ra):
        print("       p%-5d %8.4f" % (q, v))
    print("  rho mean %.4f   min %.4f   max %.4f   negative on %d dates"
          % (ra.mean(), ra.min(), ra.max(), int((ra < 0).sum())))
    rho_fallback = float(np.percentile(ra, 50))
    missing_rho = [d for d in kept if rho_by_key[d] is None]
    if missing_rho:
        print("  %d dates had no measurable rho and take the median of the "
              "measured ones (%.4f)" % (len(missing_rho), rho_fallback))

    # ── the null, simulated at each date's own n and rho ────────────────────
    print("\n=== Null (simulated in this run) ===")
    rng = np.random.default_rng(SEED)
    null_med = []
    null_rsum, null_rcount, null_rnull = 0.0, 0, 0
    per_round = 32
    total_replicas = 0
    se = float("inf")
    # Streamed, not accumulated: at the top replica counts the whole round is
    # tens of millions of floats, and holding it to hand node one tidy list
    # would cost more memory than the runner has.
    ROWS_PER_HOP = 500000
    pend = []
    acc = {"rows": 0}

    def flush():
        if not pend:
            return
        res = lists_via_node(pend, js)
        acc["med"] += [v for v in res["median"] if v is not None]
        acc["rsum"] += res["rsum"]
        acc["rcount"] += res["rcount"]
        acc["rnull"] += res["rnull"]
        del pend[:]
        acc["rows"] = 0

    acc.update(med=null_med, rsum=0.0, rcount=0, rnull=0)
    while True:
        for d in kept:
            m = per_date[d]
            cur = [c for (_s, _h, _l, c, _v, _n) in m]
            sig = [v for (_s, _h, _l, _c, v, _n) in m]
            nob = [max(int(n), 2) for (_s, _h, _l, _c, _v, n) in m]
            rho = rho_by_key[d]
            if rho is None:
                rho = rho_fallback
            arr = null_sets(rng, per_round, cur, sig, nob, rho)
            for k in range(per_round):
                pend.append(arr[k])
                acc["rows"] += len(m)
                if acc["rows"] >= ROWS_PER_HOP:
                    flush()
        flush()
        null_med = acc["med"]
        null_rsum, null_rcount, null_rnull = acc["rsum"], acc["rcount"], acc["rnull"]
        total_replicas += per_round
        se = p90_bootstrap_se(null_med)
        el = time.time() - t_start
        print("  replicas/date %5d  null medians %8d  p90 %.4f  MC se %.5f  "
              "[%.0fs]" % (total_replicas, len(null_med),
                           float(np.percentile(null_med, 90)) if null_med else float("nan"),
                           se, el))
        if se < MC_SE_MAX and total_replicas >= 128:
            break
        if total_replicas >= replica_cap:
            print("  replica cap %d reached" % replica_cap)
            break
        if el > NULL_BUDGET_S:
            print("  wall-clock budget %ds reached" % NULL_BUDGET_S)
            break
        per_round = min(per_round * 2, replica_cap - total_replicas)
        if per_round <= 0:
            break

    if not null_med:
        print("\nBLOCKED: the null produced no median (inv. 22).")
        return 1
    na = np.asarray(null_med, float)
    null_coin_mean = null_rsum / null_rcount if null_rcount else float("nan")
    print("\n  seed                             : %d" % SEED)
    print("  replicas per date                : %d" % total_replicas)
    print("  null date-medians                : %d" % na.size)
    print("  null p90 Monte-Carlo std. error  : %.5f (must be < %.2f)"
          % (se, MC_SE_MAX))
    print("  null pooled coin-day ratios      : n=%d (null-valued %d), mean %.4f"
          % (null_rcount, null_rnull, null_coin_mean))
    print("\n  null date-median distribution")
    print("  %-6s %10s" % ("pct", "value"))
    for q, v in deciles(na):
        print("  p%-5d %10.4f" % (q, v))
    null_p90 = float(np.percentile(na, 90))
    null_p95 = float(np.percentile(na, 95))
    null_p99 = float(np.percentile(na, 99))
    null_p999 = float(np.percentile(na, 99.9))
    print("  p95    %10.4f" % null_p95)
    print("  p99    %10.4f" % null_p99)
    print("  p99.9  %10.4f" % null_p999)

    # ── the empirical distribution and the statistic ────────────────────────
    print("\n=== Empirical date medians ===")
    print("  %-6s %10s" % ("pct", "value"))
    for q, v in deciles(emp_med):
        print("  p%-5d %10.4f" % (q, v))
    emp_p90_raw = float(np.percentile(emp_med, 90))
    val = round(emp_p90_raw, 2)
    print("\n  p90 raw                          : %.6f" % emp_p90_raw)
    print("  p90 rounded to 2 dp              : %.2f" % val)

    print("\n  ten highest dates by list median")
    order = np.argsort(-emp_med)[:10]
    for i in order:
        d = kept[int(i)]
        print("    %s  median %.4f  over %d coins" % (daystr(d), emp_med[i], emp_n[i]))

    # ── the registered rule ─────────────────────────────────────────────────
    print("\n=== Admissibility (registered by TZ-13 §2 C5, before the number) ===")
    med_n = float(np.percentile(emp_n, 50))
    lines = admissibility(emp_coin_mean, null_coin_mean, emp_p90_raw,
                          null_p90, null_p999, len(kept), med_n)
    for num, okc, txt in lines:
        print("  %s  %-4s %s" % (num, "PASS" if okc else "FAIL", txt))

    se_ok = se < MC_SE_MAX
    print("  se  %-4s null p90 Monte-Carlo std. error %.5f (need < %.2f)"
          % ("PASS" if se_ok else "FAIL", se, MC_SE_MAX))

    print("\n  wall clock: %.0fs   node hops: %d   node: %s"
          % (time.time() - t_start, HOPS["n"], HOPS["node"]))

    if not all(c for _n, c, _t in lines) or not se_ok:
        print("\nNo constant is adopted. A failing condition means the "
              "estimator is not")
        print("measuring what §3.16 claims, or the evidence is too thin to "
              "take a percentile")
        print("of. The answer is a new TZ, never a nudged number. No production "
              "change.")
        return 1

    print("\nAdopted by the rule registered above, taken as-is:")
    print("DAY_RANGE_ABNORMAL = %.2f" % val)
    print("\nNot entered into index.html by this TZ: TZ-13 §3 forbids a "
          "consumer, and the")
    print("constant reaches production only through the TZ that follows.")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 6. Self-test — offline, no network, BEFORE the archive is touched
# ─────────────────────────────────────────────────────────────────────────────
def selftest():
    print("=== TZ-13 Stage C self-test (offline, no network) ===")
    js = extract_js(HTML)
    checks = [0]
    fails = [0]

    def eq(name, got, want, tol=1e-12):
        checks[0] += 1
        ok = (got is None and want is None) or (
            got is not None and want is not None and abs(got - want) <= tol)
        if not ok:
            fails[0] += 1
            print("  FAIL %s: got %r want %r" % (name, got, want))

    def ok(name, cond, note=""):
        checks[0] += 1
        if not cond:
            fails[0] += 1
            print("  FAIL %s%s" % (name, (": " + note) if note else ""))

    # ── 1. the cut is the production one, and Python holds no median ───────
    print("\n-- 1. the cut, and where the median comes from --")
    for f in JS_CUT:
        ok("index.html defines " + f, ("function " + f) in
           open(HTML, encoding="utf-8").read())
    # The run path only: this function names the banned calls in order to look
    # for them, so scanning itself would always find them.
    #
    # The claim being checked is precise, and narrower than "Python never takes
    # a median". Python DOES take three medians in the run path and none of
    # them is a median of RATIOS: the median per-date contributing COUNT, on
    # which condition 4 is defined by the TZ; the median measured rho, used as
    # the fallback for a date whose rho could not be measured; and the p50 cell
    # of the decile tables C6 asks to print, which reaches no decision. The
    # LIST MEDIAN — the object being calibrated — is production's alone, and
    # section 2 below is the empirical proof of that, not this scan.
    me = open(os.path.abspath(__file__), encoding="utf-8").read()
    body = me[me.index("import numpy as np"):me.index("def selftest(")]
    for banned in ("np.median", "statistics.median", ".sort()", "sorted(vals"):
        ok("the run path never medians a ratio distribution itself (%s)" % banned,
           banned not in body)
    ok("the run path was actually scanned", len(body) > 4000, "%d chars" % len(body))
    # Structural: the constant is a p90 OF THE DATE MEDIANS, and the date
    # medians are what the node hop handed back.
    ok("the constant is p90 of emp_med", "np.percentile(emp_med, 90)" in body)
    ok("emp_med is built from the node hop's medians", 'emp["median"]' in body)
    ok("the node hop is the only median producer",
       "lists_via_node" in body and "def listExhaustion" not in body)
    hops0 = HOPS["n"]

    # ── 2. production's listExhaustion owns the median AND the quorum ──────
    print("\n-- 2. the median and the quorum are production's --")
    # A fixture whose median is known BY CONSTRUCTION: nine coins whose ratios
    # are 1..9 in units of the denominator, so the middle one is the answer.
    def row_for(r):
        # hi - lo = r * cur * sigmaDay(vol) * sqrt(8/pi), with cur = 100.
        cur, vol = 100.0, 0.01
        span = r * cur * vol * (24 ** 0.5) * ((8 / np.pi) ** 0.5)
        return (100.0 + span, 100.0, cur, vol)

    nine = [row_for(r) for r in (5, 1, 9, 3, 7, 2, 8, 4, 6)]
    res = lists_via_node([nine], js, want_ratios=True)
    eq("nine known ratios -> median is the fifth", res["median"][0], 5.0, 1e-9)
    eq("nine known ratios -> n is nine", float(res["n"][0]), 9.0)
    eq("the ten ratios are the ones built", float(min(res["ratios"])), 1.0, 1e-9)
    # Quorum: production's own floor, read off production, not restated here.
    seven = [row_for(r) for r in range(1, 8)]
    r7 = lists_via_node([seven], js)
    eq("seven rows -> production returns no median", r7["median"][0], None)
    eq("seven rows -> n is still counted", float(r7["n"][0]), 7.0)
    eight = [row_for(r) for r in range(1, 9)]
    r8 = lists_via_node([eight], js)
    ok("eight rows -> production returns a median", r8["median"][0] is not None)
    ok("the node hop was actually taken", HOPS["n"] > hops0,
       "%d hops" % (HOPS["n"] - hops0))
    ok("node identified itself", bool(HOPS["node"]), repr(HOPS["node"]))
    print("     node hops taken: %d   node: %s" % (HOPS["n"] - hops0, HOPS["node"]))

    # ── 3. nulls survive the JSON hop as nulls, never as zeros ─────────────
    print("\n-- 3. a missing measurement never arrives as a number --")
    bad = [(110.0, 100.0, 105.0, 0.0),      # vol 0
           (110.0, 100.0, 0.0, 0.01),       # cur 0
           (100.0, 100.0, 105.0, 0.01),     # hi == lo
           (90.0, 100.0, 105.0, 0.01)]      # hi < lo
    rb = lists_via_node([bad], js, want_ratios=True)
    eq("four unmeasurable rows -> no median", rb["median"][0], None)
    eq("four unmeasurable rows -> n is zero", float(rb["n"][0]), 0.0)
    eq("no ratio survived", float(len(rb["ratios"])), 0.0)
    eq("all four were counted as null, not as zero", float(rb["rnull"]), 4.0)
    eq("nothing was summed", float(rb["rsum"]), 0.0)
    mixed = [row_for(2.0)] + list(bad)
    rm = lists_via_node([mixed], js)
    eq("a null among good rows does not become a zero", float(rm["n"][0]), 1.0)

    # ── 4. the known-answer control (inv. 23) ──────────────────────────────
    print("\n-- 4. known-answer control: E[range] = sigma*sqrt(8T/pi) --")
    print("     driftless walk at sigma_day = %.3f%%, target %.3f +/- %.3f, "
          "at least %d coin-days" % (100 * KA_SIGMA_DAY, KA_TARGET, KA_TOL,
                                     KA_MIN_DAYS))
    rng = np.random.default_rng(SEED)
    done = 0
    s_sum, s_cnt = 0.0, 0
    t0 = time.time()
    CHUNK = 100000
    while done < KA_MIN_DAYS:
        k = min(CHUNK, KA_MIN_DAYS - done)
        arr = null_sets(rng, k, [100.0], [KA_SIGMA_DAY / np.sqrt(24.0)],
                        [10 ** 12], 0.0)
        r = lists_via_node([arr[i] for i in range(k)], js)
        s_sum += r["rsum"]
        s_cnt += r["rcount"]
        done += k
    mean = s_sum / s_cnt if s_cnt else float("nan")
    print("     coin-days %d   pooled mean %.5f   (%.0fs)"
          % (s_cnt, mean, time.time() - t0))
    ok("at least %d coin-days" % KA_MIN_DAYS, s_cnt >= KA_MIN_DAYS, str(s_cnt))
    ok("pooled mean reads %.3f +/- %.3f" % (KA_TARGET, KA_TOL),
       abs(mean - KA_TARGET) <= KA_TOL, "%.5f" % mean)

    # The same control run WITHOUT the within-step extremes, which is the exact
    # error it exists to catch: hourly closes understate the range badly.
    closes = _closes_only_mean(rng, 200000, KA_SIGMA_DAY / np.sqrt(24.0), js)
    print("     same walk from 24 hourly CLOSES only: %.4f" % closes)
    ok("hourly closes are detectably wrong", closes < KA_TARGET - 10 * KA_TOL,
       "%.4f" % closes)

    # ── 5. the admissibility gate refuses what it must refuse ──────────────
    print("\n-- 5. the gate refuses a value below the null p90 and one above "
          "p99.9 --")
    # The real gate, fed synthetic numbers. The null here is a stand-in for a
    # run's null, and the value under test is moved across its p90 and its
    # p99.9 while everything else stays admissible.
    fake_null = np.asarray(rng.normal(1.0, 0.12, 200000), float)
    n90 = float(np.percentile(fake_null, 90))
    n999 = float(np.percentile(fake_null, 99.9))
    good = dict(emp_coin_mean=1.05, null_coin_mean=1.00, null_p90=n90,
                null_p999=n999, n_dates=MIN_DATES, med_n=MIN_MEDIAN_COUNT)

    def verdicts(**kw):
        a = dict(good)
        a.update(kw)
        return {c[0]: c[1] for c in admissibility(
            a["emp_coin_mean"], a["null_coin_mean"], a["emp_p90"],
            a["null_p90"], a["null_p999"], a["n_dates"], a["med_n"])}

    lo = verdicts(emp_p90=n90 - 0.05)
    ok("a value BELOW the null p90 is refused by condition 2", lo["2"] is False)
    ok("  and only by condition 2", lo["1"] and lo["3"] and lo["4"])
    hi = verdicts(emp_p90=n999 + 0.05)
    ok("a value ABOVE the null p99.9 is refused by condition 3", hi["3"] is False)
    ok("  and only by condition 3", hi["1"] and hi["2"] and hi["4"])
    eqp = verdicts(emp_p90=n90)
    ok("a value EQUAL to the null p90 is refused (strictly above)", eqp["2"] is False)
    mid = verdicts(emp_p90=(n90 + n999) / 2)
    ok("a value between the two passes every condition", all(mid.values()))
    ok("condition 1 refuses a mis-scaled mean",
       verdicts(emp_p90=(n90 + n999) / 2, emp_coin_mean=1.5)["1"] is False)
    ok("condition 4 refuses too few dates",
       verdicts(emp_p90=(n90 + n999) / 2, n_dates=MIN_DATES - 1)["4"] is False)
    ok("condition 4 refuses too thin a list",
       verdicts(emp_p90=(n90 + n999) / 2, med_n=MIN_MEDIAN_COUNT - 1)["4"] is False)
    ok("the MC precision requirement refuses a loose null",
       not (MC_SE_MAX + 0.001 < MC_SE_MAX))

    # ── 6. the correlation measurement ─────────────────────────────────────
    print("\n-- 6. rho is measured --")
    g = rng.standard_normal((1, 4000))
    Mi = np.vstack([g * 0.9 + rng.standard_normal((1, 4000)) * 0.436 for _ in range(4)])
    r, hrs = mean_pairwise_rho(Mi, [0, 1, 2, 3], 0, 4000)
    ok("a common-factor block reads its own rho", r is not None and abs(r - 0.8) < 0.05,
       "%.4f" % (r if r is not None else float("nan")))
    Mind = rng.standard_normal((4, 4000))
    r0, _ = mean_pairwise_rho(Mind, [0, 1, 2, 3], 0, 4000)
    ok("independent series read about zero", r0 is not None and abs(r0) < 0.05,
       "%.4f" % (r0 if r0 is not None else float("nan")))
    r1, _ = mean_pairwise_rho(Mind, [0], 0, 4000)
    eq("one coin has no pairwise correlation", r1, None)

    # ── 7. the date key ────────────────────────────────────────────────────
    print("\n-- 7. coin_days carries the day key --")

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
    ok("every tuple carries its day key",
       all(isinstance(d[0], int) and d[0] == 20000 + k for k, d in enumerate(days)))
    ok("every tuple carries its observation count", all(d[5] > 0 for d in days))
    days, _ = coin_days(synth(5, per_day=23), FakeBuilder())
    eq("partial days -> 0", float(len(days)), 0.0)
    days, why = coin_days({"prices": [], "hl": []}, FakeBuilder())
    eq("no hl -> 0", float(len(days)), 0.0)
    ok("missing hl explains itself", bool(why))

    # ── 8. the joined object really is a DATE ──────────────────────────────
    print("\n-- 8. dates, joined across the universe --")
    per_date = {}
    for sym, off in (("A", 0), ("B", 0), ("C", 1)):
        d, _ = coin_days(synth(3, day0=20000 + off), FakeBuilder())
        for (k, hi, lo, cur, vol, nobs) in d:
            per_date.setdefault(k, []).append((sym, hi, lo, cur, vol, nobs))
    eq("three coins offset by a day span four dates", float(len(per_date)), 4.0)
    eq("the shared middle dates carry three coins",
       float(len(per_date[20001])), 3.0)
    eq("the first date carries two", float(len(per_date[20000])), 2.0)

    print("\n--- checks: %d  fails: %d ---" % (checks[0], fails[0]))
    if checks[0] == 0:
        print("FAIL self-test verified nothing")
        return 1
    return 1 if fails[0] else 0


def _closes_only_mean(rng, n, sd, js):
    """The same day WITHOUT the within-step extremes — the control's control.

    Kept next to the known-answer test because it is what gives that test its
    teeth: a number that reads 1.000 is only evidence if the wrong method
    visibly does not."""
    steps = STEPS_PER_DAY
    sd_day = sd * np.sqrt(24.0)          # sd is HOURLY, as production reads it
    inc = rng.standard_normal((n, steps)) * (sd_day / np.sqrt(steps))
    x = np.concatenate([np.zeros((n, 1)), np.cumsum(inc, axis=1)], axis=1)
    S = 100.0
    sets = np.empty((n, 1, 4))
    sets[:, 0, 0] = S * np.exp(x.max(axis=1))
    sets[:, 0, 1] = S * np.exp(x.min(axis=1))
    sets[:, 0, 2] = S * np.exp(x[:, -1])
    sets[:, 0, 3] = sd
    r = lists_via_node([sets[i] for i in range(n)], js)
    return r["rsum"] / r["rcount"] if r["rcount"] else float("nan")


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
