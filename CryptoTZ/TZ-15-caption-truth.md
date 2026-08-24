# TZ-15 — The caption that denies its own threshold, and the control for the class

**Canonical filename: `TZ-15-caption-truth.md`.** Commit the file under exactly
this name in `CryptoTZ/`, taken from this line and never from the name the artifact
arrived under.

**Model: Opus.** The production edit is one escaped string, but the second half is a
new gate section that must be proven able to fail and a whole-board differ whose
expected shape is «every board differs, in exactly one substring». A bench that
cannot fail is worse than no bench, and deciding what a caption may and may not
claim is a judgement, not a substitution. `[решение принято мной]` Discarded:
Sonnet — the string edit is mechanical, but every defect in this series so far was
born in the bench half, not in the production half.

---

## 0. Fingerprint gate — compare BEFORE any work

Run `git fetch --all --prune` first. Compare against `origin/main`, never local
`main`. A mismatch on any row is **ЗАБЛОКИРОВАНО**: stop, report, do nothing else.

| Anchor | Exact string that must be present in `SYSTEM-MAP-CRYPTOCALCUL.md` |
|---|---|
| revision | `**Revision 2026-08-25-a.**` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `50. **A stated absence is a dependency of the thing it denies.**` |

Baseline files at this revision:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3727 | `38d862bf3990b88dc8fcf5bc76d35015` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/exhaustion_bench.js` | 1557 | `f8ecc6ea28e3f7cbf98ad72c259d8ec7` |

**The bench file is in the gate table this time.** This TZ extends a file TZ-14
rewrote, and section M below reuses section L's harness by name; a file that has
moved since it was audited would make «reuses L» mean something different.

Gate baseline: `bench.yml`, 12 steps, **1 250 613** checks, measured from a
`git worktree` at `origin/main`, never assumed.

Check the clone for truncation (`git rev-parse --is-shallow-repository`) and deepen
before assessing anything historical.

---

## 1. Why this exists

TZ-14 adopted `DAY_RANGE_ABNORMAL = 1.39` and made «РИСК ВЫНОСА» print, in amber,
«ДЕНЬ УЖЕ ВЫНЕСЕН — медиана списка 2,4 обычного дня, порог 1,39. Мера дня, не
запрет.»

Directly under that line the block's own caption still reads:

> «Число печатается как есть — **порога нет, сравнения нет**, на счёт, плечо и
> вердикт оно не влияет.»

**The board contradicts itself in the Boss's own language, two lines apart, and
nothing in the gate can see it.** A bench compares behaviour against a
specification; this is a claim ABOUT the specification, and TZ-14's file list did
not include the caption. The Executor was right to leave it and the specification
was wrong to omit it — that is invariant 50, and this TZ is its first application.

The caption's second half is true and stays: the number reaches no score, no
leverage and no verdict, proven by perturbation over 1 658 fields with a
byte-identical journal record (§3.16).

A second, smaller instance of the same class sits six lines above the caption, in a
code comment that ends «and the caption below is unchanged». It is true of TZ-14
and false the moment this TZ lands.

**What this TZ is NOT.** It changes no number, no threshold, no colour, no block
order and no decision. `abnormal` remains a printed word (inv. 27). One display
string is replaced by a true one, one comment clause is corrected, and the gate
gains a section that can catch the next denial of this kind before a human reads
the board.

---

## 2. Scope — two stages

### Stage A — the caption, and the comment above it

**A1.** In `boardHtml`, the `bd-note` line of «РИСК ВЫНОСА» (currently
`index.html:2856`) is replaced. The sentence that must render, decoded, is exactly
this and nothing else:

```
1,0 — обычный день: у броуновского блуждания E[хода] = σ·√(8/π), поэтому единица здесь не выбрана, а выведена. Порог, выше которого день назван вынесенным, — 90-й процентиль медианы списка по трёхлетнему архиву; это мера дня, а не запрет: на счёт, плечо и вердикт она не влияет. Список считается по 25 спотовым монетам: три фьючерсные в меру не входят.
```

The literal to write, `\uXXXX`-escaped for every character above U+007F exactly as
the surrounding code does:

```js
    sSqz += '<div class="bd-note">1,0 \u2014 \u043e\u0431\u044b\u0447\u043d\u044b\u0439 \u0434\u0435\u043d\u044c: \u0443 \u0431\u0440\u043e\u0443\u043d\u043e\u0432\u0441\u043a\u043e\u0433\u043e \u0431\u043b\u0443\u0436\u0434\u0430\u043d\u0438\u044f E[\u0445\u043e\u0434\u0430] = \u03c3\u00b7\u221a(8/\u03c0), \u043f\u043e\u044d\u0442\u043e\u043c\u0443 \u0435\u0434\u0438\u043d\u0438\u0446\u0430 \u0437\u0434\u0435\u0441\u044c \u043d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u0430, \u0430 \u0432\u044b\u0432\u0435\u0434\u0435\u043d\u0430. \u041f\u043e\u0440\u043e\u0433, \u0432\u044b\u0448\u0435 \u043a\u043e\u0442\u043e\u0440\u043e\u0433\u043e \u0434\u0435\u043d\u044c \u043d\u0430\u0437\u0432\u0430\u043d \u0432\u044b\u043d\u0435\u0441\u0435\u043d\u043d\u044b\u043c, \u2014 90-\u0439 \u043f\u0440\u043e\u0446\u0435\u043d\u0442\u0438\u043b\u044c \u043c\u0435\u0434\u0438\u0430\u043d\u044b \u0441\u043f\u0438\u0441\u043a\u0430 \u043f\u043e \u0442\u0440\u0451\u0445\u043b\u0435\u0442\u043d\u0435\u043c\u0443 \u0430\u0440\u0445\u0438\u0432\u0443; \u044d\u0442\u043e \u043c\u0435\u0440\u0430 \u0434\u043d\u044f, \u0430 \u043d\u0435 \u0437\u0430\u043f\u0440\u0435\u0442: \u043d\u0430 \u0441\u0447\u0451\u0442, \u043f\u043b\u0435\u0447\u043e \u0438 \u0432\u0435\u0440\u0434\u0438\u043a\u0442 \u043e\u043d\u0430 \u043d\u0435 \u0432\u043b\u0438\u044f\u0435\u0442. \u0421\u043f\u0438\u0441\u043e\u043a \u0441\u0447\u0438\u0442\u0430\u0435\u0442\u0441\u044f \u043f\u043e 25 \u0441\u043f\u043e\u0442\u043e\u0432\u044b\u043c \u043c\u043e\u043d\u0435\u0442\u0430\u043c: \u0442\u0440\u0438 \u0444\u044c\u044e\u0447\u0435\u0440\u0441\u043d\u044b\u0435 \u0432 \u043c\u0435\u0440\u0443 \u043d\u0435 \u0432\u0445\u043e\u0434\u044f\u0442.</div>';
```

**The caption does not print the number, deliberately.** `DAY_RANGE_ABNORMAL` keeps
exactly three code sites — declaration, `listExhaustion`, `dayStateNote` — and a
literal `1,39` in a static caption would be a fourth site of the same quantity in a
form no re-calibration could reach (inv. 20). The value is already printed one line
above by `dayStateNote` on the days it matters; the caption states what the line
MEANS, which is what a caption is for. `[решение принято мной]` Discarded: building
the caption by concatenation so it could name the number through
`numRu(DAY_RANGE_ABNORMAL, 2)` — it buys a repetition of a number the reader has
just read and costs the three-site enumeration the gate currently proves.

Nothing else in the block moves: no row, no colour, no order, no inline `style` on
the `.bd-sec`.

**A2.** Six lines above, the comment clause `, and the caption below is unchanged.`
becomes a statement that is true after this TZ and remains checkable:

```
    // inv. 19). The caption below states what the line MEANS and never repeats
    // the number: the constant keeps exactly three code sites (inv. 20), and a
    // caption may not deny a mechanism this block has (inv. 50).
```

### Stage B — gate section M, `bench/exhaustion_bench.js`

A new section **M. The caption denies nothing the block does (inv. 50)**, appended
after section L. It reuses L's `loadLive` / `liveBook` / `liveRender` /
`renderBoard` harness by name; no second render path is written. Every counter is
incremented at the comparison site (inv. 43), and every sub-check counts what it
compared and fails on zero (inv. 22).

**M1 — the block carries no denial.** Render the board on a quiet day and on a
loud day. Extract the whole «РИСК ВЫНОСА» `.bd-sec` — L already locates it by its
header and by `lastIndexOf('<div class="bd-sec', at)`. Decode `\uXXXX` is NOT
needed: the rendered HTML already carries real characters. Lower-case the block and
assert it contains none of these six phrases, each compared and counted separately,
on each of the two renders:

```
порога нет · сравнения нет · нет порога · нет сравнения · без порога · не сравнивает
```

**M2 — the caption states what remains true.** On the same two renders, assert the
caption substring contains the derived unit `\u221a(8/\u03c0)`, the words that
place it under inv. 27 («на счёт, плечо и вердикт»), and the coverage clause
(«25 спотовым монетам»). Assert the caption decodes to the §2 A1 sentence exactly,
as one string comparison, and print it verbatim once.

**M3 — the caption never repeats the number (inv. 20).** On the loud render:
`numRu(DAY_RANGE_ABNORMAL, 2)` occurs in the day line and does NOT occur anywhere
in the caption; on the quiet render it occurs nowhere in the block. Read the value
through the live context, never as a literal.

**M4 — the negative control, which is the point of the section.** Re-evaluate the
module in a second context from a copy of the source whose caption is rewritten
back to its `origin/main` text, and assert that M1 fires, names the phrase it
found, and that the clean source is silent. Same shape as section G's existing
control and section J's `9.99` control: a section that has never failed on purpose
is not yet a control.

**M5 — scope, asserted rather than assumed.** Assert that the scan ran over a
non-empty block on both renders and that the block it scanned is the one whose
header is «РИСК ВЫНОСА», not the whole board — a denial scan that silently widened
to the whole document would fire on English comments stating true absences (§3.11's
scratch probability legitimately has no threshold).

---

## 3. Non-goals — do not do these

1. **Do not touch `.github/workflows/calib.yml`, `bench/exhaustion_calib.py` or
   `bench/exhaustion-calibration.txt`.** `calib.yml`'s paths filter names the first
   two, so any edit re-fires the full three-year calibration on the branch and
   commits a fresh record on a longer archive, which can move the p90 off 1.39 and
   turn section I red. Editing either is a re-calibration, never a touch-up.
2. **Do not change `DAY_RANGE_ABNORMAL`,** its value, its declaration, its comment,
   or the bodies of `listExhaustion`, `dayStateNote`, `numRu`, `regimeBanner`,
   `marketRegime` or `update()`. Not one byte.
3. **Do not print the number in the caption.** Three code sites, unchanged.
4. **Do not let the day state reach a decision** (inv. 27). No veto, no penalty, no
   reordering, no colour on the regime line, no hidden card, no journal field.
5. **Do not touch the card list.** The caption lives on the board only; the list
   render must stay byte-identical to `origin/main` in every case.
6. **Do not add or reorder a board block, and do not put an inline `style` on a
   `.bd-sec`** (§3.7, inv. 15, 18, 19).
7. **Do not touch** `main.py`, `catalysts.json`, `journal/**`, `bench.yml`, the
   count of gate steps, or any bench other than `bench/exhaustion_bench.js`.
8. **Do not renumber** a section or an invariant, and do not fix the three
   pre-existing issues in §6.
9. **Do not widen the denial scan beyond the «РИСК ВЫНОСА» block.** A phrase
   blacklist over the whole file is a different and much worse instrument: it fires
   on comments and captions that state an absence which is still true, and a
   control that cries wolf is removed within two TZs.

---

## 4. Files

**Modified:** `index.html`, `bench/exhaustion_bench.js`.

**Created:** none. **Renamed:** none. **Deleted:** none.

---

## 5. Validation — written by the Architect, run by the Executor

Every item is mandatory and every count is reported. A validator that compared
nothing is a failure (inv. 22).

1. **Compiles and guards.** `python3 -m py_compile main.py`; `node --check` on the
   extracted `<script>` and on `exhaustion_bench.js`. ES5 guard and escape guard
   over every changed or added line of `index.html`: every on-screen character
   above U+007F is `\uXXXX`, every new comment is English. Both guards report the
   number of lines checked and fail on zero.
2. **The caption, decoded.** Print the rendered caption once, verbatim, and report
   the character-for-character comparison against the §2 A1 sentence. Report that
   the old caption occurs nowhere in `index.html`.
3. **The denial set.** Report the six phrases, the number of comparisons made, and
   the result on both renders. Report M4's negative-control output verbatim: the
   phrase it named on the reverted source, and the silence on the clean one.
4. **inv. 20 preserved.** Section L's enclosing-site enumeration re-run and its
   line printed: the identifier still occurs in exactly three code sites. Plus M3's
   two assertions.
5. **The card list did not move.** Render the card list on every regime × side
   combination at both a quiet and a loud day and report it byte-identical to
   `origin/main` in every one. This TZ touches the board only, so any movement here
   is a defect, not a delta.
6. **No-regression, identity first (inv. 45).** `prot_bench.js`'s unconditional
   identity run reports zero differences before anything else is offered as
   evidence. Then the whole-board differ against `origin/main` across the full
   scenario set. **The expected shape is unusual and is stated here so it is not
   read as a regression: the caption is unconditional, so EVERY board differs.**
   Report boards compared, boards differing only in the caption substring — which
   must equal boards compared — and boards differing anywhere else, which must be
   **zero**. Enumerate the distinct differing substrings; there must be exactly one.
7. **Purity (inv. 27), proven by perturbation.** TZ-14's protocol unchanged: scale
   `hi24`/`lo24` until `abnormal` flips and assert that for every coin `sc.score`,
   `vd.action`, `vd.why`, `dec.L`, `dec.binding`, `dec.moneyBelowMin`, `geo.rr`,
   `inv.price` and the card's number and tier are unchanged, and that the journal
   record `journal/write.js` would write is byte-identical. Report the number of
   fields compared and confirm the two-sided form: whatever the perturbation moves,
   it moves identically on `origin/main`.
8. **Extremes**, all ten: slider edges, null betas, truncated Gist, HTTP 400
   ticker, dead-market fields, missing coeffs fields, absent `btcStats`, absent
   `volatility`, `E ≤ 0`, non-finite `liq`. `update()` throws in none; the caption
   renders exactly once per board and never twice; a board with no metrics prints
   no caption and no new `NaN`.
9. **Full gate on a runner, 12 steps.** Baseline 1 250 613 measured from a
   `git worktree` at `origin/main`; candidate measured with the same harness.
   Report the per-step table and explain the delta term by term (inv. 43).
   **Steps 1–11 must all read unchanged, and that is an assertion, not an
   observation** — this TZ edits one display string and one bench, so any movement
   outside step 12 is a defect. Step 7 must read **691 109**.
10. **Release checklist** items 15 and 18 re-run and reported, plus item 11; and
    the `.bd-sec` of «РИСК ВЫНОСА» still carries no inline `style`, so the metal
    ring survives.

---

## 6. Pre-existing issues — confirm, do not fix

1. `NaN% от входа` at `E ≤ 0` in «ГРАНИЦЫ СДЕЛКИ» — unreachable live.
2. Raw Cyrillic literal in `bench/prot_bench.js`, line 177.
3. The Node 20 action pin in `bench.yml`, warning only.

Report each as confirmed-present. Report anything new found, and fix nothing.

---

## 7. Report

`CryptoReports/TZ-15-caption-truth-report.md`, straight to `main` where the session's
own permissions allow it; on a branch otherwise, saying so in one line.

Mandatory: the fingerprint gate result · scope executed and any deviation stated
plainly · the caption verbatim with its exact comparison · the six-phrase result
and the negative control's output · the three-site enumeration · the card-list
identity result · the whole-board differ counts with the single distinct differing
substring named · the purity field count · the 12-step table with steps 1–11
asserted unchanged and the step-12 delta explained term by term · **one line stating
whether the hosted `Bench gate` result was observable from the session, and its run
id if it was** · line counts and MD5s for `index.html`, `bench/exhaustion_bench.js`,
`main.py`, `catalysts.json`, `bench/exhaustion-calibration.txt` and the System Map ·
branch name and compare URL.

**NOT IN EFFECT UNTIL MERGED.**
