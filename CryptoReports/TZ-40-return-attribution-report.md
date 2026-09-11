# Implementation Report — TZ-40

**The previous TZ's branch is NOT merged.** `claude/tz-39-transport-outcome-and-budget`
(`396f961`) is not an ancestor of `origin/main`, and pull request #35 reads `state: open`,
`merged: false`. TZ-40 makes that merge its precondition (TZ lines 8–10), so this run
stopped there.

## Status

**BLOCKED.**

The System Map fingerprint gate PASSED in full. Work stopped at contract §4a step 6, on the
sequencing requirement TZ-40 states in its own header:

> **Sequencing: TZ-39 is merged before this TZ starts.** Both TZs edit the same two benches,
> so a branch cut before that merge produces work that is complete and live nowhere
> (contract §8). Check it and say so at the top of your report.

TZ-39 is not merged. No file in the TZ's scope was modified, no branch was opened, and no
pull request exists.

**What unblocks it:** PR #35 is merged, after the Architect's audit of TZ-39, and
`EXECUTE TZ-40` is sent again. The TZ itself needs no change. The re-run writes
`CryptoReports/TZ-40-return-attribution-report-2.md` (contract §10, §13).

## Inbound Filing

None. `CryptoTZ/TZ-40-return-attribution.md` arrived on `origin/main` in `8c3392f`, already
under the canonical filename its header states. Nothing was moved or renamed.

A second upload of the same file is `5d0f069` on `seahomebatumi-ai-patch-1`, which
reached `main` as PR #36 (`b48a75c`, merged 2026-09-11T23:34:36Z). The two uploads are
byte-identical (`git diff --quiet 5d0f069 8c3392f -- CryptoTZ/TZ-40-return-attribution.md`
→ exit 0). `git diff --stat ceed367 b48a75c` is empty, so that merge changed no content, and
the TZ was not replaced in place.

At session start the worktree stood at `ceed367`. `git fetch` showed `origin/main` at
`b48a75c`, and the tree was brought there by `git merge --ff-only origin/main`. The
repository is not shallow (`git rev-parse --is-shallow-repository` → `false`).

## Scope Executed

**Class: branch TZ** (contract §8). `## 2. Scope` names three files outside
`CryptoReports/**`: `bench/backtest_bench.py`, `bench/backtest_guard_bench.py` and
`.github/workflows/backtest_bench.yml`.

Executed: contract §4a steps 1–6 (contract read, fetch, TZ located and read, fingerprint
gate, repository state). Step 6 found the blocker, so step 7 was not entered. Steps 8 and 9
were not reached. Step 10 is this report.

## Files Created

- `CryptoReports/TZ-40-return-attribution-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

No implementation was performed. What follows is the blocker and its evidence.

### The gate passed

The revision string, all seven content anchors and all four `## 0` file fingerprints matched
exactly. The readings are under `## Test Results` and `## Fingerprints`.

### The blocker — TZ-39 is not on `main`

Four independent readings, all taken after `git fetch` on `b48a75c`:

| Reading | Command | Result |
|---|---|---|
| ancestry | `git merge-base --is-ancestor origin/claude/tz-39-transport-outcome-and-budget origin/main` | exit 1: **not an ancestor** |
| branch list | `git branch -a --no-merged origin/main` | lists `claude/tz-39-transport-outcome-and-budget` and `remotes/origin/claude/tz-39-transport-outcome-and-budget` |
| pull request | `curl -s https://api.github.com/repos/seahomebatumi-ai/crypto-auto/pulls/35` | `state: open`, `merged: False`, `merged_at: None`, head `396f961f413599d3c9f10d9252119af2e74a2f74` |
| file content | `md5sum` of the two benches on `b48a75c` | the **pre-TZ-39** figures, exactly (table below) |

The last row is the TZ's own control. TZ-40 §0 states the two bench figures as the map's
"taken BEFORE TZ-39" and adds that "TZ-39 moves both files, so they will differ when you
measure them". **They did not differ.** Both files on `main` are byte-for-byte the files
TZ-39 started from:

| File | TZ-40 §0, pre-TZ-39 | Measured on `main` (`b48a75c`) | TZ-39 branch (`396f961`) |
|---|---|---|---|
| `bench/backtest_bench.py` | 4555, `deac9dd8a53f2047c25c2d6fb24f09b4` | 4555, `deac9dd8a53f2047c25c2d6fb24f09b4` | 4572, `ce38ef842b60699b9ea34dad4f322a29` |
| `bench/backtest_guard_bench.py` | 1726, `ce08dd99edebfa90d8fce3dd6b7ba472` | 1726, `ce08dd99edebfa90d8fce3dd6b7ba472` | 1986, `1580b9a02b7d4453cd3eebd0b25e33ad` |

`git diff --stat origin/main 396f961 -- bench/` → `2 files changed, 305 insertions(+), 28
deletions(-)`: the TZ-39 change that is not yet on `main`.

### Why this stops the run instead of being reported and worked around

Contract §8 alone would only require the unmerged base to be named at the top of the report.
TZ-40 goes further: it makes the merge a precondition, and it states the consequence it
exists to prevent. The two ways to proceed produce different work, and the TZ authorises
neither:

- **Reading A — branch from `main` as it stands.** This is exactly "a branch cut before that
  merge", which the TZ names as the failure. Both TZs rewrite `bench/backtest_bench.py` and
  `bench/backtest_guard_bench.py`. TZ-39 adds 50 assertions to section H of the guard and
  edits `_http`, `fetch_prices` and `fetch_funding`. A TZ-40 branch cut from `main` would
  measure its §8 item 2 baseline (step 14 = 323) on a guard that TZ-39 has already replaced
  (373), and it would conflict with PR #35 in both files.
- **Reading B — stack on TZ-39's branch, the way TZ-35 continued TZ-34's.** TZ-35's own
  text made that its premise. TZ-40's text says the opposite: TZ-39 is to be merged first,
  not carried. Stacking would put TZ-39's commit inside TZ-40's pull request before the
  Architect has ruled on it. It would also leave TZ §8 item 8 ("`git diff --name-only` names
  exactly three files") with two bases that measure different diffs.

Under contract §12 a requirement with two readings that produce different code is not
resolved by choosing. Contract §14 adds: "When in doubt: stop and report." Stopping now also
costs no work. Nothing in the TZ's scope was written, and the re-run can start from a merged
base.

### Not assessed

The spec was not checked against the code. §3–§5 of the TZ were read in full, but no
feasibility reading was taken: the call sites they name (the AST cut from `get_token_betas`,
`--verify`'s acquisition path, its comparison site and the gap derivation) sit in a file
that PR #35 is about to change. A reading taken now would describe a base the TZ does not
execute against.

## Validation

The TZ's validation was **not entered**. The blocker comes before any code exists to
validate. Per contract §9 no item is marked "not applicable". Each is recorded as NOT RUN
with its reason, and **none is recorded as passed**.

| # | Item | Result |
|---|---|---|
| 1 | `py_compile` both benches | NOT RUN — neither file was changed |
| 2 | Guard green, new section letter, step 14 before/after, gate total | NOT RUN — no section was written. The baseline the TZ requires is the post-TZ-39 guard, which is not on `main` |
| 3 | `verify_bench.py` 40 checks | NOT RUN — `backtest_bench.py` was not changed |
| 4 | Identity control (W1) | NOT RUN — no instrument exists |
| 5 | Zero-cell refusal (W5) | NOT RUN — no instrument exists |
| 6 | `--attrib` end to end offline | NOT RUN — the mode does not exist |
| 7 | YAML step | NOT RUN — `backtest_bench.yml` was not modified |
| 8 | `git diff --name-only` names three files, four `## 0` hashes after | NOT RUN as specified — there is no diff. The four hashes are recorded below and are unchanged, because nothing was written |
| 9 | Extremes | NOT RUN — no mode exists to drive them through |

## Test Results

**Fingerprint gate (contract §5) — PASSED.**

The revision string matched as an exact substring:

```
$ grep -n '^\*\*Revision' SYSTEM-MAP-CRYPTOCALCUL.md
17:**Revision 2026-09-10-a.** Baseline: TZ-38 on the bench's transport — one helper at one
```

All seven content anchors were matched with `grep -cF`. Each occurs twice: once in the map's
own anchor table and once at its site.

| Anchor | Matched substring | Count |
|---|---|---:|
| revision | `**Revision 2026-09-10-a.**` | 2 |
| direction engine | `### 3.12 Direction engine — veto cascade` | 2 |
| catalyst registry | `### 3.15 Catalyst registry` | 2 |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | 2 |
| analytical engine | `## 11. Analytical engine` | 2 |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` | 2 |

7 anchors compared, 7 present, 0 missing.

**Map `## 0` file table: 4 files compared, 4 exact, 0 differences.**

| File | Required | Measured | Result |
|---|---|---|---|
| `index.html` | 3799, `4e71da9badca3ccae85b656fdc3773e8` | 3799, `4e71da9badca3ccae85b656fdc3773e8` | exact |
| `main.py` | 518, `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518, `0e3ead8c300d2ee6783303c4bf2fb6b5` | exact |
| `catalysts.json` | 17, `f9b2dd4a3594134b2b7b603de19075c3` | 17, `f9b2dd4a3594134b2b7b603de19075c3` | exact |
| `bench/exhaustion-calibration.txt` | 175, `3b8730b254467c9df4c0a845a0f3cfb3` | 175, `3b8730b254467c9df4c0a845a0f3cfb3` | exact |

Contract: `EXECUTOR-INSTRUCTIONS.md` 814 lines, `9a257890e9db663eb0fc74129f4841e0`. This
matches the v20 figures TZ §0 states.

**Repository state (contract §4a step 6):** see the blocker table above.
`git status --porcelain` is empty on `b48a75c`. `CryptoReports/` held no TZ-40 report before
this one, so no `-2` suffix applies to this file.

## Deviations

None. Nothing within the TZ's scope was written, so there was nothing to deviate from. Work
stopped under the TZ's own sequencing clause and contract §12, not on a chosen reading.

## Pre-existing Issues

None new. Every fingerprint the gate compares matched exactly. The two bench files matching
their pre-TZ-39 figures is not a pre-existing defect: it is the blocker's evidence, and it
is the state the TZ says should already have moved on.

## Remaining Risks

- **The precondition depends on an audit outcome.** If the Architect rejects TZ-39 rather
  than accepting it, PR #35 is never merged and TZ-40's sequencing clause cannot be met as
  written. Re-sequencing is then the Architect's decision. It is not an Executor's reading
  of the clause.
- **§10's open row stays open.** Map §10 conditions every gated figure cited on more than
  twelve coins on this attribution. Until it lands, `--target`'s universe is twelve, as the
  map already states. This report changes nothing about that.

## Commit

One commit, on `main`, on the `CryptoReports/**` direct-push path (contract §8). Before the
push, both workflow filters were read and confirmed. `bench.yml`'s `push` trigger carries
`'**.md'` under `paths-ignore`. `main.yml`'s `push` trigger is a `paths` allow-list of
exactly `main.py` and `.github/workflows/main.yml`.

Message:

```
docs(reports): TZ-40 — BLOCKED, TZ-39 is not merged and TZ-40 requires it first (TZ-40)
```

Contents: `CryptoReports/TZ-40-return-attribution-report.md`, added.

No hash appears here. This report's own commit has not been made at the time of writing, and
a hash or an outcome for it would be a forecast inside an immutable record (inv. 54,
contract §10).

## Pull Request

None. This is a branch TZ by class, but the run was BLOCKED before any file in its scope was
written, so no implementation commit, no branch and no pull request exists. The section is
recorded rather than omitted, because an absent section cannot be told from a forgotten one
(contract §10). The fixed report-only line is deliberately not used: it would assert a class
this TZ does not have.

## CI Execution

No workflow executed on a runner for this task. Nothing was pushed to a branch, so nothing
could trigger one. `bench.yml` and `backtest_bench.yml` did not run for this task, and
neither was modified. No forecast is offered for any of them (inv. 54).

## Final Repository State

This session leaves the working tree clean at `b48a75cb4edb925c6d0d04b7d4b1492a16ef6e1d`
(`origin/main` after the fetch), with no modification to any file in the TZ's scope. No
branch was created and none was pushed. The fingerprints below were taken against that
commit.

Nothing awaits a merge from this TZ, so "NOT IN EFFECT UNTIL MERGED" has no referent and is
not written.

## Fingerprints

Taken at `b48a75c`, when this report was written.

**System Map revision string:** `**Revision 2026-09-10-a.**`

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2590 | `86dac370fb4e3e096cb24e23dec1aa1c` |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` |
| `ANALYST-INSTRUCTIONS.md` | 2615 | `e945ac9e93c03e72f551bc7972541148` |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/backtest_bench.py` | 4555 | `deac9dd8a53f2047c25c2d6fb24f09b4` |
| `bench/backtest_guard_bench.py` | 1726 | `ce08dd99edebfa90d8fce3dd6b7ba472` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
| `.github/workflows/backtest_bench.yml` | 156 | `60ac7db0c4f1960f57d67da8e9beebfe` |
| `CryptoTZ/TZ-40-return-attribution.md` | 296 | `5292d8927275827beb1695613a301b33` |

The map plus `index.html`, `main.py`, `catalysts.json` and
`bench/exhaustion-calibration.txt` are the set the map's `## 0` block requires. The two
contracts are recorded for the audit's comparison. The two benches are added because TZ-40's
gate table names them. The last three rows are added because the TZ's scope or `## Touches`
names them.
