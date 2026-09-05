# Implementation Report — TZ-29

## Status

**PARTIAL.**

The work of scopes 2.1, 2.2, 2.3, 2.5 and 2.6 is complete, committed and proven
by offline controls that run the shipping code end to end. Two things are not
closed, and neither is a CI-readability gap:

1. **Scope 2.4's second half is void, and it is void because its premise is
   contradicted by the repository.** `vol_ratio` is not `vol7 / volatility`. It
   is `volume_expansion(c_data.get('total_volumes'))` — 24 h turnover over the
   90 d median turnover — read out of `main.py`'s own AST by the bench itself.
   The quotient `vol7 / volatility` is `volRegime` in `index.html:1414-1417`,
   the §3.2 leverage cap, and it is **not a `coeffs.json` field at all**. There
   is therefore no pair of thresholds to propagate into `vol_ratio`, and the TZ
   forbids typing one. Measured, not argued: §5 item 6 below.
2. **Validation items 8, 12 and the live half of item 9 need a dispatch of
   `.github/workflows/backtest_bench.yml`, and this session cannot dispatch
   one.** No `gh`, no API token (`git` has an SSH deploy key and nothing else).
   The TZ places the top-up and the alias verification on the runner and not in
   a session (§4 item 9, inv. 44), so the outcome for the real `GRAM`/`SKY`
   archive, the real 31-of-31 census and run #15 are not in this report and
   were not manufactured.

The single action that closes item 2 is a manual dispatch of
`Backtest bench (ручной запуск)` on this branch. Item 1 is the Architect's.

## Inbound Filing

None. The TZ arrived at its own canonical path,
`CryptoTZ/TZ-29-archive-coverage-and-verify-reconciliation.md`, matching the
filename its header fixes (contract §3). No `git mv` was needed and no second
copy exists.

TZ-28's branch `claude/tz-28-scorer-extraction-and-target-bars` **was merged**
(PR #26, `4ad3759`), so this work does not build on an unmerged base.

## Scope Executed

**Branch TZ** (contract §8): the scope authorises two files outside
`CryptoReports/**`, so this opened a branch. Six scopes, five delivered, one
void by the TZ's own rule.

| Scope | Outcome |
|---|---|
| 2.1 tail top-up on the spot path | **DONE** — and the diagnosis is not the one the TZ assumed; see below |
| 2.2 coverage census on every line | **DONE** |
| 2.3 ticker alias with a derived splice test | **DONE** — rule shown to admit and to refuse; the two candidates await the runner |
| 2.4 `vol_ratio` reconcile, then threshold | **first half DONE as a reconciliation; second half VOID** — premise false, proven |
| 2.5 `--verify` signs and classes | **DONE** |
| 2.6 `--target` gated on the reconciliation | **DONE** |

## Files Created

None.

## Files Modified

- `bench/backtest_bench.py` — 2768 → 3216 lines (2.1, 2.2, 2.3, 2.4 first half, 2.5, 2.6)
- `bench/verify_bench.py` — 254 → 287 lines (2.5's expectations re-registered; check count held at 35)

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### 2.1 — the diagnosis is a publication lag, and there was never a second code path

**The TZ's framing does not survive reading the code.** `fetch_prices` had
**one** fetch path; spot and perp both went through `_vision_rows` and both
reached the same tail top-up. The asymmetry was never in the code — it is in
which files the two archives carry.

Two independent lines of evidence.

**Arithmetic, from run #14's own printed numbers.** `--fetch` prints hours
PRESENT and the hole percentage, so the missing count is `hours/(1−p) − hours`,
not `p × hours`. On the four series the TZ names that gives 739, 744, 736 and
740 h, and every one of them is inside the rounding band of **744 h = 31 days =
one whole calendar month**. A constant that is 744 h on series of 25 664,
20 520, 20 300 and 17 760 h is calendar-aligned, not proportional — which also
says the block is INTERIOR, because `_save`'s `gaps` is measured across
`ts[-1] − ts[0]` and a tail deficit falls outside it.

**Direct measurement, HTTP status only, no price read** (contract §7 item 9's
environment clause; commands and results together):

```
$ python3 -c "import requests; ..."   # HEAD, BTCUSDT, 05.09.2026
data-api futures klines    404      https://data-api.binance.vision/fapi/v1/klines?symbol=BTCUSDT&interval=1h&limit=1
data-api spot klines       200      https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=1
vision futures um daily    200      .../futures/um/daily/klines/BTCUSDT/1h/BTCUSDT-1h-2026-09-03.zip
vision spot daily          200      .../spot/daily/klines/BTCUSDT/1h/BTCUSDT-1h-2026-09-03.zip
vision spot monthly 08     404      .../spot/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2026-08.zip
vision um monthly 08       200      .../futures/um/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2026-08.zip
vision spot monthly 07     200      .../spot/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2026-07.zip
```

The monthly aggregate for the **last complete month** is published on
`futures/um` and not yet on `spot`. The old daily-refill loop covered
`months[-1]` — the CURRENT month — and broke the moment the day rolled into the
previous one, so the whole of the last complete month was never fetched by
either route on a spot pair, and always was on a perp one. The tail top-up
could not save it because `tail` is computed from `max(rows)` and September's
daily files were already in `rows`: the hole is behind the last row, not in
front of it.

**The repair does not depend on that measurement being true.** `_vision_rows`
now records which months the monthly ZIP did not carry and refills **every** one
of them from that month's daily files, whatever the reason it was absent.
Months before the pair's first archived month are skipped, because they are
pre-listing and have no daily files either — and that window is read off the
data (the first month that answered 200), never declared.

**A second, silent defect was found and repaired in the same function.** The
tail top-up called `_rest_rows("https://data-api.binance.vision",
"/api/v3/klines", …)` — the **spot** endpoint — for a perpetual leg too. The
mirror carries no futures endpoint (measured above: 404) and `fapi.binance.com`
is inv. 24, so every `fut:true` series was having roughly a day of **spot**
candles spliced onto its tail. That is exactly the silent failure mode the TZ's
model note names: a wrong join fabricates a move the whole bench then measures,
and it is very probably part of why the perps read 0.0–0.1 % missing. The
top-up is now spot-only; a perpetual's archive lag is **reported by the census**
instead of being papered over with the wrong instrument.

The top-up now also stops at the **last complete hour** rather than at `now`,
so the hour in progress can no longer enter the series as an hourly close.

**This will cost the perps their 0.1 % tail bar** (§5 item 8). That is the
correct direction: hiding a wrong-instrument splice to reach a number is what
hard floor item 2 forbids, and the number is now reported honestly instead.

### 2.2 — the census

`census(P, t_ref)` returns hours present, first and last stamp, **tail deficit
to the last complete hour**, **interior gap count**, total interior hours, and
the largest interior gap with its own start and end. `print_census` prints one
line per **attempted** symbol — accepted, skipped, restored from the Actions
cache, or refused — and `_save` now returns `(bool, verdict)` instead of
printing, so the verdict and the census are one line and cannot drift apart.

Tail and interior are separate numbers, deliberately: that separation is what
decides whether the top-up was the whole defect, and an interior gap that
survives it is a finding for the report and not a repair in this TZ. Nothing in
the bench acquired a gap rule — production's cut code still owns that (inv. 21,
inv. 38).

The census is stored in the cache file under an additive `"cov"` key, exactly as
`"hl"` is (inv. 1, 9): `--verify` reads it, and a reader that does not know the
key is unaffected. A cache restored without it falls back to
`census_of_doc`, so no line is ever missing.

**The two existing skip rules did not move**: 2600 hours of history and the 5 %
hole fraction are the numbers they were (inv. 47, hard floor item 2).

### 2.3 — the alias

```python
ALIAS = {"GRAMUSDT": "TONUSDT", "SKYUSDT": "MKRUSDT"}
```

Two candidates and nothing else is asserted. **The cutover is not written into
the code either** — it is read off the archive as the first hour the new pair
carries, and the pre-rename leg is whatever the old pair carries before it.

`_splice` is the admissibility rule and it is arithmetic (inv. 49): the joint's
own return across the splice is admitted only if it lies inside the
**hourly-return extremes the two legs themselves exhibit**, taken between
adjacent buckets only, inside each leg separately — production's own gap rule
(map §2), never across the joint being judged. No numeral appears in the rule,
in the code, or from the TZ. A refused splice is not a failure: the symbol
enters by its post-rename leg alone, and the refusal is printed beside the
joint return that caused it, the extremes it was compared against, and the
count of hourly pairs those extremes came from (inv. 43).

If that leg is then shorter than the skip rule, the coin is **legitimately
absent**, and the second commit on this branch exists to make the line say so:
the census now reports the BEST attempt across legs, because a spot symbol
whose post-rename leg is real but short falls through to a futures leg that
does not exist for it, and reporting that second attempt printed «строк 0»
where the fact is «1500 h, refused by the skip rule».

### 2.4 — what `--verify` compares for `vol_ratio`, established

The bench already cuts production's coin-metric block out of `get_token_betas`
by AST. `bot_field_expr` now reads the **expression** a field is built from out
of that same AST, and `--verify` prints it:

```
vol_ratio построен продакшном как: volume_expansion(c_data.get('total_volumes'))
  — это ОБОРОТ, а не vol7/volatility (то частное — volRegime во фронте и полем
  coeffs.json не является); порога не имеет
```

That single printed line is the reconciliation. `vol_ratio` is turnover;
`vol7` and `volatility` are price quantities; the field is not a function of
them, so no bound derived from their deviations can constrain it and none is
attached. The `info` kind is now handled **explicitly** rather than falling
through into the `rel` branch — same measure, stated instead of inherited.

Why the deviation is large in production is now also identifiable rather than
mysterious: `volume_expansion` is `last 24 h turnover / median 90 d turnover`,
the bench's cache carries **Binance quote turnover** (`_series_from_rows`,
column 7, rolling 24 h) and `main.py` reads **CoinGecko's composite
`total_volumes` across every venue**. Two different turnover series, one
scale-free ratio, spot and perp alike — which is exactly the TZ's own
observation that ten of twenty-seven violate the bound on both sides of the
venue split and that the five zero-hole controls violate it too.

**No threshold was added.** 2.4's own rule — «the second half is void without
the first» — is what governs, and the first half's stated goal («make the
printed deviation consistent with the deviations of `vol7` and `volatility`»)
cannot be reached by any implementation because the relation it assumes does
not exist. Typing a number here would be the numeral inv. 49 refuses.

### 2.5 — signs and classes

- **Deviations carry their sign.** `pp`, `abs` and `rel` all keep `a − b`; the
  threshold comparison is on the magnitude; the table and the per-field summary
  print `%+`. `worst` keeps the signed value of the largest magnitude.
- **Every failing cell is classified**, and the class table prints a count per
  class and every cell under it (inv. 43). A class with no cells prints as zero
  rather than being omitted.
- **`venue-basis` is READ from the calculation that already produces the
  `БАЗИС ПЕРП/СПОТ` line** — the cell is appended to `basis` and classed in the
  same statement. There is no field-family label anywhere. That is what keeps
  `min_price` on XMR and `eff14` on XMR and HYPE inside the basis lane instead
  of pushing them into `unexplained` (inv. 58). The identity of the two sets is
  asserted offline in `verify_bench.py` (`basis_sets`), which now requires the
  classifier's `venue-basis` set to BE the printed note, cell for cell.
- **`coverage`** is decided by the field's OWN window against the census.
  `bot_field_windows` reads the windows out of `main.py`'s AST — the
  `window_stats`/`window_vol` calls and the constants they take — so 7/14/30 is
  not written down a second time (inv. 20, 58); anything the block does not
  build from an explicit window is measured over `CdBuilder`'s 90-day cut, and
  `eff14` takes the wider of its two inputs. The verdict names the gap.
- **The verdict is decided by the class.** `venue-basis` is reference;
  `coverage` and `unexplained` return non-zero.

**This retires the v3 single-outlier licence of 12.08.2026, and that is a
tightening, not a loosening.** The v3 rule let one coin over the bar exit 0 at
any magnitude, and it existed precisely because one threshold table was
reporting three causes as one verdict — the thing 2.5 exists to end. The
pipeline protection it provided is now provided where it belongs: 2.6 removes
the symbol from `--target` instead of the run swallowing the disagreement.
`verify_bench.py`'s two v3 assertions are re-registered against the class rule,
in place, and the file's check count is **unchanged at 35** so the gate figure
does not move.

### 2.6 — the gate

`verify_against_live` was split. `reconcile()` does the comparison and returns
it — no printing, no exit code. `verify_against_live()` prints it and returns
the code. `--target` calls the same `reconcile()`.

**The gate is computed inside `--target`, not read out of a file `--verify`
writes.** `backtest_bench.yml` runs `--target` BEFORE `--verify`, so a gate that
depended on the step order would not be a control over the numbers it guards
(inv. 62), and one reconciliation serving both is inv. 20.

A symbol whose class is `coverage` or `unexplained` is dropped from every arm
and named with its class in «ЧТО СРАВНИВАЛОСЬ». Below quorum, **no `Ω` and no
`k*` are printed** and the line says which class removed the setups. If the
reconciliation cannot be obtained at all, `--target` stops with that reason
rather than measuring ungated.

**No bar moved and no primary changed.** `Ω` is still read against
`1/RR_MIN = 0.50` and `k*` is still the smallest `k` whose CI95 covers it. One
line was added stating the arithmetic, and the arm's mean `1/RR` is now printed
beside `Ω`.

## Validation

Every item was run. Two failed and both are reported as failures, not as «not
applicable». Environment note recorded once: this container has 955 MB of RAM
and node's default heap dies inside `direction_bench.py --sim`; every gate
replay below ran with `NODE_OPTIONS=--max-old-space-size=4096`. That is a
property of this session, not of the repository.

**Baseline, before any edit** (`origin/main` @ `69047d5`):
`--probe` 5/5 answered; `verify_bench.py` `checks run: 35 FAIL 0`, exit 0;
`--selftest` exit 0; `--lab-selftest` exit 0; gate replay 13/13 green,
**1 255 401** checks.

| # | Item | Command | Result |
|---|---|---|---|
| 1 | compile | `python3 -m py_compile bench/backtest_bench.py bench/verify_bench.py` | exit 0 |
| 2 | offline rule suite | `python3 bench/verify_bench.py` | `checks run: 35 FAIL 0`, exit 0 |
| 3 | census self-proof | harness `case_census_selfproof` | **PASS** — see below |
| 4 | alias identity control | harness `case_identity` | **PASS** — 9/9 MD5 identical |
| 5 | splice negative test | harness `case_splice_negative` | **PASS** — planted ratio refused |
| 6 | `vol_ratio` coherence | harness `case_vol_ratio` | **FAILS 8 of 8, and cannot pass** — see below |
| 7 | `--probe` | `python3 backtest_bench.py --probe` | 5 hosts, all 200 **from this session** |
| 8 | `--fetch` 31 of 31 | needs a runner dispatch | **NOT RUN — no dispatch capability** |
| 9 | `--verify` live | needs a runner dispatch | **NOT RUN**; the classifier's known-answer identity proven offline |
| 10 | `--verify` negative test | harness `case_verify_negative` | **2 of 3 return non-zero**; `vol_ratio` cannot — see below |
| 11 | `--selftest` / `--lab-selftest` | both modes + negative control | **PASS** — byte-identical to baseline |
| 12 | `--target` run #15 | needs a runner dispatch | **NOT RUN — no dispatch capability** |
| 13 | gate no-regression | 13 steps replayed locally | **1 255 401, delta zero** |
| 14 | extremes | harness `case_extremes`, `case_nan_forced`, `case_target_gate` | **PASS** — 7 of 7 attempted |

**The harness.** Items 3, 4, 5, 6, 10, 14 and 2.6's gate run through a synthetic
`data.binance.vision` that serves real ZIP bytes into the bench's own parser,
with `requests` replaced. No network, no product fact, and the code under test
is the code that ships, not a copy of it. It lives outside the repository
because the TZ authorises no new file and forbids opening `bench.yml`; that is
a gap and it is named under `## Remaining Risks`.

## Test Results

### 3 — census self-proof

48 hours deleted from a cached symbol, ten days back, then restored:

```
удалено 48 часов, окно 2026-08-26T16 .. 2026-08-28T15
ПЕРЕПИСЬ говорит: дыр 1 · крупнейшая 2026-08-26T16 .. 2026-08-28T15 (48 ч)
--verify классы: AAA coverage · DDD unexplained · EEE clean · FFF clean · ...
код возврата 1
восстановлено: md5 f4b11bc628f2be210d91655b01985e10 -> f4b11bc628f2be210d91655b01985e10 · совпало: True
```

The census names the deleted span exactly. The **same planted deviation** is
`coverage` on the symbol with the gap and `unexplained` on the symbol without
it — the classifier is reading the census, not guessing. Cache restored
byte-identical.

### 4 — alias identity control (inv. 45)

With every old leg positioned so nothing can splice, the alias path runs in
full — both fetches, both judgements printed — and the cache is byte-identical
to a run with the table empty, on all nine files:

```
    СКЛЕЙКА TONUSDT -> GRAMUSDT · стык 2026-04-08T17 · плечо до 0 ч · доходность стыка — за 0 ч
    крайности ряда [—; —] по 0 часовым парам -> ОТКЛОНЕНА: плеча до переименования нет
  РЕЗУЛЬТАТ: кэш байт в байт одинаков: True
```

### 5 — splice negative test (inv. 23)

An admitted splice, then the same splice with a fabricated 1/137 ratio planted
on the old leg:

```
до подсадки:    доходность стыка +0.0000 за 1 ч
                крайности ряда [-0.0020; +0.0020] по 8806 часовым парам -> ПРИНЯТА
после подсадки: доходность стыка -0.9927 за 1 ч
                крайности ряда [-0.0020; +0.0020] по 8806 часовым парам -> ОТКЛОНЕНА: стык ВНЕ собственных часовых крайностей ряда
GRAM после отказа: GRAM  GRAMUSDT  2026-04-08T13 .. 2026-09-05T12  3600 ч  ok
```

The rule admits, the rule refuses, and a refused symbol enters on its
post-rename leg alone.

### 6 — `vol_ratio` coherence: the acceptance test cannot be satisfied

Live record rebuilt on a **different turnover series** and identical prices —
the real situation, since `main.py` reads CoinGecko's composite volumes and the
cache carries Binance's:

```
монета        vol7   volatility      граница    vol_ratio внутри?
AAA         0.000%       0.000%       0.000%     134.740%  НЕТ
DDD         0.000%       0.000%       0.000%     134.740%  НЕТ
EEE         0.000%       0.000%       0.000%     134.740%  НЕТ
FFF         0.000%       0.000%       0.000%     138.100%  НЕТ
GRAM        0.000%       0.000%       0.000%     134.740%  НЕТ
HHH         0.000%       0.000%       0.000%     134.740%  НЕТ
JJJ         0.000%       0.000%       0.000%     134.740%  НЕТ
SKY         0.000%       0.000%       0.000%     125.230%  НЕТ
вне границы: 8 из 8
vol_ratio построен как: volume_expansion(c_data.get('total_volumes'))
vol7 построен как:      window_vol(c_data['prices'], 7)
volatility построен как:float(np.std(np.diff(c_prices) / c_prices[:-1])) ...
```

**`vol7` and `volatility` deviate by exactly zero and `vol_ratio` moves 134 %.**
The bound the TZ derives from those two components is identically 0.000 %, on
clean data, with no coverage defect available to blame. This is not evidence
that the reconciliation was done badly; it is a proof that the quantity being
bounded is not a function of the bounding quantities. Item 6 fails at 8 of 8
and would fail at 5 of 5 on the live set for the same reason.

### 10 — `--verify` negative test (inv. 29)

```
уровень min_price +5 %   -> код 1   AAA unexplained · DDD unexplained · EEE unexplained · FFF venue-basis
доходность r7 +5 пп      -> код 1   AAA unexplained · DDD unexplained · EEE unexplained · FFF venue-basis
vol_ratio x3             -> код 0   AAA clean · DDD clean · ...
без подсадки             -> код 0
```

A level field and a return field both **return** non-zero and name the class.
`vol_ratio` cannot, because it carries no threshold — and 2.4's second half,
which would have given it one, is void. **This item fails**, and the failure is
downstream of the finding rather than of the implementation.

### 11 — `--selftest`, `--lab-selftest`, and the negative control

Both modes are **byte-identical to the baseline**, diff empty, exit 0:
T1/T2/T3 green, three worlds × 10 seeds, `SE(IC) ≈ 0.030`; lab A–D with
`D1 0.93 [0.69;1.16]`, `D2 0.287 > 0.121 > 0.055 > 0.018`, `D3a/b/c` green,
`D4 сравнений 7848, расхождений 0`, `D5` green, `D6 лонг 0.037 · шорт 0.013`.

Negative control, `_touch_calc`'s long/short branch inverted:

```
D1 калибровка цели, k=1.5: 7.48 [7.48; 7.48] СТОП
D2 монотонность Ω(k): nan > nan > nan > nan СТОП
D3a/D3b/D3c СТОП
D4 тождественный дифф: сравнений 7848, расхождений 0 ОК
D5 взгляд в будущее: совпала ОК
D6 обмен сторон: Ω лонг nan · Ω шорт nan СТОП
ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить      (exit 1)
```

D1, D2, D3, D6 red; D4, D5 green; exactly as registered. Reverted; output
byte-identical to baseline again.

### 13 — gate no-regression

13 steps replayed locally, all exit 0:

```
109 + 130 + 372 + 35 + 255708 + 3424 + 693895 + 24692 + 24598 + 16171
    + 15629 + 220598 + 40  =  1 255 401      delta 0
```

`bench.yml` was not opened. `_assert_js_closed` counts non-zero for every
bundle built: `_score_bridge.js` 45/11, `_inv_bridge.js` 23/11,
`_res_bridge.js` 14/6, `_tgt_bridge.js` 116/36, missing 0 in all.

### 14 — extremes, all seven attempted

| Extreme | Reading |
|---|---|
| symbol with no pre-rename leg | `ОТКЛОНЕНА: плеча до переименования нет`, symbol enters alone |
| cutover outside the archive's span on both sides | `ОТКЛОНЕНА: новой пары в архиве нет` |
| current month's monthly ZIP does not exist | normal case; daily refill closes it, tail 0, gaps 0 |
| top-up returns zero rows | `ok … · хвост не добран (HTTP 200)`, tail 16 h printed |
| mirror answers non-200 mid-fetch | `ok … · хвост не добран (HTTP 503)`, tail 16 h printed |
| arm with zero stop touches | `n_stop = 0 · Ω = nan`, bare `NaN` serialised, **no crash** |
| every spot symbol excluded by 2.6 | `СТОП: после исключений в кэше 1 монет … снято сверкой: unexplained 7 (AAA, DDD, EEE, GRAM, HHH, JJJ, SKY)` — no `Ω` |

Additionally, an interior gap that **survives** the top-up is named and the
existing 5 % rule still refuses it, unmoved:

```
CCC  CCCUSDT  2025-09-03T17  2026-09-05T16  8064 ч  хвост 0  дыр 1  744 ч
     2026-03-01T01 .. 2026-04-01T00   ДЫР 8.4% — пропуск
```

### 2.6 — the gate, end to end

```
СВЕРКА ПЕРЕД ЗАМЕРОМ: сверено монет 8 · исключено 0 · в рукава идёт 8
АРИФМЕТИКА ПЛАНКИ: допуск требует RR ≥ RR_MIN, значит 1/RR ≤ 0.50 на КАЖДОМ …
  Ω = 0.000  ДИ95 [0.000; 0.000]   ·   среднее 1/RR = 0.248
ИСКЛЮЧЕНО СВЕРКОЙ (--verify): нет
```

and with two symbols removed and the quorum down:

```
сетапов 124 · дат 38 · … · НИЖЕ КВОРУМА — Ω не печатается
ВЕРДИКТ: не выносится — ниже кворума; Ω и k* не печатаются
         снято сверкой: coverage 1 (AAA) · unexplained 1 (DDD)
k*: не печатается — продакшн-рукав этой стороны ниже кворума. снято сверкой: …
ИСКЛЮЧЕНО СВЕРКОЙ (--verify): 2
AAA      coverage
DDD      unexplained
```

## Deviations

1. **2.1's diagnosis is not the TZ's.** The TZ asks to «diagnose why the perp
   path does this and the spot path does not», presupposing two fetch paths.
   There was one. The divergence is a publication lag between the spot and the
   futures monthly archives, and the code defect is that the daily refill was
   scoped to `months[-1]`. The requirement «one code path serves both» is met
   and strengthened, and the repair does not depend on the lag being the
   permanent state of the archive.

2. **The perp tail top-up was repaired in the opposite direction from §5 item
   8's bar.** Perpetual series will now carry a visible tail deficit of roughly
   one archive day instead of a silent splice of spot candles. §5 item 8 states
   the top-up «has landed when no accepted coin carries a tail deficit above
   0.1 %», and a perp at ~24 h of 25 000 sits at about 0.09–0.10 %, on the bar
   or just over it. I did not reach for the number: hard floor item 2 forbids
   editing a bench to make it pass, and the only way to clear that bar for a
   perp is to keep splicing the wrong instrument.

3. **2.4's second half is not implemented and no threshold was typed.** By the
   TZ's own sentence — «the second half is void without the first» — and by
   inv. 49. `--verify` therefore still returns 0 on a planted `vol_ratio`
   deviation, which is validation item 10's third case and is reported as a
   failure above.

4. **2.6 excludes exactly the two classes the TZ names and no more.** A cached
   symbol that the live `coeffs.json` does not carry at all is never
   reconciled, so it is neither `clean` nor failed; I **named** it in the
   printed output and did **not** exclude it, because widening the gate is not
   authorised (contract §6). It is a gap and it is under `## Remaining Risks`.

5. **`verify_bench.py`'s v3 single-outlier assertions were re-registered.** Two
   `ok()` calls that asserted «a single outlier exits 0» now assert «a single
   unexplained outlier is red and named». This is the TZ's own class table and
   it makes the bench stricter, never laxer. The file's check count is held at
   35 so validation item 13's figure does not move; existing assertions were
   strengthened in place rather than new ones added, for the same reason.

## Pre-existing Issues

All fingerprint-gated files matched the TZ's table **exactly**, in both
directions, including `bench/backtest_bench.py` at 2768 lines /
`9357c2bc4e71542c21068be79f8691f9`. Nothing to report there.

1. **`.gitignore`'s bench-scratch comment is one bridge name short.** It
   enumerates `_tokens.js`, `_score_bridge.js`, `_inv_bridge.js`,
   `_res_bridge.js`, `_job.json`, `_out.json`, `_job2.json`, `_out2.json` and
   omits `_tgt_bridge.js`. The `bench/_*` pattern still covers it; only the
   comment is stale. Named in TZ §6; confirmed, not acted on.
2. **`bench/prot_bench.js:177` carries a raw Cyrillic literal**
   `src: 'мин30'`. Everything else in that file is `\uXXXX`-escaped. Named in
   TZ §6; confirmed, not acted on.
3. **`target_raw.json` can emit bare `NaN`.** Confirmed by construction: an arm
   with zero stop touches yields `Ω = nan`, `json.dump` writes bare `NaN`, and
   Python's own `json.loads` reads it back — but no other JSON parser will.
   Named in TZ §6; the run does not crash. Not acted on.
4. **`bench.yml` does not run `backtest_bench.py` at all**, so
   `_assert_js_closed` never fires in the gate and neither does anything else
   in this file. Every control this TZ added is exercised by the dispatched
   workflow or by the harness, never by the push gate. Named in TZ §6 as
   inv. 62's residual; confirmed.
5. **`--probe` from this session reads 200 on all five hosts**, including
   `api.binance.com` and `fapi.binance.com`, which answer 451 from a GitHub
   runner. This is inv. 52 exactly — reachability is a measurement and a rule
   resting on one falls with it. It changes nothing: hard floor item 9 bans
   those hosts from CI code, not from a session's own diagnosis, and no new
   code calls them.
6. **Environment, not repository:** this container has 955 MB of RAM and
   `direction_bench.py --sim` exhausts node's default heap. Every gate replay
   in this report used `NODE_OPTIONS=--max-old-space-size=4096`.

## Remaining Risks

1. **The runner has not executed any of this.** The census, the alias
   verdict for the real `GRAM` and `SKY`, the 31-of-31 line, the live
   classification and run #15 all need a dispatch of `backtest_bench.yml`.
   Everything above was proven against a synthetic archive.
2. **Nothing added by this TZ is inside `bench.yml`'s gate.** `bench.yml` may
   not be opened and no file may be created, so the census, the splice rule and
   the `--target` gate are locked only by validation-time controls and by the
   35 checks in `verify_bench.py`. A control outside the gate is not a control
   (inv. 37). Closing it needs either a new bench file wired into `bench.yml`
   or a raised gate figure — both outside this TZ.
3. **An unreconciled cached symbol still enters `--target`'s arms.** Deviation 4.
4. **`vol_ratio` has no threshold and now visibly says so.** Until the Architect
   decides what it should be compared against — its own construction suggests a
   turnover-basis lane beside `venue-basis`, not a propagated bound — the field
   is reference-only in a mode that gates `--target`.
5. **The class rule will make `--verify` red on ordinary source noise.** The v3
   licence that tolerated one outlier is gone by 2.5's table. That is the
   intended direction, and 2.6 keeps the pipeline running by removing the
   symbol rather than the run — but the first live dispatch should be read
   expecting red, with the class breakdown as the thing that matters.
6. **`map §3.14` Consequence 3 remains untested.** Its reconciliation on 25
   spot coins and its prediction for MORPHO and ARB cannot be checked without a
   run. Named in TZ §6.

## Commit

Two commits on `claude/tz-29-archive-coverage-and-verify-reconciliation`, both
pushed before this section was written, so their hashes are measurements:

- `8ab0a0e` — `fix(bench): archive coverage census, ticker alias splice, --verify classified and signed (TZ-29)`
  — `bench/backtest_bench.py`, `bench/verify_bench.py`.
- `6faf833` — `fix(bench): the census reports the best fetch attempt, and names a short leg as short (TZ-29)`
  — `bench/backtest_bench.py`.

This report's own commit carries the message
`docs(reports): TZ-29 — archive coverage census, derived splice rule, vol_ratio reconciled against its own construction (TZ-29)`
and nothing is stated about its outcome (inv. 54).

## Pull Request

**No pull request exists.** This session has no `gh` CLI and no GitHub API
token; `git` authenticates with an SSH deploy key, which pushes and cannot open
a pull request. Contract §8's fallback applies.

- Branch: `claude/tz-29-archive-coverage-and-verify-reconciliation`
- Compare: https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-29-archive-coverage-and-verify-reconciliation

**The Boss opens and merges from that link in one action, after the
Architect's verdict.**

## CI Execution

**No workflow result was read by this session, and none is forecast.**

What is established: the branch reached the remote (`8ab0a0e..6faf833`
accepted by `origin`), and the changed paths clear `bench.yml`'s filters —
that workflow triggers on `push` to `main` and `claude/**`, and its
`paths-ignore` list covers only `journal/data/**`, `journal/out/**`,
`journal/runs.jsonl`, `analyst/state.json`, `analyst/live.json`,
`analyst/log/**` and `**.md`, none of which matches `bench/*.py`.

`backtest_bench.yml` is `workflow_dispatch` only and **was not dispatched** —
this session has no credential to dispatch it. Validation items 8, 12 and the
live half of 9 have no runner reading, which is why the status is PARTIAL.

## Final Repository State

The branch `claude/tz-29-archive-coverage-and-verify-reconciliation`, pushed at
`6faf833`, carries `bench/backtest_bench.py` (3216 lines) and
`bench/verify_bench.py` (287 lines) and nothing else. The working tree is
clean: no `bench/_*`, no `__pycache__`, no `target_raw.json`, no cache
directory. No production file, workflow, contract or registry was opened.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Measured on the branch at `6faf833`.

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2065 | `f3da75f9dc1c62852c27a65f8b5052dc` |
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/backtest_bench.py` (before) | 2768 | `9357c2bc4e71542c21068be79f8691f9` |
| `bench/backtest_bench.py` (after) | 3216 | `1b921e88fdae5c1c404fbf9fbcee8b2c` |
| `bench/verify_bench.py` (before) | 254 | `877e91e3b5664158b81d7972cac79112` |
| `bench/verify_bench.py` (after) | 287 | `520777380f2ec69a3d05d792d78c7f78` |
| `.github/workflows/bench.yml` (untouched) | 135 | `ece76785638496963a2ea068d6a1b9df` |
| `.github/workflows/backtest_bench.yml` (untouched) | 140 | `8a994edb5be622d75196e2769c3cf45c` |

Map revision string, read from `## 0. Fingerprint` on `origin/main`:
**`**Revision 2026-09-05-a.**`** — required by the TZ, found in the map, all
seven content anchors matched as exact substrings, and every file in the map's
`## 0` table matched its stated line count and MD5.
