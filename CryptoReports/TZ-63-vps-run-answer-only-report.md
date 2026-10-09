# Implementation Report — TZ-63

## Status

**COMPLETED.** The session ran on the VPS. `hostname` returned `vultr`, and every A0 answer matched the known one.

1. **The delivery test is built.** `vps/run.py`, `vps/selftest.py` and `vps/units/crypto-run.service` all match B4's MD5s and line counts on the first copy. V1 exited 0 with `selftest: sections 21 checks 314 failed 0 empty 0`, `section O: checks 27 failed 0` and `section U: checks 18 failed 0`. Each of the four negative controls failed exactly the checks the TZ registers. Control 1 failed **5**: the three `a status as the final message:` checks, `one line crypto-run: final message is not an answer chars=171` and `the summary carries answer_chars=0`. Control 2 failed **2**: `an answer after blank lines and indentation` and `an answer under emphasis`. Control 3 failed **1**: `exactly one Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`. Control 4 failed **2**, both in section O: `the run answered: exit 0` and `the answer went to the outbox`. No other check of the 21 sections failed in any control.
2. **The variable is set, and the installed CLI contains both names.** `vps/units/crypto-run.service` line 19 is `Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`. C1 found the program at `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`, 238767288 bytes. `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` appears **4** times in it and `run_in_background` **40** times. Neither count is `0`, so the TZ's conditional directory listing does not apply. The file was read by `readlink`, `ls`, `stat` and `grep` only, never executed.
3. **The record passes.** C2 printed `answers 48 refused 0` and `status refused`.
4. **The tree.** `git rev-parse origin/main:vps` and `/var/lib/crypto-auto/deployed-vps-tree` both read `d65dfbd5d1830b477a084e2f288a851e377d6947`.

The previous TZ, TZ-62, is merged. `git merge-base --is-ancestor d446a6b origin/main` exited 0, and `d446a6b` is `Merge pull request #50 from seahomebatumi-ai/tz-62-vps-alert-rule`.

## Inbound Filing

Nothing was moved. `CryptoTZ/TZ-63-vps-run-answer-only.md` sits at its canonical path on `origin/main`, in one copy (`git ls-tree -r --name-only origin/main | grep -ic tz-63` → `1`). It is 526 lines, blob `3ed8aa4291e6e905e79bf0ad864910f015872ad7`, uploaded in `102292f`. It was found after `git fetch --all --prune`. The clone is not shallow: `git rev-parse --is-shallow-repository` returned `false`.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names three files under `vps/`. The branch `tz-63-vps-run-answer-only` was opened from `origin/main` at `102292f7ed384698f617edf22789da110e7a1d22`.

| Stage | Executed | Outcome |
|---|---|---|
| A0 | yes | all four known answers |
| A1 (§4a 1–6, §5 gate, A1.1–A1.4) | yes | Gate passed: 7 rows, 7 compared. All nine edit lines counted `1`. Selftest baseline 20 / 296 / 0 / 0. |
| B1–B4 | yes | All three files at the TZ's MD5 and line count. |
| C1, C2 | yes | C1 is not registered: path, size and counts recorded. C2 matched its known answer. |
| V1–V6 | yes | see `## Validation` |

No credential arrived, was read or was written. No model session was opened and the `claude` binary was not run. The session's only network reads were `git` (fetch, push, ls-remote) and `gh` (`auth status`, `pr create`, `pr checks`, `run list`, `run watch`, `run view`). C2's script prints counts and file names only, and no answer text was printed by any command.

### A0 — the host, before the gate

```
$ hostname; systemctl is-active crypto-bot.service crypto-exchange.service; test -d /srv/crypto-auto/.git && echo clone; id -u cryptorun; date -u +%FT%TZ
vultr
active
active
clone
995
2026-10-09T16:11:32Z
```

### A1.1 — the tree

```
$ git rev-parse origin/main:vps; cat /var/lib/crypto-auto/deployed-vps-tree
d65dfbd5d1830b477a084e2f288a851e377d6947
d65dfbd5d1830b477a084e2f288a851e377d6947
```

### A1.2 — the edit lines on `origin/main` (`git show origin/main:<file> | grep -c -F -- <line>`)

| File | Line | Count |
|---|---|---:|
| `vps/run.py` | `RESULT_CATEGORIES = ("subtype", "api_error_status", "terminal_reason", "stop_reason")` | 1 |
| `vps/run.py` | `def category(value):` | 1 |
| `vps/run.py` | `    answered =(not is_error) and isinstance(result, str) and result.strip() != ""` | 1 |
| `vps/units/crypto-run.service` | `Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` | 1 |
| `vps/selftest.py` | `"is_error": False, "result": "SELFTEST-O-RESULT-TEXT",` | 1 |
| `vps/selftest.py` | `                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW")` | 1 |
| `vps/selftest.py` | `                           "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": writer_saw})` | 1 |
| `vps/selftest.py` | `SECTIONS = (("A", section_a),` | 1 |
| `vps/selftest.py` | `            ("T", section_t))` | 1 |

### A1.3 — unit state before C (V5 compares against this)

```
NRestarts=0
ActiveState=inactive
UNIT FILE               STATE   PRESET
crypto-run.path         enabled enabled
crypto-stop.path        enabled enabled
crypto-announce.service enabled enabled
crypto-bot.service      enabled enabled
crypto-cleanup.service  static  -
crypto-deploy.service   static  -
crypto-exchange.service enabled enabled
crypto-run.service      static  -
crypto-stop.service     static  -
crypto-cleanup.timer    enabled enabled
crypto-deploy.timer     enabled enabled

11 unit files listed.
```

### A1.4 — selftest before any edit

`python3 vps/selftest.py` on the branch at `102292f`: exit 0, `selftest: sections 20 checks 296 failed 0 empty 0`.

### Stage B — how the blocks were copied

A script read the TZ file between `## 12. Dictated blocks` and `## 13. Commit messages`. It split out the 14 fenced blocks, each as the lines between an opening fence and the next closing fence, each line ending in a newline. It asserted that every block is ASCII. It applied each block at its anchor, asserting the anchor occurs exactly once: §12.1 after its line, §12.2 before `def category(value):`, §12.3 replacing the `answered =` line, §12.4 after the `AUTO_MEMORY` line, §12.5's three whole-line replacements, §12.6's section U before `SECTIONS = (("A", section_a),`, and the `("T", section_t))` line replaced. No block was retyped. The same extraction produced §12.7's script, and `cmp` against the TZ's §12.7 block printed `script-equals-tz-block`.

### C1 — the CLI the run unit starts

```
$ p="$(readlink -f "$(command -v claude)")"; echo "$p"; ls -l "$p"
/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
-rwxr-xr-x 2 root root 238767288 Sep 24 21:21 /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
$ grep -a -c -F CLAUDE_CODE_DISABLE_BACKGROUND_TASKS "$p"
4
$ grep -a -c -F run_in_background "$p"
40
```

The file is 238767288 bytes, not a launcher under 1 MiB, and both counts are non-zero, so the directory listing was not run. `vps/run.py` line 52 starts the session as bare `claude`. Under the unit's own `PATH` (`vps/units/crypto-run.service` line 15), the only `claude` entries are `/usr/bin/claude` and `/bin/claude`. Both resolve with `readlink -f` to the same `claude.exe`, so C1 read the program the unit starts. This was checked as root over the unit's `PATH` directories, not as `cryptorun`.

### C2 — the delivery test on the record

```
$ install -d -m 0700 /root/tz63 && cp <extracted §12.7> /root/tz63/tz63_record.py
$ stat -c '%a %n' /root/tz63
700 /root/tz63
$ python3 /root/tz63/tz63_record.py "$PWD"
answers 48 refused 0
status refused
```

Exit 0. `ls analyst/log/*.md | grep -v '\.hunt\.md$' | wc -l` → `48`, and `git log --oneline ef89542..origin/main -- analyst/log | wc -l` → `0`: no log was added after `ef89542`. `/root/tz63` was removed afterwards, and `test -e /root/tz63` fails.

## Files Created

None.

## Files Modified

| File | Before (lines, MD5) | After (lines, MD5) |
|---|---|---|
| `vps/run.py` | 336, `beb420d158630b8e5801badf26aee2b4` | 351, `41161832221abd8a6d4f026c6b7b21d8` |
| `vps/selftest.py` | 1107, `53045fb9aafcf1c26252a4f76da2babe` | 1186, `e7fb68d609bd36965f76145528d2575e` |
| `vps/units/crypto-run.service` | 37, `dc6ac1073c42b03c1a2f3b754e28bca0` | 38, `9355ee94131624ff3fcdafe409183f38` |

`git diff --stat origin/main...HEAD`: 3 files changed, 100 insertions(+), 5 deletions(-).

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

- `vps/run.py` gains `ANSWER_HEAD`, «Время анализа:» written as `\u` escapes, and `ANSWER_MARKS = " \t*_#>"` (§12.1). It also gains `is_answer(result)` (§12.2): True only for a string with a line that opens with the head once leading whitespace and markdown marks are stripped. In `main`, `answered` is now `(not is_error) and is_answer(result)` (§12.3). A non-error, non-empty final message that is not an answer logs one line, `crypto-run: final message is not an answer chars=<len>`, and goes down the unanswered path, which sends notice S7. The message's text is never logged.
- `vps/units/crypto-run.service` gains `Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` beside the auto-memory line (§12.4).
- `vps/selftest.py`: section O's stub now returns `run.ANSWER_HEAD + " SELFTEST-O-RESULT-TEXT"` through the new environment key `SELFTEST_O_RESULT`, which joins section O's saved and restored keys (§12.5). New section U (§12.6) holds 18 checks: one on the methodology's §2 skeleton, ten `is_answer` cases, six on `run.main` with the status of 09.10.2026 as the final message, and one on the unit file. It is registered as `("U", section_u)`.

`run.CLAUDE`, `run.PROMPT`, `run.APPEND`, `common.S7` and `vps/bot.py` were not touched (TZ §5).

## Validation

**V1 — selftest.** `python3 vps/selftest.py` on the branch: exit 0.

```
section O: checks 27 failed 0
section U: checks 18 failed 0
selftest: sections 21 checks 314 failed 0 empty 0
```

Sections A–T keep the same check counts as at A1.4 (32, 12, 4, 13, 12, 14, 8, 2, 4, 26, 2, 4, 19, 10, 27, 21, 3, 9, 35, 39), all with 0 failed.

**Negative controls.** Each was applied alone by an exact-once string replacement. Afterwards the three files were restored from copies, B4's three MD5s were read again (`41161832…`, `e7fb68d6…`, `9355ee94…` every time), and the selftest was green again (`sections 21 checks 314 failed 0 empty 0` every time).

| # | Change | Exit | Summary | `FAIL` lines on stderr |
|---|---|---:|---|---|
| 1 | `answered = (not is_error) and is_answer(result)` → the old non-empty test | 1 | `failed 5`, all in section U | `a status as the final message: exit 1` · `a status as the final message: one notice S7` · `a status as the final message: no answer in the outbox` · `one line crypto-run: final message is not an answer chars=171` · `the summary carries answer_chars=0` |
| 2 | `ANSWER_MARKS = " \t*_#>"` → `ANSWER_MARKS = ""` | 1 | `failed 2`, all in section U | `is_answer: an answer after blank lines and indentation is True` · `is_answer: an answer under emphasis is True` |
| 3 | line `Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` deleted | 1 | `failed 1`, in section U | `exactly one Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` |
| 4 | `"result": os.environ["SELFTEST_O_RESULT"],` → `"result": "SELFTEST-O-RESULT-TEXT",` | 1 | `failed 2`, all in section O | `the run answered: exit 0` · `the answer went to the outbox` |

In each control the summary's only non-zero `failed` section was the one listed.

**V2 — syntax.** `python3 -m py_compile vps/run.py vps/selftest.py`: exit 0. The `__pycache__` it produced is git-ignored (`git check-ignore -q vps/__pycache__` exit 0) and was removed.

**V3 — the units.** `systemd-analyze verify vps/units/*` from the branch: exit 0, 0 bytes of output.

**V4 — scope.** `git diff --name-only origin/main...HEAD`:

```
vps/run.py
vps/selftest.py
vps/units/crypto-run.service
```

**V5 — nothing touched.** After C, I wrote the same two `systemctl` readings to a file and ran `cmp` against A1.3's file, which printed `V5 equal`. `systemctl list-units --type=service --all 'run-*' --no-legend | wc -l` → `0`: no transient unit is left.

**V6 — pushes.** The branch `tz-63-vps-run-answer-only` was pushed with the implementation commit `cc6c4987567def7efa2ac821a58d7b6f516b45c9`, and pull request #51 was opened. This session sends nothing to `main` but this report.

## Test Results

| Check | Where | Result |
|---|---|---|
| `vps/selftest.py` baseline (A1.4) | VPS, branch at `102292f` | exit 0, 20 / 296 / 0 / 0 |
| `vps/selftest.py` (V1) | VPS, branch | exit 0, 21 / 314 / 0 / 0 |
| Negative controls 1–4 | VPS, branch | 5 / 2 / 1 / 2 failures, exactly as registered |
| `py_compile` (V2) | VPS | exit 0 |
| `systemd-analyze verify` (V3) | VPS | exit 0, no output |
| C2 record | VPS, branch checkout | `answers 48 refused 0`, `status refused` |
| Bench gate | GitHub runner, run 37957622134 | `success` (see `## CI Execution`) |

## Deviations

None.

## Pre-existing Issues

- **The hosted gate does not run `vps/selftest.py`.** `grep -n vps .github/workflows/bench.yml` prints nothing. The `success` in `## CI Execution` therefore covers the bench suite only. The selftest that guards this change runs only locally on the VPS (V1 here) and in the deployer before each install. This was true before TZ-63, and this TZ does not change it.

## Remaining Risks

- **Whether the variable keeps a subagent in the foreground is unmeasured** (TZ §5). C1 shows that the name `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` appears in the installed program, and nothing more. The first press after the merge measures it, in the run unit's journal. If the variable has no effect, the delivery test still keeps a status from reaching the owner, who gets «Анализ не завершён.» instead, and the hunt is lost as it was on 09.10.
- **The head is a fixed string in two places.** `run.ANSWER_HEAD` and `ANALYST-INSTRUCTIONS.md` §2's skeleton must move together (contract §4). Section U's first check fails if the methodology's skeleton stops opening with `run.ANSWER_HEAD`, and the deployer runs the selftest before installing. A methodology upload that changes the line would therefore stop the next `vps` install, but not a press already running on the installed code.

## Commit

Implementation, on the branch, already pushed: `cc6c4987567def7efa2ac821a58d7b6f516b45c9`

```
TZ-63: vps — the run delivers an answer or the notice, never a status; subagents cannot leave the foreground
```

It contains `vps/run.py`, `vps/selftest.py` and `vps/units/crypto-run.service`. The message is followed by a `Co-Authored-By:` trailer, as on TZ-62's `42ecda3`.

Report, on `main`:

```
TZ-63: report — the delivery test, the variable, and the record read through it
```

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/51 — `tz-63-vps-run-answer-only` → `main`.

## CI Execution

**Bench gate**, run `37957622134`, event `pull_request`, head `cc6c4987567def7efa2ac821a58d7b6f516b45c9`: `completed` / `success`, read with `gh run watch --exit-status` (exit 0) and `gh run view --json`. No other workflow ran on the branch: `gh run list --branch tz-63-vps-run-answer-only` lists that run alone. As `## Pre-existing Issues` says, this gate does not execute `vps/selftest.py`.

## Final Repository State

Branch `tz-63-vps-run-answer-only` at `cc6c4987567def7efa2ac821a58d7b6f516b45c9`, pushed, `vps` tree `96d72e8df795c79ad7d77c9ee73d4bbc284534e7`. The working tree was clean after the commit. On the VPS, `/root/tz63` is gone, every unit is in its A1.3 state and no transient unit is left. Nothing outside the repository was written except `/root/tz63`, which was created and removed.

**NOT IN EFFECT UNTIL MERGED.** The deployer installs the change after the merge, behind the selftest and `systemd-analyze verify`.

## Fingerprints

Taken against `origin/main` at `102292f7ed384698f617edf22789da110e7a1d22`.

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md`, 3365 lines, MD5 `a3d99eb9bcbd9965a18f80cfc0fbb281`. Its first revision line in `## 0` is `**Revision 2026-10-09-e.**`, the one the TZ requires.

**Anchor table.** It was cut by structure: the `| Anchor |` header at line 626, the separator at 627, then every following line beginning `|`. The table has **7 rows**, and **7 were compared**. For each row, the TZ header carries the identical `| <name> | `<anchor>` |` row, and the anchor occurs in the map. Each line below is `grep -n -o -F -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md`, showing the first match outside the table's own lines 628–634. Every anchor's total count is 2: the table row plus this occurrence.

| Anchor | Text returned |
|---|---|
| revision | `17:**Revision 2026-10-09-e.**` |
| direction engine | `1598:### 3.12 Direction engine — veto cascade` |
| catalyst registry | `1988:### 3.15 Catalyst registry` |
| exhaustion measure | `2085:### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `3106:## 11. Analytical engine` |
| squeeze block | `2252:### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `2794:72. **A write that fails leaves this run's product or nothing` |

**Files the map's `## 0` table lists**, all as required:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Files the TZ's gate adds**, on `origin/main` before the change:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 1028 | `5f50e8785755b340d2e8f07425432f44` | `**Version 28.**` present |
| `ANALYST-INSTRUCTIONS.md` | 4738 | `918a86d648a80e09c72c8c0f4660fbe8` | `**Revision 2026-10-09-b.**` present |
| `vps/run.py` | 336 | `beb420d158630b8e5801badf26aee2b4` | as the TZ states |
| `vps/selftest.py` | 1107 | `53045fb9aafcf1c26252a4f76da2babe` | as the TZ states |
| `vps/units/crypto-run.service` | 37 | `dc6ac1073c42b03c1a2f3b754e28bca0` | as the TZ states |

`origin/main:vps` = `d65dfbd5d1830b477a084e2f288a851e377d6947`, the tree the TZ was written against.
