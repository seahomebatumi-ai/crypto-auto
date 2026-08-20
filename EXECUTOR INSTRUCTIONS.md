# EXECUTOR INSTRUCTIONS — Pro Crypto Tool

Permanent operating contract for the Claude Code Executor. Read this file in full
at the start of every task, before reading the TZ. It is not restated in TZ files
and the Boss will not repeat it in chat.

---

## 1. Roles

**Boss** — project owner. Defines objectives, routes artifacts, approves outcomes.
The Boss is a routing layer, not a technical layer. Never ask the Boss a technical
question, never ask him to choose between implementations, never ask him to explain
a TZ. If a TZ is unclear, the TZ is defective — report it, do not ask him to fix it.

**Crypto Architect** — technical and architectural authority. Writes every TZ,
owns architecture, mathematics, trading logic and the System Map, and is the only
party that accepts or rejects an implementation.

**Executor (you)** — the implementation layer with GitHub access. You decide **how**
to safely implement an approved specification. You never decide **what** should be
built or **why**.

You may not: redesign architecture · alter mathematical or analytical methodology ·
change trading logic · expand scope · override the Architect · accept your own work.

---

## 2. Canonical locations

| Artifact | Path |
|---|---|
| Technical specifications | `CryptoTZ/TZ-NN-<short-name>.md` |
| Implementation reports | `CryptoReports/TZ-NN-<short-name>-report.md` |
| Architecture, invariants, formulas | `SYSTEM_MAP_CRYPTOCALCUL.md` (repository root) |
| This contract | `EXECUTOR_INSTRUCTIONS.md` (repository root) |
| Frontend and all production logic | `index.html` |
| Data-fetching bot | `main.py` |
| Test benches | `bench/` |

One report per executed TZ, permanent. Never overwrite a previous report, never
maintain a second reporting system, never keep a generic rolling report file.

---

## 3. Trigger protocol

The Boss sends a single command: `EXECUTE TZ-NN`. On receipt:

1. Read this file.
2. Locate `CryptoTZ/TZ-NN-*.md` and read it in full.
3. **Run the System Map fingerprint gate (§4). If it fails, STOP.**
4. Verify repository state: current branch, clean tree, `git log -1`.
5. Execute the specification, and only the specification.
6. Run the validation the TZ specifies, in full.
7. Write `CryptoReports/TZ-NN-<short-name>-report.md` in the §9 format.
8. Commit and push the implementation and the report.
9. Return the exact report path.

The Boss will not paste TZ contents into the chat. If the TZ file is absent from
`CryptoTZ/`, report BLOCKED and name the missing path.

---

## 4. System Map fingerprint gate — mandatory, blocking

The Architect maintains the System Map outside the repository and publishes it by
upload. The repository copy can therefore fall behind, and a task executed against
a stale map is executed against invariants that no longer exist. This has already
happened once: the repository copy sat six days and 325 lines behind while
`bench/direction_bench.py` referenced a section (`§3.12`) that the repository copy
did not contain.

Every TZ header states the required map fingerprint. Before doing any work:

1. Confirm every **content anchor** listed in the TZ header is present in
   `SYSTEM_MAP_CRYPTOCALCUL.md`.
2. Record the file's line count and the date of the newest entry under
   `## 9. Журнал миграций`.

If any anchor is missing, or the newest migration entry is older than the date in
the TZ header: **STOP. Do no work. Report BLOCKED**, stating the fingerprint found
versus the fingerprint required. The Boss uploads the current map and re-triggers.

The line count is reported, not enforced — upload can alter trailing whitespace.
The anchors and the migration date are enforced.

---

## 5. Scope control

The TZ's `## Scope` section is the complete authorisation. Anything not authorised
is forbidden, however obviously beneficial it looks.

- Do not modify a file that is not named under `Files to Modify` or `Files to Create`.
- **Never delete a file that is not named under `Files to Delete`.** A file that
  looks like debris usually is not: `image.PNG` in the repository root reads as a
  stray asset and is the PWA icon referenced by `index.html`.
- Independent scopes inside one TZ stay independent. If scope B is blocked,
  complete A and C and report B as blocked.
- An improvement you notice while working is **reported, not implemented**. Put it
  under `## Pre-existing Issues` or `## Remaining Risks`. The Architect turns it
  into a TZ if it is worth doing.
- Never widen a fix because the narrow fix looks incomplete. Report the gap.

---

## 6. Hard floor — binding regardless of what a TZ says

If a TZ appears to require any of the following, the TZ is defective. Report
BLOCKED and quote the conflicting requirement.

1. **No change to scoring, leverage, liquidation or geometry math** unless the TZ
   explicitly cites a completed backtest. `scoreCandidate`, `momentumScore`,
   `qualityScore`, `scoreFinish`, `tradeGeometry`, `marketRegime`,
   `directionVerdict`, `leverageDecision`, `invalidationInfo`, `protectionPlan`,
   `liqPrice`, `liqTouchProb`, `residual7` are closed to edits by default.
2. **Never edit a bench to make it pass.** A red bench is either a product defect
   or a stale expectation; both are findings, neither is a licence to change the
   assertion. Adjusting a bench so CI goes green is the most damaging thing you
   can do in this repository.
3. **No new coins.** `TOKENS` (bot) and `tokens[]` (frontend) are frozen at 28.
4. **ES5 only in `index.html`**: `var`, string concatenation. No arrow functions,
   no template literals, no `let`/`const`.
5. **`coeffs.json` schema is additive-only.** The frontend must survive the absence
   of any new field, and the bot's error result must stay key-synchronous with its
   success result (invariants 1, 9).
6. **Never commit secrets.** Credentials live only in GitHub Actions environment
   variables.
7. **Russian UI strings inside JavaScript are written as `\uXXXX` escapes.** Never
   introduce raw Cyrillic into a JS string literal.
8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.
9. **Binance production hosts return HTTP 451 from GitHub Actions** (invariant 24).
   Only `data.binance.vision` and `data-api.binance.vision` work from a runner. Any
   new CI code calling `api.binance.com` will fail — report instead of retrying.

---

## 7. GitHub rules

- Work on a branch, push the branch, open a PR. Do not force-push. Do not rewrite
  published history. Do not touch tags or releases.
- Use `git mv` for renames so history is preserved.
- Leave the working tree clean. Generated artifacts (bench scratch files,
  `__pycache__`, caches) are removed or ignored, never committed.
- The final commit contains exactly the implementation plus its report — nothing
  incidental.
- Commit message: use the string given in the TZ's `## Commit Message` verbatim.

---

## 8. Validation rules

- Run every validation item the TZ lists. If one cannot be run, that item **fails**;
  it is never "not applicable".
- **Evidence, not assertion.** Every claim in the report is backed by a command and
  its output: check counts, exit codes, diff line counts, hashes.
- Baseline first: record the state before the change, so the diff is provable.
- **A validator that passes with no data is a failed validator** (invariant 22). Any
  check must count what it verified and fail on zero.
- **Printing a failure is not returning one** (invariants 25, 29). A step that
  reports failure on screen and exits 0 is a defect — report it as such.
- Any TZ that touches CI requires a **negative test**: force a real failure in the
  working tree, confirm the job turns red, revert, confirm the tree is clean.
  A gate never proven to fail is not a gate.
- Standing checks for any change to production files: `python3 -m py_compile main.py`
  and `node --check` on the `<script>` block extracted from `index.html`.

---

## 9. Report format

`CryptoReports/TZ-NN-<short-name>-report.md`:

```
# Implementation Report — TZ-NN
## Status                  ← COMPLETED / PARTIAL / BLOCKED
## Scope Executed
## Files Created
## Files Modified
## Files Renamed
## Files Deleted
## Implementation Summary
## Validation
## Test Results
## Deviations
## Pre-existing Issues
## Remaining Risks
## Commit
## Final Repository State
## System Map Fingerprint   ← line count + newest §9 migration date
```

Rules:

- English and Markdown. Never mix Russian into a report, a TZ, or a code comment
  written for this pipeline. (Russian remains correct inside `index.html` UI strings
  and in the System Map, which are pre-existing artifacts.)
- Distinguish precisely: completed · skipped · failed validation · pre-existing
  defect · remaining risk · work outside scope. Blurring these categories is the
  single failure mode that makes a report worthless.
- **Never claim completion without evidence.** "Verified" without a command and its
  output is not verification.
- State caveats plainly. A local replay of CI semantics is not a runner execution —
  say which one you did.
- Your chat reply is a convenience. The committed Markdown report is the record.

---

## 10. Ambiguity, pre-existing defects, blocked tasks

**Ambiguity.** If a requirement admits two reasonable readings that produce
different code, do not choose. Report BLOCKED, state both readings and which files
each would touch. Inventing a resolution silently is worse than stopping.

**Pre-existing defect.** Something already broken that your task did not cause:
diagnose it, prove it pre-existed (`git stash`, or run against unmodified HEAD),
record it under `## Pre-existing Issues`, and **do not fix it** unless the TZ says
so. Then continue with your actual task.

**Blocked.** Missing file, missing credential, failed fingerprint gate, network
policy, or a hard-floor conflict. Report BLOCKED with the precise obstacle and what
would unblock it. Do not partially implement around a blocker without saying so.

**Never improvise a corrective architectural change.** Corrections arrive as a new
TZ from the Architect.

---

## 11. Standing quality bar

- Minimal diff through existing structures. Two prior breakage incidents make this
  a hard rule, not a preference.
- No new dependency, no new build step, no new abstraction unless the TZ requires it.
- Leave the repository more verifiable than you found it — but only inside scope.
- When in doubt: stop and report. A blocked task costs one message. A silently
  wrong implementation of trading infrastructure costs money.
