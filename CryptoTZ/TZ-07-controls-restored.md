# ТЗ-07 — Restore the executing controls

**Canonical filename: `TZ-07-controls-restored.md`.** Commit the file under this
name regardless of the name it arrived under (§3 of the contract). Destination:
`CryptoTZ/`.

**Claude Code model: Opus.** Four independent scopes across six files, one of
them a CI gate, plus a bench-expectation update that is only safe because this
document states the correct contract. Sonnet is not appropriate here.

**Executor contract: Version 6.** Read it from the repository root before
anything else. Version 6 adds a defined pull-request fallback (§8), a CI
execution heading in the report (§9, §10), and two hard-floor items (§7.11,
§7.12) that this TZ depends on.

---

## 0. System Map fingerprint gate — blocking

Verify in `SYSTEM-MAP-CRYPTOCALCUL.md` **before any work**. On any mismatch:
STOP, report ЗАБЛОКИРОВАНО, state found versus required.

| Anchor | Required |
|---|---|
| `<!-- EDIT-MARKER 2026-08-22-VENUE-CONTRACT -->` | present, exactly 1 occurrence |
| `<!-- EDIT-MARKER 2026-08-22-CATALYST-REGISTRY -->` | present, exactly 1 occurrence |
| `### 3.14 Asset venue contract` | present |
| `### 3.15 Catalyst registry as data` | present |
| `## 9. Журнал миграций`, newest entry | `- 2026-08-22:` |
| `## 4. Инварианты`, highest number | **40** |

The map was rebuilt on 22.08: `§3.10` moved into numeric order and the invariant
list was sorted ascending. **No invariant was renumbered and no invariant text
changed** — every existing reference in code, benches and reports stays correct.

Baseline for the diff, to be recorded in the report before you change anything:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3522 | `a7b10d80bea67824cf9643842d2e505a` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 15 | `eb591d2ef2d792ca6a4a25f26442e9b9` |

---

## 1. Why this TZ exists

TZ-06 was correct work. It also reached `main` with **zero controls having
executed on a runner**, and it surfaced three more places where a check looks
green while verifying nothing. That is the invariant 22 / 25 / 29 / 37 family,
and it is the only family in this project that gets worse silently.

Four defects, each independently sufficient to justify the work:

1. **The journal's `status` field is degraded every day on a healthy system.**
   The mirror still serves a delisted, zero-volume row for `XMRUSDT` and
   `LITUSDT`, the classifier reads that as `dead market`, and `dead market`
   counts as a hard skip. `status` will therefore read `partial` on every run
   forever. A field that says «degraded» unconditionally carries no information,
   and the field exists precisely so that a real gap is visible.
2. **Three board benches execute the board with an empty catalyst registry.**
   `verify_board.js`, `board2_bench.js` and `prot_bench.js` have no
   `XMLHttpRequest` in their sandboxes, so the loader fails and `CATALYSTS`
   stays `{}`. Today that is harmless because every entry is `disputed`. The
   moment one entry becomes `confirmed`, these three validate a configuration
   that is not production — and they were built specifically to reproduce the
   Boss's live board.
3. **`bench.yml` does not run on a branch without a pull request.** Its triggers
   are `push` to `main` and `pull_request`. TZ-06's 1 199 724 checks passed on
   the Executor's machine and on no runner at all before the merge.
4. **The display contract has no executing control whatsoever.**
   `display_bench.py`, `render_bench.py` and `direction_bench.py --display` are
   all excluded from the gate as «red on the current `index.html`». They are red
   on **stale expectations**, not on a product defect: they encode the 19.08 (3)
   contract, which invariants 33 and 34 explicitly reversed. So the single most
   Boss-visible contract in the system — rewritten twice in two days after two
   live misreadings — is currently unguarded, and invariant 37 says a bench
   outside the gate is not a control.

Ordering note: this precedes filling `catalysts.json` with sources. The first
`confirmed` entry changes a verdict, and changing verdicts while the controls
are down is exactly the sequence §10 forbade itself when it put the journal
before the registry.

---

## 2. Scope

Four independent scopes. If one is blocked, complete the others and report that
one as blocked (contract §6).

### Files to Modify

- `journal/write.js` — scope A
- `bench/journal_bench.js` — scope A
- `bench/verify_board.js` — scope B
- `bench/board2_bench.js` — scope B
- `bench/prot_bench.js` — scope B
- `bench/display_bench.py` — scope C
- `bench/render_bench.py` — scope C
- `bench/direction_bench.py` — scope C
- `.github/workflows/bench.yml` — scopes C and D

### Files to Create

None.

### Files to Delete

None. In particular `image.PNG` is the PWA icon (contract §6).

### Explicitly out of scope

`index.html`, `main.py`, `catalysts.json`, `journal/data/**`,
`journal/out/**`, `journal/runs.jsonl`, and every workflow other than
`bench.yml`. **No production logic changes in this TZ at all.** If a scope below
appears to require touching `index.html`, the TZ is defective — report BLOCKED.

---

## 3. Scope A — coverage semantics keyed on the venue declaration

**Authoritative statement of the contract.** System Map §3.14 fixes XMR, LIT and
HYPE as Binance Futures only; the other 25 are Binance Spot. A skip on a
`fut:true` asset is therefore **declared coverage**, not a discovered fault,
*whatever form it takes* — an absent row, or a ghost row for a pair that is
delisted but still served by the mirror.

**3.1** In `journal/write.js`, the `fut:true` test must be evaluated **before**
the dead-market test, so that a `fut:true` asset never reaches a branch that
increments `hardSkip`. The current order is: absent row → dead market → no bot
row → error flag → no metrics. `fut:true` must short-circuit ahead of all of
them.

**3.2** The reason string still records what was actually observed. Invariant 37
requires the gap to be *measured*, not assumed, so «futures-only» alone is not
enough. Use exactly these strings:

```
no row at all          futures-only: no spot mirror pair
row present, dead      futures-only: delisted spot mirror row
row present, alive     futures-only: spot mirror row unexpectedly alive
```

The third case must not silently pass as normal. It records the skip, does not
increment `hardSkip`, and additionally sets `run.note` to
`fut:true asset trading on spot: <SYM>` so the anomaly reaches `runs.jsonl`.
A relisting is a `tokens[]` decision for the Architect, never yours (§7.11).

**3.3** A non-`fut` asset's classification is unchanged in every respect. Do not
touch the ordering, the strings or the counters on that path.

**3.4** Consequence to verify, not to assume: on a healthy day
`hardSkip === 0`, so `status === 'ok'`, `cov === 25`, `skip === 3`. Prove it by
executing, not by reading the code.

**3.5** Extend `bench/journal_bench.js` with cases that pin all three strings and
the counter behaviour, including a synthetic run in which a `fut:true` asset
returns a live row. **Do not weaken any existing assertion** — the new cases are
additions.

---

## 4. Scope B — registry parity in the board benches

**4.1** `verify_board.js`, `board2_bench.js` and `prot_bench.js` must execute the
board against the **real `catalysts.json` from the checkout**, by the same
technique `journal/write.js` already uses: read the file, validate it, and inject
the parsed `items` into the sandbox context. Do not add `XMLHttpRequest` stubs
and do not reimplement the loader — one mechanism, already written, reused.

**4.2** If `catalysts.json` is missing or invalid, these benches **fail with a
non-zero exit**. They must not fall back to an empty registry: a bench that
quietly validates a different configuration than production is the defect this
scope exists to remove (invariants 22, 40).

**4.3** Every existing assertion and every existing check count stays. The
expected outcome is that all three stay green with their current numbers
(108 / 129 / 167) because all live entries are `disputed` and therefore veto
nothing. **If any number changes, stop and report it** — that would mean the
empty registry had been masking a difference, which is a finding, not something
to absorb.

**4.4** Add one assertion to each of the three: the registry actually loaded and
is non-empty. A parity fix that silently degrades to `{}` reproduces the original
defect one layer down.

---

## 5. Scope C — the display contract back under an executing control

**This is the one place in this TZ where bench expectations change.** Contract
§7.2 forbids editing a bench to make it pass; that prohibition covers changing an
assertion to match code. It does not cover updating an expectation the Architect
has re-specified — and this section is that re-specification. Update the
expectations to the contract stated here. **Do not update them to whatever
`index.html` currently prints.** If production disagrees with the statement
below, production is the defect: stop and report it.

**5.1 Authoritative display contract — invariants 33 and 34, edition 20.08.2026.**

```
tier word     score >= TIER_STRONG (70)  ->  Сильный    var(--green)
              score >= TIER_MID    (50)  ->  Средний    var(--cyan)
              score >= TIER_MIN    (35)  ->  Кандидат   var(--accent)
              otherwise                  ->  Фон        #888
              boundaries are INCLUSIVE at the lower edge

badge         <tier> [#<no>] — <round(score)><glyph>
              " #<no>" present if and only if row.no > 0
              the separator is an em dash U+2014, with a space on both sides

colour        action === 'none'  ->  #888 for the whole badge
              otherwise          ->  the tier colour above

glyph         trade -> empty      wait -> "~ $<price>"      none -> "✕"

numbering     place in the SCORE ranking of the side's shown list,
              contiguous 1..N, ordered strictly by score
              (tie window 0.05 resolved by market-cap rank).
              Present on EVERY shown scored row.
              Absent ONLY on: rows with no score, and rows collapsed as
              irrelevant to the side (row.off).
```

**5.2 Three expectations are stale and must be replaced.** Each was correct under
the 19.08 (3) contract and was reversed by invariant 34 on the same day.

| Stale expectation | Correct contract | Where |
|---|---|---|
| lowest tier is `Наблюдать` | lowest tier is **`Фон`** | `display_bench.py` `TIER_WORDS` and the `want` list; `render_bench.py` `TIER_WORDS`; `direction_bench.py` `want` map |
| rank sits immediately after `>` — `RANK_RE = r'>#(\d+) '` | rank sits **after the tier word**, before the em dash | `display_bench.py` `RANK_RE` |
| only actionable rows are numbered; **no coin is numbered on both sides** | every shown scored row is numbered, **per side independently**; a coin may hold a number on both lists | `display_bench.py --display` block; `direction_bench.py --display` block |

On that last row, be precise about what is *not* changing: invariant 30 stands
untouched. **One coin still never receives both ЛОНГ and ШОРТ.** What was
reversed is only that the number stopped being a trade assertion and went back to
being a place in the ranking. The one-side guarantee is carried by `action`, and
its assertion in every bench stays exactly as it is. Do not relax it.

**5.3** Once green, wire all three into `.github/workflows/bench.yml` as separate
named steps, under `shell: bash -euo pipefail` like every existing step:
`display_bench.py`, `render_bench.py`, `direction_bench.py --display`. Remove the
three corresponding lines from the file's header comment listing what is
deliberately excluded, and leave the remaining exclusions
(`backtest_bench.py`, `badge_bench.js`, `clean_bench.py`,
`direction_bench.py --identity`) untouched with their reasons intact.

**5.4** If any of the three cannot be made green by the changes in 5.2 alone, do
not extend the fix and do not wire that bench in. Complete the others, and report
the residue under `## Remaining Risks` with the exact failing assertions. A
half-understood green is worse than a documented red.

---

## 6. Scope D — the gate runs on the branch

**6.1** In `.github/workflows/bench.yml`, add `claude/**` to the `push` branch
list so the gate executes on every Executor branch push, with or without a pull
request:

```yaml
on:
  push:
    branches: [ main, 'claude/**' ]
```

The existing `paths-ignore` block and the `pull_request` trigger stay exactly as
they are. Do not broaden to `'**'`: the journal's own daily commits land on
`main` and are already handled by `paths-ignore`, and a wildcard would add
runner minutes with no additional coverage.

**6.2** Cost, stated so it is a decision and not an accident: every branch push
now spends one runner execution of the full gate. At this project's rate — a few
pushes per TZ — that is a few minutes per task against a defect class that has
already let an entire unvalidated change reach production once.

---

## 7. Validation — written by the Architect, run in full by the Executor

Every item is mandatory. An item that cannot be run **fails**; it is never «not
applicable» (contract §9). Record the check count and exit code of each.

**7.1 Baseline.** Record line counts and MD5 for every file in §2 before any
edit, and confirm the §0 fingerprints.

**7.2 Syntax.**
- `node --check` on the `<script>` block extracted from `index.html` — must pass
  **and** `index.html` must be byte-identical to baseline (it is out of scope).
- `python3 -m py_compile main.py` — must pass, file untouched.
- `node --check journal/write.js` and on each modified `bench/*.js`.
- `python3 -m py_compile` on each modified `bench/*.py`.

**7.3 No-regression statement, mandatory and explicit.** This TZ changes no
production logic. Prove it, do not assert it: `git diff --stat` must show
**zero** changes to `index.html`, `main.py` and `catalysts.json`. State this
in the report as a sentence with the command output beside it.

**7.4 Scope A.**
- `node bench/journal_bench.js` — full count, 0 failures, new cases included.
- Execute `journal/write.js` in the mode that produces a snapshot without
  writing a new dated file, and show that on the current data
  `hardSkip === 0`, `status === 'ok'`, `cov === 25`, `skip === 3`, with the three
  skip lines carrying the exact strings from §3.2.
- Negative control: force each of the three `fut:true` branches synthetically and
  show the string and counter for each, including the «unexpectedly alive» case
  and its `run.note`.
- Confirm no dated journal file was created or modified by any of this
  (invariant 38 — the record is immutable, and validation never writes to it).

**7.5 Scope B.** Run all three benches; report counts and exit codes. They must
read the real registry, and each must carry the new non-empty assertion.
Negative control: move `catalysts.json` aside, run each of the three, show a
non-zero exit and the message, restore it, show green again.

**7.6 Scope C.** Run `display_bench.py`, `render_bench.py` and
`direction_bench.py --display`; report counts, failures and exit codes. Each must
fail on zero comparisons (invariant 22) — state the count it verified.
Negative control per bench: inject one deliberate deviation from §5.1 into a
copy of the expectation, confirm the bench turns red, revert, confirm green.

**7.7 Scope D — the gate must be proven to fail.** Contract §9: a gate never
proven to fail is not a gate. Push a branch containing a deliberate failure in
one bench, confirm `Bench gate` runs **on the branch** and its conclusion is
`failure`, revert, confirm it runs and passes. Report both run URLs. This is the
only proof that accepts nothing local.

**7.8 Full gate.** Every step in `bench.yml`, in order, with per-step counts and
a total. Compare against TZ-06's total of 1 199 724 and account for the
difference.

**7.9 CI execution.** Report which workflows executed on a GitHub runner and
their conclusions. If `Bench gate` did not execute on a runner, `## Status` is
PARTIAL regardless of how complete the implementation is (contract §9).

---

## 8. Constraints

- Minimal diff through existing structures. No new dependency, no new build step,
  no new abstraction.
- ES5 only in anything that runs in the browser. `journal/write.js` and the JS
  benches run under Node and keep their current style.
- Language: new code comments and any new bench text in English. Edits inside
  `journal/write.js` continue in Russian — that file is Russian throughout, and
  consistency beats the rule inside a single file (the precedent is TZ-06 §7.8).
- Russian UI strings in JS remain `\uXXXX` escapes. This TZ should not create any.
- Never edit a bench assertion to make it pass, never remove a step from the
  gate to make it green (contract §7.2, §7.12). Scope C changes expectations
  **only** where §5.1 re-specifies them.
- No new coins, no schema change, no touching the four workflows other than
  `bench.yml`.

---

## 9. Commit Message

```
fix(controls): benches that verify nothing are not controls (TZ-07)
```

---

## 10. Report

`CryptoReports/TZ-07-controls-restored-report.md`, contract §10 format,
including the new `## CI Execution` heading. Commit it directly to `main`
before the closing message.

State separately and without blurring: what was completed · what was skipped ·
what failed validation · what is a pre-existing defect · what remains a risk.
`## Fingerprints` is mandatory: line count and MD5 for `index.html`, `main.py`
and `SYSTEM-MAP-CRYPTOCALCUL.md`, plus the map's newest migration date.

If no pull request could be opened, apply the §8 fallback of contract Version 6:
branch name and compare URL, in the report **and** in the closing message, with
the CI consequence stated in bold.
