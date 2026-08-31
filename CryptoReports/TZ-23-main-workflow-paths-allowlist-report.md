# Implementation Report — TZ-23

**`main.yml` paths allow-list.** Specification:
`CryptoTZ/TZ-23-main-workflow-paths-allowlist.md`. Executed 2026-08-31, session
moment `Mon Aug 31 08:55:55 AM UTC 2026` (`date -u`).

---

## Status

**COMPLETED.**

One file modified — `.github/workflows/main.yml`, its `on.push` block only. The
`paths-ignore` list is replaced by a `paths` allow-list carrying two literal paths
derived from `main.py` at execution time. All nine validation items of the TZ's §5 are
run and pass, plus the negative test contract §9 requires of any TZ touching CI. The
work is on a pushed branch and is **not in effect until merged**.

**Read first — a previous TZ's branch is not merged, and it is not this one's.**
Contract §8 requires this check before the work starts. `claude/tz-21-...` (TZ-21) **is**
merged (`edd650c`), so the base this TZ builds on is current. But
`claude/tz-20-catalyst-registry-content` (`fe2660f`) is **not an ancestor of
`origin/main`**, and one half of TZ-20's authorised change is therefore live nowhere
while its report on `main` describes it as delivered. Detail and evidence under
`## Pre-existing Issues`, item 2. TZ-23 touches none of those files and does not repair
it.

---

## Inbound Filing

The TZ arrived at its canonical path and needed no move.

At session start the clone's tip was `5faffc9` and `CryptoTZ/TZ-23-*.md` did not exist —
the §3 trap exactly. `git fetch --all --prune` brought `5faffc9..deb788f`:

```
$ git fetch --all --prune
From github.com:seahomebatumi-ai/crypto-auto
 - [deleted]         (none)     -> origin/claude/tz-21-catalyst-registry-scope-and-basis
   5faffc9..deb788f  main       -> origin/main

$ git rev-parse --is-shallow-repository
false

$ git show --stat --oneline deb788f
deb788f Add files via upload
 CryptoTZ/TZ-23-main-workflow-paths-allowlist.md | 278 ++++++++++++++++++++++++
 1 file changed, 278 insertions(+)
```

Path on arrival: `CryptoTZ/TZ-23-main-workflow-paths-allowlist.md`. Canonical path
stated in the TZ's own header: `CryptoTZ/TZ-23-main-workflow-paths-allowlist.md`.
Identical.

**Files moved: none. Files renamed: none. `git mv` invocations: 0.** The clone was not
shallow, so no `--unshallow` was needed and the historical searches below run against a
complete history.

Two further commits arrived in the same fetch and are the working base:
`8c995db Update ANALYST-INSTRUCTIONS.md` and `7656046 Update SYSTEM-MAP-CRYPTOCALCUL.md`.
The branch was cut from `deb788f`.

---

## Scope Executed

**Class: branch TZ** (contract §8). Read off the TZ's `## Scope`, not chosen: it names
`.github/workflows/main.yml` under *Files to modify*, a path outside `CryptoReports/**`.
A branch and a pull request are therefore in scope, and `## Final Repository State`
carries the merge sentence.

| TZ section | Requirement | Executed |
|---|---|---|
| §0 | System Map fingerprint gate | yes — passed, `## Validation` item 0 |
| §0 | Second gate: contract v15, §8 names two TZ classes | yes — passed |
| §3.1 | Derive the bot's read set from `main.py`, never from the TZ | yes — result is **nil**; see below |
| §3.2 | `paths` with literal entries, no glob; `branches` and `workflow_dispatch` untouched | yes |
| §3.3 | Rewrite the Russian comment for the allow-list, three named clauses; cron comment untouched | yes |
| §3.4 | Evaluate both filters against real changed-file lists, both directions, with two must-fire controls | yes — 6 rows, 0 failures |
| §4 | `workflow_dispatch` present, unindented under `on:`, unfiltered | yes — verified in the parse and in the raw text |
| §5 | Nine validation items | yes — all pass |
| §6 | Post-merge readings stated as pending, never observed | yes |
| §7 | Three documentation sites listed for the Architect | yes — line numbers below |
| §3.5 | Nothing else touched | yes — one file, one hunk |

Out of scope and untouched, as §2 and §3.5 require: `jobs:`, `main.py`, every bench,
`bench.yml`, `backtest_bench.yml`, `journal.yml`, `calib.yml`, `index.html`,
`catalysts.json`, everything under `analyst/`.

---

## Files Created

- `CryptoReports/TZ-23-main-workflow-paths-allowlist-report.md` — this report.

## Files Modified

- `.github/workflows/main.yml` — `on.push` block only. 51 → 57 lines.
  MD5 `bbba090ebaa8d0f9c7c3530fd4bd7674` → `4d3a83651f7d3a57da19609b9894118e`.

## Files Renamed

None.

## Files Deleted

None. (The `paths-ignore` **list** is deleted from inside `main.yml`; no file is.)

---

## Implementation Summary

### §3.1 — the derivation, and it is nil

The allow-list is derived from `main.py`'s source at execution time. **The result is
that the bot reads no repository file at all**, stated as nil rather than passed over:

```
$ grep -n -E "^\s*(import|from)\s" main.py
1:import os
2:import json
3:import time
4:import sys
5:import numpy as np
6:import requests
7:from datetime import datetime, timezone, timedelta
8:from pycoingecko import CoinGeckoAPI
```

No repository module is imported. Every name on lines 1–8 is stdlib or a PyPI package
the workflow installs itself (`pip install requests pycoingecko numpy`); there is no
`requirements.txt` in the job and therefore no repository file behind that step either.

Filesystem-access counts, each measured, each zero:

| Probe | Occurrences in `main.py` |
|---|---:|
| `open(` | **0** |
| `Path(` | **0** |
| `pathlib` | **0** |
| `read_text` | **0** |
| `read_bytes` | **0** |
| `json.load(` (the file variant) | **0** |
| `__file__` | **0** |
| `os.path` | **0** |
| `os.getcwd` / `os.listdir` / `os.scandir` | **0** |
| `glob` | **0** |
| `shutil` | **0** |
| `csv` / `yaml` / `configparser` | **0** |
| `sys.path` | **0** |
| `np.load` / `np.loadtxt` / `np.genfromtxt` / `np.fromfile` | **0** |

`os.environ` appears twice and neither is a path:

```
13:api_key = os.environ.get('COINGECKO_API_KEY')
17:GIST_TOKEN = os.environ.get('GIST_TOKEN')
```

Both are secrets (hard floor 6), not filesystem locations.

Five string literals in `main.py` end in `.json`, and all five are **Gist file keys
inside an HTTP payload**, not repository paths:

```
428:"history.json"   429:"history.json"   475:"coeffs.json"   480:"debug.json"   481:"history.json"
```

Their lane is visible in the source. Line 421 issues
`requests.get("https://api.github.com/gists/{GIST_ID}")`; line 427 reads
`existing.json().get("files", {})` — the parsed HTTP **response**; line 437 is
`history_points = json.loads(raw)` where `raw` came from `hf.get("content")` or from a
second `requests.get(hf["raw_url"])` on line 434. Line 485 `requests.patch` writes the
three files back. Three `requests.*` calls in the whole file (421, 434, 485), two
CoinGecko calls (71, 89), and no file handle anywhere.

`sys` is used once, at line 506: `sys.exit(main() or 0)`.

**`catalysts.json` — the path the TZ names as the one to confirm rather than assume:**

```
$ grep -c "catalysts" main.py
0
```

Zero occurrences. The map corroborates independently at §1's module table — Data bot
`main.py` **Reads: CoinGecko**; the registry is read by `index.html` in the browser and
by `journal/write.js` under `journal.yml` (map lines 104–106), and map line 129 states
it is "read by the frontend over plain XHR. The bot does not write it." The derivation
above is from the source; the map is agreement, not the basis.

**Therefore the §3.1 nil branch applies and the set is exactly two paths:** `main.py`
(itself) and `.github/workflows/main.yml` (its own trigger and job definition). Nothing
was added on plausibility.

### §3.2 — literal entries, no glob

```yaml
    paths:
      - 'main.py'
      - '.github/workflows/main.yml'
```

Wildcard characters (`*`, `?`, `[`, `]`, `!`) across both entries: **0**. `branches:
[ main ]` is byte-identical to its previous text; `workflow_dispatch:` is byte-identical
and still unfiltered. No pattern was invented, so inv. 52's failure mode — a reading of a
third party's matcher standing as a fact about it — does not arise for the new list.

### §3.3 — the comment

The cron comment above `push:` is untouched and byte-identical (proof under
`## Validation` item 6). The comment that explained the ignore list is rewritten for the
allow-list, in Russian per the standing workflow-comment exception, and carries the three
clauses the TZ names:

1. **what the bot reads and that the list is derived**, with the derivation's own
   evidence in the comment: zero `open( / Path( / json.load( / __file__ / os.path`,
   imports on lines 1–8 stdlib and PyPI only, `os.environ` at 13 and 17 holding secrets
   and not paths, CoinGecko and the Gist over HTTP, and `catalysts.json` named explicitly
   as read by the frontend and `journal/write.js` but not by the bot;
2. **`workflow_dispatch` is not filtered** — the 17 daily iPhone runs pass outside this
   list and it cannot stop them;
3. **the coupling, named as a coupling** — the allow-list must GROW when the bot gains an
   input; a forgotten entry in `paths-ignore` burned runner minutes loudly (inv. 53), a
   forgotten entry here withholds the run quietly, `coeffs.json` ages and nothing on
   screen says so. The comment states that this is the worse direction and is why it
   exists.

The two-line note about `analyst/**` went with the list it annotated: `analyst/` is not
in the allow-list, so it cannot start the bot, and an exclusion for it would be a
sentence about a rule that no longer exists.

---

## Validation

### 0. System Map fingerprint gate — PASS (blocking, run before any work)

Revision found: `**Revision 2026-08-30-f.**` Revision required by the TZ header:
`**Revision 2026-08-30-f.**` Identical.

All seven anchors matched as exact substrings against the repository copy:

| Anchor | Result |
|---|---|
| `**Revision 2026-08-30-f.**` | PRESENT |
| `### 3.12 Direction engine — veto cascade` | PRESENT |
| `### 3.15 Catalyst registry` | PRESENT |
| `### 3.16 List exhaustion — the day-range measure` | PRESENT |
| `## 11. Analytical engine` | PRESENT |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | PRESENT |
| `55. **A specification is checked against the text it must obey, never against memory of it.**` | PRESENT |

Anchors checked: **7**. Missing: **0**.

Every file the map's `## 0` table lists, measured at the required revision — all four
match line count and MD5 exactly, so nothing is reported as ahead:

| File | Lines required / found | MD5 required / found | Verdict |
|---|---|---|---|
| `index.html` | 3729 / 3729 | `fdf331906bf205944b25e3635135789c` / same | match |
| `main.py` | 506 / 506 | `1a5a5d98b2fd76010f202ee3eebaa717` / same | match |
| `catalysts.json` | 17 / 17 | `f9b2dd4a3594134b2b7b603de19075c3` / same | match |
| `bench/exhaustion-calibration.txt` | 175 / 175 | `3b8730b254467c9df4c0a845a0f3cfb3` / same | match |

**Second gate — contract v15.** `EXECUTOR-INSTRUCTIONS.md` carries `**Version 15.**`
(1 occurrence at the head of the file), and §8 names both classes at lines 458 and 460:
`A **branch TZ** authorises at least one written file outside CryptoReports/**` and
`A **report-only TZ** authorises exactly one written file — its own report`. This TZ is
the **branch** class.

### 1. YAML parses; `on.push` carries `paths` and no `paths-ignore` — PASS

```
$ python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/main.yml'))"
(no output, exit 0)   pyyaml 6.0.1
```

Parsed structure (`on` is read at key `True`, because YAML 1.1 parses the bare token `on`
as a boolean — noted so the reading is reproducible):

```
top-level keys : ['name', True, 'jobs']
on.* keys      : ['push', 'workflow_dispatch']
on.push keys   : ['branches', 'paths']
has paths        : True
has paths-ignore : False
on.push.branches : ['main']
on.push.paths    : ['main.py', '.github/workflows/main.yml']
```

### 2. §3.1 derivation reported with line numbers, nil stated as nil — PASS

`## Implementation Summary` §3.1 above. Line numbers 1–8 (imports), 13 and 17
(`os.environ`), 421 / 427 / 434 / 437 / 485 (the Gist HTTP lane), 428 / 429 / 475 / 480 /
481 (the five `.json` literals), 506 (`sys.exit`), and thirteen zero counts including
`open(` = 0 and `catalysts` = 0. The nil result is the finding, not an omission.

### 3. Every `paths` entry literal — wildcard count zero — PASS

```
literal entry 'main.py'                       (wildcard chars=0)
literal entry '.github/workflows/main.yml'    (wildcard chars=0)
TOTAL wildcard characters across all paths entries: 0
```

### 4. §3.4 evaluation table — PASS, 6 rows, 0 failures, both must-fire controls present

Both pattern lists are **read from the YAML** — the old one from a byte-identical copy of
the pre-edit file, the new one from the working tree — and every changed-file list is the
output of `git diff --name-only` against a named commit. Nothing in this table is typed.

```
old paths-ignore (6): ['bench/**', '**.md', 'index.html', '.github/workflows/bench.yml',
                       '.github/workflows/backtest_bench.yml', 'analyst/**']
new paths        (2): ['main.py', '.github/workflows/main.yml']
```

| Row | Commit | `git diff --name-only` | Old `paths-ignore` | New `paths` | Required | Verdict |
|---|---|---|---|---|---|---|
| **must fire** | `2ca4e18` *Update main.py* | `main.py` | FIRES (unignored: `main.py`) | **FIRES** (`main.py` ~ `main.py`) | fires | PASS |
| **must fire** | `14ed625` *revert(ci): remove the hourly cron* | `.github/workflows/main.yml` | FIRES (unignored: `.github/workflows/main.yml`) | **FIRES** (`.github/workflows/main.yml` ~ `.github/workflows/main.yml`) | fires | PASS |
| must not fire | `edd650c^1..edd650c` — the TZ-21 merge | `bench/catalyst_bench.js`, `catalysts.json` | **FIRES — the defect** (unignored: `catalysts.json`) | does not fire | does not fire | PASS |
| must not fire | `fe24061` *Update index.html* | `index.html` | does not fire | does not fire | does not fire | PASS |
| must not fire | `5faffc9` *docs(discovery) … (TZ-24)* | `CryptoReports/TZ-24-discovery-host-permission-and-extractability-report.md` | does not fire | does not fire | does not fire | PASS |
| must not fire | `0a734ab` *analyst: 2026-08-30* | `analyst/log/2026-08-30-2.md`, `analyst/state.json` | does not fire | does not fire | does not fire | PASS |

Rows evaluated: **6**. Must-fire control rows: **2**. Failures: **0**.

The third row reproduces the measured defect §1 of the TZ describes: the old list fires
on the TZ-21 merge because `catalysts.json` matches none of its six patterns, which is
`Crypto Update` #1492 and its thirty CoinGecko calls. The new list does not.

**Matcher and its standing.** `**` → any characters including `/`; `*` → any characters
except `/`; every other character literal and anchored at both ends. This is a **local
reading of GitHub's filter-pattern semantics, not a runner result.** It is the second
method inv. 52 permits — evaluation against a changed-file list from `git diff
--name-only` — and it is used because the first method is unavailable here: `main.yml`'s
`push` trigger is `branches: [ main ]`, so no `claude/**` push exercises it, and this
session has no GitHub API access to read Actions history (map §10, contract §9). The
final proof is on the runner after the merge and is §6's, not this report's. §3.2's
refusal of globs is what keeps the new list's reading unambiguous under any matcher: two
literal strings compare equal or they do not.

### 5. `workflow_dispatch` verified per §4 — PASS

- Present: yes — `on.* keys: ['push', 'workflow_dispatch']`.
- Unindented under `on:`: yes — raw line 32 is `'  workflow_dispatch:'`, leading spaces
  **2**, the same column as `push:` on line 11.
- Carries no filter of any kind: yes — its parsed value is `None`, and `on` has exactly
  two events, `{'push', 'workflow_dispatch'}`.

`paths` filters `push` only. The Boss's 17 daily Shortcut runs are outside this filter
and cannot be stopped by it. This is the check that separates "the bot skips a commit it
did not need" from "the bot stopped", and it passes.

### 6. Comment clauses present; cron comment byte-identical — PASS

The cron comment is repository lines 4–10 in both the pre-edit and post-edit file, seven
lines, and is byte-identical:

```
cron md5 before: 72e86584e21554956cbae5279f56be18
cron md5 after : 72e86584e21554956cbae5279f56be18
lines 1-12 byte-identical: True
```

Lines 1–12 — through `branches: [ main ]` — are byte-identical, so `name:`, `on:`, the
cron comment and the branch filter are all provably untouched. The three clauses of the
new comment are itemised in `## Implementation Summary` §3.3.

### 7. Diff touches exactly one file and only the `on.push` block — PASS

```
$ git diff --name-only
.github/workflows/main.yml
count=1

$ git diff -U0 .github/workflows/main.yml | grep -c '^@@'
1

$ git diff --stat
 .github/workflows/main.yml | 32 +++++++++++++++++++-------------
 1 file changed, 19 insertions(+), 13 deletions(-)
```

**One file. One hunk.** The hunk header is `@@ -10,19 +10,25 @@ on:` — it opens inside
the `on:` mapping and closes before `jobs:`.

`jobs:` shown identical as a measurement rather than a claim:

```
jobs: starts at old line 28, new line 34
jobs section byte-identical: True
jobs md5 before: 147f78e86aefeebabab1d914812fb5de
jobs md5 after : 147f78e86aefeebabab1d914812fb5de
jobs section lines: 25 -> 25
```

### 8. No-regression on the gate — 13 steps, 1 250 739 checks, unmoved

**This is a LOCAL replay of `bench.yml`'s 13 steps in file order, not a runner run.**
The runner reading belongs to the audit (contract §9).

| # | Step | Checks |
|---:|---|---:|
| 1 | `node bench/verify_board.js` | 109 |
| 2 | `node bench/board2_bench.js` | 130 |
| 3 | `node bench/prot_bench.js index.html` | 372 |
| 4 | `python3 bench/verify_bench.py` | 35 |
| 5 | `python3 bench/direction_bench.py --props --fixtures --control --sim` | 255 708 |
| 6 | `node bench/fresh_bench.js` | 3 424 |
| 7 | `node bench/journal_bench.js` | 691 109 |
| 8 | `node bench/catalyst_bench.js` | 23 062 |
| 9 | `python3 bench/display_bench.py` | 24 598 |
| 10 | `python3 bench/render_bench.py` | 15 925 |
| 11 | `python3 bench/direction_bench.py --display` | 15 629 |
| 12 | `node bench/exhaustion_bench.js` | 220 598 |
| 13 | `bash analyst/live-gate.sh --selftest` | 40 |
| | **TOTAL** | **1 250 739** |

Steps: **13**. Failures reported by any bench: **0**. Total required by the map's `## 0`
block at revision `2026-08-30-f`: **1 250 739**. **Match.** Step 8 reads 23 062, the
value TZ-21 left it at; step 13 reads 40, the value TZ-18 left it at. No count moved,
which is the required result for a change that writes no production file, bench or
constant.

**One step needed a raised Node heap in this session and the reason is the machine, not
the change.** Under `bench.yml`'s own command, step 5 exits 1 here with
`FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory`. The
failure is isolated to `direction_bench.py --control`; `--sim` alone exits 0 with 6
checks. It reproduces identically on a pristine `origin/main` tree carrying none of this
branch's changes, and it clears when the heap ceiling is lifted. Full evidence under
`## Pre-existing Issues` item 1, and the deviation is stated under `## Deviations`.

### 9. Standing checks — PASS

```
$ python3 -m py_compile main.py
(no output, exit 0)

$ node --check <script block extracted from index.html>
(no output, exit 0)     node v22.23.1
script blocks found: 1; extracted block 192 939 chars, 3 161 lines
```

Neither file is edited by this TZ, so these confirm the branch is clean rather than
confirm a change.

### Negative test — required by contract §9 of any TZ touching CI

A gate never proven to fail is not a gate. Four real failures were forced in the working
tree, each instrument's response measured, each reverted with the file's MD5 confirmed
byte-identical afterwards. Post-edit MD5 held throughout:
`4d3a83651f7d3a57da19609b9894118e`.

| # | Forced failure | Instrument | Result | Revert |
|---|---|---|---|---|
| A | `- 'main.py'` → `- '**.py'` | literal-path check | wildcard chars **2** → **FAIL** as required | IDENTICAL |
| B | `- 'main.py'` deleted | §3.4 evaluator | must-fire row 1 → **FAIL**, evaluator **exit 1** | IDENTICAL |
| C | `paths-ignore:` reintroduced beside `paths:` | structural check | `on.push keys: ['branches','paths-ignore','paths']` → **FAIL**, **exit 3** | IDENTICAL |
| D | a tab character appended inside the block | YAML parse check | `yaml.scanner.ScannerError: found character '\t' that cannot start any token`, **exit 4** | IDENTICAL |

Test A is worth reading precisely: the literal-path check went red, and the §3.4
evaluator stayed green — correctly, because `'**.py'` still matches `main.py`, so the
fire/no-fire behaviour is unchanged and only §3.2's literal requirement is broken. The
two instruments measure different things and neither substitutes for the other. Test B is
the one that proves the evaluator is not blind: remove the path and the must-fire control
goes red, which is why §3.4 refuses a table without those two rows — a filter matching
nothing passes every must-not-fire row perfectly.

After all four reverts the full structural suite was re-run on the restored file: **11
checks, 0 failures**, and the §3.4 evaluator re-run: **6 rows, 0 failures, exit 0**.

---

## Test Results

| Item | Result |
|---|---|
| §0 fingerprint gate — revision, 7 anchors, 4 file fingerprints | PASS |
| §0 second gate — contract v15, §8 names both classes | PASS |
| §5.1 YAML parses; `paths` present, `paths-ignore` absent | PASS |
| §5.2 derivation reported with line numbers, nil stated as nil | PASS |
| §5.3 wildcard count zero | PASS |
| §5.4 evaluation table, 6 rows, 2 must-fire controls | PASS (0 failures) |
| §5.5 `workflow_dispatch` present, unindented, unfiltered | PASS |
| §5.6 three comment clauses; cron comment byte-identical | PASS |
| §5.7 one file, one hunk, `jobs:` byte-identical | PASS |
| §5.8 13-step gate, 1 250 739 checks, unmoved | PASS (local replay; see `## Deviations`) |
| §5.9 `py_compile` + `node --check` | PASS |
| contract §9 negative test, 4 forced failures | PASS (4/4 went red, 4/4 reverted identical) |
| **Total validation items** | **12 run, 12 pass, 0 skipped, 0 failed** |

---

## Deviations

**One, and it is in how a validation item was measured, not in what was built.**

§5 item 8 asks for the 13-step gate green at 1 250 739 checks. Under `bench.yml`'s own
command, step 5 exits 1 on this machine with a V8 heap OOM. To obtain step 5's check
count the step was re-run with `NODE_OPTIONS="--max-old-space-size=2600"` and then exits
0 with **255 708** checks, which is exactly the residual the other twelve steps leave
against the required total (995 031 + 255 708 = 1 250 739).

What that flag is and is not:

- it is an environment variable set on one command line in this session;
- it is **not** in the repository, **not** in `bench.yml`, and **not** committed;
- **no bench file, assertion, expectation or step was edited, skipped, commented out or
  given `continue-on-error`** (hard floor 2 and 12). The bench that failed is the bench
  that then passed, byte for byte.

The underlying failure is diagnosed as environmental and pre-existing under
`## Pre-existing Issues` item 1. The runner has no such ceiling and its reading of the
gate is the audit's, per contract §9.

No other deviation. Scope, filter contents, comment language and commit message are as
the TZ specifies.

---

## Pre-existing Issues

### 1. `direction_bench.py --control` exhausts the Node heap on this VPS — environment, not product

**Diagnosis.** Step 5 shells out to `node` (`run_node`, `bench/direction_bench.py:132`,
invoked at line 138). `check_control(seeds=16, coins=70, days=360)` at line 826 builds
enough array data that V8 aborts:

```
FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory
...
17: v8::internal::Runtime_CreateArrayLiteral(...)
```

The three preceding blocks print `[OK ] СВОЙСТВА`, `[OK ] РЕЖИМ`, `[OK ] ФИКСТУРЫ` before
the abort, so the failure is inside `--control`.

**Proof that it pre-existed.** Reproduced on a pristine `origin/main` tree extracted with
`git archive origin/main` into `/tmp`, carrying none of this branch's changes — the
workflow file there hashes `bbba090ebaa8d0f9c7c3530fd4bd7674`, the pre-edit value:

```
$ (pristine origin/main) python3 bench/direction_bench.py --props --fixtures --control --sim
EXIT=1        "heap out of memory" occurrences: 1

$ (pristine origin/main) python3 bench/direction_bench.py --control
EXIT=1        "heap out of memory" occurrences: 1

$ (pristine origin/main) python3 bench/direction_bench.py --sim
EXIT=0        ИТОГО проверок: 6 | провалов блоков: 0
```

**Proof that it is a ceiling and not a defect.** The same `--control` on the same
pristine tree, with the heap ceiling lifted:

```
$ (pristine origin/main) NODE_OPTIONS="--max-old-space-size=2600" python3 bench/direction_bench.py --control
EXIT=0        "heap out of memory" occurrences: 0
[OK ] КОНТРОЛЬ
ИТОГО проверок: 2 | провалов блоков: 0
```

**The machine.** `free -m` reports **955 MB total**, 443 MB available, **1 CPU**, 3 GB
swap. Node sizes its default old-space from available memory, so the ceiling here is a
few hundred megabytes. `bench.yml` runs on `ubuntu-latest`, which is not this machine.
Nothing in the repository is wrong and nothing was changed: this is a fact about the
session's environment, recorded because §5 item 8 was measured on it. Flagged, not fixed,
and out of this TZ's scope in any case.

### 2. `claude/tz-20-catalyst-registry-content` was never merged, and half of TZ-20 is live nowhere

Found while performing the contract §8 check that opens this report.

```
$ git merge-base --is-ancestor fe2660f origin/main
exit=1        (non-zero: NOT an ancestor)

$ git show origin/main:bench/catalyst_bench.js | grep -c "federalregister.gov"
0
```

`CryptoReports/TZ-20-catalyst-registry-content-report.md`, immutable on `main`, states
under its own `## Files Modified`:

> `bench/catalyst_bench.js` — `federalregister.gov` added to `PRIMARY`; a justification
> paragraph added to the block comment that governs that list; four boundary cases added
> to `QCASES`.

None of those three are on `origin/main`. `PRIMARY` there ends `'hyperliquid.xyz',
'ton.org'` with no `federalregister.gov` anywhere in the file.

**The registry half did land, by a different route.** `catalysts.json` on `origin/main`
carries the ZEC entry byte-identically to the branch's, and its ENA entry is TZ-21's
later, superseding version (`d` `2026-09-02` → `2026-09-05`, plus the `basis` field). The
file's MD5 on `main` matches the map's `## 0` table, so the map treats the registry as
current — which it is. The gap is confined to the bench.

**It is consistent with the gate count, which is why nothing has caught it.** Step 8 of
the gate reads 23 062 both in the map at revision `-f` and in this session's local
replay — the value TZ-21 left. TZ-20's four `QCASES` boundary cases would have moved it.
The count agreeing is not evidence the work landed; it is evidence that nothing on `main`
ever reflected it.

**Not repaired here and not repairable here.** `bench/catalyst_bench.js` is outside this
TZ's scope (§6), and `PRIMARY` is a trust root that hard floor 13 closes to any change a
TZ does not name explicitly — one added host silently converts an aggregator into an
authority. This is a finding for the Architect: either the branch is merged, or a new TZ
re-applies the bench half, or TZ-20's report is understood to overstate what reached
`main`.

### 3. `main.yml`'s old list fired on `journal/**`, and `[skip ci]` was the only thing stopping it

Not a defect this TZ introduces — it is the shape §1 of the TZ describes, recorded because
the evaluation surfaced it. `journal/**` was absent from the six `paths-ignore` entries,
so `journal.yml`'s daily commit to `main` matched nothing and qualified to start
`Crypto Update`. It did not, because every such commit carries `[skip ci]` in its subject:

```
$ git log --all --format='%s' -6 -- journal/runs.jsonl
journal: 2026-08-30 [skip ci]
journal: 2026-08-29 [skip ci]
journal: 2026-08-28 [skip ci]
journal: 2026-08-27 [skip ci]
journal: 2026-08-26 [skip ci]
journal: 2026-08-25 [skip ci]
```

A commit-message convention was the whole of the control. Under the allow-list the path
cannot start the bot whatever the subject line says, so this TZ removes a dependency
rather than adding one. Recorded, not acted on.

---

## Remaining Risks

1. **The coupling this change creates is real and is carried by a comment.** An allow-list
   must grow whenever the bot gains a repository input; a forgotten entry stops the bot
   silently and `coeffs.json` ages with nothing on screen to say why. That is inv. 53's
   shape with its sign reversed, and reversed into the worse direction — inv. 53's
   forgotten entry burned runner minutes loudly. §3.3 requires the comment to name it and
   the comment does. **No bench can enforce it**: a control over a workflow's trigger
   would have to observe the trigger, and this session already established that
   `main.yml`'s `push` filter is unreachable from any `claude/**` push. Today the derivation
   is nil, so the list is as small as it can be and the coupling is dormant; the risk
   materialises the first time `main.py` learns to read a file.
2. **The matcher in §3.4 is a local reading.** Two literal strings leave little room for
   a matcher to disagree, which is why §3.2 forbids globs, but the reading is still a
   reading. §6's two post-merge observations are the measurement.
3. **The bot now skips paths it previously ran on.** `catalysts.json`, `journal/**`,
   `.github/workflows/journal.yml`, `.github/workflows/calib.yml` and every future
   unnamed path no longer start `Crypto Update` on a push to `main`. This is the change's
   purpose and is safe on today's derivation — none of them is read by `main.py`. It stops
   being safe the moment that stops being true, which is risk 1.
4. **`bench.yml` has an allow-list question of its own** and the TZ explicitly leaves it
   alone (§3.5). Untouched here; named so it is not mistaken for settled.
5. **Step 5 of the gate cannot be run on this VPS under the workflow's own command.** Any
   future session validating on this machine will meet the same ceiling and should not read
   it as a product failure. See `## Pre-existing Issues` item 1.

---

## Documentation dependency — §7, recorded for the Architect, not repaired here

The map is Architect-owned and arrives by Boss upload (contract §2), so the Executor
neither edits it nor is asked to. Three sites assert the absence this change removes and
turn false on merge (inv. 50). Located in
`SYSTEM-MAP-CRYPTOCALCUL.md` at revision `2026-08-30-f`, 1664 lines:

| # | Line | Text that turns false |
|---:|---:|---|
| 1 | **1515** | §10 row: `` | `main.yml` has no `paths` allow-list | open, measured live | TZ-23. … | `` |
| 2 | **1645–1646** | §11 last line: ``main.yml` still has no `paths` allow-list, only `paths-ignore`, so every path nobody named fires it (inv. 52).` |
| 3 | **1314–1316** | inv. 52's closing sentence: `A `paths-ignore` list with no `paths` allow-list beside it still fires on every path nobody thought to name, which remains the shape in `main.yml` and is a separate, open matter.` |

All three are listed so the post-merge edit cannot forget one.

---

## Commit

**Implementation commit — made and pushed before this report was written, so its hash is
a measurement:**

```
5fc2da5f8e5790bc0106f116a717a0ffa784c37c
Claude Code Executor <diva_ps5@yahoo.com>

ci(main): replace paths-ignore with a derived literal paths allow-list (TZ-23)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Subject line verbatim from the TZ's `## Commit Message`. Contents: one file,
`.github/workflows/main.yml`, 19 insertions and 13 deletions in a single hunk. Nothing
else is in the commit — no scratch file, no cache, no generated artifact.

**This report's own commit** carries the message

```
docs(report): TZ-23 derived literal paths allow-list for main.yml
```

and goes direct to `main` on the `CryptoReports/**` path (contract §8). It has not
happened at the time this section is written, so it carries no hash, no conclusion and no
push result.

---

## Pull Request

**No pull request exists.** `gh` is not installed in this session and no GitHub token is
present (`command -v gh` → not found; `GH_TOKEN` and `GITHUB_TOKEN` both unset), so the
environment cannot open one. Contract §8's fallback applies.

- **Branch:** `claude/tz-23-main-workflow-paths-allowlist`
- **Compare URL:** https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-23-main-workflow-paths-allowlist

The branch is pushed and the Boss opens and merges from that link in one action, after
the Architect's verdict.

---

## CI Execution

**No workflow ran under this session's control, and this session cannot read runner
results** — no `gh`, no token, no GitHub API access (map §10, contract §9). Only what is
established is stated here.

Established:

- The branch reached the remote. `git push -u origin claude/tz-23-main-workflow-paths-allowlist`
  exited 0, and `git rev-parse origin/claude/tz-23-main-workflow-paths-allowlist` reads
  `5fc2da5f8e5790bc0106f116a717a0ffa784c37c`.
- **The pushed path clears `bench.yml`'s filters.** That workflow's `push` trigger is
  `branches: [ main, 'claude/**' ]`, which covers this branch name, and its
  `paths-ignore` — `journal/data/**`, `journal/out/**`, `journal/runs.jsonl`,
  `analyst/state.json`, `analyst/live.json`, `analyst/log/**`, `**.md` — is evaluated
  against this branch's only changed path, `.github/workflows/main.yml`, and matches
  none of the seven.
- **The pushed path cannot clear `main.yml`'s own filters**, in either the old shape or
  the new one, because its `push` trigger is `branches: [ main ]` and this is a
  `claude/**` branch. `Crypto Update` is not reachable from this push at all.

Not established, and deliberately not asserted: whether `Bench gate` executed on the
runner, its run id, and its conclusion. That reading belongs to the audit and to the
actor who opens the pull-request page to merge (contract §9).

**Post-merge evidence — §6, PENDING, stated as pending and not as observed.** Two
readings settle this change and both are taken from the Actions page after the merge:

- the merge commit produced exactly one `Crypto Update` run — the must-fire direction,
  live. The merge commit changes `.github/workflows/main.yml`, which is in the
  allow-list, so this run is the control firing for real and is the expected result, not
  a leak through the new filter;
- the next push touching only `.md` or `catalysts.json` produced none — the must-not-fire
  direction, live.

Neither has been observed by this session.

---

## Final Repository State

**The branch `claude/tz-23-main-workflow-paths-allowlist`, pushed to `origin` at
`5fc2da5f8e5790bc0106f116a717a0ffa784c37c` before this report was written.** It is one
commit ahead of `origin/main` at `deb788fb0fe861f3d5802393bf55e4904dd393a7`, and that
commit changes one file.

Working tree at the branch tip: clean. `git status --porcelain --untracked-files=all`
lists nothing — no scratch file, no duplicate, no superseded copy. Every artifact this
session produced for measurement (the pristine `origin/main` extract, the gate logs, the
evaluator, the baseline copy of the workflow) was written under `/tmp`, outside the
repository, and none is tracked.

**NOT IN EFFECT UNTIL MERGED.** Until the Boss merges, `main.yml` on `main` still carries
the `paths-ignore` list, and every path nobody named still starts the bot.

---

## Fingerprints

Measured at the branch tip, `5fc2da5f8e5790bc0106f116a717a0ffa784c37c`.

**System Map** — `SYSTEM-MAP-CRYPTOCALCUL.md`, revision string from its `## 0.
Fingerprint` block: `**Revision 2026-08-30-f.**`

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1664 | `8bd9e075b786f199b083346c41617382` |

**Files the map's `## 0` table lists at this revision** — all four match the values the
table requires:

| File | Lines | MD5 | Required by map |
|---|---:|---|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | match |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

**Contracts read this session** (the TZ's second gate names the first):

| File | Lines | MD5 |
|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` (**Version 15**) | 693 | `3d73f4ddbf3bdb8eb0b94547c101b6a0` |
| `ANALYST-INSTRUCTIONS.md` | 783 | `a5c9218fe1745882b4baaadd48797109` |

**The file this TZ writes, before and after:**

| File | Lines | MD5 |
|---|---:|---|
| `.github/workflows/main.yml` — before (`origin/main`, `deb788f`) | 51 | `bbba090ebaa8d0f9c7c3530fd4bd7674` |
| `.github/workflows/main.yml` — after (branch tip) | 57 | `4d3a83651f7d3a57da19609b9894118e` |

**Read but not written, fingerprinted because §5 item 8 and `## CI Execution` rest on
it:**

| File | Lines | MD5 |
|---|---:|---|
| `.github/workflows/bench.yml` | 135 | `ece76785638496963a2ea068d6a1b9df` |
