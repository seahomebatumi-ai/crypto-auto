# TZ-41 — The attribution is retained, the dispatch stops deleting what follows the reconciliation, and the gap is read in UTC

**Canonical filename: `TZ-41-attrib-retained-and-utc-gap.md`.** Name the committed file from
this line, never from the name it arrived under (contract §3).

**Model: Sonnet.** Every edit is named to its line and its construction; the only authored
logic is one known-answer control.

**Sequencing: TZ-40 is merged before this TZ starts** — pull request **#37**, merge commit
**`f122bd7`**, implementation commit `805d5e3`. This TZ edits the step TZ-40 added. Check it
and say so at the top of your report.

---

## 0. Fingerprint gate — blocking, before any work

Required map revision, matched as an exact substring against the repository copy
(contract §5):

**Revision 2026-09-10-a.**

The map does not move for TZ-39, TZ-40 or this TZ: the revision that records all three lands
after this report, as TZ-34 and TZ-35 both executed against `2026-09-08-b`.

Content anchors — all seven, each matched as an EXACT substring. **Report the matched
substring, not the verdict** (§10).

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-10-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` |

The map's `## 0` file table — measure each at the stated line count and MD5; a difference is
reported under `## Pre-existing Issues` and is **not acted on** (contract §5).

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**The figures below are the files this TZ touches, measured on `main` at `f122bd7` and
stated so you do not have to explain a difference the map cannot yet carry.** Benches and
workflows are absent from the enforced table by decision (map §0); the gate enforces the
anchors and the revision string only. Report what you measure and do not block on it.

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5009 | `bcdccf8614f1cecbe4d0c0b78129ddf5` |
| `bench/backtest_guard_bench.py` | 2375 | `3937226bc0a15b0cf6917ad7393cd827` |
| `.github/workflows/backtest_bench.yml` | 169 | `a62abbb50a4775999011d802aea5916b` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |

Contract in force: **v20**, 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0`.
Gate after TZ-40: `bench.yml`, 14 steps, **1 336 108** checks; step 4 = **40**, step 14 =
**467**. Your baseline is what you measure.

---

## 1. Why — three facts from the dispatch of 13.09.2026, read from the artifact

- **`--attrib` printed into the job log and nothing retained it.** The `backtest-report`
  artifact carries fourteen files and not one of them is the attribution: the step's `run`
  block has no `tee`, and `bench/attrib.txt` is in no `path:` list. The instrument merged
  yesterday produces an output that exists only until the log expires, and the one reader it
  was built for cannot open it beside the reconciliation it explains.
- **The reconciliation now deletes every measurement after it.** `--verify` exited 1 on a
  single `unexplained` cell, so its step failed, and `Деление по режиму BTC` — which carries
  no condition — did not run: `regimes.txt` is absent from the artifact while every file
  written before `--verify` is present. The attribution step ran only because TZ-40 put
  `!cancelled()` on it. One disagreeing cell should fail the job; it should not cost the run
  the measurements that follow.
- **`_gap_hours` converts through local time.** It computes
  `time.mktime(time.strptime(...)) − time.timezone`, exact only where local time has no
  daylight saving, and the site is now shared by `--verify` and `--attrib`. `calendar` is
  already imported in that file and `calendar.timegm` is already the construction used
  elsewhere in it.

---

## 2. Scope

**Files to Modify:** `.github/workflows/backtest_bench.yml`, `bench/backtest_bench.py`,
`bench/backtest_guard_bench.py`.
**Files to Create:** none. **Files to Delete:** none.

**This TZ names `.github/workflows/backtest_bench.yml` explicitly, which is the
authorisation hard floor item 8 requires.** Nothing in that file changes beyond the three
edits below.

### `## Touches`

- `bench/verify_bench.py` — it imports `backtest_bench.py` at scope (map §0), and this TZ
  edits a function `--verify` calls, so it can turn gate step 4 red. Run it; do not edit it.

---

## 3. Four edits, in three files, and nothing else

1. **The `--attrib` step retains its output.** Its command becomes
   `python backtest_bench.py --attrib --bot ../main.py --html ../index.html 2>&1 | tee attrib.txt`,
   the shape the `--verify` step immediately above it already uses. The step's `name`, its
   `if: ${{ !cancelled() }}` and its comment block are unchanged.
2. **`bench/attrib.txt` joins the `upload-artifact` `path:` list**, on its own line next to
   `bench/verify.txt`. The `if: always()` on that step and every other entry are unchanged.
3. **`if: ${{ !cancelled() }}` goes on the `Деление по режиму BTC` (`--regimes`) step, and
   on that step only.** The reason is the one TZ-40 recorded for `--attrib`: a failed
   reconciliation must not delete the measurements after it. This is not `continue-on-error`
   and removes no step — a failed `--verify` still fails the job, and a failed `--regimes`
   fails it too (hard floor item 12).
4. **`_gap_hours` reads the stamp in UTC.** Replace the `time.mktime(...) − time.timezone`
   pair with `calendar.timegm(time.strptime(gen[:19], "%Y-%m-%dT%H:%M:%S"))`, the
   construction the same file already uses. The `except` path, the `if g and ends` guard, the
   return expression and every caller are unchanged, and `time.timezone` disappears from the
   function.

**No behaviour of `--attrib`, `--verify` or `--regimes` changes beyond these four.** No
threshold, class, `HARD_CLASSES` entry or comparison-window rule is touched.

---

## 4. The control — a new section in `bench/backtest_guard_bench.py`, gate step 14

**Its letter is read FROM THE FILE and never by counting**: two sections already share `E`
(map §0). Name the letter and why in the report.

Known-answer assertions, no tolerance anywhere — every equality is exact because both sides
are built from the same constants:

- a `generated_at` string and an `ends` value whose separation in hours is exact by
  construction; `_gap_hours` returns exactly that number;
- **the same assertion under two time zones**: `os.environ["TZ"]` set to a zone that
  observes daylight saving, `time.tzset()` called, then the same with `TZ=UTC`. The two
  readings must be identical, and identical to the constructed answer. Restore the previous
  environment afterwards and assert the restoration;
- a `generated_at` that does not parse returns `None`; an empty `ends` returns `None`.

Every assertion is one comparison, counted where it compares (inv. 43).

**The pre-repair reading is a measurement and belongs in the report.** Run the same two-zone
probe against the file BEFORE the edit and state both values. If this runner shows them
identical, say so and state the zone that produced each — that is the finding, not a failure,
and a repair reported without the reading it repairs is an assertion (inv. 61).

---

## 5. Validation

Run every item; an item that cannot be run **fails** and is never «not applicable»
(contract §9). Baseline first: record each figure before the change.

1. `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` — exit 0.
2. `python3 bench/backtest_guard_bench.py` — exit 0, `FAIL 0`. State the new section's letter
   and check count, step 14's total before and after, and the new gate total term by term
   against your measured baseline (inv. 43).
3. `python3 bench/verify_bench.py` — exit 0, **40** checks, `FAIL 0`.
4. **The two-zone probe, before and after the repair**, all four values stated (§4).
5. **The exit code survives the pipe.** Run the added command's shape under
   `bash -euo pipefail` with a stub that exits non-zero, and state the shell's exit code. A
   `tee` that swallowed a failure would leave the job green on a broken mode, which is the
   whole reason `pipefail` is on the job.
6. **YAML:** `yaml.safe_load` parses the file; the `--attrib` step's command carries
   `tee attrib.txt`; `bench/attrib.txt` is in the artifact `path:` list; the `--regimes` step
   carries `if: ${{ !cancelled() }}`; **no step anywhere carries `continue-on-error`**;
   `git diff` on the file shows these three hunks and nothing else, with the added and
   removed line counts stated.
7. `git diff --name-only` names exactly three files. Restate the four `## 0` hashes measured
   after the change.

---

## 6. What this TZ does NOT do

- **No production file is touched.** `index.html`, `main.py` and `catalysts.json` appear in
  no diff.
- **`--attrib`'s measurement is unchanged** — no term, no population, no exit rule, no
  printed field moves. This TZ carries its output to a file and nothing else.
- **The skip defect is NOT repaired here.** TZ-40 measured that `over` is computed with no
  reference to `skip` and that the skip is one-sided at `gap > 3`; that is a change to
  `--verify`'s verdict and it gets its own TZ against its own worlds.
- **No fetch in this session** (hard floor item 9, inv. 44), and **no forecast about a run
  that has not happened** (inv. 54).

---

## 7. Hard floor clauses this TZ touches — quoted from contract v20

> 2. **Never edit a bench to make it pass.** A red bench is either a product defect or
> a stale expectation; both are findings, neither is a licence to change the
> assertion.

> 8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.

> 12. **Never remove, skip, comment out or `continue-on-error` a bench step to make CI
> green** — editing the assertion (item 2) and deleting the assertion are the same
> act; a step that cannot pass is a finding for the report.

---

## 8. Report requirements

Beyond the §10 template: the section letter and why it was chosen from the file · the
two-zone probe values before and after the repair · the shell exit code from item 5 ·
`## Fingerprints`, mandatory.

`## Status` is COMPLETED when the four edits are in and the gate is green offline. The
dispatch is the Boss's and its absence is not PARTIAL (contract §9).

## Commit Message

```
TZ-41: retain the attribution output as an artifact, keep the post-verify steps running, read the gap in UTC
```
