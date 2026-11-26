# Implementation Report — TZ-83

## Status
COMPLETED. Every gate G1–G5 and validation item V1–V5 met; the hosted `Bench gate` run was still in progress when read (see `## CI Execution`).

## Inbound Filing
None.

## Scope Executed
Branch TZ (contract §8): `vps/run.py` and `vps/selftest.py` by the shipped patch alone, on branch `claude/tz-83-run-part-a-and-models`; plus the three readings R1–R3. Session ran in a linked worktree, `kit ready` took a detached `HEAD` at `origin/main` (`9338f18`) because `main` is held by `/root/crypto-auto`. TZ-82's earlier BLOCKED report was not in this session's context.

## Files Created
None.

## Files Modified
`vps/run.py` (375 → 394 lines), `vps/selftest.py` (4101 → 4130 lines).

## Files Renamed
None.

## Files Deleted
None.

## Implementation Summary
`kit stage TZ-83` applied `CryptoTZ/TZ-83-run-part-a-and-models.patch` unread and committed it with §7's message. No hand edit. No unit, timer or service was started.

## Validation
- `open`: PASS (self, ready, number, fingerprint 7 of 7, host the VPS, shipped patch 12072 bytes sha256 `b582511b77145d43` = manifest).
- G1, baseline before `stage` (log `selftest-base`, sha256 `1a28a327df1985cb`): `selftest: sections 28 checks 807 failed 1 empty 0`, the one FAIL `section U: ANALYST-INSTRUCTIONS.md section 2's skeleton opens with run.ANSWER_HEAD` — as G1.
- V1 `stage`: PASS, `vps/run.py` 394 lines sha256 `f039b2594d0c9988` and `vps/selftest.py` 4130 lines sha256 `7db8e7c9d3c918bd` = manifest.
- V2 `pycompile` (sha256 `e3b0c44298fc1c14`, empty): exit 0.
- V3/G2 `selftest` (sha256 `f46f7d80c59438c9`): exit 0, `selftest: sections 28 checks 813 failed 0 empty 0`, `section O: checks 39 failed 0`, `section U: checks 18 failed 0`.
- V4/G3 negative controls in copies of the tree: head line altered → `checks 813 failed 1`, FAIL in section U alone (`neg-head`, sha256 `e57235e5898a7a2b`); `# PART B` line altered → `checks 813 failed 1`, FAIL in section O alone (`neg-part`, sha256 `dafc88d5c101bc16`). Copy removed; `git status --porcelain --untracked-files=no` listed only `M vps/run.py`, `M vps/selftest.py`.
- V5 `kit units`: PASS 18 crypto units read, none transient.
- R1 (G4, log `cli-help` sha256 `b10f5c36adfe3285`, 2 matches): `--effort <level>                      Effort level for the current session` / `(low, medium, high, xhigh, max)` — as G4.
- R2 (logs `run-journal` sha256 `3c4396acd6592aa6`, `run-journal-1123` sha256 `82a806b3fb2fac28`; no line is a credential): the journal holds five presses since 01.11.2026. The journal carries no `crypto-run: usage model=` line yet, so the token fields are the run unit's aggregate ones.

| Press (UTC) | claude_exit | is_error | num_turns | answer_chars | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|---|---|---|
| 06.11 20:32 | 0 | false | 24 | 3278 | 40 | 56954 | 3067879 | 273335 | 7.4388 |
| 15.11 13:12 | 0 | false | 47 | 4098 | 92 | 58141 | 7588874 | 248453 | 8.2217 |
| 16.11 15:39 | 0 | false | 53 | 4439 | 100 | 69130 | 8451818 | 255323 | 8.0643 |
| 19.11 03:50 | 0 | false | 54 | 6818 | 108 | 91835 | 9742276 | 287626 | 10.3412 |
| 23.11 16:25 | 1 | true | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

  23.11.2026, every `crypto-run:` line verbatim:
  - `crypto-run: limits unit=crypto-run.service mem_available=377360384 swap_free=2525237248 budget=704643072 memory_max=301989888 memory_swap_max=402653184 set=0`
  - `crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=1 is_error=true num_turns=1 duration_ms=782 denials=0 answer_chars=0`
  - `crypto-run: models=- unpinned=- denied_tools=- subtype=success api_error_status=429 terminal_reason=api_error stop_reason=stop_sequence`
  - `crypto-run: memory_max=301989888 memory_swap_max=402653184 mem_available=377237504 swap_free=2525237248 memory_peak=301989888 memory_swap_peak=13922304 input_tokens=0 output_tokens=0 cache_read_tokens=0 cache_creation_tokens=0 cost_usd=0`

  The `models=… api_error_status=429 terminal_reason=api_error` line shows why no day log followed: the session ended after 782 ms on an API 429 with no turn run, so the writer's `analyst/live.json` push (`writer: gate_exit=0 committed=yes pushed=yes`) was the only commit.
- R3 (log `usage-old` sha256 `fdbcbe1f2dd8a68b`, every project directory of the repository listed): see `## Tokens`.

## Test Results
Selftest 813 checks, 0 failed, 0 empty (G2). No CI step executes `vps/selftest.py`.

## Deviations
None. Model in `kit usage` is the header's family (claude-sonnet-5-5).

## Pre-existing Issues
The selftest's head check failed on `main` at 807 checks / 1 FAIL (G1): a stale expectation, repaired by the shipped patch as the TZ states.

## Remaining Risks
The new per-model `crypto-run: usage model=` lines and the `xhigh` / Sonnet 5.5 settings take effect only after the deployer installs the merge; the first press after that is the first reading of them. The `vps` tree installs only from a GitHub-signed commit (item 15), so the merge must be done on GitHub.

## Commit
`TZ-83: vps — the run reads the contract's Part A and logs its tokens per model; the trader on xhigh, the page reader on Sonnet 5.5; the selftest's head check repaired (TZ-82's scope)` — `vps/run.py` and `vps/selftest.py`, commit `895e7ad`, pushed to `claude/tz-83-run-part-a-and-models`.

## Pull Request
https://github.com/seahomebatumi-ai/crypto-auto/pull/68 — titled `TZ-83: vps — the run reads its part and logs its tokens per model`, body naming this TZ and TZ-82.

## CI Execution
Branch push started two `Bench gate` runs (ids 45736401886 and 45736414402); both `in_progress` at the last read, no conclusion read. The patch's paths are not read by that gate; no workflow executes `vps/selftest.py`, so V3 is a local run only.

## Final Repository State
Branch `claude/tz-83-run-part-a-and-models` pushed at `895e7ad`, two files changed against `9338f18`. **NOT IN EFFECT UNTIL MERGED.** Fingerprints below were taken on a detached `HEAD` at `9338f18` = `origin/main`.

## Fingerprints
- `fingerprint: anchor revision             map line 17 · quoted yes · matched `**Revision 2026-11-26-b.**``
- `fingerprint: anchor direction engine     map line 55 · quoted yes · matched `### 3.12 Direction engine — veto cascade``
- `fingerprint: anchor catalyst registry    map line 56 · quoted yes · matched `### 3.15 Catalyst registry``
- `fingerprint: anchor exhaustion measure   map line 57 · quoted yes · matched `### 3.16 List exhaustion — the day-range measure``
- `fingerprint: anchor analytical engine    map line 58 · quoted yes · matched `## 11. Analytical engine``
- `fingerprint: anchor squeeze block        map line 59 · quoted yes · matched `### 3.17 «РИСК ВЫНОСА» — the day's own risk``
- `fingerprint: anchor newest invariant     map line 60 · quoted yes · matched `74. **A chat is handed off only under a marker``
- `fingerprint: map table rows 7 · header rows 7 · compared 7`
- `fingerprint: file index.html 3799 4e71da9badca3ccae85b656fdc3773e8 = map`
- `fingerprint: file main.py 518 0e3ead8c300d2ee6783303c4bf2fb6b5 = map`
- `fingerprint: file catalysts.json 17 f9b2dd4a3594134b2b7b603de19075c3 = map`
- `fingerprint: file bench/exhaustion-calibration.txt 175 3b8730b254467c9df4c0a845a0f3cfb3 = map`
- `fingerprint: added vps/run.py 375 36dc8f3bf39b44168674677c85aecd44 = header`
- `fingerprint: added vps/selftest.py 4101 25136248a1fba37be97af33b1e9a598c = header`
- `fingerprint: map 2783 lines md5 4ac1ebf55b6a03ac6e73215410fdc5e2 revision 2026-11-26-b`
- `fingerprint: PASS revision 2026-11-26-b · anchors 7 of 7 rows · files 4 measured, 0 differ · map md5 4ac1ebf5`

## Tokens
`kit usage TZ-83` (taken before this report was written):

usage: claude-sonnet-5-5 calls 16 input 32 cache_creation 108767 cache_read 1301172 output 4431
usage: PASS calls 16 (main chain 16) input 32 cache_creation 108767 cache_read 1301172 output 4431 · peak context 108769 · 2026-11-26T01:31:11.810Z to 2026-11-26T01:32:05.818Z


Documents read in full by this session: TZ-83 11 883 bytes and contract v33 52 023 bytes.

R3, the old form against the new — `usage:` line per TZ and the directory it was found in (`/root/.claude-sea/projects/`):
- TZ-80, `-root-crypto-auto--claude-worktrees-bridge-cse-01KgRjgwu9bKSKKi6mMHqNZQ`: `usage: PASS calls 66 (main chain 66) input 132 cache_creation 189927 cache_read 8419381 output 62231 · peak context 189929` — model claude-opus-5; read in full 143 638 + contract v31 57 581.
- TZ-81, `-root-crypto-auto--claude-worktrees-bridge-cse-01KgRjgukYsYE1dD9i9M5U92`: `usage: PASS calls 69 (main chain 69) input 138 cache_creation 209954 cache_read 10545614 output 44799 · peak context 209956` — model claude-opus-5; read in full 120 517 + contract v31 57 581.
- TZ-82, `-root-crypto-auto--claude-worktrees-bridge-cse-01KgRjguyzVwuLjGoPcmN4Sq`: `usage: PASS calls 12 (main chain 12) input 24 cache_creation 44735 cache_read 1051807 output 6431 · peak context 101343` — model claude-sonnet-5-5; read in full 10 912 + contract v32 52 031.
- TZ-83 for comparison: 16 calls, cache_read 1 301 172, output 4431, peak context 108 769.
