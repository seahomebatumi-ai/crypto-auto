# TZ-32 — Regime gate and horizon on the archive

**Canonical filename:** `TZ-32-regime-gate-on-archive.md` — commit to `CryptoTZ/`
under exactly this name, whatever name the file arrived under (contract §3).

**Model: Opus.** Statistical instrument, four files, a driver addition, a bar that must
be derived rather than written, and a known-answer control whose correct outcome is a
REFUSAL. Sonnet is not authorised for this TZ.

**Supersedes TZ-31** (`TZ-31-horizon-ladder-on-archive.md`), which was BLOCKED under
contract §12 without touching a file: its `## 6. Validation` specified a known-answer
control for a horizon-ladder arm while its `## 2. Scope` authorised a regime gate. TZ-31
is closed and is not to be executed. Nothing it specified was implemented; this TZ is
written against the unmodified tree.

---

## 0. Fingerprint gate — blocking

Required System Map revision and all seven content anchors, quoted in full
(contract §5). Any mismatch in either direction → **BLOCKED**, no work.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-06-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `65. **A bar derived from the constant it judges moves with it.**` |

Live files at this revision — measure each, report any difference under
`## Pre-existing Issues`, act on none:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Every file this TZ modifies carries no row in that table**, so each figure is stated
here as the map requires. A difference is a `## Pre-existing Issues` line, never a reason
to adapt the work.

| File this TZ modifies | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 3240 | `d2dad0f80afa2c191c2faf1d40081a88` |
| `bench/backtest_guard_bench.py` | 580 | `93c2726342e9f8b59579d0ba707a8a52` |
| `.github/workflows/backtest_bench.yml` | 140 | `8a994edb5be622d75196e2769c3cf45c` |

---

## 1. Why this exists — the direction layer has one input and it is the wrong one

Every directional side this engine publishes comes from `marketRegime`
(`index.html:1864`). Below its stress override — `volatility >= VOL_HARD` or
`|z| >= REG_STRESS_Z`, which closes both sides and is not the subject here — the word is
decided by one number: `eff14 = r14 / (v·√(2·H_NOISE))` against `EFF_TREND`.
**Efficiency measures SMOOTHNESS, not direction.** A market that climbs with pullbacks —
the only kind that exists — reads `ДИАПАЗОН` while it climbs, and on a `ДИАПАЗОН` word
the engine refuses every directional entry on every coin without a trend of its own.
Measured 07.09: BTC sat at 91 % of its ninety-day range, roughly a third above the low of
that range, and the word was `ДИАПАЗОН` on three consecutive runs. **The owner is watching
a rising market and reading an answer with no long in it, and the reason is not caution —
it is that the classifier cannot see a rally that breathes.**

Five revisions of `ANALYST-INSTRUCTIONS.md` in four days each repaired the symptom the
previous one produced. That is the signature of a defect upstream of the methodology, and
it sits in a function the hard floor closes to edits without a completed backtest
(item 1). **So the measurement comes first, and this TZ is it.**

**The second axis is the window, and the owner named it: two to seven days.** The whole
standing result rests on `H_NOISE = 168 h`, where run #16 recorded `P(никуда)` at 69 %
long and 60 % short — two thirds of the engine's decisions never reach either barrier
inside the window they are judged in. A gate judged only at the horizon where most
outcomes are missing has not been judged.

---

## 2. Scope — exactly this, nothing adjacent

1. `bench/backtest_bench.py` — one additive arm, `--regime-gate`, on the existing archive
   machinery. Without the flag every existing mode behaves byte-identically; **this is
   asserted, not claimed** (§6 item 2).
2. `bench/backtest_bench.py` — `TARGET_DRIVER` gains the R:R substitution described in
   §3, additive: no existing key, field or arm changes shape.
3. `bench/backtest_bench.py` — section D of `--lab-selftest` gains **D7**, the
   known-answer control for the new arm.
4. `bench/backtest_guard_bench.py` — offline assertions on the new arm's bar derivation,
   its partition and its right-truncation accounting, calling production functions by
   name and re-implementing none of them (inv. 21).
5. `.github/workflows/backtest_bench.yml` — **named explicitly, per hard-floor item 8** —
   gains a `workflow_dispatch` boolean input passing `--regime-gate`. No other change.

**Out of scope, and a TZ deviation if touched:** `index.html`, `main.py`,
`catalysts.json`, `ANALYST-INSTRUCTIONS.md`, any production constant, any scoring, regime
or geometry function (hard-floor item 1), `btc_regimes()` and everything downstream of it,
`bench.yml` steps 1–13, and every existing published figure. **No new dependency, no new
data source, no host this bench does not already use.**

---

## 3. The arm

### 3.1 The regime word is already on the row — read it, do not build it

`marketRegime` is already exported to the target bridge (`TARGET_JS_FUNCS`,
`bench/backtest_bench.py:2223`), already called per job in the driver
(`reg: marketRegime(j.btcStats).mode`, `:2280`), and its word is already stored on every
setup row as `o["reg"]` (`:2431`). `VOL_HARD`, `EFF_TREND` and `REG_STRESS_Z` are already
in `TARGET_JS_VARS` (`:2224-2228`). **No bridge extension is authorised and none is
needed**; the partition is a grouping over a field the arm already carries. An
implementation that recomputes the regime word anywhere is a second implementation of a
production rule and is banned (inv. 38).

### 3.2 The grid

For every archive date the bench already resolves, construct the production long and short
setups on every admitted symbol and resolve each over

`H ∈ {48, 72, 96, 120, 168, 336} h` × `RR ∈ {1.0, 1.5, 2.0, 3.0}`

with the stop untouched. `H` is passed through the existing `H_override` parameter of
`run_target`, which `--lab-selftest` D3 already uses (`:2982-2986`); no new horizon
machinery is written.

**R:R is applied as a target substitution inside the driver, because the stop is only
known there.** After `dec = leverageDecision(...)`, with `b_log = |log(dec.inv.price / E)|`
in the same log units the bench already uses, the substituted extremum for each `RR` in a
grid carried on the job is `E·exp(+RR·b_log)` long and `E·exp(−RR·b_log)` short, handed to
the **unmodified** `tradeGeometry` through the same shape `subs` already returns. Keys are
`rr:<value>`. `[решение принято мной]` The discarded alternative is a two-pass design that
reads `stop` back into Python and re-calls the bridge: it doubles the node work and splits
one decision across two round trips for no gain in fidelity.

### 3.3 The partition — three words, two populations

`marketRegime` returns **three** modes. All three are reported; only two are compared.

| Population | Rule |
|---|---|
| `range` | the primary claim's first population |
| `trend` | the primary claim's second population |
| `stress` | **excluded from the claim**, printed as its own counts and never folded into either |

Folding `stress` into either side contaminates the exact word under test, and reporting it
as a third comparison would multiply the cells without multiplying the evidence.

**`btc_regimes()` is not touched, not replaced and not compared as a claim.** The arm
prints one integer per (`marketRegime` word × `btc_regimes` word) cell across the dates it
resolved — a count of agreement, wiring nothing and deciding nothing. The labeller under
test is production's, because the gate under test is production's.

### 3.4 Reported per cell, per side, per population

| Field | Note |
|---|---|
| `n` setups and `n_dates` | counts, never estimates (inv. 43) |
| `P_none` | reached neither barrier inside `H` |
| `Ω = n_tgt / n_stop` with CI95 | the block bootstrap the arm already uses — cut it, do not rewrite it (inv. 38) |
| the cell's own bar | **derived at run time**, below |
| `n_dates` lost to right-truncation | below |
| break-even funding rate | below |

**The bar is derived at run time and no numeral for it appears in this TZ or in the
code.** Each cell's bar is the mean of `1/rr` over that cell's own admitted setups, taken
from the `rr` the **unmodified** `tradeGeometry` returns. It is computed rather than
written even where the nominal `RR` looks like the answer, because the chase anchor can
move the entry and the realised `rr` need not equal the nominal one — and a bar must
follow the object it judges (inv. 61, inv. 65).

**Right-truncation is accounted or the grid is uninterpretable.** A setup at `H = 336 h`
needs fourteen days of archive after entry, so the tail of the series produces no resolved
setup there and that sample is not the sample at 48 h. Report per cell the dates lost and
the last usable entry date. **A rising `Ω` on a shrinking sample is not a rising `Ω`.**

**Funding is charged in arithmetic because the archive cannot charge it in data.**
Historical funding is a separate dataset and importing it is a new source this TZ does not
authorise. Report per cell the constant eight-hour rate at which the cell's advantage over
the `168 h / RR 2.0` reference is exactly consumed, from the cell's own mean reward and
`FUND_PAY_7D` scaled by `H`.

**Quorum is the one the existing grid already applies**, read from the code, not restated
here (inv. 20). A cell below quorum prints its counts and no `Ω`.

---

## 4. Registration — one primary claim, fixed before the run

**PRIMARY CLAIM.** Partitioned by the regime word `marketRegime` returns on the entry
date, the directional setups admitted on `range` dates resolve **no worse** than those
admitted on `trend` dates: at every cell clearing quorum, the `range` `Ω` CI95 overlaps or
exceeds the `trend` `Ω` CI95 on the same side.

**Consequence, registered now (inv. 23):**

- **Claim holds** → the regime word does not separate profitable directional entries from
  unprofitable ones, so the gate that refuses every `ДИАПАЗОН` day is destroying trades
  rather than avoiding losses. The finding opens a production TZ against `marketRegime`
  under hard-floor item 1, which this measurement then satisfies.
- **Claim fails** → the gate is doing its job, `ДИАПАЗОН` days genuinely have nothing, and
  the engine's silence on those days is correct. The methodology stops being edited for it
  and the owner is told plainly that the market, not the engine, is the constraint.

**Registered exploration, at §3.10a's doubled bar (CI99), wiring nothing by itself:** where
`eff14` does not separate the two populations, does **position inside the ninety-day
range** or **fourteen-day relative strength against BTC** — both already carried in `cd`,
neither requiring a new input — separate them? This is the owner's standing request
measured rather than argued, and a positive cell buys a hypothesis for a later TZ, never a
production edit.

**A positive primary wires nothing by itself** — §3.10a's standing gate is a fresh
confirmation run after +26 weeks of new data, and it is not waived here.

---

## 5. Constraints

- **Never edit an assertion to make it pass** (hard-floor item 2). A red D7 is a broken
  instrument and a finding; report it and stop.
- **A validator that passes with no data is a failed validator** (inv. 22). Every count is
  a count of comparisons and every check fails on zero.
- **No expected totals are predicted anywhere in this TZ** (inv. 49). Check counts are
  reported as measured.
- **The run needs a warm cache and the three-year archive**, which is why
  `backtest_bench.yml` is `workflow_dispatch` only. Do not attempt the measurement in
  session; a session fetch may not stand behind a product fact (hard-floor item 9).
- Report the local reading and the runner reading separately and name which is which.

---

## 6. Validation

Written by the Architect, against the arm `## 2` authorises. Every item runs; an item that
cannot run **fails** (contract §9).

1. `python3 -m py_compile bench/backtest_bench.py` and
   `python3 -m py_compile bench/backtest_guard_bench.py` — exit 0.
2. **Byte-identity of the untouched path.** Run `--target` WITHOUT `--regime-gate`
   against the pre-change checkout and the post-change checkout on the same cached
   archive; every published figure identical. The driver addition of §3.2 is inside this
   assertion, not outside it: an unused `rr:` key must not move one existing number.
   Report the diff line count, and report `0` only if a diff was actually taken.
3. `python3 bench/backtest_bench.py --lab-selftest` — green, check count recorded, delta
   against the baseline count stated.
4. **D7, the known-answer control on the PARTITION, and its correct outcome is a
   REFUSAL.** On the driftless synthetic world the two populations must **not** separate:
   for every cell clearing quorum, the `range` `Ω` CI95 and the `trend` `Ω` CI95 must
   overlap on the same side. A driftless world has no regime to find; an instrument that
   separates the populations there is inverted, and every number it produces on the
   archive is worthless. **D7 fails on a separation.**
   **D7 also fails if the control cannot fire.** Before the overlap is read, assert on
   that same world that both words occur, that each clears quorum on at least one cell,
   and that `stress` is excluded rather than absent by construction. A control in which
   one population is empty asserts nothing (inv. 22), and a known-answer control that
   cannot fail is dead specification, not a guard. If the driftless world cannot produce
   both words at quorum, that is an instrument defect: report it and stop.
5. **Negative test on the guard** (contract §9, CI clause): break the bar derivation in
   the working tree, confirm gate step 14 turns red and names the assertion, revert,
   confirm the tree is clean and the step green. Report both check counts.
6. `bench.yml` steps 1–13 — **delta zero**, replayed against the unmodified checkout
   before any edit and again after, so the zero compares two measurements and not a
   measurement against this document.
7. Step 14 check count before and after, both as measured.
8. **The dispatch.** Running `backtest_bench.yml` with the new input on `main` after merge
   is the Boss's action, not the Executor's; the report states that the input exists, that
   the flag reaches `--target`, and that the workflow file parses. Do not forecast the run
   (inv. 54).
9. Extremes, each in this arm's own vocabulary: a cell with zero resolved setups · a cell
   below quorum · a population with no dates at all · a date range in which every date is
   `stress` · a symbol removed by `target_gate` mid-grid · an archive whose last usable
   entry precedes the first date at `H = 336 h` · a side with no setups in one population ·
   a cell whose realised `rr` differs from its nominal `RR` on every setup.
10. Explicit no-regression statement covering `index.html`, `main.py`, `catalysts.json`,
    every existing `--target` figure and every `bench.yml` step.

---

## 7. Report

Contract §10 format, to `CryptoReports/TZ-32-regime-gate-on-archive-report.md`,
straight to `main`. Fingerprints for the System Map and for every file the map's `## 0`
table lists, read from that table at authoring time. The implementation waits on a branch.
