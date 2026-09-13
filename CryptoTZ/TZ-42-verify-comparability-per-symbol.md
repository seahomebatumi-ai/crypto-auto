# TZ-42 — Comparability is decided per SYMBOL and before the class: an incomparable cell carries no class, the window is two-sided, and the `venue-basis` licence stops forgiving the tail

**Canonical filename: `TZ-42-verify-comparability-per-symbol.md`.** Name the committed file
from this line, never from the name it arrived under (contract §3).

**Model: Opus.** `--verify` is the one mode that can fail in the dangerous direction — print
«matches» where nothing matched — and this TZ moves its verdict, its exit code and the set
`--target` gates on. The three named defects are one rule seen three times, and the repair is
worthless if they are implemented as three.

**Sequencing: TZ-41 is merged before this TZ starts** — pull request **#38**, merge commit
**`d88593e`**, implementation commit `dc42e4e`. TZ-41 §6 deferred exactly this work
(«The skip defect is NOT repaired here … it gets its own TZ against its own worlds»). Check
the merge and say so at the top of your report.

---

## 0. Fingerprint gate — blocking, before any work

Required map revision, matched as an exact substring against the repository copy
(contract §5):

**Revision 2026-09-13-b.**

The map does not move for this TZ: the revision recording it lands after the report, as
TZ-39, TZ-40 and TZ-41 all executed against the revision preceding their own.

Content anchors — all seven, each matched as an EXACT substring. **Report the matched
substring, not the verdict** (§10).

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-13-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `71. **A measurement that is not RETAINED was not taken,` |

The map's `## 0` file table — measure each at the stated line count and MD5; a difference is
reported under `## Pre-existing Issues` and is **not acted on** (contract §5).

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Baselines for the files this TZ touches**, measured on `main` at `d88593e`. Benches are
absent from the enforced table by decision (map §0): report what you measure, do not block.

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5008 | `c7fedd64bce7c27c07803325b1f807d3` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
| `bench/backtest_guard_bench.py` | 2438 | `85ea609882ac3761fd526b3ebff2fe5f` |

Contract in force: **v20**, 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0`. Map:
2691 lines, MD5 `7c8b58ec4dea7142104fc9dc0173edcc`. Gate: `bench.yml` step 4
(`verify_bench.py`) = **40** checks, step 14 (`backtest_guard_bench.py`) = **475**. Your
baseline is what you measure.

---

## 1. Why — one defect, measured three times

- **The comparison window is derived for the CACHE and applied to every SYMBOL.**
  `reconcile()` computes `gap` from `max(ends)` — the newest last bar anywhere in the cache —
  and then decides comparability once for all thirty coins. On 13.09 that number was −0.2 h
  while the five perpetuals ended about 20 h earlier, because the tail is topped up from the
  spot endpoint and no futures mirror exists (inv. 64). The symbols that needed the window
  are exactly the symbols whose own bar is never the newest, so the rule is blind precisely
  where it is load-bearing.
- **A cell announced as not compared is classified anyway.** `over` is computed with no
  reference to `skip`; `skip` reaches the printed line and the `never` list and nothing else.
  Measured 12.09 offline on a three-coin world with BBB `r7` +5 pp: at +30 h the run prints
  «НЕ СВЕРЯЛОСЬ … r7, r14, r30, eff14», classes BBB `r7` `unexplained` in the same output,
  exits 1 and removes the symbol from `--target`'s arms. `verify_bench.py` case 5 passes only
  because its big-gap world carries no disagreeing return — inv. 22, one layer inside a
  control that reads correct.
- **The window is one-sided.** `gap > 3` compares an archive LATER than production at any
  distance with no announcement at all. Nothing about the arithmetic is directional: the two
  sides are built at different instants either way.
- **The consequence is the mixture in `venue-basis`.** Nine cells took the licence on 13.09
  and `--attrib` splits them differently one from another — ARB `r7` is Δ −8.241 pp with
  `T_start` −7.500, so the start instant carries 91 % of the biggest cell of the run, while
  HYPE `r14` is Δ −2.035 with `T_start` −0.003. The licence is granted per SERIES and the
  deviation is per CELL, so a cell whose gap is the perp's own 20 h is forgiven under a name
  that says «basis». **A perp/spot basis is a price-level fact; it cancels in a return taken
  over one series.** The licence keeps what it can explain and loses what it cannot.

---

## 2. Scope

**Files to Modify:** `bench/backtest_bench.py`, `bench/verify_bench.py`,
`bench/backtest_guard_bench.py`.
**Files to Create:** none. **Files to Delete:** none.

No production file is in scope. `.github/workflows/**` is not named by this TZ and is
therefore closed to it (hard floor item 8).

### `## Touches`

- `--target` and `--regime-gate` read `reconcile()`'s `sym_class`; both gain one printed
  line (§3 edit 7) and neither changes which symbols it measures.
- `--attrib` reads `reconcile()`'s return dict; one key disappears from it (§3 edit 8) and
  no term, population, printed field or exit rule of the attribution moves.

---

## 3. The repair — one rule, eight edits, `bench/backtest_bench.py`

**The rule.** A cell is COMPARABLE when both sides were built over the same window.
Comparability is decided per symbol and per field, BEFORE the threshold, from the quantity
that actually decides it: the symbol's OWN end instant against production's `generated_at`.
An incomparable cell is read, printed and named — and it **carries no class**, no threshold
verdict, no contribution to any count of agreement and no exclusion from `--target`.

1. **`RET_FIELDS` moves to module scope**, beside `CLASSES`, unchanged in content
   (`"r7", "r14", "r30", "eff14"`). It is now read by two functions and a control; a second
   copy is what inv. 20 forbids.
2. **`CMP_GAP_H = 3.0`, one module constant**, beside `RET_FIELDS`. The three hours are
   currently written twice — the decision in `reconcile()` and the announcement in
   `verify_against_live()` — and a threshold in two places is a threshold that moves in one.
3. **`_cell_comparable(field, gap_sym)`**, a new module-level function next to `_cell_class`,
   returning `(bool, why)`:
   - a field not in `RET_FIELDS` → `(True, None)`. A level is a 90-day extremum and the
     existing judgement that hours do not move it is unchanged;
   - `gap_sym is None` → `(False, "разрыв во времени неизвестен")`;
   - `abs(gap_sym) > CMP_GAP_H` → `(False, "разрыв во времени %+.1f ч" % gap_sym)`. **The
     window is two-sided and the sign is carried into the reason**, never into the decision;
   - otherwise `(True, None)`.
   It reads no venue, no census and no threshold: comparability is a fact about instants.
4. **The per-symbol gap is the existing derivation, called with one stamp.** Inside
   `reconcile()`'s symbol loop, after `t_last` is known: `gap_sym = _gap_hours(gen, [t_last])`.
   `--attrib` already calls it exactly this way per coin (TZ-40 §3), so this adds no
   arithmetic and creates no second site (inv. 20). The cache-wide `gap` stays as it is and
   keeps being printed — it is a reading of the archive, and it stops being a verdict.
5. **The cell loop asks comparability first.** For a cell whose two sides are both present:
   count it in a new `present[k]` counter, then call `_cell_comparable`. If it is not
   comparable — record `(sym, k, why, gap_sym)` in a new `nocmp` list, keep the computed `dv`
   in the cell for printing, set `cmp: False`, and **do not** increment `seen[k]`, **do not**
   update `worst[k]`, **do not** compute `over`, **do not** call `_cell_class`. Printing a
   number and counting it as a comparison are two different acts; only the second is a claim.
   Everything for a comparable cell is exactly what it is today.
6. **`never` reads presence, not comparisons.** It becomes the fields with `present[k] == 0`
   and `kind != "info"` — the field is absent from the live `coeffs.json`, which is what that
   list has always meant and what makes it a failure. A field present everywhere and
   comparable nowhere is an operational state, named in §3 edit 9 and not a failure.
7. **A symbol whose cells were not all compared is not `clean`.** Add `UNVERIFIED =
   "unverified"` beside `CLASSES`; it joins neither `CLASSES` nor `HARD_CLASSES`. Symbol
   precedence, in order: a hard class · `UNVERIFIED` if any cell of that symbol is
   incomparable · `venue-basis` · `clean`. **`clean` may never mean «nothing was compared»** —
   that is the dangerous direction this mode exists to refuse. `target_gate` is unchanged and
   `unverified` is therefore not excluded; `--target` and `--regime-gate` each print one line
   naming the admitted set, in the shape of the existing «НЕ СВЕРЕНО … но в рукава допущено»
   line: `СВЕРКА НЕПОЛНАЯ (окно не совпадает), но в рукава допущено: …`.
8. **`attrib_run` drops `"skip": R["skip"]` from its return dict**, the key having gone.
   `report_attrib`'s printed sentence is prose and stays verbatim: the comparability filter is
   still not applied to the attribution, and that is still the reason it can attribute the
   cells `--verify` declines to compare.
9. **A run that compared nothing refuses.** After the loop, beside the existing `cmp_n == 0`
   refusal: if `sum(seen[k] for k, kind, _ in SPEC if kind != "info") == 0` —
   `sys.exit("СТОП: ни одной сравнимой ячейки — сверка не состоялась …")` naming the count of
   symbols and the worst gap. **This is the hole the per-cell rule opens and it is closed in
   the same change**: without it a stale `coeffs.json` makes every cell incomparable and the
   mode exits 0 having verified nothing (inv. 22).

### Printing — `verify_against_live()`, the same rule made visible

- the gap line gains the dispersion that would have caught this defect:
  `разрыв по монетам: от %+.1f до %+.1f ч` over the symbols with a known gap, and the count
  of symbols whose gap is unknown;
- the announcement fires on `nocmp` being non-empty and **keeps its opening literal**:
  `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ у N монет из M` — their return fields are computed at different
  instants and are not comparable; the rest are compared as usual;
- the per-field summary prints `сверок %2d из %2d` (comparable of present) and, where they
  differ, `не сравнимо у N монет`;
- the «ожидаемый сдвиг цены за разрыв» line reads the worst `abs(gap_sym)` among the
  incomparable symbols, never a negative number under a square root;
- a new block **keeps the literal `НЕ СВЕРЯЛОСЬ`**: `НЕ СВЕРЯЛОСЬ (окно не совпадает): r7,
  r14, r30, eff14 — ячеек N на M монетах`, then one line per symbol with its own gap and its
  fields;
- the agreement line lists only fields with `seen[k] > 0`, and «СВЕРКА ПО МОНЕТАМ» prints
  `unverified` where the precedence says so.

**Nothing else moves.** No threshold in `SPEC`, no member of `CLASSES` or `HARD_CLASSES`, no
line of `_cell_class`, `_cov_hit`, `_venue_licence`, `_gap_hours`, `census` or `target_gate`,
no measure, no sign convention, and no symbol's membership in the arms.

---

## 4. Controls

**`bench/verify_bench.py` — the worlds. Every existing assertion stays exactly as written**;
if one of the 40 goes red, that is a finding for the report and a BLOCKED verdict, never an
edit (hard floor item 2). The lanes below are additions.

| Lane | World | Must hold |
|---|---|---|
| L1 | +30 h gap, a return over the bar on every coin | exit 0 · the class lists are empty · «НЕ СВЕРЯЛОСЬ» names the field and the coins · no symbol excluded |
| L2 | the same at −30 h | identical exit and identical class sets to L1 — **the equality is the assertion**; the sign decides nothing |
| L3 | 0.5 h gap, one coin's series ending 20 h earlier, that coin on the PERPETUAL | (a) its return over the bar → not compared, NOT `venue-basis`, absent from the basis note, exit 0, symbol reads `unverified`; (b) its LEVEL over the bar → still `venue-basis`, named in the basis note, exit 0. **The pair is the assertion**: the licence keeps the level and loses the return |
| L4 | L3(a) with the same coin on SPOT | the same class sets as L3(a) — comparability reads no venue |
| L5 | every coin's series 30 h short | non-zero exit, the refusal of §3 edit 9 printed |
| L6 | gap exactly 3.0 h · exactly −3.0 h · 3.1 h, each with a return 5 pp over the bar | compared, compared, not compared — the boundary is stated, not implied |
| L7 | `generated_at` unparseable | returns not compared and announced, levels still compared |

The 20 h shortening is produced by building that coin's series 20 h shorter, never by writing
a census by hand: `make_cache` builds the census with production's own `census_of_doc`
(inv. 21, 38), so the fixture's `tail` stays 0 and the lane proves the decision is taken on
the INSTANT and not on `cov`.

**`bench/backtest_guard_bench.py` — the function.** A new section, **its letter read FROM THE
FILE and never by counting** (two sections already share `E`, map §0); name the letter and
why in the report. Known-answer assertions on `_cell_comparable`: a level is comparable at
any gap · `None` is not comparable · 3.0 comparable and 3.1 not, on both signs · the boolean
at `+g` equals the boolean at `−g` while the printed reason carries the sign · every member
of `RET_FIELDS` behaves identically · **the constant is the only place the three hours
live** — set `bb.CMP_GAP_H` to 10.0, assert the decision at 5 h moves, restore it and assert
the restoration. Every assertion is one comparison, counted where it compares (inv. 43).

---

## 5. Validation

Run every item; an item that cannot be run **fails** and is never «not applicable»
(contract §9). Record each baseline figure before the change.

1. `python3 -m py_compile bench/backtest_bench.py bench/verify_bench.py
   bench/backtest_guard_bench.py` — exit 0.
2. `python3 bench/verify_bench.py` — exit 0, `FAIL 0`. State the total against your measured
   40, the number of added checks, and confirm **no pre-existing assertion was edited or
   removed** (`git diff` on that file shows additions only).
3. `python3 bench/backtest_guard_bench.py` — exit 0, `FAIL 0`. State the new section's letter,
   its check count, step 14 before and after, and the gate total term by term (inv. 43).
4. **The seven lanes, each reported with its exit code and its class sets** — L2's equality
   and L3's pair stated as equalities, not as two greens.
5. **The pre-repair reading belongs in the report** (inv. 61): run L1's world against the file
   BEFORE the edit and state what it does — the exit code, the class it assigns, and whether
   the symbol leaves the arms. A repair reported without the reading it repairs is an
   assertion.
6. **Extremes:** empty cache (existing case 8) · a `_`-prefixed side file (case 7) · a field
   dropped from the live JSON for every coin (case 6, must still exit non-zero via `never`) ·
   a single-bar series · a coin present in the cache and absent from `coeffs.json`.
7. `python3 bench/clean_bench.py` and `python3 bench/direction_bench.py` — exit 0, unchanged
   counts; they share the module and must be shown untouched.
8. `git diff --name-only` names exactly three files, none of them production. Restate the four
   `## 0` hashes measured after the change and the three baseline hashes of §0.

---

## 6. What this TZ does NOT do

- **No production file is touched.** `index.html`, `main.py` and `catalysts.json` appear in no
  diff, and no `coeffs.json` field, window or construction moves.
- **No threshold, no class and no `HARD_CLASSES` entry moves.** `coverage` keeps its meaning
  and its severity; `venue-basis` keeps its own; `_cell_class` and `_cov_hit` are not edited.
- **The universe does not move** (hard floor item 3). Thirty coins, five declared `fut:true`,
  none added and none removed; `--target` measures exactly the symbols it measures today.
- **`--attrib` is unchanged as a measurement** — one dead key leaves its return dict.
- **No workflow file is opened** (hard floor item 8).
- **No fetch in this session** (hard floor item 9, inv. 44), and **no forecast about a
  dispatch that has not happened** (inv. 54). The next dispatch is the Boss's.

---

## 7. Hard floor clauses this TZ touches — quoted from contract v20

> 2. **Never edit a bench to make it pass.** A red bench is either a product defect or
> a stale expectation; both are findings, neither is a licence to change the
> assertion.

> 8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.

> 12. **Never remove, skip, comment out or `continue-on-error` a bench step to make CI
> green** — editing the assertion (item 2) and deleting the assertion are the same
> act; a step that cannot pass is a finding for the report.

---

## 8. Report requirements

Beyond the §10 template: the guard section's letter and why it was chosen from the file · the
seven lanes with exit codes and class sets · the pre-repair reading of item 5 · the check
counts term by term · `## Fingerprints`, mandatory.

`## Status` is COMPLETED when the eight edits are in, the seven lanes hold and both benches
are green offline. The dispatch is the Boss's and its absence is not PARTIAL (contract §9).

## Commit Message

```
TZ-42: decide comparability per symbol and before the class — an incomparable cell carries no class, the window is two-sided, and the basis licence stops covering the tail
```
