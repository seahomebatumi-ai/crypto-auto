# TASK

**TZ ID:** TZ-04
**Canonical filename:** `CryptoTZ/TZ-04-freshness-truth.md`
**Model:** Opus — three files, an exit-code change with CI consequences, and a display
rule that must not move a single number. Not mechanical.

> Filenames degrade in transit. Commit this file under the canonical path above, taken
> from **this header**, never from the name it arrived under.

---

## Precondition — read before anything else

1. `git fetch --all --prune`.
2. **`git rev-parse --is-shallow-repository`. If it prints `true`, run
   `git fetch --unshallow` before assessing anything.** A shallow clone hid 39 commits
   of `.github/workflows/main.yml` history and produced a confident, wrong, committed
   finding in `CryptoReports/TZ-02-foundation-report-2.md`. *"Not in my working tree"*
   is not *"not in the repository"*, and neither is *"not in my truncated history"*.
   Challenge any suspiciously small `git log` result before building on it.
3. `origin/main` must contain, all four:
   - `CryptoReports/TZ-02-foundation-report-3.md`
   - `LATEST-REPORT.md` at the repository root
   - `.github/workflows/main.yml` **without** a `schedule` key
   - `EXECUTOR-INSTRUCTIONS.md` at the root, **Version 5**

If `main.yml` contains a `schedule` key, or the contract is not Version 5 → **STOP,
report BLOCKED.** Do not add, remove or edit any workflow trigger in this task.

**TZ-03 is dead. Do not execute it.** Its precondition demands a `schedule` trigger that
PR #2 removed, and its scope D ("confirm the restored cron fires") is unperformable.
Its two live items are absorbed here as scopes A and B. Nothing from TZ-03 ever reached
the repository; treat `CryptoTZ/TZ-03-report-delivery.md` as superseded, and **do not
delete it** — it stays as history.

## Required System Map fingerprint

- **Content anchors, all three must be present in `SYSTEM-MAP-CRYPTOCALCUL.md`:**
  - the string `**Расписание — НЕ cron.**` inside `## 1. Поток данных`
  - invariant `4.` containing `ЧАСОВОЙ ТЕМП Shortcuts`
  - inside `## 10. На горизонте`, the string `Порядок работ — ПЕРЕСМОТРЕН 21.08`
- **Newest `## 9. Журнал миграций` entry: `2026-08-21`.**
- Reference size: 1482 lines, MD5 `5f9393c386aa2b885aad6f5ab6b4c29d`.

**The anchors and the migration date are the gate; the MD5 is advisory.** If all three
anchors and the date match but the MD5 differs, check whether stripping or adding one
trailing newline reproduces it (`da64e0bc10520787f46c6952386c19ef` without the final
newline). Trailing-whitespace-only difference is **not** a mismatch — the upload path
is known to normalise it. Any other difference → **BLOCKED**, and state which anchor
failed.

---

## Objective

**Make the pipeline able to prove it ran.**

Everything the roadmap puts after this point — the verdict journal, `catalysts.json`,
any backtest of any factor — is a measurement whose time axis is `generated_at`. Right
now three things make that axis untrustworthy:

1. `main.py` returns 0 on every failure path, so a green workflow run is **not**
   evidence that the data refreshed, and the `||` retry in `main.yml` has never been
   able to fire for a write failure.
2. Nothing in the workflow log carries `generated_at`, so a run cannot be audited from
   the outside at all.
3. The board's staleness badge goes red every night on a healthy system, because the
   only regular trigger is an iPhone Shortcut that sleeps from 01:50 to 09:00 local.
   A signal that fires nightly for a non-reason cannot report the real thing.

A sample with unexplained holes cannot support a statistical claim about anything. Fix
the holes before the sample starts accumulating.

## Scope

- **A** — delete the `LATEST-REPORT.md` duplicate.
- **B** — `main.py`: non-zero exit on every path that did not write; one grep-able
  success line carrying `generated_at`.
- **C** — `index.html`: the freshness display separates *schedule pause* from
  *missed refresh*. **Display only — not one number changes.**

Scopes are independent. If one is blocked, complete the rest and report.

**Out of scope, do not touch:** scoring, leverage, geometry, liquidation and protection
math; the `coeffs.json` schema; `CATALYSTS` and `catalystCheck`; workflow triggers;
`actions/checkout@v3` / `actions/setup-python@v4` (known deprecation, deliberately left);
`README.md`; `image.PNG`; the three stale display benches — `display_bench.py`,
`render_bench.py`, `direction_bench.py --display` — reserved for a later TZ.
**Do not disable, alter or replace any automation outside the repository.** The hourly
Shortcut is the Boss's production automation and is not yours to change.

## Files to Modify

- `main.py`
- `index.html`

## Files to Create

- `bench/fresh_bench.js` — new bench, scope C.
- `CryptoReports/TZ-04-freshness-truth-report.md` — **committed directly to `main`**,
  per contract §8. Name its exact path in your closing message.

## Files to Delete

- `LATEST-REPORT.md` (repository root).

Nothing else.

---

## Implementation Requirements

### A — remove the `LATEST-REPORT.md` duplicate

`LATEST-REPORT.md` is a copy of `CryptoReports/TZ-02-foundation-report.md` placed at the
root before `CryptoReports/` existed, and both are 32 341 bytes.

1. Compare the two files byte-for-byte.
2. **Identical → `git rm LATEST-REPORT.md`.**
3. **Different → do NOT delete.** Report the difference under `## Deviations`, leave both
   files in place, and continue with B and C. A root file that is not the duplicate it
   was believed to be is a finding, not a cleanup.

### B — `main.py` fails when it did not write

`main()` has three exits that print and yield status 0:

| # | Location | Current behaviour |
|---|---|---|
| 1 | `if b_data is None:` — BTC download failed | `print(...)`, `return` |
| 2 | `if not r.ok:` — Gist PATCH rejected | `print(...)`, falls through to the end |
| 3 | `except Exception as e:` — anything unhandled | `print(...)`, falls through |

Requirements:

1. **`main()` returns 0 only when the Gist PATCH succeeded.** Paths 1, 2 and 3 each
   return a non-zero code. Use distinct codes so the log tells them apart: `2` for the
   BTC path, `3` for the Gist path, `4` for the unhandled exception.
2. **The entry point must propagate it.** `if __name__ == "__main__": main()` currently
   discards the return value. Change it to `sys.exit(main() or 0)` — and confirm `sys`
   is imported.
3. **One success line, after a successful PATCH**, on stdout, in this exact shape:
   `OK coeffs generated_at=<iso> coins=<n> errors=<n_err>`
   where `<n_err>` is the number of rows in `results` with a truthy `error`. On failure
   print a line of the same shape beginning `FAIL` and naming which path failed.
   This is the whole of the log-visibility fix — nothing else is added to the log.
4. **The history-read failure at `print(f"История: не удалось прочитать прошлую …")`
   keeps returning 0 and keeps writing.** Degrading to an empty history is the designed
   behaviour (invariant 3), and the run still produces `coeffs.json`. Do not change it.
5. **Nothing about what is written may change.** The `payload` dict, key order, rounding
   and `json.dumps` call stay exactly as they are. `coeffs.json`, `debug.json` and
   `history.json` must serialise byte-identically for identical inputs — invariants 1
   and 9.

**Understand the consequence before you write it.** `main.yml` runs
`python main.py || (sleep 60 && python main.py)`. Once `main.py` can exit non-zero the
retry becomes live, and a failed run costs one extra full pass — 30 more CoinGecko
calls. That is the intended fail-safe, it fires only on failure, and the budget carries
it (§1 of the map: ~15.3k/month, no API key, IP-rate-limited only). Do not add a guard
against the retry and do not touch the workflow.

### C — `index.html`: schedule pause is not a failure

Current `updateFreshnessDisplay()` compares age against `STALE_WARN_MIN 75` /
`STALE_CRIT_MIN 130` and nothing else, so between roughly 04:00 and 09:00 local it
reports `! Молчит N мин` in red every single night while the system is healthy.

1. **Extract a pure function** — no DOM, no `Date.now()` inside it:

   ```
   function freshnessState(ageMin, now)   // now: Date
       -> { kind: 'ok' | 'warn' | 'crit' | 'pause', mins: <int> }
   ```

   `updateFreshnessDisplay()` becomes: read `botData.generated_at`, compute `ageMin`,
   call `freshnessState`, render. Same extraction pattern as `tierBadge()` /
   `stateMark()` / `verdictNote()`. This is what makes scope C testable without
   overriding the global clock, and it is required, not optional.

2. **New constants**, beside `STALE_WARN_MIN` / `STALE_CRIT_MIN`, with a comment naming
   §1 of the map as the source of the cadence:

   ```
   var SCHED_FIRST_H = 9;    // первый плановый прогон Shortcuts, локальное время
   var SCHED_LAST_H  = 1;    // последний плановый прогон — 01:50
   var SCHED_LAST_M  = 50;
   ```

3. **The rule**, applied before the existing ladder and nowhere else:

   - Night window: local hour `>= 2` **and** `< SCHED_FIRST_H`.
   - Inside it, `expectedMin` = minutes elapsed since **today's local 01:50**.
   - If `ageMin <= expectedMin + STALE_WARN_MIN` → `kind = 'pause'`.
   - Otherwise, and everywhere outside the night window, the existing
     crit / warn / ok ladder applies **unchanged**.

   The tolerance forgives exactly one missed hourly run inside the night window; two
   missed runs go red. That is a deliberate limit, and it is why scope B exists — the
   run log, not the badge, is where a single missed night run gets resolved.

4. **Rendering.** `kind = 'pause'` prints `Пауза расписания · N мин` in `#888`. The
   other three branches keep their current text and colour byte-for-byte. Russian UI
   strings go into JS as `\uXXXX` escapes, as everywhere else in this file.

5. ES5 only: `var`, string concatenation, no arrow functions, no template literals. No
   new CSS class, no new DOM node, no new network call, no change to any board block or
   scroll-anchor key (invariants 15, 18).

---

## Validation

Run all of it. Record real numbers, not "passed".

### B1 — compile

`python3 -m py_compile main.py` → must pass.

### B2 — exit-code matrix, executed under stubs, no network

Force each path and record the **observed** exit code. Stub CoinGecko and the Gist
entirely; a run that reaches the network invalidates the row.

| Path forced | How | Expected |
|---|---|---|
| BTC download fails | `fetch_with_retry` → `(None, 'stub')` | exit 2 |
| Gist PATCH rejected | `requests.patch` → object with `ok=False`, `status_code=500` | exit 3 |
| Unhandled exception | make `window_stats` raise | exit 4 |
| History read fails | the history `requests.get` raises | **exit 0**, and the PATCH still happened |
| Full success | `requests.patch` → `ok=True` | **exit 0**, stdout contains `OK coeffs generated_at=` |

### B3 — payload identity, the no-regression proof

With one fixed stubbed input set, capture the `json=` argument handed to
`requests.patch` on the **pre-change** and **post-change** code, and compare the
serialised `coeffs.json`, `debug.json` and `history.json` strings. **Byte-identical, all
three.** Report the comparison result explicitly; this is the evidence for invariants
1 and 9, and a difference here fails the whole scope.

### C1 — compile

`node --check` on the `<script>` block extracted from `index.html` → must pass.

### C2 — `bench/fresh_bench.js`, new

Extract `freshnessState` **from `index.html` at runtime and execute it** — invariant 21.
Do not copy the rule into the bench; a bench containing its own copy of the rule proves
nothing. Cover at minimum these cases and report the total check count:

| local time | age, min | expected `kind` |
|---|---|---|
| 14:00 | 20 | `ok` |
| 14:00 | 90 | `warn` |
| 14:00 | 200 | `crit` |
| 01:00 | 200 | `crit` — 01:00 is inside the schedule, nothing is forgiven |
| 02:00 | 10 | `pause` |
| 03:00 | 70 | `pause` |
| 03:00 | 190 | `crit` — two missed runs |
| 08:55 | 425 | `pause` |
| 09:30 | 200 | `crit` — outside the window, nothing is forgiven |
| 09:30 | 40 | `ok` |

Add the boundary pair yourself: `01:59` and `02:00` at the same age must land on
different sides, and `08:59` / `09:00` likewise. Report what they returned.

### C3 — nothing else moved

Diff the extracted `<script>` before and after. The diff must be confined to
`updateFreshnessDisplay`, the new `freshnessState`, and the three new constants.
State explicitly, having checked byte-for-byte, that these are unchanged:
`scoreCandidate`, `momentumScore`, `qualityScore`, `scoreFinish`, `tradeGeometry`,
`marketRegime`, `catalystCheck`, `directionVerdict`, `leverageDecision`,
`invalidationInfo`, `protectionPlan`, `liqPrice`, `tierOf`, `byScore`, `assignRanks`,
`residual7`, and every existing constant.

### D — the gated benches

Run the five benches that CI gates and report checks and failures for each:
`verify_board.js`, `board2_bench.js`, `prot_bench.js index.html`, `verify_bench.py`,
`direction_bench.py --props --fixtures --control --sim`.

**A bench is never edited to make it pass.** A red bench is either a product defect or a
stale expectation — both are findings, both get reported, neither gets silenced here.

### E — repository state

`git status` clean; the branch pushed; the pull request opened with its CI conclusion
recorded; `LATEST-REPORT.md` absent from the branch (or present with the scope-A
deviation explained).

---

## Report

Standard contract §10 format. In addition, the report must state:

- the five observed exit codes from B2, as codes, not as words;
- the B3 comparison result for all three Gist files;
- the `fresh_bench.js` check count and the four boundary results from C2;
- fingerprints (lines + MD5) for `index.html`, `main.py` and
  `SYSTEM-MAP-CRYPTOCALCUL.md`, and the newest migration-log date;
- the pull-request URL, its CI conclusion, and **`NOT IN EFFECT UNTIL MERGED`**.

Commit the report directly to `main` under `CryptoReports/`, and name its exact path in
your closing message to the Boss, in Russian.
