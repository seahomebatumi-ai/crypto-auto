# Implementation Report — TZ-84

## Status
COMPLETED

## Inbound Filing
None.

## Scope Executed
Branch TZ (§8): five files under `vps/` by `kit stage`'s patch, plus this report. R1 taken as the one reading. The session began on a snapshot of `main` behind `origin/main` (`9208ea2`), which did not yet hold TZ-84; it fast-forwarded to `81493e5` before reading the contract (§4a step 1). The previous TZ's branch (TZ-83) is merged.

## Files Created
None (`score-cards/` is the daily close's to make).

## Files Modified
`vps/book.py` (582 lines), `vps/score.py` (834), `vps/run.py` (413), `vps/common.py` (413), `vps/selftest.py` (4384) — 724 insertions, 55 deletions.

## Files Renamed
None.

## Files Deleted
None.

## Implementation Summary
`kit stage TZ-84` applied `CryptoTZ/TZ-84-card-ledger.patch` on branch `claude/tz-84-card-ledger` and committed it with §7's message; no hand edit.

## Validation
Local, on the VPS, Python 3.12.3. Logs by name and SHA-256 (full SHA-256 where it is the gate).
- Baseline G1, log `selftest-base` `f46f7d80c59438c9`: `selftest: sections 28 checks 813 failed 0 empty 0`, exit 0.
- Baseline G3 first half, log `arch-base` `8fc070223eac810b83a725e63c14585475319a83beff2e933992e6e60906ac48`: 9 lines, exit 0.
- V1 `kit stage TZ-84`: PASS, five files at their lines and SHA-256 = manifest.
- V2 log `pycompile` (`e3b0c44298fc1c14`, empty): exit 0.
- V3 log `selftest` `52c791137e176b4e`: exit 0, `section O: checks 39 failed 0`, `section AB: checks 145 failed 0`, `section AC: checks 29 failed 0`, `selftest: sections 29 checks 842 failed 0 empty 0` — G2.
- V4 log `arch-new` `8fc070223eac810b83a725e63c14585475319a83beff2e933992e6e60906ac48`; log `arch-cmp` exit 0 (`cmp` of `arch-base` and `arch-new`, no output) — G3 equal byte for byte; out of sample 298 −15.96 R, plan 303 −6.09 R, book held 121 +30.48 R.
- V4 log `late` `ab9a1e9748b6e3363204892d68ffc5ad9015a9e4dcc4d1287e951f94ad022292`: 9 lines, exit 0, `all out-of-sample trades 3435  win 0.29  mean R -0.227  total R  -779.97  PF 0.64` — G4.
- V5 log `card-1126` `aaf5d6977cb450f9`: `cards 10 differ 0` — G5.
- V6 `kit units`: PASS 18 crypto unit(s) read, none transient. `git status --porcelain --untracked-files=no` after the commit: 0 lines.
- R1 (G6, log `run-journal-1126` `048c0b4c4b5399f3`, 11 lines, no line is a credential): the journal holds one press since 26.11.2026. R1 registers nothing — G6.

| Press (UTC) | claude_exit | is_error | num_turns | answer_chars | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|---|---|---|
| 26.11 08:53 | 0 | false | 56 | 11490 | 104 | 120401 | 6751592 | 241606 | 12.2705 |

  `usage model=` lines of that press, and every `crypto-run:` line of it, verbatim:
  - `crypto-run: limits unit=crypto-run.service mem_available=406212608 swap_free=2568212480 budget=704643072 memory_max=335544320 memory_swap_max=369098752 set=0`
  - `crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=0 is_error=false num_turns=56 duration_ms=2011321 denials=0 answer_chars=11490`
  - `crypto-run: models=claude-opus-5-5,claude-sonnet-5-5 unpinned=- denied_tools=- subtype=success api_error_status=- terminal_reason=completed stop_reason=end_turn`
  - `crypto-run: memory_max=335544320 memory_swap_max=369098752 mem_available=405622784 swap_free=2568212480 memory_peak=336838656 memory_swap_peak=134471680 input_tokens=104 output_tokens=120401 cache_read_tokens=6751592 cache_creation_tokens=241606 cost_usd=12.270534899999994`
  - `crypto-run: usage model=claude-opus-5-5 input=108 output=142661 thinking=72994 cache_read=6773204 cache_creation=265440 web_searches=0 cost_usd=6.2603108`
  - `crypto-run: usage model=claude-sonnet-5-5 input=1089058 output=138735 thinking=30085 cache_read=8907031 cache_creation=321622 web_searches=75 cost_usd=6.010224099999998`

## Test Results
`vps/selftest.py`: 813 checks before, 842 after, 0 failed, 0 empty. Archive replay of the base and of the patched tree: 9 lines each, identical SHA-256.

## Deviations
- The session started in a linked worktree on a snapshot of `main` older than the TZ's upload; it fast-forwarded to `origin/main` `81493e5` before the contract and the TZ were read. `kit open` took a detached `HEAD` there (v33).
- `kit close` WARN `secrets: review origin/claude/tz-84-card-ledger:vps/selftest.py: 6 anthropic key pattern(s)`: read by grep, the matches are the selftest's planted fixtures a "selftest-planted" prefix plus os.urandom, shipped by the patch; 0 credential value hits.
- The session's own transcript is one conversation holding no earlier TZ; its model is `claude-sonnet-5-5`, the header's.

## Pre-existing Issues
None.

## Remaining Risks
- No CI step executes `vps/selftest.py` (TZ §4): the card ledger's first live close is the first run of `score.py`'s new path on real day logs.
- R1 holds a single press since 26.11.2026; S16 and S17 have not yet fired on the host.

## Commit
`TZ-84: vps — the card ledger follows every card the answer printed; the card a state gives and the late card's replay in book.py; notices S16 and S17; the trader back on high` — the five files above, on `claude/tz-84-card-ledger`, commit `90a4e62`, pushed.

## Pull Request
https://github.com/seahomebatumi-ai/crypto-auto/pull/69 — title `TZ-84: vps — the card ledger, the card a state gives, the run's two notices`, body naming this TZ.

## CI Execution
Read with `gh run list`: `Bench gate` run 45847899010 (event push) — success; `Bench gate` run 45847905443 (event pull_request) — success. Neither executes `vps/selftest.py`; the local runs above are not runner runs.

## Final Repository State
Branch `claude/tz-84-card-ledger` at `90a4e62`, pushed, one commit above `origin/main` `81493e5`, five files. **NOT IN EFFECT UNTIL MERGED.** Fingerprints were taken against detached `HEAD` `81493e5` = `origin/main`.

## Fingerprints
- `fingerprint: map 2783 lines md5 bc26cde00272340bc1ca03173d809f97 revision 2026-11-26-c`
- `fingerprint: PASS revision 2026-11-26-c · anchors 7 of 7 rows · files 4 measured, 0 differ · map md5 bc26cde0`
- `anchor revision` map line 17 · `**Revision 2026-11-26-c.**`
- `anchor direction engine` map line 55 · `### 3.12 Direction engine — veto cascade`
- `anchor catalyst registry` map line 56 · `### 3.15 Catalyst registry`
- `anchor exhaustion measure` map line 57 · `### 3.16 List exhaustion — the day-range measure`
- `anchor analytical engine` map line 58 · `## 11. Analytical engine`
- `anchor squeeze block` map line 59 · `### 3.17 «РИСК ВЫНОСА» — the day's own risk`
- `anchor newest invariant` map line 60 · `74. **A chat is handed off only under a marker`
- `map table rows 7 · header rows 7 · compared 7`
- `file index.html 3799 4e71da9badca3ccae85b656fdc3773e8 = map`
- `file main.py 518 0e3ead8c300d2ee6783303c4bf2fb6b5 = map`
- `file catalysts.json 17 f9b2dd4a3594134b2b7b603de19075c3 = map`
- `file bench/exhaustion-calibration.txt 175 3b8730b254467c9df4c0a845a0f3cfb3 = map`
- `added vps/book.py 419 4e283c02783b4f959c49b613b4e518a5 = header`
- `added vps/score.py 613 eb76418a35e4c9389a80e61b1d449387 = header`
- `added vps/run.py 394 870669d4ab7ce889ad619a2595ccfcc2 = header`
- `added vps/common.py 401 d307c80cdc9cc0694496d8705dc63cfc = header`
- `added vps/selftest.py 4130 87fb628b69675afb3c878f29040b9f26 = header`

## Tokens
usage: claude-sonnet-5-5 calls 18 input 36 cache_creation 107776 cache_read 1544107 output 5408
usage: PASS calls 18 (main chain 18) input 36 cache_creation 107776 cache_read 1544107 output 5408 · peak context 107778 · 2026-11-26T15:15:12.231Z to 2026-11-26T15:20:34.328Z
