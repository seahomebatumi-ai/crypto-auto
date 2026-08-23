# TZ-13 — Live wiring of the exhaustion measure, and the threshold re-registered on the list median

**Canonical filename: `TZ-13-live-exhaustion-and-median-calibration.md`.** Commit
the file under exactly this name in `CryptoTZ/`, taken from this line and never
from the name the artifact arrived under.

**Model: Opus.** A production edit with a no-regression obligation across four
benches, plus a statistical instrument whose admissibility rule is derived in-run.
Not a mechanical edit.

---

## 0. Fingerprint gate — compare BEFORE any work

Run `git fetch --all --prune` first. Compare against `origin/main`, never local
`main`. A mismatch on any row is **ЗАБЛОКИРОВАНО**: stop, report, do nothing else.

| Anchor | Exact string that must be present in `SYSTEM-MAP-CRYPTOCALCUL.md` |
|---|---|
| revision | `**Revision 2026-08-23-c.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `48. **A bench that builds its own input proves the function, not the wiring.**` |

Baseline files at this revision:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3656 | `64acaaa59f2ed96d568714d2813d20f9` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |

Gate baseline: `bench.yml`, 12 steps, **1 250 354** checks, measured from a
`git worktree` at `origin/main`, never assumed.

Check the clone for truncation (`git rev-parse --is-shallow-repository`) and
deepen before assessing anything historical.

---

## 1. Why this exists

**Defect 1 — the measure is dead on the live board, and twelve green gate steps
say nothing about it.** `listExhaustion` reads `row.hi24`, `row.lo24` and
`row.cur`. The row object built in `update()` carries none of the three: the
render loop parses those ticker fields into LOCALS inside its `sideOn` branch and
hands them positionally to `directionVerdict`. Live, the function returns
`{median: null, n: 0}` on every render; §3.17's list line prints «список не
измерен: своя мера есть у 0 монет» beneath a caption that states the list is
computed over 25 spot coins. Both gate steps that exercise `listExhaustion` build
their own rows in the contract's shape and pass. This is inv. 48.

**Defect 2 — no threshold exists, because the registered rule measured the wrong
random variable.** TZ-11 calibrated the pooled 90th percentile of the COIN-DAY
distribution and compared it to a window drawn around that same object;
`listExhaustion` thresholds the LIST MEDIAN, whose upper tail is materially lower
because averaging correlated members strips idiosyncratic dispersion (inv. 47).
The run returned 1.59 against a floor of 1.60, the script exited non-zero, and
nothing was adopted — correctly. The floor itself was wrong before any data
existed.

The two are independent and both belong here: the first makes the estimator reach
the screen, the second gives its output a scale. **Neither adopts a constant and
neither builds a consumer.** That is the TZ after this one, and by then the number
will already have been decided by the rule registered below.

---

## 2. Scope — three stages

### Stage A — the row contract, one parse site per quantity

In `update()`'s token loop, immediately after the `nopair` early return and before
the dead-market test, three assignments:

```
var row = { t: t, idx: idx, coin: coin, cd: null, state: 'ok', sc: null };
if (!coin) { row.state = 'nopair'; rows.push(row); return; }

row.cur  = parseFloat(coin.lastPrice);
row.hi24 = parseFloat(coin.highPrice);
row.lo24 = parseFloat(coin.lowPrice);
```

They are assigned for **every** row that has a ticker, `fut:true` included. The
venue rule lives in `listExhaustion` and nowhere else (inv. 41): a row filtered at
the assignment site would put the declaration in two places.

**Every existing consumer of those three quantities then reads the row, and the
`parseFloat` disappears from its old site.** Exactly one site may parse each of
`lastPrice`, `highPrice`, `lowPrice` per row after this stage:

| Site | Before | After |
|---|---|---|
| `update()`, `sideOn` branch | `var curP = parseFloat(coin.lastPrice)` and the same for `hi24`, `lo24` | reads `row.cur`, `row.hi24`, `row.lo24` |
| `boardHtml`, header | `var cur = parseFloat(coin.lastPrice)` | `var cur = row.cur` |
| `boardHtml`, §3.17 row 2 | `dayRangeRatio(parseFloat(coin.highPrice), parseFloat(coin.lowPrice), cur, …)` | `dayRangeRatio(row.hi24, row.lo24, cur, …)` |

Values are identical on both sides of every row of that table, so **no board and
no verdict may move because of Stage A.** The only thing that changes is that
`listExhaustion(lastRows)` now finds what it reads.

`coin.priceChangePercent` and `coin.quoteVolume` are **not** touched: they are not
read by `listExhaustion` and widening the edit buys a diff and nothing else.

**Fixture updates in existing benches are AUTHORISED by this TZ and are not «a
bench edited to make it pass».** The row contract changed, so a fixture that
builds a row must build the new one. The constraint is exact: a fixture sets
`row.cur` / `row.hi24` / `row.lo24` from the SAME ticker object it already carries
(`lastPrice` / `highPrice` / `lowPrice`), never from a new number. Any expectation
string may be updated only where the list line legitimately moves — enumerated per
§5 item 4.

### Stage B — the wiring check that would have caught it (inv. 48)

New section in `bench/exhaustion_bench.js`, inside the gate.

1. Cut `listExhaustion` out of `index.html` by brace matching and collect every
   field it reads off its row argument, from the SOURCE: `row.<ident>`, plus the
   second level where the source reads one (`row.t.fut`).
2. Cut `update()` out of `index.html` the same way and collect every field the row
   object receives there: the keys of the `var row = { … }` literal plus every
   `row.<ident> =` assignment in that function body.
3. Assert set inclusion: every field read is a field written. Failure names the
   missing fields.
4. One check per field read. **Zero reads or zero writes is a failure, not a
   pass** (inv. 22).
5. **Positive control (inv. 23).** The same extractor, run over a copy of the
   source with one producing assignment deleted, must report exactly that field
   missing; run over a copy with one extra read added, must report that one. A
   checker that cannot fail is not a check.

The mechanism is written so a second reader can be added by naming it, but only
`listExhaustion` is wired in this TZ.

### Stage C — the calibration, re-registered on the list median

`bench/exhaustion_calib.py`. Not in `bench.yml`; it runs through `calib.yml`,
unchanged, on a runner (inv. 24, inv. 44). **No fetch happens in the
implementation session.**

**C1 — the object.** The unit becomes a DATE, not a coin-day. `coin_days` returns
its day key with every tuple; days are joined across the spot universe by that
key, and for each date the script builds row objects in production's own contract

```
{ t: {name: SYM, fut: false}, cd: {volatility: vol}, hi24: hi, lo24: lo, cur: cur }
```

and calls **production's `listExhaustion`** through the existing node hop.
`JS_CUT` becomes `["has", "sigmaDay", "dayRangeRatio", "listExhaustion"]`. The
median, the count and the quorum are production's; Python computes no median
anywhere, in any form (inv. 21, inv. 38(1)). Dates below quorum return `null` and
drop out, and the number of such dates is reported.

**C2 — the statistic. Unchanged: the 90th percentile**, numpy linear
interpolation, rounded to two decimals. The object was wrong, not the statistic;
changing both after a failure would be fitting.

**C3 — the null, simulated in the same run.** Its only purpose is to give the
admissibility window an object instead of a guess.

- The ratio is scale-free in each coin's own σ, so the law of a date's median
  under the null depends on exactly two things: **how many coins contributed that
  date, and how tightly they move together.** Dates sharing an `n` share a law and
  may be pooled.
- **ρ is measured, not assumed:** for each date, the mean pairwise Pearson
  correlation of hourly returns over the same trailing 90-day window the
  volatility comes from, across that date's contributing coins. Each date's null
  is simulated at its own ρ through a single common factor. The distribution of
  ρ over dates is printed.
- **The simulated day must be a CONTINUOUS-time range.** The archive's hourly
  candles carry true intra-hour extremes, so a null built from 24 hourly closes
  understates the range by roughly 16 % and would move the window in the dangerous
  direction. Method is the Executor's call; the control below decides whether it
  is right.
- The ratio in the null is formed by **production's `dayRangeRatio`** from the
  simulated path's own high, low and last value — the same denominator, the same
  null handling, the same node hop.
- The sampling error of the 90-day σ estimate belongs in the null. Simulating 90
  days of history per replica is not required: a multiplicative factor with the
  standard deviation of a variance estimator on the same number of hourly
  observations is admissible, and the record states which was used.
- **Replica count is set by precision, not by taste:** enough that the
  Monte-Carlo standard error of the null p90 is **below 0.01**. The script prints
  that standard error and **fails if it exceeds 0.01**. Wall-clock budget for the
  null: 20 minutes on the runner. Seed fixed and recorded.

**C4 — the known-answer control (inv. 23), offline, inside `--selftest`, run
BEFORE the archive is touched.** For a driftless walk `E[range] = σ·√(8T/π)`
exactly, so at a σ small enough for the price-scale term to vanish
(`σ_day = 0.5 %`), the pooled mean of single-coin simulated ratios must read
**1.000 ± 0.005** over at least 10⁶ coin-days. A path discretised at hourly steps
reads ≈ 0.84 and at minute steps ≈ 0.97, so this control detects the exact error
it exists to catch. It fails the run, not a warning.

**C5 — the admissibility rule, registered here, before the number
(inv. 23, 47).** Adopt

```
DAY_RANGE_ABNORMAL = p90( per-date list medians ), rounded to 2 dp
```

if and only if all four hold, each printed with its own PASS / FAIL line:

| # | Condition | What it protects |
|---|---|---|
| 1 | pooled mean of the empirical COIN-DAY ratios within ±15 % of the null's pooled coin-day mean | a mis-scaled σ or a mis-scaled `√(8/π)` — the estimator measuring something other than «a diffusive day» |
| 2 | empirical p90 of the date medians **strictly above** the NULL p90 of the date medians | a constant a quiet market reaches at least a tenth of the time is not a threshold |
| 3 | empirical p90 **strictly below** the null p99.9 | broken-pipeline guard only. Above it the answer is a new TZ, never a nudged number |
| 4 | at least 300 dates with a median, and a median per-date contributing count of at least 15 | a percentile over a handful of dates is not a percentile (inv. 22) |

**No numeric band appears anywhere in the script.** Conditions 2 and 3 are read
off the null computed in the same run; that is the entire correction over TZ-11,
where a hand-written floor sat above the p95 of the very distribution it was
supposed to bound. Any FAIL → non-zero exit, no constant, no production change,
and the answer is a new TZ.

**C6 — the record.** `bench/exhaustion-calibration.txt`, committed by `calib.yml`
(inv. 46). It carries: the universe and per-coin coverage; the date count and the
distribution of per-date contributing counts; the ρ distribution; the seed, the
replica count and the null-p90 Monte-Carlo standard error; the null deciles plus
p95 / p99 / p99.9; the empirical deciles of the date medians; the empirical pooled
coin-day mean; the ten highest dates by list median, with their dates; the four
admissibility lines; and the constant on **exactly one machine-readable line** of
the form `DAY_RANGE_ABNORMAL = X.XX`, because a later bench must compare a source
constant against this file without parsing prose.

---

## 3. Non-goals — do not do these

- **Nothing is adopted.** `DAY_RANGE_ABNORMAL` does not enter `index.html`,
  `abnormal` stays hardcoded `false`, `reg.day` stays unreferenced, and no
  threshold, colour, or word like «аномально» appears on any surface.
- **§3.17 is not redesigned.** Its rows, wording and order are TZ-12's; Stage A
  changes where two numbers come from, not what is printed.
- **The 1.59 result is not touched**, not re-run at another depth, not rounded,
  not carried into the new rule as a prior. It was measured on a different random
  variable and says nothing about this one.
- **`marketRegime`, `regimeBanner`, the leverage engine, «ЦЕНА ВРЕМЕНИ», «ЗАЩИТА
  ПОЗИЦИИ», the four ceilings, `LIQ_MMR` and `L_CAP` are not modified.**
- **No new constant anywhere** (inv. 20); no ranking factor; no `scoreCandidate`
  change; no new external data source.
- **`main.py`, `catalysts.json`, `journal/**` and `.github/workflows/**` are not
  touched.** `calib.yml` already triggers on a push touching
  `bench/exhaustion_calib.py`; if it does not fire, report that — do not edit it.
- **No bench is edited to make it pass.** Fixture updates are authorised only in
  the exact form §2 Stage A defines.

---

## 4. Files

| Path | Change |
|---|---|
| `index.html` | three row assignments in `update()`; consumers rerouted to them in `update()` and `boardHtml` |
| `bench/exhaustion_bench.js` | the inv. 48 wiring section and its positive control |
| `bench/exhaustion_calib.py` | rewritten to the date/list-median object, the measured-ρ null, the known-answer control and the derived admissibility rule |
| `bench/exhaustion-calibration.txt` | written and committed by the `calib.yml` runner |
| existing benches carrying row fixtures | row shape only, per §2 Stage A |
| `CryptoReports/TZ-13-live-exhaustion-and-median-calibration-report.md` | new, straight to `main` |

ES5 only in `index.html`: `var`, string concatenation, no arrow functions, no
template literals. Every on-screen Russian string is `\uXXXX`-escaped.

---

## 5. Validation — written by the Architect, run by the Executor

The Executor runs these and reports results; it does not design them, add to
them, or mark any item «not applicable».

1. `python3 -m py_compile main.py`; `node --check` on the extracted `<script>`;
   ES5 guard and Cyrillic guard over every added line, each reporting how many
   lines it checked and failing on zero.
2. **Stage A, one parse site.** Grep the whole of `index.html` for
   `lastPrice`, `highPrice` and `lowPrice` and report every remaining occurrence
   with its line and function. Exactly one parse site per field per row must
   survive; any other occurrence is named and justified.
3. **Stage A, the measure reaches the list.** Build a row set the way `update()`
   builds it — 25 spot tickers plus the three `fut:true` — through the assignment
   sequence taken from the source, and report `listExhaustion` over it: `n` must
   be 25 and `median` a number. Then the same with one ticker missing
   `highPrice`, and with only three spot rows, and report both.
4. **Stage A, no-regression.** Whole boards against `origin/main` across the
   `prot_bench.js` scenario set and every extreme in item 9. Every board must be
   **byte-identical** except where the scenario's `lastRows` legitimately yields a
   different `listExhaustion` result; each such case is enumerated with its before
   and after list line and the reason. A board differing anywhere else is a
   finding. Identity first (inv. 45): the differ reports zero on identical input
   before any of this is offered as evidence.
5. **Stage B, the negative controls.** Delete one producing assignment → the
   wiring section fails and the step exits non-zero, naming that field; add one
   read → likewise. Restore and verify by MD5 against the pre-control copy.
6. **Stage C, offline.** `--selftest` in full: the known-answer control at
   `σ_day = 0.5 %` with its measured mean and tolerance; proof that the median and
   the quorum come from production's `listExhaustion` and not from Python (a
   fixture whose median is known by construction, plus evidence the node hop was
   taken); the admissibility gate refusing a synthetic value below the null p90
   and one above the null p99.9; nulls surviving the JSON hop as nulls, never as
   zeros.
7. **Stage C, the run.** On the runner, through `calib.yml`. Report the workflow
   run id and URL, the wall clock, and the record file **verbatim in the report**.
   If any admissibility condition fails, that is the outcome: report it, adopt
   nothing, and do not re-run at a different depth or seed to obtain another
   number.
8. **Full gate, 12 steps, every step exit 0.** Baseline and candidate counts per
   step against a `git worktree` at `origin/main`, delta explained term by term.
   Baseline total must reproduce **1 250 354**. Step 7 is content-sensitive: if it
   moves, attribute the move field by field.
9. **Extremes**, unchanged from the release checklist: slider edges, null betas,
   truncated Gist, HTTP 400 ticker, dead-market fields, missing coeffs fields,
   absent `btcStats`, absent `volatility`, `E ≤ 0`, non-finite `liq`.
10. **Release checklist item 15** (map §6): the list line names a coin count that
    matches the spot rows on screen and never zero.

---

## 6. Pre-existing issues

Report anything found and **do not fix it.** Three are already known and need no
new investigation: `NaN% от входа` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ», the raw
Cyrillic literal at `bench/prot_bench.js:166`, and the Node 20 action pin. Name
anything else in its own section.

---

## 7. Report

`CryptoReports/TZ-13-live-exhaustion-and-median-calibration-report.md`, straight
to `main`, branch left unmerged. State line counts and MD5 for
`SYSTEM-MAP-CRYPTOCALCUL.md`, `index.html`, `main.py` and `catalysts.json`, the
per-step gate table with the delta explained term by term, the enumerated board
differences from item 4, and the calibration record in full.

Note that `calib.yml` commits the record back to the branch with `[skip ci]`:
pull before any further commit.

**NOT IN EFFECT UNTIL MERGED.**
