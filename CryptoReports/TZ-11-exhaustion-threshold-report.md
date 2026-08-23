# Implementation Report — TZ-11

Exhaustion threshold: calibrate on a runner, wire one consumer.

## Status

**PARTIAL.** Stages A and B are COMPLETED. Stages C and D are **BLOCKED on the
merits** — the status TZ-11 §2 writes as `ЗАБЛОКИРОВАНО` — by the adoption rule TZ-10 registered before the number existed and
TZ-11 §2 restated: the calibration run produced a pooled 90th percentile of
**1.59**, which is below the **1.60** floor of the registered window `1.60 … 4.00`.

No production change was made. `index.html` is byte-identical to `origin/main`.
The number was not nudged to reach the floor, and no consumer was wired.

Per TZ-11 §2 Stage B, restating the registered rule:

> Below **1.60** or above **4.00**, Stages C and D are **ЗАБЛОКИРОВАНО** on the
> merits: no production change, the full decile table in the report, and the
> answer is a new TZ. The script enforces the window itself and exits non-zero
> outside it.

The script did exactly that. It printed `verdict : BLOCKED — outside the window.`
and exited 1.

**The previous TZ's branch was merged.** TZ-10 landed as PR #10, `baa9d9b`, and
`origin/main` is two commits beyond it (`afd2aa8` map update, `7449721` upload).
This work is not stacked on an unmerged base.

## Inbound Filing

None. `CryptoTZ/TZ-11-exhaustion-threshold.md` was already present on
`origin/main` under its canonical filename after `git fetch --all --prune`. No
artifact arrived under a mangled name and no `git mv` was required.

The clone was checked for truncation as §3 requires, and **was** truncated:

```
$ git rev-parse --is-shallow-repository
true
$ git fetch --unshallow
$ git rev-parse --is-shallow-repository
false
$ git rev-list --count HEAD
301                     # was 78 before unshallowing
```

The clone arrived shallow at 78 commits and was deepened to the full 301 before
anything historical was assessed. No finding in this report rests on truncated
history: every baseline comparison is against `origin/main` at `7449721`, which
is the same object before and after the unshallow, and the gate baseline was
measured in a `git worktree` checked out from it.

## Fingerprint gate — PASSED

All four content anchors are present in the repository copy of the System Map,
matched as exact substrings, and the revision string is the one TZ-11 requires.

| Anchor | Required string | Found |
|---|---|---|
| revision | `**Revision 2026-08-23-a.**` | line 15 |
| direction engine | `### 3.12 Direction engine — veto cascade` | line 596 |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | line 866 |
| newest invariant | `46. **A calibrated constant is checked against its calibration record.**` | line 973 |

Baseline stated by the TZ: `index.html` 3569 lines, MD5
`56af2e274e5568527a6bb0e5cb4e3456`. Measured: **identical**.

The map's own `## 0. Fingerprint` block declares `index.html` 3569 /
`56af2e274e5568527a6bb0e5cb4e3456`, `main.py` 506 /
`1a5a5d98b2fd76010f202ee3eebaa717`, `catalysts.json` 11 /
`021dd2c90dc395240c0b0c3dbae40426`. All three measured identical. **No
fingerprint drift in either direction** — nothing to report under Pre-existing
Issues on that count.

`git fetch --all --prune` was run first and every baseline comparison in this
report is taken from `origin/main`, never from local `main`, as the TZ header
requires.

## Scope Executed

| Stage | Outcome |
|---|---|
| A — repair the baseline differ | **COMPLETED** |
| B — run the calibration where the archive answers | **COMPLETED** (ran, produced a number, verdict BLOCKED) |
| C — adopt the constant, wire one consumer | **BLOCKED on the merits** — not implemented |
| D — pin the constant to its record, finish the bench | **BLOCKED** — depends on C |

Stages A and B are independent, and the TZ states that a blocked B does not block
A. Here B was not blocked — it executed and returned a verdict — and that verdict
blocks C, which blocks D. Stage A is unaffected and shipped.

## Files Created

- `.github/workflows/calib.yml` — the Stage B calibration workflow.

## Files Modified

- `bench/prot_bench.js` — symmetric strip removed, identity run added to the
  default suite, comparison counter and its zero-comparison guard.

## Files Renamed

None.

## Files Deleted

None.

## Files NOT Modified

Stated explicitly because the blocked stages are the ones that would have touched
them:

- `index.html` — untouched. No `DAY_RANGE_ABNORMAL` constant, no `listExhaustion`
  change, no `update()` change, no `regimeBanner` change.
- `bench/exhaustion_bench.js` — untouched.
- `bench/exhaustion-calibration.txt` — does not exist in the repository. See
  Deviations.
- `main.py`, `catalysts.json`, `journal/**`, `.github/workflows/bench.yml`,
  `.github/workflows/backtest_bench.yml` — untouched, as §3 Non-goals requires.

```
$ git diff --stat origin/main
 .github/workflows/calib.yml | 91 +++++++++++++++++++++++++++++++++++++++++++++
 bench/prot_bench.js         | 74 ++++++++++++++++++++++--------------
 2 files changed, 137 insertions(+), 28 deletions(-)
```

## Implementation Summary

### Stage A — the differ was measuring its own transformation

`suiteNoRegression` located the «ЗАЩИТА ПОЗИЦИИ» section in the **candidate**
output, cut it out by div-depth matching, and compared the remainder against the
**baseline** in full. That was correct exactly once: while the baseline predated
the section and the candidate carried it. Both revisions have carried it since
TZ-07, so the transformation stopped compensating for anything and became a
one-sided deletion — six differences manufactured by the differ itself, against a
file compared with a byte-identical copy of itself.

The repair takes the option the TZ prefers: **neither side is stripped**. The
assertion is not weakened, it is strengthened — the comparison is now over the
whole board, protection section included.

The identity run is the second half, and it is the half that makes the differ
admissible as evidence at all (inv. 45). `index.html` is read a second time and
evaluated into its own VM context, so the two sides of the comparison are
independent evaluations of the same bytes rather than the same object. It lives
inside the default suite and is unconditional — it may not depend on an optional
argument, because it is what licenses every other comparison in the file.

Comparisons are counted at the comparison site (inv. 43) in a module-level
`boardCmp`. Two guards were added, both proven below: `ok('identity run compared
boards', boardCmp > before)` inside the suite, and a top-level
`if (boardCmp === 0) { … process.exit(1); }` next to the existing
`pass + fail === 0` guard.

`bench.yml` was not edited, as §2 Stage A requires: the identity run lives inside
the default suite, so step 3's invocation is unchanged and only its check count
moves.

### Stage B — the workflow, and what the run returned

`.github/workflows/calib.yml` is built to the specification exactly:

- `workflow_dispatch` **and** `push` on `branches: [ 'claude/**' ]` with the two
  specified path filters. **`main` is absent.**
- `shell: bash -euo pipefail {0}` (inv. 25), `timeout-minutes: 120`.
- `actions/setup-python@v5` at `3.12`, `pip install numpy requests`.
- `actions/cache@v4` on `path: bench/cache`, key `bench-vision-3y-v4` — the same
  key shape `backtest_bench.yml` produces for `vision` at 3 years
  (`bench-${{ inputs.source }}-${{ inputs.years }}y-v4`).
- Step 1 `--selftest`, step 2 the run tee'd into
  `bench/exhaustion-calibration.txt`, step 3 the commit-back with `[skip ci]` and
  `permissions: contents: write`, then `actions/upload-artifact@v4` with
  `if: always()`.

The push that added the file fired the workflow, as the TZ intended.

**The run produced a number, and the number is outside the registered window.**

## Test Results

### Stage B — the calibration run

Run: <https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32623034089>
Job: `calib` (97154049028). Conclusion: **failure**, and the failure is the
verdict, not a malfunction — the script exits non-zero outside the window by
design.

**Selftest green BEFORE the run** (step 6, `success`, 06:29:03):

```
=== Stage B self-test (offline) ===

--- checks: 12  fails: 0 ---
```

Step 7 ran 06:29:03 → 06:37:52 (8m49s) and exited 1.

**n, coins contributing, and the full decile table:**

```
=== Pooled distribution ===
  coins contributing : 24
  coin-days pooled n : 24384
  coins skipped      : GRAM (not in cache)

  pct         ratio
  p0         0.0887
  p10        0.4304
  p20        0.5362
  p30        0.6238
  p40        0.7126
  p50        0.8102
  p60        0.9182
  p70        1.0544
  p80        1.2441
  p90        1.5940
  p100      15.6014

  mean               : 0.9509
  median (p50)       : 0.8102
```

**p90 raw and rounded, and the window verdict:**

```
=== 90th percentile ===
  raw                : 1.593970
  rounded to 2 dp    : 1.59

=== Registered rule (inv. 23) ===
  window             : 1.60 .. 4.00 (registered before the number)
  verdict            : BLOCKED — outside the window.

DAY_RANGE_ABNORMAL is NOT adopted. Stage C makes no production
change. A threshold outside the window means the measure is not
measuring what TZ-10 claims: the answer is a new TZ, not a nudge.
```

The miss is **0.006030**, or 0.377 % below the floor. It is stated here precisely
so the Architect can see how narrow it is — and it is not acted on. A rule that
only binds when the miss is large is not a rule.

**Per-coin `n`, p90 and p50, all 24 contributing coins:**

```
    AAVE     n= 1110  p90=1.6222  p50=0.8528
    ADA      n= 1110  p90=1.6302  p50=0.8073
    ALGO     n= 1110  p90=1.6127  p50=0.8276
    AVAX     n= 1110  p90=1.6199  p50=0.8626
    BCH      n= 1110  p90=1.6681  p50=0.7894
    BNB      n= 1110  p90=1.6626  p50=0.7735
    ENA      n=  865  p90=1.4971  p50=0.8442
    ETH      n= 1110  p90=1.6706  p50=0.8470
    FET      n= 1110  p90=1.5832  p50=0.8231
    HBAR     n= 1110  p90=1.5462  p50=0.7469
    LINK     n= 1110  p90=1.6085  p50=0.8490
    NEAR     n= 1110  p90=1.5914  p50=0.8401
    ONDO     n=  491  p90=1.5369  p50=0.8236
    RENDER   n=  750  p90=1.4244  p50=0.7891
    SKY      n=  332  p90=1.5455  p50=0.8184
    SOL      n= 1110  p90=1.5982  p50=0.8517
    SUI      n= 1110  p90=1.5482  p50=0.8445
    TAO      n=  856  p90=1.4676  p50=0.8300
    TRX      n= 1110  p90=1.5345  p50=0.7579
    UNI      n= 1110  p90=1.5559  p50=0.8092
    XLM      n= 1110  p90=1.5353  p50=0.7295
    XRP      n= 1110  p90=1.6333  p50=0.7221
    YFI      n= 1110  p90=1.5970  p50=0.7683
    ZEC      n= 1110  p90=1.7004  p50=0.8222
```

Not one per-coin p90 reaches 1.75. The pooled p90 is not being dragged under the
floor by an outlier coin; the whole distribution sits there.

**The run header, universe and source availability:**

```
Universe: 25 spot of 28 declared tokens (fut:true excluded by declaration, inv. 41): HYPE, XMR, LIT
Cut out of index.html: has, sigmaDay, dayRangeRatio

Cache incomplete (0 of 25) — the archive is needed.
Source availability:
  архив data.binance.vision        200
  зеркало data-api.binance.vision  200
  боевой api.binance.com           451 — доступ закрыт по географии (раннер в США)
  боевой fapi.binance.com          451 — доступ закрыт по географии (раннер в США)
  api.coingecko.com                200
Источник: vision
```

Invariant 24 held on the runner exactly as documented: the production Binance
hosts answered 451, the archive and its mirror answered 200.

**Per-coin archive coverage, and the one gap:**

```
  GRAM    НЕТ ДАННЫХ (нет 36 месячных файлов, строк 1247)
```

Every other declared token downloaded cleanly (`дыр 0.0 %`, except `LIT` at
0.1 %). `монет в кэше: 28 из 29`.

### Stage A — before and after

**Before**, candidate compared against a byte-identical copy of itself:

```
$ cp index.html /tmp/…/baseline-identity.html
$ md5sum index.html /tmp/…/baseline-identity.html
56af2e274e5568527a6bb0e5cb4e3456  index.html
56af2e274e5568527a6bb0e5cb4e3456  /tmp/…/baseline-identity.html

$ node bench/prot_bench.js index.html /tmp/…/baseline-identity.html
FAIL: rest of board unchanged #0  [len 11982 vs 13372]
FAIL: rest of board unchanged #1  [len 13977 vs 15398]
FAIL: rest of board unchanged #2  [len 12435 vs 13857]
FAIL: rest of board unchanged #3  [len 13428 vs 14679]
FAIL: rest of board unchanged #4  [len 12207 vs 13581]
FAIL: rest of board unchanged #5  [len 6521 vs 7248]
PASS 1885   FAIL 6
```

The first-difference dump names the cause without ambiguity — in every one of the
six the candidate is missing the section the baseline still has:

```
  first diff at 9865: …<div class="bd-h">ОТКУДА ПЛЕЧО</div>…
                  ||| …<div class="bd-h">ЗАЩИТА ПОЗИЦИИ</div>…
```

**All six failures are accounted for as the removed asymmetry**, one per
scenario, and the candidate side is shorter by exactly the section length in each
case (1390, 1421, 1422, 1251, 1374, 727 bytes).

**After:**

```
$ node bench/prot_bench.js index.html /tmp/…/baseline-identity.html
identity: 6 boards compared against index.html itself
PASS 1898   FAIL 0     exit 0
```

**The identity run inside the DEFAULT suite** — the invocation `bench.yml`
actually makes, with no baseline argument:

```
$ node bench/prot_bench.js index.html
identity: 6 boards compared against index.html itself
PASS 175   FAIL 0      exit 0
```

168 → 175 is +7: six board comparisons plus the one check that asserts the
comparisons happened.

**Negative control 1 — re-plant the asymmetry, the suite must turn red:**

```
$ # one-sided strip restored inside suiteNoRegression
$ node bench/prot_bench.js index.html
PASS 169   FAIL 6      exit 1
$ # restored
$ node bench/prot_bench.js index.html
PASS 175   FAIL 0      exit 0
```

**Negative control 2 — zero comparisons must not pass** (inv. 22):

```
$ # scenarios forced empty inside suiteNoRegression
$ node bench/prot_bench.js index.html
FAIL: identity run compared boards  [0 comparisons]
identity: 0 boards compared against index.html itself
PASS 168   FAIL 1
FAIL board differ compared nothing
exit 1
```

Both guards fire, and both exit non-zero rather than printing a failure and
returning success (inv. 25, 29). The working tree was restored after each control
and verified by MD5 against the pre-control copy.

### Standing checks

```
$ node --check <script> extracted from index.html      SYNTAX OK   (178177 bytes)
$ node --check bench/prot_bench.js                     SYNTAX OK
$ python3 -m py_compile main.py                        COMPILES
$ python3 -c "yaml.safe_load(open('.github/workflows/calib.yml'))"   YAML OK
```

**ES5 guard.** 46 lines were added to `bench/prot_bench.js`; none contains `=>`,
a template literal, `let` or `const`. Zero lines were added to `index.html`, so
the ES5 floor for production is trivially intact.

**Cyrillic guard.** Zero added lines in `bench/prot_bench.js` contain raw
Cyrillic. `calib.yml` carries Cyrillic on 30 lines, every one of which is a YAML
comment or a step `name:` — none is a JavaScript string literal, so hard-floor
item 7 is not engaged.

### §5.5 No-regression, in the order the TZ specifies

**First, the differ on identity (Stage A).** Proven above: the default suite
compares `index.html` against an independent evaluation of its own bytes across
six scenarios and finds zero differences, and is proven able to report a
difference and to refuse a zero-comparison run.

**Then, whole boards through production `boardHtml`.** Driven from the recorded
journal snapshots `journal/data/2026-08-21.jsonl` and `2026-08-22.jsonl`, across
side × leverage × stress (2 sides × 4 leverages {2,3,5,7} × 3 stress states
{normal, stress, panic} × 50 coin-days), candidate against `origin/main`:

```
PART 1  candidate vs origin/main, reg.day absent
  boards compared : 1200
  bytes compared  : 16588536
  differences     : 0
```

**Then the same comparison with `reg.day` absent, present-and-false and
present-and-true**, all three against `origin/main`:

```
PART 2  reg.day absent / present-false / present-true, all vs origin/main
  boards compared : 3600
  bytes compared  : 49765608
  differences     : 0

TOTAL boards 4800   bytes 66354144   differences 0     exit 0
```

**Caveat, stated plainly.** Because Stage C was blocked, `index.html` is
byte-identical to `origin/main`, so Part 1 could not have differed and is a
control on the harness rather than on a change. Part 2 is not vacuous in the same
way: it attaches `reg.day` to `lastRegime` in all three shapes and shows the
board indifferent to it, which is the inertness claim TZ-10 made and which still
holds. Neither part is evidence about a Stage C that was not written.

### §5.6 Replay of the two journaled days

Re-measured through the extracted production functions — `listExhaustion`,
`dayRangeRatio` and `sigmaDay` cut out of `index.html` at run time, no formula
reimplemented (inv. 21):

| Date | rows read | contributing `n` | median | `abnormal` | fires? |
|---|---|---|---|---|---|
| 2026-08-21 | 25 | 25 | **1.6878** | `false` | **no constant exists to fire against** |
| 2026-08-22 | 25 | 25 | **2.4298** | `false` | **no constant exists to fire against** |

`abnormal` is `false` on both dates because production still hardcodes it: Stage C
was not implemented, so `DAY_RANGE_ABNORMAL` does not exist in `index.html`. The
only occurrence of the identifier in the file is the TZ-10 comment at line 1286
explaining that the comparison arrives in Stage C.

These reproduce the System Map's stated 1.69 and 2.43 to the printed precision.

The venue declaration was read from production's own `tokens[]`, never from the
journal (inv. 41): `HYPE, LIT, XMR`, 3 of 28. The journal records only the 25
spot assets, so no `fut:true` row was present to exclude.

This is a **measurement**, counted separately from the check total (inv. 43).

### §5.8 Full gate, 12 steps

Replayed locally in `bench.yml` order. **Every step exits 0.**

| # | Bench | Baseline | Candidate | Δ |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 |
| 3 | `prot_bench.js` | 168 | **175** | **+7** |
| 4 | `verify_bench.py` | 35 | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 188 577 | 188 577 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 |
| 7 | `journal_bench.js` | 694 030 | 694 030 | 0 |
| 8 | `catalyst_bench.js` | 23 040 | 23 040 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 15 925 | 15 925 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | 220 199 | 220 199 | 0 |
| | **TOTAL** | **1 185 864** | **1 185 871** | **+7** |

The baseline column was measured against a `git worktree` at `origin/main`, not
assumed. It reproduces the TZ's stated **1 185 864** exactly, which is what
licenses the delta.

**Term by term:** the entire +7 is step 3, and it is the identity run — six board
comparisons (one per existing scenario) plus one check asserting that those
comparisons happened. Step 12 did **not** move, because Stage D was blocked and
`bench/exhaustion_bench.js` is unchanged. The TZ states that steps 3 and 12 are
the only ones whose counts may move and that any other movement is a finding: no
other step moved.

### §5.9 Extremes

Unchanged and still green inside step 12 on the untouched
`bench/exhaustion_bench.js`: the `unknown` banner state with `reg.day` attached
is covered by its section E, which drives all five modes × `isLong` ×
`{abnormal true, abnormal false, below-quorum null}` and requires the banner
byte-identical throughout. Truncated Gist, HTTP 400 ticker, dead-market fields,
missing coeffs fields and absent `btcStats` are covered by steps 1, 2, 3, 6, 9
and 10, all of which are green and none of which moved.

## Validation

Item-by-item against §5, with no item marked "not applicable":

| # | Item | Result |
|---|---|---|
| 1 | `node --check`, `py_compile`, ES5 and Cyrillic guards | **PASS** |
| 2 | Stage A identity green in the default suite; six failures accounted for; before/after quoted; negative control red | **PASS** |
| 3 | Stage B run linked; selftest green before the run; `n`, coins, decile table, per-coin figures, p90 raw and rounded, window verdict | **PASS** |
| 4 | Stage C banner matrix, threshold edge, `fut:true` exclusion, quorum, purity | **BLOCKED** — the code under test was not written |
| 5 | No-regression, identity first | **PASS**, with the caveat above |
| 6 | Replay of both journaled dates | **PASS** |
| 7 | Stage D negative control (one-digit change turns the record section red) | **BLOCKED** — the section was not written |
| 8 | Full gate green, 12 steps, delta explained term by term | **PASS** |
| 9 | Extremes | **PASS** |

Items 4 and 7 are blocked by the TZ's own gating rule, not by an inability to run
them. They are recorded as blocked rather than failed, and the distinction is
load-bearing: the work was authorised only on condition of a number the run did
not produce.

## Deviations

**1. Stages C and D were not implemented.** Required by TZ-11 §2 Stage B: the
pooled p90 rounded to 1.59, below the 1.60 floor, so the stages are BLOCKED on
the merits. This is compliance with the TZ, not a departure from it, and it is listed here because the TZ's `## Files` table names `index.html`
and `bench/exhaustion_bench.js` as files to change and neither was changed.

The Stage C and D edits were fully drafted before the run returned — the constant
site, the `>=` comparison, the `fut:true` skip, the three row fields, the single
`update()` call site, the banner clause and `var(--orange)` override, and the
Stage D sections including the constant-against-record comparison. All of it was
**discarded** when the verdict came back, and `bench/exhaustion_bench.js` was
restored to `origin/main` and re-verified by `node --check` and by a green step 12
at its unchanged count of 220 199. None of it reached a commit.

**2. `bench/exhaustion-calibration.txt` is not in the repository.** The TZ's
`## Files` table lists it as "new, written by the workflow, committed once", and
the workflow's step 3 was **skipped** because step 2 exited non-zero under
`bash -euo pipefail`. The workflow is built exactly as specified: the TZ places
`if: always()` on the artifact upload and **not** on the commit step, so a run
that fails its own window check uploads the record but does not commit it.

I did not hand-commit the file, for three reasons: the TZ assigns it to the
workflow, not to the Executor; inv. 46 pins a constant to a record and there is no
constant to pin, so the file would pin nothing while looking authoritative; and a
committed record for a number nobody adopted is exactly the kind of artifact that
misleads a later reader. The full run output is quoted verbatim in this report,
which is permanent and immutable, and the artifact is retained on the run:
**artifact ID 9489029230**, `exhaustion-calibration.zip`, 1806 bytes, SHA-256
`1b33c9b93f41f84f5b6e030c7240e1a932ae9829408b36c20ecd30dfd6edaadb`, at
<https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32623034089>. If the
Architect wants the file committed regardless of the verdict, that is a one-line
change to `calib.yml` (`if: always()` on the commit step) and belongs in the next
TZ.

**3. `bench/exhaustion_bench.js` gained an optional baseline argument — reverted.**
While Stage D was being drafted, the file was given a `process.argv[2]` baseline
in the pattern `prot_bench.js` already uses, so the abnormal-false banners could
be required byte-identical to `origin/main` as §5.4 asks. That change went out
with the rest of Stage D. It is mentioned only so the Architect knows the §5.4
byte-identity requirement had a concrete mechanism, should the next TZ want it.

## Pre-existing Issues

**1. The calibration universe was 24 coins, not the 25 the estimator covers.**
`GRAM` has no usable archive history — `НЕТ ДАННЫХ (нет 36 месячных файлов,
строк 1247)` — and the run reports `coins skipped : GRAM (not in cache)`.

System Map §3.16 states: *"The estimator and its calibration must share a
universe… Coverage is 25 of 28 by declaration (inv. 41)."* The live estimator
covers 25 spot assets; this calibration measured 24. `GRAM` is not a marginal
member: it reads consistently at the bottom of the live list — on 2026-08-22 the
**lowest of all 25** (1.3385), and on 2026-08-21 the fourth lowest (1.0898,
against a list minimum of 0.8351 for `TRX`). Dropping it raises the list median
on both days (1.6878 → 1.7011 and 2.4298 → 2.4360), so a low-reading coin being
absent biases the pooled statistic **upward**: the true 25-coin p90 is more
likely at or below the 1.5940 measured than above it — further from the floor,
not nearer it. That direction matters, because it means the missing coin cannot
be the reason the number fell short. Pre-existing: it is a property of the archive and
of `exhaustion_calib.py`'s cache handling, not of anything TZ-11 changed. Not
fixed, per §6 and §12.

**2. The measured distribution contradicts the System Map's construction claim.**
§3.16 states: *"σ is close-based and therefore understates true range, so the
reading is above 1 by construction."* The pooled distribution says otherwise:

| statistic | measured |
|---|---|
| p50 | **0.8102** |
| mean | 0.9509 |
| p60 | 0.9182 |
| p70 | 1.0544 |

The median coin-day reads **0.81**, and only somewhere between p60 and p70 does
the distribution cross 1. Roughly two coin-days in three read *below* 1, not
above it. Every one of the 24 per-coin p50 values lies between 0.7221 and 0.8626 —
this is not an artefact of pooling.

This matters directly to the blocked stages: the window `1.60 … 4.00` was
registered on the premise that typical readings sit above 1, and the p90 missing
the floor by 0.006 is the visible symptom of that premise not holding. The two
journaled days measured **1.6878** and **2.4298** on the live path, i.e. around
the archive distribution's own p90–p95 — the live readings and the archive
readings do not look like samples from one distribution.

A plausible mechanism, offered as a lead and **not** as a finding I have
established: the live path takes `volatility` from `coeffs.json` as the bot
publishes it, while the calibration takes it from `backtest_bench.CdBuilder`
reconstructing the same metric from archive candles. If those two differ
systematically in scale, the ratio's denominator differs with them, and the
estimator calibrated is not quite the estimator running. Resolving that is
outside TZ-11's scope and is reported, not acted on.

**3. The Actions cache was cold.** `Cache not found for input keys:
bench-vision-3y-v4`, and the run reported `Cache incomplete (0 of 25) — the
archive is needed`, so it downloaded three years of history rather than reusing a
warm backtest cache. The key shape is the one the TZ specifies and matches
`backtest_bench.yml` exactly; no cache under that key existed to restore, which
is a property of the repository's cache state, not of `calib.yml`. Cost was
8m49s, well inside `timeout-minutes: 120`. No action taken.

**4. Node 20 deprecation warnings on both runners.** `actions/cache@v4`,
`actions/checkout@v4`, `actions/setup-python@v5` and `actions/upload-artifact@v4`
are being forced onto Node 24. The TZ names this a known, queued item and puts
`bench.yml` out of scope; `calib.yml` inherits the same warning from the same
actions. Reported only.

## Remaining Risks

**1. The banner still says the wrong thing.** The condition TZ-11 exists to close
is unchanged: on a session like 2026-08-22 the banner reads
`«ТРЕНД ВВЕРХ — счёт по каналу импульса»` in green while the list median
day-range is 2.43 and geometry refuses 24 of 25 coins. The measure exists and reaches nothing. That is the state
TZ-10 left and the state this TZ leaves, and it is the cost of not nudging the
number.

**2. A re-run at a different depth would produce a different number, and must not
be used to obtain one.** TZ-11 §3 names this a non-goal explicitly: *"The
calibration is not re-run at a different `--years` to see whether the number
moves."* It was not re-run. A single run at `--years 3 --source vision` is the
whole of the evidence, deliberately.

**3. `calib.yml`'s push trigger has now fired and will not fire again on this
branch.** The path filter covers `bench/exhaustion_calib.py` and
`.github/workflows/calib.yml`; neither will change again on this branch. Once the
workflow is on `main`, `workflow_dispatch` becomes available and the instrument
can be re-run on demand — which is the mechanism the next TZ will want.

**4. The differ repair changes what a future failure means.** `suiteNoRegression`
now compares the whole board, so a future change that legitimately alters the
protection section will show up as six failures against a stale baseline. That is
correct behaviour and the intended one, but it is a different signal from what a
reader of the old code would expect.

## Commit

```
3fcdddc  fix(bench): symmetric board differ + identity run; add calibration workflow (TZ-11 A/B)
```

Branch: `claude/execute-tz-11-paxmuo`, pushed to `origin`. One commit, containing
Stage A and Stage B and nothing else. The tree is clean; no scratch file,
`__pycache__` or bench bridge artifact was committed.

## Pull Request

**<https://github.com/seahomebatumi-ai/crypto-auto/pull/11>** — PR **#11**,
`claude/execute-tz-11-paxmuo` → `main`. Open, **not merged**, awaiting the
Architect's verdict.

## CI Execution

Both workflows executed **on GitHub runners**, not locally.

| Workflow | Run | Trigger | Conclusion |
|---|---|---|---|
| `Bench gate` | [32623034066](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32623034066) | push to `claude/**` | **success** |
| `Calibration (archive)` | [32623034089](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32623034089) | push to `claude/**` | **failure — the window verdict, by design** |

`Bench gate` run 54 went green on commit `3fcdddc` with all twelve bench steps
succeeding, including step 3 `prot_bench.js` at its new count. That is the
runner-side proof for Stage A; the per-step counts in §5.8 above are from the
local replay, and the two are distinguished deliberately.

`Calibration (archive)` reports `failure` because `exhaustion_calib.py` exits
non-zero when the number lands outside the registered window. The job is not
broken: steps 1–6 all succeeded, the selftest was green, the run completed and
printed its full table, and only the window check failed it. Step 8 (the
commit-back) shows `skipped` as a consequence; step 9 (upload) shows `success`.

`main.yml` and `journal.yml` did not run: neither is triggered by a push to a
`claude/**` branch, and nothing in this change touches the bot or the journal.

## Final Repository State

- `main` carries this report only. No implementation reached `main`.
- `claude/execute-tz-11-paxmuo` carries `3fcdddc`: `calib.yml` and the
  `prot_bench.js` repair.
- `index.html`, `main.py`, `catalysts.json`, `bench/exhaustion_bench.js`,
  `bench.yml`, `backtest_bench.yml` and `journal/**` are byte-identical to
  `origin/main`.
- PR #11 is open.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1086 | `bebaae536c3a71e9315ece12f643224c` |
| `index.html` | 3569 | `56af2e274e5568527a6bb0e5cb4e3456` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |

System Map revision string, from its `## 0. Fingerprint` block:
**`Revision 2026-08-23-a.`**

All four match the map's own declared values and the TZ-11 baseline. `index.html`
is unchanged from `origin/main` because Stage C was blocked.
