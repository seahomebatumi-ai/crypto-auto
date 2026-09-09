# Implementation Report — TZ-37

## Status

COMPLETED.

All sixteen validation items ran. None was deferred, none was assigned to a dispatch,
and none is "not applicable". Item 15's step 5 failed locally; it is proven below to fail
identically on a pristine `origin/main` checkout with no TZ-37 edits in it, and **the same
step concluded `success` on the runner** (item 16) — which map §10 records as an
environmental ceiling rather than a product failure, and which the hosted run now
confirms independently.

The hosted `Bench gate` on the pushed branch concluded **`success`**, with every step
`success` and none `skipped`.

The previous TZ's branch WAS merged: `be25352 Merge pull request #32 from
seahomebatumi-ai/claude/tz-36-anchored-recorders` is an ancestor of `origin/main`, so this
work does not build on an unmerged base.

## Inbound Filing

None. The TZ arrived on `origin/main` already under its canonical filename
`CryptoTZ/TZ-37-lab-identity-partition.md` (§0 line 3), so nothing was moved or renamed.
No prior `CryptoTZ/**` file differs between the session's starting HEAD (`7f7b976`) and
`origin/main` (`f98a1aa`) — checked, because a TZ can be replaced in place under an
unchanged filename:

```
$ git diff --stat 7f7b976 origin/main -- CryptoTZ/
 CryptoTZ/TZ-37-lab-identity-partition.md | 398 +++++++++++++++++++++++++++++++
 1 file changed, 398 insertions(+)
```

## Scope Executed

**Class: branch TZ.** Read off the TZ's `## Scope`, not chosen: the scope names
`bench/backtest_bench.py` and `bench/backtest_guard_bench.py`, both outside
`CryptoReports/**`. A branch and a pull request therefore apply, and
`## Final Repository State` carries "NOT IN EFFECT UNTIL MERGED".

Stages A, B and C were all executed. No stage was blocked. No file outside the two
authorised ones was written, and no hard-floor item was reached: this TZ cites no
backtest and required no edit to any of the closed scoring, leverage, liquidation or
geometry functions. It changes what one control ASSERTS about numbers those functions
already produce.

## Files Created

None. The TZ authorises none, and none was created. No `bench.yml` wiring was therefore
required (hard floor item 12's second clause does not fire); the gate reaches this work
through step 14, which already runs.

## Files Modified

| File | Stage | Lines before → after |
|---|---|---|
| `bench/backtest_bench.py` | A, B | 4110 → 4258 |
| `bench/backtest_guard_bench.py` | C | 1140 → 1425 |

```
$ git diff --numstat origin/main
167	19	bench/backtest_bench.py
285	0	bench/backtest_guard_bench.py
```

Exactly the two in-scope files. `index.html`, `main.py`, `catalysts.json`,
`.github/workflows/**`, `.gitignore`, `SYSTEM-MAP-CRYPTOCALCUL.md`,
`EXECUTOR-INSTRUCTIONS.md`, `ANALYST-INSTRUCTIONS.md`, `journal/**`,
`bench/journal_bench.js`, `bench/verify_bench.py` and `bench/direction_bench.py` appear
in no diff — verified by filtering the diff's own file list, not by recollection.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### Stage A — the partition became a named module-level function

`d4_partition(dates) -> dict`, at `bench/backtest_bench.py:3468`, module level, directly
above `lab_selftest`. Signature and return keys as built:

| Key | Type | Meaning as implemented |
|---|---|---|
| `n_cmp`, `n_diff` | int | totals over the eight compared fields, on **exactly** D4's original construction — a presence mismatch is one comparison and one difference, a matched pair is eight of each |
| `n_still`, `n_moved` | int | matched pairs the chase rule did not fire on, and did |
| `still_diff` | int | field differences summed over the eight on `n_still` rows — the HOLD side |
| `moved_missing` | dict, keyed on `TGT_FLIP_F` | per field: `n_moved` rows that did NOT differ where the rule says they must |
| `moved_extra` | dict, keyed on `TGT_HOLD_F` | per field: `n_moved` rows that DID differ where the rule says they must not |
| `r_bad` | int | `n_moved` rows where `(R differs) != (first == "tgt")` |
| `r_tgt` | int | `n_moved` rows whose `first` is `tgt` — printed, never asserted |
| `miss_prod`, `miss_ident` | int | presence mismatches, by direction (see `## Deviations`) |
| `miss_bad` | int | presence mismatches whose direction disagrees with `o["adm"]` |
| `n_unclassed` | int | matched pairs carrying no `prod_anchor` |

The eight compared fields are named at **one** site (inv. 20) and split three ways:

```python
SAME_F     = ("first", "hit", "R", "p", "rr", "tgtSig", "a", "b")
TGT_FLIP_F = ("rr", "tgtSig")                    # measured at the anchor vs at E
TGT_HOLD_F = ("first", "hit", "p", "a", "b")     # the shared reference leg
TGT_COND_F = ("R",)                              # differs iff `first` is `tgt`
```

2 + 5 + 1 = 8: the eight stay eight. A module-level check raises at import if the three
tuples ever stop covering `SAME_F` exactly once each, so the guard runs on every import
including the gate's. `lab_selftest`'s `same_f`, which D8 reads, is now `same_f = SAME_F`
(`bench/backtest_bench.py:3934`) — D8 and D4 read the same tuple and not a copy.

The population test is READ, never re-derived: a row is «moved» when
`o["arms"]["prod_anchor"]["wait"]` is true and «still» when it is false. A matched pair
whose `prod_anchor` is absent is counted in `n_unclassed` and lands in NEITHER population
(inv. 21, 67).

### Stage B — D4 became the pair

**D4a**, the identity in the world where it holds. With the chase rule forced off the
anchor IS the current price, so `ident` must reproduce `prod` exactly. Asserts zero field
differences over all eight, zero presence mismatches, zero rows classified as moved, and
`n_cmp` non-zero.

**D4b**, the partition on the live path, over the existing `dA`. Passes when
`still_diff`, every `moved_missing`, every `moved_extra`, `r_bad`, `miss_bad` and
`n_unclassed` are all zero and both populations are non-zero. Four printed lines carry
every count, and a fifth `D4b ОТКАЗАЛА СТОРОНА:` line names which side failed and by how
much — a control that says only «СТОП» has localised nothing.

`miss_prod`, `miss_ident` and `r_tgt` are printed with the explicit annotation
`(без требования)`. No non-zero bar was placed on any of them: a world in which the
anchored pass changes no admission is a legitimate world, and a bar on it would be a bar
on the DATA rather than on the code (inv. 61).

### The D9 `want_identity` proof (item 6)

D9's anchor-off `run_target` call gained `want_identity=True` and moved to the D4 slot so
that D4a and D9 read one world; the TZ's §5 B1 forbids a third `run_target` over it. D9's
comparison, its bar and its printed line are untouched. Proven, not asserted:

```
baseline  D9 тождество ТЗ-36 (якорь погашен): сравнений 8829, расхождений 0, строк ожидания 0 ОК
final     D9 тождество ТЗ-36 (якорь погашен): сравнений 8829, расхождений 0, строк ожидания 0 ОК
$ md5sum on both lines → 953df8709d557a28e786f028b05cd00d  (identical)
```

Adding a substituted arm did not move a comparison between `prod` and `prod_anchor`. The
mechanism is visible in `TARGET_DRIVER`: the `subs` loop copies `j.cd` into a fresh `cdk`
per arm, and `prod` / `prod_anchor` are computed before `subs` is walked at all.

### Stage C — section G in the guard bench

`bench/backtest_guard_bench.py`, gate step 14, **63 comparisons**, all calling
`bb.d4_partition` by name on hand-built `dates` and comparing its return (inv. 21).
`requests` stays stubbed, no socket is opened, nothing is read from the archive.

**The section letter is `G`, and the `E` collision is real and was left alone.** The file
carries two sections lettered `E` — TZ-32's regime-gate arm at line 571 and TZ-34's venue
observation at line 813 — and only the second prints a section line. Neither was
renumbered, for the reason an invariant number never is: a section letter appears in the
immutable report of the TZ that created it. `F` is TZ-36's. `G` is the next free letter.

Checks 45–56. Beyond C2's eleven fixtures, section G asserts the three-way field split
(45), runs each fixture ALONE so that a bucket rising from zero is a measurement rather
than a comparison (46–53), proves the buckets compose over all eleven at once (54), and
proves a world of nothing but clean rows raises nothing at all (55) — without that last
one the section could be green because every fixture is red. A `g_zero()` helper asserts
the half of inv. 68 that is most often skipped: which buckets must NOT move.

## Validation

| # | Item | Result |
|---:|---|---|
| 1 | `py_compile` both files | **PASS** — exit 0 |
| 2 | diff names exactly the two in-scope files | **PASS** |
| 3 | fingerprint gate: anchor line numbers, map count/MD5, both bench figures | **PASS** |
| 4 | baseline `--lab-selftest` recorded before the first edit | **PASS** |
| 5 | D4a zero/zero/zero, `n_cmp` non-zero | **PASS** |
| 6 | D9's printed counts byte-identical after `want_identity=True` | **PASS** |
| 7 | D4b both populations non-zero, every defect bucket zero | **PASS** |
| 8 | reconciliation against map §3.10a, as a comparison and not a bar | **PASS** |
| 9 | negative control on the FLIP side | **PASS** |
| 10 | negative control on the HOLD side | **PASS** |
| 11 | D1, D2, D3, D5–D9 lines byte-identical | **PASS** |
| 12 | exit code and verdict line on both trees | **PASS** |
| 13 | gate step 14 count delta attributed to G; refuses on zero; no socket | **PASS** |
| 14 | every C2 fixture lands in its named bucket | **PASS** |
| 15 | full local `bench.yml` replay | **13 of 14 steps pass locally; step 5 fails identically on a pristine checkout and passes on the runner** |
| 16 | hosted `Bench gate` on the pushed branch | **PASS** — run #149, conclusion `success`, every step `success` |

## Test Results

### Item 1 — compilation

```
$ python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py
$ echo $?
0
```

### Item 3 — fingerprint gate

Every figure the TZ's §0 states was measured and matched. **The line number at which each
anchor matched is given, not a verdict that it did.** Each anchor matches twice: once in
the map's own `## 0` anchor table at lines 139–145, and once at the section it names.

```
$ grep -nF -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md | cut -d: -f1
```

| Anchor | Matched at lines |
|---|---|
| `**Revision 2026-09-09-a.**` | **17**, 139 |
| `### 3.12 Direction engine — veto cascade` | 140, **1058** |
| `### 3.15 Catalyst registry` | 141, **1435** |
| `### 3.16 List exhaustion — the day-range measure` | 142, **1532** |
| `## 11. Analytical engine` | 143, **2408** |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 144, **1699** |
| `69. **An identity control names the WORLD in which the identity holds.**` | 145, **2152** |

Contract: `EXECUTOR-INSTRUCTIONS.md` v20, 814 lines, MD5
`9a257890e9db663eb0fc74129f4841e0` — matches §0.

### Item 4 — the baseline, recorded before the first edit

```
$ cd bench && python3 backtest_bench.py --lab-selftest --html ../index.html --bot ../main.py
...
  D4 тождественный дифф: сравнений 7926, расхождений 1165 СТОП
...
ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить
$ echo $?
1
```

D4 was the **sole** red section on the unmodified tree. A, B, C, D1, D2, D3, D5, D6, D7,
D8 and D9 all read ОК. The lab exits 1 on an unedited tree and no push gate ever sees it,
exactly as map §3.10a and inv. 62 record.

### Items 5 and 7 — the pair, on the final tree

```
  D4a тождество в мире, где оно держится (якорь погашен): сравнений 7848, расхождений 0,
      пропусков присутствия 0, строк погони 0 (без погони 981, неклассифицируемых 0) ОК
  D4b деление на живом пути: сравнений 7926, расхождений 1165 · строк без погони 455
      (расхождений 0, должно 0) · строк погони 521 ОК
     на строках погони ОБЯЗАНЫ разойтись: rr · tgtSig — не разошлись: rr 0 · tgtSig 0
     на строках погони ОБЯЗАНЫ совпасть: first · hit · p · a · b — разошлись:
        first 0 · hit 0 · p 0 · a 0 · b 0
     R расходится тогда и только тогда, когда first==tgt: нарушений 0 (должно 0) ·
        строк с first==tgt 5 (без требования)
     присутствие: prod без ident 113 · ident без prod 5 (без требования) ·
        против adm 0 (должно 0) · неклассифицируемых пар 0 (должно 0)
```

Both populations non-zero (455 and 521). Every asserted bucket zero. `n_unclassed` is
**0** — no matched pair lacked `prod_anchor`, so the refusal path §4 A3 specifies was
never exercised on real data; it is exercised by fixture in section G check 53.

### Item 8 — reconciliation against map §3.10a, stated as a comparison

Map §3.10a's prior reading was taken by the Architect on the merged tree at revision
`2026-09-09-a`. This session took its own counts. **No numeral from the map appears in any
assertion; nothing was adjusted to reach it.**

| Quantity | Map §3.10a | This session | Agrees |
|---|---:|---:|:--:|
| comparisons, live path | 7 926 | 7 926 | ✓ |
| differences, live path | 1 165 | 1 165 | ✓ |
| rows the chase rule never fired on | 455 | 455 | ✓ |
| waiting rows | 521 | 521 | ✓ |
| presence mismatches | 118 | 118 | ✓ |
| — `prod` present, `ident` absent | 113 | 113 | ✓ |
| — `ident` present, `prod` absent | 5 | 5 | ✓ |
| field differences | 1 047 | 1 047 | ✓ |
| comparisons with the anchor forced off | 7 848 | 7 848 | ✓ |
| differences with the anchor forced off | 0 | 0 | ✓ |
| presence mismatches, anchor off | 0 | 0 | ✓ |

**No divergence.** There was therefore nothing to report as a finding under §3.

The reading also closes arithmetically against its neighbours, which is stronger than
agreement with a written number because nothing was fitted to it:

```
matched pairs        455 + 521 = 976;  976 × 8 = 7808;  + 118 presence = 7926 = n_cmp
field differences    1165 − 118 = 1047;  521 × 2 (rr, tgtSig) + 5 (R on first==tgt) = 1047
D8 vs D4b            D8 waiting 634 − D4b moved 521 = 113 = miss_prod
                     (D8's population is prod/prod_anchor; D4b's is prod/ident, so the 113
                      rows with no `ident` are presence mismatches for D4 and enter neither
                      population)
D8 still 455       = D4b still 455
D3 rung m=1 n=1089 = 455 + 634
anchor off           981 pairs × 8 = 7848 = D4a n_cmp;  981 × 9 = 8829 = D9 i_cmp
```

`r_tgt` = 5 and `miss_prod`/`miss_ident` = 113/5 are printed and carry no requirement.

### Items 9 and 10 — the two negative controls

Both were run in scratch copies under `/tmp/tz37/`, so the repository tree never carried
either defect. Full `--lab-selftest` in each case.

**Item 9 · FLIP side.** One line injected into `TARGET_DRIVER`, firing only on a waiting
row, so the anchoring is undone for `rr` and for nothing else:

```js
if (gP && g0) gP.rr = g0.rr;   /* ТЗ-37 item 9 INJECTED DEFECT */
```

| Reading | Clean tree | With the defect |
|---|---:|---:|
| `moved_missing['rr']` | 0 | **521** |
| `r_bad` | 0 | **5** |
| `still_diff`, `moved_extra[*]`, `miss_bad`, `n_unclassed` | 0 | 0 |
| D4b | ОК | **СТОП** |
| D4a | ОК | **ОК** |
| D8, D9 | ОК | ОК |
| verdict / exit | `измеряет то, что должна` / 0 | `НЕИСПРАВНА — результатам не верить` / **1** |

```
     D4b ОТКАЗАЛА СТОРОНА: сторона FLIP: rr не разошлось на 521 строках · R против first==tgt: 5
```

`r_bad` rising to 5 alongside is a real consequence and not noise: `R` IS `rr` on a
`first == "tgt"` row, so equalising `rr` also equalises `R` on exactly those 5 rows.
`n_diff` moves 1165 → 639 = 1165 − 521 − 5, which closes.

**Item 10 · HOLD side — the case the control exists for.** `prod`'s `a` computed from the
anchor instead of from `E`, i.e. the shared reference leg moved:

```python
"a": abs(math.log(tgt / (r["prod"]["anchor"] if key == "prod" else E))),
```

| Reading | Clean tree | With the defect |
|---|---:|---:|
| `moved_extra['a']` | 0 | **521** |
| `still_diff`, `moved_missing[*]`, `moved_extra[first/hit/p/b]`, `r_bad`, `miss_bad`, `n_unclassed` | 0 | 0 |
| D4b | ОК | **СТОП** |
| D4a | ОК | **ОК** |
| D8, D9 | ОК | ОК |
| verdict / exit | `измеряет то, что должна` / 0 | `НЕИСПРАВНА — результатам не верить` / **1** |

```
     D4b ОТКАЗАЛА СТОРОНА: сторона HOLD: a разошлось на 521 строках
```

This one flips **exactly one bucket and nothing else** — the partition inv. 68 asks a
negative control to name. `n_diff` moves 1165 → 1686 = 1165 + 521, which closes.

In both controls D4a stayed green, which is the point of the pair: with the chase rule
forced off the anchor is the current price, so neither injection can reach that world.
Both defects also left D8 and D9 green, confirming they are D4's to catch and nobody
else's.

**Revert.** Neither defect was ever applied to the repository tree; the scratch copies
lived outside it and were the whole of the injection.

```
$ md5sum bench/backtest_bench.py bench/backtest_guard_bench.py
11654488e2e5637c00fc9ae1f1880916  bench/backtest_bench.py
b42b660d3ede3196ba6c1c694d8f7fde  bench/backtest_guard_bench.py
$ git status --porcelain
 M bench/backtest_bench.py
 M bench/backtest_guard_bench.py
```

Only the two authorised modifications, taken after both controls had run.

### Item 11 — every other section is unchanged

Twenty printed lines — D1, D2 (with its three sub-lines), D3 (with its five ladder rungs
and three sub-lines), D5, D6, D7 (four lines), D8 and D9 — extracted from the baseline
capture and from the final tree and compared:

```
$ diff -u /tmp/tz37/b-other.txt /tmp/tz37/a-other.txt
$ echo $?
0        # IDENTICAL (20 lines compared)
```

No section other than D4 moved. Nothing turned red that was green, so there is no finding
to report under §2's "any other section turning red is a FINDING".

### Item 12 — exit code and verdict on both trees

| Tree | Verdict line | Exit |
|---|---|---:|
| baseline (`origin/main`, unedited) | `ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить` | 1 |
| final (this branch) | `ВЕРДИКТ ЛАБОРАТОРИИ: измеряет то, что должна` | 0 |

The verdict line itself was not edited. Its turning is an OUTCOME of D4 passing, and no
other section is red.

### Items 13 and 14 — gate step 14

```
$ python3 bench/backtest_guard_bench.py      # baseline, origin/main
checks run: 203   FAIL 0        exit 0

$ python3 bench/backtest_guard_bench.py      # final tree
E. venue-as-observation: 32 comparisons
F. anchored production arm: 29 comparisons
G. D4 partition: 63 comparisons
checks run: 266   FAIL 0        exit 0
```

Delta 266 − 203 = **63**, and section G reports 63 — the delta is attributed to G in
full, with nothing unaccounted. Check 56 refuses to pass on zero. No socket is opened:
`requests` remains stubbed and every section G fixture is a Python dict handed to
`d4_partition`.

Every C2 fixture was shown landing in its named bucket, each run in isolation so the
bucket rises from zero:

| Fixture | Required | Read |
|---|---|---|
| still row, all eight equal | `n_still`, `still_diff` unchanged | `n_still` 1, all buckets 0 |
| still row, one field different | `still_diff` rises | `still_diff` 1, nothing else |
| moved row differing in exactly `rr`, `tgtSig` | clean | `n_moved` 1, no bucket raised |
| moved row where `rr` is equal | `moved_missing['rr']` rises | 1; `tgtSig` 0 |
| moved row where `first` differs | `moved_extra['first']` rises | 1; `r_bad` 0 |
| moved row, `first=="tgt"`, `R` equal | `r_bad` rises | 1 |
| moved row, `first!="tgt"`, `R` different | `r_bad` rises | 1; `r_tgt` 0 |
| `prod` present, `ident` absent, `adm` true | `miss_prod` rises, `miss_bad` unchanged | 1 / 0 |
| `prod` present, `ident` absent, `adm` false | `miss_bad` rises | 1 |
| `ident` present, `prod` absent, `adm` false | `miss_ident` rises, `miss_bad` unchanged | 1 / 0 |
| matched pair with no `prod_anchor` | `n_unclassed` rises, lands in NEITHER population | 1; `n_still` 0, `n_moved` 0 |

Two fixtures beyond the required minimum: `ident` alone on a row `adm` says was admitted
(the second half of `miss_bad`'s biconditional, which the C2 list leaves untested), and
`moved_extra` for each of `hit`, `p`, `a`, `b` individually.

**The section was also proven able to fail** (contract §9 — a gate never proven to fail
is not a gate). Two defects injected into `d4_partition` in a scratch copy:

| Injected defect | Section G | Bench exit |
|---|---|---:|
| `moved_missing` stops incrementing | FAIL 3 (checks 49 ×2, 54) | **1** |
| an unclassifiable pair is defaulted into `n_still` | FAIL 5 (checks 53 ×3, 54 ×2) | **1** |
| reverted | FAIL 0 | 0 |

Printing a failure is not returning one (inv. 25, 29): the exit code was read, not the
screen.

### Item 15 — full local replay of `bench.yml`

**A local replay is not a runner run.** This is a local execution of the same commands
under `bash -euo pipefail`, on this session's machine, and it establishes nothing about
GitHub. The hosted result is `## CI Execution`.

| Step | Command | Exit | Checks reported |
|---:|---|---:|---|
| 1 | `node bench/verify_board.js` | 0 | — |
| 2 | `node bench/board2_bench.js` | 0 | — |
| 3 | `node bench/prot_bench.js index.html` | 0 | — |
| 4 | `python3 bench/verify_bench.py` | 0 | 40 |
| 5 | `python3 bench/direction_bench.py --props --fixtures --control --sim` | **1** | — |
| 6 | `node bench/fresh_bench.js` | 0 | — |
| 7 | `node bench/journal_bench.js` | 0 | 774 130 |
| 8 | `node bench/catalyst_bench.js` | 0 | — |
| 9 | `python3 bench/display_bench.py` | 0 | 24 598 |
| 10 | `python3 bench/render_bench.py` | 0 | 16 171 |
| 11 | `python3 bench/direction_bench.py --display` | 0 | 15 629 |
| 12 | `node bench/exhaustion_bench.js` | 0 | — |
| 13 | `bash analyst/live-gate.sh --selftest` | 0 | — |
| 14 | `python3 bench/backtest_guard_bench.py` | 0 | **266** |

Every step was run regardless of the previous one's result, so this table is not a gate
transcript: the hosted gate halts at the first red step and reports the rest as `skipped`.

**Step 5 is environmental and it is proven, not asserted.** The failure is a V8 heap
exhaustion inside the node child the bench spawns:

```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
node failed
```

Reproduced on a **pristine `origin/main` checkout carrying no TZ-37 edits at all**
(`git archive origin/main` into `/tmp/tz37/pristine`;
`md5sum bench/backtest_bench.py` = `8cca251ee28c5c9332c44405558cc339`, the §0 figure):

```
$ cd /tmp/tz37/pristine && bash -euo pipefail -c 'python3 bench/direction_bench.py --props --fixtures --control --sim'
exit=1     ...same FATAL ERROR, same `node failed`
```

The two outputs differ only in the node PID and in the millisecond GC timestamps; the
progress reached, the fatal error, the message and the exit code are the same. The machine
reports `Mem: 955 total, 329 available` (MB) and the kernel OOM killer has fired on this
box before. Map §10 records this ceiling as environmental, and this replay is consistent
with that record. **TZ-37 does not touch `bench/direction_bench.py`, which is on the TZ's
explicitly-not-authorised list and appears in no diff.**

## Deviations

**1. `miss_prod` / `miss_ident` — the TZ names them two contradictory ways, and §6 C2 was
followed.** §4 A1's gloss reads "presence mismatches, by which arm is ABSENT", which would
put a row with `prod` present and `ident` absent into `miss_ident`. §6 C2's fixture table
requires the opposite: "`prod` present, `ident` absent, `adm` true | `miss_prod` rises".
The two cannot both hold.

C2 was implemented, for three reasons stated so the Architect can overrule them cheaply:
C2 is the operative specification (it is the negative control, and validation item 14
checks against it); only the C2 reading makes `miss_bad`'s direction rule coherent, since
`prod` present implies `o["adm"]` true and `prod` absent implies it false; and the C2
reading is what reproduces map §3.10a's own 113 / 5 split, whose text describes the 113 as
"`prod` present with `ident` absent". Under A1's gloss the two counts would simply swap
names — no assertion changes, because `miss_bad` is computed from the direction itself and
neither count carries a bar. **The naming is the whole of the deviation; no reading is
affected.**

**2. `R` is asserted by `r_bad` alone and is in neither field dict.** §4 A2 gives `R` a
conditional rule while §4 A1 gives `moved_missing` and `moved_extra` unconditional ones, so
keying either dict on `R` would require a truth value the dict has no room for. `R` is
therefore `TGT_COND_F` and is asserted by `r_bad`, which is exactly what A1 specifies it
for. The eight compared fields stay eight: 2 (FLIP) + 5 (HOLD) + 1 (conditional), checked
at import and again by section G check 45.

**3. The `R` biconditional reads `prod`'s `first`.** `r_bad` evaluates
`(a1["R"] != a2["R"]) != (a1["first"] == "tgt")`. On a conforming row `first` is shared, so
the choice is invisible; on a row where it is not shared, `moved_extra['first']` already
fires, so no case escapes. `prod` is the reference arm and was chosen for that reason.

**4. D9's `run_target` call moved earlier inside `lab_selftest`.** §5 B1 requires D4a and
D9 to read the same `dates` and forbids a third `run_target`; D4 prints above D9, so the
shared world is now built in D4's slot. The call is otherwise unchanged apart from the
authorised `want_identity=True`, and D9's comparison, bar and printed line are byte-
identical (item 6). D4's own two lines sit in D4's slot, between D3 and D5, as before.

**5. `n_unclassed` read zero on real data**, so the §9 clause about a non-zero reading has
no referent. It is not a finding; it is the absence of one. The refusal path is exercised
by fixture instead (section G check 53), which is why that fixture is in the section.

## Pre-existing Issues

Neither was caused by this TZ, neither was fixed, and neither is in scope.

**1. `bench/direction_bench.py` under `--sim` exhausts the V8 heap on this machine.**
Proven above to fail identically on a pristine `origin/main` checkout. It is a property of
a 955 MB box, not of the repository. Reported, not repaired: `bench/direction_bench.py` is
on the TZ's explicitly-not-authorised list.

**2. Map §3.10's figure for gate step 14 is stale.** It reads "gate step 14, 94 checks";
the step ran 203 checks on `origin/main` before this TZ and 266 after. The drift predates
TZ-37 — sections E (TZ-34) and F (TZ-36) both added checks without the figure following.
`SYSTEM-MAP-CRYPTOCALCUL.md` is out of scope and was not touched.

**3. `bench/backtest_guard_bench.py`'s module docstring lists sections A–E only.** F
(TZ-36) was never added to it, and G was not added by this TZ either, so the list is
consistently one convention behind rather than newly wrong. Reported rather than
implemented (§6): the docstring is prose about the file's shape and belongs to whoever
decides the shape.

## Remaining Risks

**The `prod_anchor` archive figure is untouched by this work and remains outstanding.**
Map §10 carries it as `built, unmeasured`: the arm exists, is self-tested offline in
`--lab-selftest` D8/D9 and in gate step 14 section F, and now also has D4's partition
checking the leg it rests on. Taking the reading is a `backtest_bench.yml` dispatch —
`--fetch`, then `--target` — and is its own §10 row. This TZ did not take it, does not
predict it and did not wait on it. Nothing here forecasts what it will say.

**The lab's verdict is now `ИСПРАВНА` in substance**: `--lab-selftest` prints
`ВЕРДИКТ ЛАБОРАТОРИИ: измеряет то, что должна` and exits 0. Every section A, B, C and
D1–D9 reads ОК. The two TZs during which the lab declared itself unfit are closed.

**What this does and does not narrow.** D4's CONSTRUCTION now executes on every push
through gate step 14 section G, so a change that breaks the classifier is caught by a
push. D4's READING still requires a `backtest_bench.yml` dispatch, because the partition
needs a seeded world that takes minutes to build. Inv. 62 is narrowed by exactly the same
amount TZ-30's garrison narrowed it and no further: a stale construction is now caught on
every push; a stale reading still needs a dispatch.

**One judgement is load-bearing and is worth the Architect's eye**: the FLIP/HOLD split is
written into the code as a constant, derived from §3.10's prose rather than from
production at run time. That is what the TZ specifies (§4 A2, "written here and not
discovered at run time"), and it is the right call for a rule about which leg is shared.
But it is the class of object inv. 61 warns about, so if production ever moves another
field to the anchor, D4b will go red and the red will be correct — and the repair will be
a TZ moving the field between the two tuples, never a deletion from either.

## Commit

Implementation commit, made and pushed before this report was written:

```
e5b4bee7f49df3b58e6fe668344d9f2a22fec52f
TZ-37: D4 re-registered — anchor-off identity plus live partition, construction in gate step 14
```

Message verbatim from the TZ's `## Commit Message`. Contents: `bench/backtest_bench.py`
(+167 / −19) and `bench/backtest_guard_bench.py` (+285 / −0), and nothing else.

This report is committed separately, directly to `main` on the `CryptoReports/**` path.
That commit carries the message
`docs(reports): TZ-37 — lab identity, re-registered as a partition (TZ-37)` and no hash is
stated for it here.

## Pull Request

**No pull request exists.** This session has no `gh` CLI (`which gh` → absent) and no
GitHub token in its environment, so it cannot open one. This is the §8 fallback, not a
blocker and not a question for the Boss.

- Branch: `claude/tz-37-lab-identity-partition`
- Compare URL: https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-37-lab-identity-partition

The Boss opens and merges from that link in one action, after the Architect's audit
returns ПРИНЯТО.

## CI Execution

The branch was pushed and the hosted gate fired on it. Read from the runs API, which
answers unauthenticated:

| Field | Value |
|---|---|
| Workflow | `Bench gate` (`.github/workflows/bench.yml`) |
| Run number | **149** |
| Run id | 34338391916 |
| Head SHA | `e5b4bee7f49df3b58e6fe668344d9f2a22fec52f` |
| Event | `push` |
| Status | `completed` |
| Conclusion | **`success`** |

Read from the jobs API, the single job `bench` concluded `success` and **every one of its
steps concluded `success`** — none `skipped`, which matters because the gate halts at the
first red step and reports the rest as skipped:

```
JOB: bench | completed | success
    6 Доска 19.08 против продакшн-математики (verify_board.js)       success
    7 Доска 20.08, LONG + SHORT + два экрана (board2_bench.js)       success
    8 Блок «ЗАЩИТА ПОЗИЦИИ» + фаззинг доски (prot_bench.js)          success
    9 Офлайн-набор для --verify (verify_bench.py)                    success
   10 Движок направления (direction_bench.py)                        success
   11 Свежесть данных — пауза расписания против сбоя (fresh_bench.js) success
   12 Журнал вердиктов, офлайн (journal_bench.js)                    success
   13 Слой катализаторов (catalyst_bench.js)                         success
   14 Бейдж и нумерация карточек (display_bench.py)                  success
   15 Отрисовка списка целиком (render_bench.py)                     success
   16 Отображение и порядок (direction_bench.py --display)           success
   17 Истощение списка и баннер режима (exhaustion_bench.js)         success
   18 Ворота живых данных аналитика (live-gate.sh --selftest)        success
   19 Гарнизон бэктеста (backtest_guard_bench.py)                    success
```

Step 19 is the one carrying section G. **Step 10 is the step that failed locally**, and it
concluded `success` on the runner — which is the independent confirmation that item 15's
step 5 failure is a property of this session's 955 MB machine and not of the repository.
That is a measurement of the runner, not an inference from it.

**Per-step check counts are NOT claimed from the runner.** The logs endpoint answers 403
to a session holding no token (inv. 44), so the counts in item 15 are this machine's and
are labelled as such. What is claimed here is what the jobs API returns: status and
conclusion, per step. `backtest_bench.yml` is `workflow_dispatch` only and did not run;
this TZ requires no dispatch.

## Final Repository State

**NOT IN EFFECT UNTIL MERGED.**

The session leaves behind the branch `claude/tz-37-lab-identity-partition` at
`e5b4bee7f49df3b58e6fe668344d9f2a22fec52f`, pushed to
`origin/claude/tz-37-lab-identity-partition` and measured there. It carries two modified
files and no others. The working tree is clean: no `__pycache__`, no bridge scratch files
and no bench artifacts were committed — `backtest_guard_bench.py` removes the
`_*_bridge.js` files it creates, and every negative-control copy lived under `/tmp/tz37/`,
outside the repository.

## Fingerprints

`SYSTEM-MAP-CRYPTOCALCUL.md` — revision string `**Revision 2026-09-09-a.**`, **2628**
lines, MD5 `8388e3b1edf45cae4069c2d35b1f1ac9`. Matches §0 exactly.

`EXECUTOR-INSTRUCTIONS.md` — **v20**, **814** lines, MD5
`9a257890e9db663eb0fc74129f4841e0`. Matches §0 exactly.

The map's `## 0` file table at this revision — untouched by this TZ, all four unchanged:

| File | Lines | MD5 | vs §0 |
|---|---:|---|:--:|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | ✓ |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | ✓ |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | ✓ |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | ✓ |

The two benches this TZ edits, which have no row in that table by design — before and
after:

| File | Lines before | MD5 before | vs §0 | Lines after | MD5 after |
|---|---:|---|:--:|---:|---|
| `bench/backtest_bench.py` | 4110 | `8cca251ee28c5c9332c44405558cc339` | ✓ | **4258** | `11654488e2e5637c00fc9ae1f1880916` |
| `bench/backtest_guard_bench.py` | 1140 | `3b6ef587dd5e066c615300e530524aa9` | ✓ | **1425** | `b42b660d3ede3196ba6c1c694d8f7fde` |
