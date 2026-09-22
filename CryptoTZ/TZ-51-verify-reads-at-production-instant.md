# TZ-51 — `--verify` reads the archive at production's instant

**Canonical filename:** `CryptoTZ/TZ-51-verify-reads-at-production-instant.md`
**Report:** `CryptoReports/TZ-51-verify-reads-at-production-instant-report.md`
**Class:** branch TZ — it authorises three written files outside `CryptoReports/**` (contract §8).
**Model:** Opus — a classifier change asserted by two gate benches, with a known-answer world per edge.

---

## 0. Required System Map fingerprint

Quoted in full from `SYSTEM-MAP-CRYPTOCALCUL.md` `## 0. Fingerprint` (contract §5).
**Required revision string:** `Revision 2026-09-22-b` — the map uploaded together with this file.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-22-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**TZ gate table** — the three files this TZ moves, at the pairs the Architect measured on the
copies it wrote this specification against (contract §10: «any file the TZ's gate table adds»).
Measure each before the first edit and after the last:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5830 | `a1b1ce27773332e5630bba4189bd4d69` |
| `bench/verify_bench.py` | 540 | `28eb1949f21d0afadb062303108f7101` |
| `bench/backtest_guard_bench.py` | 2513 | `622b844efcca4292df2a157680ca4324` |

---

## 1. What failed, and why it is a stale expectation and not a product defect

Dispatch run #25 of `backtest_bench.yml` (commit `3758dc6`, 21.09.2026) went red at
`Сверка восстановления с живым coeffs.json`: one `unexplained` cell, TAO `r7`, +1.748 pp
(archive minus production) against a 1.50 pp bar. `--target`, which runs before `Сверка` and
calls the same reconciliation, measured 29 coins with TAO out of its arms. TAO's `r14` +1.571,
`r30` +1.881, `max_price` and `max30` +1.50 % sat under their bars with the same sign.

**Production and the archive disagree about the INSTANT, not about the arithmetic.** The bench
executes production's own block (`--attrib` on the same run: `eff14` residual 0 on 30 of 30,
`f` two-point on 30 of 30), so no formula can differ. What differs is where each side reads the
window's end:

- `coeffs.json` was built at **10:50:25Z**; the archive's last stamp is **11:00**, and a price is
  stamped at the END of its hour (`_series_from_rows`). Production's instant lies INSIDE the
  archive's last bar.
- `reconcile()` compares production with `cdb.build(..., len(prices) - 1)` — the archive at its
  LAST stamp — whatever the gap. On 21.09, a day the analysis engine's own run measured BTC
  +6.5 % over 24 hours, that was ten minutes of a violent hour.
- `--attrib`'s printed terms place TAO exactly: production's value lies between the archive's
  value at its last close (Δ = 0) and the value the same window takes with the previous close at
  its end (`T_end`) on all three horizons — Δ −1.748 / −1.571 / −1.881 pp against `T_end`
  −3.136 / −2.783 / −3.309 pp (`attrib.txt`, sign production minus archive).

The expectation that went stale is **«the archive's value at production's instant is its value
at its last close»**. It is false wherever production's instant is earlier than that close, and
map §0 measured on 13.09 that one bar moves a return field by the order of its own threshold.
The repair reads the archive AT production's instant wherever the archive holds the bar that
contains it. **No threshold, class, comparability rule or failing set moves.** This is the
stale-expectation route contract §7 item 2 names: the finding is the Architect's, the
expectation is re-derived here with its derivation in §5, and no assertion of either gate bench
changes.

---

## 2. Scope

**Files to Modify**
- `bench/backtest_bench.py` — §3.
- `bench/verify_bench.py` — §4.1, additions only.
- `bench/backtest_guard_bench.py` — §4.2, additions only.

**Files to Create:** none. **Files to Delete:** none.

**Explicitly untouched:** `main.py`, `index.html`, `catalysts.json`, every workflow
(`backtest_bench.yml` included — contract §7 item 8), `CMP_GAP_H`, the `SPEC` thresholds,
`CLASSES`, `HARD_CLASSES`, `_cell_comparable`'s code (§3.6 edits its docstring only),
`_cell_class`, `target_gate`, `--attrib`, the fetch layer and the dispatch cache.
**No existing check in either bench is edited, removed or re-registered.**

---

## 3. The change in `bench/backtest_bench.py`

Three module-level helpers, placed together immediately before `_cell_dv` (after
`_gap_hours`), and one reading inside `reconcile()`.

**3.1 `_enclosing(pts, t)`** — pure. `pts` is a sorted list of the archive's stamps in ms, `t`
an instant in ms. Returns `(j_lo, j_hi)`, the indices of the two stamps between which `t` lies:
`j_hi` is the first index with `pts[j_hi] >= t`; where `pts[j_hi] == t` it returns
`(j_hi, j_hi)`; otherwise `j_lo = j_hi - 1`. Returns `None` where the archive does not hold the
bar containing `t`: `j_hi` past the end (after the last stamp), `j_lo < 0` (before the first),
or `pts[j_hi] - pts[j_lo] > HOUR_MS` (an interior hole). An empty `pts` returns `None`.

**3.2 `_archive_at(cdb, P, V, t, cd_last=None)`** — the archive read at instant `t` by
production's own construction. `_enclosing([p[0] for p in P], t)`; `None` → return `None`. Let
`own(j)` be `cd_last` where `j` is the last index of `P` and `cd_last` is not `None`, else
`cdb.build(P, V, j)`. Where `j_lo == j_hi` return `[own(j_lo)]`. Otherwise return exactly, in
this order:
`[own(j_lo), own(j_hi), cdb.build(_attr_swap(P, {j_hi: j_lo}), V, j_hi),
cdb.build(_attr_swap(P, {j_lo: j_hi}), V, j_lo)]` — the two windows ending at the enclosing
stamps, each with its own close and then with the other stamp's close at its end. Where any
element is `None`, return `None`. **Why four and not two:** production derives its window's
start from its end on CoinGecko's own sampling grid, which this system does not publish, so its
start can sit on either window's grid; the two own records alone miss the case where the start
bar moved too, and lane P6 is that case.

**3.3 `_nearest(recs, k, b)`** — the value of field `k` nearest production's `b` inside
`[min, max]` of the records' `k` values, i.e. `b` itself where it lies inside. `None` where any
record carries no number for `k` — judged by `_attr_num`, the module's one definition of a
number (inv. 20).

**3.4 `reconcile()`** — per symbol, after `gap_sym = _gap_hours(gen, [t_last])`:

- `at = None if gap_sym is None else _archive_at(cdb, ser["prices"], ser["volumes"],
  t_last + round(gap_sym * HOUR_MS), cd)` — production's instant is read off the one
  derivation of the gap and never parsed a second time (inv. 20);
- per `SPEC` cell, after the existing `a, b` guard: `an = _nearest(at, k, b) if at else None`,
  then `an = a` where `an is None`, then `dv = _cell_dv(kind, an, b)` in place of
  `_cell_dv(kind, a, b)`;
- both cell dicts (compared and not compared) gain the key `"an"`; **`"a"` keeps its meaning —
  the archive's value at its last close** — because `--attrib` raises when `rc["a"]` differs
  from its own build at the last bar;
- each `rows` entry gains `"at": at is not None`.

Everything downstream of `dv` — `_cell_comparable`, `seen`, `worst`, `over`, the class,
`sym_class` — is unchanged and reads the new `dv`. `--target`, `--regime-gate` and `--attrib`
read the same classes and move with them; none of their code changes.

**3.5 `verify_against_live()`** — immediately after the `разрыв по монетам: …` print, inside
the same `if R["rows"]:` block, print exactly:

```
"архив прочитан в момент продакшна у %d монет · по последнему закрытию у %d"
```

with the count of rows whose `"at"` is true and the count of the rest.

**3.6 `_cell_comparable`'s docstring** — run #25 refuted one of its sentences. Replace
«A level is a 90-day extremum and hours do not move it, so it is comparable at any gap.» with:
«A level is comparable at any gap. Hours DO move it where an extreme is being made at the
window's end — run #25's TAO `max_price` moved 1.50 % inside one bar — which is why
reconcile() reads the archive at production's instant wherever it holds that bar (ТЗ-51).»
The function's code does not change.

---

## 4. The checks — written here, run by you

Both blocks are the Architect's, measured on the copies in §0's gate table against a reference
implementation of §3 (§5). Insert them verbatim; formatting may follow the file, conditions and
check names may not. **A check that fails means the implementation differs from §3** — fix the
implementation, never the check (contract §7 item 2).

**4.1 `bench/verify_bench.py`** — a new case 12, inserted immediately before the final
`shutil.rmtree(tmp, ignore_errors=True)` / `shutil.rmtree(tmp_in, ignore_errors=True)` pair.
15 checks. The prefix is `P` so no lane reads as the file's own L1–L8.

```python
# 12. The archive read AT production's instant (ТЗ-51). A price is stamped at
#     the END of its hour, so a production built inside the archive's last bar
#     was compared with the archive's value at a LATER instant, and on a violent
#     hour that alone crossed a threshold (run #25, TAO `r7`). Where the archive
#     holds the bar containing production's instant it is now read there: the
#     windows ending at the two stamps that enclose the instant, each with its own
#     close and with the other close at its end, and a cell is measured from
#     production's value to the nearest point of what those records span. Where no
#     bar holds the instant — after the last stamp, or across a hole — the reading
#     stays at the last close. Lanes keep the prefix P so they never read as this
#     file's own L1-L8. Every world is AAA over the file's three-coin series with a
#     violent last bar; production is production's own `f` on the same stamps with
#     its last close moved inside that bar, and the non-vacuity checks prove each
#     world really puts the old reading over its bar (inv. 22).
def p_reading(text, n_at, n_last):
    return ('архив прочитан в момент продакшна у %d монет · по последнему закрытию у %d'
            % (n_at, n_last)) in text


def p_cell(L, sym, k):
    return next(row['cells'][k] for row in L[2]['rows'] if row['sym'] == sym)


_pa = [list(x) for x in coins['AAA']]
_pa[-1][1] = round(_pa[-2][1] * 1.04, 6)
_pm = [list(x) for x in _pa]
_pm[-1][1] = round(_pa[-2][1] * 1.02, 6)
make_cache(tmp, dict(coins, AAA=_pa))
P1 = run_lane(tmp, live_from_cache(dict(coins, AAA=_pm), cdb, gap_h=-0.5))
_thr = dict((k, t) for k, _, t in P1[2]['spec'])
_kind = dict((k, kd) for k, kd, _ in P1[2]['spec'])
_c = p_cell(P1, 'AAA', 'r7')
ok('P1. production inside the last bar: exits 0', P1[0] == 0, 'exit=%s' % P1[0])
ok('P1. every symbol is clean',
   P1[4] == dict((s, 'clean') for s in coins), repr(P1[4]))
ok('P1. every compared cell of AAA reads exactly zero',
   all(row['cells'][k]['dv'] == 0.0 for row in P1[2]['rows'] if row['sym'] == 'AAA'
       for k in row['cells'] if row['cells'][k] and row['cells'][k]['cmp']),
   repr([(k, c['dv']) for row in P1[2]['rows'] if row['sym'] == 'AAA'
         for k, c in row['cells'].items() if c]))
ok('P1. the reading line names every symbol at production\'s instant',
   p_reading(P1[1], 3, 0), last_line(P1[1]))
ok('P1. not vacuous: read at the last close, AAA r7 is over its bar',
   abs(bb._cell_dv(_kind['r7'], _c['a'], _c['b'])) > _thr['r7'],
   repr((_c['a'], _c['b'])))


def p_minus(rec):
    if rec['symbol'] == 'AAA':
        rec['r7'] = rec['r7'] - 0.05                       # 5 pp BELOW the bar


P2 = run_lane(tmp, live_from_cache(dict(coins, AAA=_pm), cdb, -0.5, mutate=p_minus))
_c2 = p_cell(P2, 'AAA', 'r7')
ok('P2. a planted 5 pp is still red: exit 1, only the planted cell unexplained',
   P2[0] == 1 and P2[3].get('unexplained') == [('AAA', 'r7')], repr((P2[0], P2[3])))
ok('P2. measured from the bar: nearer than the last close, and still over its bar',
   _c2['an'] != _c2['a']
   and _thr['r7'] < abs(_c2['dv']) < abs(bb._cell_dv(_kind['r7'], _c2['a'], _c2['b'])),
   repr((_c2['a'], _c2['an'], _c2['b'], _c2['dv'])))

P3 = run_lane(tmp, live_from_cache(dict(coins, AAA=_pm), cdb, gap_h=0.5))
ok('P3. production after the last stamp: read at the last close, AAA unexplained',
   P3[0] == 1 and P3[4].get('AAA') == 'unexplained', repr((P3[0], P3[4])))
ok('P3. the reading line names every symbol at the last close',
   p_reading(P3[1], 0, 3), last_line(P3[1]))

P4 = run_lane(tmp, live_from_cache(dict(coins, AAA=_pm), cdb, gap_h=0.0))
ok('P4. production exactly on the last stamp: read at that close, AAA unexplained',
   P4[0] == 1 and P4[4].get('AAA') == 'unexplained', repr((P4[0], P4[4])))
ok('P4. an instant on a stamp is read at production\'s instant',
   p_reading(P4[1], 3, 0), last_line(P4[1]))

_ph = [x for i, x in enumerate(_pa) if i != len(_pa) - 2]
_phm = [list(x) for x in _ph]
_phm[-1][1] = _pm[-1][1]
make_cache(tmp, dict(coins, AAA=_ph))
P5 = run_lane(tmp, live_from_cache(dict(coins, AAA=_phm), cdb, -0.5))
ok('P5. a hole around production\'s instant: no reading, AAA reads coverage',
   P5[0] == 1 and P5[4].get('AAA') == 'coverage', repr((P5[0], P5[4])))
ok('P5. the reading line names AAA at the last close',
   p_reading(P5[1], 2, 1), last_line(P5[1]))

_pc = [list(x) for x in coins['AAA']]
_i0 = len(_pc) - 1
_s = bb.attrib_start(lambda Q, W, i: cdb.build(Q, W, i),
                     _pc, [[t, 1e7] for t, _ in _pc], _i0, 'r7')
for _j in range(_s, len(_pc)):
    _pc[_j][1] = round(_pc[_j][1] * 1.05, 6)
_pc[-1][1] = round(_pc[-2][1] * 1.04, 6)
_pcm = [list(x) for x in _pc]
_pcm[-1][1] = round(_pc[-2][1] * 1.02, 6)
make_cache(tmp, dict(coins, AAA=_pc))
P6 = run_lane(tmp, live_from_cache(dict(coins, AAA=_pcm), cdb, -0.5))
_v = [[t, 1e7] for t, _ in _pc]
_two = [cdb.build(_pc, _v, _i0 - 1), cdb.build(_pc, _v, _i0)]
_b6 = p_cell(P6, 'AAA', 'r7')['b']
ok('P6. the start bar moved too: the other close at each window\'s end holds AAA, exit 0',
   P6[0] == 0 and P6[4].get('AAA') == 'clean', repr((P6[0], P6[4])))
ok('P6. not vacuous: the two own records alone leave AAA r7 over its bar',
   abs(bb._cell_dv(_kind['r7'], bb._nearest(_two, 'r7', _b6), _b6)) > _thr['r7'],
   repr((_two[0]['r7'], _two[1]['r7'], _b6)))
```

**4.2 `bench/backtest_guard_bench.py`** — a new section L, inserted after section K's
`print('K. comparability: …')` line and before the final
`# ═══…` / `shutil.rmtree(tmp, ignore_errors=True)` cleanup block. 18 checks. The letter is read
off the file: its last section is K (map §10: a section letter is chosen from the FILE, never by
counting). It reuses section I's `I_T0`, `I_N`, `I_CDB`, `i_series` and `i_vol`.

```python
# ═══════════════════════════════════════════════════════════════════════════
# L. The archive read AT production's instant  (ТЗ-51)
# ═══════════════════════════════════════════════════════════════════════════
# The letter is L, read off the FILE: the last section it carries is K, and two
# sections already share E, so counting sections would say M (ТЗ-51 §4).
#
# Known answers on the three helpers alone. The worlds that reach them through
# --verify are verify_bench's lanes P1-P6: which class a cell earns is that
# bench's, not this one's (inv. 20). Stamps are whole hours and the instants
# probed sit on them or one millisecond away, so every equality is exact and no
# tolerance appears. L8-L10 compare the reading with production's own builds by
# dict equality: the records are the same floating-point expressions on the same
# operands, never a restatement of them (inv. 21, 38).
l0 = checks[0]
L_PTS = [I_T0 + (k + 1) * HOUR for k in range(10)]
L_HOLE = L_PTS[:5] + L_PTS[6:]                  # the bar stamped L_PTS[5] is absent
ok('L1. on an interior stamp: that stamp twice', bb._enclosing(L_PTS, L_PTS[4]) == (4, 4),
   bb._enclosing(L_PTS, L_PTS[4]))
ok('L2. one millisecond past an interior stamp: the next bar',
   bb._enclosing(L_PTS, L_PTS[4] + 1) == (4, 5), bb._enclosing(L_PTS, L_PTS[4] + 1))
ok('L3. one millisecond before an interior stamp: the bar that stamp ends',
   bb._enclosing(L_PTS, L_PTS[4] - 1) == (3, 4), bb._enclosing(L_PTS, L_PTS[4] - 1))
ok('L4. on the last stamp: that stamp twice', bb._enclosing(L_PTS, L_PTS[-1]) == (9, 9),
   bb._enclosing(L_PTS, L_PTS[-1]))
ok('L4. one millisecond past the last stamp: no bar holds it',
   bb._enclosing(L_PTS, L_PTS[-1] + 1) is None, bb._enclosing(L_PTS, L_PTS[-1] + 1))
ok('L5. inside a hole: no bar holds it',
   bb._enclosing(L_HOLE, L_PTS[5] - 1) is None, bb._enclosing(L_HOLE, L_PTS[5] - 1))
ok('L5. on the stamp after a hole: that stamp twice',
   bb._enclosing(L_HOLE, L_PTS[6]) == (5, 5), bb._enclosing(L_HOLE, L_PTS[6]))
ok('L6. before the first stamp: no bar holds it',
   bb._enclosing(L_PTS, L_PTS[0] - 1) is None, bb._enclosing(L_PTS, L_PTS[0] - 1))
ok('L6. on the first stamp: that stamp twice', bb._enclosing(L_PTS, L_PTS[0]) == (0, 0),
   bb._enclosing(L_PTS, L_PTS[0]))
ok('L7. an empty archive holds nothing', bb._enclosing([], L_PTS[0]) is None)
L_P = i_series(I_N, 23)
L_V = i_vol(L_P)
L_I = len(L_P) - 1
L_LAST = I_CDB.build(L_P, L_V, L_I)
L_IN = bb._archive_at(I_CDB, L_P, L_V, L_P[L_I - 3][0] + HOUR // 2, L_LAST)
ok('L8. inside a bar: four records, each production\'s own build',
   L_IN == [I_CDB.build(L_P, L_V, L_I - 3), I_CDB.build(L_P, L_V, L_I - 2),
            I_CDB.build(bb._attr_swap(L_P, {L_I - 2: L_I - 3}), L_V, L_I - 2),
            I_CDB.build(bb._attr_swap(L_P, {L_I - 3: L_I - 2}), L_V, L_I - 3)],
   None if L_IN is None else len(L_IN))
L_ON = bb._archive_at(I_CDB, L_P, L_V, L_P[L_I][0], L_LAST)
ok('L9. on the last stamp: one record, the caller\'s own and not a rebuild',
   isinstance(L_ON, list) and len(L_ON) == 1 and L_ON[0] is L_LAST,
   None if L_ON is None else len(L_ON))
ok('L10. past the last stamp: no reading',
   bb._archive_at(I_CDB, L_P, L_V, L_P[L_I][0] + 1, L_LAST) is None)
L_R = [{'r7': 0.01}, {'r7': 0.03}, {'r7': 0.02}]
ok('L11. inside the span: production\'s own value', bb._nearest(L_R, 'r7', 0.025) == 0.025,
   bb._nearest(L_R, 'r7', 0.025))
ok('L11. below the span: its lower bound', bb._nearest(L_R, 'r7', -0.5) == 0.01,
   bb._nearest(L_R, 'r7', -0.5))
ok('L11. above the span: its upper bound', bb._nearest(L_R, 'r7', 0.5) == 0.03,
   bb._nearest(L_R, 'r7', 0.5))
ok('L11. a record with no number for the field: no reading',
   bb._nearest(L_R + [{'r7': None}], 'r7', 0.02) is None)

# ── §5.2.6 the section reports its own count and refuses to pass on zero.
ok('L. section L compared something', checks[0] - l0 > 0, checks[0] - l0)
print('L. reading at production\'s instant: %d comparisons' % (checks[0] - l0))
```

---

## 5. Registered expectations and what derived each

| Expectation | Derived by |
|---|---|
| `verify_bench.py`: `checks run: 74   FAIL 0` (59 before) | Architect's probe: §4.1 on the gate-table copy against a reference implementation of §3 on the gate-table `backtest_bench.py` and `main.py` 518 / `0e3ead8c…` — 59 pre-existing checks unchanged, 15 added |
| `backtest_guard_bench.py`: `checks run: 506   FAIL 0`, `L. reading at production's instant: 18 comparisons`, sections E 32 · F 29 · G 63 · H 107 · I 95 · J 8 · K 11 unchanged | the same probe on the gate-table guard with `index.html` 3799 / `4e71da9b…` |
| Negative control, `verify_bench.py`: `checks run: 74   FAIL 9` — P1 ×4 (exits 0 · every symbol clean · AAA reads zero · reading line), P2 ×2, P4 (reading line), P5 (reading line), P6 (exits 0) | the same probe with `_archive_at` returning `None` before its first statement |
| Negative control, guard: `checks run: 506   FAIL 2` — L8, L9 | the same control |
| Lanes P1, P6 fail under the old reading for the reason #25 failed | the last check of P1 and the last check of P6 prove each world puts the last-close reading over the `r7` bar, and both pass under either reading |
| Gate total `1 336 148` → **`1 336 181`** | map §0's total + 15 (step 4) + 18 (step 14); no other step moves |
| On #25's own data TAO's three return cells read inside | `attrib.txt` of run #25: Δ lies between 0 and `T_end` on `r7`, `r14`, `r30`, and `T_end` is `_archive_at`'s third record — the last window with the previous close at its end — for a two-point field — a derivation from printed terms, not a replay (the dispatch cache is not saved) |

No expectation above is a threshold about the answer (inv. 49): nothing new is compared with a
number.

---

## 6. Validation

1. **Baseline, before any edit**, on the checkout: `python3 bench/verify_bench.py` →
   `checks run: 59   FAIL 0`; `python3 bench/backtest_guard_bench.py` →
   `checks run: 488   FAIL 0`. Record the gate-table pairs (§0).
2. `python3 -m py_compile` on all three files.
3. **After:** `verify_bench.py` → `checks run: 74   FAIL 0`; the guard →
   `checks run: 506   FAIL 0` with the section lines of §5 row 2. Record the printed lines.
4. **Negative control** in the working tree: make `_archive_at` return `None` as its first
   statement; run both benches; record the two results against §5 rows 3 and 4 with every FAIL
   name; revert; show `git status` clean for that file and both benches green again.
5. `grep -n` evidence that `bench/backtest_bench.py` carries each of: `def _enclosing(pts, t):`,
   `def _archive_at(cdb, P, V, t, cd_last=None):`, `def _nearest(recs, k, b):`,
   `t_last + round(gap_sym * HOUR_MS)`, `архив прочитан в момент продакшна у %d монет` and
   `Hours DO move` (keep each of these two strings on one line), and that
   `grep -c 'hours do not' bench/backtest_bench.py` prints `0` — the retired sentence.
6. **No-regression statement**, with evidence: `git diff --stat` names exactly the three files;
   `git diff` on the two benches contains no `-` line outside the file header (additions only);
   every pre-existing check of both benches passes.
7. Push the branch and read `bench.yml` on it per contract §9; record steps 4 and 14 from the
   runner's log when the session can read it.
8. Fingerprints per contract §10: the map (revision `2026-09-22-b`), the four files of its
   table, and the three files of §0's gate table before and after.

---

## 7. Risks this TZ states and does not repair

- **A positive gap is not reached.** Where production was built after the archive's last close,
  no bar holds its instant and the reading stays at that close; a violent hour can still turn a
  return cell red there — the 09.09 shape at +0.8 h. Its own row is map §10 «One dispatch reads
  production up to four times».
- **The reading is bounded by the enclosing CLOSES, not the bar's high and low.** A production
  value sampled at an intra-bar extreme beyond both closes still reads as a disagreement of that
  size.

---

## Commit Message

`TZ-51: --verify reads the archive at production's instant`
