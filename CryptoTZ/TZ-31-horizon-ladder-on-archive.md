# TZ-31 — Regime gate and horizon on the archive

**Canonical filename:** `TZ-31-horizon-ladder-on-archive.md` — commit to `CryptoTZ/`
under exactly this name, whatever name the file arrived under (contract §3).

**Model: Opus.** Statistical instrument, three files, a bar that must be derived rather
than written, and a known-answer control whose correct outcome is a REFUSAL. Sonnet is
not authorised for this TZ.

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

**The bench this TZ modifies carries no row in that table**, so its figure is stated
here as the map requires: `bench/backtest_bench.py`, **3240 lines**, MD5
`d2dad0f80afa2c191c2faf1d40081a88`. Report the reading; a difference is a
`## Pre-existing Issues` line, never a reason to adapt the work.

---

## 1. Why this exists — the direction layer has one input and it is the wrong one

Every side this engine publishes comes from `marketRegime`, and `marketRegime` reads one
number: `eff14`, the fourteen-day efficiency ratio, against `EFF_TREND`. **Efficiency
measures SMOOTHNESS, not direction.** A market that climbs with pullbacks — the only kind
that exists — reads `ДИАПАЗОН` while it climbs, and on a `ДИАПАЗОН` word the engine refuses
every directional entry on every coin without a trend of its own. Measured 07.09: BTC sat at
91 % of its ninety-day range, roughly a third above the low of that range, and the word was
`ДИАПАЗОН` on three consecutive runs. **The owner is watching a rising market and reading an
answer with no long in it, and the reason is not caution — it is that the classifier cannot
see a rally that breathes.**

Four revisions of `ANALYST-INSTRUCTIONS.md` in three days each repaired the symptom the
previous one produced. That is the signature of a defect upstream of the methodology, and it
sits in a function the hard floor closes to edits without a completed backtest (item 1). **So
the measurement comes first, and this TZ is it.**

**The second axis is the window, and the owner named it: two to seven days.** The whole
standing result rests on `H_NOISE = 168 h`, where run #16 recorded `P(никуда)` at 69 % long
and 60 % short — two thirds of the engine's decisions never reach either barrier inside the
window they are judged in. A gate judged only at the horizon where most outcomes are missing
has not been judged.

---

## 2. Scope — exactly this, nothing adjacent

1. `bench/backtest_bench.py` — one additive arm, `--regime-gate`, on the existing archive
   machinery. Without the flag every existing mode behaves byte-identically; **this is
   asserted, not claimed** (§6).
2. `bench/backtest_bench.py` — section D of `--lab-selftest` gains **D7**, the known-answer
   control for the new arm.
3. `bench/backtest_guard_bench.py` — offline assertions on the new arm's bar derivation and
   its right-truncation accounting, calling production functions by name and
   re-implementing none of them (inv. 21).
4. `.github/workflows/backtest_bench.yml` — **named explicitly, per hard-floor item 8** —
   gains a `workflow_dispatch` boolean input passing `--regime-gate`. No other change.

**Out of scope, and a TZ deviation if touched:** `index.html`, `main.py`, `catalysts.json`,
`ANALYST-INSTRUCTIONS.md`, any production constant, any scoring, regime or geometry function
(hard-floor item 1), `bench.yml` steps 1–13, and every existing published figure. **No new
dependency, no new data source, no host this bench does not already use.**

---

## 3. The arm

For every archive date the bench already resolves, compute the regime word from the
unmodified `marketRegime` on that date's BTC row, construct the production long and short
setups on every admitted symbol, and resolve each over the grid
`H ∈ {48, 72, 96, 120, 168, 336} h` × `RR ∈ {1.0, 1.5, 2.0, 3.0}` — `RR` setting the target
at `RR × |вход − стоп|` with the stop untouched.

| Reported per cell, per side, per regime word | Note |
|---|---|
| `n` setups and `n_dates` | counts, never estimates (inv. 43) |
| `P_none` | reached neither barrier inside `H` |
| `Ω = n_tgt / n_stop` with CI95 | the block bootstrap the arm already uses — cut it, do not rewrite it (inv. 38) |
| the cell's own bar | **derived at run time**, below |
| `n_dates` lost to right-truncation | below |
| break-even funding rate | below |

**The bar is derived at run time and no numeral for it appears in this TZ or in the code.**
`1/RR_MIN = 0.50` is nominal and the map already records why it is wrong: the admitted set
sits far above `RR_MIN`, mean `1/RR` reading 0.213 long and 0.293 short. **Each cell's bar is
the mean of `1/RR` over its own setups**, exactly as D2 and D3 were re-registered to derive
their objects rather than assert them (inv. 61, inv. 65).

**Right-truncation is accounted or the grid is uninterpretable.** A setup at `H = 336 h`
needs fourteen days of archive after entry, so the tail of the series produces no resolved
setup there and that sample is not the sample at 48 h. Report per cell the dates lost and the
last usable entry date. **A rising `Ω` on a shrinking sample is not a rising `Ω`.**

**Funding is charged in arithmetic because the archive cannot charge it in data.**
Historical funding is a separate dataset and importing it is a new source this TZ does not
authorise. Report per cell the constant eight-hour rate at which the cell's advantage over
the `168 h / RR 2.0` reference is exactly consumed, from the cell's own mean reward and
`FUND_PAY_7D` scaled by `H`.

**Quorum is the one the existing grid already applies**, read from the code, not restated
here (inv. 20). A cell below quorum prints its counts and no `Ω`.

---

## 4. Registration — one primary claim, fixed before the run

**PRIMARY CLAIM.** Partitioned by the regime word `marketRegime` returns on the entry date,
the directional setups admitted on `ДИАПАЗОН` dates resolve **no worse** than those admitted
on trend dates: at every cell clearing quorum, the `ДИАПАЗОН` `Ω` CI95 overlaps or exceeds
the trend `Ω` CI95 on the same side.

**Consequence, registered now (inv. 23):**

- **Claim holds** → the regime word does not separate profitable directional entries from
  unprofitable ones, so the gate that refuses every `ДИАПАЗОН` day is destroying trades
  rather than avoiding losses. The finding opens a production TZ against `marketRegime`
  under hard-floor item 1, which this measurement then satisfies.
- **Claim fails** → the gate is doing its job, `ДИАПАЗОН` days genuinely have nothing, and
  the engine's silence on those days is correct. The methodology stops being edited for it
  and the owner is told plainly that the market, not the engine, is the constraint.

**Registered exploration, at §3.10a's doubled bar (CI99), wiring nothing by itself:** where
`eff14` does not separate the two populations, does **position inside the ninety-day range**
or **fourteen-day relative strength against BTC** — both already carried in `cd`, neither
requiring a new input — separate them? This is the owner's standing request measured rather
than argued, and a positive cell buys a hypothesis for a later TZ, never a production edit.

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

Written by the Architect. Every item runs; an item that cannot run **fails** (contract §9).

1. `python3 -m py_compile bench/backtest_bench.py` and
   `python3 -m py_compile bench/backtest_guard_bench.py` — exit 0.
2. **Byte-identity of the untouched path.** Run `--target` WITHOUT `--horizon-ladder`
   against the pre-change checkout and the post-change checkout on the same cached
   archive; every published figure identical. Report the diff line count, and report `0`
   only if a diff was actually taken.
3. `python3 bench/backtest_bench.py --lab-selftest` — green, check count recorded, delta
   against the baseline count stated.
4. **D7, the known-answer control, and its correct outcome is a REFUSAL.** On the
   driftless world the ladder must reproduce D3's shape — `P_none` decaying monotonically,
   `Ω` rising toward `Σq/Σ(1−q)` — **and must not produce a rung whose CI95 lower bound
   clears its derived bar.** A driftless world has no drift to find; an instrument that
   finds one there is inverted, and every number it produces on the archive is worthless.
   D7 fails on a pass.
5. **Negative test on the guard** (contract §9, CI clause): break the bar derivation in the
   working tree, confirm gate step 14 turns red and names the assertion, revert, confirm
   the tree is clean and the step green. Report both check counts.
6. `bench.yml` steps 1–13 — **delta zero**, replayed against the unmodified checkout
   before any edit and again after, so the zero compares two measurements and not a
   measurement against this document.
7. Step 14 check count before and after, both as measured.
8. **The dispatch.** Run `backtest_bench.yml` with the new input on `main` after merge is
   the Boss's action, not the Executor's; the report states that the input exists, that the
   flag reaches `--target`, and that the workflow file parses. Do not forecast the run
   (inv. 54).
9. Extremes: a rung with zero resolved setups · a rung below quorum · a symbol removed by
   `target_gate` mid-ladder · an archive whose last usable entry precedes the first date at
   the widest rung · a side with no setups at any rung.
10. Explicit no-regression statement covering `index.html`, `main.py`, `catalysts.json`,
    every existing `--target` figure and every `bench.yml` step.

---

## 7. Report

Contract §10 format, to `CryptoReports/TZ-31-horizon-ladder-on-archive-report.md`,
straight to `main`. Fingerprints for the System Map and for every file the map's `## 0`
table lists, read from that table at authoring time. The implementation waits on a branch.
