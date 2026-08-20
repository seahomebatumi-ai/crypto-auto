# TASK

**TZ ID:** TZ-03
**Canonical filename:** `CryptoTZ/TZ-03-report-delivery.md`
**Model:** Sonnet — mechanical: one file already in place, one deletion, one added print
statement, one read-only check. No merge risk, no math, no schema change.

> Filenames degrade in transit. Commit this file under the canonical path above, taken
> from this header, never from the name it arrived under.

## Precondition

**Pull request #1 (TZ-02) must be merged before this task starts.** Run
`git fetch --all --prune` and confirm `origin/main` contains
`SYSTEM-MAP-CRYPTOCALCUL.md`, `.gitignore`, `CryptoTZ/TZ-02-foundation.md` and a
`schedule` trigger in `main.yml`. If it does not, **STOP and report BLOCKED** — this task
assumes a merged base and would otherwise stack a second unmerged branch on the first.

## Required System Map fingerprint

- Anchors: `### 3.12 Direction engine — veto cascade (19.08.2026)`, and an invariant
  numbered `36.` under `## 4. Инварианты — НЕ ЛОМАТЬ`.
- Newest `## 9. Журнал миграций` entry: **2026-08-20**.
- Expected: 1461 lines, MD5 `9590fd08d149fb05d4db0d0179b54a50`.

Mismatch → **BLOCKED**.

---

## Objective

Close the report-delivery gap, remove the duplicate it produced, and make data freshness
verifiable from inside CI.

TZ-02's report was written onto the implementation branch, where the Boss could not reach
it without navigating a pull request. He had to issue a second, unplanned instruction to
get a copy placed somewhere reachable, and that copy — `LATEST-REPORT.md` — is now a
duplicate artifact in the repository root. The mechanism was wrong, not the naming: the
audit gates the merge, so the report cannot sit behind the merge.

Separately, TZ-02 validation item 7 failed because nothing in the workflow log carries
the `generated_at` the bot writes to the Gist, and the session cannot read the Gist. One
print statement makes every future run self-evidencing.

## Scope

- **A** — Install `EXECUTOR-INSTRUCTIONS.md` Version 4 and operate under it.
- **B** — Remove the `LATEST-REPORT.md` duplicate.
- **C** — Make `generated_at` visible in the workflow log.
- **D** — Confirm the restored cron fires. *(Read-only. Change nothing.)*

Scopes are independent. If one is blocked, complete the rest and report.

**Out of scope:** any change to scoring, leverage, geometry or liquidation math; the
`coeffs.json` schema; `index.html`; `bench/**`; bench expectations; workflow triggers.
The three stale display benches are reserved for TZ-04 — **do not touch them.**
**Do not disable, alter or replace any automation outside the repository.**

## Files to Create

- `CryptoReports/TZ-03-report-delivery-report.md` — **committed directly to `main`**.

## Files to Modify

- `main.py` — one added line, scope C.

## Files to Delete

- `LATEST-REPORT.md` (repository root).

Nothing else. `image.PNG` stays.

---

## Implementation Requirements

### A — Version 4 contract

1. The Boss uploads `EXECUTOR-INSTRUCTIONS.md` (Version 4) to the repository root before
   this task is triggered. **Verify after fetching that the file at the root reads
   `**Version 4.**` on line 3.** If it reads any earlier version, **STOP and report
   BLOCKED**, quoting the version line found — the delivery rules in §3, §8 and §11
   govern this task's own execution, and running under a superseded contract would
   reproduce the failure this TZ exists to fix.
2. Do not edit, reconstruct or "improve" the contract. It is an Architect artifact.
3. **Version 4 governs this task's own report:** committed to `main`, never onto the
   branch, followed by the two-line Russian closing message of §11 and nothing more.

### B — Remove the duplicate

1. Delete `LATEST-REPORT.md` from the repository root.
2. **Guard first.** Confirm `CryptoReports/TZ-02-foundation-report.md` exists on `main`
   and carries the same report. Compare content and state the result. If they differ in
   substance, **STOP and report BLOCKED** — the duplicate may hold something the
   canonical copy does not.
3. Do not replace it with a symlink, a pointer, or a `latest` alias of any kind. One
   report, one path, one copy.

### C — `generated_at` in the log

1. In `main.py`, immediately after `generated_at` is assigned from `now_utc.isoformat()`,
   add a single `print` emitting it in a greppable form, for example
   `print("generated_at=" + generated_at, flush=True)`.
2. **Locate the assignment by searching for it, not by line number.** The Architect's
   Project copy of `main.py` is one line behind the repository copy, so any line number
   quoted here would be wrong. Report the actual line number found.
3. Add nothing else: no new field, no schema change, no logging framework, no change to
   what is written to the Gist. The `coeffs.json` payload must be byte-for-byte what it
   would have been (invariants 1, 9).
4. Place the print on the success path before the Gist PATCH, so a run that reaches the
   PATCH has already logged the value.
5. If `main.py` writes to stdout in a way a print would corrupt — a piped payload, a
   structured log consumer — **stop and report instead.** Verify before adding.

### D — Cron confirmation (read-only)

Change nothing in this scope. Report facts only.

1. After the TZ-02 merge, `main.yml` on the default branch carries
   `schedule: '0 * * * *'`. List recent `Crypto Update` runs with their `event` field and
   report whether any run has `event: schedule`, with its timestamp. If none has appeared
   yet, say so and give the merge time so the Architect can judge whether enough time has
   passed.
2. Report the count of runs by event over the last 48 hours: `schedule`,
   `workflow_dispatch`, `push`.
3. **Context, so this is not re-investigated:** the hourly `workflow_dispatch` is the
   Boss's own iPhone Shortcut, built deliberately. It is identified, it is not unknown
   infrastructure, and **it is not yours to touch.** The Architect decides whether the
   repository cron or the Shortcut is retired, and the Boss executes that decision
   outside the repository.

---

## Validation

1. `EXECUTOR-INSTRUCTIONS.md` at the repository root reads `**Version 4.**` on line 3.
   State its line count and MD5.
2. `LATEST-REPORT.md` is absent from `git ls-files`, and
   `CryptoReports/TZ-02-foundation-report.md` is present on `main`. State both hashes and
   the comparison result from B.2.
3. `python3 -m py_compile main.py` passes.
4. **The added print does not alter the payload.** Show the comparison of the
   `coeffs.json` key set before and after, produced with the network stubbed. Asserting
   it is not sufficient. If the payload cannot be built offline, say so and instead show
   that the only change to `main.py` is the single added line — `git diff --stat` plus
   the diff itself.
5. `git diff` on `main.py` is exactly one added line, zero removed, zero modified.
6. `node --check` on the `<script>` block extracted from `index.html` passes, and
   `index.html` is byte-identical to its pre-task hash.
7. The five gated benches run green: `verify_board.js` · `board2_bench.js` ·
   `prot_bench.js` · `verify_bench.py` ·
   `direction_bench.py --props --fixtures --control --sim`. Record check counts.
8. **Dispatch the workflow once and confirm `generated_at` now appears in the log.**
   Quote the log line verbatim. This is what TZ-02 item 7 could not do; it is the point of
   scope C, and it must be shown on a real runner, not locally.
9. `git status --porcelain` empty; no scratch file committed; `git ls-files` contains no
   filename with a space.
10. The report exists at `CryptoReports/TZ-03-report-delivery-report.md` **on `main`**,
    and `git log origin/main -1 -- CryptoReports/` shows it. Nothing but
    `CryptoReports/**` was pushed to `main`.

## Deliverables

1. `CryptoReports/TZ-03-report-delivery-report.md`, on `main`, per contract §10.
2. The verbatim log line from validation item 8.
3. Scope D: cron-fired yes/no with timestamp, and the 48-hour event counts.
4. The actual `main.py` line number where `generated_at` is assigned, and the one-line
   diff.
5. `## Fingerprints` for `SYSTEM-MAP-CRYPTOCALCUL.md`, `index.html` and `main.py` — line
   count and MD5 each. The Architect's copy of `main.py` is known stale; these figures
   correct it.
6. `## Pull Request` with URL, CI conclusion, and **NOT IN EFFECT UNTIL MERGED**.
7. The Russian closing message per contract §11.

## Commit Message

`chore(ops): report delivery to main, contract v4, log generated_at`
