# TZ-38 — One transport for the bench, and exhaustion as its own verdict

**Canonical filename: `CryptoTZ/TZ-38-fetch-transport.md`.** Name the committed file from
this line, never from the name the file arrived under (contract §3).

| Field | Value |
|---|---|
| Report | `CryptoReports/TZ-38-fetch-transport-report.md` |
| Branch | `claude/tz-38-fetch-transport` |
| Class | **branch TZ** — the scope names files outside `CryptoReports/**` (contract §8) |
| Model | **Opus** |

---

## 0. Fingerprint gate — blocking

Run contract §5 before any work. Required map revision, matched as an exact substring:

```
**Revision 2026-09-09-b.**
```

`SYSTEM-MAP-CRYPTOCALCUL.md` at this revision is **2705 lines**, MD5
`9ac61f1dea9e6f349ac5a41e743943af`.

All seven content anchors must be present, each matched as an exact, **case-sensitive**
substring:

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-09-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` |

**The report states the LINE NUMBER at which each anchor matched, not a verdict that it
did.** «All seven matched» is the sentence that has already been wrong once (map §0, §10):
a line number is an artifact, a verdict is a claim.

The map's `## 0` file table at this revision — measure each and report under
`## Fingerprints`:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**The two benches this TZ edits have no row in that table by design (map §0), so their
figures are stated here** and are part of this gate:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4258 | `11654488e2e5637c00fc9ae1f1880916` |
| `bench/backtest_guard_bench.py` | 1425 | `b42b660d3ede3196ba6c1c694d8f7fde` |

Contract required: `EXECUTOR-INSTRUCTIONS.md` **v20**, 814 lines, MD5
`9a257890e9db663eb0fc74129f4841e0`.

---

## 1. What is wrong

`backtest_bench.yml` run **#19** (09.09.2026T17:42Z, `f7fad89`) concluded `failure` at step 9
«Закачка истории». Steps 10–18 are `skipped`, so the dispatch answered none of the three
questions it was launched for: `prod_anchor` still has no archive figure, the `unexplained`
class on UNI, XLM and ZEC is still unread, and no funding archive was refreshed.

The cause is not the archive. `bench/backtest_bench.py` calls `requests.get` at seven sites
and **six of them have no handler at all** — `_vision_rows` at its monthly and daily loops,
`_rest_rows`, `fetch_funding`, `fetch_cg` and the live-`coeffs` reader in
`verify_against_live`. The seventh, in `probe`, carries its own `try/except` and is the only
one a reset does not end. One `Connection reset by peer` on one month of one coin therefore
ends the download of thirty-one.

**The obvious repair is worse than the crash, and this TZ exists to specify the one that is
not.** Map inv. 70, in full:

> 70. **A transport failure is NOT an absence of data.**
>     A reply is data whatever its status: `404` on a monthly ZIP means that month is not
>     published, and the census counts it, refills from the dailies and says so. A request
>     that never completed is a fact about the NETWORK, and merging the two is how a loud
>     failure becomes a silent one. … Catching the exception and counting the month absent
>     writes a series short by exactly the hours the reset covered, and inv. 63 already
>     records what a short series does: it raises nothing, because it is a smaller sample
>     that still answers. The repair is therefore THREE outcomes where the code has two —
>     answered, absent, exhausted — with exhaustion failing the COIN, naming itself in the
>     census, never reaching `_save` and never incrementing the counter that means «not in
>     the archive».

Inv. 63 and inv. 64 are the reason the bar is set there rather than at «the run survives»:
both record defects whose whole danger was that a shortened or spliced series **still
answers**, and neither was found by a red bench. A partial download is that same failure
arriving through the network instead of through a rename.

---

## 2. Scope

Two files, both benches:

| File | Stages |
|---|---|
| `bench/backtest_bench.py` | A, B, C, D |
| `bench/backtest_guard_bench.py` | E |

**Touches — every control that asserts what these stages change.** Enumerated here because a
TZ that changes a shape and does not name the benches asserting it costs a whole extra
specification (map §10, TZ-34):

- `bench/backtest_guard_bench.py` section B calls `bb._vision_rows(...)` at four sites and
  unpacks three values. Stage B changes that arity; Stage E updates every one of them.
- `bench/backtest_guard_bench.py` sections B and E install a fake `requests` module carrying
  only `get`. Stage A uses `requests.Session` and `requests.exceptions`; Stage E extends the
  stub to carry both, because a stub that does not model the interface production uses is a
  control measuring something else (inv. 22).
- `bench/verify_bench.py` imports `backtest_bench` at module scope (gate step 4). It is NOT
  edited and its count must not move; item 9 measures it.
- `bench/backtest_guard_bench.py` sections D, F and G call `target_gate`, the anchored arm and
  `d4_partition`. None is in scope and none may move.

**Nothing else may be written.** `index.html`, `main.py`, `catalysts.json`,
`.github/workflows/**`, `SYSTEM-MAP-CRYPTOCALCUL.md`, `EXECUTOR-INSTRUCTIONS.md`,
`ANALYST-INSTRUCTIONS.md`, `journal/**`, `analyst/**` and every other bench appear in no
diff. Hard floor item 8 stands: `backtest_bench.yml` is not named by this TZ and is not
touched.

**No session fetches anything** (hard floor item 9, inv. 44). Every stage below is
verifiable offline against a stubbed `requests`, and that is not an accident of convenience:
a transport repair proven against the real network would be proven against whichever weather
the session met. The archive reading is a dispatch, after merge, and it is the Boss's.

---

## 3. Stage A — `_http`, the one place this file touches the network

Add two module-level helpers and four module-level constants to `bench/backtest_bench.py`,
above `probe`. After Stage D they are the file's only contact with `requests`.

### 3.1 The constants, and why each number is what it is

```python
HTTP_TRIES    = 3                  # one attempt plus two retries
HTTP_BACKOFF  = (2.0, 8.0)         # seconds slept before retry 1 and retry 2
HTTP_RETRY_ST = (408, 418, 425, 429, 500, 502, 503, 504)
HTTP_BUDGET_S = 600.0              # retry sleep allowed across the whole process
```

These judge the NETWORK, not the market, so inv. 32 does not reach them. What does reach
them is that a constant whose consequence nobody can see is a constant nobody can move, so
each is derived here and its consumption is printed by Stage C:

- **`HTTP_BUDGET_S = 600.0`.** `.github/workflows/backtest_bench.yml` carries
  `timeout-minutes: 120` for a job of thirteen bench steps. 600 s is 8.3 % of that job, so a
  host that black-holes every request cannot consume the dispatch: it fails the coins it touches
  and the run reaches the modes that do not need them. Once the budget is spent every
  subsequent call makes exactly one attempt and sleeps not at all.
- **`HTTP_TRIES = 3` with `HTTP_BACKOFF = (2.0, 8.0)`.** Worst case per URL is 10 s of sleep
  plus three times the caller's own timeout — 190 s against the archive's `timeout=60` — and
  the budget bounds the total however many URLs reach it.
- **No jitter.** Jitter spreads a herd; this is one sequential client with no herd to
  spread, and determinism lets section H assert the ladder exactly rather than bound it.
  Alternative discarded in one line: full jitter `U(0.5, 1.0) · base`.

### 3.2 `_session()`

Returns a `requests.Session`, created on first use and reused thereafter — connection reuse
across the hundreds of ZIPs one `--fetch` requests from one host is the point.

**The cached session is keyed on the `requests` module object itself and rebuilt when that
object changes.** `backtest_guard_bench.py` installs a fresh fake `requests` several times in
one process and pops it in between; a session cached across installs would keep recording
into a dead stub, and a control that measures the wrong recorder is worse than no control
(inv. 22).

### 3.3 `_http(url, timeout, params=None, tries=HTTP_TRIES, want_json=False, session=None)`

Returns a RECORD, never a `requests.Response`, so that no caller can read a status off an
object that may not exist:

```python
{"ok": bool,        # a reply arrived — ANY status, 404 included
 "status": int|None,
 "content": bytes,  # b"" when not ok
 "json": obj|None,  # only when want_json and ok
 "tries": int,      # attempts actually made
 "slept": float,    # seconds this call spent in backoff
 "why": str}        # "" when ok; else the exception type name or "HTTP 503 ×3"
```

Rules, in force for every caller:

1. **`ok` means a reply arrived.** `404` is `ok: True, status: 404`. The month is not
   published; that is data.
2. **Retry only on transport and only on `HTTP_RETRY_ST`.** A `404`, `403` or `451` is
   returned on the first attempt with `tries == 1`: retrying an answer spends the budget the
   real failures need, and the daily-refill loop legitimately produces hundreds of 404s.
3. **The caught set is `(requests.exceptions.RequestException, OSError)` and nothing wider.**
   `ConnectionResetError` and `socket.timeout` are `OSError`; a bare `except Exception` would
   convert a `TypeError` in a URL builder into a network verdict, which is this TZ's own
   defect committed one level up. A non-matching exception propagates.
4. **The body read is inside the retried block.** A reset arriving while the ZIP is read is
   the failure that killed run #19, and a helper that retried only the connect would not
   catch it.
5. **Sleeping is injectable.** `_http` calls a module-level `_SLEEP` (default `time.sleep`)
   so section H asserts the ladder without spending 10 s per fixture. `_SLEEP` is not a
   parameter of every caller; it is one module attribute the bench rebinds and restores.
6. **The budget is global and monotone.** Each sleep adds to a module counter; when the
   counter is at or over `HTTP_BUDGET_S`, `tries` collapses to 1 for every later call. A
   reader function `_http_spent()` returns the counter for Stage C to print.

---

## 4. Stage B — the archive readers return a transport record

### 4.1 The record

```python
tx = {"exhausted": int,     # requests that never got a reply after their budget
      "url": str|None,      # the FIRST such URL
      "why": str,           # its `why`
      "slept": float}
```

A helper `_tx()` builds the zero record and a helper `_tx_add(tx, url, r)` folds one failed
`_http` result into it. Both are module level and section H calls them by name (inv. 21).

### 4.2 `_vision_rows(pair, is_fut, t_beg, t_end)` → `(rows, gone, note, tx)`

- Every `requests.get` becomes `_http(u, timeout=60)`.
- **`gone` counts only answered-and-absent months.** An exhausted request never increments
  it. This single line is what inv. 70 is about and section H asserts it from both sides.
- **The leg ABORTS on the first exhaustion**, monthly loop or daily loop: it returns
  immediately with what it has and `tx["exhausted"] >= 1`. The coin has already failed;
  spending the run's budget on its remaining months buys a series that will be
  discarded. Section H proves the abort from the stub's URL record and not from the row
  count — a row count cannot tell «not requested» from «requested and empty» (inv. 22).
- The tail top-up keeps every property inv. 64 gives it: spot only, mirror only, stopping at
  the last complete hour. When the top-up call is EXHAUSTED rather than answered, `note` says
  so in words that are not «HTTP None», and `tx` carries it.

### 4.3 `_rest_rows(host, path, pair, t_beg, t_end)` → `(rows, code, tx)`

- One `_http` per page. On exhaustion return `(None, None, tx)`.
- **The `if r.status_code in (429, 418): time.sleep(30); continue` branch is REMOVED**, its
  work now being the helper's: both codes are in `HTTP_RETRY_ST`. This is a deliberate
  behaviour change and it is a narrowing — the old branch looped without bound, and a run
  that never ends reports nothing at all. Three bounded attempts and a named failure are
  strictly more informative. The report states the removal under `## Deviations` if it turns
  out to change any measured count.
- The `time.sleep(0.25)` pacing between pages stays. It is not a retry.

### 4.4 `_try_alias` — the splice may not run on a truncated leg

`_try_alias` fetches the pre-rename ticker and hands both legs to `_splice`, whose bar is
**derived from the two legs' own hourly extremes** (inv. 49, 63). A leg cut short by a reset
would move that bar with it, and the splice would then be admitted or refused by an accident
of the network.

If the alias leg's `tx["exhausted"]` is non-zero: **do not splice.** Return
`(new_rows, pair)` — the symbol enters by its post-rename leg alone, exactly as a refused
splice does — and print one line saying the old leg was not read, distinct in wording from
`ОТКЛОНЕНА`. A refusal is an arithmetic verdict; this is not one.

---

## 5. Stage C — the coin's verdict

### 5.1 `attempt` and `_fetch_best`

`attempt(is_fut)` returns `(rows, why, ticker, note, tx)`.

`_fetch_best(legs, attempt, pair, t_ref)` returns
`(rows, why, ticker, note, P, V, HL, cov, tx)` and gains ONE rule:

> **A leg that suffered exhaustion is not eligible to win.** It is not compared on length and
> it does not trigger the `>= 2600` early break.

Because a partial leg can be longer than a complete one, and «keep the longest» would then
prefer the damaged series over the sound one — inv. 70's single arithmetic clause, and the
mechanism by which a naive repair truncates silently.

The returned `tx` is the aggregate over the legs ATTEMPTED, plus one key the caller branches
on:

```python
tx["won_clean"] = bool(rows) and the winning leg's own `exhausted` == 0
```

A coin whose spot leg died on transport and whose futures leg answered in full is therefore
usable, and the census line still NAMES the dead leg — a fact discarded in silence is what
this TZ removes.

### 5.2 `fetch_prices`

Immediately after `_fetch_best`, **before the `len(rows) < 2600` skip and before `_save`**:

```python
if not tx["won_clean"]:
    print_census(sym, ticker, cov,
                 "СВЯЗЬ ИСЧЕРПАНА: %d запрос(ов) без ответа (%s) — монета НЕ сохранена"
                 % (tx["exhausted"], tx["why"]))
    dead.append(sym)
    continue
```

`dead` is a list initialised beside `ok` at the top of `fetch_prices`. Order is load-bearing:
a partial series can clear 2 600 hours and a 5 % hole fraction and be saved as a healthy
coin. The transport verdict runs first and there is no path from it to `_save`.

The verdict token is NEW. «НЕТ ДАННЫХ», «МАЛО ИСТОРИИ» and «нет N месячных файлов» keep
their present meanings and must be unreachable from an exhausted leg — asserted in section H
rather than argued here.

`--fetch` ends with, in addition to `монет в кэше: %d из %d`:

```
связь исчерпана на N монет(ах): SYM, SYM — ретраи потратили S с из BUDGET
```

printed only when `N > 0`. **The exit code does not change**: a coin fails, not the run, and
`ok < 8` remains the only `sys.exit` in this function. A run that reaches twenty-eight coins
of thirty-one is a run whose universe is stated, which is how every standing result in this
map is already described (§3.10b).

### 5.3 `fetch_funding`

The same defect and the same repair. `miss` counts answered-absent months only; an exhausted
request aborts that coin's funding leg, prints `СВЯЗЬ ИСЧЕРПАНА` instead of
`funding МАЛО (… нет N мес.)`, and **writes no `_fund_<SYM>.json`**. The `ok < 8` exit is
unchanged.

---

## 6. Stage D — the remaining three sites, and the census that keeps them at one

- **`probe`** routes through `_http(url, timeout=20, tries=1)`. One attempt is the point of a
  twenty-second diagnosis. The `451` branch reads `r["status"]`; the «нет связи» line reads
  `r["why"]`, which carries the same exception type name it prints today.
- **`fetch_cg`** routes through `_http(..., want_json=True)`. Its explicit `429` branch goes
  the way `_rest_rows`'s did; on an exhausted chunk it prints the chunk failure and continues
  to the next, which is what the existing non-200 branch already does.
- **`verify_against_live`** routes the `GIST_LIVE` read through `_http(..., want_json=True)`
  and, on exhaustion, exits with a named message rather than a traceback:
  `СТОП: живой coeffs.json не получен: <why>`. Printing a failure is not returning one
  (contract §9); `sys.exit` with a message returns 1 and says why on one line.

**Census, and it is a delivery condition.** After Stage D:

- `requests.get(` appears in `bench/backtest_bench.py` **exactly once**, inside `_http`.
- `requests.Session(` appears **exactly once**, inside `_session`.
- `import requests` appears **at most twice**, in the transport helpers only.

The report states each count with the command that produced it. One definition site is the
whole reason this TZ is one helper and not six patches (inv. 20).

---

## 7. Stage E — section H in the garrison

`bench/backtest_guard_bench.py`, gate step 14, offline, `requests` stubbed, no socket
opened.

**The section letter is `H`.** The file carries A, B, C, D, E, E, F, G; the letter is chosen
from the FILE and never by counting, the duplicate `E` is left alone, and map §10 says why —
a section letter appears in the immutable report of the TZ that created it.

### 7.1 The stub must model what production now uses

`Archive.install()` currently sets only `fake.get`. It gains:

- `fake.Session` — a factory returning an object whose `get` is the same recorder, so
  connection reuse is exercised rather than bypassed;
- `fake.exceptions` — a namespace carrying `RequestException(Exception)`;
- fault injection: `Archive(faults={"substring": n})` raises a transport exception the first
  `n` times a matching URL is requested, and records the attempt either way.

`_SLEEP` is rebound to a recorder for the section and restored after it, so the section
asserts the ladder and sleeps for none of it.

### 7.2 What the section asserts

Every assertion calls a production function by name and compares its return (inv. 21).
Both halves of inv. 68 are covered: what must move and what must not.

1. Two faults then an answer: `ok` true, `tries == 3`, recorded sleeps exactly `(2.0, 8.0)`.
2. Faults throughout: `ok` false, `tries == HTTP_TRIES`, `why` naming the exception type.
3. A `404` is not retried: `tries == 1`, `ok` true, `status == 404`.
4. A `503` is retried and exhausts; a `403` is not retried.
5. `_vision_rows` with an exhausting monthly URL: `gone` does not count it, `tx["exhausted"]`
   is non-zero, and the Archive's URL record proves the later months were never requested.
6. `_vision_rows` with an absent monthly and healthy dailies: `tx["exhausted"] == 0`, `gone`
   counts the month, the dailies refill it. **Items 5 and 6 together are inv. 70**: neither
   fact can be read off the other.
7. `_fetch_best` with a synthetic `attempt`: an exhausted LONG leg and a clean SHORT one —
   the clean leg wins, `won_clean` true, and the census `venue` is the clean leg's.
8. `_fetch_best` with every leg exhausted: `won_clean` false, `rows` empty.
9. Budget spent: a further call makes exactly one attempt and records no sleep.
10. **Negative control on the caught set**: a stub raising `TypeError` propagates out of
    `_http` — a code defect is not a network verdict.
11. **Zero control**: a world of nothing but healthy URLs leaves every transport counter at
    zero and every verdict unchanged. Without it the section could be green because every
    fixture is red.
12. Host discipline: the section's whole URL record contains no host outside the two the
    fixtures name, by the same `hostset` check sections B and E already use.

Section H prints its own comparison count on one line, exactly as F and G do, so the gate
delta is attributed by the section rather than by arithmetic in the map (map §0).

---

## 8. What must not change

1. **No production file.** Not `index.html`, `main.py`, `catalysts.json`, a workflow, a
   contract, the map, or anything under `journal/**` or `analyst/**`.
2. **`_save`'s skip rules are untouched** — 2 600 hours and a 5 % hole fraction are what they
   were, so the census beside them measures the same coins against the same bar (inv. 47).
3. **`_splice`, `ALIAS`, `census`, `census_of_doc`, `_venue_name`, `_venue_licence`,
   `CLASSES`, `HARD_CLASSES`, `target_gate` and `d4_partition` are not edited.**
4. **`gone` and `miss` keep their present meaning** for answered-absent months. This TZ
   removes what they were about to absorb, and changes nothing they already count.
5. **The tail top-up stays spot-only and stops at the last complete hour** (inv. 64).
6. **No bench is edited to make it pass** (hard floor item 2). If a stage turns an existing
   assertion red, that is a finding: report it, do not soften it.
7. **No second implementation of any rule** (inv. 21, 38). The helper is transport; it
   contains no archive knowledge, no month arithmetic and no verdict text.

---

## 9. Validation — definition of done

Every item runs. An item that cannot be run FAILS; it is never «not applicable»
(contract §9).

| # | Item | Artifact and source |
|---:|---|---|
| 1 | `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py` | exit code, in-session |
| 2 | `git diff --numstat origin/main` names exactly the two in-scope files | the diff's own file list, not recollection |
| 3 | Fingerprint gate: the LINE NUMBER at which each of the seven anchors matched, map lines and MD5, the four file-table rows, both bench figures, contract v20 | repository copies, in-session |
| 4 | Baseline `python3 bench/backtest_guard_bench.py` recorded BEFORE the first edit — count and FAIL | stdout, in-session |
| 5 | Final guard run: `FAIL 0`, and `final − baseline` equals section H's own printed count | stdout, in-session |
| 6 | Census of Stage D: `grep -c "requests\.get(" bench/backtest_bench.py` is 1, `grep -c "requests\.Session(" ` is 1, `grep -n "import requests"` lists the transport helpers only | commands and their output |
| 7 | Negative assertions — superseded vocabulary is ABSENT: no `status_code in (429, 418)` in `_rest_rows`, no `time.sleep(30)` retry branch, no bare `requests.get` outside `_http`. A hit blocks delivery | `grep -n`, output quoted |
| 8 | Section B's `_vision_rows` call sites updated for the new arity — proven by the section running, since a stale unpack raises | stdout, in-session |
| 9 | `python3 bench/verify_bench.py` reads **40, FAIL 0** — gate step 4 imports this module and must not move | stdout, in-session |
| 10 | `--lab-selftest` D1–D9 printed lines byte-identical to the pre-edit baseline (`md5sum` on the captured block) | stdout, in-session, offline |
| 11 | `--selftest` offline block unchanged against its own baseline | stdout, in-session |
| 12 | Section H item 10 — the `TypeError` negative control — is shown failing when the caught set is widened to `Exception`, then restored | stdout, in-session |
| 13 | Full local `bench.yml` replay: fourteen steps with counts; step 5's known local ceiling stated as such (map §10) rather than reported as a product failure | stdout, in-session |
| 14 | Hosted `Bench gate` on the pushed branch: run id and conclusion where the API is readable; where it is not, state only that the branch was pushed and that the changed paths clear the workflow's filters — never a forecast (contract §9, inv. 54) | GitHub |
| 15 | No CI wiring changed, so contract §9's negative-CI-test clause does not fire; the negative controls are section H items 10 and 11, and the report says so explicitly | this TZ |
| 16 | No fetch of any external host was performed by the session (hard floor item 9, inv. 44) | stated in the report |

**The archive reading is NOT part of this TZ.** After merge, one `backtest_bench.yml`
dispatch answers three open rows at once — `prod_anchor`'s figure, the `unexplained` class,
and whether the transport repair holds on the real archive. That dispatch is the Boss's and
no forecast about it belongs in the report.

---

## 10. Report

Contract §10 template, in full. Beyond it, this TZ requires:

- the seven anchor line numbers (item 3), not a verdict;
- baseline and final guard counts, and section H's own printed count beside their difference;
- the Stage D census commands with their output;
- every deviation classified rather than silently corrected — in particular the removed
  `429/418` branch of `_rest_rows` if any count moved with it;
- `## Final Repository State` carrying **NOT IN EFFECT UNTIL MERGED**.
