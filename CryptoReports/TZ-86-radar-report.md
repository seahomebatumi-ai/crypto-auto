# Implementation Report — TZ-86

## Status
COMPLETED

## Inbound Filing
None.

## Scope Executed
Branch TZ (contract §8): five repository files besides the report, by the shipped patch `CryptoTZ/TZ-86-radar.patch` (63796 bytes, SHA-256 `dc84a6ab…192c65d`, equal to the manifest). Branch `claude/tz-86-radar`. Nothing outside §1's list was touched.

## Files Created
- `vps/radar.py` (649 lines)
- `vps/units/crypto-radar.service` (20 lines)
- `vps/units/crypto-radar.timer` (10 lines)

## Files Modified
- `vps/selftest.py` — section AE (4560 → 4943 lines)
- `vps/manifest` — `crypto-radar.timer` (11 → 12 lines)

## Files Renamed
None.

## Files Deleted
None.

## Implementation Summary
The patch was applied by `kit stage TZ-86`; no hand edit. R1 ran as written.

## Validation
- `kit open TZ-86` — `open: PASS` (ready, number, fingerprint 7 of 7, host, shipped bytes).
- G1 baseline `selftest-base` — `selftest: sections 30 checks 861 failed 0 empty 0`; log sha256 `06d0e10c51e8eec84a131a4c04bbd0bdc3e1c5222ef840ff0fc64a61ccf51f59` (33 lines).
- V1 `kit stage TZ-86` — `stage: PASS branch claude/tz-86-radar · 5 file(s) staged = manifest`.
- V2 `pycompile` — exit 0, log sha256 `e3b0c442…b855` (empty).
- V3 `selftest` — exit 0, `section AE: checks 53 failed 0`, `selftest: sections 31 checks 914 failed 0 empty 0` (G2 met); log sha256 `1a83b0ae81b06fead5dba1120f4b4b88f195f5a9ccbd1b5dfbb86dc42cc0a7d0` (34 lines).
- V4 `units-verify` — exit 0, empty output.
- V5 R1 `radar-probe` — exit 0, 37 lines, sha256 `0fee1a8aadfb95e9c5c96318387da5706af62c45f55428bdff557f89647d16ed`: one `radar-probe:` line per channel row (35), the unlock line and the totals line.
- V6 `kit units` — `units: PASS 18 crypto unit(s) read · none transient`; `git status --porcelain --untracked-files=no` after the commit — 0 lines.

## Test Results
- Selftest: 861 → 914 checks, 0 failed, 0 empty; 30 → 31 sections.
- G3 line: `radar-probe: channels=35 read=33 refused=2 unlock=read`; unlock `next=5 no cliff=14 not covered=11`.
- G4 reading (what the VPS registers, no expectation): of 35 rows, 33 answered 200; `solana.com` (SOL|2) HTTP 429; ALGO|1 `robots unreachable`. All eleven GitHub rows and the GitLab row answered 200 on this host.
- R1 ran as `cryptoauto` with `MemoryMax=128M`; no OOM, exit 0. The staged copy `/run/tz86-vps` was removed afterwards.

## Deviations
- The commit message carries the TZ's §7 line verbatim, followed by the harness-mandated trailer `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
- One shell call during step 3 was denied by the session's auto-mode classifier before anything ran (my compound command ended with a pointless extra `kit log` invocation). Nothing was executed from it; I re-issued only the TZ-mandated commit, without that part. No effect on the work.
- A session that started on a stale worktree commit was brought to `origin/main` by `git switch --detach` (contract §4a step 1) before `kit open`. One TZ in this conversation; model per `kit usage` is `claude-sonnet-5-5`, equal to the header's family.

## Pre-existing Issues
`kit close` prints `secrets: WARN … vps/selftest.py: 6 anthropic key pattern(s)`: the strings are synthetic planted and decoy token fixtures of the selftest (random hex generated at run time), present identically on `origin/main`'s `vps/selftest.py` (6 matches); the patch adds none. Values compared: 0 hits. Not fixed.

## Remaining Risks
- G4: `solana.com` (429) and ALGO's `robots.txt` are unreachable from this host today; those lanes will read nothing until they answer. The program holds a refusing host for the pass as specified.
- No run reads `radar.json` yet (TZ §1); consumption is the methodology's next revision.

## Commit
Implementation commit on `claude/tz-86-radar` (pushed, pull request #71):
`TZ-86: vps — the radar: the list coins' own publications and the unlock index twice a day, one alert a pass, the book's view on each positive record` — five files, the shipped patch's result.

## Pull Request
https://github.com/seahomebatumi-ai/crypto-auto/pull/71

## CI Execution
No workflow ran on a runner for the branch: `gh run list --branch claude/tz-86-radar` returned no runs. The pushed paths are under `vps/`, which no workflow filter reads (TZ §4: no CI step executes `vps/selftest.py`). Every check above is local.

## Final Repository State
Branch `claude/tz-86-radar` at `89db770`, pushed, tree clean. Fingerprints were taken against detached `HEAD` = `origin/main` `6a8c160`. NOT IN EFFECT UNTIL MERGED.

## Fingerprints
- fingerprint: anchor revision — map line 17 · matched `**Revision 2026-11-26-e.**`
- fingerprint: anchor direction engine — map line 54 · matched `### 3.12 Direction engine — veto cascade`
- fingerprint: anchor catalyst registry — map line 55 · matched `### 3.15 Catalyst registry`
- fingerprint: anchor exhaustion measure — map line 56 · matched `### 3.16 List exhaustion — the day-range measure`
- fingerprint: anchor analytical engine — map line 57 · matched `## 11. Analytical engine`
- fingerprint: anchor squeeze block — map line 58 · matched `### 3.17 «РИСК ВЫНОСА» — the day's own risk`
- fingerprint: anchor newest invariant — map line 59 · matched `74. **A chat is handed off only under a marker`
- fingerprint: map table rows 7 · header rows 7 · compared 7
- fingerprint: file index.html 3799 4e71da9badca3ccae85b656fdc3773e8 = map
- fingerprint: file main.py 518 0e3ead8c300d2ee6783303c4bf2fb6b5 = map
- fingerprint: file catalysts.json 17 f9b2dd4a3594134b2b7b603de19075c3 = map
- fingerprint: file bench/exhaustion-calibration.txt 175 3b8730b254467c9df4c0a845a0f3cfb3 = map
- fingerprint: added vps/selftest.py 4560 2568459da91ffd1090f591a2c5528cd1 = header
- fingerprint: added vps/manifest 11 0a2518c1fc7fd989ef2dfd8aa770beef = header
- fingerprint: map 2782 lines md5 272226879a5ab8ff93c70674ad93630e revision 2026-11-26-e
- fingerprint: PASS revision 2026-11-26-e · anchors 7 of 7 rows · files 4 measured, 0 differ · map md5 27222687

## Tokens
usage: selector tz TZ-86 · sessions 1 · records 85 · unreadable lines 0 · subagent calls of no trigger 0
usage: claude-sonnet-5-5 calls 16 input 32 cache_creation 102593 cache_read 1321282 output 4145
usage: PASS calls 16 (main chain 16) input 32 cache_creation 102593 cache_read 1321282 output 4145 · peak context 102595 · 2026-11-26T19:21:58.088Z to 2026-11-26T19:23:19.271Z
