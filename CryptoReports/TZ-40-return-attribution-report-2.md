# Implementation Report — TZ-40

**The previous TZ's branch IS merged.** `claude/tz-39-transport-outcome-and-budget`
landed as PR #35 at `9174fbb` (merged 2026-09-12T06:26:32Z). `git merge-base
--is-ancestor 396f961 origin/main` exits 0. This run started from that merge, so the
sequencing clause in TZ-40's header holds. The first attempt under this number stopped on
that clause and is recorded in `CryptoReports/TZ-40-return-attribution-report.md`
(BLOCKED, 2026-09-11). This file is the re-run, named `-report-2` by contract §10 and §13.

## Status

**COMPLETED.** The instrument is built and self-tested offline, and all nine validation
items ran. The archive measurement belongs to a dispatch the Boss runs; the TZ says its
absence is not PARTIAL (§6, §9).

Five points are recorded under `## Deviations`, and none of them was forced to fit:

- **`d_end` is not delivered: the object TZ §3 names does not exist.** TZ §3 defines
  `d_end` as "the `cur` cell the reconciliation already measures". `reconcile()` has no
  `cur` cell, and `coeffs.json` carries no end-of-window price. `--attrib` prints the
  absence on its own line. `d_start_implied` is printed, and is labelled as NOT net of
  `d_end`.
- **`T_end` and `T_start` each move exactly one instant.** They replace one bar's price
  and keep every stamp, instead of cutting the series short. Cutting the series moves both
  instants, because production derives the start from the end. Under that reading the TZ's
  own known-answer world W3 cannot be satisfied: a revert to it turns W3 red with 6 FAILs.
- **The workflow step carries `if: ${{ !cancelled() }}`.** `--verify` exits 1 on every
  `coverage`/`unexplained` class, and a step placed after it would otherwise be skipped on
  exactly the runs this one exists for.
- **The reference population also takes a series observed on the perpetual**, as well as
  a declared `fut:true` asset.
- **Where production was built one bar or more after the archive's newest bar, `T_end` is
  named, not read.** The archive holds no bar at production's end instant.

## Inbound Filing

None. `CryptoTZ/TZ-40-return-attribution.md` carries its canonical filename. It has not
changed since the blocked run: `git diff --quiet 752896c origin/main -- CryptoTZ/
SYSTEM-MAP-CRYPTOCALCUL.md EXECUTOR-INSTRUCTIONS.md` exits 0.

During the session `origin/main` moved from `9174fbb` to `e30c337`
(`journal: 2026-09-12 [skip ci]`). That commit touches `journal/data/2026-09-12.jsonl`,
two files under `journal/out/` and `journal/runs.jsonl`, and nothing this TZ reads or
writes, so the branch was not rebased.

## Scope Executed

**Class: branch TZ** (contract §8). `## 2. Scope` names three files outside
`CryptoReports/**`, and exactly those three were written:
`bench/backtest_bench.py`, `bench/backtest_guard_bench.py` and
`.github/workflows/backtest_bench.yml`. `bench/verify_bench.py`, which `## Touches` names,
was run and not edited. No production file was touched.

## Files Created

None on the branch. This report is created on `main` (contract §8).

## Files Modified

| File | Before (`9174fbb`) | After (`805d5e3`) | `numstat` |
|---|---|---|---|
| `bench/backtest_bench.py` | 4572, `ce38ef842b60699b9ea34dad4f322a29` | 5009, `bcdccf8614f1cecbe4d0c0b78129ddf5` | +452 −15 |
| `bench/backtest_guard_bench.py` | 1986, `1580b9a02b7d4453cd3eebd0b25e33ad` | 2375, `3937226bc0a15b0cf6917ad7393cd827` | +389 −0 |
| `.github/workflows/backtest_bench.yml` | 156, `60ac7db0c4f1960f57d67da8e9beebfe` | 169, `a62abbb50a4775999011d802aea5916b` | +13 −0 |

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### A. `bench/backtest_bench.py`

**A1 — two sites taken out of `reconcile()`, so the new mode CALLS them (TZ §3).**

- `_cell_dv(kind, a, b)` is the comparison site: `pp` → `(a − b)·100`, `abs` → `a − b`,
  and everything else → `100·(a − b)/max(1e-12, |b|)`. `reconcile()` now calls it where it
  used to compute inline, with the same arguments `(archive, production)`.
- `_gap_hours(gen, ends)` is the gap site: it parses `generated_at` and returns hours to
  `max(ends)`. `reconcile()` calls it with every cached end, as before.
- `reconcile()`'s return gains two additive keys. `ref` holds production's rows, the
  result of `--verify`'s own acquisition. `no_build` lists symbols that are cached and in
  production but too short for `f`; `reconcile()` skipped those silently before and still
  does.
- Nothing `--verify` prints or returns changed. `verify_bench.py` is 40 FAIL 0 before and
  after. A scratch probe ran `--verify` on the bench at `origin/main` and on the branch, at
  three gaps, and printed the same verdict line for every gap (`## Pre-existing Issues` 1).

**A2 — `bot_field_stmt(bot_path, field)`.** It cuts, by AST out of `get_token_betas`'s
metric block, every statement that binds one field's local, and compiles them. It derives
the inputs from the statements' own free names; a free name that no `coeffs.json` field
carries raises. For `eff14` the derived inputs are `r14` and `volatility`. This is how
`--attrib` executes production's `eff14` construction without restating it (inv. 21, 38).

**A3 — the mode `--attrib`.** `attrib_run` measures, `report_attrib` prints, `attrib_mode`
decides the exit code. `main()` gains the `--attrib` flag and dispatches it.

What it reads: `reconcile()`, which is `--verify`'s acquisition path and makes one GET of
`GIST_LIVE`, and `load_cache()`, which reads `bench/cache/`. It reads no other artifact
(inv. 62). `--verify`'s comparison-window skip is not applied.

Per coin, the quantities below are measured. The return fields are those `reconcile()`'s
`SPEC` types as `pp`, read from `SPEC` rather than listed: `r7`, `r14`, `r30`.

| Quantity | Computation |
|---|---|
| `f` | `CdBuilder.build(prices, volumes, i)` — the block cut from `get_token_betas`, called |
| `g` | `_gap_hours(generated_at, [this coin's last stamp])`, in hours. Never a numeral |
| Δ | `_cell_dv(kind, r_prod, r_arch)`, which is production − archive in pp |
| `T_end` | `_cell_dv(kind, f(A with the END bar's price replaced by the archive's price at end + g), r_arch)` |
| `T_start` | `_cell_dv(kind, f(A with the START bar's price replaced by the archive's price at start + g), r_arch)` |
| `T_resid` | `Δ − T_end − T_start`, attributed to nothing |
| `d_start_implied` | where the field was derived two-point: `100·(ln(1+r_aligned) − ln(1+r_prod))`, with `r_aligned` = `f` with both instants moved. It is **not** net of `d_end`. Elsewhere this is "not two-point", and the interior sensitivity is printed in its place, in pp |
| ladder | `100·|ln A(t₀+h) − ln A(t₀)|` at the moved start bar `t₀`, for `h ∈ {1, 2, 3, 6, 12, 24}` h and for `g`. `ATTR_H_LADDER` carries TZ §3's rungs |
| `eff14` | production's construction (A2) run at production's `r14` and `volatility`, minus the published `eff14`: a residual of 0 is an exact reproduction. The split of Δ`eff14` substitutes production's inputs one at a time, `r14` then `volatility`. Each input's deviation is printed in its own measure |

Three rules decide what the archive can say:

- **The price the archive knows at instant `t`** is the last bar stamped at or before `t`,
  because a price is stamped at the END of its hour (`_series_from_rows`'s docstring).
  `_attr_asof` returns None where the bar that would carry `t` is absent: `t` is a bar's
  width or more past the last stamp, or inside a hole. A term that needs such a bar is
  printed `—` and names why. It is never read as zero.
- **The window's start bar is located by EXECUTING `f`.** `attrib_start` scales every bar
  up to `j` by 2.0 and bisects `j` on "did the field move". A power of two changes no
  mantissa bit, so the comparison is exact. `window_stats`'s cutoff is not restated.
- **Two-point is derived, not assumed** (`attrib_two_point`, TZ §3). `f` runs on the
  archive and again with ONE interior hour, the window's middle bar, scaled by 2.0. If the
  field does not move, it is two-point on that input.

Populations (TZ §4): **reference** is a declared `fut:true` asset or a series observed on
the perpetual (`## Deviations` 4). The rest is **spot**, split into passing and failing
by the class `reconcile()` gave the coin. Every coin prints in absolute pp in the same
columns, TRX included; no symbol is special-cased in code.

Exit code: a non-zero exit comes from an exception (internal failure) or from zero cells
compared (inv. 22). A cell is compared once Δ is formed. The code does not depend on the
size of any measured term or on the number of fully attributed cells (inv. 49). One
internal check can raise: the archive value `--attrib` reads must equal `reconcile()`'s,
and a difference is `RuntimeError`.

**The mode's printed field list (TZ §9)**, as the offline end-to-end run printed it:

```
ATTRIB — production vs archive, return family: end instant · start instant · residual (TZ-40)
coeffs.json built <generated_at> · gap to the newest archive hour <±h> h · --verify's comparison-window skip is NOT applied here
sign: Δ = production − archive (--verify prints archive − production); Δ, T_end, T_start, T_resid in pp, the reconciliation's own measure; d_start_implied and the ladder in log-% (100·|Δ ln P|)
d_end: NOT AVAILABLE — reconcile() compares no `cur` cell and coeffs.json carries no end-of-window price. d_start_implied is the residual read as a start-instant level deviation, NOT net of d_end
f two-point for <field>  <n> of <m> coins (one interior hour probed, field unchanged)
pop  coin    fld      g h        Δ    T_end  T_start  T_resid  d_start  ladder h=1,2,3,6,12,24,g
<pass|fail|ref> <coin> <field> <g> <Δ> <T_end> <T_start> <T_resid> <d_start_implied> <7 rungs>  · <reason, when a term is not measured>
eff14 — production's own construction (main.py, cut by AST) re-run at production's r14 and volatility; Δ split by substituting r14 then volatility in that order
<pop> <coin> eff14 Δ <x> · reproduction <x> · from r14 <x> · from volatility <x> · inputs r14 <pp> · volatility <%>  · <reason>
coins by population: spot, passing <n> · spot, failing <n> · reference (perpetual) <n>
POPULATION EMPTY: <population> — …                                (only when one spot population is empty)
cells compared (Δ formed): <n> · attributed (all three terms): <n>
  not attributed · <reason>   <n>                                  (one line per reason)
eff14 reproduced exactly (residual 0): <n> of <n> coins where it could be evaluated
cached, absent from production's output: <list|none>
in production's output, not cached: <list|none>
cached and in production, too short for f: <list|none>
```

No line names a cause (TZ §1).

**The derivation result, from the run-time test and not from reading the source.** On
every synthetic archive this session ran, production's `f` read as **two-point for `r7`,
`r14` and `r30`**. That is guard W1 (3 coins × 3 fields; I1 asserts that the derivation
ran on every one) and the offline end-to-end run (`r7` 7 of 7, `r14` 6 of 6, `r30` 7 of
7). The `r14` count is 6 because MIS's `r14` cell ends at "no production value" before
the derivation. This is a result on synthetic inputs. The archive's own reading is what
the dispatched step prints, and none is offered here.

### B. `bench/backtest_guard_bench.py` — section **I**, gate step 14

**The letter is I, read off the file.** Its section headers run A, B, C, D, E, E, F, G, H,
and `grep -n '^# [I-Z]\.'` returned nothing before the edit. The last letter the file
carries is H, so the next is I. Counting sections would say J, because two sections share
E (TZ §5).

Every assertion is one `ok(...)` call, counted where it compares (inv. 43). **No
tolerance is used anywhere in the section.** Every equality is exact, because the
construction makes the two sides the same floating-point expression on the same operands:

- production's rows are made by production's own `f` on a moved or rescaled copy of the
  archive;
- offsets are whole bars (`I_SHIFT = DAY // HOUR`, one day of bars);
- a flattened stretch carries copies of one float;
- the rescale is ×2.0, which moves no mantissa bit.

| World | Construction | Asserted | Count |
|---|---|---|---:|
| W1 (I1) | two series identical, `g = 0` | all four terms read 0.0 on each of 9 cells · every cell attributed · the instrument saw **0** non-zero cells · `g` = 0 on every coin · `eff14` reproduces exactly on 3 coins · the derivation ran on every coin and field | 16 |
| W1 planted (I2) | the same world with BBB `r7` +0.05 and CCC `eff14` +0.5 | the instrument saw **exactly 1** non-zero cell, and it is (BBB, `r7`) · Δ ≠ 0 · both instant terms 0.0 · `T_resid == Δ` · CCC's `eff14` is NOT reproduced · the other two still are | 7 |
| W2 (I3) | production ends one day earlier, and every field's start stretch is flat across the shift | per field: Δ ≠ 0 · `T_end == Δ` · `T_start == 0.0` · `T_resid == 0.0` | 12 |
| W3 (I4) | the same shift, with the END stretch flat instead | per field: Δ ≠ 0 · `T_start == Δ` · `T_end == 0.0` · `T_resid == 0.0` | 12 |
| W4 (I5) | identical instants. (a) production scaled whole by 2.0; (b) scaled from half the shortest window on | (a) all four terms 0.0 per field — a return is a ratio, so a uniform scale is invisible to it · (b) per field Δ ≠ 0, both instant terms 0.0, `T_resid == Δ` · `eff14` still reproduces | 13 |
| W5 (I6) | empty cache, through `main()` | exit non-zero · no result printed | 2 |
| W6 (I7) | `attrib_two_point` on synthetic callables | two-point callable: start located at its own first bar, derived two-point · path-dependent callable (window mean): start located, derived NOT two-point · a callable reading no earlier bar: no start | 5 |
| populations, end to end (I8) | PAS, FAI (planted `r7`), FUT (declared, perpetual) and the extremes below | spot passing = {LAT, MIS, PAS, SHO} · spot failing = {FAI, VZ0} · reference = {FUT} · through `main()`: exit 0, the population line, the cell-count line with the measured figures, and the `d_end: NOT AVAILABLE` line | 7 |
| extremes (I9) | TZ §8 item 9 — see Validation 9 | 17 assertions | 17 |
| host audit (I10) | every URL the section's stub received | the set is exactly `{gist.githubusercontent.com}` · non-empty | 2 |
| zero guard | — | the section compared something | 1 |
| **total** | | | **94** |

### C. `.github/workflows/backtest_bench.yml`

One step is added after "Сверка восстановления с живым coeffs.json": `name: Разложение
расхождения доходностей (--attrib)`, `if: ${{ !cancelled() }}`, `run: cd bench && python
backtest_bench.py --attrib --bot ../main.py --html ../index.html`. It runs under the
job's `shell: bash -euo pipefail {0}`. It carries a six-line comment in Russian (contract
language exception) and no `continue-on-error`. Nothing else in the file changed.

## Validation

Baselines were taken on `9174fbb` before any edit: guard `checks run: 373 FAIL 0`
(E 32 · F 29 · G 63 · H 107), `verify_bench.py` `checks run: 40 FAIL 0`.

**1. `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py`** → exit 0.

**2. `python3 bench/backtest_guard_bench.py`** → exit 0, `checks run: 467   FAIL 0`.
Section **I**, 94 comparisons (`I. attribution: 94 comparisons`). E, F, G and H are 32,
29, 63 and 107, the same as before. Step 14 went from 373 to **467**, and the delta of 94
is section I's own count.

The gate total, term by term. `bench.yml` has 14 steps.

| Term | Figure | Source |
|---|---:|---|
| the 12 steps other than 4 and 14 | 1 335 601 | TZ-39 report's arithmetic (1 335 964 − 40 − 323). **Not re-measured.** Among files a `bench.yml` step runs, only `verify_bench.py` and `backtest_guard_bench.py` import `backtest_bench.py`. `grep -ln backtest_bench bench/*.py bench/*.js analyst/*.sh` also lists `exhaustion_calib.py` (a `calib.yml` file) and the bench itself |
| step 4, `verify_bench.py` | 40 | measured before and after |
| step 14, `backtest_guard_bench.py` | 467 | measured; the baseline was 373 |
| **total** | **1 336 108** | the measured baseline was 1 336 014; delta **+94** |

**3. `python3 bench/verify_bench.py`** → exit 0, `checks run: 40   FAIL 0`, before and
after, including the run on the tree restored after the negative controls.

**4. Identity control (inv. 45).** W1 reads 0.0 on all four terms of all 9 cells, and the
instrument reports seeing **0** non-zero cells. With one difference planted, it reports
seeing **exactly 1**, the planted cell, whose Δ sits whole in `T_resid`. That is 16 + 7
assertions.

**5. Zero-cell refusal.** W5, empty cache through `main()`: the exit code is non-zero and
nothing was printed. The stop comes from `reconcile()`'s own zero-coin exit, before any
attribution.

**6. `--attrib` end to end, offline, on a synthetic cache directory.** Guard I8 runs it
inside the gate. A scratch driver (`/tmp/tz40/e2e.py`, not committed) runs the same world
through `main()` and prints everything:

```
$ unshare -rn sh -c 'ip -o link | cut -d: -f2; python3 /tmp/tz40/e2e.py "$PWD"'
 lo
…
coins by population: spot, passing 4 · spot, failing 2 · reference (perpetual) 1
cells compared (Δ formed): 20 · attributed (all three terms): 16
  not attributed · no production value                                1
  not attributed · production's end instant is outside the archive    3
  not attributed · window reaches the archive's first bar             1
eff14 reproduced exactly (residual 0): 5 of 5 coins where it could be evaluated
cached, absent from production's output: NOP
in production's output, not cached: NOC
cached and in production, too short for f: TIN
[e2e] exit code: 0 · URLs requested: ['https://gist.githubusercontent.com/…/raw/coeffs.json']
```

**No socket was opened.** The run was inside a network namespace whose only interface is
`lo`, and the one URL requested went to the stub. The whole guard was also run inside
`unshare -rn`: `checks run: 467 FAIL 0`, exit 0. I10 audits the stub's record in every
gate run. The limit is the one TZ-39 recorded: the audit only sees reaches through
`requests`, and the namespace run covers this run and not future edits.

Run time at archive scale, synthetic (`/tmp/tz40/timing.py`): 30 coins × 26 280 hourly bars
→ `wall 18.5 s`, exit 0, `cells compared (Δ formed): 90 · attributed (all three terms): 90`.

**7. YAML.** `yaml.safe_load` parses the file. Step 16 is `Разложение расхождения
доходностей (--attrib)` with `if: ${{ !cancelled() }}`, and no step anywhere carries
`continue-on-error`. The command is `python backtest_bench.py --attrib --bot ../main.py
--html ../index.html`, and `--attrib` is the argparse flag. `git diff 9174fbb 805d5e3 --
.github/workflows/backtest_bench.yml` shows one hunk of **13 added lines, 0 removed**: the
comment block and the step. The step exists and runs the command above after the
`--verify` step. Whether it executes on a runner is a dispatch and is not forecast here
(inv. 54).

**8. `git diff --name-only origin/main 805d5e3 -- . ':!journal'`** →
`.github/workflows/backtest_bench.yml`, `bench/backtest_bench.py`,
`bench/backtest_guard_bench.py`: exactly three files. The `journal/**` exclusion only
removes `e30c337`'s journal-only commit, which is on `main` and not on the branch. The
four `## 0` hashes measured after the change are all unchanged:

- `index.html` 3799 `4e71da9badca3ccae85b656fdc3773e8`
- `main.py` 518 `0e3ead8c300d2ee6783303c4bf2fb6b5`
- `catalysts.json` 17 `f9b2dd4a3594134b2b7b603de19075c3`
- `bench/exhaustion-calibration.txt` 175 `3b8730b254467c9df4c0a845a0f3cfb3`

**9. Extremes, each with its own assertion (guard I9), all green:**

| Extreme | Construction | Assertion |
|---|---|---|
| archive shorter than the longest window | SHO: the longest window's bars less one day | the longest-window cell is named "window reaches the archive's first bar" and not attributed · the shorter windows are attributed |
| … and shorter than `f` accepts | TIN: one day of bars | named in `no_build`; no cell is invented |
| production value missing | MIS: no `r14` in its row | the cell is named "no production value", Δ not formed · the `eff14` reproduction names the missing input |
| `volatility` zero | VZ0: production's `volatility` = 0.0 | the `eff14` reproduction returns none, "production's construction yields no value", with no division |
| cached, absent from production | NOP | named |
| in production, not cached | NOC | named |
| production built past a coin's archive | LAT: archive ends one day before `generated_at` | `g` = +24.0 carried · every `T_end` named "production's end instant is outside the archive", `T_start` measured |
| **`g` beyond `--verify`'s comparison window** | GPA and GPB: `generated_at` one day after the newest archive bar | `--verify`'s skip is active (`skip` non-empty) · every cell still compared, `g` = +24.0 · `T_start` measured on every cell · `T_end` named on every cell · `--attrib` exits 0 |
| archive later than production by a day | W2's world, `g` = −24.0 | every cell attributed, `g` carried |
| the failing coin | FAI: `r7` +0.05 | its Δ sits whole in `T_resid` |

**Negative control (contract §9).** This TZ touches a workflow and gate step 14. Each
variant mutated the committed `bench/backtest_bench.py` at `805d5e3`, the guard was run,
and the file was restored with `git checkout --`; `git status --porcelain` printed 0
lines after each variant.

| Variant | Mutation | Guard | Red on |
|---|---|---|---|
| a | `T_end` by **truncation** — `fn(P, V, j_e)`, the TZ §3 Computation column read literally | exit 1, **FAIL 6** | W3 (I4): `T_end reads zero` and `T_resid reads zero`, on each of `r7`, `r14`, `r30` |
| b | Δ with `--verify`'s orientation, `_cell_dv(kind, a, b)` | exit 1, **FAIL 12** | W2 and W3: the carrying term and `T_resid`, per field |
| c | start instant moved against `g` (`pts[s] − gms`) | exit 1, **FAIL 12** | W2 `T_start` and `T_resid`, W3 `T_start` and `T_resid`, per field |
| d | exit keyed on cells ATTRIBUTED instead of compared | exit 1, **FAIL 1** | I9: "a measurement, so --attrib exits 0" |

After all four: guard exit 0, `checks run: 467   FAIL 0`, and HEAD is still
`805d5e38d20d561448ab6c379e77ac4886e3abb0`. The scratch drivers are `/tmp/tz40/neg.py`,
`e2e.py`, `timing.py` and `verify_probe.py`, outside the repository.

## Test Results

| Command | Where | Result |
|---|---|---|
| `python3 -m py_compile …` | local | exit 0 |
| `python3 bench/backtest_guard_bench.py` | local | exit 0, `467 FAIL 0` (baseline `373 FAIL 0`) |
| the same, inside `unshare -rn` | local | exit 0, `467 FAIL 0` |
| `python3 bench/verify_bench.py` | local | exit 0, `40 FAIL 0` (baseline `40 FAIL 0`) |
| e2e `--attrib` through `main()`, inside `unshare -rn` | local | exit 0; 20 compared, 16 attributed; populations 4 / 2 / 1 |
| timing, 30 × 26 280 | local | exit 0, 18.5 s, 90 of 90 attributed |
| negative controls a / b / c / d | local | FAIL 6 / 12 / 12 / 1, each restored to `467 FAIL 0` |
| `Bench gate`, push | runner, run `34744917873` | **success**, all 19 job steps |
| `Bench gate`, pull_request | runner, run `34744919491` | **success**, all 19 job steps |

## Deviations

**1. `d_end` is not delivered, and `d_start_implied` is printed NOT net of it.** TZ §3:
"`d_end` — the end-level deviation, i.e. the `cur` cell the reconciliation already
measures for that coin. It agrees to 0.47 % worst across the spot set". Three readings,
all measured:

- `reconcile()`'s `SPEC` lists `min_price`, `max_price`, `min30`, `max30`, `volatility`,
  `vol7`, `r7`, `r14`, `r30`, `eff14` and `vol_ratio`. It has no `cur`.
- `CD_FIELDS` has no `cur` either.
- `main.py` publishes `{"generated_at", "btc", "analysis_data": results}`. Each row carries
  `price_pos`, `min_price` and `max_price`, but no current price.

The 0.47 % the TZ quotes is the worst of the four LEVEL cells (map §7). `cur` could be
recovered as `min + price_pos·(max − min)/100`, but that restates production's formula
in the bench, which inv. 21 and 38 ban. Adding a `cur` field to `coeffs.json` needs
`main.py`, which §6 closes. No code this TZ authorises can produce `d_end`.

The mode prints the absence on its own line. `d_start_implied` is computed from TZ §3's
own identity, `log(1+r) = ln P(end) − ln P(start)`. It is therefore "d_start − d_end", and
it equals the start-level deviation only where `d_end` is zero, which the output states
beside it.

**2. `T_end` and `T_start` move ONE instant each, by replacing a bar's price; they do not
truncate.** TZ §3's Computation column reads "`f` re-executed on `A` truncated so the
window ENDS at production's end instant". Production's `window_stats` derives the window
start from its end (`cutoff = t_end − days·86400·1000`, `main.py:153-154`), so truncating
moves both instants. `T_start` then moves the start a second time, and the start is
counted in two terms.

TZ §5's must-read table decides between the two readings. W3 requires `T_end` = 0 where
only the start differs. Under truncation `T_end` carries the start's move, and W3 cannot be
satisfied by any construction. Negative-control variant **a** is the literal reading, and
it turns W3 red with 6 FAILs.

The "What it is" column agrees with the table: "what the end instant alone can produce",
"what the start instant alone can produce". The table was implemented, and the collision
is recorded here so the Architect can overrule it in one line.

**3. The workflow step carries `if: ${{ !cancelled() }}`.** `verify_against_live`
returns `1 if (hard or R["never"])`, and the reconciliation of 09.09 held 35 `unexplained`
cells. Under the job's default a step after a failed step is skipped. Unconditioned, the
step would not execute on any run where `--verify` is red, which is every run on which
there is something to attribute.

The condition is not `continue-on-error`. A failed `--verify` still fails the job, and a
failed `--attrib` fails it too. It sits on the added step only. If the TZ meant "after" to
include "only when `--verify` passed", removing this one line restores that.

**4. The reference population takes a series OBSERVED on the perpetual as well as a
declared `fut:true` asset.** TZ §4 names "the five `fut:true` assets" and gives the reason
that their cells carry the `venue-basis` licence. Since TZ-34 that licence is granted off
the observed venue (`_venue_licence(cov)`), not off the declaration. A coin not declared
`fut:true` but cached on the perpetual carries the licence and would otherwise be pooled
into spot, against §4's own reason. `_attr_pop` reads both and prints which one applied.

**5. Where production was built one bar or more after a coin's last archive bar, `T_end`
is named, not measured; the exit code keys on cells COMPARED.** TZ §8 item 9 says a coin
whose `g` exceeds `--verify`'s window "must still attribute". `--verify` skips only when
production is more than 3 h LATER than the archive (`gap > 3`), and then production's end
instant lies past the archive's last bar. No archive price exists there to substitute.

`--attrib` still forms Δ, carries `g`, measures `T_start` and the ladder, and names
`T_end` "production's end instant is outside the archive". It never reads it as 0. A first
version exited non-zero on zero cells fully attributed, and the I9 world refuted it:
§5 says "zero cells compared". Variant **d** proves the guard catches a return to it.

## Pre-existing Issues

Each was measured on the bench at `origin/main` (`ce38ef842b60699b9ea34dad4f322a29`). The
branch reproduces it unchanged, and none was acted on.

**1. `--verify`'s comparison-window skip does not reach its verdict, and it is one-sided.**
The world: three coins, BBB `r7` +5 pp.

```
gap  -24.0 h | exit 1 | skip announced: False | НЕ СВЕРЯЛОСЬ line: [] | BBB r7 classed unexplained
gap   +0.5 h | exit 1 | skip announced: False | НЕ СВЕРЯЛОСЬ line: [] | BBB r7 classed unexplained
gap  +30.0 h | exit 1 | skip announced: True  | НЕ СВЕРЯЛОСЬ (разрыв во времени 30.0 ч): r7, r14, r30, eff14 | BBB r7 classed unexplained
```

- At +30 h `--verify` prints that the return fields were NOT compared, and in the same run
  classes BBB's `r7` `unexplained` and exits 1. In `reconcile()`, `over` is computed with no
  reference to `skip`; `skip` only feeds `never` and the printed lines. `--target`'s gate
  reads the same classes. Map §7 and §10 say "a gap large enough to skip them would have
  hidden this entirely", but the code would have classed those cells and failed.
  `verify_bench.py` case 5 ("big gap still exits 0") passes only because its big-gap world
  has no disagreeing return.
- The skip reads `gap > 3`, so an archive later than production by any amount is compared
  with no announcement.

Which behaviour is intended is the Architect's decision.

**2. TZ-40 §3 names a `cur` cell that does not exist** (`## Deviations` 1). Map §3.10 lists
`cur` among the fields the AST-cut block computes. That is true of the block, but `cur` is
neither in `CD_FIELDS` nor published.

**3. Map §3.10's mode list does not carry `--attrib`**, and TZ-39 had already found
`--fetch-funding` and `--regime-gate` missing from it. The map is the Architect's.

**4. `_gap_hours` inherits `time.mktime(...) − time.timezone`.** That is exact only where
local time has no daylight saving. The runner and this session are UTC (`time.timezone
0`, `time.daylight 0`). The site is now shared by `--verify` and `--attrib`, so one repair
would fix both.

**5. `backtest_bench.yml`'s artifact list does not carry `--attrib`'s output.** The TZ
forbids any other change to that file. The output therefore lives in the job log only.

## Remaining Risks

1. **Below one bar of `g`, both instant terms are exactly zero by construction.** An hourly
   archive holds no price between two stamps: moving the end or the start by less than a
   bar lands on the same bar, and Δ goes whole to `T_resid`. The 09.09 reconciliation
   recorded a gap of 0.8 h. This is a property of the archive's resolution, not a forecast
   of the dispatch; the ladder column is there to show the hour-scale sensitivity beside
   it.
2. **At one bar or more of positive `g`, no cell is fully attributed** (`## Deviations` 5).
   The step then prints Δ, `T_start`, the ladder and `g`, and exits 0.
3. **`d_start_implied` is not net of `d_end`** until something publishes an end-of-window
   level.
4. **The two-point probe perturbs ONE interior hour, the window's middle bar**, as TZ §3
   specifies. A field reading a sparse subset of interior hours that excludes the middle
   one would read as two-point. The count printed beside it covers only the cells that
   reached the derivation.
5. **Run time was measured on a synthetic archive at scale** (18.5 s for 30 × 26 280),
   not on the runner's cache.
6. **`if: ${{ !cancelled() }}` also runs the step after an earlier failure**, a failed
   fetch included. There `--attrib` stops at `reconcile()`'s zero-coin exit, and the job
   was red already.

## Commit

The implementation is on `claude/tz-40-return-attribution`. It was pushed before this
report was written, so its hash is a measurement:
`805d5e38d20d561448ab6c379e77ac4886e3abb0`.

```
TZ-40: attribute the production/archive return gap into end-instant, start-instant and residual terms
```

That is the TZ's `## Commit Message` verbatim, followed by the `Co-Authored-By` trailer.
Contents: the three files under `## Files Modified`.

This report's own commit carries the message

```
docs(reports): TZ-40 — return gap split into end instant, start instant and residual (TZ-40)
```

Nothing is stated here about its outcome: it has not happened as this section is written
(inv. 54).

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/37** —
`claude/tz-40-return-attribution` → `main`. Not merged. Merging is the Boss's decision
after the Architect's audit.

The body first named this report's path without `-2`. `gh pr edit` failed on the
Projects-classic deprecation, so the body was corrected through `PATCH
/repos/…/pulls/37` and read back.

## CI Execution

`Bench gate` ran twice on the runner against `805d5e3`, and both runs concluded
**success**:

| Run | Event | Conclusion |
|---|---|---|
| `34744917873` | `push` | **success** |
| `34744919491` | `pull_request` | **success** |

All 19 job steps of both runs are `success` (`gh run view <id> --json jobs`). That
includes job step 9, `verify_bench.py` (gate step 4), and job step 19,
`backtest_guard_bench.py` (gate step 14). The runner's check counts live only in the job
logs, which were not read, so 40 and 467 are local figures and are not offered as runner
ones.

`calib.yml` did not run, because its `paths` filter names only `bench/exhaustion_calib.py`
and itself. `main.yml` did not run, because its allow-list names only `main.py` and
itself. `backtest_bench.yml` is dispatch-only and was not dispatched: it needs the archive,
which §6 forbids this session to fetch.

## Final Repository State

**NOT IN EFFECT UNTIL MERGED.**

This session leaves the branch `claude/tz-40-return-attribution` at
`805d5e38d20d561448ab6c379e77ac4886e3abb0`: pushed, green on both hosted runs, and
carrying exactly the three modified files. Until PR #37 is merged, `bench/backtest_bench.py`,
`bench/backtest_guard_bench.py` and `.github/workflows/backtest_bench.yml` on `main` are the
TZ-39 versions.

The worktree was left clean: `git status --porcelain` printed nothing after the last
negative control, and `__pycache__` was removed after every run. The scratch files are under
`/tmp/tz40/`, outside the repository.

## Fingerprints

Map revision string, from its `## 0. Fingerprint` block (line 17):
`**Revision 2026-09-10-a.**`

The seven content anchors of TZ §0, each matched as an exact substring with `grep -cF`.
Each occurs twice, once in the map's anchor table and once at its site.

| Anchor | Matched substring |
|---|---|
| revision | `**Revision 2026-09-10-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` |

| File | Lines | MD5 | Against TZ §0 |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2590 | `86dac370fb4e3e096cb24e23dec1aa1c` | — |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` | exact |
| `ANALYST-INSTRUCTIONS.md` | 2615 | `e945ac9e93c03e72f551bc7972541148` | — |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | exact |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | exact |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | exact |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | exact |
| `CryptoTZ/TZ-40-return-attribution.md` | 296 | `5292d8927275827beb1695613a301b33` | — |

The two benches in TZ §0's second table, which states their figures before TZ-39:

| File | TZ §0 (pre-TZ-39) | Measured at start (`9174fbb`, TZ-39 merged) | After (`805d5e3`) |
|---|---|---|---|
| `bench/backtest_bench.py` | 4555, `deac9dd8a53f2047c25c2d6fb24f09b4` | 4572, `ce38ef842b60699b9ea34dad4f322a29` | 5009, `bcdccf8614f1cecbe4d0c0b78129ddf5` |
| `bench/backtest_guard_bench.py` | 1726, `ce08dd99edebfa90d8fce3dd6b7ba472` | 1986, `1580b9a02b7d4453cd3eebd0b25e33ad` | 2375, `3937226bc0a15b0cf6917ad7393cd827` |

The figures measured at start match TZ-39's report exactly, which is the difference TZ §0
said to expect; the gate does not block on benches. The same holds for the other two files
this TZ names: `bench/verify_bench.py` (under `## Touches`) is 388 lines,
`06036d8c3d39ccec6be21d2158ef3ce1`, unchanged; `.github/workflows/backtest_bench.yml` went
from 156 lines, `60ac7db0c4f1960f57d67da8e9beebfe`, to 169, `a62abbb50a4775999011d802aea5916b`.
