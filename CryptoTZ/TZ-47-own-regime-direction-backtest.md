# TZ-47 — Direction layer: the coin's own regime word, measured

**Canonical filename: `TZ-47-own-regime-direction-backtest.md`.** The committed file is
named from this line and never from the name it arrived under (CANON hard rule 2).

**Class: branch TZ.** It authorises written files outside `CryptoReports/**`, so it opens a
branch and a pull request (contract §8).

**Model: Opus.** Multi-file, arithmetic, an additive change inside an instrument whose
existing figures must not move.

---

## 0. Fingerprint gate — quoted in full

**Required System Map revision: `**Revision 2026-09-16-b.**`** Any other revision, in
either direction, is BLOCKED before any work (contract §5).

Anchors — the complete table from the map's `## 0. Fingerprint`, to be cut by the table's
own rows and never by the anchor names expected (contract §5 step 2, since v23):

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-16-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `71. **A measurement that is not RETAINED was not taken,` |

Live files at that revision — the map's own table:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this TZ's gate adds, at the figures the map's `## 0` prose carries for them:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5102 | `ba633202f43845ba0fdafbc1b92d9c04` |
| `bench/backtest_guard_bench.py` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` |

Report all seven anchors with the text each fixed-string match returned, the table's own
row count beside the number compared, and every file above at its line count and MD5.

---

## 1. Why — the finding that forces this TZ

The map's open queue carries it in one row: **«The side of every trade rests on a smoothness
measure» — open — «a backtest TZ, and nothing in production before its reading.»**
`marketRegime`'s fourteen-day efficiency ratio decides the side on every list coin, and
efficiency measures how straight a path is, not which way it points.

`ANALYST-INSTRUCTIONS.md` `2026-09-16-c` drives two live prohibitions off that word, cut on
the coin's own structural row: **«A range coin is not published on either side»** (§2,
checklist item 57) and **«Fading a coin's own TREND is banned outright, in both
directions»** (§2, item 53). Four methodology revisions in three days each repaired the
symptom the previous one produced, and the file records why it cannot go further: it may
not invent a computation, so the defect is repaired by measurement and a specification or
not at all.

**This TZ builds the instrument and takes no reading.** The reading arrives from a
`backtest_bench.yml` dispatch, whose artifact the Architect audits. A session may not stand
behind a product fact (inv. 44, hard floor item 9), and the archive fetch is a workflow
step.

**What this TZ does not propose.** No ranking factor, no weight, no scoring switch, no
production edit. Map §8 closes «market regime as a scoring switch» on ten null cells; that
closure is about IC and about the MARKET word, and nothing here reopens it. Claim A below
is descriptive of a classifier; Claim B partitions an existing arm.

---

## 2. Interface check — run first, BLOCK on any miss

This specification was written against `SYSTEM-MAP-CRYPTOCALCUL.md` `2026-09-16-b`,
`EXECUTOR-INSTRUCTIONS.md` v23 and `ANALYST-INSTRUCTIONS.md` `2026-09-16-c`. **It quotes no
production constant by value anywhere**, deliberately: every threshold this measurement
touches is read at run time through the bench's existing cut (inv. 20, 49, 61, 65), so a
numeral here would be a fourth copy of a number that already lives in `index.html`.

What replaces inv. 55's quotation is this check. Before any work, confirm against the
repository, and **report BLOCKED naming the miss** if any line fails:

1. `marketRegime` exists in `index.html`, takes one stats object, and reads from it
   exactly `r7`, `r14` and `volatility` (map §3.12).
2. It compares against three named constants — `EFF_TREND`, `REG_STRESS_Z`, `VOL_HARD` —
   and returns a mode of `trend` / `range` / `stress` plus `dir`, where `dir` is read only
   on `trend` (map §3.12).
3. The bench's AST-cut block from `get_token_betas` in `main.py` yields per coin-date at
   least `volatility`, `r7`, `r14` and `eff14` (map §3.10).
4. `RR_MIN` is read from `index.html` at run time by the existing `--target` code path
   (map §3.10, inv. 65).
5. `marketRegime` is already inside a bundle this bench cuts and executes, and `--regimes`
   already calls it on BTC's row.

**Hard floor item 1 is not engaged and must not be read as engaged.** Quoted from
`EXECUTOR-INSTRUCTIONS.md` §7 so it can be compared rather than recalled (inv. 55):

> **No change to scoring, leverage, liquidation or geometry math** unless the TZ
> explicitly cites a completed backtest (map §3.10b). `scoreCandidate`, `momentumScore`,
> `qualityScore`, `scoreFinish`, `tradeGeometry`, `marketRegime`, `directionVerdict`,
> `leverageDecision`, `invalidationInfo`, `protectionPlan`, `liqPrice`, `liqTouchProb`,
> `residual7` are closed to edits by default.

This TZ edits none of them. It cuts `marketRegime` and executes it, which is what inv. 21
requires of a bench and what `ANALYST-INSTRUCTIONS.md` §2 already requires of an analysis
run: «the run therefore executes the cut `marketRegime` a second time, on the coin's own
structural row». If any stage of this TZ appears to require a production edit, that stage
is defective — report BLOCKED rather than editing.

---

## 3. Scope

**Files to Modify**

- `bench/backtest_bench.py` — one new mode, `--own-regime`, additive.
- `bench/backtest_guard_bench.py` — one new section, offline controls.
- `.github/workflows/backtest_bench.yml` — one step, plus its artifact path. **This TZ
  names the file, which is the authorisation hard floor item 8 requires; the authorisation
  is for the step below and for nothing else in it.**

**Files to Create** — none.
**Files to Delete** — none.
**Production files that must not appear in any diff:** `index.html`, `main.py`,
`catalysts.json`, every other bench, every other workflow.

---

## 4. Registered claims — fixed before the data (inv. 23)

Both cells and both claims are computed in one run. Every count printed is a count of
compared objects (inv. 43), and a cell with no objects fails rather than passes (inv. 22).

### Claim A — PRIMARY. The word is or is not a statement about direction

For every coin-date whose row is complete: `w` = the word `marketRegime` returns on that
coin's own row; `m` = `|r14|` from the same row, the raw fourteen-day move and the
numerator of the very ratio `w` is computed from.

Cells: `R` = coin-dates where `w` is `range`; `T` = coin-dates where `w` is `trend`.

- **The bar is derived in the same run** (inv. 49): `M_T` = the median of `m` over `T`.
- **Primary statistic:** `overlap` = the share of `R` whose `m ≥ M_T`, with CI95 by block
  bootstrap over dates, dates being the block as everywhere else in this bench.
- **Registered reading, three outcomes and all three are printed:**
  - `overlap ≤ 0.10` — the word separates movers from non-movers. «Own range → do not
    trade» refuses coin-dates that did not move, and the methodology stands as written.
  - `overlap ≥ 0.25` — falsified. At least a quarter of the coin-dates the rule refuses
    moved at least as much as the median coin-date it admits, so the word is a statement
    about smoothness and not about direction.
  - between the two — **unresolved**; the queue row stays open and no repair follows.
- **Fragility, registered now so it cannot be chosen later:** the statistic is also
  computed **leave-one-out** by coin. If dropping any single coin moves `overlap` across
  either boundary, the reading is reported as fragile and is not read as either outcome.
- Printed beside it, descriptive, no claim attached: the reverse overlap (share of `T`
  below the median of `R`), the quartiles of `m` in each cell, the `stress` cell's counts,
  the counts per cell and per coin, and the `trend`-up / `trend`-down split.

**Quorum.** A cell reports an interval only where the bootstrap has at least 20 distinct
date blocks and the cell holds at least 200 coin-dates; below either, the cell prints its
counts and no interval and the claim is unresolved. These two numbers are about the
instrument's power, not about the answer — the standing map §3.10c's `IC ≥ 0.030` carries.

**What Claim A rests on.** The word is production's word only if the archive's
`r14`/`volatility` reproduce production's. `--verify` read `unexplained` 0 and `coverage` 0
on 30 of 30 coins on 13.09.2026, and that is a dated reading which expires (inv. 56) — so
the same dispatch that takes this measurement re-takes it, and the report states both.

### Claim B — SECONDARY, doubled bar. What the refusal costs

Partition `--target`'s existing production arms — `prod` and `prod_anchor` — by the coin's
own word at the setup date, and report `Ω = n_tgt / n_stop` per cell, per side, per arm,
with CI95 by block bootstrap and the bar `1 / RR_MIN` read at run time (inv. 65).

- **Doubled bar** (§3.10a's convention for anything that is not the primary): a difference
  between cells is claimed only on non-overlapping **CI99**. Below that, the cells are
  printed and no difference is claimed.
- **Nothing follows from Claim B alone.** It cannot license a methodology change, a
  production change or a side; its one function is to say whether the refusal is expensive.
  Every existing `--target` figure sits entirely below the bar, so a cell below the bar is
  the expected state and is not a finding (inv. 32).
- **Population unchanged.** The partition reads `--target`'s own records and adds one
  field. It does not re-run geometry, does not re-admit a setup and does not touch
  `target_gate`: a symbol `--verify` removed from the arms stays removed. Claim A, like
  `--attrib`, is deliberately not filtered by comparability and reads all 30 coins.

---

## 5. Construction

- **No new formula, in any language or file** (inv. 21, 38). The word comes from
  `marketRegime`, cut and executed on the coin's row. The clipping, the thresholds and the
  `stress` branch are production's.
- **No numeral for any production constant** anywhere in the new code. `EFF_TREND`,
  `REG_STRESS_Z`, `VOL_HARD` and `RR_MIN` are read through the existing cut.
- **Look-ahead free.** The word at date `t` uses only the row at `t`, which the bench
  already builds from the series truncated at `t`.
- **Additive.** `--own-regime` adds a mode and a field; it changes no existing mode's
  output. Every other mode's numbers must be byte-identical after the change.
- **One output object, printed in full**, so the reading survives the job log (inv. 71).

---

## 6. Controls — offline, `bench/backtest_guard_bench.py`, gate step 14

**The section letter is READ from the file's own `# X.` headers and never counted** — two
sections already share `E` (map §10). State the letter chosen and why in the report.

1. **Three known-answer worlds, ten seeds each** (inv. 23, and the ten-seed convention
   `--selftest` already uses). The worlds certify what the statistic means before it is
   pointed at the archive:
   - **ramp** — every coin a smooth monotone climb: every coin-date must class `trend`,
     `R` must be empty, and the mode must say so rather than divide by zero.
   - **driftless walk**, equal volatility: the word carries no information about direction
     by construction, so `overlap` must read near 0.5 and the two cells' `m`
     distributions must overlap heavily.
   - **volatile climb** — the same drift as the ramp with volatility scaled up so
     `|eff|` falls below the trend cut: every coin-date must class `range` while `m` stays
     large, and `overlap` must read near 1. This is the hypothesised real mechanism
     installed as a known answer.
2. **Truncation invariance.** The word and every printed statistic for date `t`, computed
   from the full series, must be **byte-identical** to the same computed from the series
   truncated at `t`.
3. **Identity on the existing arms** (inv. 45). With the new field present, `--target`'s
   per-arm output on one seeded world must differ from the pre-change output in zero
   fields; the same differ must then be shown able to see a deliberately perturbed field,
   because a comparator that flips nothing has not run. The world in which the identity
   holds is named in the control: it holds unconditionally, because no existing arm reads
   the new field (inv. 69).
4. **Positive dependence on the constant, not a stated absence** (inv. 50). Perturb
   `EFF_TREND` inside the extracted bundle and assert the cell populations MOVE. This
   proves the word is read from production's constant; an assertion that no numeral
   appears would be load-bearing prose instead.
5. **Negative control, partition written here and not left to the session** (inv. 45, 68).
   Invert the trend comparison in the cut bundle. World 1, world 3 and control 4 **must
   turn red**; control 2 and control 3 **must NOT fire**, each of them running the same
   inverted code on both sides of its own comparison. Revert and confirm the tree is clean.
6. **Counts.** Every assertion increments at the comparison site; the section prints its
   own total; zero comparisons fails the section (inv. 22, 43).

---

## 7. Workflow wiring — `backtest_bench.yml`, one step

- One step running `--own-regime`, **after `--target`** so the arms exist to partition.
- **`if: ${{ !cancelled() }}` on that step** (inv. 71). `--verify` exits non-zero on every
  `coverage` or `unexplained` class, which is precisely the run with something to measure,
  and a step behind it is skipped by default. This is not `continue-on-error`: the job
  still fails.
- **The whole reading is written to `own-regime.txt` inside the uploaded artifact.** A
  measurement that is not retained was not taken (inv. 71); the job log is not a retention
  path.
- Nothing else in that workflow is authorised — not the cache key, not another step's
  condition, not the artifact's other contents.

---

## 8. Deferred deliberately — report, do not act

**The dispatch cache freeze stays untouched in this TZ.** Map §10 carries «The dispatch
cache is frozen at 05.09 and every run refetches the universe — open — any TZ opening
`backtest_bench.yml`», keyed `bench-${{ inputs.source }}-${{ inputs.years }}y-v4`. This TZ
opens that workflow and the trigger therefore fires, and the decision is to leave the key
alone: the first own-regime reading must be taken on the same fetch discipline every
standing figure in §3.10a was taken on, and moving the archive's provenance in the same
change that takes a new reading would confound the two. Record it under
`## Pre-existing Issues` with this paragraph as the reason, and do not touch the key.

---

## Validation

Written by the Architect. Every item is run; an item that cannot be run **fails** and is
never «not applicable» (contract §9). Evidence is a command and its output.

1. `python3 -m py_compile bench/backtest_bench.py` — exit 0.
2. `python3 -m py_compile bench/backtest_guard_bench.py` — exit 0.
3. `git diff --stat` shows **no change** to `index.html`, `main.py`, `catalysts.json`, any
   other bench or any other workflow. Print the command and its output.
4. `--selftest`: its three world blocks still pass, and its recorded check count is stated
   **before and after** this change.
5. Gate step 14: total **before and after**, with the delta attributed term by term — the
   new section's own count plus any movement elsewhere, stated as arithmetic (map §0
   convention). `FAIL 0`. State the section letter and that it was read from the file.
6. The three known-answer worlds, ten seeds each: print per world the cell counts,
   `overlap`, and the assertion each world carries.
7. Truncation invariance: print the number of comparisons and that all were byte-identical.
8. Identity on `--target`: zero differences on identical input, and a non-zero count
   against the perturbed field. Both numbers printed.
9. Constant-dependence control: the populations before and after the perturbation.
10. Negative control: the exact set that turned red and the exact set that did not, against
    §6 item 5's written partition. Then `git status` clean after the revert.
11. **`--own-regime` is NOT run against the archive in this session.** No fetch, no
    dispatch, no claim about a reading (inv. 44, hard floor item 9). A session figure here
    would be a product fact with no reproduction behind it.
12. CI: the hosted `Bench gate` on the pushed branch, with its conclusion, read or stated
    as unread (contract §9 — never «expected to have fired»). `backtest_bench.yml` is
    `workflow_dispatch` only and does not run on push: say so.
13. **Negative test for the CI change** (contract §9): force a real failure in the new gate
    section, confirm step 14 turns red, revert, confirm the tree is clean. The dispatch
    workflow's own new step cannot be proven red from a session — state that gap plainly;
    it does not make the report PARTIAL.

Extremes to cover in the controls: an empty cell, a cell of one coin-date, a coin whose
`volatility` is absent for a date, a date where every coin classes `stress`, and a world
where `R` and `T` are both non-empty but one holds a single date.

---

## Touches — benches asserting anything this change could falsify

Enumerated here because a TZ changing a classifier names every bench that asserts it
(inv. 67), and because a negative assertion covering only the strings a change falsifies
says nothing about the assertions it falsifies:

- `bench/backtest_guard_bench.py` — gate step 14; this TZ adds a section to it and may
  move no existing section's count without attributing it.
- `bench/verify_bench.py` — asserts `--verify`'s rules, including comparability and the
  class table. Untouched: Claim B inherits `target_gate` unchanged and Claim A is outside
  it. If any assertion there moves, that is a defect of this change.
- `bench/direction_bench.py` — asserts the production direction engine. Untouched.
- `bench/journal_bench.js`, `bench/catalyst_bench.js`, `bench/prot_bench.js`,
  `bench/exhaustion_bench.js` — no production surface changes, so none may move.

---

## Commit Message

```
TZ-47: own-regime partition for the direction layer — bench mode, offline controls, dispatch step
```
