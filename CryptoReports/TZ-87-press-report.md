# Implementation Report — TZ-87

## Status
BLOCKED. `kit open TZ-87` failed the fingerprint gate (contract §5) before any work: the repository's System Map is revision `2026-11-26-e`, the TZ requires `**Revision 2026-11-27-a.**`.

To unblock: the Boss uploads the map `2026-11-27-a` to `main` (the TZ's Base line says the delivery carried it; commit `e1286ba` carries only `CryptoTZ/TZ-87-press.md` and `CryptoTZ/TZ-87-press.patch`) and re-sends `EXECUTE TZ-87`.

## Inbound Filing
None.

## Scope Executed
Class: branch TZ (contract §8) — read off the TZ's scope. Nothing was executed: no branch opened, no code staged, no baseline run, no push other than this report.

## Files Created
`CryptoReports/TZ-87-press-report.md` (this report).

## Files Modified
None.

## Files Renamed
None.

## Files Deleted
None.

## Implementation Summary
None — blocked at `open`.

## Validation
- `kit open TZ-87` ready: PASS, detached HEAD `e1286ba` = `origin/main`, tracked tree clean, previous TZ-86 merged, 0 branches ahead.
- number: PASS, `CryptoTZ/TZ-87-press.md`; report path `CryptoReports/TZ-87-press-report.md`.
- fingerprint: FAIL — `BLOCKED -- revision; not in the map's table: revision`. The map's revision string is `**Revision 2026-11-26-e.**`; the header requires `**Revision 2026-11-27-a.**`. All six other anchors quoted and matched (table rows 7, header rows 7, compared 7). The newest-invariant anchor 74 matches in the older map too.
- Files of the map's `## 0` table: `index.html` 3799 `4e71da9b…`, `main.py` 518 `0e3ead8c…`, `catalysts.json` 17 `f9b2dd4a…`, `bench/exhaustion-calibration.txt` 175 `3b8730b2…` — all equal to the map.
- Added-files table: `vps/run.py` 413, `vps/selftest.py` 4943, `analyst/README.md` 15, `.github/workflows/bench.yml` 157 — all equal to the header.
- host: PASS the VPS. Shipped `CryptoTZ/TZ-87-press.patch` 185906 bytes, sha256 `a18236ac…` = manifest.
- No branch, local or remote, carries the string `2026-11-27-a` in its map (scanned every ref).

## Test Results
Not run — blocked before baseline (G1 unmeasured).

## Deviations
None. The gate's rule (§5) is applied as written.

## Pre-existing Issues
None found. The map on `main` (2782 lines) is simply older than the TZ's expectation (2787 lines).

## Remaining Risks
None beyond the block: no state was changed on the VPS or in the repository besides this report.

## Commit
The report only, direct to `main`, message `report: TZ-87 BLOCKED (map revision)`.

## Pull Request
None — no branch was opened: blocked before any work, and the report is on the `CryptoReports/**` path (§8).

## CI Execution
None — nothing was pushed that a workflow reads.

## Final Repository State
The checkout the fingerprints were taken against: detached `HEAD` at `e1286ba` = `origin/main`, tracked tree clean. `kit units`: PASS, 20 crypto unit(s) read, none transient.

## Fingerprints
- `fingerprint: map 2782 lines md5 272226879a5ab8ff93c70674ad93630e revision 2026-11-26-e`
- `fingerprint: FAIL BLOCKED -- revision; not in the map's table: revision`
- anchors matched: `### 3.12 Direction engine — veto cascade` (line 54) · `### 3.15 Catalyst registry` (55) · `### 3.16 List exhaustion — the day-range measure` (56) · `## 11. Analytical engine` (57) · `### 3.17 «РИСК ВЫНОСА» — the day's own risk` (58) · `74. **A chat is handed off only under a marker` (59)

## Tokens
usage: selector tz TZ-87 · sessions 1 · records 61 · unreadable lines 0 · subagent calls of no trigger 0
usage: claude-sonnet-5-5 calls 7 input 14 cache_creation 41558 cache_read 548742 output 2566
usage: PASS calls 7 (main chain 7) input 14 cache_creation 41558 cache_read 548742 output 2566 · peak context 98166 · 2026-11-27T12:48:58.756Z to 2026-11-27T12:49:27.466Z
