# Implementation Report — TZ-43

**The previous TZ is merged.** TZ-43's sequencing clause names TZ-41: pull request #38, merge
commit `d88593e`, implementation commit `dc42e4e`. `git log --oneline --graph --all` shows
`d88593e` on `main` with parents `bd2f197` and `dc42e4e`. Since then `main` carries `4f07a98`,
`f51dea1` (map uploads), `bb0cdac` (TZ-42 upload), `bb74ed4` (TZ-42 report), `e0fd374` (this
TZ's upload) and `6bddc0c` (`journal: 2026-09-13 [skip ci]`, four `journal/**` files). None
of them touches a file in this TZ's scope. TZ-42 is retired by this TZ's header, and nothing
of it is executed here.

## Status

**BLOCKED.**

The fingerprint gate passed. All eight §3 edits, the printing block, section K and the eight
lanes were built and measured on a prototype, and every one of them holds. **One thing does
not hold: the I9 replacement exactly as §4 writes it.** §4 decides that case in its own words:

> **If the replacement cannot be made to hold, that is a finding and a BLOCKED verdict — never
> a weaker assertion.**

**Why it cannot hold.** §4 asserts

```
{(c["sym"], c["field"]) for c in AG["cells"] if c["d"] is not None}  ⊇  {(s, f) for s, f, _, _ in AG["nocmp"]}
```

The two sides are built from two different field sets:

- **`AG["cells"]` holds only the `pp` fields.** `attrib_run` builds its cells from
  `fields = [k for k, kind, _ in R["spec"] if kind == "pp"]`, which is `r7`, `r14` and `r30`.
  `eff14` is attributed separately, in `AG["effs"]`, and its Δ lives there.
- **`AG["nocmp"]` covers `RET_FIELDS`.** Under §3 edits 1, 3 and 5 that is `r7`, `r14`, `r30`
  **and `eff14`**. In I9's world, where production is built 24 h after the archive, each coin
  therefore contributes four cells.

The left side can never contain `(GPA, eff14)` or `(GPB, eff14)`, so the superset fails in the
very world the assertion was written for.

**Measured, before any edit.** I executed the pristine guard up to line 2332 and printed both
sides of I9's world:

```
A fields      : ['r7', 'r14', 'r30'] · I_F ['r7', 'r14', 'r30']
cells, d formed: [('GPA','r14'), ('GPA','r30'), ('GPA','r7'), ('GPB','r14'), ('GPB','r30'), ('GPB','r7')]
effs, d formed : [('GPA','eff14', 0.0), ('GPB','eff14', 0.0)]
```

**Measured on the prototype** (all eight edits, with I9 replaced exactly as written):

```
$ python3 bench/backtest_guard_bench.py          → exit 1
checks run: 486   FAIL 1
  FAIL: I9. g beyond --verify's window: --attrib compares every cell --verify declines  [(8, [('GPA', 'eff14'), ('GPB', 'eff14')])]
```

`nocmp` holds 8 cells, so the non-empty clause holds, and the superset misses exactly the two
`eff14` cells. It is the only red among the 486 checks.

**What unblocks it:** a corrected specification from the Architect (contract §12) that
restates the I9 relation over two sets that can meet. Both repairs below make the guard green
on the prototype. **Each is weaker than the text as written, and that is why neither was
chosen here:**

| Variant | Change to the replacement | Guard on the prototype |
|---|---|---|
| **A** | the left side also counts `--attrib`'s `eff14` Δ: `… ∪ {(e["sym"], "eff14") for e in AG["effs"] if e["d"] is not None}` | exit 0, `checks run: 486   FAIL 0` |
| **B** | the right side is restricted to the fields `--attrib` splits: `{(s, f) for s, f, _, _ in AG["nocmp"] if f in AG["fields"]}` | exit 0, `checks run: 486   FAIL 0` |

- **A is closer to §4's prose** ("the attribution measures exactly the cells the
  reconciliation declines"): `--attrib` does form a Δ for `eff14`, in `effs`.
- **B asserts less:** the `eff14` cells `--verify` declines go unasserted.

Both were measuring tools on `/tmp` copies of the guard, run against the prototype, and are not
proposals. Once one is specified, `EXECUTE TZ-44` (or whatever number the Architect assigns)
has nothing else left to find, as far as this prototype can show. The rest of this report is
that evidence.

## Inbound Filing

None. `CryptoTZ/TZ-43-verify-comparability-corrected.md` arrived on `origin/main` in `e0fd374`
under the canonical filename its header states (363 lines,
`585b634869e69be6d5e0636b44e03165`).

At session start the worktree stood at `bb74ed4`. `git fetch --all --prune` put `origin/main`
at `e0fd374`, and the tree was brought there by `git merge --ff-only origin/main`. The
repository is not shallow (`git rev-parse --is-shallow-repository` → `false`). A second
`git fetch --all --prune` before writing this report found `origin/main` at `6bddc0c`. That
commit touches only `journal/data/2026-09-13.jsonl`, `journal/out/2026-08-29-h14.jsonl`,
`journal/out/2026-09-06-h7.jsonl` and `journal/runs.jsonl`, and the tree was fast-forwarded to
it the same way.

## Scope Executed

**Class: branch TZ** (contract §8). `## 2. Scope` names three files outside
`CryptoReports/**`: `bench/backtest_bench.py`, `bench/verify_bench.py` and
`bench/backtest_guard_bench.py`.

Steps run under contract §4a:

- **Steps 1–6 (read, fetch, locate, gate, repository state):** done in full.
- **Step 7 (implement):** entered as a measurement and disclosed under `## Deviations`. The
  whole TZ was written into the working tree, measured, saved outside the repository
  (`/tmp/tz43_prototype.diff`, 512 lines, MD5 `2d457dfebfebd0d6ba37097f299b0ecd`), and
  discarded with `git checkout --`.
- **Step 8 (validate):** every §6 item was run against the prototype (`## Validation`).
- **Step 9 (branch and pull request):** not reached.
- **Step 10:** this report.

## Files Created

- `CryptoReports/TZ-43-verify-comparability-corrected-report.md` — this report.

## Files Modified

None. After the discard all three files in scope read their §0 baselines: 5008
`c7fedd64…` · 388 `06036d8c…` · 2438 `85ea6098…`.

## Files Renamed

None.

## Files Deleted

None from the repository. `bench/_tokens.js` and `bench/__pycache__/` were deleted from the
working tree. My own bench runs created both, both are ignored (`.gitignore` `bench/_*`), and
neither was ever tracked.

## Implementation Summary

No implementation is delivered. What follows describes the prototype, which is what a
corrected specification would ship with a different I9 relation.

### The prototype, edit by edit

`git diff --stat`: 3 files, `+334 −30`. Under `git diff -U0` that is 18 hunks in
`backtest_bench.py`, 1 in `verify_bench.py` (additions only) and 3 in
`backtest_guard_bench.py`.

| § 3 | Where | What was written |
|---|---|---|
| 1 | beside `CLASSES` | `RET_FIELDS = ("r7", "r14", "r30", "eff14")` at module scope; the local copy in `reconcile()` removed |
| 2 | beside `RET_FIELDS` | `CMP_GAP_H = 3.0` |
| 3 | after `_cell_class` | `_cell_comparable(field, gap_sym)` → `(True, None)` for a non-return field · `(False, "разрыв во времени неизвестен")` for `None` · `(False, "разрыв во времени %+.1f ч")` when `abs(gap_sym) > CMP_GAP_H` · else `(True, None)` |
| 4 | `reconcile()` symbol loop | `gap_sym = _gap_hours(gen, [t_last])`; the cache-wide `gap` is kept and printed. Each row also carries `"gap": gap_sym`, which the dispersion line reads |
| 5 | cell loop | `present[k] += 1`, then comparability. An incomparable cell goes to `nocmp`, keeps `dv`, gets `cmp: False` and `over: None`, and touches no `seen`, no `worst`, no threshold and no `_cell_class`. `reconcile()` returns `nocmp` and `present` and drops `skip` |
| 6 | `never` | `[k … if kind != "info" and present[k] == 0]` |
| 7 | symbol class | `UNVERIFIED = "unverified"`, in neither `CLASSES` nor `HARD_CLASSES`. Precedence: hard class · `unverified` · `venue-basis` · `clean`. `--target` prints `СВЕРКА НЕПОЛНАЯ (окно не совпадает), но в рукава допущено: …`; `--regime-gate` prints `… но в сетку допущено: …`, each directly under that mode's «НЕ СВЕРЕНО …» line |
| 8 | `attrib_run` return | `"nocmp": R["nocmp"]` where `"skip": R["skip"]` stood. Nothing else in `attrib_run` or `report_attrib` changed |

The printing followed §3's list: the dispersion line, the two announcement literals, `сверок
N из M` with `не сравнимо у N монет`, the expected-shift line on the worst `abs(gap_sym)`, the
`НЕ СВЕРЯЛОСЬ (окно не совпадает)` block, and an agreement line that names only fields with
`seen > 0`. `grep` after the edits found no remaining reader of `skip` in the three files.

L1's printed block on the prototype (the level rows are omitted here):

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

L7 opens `разрыв по монетам: не измерен · разрыв неизвестен у 3 монет` and `РАЗРЫВ ВО ВРЕМЕНИ
НЕИЗВЕСТЕН у 3 монет из 3`, and prints no expected-shift line.

### Guard section K — the letter, read from the file

The section headers in the pristine guard are `# A.` (line 76), `# B.` (179), `# C.` (501),
`# D.` (583), `# E.` (652), `# E.` (894), `# F.` (1041), `# G.` (1210), `# H.` (1495),
`# I.` (1972) and `# J.` (2361). The last letter is J, so the next is **K**. Counting headers
would say L, because E is carried twice. This agrees with §1a.

Section K on the prototype asserted **11** comparisons:

- the return family is the four fields in one module constant;
- a level is comparable at every gap in `(None, 0, ±3.0, ±3.1, ±30, ±1e6)`;
- `None` is not comparable and says so;
- 3.0 is comparable on both signs;
- 3.1 is not comparable on both signs;
- the boolean at `+g` equals the boolean at `−g`;
- the reason carries the sign (`+30.0` / `-30.0`);
- all four return fields behave identically;
- with `bb.CMP_GAP_H = 10.0` the 5 h decision moves from `False` to `True`;
- restored, the constant reads 3.0 and the decision reads `False` again;
- the section's zero guard.

### The I9 replacement as it was written in the prototype

```
_AG_cmp = set((c['sym'], c['field']) for c in AG['cells'] if c['d'] is not None)
_AG_nc = set((s, f) for s, f, _, _ in AG['nocmp'])
ok('I9. g beyond --verify\'s window: --attrib compares every cell --verify declines',
   len(AG['nocmp']) > 0 and _AG_cmp >= _AG_nc,
   (len(AG['nocmp']), sorted(_AG_nc - _AG_cmp)))
```

The comment above it (lines 2325–2328) was rewritten to name the per-cell set. It is quoted
here as prototyped, not as committed: nothing was committed.

## Validation

Every §6 item was run. Because nothing is delivered, each result below describes the discarded
prototype, except where a row says "pristine".

| # | Item | Result |
|---|---|---|
| 1 | `py_compile` on the four files | exit 0 (prototype); `exhaustion_calib.py` compiled, not run, not edited |
| 2 | `verify_bench.py` | exit 0, `checks run: 59   FAIL 0` = 40 measured + 19 added; `git diff -U0` on the file: 1 hunk, `+152 −0`, so no pre-existing assertion edited or removed |
| 3 | `backtest_guard_bench.py` | **exit 1, `checks run: 486   FAIL 1`**, the I9 replacement (`## Status`). Sections E 32 · F 29 · G 63 · H 107 · I 94 · J 8 · **K 11**; A–D and the first E print no count. 475 → 486 = 475 + 11, with I9 replaced one for one. The four other I9 checks in that world (lines 2335, 2339, 2341, 2345) stayed green |
| 4 | the eight lanes | all hold — table below |
| 5 | pre-repair reading | re-measured on the pristine file — table below |
| 6 | extremes | all five reached — table below |
| 7 | importers of `backtest_bench` | closed at three — below |
| 8 | `git diff --name-only`, hashes | the prototype's diff named exactly the three bench files, and no production file. After the discard it names none. Hashes are under `## Fingerprints` |

### Item 4 — the eight lanes, on the prototype

Class sets come from `reconcile()`, the exit code from `verify_against_live()`, and the
exclusions from `target_gate()`, all on the same stubbed input.

| Lane | Exit | Classes (non-empty only) | Symbol classes | Excluded from `--target` |
|---|---:|---|---|---|
| L1 (+30 h, `r7` +5 pp on every coin) | 0 | ∅ | AAA, BBB, CCC `unverified` | none |
| L2 (−30 h, the same) | 0 | ∅ | AAA, BBB, CCC `unverified` | none |
| L3a (0.5 h cache-wide; AAA 20 h short, on the perpetual; AAA `r7` +5 pp) | 0 | ∅ | AAA `unverified` · BBB, CCC `clean` | none |
| L3b (the same world; AAA `min_price` ×1.06) | 0 | `venue-basis` {AAA `min_price`} | AAA `unverified` · BBB, CCC `clean` | none |
| L4 (L3a with AAA on spot) | 0 | ∅ | AAA `unverified` · BBB, CCC `clean` | none |
| L6 +3.0 h | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three |
| L6 −3.0 h | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three |
| L6 +3.1 h | 0 | ∅ | all `unverified` | none |
| L7 (`generated_at` = `not a stamp`) | 0 | ∅ | all `unverified` | none |
| L7b (L7 plus AAA `min_price` ×1.06) | 1 | `unexplained` {AAA `min_price`} | AAA `unexplained` · BBB, CCC `unverified` | AAA |
| L8 (L1's world) | 0 | as L1 | as L1 | none |

**Stated as equalities:**

- **L2 = L1.** Both are `(exit 0, every class ∅, {AAA, BBB, CCC: unverified}, excluded {})`.
- **The L3 pair.** `venue-basis` (class, note) is `(∅, ∅)` in (a) and `({(AAA, min_price)},
  {(AAA, min_price)})` in (b), with both exits 0. The licence keeps the level and loses the
  return.
- **L4 = L3a.** Both are `(exit 0, every class ∅, {AAA: unverified, BBB: clean, CCC: clean},
  excluded {})`.
- **L6:** `seen['r7']` = `[3, 3, 0]` and `(AAA, r7) ∈ nocmp` = `[False, False, True]`, so the
  three gaps read compared, compared, not compared.
- **L7:** 12 of 12 return cells were not compared, all with `разрыв во времени неизвестен` and
  `gap_sym = None`. The unknown-gap literal is present and «БОЛЬШЕ ТРЁХ ЧАСОВ» is absent. Every
  level field reads `сверок 3 из 3`.
- **L8:** the agreement line names `min_price, max_price, min30, max30, volatility, vol7`, and
  no return field. Each return field reads `сверок  0 из  3`.

The 20 h shortening was built as `coins['AAA'][:-20]` through `make_cache`, so production's
`census_of_doc` wrote the census and `tail` is 0.

### Item 5 — the pre-repair reading, re-measured on the pristine file (MD5 `c7fedd64…`)

| World | Exit | Classes | Symbol classes | Excluded | Announcement |
|---|---:|---|---|---|---|
| **L1** | **1** | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | **all three leave the arms** | `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ: …` and `НЕ СВЕРЯЛОСЬ (разрыв во времени 30.0 ч)` in the same output |
| L2 | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three | **none** — the −30 h gap is not `> 3` |
| L3a | 0 | `venue-basis` {AAA `eff14`, AAA `r7`} | AAA `venue-basis` | none | none — a 20 h tail forgiven as basis |
| L4 | 1 | `unexplained` {AAA `eff14`, AAA `r7`} | AAA `unexplained` | AAA | none |
| L6 +3.1 h | 1 | `unexplained` {AAA, BBB, CCC `r7`} | all `unexplained` | all three | announced as not compared, and classed anyway |
| L7 | 0 | ∅ | all `clean` | none | `НЕ СВЕРЯЛОСЬ (разрыв во времени неизвестен)` while every symbol reads `clean` |

§1's three bullets and the `venue-basis` mixture all reproduce on `main` as it stands.

### Item 6 — extremes, on the prototype

| Extreme | Result |
|---|---|
| empty cache | exit 1, on the existing `СТОП: сверять нечего …` path (`cmp_n == 0`) |
| `_quality_today.json` side file | exit 0, `сверено монет: 3` |
| `min30` dropped from every coin | exit 1, `НЕ СВЕРЕНО НИ РАЗУ: min30 — поля нет в живом coeffs.json …` |
| coin DDD cached and absent from `coeffs.json` | exit 0; DDD absent from «СВЕРКА ПО МОНЕТАМ» |
| **single-bar DDD in the cache AND a DDD row in `coeffs.json`** | **reached:** `no_build == ['DDD']`, `cmp_n == 3`, DDD absent from `sym_class`, **exit 0 — equal to the same world without DDD (exit 0)**. The row was built on DDD's full series, as the guard's TIN coin is |

### Item 7 — the importers

```
$ git grep -l -E "backtest_bench" -- '*.py' '*.js' '*.sh' '*.yml'
.github/workflows/backtest_bench.yml  .github/workflows/bench.yml  .github/workflows/calib.yml
bench/backtest_bench.py  bench/backtest_guard_bench.py  bench/exhaustion_calib.py  bench/verify_bench.py
$ git grep -n -E "^\s*import backtest_bench|from backtest_bench|spec_from_file_location\('bb'" -- '*.py'
bench/backtest_guard_bench.py:42   bench/exhaustion_calib.py:73   bench/verify_bench.py:21
```

The set is closed at three. `bench.yml`'s step list puts `verify_bench.py` at **step 4** and
`backtest_guard_bench.py` at **step 14**; none of its 14 `run:` lines names
`exhaustion_calib.py`. `clean_bench.py` and `direction_bench.py` were not run for this TZ.

## Test Results

**Fingerprint gate (contract §5) — PASSED**, against `origin/main` at `e0fd374` and again at
`6bddc0c`.

| Anchor | Matched substring (`grep -cF`) | Count |
|---|---|---:|
| revision | `**Revision 2026-09-13-b.**` | 2 |
| direction engine | `### 3.12 Direction engine — veto cascade` | 2 |
| catalyst registry | `### 3.15 Catalyst registry` | 2 |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | 2 |
| analytical engine | `## 11. Analytical engine` | 2 |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 |
| newest invariant | `71. **A measurement that is not RETAINED was not taken,` | 2 |

7 compared, 7 present. The map's revision string reads `Revision 2026-09-13-b`. The `## 0`
file table: 4 of 4 files exact. The TZ's §0 baselines: 3 of 3 exact. The contract measures
v20, 814 lines, `9a257890…`, and the map 2691 lines, `7c8b58ec…`. Both match the TZ.

**Bench baselines, unmodified tree:**

| Bench | Exit | Result |
|---|---:|---|
| `python3 bench/verify_bench.py` (step 4) | 0 | `checks run: 40   FAIL 0` |
| `python3 bench/backtest_guard_bench.py` (step 14) | 0 | `checks run: 475   FAIL 0` — E 32 · F 29 · G 63 · H 107 · I 94 · J 8 |

Both benches ran serially, never concurrently.

## Deviations

One, disclosed under contract §12 ("Do not partially implement around a blocker without saying
so"). The blocker was found by the pre-edit probe. All eight edits, section K and the lanes
were then written into the working tree as a prototype. The purpose was to confirm the block
by measurement and to find anything else a corrected specification would need. Nothing else was
found. The prototype was saved to `/tmp` and discarded, and no file in scope differs from
`origin/main`.

## Pre-existing Issues

- **The defect §1 describes is live on `main`**, re-measured above (item 5).
- **TZ-43 §4 says "The two I9 checks below it"; the file carries four.** Lines 2335, 2339, 2341
  and 2345 all sit in the same `AG` world. All four stayed green on the prototype, so this is a
  counting slip in the TZ, not a second blocker.

No fingerprint differed.

## Remaining Risks

- **The announcement literal and `CMP_GAP_H` can drift apart.** §3 fixes the literal
  `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ` and makes `CMP_GAP_H` the only place the hours live. Section K
  moves the constant to 10.0 and restores it. A permanent move would leave the literal
  asserting three hours. The TZ specifies the literal, so the prototype kept it.
- **The prototype's figures describe that prototype only.** A corrected I9 relation (A, B or
  another) changes one assertion. The other 485 guard checks and the 59 `verify_bench` checks
  were measured with the literal I9 in place.

## Commit

One commit, on `main`, on the `CryptoReports/**` direct-push path (contract §8). The workflow
filters were read before the push:

- `bench.yml`'s `push` carries `'**.md'` under `paths-ignore`;
- `main.yml`'s `push` is a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`;
- `backtest_bench.yml` triggers on `workflow_dispatch` only.

Message:

```
docs(reports): TZ-43 — BLOCKED, the written I9 replacement cannot hold: nocmp carries eff14 and --attrib's cells do not (TZ-43)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: `CryptoReports/TZ-43-verify-comparability-corrected-report.md`, added.

No hash appears here. This report's own commit has not been made at the time of writing
(inv. 54, contract §10).

## Pull Request

None. By class this is a branch TZ, but the run was BLOCKED before any deliverable was
committed. No implementation commit, branch or pull request exists. The report-only fixed line
is not used, because it would assert a class this TZ does not have.

## CI Execution

No workflow ran on a runner for this task. No branch was pushed, so nothing could trigger one.
Every bench reading in this report is a local run in this session's container.

## Final Repository State

This session leaves the working tree clean at `6bddc0c424ac430316f40297fa3596aba2fbbdcd`
(`origin/main` after the second fetch), which is the commit the fingerprints below were taken
against. The prototype was discarded and the ignored artifacts removed. The prototype diff,
the lane runners and the pristine tree extract live under `/tmp`, outside the repository. No
branch was created or pushed.

Nothing awaits a merge from this TZ, so "NOT IN EFFECT UNTIL MERGED" has no referent and is not
written.

## Fingerprints

Taken at `6bddc0c`. **System Map revision string:** `**Revision 2026-09-13-b.**`

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2691 | `7c8b58ec4dea7142104fc9dc0173edcc` |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` |
| `ANALYST-INSTRUCTIONS.md` | 2615 | `e945ac9e93c03e72f551bc7972541148` |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/backtest_bench.py` | 5008 | `c7fedd64bce7c27c07803325b1f807d3` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
| `bench/backtest_guard_bench.py` | 2438 | `85ea609882ac3761fd526b3ebff2fe5f` |
| `bench/exhaustion_calib.py` | 1031 | `3ac6a4903528cb271cd4f8520b140f27` |
| `.github/workflows/bench.yml` | 153 | `d182e514dcceda5c64410beabc9fe512` |
| `.github/workflows/backtest_bench.yml` | 171 | `703330829c377a15fc0df71e25df92a7` |
| `CryptoTZ/TZ-43-verify-comparability-corrected.md` | 363 | `585b634869e69be6d5e0636b44e03165` |

The table covers:

- the map's `## 0` set;
- the two contracts;
- the three §0 baselines, plus `exhaustion_calib.py`, which §2 names;
- the two workflows, whose filters this report's evidence reads;
- the TZ itself.
