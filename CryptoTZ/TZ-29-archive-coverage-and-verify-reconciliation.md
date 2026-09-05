# TZ-29 — Archive coverage, ticker aliases, and `--verify` reconciliation

**Canonical filename: `TZ-29-archive-coverage-and-verify-reconciliation.md`, filed under
`CryptoTZ/`.** Name the committed file from this line, never from the name it arrived
under (contract §3).

**Model: Opus.** A fetch path gaining a splice joint is a data-correctness change with a
silent failure mode — a wrong join fabricates a move the whole bench then measures — and
scope 2.4 is an arithmetic reconciliation, not an edit.

---

## 0. System Map fingerprint gate — blocking

Required revision: **`2026-09-05-a`**. Match every anchor below as an exact substring
against `SYSTEM-MAP-CRYPTOCALCUL.md` on `origin/main` after `git fetch --all --prune`.
Any mismatch, in either direction → **STOP, report BLOCKED**, stating found versus
required (contract §5).

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-05-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `62. **A workflow that runs only on demand is not a control over the files it reads.**` |

**The map is deliberately NOT revised ahead of this TZ, and the Boss's standing
instruction holds the baseline at `2026-09-05-a` until this TZ's results justify a new
one.** A rename-aware fetch path does not exist yet, and map §0 states that a map is not a
forecast of what `main` will hold. The invariant this work earns is written when the report
lands, against what was built. Discarded alternative: publish a revision carrying that
invariant first and gate on it — rejected because it makes the TZ unexecutable until a
second upload arrives and records a mechanism nobody has measured. §6 lists what the report
then owes the map; none of it is decided here.

Live files at this revision — measure each at the line count and MD5 stated, report any
difference under `## Pre-existing Issues` and **do not act on it**:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3736 | `dd39536d18cc1feb4839808e41e7bff4` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

`bench/backtest_bench.py` has no row in that table by design (map §0). Its figure at the
start of this TZ is **2768 lines, MD5 `9357c2bc4e71542c21068be79f8691f9`** (TZ-28's closing
measurement); record the actual value in `## Fingerprints` and report a difference rather
than acting on it.

---

## 1. Why — backtest run #14, 05.09.2026

The first archive dispatch of `--target` ran and produced no admissible reading.
`--target`, `--selftest` and `--lab-selftest` were green; **`--verify` was red on nine of
the ten fields that carry a threshold**, over 27 of the 30 coins. `vol_ratio`, the
eleventh column, carries no threshold and is therefore neither green nor red.

Three defects, all in this bench, none in production.

### D1 — the spot path is short by a constant block

Every spot series is missing the same absolute span regardless of its own length: 2.8 % of
25 664 h, 3.5 % of 20 520 h, 3.5 % of 20 300 h and 4.0 % of 17 760 h give **718.6, 718.2,
710.5 and 710.4 hours**, and because the percentages print to one decimal the single
constant consistent with all four at once lies in **708–719 h ≈ 29.5–30.0 days**. Every
`vision-perp` series carries 0.0–0.1 %. Reconciliation
splits on exactly that line and on nothing else:

| Group | Series | Missing | Coins reconciling on every field |
|---|---:|---:|---|
| `vision-perp` | 5 | 0.0–0.1 % | ARB and MORPHO clean; XMR, LIT, HYPE fail only fields the run's existing perp/spot basis note already covers (map §3.14) — **and three of those cells are not return-family**: `min_price` on XMR, `eff14` on XMR and HYPE |
| `vision` spot | 22 | 2.8–4.0 % | **zero** |

Per field, spot failures / perp failures: `min30` 21/0 · `r30` 20/1 · `r14` 18/3 ·
`max30` 17/0 · `eff14` 17/2 · `volatility` 15/0 · `max_price` 12/0 · `r7` 10/1 ·
`min_price` 5/1 · `vol7` 0/0.

**The design already calls for the repair.** Map §3.10 «Data» specifies monthly ZIPs with
the tail topped up from `data-api.binance.vision`, and `--probe` records that mirror
answering 200. It is the executing code that does not do it. HTTP 451 on the two
production hosts is inv. 24 and is not a finding.

**The percentage alone does not prove the block is contiguous or where it sits** — that
is arithmetic from an aggregate, not a reading, which is why 2.2 exists before 2.1 is
believed. Two consequences follow only from the census, not from this paragraph: whether
any interior gap survives the top-up, and whether the block sits at the tail.

### D2 — the archive is keyed by TICKER and production is not

`main.py` reads CoinGecko by **id**, and map inv. 10 requires the id to be kept across a
rebrand, so production survives a rename without noticing one. `data.binance.vision` is
keyed by the Binance pair, so the same rename silently truncates a series here and nowhere
else. That asymmetry is why this has never surfaced.

Run #14 shows the symptom twice: `GRAM` returned 1560 rows against 35 absent monthly files,
and `SKY` was skipped on a hole fraction the missing tail had inflated.

### D3 — `vol_ratio`'s printed deviation contradicts its own components

`vol_ratio` is `vol7 / volatility` (map §3.2 cap, §7). Both components are in the same
table, so the quotient's deviation is bounded by theirs. On **five of five zero-hole
series** the printed value exceeds that bound:

| Coin | `vol7` | `volatility` | Arithmetic bound | Printed |
|---|---:|---:|---:|---:|
| MORPHO | 0.87 % | 0.46 % | 1.34 % | 40.55 % |
| XMR | 2.27 % | 1.18 % | 3.49 % | 148.00 % |
| HYPE | 2.04 % | 1.95 % | 4.07 % | 42.65 % |
| LIT | 1.22 % | 1.59 % | 2.86 % | 8.75 % |
| ARB | 0.19 % | 0.79 % | 0.99 % | 2.58 % |

Ten of twenty-seven coins violate the bound, spot and perp alike — the violation is not
confined to clean series and no ranking among the ten is claimed. **The five zero-hole
symbols are the CONTROL, and that is the whole argument: on them coverage cannot be the
cause and all five violate anyway.** So the cause is inside `--verify`: either `vol_ratio` is not the quotient of the two fields printed beside it, or
its measure is not the one the header declares. Map §3.10 assigns a measure by field type —
levels `rel`, returns `pp`, `eff14` `abs` — and `vol_ratio` is dimensionless like `eff14`
and appears under none of the three.

This is why 2.4 reconciles before it thresholds. A threshold derived from `vol7` and
`volatility` would sit at roughly 39 % worst-case and would newly fail MORPHO and HYPE —
the two cleanest rows in the table — for a reason that has nothing to do with data.

### Two gaps that stop the run from attributing its own losses

**`--fetch` prints hours only for an accepted coin.** For `ONDO` (6.1 %) and `SKY` (8.8 %)
there is a percentage and no length, so the one number separating a short history from a
broken fetch is missing exactly where it decides the outcome. The skip threshold sits
between 4.0 % accepted and 6.1 % refused, and after 2.1 it will be applied to a different
quantity than the one it was set against (inv. 47). **Nothing in this TZ asserts that the
three absent coins were absent through the bench's fault** — that is the question 2.2 and
2.3 exist to answer, and it is answered in the report, not here.

**`--target` published a full report under a red `--verify`.** The two modes are
independent, so the only mode that checks whether the bench's numbers are production's
numbers does not reach the numbers it guards (inv. 53, inv. 62). `volatility` is not a
spectator column: through `INV_FLOOR_SD · vol · √24` it sets the stop, through
`reward/(vol·√H_NOISE)` the noise floor, through the same stop the `RR` that decides
admission, and it feeds `touchProb`. An error there does not perturb `Ω`; it selects a
different admitted sample. That is inv. 48 — the bench builds its own input, so the run
proves the function and not the wiring.

Until `--verify` is green nothing this bench measures may be cited as a market reading
(map §3.10a, §10, inv. 62).

---

## 2. Scope

Six independent scopes. If one blocks, complete the others and report that one blocked
(contract §6).

### 2.1 Tail top-up on the spot path

Bring the spot path to the behaviour the map already specifies: monthly ZIPs from
`data.binance.vision`, **tail topped up from `data-api.binance.vision`** to the last
complete hour. Diagnose why the perp path does this and the spot path does not, and repair
so that **one code path serves both** — two fetch paths differing in whether they top up is
the shape that produced this run (inv. 20).

`api.binance.com` and `fapi.binance.com` answer HTTP 451 from a runner and are not to be
called (contract §7 item 9, inv. 24).

### 2.2 Coverage census — on every line, accepted or skipped

`--fetch` prints, per attempted symbol: the ticker actually read, first timestamp, last
timestamp, hours present, **hours missing at the tail**, **interior gap count**, and the
**start and end of the largest interior gap**. A recorded state without its date is not a
state (inv. 56), and «дыр 2.8 %» names a quantity while hiding the only thing that explains
it.

Tail deficit and interior gaps are reported as separate numbers. That separation is the
whole point: it decides whether 2.1 was the entire defect, and it settles whether
production's own gap rule — returns only between adjacent buckets, gaps dropped (map §2) —
is being violated by the shape in which the archive reaches the coefficient block. **If
interior gaps survive the top-up, that is a finding for the report and not a repair in this
TZ.** Do not add a gap rule to the bench: production's cut code owns that rule (inv. 21,
inv. 38).

### 2.3 Ticker alias with a DERIVED splice test

A per-symbol alias with a cutover, in the fetch path, reading pre-rename history under the
old ticker and post-rename under the new. **Two CANDIDATES, not two facts:**
`GRAMUSDT` ← `TONUSDT`, `SKYUSDT` ← `MKRUSDT`.

They are candidates because an Architect session may not stand behind an external fact
(contract §7 item 9, inv. 44). Each is verified against the archive on the runner and the
outcome is reported; a candidate the data refuses is refused, and the report says so rather
than the TZ being right.

**Admissibility is arithmetic, never judgement, and the bar is derived from the run's own
data (inv. 49).** Compute the joint's own return across the splice and admit it only if
that return lies inside the distribution the combined series already exhibits — the
series' own realised hourly-return extremes, taken from the run, never a numeral written
into this TZ or into the code.

Expected under that rule, stated so the report can contradict it: `GRAM` is a pure rename
and splices; `SKY` is a token migration carrying a conversion ratio, so its joint carries a
fabricated multi-thousand-percent move and the rule refuses it. **A refused splice is not a
failure and does not stop the run** — the symbol enters by its post-rename leg alone, with
the refusal printed beside the joint return that caused it. **If that leg is then too short
to pass the skip rule, the coin is legitimately absent**, which is a different fact from
«the bench broke it» and is reported as the different fact.

**Never hand-write a conversion ratio into the data path** to rescue a refused splice: that
is the numeral inv. 49 refuses and it would put a production-shaped constant inside a
bench. If the derived rule admits `SKY` or refuses `GRAM`, report the numbers and do not
override it in either direction.

### 2.4 `vol_ratio` — reconcile the measure, then derive the threshold

**In this order. The second half is void without the first.**

First, establish what `--verify` compares for `vol_ratio` and under which measure, and make
the printed deviation consistent with the deviations of `vol7` and `volatility` on the same
coin. The five zero-hole coins are the control: on clean data the quotient's deviation must
lie inside the bound its components imply, and today it does not on any of the five.

Then, and only on a reconciled field, attach a threshold. **It is COMPUTED, never typed.**
`vol_ratio` is a quotient of two fields that already carry thresholds; read its construction
from the same block the bench already cuts by AST out of `get_token_betas` in `main.py`,
and propagate those two thresholds into the quotient's worst case. Report the derived
number and the propagation.

`vol_ratio` is not decorative: it feeds the leverage cap (`vol7/vol90 > 2 → 3X`, map §3.2)
and in the backtest the quality block runs on it alone (map §7). Adding a threshold to a
field that had none is creating a control, not relaxing one — contract §7 item 2 is not
engaged by 2.4, and **is** engaged by any temptation in 2.1–2.3 to move an existing
threshold to make a field green. Do not.

### 2.5 `--verify` states its failures with a sign and a class

- **Deviations carry their sign.** The table prints magnitudes, so a `volatility` too large
  and one too small are indistinguishable — and that direction is what says whether `RR`
  was understated or overstated. Print signed values; keep the threshold comparison on the
  magnitude.
- **Every failing field is classified**, and the class is printed with a comparison count
  (inv. 43), the mode still refusing to pass on zero comparisons (inv. 22):

| Class | Condition | Effect |
|---|---|---|
| `venue-basis` | the existing perp/spot basis calculation already flags this symbol-field cell | reference, per map §3.14 |
| `coverage` | the field's window overlaps a gap named by 2.2 | non-zero, gap named in the verdict |
| `unexplained` | neither | non-zero |

**`venue-basis` is READ from the calculation that already produces the `БАЗИС ПЕРП/СПОТ`
line, never from a field-family label written into this TZ or into the classifier.** The
distinction is not cosmetic and it is the reason this row was rewritten: run #14's basis
note covers `min_price` on XMR and `eff14` on XMR and HYPE, and neither field is
return-family. A hand-written family label would push those three cells into `unexplained`
and leave `--verify` red on two clean coins after a fully successful repair — a verdict
decided by a written enumeration rather than by data, which is the defect inv. 58 names and
which inv. 22 catches by requiring the classifier to count what it compared. **The set is
computed; if the computation and the note disagree, that is a finding for the report and
neither is edited to match the other.**

One threshold table currently reports three causes as one verdict, which is why a red
`--verify` needed a human to read it before anyone could act. The mode still **returns** its
exit code (inv. 29).

### 2.6 `--target` is gated on the reconciliation it depends on

A symbol whose reconciliation ends `coverage` or `unexplained` is excluded from every
`--target` arm and named, with its class, in the «ЧТО СРАВНИВАЛОСЬ» table (inv. 22,
inv. 37). If the surviving set falls below the registered quorum on a side or an arm,
`--target` prints no `Ω` and no `k*` for it and says which class removed the setups.

**No bar moves and no primary changes.** `Ω` is still read against `1/RR_MIN = 0.50` and
`k*` is still the smallest `k` whose CI95 covers it — those are the map's registered trigger
and they are not amended after seeing data (inv. 23). One line is added to the printed
output, stating the arithmetic the reader needs to interpret the verdict: admission
requires `RR ≥ RR_MIN`, so `1/RR ≤ 0.50` on every admitted setup, and on a driftless walk
the untruncated first-touch odds equal `1/RR` (inv. 32), so `Ω` approaches the bar only
where `RR` sits at the admission boundary. Print the arm's mean `1/RR` beside `Ω`; run #14
already computes it (0.213 long, 0.291 short on the production arm).

---

## 3. Files

**Modify:** `bench/backtest_bench.py` (2.1, 2.2, 2.3, 2.5, 2.6) · `bench/verify_bench.py`
(2.4, 2.5). **Create:** none. **Delete:** none.

Nothing else is authorised (contract §6). `.github/workflows/backtest_bench.yml` is not
opened (contract §7 item 8); it is dispatched, not edited. `bench.yml` is not opened.

---

## 4. Hard floor — §7 items engaged, quoted from the repository

Items 4, 5, 6, 7, 8, 10, 11, 13 and 14: **не затронуто.** No production file, workflow,
contract or registry is opened; no JS string is written; no venue flag is read as an
observation; and item 8 — «**Never modify `.github/workflows/backtest_bench.yml`** unless
the TZ names it» — holds because that workflow is dispatched here and never edited. Item 1 — «**No change to scoring, leverage, liquidation or geometry math**
unless the TZ explicitly cites a completed backtest (map §3.10b)» — is **not engaged**: no
function it names is edited, and the bench cuts production math at run time rather than
copying it (inv. 21). The four below are engaged and none is lifted.

**Item 2 —** «**Never edit a bench to make it pass.** A red bench is either a product defect
or a stale expectation; both are findings, neither is a licence to change the assertion.»
The nine red `--verify` fields go green because the DATA is repaired, never because a
threshold moved. No existing threshold in `bench/verify_bench.py` changes value; 2.4 adds
one where none existed, after reconciling the field it measures.

**Item 3 —** «**Universe membership changes only on an OWNER decision quoted in the TZ.**
`TOKENS` (bot) and `tokens[]` (frontend) are never edited on an Executor's judgement, on a
backtest result, or on a TZ that does not quote the owner's own words authorising the
change.» **No owner decision is quoted and none is needed:** neither file is opened and
membership does not move. `GRAM`, `ONDO` and `SKY` concern the bench's COVERAGE, which is a
fetch outcome. The universe stands at 30 throughout, and the alias table lives in the bench
and nowhere else.

**Item 9 —** «**Binance production hosts return HTTP 451 from GitHub Actions** (inv. 24).
Only `data.binance.vision` and `data-api.binance.vision` work from a runner; new CI code
calling `api.binance.com` will fail — report instead of retrying. **A session fetch may not
stand behind a product fact** (inv. 44)». The top-up and the alias verification are workflow
steps, not session fetches. `--probe` measures the session's own environment, is permitted,
and its command is recorded beside its result.

**Item 12 —** «**Never remove, skip, comment out or `continue-on-error` a bench step to make
CI green** — editing the assertion (item 2) and deleting the assertion are the same act; a
step that cannot pass is a finding for the report. Equally, never add a bench file without
wiring it into `.github/workflows/bench.yml` in the same change: a bench outside the gate
never executes and is not a control (inv. 37).» No bench file is added and no step removed;
`bench.yml` is not opened and its figure must not move.

---

## 5. Validation

Every item runs. An item that cannot be run **fails**; it is never «not applicable»
(contract §9). Record the command and its output for each.

**Baseline, before any edit.** `--probe`, `--fetch`, `--verify` on the current tree, with
per-field comparison counts and the exit code. The diff is not provable without it.

1. `python3 -m py_compile bench/backtest_bench.py bench/verify_bench.py`.
2. `bench/verify_bench.py`'s own offline rule suite — exit code and check counts; a
   validator that passes on zero data is a failed validator (inv. 22).
3. **Census self-proof.** Delete a known 48-hour span from one cached symbol, re-run the
   census, and confirm it names that span as the largest interior gap and that 2.5
   reclassifies the affected fields as `coverage`. Restore; confirm the cache is clean.
4. **Alias identity control (inv. 45).** Run the alias path with every cutover set so that
   nothing splices, and confirm the cache is byte-identical to the baseline run. A
   comparator never proven on identity supports no claim about a real diff.
5. **Splice negative test (inv. 23).** Plant a fabricated ratio on an admitted splice and
   confirm the derived rule refuses it and says why. A rule never shown to refuse is not a
   rule.
6. **`vol_ratio` coherence check.** On the five zero-hole symbols, assert that the printed
   `vol_ratio` deviation lies inside the bound implied by the printed `vol7` and
   `volatility` deviations for the same symbol. Report the bound and the value per symbol.
   This is the acceptance test for 2.4's first half and it currently fails on 5 of 5.
7. `--probe` — five hosts, status codes recorded beside the command. `451` on the two
   production hosts is the expected reading, not a failure.
8. `--fetch` — **31 of 31 attempted, the full census printed on every line**, accepted or
   skipped. Report tail deficit and interior gaps separately per coin; the top-up has
   landed when no accepted coin carries a tail deficit above **0.1 %**. State `GRAM`'s hours
   before and after the alias, and `ONDO`'s and `SKY`'s lengths, which have never been
   printed. **State whether the existing skip threshold still separates the same coins once
   the tail deficit is removed** — report the reading, do not move the threshold (item 2,
   inv. 47).
9. `--verify` — per-field comparison counts, the class breakdown from 2.5, and the coin
   count reached; 30 is the target and anything less is named with its reason. **Green on
   all ten thresholded fields plus the newly thresholded `vol_ratio` is the goal; if
   `unexplained` survives on any symbol, that is the result and the mode stays red.** Do not
   adjust a threshold to clear it.
   **Class known-answer control (inv. 23, inv. 45).** Print the symbol-field set the
   classifier assigned to `venue-basis` and assert it reproduces run #14's basis note
   exactly on the five `fut:true` symbols — `HYPE: r14, eff14 · LIT: r14, r30 · XMR:
   min_price, r7, r14, eff14`. A classifier never shown to reproduce a reading that already
   exists supports no claim about a new one. If it does not reproduce it, report both sets
   and change neither.
10. **`--verify` negative test (inv. 29).** Plant a deviation past the threshold in one
    level field, one return field and `vol_ratio`, and confirm the mode **returns** non-zero
    in each case. Printing a failure is not returning one. Revert; confirm the tree is
    clean.
11. `--selftest` and `--lab-selftest` — unchanged and green, all three worlds and all six
    section-D controls, with the negative control still working: inverting `_touch_calc`'s
    long/short branch turns D1, D2, D3 and D6 red and leaves D4 and D5 green. Report the
    counts, not «passed». Any movement here is a regression and is reported as one.
12. `--target` on the repaired archive → **run #15.** Attach `target.txt` and
    `target_raw.json`, plus the excluded-symbol table from 2.6 and the mean `1/RR` line.
    **Report the numbers and draw no conclusion from them** — reading `Ω` against
    `1/RR_MIN = 0.50` is the Architect's (contract §6, inv. 62).
13. **No-regression on the gate.** `bench.yml` is not opened; replay the thirteen steps
    locally and confirm **1 255 401, delta zero**. `_assert_js_closed` counts non-zero for
    every bundle built.
14. Extremes, stated so they are attempted rather than discovered: a symbol with no
    pre-rename leg · a cutover outside the archive's span on both sides · a coin whose
    monthly ZIP for the current month does not exist yet · a top-up returning zero rows ·
    `data-api.binance.vision` answering non-200 mid-fetch · an arm with zero stop touches
    (`target_raw.json` emits bare `NaN` there — do not repair it here, confirm the run does
    not crash) · a cache where every spot symbol is excluded by 2.6, which must print «no
    `Ω`» rather than an average over what survived. Each must fail loudly and name the
    symbol, never silently shorten a series.

---

## 6. Out of scope — report, do not implement

`bench.yml` does not build a bundle, so `_assert_js_closed` never fires in the gate
(map §10, inv. 62's residual) · `.gitignore`'s comment is one bridge name short ·
`prot_bench.js:177` carries a raw Cyrillic literal · `target_raw.json` can emit bare `NaN`
· map §3.14 Consequence 3 records a reconciliation on 25 spot coins that run #14
contradicts, and its prediction for MORPHO and ARB is falsified.

**The map is the Architect's and moves after this report, not before it.** Recorded here so
nothing is lost, as open questions and never as answers: what §3.10a's `--target` row should
say now that the archive dispatch has been taken · whether §3.16's «`GRAM` has no
three-year archive» is a property of the coin or of the fetch · what §3.14 Consequence 3
becomes once MORPHO and ARB are measured rather than predicted · whether §10's
Continuation-target row needs `--verify` green as a stated precondition. **The invariant
this work earns EXTENDS inv. 10** — «Rebranding a coin: change the display name and the
Binance pair; **KEEP the CoinGecko id**» — which already governs a rename on the production
side; what it does not carry is that changing the Binance pair splits a ticker-keyed
archive. A separate invariant restating the rename rule would be a second place for one
fact (inv. 20).

Anything else noticed goes under `## Pre-existing Issues` or `## Remaining Risks`
(contract §6).

---

## 7. Definition of done

`## Status COMPLETED` requires: the census printed on every `--fetch` line with tail and
interior gaps separated · `--fetch` at 31 of 31 · the splice rule shown to admit and to
refuse · `vol_ratio` coherent on the five zero-hole symbols and carrying a derived
threshold · `--verify` classified, signed, reproducing run #14's basis set on the five
`fut:true` symbols, and returning non-zero on planted failures ·
`--target` gated on it · `--selftest` and `--lab-selftest` unmoved · gate delta zero · run
#15's artifacts attached.

**`PARTIAL` is the correct status if the WORK is incomplete, not if a hosted CI result was
unreadable** (contract §9) — say which workflows executed and where, and never forecast one.
