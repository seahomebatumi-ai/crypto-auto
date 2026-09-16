# Implementation Report — TZ-47

**The previous TZ was report-only, so no branch of it could be unmerged.** TZ-46 wrote only
its report, `7683f89` on `main`. The last branch TZ, TZ-44, is merged: pull request #39, merge
commit `baec7c9` with parents `ca64541` and `99e4b0a`. Since `7683f89`, `main` carries
`80ed81f` (contract v23), `68bc49b` (methodology `2026-09-16-c`), `84d53cf` (map
`2026-09-16-b`) and `9e30a6e` (this TZ's upload, one file). TZ-47 has no sequencing clause.

## Status

**BLOCKED.**

The fingerprint gate passed: 7 of the table's 7 anchors matched and every file figure matched.
No implementation was started. The run stopped at the TZ's own §2 interface check. A synthetic
probe then showed that §6 item 1 registers known answers that correct code cannot produce. The
probe executed production's cut `marketRegime` on rows cut from `main.py`. **Either ground
blocks the run on its own.**

### Ground 1 — §2 interface check, line 5, fails as written

§2 says: «Before any work, confirm against the repository, and **report BLOCKED naming the
miss** if any line fails». Line 5 reads:

> 5. `marketRegime` is already inside a bundle this bench cuts and executes, and `--regimes`
>    already calls it on BTC's row.

**The miss: `--regimes` does not call `marketRegime`.** `main()` routes `--regimes` to
`run_regimes`. That function builds `JsScorer`, which is the `JS_FUNCS` bundle: `has`,
`clamp01`, `sigmaDay`, `volRegime`, `qualityScore`, `scoreFinish` and `scoreCandidate`, with
no `marketRegime`. It labels dates with `btc_regimes`, a Python drift t-statistic on 90 daily
BTC closes that does not read the production word. The bundle `--regimes` executes was built
and searched: it contains `marketRegime` zero times (Validation, V-2).

**What holds.** Lines 1–4 hold, and so does the first clause of line 5. `marketRegime` is in
`TARGET_JS_FUNCS` (`bench/backtest_bench.py:3221`). `TARGET_DRIVER` calls
`marketRegime(j.btcStats)` on BTC's full row (`:3325`), and `run_target` executes that driver.
`--target` and `--regime-gate` both run `run_target`; `--regime-gate` goes through
`run_regime_grid`. So the line's intent, that the bench already cuts and executes the word on
BTC's row, holds through `--target` and `--regime-gate`. The line's literal claim, that
`--regimes` does it, does not hold. §2 leaves no discretion here, and the run does not decide
which mode the line meant (contract §12).

### Ground 2 — §6 item 1 registers known answers correct code cannot produce

The probe drove production's cut `marketRegime` with the bench's own `CdBuilder`, on the date
grid `walk_grid` produces at `H_NOISE`'s 7 days. It ran 12 coins over 8760 h, 39 dates per
seed and 10 seeds per world (V-3). Results:

| World | TZ §6 item 1 requires | Measured (10 seeds, 4680 coin-dates each) |
|---|---|---|
| **2 — driftless walk, equal volatility** (σ = 0.01/h) | `overlap` near 0.5; the two cells' `m` distributions overlap heavily | **`overlap` 0.000 on 10 of 10 seeds.** range 2069, trend 2385, stress 226. The largest `m` in `R` stays below the median `m` of `T` on every seed. On 3 of 10 seeds it is below even the smallest `m` of `T`. |
| **3 — volatile climb, literal** (drift 0.0003/h, σ scaled to 0.015/h) | every coin-date `range`; `overlap` near 1 | range **1869** (39.9 %), trend 2426, stress 385; **`overlap` 0.000** on 10 of 10 |
| 3 — the same drift with zig-zag noise (amplitude 0.007/h), the only construction found that classes every coin-date `range` | (as above) | range **4680 of 4680**, `T` empty, **`overlap` undefined** |
| 3 — a mixed world: half the coins a staircase climb (world 1), half zig-zag climbs | (not a world the TZ names) | range 2340, trend 2340; **`overlap` 1.000 on 10 of 10** |

**Why world 2 cannot read 0.5.** `marketRegime` computes
`eff = r14 / (volatility · √(2·H_NOISE))`, and Claim A sets `m = |r14|`, the same numerator.
Where every coin-date has the same `volatility`, the word is a threshold on `m` itself:
`trend` is `m ≥ EFF_TREND · volatility · √(2·H_NOISE)`, and `range` is everything below that
cut. So every `R` coin-date lies below every `T` coin-date and `overlap` is 0. The only thing
that lets the two cells cross is the spread of the 90-day volatility estimate. Here it was
measured at a CV of 1.33–1.50 %, and it does not move `R` up to `T`'s median: the largest `R`
value was 0.109–0.114 against a `T` median of 0.188–0.191 (V-4). This is arithmetic on the
production formula, not a property of the seeds.

**This reaches Claim A itself and not only the control.** Claim A's heading is «The word is or
is not a statement about direction». Its reading maps `overlap ≤ 0.10` to «the methodology
stands as written». World 2 is the world the TZ itself describes as one where «the word
carries no information about direction by construction», and it reads 0.000, inside that
outcome. With volatility 4× apart across coins (0.004 / 0.008 / 0.016 per hour,
`walk_hetvol`), it reads a mean of **0.031** with a maximum of 0.079 on 10 seeds, still inside
it. **`overlap` is governed by how much volatility varies across the coin-dates compared, and
a world with no directional content lands in the outcome that upholds the methodology.**
There are two ways to repair this, and each changes the registered claim or its fixtures:

- (a) world 2's registered answer is wrong, and the claim stands as a statement about past
  move size;
- (b) the claim's heading and outcome text are wrong about what `overlap` measures.

Inv. 23 fixes both before data, so choosing between them is the Architect's call and not
the run's.

**Why world 3 as written cannot hold.** «Every coin-date must class `range`» leaves `T` empty.
`M_T`, the median of `m` over `T`, then does not exist, and `overlap` has no value. §6 requires
the mode to state exactly that for world 1's empty `R`. «`overlap` must read near 1» therefore
needs a `T` cell, and the only construction measured that gives 1.000 is the mixed world. The
TZ does not name a mixed world. The mixed world and a pure world need different fixtures and
different assertions, so this is a two-readings case (contract §12). Brownian noise alone
cannot satisfy «every coin-date `range`» at any parameter. Under a Brownian path `eff` is
approximately `N(μ, 1)`, so `P(|eff| < EFF_TREND)` is at most `P(|N(0,1)| < 0.6)` ≈ 45 %. That
is map §3.12's own «~55 % of pure-noise windows "trend"», read from the other side.

### Findings that do not block alone, recorded so the next TZ can state them

- **World 1, «smooth monotone climb — every coin-date must class `trend`».** A literally
  smooth climb classes **`stress` on 4680 of 4680** coin-dates. Its hourly-return volatility
  is floating-point residue (1.3e-16 to 5.7e-16), so `|z| = |r7| / (volatility·√H_NOISE)`
  reaches at least 2.5e13 against `REG_STRESS_Z` 2.0 (V-4). At a volatility of exactly 0,
  `marketRegime` returns `known: false` with `mode: 'range'`. A Brownian climb cannot be all
  `trend` either: at drift 0.0003/h and σ 0.004/h it read range 905, trend 2925 and stress 850,
  because `z` and `eff` share the drift in the ratio `1 : √2` and each carries unit noise. **A
  monotone STAIRCASE (a jump every 100 h, drift 0.0003/h) classes `trend` on 4680 of 4680**,
  with `R` empty. The assertion can be satisfied, but the word «smooth» describes the one
  construction that fails it.
- **Control 4 × control 5.** §6 item 4 asserts that the populations «MOVE» when `EFF_TREND` is
  perturbed. §6 item 5 requires control 4 to turn red when the trend comparison is inverted.
  **A movement-only assertion does not turn red under that inversion.** On world 2 with 10
  seeds, `EFF_TREND` 0.60 → 0.90 moved the populations from range/trend 2069/2385 to
  2894/1560 in production, and from 2385/2069 to 1560/2894 inverted: they move both times. The
  directional form, «raising `EFF_TREND` shrinks `trend`», reads True in production and False
  inverted (V-3). Item 5's partition holds only if item 4 is written directionally, and the
  TZ's text names the non-directional form.
- **Gate step 14's next section letter.** The `# X.` headers of
  `bench/backtest_guard_bench.py` read, in file order: A, B, C, D, E, E, F, G, H, I, J, K. That
  is 12 headers carrying 11 distinct letters, and the last is K. The letter was read from the
  headers, not counted; no section was written.

**What would unblock:** an amended TZ from the Architect that:

1. corrects §2 line 5 to the mode that actually executes the word;
2. re-registers world 2's answer, or Claim A's heading and outcome text, per the choice above;
3. states whether world 3 is a pure world with an empty `T` or a mixed world;
4. optionally names world 1's fixture and control 4's direction.

## Inbound Filing

None. The TZ arrived as `CryptoTZ/TZ-47-own-regime-direction-backtest.md` in `9e30a6e`,
matching its header's canonical filename. Nothing was moved or renamed.

## Scope Executed

**Class: branch TZ.** §3 names three files outside `CryptoReports/**`:
`bench/backtest_bench.py`, `bench/backtest_guard_bench.py` and
`.github/workflows/backtest_bench.yml`.

Executed:

- contract §4a steps 1–6;
- the §5 fingerprint gate, which passed;
- the TZ's §2 interface check, which failed on line 5 (Ground 1);
- the synthetic probe of §6 item 1's worlds and of the item 4 × item 5 partition (Ground 2);
- baseline readings of validation items 1–3 and of gate step 14.

Not executed: all of §3–§7. No file in scope was modified and no branch was opened.

## Files Created

- `CryptoReports/TZ-47-own-regime-direction-backtest-report.md`, this report and nothing else.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None in the repository. The run removed `bench/__pycache__/`, a generated artifact its own
`py_compile` created. It is ignored and was never tracked.

## Implementation Summary

None. The run was BLOCKED before implementation.

The probe was a measurement, not a prototype of the mode. It read the three production
constants through a cut bundle (`has`, `marketRegime`, `H_NOISE`, `VOL_HARD`, `REG_STRESS_Z`,
`EFF_TREND`). Its closure check read «сверено 17 обращений, 7 имён, пропущенных 0». Rows were
built by `CdBuilder` from `main.py`, and the date grid came from `walk_grid`. It used synthetic
series only, with no archive, no cache, no fetch and no dispatch. It ran on a copy of
`bench/backtest_bench.py` in `/tmp/tz47probe/`, MD5 `ba633202f43845ba0fdafbc1b92d9c04`,
identical to the repository file, so every bridge file the probe built was written outside the
worktree. The control-4 inversion was applied to a `/tmp` copy of `index.html`; the repository
file was never written. The probe's source is reproduced under V-5 so the reading can be
re-run (inv. 71).

**No claim of TZ-47 was measured on the archive**, and nothing in this report is an archive
figure (TZ validation item 11, inv. 44). The worlds are synthetic, so no registered claim was
exposed to data before its registration (inv. 23).

## Validation

**Gate (contract §5), commands and output:** see `## Fingerprints`.

**V-1. TZ validation items 1–3, run on the unmodified tree as a baseline:**

```
$ python3 -m py_compile bench/backtest_bench.py; echo "py_compile backtest_bench exit $?"
py_compile backtest_bench exit 0
$ python3 -m py_compile bench/backtest_guard_bench.py; echo "py_compile guard exit $?"
py_compile guard exit 0
$ git diff --stat; echo "diff --stat lines: $(git diff --stat | wc -l)"
diff --stat lines: 0
```

**Gate step 14 baseline at `9e30a6e`**, local and not a runner, with command as in `bench.yml`:

```
$ python3 bench/backtest_guard_bench.py
E. venue-as-observation: 32 comparisons
F. anchored production arm: 29 comparisons
G. D4 partition: 63 comparisons
H. transport: 107 comparisons
I. attribution: 95 comparisons
J. gap in UTC: 8 comparisons
K. comparability: 11 comparisons
checks run: 487   FAIL 0
step14 exit 0
```

This reproduces the map's `487` and every section count it records. The unprinted term is
`487 − (32+29+63+107+95+8+11) = 487 − 345 = 142`, the same as the map's. The output also
carried one numpy `RuntimeWarning: All-NaN slice encountered`, which is not a failure. Output
MD5 `6b19a1721a2787fcb8d3c83c604671ce`.

**V-2. Interface check (TZ §2), command and output** (`/tmp/tz47probe/check5.txt`, MD5
`8d28c4046dd65e60a2fe54747d6a328e`):

```
  замкнутость _score_bridge.js: сверено 45 обращений, 11 имён, пропущенных 0
--regimes bundle _score_bridge.js: 'marketRegime' occurrences = 0
run_regimes source references: JsScorer=True CdBuilder=True btc_regimes=True marketRegime=False TARGET_JS_FUNCS=False
run_walk source references marketRegime: False
btc_regimes source references marketRegime: False
'marketRegime' in TARGET_JS_FUNCS: True · in JS_FUNCS: False
run_target builds the TARGET bundle: True · TARGET_DRIVER calls marketRegime(j.btcStats): True
run_regime_grid calls run_target: True
CD_FIELDS carries volatility/r7/r14/eff14: True
target_summary reads RR_MIN at run time: True · RR_MIN in TARGET_JS_VARS: True
```

| Line | Result | Evidence |
|---|---|---|
| 1 | holds | `index.html:1864` `function marketRegime(btcStats)`. It reads `btcStats.volatility` (`:1866`), `.r7` (`:1869`) and `.r14` (`:1873`), and no other field. |
| 2 | holds | `:1882` `VOL_HARD`, `REG_STRESS_Z` → `'stress'`; `:1886` `EFF_TREND` → `'trend'` with `dir` set on that branch only; default `'range'` (`:1865`). |
| 3 | holds | `CD_FIELDS` carries all four fields, and the probe's `CdBuilder` built them on 37 440 synthetic coin-dates. |
| 4 | holds | `target_summary`: `"bar": 1.0 / _read_js_num(html, "RR_MIN")`; `RR_MIN` is in `TARGET_JS_VARS`. |
| 5 | **fails, second clause** | shown above |

**V-3. Worlds and the control-4 partition** (`/tmp/tz47probe/final.txt`, MD5
`9ee36f89fa97544fcac826c247301081`):

```
$ python3 probe.py $REPO ramp_smooth,ramp_stair,ramp_bm,walk,walk_hetvol,volclimb_bm,volclimb_zig,mixed 10
  замкнутость _tz47_probe.js: сверено 17 обращений, 7 имён, пропущенных 0
ramp_smooth   seeds 10 | n  4680 | range     0 trend     0 stress  4680 | dates/seed 39 | overlap per seed ['—', '—', '—', '—', '—', '—', '—', '—', '—', '—'] | mean undefined (a cell is empty) | seeds with maxR < minT 0/0
ramp_stair    seeds 10 | n  4680 | range     0 trend  4680 stress     0 | dates/seed 39 | overlap per seed ['—', '—', '—', '—', '—', '—', '—', '—', '—', '—'] | mean undefined (a cell is empty) | seeds with maxR < minT 0/0
ramp_bm       seeds 10 | n  4680 | range   905 trend  2925 stress   850 | dates/seed 39 | overlap per seed ['0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000'] | mean 0.000 | seeds with maxR < minT 9/10
walk          seeds 10 | n  4680 | range  2069 trend  2385 stress   226 | dates/seed 39 | overlap per seed ['0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000'] | mean 0.000 | seeds with maxR < minT 3/10
walk_hetvol   seeds 10 | n  4680 | range  2066 trend  2389 stress   225 | dates/seed 39 | overlap per seed ['0.046', '0.079', '0.029', '0.016', '0.000', '0.023', '0.046', '0.048', '0.004', '0.015'] | mean 0.031 | seeds with maxR < minT 0/10
volclimb_bm   seeds 10 | n  4680 | range  1869 trend  2426 stress   385 | dates/seed 39 | overlap per seed ['0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000', '0.000'] | mean 0.000 | seeds with maxR < minT 3/10
volclimb_zig  seeds 10 | n  4680 | range  4680 trend     0 stress     0 | dates/seed 39 | overlap per seed ['—', '—', '—', '—', '—', '—', '—', '—', '—', '—'] | mean undefined (a cell is empty) | seeds with maxR < minT 0/0
mixed         seeds 10 | n  4680 | range  2340 trend  2340 stress     0 | dates/seed 39 | overlap per seed ['1.000', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000'] | mean 1.000 | seeds with maxR < minT 0/10
exit 0
$ python3 probe.py $REPO ctl4 10
  замкнутость _tz47_probe_production.js: сверено 17 обращений, 7 имён, пропущенных 0
ctl4 production EFF_TREND 0.60 -> range/trend/stress [2069, 2385, 226] | EFF_TREND 0.90 -> [2894, 1560, 226] | populations move: True | trend shrinks as the cut rises: True
  замкнутость _tz47_probe_inverted.js: сверено 17 обращений, 7 имён, пропущенных 0
ctl4 inverted   EFF_TREND 0.60 -> range/trend/stress [2385, 2069, 226] | EFF_TREND 0.90 -> [1560, 2894, 226] | populations move: True | trend shrinks as the cut rises: False
exit 0
```

Notes on V-3:

- `seeds with maxR < minT` counts the seeds on which `R` and `T` do not cross at all. On the
  other seeds of `walk`, the crossing never reaches `T`'s median, so `overlap` stays 0.000.
- The inversion replaced the one line
  `if (out.eff !== null && Math.abs(out.eff) >= EFF_TREND) {` (`index.html:1886`, asserted to
  occur exactly once) with `<`, in a `/tmp` copy.
- `EFF_TREND` itself was read with `_read_js_num`; 0.90 is that value × 1.5.

**V-4. The two mechanism readings** (`/tmp/tz47probe/spread.txt`, MD5
`db4c6d24e47555955528a3b82abb5cac`):

```
ramp_smooth seed 1: n 468 | volatility min 1.315e-16 max 5.667e-16 (VOL_HARD 0.02) | |z| min 2.491e+13 (REG_STRESS_Z 2.0)
walk seed 1: volatility CV across coin-dates 1.33% (min 0.00962 max 0.01032) | max m in range 0.1090 · min m in trend 0.1090 · median m in trend 0.1905
walk seed 2: volatility CV across coin-dates 1.50% (min 0.00957 max 0.01055) | max m in range 0.1135 · min m in trend 0.1104 · median m in trend 0.1892
walk seed 3: volatility CV across coin-dates 1.50% (min 0.00952 max 0.01037) | max m in range 0.1131 · min m in trend 0.1066 · median m in trend 0.1877
```

**V-5. Probe source** (`/tmp/tz47probe/probe.py`, 150 lines, MD5
`f03dd4d4bceb1917efd6f4cf8221b385`). It is run as `python3 probe.py <repo> <worlds|ctl4>
<seeds>` from a directory that also holds a copy of `bench/backtest_bench.py`:

```python
#!/usr/bin/env python3
"""TZ-47 BLOCKED-run probe. Offline, synthetic, no fetch. Executes production's
marketRegime (cut from index.html) on each coin's own row (cut from main.py's
get_token_betas by the bench's CdBuilder) and computes TZ-47 §4 Claim A's
`overlap` on the §6 item 1 worlds as written, plus the variants that isolate why.
"""
import sys, os, json, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import backtest_bench as bb

REPO = sys.argv[1]
HTML = os.path.join(REPO, "index.html")
BOT = os.path.join(REPO, "main.py")
FUNCS = ["has", "marketRegime"]
VARS = ["H_NOISE", "VOL_HARD", "REG_STRESS_Z", "EFF_TREND"]
DRIVER = r"""
var fs = require('fs');
__EXTRACTED__
var job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var out = [];
for (var i = 0; i < job.length; i++) {
    var j = job[i];
    if (j.effTrend !== undefined) EFF_TREND = j.effTrend;
    var g = marketRegime(j.cd);
    out.push({ mode: g.mode, dir: g.dir, eff: g.eff, z: g.z, known: g.known });
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
"""

def bridge(html, name):
    return bb.JsBridge(html, FUNCS, VARS, DRIVER, name)

def series_from_lp(lps, t0=1700000000000):
    out = {}
    for c, lp in enumerate(lps):
        p = 10.0 * np.exp(lp)
        out["C%02d" % c] = {"prices": [[t0 + i * bb.HOUR_MS, float(p[i])] for i in range(len(p))],
                            "volumes": [[t0 + i * bb.HOUR_MS, 1e7] for i in range(len(p))]}
    return out

def world(kind, seed, n=12, hours=8760):
    rng = np.random.default_rng(seed)
    lps = []
    for c in range(n):
        t = np.arange(hours, dtype=float)
        if kind == "ramp_smooth":          # §6 w1 literal: smooth monotone climb
            lp = 0.001 * t
        elif kind == "ramp_bm":            # climb + Brownian noise, d/v in the trend band
            lp = np.cumsum(np.r_[0.0, 0.0003 + rng.normal(0, 0.004, hours - 1)])
        elif kind == "ramp_stair":         # monotone staircase: jump every 100 h
            lp = 0.0003 * 100 * np.floor(t / 100)
        elif kind == "walk":               # §6 w2: driftless, equal volatility
            lp = np.cumsum(np.r_[0.0, rng.normal(0, 0.01, hours - 1)])
        elif kind == "walk_hetvol":        # driftless, volatility differs per coin
            s = [0.004, 0.008, 0.016][c % 3]
            lp = np.cumsum(np.r_[0.0, rng.normal(0, s, hours - 1)])
        elif kind == "volclimb_bm":        # §6 w3 literal: ramp drift, volatility scaled up
            lp = np.cumsum(np.r_[0.0, 0.0003 + rng.normal(0, 0.015, hours - 1)])
        elif kind == "volclimb_zig":       # ramp drift, zig-zag noise: |eff| < cut on every date
            lp = 0.0003 * t + 0.007 * ((-1) ** np.arange(hours))
        elif kind == "mixed":              # w1 staircase coins + w3 zig-zag coins in one world
            if c % 2 == 0:
                lp = 0.0001 * 100 * np.floor(t / 100)
            else:
                lp = 0.0003 * t + 0.007 * ((-1) ** np.arange(hours))
        lps.append(lp)
    return series_from_lp(lps)

def cells(series, cdb, br, eff_trend=None):
    rows = []
    for t, row in bb.walk_grid(series, 7, 7):
        jobs, meta = [], []
        for s, i, iF, _ in row:
            cd = cdb.build(series[s]["prices"], series[s]["volumes"], i)
            if cd is None or cd["volatility"] is None or cd["r7"] is None or cd["r14"] is None:
                continue
            j = {"cd": {"volatility": cd["volatility"], "r7": cd["r7"], "r14": cd["r14"]}}
            if eff_trend is not None:
                j["effTrend"] = eff_trend
            jobs.append(j); meta.append((s, cd))
        if not jobs:
            continue
        for (s, cd), g in zip(meta, br.call(jobs)):
            if not g["known"]:
                continue
            rows.append({"t": t, "sym": s, "w": g["mode"], "dir": g["dir"],
                         "m": abs(cd["r14"]), "v": cd["volatility"], "eff": g["eff"], "z": g["z"]})
    return rows

def stat(rows):
    R = [r["m"] for r in rows if r["w"] == "range"]
    T = [r["m"] for r in rows if r["w"] == "trend"]
    S = [r for r in rows if r["w"] == "stress"]
    out = {"n": len(rows), "R": len(R), "T": len(T), "S": len(S),
           "dates": len(set(r["t"] for r in rows))}
    if R and T:
        MT, MR = float(np.median(T)), float(np.median(R))
        out["overlap"] = float(np.mean([m >= MT for m in R]))
        out["rev"] = float(np.mean([m < MR for m in T]))
        out["maxR"], out["minT"] = max(R), min(T)
    else:
        out["overlap"] = None
    return out

def ctl4(cdb, seeds):
    """§6 item 4 under §6 item 5's inversion: does a perturbed EFF_TREND still MOVE
    the populations when the trend comparison is inverted? Inversion is applied to
    a /tmp copy of index.html, never to the repository file."""
    src = open(HTML, encoding="utf-8").read()
    old = "if (out.eff !== null && Math.abs(out.eff) >= EFF_TREND) {"
    assert src.count(old) == 1, src.count(old)
    inv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index_inverted.html")
    open(inv, "w", encoding="utf-8").write(src.replace(old, old.replace(">=", "<")))
    base = bb._read_js_num(HTML, "EFF_TREND")
    for label, html in (("production", HTML), ("inverted", inv)):
        br = bridge(html, "_tz47_probe_%s.js" % label)
        tot = {}
        for sd in range(1, seeds + 1):
            ser = world("walk", sd)
            for k, et in (("base", None), ("x1.5", base * 1.5)):
                st = stat(cells(ser, cdb, br, eff_trend=et))
                a = tot.setdefault(k, [0, 0, 0])
                a[0] += st["R"]; a[1] += st["T"]; a[2] += st["S"]
        print("ctl4 %-10s EFF_TREND %.2f -> range/trend/stress %s | EFF_TREND %.2f -> %s | "
              "populations move: %s | trend shrinks as the cut rises: %s"
              % (label, base, tot["base"], base * 1.5, tot["x1.5"],
                 tot["base"] != tot["x1.5"], tot["x1.5"][1] < tot["base"][1]))

if __name__ == "__main__":
    cdb = bb.CdBuilder(BOT)
    if sys.argv[2] == "ctl4":
        ctl4(cdb, int(sys.argv[3])); sys.exit(0)
    br = bridge(HTML, "_tz47_probe.js")
    kinds = sys.argv[2].split(",")
    seeds = int(sys.argv[3])
    for kind in kinds:
        acc = []
        for sd in range(1, seeds + 1):
            st = stat(cells(world(kind, sd), cdb, br))
            acc.append(st)
        ov = [a["overlap"] for a in acc if a["overlap"] is not None]
        print("%-13s seeds %2d | n %5d | range %5d trend %5d stress %5d | dates/seed %d | "
              "overlap per seed %s | mean %s | seeds with maxR < minT %d/%d"
              % (kind, seeds, sum(a["n"] for a in acc), sum(a["R"] for a in acc),
                 sum(a["T"] for a in acc), sum(a["S"] for a in acc), acc[0]["dates"],
                 ["—" if a["overlap"] is None else "%.3f" % a["overlap"] for a in acc],
                 "undefined (a cell is empty)" if not ov else "%.3f" % np.mean(ov),
                 sum(1 for a in acc if a["overlap"] is not None and a["maxR"] < a["minT"]),
                 sum(1 for a in acc if a["overlap"] is not None)))
```

**TZ validation items, one by one.** Items marked «not run» were not run because the run stopped
at §2, and by contract §9 an item not run is a failed item.

| # | State |
|---|---|
| 1 | run on the unchanged file: exit 0 (V-1). No change exists to compile. |
| 2 | run on the unchanged file: exit 0 (V-1). |
| 3 | run: `git diff --stat` is empty (V-1). |
| 4 | **not run.** There is no «after». |
| 5 | **not run as specified.** The «before» is 487 / `FAIL 0` (V-1); there is no «after» and no letter was chosen. The next letter read from the headers is L (Status). |
| 6 | **not run as specified.** The worlds as written were probed and two of them cannot pass (Ground 2). |
| 7 | **not run.** |
| 8 | **not run.** |
| 9 | **not run as specified.** The production-vs-inverted populations are in V-3. |
| 10 | **not run as specified.** The item 4 × item 5 finding is in V-3. |
| 11 | **holds.** `--own-regime` does not exist, nothing was fetched, nothing was dispatched, and no archive figure is claimed. |
| 12 | **not run.** No branch was pushed. |
| 13 | **not run.** No CI change exists. |

## Test Results

- Fingerprint gate: **pass**. 7 anchors compared out of a 7-row table, 0 mismatches, revision
  `**Revision 2026-09-16-b.**` as required.
- TZ §2 interface check: **fail**, line 5, second clause.
- Gate step 14, local, unchanged tree: **487, `FAIL 0`**, exit 0.
- Probe, synthetic, 10 seeds per world:
  - world 2 `overlap` 0.000 against a required ≈0.5;
  - world 3 literal: 39.9 % `range` against a required 100 %;
  - world 3 all-`range` construction: `overlap` undefined;
  - mixed world: 1.000;
  - world 1 literal: 100 % `stress`; staircase: 100 % `trend`;
  - control 4, movement-only: True in production and True inverted; directional: True in
    production, False inverted.

## Deviations

None. No specification step was executed past §2. The probe executes no step of the TZ. It
measures the TZ's registered assertions on synthetic input, which contract §9 («a validator that
passes with no data is a failed validator») and the practice of TZ-42 and TZ-43 both require
before a written assertion is declared unsatisfiable.

## Pre-existing Issues

- **The dispatch cache is frozen at 05.09 and every run refetches the universe (map §10).** The
  key is `bench-${{ inputs.source }}-${{ inputs.years }}y-v4`. TZ-47 §8 instructs that it be
  recorded here with its paragraph as the reason:
  > The first own-regime reading must be taken on the same fetch discipline every standing
  > figure in §3.10a was taken on, and moving the archive's provenance in the same change that
  > takes a new reading would confound the two.

  This run was BLOCKED before it opened `backtest_bench.yml`. The workflow and its key are
  untouched, and the §10 row stands as it was.
- **`--html` / `--bot` defaults name files that do not exist.** They are
  `bench/Скрипт_Код_CriptoCalculator.html` and `bench/Код_для_Bota_на_GitHub.py` (`ls`: «No
  such file or directory» for both). Every workflow invocation passes both paths explicitly, so
  validation item 4 in a future run must use the workflow's command and not the bare flag. This
  is known, unchanged and not acted on.

## Remaining Risks

- **The probe is a session measurement on synthetic series and carries no product fact.** Its
  source, command and output are above, and re-running them is the reproduction. The worlds'
  parameters are the probe's own and are not proposed as the TZ's fixtures.
- **Claim A's reading on the archive is untouched.** Nothing here predicts it. What is
  established is that `overlap`, as registered, reads inside the «methodology stands» outcome
  on a world with no directional content (Ground 2). A future archive reading ≥ 0.25 would
  therefore rest on how widely volatility varies across the 30 coins and three years, which is
  a question the amended TZ may want to register explicitly.
- **The §2 line-5 miss is literal.** Its substance holds through `--target` and
  `--regime-gate`. An amended TZ that names one of those modes removes Ground 1, but not
  Ground 2.

## Commit

One commit, on `main`, on the `CryptoReports/**` direct-push path (contract §8). The workflow
filters were read before the push:

- `bench.yml`'s `push` carries `'**.md'` under `paths-ignore`;
- `main.yml`'s `push` is a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`;
- `calib.yml`'s `push` is limited to `claude/**` branches and two paths;
- `journal.yml` is `schedule` / `workflow_dispatch`;
- `backtest_bench.yml` is `workflow_dispatch` only.

Message:

```
docs(reports): TZ-47 — BLOCKED, §2 line 5 fails (--regimes never calls marketRegime) and §6 worlds 2 and 3 cannot read as registered (TZ-47)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: `CryptoReports/TZ-47-own-regime-direction-backtest-report.md`, added.

No hash appears here. This report's own commit had not been made when this section was written
(inv. 54, contract §10).

## Pull Request

None. By class this is a branch TZ, but the run was BLOCKED before any deliverable existed.
No implementation commit, branch or pull request exists. The report-only fixed line is not
used, because it would assert a class this TZ does not have.

## CI Execution

No workflow ran on a runner for this task, because no branch was pushed. Every bench reading
in this report is a local run in this session's container, including gate step 14's 487.
`backtest_bench.yml` is `workflow_dispatch` only and does not run on push.

## Final Repository State

This session leaves the working tree clean at `9e30a6ec4ce75b6887fca55551ab1785cda1a18a`
(`origin/main` after the fetch, reached by fast-forward from `7683f89`). That is the commit
every fingerprint below was taken against. `git status --porcelain --ignored` printed nothing
after `bench/__pycache__/` was removed. The probe, its outputs and the bench copy it imported
live under `/tmp/tz47probe/`, outside the repository. No branch was created or pushed.

Nothing awaits a merge from this TZ, so "NOT IN EFFECT UNTIL MERGED" has no referent and is not
written.

## Fingerprints

**System Map.** `SYSTEM-MAP-CRYPTOCALCUL.md`: **2759 lines**, MD5
`7f8fd2e8e553109cb7cffed329bd56e1`. Revision string in `## 0. Fingerprint`:
`**Revision 2026-09-16-b.**`, which is what the TZ requires.

**Anchor table.** The table was cut by structure: in each file, the first markdown table inside
the `## 0` block, every row after its separator line up to the first line not starting with
`|`. No anchor name was used to select rows.

- map table rows: **7** · TZ header table rows: **7** · compared: **7** · mismatches: **0** ·
  TZ rows absent from the map table: none;
- each TZ row is byte-identical to the corresponding map row.

Per anchor, the command and the text the fixed-string match returned:

| Anchor | Command | Returned (exit 0 on all seven) |
|---|---|---|
| revision | `grep -F -m1 -o -- '**Revision 2026-09-16-b.**' SYSTEM-MAP-CRYPTOCALCUL.md` | `**Revision 2026-09-16-b.**` |
| direction engine | `grep -F -m1 -o -- '### 3.12 Direction engine — veto cascade' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `grep -F -m1 -o -- '### 3.15 Catalyst registry' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.15 Catalyst registry` |
| exhaustion measure | `grep -F -m1 -o -- '### 3.16 List exhaustion — the day-range measure' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `grep -F -m1 -o -- '## 11. Analytical engine' SYSTEM-MAP-CRYPTOCALCUL.md` | `## 11. Analytical engine` |
| squeeze block | `grep -F -m1 -o -- '### 3.17 «РИСК ВЫНОСА» — the day's own risk' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `grep -F -m1 -o -- '71. **A measurement that is not RETAINED was not taken,' SYSTEM-MAP-CRYPTOCALCUL.md` | `71. **A measurement that is not RETAINED was not taken,` |

**Files in the map's `## 0` table**, measured with `wc -l` and `md5sum`. The TZ's quoted table
is byte-identical to the map's (`diff` empty).

| File | Lines | MD5 | Map / TZ |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

**Files the TZ's gate adds:**

| File | Lines | MD5 | TZ |
|---|---:|---|---|
| `bench/backtest_bench.py` | 5102 | `ba633202f43845ba0fdafbc1b92d9c04` | match |
| `bench/backtest_guard_bench.py` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` | match |

**Other documents read:**

| File | Lines | MD5 |
|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` (v23; the map states 864 / `02abb1969626d2af150a0d1f6e02f2a7`, match) | 864 | `02abb1969626d2af150a0d1f6e02f2a7` |
| `ANALYST-INSTRUCTIONS.md` (`2026-09-16-c`) | 3040 | `aa1d1ccab703b322e0801511e637b331` |
| `CryptoTZ/TZ-47-own-regime-direction-backtest.md` | 339 | `676c0becd86fd75230dea4a6bf16cc9d` |
| `bench/verify_bench.py` (map prose: 540 / `28eb1949f21d0afadb062303108f7101`, match) | 540 | `28eb1949f21d0afadb062303108f7101` |
