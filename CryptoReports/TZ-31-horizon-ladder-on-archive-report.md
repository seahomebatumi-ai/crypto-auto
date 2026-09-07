# Implementation Report — TZ-31

## Status

**BLOCKED.**

The System Map fingerprint gate PASSED in full. Work stopped at contract §4a step 7
under contract §12 (Ambiguity): the TZ's `## 6. Validation` specifies a control for a
different instrument than the one `## 2. Scope` authorises, and the two readings produce
different code, different assertions and a different registered claim. No file was
modified and no branch was opened.

## Inbound Filing

The TZ was already present under its canonical filename on `origin/main`. No `git mv` was
required and no artifact was renamed.

One fact about how it arrived matters to the audit. At session start the worktree stood at
`8bd691f` and carried an EARLIER revision of this TZ. `git fetch --all --prune` (contract
§3) showed `origin/main` at `eeaa395`, two commits ahead, and the intervening commits were:

| Commit | Subject |
|---|---|
| `3327ca7` | `Delete CryptoTZ/TZ-31-horizon-ladder-on-archive.md` |
| `eeaa395` | `Add files via upload` |

The TZ was deleted and re-uploaded — it was **replaced, not amended**. The tree was brought
to `origin/main` by `git merge --ff-only origin/main`; `git status --porcelain` is empty and
`HEAD` is `eeaa395e121eee59a25bc3e5e21eba0bd410087c`. All work below is against the
re-uploaded revision, which is the current one.

The replacement is material and is the origin of the blocker. Measured against the
superseded copy:

```
$ diff <(sed -n '/^## 6. Validation/,/^## 7. Report/p' <old>) \
       <(sed -n '/^## 6. Validation/,/^## 7. Report/p' <new>)
*** §6 VALIDATION: BYTE-IDENTICAL between the two revisions ***
```

Sections §1, §2, §3 and §4 were rewritten from a horizon-ladder arm to a regime-gate arm.
Section §6 was carried across unchanged.

## Scope Executed

**Class: branch TZ.** Read off the TZ's `## Scope` per contract §8 — it authorises three
files outside `CryptoReports/**` (`bench/backtest_bench.py`,
`bench/backtest_guard_bench.py`, `.github/workflows/backtest_bench.yml`).

Executed: contract §4a steps 1–6 (contract read, fetch, TZ located and read, fingerprint
gate, repository state). Step 7 was entered and stopped. Steps 8 and 9 were not reached.
Step 10 is this report.

## Files Created

- `CryptoReports/TZ-31-horizon-ladder-on-archive-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

No implementation was performed. What follows is the blocker and its evidence.

### The gate passed

Revision string, all seven content anchors and all four file fingerprints matched exactly,
in both directions. Readings are under `## Test Results` and `## Fingerprints`.

### Blocker 1 — §6 item 4 specifies the known-answer control for an arm §2 does not build

`## 2. Scope` item 1 authorises **one** arm:

> `bench/backtest_bench.py` — one additive arm, `--regime-gate`, on the existing archive
> machinery.

`## 3. The arm` resolves setups over `H ∈ {48, 72, 96, 120, 168, 336} h × RR ∈ {1.0, 1.5,
2.0, 3.0}`, partitioned by the regime word. `## 4` registers the PRIMARY CLAIM as a
comparison of two populations — `ДИАПАЗОН` dates against trend dates — at every cell
clearing quorum.

`## 6. Validation` item 4 specifies the known-answer control as follows:

> **D7, the known-answer control, and its correct outcome is a REFUSAL.** On the driftless
> world the ladder must reproduce D3's shape — `P_none` decaying monotonically, `Ω` rising
> toward `Σq/Σ(1−q)` — **and must not produce a rung whose CI95 lower bound clears its
> derived bar.**

That is a control on a **horizon ladder**: rungs, `P_none` decay across `m`, convergence to
the two-barrier limit. It is D3's shape, and D3 exists in the file today as
`лестница H = m×168ч` (`bench/backtest_bench.py:2975`, printed at `:2997`). It asserts
nothing whatever about the regime partition, which is the entire subject of the registered
PRIMARY CLAIM.

This is not a terminology mismatch and does not survive substituting "cell" for "rung". The
regime-gate arm's known-answer control has to state what a driftless world must NOT show
when its dates are split by regime word — that the two populations do not separate. No such
assertion appears anywhere in the TZ.

Writing it myself is the one thing the TZ forbids. `## 4` registers the claim before the run
under inv. 23; `## 5` states that a red D7 is a broken instrument, a finding, and a reason to
stop; hard-floor item 2 forbids editing an assertion to make it pass. An Executor who
composes the known-answer control for his own arm has removed the only mechanism that makes
that arm's archive numbers trustworthy — which is precisely the guarantee §6 item 4 exists
to provide.

For completeness, and to keep the finding proportionate: §6 items 2 and 9 are also written
in ladder vocabulary (`--horizon-ladder`, "rung", "mid-ladder", "the widest rung") but
**are** mechanically adaptable to cells. Item 4 is not. Item 4 alone is the blocker.

### Blocker 2 — "the regime word" has two referents in scope, and they disagree by construction

`## 3` reads:

> compute the regime word from the unmodified `marketRegime` on that date's BTC row

Two independent problems, both requiring the Architect.

**(a) The bench already carries a different, separately registered regime labeller.**
`bench/backtest_bench.py:602` defines `btc_regimes()`, which labels `тренд`/`диапазон` from
the drift t-statistic on 90 daily BTC closes with a Newey–West correction, under a rule its
own comment records as "зарегистрировано ДО прогона (одобрено 11.08.2026)"
(`bench/backtest_bench.py:540-558`). Production `marketRegime`
(`index.html:1864`) is a different rule on a different input: `r14 / (v·√(2·H_NOISE))`
against `EFF_TREND`. The two label the same date differently by construction. The TZ names
`marketRegime`, which points away from the bench's own labeller, but never says whether
`btc_regimes` is to be left standing, compared against, or is now understood to be measuring
something else. `marketRegime` is currently never called by `backtest_bench.py` at all.

**(b) `marketRegime` returns three words, and the claim is binary.** The function returns
`stress` as well as `trend` and `range`:

```js
if (v >= VOL_HARD || (out.z !== null && Math.abs(out.z) >= REG_STRESS_Z)) {
    out.mode = 'stress';
    return out;
}
```

`## 4`'s claim compares `ДИАПАЗОН` dates against "trend dates" and is silent on `stress`.
Folding stress into the range population, folding it into the trend population, reporting it
as a third partition, and excluding those dates entirely are four different arms producing
four different `Ω` populations, and the registered claim reads differently under each. This
is a §12 ambiguity in its own right.

### The two readings, per contract §12

Both touch the same three files; they differ in what is built and what is asserted.

**Reading A — build `--regime-gate`, honouring §1–§4.**
Files: `bench/backtest_bench.py`, `bench/backtest_guard_bench.py`,
`.github/workflows/backtest_bench.yml`. The arm partitions by regime word over the `H × RR`
grid. Consequence: §6 item 4 cannot be executed as written, and contract §9 makes an item
that cannot be run a FAILURE, not an "N/A". The arm ships with its known-answer control
either absent or authored by the Executor.

**Reading B — build `--horizon-ladder`, honouring §6 and the canonical filename.**
Files: the same three. The arm walks `TGT_H_LADDER = [1, 4, 8, 16, 32]`
(`bench/backtest_bench.py:2239`), which the superseded revision named exactly and which the
existing infrastructure already supports. Consequence: contradicts §2's named flag, §3's
grid and §4's registered PRIMARY CLAIM, and measures nothing about the regime gate — which
is the whole subject of §1 in the current revision.

Reading B additionally matches the file's own canonical name,
`TZ-31-horizon-ladder-on-archive.md`, and the report path §7 requires. Those were left
unchanged by the re-upload too, so the filename is evidence of the prior scope rather than
of the current one — which is why it is offered here as context and not as a tiebreak. I
did not choose between the readings.

### What would unblock it

A revision of `## 6. Validation` written against the regime-gate arm, item 4 in particular:
the assertion D7 must make on the driftless world about the regime partition, stated by the
Architect. A ruling on `stress` and on the `marketRegime` / `btc_regimes` relationship would
resolve Blocker 2 in the same pass.

## Validation

The TZ's validation was **not entered**, because the blocker is in the validation section
itself and no code exists to validate. Per contract §9 no item is marked "not applicable";
each is recorded as NOT RUN with the reason, and no item is recorded as passed.

| # | Item | Result |
|---|---|---|
| 1 | `py_compile` both benches | NOT RUN — no change was made to either file |
| 2 | Byte-identity of the untouched path | NOT RUN — names `--horizon-ladder`, a flag no reading of the current scope creates |
| 3 | `--lab-selftest` green, delta stated | NOT RUN — no change to the selftest |
| 4 | **D7 known-answer control** | **NOT RUN — this item is the blocker (Blocker 1)** |
| 5 | Negative test on the guard | NOT RUN — no guard assertion was written to break |
| 6 | `bench.yml` steps 1–13 delta zero | NOT RUN — no edit was made, so there is no post-change replay to compare |
| 7 | Step 14 check count before/after | NOT RUN — same reason |
| 8 | The dispatch input exists and parses | NOT RUN — the workflow was not modified |
| 9 | Extremes | NOT RUN — no arm exists to drive them through |
| 10 | No-regression statement | Satisfied by construction — see below |

Item 10 is the one item with a measured result, and it holds trivially: no file outside
`CryptoReports/**` was touched. `git status --porcelain` is empty against `eeaa395`, and the
post-gate fingerprints of `index.html`, `main.py`, `catalysts.json`,
`bench/exhaustion-calibration.txt`, `bench/backtest_bench.py`,
`bench/backtest_guard_bench.py` and `.github/workflows/backtest_bench.yml` are unchanged and
recorded under `## Fingerprints`. No existing `--target` figure and no `bench.yml` step was
altered, because nothing was altered.

## Test Results

**Fingerprint gate (contract §5) — PASSED.**

Revision string, matched as an exact substring:

```
$ grep -n "^\*\*Revision" SYSTEM-MAP-CRYPTOCALCUL.md
17:**Revision 2026-09-06-a.** Baseline: TZ-30 on `bench/backtest_guard_bench.py` (new),
```

Required: `**Revision 2026-09-06-a.**` — found, exact match.

All seven content anchors, each matched with `grep -qF` as an exact substring:

| Anchor | Result |
|---|---|
| `**Revision 2026-09-06-a.**` | PRESENT |
| `### 3.12 Direction engine — veto cascade` | PRESENT |
| `### 3.15 Catalyst registry` | PRESENT |
| `### 3.16 List exhaustion — the day-range measure` | PRESENT |
| `## 11. Analytical engine` | PRESENT |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | PRESENT |
| `65. **A bar derived from the constant it judges moves with it.**` | PRESENT |

7 anchors compared, 7 present, 0 missing.

**File table (map `## 0`, quoted by the TZ) — 4 files compared, 4 exact, 0 differences.**

| File | Required lines | Measured | Required MD5 | Measured MD5 | Result |
|---|---:|---:|---|---|---|
| `index.html` | 3736 | 3736 | `dd39536d18cc1feb4839808e41e7bff4` | `dd39536d18cc1feb4839808e41e7bff4` | exact |
| `main.py` | 518 | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | exact |
| `catalysts.json` | 17 | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | exact |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | exact |

**The bench figure stated in the TZ's own `## 0`** (no row in the map's table, per the map's
recorded reasoning): `bench/backtest_bench.py` required **3240 lines**, MD5
`d2dad0f80afa2c191c2faf1d40081a88`. Measured: **3240 lines**, MD5
`d2dad0f80afa2c191c2faf1d40081a88` — exact.

5 fingerprints compared in total, 5 exact, 0 differences. Nothing to report under
`## Pre-existing Issues` from the gate.

**Repository state (contract §4a step 6).** The previous TZ's branch was merged:
`claude/tz-30-backtest-guard-in-gate` appears in `git branch -a --merged origin/main`, at
merge commit `ea259c6` (pull request #28), implementation commit `7fdd7db`. This work is
therefore not built on an unmerged base. `CryptoReports/` holds no TZ-31 report, so this is
the first report for this number and no `-2` suffix applies (contract §13).

**Source readings behind the blocker.** Each is a line reference in the tree at `eeaa395`,
not a summary:

| Fact | Evidence |
|---|---|
| §6 unchanged across the re-upload | `diff` of the two `## 6` sections — byte-identical |
| Scope names `--regime-gate` | TZ line 71, line 80 |
| §6 names `--horizon-ladder` | TZ line 177 |
| D3 is the existing ladder control | `bench/backtest_bench.py:2975`, printed `:2997` |
| Selftest section D holds D1–D6 today | `:2932`, `:2938`, `:2975`, `:3060`, `:3070`, `:3078` |
| Ladder infrastructure already present | `TGT_H_LADDER = [1, 4, 8, 16, 32]` at `:2239` |
| Quorum already in code (inv. 20) | `TGT_QUORUM_N = 60`, `TGT_QUORUM_D = 20` at `:2236-2237` |
| Bench's own regime labeller | `btc_regimes()` at `:602`, rule at `:540-558`, sole caller `:661` |
| Production `marketRegime` | `index.html:1864`; returns `range` / `trend` / `stress` |
| `marketRegime` absent from this bench | no occurrence in `bench/backtest_bench.py` |

## Deviations

None. No file within the TZ's scope was written, so there is nothing to deviate in. Work
stopped under contract §12 rather than proceeding on a chosen reading.

## Pre-existing Issues

None found. Every fingerprint the gate compares matched exactly in both directions, and no
defect outside the TZ's scope was encountered while reading the bench.

Recorded as an observation and **not** acted on: `bench/backtest_bench.py` carries
`btc_regimes()`, a regime labeller registered on 11.08.2026 under a different rule from
production `marketRegime`. This is not presented as a defect — the bench's own comment
argues the choice deliberately, and which labeller a measurement should use is the
Architect's call. It is recorded here because it is load-bearing for Blocker 2.

## Remaining Risks

- **The two readings are not equally cheap to abandon.** Reading A's arm needs production
  `marketRegime` reachable from a Python bench, which means extending the existing node
  bridge to carry that function and feeding it `volatility`, `r7` and `r14` per archive
  date. The machinery exists (`TARGET_JS_VARS`, `_score_bridge.js`), but it is real work,
  and building it against the wrong reading wastes it entirely. That asymmetry is the
  reason this stopped rather than guessing.
- **The re-upload replaced the TZ in place.** Any earlier session that read `8bd691f` and
  acted on it would have implemented the horizon-ladder arm against a specification that no
  longer exists. Nothing in this repository indicates that happened — `CryptoReports/` holds
  no TZ-31 report and no TZ-31 branch exists on the remote — but the general hazard belongs
  in the record, because a TZ is immutable by contract §13 and this one was rewritten under
  a name that still describes the superseded scope.
- **The canonical filename and the report path now describe the superseded arm.** Both the
  TZ and this report carry `horizon-ladder` in their names while the current §1–§4 specify a
  regime gate. Contract §13 makes both names permanent, so a future reader will meet a
  regime-gate specification under a horizon-ladder filename. Renaming either is not the
  Executor's to do.

## Commit

One commit, on `main`, on the `CryptoReports/**` direct-push path (contract §8).

Message:

```
docs(reports): TZ-31 — BLOCKED, §6 validates a different arm than §2 authorises (TZ-31)
```

Contents: `CryptoReports/TZ-31-horizon-ladder-on-archive-report.md`, added.

No hash appears here. This report's own commit has not been made at the time of writing, and
a hash or an outcome for it would be a forecast inside an immutable record (inv. 54,
contract §10).

## Pull Request

None. This is a branch TZ by class, but the run was BLOCKED before any file in its scope was
written, so no implementation commit, no branch and no pull request exists. The section is
recorded rather than omitted, because an absent section cannot be told from a forgotten one
(contract §10).

The fixed report-only line is deliberately **not** used here: it would assert a class this
TZ does not have. The class is read off the scope, and the scope names three files outside
`CryptoReports/**`.

## CI Execution

No workflow executed on a runner for this task, and the reason is not an unreadable result:
nothing was pushed to a branch, so nothing could trigger one. `bench.yml` did not run,
`backtest_bench.yml` did not run, and neither was modified.

The measurement TZ `## 6` item 8 describes — the `workflow_dispatch` run on `main` after
merge — has no referent, since no input was added to the workflow. No forecast is offered
for any of these (inv. 54).

## Final Repository State

This session leaves the working tree clean at `eeaa395e121eee59a25bc3e5e21eba0bd410087c`,
with no modification to any file in the TZ's scope. `git status --porcelain` returns empty.
No branch was created and no branch was pushed.

The fingerprints below were taken against that commit.

Nothing awaits a merge, so "NOT IN EFFECT UNTIL MERGED" has no referent and is not written:
there is no implementation to bring into effect.

## Fingerprints

Taken at `eeaa395`, at authoring time.

**System Map revision string:** `**Revision 2026-09-06-a.**`

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2268 | `52309e809bd0c540ae52afee15fa1b01` |
| `EXECUTOR-INSTRUCTIONS.md` | 814 | `9a257890e9db663eb0fc74129f4841e0` |
| `ANALYST-INSTRUCTIONS.md` | 2615 | `e945ac9e93c03e72f551bc7972541148` |
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/backtest_bench.py` | 3240 | `d2dad0f80afa2c191c2faf1d40081a88` |
| `bench/backtest_guard_bench.py` | 580 | `93c2726342e9f8b59579d0ba707a8a52` |
| `.github/workflows/backtest_bench.yml` | 140 | `8a994edb5be622d75196e2769c3cf45c` |
| `CryptoTZ/TZ-31-horizon-ladder-on-archive.md` | 212 | `c74463c224e4e8848b3b01be4b672d5e` |

The first four rows plus the map are the set the map's `## 0` block requires. The bench
files, the workflow and the TZ are added because this TZ's gate table or its scope names
them. `EXECUTOR-INSTRUCTIONS.md` matches the v20 figures the map records (814 lines,
`9a257890e9db663eb0fc74129f4841e0`).
