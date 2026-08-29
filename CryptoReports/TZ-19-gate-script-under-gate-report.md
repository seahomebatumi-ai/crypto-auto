# Implementation Report — TZ-19

Return `live-gate.sh` to its own control.

## Status

**COMPLETED.**

One file changed, exactly as `## Scope` authorises. Every validation item in TZ-19 §4
ran and passed, including the one the TZ names as the acceptance evidence: a real push
touching only `analyst/live-gate.sh` started `Bench gate` on the hosted runner, which
before this change it did not.

**Predecessor state.** TZ-18 is merged. Implementation commit `8f45ea8` reached `main`
through pull request #18 (merge commit `4af139a`), and `CryptoReports/TZ-18-gate-floor-and-md-filter-report.md`
is on `main`. This work is therefore built on a merged base, not on an unmerged branch.

## Inbound Filing

**Nothing to move.** The Boss's upload landed at the canonical path already:
`CryptoTZ/TZ-19-gate-script-under-gate.md`, matching the filename the TZ header states.
No `git mv`, no mangled copy, no duplicate.

The session clone required two repairs from contract §3 before anything could be
assessed, both performed and both recorded here because they are exactly the traps §3
names:

| Condition | Command | Result |
|---|---|---|
| clone was **shallow** | `git rev-parse --is-shallow-repository` | printed `true` → `git fetch --unshallow` → now `false` |
| session snapshot predated the upload | `git fetch --all --prune` | `origin/main` at `2c39e9c`, four commits ahead of the local `main` ref (`5dfc469`) |

The branch `claude/execute-tz-19-1q23dl` was created from `origin/main` at `2c39e9c`.

## Scope Executed

| Path | Change | Status |
|---|---|---|
| `.github/workflows/bench.yml` | `on.push.paths-ignore`: `- 'analyst/**'` replaced by a two-line comment and three narrower entries | done |

Nothing else. `main.yml` untouched, as TZ §2 requires. No file created, renamed or deleted.

## Files Created

None.

## Files Modified

`.github/workflows/bench.yml` — one hunk, 5 insertions, 1 deletion.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

TZ-17 placed `'analyst/**'` in `bench.yml`'s `push.paths-ignore` so that an analysis run
saving its own state would not burn a 13-step gate. That is correct for the analyst's
**data**. `analyst/live-gate.sh` lives in the same tree and is not data — it is code whose
control is gate step 13. Under the old filter, a commit changing only the gate script did
not run the gate that proves the gate: the shape inv. 37 names, and invisible, because the
workflow that would have complained is the one that does not start.

The repair names the analyst's *written* paths instead of its directory:

```yaml
    paths-ignore:
      - 'journal/data/**'
      - 'journal/out/**'
      - 'journal/runs.jsonl'
      # Данные аналитика: состояние, журнал и payload от шортката.
      # Скрипт шлюза сюда не входит намеренно — его контроль это шаг 13.
      - 'analyst/state.json'
      - 'analyst/live.json'
      - 'analyst/log/**'
      - '**.md'
```

The entries are in the order and the position TZ §3 specifies. The comment is present and
its second line is the load-bearing one: it is the only place a future reader learns that
the omission of `live-gate.sh` is deliberate rather than an oversight (inv. 50).
`analyst/README.md` gets no entry because `'**.md'`, added by TZ-18, already covers it —
verified below rather than assumed.

## Validation

All seven items of TZ-19 §4 ran. None was skipped and none was "not applicable".

### 0. System Map fingerprint gate (contract §5) — PASSED, blocking

All seven anchors matched as exact substrings against the repository copy of
`SYSTEM-MAP-CRYPTOCALCUL.md`:

```
PRESENT '**Revision 2026-08-29-b.**'
PRESENT '### 3.12 Direction engine — veto cascade'
PRESENT '### 3.15 Catalyst registry'
PRESENT '### 3.16 List exhaustion — the day-range measure'
PRESENT '## 11. Analytical engine'
PRESENT "### 3.17 «РИСК ВЫНОСА» — the day's own risk"
PRESENT '52. **A filter is measured on the runner, never derived from the pattern.**'
anchors checked: 7 present: 7
```

Revision string found = revision string required = `Revision 2026-08-29-b`. All four files
in the map's `## 0` table match their stated line count and MD5 exactly — see
`## Fingerprints`. No file is ahead of the map in either direction, so there is nothing to
report under §5's "do not act on the difference" clause.

### 1. Filter evaluation, both directions, from a real changed-file list

**Method**, reusing the TZ-18 report's evaluator and throwaway-clone technique:

- A throwaway clone was made in the scratchpad at `2c39e9c`, so the real working tree was
  never contaminated and `git diff --name-only` returns exactly the probe's files.
- For each row the files were **really modified** in that clone (`git add -N` for the one
  that does not yet exist), and **the changed-file list was read from
  `git diff --name-only`, never typed**:

```
analyst/live-gate.sh::analyst/live-gate.sh
analyst/state.json::analyst/state.json
analyst/live.json::analyst/live.json
analyst/log/2026-08-29.md::analyst/log/2026-08-29.md
analyst/README.md::analyst/README.md
analyst/state.json + analyst/live-gate.sh::analyst/live-gate.sh,analyst/state.json
main.py::main.py
```

- The `paths-ignore` list is **parsed out of the committed YAML with a YAML parser**
  (PyYAML), so what is tested is what is committed, not what was intended.
- GitHub's decision rule is applied: a push starts the workflow when at least one changed
  file matches **no** pattern in `paths-ignore`.
- BEFORE is the YAML at `main` (`git show origin/main:.github/workflows/bench.yml`);
  AFTER is the YAML on the branch.
- Two readings of `**` are computed side by side, as TZ-18 did — **seg** (`**/` may match
  zero directories) and **chr** (`**` is plain "any characters"). This is a filter
  evaluation, not a live run; item 3 supplies the live run.

**`bench.yml`** — before: `['journal/data/**', 'journal/out/**', 'journal/runs.jsonl', 'analyst/**', '**.md']`;
after: `['journal/data/**', 'journal/out/**', 'journal/runs.jsonl', 'analyst/state.json', 'analyst/live.json', 'analyst/log/**', '**.md']`.

| Changed files | before | after | TZ §4 required | |
|---|---|---|---|---|
| `analyst/live-gate.sh` | NOT RUN | **RUNS** | must RUN | ✓ |
| `analyst/state.json` | NOT RUN | NOT RUN | must NOT run | ✓ |
| `analyst/live.json` | NOT RUN | NOT RUN | must NOT run | ✓ |
| `analyst/log/2026-08-29.md` | NOT RUN | NOT RUN | must NOT run | ✓ |
| `analyst/README.md` | NOT RUN | NOT RUN | must NOT run | ✓ |
| `analyst/state.json` + `analyst/live-gate.sh` | NOT RUN | **RUNS** | must RUN | ✓ |
| `main.py` | RUNS | **RUNS** | must RUN | ✓ |

**seg and chr agree on all seven rows, before and after.** No pattern in this filter is
read two ways, so the ambiguity TZ-17 §Risk 5 recorded does not reappear here.

Row 1 is the repair. Rows 2–5 are the property that had to survive it. Row 6 proves a
mixed commit is not swallowed — GitHub skips only when *every* changed file is ignored.
Row 7 is the control that a filter matching nothing would fail. 112 pattern comparisons
were performed on the AFTER list, 80 on the BEFORE list; the evaluator fails on zero
comparisons (inv. 22).

**Per-pattern attribution, cross-checked against git's own wildmatch** in a throwaway
repository whose `.gitignore` is the single pattern under test:

```
### git wildmatch, .gitignore = analyst/state.json
  unmatched analyst/live-gate.sh      MATCHED   analyst/state.json
  unmatched analyst/live.json         unmatched analyst/log/2026-08-29.md
  unmatched analyst/README.md         unmatched main.py
### git wildmatch, .gitignore = analyst/live.json
  MATCHED   analyst/live.json ; every other probe file unmatched
### git wildmatch, .gitignore = analyst/log/**
  MATCHED   analyst/log/2026-08-29.md ; every other probe file unmatched
### git wildmatch, .gitignore = **.md
  MATCHED   analyst/log/2026-08-29.md   MATCHED   analyst/README.md
  unmatched analyst/live-gate.sh, analyst/state.json, analyst/live.json, main.py
### git wildmatch, .gitignore = analyst/**
  MATCHED   analyst/live-gate.sh  <-- the defect TZ-19 repairs
  MATCHED   everything else under analyst/ ; unmatched main.py
```

Three facts fall out of this that the row table alone does not show. `analyst/README.md`
is caught by `'**.md'` alone, confirming TZ §3's claim that it needs no entry of its own.
`analyst/log/2026-08-29.md` is caught twice, by `analyst/log/**` and by `'**.md'` — so the
`analyst/log/**` entry is not redundant, because it is the only one that would catch a day
log that is not Markdown. And `analyst/live-gate.sh` is matched by the old `analyst/**`
and by none of the three replacements, which is the whole change in one line.

### 1b. Negative test on the evaluator (contract §9 — a gate never proven to fail is not a gate)

The evaluator was run against three mutated copies of the AFTER YAML, to prove it
discriminates rather than returning a constant:

| Mutation | Expected | Observed |
|---|---|---|
| **A1** — reinstate the defect: `analyst/**` back in place of the three entries | row 1 flips back to NOT RUN | row 1 **NOT RUN**, rows 2–6 NOT RUN, row 7 RUNS — the TZ-17 behaviour reproduced exactly |
| **A2** — `paths-ignore: ['**']` | every row NOT RUN | all seven **NOT RUN**, `main.py` included |
| **A3** — `paths-ignore: ['no/such/path']` | every row RUNS | all seven **RUNS** |

A1 is the important one: it reproduces the precise defect being repaired, so the AFTER
result is a measured difference and not an artefact of the evaluator.

### 2. The same seven rows against `main.yml`, which must not move

| Changed files | before | after |
|---|---|---|
| `analyst/live-gate.sh` | NOT RUN | NOT RUN |
| `analyst/state.json` | NOT RUN | NOT RUN |
| `analyst/live.json` | NOT RUN | NOT RUN |
| `analyst/log/2026-08-29.md` | NOT RUN | NOT RUN |
| `analyst/README.md` | NOT RUN | NOT RUN |
| `analyst/state.json` + `analyst/live-gate.sh` | NOT RUN | NOT RUN |
| `main.py` | **RUNS** | **RUNS** |

Identical before and after, on every row, under both readings, as TZ §4 item 2 requires.
The parsed pattern list is byte-identical in both directions
(`['bench/**', '**.md', 'index.html', '.github/workflows/bench.yml', '.github/workflows/backtest_bench.yml', 'analyst/**']`),
and `git diff origin/main -- .github/workflows/main.yml` is empty. A `bench.yml` change
that altered `main.yml`'s behaviour would have meant the evaluator was reading the wrong
file; it was not.

### 3. Runner evidence — the acceptance evidence (inv. 52)

A filter is measured on the runner, never derived from the pattern. Three real pushes to
`claude/execute-tz-19-1q23dl`:

| # | Commit | Files in the push | `Bench gate` | Run | Conclusion |
|---:|---|---|---|---|---|
| 1 | `cc8bade` | `.github/workflows/bench.yml` only | started | [`33254327296`](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33254327296) (run #102) | **success** |
| 2 | `2aa3089` | **`analyst/live-gate.sh` only** | **started** | [`33254342462`](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33254342462) (run #103) | **success** |
| 3 | `7fb4cdd` | `analyst/live-gate.sh` only | started | [`33254360369`](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33254360369) (run #104) | **success** |

**Row 2 is the acceptance evidence.** Commit `2aa3089` added two comment lines to
`analyst/live-gate.sh` and touched nothing else — `git show --stat` reads
`analyst/live-gate.sh | 2 ++`, one file changed. It was pushed alone, so the push's
changed-file set is exactly that one path. `Bench gate` started for it and ran all
thirteen steps, step 13 (`live-gate.sh --selftest`) included. Under the filter at `main`
this push would have started nothing at all; that is the defect, measured on the runner
rather than argued from the pattern.

Commit `7fb4cdd` removed those two lines again, leaving `analyst/live-gate.sh`
**byte-identical to the first commit and to `main`** — verified below and in
`## Fingerprints`. The pair exists only to produce the measurement TZ §4 item 3 requires;
their net effect on the branch is zero, and `git diff --stat origin/main..HEAD` reads one
file.

`Crypto Update` (`main.yml`) did not run for any of the three, and could not have: its
push trigger is `branches: [main]`, so a `claude/**` branch is outside it before
`paths-ignore` is ever consulted. Item 2's `main.yml` rows therefore rest on the filter
evaluation, and this is stated rather than glossed — see `## Remaining Risks` 1.

### 4. Full gate, 13 steps, per-step counter table

Run locally against the branch working tree, and independently on the hosted runner in
run `33254327296`. **The two agree on every counter**, so the table below is one column,
not two:

| Step | Bench | Checks | Runner |
|---:|---|---:|---|
| 1 | `verify_board.js` | 109 | success |
| 2 | `board2_bench.js` | 130 | success |
| 3 | `prot_bench.js index.html` | 372 | success |
| 4 | `verify_bench.py` | 35 | success |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | success |
| 6 | `fresh_bench.js` | 3 424 | success |
| 7 | `journal_bench.js` | **691 109** | success |
| 8 | `catalyst_bench.js` | 23 040 | success |
| 9 | `display_bench.py` | 24 598 | success |
| 10 | `render_bench.py` | 15 925 | success |
| 11 | `direction_bench.py --display` | 15 629 | success |
| 12 | `exhaustion_bench.js` | **220 598** | success |
| | **steps 1–12** | **1 250 677** | required 1 250 677 ✓ |
| 13 | `live-gate.sh --selftest` | **40** | required 40 ✓ |
| | **total** | **1 250 717** | required 1 250 717 ✓ |

**Nothing moved.** Steps 1–12 sum to 1 250 677, step 13 reads 40, the total is 1 250 717 —
each identical to the §0 fingerprint. Step 7 is at 691 109 and step 12 at 220 598, both
unmoved through TZ-17, TZ-18 and now TZ-19, which for a change writing no production file
is the required result. Every number above is a bench's own printed counter, a sum of
per-comparison counters and never an estimate (inv. 43). All thirteen steps exited 0
locally and are `success` on the runner.

### 4b. Negative test on the gate itself (contract §9)

A CI-touching TZ requires a forced failure. Step 13 is the control this change restores to
the gate, so it is the step worth proving can fail:

```
MD5 before plant: 3e15ec4265a7a17b36677948012b79ea
planted: LIVE_MAX_AGE_SEC = 900  ->  LIVE_MAX_AGE_SEC = 99999999
$ bash analyst/live-gate.sh --selftest
exit=1                                    <-- non-zero, the job would turn red
checks=40
selftest: 3 assertion(s) failed
$ git checkout -- analyst/live-gate.sh
MD5 after revert: 3e15ec4265a7a17b36677948012b79ea    (identical)
$ bash analyst/live-gate.sh --selftest
exit=0
checks=40
selftest: 14 cases, all exit codes as specified
$ git status --porcelain
 M .github/workflows/bench.yml            <-- the one intended file, nothing else
```

The planted defect loosened the freshness ceiling so the stale-payload cases stop failing;
three assertions caught it. The step **printed the failure and returned non-zero** — it did
not exit 0 with a complaint on screen, which would itself be a defect (inv. 25, 29). The
counter still read 40 with the defect planted, which is correct: it counts comparisons
performed, not comparisons passed. The revert restored the exact MD5 and the tree is clean.

### 5. `git diff --stat` and the diff

```
 .github/workflows/bench.yml | 6 +++++-
 1 file changed, 5 insertions(+), 1 deletion(-)
```

Exactly one file, as TZ §6 acceptance criterion 5 requires. The diff in full:

```diff
diff --git a/.github/workflows/bench.yml b/.github/workflows/bench.yml
index 154a784..3543bab 100644
--- a/.github/workflows/bench.yml
+++ b/.github/workflows/bench.yml
@@ -26,7 +26,11 @@ on:
       - 'journal/data/**'
       - 'journal/out/**'
       - 'journal/runs.jsonl'
-      - 'analyst/**'
+      # Данные аналитика: состояние, журнал и payload от шортката.
+      # Скрипт шлюза сюда не входит намеренно — его контроль это шаг 13.
+      - 'analyst/state.json'
+      - 'analyst/live.json'
+      - 'analyst/log/**'
       - '**.md'
   pull_request:
```

The file still parses as YAML and the trigger block reads as intended:

```json
{"push": {"branches": ["main", "claude/**"],
          "paths-ignore": ["journal/data/**", "journal/out/**", "journal/runs.jsonl",
                           "analyst/state.json", "analyst/live.json", "analyst/log/**",
                           "**.md"]},
 "pull_request": null}
```

### 6. The four files in §0 — unchanged

Measured on the branch; every line count and MD5 identical to the map's `## 0` table. See
`## Fingerprints`. `git diff origin/main` is empty for all four.

### 7. Map, contracts and `live-gate.sh`

All in `## Fingerprints`. **`analyst/live-gate.sh` is byte-identical to `main`**:
`git diff --quiet origin/main -- analyst/live-gate.sh` returns 0, and its MD5 on the branch
head is `3e15ec4265a7a17b36677948012b79ea`, the same value it carries on `main` and the
same value it carried before and after the negative test of item 4b.

No analysis was run and `analyst/live.json` was not touched, as TZ §4 instructs.

## Test Results

| Item | TZ §4 | Result |
|---|---|---|
| Fingerprint gate | contract §5 | **PASS** — 7/7 anchors, 4/4 files, revision matches |
| Filter evaluation, `bench.yml`, 7 rows, both directions | 1 | **PASS** — all 7 match the required table |
| Evaluator negative test, 3 mutations | §9 | **PASS** — discriminates in all three |
| Filter evaluation, `main.yml`, 7 rows | 2 | **PASS** — identical before and after |
| Runner evidence, script-only push starts the gate | 3 | **PASS** — run `33254342462`, success |
| Full gate, 13 steps, counters | 4 | **PASS** — 1 250 677 / 40 / 1 250 717, unmoved |
| Gate negative test, step 13 forced red | §9 | **PASS** — exit 1, reverted byte-identical |
| `git diff --stat` = one file | 5 | **PASS** |
| §0 four files unchanged | 6 | **PASS** |
| `live-gate.sh` byte-identical to `main` | 7 | **PASS** |

Ten items, ten passes, none skipped.

## Deviations

**1. Two commits on the branch touch `analyst/live-gate.sh`, which `## Scope` does not
list.** They are `2aa3089` (adds two comment lines) and `7fb4cdd` (removes them). This is
not scope creep: TZ §4 item 3 requires exactly this — "push a **second** commit to the
branch touching `analyst/live-gate.sh` and nothing else — a comment line added and then
removed is sufficient, leaving the file byte-identical to the first commit". The
requirement is met precisely: the file at branch head is byte-identical to `main`, and the
branch's net diff against `main` is the single authorised file. Recorded here so the
Architect sees three commits and no surprise.

**2. The required comment is Russian while contract §Language says comments are English.**
TZ §3 specifies the two comment lines verbatim and calls the second load-bearing, so it was
inserted exactly as written. This is the right resolution — every existing comment in
`bench.yml` and `main.yml` is Russian, and an English insertion would have been the odd one
out in the file a future reader is reading — but the tension between the contract's language
rule and the workflow files' established practice is a genuine one and is routed to the
Architect here rather than decided silently. No code behaviour depends on it.

No other deviation. The change is the one TZ §3 specifies, in the order and position it
specifies.

## Pre-existing Issues

**1. `analyst/live.json` carries a known producer defect.** Recorded in the TZ-18 report
under `## Pre-existing Issues` 1 and being fixed at the Shortcut, outside the repository.
TZ-19 §4 instructs that no analysis be run and the file not be touched; it was not read,
written or validated in this task. Its MD5 is unchanged from `main`.

**2. `prot_bench.js` reports a NaN in «ГРАНИЦЫ СДЕЛКИ» at E = 0.** The bench prints this
itself, on the runner and locally:

```
PRE-EXISTING (not TZ-12, present on origin/main): at E = 0 the board prints NaN
in «ГРАНИЦЫ СДЕЛКИ» — Math.abs(liq / E - 1).
```

It is annotated as pre-existing by the bench and does not fail the step. Not caused by this
task, not fixed here (§12), and repeated in this report only because a defect that lives
only inside a passing bench's stdout is easy to stop seeing.

Neither issue was acted on.

## Remaining Risks

**1. Acceptance criterion 2 has no runner evidence, only filter evaluation.** That a push
touching only `analyst/state.json`, `analyst/live.json` or `analyst/log/**` still starts
neither workflow is proven by the evaluator and by git's wildmatch, not by a real run —
because producing that evidence would require an implementation run to write under
`analyst/`, which §2 assigns to role 2 and which `## Scope` does not authorise. This is the
weaker half of the pair by construction, and it is the safe half: its failure mode is
spending runner minutes, not losing a control. **The first real analyst commit after this
merges supplies the missing measurement at zero cost** — if `Bench gate` starts for it, the
filter is wrong and that is immediately visible.

**2. The deny-list is still a deny-list, and it is now narrower.** Any *new* data file
added under `analyst/` — a second payload, a cache, a scratch artifact from the Shortcut —
will now **start** the gate until someone adds it to the list, where before it was silently
covered by `analyst/**`. That is the inverse of the defect just repaired and it is the
direction worth failing in: it costs runner minutes and is loudly visible, whereas the old
failure cost a control and was invisible. But it is a real behavioural change, and the
comment in the file does not warn about it. Worth a line in the map or in
`ANALYST-INSTRUCTIONS.md` if the analyst's written set is ever extended.

**3. No `paths` allow-list.** Standing matter, recorded in inv. 52 and in TZ §7 as
deliberately not done: converting a deny-list to an allow-list changes the trigger for
every path in the repository at once and needs a TZ that enumerates them. Unchanged by this
work; noted so it stays on the queue.

**4. `main.yml` keeps `'analyst/**'`, so a gate-script commit does not start the bot.**
Deliberate per TZ §7 and correct — `main.py` does not read the script, and starting the bot
would redraw 28 coins through CoinGecko and rewrite the live Gist for no benefit. Recorded
because the two workflows now treat the same tree differently on purpose, and a future
reader who notices the asymmetry should find it explained rather than suspicious.

**5. The evaluator is a reimplementation of GitHub's documented semantics,** not GitHub.
This risk is materially smaller than it was for TZ-18: the decisive row of this TZ is
settled by three real runs on the hosted runner, and the evaluator's role is reduced to the
rows that must *not* run. Its agreement with git's wildmatch on every pattern in the list,
and the agreement of its two `**` readings on every row, are corroboration rather than
proof.

## Commit

Three commits on `claude/execute-tz-19-1q23dl`, off `origin/main` at `2c39e9c`:

| Commit | Message | Files |
|---|---|---|
| `cc8bade` | `fix(ci): narrow bench.yml analyst ignore so the gate script runs its own gate (TZ-19)` | `.github/workflows/bench.yml` |
| `2aa3089` | `test(ci): TZ-19 probe commit touching only analyst/live-gate.sh` | `analyst/live-gate.sh` (+2) |
| `7fb4cdd` | `test(ci): remove TZ-19 probe line, restoring analyst/live-gate.sh byte-for-byte` | `analyst/live-gate.sh` (−2) |

The first carries the string from TZ `## Commit Message` verbatim. The second and third are
the runner measurement TZ §4 item 3 requires; they cancel exactly, and the branch's net diff
against `main` is one file:

```
 .github/workflows/bench.yml | 6 +++++-
 1 file changed, 5 insertions(+), 1 deletion(-)
```

This report is committed directly to `main` per contract §8, not to the branch.

## Pull Request

**No pull request exists.** This session does not open one without an explicit instruction,
and the TZ does not give one; per contract §8 that is a fallback, not a blocker.

- **Branch:** `claude/execute-tz-19-1q23dl`
- **Compare URL:** https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-19-1q23dl

The Boss opens and merges from that link in one action, after the Architect's verdict.
Runner evidence exists for the branch independently of any pull request — see below.

## CI Execution

Ran on GitHub's hosted runners, not locally replayed. `Bench gate` fires on push to
`claude/**` (contract §9), so the branch has runner evidence with no pull request open.

| Run | Head | Trigger | Steps | Conclusion |
|---|---|---|---|---|
| [`33254327296`](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33254327296) (#102) | `cc8bade` | push, `bench.yml` only | 13/13 ran | **success** |
| [`33254342462`](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33254342462) (#103) | `2aa3089` | push, `analyst/live-gate.sh` only | 13/13 ran | **success** |
| [`33254360369`](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33254360369) (#104) | `7fb4cdd` | push, `analyst/live-gate.sh` only | 13/13 ran | **success** |

Every one of the thirteen bench steps executed in runs #102 and #103 — job step 18,
`Ворота живых данных аналитика (live-gate.sh --selftest)`, included — and each reported
`success`. The runner's own printed counters for run #102 match the local run exactly, step
for step, ending at `checks=40` and `selftest: 14 cases, all exit codes as specified`.

**Run #103 is the evidence this TZ exists to produce**, and its existence is the finding:
before this change, a push carrying only `analyst/live-gate.sh` produced no run at all.

`Crypto Update` (`main.yml`) executed for none of the three commits, as expected — its push
trigger is `branches: [main]` and this work is on a `claude/**` branch. `backtest_bench.yml`,
`calib.yml` and `journal.yml` were not triggered and were not touched.

## Final Repository State

- `main` is at `2c39e9c` and is **not** modified by this work, except that this report is
  added to it under `CryptoReports/` per contract §8.
- The implementation lives on `claude/execute-tz-19-1q23dl` at `7fb4cdd`, one file ahead of
  `main`.
- Working tree clean; no scratch file, generated artifact or duplicate committed. All probe
  material (the throwaway clone, the evaluator, the wildmatch repositories, the mutated
  YAMLs) lives in the session scratchpad, outside the repository.
- `analyst/live-gate.sh`, `index.html`, `main.py`, `catalysts.json`,
  `bench/exhaustion-calibration.txt`, `SYSTEM-MAP-CRYPTOCALCUL.md` and
  `.github/workflows/main.yml` are byte-identical to `main`.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Measured on the branch head `7fb4cdd`.

**System Map** — `Revision 2026-08-29-b`, the revision TZ-19 §0 requires. Gate: PASSED,
7/7 anchors matched as exact substrings.

| File | Lines | MD5 | vs required |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1489 | `0a7bb952d0a765e24e96b4723bc91535` | reported, not enforced |

**The map's `## 0` file table** — every entry matches the required line count and MD5:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | ✓ identical |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | ✓ identical |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` | ✓ identical |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | ✓ identical |

**Contracts and the files TZ §4 item 7 adds:**

| File | Lines | MD5 | Version / note |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 590 | `3d810ec57716e7d2e5afda49d95db662` | **Version 10** — TZ-19 requires 10 or later ✓ |
| `ANALYST-INSTRUCTIONS.md` | 627 | `722e5e4c41c1ab443a0ebec32bc122ce` | schema v1 |
| `analyst/live-gate.sh` | 444 | `3e15ec4265a7a17b36677948012b79ea` | **byte-identical to `main`** ✓ |

**The file this TZ changes, and the one it must not:**

| File | Lines | MD5 | |
|---|---:|---|---|
| `.github/workflows/bench.yml` | 135 | `ece76785638496963a2ea068d6a1b9df` | changed (was 131 lines, `461c0d2042d75c8859450eab656064f9`) |
| `.github/workflows/main.yml` | 51 | `bbba090ebaa8d0f9c7c3530fd4bd7674` | unchanged from `main` ✓ |

**Gate at this revision:** `bench.yml`, 13 steps, **1 250 717 checks**, green on the hosted
runner (run `33254327296`, head `cc8bade`, all 13 steps `success`). Step 13 reads **40**;
steps 1–12 sum to **1 250 677**, step 7 at **691 109**, step 12 at **220 598** — unmoved
through TZ-17, TZ-18 and TZ-19.
