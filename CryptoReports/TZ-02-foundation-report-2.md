# Implementation Report — TZ-02

Second report for TZ-02, written under the re-trigger of 2026-08-20 22:00Z.
`CryptoReports/TZ-02-foundation-report.md` is the record of the first execution and
is immutable; this file records what the re-trigger found, changed and verified, and
does not restate the first report. Where the two disagree, this file is later and
supersedes on that point only.

## Status

**COMPLETED**, with one validation item reported rather than fully verified (item 7 —
the Gist side of the check is unreachable from this session's network policy) and one
item satisfied in substance but not in letter (item 2 — the contract in the repository
is Version 4, not the Version 2 the TZ names). Both are itemised under `## Deviations`.

The re-trigger found TZ-02 already largely implemented on the branch by the first
execution, and found one regression introduced afterwards by a web upload. That
regression is the substantive change in this run.

## Inbound Filing

`git fetch --all --prune` was run before any assessment, per `EXECUTOR-INSTRUCTIONS.md`
§4.2. It moved `origin/main` from `fe24061` to `e05e20f`. A later fetch, forced by a
rejected push, moved `origin/claude/new-session-113so9` from `30dfd85` to `1e15cc8`.

| Artifact | Found as | Filed as | Action |
|---|---|---|---|
| System Map | `SYSTEM MAP CRYPTOCALCUL.md` (branch tip, space in name) | `SYSTEM-MAP-CRYPTOCALCUL.md` | `git mv`, this run |
| TZ-02 | `CryptoTZ/TZ-02-foundation.md` | unchanged | already filed by the first execution |
| Executor contract | `EXECUTOR-INSTRUCTIONS.md` (Version 4, repository) | unchanged | kept; see Deviations |

Two artifacts were attached to this session — an Executor contract (Version 2) and
TZ-02. Neither was installed:

- The **TZ-02 attachment** is byte-identical to `CryptoTZ/TZ-02-foundation.md` already
  in the repository (`fee0638b8054901260f8336290ac604b` both sides). Nothing to file.
- The **contract attachment** is Version 2, 298 lines, `82b8da93688529e5581ecf9a050dc232`.
  The repository holds Version 4, 378 lines, `3ac729fa2f35dd8ab483eb4c41695915`, uploaded
  by the Boss at `21c3514`. §3 resolves duplicates by **content, not provenance**, and
  Version 4 states in its own §3 that the contract is read from the repository and is
  never attached to a session. Installing the attachment would have been a two-version
  regression. Version 4 was kept and this report follows Version 4's rules.

## Scope Executed

| Scope | State on arrival | Action this run |
|---|---|---|
| A — land TZ-01 on `main` | done by first execution (`e5e755e`, `384deba`) | verified, not redone |
| B — canonical filenames, contract | **regressed** — map renamed back to a spaced name | `git mv` restored; contract left at V4 |
| C — `CryptoTZ/`, `CryptoReports/` | done | verified |
| D — hourly schedule | done | verified; forensics extended, see below |
| E — `.gitignore` | done | verified, including a live firing test |
| F — TZ-01 record archived | done | verified present, 290 lines |

## Files Created

- `CryptoReports/TZ-02-foundation-report-2.md` — this file.

## Files Modified

None. No file's content was changed by this run.

## Files Renamed

- `SYSTEM MAP CRYPTOCALCUL.md` → `SYSTEM-MAP-CRYPTOCALCUL.md` (`git mv`, content untouched)

## Files Deleted

**None.** `git diff --name-status -M --diff-filter=D` over this run's commit returns
nothing. `image.PNG` remains tracked and `index.html` line 8 still references it.

## Implementation Summary

### The regression this run fixes

The branch's first execution renamed the map to `SYSTEM-MAP-CRYPTOCALCUL.md`. Three
later web uploads to the branch undid it:

```
0ea38d8  Delete SYSTEM-MAP-CRYPTOCALCUL.md
21c3514  Add files via upload      -> re-added as "SYSTEM MAP CRYPTOCALCUL.md"
1e15cc8  Merge origin/main ..., keeping branch state
```

This is the transit-corruption defect TZ-02 §B.3 describes: the Architect's
presentation layer renders a separator as a space and the file is saved under the
displayed name. It put a space back into a tracked path, breaking scope B.1 and
validation item 3. `git mv` restored the canonical name; the content was already
correct and was not touched.

### Schedule forensics (D.4) — extended

The first execution established, correctly, that **no revision of
`.github/workflows/main.yml` has ever contained a `schedule` or `cron` key**, and that
no workflow in this repository's history ever has:

```
$ git log --follow --oneline --all -- .github/workflows/main.yml
30dfd85 chore(repo): canonical system map filename, scoped bot push trigger, bench CI gate
849d8fc Update index.html          <- file created here, 2026-06-16
=> NO revision of .github/workflows/main.yml has ever contained a schedule/cron trigger.
```

This run adds the other half of the answer, which changes what the finding means.
Listing the workflow's run history shows the hourly cadence **does exist today** and is
supplied from outside the repository — an agent calling the `workflow_dispatch` API on
the hour at **:50**:

```
run 1288  2026-08-20T07:50:02Z  workflow_dispatch  success
run 1290  2026-08-20T08:50:03Z  workflow_dispatch  success
run 1295  2026-08-20T09:50:04Z  workflow_dispatch  success
run 1296  2026-08-20T10:50:03Z  workflow_dispatch  success
run 1297  2026-08-20T11:50:03Z  workflow_dispatch  success
run 1299  2026-08-20T12:50:05Z  workflow_dispatch  success
run 1300  2026-08-20T13:50:03Z  workflow_dispatch  success
run 1304  2026-08-20T14:50:03Z  workflow_dispatch  success
run 1305  2026-08-20T15:50:04Z  workflow_dispatch  success
run 1306  2026-08-20T16:50:03Z  workflow_dispatch  success
run 1307  2026-08-20T17:50:02Z  workflow_dispatch  success
          << 18:50 MISSING >>
run 1308  2026-08-20T19:50:06Z  workflow_dispatch  success
run 1316  2026-08-20T20:50:04Z  workflow_dispatch  success
run 1317  2026-08-20T21:50:04Z  workflow_dispatch  success
```

So map §1's "cron ~1 раз/час" was never a documentation error and never a silent
regression in this file — it describes a real cadence delivered by a mechanism that
lives outside the repository and is invisible to it. The 18:50 gap is the point: that
mechanism is unmonitored and has already missed an hour, and a missed hour is exactly
what `STALE_WARN_MIN 75` is calibrated to catch. Restoring the in-workflow cron gives
the cadence a home the repository can see and version.

**This creates a duplication the Architect must rule on.** The new cron fires at `:00`
and the external agent fires at `:50`, so after merge `coeffs.json` refreshes twice an
hour, ten minutes apart. At 30 CoinGecko calls per run that is ~60 calls/hour and
~43k/month against the keyless allowance the map §5 relies on. Recorded under
`## Remaining Risks`; not acted on, per §6.

## Validation

Every item TZ-02 lists, run in full. Commands and outputs are reproduced.

### 1. Exactly one System Map, canonical name, fingerprint anchors — PASS

```
tracked: SYSTEM-MAP-CRYPTOCALCUL.md          (the only match for "system" in git ls-files)
lines: 1461
md5:   9590fd08d149fb05d4db0d0179b54a50
anchor '### 3.12 Direction engine — veto cascade (19.08.2026)': 1
invariant 36 under '## 4. Инварианты — НЕ ЛОМАТЬ':            1
newest migration entry: 2026-08-20
```

MD5 is an exact match for the value named in the TZ header. Line count 1461 matches
the expected ≈1461.

### 2. Exactly one Executor contract — PASS on count, DEVIATION on version

```
tracked: EXECUTOR-INSTRUCTIONS.md   (only match)
lines: 378
md5:   3ac729fa2f35dd8ab483eb4c41695915
header: **Version 4.** Permanent operating contract for the Claude Code Executor.
```

One copy, canonical name, no spaces. The TZ asks for Version 2; the repository holds
Version 4, which post-dates the TZ. See `## Deviations`.

### 3. No tracked filename contains a space — PASS

```
$ git ls-files | grep " "
(no output)
```

This is the item the re-trigger actually repaired.

### 4. Canonical artifacts present and well-formed — PASS

```
CryptoTZ/TZ-02-foundation.md                   present (260 lines)
CryptoReports/TZ-01-repo-hardening-report.md   present (290 lines)
CryptoReports/TZ-02-foundation-report.md       present (694 lines)
```

The TZ-01 report carries all sixteen §10 headings.

### 5. `bench.yml` byte-identical to its state at `30dfd85` — PASS

```
now      : c2dc4556fb1688a344372005b73b7be1
@30dfd85 : c2dc4556fb1688a344372005b73b7be1
```

### 6. `main.yml` parses, exactly three triggers, steps untouched — PASS

Parsed with **PyYAML 6.0.1**:

```
triggers: ['push', 'schedule', 'workflow_dispatch'] count = 3
schedule: [{'cron': '0 * * * *'}]
push.paths-ignore:
  - bench/**
  - **/*.md
  - index.html
  - .github/workflows/bench.yml
  - .github/workflows/backtest_bench.yml
workflow_dispatch key present: True
paths-ignore is a key of push only: True  /  present on schedule entry: False
```

`paths-ignore` is structurally a key of the `push` mapping and cannot gate `schedule`
— confirmed as TZ-02 D.3 requires.

Job and steps section, hashed from `^jobs:` to end of file:

```
steps section md5 now      : 147f78e86aefeebabab1d914812fb5de
steps section md5 @30dfd85 : 147f78e86aefeebabab1d914812fb5de
```

Byte-identical. No env, secret, permission or step was touched.

### 7. Manual `workflow_dispatch`, fresh `generated_at` — PARTIAL

Run dispatched against this branch: **run 1318, id 32424369197**, `event:
workflow_dispatch`, `head_sha 42cc31f`.

```
created         2026-08-20T22:27:56Z
job started     2026-08-20T22:27:59Z
job completed   2026-08-20T22:35:58Z
conclusion      success        (all 8 steps success, run_attempt 1)

step 5 "Run script with fail-safe logic"
  22:28:14 -> 22:35:56   success   (7m42s)
```

GitHub accepted the dispatch against the edited `main.yml`, which independently proves
the file with the new `schedule` block parses server-side, not only under PyYAML.

**The bot ran once and cleanly.** The step is wrapped in
`python main.py || (echo "First attempt failed, retrying in 60s..." && sleep 60 && python main.py)`.
The full job log contains no `First attempt failed` line, so the retry never fired.
7m42s also matches the healthy hourly runs (run 1317: `21:50:04 -> 21:57:10`), so this
was a normal full pass, not a rate-limited one. **This is the distinction TZ-02 item 7
asks to preserve, and it resolves to "not a rate limit."**

**The Gist half of this item could not be verified from this session.** The
environment's network policy denies the host:

```
$ curl -sS https://gist.githubusercontent.com/.../coeffs.json
curl: (56) CONNECT tunnel failed, response 403

$ curl -sS "$HTTPS_PROXY/__agentproxy/status"
  "recentRelayFailures": [{ "kind": "connect_rejected",
    "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
    "host": "gist.githubusercontent.com:443" }]
```

A policy denial, not a broken tool and not a bot failure. Per §9 the item is recorded
as **not fully verified** rather than "not applicable"; the `generated_at` values before
and after are unknown to this session and should be read from the board or the Gist by
someone who can reach it.

**A green run is not by itself proof of a Gist write**, and that must be said plainly,
because `main.py` cannot report a write failure through its exit code — see
`## Pre-existing Issues` item 4. The evidence that the write happened is therefore
indirect, but it is strong and it is stated as indirect:

- every print statement in `main.py` is on an error path — `Ошибка Gist:` for a
  non-`ok` PATCH response, `Критическая ошибка:` for any exception,
  `Пустой или некорректный ответ CoinGecko` for a bad fetch;
- the job log between 22:28:14 and 22:35:56 contains **none of them**, and no output
  from the script at all;
- the elapsed time matches a full 30-call CoinGecko pass.

Silence from a script whose only output is failure, for exactly the duration of a
healthy pass, is good evidence the PATCH succeeded. It is not the timestamp comparison
the TZ asked for, and it is not recorded as one.

### 8. The five gated benches run green — PASS

```
verify_board.js                                        exit=0  --- checks: 108  fails: 0 ---
board2_bench.js                                        exit=0  --- checks: 129  fails: 0 ---
prot_bench.js index.html                               exit=0  PASS 167   FAIL 0
verify_bench.py                                        exit=0  checks run: 35   FAIL 0
direction_bench.py --props --fixtures --control --sim   exit=0  ИТОГО проверок: 489786 | провалов блоков: 0
```

Total 490 225 checks, 0 failures, every exit code 0.

### 9. Standing checks; `index.html` and `main.py` unmodified — PASS

```
py_compile main.py:      PASS
node --check <script>:   PASS
index.html now / @30dfd85 : 20a12f527e6b78a7a661791bbbd89261 / 20a12f527e6b78a7a661791bbbd89261
main.py    now / @30dfd85 : 064c9dba8313141d1d267316b2da7a39 / 064c9dba8313141d1d267316b2da7a39
```

### 10. `.gitignore` ignores nothing tracked — PASS

```
$ git ls-files --ignored --exclude-standard -c
(no output — no tracked file matches any rule)
```

Live firing test, with data rather than an assertion (invariant 22): eight files were
created, `git status --porcelain --ignored` was read, then they were removed.

```
??  index.html.prev        <- untracked, NOT ignored, as E.2 requires
??  orig.html              <- untracked, NOT ignored, as E.2 requires
!!  .DS_Store
!!  __pycache__/
!!  bench/_cases.json
!!  bench/_run.js
!!  bench/cache/
```

Both baselines TZ-03 will need stay visible; every generated artifact is caught.

### 11. No file deleted except those named under `Files to Delete` — PASS

This run's commit deletes nothing:

```
$ git status --short
R  "SYSTEM MAP CRYPTOCALCUL.md" -> SYSTEM-MAP-CRYPTOCALCUL.md
```

`EXECUTOR INSTRUCTIONS.md` (Version 1, space in filename), which TZ-02 lists for
deletion, had already been removed from `main` at `9a06078` before this task began. It
exists on no branch. Nothing was left to delete and nothing was deleted in its name.

## Test Results

### Gated benches — 490 225 checks, 0 failures

| Bench | Invocation | Checks | Failures | Exit |
|---|---|---|---|---|
| `verify_board.js` | `node bench/verify_board.js` | 108 | 0 | 0 |
| `board2_bench.js` | `node bench/board2_bench.js` | 129 | 0 | 0 |
| `prot_bench.js` | `node bench/prot_bench.js index.html` | 167 | 0 | 0 |
| `verify_bench.py` | `python3 bench/verify_bench.py` | 35 | 0 | 0 |
| `direction_bench.py` | `--props --fixtures --control --sim` | 489 786 | 0 | 0 |

### CI negative test — the gate is proven to fail

Required by §9 for any TZ touching CI. A local replay of `bench.yml`'s `run:` steps
under the workflow's own `bash -euo pipefail {0}` shell, with GitHub's fail-fast step
ordering. **This is a replay of workflow semantics, not a runner execution.**

```
=== BASELINE (clean tree) ===
  step exit=0 :: node bench/verify_board.js
  step exit=0 :: node bench/board2_bench.js
  step exit=0 :: node bench/prot_bench.js index.html
  step exit=0 :: python3 bench/verify_bench.py
  step exit=0 :: python3 bench/direction_bench.py --props --fixtures --control --sim
JOB RESULT: SUCCESS

=== INJECTED FAILURE (working tree only) ===
-eq('regime mode', regUp.mode, 'trend');
+eq('regime mode', regUp.mode, 'range');
  step exit=1 :: node bench/verify_board.js
JOB RESULT: FAILURE (step exited 1)

=== REVERTED ===
  bench/verify_board.js restored, identical to HEAD
JOB RESULT: SUCCESS
```

Green → red → green, and the working tree ends clean. No bench file was modified in
the delivered change set.

### Workflow dispatch — run 1318

`success`, run_attempt 1, all 8 steps green, `2026-08-20T22:27:59Z -> 22:35:58Z`. The
bot step took 7m42s with no retry and no error output. Full detail under Validation
item 7.

## Deviations

1. **The TZ's verbatim commit message was not reused.** TZ-02 supplies
   `chore(repo): land TZ-01, canonical artifact structure, restore hourly bot schedule`.
   The first execution already applied it verbatim at `384deba`. This run's commit
   repairs a regression that appeared afterwards, so reusing the same subject line
   would have put two different commits under one message. The commit subject is
   `chore(repo): restore canonical System Map filename after upload regression`.

2. **Validation item 2 asks for Version 2 of the contract; Version 4 was kept.** The
   TZ was authored before the Boss uploaded Version 4 at `21c3514`. §3 resolves
   duplicate artifacts by content, and Version 4 explicitly supersedes all earlier
   versions and forbids taking the contract from a session attachment. Downgrading to
   Version 2 to satisfy the letter of the item would have discarded two revisions of
   the operating contract. Reported rather than resolved unilaterally.

3. **This report is `-report-2.md`, not `-report.md`.** §10 makes reports immutable and
   directs a re-run to a `-2` file. `CryptoReports/TZ-02-foundation-report.md` was
   written by the first execution and is untouched.

4. **This report is committed to the branch, not directly to `main`.** Version 4 §8
   requires reports on `main` and explains why. This session operates under a standing
   instruction never to push to a branch other than the designated
   `claude/new-session-113so9` without explicit permission, and `main` is the branch
   GitHub Pages deploys. The two rules conflict; the conflict is escalated rather than
   resolved by an unauthorised push to production. **Action required from the Boss:**
   confirm the report may be pushed to `main` under `CryptoReports/`, or merge PR #1,
   which lands it either way.

5. **Validation item 7 is partial**, for the network-policy reason recorded under that
   item. The workflow half is verified; the Gist half is not readable from here.

6. **A concurrent writer touched the branch during execution.** The first push was
   rejected because `origin/claude/new-session-113so9` had advanced from `30dfd85` to
   `1e15cc8` mid-task. The local duplicate work was discarded in favour of the remote
   state after proving them content-equivalent file by file — `main.yml`, `.gitignore`,
   `bench.yml`, `CryptoTZ/TZ-02-foundation.md`, `index.html` and `main.py` all matched
   hash for hash. Nothing was force-pushed and no concurrent work was overwritten.

## Pre-existing Issues

Diagnosed, not fixed. None was caused by this task.

1. **Three benches are red against the current `index.html`.** Reserved for TZ-03 by
   TZ-02's own scope statement; untouched.

   | Bench | Result at HEAD |
   |---|---|
   | `display_bench.py` | 24 598 checks, **6 796 failures**, exit 1 |
   | `render_bench.py` | 123 scenarios, 12 795 checks, **1 565 failures**, exit 1 |
   | `direction_bench.py --display` | 57 661 checks, **1 block failure**, exit 1 |

   Root cause, single and shared. Production `tierOf` (`index.html` 1680–1685) returns
   `Фон` for the lowest tier, and `tierBadge` (1925–1934) emits
   `Слово #N — score`. The benches encode the pre-19.08 layout: `display_bench.py:156`
   expects the word `Наблюдать`, `display_bench.py:153` matches `>#(\d+) ` — rank
   immediately after a tag, i.e. rank *before* the tier word — and
   `render_bench.py:274` matches `^(?:#(\d+)\s+)?(\S+)\s+(\d+)`. The observed failure
   is literally `tierOf(34.99) = Фон, ждали Наблюдать`. These are **stale expectations,
   not a product defect**, and all three exit non-zero, so none violates invariant 29.

2. **Two benches cannot run at all — missing baselines.** `badge_bench.js` opens
   `index.html.prev` (`ENOENT`); `direction_bench.py --identity` opens `orig.html`
   (`FileNotFoundError`); `clean_bench.py` requires two positional HTML paths and
   raises `IndexError` without them. TZ-02 E.2 deliberately keeps both baseline names
   un-ignored so TZ-03 can restore them from history.

3. **`LATEST-REPORT.md` exists at the repository root** (32 341 bytes, added at
   `59084d0` under the Version 2 contract). Version 4 §8 now names this file
   specifically: *"Never create a second copy under a different name such as
   `LATEST-REPORT.md` — a duplicate is not a delivery mechanism, it is an artifact to
   clean up later."* It is a duplicate of a `CryptoReports/` report. Not deleted: TZ-02
   does not list it under `Files to Delete` and §6 forbids deleting what is not named.
   Flagged for the Architect to schedule.

4. **`main.py` cannot report a failure through its exit code** — invariants 25 and 29,
   the defect §9 says to report rather than work around. Two paths swallow errors:

   ```python
   if not r.ok:
       print(f"Ошибка Gist: {r.status_code} {r.text}")   # prints, does not raise
   except Exception as e:
       print(f"Критическая ошибка: {e}")                 # catches everything
   ```

   `main.py` therefore exits 0 whether or not `coeffs.json` was written. Consequences,
   both real: the workflow's `||` retry can never fire for a Gist failure, because the
   first attempt never reports one; and a green run in the Actions UI is not evidence
   the data refreshed. Every hourly `success` in the run history carries this caveat,
   not only run 1318. **Not fixed** — `main.py` is out of scope for TZ-02, and the
   file is byte-identical to its pre-task state. Offered as a candidate TZ: a non-zero
   exit on a failed PATCH would make the existing retry mean something.

5. **The workflow pins deprecated action versions.** `actions/checkout@v3` and
   `actions/setup-python@v4` target Node 20 and are being force-run on Node 24:
   `##[warning]Node.js 20 is deprecated.` Harmless today, breaks when the runner drops
   the shim. TZ-02 D.2 forbids touching any step, so this is reported only.

6. **`README.md` is a 0-byte tracked file.** Long-standing; harmless; noted only so it
   is not mistaken for damage from this run.

## Remaining Risks

1. **Double refresh after merge — the item most worth a decision.** The restored cron
   fires at `:00`; the external `workflow_dispatch` agent fires at `:50`. Both write the
   same live `coeffs.json`. After merge the bot runs twice an hour, ten minutes apart:
   ~60 keyless CoinGecko calls/hour, ~43k/month, against a budget map §1 sizes at
   ~21.6k/month for one run per hour. TZ-02 D.6 forbids adding an API key, so the
   resolution has to be retiring one of the two triggers — an Architect decision, not
   an Executor one. Until then, expect a raised rate-limit error rate.

2. **Scheduled workflows are suspended on inactive repositories.** Not currently a
   factor — all four workflows report `state: active` and the repository is active —
   but the YAML alone does not guarantee a live schedule, as TZ-02 D.7 notes. The first
   cron-triggered run should be confirmed after merge; until one appears with
   `event: schedule`, the hourly cadence is still coming only from the external agent.

3. **The transit-corruption defect will recur.** This run existed largely to repair one
   instance of it. Any future web upload of the map re-introduces a spaced filename and
   silently breaks validation item 3 again. Worth a permanent guard — a CI check that
   fails on any tracked path containing a space would cost one step in `bench.yml` — but
   that is out of scope here and is offered as a candidate TZ, not implemented.

4. **The branch has more than one writer.** Web uploads and at least one other agent
   push to `claude/new-session-113so9`. Anything verified here is verified as of
   `42cc31f`; a later upload can regress it exactly as `21c3514` did.

## Commit

```
42cc31f  chore(repo): restore canonical System Map filename after upload regression
```

Parent `1e15cc8`. One change: `R  "SYSTEM MAP CRYPTOCALCUL.md" -> SYSTEM-MAP-CRYPTOCALCUL.md`.
Pushed to `origin/claude/new-session-113so9`. The report commit follows.

Prior commits on this branch delivering TZ-02: `e5e755e` (merge of `origin/main`,
resolving the map collision), `384deba` (scopes B–E), `d87b36e` (TZ-01 and TZ-02
reports), `59084d0` (`LATEST-REPORT.md`, see Pre-existing Issues 3).

## Pull Request

**URL:** https://github.com/seahomebatumi-ai/crypto-auto/pull/1

`TZ-01 + TZ-02: land bench gate, canonical artifact structure, restore hourly bot
schedule` · state **open** · base `main` · head `claude/new-session-113so9` at
`42cc31f` · **not merged**.

The PR already existed, opened by the first execution at `2026-08-20T12:49:05Z`; a
second was not created. Awaiting the Architect's verdict.

**CI conclusion:** the repository runs no pull-request CI against this branch today —
`bench.yml`, which adds the `pull_request` trigger, is part of the change under review
and only starts gating once merged. The gate was therefore verified by local replay
(see `## Test Results`), and the bot workflow was exercised by dispatch (run 1318).

## Final Repository State

Branch `claude/new-session-113so9` at `42cc31f`, working tree clean, 25 tracked files,
none with a space in its name. `main` is unchanged by this run and still carries the
pre-TZ-01 state plus the Boss's uploads.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

| File | Lines | MD5 |
|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1461 | `9590fd08d149fb05d4db0d0179b54a50` |
| `index.html` | 3413 | `20a12f527e6b78a7a661791bbbd89261` |
| `main.py` | 485 | `064c9dba8313141d1d267316b2da7a39` |

`SYSTEM-MAP-CRYPTOCALCUL.md` — newest entry under `## 9. Журнал миграций`: **2026-08-20**.

Supporting hashes:

| File | MD5 | Note |
|---|---|---|
| `.github/workflows/bench.yml` | `c2dc4556fb1688a344372005b73b7be1` | identical at `30dfd85` |
| `main.yml` jobs/steps section | `147f78e86aefeebabab1d914812fb5de` | identical at `30dfd85` |
| `EXECUTOR-INSTRUCTIONS.md` | `3ac729fa2f35dd8ab483eb4c41695915` | Version 4, 378 lines |
| `CryptoTZ/TZ-02-foundation.md` | `fee0638b8054901260f8336290ac604b` | matches the session attachment |
