# TZ-12 — Regime stress symmetry, venue-correct list exhaustion, and the «РИСК ВЫНОСА» board block

**Canonical filename: `TZ-12-stress-symmetry-and-squeeze-block.md`.** Commit the
file under exactly this name in `CryptoTZ/`, taken from this line and never from
the name the artifact arrived under.

**Model: Opus.** Multi-site edit inside `index.html`, a behavioural change to the
direction engine, and a new board block whose arithmetic reuses production
formulas. Not a mechanical edit.

---

## 0. Fingerprint gate — compare BEFORE any work

Run `git fetch --all --prune` first. Compare against `origin/main`, never local
`main`. A mismatch on any row is **ЗАБЛОКИРОВАНО**: stop, report, do nothing else.

| Anchor | Exact string that must be present in `SYSTEM-MAP-CRYPTOCALCUL.md` |
|---|---|
| revision | `**Revision 2026-08-23-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| newest invariant | `47. **A threshold is calibrated on the distribution of the quantity its consumer compares.**` |

Baseline files at this revision:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3569 | `56af2e274e5568527a6bb0e5cb4e3456` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |

Gate baseline: `bench.yml`, 12 steps, **1 185 871** checks, measured from a
`git worktree` at `origin/main`, never assumed.

Check the clone for truncation (`git rev-parse --is-shallow-repository`) and
deepen before assessing anything historical.

---

## 1. Why this exists

Three defects, all specification-level, all independent of the blocked
`DAY_RANGE_ABNORMAL` work:

1. **The regime layer has no upper stress branch.** `marketRegime` raises
   `stress` on `z <= -REG_STRESS_Z` and has no mirror. On 2026-08-21 and
   2026-08-22 BTC's weekly move measured `z` = +4.06 and +4.01 — four sigmas of
   one-week movement — and the banner printed `«ТРЕНД ВВЕРХ — счёт по каналу
   импульса»` in green while geometry refused 24 of the 25 covered coins. A
   four-sigma week makes both sides dangerous, and the layer that exists to say
   so says nothing.

2. **`listExhaustion` does not read the venue declaration.** It pools every row
   carrying a `cd`, so live it would compute over 28 rows while every calibration
   and every journal replay covers the 25 spot assets. The three `fut:true`
   assets take their range from the perpetual and their `volatility` from a spot
   index (§3.14 Consequence 3): including them makes the live estimator a
   different estimator (§3.16, inv. 41, inv. 47).

3. **The day-range measure reaches nothing.** §3.16 was built to close the gap
   «the banner names the regime and never says how far into it the session
   already sits». The measure exists, was proven on a runner, and no surface
   reads it.

This TZ closes 1 and 2 outright, and closes 3 **as a measurement only**: the
number is printed, no threshold is applied. That distinction is load-bearing and
is restated in §3.

---

## 2. Scope — four stages

### Stage A — symmetric regime stress

In `marketRegime`, one comparison:

```
BEFORE:  if (v >= VOL_HARD || (out.z !== null && out.z <= -REG_STRESS_Z)) {
AFTER:   if (v >= VOL_HARD || (out.z !== null && Math.abs(out.z) >= REG_STRESS_Z)) {
```

No new constant. `REG_STRESS_Z` stays the single site (inv. 20). `out.dir` is
**not** touched: it stays 0 under stress, because §3.12 reads `dir` only on
`trend` and setting it under stress would hand a direction to a state that admits
neither side.

In `regimeBanner`, the `stress` branch gains one clause chosen by the sign of
`reg.z`, colour unchanged (`var(--red)`) in both:

```
reg.z !== null && reg.z >= REG_STRESS_Z
    -> 'РЫНОК ПЕРЕГРЕТ — сделок нет ни на одной стороне'
otherwise
    -> 'СТРЕСС РЫНКА — сделок нет ни на одной стороне'      (existing string, byte-identical)
```

Both strings are `\uXXXX`-escaped ES5 string concatenation. The existing string
must remain byte-identical so that every stress fixture reaching the banner by
the old route renders exactly as before.

**Expected behavioural effect, stated in advance so the report can confirm it.**
Replaying `journal/data/2026-08-21.jsonl` and `2026-08-22.jsonl`, both dates move
from `trend/dir=+1` to `stress`, every coin's `action` becomes `none`, and the
board prints the new banner. The one `trade` verdict on 2026-08-22 (`GRAM`) and
the one `wait` (`HBAR`) disappear. **This is the intended outcome, not a
regression.** If the replay shows anything else, that is a finding.

### Stage B — venue-correct list exhaustion

`listExhaustion` skips rows declared `fut:true`, reading the declaration from
production's own `tokens[]` and never from what a host returned (inv. 41). The
venue test short-circuits **before** the `cd` test, so a `fut:true` row can never
reach `dayRangeRatio` regardless of what fields it carries.

The `n < 8` quorum is unchanged and is applied **after** the exclusion: `n`
counts contributing spot rows only.

### Stage C — new board block «РИСК ВЫНОСА», sixth

A new section `sSqz`, computed anywhere after `E` and `dec` are available, and
inserted **only** into the concatenation at the end of `boardHtml` (inv. 15),
between `sLev` and `sSize`:

```
   + sLev                      //  5. ВЫБОР ПЛЕЧА
   + sSqz                      //  6. РИСК ВЫНОСА
   + sSize                     //  7. РАЗМЕР ПОЗИЦИИ
   ... every following comment number shifts by one, code order untouched
```

It sits sixth because it is the direct consequence of the pressed leverage button
(inv. 14) and must be read before size is chosen. It uses no variable declared in
the size block.

`.bd-h` text is `РИСК ВЫНОСА` — unique on the board, which is what the scroll
anchor keys on (inv. 18). **No inline `style` on the `.bd-sec`** (§3.7: an inline
style kills the metal ring); any colour needed comes from a class.

Three rows, in this order.

**Row 1 — запас до ликвидации.** From the **pressed** leverage `currentLev`, never
from the RESULT (inv. 14):

```
liq  = liqPrice(E, currentLev, isLong)                    existing function
b    = |ln(liq / E)|
dSig = b / sigmaDay(cd.volatility)                        existing function, single site
p24  = touchProb(cd.volatility, b, 24)                    existing function, inv. 20
```

Printed as the distance in daily sigmas and the 24-hour touch probability through
`probTxt` (inv. 20). This is a **new horizon**, not a duplicate of the 7/14/30d
ladder in «ЦЕНА ВРЕМЕНИ»; the ladder is not repeated here and «ЦЕНА ВРЕМЕНИ» is
not modified. Caption states that the probability is a lower bound (§7).

Missing `volatility` → the row prints the sigma distance as unavailable and the
block survives (inv. 9). `liq` non-finite or `E <= 0` → row omitted, block
survives.

**Row 2 — насколько день уже вынесен.** The coin and the list, both raw:

```
own  = dayRangeRatio(hi24, lo24, cur, cd.volatility)
list = listExhaustion(rows)          -> { median, n, abnormal }
```

Printed as plain multiples of a diffusive day — «сегодня X,X обычного дня», and
for the list «медиана списка Y,Y по N монетам». **No threshold, no comparison, no
colour, and `abnormal` is not read.** The caption states that 1,0 is an ordinary
day because `E[range] = σ·√(8/π)`, so the number is interpretable without a
constant. `median === null` (quorum not met) → the list line says the list could
not be measured and the coin line still prints. `own === null` → the coin line is
omitted.

**Row 3 — стоп отодвинут от шума.** Read from `dec.inv`, nothing recomputed
(inv. 20):

```
inv.capped  === true  -> «опоры рядом нет, уровень нарисован — стоп держится вручную»
inv.floored === true  -> «стоп прижат к полу 2σ: ближе шума ставить нельзя»
otherwise             -> the stop distance in daily sigmas, from inv.dist and inv.sd
```

**Purity.** No output of this block enters `scoreCandidate`, `tradeGeometry`,
`leverageDecision`, `directionVerdict`, `marketRegime` or the journal writer. It
is display in the standing of inv. 27, and the report must demonstrate that.

### Stage D — benches

Wire every claim above into the gate. Counters are incremented **at the
comparison site** (inv. 43); no estimated products. Any bench that would pass on
zero data fails instead (inv. 22), and every mode returns an exit code (inv. 29).

- `bench/direction_bench.py` — `marketRegime` symmetry: for a grid of `z` across
  `[-4, +4]` and `volatility` across the `VOL_HARD` boundary, assert
  `mode === 'stress'` exactly when `v >= VOL_HARD || |z| >= REG_STRESS_Z`, and
  assert `dir === 0` in every stress cell. Include the exact boundaries
  `z = ±REG_STRESS_Z`.
- `bench/exhaustion_bench.js` — Stage B: a fixture list mixing `fut:true` and
  spot rows must produce a median identical to the same list with the `fut:true`
  rows physically removed, and `n` must equal the spot count. Include a list that
  reaches quorum only by counting `fut:true` rows and assert `median === null`.
- `bench/exhaustion_bench.js` — Stage A banner: drive all five banner states
  including the new upward-stress one, `isLong` both ways, and require each
  string byte-identical to a table in the bench.
- `bench/prot_bench.js` — the block: whole-board comparison already runs on
  identity (TZ-11 Stage A). Add scenarios covering `capped`, `floored`, neither,
  missing `volatility`, `median === null`, and both sides × the four leverage
  buttons, asserting the block is present, sits sixth, and carries no inline
  `style` on its `.bd-sec`.

`bench.yml` step count stays 12. Only steps 3, 5, 11 and 12 may move; any other
movement is a finding to report, not to fix.

---

## 3. Non-goals — do not do these

- **No `DAY_RANGE_ABNORMAL`.** The constant does not exist, `abnormal` stays
  hardcoded `false`, and nothing compares anything to a threshold. Printing a
  measured ratio is not a consumer of the constant; adding a comparison, a colour
  scale, or a word like «аномально» is, and is forbidden here. The rule is
  re-registered in a later TZ (§3.16, inv. 23, inv. 47).
- **The registered window is not widened.** 1.59 against 1.60 is not touched, not
  rounded, not re-run at another depth.
- **`scoreCandidate` weights are not tuned**, no ranking factor is added, and no
  new external data source is introduced. The block uses fields already fetched.
- **«ЦЕНА ВРЕМЕНИ», «ЗАЩИТА ПОЗИЦИИ» and the leverage engine are not modified.**
  The four ceilings, `LIQ_MMR`, `L_CAP` and the invalidation level are untouched.
- **No new constant anywhere** (inv. 20).
- **`main.py`, `catalysts.json`, `journal/**`, `.github/workflows/**` are not
  touched.**
- **No bench is edited to make it pass.** A red bench is a product defect or a
  stale expectation; both are findings with their own TZ.

---

## 4. Files

| Path | Change |
|---|---|
| `index.html` | `marketRegime`, `regimeBanner`, `listExhaustion`, new `sSqz` section, one line in the `boardHtml` concatenation |
| `bench/direction_bench.py` | regime symmetry cells |
| `bench/exhaustion_bench.js` | venue exclusion, quorum, banner table |
| `bench/prot_bench.js` | board scenarios for the new block |
| `CryptoReports/TZ-12-stress-symmetry-and-squeeze-block-report.md` | new, straight to `main` |

ES5 only in `index.html`: `var`, string concatenation, no arrow functions, no
template literals. Every on-screen Russian string is `\uXXXX`-escaped; no raw
Cyrillic in a JavaScript string literal.

---

## 5. Validation — written by the Architect, run by the Executor

The Executor runs these and reports results; it does not design them, add to
them, or mark any item «not applicable».

1. `python3 -m py_compile main.py`; `node --check` on the extracted `<script>`;
   ES5 guard and Cyrillic guard over every added line.
2. **Stage A, the boundary.** `z = -REG_STRESS_Z`, `-REG_STRESS_Z + ε`,
   `+REG_STRESS_Z - ε`, `+REG_STRESS_Z`, and `z = null` with
   `volatility >= VOL_HARD`. Report the mode and `dir` for each.
3. **Stage A, the replay.** Both journaled dates through the production functions
   cut out of `index.html` (inv. 21, no formula reimplemented). Report, per date:
   `reg.mode`, `reg.z`, the count of coins by `action`, and the rendered banner
   string. The expected result is stated in §2 Stage A; a departure is a finding.
4. **Stage A, negative control.** Restore the one-sided comparison; the symmetry
   cells must turn red and the step must exit non-zero. Restore and verify by MD5
   against the pre-control copy.
5. **Stage B.** Median and `n` with and without the `fut:true` rows, on a fixture
   where their presence changes both; the below-quorum case; proof the venue test
   short-circuits ahead of the `cd` test.
6. **Stage C, the block.** Present on every board; sixth in the concatenation;
   `.bd-h` text unique; no inline `style` on its `.bd-sec`; every number recomputed
   by hand for one reference case and quoted (`UNI`, `E = $10.00`, `4X`, and the
   `vol` from the 2026-08-22 snapshot).
7. **Stage C, degradation.** Missing `volatility`, `median === null`, `capped`,
   `floored`, `E <= 0`, non-finite `liq`: in each the block renders, says what is
   missing, and the rest of the board lives (inv. 9).
8. **Stage C, purity.** Demonstrate that no field produced in the block reaches
   `scoreCandidate`, `tradeGeometry`, `leverageDecision`, `directionVerdict` or
   the journal writer — by showing the verdict and the journal record byte-identical
   with the block's inputs perturbed (inv. 27).
9. **No-regression, identity first.** `prot_bench.js` on identity must report zero
   differences before any other comparison is offered as evidence (inv. 45). Then
   whole boards against `origin/main`, and the differences that appear must be
   exactly the new block plus the banner change — enumerated, not summarised.
10. **Full gate, 12 steps, every step exit 0.** Report baseline and candidate
    counts per step against a `git worktree` at `origin/main`, and explain the
    delta term by term. Baseline total must reproduce **1 185 871**.
11. **Extremes**, unchanged from the release checklist: slider edges, null betas,
    truncated Gist, HTTP 400 ticker, dead-market fields, missing coeffs fields,
    absent `btcStats`.

---

## 6. Pre-existing issues

Report anything found and **do not fix it**. In particular: if the regime change
turns any existing bench fixture from `trend` to `stress`, say so and say which,
term by term. That is expected and is not a licence to edit the fixture.

---

## 7. Report

`CryptoReports/TZ-12-stress-symmetry-and-squeeze-block-report.md`, straight to
`main`, branch left unmerged. State line counts and MD5 for
`SYSTEM-MAP-CRYPTOCALCUL.md`, `index.html`, `main.py` and `catalysts.json`, the
per-step gate table with the delta explained term by term, the journal replay
table from item 3, and the reference case from item 6 with its arithmetic shown.

**NOT IN EFFECT UNTIL MERGED.**
