# Implementation Report — TZ-76

## Status

**COMPLETED.** The patch of §7 was applied byte-exact and every validation item V1–V7 is met. The previous TZ, TZ-75, is merged: pull request #61 is merge commit `048fc99`, and `vps/paper.py` on `origin/main` is TZ-75's bytes (`a709359a…`, A1). No remote branch is ahead of `main` other than this TZ's own: `git rev-list --count origin/main..<branch>` over every remote branch, sorted descending, printed `1` for this TZ's branch and `0` as the largest value among the thirteen others (14 remote branches in all, counted after this one was pushed).

## Inbound Filing

None. `CryptoTZ/TZ-76-paper-absence-margin.md` was already at its canonical filename on `origin/main` (`69ab0ec`, «Add files via upload»); nothing was moved. The session's worktree stood at `0a078c1` when it started and was brought to `origin/main` with `git merge --ff-only origin/main` before any reading; that merge brought in TZ-75's merged implementation and the TZ file, and nothing else.

## Scope Executed

**Branch TZ** (contract §8): it authorises one repository file besides its report, `vps/paper.py`. Stages A–D of the TZ. Host: the VPS (`hostname` prints `vultr`; `crypto-paper.service` active), so stage C ran where the TZ requires it and A2 and V3 compare counts on one machine.

## Files Created

None in the repository but this report.

## Files Modified

- `vps/paper.py` — one line (line 81): `ABSENT_AFTER_DAYS = 3` → `ABSENT_AFTER_DAYS = 7`, with its trailing comment ending `(TZ-76)`. 1413 lines before and after.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

The patch of TZ-76 §7 was extracted from the TZ with its own command and applied with `git apply`; no hand edit. The constant `ABSENT_AFTER_DAYS` is the number of days back beyond which a 404 from `data.binance.vision` is an absence and nearer is a wait. Nothing else moved: no other constant, no record, no unit, no check of `vps/selftest.py`.

## Validation

### A0 — contract §4a steps 1–6 and the §0 gate

`git fetch --all --prune` ran before anything was assessed; `git rev-parse --is-shallow-repository` printed `false`. `origin/main` = `69ab0ec79409aed4e99aaa28c226fa8b27c2b246`.

The map's revision string is `**Revision 2026-10-26-a.**`, equal to the TZ's. The anchor table was cut by its structure, not by names:

```
awk '/^## 0\. Fingerprint/{s=1} s&&/^\| Anchor \|/{t=1;next} t&&/^\|---/{r=1;next} r&&/^\|/{print;next} r&&!/^\|/{exit}' SYSTEM-MAP-CRYPTOCALCUL.md
```

**7 rows in the map, 7 rows in the TZ's own table (cut the same way from its `## 0`), 7 compared**; `diff` of the two cuts printed nothing. Per anchor, `grep -F -o -m1 -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md` returned the anchor itself — every one listed under Fingerprints. Contract version line: `**Version 31.**`.

### A1 — the three added files

`EXECUTOR-INSTRUCTIONS.md` 859 lines `4390ee0b8bf1e8d7837afffcd7a5b803`; `vps/paper.py` 1413 lines `a709359a86f630c464fd92ee93f6ae2c` (not `057440a4…`, so pull request #61 is merged); `vps/selftest.py` 2627 lines `76e814ccbe18551a8f47d6f7eae09669`. Every line count and MD5 equals the TZ's table.

### A2 — baseline on unmodified `main`, on the VPS

`python3 vps/selftest.py` → exit 0, last line `selftest: sections 27 checks 592 failed 0 empty 0`. Per section (checks, all `failed 0`):

| A | B | C | D | E | F | G | H | I | J | K | L | M | N |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 32 | 12 | 4 | 13 | 12 | 14 | 8 | 2 | 4 | 26 | 2 | 4 | 19 | 10 |

| O | P | Q | R | S | T | U | V | W | X | Y | Z | AA |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 33 | 21 | 3 | 9 | 35 | 39 | 18 | 16 | 134 | 19 | 54 | 23 | 26 |

`section W: checks 134 failed 0`.

### B1/B2 — the patch

```
awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-76-paper-absence-margin.md > <scratchpad>/tz76.patch
```

13 lines, MD5 `4eabfe2a3c439e64462e03b7a0022d72` — as the TZ states. `git apply --check` then `git apply` printed no error. After it `vps/paper.py` is **1413 lines, `dd4bab0209f99e1da430c87042a92b9c`** — B2's required result. `git diff` showed exactly the one `-`/`+` pair of §7 and no other hunk.

### B3 — local commit

Committed on branch `claude/tz-76-paper-absence-margin` (created from `origin/main` with `git checkout -b … origin/main`) before stage C, so V4's restore returns the changed file.

### V1

`python3 -m py_compile vps/paper.py` → exit 0.

### V2

`wc -l` → 1413; `md5sum` → `dd4bab0209f99e1da430c87042a92b9c`. Equal to B2's requirement.

### V3

`python3 vps/selftest.py` on the committed branch → exit 0, `selftest: sections 27 checks 592 failed 0 empty 0`; `grep -c FAIL` on its output → 0; 27 lines of the form `section X: … failed 0`. The 27 per-section counts printed are, one for one, the table under A2 (including `section W: checks 134 failed 0`).

### V4 — negative control

`git status --porcelain` printed nothing. In the working tree `sed` set the line to `ABSENT_AFTER_DAYS = 10` (`git diff -U0` showed the `7`→`10` pair), then `python3 vps/selftest.py`:

```
exit=1
23:FAIL section W raised NotReady: /daily/klines/KAITOUSDT/1m/KAITOUSDT-1m-2026-01-20.zip
selftest: sections 27 checks 571 failed 1 empty 0
```

Exactly one `FAIL` line (`grep -c '^FAIL'` → 1), the line and the summary the TZ requires. Restored with `git checkout -- vps/paper.py`; then `git status --porcelain` printed nothing and `vps/paper.py` read 1413 lines, `dd4bab0209f99e1da430c87042a92b9c`.

### V5

`git diff --numstat origin/main...HEAD` → `1	1	vps/paper.py` — one line, one added, one removed.

### V6

`systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service`:

| When | MainPID | ActiveEnterTimestamp |
|---|---|---|
| before the session's first write | 3335716 | Thu 2026-10-29 20:15:20 UTC |
| after V4 | 3335716 | Thu 2026-10-29 20:15:20 UTC |
| after the pull request's runs, before this report | 3335716 | Thu 2026-10-29 20:15:20 UTC |

Equal. No unit, timer or service was created, enabled, started or restarted by this session — not even a transient one.

### V7

`.github/workflows/bench.yml` is not modified by the branch (V5 shows the branch's only changed path). `grep -c vps .github/workflows/bench.yml` → 1, and that line is a Russian comment about the `analyst/paper/**` `paths-ignore` entry; `grep -E 'run:|python|node' … | grep -c 'vps/'` → 0, so **no step of it executes `vps/**` code**. Its runs on the pushed head `62a99eb92fc4609d1ada84f1d2551126e41532f1`, read with `gh run view`:

| Run id | Event | Status | Conclusion |
|---|---|---|---|
| 40947983802 | push | completed | success |
| 40948012276 | pull_request | completed | success |

## Test Results

| Item | Result |
|---|---|
| V1 py_compile | exit 0 |
| V2 file identity | 1413 lines, `dd4bab0209f99e1da430c87042a92b9c` |
| V3 selftest on the branch | exit 0; 27 sections, 592 checks, 0 failed, 0 empty; every section equal to A2 |
| V4 negative control | exit 1; one `FAIL` (W15's absence check, margin 10); 571 checks, 1 failed; restored clean |
| V5 numstat | `1	1	vps/paper.py` |
| V6 service | MainPID and ActiveEnterTimestamp equal across the session |
| V7 bench.yml | no step executes `vps/**`; runs 40947983802 and 40948012276 completed, success |

## Deviations

1. **Patch path.** The extraction command was run exactly as written but with its output at the session's scratchpad directory instead of `/tmp/tz76.patch`; the output's line count and MD5 are the TZ's.
2. **Commit message.** The implementation commit's first line is §5's message verbatim; the harness's attribution line `Co-Authored-By: Claude Code <noreply@anthropic.com>` follows it after a blank line.
3. **A mis-addressed scratch file.** V3's first output was redirected to `$TMPDIR/v3.txt` with `$TMPDIR` unset, so it landed at `/v3.txt`; it was moved into the scratchpad directory before anything else ran. Nothing of it is in the repository, and the check's result does not depend on it (the same counts are printed above).

## Pre-existing Issues

None found in the files this TZ touched. This session did not re-measure the publication lag that §1 describes: a fetch from `data.binance.vision` in a session is not a product fact (contract §7 item 9) and no step of the TZ asks for one.

## Remaining Risks

- **Nothing is in effect until the merge and the deployer's install.** The running `crypto-paper.service` process was not touched (V6) and holds the code it started with. The TZ's deadline is **01.11.2026 00:00 UTC** (§1).
- **A genuine absence is now called after seven days.** Until then the books after that day wait, as §1 records; the Architect's decision, not mine.
- **Seven is a margin, not a measured lag.** The only measurement behind it is §1's: 28.10.2026's daily files still answering 404 about 36 hours after the day ended. If the publisher's lag ever exceeds seven days the loss §1 describes recurs, and this change cannot detect it.

## Commit

Implementation (first line, as given by TZ §5, followed by the harness attribution line): `TZ-76: vps — the paper test's booking waits seven days, not three, before calling an unpublished Binance file absent` — one file, `vps/paper.py`, one line changed. Made locally before stage C and pushed to `claude/tz-76-paper-absence-margin` before this report was written; its hash is `62a99eb92fc4609d1ada84f1d2551126e41532f1` (`git rev-parse HEAD` and `git rev-parse origin/claude/tz-76-paper-absence-margin` printed the same value).

Report: `TZ-76: report — the booking's absence margin`, one file, `CryptoReports/TZ-76-paper-absence-margin-report.md`, direct to `main`.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/62 — titled `TZ-76: paper booking — absence after seven days, not three`, its body naming TZ-76 and the deadline of §1. Branch `claude/tz-76-paper-absence-margin`.

## CI Execution

`bench.yml` ("Bench gate") ran on a runner twice on head `62a99eb92fc4609d1ada84f1d2551126e41532f1`: run `40947983802` (push) and run `40948012276` (pull_request), both `completed` with conclusion `success`, read with `gh run view`. Neither executes `vps/**` code (V7), so they are not evidence about this change's behaviour; that evidence is V3 and V4, which are **local runs on the VPS, not runner runs**. `main.yml` did not run for the branch: `gh run list --branch claude/tz-76-paper-absence-margin` listed no run of it, and its trigger is a `paths` allow-list of `main.py` and `.github/workflows/main.yml`, neither of which the branch changes.

## Final Repository State

Branch `claude/tz-76-paper-absence-margin` at `62a99eb92fc4609d1ada84f1d2551126e41532f1`, pushed before this report was written, one commit ahead of `origin/main` at `69ab0ec79409aed4e99aaa28c226fa8b27c2b246`. Working tree clean (`git status --porcelain` printed nothing); the `__pycache__` the selftest generated under `vps/` was removed. `vps/paper.py` on the branch is 1413 lines `dd4bab0209f99e1da430c87042a92b9c`. No persistent or transient unit is left behind (V6).

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — **2796 lines, MD5 `e911fceb5f07444fe306f116a550b9cf`**; revision `**Revision 2026-10-26-a.**`.

**Anchors:** 7 rows in the map, 7 in the TZ, 7 compared, the two cuts equal (A0). Text each `grep -F -o -m1` returned:

| Anchor | Text matched |
|---|---|
| revision | `**Revision 2026-10-26-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

**Files the map lists, at `69ab0ec`:**

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Files this TZ's gate adds, at `69ab0ec`:**

| File | Lines | MD5 |
|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` (`**Version 31.**`) | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` |
| `vps/paper.py` | 1413 | `a709359a86f630c464fd92ee93f6ae2c` |
| `vps/selftest.py` | 2627 | `76e814ccbe18551a8f47d6f7eae09669` |

Every file above equals its required line count and MD5; none differs.

**The branch's changed file:** `vps/paper.py` 1413 lines `dd4bab0209f99e1da430c87042a92b9c`. **The patch:** 13 lines `4eabfe2a3c439e64462e03b7a0022d72`.
