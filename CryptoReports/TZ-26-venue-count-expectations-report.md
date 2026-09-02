# Implementation Report — TZ-26

**The previous TZ's branch is not merged, and that is by design here.** TZ-26 declares
itself a continuation of `claude/tz-25-universe-morpho-arb` at head `ea05962` — no new
branch, one pull request for TZ-25 and TZ-26 together. The branch was at exactly
`ea05962` when this session started (verified below) and is not an ancestor of
`origin/main`. `claude/tz-20-catalyst-registry-content` is still unmerged and still
**declared dead** by the map's §10 table; nothing in this TZ touches it.

**Contract version, checked first because TZ-26 §1 makes it a stop condition.**
`EXECUTOR-INSTRUCTIONS.md` on `origin/main` is **v19** (801 lines, MD5
`a6ebc2e7c2f2b74e813dfdc20400558f`), carrying the item 3 and item 11 text this work
stands on. Not BLOCKED.

---

## Status

**COMPLETED.**

Every edit TZ-26 §2 authorises is implemented and every validation item §4 lists was
run and passes. **The 13-step gate is green: 1 255 401 checks, 0 failures**, which is
the figure and the outcome §3 predicted. The three step-7 failures report 2 recorded
are gone, and no other step moved by a single check.

---

## Inbound Filing

None. `CryptoTZ/TZ-26-venue-count-expectations.md` arrived on `origin/main` at its own
canonical path in commit `e6cc145`, under the exact filename its header states. Nothing
was moved, renamed or `git mv`-ed.

---

## Scope Executed

**TZ class: branch TZ** — §2 names `bench/journal_bench.js`, `index.html` and
`bench/exhaustion_bench.js`, all outside `CryptoReports/**`. No new branch was opened;
the commit continues the existing one, as §0 of the TZ requires.

| TZ § | Scope item | Result |
|---|---|---|
| 2.1 | `journal_bench.js` — three stale expectations at 592, 641, 644–645 | done |
| 2.2 | The §3.17 caption — one sentence, two files, byte-identical | done |
| 2.2 | `CAPTION_MAIN` at `exhaustion_bench.js:1589` **not** edited | honoured, proved by hash |
| 2.3 | `bench/exhaustion-calibration.txt` **not** edited | honoured, proved by hash |
| 2.4 | Nothing else | honoured — no `tokens[]`, no `TOKENS`, no threshold, no workflow, no `analyst/**`, no `catalysts.json`, no other assertion in any bench |

---

## The licence this change stands on, and the check it is conditional upon

Hard floor item 2 forbids editing a bench to make it pass. **TZ-26 §1 is the licence**,
and it is conditional: *"If any of the three turns out to be a product defect on
inspection, STOP and report."* The condition was tested before a line was edited, on
the baseline run of the unmodified branch, and each of the three was traced to the
production source rather than assumed:

| Site | What it asserts | Product behaviour, traced | Verdict |
|---|---|---|---|
| `journal_bench.js:592` | `FUT.length === 3` | `tokens[]` declares five `fut:true` rows. Hard floor item 11 (v19): the declared set **is** whatever carries `fut:true` in `tokens[]` | stale expectation |
| `journal_bench.js:641` | `whyCount(r, ALIVE) === 1` | fixture 6a.5 kills `FUT[0]` and drops `FUT[1]`; `journal/write.js` `buildDay` (line 415–447) pushes one `alive` entry per remaining `fut:true` asset, so the correct value is structurally `FUT.length - 2` = 3, and 3 is what the product returned | stale expectation |
| `journal_bench.js:644–645` | note names exactly `FUT[2].name` | `write.js:563–567` pushes one line per `alive` symbol, in `tokens[]` order, and joins with `'; '`. The product's note named all three alive assets — correctly | stale expectation |

The same baseline run prints the positive proof in its own output: `монет 30`,
`cov 25 skip 5`, `статус ok`. **No product defect was found, so the licence applies and
the work proceeded.** Had any of the three been a product defect, this report would be
BLOCKED instead.

---

## Files Created

`CryptoReports/TZ-26-venue-count-expectations-report.md` — this report. No earlier
report was overwritten (§13); TZ-25's two reports stand untouched.

## Files Modified

| File | Lines | + / − | What |
|---|---:|---|---|
| `bench/journal_bench.js` | 967 | +13 / −4 | three expectations at 592, 641, 644–645, plus two explanatory comments |
| `index.html` | 3736 | +1 / −1 | the §3.17 caption's last clause |
| `bench/exhaustion_bench.js` | 1803 | +1 / −1 | the `CAPTION` constant's last clause |

Total diff: **15 insertions, 6 deletions across 3 files.**

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### `journal_bench.js:592` — the literal, and why it stays one (§2.1)

```js
// The number is hand-written ON PURPOSE. Derived from FUT it would read
// FUT.length === FUT.length and control nothing (inv. 22); this is the one
// site in 6a that must move when the declared venue set moves.
ok('fut:true активов ровно пять', FUT.length === 5);
```

The Russian label moved with the number it asserts, as §2.1's closing sentence
requires: a label reading «ровно три» over an assertion of five is the same defect in
prose. The comment is English, per the contract's language rule, whose exception list
covers `.github/workflows/**` and not benches; the check label stays Russian because it
is a quoted label and because §2.1 names it as one.

### `journal_bench.js:641` and `644–645` — derived, so the next venue change moves nothing

```js
eq('три формы: жива', whyCount(r, ALIVE), FUT.length - 2);
...
eq('три формы: note ровно про живых', r.run.note,
   FUT.slice(2).map(function (t) {
       return 'fut:true asset trading on spot: ' + t.name;
   }).join('; '));
```

Both are consequences of the fixture's own construction, exactly as §2.1 states, and
both are now written as that consequence rather than as its current value. The join
separator `'; '` is not a guess: it is read off `journal/write.js:567`
(`notes.join('; ')`), and the per-entry prefix off line 565.

**One label moved beyond the number.** `'три формы: note ровно про живую'` became
`'…про живых'` — singular to plural. It is named here rather than folded into the diff
because §2.1's label sentence speaks of the check that asserts a number, and this one
asserts a string. It is the wording report 2 proposed in the finding TZ-26 §1 cites as
its licence, it is inside the authorised site, and left alone it would have described
one alive asset while checking three. `'три формы'` itself was **not** touched anywhere:
it names the three FORMS of a declared skip — no pair · delisted · alive — and not a
count of assets.

### The caption (§2.2)

`index.html:2865` and `exhaustion_bench.js`'s `CAPTION` both now end:

```
Список считается по 25 спотовым монетам: пять фьючерсных в меру не входят.
```

In `index.html` the change is `три фьючерсные`
→ `пять фьючерсных`.
**Hard floor 7 held:** line 2865 contains zero raw Cyrillic bytes after the edit
(`sed -n '2865p' index.html | grep -c $'[Ѐ-ӿ]'` → `0`). The spot count 25 did not move
and was not touched, in either file.

**`CAPTION_MAIN` was not edited**, and this is proved rather than asserted:

```
$ git show ea05962:bench/exhaustion_bench.js | sed -n '1589,1592p' | md5sum
28f23b9564bfa1924826c5db3226c4fe  -
$ git show 69bddc3:bench/exhaustion_bench.js | sed -n '1589,1592p' | md5sum
28f23b9564bfa1924826c5db3226c4fe  -
$ git diff ea05962 69bddc3 -- bench/exhaustion_bench.js | grep -c CAPTION_MAIN
0
```

Section M's control derives its value from `CAPTION_MAIN` differing from the live
caption; the two now differ in two sentences instead of one, and M4 still fires naming
exactly the two denials `origin/main`'s caption carried.

### `bench/exhaustion-calibration.txt` — not edited (§2.3)

Untouched across both commits of this branch:

```
$ git show 1d73267:bench/exhaustion-calibration.txt | md5sum   3b8730b254467c9df4c0a845a0f3cfb3
$ git show 69bddc3:bench/exhaustion-calibration.txt | md5sum   3b8730b254467c9df4c0a845a0f3cfb3
```

TZ-25 §4.3 and §4.4 collided over this file; §2.3 resolves the collision in favour of
§4.4 and this session implemented that resolution and nothing else. Gate step 12's
inv. 46 comparison is therefore unmoved, and the record still describes the run that
produced it.

---

## Validation

Every item TZ-26 §4 lists was run. None was skipped and none was marked "not
applicable".

### §4.1 — `node --check` on the extracted `<script>` of `index.html`

```
$ python3 -c "…extract the single <script> block…" > /tmp/_script.js
$ wc -l /tmp/_script.js        3167
$ node --check /tmp/_script.js ; echo exit=$?
exit=0
```

`index.html` carries exactly one `<script>` opener, so the extraction is unambiguous.

### §4.2 — `python3 -m py_compile main.py`

```
$ python3 -m py_compile main.py ; echo exit=$?
exit=0
```

`main.py` is unchanged by TZ-26 (it is TZ-25's file on this branch); this is the
no-regression check §4.2 asks for, and it passes.

### §4.3 — Full `bench.yml` gate, 13 steps, every delta attributed

Both runs are local replays of the workflow's own 13 commands, in the workflow's order,
on this VPS. The **baseline** is the branch at `ea05962` extracted with `git archive`
into `/tmp/base`; the **change** is the working tree at `69bddc3` in `/tmp/new`. The
baseline reproduces report 2's published branch table exactly, which is what licenses
every number in the Δ column.

| # | Bench | Baseline `ea05962` | This change `69bddc3` | Δ | Fails before | Fails now |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 | 0 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 | 0 | 0 |
| 3 | `prot_bench.js index.html` | 372 | 372 | 0 | 0 | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 | 0 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 255 708 | 0 | 0 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 | 0 | 0 |
| 7 | `journal_bench.js` | 693 895 | **693 895** | **0** | **3** | **0** |
| 8 | `catalyst_bench.js` | 24 692 | 24 692 | 0 | 0 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 | 0 | 0 |
| 10 | `render_bench.py` | 16 171 | 16 171 | 0 | 0 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 | 0 | 0 |
| 12 | `exhaustion_bench.js` | 220 598 | **220 598** | **0** | 0 | 0 |
| 13 | `live-gate.sh --selftest` | 40 | 40 | 0 | 0 | 0 |
| | **total** | **1 255 401** | **1 255 401** | **0** | **3** | **0** |

All thirteen steps exit 0 on the changed tree; step 7 exited 1 on the baseline.

#### Attribution: why the total is unmoved, term by term

§3 predicted step 7 at 693 895 / 0 and step 12 at 220 598 / 0, and both are measured at
exactly that. The prediction holds for a reason that is stated rather than assumed: a
check count is a count of COMPARISONS (inv. 43), and all three journal sites and the one
caption site compare the same number of times as before — only the expected values moved.

- **Step 7, +0.** Three `eq`/`ok` calls in, three out. `ok` is `eq(name, !!cond, true)`,
  so 592 is one comparison before and after; 641 is one; 644 is one, whether its
  expected string is built from `FUT[2].name` or from `FUT.slice(2)`. The `.map` and
  `.join` run inside the argument and increment no counter.
- **Step 12, +0.** Section M pins one exact string in `M2` (two renders) and substitutes
  it in `M4`; changing that string's CONTENT changes no comparison. The `caption`
  section counter reads **64** on both runs, and the bench's own `SUM === checks`
  self-check passes on both.
- **Steps 1–6 and 8–13, +0.** None of them reads the caption or the venue-count
  assertions.

#### Everything that differs in the two gates' output, line by line

The two 13-step runs produce byte-identical logs except in four places. This is stated
exhaustively because a step-7 fall must be attributed and never assumed benign (map
`## 0`):

| Step | Difference | Attribution |
|---|---|---|
| 7 | `движок e25adf323f9bddc4` → `00bbe48d546c1ad1` | the bench hashes the engine it cut out of `index.html`; the caption is inside that block. A content hash moving when content moves is the control working |
| 7 | three `FAIL` lines gone | the three repaired expectations |
| 7 | `провалов: 3` → `провалов: 0` | same |
| 12 | the printed `caption:` line | the repaired sentence |
| 13 | `/tmp/tmp.rMfN2buQiX/` → `/tmp/tmp.qspL1rTxqS/` | the selftest's own mktemp directory. A host artefact, not a product difference |

Steps 1, 2, 3, 4, 5, 6, 8, 9, 10, 11 produce **zero** differing lines.

### §4.4 — The caption is byte-identical in the two files, proved by comparison

Not read — compared, programmatically, decoding `index.html`'s escapes and evaluating
`exhaustion_bench.js`'s `CAPTION` in a VM context. The command is recorded because §4.4
requires it:

```js
$ node <<'JS'
const fs = require('fs'), vm = require('vm'), crypto = require('crypto');
const html = fs.readFileSync('index.html', 'utf8');
const line = html.split('\n').filter(l => l.indexOf('bd-note') > 0
                                       && l.indexOf('\\u0431\\u043b\\u0443\\u0436\\u0434') > 0);
const src = line[0].slice(line[0].indexOf('bd-note">') + 9, line[0].indexOf('</div>'));
const fromHtml = src.replace(/\\u([0-9a-fA-F]{4})/g, (_, h) => String.fromCharCode(parseInt(h, 16)));
const bench = fs.readFileSync('bench/exhaustion_bench.js', 'utf8');
const decl = bench.slice(bench.indexOf('const CAPTION ='));
const fromBench = vm.runInNewContext(decl.slice(0, decl.indexOf(";\n") + 1) + '\nCAPTION;');
// … Buffer.compare + sha256 of both …
JS
```

```
index.html            bytes=624 sha256=c50601bba0c696dcc0a00de5a3e0d9940801bfe18f778275f02db177e7234efa
exhaustion_bench.js   bytes=624 sha256=c50601bba0c696dcc0a00de5a3e0d9940801bfe18f778275f02db177e7234efa
Buffer.compare        = 0
identical             = true
CAPTION_MAIN differs  = true
exit=0
```

A second comparison pins the new clause against the TZ's own literal rather than
against itself — the sentence was lifted out of `CryptoTZ/TZ-26-venue-count-expectations.md`
by regex and compared to the decoded production string:

```
TZ  §2.2 literal : 'Список считается по 25 спотовым монетам: пять фьючерсных в меру не входят.'
index.html tail  : 'Список считается по 25 спотовым монетам: пять фьючерсных в меру не входят.'
equal            : True
sha256 (both)    : 924274dea22aed4a6b20745ef2ffac5957fa672c8e50e5c479a6aebac44a7a34
```

### §4.5 — Section M's negative control still fires

The plant was made in a **copy** of the tree, so the repository's own working tree was
never red: `/tmp/new` was copied to `/tmp/neg` and `origin/main`'s caption — both the
second sentence and the venue clause of `CAPTION_MAIN` — was substituted into
`/tmp/neg/index.html`. The assertion that exactly one occurrence existed to replace was
made before replacing it, so the plant cannot silently substitute nothing.

```
$ cd /tmp/neg && node bench/exhaustion_bench.js ; echo exit=$?
exit=1
--- checks: 220598  fails: 11 ---
  FAIL M1 quiet: the block does not say "poroga net"
  FAIL M1 quiet: the block does not say "sravneniya net"
  FAIL M1 loud:  the block does not say "poroga net"
  FAIL M1 loud:  the block does not say "sravneniya net"
  FAIL M2 quiet: the caption IS the sentence TZ-15 s2 A1 specifies
  FAIL M2 loud:  the caption IS the sentence TZ-15 s2 A1 specifies
  FAIL M4 the encoder round-trips against the file convention
  FAIL M4 the specified caption occurs once in the source
  FAIL M4 origin/main's caption is gone from the source
  FAIL M4 the control copy differs from the source
  FAIL M4 and the clean source is silent on both renders
```

**The clean source is silent**, from the same section on the real tree:

```
  negative control: reverted caption -> scan fired, naming 2: poroga net + sravneniya net   |   clean source -> 0 phrases found
  caption: 1,0 — обычный день: … Список считается по 25 спотовым монетам: пять фьючерсных в меру не входят.
```

Two facts fall out and are worth stating. The comparison count is **220 598 in both the
red and the green run** — the counter counts comparisons, not passes (inv. 43), so a
failing section cannot shrink the gate's own volume. And the repository tree was clean
before and after: the plant lived only in `/tmp/neg`, and `git status --porcelain`
showed exactly the three intended files modified at every point.

### §4.6 — `journal_bench.js` still reads 30 coins, 25 covered, status ok

From the changed tree's step 7, unmodified:

```
journal_bench: движок 00bbe48d546c1ad1, реестр eb828b1cc4366d51, монет 30
=== 5. Покрытие: строк снимка + пропусков = длине tokens[] ===
  обычный: cov 25 skip 5 статус ok
  fut-пары доступны: cov 25 skip 5 статус ok
  нет блока btc: cov 25 skip 5 статус ok
  снимков 25, пробелов 5, календарных дат 30
```

**Neither new coin raises `hardSkip`** (map inv. 41), and section 6a proves it in both
directions with zero failures: the declared-venue cases all hold `статус ok`, while
6a.6's control — a dead SPOT pair — still drops the status to `partial` and still
counts one `dead market`. The degradation ladder that inv. 41 protects is intact; only
the expectations about how many assets sit in front of it moved.

---

## Test Results

**13 of 13 gate steps green. 1 255 401 checks executed, 0 failures.** Every step's exit
code is 0. The three failures report 2 recorded at step 7 are resolved, and no step
moved by a single check — the outcome §3 named, at the total §3 named.

Local replay, not a runner run; the distinction is kept in `## CI Execution`.

---

## Deviations

**None.** Every item of §2 was implemented as written, both `NOT edited` clauses were
honoured and proved by hash, and §4's six validation items all ran and passed. §3's
predictions were met exactly rather than approached, so nothing needed explaining
against a missed forecast.

One judgement call is recorded rather than hidden, because it is the only place this
session read past the letter of §2.1: the label at line 644 moved from «про живую» to
«про живых». It is argued in `## Implementation Summary`, it is inside the authorised
site, it changes no comparison, and the Architect may strike it without touching
anything else in this change.

---

## Pre-existing Issues

1. **The branch's own copy of `EXECUTOR-INSTRUCTIONS.md` is v18, and the merge does not
   revert v19.** The branch forks from `1d73267`, which predates the Architect's v19
   upload in `2055dc8`. `git diff origin/main...claude/tz-25-universe-morpho-arb
   --name-only` returns six files and the contract is not among them, so merging this
   branch leaves `main`'s v19 in place. Stated because a reader comparing the branch's
   root against the contract this work cites would otherwise find v18 there and have no
   way to tell a stale copy from a reverted one.
2. **The map still disagrees with the code, and only the Architect can close it.**
   `SYSTEM-MAP-CRYPTOCALCUL.md` at `2026-09-02-a` still carries inv. 2 «(Standing
   decision: no new coins.)», §1 line 161 «Universe: 28 pairs, frozen.», and the «25 of
   28» statements at lines 815, 869 and 1506; §3.14's venue set still names three
   assets. TZ-26 §0 says the map is republished only after this branch merges, so this
   is expected rather than newly broken — restated so the merge does not lose it.
3. **The map's `## 0` file table needs new values for `index.html`.** It requires
   3729 / `fdf331906bf205944b25e3635135789c`; the branch carries
   3736 / `dd39536d18cc1feb4839808e41e7bff4`, moved by TZ-25's two `tokens[]` rows and
   by this TZ's one caption line. `main.py` likewise (TZ-25's change, unmoved by
   TZ-26). `catalysts.json` and `bench/exhaustion-calibration.txt` are unchanged.
4. **The gate's published total in the map is still 1 250 739.** The branch stands at
   1 255 401, all of it attributed to TZ-25 in report 2 and none of it to TZ-26. The
   map's `## 0` gate figure moves at the next revision, not here.
5. **`bench/exhaustion-calibration.txt:1` still reads «25 spot of 28 declared tokens …
   HYPE, XMR, LIT».** Carried forward from report 2's remaining risk 4. §2.3 decides
   deliberately that it stays: it is the output of calibration run #2 and describes the
   moment it was taken. It is listed here so the map's next revision carries the
   consequence, per §2.3's closing line, and so no future sweep "fixes" it.
6. **`bench/backtest_bench.py` remains outside `bench.yml`** (it needs the external
   archive and a warm cache) and was not run. Unchanged by this TZ; noted because the
   gate's 13 steps are not the whole bench set.

## Remaining Risks

1. **Nothing is live until the Boss merges.** The branch now carries a 30-coin universe,
   repaired venue expectations and a repaired caption; `main` carries none of it.
2. **The two CoinGecko ids are still unvalidated.** `morpho` and `arbitrum` are the
   Architect's declaration, deliberately not fetched (inv. 44). The arbiter remains
   `debug.json` after the first bot run on a runner: `error: null` and
   `matched_90d > 120` on both. Carried from report 2; TZ-26 changed nothing here.
3. **The `fut:true` count is now derived in two of five places, not all five.** This
   TZ repaired `journal_bench.js:641` and `644` by derivation and left `592` a literal
   on purpose (inv. 22). The remaining hand-written counts live in the caption itself —
   in both files, by design, since the caption is prose a reader reads — and in
   `bench/exhaustion-calibration.txt`. The next venue change therefore still moves
   three strings and one literal. That is the residue of map inv. 58 and is the
   Architect's to close or to accept.
4. **`render_bench.py`'s `SYMS` fixture is a 28-symbol book containing `DOGE`** and is
   deliberately not a count of `tokens[]`. Restated from report 2 so a future sweep does
   not "correct" it.

---

## Commit

Implementation, on `claude/tz-25-universe-morpho-arb`, made and pushed before this
section was written:

```
69bddc3e9ef5ade70a17b319ab1d0fd42b3e7779
fix(bench): venue-count expectations and the 3.17 caption (TZ-26)
```

Contents: `bench/journal_bench.js`, `index.html`, `bench/exhaustion_bench.js` — 15
insertions, 6 deletions, and nothing else. TZ-26 states no `## Commit Message`, so the
message follows the branch's own established form; the section sign is spelled out in
the subject line to keep the message ASCII-safe, and the body names all four edited
sites and both files left deliberately untouched.

The branch now carries two commits: `ea05962` (TZ-25) and `69bddc3` (TZ-26).

This report's own commit carries no hash, no conclusion and no push result (inv. 54):

```
docs(reports): TZ-26 — venue-count expectations repaired, gate green (TZ-26)
```

## Pull Request

**No pull request exists, and the reason is environmental, not a refusal.** `gh` is not
installed in this session (`command -v gh` → nothing) and no `GH_TOKEN` or
`GITHUB_TOKEN` is present, so this session cannot open one. Per §8 the fallback is
taken rather than stopping:

- Branch: **`claude/tz-25-universe-morpho-arb`** (pushed, head `69bddc3`)
- Compare URL:
  **`https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-25-universe-morpho-arb`**

**One pull request covers TZ-25 and TZ-26 together**, as TZ-26 §0 and its
`## Что сделать` step 5 require. The Architect's verdict precedes the merge in every
case; unlike at report 2, the gate is no longer a reason to hold it.

## CI Execution

**Not readable from this session.** No `gh`, no token — so what executed on GitHub is
not reported here in either direction (§9).

What **is** established, by reading the workflows rather than assuming them:

- The branch reached the remote: `git rev-parse origin/claude/tz-25-universe-morpho-arb`
  → `69bddc3e9ef5ade70a17b319ab1d0fd42b3e7779`, equal to local `HEAD`.
- `bench.yml` triggers on `push` to `branches: [ main, 'claude/**' ]`, which this branch
  name matches, and none of the three changed paths (`bench/journal_bench.js`,
  `index.html`, `bench/exhaustion_bench.js`) appears in its `paths-ignore`
  (`journal/data/**`, `journal/out/**`, `journal/runs.jsonl`, `analyst/state.json`,
  `analyst/live.json`, `analyst/log/**`, `**.md`).
- `main.yml`'s `push` filter was read on `origin/main` **before** this report was
  pushed, as §8 requires rather than assumes: it is still a `paths` **allow-list** of
  exactly `'main.py'` and `'.github/workflows/main.yml'`. `CryptoReports/**` is not on
  it and everything unnamed is out, so the report's direct push to `main` cannot start
  the bot; and Pages serves `index.html`, which no path in `CryptoReports/**` can reach.
  Both facts §8 rests on hold.

What this session measured locally, on the same 13 commands `bench.yml` runs, is the
table in §4.3: **13 steps green, 1 255 401 checks, 0 failures.** A local run is not a
runner run and the two are not conflated here. The hosted gate is read by the audit,
on the page the merging actor already has open.

## Final Repository State

The session leaves behind the branch **`claude/tz-25-universe-morpho-arb`** at
`69bddc3e9ef5ade70a17b319ab1d0fd42b3e7779`, pushed before this report was written and
therefore measured. Across its two commits it carries six modified files — `main.py`,
`index.html`, `bench/journal_bench.js`, `bench/exhaustion_bench.js`,
`bench/catalyst_bench.js`, `bench/backtest_bench.py` — and nothing else. The working
tree is clean apart from gitignored scratch (`bench/_*`, `__pycache__/`), which is never
committed.

**NOT IN EFFECT UNTIL MERGED.**

On the branch: `TOKENS` and `tokens[]` stand at 30, the declared `fut:true` set at 5,
the spot universe at 25, and the gate at 1 255 401 checks with 0 failures. On `main`:
28, 3, 25, and 1 250 739.

## Fingerprints

Map, at the revision TZ-26's §0 gate requires — **all seven anchors matched as exact
substrings, revision string matched**, measured on `origin/main` before any work:

| File | Revision | Lines | MD5 |
|---|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | `Revision 2026-09-02-a` | 1841 | `03ec11fc16853947c83add15ca3e1ef8` |

| Anchor | Result |
|---|---|
| `**Revision 2026-09-02-a.**` | PRESENT |
| `### 3.12 Direction engine — veto cascade` | PRESENT |
| `### 3.15 Catalyst registry` | PRESENT |
| `### 3.16 List exhaustion — the day-range measure` | PRESENT |
| `## 11. Analytical engine` | PRESENT |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | PRESENT |
| `58. **A rule that names an object without naming how to compute it has named nothing.**` | PRESENT |

Files the map's `## 0` table lists — **required** values are the map's, **branch**
values are this branch's at `69bddc3`. The map's copy is byte-identical on `main` and on
the branch, so the gate reads the same in both places.

| File | Required (lines / MD5) | On this branch | State |
|---|---|---|---|
| `index.html` | 3729 / `fdf331906bf205944b25e3635135789c` | 3736 / `dd39536d18cc1feb4839808e41e7bff4` | **changed** — TZ-25's two rows + TZ-26's caption line |
| `main.py` | 506 / `1a5a5d98b2fd76010f202ee3eebaa717` | 518 / `0e3ead8c300d2ee6783303c4bf2fb6b5` | **changed by TZ-25**, unmoved by TZ-26 |
| `catalysts.json` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | unchanged |
| `bench/exhaustion-calibration.txt` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | unchanged — §2.3 |

Benches the gate table depends on, at `69bddc3`:

| File | Lines | MD5 |
|---|---:|---|
| `bench/journal_bench.js` | 967 | `4d59fdda46868ab357f406c6c39e8ae8` |
| `bench/exhaustion_bench.js` | 1803 | `c2d3dc7f22f8fdfc074139b2483c1f8a` |
| `bench/catalyst_bench.js` | 614 | `12b4f5b29299b90b4eec6d7376bc6a7e` |
| `bench/backtest_bench.py` | 1990 | `f1ba588949978952def15da3a1c22a04` |

Governing documents on `origin/main`, carried because this report makes claims about
their content:

| File | Version | Lines | MD5 |
|---|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` | **v19** | 801 | `a6ebc2e7c2f2b74e813dfdc20400558f` |
| `ANALYST-INSTRUCTIONS.md` | — | 1608 | `0ff09a55d2c726c9794af261c901a81a` |
