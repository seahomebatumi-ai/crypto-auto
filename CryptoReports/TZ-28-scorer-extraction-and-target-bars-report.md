# Implementation Report — TZ-28

## Status

COMPLETED. All three scopes executed; all twelve validation items run, all pass.

## Inbound Filing

None. `CryptoTZ/TZ-28-scorer-extraction-and-target-bars.md` arrived at its canonical
path in the Boss's upload commit `0e8da7a` and needed no move or rename.

```
$ git fetch origin
   d93cb2d..0e8da7a  main       -> origin/main
$ git ls-tree -r origin/main --name-only | grep -i 'TZ-2[5-9]'
CryptoReports/TZ-25-universe-morpho-arb-report-2.md
CryptoReports/TZ-25-universe-morpho-arb-report.md
CryptoReports/TZ-26-venue-count-expectations-report.md
CryptoReports/TZ-27-continuation-target-backtest-report.md
CryptoTZ/TZ-25-universe-morpho-arb.md
CryptoTZ/TZ-26-venue-count-expectations.md
CryptoTZ/TZ-27-continuation-target-backtest.md
CryptoTZ/TZ-28-scorer-extraction-and-target-bars.md
```

The session's working tree started at `d93cb2d` and was brought to `origin/main`
(`0e8da7a`) by fast-forward merge before any work; the TZ was not in the tree at start
and was not absent from the repository (contract §3).

### Previous TZ's branch (contract §8)

Merged. `claude/tz-27-continuation-target-backtest` is contained in `origin/main`:

```
$ git branch -a --merged origin/main | grep tz-27
+ claude/tz-27-continuation-target-backtest
  remotes/origin/claude/tz-27-continuation-target-backtest
$ git log --oneline -3 origin/main
0e8da7a Add files via upload
5c8d59f Merge pull request #25 from seahomebatumi-ai/claude/tz-27-continuation-target-backtest
d93cb2d docs(reports): TZ-27 — continuation-target backtest built, D2/D3 red as registered (TZ-27)
```

This work is therefore built on a merged base.

### System Map fingerprint gate (contract §5) — PASSED

Revision string required by the TZ header and found in the repository copy:
`**Revision 2026-09-03-b.**`. All seven content anchors matched as exact substrings
against `SYSTEM-MAP-CRYPTOCALCUL.md` on `origin/main` (2 occurrences each — the
fingerprint table plus the section itself):

```
2  <<**Revision 2026-09-03-b.**>>
2  <<### 3.12 Direction engine — veto cascade>>
2  <<### 3.15 Catalyst registry>>
2  <<### 3.16 List exhaustion — the day-range measure>>
2  <<## 11. Analytical engine>>
2  <<### 3.17 «РИСК ВЫНОСА» — the day's own risk>>
2  <<59. **A standing decision is amended in the floor before it is amended in the code.**>>
```

The map's `## 0` file table measured — all four match exactly (see `## Fingerprints`).
`bench/backtest_bench.py` on `origin/main` measured at the figure the TZ §0 states:
2544 lines, MD5 `fb9464afba2e87450bd3fd11877da9f1`. The map carries no row for that
file, so nothing in the table moves and the one-revision lag the TZ declares is not a
mismatch to block on.

## Scope Executed

**Branch TZ** (contract §8): the scope authorises one written file outside
`CryptoReports/**`, so the implementation goes on a branch and a pull request, and this
report goes straight to `main`.

- **Scope A — the extraction set and its closure check.** Done. A1 and A2 both.
- **Scope B — re-registration of D2 and D3 of `lab_selftest` section D.** Done. B1, B2
  and B3.
- **Scope C — the whole BTC record reaches `marketRegime`.** Done.

Nothing outside `bench/backtest_bench.py` was written. The three items TZ §4 leaves open
(`.gitignore`'s comment, `target_raw.json`'s bare `NaN`, `backtest_bench.yml`'s step
order) were not touched.

## Files Created

None.

## Files Modified

- `bench/backtest_bench.py` — 262 insertions, 38 deletions; 2544 → 2768 lines.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### Scope A1 — the extraction manifest

`JS_FUNCS` gains the two names production split out of `scoreCandidate`, in dependency
order:

```python
JS_FUNCS = ["has", "clamp01", "sigmaDay", "volRegime", "qualityScore",
            "scoreFinish", "scoreCandidate"]
```

`JS_VARS` is unchanged: the enlarged bundle reads `EFF_TREND`, `PACE_Z` and
`VOL_ABNORMAL` and no other constant, and the closure check below is what establishes
that rather than a reading.

### Scope A2 — one traversal, one closure check

Four functions, added before `extract_js`:

- **`_js_noise_span(s, i)`** — if `s[i]` opens a JS string literal or a comment, returns
  the index where that span ends, otherwise `None`. This is now the ONLY description in
  the file of how a string and a comment are traversed (inv. 20).
  `_skip_to_matching_brace` was rewritten to step with it and its own copy of the rules
  deleted; the docstring sentence that described those rules went with them.
- **`_strip_js_noise(src)`** — blanks every string literal and comment, preserving
  length and newlines, so a static scan cannot read an identifier out of prose.
- **`_js_defined(txt)`** — the names a piece of JS text declares: `function NAME(`,
  `var NAME` and every declared parameter of every function, anonymous included.
  DERIVED from the text, never typed.
- **`_assert_js_closed(bundle_src, driver_src, label)`** — raises `RuntimeError` naming
  the first identifier the bundle references that is defined neither in the bundle, nor
  in the driver, nor in `JS_GLOBALS`. Both halves run on stripped text: **called
  identifiers** (`(?<![.\w$])([A-Za-z_$][\w$]*)\s*\(` minus `JS_KEYWORDS`, so a method
  call and an `if (` are both out) and **constant reads**
  (`(?<![.\w$])([A-Z][A-Z0-9_]{2,})\b`). It counts what it compared and raises on zero
  identifiers examined (inv. 22), then prints the count.

The check runs at bundle-build time, before `node --check`, in both builders:
`extract_js` (the `JS_FUNCS` bundle, against `JS_DRIVER`) and `_extract_js_set` (the
`INV_JS_FUNCS`, `RES_JS_FUNCS` and `TARGET_JS_FUNCS` bundles, against their own
drivers). `JS_GLOBALS` is the literal list the TZ names and nothing more; it is the
check's only escape hatch and every entry on it is an identifier the check can no longer
catch, which is why it is short and commented as such.

The per-row `catch (e) { r = null; }` in every driver is untouched, as the TZ requires.

### Scope B1 — two registered constants

```python
TGT_H_LADDER = [1, 4, 8, 16, 32]   # multiples of H_NOISE, registered before data
TGT_MONO_MIN_PTS = 3               # fewest grid points a monotonicity claim needs
```

Declared once, beside `TGT_QUORUM_N`/`TGT_QUORUM_D`/`TGT_BOOT` (inv. 20, 23).

### Scope B2 — D2

New `_tgt_probe_rr(html)` builds ONE probe job and sends it through the same
`JsBridge(html, TARGET_JS_FUNCS, TARGET_JS_VARS, TARGET_DRIVER, "_tgt_bridge.js")` the
mode already uses: `E = 1`, `min30 = max30 = E` so `invalidationInfo`'s `dStruct` clamps
up to the `INV_FLOOR_SD` floor, `vol` immediately below `VOL_STOP` (both constants cut
from `index.html` with `_read_js_num`), and `subs = {k: E·exp(k·vol·√H_NOISE)}` over
`K_GRID`. It reads `g.rr` per grid point — `tradeGeometry` sets `rr` before it pushes
any veto — and calls a point **admittable** iff its probe `rr ≥ RR_MIN`, both numbers
production's own. The probe row is LONG because for the same `k` the long side dominates
the short (`exp(x) − 1 > 1 − exp(−x)`), so one row bounds both sides.

The measured admissible set reproduces the TZ §1 Fact 3 table to four decimals:
`k=1.0 rr 1.6169` (below `RR_MIN = 2.0`), then `2.6940`, `4.0023`, `5.5914`, `7.5214`.

- **D2a** — `n(k)` is zero on exactly the non-admittable grid points and non-zero on
  exactly the admittable ones, and non-decreasing across the grid.
- **D2b** — `Ω(k)` strictly decreasing across the grid points meeting `TGT_QUORUM_N`,
  with at least `TGT_MONO_MIN_PTS` such points; fewer is СТОП.

The printed line keeps its shape — the Ω chain and the per-point admitted counts — and
gains a probe line carrying `rr` and the admittable flag per grid point, so a reader
sees why a point is empty without running anything.

### Scope B3 — D3

`run_target` runs once per rung of `TGT_H_LADDER` with `k_grid=[]` and
`H_override = m · H_NOISE`, and the pooled `prod` arm is read off each. Three registered
conditions, none carrying a numeral about the outcome (inv. 49):

- **D3a** — `P_none` non-increasing across the ladder and `P_none(last) < P_none(first)`.
- **D3b** — the relative gap `|Ω − Σq/Σ(1−q)| / (Σq/Σ(1−q))` smaller at the last rung
  than at the first.
- **D3c** — at the rung with the smallest relative gap among rungs meeting quorum,
  `Σq/Σ(1−q)` lies inside `Ω`'s CI95 as the mode's own date resampling computes it, AND
  that rung's `P_none` is at or below the ladder's median `P_none`.

The whole ladder is printed, one line per rung with `n`, dates, quorum, `P_none`, `Ω`
with its CI, the closed form and the gap, then the three verdicts.

### Scope C — the whole BTC record

`run_target` now hands the bridge the whole `bcd` instead of a two-field literal, and
the comment above it is replaced with the reason: production passes `botData.btc`, i.e.
`coeffs.btc` entire; `leverageDecision` takes `volatility` off it and `marketRegime`
takes `r7` and `r14`, so a hand-built subset silences one reader to serve the other
(inv. 48). `reg` remains recorded and gates nothing — the only write is
`o = {..., "reg": r["reg"], ...}` at the observation, and a repository-wide search finds
no read of it in the target mode:

```
$ grep -n '\["reg"\]\|"reg":\|o\.get("reg"' bench/backtest_bench.py
598:        x["reg"] = reg.get(x["t"], (None,))[0]      ← run_regimes, unrelated mode
599:        n = {k: sum(1 for x in d if x["reg"] == k) ...  ← run_regimes
601: 613: 619:                                            ← run_regimes
2031:            o = {"sym": s, ..., "reg": r["reg"], ...}  ← the only target-mode write
```

### Language

Comments, docstrings, identifiers and this report are English (contract §Language). The
strings the bench PRINTS stay Russian, which is the map's own rule for on-screen text
(`## Language`: "English, except on-screen strings … quoted verbatim in Russian because
that is what the code prints") and the established form of every line in this file,
including everything TZ-27 added. TZ §2 B2/B3 require the printed line to keep its
existing shape, and an English verdict among `ОК`/`СТОП` lines would not.

## Validation

Baseline recorded first, on an untouched export of `origin/main` at `/tmp/tz28/baseline`
(`git archive origin/main`), MD5 of its `bench/backtest_bench.py` confirmed as
`fb9464afba2e87450bd3fd11877da9f1` before anything ran.

| # | Item | Result |
|---|---|---|
| 1 | `python3 -m py_compile bench/backtest_bench.py` | PASS — exit 0 |
| 2 | Baseline `--selftest` on unmodified `origin/main` | PASS — fails; `ReferenceError` frame and downstream `TypeError` quoted below |
| 3 | Closure check, silence, count printed and non-zero | PASS — four bundles, 45 / 23 / 14 / 116 occurrences, 0 missing |
| 4 | Closure check, known-answer control, both halves | PASS — both raise naming the removed identifier; restore is byte-identical |
| 5 | `--selftest --seeds 10` | PASS — exit 0, verdict and three world blocks quoted |
| 6 | `--lab-selftest` | PASS — exit 0, D1–D6 all ОК, section D quoted verbatim |
| 7 | Negative test: `_touch_calc` long/short branch inverted | PASS — D1, D2, D3, D6 all СТОП; D4, D5 do not fire; revert byte-identical |
| 8 | Scope C differ | PASS — 59 070 fields compared, 1440 differences, all in `reg` |
| 9 | Bridge smoke for `--run` and `--regimes` | PASS — `JsScorer` constructs, both sides finite |
| 10 | `bench.yml` gate | PASS — 13 steps, 1 255 401 checks, 0 failures, delta vs map = 0 |
| 11 | Production untouched | PASS — all four `md5sum` unchanged |
| 12 | Standing checks | PASS — `py_compile main.py` exit 0; `node --check` on the extracted `<script>` exit 0 |

## Test Results

### Item 2 — the baseline failure, in both of its frames

The swallowed exception, reproduced by re-running the baseline's own generated bridge
with the driver's `catch` printing instead of discarding (the bundle and the job file
are the ones the failed run wrote; only `console.error(e.stack)` was added, in a copy
under `/tmp`):

```
$ node /tmp/tz28/_probe_bridge.js _job.json /tmp/tz28/_probe_out.json
ReferenceError: scoreFinish is not defined
    at scoreCandidate (/tmp/tz28/_probe_bridge.js:58:5)
    at Object.<anonymous> (/tmp/tz28/_probe_bridge.js:70:15)
    ...
$ cat /tmp/tz28/_probe_out.json
[null,null]
```

Every row comes back `null` — which is exactly what the untouched driver produces, and
what the run then carries hundreds of lines downstream:

```
$ python3 backtest_bench.py --selftest --seeds 10 --html ../index.html --bot ../main.py
Т1 · вырезка кода: JS-мост собран, node --check пройден; блок бота разобран AST — ОК
Т2 · взгляд в будущее: запись на дату t из полного ряда и из обрезанного совпадает — ОК
Traceback (most recent call last):
  File "/tmp/tz28/baseline/bench/backtest_bench.py", line 2544, in <module>
    sys.exit(main() or 0)
  File "/tmp/tz28/baseline/bench/backtest_bench.py", line 2522, in main
    return selftest(a.html, a.bot, a.seeds)
  File "/tmp/tz28/baseline/bench/backtest_bench.py", line 1051, in selftest
    % (r[0], r[1], "ОК" if r[0] > r[1] else "СТОП"))
TypeError: '>' not supported between instances of 'NoneType' and 'NoneType'
EXIT=1
```

`Т1` prints ОК in that run: `node --check` passes on a bundle that is syntactically
valid and referentially broken. That is precisely the gap A2 closes.

### Item 3 — the closure check on all four bundles

```
$ python3 -c 'build all four bundles'
  замкнутость _score_bridge.js: сверено 45 обращений, 11 имён, пропущенных 0
  замкнутость _stops_bridge.js: сверено 23 обращений, 11 имён, пропущенных 0
  замкнутость _res_bridge.js: сверено 14 обращений, 6 имён, пропущенных 0
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
```

Four bundles, 198 identifier occurrences examined in total, none of them zero, none
missing.

### Item 4 — the known-answer control, both halves

```
pre-control bundle: 5882 bytes, md5 22b0dc3c805c92049550f6f2ff468bf0
CONTROL 1 raised: замкнутость _score_bridge.js: связка ссылается на scoreFinish, а
  определения нет ни в ней, ни в драйвере — вырезка отстала от продакшна (инв. 20)
  names scoreFinish: True
CONTROL 2 raised: замкнутость _score_bridge.js: связка ссылается на VOL_ABNORMAL, а
  определения нет ни в ней, ни в драйвере — вырезка отстала от продакшна (инв. 20)
  names VOL_ABNORMAL: True
restored bundle: 5882 bytes, md5 22b0dc3c805c92049550f6f2ff468bf0
byte-identical to pre-control: True
```

Removing `scoreFinish` from `JS_FUNCS` exercises the called-identifier half; removing
`VOL_ABNORMAL` from `JS_VARS` exercises the constant-read half. Restoring both is silent
and rebuilds the same 5882 bytes (inv. 45).

### Item 5 — `--selftest --seeds 10`, repaired

Exit 0. The bridge that returned a column of nulls now returns scores:

```
  замкнутость _score_bridge.js: сверено 45 обращений, 11 имён, пропущенных 0
Т1 · вырезка кода: JS-мост собран, node --check пройден; блок бота разобран AST — ОК
Т2 · взгляд в будущее: запись на дату t из полного ряда и из обрезанного совпадает — ОК
Т3 · монотонность: у минимума 79.3 · у максимума 37.3 — ОК

МИР «noise»  (эталонный фактор обязан дать «0»), посевов 10
  эталон «близость к мин90»  IC = +0.000 ± 0.030   нужный знак 10/10
  перемешанный счёт (нуль)   IC = +0.006 ± 0.029
  scoreCandidate целиком     IC = +0.017 ± 0.024
  он же без двух штрафов     IC = +0.008 ± 0.026

МИР «revert»  (эталонный фактор обязан дать «+»), посевов 10
  эталон «близость к мин90»  IC = +0.252 ± 0.030   нужный знак 10/10
  перемешанный счёт (нуль)   IC = +0.009 ± 0.027
  scoreCandidate целиком     IC = -0.060 ± 0.017
  он же без двух штрафов     IC = +0.096 ± 0.022

МИР «trend»  (эталонный фактор обязан дать «−»), посевов 10
  эталон «близость к мин90»  IC = -0.242 ± 0.038   нужный знак 10/10
  перемешанный счёт (нуль)   IC = +0.003 ± 0.036
  scoreCandidate целиком     IC = +0.003 ± 0.030
  он же без двух штрафов     IC = -0.162 ± 0.043

══════════════════════════════════════════════════════════════
ИТОГ САМОПРОВЕРКИ
══════════════════════════════════════════════════════════════
нулевой мир не даёт ложного сигнала: ДА
миры со знаком распознаются верно:   ДА
мощность: SE(IC) ≈ 0.030 при 39 датах → отличим |IC| ≳ 0.060
ВЕРДИКТ СТЕНДА: измеряет то, что должен
```

`Т3` and the three world blocks did not exist in the baseline run at all: it died before
reaching them.

### Item 6 — `--lab-selftest`, section D verbatim

Exit 0, whole-lab verdict green. Section D exactly as printed, closure lines included:

```
D · --target
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  D1 калибровка цели, k=1.5: 0.93 [0.69; 1.16] ОК
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  D2 монотонность Ω(k) на точках с кворумом: 0.287 > 0.121 > 0.055 > 0.018 ОК
     допущено на точку сетки: k=1.0 n=0 · k=1.5 n=346 · k=2.0 n=823 · k=2.5 n=977 · k=3.0 n=1113
     зонд продакшн-геометрии (пол инвалидации, vol у VOL_STOP): k=1.0 rr 1.6169 НЕДОСТИЖИМА · k=1.5 rr 2.6940 допустима · k=2.0 rr 4.0023 допустима · k=2.5 rr 5.5914 допустима · k=3.0 rr 7.5214 допустима
     D2a пустота совпадает с недостижимостью, заполнение не убывает: ОК · D2b точек с кворумом 4 (нужно 3): ОК
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  D3 предельный переход, лестница H = m×168ч:
    m=1   H=168   n=981   дат 82   кворум       P(никуда) 0.639 · Ω 0.026 [0.011; 0.047] · Σq/Σ(1−q) 0.248 · разрыв 89.5%
    m=4   H=672   n=946   дат 79   кворум       P(никуда) 0.304 · Ω 0.146 [0.116; 0.180] · Σq/Σ(1−q) 0.248 · разрыв 41.1%
    m=8   H=1344  n=895   дат 75   кворум       P(никуда) 0.154 · Ω 0.213 [0.176; 0.254] · Σq/Σ(1−q) 0.249 · разрыв 14.5%
    m=16  H=2688  n=811   дат 67   кворум       P(никуда) 0.055 · Ω 0.250 [0.211; 0.289] · Σq/Σ(1−q) 0.250 · разрыв 0.0%
    m=32  H=5376  n=622   дат 51   кворум       P(никуда) 0.000 · Ω 0.293 [0.245; 0.340] · Σq/Σ(1−q) 0.250 · разрыв 17.2%
     D3a уход затухает: P(никуда) 0.639 → 0.304 → 0.154 → 0.055 → 0.000 ОК
     D3b сближение с замкнутой формой: разрыв 89.5% → 17.2% ОК
     D3c предел там, где уход затух: наименьший разрыв на m=16 · Σq/Σ(1−q) 0.250 внутри ДИ95 Ω [0.211; 0.289] · P(никуда) 0.055 против медианы 0.154 ОК
  D4 тождественный дифф: сравнений 7848, расхождений 0 ОК
  замкнутость _tgt_bridge.js: сверено 116 обращений, 36 имён, пропущенных 0
  D5 взгляд в будущее: запись на полном ряде против обрезанного на t+H — совпала ОК
  D6 обмен сторон: Ω лонг 0.037 · Ω шорт 0.013 ОК

ВЕРДИКТ ЛАБОРАТОРИИ: измеряет то, что должна
```

Two readings the ladder makes visible and the single rung could not:

1. The measured limit is `Σq/Σ(1−q) ≈ 0.25` and `Ω` walks up to it monotonically —
   0.026 → 0.146 → 0.213 → 0.250 → 0.293 — while escape decays 0.639 → 0.000. The
   two-barrier property is what the section now asserts, and it holds.
2. The old bar's single rung, `8 × H_NOISE`, is a rung where `P_none` is still 0.154 and
   the gap is still 14.5 %. Its `P_none < 0.05` clause was unreachable there in the
   direction the TZ says: 0.154 is more than triple the numeral. The rung that reaches
   the limit is `m = 16`, and no numeral in the new rule names it — D3c finds it.

Baseline for comparison, same command on `origin/main` (whole-lab verdict red, exit 1):

```
  D1 калибровка цели, k=1.5: 0.93 [0.69; 1.16] ОК
  D2 монотонность Ω(k): nan > 0.287 > 0.121 > 0.055 > 0.018 СТОП
     допущено на точку сетки: k=1.0 n=0 · k=1.5 n=346 · k=2.0 n=823 · k=2.5 n=977 · k=3.0 n=1113
  D3 тождество на 8×168ч: P(никуда) 0.154 · Ω 0.213 против Σq/Σ(1−q) 0.249 СТОП
  D4 тождественный дифф: сравнений 7848, расхождений 0 ОК
  D5 взгляд в будущее: запись на полном ряде против обрезанного на t+H — совпала ОК
  D6 обмен сторон: Ω лонг 0.037 · Ω шорт 0.013 ОК

ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить
```

D1, D4, D5 and D6 print identical numbers before and after, which is the check that
Scope B moved D2 and D3 and nothing else. `n(k)` per grid point is identical too: the
re-registration changed the BAR, not the measurement.

### Item 7 — the negative test, the acceptance criterion for Scope B

The long/short branch of `_touch_calc` was inverted in the working tree:

```python
     if is_long:
-        t_hit, s_hit = seg_hi >= tgt, seg_lo <= stop
+        t_hit, s_hit = seg_lo <= tgt, seg_hi >= stop
     else:
-        t_hit, s_hit = seg_lo <= tgt, seg_hi >= stop
+        t_hit, s_hit = seg_hi >= tgt, seg_lo <= stop
```

`--lab-selftest` under the inversion, exit 1, section D:

```
D · --target
  D1 калибровка цели, k=1.5: 7.48 [7.48; 7.48] СТОП
  D2 монотонность Ω(k) на точках с кворумом: nan > nan > nan > nan СТОП
     допущено на точку сетки: k=1.0 n=0 · k=1.5 n=346 · k=2.0 n=823 · k=2.5 n=977 · k=3.0 n=1113
     зонд продакшн-геометрии (пол инвалидации, vol у VOL_STOP): k=1.0 rr 1.6169 НЕДОСТИЖИМА · k=1.5 rr 2.6940 допустима · k=2.0 rr 4.0023 допустима · k=2.5 rr 5.5914 допустима · k=3.0 rr 7.5214 допустима
     D2a пустота совпадает с недостижимостью, заполнение не убывает: ОК · D2b точек с кворумом 4 (нужно 3): СТОП
  D3 предельный переход, лестница H = m×168ч:
    m=1   H=168   n=981   дат 82   кворум       P(никуда) 0.000 · Ω — · Σq/Σ(1−q) 0.248 · разрыв —
    m=4   H=672   n=946   дат 79   кворум       P(никуда) 0.000 · Ω — · Σq/Σ(1−q) 0.248 · разрыв —
    m=8   H=1344  n=895   дат 75   кворум       P(никуда) 0.000 · Ω — · Σq/Σ(1−q) 0.249 · разрыв —
    m=16  H=2688  n=811   дат 67   кворум       P(никуда) 0.000 · Ω — · Σq/Σ(1−q) 0.250 · разрыв —
    m=32  H=5376  n=622   дат 51   кворум       P(никуда) 0.000 · Ω — · Σq/Σ(1−q) 0.250 · разрыв —
     D3a уход затухает: P(никуда) 0.000 → 0.000 → 0.000 → 0.000 → 0.000 СТОП
     D3b сближение с замкнутой формой: разрыв — → — СТОП
     D3c предел там, где уход затух: рунгов с кворумом нет СТОП
  D4 тождественный дифф: сравнений 7848, расхождений 0 ОК
  D5 взгляд в будущее: запись на полном ряде против обрезанного на t+H — совпала ОК
  D6 обмен сторон: Ω лонг nan · Ω шорт nan СТОП

ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить
```

**D1, D2, D3 and D6 all turn СТОП.** D4 and D5 correctly do not fire: the identity diff
compares two arms resolved by the same inverted function, and the truncation check
compares two records produced by it. This is the point of the item — under the bars being
replaced, D2 and D3 were red BEFORE the inversion and the inversion changed nothing about
them, so section D could not tell a broken resolver from a healthy one on those two rows.
It now can.

Every sub-clause fires for its own reason and the ladder shows why: with the resolver
inverted, no arm ever records a target touch, `P_none` collapses to 0.000 at every rung
(the stop is always hit first), `Ω` is undefined everywhere, and the quorum-bearing rung
set that D3c needs is empty.

Revert and re-run:

```
$ cp /tmp/tz28/backtest_bench.py.keep bench/backtest_bench.py
$ md5sum bench/backtest_bench.py
9357c2bc4e71542c21068be79f8691f9  bench/backtest_bench.py
$ git status --porcelain
 M bench/backtest_bench.py
$ diff /tmp/tz28/lab_after.out /tmp/tz28/lab_revert.out && echo "BYTE-IDENTICAL"
BYTE-IDENTICAL
$ md5sum /tmp/tz28/lab_after.out /tmp/tz28/lab_revert.out
a0507b52136ac8e924841136e9fbeae0  /tmp/tz28/lab_after.out
a0507b52136ac8e924841136e9fbeae0  /tmp/tz28/lab_revert.out
```

The output after the revert is byte-identical to the run before the test, and the tree
carries the one intended modification and nothing else.

### Item 8 — Scope C differ

`run_target` on one seeded world (`synth_hl("normal")`, seed 3, BTC popped as the regime
meter — the same world section D uses), `k_grid=K_GRID`, `want_identity=True`, run once
before the `btc_stats` change and once after, records compared field by field:

```
dates 82 · observations 2460
fields compared: 59070 · differences: 1440
differing fields: {'reg': 1440}
reg distribution BEFORE (subset btcStats): {'range': 2460}
reg distribution AFTER  (whole bcd):       {'trend': 1320, 'range': 1020, 'stress': 120}
differences outside `reg`: 0
```

59 070 comparisons, non-zero as inv. 22 requires: the date stamp, then `sym`, `side`,
`reg`, `rr`, `tgtSig`, `adm` and the arm key set per observation, then `first`, `hit`,
`p`, `rr`, `tgtSig`, `a`, `b`, `R` for every arm of every observation. Every difference
is in `reg` and there are 1440 of them — 1440 of 2460 observations change label.

The distribution is the finding the TZ predicted, measured: with the two-field literal
the recorded regime is `range` on **100 %** of observations — degenerate by
construction, because `marketRegime` reads `r7` and `r14` and the subset carried
neither. With the whole record it reads `trend` 1320, `range` 1020, `stress` 120. The
label can now say `trend`, and a later reader grouping by it would be grouping on
something.

### Item 9 — bridge smoke for `--run` and `--regimes`

```
  замкнутость _score_bridge.js: сверено 45 обращений, 11 имён, пропущенных 0
JsScorer constructed: .../bench/_score_bridge.js
scores: long 43.29554969340076 · short 45.386571385147825
both sides finite: True
```

### Item 10 — the `bench.yml` gate

All 13 steps run locally with `NODE_OPTIONS=--max-old-space-size=4096` set
preemptively, per the TZ's note about step 5 and the node heap ceiling this VPS carries
(map §10). No step reported heap exhaustion and none reported a failure; whether any of
them would have needed the raise was not measured, because the raise was already in
place:

| Step | Bench | Checks | Fails | rc |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 0 | 0 |
| 2 | `board2_bench.js` | 130 | 0 | 0 |
| 3 | `prot_bench.js` | 372 | 0 | 0 |
| 4 | `verify_bench.py` | 35 | 0 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 0 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 0 | 0 |
| 7 | `journal_bench.js` | 693 895 | 0 | 0 |
| 8 | `catalyst_bench.js` | 24 692 | 0 | 0 |
| 9 | `display_bench.py` | 24 598 | 0 | 0 |
| 10 | `render_bench.py` | 16 171 | 0 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 0 | 0 |
| 12 | `exhaustion_bench.js` | 220 598 | 0 | 0 |
| 13 | `live-gate.sh --selftest` | 40 | 0 | 0 |
| | **TOTAL** | **1 255 401** | **0** | |

**13 steps, 1 255 401 checks, 0 failures. Delta against the map's figure = 0.** Step 4,
`verify_bench.py`, imports `backtest_bench` at module scope and passed, which is the
gate's proof that this file still imports cleanly. This is a LOCAL replay of the gate's
steps, not a runner execution — see `## CI Execution`.

### Item 11 — production untouched

```
dd39536d18cc1feb4839808e41e7bff4  index.html
0e3ead8c300d2ee6783303c4bf2fb6b5  main.py
f9b2dd4a3594134b2b7b603de19075c3  catalysts.json
3b8730b254467c9df4c0a845a0f3cfb3  bench/exhaustion-calibration.txt
```

All four identical to the map's `## 0` table. `git diff --stat` against `origin/main`
names one file:

```
 bench/backtest_bench.py | 300 ++++++++++++++++++++++++++++++++++++++++++------
 1 file changed, 262 insertions(+), 38 deletions(-)
```

Hard floor item 1 is untouched by construction: no production JS changed, and Scope C
changes what the BENCH feeds production functions, not the arithmetic inside them.

### Item 12 — standing checks

```
$ python3 -m py_compile main.py                 → exit 0
$ node --check <script block from index.html>   → exit 0   (1 block, 193 429 bytes)
```

### Wall-clock cost of `--lab-selftest`

| | Real | User | Sys |
|---|---|---|---|
| Before (`origin/main`) | 1 m 45.8 s | 1 m 35.8 s | 5.8 s |
| After | 2 m 05.2 s | 1 m 53.2 s | 7.5 s |

**+19.4 s, +18 %**, on a single-core VPS (`nproc` = 1). Section D grew from three
`run_target` calls to seven exactly as the TZ states, and the growth is sublinear in that
count because the ladder's long rungs walk fewer dates (82 at `m = 1` down to 51 at
`m = 32`). Two minutes is not past a working length, so there is nothing to report as a
finding here.

## Deviations

None. Every item of Scopes A, B and C was implemented as written, and every validation
item was run.

Two implementation choices worth naming, neither a deviation:

- **The closure line prints on every bundle build, not once per bundle per process.**
  TZ §3 item 3 requires the count per bundle to be printed; a mode that builds a bridge
  more than once therefore prints the line more than once (six `_res_bridge.js` lines in
  section B, six `_tgt_bridge.js` lines in section D). Deduplicating would have been a
  judgement call about how much evidence to suppress, and the check runs on every build
  regardless.
- **`_extract_js_set` passes its `bridge_name` as the check's `label`.** The four bundles
  are then identified in the output by the four bridge file names, which are unique and
  already the file's own vocabulary; no new parameter was threaded through three call
  sites to carry a second name for the same thing.

## Pre-existing Issues

1. **`_skip_to_matching_brace` mishandled an unterminated block comment, and the
   factoring had to fix it.** On `origin/main` the branch reads
   `i = s.find("*/", i + 2) + 2`, and `str.find` returns `-1` when there is no closing
   `*/`, so the scanner would jump to index 1 and rescan the file from the top. TZ §2 A2
   requires exactly one description of how a string and a comment are traversed, shared
   by `_skip_to_matching_brace` and `_strip_js_noise`; a shared description that rewinds
   would make `_strip_js_noise` loop rather than terminate, so `_js_noise_span` returns
   the end of the text instead. Recorded because it is a behaviour change in an error
   path that pre-existed this TZ — it is unreachable on any well-formed `index.html`,
   and it is not a fix the TZ asked for. Direction: the old code could loop, the new
   code stops.
2. **`np.nanpercentile` emits `RuntimeWarning: All-NaN slice encountered` from
   `_arm_pool`'s bootstrap when an arm resolves no touches at all.** Pre-existing and
   only observable under a broken resolver — it appeared four times on stderr during the
   negative test and never in a healthy run. It does not change any verdict, and it is
   not in scope.
3. The two items TZ §4 leaves deliberately open — `.gitignore`'s explanatory comment
   being one bridge name short (`bench/_tgt_bridge.js`, covered by the `bench/_*` rule
   itself) and `target_raw.json` carrying bare `NaN` where a pooled arm records zero stop
   touches — were confirmed still present and not touched.
4. The map's `## 0` block is one revision behind the code, as TZ §0 states: it has no row
   for `bench/backtest_bench.py`, so this change moves no fingerprint in that table. The
   TZ notes one map revision covers TZ-27 and TZ-28 together, after this merge. Reported,
   not acted on.

## Remaining Risks

1. **The closure check is a static scan and recognises three declaration forms**:
   `function NAME(`, `var NAME` and declared parameters. A name introduced by a comma
   declarator (`var a = 1, b = 2;`) would not be collected, so if such a name were also
   CALLED or read as an `UPPER_SNAKE` constant inside a bundle, the check would raise on
   a name that is in fact defined. That is a loud build-time failure naming the
   identifier, never a silent pass — the safe direction, and the same direction the whole
   check exists to enforce — but a future refactor could trip it. No such name exists in
   any of the four bundles today.
2. **Computed member access and dynamically built identifiers are invisible to the
   scan.** `obj[name]()` is not a `name(` occurrence, and neither is a name assembled at
   runtime. The check bounds the reference class it names — the class the TZ-27 defect
   belonged to — and nothing wider.
3. **D3b compares the first rung to the last, and the ladder overshoots at the last.**
   The measured gap runs 89.5 % → 41.1 % → 14.5 % → **0.0 %** → 17.2 %: convergence is
   reached at `m = 16` and the final rung walks back out as its sample thins (622 setups
   over 51 dates versus 981 over 82). D3b holds comfortably here — 17.2 % is far below
   89.5 % — but on a shorter history a last rung whose sample collapses could fail a bar
   that the ladder as a whole satisfies. The bar is the Architect's as registered; this
   records the property rather than proposing a change, and D3c is what actually locates
   the limit (it selects `m = 16`, not `m = 32`).
4. **The lab is 18 % slower** (see the table above). Nothing here is a finding yet; it is
   the number the next TZ would need if section D grows again.

## Commit

One implementation commit on the branch, message verbatim from TZ §5:

```
fix(bench): close the JS extraction set, re-register D2/D3, full BTC cd to marketRegime (TZ-28)
```

Contents: `bench/backtest_bench.py` only — 262 insertions, 38 deletions. Commit
`b29284e`, made and pushed before this report was written.

The report's own commit is authorised to carry one message and this section states it
and stops — no hash, no conclusion, no push result (inv. 54):

```
docs(reports): TZ-28 — extraction set closed, D2/D3 re-registered, whole BTC cd to marketRegime (TZ-28)
```

## Pull Request

**No pull request exists.** This session has no `gh` CLI and no GitHub token
(`which gh` → not found; `GITHUB_TOKEN` and `GH_TOKEN` both unset), so it cannot open
one; contract §8's fallback applies.

- Branch: `claude/tz-28-scorer-extraction-and-target-bars` (pushed; upstream set)
- Compare URL:
  `https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-28-scorer-extraction-and-target-bars`

The Boss opens and merges from that link in one action, after the Architect's verdict.

## CI Execution

**No workflow result was read by this session** — there is no `gh` and no credential to
read one with, so no runner conclusion is claimed in either direction. What is
established:

- The branch reached the remote: `* [new branch] claude/tz-28-scorer-extraction-and-target-bars`.
- The changed path clears `bench.yml`'s filters, read from the workflow rather than
  assumed: its `push` trigger is `branches: [ main, 'claude/**' ]`, which this branch
  name matches, and its `paths-ignore` lists only `journal/data/**`, `journal/out/**`,
  `journal/runs.jsonl`, `analyst/state.json`, `analyst/live.json`, `analyst/log/**` and
  `**.md` — none of which matches `bench/backtest_bench.py`.
- The whole 13-step gate was replayed LOCALLY, on this VPS, with the results in item 10
  above. A local replay of CI semantics is not a runner execution, and the hosted result
  is read by the audit, not by this report.

The two facts contract §8 requires verified before a direct push to `main` were read from
the workflow, not assumed:

- `.github/workflows/main.yml`'s `push` trigger is still a `paths` ALLOW-LIST of exactly
  two literal entries — `main.py` and `.github/workflows/main.yml`. `CryptoReports/**` is
  unnamed and therefore cannot start the bot. (The one textual occurrence of
  `paths-ignore` in that file is inside a comment explaining why the allow-list replaced
  it.)
- GitHub Pages serves the calculator from `index.html`, so nothing under
  `CryptoReports/**` can reach the live calculator.

## Final Repository State

The session leaves behind the branch `claude/tz-28-scorer-extraction-and-target-bars`,
pushed to `origin` at commit `b29284e`, one commit ahead of `origin/main` (`0e8da7a`).
It carries exactly one changed file, `bench/backtest_bench.py` (2768 lines, MD5
`9357c2bc4e71542c21068be79f8691f9`), and the working tree is clean: the generated
bridges and job files under `bench/_*` are covered by `.gitignore` and none is staged or
committed.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Map, at the revision this TZ requires:

| File | Revision string | Lines | MD5 |
|---|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | `**Revision 2026-09-03-b.**` | 1915 | `0b49f7935e9fa098c13c9886d06f7d1b` |

Every file the map's `## 0` table lists, measured on the branch:

| File | Lines | MD5 | Map's figure | Match |
|---|---:|---|---|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` | 3736 / `dd39536d18cc1feb4839808e41e7bff4` | yes |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 / `0e3ead8c300d2ee6783303c4bf2fb6b5` | yes |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | yes |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | yes |

The file the TZ's own §0 adds, before and after:

| File | Lines | MD5 | |
|---|---:|---|---|
| `bench/backtest_bench.py` on `origin/main` | 2544 | `fb9464afba2e87450bd3fd11877da9f1` | matches TZ §0 |
| `bench/backtest_bench.py` on this branch | 2768 | `9357c2bc4e71542c21068be79f8691f9` | this change |

Governing text, measured for the audit's stale-copy comparison:

| File | Lines | MD5 |
|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` | 801 | `a6ebc2e7c2f2b74e813dfdc20400558f` |
| `ANALYST-INSTRUCTIONS.md` | 2226 | `5b9cd784b6015cf113f4ace054126e0d` |

`EXECUTOR-INSTRUCTIONS.md` is v19 at 801 lines and MD5 `a6ebc2e7c2f2b74e813dfdc20400558f`,
which is the figure the map's `## 0` block quotes for it.
