# TZ-36 — Anchored recorders

**Canonical filename: `CryptoTZ/TZ-36-anchored-recorders.md`.** Name the committed
file from this line, never from the name the file arrived under (contract §3).

| Field | Value |
|---|---|
| Report | `CryptoReports/TZ-36-anchored-recorders-report.md` |
| Branch | `claude/tz-36-anchored-recorders` |
| Class | **branch TZ** — the scope names files outside `CryptoReports/**` (contract §8) |
| Model | **Opus** |

---

## 0. Fingerprint gate — blocking

Run contract §5 before any work. Required map revision, matched as an exact
substring:

```
**Revision 2026-09-08-b.**
```

All seven content anchors must be present, each matched as an exact substring:

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-08-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `68. **A negative control names which items must flip and which must not.**` |

The map's `## 0` file table at this revision — measure each and report under
`## Fingerprints`:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Three benches this TZ names have no row in that table by design (map §0), so their
figures are stated here** and are part of this gate:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 3881 | `45e2294c5fc82f96a7e66b84c2a094c2` |
| `bench/backtest_guard_bench.py` | 971 | `19427e79133d48870d76eb0c908c69f6` |
| `bench/verify_bench.py` | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |

Contract required: `EXECUTOR-INSTRUCTIONS.md` **v20**, 814 lines, MD5
`9a257890e9db663eb0fc74129f4841e0`.

**`journal/write.js` and `bench/journal_bench.js` carry no pin anywhere and none is
invented here.** Read their line count and MD5 on the baseline tree and report both
under `## Fingerprints`, so the next TZ touching them has a baseline that was
measured rather than declared.

---

## 1. What is wrong

TZ-33 moved production's PUBLICATION PRICE from `cur` to the anchor. Two
instruments record what production publishes and neither moved with it. One cause,
two sites — map inv. 66.

**Site 1, the journal, and it is the primary.** Map §3.13:

> `geo` is now the ANCHORED geometry … `dec` and `inv` are still the decision taken
> at `cur`, so on a waiting row **the journal records a stop the board did not
> print** while `planLine` printed `decA.inv.price`, and the outcome layer then
> times its `stop` touch against that recorded level — against a stop no card ever
> named.

Records are immutable (map inv. 38), so **every 13:00 UTC run adds another one while
this waits**. The repair is additive and forward-only; nothing already written is
reopened.

**Site 2, the bench arm.** Map §3.10:

> **The production arm is therefore ADMITTED at the anchor and RESOLVED at `cur`**,
> so on a waiting row it counts the outcome of an entry production would not have
> taken, and its `R` pairs an anchored `rr` with a barrier pair measured somewhere
> else. The decision is right for the substituted arms and wrong for the production
> one, and the repair is a SECOND arm rather than a moved leg.

**Production is correct and is not touched.** `index.html:3351` passes all fourteen
arguments to `directionVerdict`, `planLine` prints `decA.inv.price`, and the
termination property `geoA.wait === null` holds. This TZ changes recorders only.

---

## 2. Scope

`## Scope` is the complete authorisation (contract §6). Anything not listed is
forbidden however obviously beneficial it looks.

**Files to Modify**

| File | Stage |
|---|---|
| `journal/write.js` | A, B |
| `bench/journal_bench.js` | A, B, D |
| `bench/backtest_bench.py` | C |
| `bench/backtest_guard_bench.py` | C |

**Files to Create** — none.
**Files to Delete** — none.

**Explicitly NOT authorised**, and each would be a defect if touched:
`index.html` · `main.py` · `catalysts.json` · `.github/workflows/**` ·
`.gitignore` · `SYSTEM-MAP-CRYPTOCALCUL.md` · `EXECUTOR-INSTRUCTIONS.md` ·
`ANALYST-INSTRUCTIONS.md` · `journal/data/**` · `journal/out/**` ·
`journal/runs.jsonl` · `bench/verify_bench.py`.

**No bench file is created, so no `bench.yml` wiring is required** and the workflow
is out of scope; hard floor item 12's second clause does not fire here. The
generated bridge files this bench writes are already covered by the `bench/_*`
prefix in `.gitignore` — do not edit that file to name a new one.

**Hard floor, quoted so it can be compared rather than recalled** (map inv. 55).
Contract §7 item 1:

> **No change to scoring, leverage, liquidation or geometry math** unless the TZ
> explicitly cites a completed backtest (map §3.10b). `scoreCandidate`,
> `momentumScore`, `qualityScore`, `scoreFinish`, `tradeGeometry`, `marketRegime`,
> `directionVerdict`, `leverageDecision`, `invalidationInfo`, `protectionPlan`,
> `liqPrice`, `liqTouchProb`, `residual7` are closed to edits by default.

**This TZ cites no backtest and requires no edit to any of them.** It changes what
two recorders STORE about what those functions already return. If any stage appears
to require editing one of them, the stage is defective — report BLOCKED and quote it.

Contract §7 item 2:

> **Never edit a bench to make it pass.** A red bench is either a product defect or
> a stale expectation; both are findings, neither is a licence to change the
> assertion.

Stage A changes the journal's schema, so `bench/journal_bench.js` expectations about
the side block MUST move with it. That is a specified schema change, not a bench
edited to pass: every expectation this TZ authorises is named in Stage A and Stage B
and nowhere else. An assertion that turns red for any other reason is a finding.

---

## 3. Stage A — the journal records the anchored decision

`journal/write.js`.

### A0 — the fourteenth parameter, read before anything else

Read the writer's call to `directionVerdict` and **state its argument count in the
report**. The signature is fourteen parameters and `btcStats` is the last:

```
function directionVerdict(cd, pair, name, cur, p24, qv, isLong, reg, dec, hi24, lo24, rc7, nowMs, btcStats)
```

A thirteen-argument call leaves `btcStats` undefined, so the second pass runs
`leverageDecision(cd, anchor, isLong, undefined)`, `lBtcCheck` returns `null`, and
the BTC ceiling drops out of the anchored candidate set — **higher leverage than
production issues, on waiting rows only, invisible on every `СЕЙЧАС` row.** If the
call is short, pass the same `btcStats` object the writer already builds for the
board and say so in the report; if it is already fourteen, say that.

### A1 — two new fields on the side block

The side block is `rel · score · tier · ch · action · why · note · verdict · wait ·
tgt · geo · dec · inv` (map §3.13). Add, in the same storage convention the block
already uses for `geo` and `dec` — production returns stored WHOLE and unrounded:

| Field | Value | When written |
|---|---|---|
| `anchor` | `v.anchor` | always, on every side block that carries `geo` or `dec` |
| `decA` | `v.decA`, the whole object | **always**, unconditionally |

`v` is the object `directionVerdict` returns; both members already exist on it
(`index.html:2044`, `:2080`, `:2081`).

**`decA` is stored unconditionally and the duplication is deliberate.** On a
`СЕЙЧАС` row `decA` is `dec` object-identically, so the copy carries no new
information — and storing it only where it differs would put production's pass-2
rule inside every future reader of the corpus, which is the exact class of defect
this TZ repairs. The record exists because the verdict is not reconstructible after
the fact (§3.13); a field whose absence means «look up the rule» is not a record.
`[решение принято мной]` — discarded alternative: conditional storage keyed on
`wait !== null`, rejected because absence then has two causes and no reader can tell
them apart.

**`invA`, conditionally, and the test is named.** Read how `inv` is produced in the
writer today. If it is a hoist of `dec.inv`, add `invA = v.decA ? v.decA.inv : null`
in the same place and by the same construction, so the record stays symmetric. If
`inv` is an independent `invalidationInfo` call, add nothing and report which it was.
State the branch that fired in `## Implementation Summary`.

### A2 — what must NOT move

- `geo` keeps its current meaning: `v.geo`, the ANCHORED geometry. It is not renamed
  and not re-pointed. Renaming it would break every reader of the historical corpus.
- `dec` and `inv` keep their current meaning: the decision taken at `cur`. They are
  not re-pointed either — the board, the card and every leverage control derive from
  the current-price decision (map inv. 14), and the record must keep it.
- No record already written is reopened, corrected or regenerated (map inv. 38).

After this stage the record carries a complete set at each price: `geo` + `anchor` +
`decA` (+ `invA`) at the published entry, `dec` + `inv` at `cur`.

---

## 4. Stage B — the outcome layer resolves against the published stop

`journal/write.js`, the `k:"o"` writer.

### B1 — two new fields on the outcome line

| Field | Value |
|---|---|
| `sstop` | the numeric stop level the resolution actually used |
| `ssrc` | `'decA'` or `'dec'` — which recorded object that level was read from |

Resolution rule, per side:

```
snapshot carries decA  →  level = decA.inv.price ,  ssrc = 'decA'
snapshot has no decA   →  level = dec.inv.price  ,  ssrc = 'dec'
```

### B2 — why the fallback is permitted here, stated so it is not blocked

Map inv. 67 requires a reader to refuse rather than default where an observation is
absent. Refusing here would silently drop the outcome layer for every snapshot
written before this TZ merges — fourteen days of dates that inv. 38 makes
irrecoverable. **The substance of inv. 67 is that nothing is recorded NOWHERE, and
`ssrc` records it on every line.** The epoch boundary therefore becomes readable
from the record, which is what inv. 66 demands of a meaning change:

> Where the records are immutable (inv. 38) the boundary is disclosed and never
> repaired, and it must be readable FROM THE RECORD.

**No outcome line may be written without `ssrc`.** A default in silence is the
defect; a default that names itself is the disclosure.

### B3 — what must NOT move

- The horizon, the window and the touch semantics are unchanged. Only WHICH recorded
  level the `stop` touch is timed against changes, plus the two new fields.
- **No fill gate is added to the journal.** The outcome line already carries the
  first touch of `wait`; whether a waiting setup was ever filled is a join the
  analysis does downstream. Adding the gate here would change the meaning of
  existing fields under their own names, which is the defect this TZ closes.
- `p0`, `p1`, `hi`, `lo`, the `tgt` touch, the `wait` touch and `first ∈
  tgt|stop|tie|null` are untouched.

### B4 — the readers of `dec`/`inv`, enumerated (map inv. 66)

The report names each and states whether it moved:

| Reader | Reads | Moves in this TZ |
|---|---|---|
| `journal/write.js` outcome layer | the stop level | **yes** — Stage B |
| `bench/journal_bench.js` | the side block's shape and leaves | **yes** — Stage A, D |
| `ANALYST-INSTRUCTIONS.md` §5 | `cd` and `btc` only, never a side block | no — state this by reading the methodology, not from memory |
| `SYSTEM-MAP-CRYPTOCALCUL.md` §3.13 | the schema description | no — the map is the Architect's and follows the merge |

---

## 5. Stage C — `--target` gains a second production arm

`bench/backtest_bench.py`.

### C1 — the arm

Add `prod_anchor` beside the existing arms. It is ADDITIVE: the existing production
arm and every substituted arm keep their current numbers exactly, so every
`--target` figure standing in the map stays comparable to itself.

**The shared reference leg is not touched.** `stop`, `dist`, `b_log` and the
`E`-based first-touch resolution are read by the substituted arms; moving them would
move those arms (map §3.10). `prod_anchor` computes its own levels and calls the
resolver a second time.

### C2 — semantics, decided here

| Element | Value |
|---|---|
| Entry | the anchor — `geoA`'s anchor, i.e. `geo.wait` where the chase rule fired, `cur` where it did not |
| Target | the same 90-day extremum the production arm uses — a price, so it does not move with `E` |
| Stop | `decA.inv.price`, the anchored stop |
| Fill | the setup exists only if the anchor is TOUCHED inside the horizon; the fill hour opens the resolution window |
| Window | fill hour → the SAME horizon end the production arm uses. The horizon is not extended |
| Outcomes | `tgt` · `stop` · `tie` · `никуда` · **`unfilled`** — a fifth class the existing arm cannot produce |
| `Ω` | `n_tgt / n_stop` over FILLED setups only, with `P(unfilled)` and `P(никуда \| filled)` printed beside it |
| Bar | `1 / RR_MIN`, extracted from `index.html` at run time — no numeral in the rule (map inv. 65) |

`[решение принято мной]` on two points. **The fill gate is in** — an arm admitted at
the anchor and resolved from `cur` counts trades production would not have taken,
and an arm resolved at the anchor with no fill gate counts trades that were never
entered; both are fictions and only the pair repairs it. **The window is not
extended past the original horizon** — discarded alternative `[fill, fill + H]`,
rejected because the horizon is the binding constraint on this whole measurement
(map §3.10a D3) and lengthening it silently would move the one quantity every
standing result is truncated by.

`tie` extends unchanged: anchor and stop inside one hourly candle is genuinely
unresolvable and is recorded, not guessed.

### C3 — section D controls, offline, in `--lab-selftest`

Two new controls beside D1–D6. Both are known-answer and neither reads the archive.

**D7 — the partition (map inv. 68).** On a world where the chase rule fires on a
known subset of rows:

- rows with `geo.wait === null` — `prod_anchor` is bit-identical to `prod` in every
  field. **These must NOT flip.**
- rows with `geo.wait !== null` — `prod_anchor` differs from `prod` in at least one
  of entry price, stop level, resolution start hour. **These MUST flip.**
- both counts are asserted non-zero (map inv. 22).

A control that flips everything has localised nothing and one that flips nothing has
not run. The partition is written here rather than discovered at run time.

**D8 — identity (map inv. 45).** With the anchor forced to `cur` on every row,
`prod_anchor` is bit-identical to `prod` on every row, zero differences, and the
waiting count reads zero. A comparator never proven on identity supports no claim
about a real diff.

**D1–D6 must be unchanged.** Record their counts on the baseline tree first; any
movement in them is a finding, not a licence to adjust.

### C4 — gate step 14

`bench/backtest_guard_bench.py` gains a section asserting `prod_anchor`'s
construction offline, on synthetic input, in the style the file already uses: every
assertion calls the bench's own function by name and compares its return, `requests`
stays stubbed, no socket is opened. Minimum: the fill gate admits a touched anchor
and refuses an untouched one; the window ends at the original horizon; `unfilled` is
produced and is counted separately from `никуда`.

### C5 — no archive reading in this session

The archive figure for `prod_anchor` is a `backtest_bench.yml` dispatch (`--fetch`
then `--target`) and **this TZ does not ask for it** — contract §7 item 9, map
inv. 44. Build the arm, self-test it offline, and report that the reading is
outstanding. Do not forecast what it will say.

---

## 6. Stage D — close §0's open attribution

`bench/journal_bench.js`.

Map §0 carries an unattributed fall:

> The counter fell 693 895 → 691 836, **−2 059** … **The MAGNITUDE is still
> unattributed and is not assumed benign.** The reading that closes it is the count
> of side blocks carrying `wait !== null` in the corpus that bench writes — 303
> files, 8 481 rows at this run — and TZ-36 opens the journal anyway, so it costs
> nothing there.

### D1 — the census, taken on the BASELINE tree, before any edit

Contract §9: baseline first. On the unmodified tree, over the corpus
`journal_bench.js` generates, count and print:

| Term | Definition |
|---|---|
| `n_wait` | side blocks with `wait !== null` |
| `n_geonull` | side blocks with `geo === null` while `dec.inv` is present |
| `n_side` | side blocks total |
| `n_files`, `n_rows` | corpus size, for comparison against 303 / 8 481 |

### D2 — the arithmetic

At TZ-33 a waiting row's `geo` became `geoA`, whose `wait` is null by the
termination property, so each such row loses exactly one numeric leaf. A row whose
second pass refused loses the whole `geo` object's leaves instead. Show the
reconstruction of **−2 059** term by term from `n_wait` and `n_geonull`.

**If it does not reconstruct, report the residual as a finding.** Do not adjust the
census to fit the number, and do not declare the attribution closed on a partial
match — a figure read is not a figure explained, and that is the whole reason this
row is still open.

### D3 — the census is PRINTED, never counted

Map inv. 43: a quantity that is merely measured and printed is not a check. The
census must not increment the check counter, or step 7 moves for the reading that
explains step 7 and the attribution becomes circular. Assert explicitly that the
counter moved only by the assertions Stage A and Stage B authorise, and name them.

### D4 — step 7 after the change

The side block gains `anchor`, `decA` (and possibly `invA`), and the outcome line
gains `sstop`. Step 7 counts numeric leaves, so it WILL rise. Record the new total
and attribute the delta term by term, in the shape §0's table uses.

**Publish the measurement, never the prediction** (map inv. 43). TZ-25 predicted a
step-8 delta of +4 and was wrong by two orders of magnitude; no number is written
here for that reason.

---

## 7. Validation

Written by the Architect. Every item names its artifact and its source. An item that
cannot be run FAILS and is never «not applicable» (contract §9).

| # | Item | Artifact | Source |
|---:|---|---|---|
| 1 | `node --check journal/write.js` — exit 0 | stdout, exit code | session |
| 2 | `node --check bench/journal_bench.js` — exit 0 | stdout, exit code | session |
| 3 | `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` — exit 0 | exit code | session |
| 4 | `git diff --stat` shows **zero** changed lines in `index.html` and `main.py` | diff output | session |
| 5 | A0 answered: the writer's `directionVerdict` argument count before and after, with the count of waiting rows in the baseline corpus if it was thirteen | source line, census | session |
| 6 | Baseline census D1 — `n_wait`, `n_geonull`, `n_side`, `n_files`, `n_rows`, taken before the first edit | `journal_bench.js` stdout on the baseline tree | session |
| 7 | Attribution D2 — the term-by-term reconstruction of −2 059, or the residual named | arithmetic over item 6 | session |
| 8 | Writer partition control: a fixture pair, one `wait !== null` row and one `wait === null` row. Required — the waiting row's stored `decA.inv.price` equals `invalidationInfo(cd, anchor, isLong).price` computed at run time from `index.html` and differs from `dec.inv.price`; the `СЕЙЧАС` row's `decA` is object-identical to `dec` and `anchor === cur`. Both counts non-zero | `journal_bench.js` output | session |
| 9 | Negative control on item 8 (map inv. 68): in a scratch copy, revert the writer to storing `dec` as `decA`. The waiting assertion **MUST** turn red; the `СЕЙЧАС` assertion **MUST** stay green. Revert the scratch copy and confirm the tree is clean | before/after output, `git status` | session |
| 10 | Outcome epoch: a fixture pair, one snapshot carrying `decA` and one without. Required — `ssrc:'decA'` and `ssrc:'dec'` respectively, `sstop` matching the level each names, and **no** outcome line written without `ssrc` | `journal_bench.js` output | session |
| 11 | `--lab-selftest` D7 partition passes, with both subset counts printed and non-zero | bench stdout | session |
| 12 | `--lab-selftest` D8 identity: zero differences, waiting count zero | bench stdout | session |
| 13 | `--lab-selftest` full run: exit code and per-section counts, with **D1–D6 unchanged** against a baseline recorded before the edit | bench stdout, both trees | session |
| 14 | Gate step 14 new section: check count before and after, delta attributed, no socket opened | `backtest_guard_bench.py` stdout | session |
| 15 | Step 7 after the change: new total, delta attributed term by term, and the assertion that the census incremented no counter (D3) | `journal_bench.js` stdout | session |
| 16 | Full local replay of every `bench.yml` step under `bash -euo pipefail`, with per-step counts and the total. State plainly that a local replay is not a runner run | step output | session |
| 17 | Reader enumeration B4 answered, each row justified by a command rather than by recollection | grep output over `ANALYST-INSTRUCTIONS.md` and the tree | session |
| 18 | **Runner, NOT this session.** The `prod_anchor` archive reading is a `backtest_bench.yml` dispatch (`--fetch`, then `--target`) and is outstanding. The report states this as an outstanding reading and forecasts nothing about it | — | Boss dispatch |

Item 18 is assigned rather than skipped: a session fetch cannot stand behind a
product fact (map inv. 44), and an item asking for one is unrunnable as written. The
report is **not PARTIAL** for it (contract §9).

---

## 8. Commit Message

Use verbatim (contract §8):

```
TZ-36: anchored recorders — journal anchor/decA, outcome ssrc, --target prod_anchor arm
```

---

## 9. Report

`CryptoReports/TZ-36-anchored-recorders-report.md`, §10 format, direct to `main`.
Beyond the template:

- `## Scope Executed` names the class (**branch TZ**) before any clause reads off it.
- `## Implementation Summary` states the A0 answer, the `invA` branch that fired, and
  the reader enumeration of B4.
- `## Test Results` carries every count as a count, with the command beside it.
- `## Fingerprints` adds `journal/write.js` and `bench/journal_bench.js` line counts
  and MD5s, which no document currently pins.
- `## Remaining Risks` names the outstanding `prod_anchor` dispatch and the step-7
  delta this change introduces.
- `## Final Repository State` carries **"NOT IN EFFECT UNTIL MERGED"** and says
  nothing about `main` or about this report's own commit (map inv. 54).
