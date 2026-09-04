# TZ-27 — Continuation target versus the 90-day extremum, archive backtest

**Canonical filename: `TZ-27-continuation-target-backtest.md`.** Commit the file under
this name in `CryptoTZ/`, whatever name it arrived under (contract §3).

**Executor model: Opus.** The change is one Python file and one workflow, but it adds a
first-touch resolver with a side-dependent barrier comparison — the class of error that
produces a plausible number and no exception — and its output is the measurement a later
TZ will cite to open hard-floor item 1 on `tradeGeometry`.

---

## 0. System Map fingerprint — required, blocking (contract §5)

The map's `## 0. Fingerprint` block, quoted in full. Match each anchor as an exact
substring against `SYSTEM-MAP-CRYPTOCALCUL.md` on `origin/main` after
`git fetch --all --prune`. Any mismatch, in either direction → BLOCKED, no work.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-03-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `59. **A standing decision is amended in the floor before it is amended in the code.**` |

Live files at this revision — measure each at the line count and MD5 the map states, and
report any difference under `## Pre-existing Issues` without acting on it:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

---

## 1. Basis

Map §3.12 records a structural tension and gates it on a measurement:

> **Known structural tension, deliberately not fixed.** `tradeGeometry` does not take the
> regime: the target is always the 90-day extremum, i.e. a MEAN-REVERSION target, while in
> `trend` the ranking comes from the CONTINUATION channel. […] **Opening condition:** an
> archive backtest comparing `RR ≥ 2` to the 90-day extremum against a continuation target
> (e.g. `E + k·σ·√H`) on the same momentum-channel inputs.

Map §10 carries the same item as `not built, gated`. This TZ builds the measurement and
nothing else.

**The trigger is a run, and the run made the tension numeric.** Analysis run
`analyst/log/2026-09-04-2.md`, freeze `2026-09-04T08:40:15Z`, published three setups.
Its own appendix §6 records, per side, production's `touchProb` on both barriers over
`H_NOISE`:

| SYM | anchor | stop | target | RR | tgtSig | p(target) | p(stop) |
|---|---:|---:|---:|---:|---:|---:|---:|
| GRAM | 1.35515 | 1.2485 | 1.82772 | 4.43 | 3.35 | 0.4 % | 43.1 % |
| TRX | 0.32747 | 0.320315 | 0.349583 | 3.09 | 3.01 | 0.4 % | 32.4 % |
| XLM | 0.179561 | 0.149356 | 0.247414 | 2.25 | 3.42 | 0.4 % | 9.5 % |

**Two facts in that table are the whole reason this TZ exists, and neither is a forecast.**

1. The target-touch probability is 0.4 % on all three while `RR` ranges 2.25 to 4.43. The
   reward leg is therefore constant across the admitted set and every unit of `RR`
   variation comes from the risk leg. A number published as «reward against risk» is
   ordering the list by its denominator alone.
2. `tgtSig` on the three admitted rows is 3.35 / 3.01 / 3.42 — the top of the whole
   25-row table, whose refused rows run down to 0.53. `RR_MIN` and `TGT_SIGMA_MIN` are
   both monotone increasing in target distance and there is no ceiling on either, so the
   two reward-leg gates select, jointly, for the least reachable target on the board.

Fact 2 is the sharper half and it is the reverse of the failure §3.12 describes. §3.12
names the case where the extremum sits too CLOSE and `RR` breaks; the run shows the case
where it sits so FAR that `RR` passes trivially. Both are the same root: **target distance
is set by a 90-day window and judged against a 7-day horizon, and nothing in
`tradeGeometry` reconciles the two.**

`ANALYST-INSTRUCTIONS.md` revision `2026-09-04-b` records the same finding and refuses to
act on it, correctly: «That is map §3.12's open item, and it is now gated on a measurement
rather than on a suspicion.»

**This TZ changes no production math.** Hard-floor item 1 keeps `tradeGeometry`,
`invalidationInfo`, `leverageDecision` and `directionVerdict` closed to edits, and this TZ
does not cite a completed backtest because it is the backtest. A production change, if the
measurement earns one, is a separate TZ that cites this one's report.

---

## 2. Source text read from the repository (inv. 55)

Quoted so the Executor compares rather than recalls. Every string below was read from the
files at the fingerprint above.

`index.html`, constants — the mode reads these by cutting them, never by typing them:

```
var LIQ_MMR   = 0.0125;
var H_NOISE   = 168;
var INV_FLOOR_SD = 2.0;
var INV_CAP_SD   = 6.0;
var MAX_MARGIN_LOSS = 0.35;
var RR_MIN         = 2.0;
var TGT_SIGMA_MIN  = 1.0;
var ENTRY_CHASE_SD = 0.5;
var L_MIN     = 2;
var L_CAP     = 7;
```

`index.html`, `tradeGeometry` — the four lines the measurement is about:

```js
var tgt = isLong ? cd.max_price : cd.min_price;
g.reward = isLong ? (tgt - E) / E : (E - tgt) / E;
if (g.risk > 0) g.rr = g.reward / g.risk;
g.tgtSig = g.reward / (vol * Math.sqrt(H_NOISE));
```

`index.html`, `touchProb` — the single touch formula (inv. 20), used unchanged:

```js
function touchProb(vol, b, hours) {
    if (!has(vol) || vol <= 0 || !has(b) || b < 0) return null;
    var q = vol * Math.sqrt(hours);
    if (!(q > 0)) return 0;
    return Math.max(0, Math.min(1, 2 * (1 - normCdf(b / q))));
}
```

`index.html`, the comment above `RR_MIN` — this is the claim the primary tests:

```
// RR_MIN — то же число 2, которое доска уже печатает в «ЕСЛИ СРАБОТАЕТ»:
// «отношение ниже 1:2 означает, что сделка должна угадывать чаще, чем
// ошибаться». Одно число на систему — доска и вето читают отсюда (инв. 20).
```

`bench/backtest_bench.py`, `CdBuilder.build` returns exactly the fields this mode needs and
**no new field is added to it**:

```python
return {
    "min_price": g["min_p"], "max_price": g["max_p"],
    "price_pos": float(g["price_pos"]), "volatility": g["volatility"],
    "r7": g["r7"], "r14": g["r14"], "r30": g["r30"],
    "min30": g["mn30"], "max30": g["mx30"], "vol7": g["vol7"],
    "eff14": g["eff14"], "vol_ratio": g["vratio"],
    "rank": None, "rank_prev": None, "fdv_mc": None,
}
```

`bench/backtest_bench.py`, `BetaWalk.betas` returns exactly what `advBeta` reads:

```python
return {"up_beta_90": up_b, "up_r2_90": up_r2,
        "down_beta_90": dn_b, "down_r2_90": dn_r2}
```

Contract §7 clauses this TZ's stages touch, quoted:

- **Item 1** — `tradeGeometry` and the other named functions «are closed to edits by
  default». This TZ edits none of them and asserts it by hash.
- **Item 2** — «Never edit a bench to make it pass.» Applies to the new controls from the
  moment they are written: a red control in section D is a finding.
- **Item 8** — «Never modify `.github/workflows/backtest_bench.yml` unless the TZ names
  it.» **This TZ names it**, for the single purpose in §4 Scope B and nothing else.
- **Item 9** — the archive fetch and the measurement run happen on a runner, never in the
  session, because a session fetch cannot stand behind a product fact (inv. 44). The
  session may run the offline controls.
- **Item 12** — no bench FILE is added, so no `bench.yml` wiring is created by this TZ.
  What is required instead is a measurement: §5 item 7.

---

## 3. What is being measured, and what is deliberately not

**The question is geometric and is answered without a forecast.** `RR_MIN` asserts a hit
rate — the board's own words, quoted above: below 1:2 «the trade must be right more often
than wrong». That is a testable claim about first-touch counts, and testing it assumes no
drift, because the bar is the one `RR` itself states.

**The question is NOT which target makes more money.** Under a driftless walk `E[R] = 0`
under any selection — map inv. 32, a theorem, confirmed by the bench's own `--control` run.
A profit comparison between the two targets would be measuring noise, and any positive
reading would first owe an account of where the drift came from. The realised R-multiple
is therefore computed and printed **as a registered descriptive with no consequence**, and
the mode's own report says so on the line that prints it.

**The two arms share one risk leg by construction.** `leverageDecision` is called once per
(date, coin, side) on the untouched `cd`, and the resulting `dec` is passed into both arms.
`tradeGeometry` takes `dec` as an argument, so `inv.dist`, `inv.price`, `moneyBelowMin` and
`ok` are literally the same numbers in both. The comparison is on the reward leg alone,
which is the only thing under test.

**The continuation arm calls production, it does not reimplement it** (inv. 21, inv. 38).
The arm builds a shallow copy of `cd` whose `max_price` (long) or `min_price` (short) is
replaced by the continuation level, and calls the unmodified `tradeGeometry` on it. Every
veto, the chase anchor and `tgtSig` are then production's own arithmetic on a substituted
target, which is exactly the object under test. The copy is passed to `tradeGeometry` only;
`dec` was already computed on the original `cd`, so `invalidationInfo`'s use of the
extremum as a fallback reference cannot leak the substitution into the stop.

---

## 4. Scope

Complete authorisation. Anything not below is forbidden (contract §6).

### Files to Modify

| File | Scope |
|---|---|
| `bench/backtest_bench.py` | A · new mode `--target` + `lab_selftest` section D |
| `.github/workflows/backtest_bench.yml` | B · make the mode runnable and its artifact uploaded |

### Files to Create

None. `target_raw.json` is a run artifact next to `stops_raw.json` and is not committed.

### Files that must be byte-identical after the change

`index.html`, `main.py`, `catalysts.json`, `.github/workflows/bench.yml`,
`.github/workflows/main.yml`, `journal/**`, `analyst/**`. Report `md5sum` before and after
for the first four.

---

### Scope A — `--target` in `bench/backtest_bench.py`

**A1. Mode plumbing.** Add `--target` to `main()`'s parser and dispatch, in the shape
`--stops` already uses: load the cache, refuse below eight coins, run, report, dump
`target_raw.json` into `HERE`, return 0. `--horizon` and `--step` are inherited; their
defaults are the mode's registered values (§4 A6) and the run does not override them.

**A2. High/low requirement.** The mode requires `hl` in the cache and exits with the same
class of message `run_stops` uses when it is absent. A close-based first touch understates
both barriers, and understating the target is the error this measurement exists to detect.

**A3. Per-setup construction.** For each `(t, s, i, iF, iX)` from
`walk_grid(series, horizon_d, step_d, fwd_extra_d=0)` and each side:

1. `cd = CdBuilder.build(...)` at `i`; skip on `None`.
2. `cd.update(BetaWalk.betas(...))` at the same `i`; on `None`, leave the beta fields
   absent — production's own missing-field path (inv. 9) drops the BTC ceiling, which is
   what the board does on a coin without 90-day betas.
3. `btcStats = {"volatility": <CdBuilder.build on the BTC series at the same t>["volatility"]}`.
   BTC comes from `load_cache(keep_btc=True)`; the mode exits non-zero if it is absent,
   with the message `--res7` already uses for the same reason.
4. `E = close[i]`.
5. `hi24` / `lo24` = the max `high` and min `low` over the 24 hourly `hl` rows ending at
   `i`, inclusive. **This is the one input the bench assembles itself**, so inv. 48
   applies: assert once, in the mode's own selftest, that the fields supplied are exactly
   the fields `tradeGeometry` reads off them, derived from the source rather than typed.
   A window shorter than 24 rows disqualifies the setup.
6. `dec = leverageDecision(cd, E, isLong, btcStats)` — once, shared by both arms.
7. `g_prod = tradeGeometry(cd, E, isLong, dec, hi24, lo24)`.
8. For each `k` in the grid: `cd_k` = shallow copy with the extremum replaced by
   `E * exp(+k * vol * sqrt(H))` for long, `E * exp(-k * vol * sqrt(H))` for short;
   `g_k = tradeGeometry(cd_k, E, isLong, dec, hi24, lo24)`.

**A4. Admission.** A setup enters the measured set for an arm when that arm's `g` is
non-null and `g.veto` is empty. This is `directionVerdict`'s geometry gate and nothing
else: the regime and channel layers are **not** applied, because they decide the side and
not the target, and applying them would confound a target question with a regime question.
The regime is instead recorded as a per-observation field — `marketRegime(btcStats)` with
BTC's `r7`/`r14`/`volatility` from the same BTC `cd` — so the summary can group by it
without the primary depending on it.

**A5. First-touch resolution.** Over the `H = horizon_d * 24` hourly `hl` rows after `i`:

- long: target touched when `high >= tgt`, stop touched when `low <= stop`;
- short: target touched when `low <= tgt`, stop touched when `high >= stop`;
- `first ∈ {tgt, stop, tie, none}` — `tie` when both fall inside the same hourly candle
  and the order is genuinely unresolvable. Recorded, never guessed; the journal's own
  vocabulary (map §3.13). `tie` is excluded from the odds and counted separately.
- The window must be covered: fewer than `H - 12` rows disqualifies the setup, as in
  `run_stops`.

**A6. Registered constants of the mode.** Fixed here, before any data (inv. 23), and read
by the code from one declaration each (inv. 20):

```
horizon         H_NOISE / 24 = 7 days, i.e. H = 168 hours   (cut from index.html, not typed)
step            7 days
k grid          {1.0, 1.5, 2.0, 2.5, 3.0}
quorum          60 admitted setups AND 20 contributing dates, per side per arm
bootstrap       date blocks, 2000 resamples, block 3, as stops_summary already does
```

`step = 7` is deliberate and is not raised to 1. A daily grid multiplies setups without
multiplying independent forward windows — consecutive dates share six sevenths of the
window (map §3.13) — and a CI computed over overlapping windows is narrower than the
evidence supports. That is the wrong direction of error for a measurement that will
authorise a production change.

Below quorum a side's verdict is «не выносится»; if BOTH sides of the production arm are
below quorum the mode returns non-zero, because a run that compared too little must not
look like a run that found nothing (inv. 22, inv. 37).

**A7. The registered PRIMARY, one claim, one bar.**

> **Object.** The production arm's admitted set, pooled per side.
> **Statistic.** `Ω = n_tgt / n_stop`, the realised first-touch odds, `tie` and `none`
> excluded from both counts, CI95 by date-block bootstrap.
> **Bar.** `Ω >= 1 / RR_MIN = 0.50`. The set was admitted at `RR >= 2`, whose printed
> meaning is that the trade need not be right more often than wrong; `1/RR_MIN` is the
> most generous point of the admitted range, so the bar errs toward keeping the incumbent.
> **Verdict rule, fixed before data.** CI95 entirely below 0.50 → the 90-day extremum does
> not deliver the odds its own `RR` asserts at the horizon the system trades. CI95
> covering 0.50 → it does, and the continuation target is refused. CI95 entirely above →
> the same, more strongly.

The mode prints this verdict from the rule above and never from the number's appearance,
in the shape `report_stops` already uses for its own primary.

**A8. Registered descriptives — printed, no action by registration.** Each is labelled in
the output as descriptive so no later reader mistakes it for a claim:

1. `measured / model` calibration of the TARGET leg: measured = realised share touching
   `tgt` within `H`; model = mean of `touchProb(vol, |ln(tgt/E)|, H)` on the same setups.
   The mirror of `--stops` on the barrier nobody has ever measured.
2. `P_none` — share of admitted setups resolving at neither barrier within `H`.
3. Model odds under the driftless two-barrier identity: `Σ q_i / Σ (1 - q_i)` with
   `q_i = b_i / (a_i + b_i)`, `a_i = |ln(tgt/E)|`, `b_i = |ln(stop/E)|`. Printed beside
   `1/RR`, which uses relative distances; the gap between the two is itself worth having
   and costs nothing.
4. Spearman rank correlation between `g.rr` and `g.tgtSig` over ALL rows that reached a
   geometry call, admitted or not — the mechanism §1 fact 2 names. `spearman` already
   exists in the file.
5. Distribution of `g.tgtSig` on admitted versus refused rows: n, median, p10, p90.
6. Realised R-multiple per arm, `+rr` on a target-first, `-1` on a stop-first, `0` on
   `tie`, mark-to-market at `H` on `none`. **Printed with the sentence that it carries no
   consequence and may not be cited as evidence for either target without first accounting
   for drift or costs (inv. 32).**
7. Per-symbol contribution: symbol, dates contributed, setups admitted per arm. A run
   must state what it compared (inv. 22).

**A9. The continuation arm's reading.** For each `k`: the same `Ω`, calibration, `P_none`
and admitted-set size. The reported outcome is `k*`, the smallest `k` in the grid whose
`Ω` CI95 covers or exceeds 0.50 — or `none`, if no `k` does. `k*` is a finding, not a
constant: it is not written into `index.html` by this TZ and creates no production number.

**A10. Language.** New comments and docstrings are English (CANON). New printed report
strings follow the surrounding file, which prints Russian — a report printed half in each
language is worse than either. This is stated so it is not filed as a deviation.

---

### Scope B — `.github/workflows/backtest_bench.yml`

Hard-floor item 8 is opened for this file and for this purpose only.

Make the new mode selectable and its artifact uploaded **by the identical mechanism the
file already uses for `--stops`** — read that path in the file and mirror it; do not invent
a second one. Upload `target_raw.json` alongside whatever `--stops` uploads. No other
change to this workflow: no trigger change, no runner change, no timeout change, no
dependency change. Report the diff in full.

---

## 5. Validation

Written by the Architect. Every item is run; an item that cannot be run **fails** and is
never «not applicable» (contract §9). Baseline first, so the diff is provable.

1. `python3 -m py_compile bench/backtest_bench.py` — exit 0, reported.
2. `node --check` on every bridge file the new mode generates through `_extract_js_set` —
   report the filename and the exit code. `_extract_js_set` already runs `node --check`
   itself and raises; report that it did.
3. **`--lab-selftest` green with section D present.** Print each control's measured number
   beside its registered tolerance:

   | # | Control | World | Registered pass condition |
   |---|---|---|---|
   | D1 | target-leg calibration | `synth_hl("normal")`, continuation arm at `k = 1.5` | measured/model CI95 covers 1.0, or point in [0.85, 1.10] |
   | D2 | monotonicity | same world, full `k` grid | `Ω(k)` strictly decreasing across the five grid points |
   | D3 | long-horizon identity | same world, `H = 8 × 168 h` | `P_none < 0.05` and `Ω` within ±15 % of `Σq/Σ(1−q)` |
   | D4 | identity differ (inv. 45) | same world, continuation arm with the target forced to `cd.max_price` / `cd.min_price` | zero differences against the production arm across every recorded field, with a printed comparison count that fails on zero (inv. 22) |
   | D5 | look-ahead | same world | the per-setup record built from the full series is byte-identical to the one built from the series truncated at `t + H` |
   | D6 | side swap | same world | \|Ω_long − Ω_short\| ≤ 0.10 — a symmetric world must read the same on both sides, and a swapped barrier comparison is otherwise invisible |

   D4 runs unconditionally inside the default lab suite, not behind a flag. A comparator
   never proven on identity supports no claim about a real diff.

4. **Negative test (contract §9).** In the working tree, invert the long/short barrier
   comparison in the new first-touch resolver. Confirm section D turns red and name which
   controls fired. Revert. Confirm `git status --porcelain` is empty and section D is green
   again. Report both directions. A control never proven to fail is not a control.
5. **Regression on the modes that share the new code's dependencies.** `walk_grid`,
   `CdBuilder`, `BetaWalk`, `JsBridge` and `spearman` are reused, so any refactor of them
   moves other modes. Record `--selftest` (10 seeds) and `--stops` output BEFORE the change,
   run both after, and report a byte-level comparison of the printed numbers. Any movement
   is a finding, not a rounding note.
6. **The archive run, on a runner.** `--target` through
   `.github/workflows/backtest_bench.yml`. Report: run id and conclusion; dates counted;
   admitted setups per side per arm; the per-symbol table of A8 item 7; the primary `Ω`
   with CI95 and the verdict the registered rule produces; every descriptive of A8; `k*`.
   If the cache needs `--fetch` first, that fetch is a runner step too (inv. 44) and its
   result is reported.
7. **`bench.yml` unchanged and still green.** Run the full 13-step gate and report every
   step's check count. The expected total delta against the map's 1 255 401 is **zero**,
   because no gate bench is touched; a non-zero delta is a finding and is attributed term by
   term (inv. 43). Separately, state whether `bench.yml` invokes `--lab-selftest` at all —
   read it and say — because if it does, section D is inside the gate and its step's count
   moves, and if it does not, section D is a manual control and the report says so plainly.
8. **Production untouched.** `md5sum` on `index.html`, `main.py`, `catalysts.json` and
   `.github/workflows/bench.yml` before and after; all four unchanged. This is the
   mechanical proof of hard-floor item 1 for this TZ.
9. Standing checks (map §6 item 1) even though no production file is expected to move:
   `python3 -m py_compile main.py` and `node --check` on the `<script>` block extracted
   from `index.html`.

---

## 6. Deliverables

- Branch `claude/tz-27-continuation-target-backtest`, pull request opened, not merged.
- `CryptoReports/TZ-27-continuation-target-backtest-report.md` pushed straight to `main`,
  in the contract §10 template, carrying the fingerprints of the map and of every file its
  `## 0` table lists.
- The report states the primary verdict as the registered rule produces it, and does not
  interpret it. Interpretation is the audit's.

---

## 7. What this TZ must NOT do

- Not edit `tradeGeometry`, `invalidationInfo`, `leverageDecision`, `directionVerdict`,
  `touchProb`, `scoreCandidate`, `momentumScore` or any other function named in hard-floor
  item 1 — including «harmlessly», to expose a parameter, or to make a bench easier.
- Not introduce a constant into `index.html`. `k` and `k*` are bench quantities.
- Not add a field to `CdBuilder.build`. Everything the mode needs is already returned.
- Not modify `bench.yml`, `main.yml`, `calib.yml` or `journal.yml`.
- Not widen the measurement to a second horizon, a second universe or a drift model
  because the narrow one looks incomplete. Report the gap (contract §6).
- Not act on the result. A production change is a later TZ that cites this report.
