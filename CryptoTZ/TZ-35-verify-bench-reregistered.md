# TZ-35 — `verify_bench.py` re-registered against the observation

**Canonical filename: `TZ-35-verify-bench-reregistered.md`.** The Executor names the
committed file from this line and never from the name it received.

**Model: Opus.** One file, but it is the bench that turns `--verify` green, and the failure
direction is a bench that passes. A fixture built carelessly re-greens the gate while
asserting nothing, which is worse than the red it replaces.

**Touches:** `bench/verify_bench.py`. **Nothing else** — see §3.1, which is the whole point
of this specification.

**Branch: `claude/tz-34-fetched-venue-observed`, continued.** This TZ does NOT open a branch
of its own. TZ-34's implementation is correct and accepted, and it is unmerged only because
it leaves gate step 4 red; the branch is the unit of deployment and it merges once, green,
carrying both commits under the single pull request already compared at
`main...claude/tz-34-fetched-venue-observed`.

---

## 0. Required System Map fingerprint

Matched as exact substrings against `SYSTEM-MAP-CRYPTOCALCUL.md` in the repository BEFORE any
work. Any mismatch → ЗАБЛОКИРОВАНО. The map is unchanged by TZ-34, which touched benches only.

**Branch head, additionally, and each is a GATE rather than a note.** These figures come from
the TZ-34 report and not from a reading of the repository, so they are stated here to be
checked: a mismatch means the branch is not where that report left it, and the correct action
is to BLOCK and say which figure moved.

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 3881 | `45e2294c5fc82f96a7e66b84c2a094c2` |
| `bench/backtest_guard_bench.py` | 971 | `19427e79133d48870d76eb0c908c69f6` |

**`bench/verify_bench.py` is pinned by ANCHORS and carries no hash here**, because it reached
the Architect as text rather than as bytes and a hash that was not computed must not be
published as though it were (the map's `## 0` makes the same distinction between a pin and a
provenance note). Each anchor below must be present, and the count must be exact:

| Anchor | Occurrences |
|---|---:|
| `json.dump({'prices': px, 'volumes': vol, 'src': 'synthetic'},` | 1 |
| `out.strip().splitlines()[-1][:150]` | 5 |
| `ok('fut basis: return gap exits 0 with html', code == 0, 'exit=%s' % code)` | 1 |
| `ok('single outlier exits non-zero and is classified unexplained',` | 1 |
| `def basis_sets(text):` | 1 |
| `print('checks run: %d   FAIL %d' % (checks[0], len(fails)))` | 1 |

The bench reports **35 checks** at this specification, counted at its `ok(` call sites.

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

## 1. Why this exists — a defect in TZ-34's specification, not in its implementation

TZ-34 moved the `venue-basis` licence from the declaration to the observation. `verify_bench.py`
asserts that licence end-to-end and its fixtures predate the key TZ-34 introduced, so the change
made this bench red the moment it was correct. **TZ-34's `Touches` list did not name it, and
that omission is the Architect's**: a specification that changes a classifier must enumerate
every bench that asserts that classifier, and TZ-34's negative assertions covered the STRINGS
the change makes false while saying nothing about the ASSERTIONS it makes false. The Executor
found it by measurement, refused to edit an out-of-scope bench under hard floor item 2, and was
right on both counts.

Two independent causes, both established by running the bench rather than by reading it, and
both reproduced here from the file itself:

1. **The fixtures carry no census at all.** `make_cache` writes
   `{'prices', 'volumes', 'src': 'synthetic'}` — no `cov`, therefore no `venue`. Under TZ-34
   §2.2 the reconciliation must refuse such a document, and it does.
2. **Case 10 asserts the rule TZ-34 replaced.** It writes an HTML naming `AAA` as `fut:true`
   and requires a large gap on `AAA` to be labelled basis and exit 0. The licence no longer
   follows the declaration and `AAA`'s series is spot, so it classes `unexplained`. **Exactly
   three of case 10's four checks depend on the declaration granting the licence**; the fourth,
   «systemic breach (all coins) still fails after v3», does not and must stay green throughout.

This is a stale expectation in the exact sense of hard floor item 2. The repair is
re-registration — the assertions are rewritten to say what the system now does, and they are
rewritten so that they would FAIL if it stopped doing it.

---

## 2. What must change

### 2.1 The fixtures carry an OBSERVED census

`make_cache` writes a `cov` into every document it creates, and the census is **built by
calling `bb.census_of_doc` on the document it just built** — never assembled as a literal. A
hand-written census is a second implementation of a production function (inv. 21, 38) and it
will drift from the real one silently.

- `t_ref` is the fixture's own last bar, so `tail` is 0 and `gaps` is empty. This matters:
  `_cov_hit` reads those two fields, and a fixture that accidentally reports a tail deficit
  would reclassify case 9's cell from `unexplained` to `coverage` and pass for the wrong reason.
- The venue is a per-symbol argument of `make_cache`, defaulting to spot. A fixture DECLARING
  the world it tests is not the defaulting TZ-34 §2.2 forbids: that prohibition is on
  PRODUCTION code inventing an observation it did not make.
- **The venue values are read from production's own names** — `bb.VENUE_PERP`, `bb.VENUE_SPOT`
  or whatever `backtest_bench.py` calls them at the branch head — and never written as string
  literals in this bench (inv. 65). A constant copied here is a constant that stops moving with
  the thing it judges.

### 2.2 Case 10 becomes three lanes, because the licence now has two inputs and only one of
them decides

The lane that exists today tests one cell of a two-by-two. All three lanes below use the same
over-threshold mutation and differ only in the two inputs:

| Lane | Declared `fut:true` | Series venue | Required class | Required exit |
|---|---|---|---|---:|
| A | yes | perp | `venue-basis` | 0 |
| B | yes | **spot** | `unexplained` | non-zero |
| C | **no** | perp | `venue-basis` | 0 |

- **A** is today's lane, correctly conditioned. Its existing assertion that the class set IS
  the «БАЗИС ПЕРП/СПОТ» note — `basis_sets(out)[0] == basis_sets(out)[1]` — is preserved as
  written, and the note's text changed under TZ-34 without changing that parser, which must be
  confirmed rather than assumed.
- **B** is the behaviour TZ-34 introduced and which nothing asserts end-to-end today: a
  declaration no longer buys a licence.
- **C is the case this whole line of work exists for** — a coin never declared, silently cached
  on the perpetual, now earns the basis licence instead of falling into `unexplained`. It is the
  UNI/XLM/ZEC shape, and until this lane exists it is asserted only at unit level in the
  garrison and nowhere through `--verify`'s own exit code.

**One further assertion, and it is the strongest of the four:** lanes A and C must produce the
SAME class set and the same exit code. The declaration is the only thing that differs between
them, and it must make no difference at all. An equality that holds across a varied input is
what «this input no longer decides» means; a pair of separate green checks is not.

### 2.3 The five sites that crash instead of reporting

`out.strip().splitlines()[-1][:150]` appears five times as the `info` argument of `ok(...)`.
Python evaluates that argument **before** `ok` is called, so an empty `out` raises `IndexError`
on a check that was about to PASS, and the bench dies mid-run — losing every check after it.

The repair is one helper returning an empty string on empty input, used at all five sites. **The
reason it is in scope for this TZ rather than deferred:** a crash makes `checks[0]` smaller, the
summary prints that smaller number, and nothing distinguishes a bench that shrank from a bench
that crashed. A count that can silently shrink is not a count (inv. 43), and the guard at the
foot of the file only catches the zero case.

**No expected total is added.** A bench asserting a hardcoded count of its own checks is a
numeral that stops moving with the file it judges (inv. 65); the gate step's own delta is the
signal.

---

## 3. What must NOT change — negative assertions

Checked for absence or for unchanged survival before the report is written. A hit blocks
delivery.

1. **`bench/backtest_bench.py` and `bench/backtest_guard_bench.py` are byte-identical to the
   branch head.** This is the first assertion and the one that matters: the red under repair is
   a stale expectation, and hard floor item 2 forbids moving the thing under test to satisfy the
   test. If a lane in §2.2 cannot be made to pass without editing production-side code, that is
   a finding and the TZ is reported BLOCKED — not resolved by an edit.
2. **`index.html` and `main.py` byte-identical.** Nothing here reaches production.
3. **The check count does not fall.** 35 is the floor; the new lanes and the surviving lanes add
   to it. A repair that removes an assertion to go green is the failure this bench exists to
   prevent, applied to itself.
4. **The `SPEC` metric loop is untouched** — ten checks reading the source text for the measure
   chosen per field. It is unrelated to the venue and must neither move nor be renumbered.
5. **Case 9 still classes `AAA` as `unexplained`.** This is the check that §2.1's census did not
   quietly move a cell into the `coverage` lane. Both the class name and the non-zero exit are
   asserted, as today.
6. **«systemic breach (all coins) still fails after v3» stays green throughout**, before and
   after, with no change to its mutation or its expectation.
7. **No threshold, class name or `SPEC` entry moves**, in either file.

---

## 4. Text quoted from the repository, so the Executor compares rather than recalls (inv. 55)

From `bench/verify_bench.py` at this specification:

```
    for sym, px in coins.items():
        vol = [[t, 1e7] for t, _ in px]
        json.dump({'prices': px, 'volumes': vol, 'src': 'synthetic'},
                  open(os.path.join(dirpath, sym + '.json'), 'w'))
```

```
ok('fut basis: return gap exits 0 with html', code == 0, 'exit=%s' % code)
ok('fut basis: return gap named as basis and classified venue-basis',
   'БАЗИС ПЕРП/СПОТ' in out and 'AAA' in out and basis_sets(out)[0] == basis_sets(out)[1]
   and len(basis_sets(out)[0]) > 0, out.strip().splitlines()[-1][:150])
```

```
# Invariant 22: a validator that passes with no data is a failed validator. The
# guard sits after the summary so a red run still prints its own numbers, and it
# may only ever make this bench redder.
if checks[0] == 0:
```

From the System Map, the clause §2.1 must not breach:

> **A bench contains no copy of production math.** Formulas are cut from the source at run
> time and called by name.

---

## 5. Validation — written by the Architect, run by the Executor

**5.1 Compile and scope.**
- `python3 -m py_compile bench/verify_bench.py` — clean.
- `git diff --name-only` against the branch head names exactly `bench/verify_bench.py`.
- `md5sum` for `index.html`, `main.py`, `bench/backtest_bench.py`,
  `bench/backtest_guard_bench.py` against the branch head — all four unchanged, quoted.

**5.2 The bench itself.**
`python3 bench/verify_bench.py` → **FAIL 0**, with the count published as measured and no total
predicted beforehand (inv. 43). The delta against 35 is attributed lane by lane.

**5.3 The lanes assert something — negative control (inv. 23, 45, 65).**
On a SCRATCH copy of `backtest_bench.py` under `/tmp`, never the repository's, restore the
pre-TZ-34 licence (`sym in fut`) and re-run this bench:
- lane **B** must go RED — the declaration would buy the licence again;
- lane **C** must go RED — an undeclared perp series would lose it;
- lane **A** must stay green, because it is the one cell the two rules agree on. **A control in
  which every lane flips has not localised anything**; this one names which lanes carry the new
  rule and which carries the shared one.

**5.4 The crash repair is proven, not asserted.**
On a scratch copy whose `verify_against_live` returns before printing anything, this bench must
run to completion, report its failures and print its count. Before the repair the same input
ends in `IndexError`; both readings go in the report.

**5.5 Gate replay, `bench.yml` steps 1–14, before and after.**
Before = the branch head; after = this commit. **Step 4 moves from RED to GREEN and its count
rises by the lanes added. Every other step reads delta zero, and step 14 reading anything but
zero means this TZ touched the garrison and is a §3.1 breach.**

**5.6 The hosted run, which this branch has never had past step 9.**
Push and read the `Bench gate` run for the new branch head off the run page, step by step. The
gate previously halted at `verify_bench.py`, so **steps 10–19 have never had a runner reading on
this branch** — including the garrison and TZ-34's new section. Report each step's conclusion
and the garrison's runner-measured count, which supersedes TZ-34's local 174.

**5.7 Report.**
Line counts and MD5 for the System Map and for every file the map's `## 0` table currently
lists, the set read from that table at authoring time. No claim about this report's own commit
or push (inv. 54).

---

## 6. Not this TZ

- **`backtest_bench.yml` is not dispatched** (inv. 44). Whether UNI, XLM and ZEC were on the
  perpetual stays unread; this TZ neither asserts nor predicts it.
- **`R["fut"]` is not removed.** It is computed, returned and read by nobody — verified against
  the repository, not taken from the TZ-34 report. It is a real finding and it belongs to a
  cleanup, not to a TZ that must turn a gate green without touching the file it lives in.
- **Perpetuals as the default source stays open**, unchanged from TZ-34 §7.
