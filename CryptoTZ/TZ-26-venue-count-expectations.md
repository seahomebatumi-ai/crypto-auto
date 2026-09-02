# TZ-26 — Stale venue-count expectations and the §3.17 caption

**Canonical filename:** `CryptoTZ/TZ-26-venue-count-expectations.md`
**Class:** continues on the EXISTING branch `claude/tz-25-universe-morpho-arb`
(head `ea05962`). No new branch. One pull request for TZ-25 and TZ-26 together.
**Model:** Opus.
**Corrects:** TZ-25, which is not amended (§6 of the CANON hard rules). This TZ names it.

---

## 0. System Map fingerprint gate — BLOCKING

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-02-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `58. **A rule that names an object without naming how to compute it has named nothing.**` |

The map is unchanged at `2026-09-02-a` and is republished only after this branch
merges. `index.html` and `main.py` on the branch differ from the map's `## 0` table by
TZ-25's own edits, which report 2 records; that is expected and is not a gate failure.

---

## 1. Hard floor — the items this TZ touches, quoted from `EXECUTOR-INSTRUCTIONS.md`

**Read the contract first and confirm it is v19.** If `main` still carries v18, report
BLOCKED in one line: the two clauses below are v19 text and the work stands on them.

- **Item 3, v19** — universe membership changes only on an owner decision quoted in the
  TZ. Quoted here: the Boss's written instruction of 02.09.2026, «I am informing you that
  I have added two coins to my permanent list: MORPHO and ARBITRUM». Resulting count: 30.
  This TZ adds no coin; it repairs what TZ-25's addition made stale.
- **Item 2** — *«Never edit a bench to make it pass. A red bench is either a product
  defect or a stale expectation; both are findings, neither is a licence to change the
  assertion.»* **This TZ is the licence.** Report 2 established the finding — three
  assertions in `journal_bench.js` are pinned to a venue set of exactly three assets, the
  same run prints `монет 30 · cov 25 skip 5 · статус ok`, and no product behaviour is
  wrong. The assertions are updated because an accepted finding says they are stale, not
  because the gate is red. **If any of the three turns out to be a product defect on
  inspection, STOP and report** — the finding is what authorises this, and it is
  falsifiable.

No other hard-floor item is touched by this TZ.

---

## 2. Scope

### 2.1 `bench/journal_bench.js` — three stale expectations

Exactly the three sites report 2 names, no others.

| Line | Now | Becomes |
|---|---|---|
| 592 | `ok('fut:true активов ровно три', FUT.length === 3)` | asserts the set is **five**, kept as a literal |
| 641 | `eq('три формы: жива', whyCount(r, ALIVE), 1)` | expectation derived as `FUT.length - 2` |
| 644–645 | note expected to name `FUT[2].name` | note derived from `FUT.slice(2)`, joined `'; '` |

**Two are derived, one stays a literal, and the split is deliberate.** Lines 641 and
644 are consequences of the fixture's own construction — 6a.5 kills `FUT[0]` and drops
`FUT[1]`, so «alive» is structurally `FUT.length - 2` — and deriving them means the next
venue change moves no expectation at all. Line 592 must stay a hand-written number: an
assertion derived from the thing it checks reads `FUT.length === FUT.length` and controls
nothing (map inv. 22, a check that passes with no data).

Update the check's Russian label to match the number it now asserts.

### 2.2 The §3.17 caption — one sentence, two files, byte-identical

`index.html:2865` (as `\uXXXX` escapes) and `bench/exhaustion_bench.js`'s `CAPTION`
constant both become, character for character:

```
Список считается по 25 спотовым монетам: пять фьючерсных в меру не входят.
```

The spot count 25 does not move and never did — `listExhaustion` skips `fut:true` rows
ahead of every other test (map inv. 41). The futures count in the same sentence does, and
that is the whole repair.

**`CAPTION_MAIN` at `exhaustion_bench.js:1589` is NOT edited.** `[решение принято мной]`
It is section M's negative control — the wording that must fire the scan — and its value
comes from differing from the live caption. Discarded alternative: moving it too, which
would leave the control comparing a string against itself.

### 2.3 `bench/exhaustion-calibration.txt` — NOT edited, and this closes TZ-25's contradiction

`[решение принято мной]` TZ-25 §4.3 required updating universe counts in `bench/**` and
§4.4 forbade touching this file; report 1's obstacle 3 is correct that the two collide.
**The file is not edited, and the collision resolves in favour of §4.4.**

Line 1 reads `Universe: 25 spot of 28 declared tokens … : HYPE, XMR, LIT`. That sentence
is **true of the run that produced it** — calibration run #2, seed 20260823, 1 110 dates
— and the file is that run's output, pinned to `DAY_RANGE_ABNORMAL = 1.39` by the gate
(map inv. 46). Editing it to describe today's universe would rewrite a measurement to
match a later state, which is precisely the move inv. 46 exists to make impossible. A
measurement record describes the moment it was taken or it is not a record.

The map carries the consequence in its next revision, not this TZ.

### 2.4 Nothing else

No `tokens[]` change, no `TOKENS` change, no threshold, no workflow, no
`analyst/**`, no `catalysts.json`, no other assertion in any bench.

---

## 3. Expected gate movement

| Step | Predicted | Basis |
|---|---|---|
| 7 `journal_bench.js` | **693 895, failures 0** | the three assertions compare the same number of times; only the expected values move |
| 12 `exhaustion_bench.js` | **220 598, failures 0** | section M pins one exact string; changing that string's content changes no count |
| all others | unmoved from report 2's table | nothing else is touched |

**These are predictions, not requirements.** TZ-25 §5 predicted step 8 at +4 and measured
+1 630, because it reused a per-symbol term from a change of a different shape. The
requirement is attribution term by term (map inv. 43); a delta that does not match a
prediction is reported and explained, and a bench is never edited toward a predicted
number.

Total after this TZ is expected at **1 255 401**, the figure report 2 measured, with zero
failures.

---

## 4. Validation

1. `node --check` on the extracted `<script>` of `index.html`.
2. `python3 -m py_compile main.py` (unchanged by this TZ; run as the no-regression check).
3. Full `bench.yml` gate, 13 steps, **green**, with the per-step table and every delta
   attributed.
4. **The caption is byte-identical in the two files.** Prove it by comparison, not by
   reading: decode the `index.html` escapes and compare against `exhaustion_bench.js`'s
   `CAPTION` programmatically, and record the command.
5. **Section M's negative control still fires.** Plant `CAPTION_MAIN`'s wording into a
   copy and confirm the scan turns red; confirm the clean source is silent (map §3.17).
6. `journal_bench.js` still prints `монет 30 · cov 25 skip 5 · статус ok`, and neither new
   coin raises `hardSkip` (map inv. 41).

---

## 5. Report

`CryptoReports/TZ-26-venue-count-expectations-report.md`, straight to `main`.
It states the fingerprints the map's `## 0` table lists, the 13-step table, and the
pull-request URL for the combined TZ-25 + TZ-26 branch.

---

## Что сделать
1. Загрузить `EXECUTOR-INSTRUCTIONS.md` (v19) в корень репозитория
2. Загрузить `TZ-26-venue-count-expectations.md` в `CryptoTZ/`
3. В Claude Code отправить `EXECUTE TZ-26` — модель **Opus**
4. Прислать `CryptoReports/TZ-26-venue-count-expectations-report.md`
5. Слить pull request после моего вердикта — одним слиянием за ТЗ-25 и ТЗ-26
