# Implementation Report — TZ-38

## Status

**COMPLETED.** All sixteen validation items ran. Fifteen passed as specified; item 6's
first census figure passed only after the implementation was reshaped, and item 9 was
RED at first attempt and is documented under `## Deviations` together with the two
collisions between the TZ's own sections that produced it.

The previous TZ's branch **was merged**: `claude/tz-37-lab-identity-partition` landed as
PR #33 (`0c26a56`). This work is not built on an unmerged base.

## Inbound Filing

None. `CryptoTZ/TZ-38-fetch-transport.md` already carried its canonical filename
(contract §3) and arrived on `origin/main` in `21c217a`. No artifact was moved or
renamed.

One filing note, because it cost the first minutes of the session and is the failure
mode a stale worktree produces: **the worktree was three commits behind `origin/main`
and TZ-38 did not exist in it.** `git fetch` brought `21c217a`, which carries the TZ
itself plus 123 changed lines of `SYSTEM-MAP-CRYPTOCALCUL.md` and both benches at the
figures the gate below matches. A gate failure read before fetching would have been
attributed to the wrong thing.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names files outside `CryptoReports/**`,
so the class is read off `## Scope` and not chosen.

Stages A, B, C, D in `bench/backtest_bench.py`; stage E in
`bench/backtest_guard_bench.py`. Nothing else was written.

## Files Created

None.

## Files Modified

| File | Before | After |
|---|---|---|
| `bench/backtest_bench.py` | 4258 lines, `11654488e2e5637c00fc9ae1f1880916` | 4555 lines, `deac9dd8a53f2047c25c2d6fb24f09b4` |
| `bench/backtest_guard_bench.py` | 1425 lines, `b42b660d3ede3196ba6c1c694d8f7fde` | 1726 lines, `ce08dd99edebfa90d8fce3dd6b7ba472` |

`git diff --numstat origin/main` on the implementation branch, quoted verbatim
(item 2):

```
350	57	bench/backtest_bench.py
309	8	bench/backtest_guard_bench.py
```

Two files, exactly the two in scope. No production file, no workflow, no contract, no
map, nothing under `journal/**` or `analyst/**`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### Stage A — `_http`, the one place this file touches the network

Four module-level constants and the two helpers, placed above `probe`:

```
HTTP_TRIES    = 3
HTTP_BACKOFF  = (2.0, 8.0)
HTTP_RETRY_ST = (408, 418, 425, 429, 500, 502, 503, 504)
HTTP_BUDGET_S = 600.0
```

`_http` returns a record — `ok`, `status`, `content`, `json`, `tries`, `slept`, `why` —
and never a `Response`, so no caller can read a status off an object that may not
exist. `ok` means **a reply arrived**: `404` is `ok: True, status: 404`, because the
month is not published and that is data. Retry is on transport and on `HTTP_RETRY_ST`
only; a `404`, `403` or `451` returns with `tries == 1`. The body read is inside the
retried block, which is where run #19 actually died. `_SLEEP` is a module attribute the
garrison rebinds, so section H asserts the ladder without spending it, and the 600 s
budget is global and monotone — once spent, every later call makes one attempt and
sleeps not at all.

`_session()` caches one `requests.Session` **keyed on the `requests` module object**, so
the several fake modules `backtest_guard_bench.py` installs in one process each get
their own session and none records into a dead stub.

### Stage B — the archive readers return a transport record

`_tx()`, `_tx_add()` and `_tx_merge()` build and fold the record.
`_vision_rows` returns `(rows, gone, note, tx)` and `_rest_rows` returns
`(rows, code, tx)`.

The load-bearing line: **`gone` counts answered-and-absent months only.** An exhausted
request never increments it. The leg aborts on the first exhaustion in either loop and
returns with what it has, and the abort is asserted from the stub's URL record rather
than from a row count, because a row count cannot tell «not requested» from «requested
and empty».

`_try_alias` does not splice a truncated old leg. `_splice`'s bar is derived from the
two legs' own hourly extremes, so a leg cut short by a reset would move the bar with it
and the joint would be admitted or refused by an accident of the network. The symbol
enters by its post-rename leg alone and the printed line is worded distinctly from
`ОТКЛОНЕНА`, because a refusal is an arithmetic verdict and this is not one.

### Stage C — the coin's verdict

`_fetch_best` gains one rule: **a leg that suffered exhaustion is not eligible to win.**
It is not compared on length and does not trigger the `>= 2600` early break. A partial
leg can be longer than a complete one, so «keep the longest» would otherwise prefer the
damaged series — the mechanism by which a naive repair truncates silently.

In `fetch_prices` the transport verdict runs **before** the `len(rows) < 2600` skip and
before `_save`, and `continue`s. There is no path from an exhausted coin to `_save`. A
partial series can clear 2 600 hours and a 5 % hole fraction and be written as a healthy
coin; the order is what prevents it. `fetch_funding` carries the same repair and writes
no `_fund_<SYM>.json` for an exhausted coin. Neither `sys.exit` moved: a coin fails, not
the run.

### Stage D — the remaining three sites

`probe` (`tries=1`, since one attempt is the point of a twenty-second diagnosis),
`fetch_cg`, and the live-`coeffs` read. The explicit `429` branches are gone in both
places they existed.

### Stage E — section H in the garrison

The `Archive` stub gained `Session`, an `exceptions` namespace whose
`RequestException` is a module-level class (so its identity survives every `install()`),
fault injection and a status-forcing map. Section B's four `_vision_rows` call sites and
section E's `attempt` stub were updated for the new arities. Section H is 57
comparisons and prints its own count.

## Validation

Every item ran. None is «not applicable».

| # | Item | Result |
|---:|---|---|
| 1 | `py_compile` both files | **PASS** — exit 0 |
| 2 | Diff names exactly the two in-scope files | **PASS** — quoted above |
| 3 | Fingerprint gate | **PASS** — see below and `## Fingerprints` |
| 4 | Baseline guard run, before the first edit | **266 checks, FAIL 0** |
| 5 | Final guard run and the delta | **323, FAIL 0**; 323 − 266 = **57** = section H's own printed count |
| 6 | Stage D census | **PASS** — commands and output below |
| 7 | Superseded vocabulary absent | **PASS** — 0 hits each |
| 8 | Section B call sites updated | **PASS** — the section runs; a stale unpack would raise |
| 9 | `verify_bench.py` unmoved | **40, FAIL 0** — red at first attempt, see `## Deviations` |
| 10 | `--lab-selftest` D1–D9 byte-identical | **PASS** — `md5 500699409883c2d00e89fa64c00d6462`, 17 lines, both sides |
| 11 | `--selftest` block unchanged | **PASS** — `md5 888b31de3f1f77380b23e179bca32c2a`, both sides |
| 12 | H10 shown failing when the caught set is widened | **PASS** — `FAIL 1`, named; restored |
| 13 | Local `bench.yml` replay, fourteen steps | 13 green, step 5 is the local ceiling — see below |
| 14 | Hosted `Bench gate` on the pushed branch | **success**, both runs — see `## CI Execution` |
| 15 | No CI wiring changed | **Confirmed** — see below |
| 16 | No external host fetched in-session | **Confirmed** — see below |

### Item 3 — the fingerprint gate, by line number

The TZ requires the LINE NUMBER at which each anchor matched, not a verdict that it
did. Each anchor matched **twice**: once in the map's own `## 0` anchor table and once
at the section it names. Both are stated, because reporting only the first would report
the table of anchors rather than the anchors.

| Anchor | Content line | Anchor-table line |
|---|---:|---:|
| revision `**Revision 2026-09-09-b.**` | **17** | 174 |
| `### 3.12 Direction engine — veto cascade` | **1113** | 175 |
| `### 3.15 Catalyst registry` | **1490** | 176 |
| `### 3.16 List exhaustion — the day-range measure` | **1587** | 177 |
| `## 11. Analytical engine` | **2485** | 178 |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | **1754** | 179 |
| `70. **A transport failure is NOT an absence of data.**` | **2228** | 180 |

Map: 2705 lines, `9ac61f1dea9e6f349ac5a41e743943af` — both as required. Contract v20:
814 lines, `9a257890e9db663eb0fc74129f4841e0`. The four `## 0` table rows and both
bench figures matched exactly as stated in the TZ; the figures are in `## Fingerprints`.

### Item 6 — the Stage D census

```
$ grep -c "requests\.get(" bench/backtest_bench.py
1
$ grep -c "requests\.Session(" bench/backtest_bench.py
1
$ grep -n "import requests" bench/backtest_bench.py
981:    import requests
1021:    import requests
```

Line 981 is inside `_session`, 1021 inside `_http`: the transport helpers only, and at
most twice as required. The single `requests.get(` is at line 1045 inside `_http` and
the single `requests.Session(` at line 978 inside `_session`. One definition site is the
whole reason this is one helper and not six patches.

### Item 7 — superseded vocabulary is absent

```
$ grep -cE "status_code in \(429, 418\)" bench/backtest_bench.py
0
$ grep -cE "time\.sleep\(30\)" bench/backtest_bench.py
0
$ grep -cE "time\.sleep\(65\)" bench/backtest_bench.py
0
$ grep -n "requests\.get(\|requests\.Session(" bench/backtest_bench.py
978:        _SESSION[1] = requests.Session()
1045:            r = s.get(url, **kw) if s is not None else requests.get(url, **kw)
```

The four surviving `r.status_code` reads are all inside `_http`, which is the one place
entitled to read a status off a `Response`. One hit was self-inflicted and removed: the
new `_rest_rows` docstring originally quoted the deleted branch verbatim, which is a
grep hit under a rule that says a hit blocks delivery. The docstring now describes the
branch in words.

### Item 12 — the negative control, shown failing

With `caught = (Exception,)` substituted for the registered set:

```
H. transport: 57 comparisons
checks run: 323   FAIL 1
  FAIL: H10. NEGATIVE CONTROL: a TypeError PROPAGATES out of `_http`
```

Restored, and green again at 323 / FAIL 0. The control fires on exactly the defect it
exists for, and on nothing else: no other assertion moved.

### Item 13 — local `bench.yml` replay, fourteen steps

| # | Step | Exit | Count |
|---:|---|---:|---|
| 1 | `verify_board.js` | 0 | checks 109, fails 0 |
| 2 | `board2_bench.js` | 0 | checks 130, fails 0 |
| 3 | `prot_bench.js index.html` | 0 | PASS 372, FAIL 0 |
| 4 | `verify_bench.py` | 0 | checks run 40, FAIL 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | **1** | **local ceiling — see below** |
| 6 | `fresh_bench.js` | 0 | checks 3424, fails 0 |
| 7 | `journal_bench.js` | 0 | проверок 774130, провалов 0 |
| 8 | `catalyst_bench.js` | 0 | checks 24692, fails 0 |
| 9 | `display_bench.py` | 0 | 24598 checks, 0 failures |
| 10 | `render_bench.py` | 0 | 123 scenarios, 16171 checks, 0 failures |
| 11 | `direction_bench.py --display` | 0 | проверок 15629, провалов блоков 0 |
| 12 | `exhaustion_bench.js` | 0 | checks 220598, fails 0 |
| 13 | `live-gate.sh --selftest` | 0 | checks=40 |
| 14 | `backtest_guard_bench.py` | 0 | checks run 323, FAIL 0 |

**Step 5 is this machine's ceiling and is stated as such (map §10), not as a product
failure.** It is attributed, not assumed, and four independent facts carry the
attribution:

1. `git diff --stat origin/main -- bench/direction_bench.py index.html` is **empty**.
   The step's inputs are byte-identical to `origin/main`, so its result here is what
   `origin/main` produces here.
2. `direction_bench.py` contains **zero** references to `backtest_bench` and zero to
   `requests`. Nothing in this diff can reach it.
3. The phases pass individually: `--props` 255696 checks / 0 failures, `--fixtures` 4/0,
   `--sim` 6/0. Only `--control` fails, with `node failed`, on a host with 955 MB of RAM
   and 146 MB free.
4. **The same combined invocation is `success` on the runner** — step 10 of the hosted
   gate below.

### Item 15 — the negative-CI-test clause does not fire

No CI wiring changed: `.github/workflows/**` appears in no diff, and hard floor item 8
stands — `backtest_bench.yml` is not named by this TZ and was not touched. Contract §9's
requirement for a negative test of new CI logic therefore has no referent. **The
negative controls for this TZ are section H items 10 and 11** — the `TypeError` that
must propagate, and the world of nothing but healthy URLs that must leave every
transport counter at zero. Stated explicitly, as the TZ requires.

### Item 16 — no external host was fetched

No external data host was contacted at any point. Every stage was verified offline
against a stubbed `requests`; the archive, the mirror, CoinGecko and the live gist were
all synthetic. The only network operations of the session were `git` against the
repository origin and the GitHub API reads reported under `## CI Execution`, neither of
which stands behind a product fact (hard floor item 9, inv. 44).

## Test Results

| Bench | Baseline | Final |
|---|---|---|
| `backtest_guard_bench.py` | 266, FAIL 0 | **323, FAIL 0** |
| `verify_bench.py` | 40, FAIL 0 | **40, FAIL 0** |
| `--lab-selftest` D1–D9 | 17 lines, `md5 500699409883c2d00e89fa64c00d6462` | identical |
| `--selftest` | `md5 888b31de3f1f77380b23e179bca32c2a` | identical |

Section H's own printed line: `H. transport: 57 comparisons`. The delta 323 − 266 = 57
is attributed by the section rather than by arithmetic, exactly as F and G are.

Section H covers, in the TZ's order: the ladder `(2.0, 8.0)` asserted exactly rather
than bounded; exhaustion naming its exception type; `404` answered and not retried;
`503` retried to exhaustion while `403` is not retried at all; an exhausted month not
counted absent **and** the later months provably never requested; an absent month
counted and refilled from its dailies; the exhausted long leg losing to the clean short
one in both leg orders; every leg dead; the budget collapsing `tries` to 1; the
`TypeError` negative control; the all-healthy zero control; and host discipline over
every URL the whole section touched.

## Deviations

**1. `verify_bench.py` was RED at first attempt, and the repair is in the helper rather
than in the bench.** After Stage D, gate step 4 crashed with
`AttributeError: module 'requests' has no attribute 'exceptions'`, then with
`'FakeResp' object has no attribute 'content'`. `verify_bench.py` installs its own
`requests` stub carrying a bare `get`, and `verify_against_live` now routes through
`_http`.

This is a collision inside the TZ. §2 lists `verify_bench.py` under **Touches** and says
it is NOT edited and its count must not move, and item 2 requires the diff to name
exactly two files; §7.1 separately requires the *guard* bench's stub to grow `Session`
and `exceptions`. Editing `verify_bench.py` would have satisfied §7.1's spirit and
broken §2 and item 2 — and hard floor item 2 forbids editing a bench to make it pass in
any case.

Resolved in `_http` and `_session`: both read `Session`, `exceptions` and `content` with
`getattr` and degrade when a stub carries none of them. **The degradation is strictly
narrower, never wider** — with no `RequestException` available the caught set is
`(OSError,)` — so §3.3 rule 3 holds and H10 still proves a `TypeError` propagates. The
guard bench's stub does carry the full interface, so section H exercises the real
session path and inv. 22 is satisfied where it was actually aimed. `verify_bench.py` is
unedited and reads 40, FAIL 0.

**2. §6's census figure `requests.get( == 1` and §3.2's session are in tension, and the
implementation now satisfies both literally.** A helper that always calls
`_session().get(...)` never writes `requests.get(`, so the first shape of Stage A scored
`requests.get( == 0` — the census as written could not pass alongside a session. The
`getattr` degradation of deviation 1 resolved it without contrivance: `_http` calls the
session's `get` when there is one and `requests.get` when the module has no `Session`,
which is one literal occurrence of each, both inside the helper the census names. Had
the two stayed irreconcilable, the session would have won on weight — §3.2, the §3.3
signature and §7.1 all require it, against one line in §6.

**3. §1 and §6 name `verify_against_live` as the live-`coeffs` reader; the reader is
`reconcile`.** In the file as delivered, `GIST_LIVE` is read at line 1401, inside
`reconcile` (line 1370). `verify_against_live` (line 1519) is a thin wrapper whose own
docstring says «вся арифметика — в reconcile()» and whose body calls it. There is
exactly one `GIST_LIVE` read in the file, so the site is unambiguous and it is the one
routed through `_http`; the named function reaches it through `reconcile`. The
`sys.exit` therefore sits in `reconcile`, which is where the read is, and propagates
through the wrapper unchanged. No behaviour differs from the TZ's description — only the
function name in it does.

**4. `_tx_merge` is a third module-level helper where §4.1 names two.** Folding a
callee's transport record into a caller's is needed at three sites (the tail top-up in
`_vision_rows` and both aggregation points in `_fetch_best`). Writing the same four
lines three times is the duplication inv. 20 exists against, so the fold has one
definition site. `_tx` and `_tx_add` are unchanged in name and shape and section H calls
them by name as §4.1 requires. `_tx_add` accumulates `slept` on every result and moves
`exhausted` only on a failed one, which is a superset of the «folds one failed result»
the TZ describes and matches it on the failure path exactly.

**5. `attempt` skips the alias leg when the primary leg is already exhausted.** §4.4
specifies what happens when the ALIAS leg is exhausted; it does not say what happens
when the leg that triggered the lookup is. Since such a coin has already failed
`won_clean`, fetching its alias would spend budget on a series that will be discarded —
the same reasoning §4.2 gives for aborting a leg. Recorded because it is a choice, not a
reading.

**6. The removed `429/418` branch moved no measured count.** §4.3 requires this stated
under `## Deviations` if any count moved with it. None did: the guard bench delta is
exactly section H's 57, `verify_bench.py` is unmoved at 40, and both selftest blocks are
byte-identical. The branch is unreachable offline, so no existing fixture exercised it.

**7. One `_http` record correction, made after the first green run.** On a retry status
that never cleared, the record still carried the error body while its own contract says
`content` is `b""` when not `ok`. Cleared before returning. Found by re-reading the
implementation against its docstring, not by a bench.

## Pre-existing Issues

**1. `--selftest` and `--lab-selftest` fail on their own defaults.** `DEF_HTML` and
`DEF_BOT` point at `bench/Скрипт_Код_CriptoCalculator.html` and
`bench/Код_для_Bota_на_GitHub.py`, neither of which exists in the repository; both modes
end in `FileNotFoundError` unless `--html ../index.html --bot ../main.py` is passed, as
`backtest_bench.yml` does. Present on `origin/main`, untouched here, and named because
items 10 and 11 are meaningless if run the obvious way — the first attempt of each in
this session produced exactly that traceback.

**2. `backtest_guard_bench.py` deletes `bench/_*_bridge.js` on exit**, which are shared
with any concurrently running `backtest_bench.py` mode. A guard run overlapping a
`--lab-selftest` run killed the latter with `MODULE_NOT_FOUND` from node. This is a
session-parallelism hazard, not a product defect — the gate runs its steps in sequence —
and it is recorded because the resulting failure looks like a product crash and is not
one. The affected run was discarded and re-run serially.

**3. The duplicate section letter `E`** in `backtest_guard_bench.py` is left alone, as
map §10 requires: a section letter appears in the immutable report of the TZ that
created it. The new section is `H`, read off the file's existing letters and not
counted.

## Remaining Risks

1. **The repair is proven against a stub, by design.** §2 requires it: a transport
   repair proven against the real network would be proven against whichever weather the
   session met. The real archive's behaviour under load — whether resets cluster, and
   whether 600 s is generous or tight against thirty-one coins — is unmeasured and is
   the dispatch's to answer.
2. **`HTTP_BUDGET_S` is derived from a workflow timeout, not from a measurement.** The
   8.3 % figure is arithmetic on `timeout-minutes: 120`. If the job's step count or
   timeout changes, the derivation is stale in a way nothing will report. `--fetch`
   prints the consumption, which is the mechanism by which the constant becomes
   movable.
3. **A coin can now be silently absent from a run's universe in a new way.** It is named
   on its census line and in the closing `связь исчерпана` line, and `ok < 8` still
   stops the run — but a run reaching, say, twenty-eight of thirty-one now succeeds
   where it previously died loudly. That is the intended trade (§3.10b: a universe that
   is stated), and it is a real change in what a green run means.
4. **`r.json()` inside the retried block** means a `JSONDecodeError` — a
   `RequestException` subclass in modern `requests` — is treated as transport and
   retried. Defensible for a truncated body, but it is a status-carrying reply being
   classified as exhaustion, which is the one merge inv. 70 warns about. Narrow: it
   reaches only the three `want_json` callers.

## Commit

Implementation, on `claude/tz-38-fetch-transport`, pushed before this report was
written and therefore measured — `ddd53d7bdc809ab91d5dc6ebf0796903e5ad42b1`:

```
TZ-38: one transport for the bench — answered, absent, exhausted
```

with the stage-by-stage body carried in the commit and the `Co-Authored-By` trailer.

This report's own commit carries the message

```
docs(reports): TZ-38 — one transport for the bench, exhaustion as its own verdict (TZ-38)
```

and nothing is stated here about its outcome: it has not happened as this section is
written (inv. 54).

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/34** —
`claude/tz-38-fetch-transport` → `main`. Not merged, and merging is the Boss's decision
after the Architect's audit.

## CI Execution

`Bench gate` ran on the runner against `ddd53d7`, twice, and both concluded **success**:

| Run | Event | Conclusion |
|---|---|---|
| `34405177810` | `push` | **success** |
| `34405278088` | `pull_request` | **success** |

All nineteen steps of the push run are `success`, including step 9
(`verify_bench.py`), step 10 (`direction_bench.py --props --fixtures --control --sim`)
and step 19 (`backtest_guard_bench.py`). Step 10 is the step whose local counterpart is
red on this host, and its hosted result is the fourth fact in the item 13 attribution.

`backtest_bench.yml` did not run and was not dispatched: it is not named by this TZ, it
needs the archive, and the archive reading is not part of this work.

## Final Repository State

**NOT IN EFFECT UNTIL MERGED.**

What this session leaves behind is the branch `claude/tz-38-fetch-transport` at
`ddd53d7bdc809ab91d5dc6ebf0796903e5ad42b1`, pushed, green on the hosted gate, and
carrying exactly two modified files. `bench/backtest_bench.py` and
`bench/backtest_guard_bench.py` on `main` are unchanged until the pull request is
merged, and until then no `backtest_bench.yml` dispatch benefits from any of this.

The working tree was left clean: no bench scratch file, no `_*_bridge.js`, and
`__pycache__` is ignored by `.gitignore:6`.

## Fingerprints

Map revision string, as carried in its `## 0. Fingerprint` block:
`**Revision 2026-09-09-b.**`

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2705 | `9ac61f1dea9e6f349ac5a41e743943af` |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Added by this TZ's gate table, measured **before** the edits and matching it exactly:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4258 | `11654488e2e5637c00fc9ae1f1880916` |
| `bench/backtest_guard_bench.py` | 1425 | `b42b660d3ede3196ba6c1c694d8f7fde` |

The same two files **after** the edits, on the pushed branch:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4555 | `deac9dd8a53f2047c25c2d6fb24f09b4` |
| `bench/backtest_guard_bench.py` | 1726 | `ce08dd99edebfa90d8fce3dd6b7ba472` |

The six gate files above were re-measured after all edits and are unchanged, which is
the arithmetic form of «no production file was written».
