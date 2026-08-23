# Implementation Report — TZ-13

**Live wiring of the exhaustion measure, and the threshold re-registered on the list median.**

## Status

**COMPLETED.**

All three stages implemented, all ten validation items run, and **both workflows
executed on a GitHub runner** — `Bench gate` green over 12 steps, and
`Calibration (archive)` green with every admissibility condition passing. The
calibration derived

```
DAY_RANGE_ABNORMAL = 1.39
```

and **it was not adopted.** TZ §3 forbids a consumer at this revision, so the
constant exists only in `bench/exhaustion-calibration.txt`. `index.html` declares
no such constant, `abnormal` is still hardcoded `false`, and nothing on any
surface compares against it.

The number is the correction the TZ predicted. TZ-11 measured the COIN-DAY p90 at
1.59 and rejected it against a hand-written floor of 1.60. On the object
`listExhaustion` actually thresholds — the LIST MEDIAN — the p90 is **1.39**,
materially lower, exactly as inv. 47 says it must be: averaging correlated members
strips idiosyncratic dispersion. The old floor of 1.60 sits above even this run's
null p99 (1.6271), which is the concrete form of the TZ's finding that the floor
was wrong before any data existed.

Previous TZ's branch: **merged.** TZ-12 reached `main` as PR #12 (`cd77541`), and
`origin/main` at the start of this task was `0d25baf`, two documentation commits
beyond it. This work is not stacked on an unmerged base.

## Inbound Filing

Nothing was moved or renamed. `CryptoTZ/TZ-13-live-exhaustion-and-median-calibration.md`
was already on `origin/main` under its canonical name when the trigger arrived; it
was found after `git fetch --all --prune`, not in the session's initial clone
listing.

The clone WAS shallow (`git rev-parse --is-shallow-repository` → `true`) and was
deepened with `git fetch --unshallow` before anything historical was assessed:
312 commits after deepening.

### Fingerprint gate (contract §5, TZ §0) — PASS

Compared against `origin/main`, never local `main`.

| Anchor | Present |
|---|---|
| `**Revision 2026-08-23-c.**` | yes |
| `### 3.12 Direction engine — veto cascade` | yes |
| `### 3.16 List exhaustion — the day-range measure` | yes |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | yes |
| `48. **A bench that builds its own input proves the function, not the wiring.**` | yes |

Baseline files at `origin/main`, measured with `git show origin/main:<f>`:

| File | Lines | MD5 | TZ expects | Match |
|---|---:|---|---|---|
| `index.html` | 3656 | `64acaaa59f2ed96d568714d2813d20f9` | 3656 / `64acaaa5…` | yes |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | 506 / `1a5a5d98…` | yes |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` | 11 / `021dd2c9…` | yes |

Gate baseline measured from a `git worktree` at `origin/main`, not assumed:
**1 250 354** checks over 12 steps, all exit 0. Reproduces the TZ's figure exactly.

## Scope Executed

All three stages, plus the fixture update Stage A authorises.

- **Stage A** — the row contract, one parse site per quantity.
- **Stage B** — the inv. 48 wiring section in `bench/exhaustion_bench.js`, with
  its positive control.
- **Stage C** — `bench/exhaustion_calib.py` rewritten onto the date / list-median
  object, with the measured-ρ null, the known-answer control and the derived
  admissibility rule.

Nothing was adopted. `DAY_RANGE_ABNORMAL` does not appear in `index.html`,
`abnormal` is still hardcoded `false`, `reg.day` is still unreferenced, and no
threshold, colour or new on-screen word was added.

## Files Created

None. `bench/exhaustion-calibration.txt` is written and committed by the
`calib.yml` runner, not by this session.

## Files Modified

| Path | Lines changed |
|---|---|
| `index.html` | +19 / −9 |
| `bench/exhaustion_bench.js` | +177 / −1 |
| `bench/exhaustion_calib.py` | +785 / −155 |
| `bench/prot_bench.js` | +14 / −2 |

`main.py`, `catalysts.json`, `journal/**` and `.github/workflows/**` were not
touched.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### Stage A — the row contract

`update()` now parses each of the three range fields exactly once, onto the row,
immediately after the `nopair` early return and before the dead-market test:

```js
row.cur  = parseFloat(coin.lastPrice);
row.hi24 = parseFloat(coin.highPrice);
row.lo24 = parseFloat(coin.lowPrice);
```

They are assigned for **every** row that has a ticker, `fut:true` included: the
venue rule stays in `listExhaustion` alone (inv. 41).

Consumers rerouted:

| Site | Before | After |
|---|---|---|
| `update()`, `sideOn` branch | `parseFloat(coin.lastPrice)` / `highPrice` / `lowPrice` | `row.cur`, `row.hi24`, `row.lo24` |
| `boardHtml`, header | `var cur = parseFloat(coin.lastPrice)` | `var cur = row.cur` |
| `boardHtml`, §3.17 row 2 | `dayRangeRatio(parseFloat(coin.highPrice), parseFloat(coin.lowPrice), cur, …)` | `dayRangeRatio(row.hi24, row.lo24, cur, …)` |
| `update()`, off-list filter | `rangePos(orow.cd, parseFloat(orow.coin.lastPrice))` | `rangePos(orow.cd, orow.cur)` |
| `update()`, dead-market card | `var frozenP = parseFloat(row.coin.lastPrice)` | `var frozenP = row.cur` |
| `update()`, card header | `var cur = parseFloat(coin.lastPrice)` | `var cur = row.cur` |

The last three are **not** in the TZ's Stage A table; see `## Deviations`.
`coin.priceChangePercent` and `coin.quoteVolume` were not touched.

### Stage B — the wiring section (inv. 48)

New section **H** in `bench/exhaustion_bench.js`, inside the gate. It brace-matches
`listExhaustion` and `update()` out of `index.html`, collects the fields the reader
takes off its row (first level, plus the second level where the source reads one)
and the fields the producer writes (the `var row = { … }` literal's keys plus every
`row.<ident> =` assignment in that body), and asserts inclusion with one check per
field read. A nested read is satisfied by its ROOT being written, because `update()`
assigns `row.t` and `row.cd` whole and `fut` / `volatility` are fields of those
objects, not of the row.

On the candidate:

```
update() writes: cd, coin, cur, dec, hi24, idx, lo24, sc, state, t, vd
listExhaustion reads: cd, cd.volatility, cur, hi24, lo24, t, t.fut
```

Zero reads or zero writes is a failure, not a pass (inv. 22). The brace matcher
tracks strings, both comment forms and regex literals, and distinguishes a regex
from a division by the last significant character — a wrong guess there swallows
the rest of the function and would report a producer with no fields at all, which
inv. 22 then turns into a failure rather than a silent pass.

`READERS` is a list; a second reader is added by naming it. Only `listExhaustion`
is wired at this revision.

### Stage C — the calibration

`bench/exhaustion_calib.py`, rewritten. Not in `bench.yml`; it runs through
`calib.yml`, which was **not** edited. No fetch happened in this session.

- **C1 — the object is a DATE.** `coin_days` returns its day key (and the
  observation count behind the volatility estimate) with every tuple; days are
  joined across the 25 spot assets by that key; each date's rows are built in
  production's own contract and handed to **production's `listExhaustion`**.
  `JS_CUT = ["has", "sigmaDay", "dayRangeRatio", "listExhaustion"]`. The median,
  the count and the quorum are production's. Dates below quorum come back `null`
  and drop out, and the count of those is reported.
- **C2 — the statistic is unchanged:** the 90th percentile, numpy linear
  interpolation, rounded to two decimals.
- **C3 — the null, simulated in the same run.** ρ is **measured**, not assumed:
  per date, the mean pairwise Pearson correlation of hourly **simple** returns
  (the quantity `main.py`'s `volatility` is itself the std of) over the same
  trailing 90-day window, across that date's contributing coins; each date's null
  is then simulated at its own ρ through a single common factor. The simulated day
  is a **continuous-time** range: within each step the extremes are drawn from the
  Brownian-bridge law,
  `M = (a + b + sqrt((b−a)² − 2v·ln U))/2`, and its mirror for the minimum. The
  bridges on disjoint steps are independent given the skeleton, so the maximum over
  steps is exact in distribution rather than a discretisation that improves with
  more steps. The ratio is formed by **production's `dayRangeRatio`** from the
  simulated path's own high, low and last value, through the same node hop. The
  sampling error of the 90-day σ estimate enters as a multiplicative factor with
  `sd(σ̂/σ) = sqrt(1/(2m))` on the estimator's own observation count `m` — the
  admissible form the TZ names, recorded as such. The replica count escalates until
  the bootstrap Monte-Carlo standard error of the null p90 is below 0.01; the script
  prints it and **fails** if it exceeds 0.01. Seed `20260823`, recorded.
- **C4 — the known-answer control**, offline, inside `--selftest`, before the
  archive is touched. Reported below.
- **C5 — the admissibility rule.** Extracted into `admissibility()` so the
  self-test can feed it values and watch it refuse them. **No numeric band on the
  constant appears anywhere in the file**; conditions 2 and 3 are read off the null
  computed in the same run. Any FAIL → non-zero exit, no constant, no production
  change.
- **C6 — the record**, `bench/exhaustion-calibration.txt`, written and committed by
  `calib.yml`. The machine-readable line `DAY_RANGE_ABNORMAL = X.XX` is emitted
  **if and only if** every condition passes; a refused run prints no such line at
  all, so a later bench cannot read an unadopted number off the file.

### Fixture update (authorised by TZ §2 Stage A)

`bench/prot_bench.js` builds its own rows and hands them to `boardHtml`, so the row
it builds had to become the new row. One helper, `rowRange(row)`, applies
production's own assignment sequence to a fixture row **from the ticker object that
fixture already carries**:

```js
row.cur  = parseFloat(row.coin.lastPrice);
row.hi24 = parseFloat(row.coin.highPrice);
row.lo24 = parseFloat(row.coin.lowPrice);
```

It is called in `armCtx` and again in `sqzBoard` after that function overrides
`row.coin.highPrice` / `lowPrice`. No new number was introduced and no expectation
string was changed. `prot_bench.js`'s check count is **unchanged at 372**.

`verify_board.js` and `board2_bench.js` needed no change — they call production
math directly and never `boardHtml`. `render_bench.py` needed no change — it runs
the real `update()`, so production writes the fields itself.

## Validation

Every item the TZ lists was run. Item 7 is the runner run; everything else is local
unless stated.

### 1. Compiles and guards — PASS

```
py_compile OK (main.py, exhaustion_calib.py)
node --check index.html <script> OK
node --check exhaustion_bench.js OK
node --check prot_bench.js OK
```

ES5 guard over every added line of `index.html` (arrow functions, template
literals, `let`/`const`/`class`, spread, `for..of`, `async`/`await`, optional
chaining, nullish coalescing): **19 lines checked, 0 violations**; the guard fails
on zero lines checked.

Cyrillic guard — no raw Cyrillic inside an added JS string literal: **995 lines
checked across 4 files, 0 violations**; fails on zero lines checked. Added lines
carrying any Cyrillic at all, comments included: **0** (contract §10 keeps new code
comments in English).

### 2. Stage A, one parse site — PASS

Every remaining occurrence of `lastPrice`, `highPrice`, `lowPrice` in the whole of
`index.html`, with line and enclosing function:

```
index.html:1018   refreshMarketData  ...Math.round(parseFloat(btcObj.lastPrice));
index.html:3097   update             var btc    = parseFloat(btcObj.lastPrice);
index.html:3201   update             row.cur  = parseFloat(coin.lastPrice);
index.html:3202   update             row.hi24 = parseFloat(coin.highPrice);
index.html:3203   update             row.lo24 = parseFloat(coin.lowPrice);
```

**Exactly one parse site per field per row survives** — 3201/3202/3203. The two
others are named and justified: both read `btcObj.lastPrice`, the BTC index
ticker. BTC is the regime measurer, is not a member of `rows[]`, and never reaches
`listExhaustion`; it is outside the row contract by construction, not by omission.

### 3. Stage A, the measure reaches the list — PASS

Rows built by the **real `update()`** (stronger than assembling the sequence by
hand), rendered through the real DOM path, on both revisions:

| Scenario | candidate `n` | candidate `median` | baseline `n` | baseline `median` |
|---|---:|---|---:|---|
| 25 spot + 3 `fut:true` | **25** | **0.6234115092938981** | 0 | `null` |
| one ticker missing `highPrice` | **24** | **0.6353758143754109** | 0 | `null` |
| only three spot rows | 3 | `null` (below quorum 8) | 0 | `null` |

`n` is 25 and the median is a number, as the TZ requires. Every row that has a
ticker carries `cur` / `hi24` / `lo24` (28 of 28 in the full scenario); zero rows
with a ticker lack them. The baseline returns `{median: null, n: 0}` in **every**
case — Defect 1, reproduced.

### 4. Stage A, no-regression — PASS

**Identity first (inv. 45).** `prot_bench.js`'s unconditional identity run compares
6 boards against `index.html` itself and reports zero differences before any of the
below is offered as evidence.

**`prot_bench.js` scenario set against `origin/main`:** `node bench/prot_bench.js
index.html <origin/main index.html>` → **PASS 2095, FAIL 0**, including the
6-scenario whole-board differ (byte-identical), the 1716-case `touchProb` identity
and 4000 fuzz boards.

**Whole boards across every extreme in item 9**, real `update()` + `renderBoard()`
on both revisions, byte-compared:

```
card lists compared: 21
boards compared:     308
differing ONLY in the §3.17 list line: 156
differing anywhere else:               0
```

**Zero boards differ anywhere except the §3.17 list line.** Every such case,
enumerated with its before and after and its reason — in all of them the reason is
the same and is the defect being fixed: `listExhaustion(lastRows)` now finds the
three fields it reads.

| Scenario | boards | before | after |
|---|---:|---|---|
| normal/long | 9 | список не измерен: своя мера есть у 0 монет, нужно 8 | медиана списка 1,0 по 25 монетам |
| normal/short | 10 | …у 0 монет, нужно 8 | медиана списка 1,0 по 25 монетам |
| degraded/long | 6 | …у 0 монет, нужно 8 | медиана списка 1,3 по 16 монетам |
| degraded/short | 9 | …у 0 монет, нужно 8 | медиана списка 1,0 по 16 монетам |
| showoff/long | 28 | …у 0 монет, нужно 8 | медиана списка 1,4 по 25 монетам |
| showoff/short | 28 | …у 0 монет, нужно 8 | медиана списка 0,8 по 25 монетам |
| x/slider-low | 5 | …у 0 монет, нужно 8 | медиана списка 0,8 по 25 монетам |
| x/slider-high | 9 | …у 0 монет, нужно 8 | медиана списка 0,6 по 25 монетам |
| x/null-betas | 5 | …у 0 монет, нужно 8 | медиана списка 0,9 по 25 монетам |
| x/missing-coeffs | 23 | …у 0 монет, нужно 8 | медиана списка 0,7 по 25 монетам |
| x/no-btcstats | 7 | …у 0 монет, нужно 8 | медиана списка 0,8 по 25 монетам |
| a3/full-25spot+3fut | 7 | …у 0 монет, нужно 8 | медиана списка 0,6 по 25 монетам |
| a3/one-missing-highPrice | 7 | …у 0 монет, нужно 8 | медиана списка 0,6 по 24 монетам |
| a3/three-spot-rows | 3 | …у 0 монет, нужно 8 | список не измерен: своя мера есть у **3** монет, нужно 8 |

The last row is the below-quorum case: the sentence keeps its shape and only the
count becomes truthful.

### 5. Stage B, the negative controls — PASS

Real mutations of the working tree, not in-memory copies.

`index.html` MD5 before controls: `7627e3aa418dbd371f304bdadcdd351c`.

**Control 1 — delete one producing assignment** (`row.hi24 = parseFloat(coin.highPrice);`):

```
exit=1
update() writes: cd, coin, cur, dec, idx, lo24, sc, state, t, vd
FAIL listExhaustion reads row.hi24 -> update() writes row.hi24: got false want true
FAIL listExhaustion reads fields the live row never carries: hi24
--- checks: 220290  fails: 4 ---
```

**Control 2 — add one read** (`if (row.notWiredHere) continue;` inside `listExhaustion`):

```
exit=1
listExhaustion reads: cd, cd.volatility, cur, hi24, lo24, notWiredHere, t, t.fut
FAIL listExhaustion reads row.notWiredHere -> update() writes row.notWiredHere: got false want true
FAIL listExhaustion reads fields the live row never carries: notWiredHere
--- checks: 220291  fails: 4 ---
```

Each control names **exactly** the mutated field and the step exits non-zero.
Restored and verified by MD5: `7627e3aa418dbd371f304bdadcdd351c` — match. Clean
run after restore: `checks: 220290  fails: 0`, exit 0.

**Retro-control (what inv. 48 is for).** The same section run against
`origin/main`'s `index.html`:

```
update() writes: cd, coin, dec, idx, sc, state, t, vd
listExhaustion reads: cd, cd.volatility, cur, hi24, lo24, t, t.fut
FAIL listExhaustion reads fields the live row never carries: cur, hi24, lo24
--- checks: 220290  fails: 7 ---      EXIT=1
```

It names the three fields of Defect 1 and exits non-zero. Twelve green gate steps
said nothing about it before this section existed.

### 6. Stage C, offline (`--selftest`) — PASS

Run locally and again on the runner as `calib.yml` step 6 (**conclusion:
success**, before the archive is touched). Local output, verbatim — the harness
prints a line only on failure, so a silent section is a passing section:

```
=== TZ-13 Stage C self-test (offline, no network) ===

-- 1. the cut, and where the median comes from --

-- 2. the median and the quorum are production's --
     node hops taken: 3   node: v22.22.2

-- 3. a missing measurement never arrives as a number --

-- 4. known-answer control: E[range] = sigma*sqrt(8T/pi) --
     driftless walk at sigma_day = 0.500%, target 1.000 +/- 0.005, at least 1000000 coin-days
     coin-days 1000000   pooled mean 0.99980   (5s)
     same walk from 24 hourly CLOSES only: 0.8613

-- 5. the gate refuses a value below the null p90 and one above p99.9 --

-- 6. rho is measured --

-- 7. coin_days carries the day key --

-- 8. dates, joined across the universe --

--- checks: 51  fails: 0 ---
```

Against the TZ's six sub-requirements for this item:

- **The known-answer control at `σ_day = 0.5 %`** reads **0.99980** over
  **10⁶** coin-days, against the registered **1.000 ± 0.005**. It fails the run,
  it is not a warning. The TZ predicted an hourly-close path would read ≈ 0.84;
  the same walk built from 24 hourly closes reads **0.8613** here, so the control
  detects the exact error it exists to catch.
- **The median and quorum come from production, not Python.** A fixture of nine
  rows whose ratios are 1…9 by construction returns median **5.0** and `n` **9**
  from `listExhaustion`; seven rows return `median: null` with `n: 7`; eight rows
  return a number. The node hop is proven taken — hop counter and the interpreter
  identifying itself (`v22.22.2` locally). The scan of the run path confirms the
  constant is `np.percentile(emp_med, 90)` and that `emp_med` is built from what
  the hop returned.
- **The gate refuses a synthetic value below the null p90** (condition 2 alone
  fires) **and one above the null p99.9** (condition 3 alone fires), with a value
  between them passing all four; a value EQUAL to the null p90 is also refused,
  because the condition is strict.
- **Nulls survive the JSON hop as nulls, never as zeros.** Four unmeasurable rows
  return `median: null`, `n: 0`, zero ratios, `rnull: 4` and `rsum: 0.0`; mixed
  with one good row, `n` is 1, not 5.

**Determinism.** Two consecutive `--selftest` runs differ in exactly one
character-position — the wall-clock string `(5s)` vs `(6s)`. Every number,
including `pooled mean 0.99980`, is identical. Seed `20260823` is recorded in
the run's own record.

**Step-count sensitivity**, added because the Remaining Risks entry below needs
it to be more than an assertion. The pooled mean of single-coin simulated ratios
at `σ_day = 0.5 %` over 10⁶ coin-days:

| steps/day | pooled mean | deviation from 1.000 |
|---:|---:|---:|
| 24 | 1.00018 | 0.00018 |
| 48 | 1.00002 | 0.00002 |
| 96 | 0.99999 | 0.00001 |
| 240 | 0.99983 | 0.00017 |

Flat across a 10× range, every deviation at Monte-Carlo noise level for that
sample size and two orders inside the registered ±0.005. That is the evidence
that the Brownian-bridge construction is exact in distribution rather than a
discretisation, and that the one approximation left — maximum and minimum drawn
from independent uniforms when both fall in the SAME step — does not move the
answer.

### 7. Stage C, the run

**It ran on a runner, through `calib.yml`, and it passed.**

| | |
|---|---|
| Workflow | `Calibration (archive)`, run **#2** |
| Run id | **32667872706** |
| URL | https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32667872706 |
| Head SHA | `cd9d4b7` |
| Conclusion | **success** |
| Wall clock, whole job | 21:33:24 → 21:44:44 UTC = **11 min 20 s** |
| Wall clock, the calibration step | 21:33:36 → 21:44:37 UTC = **11 min 01 s** |
| The script's own reported wall clock | **660 s** (14 node hops, node `v22.23.2`) |
| Record committed as | `b993810` |

`calib.yml` **fired on the push that added `bench/exhaustion_calib.py`**, as its
paths filter intends — it did not need prompting and it was not edited. The cache
was cold (`Cache incomplete (0 of 25)`), so the run includes a full three-year
archive fetch; the calibration proper — coin-days, ρ, the null and the gate — is
the 660 s the script reports, comfortably inside the TZ's 20-minute budget for the
null.

The record commit carries the message `chore(calib): exhaustion calibration record
(TZ-11 stage B) [skip ci]`. That string is hardcoded in `calib.yml`, which TZ-13
§3 forbids editing, so it still says TZ-11; the record it commits is this run's.

**Every admissibility condition passed and the constant is `1.39`.** No condition
failed, so nothing was re-run at another depth or seed to obtain a different
number.

A **second run** (#3, id 32668675135) was triggered by the follow-up commit
`6ed610b`, which touches `bench/exhaustion_calib.py` and therefore matches
`calib.yml`'s paths filter. It is the same script at the same depth and the same
seed after a behaviour-preserving change, so it is a reproducibility check, not a
second attempt at a number — see `## CI Execution` for its outcome.

### The record, verbatim

`bench/exhaustion-calibration.txt`, 175 lines, as committed by the runner:

```
Universe: 25 spot of 28 declared tokens (fut:true excluded by declaration, inv. 41): HYPE, XMR, LIT
Cut out of index.html: has, sigmaDay, dayRangeRatio, listExhaustion
Seed: 20260823   skeleton steps/day: 24

Cache incomplete (0 of 25) — the archive is needed.
Source availability:
  архив data.binance.vision        200
  зеркало data-api.binance.vision  200
  боевой api.binance.com           451 — доступ закрыт по географии (раннер в США)
  боевой fapi.binance.com          451 — доступ закрыт по географии (раннер в США)
  api.coingecko.com                200
Проверка доступности источников:
  архив data.binance.vision        200
  зеркало data-api.binance.vision  200
  боевой api.binance.com           451 — доступ закрыт по географии (раннер в США)
  боевой fapi.binance.com          451 — доступ закрыт по географии (раннер в США)
  api.coingecko.com                200
Источник: vision

  SUI     ok  26854 ч  дыр 0.0%  (vision)
  ONDO    ok  11984 ч  дыр 0.0%  (vision)
  LINK    ok  26854 ч  дыр 0.0%  (vision)
  RENDER  ok  18206 ч  дыр 0.0%  (vision)
  NEAR    ok  26854 ч  дыр 0.0%  (vision)
  YFI     ok  26854 ч  дыр 0.0%  (vision)
  AAVE    ok  26854 ч  дыр 0.0%  (vision)
  AVAX    ok  26854 ч  дыр 0.0%  (vision)
  FET     ok  26854 ч  дыр 0.0%  (vision)
  ENA     ok  20966 ч  дыр 0.0%  (vision)
  TAO     ok  20746 ч  дыр 0.0%  (vision)
  GRAM    НЕТ ДАННЫХ (нет 36 месячных файлов, строк 1262)
  XRP     ok  26854 ч  дыр 0.0%  (vision)
  ADA     ok  26854 ч  дыр 0.0%  (vision)
  TRX     ok  26854 ч  дыр 0.0%  (vision)
  SOL     ok  26854 ч  дыр 0.0%  (vision)
  BCH     ok  26854 ч  дыр 0.0%  (vision)
  HYPE    ok  10790 ч  дыр 0.0%  (vision-perp)
  SKY     ok   8174 ч  дыр 0.0%  (vision)
  ETH     ok  26854 ч  дыр 0.0%  (vision)
  HBAR    ok  26854 ч  дыр 0.0%  (vision)
  XLM     ok  26854 ч  дыр 0.0%  (vision)
  ALGO    ok  26854 ч  дыр 0.0%  (vision)
  BNB     ok  26854 ч  дыр 0.0%  (vision)
  ZEC     ok  26854 ч  дыр 0.0%  (vision)
  UNI     ok  26854 ч  дыр 0.0%  (vision)
  XMR     ok  26832 ч  дыр 0.0%  (vision-perp)
  LIT     ok  26815 ч  дыр 0.1%  (vision-perp)
  BTC     ok  26854 ч  дыр 0.0%  (vision)
монет в кэше: 28 из 29

=== Coverage ===
  SUI      coin-days  1110  2023-08-09 .. 2026-08-22
  ONDO     coin-days   491  2025-04-19 .. 2026-08-22
  LINK     coin-days  1110  2023-08-09 .. 2026-08-22
  RENDER   coin-days   750  2024-08-03 .. 2026-08-22
  NEAR     coin-days  1110  2023-08-09 .. 2026-08-22
  YFI      coin-days  1110  2023-08-09 .. 2026-08-22
  AAVE     coin-days  1110  2023-08-09 .. 2026-08-22
  AVAX     coin-days  1110  2023-08-09 .. 2026-08-22
  FET      coin-days  1110  2023-08-09 .. 2026-08-22
  ENA      coin-days   865  2024-04-10 .. 2026-08-22
  TAO      coin-days   856  2024-04-19 .. 2026-08-22
  XRP      coin-days  1110  2023-08-09 .. 2026-08-22
  ADA      coin-days  1110  2023-08-09 .. 2026-08-22
  TRX      coin-days  1110  2023-08-09 .. 2026-08-22
  SOL      coin-days  1110  2023-08-09 .. 2026-08-22
  BCH      coin-days  1110  2023-08-09 .. 2026-08-22
  SKY      coin-days   332  2025-09-25 .. 2026-08-22
  ETH      coin-days  1110  2023-08-09 .. 2026-08-22
  HBAR     coin-days  1110  2023-08-09 .. 2026-08-22
  XLM      coin-days  1110  2023-08-09 .. 2026-08-22
  ALGO     coin-days  1110  2023-08-09 .. 2026-08-22
  BNB      coin-days  1110  2023-08-09 .. 2026-08-22
  ZEC      coin-days  1110  2023-08-09 .. 2026-08-22
  UNI      coin-days  1110  2023-08-09 .. 2026-08-22
  skipped: GRAM (not in cache)

=== Dates ===
  dates seen                       : 1110
  dates with a median              : 1110
  dates dropped below quorum       : 0
  span                             : 2023-08-09 .. 2026-08-22
  per-date contributing count (n -> dates): {"19": 245, "20": 9, "21": 106, "22": 259, "23": 159, "24": 332}
  median per-date contributing count: 22.0

  empirical pooled coin-day ratios : n=24384 (null-valued 0), mean 0.9509

=== Correlation (measured, not assumed) ===
  dates with a measured rho        : 1110 of 1110
  hourly observations per window   : median 2161
  rho  pct       value
       p0       0.4557
       p10      0.5341
       p20      0.5482
       p30      0.5632
       p40      0.6114
       p50      0.6370
       p60      0.6500
       p70      0.6593
       p80      0.6662
       p90      0.6916
       p100     0.8265
  rho mean 0.6196   min 0.4557   max 0.8265   negative on 0 dates

=== Null (simulated in this run) ===
  replicas/date    32  null medians    35520  p90 1.2361  MC se 0.00271  [652s]
  replicas/date    96  null medians   106560  p90 1.2358  MC se 0.00158  [654s]
  replicas/date   224  null medians   248640  p90 1.2393  MC se 0.00117  [660s]

  seed                             : 20260823
  replicas per date                : 224
  null date-medians                : 248640
  null p90 Monte-Carlo std. error  : 0.00117 (must be < 0.01)
  null pooled coin-day ratios      : n=5462016 (null-valued 0), mean 1.0012

  null date-median distribution
  pct         value
  p0         0.5850
  p10        0.7789
  p20        0.8223
  p30        0.8589
  p40        0.8945
  p50        0.9325
  p60        0.9769
  p70        1.0323
  p80        1.1093
  p90        1.2393
  p100       2.6604
  p95        1.3626
  p99        1.6271
  p99.9      1.9914

=== Empirical date medians ===
  pct         value
  p0         0.2407
  p10        0.4880
  p20        0.5687
  p30        0.6367
  p40        0.7022
  p50        0.7769
  p60        0.8725
  p70        0.9769
  p80        1.1065
  p90        1.3911
  p100      10.6653

  p90 raw                          : 1.391063
  p90 rounded to 2 dp              : 1.39

  ten highest dates by list median
    2025-10-10  median 10.6653  over 24 coins
    2023-08-17  median 3.6428  over 19 coins
    2024-03-05  median 3.3370  over 19 coins
    2026-02-06  median 3.2160  over 24 coins
    2024-08-05  median 3.1683  over 22 coins
    2024-04-13  median 3.1553  over 20 coins
    2024-01-03  median 3.1525  over 19 coins
    2024-12-09  median 3.0507  over 22 coins
    2024-04-12  median 2.9482  over 20 coins
    2026-02-05  median 2.8248  over 24 coins

=== Admissibility (registered by TZ-13 §2 C5, before the number) ===
  1  PASS coin-day mean: empirical 0.9509 vs null 1.0012 -> 5.03% (allowed 15%)
  2  PASS empirical p90 1.3911 strictly above null p90 1.2393
  3  PASS empirical p90 1.3911 strictly below null p99.9 1.9914
  4  PASS 1110 dates (need 300) and median contributing count 22.0 (need 15)
  se  PASS null p90 Monte-Carlo std. error 0.00117 (need < 0.01)

  wall clock: 660s   node hops: 14   node: v22.23.2

Adopted by the rule registered above, taken as-is:
DAY_RANGE_ABNORMAL = 1.39

Not entered into index.html by this TZ: TZ-13 §3 forbids a consumer, and the
constant reaches production only through the TZ that follows.
```

### What the record says

- **Coverage.** 25 spot assets declared, 24 contributing. `GRAM` has no archive
  (`НЕТ ДАННЫХ (нет 36 месячных файлов, строк 1262)`) — a listing too recent for
  the three-year window, not a pipeline fault. The three `fut:true` assets are
  excluded by declaration (inv. 41) and named in the header. **1110 dates**,
  2023-08-09 … 2026-08-22, **none dropped below quorum**.
- **The coin-day universe is TZ-11's.** `n=24384` pooled coin-day ratios, the same
  count TZ-11 reported. The object changed; the underlying archive did not. That is
  what makes 1.59 → 1.39 a statement about the estimator rather than about the data.
- **ρ was measured on all 1110 dates**, mean **0.6196**, range 0.4557 … 0.8265,
  **negative on zero dates** — so the `[0, 0.999]` clip never engaged and the
  single-factor construction represents every date as measured. The trailing window
  carried a median of **2161** hourly observations, matching the 90-day window the
  volatility itself comes from.
- **The null is calibrated.** Its pooled coin-day mean is **1.0012** — a diffusive
  day reads 1.0, which is the whole point of the denominator being derived rather
  than chosen. Its p90 over date medians is **1.2393** at a Monte-Carlo standard
  error of **0.00117**, an order inside the required 0.01, reached at 224
  replicas/date over 248 640 simulated date medians.
- **Condition 1 is comfortable, not marginal:** empirical coin-day mean 0.9509
  against the null's 1.0012 is a 5.03 % gap against an allowance of 15 %.
- **The signal is real.** The empirical p90 of 1.3911 sits above the null's p95
  (1.3626) and well below its p99 (1.6271) — high enough that a quiet market does
  not reach it a tenth of the time, low enough that it is not a broken pipeline.
- **inv. 47, measured.** Coin-day p90 1.59 (TZ-11) versus list-median p90 1.39.
  TZ-11's floor of 1.60 is above this run's null **p99**.

### 8. Full gate, 12 steps

**All 12 steps exit 0. Baseline 1 250 354 → candidate 1 250 369, Δ = +15.**

The per-step table, the term-by-term explanation of the delta and the step-7
attribution are in `## Test Results` below. Both totals were measured, not
assumed: the baseline from a `git worktree` at `origin/main`, the candidate from
the branch working tree, with the same harness reading each bench's own printed
counter.

The candidate total was measured twice — once at `cd9d4b7` and again at the final
`6ed610b` — and read **1 250 369** both times. `bench.yml` runs
`exhaustion_calib.py` at no step, so the two follow-up commits, which touch only
that file, cannot move the gate; the second measurement confirms it.

**On the runner:** `Bench gate` run **#66** (id 32667872695, `cd9d4b7`) and run
**#67** (id 32668675133, `6ed610b`) both concluded **success**, 12 steps each,
every step green. Run #66's own log confirms step 12 independently:

```
  control: 1
  wiring: 15
  SUM: 220290

--- checks: 220290  fails: 0 ---
```

`wiring: 15` and `SUM: 220290` on the runner match the local numbers exactly.

### 9. Extremes — PASS

All ten are in the item-4 scenario set above and every one of them produced
byte-identical boards outside the list line: slider edges (`x/slider-low`,
`x/slider-high`), null betas (`x/null-betas`), truncated Gist (`x/trunc-gist`),
HTTP 400 ticker (`x/http400`), dead-market fields (`x/dead-market`), missing
coeffs fields (`x/missing-coeffs`), absent `btcStats` (`x/no-btcstats`), absent
`volatility` (`x/no-volatility`, both sides), `E ≤ 0` and non-finite `liq` (the
`prot_bench.js` squeeze suite, which asserts the §3.17 rows still print in both).
`update()` threw in none of them.

### 10. Release checklist item 15 — PASS

The list line names a coin count that matches the spot rows on screen, in every
scenario, with **0 mismatches over 18 scenarios**:

| Scenario | list line `n` | contributing spot rows |
|---|---:|---:|
| normal/long, normal/short | 25 | 25 |
| degraded/long, degraded/short | 16 | 16 |
| showoff/long, showoff/short | 25 | 25 |
| x/slider-low, x/slider-high | 25 | 25 |
| x/null-betas, x/missing-coeffs, x/no-btcstats | 25 | 25 |
| a3/full-25spot+3fut | 25 | 25 |
| a3/one-missing-highPrice | 24 | 24 |
| a3/three-spot-rows | 3 | 3 |
| emptybot, x/trunc-gist, x/http400, x/dead-market | 0 | 0 |

**"and never zero" holds on screen.** In the four degenerate scenarios there are no
bot metrics at all, so no row carries `cd`, and the board those scenarios render is
the 449-character no-data stub: **0 of 28 boards print the list line**, so no zero
is ever shown. On any board that does contain a §3.17 block the count is the live
spot-row count, and the lowest non-degenerate reading is 16.

## Test Results

| Step | Bench | Baseline (`origin/main` worktree) | Candidate | Δ |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 |
| 3 | `prot_bench.js` | 372 | 372 | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 255 708 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 |
| 7 | `journal_bench.js` | **691 109** | **691 109** | **0** |
| 8 | `catalyst_bench.js` | 23 040 | 23 040 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 15 925 | 15 925 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | 220 275 | **220 290** | **+15** |
| | **TOTAL** | **1 250 354** | **1 250 369** | **+15** |

**The delta is +15 and every unit of it is section H.** Term by term, from the
bench's own per-section counters (`wiring: 15`, `SUM: 220290`):

| Check | Count |
|---|---:|
| the wiring extractor found both sides | 1 |
| `update()` writes at least one row field (inv. 22) | 1 |
| `listExhaustion` reads at least one row field (inv. 22) | 1 |
| one check per field read — `cd`, `cd.volatility`, `cur`, `hi24`, `lo24`, `t`, `t.fut` | 7 |
| each control copy differs from the source | 2 |
| deleting `row.cur` reports exactly `[cur]` | 1 |
| adding a read of `row.zzzNotWritten` reports exactly `[zzzNotWritten]` | 1 |
| the unmutated source reports no missing field | 1 |
| **section H total** | **15** |

`exhaustion_bench.js`'s other nine sections are unchanged: `identity: 200002`,
`nulls: 20027`, `quorum: 65`, `venue: 25`, `banner: 52`, `stress: 51`,
`inert: 30`, `purity: 22`, `control: 1`.

**Step 7 did not move.** It is content-sensitive — `journal_bench.js` counts
numeric leaves of the records it writes, so a verdict that returns before
geometry changes the count without changing a control — and it reads 691 109 on
both sides. No verdict changed, which is the same fact the 308-board differ
reports from the other direction.

`bench.yml` was not edited: still 12 steps.

## Deviations

**One, stated plainly: three row-level `parseFloat` sites were rerouted that the
TZ's Stage A table does not list.**

The TZ's Stage A table enumerates three migrations. `index.html` contains three
further row-level parses of `lastPrice`, all inside `update()`:

| Line (origin/main) | Context |
|---|---|
| 3247 | the off-list relevance filter, `rangePos(orow.cd, parseFloat(orow.coin.lastPrice))` |
| 3285 | the dead-market card, `var frozenP = parseFloat(row.coin.lastPrice)` |
| 3303 | the card header, `var cur = parseFloat(coin.lastPrice)` |

Following the table alone leaves four parse sites for `lastPrice` per row, which
fails the TZ's own validation item 2 — *"Exactly one parse site per field per row
must survive"* — and defeats Stage A's stated purpose, which is its heading: *"the
row contract, one parse site per quantity."* The normative sentence above the table
is *"Every existing consumer of those three quantities then reads the row, and the
`parseFloat` disappears from its old site."* I read the table as an incomplete
enumeration rather than as an exhaustive one, and rerouted all three.

Why this is safe and cheap:

- All three read `row.coin`, which is the same object `row.cur` was parsed from, so
  every rerouted expression is **value-identical**, NaN cases included. `row.cur` is
  assigned before the dead-market test, so the `state === 'dead'` card at 3285 has
  it.
- All three are inside `update()`, which `render_bench.py` runs for real, so the
  reroute forced **no additional fixture change** anywhere.
- The 308-board / 21-card-list differ reports zero differences outside the list
  line, which is the direct proof that nothing moved.

Reverting these three is a three-line change if the Architect intended the table as
exhaustive.

Two further judgement calls, neither a scope change:

- The Stage B inclusion rule treats a nested read (`row.t.fut`, `row.cd.volatility`)
  as satisfied when its ROOT is written. `update()` assigns `row.t` and `row.cd`
  whole; `fut` and `volatility` are fields of those objects, not of the row, so
  requiring them on the write side would fail the clean source. Each nested read
  still gets its own named check, so the count is one check per field read as the TZ
  requires.
- The added code comment in `index.html` is in English. Contract §10 forbids Russian
  in a code comment written for this pipeline, and the recent TZ-10/TZ-12 additions
  in that file are English; the surrounding older Russian comments are pre-existing
  and were not touched.

## Pre-existing Issues

The three the TZ names, all confirmed still present and **not fixed**:

1. **`NaN` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ».** `Math.abs(liq / E - 1)` with `E = 0`.
   `prot_bench.js` prints its own standing note about it on every run: *"PRE-EXISTING
   (not TZ-12, present on origin/main): at E = 0 the board prints NaN in «ГРАНИЦЫ
   СДЕЛКИ»"*.
2. **Raw Cyrillic string literal in `bench/prot_bench.js`.** Confirmed at line
   **166** on `origin/main` (`src: 'мин30'`); it is at line **177** on this branch,
   shifted by the 11 lines the fixture helper adds above it. The literal itself is
   untouched.
3. **The Node 20 action pin.** Confirmed on this run's own runner log:
   *"Node.js 20 is deprecated. The following actions target Node.js 20 but are being
   forced to run on Node.js 24: actions/checkout@v4, actions/setup-node@v4,
   actions/setup-python@v5."* Warning only; the gate is green.

Nothing else new was found.

One observation that is **not** a defect, recorded because it bears on the next TZ:
`calib.yml` step 8 (the record commit) has no `if: always()`, so a calibration that
exits non-zero on an admissibility failure never commits
`bench/exhaustion-calibration.txt` — the record survives only as the
`upload-artifact` step's artifact, which does carry `if: always()`. TZ §3 forbids
editing `calib.yml`, so this is reported and not changed.

## Remaining Risks

- **The same-step joint law — measured, and it does not bite.** The
  Brownian-bridge construction is exact per step, and the bridges on disjoint steps
  are independent given the skeleton, so the global maximum and the global minimum
  are each exact in distribution. The one approximation left is the JOINT law of the
  maximum and the minimum falling **within one step**, drawn from independent
  uniforms. This was measured rather than argued: the known-answer control across
  24 / 48 / 96 / 240 steps per day reads 1.00018 / 1.00002 / 0.99999 / 0.99983, flat
  to Monte-Carlo noise over a 10× range and two orders inside the registered ±0.005.
  Whatever the residual is, it is not visible at the tolerance that matters.
- **ρ never needed clipping on this data.** ρ is clipped to `[0, 0.999]` before
  entering the single-factor construction, because a common factor cannot represent
  a negative mean pairwise correlation. On the actual run the measured ρ ranged
  0.4557 … 0.8265 with **zero** negative dates, so the clip did not engage. It
  remains a real limitation for a future universe with a genuine hedge in it, and
  the record prints the distribution and the negative-date count so any future
  clipping is visible rather than silent.
- **ρ was measurable on all 1110 dates**, so the median-of-measured fallback did
  not engage either. The record states the count in both directions.
- **The empirical distribution is wider than the null on BOTH tails**, and the null
  cannot produce that. Empirical p0 is 0.2407 against the null's 0.5850, and
  empirical p100 is 10.6653 against the null's 2.6604 — the top date, 2025-10-10,
  sits five times the null's p99.9. A constant-σ common-factor null has no
  vocabulary for a market that alternates between very quiet and very violent
  regimes, so it is a floor on what a quiet market reaches, which is precisely the
  job conditions 2 and 3 give it, and **not** a model of the return distribution.
  Reading it as one would be a mistake.
- **`GRAM` contributes nothing** — the three-year archive has no data for it — so
  the calibration rests on 24 of the 25 declared spot assets, and per-date
  contributing counts run 19 … 24. Condition 4 was designed for exactly this and
  passed with a median count of 22 against a floor of 15.
- The measure still has **no consumer**. Everything above is an instrument reading;
  §3.17 prints it and nothing else acts on it. `DAY_RANGE_ABNORMAL = 1.39` exists
  only in `bench/exhaustion-calibration.txt` and is adopted by nothing.

## Commit

Branch `claude/execute-tz-13-ddb93g`, two commits:

| SHA | Author | Subject |
|---|---|---|
| `cd9d4b7` | this session | `feat(board): live wiring of the list exhaustion measure; calibration re-registered on the list median (TZ-13)` |
| `b993810` | `calib.yml` runner | `chore(calib): exhaustion calibration record (TZ-11 stage B) [skip ci]` |
| `80dc544` | this session | `test(calib): state precisely which median the self-test rules out (TZ-13)` |
| `6ed610b` | this session | `fix(calib): read the step count at call time, not as a frozen default (TZ-13)` |
| `9715a91` | `calib.yml` runner | `chore(calib): exhaustion calibration record (TZ-11 stage B) [skip ci]` |

Branch head: `9715a91`.

The TZ carries no `## Commit Message` section, so the messages follow the
repository's own convention (`feat(scope): … (TZ-NN)`).

The two `chore(calib)` commits are the runner's, not this session's — `calib.yml`
writes and commits the record with `[skip ci]` and its own hardcoded message,
which still reads "TZ-11 stage B" because TZ-13 §3 forbids editing that workflow.
The TZ's warning to pull before any further commit was followed: `80dc544` and
`6ed610b` were rebased onto `b993810` rather than pushed over it, so the runner's
record commit is intact in the history.

`80dc544` and `6ed610b` touch `bench/exhaustion_calib.py` only, which `bench.yml`
does not run at any step, so neither can move the gate total — and the gate was
re-measured at `6ed610b` to confirm it.

Working tree clean; no scratch file, `__pycache__` or cache directory committed.

## Pull Request

**NO PULL REQUEST EXISTS.** This session runs under a base configuration that
forbids opening one without an explicit instruction, which is the case contract
§8 anticipates. The fallback applies:

- **Branch: `claude/execute-tz-13-ddb93g`**
- **Compare URL: https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-13-ddb93g**

The Boss opens and merges from that link in one action.

**Unlike TZ-06, a branch with no pull request is NOT a branch with no CI here.**
`bench.yml` triggers on `push` to `claude/**` — the hole TZ-07 §6 closed — so the
gate executed on a runner twice against this branch (runs #66 and #67, both
green), and `calib.yml` executed against it as well. The proof is on GitHub, not
on a laptop.

## CI Execution

**Everything ran on a GitHub runner. Nothing here is a laptop-only claim.**

| Workflow | Run | Head SHA | Conclusion |
|---|---|---|---|
| `Bench gate` | [#66](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32667872695) (id 32667872695) | `cd9d4b7` | **success** — 12/12 steps |
| `Calibration (archive)` | [#2](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32667872706) (id 32667872706) | `cd9d4b7` | **success** — all conditions passed |
| `Bench gate` | [#67](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32668675133) (id 32668675133) | `6ed610b` | **success** — 12/12 steps |
| `Calibration (archive)` | [#3](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32668675135) (id 32668675135) | `6ed610b` | **success** — all conditions passed |

`journal.yml`, `main.yml` and `backtest_bench.yml` did **not** run and were not
expected to: none of them triggers on a `claude/**` push for these paths, and none
was modified.

### The reproducibility check

Run #3 is the same script at the same depth (`--years 3`) and the same seed
(`20260823`) as run #2, on a different runner, after a behaviour-preserving change
to how the step count is read. It is **not** a second attempt at a number: run #2
passed every condition, so there was nothing to retry, and the TZ's prohibition is
on re-running to obtain a different answer.

The two records differ in **exactly two kinds of line** — the cache status
(`Cache incomplete (0 of 25)` vs `(24 of 25)`, and the per-coin fetch lines vs
`уже в кэше`) and the wall clock (`[652s] [654s] [660s]`, `wall clock: 660s` vs
`[54s] [57s] [63s]`, `wall clock: 63s`). **Every statistic is byte-identical**,
line for line:

```
  replicas/date    32  null medians    35520  p90 1.2361  MC se 0.00271
  replicas/date    96  null medians   106560  p90 1.2358  MC se 0.00158
  replicas/date   224  null medians   248640  p90 1.2393  MC se 0.00117
  1  PASS coin-day mean: empirical 0.9509 vs null 1.0012 -> 5.03% (allowed 15%)
  2  PASS empirical p90 1.3911 strictly above null p90 1.2393
  3  PASS empirical p90 1.3911 strictly below null p99.9 1.9914
  4  PASS 1110 dates (need 300) and median contributing count 22.0 (need 15)
  se  PASS null p90 Monte-Carlo std. error 0.00117 (need < 0.01)
DAY_RANGE_ABNORMAL = 1.39
```

Two runners, cold cache and warm, reproduced the constant exactly. The record
currently on the branch is run #3's (`9715a91`); run #2's is `b993810` in the
branch history, and both are also retained as `exhaustion-calibration`
`upload-artifact` artifacts on their runs.

## Final Repository State

Branch `claude/execute-tz-13-ddb93g` at `9715a91`, five commits ahead of
`origin/main` (`0d25baf`); two of the five are the `calib.yml` runner's own record
commits. Working tree clean.

`main` carries only this report, under `CryptoReports/`, as contract §8 requires.
No production file, bench or workflow was pushed to `main` by this session.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Measured on branch `claude/execute-tz-13-ddb93g` at `6ed610b`.

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1238 | `ba79472fde0fd478098b69ed1eadadba` |
| `index.html` | 3666 | `cef52cf6eb00ff063e66510a5bd0f828` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |

`SYSTEM-MAP-CRYPTOCALCUL.md` revision string, from its `## 0. Fingerprint` block:
**`Revision 2026-08-23-c.`** The map was not modified.

`main.py` and `catalysts.json` are byte-identical to `origin/main` and to the
figures the map's `## 0. Fingerprint` block states — `506` / `1a5a5d98…` and `11`
/ `021dd2c9…`. No file disagrees with the map at the baseline revision, so there
is nothing to report under that head.

`index.html` has moved, as this TZ requires: the map states `3656` /
`64acaaa59f2ed96d568714d2813d20f9` at revision 2026-08-23-c, which is exactly what
`origin/main` measures and what the fingerprint gate matched before any work
began. The branch figure above is the post-Stage-A file and will become the map's
figure when the Architect issues the next revision.

Also on the branch, written by the `calib.yml` runner rather than by this session:

| File | Lines | MD5 |
|---|---:|---|
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
