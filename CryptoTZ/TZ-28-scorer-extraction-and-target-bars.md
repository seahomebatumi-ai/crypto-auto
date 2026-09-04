# TZ-28 — repair the JS extraction set, re-register the D2/D3 bars, give `marketRegime` the whole BTC record

**Canonical filename: `TZ-28-scorer-extraction-and-target-bars.md`. File it at
`CryptoTZ/TZ-28-scorer-extraction-and-target-bars.md`** — the name a file arrived
under is never the identifier (contract §3).

**Model: Opus.** Three coupled changes in one file, two of them re-registrations of
lab bars and one a static analyser over extracted JavaScript. Not mechanical.

---

## 0. System Map fingerprint — required, blocking

Required revision string, quoted as an exact substring:

```
**Revision 2026-09-03-b.**
```

All seven content anchors, each matched as an exact substring against
`SYSTEM-MAP-CRYPTOCALCUL.md` on `origin/main`:

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-03-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `59. **A standing decision is amended in the floor before it is amended in the code.**` |

The map's `## 0` file table at this revision — measured, reported, not enforced:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**The map is one revision behind the code and that is deliberate, not a mismatch to
block on.** TZ-27 merged (`bench/backtest_bench.py` on `origin/main` is 2544 lines,
MD5 `fb9464afba2e87450bd3fd11877da9f1`) and the map has not yet been revised for it;
`backtest_bench.py` is not in the `## 0` table, so no fingerprint row moves. One map
revision covers TZ-27 and TZ-28 together, after this merge.

---

## 1. Why this TZ exists

TZ-27 built the `--target` instrument and reported PARTIAL for two reasons, both
outside its own scope. Both are re-derived below from the repository, not taken from
that report's word (map inv. 55).

**Fact 1 — the score bridge has been reference-broken since `scoreCandidate` was
split.** `JS_FUNCS` (`bench/backtest_bench.py:41`) reads

```python
JS_FUNCS = ["has", "clamp01", "sigmaDay", "volRegime", "scoreCandidate"]
```

and `scoreCandidate` ends at `index.html:1779` with

```js
    return scoreFinish(cd, sym, p24, qv, sd, isLong, parts, ws, reasons, true);
```

`scoreFinish` (`index.html:1802`) calls `qualityScore` (`index.html:1790`). Neither
is extracted, so the bundle throws `ReferenceError: scoreFinish is not defined` on the
first row. `JS_DRIVER`'s per-row `catch (e) { r = null; }` converts that into a list of
nulls, and the run dies far downstream comparing `None` with `None`. **`--selftest`,
`--run` and `--regimes` all drive this bridge**, and `backtest_bench.yml` runs
`--selftest` as step 2 under `bash -euo pipefail`, so that workflow has been stopping
at step 2 — which is why the archive measurement was unreachable before TZ-27 touched
anything.

**Fact 2 — a hand-written extraction manifest is the defect, and the two missing names
are its symptom.** The manifest goes stale the moment production splits a helper out,
and the failure is silent by construction: the catch swallows it and the mode reports a
data-shaped error hundreds of lines away. The repair is a check that the assembled
bundle is closed under reference, so the next split fails at build time naming the
identifier.

**Fact 3 — the k = 1.0 grid point of `--target` is unreachable by production
arithmetic, not by chance.** `tradeGeometry` (`index.html:1901`) sets
`g.reward = (tgt − E)/E` and `g.rr = g.reward / inv.dist`; `inv.dist` is floored at
`INV_FLOOR_SD · sigmaDay(vol)`, so RR is largest exactly at that floor and rises with
volatility up to `VOL_STOP`. Measured through production's own `tradeGeometry`, at the
floor and at `vol → VOL_STOP`:

| k | `rr` from production | ≥ `RR_MIN` = 2.0 |
|---:|---:|---|
| 1.0 | 1.6169 | **no** |
| 1.5 | 2.6940 | yes |
| 2.0 | 4.0023 | yes |
| 2.5 | 5.5914 | yes |
| 3.0 | 7.5214 | yes |

D2 requires `Ω(k)` strictly decreasing across five grid points, one of which can never
hold a setup. The bar cannot be met on any world, so **the control tests nothing**: it
was red before the data and stayed red after.

**Fact 4 — D3's bar is two hand-written numerals, one of them unreachable at the
horizon it names.** `P_none < 0.05` at `H = 8 × H_NOISE` and a ±15 % band around
`Σq/Σ(1−q)`. A band deciding whether a measurement is plausible is derived from a null
computed in the same run, never written into the rule as a numeral (map inv. 49);
`P_none` is a decaying function of the window and 8 × is simply the wrong rung.

**Fact 5 — `btcStats` in `--target` is a shape production never builds.**
`run_target` (`bench/backtest_bench.py:1884`) hands the bridge

```python
        btc_stats = {"volatility": bcd["volatility"]}
```

while production passes `botData.btc`, the whole `coeffs.btc` record.
`leverageDecision` reads `btcStats.volatility` and nothing else
(`index.html:1575`), but `marketRegime` reads `btcStats.r7` and `btcStats.r14`
(`index.html:1869`, `1873`), so the recorded regime label can only ever be `range` or
`stress` — degenerate by construction, and a later reader grouping by it would be
grouping on a field that cannot say `trend`. This is map inv. 48: a bench that builds
its own input proves the function, not the wiring. `CdBuilder.build` already returns
`r7`, `r14` and `r30` computed by the bot's own `window_stats`, which is the same
function `main.py:402–404` uses for BTC, so the faithful object costs nothing.

**None of this is a licence to edit an assertion (contract §7 item 2).** Facts 3 and 4
are stale expectations, which that clause routes to a TZ, and this is it: the bars
below are Architect re-registrations, and each is accepted only if it FIRES on an
inverted resolver — which is exactly what the bars being replaced could not do.

---

## 2. Scope

**Files to Modify: `bench/backtest_bench.py` — and nothing else.**

Files to Create: none. Files to Renamed/Deleted: none.

**`.github/workflows/backtest_bench.yml` is deliberately NOT in scope.** Its step
order costs the measurement runtime but nothing else, and touching CI would impose a
negative test (contract §9) that no session can perform. That is how TZ-27 acquired an
unpassable validation item; it is not repeated here.

Scopes A, B and C are independent. If one blocks, complete the others and report the
blocked one (contract §6).

### Scope A — the extraction set and its closure check

**A1.** `JS_FUNCS` becomes, in dependency order:

```python
JS_FUNCS = ["has", "clamp01", "sigmaDay", "volRegime", "qualityScore",
            "scoreFinish", "scoreCandidate"]
```

`JS_VARS` is unchanged: `EFF_TREND`, `PACE_Z` and `VOL_ABNORMAL` are the only constants
the enlarged bundle reads, and all three are already there.

**A2.** Add one helper and one check, used by BOTH bundle builders — `extract_js` and
`_extract_js_set`:

- `_strip_js_noise(src)` blanks string literals and `//` / `/* */` comments while
  preserving length and newlines. The stepping rules are the ones
  `_skip_to_matching_brace` already implements; do not write a second set of them —
  factor the shared logic or reuse it, but there must be exactly one description of
  how a JS string and a JS comment are traversed in this file (map inv. 20).
- `_assert_js_closed(bundle_src, driver_src, label)` raises `RuntimeError` naming the
  first missing identifier when the bundle references a name that is neither defined in
  the bundle, nor declared in the driver text, nor a JavaScript global. Both halves are
  required and both run on stripped text:
  - **called identifiers** — every `name(` occurrence that is not a method call and not
    a keyword;
  - **constant reads** — every bare `UPPER_SNAKE` identifier of three characters or
    more.
  The defined set is DERIVED, never typed: `function NAME(` and `var NAME` declarations
  found in the bundle and in the driver, plus the declared parameters of every function
  in either, plus a small literal list of JavaScript globals (`Math`, `JSON`,
  `isFinite`, `isNaN`, `parseFloat`, `parseInt`, `Number`, `String`, `Array`, `Object`,
  `Date`, `RegExp`, `Error`, `require`, `process`, `console`, `NaN`, `Infinity`).
- The check runs at bundle-build time, before `node --check`, for all four bundles —
  `JS_FUNCS`, `INV_JS_FUNCS`, `RES_JS_FUNCS`, `TARGET_JS_FUNCS`.

The check must count what it compared and fail on zero identifiers examined (map
inv. 22).

**Not in scope: the per-row `catch (e) { r = null; }` in any driver.** It is the right
behaviour for a data-shaped exception, and A2 removes the reference class before any
world is generated. Do not touch it.

### Scope B — re-register D2 and D3 of `lab_selftest` section D

D1, D4, D5 and D6 are untouched.

**B1 — one new registered constant, one declaration (map inv. 20):**

```python
TGT_H_LADDER = [1, 4, 8, 16, 32]   # multiples of H_NOISE, registered before data
TGT_MONO_MIN_PTS = 3               # fewest grid points a monotonicity claim needs
```

**B2 — D2, replacing the five-point form.** The admissible set is MEASURED through
production, never derived in Python (map inv. 21). Build one probe job and send it
through the same `JsBridge(html, TARGET_JS_FUNCS, TARGET_JS_VARS, TARGET_DRIVER, …)`
the mode already uses:

- `E = 1`, `vol` immediately below `VOL_STOP` (cut with `_read_js_num`), `min30` and
  `max30` set within a rounding step of `E` so `invalidationInfo`'s `dStruct` clamps up
  to the `INV_FLOOR_SD` floor, and `subs = {k: E·exp(k·vol·√H_NOISE)}` over `K_GRID`;
- read `g.rr` per grid point. `tradeGeometry` sets `rr` before it pushes any veto, so a
  refused row still reports its number.
- A grid point is **admittable** iff its probe `rr ≥ RR_MIN`, both numbers production's
  own.

Registered conditions, both required:

- **D2a** — `n(k)` is zero on exactly the non-admittable grid points, non-zero on
  exactly the admittable ones, and non-decreasing across the grid. Non-decreasing is a
  known-answer property, not an observation: RR grows with target distance at fixed
  `(vol, dist)`, so admission at `k` implies admission at every larger `k`.
- **D2b** — `Ω(k)` is strictly decreasing across the grid points that meet
  `TGT_QUORUM_N`, and there are at least `TGT_MONO_MIN_PTS` such points. Fewer is СТОП:
  a monotonicity claim over two points is not a claim (map inv. 22).

The printed line keeps the existing shape — the Ω chain and the per-point admitted
counts — and gains the probe `rr` and the admittable flag per grid point, so a reader
sees why a point is empty without running anything.

**B3 — D3, replacing the single-rung form.** Run `run_target` once per rung of
`TGT_H_LADDER` with `k_grid=[]` and `H_override = m · H_NOISE`, and read the pooled
`prod` arm. Registered conditions, all three required, none carrying a numeral about
the outcome (map inv. 49):

- **D3a — escape decays.** `P_none` is non-increasing across the ladder and
  `P_none(last) < P_none(first)`. This is the two-barrier property and nothing else.
- **D3b — convergence direction.** The relative gap `|Ω − Σq/Σ(1−q)| / (Σq/Σ(1−q))` is
  smaller at the last rung than at the first.
- **D3c — the limit is reached where escape has decayed.** At the rung with the
  smallest relative gap among rungs meeting quorum, `Σq/Σ(1−q)` lies inside `Ω`'s CI95
  as the mode's own date resampling computes it, AND that rung's `P_none` is at or
  below the ladder's median `P_none`. The second clause is what stops the first from
  being satisfied by a lucky high-escape rung.

The printed block shows the whole ladder — one line per rung with `n`, dates, quorum,
`P_none`, `Ω` with its CI, the closed form and the gap — then the three verdicts. A
ladder printed in full is what let this bar be re-registered from evidence rather than
from an opinion, and the next reader deserves the same.

### Scope C — the whole BTC record reaches `marketRegime`

`bench/backtest_bench.py:1884` passes the full `bcd` instead of a two-field literal.
The comment above it is replaced: the object production hands these functions is
`coeffs.btc` entire, `leverageDecision` takes `volatility` off it and `marketRegime`
takes `r7` and `r14`, so a hand-built subset silences one reader to serve the other
(map inv. 48).

`reg` remains recorded and never gating — no primary, descriptive or admission may
begin to read it in this TZ.

---

## 3. Validation — written by the Architect, every item runnable offline in-session

Baseline first: record the failing state on `origin/main` before the change, so the
diff is provable (contract §9).

| # | Item | Pass condition |
|---|---|---|
| 1 | `python3 -m py_compile bench/backtest_bench.py` | exit 0 |
| 2 | Baseline: `--selftest` on an unmodified `origin/main` copy | fails, and the report quotes the `ReferenceError` frame and the downstream `TypeError` line |
| 3 | Closure check, silence | all four bundles report zero missing identifiers; the number of identifiers examined per bundle is printed and is non-zero (inv. 22) |
| 4 | Closure check, known-answer control, both halves | removing `scoreFinish` from `JS_FUNCS` raises naming `scoreFinish`; removing `VOL_ABNORMAL` from `JS_VARS` raises naming `VOL_ABNORMAL`; restoring both is silent and the build is byte-identical to the pre-control build (inv. 45) |
| 5 | `--selftest --seeds 10 --html ../index.html --bot ../main.py` | exit 0; quote the verdict line and the three world blocks |
| 6 | `--lab-selftest --html ../index.html --bot ../main.py` | exit 0; section D printed in full, D1–D6 all ОК; quote section D verbatim |
| 7 | **Negative test — the acceptance criterion for Scope B.** Invert the long/short branch of `_touch_calc` in the working tree | **D1, D2, D3 and D6 all turn СТОП.** D2 and D3 turning red is the point: under the bars being replaced, both were already red and the inversion changed nothing. D4 and D5 correctly do not fire. Revert, and `--lab-selftest` output is byte-identical to the run before the test |
| 8 | Scope C differ | `run_target` on one seeded world before and after the `btc_stats` change: every field of every observation identical except `reg`; report the number of fields compared and fail on zero (inv. 22, 45). Report the `reg` distribution on both sides |
| 9 | Bridge smoke for `--run` and `--regimes` | `JsScorer(html)` constructs, and a one-row job returns a finite score on each side |
| 10 | `bench.yml` gate unchanged | 13 steps, **1 255 401 checks, 0 failures**, delta against the map = 0. Step 4 (`verify_bench.py`) imports this module and is the gate's proof that it imports cleanly. If step 5 exhausts node's heap on the VPS, that is the ceiling map §10 already records — raise `NODE_OPTIONS` and say so; it is not a product failure |
| 11 | Production untouched | the four `md5sum` of the map's `## 0` table unchanged |
| 12 | Standing checks | `python3 -m py_compile main.py` exit 0; `node --check` on the `<script>` block extracted from `index.html` exit 0 |

**No item on this list needs a runner, a credential or a network fetch.** The archive
measurement is not a validation item of this TZ and must not be attempted in-session
(contract §7 item 9, map inv. 44): it is dispatched by the Boss after the merge and its
numbers belong to the audit, not to this report.

Report the wall-clock cost of `--lab-selftest` before and after. Section D grows from
three `run_target` calls to seven; if that pushes the lab past a working length, say
so — it is a finding for the next TZ, not a reason to shorten the ladder here.

---

## 4. Out of scope — report, do not touch

- `.gitignore`'s explanatory comment is one bridge name short (`bench/_tgt_bridge.js`);
  the `bench/_*` rule itself covers it. Left open deliberately.
- `target_raw.json` can carry bare `NaN` where a pooled arm records zero stop touches,
  mirroring `stops_raw.json`. Left open deliberately.
- The step order of `backtest_bench.yml` (§2).

---

## 5. Commit Message

```
fix(bench): close the JS extraction set, re-register D2/D3, full BTC cd to marketRegime (TZ-28)
```

---

## 6. Report

`CryptoReports/TZ-28-scorer-extraction-and-target-bars-report.md`, in the format of
contract §10, straight to `main`. The implementation goes on a branch and waits for the
Boss to merge after the audit verdict.

The report carries section D verbatim, both the baseline and the repaired `--selftest`
output, and the Scope C differ's field count. A hash proves a file changed and never
proves which change landed: every claim is a command and its output.
