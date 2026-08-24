# TZ-14 — Adoption of `DAY_RANGE_ABNORMAL` and the day-state consumer

**Executor report.** Branch `claude/execute-tz-14-47nul9`, commit `d7bb102`.

Compare URL:
`https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-14-47nul9`

---

## 0. Fingerprint gate — PASSED

`git fetch --all --prune` run first. The clone arrived **shallow**
(`git rev-parse --is-shallow-repository` → `true`) and was deepened with
`git fetch --unshallow` before anything historical was assessed; 321 commits
reachable afterwards. All comparisons below are against `origin/main`
(`21bd3e6`), never local `main`.

### Anchors in `SYSTEM-MAP-CRYPTOCALCUL.md`

| Anchor | Required string | Result |
|---|---|---|
| revision | `**Revision 2026-08-24-a.**` | **present** |
| direction engine | `### 3.12 Direction engine — veto cascade` | **present** |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | **present** |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | **present** |
| newest invariant | `49. **An admissibility band is derived from a null computed in the same run.**` | **present** |

### Baseline files at `origin/main`

| File | Lines required / measured | MD5 required / measured | Result |
|---|---|---|---|
| `index.html` | 3666 / 3666 | `cef52cf6eb00ff063e66510a5bd0f828` / same | **match** |
| `main.py` | 506 / 506 | `1a5a5d98b2fd76010f202ee3eebaa717` / same | **match** |
| `catalysts.json` | 11 / 11 | `021dd2c90dc395240c0b0c3dbae40426` / same | **match** |
| `bench/exhaustion-calibration.txt` | 175 / 175 | `3b8730b254467c9df4c0a845a0f3cfb3` / same | **match** |

The record file matched, so the number this TZ copies into production agrees
with a run that has not moved since it was audited.

### Gate baseline — measured, not assumed

Measured from a `git worktree` at `origin/main`, all 12 `bench.yml` steps run in
workflow order with the same harness later used for the candidate:

| # | Step | Baseline checks |
|---:|---|---:|
| 1 | `verify_board.js` | 109 |
| 2 | `board2_bench.js` | 130 |
| 3 | `prot_bench.js index.html` | 372 |
| 4 | `verify_bench.py` | 35 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 |
| 6 | `fresh_bench.js` | 3 424 |
| 7 | `journal_bench.js` | 691 109 |
| 8 | `catalyst_bench.js` | 23 040 |
| 9 | `display_bench.py` | 24 598 |
| 10 | `render_bench.py` | 15 925 |
| 11 | `direction_bench.py --display` | 15 629 |
| 12 | `exhaustion_bench.js` | 220 290 |
| | **TOTAL** | **1 250 369** |

Exactly the 1 250 369 the TZ names. All 12 steps exit 0.

---

## 1. Scope executed

All four stages executed as written. **No deviation from §2.** Two things are
reported below that the TZ did not anticipate and that were deliberately NOT
fixed: a release-checklist clause this TZ reverses (§11), and a caption
sentence that is now half false but which §2 B4 forbids changing (§12).

### Stage A — the constant

`index.html:729-733`, immediately after `var REG_STRESS_Z = 2.0;`:

```js
// The 90th percentile of the distribution of PER-DATE LIST MEDIANS of the
// day-range ratio (inv. 47), pinned to bench/exhaustion-calibration.txt
// (inv. 46). Its null p90 is 1.2393, so a reading at or above this line is a
// measurement of the day, not a probability.
var DAY_RANGE_ABNORMAL = 1.39;
```

The comment names the three required things and nothing else: the percentile of
the per-date list medians, the record it is pinned to, and the null p90 that
makes it a measurement rather than a probability.

`listExhaustion` (`index.html:1298-1310`):

```js
if (n < 8) return { median: null, n: n, abnormal: false };
...
return { median: med, n: n, abnormal: med >= DAY_RANGE_ABNORMAL };
```

`>=`, not `>`. The comparison lives in `listExhaustion` and in no other
function — proven by enumeration in §7 below.

### Stage B — one wording function, two surfaces

**B1.** The local `sqzNum(x)` is gone from `boardHtml`; `function numRu(x, d)`
is top-level at `index.html:2114`. All four former `sqzNum(` call sites now read
`numRu(…, 1)`. Board output stayed byte-identical on every scenario where the
day is quiet — 216 of 360 boards in §7 are byte-identical to `origin/main`,
which is the proof that the lift changed no bytes of its own.

**B2.** `dayStateNote(day)` at `index.html:2124`, declared next to
`regimeBanner`. Returns `''` on an absent day, `median === null`, or
`abnormal === false`; otherwise exactly one sentence, in `\uXXXX` escapes:

```
ДЕНЬ УЖЕ ВЫНЕСЕН — медиана списка <numRu(median,1)> обычного дня, порог <numRu(DAY_RANGE_ABNORMAL,2)>. Мера дня, не запрет.
```

**B3.** `regimeBanner` keeps its signature; its existing `<div>` is byte-for-byte
what it was, and a second `<div>` in the same shape is APPENDED in
`var(--accent)` when the note is non-empty.

**B4.** «РИСК ВЫНОСА» gains one `<div class="bd-kv">` after the list line and
before the `bd-note` caption, value span in `var(--accent)`. The `.bd-sec`
carries no inline `style`; the caption's own text is untouched.

### Stage C — the wiring

`index.html:3303`, immediately after `lastRows = rows;`, unconditional and above
the `sideOn` branch:

```js
reg.day = listExhaustion(rows);
```

The board keeps its own `listExhaustion(lastRows)` call unchanged.

### Stage D — the gate

`bench/exhaustion_bench.js` gains sections **I record**, **J threshold**,
**K live**, **L surfaces**; section **H** gains the `reg.day` reader/producer
contract; sections **C** and **E**, whose own comments predicted their
inversion, are inverted rather than deleted. Every counter is incremented at the
comparison site.

---

## 2. The constant's two sides, and the two D1 mutation controls

Section I reads both sides from disk at gate time:

```
=== I. The constant and the record it is pinned to (TZ-14 D1, inv. 46) ===
  index.html: 1.39   exhaustion-calibration.txt: 1.39   equal: true
  compared: 8
```

Asserted: exactly one declaration in the source; exactly one such line in the
record; the two equal as numbers; the source literal carries two decimals.

**Control 1 — delete the record.** `bench/exhaustion-calibration.txt` removed
from the working tree, bench re-run:

```
exit=1
  FAIL the calibration record is readable: …/bench/exhaustion-calibration.txt: got false want true
  FAIL calibration record missing or unreadable: …/bench/exhaustion-calibration.txt — ENOENT: no such file or directory
```

Non-zero, naming the missing file. Not a skip, not a fallback. File restored and
verified: MD5 `3b8730b254467c9df4c0a845a0f3cfb3`.

**Control 2 — set the source constant to `1.40`.** `index.html` mutated, bench
re-run:

```
exit=1
  FAIL source constant equals the record value: got 1.4 want 1.39
  index.html: 1.40   exhaustion-calibration.txt: 1.39   equal: false
```

Non-zero, naming both values. File restored and verified: MD5
`38d862bf3990b88dc8fcf5bc76d35015`.

---

## 3. The truth table

Built on a fixture family constructed so the production denominator
`cur * sigmaDay(vol) * sqrt(8/π)` is **exactly 1** (found by an ULP scan the
bench performs and asserts at run time), with `lo = 0`. Every ratio in the
double grid is then reachable, so the epsilons below are **one ULP** — the
smallest that exists. Each fixture is asserted to BE the case it claims before
its verdict is read (inv. 23).

| Case | median | n | `abnormal` | want |
|---|---|---:|---|---|
| 1 ULP below the threshold | `1.3899999999999997` | 9 | `false` | false |
| exactly at the threshold | `1.39` | 9 | `true` | **true** |
| 1 ULP above the threshold | `1.3900000000000001` | 9 | `true` | true |
| below quorum, n = 7 | `null` | 7 | `false` | false |
| empty list | `null` | 0 | `false` | false |

**Negative control.** The whole module body is re-evaluated in a second context
from a copy of the source with the declaration rewritten to `9.99`:

```
negative control: constant 9.99 -> median 2.4300 abnormal=false (real constant 1.39 -> abnormal=true)
```

The same list flips to `false`, so the comparison demonstrably reads the
constant and not a literal that happens to equal it. The control's
`dayStateNote` also prints `9,99`, so the sentence follows the constant too.

---

## 4. Banner prefix evidence, with the appended tail verbatim

All twelve (state × side) combinations compared against `origin/main`'s own
`regimeBanner`, loaded in a second context — 48 comparisons, 0 mismatches:

| state/side | no `day` field | `abnormal:false` | below quorum | `abnormal:true` is strict prefix + gains |
|---|---|---|---|---|
| unknown/long · unknown/short | identical | identical | identical | yes |
| stress/long · stress/short | identical | identical | identical | yes |
| overheat/long · overheat/short | identical | identical | identical | yes |
| trend+/long · trend+/short | identical | identical | identical | yes |
| trend−/long · trend−/short | identical | identical | identical | yes |
| range/long · range/short | identical | identical | identical | yes |

The appended tail is identical on all of them. Verbatim, once:

```html
<div style="margin:2px 0 8px;padding:6px 10px;border-left:3px solid var(--accent);font-size:0.82em;letter-spacing:0.04em;color:var(--accent);">ДЕНЬ УЖЕ ВЫНЕСЕН — медиана списка 2,4 обычного дня, порог 1,39. Мера дня, не запрет.</div>
```

The `margin`, `padding`, `border-left` width, `font-size` and `letter-spacing`
are copied from the regime line; only the colour differs, and the regime line's
own bytes are untouched — which is what the strict-prefix property proves.

---

## 5. Live path (inv. 48)

Section K runs production's own `update()` behind a recording DOM and takes the
output from the element the browser would paint. The two books differ by a
relative `1e-9` nudge of `highPrice` — seven orders of magnitude above the
round-trip noise of a ticker string, eleven below anything a `toFixed` on this
book can print.

```
long:  quiet median 1.389999998610 n=25 dayLine=false  |  loud median 1.390000001390 n=25 dayLine=true  |  rest identical: true
short: quiet median 1.389999998610 n=25 dayLine=false  |  loud median 1.390000001390 n=25 dayLine=true  |  rest identical: true
```

Removing the day line from the loud render reproduces the quiet render **byte
for byte** on both sides. Also asserted: `reg.day` carries the measure's shape;
`n = 25` equals the declared spot count, so the three `fut:true` tokens — given a
40-sigma range on purpose — never reached the measure; the day state is
identical in LONG and SHORT; and at `side === 'none'` `reg.day` is still
computed while no banner and no day line are printed.

Section H proves the same contract structurally, off the source text:

```
marketRegime + update() write reg: day, dir, eff, known, mode, z
regimeBanner reads reg: day, dir, known, mode, z
reg controls: deleted write named, added read named, clean source silent
```

One check per field read, and the three mutation controls: deleting
`reg.day = listExhaustion(rows)` reports exactly `[day]`; adding a read of
`reg.zzzNotWritten` reports exactly `[zzzNotWritten]`; the clean source reports
nothing.

---

## 6. Both surfaces (inv. 33)

```
sentence: ДЕНЬ УЖЕ ВЫНЕСЕН — медиана списка 1,4 обычного дня, порог 1,39. Мера дня, не запрет.
```

The card list (through the banner) and «РИСК ВЫНОСА» (through the real
`renderBoard`, over the same `lastRows` the list just produced) are compared as
STRINGS and carry the identical sentence, exactly once each. A quiet day
silences both — so «both print it» is not vacuous. The `.bd-sec` of the block
carries no inline `style`, and the caption still follows the sentence.

---

## 7. Enclosing sites of the identifier

Counted over CODE, with comments stripped by the same string/regex-aware state
machine `cutFunction` uses:

```
DAY_RANGE_ABNORMAL code sites: declaration=1, listExhaustion=1, dayStateNote=1  total=3  (comments included: 5)
```

Three sites, no fourth. Additionally asserted: `listExhaustion` carries exactly
one `>= DAY_RANGE_ABNORMAL` and no bare `>`; `dayStateNote` compares nothing
against it; and each of `regimeBanner`, `boardHtml`, `update`, `scoreCandidate`,
`tradeGeometry`, `leverageDecision`, `directionVerdict`, `liqPrice`,
`tierBadge`, `byScore`, `assignRanks`, `planLine`, `marketRegime` and `numRu` is
cut from the source and required to never name it.

---

## 8. No-regression — identity first (inv. 45)

**`prot_bench.js`'s unconditional identity run, before any other evidence:**

```
identity: 6 boards compared against index.html itself
PASS 372   FAIL 0
```

Zero differences.

**Whole-board differ against `origin/main`,** 360 boards over the full scenario
set — 10 list ratios × 3 list sizes × 2 sides × 6 leverage buttons, cycling
through five `cd` shapes, four money modes and four funding rates:

| | |
|---|---:|
| boards compared | **360** |
| byte-identical | **216** |
| differ ONLY in the day line | **144** |
| **differ anywhere else** | **0** |
| anomalies (day line where the median is below 1.39, or missing where it is at or above) | **0** |

Every differing board enumerated. The difference is always one inserted
`bd-kv`, immediately before the block's caption; the BEFORE is that same block
with the list line running straight into `<div class="bd-note">`. Five distinct
day lines across the 144:

| group | boards | list medians | ratios | list sizes | sides | levers | appended line |
|---:|---:|---|---|---|---|---|---|
| 1 | 48 | 1.3900, 1.3901 | 1.39, 1.3901 | 8, 25 | long, short | 2–7 | `…медиана списка 1,4 обычного дня, порог 1,39…` |
| 2 | 24 | 1.6000 | 1.6 | 8, 25 | long, short | 2–7 | `…медиана списка 1,6 обычного дня, порог 1,39…` |
| 3 | 24 | 2.0000 | 2.0 | 8, 25 | long, short | 2–7 | `…медиана списка 2,0 обычного дня, порог 1,39…` |
| 4 | 24 | 2.4300 | 2.43 | 8, 25 | long, short | 2–7 | `…медиана списка 2,4 обычного дня, порог 1,39…` |
| 5 | 24 | 4.0000 | 4.0 | 8, 25 | long, short | 2–7 | `…медиана списка 4,0 обычного дня, порог 1,39…` |

Each line in full has the shape:

```html
<div class="bd-kv" style="margin-top:0;"><span class="bd-k"></span><span class="bd-v" style="font-size:0.9em;color:var(--accent);">ДЕНЬ УЖЕ ВЫНЕСЕН — медиана списка 2,4 обычного дня, порог 1,39. Мера дня, не запрет.</span></div>
```

Ratio `1.3899` produced no day line and ratio `1.39` did, on the same
scenario grid; list size 3 (below quorum) produced none at any ratio. Every one
of the 144 sits on a list whose median is at or above 1.39, and none of the 216
identical ones does.

---

## 9. Purity (inv. 27), proven by perturbation

`hi24`/`lo24` scaled from ratio 1.20 (median 1.2000, `abnormal=false`) to ratio
3.60 (median 3.6000, `abnormal=true`), over a 25-coin board, on both sides.

Two claims are needed, because `hi24` is ALSO the entry anchor the direction
engine has read since long before this TZ:

**A — same rows, candidate vs `origin/main`.** For every coin: `sc.score`,
`vd.action`, `vd.why`, `dec.L`, `dec.binding`, `dec.moneyBelowMin`, `geo.rr`,
`inv.price`, the card's number, tier and rendered badge — all identical, at both
the quiet and the loud ratio, on both sides. The journal record that
`journal/write.js` would write, canonicalised by its own `canon`, is
byte-identical: 14 512 B on LONG, 18 362 B on SHORT, at both ratios.

**B — the perturbation moves the same things on both revisions.**

```
LONG : flipping abnormal moves fields [none] on the candidate and [none] on origin/main; journal [none] vs [none] — identical: true
SHORT: flipping abnormal moves fields [none] on the candidate and [none] on origin/main; journal [geo.wait] vs [geo.wait] — identical: true
```

The single mover, `geo.wait` on SHORT, is the entry-chase distance measured from
the 24h maximum — a pre-existing dependency of the direction engine on the 24h
range, present identically on `origin/main`. Nothing moves because of
`abnormal`.

**Fields compared: 1 658. Failures: 0.**

---

## 10. Extremes — all ten

`update()` threw in none. A board with no metrics printed no day line and no
`NaN`.

| # | Case | threw | n | median | `abnormal` | day line: list / board | NaN: list / board |
|---:|---|---|---:|---|---|---|---|
| 1a | slider at the low edge | no | 25 | 3.600 | true | yes / yes | no / no |
| 1b | slider at the high edge | no | 25 | 3.600 | true | yes / yes | no / no |
| 2 | null betas | no | 25 | 3.600 | true | yes / yes | no / no |
| 3 | truncated Gist (3 of 28) | no | 3 | null | false | no / no | no / no |
| 4 | HTTP 400 ticker (empty spot) | no | 3 | null | false | no / no | no / no |
| 5a | dead-market fields | no | 22 | 3.600 | true | yes / yes | no / no |
| 5b | no pair | no | 22 | 3.600 | true | yes / yes | no / no |
| 6 | missing coeffs fields | no | 25 | 3.600 | true | yes / — (board length 0) | no / no |
| 7 | absent `btcStats` | no | 25 | 3.600 | true | yes / yes | no / no |
| 8 | absent `volatility` | no | 0 | null | false | no / no | no / no |
| 9 | `E ≤ 0` | no | 25 | 3.600 | true | yes / yes | no / **yes** |
| 10 | non-finite `liq` | no | 25 | 3.600 | true | yes / yes | no / no |

Cases 3, 4 and 8 are the ones that matter for the new line: an unmeasured list
prints nothing at all. Case 6 renders no board (the row carries no metrics), so
there is nothing to print into. Case 9's `NaN` is the pre-existing §6.1 defect,
confirmed below and not fixed.

---

## 11. The 12-step gate on a runner

Candidate measured with the same harness as the baseline, twice (once
mid-implementation, once after every mutation control had been restored — both
runs reproduced identically).

| # | Step | Baseline | Candidate | Δ |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 |
| 3 | `prot_bench.js index.html` | 372 | 372 | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 255 708 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 |
| **7** | **`journal_bench.js`** | **691 109** | **691 109** | **0** |
| 8 | `catalyst_bench.js` | 23 040 | 23 040 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 15 925 | 15 925 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | 220 290 | 220 534 | **+244** |
| | **TOTAL** | **1 250 369** | **1 250 613** | **+244** |

**Step 7 reads 691 109, asserted unchanged.** This TZ writes no journal field,
and §9 above proves the journal record is byte-identical under the perturbation
that flips `abnormal`, so the zero there is a result and not a coincidence.

**The +244, term by term** (per-section counters from `exhaustion_bench.js`):

| Section | Baseline | Candidate | Δ | Why |
|---|---:|---:|---:|---|
| identity | 200 002 | 200 002 | 0 | untouched |
| nulls | 20 027 | 20 027 | 0 | untouched |
| quorum (C) | 65 | 65 | 0 | the six «permanently false» checks became six «follows the rule» checks — same count |
| venue (C1) | 25 | 25 | 0 | untouched; its list median 1.0 is still below the constant |
| banner (D) | 52 | 52 | 0 | the vacuous `#e0a02a` check became a one-div count — same count |
| stress (D2) | 51 | 51 | 0 | untouched |
| inert (E) | 30 | 120 | **+90** | 10 keys × 3 checks → 10 × 12: the quiet half kept both its checks, the loud half added 10 (prefix, appended, one closed div, amber, state word, median text, threshold text, «мера, не запрет», colour kept, same tail as every other state) |
| purity (F) | 22 | 36 | **+14** | `dayStateNote`: 5 silent shapes, speaks, deterministic, non-mutating, routes through `numRu`, `numRu` restored, and 4 `numRu` formatting cases |
| control (G) | 1 | 1 | 0 | untouched |
| wiring (H) | 15 | 31 | **+16** | H2, the `reg.day` contract: 2 extractor/non-empty, 5 one-per-field-read, 3 named-field, 6 controls |
| **record (I)** | — | 8 | **+8** | D1 |
| **threshold (J)** | — | 24 | **+24** | D2: family found + 2 fixture asserts, 5 truth-table rows × 3, 6 negative control |
| **live (K)** | — | 38 | **+38** | D4 live: 2 context, 2 sides × 16, 1 side-symmetry, 3 side-none |
| **surfaces (L)** | — | 54 | **+54** | D5: 14 both-surfaces, 40 site enumeration incl. the 14 functions required to stay silent |
| **SUM** | **220 290** | **220 534** | **+244** | |

`12 × exit 0`, `fails: 0` in every step.

**Runner run ids for `Bench gate`.** The gate was executed locally on this
runner (Node v22.22.2, Python 3.11.15) rather than on GitHub Actions, because
this session has no Actions execution available to it; the per-step table above
is that measurement, taken with the workflow's own step list and order. The
GitHub-hosted `Bench gate` will fire on push to `claude/execute-tz-14-47nul9`
(its `push` trigger names `claude/**`) and its run id must be recorded before
merge. **This is the one item of §5.10 that could not be closed from here, and
it is stated rather than papered over.**

---

## 12. `calib.yml` did NOT run; no new calibration record

`.github/workflows/calib.yml` fires on `push` to `claude/**` filtered to exactly
two paths:

```yaml
paths:
  - 'bench/exhaustion_calib.py'
  - '.github/workflows/calib.yml'
```

The complete diff of this branch against `origin/main` is:

```
bench/exhaustion_bench.js | 876 ++++++++++++++++++++++++++++++++++
index.html                |  95 ++-
2 files changed, 906 insertions(+), 65 deletions(-)
```

Neither filtered path is touched, so `calib.yml` cannot fire. No calibration was
re-run, and **no new calibration record was committed** —
`bench/exhaustion-calibration.txt` is byte-identical to `origin/main`
(MD5 `3b8730b254467c9df4c0a845a0f3cfb3`, 175 lines), including after both D1
mutation controls, which were restored and verified by MD5. The stale
`(TZ-11 stage B)` inside `calib.yml`'s hardcoded commit message is untouched.
The number 1.39 was not re-run, recomputed, rounded or cross-checked.

---

## 13. Release checklist 11, 15, 17 — re-run

26 assertions, 0 failures.

**Item 11 — direction engine.** No coin carries both ЛОНГ and ШОРТ; a card with
`action = 'none'` prints no entry or target line; the glyph agrees with the
verdict on every card.

**Item 15 — «РИСК ВЫНОСА».** The block is present, sits between «ВЫБОР ПЛЕЧА»
and «РАЗМЕР ПОЗИЦИИ», and is the **sixth numbered block** in the source
concatenation (asserted where inv. 15 puts the order, not from the rendered
header list, since the two alarms come and go with the fixture). Row 1 names the
pressed leverage on all six buttons. The list line names 25 coins, never zero.
The `.bd-sec` carries **no inline `style`** — the metal ring survives.

> **This checklist item now contains one clause TZ-14 deliberately reverses.**
> Item 15 reads «no threshold word appears anywhere in the block». The block now
> carries «порог 1,39», because §2 B4 requires exactly that. Measured: the board
> gains **exactly one** occurrence of «порог» versus `origin/main` (2 → 3), and
> that occurrence is inside «РИСК ВЫНОСА» (block 1 → 2; the block already
> carried «порога нет» in its caption). «ГРАНИЦЫ СДЕЛКИ», «ЦЕНА ВРЕМЕНИ» and the
> tier badge carry none, and the card list carries the sentence exactly once —
> so non-goal 5 holds. **The System Map was not edited** (§4 permits only
> `index.html` and `bench/exhaustion_bench.js`); the clause needs the
> Architect's amendment.

**Item 17 — the row contract.** A full board measures 25 coins, not zero;
removing `highPrice` from one ticker drops it to 24 and leaves the other cards
alone; `lastPrice` / `highPrice` / `lowPrice` are parsed at exactly one site per
field per row, and there is no other parse of the three range fields anywhere.

---

## 14. Compiles and guards

| Check | Result |
|---|---|
| `python3 -m py_compile main.py` | OK |
| `node --check` on the extracted `<script>` | OK |
| `node --check bench/exhaustion_bench.js` | OK |
| ES5 guard over every added line of `index.html` | **78 lines checked**, 0 violations |
| Cyrillic guard on `index.html` (new on-screen strings `\uXXXX`, new comments English) | **78 lines checked**, 0 violations |
| Cyrillic guard on added `bench/exhaustion_bench.js` code | **828 lines checked**, 0 raw-Cyrillic literals |

Both guards report the number of lines checked and would fail on zero.

---

## 15. Pre-existing issues — confirmed, not fixed

1. **`NaN% от входа` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ»** — **confirmed present**.
   Extremes case 9 renders it: `…<div class="bd-nd">NaN% от входа</div>…`, from
   `Math.abs(liq / E - 1)` with `E = 0`. Unreachable live. Not fixed.
2. **Raw Cyrillic literal in `bench/prot_bench.js`, line 177** — **confirmed
   present**, and still at line 177:
   `var inv = { … src: 'мин30', … };`. Not fixed. (The file's other Cyrillic is
   in trailing comment glosses beside `\uXXXX` literals, which is its
   convention, not the defect.)
3. **The Node 20 action pin in `bench.yml`** — **confirmed present**,
   `.github/workflows/bench.yml:50`, `node-version: "20"`, warning only. Not
   fixed.

### Newly found, reported and NOT fixed

4. **The §3.17 caption is now half false.** `index.html:2856` still reads
   «Число печатается как есть — **порога нет, сравнения нет**, на счёт, плечо и
   вердикт оно не влияет.» A threshold and a comparison now exist and print in
   the line immediately above it. The second half («на счёт, плечо и вердикт оно
   не влияет») remains true and §9 proves it. **§2 B4 states «The caption's own
   text does not change», so it was left exactly as it was.** It needs the
   Architect's decision.

---

## 16. Final line counts and MD5s

| File | Lines | MD5 | vs `origin/main` |
|---|---:|---|---|
| `index.html` | 3727 | `38d862bf3990b88dc8fcf5bc76d35015` | modified (was 3666 / `cef52cf6…`) |
| `bench/exhaustion_bench.js` | 1557 | `f8ecc6ea28e3f7cbf98ad72c259d8ec7` | modified |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | **unchanged** |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` | **unchanged** |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | **unchanged** |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1317 | `2309fcb1e656b70de350edbbb394135a` | **unchanged** |

`journal/**`, `bench.yml`, `.github/workflows/calib.yml` and
`bench/exhaustion_calib.py`: untouched. The count of gate steps is still 12.

---

## 17. Branch, compare URL, and one deviation from §7

- Branch: `claude/execute-tz-14-47nul9`
- Code commit: `d7bb102`
- Compare: `https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-14-47nul9`

**Deviation from §7, stated plainly.** §7 says this report goes «straight to
`main`», and that is the repository's established convention — the TZ-12 and
TZ-13 reports (`5e60f6f`, `d53a044`) are both first-parent commits on `main`,
landed ahead of their merges. **This report was committed to
`claude/execute-tz-14-47nul9` instead.** The executing session operates under a
standing instruction never to push to a branch other than its designated one
without explicit permission, and a direct write to the default branch is exactly
that. Nothing about the report's content or timing changed; only its landing
branch did. If the report is wanted on `main` ahead of the merge, that is one
cherry-pick — or it arrives on `main` with the merge itself.

**NOT IN EFFECT UNTIL MERGED.**
