# Implementation Report — TZ-25

**Previous TZ's branch: nothing to merge.** TZ-24 was a report-only TZ — no branch
matching `*tz-24*` exists on any ref (`git branch -a --list '*tz-24*'` → empty) and its
report is on `main`. Of the three older branches still present locally,
`claude/tz-21-catalyst-registry-scope-and-basis` and
`claude/tz-23-main-workflow-paths-allowlist` are ancestors of `origin/main`
(`git merge-base --is-ancestor` → 0); `claude/tz-20-catalyst-registry-content` is not,
which is the state the map's §10 table already records as **declared dead — do not
merge**. No work in this session was built on any of them.

---

## Status

**BLOCKED.** No production file was modified, no branch was opened, and the
implementation was not started.

Three obstacles were measured. The first alone is decisive and is a contract-level
conflict; the second and third are defects inside TZ-25 that survive independently of
the first and would still stop the work if the first were resolved.

---

## Inbound Filing

None. `CryptoTZ/TZ-25-universe-morpho-arb.md` was already on `origin/main` under its
declared canonical filename (commit `62af0ba`, "Add files via upload"). No file landed
in the repository root, no filename was mangled, nothing was moved or renamed.

The TZ was located by `git fetch --all --prune` per contract §3 — it was absent from the
session's working tree at start (`c17d590`) and present on `origin/main` (`7f8a30a`),
which is exactly the case §3 exists for. The clone is not shallow
(`git rev-parse --is-shallow-repository` → `false`).

---

## Scope Executed

**TZ class: branch TZ** (read off TZ-25 §4, which names `main.py`, `index.html`,
`bench/**` and `journal/**` — files outside `CryptoReports/**`; the TZ header states the
same class). Contract §8's branch clauses therefore have a referent, and the class is
recorded here before any clause reads off it.

**Scope executed: none of §4.** §4.1 (`main.py` `TOKENS`), §4.2 (`index.html`
`tokens[]`), §4.3 (hardcoded universe counts) were all left untouched. §4.4's
prohibitions were honoured trivially.

What was executed is the part of §4a that precedes step 7: the fetch (§3), the
fingerprint gate (§5), the §3 ordering precondition TZ-25 requires be verified before
starting, and the repository-state check (§4a step 6). All four passed or were met. The
block is raised by contract §7, which sits between them and step 7.

The read-only survey TZ-25 §4.3 asks for was also completed and is reported in full
below, because it is the one deliverable of this TZ that a blocked session can produce
correctly and it is what a follow-up TZ needs.

---

## Files Created

`CryptoReports/TZ-25-universe-morpho-arb-report.md` — this report, and nothing else.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Obstacle 1 — hard floor §7 item 3. Decisive, and not resolvable inside a TZ.

`EXECUTOR-INSTRUCTIONS.md` on `origin/main` at `7f8a30a` is **version 18**, 780 lines,
MD5 `3dd8d30b117df610b6dba7c0377ea16b`. Its §7 item 3 reads, verbatim:

> 3. **No new coins.** `TOKENS` (bot) and `tokens[]` (frontend) are frozen at 28
>    (inv. 2).

§7's preamble governs how that clause meets a TZ:

> **Hard floor — binding regardless of what a TZ says.** If a TZ appears to require any
> of the following, the TZ is defective. Report BLOCKED and quote the conflicting
> requirement.

TZ-25 §1 requires `TOKENS` and `tokens[]` to become 30. That is the clause's exact
subject, at the clause's exact number, with no reading under which it is something else.
Contract §12 names this outcome by name — "**Blocked.** Missing file, missing
credential, failed fingerprint gate, network policy, or **a hard-floor conflict**" — and
§14 fixes the arithmetic: "A blocked task costs one message. A silently wrong
implementation of trading infrastructure costs money."

**TZ-25 §1 amends the wrong two documents.** It states that "the standing decision in
map inv. 2 and `## 8` is amended by the owner for these two assets". The hard floor is
neither of those. It is `EXECUTOR-INSTRUCTIONS.md`, the document this session is required
to read in full before reading the TZ, and the document whose §7 declares itself
un-overridable by a TZ's own text. A TZ amending a rule that binds it is the one move the
hard floor is built to refuse.

**Neither of the two documents TZ-25 does name was amended either, and this is
measured, not inferred.** Both still carry the rule on `main` at `7f8a30a`:

| Site | Text on `main` at `7f8a30a` |
|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md:161` | `**Universe: 28 pairs, frozen.** New coins are not added (standing decision, inv. 2).` |
| `SYSTEM-MAP-CRYPTOCALCUL.md:1210` (inv. 2) | `New coins enter only through TOKENS (bot) + tokens[] (frontend); … (Standing decision: no new coins.)` |

And the map carrying them is at revision **`2026-09-02-a`** — the exact revision TZ-25's
own §0 gate requires this session to verify and match. So TZ-25 pins a map revision whose
inv. 2 forbids TZ-25.

**The commit batch that delivered TZ-25 is itself evidence about intent, and it points
the same way.** `git diff --stat c17d590..origin/main` over the seven commits that
carried the TZ:

```
 ANALYST-INSTRUCTIONS.md               | 448 ++++++++++++-----------
 CryptoTZ/TZ-25-universe-morpho-arb.md | 198 +++++++++++
 analyst/live.json                     |  64 ++---
 analyst/owner.json                    |  20 +-
 journal/data/2026-09-02.jsonl         |  28 +++
 journal/out/2026-08-26-h7.jsonl       |  26 ++
 journal/runs.jsonl                    |   1 +
```

A governing document *was* uploaded in this batch — `ANALYST-INSTRUCTIONS.md`, 448 lines
changed — so the upload channel for contract-class artifacts was open and in use.
`EXECUTOR-INSTRUCTIONS.md` and `SYSTEM-MAP-CRYPTOCALCUL.md` are not in the batch. The
freeze was not lifted anywhere; it was overridden in a TZ.

**Why this session does not resolve it by judgement.** The contract's own opening rule
is explicit: "**No rule lives in two files.** … If you find the same rule in two places,
that is a defect and a finding for your report (§12) — **not a choice for you to make
between them.**" The "no new coins" rule now lives in three places (contract §7 item 3,
map inv. 2, map §1 line 161) and a fourth document asserts it is amended. That is the
described defect, and the described response is this report.

The contract also records what happens when an Executor closes a gap like this by
judgement instead. Version 15's own changelog: TZ-22 left three clauses without a
referent, "the report resolved all three correctly and **resolved them by JUDGEMENT** —
which is the thing inv. 54 says is not a control, in the same file v14 hardened for
exactly that reason." Being right is not the standard; the control is.

**What unblocks it, precisely.** Three uploads by the Boss, then re-trigger:

1. `EXECUTOR-INSTRUCTIONS.md` **v19**, amending §7 item 3 — either lifting the freeze to
   30, or restating it as "frozen except by an owner decision recorded in the map".
   Item 11 wants a wording pass in the same edit: it enumerates the venue set as
   "`fut:true` on **XMR, LIT and HYPE** is fixed by the Boss", and that enumeration
   becomes stale at five assets.
2. `SYSTEM-MAP-CRYPTOCALCUL.md` at a **new revision**, amending inv. 2, §1 line 161,
   §3.14's venue set, and the "25 of 28" coverage statements at lines 815, 869 and 1506.
3. **TZ-25's §0 gate re-pinned to that new revision** — as written it requires
   `2026-09-02-a`, so a corrected map would fail TZ-25's own fingerprint gate and block
   the work a second time for the opposite reason.

Nothing about the change is unsound on the merits. `fut:true` is the right declaration
and §2's reasoning for it is correct as far as it goes. The obstacle is procedural and
the repair is cheap — but it is the Architect's to make, not this session's.

---

### Obstacle 2 — TZ-25 §2's own STOP condition fires. Independent of obstacle 1.

TZ-25 §2 pins four sites and then binds this session to a specific reaction:

> **If any of the four sites above requires an edit, STOP and report.** A required edit
> there means the declaration leaked into the spot universe, which is a defect in this TZ
> and not a task to complete.

One of the pinned sites is "the §3.17 caption's «25 спотовым монетам» and the
exact-string expectation gate section M pins it with **do not move**".

**That site requires an edit.** The pinned string is not the coverage fragment alone. The
production caption at `index.html:2858` (decoded from its `\uXXXX` escapes) and the
bench expectation at `bench/exhaustion_bench.js:1580–1583` (`const CAPTION`) both end,
character for character:

> Список считается по 25 спотовым монетам: **три фьючерсные** в меру не входят.

The sentence states **two** counts, not one. TZ-25 §2 is correct that the spot count 25
does not move — `listExhaustion` skips `fut:true` rows ahead of every other test, so it
stays 25 whatever is added as futures-only. But the same sentence also states the
**futures** count, and that count is exactly what this TZ changes: `fut:true` goes
**3 → 5** (measured: HYPE, XMR, LIT today).

The result is a fork with no compliant branch:

- **Leave the caption.** `index.html` ships a caption asserting three futures assets are
  excluded from the day-range measure while five are, and `bench/exhaustion_bench.js`
  section M pins that false sentence as its expectation and passes — a green gate
  guarding a wrong string. TZ-15 built section M to make this class of drift impossible;
  it would be inverted into the thing that certifies it.
- **Correct the caption.** That is an edit to `index.html` beyond `tokens[]`, forbidden
  by §4.2 ("no other edit to the file"), plus an edit to the section M expectation,
  forbidden by §2's "do not move" and by §5, where step 12 is listed as MUST NOT move.

**Note the diagnosis §2 offers does not fit.** §2 predicts that a required edit here
means "the declaration leaked into the spot universe". It did not — the spot universe is
genuinely untouched at 25 and §2's whole protective argument holds. The leak is into the
**futures** count sitting in the same pinned sentence, which §2's enumeration does not
cover. The STOP is correct; the reason attached to it is not the one that occurred, and
a follow-up TZ should say so rather than inherit the wrong cause.

Also inside step 12's bench, and inspected under the same heading:
`bench/exhaustion_bench.js:408` — `eq('live shape: 28 rows, 25 counted', r.n, 25);`. The
asserted value is 25 (spot) and does not move; the literal 28 in the label is a universe
count that goes stale. A label edit does not move the check count of 220 598, but it is
still an edit to a bench §5 pins.

---

### Obstacle 3 — §4.3 and §4.4 disagree over `bench/exhaustion-calibration.txt`.

`bench/exhaustion-calibration.txt:1`:

```
Universe: 25 spot of 28 declared tokens (fut:true excluded by declaration, inv. 41): HYPE, XMR, LIT
```

That line carries a universe count (`28` → 30) **and** an enumeration of the `fut:true`
set (→ HYPE, XMR, LIT, MORPHO, ARB). §4.3 requires updating every site in `bench/**`
carrying the literal 28 as a universe count; §4.4 forbids touching this file, and §2
names it among the sites that stay untouched. Line 49 of the same file
(`монет в кэше: 28 из 29`) is a second occurrence, and is a record of a past run rather
than a live count.

This one is smaller than obstacle 2 and might be resolved by an explicit carve-out — the
calibrated content (`DAY_RANGE_ABNORMAL = 1.39`, the 25-coin basis) genuinely does not
move, and only the descriptive header is stale. But it is a direct contradiction between
two sections of the same TZ, and contract §12 says an ambiguity admitting two readings is
not for this session to resolve.

---

## Validation

TZ-25 §6 lists eight validation items. **None was run, and none is reported as passed or
as failed-on-the-work: all eight are unrun, for one reason — there is no implementation
to validate.** Contract §9's rule that an unrunnable item "fails, it is never *not
applicable*" governs validation of work performed; here §4a stops at step 7 and steps 8
and 9 are never reached. The distinction is stated rather than blurred, per §10.

| § | Item | Result |
|---|---|---|
| 6.1 | `python3 -m py_compile main.py` | NOT RUN as validation — run as **baseline** (below) |
| 6.2 | `node --check` on extracted `<script>` | NOT RUN as validation — run as **baseline** (below) |
| 6.3 | Full `bench.yml` gate, 13 steps, per-step table + §5 attribution | NOT RUN — no change to attribute |
| 6.4 | Two-way compatibility against an old `coeffs.json` | NOT RUN |
| 6.5 | Spot ticker unchanged, `?symbols=` stays ~12 KB | NOT RUN |
| 6.6 | Venue path — both coins price from `cachedFutTickers` | NOT RUN |
| 6.7 | `listExhaustion` universe still 25 | NOT RUN |
| 6.8 | No-regression statement over every file touched | NOT RUN — no file touched |

What **was** run, in full, is everything §4a places before the block.

### Fingerprint gate (contract §5, TZ-25 §0) — PASS

All seven content anchors matched as exact substrings against
`SYSTEM-MAP-CRYPTOCALCUL.md` on `origin/main`:

| Anchor | Result |
|---|---|
| `**Revision 2026-09-02-a.**` | OK |
| `### 3.12 Direction engine — veto cascade` | OK |
| `### 3.15 Catalyst registry` | OK |
| `### 3.16 List exhaustion — the day-range measure` | OK |
| `## 11. Analytical engine` | OK |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | OK |
| `58. **A rule that names an object without naming how to compute it has named nothing.**` | OK |

All four fingerprinted files matched line count and MD5 exactly. No `## Pre-existing
Issues` entry arises from the gate. Full table under `## Fingerprints`.

### TZ-25 §3 ordering precondition — MET

§3 requires verifying that the Boss's Shortcut step landed before work starts, and to
report BLOCKED in one line if it did not. It landed:

```
n = 31
len(c) = 31
MORPHOUSDT in c: True
ARBUSDT in c: True
```

`analyst/live.json` on `origin/main` carries 31 rows in `c` including both new symbols.
**This is the one precondition TZ-25 asks about that is fully satisfied**, and it is
recorded so the Architect knows the Shortcut side needs no repeat — the block is entirely
on the repository side.

### Baseline state (contract §9, "baseline first")

Both standing checks were run against the **unmodified** tree, to establish that the
tree this session leaves behind is clean and that nothing in the block is a pre-existing
compile defect:

| Check | Result |
|---|---|
| `python3 -m py_compile main.py` | exit 0 |
| `node --check` on the extracted `<script>` (3161 lines) | exit 0 |

Baseline universe counts, measured by parsing rather than by eye:

| Measure | Value |
|---|---|
| `main.py` `TOKENS` entries | 28 |
| `main.py` `TOKENS` contains MORPHO / ARB | False / False |
| `index.html` `tokens[]` entries | 28 |
| `index.html` `tokens[]` with `fut:true` | 3 — HYPE, XMR, LIT |
| `index.html` `tokens[]` spot (no `fut`) | 25 |

This is exactly the state hard floor item 3 pins, which is why obstacle 1 is a conflict
and not a stale clause.

### Direct-push preconditions (contract §8) — verified before this report's push

§8 requires the `CryptoReports/**` direct-push path be confirmed rather than assumed,
before the first push of a session:

- `.github/workflows/main.yml` `push` filter is still a `paths` **allow-list** of exactly
  two literal paths — `'main.py'` and `'.github/workflows/main.yml'`. `CryptoReports/**`
  is unnamed, so under an allow-list it cannot start the bot. The guarantee is
  structural, as TZ-23 left it.
- `.github/workflows/bench.yml` `paths-ignore` carries `'**.md'`, so this report starts
  no bench run either.
- Pages serves `index.html` from `main`; nothing under `CryptoReports/**` reaches the
  live calculator.

---

## Test Results

No test suite was executed. The gate was not run because no product file changed, and
running it would measure the unmodified tree against numbers the map already publishes
for that tree (13 steps, 1 250 739 checks).

The §5 predictions are recorded here **unverified**, so a future session does not mistake
them for measurements: step 8 `catalyst_bench.js` 23 062 → 23 066 (+4), step 7
`journal_bench.js` moves, steps 12 and 13 hold at 220 598 and 40. None of these was
measured by this session and none should be cited as if it had been.

---

## Deviations

None. The session followed §4a in order and stopped where §7 requires it to stop. No
part of §4 was partially implemented, and nothing was worked around.

Two things were done beyond the minimum a BLOCKED report requires, both read-only and
both inside the TZ's own text: the §4.3 enumeration was completed (§4.3 asks for it
explicitly and it is the one product a blocked session can deliver correctly), and the
§2 pinned sites were checked, which is what surfaced obstacle 2. Neither wrote a file.

---

## Pre-existing Issues

**1. The `fut:true` count is stated in prose in two places and derived nowhere.** The
caption at `index.html:2858` hardcodes "три фьючерсные" and
`bench/exhaustion-calibration.txt:1` hardcodes "HYPE, XMR, LIT". The spot count in the
same caption (25) is equally hardcoded. `journal/write.js` shows the alternative and does
it correctly — it derives coverage from `P.tokens.length` (lines 548, 550, 708) and
carries no literal 28 at all, which is why the journal needs no edit under §4.3 while the
frontend does. This predates TZ-25; TZ-25 is only the first change that makes it bite.
It is reported, not fixed (contract §6).

**2. Map invariant 58 applies to the object this TZ is about.** Inv. 58 — "A rule that
names an object without naming how to compute it has named nothing" — is the newest
invariant and the one TZ-25's own gate anchors on. "The universe" is named as a count in
nine prose sites and computed in none. Whether that is worth a TZ is the Architect's
call.

**3. `claude/tz-20-catalyst-registry-content` remains unmerged.** Already recorded in the
map's §10 table as declared dead. Restated here only because contract §8 requires the
previous-branch check be reported, and because the map's own open-queue row notes that
nothing in the repository verifies an accepted TZ's branch reached `main`.

---

## Remaining Risks

**1. §4.3's instruction and hard floor item 2 want a word from the Architect.** Item 2 is
"never edit a bench to make it pass … a stale expectation is a finding, neither is a
licence to change the assertion." §4.3 instructs this session to update universe counts
inside `bench/**`. The honest reading is that an Architect-authorised count update is
assertion *maintenance*, not editing-to-green, and this session would have proceeded on
that reading had it reached §4.3. But it is worth one explicit sentence in v19, because
the distinction is currently held by the Executor's judgement — the same failure class as
obstacle 1.

**2. The predicted step 8 delta of +4 rests on a per-symbol attribution, not on the added
symbols' content.** The TZ-21 attribution in map `## 0` isolates "+2 per-symbol" for
`ENA`, an entry that also carried registry content. MORPHO and ARB enter with no
`catalysts.json` entry (§4.4 forbids touching it), so whether the per-symbol term applies
identically to a symbol absent from the registry is an assumption. It is cheap to verify
— run step 8 before and after — and the TZ's own §5 already forbids accepting an
unexplained delta. Named so the next session measures it rather than matching the
prediction.

**3. `bench/backtest_bench.py` and MORPHO.** TZ-25 §6 already anticipates that a
three-year archive may not exist for MORPHO and fixes the standing (record it as `GRAM`'s
case, do not repair). Recorded here as confirmed-still-open, not as a new risk. Two
`n_coins=28` / `coins=28` defaults in that file and in `direction_bench.py` are synthetic
generator parameters, not universe counts — see the enumeration.

---

## §4.3 enumeration — every site inspected, changed and unchanged

TZ-25 §4.3 requires every site in `bench/**`, `journal/**` and `index.html` carrying the
literal 28 as a universe count to be listed, **including the ones not changed and why**.
The survey was completed even though nothing was changed, because it is the artifact a
follow-up TZ needs and it is fully determined by the current tree.

Method: `grep -rn "28" bench/ journal/ index.html`, then every hit classified by reading
its context. Numeric coincidences (`28.3`, `0.28`, four-digit matches) are excluded and
named below so the exclusion is auditable rather than silent.

**Would move (universe count of `tokens[]`, 28 → 30) — 6 sites:**

| Site | Text | Class |
|---|---|---|
| `index.html:3340` | `// он считался на каждой карточке и не печатался нигде: Босс видел 28` | comment, universe count |
| `index.html:3341` | `// запретов без причины. Один раз наверху вместо 28 раз внутри.` | comment, universe count |
| `index.html:3469` | `// 1) btc.r7 одинаков для всех 28 карточек — это шум, а не информация;` | comment, universe count |
| `bench/catalyst_bench.js:35` | `// all 28 coins for fifteen days out of roughly forty-five.` | comment, universe count |
| `bench/backtest_bench.py:314` | `«какую из 28 взять», а не «куда пойдёт рынок».` | docstring, universe count |
| `bench/exhaustion_bench.js:408` | `eq('live shape: 28 rows, 25 counted', r.n, 25);` | fixture **label**; asserted value 25 is spot coverage and does not move |

The last row is inside step 12, which TZ-25 §5 lists as MUST NOT move. A label edit does
not change the check count (220 598 counts comparisons), but it is an edit to a pinned
bench and belongs in the same decision as obstacle 2.

**Would move but is forbidden — 2 sites (obstacle 3):**

| Site | Text | Conflict |
|---|---|---|
| `bench/exhaustion-calibration.txt:1` | `Universe: 25 spot of 28 declared tokens (fut:true excluded by declaration, inv. 41): HYPE, XMR, LIT` | universe count **and** stale `fut:true` enumeration; §4.4 forbids touching the file |
| `bench/exhaustion-calibration.txt:49` | `монет в кэше: 28 из 29` | record of a past calibration run, arguably historical and correctly frozen |

**Would move for a different reason — the futures count, not the universe count (obstacle 2):**

| Site | Text | Class |
|---|---|---|
| `index.html:2858` | `… по 25 спотовым монетам: **три фьючерсные** в меру не входят.` (`\uXXXX` escaped) | `fut:true` count 3 → 5; pinned by §2 |
| `bench/exhaustion_bench.js:1580–1583` (`const CAPTION`) | same sentence, character for character | section M expectation; pinned by §2 and §5 |
| `bench/exhaustion_bench.js:1587–1590` (`const CAPTION_MAIN`) | same trailing sentence | carried so M4 can restore `origin/main`'s caption |

**Inspected and NOT a universe count — unchanged, with the reason:**

| Site | Text | Why it does not move |
|---|---|---|
| `bench/direction_bench.py:679` | `def check_display(n=4000, coins=28)` | synthetic generator parameter; sizes a random display fixture, not the product universe. Changing it would alter a bench fixture with no product referent |
| `bench/backtest_bench.py:995` | `def synth(mode, n_coins=28, hours=8760, seed=3)` | synthetic self-check with a KNOWN answer (IC≈0 / >0 / <0); the coin count is a power parameter of the synthetic, independent of the live list |
| `bench/display_bench.py:136` | `k = rnd.randint(4, 28)` | upper bound of a random case size; a range, not a count of anything |
| `bench/catalyst_bench.js:577` | `min_price: 28.3` | a price. Not a count |
| `SYSTEM-MAP-CRYPTOCALCUL.md:815, 869, 1506` | `25 of 28` coverage statements | the map is Architect-owned and out of this TZ's scope entirely; listed so the Architect's own edit is not missed |
| `journal/write.js:548, 550, 708` | `P.tokens.length` | **derived, not hardcoded.** The journal needs no edit under §4.3 — it reads the universe from `tokens[]` at run time. Coverage becomes 25 of 30 automatically |
| `journal/README.md`, `journal/data/**`, `journal/out/**`, `journal/runs.jsonl` | — | no literal 28 as a universe count; journal records are immutable by inv. 38 in any case |

**Spot-coverage counts (25) — explicitly NOT universe counts, per §2, and none moves:**
`bench/exhaustion-calibration.txt:1` (`25 spot`), `bench/exhaustion_bench.js:408`
(asserted value), `bench/exhaustion_bench.js:1575` (`const COVER = '25 спотовым
монетам'`), `index.html:2858` (caption). This is TZ-25 §2's central claim and the survey
confirms it: **no site carrying 25 as a spot count requires an edit.** The declaration
did not leak into the spot universe. It leaked into the futures count.

---

## Commit

One commit, this report only, on the `CryptoReports/**` direct-push path (§8).

```
docs(reports): TZ-25 BLOCKED — hard floor item 3 conflict, §2 caption STOP (TZ-25)
```

TZ-25 specifies no `## Commit Message`, so no verbatim string was available to reuse; the
message above is this session's, and it is the report's own commit. Per contract §10 it
carries no hash, no conclusion and no push result: there is no implementation commit in
this session, and the report's own commit never satisfies the hash rule (inv. 54).

## Pull Request

**None, and this is not the report-only fixed line.** TZ-25 is a branch TZ (§4 names
files outside `CryptoReports/**`), so §8's branch clauses do have a referent — but the
implementation was never started, so there is no branch to push and no compare URL to
give. The section is written rather than omitted, per §10, because an absent section
cannot be told from a forgotten one.

Nothing awaits the Boss's merge. When TZ-25 is re-issued after the uploads named under
obstacle 1, the branch and the pull request arrive with that execution.

## CI Execution

**No workflow executed on a runner for this TZ, and none should have.** No branch was
pushed, so `bench.yml`'s `branches: [ main, 'claude/**' ]` had nothing to match. This
report's own push to `main` starts nothing: `bench.yml`'s `paths-ignore` carries `'**.md'`
and `main.yml`'s `paths` allow-list names only `main.py` and `.github/workflows/main.yml`
— both verified by reading the workflow files this session, recorded under
`## Validation`.

This is stated as a measurement of the filters, not as a forecast of a run. Per contract
§9 the status is **not** PARTIAL for the absence of CI: the work is not incomplete, it is
blocked before it starts, and there is nothing for a gate to measure.

## Final Repository State

The session leaves behind **no branch and no modified file**. The working tree is at
commit `7f8a30a1e0c1ec4af92215bd0468a36c3bc9560a`, byte-identical to `origin/main` as
measured before this report was written (`git diff --stat origin/main HEAD` → empty,
`git status --porcelain` → empty). That commit is what every fingerprint below was taken
against.

`TOKENS` stands at 28 and `tokens[]` stands at 28 with three `fut:true` rows, exactly as
hard floor item 3 and map inv. 2 require. TZ-25 is unexecuted, and
`CryptoTZ/TZ-25-universe-morpho-arb.md` stays in `CryptoTZ/` as the specification that
did not run — not a pending task, and not one this session may execute on its own reading
(contract §13).

## Fingerprints

Map, at the revision TZ-25's gate requires:

| File | Revision | Lines | MD5 |
|---|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | `Revision 2026-09-02-a` | 1841 | `03ec11fc16853947c83add15ca3e1ef8` |

Every file the map's `## 0` table lists, all four matching the required values exactly:

| File | Lines | MD5 | Required | Match |
|---|---:|---|---|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | 3729 / `fdf331906bf205944b25e3635135789c` | OK |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | 506 / `1a5a5d98b2fd76010f202ee3eebaa717` | OK |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | OK |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | OK |

Governing documents, added by this report because obstacle 1 is a claim about their
content and the Architect compares these against the Claude Project copies:

| File | Version | Lines | MD5 |
|---|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` | v18 | 780 | `3dd8d30b117df610b6dba7c0377ea16b` |
| `ANALYST-INSTRUCTIONS.md` | — | 1608 | `0ff09a55d2c726c9794af261c901a81a` |

TZ-25's gate table adds no file beyond the map's four.
