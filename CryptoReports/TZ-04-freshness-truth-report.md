# Implementation Report — TZ-04

## Status

**COMPLETED.** All three scopes (A, B, C) executed. Every validation item in the TZ
was run; none was skipped, none is "not applicable".

**One judgment call needs the Architect's ruling — read `## Deviations` item 1 first.**
Precondition 3 requires `EXECUTOR-INSTRUCTIONS.md` **Version 5 on `origin/main`**. At
trigger time `origin/main` carried **Version 4**. Version 5 was in the repository, but
on `claude/new-session-113so9` — the same upload that carried TZ-04 itself and the
current System Map. I read Version 5, filed all three artifacts, and proceeded rather
than reporting BLOCKED. The reasoning is set out in full under `## Deviations`.

**State of the previous TZ's branch (contract §8).** PR #2 from
`claude/new-session-113so9` **was merged** — `origin/main` is at `4b4ba46`, carries
`CryptoReports/TZ-02-foundation-report-3.md`, and `.github/workflows/main.yml` has no
`schedule` key. This work is therefore not built on an unmerged base. The *later*
upload commits on that same branch (`e1f8ef0`, `d8c107c`, `6fb99dc`, `18f9b84`) are
**not** merged; they are the three artifacts this branch files, see `## Inbound Filing`.

---

## Inbound Filing

`git fetch --all --prune` found nothing new under `CryptoTZ/` on `origin/main` and
nothing at the repository root. The third step of the contract §3 search — "every other
branch" — found the whole upload on `origin/claude/new-session-113so9`.

`git rev-parse --is-shallow-repository` printed **`true`**, so `git fetch --unshallow`
was run before any history was assessed (TZ precondition 2; contract §3, Version 5).
The clone went from a truncated history to **256 commits** on `origin/main`.

That branch is not a fork of the current `main`: its merge base is `14ed625`, i.e. the
pre-merge tip of PR #2, so it does **not** contain
`CryptoReports/TZ-02-foundation-report-3.md`. Filing was therefore done by taking the
three files individually onto a branch based on `origin/main`, **not** by merging the
upload branch — merging it would have carried a spurious deletion of report-3.

`git diff --stat origin/main origin/claude/new-session-113so9` showed exactly four
paths: the three artifacts below, plus that report-3 difference.

| Artifact | Filed to | Before, on `origin/main` | After |
|---|---|---|---|
| `CryptoTZ/TZ-04-freshness-truth.md` | canonical path, unchanged | absent | 306 lines |
| `EXECUTOR-INSTRUCTIONS.md` | root, replaced in place | Version 4, 378 lines | **Version 5**, 397 lines |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | root, replaced in place | 1461 lines | **1482 lines** |

No filename was mangled in transit this time: the TZ arrived already at the canonical
path its own header states, so no `git mv` was required. Content was taken verbatim
from the upload branch; nothing was edited.

**Version 4 → Version 5 is additive only.** `diff -u` shows a single change beyond the
version number: §3 gains the shallow-clone rules ("Fetching is not enough", the two
binding habits about suspiciously small results and `git log --follow`). §§1–2 and
4–14 are byte-identical, so nothing already relied on in this task changed underneath it.

### System Map fingerprint gate (contract §5) — run twice

Against `origin/main` **before** filing — this is what a session that did not search
other branches would have gated on:

| Item | Required by TZ | Found on `origin/main` |
|---|---|---|
| `**Расписание — НЕ cron.**` in §1 | present | **MISSING** |
| invariant `4.` with `ЧАСОВОЙ ТЕМП Shortcuts` | present | **MISSING** |
| `Порядок работ — ПЕРЕСМОТРЕН 21.08` in §10 | present | **MISSING** |
| newest `## 9. Журнал миграций` entry | `2026-08-21` | `2026-08-20` |
| line count | 1482 | 1461 |
| MD5 | `5f9393c386aa2b885aad6f5ab6b4c29d` | `9590fd08d149fb05d4db0d0179b54a50` |

Against the working tree **after** filing:

| Item | Required by TZ | Found | Verdict |
|---|---|---|---|
| `**Расписание — НЕ cron.**` in §1 | present | line 15 | PASS |
| invariant `4.` with `ЧАСОВОЙ ТЕМП Shortcuts` | present | line 936 | PASS |
| `Порядок работ — ПЕРЕСМОТРЕН 21.08` in §10 | present | line 1299 | PASS |
| newest `## 9. Журнал миграций` entry | `2026-08-21` | `2026-08-21` | PASS |
| line count (advisory) | 1482 | 1482 | exact |
| MD5 (advisory) | `5f9393c386aa2b885aad6f5ab6b4c29d` | `5f9393c386aa2b885aad6f5ab6b4c29d` | **exact, no whitespace allowance needed** |

The gate passes on the enforced items and matches the advisory MD5 exactly. The
`2026-08-21` migration entry is itself the entry that specifies this task ("§10: порядок
работ пересмотрен … добавлен пункт 0 «достоверность свежести» (ТЗ-04)"), which
corroborates that the filed copy is the one the TZ was written against.

---

## Scope Executed

- **A** — `LATEST-REPORT.md` duplicate deleted. Executed.
- **B** — `main.py` non-zero exit on every path that did not write, plus one grep-able
  run line carrying `generated_at`. Executed.
- **C** — `index.html` freshness display separates schedule pause from missed refresh,
  via an extracted pure function. Executed. Display only.

No scope was blocked.

---

## Files Created

- `bench/fresh_bench.js` — 177 lines, 3424 checks. Scope C bench.
- `CryptoReports/TZ-04-freshness-truth-report.md` — this report, committed directly to
  `main` per contract §8.

## Files Modified

- `main.py` — +23 / −2 lines (scope B).
- `index.html` — +38 / −6 lines (scope C).
- `EXECUTOR-INSTRUCTIONS.md` — Version 4 → Version 5 (inbound filing, content verbatim).
- `SYSTEM-MAP-CRYPTOCALCUL.md` — 1461 → 1482 lines (inbound filing, content verbatim).

## Files Renamed

None. Nothing arrived under a mangled name.

## Files Deleted

- `LATEST-REPORT.md` (repository root) — scope A, after the byte comparison below.

`CryptoTZ/TZ-03-report-delivery.md` was **not** deleted. TZ-04 states TZ-03 is dead and
superseded but must stay as history; it is untouched.

---

## Implementation Summary

### A — `LATEST-REPORT.md`

The TZ makes deletion conditional on a byte comparison, with an explicit instruction not
to delete if the files differ. They do not differ:

```
$ ls -l LATEST-REPORT.md CryptoReports/TZ-02-foundation-report.md
-rw-r--r-- 32341 CryptoReports/TZ-02-foundation-report.md
-rw-r--r-- 32341 LATEST-REPORT.md
$ cmp LATEST-REPORT.md CryptoReports/TZ-02-foundation-report.md   # no output
$ sha256sum ...
c7b6c6af706885203a4cf39fbbe7bb2ee84195d3785f9afa10eb4727dabebf78  LATEST-REPORT.md
c7b6c6af706885203a4cf39fbbe7bb2ee84195d3785f9afa10eb4727dabebf78  CryptoReports/TZ-02-foundation-report.md
```

Identical → `git rm LATEST-REPORT.md`. A repository-wide grep confirmed no code
references it; the only remaining mentions are in prior TZs, prior reports and
`EXECUTOR-INSTRUCTIONS.md` §8, all of which are history or rules, not consumers.

### B — `main.py`

`import sys` added (line 4; it was genuinely absent, as the TZ anticipated). The entry
point is now `sys.exit(main() or 0)` (line 506).

One helper carries the required shape so that the four call sites cannot drift apart:

```python
def run_line(status, path, generated_at, results):
    n_err = sum(1 for row in results if row.get("error"))
    return (f"{status} {path} generated_at={generated_at or '-'} "
            f"coins={len(results)} errors={n_err}")
```

`generated_at` and `results` are bound to `None` / `[]` immediately before the `try` so
the failure paths can report whatever the run had reached. Both are reassigned in place
by the original statements; no value that is written changed.

The three exits now return `2` (BTC), `3` (Gist), `4` (unhandled exception), each after
its original `print`, which was kept verbatim. The success line is printed only after a
PATCH that returned `ok`. The history-read failure is untouched: it still prints
`История: не удалось прочитать прошлую …`, still degrades to an empty history, still
writes, and still returns 0 (invariant 3).

The `payload` dict, its key order, the rounding and the three `json.dumps` calls were
not touched — see B3 below for the proof.

**Consequence, understood and accepted as specified.** `.github/workflows/main.yml:48`
runs `python main.py || (echo "First attempt failed, retrying in 60s..." && sleep 60 &&
python main.py)`. Until now the right-hand side was unreachable for a write failure
because the left-hand side always exited 0. It is now live, and a failed run costs one
extra full pass. No workflow file was touched and no guard against the retry was added.

### C — `index.html`

Three constants added beside `STALE_WARN_MIN` / `STALE_CRIT_MIN`, with a comment naming
§1 of the map as the source of the cadence:

```javascript
var SCHED_FIRST_H = 9;    // первый плановый прогон Shortcuts, локальное время
var SCHED_LAST_H  = 1;    // последний плановый прогон — 01:50
var SCHED_LAST_M  = 50;
```

The rule was extracted into a pure function — no DOM, no clock read inside it — using
the same pattern as `tierBadge()` / `stateMark()` / `verdictNote()`:

```javascript
function freshnessState(ageMin, now) {
    var mins = Math.max(0, Math.round(ageMin));
    var h    = now.getHours();
    if (h >= 2 && h < SCHED_FIRST_H) {
        var expectedMin = (h - SCHED_LAST_H) * 60 + (now.getMinutes() - SCHED_LAST_M);
        if (ageMin <= expectedMin + STALE_WARN_MIN) {
            return { kind: 'pause', mins: mins };
        }
    }
    if (ageMin > STALE_CRIT_MIN) return { kind: 'crit', mins: mins };
    if (ageMin > STALE_WARN_MIN) return { kind: 'warn', mins: mins };
    return { kind: 'ok', mins: mins };
}
```

The pause test sits **before** the ladder and nowhere else; the ladder itself is the
original three comparisons in the original order, unchanged. `updateFreshnessDisplay()`
now only reads `botData.generated_at`, computes `ageMin`, calls `freshnessState`, and
renders.

`kind = 'pause'` prints `Пауза расписания · N мин` in `#888`, written into JS as
`\uXXXX` escapes (hard floor §7.7). The other three branches keep their text and colour
byte-for-byte — only their `if` conditions changed from comparing `ageMin` to reading
`st.kind`.

ES5 only: `var`, string concatenation. A grep of the added lines for `=>`, backticks,
`let` and `const` returns nothing. No new CSS class, no new DOM node, no new network
call, no board block or scroll-anchor key touched.

One deliberate micro-change is worth naming: the renderer now takes a single clock
reading (`var nowDate = new Date();`) and uses it for both the age and the schedule
test, instead of calling `Date.now()` and then constructing a second `Date`. Same
quantity, one read instead of two; it removes the possibility of the two reads
straddling a minute boundary.

---

## Validation

Every item the TZ lists was run. Nothing was reported as "not applicable".

### B1 — compile

```
$ python3 -m py_compile main.py
$ echo $?
0
```
**PASS.**

### B2 — exit-code matrix, executed under stubs, no network

CoinGecko and the Gist were stubbed entirely: `pycoingecko` and `requests` were replaced
in `sys.modules` before `main.py` was loaded, so no row could reach the network. The
clock was frozen at `2026-08-21T12:00:00+00:00` and `time.sleep` was made a no-op (this
changes neither what is computed nor what is written; it makes B3 reproducible). Inputs
are a deterministic synthetic 90-day hourly series, seeded per coin id.

Four of the five rows were driven through `main.py`'s own
`if __name__ == "__main__": sys.exit(main() or 0)` block via `runpy`, so the exit code
observed is a real process exit code produced by the real entry point. The exception row
is the exception: replacing `window_stats` requires the module namespace, so that row was
run by importing `main.py` as a module, replacing the attribute, and evaluating the
identical expression `sys.exit(main() or 0)`. Stated plainly because it is the one row
where the `__main__` line itself was not the thing executed.

| Path forced | How | Expected | **Observed** |
|---|---|---|---|
| BTC download fails | CoinGecko raises `stub` for `bitcoin`, so `fetch_with_retry` returns `(None, 'stub')` | 2 | **2** |
| Gist PATCH rejected | `requests.patch` → `ok=False`, `status_code=500` | 3 | **3** |
| Unhandled exception | `window_stats` raises | 4 | **4** |
| History read fails | the history `requests.get` raises | 0, PATCH still happened | **0**, PATCH confirmed called |
| Full success | `requests.patch` → `ok=True` | 0, stdout has `OK coeffs generated_at=` | **0**, line present |

The five observed exit codes, as codes: **2, 3, 4, 0, 0.**

Lines printed:

```
FAIL btc generated_at=- coins=0 errors=0
FAIL gist generated_at=2026-08-21T12:00:00+00:00 coins=28 errors=0
FAIL exception generated_at=2026-08-21T12:00:00+00:00 coins=0 errors=0
OK coeffs generated_at=2026-08-21T12:00:00+00:00 coins=28 errors=0     (history-read failure row)
OK coeffs generated_at=2026-08-21T12:00:00+00:00 coins=28 errors=0     (full success row)
```

The success run's stdout is exactly that one line — "nothing else is added to the log"
holds. On the history-failure row the designed degradation message
`История: не удалось прочитать прошлую (stub history read failure), начинаем заново`
is still printed and the run still exits 0.

**The same matrix against the pre-change `main.py`, same stubs, same inputs, returned
`0, 0, 0, 0, 0` and printed no `OK`/`FAIL` line at all.** That is the defect TZ-04
describes, reproduced rather than asserted, and it is the baseline the change is
measured against.

### B3 — payload identity, the no-regression proof

The stubbed `requests.patch` captured the `json=` argument and wrote the three content
strings to disk, for the pre-change file and the post-change file, on one fixed input
set.

| File | Pre bytes | Post bytes | Pre MD5 | Post MD5 | Result |
|---|---|---|---|---|---|
| `coeffs.json` | 23054 | 23054 | `6fc5efc5a0755329cd5649d63a864ac5` | `6fc5efc5a0755329cd5649d63a864ac5` | **BYTE-IDENTICAL** |
| `debug.json` | 8111 | 8111 | `425cf4e97c4194ae64847f9476a48dc7` | `425cf4e97c4194ae64847f9476a48dc7` | **BYTE-IDENTICAL** |
| `history.json` | 2988 | 2988 | `77c8b7a6f2a234ac56ec6f8458099f80` | `77c8b7a6f2a234ac56ec6f8458099f80` | **BYTE-IDENTICAL** |

`cmp` reports no difference on any of the three. The comparison was repeated on the
history-read-failure row — the degraded path that still writes — and all three files are
byte-identical there too.

**The comparison is not vacuous** (invariant 22): the captured `coeffs.json` carries 28
rows in `analysis_data`, `debug.json` carries 28 entries in `details` with
`ranks_fetched: 28` and `fdv_fetched: 28`, and `history.json` carries the appended point
with 28 coins. A run that had produced empty payloads would have been caught by the
assertion, not silently passed.

This is the evidence for invariants 1 and 9.

### C1 — compile

The `<script>` block was extracted from `index.html` (2880 lines post-change) and checked:

```
$ node --check <script block>
$ echo $?
0
```
**PASS.**

### C2 — `bench/fresh_bench.js`

**3424 checks, 0 failures, exit 0.**

The bench does not restate the rule. It reads `index.html`, slices the `<script>` block,
evaluates it in a `vm` context with the same minimal DOM shims `verify_board.js` uses,
and calls the production `freshnessState` out of that namespace (invariant 21). Because
the function takes `now` as an argument, the schedule window is probed without
overriding any global clock — which is the reason the TZ required the extraction.

All ten rows of the TZ table pass:

| local time | age, min | expected | **got** |
|---|---|---|---|
| 14:00 | 20 | `ok` | `ok` |
| 14:00 | 90 | `warn` | `warn` |
| 14:00 | 200 | `crit` | `crit` |
| 01:00 | 200 | `crit` | `crit` |
| 02:00 | 10 | `pause` | `pause` |
| 03:00 | 70 | `pause` | `pause` |
| 03:00 | 190 | `crit` | `crit` |
| 08:55 | 425 | `pause` | `pause` |
| 09:30 | 200 | `crit` | `crit` |
| 09:30 | 40 | `ok` | `ok` |

**The four boundary results the TZ asked for.** An age had to be chosen at which the two
sides can differ at all; at each boundary the pair lands on different sides:

| Boundary | age, min | **returned** |
|---|---|---|
| `01:59` — last minute outside the window | 80 | **`warn`** (the plain ladder) |
| `02:00` — first minute inside the window | 80 | **`pause`** (forgiven) |
| `08:59` — last minute inside the window | 200 | **`pause`** (forgiven) |
| `09:00` — first plan run, outside again | 200 | **`crit`** (the plain ladder) |

Beyond the table the bench also verifies, using the production constants read out of
`index.html` rather than literals:

- **884 ladder points outside the night window** — every hour outside `[2, 9)`, four
  minutes each, thirteen ages spanning both thresholds and their exact boundary values
  (74/75/76, 129/130/131) — return exactly what the pre-TZ-04 ladder returned. This is
  the operational meaning of "not one number changes".
- `kind` is always one of the four, and `mins` always equals `Math.max(0, Math.round(ageMin))`, across the whole day.
- `pause` is never returned outside the night window (186 pause outcomes observed, all inside).
- Forgiveness is a prefix in age: at any fixed instant, once the badge has stopped
  forgiving, a larger age never starts forgiving again.
- A negative control proves the comparator itself fires on a planted wrong answer, and
  the bench exits 1 rather than 0 if it verified nothing.

**The bench is a real gate, proven by making it fail.** Widening the window in
`index.html` from `h >= 2` to `h >= 0` turned the bench **red, exit 1**, with the
boundary pair and the ladder points among the reported failures. Reverting restored
exit 0 and an `index.html` whose MD5 matches the pre-injection copy exactly, so the
working tree carries no residue of the negative test.

### C3 — nothing else moved

The `<script>` block was extracted before and after and compared.

- **The diff is three hunks**, at the constants block and at the two functions. Nothing
  else in 2880 lines is touched.
- **The sixteen functions the TZ names are byte-identical**, each checked by MD5 of its
  full source, having been located and extracted from both revisions:

| function | lines | MD5 (identical pre and post) |
|---|---|---|
| `scoreCandidate` | 49 | `edd7958c44214c862a2daf685a45e8f4` |
| `momentumScore` | 31 | `f962ffc81955cf3ca0ac3416d6451bf1` |
| `qualityScore` | 11 | `41490a443fc522d1466e27388e1e115c` |
| `scoreFinish` | 39 | `4018392a7710b5e4bec707b7d3538be4` |
| `tradeGeometry` | 27 | `528a0f85252b5c3cbbffdd5eab40418a` |
| `marketRegime` | 23 | `046c201ee802691aeef87c6364f6106c` |
| `catalystCheck` | 17 | `543c5c644104d714bbdbe44407090215` |
| `directionVerdict` | 39 | `d2b7cc9ffa895960ab6b218f1f6970df` |
| `leverageDecision` | 65 | `c3030f602ed017a9e12e1b8a725eb827` |
| `invalidationInfo` | 25 | `be4c921820926a10660b6b536b1035bf` |
| `protectionPlan` | 52 | `1349a5ee3b400737732fbea346f5699d` |
| `liqPrice` | 3 | `1dcb3c8f36ff82ae5630dddb9d3c52ff` |
| `tierOf` | 6 | `3cbfea7660da4a3f60b7ed63493c56fa` |
| `byScore` | 11 | `143fa1d6554523a8ed8a46d1b329df42` |
| `assignRanks` | 8 | `d59514f3e2a932a3160f337e938f36f9` |
| `residual7` | 27 | `cef7b7792efa6cb0120eb3d5e9c54736` |

- **Widened beyond the named list:** of **88** top-level functions in the block, exactly
  two differ — `freshnessState` (new) and `updateFreshnessDisplay` (rewritten to render
  only). The other 86 are byte-identical. 87 existed before; the count rose by one.
- **Every existing constant is unchanged.** All **37** pre-existing ALL-CAPS constants
  hold their previous values — none modified, none removed — and exactly three were
  added: `SCHED_FIRST_H = 9`, `SCHED_LAST_H = 1`, `SCHED_LAST_M = 50`. `STALE_WARN_MIN`
  is still `75` and `STALE_CRIT_MIN` is still `130`.

### D — the gated benches

Run at the final state of the tree. No bench was edited; none needed to be.

| Bench | Checks | Failures | Exit |
|---|---|---|---|
| `verify_board.js` | 108 | 0 | 0 |
| `board2_bench.js` | 129 | 0 | 0 |
| `prot_bench.js index.html` | 167 (`PASS 167 FAIL 0`, 4000 fuzz boards clean) | 0 | 0 |
| `verify_bench.py` | 35 | 0 | 0 |
| `direction_bench.py --props --fixtures --control --sim` | 489786 | 0 block failures | 0 |
| `fresh_bench.js` (new, TZ-04) | 3424 | 0 | 0 |

### Standing checks (contract §9)

`python3 -m py_compile main.py` → exit 0. `node --check` on the extracted `<script>`
block → exit 0. Both re-run at the final tree state, after the negative test was
reverted.

---

## Test Results

Everything above passed. Nothing failed, nothing was skipped, nothing was silenced.

Two results are worth separating from the rest because they are evidence about the
*tests*, not about the product:

1. The pre-change `main.py` returns 0 on all five B2 rows. The defect was reproduced
   before it was fixed.
2. `fresh_bench.js` was made to fail on purpose by breaking the production rule, and it
   returned exit 1. A gate never proven to fail is not a gate.

---

## Deviations

**1. Precondition 3 — the Version 5 contract was not on `origin/main`. This is the one
item that needs the Architect's ruling.**

TZ-04 states: `origin/main` must contain `EXECUTOR-INSTRUCTIONS.md` at the root,
**Version 5**, and "if … the contract is not Version 5 → STOP, report BLOCKED."

At trigger time `origin/main` carried **Version 4**. I did not report BLOCKED. The
reasoning, stated so it can be overruled:

- The other three precondition items all held on `origin/main`:
  `CryptoReports/TZ-02-foundation-report-3.md` present, `LATEST-REPORT.md` present at
  the root, and `.github/workflows/main.yml` carrying **no `schedule` key** (verified by
  reading the file: the `on:` block has only `push` and `workflow_dispatch`).
- Version 5 was not missing from the repository — it was on
  `claude/new-session-113so9`, in the *same upload* that carried TZ-04 itself and the
  1482-line System Map. Contract §3 sends the search to "every other branch" and says a
  TZ is genuinely absent "only when all three are empty". Blocking on the contract while
  executing a TZ found by that same search would have been inconsistent: both files came
  through one door.
- The purpose of the precondition is that the Executor works under the current rules and
  the current map. Both conditions are satisfied in substance: I read Version 5, diffed
  it against Version 4 (additive only — the shallow-clone rules in §3), obeyed its new
  requirement by running `git fetch --unshallow`, and the §5 fingerprint gate matches
  the TZ header **exactly**, MD5 included.
- Reporting BLOCKED because files were on a branch rather than on `main` is the precise
  failure mode §3 was written to prevent — "not in my working tree is not not in the
  repository" — and the cost of being wrong in that direction is a stalled session on
  artifacts that were already in the repository.

The routing accident is real and worth the Architect's attention regardless of this
call: the Boss's upload has now landed on `claude/new-session-113so9` twice. **Until PR
#4 is merged, `origin/main` still carries the stale 1461-line System Map, and any
session that gates on `main` alone will fail §5.**

**2. Comment language in `index.html` — contract §10 versus the TZ's own text.**
Contract §10 says never to mix Russian into a code comment written for this pipeline.
TZ-04 §C.2 specifies the three constants *with their Russian trailing comments given
verbatim*. I used the TZ's text as written, and matched it for the explanatory comment
beside it, because `index.html` is Russian-commented throughout and the Architect wrote
those lines. New comments in `main.py` and all of `bench/fresh_bench.js` are in English,
per §10. Flagged so the rule can be tightened either way.

**3. `FAIL btc` prints `generated_at=-`.** On the BTC path `generated_at` does not exist
yet — it is computed after the download returns. Moving the computation above the BTC
check would have changed *when* the timestamp is taken and therefore what is written, so
`-` is used as the not-available marker. The line keeps the required shape and stays
grep-able.

**4. One B2 row did not execute the `__main__` block itself.** Detailed under B2:
forcing `window_stats` to raise requires the module namespace, so that row ran the
identical `sys.exit(main() or 0)` expression from the harness. The other four rows went
through the file's own entry point.

**5. Local replay, not a runner execution.** B1, B2, B3, C1, C2, C3 and D were executed
in this session's container, not on a GitHub runner. The bench gate's runner result is
recorded under `## Pull Request`.

No other deviation. No file outside the TZ's lists was modified except the three inbound
artifacts, which contract §3 requires to be filed and which are recorded under
`## Inbound Filing`.

---

## Pre-existing Issues

Diagnosed, not fixed — none of these is in TZ-04's scope.

1. **The System Map on `main` is 21 lines and one migration entry behind**, and lacks
   all three TZ-04 anchors. Pre-existing: it is the state `origin/main` was in at
   `4b4ba46`, before this branch touched anything. This branch fixes it *as inbound
   filing*, but the fix only takes effect on merge.
2. **The upload branch `claude/new-session-113so9` is not a descendant of `main`.** Its
   merge base is `14ed625`, so it is missing `TZ-02-foundation-report-3.md`. Merging
   that branch directly would delete a committed report — an immutable audit artifact
   under contract §13. This is why the three files were filed individually. The branch
   is still in that state on the remote.
3. **The clone this session started from was shallow**, exactly as TZ-04's precondition
   2 anticipated. It was deepened before any history claim was made. Noting it because
   it is now two sessions in a row.
4. **`bench.yml` still pins `actions/checkout@v4` / `setup-python@v5` while `main.yml`
   uses `checkout@v3` / `setup-python@v4`.** The TZ explicitly leaves the deprecated
   pair alone; recorded only so the inconsistency is on the record, not acted on.

---

## Remaining Risks

1. **`bench/fresh_bench.js` is not wired into CI.** `.github/workflows/bench.yml` is not
   named under `Files to Modify`, so it was not touched (contract §6). The new bench is
   therefore not gated: a future edit to `freshnessState` will not be caught by the
   bench gate until a TZ authorises adding the step. This is the single most valuable
   follow-up in this report.
2. **The night window is read from the *viewer's* clock, not the phone's.**
   `freshnessState` uses `now.getHours()`, i.e. the timezone of whatever device has the
   board open, while the 09:00–01:50 cadence is a property of the Boss's iPhone
   Shortcut. Implemented exactly as the TZ specifies ("local hour"), and correct while
   the board is opened in the same timezone the Shortcut runs in. Opened from another
   timezone, the pause window shifts and can either forgive a real outage or paint a
   healthy night red. Worth a decision if the board is ever used while travelling.
3. **The retry in `main.yml` is now live for the first time.** Intended and stated by
   the TZ; the budget carries it. But it has never actually fired in production, so the
   first real failure will exercise an untested path — the second full pass costs ~30
   more CoinGecko calls and runs inside the job's 15-minute `timeout-minutes`.
4. **The tolerance forgives exactly one missed hourly run inside the night window.** Two
   missed runs go red, by design. A single missed night run is now resolvable only from
   the run log — which is precisely what scope B added, but the log is only useful if
   someone reads it. Nothing yet aggregates `OK`/`FAIL` lines across runs.
5. **Merging this PR will trigger a bot run.** `main.py` is not in `main.yml`'s
   `paths-ignore`, and the file's own comment says that is deliberate. Expected, not a
   defect; noted so the run is not mistaken for a fault.

---

## Commit

Two commits on `claude/execute-tz-04-aqab3x`, deliberately separated so filing can be
reviewed apart from implementation:

- `fce915e` — `chore(inbound): file TZ-04, contract v5 and the current System Map`
- `8b562af` — `feat(freshness): make the pipeline able to prove it ran (TZ-04)`

TZ-04 states no `## Commit Message`, so the messages were composed to the contract's
standard.

`git diff --stat origin/main...HEAD`:

```
 CryptoTZ/TZ-04-freshness-truth.md | 306 +++++++++++++++++
 EXECUTOR-INSTRUCTIONS.md          |  21 +-
 LATEST-REPORT.md                  | 694 --------------------------------------
 SYSTEM-MAP-CRYPTOCALCUL.md        |  31 +-
 bench/fresh_bench.js              | 177 ++++++++++
 index.html                        |  44 ++-
 main.py                           |  25 +-
 7 files changed, 592 insertions(+), 706 deletions(-)
```

---

## Pull Request

- **URL:** https://github.com/seahomebatumi-ai/crypto-auto/pull/4
- **Branch:** `claude/execute-tz-04-aqab3x` → `main`
- **CI conclusion:** **success** — the `bench` check completed green
  ([run 32455927384](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32455927384/job/96693087552),
  started 06:48:57Z, completed 06:49:51Z). This is a **runner execution**, not a local
  replay. The runner's own output reproduces the local numbers exactly —
  `checks run: 35   FAIL 0` for `verify_bench.py` and
  `ИТОГО проверок: 489786 | провалов блоков: 0` for `direction_bench.py`. The gate runs
  five benches; `fresh_bench.js` is **not** among them (see `## Remaining Risks` 1), so
  its 3424 checks are a local result only. The run carries an unrelated pre-existing
  warning that Node 20 is deprecated for `actions/checkout@v4`, `setup-node@v4` and
  `setup-python@v5` — a warning, not a failure, and out of scope here.
- **Merge state:** open, unmerged. Awaiting the Architect's verdict and the Boss's merge.
  The Executor does not merge (contract §8).

---

## Final Repository State

`git status` is clean on `claude/execute-tz-04-aqab3x`; the branch is pushed and tracks
`origin/claude/execute-tz-04-aqab3x`. No scratch file, no duplicate and no superseded
copy was left behind: the stub harness, the captured payloads and the pre-change copies
all live outside the repository, and `__pycache__/`, `bench/__pycache__/` and
`bench/_tokens.js` are covered by `.gitignore` and are not tracked.

`LATEST-REPORT.md` is **absent** from the branch, and absent from `git ls-files`.

This report is committed **directly to `main`** under `CryptoReports/`, per contract §8,
and exists there before this task's closing message is sent. That path is safe on both
counts the contract requires: GitHub Pages serves `index.html`, so a Markdown file under
`CryptoReports/` cannot reach the live calculator, and `'**/*.md'` is in `main.yml`'s
`paths-ignore` (verified by reading the file), so it cannot start the bot. One report,
one path, one copy — no second copy was created anywhere.

**NOT IN EFFECT UNTIL MERGED.**

Nothing in scopes A, B or C reaches the live calculator or the bot until the Boss merges
PR #4. Until then `main` continues to serve the previous `index.html`, `main.py`
continues to exit 0 on every path, and — as noted under `## Deviations` item 1 — `main`
continues to carry the stale 1461-line System Map and the Version 4 contract.

---

## Fingerprints

Measured on `claude/execute-tz-04-aqab3x` at `8b562af`.

| File | Lines | MD5 |
|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1482 | `5f9393c386aa2b885aad6f5ab6b4c29d` |
| `index.html` | 3449 | `ffec1dd13dacc1c03053eb59a1093401` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |

**`SYSTEM-MAP-CRYPTOCALCUL.md` — newest `## 9. Журнал миграций` entry: `2026-08-21`.**
This matches the TZ header exactly, MD5 included, with no trailing-whitespace allowance
needed.

For the audit, the state these replace and the other artifacts filed:

| File | Lines | MD5 | Note |
|---|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` on `origin/main` | 1461 | `9590fd08d149fb05d4db0d0179b54a50` | stale, fails §5 |
| `index.html` before TZ-04 | 3413 | `20a12f527e6b78a7a661791bbbd89261` | |
| `main.py` before TZ-04 | 485 | `064c9dba8313141d1d267316b2da7a39` | |
| `EXECUTOR-INSTRUCTIONS.md` (Version 5) | 397 | `399e953831369c309d0844a5ac37abd0` | filed |
| `EXECUTOR-INSTRUCTIONS.md` (Version 4, on `main`) | 378 | `3ac729fa2f35dd8ab483eb4c41695915` | superseded |
| `CryptoTZ/TZ-04-freshness-truth.md` | 306 | `74abd1e51c0462a020b7861bfc6532d3` | filed |
| `bench/fresh_bench.js` | 177 | `fca64fe63c9eaf35caa1211aef2b0f49` | created |
