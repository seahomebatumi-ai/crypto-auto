# Implementation Report — TZ-66

## Status

**COMPLETED.**

1. **The code.** B1's patch extracted from `origin/main:CryptoTZ/TZ-66-run-subagent-model-pin.md` by the one command
   the TZ gives: MD5 `c5cc1d197d912fd61e55d364e7628a25`, **132 lines** — the known answer; `git apply --check` and
   `git apply` both exit 0, nothing was retyped. After the apply: `vps/run.py` **360** lines, MD5
   `07f672e5bcea06be27508db66aa3a8e0`; `vps/selftest.py` **1830** lines, MD5 `ce6220cdf2a45709bd1f09596e209ee9` —
   B2's known answers exactly. V1: exit 0, `selftest: sections 23 checks 437 failed 0 empty 0`, `section O: checks 32
   failed 0`. The four negative controls, each applied alone and reverted, failed **exactly** the partitions the TZ
   predicted: control 1 → `failed 1`; control 2 → `failed 2`; control 3 → `failed 1`; control 4 → `failed 1`; no
   control produced a failure outside section O, and after each revert `vps/run.py` read B2's digest again.
2. **The program.** `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`, **238767288 bytes**, version
   **`2.1.282`**. `ANTHROPIC_DEFAULT_SONNET_MODEL` occurs **14** times in its bytes and
   `ANTHROPIC_DEFAULT_OPUS_MODEL` **19** times — neither count is `0`. Its model-id list carries both ids the pins
   name, `claude-opus-5-5` (45) and `claude-sonnet-5` (61); the full list is in Validation, A2.
3. **The ids the runs used.** Four invocations since 09.10.2026, each `claude_exit=0`, each with the same three ids:
   `claude-haiku-4-5-20251001,claude-opus-5-5,claude-sonnet-5`. **One id in each is neither `claude-opus-5-5` nor
   `claude-sonnet-5`: `claude-haiku-4-5-20251001`** — a model the CLI used beside the two pinned ones in every run.
4. **The tree.** `git rev-parse origin/main:vps` → `8b2b6d8c5106eb1cada9c9437780cc59b5a1385a`;
   `/var/lib/crypto-auto/deployed-vps-tree` → `8b2b6d8c5106eb1cada9c9437780cc59b5a1385a`. Both the known answer.

The hosted gate read: Bench gate run **`39326987633`** on headSha `17b17951f3bc49f09edc306a9cac005c9ccfeb36` —
the implementation commit — event `pull_request`, status `completed`, conclusion **`success`**, 23 of 23 job steps
`success`.

---

## Inbound Filing

Nothing was moved and nothing was renamed. The TZ arrived at its own canonical path,
`CryptoTZ/TZ-66-run-subagent-model-pin.md`, on `origin/main` in commit `93a3d3b` ("Add files via upload"), 474
lines. No copy landed in the repository root and no filename was mangled, so §3's `git mv` clause had no referent.
No credential arrived under the trigger line, and the TZ names none (its §1).

The previous TZ's branch was merged: `git merge-base --is-ancestor 373a6cf origin/main` → exit 0 (pull request #53,
TZ-64 and TZ-65 together). `git rev-parse --is-shallow-repository` → `false`.

---

## Scope Executed

**Class: branch TZ** (contract §8) — the scope names `vps/run.py` and `vps/selftest.py`, both outside
`CryptoReports/**`. Host: the VPS. A0 passed (below) before the gate and before any other work.

Executed: Stage A (A0, A1.1–A1.3, A2, A3, all read-only), Stage B (B1–B4), V1–V6. The session ran inside a git
worktree of the repository; `git checkout -b tz-66-run-subagent-model-pin origin/main` (B1) was run in it. No model
session was opened, the `claude` binary was never executed, and no credential was read or written.

---

## Files Created

None.

## Files Modified

- `vps/run.py` — 351 → 360 lines.
- `vps/selftest.py` — 1807 → 1830 lines.

Both stay mode `100644` (`git ls-tree` on the pushed branch; `git diff --summary origin/main` printed no mode line).

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

§11's patch, applied byte for byte and nothing beside it:

- `vps/run.py`: `HUNTER_MODEL = "claude-sonnet-5"` and `PINS`, mapping `ANTHROPIC_DEFAULT_OPUS_MODEL` to `MODEL` and
  `ANTHROPIC_DEFAULT_SONNET_MODEL` to `HUNTER_MODEL`. `claude_env` calls `env.update(PINS)` on the copy
  `writer_env()` returns, so the pins sit over any value the unit's environment carries, in the claude child's
  environment alone. The journal's second summary line gains `unpinned=` after `models=`: every id of
  `modelUsage` outside `PINS.values()`, comma-separated, or `-`.
- `vps/selftest.py`: the stub claude records the two pin variables it sees and returns a configurable `modelUsage`;
  section O gains five checks (27 → 32), the total 432 → 437.
- `run.PROMPT`, `run.APPEND`, `run.CLAUDE`, `run.MODEL` and `run.EFFORT` do not move (V3).

Nothing is installed by this session: the deployer installs after the merge, behind the selftest (contract §7
item 15).

---

## Validation

All times UTC; A0 ran at 2026-10-19 21:20:40.

**A0 — the host.** `hostname` → `vultr`. `systemctl is-active crypto-bot.service crypto-exchange.service` →
`active`, `active`. `test -d /srv/crypto-auto/.git && echo clone` → `clone`. `id -u cryptorun` → `995`. All four are
the known answers.

**A1 — contract §4a steps 1–6 and the §5 gate.** Gate result in Fingerprints below: revision string present, 7 of 7
anchors matched, the TZ's anchor table identical to the map's, every file at its stated line count and MD5, the
contract at `**Version 30.**`.

- **A1.1** — both values `8b2b6d8c5106eb1cada9c9437780cc59b5a1385a` (Status item 4).
- **A1.2** — before any edit, `systemctl show crypto-run.service -p ActiveState -p NRestarts` →
  `NRestarts=0`, `ActiveState=inactive`; `systemctl list-unit-files 'crypto-*' --no-pager` → 12 unit files:
  `crypto-run.path`, `crypto-stop.path`, `crypto-announce.service`, `crypto-bot.service`, `crypto-exchange.service`,
  `crypto-paper.service`, `crypto-cleanup.timer`, `crypto-deploy.timer` — `enabled`; `crypto-cleanup.service`,
  `crypto-deploy.service`, `crypto-run.service`, `crypto-stop.service` — `static`.
- **A1.3** — `python3 vps/selftest.py` on the unmodified tree: exit 0, `selftest: sections 23 checks 432 failed 0
  empty 0`, `section O: checks 27 failed 0` — the known answer. Python `3.12.3`.

**A2 — the program the run unit starts**, read with `readlink`, `ls`, `grep -a` and `python3` reading its package
file; never executed (the only program run under the unit's `PATH` was `sh -c 'command -v claude'`).

```
/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
-rwxr-xr-x 2 root root 238767288 Sep 24 21:21 /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
2.1.282
ANTHROPIC_DEFAULT_SONNET_MODEL 14
ANTHROPIC_DEFAULT_OPUS_MODEL 19
```

`grep -a -o -E 'claude-(opus|sonnet|haiku)-[0-9]+(-[0-9]+)*' "$p" | sort | uniq -c`:

```
      1 claude-haiku-3-5
      1 claude-haiku-3-55
     31 claude-haiku-4-5
     18 claude-haiku-4-5-20251001
     11 claude-opus-4
     25 claude-opus-4-0
     32 claude-opus-4-1
     15 claude-opus-4-1-20250805
     13 claude-opus-4-20250514
     24 claude-opus-4-5
      8 claude-opus-4-5-20251101
     54 claude-opus-4-6
     48 claude-opus-4-7
     63 claude-opus-4-8
     77 claude-opus-5
     45 claude-opus-5-5
      2 claude-sonnet-3-7
      8 claude-sonnet-4
     21 claude-sonnet-4-0
      8 claude-sonnet-4-20250514
     43 claude-sonnet-4-5
     10 claude-sonnet-4-5-20250929
     61 claude-sonnet-4-6
     61 claude-sonnet-5
```

Compared, never required: the path and the size equal what TZ-63's C1 read on 09.10.2026 (the same path,
238767288 bytes), and the version equals TZ-58's reading of 03.10.2026 (`2.1.282`). **What the counts establish and
what they do not:** the two variable names occur in the program's bytes, so the case the TZ names as a finding —
a count of `0` — did not arise. The counts do not show that the program reads them for the Agent tool's `sonnet` and
`opus` aliases as the documentation says; no model session was opened here, and the first press after the merge
measures it (TZ §5).

**A3 — every id the runs used since TZ-63's install**, `journalctl -u crypto-run.service --since '2026-10-09
00:00:00 UTC' -o short-iso-precise --no-pager | grep -E 'crypto-run: (requests|models)='`, verbatim:

```
2026-10-09T13:16:06.890927+00:00 vultr python3[584455]: crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=0 is_error=false num_turns=38 duration_ms=275738 denials=0 answer_chars=1068
2026-10-09T13:16:06.891420+00:00 vultr python3[584455]: crypto-run: models=claude-haiku-4-5-20251001,claude-opus-5-5,claude-sonnet-5 denied_tools=- subtype=success api_error_status=- terminal_reason=completed stop_reason=end_turn
2026-10-10T14:45:14.292125+00:00 vultr python3[716778]: crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=0 is_error=false num_turns=56 duration_ms=2149593 denials=0 answer_chars=5736
2026-10-10T14:45:14.292940+00:00 vultr python3[716778]: crypto-run: models=claude-haiku-4-5-20251001,claude-opus-5-5,claude-sonnet-5 denied_tools=- subtype=success api_error_status=- terminal_reason=completed stop_reason=end_turn
2026-10-15T15:16:41.489447+00:00 vultr python3[1354635]: crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=0 is_error=false num_turns=43 duration_ms=2232337 denials=0 answer_chars=2285
2026-10-15T15:16:41.490200+00:00 vultr python3[1354635]: crypto-run: models=claude-haiku-4-5-20251001,claude-opus-5-5,claude-sonnet-5 denied_tools=- subtype=success api_error_status=- terminal_reason=completed stop_reason=end_turn
2026-10-19T14:34:05.006594+00:00 vultr python3[1869607]: crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=0 is_error=false num_turns=46 duration_ms=1728054 denials=0 answer_chars=3279
2026-10-19T14:34:05.007357+00:00 vultr python3[1869607]: crypto-run: models=claude-haiku-4-5-20251001,claude-opus-5-5,claude-sonnet-5 denied_tools=- subtype=success api_error_status=- terminal_reason=completed stop_reason=end_turn
```

| Invocation (journal time) | `claude_exit` | Ids | Neither `claude-opus-5-5` nor `claude-sonnet-5` |
|---|---:|---|---|
| 2026-10-09T13:16:06Z | 0 | `claude-haiku-4-5-20251001`, `claude-opus-5-5`, `claude-sonnet-5` | `claude-haiku-4-5-20251001` |
| 2026-10-10T14:45:14Z | 0 | the same three | `claude-haiku-4-5-20251001` |
| 2026-10-15T15:16:41Z | 0 | the same three | `claude-haiku-4-5-20251001` |
| 2026-10-19T14:34:05Z | 0 | the same three | `claude-haiku-4-5-20251001` |

**B1–B4.** `git checkout -b tz-66-run-subagent-model-pin origin/main` → new branch. Patch: `c5cc1d197d912fd61e55d364e7628a25`,
132 lines. `git apply --check` exit 0 and `git apply` exit 0. B2: `vps/run.py` 360 / `07f672e5bcea06be27508db66aa3a8e0`;
`vps/selftest.py` 1830 / `ce6220cdf2a45709bd1f09596e209ee9`. B3: `git diff --summary origin/main` printed nothing.
B4: `rm -r /root/tz66` → `ls /root/tz66` → `No such file or directory`.

**V1 — selftest, and the negative controls (inv. 68).** `python3 vps/selftest.py` on the branch: exit 0,
`selftest: sections 23 checks 437 failed 0 empty 0`, `section O: checks 32 failed 0`, zero `FAIL` lines. Each control
was one exact-string edit of `vps/run.py` (the script asserted exactly one occurrence of the old text before
writing), run alone, then `vps/run.py` restored and its digest re-read:

| # | Edit | Exit | Total line | Failing checks (stderr `FAIL` lines) |
|---|---|---:|---|---|
| 1 | delete `    env.update(PINS)` | 1 | `checks 437 failed 1 empty 0` | `FAIL section O: the stub claude sees every pin of run.PINS, not the unit's own values` |
| 2 | `HUNTER_MODEL = "claude-sonnet-5"` → `"sonnet"` | 1 | `checks 437 failed 2 empty 0` | `FAIL section O: run.PINS resolves sonnet to claude-sonnet-5`; `FAIL section O: the second summary line names every id used, then the one outside run.PINS` |
| 3 | `m not in PINS.values()` → `m not in PINS` in the `unpinned` line | 1 | `checks 437 failed 1 empty 0` | `FAIL section O: the second summary line names every id used, then the one outside run.PINS` |
| 4 | `env = writer_env()` + `env.update(PINS)` → `os.environ.update(PINS)` + `env = writer_env()` | 1 | `checks 437 failed 1 empty 0` | `FAIL section O: run.py put no pin into its own environment` |

After the fourth restore: `vps/run.py` 360 lines, `07f672e5bcea06be27508db66aa3a8e0`, and `python3 vps/selftest.py`
again exit 0, `checks 437 failed 0 empty 0`, `section O: checks 32 failed 0`. Each control's failed count equals the
number of `FAIL` lines it printed, so every other check of all twenty-three sections stayed green in each.

**V2.** `python3 -m py_compile vps/run.py vps/selftest.py` → exit 0.

**V3.** Output of the TZ's command: `{'ANTHROPIC_DEFAULT_OPUS_MODEL': 'claude-opus-5-5', 'ANTHROPIC_DEFAULT_SONNET_MODEL': 'claude-sonnet-5'}`
and `True` — the known answer; `run.CLAUDE` equals the TZ-59 list.

**V4.** `git diff --name-only origin/main...HEAD` → `vps/run.py`, `vps/selftest.py`, and nothing else.

**V5.** After B, `systemctl show crypto-run.service -p ActiveState -p NRestarts` and `systemctl list-unit-files
'crypto-*' --no-pager` each `diff` empty against A1.2's captures.

**V6.** The branch was pushed and pull request #54 opened (below). No regression: section O's 27 earlier checks and
sections S and U stayed green inside the 437.

---

## Test Results

| Run | Command | Result |
|---|---|---|
| Baseline, `origin/main` | `python3 vps/selftest.py` | exit 0, `sections 23 checks 432 failed 0 empty 0`, section O 27 |
| Branch | `python3 vps/selftest.py` | exit 0, `sections 23 checks 437 failed 0 empty 0`, section O 32 |
| Control 1 | as V1 | exit 1, `failed 1 empty 0` |
| Control 2 | as V1 | exit 1, `failed 2 empty 0` |
| Control 3 | as V1 | exit 1, `failed 1 empty 0` |
| Control 4 | as V1 | exit 1, `failed 1 empty 0` |
| Branch, after reverts | `python3 vps/selftest.py` | exit 0, `sections 23 checks 437 failed 0 empty 0`, section O 32 |

Section O's five new checks are the increase from 27 to 32 and from 432 to 437. A check count is a count of
comparisons the selftest made, not an estimate (inv. 43).

---

## Deviations

1. **Scratch location.** The TZ authorises one directory outside the repository for scratch, `/root/tz66`, and
   "nothing else" (its §4). `/root/tz66` held the patch and was removed in B4. The session environment also
   designates a per-session scratchpad directory, and this session wrote its own working files there — captures of
   A1.2 and V5 command output, the A1.3 and V1 selftest output, the anchor-table cuts of the fingerprint gate, a copy
   of the patched `vps/run.py`, and the script that applied the four negative-control edits. None holds a credential,
   none is in the repository, none is under a path the TZ names as forbidden (`/etc/crypto-auto/`, `/etc/systemd/`,
   `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto`, `/var/spool/crypto-auto`). They were removed
   before this report was written. Reported so that the Architect decides whether the TZ's clause is meant to cover
   the harness's own scratchpad.

No other deviation. The commit message is the TZ's string verbatim.

## Pre-existing Issues

1. **`claude-haiku-4-5-20251001` is used in every run and is outside the pins.** It appears in `models=` of all four
   invocations since 09.10.2026 (A3), so it predates this change. The pins name `sonnet` and `opus`; this id is
   neither, and TZ §5 leaves it unpinned: after the merge each run's second summary line names it in `unpinned=`.
   Which model it is for is not established by this session. The map decides on A3's reading (TZ §5).

No other pre-existing defect found. The fingerprint gate and every file measurement matched, so there is no map
lag to report.

## Remaining Risks

1. **The pins' effect is unmeasured.** No model session was opened (TZ §1), and A2 establishes only that both
   variable names occur in the program's bytes (14 and 19 times). Whether the hunter's `sonnet` and the sheriff's
   session model now resolve to the pinned ids inside a run is read from the first press after the merge: its
   journal's `unpinned=` and the day log's model lines (TZ §5). The selftest proves the child's environment carries
   the pins against a stub, not what the real CLI does with them.
2. **The pins name two literal ids.** Moving either to another model is now a change of `vps/run.py` and therefore
   a TZ, which is the purpose of TZ-66 (its §3). What a run does if the API stops serving a pinned id is not
   addressed by this TZ and was not measured.
3. **`unpinned=` will never be `-` while the CLI uses `claude-haiku-4-5-20251001` as a helper** (Pre-existing Issue 1),
   so the field names a known id on every run until the map decides on it; a reader looking for a change reads the
   ids beside it.

---

## Commit

Implementation, on the branch `tz-66-run-subagent-model-pin`, pushed — `17b17951f3bc49f09edc306a9cac005c9ccfeb36`,
one commit on top of `93a3d3b`, touching `vps/run.py` and `vps/selftest.py` (2 files changed, 42 insertions, 10
deletions):

```
TZ-66: vps — the hunter and the sheriff on pinned model ids: the session's environment resolves sonnet and opus to full ids, and the journal names every id outside them
```

Report, on `main`, the message this session is authorised to carry:

```
TZ-66: report — the hunter and the sheriff on pinned model ids
```

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/54 — base `main`, head `tz-66-run-subagent-model-pin`, state
`OPEN`, `mergeable` `MERGEABLE` when read. The Architect's verdict precedes the merge (contract §8).

## CI Execution

`gh run list --branch tz-66-run-subagent-model-pin` returned exactly one run: **Bench gate**, id **`39326987633`**,
event `pull_request`, headSha `17b17951f3bc49f09edc306a9cac005c9ccfeb36`, status `completed`, conclusion **`success`**;
`gh run view` lists one job, `bench`, `completed` / `success`, 23 of 23 steps `success`.

No other workflow has a run on the branch. Read from the files: `bench.yml` triggers on `push` to `main` and
`claude/**` and on `pull_request`, so this branch name was covered by `pull_request` only; `main.yml` triggers on
`push` to `main` with the two literal paths `main.py` and `.github/workflows/main.yml`, and on `workflow_dispatch`;
`calib.yml` on `push` to `claude/**` with two paths, and on `workflow_dispatch`; `journal.yml` on a daily cron and
`workflow_dispatch`; `backtest_bench.yml` on `workflow_dispatch`. No workflow names `vps/selftest.py`
(`grep -rn -E 'vps/selftest|selftest\.py' .github/workflows/` → no match), so none of the gate's 23 steps is this TZ's
selftest: every selftest figure in this report is the VPS's own local run, not a runner run.

Before the first direct push to `main`, §8's two facts were read: `main.yml`'s `on.push` is a `paths` allow-list of
two literal paths with no `paths-ignore` key (the one occurrence of the string is inside a comment, line 25), and
`bench.yml`'s `paths-ignore` carries `**.md`.

## Final Repository State

The branch `tz-66-run-subagent-model-pin`, pushed before this report was written: head
`17b17951f3bc49f09edc306a9cac005c9ccfeb36` on `origin`, one commit above `93a3d3b65e272e49d9d417c6d3173be1d616828e`,
the commit the fingerprints were taken against. `git diff --stat origin/main origin/tz-66-run-subagent-model-pin` →
`2 files changed, 42 insertions(+), 10 deletions(-)`; both files `100644`. The scratch directory `/root/tz66` is
gone, no unit was started, stopped, restarted, enabled or disabled (V5), and no run was started or requested.
`vps/__pycache__/`, which the selftest and `py_compile` runs generated and `.gitignore` excludes, was removed.

**NOT IN EFFECT UNTIL MERGED.** Merge is deployment on the VPS (contract §7 item 15): the deployer installs the
change after the merge, and until then the run unit runs the files of `8b2b6d8c5106eb1cada9c9437780cc59b5a1385a`.

---

## Fingerprints

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — **2788** lines, MD5 `5be2e6e013a7288b8ed03a7593ab8970`; revision string
`**Revision 2026-10-19-b.**` (the TZ requires the same). Reported, not enforced; equal to the TZ's figure.

**Anchors (contract §5 step 2).** The anchor table was cut by structure — every row between the separator line under
`| Anchor | Exact string that must be present |` and the first line that is not a table row — from both the map and the
TZ's `§0`, with `awk`; `diff` of the two cuts printed nothing (identical rows). **Table's own row count: 7. Compared:
7. Matched: 7.** Each anchor was then matched with `grep -n -o -F -m1 -- "<anchor>" SYSTEM-MAP-CRYPTOCALCUL.md`, which
prints the matched text itself:

| Anchor | Text the first match returned | Every line carrying the string |
|---|---|---|
| revision | `17:**Revision 2026-10-19-b.**` | 17, 75 |
| direction engine | `76:### 3.12 Direction engine — veto cascade` | 76, 1045 |
| catalyst registry | `77:### 3.15 Catalyst registry` | 77, 1435 |
| exhaustion measure | `78:### 3.16 List exhaustion — the day-range measure` | 78, 1532 |
| analytical engine | `79:## 11. Analytical engine` | 79, 2520 |
| squeeze block | `80:### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 80, 1699 |
| newest invariant | `81:72. **A write that fails leaves this run's product or nothing` | 81, 2241 |

(`grep -n -F -- "<anchor>"` without `-m1`. The revision string's first line is the revision paragraph, 17, and its
table row is 75; for the other six, the first line is the anchor table's own row, 76–81, and the second is the
heading or list item the anchor names.)

**Files the map's `## 0` table lists**, measured on the checkout at `93a3d3b`:

| File | Lines | MD5 | Stated |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**Files the TZ's gate adds**, same checkout:

| File | Lines | MD5 | Stated |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | equal; version line `**Version 30.**` present |
| `vps/run.py` | 351 | `41161832221abd8a6d4f026c6b7b21d8` | equal |
| `vps/selftest.py` | 1807 | `04d484d41ac49a466ec60c0df3c17dda` | equal |

**The two files this TZ changes, on the branch** (B2): `vps/run.py` 360 / `07f672e5bcea06be27508db66aa3a8e0`;
`vps/selftest.py` 1830 / `ce6220cdf2a45709bd1f09596e209ee9`.

**The tree:** `git rev-parse origin/main:vps` and `/var/lib/crypto-auto/deployed-vps-tree` both
`8b2b6d8c5106eb1cada9c9437780cc59b5a1385a`, the tree the TZ was written against.
