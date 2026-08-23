# Implementation Report — TZ-12

Regime stress symmetry, venue-correct list exhaustion, and the «РИСК ВЫНОСА» board block.

## Status

**COMPLETED.** All four stages implemented, all eleven §5 validation items run, full
12-step gate green on a runner.

**No pull request exists.** This session runs under a base configuration that forbids
opening one without an explicit instruction (contract §8). The branch is pushed and CI
ran on it — see `## Pull Request` and `## CI Execution`.

Previous TZ's branch: **TZ-11 was merged** (PR #11, `3fcdddc`, reachable from
`origin/main`). This work is not stacked on an unmerged base.

## Inbound Filing

Nothing moved or renamed. `CryptoTZ/TZ-12-stress-symmetry-and-squeeze-block.md` was
already on `origin/main` under its canonical filename at commit `e076545`, confirmed
after `git fetch --all --prune`.

The session clone was **shallow** (`git rev-parse --is-shallow-repository` → `true`,
78→305 commits after `git fetch --unshallow`). Deepened before any historical
assessment, per contract §3.

## Fingerprint Gate — PASSED

Compared against `origin/main` (`e076545`), never local `main`. Working tree was
identical to `origin/main` at start (`git diff --stat origin/main` empty).

| Anchor | Required | Found |
|---|---|---|
| revision | `**Revision 2026-08-23-b.**` | present |
| direction engine | `### 3.12 Direction engine — veto cascade` | present |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | present |
| newest invariant | `47. **A threshold is calibrated on the distribution…** ` | present |

| File | Map says | Measured at start | Match |
|---|---:|---|---|
| `index.html` | 3569 lines, `56af2e274e5568527a6bb0e5cb4e3456` | 3569, `56af2e274e5568527a6bb0e5cb4e3456` | yes |
| `main.py` | 506 lines, `1a5a5d98b2fd76010f202ee3eebaa717` | 506, `1a5a5d98b2fd76010f202ee3eebaa717` | yes |
| `catalysts.json` | 11 lines, `021dd2c90dc395240c0b0c3dbae40426` | 11, `021dd2c90dc395240c0b0c3dbae40426` | yes |

Gate baseline measured from a `git worktree` at `origin/main`, not assumed:
**1 185 871** checks over 12 steps, every step exit 0. Reproduces the TZ header exactly.

## Scope Executed

| Stage | Status |
|---|---|
| A — symmetric regime stress (`marketRegime`, `regimeBanner`) | done |
| B — venue-correct `listExhaustion` | done |
| C — new board block «РИСК ВЫНОСА», sixth | done |
| D — benches wired into the existing 12 gate steps | done |

## Files Created

- `CryptoReports/TZ-12-stress-symmetry-and-squeeze-block-report.md` (this file, direct to `main`)

## Files Modified

| Path | Change |
|---|---|
| `index.html` | `marketRegime` comparison; `regimeBanner` stress branch; `listExhaustion` venue test; new `sSqz` section; one line in the `boardHtml` concatenation. +98 / −11 lines |
| `bench/direction_bench.py` | new `check_regime()` — regime symmetry cells; wired to the existing `--props` flag. +128 lines |
| `bench/exhaustion_bench.js` | new section C1 (venue) and D2 (symmetric stress, byte-identical banner table). +201 / −3 lines |
| `bench/prot_bench.js` | new `suiteSqueezeOrder()` and `suiteSqueeze()` — block presence, position, degradation, purity. +302 lines |

`main.py`, `catalysts.json`, `journal/**` and `.github/workflows/**` were **not touched**
(`git diff --stat origin/main` names exactly the four files above).

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### Stage A — symmetric regime stress

`marketRegime`, one comparison:

```
BEFORE:  if (v >= VOL_HARD || (out.z !== null && out.z <= -REG_STRESS_Z)) {
AFTER:   if (v >= VOL_HARD || (out.z !== null && Math.abs(out.z) >= REG_STRESS_Z)) {
```

No new constant; `REG_STRESS_Z` stays the single site (inv. 20). `out.dir` is untouched
and stays 0 in stress.

`regimeBanner`, the `stress` branch gains one clause chosen by the sign of `reg.z`,
colour `var(--red)` in both:

```
reg.z !== null && reg.z >= REG_STRESS_Z  ->  «РЫНОК ПЕРЕГРЕТ — сделок нет ни на одной стороне»
otherwise                                ->  «СТРЕСС РЫНКА — сделок нет ни на одной стороне»
```

The existing literal is kept whole and byte-identical — it was not refactored into a
shared tail. `reg.z === undefined` (a fixture with no `z`) falls to the existing branch,
so every stress fixture reaching the banner by the old route renders exactly as before;
proven in `## Test Results` item 9 (4 of 20 banner states differ, all upward-stress).

### Stage B — venue-correct list exhaustion

```
BEFORE:  if (!row || !row.cd) continue;
AFTER:   if (!row || (row.t && row.t.fut)) continue;
         if (!row.cd) continue;
```

The declaration is read from production's own `tokens[]` entry carried on `row.t`
(inv. 41), never from what a host returned. The venue test short-circuits ahead of the
`cd` test, so a `fut:true` row can never reach `dayRangeRatio` regardless of the fields
it carries — proven by a throwing accessor, not by reading the source. The `n < 8`
quorum is unchanged and applied after the exclusion: `n` counts contributing spot rows
only.

### Stage C — «РИСК ВЫНОСА»

A new `sSqz` section computed after `E`, `dec` and `currentLev` are available (right
after the `sLev` block), inserted **only** into the concatenation at the end of
`boardHtml`, between `sLev` and `sSize`. Block code order is untouched; every following
comment number shifted by one (inv. 15). It uses no variable declared in the size block
(`notional`, `qty`, `mrg`, `qtyTxt` do not appear in it).

`.bd-h` text is `РИСК ВЫНОСА`, unique on the board (inv. 18). The `.bd-sec` carries **no
inline `style`** (§3.7 — an inline style kills the metal ring).

**Row 1 — запас до ликвидации.** From the pressed `currentLev`, never from the RESULT
(inv. 14). `liq = liqPrice(E, currentLev, isLong)`; `b = |ln(liq/E)|`;
`dSig = b / sigmaDay(cd.volatility)`; `p24 = touchProb(cd.volatility, b, 24)`, printed
through `probTxt` (inv. 20). Every formula is an existing production function; nothing
is recomputed (inv. 21). The caption states the horizon is a new one, distinct from the
7/14/30d ladder in «ЦЕНА ВРЕМЕНИ» (which is not modified), and that the probability is
a lower bound (§7). Missing `volatility` → the sigma distance prints as `—` and the
second line says the bot gave no volatility; the block survives (inv. 9). `liq`
non-finite or `E <= 0` → the row is omitted, the block survives.

**Row 2 — насколько день уже вынесен.** `own = dayRangeRatio(hi24, lo24, cur,
cd.volatility)` from the same ticker fields the render loop reads
(`coin.highPrice` / `coin.lowPrice`), and `list = listExhaustion(lastRows)`. Printed as
plain multiples of a diffusive day — «сегодня X,X обычного дня», «медиана списка Y,Y по
N монетам». **No threshold, no comparison, no colour, `abnormal` is not read**; the
caption states that 1,0 is an ordinary day because `E[range] = σ·√(8/π)`, so the number
is interpretable without a constant. `median === null` → the list line says the list
could not be measured and names how many coins had a measure; the coin line still
prints. `own === null` → the coin line is omitted.

**Row 3 — стоп отодвинут от шума.** Read from `dec.inv`, nothing recomputed (inv. 20):
`capped` → «опоры рядом нет, уровень нарисован — стоп держится вручную»; `floored` →
«стоп прижат к полу 2σ: ближе шума ставить нельзя»; otherwise `inv.dist / inv.sd` in
daily sigmas. `dec.inv === null` → the row is omitted (there is nothing to read), the
block survives.

**Purity.** No output of this block enters `scoreCandidate`, `tradeGeometry`,
`leverageDecision`, `directionVerdict`, `marketRegime` or the journal writer. Proven
statically and at runtime — `## Test Results` item 8.

**One formatting decision, stated because the TZ fixed it only for row 2.** The TZ
specifies «сегодня X,X обычного дня» and «медиана списка Y,Y» with a decimal comma. The
sigma distances in rows 1 and 3 use the same comma so the block reads consistently; the
rest of the board uses a dot. This is the block's only formatting departure from its
neighbours and is confined to it.

### Stage D — benches

- `bench/direction_bench.py` — new `check_regime()`. Grid of `z` over `[-4, +4]` at 0.1
  plus the exact boundaries `±REG_STRESS_Z` and their ±1e-9 / ±1e-12 neighbourhoods and
  the two journaled values `+4.06` / `+4.01`; `volatility` across the `VOL_HARD`
  boundary (`VH−1e-9`, `VH−1e-12`, `VH`, `VH+1e-12`, `VH+1e-9`, plus five values either
  side); nine `eff` values across `EFF_TREND` and the ±3 clip. **11 236 cells.** Asserts
  `mode === 'stress'` exactly when `v >= VOL_HARD || |z| >= REG_STRESS_Z`, `dir === 0`
  in every stress cell, and a **mirror property that names no threshold at all**:
  same `v`, same `eff`, opposite sign of `z` → same mode and same dir. The fixture
  asserts its own integrity (production must report the `z` it was given) and fails if
  no cell landed exactly on `|z| = REG_STRESS_Z` (468 did) or if any of the three modes
  went unexercised. Counters increment at the comparison site (inv. 43).
  Wired to the existing `--props` flag **on purpose**: a separate flag would need a 13th
  step in `bench.yml`, and the TZ holds the count at 12.
- `bench/exhaustion_bench.js` — section **C1** (venue): mixed list vs the same list with
  the `fut:true` rows physically removed, interleaved so the exclusion cannot be a
  position artefact; a list that reaches quorum only by counting `fut:true` rows
  (`median === null`); the short-circuit proof by throwing accessor, with a
  control proving the probe can detect a read; `fut` falsy variants; the live 25+3
  shape. Each case carries its own control on the control — the same rows *without* the
  declaration must move both `median` and `n`, or the assertion is vacuous (inv. 22, 23).
  Section **D2** (symmetric stress): all five banner states × `isLong` both ways, each
  compared **byte-identically to a table written out in the bench**, plus an end-to-end
  route `btcStats → marketRegime → regimeBanner` at ±4σ, ±`REG_STRESS_Z` exactly, quiet,
  and vol-driven stress.
- `bench/prot_bench.js` — `suiteSqueezeOrder()` reads the concatenation out of
  `index.html` and asserts `sSqz` is the **sixth numbered block**, between `sLev` and
  `sSize`, with every other operand unchanged: inv. 15 puts block order in exactly one
  place, so that is where position is asserted. `suiteSqueeze()` then proves the source
  order reaches the screen and covers `capped` / `floored` / neither (each fixture
  asserted to *be* that state before its text is checked), missing `volatility`,
  `median === null`, `E <= 0`, non-finite `liq`, and **both sides × all six leverage
  buttons** — see `## Deviations` on the TZ's "four".

`bench.yml` is byte-unchanged. Step count stays **12**.

## Validation

Every §5 item was run. None is marked "not applicable".

### 1. Compile and guards

```
python3 -m py_compile main.py                       -> OK
node --check <script> extracted from index.html     -> OK
ES5 guard over the 98 added lines                   -> 0 violations
Cyrillic-in-JS-string-literal guard, 98 added lines -> 0 violations
```

The guard walks `git diff -U0 origin/main -- index.html`, strips `//` comments outside
strings, and fails on `let`/`const`/`=>`/backtick/`class`/spread/`async`/`await` in code
and on raw Cyrillic inside any string literal. It reports the number of lines it
checked and fails on zero (inv. 22).

### 2. Stage A, the boundary

`REG_STRESS_Z = 2`, `VOL_HARD = 0.02`, `H_NOISE = 168`. `r7` constructed as
`z · v · √H_NOISE` so the reported `z` is the intended one; the exact-boundary rows are
confirmed to have landed exactly (`|out.z| === REG_STRESS_Z` → `true`).

| Case | v | reported z | mode | dir | known |
|---|---|---|---|---|---|
| `z = −REG_STRESS_Z` | 0.01 | −2.000000000000000 | **stress** | 0 | true |
| `z = −REG_STRESS_Z + ε` | 0.01 | −1.999999999000000 | range | 0 | true |
| `z = +REG_STRESS_Z − ε` | 0.01 | +1.999999999000000 | range | 0 | true |
| `z = +REG_STRESS_Z` | 0.01 | +2.000000000000000 | **stress** | 0 | true |
| `z = null`, `vol >= VOL_HARD` | 0.02 | null | **stress** | 0 | true |
| `z = null`, `vol < VOL_HARD` | 0.01 | null | range | 0 | true |
| `z = +4.06` (2026-08-21) | 0.01 | +4.060000000000000 | **stress** | 0 | true |
| `z = +4.01` (2026-08-22) | 0.01 | +4.009999999999999 | **stress** | 0 | true |

The comparison is `>=` on both sides and the boundary itself is stress; one ULP inside
is not.

### 3. Stage A, the replay

Both journaled dates replayed through the production functions cut out of `index.html`
(inv. 21 — `marketRegime`, `leverageDecision`, `residual7`, `directionVerdict`,
`regimeBanner` are executed, no formula is reimplemented). Inputs are the recorded
`btc`, `cd` and `px` blocks of each `k:'s'` line.

| | 2026-08-21 | 2026-08-22 |
|---|---|---|
| coins in the snapshot | 25 (3 declared skips) | 25 (3 declared skips) |
| recorded `reg` | `trend`, dir +1, z 4.0636, eff 2.2904 | `trend`, dir +1, z 4.0120, eff 2.3668 |
| replayed `reg` | **`stress`, dir 0**, z 4.0636, eff 2.2904 | **`stress`, dir 0**, z 4.0120, eff 2.3668 |
| recorded actions, LONG | none 24, wait 1 | none 23, trade 1, wait 1 |
| recorded actions, SHORT | none 25 | none 25 |
| replayed actions, LONG | **none 25** | **none 25** |
| replayed actions, SHORT | none 25 | none 25 |
| geometry veto entries | 37 → **0** | 36 → **0** |
| banner, LONG and SHORT | «РЫНОК ПЕРЕГРЕТ — сделок нет ни на одной стороне» | «РЫНОК ПЕРЕГРЕТ — сделок нет ни на одной стороне» |
| verdict changes vs the record | 1: `GRAM/long: wait → none` | 2: `GRAM/long: trade → none`, `HBAR/long: wait → none` |

This is exactly the outcome §2 Stage A stated in advance: both dates move from
`trend/dir=+1` to `stress`, every coin's `action` becomes `none`, the one `trade`
(`GRAM`) and the one `wait` (`HBAR`) on 2026-08-22 disappear, and the board prints the
new banner. **No departure — no finding.**

**Addendum — a third journaled date arrived on `main` mid-session.** `journal.yml`
committed `journal/data/2026-08-23.jsonl` at `c5d5ea5` while this work was in progress
(machine-written, direct to `main`, per the lifecycle table). It is not named in §5
item 3, which was written when two dates existed; it is replayed here because the data
now exists and it is the same question. No production file moved in that commit — the
fingerprint gate above is unaffected (`index.html`, `main.py`, `catalysts.json` and the
System Map are byte-identical at `c5d5ea5` and at `e076545`), and `journal_bench.js`
does not read the repository's `journal/data/**` (its `ROOTS` holds only the temp roots
it writes itself), so no gate count moves either.

| 2026-08-23 | `origin/main` | candidate |
|---|---|---|
| `reg` | `trend`, dir +1, z 3.9758, eff 2.3509 | **`stress`, dir 0**, z 3.9758, eff 2.3509 |
| replayed LONG | none 24, wait 1 | **none 25** |
| replayed SHORT | none 25 | none 25 |
| banner | «ТРЕНД ВВЕРХ — счёт по каналу импульса» (green) | «РЫНОК ПЕРЕГРЕТ — сделок нет ни на одной стороне» (red) |

Recorded in the journal: LONG none 24, wait 1; SHORT none 25 — the `origin/main` column
reproduces the record exactly, which is the control on the replay. A third consecutive
four-sigma day, same direction, same outcome: the layer that exists to say a week is
dangerous now says it.

### 4. Stage A, negative control

`index.html` copied, then the one-sided comparison restored in `marketRegime`:

```
direction_bench.py --props   -> [FAIL] РЕЖИМ
   режим не по спецификации: 1638; асимметрия по знаку z: 5460
   первая ячейка: зеркало v=0.0005 z=-4: stress vs range
   ИТОГО проверок: 255969 | провалов блоков: 1        exit code 1
exhaustion_bench.js          -> 6 FAILs (end-to-end +4σ / +Z exact, mode and both banners)
                                --- checks: 220275  fails: 6 ---   exit code 1
```

Restored, then verified by MD5 against the pre-control copy:

```
MD5 before control : 64acaaa59f2ed96d568714d2813d20f9
MD5 after restore  : 64acaaa59f2ed96d568714d2813d20f9
cmp against the pre-control copy: byte-identical
direction_bench.py --props exit after restore: 0
exhaustion_bench.js        exit after restore: 0
```

The symmetry cells turn red and the step exits non-zero. The gate is proven to fail.

### 5. Stage B

**(a) Median and `n` with and without the `fut:true` rows.** Nine spot rows at ratios
0.6…1.4 and three `fut:true` rows at 9.0 / 9.5 / 12.0, interleaved.

```
listExhaustion(mixed)                       -> {"median":1.0000000000000007,"n":9}
listExhaustion(fut rows physically removed) -> {"median":1.0000000000000007,"n":9}
same rows WITHOUT the declaration           -> {"median":1.1500000000000008,"n":12}   <- the defect
```

Their presence changes both `median` and `n` when the declaration is not read, and
neither when it is.

**(b) Below quorum, exclusion first.** Five spot + five `fut:true`:

```
listExhaustion(5 spot + 5 fut)      -> {"median":null,"n":5}
the same 10 without the declaration -> {"median":3.0000000000000004,"n":10}
```

Quorum is applied after the exclusion; a list that reaches eight only by counting
`fut:true` rows has no verdict.

**(c) The venue test short-circuits ahead of the `cd` test.** A `fut:true` row whose
`cd` is a getter that throws:

```
fut:true row + throwing cd getter -> exception: null | cd reads: 0 | {"median":4.5,"n":8}
the SAME probe with no declaration -> exception: "read" | cd reads: 1   <- the probe works
```

The row was skipped before anything read `cd`, and the probe is proven able to detect a
read (inv. 23) rather than being trivially silent.

**(d) Live shape.** 25 spot + 3 `fut:true` → `{"median":1.6999999999999993,"n":25}`.

### 6. Stage C, the block

**Present on every board, sixth, `.bd-h` unique, no inline `style`.** Asserted in
`prot_bench.js` over both sides × all six leverage buttons (12 boards), plus every
degradation case and every extreme in item 11 — 32 further boards. Position is asserted
where inv. 15 puts it, in the concatenation read out of `index.html`:

```
operands: sHero,sRel,sWarn,sWhy,sRange,sEntry,sLev,sSqz,sSize,sBounds,sTime,sLoss,sWin,sProt,sSrc,sTrust
numbered blocks (sRel/sWarn fold into block 1): sSqz index 5 -> SIXTH, between sLev and sSize
```

and the rendered headers are asserted to appear in the canonical display order on every
board, with `РИСК ВЫНОСА` immediately after `ВЫБОР ПЛЕЧА` and immediately before
`РАЗМЕР ПОЗИЦИИ`.

**Reference case, every number recomputed by hand.** `UNI`, `E = $10.00`, `4X`, LONG,
`vol = 0.009470732461237308` — the `cd.volatility` of `UNI` in the 2026-08-22 snapshot.
`hi/lo/cur = 4.447 / 3.743 / 4.208` from the same snapshot; `min30/max30/min90/max90`
likewise.

```
LIQ_MMR                        = 0.0125
liq  = E·(1 − 1/L + MMR)       = 10 · (1 − 0.25 + 0.0125)   = 7.625000000000
b    = |ln(liq/E)| = |ln 0.7625|                            = 0.271152770501
sigmaDay = vol·√24 = 0.009470732461237308 · 4.898979485566  = 0.046396924041
dSig = b / sigmaDay = 0.271152770501 / 0.046396924041       = 5.844197133879   printed 5,8σ дня
p24  = touchProb(vol, b, 24) = 2·(1 − Φ(b / (vol·√24)))     = 0.000000005107   printed &lt;1%
own  = (4.447 − 3.743) / (4.208 · 0.046396924041 · √(8/π))   = 2.259631818840   printed 2,3
inv.dist = 0.278381544245  inv.sd = 0.046396924041  inv.capped = true
inv.dist / inv.sd                                            = 6.000000000000   (row 3 prints
                                                                the capped text, dist is at the 6σ cap)
```

Rendered block for exactly that case, with a 25-row spot list attached so the list line
reaches quorum:

```html
<div class="bd-sec"><div class="bd-h">РИСК ВЫНОСА</div>
<div class="bd-kv" style="margin-top:0;"><span class="bd-k">Запас до ликвидации при 4X</span>
  <span class="bd-v">5,8σ дня</span></div>
<div class="bd-kv" style="margin-top:0;"><span class="bd-k"></span>
  <span class="bd-v" …>шанс задеть за сутки &lt;1%</span></div>
<div class="bd-note">Горизонт — сутки. Это не лестница 7/14/30д из «ЦЕНЫ ВРЕМЕНИ» …
  истинная вероятность ВЫШЕ печатаемой, это нижняя граница.</div>
<div class="bd-kv" style="margin-top:11px;"><span class="bd-k">Сегодня уже вынесено</span>
  <span class="bd-v">2,3 обычного дня</span></div>
<div class="bd-kv" style="margin-top:0;"><span class="bd-k"></span>
  <span class="bd-v" …>медиана списка 2,0 по 25 монетам</span></div>
<div class="bd-note">1,0 — обычный день: у броуновского блуждания E[хода] = σ·√(8/π) …</div>
<div class="bd-kv" style="margin-top:11px;"><span class="bd-k">Стоп отодвинут от шума</span>
  <span class="bd-v" …>опоры рядом нет, уровень нарисован — стоп держится вручную</span></div>
</div>
```

`listExhaustion` on that list returned `{"median":2.0065229567578204,"n":25}` — printed
as «2,0 по 25 монетам». Every printed number matches the arithmetic above.

The `.bd-sec` opening tag is `<div class="bd-sec"><div class="bd-h">` with nothing
between: no inline style, so the metal ring survives (§3.7).

### 7. Stage C, degradation

Each case renders the block, says what is missing, and leaves the rest of the board
alive (inv. 9). Asserted in `prot_bench.js`; each `capped`/`floored`/`neither` fixture
is asserted to *be* that state before its text is checked.

| Case | Block | Behaviour |
|---|---|---|
| missing `volatility` | present | row 1 sigma prints `—` and says the bot gave no volatility; no 24h probability; coin line omitted; **list line still prints**; `РАЗМЕР ПОЗИЦИИ` and the rest of the board render |
| `median === null` (3 spot rows) | present | list line says the list could not be measured and names the count; **coin line still prints** |
| `inv.capped` | present | «опоры рядом нет, уровень нарисован — стоп держится вручную» |
| `inv.floored` | present | «стоп прижат к полу 2σ: ближе шума ставить нельзя» |
| neither | present | prints `inv.dist / inv.sd` in daily sigmas, asserted equal to the value read from `dec.inv` |
| `E <= 0` | present | row 1 omitted; rest of the board renders; the block's own markup is clean |
| non-finite `liq` | present | row 1 omitted; row 2 still prints; the block's own markup is clean |

One note on `E <= 0`: the **whole board** is not clean in that state and was not before
TZ-12 — see `## Pre-existing Issues`.

### 8. Stage C, purity

**Static.** Every identifier the block produces occurs only inside the block:

```
sqzNum  2768 2780 2796 2801 2814      sqzOwn  2791 2794 2796 2798
sqzLiq  2772 2773 2774                sqzList 2793 2800 2801 2802
sqzB    2774 2776 2777                sSqz    2765 2769 2778 2795 2798 2809 2817 2990
sqzVol  2775 2776 2777                        (2990 = the concatenation, inv. 15)
sqzSd   2776 2780        sqzP  2777 2783
```

Lines 2765–2817 are the block. Nothing escapes it.

**The journal writer does not know the block exists.** `journal/write.js` contains no
reference to `boardHtml`, `listExhaustion`, `dayRangeRatio` or `sSqz`, and its `NEED`
list — the names it reads out of the production context — is
`GIST_URL, STALE_CRIT_MIN, CAT_WINDOW_D, TIER_MIN, tokens, has, marketRegime, rangePos,
sideRelevant, residual7, leverageDecision, directionVerdict, tierOf, verdictNote`.
It contains none of `boardHtml`, `listExhaustion`, `dayRangeRatio`, `sigmaDay`,
`liqPrice`, `touchProb`, `probTxt`.

**Runtime.** The journal side record (the exact object `journal/write.js` writes) and
the regime, rebuilt with the block's own input — the list — perturbed:

| Perturbation | journal record identical | regime identical |
|---|---|---|
| 25 spot → 3 spot (below quorum) | yes | yes |
| 25 spot → empty list | yes | yes |
| 25 spot → 25 spot + 3 `fut:true` | yes | yes |
| 25 spot → 25 spot at different values | yes | yes |

And the board itself **does** move with the list, or the four rows above would be
vacuous (inv. 22):

```
25 spot vs 3 spot                board identical: false
25 spot vs 25 spot + 3 fut       board identical: true    <- the declaration works
25 spot vs 25 spot, other values board identical: false
```

`prot_bench.js` carries the same demonstration as permanent checks (`4b.6`), including
`scoreCandidate`, `leverageDecision` and the full `directionVerdict`.

### 9. No-regression, identity first

**Identity first (inv. 45).** `prot_bench.js` loads `index.html` a second time into its
own context and runs the differ against itself, unconditionally, inside the default
suite:

```
identity: 6 boards compared against index.html itself
PASS 372   FAIL 0
```

Zero differences, and the run is asserted to have compared a non-zero number of boards.

**Then whole boards against `origin/main`.** Six scenarios (both sides, 2X…7X, coin and
usdt modes, `vol = 0.025`, `vol = null`). For each, the candidate board with the new
section cut out is compared byte-for-byte with the baseline board:

| # | scenario | baseline | candidate | new section | candidate − section == baseline |
|---|---|---:|---:|---:|---|
| 0 | long 4X | 13 372 B | 14 724 B | 1 352 B | yes |
| 1 | short 3X | 15 398 B | 16 800 B | 1 402 B | yes |
| 2 | long 7X, coin mode | 13 857 B | 15 259 B | 1 402 B | yes |
| 3 | short 2X | 14 679 B | 16 081 B | 1 402 B | yes |
| 4 | long 5X, vol 2.5 %/h | 13 581 B | 14 969 B | 1 388 B | yes |
| 5 | long 5X, no vol | 7 248 B | 8 456 B | 1 208 B | yes |

Added bytes equal the section's bytes in every scenario: **the only board difference is
the inserted block.** (`prot_bench.js index.html <baseline>` reports these as six
`rest of board unchanged [baseline]` failures and exits 1 — that optional suite compares
the *whole* board and correctly refuses to call an added section "unchanged". It is not
part of the gate: `bench.yml` runs `node bench/prot_bench.js index.html` with no
baseline argument.)

**Banner differences, enumerated.** All ten regime states × `isLong` both ways = 20
outputs compared against `origin/main`:

```
banner states that differ: 4 of 20
  stress z=+Z/long    СТРЕСС РЫНКА …  BECOMES  РЫНОК ПЕРЕГРЕТ …
  stress z=+Z/short   СТРЕСС РЫНКА …  BECOMES  РЫНОК ПЕРЕГРЕТ …
  stress z=+4/long    СТРЕСС РЫНКА …  BECOMES  РЫНОК ПЕРЕГРЕТ …
  stress z=+4/short   СТРЕСС РЫНКА …  BECOMES  РЫНОК ПЕРЕГРЕТ …
```

`unknown`, `stress z=null`, `stress z=−4`, `stress z=−Z`, `stress z=+Z−ε`, `trend +1`,
`trend −1` and `range` are byte-identical on both sides. The differences that appear are
exactly the new block plus the upward-stress banner, and nothing else.

### 10. Full gate — 12 steps, every step exit 0

Baseline measured from a `git worktree` at `origin/main`; candidate from the working
tree. Both runs replay `bench.yml`'s twelve steps in order with the same commands.

| # | Step | Baseline | Candidate | Δ | exit |
|---:|---|---:|---:|---:|---|
| 1 | `verify_board.js` | 109 | 109 | 0 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 | 0 |
| 3 | `prot_bench.js index.html` | 175 | 372 | **+197** | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 188 577 | 255 708 | **+67 131** | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 | 0 |
| 7 | `journal_bench.js` | 694 030 | 691 109 | **−2 921** | 0 |
| 8 | `catalyst_bench.js` | 23 040 | 23 040 | 0 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 | 0 |
| 10 | `render_bench.py` | 15 925 | 15 925 | 0 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 | 0 |
| 12 | `exhaustion_bench.js` | 220 199 | 220 275 | **+76** | 0 |
| | **total** | **1 185 871** | **1 250 354** | **+64 483** | all 0 |

Baseline total reproduces the TZ header's **1 185 871** exactly.

**Delta explained term by term.**

*Step 3, +197.* All new, all in `suiteSqueezeOrder()` + `suiteSqueeze()`: 3 concatenation
assertions; 12 boards (2 sides × 6 leverage buttons) × 11 assertions = 132; 3 `dec.inv`
states × 5–6 = 17; missing volatility 7; the list line 9; venue on the board 2; `E <= 0`
and non-finite `liq` 8; purity 3; plus the fixture-integrity assertions inside those
groups. Every one increments at its own comparison site (inv. 43).

*Step 5, +67 131 = +67 404 − 273.*
 - `check_regime` is new: **+67 404** comparisons over 11 240 cells (11 236 grid cells
   plus 4 `z = null` cells), 6 comparisons per cell plus one extra per stress/trend/range
   branch.
 - `check_props` **−273**, and the number is exact arithmetic, not drift. Its counter
   adds three comparisons per *tradeable* side; symmetric stress removed 91 trades
   (2 855 → 2 764) from the same 60 000 random scenarios, and 91 × 3 = 273. Waits moved
   13 900 → 13 223 and refusals 103 245 → 104 013; waits and refusals carry no
   conditional comparisons, so they contribute nothing to the count.

*Step 7, −2 921 — a step the TZ did not authorise to move. Reported, not fixed.* The
whole delta is inside section 7 «Схема», which walks every field of every record the
bench itself writes and counts **numeric leaves**. Localised by instrumenting the
section banners (all other sections identical to the check), then attributed by field
path:

| field | baseline | candidate | Δ |
|---|---:|---:|---:|
| `long.geo.reward` | 2 180 | 1 665 | −515 |
| `long.geo.risk` | 2 180 | 1 665 | −515 |
| `long.geo.rr` | 2 180 | 1 665 | −515 |
| `long.geo.sd` | 2 180 | 1 665 | −515 |
| `long.geo.tgtSig` | 2 180 | 1 665 | −515 |
| `long.geo.wait` | 1 180 | 894 | −286 |
| `long.wait` | 277 | 217 | −60 |
| | | | **−2 921** |

86 other field paths are unchanged, and every short-side path is unchanged. The cause is
Stage A acting on the bench's own synthetic fixtures:

```
reg.mode over the 6 743 written snapshot rows:
  baseline   range 2 593  trend 2 225  stress 1 925
  candidate  range 2 593  trend 1 675  stress 2 475      -> 550 rows move trend -> stress
long actions:  none 6 391 -> 6 463 (+72)   wait 273 -> 213 (−60)   trade 79 -> 67 (−12)
short actions: unchanged (already vetoed by trend dir=+1)
long-side geo objects: 2 180 -> 1 665 (−515; 35 of the 550 flipped rows had no long geo)
```

A stress verdict returns before geometry, so `geo` is `null` and its five numeric leaves
plus `geo.wait` are not written, and the 60 disappearing waits take `long.wait` with
them. **Files and rows are identical on both sides — 303 files, 7 937 rows** — so nothing
was skipped: only fields that no longer exist stopped being checked. The step stays
green and exits 0.

*Step 12, +76 = venue 25 + symmetric stress 51.* Existing sections `identity` (200 002),
`nulls` (20 027), `quorum` (65), `banner` (52), `inert` (30), `purity` (22),
`control` (1) are all unchanged.

**Two steps whose COUNT did not move but whose CONTENT did**, both reported here because
§6 asks which fixtures the regime change touched:

- *Step 11*, `direction_bench.py --display`, 15 629 → 15 629 checks, but over the same
  284 synthetic lists: tradeable 203 → **192**, waits 829 → **772**, greys 6 920 →
  **6 988**. Coins numbered on both sides stay at 3 976. Local and runner agree
  digit-for-digit.
- *Step 5's* `--sim` block, the `walk` world:
  `{'trend': 7, 'range': 7}` → `{'trend': 6, 'stress': 1, 'range': 7}`, trades 42 → 39,
  one empty date. The `trend` world already carried one stress date and is unchanged;
  the `mean` world is unchanged.

Neither is edited. Both are the specified behaviour reaching fixtures that previously
labelled an upward four-sigma week a trend.

### 11. Extremes

Sixteen release-checklist extremes × both sides = **32 boards**, each rendered on the
candidate and on `origin/main`, checked for: the block present, the output free of
`undefined` / `NaN` / `Infinity`, and the candidate-minus-block byte-identical to the
baseline.

```
slider edge stress=panic · slider edge stress=normal · null betas ·
truncated Gist (no analysis_data) · HTTP 400 ticker (no cachedMarketData) ·
dead-market fields (count=0, empty book) · missing coeffs min30/max30 ·
missing coeffs r7/r14/r30/eff14 · missing coeffs 90d range · absent btcStats ·
absent volatility · vol above VOL_STOP · penny coin · no funding rate ·
zero margin · coin mode with qty 0

cases: 32   flagged: 0
```

Every case: block present `true`, output clean `true`, candidate-minus-block == baseline
`true`.

## Test Results

Twelve gate steps, all exit 0, **1 250 354** checks locally; the same twelve green on a
runner (`## CI Execution`). Negative controls run and confirmed for Stage A on both
benches that assert it. `prot_bench.js` identity run: 6 boards, 0 differences.

## Deviations

1. **`bench/direction_bench.py`'s regime cells run under the existing `--props` flag,
   not a flag of their own.** A separate flag would have needed a 13th step in
   `bench.yml`; the TZ holds the count at 12 and does not authorise editing the
   workflow. The block still reports as its own named section (`[OK ] РЕЖИМ`) with its
   own counter, and `--all` picks it up.
2. **The TZ's «both sides × the four leverage buttons» is covered as both sides × all
   six.** The board draws six leverage buttons (`for (var L = 2; L <= 7; L++)` in
   `sLev`), not four. Six is a superset of any four, so nothing the TZ asked for is
   missing. Flagged rather than silently reinterpreted.
3. **Decimal comma extended to the sigma distances in rows 1 and 3.** The TZ fixes the
   comma only for row 2 («сегодня X,X», «медиана списка Y,Y»). The block would otherwise
   print «2,3 обычного дня» next to «5.8σ дня». Confined to this block; the rest of the
   board is unchanged.
4. **Step 7 of the gate moved by −2 921**, and the TZ names only steps 3, 5, 11 and 12
   as permitted to move. Reported above and not fixed. It is arithmetic, not a defect:
   the count is a sum of numeric leaves in records whose verdicts Stage A legitimately
   changed, the file and row counts are identical, and the step exits 0.

## Pre-existing Issues

Found, **not fixed**, none caused by this task.

1. **`listExhaustion` can never reach quorum on the live board, because production rows
   never carry the three fields it reads.** `listExhaustion` reads
   `row.hi24`, `row.lo24`, `row.cur`, and no site in `index.html` or
   `journal/write.js` ever assigns them:

   ```
   grep -nE '\.(hi24|lo24|cur)\s*[:=][^=]' index.html journal/write.js
     journal/write.js:659:  p0: fin(s.px ? s.px.cur : null), …      (unrelated)
   index.html:3128  var row = { t: t, idx: idx, coin: coin, cd: null, state: 'ok', sc: null };
   index.html:3126-3127  var hi24 = parseFloat(coin.highPrice);   <- locals, never stored on row
   ```

   So on the live board `listExhaustion(lastRows)` returns `{median: null, n: 0}` and
   row 2's list line will always print «список не измерен: своя мера есть у 0 монет».
   The coin line is unaffected — it reads the ticker directly.

   This contradicts §3.16's live-behaviour claim and TZ-12 §1 defect 2 ("live it would
   compute over 28 rows"): live it computes over **zero**. Stage B is still correct and
   still necessary — it is proven on fixtures with the right shape, and it is what makes
   the estimator match its calibration the moment the fields are populated — but a
   consumer cannot see a median until a TZ adds `row.hi24 / row.lo24 / row.cur` to the
   render loop's row object (three assignments at `index.html:3126-3128`). That edit is
   not in this TZ's `## Scope` or `## Files`, so it was not made (contract §6: report the
   gap, never widen the fix).

2. **At `E <= 0` the board prints `NaN% от входа` in «ГРАНИЦЫ СДЕЛКИ».** Present on
   `origin/main`, verified directly:

   ```
   BASELINE origin/main, E=0:  NaN at offset 6042
     …ЛИКВИДАЦИЯ ПРИ 4X…<div class="bd-nd">NaN% от входа</div>
   ```

   The site is `Math.abs(liqSel / E - 1)` with `E = 0` → `0/0`. Outside this TZ's scope
   («ГРАНИЦЫ СДЕЛКИ» is not named in `## Files`). `prot_bench.js` surfaces it as a
   printed note on every run rather than freezing it as an assertion, and the new block's
   own markup is asserted clean in that state.

3. **`bench/prot_bench.js:166` carries a raw Cyrillic JS string literal**
   (`src: 'мин30'`, inside the `suitePlan` fixture). Pre-existing, on `origin/main`, and
   untouched. Every string added by this task is `\uXXXX`-escaped.

4. **The TZ's own «four leverage buttons»** does not match the board's six. See
   `## Deviations` 2.

## Remaining Risks

1. **The list line is dead on the live board until issue 1 above is closed.** The block
   ships with two of its three list-facing statements working (the coin's own ratio and
   the honest "not measured" line) and the median permanently absent. If the Architect
   intends the median to appear at TZ-12's merge, this needs a follow-up TZ populating
   the three row fields.
2. **Stage A materially reduces the number of tradeable days.** Both journaled dates
   went from one `trade` + one `wait` to zero of each. That is the specified intent, but
   the live effect is a board that will show no trades on any four-sigma week in either
   direction. Nothing measures how often that state occurs; the TZ-11 archive would.
3. **`journal_bench.js`'s check count is now sensitive to verdict content**, so any
   future change to the verdict shape moves step 7's total without indicating a defect.
   The count is still a true count of comparisons (inv. 43); it is simply not a stable
   number across behavioural changes. Worth an Architect decision on whether the gate
   total should be quoted per step rather than as one sum.
4. **`abnormal` remains hardcoded `false` and `DAY_RANGE_ABNORMAL` still does not
   exist.** Unchanged by this TZ, by design (§3 non-goal). The block prints a measured
   ratio and compares it to nothing.

## Commit

```
eca63ba  feat(board): symmetric regime stress, venue-correct list exhaustion,
         squeeze-risk block (TZ-12)
```

Branch `claude/execute-tz-12-rmjhwd`, four files:
`index.html`, `bench/direction_bench.py`, `bench/exhaustion_bench.js`,
`bench/prot_bench.js`.

Working tree left clean; every scratch file (`bench/_*`) removed, no `__pycache__`
committed.

## Pull Request

**NO PULL REQUEST EXISTS.** This session's base configuration forbids opening one
without an explicit instruction. Contract §8 fallback:

- **Branch:** `claude/execute-tz-12-rmjhwd`
- **Compare URL:** **https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-12-rmjhwd**

**Unlike TZ-06, this branch is NOT a branch without CI.** `bench.yml`'s `push` trigger
covers `claude/**` (added by TZ-07 for exactly this case), so the gate executed on a
runner against this branch head — see below.

## CI Execution

| Workflow | Ran on a runner | Trigger | Conclusion |
|---|---|---|---|
| `Bench gate` (`bench.yml`) | yes, run #60, id `32651140527`, head `eca63ba` | `push` to `claude/execute-tz-12-rmjhwd` | *(recorded below)* |
| `main.yml` (bot) | no | `paths-ignore` excludes `**/*.md`; the bot is Shortcut-triggered and this change does not run it | — |
| `backtest_bench.yml` | no | needs the external archive; not touched by this TZ | — |
| `journal.yml` | no | scheduled 13:00 UTC; not triggered by a push | — |
| `exhaustion_calib.yml` | no | one-off calibration, deliberately outside the gate | — |

Run URL: https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32651140527

**Conclusion: `success`.** All 12 bench steps green on the runner, job
`97222820104`, 2026-08-23 16:16:10–16:17:08 UTC, `ubuntu-latest`, Python 3.12.14,
Node 20.20.2.

The runner's own per-step counts, read out of the job log, match the local run
**exactly, step for step**:

| # | Step | Runner | Local | Match |
|---:|---|---:|---:|---|
| 1 | `verify_board.js` | 109 | 109 | yes |
| 2 | `board2_bench.js` | 130 | 130 | yes |
| 3 | `prot_bench.js` | PASS 372 FAIL 0 | 372 | yes |
| 4 | `verify_bench.py` | 35 | 35 | yes |
| 5 | `direction_bench.py` core | 255 708 | 255 708 | yes |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | yes |
| 7 | `journal_bench.js` | 691 109 | 691 109 | yes |
| 8 | `catalyst_bench.js` | 23 040 | 23 040 | yes |
| 9 | `display_bench.py` | 24 598 | 24 598 | yes |
| 10 | `render_bench.py` | 15 925 | 15 925 | yes |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | yes |
| 12 | `exhaustion_bench.js` | 220 275 | 220 275 | yes |
| | **total** | **1 250 354** | **1 250 354** | yes |

The runner also printed the new sections by name — `[OK ] РЕЖИМ` (11 236 cells, 468
exact boundaries), `=== C1. Venue … === compared: 25`, `=== D2. Symmetric stress …
=== compared: 51` — and the pre-existing-defect note from `prot_bench.js`
(`PRE-EXISTING (not TZ-12, present on origin/main): at E = 0 …`).

One non-blocking runner warning, unrelated to this change: `actions/checkout@v4`,
`actions/setup-node@v4` and `actions/setup-python@v5` target Node.js 20, which GitHub
has deprecated and is force-running on Node.js 24. Reported, not fixed —
`.github/workflows/**` is outside this TZ's scope.

## Final Repository State

`main` is untouched by the implementation. The four modified files live on
`claude/execute-tz-12-rmjhwd` only; this report is committed directly to `main` under
`CryptoReports/`, the one path contract §8 allows (GitHub Pages serves `index.html`, so a
Markdown file under `CryptoReports/` cannot reach the live calculator, and `**/*.md` is in
`main.yml`'s `paths-ignore`, so it cannot start the bot — both still hold).

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1129 | `17e746610947dc282b0208f54d9dff46` |
| `index.html` | 3656 | `64acaaa59f2ed96d568714d2813d20f9` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |

`SYSTEM-MAP-CRYPTOCALCUL.md` revision string, from its `## 0. Fingerprint` block:
**`Revision 2026-08-23-b.`**

`index.html` moved from 3569 lines / `56af2e274e5568527a6bb0e5cb4e3456` (the map's
figure, matched exactly at session start) to 3656 lines /
`64acaaa59f2ed96d568714d2813d20f9` on the branch. `main.py` and `catalysts.json` are
byte-unchanged and still match the map. `SYSTEM-MAP-CRYPTOCALCUL.md` is unchanged by this
task; the map's own line count and MD5 are not stated in its `## 0. Fingerprint` block, so
the values above are measured, not compared.
