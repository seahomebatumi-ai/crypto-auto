# TZ-48 — The coin's own regime word, through the gate that already exists

**Canonical filename: `TZ-48-own-regime-gate.md`.** The committed file is named from this
line and never from the name it arrived under (CANON hard rule 2).

**Class: branch TZ.** One file outside `CryptoReports/**`, so a branch and a pull request.

**Model: Opus.** Arithmetic inside an instrument whose standing figures must not move.

**Supersedes TZ-47.** TZ-47 was BLOCKED correctly: its §2 line 5 named an interface that
does not exist (`--regimes` runs `btc_regimes` and `run_walk`, not `marketRegime`), and its
three known-answer worlds registered expectations their author had assigned rather than
probed. This TZ inherits TZ-47 §1 (why), and replaces everything else. Every interface
below was read from `bench/backtest_bench.py` and `index.html` in the Project at the
fingerprints stated in §0, and every registered expectation carries the line that derived
it.

---

## 0. Fingerprint gate — quoted in full

**Required System Map revision: `**Revision 2026-09-16-b.**`** Any other revision, either
direction, is BLOCKED before any work (contract §5).

Anchors — the complete table from the map's `## 0. Fingerprint`, cut by the table's own
rows and never by the anchor names expected:

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

The file this TZ edits, as measured in the Project this specification was written against:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5102 | `ba633202f43845ba0fdafbc1b92d9c04` |

Report all seven anchors with the text each fixed-string match returned, the table's own
row count beside the number compared, and every file above at its line count and MD5.

---

## 1. Why — unchanged from TZ-47 §1

The map's open queue: **«The side of every trade rests on a smoothness measure» — open — «a
backtest TZ, and nothing in production before its reading.»** `ANALYST-INSTRUCTIONS.md`
`2026-09-16-c` drives two live prohibitions off `marketRegime`'s word cut on the coin's own
structural row — a range coin is published on neither side (§2, checklist item 57), and
fading a coin's own trend is banned outright (item 53) — while the word itself is built from
`r14 / (vol · sqrt(2 · H_NOISE))`, which measures how straight a path is and not which way
it points.

The instrument takes the reading; this TZ builds it. No production edit, no methodology
edit, no ranking factor, no weight. Map §8's closure of «market regime as a scoring switch»
is about IC on the MARKET word and is not reopened.

---

## 2. What already exists — read, not assumed

| Site | What it is |
|---|---|
| `index.html:1864` `function marketRegime(btcStats)` | reads `volatility`, `r7`, `r14` off whatever record it is handed; `stress` first on `v >= VOL_HARD` or `|z| >= REG_STRESS_Z`, then `trend` on `|eff| >= EFF_TREND` with `dir`, else `range`; no stats or no volatility → `range` with `known:false` |
| `backtest_bench.py:3325` | the target driver already records `reg: marketRegime(j.btcStats).mode` — the MARKET word, one per date |
| `_rg_word` / `_rg_split` | split DATES by that word, asserting one word per date |
| `regime_gate_summary` / `run_regime_grid` (`--regime-gate`) | the `RG_H_GRID × RG_RR_GRID × side × pop` grid with Ω, CI95, quorum, right-truncation accounting, labeller agreement and a funding break-even |
| `_arm_pool(dates, arm, side, level, with_b)` | the block bootstrap over dates, cut by population rather than rewritten |
| `TGT_QUORUM_N = 60`, `TGT_QUORUM_D = 20` | the quorum, already declared once |
| `m["inv_rr"]` → `m["bar"]` | the bar, `1 / RR_MIN` read from `index.html` at run time |
| `_rg_below` / `_rg_verdict` | the registered comparison and its verdict shape |
| `CdBuilder.build` | the coin's own row, carrying `volatility`, `r7`, `r14`, `eff14` under `CD_FIELDS`' own names |

**Therefore this measurement adds no formula, no threshold, no quorum and no bar.** It adds
one call to production's `marketRegime` on an argument production's own sibling readers
already receive, and one population split. Anything beyond that is out of scope.

---

## 3. Scope

**Files to Modify:** `bench/backtest_bench.py`.
**Files to Create / Delete:** none.
**Must not appear in any diff:** `index.html`, `main.py`, `catalysts.json`, every other
bench, every workflow.

Hard floor item 1 is not engaged. Quoted from `EXECUTOR-INSTRUCTIONS.md` §7 so it is
compared rather than recalled:

> **No change to scoring, leverage, liquidation or geometry math** unless the TZ
> explicitly cites a completed backtest (map §3.10b). `scoreCandidate`, `momentumScore`,
> `qualityScore`, `scoreFinish`, `tradeGeometry`, `marketRegime`, `directionVerdict`,
> `leverageDecision`, `invalidationInfo`, `protectionPlan`, `liqPrice`, `liqTouchProb`,
> `residual7` are closed to edits by default.

`marketRegime` is cut and executed, never modified — which is what inv. 21 requires of a
bench and what `ANALYST-INSTRUCTIONS.md` §2 already requires of an analysis run. If any
stage below appears to need a production edit, that stage is defective: report BLOCKED.

---

## 4. Construction

**4.1 One field in the driver.** Beside the existing `reg`, record the coin's own word:
`marketRegime(j.cd)`, taking `mode` and `dir`. The argument is the WHOLE `j.cd` record, not
a hand-built subset — the file's own comment at `run_target` states why (inv. 48: a bench
that builds its own input proves the function and not the wiring), and `j.cd` carries
`volatility`, `r7` and `r14` under exactly the names `marketRegime` reads.

**4.2 The population is a subset of OBSERVATIONS, not of dates.** This is the one
structural difference from the market word and the reason `_rg_word` must not be reused: the
coin's word varies within a date by construction, so a date belongs to several populations
at once. Build a date-shaped VIEW — each date's `obs` filtered to one word, dates whose
filtered `obs` is empty dropped — and hand that view to `_arm_pool` unchanged. Blocks stay
dates, the bootstrap is untouched, and the pool is cut rather than rewritten (inv. 38).

**4.3 The grid is the existing one.** Same `RG_H_GRID`, `RG_RR_GRID`, sides, and
`RG_POPS` with `stress` printed separately and never merged. Same `TGT_QUORUM_N` /
`TGT_QUORUM_D`. Same `m["bar"]` from `inv_rr`. An empty cell names the REASON it is empty,
as `regime_gate_summary` already does (inv. 22).

**4.4 The census rides along, with no decision attached.** Per word, print the counts and
the quartiles of `|r14|` taken from the same `j.cd` the word was computed from, plus
`overlap` — the share of the `range` cell whose `|r14|` reaches the `trend` cell's median.
**`overlap` carries no band and decides nothing** (inv. 49): it is governed by the
cross-sectional spread of volatility, so its reference is computed in the same run from a
**decoupled null** — the same rows with the pairing between `|r14|` and `volatility`
destroyed within each date, preserving both marginals and breaking only their coupling.
Report `overlap` beside its null and let the reading be a comparison, never a threshold.

**4.5 Existing output must not move.** The market-word grid, `--target`'s arms and every
other mode produce byte-identical output after this change.

---

## 5. Registered expectations and what derived them

Fixed before the data (inv. 23). Every line names its derivation; nothing here is assumed.

| # | Expectation | Derived by |
|---|---|---|
| P1 | **PRIMARY.** On every cell with quorum in BOTH populations, CI95 of Ω on the coin's own `range` overlaps or exceeds CI95 on its own `trend`. It falls exactly when `range` is strictly below at least once — `_rg_below`, unchanged | the market-word thesis already registered in `_rg_verdict`, reused verbatim on the coin's word; falsifier and comparison are the file's, not this TZ's |
| P2 | A cell whose either side lacks quorum is **not a comparison** and is counted as such | `_rg_verdict`'s own quorum rule (inv. 22) |
| P3 | Undecidable is a legitimate outcome and is printed as `decidable: false`, not as a pass | `_rg_verdict`'s `decidable` field |
| C1 | Census, descriptive: `overlap` printed against its same-run decoupled null. No band, no decision | inv. 49; and the TZ-47 run measured `overlap` at 0.031 mean / 0.079 max on a world with a 4× volatility spread and no direction at all, which is why no fixed band is admissible |
| W1 | A world of smooth monotone climbs classes `stress`, never `trend` — `stress` is tested first and a smooth path drives `\|z\| = \|r7\|/(vol·sqrt(H_NOISE))` upward without bound | derived by the TZ-47 run: 4680 of 4680 coin-dates `stress`, `\|z\|` ≥ 2.5e13; and re-derived here from `index.html:1882`, which returns before the trend branch |
| W2 | A staircase climb (jump every 100 h over a low-vol floor) classes `trend` on every coin-date, leaving the `range` population empty | derived by the TZ-47 run's staircase world |
| W3 | A zig-zag world classes `range` on every coin-date, leaving `trend` empty — so `overlap` is UNDEFINED there, and the mode must say so rather than divide by an empty median | derived by the TZ-47 run's zig-zag world |
| W4 | A driftless walk with EQUAL volatility reads `overlap` 0.000: with `vol` constant the word is a monotone threshold on `\|r14\|` itself, so the two populations are disjoint intervals | derived by arithmetic on `index.html:1874` and confirmed by the TZ-47 run at 0.000 on 10 of 10 seeds |
| W5 | A mixed world — half staircase, half zig-zag — reads `overlap` 1.000: every `range` coin-date carries a larger raw move than the median `trend` coin-date | derived by the TZ-47 run's mixed world, 1.000 on 10 of 10 seeds |
| W6 | Brownian noise cannot reach an all-`range` world at any parameter: `P(\|eff\| < EFF_TREND)` is bounded near 0.45 | map §3.12's «~55 % of pure-noise windows read trend», read from the other side |

**The Executor re-derives W1–W6 on its own fixtures and reports every divergence from the
figures above rather than asserting them.** A figure that does not reproduce is a finding,
not a failure to be argued away; the worlds are the Executor's to build (CANON: where the
Architect cannot execute production, the world is specified by the shape it must exhibit).

---

## 6. Controls — lab section, `--lab-selftest`

**The section letter is read from the file's own `print("X · …")` headers and never
counted** — state the letter and that it was read from the file, not inferred.

1. **W1–W6 as assertions**, `--lab-seeds` seeds each, at the default and at 10.
2. **Truncation invariance.** The coin's word and every printed statistic for date `t` from
   the full series must be byte-identical to the same from the series truncated at `t`.
3. **Identity (inv. 45, 69).** With the new field present, `--target`'s and
   `--regime-gate`'s outputs on one seeded world differ in ZERO fields from the pre-change
   run; the same comparator must then be shown able to see a deliberately perturbed field.
   Name the world: the identity holds unconditionally, because no existing arm or split
   reads the new field.
4. **Positive dependence on the constant, not a stated absence (inv. 50).** Perturb
   `EFF_TREND` in the extracted bundle and assert the coin-word populations MOVE. A check
   that no numeral appears would be prose doing a control's work.
5. **Negative control, partition written here (inv. 45, 68).** Invert the trend comparison
   in the cut bundle. **Must turn red:** W2, W5 and control 4. **Must NOT fire:** controls
   2 and 3, each running the inverted code on both sides of its own comparison. Revert and
   confirm the tree is clean.
6. **Counts (inv. 22, 43).** Every assertion increments at the comparison site; the section
   prints its own total; zero comparisons fails the section.

---

## 7. Reading items — report, do not edit

These are files this specification has NOT read, so they are reading items and never check
items (CANON). Report the answer; change nothing.

1. **`.github/workflows/backtest_bench.yml`:** does a step run `--regime-gate`, and is its
   output retained inside the uploaded artifact (inv. 71)? Quote the step and its `if:`.
   If the mode is unretained or unreachable, that is the next TZ, not this one.
2. **`bench/backtest_guard_bench.py`:** does gate step 14 assert anything about `reg`,
   `_rg_word` or the driver's record shape that this change would falsify (inv. 67)? Quote
   what you find. Do not edit it.
3. **The dispatch cache key** `bench-${{ inputs.source }}-${{ inputs.years }}y-v4`, frozen
   at 05.09: still out of scope, for the reason TZ-47 §8 gave — the first coin-word reading
   is taken on the same fetch discipline every standing figure was taken on. Report under
   `## Pre-existing Issues`.

---

## Validation

Written by the Architect. An item that cannot be run **fails**; it is never «not
applicable» (contract §9). Evidence is a command and its output.

1. `python3 -m py_compile bench/backtest_bench.py` — exit 0.
2. `git diff --stat`: no change to `index.html`, `main.py`, `catalysts.json`, any other
   bench, any workflow. Print the command and its output.
3. `--selftest` check count stated **before and after**; unchanged.
4. `--lab-selftest`: the new section's own count, the letter used and how it was read, and
   the prior sections' counts before and after with any delta attributed term by term.
5. W1–W6 at `--lab-seeds 3` and `--lab-seeds 10`: per world, the cell counts, `overlap` or
   its explicit undefined, and the divergence from §5's figures if any.
6. Truncation invariance: the number of comparisons and that all were byte-identical.
7. Identity: zero differences on identical input for BOTH `--target` and `--regime-gate`,
   and a non-zero count against the perturbed field. All three numbers printed.
8. Constant dependence: the populations before and after perturbing `EFF_TREND`.
9. Negative control: the exact set that turned red and the exact set that did not, against
   §6 item 5's written partition; then `git status` clean after the revert.
10. **The archive is NOT read in this session.** No fetch, no dispatch, no figure from real
    data (inv. 44, hard floor item 9). The reading is the Boss's dispatch and the
    Architect's audit of the artifact.
11. CI: the hosted `Bench gate` on the pushed branch with its conclusion, read or stated as
    unread. `backtest_bench.yml` is `workflow_dispatch` only and does not run on push.
12. §7's three reading items answered, each with the text it was answered from.

Extremes the controls must cover: a population of one date; a date whose filtered `obs` is
empty; a coin-date whose `volatility` is absent, where `marketRegime` returns
`known:false`; a world where every coin-date is `stress`; and a grid cell where the arm
admitted no setup at all.

---

## Touches

- `bench/backtest_bench.py` — this change; every other mode's output must be byte-identical.
- `bench/backtest_guard_bench.py`, `bench/verify_bench.py`, `bench/direction_bench.py` —
  untouched. If any assertion in them moves, that is a defect of this change, not a stale
  expectation.

---

## Commit Message

```
TZ-48: the coin's own regime word through the existing gate — one driver field, one population view
```
