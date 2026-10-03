# Implementation Report — TZ-59

## Status

**COMPLETED.**

The run will use this command line, from `run.CLAUDE[3:]` (V3): `['--output-format', 'json', '--model', 'claude-opus-5-5', '--effort', 'high', '--allowedTools', 'Bash Read Write Edit Glob Grep WebSearch WebFetch', '--append-system-prompt', 'Read EXECUTOR-INSTRUCTIONS.md at the repository root in full before anything else: it is your contract, and the user message is a trigger from its §4.']`.

The deployer installs it when the branch is merged, so the first run after the merge is the first run at `high`.

The previous TZ's branch, `tz-58-vps-fit-model-stream-list` at `a172529`, is merged: `git merge-base --is-ancestor a17252950267c2d0261ee96238784415ddae5453 origin/main` exited 0. TZ-58 was merged at `2416e3f`.

## Inbound Filing

None. The TZ was already at its canonical path, `CryptoTZ/TZ-59-run-model-pin.md`, on `main` at `02be078` ("Add files via upload").

## Scope Executed

Class: **branch TZ**, because the scope names `vps/run.py` and `vps/selftest.py`, which are outside `CryptoReports/**`.

- Stage A, A1: the contract §4a steps 1–6 and the §5 gate checked against the TZ's §0, including the added-files table. The merge-ancestry check passed.
- Stage B, B1: `vps/run.py` changed as dictated in §11.1.
- Stage B, B2: `vps/selftest.py` section O gained the three checks dictated in §11.2.
- Validation: V1–V5 all ran.

No stage read or changed the VPS. No model session was opened, and the `claude` binary was not run.

## Files Created

None. This report is the only new file, and it is on `main`.

## Files Modified

- `vps/run.py`: 331 → 333 lines, MD5 `4be5ada20662f7876715b15b5250722d` → `10165bc8d4d79e92db30147a76eec48f`.
- `vps/selftest.py`: 811 → 817 lines, MD5 `dbea50aeec9b30034be9e57f8150a5c2` → `c728b6fd74d1aaad269a1fb2a6de886e`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

- **`vps/run.py`:**
  - Two constants are added immediately above `CLAUDE`: `MODEL  = "claude-opus-5-5"` and `EFFORT = "high"`.
  - `CLAUDE` now passes `"--model", MODEL, "--effort", EFFORT`. Before, it passed `"--model", "opus"`.
  - The module docstring's first line now names `TZ-59 B1`.
  - No other line moved.
- **`vps/selftest.py`:** three checks are added at the head of `section_o`. Each one counts as a comparison:
  1. `--model` is immediately followed by `claude-opus-5-5`.
  2. `--effort` is immediately followed by `high`.
  3. No element of `run.CLAUDE` equals `opus`.

The diff is 10 insertions and 2 deletions across the two files.

## Validation

**V1, selftest.** `python3 vps/selftest.py` exited 0 with the output `selftest: sections 18 checks 214 failed 0 empty 0`. Section O printed `checks 27 failed 0`.

The baseline on unmodified `origin/main` was 18 sections, 211 checks and 0 failed, with section O at 24. That is +3 checks, all in section O.

**V1, negative control (inv. 68).**

1. In the working tree, `EFFORT = "high"` was changed to `EFFORT = "medium"`.
2. The selftest exited 1 with:
   ```
   FAIL section O: run.CLAUDE carries --effort immediately followed by high
   section O: checks 27 failed 1
   selftest: sections 18 checks 214 failed 1 empty 0
   ```
   Section O was the only section that failed.
3. The line was reverted. The MD5 was restored to `10165bc8d4d79e92db30147a76eec48f`.
4. The selftest exited 0 again: `selftest: sections 18 checks 214 failed 0 empty 0`.

**V2, syntax.** `python3 -m py_compile vps/run.py vps/selftest.py` exited 0.

**V3, command line.** The list printed under `## Status` contains `--model` and `claude-opus-5-5`, then `--effort` and `high`. No element equals `opus`.

**V4, no production file.** `git diff --name-only origin/main...HEAD` on the branch returned `vps/run.py` and `vps/selftest.py`, exactly.

**V5, pushes.** The branch was pushed and pull request #48 was opened. Nothing reaches `main` from this session except this report.

The standing checks on `main.py` and `index.html` (map §6 item 1) do not apply, because no production file changed. Their fingerprints are unchanged; see `## Fingerprints`.

## Test Results

| Run | Exit | Total |
|---|---:|---|
| Baseline, unmodified `origin/main` | 0 | 18 sections, 211 checks, 0 failed |
| After the change | 0 | 18 sections, 214 checks, 0 failed, 0 empty |
| Negative control (`EFFORT = "medium"`) | 1 | 214 checks, 1 failed (section O) |
| Reverted | 0 | 214 checks, 0 failed |

## Deviations

- **The negative control's first revert was done wrong.** The session restored `vps/run.py` with `git checkout -- vps/run.py`. That command discarded the uncommitted B1 edit along with the `medium` line. The rerun then showed the original `opus` command line and 3 failed checks.
- **The fix:** B1 was re-applied from the same dictated text and the whole V1 sequence was run again: green, then the negative control, then the revert by `sed`, then green. Every figure above comes from that second sequence.
- The committed `vps/run.py` matches the dictated block byte for byte; see the diff in `## Implementation Summary`.

## Pre-existing Issues

- **The `vps/selftest.py` docstring is now incomplete.** It lists the TZs whose sections it holds, up to TZ-58, and does not name TZ-59. The TZ asked for a docstring change in `vps/run.py` only, so the selftest docstring was left as it was.

## Remaining Risks

- **The cost of a run at `high` is unmeasured.** TZ-58 measured one completed run on the alias `opus` at its default effort: 83 752 output tokens, 11 941 234 cache-read tokens and 10.09 dollars at the API's price. The first run after the merge logs its usage, and the TZ that reads the first six runs reads it. That is out of scope here (§5).
- **The binary's acceptance of the pin was not checked live.** Rule 1 forbids running the `claude` binary. The derivation rests on TZ-58's report-2: `/usr/bin/claude` 2.1.282, with `--effort` offering `low, medium, high, xhigh, max`.

## Commit

Implementation, on branch `tz-59-run-model-pin`:

- Commit `9c1af521e0958a95b902b6e19e7c782729a754de`, already pushed: `TZ-59: vps — the run on claude-opus-5-5 at high effort`.
- Contents: `vps/run.py`, `vps/selftest.py`.

Report, on `main`:

- Message: `TZ-59: report — the run's pinned model and effort`.
- Contents: `CryptoReports/TZ-59-run-model-pin-report.md`.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/48 — `tz-59-run-model-pin` → `main`.

## CI Execution

- **Bench gate** (`bench.yml`), run `37152417609`, triggered by the `pull_request` event at head `9c1af521e0958a95b902b6e19e7c782729a754de`. Status `completed`, conclusion **`success`**; its job `bench` also concluded `success`. This was read with `gh run view`.
- No other workflow ran on the branch.

## Final Repository State

- **Branch:** `tz-59-run-model-pin` at `9c1af521e0958a95b902b6e19e7c782729a754de`, pushed. Its `vps` tree is `36f06177a8899162865e17157d57d643c58e1adc`.
- **Working tree:** clean, and `__pycache__` was removed.
- **NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

**Map:**

- `SYSTEM-MAP-CRYPTOCALCUL.md`: 3205 lines, MD5 `255286398a8f28203717a4187d9124f6`. Both match the TZ.
- Revision string: `**Revision 2026-10-03-e.**`, as required.

**Anchors.** The anchor table in the map's `## 0` was cut by structure: every `|` row after the `|---|` separator under the header `| Anchor |`, until the table ends.

- The table's own row count is **7**, and **7** anchors were compared.
- Each anchor was matched with `grep -oF -m1 -- "<anchor>" SYSTEM-MAP-CRYPTOCALCUL.md`.
- Each anchor is also quoted in the TZ header: `grep -cF` over the TZ returned ≥ 1 for each.

| Anchor | Text returned |
|---|---|
| revision | `**Revision 2026-10-03-e.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

**Files**, measured on `origin/main` at `02be078`:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | match; line 3 reads `**Version 26.**` |
| `vps/run.py` (before) | 331 | `4be5ada20662f7876715b15b5250722d` | match |

- `origin/main:vps` is `94a55b6f07d6aa6b2290eb3b4646f1740cd1a47e`, which is the tree the TZ was written against.
