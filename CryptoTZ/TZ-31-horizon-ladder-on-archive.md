# TZ-31 — Horizon ladder on the archive

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

## 1. Why this exists

Every standing result about the target — `Ω` 0.025 long and 0.016 short against the bar
`1/RR_MIN = 0.50`, no `k*` anywhere in the continuation grid, the whole §3.12 veto — was
measured at **one horizon**, `H_NOISE = 168 h`, and at that horizon the map's own run #16
records `P(никуда)` at **69 % long and 60 % short**. Two thirds of the engine's decisions
never reach either barrier inside the window they are judged in, so `Ω` is computed on the
minority that resolve and is truncated far below its untruncated value. The map says this
in one line already: **the target was never the binding constraint — the horizon is.**

The instrument for the question exists and has never been pointed at real data. Section D3
of `--lab-selftest` already walks `H = m·H_NOISE`, `m ∈ {1, 4, 8, 16, 32}`, and on the
driftless world reads `P_none` 0.639 → 0.304 → 0.154 → 0.055 → 0.000 with `Ω`
0.026 → 0.146 → 0.213 → 0.250 → 0.293. **That ladder runs on a synthetic world only.** This
TZ runs the same ladder on the three-year archive, on the production arm, and nothing else.

**What the answer is worth, stated before it is known.** On a driftless walk `Ω` converges
to the reciprocal of the realized R:R exactly — that is the theorem inv. 32 rests on, and
D3's convergence to `Σq/Σ(1−q)` is it arriving. So a rung whose `Ω` merely APPROACHES its
bar has measured the absence of edge at a longer horizon, which is a real finding and closes
the question. A rung whose `Ω` clears its bar with the CI95 lower bound above it has measured
drift the seven-day truncation was hiding. Both outcomes are usable; neither is assumed.

---

## 2. Scope — exactly this, nothing adjacent

1. `bench/backtest_bench.py` — one additive arm on the existing `--target` mode,
   selected by a new flag `--horizon-ladder`. Without the flag `--target` behaves
   byte-identically to today; **this is asserted, not claimed** (§6).
2. `bench/backtest_bench.py` — section D of `--lab-selftest` gains **D7**, the
   known-answer control for the new arm.
3. `bench/backtest_guard_bench.py` — assertions on the new arm's bar derivation and its
   right-truncation accounting, offline, calling the production functions by name and
   re-implementing none of them (inv. 21).
4. `.github/workflows/backtest_bench.yml` — **named explicitly, per hard-floor item 8** —
   gains a `workflow_dispatch` boolean input that passes `--horizon-ladder` through to the
   existing `--target` invocation. No other change to that file.

**Out of scope, and a TZ deviation if touched:** `index.html`, `main.py`,
`catalysts.json`, `ANALYST-INSTRUCTIONS.md`, any production constant, any scoring or
geometry function (hard-floor item 1), `bench.yml` steps 1–13, and every existing
`--target` number. **No new dependency, no new data source, no network host not already
used by this bench.**

---

## 3. The arm

For each rung `m ∈ {1, 2, 4, 8, 16}`, on the production arm, per side, on the same cached
archive and the same symbol set `target_gate` already admits:

| Reported per rung, per side | Note |
|---|---|
| `n` setups and `n_dates` | counts, never estimates (inv. 43) |
| `P_none` | fraction reaching neither barrier inside `m·H_NOISE` |
| `Ω = n_tgt / n_stop` with CI95 | the same block bootstrap the arm already uses — cut it, do not rewrite it (inv. 38) |
| the rung's own bar | **derived at run time**, see below |
| `n_dates` lost to right-truncation | see below |
| break-even funding rate | see below |

**The bar is derived at run time and no numeral for it appears in this TZ or in the code.**
`1/RR_MIN = 0.50` is the nominal bar and the map already records why it is the wrong one:
the admitted set sits far above `RR_MIN`, mean `1/RR` reading 0.213 long and 0.293 short, so
0.50 was generous by about a factor of two. **Each rung's bar is therefore the mean of
`1/RR` over the setups in that rung**, computed from the arm's own rows, exactly as D2 and
D3 were re-registered to derive their objects instead of asserting them (inv. 61, inv. 65).
A rung is compared against its own bar and against nothing else.

**Right-truncation is accounted or the ladder is uninterpretable.** A setup at `m = 16` needs
2688 h of archive after its entry, so the last ~112 days of the series produce no resolved
setup at that rung and the sample is not the sample at `m = 1`. Report per rung the number of
dates lost this way and the date of the last usable entry. **A rising `Ω` across a shrinking
sample is not a rising `Ω`**, and a report that does not let the reader see the shrinkage has
not delivered the measurement.

**Funding is charged in arithmetic because the archive cannot charge it in data.** Historical
funding is a separate Binance dataset and importing it is a new data source, which this TZ
does not authorise. Instead report per rung the **break-even funding rate** — the constant
8-hour rate at which the rung's advantage over `m = 1` is exactly consumed, computed from the
rung's own mean reward and `FUND_PAY_7D` scaled by `m`. Pure arithmetic on numbers already in
hand, and it stops a longer horizon from winning for free.

**Quorum is the one the existing grid already applies**, read from the code, not restated
here (inv. 20). A rung below quorum prints its counts and no `Ω`.

---

## 4. Registration — one primary claim, fixed before the run

**PRIMARY CLAIM.** On the production arm, over the rungs that clear quorum, `Ω(m)` is
non-decreasing in `m`, **and** there exists a rung whose `Ω` CI95 lower bound sits at or
above that rung's own derived bar.

**Consequence, registered now (inv. 23):**

- **Claim passes** → the smallest such rung is the measured trade horizon, and the finding
  routes to an Architect edit of `ANALYST-INSTRUCTIONS.md` §4, where the target's
  reachability is currently measured at `H_NOISE`. **Nothing crosses into `index.html`
  from this TZ under any outcome** — `H_NOISE` governs the leverage ceilings and does not
  move here.
- **Claim fails** → the horizon is not the lever either. The engine's product is entry
  timing and risk control, the target is a bookkeeping level, and the §3.12 veto stands
  unchanged. This is a finding, not a failure of the work.

Everything else the arm prints is **exploration** and answers to §3.10a's doubled bar
(|effect| at CI99). No exploration cell wires anything anywhere.

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
