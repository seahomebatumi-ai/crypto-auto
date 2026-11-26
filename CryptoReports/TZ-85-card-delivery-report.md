# Implementation Report — TZ-85

## Status
COMPLETED

## Inbound Filing
None.

## Scope Executed
Branch TZ (contract §8): two repository files besides this report, on branch `claude/tz-85-card-delivery`, by §6's patch applied through `kit stage`. Run from a linked worktree: `kit ready` took a detached `HEAD` at `origin/main` (`6693104`); the base the patch was written against, `216ac3c`, is an ancestor. The branch push ran no hosted workflow.

## Files Created
None.

## Files Modified
- `vps/score.py` — 953 lines, SHA-256 `05a2f98a1627dbd5…` = manifest.
- `vps/selftest.py` — 4560 lines, SHA-256 `23a19ae93fa6c83f…` = manifest.

## Files Renamed
None.

## Files Deleted
None.

## Implementation Summary
§6's patch only (`CryptoTZ/TZ-85-card-delivery.patch`, 35531 bytes, SHA-256 `b613f6ed545d1e96…` = manifest), applied by `kit stage`; no hand edit. The patch's behaviour is the TZ's §1 and §5 and was not read or judged by the session.

## Validation
- Baseline: `kit log selftest-base` — `selftest: sections 29 checks 842 failed 0 empty 0` — **G1 met**. Log `52c791137e176b4e…`.
- V1 `kit stage TZ-85` — `stage: PASS branch claude/tz-85-card-delivery · 2 file(s) staged = manifest`.
- V2 `kit log pycompile` — exit 0, 0 lines. Log `e3b0c44298fc1c14…`.
- V3 `kit log selftest` — exit 0, 33 lines; `section AC: checks 30 failed 0`, `section AD: checks 18 failed 0`, `selftest: sections 30 checks 861 failed 0 empty 0` — **G2 met**. Log `06d0e10c51e8eec8…`.
- V4 `kit log delivered-1126`, the daily close's user (`cryptoauto`) in `crypto-score.service`'s sandbox, on the deployer's clone — exit 0, one line, `1795685159000` — **G3 met**. Log `636f118a5f6bfe35…`. `/tmp/tz85-vps` removed afterwards.
- V5 `kit units` — `units: PASS 18 crypto unit(s) read · none transient`; `git status --porcelain --untracked-files=no` after the commit — 0 lines.
- R1 (reads only, nothing written under `/var/lib/crypto-auto/`):
  - `cards-files` (log `fbc6bc75396efb3d…`), in full: `ls: cannot access '/var/lib/crypto-auto/score-cards/': No such file or directory` and the same for `score-cards-done/`.
  - `cards-record` (log `355f8877d4f635da…`), in full: `2026-11-25 null` — `score.json` holds `asof` 2026-11-25 and no `cards` block.
  - `score-journal` (log `77a970c7a337c428…`): the one run since 2026-11-26 00:00, started 00:10:00Z, finished 00:10:11Z, `Finished crypto-score.service`; its `score:` line carries no `cards` field.
  - Result: R1 registers nothing — **G4 met**. No file under `score-cards/` exists, so none stands under TZ-84's rule.

## Test Results
- `selftest: sections 30 checks 861 failed 0 empty 0` (baseline 29 / 842).
- Local runs only. No CI step executes `vps/selftest.py` (TZ §4).

## Deviations
- The commit message is §7's text verbatim, followed by the one attribution trailer the harness requires on commits.
- The session was started in a linked worktree; §4a step 1's detached `HEAD` at `origin/main` applied (contract v33).

## Pre-existing Issues
`kit close` prints one pattern warning, `secrets: WARN … vps/selftest.py: 6 anthropic key pattern(s)`: the selftest's planted `sk-ant-oat01-selftest-…` fixture strings (`os.urandom`-suffixed, built in code), which `origin/main`'s `vps/selftest.py` already carries. Zero credential-value hits (`values 10 · 0 value hits`). Not fixed.

## Remaining Risks
- The patch's behaviour against live cards is unmeasured: the card ledger has not yet run on the host (R1), so TZ-85's rules are covered by selftest section AD alone until the deployer installs the merge.

## Commit
Branch `claude/tz-85-card-delivery`, one commit, message: `TZ-85: vps — the card ledger follows each card from the minute its answer reached main; a resolved card is read once; the exchange's refusal ends the pass`. Contents: `vps/score.py`, `vps/selftest.py`.

## Pull Request
https://github.com/seahomebatumi-ai/crypto-auto/pull/70 — titled `TZ-85: vps — cards from the minute the answer reached main`.

## CI Execution
None ran. `gh run list --branch claude/tz-85-card-delivery` returned no run: the branch changes only `vps/**`, which `bench.yml`'s gate paths do not read and `main.yml`'s two-literal allow-list excludes. Local checks only.

## Final Repository State
Branch `claude/tz-85-card-delivery` pushed with the one commit above, pull request #70 open. **NOT IN EFFECT UNTIL MERGED.** Fingerprints were taken against detached `HEAD` `6693104` = `origin/main`. No transient unit left.

## Fingerprints
- `fingerprint: PASS revision 2026-11-26-d · anchors 7 of 7 rows · files 4 measured, 0 differ · map md5 becadb8f`
- map 2782 lines md5 `becadb8f75e5b747dfe1732a149f46c7` revision 2026-11-26-d
- anchor revision, map line 17 · matched `**Revision 2026-11-26-d.**`
- anchor direction engine, line 54 · matched `### 3.12 Direction engine — veto cascade`
- anchor catalyst registry, line 55 · matched `### 3.15 Catalyst registry`
- anchor exhaustion measure, line 56 · matched `### 3.16 List exhaustion — the day-range measure`
- anchor analytical engine, line 57 · matched `## 11. Analytical engine`
- anchor squeeze block, line 58 · matched `### 3.17 «РИСК ВЫНОСА» — the day's own risk`
- anchor newest invariant, line 59 · matched `74. **A chat is handed off only under a marker`
- file `index.html` 3799 `4e71da9badca3ccae85b656fdc3773e8` = map
- file `main.py` 518 `0e3ead8c300d2ee6783303c4bf2fb6b5` = map
- file `catalysts.json` 17 `f9b2dd4a3594134b2b7b603de19075c3` = map
- file `bench/exhaustion-calibration.txt` 175 `3b8730b254467c9df4c0a845a0f3cfb3` = map
- added `vps/score.py` 834 `d29c79d140616efaf19f25b0ae5c2dc2` = header
- added `vps/selftest.py` 4384 `9301f48be4d2c6fbf8a23617e9ab73bc` = header

## Tokens
usage: claude-sonnet-5-5 calls 14 input 28 cache_creation 100979 cache_read 1154563 output 3809
usage: PASS calls 14 (main chain 14) input 28 cache_creation 100979 cache_read 1154563 output 3809 · peak context 100981
