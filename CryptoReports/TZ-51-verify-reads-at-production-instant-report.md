# Implementation Report — TZ-51

## Status

**COMPLETED.**

Every validation item of §6 was run on this session's checkout and every expectation
of §5 was met at the number it states, including both negative controls and, for the
one expectation §5 marks as a derivation rather than a replay, the underlying artifact
of run #25 itself.

The previous TZ's branch is merged: `claude/tz-50-agree-map-and-artifact-write`,
pull request #41, merged 2026-09-17T17:04:09Z (`gh pr list --state all`). This work is
not built on an unmerged base.

---

## Inbound Filing

None. `CryptoTZ/TZ-51-verify-reads-at-production-instant.md` arrived at its own
canonical filename in commit `a759eb9` ("Add files via upload") and needed no `git mv`.
No second copy exists anywhere:

```
$ git rev-parse --is-shallow-repository
false
$ git ls-files | grep -i 'tz.51\|TZ_51'
CryptoTZ/TZ-51-verify-reads-at-production-instant.md
$ git log --all --oneline -1 -- 'CryptoTZ/TZ-51*'
a759eb9 Add files via upload
```

The worktree was three commits behind `origin/main` when the session began and the TZ
was not present in it. `git fetch origin` brought `a759eb9` (the TZ plus map revision
`2026-09-22-b`), `3f5027f` and `b8f0dc4`; the worktree was fast-forwarded before any
measurement was taken, so every fingerprint below is against `a759eb9`.

---

## Scope Executed

**Class: branch TZ.** The `## Scope` of TZ-51 names three files outside
`CryptoReports/**`, so the class is read off the scope and not chosen: a branch and a
pull request are opened, and nothing but this report takes the `CryptoReports/**`
direct-push path.

Executed in full:

- §3 — three module-level helpers and one reading inside `reconcile()` in
  `bench/backtest_bench.py`, plus the §3.5 print and the §3.6 docstring replacement.
- §4.1 — case 12 (lanes P1–P6, 15 checks) in `bench/verify_bench.py`, inserted verbatim.
- §4.2 — section L (18 checks) in `bench/backtest_guard_bench.py`, inserted verbatim.
- §6 — all eight validation items.

Nothing outside §2's "Files to Modify" was touched. `main.py`, `index.html`,
`catalysts.json` and every workflow are byte-identical to `origin/main` (see
`## Fingerprints`), `backtest_bench.yml` included. `CMP_GAP_H`, the `SPEC` thresholds,
`CLASSES`, `HARD_CLASSES`, `_cell_comparable`'s code, `_cell_class`, `target_gate`,
`--attrib`, the fetch layer and the dispatch cache are unchanged. **No existing check in
either bench was edited, removed or re-registered** — proved by line counts, not asserted:
both bench diffs are additions only (`## Validation`, item 6).

---

## Files Created

None.

---

## Files Modified

| File | + | − | Hunks (`-U0`) |
|---|---:|---:|---:|
| `bench/backtest_bench.py` | 110 | 11 | 7 |
| `bench/verify_bench.py` | 103 | 0 | 1 |
| `bench/backtest_guard_bench.py` | 65 | 0 | 1 |

```
$ git diff --numstat origin/main...HEAD
110	11	bench/backtest_bench.py
65	0	bench/backtest_guard_bench.py
103	0	bench/verify_bench.py
```

---

## Files Renamed

None.

---

## Files Deleted

None.

---

## Implementation Summary

### What the change is

`reconcile()` compared production with `cdb.build(..., len(prices) - 1)` — the archive at
its LAST stamp — whatever the gap. A price is stamped at the END of its hour, so a
`coeffs.json` built at 10:50:25Z was compared against the archive's 11:00 value: ten
minutes of a violent hour standing in for a disagreement between two sources. The repair
reads the archive AT production's instant wherever the archive holds the bar that
contains it. No threshold, class, comparability rule or failing set moves.

### `bench/backtest_bench.py`

Three pure module-level helpers, placed together immediately before `_cell_dv` and after
`_gap_hours`, exactly as §3 requires:

- **`_enclosing(pts, t)`** (line 1751) — `(j_lo, j_hi)`, the stamps between which `t`
  lies; `(j, j)` where a stamp IS `t`. `None` where the archive does not hold the bar:
  after the last stamp, before the first, across an interior hole (`pts[j_hi] - pts[j_lo]
  > HOUR_MS`), or on an empty archive.
- **`_archive_at(cdb, P, V, t, cd_last=None)`** (line 1773) — the reading. One record on a
  stamp; inside a bar, four in §3.2's order: the windows ending at the two enclosing
  stamps, each with its own close, then each with the other stamp's close at its end.
  `cd_last` is returned as it was given and never rebuilt, so the run does not build the
  last window twice (inv. 20). Any element `None` makes the whole reading `None` — a
  partial span is not a span.
- **`_nearest(recs, k, b)`** (line 1812) — production's `b` where it lies inside the
  records' `[min, max]` for field `k`, else the bound it is outside. `None` where any
  record carries no number for `k`, judged by `_attr_num` — the module's one definition of
  a number.

In `reconcile()`, per symbol, immediately after `gap_sym`:

```python
at = None if gap_sym is None else _archive_at(
    cdb, ser["prices"], ser["volumes"],
    t_last + round(gap_sym * HOUR_MS), cd)
```

The instant is reconstructed from the one derivation of the gap and `generated_at` is
never parsed a second time (inv. 20). Per `SPEC` cell, after the existing `a, b` guard,
`an = _nearest(at, k, b) if at else None`, then `an = a` where `an is None`, then
`dv = _cell_dv(kind, an, b)`. **`"a"` keeps its meaning — the archive at its last close —
because `--attrib` raises when `rc["a"]` differs from its own build at the last bar**
(`backtest_bench.py:2241`); the new `"an"` is the value the comparison is taken from.
Both cell dicts gain `"an"`; each `rows` entry gains `"at": at is not None`.

Everything downstream of `dv` is untouched and reads the new `dv`: `_cell_comparable`,
`seen`, `worst`, `over`, the class, `sym_class`. `--target`, `--regime-gate` and `--attrib`
read the same classes and move with them; none of their code changed.

`verify_against_live()` prints, inside the same `if R["rows"]:` block and immediately
after `разрыв по монетам: …`:

```
архив прочитан в момент продакшна у %d монет · по последнему закрытию у %d
```

`_cell_comparable`'s docstring retires the sentence run #25 refuted. Its code did not
change.

### `bench/verify_bench.py` and `bench/backtest_guard_bench.py`

§4.1's case 12 and §4.2's section L were inserted **verbatim**, at the positions the TZ
names — case 12 immediately before the final `shutil.rmtree(tmp, …)` /
`shutil.rmtree(tmp_in, …)` pair, section L after section K's `print(...)` line and before
the final cleanup block. No condition and no check name was altered; nothing was
reformatted. The letter L is right off the file: the last section `backtest_guard_bench.py`
carried was K.

### The one formatting judgement, stated

The §3.5 format string is written as two implicitly-concatenated literals so the line
stays inside the file's own width. The printed string is byte-identical to §3.5's, which
is what `p_reading` asserts in four separate checks, and §6.5's grep target
(`архив прочитан в момент продакшна у %d монет`) remains on one line, as §6.5 requires.

---

## Validation

All eight items of §6 were run. Every command below was executed in this session and its
output is reproduced, not summarised.

### 1. Baseline, before any edit

```
$ python3 bench/verify_bench.py
checks run: 59   FAIL 0

$ python3 bench/backtest_guard_bench.py
E. venue-as-observation: 32 comparisons
F. anchored production arm: 29 comparisons
G. D4 partition: 63 comparisons
H. transport: 107 comparisons
I. attribution: 95 comparisons
J. gap in UTC: 8 comparisons
K. comparability: 11 comparisons
checks run: 488   FAIL 0
```

Both match §6.1 exactly. The §0 gate-table pairs measured before the first edit are in
`## Fingerprints` and match the TZ's table on all three files.

### 2. Compilation

```
$ python3 -m py_compile bench/backtest_bench.py bench/verify_bench.py bench/backtest_guard_bench.py
(no output — all three OK)
```

### 3. After the change

```
$ python3 bench/verify_bench.py
checks run: 74   FAIL 0

$ python3 bench/backtest_guard_bench.py
E. venue-as-observation: 32 comparisons
F. anchored production arm: 29 comparisons
G. D4 partition: 63 comparisons
H. transport: 107 comparisons
I. attribution: 95 comparisons
J. gap in UTC: 8 comparisons
K. comparability: 11 comparisons
L. reading at production's instant: 18 comparisons
checks run: 506   FAIL 0
```

74 and 506, with `L. … 18 comparisons` and sections E 32 · F 29 · G 63 · H 107 · I 95 ·
J 8 · K 11 unchanged — §5 rows 1 and 2, at the number.

### 4. Negative control

`_archive_at` was made to `return None` as its first statement, in the working tree, on
top of the committed implementation.

```
$ python3 bench/verify_bench.py
checks run: 74   FAIL 9
  FAIL: P1. production inside the last bar: exits 0  [exit=1]
  FAIL: P1. every symbol is clean  [{'AAA': 'unexplained', 'BBB': 'clean', 'CCC': 'clean'}]
  FAIL: P1. every compared cell of AAA reads exactly zero  [[('min_price', 0.0), ('max_price', 1.9607843137254966), ('min30', 0.0), ('max30', 1.9607843137254966), ('volatility', 16.783763932379973), ('vol7', 70.35034226893791), ('r7', 2.037232238921649), ('r14', 2.0259717425285872), ('r30', 2.096219040055658), ('eff14', 0.5550920243596904), ('vol_ratio', 0.0)]]
  FAIL: P1. the reading line names every symbol at production's instant  [СВЕРКА ПО МОНЕТАМ: AAA unexplained · BBB clean · CCC clean]
  FAIL: P2. a planted 5 pp is still red: exit 1, only the planted cell unexplained  [(1, {'venue-basis': [], 'coverage': [], 'unexplained': [('AAA', 'eff14'), ('AAA', 'r14'), ('AAA', 'r7'), ('AAA', 'vol7'), ('AAA', 'volatility')]})]
  FAIL: P2. measured from the bar: nearer than the last close, and still over its bar  [(0.05936076423925729, 0.05936076423925729, -0.011011558149959202, 7.037232238921649)]
  FAIL: P4. an instant on a stamp is read at production's instant  [СВЕРКА ПО МОНЕТАМ: AAA unexplained · BBB clean · CCC clean]
  FAIL: P5. the reading line names AAA at the last close  [СВЕРКА ПО МОНЕТАМ: AAA coverage · BBB clean · CCC clean]
  FAIL: P6. the start bar moved too: the other close at each window's end holds AAA, exit 0  [(1, {'AAA': 'unexplained', 'BBB': 'clean', 'CCC': 'clean'})]

$ python3 bench/backtest_guard_bench.py
L. reading at production's instant: 18 comparisons
checks run: 506   FAIL 2
  FAIL: L8. inside a bar: four records, each production's own build
  FAIL: L9. on the last stamp: one record, the caller's own and not a rebuild
```

`74 FAIL 9` — P1 ×4 (exits 0 · every symbol clean · AAA reads zero · reading line),
P2 ×2, P4 (reading line), P5 (reading line), P6 (exits 0). `506 FAIL 2` — L8, L9.
Both match §5 rows 3 and 4 exactly: the same counts and the same names, with no
additional failure and none missing.

Reverted, and the tree is clean for that file:

```
$ git checkout -- bench/backtest_bench.py
$ git status --porcelain -- bench/backtest_bench.py
(empty)
$ git status --short
(empty)
$ grep -c 'NEGATIVE CONTROL' bench/backtest_bench.py
0
$ python3 bench/verify_bench.py
checks run: 74   FAIL 0
$ python3 bench/backtest_guard_bench.py
L. reading at production's instant: 18 comparisons
checks run: 506   FAIL 0
```

The control also settles §5 row 5 as more than a claim: lanes P1 and P6 fail under the
old reading for exactly the reason run #25 failed, and their last checks — which pass
under **either** reading — prove each world really does put the last-close reading over
the `r7` bar, so neither lane is vacuous.

### 5. Grep evidence

```
$ grep -n 'def _enclosing(pts, t):' bench/backtest_bench.py
1751:def _enclosing(pts, t):
$ grep -n 'def _archive_at(cdb, P, V, t, cd_last=None):' bench/backtest_bench.py
1773:def _archive_at(cdb, P, V, t, cd_last=None):
$ grep -n 'def _nearest(recs, k, b):' bench/backtest_bench.py
1812:def _nearest(recs, k, b):
$ grep -n 't_last + round(gap_sym \* HOUR_MS)' bench/backtest_bench.py
1937:            t_last + round(gap_sym * HOUR_MS), cd)
$ grep -n 'архив прочитан в момент продакшна у %d монет' bench/backtest_bench.py
2046:        print("архив прочитан в момент продакшна у %d монет"
$ grep -n 'Hours DO move' bench/backtest_bench.py
1717:    `generated_at` (ТЗ-43 §3). A level is comparable at any gap. Hours DO move
$ grep -c 'hours do not' bench/backtest_bench.py
0
```

All six strings present, each on one line; the retired sentence is gone.

### 6. No-regression statement, with evidence

```
$ git diff --stat        (working tree, before the implementation commit)
 bench/backtest_bench.py       | 121 ++++++++++++++++++++++++++++++++++++++----
 bench/backtest_guard_bench.py |  65 +++++++++++++++++++++++
 bench/verify_bench.py         | 103 +++++++++++++++++++++++++++++++++++
 3 files changed, 278 insertions(+), 11 deletions(-)
```

`git diff --stat` names exactly the three files of §2 and no others.

```
$ git diff -- bench/verify_bench.py | grep '^-'
--- a/bench/verify_bench.py
$ git diff -- bench/backtest_guard_bench.py | grep '^-'
--- a/bench/backtest_guard_bench.py
```

The only `-` line in either bench is the file header: **both are additions only**, 0
deletions in `--numstat`. Every pre-existing check of both benches passes — the 59
checks of `verify_bench.py` and the 488 of the guard are unchanged in count and all
green in item 3, and the seven pre-existing guard section lines print their original
numbers.

Two further readings, not asked for by §6 but worth recording because they bound the
blast radius: `bench/exhaustion_calib.py` is the only other file in `bench/` that names
`backtest_bench`, and it is not a step of `bench.yml`; so steps 4 and 14 are the only
two whose counts can move, which is what §5 row 6 asserts.

### 7. The hosted gate

See `## CI Execution`. Both steps were read from the runner's own log.

### 8. Fingerprints

See `## Fingerprints`.

---

## Test Results

### The two gate benches

| Bench | Before | After | Expected by §5 |
|---|---|---|---|
| `bench/verify_bench.py` | `checks run: 59   FAIL 0` | `checks run: 74   FAIL 0` | 74 / 0 |
| `bench/backtest_guard_bench.py` | `checks run: 488   FAIL 0` | `checks run: 506   FAIL 0` | 506 / 0 |

Guard section lines after the change: E 32 · F 29 · G 63 · H 107 · I 95 · J 8 · K 11 ·
**L 18**. The first seven are the baseline's, unchanged.

### Gate total

§5 registers `1 336 148` → `1 336 181`. This was not taken on trust: the fourteen gate
steps were summed from the runner's own log of run `35704029320`.

| # | Step | Checks |
|---:|---|---:|
| 1 | `verify_board.js` | 109 |
| 2 | `board2_bench.js` | 130 |
| 3 | `prot_bench.js` | 372 |
| 4 | `verify_bench.py` | **74** |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 |
| 6 | `fresh_bench.js` | 3 424 |
| 7 | `journal_bench.js` | 774 130 |
| 8 | `catalyst_bench.js` | 24 692 |
| 9 | `display_bench.py` | 24 598 |
| 10 | `render_bench.py` | 16 171 |
| 11 | `direction_bench.py --display` | 15 629 |
| 12 | `exhaustion_bench.js` | 220 598 |
| 13 | `live-gate.sh --selftest` | 40 |
| 14 | `backtest_guard_bench.py` | **506** |
| | **Total** | **1 336 181** |

`1 336 181 − 15 − 18 = 1 336 148`, the map's own figure at revision `2026-09-22-b`. The
gate is 14 steps, as the map states, and only steps 4 and 14 moved.

### §5 row 7 — verified against run #25's artifact, not restated

§5 registers this row as "a derivation from printed terms, not a replay (the dispatch
cache is not saved)". The cache is indeed not saved, but **`attrib.txt` of run #25 is
still a live artifact** (`backtest-report`, artifact id `10637160776`, run
`35593262372`, `expired: false`), so the derivation was checked against the source
rather than repeated from the TZ:

```
coeffs.json built 2026-09-21T10:50:25 · gap to the newest archive hour -0.2 h
f two-point for r7   30 of 30 coins (one interior hour probed, field unchanged)
f two-point for r14  30 of 30 coins
f two-point for r30  30 of 30 coins
pop  coin    fld      g h        Δ    T_end  T_start  T_resid ...
fail TAO     r7      -0.2   -1.748   -3.136   -0.357   +1.744 ...
fail TAO     r14     -0.2   -1.571   -2.783   -0.321   +1.533 ...
fail TAO     r30     -0.2   -1.881   -3.309   -1.796   +3.225 ...
fail TAO     eff14 Δ -0.1055 · reproduction +0.0000 ...
```

Sign is production − archive. On all three horizons Δ and `T_end` carry the same sign
and `|Δ| < |T_end|`: −1.748 inside −3.136, −1.571 inside −2.783, −1.881 inside −3.309.
Production's value therefore lies strictly between the archive's value at its last close
(Δ = 0, which is `_archive_at`'s second record, `cd_last`) and the value the same window
takes with the previous close at its end (`T_end`, which is `_archive_at`'s **third**
record for a two-point field — and `attrib.txt` reports `f` two-point on 30 of 30 coins
for all three). `_nearest` returns `b` itself whenever `b` lies inside the span, so under
the new reading TAO's `r7`, `r14` and `r30` read **0.000 pp** and sit inside their 1.50 /
2.00 / 3.00 bars. The gap was −0.2 h, so production's instant lay inside the archive's
last bar and `_archive_at` returns a reading rather than `None`.

`verify.txt` and `target.txt` of the same run confirm the failure this repairs, from the
run itself:

```
verify.txt:1   coeffs.json собран 2026-09-21T10:50 · кэш кончается 2026-09-21T11:00 · разрыв -0.2 ч
verify.txt:59    unexplained    1   ПРОВАЛ
verify.txt:60        TAO     r7             +1.748
target.txt:1   СВЕРКА ПЕРЕД ЗАМЕРОМ: сверено монет 30 · исключено 1 · в рукава идёт 29
```

**This is a reading of run #25's printed terms, not a replay of run #25.** The dispatch
cache is not retained, so the four records `_archive_at` would build on TAO's real
archive cannot be constructed in this session; what is established is the inequality the
conclusion rests on, taken from the run's own artifact instead of from the TZ's
transcription of it.

---

## Deviations

None. Both check blocks were inserted verbatim, at the positions §4 names, and no
implementation was changed to satisfy a check.

One statement that is a formatting choice and not a deviation, recorded so the audit
does not have to derive it: §3.5's format string is written as two implicitly
concatenated string literals (line 2046–2047) to stay inside the file's line width. §4
permits formatting to follow the file; the printed string is byte-identical, which four
`p_reading` checks assert, and §6.5's grep target stays on one line.

---

## Pre-existing Issues

None found. Every file in the map's `## 0` table and every file in the TZ's gate table
measured at exactly the line count and MD5 stated, before the first edit. All seven
anchors of the map's own anchor table are present in the map as exact, case-sensitive
substrings and all seven are quoted character-for-character by the TZ header.

`bench/backtest_guard_bench.py` prints a `RuntimeWarning: All-NaN slice encountered`
from numpy on every run, before and after this change alike, and the bench is green in
both states. It is pre-existing, untouched by this work, and named here only so it is
not read as new.

---

## Remaining Risks

Both risks §7 states, restated because they are still true and neither is repaired here:

- **A positive gap is not reached.** Where production was built AFTER the archive's last
  close, no bar holds its instant, the reading stays at that close, and a violent hour
  can still turn a return cell red — the 09.09 shape at +0.8 h. Lane P3 is exactly this
  world and asserts the old behaviour deliberately. In run #25 five coins carried
  +10.8 h and were already out of the comparison on comparability grounds, which is a
  different rule and unaffected.
- **The reading is bounded by the enclosing CLOSES, not the bar's high and low.** A
  production value sampled at an intra-bar extreme beyond both closes still reads as a
  disagreement of that size.

One more, this session's own and outside §7: the four-record construction calls
`cdb.build` up to three extra times per symbol per reconciliation where production's
instant falls inside a bar, each on a fresh `_attr_swap` copy of the price list. On
`--verify`'s 30 coins this is not measurable against the fetch it follows, and both
gate benches run in the same seconds they did before (`verify_bench.py` 2.8 s → 3.3 s,
guard 4.9 s → 5.3 s). It is recorded because it is a cost that scales with the universe,
not with the change.

---

## Commit

Implementation commit, made and pushed before this section was written:

```
065ba72010841ce0267000f16118243e0e78460d
TZ-51: --verify reads the archive at production's instant
```

Contents: `bench/backtest_bench.py`, `bench/verify_bench.py`,
`bench/backtest_guard_bench.py` — and nothing else. The message is the string TZ-51's
`## Commit Message` gives, verbatim.

This report is committed separately on the `CryptoReports/**` direct-push path (§8). Its
authorised message is:

```
docs(reports): TZ-51 — --verify reads the archive at production's instant; 74/0 and 506/0, PR #42 (TZ-51)
```

---

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/42**

Branch: `claude/tz-51-verify-reads-at-production-instant`, base `main`.
Compare URL: https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-51-verify-reads-at-production-instant

Not merged, and not mine to merge.

---

## CI Execution

**`bench.yml` ("Bench gate") executed on a GitHub runner, twice, and both runs concluded
`success`.** These are runner executions, not local replays.

| Run id | Event | Conclusion |
|---|---|---|
| `35704029320` | `push` | success |
| `35704045239` | `pull_request` | success |

The push run fired because the branch name matches `bench.yml`'s `branches: [ main,
'claude/**' ]` filter and the changed paths — three files under `bench/` — are outside
its `paths-ignore` list.

Every step of run `35704029320` concluded `success` — the 19 job steps and the four
post/cleanup steps alike. The two steps TZ-51 moves, read from the runner's own log
(`gh run view 35704029320 --log`) — gate step 4 is runner step 9 and gate step 14 is
runner step 19, the offset being the five preamble steps the gate does not count
(`Set up job`, `checkout`, `setup-python`, `setup-node`, `Зависимости`):

```
Офлайн-набор для --verify (verify_bench.py)   checks run: 74   FAIL 0

Гарнизон бэктеста (backtest_guard_bench.py)   E. venue-as-observation: 32 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   F. anchored production arm: 29 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   G. D4 partition: 63 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   H. transport: 107 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   I. attribution: 95 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   J. gap in UTC: 8 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   K. comparability: 11 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   L. reading at production's instant: 18 comparisons
Гарнизон бэктеста (backtest_guard_bench.py)   checks run: 506   FAIL 0
```

The runner's numbers are the session's numbers, at every figure.

`backtest_bench.yml` did **not** run and was not triggered: it is `workflow_dispatch`
only, no line of it was touched, and a dispatch needs a warmed cache and the external
archive. `main.yml` did not run: its push trigger is a `paths` ALLOW-LIST of two literals
— `main.py` and `.github/workflows/main.yml` — verified in the workflow before this
report was pushed, with no `paths-ignore` beside it, so neither `bench/**` nor
`CryptoReports/**` can start the bot.

---

## Final Repository State

The branch `claude/tz-51-verify-reads-at-production-instant` is pushed and stands at
`065ba72010841ce0267000f16118243e0e78460d`, one commit ahead of
`origin/main` (`a759eb9`), carrying exactly the three modified files. The working tree is
clean apart from this report: no `__pycache__`, no bench scratch file and no artifact was
committed, and the negative control was reverted and proved gone.

**NOT IN EFFECT UNTIL MERGED.**

---

## Fingerprints

### `SYSTEM-MAP-CRYPTOCALCUL.md`

| | |
|---|---|
| Revision string in `## 0. Fingerprint` | `Revision 2026-09-22-b` |
| Required by TZ-51 §0 | `Revision 2026-09-22-b` — **match** |
| Lines | 2924 |
| MD5 | `48164d91da50acee233dcc810741cdd9` |

### Anchors

The list was cut from the map's own anchor table **by structure** — every row between its
`|---|---|` separator and the first non-table line — and not by matching anchor names.
**The table carries 7 rows; 7 were compared.** Each was confirmed as an exact,
case-sensitive substring of the map with `grep -oF`, which prints the matched text, and
each table row was confirmed present in the TZ header character-for-character.

| Anchor | In TZ header | In map | Text the match returned |
|---|---|---|---|
| revision | yes | yes | `**Revision 2026-09-22-b.**` |
| direction engine | yes | yes | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | yes | yes | `### 3.15 Catalyst registry` |
| exhaustion measure | yes | yes | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | yes | yes | `## 11. Analytical engine` |
| squeeze block | yes | yes | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | yes | yes | `72. **A write that fails leaves this run's product or nothing` |

### Files of the map's `## 0` table

Measured before the first edit and again after the last. **Unchanged by this work** — all
four are byte-identical to `origin/main`.

| File | Lines (map) | Lines (measured) | MD5 (map) | MD5 (measured) | |
|---|---:|---:|---|---|---|
| `index.html` | 3799 | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

### Files of TZ-51's own gate table (§0)

**Before the first edit** — all three match the TZ's table exactly:

| File | Lines | MD5 | TZ §0 | |
|---|---:|---|---|---|
| `bench/backtest_bench.py` | 5830 | `a1b1ce27773332e5630bba4189bd4d69` | 5830 / `a1b1ce27773332e5630bba4189bd4d69` | match |
| `bench/verify_bench.py` | 540 | `28eb1949f21d0afadb062303108f7101` | 540 / `28eb1949f21d0afadb062303108f7101` | match |
| `bench/backtest_guard_bench.py` | 2513 | `622b844efcca4292df2a157680ca4324` | 2513 / `622b844efcca4292df2a157680ca4324` | match |

**After the last edit**, at commit `065ba72`:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5929 | `ac203e2dc54104b79e08186644337832` |
| `bench/verify_bench.py` | 643 | `ec82368f44356c34c656ebcbcb5733da` |
| `bench/backtest_guard_bench.py` | 2578 | `101ec7304467ef966c661a1f5349ae14` |
