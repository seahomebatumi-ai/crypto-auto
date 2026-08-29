# Implementation Report — TZ-18

## Status

**COMPLETED**, with one finding the Architect must read before accepting: **Change B's
stated premise is refuted by production evidence.** Both changes in `## Scope` were
implemented exactly as specified, the full validation list ran, and the hosted gate is
green over 13 steps. But `'**/*.md'` *does* match root-level Markdown on GitHub's own
runner — measured, not argued — so the `main.yml` half of Change B is behaviour-neutral
rather than the defect repair TZ-18 §3 describes. The `bench.yml` half is a real new
exclusion and delivers exactly the saving the TZ claims for it. Details under
`## Deviations`.

The previous TZ's branch **was merged**: TZ-17 landed on `main` as `60bfcb2` (implementation
commit `850e263`). This work is built on a merged base.

---

## Inbound Filing

None. `CryptoTZ/TZ-18-gate-floor-and-md-filter.md` arrived under its canonical filename
in its canonical directory (commit `72a959a`, "Add files via upload"). Nothing was moved,
renamed or de-duplicated.

---

## Scope Executed

| Path | Change | State |
|---|---|---|
| `analyst/live-gate.sh` | check 3 becomes a two-sided window; two new constants; two new selftest cases | done |
| `.github/workflows/main.yml` | `'**/*.md'` → `'**.md'` | done |
| `.github/workflows/bench.yml` | `'**.md'` added to `push.paths-ignore` | done |

Nothing else was touched. No analysis was run, and `analyst/live.json` was neither
created nor modified — it already exists on `main`, delivered by the Boss at `386cb51`.

## Files Created

None.

## Files Modified

`analyst/live-gate.sh`, `.github/workflows/main.yml`, `.github/workflows/bench.yml`.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Change A — the freshness window gets a floor (inv. 51)

Check 3 was `age > 900 → E_STALE`, a one-sided test that every payload stamped in the
future satisfies. The window now has both bounds:

```
LIVE_MAX_AGE_SEC = 900   # ceiling: how far behind now the payload may be, in seconds
LIVE_SKEW_SEC = 120      # floor: how far ahead of now the producer may plausibly be

check 3 passes  <=>  -LIVE_SKEW_SEC <= (now - ts) <= LIVE_MAX_AGE_SEC
```

Both constants are declared once, at lines 52–53 of the script, immediately after the
exit-code names. Neither number is written at a comparison site; both comparison sites
(lines 138 and 142) and both failure messages read the constant. The exit code stays **3**
on both sides, and the two stderr lines name the side:

```
live-gate: check 3: payload is stale, age 960 s exceeds the 900 s ceiling
live-gate: check 3: payload is ahead of now, age -121 s is below the -120 s floor
```

`age_sec` in the success payload keeps its sign convention and is not clamped: the direct
control at +60 s returned `"age_sec":-60`.

The new floor comparison is counted at its site (inv. 43), so the success payload's
`checked` moves 153 → 154. That number is a measurement of the validator's own work and
is not asserted anywhere; the selftest asserts the *shape* of the stdout object, not its
values.

Two selftest cases were added, generated the same way as every other fixture — the
document is built from the live `tokens[]` parse and only `ts` differs:

| case | ts | expected exit |
|---|---|---|
| `future121` | now + 121 s | 3 |
| `future_ok` | now + 60 s | 0 |

Both stamps are written in UTC (`+00:00`). The selftest passes its single clock to the
gate explicitly rather than letting the gate re-read one, so the two cases straddle the
floor by exactly one second deterministically. The `+04:00` offset path stays exercised
by the pre-existing `stale16` case, which is untouched.

### Change B — `'**.md'`

`main.yml`: `- '**/*.md'` replaced by `- '**.md'`, same list, same position, every other
entry, comment and line untouched. `bench.yml`: `- '**.md'` appended to
`push.paths-ignore`. Both diffs are one line; `bench.yml`'s step 13 was not touched, and
the `checks=N` it prints exists only at run time, never in the YAML.

---

## Validation

Every item of TZ-18 §4 was run. Nothing was skipped.

### 1. `bash -n analyst/live-gate.sh`

```
$ bash -n analyst/live-gate.sh; echo $?
0
```

Clean, before and after.

### 2. `--selftest` exits 0; `checks=N`; N > 35, delta attributed

Baseline, on unmodified `HEAD` before any edit:

```
checks=35
selftest: 12 cases, all exit codes as specified
exit=0
```

After:

```
  fresh                exit=0 expected=0
  stale16              exit=3 expected=3  live-gate: check 3: payload is stale, age 15360 s exceeds the 900 s ceiling
  future121            exit=3 expected=3  live-gate: check 3: payload is ahead of now, age -121 s is below the -120 s floor
  future_ok            exit=0 expected=0
  … ten pre-existing cases, all unmoved …
checks=40
selftest: 14 cases, all exit codes as specified
exit=0
```

**35 → 40, +5, attributed term by term.** The selftest scores three assertions per
failing case (exact exit code · stdout empty · exactly one stderr line) and two per
passing case (exact exit code · stdout is one `{ts,age_sec,n,checked}` object; a passing
case has no stderr line to count). So:

| case | want | assertions | delta |
|---|---|---|---|
| `future121` | 3 | exit code, stdout empty, one stderr line | **+3** |
| `future_ok` | 0 | exit code, stdout object shape | **+2** |
| | | | **+5** |

This reconciles the pre-existing 35 as well: 11 failing cases × 3 = 33, plus `fresh` × 2
= 35.

### 3. Negative control on the selftest (inv. 23)

`future_ok`'s expected exit was inverted from `0` to `3` in the case table:

```
--- selftest exit with the expectation inverted: 1 ---
FAIL future_ok            expected exit 3, got 0
FAIL future_ok            failure wrote 70 bytes to stdout, expected none
FAIL future_ok            expected one stderr line, got 0
  future_ok            exit=0 expected=3
selftest: 3 assertion(s) failed
```

Non-zero, and it names the case — three independent assertions caught it, not one.
Restored, and the file is byte-identical:

```
$ cmp live-gate.before analyst/live-gate.sh && echo "IDENTICAL (cmp exit 0)"
IDENTICAL (cmp exit 0)
$ md5sum analyst/live-gate.sh
3e15ec4265a7a17b36677948012b79ea  analyst/live-gate.sh
```

### 4. Direct control at the real entry point, payload outside the repository tree

The gate's payload path is fixed at `$ROOT/analyst/live.json`, so a mirror root was built
outside the repository — `…/scratchpad/gateroot/`, holding a copy of `live-gate.sh` and
`index.html` — and the gate was invoked with **no arguments**, the real entry point. The
payload is the market data the Boss actually delivered, with only `ts` varied (see
`## Pre-existing Issues` for the one repair the scratchpad copy needed; the repository
copy was not touched).

```
clock: 2026-08-29T12:05:41Z

--- ts at +60 s (inside the floor) ---
exit      : 0
stdout    : 70 bytes | {"ts":"2026-08-29T12:06:41+00:00","age_sec":-60,"n":29,"checked":154}
stderr    :

--- ts at +121 s (beyond the floor) ---
exit      : 3
stdout    : 0 bytes |
stderr    : live-gate: check 3: payload is ahead of now, age -121 s is below the -120 s floor

--- ts at -16 min (beyond the ceiling) ---
exit      : 3
stdout    : 0 bytes |
stderr    : live-gate: check 3: payload is stale, age 960 s exceeds the 900 s ceiling
```

All three as specified: exit 0 with a well-formed stdout object; exit 3 with **empty
stdout** and a stderr line naming the floor; exit 3 with a stderr line naming the ceiling.
The three lines are quoted above and are distinguishable — `is stale … ceiling` against
`is ahead of now … floor` — while sharing exit 3.

### 5. `900` and `120`: one declaration site each, no comparison site (inv. 20)

Performed two ways. First, a plain substring count over the whole file, with no word
boundaries at all, so nothing can hide inside a longer token:

```
$ grep -o '900' analyst/live-gate.sh | wc -l
1
$ grep -o '120' analyst/live-gate.sh | wc -l
1
```

One occurrence each in the entire file. Second, locating them and listing every site where
`age` is compared:

```
$ grep -nE '(^|[^0-9])(900|120)([^0-9]|$)' analyst/live-gate.sh
52:LIVE_MAX_AGE_SEC = 900   # ceiling: how far behind now the payload may be, in seconds
53:LIVE_SKEW_SEC = 120      # floor: how far ahead of now the producer may plausibly be

$ grep -nE 'age (>|<|>=|<=|==)' analyst/live-gate.sh
138:if age > LIVE_MAX_AGE_SEC:
142:if age < -LIVE_SKEW_SEC:
```

Both literals are at their declaration and nowhere else; both comparison sites and both
`die()` format arguments read the constant. The header's exit-code table previously
carried a bare `900` in prose (`payload is stale: now - ts > 900 s`) and now reads
`payload lies outside the freshness window, either side` — a second copy of a threshold
in a comment is the drift inv. 20 exists to prevent.

### 6. Change-B negative test — both workflows, six rows each, both directions

**Method.** A throwaway clone of the repository was made in the scratchpad, so the real
working tree was never contaminated and `git diff --name-only` returns exactly the probe's
files. For each row the files were really modified (or `git add -N`'d when new) in that
clone and **the changed-file list was read from `git diff --name-only`, never typed**. Each
list was evaluated by a small evaluator that parses `on.push.paths-ignore` out of the
workflow file **with a YAML parser** — so it tests what is committed, not what was
intended — and applies GitHub's decision rule: a push runs the workflow when at least one
changed file matches no `paths-ignore` pattern. This is a filter evaluation, not a live
run, as the TZ requires. BEFORE is the YAML committed at `72a959a`; AFTER is the YAML as
committed at `8f45ea8`.

The evaluator computes **two readings of `**`** side by side, because they disagree on
exactly one pattern in this repository and that disagreement is the whole finding:

- **seg** — `**/` may match zero directories, so `'**/*.md'` matches `README.md`.
- **chr** — `**` is plain "any characters", so `'**/*.md'` needs a literal `/`. This is
  the reading TZ-18 §3 states.

`main.yml`:

| Changed files | before (seg) | before (chr) | after (both) | TZ §3 expected after |
|---|---|---|---|---|
| `README.md` | NOT RUN | RUNS | **NOT RUN** | must NOT run ✓ |
| `ANALYST-INSTRUCTIONS.md` | NOT RUN | RUNS | **NOT RUN** | must NOT run ✓ |
| `CryptoReports/x-report.md` | NOT RUN | NOT RUN | **NOT RUN** | must NOT run ✓ |
| `analyst/state.json` | NOT RUN | NOT RUN | **NOT RUN** | must NOT run ✓ |
| `main.py` | RUNS | RUNS | **RUNS** | must RUN ✓ |
| `README.md` + `main.py` | RUNS | RUNS | **RUNS** | must RUN ✓ |

`bench.yml` (triggers on `main` **and** `claude/**`; ignore list is the three `journal/`
paths plus `analyst/**` plus the new `'**.md'`):

| Changed files | before (both readings) | after (both readings) |
|---|---|---|
| `README.md` | RUNS | **NOT RUN** |
| `ANALYST-INSTRUCTIONS.md` | RUNS | **NOT RUN** |
| `CryptoReports/x-report.md` | RUNS | **NOT RUN** |
| `analyst/state.json` | NOT RUN | **NOT RUN** |
| `main.py` | RUNS | **RUNS** |
| `README.md` + `main.py` | RUNS | **RUNS** |

Every TZ-required outcome is met. The control row (`main.py` alone) still starts both
workflows, so the exclusion is demonstrably not over-broad — a filter matching everything
would have passed the four "must NOT run" rows too. The mixed commit still starts both,
confirming GitHub's stated rule that it skips only when *every* changed file is ignored.

**`'**.md'` returns the same verdict under both readings, on every row.** That is the one
unambiguous gain of the `main.yml` half: the ambiguity TZ-17 §Risk 5 recorded is closed,
because the new pattern cannot be read two ways.

**Independent cross-check — git's own wildmatch**, in a throwaway repository whose
`.gitignore` is the single pattern under test:

```
### git wildmatch, .gitignore = **.md
  MATCHED   README.md
  MATCHED   ANALYST-INSTRUCTIONS.md
  MATCHED   CryptoReports/x-report.md
  unmatched analyst/state.json
  unmatched main.py

### git wildmatch, .gitignore = **/*.md
  MATCHED   README.md
  MATCHED   ANALYST-INSTRUCTIONS.md
  MATCHED   CryptoReports/x-report.md
  unmatched analyst/state.json
  unmatched main.py
```

The second matcher agrees with the **seg** reading on the decisive pattern, and agrees
with the evaluator exactly on `'**.md'`.

### 7. `git diff --stat`

```
 .github/workflows/bench.yml |  1 +
 .github/workflows/main.yml  |  2 +-
 analyst/live-gate.sh        | 39 ++++++++++++++++++++++++++++++++++-----
 3 files changed, 36 insertions(+), 6 deletions(-)
```

Exactly the three files in §1. Both workflow diffs are one line each:

```diff
--- a/.github/workflows/main.yml
+++ b/.github/workflows/main.yml
@@ -16,7 +16,7 @@ on:
     paths-ignore:
       - 'bench/**'
-      - '**/*.md'
+      - '**.md'
       - 'index.html'

--- a/.github/workflows/bench.yml
+++ b/.github/workflows/bench.yml
@@ -27,6 +27,7 @@ on:
       - 'journal/runs.jsonl'
       - 'analyst/**'
+      - '**.md'
   pull_request:
```

`bench.yml`'s step 13 is untouched; its `checks=N` is printed at run time and appears
nowhere in the YAML, so the counter moved nowhere in the file.

### 8. Full gate on the runner — 13 steps, per-step counters

Run **`33251833997`**, head `8f45ea8`, branch `claude/execute-tz-18-e0miv8`, job
`99098721651`, conclusion **success**, all 13 bench steps `success`.

| # | Step | checks |
|---:|---|---:|
| 1 | `verify_board.js` | 109 |
| 2 | `board2_bench.js` | 130 |
| 3 | `prot_bench.js` | 372 |
| 4 | `verify_bench.py` | 35 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 |
| 6 | `fresh_bench.js` | 3 424 |
| 7 | `journal_bench.js` | **691 109** |
| 8 | `catalyst_bench.js` | 23 040 |
| 9 | `display_bench.py` | 24 598 |
| 10 | `render_bench.py` | 15 925 |
| 11 | `direction_bench.py --display` | 15 629 |
| 12 | `exhaustion_bench.js` | **220 598** |
| | **steps 1–12** | **1 250 677** |
| 13 | `live-gate.sh --selftest` | **40** |
| | **total** | **1 250 717** |

**Steps 1–12 sum to 1 250 677, identical to the required baseline.** Step 7 is at
691 109 and step 12 at 220 598, both unmoved. Against TZ-17's revision total of
1 250 712, the delta is **+5, entirely step 13** (35 → 40), attributed in item 2 above.
A change that writes no production file and moves no production counter is the required
result here, and it is what happened.

### 9. The four files of §0 — identical

| File | Lines | MD5 | §0 requires |
|---|---:|---|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | identical ✓ |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | identical ✓ |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` | identical ✓ |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | identical ✓ |

No diff on any of them. Standing checks (map §6 item 1) were run anyway, as evidence they
are intact: `python3 -m py_compile main.py` OK, and `node --check` on the `<script>` block
extracted from `index.html` OK.

### 10. The three contract documents

See `## Fingerprints`.

---

## Test Results

| Control | Result |
|---|---|
| `bash -n analyst/live-gate.sh` | exit 0 |
| `--selftest`, 14 cases | exit 0, `checks=40` |
| Negative control on `future_ok` | selftest exit 1, names the case, 3 assertions fired; restored byte-identical |
| Direct entry point, ts +60 s | exit 0, `age_sec:-60`, 70-byte stdout object |
| Direct entry point, ts +121 s | exit 3, stdout empty, stderr names the floor |
| Direct entry point, ts −16 min | exit 3, stdout empty, stderr names the ceiling |
| `900` / `120` occurrence count | 1 each, in the whole file |
| Filter evaluation, 6 rows × 2 workflows × 2 directions | every TZ-required outcome met |
| Second matcher (git wildmatch) | agrees on `'**.md'` and on `'**/*.md'` |
| Hosted `Bench gate`, 13 steps | success, 1 250 717 checks |
| `py_compile main.py` / `node --check` on `index.html` | OK / OK |

---

## Deviations

**One, and it is the finding of this task. `'**/*.md'` already matched root-level
Markdown. TZ-18 §3's premise is refuted by production.**

The change was implemented exactly as §1 authorises — it is a one-line replacement in a
list, and the Architect owns whether it is made. What must not stand is the *reason*
recorded for it, because a false reason in the map's history is worse than no change.

TZ-18 §3 states that `'**/*.md'` "matches only Markdown **inside a directory**", so
"each upload of the map or a contract starts the bot". The repository's own runner history
says otherwise:

| Commit | Changed files | `Bench gate` | `Crypto Update` |
|---|---|---|---|
| `b48b99c` 2026-08-29 11:15:15Z | `SYSTEM-MAP-CRYPTOCALCUL.md` **only** (root level) | ran — run `33249689972` | **did not run** |
| `0a698ac` 2026-08-29 07:15:28Z | `EXECUTOR-INSTRUCTIONS.md` only | ran — run `33240414526` | **did not run** |
| `abe77b6` 2026-08-29 07:16:23Z | `ANALYST-INSTRUCTIONS.md` only | ran — run `33240450611` | **did not run** |

The `Bench gate` runs prove the pushes reached GitHub and were processed. `main.yml`'s
most recent `push` run before this work is `33246640310` at 09:56:19Z — the TZ-17 merge —
so no `Crypto Update` run exists for any of the three root-Markdown pushes. The bot was
not started, the Gist was not rewritten, and no CoinGecko budget was drawn. **The filter
already suppressed them.** The three sources agree: GitHub's live behaviour, the
evaluator's **seg** reading, and git's wildmatch. The **chr** reading that §3 argues from
is the lone outlier.

Consequences, stated plainly:

1. **The `main.yml` half is behaviour-neutral.** `'**.md'` and `'**/*.md'` cover the same
   set of paths in this repository, proven on all six rows. It costs nothing and it fixes
   nothing. Its one real gain is that `'**.md'` reads the same under either interpretation
   of `**`, which closes the ambiguity TZ-17 §Risk 5 recorded and could not settle.
2. **The `bench.yml` half is a genuine repair and its stated justification holds
   unchanged.** `bench.yml` had no Markdown exclusion at all, and the runs above are the
   proof: three documentation-only pushes each burned a full 13-step gate. After this
   change they will not. That is the saving the TZ describes, and it is real.
3. **Acceptance criterion 4 is met, but not in the way §3 predicts.** "`README.md` alone
   does not start `main.yml`" is true after the change — and was already true before it.
   Criterion 4's second half, "`main.py` alone still does", is met and is the control that
   makes the first half meaningful.

No other deviation. Nothing outside `## Scope` was modified, no scope was widened, and the
`'**.md'` lines are exactly where §3.1 and §3.2 place them.

---

## Pre-existing Issues

**1. `analyst/live.json`, as delivered, is not valid JSON — the gate refuses it (exit 2).**

Not caused by this task and not fixed here; the file is the Boss's Shortcut output and no
scope authorises touching it.

```
$ bash analyst/live-gate.sh; echo "exit=$?"
live-gate: check 1: payload is not valid JSON (JSONDecodeError)
exit=2
```

Proven pre-existing by running the same command against unmodified `HEAD` under
`git stash` — identical output and identical exit, and check 3 is never reached, so this
change is not implicated:

```
$ git stash -q && bash analyst/live-gate.sh; echo "exit=$?"; git stash pop -q
live-gate: check 1: payload is not valid JSON (JSONDecodeError)
exit=2
```

The cause is a single unescaped newline **inside a JSON string literal**, at byte 4393:

```
…"oi":"17367882"}\n\n,{"s":"LITUSDT\n","p":"3.461400",…
```

The symbol is written `"LITUSDT\n"` with a raw LF between the `T` and the closing quote.
JSON forbids a literal control character inside a string, so the whole document fails to
parse. Every other row is well-formed. Two observations for the Architect: the producer
is emitting a stray newline into one symbol field, and the gate caught it correctly and
refused to publish — which is the gate working, not failing. This is a Shortcut-side
defect and belongs in a TZ against the producer, not here.

For validation item 4 the scratchpad copy of this payload had that one newline removed so
the probe could exercise check 3 with real market data. **The repository copy was not
modified** — `git status` reports only the three files of `## Scope`.

**2. `prot_bench.js` prints a pre-existing NaN notice on every run** (`at E = 0 the board
prints NaN in «ГРАНИЦЫ СДЕЛКИ»`), unchanged and unrelated, recorded by TZ-12.

---

## Remaining Risks

1. **`analyst/**` is in `bench.yml`'s `paths-ignore`, and `analyst/live-gate.sh` lives
   under it.** A commit that changes only the gate script therefore does not run step 13 —
   the gate's own control. This change was not affected (it also touches both workflow
   files, so the gate ran, run `33251833997`), but the next change to `live-gate.sh` alone
   would land with no runner evidence. That is the shape inv. 37 names: a bench outside the
   gate is not a control. TZ-17 introduced the ignore for the analyst's *data* writes,
   which is correct; the script is code and has been swept up with the data. A narrower
   ignore — the analyst's written paths rather than the whole tree — would close it. Not
   fixed here: no scope.
2. **The `main.yml` half of Change B could not be live-tested in this session.** Proving
   `'**.md'` on GitHub's own filter requires a push to `main` carrying only Markdown, and
   `main.yml` is not merged. Three independent matchers agree that the new pattern covers
   both root-level and nested Markdown, and GitHub's own filter-pattern documentation gives
   `'**.js'` as "all `.js` files in the repository", but the evidence for the *new* pattern
   is a filter evaluation rather than a runner observation, unlike the evidence for the old
   one. The first report push to `main` after this branch merges is the natural live check.
3. **The floor is 120 s and the producer's clock is not monitored.** If the phone drifts
   past two minutes ahead, the gate refuses healthy data and the run publishes no levels.
   That is the specified behaviour and the correct trade, but nothing measures the drift, so
   the first symptom would be a silent run. `age_sec` is already reported in the success
   payload and is signed — a day-log line recording it over time would turn drift into
   something visible before it becomes a refusal.
4. **`main.yml`'s `paths-ignore` remains a deny-list with no `paths` allow-list.** Every
   path not named starts the bot. TZ-17 raised it and TZ-18 §7 deliberately declines to
   convert it; carried forward unchanged.
5. **The evaluator used in item 6 is a reimplementation of GitHub's documented semantics,
   not GitHub's code.** It is cross-checked against git's wildmatch and, for the old
   pattern, against three real runner observations. The nuance TZ-17 §Risk 5 left open is
   now settled by those observations rather than by the evaluator.

---

## Commit

**Implementation:** `8f45ea81e9d030208bbcfa6e196e251f2746bbdb` on
`claude/execute-tz-18-e0miv8`.

```
fix(analyst): two-sided freshness window and root-level md filter (TZ-18)
```

The subject line is the string TZ-18 §5 gives, verbatim.

---

## Pull Request

**No pull request exists.** This session does not open one without an explicit
instruction, and TZ-18 gives none; per contract §8 the branch is pushed and the link is
handed over instead.

- Branch: **`claude/execute-tz-18-e0miv8`**
- Compare URL: **https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-18-e0miv8**

The Boss opens and merges from that link in one action, after the Architect's verdict.

---

## CI Execution

**`Bench gate` executed on a hosted runner**, on the pushed branch — `bench.yml`'s `push`
trigger covers `claude/**`, so the branch has runner evidence with no pull request open.

| Workflow | Where | Run | Head | Conclusion |
|---|---|---|---|---|
| `Bench gate` (`bench.yml`) | GitHub hosted runner, `ubuntu-24.04` | `33251833997` | `8f45ea8` | **success**, all 13 steps |
| `Crypto Update` (`main.yml`) | — | none | — | not triggered: it fires only on `push` to `main` and on `workflow_dispatch`, and this is a branch push. Correct, not a gap. |
| `Calibration` (`calib.yml`), `backtest_bench.yml`, `journal.yml` | — | none | — | not triggered by this change; none is in scope. |

The 13 steps were also run locally, where **two of them could not execute**: `numpy` is
absent from this session's environment, so `verify_bench.py` and
`direction_bench.py --props …` both ended in `ModuleNotFoundError`. The runner installs
`numpy` in its `Зависимости` step and ran all 13. **The runner is the evidence for every
counter in item 8**; the local run is reported here only so the difference is not glossed.

---

## Final Repository State

- `main` untouched by this change except for this report.
- Branch `claude/execute-tz-18-e0miv8` at `8f45ea8`, pushed, gate green.
- Working tree clean; no scratch file, no generated artifact committed. All probe work
  (the mirror gate root, the throwaway clone, the evaluator, the wildmatch repositories)
  was done in the session scratchpad, outside the repository.
- Three files changed, exactly those in `## Scope`.

**NOT IN EFFECT UNTIL MERGED.**

---

## Fingerprints

Map revision string, from `## 0. Fingerprint`: **`**Revision 2026-08-29-a.**`** — matches
the revision TZ-18's header requires. All seven content anchors were matched as exact
substrings before any work began; all seven present.

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1470 | `0506510e3edbb4f90a3b625c3ce4a4d4` |
| `EXECUTOR-INSTRUCTIONS.md` | 590 | `3d810ec57716e7d2e5afda49d95db662` |
| `ANALYST-INSTRUCTIONS.md` | 627 | `722e5e4c41c1ab443a0ebec32bc122ce` |
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `analyst/live-gate.sh` | 444 | `3e15ec4265a7a17b36677948012b79ea` |
| `.github/workflows/main.yml` | 51 | `bbba090ebaa8d0f9c7c3530fd4bd7674` |
| `.github/workflows/bench.yml` | 131 | `461c0d2042d75c8859450eab656064f9` |

Version and revision strings: `EXECUTOR-INSTRUCTIONS.md` **Version 10** (TZ-18 requires 10
or later — satisfied); `ANALYST-INSTRUCTIONS.md` **Revision 2026-08-29-c**;
`SYSTEM-MAP-CRYPTOCALCUL.md` **Revision 2026-08-29-a**.

The four files of the map's `## 0` table are byte-identical to the fingerprints it states.
`analyst/live-gate.sh` and the two workflows are the three files this TZ changed; their
hashes are for the branch head `8f45ea8`.
