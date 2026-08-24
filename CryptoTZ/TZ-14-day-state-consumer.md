# TZ-14 — Adoption of `DAY_RANGE_ABNORMAL` and the day-state consumer

**Canonical filename: `TZ-14-day-state-consumer.md`.** Commit the file under
exactly this name in `CryptoTZ/`, taken from this line and never from the name the
artifact arrived under.

**Model: Opus.** A production edit that changes what the screen says, under a
whole-board no-regression obligation, a purity obligation across five decision
functions, and two new bench sections that must be able to fail. Not mechanical.

---

## 0. Fingerprint gate — compare BEFORE any work

Run `git fetch --all --prune` first. Compare against `origin/main`, never local
`main`. A mismatch on any row is **ЗАБЛОКИРОВАНО**: stop, report, do nothing else.

| Anchor | Exact string that must be present in `SYSTEM-MAP-CRYPTOCALCUL.md` |
|---|---|
| revision | `**Revision 2026-08-24-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `49. **An admissibility band is derived from a null computed in the same run.**` |

Baseline files at this revision:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3666 | `cef52cf6eb00ff063e66510a5bd0f828` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**The record file is in the gate table deliberately.** This TZ copies a number out
of it into production. A record that has moved since it was audited would make the
constant agree with a run nobody read.

Gate baseline: `bench.yml`, 12 steps, **1 250 369** checks, measured from a
`git worktree` at `origin/main`, never assumed.

Check the clone for truncation (`git rev-parse --is-shallow-repository`) and deepen
before assessing anything historical.

---

## 1. Why this exists

TZ-13 made the measure reach the screen and made the calibration measure the right
random variable. It deliberately adopted nothing: a TZ that both produces a number
and spends it can always rescue the number by adjusting what it is spent on.

The number now exists, decided by a rule registered before the data and derived
from a null simulated in the same run (inv. 23, 49):

```
DAY_RANGE_ABNORMAL = 1.39
```

pinned to `bench/exhaustion-calibration.txt` — 1 110 dates, 24 spot assets,
measured ρ, null p90 1.2393 at MC s.e. 0.00117, empirical p90 1.3911, all four
admissibility conditions passing, reproduced on a second runner.

**Two things are missing and this TZ delivers both.**

1. **The constant is in no line of `index.html`,** so `listExhaustion` still returns
   `abnormal: false` unconditionally and inv. 46 has nothing to compare.
2. **The board prints a number with no scale.** §3.17 row 2 says «медиана списка
   2,4 обычного дня» and the reader must know from memory that 1.39 is where a day
   stops being ordinary. The regime banner — the one list-wide element on screen —
   still says nothing about how far into the regime the session sits, which is the
   gap §3.16 was built to close.

**What this TZ is NOT.** It adds no veto, no colour on the regime line, no score
effect, no ranking factor. `abnormal` becomes a printed word and nothing else. The
day-range measure is a statement about the session's geometry, in the standing of
§3.12 Layer 1; turning a p90 into a prohibition would close roughly a tenth of all
sessions on both sides on the strength of zero measured evidence that entering on
such a day ends worse, and inv. 32 and §3.10b forbid acting on that.
`[решение принято мной]` Discarded: making exhaustion a Layer 1 veto. It is
reversed only by a journal-based measurement of outcomes conditioned on the day
state — which the journal already supports, because the coin-day ratio and the
list median are reconstructible from `px.hi`, `px.lo`, `px.cur` and
`cd.volatility` by cutting production's own functions (§8, inv. 21).

---

## 2. Scope — four stages

### Stage A — adopt the constant

In the production constants block of `index.html`, immediately after
`var REG_STRESS_Z = 2.0;` and its comment:

```js
var DAY_RANGE_ABNORMAL = 1.39;
```

The comment above it must name, in English, exactly three things and nothing else:
that the number is the 90th percentile of the distribution of PER-DATE LIST MEDIANS
(inv. 47), that it is pinned to `bench/exhaustion-calibration.txt` (inv. 46), and
that its null p90 was 1.2393 so the reading is a measurement of the day, not a
probability.

In `listExhaustion`, the two `abnormal:` fields become:

```js
if (n < 8) return { median: null, n: n, abnormal: false };
...
return { median: med, n: n, abnormal: med >= DAY_RANGE_ABNORMAL };
```

**`>=`, not `>`.** «At or above the calibrated p90» is what the rule adopted; a tie
on a continuous quantity is a measure-zero case and must fall on the named side
rather than on the side an operator happens to be written with. A null median or a
below-quorum list stays `abnormal: false` — an unmeasured list is not a quiet one.

The comparison lives in `listExhaustion` and in no other function.

### Stage B — one wording function, two surfaces

**B1. A single comma-decimal formatter.** `boardHtml` currently declares a local
`sqzNum(x)`. Lift it to a top-level `function numRu(x, d)` returning
`x.toFixed(d).replace('.', ',')`, replace every `sqzNum(` call with `numRu(`… `, 1)`
and delete the local. Board output must stay byte-identical; this is a
single-site obligation (inv. 20), not a cosmetic change — the day line prints one
decimal for the median and two for the threshold, and two rounding helpers would
eventually disagree.

**B2. `function dayStateNote(day)`,** declared next to `regimeBanner`. Returns the
empty string when `day` is absent, `day.median === null` or `day.abnormal` is
false. Otherwise it returns exactly one sentence, in `\uXXXX` escapes:

```
ДЕНЬ УЖЕ ВЫНЕСЕН — медиана списка <numRu(day.median,1)> обычного дня, порог <numRu(DAY_RANGE_ABNORMAL,2)>. Мера дня, не запрет.
```

No other function may build this sentence, and no other function may compare
against the constant. Both surfaces call `dayStateNote` — a board silent about what
the list said is the same defect inv. 33 names for the card and the board.

**B3. The banner.** `regimeBanner(reg, isLong)` keeps its signature and its
existing `<div>` **byte-identical**. When `dayStateNote(reg.day)` is non-empty it
APPENDS a second `<div>` in the same shape — `margin`, `padding`, `border-left`,
`font-size`, `letter-spacing` copied from the existing line — coloured
`var(--accent)`.

Amber is the decision, and it is the system's existing vocabulary: red is a closed
side, green is an open one, and amber is the «ВНИМАНИЕ» alarm's standing —
attention without prohibition. `[решение принято мной]` Discarded: recolouring the
regime line itself, which would make one line carry two independent facts and would
overwrite the stress red exactly when it matters most.

The output at `abnormal === false` must be a strict PREFIX of the output at
`abnormal === true` — that is how the bench proves the regime line was untouched.

**B4. «РИСК ВЫНОСА» row 2.** Immediately after the list line and before the
existing `bd-note` caption, when `dayStateNote` is non-empty, one
`<div class="bd-kv">` whose value span carries the same sentence in
`var(--accent)`. The `.bd-sec` element itself takes **no inline `style`** — that
kills the metal ring (§3.7, inv. 19). The caption's own text does not change.

### Stage C — the wiring

In `update()`, immediately after `lastRows = rows;`:

```js
reg.day = listExhaustion(rows);
```

Unconditional, above the `sideOn` branch that renders the banner. The board keeps
its own `listExhaustion(lastRows)` call unchanged. `[решение принято мной]`
Discarded: routing the board through `lastCtx.reg.day` to reach a single call site.
It is one pure function over one array, so two call sites cannot disagree in value,
while making the board depend on a new `lastCtx` field would force every board
fixture to invent it — which is exactly the shape inv. 48 exists to catch.

### Stage D — the gate, `bench/exhaustion_bench.js`

Four additions. Every counter is incremented at the comparison site (inv. 43).

**D1 — section `record` (inv. 46).** Cut `DAY_RANGE_ABNORMAL` out of `index.html`
and read the `DAY_RANGE_ABNORMAL = X.XX` line out of
`bench/exhaustion-calibration.txt`. Assert: exactly one declaration in the source;
exactly one such line in the record; the two values equal as numbers; the source
literal carries two decimals. A missing, unreadable or line-less record is a
**failure**, never a skip and never a fallback (inv. 22, 42).

**D2 — section `threshold`.** The truth table of `abnormal`, built from rows whose
ratios are known by construction: median at `1.39 − ε` → false, at exactly `1.39` →
true, at `1.39 + ε` → true, `median === null` → false, `n = 7` → false. Then the
negative control that proves the comparison reads the constant and not a literal:
re-cut the source with `DAY_RANGE_ABNORMAL` rewritten to `9.99` and assert the same
list flips to false.

**D3 — sections `inert` and `banner`, inverted as their own comments predict.** At
`abnormal === false` and at a below-quorum `reg.day`, all ten (state × side)
banner outputs stay byte-identical to `origin/main`. At `abnormal === true`, the
`false` output is a strict prefix of the `true` output, and the tail contains the
median text, the threshold text and the state word. `dayStateNote` is proven
deterministic and non-mutating, like `regimeBanner` before it.

**D4 — wiring (inv. 48), two claims.** First, structural: extend section H's
reader/producer mechanism so `reg.day` is proven to be a field `update()` writes
and `regimeBanner` reads, with the same one-check-per-field-read accounting and the
same mutation controls. Second, live: run the real `update()` over two fixture
lists whose list medians straddle the constant, render through the real DOM path,
and assert the banner gains exactly the day line and nothing else. A bench that
builds its own rows proves the function; this proves the reach.

**D5 — both surfaces (inv. 33).** For one set of rows above the threshold, render
the card list and `boardHtml` and assert the identical sentence appears in both,
and that the identifier `DAY_RANGE_ABNORMAL` occurs in exactly three enclosing
sites in `index.html` — the declaration, `listExhaustion`, `dayStateNote` — using
the brace matcher section H already carries.

---

## 3. Non-goals — do not do these

1. **Do not touch `.github/workflows/calib.yml` or `bench/exhaustion_calib.py`.**
   `calib.yml`'s paths filter names both, so ANY edit re-fires the full three-year
   calibration on the branch and commits a fresh record — on an archive two days
   longer than the audited one, which can move the p90 off 1.39 and turn D1 red.
   Editing either file is a re-calibration, never a touch-up. The stale
   `(TZ-11 stage B)` inside `calib.yml`'s hardcoded commit message stays.
2. **Do not re-run, recompute, round, cross-check or "sanity-check" 1.39.** The
   rule decided it. A number re-derived by the TZ that spends it is fitting.
3. **Do not let `abnormal` or `reg.day` reach a decision.** `scoreCandidate`,
   `tradeGeometry`, `leverageDecision`, `directionVerdict`, `liqPrice`, the tier
   badge, `byScore`, `assignRanks`, `planLine` and `journal/write.js` are untouched
   (inv. 27). No veto, no penalty, no reordering, no hidden card.
4. **Do not touch the regime line's own bytes, its colour or its wording.**
5. **Do not add a threshold word anywhere else** — not to the card, not to
   «ГРАНИЦЫ СДЕЛКИ», not to «ЦЕНА ВРЕМЕНИ», not to the tier badge.
6. **Do not add or reorder a board block, and do not put an inline `style` on a
   `.bd-sec`** (§3.7, inv. 15, 18, 19).
7. **Do not touch** `main.py`, `catalysts.json`, `journal/**`, `bench.yml`, or the
   count of gate steps.
8. **Do not renumber** a section or an invariant, and do not fix the three
   pre-existing issues in §6.
9. **Do not tune anything.** No new constant beyond `DAY_RANGE_ABNORMAL`, no second
   threshold, no hysteresis on the day state.

---

## 4. Files

**Modified:** `index.html`, `bench/exhaustion_bench.js`.

**Created:** none. **Renamed:** none. **Deleted:** none.

---

## 5. Validation — written by the Architect, run by the Executor

Every item is mandatory and every count is reported. A validator that compared
nothing is a failure (inv. 22).

1. **Compiles and guards.** `python3 -m py_compile main.py`; `node --check` on the
   extracted `<script>` and on `exhaustion_bench.js`. ES5 guard over every added
   line of `index.html`; Cyrillic guard — every new on-screen string is `\uXXXX`
   escaped and every new comment is English. Both guards report the number of lines
   checked and fail on zero.
2. **The constant.** Declared exactly once, two decimals, equal to the record. Then
   two real mutations of the working tree, each restored and verified by MD5:
   delete the record file → D1 exits non-zero naming the missing file; set the
   source constant to `1.40` → D1 exits non-zero naming both values.
3. **The truth table**, all five cases of D2 plus the `9.99` negative control,
   reported as a table.
4. **Banner identity.** All ten (state × side) combinations at `abnormal === false`
   byte-identical to `origin/main`; at `abnormal === true` the false output is a
   strict prefix; below-quorum identical. Report the appended tail verbatim once.
5. **Live path (inv. 48).** Real `update()` + real render, two lists straddling
   1.39: report each list's median, `n`, and whether the day line is present.
   Everything outside that line byte-identical between the two.
6. **Both surfaces.** The same sentence in the card list and in «РИСК ВЫНОСА» for
   the same rows, compared as strings; the enclosing-site enumeration of D5
   printed.
7. **No-regression, identity first (inv. 45).** `prot_bench.js`'s unconditional
   identity run reports zero differences before anything else is offered as
   evidence. Then the whole-board differ against `origin/main` across the full
   scenario set: boards may differ ONLY by the added day line, and ONLY on
   scenarios whose list median is at or above 1.39. Report boards compared, boards
   differing only in that line, boards differing anywhere else — the last must be
   **zero** — and enumerate every differing board with its before and after.
8. **Purity (inv. 27), proven by perturbation.** Take one scenario and scale the
   rows' `hi24`/`lo24` until `abnormal` flips, then assert that for every coin
   `sc.score`, `vd.action`, `vd.why`, `dec.L`, `dec.binding`, `dec.moneyBelowMin`,
   `geo.rr`, `inv.price` and the card's number and tier are unchanged, and that the
   journal record `journal/write.js` would write is byte-identical. Report the
   number of fields compared.
9. **Extremes**, all ten: slider edges, null betas, truncated Gist, HTTP 400
   ticker, dead-market fields, missing coeffs fields, absent `btcStats`, absent
   `volatility`, `E ≤ 0`, non-finite `liq`. `update()` throws in none; a board with
   no metrics prints no day line and no `NaN`.
10. **Full gate on a runner, 12 steps.** Baseline 1 250 369 measured from a
    `git worktree` at `origin/main`; candidate measured with the same harness.
    Report the per-step table and explain the delta term by term (inv. 43).
    **Step 7 must read 691 109 unchanged, and that is an assertion, not an
    observation** — this TZ writes no journal field, so any movement there is a
    defect.
11. **Release checklist** items 11, 15 and 17 re-run and reported; plus: the
    `.bd-sec` of «РИСК ВЫНОСА» carries no inline `style` and the metal ring
    survives.

---

## 6. Pre-existing issues — confirm, do not fix

1. `NaN% от входа` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ» — unreachable live.
2. Raw Cyrillic literal in `bench/prot_bench.js`, now at line 177.
3. The Node 20 action pin in `bench.yml`, warning only.

Report each as confirmed-present. Report anything new found, and fix nothing.

---

## 7. Report

`CryptoReports/TZ-14-day-state-consumer-report.md`, straight to `main`.

Mandatory: the fingerprint gate result · scope executed and any deviation stated
plainly · the constant's two sides and the two D1 mutation controls · the truth
table · the banner prefix evidence with the appended tail verbatim · the live-path
result · the whole-board differ counts with every differing board enumerated · the
purity field count · the 12-step table with the delta explained term by term and
step 7 asserted unchanged · runner run ids and conclusions for `Bench gate` ·
confirmation that `calib.yml` did NOT run and that no new calibration record was
committed · line counts and MD5s for `index.html`, `main.py`, `catalysts.json`,
`bench/exhaustion-calibration.txt` and the System Map · branch name and compare
URL.

**NOT IN EFFECT UNTIL MERGED.**
