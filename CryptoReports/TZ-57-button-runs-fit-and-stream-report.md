# Implementation Report — TZ-57

## Status

**PARTIAL. This session did not run on the VPS, so every stage that reads the host is BLOCKED.** It ran in a cloud container (`hostname` → `vm`; PID 1 is `process_api`, not systemd; `/var/lib/crypto-auto`, `/etc/crypto-auto`, `/srv/crypto-auto` and `/var/lib/cryptorun` are absent). It has no route to the VPS, so it read none of the VPS's journals and started no unit there. What follows is what each scope decided, line by line:

1. **The fit: BLOCKED. No `fits` line was written.** A2 was not read: the run unit's journal is on the VPS. No invocation was classed and no footprint was chosen. `vps/memory-record.txt` and `vps/units/crypto-run.service` are unchanged. `budget_bytes` stays 704 643 072, which equals `common.record_limits` of the record (V4). **The host's answer: none.** The host stays as it is because nothing was decided, not because a run was shown to fit.
2. **Only the button requests a run.** `announce.act` and `exchange.act` no longer call `request_run`. The bot's call is the only one left (V5). `WATCHER_DAILY_CAP`, `R1` and `R2` are gone from `common.py`. `vps/units/crypto-run.timer` is deleted (E4), and the deployer removes it from the host at the merge (V3 replay).
3. **The model scope: BLOCKED.** A4 was not read, because the `claude` binary the run unit reaches is on the VPS. `run.py` keeps `--model opus` with no `--effort` (V6).
4. **`crypto-announce.service` is not listed.** C1 did not run. B2 (the documented `SUBSCRIBE`) is on the branch, as §9 C1 requires whatever C1 answers.
5. **The list reader is not built.** A3 and C2 did not run (both are VPS readings), so there is no baseline line. Only the alerts-only half of B3 is built.

**What unblocks the rest:** a Claude Code session on the VPS, as TZ-52 through TZ-56 had, executing A2, A3, A4, C1, C2 and the host halves of V3, V4 and V7–V10. The previous TZ is merged: `16ca733` (TZ-56's implementation) is an ancestor of `origin/main`, and the merge `4c67ebe` "Merge pull request #45 from seahomebatumi-ai/tz-56-run-lane-on-swap" is on `main`'s first-parent line (A1).

## Inbound Filing

None. `CryptoTZ/TZ-57-button-runs-fit-and-stream.md` is at its canonical path on `origin/main` in one copy, added by `5c26df0`.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names files under `vps/`, which is outside `CryptoReports/**`.

| Stage | Executed | Outcome |
|---|---|---|
| A1 | §4a steps 1–6; §5 gate | gate passed: revision `2026-10-03-c`, 7 of 7 anchor rows, 4 of 4 files, contract `**Version 26.**`, analyst `**Revision 2026-10-03-a.**` |
| A2 | **not run**: no VPS | fit scope BLOCKED: no classes, no decision, no chosen invocation |
| A3 | **not run**: no VPS | list scope BLOCKED (TZ: «Anything else») |
| A4 | **not run**: no VPS | model scope BLOCKED: `run.py` keeps `--model opus` |
| B1 | `common.py` | `record_limits` added; `request_run` reduced to the button's path; `WATCHER_DAILY_CAP`, `R1`, `R2`, `fcntl` removed |
| B2 | `announce.py` | `SUBSCRIBE` sent, `SUBSCRIBE` answer awaited; `act` alerts only |
| B3 | `exchange.py`, alerts-only half | `act` alerts only and returns the alert count; `with_request` and `requests=` removed; **list reader not built** (no L1) |
| B4 | **not built** | gated on A4's M1, which was not read |
| B5 | `selftest.py` | J and M changed, P replaced, R added; R's list checks not added (no L1) |
| C1 | **not run**: no VPS | stream scope BLOCKED: E3 does not list `crypto-announce.service` |
| C2 | **not run** (gated on L1, and no VPS) | — |
| E1 | record | unchanged: no `fits` line |
| E2 | `crypto-run.service` | unchanged: E1 moved nothing |
| E3 | `vps/manifest` | unchanged: already the five units in §10's order, `crypto-announce.service` not listed |
| E4 | `git rm vps/units/crypto-run.timer` | done |
| E5 | selftest | green: 18 sections, 200 checks |
| V1–V12 | validation | see `## Validation` |

## Files Created

None.

## Files Modified

| File | Hunks (`git diff -U0`) | Lines after | MD5 after |
|---|---:|---:|---|
| `vps/announce.py` | 7 | 405 | `cb4f9dfc6e3a428283652c4d21468af5` |
| `vps/common.py` | 7 | 329 | `0a54ae9169cc06e36465413d198f2c4b` |
| `vps/exchange.py` | 9 | 145 | `1f09fe5df3a056e012da9f0e2293bd50` |
| `vps/selftest.py` | 19 | 789 | `8fb4d4ad5ddca12e729a94fbf5210253` |

These files are in scope and unchanged, each with a diff of 0 lines against `origin/main`: `vps/run.py` (`4be5ada20662f7876715b15b5250722d`), `vps/memory-record.txt` (`9dddbda291d63f14a14a45d2a1c84d03`), `vps/units/crypto-run.service` (`dc6ac1073c42b03c1a2f3b754e28bca0`) and `vps/manifest` (`4368b19c14fa75cb5289526592f66096`).

The branch's `vps` tree is `c4eef2b1d03991c05a27464038f60d2a3307c14a`.

## Files Renamed

None.

## Files Deleted

| File | Lines | MD5 (at `origin/main`) |
|---|---:|---|
| `vps/units/crypto-run.timer` | 11 | `e5b87739eb28ca3ca0e4f6b0075a6b2c` |

## Implementation Summary

**B1 — `common.py`.**
- `record_limits(record)` implements §12.4 on `derive_limits`. It takes the larger of the input and run budgets, then adds the product's footprint term when `product_class` is `C` or `K-oom` and `product_footprint_bytes` is an integer. It takes the product's duration term when `product_class` is `C` and `product_duration_s` is a number. A `-` value or an absent key is an absent term.
- `derive_limits`, `test_limits` and `start_limits` are untouched.
- `request_run(source)` writes one request and returns `requested` when runs are enabled, and returns `disabled` otherwise. Its docstring says only the owner's button requests a run.
- The watcher branch, its lock, its per-day count file, `WATCHER_DAILY_CAP`, `R1`, `R2` and the now-unused `import fcntl` are removed. No other Russian string moved (§12.1).

**B2 — `announce.py` (§12.6).**
- `ANSWER_SUBTYPE = "SUBSCRIBE"` and `SUBSCRIBE = json.dumps({"command": "SUBSCRIBE", "value": TOPIC})`.
- `connect()` opens exactly as before, sends `SUBSCRIBE` once, then hands `answer_of` the frames until the 20 s deadline. A failed send raises inside the existing `try`, so it falls into the existing `connect failed` path.
- A `REGISTER` frame arrives in `skipped` and is logged by the existing `announce: command answer` line.
- `act()` writes the same A1 alert as before, with no request and no suffix, and returns `alerted` or `recorded`.
- `--measure` is unchanged. The module and `connect()` docstrings name the documented subscription, the alerts-only rule and TZ-57, and say that `REGISTER` answers every connection.

**B3 — `exchange.py` (§12.5), the alerts-only half.**
- `act(found, cur)` writes the same A2, A3 and A4 alerts as before, with no request and no suffix, and returns the number of alerts.
- `with_request` is removed. The poll line keeps every field except `requests=`.
- The module docstring names the alerts-only rule and TZ-57.
- **`LIST_*`, `list_children`, `list_articles`, `list_diff`, `list_poll`, `--list-once` and the hourly service hook are not built**, because A3's L1 was not read.

**B4 — not built.** `run.CLAUDE` is unchanged.

**B5 — `selftest.py` (§12.8).**
- **J:** `record_limits` against §12.4's five rows, on literal dicts holding the record's TZ-55 lines as `read_record` returns them (strings). That is 26 checks.
- **M:** TZ-55's «budget_bytes = the larger budget…» and «runtime_max_s from run_duration_s» are replaced by `record_limits` equality. TZ-55's «fits=yes exactly when the last run completed» is replaced by §12.8's five `fits` checks, which run only where `fits` is present. TZ-56's «manifest lists crypto-run.timer only when fits=yes» is replaced by «vps/units/ holds no crypto-run.timer» and «the manifest names no crypto-run.timer». TZ-55's other record checks and TZ-56's unit checks are unchanged. That is 14 checks.
- **P:** replaced by §12.8's list:
  - `answer_of` under `SUBSCRIBE`;
  - `connect()` against the existing fake socket, including that it sent exactly `[SUBSCRIBE]`;
  - with a new `spool_in` context that points `common.STATE_DIR`, `SPOOL_DIR`, `OUTBOX_DIR`, `REQUESTS_DIR` and `RUNS_ENABLED` at a temporary directory: `announce.act` on a listing-catalogue message titled «Binance Will List Bitcoin (BTC)» classed `list BTC` writes one alert and no request; `request_run("bot")` writes one request and returns `requested`; with runs disabled it writes none and returns `disabled`;
  - `common` has no `WATCHER_DAILY_CAP`, `R1` or `R2`.

  That is 21 checks.
- **R (new):** `exchange.act` on §12.8's `found`/`cur` returns 1, writes one alert and writes no request. That is 3 checks. `SECTIONS` gains `R`.

## Validation

| Item | Result |
|---|---|
| V1 Selftest | **passed.** `python3.12 vps/selftest.py`: exit 0, 18 sections, none empty, total `selftest: sections 18 checks 200 failed 0 empty 0`. Negative control: `(788529152, 5400)` → `(788529153, 5400)` in J's second §12.4 row gave exit 1 with only `FAIL section J: record_limits: product block C, footprint 524288000, duration 1200` (J 26/1; every other section 0 failed). After reverting it is green again and the MD5 is restored: `8fb4d4ad5ddca12e729a94fbf5210253` before and after. |
| V2 Syntax | **passed, with an environmental `systemd-analyze` result.** `python3.12 -m py_compile` ok on all 8 `vps/*.py`. `bash -n` ok on `install.sh` and `deploy.sh`. `systemd-analyze verify vps/units/*` exits 1 with one line, `crypto-deploy.service: Command /usr/local/libexec/crypto-auto/deploy.sh is not executable: No such file or directory`. `main`'s units give the identical line and exit 1 on this host. With `vps/deploy.sh` placed at that path (container only, removed afterwards), the branch's units verify with exit 0 and no warnings (D-5). |
| V3 Dry run | **failed as specified: no VPS.** On this host (0 installed `crypto-*` unit files) `bash vps/install.sh --dry-run` exits 0. It prints `would disable --now crypto-announce.service`, no `would enable --now crypto-announce.service`, and no line naming `crypto-run.timer`, because no installed timer exists here to be removed. A local replay with `origin/main`'s 10 unit files placed under `/etc/systemd/system/` (removed afterwards; D-4) prints exactly one line naming it, `install: would remove /etc/systemd/system/crypto-run.timer`. `systemctl list-unit-files 'crypto-*'` cannot be compared with A2's, because A2 was not read. |
| V4 The fit | **failed: A2 not read.** What is established: `common.record_limits(common.read_record())` → `(704643072, 5400)`, and the record's `budget_bytes=704643072` and `runtime_max_s=5400` are equal to it. The unit has `MemoryMax=167772160`, `MemorySwapMax=536870912` (= 704 643 072 − 167 772 160) and `RuntimeMaxSec=5400`. |
| V5 The button alone | **passed.** `grep -n -E 'request_run\|WATCHER_DAILY_CAP\|\bR1\b\|\bR2\b' vps/*.py` prints `vps/bot.py:391` (its one call), `vps/common.py:308` (the definition) and `vps/selftest.py` lines 608, 719, 720, 724, 728 and 729. It prints none in `exchange.py` or `announce.py`. |
| V6 The model | **not M1, because A4 was not read.** `run.CLAUDE[3:]` → `['--output-format', 'json', '--model', 'opus', '--allowedTools', 'Bash Read Write Edit Glob Grep WebSearch WebFetch', '--append-system-prompt', '<APPEND>']`. |
| V7 The stream | **failed: C1 not run.** |
| V8 The list | **failed: A3 and C2 not run.** |
| V9 Credentials | **failed as specified.** The credential files exist only on the VPS, so the exact-value scan could not run. Supplementary pattern scan for `sk-ant-…`, `-----BEGIN … PRIVATE KEY`, Telegram-token shape and 64-character alphanumeric strings: 0 hits in the diff's added lines; 0 in every branch `vps/` file except `selftest.py`, which has 3. Those 3 are the RFC 4231 HMAC vector and the `sk-ant-oat01-selftest-planted-`/`-decoy-` fixture prefixes, and `origin/main`'s copy holds the same 3. This session never received or read a credential. |
| V10 Nothing left | **failed as specified: no VPS.** This session started no unit anywhere. In this container `/var/tmp/tz57-*`, `/run/systemd/transient/tz57-*` and `/run/systemd/system.control/tz57-*` are absent, and `systemctl` reports `System has not been booted with systemd as init system`. |
| V11 No production file | **passed.** `git diff --name-only origin/main...HEAD` → `vps/announce.py`, `vps/common.py`, `vps/exchange.py`, `vps/selftest.py`, `vps/units/crypto-run.timer`. |
| V12 Pushes | **passed under §8's fallback.** The branch is pushed (`895d1dc`) and no pull request was opened (D-3). `main` gets nothing from this session but this report. |

## Test Results

Baseline at `origin/main` before any change: `selftest: sections 17 checks 181 failed 0 empty 0`.

After Stage E:

```
section A: checks 32 failed 0
section B: checks 12 failed 0
section C: checks 4 failed 0
section D: checks 13 failed 0
section E: checks 12 failed 0
section F: checks 6 failed 0
section G: checks 8 failed 0
section H: checks 2 failed 0
section I: checks 4 failed 0
section J: checks 26 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 14 failed 0
section N: checks 10 failed 0
section O: checks 24 failed 0
section P: checks 21 failed 0
section Q: checks 3 failed 0
section R: checks 3 failed 0
selftest: sections 18 checks 200 failed 0 empty 0
```

Before E4 the selftest printed exactly one failure, `FAIL section M: vps/units/ holds no crypto-run.timer`. That is the new check firing on the old tree.

**Section M's `fits` branch, probed (scratchpad only, not committed).** The committed record has no `fits` line, so those checks compared nothing on this tree (R-1). A probe ran `section_m` against copies of the record with a §12.3 block appended and the unit lines set accordingly:

| Probe | Checks | Failed | Failure lines |
|---|---:|---:|---|
| `fits=yes`, `C`, peaks 300000000 + 224288000 = 524288000; budget 788529152 | 19 | 0 | — |
| the same, unit's `MemorySwapMax=` not moved | 19 | 1 | `MemorySwapMax= equals budget_bytes - MEMORY_MAX_FLOOR_BYTES` |
| the same block, `budget_bytes` not re-derived | 19 | 1 | `budget_bytes = record_limits(record)[0]` |
| `fits=no`, `K-oom`, footprint 704643072; budget 1056964608 | 19 | 0 | — |
| `fits=yes` with `product_killed=1` | 19 | 2 | `fits=no exactly when…`, `fits=yes exactly when…` |
| footprint ≠ the sum of the peaks | 19 | 1 | `product_footprint_bytes = the sum of the two peaks` |
| `fits=no`, `K-timeout`, peaks `-` | 18 | 0 | — (the sum check is skipped) |
| `product_not_admitted` removed | 19 | 1 | `fits present: every TZ-57 12.3 key present` |

## Deviations

- **D-1. The session was not on the VPS.** Every VPS stage is BLOCKED under the TZ's own outcome for that scope, and every validation item that needs the host fails (contract §9: an item that cannot be run fails). The cause is the environment, not a choice. The non-VPS scopes were completed under contract §6 («If scope B is blocked, complete A and C»).
- **D-2. Branch name.** The work is on `claude/vibrant-albattani-ddmwh1`, not `tz-57-button-runs-fit-and-stream`. This session's harness assigns that branch and forbids pushing to another without explicit permission.
- **D-3. No pull request.** This session's harness forbids opening one without an explicit instruction, so contract §8's fallback applies (see `## Pull Request`).
- **D-4. V3's `would remove` line is a local replay.** It was taken in this container with `origin/main`'s unit files copied into `/etc/systemd/system/`, which held no `crypto-*` file before and holds none after. PID 1 here is not systemd, so nothing was loaded.
- **D-5. V2's `systemd-analyze verify` was also run with `vps/deploy.sh` placed at `/usr/local/libexec/crypto-auto/deploy.sh`.** The directory did not exist before and was removed after. This separates this host's missing install path from the units themselves.
- **D-6. Interpreter.** This container's `python3` is 3.11.15. Rule 7 names 3.12, so every program, the selftest and `py_compile` ran with `/usr/bin/python3.12` explicitly.
- **D-7. Section P has one extra check** beyond §12.8's list: «the message is classed list BTC» (`announce.match_title`). It confirms the fixture really is the `list BTC` case the TZ names.
- **D-8. The dictated commit messages (§14) are used verbatim.** Three clauses of the implementation message («the fit from the product's own runs», «the pinned model», «the exchange's own list») name scopes that are BLOCKED here. The commit carries neither the fit, nor the pin, nor the list reader. This report is the record of what landed.

## Pre-existing Issues

- **`systemd-analyze verify vps/units/*` exits 1 on any host where `deploy.sh` is not installed.** `crypto-deploy.service` names `/usr/local/libexec/crypto-auto/deploy.sh`. `origin/main`'s units give the identical result here. On the VPS that path exists, so this is not a product defect. It means V2's command is only meaningful on an installed host.
- Every fingerprint matched (`## Fingerprints`): no file of the map's table differs.

## Remaining Risks

- **R-1. Section M's `fits` checks have no data on this tree.** The committed record has no `fits` line, so those five checks compare nothing until a §12.3 block is written. The section itself is not empty (14 checks). The probe above shows each check fires.
- **R-2. Host debris from the removed cap.** The old watcher path wrote `/var/lib/crypto-auto/run-requests-<YYYY-MM-DD>` and `run-requests.lock`. After the merge nothing reads or writes them, and `cleanup.py` does not remove them (out of scope). Whether any exist on the host is unread.
- **R-3. B2 has not connected from this branch.** `connect()` now sends `SUBSCRIBE`. TZ-56 A5's second connection, on `main`'s code, was answered `REGISTER`/`SUCCESS` and then `SUBSCRIBE`/`SUCCESS` at 246 ms, but no connection has run this code. `crypto-announce.service` stays out of the manifest, so the merge does not start it.
- **R-4. A later VPS execution.** If this branch is merged, the VPS scopes (A2/E1/E2, A4/B4, C1/E3, A3/B3-list/C2) still need a session on the host. A re-run of TZ-57 there would meet a `vps` tree other than `b9f97526…` (a finding, never a block, by §0) and the B1–B3 changes already on `main`. Whether to merge this and specify the remainder, or to re-run TZ-57 on the VPS without merging, is the Architect's decision.
- **R-5. The exchange watcher's poll line loses `requests=`** after the merge. No reader in the repository parses it. `grep -rn 'requests=' vps/` matches only `run.py:238`, the run's own summary line, and `selftest.py:578`, section O's check of that line. An outside reader keyed on it would change.
- **R-6. No hosted workflow runs `vps/selftest.py`.** `bench.yml` does not name it. The selftest runs on the VPS inside `install.sh`, so a red selftest shows only at the deployer (notice S10). This is pre-existing design, reported so the CI result below is not read as covering `vps/`.

## Commit

Implementation, on `claude/vibrant-albattani-ddmwh1`, pushed: **`895d1dc93ef57bc8298c4aa7560f93141a8354fa`**.

```
TZ-57: vps — the button alone, the fit from the product's own runs, the pinned model, the documented subscription, the exchange's own list
```

Its contents: `M vps/announce.py`, `M vps/common.py`, `M vps/exchange.py`, `M vps/selftest.py` and `D vps/units/crypto-run.timer` (5 files, +208 −104).

Report, direct to `main`:

```
TZ-57: report — the button alone, the product's first runs, the stream and the list
```

Its contents: `CryptoReports/TZ-57-button-runs-fit-and-stream-report.md`.

## Pull Request

**No pull request exists.** This session's harness forbids opening one without an explicit instruction (contract §8 fallback).

- Branch: `claude/vibrant-albattani-ddmwh1`
- Compare URL: https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/vibrant-albattani-ddmwh1

## CI Execution

- **Bench gate** (`.github/workflows/bench.yml`), run 37146981908 (#184): event `push`, head `895d1dc93ef57bc8298c4aa7560f93141a8354fa` on `claude/vibrant-albattani-ddmwh1`, status `completed`, conclusion **`success`**. Read through the GitHub API by this session: https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/37146981908
- That workflow does not run `vps/selftest.py` (R-6). The selftest ran locally only, in this container under `/usr/bin/python3.12` (V1). A local run is not a runner run.
- `main.yml` did not run and cannot run from these paths. Its `push` trigger is a `paths` allow-list of exactly `main.py` and `.github/workflows/main.yml` (lines 29–31; `paths-ignore` appears only inside a comment), read before the report's direct push.

## Final Repository State

Branch `claude/vibrant-albattani-ddmwh1` at `895d1dc`, pushed before this report was written, parent `5c26df0` (`origin/main` at the start). Its `vps` tree is `c4eef2b1d03991c05a27464038f60d2a3307c14a` and its working tree is clean (`git status --porcelain` empty). On the VPS this session changed nothing and started nothing. It had no route there.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Gate commands: `git show origin/main:<path>` for every file. The map's `## 0. Fingerprint` block was cut by structure: the rows between each table's separator line and the first line that does not start with `|`.

- Map revision string (first in the block): `**Revision 2026-10-03-c.**`. The TZ requires `**Revision 2026-10-03-c.**`. They are equal.
- Anchor table: **7 rows; 7 compared.** Each row shows the fixed-string match the map returned, then the TZ header's own row:

| Anchor | Map match (text returned) | TZ header row present |
|---|---|---|
| revision | `**Revision 2026-10-03-c.**` | `\| revision \| `**Revision 2026-10-03-c.**` \|` |
| direction engine | `### 3.12 Direction engine — veto cascade` | yes, character for character |
| catalyst registry | `### 3.15 Catalyst registry` | yes |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | yes |
| analytical engine | `## 11. Analytical engine` | yes |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | yes |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` | yes |

- File table: **4 rows; 4 measured at `origin/main` `5c26df0`.**

| File | Required | Measured |
|---|---|---|
| `index.html` | 3799 · `4e71da9badca3ccae85b656fdc3773e8` | 3799 · `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 · `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 · `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 · `f9b2dd4a3594134b2b7b603de19075c3` | 17 · `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 · `3b8730b254467c9df4c0a845a0f3cfb3` | 175 · `3b8730b254467c9df4c0a845a0f3cfb3` |

- Files the TZ's gate adds:

| File | Required | Measured | Version / revision line |
|---|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 991 · `d7bd23785656896a119e0cb7f0fddad5` | 991 · `d7bd23785656896a119e0cb7f0fddad5` | `**Version 26.**` |
| `ANALYST-INSTRUCTIONS.md` | 3921 · `7f19dc64a596ee07ad8298ee2a59c8a4` | 3921 · `7f19dc64a596ee07ad8298ee2a59c8a4` | `**Revision 2026-10-03-a.**` |

- `SYSTEM-MAP-CRYPTOCALCUL.md`: 3183 lines, MD5 `470a2ed730a1827c5bd8578e29f066e3`, the same as the TZ's reported values.
- `origin/main:vps` at the start: `b9f97526335fa2a12f60bab9bd164ded1250dd7c`, which equals the tree the TZ was written against.
