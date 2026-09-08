# TZ-34 — the venue actually fetched is an OBSERVATION, recorded and read

**Canonical filename: `TZ-34-fetched-venue-observed.md`.** The Executor names the committed
file from this line and never from the name it received.

**Model: Opus.** One file, but the change moves a classifier whose output decides an exit
code and a measurement population; a wrong edit silently widens or narrows the set of coins
every later run measures.

**Touches:** `bench/backtest_bench.py`, `bench/backtest_guard_bench.py`.
**Touches nothing else.** No production file, no workflow, no contract, no map.

---

## 0. Required System Map fingerprint

The Executor matches every anchor below as an exact substring against
`SYSTEM-MAP-CRYPTOCALCUL.md` in the repository BEFORE any work. Any mismatch → ЗАБЛОКИРОВАНО.

`bench/backtest_bench.py` has no row in the map's file table (§0 states why). At this
specification it is **3724 lines, MD5 `84b1572fd3af207b1e658f44f0191fcf`**, and that figure
is stated here rather than in the map, exactly as TZ-28, TZ-29 and TZ-30 stated theirs.

````text
## 0. Fingerprint

**Revision 2026-09-08-a.** Baseline: TZ-33 on `index.html` — `directionVerdict` computes
the trade's levels at the ANCHOR, the price the card publishes as its entry — report
`CryptoReports/TZ-33-entry-anchor-geometry-report.md`, accepted and merged.
**The file table's hashes are the pin; the commit is provenance and is not restated
here.** This revision was authored from delivered files rather than from a checkout, and
a commit hash copied out of a report is the report's word rather than a reading
(inv. 55). Content is what this block pins and MD5 pins it either way.

**What moves here is production's own PUBLICATION PRICE, and two instruments did not move
with it.** `tradeGeometry` and `leverageDecision` now run a SECOND time at the anchor and
the veto is read off that pass alone; `directionVerdict` takes `btcStats` for it; `planLine`
prints the anchored stop (§3.12). No threshold and no production constant moves. Inv. 35 was
disproven by the change and is rewritten in place; inv. 66 is new. **The journal still
records the decision taken at `cur` beside a card that prints the decision taken at the
anchor, and `--target`'s production arm is admitted at the anchor and resolved at `cur`** —
one cause, two sites, reserved as TZ-35 (§3.13, §3.10, §10).

**The reconciliation is no longer 30 of 30.** UNI, XLM and ZEC now class `unexplained`, and
that class removes a SYMBOL from `--target`'s arms rather than removing the run, so every
mode behind that gate now measures 27 coins (§7, §3.14, §10). Nothing measured on run #16
moves: that run was taken while the reconciliation was clean, and a sample is described by
the universe it was taken on (§3.10b).

**Contract v20 lands in the same revision and is not a TZ.** `EXECUTOR-INSTRUCTIONS.md` §2
gained the three `analyst/**` paths its class table never carried — `analyst/owner.json`,
`analyst/live-gate.sh`, `analyst/README.md` — a defect TZ-30 reported and correctly did not
act on, because the file is Architect-owned (contract §7.14). **v20** is 814
lines, MD5 `9a257890e9db663eb0fc74129f4841e0`.

**`bench/backtest_bench.py` has no row in the file table, and four consecutive TZs have now
had to explain the absence.** The table pins the four files a TZ header fingerprints:
three production artifacts plus the calibration record, and the record is there only
because it is one of exactly two places `DAY_RANGE_ABNORMAL = 1.39` exists (inv. 46).
A bench in that table would put a hash in every TZ header for a file that moves whenever a
bench moves — the argument §11 already makes for `live-gate.sh`. A TZ needing the figure
states it in its own `§0`, as TZ-28, TZ-29 and TZ-30 all did (2544 → 2768 → 3216 → **3240
lines**, `fb9464afba2e87450bd3fd11877da9f1` → `9357c2bc4e71542c21068be79f8691f9` →
`1b921e88fdae5c1c404fbf9fbcee8b2c` → `d2dad0f80afa2c191c2faf1d40081a88`), and TZ-33 moved
it again — **3724 lines**, `84b1572fd3af207b1e658f44f0191fcf`.

**`bench/backtest_guard_bench.py` gets no row either, and for the stronger reason:
its control is being a gate step.** It executes on every push at step 14, so a hash in a TZ
header would pin a file whose behaviour is already under a control that runs — exactly the
argument §11 makes for `live-gate.sh` at step 13. A fingerprint entry buys a second, weaker
check and costs one line in every future TZ header.

**Two of the last three TZs were delivered PARTIAL and both were right to be (hard floor
item 2).** TZ-27 left `--lab-selftest` red on D2 and D3 rather than editing an assertion to
make it pass, and TZ-28 re-registered both bars through a specification (inv. 61). TZ-29
left three validation items with NO reading rather than manufacturing one, because the
top-up, the alias verdict and the archive run all live on a runner. In both cases the red
was a property of the world, the report said so, and the next step was a specification or a
dispatch — never a softer bar. **The measurement TZ-27 could not take has now been taken:**
run #16 read `Ω` on the archive for both sides at every grid point, and the finding is that
no `k*` exists (§3.10a, §3.12, §10).

**The two revisions before this one, in one line each.** `2026-09-06-a` carried no
specification either: it recorded the hosted runner reading of the fourteenth gate step and
the inv. 53 proof the map had listed as owed; `2026-09-05-c` recorded TZ-30 and contract v20
— that step and the three `analyst/**` classes — on a local replay. Contract **v20** (814
lines, MD5 `9a257890e9db663eb0fc74129f4841e0`) is unchanged here.

Every TZ header quotes this block IN FULL — all seven anchors and the file table,
never a subset. The Executor matches each anchor as an exact substring against the
repository copy before any work (contract §5); any mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-08-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `66. **A published level and the price it was computed at are one fact.**` |

Live files at this revision — the set every TZ header and every report fingerprints:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

The calibration record is fingerprinted, unlike every other bench artifact, because
it is one of exactly two places `DAY_RANGE_ABNORMAL = 1.39` exists and gate step 12
compares the two on every push (inv. 46).

**That record describes the universe of its OWN run and is never edited to match a later
one.** Its header reads «25 spot of 28 declared tokens … HYPE, XMR, LIT», which was true
of the run that produced it and is the sentence TZ-25 §4.4 and TZ-26 §2.3 both refused to
touch. Nothing calibrated in it moved when the universe reached 30: both added coins are
`fut:true`, the measure never counted them, and the spot basis is still 25 (§3.16).
Rewriting the header would make the description of one sample describe a different one,
which is inv. 46 read backwards — the constant would then agree with a record that no
longer names the run behind it. It goes stale by design; the reader is told so here.

**The gate was NOT re-read at this revision, so the totals here are a recorded state and not
a current one (inv. 56).** Last measured 06.09.2026: `bench.yml`, **14 steps, 1 255 495
checks** — steps 1–13 at 1 255 401 and step 14 at 94 — with the hosted `Bench gate` green on
`main`, `#134` on branch commit `7fdd7db` and `#135` on merge commit `ea259c6`, read off the
run page rather than from a report (§10). This revision was authored from delivered files and
no runner reading arrived with them.

**Step 7 carries a DERIVABLE prediction and it is the first figure to read after TZ-33.**
`journal_bench.js` counts numeric leaves of the records it writes; `vd.geo` is now the
ANCHORED geometry and its `wait` is null on every waiting row by the termination property
(§3.12). If `journal/write.js` stores that object whole — which §3.13 says it does — the
counter FALLS by one leaf per waiting row, and a fall is attributed rather than assumed
benign, because a defect that nulls a field lowers it identically.

**What the fourteenth step changes is the class of decay the gate can see.** Until it landed,
the only thread from `backtest_bench.py` into these gates was step 4 — `verify_bench.py`
imports the module at scope, which proves it IMPORTS and not that a bundle builds, and that
was inv. 62's residual. **The gate now BUILDS all four bundles** on every push, runs
`node --check` on what it writes and asserts closure under reference, so a production TZ that
splits a cut function out of `index.html` is caught by the workflow that already runs rather
than by the manual one nobody dispatched. It catches a stale CUT and not a stale RESULT
(inv. 62).

The **+4 662** attribution below is `-a`'s, re-stated rather than re-measured: the whole
delta against 1 250 739 is TZ-25's and TZ-26 moved no counter at all. **Step 14 has no row
in it and never will:** a new step has no «was», so its whole count is its attribution, and
the number to compare against arrives the first time something moves it.

| Step | Bench | Was | Now | Δ | Attribution |
|---:|---|---:|---:|---:|---|
| 7 | `journal_bench.js` | 691 109 | 693 895 | **+2 786** | +2 720 declared-skip records — `x` rows 884 → 1 428, five checks each · +64 verdict content, below · +2 the declared-venue note, one assertion per `fut:true` asset, 3 → 5 |
| 8 | `catalyst_bench.js` | 23 062 | 24 692 | **+1 630** | +1 600 authority table, 400 days × 2 new symbols × 2 sides · +2 silent-symbol sweep 26 → 28 · +28 degraded load, 7 `BAD` cases × 2 symbols × 2 |
| 10 | `render_bench.py` | 15 925 | 16 171 | **+246** | 2 added cards × 123 scenarios, one increment per shown, scored, on-side row — which also proves both coins are scored and rendered rather than dropped |

**TZ-25 predicted step 8 at +4 and was wrong by two orders of magnitude**, because it
reused TZ-21's per-symbol term, measured for a symbol that also gained a registry entry.
A symbol entering `tokens[]` alone drives three sweeps that scale with the symbol list.
The published figure is the measurement and never the prediction (inv. 43), and the
prediction is recorded here so a future TZ cites the attribution instead of it.

**Steps 12 and 13 held at 220 598 and 40 across both TZs**, which is what a «must not
move» clause is for: the day-range measure and the live-data gate see the same 25 spot
assets they saw at 28. TZ-26 replaced three expected values and one on-screen string and
moved nothing, because a check count counts comparisons — a section can turn red or green
without its counter changing (inv. 43). Step 13's counter is assertions and not cases —
three per failing case (exit code · empty stdout · exactly one stderr line) and two per
passing case, so 12 × 3 + 2 × 2 = 40 — and step 12's `caption` section reads 64 on both
sides of TZ-26. Older attributions in full: TZ-21 moved step 8 by +22 and TZ-15 moved
step 12 by +64; both are in their own reports, and the rule that produced them is the
one above.

**Step 7 (`journal_bench.js`) moves with verdict CONTENT, not only with control
volume.** It counts numeric leaves of the records it writes, and a verdict that
returns before geometry writes no `geo` object, so a change in verdicts moves it
without moving a single control. A fall in step 7 is attributed, never assumed
benign, because a defect that nulls a field lowers it identically. Held at
**691 109** through TZ-13, TZ-14 and TZ-15, and moved by TZ-25 for exactly the reason
this paragraph names: the fixture generator draws every row from ONE seeded RNG and makes
two passes over the token list, so appending two tokens shifts the stream the second pass
reads, and 2 349 pre-existing snapshot rows changed cost **in both directions** for a net
**+64**. What separates that from a defect is the row-kind census, not the sign — snapshot
rows unmoved at 6 743, skip rows 884 → 1 428, every other kind unmoved — plus a separate
proof that the product's own output for pre-existing coins is byte-identical.
````

---

## 1. The defect, derived from the source and not from a report

Three coins — **UNI, XLM, ZEC** — now class `unexplained` in the reconciliation, so
`--target`, `--regime-gate` and every mode behind the same gate measure 27 coins instead of
30 (map §7, §10). `unexplained` is «everything else» by construction: it names no cause.

**The source carries a mechanism that produces exactly this outcome, and it is a blind spot
rather than an arithmetic error.** Three sites, in the order they fire:

1. **The fetch loop tries two venues and keeps the longer series.**
   `for is_fut in ((True,) if fut else (False, True)):` — a coin NOT declared `fut:true`
   attempts spot, then futures, and `best` keeps whichever returned more rows. A non-declared
   coin can therefore be cached on the PERPETUAL, legitimately and by design.
2. **The label records the DECLARATION, not the leg that won.**
   `_save(sym, P, V, source + ("-perp" if fut else ""), HL, cov)` derives `src` from `fut` —
   a fact the loop already knew before it fetched anything. `is_fut`, the only variable that
   knows which venue actually answered, is out of scope by then and is written nowhere.
   **The venue actually fetched is not recorded in the cache document at all.**
3. **The reconciliation grants its basis licence off the declaration.**
   `if sym in fut:` → `cls = "venue-basis"`, else `coverage` or `unexplained`. So a coin
   silently cached on the perpetual has its perp-versus-CoinGecko-spot-index basis measured,
   found over threshold, and classed `unexplained` — because the classifier asks a question
   («was this asset declared a perpetual?») that is not the question in front of it («is this
   SERIES a perpetual?»).

`unexplained` is in `HARD_CLASSES`, so it returns a non-zero code and removes the symbol from
`--target`'s arms. **One unrecorded observation costs three coins of every measurement.**

**This is inv. 41 read in its mirror.** That invariant says the declared venue is read BEFORE
the degradation ladder, because `fut:true` is a declaration and a host's answer may not revoke
it. It is about an ASSET in production. The classifier is asking about an ARTIFACT on disk,
where the only truthful answer is what the fetcher observed — and there the declaration is the
thing that must not be trusted, because the fetcher is free to disagree with it and does.

**Whether this is what happened to UNI, XLM and ZEC is NOT asserted here and is not
assertable in a session (inv. 44).** It is a mechanism that exists in the code. The reading
that settles it is a runner artifact and is assigned in §6, never validated in §5.

---

## 2. What must change

**2.1 The census records the venue it observed.**
`cov` gains one key, `venue`, written from the leg that actually won the `best` comparison:
`"perp"` where that leg is the futures one, `"spot"` where it is the spot one. It is
additive, exactly as `hl` and `cov` themselves were (inv. 1, 9), and it is derived from
`is_fut` at the site that has it — never re-derived downstream from `src`, from `ticker` or
from the declaration.

**2.2 A cache document that does not carry `venue` never reaches the classifier as spot.**
`census_of_doc` rebuilds a census from `prices` and cannot recover a venue from them, so a
document written before this change carries no answer. The run must refetch it or refuse it;
it may not be read as `"spot"` by default. **The mechanism is the Executor's call** — a cache
key bump and a refetch trigger are both safe — **but the property is not: no code path may
produce a `venue` value that was not observed.** A default in the reading direction reproduces
this exact defect one layer down, where nothing at all would report it.

**2.3 The reconciliation reads the observation.**
The `venue-basis` licence is granted where the SERIES is a perpetual, i.e. from
`cov["venue"] == "perp"`, and not from `sym in fut`. The three classes, their names,
`HARD_CLASSES`, the thresholds in `SPEC`, the measure chosen by field type, the sign
convention and `target_gate` are all untouched: this changes WHICH cells qualify for an
existing licence and nothing about what the licence is.

**2.4 The census line prints it.**
`print_census` gains the venue in its existing line. A field recorded and never printed is a
field the next reader has to know exists, and the census is the surface on which a
fall-through becomes visible without a diff.

**2.5 The garrison gains a section.**
`bench/backtest_guard_bench.py` is gate step 14 and already asserts `_vision_rows` offline and
what `target_gate` does with a class. It gains the checks in §5.2 so this coupling is asserted
where something already runs (inv. 62), rather than only under a dispatch nobody may perform.

---

## 3. What must NOT change — negative assertions

Each line below is a string or a behaviour that must be checked FOR ITS ABSENCE, or for its
survival unchanged, before the report is written. A hit blocks delivery.

1. **`fut:true` remains a DECLARATION and production never observes a venue.** `index.html`
   and `main.py` are byte-identical after this TZ. Inv. 41 is neither weakened nor touched:
   this specification changes what a BENCH records about a FILE IT DOWNLOADED, which is a
   different question from the venue of an asset. A change that makes production read a
   host's answer is the failure inv. 41 exists to name.
2. **The fetch ORDER does not move.** Spot is still attempted first for a non-declared coin
   and `best` still keeps the longer series. Perpetuals-as-default is a real question and is
   deliberately not in this TZ — §7 states why.
3. **No threshold, no class name and no constant moves.** `HARD_CLASSES`, `CLASSES`, `SPEC`,
   the 2600-hour and 5 % skip rules, `TGT_QUORUM_*`, `K_GRID` and every figure in them are
   the numbers they were.
4. **`src` keeps its current value and gains no new meaning.** It is not repurposed as the
   venue record and it is not deleted; a second field carrying one fact is inv. 20's failure,
   and the repair is that `venue` is the authority and `src` is a label nobody classifies on.
5. **No bench is edited to make it pass.** If the new section is red on real data, that is a
   product fact and the report says so (hard floor item 2).
6. **No copied production math** (inv. 21, 38) and no new network call: every check in §5 is
   offline against synthetic input.

---

## 4. Text quoted from the repository, so the Executor compares rather than recalls (inv. 55)

Read from `bench/backtest_bench.py` at this specification:

```
HARD_CLASSES = ("coverage", "unexplained")

for is_fut in ((True,) if fut else (False, True)):

good, verdict = _save(sym, P, V, source + ("-perp" if fut else ""), HL, cov)

            if over:
                if sym in fut:
                    # ALL fields: two different real instruments (map §3.14).
                    basis.append((sym, k, dv))
                    cls = "venue-basis"
                else:
                    why = _cov_hit(cov, windows.get(k, 90.0), t_last)
                    cls = "coverage" if why else "unexplained"
```

Read from the System Map, §3.14, inv. 41 — the clause this TZ must not contradict:

> **The declared venue is read BEFORE the degradation ladder.** `fut:true` is a DECLARATION
> (§3.14), not an observation, so a skip on such an asset is DECLARED coverage in any form it
> takes and never raises `hardSkip`.

Read from the System Map, §3.10 — the sentence this TZ makes false and which the Architect
repairs in the revision that accepts it, never the Executor (inv. 50):

> the five coins carrying every one of those cells are exactly the five `fut:true` assets

---

## 5. Validation — written by the Architect, run by the Executor

Every item names the artifact it reads and the command that produces it. An item that cannot
be taken in a session is not here; it is in §6.

**5.1 Compile and no-regression.**
- `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` — clean.
- `git diff --name-only` names exactly the two bench files.
- `md5sum index.html main.py` — both unchanged against `origin/main`, quoted in the report.
- `--selftest` and `--lab-selftest` are NOT run here: they need an archive and a runner
  (inv. 44). Their standing is unchanged and the report says so rather than implying a run.

**5.2 The new garrison section — offline, synthetic, counted (inv. 22, 43).**
Every assertion calls a production-side function by name and compares its return; no rule is
re-implemented in the check (inv. 21).

1. **The label follows the winning leg, both directions.** Two synthetic fetch outcomes where
   the futures leg is longer and where the spot leg is longer; `cov["venue"]` reads `"perp"`
   and `"spot"` respectively. The fixture varies ONLY the row counts.
2. **The declaration does not decide it.** The same two fixtures run once with the symbol
   declared `fut:true` and once without: `venue` is unchanged by the declaration in all four
   cells. This is the check that the two facts have actually been separated.
3. **The licence follows the observation.** A deviation over threshold on a symbol NOT in
   `fut` classes `venue-basis` when `cov["venue"] == "perp"` and `unexplained` when it is
   `"spot"`. Both cells are asserted; asserting only the first cannot fail.
4. **A document without `venue` never classifies as spot.** A `cov` with the key absent must
   raise, refuse or trigger a refetch — asserted as «not classified as spot», so any of the
   three safe mechanisms passes and the unsafe default fails.
5. **Negative control (inv. 23, 45, 65).** Restore `sym in fut` as the licence test in a copy
   and re-run section 5.2: items 3 and 4 must go RED. The bar here is derived from the
   fixture's `venue`, a different authority from the declaration under test, which is exactly
   what inv. 65 requires — a section that read its expectation from the thing it judges would
   stay green under the inversion.
6. **Counted, and zero fails.** The section reports its own count at the comparison site and
   refuses to pass on zero comparisons.

**5.3 Gate replay.**
`bench.yml` steps 1–14 run locally against the unmodified checkout before any edit and again
after. Steps 1–13 must read **delta zero** — a comparison of two measurements, never of a
measurement against a document. Step 14 moves and its delta is attributed term by term.
**No expected total is named here and none may be predicted (inv. 43):** the figure is
published as measured.

**5.4 Report.**
Line counts and MD5 for the System Map and for every file the map's `## 0` table currently
lists, the set read from that table at authoring time. The report states no outcome of its own
commit or push (inv. 54).

---

## 6. Assigned to a runner, and NOT a validation item of this TZ

The reading that says whether UNI, XLM and ZEC were on the perpetual is
`backtest_bench.yml`, dispatched, `--fetch` then `--verify`, and the artifact is the census
block plus the reconciliation's class table. A session may not fetch it (inv. 44). The
Executor does not perform it, does not predict its outcome and does not report it as pending
work of its own; the dispatch is the Boss's and the verdict on what it shows is the
Architect's.

**Both outcomes are informative and neither is a defect of this TZ.** If the three coins read
`venue: "perp"`, the class was wrong and the arms return to 30. If they read `"spot"`, this
mechanism is refuted for them, the blind spot is closed anyway, and the cause is somewhere
else — which is a smaller question than the one that exists today, because one candidate has
been eliminated by measurement rather than by argument.

---

## 7. Out of scope, deliberately — perpetuals as the default source

`[решение принято мной]` The bench measures 26 of 31 series on Binance SPOT while the Boss
trades perpetuals, and every first-touch resolution in `--target` and `--stops` reads `hi`/`lo`
from that spot series. Switching the default is a real question and it is **not** this TZ.

**Reason: the census must exist before the switch can be measured.** Making perpetuals the
default today changes the venue of ~26 series while nothing records which venue any series is
on, so the next run would differ from run #16 in two ways at once and no finding would be
attributable to either. It would also invert the reconciliation's meaning — every coin would
become a basis cell against CoinGecko's spot index — and that has to be designed rather than
discovered. **Discarded alternative:** doing both in one TZ, which buys one Executor session
and spends the ability to attribute the result.

The switch becomes its own TZ once this census has been read once.
