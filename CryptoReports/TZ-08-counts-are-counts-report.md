# Implementation Report — TZ-08

**A check count counts checks.** Three independent scopes: the zero-comparison
guard in four gate benches, honest counters in every block of
`direction_bench.py`, and one superseded comment in `index.html`.

## Status

**COMPLETED.** All three scopes executed, every §6 validation item run in full,
`Bench gate` executed on a GitHub runner and concluded `success`.

No pull request exists. See `## Pull Request` — **a branch with no pull request
is a branch with no CI**, but that consequence does *not* apply here: TZ-07 §6
added `claude/**` to the `push` trigger of `bench.yml`, so the gate ran on the
branch push. The consequence that remains is only that nothing is merged.

**Previous TZ's branch:** `claude/execute-tz-07-rgd98m` **was merged** (PR #7,
merge commit `b52bcaa`). This work is not stacked on an unmerged base.

## Inbound Filing

None. `CryptoTZ/TZ-08-counts-are-counts.md` was already present on `origin/main`
under its canonical name (commit `aa08188`). No file was moved or renamed.

The session clone was **shallow** (`git rev-parse --is-shallow-repository` →
`true`). Per contract §3 it was deepened with `git fetch --unshallow` before any
assessment; the complete history is 284 commits.

## Scope Executed

| Scope | Subject | Result |
|---|---|---|
| A | Zero-comparison guard in 4 benches | done |
| B | Honest check counts in `direction_bench.py` | done |
| C | Superseded venue comment in `index.html` | done |

## Files Created

None.

## Files Modified

| File | Lines before → after | MD5 before → after |
|---|---|---|
| `bench/verify_board.js` | 190 → 194 | `9a371afb1bb3904b4e8fa3b316b64395` → `166995e3c4321664ca0dc41399b54581` |
| `bench/board2_bench.js` | 195 → 199 | `b18a28ddd40ea8a9524f4f18f53720b5` → `9432e2bb149199f7c2b69d59c49903e0` |
| `bench/prot_bench.js` | 458 → 463 | `59e1f2af47dd3a75e2f1d954fd58c820` → `94b5bb01ef44e369a31be8ae7818fa05` |
| `bench/verify_bench.py` | 248 → 254 | `5f3112a8767169c69245de2ea3cdc724` → `877e91e3b5664158b81d7972cac79112` |
| `bench/direction_bench.py` | 784 → 833 | `34786b11afccfa5e84ef4158f8435e4c` → `8e0f5516164558b480913bdd47bc1ae4` |
| `index.html` | 3522 → **3522** | `a7b10d80bea67824cf9643842d2e505a` → `68eebc9b5e40c7afd09a7d00d3fd1d21` |

## Files Renamed

None.

## Files Deleted

None. `image.PNG` left in place (PWA icon, contract §6).

## Implementation Summary

### Scope A — the guard, in exactly four benches

Each of the four now exits non-zero when it performed zero comparisons, printing
one grep-able line first. The guard sits **after** the existing summary line and
**before** the existing exit, so a red run still prints its own numbers; it can
only ever make a bench redder. No assertion, message or exit path changed.

| File | Counter | Zero condition | Line printed |
|---|---|---|---|
| `bench/verify_board.js` | `checks` | `checks === 0` | `FAIL bench verified nothing` |
| `bench/board2_bench.js` | `checks` | `checks === 0` | `FAIL bench verified nothing` |
| `bench/prot_bench.js` | `pass`, `fail` | `pass + fail === 0` | `FAIL bench verified nothing` |
| `bench/verify_bench.py` | `checks[0]` | `checks[0] == 0` | `  FAIL bench compared nothing` |

Wording follows the existing precedent in `fresh_bench.js` / `catalyst_bench.js`
(JS) and `render_bench.py` / `display_bench.py` (Python); no new idiom was
introduced.

**§3.3 honoured.** `prot_bench.js` guards on `pass + fail`, not on either alone.
`index.html.prev` does **not** exist in the repository (verified: `ls
index.html.prev` → `No such file or directory`), so today's 168 is already the
"no baseline" case: the optional suites are skipped and the run is still legal.

**§3.4 honoured.** `fresh_bench.js`, `journal_bench.js`, `catalyst_bench.js`,
`display_bench.py`, `render_bench.py` and `direction_bench.py` were **not**
touched for this scope. The TZ's correction to the TZ-07 report is confirmed by
reading the code: `fresh_bench.js:173` has `if (checks === 0) … exit 1`, and
`direction_bench.py` guards in `main()` (`if cnt == 0: ok = False`), which covers
**every** block, not only `--display`. No second guard was added to either.

### Scope B — a count must be a count

Every block of `direction_bench.py` now returns a counter incremented at the
comparison site. Where the comparison happens inside the sandboxed JS string the
counter (`cmp`) is incremented there and returned in the block's JSON, exactly as
`ordFail` and `badNo` already were.

The rule applied throughout, stated once so the number can be decomposed: **one
increment per evaluated failure condition.** A quantity that is only measured and
printed — `checks` (scenarios), `trades`, `waits`, `nones`, `greys`, `lists`,
`bothNo`, `len(res)` — is *not* a check and does not increment the counter. This
is the same line invariant 22 draws: the count is a count of verifications.

**No assertion, threshold, fixture, seed, case count or failure condition was
changed.** Every block prints byte-identical findings to its pre-edit run (same
regimes, same R:R values, same verdicts, same statistics) — see `## Test
Results`. The only message changes are the two `наблюдений: N` additions required
by §4.2.

### Scope C — the comment that outlived its reason

Two lines out, two lines in, `index.html` stays at **3522 lines**. The `ZEC / UNI`
line above and the two-line `Правило:` note below are untouched. Not one
executable character changed.

## Validation

### §6.0 System Map fingerprint gate — PASS, before any work

| Anchor | Required | Found |
|---|---|---|
| `<!-- EDIT-MARKER 2026-08-22-COVERAGE-SEMANTICS -->` | 1 occurrence | **1** (line 1017) |
| `<!-- EDIT-MARKER 2026-08-22-GATE-COMPOSITION -->` | 1 occurrence | **1** (line 1361) |
| `## 4. Инварианты`, highest number | 43 | **43** |
| `## 9. Журнал миграций`, newest entry | `- 2026-08-22 (2):` | **`- 2026-08-22 (2):`** |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1807 lines, MD5 `476339934c9dcf14e0f4bf2353900d89` | **1807**, **`476339934c9dcf14e0f4bf2353900d89`** |

### §6.1 Baseline — every file matched the TZ header exactly

```
index.html                     3522  a7b10d80bea67824cf9643842d2e505a
main.py                         506  1a5a5d98b2fd76010f202ee3eebaa717
catalysts.json                   15  eb591d2ef2d792ca6a4a25f26442e9b9
bench/verify_board.js           190  9a371afb1bb3904b4e8fa3b316b64395
bench/board2_bench.js           195  b18a28ddd40ea8a9524f4f18f53720b5
bench/prot_bench.js             458  59e1f2af47dd3a75e2f1d954fd58c820
bench/verify_bench.py           248  5f3112a8767169c69245de2ea3cdc724
bench/direction_bench.py        784  34786b11afccfa5e84ef4158f8435e4c
```

All eight are byte-identical to the §0 baseline table. The diff below is therefore
provable against a known state.

### §6.2 Syntax

| Command | Result |
|---|---|
| `node --check` on the `<script>` extracted from `index.html` (175 740 bytes, 2954 lines) | exit 0 |
| `python3 -m py_compile bench/direction_bench.py` | exit 0 |
| `python3 -m py_compile bench/verify_bench.py` | exit 0 |
| `python3 -m py_compile main.py` (file untouched) | exit 0 |
| `node --check bench/verify_board.js` | exit 0 |
| `node --check bench/board2_bench.js` | exit 0 |
| `node --check bench/prot_bench.js` | exit 0 |

`__pycache__` removed afterwards; the working tree carries no generated artifact.

### §6.3 No-regression, proven not asserted

`git diff --stat` on the whole tree, before commit:

```
 bench/board2_bench.js    |  4 +++
 bench/direction_bench.py | 83 ++++++++++++++++++++++++++++++++++++++----------
 bench/prot_bench.js      |  5 +++
 bench/verify_bench.py    |  6 ++++
 bench/verify_board.js    |  4 +++
 index.html               |  4 +--
 6 files changed, 87 insertions(+), 19 deletions(-)
```

**Zero changes to `main.py`, `catalysts.json`, `journal/**` and `.github/**`** —
they do not appear in the diff at all, and their post-edit MD5s equal their
baseline MD5s (`main.py` `1a5a5d98b2fd76010f202ee3eebaa717`, `catalysts.json`
`eb591d2ef2d792ca6a4a25f26442e9b9`). No workflow was touched; action versions are
unchanged; the Node 20 deprecation warning is still present on the runner and was
deliberately left alone (TZ §2).

`git diff -U0 -- index.html`, in full:

```
diff --git a/index.html b/index.html
index 6291dca..f8dc01f 100644
--- a/index.html
+++ b/index.html
@@ -769,2 +769,2 @@ var tokens = [
-    // XMR — спот делистнут Binance (2024) => fut:true.
-    // LIT — статус спот-пары не подтверждён => fut:true.
+    // XMR / LIT / HYPE — площадка ОБЪЯВЛЕНА: только фьючерсы (карта §3.14,
+    // инв. 41). Живая строка зеркала объявление не отменяет.
```

**Every `+` and `-` line matches `^\s*//`.** Verified mechanically, not by eye:
filtering the diff for `+`/`-` content lines that do *not* match `^[+-]\s*//`
returns nothing. Line count unchanged at **3522**.

### §6.4 Scope A — counts, exit codes, and a forced zero case per bench

Post-edit, on real work — unchanged from today:

| Bench | Count | Required | Exit | Required |
|---|---:|---:|---:|---:|
| `verify_board.js` | 109 | 109 | 0 | 0 |
| `board2_bench.js` | 130 | 130 | 0 | 0 |
| `prot_bench.js index.html` | 168 | 168 | 0 | 0 |
| `verify_bench.py` | 35 | 35 | 0 | 0 |

**Forced zero case.** In each bench the comparison-site increments were
short-circuited in place (`checks++` → `checks+=0`; `pass++`/`fail++` →
`pass+=0`/`fail+=0`; `checks[0] += 1` → `checks[0] += 0`), so the bench executes
its whole body and records zero comparisons — precisely the failure mode the TZ
names ("a future edit that empties their case set leaves them green"):

| Bench | Summary printed | Guard line printed | Exit |
|---|---|---|---:|
| `verify_board.js` | `--- checks: 0  fails: 0 ---` | `FAIL bench verified nothing` | **1** |
| `board2_bench.js` | `--- checks: 0  fails: 0 ---` | `FAIL bench verified nothing` | **1** |
| `prot_bench.js` | `PASS 0   FAIL 0` | `FAIL bench verified nothing` | **1** |
| `verify_bench.py` | `checks run: 0   FAIL 0` | `  FAIL bench compared nothing` | **1** |

The summary line precedes the guard line in all four — §3.2 satisfied.

**The defect is proven, not assumed.** The same short-circuit applied to the
**pre-edit `HEAD` version** of each file exits **0**:

| Bench at `HEAD` (no guard) | Output | Exit |
|---|---|---:|
| `verify_board.js` | `--- checks: 0  fails: 0 ---` | **0** |
| `board2_bench.js` | `--- checks: 0  fails: 0 ---` | **0** |
| `prot_bench.js` | `PASS 0   FAIL 0` | **0** |
| `verify_bench.py` | `checks run: 0   FAIL 0` | **0** |

Each pair is a red-then-green control in its own right, which is why §6.8 does not
require a planted CI failure.

**Reverted and verified byte-identical** to the post-edit state (`md5sum -c`
returned `OK` for all four), and green again at 109 / 130 / 168 / 35, exit 0.

### §6.5 Scope B — one row per block

| Block | Old expression | Old | New | What is now counted |
|---|---|---:|---:|---|
| `check_identity` | `r["compared"]` | 200 000 | 200 000 | **already honest — untouched.** `cmp++` already sat at the comparison site. |
| `check_props` | `r["checks"] * 8` | 480 000 | **188 565** | 3 property assertions per scenario, plus 3 geometry assertions per **trading** side |
| `check_fixtures` | `len(rows) * 4` | 16 | **4** | the 4 pre-registered assertions |
| `check_display` | `r["lists"] * r["trades"] + len(r["tier"])` | 57 661 | **15 629** | 1 order comparison per adjacent pair, 1 numbering comparison per row, 9 tier-boundary probes |
| `check_control` | `len(res)` | 2 210 | **2** | the 2 statistical assertions (each arm inside 2SE of zero) |
| `check_sim` | `len(res)` | 7 560 | **6** | 2 pre-registered assertions × 3 worlds |

Both new numbers decompose exactly:

- `check_props` = 3 × 60 000 scenarios + 3 × 2 855 trading sides = 180 000 + 8 565 = **188 565**
- `check_display` = 284 × 27 order pairs + 284 × 28 rows + 9 probes = 7 668 + 7 952 + 9 = **15 629**

**§4.4 — which blocks landed identical.** **None of the five rewired blocks.** All
five fell. `check_identity` is the one block whose number is unchanged (200 000),
and it was unchanged because it was **already** a counter at the comparison site,
not because an old expression happened to be right. It is excluded from the gate
by design (it reads `orig.html`, which is not in the repository — `bench.yml`
header), so its 200 000 does not enter any gate total, before or after.

**§4.3 — the total fell and nothing was compensated.** Not one comparison was
added anywhere, no assertion was split, no case set was enlarged. Reconciliation
is in §6.7.

**§4.2 — the two statistical blocks now report two numbers.** `check_control`
returns 2 and prints `наблюдений: 2210`; `check_sim` returns 6 and prints
`наблюдений: 7560`. Both numbers are true; only one of them is a check.

#### §4.5 Proportionality — the counters move with the work

**`check_display`, case set cut in half** (`n=4000` → `n=2000`):

| | lists | new count | old expression would give |
|---|---:|---:|---:|
| full | 284 | **15 629** | 57 661 |
| half | 142 | **7 819** | 14 919 |

The variable term halves **exactly**: 15 629 − 9 = 15 620 → 7 819 − 9 = 7 810.
The residual 9 is the tier-boundary probe set, which is a fixed case set and was
not halved — so the decomposition is complete with no unexplained remainder.

The same halving under the **old** expression drops 57 661 → 14 919, a **3.87×**
fall for a **2×** cut in work, because `lists × trades` is a product in which both
factors halve. That is the defect in one line: the old number did not track the
work even in direction.

Restored, and the original number returns: **15 629** (`md5sum` of the restored
file matches the post-edit hash `8e0f5516164558b480913bdd47bc1ae4`).

**`check_props`, case set cut in half** (`n=60000` → `n=30000`): **188 565 →
94 311**, which decomposes as 3 × 30 000 + 3 × 1 437 trading sides = 94 311.
Restored → **188 565**, file hash verified.

#### The `--display` zero guard still fires, unchanged from TZ-07

Forcing `check_display` to compare nothing (`n=0`, tier probe list emptied):

```
[FAIL] ОТОБРАЖЕНИЕ
отображение: 0 списков -> торгуемых 0, ожиданий 0, серых 0; …
  ПРОВАЛ: блок не сверил ничего

ИТОГО проверок: 0 | провалов блоков: 1
EXIT=1
```

The `main()` guard is untouched and now receives a real count rather than a
product, which is the point of §1(b): the guard was decorative while its input
could move for reasons other than comparisons.

#### §4.6 — the same defect in another gate bench: **none found, nothing fixed**

Every other bench in the gate increments its counter at the comparison site:

| Bench | Evidence |
|---|---|
| `fresh_bench.js` | `checks++` inside `eq()` (`:40`); `ok()` delegates to `eq()` |
| `catalyst_bench.js` | `checks++` inside `eq()` (`:47`, `:54`) and at the sweep comparison (`:222`) |
| `journal_bench.js` | `checks++` inside `eq()` (`:27`), `deq()` (`:31`) and 11 inline comparison sites |
| `display_bench.py` | `checks += 1` at each comparison (`:182`, `:186`, `:203`, `:237`, `:254`) |
| `render_bench.py` | `checks += 1/2/3` at comparison sites |

`render_bench.py`'s batched `+= 2` and `+= 3` were read line by line and are
**not** the defect: each covers a fixed, adjacent, enumerable set of comparisons
immediately below it (`+= 3` at `:383` covers rank, score, and exactly one of
three mutually exclusive glyph branches), not an assumed factor over a scenario
count. **No other bench's number was changed.** One narrow observation is recorded
under `## Pre-existing Issues`.

### §6.6 Scope C

The full gate is green on the edited `index.html` — six of the eleven steps
(`verify_board.js`, `board2_bench.js`, `prot_bench.js`, `display_bench.py`,
`render_bench.py`, `direction_bench.py --display`) execute production functions
cut out of that file, and all six pass locally and on the runner.

`index.html` after the edit: **3522 lines**, MD5
**`68eebc9b5e40c7afd09a7d00d3fd1d21`**.

### §6.7 Full gate — every step of `bench.yml`, in order

Runner numbers (GitHub Actions run 36, Python 3.12.14, node 20.20.2). The local
run on Python 3.11.15 / node 22.22.2 produced **identical** counts, step for step.

| # | Step | TZ-07 | **TZ-08** | Δ | exit |
|---:|---|---:|---:|---:|---:|
| 1 | `verify_board.js` | 109 | **109** | 0 | 0 |
| 2 | `board2_bench.js` | 130 | **130** | 0 | 0 |
| 3 | `prot_bench.js index.html` | 168 | **168** | 0 | 0 |
| 4 | `verify_bench.py` | 35 | **35** | 0 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 489 786 | **188 577** | −301 209 | 0 |
| 6 | `fresh_bench.js` | 3 424 | **3 424** | 0 | 0 |
| 7 | `journal_bench.js` | 694 030 | **694 030** | 0 | 0 |
| 8 | `catalyst_bench.js` | 23 007 | **23 007** | 0 | 0 |
| 9 | `display_bench.py` | 24 598 | **24 598** | 0 | 0 |
| 10 | `render_bench.py` | 15 925 | **15 925** | 0 | 0 |
| 11 | `direction_bench.py --display` | 57 661 | **15 629** | −42 032 | 0 |
| | **Total** | **1 308 873** | **965 632** | **−343 241** | |

**Reconciliation against 1 308 873, every term accounted for:**

| Term | Before | After | Δ | Kind |
|---|---:|---:|---:|---|
| `check_props` | 480 000 | 188 565 | −291 435 | removed multiplier ×8 |
| `check_fixtures` | 16 | 4 | −12 | removed multiplier ×4 |
| `check_display` | 57 661 | 15 629 | −42 032 | removed product `lists × trades` |
| `check_control` | 2 210 | 2 | −2 208 | removed sample size |
| `check_sim` | 7 560 | 6 | −7 554 | removed sample size |
| | | | **−343 241** | |

291 435 + 12 + 42 032 + 2 208 + 7 554 = **343 241**, and 1 308 873 − 343 241 =
**965 632**. Every term of the difference is a removed multiplier or a removed
sample size, and nothing else moved: **the other nine step numbers are identical
to TZ-07's, to the unit.** Nothing had to be absorbed and there is nothing to
report under contract §7.2 on this point.

Step 5's Δ is the sum of its four block deltas: 291 435 + 12 + 2 208 + 7 554 =
301 209 = 489 786 − 188 577. ✓

## Test Results

Every block of `direction_bench.py` prints **byte-identical findings** before and
after, which is the evidence that only the counting changed:

| Block | Finding, before and after |
|---|---|
| `СВОЙСТВА` | `60000 сценариев -> сделок 2855, ожиданий 13900, отказов 103245` |
| `ФИКСТУРЫ` | режим `range`; GRAM long `rr=7.64 5.78сигм -> trade`; GRAM short `rr=0.04 -> none`; ZEC long `rr=1.55 -> none`; ZEC short `rr=2.86 -> trade` |
| `КОНТРОЛЬ` | `прежняя -0.001 (2SE 0.080), движок -0.149 (2SE 0.324, n=226)` |
| `СИНТЕТИКА` | mean 42→42 / R −0.623→−0.611 · trend 42→39 / R −0.748→−0.345 · walk 42→42 / R −0.540→−0.400 · цель в шуме 0→0 in all three |
| `ОТОБРАЖЕНИЕ` | `284 списков -> торгуемых 203, ожиданий 829, серых 6920`, `монет с номером с обеих сторон 3976` |

The only textual differences are the two `наблюдений: N` sample sizes required by
§4.2.

## Deviations

None. Every §6 item was run; none was skipped, none was declared inapplicable.

Two judgement calls, both inside the specification and recorded so the Architect
can overrule them:

1. **What counts as one comparison.** The counter increments once per **evaluated
   failure condition**. Quantities that are only measured and printed (scenarios,
   trades, waits, greys, lists, `bothNo`, `len(res)`) do not increment it. This is
   the reading §4.2 forces for the statistical blocks — "both are true; only one
   of them is a check" — applied uniformly so the gate total decomposes by the
   same rule everywhere.
2. **`check_fixtures` counts 4, not 4 per row.** The block builds 4 rows and makes
   4 assertions, one per row, but they are not "four comparisons per row": ZEC's
   `min30` is flagged in the source as an assumption that takes no part in the
   checks, and GRAM long is asserted only on R:R. `len(rows) * 4` = 16 was
   therefore wrong by construction *and* by magnitude.

## Pre-existing Issues

1. **Four gate benches exited 0 having compared nothing** (TZ §1, Defect 1) —
   pre-existed, proven on the unmodified `HEAD` versions in §6.4, **fixed by this
   TZ** (Scope A).
2. **The gate's headline number was not a count** (Defect 2) — pre-existed,
   **fixed by this TZ** (Scope B). Consequence for the record: TZ-07's
   `1 199 724 → 1 308 873` reconciliation was, as the System Map's invariant 43
   already states, inflated by 343 241 estimated units and was not usable as
   evidence of control volume. The honest figure is **965 632**.
3. **`index.html` carried a superseded reason for `fut:true` on LIT**
   (Defect 3) — pre-existed, **fixed by this TZ** (Scope C).
4. **`render_bench.py:332` over-counts by 1 on one failure path.** `checks += 2`
   is followed by `continue` when the badge is unparsable, so the second of the
   two comparisons it accounts for is not reached. Reported, **not fixed**: the
   path executes only on a run that is already red, so it can never inflate a
   green total, and §4.6 authorises a fix only for the identical defect —
   widening this one would be a change to a bench the TZ excludes from scope.
   Left for the Architect.
5. **`check_identity` cannot execute in this repository.** It reads `orig.html`,
   which does not exist; `bench.yml` excludes it from the gate for that reason.
   Pre-existing and documented in the workflow header; not touched.

## Remaining Risks

1. **Nothing is merged.** No pull request exists (see `## Pull Request`). The
   gate ran green on the branch, but `main` still carries the old benches and the
   old comment. **NOT IN EFFECT UNTIL MERGED.**
2. **The honest total is now sensitive to product behaviour in a way the old one
   was not.** `check_props` returns 3 × scenarios + 3 × trading sides, so a
   product change that alters how many sides come back `trade` moves the gate
   total legitimately. That is correct — the count follows the comparisons — but
   it means a future reconciliation must decompose the number rather than expect
   a constant. The two terms are printed side by side in the block's own message
   (`сценариев` and `сделок`), so the decomposition is always available from the
   log.
3. **`prot_bench.js`'s guard cannot distinguish "baseline absent" from "baseline
   present but empty".** Per §3.3 that is intended: the guard is on total
   comparisons, and a skipped optional suite is legal. Should `index.html.prev`
   ever be added to the repository, the baseline suites' own coverage is not
   separately guarded. Reported, not acted on.
4. **The Node 20 deprecation warning persists on every runner job** (visible in
   run 36's log). Left alone by TZ §2 `[решение принято мной]`; it is a warning
   and the jobs are forced onto Node 24 automatically.

## Commit

```
3efbf98  fix(controls): a check count counts checks (TZ-08)
```

Branch `claude/execute-tz-08-lpkhu2`, six files, `87 insertions(+), 19 deletions(-)`.
The commit message is the string given in TZ §8, verbatim. This report is committed
separately, directly to `main`, per contract §8.

## Pull Request

**NO PULL REQUEST EXISTS.** This session runs under a base configuration that
forbids opening one without an explicit instruction. Contract §8 fallback applied.

- **Branch:** `claude/execute-tz-08-lpkhu2`
- **Compare URL:** https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-08-lpkhu2

**A branch with no pull request is a branch with no CI** — that is the standing
rule, and the reason it is stated in bold here. **In this instance the CI
consequence did not materialise:** TZ-07 §6 added `claude/**` to `bench.yml`'s
`push` trigger precisely to close that hole, and the gate executed on this branch
push and concluded `success` (see `## CI Execution`). What remains missing is the
merge, not the proof.

## CI Execution

| Workflow | Ran on a runner? | Run | Conclusion |
|---|---|---|---|
| **Bench gate** (`bench.yml`) | **yes** | **#36**, id `32557010968` | **`success`** |
| `main.yml` (bot) | no | — | its `push` trigger is `branches: [ main ]` only (plus `workflow_dispatch`); a `claude/**` branch push does not match |
| `journal.yml` | no | — | triggers are `schedule: '0 13 * * *'` and `workflow_dispatch`; no `push` trigger at all |
| `backtest_bench.yml` | no | — | `workflow_dispatch` only; needs the `data.binance.vision` archive and a warm cache, out of the gate by design, not touched by this TZ |

- **URL:** https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32557010968
- **Head SHA:** `3efbf980acd06531895c00d4354a0b2c8cd71837`
- **Event:** `push` to `claude/execute-tz-08-lpkhu2`
- **Duration:** 06:27:20Z → 06:28:17Z
- **Steps:** 11 bench steps, **all `success`**, no step skipped, no
  `continue-on-error` anywhere.

The runner reproduced every count exactly: 109 · 130 · 168 · 35 · 188 577 · 3 424
· 694 030 · 23 007 · 24 598 · 15 925 · 15 629 = **965 632**.

**No failure was planted in CI**, per TZ §6.8. The gate's ability to fail was
proven on the runner in TZ-07 run 29, and each Scope A guard proof in §6.4 is
itself a red-then-green control, executed locally with both halves shown.

Per contract §9, the distinction is stated rather than glossed: the §6.4 forced
zero cases, the §4.5 proportionality proofs and the syntax checks were run
**locally**; the full gate was run **both locally and on a GitHub runner**, with
identical results.

## Final Repository State

- Branch `claude/execute-tz-08-lpkhu2` pushed to `origin`, 1 commit ahead of `main`.
- `main` carries this report only; the implementation is **not** on `main`.
- Working tree clean; no scratch file, no `__pycache__`, no duplicate, no
  superseded copy left behind.
- Pushing this report to `main` is safe under contract §8 and was re-verified,
  not assumed: GitHub Pages serves `index.html`, and `- '**/*.md'` is present in
  `main.yml`'s `paths-ignore`, so a Markdown file under `CryptoReports/` can
  neither reach the live calculator nor start the bot.
- No pull request. Merge from the compare URL above.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1807 | `476339934c9dcf14e0f4bf2353900d89` |
| `index.html` | 3522 | `68eebc9b5e40c7afd09a7d00d3fd1d21` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |

| `catalysts.json` | 15 | `eb591d2ef2d792ca6a4a25f26442e9b9` |

System Map, newest `## 9. Журнал миграций` entry: **2026-08-22 (2)**.

`SYSTEM-MAP-CRYPTOCALCUL.md`, `main.py` and `catalysts.json` are byte-identical to
their state at session start; none of the three was touched. `index.html` changed
by two comment lines only and holds its line count at 3522.
