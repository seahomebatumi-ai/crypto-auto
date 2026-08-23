# TZ-11 — Exhaustion threshold: calibrate on a runner, wire one consumer

**Canonical filename: `TZ-11-exhaustion-threshold.md`.** The Executor commits the
file under exactly this name, taken from this line and never from the name the
file arrived with.

**Model: Opus.** A workflow, a repaired control, a production constant derived
from a measurement, and the colour of the single list-wide element on screen. A
wrong number here is a permanent, silent mis-statement on the loudest thing the
Boss sees.

## Fingerprint gate

Compare against the repository copy of `SYSTEM-MAP-CRYPTOCALCUL.md` BEFORE any
work. Any mismatch → **ЗАБЛОКИРОВАНО**, report and stop.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-23-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| newest invariant | `46. **A calibrated constant is checked against its calibration record.**` |

Baseline: TZ-10 merged (PR #10, `baa9d9b`). `index.html` 3569 lines, MD5
`56af2e274e5568527a6bb0e5cb4e3456`.

**A fresh session clone has been observed with a local `main` that is not
`origin/main`.** Run `git fetch --all --prune` first and take every baseline
comparison from `origin/main`, never from local `main`.

---

## 1. What this closes

TZ-10 delivered the measure and, correctly, refused to invent the number that
makes it act. `DAY_RANGE_ABNORMAL` does not exist because Stage B was specified
as a session run, and a session reaches no archive host — the constraint is now
inv. 44. The instrument is complete, self-tested and negative-controlled; it has
never fetched a byte.

Consequence today: on a session like 2026-08-22 the banner still reads
«ТРЕНД ВВЕРХ — счёт по каналу импульса» in green while the list median day-range
is 2.43 times a diffusive day and geometry refuses 24 of 25 coins.

This TZ moves the fetch to where fetches happen, adopts the number the run
produces under the rule already registered, wires exactly one consumer, and pins
the constant to its own record so it can never be moved quietly afterwards.

Nothing predictive is added. No ranking factor, no weight, no leverage effect.

---

## 2. Scope — four stages

Stages A and B are independent of each other. C depends on B. D depends on C.
**A blocked B does not block A.**

### Stage A — repair the baseline differ

`bench/prot_bench.js`, `suiteNoRegression`. The suite strips the
«ЗАЩИТА ПОЗИЦИИ» section from the **candidate** only. That was correct when the
baseline predated the section; both revisions carry it now, so the comparison
differs by exactly that section and reports six failures against a
**byte-identical** baseline.

1. Make the transformation symmetric: whatever is stripped from one side is
   stripped from the other, or from neither. Prefer neither — the section exists
   on both sides and there is nothing left to compensate for.
2. Add an **identity run to the DEFAULT suite**, the one `bench.yml` invokes
   with no baseline argument: compare `index.html` against itself through the
   same differ and require zero differences. Counted at the comparison site
   (inv. 43), non-zero exit on any difference, non-zero exit on zero comparisons
   (inv. 22).

**This is not editing a bench to make it pass.** Six failures against a file
compared with itself are a stale expectation, and the repair removes the
asymmetry, not the assertion. The identity run is what makes the differ usable as
evidence at all (inv. 45), and Stage C's no-regression proof needs it.

`bench.yml` is not edited: the identity run lives inside the default suite, so
step 3's invocation is unchanged and only its check count moves.

### Stage B — run the calibration where the archive answers

Add `.github/workflows/calib.yml`.

```
name: Calibration (archive)
on:
  workflow_dispatch:
  push:
    branches: [ 'claude/**' ]
    paths:
      - 'bench/exhaustion_calib.py'
      - '.github/workflows/calib.yml'
```

- **Never `main`.** This is a one-shot instrument, not a control; it is
  deliberately absent from `bench.yml` and must not run on every push.
- **The `push` trigger is load-bearing.** A `workflow_dispatch`-only workflow is
  not dispatchable until it sits on the default branch, so a dispatch-only file
  could only run after the merge it is supposed to precede. The path filter means
  it fires on the push that adds it and on no later push to the same branch.
- `shell: bash -euo pipefail {0}` (inv. 25). `timeout-minutes: 120`.
- `actions/setup-python@v5` with `python-version: "3.12"`; `pip install numpy
  requests`; `actions/cache@v4` on `path: bench/cache` with the **same key shape
  `backtest_bench.yml` already uses for `vision` at 3 years**, so a warm backtest
  cache is reused instead of re-downloaded.
- Step 1: `python bench/exhaustion_calib.py --selftest` — offline wiring proof
  first. A red selftest fails the job; a number produced after a red selftest is
  not evidence (inv. 23).
- Step 2: `python3 bench/exhaustion_calib.py --years 3 --source vision 2>&1 |
  tee bench/exhaustion-calibration.txt`.
- Step 3: commit `bench/exhaustion-calibration.txt` back to the same branch with
  `[skip ci]` in the message (`permissions: contents: write`). Also upload it with
  `actions/upload-artifact@v4`, `if: always()`.

The committed file is the calibration record required by inv. 46. It is written
once and never reopened.

**The Executor must `git pull --rebase` the branch after the run** before pushing
Stage C, or the push is rejected against the workflow's own commit.

**The registered rule is unchanged and is restated here only so it cannot be
looked up wrongly (inv. 23):**

> `DAY_RANGE_ABNORMAL` = the pooled 90th percentile printed by the run, rounded
> to two decimals, taken as-is. Not moved to make 2026-08-22 fire, not moved to
> make any other date fire or not fire, never retuned afterwards. Below **1.60**
> or above **4.00**, Stages C and D are **ЗАБЛОКИРОВАНО** on the merits: no
> production change, the full decile table in the report, and the answer is a new
> TZ. The script enforces the window itself and exits non-zero outside it.

### Stage C — adopt the constant, wire exactly one consumer

1. Add `DAY_RANGE_ABNORMAL <value>` to the constants block — the single site
   (inv. 20).

2. `listExhaustion`:
   - `abnormal = (median !== null) && (median >= DAY_RANGE_ABNORMAL)`. **`>=`,
     so equality fires** — stated here so it cannot drift.
   - **Skip `fut:true` rows** (`row.t && row.t.fut`). The three perpetual-only
     assets read their range off the futures ticker while `volatility` comes from
     a spot index (§3.14 Consequence 3), so including them would make the live
     estimator a different estimator from the one the threshold was measured on.
     Exclusion is by DECLARATION, never by observation (inv. 41). Coverage is 25
     of 28, the same coverage as the journal and as the calibration.

3. `update()`:
   - Inside the existing `if (sideOn)` block, where `curP`, `hi24` and `lo24` are
     already parsed, attach them to the row: `row.cur`, `row.hi24`, `row.lo24`.
     **No second `parseFloat` of the same string** (inv. 20).
   - After row assembly and before `regimeBanner` is called: `reg.day =
     listExhaustion(rows);` — **once per render**, not per card.
   - `marketRegime` is not modified.

   **TZ-10 report Deviation 4 is resolved: the implemented reading stands.**
   `listExhaustion` reads row fields and does not re-parse ticker strings. It
   keeps the function pure and callable from fixtures, and `update()` already
   holds the parsed numbers.

4. `regimeBanner(reg, isLong)` stays a pure namer and **computes nothing**. When
   `reg.day && reg.day.abnormal`:
   - append to the existing text:
     `' \u00B7 \u0414\u0415\u041D\u042C \u0410\u041D\u041E\u041C\u0410\u041B\u042C\u041D\u042B\u0419 \u2014 \u0432\u0445\u043E\u0434 \u0442\u043E\u043B\u044C\u043A\u043E \u043F\u043E \u043E\u0442\u043A\u0430\u0442\u0443'`
   - set the colour to **`var(--orange)`** in the `unknown`, `range` and both
     `trend` branches, overriding green and `var(--accent)`.
     **`--orange` is already declared in `:root` as the ЖДАТЬ entry-state colour**,
     and «вход только по откату» is exactly that state at list level. TZ-10 named
     a raw `#e0a02a`; that is **overruled** — a new hex would be a second colour
     carrying an existing meaning (inv. 20, inv. 33).
   - In the `stress` branch the clause is appended and the colour stays
     `var(--red)`. Stress is the stronger statement and red belongs to it alone.

5. **Nothing else consumes it.** Not `scoreCandidate`, `tradeGeometry`,
   `leverageDecision`, `directionVerdict`, `boardHtml`, or the journal writer.
   `lastRegime` is the same object as `reg` and therefore gains `.day`; that must
   be proved inert, not assumed.

Russian on-screen strings are written as `\uXXXX` escapes. ES5 only.

### Stage D — pin the constant to its record, finish the bench

`bench/exhaustion_bench.js`:

1. **New section: constant against record (inv. 46).** Read `DAY_RANGE_ABNORMAL`
   out of `index.html` and the `DAY_RANGE_ABNORMAL = X.XX` line out of
   `bench/exhaustion-calibration.txt`; they must be equal to the printed
   precision. A missing constant, a missing record, an unparseable line or a
   mismatch each fail the bench non-zero. Counted at the comparison site.
2. Write the two cases TZ-10 left out because the code did not exist: the
   **threshold edge** (`median === DAY_RANGE_ABNORMAL` fires) and the eight
   **`abnormal === true`** banner cases.
3. **Section E inverts, it is not deleted.** It asserted inertness; it now
   asserts that the measure reaches exactly one consumer and no other —
   `regimeBanner` changes with `reg.day`, and `scoreCandidate`, `tradeGeometry`,
   `leverageDecision`, `directionVerdict` and `boardHtml` do not. Deleting it
   would make the inversion look like a regression.
4. The assertion that `#e0a02a` is absent from `index.html` is stale — replace it
   with the `var(--orange)` assertion on the abnormal branches.
5. Section C gains two exclusion cases: a `fut:true` row contributes nothing even
   with a valid ratio, and a row whose `cd.error` is true contributes nothing.

---

## 3. Non-goals — do not implement, do not propose in the report

Everything TZ-10 §3 lists remains a non-goal, unchanged. In addition:

- No edit to `bench.yml` — not its step list, not its invocations, not the Node
  pin. The Node 20 deprecation is a known, queued item and its validation is a
  full gate re-run of its own.
- No second threshold, no per-coin exhaustion badge, no new card row, no new
  board block, no new `wait` state, no change to `ENTRY_CHASE_SD`.
- No effect on any leverage ceiling, on the score, on ranking or on the
  invalidation level.
- No journal schema change. `px.hi`, `px.lo`, `px.cur` and `cd.volatility` are
  already recorded, so every journaled day stays reconstructible.
- The calibration is not re-run at a different `--years` to see whether the
  number moves.
- `backtest_bench.yml` is not edited.

---

## 4. Files

| File | Change |
|---|---|
| `bench/prot_bench.js` | symmetric strip + identity run in the default suite |
| `.github/workflows/calib.yml` | new |
| `bench/exhaustion-calibration.txt` | new, written by the workflow, committed once |
| `index.html` | one constant, `listExhaustion` threshold + `fut:true` skip, three row fields and one call site in `update()`, `regimeBanner` text and colour |
| `bench/exhaustion_bench.js` | constant-vs-record section, the two omitted cases, section E inverted, `--orange`, two exclusion cases |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | Architect-authored, delivered separately — the Executor does not edit the map |

No change to `main.py`, `catalysts.json`, `journal/**`, `bench.yml`,
`backtest_bench.yml`.

---

## 5. Validation — written by the Architect

The Executor runs these and does not design them.

1. `node --check` on the extracted `<script>` and on every edited bench;
   `python3 -m py_compile main.py`. ES5 guard and Cyrillic guard on added lines.

2. **Stage A.** The identity run green inside the default suite. The six historical
   failures accounted for as the removed asymmetry, with a before/after run
   quoted. Negative control: re-plant the asymmetry and the suite must turn red.

3. **Stage B.** The runner run linked by URL and number. Selftest green **before**
   the run. Report states `n`, coins contributing, the full decile table, per-coin
   `n`/p50/p90, p90 raw and rounded, and the window verdict. The committed
   `bench/exhaustion-calibration.txt` is quoted, not paraphrased.

4. **Stage C**, all inside `bench/exhaustion_bench.js`:
   - **Banner:** every `mode` (`unknown`, `stress`, `trend` up, `trend` down,
     `range`) × `abnormal` true/false × `isLong` true/false. The clause is present
     **iff** `abnormal`; colour is `var(--orange)` in `unknown`/`range`/`trend`
     when abnormal, `var(--red)` in `stress` regardless, and **byte-identical to
     `origin/main`** in every `abnormal === false` case.
   - **Threshold edge:** `median === DAY_RANGE_ABNORMAL` fires; one ulp below does
     not.
   - **`fut:true` exclusion:** a 28-row list whose three perpetual rows carry
     deliberately extreme ratios must produce the SAME median and the SAME `n` as
     the 25 spot rows alone.
   - **Quorum unchanged:** `n < 8` → `median === null`, `abnormal === false`,
     regardless of the values present.
   - **Purity:** `regimeBanner` called twice on the same frozen `reg` returns an
     identical string and does not mutate `reg`.

5. **No-regression, in this order.** First prove the differ on identity (Stage A).
   Then, with `abnormal` forced false, drive whole boards through production
   `boardHtml` from the recorded journal snapshots across side × leverage ×
   stress and require **byte-identical** output against `origin/main`. Then the
   same comparison with `reg.day` absent, present-and-false, and
   present-and-true — the board must be identical in all three, because
   `lastRegime` now carries `.day`. State bytes compared and boards compared.

6. **Replay.** Re-measure `journal/data/2026-08-21.jsonl` and
   `2026-08-22.jsonl` through the extracted production functions and state, for
   each date, the median and whether it fires under the adopted constant. A
   measurement, counted separately from the check total (inv. 43).

7. **Stage D negative control.** Change `DAY_RANGE_ABNORMAL` in `index.html` by
   one digit: the constant-vs-record section must turn red. Restore.

8. **Full gate green, 12 steps**, the new total stated as a sum of per-comparison
   counters with the delta against **1 185 864** explained term by term (inv. 43).
   Steps 3 and 12 are the only ones whose counts may move; any other movement is a
   finding.

9. Extremes, unchanged obligations: truncated Gist, HTTP 400 ticker, dead-market
   fields, missing coeffs fields, `btcStats` absent — the `unknown` banner state
   with `reg.day` attached is inside the case matrix above.

---

## 6. Report

`CryptoReports/TZ-11-exhaustion-threshold-report.md`, straight to `main`, stating:

- line counts and MD5 for `index.html`, `main.py`, `catalysts.json` and the
  System Map;
- the Stage B decile table, `n`, p90 raw and rounded, and the window verdict;
- the two replay medians and whether each fires;
- the gate total with the term-by-term delta;
- the no-regression evidence of §5.5, with the identity proof stated first.

**Open the pull request from the branch to `main` and state its number in the
report.** Implementation waits on the branch; the pull request is not merged
before the Architect's verdict.
