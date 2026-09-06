# Implementation Report — TZ-30

## Status

**COMPLETED.**

All three stages of `CryptoTZ/TZ-30-backtest-guard-in-gate.md` are implemented and all
nine validation items of its §6 were run and passed. The fingerprint gate (§5 of the
contract, §0 of the TZ) passed on every enforced string and on every measured file,
including the two figures the TZ's §0 adds.

The previous TZ's branch was merged: `claude/tz-29-archive-coverage-and-verify-reconciliation`
landed on `main` as pull request #27, merge commit `fa0b8fc`. This work is built on a
merged base.

---

## Inbound Filing

None. `CryptoTZ/TZ-30-backtest-guard-in-gate.md` arrived on `origin/main` in commit
`60ce04d` («Add files via upload») already at its canonical filename — the name the TZ's
own header states. Nothing was moved and nothing was renamed.

The session's checkout was one commit behind that upload and was brought to
`origin/main` by fast-forward before any assessment (`git fetch --all --prune`, then
`git merge --ff-only origin/main`: `bf38628..60ce04d`). The clone is not shallow
(`git rev-parse --is-shallow-repository` → `false`).

---

## Scope Executed

**Class: branch TZ.** The scope names three files outside `CryptoReports/**` —
`bench/backtest_guard_bench.py` created, `bench/backtest_bench.py` and
`.github/workflows/bench.yml` modified — so the class is read off the scope and this
change opens a branch. Every clause below that speaks of a branch, a pull request or a
merge is read off that class.

| Stage | TZ § | What was done |
|---|---|---|
| 1 | §3.1 | `HARD_CLASSES` added immediately after `CLASSES`; `verify_against_live` rewritten to read it |
| 1 | §3.2 | the `--target` arm gate lifted out of `main()` into module-level `target_gate`, placed after `verify_against_live` and before `load_cache`; `main()` rewritten to call it |
| 2 | §4 | `bench/backtest_guard_bench.py` created — sections A, B, C, D, 94 comparisons |
| 3 | §5.1 | new last step in `bench.yml`, so steps 1–13 keep their numbers |
| 3 | §5.2 | `analyst/owner.json` added to `paths-ignore` as an exact literal |
| 3 | §5.3 | the header line about `backtest_bench.py` repaired |

Nothing outside that list was touched. The files the TZ names as the obvious next
thought — `index.html`, `main.py`, `catalysts.json`, `.gitignore`,
`bench/verify_bench.py`, any other bench, `.github/workflows/backtest_bench.yml`,
`analyst/**`, `SYSTEM-MAP-CRYPTOCALCUL.md`, `EXECUTOR-INSTRUCTIONS.md` — are all
byte-identical to `origin/main` at the end of the session. No new dependency and no new
build step: the gate's `Зависимости` step already installs `numpy` and `requests`, and
the new bench opens no socket.

The new bench gets **no fingerprint entry in the map's `## 0` file table**, as §2 of the
TZ directs: its control is being a gate step.

---

## Files Created

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_guard_bench.py` | 580 | `93c2726342e9f8b59579d0ba707a8a52` |

## Files Modified

| File | Lines before → after | MD5 after |
|---|---|---|
| `bench/backtest_bench.py` | 3216 → 3240 | `d2dad0f80afa2c191c2faf1d40081a88` |
| `.github/workflows/bench.yml` | 135 → 153 | `d182e514dcceda5c64410beabc9fe512` |

`git diff --stat origin/main..HEAD`: 3 files changed, 627 insertions(+), 5 deletions(-).

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Stage 1 — two pure moves in `bench/backtest_bench.py`

**§3.1, one place for the failing classes.** `HARD_CLASSES = ("coverage", "unexplained")`
is defined immediately after `CLASSES`, carrying the comment the TZ specifies verbatim.
`verify_against_live`'s `hard = R["classes"]["coverage"] + R["classes"]["unexplained"]`
became `hard = sum((R["classes"][c] for c in HARD_CLASSES), [])`. `CLASSES` keeps its own
order — it is severity order and drives the printed table.

**§3.2, the arm gate becomes a function.** The five lines inside `main()` are now
module-level `target_gate(sym_class, symbols)`, placed after `verify_against_live` and
before `load_cache`, with the docstring the TZ specifies. `main()` reads

```python
        excluded, unrec = target_gate(R["sym_class"], ser)
        for sy in excluded:
            ser.pop(sy, None)
```

and everything after it — the `СВЕРКА ПЕРЕД ЗАМЕРОМ` line, the `НЕ СВЕРЕНО` line, the
`len(ser) < 8` stop, the `target_summary(..., excluded=excluded)` call — is untouched.
Neither move changes a number, a threshold or an output line. The identity is
demonstrated, not asserted, under validation item 3 below.

### Stage 2 — `bench/backtest_guard_bench.py`

Offline, in the idiom of `bench/verify_bench.py`: English throughout, module docstring
naming what it locks, `requests` stubbed, one counter incremented at each comparison
site, a summary line, a zero-comparison guard, non-zero exit on any failure. It loads
`backtest_bench.py` by `importlib` from the given path and **never re-implements a rule
it checks** — every assertion calls the production function by name and compares its
return, and every fixture is synthetic input to that function.

`backtest_bench.HERE` is redirected to a scratch directory before section A, so the
bridge files the real builders write land there and leave with it. Nothing is written
outside that directory; `bench/cache/` is never read or created; no socket is opened.

| Section | What it locks | Checks |
|---|---|---:|
| A | the four bundles build and close; three negative controls | 17 |
| B1 | `_vision_rows` offline — refill, pre-listing, `gone`, inv. 64, mirror host, last complete hour | 18 |
| B2 | `census`, `census_of_doc`, `_cov_hit` on hand-built buckets | 16 |
| C | `_splice` — admission, refusal, extremes inside each leg, derived `cut`, degenerate legs, identity | 19 |
| D | `target_gate` and `_excl_line` — what the gate DOES with a class | 24 |
| | **total** | **94** |

Section A builds all four bundles through the same code the real modes use —
`JsScorer(html)` for `_score_bridge.js` and `_extract_js_set` for the inv., res. and
target bundles — capturing stdout so the printed
`замкнутость <name>: сверено N обращений` can be read and `N > 0` asserted. Both
builders run `node --check` on what they wrote, so a bundle that builds and closes is
also proved syntactically valid. The names used by the negative controls are taken from
the bundle's and the driver's own text at run time, never typed.

Section D does **not** re-test the classifier: which cell earns which class is locked by
`bench/verify_bench.py` cases 9 and 10. What is locked here is what the gate does with a
class, and the expectation is read from `bb.HARD_CLASSES` so it moves with the constant.
Two anchors are the exception and are described under **Deviations** below.

Every temporary artifact is removed before exit: the scratch tree is deleted, and any
`bench/_*_bridge.js` is unlinked as a second line of defence. `git status` is clean after
every run recorded in this report.

### Stage 3 — `.github/workflows/bench.yml`

The new step is appended **last**, so steps 1–13 keep their numbers and the map's
per-step attribution table stays valid. The comment above it is Russian, following the
file's established language (contract §Language, third exception).

`analyst/owner.json` is added to `push.paths-ignore` as an exact literal with the reason
in the comment. **The Executor did not write `analyst/owner.json`** — it is not named
under `Files to Modify` and was not touched; this stage edited the workflow's list and
nothing under `analyst/`.

The header line

```
#   backtest_bench.py  — нужен архив/кэш, обслуживается backtest_bench.yml
```

was a stated absence that this change made false (inv. 50). It now keeps the true half —
`backtest_bench.py` itself still runs only under `backtest_bench.yml` — and adds that the
bundle build, the coverage census, the splice rule and the `--target` arm gate are held
by `backtest_guard_bench.py` at the last step of these gates. The individual checks are
not enumerated there: a list in a comment is a second list (inv. 20).

---

## Validation

Every item of the TZ's §6 was run. All commands were run from the session's worktree at
commit `7fdd7db`, against the artifacts as committed.

| # | Item | Result |
|---:|---|---|
| 1 | `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` | exit 0 |
| 2 | `python3 bench/backtest_guard_bench.py` | exit 0, **`checks run: 94   FAIL 0`** |
| 3 | stage-1 identity, demonstrated | 100 000 cases, **0 differences**; differ proved able to see one |
| 4 | `python3 bench/verify_bench.py` | exit 0, `checks run: 35   FAIL 0` — unchanged against `origin/main` |
| 5 | full local replay of `bench.yml`, fourteen steps | steps 1–13 **delta zero**; step 14 = 94 |
| 6 | negative test, three injected failures | all three red and non-zero; all three reverted clean and green |
| 7 | `node --check` on the `<script>` block · `py_compile main.py` · production fingerprints | exit 0 · exit 0 · identical to §0 |
| 8 | `bench.yml` parses; fourteen bench steps in order; `analyst/owner.json` literal present | pass |
| 9 | `git status` clean | pass |

**Item 3 in detail.** The old inline expression was not retyped: it was cut by text out
of `origin/main`'s `bench/backtest_bench.py` and `exec`'d in a namespace shaped like
`main()`'s, so what ran on the left is the code that was there:

```
        excluded = dict((sy, cl) for sy, cl in R["sym_class"].items()
                        if cl in ("coverage", "unexplained") and sy in ser)
        for sy in excluded:
            ser.pop(sy, None)
        unrec = sorted(sy for sy in ser if sy not in R["sym_class"])
```

The case set is the exhaustive product of five symbols over ten per-symbol states — each
member of `CLASSES`, `clean`, and no reconciliation row at all, each of those either
present in the cache or absent — which is 100 000 cases and covers `clean`, `coverage`,
`unexplained`, `venue-basis`, an unreconciled symbol and a failing symbol absent from the
cache, in every combination:

```
cases compared           : 100000
classes exercised        : ['clean', 'coverage', 'unexplained', 'venue-basis']
differences in `excluded`: 0
differences in `unrec`   : 0
differences in the kept  : 0
control (differ vs a KNOWN-wrong gate): 40951 differences seen
```

The last line is the point inv. 45 makes: the same harness was re-run against a
deliberately wrong gate (one that also removes `venue-basis`) and reported 40 951
differences, so the zeros above are a measurement and not a blind differ.

**Item 5 in detail.** The replay runs each step with the same command the workflow
gives it and reads each count off that bench's own printed summary. One environment note,
recorded because the command is part of the evidence: step 5 (`direction_bench.py --sim`)
aborts on this machine with `FATAL ERROR: Reached heap limit` — the session VM has 955 MB
of RAM and V8's default cap lands near 458 MB. It was run with
`NODE_OPTIONS=--max-old-space-size=1400` and then completed at its full count. This is a
property of the session's environment, not of the repository: nothing in the tree was
changed for it, and a GitHub runner has 16 GB.

---

## Test Results

### The fourteen steps of `bench.yml`, replayed locally

| Step | Bench | Exit | Checks |
|---:|---|---:|---:|
| 1 | `verify_board.js` | 0 | 109 |
| 2 | `board2_bench.js` | 0 | 130 |
| 3 | `prot_bench.js index.html` | 0 | 372 |
| 4 | `verify_bench.py` | 0 | 35 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 0 | 255 708 |
| 6 | `fresh_bench.js` | 0 | 3 424 |
| 7 | `journal_bench.js` | 0 | 693 895 |
| 8 | `catalyst_bench.js` | 0 | 24 692 |
| 9 | `display_bench.py` | 0 | 24 598 |
| 10 | `render_bench.py` | 0 | 16 171 |
| 11 | `direction_bench.py --display` | 0 | 15 629 |
| 12 | `exhaustion_bench.js` | 0 | 220 598 |
| 13 | `live-gate.sh --selftest` | 0 | 40 |
| | **steps 1–13** | | **1 255 401** |
| 14 | `backtest_guard_bench.py` | 0 | **94** |
| | **total, fourteen steps** | | **1 255 495** |

**Delta on steps 1–13: 1 255 401 − 1 255 401 = 0.** No step's count moved, so nothing
needs attributing term by term. That is the expected result and not an accident of
scope: `index.html`, `main.py` and every existing bench are byte-identical to
`origin/main`, and the only pre-existing bench that reads the edited module is
`verify_bench.py`, whose count is item 4's evidence.

**Step 14 measured 94.** The TZ states no expected total and this report predicts none:
the published figure is the measurement (inv. 43).

The same thirteen steps were replayed on the unmodified checkout **before** any edit and
produced the identical 1 255 401 at 0 failures, so the delta above is a comparison of two
measurements rather than of a measurement against a document.

### Negative test — three injected failures (TZ §6.6, contract §9)

Each injection was made in the **working tree**, run with the bare command the gate step
uses (`python3 bench/backtest_guard_bench.py`), then reverted, with the file's MD5 and
`git status` checked before the re-run.

| # | Injection | Command that produced it | Result |
|---:|---|---|---|
| 1 | remove `function clamp01(…)` — a `JS_FUNCS` name — from `index.html` | `python3 bench/backtest_guard_bench.py` | **red, exit 1**, `checks run: 94   FAIL 5`, section A first failure: `ValueError: в HTML не найдена функция clamp01` |
| 2 | invert the admissibility comparison in `_splice`: `r["ok"] = bool(not (r["lo"] <= r["r"] <= r["hi"]))` | `python3 bench/backtest_guard_bench.py` | **red, exit 1**, `checks run: 94   FAIL 9`, all nine in section C (cases 14, 15, 16, 20) |
| 3 | `HARD_CLASSES = ("coverage", "unexplained", "venue-basis")` | `python3 bench/backtest_guard_bench.py` | **red, exit 1**, `checks run: 97   FAIL 1`, section D: `22. and the failing set is PROPER — the reference lane of §3.14 survives` |

After each: revert, `git status` empty, re-run green at `checks run: 94   FAIL 0`,
exit 0. `index.html` returned to `dd39536d18cc1feb4839808e41e7bff4` and
`bench/backtest_bench.py` to `d2dad0f80afa2c191c2faf1d40081a88` after their respective
injections, both verified by MD5.

Injection 3 also turns **step 4** red — `verify_bench.py` reports
`FAIL 2` on its two `fut basis` cases, because `verify_against_live` now reads the same
constant. The widening is therefore caught twice, from two directions, which is the
whole argument for the single definition in §3.1.

A **fourth injection** was run beyond the three the TZ requires, because the three do not
exercise the closure check on a real `index.html` change and that check is the reason
section A exists. A call to an undefined helper was inserted inside `qualityScore` in
`index.html` — the shape of «production splits a helper out» that inv. 62 names:

```
FAIL: _score_bridge.js builds from index.html without raising
  [RuntimeError: замкнутость _score_bridge.js: связка ссылается на splitOutHelper,
   а определения нет ни в ней, ни в драйвере — вырезка отстала от продакшна (инв. 20)]
```

Red, exit 1, reverted, MD5 back to `dd39536d18cc1feb4839808e41e7bff4`, tree clean, green.

### Standing checks on production

| Check | Result |
|---|---|
| `python3 -m py_compile main.py` | exit 0 |
| `node --check` on the single `<script>` block of `index.html` (193 429 bytes) | exit 0 |
| `index.html`, `main.py`, `catalysts.json`, `bench/exhaustion-calibration.txt` | all four identical to the TZ's §0 figures at the end of the session |

### `bench.yml` structure

Parsed with `yaml.safe_load`. The job carries 15 `- name:` entries, of which the first is
`Зависимости` (`pip install numpy requests`, not a bench) and the remaining **14 are the
bench steps**, in the order the TZ gives, with `Гарнизон бэктеста
(backtest_guard_bench.py)` last. This is the same numbering the map uses: its «13 steps»
counts the bench steps and not the dependency install, which is why its step 7 is
`journal_bench.js` and its step 12 is `exhaustion_bench.js`. `push.paths-ignore` reads
`['journal/data/**', 'journal/out/**', 'journal/runs.jsonl', 'analyst/state.json',
'analyst/live.json', 'analyst/log/**', 'analyst/owner.json', '**.md']` — the new entry is
present as an exact literal.

---

## Deviations

**1. Section A's negative control (b) does not use the name the TZ's parenthetical
selects, and the bundle carries one appended line.**

The TZ requires three raises and says of the names: «the first `function NAME(` the
assembled bundle declares, and the first `var NAME` the driver declares». Control (a)
uses the first, exactly as written. Control (b) cannot be built from the second as
written, and the reason is a measurement:

```
_score_bridge.js | seen  45 | resolved ONLY by driver: []
_inv_bridge.js   | seen  23 | resolved ONLY by driver: []
_res_bridge.js   | seen  14 | resolved ONLY by driver: []
_tgt_bridge.js   | seen 116 | resolved ONLY by driver: []
```

`_assert_js_closed` scans the **bundle** and never the driver, so a driver `var` is
load-bearing only if the bundle references that name in a form the scan collects — a
call `NAME(` or an ALL-CAPS token. No real bundle does: the first `var` every driver
declares is `fs`, which no bundle calls. Removing it therefore raises nothing, and a
control that cannot fail is not a control.

What was implemented keeps both of the TZ's constraints that can be kept — the name is
still read off the driver's own text as the first `var` it declares, and the driver is
the real one — and adds the single reference that makes the name load-bearing: the real
bundle plus `var _guard_probe = fs(0);`. Two comparisons follow, and the pair is what
proves the driver half of `known` contributes: **with** the declaration present the check
must pass, and **only then** does removing it from the driver raise, naming `fs`. Both
are asserted.

**2. Section D carries two anchors that do not move with `HARD_CLASSES`.**

As first written, section D was derived from `bb.HARD_CLASSES` throughout, exactly as
§4.4 case 22 requires — and injection 3 then measured green at `checks run: 97   FAIL 0`,
because widening the constant moved the expectation with it. The TZ requires that
injection to turn section D red, so two checks were added that read the two constants
against each other rather than reading one as the expectation for the other:

- every member of `HARD_CLASSES` is a class `CLASSES` can produce;
- `HARD_CLASSES` is a **proper** subset of `CLASSES` — some class is still reference.

The second is what injection 3 trips. It is not a restatement of the membership rule: it
is the fact §3.14 owns, that a reference lane exists at all, and a failing set that had
swallowed every class would put `venue-basis` cells into the failure path and leave
`--verify` red on two clean coins after a successful repair (inv. 58). The membership
rule itself is still asserted against `HARD_CLASSES` and still moves with it, as the TZ
directs.

**3. One check beyond the TZ's list, in section A.** `the negative controls have a real
bundle to work on`. Without it, an `index.html` that has lost a cut function makes
`extract_js` raise where the controls are built, and the bench dies with a traceback
before printing its summary line — a red run that reports no count at all. The check
makes that state a named failure instead. It is what injection 1's third `FAIL` line is.

**4. `NODE_OPTIONS=--max-old-space-size=1400` for step 5 of the local replay.** Described
under validation item 5. It is a property of the session VM's 955 MB of RAM; no file was
changed for it and no workflow carries it.

Nothing else deviates. No file outside `## Scope` was modified, no rule was widened, and
no bench assertion was edited to make anything pass.

---

## Pre-existing Issues

**1. `analyst/owner.json` has no row in the contract's §2 class table.** Confirmed by
reading the table: it carries `analyst/live.json`, `analyst/state.json` and
`analyst/log/**`, and nothing for `analyst/owner.json`. As the TZ directs, no class is
named for it here, nothing was created, and the repair is the Architect's. The map
already records the file's ownership (`analyst/owner.json | Architect → Boss upload | one
copy, replaced`), so the two documents disagree only by omission.

Two further files in the same tree are in the same position and are reported for the same
reason, not acted on: `analyst/live-gate.sh` and `analyst/README.md` have no §2 row
either.

**2. The driver half of `_assert_js_closed`'s `known` set is load-bearing for no current
bundle**, and one name makes that visible. `JS_DRIVER` declares `var cachedFunding` and
the score bundle genuinely reads it — but as a property access, `cachedFunding[sym]`,
which the scan's two patterns (`NAME(` and ALL-CAPS) do not collect. So the real instance
of «a name the bundle reads and the driver declares» is invisible to the check that
exists to catch exactly that. This is not a defect this TZ introduced and not one it
authorises fixing; it is the reason deviation 1 above had to construct its reference
rather than find one. Widening the scan to bare identifier reads is a judgement about
false positives that belongs to the Architect.

**3. No fingerprint difference anywhere.** All six files the TZ's §0 names — the four of
the map's table and the two the TZ adds — measured exactly at the stated line count and
MD5 on `origin/main`. There is nothing to report under this heading for the gate itself.

---

## Remaining Risks

**1. The closure check catches a stale CUT, not a stale RESULT.** After this change the
gate proves that every function `backtest_bench.py` cuts still exists in `index.html` and
that each of the four bundles is closed under reference. It proves nothing about the
arithmetic inside those functions: production may change what `qualityScore` computes,
every bundle will still build and close, and the standing results remain what they were
measured on. The wider half of inv. 62 — a manual workflow decaying from upstream — is
**narrowed here, not retired**, and the map's row should be updated to that claim and no
further.

**2. The `analyst/owner.json` reading is owed, not done.** §5.2 of the TZ is explicit that
the runner reading inv. 53 requires is not a validation item of this TZ, and its absence
is not a PARTIAL. The proof is a real push carrying only that file; the only actor who may
make that push is the Boss; the reading therefore belongs to the audit of his next upload
after the merge. What is established here is only that the literal is present in
`paths-ignore` and that the workflow parses. **Owed.**

**3. Section D's coverage of a NARROWING of `HARD_CLASSES` is indirect.** If a future edit
removed `unexplained` from the constant, section D would move with it and stay green; the
gate catches that at step 4 instead, where `verify_bench.py` case 9 asserts a single
unexplained outlier exits non-zero. That is a real control and it executes on every push,
but it is in a different step from the constant's other reader, and a report that did not
say so would be claiming section D covers both directions.

**4. Step 14 opens no socket, and that is asserted only by construction.** `requests` is
replaced by a stub whose `get` records URLs, and every assertion about a host that must
not be contacted reads that record. If a future edit to `backtest_bench.py` reached the
network through something other than `requests`, this bench would not see it.

---

## Commit

One implementation commit, already made and pushed when this section was written:

```
7fdd7db6d869dcb986a7831c009bc6873545a5c7
TZ-30: backtest garrison in the tree and in the gate (step 14)
```

The subject line is the string the TZ's `## Commit Message` gives, verbatim. Contents:
`bench/backtest_guard_bench.py` (new, 580 lines), `bench/backtest_bench.py` (+28/−4),
`.github/workflows/bench.yml` (+19/−1). Nothing else is in it — no scratch copy, no
bridge file, no `__pycache__`.

This report is committed separately and directly to `main` on the `CryptoReports/**`
path, carrying the message
`docs(reports): TZ-30 — backtest garrison in the tree and in the gate (TZ-30)`.

---

## Pull Request

**No pull request exists.** This session has no `gh` binary and no GitHub token
(`gh: command not found`; no `GH_TOKEN` and no `GITHUB_TOKEN` in the environment), so it
cannot open one. Under contract §8 that is the defined fallback and not a blocker.

- Branch: `claude/tz-30-backtest-guard-in-gate`
- Compare URL: https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-30-backtest-guard-in-gate

The Boss opens and merges from that link in one action, after the Architect's verdict.

---

## CI Execution

**No workflow run was read by this session**, and none is forecast here.

What is established: the branch `claude/tz-30-backtest-guard-in-gate` was pushed to
`origin` at commit `7fdd7db` (`* [new branch]`, reported by `git push`), and the changed
paths clear `bench.yml`'s filters — the workflow triggers on `push` to `main` and
`claude/**`, this branch matches `claude/**`, and none of the three changed paths
(`bench/backtest_guard_bench.py`, `bench/backtest_bench.py`,
`.github/workflows/bench.yml`) appears in `paths-ignore`, whose entries are
`journal/data/**`, `journal/out/**`, `journal/runs.jsonl`, `analyst/state.json`,
`analyst/live.json`, `analyst/log/**`, `analyst/owner.json` and `**.md`.

`main.yml` was read before this session's first direct push to `main` and its trigger
filter is still a `paths` ALLOW-LIST of exactly two literals — `main.py` and
`.github/workflows/main.yml` — so nothing in `CryptoReports/**` can start the bot.

Everything under **Test Results** is a **local replay** of the workflow's steps on the
session's machine, not a runner execution. The hosted gate is read by the audit, from the
pull-request page.

---

## Final Repository State

**NOT IN EFFECT UNTIL MERGED.**

The branch `claude/tz-30-backtest-guard-in-gate` at commit `7fdd7db` carries the whole
implementation and is pushed. Its working tree is clean: `git status --short` is empty
after the last recorded run, with no bridge file, no scratch copy, no `__pycache__` and
no cache directory staged or committed. `main` is untouched by this branch.

Relative to `origin/main` (`60ce04d`) the branch adds one file and modifies two; the four
production files of the map's `## 0` table are byte-identical to that baseline.

---

## Fingerprints

Measured in the session's worktree at commit `7fdd7db`.

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2188 | `6a666ddb100c2cc4a51cb5422fa20f08` |
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/backtest_bench.py` (after this change) | 3240 | `d2dad0f80afa2c191c2faf1d40081a88` |
| `EXECUTOR-INSTRUCTIONS.md` (v19) | 801 | `a6ebc2e7c2f2b74e813dfdc20400558f` |

**Map revision string:** `**Revision 2026-09-05-b.**` — matches the string the TZ's §0
enforces. All seven content anchors were matched as exact substrings of
`SYSTEM-MAP-CRYPTOCALCUL.md` on `origin/main`:

| Anchor | Found |
|---|---|
| `**Revision 2026-09-05-b.**` | yes |
| `### 3.12 Direction engine — veto cascade` | yes |
| `### 3.15 Catalyst registry` | yes |
| `### 3.16 List exhaustion — the day-range measure` | yes |
| `## 11. Analytical engine` | yes |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | yes |
| `64. **A tail top-up must serve the instrument it tops up.**` | yes |

The four files of the map's `## 0` table and the two figures the TZ's §0 adds were each
measured against `origin/main` before any work: **all six matched exactly**, so there is
no fingerprint difference to report and nothing was acted on.

Files this change created or modified, for the audit:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_guard_bench.py` | 580 | `93c2726342e9f8b59579d0ba707a8a52` |
| `.github/workflows/bench.yml` | 153 | `d182e514dcceda5c64410beabc9fe512` |
