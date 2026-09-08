# Implementation Report — TZ-34

## Status

**PARTIAL.**

Every item of §2 is implemented and every negative assertion of §3 holds. The §5.2
garrison section is written, green, and shown by mutation to catch the defect it exists
for. **The one thing not delivered is §5.3's «steps 1–13 read delta zero»: gate step 4,
`bench/verify_bench.py`, is RED** — on a local replay and on the hosted runner. It is red
because this specification changes the rule its fixtures and its case 10 were written
against, and `verify_bench.py` is outside this TZ's `Touches` list. Hard floor item 2 and
§3.5 both forbid editing it to pass, so it is reported here, with the cause isolated by
measurement rather than by argument (§ Test Results, D).

The gate halts at the first failure, so **steps 5–14 have no runner reading on this
branch**; their readings below are a local replay and are labelled as such.

## Inbound Filing

None. `CryptoTZ/TZ-34-fetched-venue-observed.md` was already present on `origin/main`
under its canonical name and needed no move or rename.

Two facts about how it arrived, recorded because they cost a fetch to establish:

- The worktree was behind `origin/main` and carried no TZ-34 at all. `git fetch` was the
  first action of the session.
- **A different TZ-34 existed and was replaced in place on the remote.**
  `13ebbaf` added `CryptoTZ/TZ-34-futures-archive-census.md`; `96c88ab` deleted it;
  `b5757f9` added `CryptoTZ/TZ-34-fetched-venue-observed.md`. The scope is not a revision
  of the first — it is a different specification under the same number. The file executed
  is the one live on `origin/main` at `b5757f9`, and §0's own line («The Executor names
  the committed file from this line and never from the name it received») was matched
  against it.

## Scope Executed

**Branch TZ** (§8): the scope authorises two files outside `CryptoReports/**`, so it opens
a branch and awaits a pull request.

The §0 fingerprint gate was matched BEFORE any work and passed in full: all seven anchors
as exact substrings of `SYSTEM-MAP-CRYPTOCALCUL.md`, all four rows of the map's `## 0`
file table, the TZ header's own figure for `bench/backtest_bench.py` (3724 lines, MD5
`84b1572fd3af207b1e658f44f0191fcf`) and contract v20 (814 lines, MD5
`9a257890e9db663eb0fc74129f4841e0`). Every one matched; nothing was BLOCKED.

Executed: §2.1, §2.2, §2.3, §2.4, §2.5 — all five.
Not executed, and not this TZ's: §6 (the runner dispatch) and §7 (perpetuals as default).

## Files Created

None.

## Files Modified

- `bench/backtest_bench.py` — 3724 → 3881 lines.
- `bench/backtest_guard_bench.py` — 823 → 971 lines.

`git diff --name-only` names exactly these two and nothing else.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### §2.1 — the census records the venue it observed

`cov` gains one key, `venue`, additive exactly as `hl` and `cov` themselves were (inv. 1,
9). It is written from the leg that actually won the `best` comparison and from nowhere
else.

The write needed one extraction, because the winning leg was known only inside a loop that
also performs the network I/O, and §5.2 requires the rule to be asserted offline against
synthetic legs (inv. 21). `_fetch_best(legs, attempt, pair, t_ref)` now holds the whole
rule: it attempts the legs in the order given, keeps the longest series, and returns the
census with `cov["venue"]` set from the leg that won. `attempt(is_fut)` — the only part
that touches the network — is a parameter.

Three properties are deliberate and all three are asserted:

- **A tie keeps the leg attempted FIRST.** That is what the pre-existing strict `>` always
  did; it is preserved rather than reasoned about, and for a non-declared coin it means
  spot.
- **`None`, not `"spot"`, when no leg returned a row.** Nothing was observed, and that is
  not the same fact as an observation of spot. Such a coin never reaches `_save` anyway —
  `< 2600` rows is a skip — so no document can carry a null venue.
- **The declaration is not an argument of `_fetch_best` and cannot reach the answer.** The
  leg ORDER is still decided by the declaration, at the call site, unchanged.

`fetch_cg` records `venue` too, from `_venue_name(False)`. That path queries CoinGecko's
`market_chart` — a spot index — and attempts no second leg, so its one leg won and the
value is read off the endpoint that answered. This is the same act as reading it off
`is_fut`, not the default §2.2 forbids: it is written by the code that performed the
fetch, never by the code that reads it. Had it been left unset, every CoinGecko-sourced
cache would have been refused under §2.2 and the fallback source would have stopped
working entirely — a behaviour change well outside this scope.

### §2.2 — a document without `venue` never reaches the classifier as spot

The TZ leaves the mechanism to the Executor and fixes the property. **A cache-key bump was
available and was NOT used**: the key lives in `.github/workflows/backtest_bench.yml`,
which this TZ does not name and hard floor item 8 protects. Both mechanisms used are
inside the two authorised files:

1. **Refetch, on the fetch side.** `fetch_prices` and `fetch_cg` both read an existing
   cache document before deciding to skip it. Where `_venue_licence(cov)` is `None`, the
   document is treated as absent and falls through to the fetch, printing
   «площадка не записана — перекачка» on its census line. This is the normal path: the
   Actions cache restores such documents and `--fetch` is the only thing that can replace
   them.
2. **Refusal, on the read side.** `_cell_class` raises `VenueUnobserved` rather than
   answering. `reconcile` collects every affected symbol instead of dying on the first,
   then prints the whole list to **stdout** and exits non-zero.

Stdout rather than stderr is deliberate and was a correction made during validation: the
first implementation let the exception propagate, `verify_bench.py`'s `run_verify`
captured only stdout, and the empty result crashed that bench with an `IndexError` at its
own line 212 — a bench that could not report what it found. With the refusal printed, it
now runs all 35 checks to completion and names its failures.

`_venue_licence` returns three values — `True`, `False`, `None` — and `None` is the
absence. Returning `False` there would have been the defect one layer down.

### §2.3 — the reconciliation reads the observation

`_cell_class(cov, win_d, t_last)` replaces the inline `if sym in fut:` block. The
`venue-basis` licence is granted from `cov["venue"] == VENUE_PERP`.

The three class names, `CLASSES`, `HARD_CLASSES`, every threshold in `SPEC`, the measure
chosen by field type, the sign convention and `target_gate` are untouched. `sym in fut`
appears nowhere in the classifier.

### §2.4 — the census line prints it

`print_census` gains a `площадка` column after `тикер`, and the header in `fetch_prices`
gains it in the same position. **An absent observation prints `—` and never the word
`spot`**, which is the same distinction the record itself makes.

### §2.5 — the garrison gains a section

`bench/backtest_guard_bench.py` gains section E, 32 offline comparisons, one item per
§5.2 item. Every assertion calls a production function by name; no rule is
re-implemented except inside the §5.2.5 inversion, where re-implementation IS the control.
The module docstring's A–D list gains its E row.

### Two printed strings this change made false, repaired

Both are inside `backtest_bench.py` and both would otherwise have shipped as known-wrong
output. They are named here rather than left for the audit to find:

- `fut_note` read «tokens[] из HTML не разобраны — базис-поблажки нет». The licence no
  longer hangs off that set, so a parse failure no longer removes it. Now: «объявленный
  набор не показан; на класс ячейки это не влияет».
- The basis line read «БАЗИС ПЕРП/СПОТ (fut-монеты, …)». That list can now name a coin
  never declared. Now: «(серия качана с перпетуала, …)».

`R["fut"]` is still computed and still returned. It has no reader in the repository and
was not removed — removing it is not in this scope.

## Validation

### §5.1 Compile and no-regression — all clean

| Item | Command | Result |
|---|---|---|
| compile | `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` | clean, no output |
| scope | `git diff --name-only` | exactly the two bench files |
| production | `md5sum index.html main.py` vs `origin/main` | both **identical** |

```
index.html   worktree 4e71da9badca3ccae85b656fdc3773e8   origin/main 4e71da9badca3ccae85b656fdc3773e8
main.py      worktree 0e3ead8c300d2ee6783303c4bf2fb6b5   origin/main 0e3ead8c300d2ee6783303c4bf2fb6b5
```

`--selftest` and `--lab-selftest` were **NOT run**: they need an archive and a runner
(inv. 44). Their standing is exactly what it was before this TZ; nothing here implies a
run of either.

### §3 negative assertions — every one checked, none hit

| § | Assertion | Reading |
|---|---|---|
| 3.1 | `index.html` and `main.py` byte-identical; inv. 41 untouched | `git diff --quiet origin/main -- index.html main.py` → **YES** |
| 3.2 | fetch ORDER does not move | `(True,) if fut else (False, True)` present, once; `best` still keeps the strictly longer series |
| 3.3 | no threshold, class name or constant moves | `HARD_CLASSES`, `CLASSES`, `SPEC`, `TGT_QUORUM_*`, `K_GRID`, `2600`, `0.05` — occurrence counts identical to `origin/main`; the diff touches no threshold line |
| 3.4 | `src` keeps its value and gains no meaning | `source + ("-perp" if fut else "")` unchanged, present once; nothing classifies on `src` |
| 3.5 | no bench edited to make it pass | `verify_bench.py` untouched and RED — reported, not repaired |
| 3.6 | no copied production math, no new network call | section E is synthetic input to named functions; `_fetch_best`'s network is a parameter and is stubbed |

## Test Results

### A. Gate step 14 — `backtest_guard_bench.py`, local

```
E. venue-as-observation: 32 comparisons
checks run: 174   FAIL 0
```

**142 → 174, Δ +32**, attributed term by term as §5.3 requires:

| Item | §5.2 | Comparisons |
|---|---|---:|
| 34 | 1 — the label follows the winning leg, both directions, plus tie, absence, declared-only | 6 |
| 35 | 2 — the declaration does not decide it: 2 fixtures × 2 declarations × 2 assertions | 8 |
| 36 | 3 — the licence follows the observation, both cells, plus the coverage lane | 5 |
| 37 | 4 — no observed venue never classifies as spot: 3 fixtures × 2, plus 2 | 8 |
| 38 | 5 — the inversion | 4 |
| 39 | 6 — the section's own count guard | 1 |
| | | **32** |

The section prints its count AFTER its own guard, so the figure it prints is the figure
the gate total moves by. A section reporting one less than it added is a delta nobody can
attribute (inv. 43).

### B. §5.2.5 — the negative control, in-bench

Item 38 restores `sym in fut` as the licence test and re-runs items 36 and 37's
expectations against it. Both go red: a perp series not declared loses its licence, and a
document with no venue is read as spot anyway. The bar is read off the fixture's own
`venue` — a different authority from the declaration under test (inv. 65).

### C. Mutation testing of section E — three defects, all caught

Beyond the in-bench inversion, the section was run against three mutated copies of
`backtest_bench.py` to establish that it is wired to production and not to itself.

| Mutation | Result |
|---|---|
| the licence ignores the observation (`perp = False`) | **FAIL 4** — items 36 and 37 |
| an unobserved venue defaults to spot (`_venue_name` drops its `None` branch) | **FAIL 1** — item 34 |
| the venue is read from the declared leg set, not the winner | **FAIL 6** — items 34 and 35 |

The unmodified file reads FAIL 0.

### D. Gate step 4 — `verify_bench.py` — RED, with the cause isolated

Local replay: **35 checks, 8 FAIL** (the count is unmoved from 35; the verdict moved).
Two causes, both established by running the bench, not by reading it. Both diagnostics
were performed on scratch copies under `/tmp`; **the repository's `verify_bench.py` was
never modified** and is byte-identical to `origin/main`.

1. **Its fixtures predate the key.** `make_cache` writes
   `{'prices', 'volumes', 'src': 'synthetic'}` — no `cov` at all, so no `venue`. Under
   §2.2 the reconciliation must refuse such a document, and it does. Adding
   `cov` with `venue: "spot"` to the fixture in a scratch copy takes the bench to
   **35 checks, 3 FAIL** — 32 of the 35 pass with no other change.
2. **Case 10 asserts the rule this TZ replaces.** The 3 that remain are case 10, which
   writes an HTML naming `AAA` as `fut:true` and expects a big gap on `AAA` to be
   labelled basis and exit 0. Under §2.3 the declaration no longer buys the licence, and
   `AAA`'s series is spot, so it classes `unexplained`. Setting the same fixture's venue
   to `"perp"` instead makes exactly those 3 pass and makes the outlier cases fail
   instead — the mirror, and confirmation that the licence now tracks the observation and
   nothing else.

So the whole of step 4's red is the specified behaviour change meeting a bench whose
fixtures and whose case 10 were written against the pre-TZ-34 rule. It is a stale
expectation in the exact sense of hard floor item 2, and item 2's own sentence is that
this is a finding and not a licence to change the assertion. `verify_bench.py` is not in
this TZ's `Touches` list, so it was not touched.

### E. §5.3 Gate replay — `bench.yml` steps 1–14, before and after

Before = `origin/main` at `b5757f9` in a separate clean checkout; after = this branch.
Both **local replays, not runner executions**.

| Step | Bench | Before | After | Δ |
|---:|---|---:|---:|---|
| 1 | `verify_board.js` | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 |
| 3 | `prot_bench.js` | 372 | 372 | 0 |
| 4 | `verify_bench.py` | 35, rc 0 | 35, **rc 1** | count 0, **verdict RED** |
| 5 | `direction_bench.py --props …` | rc 1 | rc 1 | 0 — see below |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 |
| 7 | `journal_bench.js` | 691 836 | 691 836 | 0 |
| 8 | `catalyst_bench.js` | 24 692 | 24 692 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 16 171 | 16 171 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | 220 598 | 220 598 | 0 |
| 13 | `live-gate.sh --selftest` | 40 | 40 | 0 |
| 14 | `backtest_guard_bench.py` | 142 | **174** | **+32** |

No total was predicted before it was measured (inv. 43).

**Step 5 fails identically on both sides of the replay and is not this TZ's.** It ends
`node failed` with byte-identical output before and after, and it passed on the hosted
runner for this branch's commit. It is a property of this session's machine, not of the
repository — the same reading a previous session recorded for this step.

**Step 7 reads 691 836 on both sides here, against the 693 895 the map records.** That
difference is a property of the environment and of TZ-33, not of this change: it is
identical before and after, and this TZ writes nothing the journal records.

## Deviations

1. **The refusal prints to stdout and exits non-zero, rather than propagating an
   exception.** §2.2 permits «raise, refuse or refetch» and this is the refusal, made
   legible: an uncaught exception produced an empty stdout, which crashed a calling bench
   before it could report anything. Both mechanisms are present — `_cell_class` still
   raises, which is what §5.2.4 asserts, and `reconcile` converts it into a named refusal
   listing every affected symbol.
2. **`fetch_cg` records `venue: "spot"`.** §2.1 speaks of the leg that won the `best`
   comparison; that path has exactly one leg and no comparison. Reasoning in
   § Implementation Summary. Flagged because it is the only place a venue is written from
   an endpoint rather than from an `is_fut`.
3. **§5.2.2 was read as «the declaration is not an input», not as «the attempted legs are
   the same».** Taken literally against production's own leg order, a declared coin
   attempts only futures, so a «spot leg longer» fixture cannot produce `spot` when
   declared and the venue WOULD differ. Item 35 therefore holds the attempted legs at
   production's non-declared order and varies the declared set, asserting `venue` and
   `_venue_licence` unchanged across all four cells — which is the separation the item
   exists to prove. That declared coins still attempt futures only is asserted separately,
   in item 34.
4. **Two printed strings were repaired** because this change made them false. Named in
   full in § Implementation Summary.

## Pre-existing Issues

1. **`verify_bench.py` crashes instead of reporting when `--verify` produces no stdout.**
   Five sites, line 212 among them, read `out.strip().splitlines()[-1]` while building the
   `info` argument of a failing check, which raises `IndexError` on empty output and takes
   the bench down mid-run — losing every check after it. This TZ exposed it but did not
   cause it: any `--verify` path that exits before printing does the same. Not repaired —
   the file is out of scope.
2. **`R["fut"]` has no reader.** `reconcile` computes and returns the declared set; no
   caller in the repository reads the key. Pre-existing, unrelated, and untouched.

## Remaining Risks

1. **`bench.yml` cannot go green on this branch until `verify_bench.py` is
   re-registered.** This is the one thing standing between PARTIAL and COMPLETED, and it
   needs a specification, not an Executor edit. The shape is known and measured
   (§ Test Results, D): its fixtures must carry a `venue`, and case 10 must be re-registered
   against the observation — either by giving its `AAA` fixture `venue: "perp"` to keep
   testing the basis lane, or by rewriting the case to assert that a DECLARED coin whose
   series is spot no longer earns the licence, which is the behaviour this TZ introduces
   and which nothing currently asserts end-to-end.
2. **Whether UNI, XLM and ZEC were on the perpetual is still unread**, and this TZ neither
   asserts nor predicts it (§6, inv. 44). It is `backtest_bench.yml`, dispatched,
   `--fetch` then `--verify`; the dispatch is the Boss's and the verdict the Architect's.
   Both outcomes are informative and neither is a defect of this TZ.
3. **The first `--fetch` after this merges will refetch every cached coin**, because no
   document on the Actions cache carries a `venue` yet. That is the refetch trigger
   working as designed, not a fault, but it makes the next archive run longer than usual
   and it should not be read as a cache failure.
4. **§7 is untouched and remains open**: 26 of 31 series are measured on Binance spot
   while the Boss trades perpetuals. The census this TZ adds is the precondition for
   measuring that switch, and the switch is deliberately not here.

## Commit

One implementation commit, on the branch, made and pushed before this report was written:

- `a73359d` — `TZ-34: the venue actually fetched is recorded and read`
  Contents: `bench/backtest_bench.py`, `bench/backtest_guard_bench.py`. Nothing else.

This report is authorised to be committed to `main` on the `CryptoReports/**` direct-push
path with the message `docs(reports): TZ-34 — the venue actually fetched is an
observation (TZ-34)`. That commit has not happened at the time of writing and carries no
hash, conclusion or push result here.

## Pull Request

**No pull request exists.** The `gh` CLI is not installed in this session
(`gh: command not found`), and §8's fallback applies rather than a stop or a question.

- Branch: `claude/tz-34-fetched-venue-observed`
- Compare URL: https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-34-fetched-venue-observed

The Boss opens and merges from that link in one action, after the Architect's verdict.
**The gate is RED on this branch** (below) — the merge should not be made on the strength
of this report alone.

## CI Execution

**`Bench gate` ran on a hosted runner** for branch commit `a73359d`
(`push` to `claude/**` is in its trigger list) and its conclusion is **failure**.

Run: https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/34239183167

Read off the run's own job steps, not from a local replay:

| Workflow step | Bench | Conclusion |
|---|---|---|
| 6 | `verify_board.js` | success |
| 7 | `board2_bench.js` | success |
| 8 | `prot_bench.js` | success |
| **9** | **`verify_bench.py`** | **failure** |
| 10–19 | `direction_bench.py` … `backtest_guard_bench.py` | **skipped** |

The gate halts at the first failing step, so **steps 5–14 of the bench numbering have no
runner reading on this branch, including step 14 and its new section.** Their readings in
this report are a local replay and are labelled as such throughout. What the runner does
establish is that the failure is `verify_bench.py` alone and that steps 1–3 are green
there.

It also settles the local step 5: it did not fail on the runner, so its local `node
failed` is this session's machine.

`backtest_bench.yml` was NOT dispatched (§6, inv. 44). `main.yml` cannot have been
triggered by anything in this session: its `push` filter is an ALLOW-list of two literal
paths, `main.py` and `.github/workflows/main.yml`, verified by reading the workflow before
the first push, and the only `paths-ignore` string in that file is inside a comment.

## Final Repository State

The session leaves behind the branch **`claude/tz-34-fetched-venue-observed`** at
`a73359d`, pushed and measured. It carries exactly two modified files against `main`:
`bench/backtest_bench.py` and `bench/backtest_guard_bench.py`.

The working tree is clean. No generated artifact is committed: `__pycache__/` was removed
and the bench scratch files (`bench/_*.js`, `bench/_*.json`) are untracked under
`.gitignore`. The scratch checkouts and the diagnostic copies used for § Test Results C
and D were under `/tmp` and are removed.

**NOT IN EFFECT UNTIL MERGED.**

The previous TZ's branch WAS merged before this work started — `f1c6d46`, pull request
#30, `claude/tz-33-entry-anchor-geometry` — so this is not built on an unmerged base.

## Fingerprints

`SYSTEM-MAP-CRYPTOCALCUL.md` — **2384 lines, MD5 `7807a6787f5db7b0d52eb9916b781ffe`**,
revision string **`**Revision 2026-09-08-a.**`**, matching the TZ header's required
revision.

Every file the map's `## 0` table lists, at that revision — all four unchanged by this TZ:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

The files this TZ's header adds, and the contract:

| File | Lines | MD5 | |
|---|---:|---|---|
| `bench/backtest_bench.py` | 3724 | `84b1572fd3af207b1e658f44f0191fcf` | was, at the specification |
| `bench/backtest_bench.py` | **3881** | **`45e2294c5fc82f96a7e66b84c2a094c2`** | now |
| `bench/backtest_guard_bench.py` | 823 | `99d5f415f0a8d79eadeaf644b718e899` | was |
| `bench/backtest_guard_bench.py` | **971** | **`19427e79133d48870d76eb0c908c69f6`** | now |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` | unchanged |
| `CryptoTZ/TZ-34-fetched-venue-observed.md` | 409 | `850588256088320075f3b08a23d136cc` | the specification executed |
