# Implementation Report — TZ-25 (report 2)

**This is the second report on TZ-25.** The first,
`CryptoReports/TZ-25-universe-morpho-arb-report.md`, returned **BLOCKED** on a hard
floor §7 item 3 conflict. It is immutable (§13) and stands; this report does not
supersede its findings, it records what happened after the block was lifted. Read it
first — its §4.3 enumeration and its analysis of the caption are not repeated here in
full.

**Previous TZ's branch: nothing to merge.** TZ-24 was report-only, no branch exists.
`claude/tz-20-catalyst-registry-content` is still not an ancestor of `origin/main` and
is still **declared dead** by the map's §10 table. This work was built on `main` at
`1d73267` and on nothing else.

---

## Status

**PARTIAL.**

Every edit TZ-25 §4 authorises is implemented, and every validation item in §6 that can
be run has been run and passes. **The 13-step gate does not pass: step 7
(`journal_bench.js`) reports 3 failures.** All three are stale expectations pinned to a
`fut:true` set of exactly three assets, none is a product defect, and **hard floor item
2 forbids this session from editing them** — as does TZ-25 §5's own sentence, "a bench
is never edited to make it pass."

The change is therefore **not mergeable as it stands**. It needs a one-paragraph
follow-up TZ authorising three assertion updates in `journal_bench.js` and the caption
repair carried over from report 1. Both are specified below, ready to approve.

---

## Inbound Filing

None. `CryptoTZ/TZ-25-universe-morpho-arb.md` was already at its canonical path. Nothing
was moved or renamed.

---

## Scope Executed

**TZ class: branch TZ** — TZ-25 §4 names `main.py`, `index.html` and `bench/**`, all
outside `CryptoReports/**`. Branch opened, pushed; no pull request (see
`## Pull Request`).

| TZ § | Scope item | Result |
|---|---|---|
| 4.1 | `main.py` `TOKENS` += MORPHO, ARB | done |
| 4.2 | `index.html` `tokens[]` += two `fut:true` rows | done |
| 4.3 | Hardcoded universe counts + full enumeration | done, enumeration below |
| 4.4 | Touch nothing else | honoured — `catalysts.json`, `analyst/**`, `bench/exhaustion-calibration.txt`, every threshold and every workflow are unmodified |

---

## The authority this change stands on — stated plainly, because it is not the usual one

Report 1 blocked on `EXECUTOR-INSTRUCTIONS.md` v18 §7 item 3, *"**No new coins.**
`TOKENS` (bot) and `tokens[]` (frontend) are frozen at 28 (inv. 2)"*, under a preamble
declaring the hard floor binding "regardless of what a TZ says".

**That block was lifted by the Boss in session, not by a contract upload.** He stated
that MORPHO and ARB are on his permanent list, reaffirmed the instruction after report 1
set out the conflict, and directed that TZ-25 be completed despite §7 item 3. He also
stated the instruction is not a request to change trading logic — and it was not treated
as one: no scoring weight, threshold, geometry or veto rule was touched.

**The Architect needs to know exactly what this means for the repository's standing, so
it is recorded rather than smoothed over:**

- `EXECUTOR-INSTRUCTIONS.md` on `main` is still **v18**, MD5
  `3dd8d30b117df610b6dba7c0377ea16b`, and its §7 item 3 still says 28.
- `SYSTEM-MAP-CRYPTOCALCUL.md` is still at revision **`2026-09-02-a`**, MD5
  `03ec11fc16853947c83add15ca3e1ef8`; inv. 2 (line 1210) still ends "(Standing decision:
  no new coins.)" and §1 line 161 still reads "**Universe: 28 pairs, frozen.**"
- So `main` now carries, on a branch awaiting merge, a 30-coin universe against a
  contract and a map that both say 28. **Three documents disagree with the code until
  the Architect uploads v19 and a new map revision.**

The repairs report 1 named are unchanged and still required: contract v19 amending item
3 (and item 11's "XMR, LIT and HYPE" enumeration, now five assets), and a map revision
amending inv. 2, §1 line 161, §3.14's venue set and the "25 of 28" statements at lines
815, 869 and 1506.

---

## Files Created

`CryptoReports/TZ-25-universe-morpho-arb-report-2.md` — this report. Per §13 the first
report was **not** overwritten.

## Files Modified

| File | Lines | + / − | What |
|---|---:|---|---|
| `main.py` | 518 | +13 / −1 | two `TOKENS` entries + declaration comment |
| `index.html` | 3736 | +11 / −4 | two `fut:true` `tokens[]` rows + comment; two universe-count comments |
| `bench/exhaustion_bench.js` | 1803 | +5 / −3 | C1.5 fixture now mirrors the live shape (25 spot + 5 fut) |
| `bench/catalyst_bench.js` | 614 | +1 / −1 | universe count in a comment |
| `bench/backtest_bench.py` | 1990 | +1 / −1 | universe count in a docstring |

Total diff: **31 insertions, 10 deletions across 5 files.**

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### `main.py` (§4.1)

`'MORPHO': 'morpho'` and `'ARB': 'arbitrum'` appended to `TOKENS`, following the file's
established pattern in which each addition carries a dated comment recording the running
call total. The comment states that the ids are the Architect's declaration, that the
arbiter is `debug.json` on a runner (`error: null`, `matched_90d > 120`), and that they
were **not** fetched in this session — inv. 44 and TZ-25 §4.1 both forbid it, and no
CoinGecko request was made at any point.

Per-run CoinGecko calls: **30 → 32** (BTC + 30 alts + one `/coins/markets`), recorded in
the comment as ~16.3k/month at 17 dispatches/day. No Demo key was attached; map §5's ban
is untouched.

The comment is English, matching the newer comments in the repository and the language
rule; the pre-existing Russian comments around it were left alone, and the historical
running-total line for the 2026-08-07 addition was **not** rewritten — it records what
the total was on that date, exactly as the 2026-07-29 BNB line above it does.

### `index.html` (§4.2)

Two rows appended to `tokens[]`, both `fut:true`, with the Binance USDⓈ-M perpetual pair
and display names `MORPHO` and `ARB`. Appended at the end, which is also what inv. 6
wants: new coins go to the end of the saved order.

**ES5 confirmed:** the added lines are object literals and comments — no `let`/`const`,
no arrow function, no template literal. `node --check` on the extracted `<script>` exits
0. No raw Cyrillic entered a JS string (hard floor 7): the new comment is English, and
no string literal was touched.

### Universe counts (§4.3)

Four sites updated, one bench fixture aligned. Full enumeration below, including every
site inspected and not changed.

---

## Validation

### §6.1 — `python3 -m py_compile main.py`

```
py_compile main.py: exit 0
```

### §6.2 — `node --check` on the extracted `<script>` of `index.html`

```
node --check index.html <script>: exit 0
```

### §6.3 — Full `bench.yml` gate, 13 steps, every delta attributed

Baseline is a pristine `origin/main` tree extracted to `/tmp/base` via `git archive`
(`index.html` MD5 `fdf331906bf205944b25e3635135789c`, matching the map's `## 0` table).
**The baseline total reproduces the map's published figure exactly — 1 250 739 — which
is what licenses every delta below.**

| # | Bench | Baseline | This branch | Δ | Fails |
|---:|---|---:|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 | 0 |
| 3 | `prot_bench.js index.html` | 372 | 372 | 0 | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 255 708 | 0 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 | 0 |
| 7 | `journal_bench.js` | 691 109 | 693 895 | **+2 786** | **3** |
| 8 | `catalyst_bench.js` | 23 062 | 24 692 | **+1 630** | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 | 0 |
| 10 | `render_bench.py` | 15 925 | 16 171 | **+246** | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 | 0 |
| 12 | `exhaustion_bench.js` | 220 598 | 220 598 | **0** | 0 |
| 13 | `live-gate.sh --selftest` | 40 | 40 | **0** | 0 |
| | **total** | **1 250 739** | **1 255 401** | **+4 662** | **3** |

Step 5 was run with `NODE_OPTIONS=--max-old-space-size=2600`, the documented ceiling of
this 955 MB VPS (map §10). That is a host property, not a product one.

#### Step 8 — +1 630, attributed term by term

TZ-25 §5 predicted **+4**. The prediction is wrong, and the reason is instructive: it
reused TZ-21's "+2 per-symbol" term, which was measured for a symbol that *also received
a registry entry*. A symbol added to `tokens[]` instead drives three sweeps that scale
with `SYMS.length`. Measured, not inferred:

| Term | Site | Formula | Δ |
|---|---|---|---:|
| Authority table | `catalyst_bench.js:427` | 400 days × **2** new symbols × 2 sides × 1 `deq` | **+1 600** |
| Silent-symbol sweep | `catalyst_bench.js:452–455` | `noSuch` 26 → 28, 1 `deq` each | **+2** |
| Degraded load | `catalyst_bench.js:564–567` | 7 `BAD` cases × **2** symbols × 2 `deq` | **+28** |
| | | | **+1 630** |

Corroborated by the bench's own printed counters: `calls: 22400 → 24000`, `symbols with
no entry stay silent: 26 → 28`, and the section header `400 days x 28 → 30 symbols`.

**A safety fact falls out of the same run:** `days a side was closed: 30` and `days a
side was annotated: 15` are **unchanged**. The two new coins have no `catalysts.json`
entry (§4.4 forbids adding one), so they can neither veto nor annotate a side. The trust
root of inv. 39 is untouched.

#### Step 7 — +2 786, attributed term by term

Measured by instrumenting a **scratch copy** of the bench in `/tmp` (the repository bench
was not modified) to print running check totals per section:

| Term | Where | Measurement | Δ |
|---|---|---|---:|
| Declared-skip records | section 7 | `x` rows 884 → 1 428 (+544), 5 checks each — parse · known `k` · key set · date · `why` in dictionary; `walk` adds nothing because every `x` field is a string | **+2 720** |
| Verdict-content drift | section 7 | `s` rows unchanged at 6 743, cost 490 188 → 490 252 | **+64** |
| Declared-venue note | section 6a | `FUT.forEach` note assertion, one `ok` per fut asset, 3 → 5 | **+2** |
| | | | **+2 786** |

The +64 is the only term that is not structural, so it is pinned down rather than waved
at. `makeDay` (line 102) draws every fixture row from **one** seeded RNG and makes **two**
`P.tokens.forEach` passes over it. The two new tokens are appended, so the first pass
reproduces the old draws and then consumes two more — which shifts the stream the second
(ticker) pass reads. Verdict content therefore moves for pre-existing coins: 2 349 `s`
rows changed cost, **in both directions**, netting +64. Row-kind census confirms nothing
else moved:

```
base {"s":6743,"x":884, "r":258,"g":8,"oh":10,"o":34}
new  {"s":6743,"x":1428,"r":258,"g":8,"oh":10,"o":34}
```

This is exactly the content-sensitivity the map's `## 0` names for step 7 ("moves with
verdict CONTENT, not only with control volume… a fall is attributed, never assumed
benign") and that TZ-25 §5 predicted. It is a fixture-generator artifact, not a product
change — the product's own outputs for pre-existing coins are proved byte-identical under
§6.4 below.

#### Step 10 — +246, attributed

`render_bench.py` runs 123 scenarios (unchanged). The rank-order loop at line 315–317
does one `checks += 1` per shown, scored, on-side row. Two added cards × 123 scenarios =
**+246**. This also confirms the two coins are scored and rendered rather than silently
dropped.

#### Steps 12 and 13 — held, as §5 requires

Step 12 is **220 598, unmoved**, and step 13 is **40, unmoved**. Step 12 was measured
twice on purpose: once after the product edits and before the C1.5 fixture edit
(220 598), and once after (220 598). The fixture gained two rows, not two comparisons —
which is why §5's "MUST NOT move" and §4.3's "update universe counts" do not collide
here.

#### Step 7's three failures — the gate is RED

```
FAIL fut:true активов ровно три: got false want true
FAIL три формы: жива: got 3 want 1
FAIL три формы: note ровно про живую:
     got  "fut:true asset trading on spot: LIT; ...: MORPHO; ...: ARB"
     want "fut:true asset trading on spot: LIT"
```

**All three are stale expectations. None is a product defect**, and the same bench run
proves it in its own output: `монет 30`, `cov 25 skip 5`, `статус ok`. Coverage is 25 of
30 exactly as TZ-25 §2 requires, and **neither new coin raises `hardSkip`** — the venue
test short-circuits ahead of the degradation ladder, which is the §2 promise that
mattered most.

What each failure actually is:

1. `journal_bench.js:592` — `ok('fut:true активов ровно три', FUT.length === 3)`. A
   hardcoded venue-set size. The declared set is now five.
2. `journal_bench.js:641` — `eq('три формы: жива', whyCount(r, ALIVE), 1)`. Fixture 6a.5
   kills `FUT[0]` and drops `FUT[1]`, so the correct expectation is structurally
   `FUT.length - 2`: it was 1 at three assets and is 3 at five.
3. `journal_bench.js:644–645` — expects the run note to name exactly `FUT[2].name`. With
   five assets the note correctly names all three that are alive.

**Why this session did not repair them.** Hard floor item 2: *"Never edit a bench to make
it pass. A red bench is either a product defect or a stale expectation; **both are
findings**, neither is a licence to change the assertion."* TZ-25 §5 says the same in its
own words. §4.3's authorisation is explicitly scoped to sites carrying **the literal 28**
as a universe count, and none of these three does. Two of them are not count updates at
all — they require re-deriving an expectation from the fixture's construction and
composing a new multi-symbol expected string, which is authoring assertions, i.e. the
"corrective architectural change" §12 forbids improvising.

The Boss's instruction lifted §7 item 3 and named no other clause; extending it to item 2
would be this session deciding the scope of its own permission.

**The repair, ready to approve** — three edits, no new logic:

```js
// journal_bench.js:592
ok('fut:true активов ровно пять', FUT.length === 5);
// journal_bench.js:641   (6a.5 kills FUT[0] and drops FUT[1])
eq('три формы: жива', whyCount(r, ALIVE), FUT.length - 2);
// journal_bench.js:644
eq('три формы: note ровно про живых', r.run.note,
   FUT.slice(2).map(function (t) { return 'fut:true asset trading on spot: ' + t.name; }).join('; '));
```

Deriving #2 and #3 from `FUT` rather than re-hardcoding them means the next venue change
moves no expectation at all. #1 must stay a literal — deriving it would make it assert
`FUT.length === FUT.length` and control nothing.

### §6.4 — Two-way compatibility against an OLD `coeffs.json` (inv. 1, inv. 9)

Executed, not asserted. `render_bench.py`'s own recording DOM harness was driven from a
scratch script against **both** trees with an identical case: a book of **28** symbols
carrying no `MORPHO` and no `ARB` row (it also carries `DOGE`, which is in no `tokens[]`
— the mismatch is deliberate in that fixture).

```
book symbols: 28 | MORPHO in book: False | ARB in book: False

--- scenario seed4242-long ---
  cards: base 28 -> new 30
  added cards: ['ARB', 'MORPHO']
     ARB     state=nopair  score=None  no=0  off=False  action=None
     MORPHO  state=nopair  score=None  no=0  off=False  action=None
  pre-existing cards that CHANGED: none
  boards compared: 9 common, byte-differences: 0

--- scenario seed4242-short ---   (same result, 10 boards compared)
RESULT: PASS
```

**Stated explicitly, as §6.4 requires:** the frontend running against an old
`coeffs.json` with no rows for the two new coins renders those two cards as a protective
no-data state — `state=nopair`, no score, no rank, no action, so they cannot enter the
board or take a number — and **every other card is unchanged**, byte-for-byte, including
every rendered board's HTML. The frontend survives the absence of the rows exactly as
inv. 9 requires.

### §6.5 — Spot ticker unchanged (inv. 12)

`marketTickerUrl()` called on both trees:

```
base(28): 26 symbols, url 481 bytes | MORPHOUSDT false | ARBUSDT false | full-ticker fallback: false
new(30):  26 symbols, url 481 bytes | MORPHOUSDT false | ARBUSDT false | full-ticker fallback: false
```

**The spot request is byte-identical to `main`'s.** Adding two coins changed it by zero
bytes, neither new symbol appears in `?symbols=`, and there is no fall-back to the 1.2 MB
full ticker. TZ-25 §6.5 calls this "the check that proves the declaration reached the
code", and it does: `marketTickerUrl()` skips `fut:true` at `index.html:874`, so an
unconfirmed spot symbol can never reach the request that HTTP 400 would kill (inv. 5).

### §6.6 — Venue path (inv. 41)

`refreshFuturesTickers()` called with a recording `fetch` stub:

```
fut:true tokens (5): HYPE, XMR, LIT, MORPHO, ARB
  https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=HYPEUSDT
  https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=XMRUSDT
  https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=LITUSDT
  https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=MORPHOUSDT
  https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=ARBUSDT
```

Both new coins issue their own `fapi` request and are read back from `cachedFutTickers`
at `index.html:3246–3247`. The dead-market detector works on `count` alone for them, the
same branch XMR/LIT/HYPE already take.

### §6.7 — `listExhaustion` universe unchanged

A full board, one row per real `tokens[]` entry, rows built from the production
`sigmaDay` so the fixture cannot drift from the measure it feeds:

```
tokens[] = 30  (spot 25 + fut 5)
full board rows fed to listExhaustion: 30
listExhaustion n      = 25   (must be 25, NOT 27 and NOT 30)
listExhaustion median = 1.1000000000000008
RESULT: PASS
```

The day-range measure still counts **25** rows on a full board. `DAY_RANGE_ABNORMAL =
1.39` is therefore not re-opened, `bench/exhaustion-calibration.txt` is untouched (MD5
`3b8730b254467c9df4c0a845a0f3cfb3`, unchanged), and gate step 12's inv. 46 comparison
stays green.

*(An earlier attempt at this check returned `n = 0` because the fixture used `px.hi/px.lo`
instead of the `hi24/lo24/cd.volatility` shape the measure consumes. That was a defective
instrument, not a product reading; it is recorded because a validator that passes with no
data is a failed validator (inv. 22), and one that fails with malformed data must not be
reported as a product failure either.)*

### §6.8 — No-regression statement

- `main.py` — only `TOKENS` gained entries. No function, constant, threshold or request
  shape changed. `py_compile` exit 0. The bot's `err_result` remains key-synchronous with
  its success result (inv. 1); nothing in this diff touches either.
- `index.html` — `tokens[]` gained two rows; two comments changed a number. No function
  body, no string literal, no threshold, no `scoreCandidate` weight, no geometry. Steps
  1, 2, 3, 9, 10, 11 all hold at their baseline counts with 0 failures, and §6.4 proves
  every pre-existing card and board renders byte-identically.
- `bench/catalyst_bench.js`, `bench/backtest_bench.py` — comment/docstring text only; no
  assertion added, removed or altered. Step 8's every delta is attributed to `tokens[]`
  growth, not to the comment.
- `bench/exhaustion_bench.js` — C1.5 fixture only. Step 12 holds at 220 598 with 0
  failures, measured before and after the edit.
- Untouched and verified by MD5: `catalysts.json`
  (`f9b2dd4a3594134b2b7b603de19075c3`), `bench/exhaustion-calibration.txt`
  (`3b8730b254467c9df4c0a845a0f3cfb3`), every workflow, all of `analyst/**`.

### Note carried from TZ-25 §6

`bench/backtest_bench.py` is outside `bench.yml` (it needs the external archive and a warm
cache) and was not run. If it cannot build a three-year archive for MORPHO, TZ-25 fixes
the standing in advance: that is `GRAM`'s case per map §3.16 — record it, do not repair
it.

---

## Test Results

**12 of 13 gate steps green; step 7 RED with 3 failures.** Totals, counts and attribution
in the §6.3 table above. 1 255 401 checks executed, 3 failing, every one of them a
`fut:true`-count expectation in `journal_bench.js`.

Every validation item §6 lists was run. None was skipped and none was marked "not
applicable".

---

## Deviations

**One, and it is the reason `## Status` is PARTIAL rather than COMPLETED.**

TZ-25 §2 instructs: *"If any of the four sites above requires an edit, STOP and report."*
Report 1 established that one pinned site — the §3.17 caption, pinned character-for-
character by `exhaustion_bench.js` section M — **does** require an edit, because it ends
«Список считается по 25 спотовым монетам: **три фьючерсные** в меру не входят» and the
futures count moves 3 → 5. Under §2 as written, this TZ stops there.

It did not stop, because the Boss directed that TZ-25 be completed. The consequence is
recorded rather than hidden: **`index.html` on this branch ships a caption asserting that
three futures assets are excluded from the day-range measure, while five are**, and
`exhaustion_bench.js` section M pins that sentence and passes — a green control standing
over a wrong string.

The caption was **not** repaired here. Repairing it means editing `index.html` beyond
`tokens[]` (§4.2 forbids), and editing the section M expectation (§2 and §5 forbid). Note
also that §2's stated diagnosis does not fit: the declaration did **not** leak into the
spot universe — the spot count 25 is correct everywhere and §2's protective argument
holds in full. It leaked into the *futures* count that shares the sentence, which §2's
enumeration does not cover.

The repair needs one line in each of two files, and belongs in the same follow-up TZ as
the three `journal_bench.js` assertions:

```
Список считается по 25 спотовым монетам: пять фьючерсных в меру не входят.
```

(as `\uXXXX` escapes in `index.html:2865`, and verbatim in `exhaustion_bench.js`'s
`CAPTION`. `CAPTION_MAIN` at line 1589 is `origin/main`'s caption, carried so M4 can
restore it — whether it also moves is the Architect's call, since it is a record of what
`main` said, not a claim about what production should say.)

---

## Pre-existing Issues

1. **The `fut:true` count is hardcoded in prose and in assertions, and derived nowhere.**
   This single defect produced *all three* step-7 failures and the caption problem. It
   lives at `index.html:2865` («три фьючерсные»), `journal_bench.js:592, 641, 644`,
   `exhaustion_bench.js:1582` and `bench/exhaustion-calibration.txt:1` («HYPE, XMR,
   LIT»). `journal/write.js` shows how it should be done — it derives everything from
   `P.tokens.length` and needed no edit under §4.3. Pre-existing; TZ-25 is the first
   change that makes it bite. Map inv. 58 — "a rule that names an object without naming
   how to compute it has named nothing" — is exactly this.
2. **TZ-25 §5's step-8 prediction was wrong** (+4 predicted, +1 630 measured), because it
   reused TZ-21's per-symbol term, which was measured for a symbol that also gained a
   registry entry. Recorded so the attribution above, not the prediction, is what a
   future TZ cites.
3. **`claude/tz-20-catalyst-registry-content` is still unmerged** and still declared
   dead. Restated per §8's previous-branch requirement.

---

## Remaining Risks

1. **The gate is red, so this branch must not be merged until the follow-up TZ lands.**
   Merging as-is puts a failing `bench.yml` on `main`.
2. **Three documents disagree with the code until v19 and a new map revision arrive.**
   Detailed above under "The authority this change stands on".
3. **The two CoinGecko ids are unvalidated.** `morpho` and `arbitrum` are the Architect's
   declaration and were deliberately not fetched (inv. 44). The arbiter is `debug.json`
   after the first bot run on a runner: `error: null` and `matched_90d > 120` on both. If
   either returns an error, TZ-25 §4.1 fixes the remedy — a one-line follow-up, not an
   amendment to this work.
4. **`bench/exhaustion-calibration.txt:1` now understates the universe** — it reads
   "25 spot of 28 declared tokens … : HYPE, XMR, LIT". §4.4 forbade touching it, so it
   was not touched. The calibrated content (1.39, the 25-coin basis) is still correct;
   only the descriptive header is stale.
5. **`render_bench.py`'s `SYMS` fixture is a 28-symbol book containing `DOGE`.** It is not
   a count of `tokens[]` and correctly did not move — the mismatch is the point of the
   fixture, and it is what made the §6.4 evidence available for free. Named so a future
   sweep does not "fix" it.

---

## §4.3 enumeration — every site inspected

**Changed (universe counts of `tokens[]`, 28 → 30):**

| Site | Change |
|---|---|
| `index.html:3347` | `Босс видел 28` → `30` |
| `index.html:3348` | `вместо 28 раз внутри` → `30` |
| `index.html:3476` | `для всех 28 карточек` → `30` |
| `bench/catalyst_bench.js:35` | `all 28 coins` → `all 30 coins` |
| `bench/backtest_bench.py:314` | `«какую из 28 взять»` → `«какую из 30 взять»` |
| `bench/exhaustion_bench.js:403–408` | C1.5 fixture `25 spot + 3 fut` → `25 spot + 5 fut`; label `28 rows` → `30 rows`. Asserted value stays 25. Step 12 verified unmoved at 220 598 before and after |

**Inspected, NOT changed, with the reason:**

| Site | Why it does not move |
|---|---|
| `bench/exhaustion-calibration.txt:1, :49` | §4.4 forbids touching the file. Carries `of 28 declared tokens` and `HYPE, XMR, LIT` — both stale; see Remaining Risk 4 |
| `index.html:2865` · `exhaustion_bench.js:1582, 1589` | the caption. Not a `tokens[]` count — a `fut:true` count. Pinned by §2/§5; see `## Deviations` |
| `journal_bench.js:592, 641, 644` | `fut:true` count expectations. Not the literal 28, so outside §4.3; hard floor item 2 forbids editing. See §6.3 |
| `bench/direction_bench.py:679` | `coins=28` — synthetic display-fixture parameter, no product referent |
| `bench/backtest_bench.py:995` | `n_coins=28` — power parameter of a synthetic with a known answer |
| `bench/display_bench.py:136` | `rnd.randint(4, 28)` — upper bound of a random case size |
| `bench/catalyst_bench.js:577` | `min_price: 28.3` — a price |
| `render_bench.py` `SYMS` | 28-symbol book incl. `DOGE`; a deliberate mismatch fixture, not a universe count |
| `index.html:223, 484` | `28px` — CSS |
| `index.html:649` | `XMR 1.28%` — a percentage |
| `main.py:52` | historical running total for the 2026-08-07 addition, matching the 2026-07-29 pattern above it |
| `journal/write.js:548, 550, 708` · `journal/README.md` · `journal/data/**`, `out/**`, `runs.jsonl` | **derived** from `P.tokens.length`; journal needed no edit at all. Coverage became 25 of 30 automatically — measured: `монет 30`, `cov 25 skip 5` |
| `SYSTEM-MAP-CRYPTOCALCUL.md:815, 869, 1506` | Architect-owned, outside this TZ's scope; listed so the map edit is not missed |

**Spot-coverage counts (25) — none moved**, confirming §2's central claim: no site
carrying 25 as a spot count required an edit.

---

## Commit

Implementation, on `claude/tz-25-universe-morpho-arb`, pushed:

```
ea0596232d8a3c9a8fe1c39b86d34c5c58385cbb
feat(universe): add MORPHO and ARB as declared futures-only (TZ-25)
```

Contents: `main.py`, `index.html`, `bench/exhaustion_bench.js`,
`bench/catalyst_bench.js`, `bench/backtest_bench.py` — 31 insertions, 10 deletions. The
hash is a measurement: the commit existed and was pushed before this section was written.

This report's own commit carries no hash, no conclusion and no push result (inv. 54):

```
docs(reports): TZ-25 report 2 — implemented, gate red at step 7 (TZ-25)
```

## Pull Request

**No pull request exists, and the reason is environmental, not a refusal.** The `gh` CLI
is not installed in this session and no GitHub API credential is available, so this
session cannot open one. Per §8 the fallback is taken rather than stopping:

- Branch: **`claude/tz-25-universe-morpho-arb`** (pushed, head `ea05962`)
- Compare URL:
  **`https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-25-universe-morpho-arb`**

**The Boss must not merge this branch yet.** The gate is red at step 7 and the
Architect's verdict precedes any merge in every case.

## CI Execution

**Not readable from this session.** No `gh`, no token — so what happened on GitHub is not
reported here in either direction (§9).

What **is** established: the branch reached the remote, and `bench.yml` triggers on
`push` to `branches: [ main, 'claude/**' ]`, which `claude/tz-25-universe-morpho-arb`
matches. None of the five changed paths appears in that workflow's `paths-ignore`
(`journal/data/**`, `journal/out/**`, `journal/runs.jsonl`, `analyst/state.json`,
`analyst/live.json`, `analyst/log/**`, `**.md`).

The hosted gate is read by the audit. What this session measured locally, on the same 13
commands `bench.yml` runs, is the table in §6.3: **12 steps green, step 7 red with 3
failures.** A local run is not a runner run, and the two are not conflated here — but the
red step is a product of the assertions themselves and will reproduce on any host.

`main.yml` was checked before the report push: its `push` filter is still a `paths`
allow-list of `'main.py'` and `'.github/workflows/main.yml'` only. **`main.py` is on that
list**, so the bot would start on a merge to `main` — correctly, since the bot's token
list is exactly what changed. Nothing in this session pushed `main.py` to `main`; it is
on the branch, behind the Boss's merge.

## Final Repository State

The session leaves behind the branch **`claude/tz-25-universe-morpho-arb`** at
`ea0596232d8a3c9a8fe1c39b86d34c5c58385cbb`, pushed before this report was written and
therefore measured. It carries five modified files, 31 insertions and 10 deletions, and
nothing else; the working tree is clean apart from gitignored scratch (`bench/_*`,
`__pycache__/`), which is never committed.

**NOT IN EFFECT UNTIL MERGED.**

`TOKENS` and `tokens[]` stand at **30** on the branch and at **28** on `main`. The spot
universe is 25 in both.

## Fingerprints

Map, at the revision TZ-25's gate requires — anchors all seven matched, revision string
matched:

| File | Revision | Lines | MD5 |
|---|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | `Revision 2026-09-02-a` | 1841 | `03ec11fc16853947c83add15ca3e1ef8` |

Files the map's `## 0` table lists — **required** values are the map's, **branch** values
are this branch's:

| File | Required (lines / MD5) | On this branch | State |
|---|---|---|---|
| `index.html` | 3729 / `fdf331906bf205944b25e3635135789c` | 3736 / `7e67821c45e47b8c35b987eaaaf62596` | **changed by this TZ** |
| `main.py` | 506 / `1a5a5d98b2fd76010f202ee3eebaa717` | 518 / `0e3ead8c300d2ee6783303c4bf2fb6b5` | **changed by this TZ** |
| `catalysts.json` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | unchanged |
| `bench/exhaustion-calibration.txt` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | unchanged |

Both fingerprints matched the map exactly **before** work began (recorded in report 1);
the two differences above are this TZ's own diff, and the map's `## 0` table needs the
new values at the next revision.

Benches this TZ touched, added because the gate table depends on them:

| File | Lines | MD5 |
|---|---:|---|
| `bench/catalyst_bench.js` | 614 | `12b4f5b29299b90b4eec6d7376bc6a7e` |
| `bench/exhaustion_bench.js` | 1803 | `ae7828eae9b77b64fb62632fa71c9a0b` |
| `bench/backtest_bench.py` | 1990 | `f1ba588949978952def15da3a1c22a04` |

Governing documents, carried because this report makes claims about their content:

| File | Version | Lines | MD5 |
|---|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` | v18 | 780 | `3dd8d30b117df610b6dba7c0377ea16b` |
| `ANALYST-INSTRUCTIONS.md` | — | 1608 | `0ff09a55d2c726c9794af261c901a81a` |
