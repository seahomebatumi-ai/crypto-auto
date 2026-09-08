# TZ-33 — Trade levels are computed at the price the entry is PUBLISHED at

**Canonical filename: `TZ-33-entry-anchor-geometry.md`.** File the artifact under this
name in `CryptoTZ/`, whatever name it arrived under (contract §3).

**Executor model: Opus.** A signature change on `directionVerdict` ripples into every
bench that calls it, and the same second pass has to land in `backtest_bench.py`'s
target driver or the bench stops executing production's own call sequence. Multi-file,
with a math surface underneath.

---

## 0. Fingerprint gate — blocking (contract §5)

Required map revision and every content anchor, quoted in full from
`SYSTEM-MAP-CRYPTOCALCUL.md` `## 0. Fingerprint`. Match each as an exact substring
against the repository copy on `origin/main` after fetching. Any mismatch → BLOCKED
before any work.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-06-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `65. **A bar derived from the constant it judges moves with it.**` |

The map's `## 0` file table at this revision — measure each, report each, act on no
difference (contract §5):

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**`bench/backtest_bench.py` has no row in that table and this TZ states its figure
here, as the map's `## 0` requires of any TZ that needs it: 3703 lines, MD5
`4d4242d37e63a01bdf74c474b3cfcb02`.** The map's own prose still carries 3240 /
`d2dad0f80afa2c191c2faf1d40081a88`, which was TZ-30's reading; two later TZs moved the
file and the map has not been revised since. **This is a known map staleness, not a
gate failure** — the file is not in the fingerprint table, nothing blocks on it, and
the map revision that follows this TZ closes it. Record the measured figure under
`## Pre-existing Issues` and do not act on the difference.

---

## 1. Why — the published stop breaches its own floor, and the veto deletes the trade

`directionVerdict` computes the whole trade at `cur`, the current price, and then
publishes an entry at a different price.

`index.html:2034` — one call, at `cur`:

```
var geo = tradeGeometry(cd, cur, isLong, dec, hi24, lo24);
```

`index.html:1920–1925` — the entry the card actually names:

```
var anchor = isLong ? lo24 : hi24;
if (has(anchor) && anchor > 0 && has(inv.sd)) {
    var lim = isLong ? anchor * (1 + ENTRY_CHASE_SD * inv.sd)
                     : anchor * (1 - ENTRY_CHASE_SD * inv.sd);
    if (isLong ? E > lim : E < lim) g.wait = lim;
}
```

`index.html:2213–2219` — what is printed on a `ЖДАТЬ` card:

```
'\u0412\u0425\u041e\u0414 ' + fmtP(row.vd.wait)      // the pullback price
... fmtP(row.dec.inv.price)                          // the stop, computed at cur
... geo.rr.toFixed(1)                                // the ratio, computed at cur
```

**Entry from one price, stop and ratio from another.** Two consequences, both derived
from production's own constants, neither requiring any market data.

**(a) The stop sits inside the floor that exists to keep it out.** `invalidationInfo`
clamps `dist` to `INV_FLOOR_SD · sigmaDay(vol)` — a distance *from an entry* — so an
entry the call never saw is an entry the floor never protected. Worked at
`INV_FLOOR_SD = 2.0`, `ENTRY_CHASE_SD = 0.5`, `vol = 1 %/h` (`sigmaDay` 0.0490), 24-hour
low 100, published entry 102.4495, target 140:

| stop configuration | 24h run | `cur` | published `СТОП` | actual distance from the published entry | distance if computed at the entry | `R:R` at `cur` | at the entry |
|---|---:|---:|---:|---:|---:|---:|---:|
| structural (`min30` 97) | 2.0σ | 109.798 | 94.624 | **1.56σ** | 2.00σ | 1.99 → **REFUSED** | 3.74 |
| structural | 4.0σ | 119.596 | 94.624 | **1.56σ** | 2.00σ | 0.82 → **REFUSED** | 3.74 |
| floored (`min30` 101) | 3.0σ | 114.697 | 98.526 | **0.78σ** | 2.00σ | 1.56 → **REFUSED** | 3.74 |
| floored | 5.0σ | 124.495 | 98.526 | **0.78σ** | 2.00σ | 0.60 → **REFUSED** | 3.74 |

The breach is on **every** waiting card, never above 1.56σ and as low as 0.78σ against a
floor of 2.0. It is not a tail case: it is what the code does whenever `g.wait` is set.

**(b) The veto deletes trades that clear the bar at their own published entry.** The
anchor is always on the favourable side — `lim < cur` for a long, `lim > cur` for a
short, by the wait's own firing condition — so reward is larger and the structural
distance smaller at `lim`. In the table above the board refuses on `R:R` 0.60–1.99 while
the entry it is naming carries 3.74. **The chase rule currently destroys setups instead
of improving them**, which inverts the reason it exists (map §3.12 Layer 1).

**This is not a new rule. It is production catching up with a rule the system already
runs.** `ANALYST-INSTRUCTIONS.md` §4 states it and the analyst engine has obeyed it
since revision `-b`:

> **Every level of a setup is computed at the price that setup is PUBLISHED at, and that
> price is the row's own ANCHOR.** … `invalidationInfo` is executed with the anchor as
> its entry, the stop is what that call returns, the reward is measured from the anchor
> to the structural target, and the R:R is the ratio at the anchor. **The order is two
> passes and is not circular** … **A level computed at one price and published against
> another is not the same level**.

The same section records the measurement: **«Measured 03.09, fourth run: the published
GRAM stop sat 1.57 daily sigmas from its published entry, under an `INV_FLOOR_SD` that
exists to make exactly that impossible.»** The arithmetic above lands on 1.56σ in the
structural configuration. Two independent derivations, one from a live run and one from
production's constants, on the same number.

So the two engines currently implement one rule two ways, which is what map inv. 20 and
inv. 38 forbid. **This TZ makes production the single implementation and the analyst
contract the description of it.**

**Hard floor item 1 authorisation.** Item 1 closes `tradeGeometry`, `marketRegime`,
`invalidationInfo` and `leverageDecision` to edits «unless the TZ explicitly cites a
completed backtest». The cited backtest is **`bench/backtest_bench.py --regime-gate`,
run on the three-year archive, 145 dates, 27 reconciled coins**, whose own verdict block
registers that it opens a TZ under item 1. **Note what this TZ does and does not do:
none of the four closed functions has a line changed inside it.** What changes is the
call site — `directionVerdict` calls the same functions a second time, at a second
price. The justification above is arithmetic and does not rest on the backtest at all;
the citation is recorded because item 1 requires one, not because the number is doing
work here.

---

## 2. Scope

Four scopes, independent in the sense of contract §6: if D is blocked, complete A, B, C
and report D.

### A · `index.html` — the anchored second pass in `directionVerdict`

`directionVerdict` gains `btcStats` as its **last** positional parameter, because it must
be able to re-run `leverageDecision`, and it currently receives only the already-built
`dec`. Appending keeps every existing positional argument in place.

The body between the geometry call and the return becomes, in order:

1. First pass at `cur`, unchanged, **used only to locate the anchor**.
2. `anchor` = `geo.wait` when the wait fired, `cur` otherwise.
3. When the wait fired: `decA = leverageDecision(cd, anchor, isLong, btcStats)` and
   `geoA = tradeGeometry(cd, anchor, isLong, decA, hi24, lo24)`. When it did not:
   `decA = dec`, `geoA = geo`, with **no second call made at all**.
4. `v.geo = geoA`, plus the anchored decision and the anchor itself on `v`, under
   additive field names.
5. **The veto is evaluated once, on `geoA`** — never on the first pass. A coin refused at
   `cur` must reach the anchor before it can be refused.
6. Catalyst check, unchanged, after the geometry gate as it is today.
7. `action` = `wait` when the first pass set `geo.wait`, `trade` otherwise; `v.wait`
   stays `geo.wait`.

**Two passes terminate and that is a property, not a hope: assert it.** `lim` is built
from `inv.sd`, and `invalidationInfo` returns `sd = sigmaDay(vol)`, which does not depend
on `E`. So `lim` is identical in both passes and the second pass evaluates `E > lim` at
`E === lim`, which is false. **`geoA.wait === null` whenever `geo.wait !== null`** is a
required assertion, not a comment.

`geoA` may be `null` (a `leverageDecision` that fails at the anchor leaves `decA.inv`
absent and `tradeGeometry` returns `null` at its own guard). Handle it exactly as the
existing `if (!geo)` branch handles the first pass — a refusal with a reason, never a
throw.

ES5 only: `var`, string concatenation, no arrow functions, no template literals, Russian
strings as `\uXXXX` escapes (hard floor items 4, 7).

### B · `index.html` — `planLine` reads the anchored objects

`planLine` currently prints `row.dec.inv.price`. It prints the anchored stop instead.
`R:R` already reads `row.vd.geo`, which scope A has made the anchored geometry, so that
line needs no change — verify it, do not rewrite it.

**`row.dec` is NOT touched and must not be.** It is the current-price leverage decision
the card, the board and every leverage control are built on, and map inv. 14 requires
everything the Boss controls to derive from `currentLev` against that decision. The
anchored decision exists for the trade-plan line and for the geometry gate, and for
nothing else.

### C · `bench/backtest_bench.py` — the target driver executes production's own sequence

`TARGET_DRIVER` calls `leverageDecision` once and `tradeGeometry` once, at the frozen
`E`. After scope A, production performs two calls on a waiting row, so the driver as it
stands measures a call sequence production no longer performs — map inv. 42 («a bench
executes production with the same external input as production») and inv. 48 («a bench
that builds its own input proves the function, not the wiring»).

The driver gains the same anchored second pass for the **production arm** (`prod`). The
substituted arms — the `k` grid and the `rr` grid — are unchanged: they exist to move the
TARGET, and the anchor is a property of the entry.

**Record, do not resolve, what this does to the standing numbers.** Every `--target` and
`--regime-gate` figure in the map was measured on the single-pass arm. After this change
the production arm is a different arm and its earlier readings are not comparable. State
that in `## Remaining Risks`; re-measuring is a dispatch and belongs to a later TZ.

### D · Comment and prose sites that describe the single pass (map inv. 50)

A sentence asserting that a mechanism does not exist is load-bearing text that turns
false the moment it is built. Enumerate every comment in `index.html` and every bench
expectation string that describes trade levels as computed at the current price or as
read from `row.dec`, and repair each in this change. At minimum the header comments on
`tradeGeometry` and `planLine`. **Report the full enumeration** — if a site is found that
this TZ did not anticipate, repair it and name it; if one cannot be repaired inside this
scope, name it and the TZ that must.

---

## 3. What must NOT move

Report a violation rather than acting on it.

- `tradeGeometry`, `invalidationInfo`, `leverageDecision`, `marketRegime` — **no line
  inside any of the four bodies.**
- Any constant. This TZ introduces none and tunes none.
- `row.dec` and every leverage control reading it (inv. 14).
- The score, and therefore the board order. The anchor is located after the score is
  fixed and after the side is decided; `scoreCandidate` and `momentumScore` are never
  re-run at the anchor. A score that moved with a hypothetical price would reorder the
  board on a price nobody paid.
- The side. Map inv. 30's guarantee is the regime layer's and is upstream of everything
  here.
- `stateMark`'s glyph vocabulary and `v.wait`'s meaning (inv. 33).
- `catalysts.json`, the `PRIMARY` allow-list, `tokens[]`, any workflow.

---

## 4. Validation — written by the Architect, run by the Executor

Every item runs. An item that cannot run **fails**; it is never "not applicable"
(contract §9).

1. `python3 -m py_compile bench/backtest_bench.py`.
2. `node --check` on the `<script>` block extracted from `index.html`.
3. **Call-site enumeration.** `grep -rn "directionVerdict(" .` across the repository.
   Every call site moves with the signature. **List them all in the report, with the
   file and line.** A site left passing thirteen arguments receives `undefined` for
   `btcStats` and silently drops the BTC-crash ceiling — a wrong number, not a crash.
4. **Known-answer control on the floor, derived at run time (map inv. 61, 65).** Build
   synthetic `cd` / `E` / `hi24` / `lo24` covering both configurations in §1's table —
   the structural stop and the floored stop — such that the wait fires. Assert, for the
   published row:
   `(anchor − stop_published) / anchor  ≥  INV_FLOOR_SD × sigmaDay(vol) − 1e-12` for a
   long and the mirror for a short. **`INV_FLOOR_SD` and `sigmaDay` are cut from
   `index.html` at run time and never typed into the check.** The bar's authority is
   `invalidationInfo`'s own clip and the object judged is the published entry — two
   different authorities, which is what inv. 65 requires of a derived bar.
5. **Negative control (map inv. 23, 50).** Plant the single-pass call back — `planLine`
   reading `row.dec.inv.price`, the veto evaluated on the first pass — and confirm item 4
   turns red on both configurations. Revert, confirm the tree is clean, confirm item 4 is
   green again. **A check never proven able to fail is not a check.**
6. **Termination assertion.** On every synthetic row where the first pass set
   `geo.wait`, assert `geoA.wait === null`. Count the rows compared and fail on zero
   (inv. 22).
7. **Identity control (map inv. 45).** On rows where the wait does NOT fire, the anchored
   objects must be the first-pass objects. Run the comparison with the same revision on
   both sides first and confirm zero differences, then confirm every non-waiting row is
   unchanged field by field. Count the comparisons.
8. **Direction of the change, measured not asserted.** Over the synthetic set, count and
   report: rows that were `none` at `cur` and are `wait` at the anchor, rows that were
   `wait` and are now `none`, rows unchanged. Both directions are legitimate outcomes —
   the anchor tightens the stop test and loosens the ratio test — and the report states
   the counts rather than a claim about them.
9. **Gate replay.** Run `.github/workflows/bench.yml`'s steps locally against the
   unmodified checkout first, then against the change. Report every step's check count on
   both sides, term by term for any that moved (map inv. 43). **Step 14
   (`bench/backtest_guard_bench.py`) must still build all four bundles closed** —
   scope C adds identifiers to the target driver and an unresolved one is exactly what
   that step exists to catch (map inv. 60).
10. **A local replay is not a runner run.** Say which workflows executed on GitHub with
    their conclusion, and which did not, with the reason (contract §9). Do not forecast a
    gate result.

---

## 5. Files

**Modify:** `index.html` · `bench/backtest_bench.py` · any bench whose
`directionVerdict` call site item 3 finds.

**Create:** nothing.

**Delete:** nothing.

---

## 6. Known contradictions this TZ opens and does not close

Map inv. 35 reads «stop is `dec.inv.price`». After this change the published stop on a
waiting row is the anchored decision's. **The map is Architect-owned and the Executor may
not edit it** (contract §2, §7 item 14), so the contradiction is recorded here and closed
by the map revision that follows this TZ — the route map inv. 50 names for exactly this
case. Record it under `## Pre-existing Issues`; do not act on it.
