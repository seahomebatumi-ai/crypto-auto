# Implementation Report — TZ-87

## Status
COMPLETED. Every gate G1–G5 met; every validation item V1–V7 passed. The branch awaits the Architect's verdict; nothing is merged.

## Inbound Filing
None.

## Scope Executed
Class: branch TZ (contract §8) — read off the TZ's scope: five repository files besides the report, and block C's two probe commits on its own branch. Executed in full: baseline, `stage`, V1–V4, R1, push, block C, pull request. This is the re-run of the TZ after its earlier BLOCKED attempt (map revision `2026-11-27-a` was then absent from `main`); `main` now holds the map at that revision and the earlier BLOCKED report is no longer on `main`, so this report takes the canonical name.

## Files Created
`vps/press.py` (1964 lines) — by the shipped patch. `CryptoReports/TZ-87-press-report.md` (this report), direct to `main`.

## Files Modified
`vps/run.py` (547), `vps/selftest.py` (5707), `analyst/README.md` (17), `.github/workflows/bench.yml` (162) — by the shipped patch, nothing else.

## Files Renamed
None.

## Files Deleted
None. Block C's probe files `analyst/press/probe.json` and `analyst/score/probe.json` were added and removed on the branch; the branch's tip holds neither.

## Implementation Summary
The shipped patch `CryptoTZ/TZ-87-press.patch` (185906 bytes, sha256 `a18236ac…` = manifest) applied through `kit stage`; no hand edit. Shadow mode as the TZ states: nothing the session runs calls the press yet. The branch carries three commits: the implementation (TZ §7 message verbatim), the block C probe, and its removal.

## Validation
- open: PASS — kit pin `3716dc4b…`, detached HEAD `be8b2b0` = `origin/main`, previous TZ-86 merged, 0 branches ahead, fingerprint PASS, host PASS (the VPS), shipped bytes = manifest.
- **G1 baseline:** `kit log selftest-base` — `selftest: sections 31 checks 914 failed 0 empty 0` — met. sha256 `1a83b0ae81b06fea…`.
- **V1** `kit stage TZ-87` — PASS, five files at the manifest's lines and SHA-256 (`press.py` 1964 `980ef000…`, `run.py` 547 `22527db4…`, `selftest.py` 5707 `04c74a27…`, `README.md` 17 `797bd096…`, `bench.yml` 162 `4eabb997…`).
- **V2** `kit log pycompile` — exit 0, 0 lines.
- **V3** `kit log selftest` — exit 0, `selftest: sections 33 checks 1078 failed 0 empty 0`, `section AF: checks 153 failed 0`, `section AG: checks 11 failed 0` — **G2 met**. sha256 `c1dde239…`. `kit log sections` diff of every other section's line against G1's log — exit 0, no line.
- **V4** `kit log bench-yml` — `5 0` and `2`: five lines added, none removed, both paths among them.
- **V5 / R1** `kit log press-r1` — exit 0, sha256 `65a1dee4…`. One `press:` line: `stem=2026-11-27 gate=3 cards=4 refused=1 reads=183 seconds=14.2 brief_bytes=5528 sha256=ad1affc3c84f book=list_31/31_outside_22/22 coingecko=ok deriv=binance,bybit etf=stands map=ok_180_bars positioning=read_34_unread_0 production=ok score=ok structural=2026-11-26.jsonl_ok`. systemd: result success, runtime 14.404 s (inside `PRESS_TIMEOUT_S` 600), CPU 1.102 s, **Memory peak 1.1M**, swap peak 0B, under the run unit's `MemoryMax` 335544320 and `MemorySwapMax` 369098752 (read from `crypto-run.service`). **G3 met.** `kit log press-r1-brief` (sha256 `96a7bdbd…`): record `2026-11-27.json` 36634 bytes, brief `2026-11-27.md` 5528 bytes; the brief opens `PRESS 2026-11-27 · freeze 2026-11-27T13:00:51Z · gate 3 · record analyst/press/2026-11-27.json` and `lanes short: none`. **G4 — reported, registers nothing:** lanes answering this host: Binance and Bybit derivatives, CoinGecko, ETF record, map 180 bars, positioning 34 read 0 unread, 183 reads, 14.2 s, brief 5528 bytes. Scratch tree removed (`/var/lib/cryptorun` holds only `crypto-auto`).
- **V6 / block C — G5 met.** Commits: implementation `2786d48afbffe944a6905d41c6cd959e0639f489`; probe `e533ab3a23c3f144cc8f5616e58eb7fb2207660c`; probe removed `e7d391fed144f78029c92835ff68c9e8b7f4605b`. `kit log ci-runs` at the three-minute mark, read at 13:04:27 UTC (sha256 `9b2532dd…`): one `bench.yml` push run, id 46003491152, headSha `2786d48a…` (the implementation commit), completed, success; **no run listed against either probe commit.** The implementation push is the positive control.
- `kit close`: PASS, 0 credential-value hits; one pattern WARN — 7 `sk-ant-` strings in the shipped `vps/selftest.py`, each a fixture built as `selftest` plus `os.urandom` hex (6 such lines already on `main`; the patch adds one). Reviewed: not a credential.
- **V7:** `kit units` — PASS, 20 crypto unit(s) read, none transient. `git status --porcelain --untracked-files=no` after the commit — no line.

## Test Results
`vps/selftest.py`: 33 sections, 1078 checks, 0 failed, 0 empty, local run on this host under Python 3.12.3 (baseline 31 / 914). Python 3.11 and 3.13 were not run here. R1: exit 0, one `press:` line. No CI step executes `vps/selftest.py`.

## Deviations
- **Observation on G3's source figure:** the TZ derives G3 from a 40 356 KiB peak against "the unit's 160 MiB"; this host's `crypto-run.service` reads `MemoryMax` 335544320 (320 MiB). systemd's own accounting printed `Memory peak: 1.1M` for R1's transient unit. The gate as written (exit 0 under the unit's own ceilings, inside the timeout, one `press:` line) is met; the two figures are stated for the audit and not judged here.
- The earlier BLOCKED attempt of this TZ is not part of this session's context, so this session's tokens are its own.

## Pre-existing Issues
None found.

## Remaining Risks
- Shadow mode: until the methodology's revision `2026-11-27-a` calls the press, only the unit's own code path (`vps/run.py`) exercises it, and that path first runs after the deployer installs the merge. R1 exercised `press.py` alone, not `run.py`'s push of the record and usage commits to `main`.
- The three-minute reading found no probe run; a probe run that started later than that reading would not appear in it.

## Commit
Implementation commit, on `claude/tz-87-press` and pushed: `TZ-87: vps — the press: the run's numbers in code before the model, its record and the session's spend on main`, with the five files above. Two probe commits follow it on the same branch, as above. The report's own commit is direct to `main`, message `report: TZ-87 press`.

## Pull Request
https://github.com/seahomebatumi-ai/crypto-auto/pull/72 — `TZ-87: vps — the press: the run's numbers in code before the model, its record and spend on main`, head `claude/tz-87-press`, base `main`.

## CI Execution
Read from the runner with `gh`: workflow `Bench gate` ran twice on the branch, both **success** — event `push`, run 46003491152 on the implementation commit `2786d48a…`; event `pull_request` on head `e7d391fe…`. No other workflow ran. The probe pushes started none. `vps/selftest.py` runs on no runner and was run locally only.

## Final Repository State
The branch `claude/tz-87-press` is pushed, three commits ahead of `main`, tracked tree clean; the checkout the session leaves is a detached `HEAD` at `origin/main` (`be8b2b0`) in the linked worktree. **NOT IN EFFECT UNTIL MERGED.** `kit units`: PASS, none transient.

## Fingerprints
- `fingerprint: map 2787 lines md5 3566be930d0d70060e2ed74b19bb4959 revision 2026-11-27-a`
- `fingerprint: PASS revision 2026-11-27-a · anchors 7 of 7 rows · files 4 measured, 0 differ · map md5 3566be93`
- anchors matched: `**Revision 2026-11-27-a.**` (line 17) · `### 3.12 Direction engine — veto cascade` (54) · `### 3.15 Catalyst registry` (55) · `### 3.16 List exhaustion — the day-range measure` (56) · `## 11. Analytical engine` (57) · `### 3.17 «РИСК ВЫНОСА» — the day's own risk` (58) · `74. **A chat is handed off only under a marker` (59); table rows 7, header rows 7, compared 7
- files = map: `index.html` 3799 `4e71da9b…` · `main.py` 518 `0e3ead8c…` · `catalysts.json` 17 `f9b2dd4a…` · `bench/exhaustion-calibration.txt` 175 `3b8730b2…`
- files added by the gate = header, measured before the patch: `vps/run.py` 413 `b0b9c651…` · `vps/selftest.py` 4943 `feec4dc6…` · `analyst/README.md` 15 `f99d04e1…` · `.github/workflows/bench.yml` 157 `9d8687f5…`

## Tokens
usage: selector tz TZ-87 · sessions 1 · records 128 · unreadable lines 0 · subagent calls of no trigger 0
usage: claude-sonnet-5-5 calls 25 input 50 cache_creation 49508 cache_read 2386413 output 7327
usage: PASS calls 25 (main chain 25) input 50 cache_creation 49508 cache_read 2386413 output 7327 · peak context 108998 · 2026-11-27T12:59:55.785Z to 2026-11-27T13:04:30.720Z
