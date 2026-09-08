# Implementation Report — TZ-33

## Status

**COMPLETED.** All four scopes executed. All ten validation items ran; none was skipped
and none is reported "not applicable". Two items carry a red reading that is a property
of the world rather than of this change and is named as such: gate step 5 is red on
**both** sides of the replay (a V8 heap exhaustion on this machine), and no hosted
workflow conclusion could be read because this session has no GitHub API credential
(§9 — the report is not PARTIAL for that omission).

The previous TZ's branch **was merged**: `claude/tz-32-regime-gate-on-archive` landed as
pull request #29, merge commit `171b9d0`. This work is not built on an unmerged base.

---

## Inbound Filing

None. `CryptoTZ/TZ-33-entry-anchor-geometry.md` was already present on `origin/main`
under its canonical filename. No `git mv`, no rename, no duplicate copy.

```
$ git fetch --all --prune
 - [deleted]  (none) -> origin/claude/tz-32-regime-gate-on-archive
$ git rev-parse --is-shallow-repository
false
$ git rev-parse HEAD origin/main
e96aa1029a76325b3c1d24290c6f55db22a263f1
e96aa1029a76325b3c1d24290c6f55db22a263f1
```

---

## Fingerprint Gate (contract §5) — PASSED

Run against the repository copy on `origin/main` after fetching. Every anchor matched as
an exact substring; the revision string matched in both directions.

| Anchor | Required string | Result |
|---|---|---|
| revision | `**Revision 2026-09-06-a.**` | PRESENT |
| direction engine | `### 3.12 Direction engine — veto cascade` | PRESENT |
| catalyst registry | `### 3.15 Catalyst registry` | PRESENT |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | PRESENT |
| analytical engine | `## 11. Analytical engine` | PRESENT |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | PRESENT |
| newest invariant | `65. **A bar derived from the constant it judges moves with it.**` | PRESENT |

The map's `## 0` file table, measured on `origin/main` before any edit:

| File | Required lines | Measured | Required MD5 | Measured MD5 | Result |
|---|---:|---:|---|---|---|
| `index.html` | 3736 | 3736 | `dd39536d18cc1feb4839808e41e7bff4` | `dd39536d18cc1feb4839808e41e7bff4` | MATCH |
| `main.py` | 518 | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | MATCH |
| `catalysts.json` | 17 | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | MATCH |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | MATCH |

`bench/backtest_bench.py`, whose figure the TZ states in its own `§0` because the map's
table carries no row for it: **measured 3703 lines, MD5 `4d4242d37e63a01bdf74c474b3cfcb02`
— exactly the figure the TZ states.** The map's prose still carries TZ-30's 3240 /
`d2dad0f80afa2c191c2faf1d40081a88`; per the TZ's own `§0` that is a known map staleness,
recorded under `## Pre-existing Issues` and **not acted on**.

---

## Scope Executed

**Class: BRANCH TZ** (contract §8). The TZ's `## Scope` names files outside
`CryptoReports/**`, so the implementation goes to a branch and a pull request, and this
report goes directly to `main`.

All four scopes executed; none was blocked.

- **A — `index.html`, the anchored second pass in `directionVerdict`.** Signature gains
  `btcStats` as its last positional parameter. The body between the geometry call and the
  return is now, in order: first pass at `cur` used only to locate the anchor; `anchor =
  geo.wait` when the wait fired and `cur` otherwise; on a waiting row `decA =
  leverageDecision(cd, anchor, isLong, btcStats)` and `geoA = tradeGeometry(cd, anchor,
  isLong, decA, hi24, lo24)`, with **no second call made at all** when it did not fire;
  `v.geo = geoA` plus the additive `v.anchor` and `v.decA`; the veto evaluated **once, on
  `geoA`**; the catalyst check unchanged and after the geometry gate; `action = 'wait'`
  when the **first** pass set `geo.wait`, and `v.wait` still `geo.wait`. A null `geoA` is
  handled exactly as the existing `if (!geo)` branch handles the first pass — a refusal
  carrying the same reason, never a throw.
- **B — `index.html`, `planLine` reads the anchored objects.** The stop is
  `row.vd.decA.inv.price`. The `R:R` line was **verified, not rewritten**: it already read
  `row.vd.geo`, which scope A has made the anchored geometry. `row.dec` is untouched.
- **C — `bench/backtest_bench.py`, the target driver executes production's own sequence.**
  `TARGET_DRIVER` gains the same anchored second pass on the **production arm**; the `k`
  grid and the `rr` grid are unchanged.
- **D — comment and prose sites that describe the single pass.** Full enumeration below.

---

## Files Created

None. The TZ authorises none.

## Files Modified

| File | Scope | What moved |
|---|---|---|
| `index.html` | A, B, D | `directionVerdict` signature + body + header comment; `planLine` stop read + header comment; `tradeGeometry` header comment; the production call site at line 3351 |
| `bench/backtest_bench.py` | C, D | `TARGET_DRIVER` second pass on the `prod` arm; the `§10` header prose; the driver's "ONE decision" comment; `report_regime_gate`'s bar prose |
| `bench/direction_bench.py` | A (call sites) | six `directionVerdict` call sites |
| `bench/catalyst_bench.js` | A (call site) | one call site |
| `bench/journal_bench.js` | A (call site) | one call site |
| `bench/prot_bench.js` | A (call site) | one call site |
| `journal/write.js` | A (call site) | one call site — see `## Deviations` |

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### What was wrong, measured rather than restated

`directionVerdict` computed the whole trade at `cur` and then published an entry at
`geo.wait`. `invalidationInfo` clips its distance FROM AN ENTRY, so the published stop was
never protected by the `INV_FLOOR_SD` floor, and the ratio the veto read was a ratio at a
price the card did not name. Both consequences were reproduced against production's own
constants, with no market data — see `## Test Results` item 4 and item 5, plant B.

### Scope A — the two passes

```
    // Pass 1, at cur. Its ONLY product is the anchor: no veto is read here.
    var geo = tradeGeometry(cd, cur, isLong, dec, hi24, lo24);
    if (!geo) { v.why = 'нет геометрии'; return v; }

    var anchor = (geo.wait !== null) ? geo.wait : cur;
    var decA = dec, geoA = geo;
    if (geo.wait !== null) {
        decA = leverageDecision(cd, anchor, isLong, btcStats);
        geoA = tradeGeometry(cd, anchor, isLong, decA, hi24, lo24);
    }
    v.anchor = anchor;
    v.decA   = decA;
    if (!geoA) { v.why = 'нет геометрии'; return v; }
    v.geo = geoA;
    if (geoA.veto.length) { v.why = geoA.veto[0]; return v; }
```

**Termination is asserted, not commented** (validation item 6): `lim` inside
`tradeGeometry` is built from the 24-hour anchor and `inv.sd = sigmaDay(vol)`, neither of
which depends on `E`, so `lim` is identical in both passes and the second evaluates
`E > lim` at `E === lim`. Over 7 457 waiting rows, `geoA.wait === null` on every one and
the violation count is 0.

**No line inside any closed function moved.** Proved by cutting each body out of both
revisions by brace matching and hashing it:

```
tradeGeometry      528a0f85252b   528a0f85252b   UNCHANGED
marketRegime       e1025852a15f   e1025852a15f   UNCHANGED
invalidationInfo   be4c92182092   be4c92182092   UNCHANGED
leverageDecision   c3030f602ed0   c3030f602ed0   UNCHANGED
scoreCandidate     edd7958c4421   edd7958c4421   UNCHANGED
momentumScore      f962ffc81955   f962ffc81955   UNCHANGED
qualityScore       41490a443fc5   41490a443fc5   UNCHANGED
scoreFinish        4018392a7710   4018392a7710   UNCHANGED
protectionPlan     1349a5ee3b40   1349a5ee3b40   UNCHANGED
liqPrice           1dcb3c8f36ff   1dcb3c8f36ff   UNCHANGED
liqTouchProb       703bbf2919d0   703bbf2919d0   UNCHANGED
residual7          cef7b7792efa   cef7b7792efa   UNCHANGED
stateMark          9e2a0817560d   9e2a0817560d   UNCHANGED
verdictNote        69fff63c0f1b   69fff63c0f1b   UNCHANGED
byScore            143fa1d65545   143fa1d65545   UNCHANGED
assignRanks        d59514f3e2a9   d59514f3e2a9   UNCHANGED
catalystCheck      2e623ac89bf0   2e623ac89bf0   UNCHANGED
sigmaDay           6a5f99cb23f5   6a5f99cb23f5   UNCHANGED

directionVerdict   d2b7cc9ffa89   85d878f17abf   changed (scope A)
planLine           10f4d091d46d   6e8d0d2dfe63   changed (scope B)
```

`directionVerdict`'s baseline body hash `d2b7cc9ffa89…` is the same figure
`CryptoReports/TZ-04-freshness-truth-report.md` recorded for it, so the two revisions are
anchored to a published measurement rather than to this session's memory.

**ES5 and hard floor 7.** Every added code line was scanned for `=>`, `let`, `const` and
template literals: zero hits. Every added JS string literal was scanned for raw Cyrillic:
zero hits — the one Russian string touched (`СТОП`) is carried through unchanged as
`СТОП`. New comments are English, per the contract's language rule.

### Scope B — what the plan line prints

`row.dec` was not touched and gained no reader. The `R:R` line was verified rather than
rewritten. `СЕЙЧАС` rows print the same stop they printed before, because on a
non-waiting row `decA` **is** `dec`, object-identically — proved on 32 543 rows in
validation item 7.

### Scope C — the target driver

The production arm now performs the same second pass; `prod.g` is `armOut(gP)`. The `k`
grid, the `rr` grid, `stop`, `dist`, `b_log`, `mtm` and the first-touch resolution are
untouched, because the reference leg is shared with the substituted arms and moving it
would move those arms too. The consequence for the standing figures is recorded under
`## Remaining Risks`, not resolved.

### Scope D — the full enumeration (map inv. 50)

Six sites found, six repaired. Two more found that cannot be repaired inside this scope,
both named with the route that must close them.

| # | Site | What was false | Action |
|---|---|---|---|
| 1 | `index.html`, `tradeGeometry` header | said nothing about which price `E` is, while the function is now executed twice per waiting row | repaired — the header states that the caller decides `E`, that `directionVerdict` runs it twice, and that `dec` must be the decision taken at the same `E` |
| 2 | `index.html`, `directionVerdict` header | described one geometry pass | repaired — the two passes, the veto's single evaluation, the termination argument and the `row.dec` boundary are stated |
| 3 | `index.html`, `planLine` header | «стоп — тот же `dec.inv.price`, что печатает доска» | repaired — the stop is `vd.decA.inv.price`, with the reason and the `СЕЙЧАС` identity |
| 4 | `bench/backtest_bench.py`, `§10` header | «Both arms share ONE `leverageDecision`» | repaired — every arm still shares one decision at `E`; the production arm is the named exception |
| 5 | `bench/backtest_bench.py`, `TARGET_DRIVER` | «ONE decision per (date, coin, side): both arms get the same `dec`» | repaired — same correction inside the driver |
| 6 | `bench/backtest_bench.py`, `report_regime_gate` | «снятое с rr, который вернула НЕТРОНУТАЯ `tradeGeometry`: **погоня двигает вход**, и реализованный rr номинальному RR не обязан» — the conclusion survives but its stated reason does not: the production arm's rr is now taken AT the moved entry | repaired — the bar is named as taken at the anchor, and the surviving reason (the touch is still played from `E`) is stated. **Not anticipated by the TZ; found and repaired inside `§5`'s file list** |
| 7 | `bench/badge_bench.js` lines 179–207 | its `planLine` fixtures supply `dec: { inv: { price: 1.8 } }` and no `vd.decA`, and assert `pt.indexOf('$1.8000')` — an expectation that the stop is read from `row.dec` | **NOT repaired.** The file is outside `§5`'s `Modify` list and carries no `directionVerdict` call site, so validation item 3 does not reach it. It also **cannot run at all** — see `## Pre-existing Issues`. A TZ naming `bench/badge_bench.js` must repair it |
| 8 | `SYSTEM-MAP-CRYPTOCALCUL.md` inv. 35, «stop is `dec.inv.price`» | false for a waiting row after scope B | **NOT repaired.** The map is Architect-owned (contract §2, §7 item 14). Recorded here exactly as the TZ's `§6` requires; the map revision that follows this TZ closes it |

Two further sites were examined and found **not** falsified, and are recorded so a later
reader does not have to re-derive it: `index.html:724` (`ENTRY_CHASE_SD`'s comment — «вход
даётся не по цене сетапа, а по цене после движения» is still true, and is the defect this
TZ removes), and `index.html:2867` (the squeeze block's «стоп … читается из `dec.inv`» —
correct and unchanged, that block is a `currentLev` surface under inv. 14).

---

## Validation

Every item ran. Environment: node v22.23.1, Python 3.12.3, 1 CPU, 978 640 kB RAM.

### 1 — `python3 -m py_compile bench/backtest_bench.py`

```
$ python3 -m py_compile bench/backtest_bench.py && echo OK
OK
```
Also run and green: `python3 -m py_compile bench/direction_bench.py`, `python3 -m
py_compile main.py`.

### 2 — `node --check` on the `<script>` block extracted from `index.html`

```
$ node --check /tmp/tz33/script.js && echo OK        # 197 450 chars extracted
OK
```

### 3 — Call-site enumeration

`grep -rn "directionVerdict(" .` across the repository, then every call site's top-level
argument count measured by paren-matching rather than read by eye:

| File | Line | Args | Last argument |
|---|---:|---:|---|
| `index.html` | 2041 | — | *declaration:* `…, rc7, nowMs, btcStats)` |
| `index.html` | 3351 | 14 | `btcStats` |
| `journal/write.js` | 361 | 14 | `btcStats` |
| `bench/prot_bench.js` | 629 | 14 | `ctx.botData.btc` |
| `bench/journal_bench.js` | 241 | 14 | `btc` |
| `bench/catalyst_bench.js` | 589 | 14 | `BTC` |
| `bench/direction_bench.py` | 254 | 14 | `btc` |
| `bench/direction_bench.py` | 444 | 14 | `btc` |
| `bench/direction_bench.py` | 466 | 14 | `btc` |
| `bench/direction_bench.py` | 602 | 14 | `bat.btc` |
| `bench/direction_bench.py` | 746 | 14 | `btc` |
| `bench/direction_bench.py` | 875 | 14 | `bat.btc` |

**Call sites measured: 11. All 11 pass 14 arguments; none was left at 13.**

Two further matches are text, not call sites, and are correctly untouched:
`CryptoTZ/TZ-05-journal.md:155` documents the 13-argument signature and is immutable
evidence (contract §13); `CryptoTZ/TZ-33-entry-anchor-geometry.md:248` is this TZ quoting
the grep.

No bundle manifest needed a new name: `directionVerdict` appears in no
`backtest_bench.py` bundle, and every manifest that cuts it already cuts
`leverageDecision` (`bench/direction_bench.py` `FUNCS`) or executes the whole `<script>`
block in a sandbox (`journal/write.js`, `prot_bench.js`, `catalyst_bench.js`,
`journal_bench.js`, `display_bench.py`, `render_bench.py`). Verified by gate step 14
staying green at 142 checks.

### 4 — Known-answer control on the floor, derived at run time (inv. 61, 65)

Synthetic `cd` / `E` / `hi24` / `lo24` covering **both** configurations of the TZ's `§1`
table — the structural stop and the floored stop — on **both sides**, such that the wait
fires and the row is actually published by `planLine`. `INV_FLOOR_SD` and `sigmaDay` are
read out of the loaded `index.html` at run time and never typed into the check: the bar's
authority is `invalidationInfo`'s own clip, the object judged is the published entry.

The engine reproduces the TZ's `§1` table before anything is asserted: `sigmaDay(0.01) =
0.048990`, `ENTRY_CHASE_SD = 0.5`, anchor `= 100 × (1 + 0.5σ) = 102.4495`, and the four
`cur` values 109.7980 / 119.5959 / 114.6969 / 124.4949.

| Config | Side | Run | Anchor | Stop at anchor | σ from anchor | Stop at `cur` | σ of that stop from the anchor | R:R at anchor |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| structural | long | 2.0σ | 102.4495 | 92.4115 | **2.00** | 94.6240 | **1.56** | 3.74 |
| structural | long | 4.0σ | 102.4495 | 92.4115 | **2.00** | 94.6240 | **1.56** | 3.74 |
| structural | short | 2.0σ | 126.8157 | 139.2410 | **2.00** | 136.2578 | **1.52** | 6.99 |
| structural | short | 4.0σ | 126.8157 | 139.2410 | **2.00** | 135.2493 | **1.36** | 6.99 |
| floored | long | 3.0σ | 102.4495 | 92.4115 | **2.00** | 98.5260 | **0.78** | 3.74 |
| floored | long | 5.0σ | 102.4495 | 92.4115 | **2.00** | 98.5260 | **0.78** | 3.74 |
| floored | short | 3.0σ | 126.8157 | 139.2410 | **2.00** | 132.1598 | **0.86** | 6.99 |
| floored | short | 5.0σ | 126.8157 | 139.2410 | **2.00** | 127.0087 | **0.03** | 6.99 |

The four long rows land on the TZ's own 1.56σ / 0.78σ and 3.74, from a different
direction: the TZ derived them by hand, this run read them off the shipping functions.
The mirrored short is not symmetric (the geometry is multiplicative) and its worst case is
worse — **0.03σ against a floor of 2.0**.

Asserted, per row: `(anchor − stop_published) / anchor ≥ INV_FLOOR_SD × sigmaDay(vol) −
1e-12` for a long and the mirror for a short; that the chase rule fired; that `planLine`
actually printed the row; and that the printed `СТОП` string equals `fmtP` of the anchored
decision's price. **Published rows judged: 8 of 8 cases. 41 checks, 0 failures.**

### 5 — Negative control (inv. 23, 50)

The single pass was planted back into the working tree, three ways, and item 4 re-run each
time. `index.html` md5 before planting: `4e71da9badca3ccae85b656fdc3773e8`.

| Plant | What was put back | Result |
|---|---|---|
| **5A** | `planLine` reads `row.dec.inv.price` | **RED — 8 failures, exit 1.** Every one of the eight configurations: `the printed stop IS the anchored decision [$94.6240 vs $92.4115]`, `[$98.5260 vs $92.4115]`, `[$136.2578 vs $139.2410]`, `[$127.0087 vs $139.2410]` … |
| **5B** | the veto evaluated on the first pass | **RED — 10 failures, exit 1.** The rows disappear from the board rather than being published: `none / риск/прибыль 1:2.0`, `1:0.8`, `1:1.6`, `1:0.6` |
| **5C** | `decA` left at the current-price decision | **RED — 11 failures, exit 1.** The floor inequality itself goes red: `d=0.076384 bar=0.097980 (1.5592 sigma)`, `(0.7817 sigma)`, `(1.5198 sigma)`, `(1.3575 sigma)`, `(0.0311 sigma)` |

Plant 5B is worth reading twice. The four refusal strings it produces — **1:2.0, 1:0.8,
1:1.6, 1:0.6** — are the TZ's own **1.99, 0.82, 1.56, 0.60** column, printed by
production's veto rather than by the TZ's arithmetic. Two independent derivations landing
on the same four numbers.

Reverted; `index.html` md5 `4e71da9badca3ccae85b656fdc3773e8` — **identical**; item 4 green
again at **41 checks, 0 failures**. The working tree is clean (`git status --porcelain`
empty at commit time).

### 6 — Termination assertion (inv. 22)

Over 20 000 synthetic rows × 2 sides = 40 000 verdicts:

```
rows that reached pass 2: 10385 | waiting rows: 7457 | geoA compared: 7457
| geoA null (refused at the anchor): 0 | violations: 0
```

**Rows compared: 7 457, not zero. `geoA.wait === null` on every one.**

### 7 — Identity control (inv. 45)

Run first with the SAME revision on both sides, as the invariant requires, and only then
against the baseline.

```
same-revision comparisons: 320000, differences: 0
non-waiting rows: 32543 | field comparisons: 227801, differences: 0
                         | planLine comparisons: 32543, differences: 0
```

Compared per row: `action`, `score`, `why`, `wait`, `ch`, `note`, the whole `geo` object
by value, and the rendered `planLine` HTML. **Every non-waiting row is unchanged field by
field, and prints a byte-identical plan line.**

### 8 — Direction of the change, measured not asserted

```
rows compared             : 40000
none @cur -> wait @anchor : 259
wait @cur -> none @anchor : 35
unchanged                 : 39706
other transitions         : 0
(of the unchanged, wait->wait: 1990)
```

Both directions occur, as the TZ says they legitimately may. No row moved into or out of
`trade`: the `trade` state is the non-waiting state, and item 7 proves it byte-identical.

### 9 — Gate replay

`.github/workflows/bench.yml`'s fourteen steps, run locally against the unmodified
checkout first and then against the change. Every step's exit code is identical on both
sides.

| Step | Bench | Exit before | Exit after | Checks before | Checks after | Δ |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `verify_board.js` | 0 | 0 | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 0 | 0 | 130 | 130 | 0 |
| 3 | `prot_bench.js` | 0 | 0 | 372 | 372 | 0 |
| 4 | `verify_bench.py` | 0 | 0 | 35 | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | **1** | **1** | — | — | — |
| 6 | `fresh_bench.js` | 0 | 0 | 3 424 | 3 424 | 0 |
| 7 | `journal_bench.js` | 0 | 0 | 693 895 | 691 836 | **−2 059** |
| 8 | `catalyst_bench.js` | 0 | 0 | 24 692 | 24 692 | 0 |
| 9 | `display_bench.py` | 0 | 0 | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 0 | 0 | 16 171 | 16 171 | 0 |
| 11 | `direction_bench.py --display` | 0 | 0 | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | 0 | 0 | 220 598 | 220 598 | 0 |
| 13 | `live-gate.sh --selftest` | 0 | 0 | 40 | 40 | 0 |
| 14 | `backtest_guard_bench.py` | 0 | 0 | 142 | 142 | 0 |
| | **total of the thirteen that print a count** | | | **999 835** | **997 776** | **−2 059** |

**Step 14 must still build all four bundles closed** — it does, at 142 checks and exit 0,
byte-identical output on both sides. Scope C added `decP` and `gP` to the target driver
and both are declared in the driver, so `_assert_js_closed` still resolves every
identifier.

Nine of the fourteen step outputs are **byte-identical** on both sides (steps 1, 2, 3, 4,
6, 8, 9, 10, 12, 14). Step 13 differs only in a `mktemp` path. The three that carry a real
difference are all the same fact seen from three places, and none of them moved a check
counter (inv. 43: a section can change its census without changing its count):

**Step 7, attributed term by term** — the map requires this and warns that a fall is
never assumed benign, because a defect that nulls a field lowers it identically. The
journal's records were re-counted by JSON path on both revisions:

| Path | Before | After | Δ |
|---|---:|---:|---:|
| `k=s.long.geo.wait` | 870 | 4 | **−866** |
| `k=s.short.geo.wait` | 1 356 | 4 | **−1 352** |
| `k=s.long.wait` | 229 | 294 | **+65** |
| `k=s.short.wait` | 377 | 471 | **+94** |
| | | **net** | **−2 059** |

Every other path is unchanged; rows 8 481 → 8 481 and files 303 → 303 on both sides. The
two negative terms are validation item 6 appearing in the instrument: `side.geo` is now
the anchored geometry and its `wait` is null on every written row, where before it was the
first pass carrying the pullback price. The residual 4 + 4 are `journal_bench.js` section
8's hand-built snapshots, which call no production function and are revision-independent.
The two positive terms are validation item 8's `none → wait` direction: 159 more rows
reach `action === 'wait'` and therefore write a `wait` number. −2 218 + 159 = −2 059,
which is the observed delta exactly.

**Step 11**, check count unchanged at 15 629; its printed census moved
`ожиданий 772 → 899` and `серых 6988 → 6861`, with `торгуемых 192` unchanged.

**Step 5**, red on both sides; the `--props` section it does reach before dying reports
`ожиданий 13223 → 15418` and `отказов 104013 → 101818`, with `сделок 2764` unchanged.

The same signature in all three: refusals become waits, and nothing enters or leaves
`trade`.

### 10 — A local replay is not a runner run

**No workflow conclusion was read on GitHub, and none is forecast.** What is established:
the branch `claude/tz-33-entry-anchor-geometry` was pushed to `origin` (commit
`a4225cab8d32ed8fbab792777dbc2157b6e4ef2a`); `bench.yml` triggers on
`push: branches: [main, 'claude/**']`, which this branch name matches; and none of the
seven changed paths falls under its `paths-ignore` list (`journal/data/**`,
`journal/out/**`, `journal/runs.jsonl`, `analyst/state.json`, `analyst/live.json`,
`analyst/log/**`, `analyst/owner.json`, `**.md`). This session has **no `gh` CLI and no
GitHub API token** (`which gh` → not found), so the run id and its conclusion cannot be
read here; per contract §9 they are read by the audit, on the pull-request page.

`main.yml`'s trigger filter was re-read before the direct push of this report, as contract
§8 requires rather than assumes: it is still a `paths` ALLOW-LIST of exactly two literal
entries, `main.py` and `.github/workflows/main.yml`. Neither `CryptoReports/**` nor
`analyst/**` can start the bot.

---

## Test Results

| Control | Checks | Failures | Exit |
|---|---:|---:|---:|
| TZ-33 harness, items 4 + 6 + 7 + 8 | 48 | 0 | 0 |
| TZ-33 harness, item 4 alone | 41 | 0 | 0 |
| negative control 5A | 41 | **8** | **1** |
| negative control 5B | 26 | **10** | **1** |
| negative control 5C | 32 | **11** | **1** |
| item 4 after the revert | 41 | 0 | 0 |
| gate replay, 14 steps | 997 776 | 0 in 13 steps; step 5 red on both sides | 13 × 0, 1 × 1 |

The harness executes both revisions by cutting the `<script>` block out of the respective
`index.html` and running it in a real `vm` context (inv. 21): it re-implements no
production rule, and every number it judges is a return value of a production function
called by name. It is a session artifact under `/tmp` and is **not committed** — see
`## Remaining Risks`, item 3.

---

## Deviations

**One.** `journal/write.js` was modified, and `§5`'s third `Modify` clause reads «any
**bench** whose `directionVerdict` call site item 3 finds». `journal/write.js` is not a
bench: contract §2 classes it as *Journal code*.

It was modified anyway, and the reasoning is recorded here rather than resolved silently.
Validation item 3 is unconditional — «**Every call site moves with the signature**» — and
names the exact harm of not moving one: «A site left passing thirteen arguments receives
`undefined` for `btcStats` and silently drops the BTC-crash ceiling — a wrong number, not
a crash.» Leaving this site would put that wrong number into the journal, which inv. 38
makes an immutable instrument record. A reading of `§5` that produces a known-wrong number
in an immutable record, and fails the TZ's own item 3 while doing it, is not a reading the
specification can have meant; `§5`'s clause delegates the file list to item 3's grep and
the word «bench» is the Architect's expectation of what that grep would return. The change
is one argument, `btcStats`, which `sideBlock` already receives as a parameter.

This is reported, not asked about (contract §1: the Boss is never asked a technical
question). If the Architect reads `§5` the other way, the repair is a one-line revert.

---

## Pre-existing Issues

Each of these existed before this task, is proved to pre-exist, and **none was acted on**.

1. **`bench/backtest_bench.py`'s figure in the map's prose is stale.** Measured on
   `origin/main`: 3703 lines, MD5 `4d4242d37e63a01bdf74c474b3cfcb02`. The map's `## 0`
   prose carries TZ-30's 3240 / `d2dad0f80afa2c191c2faf1d40081a88`. The file has no row in
   the fingerprint table, nothing blocks on it, and the TZ names this as a known map
   staleness. Recorded, not acted on. After this change the file measures **3724 lines,
   MD5 `84b1572fd3af207b1e658f44f0191fcf`**.
2. **Gate step 5 is RED on this machine, on both sides of the replay.** `direction_bench.py
   --props --fixtures --control --sim` completes `СВОЙСТВА`, `РЕЖИМ` and `ФИКСТУРЫ` and
   then dies inside node with `FATAL ERROR: Reached heap limit Allocation failed —
   JavaScript heap out of memory`, at roughly 458 MB of a 978 640 kB / 1-CPU machine. It is
   red identically on the unmodified checkout, so it is a property of this environment and
   not of the change; the equality of the two readings is the evidence. This costs the
   replay step 5's check count, which is why the totals above are named as «the thirteen
   that print a count».
3. **`bench/badge_bench.js` cannot execute at all.** It loads `index.html.prev`, which is
   not in the repository; the bench is deliberately outside `bench.yml` for that reason,
   stated in the workflow's own header. Its `planLine` fixtures assert that the printed
   stop comes from `row.dec.inv.price` (lines 181–207), which scope B has made false. The
   file is outside `§5`'s `Modify` list and carries no `directionVerdict` call site, so
   this TZ may not repair it (hard floor item 2 also forbids editing a bench to make it
   pass). **A TZ naming `bench/badge_bench.js` must repair both facts together** — the
   missing baseline and the stale expectation — since repairing one without the other
   leaves an unrunnable bench with a correct assertion or a runnable bench with a wrong
   one.
4. **Map inv. 35 reads «stop is `dec.inv.price`».** After scope B the published stop on a
   waiting row is the anchored decision's. The map is Architect-owned and the Executor may
   not edit it; recorded here exactly as the TZ's `§6` instructs, to be closed by the map
   revision that follows this TZ.
5. **`CryptoTZ/TZ-05-journal.md:155` documents the 13-argument signature.** A TZ is
   immutable evidence (contract §13) and was correctly left alone. Named so the audit's
   grep does not read it as a missed call site.
6. **`§2B`'s account of `row.dec`'s readers does not match the code.** The TZ says
   `row.dec` «is the current-price leverage decision the card, the board and every leverage
   control are built on». Measured: `boardHtml` builds its **own** decision at
   `leverageDecision(cd, E, isLong, btcStats)` with `E = entryOf(sym) ? … : cur`
   (`index.html:2381–2383`), so the board has always recomputed at whatever entry it was
   given and has never read `row.dec`. After scope B, `row.dec` has exactly two mentions
   left in `index.html` — its own assignment at line 3350 and `directionVerdict`'s first
   pass at line 3352 — plus its readers in `journal/write.js` and the benches. **Inv. 14
   holds, and holds more strongly than the TZ's prose claims**, because the surface the
   Boss controls never depended on `row.dec` at all. A side effect worth naming: a Boss who
   types the published pullback price into the board now gets exactly the stop the plan
   line printed, where before the two disagreed.

---

## Remaining Risks

1. **Every `--target` and `--regime-gate` figure the map carries was measured on the
   single-pass production arm, and after scope C that arm is a different arm.** The earlier
   readings are not comparable to anything this driver will produce. Re-measuring needs the
   three-year archive and a warm cache, so it is a `backtest_bench.yml` dispatch and
   belongs to a later TZ — as `§2C` states.
2. **Inside the `--target` driver the production arm is now measured across two prices.**
   Its admission and its `rr` come from the anchor; `stop`, `dist`, `b_log`, `mtm` and the
   first-touch resolution still run from `E`. That is deliberate and forced: those five are
   shared with the `k` and `rr` arms, which `§2C` freezes, so moving them would move those
   arms too. The consequence is that the production arm's `R` has a numerator measured at
   one price and a resolution played from another. Named, not resolved; a TZ that
   re-measures the arm should decide this first.
3. **Validation items 4–8 are session controls and are wired into no gate step.** Inv. 37
   is explicit that a bench outside the gate is not a control: nothing in `bench.yml` will
   notice if the anchored pass regresses, and the floor control that turned red three ways
   in item 5 exists only in this session's `/tmp`. The TZ's `§5` says «**Create:**
   nothing», and hard floor item 12 forbids adding a bench file without wiring it into
   `bench.yml` in the same change — so no file was added rather than an unwired one. **A TZ
   authorising a gate step for the anchor floor is the remedy**, and it is the single
   largest gap this change leaves behind.
4. **The `geoA === null` branch is handled but unreachable, and no control exercises it.**
   Derived: `invalidationInfo` returns `null` only on `!has(vol) || vol <= 0 || !(E > 0)`
   or on a null / non-positive structural reference, and the first three do not depend on
   `E` while the reference is clamped to `E` when it would otherwise disqualify. Since the
   chase rule only fires when `anchor > 0`, a first pass that produced a geometry
   guarantees a second one that does too. 0 of 40 000 synthetic rows reached the branch.
   The guard stays because the TZ requires it; the report says plainly that it is defensive
   rather than tested.
5. **The journal's `side.geo.wait` has changed meaning without changing its schema.** It
   was the pullback price and is now null on every written row, because `side.geo` is the
   anchored geometry. The anchor is still recorded, at `side.wait`, unchanged. Records
   written before and after this change therefore carry the same field with two different
   meanings; nothing was added or removed, so no schema check can see it. `vd.anchor` is
   **not** written to the journal — the record's key list is asserted verbatim by
   `journal_bench.js` and adding a field is outside this TZ's scope.
6. **259 rows in 40 000 changed from `none` to `wait` and 35 the other way.** Both are
   legitimate, and the report states counts rather than a claim about them. What they mean
   in production is that the board will show more waiting cards and slightly fewer refusals
   the first time it loads after the merge; the `trade` state does not move at all.

---

## Commit

**Implementation commit — already made and pushed, so its hash is a measurement:**
`a4225cab8d32ed8fbab792777dbc2157b6e4ef2a` on branch
`claude/tz-33-entry-anchor-geometry`.

Message (first line): `TZ-33: trade levels are computed at the price the entry is
published at`. The TZ carries no `## Commit Message` section, so the message was composed
in the repository's established style and states what moved, what did not, and the
measured breach it removes.

Contents: `index.html`, `bench/backtest_bench.py`, `bench/catalyst_bench.js`,
`bench/direction_bench.py`, `bench/journal_bench.js`, `bench/prot_bench.js`,
`journal/write.js` — 112 insertions, 28 deletions across 7 files. No generated artifact was
committed; `bench/_*`, `bench/cache/` and `__pycache__/` are ignored and were left ignored.

**This report's own commit** carries the message `docs(reports): TZ-33 — the anchored
second pass in directionVerdict (TZ-33)` and no hash, no conclusion and no push result:
it has not happened when this section is written (inv. 54).

---

## Pull Request

**No pull request exists.** This session cannot open one — there is no `gh` CLI and no
GitHub API credential. Per contract §8's fallback:

- Branch: **`claude/tz-33-entry-anchor-geometry`** (pushed, tracking `origin`)
- Compare URL: **https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-33-entry-anchor-geometry**

The Boss opens and merges from that link in one action, after the Architect's verdict.

---

## CI Execution

**No workflow executed on a runner within this session's knowledge, and none is
forecast.** `which gh` returns nothing and no token is present, so no run id and no
conclusion could be read. What was established instead: the branch reached the remote, its
name matches `bench.yml`'s `claude/**` branch filter, and none of the seven changed paths
falls under that workflow's `paths-ignore`. The hosted result is on the pull-request page
and is read by the audit (contract §9).

Everything reported above under `## Validation` is a **local replay** of `bench.yml`'s
steps, run by hand in this session on the machine described in item 9. It is not a runner
execution and is not offered as one.

---

## Final Repository State

The session leaves behind the branch **`claude/tz-33-entry-anchor-geometry`** at commit
`a4225cab8d32ed8fbab792777dbc2157b6e4ef2a`, pushed to `origin` before this report was
written and therefore measured rather than predicted. Working tree clean
(`git status --porcelain` empty). Seven files modified, none created, none renamed, none
deleted.

**NOT IN EFFECT UNTIL MERGED.**

---

## Fingerprints

Contract documents, unchanged by this task:

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2268 | `52309e809bd0c540ae52afee15fa1b01` |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` |
| `ANALYST-INSTRUCTIONS.md` | 2615 | `e945ac9e93c03e72f551bc7972541148` |

Revision string carried by the map's `## 0. Fingerprint`: **`Revision 2026-09-06-a.`**

Files the map's `## 0` table lists, plus the file this TZ's gate table adds, measured on
`origin/main` before the change and on the branch after it:

| File | Lines before | MD5 before | Lines after | MD5 after |
|---|---:|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` | **3799** | **`4e71da9badca3ccae85b656fdc3773e8`** |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/backtest_bench.py` | 3703 | `4d4242d37e63a01bdf74c474b3cfcb02` | **3724** | **`84b1572fd3af207b1e658f44f0191fcf`** |

The other files this change touched:

| File | Lines before | MD5 before | Lines after | MD5 after |
|---|---:|---|---:|---|
| `bench/direction_bench.py` | 961 | `4fed3b1e1dcd8524bb26fd275d33b744` | 961 | `b176cea7b1ba1d62294a50d255d6057c` |
| `bench/catalyst_bench.js` | 614 | `12b4f5b29299b90b4eec6d7376bc6a7e` | 614 | `c3537368c0699b3df0391b36bbe82d4f` |
| `bench/journal_bench.js` | 967 | `4d59fdda46868ab357f406c6c39e8ae8` | 967 | `a973f4c52dfc45b3c8b86d25d6f6957e` |
| `bench/prot_bench.js` | 795 | `b2764444c6ee15cb491168cdca644d76` | 795 | `b61b009810e091823d2734990d1cfceb` |
| `journal/write.js` | 796 | `25f732ebdfd9efaf13077cf6e4afe2a9` | 796 | `d468b4502a8d6f4807f579ea9b8fc53f` |
