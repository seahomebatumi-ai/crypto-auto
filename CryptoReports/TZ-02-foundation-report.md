# Implementation Report — TZ-02

Executed 2026-08-20. Specification: `CryptoTZ/TZ-02-foundation.md`.

## Status

**PARTIAL** — scopes A, B, C, D, E and F are all completed. One validation item
(item 7, the Gist `generated_at` comparison) **could not be run** and is therefore
recorded as failed, per `EXECUTOR-INSTRUCTIONS.md` §9. No scope was blocked.

**The previous TZ's branch was not merged.** TZ-01's work sat on
`claude/new-session-113so9` at `30dfd85` while `main` advanced five commits. That is
the condition scope A exists to resolve, and it is stated here first as §8 requires.

## Inbound Filing

| Attached as | Filed as | Action |
|---|---|---|
| `0fc1993b-TZ02foundation.md` | `CryptoTZ/TZ-02-foundation.md` | `git mv` of the root copy `main` already carried, then content set to the attachment |
| `86b13784-EXECUTORINSTRUCTIONS.md` | `EXECUTOR-INSTRUCTIONS.md` | content of the existing root file replaced with the attachment |

Both artifacts already existed on `main`, uploaded through the GitHub web interface at
`e05e20f`. **In both cases the repository copy was an earlier revision than the session
attachment**, so the attachment won, per §3 ("Content must be byte-identical to the
attachment") and §3's rule that the correct content wins over the better-looking name.

| Artifact | Repository copy at `e05e20f` | Session attachment | Chosen |
|---|---|---|---|
| Executor contract | 287 lines, `c21904a9bc78795e15a8e952c343a872` | 298 lines, `82b8da93688529e5581ecf9a050dc232` | attachment |
| TZ-02 | 249 lines, `cc6ae2de4a2f4b43316ffcb110e35fae` | 260 lines, `fee0638b8054901260f8336290ac604b` | attachment |

The differences are substantive, not whitespace. The repository copy of the contract
still carried the superseded §3 ("The Boss uploads Architect artifacts to the
**repository root**"); the attachment carries the current §3 ("**TZ files arrive as
attachments in this Claude Code session**"). The repository copy of TZ-02 lacked the
`**Canonical filename:** CryptoTZ/TZ-02-foundation.md` header line and the
`git fetch --all --prune` instruction. Neither file contains CRLF; the byte difference
is real content.

Both surviving files are byte-identical to their attachments — verified with `cmp`.

## Scope Executed

| Scope | Description | Result |
|---|---|---|
| A | Land TZ-01 on `main` without losing the current System Map | Completed |
| B | Normalise artifact filenames; install Version 2 contract | Completed |
| C | Create `CryptoTZ/` and `CryptoReports/`; commit this TZ | Completed |
| D | Restore the hourly bot schedule | Completed |
| E | `.gitignore` for generated artifacts | Completed |
| F | Archive the TZ-01 implementation record | Completed |

## Files Created

| File | Lines | MD5 |
|---|---|---|
| `CryptoTZ/TZ-02-foundation.md` | 260 | `fee0638b8054901260f8336290ac604b` |
| `CryptoReports/TZ-01-repo-hardening-report.md` | — | see `## Commit` |
| `CryptoReports/TZ-02-foundation-report.md` | — | this file |
| `.gitignore` | 33 | `aa1aa7c4400033198175a1eaa02113eb` |

`.github/workflows/bench.yml` is not listed as created here — it was created by TZ-01
and is carried onto `main` by this branch, unmodified.

## Files Modified

| File | Change |
|---|---|
| `.github/workflows/main.yml` | trigger block only: `schedule` added, 7 lines |
| `EXECUTOR-INSTRUCTIONS.md` | content replaced with the Version 2 session attachment |

## Files Renamed

| From | To | Detection |
|---|---|---|
| `SYSTEM MAP CRYPTOCALCUL.md` (on `main`) | `SYSTEM-MAP-CRYPTOCALCUL.md` | `R100` |
| `TZ-02-foundation.md` (root, on `main`) | `CryptoTZ/TZ-02-foundation.md` | `R041` at `-M20%` |

The TZ-02 relocation is reported by `git diff` at its default 50 % rename threshold as a
delete plus an add, because the content advanced to the newer attachment revision in the
same commit (measured similarity 81.9 % by `difflib`, but git's own index-level
similarity scores it 41 %). `git mv` was used, and `git diff -M20%` pairs it as a rename.
No content was lost: the older revision remains at `origin/main:TZ-02-foundation.md`.

## Files Deleted

**None by this task.**

TZ-02 named two candidates under `Files to Delete`. Neither required action:

| Named for deletion | Disposition |
|---|---|
| `EXECUTOR INSTRUCTIONS.md` (v1, space in filename) | **Already deleted on `main` by the Boss at `9a06078`.** It had been added at `7e2c28c` and removed within the same run of uploads. It existed in neither the merge base nor either branch tip at the time TZ-02 began. Hash while it existed: 237 lines, `e3fe7dd0e686848c339a4ad6edb48bc0`; its header carries no "Version 2" line, confirming it was v1. |
| Superseded duplicates of the System Map | **None existed after scope A.** The merge produced exactly one map file. `git ls-files \| grep -i "system.map"` returns one path. |

Verification that nothing else was removed:

```
$ git diff --name-status -M20% origin/main..HEAD | grep '^D'
(no output)
```

`image.PNG` remains tracked; `index.html` line 8 still references it as the PWA icon.

## Implementation Summary

### A — Landing TZ-01, and the System Map collision

The repository state discovered at A.1, verbatim, is reproduced under
`## Test Results`. In short: `main` had advanced by five commits, all Boss uploads
through the web interface, and the branch and `main` disagreed about the same file.

`origin/main` was merged into the branch (commit `e5e755e`) — a merge, not a rebase, so
no published history was rewritten. Git resolved the rename/modify collision
automatically by tracking the branch's rename and applying `main`'s whole-file
replacement onto the renamed path. **That result was not trusted on git's word.** The
merged file was compared byte-for-byte against `origin/main`'s copy and checked against
every fingerprint anchor before the merge was committed:

```
$ cmp SYSTEM_MAP_CRYPTOCALCUL.md <(git show 'origin/main:SYSTEM MAP CRYPTOCALCUL.md')
  (identical — no hybridisation)
```

The dangerous outcome TZ-02 A.3 warned about — the branch's stale 1136-line content
surviving under the new name — did not occur. Proof is in `## Validation` item 1.

TZ-01's other deliverables were verified intact before the merge was committed:
`bench.yml` byte-identical to its state at `30dfd85`, `main.yml` carrying the full
`paths-ignore` list, and no file deleted.

### B — Canonical filenames and the Version 2 contract

`git mv` to `SYSTEM-MAP-CRYPTOCALCUL.md`, hyphenated per §2. The Version 2 contract was
installed from the session attachment. The v1 file needed no deletion (see
`## Files Deleted`).

**References to the old names: none required updating.** A repository-wide search found
hits only inside the artifact documents' own prose — `CryptoTZ/TZ-02-foundation.md`
lines 30, 94 and 130 describing the corrupted name, and `EXECUTOR-INSTRUCTIONS.md`
lines 1, 8 and 61 describing what Version 2 supersedes. Those are deliberate historical
references inside files that must stay byte-identical to their attachments, and B.3
explicitly forbids "fixing" them. No code, workflow or bench references either name.

### C — Canonical directories

`CryptoTZ/` and `CryptoReports/` are created by their first files, with no `.gitkeep`
placeholders, as C.3 requires.

### D — The hourly schedule, and what the forensics actually found

`schedule: - cron: '0 * * * *'` was added ahead of the existing `push` block. The `push`
trigger, its `paths-ignore` list and `workflow_dispatch` are untouched, and the jobs
section is byte-identical (`147f78e86aefeebabab1d914812fb5de` before and after).
`paths-ignore` is a key of the `push` mapping and does not apply to `schedule` — see
`## Validation` item 6 for the parsed structure. `STALE_WARN_MIN` / `STALE_CRIT_MIN`
were not touched, and no CoinGecko key or key-related configuration was added.

**The forensic finding contradicts TZ-02's stated premise, and the Architect needs it
before merging.** This is reported, not acted on. Full detail in
`## Pre-existing Issues` item 1.

### E — `.gitignore`

Contents are reproduced in full under `## Test Results`. The `backtest_bench.py` cache
path was read from the source rather than guessed: `CACHE = os.path.join(HERE, "cache")`
at `bench/backtest_bench.py:36`, where `HERE` is the `bench/` directory — so
`bench/cache/`.

One path was added beyond E.1's list: **`bench/_*`** instead of the two named scratch
files. Reason: twelve distinct scratch files are written into `bench/` by three
different benches, and their names are composed at run time, so enumerating them would
go stale on the next bench. Every one is underscore-prefixed and **no tracked file under
`bench/` begins with `_`**, verified before adopting the pattern. The two names E.1
specifies, `bench/_run.js` and `bench/_cases.json`, are both covered.

`index.html.prev` and `orig.html` are deliberately **not** ignored, per E.2, and this is
proven positively rather than asserted — see `## Validation` item 10.

### F — The TZ-01 record

`CryptoReports/TZ-01-repo-hardening-report.md` was reconstructed from repository
evidence only: `git log`, `git diff --name-status -M`, the committed contents of
`bench.yml` and `main.yml`, and a fresh execution of all eleven benches at HEAD. It is
marked as reconstructed under TZ-02 with the date, and is not backdated.

## Validation

| # | TZ-02 validation item | Result |
|---|---|---|
| 1 | Exactly one map file, canonical name, all anchors | **PASS** |
| 2 | Exactly one contract file, Version 2 | **PASS** |
| 3 | No tracked filename contains a space | **PASS** — 0 |
| 4 | TZ and TZ-01 report exist, valid Markdown, all sections | **PASS** — 17/17 sections |
| 5 | `bench.yml` byte-identical to `30dfd85` | **PASS** |
| 6 | `main.yml` valid YAML, exactly three triggers, steps identical | **PASS** |
| 7 | Manual dispatch refreshes the Gist `generated_at` | **FAILED — could not be run** |
| 8 | The five gated benches run green | **PASS** |
| 9 | `py_compile` + `node --check`; `index.html`/`main.py` unchanged | **PASS** |
| 10 | `git ls-files` identical before/after `.gitignore`; status clean | **PASS** |
| 11 | No file deleted except those named | **PASS** — none deleted at all |

### Item 1 — the System Map

| Property | Required by TZ header | Found |
|---|---|---|
| Filename | `SYSTEM-MAP-CRYPTOCALCUL.md` | matches |
| Count of map files tracked | exactly one | one |
| Line count | ≈ 1461 | **1461** |
| MD5 | `9590fd08d149fb05d4db0d0179b54a50` | **exact match** |
| Newest `## 9. Журнал миграций` entry | 2026-08-20 | **2026-08-20** |
| Anchor `### 3.12 Direction engine — veto cascade (19.08.2026)` | present | present, line 312 |
| Anchor: invariant `36.` under `## 4. Инварианты — НЕ ЛОМАТЬ` | present | present |

The MD5 matches the TZ header exactly, which is stronger than the TZ asked for — it
allowed for whitespace drift from the upload path and there was none.

### Item 2 — the Executor contract

One file, `EXECUTOR-INSTRUCTIONS.md`, 298 lines, MD5
`82b8da93688529e5581ecf9a050dc232`. Line 3 reads `**Version 2.** Permanent operating
contract for the Claude Code Executor.` No second copy exists under any name.

### Item 6 — `main.yml` structure

Parsed with **PyYAML 6.0.1**. Exactly three triggers:

```
triggers: ['push', 'schedule', 'workflow_dispatch']  count = 3
schedule : [{'cron': '0 * * * *'}]
push.branches: ['main']
push.paths-ignore: bench/**, **/*.md, index.html,
                   .github/workflows/bench.yml, .github/workflows/backtest_bench.yml
workflow_dispatch: None
paths-ignore present on schedule? False
```

Jobs/steps section MD5 `147f78e86aefeebabab1d914812fb5de` — identical before and after.

### Item 7 — FAILED, could not be run

The workflow was dispatched successfully and the run outcome is recorded under
`## Test Results`. **The `generated_at` comparison could not be made**, because this
session cannot read the Gist by either available route:

```
$ curl https://gist.githubusercontent.com/seahomebatumi-ai/3f50574a.../raw/coeffs.json
curl: (56) CONNECT tunnel failed, response 403

$ curl https://api.github.com/gists/3f50574a29bc37434c18cc8480779ccb
HTTP=403
{"message":"This GitHub API path is not available: sessions are bound to their
 configured repositories. Use repository-scoped endpoints (repos/{owner}/{repo}/...)."}
```

The agent proxy's own status endpoint confirms the first as a policy denial, not a
transient failure: `"kind": "connect_rejected", "host": "gist.githubusercontent.com:443"`.

`main.py` does not print `generated_at` on success — it is assigned at line 362 as
`now_utc.isoformat()` and only ever written into the Gist payload — so the workflow log
does not carry it either. **Per §9 this item fails; it is not "not applicable."** What
would unblock it: allowing `gist.githubusercontent.com` in the session's network policy,
or the Architect reading the Gist directly.

## Test Results

### Deliverable 2 — repository state discovered at A.1, verbatim

```
$ git fetch --all --prune
From https://github.com/seahomebatumi-ai/crypto-auto
   fe24061..e05e20f  main       -> origin/main

$ git log --oneline --graph --all -20
* e05e20f Add files via upload
* 9a06078 Delete EXECUTOR INSTRUCTIONS.md
* 7e2c28c Add files via upload
* 4b4e76a Delete SYSTEM MAP CRYPTOCALCUL.md
* 0c42e51 Update SYSTEM MAP CRYPTOCALCUL.md
| * 30dfd85 chore(repo): canonical system map filename, scoped bot push trigger, bench CI gate
|/
* fe24061 Update index.html
* 3611f5c Add files via upload
* 5a1febd Update badge_bench.js
* acb6494 Update verify_board.js
* c665df6 Update index.html
* 76e0017 Add files via upload

$ git diff --name-status -M origin/main..claude/new-session-113so9
A	.github/workflows/bench.yml
M	.github/workflows/main.yml
D	EXECUTOR-INSTRUCTIONS.md
R074	SYSTEM MAP CRYPTOCALCUL.md	SYSTEM_MAP_CRYPTOCALCUL.md
D	TZ-02-foundation.md
```

The `R074` line is the collision: git paired `main`'s freshly uploaded 1461-line map
with the branch's renamed 1136-line copy at 74 % similarity. The two `D` lines are
artifacts of comparing a branch that predates the Boss's uploads — not deletions
proposed by the branch.

### Deliverable 3 — how the collision was resolved, and proof

Resolved by merging `origin/main` into the branch and verifying the result against the
fingerprint before committing. Proof that the 2026-08-20 content survived:

```
merged file : 1461 lines, MD5 9590fd08d149fb05d4db0d0179b54a50
origin/main : 1461 lines, MD5 9590fd08d149fb05d4db0d0179b54a50   -> identical
branch copy : 1136 lines, MD5 813fa95f1512806ebcad057a84d4dcce   -> discarded, correctly

anchor "### 3.12 Direction engine — veto cascade (19.08.2026)"  present (line 312)
invariant 36. under "## 4. Инварианты — НЕ ЛОМАТЬ"              present
newest migration entry                                          2026-08-20
conflict markers anywhere in the tree                           none
```

The discarded copy contained neither anchor — `grep -c` returned 0 for both — which is
independent confirmation that the surviving file is the newer one and not a hybrid.

### Deliverable 4 — schedule forensics (D.4)

**No `schedule` trigger has ever existed in this file, and no workflow in this
repository's history has ever carried a cron.**

```
$ git log --follow --oneline --all -- .github/workflows/main.yml
30dfd85 chore(repo): canonical system map filename, scoped bot push trigger, bench CI gate
849d8fc Update index.html

$ (every revision of main.yml scanned for schedule:/cron:)
NO revision of .github/workflows/main.yml has ever contained a schedule/cron trigger.

$ (every workflow file in every commit scanned for cron:)
(no output)
```

`main.yml` has been touched by exactly two commits in its life: `849d8fc`, which created
it (mislabelled "Update index.html"), and `30dfd85`, TZ-01. So there is **no commit and
no date that removed a schedule** — there was never one to remove.

This answers the question D.4 posed: it is a **documentation error in map §1**, not a
silent regression. But the fuller answer is in `## Pre-existing Issues` item 1, because
the hourly cadence map §1 describes is real — it is simply produced outside the
repository.

### Deliverable 5 — validation item 7, the manual run

Dispatched at **2026-08-20T12:49:21Z** against `claude/new-session-113so9`, so the run
exercised the `main.yml` this branch delivers, not `main`'s.

```
Run 1298 (id 32370836645), event workflow_dispatch, branch claude/new-session-113so9
  Set up job                       success   12:49:22 -> 12:49:22
  Checkout repository              success   12:49:22 -> 12:49:23
  Set up Python                    success   12:49:23 -> 12:49:31
  Install dependencies             success   12:49:31 -> 12:49:35
  Run script with fail-safe logic  success   12:49:35 -> 12:56:17   (6m42s)
  Post Set up Python               success
  Post Checkout repository         success
  Complete job                     success

  job conclusion: success        run conclusion: success
  completed 2026-08-20T12:56:20Z
```

**The run completed successfully.** The bot step took 6m42s, in line with the ~7-minute
whole-run duration of every recent successful run. That timing is itself evidence the
first attempt succeeded: `main.yml`'s step is
`python main.py || (… sleep 60 && python main.py)`, so a failed first attempt would have
produced a step of roughly thirteen minutes. It did not. This was not a keyless
CoinGecko rate-limit failure, and it was not a broken workflow — the distinction TZ-02
item 7 asked to be kept.

`generated_at` before and after: **not obtainable from this session** — see
`## Validation` item 7 for the two blocked routes and what would unblock them. What can
be said from the run alone: `main.py:362` sets `generated_at = now_utc.isoformat()` and
the Gist PATCH at line 471 is the last thing the script does, so a successful run
necessarily wrote a `generated_at` inside the window **12:49:35Z – 12:56:17Z**. That is
an inference from the code path and the step timing, **not** an observation of the Gist,
and it is not offered as satisfying item 7.

### Deliverable 6 — the `paths-ignore` list as it now stands

```yaml
paths-ignore:
  - 'bench/**'
  - '**/*.md'
  - 'index.html'
  - '.github/workflows/bench.yml'
  - '.github/workflows/backtest_bench.yml'
```

Unchanged from TZ-01. `main.py` and `main.yml` are deliberately absent and still trigger
the bot on push.

### Deliverable 7 — `.gitignore` in full

```gitignore
# Generated artifacts only. Nothing here is an input to the product or to a
# bench — every entry is something a tool writes and can rewrite.

# Python bytecode. `python3 -m py_compile main.py` (a standing validation step)
# leaves __pycache__/ in the repository root; the benches leave one in bench/.
__pycache__/
*.py[cod]

# Bench scratch. Every bench that drives node from Python writes its bridge
# script and its case file next to itself and does not clean up:
#   display_bench.py    -> bench/_run.js, bench/_cases.json
#   render_bench.py     -> bench/_render_run.js, bench/_render_cases.json
#   backtest_bench.py   -> bench/_tokens.js, bench/_score_bridge.js,
#                          bench/_inv_bridge.js, bench/_res_bridge.js,
#                          bench/_job.json, bench/_out.json,
#                          bench/_job2.json, bench/_out2.json
# The names are derived at run time, so the prefix is matched rather than the
# twelve names enumerated: no tracked file under bench/ begins with '_'.
bench/_*

# Downloaded history for backtest_bench.py. CACHE = os.path.join(HERE,
# "cache") at bench/backtest_bench.py:36, i.e. bench/cache. It holds the
# data.binance.vision archive and is restored from the Actions cache by
# .github/workflows/backtest_bench.yml, never from the repository.
bench/cache/

# OS noise
.DS_Store

# NOT ignored, deliberately: index.html.prev and orig.html. They read as
# debris and are the baselines badge_bench.js and direction_bench.py
# --identity require. Ignoring them would foreclose sourcing them from git
# history, which is TZ-03's job.
```

Paths beyond E.1's list: **`bench/_*`** only, with the reason given in
`## Implementation Summary` scope E.

### Item 10 — `.gitignore` changes nothing that is tracked

```
tracked files before .gitignore : 20
tracked files after  .gitignore : 20 (excluding .gitignore itself)
diff of the two lists           : identical

$ git ls-files --ignored --exclude-standard -c
(empty — no tracked file matches .gitignore)
```

The rules were then exercised against real files rather than asserted — a validator that
passes with no data is a failed validator (invariant 22):

```
!! .DS_Store            ignored
!! __pycache__/         ignored
!! bench/_cases.json    ignored
!! bench/_run.js        ignored
!! bench/cache/         ignored
?? index.html.prev      NOT ignored   <- E.2 requirement, proven
?? orig.html            NOT ignored   <- E.2 requirement, proven
```

All seven probe files were removed afterwards.

### Item 8 — the five gated benches

Run locally at HEAD:

| Bench | Checks | Failures | Exit |
|---|---|---|---|
| `verify_board.js` | 108 | 0 | 0 |
| `board2_bench.js` | 129 | 0 | 0 |
| `prot_bench.js index.html` | 167 | 0 | 0 |
| `verify_bench.py` | 35 | 0 | 0 |
| `direction_bench.py --props --fixtures --control --sim` | 489 786 | 0 blocks | 0 |

And on a real GitHub runner — **Bench gate run #1, conclusion `success`**, every bench
step individually green on `ubuntu-latest`, 55 seconds wall clock. This is the first
runner execution of the gate TZ-01 created; TZ-01 could only replay it locally.

### CI negative test

`EXECUTOR-INSTRUCTIONS.md` §9 requires a negative test from any TZ touching CI. Green →
red → green, with the tree left clean:

```
BASELINE          all five steps exit 0        JOB RESULT: SUCCESS
INJECT            -eq('regime mode', regUp.mode, 'trend');
                  +eq('regime mode', regUp.mode, 'range');
                  step exit=1 :: node bench/verify_board.js
                                              JOB RESULT: FAILURE (step exited 1)
REVERT            bench/verify_board.js identical to HEAD
                  all five steps exit 0        JOB RESULT: SUCCESS
```

Caveat stated plainly: the negative test is a **local replay** of the workflow's shell
contract (`bash -euo pipefail`, fail-fast step ordering), not a runner execution — a
deliberate failure was not pushed to GitHub. The **positive** case is runner-proven, as
above.

### Item 9 — standing checks

```
python3 -m py_compile main.py                       PASS
node --check on the <script> block of index.html    PASS

index.html  20a12f527e6b78a7a661791bbbd89261  == its value at 30dfd85
main.py     064c9dba8313141d1d267316b2da7a39  == its value at 30dfd85
```

Neither production file was modified by this task.

## Deviations

1. **TZ-02 §1 states TZ-01's branch had "an open pull request". It did not.**
   `list_pull_requests` with `state: all` returned an empty set — the repository had
   never had a pull request. TZ-01 as delivered did not request one, and the session's
   operating rules forbade opening one unsolicited. Pull request **#1** was therefore
   created by this task rather than updated, which is what A.2's "open or update"
   permits.

2. **The root `TZ-02-foundation.md` was relocated, not left in place or deleted.**
   `Files to Rename` names only the System Map, and `Files to Delete` does not name this
   file. Leaving it would have violated §3 ("Never keep two copies of the same artifact
   under different names") and §2's canonical path. `git mv` was chosen over
   delete-plus-create so history follows the file. Nothing was lost.

3. **`EXECUTOR-INSTRUCTIONS.md` was modified, though `Files to Modify` names only
   `main.yml`.** B.2 instructs "Commit the attached Executor contract as
   `EXECUTOR-INSTRUCTIONS.md`", which the TZ lists under `Files to Create`. Because the
   Boss had already uploaded an earlier revision to that exact path, creating it
   registers as a modification. The end state is what B.2 specifies.

4. **The branch carries two commits, not one.** §8 asks that the final commit contain
   exactly the implementation plus its report. The pull-request URL and the CI conclusion
   are required inside the report, and neither exists until the implementation is pushed,
   so the implementation was committed and pushed first and the two reports follow in a
   second commit. The delivered branch contains exactly the implementation plus its
   reports and nothing else. No history was rewritten after publication.

5. **Validation item 7 is failed, not skipped.** Recorded under `## Validation`.

## Pre-existing Issues

1. **The hourly refresh is real but comes from outside the repository — TZ-02's premise
   that `coeffs.json` "was refreshed only by pushes" is incorrect.**

   TZ-02 D.4 asked whether a cron was silently removed. It was not: no revision ever had
   one. But the run history shows the bot **has** been running hourly, triggered by
   `workflow_dispatch` from something that is not a person:

   ```
   consecutive workflow_dispatch gaps
     08-20 10:50 -> 11:50   1:00:00
     08-20 09:50 -> 10:50   0:59:59
     08-20 08:50 -> 09:50   1:00:01
     08-20 07:50 -> 08:50   1:00:01
     08-20 06:50 -> 07:50   0:59:58
   seconds-past-the-minute across all observed dispatches: {2, 3, 4}
   ```

   Gaps accurate to one second, at a fixed second past a fixed minute, are a machine.
   **Direct confirmation arrived during this task:** while run 1298 (the dispatch this
   report requested) was still executing, run **1299** was dispatched on `main` at
   `2026-08-20T12:50:05Z` — 48 seconds later, on the same hourly cadence, by something
   other than this session.

   **Consequence the Architect must weigh before merging.** The cron added by scope D
   does not restore a lost refresh; it adds a **second** one. Expect roughly two bot runs
   per hour, two full 28-coin CoinGecko passes, and two Gist writes, on a keyless
   account — against map §1's budget of ~21.6k calls/month, which assumes one.
   Occasionally the two will overlap, as 1298 and 1299 did, with both processes writing
   the same Gist.

   **Evidence for keeping the cron regardless:** the external dispatcher is not reliable.
   It missed the 18:55 slot on 2026-08-19, and it stopped entirely between
   2026-08-19 21:55:04Z and 2026-08-20 05:00:03Z — a 7h05m outage. Accounting for
   push-triggered runs, the real data gap was 2026-08-19 22:44Z → 2026-08-20 05:00Z,
   **about 6h16m**, during which the board was far past both `STALE_WARN_MIN` (75 min)
   and `STALE_CRIT_MIN` (130 min) while still computing leverage from the aged metrics.

   Implemented exactly as D.1 specifies and flagged rather than altered, per §6. The
   choice between retiring the external dispatcher and dropping the cron belongs to the
   Architect and is a TZ-03 decision.

2. **Three benches encode a superseded badge layout.** `display_bench.py` (24 598 checks,
   6 796 failures), `render_bench.py` (123 scenarios, 12 795 checks, 1 565 failures) and
   `direction_bench.py --display` (57 661 checks, 1 block failure) all fail against the
   shipping `index.html`. Root cause: `tierOf` (`index.html:1680–1685`) emits `Фон` at the
   lowest tier and `tierBadge` (`1925–1934`) emits `Word #N — score`, while the benches
   expect the pre-19.08 wording (`Наблюдать`) and ordering (`#N Word score`). All three
   exit non-zero, so invariant 29 is intact — they are honest, merely stale. Untouched, as
   TZ-02's out-of-scope clause requires; reserved for TZ-03.

3. **Two benches have no baseline file in the repository.** `badge_bench.js` needs
   `index.html.prev` and `direction_bench.py --identity` needs `orig.html`; both fail at
   load. `.gitignore` deliberately leaves both filenames un-ignored so TZ-03 can source
   them from git history.

4. **`main.yml` was created by a commit titled "Update index.html" (`849d8fc`).** Commit
   titles on `main` do not describe their contents, which is why the D.4 forensics had to
   scan every revision's bytes rather than read the log. Noted so future forensics do not
   trust the subject lines.

## Remaining Risks

1. **The cron cannot take effect until this pull request is merged.** GitHub runs
   `schedule` triggers only from the default branch, and `origin/main`'s `main.yml`
   contains no `schedule`. Until merge, the hourly refresh continues to depend entirely
   on the external dispatcher described above.

2. **Scheduled workflows are suspended on repositories inactive for 60 days.** Not a
   present risk — the repository has 1 299 workflow runs and commits from today — but the
   cron will stop silently if the project goes quiet, and restoring the YAML would not
   restore it. Actions are currently **enabled**: `Crypto Update` is `state: active`.

3. **GitHub cron is best-effort and drifts under load**, frequently by several minutes at
   the top of the hour. `STALE_WARN_MIN` at 75 minutes absorbs ordinary drift; sustained
   drift beyond 130 minutes would trip `STALE_CRIT_MIN` with nothing actually broken.

4. **Two writers on one Gist.** With both the cron and the external dispatcher active,
   overlapping runs will occasionally race on `coeffs.json`. `main.py` PATCHes the whole
   file, so the loser's pass is simply overwritten — wasted quota rather than corruption,
   but it is quota spent for nothing.

5. **`bench.yml` runs on `pull_request` from this repository only.** It gates nothing on
   a fork, and nothing prevents a direct push to `main` from bypassing it, since branch
   protection is not configured.

## Commit

```
e5e755e Merge origin/main into claude/new-session-113so9
384deba chore(repo): land TZ-01, canonical artifact structure, restore hourly bot schedule
```

The subject line of `384deba` is the string given in TZ-02's `## Commit Message`,
verbatim. A third commit adds the two reports.

Diff of the implementation against `origin/main`:

```
 .github/workflows/bench.yml                        |  62 +++++
 .github/workflows/main.yml                         |  17 ++
 .gitignore                                         |  33 +++
 CryptoTZ/TZ-02-foundation.md                       | 260 +++++++++++++++++++++
 EXECUTOR-INSTRUCTIONS.md                           |  63 ++---
 ...P CRYPTOCALCUL.md => SYSTEM-MAP-CRYPTOCALCUL.md |   0
 TZ-02-foundation.md                                | 249 --------------------
 7 files changed, 409 insertions(+), 275 deletions(-)
```

`main.yml` shows 17 lines added against `origin/main` because that total includes TZ-01's
10-line `paths-ignore` block; TZ-02's own contribution is the 7-line `schedule` block.

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/1**

CI conclusion: **Bench gate — `success`** (run #1, `ubuntu-latest`, all five bench steps
green). The `Crypto Update` run triggered for validation item 7 is reported under
`## Test Results`, Deliverable 5.

**NOT IN EFFECT UNTIL MERGED**

## Final Repository State

Branch `claude/new-session-113so9` carries the merge of `origin/main`, the TZ-02
implementation, and both reports. `main` is untouched — nothing was pushed to it and no
history was rewritten anywhere. Merging is the Boss's action, because `main` deploys the
live calculator through GitHub Pages.

Working tree clean; `git status --porcelain` empty after the final commit.

**NOT IN EFFECT UNTIL MERGED**

## Fingerprints

| File | Lines | MD5 |
|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1461 | `9590fd08d149fb05d4db0d0179b54a50` |
| `index.html` | 3413 | `20a12f527e6b78a7a661791bbbd89261` |
| `main.py` | 485 | `064c9dba8313141d1d267316b2da7a39` |

Newest entry under `## 9. Журнал миграций`: **2026-08-20**.

Supporting artifacts:

| File | Lines | MD5 |
|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 298 | `82b8da93688529e5581ecf9a050dc232` |
| `CryptoTZ/TZ-02-foundation.md` | 260 | `fee0638b8054901260f8336290ac604b` |
| `.gitignore` | 33 | `aa1aa7c4400033198175a1eaa02113eb` |
| `.github/workflows/bench.yml` | 62 | `c2dc4556fb1688a344372005b73b7be1` |
| `.github/workflows/main.yml` | 48 | `efdc9b444b0c25b1f7f67edd6bfa6d65` |
