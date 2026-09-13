# TZ-44 — Guard I9 re-registered as a PAIR: the attribution's two structures are read together, and the split between them is asserted

**Canonical filename: `TZ-44-verify-comparability-i9-union.md`.** Name the committed file
from this line, never from the name it arrived under (contract §3).

**Model: Opus.** Unchanged from TZ-43 and for the same reason: `--verify` is the one mode
that can fail in the dangerous direction, and this TZ ships its verdict, its exit code and
the set `--target` gates on.

**TZ-43 is the BASE TEXT and stands in full, except three clauses named in §3.** It executed
and was correctly BLOCKED on one clause of its own §4; report
`CryptoReports/TZ-43-verify-comparability-corrected-report.md` is immutable and accepted as
evidence. Nothing of TZ-43 is retired here but that clause: its §1, §1a, §2, §3, §5, §6 and
§7 are the specification you execute, read from the repository copy this TZ pins in §0. This
is not a restatement — a 363-line document copied to change twenty lines is two documents
that drift (inv. 20).

**Sequencing.** Nothing of TZ-43 was merged, branched or committed: its run left the tree
clean and the three files in scope at their §0 baselines. `main` stood at `6bddc0c` when that
report was written. Your baseline is what you measure.

---

## 0. Fingerprint gate — blocking, before any work

Required map revision, matched as an exact substring against the repository copy
(contract §5):

**Revision 2026-09-13-b.**

The map does not move for this TZ: the revision recording it lands after the report.

Content anchors — all seven, each matched as an EXACT substring. **Report the matched
substring, not the verdict.**

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

**The base text is gated too, and this one is BLOCKING.** You execute TZ-43 by reference, so
a TZ-43 that is not the document this TZ amends makes every reference wrong:

| File | Lines | MD5 |
|---|---:|---|
| `CryptoTZ/TZ-43-verify-comparability-corrected.md` | 363 | `585b634869e69be6d5e0636b44e03165` |

A difference here is **BLOCKED before any work**, stating what you measured.

**Baselines for the files this TZ touches**, unchanged from TZ-43 §0 because nothing was
committed. Benches are absent from the enforced table by decision (map §0): report what you
measure, do not block.

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5008 | `c7fedd64bce7c27c07803325b1f807d3` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
| `bench/backtest_guard_bench.py` | 2438 | `85ea609882ac3761fd526b3ebff2fe5f` |

Contract in force: **v20**, 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0`. Map: 2691
lines, MD5 `7c8b58ec4dea7142104fc9dc0173edcc`. Gate: step 4 (`verify_bench.py`) = **40**
checks, step 14 (`backtest_guard_bench.py`) = **475**.

---

## 1. Why — the retired clause could not hold, and the reason is in the map

TZ-43 §4 asserted that the set of cells `--attrib` compared is a superset of the set
`--verify` declined. The two sides are built from two different field sets, so the relation
is unsatisfiable by construction in the very world it was written for. The map states the
split it missed, §3.10:

> the measure is chosen by FIELD TYPE (levels `rel`, returns `pp`, `eff14` `abs`)

`attrib_run` splits per cell only the `pp` fields — `r7`, `r14`, `r30` — and attributes
`eff14` separately, in its own structure. `nocmp` covers the whole return family, `eff14`
included. The left side can therefore never contain an `eff14` pair, and TZ-43's run measured
exactly that: 486 checks, one red, missing precisely the two `eff14` cells.

**The repair is the pair form inv. 69 requires**, not a narrower comparison:

> **The repaired form is a pair** — the identity re-asserted in the world where it
> holds, and a partition on the live path naming field by field what must differ and what
> must not, both populations non-zero (inv. 22, 68).

So: the identity is re-asserted over BOTH structures the attribution writes, and a second
check asserts the split between them. Restricting the right side to the fields `--attrib`
splits was rejected — it leaves the `eff14` cells `--verify` declines unasserted, and on the
archive those are the cells that carry the defect (map §10, `venue-basis` row).

---

## 2. Guard I9 — the corrected registration, `bench/backtest_guard_bench.py`

**This replaces TZ-43 §4 entirely.** Everything §4 said about WHY the old check is retired
stands: the key it reads is replaced by edit 8, the expectation is stale by decision, the
check count does not fall, and this is not hard-floor item 2 — the assertion that lands is
strictly stronger and the count RISES by one.

Retired text, pristine `bench/backtest_guard_bench.py:2333–2334`:

```
ok('I9. g beyond --verify\'s window: --verify skips the return fields',
   len(AG['skip']) > 0, AG['skip'])
```

**Also retired: the replacement TZ-43 §4 specified**, whose label read
`--attrib compares every cell --verify declines`. It is not written.

### 2a. Read the two structures before writing the code

Before the edit, print and quote in the report the key set of one `AG['cells']` entry and one
`AG['effs']` entry, in I9's own world. The code below reads `c['sym']`, `c['field']`, `c['d']`
and `e['sym']`, `e['d']`. **If an `effs` entry does not carry `sym` and `d`, stop and report
BLOCKED** — do not substitute a key on your judgement (contract §12). This step exists
because the clause this TZ repairs was written against a structure nobody had read.

### 2b. The pair

Written where the retired check stands, both checks inside the same `AG` world:

```
_EFF = 'eff14'
_AG_pp = set((c['sym'], c['field']) for c in AG['cells'] if c['d'] is not None)
_AG_eff = set((e['sym'], _EFF) for e in AG['effs'] if e['d'] is not None)
_AG_nc = set((s, f) for s, f, _, _ in AG['nocmp'])
ok('I9. g beyond --verify\'s window: --attrib measures every cell --verify declines',
   len(AG['nocmp']) > 0 and (_AG_pp | _AG_eff) >= _AG_nc,
   (len(AG['nocmp']), sorted(_AG_nc - (_AG_pp | _AG_eff))))
_AG_ppf = set(c['field'] for c in AG['cells'])
ok('I9b. --attrib splits the return family in two: the per-cell fields, and eff14 in its own structure',
   len(AG['cells']) > 0 and len(AG['effs']) > 0 and _AG_ppf == set(bb.RET_FIELDS) - set([_EFF]),
   (sorted(_AG_ppf), len(AG['cells']), len(AG['effs'])))
```

- **I9** is the identity, re-asserted over the union of the two structures. Its non-empty
  clause is unchanged: `nocmp` must be populated or the check proves nothing (inv. 22).
- **I9b** is the partition, and it is the check whose absence cost TZ-43 a session: it reads
  the family from the module constant edit 1 creates and asserts that `--attrib`'s per-cell
  field set is exactly the family minus `eff14`, with both structures non-empty. A future
  change that moves `eff14` into `cells` turns I9b red naming the move, instead of turning
  I9 red naming a symbol.
- `_AG_ppf` is built from **every** cell, not only those with a Δ formed: the claim is about
  which fields the attribution splits, not about which ones produced a number in one world.
- The comment block above the check (pristine lines 2325–2328) names the old cache-wide skip
  and is updated to name the two structures, in the same edit.

**The checks that follow I9 in that world are FOUR, not two** — pristine lines 2335, 2339,
2341 and 2345. TZ-43 §4 said two; that was a counting slip and is corrected here. All four
are unchanged and must stay green; name each by its label in the report.

**If either check of the pair cannot be made to hold, that is a finding and a BLOCKED
verdict — never a weaker assertion.**

---

## 3. What changes in TZ-43's own text — the complete delta

Three clauses, and nothing else:

1. **§4 in full** → replaced by §2 above.
2. **§6 item 3** → its sentence «The I9 replacement of §4 is quoted in the report as
   committed» reads: the corrected I9 **and I9b** of TZ-44 §2b are quoted in the report as
   committed. The rest of item 3 stands, amended by §5 below for the arithmetic.
3. **`## Commit Message`** → replaced by the block at the end of this TZ.

TZ-43 §9's `## Status` condition reads with the pair substituted: COMPLETED when the eight
edits are in, **guard I9 is re-registered as the pair and I9b is green**, the eight lanes
hold and both benches are green offline.

---

## 4. Scope

**Files to Modify:** `bench/backtest_bench.py`, `bench/verify_bench.py`,
`bench/backtest_guard_bench.py`.
**Files to Create:** none. **Files to Delete:** none.

No production file is in scope. `.github/workflows/**` is not named by this TZ and is
therefore closed to it (hard floor item 8).

### `## Touches`

Unchanged from TZ-43 §2: `--target` and `--regime-gate` each gain one printed line and
neither changes which symbols it measures; `--attrib` has one key of its return dict replaced
and no term, population, printed field or exit rule of the attribution moves;
`bench/exhaustion_calib.py` is compiled, never run and never edited.

---

## 5. Validation — TZ-43 §6 in full, with these amendments

Every one of TZ-43's eight items is run as written. An item that cannot be run **fails** and
is never «not applicable» (contract §9). The amendments:

- **Item 3 — the arithmetic moves.** Expected: section I **94 → 95** (I9 replaced one for
  one, I9b added), section K **11**, step 14 **475 + 1 + 11 = 487**. State the measured
  figures term by term (inv. 43); a figure that differs from this arithmetic is a finding for
  the report, never an edit.
- **Item 3 — the union is load-bearing, stated as a measurement.** In I9's world, report both
  booleans: `_AG_pp >= _AG_nc` must be **False** and `(_AG_pp | _AG_eff) >= _AG_nc` must be
  **True**. A check that would be green without the repair is not evidence of the repair
  (inv. 22, 68).
- **New item 9 — the structures as read.** The key sets of §2a, quoted, with the command that
  printed them.
- **Item 4 stands unchanged and its count is EIGHT** — L1, L2, L3, L4, L6, L7, L7b, L8. TZ-43
  §5 skips L5 deliberately, so no lane is missing; report each of the eight by name, with its
  exit code and class sets, and L2's equality and L3's pair stated as equalities.

---

## 6. Hard floor clauses this TZ touches — quoted from contract v20

> 2. **Never edit a bench to make it pass.** A red bench is either a product defect or
> a stale expectation; both are findings, neither is a licence to change the
> assertion.

> 8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.

> 12. **Never remove, skip, comment out or `continue-on-error` a bench step to make CI
> green** — editing the assertion (item 2) and deleting the assertion are the same
> act; a step that cannot pass is a finding for the report.

Item 2 is the clause this TZ is closest to and does not touch: the retired check is retired
by the Architect in writing, its replacement asserts strictly more than it did, and the
check count rises.

---

## 7. What this TZ does NOT do

- **No production file is touched.** `index.html`, `main.py` and `catalysts.json` appear in
  no diff, and no `coeffs.json` field, window or construction moves.
- **No threshold, no class and no `HARD_CLASSES` entry moves**, and `attrib_run`'s own
  behaviour, terms and printed prose are unchanged — only guard code reads its structures
  differently.
- **The universe does not move** (hard floor item 3).
- **No workflow file is opened** (hard floor item 8).
- **No fetch in this session** (hard floor item 9, inv. 44), and **no forecast about a
  dispatch that has not happened** (inv. 54).

---

## 8. Report requirements

TZ-43 §9 in full, with two additions: the key sets of §2a quoted; and the two booleans of §5
reported side by side. `## Fingerprints` is mandatory and adds
`CryptoTZ/TZ-44-verify-comparability-i9-union.md` to the set TZ-43 §0 lists.

## Commit Message

```
TZ-44: decide comparability per symbol and before the class — guard I9 is re-registered as a pair, reading both structures the attribution writes and asserting the split between them
```
