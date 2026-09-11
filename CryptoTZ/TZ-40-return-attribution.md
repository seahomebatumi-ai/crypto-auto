# TZ-40 — Return-discrepancy attribution: end instant, start instant, residual

**Canonical filename: `TZ-40-return-attribution.md`.** Name the committed file from this
line, never from the name it arrived under (contract §3).

**Model: Opus.** New measurement instrument with math risk across two files.

**Sequencing: TZ-39 is merged before this TZ starts.** Both TZs edit the same two benches,
so a branch cut before that merge produces work that is complete and live nowhere
(contract §8). Check it and say so at the top of your report.

---

## 0. Fingerprint gate — blocking, before any work

Required map revision, matched as an exact substring against the repository copy
(contract §5):

**Revision 2026-09-10-a.**

The map does not move for TZ-39: both TZs execute against this revision, as TZ-34 and TZ-35
did against `2026-09-08-b`.

Content anchors — all seven, each matched as an EXACT substring. **Report the matched
substring, not the verdict** (§10).

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-10-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` |

The map's `## 0` file table — measure each at the stated line count and MD5; a difference
is reported under `## Pre-existing Issues` and is **not acted on** (contract §5):

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**The two bench figures below are the map's at this revision, taken BEFORE TZ-39.** TZ-39
moves both files, so they will differ when you measure them: report the measured figures
and **do not block on the difference** — benches are absent from the enforced table by
decision (map §0), and the gate enforces the anchors and the revision string only.

| File | Lines at 2026-09-10-a, pre-TZ-39 | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4555 | `deac9dd8a53f2047c25c2d6fb24f09b4` |
| `bench/backtest_guard_bench.py` | 1726 | `ce08dd99edebfa90d8fce3dd6b7ba472` |

Contract in force: **v20**, 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0`.
Gate at 2026-09-10-a: `bench.yml`, 14 steps, **1 335 964** checks; step 14 = **323**,
step 4 = **40**. TZ-39 moves step 14 and the total; your baseline is what you measure.

---

## 1. Why

The reconciliation of 09.09.2026 refused eighteen of thirty coins on 35 cells, and every
cell is in the return family — `r7`, `r14`, `r30`, `eff14` — with not one a level and not
one a volatility. Across the 25 spot coins the levels agree to **0.47 %** worst against a
2 % bar and `volatility` to 2.4 % against 10 %, while the returns miss by up to
**+5.15 pp** with a POSITIVE sign on 24 of 25. `eff14` is `r14` divided by the same coin's
`volatility·√336` and reproduces it cell by cell, so this is **one quantity at four
horizons**, not four findings. The time gap was 0.8 h, inside the comparison window, so the
returns were compared at all; a larger gap would have skipped them and hidden this entirely.

`unexplained` is «everything else» and names no cause. A systematic sign is not noise. This
TZ builds the instrument that ATTRIBUTES the gap and takes no position on what it will say.

**Nothing in this TZ names a cause, and nothing you write may** — not the code, not its
printed output, not `## Implementation Summary`. The terms are reported; the Architect
reads them.

---

## 2. Scope

**Files to Modify:** `bench/backtest_bench.py`, `bench/backtest_guard_bench.py`,
`.github/workflows/backtest_bench.yml`.
**Files to Create:** none. **Files to Delete:** none.

**This TZ names `.github/workflows/backtest_bench.yml` explicitly, which is the
authorisation hard floor item 8 requires.** Nothing else in that file is touched.

### `## Touches`

- `bench/backtest_guard_bench.py` — gate step 14 holds this instrument's offline control.
- `bench/verify_bench.py` — it imports `backtest_bench.py` at scope (map §0), so a change
  here can turn gate step 4 red. Named because omitting exactly this file from a `Touches`
  list cost TZ-34 an extra specification (§10). Run it; do not edit it.

---

## 3. What is measured

All terms are measured on the archive the bench already holds. Definitions first, so that
no term is named without the computation that produces it (inv. 58).

- **`f`** — production's own return computation: the block the bench already cuts by AST
  from `get_token_betas` in `main.py` (map §3.10). It is **CALLED**. A second implementation
  of any formula is banned in any language and any file (inv. 21, inv. 38).
- **`r_prod`** — the published value, obtained through the same acquisition path `--verify`
  uses. Never a second path, and never read out of a file another mode wrote: a control
  whose answer depends on step order is not a control (inv. 62, map §3.10).
- **`r_arch = f(A)`** — the baseline on the archive as held; what the reconciliation
  already compares.
- **`Δ = r_prod − r_arch`**, in the measure `--verify` already applies to this field class
  (`pp` for returns), obtained by CALLING that comparison site rather than restating it.
- **`g`** — the gap between production's window end and the archive's last hour, derived at
  the site `--verify` already derives it. Never typed as a numeral anywhere in this work.

**The three terms, per coin per return field:**

| Term | Computation | What it is |
|---|---|---|
| `T_end` | `f` re-executed on `A` truncated so the window ENDS at production's end instant, minus `r_arch` | what the end instant alone can produce |
| `T_start` | `f` re-executed on `A` with the window START moved by the same offset, end left at the baseline's, minus `r_arch` | what the start instant alone can produce |
| `T_resid` | `Δ − T_end − T_start` | what remains once both instants are aligned: the two series disagreeing about PRICE rather than about TIME |

`T_resid` is reported as a residual and attributed to nothing.

**Two quantities reported beside them, because they name the same instants:**

- **`d_end`** — the end-level deviation, i.e. the `cur` cell the reconciliation already
  measures for that coin. It agrees to 0.47 % worst across the spot set, and it is the one
  end-of-window fact already in hand.
- **`d_start_implied`** — for a two-point return, `log(1+r) = log P(end) − log P(start)`, so
  the residual is exactly a start-instant level deviation. Report it per cell, **together
  with the archive's own sensitivity at that instant**: `|log A(t₀+h) − log A(t₀)|` over the
  registered ladder `h ∈ {1, 2, 3, 6, 12, 24}` hours plus the measured `g`. The ladder
  LOCATES and never judges — no rung is a bar, no rung is named by the size of any observed
  term, and the rungs are registered here before the data (inv. 23, inv. 49, inv. 61).

**`d_start_implied` rests on `f` being two-point, and that is DERIVED at run time, never
assumed by this TZ.** Execute `f` on the archive, then on an archive perturbed only at an
interior hour, and record whether the return moved. If it moved, the interior matters:
report `d_start_implied` as not applicable for that field and put the measured interior
sensitivity in its place. The derivation is a named function so the guard can call it
(§5 W6). An author who wrote «it is two-point» here would be asserting a property of
production he did not measure — the failure inv. 61 names.

**`eff14` is not decomposed separately.** Assert, cell by cell, that it reproduces from the
decomposed `r14` and the measured `volatility` deviation. That assertion IS the check that
the four horizons are one quantity; §7 measured the ratio to within 2 % on sixteen cells,
3 % on nineteen and 11 % on all twenty-three, and the instrument re-derives it rather than
inheriting it.

---

## 4. Population — both classes, never the failures alone

- **Every coin with a cached archive**, passing and failing both, **both populations
  non-zero** (inv. 22). A term that reads the same on a passing coin as on a failing one
  explains nothing, and a set restricted to the eighteen cannot show that.
- **The five `fut:true` assets are reported separately as reference** and never pooled with
  the spot population: their cells carry the `venue-basis` licence (map §3.14, §7).
- **TRX is reported in absolute pp, not only against its threshold.** It is the one spot
  coin whose return cells all pass while its returns over every window are themselves near
  zero (§7), so a small deviation there may be a small numerator rather than a small
  mechanism. Print its terms in the same units as the failing population's and let the
  reader compare them.

---

## 5. Where it runs

**A new mode `--attrib` on `bench/backtest_bench.py`.** The name is decided here; do not
rename it.

- **Exit code.** `--attrib` is a MEASUREMENT, not a control. It exits non-zero on an
  internal failure and on **zero cells compared** (inv. 22), and **never on the size of what
  it measured**. A mode that failed on its own finding would be a bar written before the
  data (inv. 49).
- **It reads only `bench/cache/` and production's output through `--verify`'s own
  acquisition path**, and no artifact another step wrote (inv. 62).
- **It does not apply `--verify`'s comparison-window skip.** It attributes every cell and
  PRINTS `g` per coin. The skip decides whether a comparison is admissible; a gap large
  enough to skip the cell is exactly the case where this mechanism would otherwise be
  invisible (§10).
- **A workflow step** in `.github/workflows/backtest_bench.yml`, after the existing
  `--verify` step, under `shell: bash -euo pipefail` as the other steps run (inv. 25). No
  `continue-on-error` (hard floor item 12). Nothing else in that file changes.

**The offline control is a new section in `bench/backtest_guard_bench.py`** — gate step 14,
so the instrument cannot rot between dispatches the way a dispatch-only control does
(inv. 62). **Its letter is read FROM THE FILE and never by counting**: two sections already
share `E` (§10). Name the letter and why in the report.

Known-answer worlds, built by construction, each asserting what a constructed disagreement
must produce (inv. 23, inv. 45). Every assertion is counted at the comparison site (inv. 43).

| World | Construction | Must read |
|---|---|---|
| W1 | the two series identical | every term zero — **then plant a difference and show the instrument sees it**, with the count it saw (inv. 45) |
| W2 | differ only in where the window ENDS | `T_end` carries Δ; `T_start` and `T_resid` zero |
| W3 | differ only in where the window STARTS | `T_start` carries Δ; `T_end` and `T_resid` zero |
| W4 | identical instants, one series scaled | both instant terms zero; `T_resid` carries Δ |
| W5 | empty cache | non-zero exit, no result printed (inv. 22) |
| W6 | the §3 derivation called with a two-point and a path-dependent callable | it answers correctly on each |

**Tolerances are derived from each world's own construction, never chosen.** Where exact
equality is achievable in the arithmetic used, assert exact equality; where it is not,
state the construction the tolerance follows from. A numeral picked to make a world pass is
the defect inv. 49 names.

---

## 6. What this TZ does NOT do

- **No production file is touched.** `index.html`, `main.py` and `catalysts.json` appear in
  no diff; `coeffs.json`'s schema is untouched (hard floor item 5); the functions hard floor
  item 1 closes are CALLED, never edited.
- **`--verify`'s thresholds, its classes and `HARD_CLASSES` are unchanged.** The eighteen
  coins keep class `unexplained` and `--target`'s universe stays twelve until a later TZ
  acts on what this one measures. Reclassifying a coin because its gap is now attributed is
  out of scope, and is exactly the change a measurement may not authorise by itself.
- **No cause is named** — §1.
- **No fetch in this session** (hard floor item 9, inv. 44). The archive figures come from a
  dispatch the Boss runs. This TZ delivers an instrument built and self-tested offline;
  saying so is not PARTIAL (contract §9), and a forecast about a run that has not happened
  is banned outright (inv. 54).

---

## 7. Hard floor clauses this TZ touches — quoted from contract v20

> 1. **No change to scoring, leverage, liquidation or geometry math** unless the TZ
> explicitly cites a completed backtest (map §3.10b).

> 2. **Never edit a bench to make it pass.** A red bench is either a product defect or
> a stale expectation; both are findings, neither is a licence to change the
> assertion.

> 8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.

> 12. **Never remove, skip, comment out or `continue-on-error` a bench step to make CI
> green** — editing the assertion (item 2) and deleting the assertion are the same
> act; a step that cannot pass is a finding for the report.

---

## 8. Validation

Run every item; an item that cannot be run **fails** and is never «not applicable»
(contract §9). Baseline first: record each figure before the change.

1. `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` — exit 0.
2. `python3 bench/backtest_guard_bench.py` — exit 0, `FAIL 0`. State the new section's
   letter and check count, step 14's total before and after, and the new gate total term by
   term against your measured baseline (inv. 43).
3. `python3 bench/verify_bench.py` — exit 0, **40** checks, `FAIL 0`.
4. **Identity control (inv. 45):** W1 reports zero on identical input, and the instrument is
   then shown able to see a planted difference, with the count it saw. A comparator never
   proven on identity supports no claim about a real diff.
5. **Zero-cell refusal:** W5 exits non-zero.
6. **`--attrib` executed end to end offline against a synthetic cache directory**, with the
   number of cells attributed, the number of coins in each population, and confirmation that
   the run opened no socket. A mode reachable only by a dispatch is not covered by anything
   that runs (inv. 62).
7. **YAML:** the added step parses; its command matches the mode name; no
   `continue-on-error`; `git diff` on `backtest_bench.yml` shows the added step and nothing
   else, with the line count stated. **Whether that step executes on a runner is not
   forecast** (inv. 54, contract §9) — it is a dispatch; state only that the step exists and
   what it will run.
8. `git diff --name-only` names exactly three files. Restate the four `## 0` hashes measured
   after the change.
9. **Extremes, each with its own assertion:** an archive shorter than the longest window · a
   cell whose production value is missing · a cell where `volatility` is zero, which the
   `eff14` reproduction divides by · a coin in the cache and absent from production's output,
   and the reverse · a coin whose gap `g` exceeds `--verify`'s comparison window, which this
   mode must still attribute.

---

## 9. Report requirements

Beyond the §10 template: the section letter and why it was chosen from the file · per
world, the terms asserted and the count · **the derivation result — is production's `f`
two-point on this tree, established by the run-time test rather than by reading the
source** · the mode's own printed field list · `## Fingerprints`, mandatory.

`## Status` is COMPLETED when the instrument is built and self-tested offline. The archive
measurement is the Boss's dispatch and its absence is not PARTIAL (contract §9).

## Commit Message

```
TZ-40: attribute the production/archive return gap into end-instant, start-instant and residual terms
```
