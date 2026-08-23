# SYSTEM MAP — Pro Crypto Tool

Technical contract of the live system: architecture, data flow, modules,
dependencies, invariants. Consult before any code change and when interpreting a
metric. Nothing here is history — the record of how the system got here is git
history plus `CryptoReports/**`.

**Language.** English, except on-screen strings and board block names, which are
quoted verbatim in Russian because that is what the code prints.

---

## 0. Fingerprint

**Revision 2026-08-23-a.** Baseline: TZ-10 merged (PR #10, `baa9d9b`).

Every TZ header quotes this block. The Executor compares it against the
repository copy before doing any work (contract §5); a mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-23-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| newest invariant | `46. **A calibrated constant is checked against its calibration record.**` |

Live files at this revision:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3569 | `56af2e274e5568527a6bb0e5cb4e3456` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |

Gate at this revision: `bench.yml`, **12 steps, 1 185 864 checks**, all green on a
runner. The number is a sum of per-comparison counters (inv. 43), not an
estimate.

**A TZ has executed if and only if `CryptoReports/` holds a report with its
number.** `CryptoTZ/TZ-03-report-delivery.md` has no report and never ran: it was
declared dead by TZ-04 and is retained as evidence, not as a pending task.

---

## 1. Data flow

```
iPhone Shortcut → workflow_dispatch → GitHub Actions → main.py
   → CoinGecko /market_chart (90d hourly; BTC + 28 alts = 29 calls)
   + CoinGecko /coins/markets (ranks, FDV = 1 call)          30 calls/run
   → metrics → PATCH Gist → WebApp (GitHub Pages) on iPhone
```

| Module | Path | Runs | Reads | Writes |
|---|---|---|---|---|
| Data bot | `main.py` | hourly, Shortcut-triggered | CoinGecko | Gist: `coeffs.json`, `debug.json`, `history.json` |
| Calculator | `index.html` | in browser | Gist + Binance + `catalysts.json` | localStorage (order, side) |
| Catalyst registry | `catalysts.json` | static, served by Pages | — | edited by the Architect through a TZ |
| Verdict journal | `journal/write.js` | `journal.yml`, 13:00 UTC | Gist, `data-api.binance.vision`, `catalysts.json`, `index.html` | `journal/data/**`, `journal/out/**`, `journal/runs.jsonl` |
| Benches | `bench/**` | `bench.yml` on push/PR | production files at runtime | nothing tracked |
| Backtest | `bench/backtest_bench.py` | `backtest_bench.yml`, manual | `data.binance.vision` archive | artifacts only |
| Calibration | `bench/exhaustion_calib.py` | no workflow yet — archive-dependent, so a runner only (inv. 44) | `data.binance.vision` archive | nothing tracked |

**Schedule is not cron.** The only regular trigger is the Boss's iPhone
Shortcut: hourly from 09:00 to 01:50 local = **17 runs/day ≈ 15.3k CoinGecko
calls/month**, plus rare `push` runs on `main.py` / `main.yml`. Automation
outside the repository is never duplicated and never switched off — it belongs
to the Boss. Cron in `main.yml` was removed deliberately in June 2026; a second
scheduler is a second source of truth for freshness.

**The 7 h 10 min night pause is part of the design.** Between 01:50 and 09:00
there are no runs, `coeffs.json` ages to ~7 h and `STALE_CRIT` lights every night
on a fully healthy system. Hence inv. 4: «schedule asleep» and «update failed»
are different states.

**Second scheduled run — the verdict journal** (`journal.yml`, 13:00 UTC, §3.13).
It never calls CoinGecko: it reads the finished Gist and prices from
`data-api.binance.vision`, executes production functions out of `index.html`, and
appends the day's record.

**Third file served by Pages — `catalysts.json`** (§3.15), next to `index.html`,
read by the frontend over plain XHR. The bot does not write it and it never
enters the Gist. If it fails to load, the layer goes dark with a banner and the
board keeps working (inv. 40).

**Venue is declared, not observed (§3.14):** 25 coins are Binance Spot, three —
**XMR, LIT, HYPE** — Binance Futures only.

**Gist files**

- `coeffs.json` — `generated_at` + `btc` (min/max/price_pos/volatility + r7/r14/r30) + `analysis_data[]` (incl. `rank`, `rank_prev`, `fdv_mc`)
- `debug.json` — per coin: `candles_total`, `matched_90d/14d`, `returns_90d/14d`, `error`, `ranks_fetched`, `fdv_fetched`
- `history.json` — ≤ 720 points (~30 days): ub/ur/db/dr/ub90/db90 + rank `r`

**Frontend's own three Binance sources**

- spot ticker `api/v3/ticker/24hr?symbols=` — 30 s, only pairs without `fut:true`
- futures ticker `fapi/v1/ticker/24hr?symbol=` — 30 s, one request per `fut:true` token
- funding `fapi/v1/premiumIndex` — 5 min

**Universe: 28 pairs, frozen.** New coins are not added (standing decision).

---

## 2. Bot mathematics — `main.py`

- Bucketing: `floor(ts_ms / 3.6e6)` → hourly buckets; keys common to BTC ∩ coin.
- Returns: **only between adjacent buckets**; returns across gaps are dropped.
- Betas: OLS with intercept, separately up (BTC hour > 0) and down (< 0); windows 14d and 90d. Minimums: 24 matched (14d), 120 (90d); < 5 returns in a direction → `None`. The intercept (alpha) is deliberately unused: at 14d its standard error is comparable to the estimate itself.
- `up_beta_90`/`up_r2_90` and `down_*` are always paired: `fit_stats` returns either (float, float) or (None, None).
- `corr_90`: Pearson over all 90d returns. `volatility`: std of hourly returns over 90d. `min`/`max`/`price_pos`: over 90d.
- `btc.volatility` — BTC's own hourly volatility over 90d; the frontend uses it to size the BTC-crash ceiling (§3.2).
- `btc.r7` / `btc.r14` / `btc.r30` — BTC's own return over 7/14/30 days, from the already-downloaded series: **zero new API calls**. Needed for `res7` (§3.9). `null` is a normal state and the frontend must survive it (inv. 9). Windows are cut from the LAST point of each series; a few minutes of offset between BTC and an alt is below noise at a 7-day horizon.
- `fdv_mc` = `fully_diluted_valuation / market_cap` from the same `/coins/markets` call as ranks (zero new requests). Values < 0.95 and > 100 are discarded as supply-data garbage. `None` is normal: coins without a max supply (ETH, XMR) return FDV `null`.
- `error = true` ⇔ too few 14d points or a failed request → the card renders NO DATA.
- The bot does not depend on a spot pair existing: betas come from CoinGecko.

**Integrity cross-check.** From the single-factor identity `σ_BTC = σ_alt·√R²/|β|`, BTC's hourly volatility recovered from five independent cards reads 0.316–0.393 %/h, mean 0.367 %, spread ±11 % — betas and R² are computed correctly.

---

## 3. Frontend mathematics — `index.html`

- `ratio = (target − btc)/btc`; `1 + ratio = target/btc > 0` always.
- `rawBeta` = up_beta | down_beta by the sign of `ratio`; null / non-number → card shows **NO BETA**.
- `beta = rawBeta × stress` (normal 1.0 / panic 1.3 / crash 1.8).
- Forecast: `growth = (1+ratio)^beta`; `pPct = (growth−1)·100`; `pred = cur·growth`.
- Liquidation from `pred`, isolated, `LIQ_MMR = 0.0125`: LONG `pred·(1 − 1/L + MMR)`, SHORT `pred·(1 + 1/L − MMR)`. Fees and funding excluded. **Base on the card is `pred`; on the board it is the entry price `E`.**
- `LIQ_MMR = 0.0125` was recovered by back-calculation from three of the Boss's real positions (XMR 1.28 %, YFI 1.25 %, LIT 1.13 %). The earlier 0.01 placed liquidation further away than reality — an error in the dangerous direction.
- Confidence (0–100): `0.45·R²₁₄ + 0.25·R²₉₀ + 0.20·(1−min(div90,1)) + 0.10·(1−min(vol%/3,1))`; missing components drop out with renormalisation. Colours: ≥ 70 green, 40–69 yellow, < 40 red.
- **R² in both rows (14d and 90d) shares one scale:** < 0.30 red, 0.30–0.60 yellow, ≥ 0.60 green.
- ρ (`corr_90`): ≥ 0.75 green, 0.5–0.75 yellow, < 0.5 red. There is no separate 14d/90d beta-divergence glyph — divergence is already inside Conf.
- **МДЛ gate** (`gateState`, pure display): red when `Conf < 40` OR `R²₁₄ < 0.25` OR (`corr_90` present AND `|ρ| < 0.5`); green when `Conf ≥ 70` and the rest hold; yellow otherwise. High Conf measures correlation-model quality, never direction.

**Production constants, one place each (inv. 20).**

```
LIQ_MMR 0.0125 · H_NOISE 168 · H_BTC 168 · H_REACT 12
L_CAP 7 · L_MIN 2 · INV_FLOOR_SD 2.0 · INV_CAP_SD 6.0 · MAX_MARGIN_LOSS 0.35
EFF_TREND 0.6 · PACE_Z 0.25 · VOL_ABNORMAL 2.0 · VOL_HARD 0.02 · VOL_STOP 0.03
RES_Z 1.0 · RES_R2_CAP 0.90 · FEE_TAKER 0.0005 · FUND_PAY_7D 21 · ARM_R 1.0
RR_MIN 2.0 · TGT_SIGMA_MIN 1.0 · ENTRY_CHASE_SD 0.5 · REG_STRESS_Z 2.0
CAT_WINDOW_D 14 · TIER_STRONG 70 · TIER_MID 50 · TIER_MIN 35
STALE_WARN_MIN 75 · STALE_CRIT_MIN 130
```

### 3.1 Trade side — explicit input

`currentSide ∈ {long, short}`, default `long`, set by the ЛОНГ/ШОРТ buttons, not
persisted to localStorage.

**Slider direction ≠ position side.** The slider sets a BTC scenario; the header
reads `BTC ВВЕРХ` / `BTC ВНИЗ`.

From `currentSide`: the leverage formula (§3.2) and the funding colour. From the
sign of `ratio`: beta choice, slider/button/arrow colours, both liquidation rows.

**Funding colour = the economic effect for the PRESSED side** — green «мне
платят», red «я плачу». Deriving the side from `ratio` inverted the colour
exactly when risk was being measured.

### 3.2 Leverage engine — three independent ceilings

All three are computed at a **7-day horizon** (`H_NOISE = H_BTC = 168`); the
minimum wins, rounded DOWN.

```
Invalidation level (invalidationInfo):
  ref   = min30 / max30   (absent -> min90 / max90, inv. 9)
  ref beyond entry -> src = 'вход'      no structure left, only noise
  structPrice = ref ∓ ½σ_day
  dist = clamp(dStruct, 2σ_day, 6σ_day)          INV_FLOOR_SD, INV_CAP_SD

1. STRUCTURE  L = 1/(dist + 1.645·Vol·√12 + MMR)          H_REACT = 12 h
2. NOISE 7d   need = LONG 1−e^(−q), SHORT e^q−1,  q = 1.645·Vol·√168
              L = 1/(need + MMR)
3. BTC CRASH  D = 2·btc.volatility·√168
              move = |(1 ∓ D)^β_adv − 1|                  L = 1/(move + MMR)
              β_adv = |β90 of the opposite direction|, tightened by the tail
              beta only when tail_r2 ≥ 0.10

RESULT = floor( min(three ceilings, cap) )
cap: L_CAP 7 · vol7/vol90 > 2 -> 3X · Vol ≥ 2 %/h -> 2X · Vol ≥ 3 %/h -> no leverage
RESULT < L_MIN -> «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» + fixHint
```

**Why exactly three.** Structure — «can I exit at my own level before the
exchange does, plus 12 hours of reaction time». Noise — «will chop alone take me
out within a week». BTC crash — «do I survive a systemic move». They rest on
different quantities (distance to the reference / Vol / β), so the binding
ceiling differs per coin and the board names which one binds (`dec.binding`).

**The 6σ distance cap is mandatory:** without it an entry mid-range produced «no
leverage», reading a distant reference as huge risk instead of as absent
guidance. Under `capped` the card says plainly there is no nearby reference and
the stop must be held manually.

**The 2σ distance floor is mandatory:** a move smaller than two daily sigmas is
noise, not a broken idea, and no exit can be promised at such a level.

**Horizon 7 days, not 30.** 30 days was the single most sensitive parameter in
the system — alone it moved the verdict two leverage steps. 7 days is the upper
bound of the Boss's typical hold.

### 3.3 Liquidation-touch probability — `liqTouchProb`

```
d = 1/L − MMR;   LONG b = −ln(1−d)   SHORT b = ln(1+d)
P(touch within H) = 2·(1 − Φ( b / (Vol·√H) ))     reflection principle, drift = 0
```

Shown as a 7d / 14d / 30d ladder from the **pressed** leverage button
(`currentLev`), not from the RESULT.

**Liquidation is a TOUCH event, not a terminal value** — the reflection principle
doubles the probability against the naive estimate. Risk is heavily back-loaded:
at Vol 1 %/h and 3X it is ~0 % over 7d, 3 % over 14d, 15 % over 30d.

The touch formula lives once, in `touchProb(vol, b, hours)`; break-even (§3.11)
uses the same function — two copies of the reflection principle would inevitably
diverge.

**R² deliberately does not enter.** The position is not hedged against BTC, so
liquidation is caused by the coin's full move, not by the idiosyncratic part.

Side asymmetry is built in: price is unbounded upward, so at equal leverage a
short is always riskier than a long (Vol 1.0 %/h, 3X: long 14.6 %, short 29.6 %).

### 3.4 Margin risk — the fourth ceiling, HARD

`MAX_MARGIN_LOSS = 0.35`: exiting at the structural stop must not cost more than
35 % of margin. Professional replacement for «keep the stop within 10 %» — the
distance is set by the coin's structure, so what gets limited is the LEVERAGE,
not the stop.

The division `MAX_MARGIN_LOSS / dist` lives in exactly one function, `lMoney(dist)`
(inv. 20).

```
hard mode      ⇔  inv.capped === false
contribution   =  max( lMoney(dist), L_MIN )
decision fields   parts.money · moneyHard · moneyBelowMin
```

**The condition is exactly `capped`, nothing else.** An added clause
`src ≠ 'вход'` was rejected as arbitrary: at two different entries `dist` hits the
same 2σ floor, so the stop is mathematically identical and the rule must behave
identically. With the clause, an entry BELOW a broken low would have *lifted* the
limit — more risk buying more leverage.

**The 2σ floor participates in hard mode, the 6σ cap does not.** A stop cannot be
placed quieter than noise, so 2σ is an honest minimum distance and money rules
apply to it. A level clipped by the 6σ cap is drawn, not tradable; the row stays
informational.

**The `L_MIN` floor is mandatory (inv. 26).** `loss/margin = dist·L` is
independent of position size, so the money rule speaks about the SHARE OF THE
ACCOUNT, not about survival. Without the floor, 538 of 1230 control setups
received «no safe leverage»; with it, none. When the stop does not fit even at
`L_MIN`, `moneyBelowMin` rises and the board says to take a smaller share of the
account instead.

Measured price of the rule: 22 % of control setups get lower leverage; across
3243 comparable setups on both sides there is not one case of leverage rising.

### 3.5 FDV

`fdv_mc` in the badge next to the rank. Thresholds: grey < 1.5, yellow 1.5–3, red
> 3. **Context for unlock risk, never a standalone long/short trigger** — it says
how large future issuance is relative to float, i.e. which coins to check by hand.
Optional field (inv. 9); no max supply → not drawn.

### 3.6 Forecast uncertainty band — NOT IMPLEMENTED, reasoning fixed

`pred` is the conditional mean of only the part of the move BTC explains. The
idiosyncratic part is unforecastable by construction:

```
σ_idio(hour) = Vol·√(1−R²)      signal/noise = √(R²/(1−R²))
```

At typical R² = 0.15–0.36 signal/noise = 0.42–0.75, i.e. **the coin's own move
exceeds the part explained by BTC**. A 5–15 % simulation-vs-fact divergence is the
expected width of the distribution, not a model defect.

Consequence: a separate «signal/noise» metric is meaningless — it is identical to
R², already on the card. The practical answer to this risk is the liquidation
probability (§3.3), not a band on the forecast.

### 3.7 Board CRYPTO FUTURE — the work surface

Full-screen overlay (`#board`, z-index 5000), opened from a card. The card is the
shop window, the board is the desk; there is no duplication by construction. One
coin at a time, session state only.

**Block order lives ONLY in the concatenation at the end of `boardHtml`** — the
blocks are computed above in their original order because of variable
dependencies. Reordering means moving 13 strings, never the code.

```
1 ИТОГ·СТОРОНА·ПОТОЛОК   2 ПОЧЕМУ ЭТА МОНЕТА   3 ДИАПАЗОН 90 ДНЕЙ   4 ТОЧКА ВХОДА
5 ВЫБОР ПЛЕЧА   6 РАЗМЕР ПОЗИЦИИ   7 ГРАНИЦЫ СДЕЛКИ   8 ЦЕНА ВРЕМЕНИ
9 ЕСЛИ ИДЕЯ НЕ СРАБОТАЕТ   10 ЕСЛИ СРАБОТАЕТ   11 ЗАЩИТА ПОЗИЦИИ
12 ОТКУДА ПЛЕЧО   13 ДОВЕРИЕ К МОДЕЛИ
```

«ЗАЩИТА ПОЗИЦИИ» sits eleventh deliberately: 9 and 10 are outcomes, 11 is the only
action that converts unrealised profit into inability to lose, and 12–13 are
methodology and diagnostics. «СТОРОНА ПРОТИВ СТРУКТУРЫ» and «ВНИМАНИЕ» come
straight after the verdict: they are alarms, not sections.

**Position size — two input units.** `sizeMode ∈ {usdt, coin}`.

```
Identity: notional = qty·E = mrg·L.  ONE number is entered, the other derived.
usdt: mrg = posMargin;  notional = mrg·L;  qty = notional/E
coin: qty = posQty;     notional = qty·E;  mrg = notional/L
```

Switching the unit does not move position volume (recomputed through the identity
in `setSizeMode`, using the exact entry price from `entryState`, never a rounded
HTML attribute). In coin mode a leverage change keeps quantity and moves margin —
the correct order for «I want 1000 UNI».

**Pressed-button highlight is one law of the board.** Exactly one button lights in
each group: side, leverage, size unit, entry point. For the entry point the lit
button is the preset price matching the current one within 0.25 % — half the
0.5 % step of the −/+ buttons; if none matches, the pencil lights and that is
«своя цена».

**Funding in money:** `costUsd = |fr|·21·notional` (21 = 3 payments/day × 7 days),
identical to `cost% = |fr|·21·L·100` of margin. Both are shown; the block's colour
is the economic effect for the pressed side.

**Scroll anchor is mandatory.** The board re-renders wholly through `innerHTML` on
every action and every 30 s with the ticker. Restoring absolute `scrollTop` caused
a jump, because block heights ABOVE the reading point change between renders. What
is remembered is the section under the top of the screen and the offset inside it;
the key is the text of its `.bd-h`. Section gone → previous behaviour;
`scrollTop < 4` → no anchor.

**Metal on the frames.** The ring is a SECOND background layer: the block fill is
clipped to `padding-box`, the metal to `border-box`, and the border-wide gap shows
`linear-gradient(148deg, …)`. Radii stay exact (`border-image` breaks them) and no
new nodes, pseudo-elements or masks appear — decisive on a surface that re-renders
every 30 s. Highlights are near-white deliberately: at 1px and DPR 3 a soft
gradient collapses into one grey line.

**Switch is `:not([style])`.** Inline `style` on `.bd-sec` exists on exactly two
blocks — the alarms «СТОРОНА ПРОТИВ СТРУКТУРЫ» (red) and «ВНИМАНИЕ» (amber) —
where the border colour carries meaning. **Trap:** any new inline style edit on a
`.bd-sec` kills the metal on it; if an inline is needed, use a class.

### 3.8 «ШОРТ СОЗРЕЕТ, КОГДА»

Lives INSIDE block 2 «ПОЧЕМУ ЭТА МОНЕТА»; no separate section, so the block order
and anchor keys (inv. 15, 18) stay untouched. Drawn only when `boardSide = short`
and the bot supplied at least one of the two numbers.

Two PACE conditions — exactly the ones that currently cut a short candidate's
score in `scoreCandidate`:

```
1. eff14 <= EFF_TREND (0.60)      above -> the rise went in a straight line, score ×0.5
2. r7   <= r30·(7/30) − PACE_Z·sd_day·√7        PACE_Z = 0.25
```

Both thresholds are read from the same constants as the score (inv. 20).
Counter `N / M` in the header: `M` is how many conditions could be checked at all.
Colours: green when `done = known`, amber when partial, grey at zero. **Red is
deliberately unused** — «not ripe yet» is waiting, not danger.

Stated in the block's own caption: these are conditions of PACE, not of PRICE.
Price belongs to «ДИАПАЗОН 90 ДНЕЙ» and to the «СТОРОНА ПРОТИВ СТРУКТУРЫ» alarm and
must not be duplicated here.

### 3.9 Residual to BTC — `res7`

The coin's weekly move decomposes EXACTLY, with no remainder:

```
r7 = mkt + own      mkt = β₉₀·btc.r7 (market part)     own = res7 (its own)
```

**Beta by the sign of the REALISED `btc.r7`**, not by the slider: `up_beta_90` when
`btc.r7 ≥ 0`, `down_beta_90` when `< 0`. The slider is a hypothetical future; `res7`
measures the past seven days, and a scenario has no right to influence a
measurement of the past. No discontinuity at zero: the multiplier `β·btc.r7 → 0`
there. Consequently this beta may differ from `b=` in the `90d:` row, which is
chosen by the slider's sign — the divergence is normal and is named on the board.

**The measure is the sigma of the RESIDUAL, not the coin's full sigma.**

```
σ_res(hour) = Vol·√(1−R²)                    single-factor identity (§3.6)
z = own / ( Vol·√H_NOISE·√(1−R²) )           H_NOISE = 168 h
R² is the one PAIRED to the beta used: up_r2_90 / down_r2_90
R² clipped to [0, RES_R2_CAP], RES_R2_CAP = 0.90 — guard against dividing by ~0
```

Full sigma would systematically understate `|z|` (at R² = 0.42, by 24 %). No R² →
fall back to full sigma, which is conservative. No `volatility` → `z = null` and
the number is shown raw and called raw.

**Threshold `RES_Z = 1.0`** — a residual of exactly one weekly residual-sigma;
fires in ~32 % of weeks by chance. 0.5 was rejected: 62 % of weeks says nothing.

Four states (`cls`), each caption correct for ANY signs of `own` and `mkt`:
`own` (`|z| ≥ RES_Z`, green if `own ≥ 0`, red if `< 0`) · `market` · `quiet` ·
`unknown`. **Colour = significance, not trade side** — grey means «no own move»,
not «bad for a long».

Shown on the card as one line `Своё 7д: +X.X% · Zσ`, visible in all screen modes,
and on the board inside block 2 with the full audit. **Not in `scoreCandidate`** —
pure display, measured at zero predictive value (§3.10). Missing inputs → the
block is not drawn and the rest of the card lives (inv. 9).

### 3.10 Scoring backtest — `bench/backtest_bench.py`

Separate file, production untouched. Answers one question: does `scoreCandidate`
sort coins better than a lottery.

**Construction.** Zero copies of production math (inv. 21). Each run cuts
`scoreCandidate` + `has/clamp01/sigmaDay/volRegime` + `EFF_TREND/PACE_Z/
VOL_ABNORMAL` out of `index.html` and executes them with node; the fields
`cur/min/max/volatility/r7/r14/r30/vol7/eff14/vol_ratio` come from a block cut by
AST from `get_token_betas` in `main.py`. Editing either production file changes
the bench automatically.

**Data.** `data.binance.vision` monthly ZIPs (3 years of hourly candles), tail
topped up from `data-api.binance.vision`. Pair list from the frontend's `tokens[]`.

**Metric.** Excess return against the list mean: the score decides «which of the
28», not «where the market goes». IC = rank correlation of score with the future
per date, averaged, CI by block bootstrap; plus top-3 vs mean, worst drawdown by
score tercile, and three controls (shuffled score, «proximity to min90 only»,
«r7 only»).

**Modes:** `--probe` · `--selftest` · `--fetch` · `--verify` · `--run` ·
`--regimes` · `--stops` · `--res7` · `--funding` · `--lab-selftest`.

**`--verify` is the only mode that can fail in the DANGEROUS direction** — print
«matches» where nothing matched. Its rules are locked by `bench/verify_bench.py`
(offline): the measure is chosen by FIELD TYPE (levels `rel`, returns `pp`,
`eff14` `abs`); a non-zero exit code on any failure; comparisons counted PER FIELD,
not per coin; fields not comparable because of the archive's ~1-day lag are named
in the verdict; cache files starting with `_` are skipped.

**Selftest is mandatory before trusting any number.** Three worlds — pure random
walk (the reference factor must read 0), mean reversion (+), momentum (−) — ten
seeds each, because at SE(IC) ≈ 0.03 a single seed strays 2 SE about one run in
twenty. Plus a look-ahead check: the record for date `t` built from the full
series must be byte-identical to the one built from the series truncated at `t`.
Below ten seeds the selftest raises a FALSE ALARM by construction — it errs
towards declaring itself broken, never healthy.

**Standing result — the model is an attention sorter with measured zero
predictive power.** `scoreCandidate` IC across both sides and 3/7/14d horizons
lies inside [−0.006; +0.026] with CI95 crossing zero, on 145 weekly dates × ~24
coins, at a power that resolves |IC| ≥ 0.041. Shuffled control −0.033…+0.000.
Rank-1 follow-up: №1 beats the list median on 50 % / 48 % of dates. **Weights are
never tuned** — the rule «do not touch the weights under any outcome» was
registered before the run and holds.

### 3.10a Experiment lab — pre-registered measurements

Additive modes of the same bench; production untouched; rules registered BEFORE
data (inv. 23). One PRIMARY claim per experiment; everything else is exploration
at a doubled bar (|IC| ≥ 0.10, CI99). **A positive primary wires NOTHING into the
product by itself: the standing gate is a fresh confirmation run after +26 weeks
of new data.**

| Experiment | Primary claim | Result | Consequence |
|---|---|---|---|
| `--stops` | pooled measured/model calibration of the invalidation layer at 7d | LONG 0.88 [0.68; 1.07], SHORT 0.88 [0.74; 1.03] — CI covers 1 | touch model honest; no multiplier in §7 |
| `--res7` | LONG · 7d · contrarian residual, IC ≥ +0.05 | −0.009 [−0.048; +0.030]; all 11 exploration cells fail | `residual7` stays display-only |
| `--funding` | SHORT · 7d crowding-z, IC ≥ +0.05 | +0.003 [−0.030; +0.039]; all 8 exploration cells fail | no crowding factor; funding stays a cost |

Descriptive, no action by registration: 35 % / 42 % of stopped setups return to
entry within 7d; the only cell where measured exceeds model is the 6σ-capped LONG
bucket (3.5 % vs 0.9 %, n = 681), consistent with the fat-tail prior in §7.

**Lab selftest (`--lab-selftest`)** — known-answer worlds, offline: flat-vol GBM
→ stops ratio must read 1 (reads 0.93–0.98); wick world (one-sided intra-hour
spikes invisible to close-based σ) → must exceed 1 (reads 1.45–1.63); res-null /
res-reversion worlds → 0 / strongly positive; uncoupled / coupled funding worlds
→ 0 / +0.24…0.27. Two lessons recorded before real data: volatility clustering at
the 2σ floor pushes the stops ratio BELOW 1 (errs safe), and symmetric diffusive
jumps stay inside the estimated σ — only wick-like moves can push the ratio above 1.

**Capital-efficiency question, answered by identity.** P&L per dollar of margin =
`L · move`, and the engine sets `L ≈ risk_budget / dist`, so ranking by capital EV
is ranking by expected R-multiple and nothing else. Measured with a handicap
favouring the hypothesis: LONG IC(score, R) −0.027, SHORT +0.014; №1 above the
list median R on 47 % of dates. Cost spread between candidates is ~6 % of a
typical move whose sign is unpredictable. **No EV ranking.**

**Regime follow-up.** Look-ahead-free buckets (trend-up > +5 % 51 dates · range
±5 % 50 · trend-down < −5 % 41; expansion split 70 / 72) — all ten cells null at
the doubled bar.

### 3.10b Resolution ceiling — what this bench can and cannot see

Detection threshold is set by universe width, and the standing «no new coins»
decision fixes it permanently: **|IC| ≈ 0.06–0.07 for a single pre-registered
test, ≈ 0.09 for any search.** ~40 directional cells have been measured here; all
lie inside the null distribution for that number of tests. Effect sizes in the
external literature are produced on cross-sections of 84–500+ coins and locate the
profit in small, illiquid, high-cost assets — the exact complement of a 28-coin
top-perp list.

**Operative rule.** A new ranking factor is admissible ONLY on an external prior
that names an effect size THIS sample could resolve, on a cross-section shaped
like ours, at a 7–14 day horizon. «It predicts in the literature» is not such a
prior.

### 3.10c Next architectural gate

**THE GATE, IN ONE LINE.** The wide research bench is built the first time a named
tier-1 hypothesis arrives carrying an external effect size **≥ 0.030 IC, measured
on a LIQUID cross-section (top-100 by volume or equivalent), at a 7–14 day
horizon.** An effect size from a small-cap universe, or a claim of predictiveness
with no number attached, does not open the gate.

If triggered: Binance USDⓈ-M perpetuals, target **n = 120** (150 buys only
0.026 → 0.023 for 25 % more fetch; below 100 the tier-1 unlock is lost). Filters,
in order: ≥ 3 years of continuous hourly candles with no listing gap > 48 h
(binding filter) · median 24h notional ≥ $30M · exclude wrapped duplicates,
pegged assets and 1000X-style pairs · **delisted perps MUST be included for the
period they traded** — today's 28-coin bench is survivorship-biased by
construction. Bench-only, production untouched, no new runtime dependency.

**Transfer gate is a VETO, never a confirmation.** Any factor passing on the wide
universe is re-measured on the 28 traded coins; required: same sign, and the
28-coin point estimate inside the wide-universe CI95. That test resolves only
|IC| ≥ 0.060, so it can KILL a factor but can never bless one.

**The prize, sized honestly.** A validated IC = 0.030 factor is worth 0.57 % per
selection to the top-1 pick — about $34 per trade at $1.5k margin × 4X, ~$890/year
at 26 selections, and it would take ~2300 live trades to separate from luck. Even
a fully validated factor could never be confirmed by the Boss's own trading
experience; using it would be an act of trust in the bench. That is why the gate
is deliberately expensive.

**Build trigger is not perishable.** `data.binance.vision` is historical, so
building the wide bench in 2027 yields 2027's history including everything back to
2023. Building it now with no hypothesis queued buys a fishing expedition.

### 3.11 Position protection — «ЗАЩИТА ПОЗИЦИИ»

The other twelve blocks answer *«may I open this, and how big»*. This one answers
the question that exists only once the position does: **when can the trade stop
being able to lose money, and what does that cost.**

```
break-even  BE  = E·(1 ± c),  c = 2·FEE_TAKER + f,  f = ±|fr|·FUND_PAY_7D
                  sign of f = economic direction for THIS side (§3.1)
                  c clamped to [−0.9, +0.9] — pathological-rate guard only
arm price   ARM = E·(1 ± ARM_R·dist),  dist from invalidationInfo (§3.2)
                  never closer than BE — below BE a "break-even stop" locks a loss
scratch     P   = touchProb(|ln(ARM/BE)|, H_NOISE)           §3.3
                  armed → the row switches to |ln(cur/BE)|
top-up      add = notional/L_ceiling − mrg → liquidation moves to liqPrice(E, L_ceiling)
```

**Why 1R and nothing else.** R — entry to structural stop — is the only risk unit
this system measures. Any other trigger would be a newly invented constant.

**Taker on both legs.** A stop exit is a stop-market order; charging entry as
taker too errs to the safe side. Round trip = 0.10 % of notional = 0.10 %·L of
margin.

**Seven days everywhere,** so the leverage engine, the funding block and this one
cannot disagree.

**No threshold on the scratch probability, deliberately.** Whether a 47 % chance
of scratching is worth removing stop risk depends on the Boss's own hit rate,
which the system has never measured. A traffic light would look like a measured
verdict without being one.

**The scratch number is the point of the block.** Moving a stop to break-even is
normally believed free. On XRP-like inputs (Vol 0.9 %/h, 1R = 9.1 %) noise drags
price back to break-even within 7 days in **47 %** of weeks.

Degenerate cases are named, not hidden: `inv.capped` → the arm inherits a drawn
stop and says so · costs ≥ 1R → the arm collapses onto break-even and the
probability row is dropped · no `volatility` → probabilities disappear,
break-even survives · no invalidation level → break-even alone · no funding rate →
fees only. **Exactly one probability on screen at any time** (`pArm` before the
arm, `pNow` after).

Pure display: no output enters leverage, score, ranking or the invalidation level
(inv. 27).

### 3.12 Direction engine — veto cascade

**Principle: direction is decided by a CASCADE OF VETOES, not by a sum of
weights.** Nothing in it predicts anything. Each layer either asserts «the
geometry of this trade is bad» or «this prior is not admitted right now»; both are
measurable without a forecast. It therefore does **not** reopen the predictive
layer closed in §3.10b: no ranking factor is added and no weight is tuned.

```
Layer 0  REGIME     one per list      trend | range | stress
Layer 1  GEOMETRY   veto, no forecast R:R · noise floor · money · entry chase
Layer 2  CHANNEL    exactly one       mean reversion  XOR  continuation
Layer 3  CATALYSTS  veto only         manual registry, cannot raise a score
Layer 4  VERDICT    default = NO      trade | wait | watch
```

**Layer 0 — `marketRegime(btcStats)`**

```
z   = btc.r7  / (btc.volatility·√H_NOISE)          BTC's weekly move in its own σ
eff = btc.r14 / (btc.volatility·√(2·H_NOISE))      clipped to ±3
stress  if  btc.volatility ≥ VOL_HARD  or  z ≤ −REG_STRESS_Z
trend   if  |eff| ≥ EFF_TREND,  dir = sign(eff)
range   otherwise
```

`eff` is deliberately the same formula the bot uses for a coin's `eff14`, compared
against the same `EFF_TREND`: one threshold per system (inv. 20). **Known
property, measured:** under a driftless random walk `eff ~ N(0,1)`, so
`|eff| ≥ 0.6` labels ~55 % of pure-noise windows «trend». Accepted, because a
false trend label cannot produce a wrong direction — it narrows the admissible
side to one, and on a driftless market both channels are worth exactly zero.
No `btcStats` or no `volatility` → `mode = 'range'`, `known = false`, which is
exactly the pre-engine production behaviour (inv. 9). The regime label says WHICH
state the market is in and never HOW FAR into it the session sits; that second
quantity is measured in §3.16 and is not yet wired to any consumer.

**Layer 1 — `tradeGeometry(cd, E, isLong, dec, hi24, lo24)`**

Turns numbers the board already prints from advice into prohibition. Nothing is
recomputed: the target is the 90-day extremum, the risk is `dec.inv.dist`, the
money veto is read from `dec.moneyBelowMin` (inv. 20).

| Veto | Condition | What it prevents |
|---|---|---|
| target passed | `tgt ≤ E` (long) / `tgt ≥ E` (short) | trading toward a target already behind price |
| reward/risk | `reward/risk < RR_MIN` | a trade that must be right more often than wrong |
| noise floor | `reward/(vol·√H_NOISE) < TGT_SIGMA_MIN` | targets the market reaches by chop |
| money | `dec.moneyBelowMin` | a stop costing more than `MAX_MARGIN_LOSS` even at `L_MIN` |
| leverage | `!dec.ok` | «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» becoming a tradable card |

**Entry discipline — `wait`, not a veto.** Anchor = the 24-hour low for a long,
the 24-hour high for a short (already in the Binance ticker — zero new requests).
Beyond `ENTRY_CHASE_SD` daily sigmas from that anchor the card enters ЖДАТЬ and
prints the price to wait for. It forbids not «buying high» but «buying AFTER the
move» — chasing, not strength.

**Layer 2 — `momentumScore`, and the ban on adding channels.** `scoreCandidate`
is the mean-reversion channel and is not modified. The continuation channel is its
mirror: trend intactness (`eff14` in the side's direction), own strength (`res7`
z), weekly vs monthly pace, quality. **The two are NEVER summed** — summing
opposite priors is exactly what produced one coin ranked both long and short on
the same data. The regime admits one; the other is not computed. Quality and
penalties are shared through `qualityScore` / `scoreFinish`, lifted out of
`scoreCandidate` without a single arithmetic change (proven on 200 000 random
inputs, 0 mismatches). `trendPenalty = false` removes exactly the two `eff14`
penalties: continuation wants the trend intact, mean reversion wants it broken.

**Layer 3 — `catalystCheck`** (registry §3.15). Events older than one day
(`−1` back edge) or further out than `CAT_WINDOW_D` are ignored; first note wins.

```
conf !== 'confirmed'  →  may ANNOTATE its own side only, never veto      (inv. 39)
conf === 'confirmed'  →  dir !== my side  →  VETO, early return          (inv. 31)
                         dir === my side  →  note
dir = 'both'          →  vetoes both sides: two-sided event risk, zero code change
```

**Layer 4 — `directionVerdict`.** Default is NO TRADE. A side is emitted only when
everything lines up: regime admits the prior → channel ranks the coin → geometry
passes → no catalyst veto → the entry is not a chase. The score is computed
ALWAYS, at any outcome: a card without a score is invisible to sorting, and the
prohibition lives in `action`, not in silence.

**One coin can never receive both ЛОНГ and ШОРТ — structurally, not empirically:**

```
stress → neither side
trend  → only the side matching reg.dir
range  → only the side with the HIGHER mean-reversion score (tie → neither)
```

The range rule is load-bearing: a coin mid-range with a wide 90-day range can
clear R:R ≥ 2 on both sides simultaneously. Geometry filters bad trades; it does
not arbitrate direction. The regime does (inv. 30).

**Display contract** — inv. 33–36 carry it: number and word mean PLACE IN THE
RANKING and STRENGTH OF ATTENTION, the glyph (`stateMark`) means ENTRY STATE
(empty = trade, `~` = wait for the pullback with its price, `✕` = no trade); the
tier badge reads «Сильный / Средний / Кандидат / Фон» at thresholds 70/50/35;
`planLine` prints entry and target only where the engine allowed the trade; a card
below `TIER_MIN` moves to the expandable strip rather than vanishing; degraded
rows are never hidden.

**Known structural tension, deliberately not fixed.** `tradeGeometry` does not
take the regime: the target is always the 90-day extremum, i.e. a MEAN-REVERSION
target, while in `trend` the ranking comes from the CONTINUATION channel. A coin
with strong momentum sits near its 90-day extremum, so remaining reward is small
and R:R breaks against `RR_MIN`. The veto is substantively CORRECT in the observed
cases, and «a continuation target would have produced a better outcome» is a
hypothesis without a backtest, which inv. 32 forbids acting on. **Opening
condition:** an archive backtest comparing `RR ≥ 2` to the 90-day extremum against
a continuation target (e.g. `E + k·σ·√H`) on the same momentum-channel inputs.

### 3.13 Verdict journal — «вход → вердикт доски → факт»

**Built and running** (`journal.yml`, 13:00 UTC). A daily record of what the board
said about every coin — inputs, verdict, the catalyst registry in force, the engine
fingerprint — plus, 7 and 14 days later, what the price did. A measuring
instrument: nothing is displayed, nothing feeds back into any calculation
(inv. 27).

**Why it could not wait.** The verdict is not reconstructible after the fact:
`history.json` keeps betas, R² and rank only — no price, no min/max, no
volatility, no volume — and `scoreCandidate`, `tradeGeometry` and
`leverageDecision` all need exactly the fields it does not keep. Every unjournaled
day is lost permanently.

**Layout — one file per unit of work, never reopened.**

| Path | Written | Content |
|---|---|---|
| `journal/data/YYYY-MM-DD.jsonl` | once per date | `k:"s"` snapshot line per covered coin, `k:"x"` skip line per uncovered one |
| `journal/out/YYYY-MM-DD-h7.jsonl`, `…-h14.jsonl` | once per date × horizon | `k:"oh"` BTC header, then `k:"o"` per coin |
| `journal/runs.jsonl` | appended per run | `k:"r"` run line, `k:"g"` gap line per unrecorded date |

**Snapshot fields.** `d · ts · sym · pair · gen · age · px{src,cur,p24,qv,hi,lo,cnt}
· reg · cd (analysis_data row verbatim) · btc (coeffs.btc verbatim) · rp ·
long{…} · short{…} · cat{acting,hash} · fp{script,commit}`. Side block:
`rel · score · tier · ch · action · why · note · verdict · wait · tgt ·
geo{rr,reward,risk,tgtSig} · dec{ok,L,binding,moneyBelowMin,parts} ·
inv{dist,price,dStruct,capped,floored,sd,ref,src}`. Objects returned by production
functions are stored WHOLE and unrounded: a field not written today cannot be
recovered from a year-old record, and it costs bytes. Outcome line: `p0 · p1 · hi ·
lo` plus, per side, the ISO hour of first touch of `tgt` / `stop` / `wait` and
`first ∈ tgt|stop|tie|null`. `tie` means both levels fell inside one hourly candle
and the order is genuinely unresolvable — recorded, not guessed.

**Three standing decisions.**

1. **Daily, not hourly.** Daily resampling is worth exactly 1.00× against weekly
   at a 7–14 day horizon (consecutive dates share 6/7 of the forward window);
   hourly buys 24× the storage and zero independent observations. Reversed if the
   Boss starts trading intraday.
2. **Coverage is 25 of 28 by construction** — the three `fut:true` assets have no
   spot leg (§3.14) and Binance production hosts answer HTTP 451 from Actions
   (inv. 24). They are attempted every run and recorded as explicit skip lines, so
   the gap is measured rather than assumed. The venue test short-circuits ahead of
   all five classifier branches, so a `fut:true` asset can never increment
   `hardSkip`; the reason string still records what was observed:

   | Observed | Reason string | `hardSkip` |
   |---|---|---|
   | no row at all | `futures-only: no spot mirror pair` | no |
   | row present, dead | `futures-only: delisted spot mirror row` | no |
   | row present, **alive** | `futures-only: spot mirror row unexpectedly alive` | no |

   The third case contradicts the §3.14 declaration and additionally pushes
   `fut:true asset trading on spot: <SYM>` into `run.note`. A dead **spot** pair
   still hard-skips and still degrades `status`.
3. **`#N` is NOT recorded.** The board's number is produced inside `update()` by
   `byScore` → strip filter → `assignRanks`, which is not callable in isolation;
   recording it would mean reimplementing it (inv. 21 forbids that). It is fully
   derivable at analysis time from `score`, `rp`, `rel`, `tier`.

**What it is for, in order:** an audit trail of what the Boss actually saw · the
compensating control that makes `catalysts.json` safe (the acting set and its hash
sit next to every verdict) · eventually a live sample. It is NOT a backtest and
carries no predictive claim: §3.10b's resolution ceiling applies unchanged, and a
year of daily records is ~52 independent 7-day windows.

**Growth:** ~73 KB per day of snapshot data, plus outcome files. This is the only
unbounded artifact in the repository and the one thing the monthly audit watches.

### 3.14 Asset venue contract — 25 spot, 3 futures-only

**Boss's architectural decision, permanent.** Three of the 28 assets — **XMR, LIT
and HYPE** — exist for this system on **Binance Futures only**. The other 25 trade
on Binance Spot. This is a declared property of the asset inside this list, not an
observation about what some host answered on a given morning.

```
fut:true   XMR · LIT · HYPE        perpetual only, no spot leg in this system
default    the remaining 25        spot ticker + perpetual funding
```

**Consequence 1 — price source (inv. 12).** `fut:true` tokens are excluded from
the spot `?symbols=` list and priced only from `cachedFutTickers`; the dead-market
detector works on `count` alone.

**Consequence 2 — a ghost spot pair does not revoke the declaration.**
`data-api.binance.vision` still answers for `XMRUSDT` and `LITUSDT` with a
delisted, zero-volume row. The row exists; the market does not. Classifying by
what the host returned disagreed with the declaration and showed up not as an
error but as a permanently degraded `status` (inv. 41).

**Consequence 3 — the bench divergence in §7 is a source property.** The backtest
reconciles with production on 25 of 28 coins; the three that diverge by 7–9 pp on
returns are exactly these three — the bench reads the perpetual, CoinGecko reads a
spot index, and the basis is the difference.

**Consequence 4 — coverage is 25/28 permanently.** Every statistical statement
built on the journal is a statement about 25 assets. Closing that gap would
require a second price source bought for three rows.

Reversed if Binance relists XMR or LIT on spot with real volume: that is a
`tokens[]` edit plus this paragraph, not a code change anywhere else.

### 3.15 Catalyst registry — `catalysts.json`

The only external input of the direction engine, served next to `index.html` and
read by the frontend over ES5 XHR. **The data lives in the file; the rule lives in
`catalystCheck` and did not move.**

**Schema v1.**

```
{ "v":1, "updated":"YYYY-MM-DD",
  "items": { "SYM": [ { d, dir, kind, t, conf, src[], added } ] } }

d      ISO date of the event            dir   long | short | both
kind   unlock | protocol | listing | …  t     the string the card prints
conf   confirmed | disputed             src   array of source URLs
added  ISO date the entry was written
```

The file is ASCII-only and the printed string `t` is `\uXXXX`-escaped.

**Authority — `conf`, and the quorum behind it (inv. 39).** Externalising the
registry removed a control: before, a veto passed through a TZ, an Executor, a
pull request and an audit; after, it passes through one file edit. The
compensating control is that only `conf === 'confirmed'` may close a side,
compared exactly and case-sensitively, and **`confirmed` requires at least one
PRIMARY source** — the protocol, the exchange or the foundation, matched by host
on a dot boundary against the allow-list in `bench/catalyst_bench.js`. Two
aggregators repeating each other are **not** a quorum: authority, not repetition,
is the bar. The PRIMARY list is the registry's trust root and changes only through
a TZ.

An unverified entry annotates **only its own side**: the note prints under an
*allowed* trade and therefore reads as an argument *for* it, so a
contrary-direction event there would lie in the loudest place on the board.

**Unavailability is not emptiness (inv. 40).** Every failure path — HTTP ≠ 200,
unparseable JSON, `v ≠ 1`, missing `items`, network error, `status 0` — lands in
the same state: registry `{}`, `CAT_LOADED = false`, `CAT_ERR` set, banner on
screen with the reason. The board keeps working and says it is running without the
layer. Known inert edge: opening the board over `file://` gives `xhr.status 0`.

**The journal reads the same file** and refuses to record a day whose registry it
could not read, in every mode, with a non-zero exit. `cat.hash` is sha256 over
canonicalised `items` — object keys sorted, array order preserved, because within
a coin the order decides which note wins.

**Registry content is analyst work under a TZ.** Current content: one `confirmed`
ZEC entry, `dir:'both'`, primary source, for the NU7 vote resolution on 14.09.
Entries that no host confirms are deleted rather than demoted — a `disputed` entry
still annotates its own side, so keeping one keeps printing an argument built on a
date nobody confirms.

### 3.16 List exhaustion — the day-range measure

**Built to the measure only; nothing on screen reads it yet.** The gap it exists
to close: `regimeBanner` names the regime and says nothing about how far into it
the session already sits. On 2026-08-22 the geometry layer refused 24 of 25
covered coins while the banner printed «ТРЕНД ВВЕРХ — счёт по каналу импульса» in
green, on a day whose list median day-range was 2.43 times a diffusive day.

```
dayRangeRatio(hi, lo, cur, vol) = (hi − lo) / ( cur · sigmaDay(vol) · √(8/π) )

E[range] = σ·√(8/π) for Brownian motion — the denominator is DERIVED, not chosen
sigmaDay is the single site of the daily-σ conversion (inv. 20); this function
never recomputes vol·√24 of its own
null on any missing or non-finite input, on cur ≤ 0, vol ≤ 0, hi ≤ lo, on an
underflowed denominator and on an overflowed ratio — a missing measurement never
arrives downstream as a zero

listExhaustion(rows) -> { median, n, abnormal }
n counts only rows that produced a ratio; n < 8 → median null, abnormal false
```

**σ is close-based and therefore understates true range, so the reading is above
1 by construction.** That is why the acting threshold is a percentile of the
measured distribution and can never be a round number picked by eye.

**Nothing predictive is added.** This measures what the session already did, in
the same standing as §3.12 Layer 1: it asserts «the geometry of entering right
now is bad», which is measurable without a forecast. No ranking factor, no weight,
and §3.10b's resolution ceiling is untouched.

**Quorum `n ≥ 8` is load-bearing.** A statement about the list computed from three
coins is not a statement about the list, and the banner is the one list-wide
element on screen.

**The estimator and its calibration must share a universe.** The reference figures
and the journal replay are both 25 spot assets; the three `fut:true` assets read
their range off the perpetual while `volatility` comes from a spot index (§3.14
Consequence 3), so a live estimator that included them would not be the estimator
the threshold was measured on. Coverage is 25 of 28 by declaration (inv. 41).

**Registered adoption rule, fixed before the number exists (inv. 23).**
`DAY_RANGE_ABNORMAL` = the pooled 90th percentile of the coin-day distribution
over the archive, rounded to two decimals, taken as-is; adopted only inside
`1.60 … 4.00`, and outside that window the consumer is not built and the answer is
a new TZ, never a nudged number. Once adopted the constant is pinned to the run
that produced it (inv. 46).

**State at this revision.** `dayRangeRatio` and `listExhaustion` exist in
`index.html` and are reachable from nothing: `abnormal` is hardcoded `false`,
`reg.day` is referenced nowhere, and no output enters `scoreCandidate`,
`tradeGeometry`, `leverageDecision`, `directionVerdict` or the journal writer.
The constant does not exist, because the archive is unreachable from an
implementation session (inv. 44) and the calibration has never run. Measured on
the two journaled days by replaying the production functions: **1.69** on
2026-08-21 (6 of 25 coins above 2.0) and **2.43** on 2026-08-22 (20 of 25). Two
days are not a distribution and do not bound the percentile.

---

## 4. Invariants — DO NOT BREAK

1. `coeffs.json` schema is **additive-only**; the bot's `err_result` is key-synchronous with its success result.
2. New coins enter only through `TOKENS` (bot) + `tokens[]` (frontend); check CoinGecko id, spot pair, futures pair, quota. No spot pair but a perp → `fut:true` is mandatory. (Standing decision: no new coins.)
3. `history.json` ≤ 720 points; reads must handle `truncated` via `raw_url`.
4. `STALE_WARN 75` / `STALE_CRIT 130` min ↔ the hourly Shortcut tempo (no cron, §1); change only as a pair. **Inside the 02:00–09:00 night pause a red threshold does not by itself mean failure:** age is compared against the last SCHEDULED run at 01:50, tolerance one missed hour; two missed hours is a failure.
5. Spot ticker `?symbols=`: HTTP 400 → the frontend sticks to the full 1.2 MB ticker until reload. Keep delisted pairs out; mark futures-native ones `fut:true`.
6. `applySavedOrder`: new coins go to the END of the saved order.
7. The client-side password is decoration. Secrets live only in GitHub Actions env.
8. Every bot `requests` call carries `timeout=30`.
9. **The frontend must survive the absence of any new coeffs field** — both bot↔frontend combinations must work.
10. Rebranding a coin: change the display name and the Binance pair; **KEEP the CoinGecko id** — ids are permanent, a new id loses 90 days of history.
11. Three protective card states: «НЕТ ПАРЫ» · «ТОРГИ ОСТАНОВЛЕНЫ» (`count = 0` or empty book → calculations off) · amber «Расхождение источников» (price outside 0.5×min…1.5×max).
12. `fut:true` tokens: price only from `cachedFutTickers`, excluded from the spot `?symbols=` list; the dead-market detector works on `count` alone.
13. **Leverage math is validated — change only with a full bench re-run.** Three ceilings (§3.2), 7-day horizon for all three, minimum, round DOWN. Margin risk is the fourth (§3.4).
14. **Everything the Boss controls must derive from `currentLev`.** A block computing from the RESULT while the pressed button says otherwise produces a screen where liquidation moves and probabilities do not.
15. Board block order lives ONLY in the concatenation at the end of `boardHtml`; the block code must not be reordered (variables `notional`, `qty`, `mrg`, `qtyTxt` are declared in the size block and used below).
16. **Size unit identity `qty·E = mrg·L`.** One number is entered, the other derived; switching `sizeMode` never changes position volume. The entry price for the recomputation comes from `entryState`, not from a rounded HTML attribute.
17. **Exactly one button lights per group** (side, leverage, size unit, entry point). The 0.25 % entry-highlight tolerance is tied to the 0.5 % −/+ step: change only as a pair.
18. **Board scroll is restored by SECTION ANCHOR, never by absolute `scrollTop`.** The anchor key is the `.bd-h` text, which must stay unique within the board.
19. Min/Max blinking and the running edge borders are Boss-approved: never remove; improvements may be proposed, never silently applied.
20. **One number per threshold, system-wide.** `EFF_TREND` and `PACE_Z` are read by both `scoreCandidate` and «ШОРТ СОЗРЕЕТ, КОГДА»; `RES_Z` and `RES_R2_CAP` only inside `residual7()`; `FUND_PAY_7D`, `FEE_TAKER`, `ARM_R` likewise; `touchProb()` is the single touch formula and `probTxt()` the single probability-to-text rounding; `lMoney()` the single `MAX_MARGIN_LOSS / dist`. A threshold hardcoded in a second place will eventually diverge, and the screen will start explaining the score with the wrong number.
21. **A bench contains no copy of production math.** Formulas are cut out of `index.html` and `main.py` at every run. A hand-pasted copy diverges silently and the bench starts verifying code that is not in production.
22. **A check that passes with no data is forbidden.** Any validator must count the objects it compared and fail on zero.
23. **Experiment rules are fixed BEFORE the data, and the implementation of the rule is proved by a known-answer control BEFORE real data.** A naive price-on-time regression called 70 % of pure random walks a trend — the rule was right, the implementation was broken; replacing it after seeing results would have been fitting.
24. **Binance production hosts are unreachable from GitHub Actions — HTTP 451.** Only `data.binance.vision` and `data-api.binance.vision` work from a runner.
25. **`| tee` in a workflow step returns `tee`'s exit code, not Python's.** Without `set -o pipefail` a failed step looks green. All bench steps run `shell: bash -euo pipefail`.
26. **The money ceiling never kills a trade.** Margin risk participates in the `min` but with an `L_MIN` floor: `loss/margin = dist·L` is size-independent, so it is a rule about the SHARE OF THE ACCOUNT. Only the first three ceilings may produce «БЕЗ БЕЗОПАСНОГО ПЛЕЧА».
27. **«ЗАЩИТА ПОЗИЦИИ» and `res7` are pure display.** No output of either enters leverage, score, ranking or the invalidation level. Making a display block influence a decision is a separate change with its own justification.
28. **A class assembled by concatenation is invisible to text search.** `renderButtons` builds exactly two: `'side-btn' + ' a-' + mode` and `'stress-btn' + ' s-' + mode`. Any future CSS cleanup must resolve such sites by enumerating THEIR OWN loop; merging the two enumerations invents `s-long`/`s-short` and hides real orphans. Automated in `bench/clean_bench.py`.
29. **A verifying mode must RETURN an exit code.** A function without `return` yields `None`, `sys.exit(main() or 0)` turns it into zero, and a failed comparison looks successful while the screen honestly prints the failure. Printing is not returning.
30. **One coin — ONE side.** The guarantee comes from the regime layer, not from geometry: stress → neither, trend → only the market's direction, range → only the higher mean-reversion score. A mid-range coin passes R:R ≥ 2 on BOTH sides; removing the regime rule restores the contradiction.
31. **A catalyst can ONLY veto.** It can never raise a score and never override a geometry veto. A catalyst placed above geometry is what produced a short on the floor of a range.
32. **Geometry does not predict and is not required to.** On a random walk `E[R] = 0` under ANY selection — a theorem, confirmed by the `--control` run (−0.001 at 2SE 0.080). Any future claim that «a veto raised accuracy» must first explain where drift or costs came from.
33. **One channel, one meaning, and no channel argues with the glyph.** NUMBER + WORD speak about PLACE IN THE RANKING and STRENGTH OF ATTENTION; the GLYPH (`stateMark`) speaks about ENTRY STATE: empty = trade, `~ $price` = wait for the pullback, `✕` = no trade. The distinction may never be carried by colour alone and may never erase the number. Both surfaces take glyph and verdict text from the SAME functions (`stateMark`, `verdictNote`) — a board silent about the card's prohibition is the same defect. Colour carries STATE, not score quality: at `action === 'none'` the badge fades to `#888` while the tier colour remains on `trade` and `wait`. Tier vocabulary is «Сильный / Средний / Кандидат / Фон», badge format «Сильный #1 — 91», thresholds `TIER_STRONG/TIER_MID/TIER_MIN` = 70/50/35. The market-cap rank carries no «#»: that symbol belongs to the score ranking alone.
34. **The number is a PLACE IN THE RANKING and every scored card has one.** Order is strictly by score (`byScore`, a 0.05 tie window resolved by market-cap rank), numbering continuous 1..N over the displayed list. Entry state may neither reorder the list nor take a number away. Only rows without a score and rows collapsed as irrelevant to the side (`row.off`) go unnumbered. `byScore`, `assignRanks`, `tierBadge`, `stateMark`, `verdictNote` are separate functions precisely so a bench can check them.
35. **Only an allowed trade prints an entry price and a target.** `planLine` is empty at `action === 'none'`: printing «entry / target» where geometry or regime refused invents a recommendation the model does not have. No number in the line is recomputed — target is the same 90-day extremum `tradeGeometry` used, stop is `dec.inv.price`, R:R is `geo.rr` (inv. 20). The line exists only for tiers Сильный and Средний.
36. **A score below `TIER_MIN` leaves the main board but never disappears silently.** Such coins go into the same expandable strip as coins at the irrelevant edge of the range, with separate reason counters. Check order is fixed: weak score first, then position — otherwise one coin lands in both groups and the counters stop matching the strip length. Degraded rows (no pair / dead market / no metrics) are NEVER hidden: they are operational warnings, not candidates.
37. **Silence must be explained, and the explanation must be machine-readable.** A run that recorded nothing must return a NON-ZERO code; every run must leave one grep-able line with `generated_at`; the night pause must differ from a failure by rule (`freshnessState`), not by eye. A gap in the sample with no recorded reason is indistinguishable from «no events», and a sample with unexplained gaps supports no statistical statement. Hence the journal writes a missing date as a gap LINE, not as an absent line. **A bench not wired into `bench.yml` never executes and is not a control.**
38. **The journal is an instrument, and a record in it is immutable.** (1) The verdict is produced by EXECUTING the production script — functions are cut out of `index.html` and called by name (inv. 21). **A second implementation of any rule, threshold or formula is banned in any language and any file.** (2) A file once written is never reopened — not to append an outcome, not to fix a typo; the outcome lives in a separate file joined by key, and a re-run that finds an existing file writes `dup` and exits zero. Immutability is physical, not promised, because a record that can be rewritten stops being evidence exactly when the result is unwelcome. (3) Next to the verdict lies what can explain it: the acting catalyst set and its hash, the script fingerprint and the commit.
39. **Only a CONFIRMED catalyst may veto.** The registry is a freely editable file and a veto changes the verdict, so the right to close a side is granted by exactly `conf === 'confirmed'` — exact, case-sensitive; a missing field, `'CONFIRMED'` or any typo is NOT a confirmation, and every refusal errs safe. Confirmation requires a **primary source** (protocol, exchange, foundation) matched by host on a dot boundary against the PRIMARY allow-list; aggregators repeating each other are not a quorum, and the allow-list changes only through a TZ. An unconfirmed entry may annotate, and only its OWN side. Inv. 31 is neither weakened nor strengthened by this.
40. **An empty registry and an UNAVAILABLE registry are different states and must render differently.** A loader that did not get the file for any reason must leave the registry `{}`, raise `CAT_ERR` and put a banner on screen carrying the reason, while the board keeps working (inv. 9). The journal is stricter: a day whose registry could not be read is not recorded AT ALL, with a non-zero exit, in every mode — a verdict without a known catalyst set is not explainable after the fact (inv. 38(3)).
41. **The declared venue is read BEFORE the degradation ladder.** `fut:true` is a DECLARATION (§3.14), not an observation, so a skip on such an asset is DECLARED coverage in any form it takes and never raises `hardSkip`. The reverse order already cost the `status` field: a mirror served a delisted row and a healthy system reported `partial` every day. The reason is still MEASURED in three distinct strings, and a live spot pair on a `fut:true` asset must reach `run.note` — a contradiction of the declaration may not pass quietly. The rule is wider than the journal: any future consumer of `tokens[]` asks the declaration, not the host.
42. **A bench must execute production with the SAME external input as production.** Three board benches ran the board with an empty `CATALYSTS` for eight days because the sandbox has no `XMLHttpRequest`: the loader failed silently and the benches reproduced a configuration that exists neither for the Boss nor on Pages. Therefore: the registry is read from the checkout by the SAME loader as production (inv. 21), injection happens AFTER `vm.runInContext` (otherwise the production line `var CATALYSTS = {}` overwrites it), and a missing or corrupt file fails the bench NON-ZERO — there is no fallback to an empty registry.
43. **A check count must be a count.** The number a bench prints as «checks» is used as proof of control volume and as the input to inv. 22, so it must count comparisons, not be estimated as a product of unrelated quantities. The counter is incremented at the comparison site, the gate total is the sum of those counters, and any discrepancy is explained term by term. A quantity that is merely measured and printed — scenarios, rows, lists — is not a check.
44. **External data is fetched on a runner, never in an implementation session.** Inv. 24 names what a runner can reach; this names where a fetch may happen at all. An Executor session's egress refuses every market host at CONNECT — archive, mirror, both production hosts, CoinGecko — so a stage needing external data cannot execute there however well it is written. Any TZ stage requiring external data is therefore specified as a workflow step and nothing else, and a TZ that asks for an in-session fetch is blocked before it starts. TZ-10 Stage B was specified as a session run: the instrument was correct, complete, self-tested — and returned no number.
45. **A differ returns zero on identical input.** Any comparison offered as no-regression evidence is first run with the SAME revision on both sides and must report zero differences, and a transformation applied to one side is applied to the other. `prot_bench.js`'s optional baseline suite strips one section from the candidate only, so it reports six failures against a byte-identical baseline — a stale expectation a self-comparison would have caught the day it was written. Identity is the known-answer control of a comparator (inv. 23); a comparator never proven on identity supports no claim about a real diff.
46. **A calibrated constant is checked against its calibration record.** A production number derived from a measurement lives in two places — the constant in the source and the committed output of the run that produced it — and a bench inside the gate compares them on every push. Inv. 23 fixes the rule before the data; this fixes the number to its run afterwards. A constant that agrees with nothing can be moved silently in either direction, and the move is invisible precisely because the number looks measured.

---

## 5. Limits

- **CoinGecko: the bot runs WITHOUT a key.** `main.yml` passes only `GIST_TOKEN`, so `api_key = None` → public access, no monthly quota, IP-rate-limited on the runner, handled by `REQUEST_GAP_SEC = 1.0` and three retries.
- **The free Demo key must NOT be attached at the current schedule.** Demo gives 100 calls/min but caps at 10 000/month; consumption is 17 runs/day × 30 calls ≈ 15 300/month plus `push`-triggered runs. A Demo key would create a cut-off around the 19th–20th that does not exist today. Attach only together with a cut to ≤ 10 runs/day.
- Binance spot ticker with `symbols`: weight 40, ~12 KB (full ticker: weight 80, ~1.2 MB).
- Binance `fapi/ticker/24hr?symbol=`: weight 1 × number of `fut:true` tokens, every 30 s.
- Gist API: files > 1 MB are truncated (handled through `raw_url`).
- Detection ceiling of the bench: |IC| ≈ 0.06–0.07 single test, ≈ 0.09 for a search (§3.10b).
- **An implementation session reaches no market host at all** — archive, mirror, production and CoinGecko are all refused at CONNECT. Every fetch happens on a runner (inv. 44).

---

## 6. Release checklist

1. `python3 -m py_compile main.py`; `node --check` on the extracted `<script>`.
2. `debug.json`: every coin has `matched_90d > 120`, `returns_14d ≳ 300`, `error = null`.
3. Frontend: no NO DATA / NO BETA cards; Conf, ρ, МДЛ and both R² coloured; slider edges → `pred > 0`.
4. `fut:true` cards: price arrives, and the spot list does not contain them (ticker ~12 KB, not 1.2 MB).
5. Board: block order per §3.7; exactly one button lit per group; `notional` unchanged when switching МОНЕТЫ/USDT; a leverage change in coin mode moves margin, not quantity; funding shows both sum and % of margin; «ЦЕНА ВРЕМЕНИ» computes from the pressed button, not from the RESULT (inv. 14). Reference case (UNI, E = $10.00, 4X): 1000 USDT → notional $4000, 400 UNI; switch to coins → 400 UNI, margin $1000, same notional; `qty = 1000` → notional $10 000, margin $2500; at 2X margin $5000, notional unchanged. Funding +0.0100 %/8h at notional $11 110 → $23.33 per 7 days.
6. Board in SHORT mode: «ШОРТ СОЗРЕЕТ, КОГДА» shows `N / M` and both thresholds; absent entirely in LONG; on a `coeffs.json` without `eff14`/`r7`/`r30` the block disappears and the rest of the card lives.
7. Two-way compatibility (inv. 9).
8. `coeffs.json`: `btc` carries non-null `r7/r14/r30`; the frontend works on an OLD `coeffs.json` without them.
9. Frames: all board blocks and the hero show the metal ring; the two alarms keep red/amber borders WITHOUT metal; corner radii intact.
10. `res7` (§3.9): the `Своё 7д` line with its sigma on the card, visible in ОБЗОР; the board block inside «ПОЧЕМУ ЭТА МОНЕТА»; `market + own` reconciles with `r7` to the displayed digit; on a coin without 90d betas the block disappears and the card lives; at `sc = null` the section stays and says the score was not computed.
11. Direction engine: no coin carries both ЛОНГ and ШОРТ; a card with `action = 'none'` prints no entry or target; the glyph and the tier badge agree (inv. 33–35).
12. Catalyst layer: with the file served, the banner is absent and a `confirmed` entry vetoes the opposite side; with the file removed, the banner appears with a reason and the board keeps working (inv. 40).
13. Hard margin ceiling (§3.4): at `capped = true` the fourth row stays informational without the «← ограничитель» marker and the caption reads «Три независимых потолка…»; at `capped = false` it joins the list, can bind the RESULT, and the caption reads «Четыре…». Under no data does it produce «БЕЗ БЕЗОПАСНОГО ПЛЕЧА» (inv. 26).
14. Position protection (§3.11): the block is eleventh; break-even is further from entry when funding is «я плачу» and nearer when «мне платят»; with price at entry the status line says so; on a coin without `volatility` only the probabilities disappear.

**Bench triggers.** Editing `verify_against_live` → run `bench/verify_bench.py`
(offline, ~20 s, must give 0 failures). Editing `scoreCandidate`, `window_stats`,
`window_vol` or `volume_expansion` → run `bench/backtest_bench.py --selftest`.
Any production edit → the full `bench.yml` gate, 11 steps.

---

## 7. Deliberate simplifications

- Beta on simple returns ≈ log returns at an hourly step.
- Liquidation: one MMR = **1.25 %** for everyone, no tiers, no fees, no funding.
- Reaction buffer of 12 h — an estimate of how long a position may stand unattended (sleep, work). Not measured, chosen. It sets the structural ceiling directly: doubling `H_REACT` cuts leverage by about a quarter.
- Card range min/max is 90d; the invalidation reference is 30d with a 90d fallback.
- Funding in money uses the CURRENT rate extrapolated over `FUND_PAY_7D = 21` payments. The rate floats — this is an estimate, not an exchange commitment.
- One fee for everyone: `FEE_TAKER` = 0.05 % per leg, both legs taker, no VIP tiers, no BNB discount, no slippage. The error points to the safe side.
- BTC→alt lag is not modelled: hourly bars are coarser than the real lag. Revisit only on minute data.
- Alpha (the regression intercept) is not extrapolated — at 14d it is indistinguishable from zero.
- Unlocks are deliberately NOT automated.
- Liquidation probability (§3.3) assumes normality and constant volatility. Crypto tails are fatter and volatility clustering is unmodelled → **the true probability is higher than computed**; the figure is a LOWER BOUND. Measured at 7d and typical 2σ–6σ distances the same touch formula is honest and even conservative (measured/model 0.88, CI95 covers 1 on both sides); beyond the 6σ clip the far tail confirms the prior (3.5 % measured vs 0.9 % model on the long side). **Crediting the 0.88 into the calculation is REJECTED:** the CI covers 1, the understatement is explained by clustering (so the correction would break exactly in an expansion regime), and `touchProb` does not enter leverage at all — all four ceilings are distance-based.
- The backtest reconstructs 82.5 % of the long score and 86 % of the short: market-cap rank and Binance turnover are historically unavailable, so the quality block runs on `vol_ratio` alone, through production's own missing-field path (inv. 9). Both inputs move slowly across the list, so their contribution is close to a constant tilt.
- Backtest vs production reconciles on 25 of 28 coins (median divergence: prices 0.06–0.12 %, `r7` 0.32 pp, `r14` 0.26 pp, `r30` 0.31 pp, `eff14` 0.02). The three that diverge are exactly the `fut:true` assets — a source identity, not an error (§3.14).

---

## 8. Closed decisions — do not re-propose without a new argument

| Idea | Why it is closed |
|---|---|
| 5d beta / R² | SE(β) at 5d is ±17…31 % vs ±10…18 % at 14d — adds variance, not information |
| «Signal/noise» as its own number | identical to √(R²/(1−R²)) — a duplicate of the R² already displayed |
| Automating unlocks | no reliable free source, dates drift, affects ~5 coins |
| TVL | applies to a quarter of the list, moves conviction over weeks — REVIEW material, not card material |
| Futures liquidity | on top Binance perps the Boss's size does not move the book; a dead market is caught by the detector |
| Token identity layer | over-engineering |
| Aurora animation | built and removed by the Boss: `mix-blend-mode: screen` on a dark theme raised grey, not colour, and two blurred 200 %×220 % layers at DPR 3 cost tens of MB of GPU texture |
| Global highlight of the «recommended» leverage button | the recommendation is per coin; a global button cannot express it |
| Liquidation heat map | no free source — vendor maps are models rebuilt from OI and price, and Binance `forceOrder` returns at most one liquidation per second per symbol. Squeezes live for hours; the Boss holds 1–14 days |
| «TP before SL» probability | without drift it equals `b/(a+b)` — identical to the risk/reward already in «ГРАНИЦЫ СДЕЛКИ». The system cannot estimate drift (§3.6), so the number would look like a measured edge without being one |
| Spot/perp basis | `premiumIndex` already returns `markPrice` and `indexPrice`, but Binance computes mark price from the same premium index as funding: basis and funding are mechanically one quantity in two forms, and funding is already on the board |
| Tuning `scoreCandidate` weights | measured zero over 3 years and 28 coins at sufficient power. Turning weights against a null result is pure overfitting; the rule «never touch the weights» was registered before the run |
| Market regime as a scoring switch | ten of ten cells null at the doubled bar on a powerful split (51/50/41 dates, expansion 70/72). Expansion is already implemented where it is legitimate — in the risk ceilings §3.2 |
| CoinGecko as a bench source | free tier gives 365 days → 39 dates → resolves only \|IC\| ≳ 0.060. Fine for reconciliation, not for a test |
| **Open Interest — closed permanently, as signal AND as display** | (1) funding is the market-clearing PRICE of the same imbalance and is measured at zero with a tight CI, so the conditional probability that the quantity measure carries a signal the price does not is far below 10 %; (2) power: our sample resolves \|IC\| ≳ 0.06 and a plausible OI effect at 7–14d sits below that — a test without resolving power is not run; (3) the display «new money / position closing» rested entirely on future directional use. Reversed only by external evidence at an effect size our sample could resolve |
| Ranking by expected profit on capital ($1–2k) | reduces by identity to ranking by expected R-multiple; measured with a handicap favouring the hypothesis — IC −0.027 / +0.014 |
| Nonlinear factor-interaction layer | (1) the source locates the profit in small, illiquid coins — the complement of our list; (2) a 5×5 double sort needs ~20 coins per bucket and we have ~24 in total; (3) a family of 45–66 interactions needs a true \|IC\| ≈ 0.087–0.089, more than any effect ever measured here |
| Order flow / microstructure as a ranking factor | the published predictor is **world order flow** — one number per date, common to all coins, so its cross-sectional IC is identically zero. The quoted R² are contemporaneous, not predictive, and the data is a paid multi-venue aggregate |
| Cross-sectional term-futures basis | (a) perpetual basis = the premium index behind funding, measured zero; (b) the term contracts overlap our list on six coins, and a cross-section of six resolves only \|IC\| ≳ 0.18; (c) the factor decays exactly at our 7–14d horizon |
| ML rankers, GARCH, on-chain/TVL as ranking inputs | 28 coins × ~145 dates guarantee overfit; ±30 % vol forecast error sits inside one leverage step and is absorbed by rounding down; on-chain moves on a weekly scale and covers a quarter of the list |
| 7d/30d horizon switch | deliberate: scaling is manual (√H) and an extra control invites tuning the horizon to the desired leverage. Revisit if the holding period starts changing systematically |

---

## 9. History

Removed. The migration log lived here until revision 2026-08-22-b; the record is
git history plus `CryptoReports/**`, both of which are permanent and immutable.
Nothing in this map depends on it.

---

## 10. Open queue and gates

Each item states its trigger. Nothing here is scheduled work; an item is picked up
only when its trigger fires.

| Item | State | Trigger to act |
|---|---|---|
| Wide research universe (n = 120) | not built, gated | a named tier-1 hypothesis with external effect size ≥ 0.030 IC on a liquid cross-section at 7–14d (§3.10c) |
| Regime hysteresis | not built | the Boss reports the regime label flapping between renders. Not built pre-emptively: a second trend constant on speculation violates inv. 20 |
| Continuation target for `tradeGeometry` | not built, gated | an archive backtest comparing the 90-day extremum against a continuation target on the same momentum-channel inputs (§3.12) |
| Journal outcome layer at scale | running | nothing — h7/h14 files appear automatically 7 and 14 days after each snapshot |
| Journal storage growth | watched | ~73 KB/day. Act if the repository becomes unwieldy; records are immutable (inv. 38), so the answer is archival, never deletion |
| Catalyst registry content | live, one confirmed entry | analyst work, delivered as a TZ; entries never promoted to `confirmed` without a primary source (inv. 39) |
| `DAY_RANGE_ABNORMAL` and the banner consumer (§3.16) | measure built, consumer not built | an archive run of `bench/exhaustion_calib.py` on a runner (inv. 44). Adopted as-is inside 1.60…4.00; outside it the consumer is not built and the answer is a new TZ |
| `prot_bench.js` optional baseline suite | broken — six failures against a byte-identical baseline | it is a prerequisite of any no-regression claim (inv. 45), so the first change needing one |
| `bench.yml` Node 20 pin | watched | GitHub already forces the actions onto Node 24 with a warning. Act when a step fails or the whole gate can be re-run as the validation |
| Beta history in `history.json` | reserved | future analysis of beta stability and horizon calibration |

**Standing decisions.** No new coins beyond 28 · weights are never tuned · the
directional layer is closed at the current evidence level: the machine owns risk,
sizing, honesty and geometry, the human owns direction via catalysts and REVIEW.
