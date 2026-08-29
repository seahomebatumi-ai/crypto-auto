# TZ-19 — Return `live-gate.sh` to its own control

**Canonical filename:** `TZ-19-gate-script-under-gate.md`
**Directory:** `CryptoTZ/`
**Report:** `CryptoReports/TZ-19-gate-script-under-gate-report.md`
**Model:** **Sonnet.** One YAML list edited in one file, with a filter evaluation and a
runner check. No math, no diagnosis, no production code.

**Predecessor:** `CryptoReports/TZ-18-gate-floor-and-md-filter-report.md`, ПРИНЯТО and
merged. This closes that report's `## Remaining Risks` item 1, which is a defect of
TZ-17's specification, not of either implementation.

**Requires `EXECUTOR-INSTRUCTIONS.md` version 10 or later.**

---

## 0. Required System Map fingerprint — quoted IN FULL

**Revision 2026-08-29-b.** Baseline: TZ-18 merged into `main`; implementation
commit `8f45ea8`, report `CryptoReports/TZ-18-gate-floor-and-md-filter-report.md`. **The
baseline names the implementation commit, not the merge commit** — a merge commit
carries no content, and content is what this block pins.

Every TZ header quotes this block IN FULL — all seven anchors and the file table,
never a subset. The Executor matches each anchor as an exact substring against the
repository copy before any work (contract §5); any mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-29-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `52. **A filter is measured on the runner, never derived from the pattern.**` |

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

Gate at this revision: `bench.yml`, **13 steps, 1 250 717 checks**, green on the
hosted runner (run `33251833997`, head `8f45ea8`, all 13 steps `success`). Step 13
(`analyst/live-gate.sh --selftest`) reads **40**; steps 1–12 sum to **1 250 677**, step 7
at **691 109**, step 12 at **220 598**, unmoved through TZ-17 and TZ-18.

**This TZ modifies none of the four files above,** and none of steps 1–13 may move: it
edits a trigger filter and nothing a bench reads.

---

## 1. The defect

TZ-17 put `'analyst/**'` in `bench.yml`'s `push.paths-ignore` so an analysis run saving
its own state would not burn a 13-step gate. That reasoning is correct for the analyst's
**data**. But `analyst/live-gate.sh` lives in the same tree, and it is **code with a
control** — step 13 is its selftest.

Consequence: a commit that changes only the gate script does not run the gate that
proves the gate. TZ-18 was unaffected because it also touched both workflow files, so
step 13 ran; the next script-only change would land with no runner evidence at all.
That is exactly the shape inv. 37 names — a bench outside the gate is not a control —
and it is invisible, because the workflow that would have complained is the one that
does not start.

**The ignore was written for a tree and the tree holds two classes of file.** The fix is
to name the analyst's *written* paths rather than its directory.

---

## 2. Scope

| Path | Change |
|---|---|
| `.github/workflows/bench.yml` | replace `- 'analyst/**'` with three narrower entries |

Nothing else. **Files to Delete:** none.

**`main.yml` is not touched.** Its `'analyst/**'` is correct as it stands: no file under
`analyst/`, script included, is a reason to start the bot, redraw 28 coins through
CoinGecko and rewrite the live Gist.

---

## 3. The change

In `.github/workflows/bench.yml`, `on.push.paths-ignore`, replace the single entry

```yaml
      - 'analyst/**'
```

with, in this order and in the same position in the list:

```yaml
      # Данные аналитика: состояние, журнал и payload от шортката.
      # Скрипт шлюза сюда не входит намеренно — его контроль это шаг 13.
      - 'analyst/state.json'
      - 'analyst/live.json'
      - 'analyst/log/**'
```

The comment is required and its second line is load-bearing: it is the only place a
future reader learns that the omission of `live-gate.sh` is deliberate rather than an
oversight, and an unexplained narrow filter invites being widened back (inv. 50).

`analyst/README.md` needs no entry — `'**.md'`, added by TZ-18, already covers it.

---

## 4. Validation — written by the Architect

1. **Filter evaluation, both directions, from a real changed-file list.** Reuse the
   evaluator and the throwaway-clone method of the TZ-18 report: files really modified
   in a scratch clone, the list read from `git diff --name-only` and never typed, the
   `paths-ignore` list parsed out of the committed YAML with a YAML parser. BEFORE is
   the YAML at `main`; AFTER is the YAML on the branch.

   | Changed files | before | after |
   |---|---|---|
   | `analyst/live-gate.sh` | NOT RUN | must **RUN** |
   | `analyst/state.json` | NOT RUN | must NOT run |
   | `analyst/live.json` | NOT RUN | must NOT run |
   | `analyst/log/2026-08-29.md` | NOT RUN | must NOT run |
   | `analyst/README.md` | NOT RUN | must NOT run |
   | `analyst/state.json` + `analyst/live-gate.sh` | NOT RUN | must **RUN** |
   | `main.py` | RUNS | must **RUN** |

   Row 1 is the repair; rows 2–5 are the property that must survive it; row 6 proves a
   mixed commit is not swallowed; row 7 is the control that a filter matching nothing
   would fail.

2. **The same seven rows against `main.yml`, which must not move.** Every row must
   return NOT RUN except `main.py`, before and after, identically. A change to
   `bench.yml` that altered `main.yml`'s behaviour would mean the evaluator is reading
   the wrong file.

3. **Runner evidence, and it is the point of the change** (inv. 52 — a filter is
   measured on the runner, not derived). After pushing the branch, report the `Bench
   gate` run id, head and conclusion. Then push a **second** commit to the branch
   touching `analyst/live-gate.sh` and nothing else — a comment line added and then
   removed is sufficient, leaving the file byte-identical to the first commit — and
   report whether `Bench gate` ran for it. **That second run is the acceptance
   evidence**; the filter evaluation alone is what this repository has already been
   wrong with once.
4. Full gate, 13 steps, per-step counter table. Steps 1–12 must total **1 250 677**,
   step 13 must read **40**, total **1 250 717**. Any movement is a finding reported
   before anything else.
5. `git diff --stat` — one file, `.github/workflows/bench.yml`. Quote the diff.
6. MD5 and line counts for the four files in §0 — identical to §0.
7. MD5 and line counts for the map, `EXECUTOR-INSTRUCTIONS.md`, `ANALYST-INSTRUCTIONS.md`
   and `analyst/live-gate.sh`, with version and revision strings. `live-gate.sh` must be
   **byte-identical to `main`** — this TZ does not touch it.

**Do not run an analysis** and do not touch `analyst/live.json`. Its content is a known
producer defect (TZ-18 report, `## Pre-existing Issues` 1) and is being fixed at the
Shortcut, outside the repository.

---

## 5. Commit Message

```
fix(ci): narrow bench.yml analyst ignore so the gate script runs its own gate (TZ-19)
```

---

## 6. Acceptance criteria

1. A push touching only `analyst/live-gate.sh` starts `Bench gate` — **proven by a real
   run on the runner**, not by evaluation.
2. Pushes touching only `analyst/state.json`, `analyst/live.json` or `analyst/log/**`
   still start neither workflow.
3. `main.yml` behaviour is unchanged on all seven rows.
4. The gate is green at 13 steps; steps 1–12 at 1 250 677 and step 13 at 40, unmoved.
5. Exactly one file changed.

---

## 7. Deliberately not done

`[решение принято мной]`

- **`main.yml` keeps `'analyst/**'`.** Narrowing it there would let a gate-script commit
  start the bot, which is a cost with no benefit: `main.py` does not read the script.
- **No `paths` allow-list.** Standing matter, recorded in inv. 52 and the open queue;
  converting a deny-list to an allow-list changes the trigger for every path in the
  repository at once and needs a TZ that enumerates them.
- **No move of `live-gate.sh` out of `analyst/`.** Relocating the script to `bench/`
  would also fix this and would put the gate away from the thing it gates; the tree is
  the analyst's and the script belongs to it. The filter is the wrong object to work
  around, and it is the object that was wrong.
