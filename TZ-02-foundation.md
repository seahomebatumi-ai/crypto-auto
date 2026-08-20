# TASK

**TZ ID:** TZ-02
**Model:** Opus — this task resolves a rename/modify collision with real data-loss risk.

## Required System Map fingerprint

Verify before any work (`EXECUTOR-INSTRUCTIONS.md` §5). Check the map wherever it
currently lives — the canonical name does not exist yet and scope B creates it.

- Content anchors, all must be present:
  - `### 3.12 Direction engine — veto cascade (19.08.2026)`
  - an invariant numbered `36.` under `## 4. Инварианты — НЕ ЛОМАТЬ`
- Newest entry under `## 9. Журнал миграций` must be dated **2026-08-20**.
- Expected line count ≈ 1461, MD5 `9590fd08d149fb05d4db0d0179b54a50` (report the
  actual figures; do not block on them — upload can alter trailing whitespace).

If no copy in the repository satisfies the anchors and the migration date, **STOP and
report BLOCKED.**

---

## Objective

Put the repository into the finalized operating structure and restore automatic data
refresh. Two live problems and one missing capability:

1. **TZ-01 was never merged.** Its work sits on branch `claude/new-session-113so9`
   with an open pull request; `main` still carries the pre-TZ-01 state. Everything
   TZ-01 delivered — the bench gate, the scoped push trigger, the map rename — is not
   in effect. Meanwhile the Boss uploaded a fresh System Map and Executor contract
   directly to `main`, so the branch and `main` now disagree about the same file.
2. **The bot has no schedule.** `main.yml` has only `push` and `workflow_dispatch`.
   `coeffs.json` was refreshed only by pushes, and TZ-01 correctly narrowed the push
   trigger, which removes the last accidental refresh path. The frontend's staleness
   thresholds (`STALE_WARN_MIN = 75`, `STALE_CRIT_MIN = 130`, `index.html` 745–746)
   are calibrated against an hourly run (invariant 4), and System Map §1 describes the
   data flow as `GitHub Actions (cron ~1 раз/час)`. Without the schedule every 90-day
   metric on the board ages silently while the board keeps computing leverage and
   levels from it.
3. **The canonical artifact structure does not exist yet** — no `CryptoTZ/`, no
   `CryptoReports/`, and two artifacts landed with spaces in their filenames.

## Scope

- **A** — Land TZ-01 on `main` without losing the current System Map content. *(First. Everything else builds on it.)*
- **B** — Normalise artifact filenames to the canonical hyphenated set.
- **C** — Create `CryptoTZ/` and `CryptoReports/`; file this TZ into `CryptoTZ/`.
- **D** — Restore the hourly bot schedule. *(Critical.)*
- **E** — `.gitignore` for generated artifacts.
- **F** — Archive the TZ-01 implementation record under `CryptoReports/`.

Scopes are independent except that A precedes all others. If one is blocked, complete
the rest and report.

**Out of scope:** any change to `index.html`, `main.py`, `bench/**`, bench
expectations, `.github/workflows/backtest_bench.yml`, thresholds, constants, or the
`coeffs.json` schema. The red benches (`display_bench.py`, `render_bench.py`,
`direction_bench.py --display`) are known, diagnosed and reserved for TZ-03 —
**do not touch them.**

## Files to Create

- `CryptoTZ/TZ-02-foundation.md` — this file, moved from the repository root.
- `CryptoReports/TZ-01-repo-hardening-report.md`
- `CryptoReports/TZ-02-foundation-report.md`
- `.gitignore` — repository root.

## Files to Modify

- `.github/workflows/main.yml` — trigger block only.

## Files to Rename

- the System Map copy → `SYSTEM-MAP-CRYPTOCALCUL.md`
- the Executor-instructions copy → `EXECUTOR-INSTRUCTIONS.md`

## Files to Delete

Only superseded duplicates of the two artifacts above, once the surviving copy is
verified correct. Nothing else. **`image.PNG` stays** — `index.html` line 8 references
it as the PWA icon.

---

## Implementation Requirements

### A — Land TZ-01 on `main`

1. Determine the exact current state: `git log --oneline --graph --all -20`,
   `git branch -a`, and the diff between `main` and `claude/new-session-113so9`.
   Report it before acting.
2. Bring the branch up to date with `main` (merge `main` into the branch — do not
   rebase published history), resolve conflicts, and open or update the pull request.
   Do not merge it yourself; merging is the Boss's action.
3. **The System Map collision is the dangerous part and must be resolved
   deliberately.** `main` holds a freshly uploaded map (1461 lines, newest migration
   entry 2026-08-20). The branch holds a rename of the *older* map (1136 lines, newest
   entry 2026-08-14c). A default conflict resolution can easily keep the branch's
   stale content under the new name and silently discard six days of architecture.
   **Required final state: one map file, canonical name, containing the 2026-08-20
   content.** Verify by the anchors in the fingerprint header above, and state the
   line count, MD5 and newest migration date in the report.
4. Everything else TZ-01 delivered must survive intact: `.github/workflows/bench.yml`
   present and unmodified, `main.yml` carrying the TZ-01 `paths-ignore` list, no file
   deleted. Itemise the `paths-ignore` entries in the report.
5. If the collision cannot be resolved without ambiguity, **STOP and report BLOCKED**
   with both candidate states described. Losing the map is worse than a delayed task.

### B — Canonical filenames

1. Rename to the canonical hyphenated names using `git mv`:
   - the System Map copy → `SYSTEM-MAP-CRYPTOCALCUL.md`
   - the Executor-instructions copy → `EXECUTOR-INSTRUCTIONS.md`
2. Both artifacts currently exist on `main` with **spaces** in their filenames. This
   is a defect of the delivery path: the Architect's file-presentation layer renders
   an underscore as a space and the file is saved under the displayed name. All future
   Architect artifacts use hyphens for this reason. Do not "fix" it by restoring
   underscores.
3. If more than one copy of either artifact exists after scope A, keep the one whose
   content is correct — for the map, the one satisfying the fingerprint anchors; for
   the contract, the one whose first lines identify it as **Version 2** — and delete
   the other. Verify content before choosing. Report exactly which file survived and
   which was deleted, with both hashes.
4. Search the repository for references to the old names and update any that exist.

### C — Canonical directories

1. Create `CryptoTZ/` and `CryptoReports/`.
2. `git mv` this TZ from the repository root into `CryptoTZ/TZ-02-foundation.md`,
   normalising the filename if it arrived with spaces.
3. Directories are created by their first file; do not add placeholder or `.gitkeep`
   files unless the directory would otherwise be empty at commit time.

### D — Restore the hourly schedule

1. Add a `schedule` trigger to `main.yml`: `cron: '0 * * * *'`.
2. Do not remove, reorder or alter the existing `push` trigger, its `paths-ignore`
   list, or `workflow_dispatch`. Do not change env, secrets, permissions, concurrency,
   or any step inside the job.
3. `paths-ignore` applies to `push` only and must not affect `schedule`. Confirm this
   in the report.
4. **Forensics, required.** Run `git log --follow -p -- .github/workflows/main.yml`
   and determine whether a `schedule` trigger ever existed and, if so, which commit
   and date removed it. Report the finding — including "no schedule has ever been
   present in this file's history" if that is the answer. This distinguishes a silent
   regression from a documentation error in map §1, and the Architect needs to know
   which.
5. Do not touch `STALE_WARN_MIN` / `STALE_CRIT_MIN`. Invariant 4 pairs them with the
   cron interval, and that interval is being restored to the value they were
   calibrated for, not changed.
6. Do not add a CoinGecko API key or any key-related configuration. The bot runs
   keyless by design (map §5); a Demo key at hourly cadence exhausts the monthly quota
   mid-month.
7. If Actions are disabled on the repository, or scheduled workflows are suspended
   (GitHub suspends cron on inactive repositories), say so explicitly — restoring the
   YAML does not restore a suspended schedule.

### E — `.gitignore`

1. Create `.gitignore` at the repository root covering generated artifacts only:
   - Python: `__pycache__/`, `*.py[cod]`
   - Bench scratch files observed during TZ-01: `bench/_run.js`, `bench/_cases.json`
   - Any cache directory used by `backtest_bench.py` — read the file to find its
     actual path rather than guessing, and list what you added in the report.
   - OS noise: `.DS_Store`
2. **Do not ignore `index.html.prev` or `orig.html`.** They look like debris and are
   the baselines `badge_bench.js` and `direction_bench.py --identity` require; TZ-03
   will source them from git history instead. Ignoring them now forecloses that.
3. No currently tracked file may become ignored. Verify with `git ls-files` and
   `git status --ignored` before and after; report the comparison.

### F — Archive the TZ-01 record

1. Create `CryptoReports/TZ-01-repo-hardening-report.md` in the format of
   `EXECUTOR-INSTRUCTIONS.md` §10.
2. **Reconstruct it from repository evidence, not from memory or chat.** Use
   `git log`, `git diff --name-status -M`, the actual contents of `bench.yml` and
   `main.yml`, and a fresh run of the five gated benches. A record derived from the
   repository is verifiable; a transcription is not.
3. It must state accurately: the map rename (`R100`), the five gated benches with
   current check counts, the four benches left out with the reason for each, the
   `main.yml` trigger change, that no file was deleted, and the three red benches as
   pre-existing defects with their root cause — stale tier vocabulary and badge
   layout: production `tierOf` (`index.html` 1680–1685) emits `Фон` at the lowest tier
   and `tierBadge` (1925–1934) emits `Слово #N — score`, while the benches expect the
   pre-19.08 wording and ordering.
4. Under `## Deviations`, record that the TZ-01 negative test was run on all five
   gated benches although one was specified, and that it was a local replay of
   workflow semantics rather than a runner execution.
5. Under `## Pre-existing Issues`, record the missing schedule as discovered during
   TZ-01 and resolved by TZ-02, and the unmerged-branch state as the reason this
   record is being written retroactively.
6. Do not backdate. Mark the file as reconstructed under TZ-02, with the date.

---

## Validation

1. Exactly one System Map file exists, named `SYSTEM-MAP-CRYPTOCALCUL.md`, satisfying
   every fingerprint anchor. State its line count, MD5 and newest migration date.
2. Exactly one Executor-contract file exists, named `EXECUTOR-INSTRUCTIONS.md`, whose
   header identifies it as Version 2. State its MD5.
3. `git ls-files` shows no tracked filename containing a space.
4. `CryptoTZ/TZ-02-foundation.md` and `CryptoReports/TZ-01-repo-hardening-report.md`
   exist and are valid Markdown containing every required section.
5. `.github/workflows/bench.yml` is present and byte-identical to its state on branch
   `claude/new-session-113so9`. State its MD5 on both.
6. `main.yml` parses as valid YAML (state the tool) and exposes exactly three
   triggers: `schedule` (hourly), `push` with the TZ-01 `paths-ignore` list intact and
   itemised, and `workflow_dispatch`. Every job step byte-identical to before — hash
   the steps section before and after.
7. Trigger the workflow once manually (`workflow_dispatch`) and confirm it completes
   and that `coeffs.json` in the Gist receives a fresh `generated_at`. Report the
   timestamp before and after. If the run fails, **do not retry blindly** — report the
   failure with its log excerpt; a keyless CoinGecko rate limit and a broken workflow
   look different and the distinction matters.
8. The five benches gated by `bench.yml` run green: `verify_board.js` ·
   `board2_bench.js` · `prot_bench.js` · `verify_bench.py` ·
   `direction_bench.py --props --fixtures --control --sim`. Record check counts.
9. `python3 -m py_compile main.py` passes; `node --check` on the `<script>` block
   extracted from `index.html` passes. Neither file was modified — confirm by hash
   against the pre-task state.
10. `git ls-files` before and after `.gitignore`: identical set, no tracked file
    became ignored. `git status --porcelain` empty after commit.
11. No file deleted except the superseded artifact duplicates named in B.3, each
    listed with its hash.

## Deliverables

1. `CryptoReports/TZ-02-foundation-report.md` in the §10 format.
2. The repository state discovered in A.1, verbatim: branch graph and the `main` ↔
   branch diff.
3. How the System Map collision was resolved, and proof the 2026-08-20 content
   survived.
4. The result of D.4 (schedule forensics): whether a cron ever existed, and the commit
   and date that removed it.
5. The result of validation item 7: the manual run's outcome and both `generated_at`
   timestamps.
6. The exact `paths-ignore` list as it now stands.
7. The complete contents of `.gitignore`, and any path added beyond E.1 with its
   reason.
8. `## Fingerprints` for `SYSTEM-MAP-CRYPTOCALCUL.md`, `index.html` and `main.py`.
9. `## Pull Request` with URL, CI conclusion, and the sentence
   **NOT IN EFFECT UNTIL MERGED**.

## Commit Message

`chore(repo): land TZ-01, canonical artifact structure, restore hourly bot schedule`
