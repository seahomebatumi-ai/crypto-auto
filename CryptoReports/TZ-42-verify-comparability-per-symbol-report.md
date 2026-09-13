# Implementation Report — TZ-42

**The previous TZ is merged.** TZ-41's pull request #38 reads `state: closed`, `merged: true`,
`merged_at: 2026-09-13T09:23:03Z` and `merge_commit_sha: d88593eb…` (REST API,
`curl -s https://api.github.com/repos/seahomebatumi-ai/crypto-auto/pulls/38`). The merge
commit `d88593e` has parents `bd2f197` and `dc42e4e`. `dc42e4e`, the implementation commit
the TZ names, is an ancestor of `origin/main` (`git merge-base --is-ancestor dc42e4e HEAD` →
exit 0). The sequencing clause is met.

## Status

**BLOCKED.**

The fingerprint gate and the sequencing clause both passed. Work stopped on two defects in the
TZ. Each is proven below by a measurement.

1. **§3 edit 8 needs an existing guard assertion edited, and hard-floor items 2 and 12 forbid
   that.** `bench/backtest_guard_bench.py:2333–2334` (section I, check I9) reads the key edit
   8 removes:

   ```
   ok('I9. g beyond --verify\'s window: --verify skips the return fields',
      len(AG['skip']) > 0, AG['skip'])
   ```

   Apply edit 8 and nothing else, and the guard dies at that line with `KeyError: 'skip'`. It
   exits 1, and every check after the crash is lost. TZ-42 does not re-register that assertion.
   Its `## Touches` says no term, population, printed field or exit rule of the attribution
   moves. The only way to keep gate step 14 green is to edit or delete I9, which is exactly
   what the TZ's own §7 quotes:

   > 2. **Never edit a bench to make it pass.** A red bench is either a product defect or
   > a stale expectation; both are findings, neither is a licence to change the
   > assertion.

   > 12. **Never remove, skip, comment out or `continue-on-error` a bench step to make CI
   > green** — editing the assertion (item 2) and deleting the assertion are the same
   > act; a step that cannot pass is a finding for the report.

   TZ-42 §4 applies the same rule to the other bench: a red pre-existing assertion is "a
   finding for the report and a BLOCKED verdict, never an edit".

2. **Lane L5 cannot be satisfied by any implementation that also keeps verify_bench case 5
   green.** L5 requires "every coin's series 30 h short → non-zero exit, the refusal of §3
   edit 9 printed". Under §3 edit 3 a level is comparable at any gap, so edit 9's refusal can
   fire only when every level field is missing from `coeffs.json`. A 30-hour-short series
   leaves every level present. Case 5 ("big gap still exits 0 (expected operational state)")
   is, as far as comparability goes, the same world, and §4 says it stays exactly as written.
   On a measured prototype, L5's world exits 0 and prints no refusal.

**What unblocks it:** a corrected specification from the Architect (contract §12) that:

- **(1)** either re-registers guard assertion I9 (`backtest_guard_bench.py:2333–2334`) by
  name, or withdraws edit 8;
- **(2)** re-specifies L5 so that it holds together with case 5. The options, which are the
  Architect's to choose between, are:
  - name the world where the refusal is reachable (measured below as L5r);
  - change L5's expectation;
  - change §3 edit 9.

Then `EXECUTE` is sent again. Nothing else in the TZ blocked the measured prototype
(`## Implementation Summary`, last two subsections).

## Inbound Filing

None. `CryptoTZ/TZ-42-verify-comparability-per-symbol.md` arrived on `origin/main` in `bb0cdac`
(2026-09-13T15:41:34+04:00), under the canonical filename its header states. `git log --all --
'CryptoTZ/TZ-42*' '*TZ-42*'` lists that one commit and no copy on any other ref.

At session start the worktree stood at `bd2f197`. `git fetch` showed `origin/main` at
`bb0cdac` (with `d88593e`, `4f07a98`, `f51dea1` and `bb0cdac` on top), and the tree was brought
there by `git merge --ff-only origin/main`. The repository is not shallow
(`git rev-parse --is-shallow-repository` → `false`). A second `git fetch --all --prune` before
writing this report left `origin/main` at `bb0cdac`.

## Scope Executed

**Class: branch TZ** (contract §8). `## 2. Scope` names three files outside
`CryptoReports/**`: `bench/backtest_bench.py`, `bench/verify_bench.py` and
`bench/backtest_guard_bench.py`.

Steps run under contract §4a:

- **Steps 1–6 (read, fetch, locate, gate, repository state):** done in full.
- **Step 7 (implement):** entered only as a measurement, disclosed under `## Deviations`. The
  eight §3 edits were written into `bench/backtest_bench.py` in the working tree to find out
  whether the TZ can be satisfied at all. The prototype was measured, its diff was saved
  outside the repository, and it was discarded with `git checkout -- bench/backtest_bench.py`.
  The file's MD5 afterwards is the baseline `c7fedd64bce7c27c07803325b1f807d3`.
  `bench/verify_bench.py` and `bench/backtest_guard_bench.py` were never modified.
- **Step 8 (validate):** each item was run where it produces evidence for the block
  (`## Validation`).
- **Step 9 (branch and pull request):** not reached.
- **Step 10:** this report.

## Files Created

- `CryptoReports/TZ-42-verify-comparability-per-symbol-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None. `bench/_tokens.js` and `bench/__pycache__/` were deleted from the working tree. My own
bench runs made both at 11:56 UTC in this session, both are ignored (`.gitignore:19`
`bench/_*`), and neither was ever tracked.

## Implementation Summary

No implementation was delivered. Below are the two blockers with their evidence, followed by
what the discarded prototype showed about the rest of the TZ, so that a corrected
specification does not need a second round of discovery.

### Blocker 1 — edit 8 against guard I9

Each run is the repository's own `bench/backtest_guard_bench.py`, except where the Guard column
says otherwise. Its `argv[1]` names the `backtest_bench.py` under test.

| Run | Guard | `backtest_bench.py` under test | Result |
|---|---|---|---|
| control | repository | pristine copy in `/tmp/tz42_before/` (MD5 `c7fedd64…`, identical to the repository's) | exit 0, `checks run: 475   FAIL 0` |
| edit 8 alone | repository | the same copy with one line changed: `"skip": R["skip"],` removed from `attrib_run`'s return | **exit 1**, `line 2334 … KeyError: 'skip'`. The last section count printed is `H. transport: 107`, so section I never finishes and section J never runs |
| all eight edits | repository | the prototype | **exit 1**, the same traceback |
| all eight edits, I9's key read neutralised | pristine `git archive HEAD` extract, where `len(AG['skip']) > 0, AG['skip']` → `True, '…'` | the prototype | exit 0, `checks run: 475   FAIL 0` |

The last row shows that I9's read of the key is the **only** guard breakage the eight edits
cause. The neutralised copy was a measuring tool in `/tmp`, not a proposal.

**Why this is a BLOCK and not a recorded deviation.** There are two ways forward, and the TZ
authorises neither of them:

- **(a) Edit I9.** This is hard-floor items 2 and 12.
- **(b) Keep `"skip"` in `attrib_run`'s return.** This contradicts edit 8's explicit text. It
  also needs `reconcile()` to keep producing the old cache-wide `skip`, which is the second
  comparability rule this TZ exists to remove (§1, inv. 20).

Contract §7: "If a TZ appears to require any of the following, the TZ is defective. Report
BLOCKED and quote the conflicting requirement." The conflicting requirement is §3 edit 8,
quoted in `## Status`.

### Blocker 2 — L5 against case 5

**The argument, entirely from the TZ's own text:**

- **§3 edit 3:** "a field not in `RET_FIELDS` → `(True, None)`", and comparability "reads no
  venue, no census and no threshold". A level cell is therefore compared whenever both of its
  sides are present.
- **§3 edit 9:** the refusal fires when `sum(seen[k] … if kind != "info") == 0`. Level cells
  are always comparable, so that sum reaches zero only when all six level fields (`min_price`,
  `max_price`, `min30`, `max30`, `volatility`, `vol7`) are missing for every compared symbol.
  When that happens, §3 edit 6's `never` already names them.
- **L5:** "every coin's series 30 h short". This leaves every level present, so the refusal
  cannot fire.
- **Case 5** (existing, "big gap still exits 0") is a world where every symbol's own gap is
  far beyond the window and every field is present. Comparability-wise that is exactly L5's
  world. Any rule that refuses L5 also refuses case 5.
- **The other reading.** Counting only return cells would satisfy L5. It would also turn case
  5 red, and L1 and L2 too, whose must-hold is exit 0. So the lane has no reading that
  satisfies every row.

**Measured on the prototype** (the lane runner is described in the next subsection):

| World | `--verify` exit | Refusal printed | Classes | Symbol classes |
|---|---:|---|---|---|
| **L5 literal:** every coin 30 h short, production built on the full series (each symbol's own gap +30.5 h) | **0** | no | all empty | `unverified` ×3 |
| L5 literal-b: the short series, production built on the same series at +30.5 h | 0 | no | all empty | `unverified` ×3 |
| case-5 world: +30 h, no mutation | 0 | no | all empty | `unverified` ×3 |
| **L5r:** L5 literal with all six level fields removed from `coeffs.json` | **1** | yes: `СТОП: ни одной сравнимой ячейки — сверка не состоялась. Монет 3, худший разрыв +30.5 ч. Нулевое число сравнений не является совпадением.` | — | — |

In L5 literal the levels were still compared: 3 of 3 on every level field, worst `min30`
−0.478 %, all inside their thresholds.

**L5r on the file BEFORE any edit also exits 1**, through `never` (`['min_price',
'max_price', 'min30', 'max30', 'volatility', 'vol7']`). So edit 9 does not change `--verify`'s
exit code in any world. Wherever it can fire, the unrepaired file already exits 1. What it adds
is the message, and a stop inside `reconcile()` that ends `--target` and `--regime-gate` too,
which `never` does not do.

The memory of earlier runs holds that "build the fixture table and record the collision" is
right only when some reading satisfies every must-hold row. Here no reading does, and blocker 1
would stop the run in any case.

### What the prototype showed for the rest of the TZ

**The prototype:**

- all eight §3 edits plus the printing block;
- `+118 −27` lines in `bench/backtest_bench.py`, 18 hunks under `git diff -U0`;
- measured, then discarded.

**The lane runner:** a scratch script, never committed, built with `verify_bench.py`'s fixture
idiom:

- the census comes from `census_of_doc`;
- the live `coeffs.json` comes from `CdBuilder` on `main.py`;
- `requests` is stubbed;
- class sets are read from `reconcile()`, the exit code from `verify_against_live()`, and the
  arms from `target_gate()`.

**`bench/verify_bench.py`, unmodified, against the prototype:** exit 0, `checks run: 40   FAIL
0`. None of the 40 goes red.

| Lane | World | Exit | `venue-basis` | `coverage` | `unexplained` | Symbol classes | Excluded from `--target` |
|---|---|---:|---|---|---|---|---|
| L1 | +30 h; `r7` +5 pp on every coin | 0 | ∅ | ∅ | ∅ | AAA, BBB, CCC `unverified` | none |
| L2 | −30 h; the same | 0 | ∅ | ∅ | ∅ | AAA, BBB, CCC `unverified` | none |
| L3a | cache-wide 0.5 h; AAA's series 20 h shorter and on the perpetual; AAA `r7` +5 pp | 0 | ∅ | ∅ | ∅ | AAA `unverified` · BBB, CCC `clean` | none |
| L3b | the same world; AAA `min_price` ×1.06 | 0 | {AAA `min_price`} | ∅ | ∅ | AAA `unverified` · BBB, CCC `clean` | none |
| L4 | L3a with AAA on spot | 0 | ∅ | ∅ | ∅ | AAA `unverified` · BBB, CCC `clean` | none |
| L5 | see blocker 2 | 0 | ∅ | ∅ | ∅ | all `unverified` | none — **must-hold fails** |
| L6 | +3.0 h; `r7` +5 pp on every coin | 1 | ∅ | ∅ | {AAA, BBB, CCC `r7`} | all `unexplained` | all three |
| L6 | −3.0 h; the same | 1 | ∅ | ∅ | {AAA, BBB, CCC `r7`} | all `unexplained` | all three |
| L6 | +3.1 h; the same | 0 | ∅ | ∅ | ∅ | all `unverified` | none |
| L7 | `generated_at` = `not a stamp` | 0 | ∅ | ∅ | ∅ | all `unverified` | none |
| L7b | L7 plus AAA `min_price` ×1.06 | 1 | ∅ | ∅ | {AAA `min_price`} | AAA `unexplained` · BBB, CCC `unverified` | AAA |

**Stated as equalities:**

- **L2 = L1.** Both are `(exit 0, every class ∅, {AAA, BBB, CCC: unverified}, excluded {})`.
- **The L3 pair.** The `venue-basis` sets of (a) and (b) are `(∅, {(AAA, min_price)})`. The
  basis note appears in (b) only: `БАЗИС ПЕРП/СПОТ (серия качана с перпетуала, справочно, не
  провал): AAA: min_price -5.7`.
- **L4 = L3a.** Both are `(exit 0, every class ∅, {AAA: unverified, BBB: clean, CCC: clean})`.

**L1's announcement block:**

```
НЕ СВЕРЯЛОСЬ (окно не совпадает): r7, r14, r30, eff14 — ячеек 12 на 3 монетах
  AAA     разрыв во времени +30.0 ч: r7, r14, r30, eff14
  BBB     разрыв во времени +30.0 ч: r7, r14, r30, eff14
  CCC     разрыв во времени +30.0 ч: r7, r14, r30, eff14
```

**L7:** all 12 return cells were not compared, with the reason `разрыв во времени неизвестен`.
Every level field printed `сверок  3 из  3`.

**§5 item 6 extremes, on the prototype:**

| Extreme | Result |
|---|---|
| empty cache | exit 1 on the existing `СТОП: сверять нечего …` refusal |
| `_quality_today.json` side file | exit 0, 3 coins compared |
| `min30` dropped from every coin | exit 1, `never = ['min30']` |
| coin cached but absent from `coeffs.json` | exit 0, the coin ignored |
| single-bar series | **not reached** — see finding 6 below |

### Pre-repair reading (§5 item 5)

**L1's world against the file before any edit** (MD5 `c7fedd64…`):

- **exit 1**;
- `unexplained` = {AAA `r7`, BBB `r7`, CCC `r7`}, and every symbol reads `unexplained`;
- `target_gate` **excludes all three**;
- the same output still prints `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ: доходности r7/r14/r30/eff14 …` and
  `НЕ СВЕРЯЛОСЬ (разрыв во времени 30.0 ч): r7, r14, r30, eff14`.

That is TZ §1's second bullet, reproduced.

**Other readings on the unrepaired file:**

| World | Result on the unrepaired file | What it shows |
|---|---|---|
| L2 (−30 h) | exit 1, the same three cells `unexplained`, and no announcement at all, because the cache-wide `gap` of −30 is not `> 3` | §1's third bullet |
| L3a | exit 0, AAA `r7` classed `venue-basis` and named in the basis note | a 20 h tail forgiven as basis, §1's fourth bullet |
| L4 | exit 1, AAA `r7` `unexplained`, AAA excluded | |
| L6 at +3.1 h | exit 1, three `r7` cells `unexplained` while the same output announces them as not compared | |
| L5 literal | exit 1, BBB `eff14` classed `unexplained` | a real 30-hour shift in the value got a class |

### Further findings for a corrected specification

1. **§5 item 7's premise does not hold.** Neither `bench/clean_bench.py` (`import io, re, sys`)
   nor `bench/direction_bench.py` (standard library only) imports `backtest_bench`, so no edit
   to it can reach them.
   - `python3 bench/clean_bench.py` as written: `IndexError`, exit 1. It takes `<before.html>
     <after.html>`, and `bench.yml` line 13 records that this is why it is outside the gate.
     Given `index.html index.html` it exits 1 with `FAIL 1  script changed only by the
     declared removals`: it is a bench for one past cleanup.
   - `python3 bench/direction_bench.py` as written: exit 2 (usage).
   - The gate's own forms: `--display` exits 0 with `ИТОГО проверок: 15629 | провалов блоков:
     0`. Step 5 is under `## Pre-existing Issues`.
2. **Edit 9 never changes `--verify`'s exit code** (blocker 2 above).
3. **The announcement literal can be false.** `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ` asserts a size where
   the gap is unknown (L7). The prototype appended `(у N разрыв неизвестен)`; the TZ says
   nothing either way.
4. **Edit 7 gives one literal for two modes.** It prescribes `…но в рукава допущено`, but
   `--regime-gate`'s existing sibling line reads `но в сетку допущено`. The prototype used
   each mode's own word.
5. **The guard section's letter, read from the file, is K.** The last section header is `# J.
   \`_gap_hours\` reads the stamp in UTC  (ТЗ-41)` at line 2361. `E` is carried by two
   sections (lines 652 and 894), so counting sections would say L. No section was written.
6. **The single-bar extreme was not reached.** My runner cached a one-bar coin but left it out
   of `coeffs.json`, so `reconcile()` skipped it before any build. It is recorded as not
   reached, not as passed.

## Validation

The TZ's validation was run only as far as it produces evidence for the block. No item is
recorded as passed on a delivered change, because none exists (contract §9).

| # | Item | Result |
|---|---|---|
| 1 | `py_compile`, three benches | exit 0 on the prototype, which was discarded. Nothing is delivered |
| 2 | `verify_bench.py` exit 0, `FAIL 0`, additions only | baseline 40 / FAIL 0. Against the prototype, 40 / FAIL 0. **No lane was added**: the lanes cannot all hold (blocker 2) |
| 3 | guard exit 0, `FAIL 0`, new section | baseline 475 / FAIL 0. Against the prototype, **exit 1** (`KeyError` at I9, blocker 1). Section K was not written |
| 4 | the seven lanes, exit codes and class sets | measured on the prototype (table above). L1, L2 (= L1), the L3 pair, L4 (= L3a), L6 and L7 hold. **L5 fails** |
| 5 | pre-repair reading | done: L1's world exits 1, classes three `r7` cells `unexplained`, and removes all three symbols from the arms |
| 6 | extremes | empty cache, side file, field dropped everywhere, and coin absent from production: measured on the prototype. Single-bar series: **not reached** (finding 6) |
| 7 | `clean_bench.py`, `direction_bench.py` | **fails as written**: `clean_bench.py` needs two positional HTML files, and `direction_bench.py` with no flag exits 2. See finding 1 |
| 8 | `git diff --name-only`, hashes | no diff exists. Every hash below equals its §0 baseline |

## Test Results

**Fingerprint gate (contract §5) — PASSED.**

```
$ grep -n '^\*\*Revision' SYSTEM-MAP-CRYPTOCALCUL.md
17:**Revision 2026-09-13-b.** Baseline: three TZs on the bench's MEASUREMENT layer, merged in
```

Each anchor was matched with `grep -cF`. Each occurs twice: once in the map's own anchor table
(lines 160–165, or line 17 for the revision) and once at its site.

| Anchor | Matched substring | Count |
|---|---|---:|
| revision | `**Revision 2026-09-13-b.**` | 2 |
| direction engine | `### 3.12 Direction engine — veto cascade` | 2 |
| catalyst registry | `### 3.15 Catalyst registry` | 2 |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | 2 |
| analytical engine | `## 11. Analytical engine` | 2 |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 |
| newest invariant | `71. **A measurement that is not RETAINED was not taken,` | 2 |

7 anchors compared, 7 present, 0 missing.

**Map `## 0` file table: 4 files compared, 4 exact.**

| File | Required | Measured | Result |
|---|---|---|---|
| `index.html` | 3799, `4e71da9badca3ccae85b656fdc3773e8` | 3799, `4e71da9badca3ccae85b656fdc3773e8` | exact |
| `main.py` | 518, `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518, `0e3ead8c300d2ee6783303c4bf2fb6b5` | exact |
| `catalysts.json` | 17, `f9b2dd4a3594134b2b7b603de19075c3` | 17, `f9b2dd4a3594134b2b7b603de19075c3` | exact |
| `bench/exhaustion-calibration.txt` | 175, `3b8730b254467c9df4c0a845a0f3cfb3` | 175, `3b8730b254467c9df4c0a845a0f3cfb3` | exact |

**TZ §0 baselines: 3 files compared, 3 exact.** `bench/backtest_bench.py` 5008
`c7fedd64bce7c27c07803325b1f807d3` · `bench/verify_bench.py` 388
`06036d8c3d39ccec6be21d2158ef3ce1` · `bench/backtest_guard_bench.py` 2438
`85ea609882ac3761fd526b3ebff2fe5f`. The contract (v20) measures 814 lines,
`9a257890e9db663eb0fc74129f4841e0`, and the map 2691 lines, `7c8b58ec4dea7142104fc9dc0173edcc`.
Both match the TZ.

**Bench baselines on the unmodified tree:**

| Bench | Command | Exit | Result |
|---|---|---:|---|
| `verify_bench.py` (gate step 4) | `python3 bench/verify_bench.py` | 0 | `checks run: 40   FAIL 0` |
| `backtest_guard_bench.py` (gate step 14) | `python3 bench/backtest_guard_bench.py` | 0 | `checks run: 475   FAIL 0` |

The guard's sections that print their own count: second E 32 · F 29 · G 63 · H 107 · I 94 · J
8. Sections A–D and the first E print none.

The two benches match the TZ's figures of 40 and 475.

## Deviations

One, disclosed under contract §12 ("Do not partially implement around a blocker without
saying so"). Blocker 1 was proven first, from a one-line scratch copy. After that, all eight
edits were written into the working tree as a prototype. It served one purpose: to test
whether anything else in the TZ also blocks, so that one corrected specification can close
everything. It was measured, saved outside the repository, and discarded. No file in the TZ's
scope differs from `origin/main`. No lane was added to `verify_bench.py` and no section to
the guard.

## Pre-existing Issues

- **Gate step 5 cannot finish in this container.** `python3 bench/direction_bench.py --props
  --fixtures --control --sim` exits 1 with `FATAL ERROR: Reached heap limit Allocation failed
  - JavaScript heap out of memory`. The same happens without `--sim`. The container has 955 MB
  of memory in total (`free -m`). The file does not import `backtest_bench`, so this TZ could
  not move it in either direction. This is a fact about the machine; the TZ-41 report records
  the same step as "not measurable here".
- **`clean_bench.py` has no runnable form in this repository** (finding 1). This is by design:
  it is outside the gate and needs two HTML files that are not in the tree.

No fingerprint differed.

## Remaining Risks

- **The defect TZ-42 describes is live on `main`, unchanged.** The pre-repair readings above
  apply today:
  - `--verify` classes cells it announces as not compared, and exits 1 on them;
  - `--target` and `--regime-gate` drop those symbols from their arms;
  - an archive later than production is compared at any distance with no announcement;
  - the `venue-basis` licence forgives a perpetual's 20-hour tail as basis.
- **The prototype's figures describe that prototype only.** A corrected specification may
  change edit 9, L5 or edit 8 in a way that meets interactions this reading did not.

## Commit

One commit, on `main`, on the `CryptoReports/**` direct-push path (contract §8). Both workflow
filters were read and confirmed before the push:

- `bench.yml`'s `push` trigger carries `'**.md'` under `paths-ignore`;
- `main.yml`'s `push` trigger is a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`;
- `backtest_bench.yml` has `workflow_dispatch` as its only trigger.

Message:

```
docs(reports): TZ-42 — BLOCKED, edit 8 breaks guard I9 and lane L5 is unsatisfiable against case 5 (TZ-42)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: `CryptoReports/TZ-42-verify-comparability-per-symbol-report.md`, added.

No hash appears here. This report's own commit has not been made at the time of writing, and a
hash or an outcome for it would be a forecast inside an immutable record (inv. 54, contract
§10).

## Pull Request

None. This is a branch TZ by class, but the run was BLOCKED before any deliverable was
written, so no implementation commit, no branch and no pull request exists. The section is
recorded rather than omitted, because an absent section cannot be told from a forgotten one
(contract §10). The fixed report-only line is deliberately not used: it would assert a class
this TZ does not have.

## CI Execution

No workflow ran on a runner for this task. No branch was pushed, so nothing could trigger one.
`bench.yml` and `backtest_bench.yml` did not run for this task, and neither was modified. Every
bench reading in this report is a local run in this session's container. No forecast is offered
for any runner (inv. 54).

## Final Repository State

This session leaves the working tree clean at `bb0cdac312316336e3deae39c6a7d2fc73386c87`
(`origin/main` after the fetch). No file in the TZ's scope is modified: the prototype was
discarded, and the ignored artifacts this session produced were removed. The scratch lane
runner, the pristine copies and the prototype diff live under `/tmp`, outside the repository.
No branch was created or pushed. The fingerprints below were taken against that commit.

Nothing awaits a merge from this TZ, so "NOT IN EFFECT UNTIL MERGED" has no referent and is not
written.

## Fingerprints

Taken at `bb0cdac`, when this report was written.

**System Map revision string:** `**Revision 2026-09-13-b.**`

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
| `.github/workflows/bench.yml` | 153 | `d182e514dcceda5c64410beabc9fe512` |
| `.github/workflows/backtest_bench.yml` | 171 | `703330829c377a15fc0df71e25df92a7` |
| `CryptoTZ/TZ-42-verify-comparability-per-symbol.md` | 298 | `9c844053b8b5a6b912cff3ed49e590f8` |

The table covers these files:

- **The map `## 0` set:** the map plus `index.html`, `main.py`, `catalysts.json` and
  `bench/exhaustion-calibration.txt`.
- **The two contracts:** recorded for the audit's comparison.
- **The three benches:** TZ-42's §0 baseline table names them.
- **The two workflows:** recorded because the TZ closes them (§2, hard-floor item 8) and this
  report's evidence reads their filters.
- **The TZ itself.**
