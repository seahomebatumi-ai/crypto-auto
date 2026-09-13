# Implementation Report — TZ-41

**Sequencing (TZ-41 header): TZ-40 is merged.** On `origin/main` after `git fetch --all --prune`,
`f122bd7` is `Merge pull request #37 from seahomebatumi-ai/claude/tz-40-return-attribution`, with
parents `d0e4f43` and `805d5e3` (`git cat-file -p f122bd7`). `805d5e3` is the TZ-40
implementation commit the TZ names. `origin/claude/tz-40-return-attribution` was pruned by the
fetch. This TZ was built on `2cf765c` (`Add files via upload`, the commit that added this TZ
file, whose parent is `f122bd7`).

## Status

**COMPLETED.** All four edits are in, and every §5 validation item was run. The offline gate is
green on every step this session can run; step 5 is the exception, and it is covered under
`## Pre-existing Issues`. The dispatch of `backtest_bench.yml` is the Boss's to make and was not
run (contract §9).

## Inbound Filing

None. The TZ arrived as `CryptoTZ/TZ-41-attrib-retained-and-utc-gap.md`, which is exactly the
canonical filename in its header. No other copy exists on `origin/main` or any remote branch
(`git ls-tree -r --name-only <ref> | grep -i tz-41` over every remote ref).

## Scope Executed

**Class: branch TZ.** `## Scope` names three files outside `CryptoReports/**`.

**Fingerprint gate (§0): passed.** Measured against `origin/main` = `2cf765c` after
`git fetch --all --prune`. `git rev-parse --is-shallow-repository` printed `false`. The anchors
were matched with `grep -F`. Each is quoted below as the substring that matched (`grep -F -o -m1`),
and each occurs twice in the map (`grep -F -c` = 2):

| Anchor | Matched substring |
|---|---|
| revision | `**Revision 2026-09-10-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` |

The map's revision string is `Revision 2026-09-10-a`, and the TZ requires `2026-09-10-a`. All four
`## 0` files match their line counts and MD5s. So do the four files in the TZ's touched-file
table. The contract is v20, 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0`, matching the TZ.
Figures are under `## Fingerprints`.

Executed: the four edits of §3, the §4 control, and all seven §5 validation items.

## Files Created

None. This report is committed separately to `main` (§8).

## Files Modified

| File | + | − |
|---|---:|---:|
| `.github/workflows/backtest_bench.yml` | 3 | 1 |
| `bench/backtest_bench.py` | 1 | 2 |
| `bench/backtest_guard_bench.py` | 63 | 0 |

Source: `git diff --numstat`. The TZ names `.github/workflows/backtest_bench.yml` under
`Files to Modify`, which is the authorisation hard floor item 8 requires.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**Edit 1: the `--attrib` step keeps its output.** Its second `run` line went from
`--html ../index.html` to `--html ../index.html 2>&1 | tee attrib.txt`. The step now has the same
two-line shape as the `--verify` step above it:
`python backtest_bench.py --attrib --bot ../main.py \` / `--html ../index.html 2>&1 | tee attrib.txt`.
Its `name`, its `if: ${{ !cancelled() }}` and its comment block are unchanged.

**Edit 2: `bench/attrib.txt` is in the artifact.** The file is on its own line directly after
`bench/verify.txt` in the `upload-artifact` `path:` list, which now has 19 entries.
`if: always()` and every other entry are unchanged.

**Edit 3: `if: ${{ !cancelled() }}` on `Деление по режиму BTC` (`--regimes`), and on no other
step.** No `continue-on-error` was added and no step was removed. Four steps carry an `if` now:
- `--regime-gate`: `${{ inputs.regime_gate }}`, unchanged
- `--attrib`: `${{ !cancelled() }}`, unchanged
- `--regimes`: `${{ !cancelled() }}`, **new**
- `upload-artifact`: `always()`, unchanged

**Edit 4: `_gap_hours` reads the stamp in UTC** (`bench/backtest_bench.py`, line 1709). The pair
```
        g = time.mktime(time.strptime(gen[:19], "%Y-%m-%dT%H:%M:%S"))
        g -= time.timezone
```
became
```
        g = calendar.timegm(time.strptime(gen[:19], "%Y-%m-%dT%H:%M:%S"))
```
- `calendar` was already imported at line 28.
- `calendar.timegm` is already used at line 1207.
- The `except` path, the `if g and ends` guard, the return expression, the docstring and both
  callers (lines 1797 and 2147 after the edit) are unchanged.
- `time.timezone` no longer appears anywhere in the file (`grep -c 'time\.timezone'` = 0).

**The control is section J of `bench/backtest_guard_bench.py`, in gate step 14, with 8
comparisons.**

**Why the letter is J.** It is read off the file, not counted. The file's section headers are
A, B, C, D, E (line 652), E (line 894), F, G, H and I (line 1972). The last letter in use is I,
so the new section is J. Counting sections would say K, because two sections share E. The
section's header comment records this.

**What the control constructs.** Every value is built from integers, so every equality is exact
and there is no tolerance:
- `J_T = 1784116800000` is the instant `2026-07-15T12:00:00Z`.
- The stamp `J_GEN` is formatted from `J_T` with `gmtime`, the same construction section I's
  `i_live` uses.
- The ends are 30, 5 and 9 hours before `J_T`. The newest is 5 hours before, so the known answer
  is 5.0.

**The zone.** The DST zone is the POSIX rule string `EST+05EDT,M3.2.0,M11.1.0`, not a tzdata
name. libc parses a rule string without zone files, so a runner without tzdata cannot quietly
fall back to UTC and make the two readings trivially equal.

**The 8 comparisons:**

| Check | Comparison |
|---|---|
| J1 | the zone is in daylight time at `J_T` (`tm_isdst == 1`). A probe run outside DST proves nothing, so this is the precondition |
| J2 | under the DST zone, `_gap_hours == 5.0` |
| J2 | under `UTC`, `_gap_hours == 5.0` |
| J3 | the two readings are equal |
| J4 | `(os.environ.get('TZ'), time.tzname, time.timezone, time.altzone)` equals the tuple saved before the probe |
| J5 | an unparseable `generated_at` returns `None` |
| J5 | an empty `ends` returns `None` |
| J | the section's own non-zero count guard, the pattern sections H and I use |

The restoration runs in a `finally` block, so a failing probe cannot leak a zone into the rest of
the process.

## Validation

All figures below are local, from this session's container (`TZ` unset, `/etc/localtime` →
`Etc/UTC`).

**Baselines, taken before any edit:**
- `python3 bench/backtest_guard_bench.py`: exit 0, `checks run: 467   FAIL 0`
- `python3 bench/verify_bench.py`: exit 0, `checks run: 40   FAIL 0`

**1. `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py`:** exit 0.

**2. `python3 bench/backtest_guard_bench.py`:** exit 0, `checks run: 475   FAIL 0`.
- The new section is **J**, 8 comparisons (`J. gap in UTC: 8 comparisons`).
- Sections E, F, G, H and I read 32, 29, 63, 107 and 94, identical before and after.
- Step 14 went from **467** to **475**. The delta of +8 is exactly J's count.

The gate total, term by term. `bench.yml` has 14 steps. I measured every step this container can
run, serially and one bench at a time. Steps 1–3 and 5–13 ran from the repository root, with the
commands copied from `bench.yml`.

| Step | Bench | Measured | Before | After |
|---:|---|---|---:|---:|
| 1 | `verify_board.js` | `--- checks: 109  fails: 0 ---`, exit 0 | 109 | 109 |
| 2 | `board2_bench.js` | `--- checks: 130  fails: 0 ---`, exit 0 | 130 | 130 |
| 3 | `prot_bench.js index.html` | `PASS 372   FAIL 0`, exit 0 | 372 | 372 |
| 4 | `verify_bench.py` | `checks run: 40   FAIL 0`, exit 0 | 40 | 40 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | **not measurable here**: V8 heap OOM, exit 1 (`## Pre-existing Issues`) | 255 708 | 255 708 |
| 6 | `fresh_bench.js` | `--- checks: 3424  fails: 0 ---`, exit 0 | 3 424 | 3 424 |
| 7 | `journal_bench.js` | `--- проверок: 774130  провалов: 0 ---`, exit 0 | 774 130 | 774 130 |
| 8 | `catalyst_bench.js` | `--- checks: 24692  fails: 0 ---`, exit 0 | 24 692 | 24 692 |
| 9 | `display_bench.py` | `display_bench: 24598 checks, 0 failures`, exit 0 | 24 598 | 24 598 |
| 10 | `render_bench.py` | `render_bench: 123 scenarios, 16171 checks, 0 failures`, exit 0 | 16 171 | 16 171 |
| 11 | `direction_bench.py --display` | `ИТОГО проверок: 15629 | провалов блоков: 0`, exit 0 | 15 629 | 15 629 |
| 12 | `exhaustion_bench.js` | `--- checks: 220598  fails: 0 ---`, exit 0 | 220 598 | 220 598 |
| 13 | `live-gate.sh --selftest` | `checks=40`, `selftest: 14 cases, all exit codes as specified`, exit 0 | 40 | 40 |
| 14 | `backtest_guard_bench.py` | `checks run: 475   FAIL 0`, exit 0 | 467 | **475** |
| | **total** | | **1 336 108** | **1 336 116** |

How to read the table:
- **Step 5 is carried, not measured.** Its figure of 255 708 comes from TZ-13, TZ-27 and TZ-30,
  which all record that number.
- **The 11 other steps outside 4 and 14 were measured once.** Each one's inputs are identical
  before and after this change, and none of them reads any of the three changed files: among the
  gate's steps, only `verify_bench.py` and `backtest_guard_bench.py` mention `backtest_bench`
  (`grep -ln backtest_bench bench/* .github/workflows/* analyst/*`). They sum to **1 079 893**.
  With step 5 that makes 1 335 601, the figure the TZ-40 report used for "the 12 steps other
  than 4 and 14".
- **The before total reproduces the TZ's figure exactly:** 1 335 601 + 40 + 467 = **1 336 108**.
- **After:** 1 335 601 + 40 + 475 = **1 336 116**, a delta of **+8**, which is section J.

**3. `python3 bench/verify_bench.py`:** exit 0, `checks run: 40   FAIL 0`, both before and after.

**4. The two-zone probe, before and after the repair.** The script is `/tmp/tz41_probe.py`
(session scratch, not committed). It loads the file under test, then calls `_gap_hours` on
`generated_at = 2026-07-15T12:00:00` with the newest end at `1784098800000` (5 h earlier). It
does this once under `TZ=EST+05EDT,M3.2.0,M11.1.0` and once under `TZ=UTC`, with `time.tzset()`
before each. The constructed answer is 5.0.

| File | Zone | `_gap_hours` | `tm_isdst` | `time.timezone` | `time.altzone` |
|---|---|---:|---:|---:|---:|
| before (`bcdccf86…`, 5009 lines) | `EST+05EDT,M3.2.0,M11.1.0` | **4.0** | 1 | 18000 | 14400 |
| before | `UTC` | **5.0** | 0 | 0 | 0 |
| after (`c7fedd64…`, 5008 lines) | `EST+05EDT,M3.2.0,M11.1.0` | **5.0** | 1 | 18000 | 14400 |
| after | `UTC` | **5.0** | 0 | 0 | 0 |

**Before the repair, the two zones did NOT read the same gap.**
- In daylight time, `mktime` applied the EDT offset of 14400 s.
- The correction then subtracted `time.timezone`, the standard offset of 18000 s.
- The result was 3600 s too early, so the gap read one hour short.

Under UTC, the old construction was exact. That is why this defect is invisible on a runner
whose zone is UTC. The UTC reading is correct on both files; only the DST reading changed.

**Negative control for step 14** (contract §9).
- I put the two original lines back into the working tree. `git diff --quiet
  bench/backtest_bench.py` confirmed the file was byte-identical to HEAD
  (`bcdccf8614f1cecbe4d0c0b78129ddf5`).
- `python3 bench/backtest_guard_bench.py` then **exited 1** with `checks run: 475   FAIL 2`:
  - `FAIL: J2. EST+05EDT,M3.2.0,M11.1.0: the gap is the constructed 5.0 hours  [4.0]`
  - `FAIL: J3. the two zones read the same gap  [(4.0, 5.0)]`
- J1, the UTC J2, J4 and J5 still passed, as expected: the UTC reading and the `None` paths never
  depended on the zone.
- I then restored the repaired file (`c7fedd64bce7c27c07803325b1f807d3`), and the bench exited 0
  with `checks run: 475   FAIL 0`.
- `git diff --numstat` was the same before and after the control.

**5. The exit code survives the pipe.**
- Setup: the `--attrib` step's `run` block was extracted from the parsed YAML and written to a
  file verbatim:
  ```
  cd bench
  python backtest_bench.py --attrib --bot ../main.py \
    --html ../index.html 2>&1 | tee attrib.txt
  ```
- It ran in a scratch directory whose `bench/backtest_bench.py` is a stub that prints its argv and
  exits 3.
- This container has no `python` on `PATH` (`command -v python` → absent), so a `python → python3`
  symlink was put first on `PATH` for the test.

| Shell | Stub | Shell exit code | `attrib.txt` |
|---|---|---:|---|
| `bash -euo pipefail` (the job's shell) | exits 3 | **3** | holds the stub's output line |
| `bash -eu` (no `pipefail`, for contrast) | exits 3 | **0** | holds the stub's output line |
| `bash -euo pipefail` | exits 0 | **0** | `stub ok` |

Under the job's shell, the failure reaches the step. Without `pipefail`, `tee` swallows it.

**6. YAML** (`yaml.safe_load`):
- The file parses: 19 steps, job shell `bash -euo pipefail {0}`.
- The `--attrib` step's `run` contains `tee attrib.txt`, and its `if` is `${{ !cancelled() }}`.
- `bench/attrib.txt` is in the artifact `path:` list, directly after `bench/verify.txt`, and the
  upload step's `if` is `always()`.
- The `--regimes` step's `if` is `${{ !cancelled() }}`.
- `continue-on-error`: on no step, not at job level, and `grep -c continue-on-error` on the file
  prints `0`.

`git diff -U0 .github/workflows/backtest_bench.yml` shows **three hunks: 3 lines added, 1
removed**:
```
@@ -137 +137 @@ jobs:
-            --html ../index.html
+            --html ../index.html 2>&1 | tee attrib.txt
@@ -140,0 +141 @@ jobs:
+        if: ${{ !cancelled() }}
@@ -154,0 +156 @@ jobs:
+            bench/attrib.txt
```
With git's default three lines of context, the first two edits are three lines apart, so plain
`git diff` merges them into **two** hunks. The content is the same three edits either way.

**7. `git diff --name-only`** names exactly three files:
- `.github/workflows/backtest_bench.yml`
- `bench/backtest_bench.py`
- `bench/backtest_guard_bench.py`

The four `## 0` hashes after the change, all unchanged:
- `index.html` 3799 `4e71da9badca3ccae85b656fdc3773e8`
- `main.py` 518 `0e3ead8c300d2ee6783303c4bf2fb6b5`
- `catalysts.json` 17 `f9b2dd4a3594134b2b7b603de19075c3`
- `bench/exhaustion-calibration.txt` 175 `3b8730b254467c9df4c0a845a0f3cfb3`

No production file is touched.

## Test Results

| Item | Result |
|---|---|
| 1 py_compile | exit 0 |
| 2 guard bench | exit 0, 475 checks, FAIL 0; section J = 8; step 14: 467 → 475; gate: 1 336 108 → 1 336 116 |
| 3 verify bench | exit 0, 40 checks, FAIL 0 |
| 4 two-zone probe | before 4.0 (DST) / 5.0 (UTC); after 5.0 / 5.0 |
| 5 pipefail | shell exit 3 on a stub exiting 3 |
| 6 YAML | parses; the three edits present; no `continue-on-error`; `-U0` shows 3 hunks, +3 −1 |
| 7 diff scope | three files; the `## 0` hashes are unchanged |
| negative control | reverted: exit 1, FAIL 2 (J2 DST, J3); restored: exit 0 |

## Deviations

None in what was built. Two presentation facts are recorded here because a reader could take
them for deviations:
- **The hunk count.** §5 item 6 expects "three hunks". `git diff -U0` shows three; the default
  `git diff` shows two, for the reason given under item 6.
- **Section J's count.** J carries 8 comparisons, one more than §4's list enumerates. The extra
  comparisons are J1 (the DST precondition) and the section's own non-zero count guard. Both
  follow from rules already in force: a probe that never entered daylight time would pass without
  testing anything (inv. 22), and sections H and I carry the same count guard. Each is one
  comparison, counted where it compares (inv. 43).

## Pre-existing Issues

1. **Gate step 5 (`direction_bench.py --props --fixtures --control --sim`) cannot finish in this
   container.** It prints `[OK ] СВОЙСТВА`, `[OK ] РЕЖИМ` and `[OK ] ФИКСТУРЫ`, then dies with
   `FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory` and exits 1.
   - The cause is the container's RAM, not the repository. The same step is green on a runner in
     this TZ's own CI runs (`## CI Execution`).
   - Its inputs are untouched by this change: the diff names three files, and the step reads none
     of them.
   - Its figure in the gate total is carried from the earlier reports, as stated under item 2.
2. **A misplaced workflow comment.** In `.github/workflows/backtest_bench.yml`, the comment
   `# Артефакт нужен именно тогда, когда что-то упало.` sits directly above the
   `Деление по режиму BTC` step. It describes the `upload-artifact` step's `if: always()` two
   steps below it, and reads as if it belonged to `--regimes`. It was left untouched: §2 permits
   only the three edits. Reported for a later TZ.
3. **`_gap_hours` treats a `g` of 0 as unparsed.** The guard `if g and ends` is falsy for a stamp
   of exactly `1970-01-01T00:00:00`, so that stamp returns `None`. No real `generated_at` can
   carry it, and §3 item 4 keeps the guard unchanged. Recorded only as a property of the guard.
4. **`bench/backtest_bench.py`'s argparse defaults name two files that do not exist**
   (`DEF_HTML`, `DEF_BOT`). This was already known and did not affect this TZ: every mode here ran
   with explicit paths or through the benches.

## Remaining Risks

- **This change has no dispatch reading yet.** `backtest_bench.yml` is `workflow_dispatch` only,
  so the three workflow edits have never run on a runner. Two things stand behind them:
  - the structural checks of item 6;
  - the item 5 replay of the `--attrib` run block under the job's shell, which ran in this
    container against a stub, not on a runner.

  Whether the next dispatch's artifact carries `attrib.txt` and `regimes.txt` is not established
  here, and nothing in this report forecasts it (inv. 54).
- **The skip defect is not repaired, by §6.** TZ-40 measured that `over` is computed with no
  reference to `skip`, and that the skip is one-sided at `gap > 3`. `--verify`'s verdict is
  unchanged.
- **`_gap_hours` gave the same numbers before and after on any UTC machine.** Any `--verify`
  reading already produced on a runner is therefore unaffected by the repair: the probe shows the
  UTC reading is identical before and after.

## Commit

Implementation commit on `claude/tz-41-attrib-retained-and-utc-gap`, already pushed when this
section was written: **`dc42e4e884d4e45bf014225cac26ee3848b47ca0`**.
```
TZ-41: retain the attribution output as an artifact, keep the post-verify steps running, read the gap in UTC

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```
It contains `.github/workflows/backtest_bench.yml` (+3 −1), `bench/backtest_bench.py` (+1 −2)
and `bench/backtest_guard_bench.py` (+63 −0).

This report is committed to `main` with the message
`docs(reports): TZ-41 — attribution retained, post-verify steps kept, gap read in UTC (TZ-41)`.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/38. The base is `main`; the head is
`claude/tz-41-attrib-retained-and-utc-gap`.

## CI Execution

**`Bench gate` ran twice on a runner, both on `dc42e4e884d4e45bf014225cac26ee3848b47ca0`,
and both concluded `success`.** Read with `gh run view <id> --json jobs`:

| Run | Event | Conclusion |
|---|---|---|
| [34749013673](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/34749013673) | `push` to `claude/tz-41-attrib-retained-and-utc-gap` | `success` |
| [34749017673](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/34749017673) | `pull_request` #38 | `success` |

In both runs every one of the job's 19 steps is `success`, including all 14 bench steps
(workflow steps 6–19):
- workflow step 9, `verify_bench.py`, which is bench step 4;
- workflow step 10, `direction_bench.py --props --fixtures --control --sim`, which is bench
  step 5 and cannot finish in this container;
- workflow step 19, `backtest_guard_bench.py`, which is bench step 14 and carries section J.

No step was `skipped`.

**Check counts on the runner are not read.** They exist only in the step logs, and I did not
read the logs. Every count in this report is local.

**`backtest_bench.yml` did not run.** It is `workflow_dispatch` only, and no dispatch was made in
this session (§6: no fetch; the dispatch is the Boss's). The three edits to that file have no
runner reading.

## Final Repository State

- Branch `claude/tz-41-attrib-retained-and-utc-gap`, pushed at `dc42e4e`, one commit ahead of
  `2cf765c`, tracking `origin/claude/tz-41-attrib-retained-and-utc-gap`.
- When this report was written, the only entry in `git status --porcelain --ignored` was this
  report, untracked. The scratch `bench/_*` files and `bench/__pycache__` had been removed. The
  report is not part of the branch.
- PR #38 is open.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Map revision string: **`Revision 2026-09-10-a`** (`**Revision 2026-09-10-a.**`).

| File | Lines | MD5 | vs. required |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2590 | `86dac370fb4e3e096cb24e23dec1aa1c` | reported, not enforced |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |
| `EXECUTOR-INSTRUCTIONS.md` | 814 | `9a257890e9db663eb0fc74129f4841e0` | match (v20) |

The TZ's touched-file table, before (at `2cf765c`, matching every TZ figure) and after
(branch `dc42e4e`):

| File | Lines before | MD5 before | Lines after | MD5 after |
|---|---:|---|---:|---|
| `bench/backtest_bench.py` | 5009 | `bcdccf8614f1cecbe4d0c0b78129ddf5` | 5008 | `c7fedd64bce7c27c07803325b1f807d3` |
| `bench/backtest_guard_bench.py` | 2375 | `3937226bc0a15b0cf6917ad7393cd827` | 2438 | `85ea609882ac3761fd526b3ebff2fe5f` |
| `.github/workflows/backtest_bench.yml` | 169 | `a62abbb50a4775999011d802aea5916b` | 171 | `703330829c377a15fc0df71e25df92a7` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
