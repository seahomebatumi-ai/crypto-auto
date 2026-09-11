# TZ-39 — Transport outcome decided after the last failing step, and a retry budget that prints

**Canonical filename: `TZ-39-transport-outcome-and-budget.md`.** Name the committed file
from this line, never from the name it arrived under (contract §3).

**Model: Opus.** Multi-site state machine with a data-loss direction; not a mechanical edit.

---

## 0. Fingerprint gate — blocking, before any work

Required map revision, matched as an exact substring against the repository copy
(contract §5):

**Revision 2026-09-10-a.**

Content anchors — all seven, each matched as an EXACT substring. **Report the matched
substring, not the verdict**: an anchor reported as present without the string it matched
is what §10 records as worse than a mismatch.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-10-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` |

The map's `## 0` file table — measure each at the stated line count and MD5; a difference
is reported under `## Pre-existing Issues` and is **not acted on** (contract §5):

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Benches carry no row in that table by decision (map §0), so this TZ states the two figures
it needs in its own §0. These are **reported, not enforced**:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4555 | `deac9dd8a53f2047c25c2d6fb24f09b4` |
| `bench/backtest_guard_bench.py` | 1726 | `ce08dd99edebfa90d8fce3dd6b7ba472` |

Contract in force: **v20**, 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0`.
Gate at this revision: `bench.yml`, 14 steps, **1 335 964** checks; step 14 = **323**,
step 4 = **40**.

---

## 1. Why

TZ-38 gave the fetch layer three outcomes where the code had two, and §10 carries two
residuals of it, both measured, neither closed. This TZ closes both.

**The first is inv. 70 inverted at the one place it may not be.** `_http` sets
`rec["ok"] = True` **before** `rec["json"] = r.json()`, so a `want_json` call whose body
does not parse raises into the caught branch — which sets `status: None`, `content: b""`
and `why`, and never clears `ok`. The call retries to exhaustion and returns
`ok: True, status: None, json: None`. `_tx_add` moves `exhausted` only on `not ok`, so an
exhausted request is folded in as an answered one and `won_clean` stays true: a request
that never completed is counted as data. Three callers reach it and each fails a different
way downstream — `_rest_rows` returns an empty transport record, `fetch_cg` raises
`TypeError` on `"%d" % None`, and `reconcile` passes its own `ok` check and then
dereferences `None`, which is the traceback TZ-38 §6 exists to remove.

**The second is that the layer has no reading of its own.** The `ретраи потратили S с из
BUDGET` line sits inside `if dead:`, so on the dispatch of 09.09 — 31 of 31 coins, nothing
lost — it did not print, and whether the transport served one attempt per URL or three
hundred is unknown. Inv. 70 requires the seconds spent to be PRINTED: a constant whose
consumption nobody can see is a constant nobody can move. The same shape makes TZ-38's own
code unobservable — its only visible signature today is a line that prints exactly when a
coin dies, and nothing died.

---

## 2. Scope

**Files to Modify:** `bench/backtest_bench.py`, `bench/backtest_guard_bench.py`.
**Files to Create:** none. **Files to Delete:** none.

Three scopes, independent (contract §6): if one is blocked, complete the others and report
it blocked.

`.github/workflows/backtest_bench.yml` is **not named by this TZ** and stays closed under
hard floor item 8. No bench file is added, so item 12's wiring clause does not fire.

### `## Touches`

- `bench/backtest_guard_bench.py` — section H asserts `_http`'s outcomes and is gate step 14.
- `bench/verify_bench.py` — it imports `backtest_bench.py` at scope (map §0), which is how a
  change here turns gate step 4 red. It is named because omitting exactly this file from a
  `Touches` list cost TZ-34 a whole extra specification (§10). This TZ does not authorise
  editing it; it authorises running it.

---

## 3. Scope A — the outcome is decided after the last step that can fail

**A1.** Move the success flag so it is set only when every step the call performs has
succeeded, the body parse included. This is the shape inv. 70 now carries: *the outcome is
decided after the LAST thing that can fail.*

**A2. No field survives the failure that should have cleared it.** Clearing `ok` in the
caught branch repairs one field; the class is repaired by every exit path of `_http`
setting every field the record carries, so no value from an earlier attempt or an earlier
stage can stand beside a failure. Enumerate the record's fields and the exit paths you
found, in the report.

**A3. A status is not a failure, and this repair may not convert one into the other.** A
reply is data whatever its status (inv. 70): a response that arrived is answered, carries
its status, and the caller decides what the status means. `404` on a monthly ZIP stays
ABSENT, is not retried, is not folded as exhausted, and the census still counts it and
refills from the dailies. Therefore the body is parsed — and a parse failure is a failure
of the call — **only where the status says a payload is there**. Without this clause the
repair turns every `404` page served as text into an exhaustion and the middle outcome
TZ-38 built disappears.

**A4. `_tx_add` is not changed.** It reads `not ok`, and that is correct once `ok` is
correct; a second edit site would create a second definition of «answered» (inv. 20). If
you establish it must change, that is a finding under `## Pre-existing Issues`, not a
licence.

**A5. The three callers are verified, not rewritten.** With `ok` correct, `_rest_rows`,
`fetch_cg` and `reconcile` each receive `ok: False` and should take the exhaustion path
they already have. State, per caller, which path it takes and prove it with the fixture in
C2. Add handling only to a caller that has none, name every line you added, and add
nothing else — a narrow fix that looks incomplete is reported, never widened (contract §6).

**A6. Policy and constants are unchanged.** A parse failure is a failure of the ATTEMPT and
is retried under the existing budget. No new constant, no new field name, no new helper, no
change to the retry bound or to `HTTP_BUDGET_S`.

---

## 4. Scope B — the retry budget prints on every run

**B1.** Move the call site of the existing `ретраи потратили S с из BUDGET` line out of
`if dead:` so it runs once per fetch pass, whatever the outcome.

**B2. This is a call site, never a new counter.** `_http_spent()` already exists and is
already read; wording, source and the budget constant are unchanged (inv. 20). The string
stays verbatim — it is one of the Russian operational lines the Boss reads, and this TZ
does not redesign it.

**B3. It prints when the figure is zero.** «0 с» is the reading that says the layer served
one attempt per URL, and that is precisely the unknown §0 records. A print suppressed on
zero reproduces the defect in a quieter form.

**B4. The funding path carries the identical shape.** Apply the same change to
`fetch_funding`. **The map's mode list in §3.10 carries no `--fetch-funding`**: bind the
FUNCTION, and name in the report the mode that reaches it. If a mode exists that §3.10 does
not list, say so — the map is the Architect's to repair, not yours.

**B5.** The printed seconds are a measured quantity, not a check (inv. 43). No check-count
total moves because of this scope.

---

## 5. Scope C — section H gains the fixture that can fail

**C1. The stub must be able to fail.** §10: the guard stub's `json()` returns a stored
payload and never raises, so the fixture that would fail does not exist — a control that
stubs the parse step so that it cannot fail is not a control over this rule (inv. 22,
inv. 70). Give the stub a response whose `json()` raises and one whose body is truncated.
**Existing H fixtures keep their expectations byte-identical**; report H's check count
before and after.

**C2. Fixtures.** Each calls a production function by name and compares its return, and
every fixture is synthetic input to that function — the garrison's standing rule (map
§3.10). Every assertion is counted at the comparison site (inv. 43).

| Id | Input | Must read |
|---|---|---|
| H-p1 | status carrying a payload, body unparseable | not answered · `json` None · `why` names the parse failure · `_tx_add` folds `exhausted` · `won_clean` false |
| H-p2 | status carrying a payload, body parses | unchanged from today |
| H-p3 | `404`, body not JSON | answered · status preserved · ABSENT · not retried · not exhausted · the census behaviour H already asserts for an absent month unchanged |
| H-p4 | no response at all | unchanged exhausted behaviour |
| H-p5 | parse failure on attempt 1, success on attempt 2 | answered, and **no field of the returned record carries a value from the failed attempt** |
| H-c1 | `_rest_rows` driven with H-p1's stub | takes its exhaustion path, does not raise, returns a populated transport record naming the coin |
| H-c2 | `fetch_cg` driven with H-p1's stub | takes its exhaustion path, does not raise |
| H-c3 | `reconcile` driven with H-p1's stub | its own `ok` check refuses, nothing is dereferenced, no traceback |

**C3. Section letter.** This TZ EXTENDS H; the subject is H's own. If you establish that a
new section is needed, its letter is read FROM THE FILE and never by counting — two
sections already share `E` (§10) — and the report names the letter and why.

**C4. Negative control — which must FLIP and which must NOT** (inv. 68). Restore the old
ordering in the working tree, run gate step 14 and record the result per fixture:

- **must turn RED:** H-p1, H-p5, H-c1, H-c2, H-c3.
- **must stay GREEN:** H-p2, H-p3, H-p4.

Then revert, confirm the tree is clean and step 14 green. A control that cannot tell the
defect from the repair is not a control (inv. 22); a control that turns red on everything
is not one either.

---

## 6. Hard floor clauses this TZ touches — quoted from contract v20

> 2. **Never edit a bench to make it pass.** A red bench is either a product defect or
> a stale expectation; both are findings, neither is a licence to change the
> assertion.

> 8. **Never modify `.github/workflows/backtest_bench.yml`** unless the TZ names it.

> 12. **Never remove, skip, comment out or `continue-on-error` a bench step to make CI
> green** — editing the assertion (item 2) and deleting the assertion are the same
> act; a step that cannot pass is a finding for the report.

C4 deliberately turns fixtures red and reverts; that is a negative test under contract §9,
not an edit to make a bench pass. Nothing else in this TZ removes or weakens an assertion.

---

## 7. What this TZ does NOT do

- No production file moves. `index.html`, `main.py`, `catalysts.json` and
  `bench/exhaustion-calibration.txt` appear in no diff.
- No change to the retry bound, the budget constant, the census arithmetic, `_save`, or the
  venue-observation logic TZ-34 added.
- No new mode, no new file, no new dependency.
- No fetch in this session (hard floor item 9, inv. 44). Every fixture is synthetic and the
  guard step opens no socket.

---

## 8. Validation

Run every item; an item that cannot be run **fails** and is never «not applicable»
(contract §9). Baseline first: record each figure before the change.

1. `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` — exit 0.
2. `python3 bench/backtest_guard_bench.py` — exit 0, `FAIL 0`. State section H's check count
   before and after, step 14's total before and after, and the new gate total against
   **1 335 964**, term by term (inv. 43).
3. `python3 bench/verify_bench.py` — exit 0, **40** checks, `FAIL 0`. This is the regression
   check on the import at scope.
4. The negative control of C4, with the flip list result per fixture, the revert, and a
   clean tree confirmed by `git status --porcelain`.
5. **No socket:** state how the stub's own record was read to establish that the guard step
   contacted no host, and name the limit of that method — a reach to the network through
   something other than `requests` is invisible to it (map §3.10).
6. `git diff --name-only` names exactly `bench/backtest_bench.py` and
   `bench/backtest_guard_bench.py`. Restate the four `## 0` hashes measured after the change.
7. Extremes, each as a fixture with its own assertion: zero-length body on a status carrying
   a payload · a body that is valid JSON but not the shape the caller expects — **this is
   data, not a transport failure**, and the caller's own validation owns it · a first attempt
   that fails to parse and a second that returns a different payload, where the returned
   record is the second attempt's, whole · a `404` whose body happens to be valid JSON.
8. State the mode that reaches `fetch_funding`, and whether it is present in the map's
   §3.10 mode list.

---

## 9. Report requirements

Beyond the §10 template: the record's field list and `_http`'s exit paths (A2) · the path
each of the three callers takes with `ok: False` (A5) · the section letter (C3) · the flip
list result (C4) · the mode reaching `fetch_funding` (B4) · `## Fingerprints`, mandatory.

## Commit Message

```
TZ-39: decide the transport outcome after the last failing step; print the retry budget on every fetch
```
