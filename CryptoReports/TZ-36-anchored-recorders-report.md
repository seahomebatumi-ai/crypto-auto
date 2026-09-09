# Implementation Report — TZ-36

## Status

**COMPLETED.** All four stages executed. Every validation item 1–17 was run and is
reported with its command and output; item 18 is assigned to the Boss dispatch by the TZ
itself and the report is not PARTIAL for it (TZ §7).

Two findings are carried and neither was caused by this work: `--lab-selftest`'s **D4 is
red on the unmodified tree** and has been since TZ-33 (`## Pre-existing Issues` 1), and
this session's machine cannot run gate step 5 (`## Pre-existing Issues` 2). Both are
proven against unmodified checkouts.

## Inbound Filing

None. `CryptoTZ/TZ-36-anchored-recorders.md` arrived on `origin/main` in commit `bab2e85`
under its canonical filename; nothing was moved or renamed.

The worktree was five commits behind `origin/main` when the trigger arrived and the TZ
was not present in it. `git fetch origin main` then `git merge --ff-only origin/main`
brought it to `bab2e85` before any assessment (contract §3).

## Scope Executed

**Class: branch TZ.** Read off the TZ's `## Scope`, which names four files outside
`CryptoReports/**` (contract §8). A branch and a pull-request path therefore apply, and
every clause in this report that speaks of a branch has a referent.

Executed: Stage A, Stage B, Stage C, Stage D — all four, in full.

## Files Created

None.

## Files Modified

| File | Stage | +/− |
|---|---|---:|
| `journal/write.js` | A, B | +56 / −3 |
| `bench/journal_bench.js` | A, B, D | +222 / −12 |
| `bench/backtest_bench.py` | C | +235 / −6 |
| `bench/backtest_guard_bench.py` | C | +169 / −0 |

Nothing outside this list was touched. `git diff --numstat` names exactly these four
paths, and `index.html` and `main.py` appear in no diff at all (validation item 4).

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### A0 — the fourteenth parameter

**The writer's call is already FOURTEEN arguments and no repair was needed.**
`journal/write.js:361-362`:

```js
const vd = P.directionVerdict(cd, token.s, token.name, cur, p24, qv, isLong,
                              reg, dec, hi, lo, rc7, tsMs, btcStats);
```

`cd · token.s · token.name · cur · p24 · qv · isLong · reg · dec · hi · lo · rc7 ·
tsMs · btcStats` — fourteen, with `btcStats` last, matching the signature at
`index.html:2040`.

It was TZ-33 itself that added it, in the same commit that created the second pass:

```
$ git diff a4225ca^ HEAD -- journal/write.js | grep -E '^[-+][^-+]'
-                                        reg, dec, hi, lo, rc7, tsMs);
+                                        reg, dec, hi, lo, rc7, tsMs, btcStats);
```

So the failure mode the TZ names first — a thirteen-argument call dropping the BTC
ceiling out of the anchored candidate set on waiting rows only — **does not exist in this
tree**. The baseline corpus carries 765 side blocks with `wait !== null`; had the call
been short, that is the population that would have been affected.

### The `invA` branch that fired

`inv` **is a hoist of `dec.inv`** — `journal/write.js` builds it as
`const g = vd.geo, iv = dec.inv;` and never calls `invalidationInfo` itself. The TZ's
first branch therefore fired: `invA` was added in the same place and by the same
construction,

```js
const dA = vd.decA, ivA = dA ? dA.inv : null;
```

so the record stays symmetric — `decA` is stored WITHOUT `inv` exactly as `dec` is, and
the anchored stop lives in the sibling `invA`, exactly as the cur-price stop lives in
`inv`. Where the TZ's Stage B rule says «`decA.inv.price`», the record's spelling of that
level is `invA.price`, and the resolver reads it there. Reading `side.decA.inv` would
have been a read of a field the writer never writes; it was caught while authoring
(`## Deviations` 2).

### Stage A — what the side block gained

`anchor` · `decA` · `invA`, appended after `inv`, following the writer's own stated
convention (schema names first in schema order, the rest after). `decA` is stored
unconditionally, including on `СЕЙЧАС` rows where it is `dec` object-identically.
`geo`, `dec` and `inv` keep their meanings and were not re-pointed; no record already
written was reopened.

### Stage B — what the outcome line gained

`sstop` (the numeric level the resolution used) and `ssrc` (`'decA'` or `'dec'`), per
side. The resolution rule:

```js
function stopUsed(side) {
    if (side && side.decA) {
        return { price: side.invA ? fin(side.invA.price) : null, src: 'decA' };
    }
    return { price: side && side.inv ? fin(side.inv.price) : null, src: 'dec' };
}
```

Presence of `decA` is the epoch test; the level is read from `invA`. **No outcome line is
written without `ssrc` in any branch**, including the defensive `!side` path, which routes
through the same helper. The horizon, the window, the touch semantics, `p0`, `p1`, `hi`,
`lo`, the `tgt`/`wait` touches and `first` are unchanged. No fill gate was added to the
journal.

### Stage C — the second production arm

`prod_anchor`, additive. Entry = the anchor; target = the same 90-day extremum; stop =
the anchored `inv.price`; fill = the anchor must be TOUCHED inside the horizon (a row the
chase rule never fired on is entered at once, because the anchor IS the current price);
window = fill hour → the SAME horizon end; outcomes = `tgt · stop · tie · никуда ·
unfilled`; Ω = `n_tgt / n_stop` over filled setups only, with `P(unfilled)` and
`P(никуда | filled)` beside it; bar = `1 / RR_MIN`, read from `index.html` at run time by
the existing `_read_js_num`, no numeral written here.

The shared reference leg was not touched: `stop`, `dist`, `b_log` and the `E`-based
resolution are byte-for-byte what they were, and `prod_anchor` computes its own levels and
calls `_touch_calc` a second time. The driver's new members live INSIDE `r.prod` rather
than at the top level, so guard-bench item 33 — which pins the driver's top-level key list
— is untouched and no bench assertion had to move for Stage C (`## Deviations` 3).

### Stage D — §0's open attribution

Closed, with a residual named. See `## Test Results` §D.

### B4 — the readers of `dec`/`inv`, enumerated by command

```
$ grep -rln --exclude-dir=.git -e '\.inv\.price' -e "\['inv'\]" \
    -e '\.long\.\(dec\|inv\)' -e '\.short\.\(dec\|inv\)' .
bench/backtest_bench.py   bench/direction_bench.py   bench/journal_bench.js
index.html   journal/write.js   SYSTEM-MAP-CRYPTOCALCUL.md   (+ CryptoTZ/, CryptoReports/)
$ grep -rn "journal/data\|journal/out" --include=*.js --include=*.py --include=*.sh --include=*.yml .
.github/workflows/bench.yml:30,31        # path filter entries, not reads
```

| Reader | Reads | Moves | Evidence |
|---|---|---|---|
| `journal/write.js` outcome layer | the stop level | **yes** — Stage B | the diff |
| `bench/journal_bench.js` | the side block's shape and leaves | **yes** — Stage A, D | the diff |
| `ANALYST-INSTRUCTIONS.md` §5 | `cd` and `btc` only | **no** | see below |
| `SYSTEM-MAP-CRYPTOCALCUL.md` §3.13 | the schema description | **no** — the Architect's | — |
| `bench/backtest_bench.py`, `bench/direction_bench.py` | their OWN `dec` from a production call | **no** | `grep -c journal bench/direction_bench.py` → `0`; `backtest_bench.py`'s two `journal` hits are comments |

`ANALYST-INSTRUCTIONS.md` **does** read `journal/data/YYYY-MM-DD.jsonl` — it is «the only
structural source this engine has» — and the methodology names exactly what it takes,
read from the file rather than from memory:

> `records   k:"s", one per covered coin. The structural objects are the row's `cd` — the
> bot's analysis_data row, verbatim and unrounded — and `btc`, which is coeffs.btc
> verbatim.`

`cd` and `btc` only. No side block, no `dec`, no `inv`. The row stands: **no move.**

## Validation

| # | Item | Result |
|---:|---|---|
| 1 | `node --check journal/write.js` | **PASS** — exit 0 |
| 2 | `node --check bench/journal_bench.js` | **PASS** — exit 0 |
| 3 | `python3 -m py_compile` on both Python benches | **PASS** — exit 0 |
| 4 | zero changed lines in `index.html`, `main.py` | **PASS** — absent from `git diff --numstat`; MD5s unchanged |
| 5 | A0 answered | **PASS** — fourteen arguments, before and after; 765 waiting side blocks in the baseline corpus |
| 6 | Baseline census D1 | **PASS** — taken on the unmodified tree before the first edit |
| 7 | Attribution D2 | **PASS with a FINDING** — reconstructed exactly by JSON path; D2's own terms do not close, residual named |
| 8 | Writer partition control | **PASS** — 1 567 anchored / 1 264 `СЕЙЧАС`, both non-zero |
| 9 | Negative control on item 8 | **PASS** — waiting assertion red 1 268×, every `СЕЙЧАС` assertion green, tree clean |
| 10 | Outcome epoch pair | **PASS** — `ssrc:'decA'` and `ssrc:'dec'`, no line without `ssrc` |
| 11 | D8 partition (TZ's «D7») | **PASS** — 455 / 634, both non-zero, 0 wrong on each side |
| 12 | D9 identity (TZ's «D8») | **PASS** — 8 829 comparisons, 0 differences, 0 waiting |
| 13 | `--lab-selftest` full run | **RUN; exit 1 on BOTH trees.** D1–D6 byte-identical to baseline. Exit 1 is the pre-existing D4 |
| 14 | Gate step 14 new section | **PASS** — 174 → 203, +29, all section F, no socket |
| 15 | Step 7 after the change | **PASS** — 691 836 → 774 130, attributed term by term, census increments nothing |
| 16 | Full local `bench.yml` replay | **RUN** — 13 of 14 steps green; step 5 red on this machine and red on a pristine HEAD |
| 17 | Reader enumeration B4 | **PASS** — every row justified by a command |
| 18 | `prod_anchor` archive reading | **ASSIGNED, NOT RUN** — Boss dispatch; outstanding, and nothing is forecast about it |

## Test Results

### A · Journal — step 7

```
$ node bench/journal_bench.js
--- проверок: 774130  провалов: 0 ---     (baseline: 691836, провалов 0)
  файлов 307, строк 8481 → 8487
```

**Delta +82 294, attributed term by term with zero residual.** The per-section split was
measured, not derived: two instrumented copies in `/tmp` (baseline and final) printing the
counter after every section.

| Term | Δ | Stage |
|---|---:|---|
| §1 field identity — `anchor`, `decA`, `invA` against a fresh production call: 5 500 records × 2 sides × 3 | +33 000 | A |
| §1 partition control — 1 567 anchored × 2 + 1 264 `СЕЙЧАС` × 3 | +6 926 | A |
| §1 population guards, 4 × `ok` | +4 | A |
| §2 key order — `decA`, `decA.parts`, `invA`, + the «a row with a non-empty `decA` exists» guard | +4 | A |
| §8g outcome-epoch fixture pair | +14 | B |
| §9a census neutrality guard | +1 | D |
| §7 numeric leaves — `anchor` 3 985 · `decA` 18 131 · `invA` 19 925 · `sstop` 66 | +42 107 | A + B |
| §7 numeric leaves added by the 8g fixture pair — 59 paths × 2 | +118 | B |
| §7 non-leaf — 4 new files × 4, 6 new rows × 4, the `ssrc` dictionary check on 36 × 2 outcome sides | +120 | B |
| **total** | **+82 294** | |

The §1 sub-terms are confirmed independently by the bench's own `cmps` counter
(192 500 → 232 426 = +39 926, plus the 4 `ok` guards it does not tally = +39 930, which is
exactly §1's measured delta). The §7 leaf terms are confirmed independently by a
numeric-leaf census aggregated by JSON path.

**D3 — the census increments nothing.** Enforced rather than promised: §9a captures the
counter before it walks the corpus and asserts it is unchanged after. That single guard is
the section's only check and is the `+1` in the table above. The assertions that moved the
counter are the ones Stage A and Stage B authorise and are named in every row.

### B · Item 8 — the writer partition, and item 9 — its negative control

```
ТЗ-36 деление: якорь ушёл 1567 (из них ожидание 501, стоп сдвинулся 1268) · якорь = cur 1264
```

Both populations non-zero. On every anchored row the stored `invA.price` equals
`P.invalidationInfo(cd, vd.anchor, isLong).price` computed at run time from `index.html`,
and production's `vd.decA` is a different object from `dec`. On every `СЕЙЧАС` row
`vd.decA === dec` object-identically, `anchor === cur`, and `invA` deep-equals `inv`.

The anchored stop differs from the cur-price stop on **1 268 of 1 567** anchored rows, not
all of them — so the control counts the divergence and asserts the count is non-zero,
rather than asserting a per-row difference that is not universally true.

**Negative control** (scratch copy in `/tmp`, writer inverted to store `dec` as `decA`):

| Assertion | Required | Measured |
|---|---|---|
| `якорь: invA.price = invalidationInfo при якоре` | **RED** | red, **1 268×** — exactly the rows whose stop moves |
| `ТЗ-36: сдвинутый якорь сдвинул и стоп` | **RED** | red, 1× |
| `СЕЙЧАС: invA совпадает с inv` | green | **green, 0 failures** |
| `СЕЙЧАС: anchor = cur` | green | **green, 0 failures** |
| `СЕЙЧАС: decA тождественен dec` | green | **green, 0 failures** |
| all four population guards | green | **green, 0 failures** |

The control flips exactly the rows the rule says must flip and nothing else. The scratch
copy lives entirely in `/tmp`; `git status --porcelain` on the worktree named only the
four in-scope files throughout.

### C · Item 10 — the outcome epoch

Section 8g builds two snapshots on one path: one carrying `decA`/`invA` (anchored stop 97
long, 103 short) and one from the pre-TZ-36 epoch carrying neither (stop 90 / 110). The
hour-6 candle spans 96–104, so it reaches the anchored stops and not the cur-price ones.

| | `ssrc` | `sstop` | `stop` touch |
|---|---|---|---|
| with `decA` | `decA` | 97 / 103 | hour 6 |
| without | `dec` | 90 / 110 | `null` |

Same path, same hour: the difference comes from WHICH level was read. Outcome lines
checked: 2; lines written without `ssrc`: **0**. The fixture stores `decA` **without**
`inv`, mirroring the record's real shape, so a resolver reading `decA.inv` would be caught
here.

### D · Stage D — §0's −2 059, and the residual

**Baseline census, taken on the unmodified tree before the first edit:**

| Term | Baseline (post-TZ-33) | pre-TZ-33 tree |
|---|---:|---:|
| `n_files` | 303 | 303 |
| `n_rows` | 8 481 | 8 481 |
| `n_side` | 13 486 | 13 486 |
| `n_wait` | **765** | **606** |
| `n_geonull` | **8 535** | **8 535** |

`n_files` and `n_rows` reproduce the map's «303 files, 8 481 rows» exactly. Both trees were
run in-session: the pre-TZ-33 tree is `git archive a4225ca^` with the current bench and
writer, and it reproduces the map's «was» figure to the digit.

```
pre-TZ-33 index.html : --- проверок: 693895  провалов: 0 ---
this tree, baseline  : --- проверок: 691836  провалов: 0 ---   Δ = −2059
```

**D2's stated arithmetic does not reconstruct it, and the residual is a finding.**

- **`n_geonull` contributes exactly ZERO.** It reads 8 535 on both trees. The term D2
  predicts — «a row whose second pass refused loses the whole `geo` object's leaves» —
  never fires: no row in this corpus lost its `geo` object at TZ-33.
- **`n_wait` is the wrong population and moves the wrong way.** It ROSE, 606 → 765.
  Predicting «one lost leaf per waiting row» gives −606 (or −765 read on the later tree)
  against an actual −2 059. **Residual: −1 453.**

**The measured reconstruction, by JSON path, closes exactly:**

| Path | pre-TZ-33 | post | Δ |
|---|---:|---:|---:|
| `s.long.geo.wait` | 870 | 4 | **−866** |
| `s.short.geo.wait` | 1 356 | 4 | **−1 352** |
| `s.long.wait` | 229 | 294 | **+65** |
| `s.short.wait` | 377 | 471 | **+94** |
| **total** | | | **−2 059** |

Total numeric leaves fell 464 270 → 462 211, which is the same −2 059: every one of those
checks is a section-7 leaf and nothing else moved.

**Why D2's terms miss it, named.** `side.wait` is `v.wait`, and production sets `v.wait`
at the END of the cascade — after the geometry veto and after the catalyst veto. The
population that actually lost a leaf is every row where PASS 1's `geo.wait` was non-null:
2 226 side blocks, of which 8 are hand-built fixtures, so **2 218 production rows** — 3.7×
`n_wait`. The gap is rows where the chase rule fired and the verdict then refused: they
carried `geo.wait` and never carried `v.wait`. The eight survivors are `handSnapshot`
fixtures in sections 8 and 9, not production output; the production corpus lost 100 % of
its `geo.wait` leaves, exactly as the termination property requires.

The `+159` runs the other way and is the second thing D2 does not model: since TZ-33 the
veto is evaluated ONCE, on the anchored geometry, so a coin refused at `cur` now reaches
the anchor before it can be refused — and `n_wait` rose while `geo.wait` collapsed.

**Stage A restores the observable D2 needed.** Post-change the census reads
`якорь сдвинут 2220`, of which 2 are the new 8g fixture pair → **2 218 production rows**,
which is precisely the pre-TZ-33 `geo.wait` population. The count of rows where the chase
rule fired was unreadable from a post-TZ-33 record and is readable again.

**Post-change census** (printed, never counted):

```
n_files 307 · n_rows 8487 · n_side 13490
n_wait 769 · n_geonull 8535 · якорь сдвинут 2220 · decA пуст 9481
 · decA есть, invA пуст 0 · сторон эпохи до ТЗ-36 24
```

`decA пуст 9481` equals the count of side blocks whose `geo` is null — a cross-check that
`v.decA` is null exactly when the verdict returned before the second pass — and
`invA пуст 0` says no anchored decision in this corpus produced a `decA` without an `inv`.

### E · `--lab-selftest` — D8, D9, and D1–D6

```
$ python3 backtest_bench.py --lab-selftest --html ../index.html --bot ../main.py
D8 деление ТЗ-36: строк без погони 455 (разошлись 0, должно 0)
                · строк ожидания 634 (не разошлись 0, должно 0) ОК
D9 тождество ТЗ-36 (якорь погашен): сравнений 8829, расхождений 0, строк ожидания 0 ОК
EXIT=1
```

**D8 (the TZ's «D7», the partition).** 455 rows the chase rule never fired on: all
bit-identical to `prod` across `first · hit · R · p · rr · tgtSig · a · b`, plus entry,
stop and resolution start hour — 0 diverged. 634 waiting rows: every one differs in at
least one of entry, stop or start hour — 0 failed to flip. Both counts non-zero, and a
line fires explicitly if either population is empty.

**D9 (the TZ's «D8», identity).** With the chase rule forced off on every row,
`prod_anchor` reproduces `prod` exactly: 8 829 comparisons, **0** differences, waiting
count **0**. The arm is not short-circuited under the flag — it runs its own fill gate,
its own window and its own resolver call and has to land on `prod`'s numbers.

**D1–D6 unchanged.** The diff between the baseline run and the modified run is exactly two
added lines:

```
$ diff <(grep -v замкнутость lab-baseline.txt) <(grep -v замкнутость lab-after.txt)
27a28,29
>   D8 деление ТЗ-36: ... ОК
>   D9 тождество ТЗ-36 ... ОК
```

Every D1–D7 line, including D4's counts and D3's whole ladder, is byte-identical between
the two trees.

### F · Gate step 14

```
$ python3 bench/backtest_guard_bench.py
F. anchored production arm: 29 comparisons
checks run: 203   FAIL 0          (baseline: checks run: 174   FAIL 0)
```

**+29, all of it section F**, which reports its own count and refuses to pass on zero — so
the delta is attributed by the section itself, not by arithmetic here. `requests` stays
stubbed and no socket is opened: the section's only outward call is `JsBridge`, which
builds and runs a local `node` bundle, exactly as items 32–33 already do.

Section F asserts the fill gate (first touching hour, refusal when never touched, the
long/short extreme convention), that the window ends at the ORIGINAL horizon (the same
touch inside `[0,50)` and outside `[0,30)`), that resolving from the fill hour ignores a
stop hit that happened before the fill, that `unfilled` is produced and counted apart from
«никуда» through `_anchor_pool`, that an arm which never filled reaches no quorum and
prints no Ω, and that the driver emits the anchor pair and honours `anchorOff`.

### G · Item 16 — full local replay of `bench.yml`

Each step under `bash -euo pipefail -c`:

| Step | Bench | rc | checks |
|---:|---|---:|---:|
| 1 | `verify_board.js` | 0 | 109 |
| 2 | `board2_bench.js` | 0 | 130 |
| 3 | `prot_bench.js` | 0 | 372 |
| 4 | `verify_bench.py` | 0 | 40 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | **1** | — |
| 6 | `fresh_bench.js` | 0 | 3 424 |
| 7 | `journal_bench.js` | 0 | **774 130** |
| 8 | `catalyst_bench.js` | 0 | 24 692 |
| 9 | `display_bench.py` | 0 | 24 598 |
| 10 | `render_bench.py` | 0 | 16 171 |
| 11 | `direction_bench.py --display` | 0 | 15 629 |
| 12 | `exhaustion_bench.js` | 0 | 220 598 |
| 13 | `live-gate.sh --selftest` | 0 | 40 |
| 14 | `backtest_guard_bench.py` | 0 | **203** |

**A local replay is not a runner run.** This table is thirteen local executions and one
local failure on a machine with 955 MB of RAM; what executed on GitHub is in
`## CI Execution`, and there step 5 is green.

**Reconciliation against the map's §0 gate total.** Excluding steps 5 and 7, the replay
sums to **305 803**; the map's own figures for the same subset — `1 253 347 − 255 708
(step 5, the map's arithmetic residual) − 691 836 (step 7)` — are **305 803**. Exact
match: every step except 7 reads what the map records, and step 7 is the only one that
moved.

Carrying step 5 forward at the map's residual, the gate becomes
`305 803 + 255 708 + 774 130 + 203 = 1 335 844`, a delta of **+82 323** on 1 253 521,
which is step 7's +82 294 and step 14's +29 and nothing else. **This is a local
measurement and the map's figure is the Architect's to set.**

## Deviations

1. **The two new lab controls are numbered D8 and D9, not D7 and D8.** The TZ specifies
   «two new controls beside D1–D6» and calls them D7 (the partition) and D8 (identity),
   but **`lab_selftest` already carries a D7** — the regime-gate partition control added
   by TZ-32, printed as `D7 деление по слову режима…` with sub-items D7a–D7d. Taking the
   TZ's numbers would have put two different D7s in one output and silently redefined an
   existing control, which «D1–D6 must be unchanged» plainly does not intend. The two
   controls are built exactly as specified — only the labels moved. The mapping is stated
   in the code beside them: **TZ «D7» = D8 (partition), TZ «D8» = D9 (identity).**
2. **A defect in this session's own Stage B, found and fixed before commit.** The first
   implementation of `stopUsed` tested `side.decA.inv` — a field the writer never writes,
   because A1's own `invA` clause hoists it out. On a real record that test always fails
   and the whole Stage B repair would have been a silent no-op. It was caught by making
   the 8g fixture mirror the record's real shape (`decA` without `inv`) rather than a
   convenient one, and the resolver now reads `invA`. Recorded because the fixture choice
   is what caught it and that choice is worth keeping.
3. **The driver's new members are nested inside `r.prod` rather than added at the top
   level.** Guard-bench item 33 pins the driver's top-level key list
   (`['dist','moneyBelowMin','ok','prod','reg','stop','subs']`); a new top-level key would
   have turned it red, and hard-floor item 2 forbids editing it. Nesting is also the
   truer place: the anchor is the production arm's own entry price. **No pre-existing
   bench assertion was moved for Stage C.**
4. **The item-8 partition asserts a COUNT of moved stops, not a per-row difference.** On
   1 567 anchored rows the anchored stop differs from the cur-price stop on 1 268 — a
   per-row assertion would have been false on 299 rows where `invalidationInfo` clips to
   the same structural level from both prices. The per-row invariant that IS universally
   true — the stored `invA.price` equals `invalidationInfo` at the anchor — is asserted on
   every anchored row, and the negative control turns exactly the 1 268 red.

## Pre-existing Issues

**1. `--lab-selftest`'s D4 is RED on the unmodified tree, and has been since TZ-33.**

```
D4 тождественный дифф: сравнений 7926, расхождений 1165 СТОП
ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить
```

Measured on the tree at `bab2e85` **before the first edit of this session**, with
`git status --porcelain` naming no modified file. The identical counts appear after the
change (`## Test Results` §E), so nothing here moved it.

The cause is the second site this TZ describes. `git log -S'decP = leverageDecision' --
bench/backtest_bench.py` returns exactly one commit — `a4225ca`, TZ-33 — which put
production's second pass into `TARGET_DRIVER`. Since then the `prod` arm's geometry is the
ANCHORED one while the `ident` arm substitutes the same target at `E`, so on a waiting row
the two are no longer identical and the identity control correctly refuses. **1 165 of
7 926 comparisons is the size of the waiting population.**

**This was invisible because `--lab-selftest` is not in the push gate.**
`grep -c lab-selftest .github/workflows/bench.yml` → `0`; it runs only under
`backtest_bench.yml`, which is manual dispatch. So the lab has reported itself
«НЕИСПРАВНА» on every dispatch since TZ-33 merged and no push ever surfaced it.

**Not fixed, and it is not fixable inside this scope.** The repair is either in
`index.html`/the `prod` arm's definition (explicitly not authorised) or in D4's assertion
(hard-floor item 2). It is named here for the Architect. Note that TZ-36's own D9 is the
identity control the arm it adds does pass, so the new arm is not affected by this.

**2. Gate step 5 cannot run on this machine.** `direction_bench.py --props --fixtures
--control --sim` exits 1 with `node failed` after printing its fixture rows. Reproduced on
`git archive HEAD` with none of this session's edits — **identical output, identical exit
code**. The machine has 955 MB total RAM with ~91 MB available, and the kernel log carries
`Out of memory: Killed process … (python3)`. It is the machine, not the repository: the
same step is **green on the runner** (`## CI Execution`).

**3. The map's §0 gate table has no row that a new section reads into.** Not a defect
found by this work, only a note: step 14's attribution («a new step has no was») now has a
«was» — 174 — and this change moves it to 203.

## Remaining Risks

1. **The `prod_anchor` archive reading is OUTSTANDING** and is a `backtest_bench.yml`
   dispatch — `--fetch`, then `--target` (TZ §5 C5, contract §7 item 9, map inv. 44). The
   arm is built and self-tested offline; **no figure for it exists and none is forecast
   here.** Until that dispatch runs, nothing is known about what the anchored arm says on
   the archive, and the standing `--target` numbers in map §3.10a are the OLD arm's and
   are unaffected.
2. **Step 7 rises 691 836 → 774 130** and step 14 rises 174 → 203. The map's §0 gate total
   and its per-step table will need both, and the runner is the authority for them; this
   session could not read the runner's counts (`## CI Execution`).
3. **The epoch boundary in the journal is now readable but is not uniform.** Every record
   written before this merges carries no `decA`, resolves through `ssrc:'dec'`, and by
   inv. 38 will never be repaired. Analysis that pools outcome lines across the boundary
   must split on `ssrc`, which is exactly what the field is for. Fourteen days of dates
   are on the old side of it.
4. **`decA` is stored on every side block and the corpus grows.** The journal is already
   the one unbounded artifact in the repository (map §3.13); this adds three fields per
   side block, and the measured effect on the bench corpus was +42 107 numeric leaves on
   13 486 side blocks — roughly three leaves per block. The daily record grows in the same
   proportion.
5. **D4's redness masks any future D4 regression.** While it stands red for the TZ-33
   reason, a second, different cause landing in D4 would not be distinguishable from the
   first without reading the counts.

## Commit

Implementation commit on `claude/tz-36-anchored-recorders`, pushed before this report was
written:

```
6c21e98  TZ-36: anchored recorders — journal anchor/decA, outcome ssrc, --target prod_anchor arm
```

Contents: `journal/write.js`, `bench/journal_bench.js`, `bench/backtest_bench.py`,
`bench/backtest_guard_bench.py` — four files, +682 / −21.

This report is committed separately, directly to `main` on the `CryptoReports/**` path
(§8). Its own commit and push have not happened as this section is written and no hash,
conclusion or outcome for them appears here.

## Pull Request

**No pull request exists.** `gh` is not installed in this environment
(`command -v gh` → empty) and this session has no credential to open one, so the contract's
§8 fallback applies.

- Branch: **`claude/tz-36-anchored-recorders`**
- Compare URL: **https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-36-anchored-recorders**

The Boss opens and merges from that link in one action, after the Architect's verdict.

## CI Execution

**The hosted gate ran on the pushed branch and it is green.**

| | |
|---|---|
| Workflow | `Bench gate` (`.github/workflows/bench.yml`) |
| Run | **#146**, id `34310999611` |
| Head SHA | `6c21e98` |
| Status / conclusion | `completed` / **`success`** |
| URL | https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/34310999611 |

All fourteen bench steps report `success`, **including step 5 (`direction_bench.py`), which
this session's machine cannot run** — which settles `## Pre-existing Issues` 2 as
environmental.

**The runner's own check COUNTS could not be read.** The logs endpoint answers
`403 Must have admin rights to Repository`, so this report states conclusions from the API
and takes every count from the local replay, labelled as such. No workflow other than
`Bench gate` executed: `backtest_bench.yml` is manual dispatch and was not dispatched, so
`--lab-selftest`, `--target` and the `prod_anchor` reading did not run on a runner.

## Final Repository State

**NOT IN EFFECT UNTIL MERGED.**

The session leaves behind the branch `claude/tz-36-anchored-recorders` at `6c21e98`,
pushed and measured, carrying four modified files and no new or deleted ones. The working
tree is clean apart from this report; every scratch artifact of this session — the
pre-TZ-33 tree, the instrumented profiling copies, the negative-control copy and the
replay driver — was created under `/tmp` and no generated file was committed.

## Fingerprints

`SYSTEM-MAP-CRYPTOCALCUL.md` — revision string **`**Revision 2026-09-08-b.**`**,
2 456 lines, MD5 `f0d0b2fb5e925409ba3cb64d7add6c18`. All seven content anchors the TZ
quotes are present as exact substrings.

**Gate table, measured on the baseline tree before any work — every file MATCHES.**

| File | Lines | MD5 | Required | |
|---|---:|---|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | 3799 / same | ✓ |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 / same | ✓ |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 / same | ✓ |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / same | ✓ |
| `bench/backtest_bench.py` | 3881 | `45e2294c5fc82f96a7e66b84c2a094c2` | 3881 / same | ✓ |
| `bench/backtest_guard_bench.py` | 971 | `19427e79133d48870d76eb0c908c69f6` | 971 / same | ✓ |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` | 388 / same | ✓ |
| `EXECUTOR-INSTRUCTIONS.md` | 814 | `9a257890e9db663eb0fc74129f4841e0` | v20, 814 / same | ✓ |

**`journal/write.js` and `bench/journal_bench.js` — measured, not declared.** Neither
carries a pin anywhere and none was invented; these are readings, so the next TZ touching
them has a baseline that was measured.

| File | Baseline lines | Baseline MD5 |
|---|---:|---|
| `journal/write.js` | **796** | **`d468b4502a8d6f4807f579ea9b8fc53f`** |
| `bench/journal_bench.js` | **967** | **`a973f4c52dfc45b3c8b86d25d6f6957e`** |

**After this change, on the branch** — recorded so the next reader can tell the two apart:

| File | Lines | MD5 |
|---|---:|---|
| `journal/write.js` | 849 | `19722fb53d75b6d25a8f957f74f97422` |
| `bench/journal_bench.js` | 1177 | `993271f44995c8ae21c54935a3f80adf` |
| `bench/backtest_bench.py` | 4110 | `8cca251ee28c5c9332c44405558cc339` |
| `bench/backtest_guard_bench.py` | 1140 | `3b6ef587dd5e066c615300e530524aa9` |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` (unchanged) |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` (unchanged) |
