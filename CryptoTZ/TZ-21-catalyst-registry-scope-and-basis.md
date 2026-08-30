# TZ-21 — Catalyst registry: scope rules, `basis` field, ENA entry

Supersedes the unmerged branch of TZ-20. That branch is **not merged and not
rebased** — its evidence lives in `CryptoReports/TZ-20-catalyst-registry-content-report.md`
on `main`, which is what it was for. Branch from `main`.

---

## 0. Baseline fingerprint

Quoted in full from `SYSTEM-MAP-CRYPTOCALCUL.md` §0. Match every anchor as an exact
substring against the repository copy before any work (contract §5); any mismatch is
BLOCKED.

**Revision 2026-08-30-b.** Baseline: TZ-19 merged into `main`; implementation commit
`cc8bade`, report `CryptoReports/TZ-19-gate-script-under-gate-report.md`.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-30-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `54. **A record cannot contain the outcome of the action that stores it.**` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Gate at this revision: `bench.yml`, **13 steps, 1 250 717 checks** — steps 1–12 sum to
**1 250 677**, step 13 reads **40**.

---

## 1. Scope — exactly two files

| Path | Authorised change |
|---|---|
| `bench/catalyst_bench.js` | the `basis` assertions of §3.A; two scope rules appended to the editing-rules block comment; whatever `QCASES` rows §5.5 requires |
| `catalysts.json` | one `ENA` entry added; `updated` bumped |

**No other file.** Not `index.html`, not `main.py`, not any workflow, not the map, not
`EXECUTOR-INSTRUCTIONS.md`, not anything under `analyst/`. The map and contract edits
this TZ implies are the Architect's and are made outside this branch.

---

## 2. Standing rulings this TZ writes

These are Architect decisions, recorded here because the Executor implements them and a
future reader must find the reason next to the rule.

### Rule 1 — the registry carries COIN-SCOPED events only

A market-wide event — a macro release, a central-bank decision, an index rebalance —
never enters `catalysts.json`. Market-wide risk is already measured, by §3.12 Layer 0
(`marketRegime`), and a per-coin veto is the wrong instrument for it: a `dir:'both'`
macro entry would close both sides on all 28 coins for fifteen days out of roughly
forty-five.

**A `"*"` key is therefore not a missing feature. It is out of scope permanently**, and
the `items key "<sym>" is in tokens[]` assertion that refuses it is correct rather than
a limitation to work around. TZ-20's NFP and FOMC rows are closed by this rule, not
deferred.

### Rule 2 — the registry carries RESOLVING events only

An event qualifies when something the market prices becomes **known or irreversible on
`d`**: an unlock releases supply, a governance vote concludes, a listing goes live, a
court or an agency issues a decision.

An administrative milestone on the path to such an event does **not** qualify — a
comment-period deadline, a filing date, a hearing being scheduled. Nothing resolves on
that date, so a veto would spend fifteen days of both sides on a non-event.

**TZ-20's `ONDO` row is closed by this rule.** The Federal Register document is real and
its `comments_close_on` is 2026-10-20, as TZ-20's report measured; the date is not in
doubt. The event is. Consequently:

- `regulatory` is **not** added to `KINDS` — the map's open-ended `…` is a defect the
  Architect repairs in the map, and an enum value with no admissible consumer is the
  same speculative widening §7 of TZ-20 forbade for hosts;
- `federalregister.gov` is **not** added to `PRIMARY` — that host arrives with the entry
  that needs it, and under Rule 2 no such entry is coming from this line of work.

Reversal path, one line: if the Boss judges an SEC comment deadline to be a resolving
event for ONDO, Rule 2 gains the exception and the host, the enum value and the entry
arrive together in one TZ.

### Rule 3 — a `disputed` entry must carry its own argument

Map §3.15 says entries no host confirms are deleted rather than demoted, because a
`disputed` entry keeps printing an argument built on a date nobody confirms. That
sentence was written for an entry with **no primary standing at all**, and it stays
correct for that case.

It does not fit a second case the map has not yet named: **the primary publishes the
mechanism but not the calendar.** `docs.ethena.fi` publishes a 25 % cliff one year after
TGE on 2024-03-05 followed by three years of linear monthly vesting; monthly steps from
that anchor fall on the 5th. The date is derived from a primary-published rule, not
asserted against silence.

So the classes split, and the split is what makes the second one safe:

| Case | Treatment |
|---|---|
| no primary publishes the event at all | delete the entry (map §3.15 unchanged) |
| primary publishes the mechanism, not the date | `conf:'disputed'` permitted, **`basis` mandatory** |
| primary publishes the date | `conf:'confirmed'` per inv. 39 |

`basis` records the derivation in the file, so §3.15's objection is answered where it was
raised: the argument is no longer unrecorded. It is also inside `cat.hash`, so it sits
next to every journaled verdict (§3.13).

---

## 3. Changes

### 3.A `bench/catalyst_bench.js`

**A1 — the `basis` field.** Add to the per-entry schema block:

- if `conf === 'disputed'`, `basis` MUST be present, a string, non-empty after trim, and
  ASCII-only;
- if `basis` is present at any `conf`, it MUST be a string, non-empty after trim,
  ASCII-only, and at most 300 characters;
- `conf === 'confirmed'` neither requires nor forbids it.

Every assertion names the offending entry as the existing ones do (`SYM[i] …`).

`basis` is additive and no production file reads it (inv. 1, inv. 9). Prove that rather
than assert it — see §5.4.

**A2 — the editing-rules block comment.** Append Rules 1, 2 and 3 of §2, in the file's
own English, next to the existing clause «`src` must support the date in `d`, not merely
the existence of the event». Rule 3 states plainly that a derived date is supported by
the rule it is derived from **only when the derivation is written into `basis`**.

Nothing else in this file moves. `PRIMARY` is untouched. `KINDS` is untouched. `isPrimary`
is untouched.

### 3.B `catalysts.json`

One entry under `ENA`, and `updated` → the date of the commit.

```
d      2026-09-05
dir    short
kind   unlock
conf   disputed
t      "Разблокировка ENA 05.09 — расчётная дата"   (\uXXXX-escaped, ASCII file)
src    ["https://docs.ethena.fi/overview/ena/tokenomics"]
added  <commit date>
basis  "Primary publishes vesting policy only: 25% cliff 1y after TGE 2024-03-05,
        then 3y linear monthly; monthly steps fall on the 5th. No dated calendar is
        published. Date asserted by the Boss on 2026-08-30 on that derivation."
```

`basis` is ASCII as written and needs no escaping. `t` carries «расчётная дата» because
the board is where the reader meets this entry and the derived status must reach the
reader, not only the file.

**The 2026-09-02 of TZ-20 is not used.** No source reached it, and TZ-20's own report
recorded the arithmetic that puts the step on the 5th.

`conf` is `disputed` and this is not negotiable inside the implementation: inv. 39 grants
`confirmed` on a primary source that supports the date, and an owner's assertion is not a
source. The registry is externally editable and `confirmed` is its compensating control;
a flag that can be set by assertion is not a control. `disputed` annotates SHORT on ENA
and vetoes nothing (inv. 31, 39).

---

## 4. Explicitly NOT in scope

- No external fetch of any kind. **This TZ requires none** — every fact it rests on is
  already recorded in TZ-20's report on `main`. Do not fetch to re-verify; if you believe
  a fetch is required to complete this TZ, that is a BLOCKED report, not a fetch.
- No new host in `PRIMARY`. No new value in `KINDS`. No `"*"` key. No `ONDO` entry.
- No change to `catalystCheck`, to `index.html`, or to any workflow.
- Do not merge, rebase or cherry-pick `claude/tz-20-catalyst-registry-content`.

---

## 5. Validation

Run every item. None is skippable and none is «not applicable».

1. **Baseline first.** Replay all 13 gate steps on the unmodified tree and report each
   step's own counter. Steps 1–12 must sum to **1 250 677** and all 13 to **1 250 717**.
   If they do not, stop and report — the branch base is wrong.
2. `catalysts.json` parses; symbol and entry counts before and after.
3. The file is ASCII-only, proven by a byte count above 127, which must be **0**.
4. `node --check bench/catalyst_bench.js` exits 0. Then grep every production file
   (`index.html`, `main.py`, `journal/write.js`) for `basis` and report **zero matches** —
   this is the inv. 1 / inv. 9 proof that the field is invisible to production.
5. Catalyst bench check count before and after, **attributed term by term** (inv. 43).
   The expected shape is: `+2` per-symbol, `+10` per-entry schema, `+1` quorum, `−1` on
   the silent-symbol sweep as it falls 27 → 26, plus the new `basis` assertions and any
   `QCASES` rows you add. A term you cannot name is a finding, not a rounding.
6. **Negative control on `basis`, four cases, each proven able to fail:** `basis` absent
   at `conf:'disputed'` · `basis` present but empty · `basis` non-string · `basis`
   carrying a non-ASCII byte. Each must exit non-zero and name `ENA[0]`. Restore the file
   byte-identical and record the md5 before and after.
7. Full `bench.yml`, all 13 steps. Only step 8 may move. **Step 7 must hold at 691 109
   and step 12 must move by exactly 0** (§0).
8. `git diff --stat` — exactly the two files of §1.
9. The three unchanged files of §0 byte-identical; new hash for `catalysts.json`.
10. Standing checks, map §6 item 1: `python3 -m py_compile main.py`; `node --check` on the
    `<script>` extracted from `index.html`.

**Do not run a market analysis.** Nothing under `analyst/` is read, written or consulted.

---

## 6. Acceptance criteria

1. `ENA` is in the registry at `2026-09-05`, `conf:'disputed'`, carrying a `basis` that
   states the derivation.
2. `basis` is asserted by the gate, and its absence at `conf:'disputed'` is proven to turn
   the gate red.
3. `basis` appears in no production file.
4. `PRIMARY`, `KINDS` and `isPrimary` are byte-identical to `main`.
5. The check-count delta is attributed term by term, with steps 7 and 12 unmoved.
6. The hosted `Bench gate` is green on the branch head, reported with run id and head SHA.
7. No external fetch was performed.

---

## 7. Hard floor

Unchanged and binding. Two are live here:

- **Item 2 — a bench is never edited so that a new input passes.** §3.A adds assertions
  and weakens none. If the ENA entry fails an existing assertion, the entry is wrong, not
  the bench.
- **Item 9 — no in-session fetch.** This TZ asks for none. The clause's own premise
  (inv. 44) is under Architect review after TZ-20's measurement; until that review lands
  the clause binds as written, and this TZ is built so the question never arises.

---

## 8. Report

Per contract §4a. One addition: the report must **not** state the outcome of its own
commit or push to `main` (inv. 54 read forward — see TZ-20's report, which did). State
what you did; the next record states that it landed.

---

## 9. Branch, commit, PR

- Branch from `main`: `claude/tz-21-catalyst-registry-scope-and-basis`
- Commit message, verbatim:
  `feat(catalysts): ENA derived-date entry, basis field, registry scope rules (TZ-21)`
- Open a pull request if `gh` is available; otherwise report the compare URL, per §8 of
  the contract.

**NOT IN EFFECT UNTIL MERGED.**
