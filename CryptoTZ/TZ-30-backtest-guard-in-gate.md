# TZ-30 — The backtest garrison moves into the tree and into the gate

**Canonical filename: `TZ-30-backtest-guard-in-gate.md`.** Name the committed file from
this line, never from the name the upload produced (contract §3).

**Class: branch TZ** — it writes files outside `CryptoReports/**`, so it opens a branch
and a pull request (contract §8). **Model: Opus** — three files, a CI edit, a refactor
carrying an identity argument, and a mandatory negative test.

---

## 0. Fingerprint gate — blocking, before any work

`git fetch --all --prune`, then match every string below against `origin/main`
(contract §5). Any mismatch → **BLOCKED**, no work.

**Revision string, enforced:**

```
**Revision 2026-09-05-b.**
```

**Content anchors, all seven, each an exact substring of `SYSTEM-MAP-CRYPTOCALCUL.md`:**

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-05-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `64. **A tail top-up must serve the instrument it tops up.**` |

**The map's `## 0` file table — measure each, report, do not act on a difference:**

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Two figures this TZ needs that the map's table deliberately does not carry**, stated
here as the map instructs (`## 0`: «A TZ needing the figure states it in its own `§0`»):

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 3216 | `1b921e88fdae5c1c404fbf9fbcee8b2c` |
| `EXECUTOR-INSTRUCTIONS.md` (v19) | 801 | `a6ebc2e7c2f2b74e813dfdc20400558f` |

A difference in either is reported under `## Pre-existing Issues` and is not acted on.

---

## 1. Why

`bench.yml` runs thirteen steps and **not one of them builds a JS bundle.** Step 4's
`verify_bench.py` imports `backtest_bench.py`, which proves the module imports; it does
not prove that `extract_js` still finds what it cuts. So `_assert_js_closed` — the one
check that catches a cut that has fallen behind `index.html` — never fires where
something already runs. That is the residual of inv. 62, and the map owns it as an open
row.

TZ-29 widened the same hole. The coverage census, the derived splice rule and the
`--target` reconciliation gate were proved by a harness that was never authorised as a
file, so it does not exist in the tree. **A harness outside the tree is not evidence for
the next session** (inv. 37), and the three rules it proved are today locked only by the
validation run of a TZ that has closed.

This TZ moves that garrison into `bench/` and wires it into the gate in the same change,
which hard floor item 12 requires of any new bench.

---

## 2. Scope — the complete authorisation

**Files to Create**

- `bench/backtest_guard_bench.py`

**Files to Modify**

- `bench/backtest_bench.py` — two named refactors, §3 below. Nothing else.
- `.github/workflows/bench.yml` — one new step, one `paths-ignore` line, one header
  repair, §5 below. Nothing else.

**Files to Delete** — none.

Not authorised, and each is named because it is the obvious next thought: `index.html`,
`main.py`, `catalysts.json`, `.gitignore`, `bench/verify_bench.py`, any other bench,
`.github/workflows/backtest_bench.yml` (hard floor item 8), `analyst/**` (§5.2 below),
`SYSTEM-MAP-CRYPTOCALCUL.md`, `EXECUTOR-INSTRUCTIONS.md`.

**No new dependency and no new build step** (contract §14). The gate's `Зависимости`
step already installs `numpy` and `requests`; the new bench needs neither beyond what
importing `backtest_bench.py` already pulls, and it opens no socket.

**The new bench gets no fingerprint entry in the map's `## 0` file table.** Its control
is being a gate step, not a fingerprint entry — the argument §11 already makes for
`analyst/live-gate.sh`: a hash in every TZ header for a file that moves whenever a bench
moves buys nothing.

---

## 3. Stage 1 — two refactors in `bench/backtest_bench.py`

Both are pure moves. Neither changes a number, a threshold or an output line.

### 3.1 One place for the failing classes (inv. 20)

The set «which reconciliation classes are a failure» is written twice today. In
`verify_against_live`:

```python
    hard = R["classes"]["coverage"] + R["classes"]["unexplained"]
```

and in `main()` under `if a.target:`:

```python
        excluded = dict((sy, cl) for sy, cl in R["sym_class"].items()
                        if cl in ("coverage", "unexplained") and sy in ser)
```

Two literals for one rule diverge eventually, and the direction of that divergence is
`--target` measuring a symbol `--verify` refused. Add, immediately after the existing
`CLASSES` definition:

```python
# The classes that FAIL. `venue-basis` is reference (§3.14) and is not here.
# One place, because --verify's exit code and --target's arm gate are the same
# rule read twice (inv. 20): a set that drifted would let --target measure a
# symbol --verify refused.
HARD_CLASSES = ("coverage", "unexplained")
```

Rewrite both sites to read it. `verify_against_live` becomes:

```python
    hard = sum((R["classes"][c] for c in HARD_CLASSES), [])
```

The `main()` site is replaced by the call in §3.2. `CLASSES` keeps its own order — it is
severity order and drives the printed table; `HARD_CLASSES` is a membership set, not a
second ordering.

### 3.2 The `--target` arm gate becomes a function

The gate is five lines inside `main()`, so nothing can reach it without a warm cache, a
BTC series and three node bridges. Lift it, unchanged, to a module-level function placed
**immediately after `verify_against_live` and before `load_cache`**:

```python
def target_gate(sym_class, symbols):
    """Which symbols --target may measure, given the reconciliation's verdict.

    §2.6 authorises removing `coverage` and `unexplained` and NOTHING else, so
    the removed set is read from HARD_CLASSES rather than from this function's
    own judgement. A symbol the reconciliation never saw is NOT removed — it is
    returned separately to be named, because an unreconciled symbol and a
    refused one are different facts and silence would merge them (inv. 22, 37).

    Pure: it mutates neither argument. Returns
    (excluded {symbol: class}, unrec [symbols the reconciliation never saw]).
    """
    keep = set(symbols)
    excluded = dict((sy, cl) for sy, cl in sym_class.items()
                    if cl in HARD_CLASSES and sy in keep)
    unrec = sorted(sy for sy in keep
                   if sy not in sym_class and sy not in excluded)
    return excluded, unrec
```

`main()` then reads:

```python
        excluded, unrec = target_gate(R["sym_class"], ser)
        for sy in excluded:
            ser.pop(sy, None)
```

and everything after it — the `СВЕРКА ПЕРЕД ЗАМЕРОМ` line, the `НЕ СВЕРЕНО` line, the
`len(ser) < 8` stop, the `target_summary(..., excluded=excluded)` call — is untouched.

**Why this is an identity and not a behaviour change.** Today `unrec` is computed after
the pops, over the reduced `ser`. Every excluded symbol is by construction a key of
`sym_class`, so it could never have been in `unrec` either way; the extra
`sy not in excluded` term above is therefore redundant on real input and is written only
so the function is correct read alone. The old and the new produce the same two objects
on every input, which §6 requires to be demonstrated rather than asserted.

---

## 4. Stage 2 — `bench/backtest_guard_bench.py`

A new offline bench, in the idiom of `bench/verify_bench.py`: English throughout, a
module docstring naming what it locks, `requests` stubbed, one counter incremented at
each comparison site, a summary line, a zero-comparison guard, a non-zero exit on any
failure.

```
python3 bench/backtest_guard_bench.py [path/to/backtest_bench.py] [path/to/index.html]
```

Load `backtest_bench.py` by `importlib` from the given path exactly as `verify_bench.py`
does. **Never re-implement a rule this bench checks** (inv. 21, 38): every assertion
calls the production-bench function by name and compares its return, and every fixture
is synthetic input to that function.

### 4.1 Section A — the four bundles build and close

This is the inv. 62 residual and the reason the gate is being opened at all.

Build all four bundles from the checkout's real `index.html`, through the same code the
real modes use, capturing stdout so the printed closure line can be read:

| Bundle | Built by |
|---|---|
| `_score_bridge.js` | `bb.JsScorer(html)` |
| `_inv_bridge.js` | `bb._extract_js_set(html, bb.INV_JS_FUNCS, bb.INV_JS_VARS, bb.INV_DRIVER, "_inv_bridge.js")` |
| `_res_bridge.js` | `bb._extract_js_set(html, bb.RES_JS_FUNCS, bb.RES_JS_VARS, bb.RES_DRIVER, "_res_bridge.js")` |
| `_tgt_bridge.js` | `bb._extract_js_set(html, bb.TARGET_JS_FUNCS, bb.TARGET_JS_VARS, bb.TARGET_DRIVER, "_tgt_bridge.js")` |

Per bundle, two checks: the build raises nothing, and its printed line
`замкнутость <name>: сверено N обращений` carries `N > 0`. `JsScorer` and
`_extract_js_set` both run `node --check` on what they wrote, so a bundle that builds and
closes is also proved syntactically valid.

**Negative control (inv. 23), in the shape inv. 60 names: a known-answer control that
removes a name from each half and must raise.** Call `bb._assert_js_closed` directly,
three times, each of which must raise `RuntimeError`:

a. a bundle with one `function NAME(` definition removed from its text, the real driver
   beside it — the raise must name that identifier;
b. the real bundle with a driver whose `var` declaration of a name the bundle reads has
   been removed;
c. an empty bundle with an empty driver — the raise must be the inv. 22 message, not a
   silent pass.

A control that fails to raise is a failure of this bench. Both halves are exercised
because the check's `known` set is the union of two texts, and a check that only ever
loses names from one of them has never been proved on the other.

**Take the names for cases a and b from the bundle's own text, never typed:** the first
`function NAME(` the assembled bundle declares, and the first `var NAME` the driver
declares. A typed name goes stale the day production renames a helper, which is the
class of defect this whole section exists to catch.

### 4.2 Section B — the coverage census

**B1, `_vision_rows` offline.** Stub `requests` with a fake whose `get` serves the
fixture and **records every URL it was asked for**, since half the rules here are about
requests that must NOT happen. Build monthly and daily payloads as real ZIPs in memory
(`zipfile` over a CSV in the twelve-column layout `_rows_from_zip` reads), and serve 404
where the fixture says the file is absent. Lock:

1. **Every absent month is refilled, not only the last.** A window of three months where
   the middle month's monthly ZIP answers 404 while its dailies answer 200 must return
   that month's hours; the recorded URLs must contain that month's daily paths.
2. **Pre-listing months are not refilled.** A month before the first month that answered
   200 must produce no daily request at all — assert the recorded URL list, not the row
   count, because zero rows is also what a failed fetch looks like.
3. **`gone` counts the months whose monthly ZIP was absent**, including the ones the
   dailies then covered.
4. **A perpetual is never topped up from the spot mirror** (inv. 64): with `is_fut=True`
   and a tail short of the last complete hour, the recorded URLs must contain no
   `data-api.binance.vision` entry and no `fapi` entry of any kind, and the returned
   `note` must be non-empty.
5. **A spot series is topped up from `data-api.binance.vision/api/v3/klines`** and from
   no other host.
6. **The top-up stops at the last complete hour**: with `t_end` set mid-hour and the REST
   fixture offering a row for the hour in progress, no returned row carries a stamp at or
   after the last complete hour.

**B2, the census functions** — `census`, `census_of_doc`, `_cov_hit` — on hand-built
bucket dictionaries with known answers:

7. tail is counted to the last complete hour and not to `t_ref`: moving `t_ref` within
   one hour does not move `tail`;
8. an interior gap is reported with its own start, end and length; `n_gaps` counts gaps,
   `inside` sums their hours, `max_gap` is the longest;
9. a series with no gap reports `n_gaps 0`, `inside 0`, `max_gap None` — and a non-zero
   `hours`, so the case is not passing on an empty series;
10. `census_of_doc` on a document built from the same buckets returns the same census as
    `census` on those buckets — the cache path and the live path are one measure;
11. `_cov_hit` returns a tail reason whenever `tail > 0`, whatever the window;
12. `_cov_hit` returns a gap reason only when the gap ends inside the field's own window,
    and `None` when it ends before it — one case each side of the boundary;
13. `_cov_hit(None, …)` returns `None`.

### 4.3 Section C — the splice rule (inv. 63)

All against `bb._splice(old_rows, new_rows)` on synthetic two-leg row lists.

14. **ADMITTED**: a joint return inside the extremes the two legs themselves exhibit —
    `ok True`, `why` names the admission, and `rows` is the pre-cut old leg followed by
    the whole new leg.
15. **REFUSED**: a joint return far outside those extremes, the redenomination shape —
    `ok False`, and `rows` is the new leg alone, unmodified.
16. **The extremes are taken inside each leg and never across the joint.** Construct a
    case where including the joint's own return in the extremes would admit it and
    excluding it refuses; assert the refusal. This is the clause with no other witness:
    every other case passes under either reading.
17. `cut` is read from the data — it equals the first bucket of the new leg, on a fixture
    where the two legs overlap so a declared cutover would land elsewhere.
18. no new leg → `ok False` with its own `why`; no pre-cut old leg → `ok False` with its
    own `why`; a non-positive price at the joint → `ok False`.
19. **No adjacent hourly pair in either leg → `ok False`** with the inv. 22 reason. A rule
    with nothing to compare against must not admit.
20. **Identity control (inv. 45): split-then-splice reproduces the original.** Cut one
    continuous hourly series at an arbitrary interior hour into two legs, splice them,
    and assert the returned `rows` equal the original list. A comparator never proved on
    identity supports no claim about a real joint, and this case also proves the row
    reconstruction rather than only the verdict.

### 4.4 Section D — the `--target` arm gate

Against `bb.target_gate` and `bb._excl_line` from stage 1. **This section does not
re-test the classifier**: which cell earns which class is locked by
`bench/verify_bench.py` cases 9 and 10, and a second control over one rule is the defect
inv. 20 names. What is locked here is what the gate DOES with a class.

21. **The case table is derived from `CLASSES`, not typed** — read `bb.CLASSES` at run
    time. Build one symbol per
    class in `bb.CLASSES`, plus one `clean` symbol, plus one symbol present in the cache
    with no reconciliation row. Assert every member of `bb.CLASSES` is covered by the
    table and fail if a class appears that the table does not name — a class added later
    must turn this bench red rather than pass unexamined.
22. Symbols whose class is in `bb.HARD_CLASSES` are excluded, with their class as the
    value; `venue-basis` and `clean` are kept. Assert against `bb.HARD_CLASSES`, so the
    expectation moves with the constant instead of restating it.
23. A symbol carrying a failing class but absent from the cache does not appear in
    `excluded`.
24. A symbol present in the cache with no reconciliation row is **kept and named in
    `unrec`** — never silently excluded.
25. `target_gate` mutates neither argument: compare both inputs against copies taken
    before the call.
26. `_excl_line` on an empty exclusion set prints the «ничего» wording; on a populated
    one it names each class with its count and its symbols. A withheld verdict must be
    readable as «removed by the reconciliation», never as «the market gave nothing».

### 4.5 Counting, exit and hygiene

- One counter, incremented at the comparison site, printed as
  `checks run: N   FAIL M` followed by one line per failure (inv. 43).
- `sys.exit(1 if fails else 0)`, and a guard that prints a failure and exits non-zero if
  the counter is zero (inv. 22, 29).
- **State no expected total in this TZ and predict none in the report.** The published
  figure is the measurement and never a prediction (inv. 43); the map records what a
  predicted bench count cost once already, when a step forecast at +4 measured +1 630.
- Every temporary file the run created — the four `bench/_*_bridge.js` files, any
  scratch directory — is removed before exit, and `git status` is clean afterwards
  (contract §8).
- No network, no `bench/cache/`, no writes outside a temporary directory.

---

## 5. Stage 3 — `.github/workflows/bench.yml`

### 5.1 The new step

Append as the **last** step, so steps 1–13 keep their numbers and the map's per-step
attribution table stays valid:

```yaml
      # ТЗ-30. Гарнизон backtest_bench.py: замкнутость всех четырёх связок,
      # перепись покрытия, арифметика склейки и гейт рукавов --target. Сети шагу
      # не нужно — requests подменяется, архив синтетический, index.html берётся
      # из чекаута. Именно этот шаг закрывает остаток инв. 62: ворота впервые
      # СОБИРАЮТ связку, а не только импортируют модуль.
      - name: Гарнизон бэктеста (backtest_guard_bench.py)
        shell: bash -euo pipefail {0}
        run: python3 bench/backtest_guard_bench.py
```

### 5.2 One line in `paths-ignore`

The current block is:

```yaml
      # Данные аналитика: состояние, журнал и payload от шортката.
      # Скрипт шлюза сюда не входит намеренно — его контроль это шаг 13.
      - 'analyst/state.json'
      - 'analyst/live.json'
      - 'analyst/log/**'
```

Add `analyst/owner.json` to it, as a literal path, with the reason in the comment: the
file is the owner's channel into the engine, uploaded by the Boss, read by an analysis
run and never a control, so every upload of it currently fires the whole gate. A literal
is used rather than a glob for the reason inv. 52 gives — two exact strings compare equal
or they do not.

**The Executor never writes `analyst/owner.json`.** It is not named under
`Files to Modify`, so §6 forbids touching it; this stage edits the workflow's list and
nothing under `analyst/`. The file arrives by Boss upload, which is why it fires the gate
today. **The runner reading that inv. 53 requires is not a validation item of this TZ**
and its absence is not a PARTIAL: the proof is a real push carrying only that file, the
only actor who may make that push is the Boss, and the reading belongs to the audit of
his next upload after the merge.

`analyst/owner.json` has no row in the contract's §2 class table. That is a defect of
that file, not of this TZ and not a reason to block: report it under
`## Pre-existing Issues`, name no class for it, and create nothing. The repair is the
Architect's.

### 5.3 The header comment now denies a mechanism that exists

The file's header currently reads, among the benches left outside the gate:

```
#   backtest_bench.py  — нужен архив/кэш, обслуживается backtest_bench.yml
```

After this change that sentence is a stated absence that has become false (inv. 50):
`backtest_bench.py` itself still runs only under `backtest_bench.yml`, but four of its
rules are now under the gate. Repair the line in the same change — keep the true half,
and add that the bundle build, the coverage census, the splice rule and the `--target`
arm gate are held by `backtest_guard_bench.py` at the last step. Do not enumerate the
individual checks there; a list in a comment is a second list (inv. 20).

---

## 6. Validation — run every item; an item that cannot be run FAILS

1. `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py`.
2. `python3 bench/backtest_guard_bench.py` — exit 0, zero failures, and the printed
   check count recorded verbatim as a **measurement**.
3. **The stage-1 identity, demonstrated not asserted.** Against `origin/main`'s
   `backtest_bench.py` and the new one, run `target_gate`'s inputs through both forms —
   the old inline expression evaluated in a scratch script and the new function — over a
   case set covering every member of `CLASSES`, `clean`, an unreconciled symbol and a
   failing symbol absent from the cache, and report zero differences in both returned
   objects. A differ that has never returned zero on identical input proves nothing
   (inv. 45).
4. `python3 bench/verify_bench.py` — unchanged check count against `origin/main` and
   zero failures. This is the no-regression evidence for stage 1: `verify_against_live`
   was edited, and `verify_bench.py` is its control.
5. **Full local replay of `bench.yml`, now fourteen steps**, each with its own recorded
   count and exit code. Steps 1–13 must read **delta zero** against the map's figure of
   **13 steps, 1 255 401 checks**; step 14 reports its own measured count. Any step whose
   count moved is explained term by term or the TZ is PARTIAL (inv. 43).
6. **Negative test, mandatory for any TZ touching CI** (contract §9). Three injected
   failures, one per class of control, each reverted with a clean tree afterwards:
   - remove one name from `JS_FUNCS` in a scratch copy of `index.html` and point the
     bench at it → section A must go red naming that identifier, and the step must exit
     non-zero;
   - invert the admissibility comparison in `_splice` in a scratch copy of
     `backtest_bench.py` → section C must go red;
   - add `"venue-basis"` to `HARD_CLASSES` in a scratch copy → section D must go red.
   After each: revert, re-run, confirm green and `git status` clean. A gate never proven
   to fail is not a gate.
7. `node --check` on the `<script>` block extracted from `index.html`, and
   `python3 -m py_compile main.py`. Both production files are outside scope and must
   fingerprint identically to §0 at the end of the session — that equality is the
   no-regression statement for production.
8. `bench.yml` parses as YAML and its job carries exactly fourteen `- name:` bench steps
   in the order given, with `analyst/owner.json` present in `paths-ignore` as an exact
   literal.
9. `git status` clean: no bridge file, no `__pycache__`, no scratch copy committed.

---

## 7. What this TZ does NOT close — state it in the report

**The closure check catches a stale CUT, not a stale RESULT.** After this change the gate
proves that every function `backtest_bench.py` cuts still exists in `index.html` and that
each bundle is closed under reference. It proves nothing about the arithmetic inside
those functions: production may change what `qualityScore` computes, every bundle will
still build and close, and the standing results remain what they were measured on. The
wider half of inv. 62 — a manual workflow decaying from upstream — is narrowed here, not
retired.

Report this under `## Remaining Risks`, in those terms. A row that closes on a wider
claim than the work supports is worse than an open row.

---

## 8. Commit Message

This section is the `## Commit Message` contract §8 sends you to; the string below is
committed verbatim.

```
TZ-30: backtest garrison in the tree and in the gate (step 14)
```

---

## 9. Report requirements beyond the template

- `## Scope Executed` names the class — **branch TZ** — before any clause reads off it.
- `## Fingerprints` carries `SYSTEM-MAP-CRYPTOCALCUL.md` with its revision string, all
  four files of the map's `## 0` table, and `bench/backtest_bench.py` and
  `EXECUTOR-INSTRUCTIONS.md` at the figures this TZ's §0 adds.
- `## Test Results` carries the fourteen step counts as a table, with the delta against
  1 255 401 stated as a subtraction, and the three negative-test outcomes each with the
  command that produced them.
- `## Remaining Risks` carries §7 above and the `analyst/owner.json` reading that belongs
  to the audit, named as owed rather than as done.
- The hosted gate is read by the audit, not by the session (contract §9). State that the
  branch was pushed and that the changed paths clear the workflow's filters; write no
  forecast about a run you cannot read.
