# Implementation Report — TZ-32

## Status

**COMPLETED.** All five scope items implemented, all ten validation items run.
Two items could not run in their literal archive form in this session and were
run in the strongest form available; both are named precisely under
`## Validation` and neither is claimed as something it was not. The measurement
itself is a `workflow_dispatch` on `main` after merge and is the Boss's action,
not the Executor's (TZ §5, §6.8).

## Inbound Filing

None. `CryptoTZ/TZ-32-regime-gate-on-archive.md` arrived under its canonical
filename in commit `830265d` and needed no `git mv`.

The session clone was one commit behind at trigger time — TZ-32 was not in the
working tree until `git fetch origin` and a fast-forward from `31bbf3a` to
`830265d` (§3: "not in my working tree" is not "not in the repository"). The
clone is not shallow (`git rev-parse --is-shallow-repository` → `false`).

**Previous TZ base:** TZ-30's work is on `origin/main`
(`git merge-base --is-ancestor` → true). TZ-31 was BLOCKED under §12 without
touching a file, so it left no branch. This work is built on a merged base.

## Scope Executed

**Class: branch TZ** — the scope names files outside `CryptoReports/**`, so an
implementation branch and the §8 pull-request clause both apply.

| # | TZ §2 item | State |
|---|---|---|
| 1 | `--regime-gate`, one additive arm on the existing archive machinery | done |
| 2 | `TARGET_DRIVER` gains the R:R substitution of §3.2, additive | done |
| 3 | `--lab-selftest` section D gains **D7** | done |
| 4 | `backtest_guard_bench.py` offline assertions on the new arm | done, section E |
| 5 | `backtest_bench.yml` gains a `workflow_dispatch` boolean passing the flag | done |

Nothing outside `## 2` was touched. `index.html`, `main.py`, `catalysts.json`,
`ANALYST-INSTRUCTIONS.md`, `btc_regimes()`, every production constant and
`bench.yml` steps 1–13 are unmodified — proven by fingerprint and by replay
below, not asserted.

## Files Created

None.

## Files Modified

| File | Lines before → after |
|---|---|
| `bench/backtest_bench.py` | 3240 → 3703 |
| `bench/backtest_guard_bench.py` | 580 → 823 |
| `.github/workflows/backtest_bench.yml` | 140 → 156 |

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**The regime word is read, never rebuilt.** `marketRegime(j.btcStats).mode` was
already on every setup row as `o["reg"]` (`backtest_bench.py:2431`). The arm
groups by that field. No bridge extension, no second implementation of a
production rule (inv. 38).

**The partition is per DATE, and that is checked rather than assumed.**
`run_target` builds `btc_stats` once per date, so every observation on a date
carries one word. `_rg_word` refuses a date carrying two — a partition over a
field that varied inside a date would be a partition over nothing, and the
block bootstrap resamples dates, so a mixed date would silently blend the two
populations.

**The pooling is cut, not rewritten** (§3.4, inv. 38). A population is a subset
of dates, so each cell is `_arm_pool(<that population's dates>, "rr:<RR>",
side)` — the same block bootstrap `--target` already uses. `Ω`, its CI95,
`P_none`, the counts and the cell's bar all come from the existing function.

**The R:R substitution lives in the driver because the stop lives there**
(§3.2). After `dec`, `b_log = |log(dec.inv.price / E)|`, and the substituted
extremum is `E·exp(+RR·b_log)` long / `E·exp(−RR·b_log)` short, handed to the
**unmodified** `tradeGeometry` through the same `subs` shape it already
receives. Keys are `rr:<value>`. The block does not execute without
`j.rrGrid`, and `run_target` attaches that key only when asked — which is what
makes the untouched path byte-identical rather than merely unaffected.

**The bar is derived and no numeral for it appears anywhere.** Each cell's bar
is `_arm_pool`'s `inv_rr` — the mean of `1/rr` over that cell's own admitted
setups, taken from the `rr` the unmodified `tradeGeometry` returned. Measured on
the driftless world, a cell nominally at `RR = 3.0` carried a bar of `0.243`
long and `0.426` short (nominal `1/RR` = `0.333`): the chase anchor moves the
entry and the realised `rr` does not equal the nominal one, which is exactly why
inv. 61 and inv. 65 require the bar to follow the object it judges.

**Right-truncation is accounted per horizon.** `walk_grid` holds `t0` and the
step fixed and moves only the right edge, so the date grid at a larger `H` is a
prefix of the grid at a smaller one. Each horizon reports its date count, the
dates lost against the shallowest horizon, and its own last usable entry date.
A horizon whose archive cannot yield even one date is recorded EMPTY and
printed, rather than killing the other five — and only that one `ValueError` is
caught; any other propagates.

**Funding is charged in arithmetic** (§3.4). `f*` is the constant eight-hour
rate solving `R_c − f·N_c/b_c = R_r − f·N_r/b_r` against the `168 h / RR 2.0`
reference, where `N(H) = FUND_PAY_7D · H / H_NOISE` with both constants read
from `index.html` at run time (inv. 20) and `b` is the cell's own mean risk leg.
Where the reference cell is empty, `f*` prints `—` rather than a number with
nothing behind it.

**`stress` is reported and never folded.** It is a bucket of its own with its
own counts; it enters no comparison. `btc_regimes()` is untouched and appears
only as a count per (`marketRegime` word × `btc_regimes` word) cell — wiring
nothing, deciding nothing.

**A cell that cannot be read says why.** "No population at all", "the arm
admitted no setup", and "below quorum" are three different facts and print as
three different lines. Below quorum, `Ω` is not printed at all.

**The verdict is the rule registered before the run** (§4). The claim falls only
where `range`'s CI95 is strictly below `trend`'s on the same side; overlap and
excess both hold it. A cell is compared only when BOTH populations clear the
existing quorum. Zero comparisons reads as NOT DECIDABLE and never as "the claim
held" (inv. 22), and `--regime-gate` exits non-zero in that case.

## Validation

Every item of TZ §6, in order.

**1. `py_compile` — PASS.** `bench/backtest_bench.py` exit 0,
`bench/backtest_guard_bench.py` exit 0.

**2. Byte-identity of the untouched path — PASS in the form the session
permits; the literal archive form did NOT run.**

The archive form is not runnable here: `bench/cache` does not exist in the
checkout (it is git-ignored and restored from the Actions cache), and TZ §5 and
hard-floor item 9 both forbid fetching the archive in session. I did not fetch.

What DID run is the same `run_target` → `target_summary` code path `--target`
executes, on the deterministic synthetic world, pre-change vs post-change,
covering the full `K_GRID` with the identity arm, the whole D3 `H_override`
ladder and the admissibility probe — i.e. the payload of `target_raw.json` plus
the complete per-date record:

```
pre   md5 bcdc781ced77476a5458d2e8769593d7   77655 lines
final md5 bcdc781ced77476a5458d2e8769593d7   77655 lines
diff  exit 0   diff lines: 0
```

A diff was actually taken, and the count is `0`. This was re-run against the
final tree after the last edit. The driver addition is inside this assertion:
an unused `rr:` key moved no existing number.

**What this does not establish:** that the figures are identical on the real
archive. The synthetic world exercises the same code with the same inputs
shape, but it is not the archive, and I am not claiming it is.

**3. `--lab-selftest` — PASS, green, exit 0.**

| | baseline | after | delta |
|---|---:|---:|---:|
| `ОК` verdicts | 19 | 23 | **+4** (D7a–D7d) |
| `СТОП` verdicts | 0 | 0 | 0 |

D1–D6 verdict lines are byte-identical to the baseline (10 lines compared, 0
diff lines).

**4. D7, the known-answer control on the PARTITION — PASS, and its correct
outcome is the REFUSAL it produced.**

```
D7 деление по слову режима на мире БЕЗ сноса — верный исход ОТКАЗ
   дат на популяцию: range 34 · trend 45 · stress 4
   D7a оба слова встречаются: ОК · D7b ячеек с кворумом range 24 · trend 24: ОК
   D7c stress исключён, а не отсутствует: дат 4 · протекло в популяции 0 ·
       деление покрывает все даты: да ОК
   D7d ДИ95 перекрываются на всех ячейках с кворумом: сравнений 19,
       разделений 0 ОК
```

The preconditions are read before the overlap, exactly as §6.4 requires: both
words occur, each clears quorum on at least one cell (24 each), and `stress` is
EXCLUDED rather than absent — it occurs on 4 dates, and the intersection of the
stress timestamp set with the two compared populations' timestamp set is empty,
read off the arm's own `_rg_split`. The partition is also checked to cover every
date.

**D7 was proven to be a live control, in both of its failure modes.** A control
that cannot fail is dead specification, so I broke it deliberately, twice:

- *Degenerate labeller* (label by raw target/stop counts): populations came out
  `range 82 · trend 2`; D7b, D7c and D7d all went `СТОП`, the "preconditions not
  met" line printed, lab verdict `НЕИСПРАВНА`, exit 1.
- *Balanced leak* (label by the sign of the date's own mean reward, which splits
  a driftless world near half and half): populations `range 41 · trend 48`, both
  at quorum (D7a, D7b `ОК`), and **D7d fired on the separation it exists to
  catch — 19 comparisons, 7 separations, `СТОП`**, exit 1.

Both were reverted; the tree carries neither.

**5. Negative test on the guard — PASS.** The bar derivation was broken in the
working tree the way inv. 61/65 forbid (`m["bar"] = 1.0 / rr`, the nominal
numeral where the derived mean belongs). Gate step 14 turned red and NAMED the
assertion:

```
checks run: 142   FAIL 2
  FAIL: 30b. the cell's bar IS the derived mean of 1/rr, not a written numeral
        [(0.5, 0.18055555555555555)]
  FAIL: 30b. and it differs from the nominal 1/RR the cell is named after
        [(0.5, 0.5)]
exit=1
```

Reverted → `checks run: 142  FAIL 0`, exit 0, and `grep -c 'NEGATIVE TEST'` → 0.

This check was added *because* the first draft of section E did not have it:
checks 29 proved `_arm_pool` derives the bar, but nothing proved
`regime_gate_summary` carried that number onto the cell the report prints —
which is precisely where a nominal numeral would be substituted. The negative
test found that gap, which is what a negative test is for.

**6. `bench.yml` steps 1–13 — DELTA ZERO, two measurements compared.** Replayed
with the workflow's own commands against a pristine `git archive HEAD` extract
and again against the working tree.

- Per-step exit codes: identical, 13/13.
- Full output content: 237 lines each, **0 diff lines** (after removing V8 crash
  addresses and step 13's per-run temp paths, both nondeterministic by
  construction).

**Step 5 is RED on both sides — a pre-existing, environment-caused failure.**
See `## Pre-existing Issues`. The zero compares two measurements, not a
measurement against this document.

**7. Step 14 check count — 94 → 142, delta +48**, both as measured, 0 FAIL on
both sides.

**8. The dispatch — the three facts stated, and no forecast.**
- The input exists: `regime_gate`, `type: boolean`, `default: false`.
- The flag reaches the bench: the step runs
  `python backtest_bench.py --regime-gate --html ../index.html --bot ../main.py`
  under `if: ${{ inputs.regime_gate }}`; invoked directly, `--regime-gate`
  parses and reaches its branch, failing only at `load_cache()` on the absent
  cache — byte for byte how `--target` fails on the same empty cache at HEAD.
- The workflow file parses: `yaml.safe_load` → 3 inputs, 18 steps.

Per inv. 54 I do not forecast the run. **TZ §6.8 says "the flag reaches
`--target`"; the flag §2.5 authorises is `--regime-gate`, and that is what was
wired.** I read the `--target` in that sentence as naming the measurement
family, not a second flag, and flag it here rather than resolve it silently.

**9. Extremes — all eight exercised against the shipped functions.**

| Extreme | Observed |
|---|---|
| cell with zero resolved setups | `сетапов 0 на 0 датах (дат в популяции 30) — пул не собран`; verdict not decidable |
| cell below quorum | `n 8 дат 8 · НИЖЕ КВОРУМА — Ω не печатается`; `n_cmp` 0 |
| population with no dates at all | stub names the absent population; `n_cmp` 0, `holds` False |
| every date is `stress` | both compared populations empty, `stress` reported with its own counts; CLI exits `СТОП` |
| symbol removed by `target_gate` | gate runs ONCE before the grid, so every horizon sees the same symbol set |
| symbol dropped mid-grid (unbalanced panel) | `H=48` 12 dates / 24 setups for the short coin vs `H=336` 11 / 22 — counts report it |
| archive shorter than the first `H=336` date | horizon recorded EMPTY and printed; shallower horizons still report; `lost` accounted |
| side with no setups in one population | that side is not a comparison; `n_cmp` counts the other side only |
| realised `rr` ≠ nominal on every setup | nominal `1/RR` 0.5000, derived bar 0.2186 — the bar followed the realised `rr` |

Every degenerate case degrades to NOT DECIDABLE. None produces a false "claim
held" (inv. 22).

**10. No-regression statement.**

- `index.html` — untouched, MD5 `dd39536d18cc1feb4839808e41e7bff4`, identical to
  the gate table.
- `main.py` — untouched, MD5 `0e3ead8c300d2ee6783303c4bf2fb6b5`, identical.
- `catalysts.json` — untouched, MD5 `f9b2dd4a3594134b2b7b603de19075c3`, identical.
- Every existing `--target` figure — identical by diff (item 2), 0 lines over
  77,655.
- Every `bench.yml` step — delta zero by replay (item 6).
- `git status --porcelain` lists exactly the three authorised files.

## Test Results

| Check | Before | After | Exit |
|---|---:|---:|---:|
| `backtest_guard_bench.py` (gate step 14) | 94 / 0 FAIL | 142 / 0 FAIL | 0 |
| `--lab-selftest` `ОК` / `СТОП` | 19 / 0 | 23 / 0 | 0 |
| `bench.yml` steps 1–13 exit codes | 12×0, 1×1 | 12×0, 1×1 | delta 0 |
| byte-identity diff lines | — | 0 of 77,655 | 0 |
| `py_compile` × 2 | — | — | 0, 0 |

**All readings above are LOCAL**, in this session's container. No workflow
executed on a GitHub runner during this session — see `## CI Execution`.

## Deviations

**None in scope.** Two reporting-level notes, neither a change to what was
built:

1. **TZ §6.2's archive form did not run** — no cache in the checkout, and TZ §5
   plus hard-floor item 9 forbid a session fetch. Run in the strongest available
   form with a real diff; stated as such rather than as an archive result.
2. **TZ §6.8 wording** — "the flag reaches `--target`" vs the `--regime-gate`
   flag §2.5 authorises. Named above, not silently resolved.

## Pre-existing Issues

**1. `bench.yml` step 5 (`direction_bench.py --props --fixtures --control
--sim`) fails in this session's environment.** `FATAL ERROR: Reached heap limit
Allocation failed - JavaScript heap out of memory` from V8 during `--sim`, after
`СВОЙСТВА`, `РЕЖИМ` and `ФИКСТУРЫ` all print `[OK ]`. Proven pre-existing: it
fails identically on a pristine `git archive HEAD` extract, before any edit of
mine. The container has 955 MB of RAM total; a GitHub runner has ~7 GB, so this
is a fact about this session's machine, not about the repository. **Not acted
on** (§12).

**2. `_arm_pool` emits `RuntimeWarning: All-NaN slice encountered`** from
`np.nanpercentile` whenever every bootstrap resample of a cell has zero stops,
so `Ω` is NaN throughout. Pre-existing code, reachable by `--target` today; the
regime grid reaches it far more often because low-`RR` cells legitimately never
hit a stop. It is stderr noise, not a failure — the cell correctly prints
`Ω не определена`. **Not acted on:** silencing it would change existing
statistical code this TZ does not authorise (§2, hard-floor item 1 territory).
Worth an Architect decision.

**3. The map's `## 0` table carries no row for any file this TZ modifies**, as
TZ §0 itself states. All four files the table does list match their stated line
count and MD5 exactly. No difference to report.

## Remaining Risks

1. **The primary claim is unmeasured on the archive.** Everything here proves
   the instrument; nothing here is a market result. The synthetic world is
   driftless by construction, so its "claim held" verdict is the D7 refusal and
   carries no information about the real market.
2. **The `168 h / RR 2.0` reference cell may be empty on the archive**, as it
   was on the short side of the synthetic world. `f*` then prints `—` for that
   whole side. That is honest, but it means the funding column can be absent
   exactly where it is most wanted. Whether the reference should fall back to
   the densest cell is a specification question, not an Executor's.
3. **Low-`RR` cells may be structurally empty.** Admission requires the realised
   `rr ≥ RR_MIN = 2.0`; on the synthetic world `RR = 1.0` admitted nothing on
   either side and `RR ∈ {1.0, 1.5, 2.0}` admitted nothing on the short side.
   The grid may therefore be sparser on the archive than four RR points suggest.
   The counts say so per cell, but the Architect should expect it.
4. **Grid cost.** Six `run_target` passes. The synthetic world takes ~63 s for
   the grid; the three-year archive with ~30 coins will be substantially longer,
   inside `backtest_bench.yml`'s 120-minute budget but not negligibly.
5. **`--lab-selftest` runtime roughly doubled** (≈3–6 min here) because D7 runs
   the full grid. It remains well inside `bench.yml`'s 20-minute timeout —
   though note `--lab-selftest` runs in `backtest_bench.yml`, not in `bench.yml`.

## Commit

Implementation commit, on the branch, already pushed when this section was
written:

`680a33e13f56964f9037bc4d72a75b0a272e81d0`

```
TZ-32: regime gate and horizon on the archive (--regime-gate)

An additive arm on the existing --target machinery: the H x RR grid is
partitioned by the regime word marketRegime returns on the entry date, so
the direction layer's one input is measured instead of argued.

- backtest_bench.py: --regime-gate, the R:R substitution inside TARGET_DRIVER
  (the stop is only known there), per-cell bar derived at run time from the rr
  the unmodified tradeGeometry returns, right-truncation accounting and the
  break-even funding rate; stress is reported and never folded into the claim.
- backtest_bench.py: lab-selftest section D gains D7, the known-answer control
  on the PARTITION whose correct outcome is a REFUSAL, with preconditions that
  fail when the control cannot fire.
- backtest_guard_bench.py: section E, offline assertions on the partition, the
  bar derivation, the right-truncation accounting and the registered verdict
  rule; the bridge is built and called rather than read.
- backtest_bench.yml: a workflow_dispatch boolean passing --regime-gate.

Without the flag every existing figure is byte-identical: asserted by diff,
not claimed.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: the three files under `## Files Modified`, nothing else.

This report is authorised to be committed to `main` with the message
`docs(reports): TZ-32 — regime gate and horizon on the archive (TZ-32)`.

## Pull Request

**No pull request exists.** The `gh` CLI is not installed in this session
(`gh: command not found`) and no GitHub API token is available, so one could not
be opened. Per §8 this is the defined fallback, not a blocker.

- Branch: `claude/tz-32-regime-gate-on-archive` (pushed, tracking set)
- Compare URL:
  `https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-32-regime-gate-on-archive`

The Boss opens and merges from that link in one action, after the Architect's
audit returns ПРИНЯТО.

## CI Execution

**No workflow conclusion was read by this session**, because there is no `gh`
and no API token to read one with. What IS established:

- The branch `claude/tz-32-regime-gate-on-archive` reached the remote
  (`* [new branch]` in the push output).
- `bench.yml` triggers on `push` to `branches: [ main, 'claude/**' ]`; the
  branch matches `claude/**`.
- Its `paths-ignore` covers `journal/**`, three `analyst/` paths and `**.md`.
  None of the three changed paths is ignored, so the gate's filters are cleared.
- `backtest_bench.yml` is `workflow_dispatch` only and therefore did not run and
  will not run on a push.

Whether the gate actually went green on the runner is read from the pull-request
page by whoever opens it (§9).

## Final Repository State

This session leaves behind the branch `claude/tz-32-regime-gate-on-archive` at
`680a33e13f56964f9037bc4d72a75b0a272e81d0`, one commit ahead of
`origin/main` at `830265d`, containing exactly the three modified files.
`git status --porcelain` on that branch lists nothing beyond them; every bench
scratch artifact (`bench/_*_bridge.js`, `bench/__pycache__/`, `bench/cache/`) is
git-ignored and none was committed.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

**System Map** — `SYSTEM-MAP-CRYPTOCALCUL.md`, revision `2026-09-06-a`,
**2268 lines**, MD5 `52309e809bd0c540ae52afee15fa1b01`.

All seven content anchors the TZ header quotes were found as exact substrings
before any work began. Gate GREEN.

Files the map's `## 0` table lists — measured, unchanged by this TZ:

| File | Lines | MD5 | vs required |
|---|---:|---|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` | match |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

Files the TZ's gate table adds — required (at HEAD `830265d`) and final:

| File | Required | Measured at HEAD | Final |
|---|---|---|---|
| `bench/backtest_bench.py` | 3240 / `d2dad0f80afa2c191c2faf1d40081a88` | match | 3703 / `4d4242d37e63a01bdf74c474b3cfcb02` |
| `bench/backtest_guard_bench.py` | 580 / `93c2726342e9f8b59579d0ba707a8a52` | match | 823 / `99d5f415f0a8d79eadeaf644b718e899` |
| `.github/workflows/backtest_bench.yml` | 140 / `8a994edb5be622d75196e2769c3cf45c` | match | 156 / `60ac7db0c4f1960f57d67da8e9beebfe` |

Every required fingerprint matched in both directions before work started.
