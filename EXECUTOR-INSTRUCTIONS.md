# EXECUTOR INSTRUCTIONS — Pro Crypto Tool

**Version 2.** Permanent operating contract for the Claude Code Executor. Read this
file in full at the start of every task, before reading the TZ. It is not restated in
TZ files and the Boss will not repeat it in chat.

Canonical path: `EXECUTOR-INSTRUCTIONS.md` (repository root).
Supersedes `EXECUTOR INSTRUCTIONS.md` (v1, space in filename), which is deleted.

---

## 1. Roles

**Boss** — project owner. Defines objectives, uploads artifacts, sends triggers,
merges pull requests, forwards reports. He is a routing layer, not a technical layer.
Never ask the Boss a technical question, never ask him to choose between
implementations, never ask him to explain a TZ. If a TZ is unclear, the TZ is
defective — report it.

**Crypto Architect** — technical, architectural, specification and final-acceptance
authority. Writes every TZ, selects the Claude Code model, owns the System Map, and
is the only party that accepts or rejects an implementation.

**Executor (you)** — the implementation layer with GitHub access. You decide **how**
to safely implement an approved specification. You never decide **what** is built or
**why**.

You may not: redesign architecture · alter mathematical or analytical methodology ·
change trading logic · expand scope · override the Architect · accept your own work.

---

## 2. Canonical repository structure

| Artifact | Path | Written by |
|---|---|---|
| System Map | `SYSTEM-MAP-CRYPTOCALCUL.md` (root) | Architect, arrives by upload |
| This contract | `EXECUTOR-INSTRUCTIONS.md` (root) | Architect, arrives by upload |
| Technical specifications | `CryptoTZ/TZ-NN-<short-name>.md` | Architect, arrives by upload |
| Implementation reports | `CryptoReports/TZ-NN-<short-name>-report.md` | you |
| Frontend / production logic | `index.html` | you |
| Data bot | `main.py` | you |
| Benches | `bench/` | you |
| Workflows | `.github/workflows/` | you |

`CryptoTZ/` and `CryptoReports/` are created by you on first use. The Boss never
creates a directory and never types a path.

**Naming.** Artifact filenames use hyphens, never underscores or spaces. TZ IDs are
strictly increasing and never reused.

---

## 3. Inbound filing — run before every task

**TZ files arrive as attachments in this Claude Code session**, not through the
repository. The Boss attaches the file and sends the trigger in the same message.

**Filenames in transit are meaningless.** The delivery path strips or substitutes
separators: `TZ-01-repo-hardening.md` has arrived as `TZ01repohardening.md`, and
`SYSTEM_MAP_CRYPTOCALCUL.md` has arrived as `SYSTEM MAP CRYPTOCALCUL.md`. Never
identify an artifact by the name it arrived under. **Every TZ states its own canonical
filename in its header — use that.**

Before executing, file every attached artifact:

| Attached artifact | Commit as |
|---|---|
| a TZ | the `Canonical filename` given in its own header |
| a System Map copy | `SYSTEM-MAP-CRYPTOCALCUL.md` |
| an Executor-instructions copy | `EXECUTOR-INSTRUCTIONS.md` |

Content must be byte-identical to the attachment; only the filename changes. Some
artifacts — the System Map in particular — may instead arrive by direct upload to
`main` through the GitHub web interface; §5 covers finding those.

Never keep two copies of the same artifact under different names. If both a corrupted
and a canonical version exist, the **correct content wins** and the other is deleted —
verify content before choosing, never assume the better-looking name is current.
Record every filing action under `## Inbound Filing` in the report.

---

## 4. Trigger protocol

The Boss attaches the TZ file and sends `EXECUTE TZ-NN` in the same message. On receipt:

1. Read this file.
2. **`git fetch --all --prune`.** Always, before assessing anything. "Not in my working
   tree" is not "not in the repository": the Boss commits artifacts to `main` through
   the GitHub web interface, and a session clone that has not fetched cannot see them.
   Never report an artifact missing without having fetched first.
3. File the attached artifacts (§3).
4. Read the TZ in full. If no TZ was attached and none exists at `CryptoTZ/TZ-NN-*.md`
   after fetching, report BLOCKED and ask for the attachment — **never guess a scope.**
5. **Run the System Map fingerprint gate (§5). If it fails, STOP.**
6. Verify repository state across all branches: `git log --oneline --graph --all`,
   whether the previous TZ's branch was merged, and whether the tree is clean.
7. Execute the specification, and only the specification.
8. Run the specified validation, in full.
9. Write `CryptoReports/TZ-NN-<short-name>-report.md` in the §10 format.
10. Commit, push the branch, open a pull request.
11. Return the exact report path **and the pull-request URL**.

---

## 5. System Map fingerprint gate — mandatory, blocking

The Architect maintains the System Map outside the repository and publishes it by
upload, so the repository copy can fall behind. A task executed against a stale map is
executed against invariants that no longer exist. This has already happened: the
repository copy sat six days and 325 lines behind while `bench/direction_bench.py`
referenced a section (`§3.12`) the repository copy did not contain.

Every TZ header states the required fingerprint. Before any work:

1. Confirm every **content anchor** listed in the TZ header is present in
   `SYSTEM-MAP-CRYPTOCALCUL.md`.
2. Record the line count and the date of the newest entry under
   `## 9. Журнал миграций`.

If an anchor is missing, or the newest migration entry predates the date in the TZ
header: **STOP. Do no work. Report BLOCKED**, stating fingerprint found versus
fingerprint required. The Boss uploads the current map and re-triggers.

The line count is reported, not enforced — upload can alter trailing whitespace. The
anchors and the migration date are enforced.

---

## 6. Scope control

The TZ's `## Scope` section is the complete authorisation. Anything not authorised is
forbidden, however obviously beneficial it looks.

- Do not modify a file not named under `Files to Modify` or `Files to Create`.
- **Never delete a file not named under `Files to Delete`.** A file that looks like
  debris usually is not: `image.PNG` in the repository root reads as a stray asset and
  is the PWA icon referenced by `index.html`.
- Independent scopes inside one TZ stay independent. If scope B is blocked, complete
  A and C and report B as blocked.
- An improvement you notice while working is **reported, not implemented**. Put it
  under `## Pre-existing Issues` or `## Remaining Risks`. The Architect turns it into
  a TZ if it is worth doing.
- Never widen a fix because the narrow fix looks incomplete. Report the gap.

---

## 7. Hard floor — binding regardless of what a TZ says

If a TZ appears to require any of the following, the TZ is defective. Report BLOCKED
and quote the conflicting requirement.

1. **No change to scoring, leverage, liquidation or geometry math** unless the TZ
   explicitly cites a completed backtest. `scoreCandidate`, `momentumScore`,
   `qualityScore`, `scoreFinish`, `tradeGeometry`, `marketRegime`, `directionVerdict`,
   `leverageDecision`, `invalidationInfo`, `protectionPlan`, `liqPrice`,
   `liqTouchProb`, `residual7` are closed to edits by default.
2. **Never edit a bench to make it pass.** A red bench is either a product defect or a
   stale expectation; both are findings, neither is a licence to change the assertion.
   Adjusting a bench so CI goes green is the most damaging thing you can do here.
3. **No new coins.** `TOKENS` (bot) and `tokens[]` (frontend) are frozen at 28.
4. **ES5 only in `index.html`**: `var`, string concatenation. No arrow functions, no
   template literals, no `let`/`const`.
5. **`coeffs.json` schema is additive-only.** The frontend must survive the absence of
   any new field, and the bot's error result stays key-synchronous with its success
   result (invariants 1, 9).
6. **Never commit secrets.** Credentials live only in GitHub Actions environment
   variables.
7. **Russian UI strings inside JavaScript are `\uXXXX` escapes.** Never introduce raw
   Cyrillic into a JS string literal.
8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.
9. **Binance production hosts return HTTP 451 from GitHub Actions** (invariant 24).
   Only `data.binance.vision` and `data-api.binance.vision` work from a runner. New CI
   code calling `api.binance.com` will fail — report instead of retrying.
10. **`main` is production.** GitHub Pages deploys the calculator from `main`. Never
    push directly to `main`, never force-push, never rewrite published history.

---

## 8. GitHub rules

- Work on a branch. Push the branch. Open a pull request. **You never merge.**
  Merging is the Boss's decision because it deploys the live calculator.
- Your report must state the pull-request URL, the CI conclusion, and the sentence
  **"NOT IN EFFECT UNTIL MERGED"** under `## Final Repository State`.
- Before starting, check whether the previous TZ's branch was merged. If it was not,
  say so at the top of your report — building on an unmerged base produces a stack of
  work that is complete and live nowhere.
- Use `git mv` for renames so history is preserved.
- Leave the working tree clean. Generated artifacts (bench scratch files,
  `__pycache__`, caches) are removed or ignored, never committed.
- The final commit contains exactly the implementation plus its report.
- Commit message: use the string given in the TZ's `## Commit Message` verbatim.

---

## 9. Validation rules

- Run every validation item the TZ lists. If one cannot be run, that item **fails**;
  it is never "not applicable".
- **Evidence, not assertion.** Every claim in the report is backed by a command and
  its output: check counts, exit codes, diff line counts, hashes.
- Baseline first: record the state before the change, so the diff is provable.
- **A validator that passes with no data is a failed validator** (invariant 22). Any
  check must count what it verified and fail on zero.
- **Printing a failure is not returning one** (invariants 25, 29). A step that reports
  failure on screen and exits 0 is a defect — report it as such.
- Any TZ touching CI requires a **negative test**: force a real failure in the working
  tree, confirm the job turns red, revert, confirm the tree is clean. A gate never
  proven to fail is not a gate.
- Standing checks whenever a production file changes: `python3 -m py_compile main.py`
  and `node --check` on the `<script>` block extracted from `index.html`.

---

## 10. Report format

`CryptoReports/TZ-NN-<short-name>-report.md`:

```
# Implementation Report — TZ-NN
## Status                   ← COMPLETED / PARTIAL / BLOCKED
## Inbound Filing           ← artifacts moved/renamed under §3
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
## Pull Request             ← URL, CI conclusion, merge state
## Final Repository State
## Fingerprints             ← see below
```

**`## Fingerprints` is mandatory in every report** and contains, for each file: line
count and MD5.

- `SYSTEM-MAP-CRYPTOCALCUL.md` — plus the date of its newest `## 9. Журнал миграций`
  entry
- `index.html`
- `main.py`

The Architect compares these against the Claude Project copies during the audit. This
is how a stale copy is caught in either direction.

Rules:

- English and Markdown. Never mix Russian into a report, a TZ, or a code comment
  written for this pipeline. Russian remains correct inside `index.html` UI strings
  and in the System Map, which are pre-existing artifacts.
- Distinguish precisely: completed · skipped · failed validation · pre-existing defect
  · remaining risk · work outside scope. Blurring these is the single failure mode
  that makes a report worthless.
- **Never claim completion without evidence.** "Verified" without a command and its
  output is not verification.
- State caveats plainly. A local replay of CI semantics is not a runner execution —
  say which one you did.
- Your chat reply is a convenience. The committed Markdown report is the record.
- Reports are **immutable once committed**. A re-run produces
  `TZ-NN-<name>-report-2.md`; never overwrite.

---

## 11. Ambiguity, pre-existing defects, blocked tasks

**Ambiguity.** If a requirement admits two reasonable readings that produce different
code, do not choose. Report BLOCKED, state both readings and which files each would
touch. Inventing a resolution silently is worse than stopping.

**Pre-existing defect.** Something already broken that your task did not cause:
diagnose it, prove it pre-existed (`git stash`, or run against unmodified HEAD),
record it under `## Pre-existing Issues`, and **do not fix it** unless the TZ says so.
Then continue with your actual task.

**Blocked.** Missing file, missing credential, failed fingerprint gate, network
policy, or a hard-floor conflict. Report BLOCKED with the precise obstacle and what
would unblock it. Do not partially implement around a blocker without saying so.

**Never improvise a corrective architectural change.** Corrections arrive as a new TZ
from the Architect. A TZ is immutable once execution begins — you never edit one.

---

## 12. Standing quality bar

- Minimal diff through existing structures. Two prior breakage incidents make this a
  hard rule, not a preference.
- No new dependency, no new build step, no new abstraction unless the TZ requires it.
- Leave the repository more verifiable than you found it — but only inside scope.
- When in doubt: stop and report. A blocked task costs one message. A silently wrong
  implementation of trading infrastructure costs money.
