# SYSTEM MAP — Pro Crypto Tool

Technical contract of the live system: architecture, data flow, modules,
dependencies, invariants. Consult before any code change and when interpreting a
metric. Nothing here is history — the record of how the system got here is git
history plus `CryptoReports/**`. Workflow, roles and acceptance live in the
Architect's canon and in `EXECUTOR-INSTRUCTIONS.md` (the contract); this map
states only what the system is.

**Language.** English, except on-screen strings and board block names, which are
quoted verbatim in Russian because that is what the code prints.

---

## 0. Fingerprint

**Revision 2026-09-02-a.** Baseline: TZ-23 merged into `main`; implementation
commit `5fc2da5`, report
`CryptoReports/TZ-23-main-workflow-paths-allowlist-report.md`. **The
baseline names the implementation commit, not the merge commit** — a merge commit
carries no content, and content is what this block pins.

**The baseline moved and the file table did not, which is the correct pair here.** TZ-23
edited `.github/workflows/main.yml` — a workflow, not a file this block fingerprints — so
`index.html`, `main.py`, `catalysts.json` and the calibration record are unaltered and the
gate holds at thirteen steps and 1 250 739 checks, verified term by term against the map's
own totals. The three `2026-08-30` letters were documentation revisions on the TZ-21
baseline: `-d` recorded TZ-22's measurement where `-c` denied having one, `-e` corrected a
§10 row naming a TZ number for a repair that became contract **v15**, and `-f` recorded
TZ-24 closing the §6a discovery question in the negative. **`2026-09-01-a` is a documentation
revision on the same TZ-23 baseline:** no file this block fingerprints moved, the gate holds
at thirteen steps and 1 250 739 checks, and what changed is the analytical engine's own
governing text — `ANALYST-INSTRUCTIONS.md` to revision `2026-09-01-c` and
`EXECUTOR-INSTRUCTIONS.md` to **v16**, neither of which this table has ever fingerprinted
because neither is a production file. **`2026-09-01-c` is a third such revision on that
same baseline:** no file this block fingerprints moved, the gate holds at thirteen steps
and 1 250 739 checks, and what changed is again governing text — `ANALYST-INSTRUCTIONS.md`
to `2026-09-01-d` and `EXECUTOR-INSTRUCTIONS.md` to **v17**, both forced by the first
production analysis run to reach the Boss (§10, §11) — plus invariant 57, which that run
produced. **`2026-09-02-a` is a fourth such revision on that same baseline:** no file this
block fingerprints moved, the gate holds at thirteen steps and 1 250 739 checks, and what
changed is again governing text — `ANALYST-INSTRUCTIONS.md` to `2026-09-02-b` and
`EXECUTOR-INSTRUCTIONS.md` to **v18**, both forced by the audit of the 02.09 analysis run
(§10, §11) — plus invariant 58, which is the single mechanism behind all four failures
that audit found.

Every TZ header quotes this block IN FULL — all seven anchors and the file table,
never a subset. The Executor matches each anchor as an exact substring against the
repository copy before any work (contract §5); any mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-02-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `58. **A rule that names an object without naming how to compute it has named nothing.**` |

Live files at this revision — the set every TZ header and every report fingerprints:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

The calibration record is fingerprinted, unlike every other bench artifact, because
it is one of exactly two places `DAY_RANGE_ABNORMAL = 1.39` exists and gate step 12
compares the two on every push (inv. 46).

Gate at this revision: `bench.yml`, **13 steps, 1 250 739 checks**, green on the
hosted runner (`Bench gate` #110 on head `8069341`, #111 on merge commit `edd650c`).
TZ-21 moved exactly one step: 8 (`catalyst_bench.js`) 23 040 -> 23 062, **+22** —
`+2` per-symbol for `ENA`, `+10` per-entry schema, `+10` for five `basis` assertions
across two entries, `+1` quorum, `−1` as the silent-symbol sweep falls 27 -> 26. The
`basis` term is measured rather than inferred: the modified bench run against the
unmodified registry reads 23 045, isolating +5 per entry. Steps 7 and 12 did not move.
Step 13
(`analyst/live-gate.sh --selftest`) arrived with TZ-17 at **35** and reads **40** after
TZ-18 added two freshness cases; steps 1–12 have not moved through TZ-17, TZ-18 or
TZ-19, which for changes writing no production file is the required result rather than a
pleasant one. Step 13's counter is assertions and not cases — three per failing case (exit code ·
empty stdout · exactly one stderr line) and two per passing case — so 12 × 3 + 2 × 2 = 40
and the +5 is attributable without inspecting the script. The
number is a sum of per-comparison counters (inv. 43), never an estimate, and every
delta between revisions is attributed term by term. TZ-15 moved exactly one step:
12 (`exhaustion_bench.js`) 220 534 → 220 598, **+64**, one new section `caption`
(M1–M5); all fourteen pre-existing counters of that bench and all of steps 1–11 are
unmoved, which for a change touching one display string, one comment and one bench
is the required result rather than a pleasant one.

**Step 7 (`journal_bench.js`) moves with verdict CONTENT, not only with control
volume.** It counts numeric leaves of the records it writes, and a verdict that
returns before geometry writes no `geo` object, so a change in verdicts moves it
without moving a single control. A fall in step 7 is attributed, never assumed
benign, because a defect that nulls a field lowers it identically. Held at
**691 109** through TZ-13, TZ-14 and TZ-15.

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
| Calibration | `bench/exhaustion_calib.py` | `calib.yml`, `workflow_dispatch` + push on `claude/**` — never on `main` | `data.binance.vision` archive | `bench/exhaustion-calibration.txt` on a PASSING run; artifact always |
| Analytical engine | `ANALYST-INSTRUCTIONS.md` + `analyst/**` | Boss-triggered, in a Claude Code session | `analyst/live.json`, `analyst/state.json`, `index.html` (`tokens[]`) | `analyst/state.json`, `analyst/log/**` |

**Schedule is not cron.** The only regular trigger is the Boss's iPhone
Shortcut: hourly from 09:00 to 01:50 local = **17 runs/day ≈ 15.3k CoinGecko
calls/month**, plus rare `push` runs on `main.py` / `main.yml`. Cron in `main.yml`
was removed deliberately (June 2026): a second scheduler is a second source of
truth for freshness. Automation outside the repository belongs to the Boss and is
never duplicated or switched off from inside it.

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

**Universe: 28 pairs, frozen.** New coins are not added (standing decision, inv. 2).

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

**Integrity cross-check.** From the single-factor identity `σ_BTC = σ_alt·√R²/|β|`,
BTC's hourly volatility recovered from five independent cards reads 0.316–0.393 %/h
(mean 0.367 %, spread ±11 %): betas and R² are computed correctly.

---

## 3. Frontend mathematics — `index.html`

- `ratio = (target − btc)/btc`; `1 + ratio = target/btc > 0` always.
- `rawBeta` = up_beta | down_beta by the sign of `ratio`; null / non-number → card shows **NO BETA**.
- `beta = rawBeta × stress` (normal 1.0 / panic 1.3 / crash 1.8).
- Forecast: `growth = (1+ratio)^beta`; `pPct = (growth−1)·100`; `pred = cur·growth`.
- Liquidation from `pred`, isolated, `LIQ_MMR = 0.0125`: LONG `pred·(1 − 1/L + MMR)`, SHORT `pred·(1 + 1/L − MMR)`. Fees and funding excluded. **Base on the card is `pred`; on the board it is the entry price `E`.**
- `LIQ_MMR = 0.0125` was recovered by back-calculation from three of the Boss's real positions (XMR 1.28 %, YFI 1.25 %, LIT 1.13 %); the earlier 0.01 placed liquidation further away than reality — an error in the dangerous direction.
- Confidence (0–100): `0.45·R²₁₄ + 0.25·R²₉₀ + 0.20·(1−min(div90,1)) + 0.10·(1−min(vol%/3,1))`; missing components drop out with renormalisation. Colours: ≥ 70 green, 40–69 yellow, < 40 red.
- **R² in both rows (14d and 90d) shares one scale:** < 0.30 red, 0.30–0.60 yellow, ≥ 0.60 green.
- ρ (`corr_90`): ≥ 0.75 green, 0.5–0.75 yellow, < 0.5 red. There is no separate 14d/90d beta-divergence glyph — divergence is already inside Conf.
- **МДЛ gate** (`gateState`, pure display): red when `Conf < 40` OR `R²₁₄ < 0.25` OR (`corr_90` present AND `|ρ| < 0.5`); green when `Conf ≥ 70` and the rest hold; yellow otherwise. High Conf measures correlation-model quality, never direction.

**Boss-approved display conventions — unchanged without his explicit request:**
funding colour = payment direction for the pressed side, «зелёный = мне платят,
красный = я плачу» (§3.1) · 14d beta on the card next to R² · МДЛ is the single
model-trust signal, no duplicate icons · Min/Max blinking and the running edge
borders are never removed (inv. 19); improvements may be proposed, never silently
applied.

**Production constants, one place each (inv. 20).**

```
LIQ_MMR 0.0125 · H_NOISE 168 · H_BTC 168 · H_REACT 12
L_CAP 7 · L_MIN 2 · INV_FLOOR_SD 2.0 · INV_CAP_SD 6.0 · MAX_MARGIN_LOSS 0.35
EFF_TREND 0.6 · PACE_Z 0.25 · VOL_ABNORMAL 2.0 · VOL_HARD 0.02 · VOL_STOP 0.03
RES_Z 1.0 · RES_R2_CAP 0.90 · FEE_TAKER 0.0005 · FUND_PAY_7D 21 · ARM_R 1.0
RR_MIN 2.0 · TGT_SIGMA_MIN 1.0 · ENTRY_CHASE_SD 0.5 · REG_STRESS_Z 2.0
DAY_RANGE_ABNORMAL 1.39 · CAT_WINDOW_D 14 · TIER_STRONG 70 · TIER_MID 50
TIER_MIN 35 · STALE_WARN_MIN 75 · STALE_CRIT_MIN 130
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

**Both distance clips are mandatory.** Without the 6σ cap an entry mid-range
produced «no leverage», reading a distant reference as huge risk instead of as
absent guidance; under `capped` the card says plainly that there is no nearby
reference and the stop must be held manually. Without the 2σ floor a move smaller
than two daily sigmas — noise, not a broken idea — would be promised as an exit.

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
at Vol 1 %/h and 3X it is ~0 % over 7d, 3 % over 14d, 15 % over 30d. The touch
formula lives once, in `touchProb(vol, b, hours)`; break-even (§3.11) and
§3.17 use the same function — two copies of the reflection principle would
inevitably diverge.

**R² deliberately does not enter.** The position is not hedged against BTC, so
liquidation is caused by the coin's full move, not by the idiosyncratic part.

Side asymmetry is built in: price is unbounded upward, so at equal leverage a
short is always riskier than a long (Vol 1.0 %/h, 3X: long 14.6 %, short 29.6 %).

### 3.4 Margin risk — the fourth ceiling, HARD

`MAX_MARGIN_LOSS = 0.35`: exiting at the structural stop must not cost more than
35 % of margin. Professional replacement for «keep the stop within 10 %» — the
distance is set by the coin's structure, so what gets limited is the LEVERAGE,
not the stop. The division `MAX_MARGIN_LOSS / dist` lives in exactly one function,
`lMoney(dist)` (inv. 20).

```
hard mode      ⇔  inv.capped === false
contribution   =  max( lMoney(dist), L_MIN )
decision fields   parts.money · moneyHard · moneyBelowMin
```

**The condition is exactly `capped`, nothing else.** A clause `src ≠ 'вход'` was
rejected as arbitrary: at two different entries `dist` hits the same 2σ floor, so
the stop is mathematically identical and the rule must behave identically — with
the clause, an entry BELOW a broken low would have *lifted* the limit.

**The 2σ floor participates in hard mode, the 6σ cap does not.** A stop cannot be
placed quieter than noise, so 2σ is an honest minimum distance and money rules
apply to it. A level clipped by the 6σ cap is drawn, not tradable; the row stays
informational.

**The `L_MIN` floor is mandatory (inv. 26).** `loss/margin = dist·L` is
independent of position size, so the money rule speaks about the SHARE OF THE
ACCOUNT, not about survival. Without the floor, 538 of 1230 control setups
received «no safe leverage»; with it, none. When the stop does not fit even at
`L_MIN`, `moneyBelowMin` rises and the board says to take a smaller share of the
account instead. Measured price of the rule: 22 % of control setups get lower
leverage; across 3243 comparable setups on both sides not one case of leverage
rising.

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
expected width of the distribution, not a model defect. A separate «signal/noise»
metric is therefore meaningless — it is identical to R², already on the card (§8).
The practical answer to this risk is the liquidation probability (§3.3), not a
band on the forecast.

### 3.7 Board CRYPTO FUTURE — the work surface

Full-screen overlay (`#board`, z-index 5000), opened from a card. The card is the
shop window, the board is the desk; there is no duplication by construction. One
coin at a time, session state only.

**Block order lives ONLY in the concatenation at the end of `boardHtml`** — the
blocks are computed above in their original order because of variable
dependencies. Reordering means moving 14 strings, never the code (inv. 15).

```
1 ИТОГ·СТОРОНА·ПОТОЛОК   2 ПОЧЕМУ ЭТА МОНЕТА   3 ДИАПАЗОН 90 ДНЕЙ   4 ТОЧКА ВХОДА
5 ВЫБОР ПЛЕЧА   6 РИСК ВЫНОСА   7 РАЗМЕР ПОЗИЦИИ   8 ГРАНИЦЫ СДЕЛКИ
9 ЦЕНА ВРЕМЕНИ   10 ЕСЛИ ИДЕЯ НЕ СРАБОТАЕТ   11 ЕСЛИ СРАБОТАЕТ   12 ЗАЩИТА ПОЗИЦИИ
13 ОТКУДА ПЛЕЧО   14 ДОВЕРИЕ К МОДЕЛИ
```

«РИСК ВЫНОСА» sits sixth deliberately (§3.17): it is the direct consequence of the
pressed leverage button (inv. 14) and must be read BEFORE size is chosen; it
declares no variable of the size block. «ЗАЩИТА ПОЗИЦИИ» sits twelfth: 10 and 11
are outcomes, 12 is the only action that converts unrealised profit into inability
to lose, and 13–14 are methodology and diagnostics. «СТОРОНА ПРОТИВ СТРУКТУРЫ» and
«ВНИМАНИЕ» come straight after the verdict: they are alarms, not sections.

**Position size — two input units.** `sizeMode ∈ {usdt, coin}`.

```
Identity: notional = qty·E = mrg·L.  ONE number is entered, the other derived.
usdt: mrg = posMargin;  notional = mrg·L;  qty = notional/E
coin: qty = posQty;     notional = qty·E;  mrg = notional/L
```

Switching the unit does not move position volume (recomputed through the identity
in `setSizeMode`, using the exact entry price from `entryState`, never a rounded
HTML attribute). In coin mode a leverage change keeps quantity and moves margin —
the correct order for «I want 1000 UNI» (inv. 16).

**Pressed-button highlight is one law of the board (inv. 17).** Exactly one button
lights in each group: side, leverage, size unit, entry point. For the entry point
the lit button is the preset price matching the current one within 0.25 % — half
the 0.5 % step of the −/+ buttons; if none matches, the pencil lights and that is
«своя цена».

**Funding in money:** `costUsd = |fr|·21·notional` (21 = 3 payments/day × 7 days),
identical to `cost% = |fr|·21·L·100` of margin. Both are shown; the block's colour
is the economic effect for the pressed side.

**Scroll anchor is mandatory (inv. 18).** The board re-renders wholly through
`innerHTML` on every action and every 30 s with the ticker. Restoring absolute
`scrollTop` caused a jump, because block heights ABOVE the reading point change
between renders. What is remembered is the section under the top of the screen and
the offset inside it; the key is the text of its `.bd-h`. Section gone → previous
behaviour; `scrollTop < 4` → no anchor.

**Metal on the frames.** The ring is a SECOND background layer: the block fill is
clipped to `padding-box`, the metal to `border-box`, and the border-wide gap shows
`linear-gradient(148deg, …)`. Radii stay exact (`border-image` breaks them) and no
new nodes, pseudo-elements or masks appear — decisive on a surface that re-renders
every 30 s. Highlights are near-white deliberately: at 1px and DPR 3 a soft
gradient collapses into one grey line.

**Switch is `:not([style])`.** Inline `style` on `.bd-sec` exists on exactly two
blocks — the alarms «СТОРОНА ПРОТИВ СТРУКТУРЫ» (red) and «ВНИМАНИЕ» (amber) —
where the border colour carries meaning. **Trap:** any new inline style on a
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
deliberately unused** — «not ripe yet» is waiting, not danger. The block's own
caption states that these are conditions of PACE, not of PRICE: price belongs to
«ДИАПАЗОН 90 ДНЕЙ» and to the «СТОРОНА ПРОТИВ СТРУКТУРЫ» alarm and is not duplicated
here.

### 3.9 Residual to BTC — `res7`

The coin's weekly move decomposes EXACTLY, with no remainder:

```
r7 = mkt + own      mkt = β₉₀·btc.r7 (market part)     own = res7 (its own)
```

**Beta by the sign of the REALISED `btc.r7`**, not by the slider: `up_beta_90` when
`btc.r7 ≥ 0`, `down_beta_90` when `< 0`. The slider is a hypothetical future; `res7`
measures the past seven days, and a scenario has no right to influence a
measurement of the past. No discontinuity at zero: the multiplier `β·btc.r7 → 0`
there. This beta may therefore differ from `b=` in the `90d:` row, which is chosen
by the slider's sign — the divergence is normal and is named on the board.

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
pure display, measured at zero predictive value (§3.10a, inv. 27). Missing inputs →
the block is not drawn and the rest of the card lives (inv. 9).

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

The other thirteen blocks answer *«may I open this, and how big»*. This one answers
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
margin. **Seven days everywhere,** so the leverage engine, the funding block and
this one cannot disagree.

**No threshold on the scratch probability, deliberately.** Whether a 47 % chance
of scratching is worth removing stop risk depends on the Boss's own hit rate,
which the system has never measured. A traffic light would look like a measured
verdict without being one. The scratch number is the point of the block: moving a
stop to break-even is normally believed free, and on XRP-like inputs (Vol 0.9 %/h,
1R = 9.1 %) noise drags price back to break-even within 7 days in **47 %** of weeks.

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
stress  if  btc.volatility ≥ VOL_HARD  or  |z| ≥ REG_STRESS_Z
trend   if  |eff| ≥ EFF_TREND,  dir = sign(eff)
range   otherwise
```

`eff` is deliberately the same formula the bot uses for a coin's `eff14`, compared
against the same `EFF_TREND`: one threshold per system (inv. 20). **Known
property, measured:** under a driftless random walk `eff ~ N(0,1)`, so
`|eff| ≥ 0.6` labels ~55 % of pure-noise windows «trend». Accepted, because a
false trend label cannot produce a wrong direction — it narrows the admissible
side to one, and on a driftless market both channels are worth exactly zero.

**Stress is symmetric, and that is the whole point of the layer.** The comparison
is on `|z|`: a four-sigma week UP admits no side either — a one-sided lower branch
once printed «ТРЕНД ВВЕРХ» in green on days when geometry refused 24 of 25 covered
coins. `out.dir` stays 0 under stress: `dir` is read only on `trend`, and handing
a direction to a state that admits neither side would be a contradiction in one
object. The banner picks its wording by the SIGN of `reg.z` — «РЫНОК ПЕРЕГРЕТ»
above, «СТРЕСС РЫНКА» below, red in both. The cost is by design: on a stress day
every `action` is `none` on both sides.

No `btcStats` or no `volatility` → `mode = 'range'`, `known = false`, which is
exactly the pre-engine production behaviour (inv. 9). The regime label says WHICH
state the market is in and never HOW FAR into it the session sits; that second
quantity is measured in §3.16 and printed in §3.17, and no threshold in this
engine reads it.

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
(inv. 27). It exists because the verdict is not reconstructible after the fact:
`history.json` keeps betas, R² and rank only, while `scoreCandidate`,
`tradeGeometry` and `leverageDecision` need exactly the fields it does not keep —
every unjournaled day is lost permanently.

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
   derivable at analysis time from `score`, `rp`, `rel`, `tier`. The same standing
   applies to the day-range reading (§8).

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

**Consequence 2 — a ghost spot pair does not revoke the declaration (inv. 41).**
`data-api.binance.vision` still answers for `XMRUSDT` and `LITUSDT` with a
delisted, zero-volume row. The row exists; the market does not. Classifying by
what the host returned disagreed with the declaration and showed up as a
permanently degraded `status`.

**Consequence 3 — the bench divergence in §7 is a source property.** The backtest
reconciles with production on 25 of 28 coins; the three that diverge by 7–9 pp on
returns are exactly these three — the bench reads the perpetual, CoinGecko reads a
spot index, and the basis is the difference.

**Consequence 4 — coverage is 25/28 permanently.** Every statistical statement
built on the journal or on the day-range measure is a statement about 25 assets.
Closing that gap would require a second price source bought for three rows.

Reversed if Binance relists XMR or LIT on spot with real volume — and since TZ-15
that is four moves in one change, not two: `tokens[]`, this paragraph, the static
«25 спотовым монетам» in the §3.17 caption, and the exact-string expectation section
M pins it with. The gate stays red until all four move together, which is the safe
direction — a declaration and the sentence describing it cannot drift apart quietly
(inv. 20, 50). The count in that caption is a code site of the coverage in
everything but syntax.

### 3.15 Catalyst registry — `catalysts.json`

The only external input of the direction engine, served next to `index.html` and
read by the frontend over ES5 XHR. **The data lives in the file; the rule lives in
`catalystCheck` and did not move.**

**Schema v1.**

```
{ "v":1, "updated":"YYYY-MM-DD",
  "items": { "SYM": [ { d, dir, kind, t, conf, src[], added } ] } }

d      ISO date of the event       dir    long | short | both
kind   unlock | protocol | listing | macro     CLOSED set, gate-asserted
t      the string the card prints  conf   confirmed | disputed
src    array of source URLs        added  ISO date the entry was written
basis  why the date is believed    OPTIONAL; MANDATORY at conf 'disputed'
```

The file is ASCII-only and the printed string `t` is `\uXXXX`-escaped.

**The `kind` enum is CLOSED.** It was once written with an ellipsis and read as open, so a
TZ proposed a fifth value and the gate refused it — one rule living in two places and
disagreeing (inv. 20). A new member is additive, needs its own TZ, and arrives with the
entry that consumes it, never speculatively.

**`basis` is invisible to production.** `catalystsApply` copies `items` wholesale and
`catalystCheck` reads `d`, `dir`, `conf` and `t` only, so an unknown key is inert by
construction (inv. 1, inv. 9) — measured, not assumed: the identifier appears in no
production file. It is inside `cat.hash`, so it sits beside every journalled verdict.

**Authority — `conf`, and the quorum behind it (inv. 39).** A registry edit
bypasses the TZ → Executor → pull request → audit chain, so the compensating
control is that only `conf === 'confirmed'` may close a side, compared exactly and
case-sensitively, and **`confirmed` requires at least one PRIMARY source** — the
protocol, the exchange or the foundation, matched by host on a dot boundary
against the allow-list in `bench/catalyst_bench.js`. Two aggregators repeating each
other are **not** a quorum: authority, not repetition, is the bar. The PRIMARY list
is the registry's trust root and changes only through a TZ (contract §7 item 13).

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

**Registry content is analyst work under a TZ.** Current content: one `confirmed` ZEC
entry, `dir:'both'`, primary source, for the NU7 vote resolution on 14.09; one `disputed`
ENA entry, `dir:'short'`, for a derived unlock date on 05.09.

**Three classes of standing, and the third is why `basis` exists.**

| The primary publishes | Treatment |
|---|---|
| the date | `conf:'confirmed'` per inv. 39 |
| the mechanism but not the date | `conf:'disputed'`, **`basis` mandatory** |
| nothing about the event at all | the entry is deleted, never demoted |

The third row is the original rule, unchanged: a `disputed` entry annotates its own side,
so keeping one built on nothing keeps printing an argument nobody can check. The second
row is a case that rule did not name. Ethena publishes a 25 % cliff one year after TGE on
2024-03-05 and three years of linear monthly vesting thereafter, so monthly steps fall on
the 5th and 2026-09-05 is DERIVED from a primary-published rule rather than asserted
against silence. `basis` records the derivation in the file, which answers the objection
the third row raises — the argument is no longer unrecorded, and it can be argued with.

**An owner's assertion is not a source.** The date may be set by the Boss; `conf` may not.
`confirmed` is the compensating control over an externally editable file, and a flag that
can be set by assertion has stopped being one (inv. 39).

**Two scope rules, both closed permanently.**

1. **Coin-scoped events only.** A macro release, a central-bank decision, an index
   rebalance never enters this file. Market-wide risk is measured by §3.12 Layer 0, and a
   `dir:'both'` macro entry would close both sides on all 28 coins for fifteen days out of
   roughly forty-five. A `"*"` key is therefore not a missing feature, and the
   `items key "<sym>" is in tokens[]` assertion that refuses it is correct.
2. **Resolving events only.** An event qualifies when something the market prices becomes
   known or irreversible on `d` — an unlock releases supply, a vote concludes, a listing
   goes live, an agency decides. An administrative milestone on the path to one does not:
   a comment-period deadline, a filing date, a hearing being scheduled. Nothing resolves,
   and the veto would spend fifteen days of both sides on a non-event. TZ-20's ONDO row
   was closed by this rule with its date fully verified — the date was never in doubt, the
   event was.

Both rules also live in `bench/catalyst_bench.js`'s editing-rules comment, which is where
an editor meets them.

### 3.16 List exhaustion — the day-range measure

**Live, thresholded, printed; compared against one constant and forbidding
nothing.** It closes the gap that `regimeBanner` names the regime and says nothing
about how far into it the session already sits.

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

**The reference value is 1, not «somewhere above 1» — and the archive confirms
the scale.** `E[range] = σ·√(8/π)` makes the ratio unbiased when σ is right, so a
diffusive day reads 1 on average. The archive measures a pooled coin-day mean of
**0.9509** against a null simulated in the same run at **1.0012** — a 5.03 % gap,
inside the 15 % the rule allowed: the denominator is correctly scaled, and a
mismatch between the bot's `volatility` and a reconstructed one would have moved
the mean and did not. The earlier claim that close-based σ pushes the reading above
1 by construction is **withdrawn** — the intra-hour understatement and the √24
scaling of microstructure-inflated hourly returns cancel to within noise.

**What the archive does show is over-dispersion against the null**, on both
objects. Coin-days (TZ-11): median 0.81 vs 0.93, p90 1.59 vs 1.38, maximum 15.6 vs
3.2. List medians (TZ-13, the object the consumer thresholds): p0 0.2407 vs 0.5850,
p50 0.7769 vs 0.9325, p90 1.3911 vs 1.2393, p100 10.6653 vs 2.6604. That is
volatility clustering (§7) thinning the middle and fattening both tails — the
property the banner exists to surface, not an artefact to calibrate away.

**The null is a floor on what a quiet market reaches, never a model of this one.**
It is a constant-σ common-factor construction with no vocabulary for a market that
alternates between very quiet and very violent regimes: the empirical distribution
is wider than it on BOTH tails, and the worst journaled date sits five times the
null's p99.9. Its whole job is to say where a quiet market stops, so that an
admissibility band can be drawn without writing one down (inv. 49). Reading a
percentile of it as the probability of a real day is a category error; the figure
printed on screen is a measurement of the day, not a likelihood.

**Nothing predictive is added.** This measures what the session already did, in
the same standing as §3.12 Layer 1: it asserts «the geometry of entering right
now is bad», which is measurable without a forecast. No ranking factor, no weight,
and §3.10b's resolution ceiling is untouched.

**Quorum `n ≥ 8` is load-bearing.** A statement about the list computed from three
coins is not a statement about the list, and the banner is the one list-wide
element on screen.

**The estimator and its calibration share a universe: 25 spot assets (inv. 41).**
The three `fut:true` assets read their range off the perpetual while `volatility`
comes from a spot index (§3.14 Consequence 3), so `listExhaustion` skips rows whose
`tokens[]` entry carries `fut:true`; the venue test short-circuits AHEAD of the `cd`
test, so such a row can never reach `dayRangeRatio` whatever fields it carries, and
the quorum is applied AFTER the exclusion — a list reaching eight only by counting
`fut:true` rows has no median.

**The threshold and its consumer are the same random variable (inv. 47).**
`listExhaustion` compares the **median of the list**, so the constant is a
percentile of the distribution of per-date list medians, never of individual
coin-days: averaging 25 correlated coins removes idiosyncratic dispersion and moves
the upper tail. Measured on the same archive and the same 24 384 coin-days:
coin-day p90 **1.59**, list-median p90 **1.39** — the object was the error, the
data never moved.

**The adoption rule (inv. 23, 49).** The object is the per-date LIST MEDIAN produced
by production's own `listExhaustion`; the statistic is the 90th percentile; the
admissibility band is not written down but derived in the same run from a simulated
driftless null of that same statistic; once adopted, the constant is pinned to the
run that produced it (inv. 46). A hand-written band once refused a correct number —
TZ-11's `1.60 … 4.00` sat above the p99 of this run's null — and a band is never
widened to admit an observed number.

**The rule ran and returned `DAY_RANGE_ABNORMAL = 1.39`.** Run `Calibration
(archive)` #2, id 32667872706, seed 20260823, reproduced byte-for-byte on every
statistic by #3 on a second runner with a warm cache. The record is
`bench/exhaustion-calibration.txt`, fingerprinted in §0.

| Quantity | Value |
|---|---|
| object | per-date list median, produced by production's own `listExhaustion` through a node hop |
| sample | 1 110 dates, 2023-08-09 … 2026-08-22, none dropped below quorum |
| universe | 24 of the 25 declared spot assets; `GRAM` has no three-year archive |
| per-date contributing count | median 22, range 19 … 24 |
| ρ, MEASURED per date | mean 0.6196, range 0.4557 … 0.8265, negative on zero dates |
| null | 248 640 simulated date medians, p90 **1.2393**, MC s.e. 0.00117 |
| empirical p90 | **1.3911** → **1.39** at two decimals |

All four registered conditions passed, none marginally: the coin-day mean sits
5.03 % from the null's against an allowance of 15 %, and the empirical p90 lands
above the null's p95 (1.3626) and below its p99 (1.6271) — high enough that a quiet
market does not reach it a tenth of the time, low enough not to be a broken
pipeline. The known-answer control read **0.99980** over 10⁶ coin-days against a
registered 1.000 ± 0.005, and the same walk built from hourly CLOSES read 0.8613 —
the control detects the exact error it exists to catch. Step counts of 24/48/96/240
per day move the control by less than 0.0002, so the Brownian-bridge day is exact
in distribution rather than a discretisation.

**The row is the contract, with exactly one parse site per quantity (inv. 48).**
`update()` assigns `row.cur`, `row.hi24` and `row.lo24` from the ticker once,
immediately after the `nopair` early return and before the dead-market test, for
EVERY row that has a ticker — `fut:true` included, because the venue rule lives in
`listExhaustion` and a row filtered at the producer would put that declaration in
two places (inv. 41). Every consumer then reads the row: the `sideOn` branch, the
board header, §3.17 row 2, the off-list relevance filter, the dead-market card and
the card header. Only two `parseFloat(…lastPrice)` sites survive anywhere in
`index.html` and both read `btcObj` — BTC is the regime measurer, is not a member of
`rows[]` and never reaches the measure. The gate's wiring section derives both
sides of the contract from the source — `update()` writes `cd, coin, cur, dec,
hi24, idx, lo24, sc, state, t, vd`; `listExhaustion` reads `cd, cd.volatility,
cur, hi24, lo24, t, t.fut` — and, run against a file whose rows lack the three
fields, names them as missing and exits non-zero.

**State at this revision.** The measure runs live, reads 25 on a full board, and has
one threshold and two readers. `DAY_RANGE_ABNORMAL = 1.39` is declared once in
`index.html`, compared once — inside `listExhaustion`, with `>=` — and worded once,
by `dayStateNote`; those three are the identifier's only code sites and the gate
enumerates them (inv. 20). `reg.day = listExhaustion(rows)` is written in
`update()` unconditionally and above the `sideOn` branch, because whether the day
is abnormal is a fact about the session and not about the pressed side. The board
keeps its own `listExhaustion(lastRows)` call: one pure function over one array
cannot disagree with itself, while routing the board through `lastCtx` would force
every board fixture to invent the field — the shape inv. 48 exists to catch.

**`abnormal` is a printed word and nothing else (inv. 27).** No output enters
`scoreCandidate`, `tradeGeometry`, `leverageDecision`, `directionVerdict`,
`liqPrice`, the tier badge, `byScore`, `assignRanks`, `planLine` or the journal
writer — proven by perturbation rather than inspection: scaling `hi24`/`lo24` until
`abnormal` flips moves no compared field on either side and leaves the record
`journal/write.js` would write byte-identical. The one field that moves under that
perturbation, `geo.wait` on SHORT, moves identically on the pre-TZ-14 revision — the
entry-chase anchor's long-standing dependency on the 24-hour range. That two-sided
form of the test is the general one: a perturbation that moves a field on both
revisions has proven nothing about the change. TZ-15 ran the identical protocol on a
harness written fresh and read 0 of **1 240** fields with the record byte-identical
again; the two field counts are properties of each harness's enumeration, and the
result replicating across two independent harnesses is worth more than either run.

`[решение принято мной]` Discarded: making exhaustion a Layer 1 veto. At the
adopted line it would close roughly a tenth of all sessions on both sides on the
strength of zero measured evidence that entering on such a day ends worse, and
inv. 32 forbids acting on that. Reopened only by a journal-based measurement of
outcomes conditioned on the day state, which needs no new recorded field (§8:
recording the reading is closed). **The decision now carries a text dependency, and
it is mechanical rather than remembered:** since TZ-15 the caption tells the Boss
that this is «мера дня, а не запрет», so a TZ reopening the veto repairs that
sentence in the same change (inv. 50) — and cannot forget, because gate section M
pins the caption as one exact string and turns red on any rewrite.

Two decile tables are on file: the coin-day one in
`CryptoReports/TZ-11-exhaustion-threshold-report.md`, the list-median one in the
record itself. Replayed on journaled days through the production functions:
**1.69** on 2026-08-21 (6 of 25 coins above 2.0) and **2.43** on 2026-08-22 (20 of
25) — against 1.39 both are abnormal days, which is what two of the most violent
sessions of the quarter should read. Days are not a distribution and bound nothing.

### 3.17 «РИСК ВЫНОСА» — the day's own risk

Sixth board block (§3.7). It answers a question none of the other thirteen asks:
**not «is this trade sound» but «does the position survive TODAY»** — the horizon
is 24 hours, everywhere else it is seven days. Three rows, all read from existing
production functions; nothing is recomputed and no formula is duplicated
(inv. 20, 21).

```
1  запас до ликвидации   liq = liqPrice(E, currentLev, isLong)   PRESSED lever, inv. 14
                         b   = |ln(liq/E)|
                         dist = b / sigmaDay(vol)      touch = touchProb(vol, b, 24)
2  день уже вынесен      own  = dayRangeRatio(hi24, lo24, cur, vol)      §3.16
                         list = listExhaustion(rows) -> median, n
3  стоп против шума      read from dec.inv: capped | floored | dist/sd
```

**The 24-hour horizon is the block's reason to exist and is not a duplicate of the
7/14/30d ladder in «ЦЕНА ВРЕМЕНИ».** The ladder answers «will this position live
out the week»; a four-sigma session asks whether it lives out the afternoon. Both
come from the single `touchProb` (inv. 20), so the two horizons can never
disagree, and the ladder is not repeated here.

**Row 2 compares, and forbids nothing.** Whenever the list median reaches
`DAY_RANGE_ABNORMAL` the row gains a third line: the one sentence `dayStateNote`
builds, in amber, byte-identical to the sentence the regime banner prints above the
card list (inv. 33). Amber is the «ВНИМАНИЕ» alarm's standing — attention without
prohibition — and it is deliberately not applied to the regime line itself, which
would make one line carry two independent facts and would overwrite the stress red
exactly when it matters most. On a quiet day and on a below-quorum list both
surfaces are silent, so the sentence's presence is itself the measurement, and its
absence is not an omission. The two raw numbers above it stay interpretable without
a threshold because the unit is derived, not chosen: `E[range] = σ·√(8/π)`, so 1,0
is an ordinary day. This is the standing of §3.12 Layer 1 — an assertion about
geometry that needs no forecast — and it adds no ranking factor, so §3.10b's
resolution ceiling is untouched.

**The caption states what the day line means and denies nothing the block has
(inv. 50).** It names the threshold as the 90th percentile of the list median over
the three-year archive, a measure of the day and not a veto, and keeps the half that
is true and proven (§3.16): the number reaches no score, no leverage and no verdict.
It never prints the number — `DAY_RANGE_ABNORMAL` keeps exactly three code sites
(inv. 20), and the value is already printed one line above on the days it matters.
Gate section M scans this one block for six denial phrasings on both the quiet and
the loud render, pins the caption as one exact string, reads the constant through
the live context, and carries its own control: a copy with the old caption fires the
scan by name, the clean source is silent. Any future TZ that legitimately changes
this caption updates section M in the same change.

**Degradation is stated, never hidden** (inv. 9): no `volatility` → the sigma
distance and the 24h probability go, the block lives; `E ≤ 0` or non-finite `liq`
→ row 1 is dropped; `median === null` → the list line says how many coins had a
measure and that eight are needed; no `dec.inv` → row 3 is dropped.

Pure display in the standing of inv. 27, and the probability is a LOWER bound
(§7) — the caption says so, because a 24-hour number is the one most likely to be
read as a promise.

---

## 4. Invariants — DO NOT BREAK

Numbers are stable identifiers: production comments, benches, TZs and the contract
cite them, so an invariant is rewritten in place and never renumbered.

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
44. **A fetch may stand behind a product fact only if anyone can reproduce it; a session fetch cannot.** The earlier form of this invariant said external data is fetched on a runner and never in an implementation session, and gave reachability as the reason: an Executor session refused every market host at CONNECT. **That measurement no longer reproduces** — TZ-20 reached four hosts from the VPS and read 200 on all four — and a rule resting on a measurement falls with it (inv. 52). What survives is a rule about STANDING, not about reach. A runner fetch is recorded, repeatable by anyone holding the repository, and its inputs are named in a workflow file; a session fetch is none of those, because the session ends, the market moves, and the only trace is a sentence in a report. Therefore: **forbidden in a session** — fetching an external FACT that enters the product (a price, a date, a figure, an event) as the standing behind it; such a stage is specified as a workflow step and nothing else, and a TZ asking for it in-session is blocked before it starts. **Permitted in a session** — measuring the session's OWN ENVIRONMENT (egress, tool availability, host reachability), because the artifact IS the measurement, the command is recorded beside its result, and re-running the command is the reproduction; this class produces no product fact. TZ-10 Stage B remains the cautionary case for the first class: the instrument was correct, complete, self-tested — and returned no number. TZ-20 is the case for the second: reachability was asserted from an old measurement and was wrong.
45. **A differ returns zero on identical input.** Any comparison offered as no-regression evidence is first run with the SAME revision on both sides and must report zero differences, and a transformation applied to one side is applied to the other. `prot_bench.js`'s optional baseline suite strips one section from the candidate only, so it reports six failures against a byte-identical baseline — a stale expectation a self-comparison would have caught the day it was written. Identity is the known-answer control of a comparator (inv. 23); a comparator never proven on identity supports no claim about a real diff.
46. **A calibrated constant is checked against its calibration record.** A production number derived from a measurement lives in two places — the constant in the source and the committed output of the run that produced it — and a bench inside the gate compares them on every push. Inv. 23 fixes the rule before the data; this fixes the number to its run afterwards. A constant that agrees with nothing can be moved silently in either direction, and the move is invisible precisely because the number looks measured.
47. **A threshold is calibrated on the distribution of the quantity its consumer compares.** A constant thresholding a LIST MEDIAN is measured on the distribution of list medians, never on the distribution of the individual readings the median is taken over: averaging across correlated members strips idiosyncratic dispersion and moves the upper tail (driftless null at ρ = 0.75: coin-day p90 1.38, list-median p90 1.27). Inv. 46 pins a constant to its run; this pins it to the right random variable. A percentile measured on the wrong object looks fully calibrated and is wrong by exactly the amount nobody can see, and an admissibility window drawn around that object inherits the error.
48. **A bench that builds its own input proves the function, not the wiring.**
    Where a production function reads an object assembled somewhere else in
    production, at least one check must prove the assembling site supplies every
    field the reader takes: the fields read off the object are derived FROM THE
    SOURCE and compared against the fields the producer writes. `listExhaustion`
    was green in two gate steps on fixtures carrying `hi24`, `lo24` and `cur`
    while the live row object carried none of them, so the measure returned
    `n = 0` on every render and the board printed a caption claiming a coverage it
    never had. Inv. 42 makes a bench take production's EXTERNAL input; this makes
    it take production's INTERNAL shape. A green bench on invented input is
    evidence about arithmetic and never about reach.
49. **An admissibility band is derived from a null computed in the same run.**
    A band that decides whether a MEASUREMENT is plausible — «is this reading
    consistent with a quiet market, or is the pipeline broken» — is computed from a
    simulated null of the SAME statistic inside the run that produces the number,
    never written into the rule as a numeral. A hand-written band is a prior about
    the answer disguised as a control: TZ-11's `1.60 … 4.00` sat above the p95 of
    both relevant nulls and was ~15 % too high before any data existed, so a
    correct rule refused a correct number. Inv. 23 fixes the rule before the data;
    this says a rule carrying a numeral about the outcome is not yet a rule. A band
    stating what is WORTH acting on is a different object and may be written down
    (§3.10c's `IC ≥ 0.030` is one): the first is a fact about the measurement, the
    second is a decision about its value.
50. **A stated absence is a dependency of the thing it denies.** A caption, an
    on-screen sentence or a checklist clause asserting that some mechanism does
    NOT exist — «порога нет, сравнения нет», «no threshold word appears anywhere
    in the block» — is load-bearing text that turns false the moment the mechanism
    is built, and no bench comparing BEHAVIOUR catches it: such a bench measures
    the specification, while this is a claim ABOUT the specification. Therefore a TZ
    that builds a mechanism enumerates every place that currently denies it and
    either repairs them in the same TZ or records the contradiction together with
    the TZ that closes it. A denial that outlives its subject is the board
    contradicting itself in the reader's own language, two lines apart, and the
    reader has no way to tell which half is stale. TZ-14 adopted
    `DAY_RANGE_ABNORMAL`, printed «порог 1,39» in §3.17 and left the caption
    beneath it denying any threshold; the Executor was right to obey its file list
    and the specification was wrong to omit the sentence. **TZ-15 repaired it and
    supplied the general remedy:** a denial escapes the gate only while it is prose,
    so the sentence is asserted as one exact string beside a control that plants the
    old wording back and must fail. A stated absence nobody can plant and catch is
    not yet checked.

51. **A freshness check is two-sided, or it is not a freshness check.**
    `now − ts ≤ limit` is satisfied by every payload timestamped in the future, so a
    producer whose clock runs ahead delivers a stale snapshot that presents as fresh —
    the exact failure the check exists to prevent, arriving through the check itself
    and reported as a pass. An age window therefore has a floor as well as a ceiling,
    and the floor is the producer's plausible clock skew rather than zero: the phone
    that writes the payload and the machine that reads it are different clocks, and
    a hard zero would refuse healthy data every time they disagree by a second. The
    one-sided form is invisible in testing because every fixture a author writes is
    in the past.
52. **A filter is measured on the runner, never derived from the pattern.**
    Glob semantics differ between matchers on exactly the cases that matter, so a
    reading of a pattern is a hypothesis about a third party's code and never a fact
    about it. This entry exists because the Architect derived one and was wrong:
    `'**/*.md'` was declared unable to match a root-level file, an invariant was
    written on that reading, and a corrective TZ was issued — while the repository's
    own run history already showed three pushes of root-level Markdown, none of which
    started the bot. The pattern had always matched. **The evidence was older than the
    error and nobody had looked.** Therefore: any claim about a `paths` or
    `paths-ignore` entry is settled first against runner history for paths that have
    actually been pushed, and only where history is silent by evaluation against a
    changed-file list taken from `git diff --name-only` rather than typed — in **both**
    directions, with the pattern and without it, and against a control path that must
    still fire, since a filter matching everything also passes every «must not run»
    row. This is inv. 45 applied to a matcher, and inv. 23's known-answer discipline
    applied to a belief about someone else's implementation. Where two readings of a
    pattern disagree, the pattern is replaced by one that reads the same under both —
    `'**.md'` over `'**/*.md'` — because closing an ambiguity is a real gain even when
    the behaviour does not move. A `paths-ignore` list with no `paths` allow-list
    beside it still fires on every path nobody thought to name; that was `main.yml`'s
    shape until TZ-23 replaced it with an allow-list of two literal paths, and the
    literals are deliberate — a glob is a hypothesis about a third party's matcher,
    two exact strings compare equal or they do not.
53. **A control is not wired until the trigger that reaches it has been measured.**
    Inv. 37 says a bench outside the gate is not a control; this says a bench inside the
    gate is not one either while the trigger excludes the commits that would exercise it.
    `analyst/live-gate.sh` was step 13 of a green gate and sat under an ignore written for
    the analyst's DATA, so a commit changing only the gate script started nothing — the
    control existed, was wired, was green, and could not be reached by the one change it
    exists to judge. The failure is invisible by construction, because the thing that would
    have complained is the workflow that does not run. **An exclusion is written for a class
    of file, but it is applied to a path**, so whenever one is added or widened the question
    is not «is this data» but «does this path also hold a control». Proof is a real push
    carrying only that file (inv. 52), never a reading of the pattern. The converse is the
    price and is the right direction to fail in: a narrowed list must be extended whenever
    the writing set grows, and a forgotten entry costs runner minutes loudly instead of
    costing a control silently.
54. **An immutable record cannot contain the outcome of the action that stores it.**
    This binds every record the repository never reopens — the analyst's day log, a TZ
    implementation report under `CryptoReports/**`, any future artifact in that standing.
    Such a record is written, then committed, then pushed, so every sentence it
    carries about its own commit or push is a forecast of a step that has not run — and
    the first one written was wrong in the dangerous direction, declaring a push that had
    in fact succeeded to have failed. A reader of an immutable record cannot tell a
    forecast from a measurement inside it, and the record's whole value is that the
    distinction never has to be made. The remedy is not more care in wording: it is that
    the outcome belongs to the NEXT record, where it is history. This is inv. 38's
    immutability read forwards — a file that may not be corrected must not contain the
    class of statement most likely to need correcting.
    **It is enforced by the report template, not by care.** TZ-21 named this prohibition
    in its own §8 and the report violated it anyway, in the section that always carries
    that sentence — the second occurrence in two consecutive TZs. A clause an author must
    remember is not a control; a template with no such line is.

55. **A specification is checked against the text it must obey, never against memory of it.**
    Six defects across two consecutive TZs came from one mechanism: the Architect
    wrote a requirement from a correct recollection of a rule and a wrong recollection of
    its detail — an enum's members, an allow-list's host, a hard-floor clause, a count of
    entries. Each was caught downstream, which is the design working, and each cost a
    full Executor session. Therefore every TZ, before it ships, reads FROM THE REPOSITORY
    every constant, enum and allow-list it names and every hard-floor clause its stages
    touch, and quotes them into the TZ where the Executor can compare. Inv. 21 bans a
    second implementation of a rule; this bans a second recollection of one. The failure
    is invisible at authoring time by construction — a specification never runs, so
    nothing contradicts it until a session has been spent on it.
56. **A recorded state is not a current state unless it carries the date it was measured.**
    §10 is this system's own register of what is true, and a row in it is read as a fact
    about today. A row whose State rests on a MEASUREMENT — a host's answer, a machine's
    ceiling, a producer's output, a third party's behaviour — therefore carries the date
    and, where it exists, the time of that reading, inside the State cell. **A State with
    no date is a DECISION and may be read as standing; a State with a date is a READING
    and expires.** Before a dated row is repeated as current state it is re-measured, and
    the cost of re-measuring is exactly one command in every case that has arisen.
    Inv. 52 says a rule resting on a measurement falls with it; that was written about
    somebody else's matcher, and this says the same thing about this map's own rows. The
    failure it names has happened: the row recording a malformed `analyst/live.json` was
    written when it was true, was never re-measured, and was reported to the Boss as an
    active blocker while a valid payload sat one command away. **Nothing in a flat table
    distinguishes a fact from a fossil**, and the reader who is most likely to be misled
    is the author, because a row he wrote reads like a thing he knows.
57. **A verdict computed from a frozen measurement is dated, not timed, and no clock revokes it.**
    Where a process cannot take a SECOND measurement, re-deciding a question after time
    has passed uses the same evidence and can only lose: the second answer is not a
    check, it is the first answer with the confidence removed. A measurement expires; a
    verdict about a named minute does not — it is true of that minute or false of it,
    and the clock says nothing either way. **The remedy for an ageing verdict is
    disclosure, never deletion:** the moment is printed, the anchoring number is printed
    beside the claim, and the reader who can see the current number resolves it in a
    second. Where no reader can, the claim is not published at all — but that is a fact
    about who is reading, never about the clock. The analytical engine produced this
    twice in two days. `ANALYST-INSTRUCTIONS.md` revision `2026-09-01-a` moved a
    fifteen-minute ceiling off the LEVELS after it deleted seven computed setups, and
    left the same ceiling on the STATUS; on 01.09 that demoted the one live trade the run
    had correctly found, printed «сделок нет» above a table it had computed correctly,
    and asked the Boss for a fresh snapshot it did not need. **A ceiling moved to a
    smaller object is not a repair — it is the same rule costing less per occurrence**,
    and this one occurred on every thorough run, so it cost more. Inv. 56 says a recorded
    state expires; this says a recorded VERDICT does not, and confusing the two throws
    away work that was right.
58. **A rule that names an object without naming how to compute it has named nothing.**
    Such a clause is not ambiguous and does not read as ambiguous: it is correct, it is
    read correctly, and it is obeyed in good faith by a reader who must supply the missing
    computation and cannot know he supplied one. The four defects the 02.09 analysis run
    produced are one defect four times. «A settled DATE cannot expire for want of a
    re-read» named no test, so the run tested settledness by judgement and protected two
    unlock dates no primary had ever published. «The MD5 of the §6 + §6a text» named no
    span, so the run hashed the whole file, marked all eight discovery lanes stale on one
    unrelated revision and left four unopened — the exact outcome the clause beneath it
    forbids, arriving through the clause itself. «Reported in the same answer» named no
    artifact to compare against, so four closures were archived in silence. And «an
    analysis run never starts from a branch» named a checkout where it meant a tree, so a
    run that had brought its tree to `origin/main` correctly had to argue past the rule in
    its own log. **The remedy is dull by construction and that is the point:** name the
    field, name the command, name the artifact the check reads — `dclass`, `sed -n
    '/^## 6\./,/^## 7\./p'`, the diff of `items`, `git push origin HEAD:main`. Inv. 55
    bans a second recollection of a rule and inv. 52 bans a derivation of somebody else's
    behaviour; this bans a rule that requires either. **The failure is invisible to the
    author and to the reader alike** — the author knows the object he meant, and the
    reader has an object that fits, so nothing anywhere reports a disagreement until the
    two objects produce different answers on a live run.

---

## 5. Limits

- **CoinGecko: the bot runs WITHOUT a key.** `main.yml` passes only `GIST_TOKEN`, so `api_key = None` → public access, no monthly quota, IP-rate-limited on the runner, handled by `REQUEST_GAP_SEC = 1.0` and three retries.
- **The free Demo key must NOT be attached at the current schedule.** Demo gives 100 calls/min but caps at 10 000/month; consumption is 17 runs/day × 30 calls ≈ 15 300/month plus `push`-triggered runs. A Demo key would create a cut-off around the 19th–20th that does not exist today. Attach only together with a cut to ≤ 10 runs/day.
- Binance spot ticker with `symbols`: weight 40, ~12 KB (full ticker: weight 80, ~1.2 MB).
- Binance `fapi/ticker/24hr?symbol=`: weight 1 × number of `fut:true` tokens, every 30 s.
- Gist API: files > 1 MB are truncated (handled through `raw_url`).
- Detection ceiling of the bench: |IC| ≈ 0.06–0.07 single test, ≈ 0.09 for a search (§3.10b).
- The day-range measure sees one day at a time and has no memory: it says how far
  the session has already gone, never where it goes next (§3.16, §3.17).
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
14. Position protection (§3.11): the block is twelfth; break-even is further from entry when funding is «я плачу» and nearer when «мне платят»; with price at entry the status line says so; on a coin without `volatility` only the probabilities disappear.
15. «РИСК ВЫНОСА» (§3.17): the block is sixth, between «ВЫБОР ПЛЕЧА» and «РАЗМЕР
    ПОЗИЦИИ»; row 1 moves when the leverage BUTTON moves and not when the RESULT
    does (inv. 14); the list line names a coin count that matches the spot rows on
    screen, never zero; the threshold is named inside this block and nowhere else
    on the board or the card, and inside it only through the `dayStateNote`
    sentence and only when the day is abnormal; the caption denies no mechanism
    the block has AND states the ones it does — the derived unit, the object of the
    threshold, the inv. 27 words and the 25-coin coverage — equal to its
    specification character for character (inv. 50, gate section M); the `.bd-sec`
    carries no inline `style`, so the metal ring survives (§3.7).
16. Regime symmetry (§3.12): a BTC week at `z ≥ +REG_STRESS_Z` prints «РЫНОК
    ПЕРЕГРЕТ» in red and no card is tradable on either side; at `z ≤ −REG_STRESS_Z`
    the wording is «СТРЕСС РЫНКА», also red; `dir` is 0 in both.
17. Row contract (§3.16): on a full board the §3.17 list line reads 25 coins, not
    zero; removing `highPrice` from one ticker drops it to 24 and changes nothing
    else; `lastPrice` / `highPrice` / `lowPrice` are parsed at exactly one site per
    field per row, and the only survivors elsewhere read `btcObj`.
18. Day state (§3.16, §3.17): on a list whose median reaches `DAY_RANGE_ABNORMAL`
    the amber sentence appears BOTH under the regime banner and inside «РИСК
    ВЫНОСА» and is byte-identical in the two places; on a quiet day and on a
    below-quorum list it appears in neither; the regime line's own bytes and colour
    are unchanged in every regime × side combination, so the `abnormal === false`
    banner is a strict prefix of the `abnormal === true` one; and the source
    literal equals `bench/exhaustion-calibration.txt` (inv. 46).

**Bench triggers.** Editing `verify_against_live` → run `bench/verify_bench.py`
(offline, ~20 s, must give 0 failures). Editing `scoreCandidate`, `window_stats`,
`window_vol` or `volume_expansion` → run `bench/backtest_bench.py --selftest`.
Any production edit → the full `bench.yml` gate, 13 steps.

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
| Literature momentum at a 7-14d horizon on a liquid cross-section | swept 02.09 against §3.10c's gate and it did not open. No published study carries a named IC on a liquid cross-section at 7–14 d: the strong horizon results (Dobrynskaya 57–70 % ann. at 1–2 wk hold) are measured on ~2 000 coins above $1 M cap — the small-cap tail §3.10b already names — and everything on a real liquidity screen reports t-stats or quintile spreads and no effect size. The practitioner spec closest to ours (30 d formation / 7 d hold, ≥ $5 M ADV) reports its own out-of-sample top quintile at −2.35 % ann. **The one study reporting IC in our units measured the same object we did and got the same answer:** ten Binance USDT perpetuals, rank-IC −0.010 … +0.024, the one nominally significant cell net-negative after costs, against our own [−0.006; +0.026]. Grobys & Shahzad 2026 additionally show crypto momentum portfolios have infinite return variance, so the t-statistics the positive half of that literature is built from are formally undefined |
| 7d/30d horizon switch | deliberate: scaling is manual (√H) and an extra control invites tuning the horizon to the desired leverage. Revisit if the holding period starts changing systematically |
| Recording the day-range reading in the journal | fully derivable at analysis time: the snapshot already carries `px.hi`, `px.lo`, `px.cur` and `cd.volatility`, so the coin-day ratio and the list median are reproduced by cutting production's own `dayRangeRatio` / `listExhaustion` (inv. 21) — the standing of `#N` (§3.13). Writing it would add bytes to the only unbounded artifact and create a second place for one number to be wrong. The analysis note that matters: the journal's `px.hi`/`px.lo` are the 13:00 UTC kline day, the board's are the rolling 24 h ticker |

---

## 9. History

Removed. The migration log lived here until revision 2026-08-22-b; the record is
git history plus `CryptoReports/**`, both permanent and immutable. Nothing in this
map depends on it.

---

## 10. Open queue and gates

Each item states its trigger. Nothing here is scheduled work; an item is picked up
only when its trigger fires. Items with trigger «nothing» are recorded so that the
monthly audit stops rediscovering them.

**The State column carries a CLOSED vocabulary, and a measured state carries its date
(inv. 56).**

| State | Means | Dated |
|---|---|---|
| `open` | live work, nobody has done it | no |
| `watched` | known, deliberately not acted on | only if it rests on a reading |
| `closed by TZ-NN` / `closed by contract vNN` | done and in `main` | no — the TZ number is the date |
| `closed, deliberately` | decided not to do, permanently | no |
| `declared dead` | built or specified, will never land, retained as evidence | no |
| `withdrawn` | the claim behind it was false | no |
| `measured DD.MM.YYYY[Thh:mmZ]` | a reading of a host, machine or producer | **yes, always** |
| `not built, gated` | waits on a named external condition | no |

**A `measured` row is re-measured before it is cited as current state**, and the reading
that replaces it replaces the date with it. A row carrying `measured` with no date, or a
reading whose date was never recorded, says so in the cell and is treated as unverified
until someone re-runs the command.

| Item | State | Trigger to act |
|---|---|---|
| Wide research universe (n = 120) | not built, gated — **gate probed 02.09.2026, did not open** | a named tier-1 hypothesis with external effect size ≥ 0.030 IC on a liquid cross-section at 7–14d (§3.10c). The probe was a full literature sweep of cross-sectional predictability in liquid perpetuals 2019–2026 and it returned nothing that clears all three conditions at once; §8 carries the reading and the one external IC that matched our own measurement. **A run never re-sweeps this on its own** — the gate opens on a hypothesis ARRIVING, never on another search for one, and re-probing a closed lane is the failure this repository exists to prevent |
| Regime hysteresis | not built | the Boss reports the regime label flapping between renders. Not built pre-emptively: a second trend constant on speculation violates inv. 20 |
| Continuation target for `tradeGeometry` | not built, gated | an archive backtest comparing the 90-day extremum against a continuation target on the same momentum-channel inputs (§3.12) |
| Journal outcome layer at scale | running | nothing — h7/h14 files appear automatically 7 and 14 days after each snapshot |
| Journal storage growth | watched | ~73 KB/day. Act if the repository becomes unwieldy; records are immutable (inv. 38), so the answer is archival, never deletion |
| Catalyst registry content | live, one confirmed entry | analyst work, delivered as a TZ; entries never promoted to `confirmed` without a primary source (inv. 39) |
| The §3.17 caption's own couplings | live, deliberate | any TZ that rewrites the caption (gate section M2 fails until the bench moves with it), reopens the exhaustion veto (§3.16) or relists a `fut:true` asset on spot (§3.14) — each must move the sentence in the same change |
| Re-running the calibration | frozen, deliberately | nothing at present. `calib.yml`'s paths filter names `calib.yml` itself, so ANY edit to that workflow re-fires the whole 3-year run on the branch and commits a fresh record on a longer archive, which can move the p90 away from the adopted constant and turn the inv. 46 bench red. Editing it is a re-calibration, never a touch-up; the stale `(TZ-11 stage B)` in its hardcoded commit message stays until a TZ genuinely needs a new run |
| `calib.yml` commits the record only on a PASS | correct by design | nothing. The commit step has no `if: always()`, so a refused run leaves no repository record and only an artifact — a record pinning no constant would look authoritative and pin nothing |
| `badge_bench.js`, `clean_bench.py` unwired | deliberate, documented in `bench.yml`'s own header | nothing. Both are two-input differs needing a `before` file the repository does not carry: manual tools, not controls (inv. 37) |
| `journal_bench.js` count is content-sensitive (§0) | watched; held at 691 109 through TZ-15 | the first step-7 delta that cannot be attributed field by field, or any TZ touching `journal/write.js` |
| `NaN% от входа` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ» | pre-existing, unreachable live | any TZ touching that block. `Math.abs(liqSel / E - 1)` at `E = 0` is `0/0`; entry price is never zero on a live board, so it buys a diff and no safety |
| Raw Cyrillic literal at `bench/prot_bench.js:177` | pre-existing, bench-only | any TZ editing that bench. It violates the ES5/escape rule the frontend keeps, in a file no browser loads |
| `prot_bench.js` optional baseline suite | repaired in TZ-11 — neither side stripped, unconditional identity run inside the default suite, comparison counter with a zero-comparison guard | nothing; inv. 45 is satisfied by the gate itself |
| Hosted gate evidence per TZ | watched — structural, not a reading | an Executor session cannot start GitHub Actions, so its 13-step table is a LOCAL measurement with the workflow's own step list. The hosted `Bench gate` fires on `pull_request` and on push to `claude/**` and `main` regardless, so the evidence exists; the audit reads it rather than taking the report's word |
| `bench.yml` Node 20 pin | watched — **measured, date unrecorded; re-measure before citing** | GitHub already forces the actions onto Node 24 with a warning. Act when a step fails or the whole gate can be re-run as the validation |
| `CryptoTZ/TZ-03-report-delivery.md` | never executed; declared dead by TZ-04 and retained as evidence, so no report exists by design | nothing — a specification without a report is never resurrected (contract §13) |
| Analyst engine transport | **closed by TZ-17**: no network path; the payload is a file in the tree, the gate exits non-zero on stale, short or corrupt input, step 13 holds it | nothing. Re-opened only by a fresh egress measurement (§11) |
| `live-gate.sh` check 3 is one-sided | **closed by TZ-18** | nothing. Window is `−120 … +900` s, both sides named in stderr, both constants single-site |
| `'**/*.md'` root-level claim | **withdrawn by TZ-18** | nothing. The claim was false: runner history shows three root-Markdown pushes and no bot run. `'**.md'` was adopted anyway, for the ambiguity, not for a repair (inv. 52) |
| `live-gate.sh` sits under `bench.yml`'s `analyst/**` ignore | **closed by TZ-19** | nothing. Proven on the runner: a push carrying only the script now starts the gate |
| `bench.yml`'s analyst ignore must grow with the written set | watched | any TZ or methodology change that adds a file the analyst writes. A forgotten entry burns a gate per run — loud, not silent (inv. 53). **`analyst/owner.json` is now the first file in that tree the analyst does NOT write and still qualifies:** it is pushed by the Boss, so every upload fires the full thirteen-step gate. Deliberately not fixed alone — the file changes rarely and the cost is runner minutes, which is inv. 53's correct direction to fail in; the line is added by the next TZ that opens `bench.yml` for another reason |
| `analyst/live.json` producer emits a stray newline | **closed — measured 31.08.2026T10:03:40Z on a live payload** | nothing. The Shortcut no longer emits the raw LF inside the symbol list: a payload of `n:29` parses, `n == len(c)`, every `p`/`h`/`l` casts to a finite positive, no symbol carries whitespace, no duplicate. **The row above it was stale for days and nobody re-measured it** — the Architect read a recorded blocker as current state and reported the engine unusable when it was not. That is inv. 52 applied to this map's own rows: a row resting on a measurement falls with it, and a blocker is re-measured before it is repeated |
| First live analysis runs | **31.08 two runs, 01.09 one run, 02.09 one run, all measured** | nothing. The gate's freshness window is `−120 … +900` s and is a GATE budget, not a RUN budget. The 14:29Z run of 31.08 passed the gate three times and published no level; the 20:32Z run froze levels at gate step 4 and published two setups. **The 01.09 run proved the repair incomplete rather than wrong:** the freeze held every level, and the same window then demoted every status, so the answer carried a correct strategy table under «СДЕЛОК СЕЙЧАС НЕТ». The constant has still never moved; the object it governed was wrong twice, each time smaller than the last (inv. 57). **The 02.09 run is the first with no clock defect at all** — gate green at 116 s after a fetch that had moved the payload, one freeze, levels traced to the payload and to a 14.7-hour-old journal file, and not one number off the open web. Its four defects were all of the kind inv. 58 names, and none of them touched a price |
| A rule moved between environments is re-derived, not copied | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-a** | nothing. The 15-minute price age was written where the Boss pasted the payload into chat, so «re-pull before sending, or the coin leaves the answer» had two live exits; moving the reader into the repository closed the first and left the sentence untouched, and the file's own provenance table certified the clause carried «byte-equivalent in substance». Byte-equivalence WAS the defect. Appendix A now records that a provenance table asserting a clause unchanged is asserting the environment did not matter |
| A cache keyed by a stage's NAME hides a widening of its CONTENT | **closed by `ANALYST-INSTRUCTIONS.md` §6a, and it paid on the first run** | nothing. Each stored sweep now records the contract MD5 it was read under and is stale when that differs, whatever its age. The motivating case and the first catch are the same one: the international-institutional lane and its named host were added on 30.08, the 31.08 morning run found `horizon` two days inside a seven-day limit and never opened the host, and the evening run — forced to re-sweep by the MD5 rule — found a G20 finance ministerial in session with digital assets on its published agenda. Without the rule that event stayed invisible for six more days |
| The engine reads `fr` but not `oi` or `mark` | **closed by the run of 02.09** | nothing, and it is now checklist item 23. The FIL refusal was built on rising open interest with positive funding — fresh buying rather than short-covering — and that read is what kept the coin out of a short into strength. Four runs printed funding alone before an item existed to check the columns beside it, which is the whole argument for §7 growing by measurement. Original entry: Every row of `analyst/live.json` carries funding, open interest and mark beside the price, so positioning is a read of a file already open and costs nothing. Methodology §5 step 6 has mandated it since `2026-09-01-a`; **three runs have now printed funding and none has read the column beside it.** Not a defect in the payload and not a missing source — an unexecuted clause, which is the class §7's checklist exists to convert into a check |
| The freeze aged out the STATUS after `-a` moved it off the LEVELS | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d; inv. 57** | nothing. There is one clock in a run and it stops at the freeze: the `СЕЙЧАС`/`ЖДАТЬ` split is decided once, against the frozen price, and prints that price in its own cell. **The measurement behind the demotion never existed** — the engine cannot re-pull, so every later moment compared the same number against a longer wait. Measured 01.09: gate green at 65 s, ADA short at 0.1998 inside 0.1985–0.2020, composition past fifteen minutes, and the section printed «СДЕЛОК СЕЙЧАС НЕТ» over a correct table |
| Outside-list candidates had no price lane | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d** | nothing. §3B now prices them from the payload's `x` array — the exchange's own book from the Boss's own network, frozen with everything else — and the two-source web rule is retired: membership of `x` and tradability on a USDⓈ-M perpetual are the same fact, so nothing is left for the old rule to govern. Measured 01.09: APT (unlock 11.09) and CELO (hardfork 10.09) were fully argued and dropped for want of two web quotes, while both prices sat in the file the run had open |
| An analysis run's direct push has no failure branch | **closed by contract v17** | nothing. `git pull --rebase` and push again; a second rejection is one reported line and the answer is still sent. Four clauses said `analyst/**` goes straight to `main` and none said what happens when that push is REJECTED — which is ordinary, because the Shortcut writes `analyst/live.json` to `main` while the run composes. With no branch defined the run fell into §8's pull-request fallback, written for role 1 and carrying no role qualifier, and the engine's own state waited on a human merge. §8 now opens by putting role 2 outside every branch clause in it |
| `analyst/live.json` growth in git history | watched | ~280 KB per LIVE SNAP, several snapshots a day — hundreds of MB a year, in the one file that is replaced in place and therefore keeps every version as a distinct blob. Act if the clone becomes unwieldy. **The answer is archival, never a smaller snapshot:** the payload's width is what made §3B's price lane possible, and trimming it to save history would spend a capability to buy disk. Same standing as `journal/**` growth, and recorded here so the monthly audit stops rediscovering it |
| `home.treasury.gov` refuses this machine | **measured 31.08.2026T20:32Z — timeout on direct fetch** | any egress change. The G20 finance-track text was read from a documentary archive carrying the same release verbatim, and `ANALYST-INSTRUCTIONS.md` §6 now names that class: an archive of a primary's own words is admissible for a DATE and a FACT while the primary is unreachable, for nothing else, and the primary is re-attempted every run. Re-measure before citing this row as current (inv. 56) |
| CANON Part I amputation | prepared, held | one verified analysis run. Removing the Architect's engine before its replacement has produced a correct answer leaves no fallback |
| ETF flow figures have no reachable primary lane | **closed, deliberately** — the three probe rounds behind it are **measured, date unrecorded** | a named machine-readable endpoint from an issuer or a listing venue, arriving as a TZ. Three probe rounds from the VPS found none: issuer pages 403/429, Bitwise 200 alone is not the dominant fund, Cboe and Fidelity answered 404 on guessed paths, an NYSE quote page carries price and not creation/redemption. A figure is therefore not published and a direction is not published; press-sourced readings still inform the run internally (methodology §6). **A run never re-probes this** — rediscovering a closed lane every day is the failure this repository exists to prevent |
| Producer clock drift is unmeasured | watched | the floor refuses a payload more than 120 s ahead and nothing tracks approach. `age_sec` is signed and already recorded in the day log, so drift becomes visible before it becomes a refusal |
| Beta history in `history.json` | reserved | future analysis of beta stability and horizon calibration |

| `index.html:799` restates the registry schema | open, unowned | any TZ that opens `index.html`. The comment lists seven fields and the schema now has eight. **The repair is deletion, not synchronisation** — replaced by a pointer to `bench/catalyst_bench.js`, or the schema keeps living in three files (inv. 20) |
| `main.yml` `paths` allow-list | **closed by TZ-23, merged** | nothing on the filter. The residual is a coupling, not a defect: the list must grow the first time `main.py` reads a repository file, no bench can enforce it (§11), and today's derivation is nil so the list is as small as it can be. A second reading arrives free — `journal/**` used to qualify to start the bot and was stopped only by `[skip ci]` in every journal commit subject, so a message convention was the whole control; the allow-list removes that dependency |
| `claude/tz-20-catalyst-registry-content` was never merged | **declared dead — do not merge** | nothing. `federalregister.gov` is absent from `PRIMARY` on `main` (measured), while TZ-20's immutable report describes adding it. Merging now would reintroduce a PRIMARY host for regulatory and macro events — **the exact class §3.15 closed permanently** — and would roll `catalysts.json`'s ENA entry back to the version TZ-21 superseded. The branch is retained as evidence in the standing of `CryptoTZ/TZ-03-report-delivery.md`. If TZ-20's four `QCASES` boundary cases are wanted, they arrive in their own TZ on their own merits, never as a side effect of a merge |
| A coin refused on both sides never reached the Boss | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d** | nothing. `ИЗБЕГАТЬ` now carries two classes — a bare name for an entry refusal, `XXX до ДД.ММ` for one that lifts on a dated event — and a coin refused on both sides is named rather than absent. Measured 01.09: HYPE was barred for the 06.09 unlock, the reasoning was in the internal appendix, and the answer said nothing about HYPE at all. A refusal that is not printed is indistinguishable from a coin nobody examined (inv. 37) |
| Four methodology clauses named an object and no computation | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-02-b; inv. 58** | nothing. The audit of 02.09 found one mechanism four times, in the most disciplined run this engine has produced. `dclass` now records who established a date and is read by both rules that needed it — the counter's exemption and §2's dated prohibition class; the §6a hash is a written command over a named span and its field is `sec6_md5`; checklist items 25–28 compare the answer against `items`, against state and against the horizon store rather than against the run's memory of what it wrote. **The run kept two items alive at `unver 2` to avoid lifting a prohibition that its own `signal` items were already holding** — a rule broken to buy something already owned, which is what deciding in the minute before publication looks like from outside |
| An analysis run's landing place depended on its checkout | **closed by contract v18** | nothing. The 02.09 run executed inside a harness worktree with no upstream, brought its tree to `origin/main` by ff-only merge — correctly — and then had to argue past a clause reading «never starts from a branch», which named a checkout where it meant a tree. §4b step 2 now states the two facts it was always about (tree byte-identical to `origin/main`, reached without a merge commit) and step 8 pushes `HEAD:main` by explicit refspec. **The refspec is the load-bearing half:** inv. 54 forbids the day log from reporting its own push, so a target that depends on the checkout is a landing nobody can name until the next run reads a stale state. Whether that run's own commit reached `main` is still unknown here and is reported by the next run under methodology §12 |
| A carried catalyst printed a verified status on an unread source | **closed by `ANALYST-INSTRUCTIONS.md` 2026-09-01-d** | nothing. Status `НЕ ПРОВЕРЕНО`, purely subtractive in the standing of inv. 31, counted per item and closing as `ИСТЕКЛО` on the second consecutive run. **A DATE established by a primary is permanent and is never re-established; the ASSESSMENT built on it decays** — the distinction the engine reached by hand three times on 01.09 with no rule to reach it by |
| Nothing verifies that an accepted TZ's branch reached `main` | open, unowned | the next TZ touching the audit procedure. TZ-20 sat unmerged across four subsequent TZs and a monthly audit without being noticed, because §13's rule reads «executed ⇔ a report exists in `CryptoReports/`» and a report exists for work that never landed. **The gate count masked it rather than exposing it:** step 8 agreed at 23 062 the whole time, and the agreement was evidence that nothing on `main` ever reflected TZ-20, not evidence that it had. The check is one command — `git merge-base --is-ancestor <branch> origin/main` per open branch — and it belongs in the audit, not in a bench |
| The Executor's VPS cannot run gate step 5 under `bench.yml`'s own command | watched — **measured 31.08.2026**, TZ-23's session | nothing. `direction_bench.py --control` exhausts V8's default old-space on a 955 MB single-CPU host; reproduced on a pristine `origin/main` tree and cleared by `NODE_OPTIONS=--max-old-space-size=2600`, so it is a ceiling and not a defect. `ubuntu-latest` has no such ceiling. Recorded so a future session does not read the OOM as a product failure and does not edit a bench to make it pass |
| `tokenomist.ai`, `cryptorank.io` egress | **measured 30.08.2026T18:07Z (TZ-22) — both open at the network layer** | nothing on egress. The reading is a point in time behind Cloudflare and is replaced by a later reading, never argued with (inv. 52). What remains is not an egress question and carries its own row |
| §6a discovery host | **closed by TZ-24; the readings behind it measured 30.08.2026T20:42Z — both hosts refused on the data question** | nothing, and a run never re-probes them. Permission was answered — `tokenomist.ai/robots.txt` grants `Allow: /` to a group naming `ClaudeBot`, `Claude-SearchBot`, `anthropic-ai` and `Claude-User`; `cryptorank.io` names no agent beyond `*`. **Extractability was answered and it is what closes the lane:** the unlock-events page serves the boolean `isUnlockScheduleEmpty` and no schedule, nine schedule key names return zero across 617 540 bytes, and a fund's rounds page serves dated round records whose element schema carries no amount, valuation or investor key. Both load those figures client-side from a credentialed API. §6a now records the closure so no future run spends a fetch rediscovering it |
| A reachability control that fails only at DNS | **partly closed by TZ-24, measured 30.08.2026T20:42Z; one layer still unproven** | any future egress TZ. TZ-24 added `192.0.2.1` (RFC 5737) beside the `.invalid` host and the exit codes differ — 6 at resolution, 28 at connection — so the instrument is now known to distinguish the two layers. **The residual is mine and is the reading that matters most:** TEST-NET-1 is blackholed, so control 3 times out (28) rather than being refused (7), and a REFUSED connect is the old cloud sandbox's exact signature. A third control returning exit 7 — a loopback port that actively rejects is enough, since the claim is about the instrument and not about egress — belongs beside the other two |
| Report template lets inv. 54 rest on the author's care | **closed by contract v15** | nothing. **Not a TZ, and the row that said so was wrong:** `EXECUTOR-INSTRUCTIONS.md` is Architect-owned and arrives by Boss upload (contract §2), so the Executor may never write it (contract §7.14) and a TZ asking it to would be defective. The repair is an Architect edit forced by TZ-22, in the standing of v13 and v14. §8 now names the two TZ classes once and every branch clause is silent on a report-only TZ instead of deviated from; §10's `## Commit` and `## Pull Request` read off the class; a hash appears only for a commit already pushed. **A bench over `CryptoReports/**` was considered and is impossible**: a report is pushed direct to `main` on a path both workflows carry in `paths-ignore` as `'**.md'`, so such a control could never fire — the template is the only place this rule can live |
| Executor has no GitHub API access | **closed, deliberately** | nothing. `gh` is absent and no PAT exists; the deploy key `crypto-auto-vps` carries git write and that is the whole of the Executor's reach. A fine-grained PAT cannot separate «push a branch» from «merge to main» — both need `Contents: write` — and the hosted-gate reading it would automate is already performed by the actor who opens the pull-request page to merge. The gap is closed in the CONTRACT instead: CI evidence left the Executor's acceptance criteria and became an audit step (contract §9) |

**Standing decisions.** No new coins beyond 28 · weights are never tuned · the
directional layer is closed at the current evidence level: the machine owns risk,
sizing, honesty and geometry, the human owns direction via catalysts and REVIEW.

---

## 11. Analytical engine — `analyst/**`

**The Claude Code Executor carries two roles.** Role 1 implements an approved TZ;
role 2 is the operational market-analysis engine. One process, one contract
(`EXECUTOR-INSTRUCTIONS.md`), two roles, never both in one turn. The methodology —
what is analysed, what is published, in what shape, under what data discipline — is
`ANALYST-INSTRUCTIONS.md`, which stands to role 2 exactly as this map stands to role 1:
binding text the Executor reads and never writes.

**This section states what the engine IS.** It carries no analytical rule, because a
rule written here and in the methodology would eventually be written two ways.

| Path | Written by | Retention |
|---|---|---|
| `analyst/live.json` | the Boss's iOS Shortcut | one copy, replaced |
| `analyst/owner.json` | Architect → Boss upload | one copy, replaced |
| `analyst/state.json` | role 2 | one copy, replaced |
| `analyst/log/YYYY-MM-DD.md` | role 2 | **permanent, immutable** |
| `analyst/live-gate.sh` | role 1, under a TZ | live |

**The engine performs no network fetch for PRICES, and that is a measurement rather than
a preference (TZ-16).** Measured in the cloud sandbox, every market host was refused at
CONNECT — `fapi.binance.com`, CoinGecko, `gist.githubusercontent.com`, and
`data-api.binance.vision` **which inv. 24 permits from a runner**. The runner's egress and
a session's egress are different networks and neither may be assumed from the other.

**Since 2026-08-30 the engine runs on a Vultr VPS, and the egress was re-measured there
rather than inherited (inv. 52).** The sandbox proxy is gone and the picture is different
by host class, not uniformly better: `federalreserve.gov` open · `bls.gov` and
`defillama.com` serve their APIs and refuse the rendered page with 403 · `farside.co.uk`
answers a managed bot challenge · ETF issuer product pages refuse the VPS — BlackRock and
ARK 403, Grayscale 429, Bitwise 200. **A 403 on a page whose API answers is not a closed
lane**, which is why the methodology names the machine-readable endpoint as the primary
artifact.

**`tokenomist.ai` and `cryptorank.io` were measured by TZ-22 and both answer this
machine.** Apex and `www` resolve to Cloudflare, TLS completes against a valid
certificate, the rendered page returns 200 carrying its own product title and none of
the four managed-challenge markers, and `robots.txt` serves. Their DATA APIs are
credentialed and this repository holds no key: `api.tokenomist.ai/v4/token/list` answers
401 `x-api-key not found`, and `api.cryptorank.io` declares `X-Api-Key` as its only
security scheme across 76 paths, with `/v3/documentation-json` and `/v3/ping` as the
keyless exceptions — `/v3/ping` returns a server clock and no data. **An open lane is
neither an extractable figure nor a permission, and TZ-22 measured only the lane.** Both
pages are JS-hydrated applications, so whether a figure can be read out of the served
HTML without executing JavaScript is untested; and `tokenomist.ai/robots.txt` carries a
directive group naming `ClaudeBot`, `Claude-SearchBot` and `anthropic-ai` whose contents
that run did not quote. The run's own client was `curl/8.5.0`, which the `*` group admits,
so the measurement is clean — but a methodology naming the host would be admitting it for
an agent the host addresses by name.

**TZ-24 closed both questions, and the answer is no.** Permission: `tokenomist.ai` grants
`Allow: /` to a group naming `ClaudeBot`, `Claude-SearchBot`, `anthropic-ai` and `Claude-User`;
`cryptorank.io` names no agent beyond `*`. Extractability: both pages DO carry a
machine-locatable payload without JavaScript — an RSC flight stream of 352 138 B and a
`__NEXT_DATA__` block of 43 757 B — **and neither payload contains the data a sweep needs.** The
unlock-events page serves the boolean `isUnlockScheduleEmpty` and no tranche array, and nine
schedule key names return zero occurrences across the whole document; a fund's rounds page serves
dated round records whose element schema has no amount, valuation or investor key. The figures
arrive client-side from the credentialed API that answered 401. **A lane can be open, permitted
and parseable and still be closed**, and that is why the two verdicts were kept apart: a single
`usable` label would have named both hosts in §6a and every sweep would have located a payload,
found nothing in it, and reported an empty result indistinguishable from a quiet market.
`ANALYST-INSTRUCTIONS.md` §6a records the closure so no run re-probes them.

Price delivery is unchanged regardless: `analyst/live.json` reaches the engine
through the Boss's Shortcut and the working tree, and no measurement of this machine
reopens that. The one surviving route to the payload was scraping a rendered Gist HTML page;
it was refused as a transport, because a presentation detail with no compatibility
promise fails by returning something rather than by erroring, and a price behind a
stop may not depend on that. The Shortcut's collection is unchanged — same calls, same
network, same payload — and only the destination moved, so the engine reads a file in
its own tree and the transport leaves the design instead of being hardened.

**Since 01.09 the payload carries two arrays, and the second one closed the outside-list
lane the aggregators could not.** `c` is the 28-coin universe plus BTC, validated row by
row at the gate; `x` is the whole Binance USDⓈ-M perpetual book — 754 rows carrying
symbol, last, 24-hour high and low, change and turnover. **Membership of `x` and
tradability on a perpetual are the same fact**, so `ANALYST-INSTRUCTIONS.md` §3B now
prices an outside-list candidate from it and the two-source web rule is retired: nothing
is left for that rule to govern, because a coin absent from `x` was never publishable.
The lane is filtered on the symbol and the turnover — USDT quote, no `_` (dated and
COIN-M contracts), a nameable crypto underlying, and $10M of 24-hour turnover — and no
name list is written into the methodology, because a typed list is a second universe
(inv. 21). **The payload is read by command and never opened**: it is several hundred
kilobytes, a run needs a handful of rows, and a reader that pulls the whole artifact in
to reach thirty lines has taken the artifact instead of what it needed. The width is not
free — each snapshot is a new ~280 KB blob in git history, which §10 carries as an
archival question and never as a reason to narrow the payload.

**The freshness window is two-sided:** `LIVE_SKEW_SEC = 120` s below, `LIVE_MAX_AGE_SEC
= 900` s above, one declaration site each, both breaches sharing exit 3 and naming their
side in stderr. The floor exists because the producer is a phone and the reader is not:
a one-sided ceiling passes every payload stamped in the future, which is the failure the
check exists to prevent arriving through the check itself (inv. 51).

**That window is a GATE budget and was never a RUN budget, and the two were conflated
until 31.08.** The gate reads a file once; a run reads state, freezes geometry, hunts
catalysts, sweeps, composes, writes state and log, commits, and sends. Methodology §5
measured price age at the moment of SENDING, so a run doing the second job honestly
arrived at composition with the ceiling spent — and its only other exit, re-pulling the
price, does not exist for an engine whose payload is written by the Boss's Shortcut.
Since `ANALYST-INSTRUCTIONS.md` revision `2026-09-01-a` the stage order is binding and
levels are FROZEN at gate step 4, before any search: the anchoring price is fixed with
them, every later stage is subtractive, and an aged freeze demotes `СЕЙЧАС` to `ЖДАТЬ`
instead of deleting the level. **Revision `2026-09-01-d` removed that demotion too, and
the reason is inv. 57.** The demotion rested on no measurement: the engine cannot re-pull,
so a later moment compares the same number against a longer wait and can only subtract.
The `СЕЙЧАС`/`ЖДАТЬ` split is now decided once, at the freeze, and the row prints the
frozen price beside the zone — a dated claim the Boss checks against his own screen in a
second. **Nothing about the constant changed, in either revision.** What changed twice is
the object it was applied to, and the second correction is what made the first one hold:
after `-a` a thorough run still emptied its own best-trades section, because four sweeps,
a catalyst hunt and composition do not fit in fifteen minutes and were never meant to.

**The Boss's production trigger is a third spelling, not a third mode.** `ANALYZE
TODAY'S CRYPTO MARKET AND DETERMINE THE STRATEGY FOR ENTERING ALTCOINS ON BINANCE
FUTURES.` selects role 2 and runs methodology §2's skeleton identically to `Анализ
крипторынка`. It lives in `EXECUTOR-INSTRUCTIONS.md` §4 and in the methodology's §0, and
the pair moves together: §4 is the only place a role is selected, so a string present in
one file and absent from the other is an unrecognised trigger that stops the run.

**`analyst/live-gate.sh` is the blocking gate and returns an exit code** (inv. 29),
one distinct class per failure: unreadable or unparseable 2 · stale 3 · `n ≠ len(c)` 4
· a `tokens[]` symbol absent 5 · a price that does not cast to a finite positive 6 ·
zero rows compared 7 (inv. 22) · `tokens[]` unreadable 8. A non-zero exit removes
every price level from the answer and nothing else; the regime, the catalysts and the
verdict are still produced. The universe is cut from `tokens[]` at run time and never
typed (inv. 21), and the selftest's fixtures are generated from that same parse, so a
change to `tokens[]` cannot leave the selftest behind.

**The cast is explicit because `jq` is not safe on this payload.** Every value except
top-level `n` is a JSON string, and `jq '.p|tonumber'` accepts `"Infinity"` and
`"1e999"` as finite-looking positives while `"NaN"` passes a naive range check *by
failing it*: `NaN > 0` and `NaN <= 0` are both false. The validator uses
`float()` with `math.isfinite(x) and x > 0`, which rejects all four.

**The gate is wired into `bench.yml` as step 13** (inv. 37) — `--selftest`, 14
known-answer cases, 40 assertions, offline (12 failing × 3 + 2 passing × 2). That step, not a fingerprint entry, is why
`live-gate.sh` is trustworthy after the session that wrote it ended; adding the script
to the `## 0` table would put a hash in every TZ header for a file whose behaviour is
already under a control.

**The two workflows treat this tree differently, on purpose.** `main.yml` ignores
`analyst/**` whole: no file here, script included, is a reason to start the bot, redraw 28
coins through CoinGecko and rewrite the live Gist. Before TZ-17 it ignored none of them, so
the engine saving its own state did exactly that, with a retry doubling the draw.
`bench.yml` ignores only the three paths the analyst WRITES — `analyst/state.json`,
`analyst/live.json`, `analyst/log/**` — because `analyst/live-gate.sh` is code whose control
is step 13, and the wider form excluded the gate script from its own gate (inv. 53, measured
on the runner: run `33254342462`, a push carrying only the script, which started nothing
under the old filter). `analyst/README.md` needs no entry; `'**.md'` covers it.

**That narrowing creates a coupling and it is deliberate.** Any NEW file the analyst writes
must be added to `bench.yml`'s list, or it starts a 13-step gate on every analysis run.
Making the coupling mechanical would need the written set to exist as data that both the
filter and a bench read, i.e. a second list of three paths — rejected as worse than the
coupling it removes (inv. 20). The failure is loud and costs runner minutes, which is the
direction to fail in.

**Since TZ-23 `main.yml` filters `push` with a `paths` allow-list and no `paths-ignore`.**
The two cannot coexist on one event, so adopting the list DELETED the exclusions rather
than joining them — an allow-list needs none, because everything unnamed is already out.
The list is two literal paths, `main.py` and `.github/workflows/main.yml`, derived from
`main.py`'s source at execution time and never typed: the bot opens no file, imports no
repository module and reaches CoinGecko and the Gist over HTTP only, so `catalysts.json`,
`journal/**` and every future unnamed path now start nothing. `workflow_dispatch` is
unfiltered, so the phone's 17 daily runs sit outside this filter entirely and no list
written here can stop them — that is the whole safety argument and it is checked, not
assumed. **The coupling now runs the other way and into the worse direction:** the list
must GROW the first time the bot learns to read a repository file, and a forgotten entry
withholds a run quietly while `coeffs.json` ages, where inv. 53's forgotten entry only
burned runner minutes loudly. No bench can hold it — a control over a trigger would have
to observe the trigger, and `main.yml`'s `push` filter is unreachable from any `claude/**`
push — so the coupling is carried by the Russian comment beside the list and nowhere
else.

**`analyst/owner.json` is the owner's channel into the engine, and it exists because the
Boss does not talk to the engine.** He addresses the Architect; the role table forbids
making him relay a technical fact between the two systems. Methodology §11 nevertheless
declared a position «on «вошёл в SOL ЛОНГ»» — a clause inherited from the chat-era engine,
where such a sentence could actually be said. **With no channel, the relay was the only
route the information had, and the Architect took it**, telling the Boss to inform the
engine himself. A rule with no mechanism behind it is broken by whoever needs the
information to move. The file is written by the Architect, uploaded by the Boss on the
single existing channel, read at gate step 3 and never written by the engine (§13): an
input a system can edit has stopped being an input. Its two arrays have opposite
standing — `positions` are the owner's own facts and are taken as given, `vectors` are
hypotheses with no authority at all, resolved against a primary or reported unresolved,
because an owner's assertion is not a source (inv. 39) and the place that rule must hold
hardest is the place it is least comfortable.

**Two states are permanent and different.** `analyst/state.json` is the working set —
one copy, replaced every run, carrying only what is currently true. `analyst/log/**`
is evidence — written once, never reopened, in the standing of a journal record
(inv. 38). Merging them would make the working set grow without bound and the evidence
rewritable, which is the pairing §3.13 already uses.

**The engine never writes `catalysts.json`** (inv. 39). That registry vetoes the
board's verdict and its `confirmed` flag is the compensating control for an
externalised file; an analysis run able to edit it would turn one file write into a
silent change to production behaviour. A discovered event that deserves an entry is a
line in the day log, and the Architect turns it into a TZ or does not.

**The state was seeded empty, never imported.** The Gist copy written by the Shortcut
from a printed chat block carries 211 pairs of typographic quotes and an abbreviated
item schema; it fails `json.loads` at character 1, and an unparseable state file stops
an analysis run outright. Importing it would have stopped every future run — a file
that exists, looks right and is refused.
