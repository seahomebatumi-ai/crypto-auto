# TZ-17 — Analyst engine build

**Canonical filename:** `TZ-17-analyst-engine-build.md`
**Directory:** `CryptoTZ/`
**Report:** `CryptoReports/TZ-17-analyst-engine-build-report.md`
**Model:** **Opus.** A workflow filter with a live-calculator blast radius, a gate whose
failure mode is silence, and a state file that stops every future run if it is wrong.

**Requires `EXECUTOR-INSTRUCTIONS.md` version 10 or later.** v9 carried the three
defects TZ-16 measured; under v9 the first analyst commit is a hard-floor violation
(finding C1). If the repository contract reads **Version 9** or lower, report BLOCKED
naming the version found, and stop.

**Predecessor:** `CryptoReports/TZ-16-analyst-path-verification-report.md`, ПРИНЯТО.
Every design decision below is a consequence of a number in that report, not of an
assumption. Read it before this file.

---

## 0. Required System Map fingerprint — quoted IN FULL

**Revision 2026-08-28-a.** Baseline: TZ-15 merged into `main`; implementation
commit `c8be42b`, report `CryptoReports/TZ-15-caption-truth-report.md`. **The
baseline names the implementation commit, not the merge commit** — a merge commit
carries no content, and content is what this block pins.

Every TZ header quotes this block IN FULL — all six anchors and the file table,
never a subset. The Executor matches each anchor as an exact substring against the
repository copy before any work (contract §5); any mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-28-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `50. **A stated absence is a dependency of the thing it denies.**` |

Live files at this revision — the set every TZ header and every report fingerprints:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

The calibration record is fingerprinted, unlike every other bench artifact, because
it is one of exactly two places `DAY_RANGE_ABNORMAL = 1.39` exists and gate step 12
compares the two on every push (inv. 46).

Gate at this revision: `bench.yml`, **12 steps, 1 250 677 checks**, green on the
hosted runner (run `32780919062`, head `c8be42b`, all 12 steps `success`). The
number is a sum of per-comparison counters (inv. 43), never an estimate, and every
delta between revisions is attributed term by term. TZ-15 moved exactly one step:
12 (`exhaustion_bench.js`) 220 534 → 220 598, **+64**, one new section `caption`
(M1–M5); all fourteen pre-existing counters of that bench and all of steps 1–11 are
unmoved, which for a change touching one display string, one comment and one bench
is the required result rather than a pleasant one.

**Step 7 (`journal_bench.js`) moves with verdict CONTENT, not only with control
volume.** It counts numeric leaves of the records it writes, and a verdict that
returns before geometry writes no `geo` object, so a change in verdicts moves it
without moving a single control. A fall in step 7 is attributed, never assumed
benign, because a defect that nulls a field lowers it identically. Held at
**691 109** through TZ-13, TZ-14 and TZ-15.

**This TZ modifies none of those four files.** Their hashes must be identical in the
report; a diff on any of them is a scope violation and the TZ is rejected whole.

---

## 1. What TZ-16 changed about the design

Three measurements, three consequences. Stated so the Executor knows why each stage
exists and refuses anything that contradicts them.

| Measured | Consequence in this TZ |
|---|---|
| Every market host refused at CONNECT — `fapi`, `data-api.binance.vision`, CoinGecko, `gist.githubusercontent.com` | The engine performs **no network fetch for prices at all**. Stage A. |
| The only surviving payload route was scraping a rendered gist HTML page | Rejected as a transport. A presentation detail with no compatibility promise cannot sit behind a stop loss. Stage A. |
| A commit touching `analyst/state.json` fires `main.yml`, running `main.py` with `GIST_TOKEN` against the live Gist, with a retry | Stage B, and it is the **first** stage: the hazard is live on `main` today. |

**The collection pipeline does not change.** The Boss's Shortcut makes the same
Binance Futures calls from the same network and produces the same payload. Only the
destination moves — from a Gist the engine cannot reliably read to the repository the
engine already has open. That is not a second delivery mechanism; it is the existing
one, one hop shorter.

---

## 2. Files

| Path | Action | Written by |
|---|---|---|
| `.github/workflows/main.yml` | modify — one line in `paths-ignore` | Executor, branch + PR |
| `.github/workflows/bench.yml` | modify — `paths-ignore`, and one new step | Executor, branch + PR |
| `analyst/live-gate.sh` | create | Executor |
| `analyst/state.json` | create, seeded empty | Executor |
| `analyst/log/.gitkeep` | create | Executor |
| `analyst/README.md` | create — 15 lines, what the tree is and who writes each file | Executor |

Nothing else. **No `analyst/live.json` is created by this TZ** — it arrives from the
Boss's Shortcut, and a placeholder would be a price with no producer behind it.

---

## 3. Stage A — `analyst/live-gate.sh`

One `bash` script, `set -euo pipefail`. It **reads a file**; it opens no socket. A
network call anywhere in this script is a scope violation.

### A.1 Universe

The symbol list is cut from `tokens[]` in `index.html` at run time. **A hard-coded
list of coins is banned** (inv. 21). TZ-16 measured `tokens[]` at 28 entries and the
payload at 29 symbols, the extra being `BTCUSDT` — the regime reference, expected and
not an error. The required relation is one-directional: **every `tokens[]` symbol
present in the payload**; extra symbols in the payload are allowed and counted.

### A.2 Input

`analyst/live.json`, path fixed, no argument, no environment variable, no URL.

Schema as measured, all values JSON **strings** except top-level `n`:

```
{ "ts":"ISO-8601 with offset", "src":"fapi", "n":29,
  "c":[ {"s","p","h","l","chg","qv","mark","fr","oi"} × n ] }
```

### A.3 Validation — all must hold for exit 0

| # | Check | Exit |
|---|---|---|
| 1 | file exists and parses as JSON | 2 |
| 2 | `ts` present and parseable, offset form accepted | 2 |
| 3 | `now − ts ≤ 900` s, `now` from `date -u` | 3 |
| 4 | `n` equals `len(c)` | 4 |
| 5 | every `tokens[]` symbol present in `c` | 5 |
| 6 | every `p`, `h`, `l` casts to a finite number > 0 for every row | 6 |
| 7 | comparisons performed > 0 | 7 |

**Check 4 is not redundant.** TZ-16 used it to prove a whole file had been delivered
rather than a truncated one, and it costs one comparison.

**Check 6 is the string trap, and it is why the cast is explicit.** Every price in
the payload is a string; a silent cast yields `NaN`, and `NaN` compared with anything
is false, so a corrupt row would pass a naive range check by failing it quietly.

**Check 7 is not decoration** (inv. 22): a validator that passes with no data is a
failed validator. Count what was compared; fail on zero.

On success stdout is one JSON object: `{"ts","age_sec","n","checked"}`. On failure
stdout is **empty** and stderr is one line naming the failed check — a partial payload
on stdout is the exact shape a caller mistakes for a good one.

### A.4 `--selftest` — offline, known-answer

Fixtures built in a temp dir, fed through the same validation path as real input
(inv. 21 — no second validator). Each case asserts the exact exit code:

```
fresh + complete                 -> 0
ts 16 minutes old                -> 3
ts absent                        -> 2
malformed JSON                   -> 2
n disagrees with len(c)          -> 4
one tokens[] symbol missing      -> 5
one price is the string "abc"    -> 6
one price is "0"                 -> 6
one price is "NaN"               -> 6
empty c array                    -> 7
file absent                      -> 2
tokens[] unreadable              -> non-zero, named
```

Prints `checks=N`, exits non-zero if N is zero or any case disagrees.

`--now` prints the UTC ISO timestamp from `date -u` and exits 0, so a run has exactly
one clock.

---

## 4. Stage B — the workflow filters

**Do this stage first and report it first.** The hazard is live on `main` now.

1. `main.yml`: add `- 'analyst/**'` to the existing `push.paths-ignore` list.
   Add a one-line comment in the same Russian style as its neighbours stating why:
   the analyst tree is consumed and written by the analyst, never by the bot, and a
   state write is not a reason to redraw 28 coins through CoinGecko.
2. `bench.yml`: add `- 'analyst/**'` to its `push.paths-ignore`. The gate proves
   nothing about a payload commit and costs runner minutes on every analysis run.
3. Change nothing else in either file. `calib.yml`, `journal.yml` and
   `backtest_bench.yml` were measured in TZ-16 as unable to fire on `analyst/**` and
   are not touched.

**Negative test, mandatory** (contract §9, «any TZ touching CI requires a negative
test»). On the branch, in the working tree: construct a commit touching
`analyst/state.json` and demonstrate from the filter — not from a live run — that
`main.yml` would not match it, and that removing the new line restores the match.
State the method used and its output. A filter never proven to exclude is not a filter.

---

## 5. Stage C — state, log, and the tree's own README

`analyst/state.json`, seeded exactly:

```json
{"v":1,"k":"state","d":"1970-01-01","ts":"1970-01-01T00:00:00Z","items":[],"archive":[]}
```

**Seeded empty, never imported.** TZ-16 found the Gist's `state.json` carries 211
pairs of typographic quotes and a different, abbreviated item schema; it fails
`json.loads` at character 1. Contract §4b names an unparseable state file as one of
two conditions that stop a run outright, so importing it would stop every run forever
— a file that exists, looks right and is refused. Any migration of its 17 items is a
separate TZ and is not attempted here.

The past date is deliberate: a first real run must overwrite it, and an unwritten
state must be recognisable as unwritten rather than as a quiet day.

`analyst/log/.gitkeep` — empty.

`analyst/README.md` — at most 15 lines: what each file is, who writes it, that the log
is immutable and the state is replaced in place, and that the methodology is
`ANALYST-INSTRUCTIONS.md`. **No rule is restated there**; it is a signpost, and a
signpost that grows into a fourth copy of the rules is a defect.

No `.gitignore` entry for `analyst/**` — the tree is the artifact.

---

## 6. Stage D — wire the selftest into the gate

Add step 13 to `bench.yml`, `Analyst gate selftest`, running
`bash analyst/live-gate.sh --selftest` under `shell: bash -euo pipefail` (inv. 25 — a
pipe without `pipefail` makes a failed step look green). It needs no network.

Record the step's `checks=N`. **An unwired bench is not a control** (inv. 37); this
step is why the gate can be trusted after the session that wrote it has ended.

Steps 1–12 must be untouched and their counters identical to the TZ-15 baseline —
**1 250 677** total, step 7 at **691 109**, step 12 at **220 598**. This TZ writes no
production file, so any movement in steps 1–12 is a finding reported term by term
before anything else.

---

## 7. Validation — written by the Architect

1. `bash -n analyst/live-gate.sh` — clean.
2. `shellcheck` if available; report the version or its absence.
3. `--selftest` exits 0, `checks=N`, N ≥ 12.
4. `--now` exits 0, output within 5 s of `date -u`.
5. **Negative control on the selftest:** invert one fixture's expected exit code,
   confirm `--selftest` exits non-zero and names that case, restore. Report both
   outcomes. A selftest never proven able to fail is not evidence (inv. 23).
6. **Zero-data control:** run the validator against `{"ts":…,"n":0,"c":[]}` and
   confirm exit 7, not exit 0.
7. **String-trap control:** confirm a row whose `p` is `"NaN"` exits 6 and does not
   pass check 6 by silent comparison.
8. Stage B negative test per §4, with its method and output.
9. `python3 -c "import json;json.load(open('analyst/state.json'))"` — parses; print
   the parsed keys.
10. `git diff --stat` — the changed-file list equals §2 exactly.
11. MD5 and line counts for the four files in §0 — identical to §0.
12. MD5 and line counts for `ANALYST-INSTRUCTIONS.md` and `EXECUTOR-INSTRUCTIONS.md`,
    with the contract's version string.
13. Full `bench.yml` gate, now 13 steps, per-step counter table.
14. Explicit no-regression statement covering steps 1–12.

**Do not run an analysis.** Building the engine and exercising it are two acts; a
first run inside the implementation session would write a state file nobody audited,
and it would do so before the Shortcut has been changed to produce a payload.

---

## 8. Acceptance criteria

1. A commit touching `analyst/**` cannot start `main.yml`, proven by a negative test.
2. `analyst/live-gate.sh` opens no socket, reads the universe from `tokens[]`, and
   returns a distinct non-zero exit for each failure class in §3.A.3.
3. The selftest is itself proven able to fail.
4. `analyst/state.json` parses and matches schema v1, seeded empty.
5. `bench.yml` runs 13 steps; steps 1–12 unmoved.
6. No production file changed; the four §0 hashes identical.
7. The report carries the fingerprints contract §10 requires, both directions.

---

## 9. Deliberately not built

`[решение принято мной]`

- **No network path of any kind in the engine.** The alternative — scraping the gist
  HTML page — was measured working and is refused: it depends on GitHub's rendering of
  a file into a table, which can change without notice and would fail by returning
  something rather than by erroring. Discarded alternative named, per house rule.
- **No migration of the Gist `state.json`.** Seventeen items in an abbreviated schema
  with broken quoting is a data problem, not a build problem, and mixing them lets a
  bad parse block the build.
- **No scheduled analysis run.** The trigger stays the Boss's: an unattended engine
  publishing levels nobody asked for is the failure mode of every automated advisor.
- **No change to `catalysts.json`, the journal, the calculator or any bench but the
  new step.** The engine is additive to the ecosystem or it is not admitted.
