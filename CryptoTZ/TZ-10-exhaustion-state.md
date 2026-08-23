# TZ-10 — List-level exhaustion state in the regime banner

**Canonical filename: `TZ-10-exhaustion-state.md`.** The Executor commits the file
under exactly this name, taken from this line and never from the name the file
arrived with.

**Model: Opus.** Multi-file, touches a production display path plus a bench plus a
calibration run over the archive; a wrong constant here is a silent, permanent
mis-statement on the one list-level element on screen.

## Fingerprint gate

Compare against the repository copy of `SYSTEM-MAP-CRYPTOCALCUL.md` BEFORE any
work. Any mismatch → **ЗАБЛОКИРОВАНО**, report and stop.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-22-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| newest invariant | `43. **A check count must be a count.**` |

Baseline: TZ-09 merged (PR #9, `ae47103`). `index.html` 3522 lines, MD5
`68eebc9b5e40c7afd09a7d00d3fd1d21`.

---

## 1. The defect this closes

On 2026-08-22 the journal recorded a session in which the geometry layer refused
**24 of 25 covered coins**, and the single loudest list-level element on the
screen — `regimeBanner` — printed

> ТРЕНД ВВЕРХ — счёт по каналу импульса

in **green**.

The regime label was correct: `eff = 2.37`, `z = 4.01`, `mode = 'trend'`,
`dir = +1`. What the label did not say is that BTC's weekly move was **four
standard deviations**, that BTC sat at **94.2 %** of its own 90-day range, and
that the day-range across the covered list ran far outside anything diffusive:

| Statistic, 2026-08-22, 25 covered coins | Value |
|---|---:|
| median (hi24 − lo24) / (cur · σ_day · √(8/π)) | **2.43** |
| coins above 2.0 | 20 / 25 |
| coins that closed in the lower half of their own day range | 18 / 25 |
| coins the geometry layer allowed | 1 (`GRAM`, and the **lowest** ratio in the list at 1.34) |

`marketRegime` already computes `z` and `eff` and throws both away for display
purposes. The banner names a state without naming how far into it the market
sits, so on the single worst buying session of the quarter the one list-wide
signal read as encouragement.

**Nothing predictive is being added.** This is a measurement of what the session
already did, in the same spirit as §3.12 Layer 1: it asserts «the geometry of
entering right now is bad», which is measurable without a forecast. No ranking
factor is introduced, no weight is touched, and §3.10b's resolution ceiling is
untouched.

---

## 2. Scope — exactly three changes, in this order

### Stage A — the measure, with no consumer

Add to `index.html`, next to `sigmaDay` (line ~1246):

```
// Day range against the range a driftless walk would produce over the same
// day. E[range] = sigma * sqrt(8/pi) for Brownian motion, so the denominator
// is derived, not chosen. sigma is close-based and therefore understates true
// range: the typical reading is ABOVE 1 by construction and the acting
// threshold is calibrated in Stage B, never guessed.
function dayRangeRatio(hi, lo, cur, vol) { ... }
```

Rules:

- Uses `sigmaDay(vol)` — the existing single site (inv. 20). It must not
  recompute `vol * Math.sqrt(24)`.
- Returns `null` on any missing / non-finite input, on `cur <= 0`, and on
  `hi <= lo`. A null must never become a zero.
- ES5 only. `Math.sqrt(8 / Math.PI)` written once, inside this function.
- No consumer in Stage A. Nothing on screen changes.

Also add, in the same stage:

```
function listExhaustion(rows) -> { median: <number|null>, n: <int>, abnormal: <bool> }
```

- Takes the assembled row list, reads each row's already-parsed `hi24`, `lo24`,
  `cur` and `cd.volatility`, and calls `dayRangeRatio` per row.
- `n` counts rows that produced a non-null ratio; rows with no metrics, no pair
  or a dead market contribute nothing and are not counted.
- `median` is `null` and `abnormal` is `false` when `n < 8`. A verdict on the
  list computed from three coins is not a verdict on the list.
- It is a separate named function precisely so a bench can call it (same reason
  `byScore`, `assignRanks`, `stateMark` are separate — inv. 34).
- `abnormal` is left permanently `false` in Stage A; the comparison is wired in
  Stage C.

### Stage B — calibrate the constant from the archive

Add `bench/exhaustion_calib.py`, run once, output recorded in the report.

- Data: `data.binance.vision` monthly hourly ZIPs, the same path and the same
  cache `backtest_bench.py` already uses. **No new dependency, no new host**
  (inv. 24 — only `data.binance.vision` / `data-api.binance.vision` answer from
  a runner).
- Universe: the 25 spot pairs from the frontend's `tokens[]`. The three
  `fut:true` assets are excluded by declaration, not by observation (inv. 41),
  and the report states the coverage as 25 of 28.
- **`dayRangeRatio` and `sigmaDay` are CUT OUT of `index.html` at runtime and
  executed with node** — no second implementation in Python, in any form
  (inv. 21, inv. 38(1)).
- Per coin-day: `hi`/`lo` from that day's 24 hourly candles, `cur` = the day's
  last close, `vol` = the trailing 90-day hourly volatility computed by the same
  path `backtest_bench.py` already uses.
- Output: n, the full decile table, and the **90th percentile of the pooled
  distribution**.

**The rule is registered here, before the number is known (inv. 23):**

> `DAY_RANGE_ABNORMAL` = the pooled 90th percentile, rounded to two decimals,
> taken as-is. It is not moved to make 2026-08-22 fire, not moved to make any
> other date fire or not fire, and never retuned afterwards. If the pooled 90th
> percentile lands below 1.60 or above 4.00 the stage is **ЗАБЛОКИРОВАНО** and
> reported without a production change — a threshold outside that window means
> the measure is not measuring what this TZ claims, and the answer is a new TZ,
> not a nudged number.

The window is stated in advance and is deliberately wide: it exists to catch a
broken pipeline, not to steer the value.

### Stage C — one production consumer, and only one

1. Add to the constants block (§3 of the map, the single-site block):
   `DAY_RANGE_ABNORMAL <value from Stage B>`.
2. `listExhaustion` sets `abnormal = median >= DAY_RANGE_ABNORMAL`.
3. `update()` calls `listExhaustion(rows)` ONCE per render and attaches the
   result to the already-computed `reg` object as `reg.day` before
   `regimeBanner` is called. `marketRegime` itself is not modified.
4. `regimeBanner(reg, isLong)` stays a pure namer — **it computes nothing**
   (existing contract, inv. 15). When `reg.day && reg.day.abnormal` it:
   - appends ` · ДЕНЬ АНОМАЛЬНЫЙ — вход только по откату` to the existing text;
   - forces the colour to amber (`#e0a02a`), overriding green in the
     trend-matching case and overriding `var(--accent)` in range. **Red is not
     used** — an abnormal session is not stress, and `stress` must keep its own
     red exclusively (existing branch, unchanged).
   - In the `stress` branch the text is appended but the colour stays red:
     stress is the stronger statement and must not be softened.
5. Nothing else consumes it. Not `scoreCandidate`, not `tradeGeometry`, not
   `leverageDecision`, not `directionVerdict`, not the journal writer. The
   measure is display-only at this revision (inv. 27 pattern).

**Russian on-screen strings are written as `\uXXXX` escapes.**

---

## 3. Non-goals — do not implement, do not propose in the report

These were considered by the Architect and decided against for this revision.
The Executor implements none of them and does not raise them again inside this
TZ.

- No composite 0–100 «squeeze» score.
- No open-interest input, live or archived.
- No liquidation-imbalance input.
- No funding-extreme input.
- No per-coin badge, no per-coin score, no new card row, no new board block.
- No new `wait` state and no change to `ENTRY_CHASE_SD`: entry discipline
  already anchors a long to `lo24` and a short to `hi24`, and a second entry
  gate on a fresh constant is exactly what inv. 20 exists to prevent.
- No change to any leverage ceiling. §7 rejected crediting a measured 0.88
  calibration into the calculation; an uncalibrated haircut is strictly worse.
- No journal schema change. `px.hi`, `px.lo`, `px.cur` and `cd.volatility` are
  already recorded in every snapshot, so every journaled day is already
  reconstructible and inv. 38(2) is not touched.

---

## 4. Files

| File | Change |
|---|---|
| `index.html` | `dayRangeRatio`, `listExhaustion`, one constant, `regimeBanner` text/colour, one call site in `update()` |
| `bench/exhaustion_bench.js` | new, wired into `bench.yml` |
| `bench/exhaustion_calib.py` | new, manual, NOT wired into `bench.yml` (one-shot calibration, not a control) |
| `.github/workflows/bench.yml` | one step added |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | Architect-authored, delivered separately — the Executor does not edit the map |

No change to `main.py`, `catalysts.json`, `journal/**`.

---

## 5. Validation — written by the Architect

The Executor runs these and does not design them.

1. `node --check` on the extracted `<script>`; `python3 -m py_compile` on the new
   Python file.
2. `bench/exhaustion_bench.js` — cuts `dayRangeRatio`, `sigmaDay` and
   `listExhaustion` out of `index.html` and executes them (inv. 21). Counted
   comparisons at the comparison site (inv. 43), non-zero exit on any failure,
   non-zero exit on zero comparisons (inv. 22). Cases:
   - **Identity.** On a known input set, `dayRangeRatio` equals
     `(hi − lo) / (cur · vol · √24 · √(8/π))` to 1e-12, over ≥ 200 000 random
     finite inputs.
   - **Nulls.** `vol` null / 0 / NaN / negative, `cur` 0 or negative, `hi < lo`,
     `hi === lo`, any argument undefined → `null`, never `0`, never `Infinity`.
   - **Median and quorum.** `listExhaustion` on hand-built row lists: even and
     odd `n`; rows with null ratios excluded from both `median` and `n`;
     `n < 8` → `median === null` and `abnormal === false` regardless of the
     values present.
   - **Threshold edge.** `median` exactly equal to `DAY_RANGE_ABNORMAL` → fires
     (`>=`, stated here so it cannot drift).
   - **Banner.** `regimeBanner` for all four `mode` values × `abnormal` true and
     false × `isLong` true and false = 16 cases: text contains the exhaustion
     clause if and only if `abnormal`; colour is amber in `trend`/`range`/unknown
     when `abnormal`, red in `stress` regardless, and byte-identical to today's
     output in all eight `abnormal === false` cases.
   - **Purity.** `regimeBanner` called twice with the same frozen `reg` returns
     an identical string and does not mutate `reg`.
3. **Replay on the live journal.** Read `journal/data/2026-08-21.jsonl` and
   `2026-08-22.jsonl` from the checkout, feed the recorded `px.hi`, `px.lo`,
   `px.cur`, `cd.volatility` into the extracted production functions, and print
   the median per date. The report states both numbers and whether each date
   fires. **This is a measurement, not a check** (inv. 43) and is counted
   separately from the check total.
4. **No-regression statement, explicit.** The report must state, with the
   evidence that establishes it, that with `abnormal === false` the rendered
   board is byte-identical to `main`, and that no output of the new code reaches
   `scoreCandidate`, `tradeGeometry`, `leverageDecision`, `directionVerdict` or
   the journal writer.
5. Full `bench.yml` gate green, 12 steps, with the new check total stated as a
   sum of per-comparison counters and the delta against 965 665 explained term
   by term (inv. 43).
6. Extremes, unchanged obligations: truncated Gist, HTTP 400 ticker, dead-market
   fields, missing coeffs fields, `btcStats` absent (`reg.known === false` → the
   exhaustion clause may still attach; that combination is in the 16 banner
   cases above).

---

## 6. Report

`CryptoReports/TZ-10-exhaustion-state-report.md`, straight to `main`, stating:

- line counts and MD5 for `index.html`, `main.py`, `catalysts.json` and the
  System Map;
- the Stage B decile table, `n`, and the chosen `DAY_RANGE_ABNORMAL`;
- the two journal replay medians;
- the gate total with the term-by-term delta;
- the no-regression statement of §5.4.

Implementation waits on a branch. The pull request is not merged before the
Architect's verdict.
