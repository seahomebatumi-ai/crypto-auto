# ТЗ-08 — A count must be a count

**Canonical filename: `TZ-08-counts-are-counts.md`.** Commit the file under this
name regardless of the name it arrived under (§3 of the contract). Destination:
`CryptoTZ/`.

**Claude Code model: Opus.** The main scope rewires the counters of a 784-line
bench without moving one assertion, and one scope edits `index.html` — a file
that is otherwise forbidden. Both are places where a plausible-looking change is
wrong in a way no syntax check catches.

**Executor contract: Version 6.** Read it from the repository root before
anything else.

---

## 0. System Map fingerprint gate — blocking

Verify in `SYSTEM-MAP-CRYPTOCALCUL.md` **before any work**. On any mismatch:
STOP, report ЗАБЛОКИРОВАНО, state found versus required.

| Anchor | Required |
|---|---|
| `<!-- EDIT-MARKER 2026-08-22-COVERAGE-SEMANTICS -->` | present, exactly 1 occurrence |
| `<!-- EDIT-MARKER 2026-08-22-GATE-COMPOSITION -->` | present, exactly 1 occurrence |
| `## 4. Инварианты`, highest number | **43** |
| `## 9. Журнал миграций`, newest entry | `- 2026-08-22 (2):` |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1807 lines, MD5 `476339934c9dcf14e0f4bf2353900d89` |

Invariants **41, 42, 43** are new in this edition and none of 1–40 was renumbered
or reworded. Invariant 43 is the subject of this TZ.

Baseline for the diff, recorded in the report **before** any edit:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3522 | `a7b10d80bea67824cf9643842d2e505a` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 15 | `eb591d2ef2d792ca6a4a25f26442e9b9` |
| `bench/verify_board.js` | 190 | `9a371afb1bb3904b4e8fa3b316b64395` |
| `bench/board2_bench.js` | 195 | `b18a28ddd40ea8a9524f4f18f53720b5` |
| `bench/prot_bench.js` | 458 | `59e1f2af47dd3a75e2f1d954fd58c820` |
| `bench/verify_bench.py` | 248 | `5f3112a8767169c69245de2ea3cdc724` |
| `bench/direction_bench.py` | 784 | `34786b11afccfa5e84ef4158f8435e4c` |

---

## 1. Why this TZ exists

TZ-07 restored the controls. An independent audit of its result on 22.08 found
that two members of the same family survived it, and that the report's own list
of survivors was wrong in both directions. Both findings are measured, not
inferred.

**Defect 1 — four benches in the gate still exit 0 having compared nothing.**
`verify_board.js`, `board2_bench.js`, `prot_bench.js` and `verify_bench.py` have
no zero-comparison guard. A future edit that empties their case set leaves them
green. This is invariant 22 verbatim.

**Correction to the TZ-07 report, verified by execution:** `fresh_bench.js`
already has the guard (`if (checks === 0) … exit 1`), and `direction_bench.py`
has it in `main()`, which covers **every** block and not only `--display`. The
report listed both as unguarded. Do not add a second guard to either.

**Defect 2 — the gate's headline number is not a count.** Three blocks of
`direction_bench.py` return an estimate where a count belongs:

```
check_props     line 288   return …, r["checks"] * 8
check_fixtures  line 367   return …, len(rows) * 4
check_display   line 656   return …, r["lists"] * r["trades"] + len(r["tier"])
```

The last is a product of two unrelated quantities. The multipliers 8 and 4 are
assumptions about how many assertions run per scenario, and nothing enforces
them. Two further blocks — `check_control` and `check_sim` — return `len(res)`,
which is a **sample size**: a simulation of hundreds of thousands of paths ending
in three statistical assertions performs three comparisons, not hundreds of
thousands.

This matters for three reasons, any one sufficient. (a) The total is used as
evidence: TZ-07 reconciled `1 199 724 → 1 308 873` line by line, and an
accounting built on estimated terms is arithmetic theatre. (b) The count is the
input to the invariant-22 guard, so a number that moves for reasons other than
comparisons makes the guard decorative. (c) A number nobody can decompose cannot
be audited at all — which is the same failure mode as a green bench that
verified nothing, one level up.

**Defect 3 — a production comment contradicts the map.** `index.html` line 770
still explains `fut:true` for LIT as «статус спот-пары не подтверждён». §3.14
replaced that reasoning on 22.08 with a declaration, and invariant 41 now keys
the journal's classifier on it. A comment that states a superseded reason next to
the data it describes is how the next reader re-derives the wrong rule.

**Not in this TZ, measured and closed:** the TZ-07 report's risk 4 — that a
`confirmed` registry entry would move the three board benches — was tested by
flipping two live entries to `confirmed` with dates inside the window. All three
stayed at 109 / 130 / 168. `catalyst_bench.js` correctly went red, because a
`confirmed` entry without a source quorum violates invariant 39. The registry
population order is therefore unblocked and proceeds in parallel, not after.

---

## 2. Scope

Three scopes. If one is blocked, complete the others and report that one as
blocked (contract §6).

### Files to Modify

- `bench/verify_board.js` — scope A
- `bench/board2_bench.js` — scope A
- `bench/prot_bench.js` — scope A
- `bench/verify_bench.py` — scope A
- `bench/direction_bench.py` — scope B
- `index.html` — scope C, **comment text only**

### Files to Create / Delete

None. `image.PNG` is the PWA icon (contract §6).

### Explicitly out of scope

`main.py`, `catalysts.json`, `journal/**`, every workflow including `bench.yml`,
and every bench not named above. **No change to any formula, threshold, constant,
assertion or expectation anywhere in this TZ.** Scope C is the only edit to
`index.html` this TZ permits and it may not touch one executable character.

Action versions in the workflows stay as they are. The Node 20 deprecation
warning on the runners is a warning, and bumping the bot's workflow to silence it
risks the data pipeline for zero decision value today `[решение принято мной]`.

---

## 3. Scope A — the guard, in exactly four benches

**3.1** Each of the four must exit **non-zero** when it performed zero
comparisons, printing one grep-able line before it does. Use the counter each
file already keeps:

| File | Counter | Zero condition |
|---|---|---|
| `bench/verify_board.js` | `checks` | `checks === 0` |
| `bench/board2_bench.js` | `checks` | `checks === 0` |
| `bench/prot_bench.js` | `pass`, `fail` | `pass + fail === 0` |
| `bench/verify_bench.py` | `checks[0]` | `checks[0] == 0` |

**3.2** The guard sits immediately before the existing exit, after the summary
line is printed, so a red run still prints its own numbers. It may only ever make
a bench redder: no existing assertion, message or exit path changes.

**3.3** `prot_bench.js` runs some suites only when `index.html.prev` exists. The
guard is on the total of both counters, so an absent baseline stays legal — it is
zero *comparisons* that is illegal, not a skipped optional suite.

**3.4** Do not touch `fresh_bench.js`, `journal_bench.js`, `catalyst_bench.js`,
`display_bench.py`, `render_bench.py` or `direction_bench.py` for this scope.
They already guard. A second guard is not twice as safe; it is a second thing to
keep true.

---

## 4. Scope B — a count must be a count

**Rule, invariant 43.** The number a block returns as «проверок» is the number of
**comparisons it actually performed**, produced by a counter incremented at the
comparison site. It is never a multiplication, never an assumed assertions-per-
scenario factor, and never a sample size.

**4.1** Every block of `direction_bench.py` — `check_identity`, `check_props`,
`check_fixtures`, `check_display`, `check_control`, `check_sim` — returns such a
count. Where the comparison happens inside a sandboxed JS string, the counter is
incremented there and returned in the block's JSON, exactly as `ordFail` and
`badNo` already are.

**4.2** A block whose work is statistical reports **two** numbers: the count of
comparisons, which is what it returns and what enters the gate total, and its
sample size, printed in the message as `наблюдений: N`. Both are true; only one
of them is a check. `check_control` and `check_sim` are these blocks: their
statistical assertions are the comparisons, the simulated paths are the
observations.

**4.3** **The total will fall, and that is the correct outcome.** Do not
compensate, do not split an assertion in two to keep the number up, and do not
add a single new comparison anywhere in this TZ. Report the new total plainly
against TZ-07's `1 308 873` and account for every term.

**4.4** No assertion, threshold, fixture, seed, case count or failure condition
changes. If a block's honest count happens to equal its old expression — for
example if `check_fixtures` really does perform four comparisons per row — the
number is unchanged, and that identity is itself the proof the old expression was
right by accident rather than by construction. State which blocks landed that
way.

**4.5** Prove the counters move with the work: run one block with its case set
cut in half and show the count falls in the same proportion, then restore it and
show the original number returns. A counter that does not respond to the amount
of work is not a counter.

**4.6** If the same defect exists in another gate bench, you may fix it under
this identical rule — report-only numbers, no assertion touched — and must list
each such fix with its before and after. If it is anything more than that, report
it and leave it alone.

---

## 5. Scope C — the comment that outlived its reason

**5.1** In `index.html`, replace exactly these two lines:

```
    // XMR — спот делистнут Binance (2024) => fut:true.
    // LIT — статус спот-пары не подтверждён => fut:true.
```

with exactly these two:

```
    // XMR / LIT / HYPE — площадка ОБЪЯВЛЕНА: только фьючерсы (карта §3.14,
    // инв. 41). Живая строка зеркала объявление не отменяет.
```

Two lines in, two lines out: `index.html` stays at **3522 lines**. The
surrounding lines — the `ZEC / UNI` line above and the two-line `Правило:` note
below — are not touched.

**5.2** Nothing else in `index.html` changes. Every added and removed line must
match `^\s*//`. If any other line appears in the diff, revert the file and report
the scope as blocked rather than explaining the extra line.

---

## 6. Validation — written by the Architect, run in full by the Executor

Every item is mandatory. An item that cannot be run **fails**; it is never «not
applicable» (contract §9). Record the check count and exit code of each.

**6.1 Baseline.** Line counts and MD5 for every file in §2 before any edit, plus
the §0 map fingerprint.

**6.2 Syntax.** `node --check` on the `<script>` extracted from `index.html` and
on nothing else that changed in JS; `python3 -m py_compile` on both modified
Python files; `python3 -m py_compile main.py` with the file untouched.

**6.3 No-regression, proven not asserted.** `git diff --stat` shows zero changes
to `main.py`, `catalysts.json`, `journal/**` and `.github/**`. For `index.html`,
paste `git diff -U0 -- index.html` in full and state that every `+`/`-` line
matches `^\s*//`, with the line count unchanged at 3522.

**6.4 Scope A.** Run the four benches: counts and exit codes, which must be
`109 / 130 / 168 / 35` and `0`, unchanged from today. Then, per bench, force the
zero case (empty the case set in a scratch copy or short-circuit the loop), show
the non-zero exit and the printed line, revert, and show the file byte-identical
to its post-edit state and the bench green again.

**6.5 Scope B.** A table with one row per block: old expression, old number, new
number, and one line naming what is now counted. Then §4.5's proportionality
proof. Then the `--display` guard still fires at zero, unchanged from TZ-07.

**6.6 Scope C.** The full gate green on the edited `index.html`, and the new line
count and MD5 of the file.

**6.7 Full gate.** Every step of `bench.yml` in order with per-step counts and a
total. Reconcile against `1 308 873`: every term of the difference is either a
removed multiplier or a removed sample size, and nothing else is permitted to
move. If any other bench's number changes, stop and report it — that is a finding
(contract §7.2), not something to absorb.

**6.8 CI.** `Bench gate` executes on the branch push (TZ-07 §6 made this
automatic) and its conclusion is `success`. **Do not plant a failure this time:**
the gate's ability to fail was proven on the runner in TZ-07 run 29, and each
Scope A guard proof in §6.4 is itself a red-then-green control. Report the run
number, URL and conclusion.

---

## 7. Constraints

- Minimal diff through existing structures. No new dependency, no new file, no
  new abstraction, no refactor beyond the counters named in §4.
- ES5 only in anything that runs in the browser. This TZ adds no browser code at
  all — Scope C is a comment.
- Language: new bench text in English, except inside `direction_bench.py`, which
  is Russian throughout and stays Russian (precedent: TZ-07 §8). The Scope C
  comment is given verbatim in §5.1 and is Russian because `index.html` comments
  are.
- Never edit an assertion to make a bench pass, never remove a step from the gate
  to make it green (contract §7.2, §7.12).
- No new coins, no schema change, no touching a workflow.

---

## 8. Commit Message

```
fix(controls): a check count counts checks (TZ-08)
```

---

## 9. Report

`CryptoReports/TZ-08-counts-are-counts-report.md`, contract §10 format, including
`## CI Execution`. Commit it directly to `main` before the closing message.

State separately and without blurring: what was completed · what was skipped ·
what failed validation · what is a pre-existing defect · what remains a risk.
`## Fingerprints` is mandatory: line count and MD5 for `index.html`, `main.py`
and `SYSTEM-MAP-CRYPTOCALCUL.md`, plus the map's newest migration date.

If no pull request could be opened, apply the §8 fallback of contract Version 6:
branch name and compare URL, in the report **and** in the closing message, with
the CI consequence stated in bold.
