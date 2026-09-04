# Implementation Report — TZ-27

## Status

**PARTIAL.** Scope A and Scope B are complete and every file the TZ forbids to move is
byte-identical. Two of the nine validation items do not pass, and neither can be made to
pass by this Executor:

- **Item 3 — `--lab-selftest` green with section D present: FAILS.** Section D is
  implemented in full; **D1, D4, D5 and D6 are green, D2 and D3 are red on their
  registered pass conditions.** Both are red for reasons that are properties of production
  geometry, not of the new code, and both are proved below with the arithmetic. Hard floor
  item 2 forbids editing an assertion to make it pass, so they stand red and are reported
  as findings.
- **Item 6 — the archive run on a runner: NOT RUN.** This session has no runner and no
  credential, and inv. 44 forbids a session fetch from standing behind a product fact. It
  is also unreachable through `backtest_bench.yml` today for a **pre-existing** reason
  recorded under `## Pre-existing Issues`: step 2 of that workflow (`--selftest`) is red on
  `origin/main` before this TZ touched anything.

The measurement instrument therefore exists, is self-tested and is wired into its
workflow; the measurement itself has not been taken, so **the numbers this TZ was
commissioned to produce do not exist yet** and no later TZ can cite them.

## Inbound Filing

None. The TZ arrived at its canonical path `CryptoTZ/TZ-27-continuation-target-backtest.md`
(commit `3d7fdaf`, "Add files via upload") and needed no `git mv`.

## Scope Executed

**Branch TZ** (§8): the scope names files outside `CryptoReports/**`, so this opened a
branch and, under the §8 fallback, a compare URL in place of a pull request.

- **Scope A** — `bench/backtest_bench.py`: new `--target` mode plus section D of
  `lab_selftest`. Complete.
- **Scope B** — `.github/workflows/backtest_bench.yml`: the mode is selectable and its
  artifact uploaded, by the mechanism `--stops` already uses. Complete.

## Files Created

None. `target_raw.json` is a run artifact next to `stops_raw.json` and is not committed.

## Files Modified

| File | Lines added | Note |
|---|---:|---|
| `bench/backtest_bench.py` | +555 / −1 | new section 10 (`--target`); section 10 renumbered to 11; section D added to `lab_selftest`; `--target` parsed and dispatched |
| `.github/workflows/backtest_bench.yml` | +10 | one step, two artifact paths |

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**The two arms share one risk leg, by construction rather than by care.**
`leverageDecision` is called once per (date, coin, side) on the untouched `cd`, and the
resulting `dec` is passed into every `tradeGeometry` call, so `inv.dist`, `inv.price`,
`moneyBelowMin` and `ok` are the same numbers in both arms and only the reward leg moves.
The continuation arm is a shallow copy of `cd` whose `max_price` (long) / `min_price`
(short) is replaced by `E·exp(±k·vol·√H)`, handed to the **unmodified** `tradeGeometry`;
the copy reaches `tradeGeometry` and nothing else. The substituted field is the opposite
side from the one `invalidationInfo` reads for its reference, so the substitution cannot
leak into the stop — that is a property of the code, not an assumption: for a long the
target side is `max_price` while `invalidationInfo` reads `min30`/`min_price`.

**Nothing is reimplemented.** Seventeen production functions and eighteen constants are
cut out of `index.html` at every run through the existing `_extract_js_set`/`JsBridge`
path (inv. 21, 38); the mode adds no second implementation of any rule, and the horizon
and the primary's bar are read from the source (`H_NOISE`, `RR_MIN`) rather than typed.

**Admission** is that arm's own geometry veto and nothing else — `g` non-null and
`g.veto` empty. The regime and channel layers are deliberately not applied: they decide
the side, not the target. `marketRegime` is recorded per observation so a later reader can
group by it without the primary depending on it.

**First touch** is resolved on the hourly high/low rows of the forward window: for a long,
target when `high ≥ tgt` and stop when `low ≤ stop`, mirrored for a short. When both
barriers fall inside the same hourly candle the order is unresolvable at this resolution,
so the outcome is recorded as `tie` and excluded from the odds — recorded, never guessed.

**Registered before any data** (inv. 23), each from one declaration (inv. 20): horizon
`H_NOISE` cut from `index.html` (168 h), step 7 days, k grid {1.0, 1.5, 2.0, 2.5, 3.0},
quorum 60 admitted setups and 20 contributing dates per side per arm, 2000 date-level
resamples with the same construction `stops_summary` uses. `--horizon`/`--step` are
deliberately not read by this mode.

**The primary** is `Ω = n_tgt / n_stop` on the production arm, pooled per side, `tie` and
`none` excluded from both counts, CI95 by date resampling, against the bar
`1/RR_MIN = 0.50`. The verdict is printed from the registered rule, never from the
number's appearance. The realised R-multiple is printed with the sentence that it carries
no consequence (inv. 32).

**Inv. 48** — the mode assembles `hi24`/`lo24` itself, so `run_target` reads
`tradeGeometry`'s declared parameter names out of the source and refuses to run if the
last two are not `hi24, lo24`. The check runs once per invocation, in the real run and in
every lab control.

## Validation

| # | Item | Result |
|---|---|---|
| 1 | `python3 -m py_compile bench/backtest_bench.py` | **exit 0** |
| 2 | `node --check` on the generated bridge | **exit 0** on `bench/_tgt_bridge.js`; `_extract_js_set` also runs `node --check` itself and raises on failure — it ran on every mode invocation and never raised |
| 3 | `--lab-selftest` green with section D present | **FAILS** — D1/D4/D5/D6 green, **D2/D3 red**; lab exit 1. Detail below |
| 4 | Negative test | **PASS** — inversion turns D1 and D6 from ОК to СТОП; revert restores byte-identical output |
| 5 | Regression on shared dependencies | **PASS** — lab sections A/B/C byte-identical before/after; `--selftest` identical (and identically broken, pre-existing) |
| 6 | The archive run, on a runner | **NOT RUN** — no runner, no credential; inv. 44. See `## Status` |
| 7 | `bench.yml` unchanged and still green | **PASS** — 13 steps, **1 255 401 checks, 0 failures, delta against the map = 0** |
| 8 | Production untouched | **PASS** — four `md5sum` unchanged |
| 9 | Standing checks | **PASS** — `py_compile main.py` exit 0; `node --check` on the `<script>` block exit 0 |

### Item 7 — the gate, step by step

Run locally, not on a runner. Every step's own printed count:

| Step | Bench | Checks |
|---:|---|---:|
| 1 | `verify_board.js` | 109 |
| 2 | `board2_bench.js` | 130 |
| 3 | `prot_bench.js` | 372 |
| 4 | `verify_bench.py` | 35 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 |
| 6 | `fresh_bench.js` | 3 424 |
| 7 | `journal_bench.js` | 693 895 |
| 8 | `catalyst_bench.js` | 24 692 |
| 9 | `display_bench.py` | 24 598 |
| 10 | `render_bench.py` | 16 171 |
| 11 | `direction_bench.py --display` | 15 629 |
| 12 | `exhaustion_bench.js` | 220 598 |
| 13 | `live-gate.sh --selftest` | 40 |
| | **total** | **1 255 401** |

The map states 1 255 401 at this revision. **Delta zero**, so no term needs attributing.
Step 4 matters here beyond its own count: `verify_bench.py` imports `backtest_bench.py`,
so it is the gate's proof that the new module-level code imports cleanly.

**`bench.yml` does not invoke `--lab-selftest` and does not run `backtest_bench.py`
directly** — read at `.github/workflows/bench.yml`, and stated in that file's own header
("`backtest_bench.py` — нужен архив/кэш, обслуживается `backtest_bench.yml`").
**Section D is therefore a manual control, outside the gate**, and its step count moves
nothing. Section D is not a bench FILE, so hard floor item 12's wiring requirement does not
apply (TZ §2 says the same).

### Item 4 — the negative test, both directions

The long/short barrier comparison in `_touch_calc` was inverted in the working tree
(`if is_long:` → `if not is_long:`, swapping the two branches).

| Control | Correct code | Inverted | Fired? |
|---|---|---|---|
| D1 calibration | 0.93 [0.69; 1.16] ОК | **7.48 [7.48; 7.48] СТОП** | **yes** |
| D2 monotonicity | СТОП (see below) | СТОП, all five `nan` | already red |
| D3 long-horizon identity | СТОП (see below) | СТОП, Ω `nan` | already red |
| D4 identity differ | 7 848 comparisons, 0 diffs ОК | 7 848 comparisons, 0 diffs ОК | no — correctly |
| D5 look-ahead | ОК | ОК | no — correctly |
| D6 side swap | 0.037 / 0.013 ОК | **`nan` / `nan` СТОП** | **yes** |

D4 and D5 not firing is the right behaviour and worth stating: an identity comparator and
a truncation-invariance check are both insensitive to the direction of a barrier, because
the same inverted resolver runs on both sides of each comparison. The controls that exist
to catch a side error — D1 and D6 — both caught it.

After reverting, `--lab-selftest` output is **byte-identical** to the pre-test run
(`diff` clean over the whole file), and the working tree contains only the two in-scope
files.

## Test Results

### Section D, as registered, on `synth_hl("normal")` (15 coins + 1 as the BTC meter, 82 dates)

```
D1 калибровка цели, k=1.5: 0.93 [0.69; 1.16] ОК
D2 монотонность Ω(k): nan > 0.287 > 0.121 > 0.055 > 0.018 СТОП
   допущено на точку сетки: k=1.0 n=0 · k=1.5 n=346 · k=2.0 n=823 · k=2.5 n=977 · k=3.0 n=1113
D3 тождество на 8×168ч: P(никуда) 0.154 · Ω 0.213 против Σq/Σ(1−q) 0.249 СТОП
D4 тождественный дифф: сравнений 7848, расхождений 0 ОК
D5 взгляд в будущее: запись на полном ряде против обрезанного на t+H — совпала ОК
D6 обмен сторон: Ω лонг 0.037 · Ω шорт 0.013 ОК
```

### D2 — why the registered condition cannot be met

`Ω(k)` is required to be strictly decreasing **across the five grid points**. The first
grid point has an empty admitted set, and not by chance: **a `k = 1.0` continuation target
can never clear `RR_MIN`.** `RR = reward / dist`, and `dist` is floored at
`INV_FLOOR_SD · sigmaDay = 2·vol·√24 = 9.80·vol`, so `RR` is largest exactly at that
floor, where `RR(k=1) = (exp(vol·√168) − 1) / (9.80·vol) → 12.96/9.80 = 1.32` as vol → 0,
rising only with the convexity of `exp`.

Measured through production's own arithmetic, sweeping the entire range in which leverage
is issued at all (`0 < vol < VOL_STOP = 0.03`), both sides, stop pinned at the floor:

| k | max RR over the sweep | admitted |
|---:|---:|---:|
| 1.0 | **1.611** | **0 of 120** |
| 1.5 | 2.680 | 34 |
| 2.0 | 3.973 | 70 |
| 2.5 | 5.539 | 70 |
| 3.0 | 7.435 | 70 |

`RR_MIN = 2.0`. The point is unreachable for every coin the system can trade, on every
world, so the five-point form of D2 can never be evaluated.

**The property D2 exists to test passes** wherever it can be measured: across the four
populated grid points `Ω(k)` falls **0.287 > 0.121 > 0.055 > 0.018**, strictly. And the
mechanism is the TZ's own §1 fact 2, applied to the continuation arm: `RR_MIN` is monotone
increasing in target distance with no ceiling, so it does not merely admit the far target —
it **refuses the near one outright**.

### D3 — why the registered condition cannot be met

D3 requires `P_none < 0.05` **and** `Ω` within ±15 % of `Σq/Σ(1−q)` at `H = 8 × 168 h`.
The identity half passes (0.213 against 0.249, a 14.5 % gap). `P_none` measures **0.154**.

Sweeping the horizon on the same world shows the resolver is right and the bar is set at
the wrong multiple:

| H | P_none | Ω | Σq/Σ(1−q) | gap |
|---|---:|---:|---:|---:|
| 1 × 168 h | 0.639 | 0.026 | 0.248 | 89.5 % |
| 4 × | 0.304 | 0.146 | 0.248 | 41.1 % |
| 8 × | **0.154** | 0.213 | 0.249 | 14.5 % |
| 16 × | 0.056 | **0.250** | **0.250** | **0.0 %** |
| 32 × | 0.000 | 0.293 | 0.250 | 17.2 % |

`P_none` decays monotonically to zero as the window grows, exactly as a two-barrier
problem requires, and the realised first-touch odds converge on the closed-form driftless
prediction — **exactly** at 16 ×, where `P_none` has all but vanished. That is as strong a
statement as this control can make about the resolver, and it is a pass on the substance.
The registered `< 0.05` is reached at roughly 16–20 ×, not at 8 ×: at 8 × the stop still
sits only ≈0.27–0.80 σ of the window away, so a sixth of the setups legitimately touch
neither barrier.

### The primary, exercised end to end (synthetic world — NOT a market reading)

On the driftless world the production arm reads `Ω = 0.037` (long, CI95 [0.011; 0.071],
570 setups, 82 dates) and `Ω = 0.013` (short, CI95 [0.000; 0.033], 411 setups), both above
quorum, both CI95 entirely below 0.50, and the registered rule prints the corresponding
verdict. This demonstrates the mode reaches a verdict and nothing else: on a random walk
the 90-day extremum sits ≈4.5 weekly sigma away, so a near-zero Ω is arithmetic, not a
finding about markets. **No claim about the real universe is made anywhere in this report.**

## Deviations

1. **D1, D2 and D3 are evaluated on both sides pooled; D6 per side.** A7 registers
   "pooled per side" for the primary only; D1/D2/D3 name no side. Pooling is what makes
   the grid points evaluable at all and gives each control its data; D6 is per side because
   it compares the sides to each other.
2. **The extraction set carries eight constants beyond the ten TZ §2 quotes** —
   `RISK_Z`, `H_REACT`, `H_BTC`, `VOL_ABNORMAL`, `VOL_HARD`, `VOL_STOP`, `EFF_TREND`,
   `REG_STRESS_Z`. `leverageDecision` and `marketRegime` read them transitively, so a
   bridge without them throws. §2's list is quoted source text, not an extraction manifest.
   No constant is introduced anywhere and none is typed: all eighteen are cut.
3. **The TZ carries no `## Commit Message` section**, so the message was composed in the
   established style of TZ-20/23/26 rather than quoted verbatim (§8).
4. **`--lab-selftest`'s section D uses one of `synth_hl`'s own coins as the BTC meter**
   (popped from the world, as `load_cache` pops BTC), rather than a new generator. No
   change to `synth_hl`.

## Pre-existing Issues

Not caused by this TZ, not fixed by it (§6, §12). Each was proved against `origin/main`'s
own copy, not argued.

1. **`--selftest` is broken on the current `index.html`, and with it every `JsScorer`
   mode.** `JS_FUNCS` (`bench/backtest_bench.py:41`) extracts
   `has, clamp01, sigmaDay, volRegime, scoreCandidate`, but `scoreCandidate` also calls
   **`qualityScore`** and **`scoreFinish`**, neither of which is extracted. The bridge
   throws `scoreFinish is not defined`, the driver's `catch` turns every score into `null`,
   and the run dies at `backtest_bench.py:1051` with
   `TypeError: '>' not supported between instances of 'NoneType' and 'NoneType'`.
   Proved by running `git show origin/main:bench/backtest_bench.py` from `/tmp`: identical
   failure, identical frame. `--run` and `--regimes` drive the same bridge.
   **Operational consequence, and the reason item 6 was already unreachable:** in
   `backtest_bench.yml` the `--selftest` step is step 2 of the job, before the lab and long
   before `--fetch`, and the job runs under `bash -euo pipefail`. That workflow therefore
   stops at step 2 today, on `origin/main`, independently of anything in TZ-27.
2. **`direction_bench.py --props --fixtures --control --sim` exhausts node's default heap
   in this session's environment** — `FATAL ERROR: Reached heap limit Allocation failed`.
   Reproduced identically on a pristine `origin/main` worktree, so it is the environment,
   not the product; with `NODE_OPTIONS=--max-old-space-size=8192` the step passes with
   255 708 checks and 0 failures. Reported because the local gate figure above depends on
   it. Nothing suggests the hosted runner is affected — `Bench gate` #122 is green on
   `f27d5ee`.
3. **`.gitignore`'s comment enumerates the bridge files `backtest_bench.py` writes** and
   is now one name short (`bench/_tgt_bridge.js`). The **rule** is a prefix match
   (`bench/_*`) and covers the new file correctly; only the explanatory list is incomplete.
   `.gitignore` is not in this TZ's scope, so it was not touched.

## Remaining Risks

1. **The measurement has not been taken.** Every number in this report comes from
   synthetic worlds or from a constant sweep. `k*` does not exist yet, and no later TZ can
   cite a result from this one until the archive run happens.
2. **Two blockers now stand between the workflow and that run**, and they are independent:
   the pre-existing red `--selftest` at step 2, and D2/D3 at step 3. Removing either alone
   does not reach `--target`.
3. **The effective k grid is four points, not five, on real data too** — the sweep that
   proves `k = 1.0` unadmittable covers the whole admissible volatility range, so this is
   not a property of the synthetic world.
4. **`marketRegime` can only ever return `range` or `stress` in this mode.** A3 step 3
   registers `btcStats` as `{"volatility": …}` alone; `marketRegime`'s `trend` branch needs
   `r14` and its `z` needs `r7`, so the recorded regime label is degenerate by construction.
   It is recorded only, never gating, so no primary or descriptive depends on it — but a
   reader grouping by it later would be grouping on a field that cannot say `trend`.
5. **`target_raw.json` can carry bare `NaN`** when a pooled arm records zero stop touches
   (Python's `json` reads it back; strict JSON parsers do not). This mirrors
   `stops_raw.json` and the mechanism the TZ asked to be mirrored.

## Commit

One implementation commit, on the branch, already pushed when this section was written:

- `0404286` — `feat(bench): --target measures the 90-day extremum against a continuation target (TZ-27)`
  - `bench/backtest_bench.py` (+555 / −1), `.github/workflows/backtest_bench.yml` (+10).

This report is committed separately, directly to `main` on the `CryptoReports/**` path
(§8). The message it is authorised to carry is
`docs(reports): TZ-27 — continuation-target backtest built, D2/D3 red as registered (TZ-27)`.

## Pull Request

**No pull request exists.** This session has no `gh` CLI and no GitHub token, so it cannot
open one; §8's fallback applies and the Boss opens and merges from the link below in one
action.

- Branch: `claude/tz-27-continuation-target-backtest`
- Compare: `https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-27-continuation-target-backtest`

## CI Execution

No workflow result is claimed, because this session has no credential to read one (§9).
What is established:

- The branch was pushed to `origin` (`0404286`).
- `bench.yml` triggers on `push` to `branches: [main, 'claude/**']`; its `paths-ignore`
  covers `journal/**`, three `analyst/` paths and `**.md` — **not** `bench/**` and **not**
  `.github/workflows/**`. Both changed paths therefore clear its filters.
- `backtest_bench.yml` is `workflow_dispatch` only and does not run on a push.
- `main.yml` still carries a two-entry `paths` **allow-list** (`main.py`,
  `.github/workflows/main.yml`) and no `paths-ignore`, so neither changed path can start
  the bot — verified by reading the file, as §8 requires before the first direct push of a
  session.

The gate's conclusion on this branch is readable on the compare/pull-request page by the
actor who merges.

## Final Repository State

The branch `claude/tz-27-continuation-target-backtest` at `0404286`, pushed and therefore
measured: two files modified, nothing created, renamed or deleted, working tree clean apart
from ignored bench scratch, which was removed.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

`SYSTEM-MAP-CRYPTOCALCUL.md` — revision string `**Revision 2026-09-03-b.**`,
**1915 lines**, MD5 `0b49f7935e9fa098c13c9886d06f7d1b`.

Every file the map's `## 0` table lists, measured on the branch — all four identical to the
required fingerprint, which is the mechanical proof of hard floor item 1 for this TZ:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` | matches |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | matches |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | matches |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | matches |

The two files this TZ authorised, after the change:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 2544 | `fb9464afba2e87450bd3fd11877da9f1` |
| `.github/workflows/backtest_bench.yml` | 140 | `8a994edb5be622d75196e2769c3cf45c` |

Also unchanged, as §4 requires: `.github/workflows/bench.yml`
(`ece76785638496963a2ea068d6a1b9df`), `.github/workflows/main.yml`
(`4d3a83651f7d3a57da19609b9894118e`), and every path under `journal/**` and `analyst/**`
(untouched by this branch).
