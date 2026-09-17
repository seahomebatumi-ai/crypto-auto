# Implementation Report — TZ-48

**The previous TZ was report-only, so no branch of it could be unmerged.** TZ-47 was BLOCKED and
wrote only its report, `7e6402b` on `main`. The last branch TZ, TZ-44, is merged: pull request
#39, merge commit `baec7c9`. TZ-48 supersedes TZ-47 and has no sequencing clause.

`main` moved once during the session, from `61ecfae` (this TZ's upload) to `b6dc991`. That
commit is `update live.json⁠` and touches `analyst/live.json` only. The implementation commit was
rebased onto `b6dc991` before its first push.

## Status

**COMPLETED.**

- **Gate.** The fingerprint gate passed: 7 of the table's 7 anchors matched, and every file figure
  matched.
- **Diff.** `bench/backtest_bench.py` is the only file in the diff.
- **Validation.** Every validation item was run.
- **CI.** Both hosted `Bench gate` runs on the implementation commit concluded `success`. Their
  own logs were read: gate step 4 prints **59 / FAIL 0** and gate step 14 prints **487 / FAIL 0**.

**Two deviations are recorded (`## Deviations`).** In each, the only reading that satisfies
another clause of the TZ was taken:

1. **The driver field sits inside `prod`, not beside `reg`.** With the field beside `reg`, gate
   step 14 measured **487 / FAIL 1** at check 33. That guard is one the TZ forbids editing.
2. **Control 4 asserts the direction of the move, not only the move.** A movement-only control 4
   stays green under §6 item 5's inversion, yet that item lists control 4 as must-turn-red.

**A pre-existing defect sits in the mode the reading rides on.** `--regime-gate` raises
`TypeError` at its `json.dump`, so its raw JSON has never been writable. See reading item 1 and
`## Pre-existing Issues`.

## Inbound Filing

None. The TZ arrived as `CryptoTZ/TZ-48-own-regime-gate.md` in `61ecfae`, matching its header's
canonical filename. Nothing was moved or renamed.

## Scope Executed

**Class: branch TZ.** §3 names one file outside `CryptoReports/**`: `bench/backtest_bench.py`.

Executed:

- contract §4a, steps 1–11;
- the §5 fingerprint gate, which passed;
- TZ §4.1–§4.5: the driver field, the observation-level population view, the existing grid, the
  census, and unchanged existing output;
- TZ §6 items 1–4 and 6, as `--lab-selftest` section E;
- TZ §6 item 5, as a session negative control against its written partition;
- TZ §7's three reading items, answered with nothing edited;
- TZ validation items 1–12.

Nothing in scope was skipped. No archive was read (validation item 10).

## Files Created

- `CryptoReports/TZ-48-own-regime-gate-report.md`: this report, on `main`.

## Files Modified

- `bench/backtest_bench.py`
  - lines 5102 → **5795**;
  - MD5 `ba633202f43845ba0fdafbc1b92d9c04` → `ed4db7c2bab9076e92982c664c6fc2f6`;
  - `git diff --numstat` against `main`: 702 added, 9 deleted;
  - `git diff -U0` shows **18** hunks. The default diff shows 16, because it merges edits whose
    three-line context windows touch.

## Files Renamed

None.

## Files Deleted

None in the repository. This session's in-tree runs wrote ignored scratch (`bench/_*`,
`bench/__pycache__/`), which was removed. No file under `bench/_*` is tracked:
`git ls-files 'bench/_*'` prints nothing.

## Implementation Summary

Line numbers are in the committed file at `4a11c8b`.

**§4.1: one field in the driver.**

- `TARGET_DRIVER` gains the helper `wordOut(w)` (`:3248`), which returns `{mode, dir}`, and one
  field, `own: wordOut(marketRegime(j.cd)),` (`:3341`). The argument is the whole `j.cd`.
- The field sits inside `prod` (Deviation 1), and the comment at the site says why.
- `TGT_OWN_JS` (`:3354`) names that one line. Import raises unless it occurs exactly once. The
  lab's identity control removes exactly this line to obtain the pre-change driver.
- `run_target` (`:3420`) copies the field into each observation as `o["own"]`, beside
  `o["reg"]` (`:3537`). With it goes `o["cd"]`, the job's own record object, so the census reads
  |r14| and its null reads the record from one place and never re-builds either. The observation
  loop now zips `jobs` as well (`:3516`).
- `run_target` and `run_regime_grid` gain `driver=None`. No mode sets it; only lab E3 and E4
  pass one.

**§4.2: observations, not dates.**

- `_own_split` (`:4028`) returns `{word: view}`. A view is shaped like a date list: it keeps each
  date's `t` and only the observations carrying that word.
- A date left with no observation for a word is absent from that word's view.
- An observation with no word is refused with a `ValueError` naming the date (inv. 67).
- A view goes to `_arm_pool` unchanged.

**§4.3: the existing grid.**

- `regime_gate_summary` (`:4110`) gains `splitter=_rg_split` (`:4127`).
- With `_own_split`, the same function produces the same `RG_H_GRID × RG_RR_GRID × side × RG_POPS`
  cells, with `stress` kept apart. The quorum, `bar = inv_rr`, the empty-cell reasons,
  `_rg_verdict` and `_rg_below` are unchanged.
- `btc=None` omits the labeller agreement (`:4166`), because that is a count about the market word.
- `own_regime_summary` (`:4469`) is that call plus the census.

**§4.4: the census.** `own_census` (`:4460`) runs `_own_rows` (`:4366`), then `_own_table`
(`:4385`), then `_own_stats` (`:4408`).

- **Rows.** There is one row per coin-date. A coin-date met again with a different word or record
  is counted in `n_conflict`.
- **Per word.** Each word gets its coin-date count and the quartiles of |r14|, taken from the
  record the word was computed from.
- **`overlap`** (`_own_overlap`, `:4396`) is the share of `range` whose |r14| reaches `trend`'s
  median. When either cell is empty it is `None`, and the empty cell is named.
- **The decoupled null.**
  - `OWN_DRIVER` (`:4336`) computes production's word on each record under every volatility its
    date carries. The record is copied and one field substituted.
  - `_own_stats` permutes volatility within each date `TGT_BOOT` (2000) times. Each date is
    seeded by itself alone.
  - It prints the null's median and its 2.5–97.5 % spread beside `overlap`. No band and no
    verdict word attach.
  - The null is a distribution rather than one permutation, so a reader can set `overlap` against
    the null's own spread. `TGT_BOOT` is reused rather than a new numeral.
- **Identity count.** `id_cmp` / `id_diff` compare the recorded field with production's word on
  the recorded record.

**§4.5: existing output.**

- `--regime-gate` (`:5719`) prints `report_own_regime` (`:4480`) after the market-word report and
  before the dump. `sm` and `regime_gate_raw.json` are untouched.
- The coin-word reading is therefore retained as text, in `regime_gate.txt`.
- It is not added to the JSON for two reasons. The dump raises before any key it would add
  (Pre-existing Issue 1), and §4.5 forbids that file to move.

**§6: section E.**

- `lab_own_word` (`:4820`) runs after section D (`:5579`). It reuses section D's world and its
  `--target` and `--regime-gate` records, so the identity control's field-present side costs no
  second pass.
- Helpers: `synth_own` (`:4737`) builds the six worlds; `_out_fields` and `_out_diff` (`:4793`,
  `:4811`) are the field comparator.
- Every comparison increments the section counter at its own site. The section prints
  `E сравнений N, отказов K` and fails on zero comparisons.

| Printed line | TZ clause |
|---|---|
| `E0`, three lines | The view, and these extremes: a population of one date; a date whose filtered `obs` is empty; a cell whose arm admitted no setup; a coin-date with absent volatility (`known:false`) |
| `E1 W1` … `E1 W6` | §6 item 1. W1 also covers the all-`stress` world and P3's printed `decidable: false` |
| `E2` | §6 item 2 |
| `E3` (four lines) | §6 item 3, plus the coin-word grid built from the same passes |
| `E4` | §6 item 4 (Deviation 2) |
| `E сравнений …` | §6 item 6 |

**What goes beyond §2's closing sentence.** §2 reads «It adds one call to production's
`marketRegime` … and one population split. Anything beyond that is out of scope.» §4.4 and §6
require more. Each addition below serves one of those clauses:

| Addition | Clause it serves |
|---|---|
| `o["cd"]`, `OWN_DRIVER` | §4.4: the |r14| quartiles and the null |
| `driver=` | §6 items 3 and 4 |
| `splitter`, `btc=None` | §4.2 and §4.3, which run through the existing function |
| `synth_own`, `_out_fields`, `_out_diff` | §6 items 1 and 3 |

None of them adds a formula, a threshold, a quorum or a bar to the measurement.

## Validation

All bench runs were made in this session's container: 1 CPU, 955 MB of RAM, Python 3.12.3,
numpy 2.5.0, node 22.23.1. They ran one at a time. The «before» runs used a `git archive`
extract of `61ecfae` under `/tmp/tz48/pristine` (file MD5 `ba633202…`). The «after» runs used
the committed file `ed4db7c2…`. Every lab command is `backtest_bench.yml`'s own.

In quoted lab output, the closure-check lines (`замкнутость …`) and numpy's stderr
`RuntimeWarning` are filtered out, and nothing else is.

### 1. `py_compile`

```
$ python3 -m py_compile bench/backtest_bench.py; echo "py_compile exit $?"
py_compile exit 0
```

### 2. The diff touches one file

```
$ git diff --stat origin/main...claude/tz-48-own-regime-gate
 bench/backtest_bench.py | 711 +++++++++++++++++++++++++++++++++++++++++++++++-
 1 file changed, 702 insertions(+), 9 deletions(-)
$ git diff --name-only origin/main...claude/tz-48-own-regime-gate
bench/backtest_bench.py
```

No change to `index.html`, `main.py`, `catalysts.json`, any other bench or any workflow.

### 3. `--selftest`, before and after

Command: `cd bench && python3 backtest_bench.py --selftest --seeds 10 --html ../index.html --bot ../main.py`

| | Exit | Seconds | Output MD5 |
|---|---:|---:|---|
| before | 0 | 90 | `888b31de3f1f77380b23e179bca32c2a` |
| after | 0 | 89 | `888b31de3f1f77380b23e179bca32c2a` |

The output is **byte-identical**. `--selftest` prints no count of its own. Counted at its
comparison sites, it makes **36 comparisons before and 36 after**:

| Site | Comparisons | What it compares |
|---|---:|---|
| Т2 | 1 | record identity; the run exits on failure |
| Т3 | 1 | monotonicity |
| Т4 | 30 | the sign or 2·SE test, 10 seeds × 3 worlds, printed as «нужный знак k/10» |
| ИТОГ | 4 | `ok_null` twice, `ok_pow` twice |

`selftest()` is outside the diff.

### 4. `--lab-selftest`: section E, its letter, and the prior sections

**Letter `E`, read from the file.** Before the change
(`git show origin/main:bench/backtest_bench.py`), `lab_selftest` printed four section headers of
the form `print("X · …")` and no others:

- `A · --stops` (`:4470`)
- `B · --res7` (`:4485`)
- `C · --funding` (`:4511`)
- `D · --target` (`:4530`)

The new section is the next letter. In the changed file it prints `E · --regime-gate, слово
монеты` (`:4827`), after D.

Command: `cd bench && python3 backtest_bench.py --lab-selftest --html ../index.html --bot ../main.py`

| | Exit | Seconds | Output MD5 | Verdict |
|---|---:|---:|---|---|
| before | 0 | 194 | `8be6325f0d7ed959566dcd136e696cb6` | «измеряет то, что должна» |
| after, committed file, run from the worktree | 0 | 354 | `c05f2a83e0c168c8cd7777ce5393be24` | «измеряет то, что должна» |

**Section E: 4254 comparisons, 0 failures.** A run of the same file from a `/tmp` copy produced
the same output MD5 (`c05f2a83…`).

**Prior sections, before and after.**

- **Lines.** All 38 lines of sections A–D plus the verdict line are identical
  (`diff` exit 0, closure lines and the numpy warning excluded).
- **Closure lines.** The 23 closure lines before section E are identical, as a multiset. For
  `_tgt_bridge.js` both read `сверено 116 обращений, 36 имён`: `wordOut` is driver-local, and
  `marketRegime` was already referenced.
- **Printed counts.** Every one is unchanged:

  | Count | Before | After |
  |---|---:|---:|
  | D4a | 7848 | 7848 |
  | D4b | 7926 | 7926 |
  | D9 | 8829 | 8829 |
  | D7d | 19 | 19 |

  D2's admissions per grid point (0 / 346 / 823 / 977 / 1113) and D3's five rungs are also
  identical.

The delta is zero on every term.

Section E at the default seeds, verbatim (`/tmp/tz48/final_lab3.txt`):

```
E · --regime-gate, слово монеты
  E0 деление по наблюдениям: каждое в одном виде, дата без своего слова из вида выпала, запись без слова отвергнута ОК
  E0 края сетки: популяция из одной даты — «сетапов 1 на 1 датах (дат в популяции 1) — пул не собран» · ни одного сетапа — «сетапов 0 на 0 датах (дат в популяции 6) — пул не собран» · сравнений 0, decidable false ОК
  E0 волатильности нет: та же запись с волатильностью — stress, без неё — range (known:false) · в мире с плоской монетой её монето-дат в записи 0, остальных монет 3 ОК
  E1 W1 гладкий подъём — только stress: посевов 3 · монето-дат 1404 · range 0 · trend 0 · stress 1404 · overlap — — — (пуста ячейка range и trend) · нуль — — — · волатильность не выше 7.8e-16 ОК
  E1 W2 лестница — только trend: посевов 3 · монето-дат 1404 · range 0 · trend 1404 · stress 0 · overlap — — — (пуста ячейка range) · нуль — — — ОК
  E1 W3 зигзаг — только range, overlap не определён: посевов 3 · монето-дат 1404 · range 1404 · trend 0 · stress 0 · overlap — — — (пуста ячейка trend) · нуль — — — ОК
  E1 W4 блуждание с одной волатильностью — overlap 0: посевов 3 · монето-дат 1404 · range 634 · trend 707 · stress 63 · overlap 0.000 0.000 0.000 · нуль 0.000 0.000 0.000 ОК
  E1 W5 лестницы и зигзаги поровну — overlap 1: посевов 3 · монето-дат 1404 · range 702 · trend 702 · stress 0 · overlap 1.000 1.000 1.000 · нуль 0.880 0.885 0.876 ОК
  E1 W6 броуновские σ × снос — ни одна монета не вся в range: посевов 3 · монето-дат 1404 · range 544 · trend 753 · stress 107 · overlap 0.026 0.050 0.000 · нуль 0.010 0.015 0.000 · доля range у монет без сноса 0.453, для справки P(|N(0,1)| < EFF_TREND) = 0.451 ОК
  E2 усечение на дате (W4, посев 1): записей 468, расхождений 0 · слов 468, расхождений 0 · дат со статистикой переписи 39, расхождений 0 ОК
  E3 тождество (мир D: synth_hl «normal», первая монета — BTC; безусловно — ни рукав, ни деление по слову рынка не читают новое поле): наблюдений с полем 2460 из 2460, в прогоне без поля 0 из 2460
     --target: полей 425, расхождений 0, пропало 0, добавлено 0 · строк отчёта 100, расхождений 0
     --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 233
     тот же сравниватель против возмущённого поля: --target расхождений 1 · --regime-gate расхождений 1 (120|1.5|long|range) ОК
     сетка слова монеты на тех же проходах: ячеек 144 (у слова рынка 144) · монето-дат 1245 · range 575 · trend 605 · stress 65 · decidable true ОК
  E4 EFF_TREND 0.60 → 0.90 в вырезанном бандле (W4, посев 1): range/trend/stress 222/223/23 → 297/148/23 · trend→range 75 (нужно > 0) · range→другое 0 (должно 0) · stress сменило слово 0 (должно 0) ОК
  E сравнений 4254, отказов 0 ОК
ВЕРДИКТ ЛАБОРАТОРИИ: измеряет то, что должна
```

### 5. W1–W6 at `--lab-seeds 3` and `--lab-seeds 10`

The 10-seed run: `--lab-selftest --lab-seeds 10`, exit **0**, 542 s, output MD5
`ecb32dfb6e70c617234ec91657cd3e07`. Section E makes **4562 comparisons with 0 failures**, and the
verdict is «измеряет то, что должна».

The +308 comparisons over the 3-seed run are 7 extra seeds × the per-seed checks of each world:
W1 6, W2 6, W3 6, W4 5, W5 5, W6 16. W1's P3 checks run on seed 1 only. Its section E lines:

```
  E1 W1 гладкий подъём — только stress: посевов 10 · монето-дат 4680 · range 0 · trend 0 · stress 4680 · overlap — — — — — — — — — — (пуста ячейка range и trend) · нуль — — — — — — — — — — · волатильность не выше 8.3e-16 ОК
  E1 W2 лестница — только trend: посевов 10 · монето-дат 4680 · range 0 · trend 4680 · stress 0 · overlap — — — — — — — — — — (пуста ячейка range) · нуль — — — — — — — — — — ОК
  E1 W3 зигзаг — только range, overlap не определён: посевов 10 · монето-дат 4680 · range 4680 · trend 0 · stress 0 · overlap — — — — — — — — — — (пуста ячейка trend) · нуль — — — — — — — — — — ОК
  E1 W4 блуждание с одной волатильностью — overlap 0: посевов 10 · монето-дат 4680 · range 2072 · trend 2391 · stress 217 · overlap 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 · нуль 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 ОК
  E1 W5 лестницы и зигзаги поровну — overlap 1: посевов 10 · монето-дат 4680 · range 2340 · trend 2340 · stress 0 · overlap 1.000 1.000 1.000 1.000 1.000 1.000 1.000 1.000 1.000 1.000 · нуль 0.880 0.885 0.876 0.868 0.880 0.876 0.885 0.885 0.885 0.889 ОК
  E1 W6 броуновские σ × снос — ни одна монета не вся в range: посевов 10 · монето-дат 4680 · range 1752 · trend 2522 · stress 406 · overlap 0.026 0.050 0.000 0.000 0.000 0.017 0.013 0.027 0.000 0.000 · нуль 0.010 0.015 0.000 0.000 0.000 0.010 0.000 0.010 0.000 0.000 · доля range у монет без сноса 0.468, для справки P(|N(0,1)| < EFF_TREND) = 0.451 ОК
  E2 усечение на дате (W4, посев 1): записей 468, расхождений 0 · слов 468, расхождений 0 · дат со статистикой переписи 39, расхождений 0 ОК
  E3 тождество (мир D: synth_hl «normal», первая монета — BTC; безусловно — ни рукав, ни деление по слову рынка не читают новое поле): наблюдений с полем 2460 из 2460, в прогоне без поля 0 из 2460
     --target: полей 425, расхождений 0, пропало 0, добавлено 0 · строк отчёта 100, расхождений 0
     --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 233
     тот же сравниватель против возмущённого поля: --target расхождений 1 · --regime-gate расхождений 1 (120|1.5|long|range) ОК
     сетка слова монеты на тех же проходах: ячеек 144 (у слова рынка 144) · монето-дат 1245 · range 575 · trend 605 · stress 65 · decidable true ОК
  E4 EFF_TREND 0.60 → 0.90 в вырезанном бандле (W4, посев 1): range/trend/stress 222/223/23 → 297/148/23 · trend→range 75 (нужно > 0) · range→другое 0 (должно 0) · stress сменило слово 0 (должно 0) ОК
  E сравнений 4562, отказов 0 ОК
```

**The fixtures.** Every world is 12 coins over 8760 h, and every seed gives 39 dates, so there
are 468 coin-dates per seed: 1404 at 3 seeds and 4680 at 10. These are TZ-47's dimensions, so its
figures are directly comparable. The worlds:

| World | Construction |
|---|---|
| W1 | log-price `a·t`, with `a` drawn per coin in [0.0008, 0.0012] |
| W2 | a jump of 0.03 every 100 h at a random phase |
| W3 | `0.0003·t ± 0.007` alternating, at a random sign |
| W4 | gaussian walks, σ 0.01 for every coin |
| W5 | even coins W2 with a jump of 0.01, odd coins W3 |
| W6 | σ ∈ {0.004, 0.008, 0.016} × drift ∈ {0, +0.0002, −0.0002, +0.0004} per hour |

**Readings against §5's figures.** Two figures the lab does not print were re-derived for this
report by `/tmp/tz48/probe/figs.py`, quoted in V-A: W1's |z| and C1.

| # | §5 registers | 3 seeds | 10 seeds | Divergence |
|---|---|---|---|---|
| W1 | every coin-date `stress`; |z| ≥ 2.5e13 | 1404 / 1404 `stress`; `overlap` undefined, both cells named empty; volatility ≤ 7.8e-16 | 4680 / 4680 `stress`; volatility ≤ 8.3e-16; min |z| **2.055e13** | **|z| floor 2.06e13, not 2.5e13.** This fixture draws a slope per coin; TZ-47 used one slope, 0.001. `stress` fires at `REG_STRESS_Z` 2.0, twelve orders below either figure. |
| W2 | `trend` on every coin-date; `range` empty | 1404 / 1404 `trend`; `overlap` undefined (`range` named empty) | 4680 / 4680 | none |
| W3 | `range` on every coin-date; `trend` empty; `overlap` undefined and said so | 1404 / 1404 `range`; «пуста ячейка trend» | 4680 / 4680 | none |
| W4 | `overlap` 0.000 | 0.000 on 3 / 3 (range 634, trend 707, stress 63) | **0.000 on 10 / 10** (range 2072, trend 2391, stress 217) | none. TZ-47 read range 2069, trend 2385, stress 226 on its own draws. |
| W5 | `overlap` 1.000 | 1.000 on 3 / 3 (range 702, trend 702) | **1.000 on 10 / 10** (range 2340, trend 2340) | none. The null's median is 0.868–0.889. |
| W6 | cannot reach all-`range`; P(|eff| < EFF_TREND) bounded near 0.45 | no coin wholly `range` (36 coin-seeds); driftless `range` share 0.453 | no coin wholly `range` (120 coin-seeds); driftless share **0.468** | **At 10 seeds the driftless share is 0.468, 0.017 above the Gaussian 0.451.** The share's denominator is every coin-date of the driftless coins, `stress` included. `eff` divides a 14-day simple return by a 90-day volatility estimate, so it is not exactly N(0, 1). The structural claim holds on every coin and seed. The figure itself is not asserted. |
| C1 | `overlap` against its same-run null, no band; TZ-47 read 0.031 mean / 0.079 max on a driftless 4×-volatility world | — | rebuilt world, same construction: **`overlap` 0.023 mean / 0.071 max**; null median 0.019 mean / 0.045 max; `id_diff` 0 on every seed | **Different values, same order.** The rebuilt world draws its noise in a different order from TZ-47's probe, so these are different samples of the same construction. |

### 6. Truncation invariance

E2, on W4 seed 1:

- **468 records.** Each coin-date's `cd` was rebuilt from the series truncated at its own date
  with `CdBuilder`, and compared by `json.dumps(…, sort_keys=True)` against the record the
  driver consumed.
- **468 words.** The recorded field was compared with production's word on the truncated record.
- **39 dates.** Every census statistic of the date was compared: counts, quartiles, `overlap`,
  and the null's median, spread and undefined count.

That is **975 comparisons, all byte-identical**, and it holds at both seed counts.

### 7. Identity

E3's three numbers:

- `--target` against the pre-change driver: **0** differences over 425 fields (and 0 over 100
  report lines);
- `--regime-gate` against the pre-change driver: **0** differences over 1649 fields (and 0 over
  250 report lines);
- the same comparator against one deliberately perturbed field: **1** and **1**.

The pre-change side is `TARGET_DRIVER` with `TGT_OWN_JS` removed. It is shown to lack the field
(0 of 2460 observations carry `own`), and the field-present side carries it on 2460 of 2460.

The world is named in the output: `synth_hl «normal»`, its first coin as BTC. The identity holds
there unconditionally, because no arm and no market-word split reads the new field. The
`--regime-gate` output gains the 233-line coin-word section, reported as added lines and not as
differences.

**Session evidence against the PRISTINE file.** This goes beyond E3, which compares the new code
with itself minus one line. The same seeded world, `synth_hl("normal", seed=11)`, was run through
`--target` and `--regime-gate` exactly as `main()` builds them (with `BetaWalk`, `excluded = {}`).
Each run was a separate process, one on the pristine module and one on the changed module. The
scripts are in V-B.

```
pristine src md5 ba633202f43845ba0fdafbc1b92d9c04 | changed src md5 ed4db7c2bab9076e92982c664c6fc2f6
--target summary: fields compared 425, differing 0, missing in changed 0, added in changed 0
--regime-gate summary: fields compared 2151, differing 0, missing in changed 0, added in changed 0
--target report: lines pristine 100 changed 100, differing over pristine lines 0, text identical True
--target json: bytes 9067 / 9067 identical True
--regime-gate report: lines pristine 248 changed 481, differing over pristine lines 0, changed text starts with pristine text True, added lines 233
--regime-gate json.dump: pristine 'TypeError: keys must be str, int, float, bool or None, not tuple' | changed 'TypeError: keys must be str, int, float, bool or None, not tuple' | partial bytes 47073 / 47073 identical True
```

(`/tmp/tz48/ident_cmp.txt`, MD5 `f199127f53193c740910410cc9ff50fb`.)

### 8. Dependence on the constant

E4, on W4 seed 1, raising `EFF_TREND` inside the cut bundle from 0.60 (read from `index.html`) to
0.90. The populations as `range / trend / stress`:

- before: **222 / 223 / 23**;
- after: **297 / 148 / 23**.

Exactly 75 coin-dates moved `trend` → `range`. None left `range`, and none entered or left
`stress`. How this check is written is Deviation 2.

### 9. Negative control

The one trend comparison in `index.html` was inverted, `>=` → `<`, asserted to occur exactly once.
The full lab then ran with the workflow's command, and the file was reverted. The script is in
V-C (`/tmp/tz48/negctl.sh`, MD5 `661dc455b56917f4426f97a07d1895bb`). Its output:

```
before: 4e71da9badca3ccae85b656fdc3773e8  index.html
occurrences of the trend comparison: 1
mutated: aafaf1c81db7921408071ca06d4494d2  index.html
-    if (out.eff !== null && Math.abs(out.eff) >= EFF_TREND) {
+    if (out.eff !== null && Math.abs(out.eff) < EFF_TREND) {
inverted lab exit 1 secs 356
inverted line inside the cut bundles: _tgt_bridge.js 1 · _own_bridge.js 1
after revert: 4e71da9badca3ccae85b656fdc3773e8  index.html
git status --porcelain lines: 0
script exit 0
```

Section E under the inversion (`/tmp/tz48/negctl_lab.txt`, MD5 `0c591c457fcb6718c473b59b50e297bc`):

```
E · --regime-gate, слово монеты
  E0 деление по наблюдениям: каждое в одном виде, дата без своего слова из вида выпала, запись без слова отвергнута ОК
  E0 края сетки: популяция из одной даты — «сетапов 1 на 1 датах (дат в популяции 1) — пул не собран» · ни одного сетапа — «сетапов 0 на 0 датах (дат в популяции 6) — пул не собран» · сравнений 0, decidable false ОК
  E0 волатильности нет: та же запись с волатильностью — stress, без неё — range (known:false) · в мире с плоской монетой её монето-дат в записи 0, остальных монет 3 ОК
  E1 W1 гладкий подъём — только stress: посевов 3 · монето-дат 1404 · range 0 · trend 0 · stress 1404 · overlap — — — (пуста ячейка range и trend) · нуль — — — · волатильность не выше 7.8e-16 ОК
  E1 W2 лестница — только trend: посевов 3 · монето-дат 1404 · range 1404 · trend 0 · stress 0 · overlap — — — (пуста ячейка trend) · нуль — — — СТОП
  E1 W3 зигзаг — только range, overlap не определён: посевов 3 · монето-дат 1404 · range 0 · trend 1404 · stress 0 · overlap — — — (пуста ячейка range) · нуль — — — СТОП
  E1 W4 блуждание с одной волатильностью — overlap 0: посевов 3 · монето-дат 1404 · range 707 · trend 634 · stress 63 · overlap 1.000 1.000 1.000 · нуль 1.000 1.000 1.000 СТОП
  E1 W5 лестницы и зигзаги поровну — overlap 1: посевов 3 · монето-дат 1404 · range 702 · trend 702 · stress 0 · overlap 0.000 0.000 0.000 · нуль 0.000 0.000 0.000 СТОП
  E1 W6 броуновские σ × снос — ни одна монета не вся в range: посевов 3 · монето-дат 1404 · range 753 · trend 544 · stress 107 · overlap 1.000 1.000 1.000 · нуль 0.989 1.000 1.000 · доля range у монет без сноса 0.490, для справки P(|N(0,1)| < EFF_TREND) = 0.451 ОК
  E2 усечение на дате (W4, посев 1): записей 468, расхождений 0 · слов 468, расхождений 0 · дат со статистикой переписи 39, расхождений 0 ОК
  E3 тождество (мир D: synth_hl «normal», первая монета — BTC; безусловно — ни рукав, ни деление по слову рынка не читают новое поле): наблюдений с полем 2460 из 2460, в прогоне без поля 0 из 2460
     --target: полей 425, расхождений 0, пропало 0, добавлено 0 · строк отчёта 100, расхождений 0
     --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 233
     тот же сравниватель против возмущённого поля: --target расхождений 1 · --regime-gate расхождений 1 (120|1.5|long|range) ОК
     сетка слова монеты на тех же проходах: ячеек 144 (у слова рынка 144) · монето-дат 1245 · range 605 · trend 575 · stress 65 · decidable true ОК
  E4 EFF_TREND 0.60 → 0.90 в вырезанном бандле (W4, посев 1): range/trend/stress 223/222/23 → 148/297/23 · trend→range 0 (нужно > 0) · range→другое 75 (должно 0) · stress сменило слово 0 (должно 0) СТОП
  E сравнений 4255, отказов 97 СТОП
ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить
```

**Against §6 item 5's written partition:**

| Partition | Item | Required | Measured |
|---|---|---|---|
| must turn red | W2 | red | **СТОП** |
| must turn red | W5 | red | **СТОП** |
| must turn red | control 4 (E4) | red | **СТОП** |
| must NOT fire | control 2 (E2) | green, inverted code on both sides | **ОК** |
| must NOT fire | control 3 (E3, all four lines) | green, inverted code on both sides | **ОК** |
| not named | W3, W4 | — | СТОП, СТОП |
| not named | W1, W6, E0 (three lines) | — | ОК |

The partition holds exactly.

- **Failure count.** The 97 failures break down as W2 6 (2 per seed), W3 9 (3 per seed), W4 3,
  W5 3, and E4 76: 75 rows that left `range`, plus `trend→range` = 0.
- **Comparison count.** 4255 against 4254 is E4's base `range` population, 223 rows inverted
  against 222.
- **Sections A–D.** One line moved under the inversion, D7's date counts, from
  `range 34 · trend 45 · stress 4` to `range 45 · trend 34 · stress 4`. Every D check stayed ОК.
- **Revert.** After the revert `index.html` is back at `4e71da9b…`, and `git status --porcelain`
  printed nothing.

### 10. The archive was not read

- No fetch, no dispatch, and no figure from real data.
- Every run in this report used synthetic series built in the process: `synth_hl`, `synth_own`,
  and the probe's rebuilt world.
- `bench/cache` does not exist in the worktree or in either `/tmp` copy
  (`ls: cannot access 'bench/cache': No such file or directory`).
- No `--fetch`, `--target`, `--regime-gate` or `--verify` mode was invoked; those are the modes
  that read the cache or the network.

### 11. CI

Two `Bench gate` runs, both on `4a11c8bf1c8e213221676c8d16cac2b24645fa68`, both read
(`## CI Execution`):

| Run | Event | Conclusion |
|---|---|---|
| `35167655239` | push | **success** |
| `35168048279` | pull_request | **success** |

Every step concluded `success`, and the runner's own logs print gate step 4 **59 / FAIL 0** and
gate step 14 **487 / FAIL 0**. `backtest_bench.yml` is `workflow_dispatch` only and did not run,
so section E has no runner reading (`## Remaining Risks`).

### 12. Reading items

**Reading item 1: `.github/workflows/backtest_bench.yml`.**

A step runs `--regime-gate`, and only when a dispatch sets the boolean input. Its printed text is
retained; its JSON is not.

The input (`:15`–`:18`):

```yaml
      regime_gate:
        description: "ТЗ-32: ворота режима на архиве (--regime-gate)"
        type: boolean
        default: false
```

The step (`:89`–`:94`):

```yaml
      - name: Ворота режима на архиве (--regime-gate)
        if: ${{ inputs.regime_gate }}
        run: |
          cd bench
          python backtest_bench.py --regime-gate \
            --html ../index.html --bot ../main.py 2>&1 | tee regime_gate.txt
```

The upload (`:147`–`:168`) runs with `if: always()`, and its `path` list includes both
`bench/regime_gate.txt` and `bench/regime_gate_raw.json`.

What the TZ asks, answered:

- **Retained?** Only as text. `tee` keeps everything the mode prints, including the coin-word
  section, which prints before the dump. The JSON is not retained: the mode's
  `json.dump(sm, …)` raises `TypeError: keys must be str, int, float, bool or None, not tuple` on
  the tuple-keyed `sm["agree"]`, and leaves a truncated file behind (Pre-existing Issue 1).
- **Reachable?** Only through the dispatch input, whose default is `false`.
- **Consequence under the job's `bash -euo pipefail` shell.** The step fails after printing. The
  next four steps carry no `if:` and are therefore skipped: `--res7`, `--funding`, `Прогон` and
  `Сверка`. `--attrib` and `Деление по режиму BTC` still run (`if: ${{ !cancelled() }}`), and so
  does the upload.

By the TZ's own rule, the JSON's retention is the next TZ, not this one.

**Reading item 2: `bench/backtest_guard_bench.py`, gate step 14.**

Yes. One assertion pins the driver's record shape, and a change written as §4.1's words place it
would falsify it. Check 33 (`:878`–`:892`):

```python
# ── 33. and WITHOUT the grid the driver adds nothing: the untouched path is
# byte-identical, which is the assertion ТЗ-32 §6.2 rests on.
...
ok('33. and the untouched keys of the answer are unchanged',
   r_no[0] is not None and r_no[1] is not None
   and sorted(r_no[0]) == sorted(r_no[1]) == ['dist', 'moneyBelowMin', 'ok',
                                              'prod', 'reg', 'stop', 'subs'],
   None if not r_no[0] else sorted(r_no[0]))
```

A field beside `reg` makes the answer's keys
`['dist', 'moneyBelowMin', 'ok', 'own', 'prod', 'reg', 'stop', 'subs']`. That was measured on a
discarded `/tmp` prototype (V-D):

```
checks run: 487   FAIL 1
  FAIL: 33. and the untouched keys of the answer are unchanged  [['dist', 'moneyBelowMin', 'ok', 'own', 'prod', 'reg', 'stop', 'subs']]
```

Nothing else moves:

- **Check 43** (`:1183`–`:1186`) asserts `prod` is a *superset* of the anchor pair
  (`all(k in r_on['prod'] for k in ('anchor', 'waiting', 'anchorStop', 'anchorDist', 'pA'))`), so
  a key inside `prod` does not falsify it.
- **The `reg` fixtures** (`rg_obs`, `:659`) carry no `own` and are read by `_rg_word`, `_rg_split`
  and `regime_gate_summary` (check 30b, `:777`), on the market-word path. That path reads no
  `own`, and `splitter` defaults to `_rg_split`.
- **No other check** reads `_rg_word` or the record shape.

With the field inside `prod`, step 14 prints `487 / FAIL 0`. Its output is byte-identical to the
pre-change run (MD5 `d91178acbed79648100d6b07b2f88c2c` both) and identical on the runner. The file
was not edited.

**Reading item 3: the dispatch cache key.** It is unchanged: `key:
bench-${{ inputs.source }}-${{ inputs.years }}y-v4` (`backtest_bench.yml:41`). It is out of scope,
for the reason TZ-47 §8 gave. It is recorded under `## Pre-existing Issues`.

### V-A. Figure re-derivation probe

`/tmp/tz48/probe/figs.py`, 47 lines, MD5 `2e87eb0468ec1c2426b2047acf9b1d8b`. It imports a `/tmp`
copy of the committed file, so the bridge files it writes stay outside the repository.

```python
"""TZ-48 report-only re-derivation of §5's figures that the lab does not print:
W1's |z| floor and C1's overlap on a driftless 4x-volatility world, both on records
built by run_target with the changed bench (field prod.own), 10 seeds."""
import sys, math
import numpy as np
sys.path.insert(0, "/tmp/tz48/work/bench")
import backtest_bench as bb
HTML, BOT = "/tmp/tz48/work/index.html", "/tmp/tz48/work/main.py"
ZDRV = r"""
var fs = require('fs');
__EXTRACTED__
var job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
var out = [];
for (var i = 0; i < job.length; i++) { var g = marketRegime(job[i]); out.push([g.mode, g.z, g.eff, g.known]); }
fs.writeFileSync(process.argv[3], JSON.stringify(out));
"""
zb = bb.JsBridge(HTML, bb.TARGET_JS_FUNCS, bb.TARGET_JS_VARS, ZDRV, "_z_probe.js")
zmin, n1, modes = float("inf"), 0, {}
for sd in range(1, 11):
    ser, bt = bb.synth_own("smooth", seed=sd)
    rows, _ = bb._own_rows(bb.run_target(ser, BOT, HTML, bt, k_grid=[], verbose=False))
    cds = [cd for t in rows for _, _, cd in rows[t]]
    for mode, z, eff, known in zb.call(cds):
        n1 += 1; modes[mode] = modes.get(mode, 0) + 1
        zmin = min(zmin, abs(z)) if z is not None else zmin
print("W1 smooth, 10 seeds: coin-dates %d, modes %s, min |z| %.3e (REG_STRESS_Z %.1f)"
      % (n1, modes, zmin, bb._read_js_num(HTML, "REG_STRESS_Z")))
def hetvol(seed, n_coins=12, hours=8760):
    rng = np.random.default_rng(seed); t0 = 1700000000000
    ts = [t0 + (i + 1) * bb.HOUR_MS for i in range(hours)]
    def ser(lp):
        p = 10.0 * np.exp(lp)
        return {"prices": [[ts[i], float(p[i])] for i in range(hours)],
                "volumes": [[ts[i], 1e7] for i in range(hours)],
                "hl": [[ts[i], float(p[i]), float(p[i])] for i in range(hours)]}
    s = {"C%02d" % c: ser(np.cumsum(rng.normal(0, (0.004, 0.008, 0.016)[c % 3], hours))) for c in range(n_coins)}
    return s, ser(np.cumsum(rng.normal(0, 0.004, hours)))
ov, nl = [], []
for sd in range(1, 11):
    ser, bt = hetvol(sd)
    c = bb.own_census(bb.run_target(ser, BOT, HTML, bt, k_grid=[], verbose=False), HTML)
    ov.append(c["overlap"]); nl.append(c["null"]["med"])
    print("  hetvol seed %2d: range %d trend %d stress %d | overlap %s | null median %s spread %s | id_diff %d"
          % (sd, c["words"]["range"]["n"], c["words"]["trend"]["n"], c["words"]["stress"]["n"],
             c["overlap"], c["null"]["med"], c["null"]["ci"], c["id_diff"]))
print("C1 driftless 0.004/0.008/0.016 world, 10 seeds: overlap mean %.3f max %.3f | null median mean %.3f max %.3f"
      % (np.mean(ov), max(ov), np.mean(nl), max(nl)))
```

Output (`/tmp/tz48/figs.txt`, MD5 `3d7288b8755dae2590409c54e8877b4b`; closure lines filtered), exit 0, 40 s:

```
W1 smooth, 10 seeds: coin-dates 4680, modes {'stress': 4680}, min |z| 2.055e+13 (REG_STRESS_Z 2.0)
  hetvol seed  1: range 222 trend 222 stress 24 | overlap 0.02252252252252252 | null median 0.02666666666666667 spread [0.004328537841468876, 0.06060606060606061] | id_diff 0
  hetvol seed  2: range 197 trend 253 stress 18 | overlap 0.07106598984771574 | null median 0.04504504504504504 spread [0.013888888888888888, 0.08597285067873303] | id_diff 0
  hetvol seed  3: range 214 trend 237 stress 17 | overlap 0.014018691588785047 | null median 0.017467248908296942 spread [0.0, 0.048040201486248345] | id_diff 0
  hetvol seed  4: range 185 trend 259 stress 24 | overlap 0.032432432432432434 | null median 0.01431989063568011 spread [0.0, 0.04326923076923077] | id_diff 0
  hetvol seed  5: range 200 trend 241 stress 27 | overlap 0.0 | null median 0.0 spread [0.0, 0.004830917874396135] | id_diff 0
  hetvol seed  6: range 213 trend 237 stress 18 | overlap 0.018779342723004695 | null median 0.01702127659574468 spread [0.0, 0.046813511547554074] | id_diff 0
  hetvol seed  7: range 200 trend 244 stress 24 | overlap 0.035 | null median 0.02625833141806481 spread [0.004347826086956522, 0.059914767878477514] | id_diff 0
  hetvol seed  8: range 214 trend 231 stress 23 | overlap 0.02336448598130841 | null median 0.02262443438914027 spread [0.0, 0.05429864253393665] | id_diff 0
  hetvol seed  9: range 234 trend 221 stress 13 | overlap 0.0 | null median 0.012295081967213115 spread [0.0, 0.03966445218132718] | id_diff 0
  hetvol seed 10: range 190 trend 248 stress 30 | overlap 0.010526315789473684 | null median 0.004739336492890996 spread [0.0, 0.032867725219239946] | id_diff 0
C1 driftless 0.004/0.008/0.016 world, 10 seeds: overlap mean 0.023 max 0.071 | null median mean 0.019 max 0.045
```

### V-B. Identity probe against the pristine file

The probe is two scripts, run as follows:

```
python3 ident_side.py /tmp/tz48/probe /tmp/tz48/pristine/index.html /tmp/tz48/pristine/main.py /tmp/tz48/ident_pristine.pkl
python3 ident_side.py /tmp/tz48/work/bench /tmp/tz48/work/index.html /tmp/tz48/work/main.py /tmp/tz48/ident_changed.pkl
python3 ident_cmp.py /tmp/tz48/ident_pristine.pkl /tmp/tz48/ident_changed.pkl
```

In the first command, `/tmp/tz48/probe/backtest_bench.py` is the pristine file (`ba633202…`). In
the second, `/tmp/tz48/work/bench/backtest_bench.py` is the committed file (`ed4db7c2…`). Both
sides ran in 228 s together.

`ident_side.py`, 38 lines, MD5 `bfcec6497a90ad3504595bb8d9335bd8`:

```python
"""One side of the pristine-vs-changed identity probe (TZ-48 validation 7).
argv: <dir holding backtest_bench.py> <html> <bot> <out.pickle>
Runs --target's and --regime-gate's construction exactly as main() does, minus the
archive (a seeded synthetic world) and minus the reconciliation (excluded = {})."""
import sys, io, contextlib, json, pickle
sys.path.insert(0, sys.argv[1])
import backtest_bench as bb
HTML, BOT, OUT = sys.argv[2], sys.argv[3], sys.argv[4]
def printed(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a)
    return buf.getvalue()
w = bb.synth_hl("normal", seed=11)
btc = w.pop(sorted(w)[0])
res = {"md5_src": __import__("hashlib").md5(open(bb.__file__, "rb").read()).hexdigest()}
# --target, as main(): run_target(ser, bot, html, btc, betawalk=BetaWalk(bot, btc prices))
sm_t = bb.target_summary(bb.run_target(w, BOT, HTML, btc, betawalk=bb.BetaWalk(BOT, btc["prices"]), verbose=False),
                         HTML, excluded={})
res["t_sm"] = sm_t
res["t_txt"] = printed(bb.report_target, sm_t)
buf = io.StringIO(); json.dump(sm_t, buf); res["t_json"] = buf.getvalue()
# --regime-gate, as main()
by_H = bb.run_regime_grid(w, BOT, HTML, btc, betawalk=bb.BetaWalk(BOT, btc["prices"]), verbose=False)
sm_g = bb.regime_gate_summary(by_H, btc, HTML, excluded={})
res["g_sm"] = sm_g
txt = printed(bb.report_regime_gate, sm_g)
if hasattr(bb, "report_own_regime"):
    txt += printed(bb.report_own_regime, bb.own_regime_summary(by_H, HTML, excluded={}))
res["g_txt"] = txt
buf = io.StringIO()
try:
    json.dump(sm_g, buf); res["g_json_err"] = None
except Exception as e:
    res["g_json_err"] = "%s: %s" % (type(e).__name__, e)
res["g_json_partial"] = buf.getvalue()
pickle.dump(res, open(OUT, "wb"))
print("side done", res["md5_src"])
```

`ident_cmp.py`, 28 lines, MD5 `64e488190fc35e087426831bc37b2024`:

```python
import pickle, sys
def fields(x, path=()):
    if isinstance(x, dict) and x:
        out = {}
        for k in x: out.update(fields(x[k], path + (repr(k),)))
        return out
    if isinstance(x, (list, tuple)) and x:
        out = {}
        for i, v in enumerate(x): out.update(fields(v, path + (i,)))
        return out
    return {path: repr(x)}
a = pickle.load(open(sys.argv[1], "rb")); b = pickle.load(open(sys.argv[2], "rb"))
print("pristine src md5", a["md5_src"], "| changed src md5", b["md5_src"])
for tag in ("t", "g"):
    fa, fb = fields(a[tag + "_sm"]), fields(b[tag + "_sm"])
    shared = [p for p in fa if p in fb]
    print("%s summary: fields compared %d, differing %d, missing in changed %d, added in changed %d"
          % ({"t": "--target", "g": "--regime-gate"}[tag], len(shared), sum(1 for p in shared if fa[p] != fb[p]),
             sum(1 for p in fa if p not in fb), sum(1 for p in fb if p not in fa)))
la, lb = a["t_txt"].split("\n"), b["t_txt"].split("\n")
print("--target report: lines pristine %d changed %d, differing over pristine lines %d, text identical %s"
      % (len(la), len(lb), sum(1 for x, y in zip(la, lb) if x != y), a["t_txt"] == b["t_txt"]))
print("--target json: bytes %d / %d identical %s" % (len(a["t_json"]), len(b["t_json"]), a["t_json"] == b["t_json"]))
la, lb = a["g_txt"].split("\n"), b["g_txt"].split("\n")
print("--regime-gate report: lines pristine %d changed %d, differing over pristine lines %d, changed text starts with pristine text %s, added lines %d"
      % (len(la), len(lb), sum(1 for x, y in zip(la, lb) if x != y), b["g_txt"].startswith(a["g_txt"]), len(lb) - len(la)))
print("--regime-gate json.dump: pristine %r | changed %r | partial bytes %d / %d identical %s"
      % (a["g_json_err"], b["g_json_err"], len(a["g_json_partial"]), len(b["g_json_partial"]), a["g_json_partial"] == b["g_json_partial"]))
```

### V-C. Negative-control script

`/tmp/tz48/negctl.sh`, 29 lines, MD5 `661dc455b56917f4426f97a07d1895bb`:

```bash
#!/bin/bash
# TZ-48 §6 item 5 · negative control. Inverts the trend comparison in index.html (the
# source every bundle is cut from), runs the lab exactly as backtest_bench.yml does,
# then reverts and proves the tree clean.
set -u
cd /root/crypto-auto/.claude/worktrees/bridge-cse_015FW2PzAw8V2nHSWur4mBbN
OLD='    if (out.eff !== null && Math.abs(out.eff) >= EFF_TREND) {'
NEW='    if (out.eff !== null && Math.abs(out.eff) < EFF_TREND) {'
echo "before: $(md5sum index.html)"
echo "occurrences of the trend comparison: $(grep --count --fixed-strings -- "$OLD" index.html)"
python3 - "$OLD" "$NEW" <<'PY'
import sys
old, new = sys.argv[1], sys.argv[2]
src = open("index.html", encoding="utf-8").read()
assert src.count(old) == 1, src.count(old)
open("index.html", "w", encoding="utf-8").write(src.replace(old, new))
PY
echo "mutated: $(md5sum index.html)"
git diff -U0 index.html | grep '^[-+] '
cd bench
s=$(date +%s)
python3 backtest_bench.py --lab-selftest --html ../index.html --bot ../main.py > /tmp/tz48/negctl_lab.txt 2>&1
echo "inverted lab exit $? secs $(( $(date +%s)-s ))"
echo "inverted line inside the cut bundles: _tgt_bridge.js $(grep --count --fixed-strings -- "$NEW" _tgt_bridge.js) · _own_bridge.js $(grep --count --fixed-strings -- "$NEW" _own_bridge.js)"
cd ..
git checkout -- index.html
echo "after revert: $(md5sum index.html)"
echo "git status --porcelain lines: $(git status --porcelain | wc -l)"
git status --porcelain
```

### V-D. The literal §4.1 placement, measured on a discarded prototype

The builder below was run from the worktree. It writes `/tmp/tz48/r1/bench/backtest_bench.py`,
which moves the one field line to sit beside `reg` at the top level and adjusts the two sites that
name it. Nothing in the repository was written.

```python
src = open("bench/backtest_bench.py", encoding="utf-8").read()
inner = "                      own: wordOut(marketRegime(j.cd)),\n"
reg = "              reg: marketRegime(j.btcStats).mode,\n"
top = "              own: wordOut(marketRegime(j.cd)),\n"
assert src.count(inner) == 1 and src.count(reg) == 1
out = src.replace(inner, "").replace(reg, reg + top)
lit_old = 'TGT_OWN_JS = "                      own: wordOut(marketRegime(j.cd)),\\n"'
lit_new = 'TGT_OWN_JS = "              own: wordOut(marketRegime(j.cd)),\\n"'
assert out.count(lit_old) == 1
out = out.replace(lit_old, lit_new)
rd_old = '            if "own" in r["prod"]:\n                o["own"] = r["prod"]["own"]'
assert out.count(rd_old) == 1
out = out.replace(rd_old, '            if "own" in r:\n                o["own"] = r["own"]')
open("/tmp/tz48/r1/bench/backtest_bench.py", "w", encoding="utf-8").write(out)
print("R1 prototype written")
```

The guard was then run against that copy:

```
$ python3 bench/backtest_guard_bench.py /tmp/tz48/r1/bench/backtest_bench.py index.html
checks run: 487   FAIL 1
  FAIL: 33. and the untouched keys of the answer are unchanged  [['dist', 'moneyBelowMin', 'ok', 'own', 'prod', 'reg', 'stop', 'subs']]
guard on R1 exit 1
```

The same guard on the committed file: `checks run: 487   FAIL 0`, exit 0.

## Test Results

- **Fingerprint gate: pass.** 7 of the table's 7 rows compared, 0 mismatches, revision
  `**Revision 2026-09-16-b.**` as required.
- **`py_compile`:** exit 0.
- **Diff scope:** `bench/backtest_bench.py` only.
- **`--selftest`:** exit 0 before and after; output byte-identical; 36 comparisons both times.
- **`--lab-selftest`, 3 seeds:** exit 0. Sections A–D identical to before; section E
  **4254 / 0**.
- **`--lab-selftest`, 10 seeds:** exit 0. Section E **4562 / 0**.
- **W1–W6:** every structural claim holds at 3 and 10 seeds. W1's |z| floor diverges (2.06e13
  against 2.5e13), W6's driftless share diverges (0.468 against 0.451), and C1's figures diverge
  (0.023 / 0.071 against 0.031 / 0.079).
- **Truncation invariance:** 975 comparisons, all byte-identical.
- **Identity:** `--target` 0 differences, `--regime-gate` 0, the perturbed field 1 and 1. Against
  the pristine file: 425 / 0 and 2151 / 0 fields; `--target` text and JSON identical;
  `--regime-gate` text a byte prefix.
- **Constant dependence:** 222 / 223 / 23 → 297 / 148 / 23; 75 rows moved `trend` → `range`,
  0 moved against the direction.
- **Negative control:** exactly the written partition (W2, W5, E4 red; E2, E3 green); W3 and W4
  also red. Tree clean after the revert.
- **Gate step 4, `verify_bench.py`:** 59 / FAIL 0, locally and on the runner; local output
  byte-identical to before.
- **Gate step 14, `backtest_guard_bench.py`:** 487 / FAIL 0, locally and on the runner; local
  output byte-identical to before. The literal §4.1 placement reads 487 / FAIL 1.
- **Hosted `Bench gate`:** 2 runs, both `success`.

## Deviations

**Deviation 1: the driver field is inside `prod`, not beside `reg`.**

- **Text.** §4.1: «Beside the existing `reg`, record the coin's own word: `marketRegime(j.cd)`,
  taking `mode` and `dir`.»
- **Reading A, literal: `own` as a top-level key of the driver's answer, a sibling of `reg`.** It
  touches the same file, and it falsifies gate step 14 check 33, which pins that answer's key set
  exactly. Measured: **487 / FAIL 1** (V-D). The only ways to keep step 14 green under reading A
  are to edit check 33, which is hard floor items 2 and 12 and forbidden by §7 item 2 («Do not
  edit it»), or to leave it red, which `## Touches` names «a defect of this change».
- **Reading B, implemented: `own` inside `prod`; the observation carries `o["own"]` beside
  `o["reg"]`.** The field is still one field in the driver, computed on the whole `j.cd` and
  taking `mode` and `dir`. The value that reaches every reader is identical; only its path inside
  the driver's answer differs. Gate step 14 reads 487 / FAIL 0, locally and on the runner. TZ-36
  placed its anchor pair inside `prod` too, and its driver comment names the same property: «ни
  один ключ верхнего уровня не добавлен».
- **Why it is recorded, not BLOCKED.** Reading B is the only reading that satisfies §4.1's
  content, `## Touches` and §7 item 2 together, and no existing assertion changes under it. The
  Architect can overrule it in one line; the move is the V-D diff.

**Deviation 2: control 4 asserts the move's direction.**

- **Text.** §6 item 4: «Perturb `EFF_TREND` in the extracted bundle and assert the coin-word
  populations MOVE.» §6 item 5 lists control 4 under «Must turn red» for the inverted comparison.
- **Measured.** A movement-only assertion cannot satisfy item 5. Under the inversion the
  populations still move: 223 / 222 / 23 → 148 / 297 / 23, 75 coin-dates (V-C, §9). TZ-47's
  report measured the same (its V-3).
- **Implemented.** E4 asserts the move and its direction:
  - some coin-dates must move `trend` → `range` («нужно > 0»);
  - none may leave `range` when the cut rises;
  - `stress`, tested first, may not change.

  In production that reads 75 / 0 / 0 and is green. Inverted, it reads 0 / 75 / 0 and is red, as
  item 5 requires.
- **Why.** «Positive dependence on the constant» is satisfied more strictly, never less. Every
  movement-only failure still fails. Nothing else in the TZ's text changes.

No other written clause was departed from. The §2-sentence note under `## Implementation Summary`
lists the additions later clauses required.

## Pre-existing Issues

1. **`--regime-gate` cannot write `regime_gate_raw.json`.**
   - **Defect.** `regime_gate_summary` stores the labeller agreement as a dict keyed by
     `(word, word)` tuples (`_rg_agree`). `main()` then calls `json.dump(sm, …)`, which raises
     `TypeError: keys must be str, int, float, bool or None, not tuple` after writing a truncated
     file.
   - **Proved pre-existing** on the pristine file, twice:
     - a fixture on `ba633202…` (`/tmp/tz48/jsonchk/chk.py`, MD5
       `c42e8fc079a3c740b3d9f47969d96af1`), output:

       ```
       agree keys: [(('trend', 'нет метки'), 30), (('range', 'нет метки'), 30)] agree_dates 60
       json.dump raised: TypeError keys must be str, int, float, bool or None, not tuple
       partial file bytes: 3428
       ```

     - the identity probe, which raised identically on both files, with a byte-identical partial
       dump of 47 073 bytes (§7).
   - **Consequence on a dispatch with `regime_gate: true`.** The step exits non-zero after printing
     its report. `--res7`, `--funding`, `Прогон` and `Сверка` are skipped, while `--attrib` and
     `Деление по режиму BTC` still run. The artifact carries an unparseable JSON.
   - **Unobserved so far.** No map revision records a `--regime-gate` dispatch reading.
   - **Not fixed.** §4.5 forbids moving the mode's existing output, and the fix is the next TZ
     under §7 item 1's own rule.
2. **The dispatch cache key is frozen:** `key: bench-${{ inputs.source }}-${{ inputs.years }}y-v4`
   (`backtest_bench.yml:41`), unchanged. Per §7 item 3, it stays out of scope for the reason TZ-47
   §8 gave: the first coin-word reading is taken on the same fetch discipline every standing
   figure was taken on.
3. **The `--html` and `--bot` defaults name files that do not exist**
   (`bench/Скрипт_Код_CriptoCalculator.html`, `bench/Код_для_Bota_на_GitHub.py`). Every command in
   this report was taken from `backtest_bench.yml`, which passes both paths explicitly. Known and
   unchanged.

## Remaining Risks

- **Section E has no runner reading.** `--lab-selftest` runs only under `backtest_bench.yml`,
  which is `workflow_dispatch` only. Every green in section E is a local reading until a dispatch
  runs it (inv. 62). Gate step 14 carries no section for the new code, because the TZ placed its
  controls in the lab.
- **The coin-word reading is retained as text only** while Pre-existing Issue 1 stands. A dispatch
  that enables `regime_gate` today also loses four downstream steps.
- **Cost on the archive is unmeasured.**
  - Locally, `--lab-selftest` went from 194 s to 354 s at the default seeds.
  - On the archive, `--regime-gate` gains a second cell-bootstrap pass (on section D's world,
    `regime_gate_summary` took 31 s) and a census table of n² words per date (about 140 000 words
    at 30 coins × 156 dates).
  - `o["cd"]` keeps each coin-date's record alive for the whole run.
  - None of this has been measured on a runner.
- **W6's figure is not asserted.** At 10 seeds the driftless `range` share read 0.468, above the
  Gaussian 0.451. W6 asserts only «no coin wholly `range`».
- **E3's identity names its world.** It holds because nothing reads `own`. An arm or split that
  later reads the field turns E3 into a partition case (inv. 69).
- **An extra stderr warning.** The lab prints numpy's `All-NaN slice encountered` a second time,
  from E3's pre-change `regime_gate_summary` on section D's world (the same cell D7's summary warns
  on). It is stderr, not a failure.
- **`TGT_OWN_JS` matches the field line exactly.** An edit to that line without the constant
  raises at import. That is by design, so the identity control can never compare against a driver
  that still carries the field.

## Commit

**Implementation.**

- **Commit:** `4a11c8bf1c8e213221676c8d16cac2b24645fa68`, pushed to
  `origin/claude/tz-48-own-regime-gate`.
- **Contents:** `bench/backtest_bench.py`, modified, 702 lines added and 9 deleted.
- **Message** (the TZ's `## Commit Message`, verbatim, plus the attribution line):

```
TZ-48: the coin's own regime word through the existing gate — one driver field, one population view

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

**Report.** One commit on `main`, on the `CryptoReports/**` direct-push path (contract §8). The
workflow filters were read before the push:

- `main.yml`'s `push` is a `paths` allow-list of exactly `main.py` and `.github/workflows/main.yml`;
- `bench.yml`'s `push` carries `'**.md'` under `paths-ignore`;
- `calib.yml`'s `push` is limited to `claude/**` branches and two paths;
- `journal.yml` is `schedule` / `workflow_dispatch`;
- `backtest_bench.yml` is `workflow_dispatch` only.

Message:

```
docs(reports): TZ-48 — the coin's own regime word through the existing gate, lab section E, PR #40 (TZ-48)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: `CryptoReports/TZ-48-own-regime-gate-report.md`, added. No hash appears for this commit,
because it had not been made when this section was written (inv. 54, contract §10).

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/40**. Base `main`, head
`claude/tz-48-own-regime-gate`, opened with `gh pr create`. Merging is the Boss's decision, taken
after the Architect's verdict.

## CI Execution

Two `Bench gate` runs executed on a GitHub runner, both on head SHA `4a11c8bf…`. Each was read
with `gh run view <id> --json status,conclusion,jobs`:

| Run | Event | Status | Conclusion |
|---|---|---|---|
| 35167655239 | `push` (branch `claude/**`) | completed | **success** |
| 35168048279 | `pull_request` | completed | **success** |

Every job step concluded `success` in both runs, workflow steps 6–19. No step was skipped.

**The runner's own counts were read** with `gh run view <id> --log`, which returned the full log
this time (87 709 and 89 088 bytes). Both runs print the same lines:

```
Офлайн-набор для --verify (verify_bench.py)   checks run: 59   FAIL 0
Гарнизон бэктеста (backtest_guard_bench.py)   E. venue-as-observation: 32 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   F. anchored production arm: 29 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   G. D4 partition: 63 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   H. transport: 107 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   I. attribution: 95 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   J. gap in UTC: 8 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   K. comparability: 11 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   checks run: 487   FAIL 0
```

Here «gate step» follows the map's numbering, which runs from 1 to 14 over the benches. Workflow
job step 9 is gate step 4, and job step 19 is gate step 14.

What did not run:

- **Gate steps 1–3 and 5–13.** Their totals were not extracted from the log. None of them imports
  `backtest_bench.py`: the only benches that do are `backtest_guard_bench.py`, `verify_bench.py`
  and `exhaustion_calib.py`, and the last is not a gate step.
- **`backtest_bench.yml`** is dispatch-only and did not run, so section E has no runner reading.
- **`main.yml`** did not run, because its allow-list names neither changed path.
- **`calib.yml`** did not run, because its `paths` name neither changed path.

## Final Repository State

- **Branch.** `claude/tz-48-own-regime-gate` is at `4a11c8b`, pushed to `origin` before this
  report was written. It carries `bench/backtest_bench.py` and nothing else against `b6dc991`.
  Pull request #40 is open.
- **Report checkout.** The report was written on the session worktree, whose tree matches
  `b6dc991` (`origin/main` at the last fetch) for every file this report fingerprints. The
  `bench/backtest_bench.py` row is also given at `4a11c8b`.
- **Cleanup.** `git status --porcelain` is empty. The ignored bench scratch written by the in-tree
  runs was removed. Scratch files live under `/tmp/tz48`, outside the repository: the pristine
  extract, the working copies, the probes and every run output quoted above.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

**System Map.** `SYSTEM-MAP-CRYPTOCALCUL.md`: **2759 lines**, MD5
`7f8fd2e8e553109cb7cffed329bd56e1`. The revision string in `## 0. Fingerprint` is
`**Revision 2026-09-16-b.**`, which is what the TZ requires.

**Anchor table.** The table was cut by structure: in each file, the first markdown table inside the
`## 0` block, every row after its separator line up to the first line not starting with `|`. No
anchor name was used to select rows (`/tmp/tz48/gate2.py`, MD5 `23650f7eff0df292a84c2de2758f6c3e`).

- map table rows: **7**;
- TZ header table rows: **7**;
- compared: **7**;
- TZ rows byte-identical to map rows: 7;
- TZ rows absent from the map table: 0;
- map rows absent from the TZ table: 0.

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

**Files in the map's `## 0` table**, measured with `wc -l` and `md5sum`. The TZ's quoted file table
is identical to the map's, row for row.

| File | Lines | MD5 | Map / TZ |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

**The file the TZ's gate adds:**

| File | Lines | MD5 | TZ |
|---|---:|---|---|
| `bench/backtest_bench.py` at `b6dc991` (before) | 5102 | `ba633202f43845ba0fdafbc1b92d9c04` | match |
| `bench/backtest_bench.py` at `4a11c8b` (after) | 5795 | `ed4db7c2bab9076e92982c664c6fc2f6` | — |

**Other files read:**

| File | Lines | MD5 |
|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` (v23; the map states 864 / `02abb1969626d2af150a0d1f6e02f2a7`, match) | 864 | `02abb1969626d2af150a0d1f6e02f2a7` |
| `ANALYST-INSTRUCTIONS.md` (`2026-09-16-c`) | 3040 | `aa1d1ccab703b322e0801511e637b331` |
| `CryptoTZ/TZ-48-own-regime-gate.md` | 263 | `9cfb148b270c9fe91f9eeeca4fffdabb` |
| `bench/backtest_guard_bench.py` (map prose: 2503 / `bfc984b1d22ec1ad89cf536a1a47c529`, match) | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` |
| `bench/verify_bench.py` (map prose: 540 / `28eb1949f21d0afadb062303108f7101`, match) | 540 | `28eb1949f21d0afadb062303108f7101` |
| `.github/workflows/backtest_bench.yml` | 171 | `703330829c377a15fc0df71e25df92a7` |
