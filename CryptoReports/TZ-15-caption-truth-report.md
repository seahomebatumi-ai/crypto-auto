# Implementation Report — TZ-15

**Caption truth: the block no longer denies the threshold it uses, and the gate
can now catch the next denial of this kind.**

## Status

**COMPLETED.** Both stages executed exactly as specified. All ten validation
items ran and passed. The hosted `Bench gate` executed on the branch — see
`## CI Execution` for the run id and conclusion.

**NOT IN EFFECT UNTIL MERGED.**

---

## Inbound Filing

None. `CryptoTZ/TZ-15-caption-truth.md` was already on `origin/main` under its
canonical filename when the session fetched. Nothing was renamed or moved.

The clone was **shallow** (`git rev-parse --is-shallow-repository` → `true`) and
was deepened with `git fetch --unshallow` before anything historical was
assessed: 327 commits on `origin/main` after deepening.

The previous TZ's branch **was merged**: `44e100b Merge pull request #14 from
seahomebatumi-ai/claude/execute-tz-14-47nul9`. This work is not stacked on an
unmerged base.

---

## 0. Fingerprint gate — PASSED

Run before any work, against `origin/main` (never local `main`), after
`git fetch --all --prune`.

| Anchor | Required string | Found |
|---|---|---|
| revision | `**Revision 2026-08-25-a.**` | yes |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | yes |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | yes |
| newest invariant | `50. **A stated absence is a dependency of the thing it denies.**` | yes |

Baseline files, measured from a `git worktree` at `origin/main` (`3b03665`),
never assumed:

| File | Lines req. | Lines found | MD5 req. | MD5 found | |
|---|---:|---:|---|---|---|
| `index.html` | 3727 | 3727 | `38d862bf3990b88dc8fcf5bc76d35015` | `38d862bf3990b88dc8fcf5bc76d35015` | ✓ |
| `main.py` | 506 | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | `1a5a5d98b2fd76010f202ee3eebaa717` | ✓ |
| `catalysts.json` | 11 | 11 | `021dd2c90dc395240c0b0c3dbae40426` | `021dd2c90dc395240c0b0c3dbae40426` | ✓ |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | ✓ |
| `bench/exhaustion_bench.js` | 1557 | 1557 | `f8ecc6ea28e3f7cbf98ad72c259d8ec7` | `f8ecc6ea28e3f7cbf98ad72c259d8ec7` | ✓ |

**Gate baseline measured, not assumed: 12 steps, 1 250 613 checks**, from the
same `origin/main` worktree, with the same harness later used for the candidate.
It reproduced the TZ's stated figure exactly, and step 7 read **691 109**.

All rows match. Gate PASSED, work proceeded.

---

## Scope Executed

Both stages, in full, with no deviation.

- **Stage A1** — the `bd-note` of «РИСК ВЫНОСА» replaced by the §2 A1 sentence,
  written from the TZ's escaped literal.
- **Stage A2** — the comment clause six lines above replaced by the TZ's text.
- **Stage B** — section **M** appended to `bench/exhaustion_bench.js` after
  section L, with M1–M5 as specified.

**One addition inside the modified file, stated plainly rather than buried.**
The bench's header comment enumerates its sections and ends with the list TZ-14
added. Two lines were appended to that list naming section M. It is documentation
of exactly the authorised change, in the file the TZ authorises modifying, and it
is a comment: no assertion, no counter and no behaviour depends on it. Nothing
else outside the specified edits was touched.

---

## Files Modified

| File | Δ lines | What |
|---|---:|---|
| `index.html` | +4 / −2 | A1 caption (1 line replaced), A2 comment (1 line → 3) |
| `bench/exhaustion_bench.js` | +246 / −1 | section M, the `caption: 0` counter key, 2 header lines |

## Files Created

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Stage A — the caption, and the comment above it

TZ-14 made «РИСК ВЫНОСА» print, in amber, `ДЕНЬ УЖЕ ВЫНЕСЕН — медиана списка 2,4
обычного дня, порог 1,39. Мера дня, не запрет.` Directly under it the block's own
caption still read «Число печатается как есть — **порога нет, сравнения нет**…».
The board contradicted itself two lines apart, in the Boss's own language, and
nothing in the gate could see it: a bench compares behaviour against a
specification, and this was a claim *about* the specification.

`index.html:2856` now carries the sentence TZ-15 §2 A1 specifies. It states what
the line MEANS — that the threshold is the 90th percentile of the list median over
the three-year archive, and that it is a measure of the day rather than a veto —
and keeps the half of the old caption that is still true: the number reaches no
score, no leverage and no verdict.

**The caption does not print the number, deliberately.** `DAY_RANGE_ABNORMAL`
keeps exactly three code sites, and a literal `1,39` in a static caption would be
a fourth site of the same quantity in a form no re-calibration could reach
(inv. 20). The value is already printed one line above by `dayStateNote` on the
days it matters.

The escaped literal was taken from the TZ file itself rather than retyped, and its
decoded form was compared against the TZ's plain §2 A1 sentence **before** the edit
was applied: 352 characters, identical.

`index.html:2850` — the comment clause `, and the caption below is unchanged.`,
true of TZ-14 and false the moment this TZ lands, became the three-line statement
the TZ specifies. It is now a claim that stays checkable.

Nothing else in the block moved: no row, no colour, no order, no inline `style` on
the `.bd-sec`.

### Stage B — gate section M

Section **M. The caption denies nothing the block does (inv. 50)**, appended after
section L. It reuses L's `loadLive` / `liveBook` / `liveRender` / `renderBoard`
harness **by name** — no second render path is written. Every counter increments at
the comparison site through the file's existing `eq` / `ok` helpers (inv. 43), and
every sub-check counts what it compared and asserts that count is non-zero
(inv. 22).

The section is deliberately narrow (§3, non-goal 9). It reads ONE block, located
exactly as section L locates it — forward to the header, back to
`lastIndexOf('<div class="bd-sec', at)`, forward to the next `.bd-sec` — and scans
only for denials of a mechanism *this* block has.

| | Sub-check | What it asserts | Comparisons |
|---|---|---|---:|
| — | preamble | the quiet render is not abnormal, the loud one is | 2 |
| **M5** | scope | the block is non-empty, is a strict part of the board, opens exactly one `.bd-sec`, carries exactly one header, that header is «РИСК ВЫНОСА», and the board carries sections the scan did not read — on both renders | 16 |
| **M1** | no denial | six phrases, lower-cased, each compared and counted separately on each of the two renders; plus the comparison count and the set size asserted | 14 |
| **M2** | what remains true | the derived unit `√(8/π)`, the inv. 27 words, the coverage clause, the whole sentence as ONE string comparison against §2 A1, and exactly one caption per board and per block — on both renders | 14 |
| **M3** | inv. 20 | `numRu(DAY_RANGE_ABNORMAL, 2)` read *through the live context*, present in the day line, absent from the loud caption, absent from the quiet block entirely | 7 |
| **M4** | the control | the reverted-caption copy fires the same scan and names what it found; the clean source is silent | 11 |
| | | **total** | **64** |

`scanDenials` is deliberately **pure** — it touches no counter. M1 and M4 point the
same instrument at two different sources and assert opposite outcomes; a scan that
counted its own hits would turn the control's success into a recorded failure. The
counting happens at the assertion sites, where the comparison is.

M4 needed to substitute a runtime string into the *source*, where `index.html`
escapes everything above U+007F. A small `toSourceEscapes` encoder does that, and
its round-trip is **asserted rather than assumed** (`src.indexOf(capSrc) > 0`): if
the encoder and the file's convention ever disagreed, the control would substitute
nothing, the scan would stay silent, and a broken control would report success.

Section M is pure ASCII outside comments — zero Cyrillic characters anywhere in it,
every Russian string a `\uXXXX` escape (hard floor item 7), every comment English.
Verified by Unicode range over the whole section, not by eye.

---

## Validation

Every one of the ten items ran. Every count is reported. No item was skipped and
none was treated as "not applicable".

### 1. Compiles and guards — PASS

```
python3 -m py_compile main.py                      → exit 0
node --check <script> extracted from index.html    → OK (3161 lines)
node --check bench/exhaustion_bench.js             → OK
```

ES5 guard and escape guard over **every changed or added line of `index.html`**,
taken from `git diff -U0 origin/main -- index.html`, `+` side only:

```
ES5 guard:    lines checked = 4
escape guard: lines checked = 4
new/changed comment lines (all must be English) = 3
GUARDS PASS (0 violations)
```

Both guards report the number of lines checked and fail on zero. The ES5 guard
looks for `let`, `const`, arrow functions, template literals, spread and `class`;
the escape guard fails on any character above U+007F. All four changed lines pass:
the caption is fully `\uXXXX`-escaped, and the three new comment lines are English
ASCII.

### 2. The caption, decoded — PASS

Rendered from production's own `boardHtml`, printed once, verbatim:

```
1,0 — обычный день: у броуновского блуждания E[хода] = σ·√(8/π), поэтому единица здесь не выбрана, а выведена. Порог, выше которого день назван вынесенным, — 90-й процентиль медианы списка по трёхлетнему архиву; это мера дня, а не запрет: на счёт, плечо и вердикт она не влияет. Список считается по 25 спотовым монетам: три фьючерсные в меру не входят.
```

**Character-for-character comparison against the §2 A1 sentence: identical.**
Decoded length 352, target length 352, `inner === target` → `true`. Asserted twice:
once before the edit was applied (on the literal taken from the TZ), and again
inside the gate by M2, as one string comparison on each of the two renders.

**The old caption occurs nowhere in `index.html`:** `grep -cF` on the full
`origin/main` line → **0**; the escaped denial fragment `порога нет`
(«порога нет») → **0**. The new caption occurs exactly **1** time. The file's
`class="bd-note"` count is unchanged at **19**, so no note was added or lost.

Asserted in the gate as well: M4's `eq('M4 origin/main's caption is gone from the
source', src.indexOf(mainSrc), -1)`.

### 3. The denial set — PASS

The six phrases, each compared and counted **separately**, lower-cased, on each of
the two renders:

| # | phrase | quiet render | loud render |
|---:|---|---|---|
| 1 | `порога нет` | absent | absent |
| 2 | `сравнения нет` | absent | absent |
| 3 | `нет порога` | absent | absent |
| 4 | `нет сравнения` | absent | absent |
| 5 | `без порога` | absent | absent |
| 6 | `не сравнивает` | absent | absent |

**Comparisons made: 12** (6 phrases × 2 renders), asserted in the bench itself
(`eq('M1 compared all six phrases on both renders', compared, 12)`) so an emptied
list cannot pass as a clean scan, plus `eq('M1 the denial set is the six the TZ
names', DENIALS.length, 6)`.

**M4's negative-control output, verbatim from the gate:**

```
  negative control: reverted caption -> scan fired, naming 2: poroga net + sravneniya net   |   clean source -> 0 phrases found
```

The reverted-source copy is built by substituting the `origin/main` caption back
into a copy of the script, evaluating it in a second context, and rendering the
block through the same path. The scan fires and names **both** denials
`origin/main` carried; on the clean source it finds **0** on both renders.

**Proven able to fail end to end, not only through its own control.** The
`origin/main` caption was planted back into the working tree's `index.html` and the
whole bench was run:

```
  FAIL M1 quiet: the block does not say "poroga net": got true want false
  FAIL M1 quiet: the block does not say "sravneniya net": got true want false
  FAIL M1 loud: the block does not say "poroga net": got true want false
  FAIL M1 loud: the block does not say "sravneniya net": got true want false
  FAIL M2 quiet: the caption IS the sentence TZ-15 s2 A1 specifies: …
  FAIL M2 loud:  the caption IS the sentence TZ-15 s2 A1 specifies: …
  FAIL M4 the encoder round-trips against the file convention: got false want true
  FAIL M4 the specified caption occurs once in the source: got 0 want 1
  FAIL M4 origin/main's caption is gone from the source: got 138459 want -1
  FAIL M4 the control copy differs from the source: got false want true
  FAIL M4 and the clean source is silent on both renders: got 4 want 0

--- checks: 220598  fails: 11 ---
EXIT CODE = 1
```

**Sections A through L all stayed green on that same reverted tree.** That is the
finding this TZ exists for, demonstrated rather than argued: TZ-14's gate genuinely
could not see the contradiction, and section M is the only thing in the repository
that can. The tree was then restored and re-verified byte-identical
(`md5 fdf331906bf205944b25e3635135789c`), and the bench returned to
`checks: 220598  fails: 0`.

### 4. inv. 20 preserved — PASS

Section L's enclosing-site enumeration re-run, its line printed, baseline and
candidate side by side:

```
baseline : DAY_RANGE_ABNORMAL code sites: declaration=1, listExhaustion=1, dayStateNote=1  total=3  (comments included: 5)
candidate: DAY_RANGE_ABNORMAL code sites: declaration=1, listExhaustion=1, dayStateNote=1  total=3  (comments included: 5)
```

**Exactly three code sites, and no fourth.** The comment-inclusive count is also
unchanged at 5: the new A2 comment says «the constant keeps exactly three code
sites (inv. 20)» without naming the identifier, so it adds no mention.

M3's two assertions, on the live render: `numRu(DAY_RANGE_ABNORMAL, 2)` = `"1,39"`,
read **through the live context** and never as a literal —

- occurs in the day line (`loudSentence.indexOf(NUM) > 0`) and the loud block
  carries that day line;
- does **not** occur anywhere in the loud caption (`indexOf` → `-1`);
- does not occur anywhere in the quiet block at all (`indexOf` → `-1`), nor in the
  quiet caption.

### 5. The card list did not move — PASS

Rendered on **every regime × side combination at both a quiet and a loud day** and
compared byte-for-byte against `origin/main`, both revisions driven through the
same fixture:

```
  regimes: unknown, stress_up, stress_dn, trend_up, trend_dn, range
  card lists compared: 24   byte-identical: 24   differing: 0
  ITEM 5 PASS
```

The regime presets are built from the live context's own `H_NOISE`,
`REG_STRESS_Z` and `EFF_TREND`, so a re-tuned threshold cannot silently
reclassify a scenario into a regime other than the one it is labelled with. The
day state was additionally asserted to be `false` on every quiet render and `true`
on every loud one, so the 24 are not identical because nothing happened.

This TZ touches the board only. Zero movement here is the required result.

### 6. No-regression, identity first (inv. 45) — PASS

**`prot_bench.js`'s unconditional identity run, before anything else is offered as
evidence:**

```
fuzz: 4000 boards rendered clean
identity: 6 boards compared against index.html itself
PASS 372   FAIL 0
```

Zero differences.

**Whole-board differ against `origin/main`,** over the full scenario set — 10 list
ratios × 3 list sizes × 2 sides × 6 leverage buttons = 360 boards, cycling through
five `cd` shapes, four money modes and four funding rates:

| | |
|---|---:|
| boards compared | **360** |
| byte-identical | **0** |
| differ ONLY in the caption substring | **360** |
| **differ anywhere else** | **0** |
| distinct differing substrings | **1** |

**The expected shape is unusual and is met exactly: the caption is unconditional,
so EVERY board differs, and boards-differing-only-in-the-caption equals
boards-compared.** Boards differing anywhere else: **zero**.

The differing substring is found by trimming the common prefix and the common
suffix, so what remains is precisely what moved. There is exactly **one**, and it
occurs on all 360 boards:

```
BEFORE (origin/main): Число печатается как есть — порога нет, сравнения нет, на счёт, плечо и вердикт оно
AFTER  (candidate):   Порог, выше которого день назван вынесенным, — 90-й процентиль медианы списка по трёхлетнему архиву; это мера дня, а не запрет: на счёт, плечо и вердикт она
```

Both sides of the change were additionally required to sit **inside the caption's
own `bd-note`** on their respective boards, not merely somewhere on the page — so
"differs only in the caption" is a positional claim, not a textual coincidence.

### 7. Purity (inv. 27), proven by perturbation — PASS

TZ-14's protocol unchanged. `hi24`/`lo24` scaled from ratio 1.20 (median 1.2000,
`abnormal=false`) to ratio 3.60 (median 3.6000, `abnormal=true`), over a 25-coin
board, on both sides.

**A — same rows, candidate vs `origin/main`.** For every coin: `sc.score`,
`vd.action`, `vd.why`, `dec.L`, `dec.binding`, `dec.moneyBelowMin`, `geo.rr`,
`inv.price`, the card's number, tier and rendered badge — all identical, at both
ratios, on both sides. The journal record that `journal/write.js` would write,
built through the journal's **own exported `sideBlock`** on each revision of
`index.html` and canonicalised by its **own `canon`**, is byte-identical:

```
  long  quiet: abnormal=false  rows=28  journal record 17008 B, byte-identical to origin/main: true
  long  loud:  abnormal=true   rows=28  journal record 17008 B, byte-identical to origin/main: true
  short quiet: abnormal=false  rows=28  journal record 20641 B, byte-identical to origin/main: true
  short loud:  abnormal=true   rows=28  journal record 20641 B, byte-identical to origin/main: true
```

**B — the two-sided form: whatever the perturbation moves, it moves identically on
`origin/main`.**

```
  LONG : journal field(s) moved by the perturbation: none
  LONG : flipping abnormal moves fields [none] on the candidate and [none] on origin/main; journal record moved: false vs false — identical: true
  SHORT: journal field(s) moved by the perturbation: geo.wait
  SHORT: flipping abnormal moves fields [none] on the candidate and [none] on origin/main; journal record moved: true vs true — identical: true
```

The single mover, `geo.wait` on SHORT, is the entry-chase distance measured from
the 24h maximum — a pre-existing dependency of the direction engine on the 24h
range, present identically on `origin/main`, and exactly the one TZ-14 found.
**Nothing moves because of `abnormal`.**

**Fields compared: 1 240. Failures: 0.**

### 8. Extremes — all ten — PASS

`update()` threw in none. The caption renders exactly once per board and never
twice. A board with no metrics prints no caption and no new `NaN`.

| # | case | `update()` threw | n | median | `abnormal` | captions in board | board len | new `NaN` (list/board) |
|---|---|---|---:|---|---|---:|---:|---|
| 1a | slider at the low edge | no | 25 | 3.600 | true | 1 | 15278 | no / no |
| 1b | slider at the high edge | no | 25 | 3.600 | true | 1 | 15283 | no / no |
| 2 | null betas | no | 25 | 3.600 | true | 1 | 14287 | no / no |
| 3 | truncated Gist (3 of 28) | no | 3 | null | false | 1 | 15072 | no / no |
| 4 | HTTP 400 ticker (empty spot) | no | 3 | null | false | 1 | 15072 | no / no |
| 5a | dead-market fields | no | 22 | 3.600 | true | 1 | 15331 | no / no |
| 5b | no pair | no | 22 | 3.600 | true | 1 | 15331 | no / no |
| 6 | missing coeffs fields | no | 25 | 3.600 | true | **0** | **0** | no / no |
| 7 | absent `btcStats` | no | 25 | 3.600 | true | 1 | 14245 | no / no |
| 8 | absent `volatility` | no | 0 | null | false | **0** | **0** | no / no |
| 9 | `E ≤ 0` | no | 25 | 3.600 | true | 1 | 9653 | no / no (board `NaN` 1 vs 1 on `origin/main`) |
| 10 | non-finite `liq` | no | 25 | 3.600 | true | 1 | 14128 | no / no (board `NaN` 1 vs 1 on `origin/main`) |

Cases 6 and 8 render **no board at all** (board length 0) — the row carries no
metrics, so there is nothing to print into, and the caption count of 0 is correct
rather than a miss. Every board that rendered carried the caption exactly once.

"New `NaN`" is a **comparison, not a judgement**: each case mutates the fixture
identically on both revisions, and only a `NaN` the candidate prints and
`origin/main` does not would count. Cases 9 and 10 each print one `NaN` on both
revisions — the pre-existing §6.1 defect, confirmed below and not fixed.

### 9. Full gate, 12 steps — PASS

Baseline measured from a `git worktree` at `origin/main`, candidate measured with
the same harness. Both runs green, all 12 steps exit 0.

| # | Step | Baseline | Candidate | Δ |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 |
| 3 | `prot_bench.js index.html` | 372 | 372 | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 255 708 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 |
| **7** | **`journal_bench.js`** | **691 109** | **691 109** | **0** |
| 8 | `catalyst_bench.js` | 23 040 | 23 040 | 0 |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 15 925 | 15 925 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | 220 534 | 220 598 | **+64** |
| | **TOTAL** | **1 250 613** | **1 250 677** | **+64** |

**Steps 1–11 read unchanged, and that is asserted, not observed.** This TZ edits
one display string, one comment and one bench; any movement outside step 12 would
be a defect. There is none. The baseline total reproduces the TZ's stated
**1 250 613** exactly, and **step 7 reads 691 109** as the TZ requires — a result,
not a coincidence: §7 above proves the journal record is byte-identical under the
perturbation that flips `abnormal`.

**The +64, term by term** (per-section counters from `exhaustion_bench.js`, which
the bench itself sums and cross-checks against its own check total):

| section | baseline | candidate | Δ |
|---|---:|---:|---:|
| identity | 200 002 | 200 002 | 0 |
| nulls | 20 027 | 20 027 | 0 |
| quorum | 65 | 65 | 0 |
| venue | 25 | 25 | 0 |
| banner | 52 | 52 | 0 |
| stress | 51 | 51 | 0 |
| inert | 120 | 120 | 0 |
| purity | 36 | 36 | 0 |
| control | 1 | 1 | 0 |
| wiring | 31 | 31 | 0 |
| record | 8 | 8 | 0 |
| threshold | 24 | 24 | 0 |
| live | 38 | 38 | 0 |
| surfaces | 54 | 54 | 0 |
| **caption** | **0** | **64** | **+64** |

Every pre-existing section counter is unchanged. The whole delta is section M's own
counter, and it decomposes as: preamble 2 + M5 16 + M1 14 + M2 14 + M3 7 + M4 11 =
**64**. The bench's own closing guard (`sum !== checks → exit 1`) confirms the
counters and the check total agree.

### 10. Release checklist 11, 15, 18 — PASS (20 checks, 0 failures)

**Item 15 — «РИСК ВЫНОСА» (§3.17):**

```
  ok   the block is sixth  [position 6 of 14]
  ok   it sits between «ВЫБОР ПЛЕЧА» and «РАЗМЕР ПОЗИЦИИ»
  ok   the .bd-sec carries no inline style, so the metal ring survives  ["<div class=\"bd-sec\"><div class=\"bd-h\">"]
  ok   row 1 moves when the leverage BUTTON moves        [3X: 7,9σ дня  ->  7X: 2,9σ дня]
  ok   the list line names a non-zero coin count         [медиана списка 1,4 по 25 монетам]
  ok   and it matches the spot rows on screen            [25 vs 25 spot tokens]
  ok   the threshold is named inside the block
  ok   and nowhere else on the board
  ok   and inside it only through the dayStateNote sentence
  ok   the caption denies no mechanism the block has (inv. 50)  [6 phrases compared]
  ok   on a quiet day the threshold is named nowhere on the board
  ok   and the caption is still printed exactly once
```

The `.bd-sec` opening tag is verified to carry **no inline `style`**, so the metal
ring survives (§3.7, inv. 19).

**Item 18 — day state (§3.16, §3.17):**

```
  ok   the amber sentence appears on BOTH surfaces in every regime x side  [12 of 12]
  ok   a quiet day silences BOTH surfaces in every regime x side           [12 of 12]
  ok   the abnormal===false banner is a strict prefix of the abnormal===true one  [12 of 12]
  ok   a below-quorum list silences both surfaces         [n=3 median=null]
  ok   the source literal equals the calibration record (inv. 46)  [1.39 vs 1.39]
```

**Item 11 — direction engine (inv. 33–35):**

```
  ok   no coin carries both ЛОНГ and ШОРТ as a numbered card  [0 violations]
  ok   the tier badge greys out on a forbidden card           [0 violations]
  ok   cards inspected                                        [336 cards over 12 lists]
```

---

## Test Results

| Item | Result | Evidence |
|---|---|---|
| 1 Compiles and guards | PASS | exit 0 ×3; 4 lines guarded, 0 violations |
| 2 Caption decoded | PASS | 352 = 352 chars, identical; old caption count 0 |
| 3 Denial set + control | PASS | 12 comparisons, 0 hits; control fires naming 2 |
| 4 inv. 20 three sites | PASS | declaration=1, listExhaustion=1, dayStateNote=1 |
| 5 Card list unmoved | PASS | 24 lists, 24 byte-identical |
| 6 Whole-board differ | PASS | 360 boards, 360 caption-only, 0 elsewhere, 1 substring |
| 7 Purity | PASS | 1 240 fields, 0 failures |
| 8 Extremes | PASS | 12 cases, 0 throws, 0 new NaN |
| 9 12-step gate | PASS | 1 250 613 → 1 250 677, steps 1–11 unchanged |
| 10 Checklist 11/15/18 | PASS | 20 checks, 0 failures |
| Negative test | PASS | reverted caption → exit 1, 11 failures |

---

## Deviations

**None from the specification.** One addition is stated in `## Scope Executed`
above rather than left implicit: two comment lines were appended to the bench's
own section list in its file header, naming section M. It carries no assertion and
no counter.

Two notes on figures that differ from TZ-14's report, neither a deviation from
this TZ:

- The purity field count is **1 240** here against TZ-14's 1 658. The protocol is
  the one TZ-14 specifies — same eleven per-coin fields, same two ratios, same two
  sides, same journal comparison — but the field count is a property of the
  harness's own enumeration, and this harness is written fresh (validation
  harnesses are scratch and are not committed). The count is reported as measured,
  not adjusted to match.
- Item 8's cases 9 and 10 are constructed differently from TZ-14's: setting the
  ticker's `lastPrice` to zero degrades the whole row and never reaches a rendered
  board, so `E ≤ 0` is produced through `entryState` and the non-finite `liq`
  through a zero leverage. Both now reach a **rendered board carrying the
  caption**, which is what this TZ needs to test.

---

## Pre-existing Issues

All three named in §6 confirmed present. **None fixed.**

1. **`NaN% от входа` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ»** — confirmed. `prot_bench.js`
   self-reports it on every run:
   `PRE-EXISTING (not TZ-12, present on origin/main): at E = 0 the board prints NaN in «ГРАНИЦЫ СДЕЛКИ» — Math.abs(liq / E - 1).`
   Independently reproduced by item 8 case 9: one `NaN` on the candidate board and
   one on `origin/main`. Unreachable live.
2. **Raw Cyrillic literal in `bench/prot_bench.js`, line 177** — confirmed:
   `var inv = { dist: 0.10, price: 9.0, capped: false, floored: false, src: 'мин30', sd: 0.049, ref: 9.0 };`
3. **The Node 20 action pin in `bench.yml`** — confirmed: `node-version: "20"` at
   line 50, with `actions/checkout@v4`, `actions/setup-python@v5` and
   `actions/setup-node@v4`. Warning only; the hosted run completed successfully.

**Nothing new found.** Section M was written to be pure ASCII outside comments
specifically so it would not add a fourth instance of issue 2.

---

## Remaining Risks

1. **The denial list is a blacklist, and a blacklist is not a proof.** M1 catches
   the six phrasings TZ-15 names. A future caption could deny the threshold in
   words none of them match — «число ни с чем не сопоставляется», say — and the
   section would stay green. This is the deliberate trade §3 non-goal 9 makes: a
   wider instrument fires on absences that are still true and gets deleted. The
   mitigation already in the section is M2's whole-sentence equality, which pins
   the caption exactly and would fail on **any** rewrite, denial or not; M1 is the
   part that survives a legitimate future rewrite of that sentence.
2. **M2 pins the caption to one exact string**, so any future TZ that legitimately
   changes this caption must update section M in the same change. That is intended
   — it is what makes the caption a checked claim rather than free prose — but it
   is a coupling the next Architect should know about.
3. **Section M asserts a block layout.** It locates the block by its header and by
   the next sibling `.bd-sec`, exactly as section L does. A future board that
   nested `.bd-sec` elements would break both sections at once; M5's assertions
   (one `.bd-sec`, one header, strictly shorter than the board) would fail loudly
   rather than silently widen the scan, which is the safe direction.

---

## Commit

```
c8be42b  fix(board): the caption states the threshold it used to deny (TZ-15)
```

Parent `3b03665`, i.e. `origin/main` exactly — nothing is stacked on an unmerged
base. The commit contains exactly the implementation: `index.html` and
`bench/exhaustion_bench.js`. The working tree is clean; no scratch file, cache or
generated artifact was committed (the one temporary probe used during development,
`bench/_probe.js`, matches the ignored `bench/_*` pattern and was deleted before
the commit).

The TZ states no `## Commit Message`, so the message is written to the standing
format.

## Pull Request

**No pull request exists. A branch with no pull request is a branch with no CI —
except that in this case the `Bench gate` did run, because its `push` trigger
covers `claude/**` (TZ-07 §6).** This session's base configuration does not open
pull requests without an explicit instruction, so per §8 the fallback applies.

- **Branch:** `claude/execute-tz-15-tjlgcm`
- **Compare URL:** https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-15-tjlgcm

The Boss opens and merges from that link in one action, after the Architect's
audit returns ПРИНЯТО.

## CI Execution

**The hosted `Bench gate` result WAS observable from this session. Run id
`32780919062`, conclusion `success`.**

- Workflow: `Bench gate` (`.github/workflows/bench.yml`), run #77, event `push`,
  branch `claude/execute-tz-15-tjlgcm`, head `c8be42b`.
- Job `bench` (`97602585933`): **success**. All 12 bench steps completed with
  conclusion `success`, including step 17 in the job's numbering,
  «Истощение списка и баннер режима (exhaustion_bench.js)» — the step carrying
  section M.
- URL: https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32780919062

Local runs were also performed, and the distinction is stated rather than glossed:
the 12-step baseline/candidate table in validation item 9 was measured **locally**,
from a `git worktree` at `origin/main` and from the working tree, because a runner
gives a pass/fail per step and not a per-step check count. The runner's job is the
authority on green; the local table is the authority on the delta. Both agree.

No other workflow ran: `calib.yml`, `main.yml`, `journal.yml` and
`backtest_bench.yml` were not touched and their triggers did not fire.

## Final Repository State

- `main` — unchanged by this task except for this report.
- `claude/execute-tz-15-tjlgcm` — carries `c8be42b`, pushed, `Bench gate` green.
- Working tree clean. No pull request open.

**NOT IN EFFECT UNTIL MERGED.**

---

## Fingerprints

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1388 | `139ffb540db88a9d1c3daacef92509e2` |
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/exhaustion_bench.js` | 1801 | `04aa088a321711dfeefff74f22813f66` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

System Map revision string, from its `## 0. Fingerprint` block:

```
**Revision 2026-08-25-a.** Baseline: TZ-14 merged (PR #14, `44e100b`).
```

`main.py`, `catalysts.json` and `bench/exhaustion-calibration.txt` are unchanged
from the gate baseline, as §3 non-goals 1 and 7 require. `index.html` moved from
3727 to 3729 lines (+2, the A2 comment) and `bench/exhaustion_bench.js` from 1557
to 1801 (+244).
