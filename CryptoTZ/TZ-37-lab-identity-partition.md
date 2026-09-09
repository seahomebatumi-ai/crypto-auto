# TZ-37 — Lab identity, re-registered as a partition

**Canonical filename: `CryptoTZ/TZ-37-lab-identity-partition.md`.** Name the committed
file from this line, never from the name the file arrived under (contract §3).

| Field | Value |
|---|---|
| Report | `CryptoReports/TZ-37-lab-identity-partition-report.md` |
| Branch | `claude/tz-37-lab-identity-partition` |
| Class | **branch TZ** — the scope names files outside `CryptoReports/**` (contract §8) |
| Model | **Opus** |

---

## 0. Fingerprint gate — blocking

Run contract §5 before any work. Required map revision, matched as an exact substring:

```
**Revision 2026-09-09-a.**
```

`SYSTEM-MAP-CRYPTOCALCUL.md` at this revision is **2628 lines**, MD5
`8388e3b1edf45cae4069c2d35b1f1ac9`.

All seven content anchors must be present, each matched as an exact, **case-sensitive**
substring:

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-09-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `69. **An identity control names the WORLD in which the identity holds.**` |

**The report states the LINE NUMBER at which each anchor matched, not a verdict that it
did.** The anchor carried at `2026-09-08-b` for inv. 68 differed from the invariant in case
alone and could not match anything, and TZ-36's report recorded all seven as present as exact
substrings — so «all seven matched» is exactly the sentence that has already been wrong once
(map §0, §10). A line number is an artifact; «matched» is a claim.

The map's `## 0` file table at this revision — measure each and report under
`## Fingerprints`:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**The two benches this TZ edits have no row in that table by design (map §0), so their
figures are stated here** and are part of this gate:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4110 | `8cca251ee28c5c9332c44405558cc339` |
| `bench/backtest_guard_bench.py` | 1140 | `3b6ef587dd5e066c615300e530524aa9` |

Contract required: `EXECUTOR-INSTRUCTIONS.md` **v20**, 814 lines, MD5
`9a257890e9db663eb0fc74129f4841e0`.

---

## 1. What is wrong

`--lab-selftest` prints `ВЕРДИКТ ЛАБОРАТОРИИ: НЕИСПРАВНА — результатам не верить` and has
done so on every dispatch since TZ-33 merged. One control is red. Map §3.10a:

> **D4 has been RED since TZ-33 and the lab has said so to nobody.** It compares the `prod`
> arm against `ident` — a substituted arm handed production's own 90-day extremum, which must
> therefore reproduce `prod` exactly — and TZ-33 made `prod`'s geometry the ANCHORED one while
> `ident` stays at `E`. **The control is CORRECT to refuse**; what is wrong is that it
> asserted an identity without naming the world that makes it one (inv. 69).

**The control is not the defect and production is not the defect.** D4 states an
unconditional identity; production legitimately gained a second pass; the claim is now false
on exactly the rows the second pass touches and true everywhere else. Inv. 69 names both what
this costs and what may not be done about it:

> **The two repairs a red identity invites are both wrong.** Deleting the fields that moved
> is an assertion removed to make a bench pass (hard floor item 2), and it silently stops
> checking the leg that did NOT move — here the resolution leg, whose immobility is the whole
> claim `--target`'s additivity rests on.

**Nothing in the push gate can see any of this**, because `--lab-selftest` runs only under
`backtest_bench.yml`, which is `workflow_dispatch` (inv. 62). Two TZs passed with the lab
declaring itself unfit and no push able to say so.

**Production is not touched by this TZ.** `index.html` and `main.py` are out of scope and a
diff against either is a defect.

---

## 2. Scope

`## Scope` is the complete authorisation (contract §6). Anything not listed is forbidden
however obviously beneficial it looks.

**Files to Modify**

| File | Stage |
|---|---|
| `bench/backtest_bench.py` | A, B |
| `bench/backtest_guard_bench.py` | C |

**Files to Create** — none.
**Files to Delete** — none.

**Explicitly NOT authorised**, and each would be a defect if touched:
`index.html` · `main.py` · `catalysts.json` · `.github/workflows/**` · `.gitignore` ·
`SYSTEM-MAP-CRYPTOCALCUL.md` · `EXECUTOR-INSTRUCTIONS.md` · `ANALYST-INSTRUCTIONS.md` ·
`journal/**` · `bench/journal_bench.js` · `bench/verify_bench.py` ·
`bench/direction_bench.py`.

**No bench file is created, so no `bench.yml` wiring is required** and the workflow is out of
scope; hard floor item 12's second clause does not fire here. The gate reaches this work
through step 14, which already runs.

**Hard floor, quoted so it can be compared rather than recalled** (map inv. 55).
Contract §7 item 1:

> **No change to scoring, leverage, liquidation or geometry math** unless the TZ explicitly
> cites a completed backtest (map §3.10b). `scoreCandidate`, `momentumScore`, `qualityScore`,
> `scoreFinish`, `tradeGeometry`, `marketRegime`, `directionVerdict`, `leverageDecision`,
> `invalidationInfo`, `protectionPlan`, `liqPrice`, `liqTouchProb`, `residual7` are closed to
> edits by default.

**This TZ cites no backtest and requires no edit to any of them.** It changes what one
control ASSERTS about numbers those functions already produce. If any stage appears to
require editing one of them, the stage is defective — report BLOCKED and quote it.

Contract §7 item 2:

> **Never edit a bench to make it pass.** A red bench is either a product defect or a stale
> expectation; both are findings, neither is a licence to change the assertion.

**This TZ moves a bench assertion and says so in its own text, which is the only way that is
permitted** — a re-registration through a specification, exactly as TZ-28 re-registered D2
and D3 (map inv. 61). The permission is bounded and the bound is the whole of it:

- **Only D4 may move**, and only into the two-legged form §4 and §5 specify.
- **No field is removed from any comparison.** The eight compared fields stay eight. What
  changes is that each one is now asserted to HOLD or to FLIP on a named population instead
  of being asserted to hold on all of them.
- **Any other section turning red is a FINDING**, reported and not repaired. D1, D2, D3, D5,
  D6, D7, D8 and D9 are recorded on the baseline tree before the first edit and must be
  unchanged after.

---

## 3. What is already measured, and what it is for

Map §3.10a carries a reading taken by the Architect on the merged tree at revision
`2026-09-09-a`: 7 926 comparisons, 1 165 differences, 455 rows the chase rule never fired on,
521 it did, 118 presence mismatches split 113 / 5, and — with the anchor forced off — 7 848
comparisons with zero differences and zero presence mismatches.

**Those figures are a PRIOR READING and they are not the bar.** The bars in §4 and §5 are
rules over populations, asserted row by row, and no numeral from the paragraph above appears
in any of them. The session takes its own counts and prints them; **a divergence from the
map is reported as a finding and no assertion is ever adjusted to reach the map's number**
(inv. 43). The world is seeded and the tree is the same, so a divergence would mean something
moved that this TZ did not move — which is worth more than agreement.

---

## 4. Stage A — the partition becomes a named function

`bench/backtest_bench.py`.

### A1 — lift D4's comparison out of `lab_selftest` into a module-level function

D4's loop is inline inside `lab_selftest()`, so nothing outside that function can execute it
and gate step 14 cannot assert it without re-implementing it — which inv. 21 forbids
outright. Give it a name and a return value:

```
d4_partition(dates) -> dict
```

It walks `dates` exactly as the current loop does, over `o["arms"]["prod"]` and
`o["arms"]["ident"]`, and CLASSIFIES rather than merely counting. Required members, named
here so a reader of the return does not have to reconstruct the rule:

| Key | Meaning |
|---|---|
| `n_cmp`, `n_diff` | totals over the eight compared fields, on the same construction the current D4 uses |
| `n_still`, `n_moved` | matched pairs on rows the chase rule did NOT fire on, and did |
| `still_diff` | field differences on `n_still` rows — the HOLD side of the partition |
| `moved_missing` | per field: `n_moved` rows that did NOT differ where the rule says they must |
| `moved_extra` | per field: `n_moved` rows that DID differ where the rule says they must not |
| `r_bad` | `n_moved` rows whose `R` difference disagrees with `first == "tgt"` |
| `r_tgt` | `n_moved` rows whose `first` is `tgt`, printed and never asserted (see A4) |
| `miss_prod`, `miss_ident` | presence mismatches, by which arm is ABSENT |
| `miss_bad` | presence mismatches whose direction disagrees with `o["adm"]` |
| `n_unclassed` | matched pairs the population test could not classify (see A3) |

### A2 — the FLIP set and the HOLD set, written here and not discovered at run time

Over the eight fields `first · hit · R · p · rr · tgtSig · a · b`, on a row the chase rule
FIRED on:

| Field | Rule |
|---|---|
| `rr`, `tgtSig` | **MUST differ.** They are measured at the anchor for `prod` and at `E` for `ident` |
| `first`, `hit`, `p`, `a`, `b` | **MUST NOT differ.** The target, the stop, the entry `E` and the window are the shared reference leg (map §3.10) |
| `R` | **differs if and only if `first == "tgt"`**, because `R` is `rr` there and is `−1`, `0` or the shared mark-to-market otherwise |

On a row the chase rule did NOT fire on, all eight MUST hold and both arms must be present.

**This is the property §3.10 states in prose and nothing currently checks**: that
`prod_anchor` is additive because the reference leg did not move. A control that merely
counted differences would pass while the resolution leg drifted.

### A3 — the population test, read and never re-derived

A row is «moved» when `o["arms"]["prod_anchor"]["wait"]` is true and «still» when it is
false. TZ-36 already records that member at the site that knows it; **do not re-derive the
chase rule from geometry here** (inv. 21, 67).

A matched pair whose `prod_anchor` is absent cannot be classified by that test. It is counted
in `n_unclassed` and **asserted zero**; a non-zero reading is a FINDING and is never defaulted
into either population — a reader without the observation refuses rather than guessing
(inv. 67). State the count in the report whatever it is.

### A4 — what carries a non-zero requirement and what does not

`n_still > 0` and `n_moved > 0` are asserted, and D4 fails loudly with a named line if either
population is empty: a control that ran on nothing has not run (inv. 22, 68), and D8 already
has that line to copy the shape from.

**`miss_prod`, `miss_ident` and `r_tgt` carry NO non-zero requirement, deliberately, and none
is to be added.** A world in which the anchored pass changes no admission, or in which no
waiting row reaches its target, is a legitimate world; requiring those counts non-zero would
be a bar on the DATA rather than on the code, which is the class inv. 61 exists to refuse.
They are printed. `miss_bad` and `r_bad` are the assertions, and both are non-vacuous over
the whole `n_moved` population regardless of what those three read.

`[решение принято мной]` — discarded alternative: assert `miss_prod > 0` on the strength of
the map's own reading of it. Rejected because that count is a property of one seeded world,
and quoting it here would convert a prior reading into a bar — which §3 forbids in this very
TZ, and which is why no figure from that paragraph appears anywhere after it.

---

## 5. Stage B — D4 becomes the pair

`bench/backtest_bench.py`, inside `lab_selftest`.

### B1 — D4a, the identity in the world where it holds

With the chase rule forced off on every row the anchor IS the current price, so `ident` must
reproduce `prod` exactly. Required: **zero** field differences over all eight, **zero**
presence mismatches, **zero** rows classified as moved, and `n_cmp` non-zero (inv. 22, 45).

**Read the world D9 already builds; do not run a third `run_target` over it.** D9's
anchor-off call passes no `want_identity`, so `ident` is absent from that run — add
`want_identity=True` to **that existing call** and let D4a and D9 read the same `dates`.

That addition is authorised, and it is the one place this stage touches something D9 owns, so
it is proven rather than asserted: **record D9's four printed counts on the baseline tree
before the edit and assert they are byte-identical after.** Adding a substituted arm must not
move a comparison between `prod` and `prod_anchor`; if it does, that is a finding about the
driver and this stage stops.

### B2 — D4b, the partition on the live path

`d4_partition` over the existing `dA`. Passes when `still_diff`, every entry of
`moved_missing`, every entry of `moved_extra`, `r_bad`, `miss_bad` and `n_unclassed` are all
zero and both populations are non-zero.

Both legs print their counts. **The printed line names which side failed** — a control that
says only «СТОП» has localised nothing.

### B3 — what must NOT move

- D1, D2, D3, D5, D6, D7, D8, D9 keep their current construction, their current bars and
  their current printed lines. Record every line on the baseline tree first; any movement in
  them is a finding, not a licence to adjust.
- The eight compared fields stay eight, and `same_f` stays the single site that names them
  (inv. 20). D8 already reads that tuple; D4 must read the same one and not a copy.
- `run_target`, `_touch_calc`, `_anchor_fill`, the arms, the summaries and every existing
  figure are untouched. This stage changes what is ASSERTED, never what is COMPUTED.
- The lab's overall verdict line is not edited. If it turns from `НЕИСПРАВНА` to `ИСПРАВНА`
  that is an OUTCOME of the sections passing; if any other section is red it stays
  `НЕИСПРАВНА` and the report names which one.

---

## 6. Stage C — the construction goes where something already runs

`bench/backtest_guard_bench.py`, gate step 14.

### C1 — a new section, and its letter is chosen from the file

**The next free letter is `G`.** The file already carries TWO sections lettered `E` — TZ-32's
regime-gate arm and TZ-34's venue observation — and only the second prints a section line
(map §10). **Do not renumber either**, for the reason invariant numbers are never renumbered:
a section letter appears in the immutable report of the TZ that created it. Take `G`, state
the collision in the report, and change nothing about it.

### C2 — what the section asserts

It calls `d4_partition` **by name** on hand-built `dates` structures and compares its return
(inv. 21). `requests` stays stubbed, no socket is opened, nothing is read from the archive.
The section reports its own count and refuses to pass on zero.

Minimum cases, each of which must be shown to land in the bucket named:

| Fixture | Required |
|---|---|
| still row, all eight fields equal | counted in `n_still`, `still_diff` unchanged |
| still row, one field different | `still_diff` rises — the HOLD side can go red |
| moved row differing in exactly `rr` and `tgtSig` | clean; no bucket rises |
| moved row where `rr` is equal | `moved_missing['rr']` rises |
| moved row where `first` differs | `moved_extra['first']` rises |
| moved row, `first == "tgt"`, `R` equal | `r_bad` rises |
| moved row, `first != "tgt"`, `R` different | `r_bad` rises |
| `prod` present, `ident` absent, `adm` true | `miss_prod` rises, `miss_bad` unchanged |
| `prod` present, `ident` absent, `adm` false | `miss_bad` rises |
| `ident` present, `prod` absent, `adm` false | `miss_ident` rises, `miss_bad` unchanged |
| matched pair with no `prod_anchor` | `n_unclassed` rises, and the row lands in NEITHER population |

**This list IS the negative control** (inv. 45, 68): every constructed defect must be detected
and the clean fixtures must stay clean, so the section proves the classifier flips exactly on
what it should and on nothing else. A section that only ran the clean cases would be green
while asserting nothing.

### C3 — no archive reading in this session

Nothing here is dispatched and nothing is forecast. The `prod_anchor` archive figure is a
separate `backtest_bench.yml` dispatch and a separate §10 row (map inv. 44); this TZ does not
touch it, does not predict it and does not wait on it.

---

## 7. Validation

Written by the Architect. Every item names its artifact and its source. An item that cannot
be run FAILS and is never «not applicable» (contract §9).

| # | Item | Artifact | Source |
|---:|---|---|---|
| 1 | `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` — exit 0 | exit code | session |
| 2 | `git diff --numstat` names exactly the two in-scope files; `index.html`, `main.py`, `journal/**`, `bench/journal_bench.js`, `bench/verify_bench.py` and `.github/workflows/**` appear in no diff | diff output | session |
| 3 | Fingerprint gate: the line number at which each of the seven anchors matched, case-sensitively; the map's own line count and MD5; both bench figures from §0 | `grep -n`, `md5sum` | session |
| 4 | Baseline `--lab-selftest` recorded BEFORE the first edit: full stdout, exit code, and the D4 line verbatim | bench stdout on the unmodified tree | session |
| 5 | D4a: zero differences, zero presence mismatches, zero moved rows, `n_cmp` printed and non-zero | bench stdout | session |
| 6 | B1's proof: D9's four printed counts on the baseline tree and after adding `want_identity=True` to its call — byte-identical | both trees | session |
| 7 | D4b: `n_still` and `n_moved` printed and non-zero; `still_diff`, every `moved_missing`, every `moved_extra`, `r_bad`, `miss_bad`, `n_unclassed` all zero; `miss_prod`, `miss_ident`, `r_tgt` printed | bench stdout | session |
| 8 | Reconciliation against map §3.10a's prior reading, stated as a comparison and **not** as a bar. A divergence is reported as a finding and no assertion is adjusted (§3, inv. 43) | item 7 against the map | session |
| 9 | **Negative control on the FLIP side** (inv. 68): in a scratch copy, make `prod`'s `rr` read from the `E`-geometry — undoing the anchoring for that field alone. `moved_missing['rr']` MUST go non-zero and D4b MUST turn red; D4a MUST stay green. Revert; `git status --porcelain` clean | before/after stdout, `git status` | session |
| 10 | **Negative control on the HOLD side** — the case the control exists for: in a scratch copy, compute `prod`'s `a` from the anchor instead of `E`, i.e. move the reference leg. `moved_extra['a']` MUST go non-zero and D4b MUST turn red; D4a MUST stay green. Revert; tree clean | before/after stdout, `git status` | session |
| 11 | D1, D2, D3, D5, D6, D7, D8, D9 lines byte-identical between the baseline of item 4 and the final tree, shown by `diff` over the two captured outputs | both trees | session |
| 12 | `--lab-selftest` exit code and verdict line verbatim on BOTH trees, with the reason stated if it is still `НЕИСПРАВНА` | bench stdout | session |
| 13 | Gate step 14: check count before and after, delta attributed to section `G`, which reports its own count; the section refuses to pass on zero; no socket opened | `backtest_guard_bench.py` stdout | session |
| 14 | Every fixture row of C2 shown landing in its named bucket, and the clean fixtures shown clean | step 14 stdout | session |
| 15 | Full local replay of every `bench.yml` step under `bash -euo pipefail`, per-step counts and total. **State plainly that a local replay is not a runner run.** If step 5 fails, prove it fails identically on a pristine checkout — map §10 records that ceiling as environmental and it is not a product failure | step output | session |
| 16 | Hosted `Bench gate` on the pushed branch: workflow, run number, head SHA, status and conclusion from the jobs API. **Per-step check counts are NOT claimed from the runner** — the logs endpoint answers 403 to a session holding no token (inv. 44) | jobs API | session |

**No item is assigned to a dispatch and none is deferred.** This TZ requires no archive read,
so there is no runner-only item and the report is not PARTIAL for anything (contract §9).

---

## 8. Commit Message

Use verbatim (contract §8):

```
TZ-37: D4 re-registered — anchor-off identity plus live partition, construction in gate step 14
```

---

## 9. Report

`CryptoReports/TZ-37-lab-identity-partition-report.md`, §10 format, direct to `main`.
Beyond the template:

- `## Scope Executed` names the class (**branch TZ**) before any clause reads off it.
- `## Fingerprints` gives the anchor LINE NUMBERS, not a verdict, plus both bench files
  before and after.
- `## Implementation Summary` states the `d4_partition` signature and return keys as built,
  the D9 `want_identity` proof from item 6, and the section letter taken in the guard bench
  with the `E` collision named.
- `## Test Results` carries every count as a count, with the command beside it, and the two
  negative controls with their before/after readings.
- `## Deviations` records any place where the specified rule met a case §4 did not name —
  particularly a non-zero `n_unclassed`, which is a finding and never a default.
- `## Remaining Risks` names the outstanding `prod_anchor` archive dispatch as untouched by
  this work, and states whether the lab's verdict is now `ИСПРАВНА`.
- `## Final Repository State` carries **"NOT IN EFFECT UNTIL MERGED"** and says nothing about
  `main` or about this report's own commit (map inv. 54).
