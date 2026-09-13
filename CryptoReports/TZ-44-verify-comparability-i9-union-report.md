# Implementation Report — TZ-44

**The previous TZ left nothing to merge.** TZ-43 was BLOCKED and committed only its report
(`2660631`). TZ-44's sequencing clause says nothing of TZ-43 was merged, branched or committed,
and the tree confirms it: at session start the three files in scope read their §0 baselines,
`5008 c7fedd64…` · `388 06036d8c…` · `2438 85ea6098…`. The last merged implementation is
TZ-41's (pull request #38, merge commit `d88593e`). Since the TZ-43 report, `main` carries one
commit, `b3973ef` (this TZ's upload), which adds only
`CryptoTZ/TZ-44-verify-comparability-i9-union.md`.

## Status

**COMPLETED.**

TZ-44 §3 amends TZ-43 §9's condition, and all four parts of it hold:

- the eight edits of TZ-43 §3 are in;
- guard I9 is re-registered as the §2b pair, and I9b is green;
- the eight lanes hold;
- both benches are green offline: `verify_bench.py` exit 0, `checks run: 59   FAIL 0`, and
  `backtest_guard_bench.py` exit 0, `checks run: 487   FAIL 0`.

The hosted `Bench gate` also ran on the implementation commit, twice, and concluded `success`
both times (`## CI Execution`).

## Inbound Filing

None. `CryptoTZ/TZ-44-verify-comparability-i9-union.md` arrived on `origin/main` in `b3973ef`
under the canonical filename its header states (269 lines, `120f364142afa4ff74e41a79d885c916`).

At session start the worktree stood at `2660631`. `git fetch origin` put `origin/main` at
`b3973ef`, and the tree was brought there with `git merge --ff-only origin/main`. The repository
is not shallow (`git rev-parse --is-shallow-repository` → `false`). A second
`git fetch --all --prune`, run before writing this report, found `origin/main` still at
`b3973ef`.

## Scope Executed

**Class: branch TZ** (contract §8). TZ-44 §4 names three files outside `CryptoReports/**`:
`bench/backtest_bench.py`, `bench/verify_bench.py` and `bench/backtest_guard_bench.py`.

Steps run under contract §4a:

- **Steps 1–6 (read, fetch, locate, gate, repository state):** done in full. Both gates
  passed. The map gate is in `## Test Results`. The base-text gate (TZ-44 §0, blocking) found
  `CryptoTZ/TZ-43-verify-comparability-corrected.md` at 363 lines,
  `585b634869e69be6d5e0636b44e03165`, matching exactly.
- **Step 7 (implement):**
  - TZ-43 §3 (the eight edits and the printing), TZ-43 §5 (the lanes and guard section K), and
    TZ-44 §2 (the I9 pair in place of TZ-43 §4).
  - TZ-43 §4 and its written replacement (label `--attrib compares every cell --verify
    declines`) are not implemented. TZ-44 §2 retires both.
- **Step 8 (validate):** TZ-43 §6 items 1–8 with TZ-44 §5's amendments, plus new item 9.
- **Step 9:** implementation commit `99e4b0a` on branch
  `claude/tz-44-verify-comparability-i9-union`, pushed. Pull request #39 opened.
- **Step 10:** this report.

## Files Created

- `CryptoReports/TZ-44-verify-comparability-i9-union-report.md` — this report (on `main`, not on
  the branch).

## Files Modified

On the branch, in `99e4b0a`. Figures are measured from the committed blobs
(`git show 99e4b0a:<path> | wc -l`, `| md5sum`):

| File | Before | After | `git diff -U0` |
|---|---|---|---|
| `bench/backtest_bench.py` | 5008 `c7fedd64…` | 5102 `ba633202f43845ba0fdafbc1b92d9c04` | 18 hunks, `+118 −24` |
| `bench/verify_bench.py` | 388 `06036d8c…` | 540 `28eb1949f21d0afadb062303108f7101` | 1 hunk, `+152 −0` |
| `bench/backtest_guard_bench.py` | 2438 `85ea6098…` | 2503 `bfc984b1d22ec1ad89cf536a1a47c529` | 3 hunks, `+71 −6` |

## Files Renamed

None.

## Files Deleted

None from the repository. `bench/_tokens.js` and `bench/__pycache__/` were deleted from the
working tree. My own bench runs created both, both are ignored (`.gitignore` `bench/_*`), and
neither is tracked.

## Implementation Summary

### Where the code came from

TZ-43's report describes a prototype of its whole specification. It was measured and discarded,
and saved as `/tmp/tz43_prototype.diff`: 512 lines, MD5 `2d457dfebfebd0d6ba37097f299b0ecd`. The
file was still in this session's container, and its MD5 matched the report. The steps:

1. `git apply --check` succeeded on the pristine tree, and the diff was applied.
2. The prototype's I9 (the retired TZ-43 §4 relation) was replaced by the TZ-44 §2b pair, and
   the comment above it was rewritten.
3. Nothing else of the prototype was edited.

Every measurement below was taken fresh in this session, on this tree. None is carried over
from TZ-43's report.

### `bench/backtest_bench.py` — TZ-43 §3, edit by edit

| § 3 | Where | What is in the file |
|---|---|---|
| 1 | beside `CLASSES` | `RET_FIELDS = ("r7", "r14", "r30", "eff14")` at module scope; the local copy in `reconcile()` removed |
| 2 | beside `RET_FIELDS` | `CMP_GAP_H = 3.0` |
| 3 | after `_cell_class` | `_cell_comparable(field, gap_sym)` returns: `(True, None)` for a non-return field · `(False, "разрыв во времени неизвестен")` for `None` · `(False, "разрыв во времени %+.1f ч")` when `abs(gap_sym) > CMP_GAP_H` · `(True, None)` otherwise |
| 4 | `reconcile()` symbol loop | `gap_sym = _gap_hours(gen, [t_last])`. The cache-wide `gap` is kept and printed. Each row carries `"gap": gap_sym` |
| 5 | cell loop | `present[k] += 1`, then the comparability check. An incomparable cell goes to `nocmp`, keeps `dv`, and gets `cmp: False` and `over: None`. It touches no `seen`, no `worst`, no threshold and no `_cell_class`. `reconcile()` returns `nocmp` and `present`, and drops `skip` |
| 6 | `never` | `[k … if kind != "info" and present[k] == 0]` |
| 7 | symbol class | `UNVERIFIED = "unverified"`, in neither `CLASSES` nor `HARD_CLASSES`. Precedence: hard class · `unverified` · `venue-basis` · `clean`. `--target` prints `СВЕРКА НЕПОЛНАЯ (окно не совпадает), но в рукава допущено: …`; `--regime-gate` prints `… но в сетку допущено: …` |
| 8 | `attrib_run` return | `"nocmp": R["nocmp"]` where `"skip": R["skip"]` stood. Nothing else in `attrib_run` or `report_attrib` changed |

The printing follows TZ-43 §3's list. L1's block is quoted under item 4 below. After the commit,
`git grep` finds no reader of the retired `skip` key in `bench/`. The three hits it does return,
`direction_bench.py:641/649/671`, belong to that bench's own counter dict and are unrelated.

### `bench/verify_bench.py` — the lanes

Block `# 11. Comparability per SYMBOL and before the class` adds 19 checks for L1, L2, L3a, L3b,
L3 (the pair), L4, L6, L7, L7b and L8. It is purely additive: one hunk, `+152 −0`, and zero
`-` lines under `git diff -U0`.

### `bench/backtest_guard_bench.py` — section K

**K, read from the file:**

```
$ git show b3973ef:bench/backtest_guard_bench.py | grep -n -E "^# [A-Z]\. "
76:# A. …   179:# B. …   501:# C. …   583:# D. …   652:# E. The `--regime-gate` arm …
894:# E. The venue actually fetched is an OBSERVATION …   1041:# F. …   1210:# G. …
1495:# H. …   1972:# I. …   2361:# J. `_gap_hours` reads the stamp in UTC  (ТЗ-41)
```

The last letter is J, so the next is **K**. Counting headers would give L, because E appears
twice. On `99e4b0a` the same command returns `2436:# K. \`_cell_comparable\` — comparability
per symbol, b…`. Section K holds 11 comparisons: 10 known-answer checks on `_cell_comparable`
(TZ-43 §5's list) and the section's zero guard.

### Guard I9 — the pair, quoted as committed (`99e4b0a`, lines 2325–2346)

```
# Production built a day AFTER the archive's newest bar: each coin's OWN gap is
# beyond --verify's window, so the reconciliation declines those return cells
# and names each one in `nocmp` (ТЗ-43 §3). --attrib writes two structures —
# the pp fields per cell in `cells`, eff14 in its own `effs` — and between them
# it must measure every cell --verify declines (ТЗ-44 §2). It must also carry g,
# move the start instant, and NAME the end term — the archive holds no bar at
# production's end instant — rather than skip or read it as 0.
_XG = dict((s, i_series(I_N, seed)) for s, seed in (('GPA', 89), ('GPB', 97)))
_cG = i_cache(_XG)
_lG = i_live([i_rec(s, _XG[s]) for s in sorted(_XG)], I_TA + I_SHIFT * HOUR)
AG, _t, _m = i_run(_cG, _lG)
_EFF = 'eff14'
_AG_pp = set((c['sym'], c['field']) for c in AG['cells'] if c['d'] is not None)
_AG_eff = set((e['sym'], _EFF) for e in AG['effs'] if e['d'] is not None)
_AG_nc = set((s, f) for s, f, _, _ in AG['nocmp'])
ok('I9. g beyond --verify\'s window: --attrib measures every cell --verify declines',
   len(AG['nocmp']) > 0 and (_AG_pp | _AG_eff) >= _AG_nc,
   (len(AG['nocmp']), sorted(_AG_nc - (_AG_pp | _AG_eff))))
_AG_ppf = set(c['field'] for c in AG['cells'])
ok('I9b. --attrib splits the return family in two: the per-cell fields, and eff14 in its own structure',
   len(AG['cells']) > 0 and len(AG['effs']) > 0 and _AG_ppf == set(bb.RET_FIELDS) - set([_EFF]),
   (sorted(_AG_ppf), len(AG['cells']), len(AG['effs'])))
```

The code lines are TZ-44 §2b character for character. The comment names the two structures, as
§2b's last bullet requires. The retired check (pristine lines 2333–2334,
`--verify skips the return fields`) is gone.
`git show 99e4b0a:bench/backtest_guard_bench.py | grep -n -F "skips the return fields"` prints
nothing. On `b3973ef` the same command prints lines 2326 (the old comment) and 2333 (the old
label).

**The four checks that follow the pair, unchanged and green:**

| Pristine line | Committed line | Label |
|---:|---:|---|
| 2335 | 2347 | `I9. g beyond --verify's window: every cell is still compared, g carried` |
| 2339 | 2351 | `I9. g beyond --verify's window: the start term is measured on every cell` |
| 2341 | 2353 | `I9. g beyond --verify's window: the end term is named, never read as zero` |
| 2345 | 2357 | `I9. g beyond --verify's window: a measurement, so --attrib exits 0` |

"Green" here means the guard's `FAIL 0`: a failed `ok()` prints its label, and none was printed.

## Validation

Every item was run: TZ-43 §6's eight, amended by TZ-44 §5, plus TZ-44's item 9. Benches ran
one at a time, never concurrently.

| # | Item | Result |
|---|---|---|
| 1 | `python3 -m py_compile bench/backtest_bench.py bench/verify_bench.py bench/backtest_guard_bench.py bench/exhaustion_calib.py` | exit 0. `exhaustion_calib.py` compiled; not run, not edited |
| 2 | `python3 bench/verify_bench.py` | exit 0, `checks run: 59   FAIL 0` = 40 measured before + 19 added. `git diff -U0` on the file: 1 hunk, `+152 −0`, 0 removed lines, so no pre-existing assertion was edited or removed |
| 3 | `python3 bench/backtest_guard_bench.py` | exit 0, `checks run: 487   FAIL 0`. Arithmetic below |
| 4 | the eight lanes | all hold — table below |
| 5 | pre-repair reading | re-measured on the pristine files — table below |
| 6 | extremes | all five reached — table below |
| 7 | importers of `backtest_bench` | closed at three — below |
| 8 | `git diff --name-only`, hashes | exactly the three bench files; no production file. Hashes are under `## Files Modified` and `## Fingerprints` |
| 9 | the structures, as read | quoted below, with the command |

### Item 3 — the arithmetic, term by term

| Section | Before (pristine, measured) | After (`99e4b0a`, measured) |
|---|---:|---:|
| A–D and the first E (print no count) | 142 | 142 |
| E. venue-as-observation | 32 | 32 |
| F. anchored production arm | 29 | 29 |
| G. D4 partition | 63 | 63 |
| H. transport | 107 | 107 |
| **I. attribution** | **94** | **95** |
| J. gap in UTC | 8 | 8 |
| **K. comparability** | — | **11** |
| **`checks run`** | **475** | **487** |

The unprinted term is the total minus the printed sections: 475 − 333 = 142 and
487 − 345 = 142. It does not move. **475 + 1 + 11 = 487**, as TZ-44 §5 expects:
- I9 is replaced one for one, and I9b adds one, so I goes 94 → 95;
- K adds 11.

No figure differs from the TZ's arithmetic.

### Item 3 — the union is load-bearing

This was measured in I9's own world on the implementation. The guard was executed up to the line
before the pair (line 2335) and both relations were printed:

```
$ python3 /tmp/tz44_keys.py bench/backtest_guard_bench.py 2335
nocmp          : 8 [('GPA', 'eff14'), ('GPA', 'r14'), ('GPA', 'r30'), ('GPA', 'r7'), ('GPB', 'eff14'), ('GPB', 'r14'), ('GPB', 'r30'), ('GPB', 'r7')]
_AG_pp >= _AG_nc            : False · missing [('GPA', 'eff14'), ('GPB', 'eff14')]
(_AG_pp | _AG_eff) >= _AG_nc: True · missing []
fails so far   : []
```

| Relation | Required | Measured |
|---|---|---|
| `_AG_pp >= _AG_nc` (per-cell set alone — TZ-43 §4's relation) | **False** | **False** |
| `(_AG_pp \| _AG_eff) >= _AG_nc` (the union — TZ-44's I9) | **True** | **True** |

Without the union the check would be red, so its green is evidence of the repair.

### Item 4 — the eight lanes, on the implementation

```
$ python3 /tmp/lanes_proto.py bench/verify_bench.py
bench: ['checks run: 59   FAIL 0']
```

The runner executes the whole of `verify_bench.py` and then prints each lane's tuple.
- Class sets come from `reconcile()`, the exit code from `verify_against_live()`, and the
  exclusions from `target_gate()`, all on the same stubbed input.
- "Classes" lists the non-empty classes only; every lane has `coverage` empty.

| Lane | Exit | Classes | Symbol classes | Excluded from `--target` | `nocmp` | `seen['r7']` |
|---|---:|---|---|---|---:|---:|
| L1 (+30 h, `r7` over the bar on every coin) | 0 | ∅ | AAA, BBB, CCC `unverified` | none | 12 | 0 |
| L2 (−30 h, the same) | 0 | ∅ | AAA, BBB, CCC `unverified` | none | 12 | 0 |
| L3a (0.5 h cache-wide; AAA 20 h short, on the perpetual; AAA `r7` +5 pp) | 0 | ∅ | AAA `unverified` · BBB, CCC `clean` | none | 4 | 2 |
| L3b (the same world; AAA `min_price` over the bar) | 0 | `venue-basis` {(AAA, `min_price`)} | AAA `unverified` · BBB, CCC `clean` | none | 4 | 2 |
| L4 (L3a with AAA on spot) | 0 | ∅ | AAA `unverified` · BBB, CCC `clean` | none | 4 | 2 |
| L6 +3.0 h | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three | 0 | 3 |
| L6 −3.0 h | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three | 0 | 3 |
| L6 +3.1 h | 0 | ∅ | all `unverified` | none | 12 | 0 |
| L7 (`generated_at` = `not a stamp`) | 0 | ∅ | all `unverified` | none | 12 | 0 |
| L7b (L7 plus AAA `min_price` over the bar) | 1 | `unexplained` {(AAA, `min_price`)} | AAA `unexplained` · BBB, CCC `unverified` | AAA | 12 | 0 |
| L8 (L1's world) | 0 | as L1 | as L1 | none | 12 | 0 |

**Stated as equalities:**

- **L2 = L1.** Both read (exit 0, every class ∅, {AAA, BBB, CCC: `unverified`}, excluded ∅).
  The sign decides nothing.
- **The L3 pair.** `venue-basis` (class set, basis-note set) is `(∅, ∅)` in (a) and
  `({(AAA, min_price)}, {(AAA, min_price)})` in (b). Both exit 0. The licence keeps the level
  and loses the return.
- **L4 = L3a.** Both read (exit 0, every class ∅, {AAA: `unverified`, BBB: `clean`,
  CCC: `clean`}, excluded ∅). Comparability reads no venue.
- **L6.** `seen['r7']` = `[3, 3, 0]` and `(AAA, r7) ∈ nocmp` = `[False, False, True]`, so the
  three gaps read compared, compared, not compared.
- **L7.** All 12 of 12 return cells are not compared, each with `разрыв во времени неизвестен`
  and `gap_sym = None`. The line `РАЗРЫВ ВО ВРЕМЕНИ НЕИЗВЕСТЕН у 3 монет из 3` is printed and
  «БОЛЬШЕ ТРЁХ ЧАСОВ» is absent. Every level field reads `сверок  3 из  3`.
- **L8.** The agreement line names `min_price, max_price, min30, max30, volatility, vol7` and
  no return field. Each of `r7`, `r14`, `r30`, `eff14` reads `сверок  0 из  3`.

L1's printed block (the level rows and `vol_ratio` are omitted):

```
разрыв по монетам: от +30.0 до +30.0 ч
РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ у 3 монет из 3: доходности r7/r14/r30/eff14 считаются на разные моменты и НЕ СРАВНИМЫ. …
  r7          сверок  0 из  3   окно  7д   худшее    +0.000 пп   порог 1.50 пп   не сравнимо у 3 монет
  eff14       сверок  0 из  3   окно 90д   худшее    +0.000   порог 0.15   не сравнимо у 3 монет
  ожидаемый сдвиг цены за разрыв: ~5.5% при часовой воле 1%
СВЕРКА ПО МОНЕТАМ: AAA unverified · BBB unverified · CCC unverified
совпадает с продакшном по сверенным полям: min_price, max_price, min30, max30, volatility, vol7
НЕ СВЕРЯЛОСЬ (окно не совпадает): r7, r14, r30, eff14 — ячеек 12 на 3 монетах
  AAA     разрыв во времени +30.0 ч: r7, r14, r30, eff14
```

L2 prints `разрыв по монетам: от -30.0 до -30.0 ч` and the same announcement. L7 opens
`разрыв по монетам: не измерен · разрыв неизвестен у 3 монет` and prints no expected-shift line.
The 20 h shortening is built as `coins['AAA'][:-20]` through `make_cache`, so production's
`census_of_doc` writes the census and `tail` stays 0.

### Item 5 — the pre-repair reading, on the pristine files

The pristine files were extracted with `git archive b3973ef bench index.html main.py` into
`/tmp/tz44_pristine`. Then:

```
$ python3 /tmp/lanes_pre.py /tmp/tz44_pristine/bench/verify_bench.py /tmp/tz44_pristine/bench/backtest_bench.py
backtest_bench under test: /tmp/tz44_pristine/bench/backtest_bench.py · has RET_FIELDS at module scope: False
```

| World | Exit | Classes | Symbol classes | Excluded | Announcement |
|---|---:|---|---|---|---|
| **L1** | **1** | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | **all three leave the arms** | `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ: …` and `НЕ СВЕРЯЛОСЬ (разрыв во времени 30.0 ч)` in the same output |
| L2 | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three | **none** — −30 h is not `> 3` |
| L3a | 0 | `venue-basis` {(AAA, `eff14`), (AAA, `r7`)} | AAA `venue-basis` | none | none — a 20 h tail forgiven as basis |
| L3b | 0 | `venue-basis` {(AAA, `eff14`), (AAA, `min_price`)} | AAA `venue-basis` | none | none |
| L4 | 1 | `unexplained` {(AAA, `eff14`), (AAA, `r7`)} | AAA `unexplained` | AAA | none |
| L6 ±3.0 h | 1 · 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three | none |
| L6 +3.1 h | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three | announced as not compared, and classed anyway |
| L7 | 0 | ∅ | all `clean` | none | `НЕ СВЕРЯЛОСЬ (разрыв во времени неизвестен)` while every symbol reads `clean` |
| L7b | 1 | `unexplained` {(AAA, `min_price`)} | AAA `unexplained` · BBB, CCC `clean` | AAA | as L7 |

**L1 before the repair:** exit 1, the three `r7` cells classed `unexplained`, all three symbols
leave the arms. After: exit 0, no class, no exclusion, every symbol `unverified`.

### Item 6 — extremes, on the implementation

```
$ python3 /tmp/lanes_pre.py bench/verify_bench.py bench/backtest_bench.py extremes
```

| Extreme | Result |
|---|---|
| empty cache | exit 1. `$ python3 /tmp/tz44_empty.py` shows `SystemExit` carrying `СТОП: сверять нечего — в кэше ноль монет. Это провал закачки, а не успешная сверка.` — the existing `cmp_n == 0` path |
| `_quality_today.json` side file | exit 0, `сверено монет: 3` present |
| `min30` dropped from every coin | exit 1, `НЕ СВЕРЕНО НИ РАЗУ: min30 — поля нет в живом coeffs.json …` (via `never`) |
| coin DDD cached and absent from `coeffs.json` | exit 0; DDD absent from «СВЕРКА ПО МОНЕТАМ» |
| **single-bar DDD in the cache AND a DDD row in `coeffs.json`** | **reached:** DDD row present = `True`, `no_build == ['DDD']`, `cmp_n == 3`, DDD absent from `sym_class`, **exit 0 — equal to the same world without DDD (exit 0)** |

### Item 7 — the importers

```
$ git grep -l -E "backtest_bench" -- '*.py' '*.js' '*.sh' '*.yml'
.github/workflows/backtest_bench.yml  .github/workflows/bench.yml  .github/workflows/calib.yml
bench/backtest_bench.py  bench/backtest_guard_bench.py  bench/exhaustion_calib.py  bench/verify_bench.py
$ git grep -n -E "^\s*import backtest_bench|from backtest_bench|spec_from_file_location\('bb'" -- '*.py'
bench/backtest_guard_bench.py:42   bench/exhaustion_calib.py:73   bench/verify_bench.py:21
```

The set is closed at three. In `bench.yml`, `run: python3 bench/verify_bench.py` is the 6th
`run:` line (gate step 4) and `run: python3 bench/backtest_guard_bench.py` is the 16th (gate
step 14). No `run:` line names `exhaustion_calib.py`, which stays outside the gate by decision.
`clean_bench.py` and `direction_bench.py` do not import it and were not run locally for this TZ.

### Item 8 — the diff

```
$ git diff --name-only b3973ef 99e4b0a
bench/backtest_bench.py
bench/backtest_guard_bench.py
bench/verify_bench.py
```

No production file appears in it, and no workflow file. After the change, the four `## 0`
hashes are unchanged, and the three §0 baselines moved only as `## Files Modified` states.

### Item 9 — the structures, as read (TZ-44 §2a)

Printed on the pristine guard **before any edit**, in I9's own world (the guard executed up to
pristine line 2332, the line that builds `AG`):

```
$ python3 /tmp/tz44_keys.py /tmp/tz44_pristine/bench/backtest_guard_bench.py 2332   # pristine, HEAD b3973ef
AG keys        : ['cached_not_prod', 'cells', 'coins', 'eff_in', 'effs', 'fields', 'gap', 'gen', 'kinds', 'n_attr', 'n_cmp', 'no_build', 'prod_not_cached', 'reasons', 'skip', 'two']
cells[0] keys  : ['d', 'dstart', 'end', 'field', 'g', 'interior', 'ladder', 'pop', 'resid', 'start', 'sym', 'tp', 'why']
effs[0] keys   : ['d', 'inputs', 'parts', 'pop', 'rep', 'sym', 'why']
len cells/effs : 6 2
cell fields    : ['r14', 'r30', 'r7'] · AG fields ['r7', 'r14', 'r30']
effs (sym, d)  : [('GPA', 0.0), ('GPB', 0.0)]
RET_FIELDS     : <not at module scope>
skip           : ('r7', 'r14', 'r30', 'eff14')
fails so far   : []
```

Every `effs` entry carries `sym` and `d`, so §2a's stop condition is not met and no key was
substituted. The code reads `c['sym']`, `c['field']`, `c['d']`, `e['sym']` and `e['d']`, and all
five are present. Re-read on the implementation (line 2335, the same world): the `cells` and
`effs` key sets are identical, and `AG` carries `nocmp` where it carried `skip`.

## Test Results

**Fingerprint gate (contract §5) — PASSED**, against `origin/main` at `b3973ef`.

| Anchor | Matched substring (`grep -cF`) | Count |
|---|---|---:|
| revision | `**Revision 2026-09-13-b.**` | 2 |
| direction engine | `### 3.12 Direction engine — veto cascade` | 2 |
| catalyst registry | `### 3.15 Catalyst registry` | 2 |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | 2 |
| analytical engine | `## 11. Analytical engine` | 2 |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 |
| newest invariant | `71. **A measurement that is not RETAINED was not taken,` | 2 |

- **Anchors:** 7 compared, 7 present.
- **Revision:** the map reads `**Revision 2026-09-13-b.**` at line 17.
- **Map `## 0` file table:** 4 of 4 files exact.
- **Base-text gate (blocking):** exact, `CryptoTZ/TZ-43-verify-comparability-corrected.md` at
  363 lines, `585b6348…`.
- **§0 baselines:** 3 of 3 exact.
- **Contract:** v20, 814 lines, `9a257890…`. **Map:** 2691 lines, `7c8b58ec…`. Both match
  the TZ.

**Bench baselines, unmodified tree:**

| Bench | Exit | Result |
|---|---:|---|
| `python3 bench/verify_bench.py` (step 4) | 0 | `checks run: 40   FAIL 0` |
| `python3 bench/backtest_guard_bench.py` (step 14) | 0 | `checks run: 475   FAIL 0` — E 32 · F 29 · G 63 · H 107 · I 94 · J 8 |

**After the change, local:**

| Bench | Exit | Result |
|---|---:|---|
| `python3 bench/verify_bench.py` | 0 | `checks run: 59   FAIL 0` |
| `python3 bench/backtest_guard_bench.py` | 0 | `checks run: 487   FAIL 0` — E 32 · F 29 · G 63 · H 107 · I 95 · J 8 · K 11 |

## Deviations

None from the specification. How the implementation was produced — TZ-43's discarded prototype,
re-applied, with only I9 rewritten — is disclosed under `## Implementation Summary`. It is a
method, not a deviation. The prototype's hash matched TZ-43's report, and every result in this
report was measured on this session's tree.

## Pre-existing Issues

- **The defect TZ-43 §1 describes is live on `main`**, re-measured above (item 5). It stays live
  until pull request #39 is merged.
- **TZ-43 §4's "The two I9 checks below it" was a counting slip.** TZ-44 §2b corrects it, and it
  is confirmed here: four checks, at pristine lines 2335, 2339, 2341 and 2345.

No fingerprint differed.

## Remaining Risks

- **The announcement literal and `CMP_GAP_H` can drift apart.** TZ-43 §3 fixes the literal
  `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ`, while `CMP_GAP_H` is the only place the hours live. Section K
  moves the constant and restores it. A permanent move would leave the literal asserting three
  hours. The TZ specifies the literal, so it is kept.
- **I9b pins the per-cell field set to `RET_FIELDS` minus `eff14`.** A future field added to
  `RET_FIELDS` turns I9b red unless `attrib_run` also splits it per cell. This is the intended
  behaviour (TZ-44 §2b), and it is recorded so the red is recognised when it comes.
- **Check counts on the runner are unread.** The hosted runs' conclusions are read below. The
  runner's printed totals (`checks run: 59` / `487`) live in the job log, which this session's
  token was not used to fetch. The local counts are not offered as a substitute for them.

## Commit

**Implementation commit, already pushed:** `99e4b0a3b474088e5d08cb5c1268226b0ec3dea2` on branch
`claude/tz-44-verify-comparability-i9-union`. Parent `b3973ef`. It contains exactly the three
files in `## Files Modified`. Message, verbatim from TZ-44 `## Commit Message`, with the session
trailer:

```
TZ-44: decide comparability per symbol and before the class — guard I9 is re-registered as a pair, reading both structures the attribution writes and asserting the split between them

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

**This report's commit** goes to `main` on the `CryptoReports/**` direct-push path (contract §8).
The workflow filters were read before it:

- `bench.yml`'s `push` carries `'**.md'` under `paths-ignore`;
- `main.yml`'s `push` is a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`;
- `backtest_bench.yml` triggers on `workflow_dispatch` only.

Message:

```
docs(reports): TZ-44 — guard I9 re-registered as a pair over cells ∪ effs, I9b asserts the split; 487/0 and 59/0 (TZ-44)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: `CryptoReports/TZ-44-verify-comparability-i9-union-report.md`, added.

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/39** — base `main`, head
`claude/tz-44-verify-comparability-i9-union`, opened with `gh pr create`. Merging is the Boss's
decision, taken after the Architect's verdict.

## CI Execution

Two `Bench gate` runs executed on a GitHub runner, both on head SHA `99e4b0a3…`. They were read
with `gh run view <id> --json status,conclusion,jobs` after `gh run watch` returned:

| Run | Event | Status | Conclusion |
|---|---|---|---|
| 34786159289 | `push` (branch `claude/**`) | completed | **success** |
| 34786168232 | `pull_request` | completed | **success** |

Every step concluded `success` in both runs, including:
- job step 9, `Офлайн-набор для --verify (verify_bench.py)`, which is gate step 4;
- job step 19, `Гарнизон бэктеста (backtest_guard_bench.py)`, which is gate step 14.

No step was skipped. `backtest_bench.yml` is `workflow_dispatch`-only and did not run. `main.yml`
did not run, because its allow-list names neither changed path. The per-step check counts on
the runner are unread (`## Remaining Risks`).

## Final Repository State

- **Branch.** `claude/tz-44-verify-comparability-i9-union` is at `99e4b0a`, pushed to `origin`
  before this report was written. It carries the three modified bench files and nothing else.
  Pull request #39 is open.
- **Report checkout.** It was written on the session worktree, whose tree matches `b3973ef`
  (`origin/main` at the second fetch). That is the commit the fingerprints below were taken
  against, with the three bench rows also given at `99e4b0a`.
- **Cleanup.** The ignored bench artifacts were removed. Scratch files (the pristine extract, the
  probe and lane runners, bench outputs) live under `/tmp`, outside the repository.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Taken at `b3973ef` (the bench rows also at `99e4b0a`). **System Map revision string:**
`**Revision 2026-09-13-b.**`

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2691 | `7c8b58ec4dea7142104fc9dc0173edcc` |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` |
| `ANALYST-INSTRUCTIONS.md` | 2615 | `e945ac9e93c03e72f551bc7972541148` |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/backtest_bench.py` @ `b3973ef` | 5008 | `c7fedd64bce7c27c07803325b1f807d3` |
| `bench/backtest_bench.py` @ `99e4b0a` | 5102 | `ba633202f43845ba0fdafbc1b92d9c04` |
| `bench/verify_bench.py` @ `b3973ef` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
| `bench/verify_bench.py` @ `99e4b0a` | 540 | `28eb1949f21d0afadb062303108f7101` |
| `bench/backtest_guard_bench.py` @ `b3973ef` | 2438 | `85ea609882ac3761fd526b3ebff2fe5f` |
| `bench/backtest_guard_bench.py` @ `99e4b0a` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` |
| `bench/exhaustion_calib.py` | 1031 | `3ac6a4903528cb271cd4f8520b140f27` |
| `.github/workflows/bench.yml` | 153 | `d182e514dcceda5c64410beabc9fe512` |
| `.github/workflows/backtest_bench.yml` | 171 | `703330829c377a15fc0df71e25df92a7` |
| `CryptoTZ/TZ-43-verify-comparability-corrected.md` | 363 | `585b634869e69be6d5e0636b44e03165` |
| `CryptoTZ/TZ-44-verify-comparability-i9-union.md` | 269 | `120f364142afa4ff74e41a79d885c916` |

The table covers:

- the map's `## 0` set;
- the two contracts;
- the three §0 baselines, before and after, plus `exhaustion_calib.py`;
- the two workflows, whose filters this report's evidence reads;
- the base text TZ-44 gates, and TZ-44 itself (TZ-44 §8).
