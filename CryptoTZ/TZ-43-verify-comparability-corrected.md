# TZ-43 — Comparability per SYMBOL and before the class, corrected: the attribution keeps a key with a new meaning, guard I9 is re-registered, and the unreachable refusal is withdrawn

**Canonical filename: `TZ-43-verify-comparability-corrected.md`.** Name the committed file
from this line, never from the name it arrived under (contract §3).

**Model: Opus.** Unchanged from TZ-42 and for the same reason: `--verify` is the one mode
that can fail in the dangerous direction, and this TZ moves its verdict, its exit code and
the set `--target` gates on.

**This TZ REPLACES TZ-42, which was correctly BLOCKED and is retired.** Report
`CryptoReports/TZ-42-verify-comparability-per-symbol-report.md`, commit `bb74ed4` on `main`,
is immutable and stands; `CryptoTZ/TZ-42-verify-comparability-per-symbol.md` is never
executed. Both of its blockers were reproduced independently before this TZ was written
(§1a). The architecture is unchanged — the defect, the rule and seven of the eight edits are
TZ-42's, restated here in full so that nothing is read out of a retired document (inv. 55).

**Sequencing.** TZ-41 is merged — pull request **#38**, merge commit **`d88593e`**,
implementation commit `dc42e4e`. Since then `main` carries `bb0cdac` (the TZ-42 upload) and
`bb74ed4` (its report), neither of which touches code. Your baseline is what you measure.

---

## 0. Fingerprint gate — blocking, before any work

Required map revision, matched as an exact substring against the repository copy
(contract §5):

**Revision 2026-09-13-b.**

The map does not move for this TZ: the revision recording it lands after the report.

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

**Baselines for the files this TZ touches**, measured on `main` at `bb74ed4`. Benches are
absent from the enforced table by decision (map §0): report what you measure, do not block.

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5008 | `c7fedd64bce7c27c07803325b1f807d3` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
| `bench/backtest_guard_bench.py` | 2438 | `85ea609882ac3761fd526b3ebff2fe5f` |

Contract in force: **v20**, 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0`. Map: 2691
lines, MD5 `7c8b58ec4dea7142104fc9dc0173edcc`. Gate: step 4 (`verify_bench.py`) = **40**
checks, step 14 (`backtest_guard_bench.py`) = **475**.

---

## 1. Why — one defect, measured three times

- **The comparison window is derived for the CACHE and applied to every SYMBOL.**
  `reconcile()` computes `gap` from `max(ends)` — the newest last bar anywhere in the cache —
  and decides comparability once for all thirty coins. On 13.09 that number was −0.2 h while
  the five perpetuals ended about 20 h earlier, because the tail is topped up from the spot
  endpoint and no futures mirror exists (inv. 64). The symbols that need the window are
  exactly the symbols whose own bar is never the newest.
- **A cell announced as not compared is classified anyway.** `over` is computed with no
  reference to `skip`; `skip` reaches the printed line and the `never` list and nothing else.
  Reproduced by TZ-42's run: at +30 h a 5 pp `r7` prints «НЕ СВЕРЯЛОСЬ … r7, r14, r30,
  eff14», is classed `unexplained` in the same output, exits 1, and all three symbols leave
  `--target`'s arms.
- **The window is one-sided.** `gap > 3` compares an archive LATER than production at any
  distance with no announcement at all — measured at −30 h: exit 1, three cells classed, no
  announcement printed.
- **The consequence is the mixture in `venue-basis`.** A perp/spot basis is a price-level
  fact and cancels in a return taken over one series; a 20 h tail is a window fact and does
  not. Measured: a coin 20 h short on the perpetual has its `r7` forgiven as basis today.
  The licence keeps what it can explain and loses what it cannot.

### 1a. What TZ-42's blocked run added, verified against the repository before this TZ

- **`bench/backtest_guard_bench.py:2333–2334` reads `AG['skip']`.** Removing that key from
  `attrib_run`'s return, and changing nothing else, kills the guard with `KeyError: 'skip'`
  after `H. transport: 107` — section I never finishes and section J never runs. Reproduced
  here on a scratch copy.
- **TZ-42's edit 9 was unreachable.** Its refusal fired on zero comparable non-`info` cells,
  while its own edit 3 makes every level comparable at any gap; the only world that reaches
  it is one where all six level fields are absent, and there `never` already exits 1. It was
  dead code and its lane L5 had no satisfiable reading. **Withdrawn** (§3, `## Not done`).
- **TZ-42 §5 item 7 named the wrong files.** `clean_bench.py` and `direction_bench.py` do not
  import `backtest_bench`; the importers are `verify_bench.py`, `backtest_guard_bench.py` and
  `exhaustion_calib.py`. Corrected in §6.
- **Three smaller findings, all folded in below:** the announcement literal asserted a size
  where the gap is unknown; `--regime-gate`'s sibling line says «в сетку», not «в рукава»;
  the guard's next section letter, read from the file, is **K** (J is the last header, at
  line 2361; `E` is carried twice, so counting would say L).

---

## 2. Scope

**Files to Modify:** `bench/backtest_bench.py`, `bench/verify_bench.py`,
`bench/backtest_guard_bench.py`.
**Files to Create:** none. **Files to Delete:** none.

No production file is in scope. `.github/workflows/**` is not named by this TZ and is
therefore closed to it (hard floor item 8).

### `## Touches`

- `--target` and `--regime-gate` read `reconcile()`'s `sym_class`; each gains one printed
  line (§3 edit 7) and neither changes which symbols it measures.
- `--attrib` reads `reconcile()`'s return dict: one key is replaced by another (§3 edit 8),
  and no term, population, printed field or exit rule of the attribution moves.
- `bench/exhaustion_calib.py` imports `backtest_bench` and is outside the gate by decision
  (`bench.yml`, ТЗ-10 §4). Measured: it uses `CACHE`, `CdBuilder`, `DAY_MS`, `HOUR_MS`,
  `_skip_to_matching_brace`, `fetch_prices`, `load_cache`, `probe` and `tokens_from_html` —
  none of them touched here. Compile it; do not run it and do not edit it.

---

## 3. The repair — one rule, eight edits, `bench/backtest_bench.py`

**The rule.** A cell is COMPARABLE when both sides were built over the same window.
Comparability is decided per symbol and per field, BEFORE the threshold, from the quantity
that decides it: the symbol's OWN end instant against production's `generated_at`. An
incomparable cell is read, printed and named — and it **carries no class**, no threshold
verdict, no contribution to any count of agreement, and no exclusion from `--target`.

1. **`RET_FIELDS` moves to module scope**, beside `CLASSES`, unchanged in content
   (`"r7", "r14", "r30", "eff14"`). It is now read by two functions and a control; a second
   copy is what inv. 20 forbids.
2. **`CMP_GAP_H = 3.0`, one module constant**, beside `RET_FIELDS`. The three hours are
   written twice today — the decision in `reconcile()` and the announcement in
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
4. **The per-symbol gap is the existing derivation, called with one stamp.** In
   `reconcile()`'s symbol loop, after `t_last` is known: `gap_sym = _gap_hours(gen, [t_last])`.
   `--attrib` already calls it exactly this way per coin (TZ-40 §3), so this adds no
   arithmetic and no second site (inv. 20). The cache-wide `gap` stays and keeps being
   printed — it is a reading of the archive, and it stops being a verdict.
5. **The cell loop asks comparability first.** For a cell whose two sides are both present:
   count it in a new `present[k]`, then call `_cell_comparable`. If it is not comparable —
   append `(sym, field, why, gap_sym)` to a new `nocmp` list, keep the computed `dv` in the
   cell for printing, set `cmp: False`, and **do not** increment `seen[k]`, **do not** update
   `worst[k]`, **do not** compute `over`, **do not** call `_cell_class`. Printing a number and
   counting it as a comparison are two different acts; only the second is a claim. A
   comparable cell behaves exactly as it does today. `reconcile()` returns `nocmp` and
   `present` alongside its existing keys, and drops `skip`.
6. **`never` reads presence, not comparisons.** It becomes the fields with `present[k] == 0`
   and `kind != "info"` — the field is absent from the live `coeffs.json`, which is what that
   list has always meant and what makes it a failure. A field present everywhere and
   comparable nowhere is an operational state: named, never a failure.
7. **A symbol whose cells were not all compared is not `clean`.** Add `UNVERIFIED =
   "unverified"` beside `CLASSES`; it joins neither `CLASSES` nor `HARD_CLASSES`. Symbol
   precedence, in order: a hard class · `UNVERIFIED` if any cell of that symbol is
   incomparable · `venue-basis` · `clean`. **`clean` may never mean «nothing was compared»** —
   that is the dangerous direction this mode exists to refuse. `target_gate` is unchanged, so
   `unverified` is not excluded; `--target` and `--regime-gate` each print one line naming the
   admitted set, **each in its own existing word** — `СВЕРКА НЕПОЛНАЯ (окно не совпадает), но
   в рукава допущено: …` and `… но в сетку допущено: …` respectively, matching the «НЕ
   СВЕРЕНО …» line already above it in each mode.
8. **`attrib_run`'s return carries `"nocmp": R["nocmp"]` where it carried `"skip": R["skip"]`.**
   The attribution's own behaviour does not change — the comparability filter is still not
   applied to it, which is still why it can attribute the cells `--verify` declines. The key
   is not merely dropped because guard I9 reads it, and a control is re-registered by name,
   never silently broken (§4). `report_attrib`'s printed prose is unchanged.

### Printing — `verify_against_live()`, the same rule made visible

- the gap line gains the dispersion that would have caught this defect:
  `разрыв по монетам: от %+.1f до %+.1f ч`, plus the count of symbols whose gap is unknown;
- the announcement fires on `nocmp` being non-empty and **keeps its opening literal where it
  is true**: `РАЗРЫВ БОЛЬШЕ ТРЁХ ЧАСОВ у N монет из M`, with `(у K разрыв неизвестен)`
  appended when `K > 0`. Where EVERY incomparable symbol has an unknown gap the line opens
  `РАЗРЫВ ВО ВРЕМЕНИ НЕИЗВЕСТЕН у N монет из M` instead — an announcement may not assert a
  size it did not measure (inv. 22);
- the per-field summary prints `сверок %2d из %2d` (comparable of present) and, where they
  differ, `не сравнимо у N монет`;
- the «ожидаемый сдвиг цены за разрыв» line reads the worst `abs(gap_sym)` among the
  incomparable symbols, never a negative number under a square root;
- a new block **keeps the literal `НЕ СВЕРЯЛОСЬ`**: `НЕ СВЕРЯЛОСЬ (окно не совпадает): r7,
  r14, r30, eff14 — ячеек N на M монетах`, then one line per symbol with its own gap and its
  fields;
- the agreement line lists only fields with `seen[k] > 0`, and «СВЕРКА ПО МОНЕТАМ» prints
  `unverified` where the precedence says so.

### `## Not done` — the withdrawn refusal

**TZ-42's edit 9 (`СТОП` on zero comparable cells) is withdrawn and nothing replaces it.**
Measured: with levels comparable at any gap it can fire only where every level field is
absent, and there `never` already exits 1 — it changed no exit code in any world. What
protects the dangerous direction instead is already in the printing above and is asserted by
lane L8: a field with zero comparisons is never named in the agreement line. **Nothing else
of TZ-42 is withdrawn.**

**Nothing else moves.** No threshold in `SPEC`, no member of `CLASSES` or `HARD_CLASSES`, no
line of `_cell_class`, `_cov_hit`, `_venue_licence`, `_gap_hours`, `census` or `target_gate`,
no measure, no sign convention, and no symbol's membership in the arms.

---

## 4. Guard I9 — RE-REGISTERED by name, not edited into passing

The assertion below reads a key edit 8 replaces. **It is retired by the Architect and
replaced by a strictly stronger one; the check count does not fall.** This is not hard-floor
item 2: that clause forbids weakening an assertion to make a red bench green. Here the
expectation is stale by decision, the TZ names it, quotes it, and specifies what stands in
its place. The two I9 checks below it are unchanged and must stay green as written.

Current text, `bench/backtest_guard_bench.py:2333–2334`:

```
ok('I9. g beyond --verify\'s window: --verify skips the return fields',
   len(AG['skip']) > 0, AG['skip'])
```

Its replacement asserts the relationship the section exists for — the attribution measures
exactly the cells the reconciliation declines:

- `AG["nocmp"]` is **non-empty** in that world (the reconciliation declined the return cells),
  and
- the set of cells `--attrib` compared, `{(c["sym"], c["field"]) for c in AG["cells"] if
  c["d"] is not None}`, is a **superset** of `{(s, f) for s, f, _, _ in AG["nocmp"]}`.

One check, both clauses, counted where it compares (inv. 43). The comment block above it
(lines 2325–2328) names the old cache-wide skip and is updated to the per-cell set in the
same edit. **If the replacement cannot be made to hold, that is a finding and a BLOCKED
verdict — never a weaker assertion.**

---

## 5. Controls — the worlds

**`bench/verify_bench.py`. Every existing assertion stays exactly as written**; if one of the
40 goes red, that is a finding for the report and a BLOCKED verdict, never an edit (hard
floor item 2). The lanes below are additions. TZ-42's L5 does not appear: it had no
satisfiable reading, and L8 replaces what it was for.

| Lane | World | Must hold |
|---|---|---|
| L1 | +30 h gap, `r7` over the bar on every coin | exit 0 · every class list empty · «НЕ СВЕРЯЛОСЬ» names the fields and the coins · no symbol excluded |
| L2 | the same at −30 h | identical exit and identical class sets to L1 — **the equality is the assertion**; the sign decides nothing |
| L3 | 0.5 h cache-wide gap, one coin's series ending 20 h earlier, that coin on the PERPETUAL | (a) its return over the bar → not compared, NOT `venue-basis`, absent from the basis note, exit 0, symbol reads `unverified`; (b) its LEVEL over the bar → still `venue-basis`, named in the basis note, exit 0. **The pair is the assertion**: the licence keeps the level and loses the return |
| L4 | L3(a) with the same coin on SPOT | the same class sets as L3(a) — comparability reads no venue |
| L6 | gap exactly 3.0 h · exactly −3.0 h · 3.1 h, each with `r7` 5 pp over the bar | compared, compared, not compared — the boundary is stated, not implied |
| L7 | `generated_at` unparseable | returns not compared, the unknown-gap announcement printed and the «БОЛЬШЕ ТРЁХ ЧАСОВ» literal absent, levels still compared |
| L7b | L7 plus a level over the bar | exit 1, that cell `unexplained`, its symbol excluded — an unknown gap does not excuse a level |
| L8 | L1's world | the agreement line names **no** return field, and each return field's summary reads `сверок 0 из N`. This is the claim that must not be made, asserted directly |

Lane numbering skips L5 deliberately: the retired lane keeps its number so this table and
TZ-42's report can be read against each other.

The 20 h shortening is produced by building that coin's series 20 h shorter, never by writing
a census by hand: `make_cache` builds the census with production's own `census_of_doc`
(inv. 21, 38), so the fixture's `tail` stays 0 and the lane proves the decision is taken on
the INSTANT and not on `cov`.

**`bench/backtest_guard_bench.py` — the function.** A new section, **its letter read FROM THE
FILE** (§1a measured it as **K**; confirm it yourself and say so). Known-answer assertions on
`_cell_comparable`: a level is comparable at any gap · `None` is not comparable · 3.0
comparable and 3.1 not, on both signs · the boolean at `+g` equals the boolean at `−g` while
the printed reason carries the sign · every member of `RET_FIELDS` behaves identically ·
**the constant is the only place the three hours live** — set `bb.CMP_GAP_H` to 10.0, assert
the decision at 5 h moves, restore it and assert the restoration.

---

## 6. Validation

Run every item; an item that cannot be run **fails** and is never «not applicable»
(contract §9). Record each baseline figure before the change.

1. `python3 -m py_compile bench/backtest_bench.py bench/verify_bench.py
   bench/backtest_guard_bench.py bench/exhaustion_calib.py` — exit 0.
2. `python3 bench/verify_bench.py` — exit 0, `FAIL 0`. State the total against your measured
   40, the number of added checks, and confirm **no pre-existing assertion was edited or
   removed** (`git diff` on that file shows additions only).
3. `python3 bench/backtest_guard_bench.py` — exit 0, `FAIL 0`. State the new section's letter,
   its check count, step 14 before and after, and the gate total term by term (inv. 43). The
   I9 replacement of §4 is quoted in the report as committed.
4. **The eight lanes, each with its exit code and its class sets** — L2's equality and L3's
   pair stated as equalities, not as two greens.
5. **The pre-repair reading** (inv. 61): run L1's world against the file BEFORE the edit and
   state the exit code, the classes assigned and whether the symbols leave the arms. TZ-42's
   report carries this reading; re-measure it rather than citing it.
6. **Extremes:** empty cache · a `_`-prefixed side file · a field dropped from the live JSON
   for every coin (must still exit non-zero via `never`) · a coin cached and absent from
   `coeffs.json` · **a single-bar series present in BOTH the cache and `coeffs.json`** — it
   must reach `no_build` and change no exit code. TZ-42's run left that coin out of
   `coeffs.json` and the case was never reached; it is reached here or it fails.
7. **The importers of `backtest_bench`** are `verify_bench.py`, `backtest_guard_bench.py` and
   `exhaustion_calib.py`; state the command you used to establish that the set is closed, and
   that the first two are gate steps 4 and 14 while the third is outside the gate by decision.
   `clean_bench.py` and `direction_bench.py` do not import it and are not run for this TZ.
8. `git diff --name-only` names exactly three files, none of them production. Restate the four
   `## 0` hashes measured after the change and the three baselines of §0.

---

## 7. What this TZ does NOT do

- **No production file is touched.** `index.html`, `main.py` and `catalysts.json` appear in no
  diff, and no `coeffs.json` field, window or construction moves.
- **No threshold, no class and no `HARD_CLASSES` entry moves.** `coverage` keeps its meaning
  and its severity; `venue-basis` keeps its own; `_cell_class` and `_cov_hit` are not edited.
- **The universe does not move** (hard floor item 3). Thirty coins, five declared `fut:true`;
  `--target` measures exactly the symbols it measures today.
- **No new refusal and no new exit path** — see `## Not done`.
- **No workflow file is opened** (hard floor item 8).
- **No fetch in this session** (hard floor item 9, inv. 44), and **no forecast about a
  dispatch that has not happened** (inv. 54).

---

## 8. Hard floor clauses this TZ touches — quoted from contract v20

> 2. **Never edit a bench to make it pass.** A red bench is either a product defect or
> a stale expectation; both are findings, neither is a licence to change the
> assertion.

> 8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.

> 12. **Never remove, skip, comment out or `continue-on-error` a bench step to make CI
> green** — editing the assertion (item 2) and deleting the assertion are the same
> act; a step that cannot pass is a finding for the report.

---

## 9. Report requirements

Beyond the §10 template: the guard section's letter and how it was read from the file · the
I9 replacement quoted as committed · the eight lanes with exit codes and class sets · the
pre-repair reading of item 5 · the check counts term by term · `## Fingerprints`, mandatory.

`## Status` is COMPLETED when the eight edits are in, guard I9 is re-registered, the eight
lanes hold and both benches are green offline. The dispatch is the Boss's and its absence is
not PARTIAL (contract §9).

## Commit Message

```
TZ-43: decide comparability per symbol and before the class — an incomparable cell carries no class, the window is two-sided, the basis licence stops covering the tail, and guard I9 is re-registered on the per-cell set
```
