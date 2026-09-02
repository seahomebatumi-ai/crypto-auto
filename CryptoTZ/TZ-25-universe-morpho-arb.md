# TZ-25 — Universe: add MORPHO and ARB as declared futures-only

**Canonical filename:** `CryptoTZ/TZ-25-universe-morpho-arb.md`
**Class:** branch + pull request (production files).
**Model:** Opus. Multi-file, touches the bot, the frontend and the declared venue set.

---

## 0. System Map fingerprint gate — BLOCKING

Match every anchor below as an exact substring against `SYSTEM-MAP-CRYPTOCALCUL.md`
in the repository before any work. Any mismatch → BLOCKED, report and stop.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-02-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `58. **A rule that names an object without naming how to compute it has named nothing.**` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

---

## 1. Objective

The owner has reversed the standing «no new coins» decision for exactly two assets.
The universe becomes **30 coins**: the current 28 plus **MORPHO** and **ARB**, both
entering as **declared futures-only** (`fut:true`).

**This is an owner decision, not an analytical one.** Nothing in it reopens the
directional layer, no ranking factor is added, no weight is tuned, and no threshold
moves. The standing decision in map inv. 2 and `## 8` is amended by the owner for
these two assets and remains in force for every other.

---

## 2. Why `fut:true`, and what it protects — do not deviate

Both coins are declared **Binance Futures only inside this system**, joining XMR, LIT
and HYPE under map §3.14. The declaration is a property of the asset in this list and
is not an observation about what a host answers (inv. 41).

The declaration is what keeps this change small. Every measurement in the system that
is calibrated on the SPOT universe stays untouched, because `listExhaustion` skips
`fut:true` rows ahead of every other test (inv. 41):

- the spot universe stays at **25**, so `DAY_RANGE_ABNORMAL = 1.39` is not re-opened,
  `bench/exhaustion-calibration.txt` is not touched, and the inv. 46 comparison in gate
  step 12 stays green;
- the §3.17 caption's «25 спотовым монетам» and the exact-string expectation gate
  section M pins it with **do not move** (map §3.14, inv. 50);
- journal coverage becomes **25 of 30**, declared, and neither coin may ever raise
  `hardSkip` — the venue test short-circuits ahead of the degradation ladder (inv. 41).

**If any of the four sites above requires an edit, STOP and report.** A required edit
there means the declaration leaked into the spot universe, which is a defect in this
TZ and not a task to complete.

Discarded alternative, named for the record: declaring both as spot assets. It moves
the spot count 25 → 27, which drags four coupled text sites, the exhaustion universe
and a calibrated constant into a change whose purpose is two rows in a list, and it
would put a live question over a number pinned to a three-year archive run.

---

## 3. Ordering — the Boss's Shortcut moves FIRST

`analyst/live-gate.sh` exits **5** when a `tokens[]` symbol is absent from the `c`
array of `analyst/live.json`, and a non-zero exit strips every price level from every
analysis run. The payload is written by the Boss's Shortcut, which this repository
never edits.

```
step 1  Boss adds MORPHOUSDT and ARBUSDT to the Shortcut's c-array symbol list
step 2  Boss runs LIVE SNAP once; analyst/live.json lands on main carrying n = 31
step 3  THIS TZ is executed
```

Step 1 is safe on its own and reversible: extra rows in `c` are not a gate failure
class, so a payload of 31 rows validates cleanly against a 28-coin `tokens[]`.
**The reverse order is not safe** and would take the analysis engine's levels off
line until the Shortcut catches up.

**Before starting, verify step 2 landed**: `analyst/live.json` on `origin/main` carries
`n` = 31 and both symbols in `c`. If it does not, report BLOCKED in one line and stop.

---

## 4. Scope — exactly these edits

### 4.1 `main.py`

Add two entries to `TOKENS`, following the existing structure exactly, minimal diff.

| Symbol | CoinGecko id (declared) | Note |
|---|---|---|
| MORPHO | `morpho` | |
| ARB | `arbitrum` | |

**The two ids are declared by the Architect and are validated empirically, never in
this session.** Do not fetch CoinGecko to check them (map inv. 44): a product fact
behind a session fetch is not reproducible. The arbiter is `debug.json` after the
first bot run on a runner — `error: null` and `matched_90d > 120` on both. If either
returns `error: true`, report it and stop; the corrected id arrives as a one-line
follow-up and this TZ is not amended.

Per-run CoinGecko calls move **30 → 32** (BTC + 30 alts + one `/coins/markets`).
At 17 dispatches/day that is ≈ 16 300 calls/month, inside the keyless public tier;
map §5's ban on attaching the Demo key is unaffected and unchanged.

### 4.2 `index.html`

Add two entries to `tokens[]`, following the existing structure exactly, each with
**`fut:true`** and the Binance USDⓈ-M perpetual pair. Display names: `MORPHO`, `ARB`.
ES5 only, no other edit to the file.

### 4.3 Hardcoded universe counts

Enumerate every site in `bench/**`, `journal/**` and `index.html` that carries the
literal 28 as a universe count, and update those that are counts of `tokens[]`.
**List every site inspected in the report, including the ones you did not change and
why.** A count that is a spot-coverage count (25) is NOT a universe count and does not
move (§2 above).

### 4.4 Nothing else

Do not touch: `catalysts.json` · `analyst/**` · `bench/exhaustion-calibration.txt` ·
`DAY_RANGE_ABNORMAL` · any threshold · any workflow file · `scoreCandidate` weights.

---

## 5. Expected bench movement — attribute it, do not accept it

Gate steps that MUST move, with the predicted delta:

| Step | Bench | Predicted | Why |
|---|---|---|---|
| 8 | `catalyst_bench.js` | 23 062 → **23 066** (+4) | +2 per-symbol assertions per added symbol, per the TZ-21 attribution in map `## 0` |
| 7 | `journal_bench.js` | moves | content-sensitive: two more symbols produce two more records (map `## 0`) |

Steps that MUST NOT move: **12** (`exhaustion_bench.js`, 220 598) and the section M
expectations. Step 13 (`live-gate.sh --selftest`, 40) cuts its universe from
`tokens[]` at run time and its fixtures are generated from that same parse, so it
should hold at 40 — if it moves, say by how much and why.

**Any delta is attributed term by term** (inv. 43). A count that moved by an amount
you cannot explain is a finding, not a pass, and a bench is never edited to make it
pass.

---

## 6. Validation — written by the Architect, executed by the Executor

1. `python3 -m py_compile main.py`.
2. `node --check` on the extracted `<script>` of `index.html`.
3. Full `bench.yml` gate, 13 steps, with the per-step table and the attribution of §5.
4. **Two-way compatibility (inv. 1, inv. 9):** the frontend running against an OLD
   `coeffs.json` that has no rows for the two new coins renders those two cards as
   NO DATA and every other card unchanged. State this explicitly.
5. **Spot ticker unchanged (inv. 12):** neither new symbol appears in the spot
   `?symbols=` request; the request stays ~12 KB and does not fall back to the 1.2 MB
   full ticker. This is the direct consequence of `fut:true` and is the check that
   proves the declaration reached the code.
6. **Venue path (inv. 41):** both coins price from `cachedFutTickers`; the dead-market
   detector works on `count` alone for them.
7. **`listExhaustion` universe unchanged:** the day-range measure still counts 25 rows
   on a full board, not 27.
8. No-regression statement covering every file touched.

Note: if `bench/backtest_bench.py` cannot build a three-year archive for MORPHO, that
is expected and is the standing of `GRAM` (map §3.16); record it, do not repair it.

---

## 7. Report

`CryptoReports/TZ-25-universe-morpho-arb-report.md`, straight to `main`, per
`EXECUTOR-INSTRUCTIONS.md` §10. The report states the fingerprints the map's `## 0`
table currently lists, the 13-step gate table with every delta attributed, and the
enumeration required by §4.3.

---

## Что сделать
1. Загрузить `TZ-25-universe-morpho-arb.md` в `CryptoTZ/`
2. Добавить MORPHOUSDT и ARBUSDT в список символов Shortcut, запустить LIVE SNAP один раз
3. В Claude Code отправить `EXECUTE TZ-25` — модель **Opus**
4. Прислать `CryptoReports/TZ-25-universe-morpho-arb-report.md`
5. Слить pull request после моего вердикта
