# Implementation Report — TZ-17

**Specification:** `CryptoTZ/TZ-17-analyst-engine-build.md`
**Predecessor:** `CryptoReports/TZ-16-analyst-path-verification-report.md`, ПРИНЯТО
**Contract:** `EXECUTOR-INSTRUCTIONS.md` **Version 10** — the TZ requires v10 or later;
v10 was found, so the version gate did not block.
**Role:** 1 — implementation. No analysis was run and nothing under `analyst/` was
written as an analyst (§1, §7 of the TZ).

---

## Status

**COMPLETED.**

All four stages executed. The hosted gate ran on the pushed branch and is green at
13 steps. Steps 1–12 are unmoved, term by term, on the runner as well as locally.
No production file was touched; the four `## 0` fingerprints are identical.

One validation item could not be executed and is recorded as a failure rather than
as "not applicable" (§9): **item 2, `shellcheck`** — the binary is not installed in
this session. Item 2 itself only asks that its version or its absence be reported,
and the absence is reported below; the substantive syntax control, item 1
(`bash -n`), ran clean.

---

## Inbound Filing

**Nothing moved.** `git fetch --all --prune` was run first (§3), and the clone was
found **shallow** (`git rev-parse --is-shallow-repository` → `true`), so
`git fetch --unshallow` was run before any historical assessment; the complete
history is 344 commits.

The TZ was already at its canonical path on `origin/main`, uploaded in commit
`18d5816` ("Add files via upload"):

```
$ git log --oneline --all -- CryptoTZ/TZ-17-analyst-engine-build.md
18d5816 Add files via upload
```

No mangled or duplicate copy was found in the repository root or on any other
branch. No `git mv` was required.

**Previous TZ's branch:** TZ-16 was merged into `main` as pull request #16
(`abf5607`), so this work is built on a merged base, not an unmerged one.

**One branch-state fact worth recording:** at session start `origin` carried a
branch named `claude/execute-tz-17-8e9ttq`; the first `git fetch --all --prune`
reported it deleted (`- [deleted] (none) -> origin/claude/execute-tz-17-8e9ttq`).
The local branch of that name was identical to `origin/main` (`git diff
origin/main HEAD` empty), so no work was lost and nothing was rebased or
discarded. The branch was re-created on push.

---

## System Map fingerprint gate (§5)

**PASS.** Run against the repository copy before any work.

| Anchor required by the TZ header | Result |
|---|---|
| `**Revision 2026-08-28-a.**` | PASS |
| `### 3.12 Direction engine — veto cascade` | PASS |
| `### 3.15 Catalyst registry` | PASS |
| `### 3.16 List exhaustion — the day-range measure` | PASS |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | PASS |
| `50. **A stated absence is a dependency of the thing it denies.**` | PASS |

Six of six matched as exact substrings; `anchors_pass=6 anchors_fail=0`. The map's
revision string is `Revision 2026-08-28-a`, the revision the TZ header requires.

The four files the map's `## 0` table lists were measured at the line count and MD5
it states, and all four are identical — see `## Fingerprints`.

---

## Scope Executed

Four stages, in the order the TZ fixes: **B first**, because the hazard was live on
`main` at the moment the session began.

| Stage | What | Result |
|---|---|---|
| **B** | `paths-ignore` in `main.yml` and `bench.yml`, plus the mandatory negative test | done, proven both directions |
| **A** | `analyst/live-gate.sh` — validator, seven exit classes, `--selftest`, `--now` | done, 35 assertions |
| **C** | `analyst/state.json` seeded, `analyst/log/.gitkeep`, `analyst/README.md` | done |
| **D** | selftest wired into `bench.yml` as step 13 | done, green on the runner |

**Deliberately not done, per TZ §7:** no analysis was run. No `analyst/live.json`
was created — it arrives from the Boss's Shortcut, and a placeholder would be a
price with no producer behind it.

---

## Files Created

| Path | Lines | Purpose |
|---|---:|---|
| `analyst/live-gate.sh` | 415 | the live-data gate; reads a file, opens no socket |
| `analyst/state.json` | 1 (no trailing newline) | schema v1, seeded empty at 1970-01-01 |
| `analyst/log/.gitkeep` | 0 | empty, holds the immutable day-log directory |
| `analyst/README.md` | 14 | signpost; the cap is 15 lines |

## Files Modified

| Path | Change |
|---|---|
| `.github/workflows/main.yml` | `+ 'analyst/**'` in `push.paths-ignore`, with the one-line Russian comment TZ §4.1 requires |
| `.github/workflows/bench.yml` | `+ 'analyst/**'` in `push.paths-ignore`; new step 13 |

## Files Renamed

None.

## Files Deleted

None. Nothing was removed, and nothing outside the six paths in TZ §2 was touched.

---

## Implementation Summary

### Stage B — the workflow filters, done first

TZ-16 measured the hazard precisely: `main.yml` has no `push.paths`, only
`push.paths-ignore`, so **every path not listed fires it** — and `analyst/**` was
not listed. A commit touching `analyst/state.json` therefore started the bot,
running `main.py` with `GIST_TOKEN` against the live Gist, with a retry. Every
analysis run would have redrawn 28 coins through CoinGecko as a side effect of
saving its own state.

The fix is one line in each of two files. `main.yml` carries the comment TZ §4.1
requires, in the Russian style of its neighbours:

```yaml
      - '.github/workflows/backtest_bench.yml'
+      # Дерево analyst/ читает и пишет аналитик, а не бот: запись состояния —
+      # не повод гонять 28 монет через CoinGecko и переписывать живой Gist.
+      - 'analyst/**'
   workflow_dispatch:
```

```yaml
       - 'journal/runs.jsonl'
+      - 'analyst/**'
   pull_request:
```

Contract §8 requires the claim that `analyst/**` cannot start the bot to be
**verified before the first analyst commit, not assumed**. It is now verified, and
the verification is below rather than asserted.

### Stage A — the gate

**`analyst/live-gate.sh`, 415 lines, `set -euo pipefail`. It reads a file.**

The transport decision follows TZ-16's measurements and is not re-litigated here:
every market host refused this session at CONNECT, and the one surviving payload
route was scraping a rendered gist HTML page — refused as a transport, because a
presentation detail with no compatibility promise cannot sit behind a stop loss.
The script therefore performs **no network fetch of any kind**.

*Proof, mechanically:* scanning the script's non-comment lines for
`curl|wget|netcat|nc|https?://|urllib|requests.|socket|http.client|urlopen|/dev/tcp`
returns **0 matches**. The validator imports `json, math, re, sys, datetime` and
nothing else. The complete set of external commands the script invokes is
`cat date grep head mktemp printf python3 rm tr wc`.

**The universe (§A.1).** Cut from `tokens[]` in `index.html` at run time by parsing
the `var tokens = [ … ];` block, with `//` comments stripped before symbols are
extracted. A hard-coded coin list is banned (inv. 21), and the selftest's own
fixtures are generated *from that same parse*, so a change to `tokens[]` cannot
leave the selftest behind. Measured at run time: **28 symbols**, matching TZ-16.
The required relation is one-directional — every `tokens[]` symbol must be present
in the payload; extra symbols (`BTCUSDT`, the regime reference) are allowed and
counted.

**The seven checks and their exit codes (§A.3).** One distinct non-zero code per
failure class, so a caller can tell a stale payload from a truncated one from a
corrupt price without parsing text:

| # | Check | Exit |
|---|---|---:|
| 1 | file exists and parses as JSON | 2 |
| 2 | `ts` present and parseable, offset form accepted | 2 |
| 3 | `now − ts ≤ 900` s, `now` from `date -u` | 3 |
| 4 | `n` equals `len(c)` | 4 |
| 5 | every `tokens[]` symbol present in `c` | 5 |
| 6 | every `p`, `h`, `l` casts to a finite number > 0 | 6 |
| 7 | comparisons performed > 0 | 7 |
| — | `tokens[]` unreadable — "non-zero, named" per §A.4 | 8 |
| — | usage error | 9 |

**Check 6 is the string trap, and the cast is explicit for a measured reason.**
Every price in the payload is a JSON string (TZ-16 §4: only top-level `n` is a
number). The obvious tool for a bash script is `jq`, and `jq` is **not safe here** —
measured in this session:

| value | `jq '.p|tonumber'` | exit | would a naive `> 0` accept it? |
|---|---|---:|---|
| `"abc"` | error | 5 | no |
| `"NaN"` | `null` | 0 | no, but silently |
| `"Infinity"` | `1.7976931348623157e+308` | 0 | **yes** |
| `"1e999"` | `1E+999` | 0 | **yes** |

Two corrupt values pass `jq`'s cast as finite-looking positives. The validator
therefore casts with Python's `float()` and tests `math.isfinite(x) and x > 0`,
which rejects all four:

```
'abc'      -> ValueError                       ACCEPT=False
'0'        -> 0.0    isfinite=True   >0=False  ACCEPT=False
'NaN'      -> nan    isfinite=False  >0=False  ACCEPT=False
'Infinity' -> inf    isfinite=False  >0=True   ACCEPT=False
'1e999'    -> inf    isfinite=False  >0=True   ACCEPT=False
```

This is exactly the failure the TZ names: `NaN` compared with anything is false, so
a corrupt row passes a naive range check *by failing it quietly*.

**Output discipline.** On success stdout is one JSON object and nothing else; on
failure **stdout is empty** and stderr carries one line naming the failed check.
This is structural, not incidental: the bash wrapper captures the validator's stdout
and forwards it only when the exit code is 0, because a partial payload on stdout is
the exact shape a caller mistakes for a good one. The selftest asserts this
discipline on every case.

**One validator, not two (inv. 21).** `--selftest` builds fixtures in a temp
directory and feeds every one of them through the same `gate_run` → validator path
that real input takes. There is no second implementation of any check.

**`--now`** prints the UTC ISO timestamp from `date -u` and exits 0, and the real
run takes its `now` from the same function, so a run has exactly one clock.

### Stage C — state, log, README

`analyst/state.json` is seeded **byte-identical to the TZ's own text**. The seed
line was cut out of `CryptoTZ/TZ-17-analyst-engine-build.md` rather than retyped and
compared with `cmp`: 88 bytes, identical. It is written without a trailing newline,
which is what "seeded exactly" produces; `json.load` is indifferent either way.

```
$ python3 -c "import json;d=json.load(open('analyst/state.json'));print(list(d.keys()))"
['v', 'k', 'd', 'ts', 'items', 'archive']
{'v': 1, 'k': 'state', 'd': '1970-01-01', 'ts': '1970-01-01T00:00:00Z', 'items': [], 'archive': []}
```

The top-level key set matches `ANALYST-INSTRUCTIONS.md` §11 schema v1.

**Seeded empty, never imported** — as the TZ requires, and the reason is worth
restating because it is load-bearing: TZ-16 found the Gist's `state.json` carries
211 pairs of typographic quotes and an abbreviated item schema, and it fails
`json.loads` at character 1. Contract §4b names an unparseable state file as one of
the two conditions that stop an analysis run outright, so importing it would stop
every future run — a file that exists, looks right, and is refused.

The 1970 date is deliberate: a first real run must overwrite it, and an unwritten
state must be recognisable as unwritten rather than as a quiet day.

`analyst/README.md` is 14 lines against a cap of 15. It names each file and its
writer, states that the log is immutable and the state is replaced in place, and
points at `ANALYST-INSTRUCTIONS.md` for the methodology. **No rule is restated
there.** No `.gitignore` entry was added — the tree is the artifact.

### Stage D — the selftest inside the gate

Step 13 was added to `bench.yml` under `shell: bash -euo pipefail {0}` (inv. 25). It
needs no network. An unwired bench is not a control (inv. 37); this step is why the
gate can be trusted after this session has ended.

---

## Validation

All fourteen items from TZ §7. Every claim below is a command and its output.

| # | Item | Result |
|---|---|---|
| 1 | `bash -n analyst/live-gate.sh` | **PASS** — clean, exit 0 |
| 2 | `shellcheck`, version or absence | **NOT RUN — recorded as a failure per §9.** `shellcheck: command not found`; the binary is absent from this session. Its absence is reported as item 2 asks. |
| 3 | `--selftest` exits 0, `checks=N`, N ≥ 12 | **PASS** — exit 0, **`checks=35`**, 12 cases |
| 4 | `--now` exits 0, within 5 s of `date -u` | **PASS** — `2026-08-29T07:31:30Z`, delta **0 s** |
| 5 | Negative control on the selftest | **PASS** — see below |
| 6 | Zero-data control → exit 7, not 0 | **PASS** — exit **7** |
| 7 | String-trap control, `p = "NaN"` → exit 6 | **PASS** — exit **6** |
| 8 | Stage B negative test | **PASS** — both directions, two engines |
| 9 | `state.json` parses; print parsed keys | **PASS** — keys printed above |
| 10 | `git diff --stat` equals TZ §2 exactly | **PASS** — 6 files, exactly the six named |
| 11 | The four `## 0` files identical | **PASS** — all four |
| 12 | Contract + methodology fingerprints | **PASS** — see `## Fingerprints` |
| 13 | Full gate, now 13 steps, per-step table | **PASS** — green on the runner |
| 14 | Explicit no-regression statement, steps 1–12 | **PASS** — zero movement, term by term |

### Item 5 — the selftest is proven able to fail (inv. 23)

One fixture's expected exit code was inverted (`price_nan:6` → `price_nan:0`), the
selftest re-run, and the file restored.

```
md5 before:            2fe852b38685b4744fa2554e05e6061a

--- with the expectation inverted ---
exit=1                                       (required: non-zero)
FAIL price_nan            expected exit 0, got 6
FAIL price_nan            stdout is not one {ts,age_sec,n,checked} object:
selftest: 2 assertion(s) failed
checks=34

--- after restore ---
md5 after restore:     2fe852b38685b4744fa2554e05e6061a   → byte-identical
selftest: exit=0  checks=35
```

The selftest exits non-zero and **names the case**, twice — once on the exit code
and once on the stdout discipline. `checks` reads 34 rather than 35 in the inverted
run because a case expected to succeed is not asked for a stderr line; the drop is
attributed, not waved past. A selftest never proven able to fail is not evidence.

### Items 6 and 7 — the two data controls, at the real entry point

Both were run through the script's **real entry point** — no arguments, fixed path —
by placing the payload at `analyst/live.json` inside a temporary root, so the repository
tree was never touched.

```
--- §7.6 zero-data control: {"ts":…,"n":0,"c":[]} ---
live-gate: check 7: payload carries zero rows, no comparison possible
exit=7 (required 7, and specifically NOT 0)   stdout_bytes=0

--- §7.7 string-trap control: one row p="NaN" ---
row 7 symbol: AAVEUSDT, p set to the string "NaN"
live-gate: check 6: row 7 (AAVEUSDT) field p casts to a non-finite value: 'NaN'
exit=6 (required 6)   stdout_bytes=0
```

Both fail with empty stdout, as the output contract requires. For contrast, the
comparison this defeats: `float("NaN") > 0` is `False` **and** `float("NaN") <= 0`
is `False` — a naive range check passes the row by failing it quietly.

The same entry point on a complete, fresh payload returns:

```
{"ts":"2026-08-29T07:25:48+00:00","age_sec":0,"n":29,"checked":153}
```

and with no payload present at all it returns exit 2 with `stdout_bytes=0`.

**`checked=153` reconciles term by term** (inv. 43 — a check count is a count):
check 1 = 3, check 2 = 3, check 3 = 1, check 4 = 1, check 5 = 28 (`tokens[]`
membership) + 29 (payload symbol classification) = 57, check 6 = 29 rows × 3 fields
= 87, check 7 = 1. Total **153**.

### Item 8 — the Stage B negative test (TZ §4, contract §9)

**Method.** A real commit touching only `analyst/state.json` was constructed on the
branch — the exact shape of an analysis-run commit under contract §4b step 8 — and
its changed-file list was taken from `git diff --name-only`, never typed. That list
was evaluated against the filter with a small evaluator that **parses the
`paths-ignore` list out of `.github/workflows/main.yml` with a YAML parser**, so it
tests what is committed rather than what was intended. It implements GitHub's
documented filter semantics (`**` matches across `/`, `*` does not) and GitHub's
decision rule: a push runs the workflow when at least one changed file matches no
`paths-ignore` pattern. This is a filter evaluation, not a live run, as the TZ
requires.

```
$ git diff --name-only HEAD~1 HEAD
analyst/state.json

--- TEST 1: the filter AS COMMITTED ---
branches      : ['main']
paths-ignore  : ['bench/**', '**/*.md', 'index.html',
                 '.github/workflows/bench.yml',
                 '.github/workflows/backtest_bench.yml', 'analyst/**']
   analyst/state.json           ignored by 'analyst/**'
RESULT        : main.yml WOULD NOT RUN

--- TEST 2: the SAME commit with 'analyst/**' REMOVED ---
paths-ignore  : [… without 'analyst/**']
   analyst/state.json           NOT ignored -> fires
RESULT        : main.yml WOULD RUN
```

Removing the new line restores the match. **The line is what does the work**, and
the filter is proven to exclude rather than merely assumed to.

The probe commit was then reverted (`git reset --hard HEAD~1`); the working tree is
clean and `analyst/state.json` is byte-identical to the seed again.

**Controls, so the exclusion is not over-broad.** A filter that ignored everything
would also pass test 1:

| changed files | result | why it matters |
|---|---|---|
| `main.py` | **WOULD RUN** | the bot can still be started by its own source |
| `analyst/state.json` + `analyst/log/2026-08-29.md` | WOULD NOT RUN | the whole analyst commit is covered |
| `analyst/state.json` + `main.py` | **WOULD RUN** | a mixed commit is not silently swallowed |
| `CryptoReports/TZ-17-…-report.md` | WOULD NOT RUN | this report's own push to `main` is covered by `**/*.md` |

**`bench.yml`, same test, same outcome:** `analyst/state.json` → WOULD NOT RUN as
committed; → WOULD RUN with the line removed.

**Independent cross-check.** The decisive pattern was matched by a second, unrelated
engine — git's own wildmatch, via `git check-ignore -v` in a throwaway repository
whose `.gitignore` is the single line `analyst/**`:

```
MATCHED   .gitignore:1:analyst/**	analyst/state.json
MATCHED   .gitignore:1:analyst/**	analyst/log/2026-08-29.md
unmatched main.py
```

Both engines agree. **Live confirmation, additionally:** every `main.yml` run in the
repository's recent history is `workflow_dispatch` from the phone, and the branch
push carrying this work started **no** `Crypto Update` run.

### Standing checks (map §6 item 1)

No production file changed, so these were not required; they were run anyway as
evidence the production files are untouched and still valid.

```
python3 -m py_compile main.py                          → OK
node --check on the <script> block cut from index.html → OK  (1 block, 192 939 chars)
```

---

## Test Results

### The gate, 13 steps — hosted runner

**Run `33241068850`**, workflow `Bench gate`, event `push`, head
`850e263ea03eb4db673063b5bd7b11e1fb215378`, branch `claude/execute-tz-17-8e9ttq`,
job `bench` (`99070388321`), **conclusion `success`**, all steps `success`.
Runner `ubuntu-24.04`, Python 3.12.14, Node 20.20.2.

| # | Bench | Checks (runner) | Baseline | Δ |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 |
| 3 | `prot_bench.js` | 372 | 372 | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 255 708 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 |
| 7 | `journal_bench.js` | **691 109** | **691 109** | **0** |
| 8 | `catalyst_bench.js` | 23 040 | 23 040 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 15 925 | 15 925 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | **220 598** | **220 598** | **0** |
| | **steps 1–12** | **1 250 677** | **1 250 677** | **0** |
| 13 | `live-gate.sh --selftest` | **35** | — | new |
| | **gate total, 13 steps** | **1 250 712** | | **+35** |

The same thirteen benches were also run locally before the push and produced
**identical** counters, step for step. A local run is not a runner run; both were
done, and the runner is the one that counts.

### Item 14 — no-regression statement, steps 1–12

**Steps 1–12 moved by exactly zero, and the whole delta is step 13.** This TZ writes
no production file, so any movement in steps 1–12 would have been a finding reported
before anything else; there is none to report. Specifically:

- **Step 7 (`journal_bench.js`) holds at 691 109**, its value through TZ-13, TZ-14
  and TZ-15. This step moves with verdict *content*, not only with control volume —
  a verdict that returns before geometry writes no `geo` object, so a defect that
  nulls a field lowers it identically to a benign change. It did not move.
- **Step 12 (`exhaustion_bench.js`) holds at 220 598**, and all fifteen of its
  per-section counters are unchanged (`identity: 200002 · nulls: 20027 ·
  quorum: 65 · venue: 25 · banner: 52 · stress: 51 · inert: 120 · purity: 36 ·
  control: 1 · wiring: 31 · record: 8 · threshold: 24 · live: 38 · surfaces: 54 ·
  caption: 64`, `SUM: 220598`).
- Step 12 also re-confirmed inv. 46 on this head:
  `index.html: 1.39   exhaustion-calibration.txt: 1.39   equal: true`.

### Step 13, as it ran on the runner

```
universe: 28 symbols cut from index.html
  fresh                exit=0 expected=0
  stale16              exit=3 expected=3  check 3: payload is stale, age 15360 s exceeds 900 s
  no_ts                exit=2 expected=2  check 2: ts absent or not a non-empty string
  bad_json             exit=2 expected=2  check 1: payload is not valid JSON (JSONDecodeError)
  n_mismatch           exit=4 expected=4  check 4: n=30 disagrees with len(c)=29
  missing_symbol       exit=5 expected=5  check 5: 1 tokens[] symbol(s) absent from payload: SUIUSDT
  price_abc            exit=6 expected=6  check 6: row 28 (LITUSDT) field p does not cast to a number: 'abc'
  price_zero           exit=6 expected=6  check 6: row 28 (LITUSDT) field p is not greater than zero: '0'
  price_nan            exit=6 expected=6  check 6: row 28 (LITUSDT) field p casts to a non-finite value: 'NaN'
  empty_c              exit=7 expected=7  check 7: payload carries zero rows, no comparison possible
  file_absent          exit=2 expected=2  check 1: payload not readable: …/does-not-exist.json
  universe_unreadable  exit=8 expected=8  universe: tokens[] block not found in …/no-tokens.html
checks=35
selftest: 12 cases, all exit codes as specified
```

All twelve cases from TZ §A.4, each returning the exact exit code specified.
**`checks=35` counts assertions, not cases** (inv. 43): each case asserts its exact
exit code (12) and its stdout discipline (12), and each of the eleven failing cases
additionally asserts that stderr carries exactly one line naming a check (11).
12 + 12 + 11 = 35.

---

## Deviations

Five, all recorded rather than resolved silently. None changes a specified exit
code, a check, or a file in TZ §2.

1. **The empty-`c` payload is reported as check 7, not check 5.** With 28 symbols in
   `tokens[]` and zero rows, a strict table-order evaluation would fail check 5
   (coverage) first and return 5. The TZ's own fixture table requires
   `empty c array -> 7`, and §7.6 requires exit 7 specifically, so the zero-data
   condition is detected immediately after check 4 and reported as check 7. This is
   also the semantically correct classification: with zero rows, "symbols missing"
   and "no data at all" are the same observation, and inv. 22 names the second one.
   A second, defence-in-depth check 7 on the row-comparison counter remains at the
   end of the validator. **Every exit code in §A.3 and §A.4 is met exactly.**

2. **Two exit codes beyond the seven in §A.3.** §A.4 requires `tokens[] unreadable`
   to be "non-zero, named" without fixing a number; **8** was chosen, kept distinct
   from 2–7 so a broken universe is never mistaken for a payload defect. **9** is a
   usage error. Neither collides with a specified class.

3. **`bench.yml`'s `paths-ignore` line carries no comment; `main.yml`'s does.**
   TZ §4.1 requires a comment for `main.yml` and §4.2 pointedly does not for
   `bench.yml`, against a §4.3 instruction to change nothing else in either file.
   The literal reading was taken. The new **step 13** does carry a comment, in the
   established style of every other TZ-added step block in that file.

4. **No `## Commit Message` section exists in TZ-17**, so contract §8's "the string
   given in the TZ, verbatim" had nothing to quote. A descriptive message in the
   repository's established style was written instead.

5. **`analyst/state.json` has no trailing newline**, which is what byte-exactness
   with the TZ's seed text produces. `git` will render `\ No newline at end of file`
   in diffs of this file. It parses; the analyst role replaces the file wholesale
   every run.

---

## Pre-existing Issues

1. **`prot_bench.js` reports a pre-existing product defect on every run**, unchanged
   by this work and printed by the bench itself on the runner:
   `PRE-EXISTING (not TZ-12, present on origin/main): at E = 0 the board prints NaN
   in «ГРАНИЦЫ СДЕЛКИ» — Math.abs(liq / E - 1).` Recorded, not fixed — out of scope
   (§6).

2. **The `Bench gate` job emits a GitHub deprecation warning:**
   `Node.js 20 is deprecated. The following actions target Node.js 20 but are being
   forced to run on Node.js 24: actions/checkout@v4, actions/setup-node@v4,
   actions/setup-python@v5.` The job is green and the warning is not a failure, but
   it is a dated dependency in CI and the Architect may want a TZ for it. Not
   touched: `bench.yml` is authorised here for `paths-ignore` and one new step only.

3. **`shellcheck` is not available in the Executor session**, so no shell linting
   beyond `bash -n` can be performed here on any future TZ either. If shell scripts
   are to become a normal part of this repository, a `shellcheck` step in
   `bench.yml` would make the control real rather than dependent on which session
   happens to have the binary. Reported, not implemented — outside scope.

---

## Remaining Risks

1. **A payload timestamped in the future passes check 3.** The TZ fixes the check as
   `now − ts ≤ 900`, which a negative age satisfies. Implemented exactly as
   specified; a lower bound would have been widening the scope, which §6 forbids. If
   the Shortcut's clock ever runs ahead, a stale payload could present as fresh. A
   two-sided window is a one-line change and belongs to the Architect.

2. **The engine is built but has no input yet.** No `analyst/live.json` exists —
   correctly, per TZ §2 — so the gate returns exit 2 until the Boss's Shortcut is
   changed to write the payload into the repository instead of the Gist. Until that
   happens, an analysis run publishes no levels. This is the expected state at the
   end of this TZ, not a defect, but the engine is not usable before that change.

3. **The gate has never been exercised against a real payload**, only against
   fixtures generated from the live `tokens[]`. TZ §7 forbids running an analysis in
   the implementation session, and that instruction was followed. The first real
   payload is the first true test of the schema assumptions, which come from TZ-16's
   measurement of one Gist revision.

4. **`main.yml`'s `paths-ignore` is a deny-list with no `paths` allow-list.** The
   hazard closed here was created by exactly that shape: every path not named fires
   the bot. Any future tree written by the analyst outside `analyst/**` would
   reproduce it. The tree is now covered; the shape remains.

5. **The filter evaluator used for the negative test is a reimplementation of
   GitHub's documented semantics, not GitHub's own code.** It was cross-checked
   against git's wildmatch on the decisive pattern and agrees, and the live evidence
   (no `Crypto Update` run on the branch push) is consistent. One nuance it does not
   settle: whether `**/*.md` matches a **root-level** `.md` file. Nothing in this
   change depends on that — the report path
   `CryptoReports/TZ-17-analyst-engine-build-report.md` contains a `/` and is
   covered under either reading, and the analyst writes no root-level Markdown.

---

## Commit

**Implementation:** `850e263ea03eb4db673063b5bd7b11e1fb215378` on
`claude/execute-tz-17-8e9ttq`.

```
feat(analyst): live-data gate, state seed and workflow filters (TZ-17)
```

```
 .github/workflows/bench.yml |  10 ++
 .github/workflows/main.yml  |   3 +
 analyst/README.md           |  14 ++
 analyst/live-gate.sh        | 415 ++++++++++++++++++++++++++++++++++++++++++++
 analyst/log/.gitkeep        |   0
 analyst/state.json          |   1 +
 6 files changed, 443 insertions(+)
```

Six files, exactly the six TZ §2 names, with zero insertions or deletions anywhere
else. The working tree is clean; no scratch file, cache or `__pycache__` was
committed.

**This report** is committed directly to `main` (§8), separately from the branch.

---

## Pull Request

**No pull request exists.** This session is not permitted to open one without an
explicit instruction, which contract §8 anticipates as a defined fallback rather
than a blocker — so the branch is pushed and the link is below.

- **Branch:** `claude/execute-tz-17-8e9ttq`
- **Compare URL:** https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-17-8e9ttq

The Boss opens and merges from that link in one action, after the Architect's audit
returns ПРИНЯТО.

---

## CI Execution

**The hosted gate ran, and it ran on this exact head.**

| Workflow | Ran? | Detail |
|---|---|---|
| `bench.yml` — Bench gate | **YES** | run [`33241068850`](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33241068850), event `push`, head `850e263`, **conclusion `success`**, all 13 bench steps `success`, 07:32:11 → 07:33:13 UTC |
| `main.yml` — Crypto Update | no | triggers only on `push` to `main`; this is a branch push. Confirmed: no run exists for `850e263`. |
| `calib.yml` | no | not triggered by this change |
| `journal.yml` | no | scheduled; unrelated to this change |
| `backtest_bench.yml` | no | needs the external archive; never modified (hard floor 8) |

The gate fires on `claude/**` (TZ-07 §6), which is why runner evidence exists with
no pull request open. Status is **COMPLETED**, not PARTIAL: a workflow did execute
on a runner.

---

## Final Repository State

- `main` is unchanged by the implementation and carries only this report.
- The implementation lives on `claude/execute-tz-17-8e9ttq` at `850e263`, green on
  the hosted gate.
- No production file (`index.html`, `main.py`, `catalysts.json`, `coeffs.json`) was
  modified. Pages serves `index.html`, which is byte-identical to `origin/main`.
- Working tree clean, on the branch, no untracked artifacts.

**NOT IN EFFECT UNTIL MERGED.**

Until the merge, `main.yml` on `main` still lacks `analyst/**` in its
`paths-ignore` — the hazard TZ-16 measured is closed on the branch and **remains
open on `main`**. No analyst commit should be made to `main` before this is merged.

---

## Acceptance criteria (TZ §8)

| # | Criterion | Result |
|---|---|---|
| 1 | A commit touching `analyst/**` cannot start `main.yml`, proven by a negative test | **MET** — both directions, two independent matchers |
| 2 | The gate opens no socket, reads the universe from `tokens[]`, returns a distinct non-zero exit per failure class | **MET** — 0 network primitives; 28 symbols cut at run time; exits 2–8 distinct |
| 3 | The selftest is itself proven able to fail | **MET** — inverted fixture, named failure, byte-identical restore |
| 4 | `analyst/state.json` parses and matches schema v1, seeded empty | **MET** — parses; keys match §11 |
| 5 | `bench.yml` runs 13 steps; steps 1–12 unmoved | **MET** — 13 green; Δ = 0 term by term |
| 6 | No production file changed; the four `## 0` hashes identical | **MET** |
| 7 | The report carries the §10 fingerprints, both directions | **MET** — below |

---

## Fingerprints

Measured on `claude/execute-tz-17-8e9ttq` at `850e263`.

### System Map

| File | Lines | MD5 | Revision |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1 359 | `bbe10e931f4dcc2546a9daa31c03b856` | `Revision 2026-08-28-a` |

### The map's `## 0` file table — required vs found

| File | Lines req. | Lines found | MD5 required | MD5 found | Verdict |
|---|---:|---:|---|---|---|
| `index.html` | 3 729 | 3 729 | `fdf331906bf205944b25e3635135789c` | `fdf331906bf205944b25e3635135789c` | **IDENTICAL** |
| `main.py` | 506 | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | `1a5a5d98b2fd76010f202ee3eebaa717` | **IDENTICAL** |
| `catalysts.json` | 11 | 11 | `021dd2c90dc395240c0b0c3dbae40426` | `021dd2c90dc395240c0b0c3dbae40426` | **IDENTICAL** |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | **IDENTICAL** |

Four of four identical. **This TZ modified none of these files**, as it requires.

### Contracts (TZ §7.12)

| File | Lines | MD5 | Version / revision |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 590 | `3d810ec57716e7d2e5afda49d95db662` | **Version 10** |
| `ANALYST-INSTRUCTIONS.md` | 627 | `722e5e4c41c1ab443a0ebec32bc122ce` | **Revision 2026-08-29-c** |

### Files this TZ created or modified

| File | Lines | MD5 |
|---|---:|---|
| `analyst/live-gate.sh` | 415 | `2fe852b38685b4744fa2554e05e6061a` |
| `analyst/state.json` | 0 (88 bytes, no trailing newline) | `970fe700ecea2021b5f14d2c5a25e53f` |
| `analyst/README.md` | 14 | `fd373be9e34a303d87259a0a4c8dedde` |
| `analyst/log/.gitkeep` | 0 (0 bytes) | `d41d8cd98f00b204e9800998ecf8427e` |
| `.github/workflows/main.yml` | 51 | `79cba19427922e0d972c0509b4a6f7ed` |
| `.github/workflows/bench.yml` | 130 | `8616c98d24bb494811facdd7e95ae092` |

### The specification

| File | Lines | MD5 |
|---|---:|---|
| `CryptoTZ/TZ-17-analyst-engine-build.md` | 309 | `c52723e866ca4e3e3e3bfb9b1f75d8d8` |
