# TZ-34 — Census the perpetual archive before anything switches to it, and repair the crash that ate the regime-gate raw file

**Canonical filename: `TZ-34-futures-archive-census.md`.** File the artifact under this
name in `CryptoTZ/`, whatever name it arrived under (contract §3).

**Executor model: Opus.** The new mode runs beside a three-year cache that costs a full
re-download to rebuild, and its whole correctness claim is that it writes nothing. A mode
that touches `bench/cache/` by accident is a data-loss event, and that is the risk this
model choice is buying against.

**This TZ takes a measurement and changes no policy.** Nothing here switches a venue,
moves a threshold or re-runs a study. It exists because the next TZ cannot be written
honestly without a reading that only a runner can take.

---

## 0. Fingerprint gate — blocking (contract §5)

Required map revision and every content anchor, quoted in full from
`SYSTEM-MAP-CRYPTOCALCUL.md` `## 0. Fingerprint`. Match each as an exact substring
against the repository copy on `origin/main` after fetching. Any mismatch → BLOCKED
before any work.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-06-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `65. **A bar derived from the constant it judges moves with it.**` |

The map's `## 0` file table at this revision — measure each, report each, act on no
difference (contract §5):

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**`bench/backtest_bench.py` figure, stated here as the map's `## 0` requires of any TZ
that needs it: 3703 lines, MD5 `4d4242d37e63a01bdf74c474b3cfcb02`.** The map's prose
still carries TZ-30's 3240 / `d2dad0f80afa2c191c2faf1d40081a88`. Known map staleness, not
a gate failure — the file is not in the fingerprint table. Record the measured figure
under `## Pre-existing Issues` and do not act on the difference.

**If TZ-33 is already merged, `index.html` and `bench/backtest_bench.py` will both be
ahead of these figures.** Report the measured values and continue; this TZ touches
neither the direction engine nor the target driver, so the two do not collide.

---

## 1. Why

### 1.1 The bench measures spot and the Boss trades perpetuals

`bench/backtest_bench.py:1115`, inside `fetch_prices`:

```
for is_fut in ((True,) if fut else (False, True)):
```

with the loop breaking at `len(rows) >= 2600` and `best` keeping the **longest** leg. So
a coin without `fut:true` is fetched from `data/spot` first and, once its spot leg clears
the history bar, the futures leg is never requested at all. The declared set is five —
`ARB`, `HYPE`, `LIT`, `MORPHO`, `XMR` — so **26 of the 31 cached symbols are Binance spot
series**, and every Ω, every stop touch, every first-touch resolution and every
reconciliation cell in the standing results was measured on them.

That is a source property with three known consequences and one unknown, and the unknown
is why this TZ is a census rather than a switch:

- **Known — the tail.** Map inv. 64: `data-api.binance.vision` carries a spot klines
  endpoint and no futures one (measured 05.09.2026, `/fapi/v1/klines` → 404), and
  `fapi.binance.com` is banned from CI by inv. 24 and by hard floor item 9. A perpetual
  series therefore ends at the archive's last daily file and cannot be topped up. Today
  five symbols carry ~20 h of tail deficit; on a perpetual archive all 31 would.
- **Known — the reconciliation's basis licence.** `reconcile` grants `venue-basis` on
  `sym in fut`, a declaration read from `tokens[]`. On a perpetual archive twenty-five
  more symbols acquire exactly the same perp-versus-composite mismatch while the licence
  still names five, so they would class `unexplained`, `target_gate` would strip them
  from the arms, and the switch would present as «the bench broke». **That coupling is
  the next TZ's and is named here so it is not discovered by paying for it.**
- **Known — the splice.** `ALIAS` carries `GRAMUSDT → TONUSDT` and `SKYUSDT → MKRUSDT`,
  and `_splice` judges each joint against the hourly extremes of the two legs
  themselves. Those verdicts — TON→GRAM admitted, MKR→SKY refused (map inv. 63) — are
  readings taken on the **spot** legs. They do not carry across to `futures/um` and must
  be re-taken there.
- **Unknown — how much history exists.** A Binance perpetual is listed after its spot
  pair, so each futures leg starts later, and `_save` refuses a series under 2600 hours
  or with more than 5 % holes. **Nobody has measured, per symbol, what the futures leg
  actually returns.** A switch written against a guess about a third party's archive is
  exactly what map inv. 52 and inv. 44 refuse.

### 1.2 The funding archive already exists and the measurement that needed it did not read it

`fetch_funding` pulls
`https://data.binance.vision/data/futures/um/monthly/fundingRate/<PAIR>/<PAIR>-fundingRate-<YYYY-MM>.zip`
for every token in `tokens[]`, three years, caching to `bench/cache/_fund_<SYM>.json`;
`load_funding()` reads them and `--funding` consumes them.

Meanwhile `--regime-gate` prints `f*` under its own header line:

> `f* — постоянная восьмичасовая ставка, съедающая преимущество ячейки над опорной`
> `(168ч / RR 2.0) ровно; фандинг в архиве не лежит и заряжается арифметикой (§3.4).`

**The second clause is false about this repository.** The funding is in the archive; it
is not in that arm. One quantity with two treatments is what map inv. 21 and inv. 38 ban,
and this is the perpetual's whole distinguishing economics being charged as an algebraic
break-even instead of being read. **The repair belongs with the venue switch, not here**,
because charging realised funding onto a spot kline series would be a third reading of
the wrong instrument. It is recorded so the next TZ carries it.

### 1.3 The regime-gate run crashed after printing its verdict

`bench/backtest_bench.py:2844`, inside `_rg_agree`, keys the agreement table by a tuple:

```
cell[(_rg_word(d), w2[0] if w2 else "нет метки")] = ...
```

`main()` at line 3630 then does `json.dump(sm, ...)`, which refuses a non-scalar dict
key. The observed failure:

```
File ".../bench/backtest_bench.py", line 3630, in main
  json.dump(sm, open(os.path.join(HERE, "regime_gate_raw.json"), "w"))
TypeError: keys must be str, int, float, bool or None, not tuple
```

`report_regime_gate(sm)` runs at 3629, one line earlier, so the verdict reached stdout
and **`regime_gate_raw.json` was never written and the step exited non-zero.** The raw
data behind a completed three-year measurement does not exist, and a re-dispatch
reproduces the crash rather than recovering it. `out["cells"]` in the same function
already keys by the string `"%d|%.1f|%s|%s"`; the agreement table is the one place that
did not follow it.

---

## 2. Scope

Three scopes, independent in the sense of contract §6.

### A · `bench/backtest_bench.py` — a new read-only mode `--venue-census`

**Read-only is the whole specification and it is asserted, not promised.** The mode
writes nothing under `bench/cache/`, creates no `<SYM>.json`, replaces no file and
removes none. It prints a table and returns an exit code.

For **every symbol in `tokens[]` plus BTC**, request both legs through the existing
`_vision_rows` — the same function, both values of `is_fut`, no second fetch path
(map inv. 21, inv. 20) — and print one line per symbol per leg carrying:

- the first and last hour the leg returns, and the first month that answered 200 (the
  pre-listing window `_vision_rows` already reads off the data);
- total hours, interior gap count, interior hours missing, largest gap with its own start
  and end, and tail deficit to the last complete hour — the quantities `census` already
  computes, called on the leg's own bucket dict;
- whether the leg would clear `_save`'s own bars, **read from `_save` rather than
  restated** (map inv. 65): under 2600 hours, or holes above 5 %, is a refusal, and the
  line says which bar it failed;
- for the two `ALIAS` symbols, `_splice`'s verdict **on that leg**, with the joint
  return, the leg extremes and the pair count it compared — the existing printout, run on
  the futures leg for the first time.

Then a summary the next TZ is written against: how many symbols have a usable futures
leg, how many hours the list loses in total and per symbol against its spot leg, and
which symbols would be refused outright.

**Count what was compared and fail on zero** (map inv. 22). A census that fetched nothing
must exit non-zero rather than print an empty table.

**Names the venue in its own output.** Every line states which archive root it read, so
the artifact cannot be misread later as a statement about the other leg.

### B · `bench/backtest_bench.py` — the crash

The agreement table is keyed by a string, in the convention `out["cells"]` already uses
in the same function. **Both ends move together**: the writer inside `_rg_agree` and the
reader in `report_regime_gate` at line 3079, which currently unpacks the tuple. A
one-sided change turns a crash into a wrong table.

`sm` must be JSON-serialisable **as a whole** after this change, not only in the field
that raised — verify by serialising, not by inspection.

### C · `.github/workflows/backtest_bench.yml` — wire the mode

Hard floor item 8 forbids touching this workflow unless the TZ names it; **this TZ names
it.** Add `--venue-census` to the workflow's mode selection so the census can be
dispatched, changing no existing mode, no existing step and no existing input default.

**I have not read this file and this TZ quotes nothing from it.** Read it, make the
minimal addition its current shape allows, and **quote the before-and-after of the block
you changed in the report** so the audit compares text rather than a description. If its
shape makes the addition non-minimal, report that instead of widening the change
(contract §6).

---

## 3. What must NOT move

Report a violation rather than acting on it.

- **`bench/cache/**` — not one file written, replaced or removed by scope A.**
- `fetch_prices`, `_save`, `census`, `_splice`, `ALIAS`, `reconcile`, `target_gate`,
  `HARD_CLASSES`, `CLASSES` — the census reads them and changes none. **No venue policy
  changes in this TZ.**
- `index.html`, `main.py`, `catalysts.json`, `tokens[]`, any threshold anywhere.
- Every existing mode's behaviour and output.
- `.github/workflows/bench.yml`.

---

## 4. Validation — written by the Architect, run by the Executor

Every item runs. An item that cannot run **fails**; it is never "not applicable"
(contract §9).

1. `python3 -m py_compile bench/backtest_bench.py`.
2. **Read-only, proven rather than stated.** Record `bench/cache/` before the census —
   file list, sizes, mtimes — run the census, record it again, and assert the two are
   identical. **Then run the census with the cache directory made read-only and confirm
   it still completes.** A mode that only *happens* not to write is not the mode this TZ
   specifies.
3. **Offline serialisation control for scope B.** Build the summary object on synthetic
   `by_H` / `btc` input, `json.dump` it to a temp path, read it back, and assert the
   agreement table round-trips with the same counts. Count the entries compared and fail
   on zero (map inv. 22).
4. **Negative control on scope B** (map inv. 23). Plant the tuple key back and confirm
   item 3 turns red with the same `TypeError`. Revert, confirm the tree is clean, confirm
   item 3 is green again.
5. **Reader control on scope B.** Confirm `report_regime_gate` prints the same agreement
   counts before and after the key change, on the same synthetic input. The observed
   counts on the attached run — `range × диапазон 72`, `range × тренд 6`,
   `stress × диапазон 8`, `stress × тренд 1`, `trend × диапазон 53`, `trend × тренд 5`,
   over 145 dates — are the shape to reproduce; the numbers themselves belong to that
   run's data and are not an expectation here.
6. **Gate replay.** Run `.github/workflows/bench.yml`'s steps locally against the
   unmodified checkout and against the change. Report every step's check count on both
   sides. Step 14 (`bench/backtest_guard_bench.py`) loads this module by path — confirm
   it still passes and report its count (map inv. 62).
7. **The census itself is a DISPATCH, not a validation item.** It fetches from
   `data.binance.vision`, and map inv. 44 with hard floor item 9 forbid a session fetch
   standing behind a product fact. **Do not run the census in-session against the live
   archive.** Validate the mode offline — items 1–6, plus its arithmetic on a hand-built
   bucket dict with a known gap, a known tail and a known pre-listing window — and report
   the mode as built and unmeasured. The reading is taken on a runner, by the Boss's
   dispatch, after the merge.
8. **A local replay is not a runner run.** Say which workflows executed on GitHub with
   their conclusion, and which did not, with the reason (contract §9). Do not forecast a
   gate result.

---

## 5. Files

**Modify:** `bench/backtest_bench.py` · `.github/workflows/backtest_bench.yml`.

**Create:** nothing.

**Delete:** nothing.

---

## 6. What this TZ deliberately leaves open

Recorded so the next TZ is written against a stated gap rather than a silence.

- **The venue switch itself.** It is written against scope A's reading and not before it.
- **The basis licence in `reconcile`.** It keys on `sym in fut` and must key on the venue
  the series was actually fetched from. `_save` already records that as `doc["src"]`
  (`"vision"` / `"vision-perp"`), so the field exists and nothing new is invented — but
  it moves with the switch, never ahead of it.
- **Realised funding in `--regime-gate`, replacing `f*`'s arithmetic** (§1.2).
- **UNI, XLM and ZEC.** All three are spot-declared, so `reconcile` gives them no basis
  licence, and all three newly classed `unexplained` — a state the map's §7 records as
  zero on 30 of 30 coins, measured 05.09.2026. Both attached runs were therefore taken on
  27 coins, not 30. **The diagnosis is not attempted here**: it needs the same census to
  say whether the spot leg or the composite moved, and guessing it now would be the
  fourth reading taken on the wrong instrument.
