# TZ-59 — The run's pinned model and its effort

**Canonical filename:** `CryptoTZ/TZ-59-run-model-pin.md`
**Report:** `CryptoReports/TZ-59-run-model-pin-report.md`
**Host:** any machine. **No stage reads or changes the VPS**: every fact this TZ rests on is already in
TZ-58's report, and the code reaches the server only through the deployer after the merge.
**Class:** branch TZ (contract §8) — it modifies two files under `vps/**`.
**Branch:** `tz-59-run-model-pin` · **Model:** Sonnet
**Previous TZ:** TZ-58, PARTIAL — its branch `tz-58-vps-fit-model-stream-list` at `a172529` is accepted
and **must be merged before this TZ starts** (A1); its reports are on `main`.
**Written against:** contract v26, map `2026-10-03-e`, methodology `2026-10-03-a`, TZ-58's report
`CryptoReports/TZ-58-vps-fit-model-stream-list-report-2.md`, and TZ-58's branch at `a172529` — its `vps`
tree `94a55b6f07d6aa6b2290eb3b4646f1740cd1a47e` — read by the Architect from the repository on
04.10.2026. Map §10 row «The assistant's build sequence», item (17) with the decision of `2026-10-03-e`,
is what this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-03-e.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-03-e.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this TZ's gate adds:

| Added file | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | its version line reads `**Version 26.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `vps/run.py` | 331 | `4be5ada20662f7876715b15b5250722d` | reported; a different file is a finding, never a block |

The map itself: 3205 lines, MD5 `255286398a8f28203717a4187d9124f6` — reported, not enforced. The tree
`origin/main:vps` is reported beside them; `94a55b6f07d6aa6b2290eb3b4646f1740cd1a47e`, TZ-58's branch's
tree, is the one this TZ was written against, and a different one is a finding, never a block.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened, and the `claude` binary is
not run.**

---

## 2. Contract and map text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> **Decided at `2026-10-03-e`:** TZ-59 pins `claude-opus-5-5` at `--effort high` on that reading, with no stage on the VPS, because every fact it rests on is already in TZ-58's report

— map §10, row «The assistant's build sequence».

> the binary `/usr/bin/claude` 2.1.282 wraps the levels of `--effort` — `low, medium, high, xhigh, max` — onto the next line, which the session's own probe printed

— map §10, row «The assistant's build sequence».

---

## 3. What is built

The analysis run starts the session on a pinned model at a set effort — `claude-opus-5-5` at `--effort
high` — in place of the alias `opus` at the model's default effort. Nothing else in the run moves.
**Derivation of the facts it rests on, all read on the VPS by TZ-58** (report-2): the run unit reaches
`/usr/bin/claude`, version `2.1.282 (Claude Code)` (A4); its `--effort <level>` entry wraps onto a second
line reading `(low, medium, high, xhigh, max)` (D-2). Claude Code's «Model configuration» page, read by
the Architect's session on 03.10.2026: Opus 5.5 requires v2.1.280 or later, offers all five levels,
defaults to `medium`, and is pinned by its full name `claude-opus-5-5`.

---

## 4. Scope

### Files to Modify

```
vps/run.py         vps/selftest.py
```

### Files to Create

None.

### Files to Delete

None.

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **Any other line of `vps/run.py`** — the prompt, the tools, the admission, the summary lines.
- **Every other file under `vps/`**, `bench.yml`, the methodology.
- **The cost of a run at `high`.** The next run logs its usage; the TZ that reads the first six runs
  after TZ-57's merge reads it (map §10).

---

## 6. Rules — binding in every stage

1. **No model session**, and the `claude` binary is not run.
2. **Python 3.12's standard library only.**
3. **No network read** besides `git`'s and `gh`'s.
4. **No new Russian text.**

---

## 7. Stage A — readings, no writes

- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then
  `git merge-base --is-ancestor a17252950267c2d0261ee96238784415ddae5453 origin/main` → exit 0. **Exit 1:
  BLOCKED** — TZ-58's accepted implementation is not merged, and this TZ is written against its tree;
  the report says so and nothing else is done.

---

## 8. Stage B — the code, on the branch

### B1. `vps/run.py` — §11.1

### B2. `vps/selftest.py` — §11.2

---

## 9. Validation

- **V1. Selftest.** `python3 vps/selftest.py`: exit 0, every section non-empty, the total printed.
  **Negative control** (inv. 68): `EFFORT = "high"` changed to `EFFORT = "medium"` in the working tree →
  exit non-zero with section O alone failing; reverted; green again, MD5 restored.
- **V2. Syntax.** `python3 -m py_compile vps/run.py vps/selftest.py`.
- **V3. The command line.** `python3 -c 'import sys; sys.path.insert(0, "vps"); import run; print(run.CLAUDE[3:])'`
  prints `--model`, `claude-opus-5-5`, `--effort`, `high`, and no element equal to `opus`.
- **V4. No production file.** `git diff --name-only origin/main...HEAD` lists exactly `vps/run.py` and
  `vps/selftest.py`.
- **V5. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main` receives
  nothing from this session but its report.

---

## 10. The report

Contract §10's template. **The first line after `## Status` states the command line the run will use** —
V3's printed list — and the second that the deployer installs it at the merge, so the first run after
the merge is the first at `high`.

---

## 11. Dictated blocks

### 11.1 `vps/run.py`

The `CLAUDE` assignment becomes exactly these lines, with the two constants immediately above it:

```
MODEL  = "claude-opus-5-5"
EFFORT = "high"
CLAUDE = ["claude", "-p", PROMPT,
          "--output-format", "json", "--model", MODEL, "--effort", EFFORT,
          "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch",
          "--append-system-prompt", APPEND]
```

The module docstring names TZ-59.

### 11.2 `vps/selftest.py` — section O gains three checks

| Check | Known answer |
|---|---|
| `run.CLAUDE` carries `--model` immediately followed by `claude-opus-5-5` | true |
| `run.CLAUDE` carries `--effort` immediately followed by `high` | true |
| no element of `run.CLAUDE` equals `opus` | true |

Every other section stays green.

---

## 12. Commit messages

Implementation, on the branch:

```
TZ-59: vps — the run on claude-opus-5-5 at high effort
```

Report, on `main`:

```
TZ-59: report — the run's pinned model and effort
```
