# Implementation Report — TZ-39

## Status

**COMPLETED.** All three scopes were implemented and all eight validation items ran. Two
expected readings in the TZ could not be produced by any code the TZ authorises. Both are
recorded under `## Deviations` and neither was forced:

- **C4 lists H-p5 as must-turn-RED. It stays green under every revert that was
  measured.** A record that ends in success is overwritten field by field on its success
  exit, in TZ-38's code and in this repair alike, so no revert of the ordering can make
  it carry a value from the failed attempt.
- **C2's H-c1 asks for a transport record "naming the coin". `_rest_rows`'s record
  cannot do that.** It folds `host + path`, and the pair travels in `params`. Making it
  name the coin means editing a caller that already has an exhaustion path, which A5
  forbids.

The previous TZ's branch **was merged**: `claude/tz-38-fetch-transport` landed as PR #34
(`fab9ca5`). This work is not built on an unmerged base.

## Inbound Filing

None. `CryptoTZ/TZ-39-transport-outcome-and-budget.md` already carried its canonical
filename and arrived on `origin/main` in `8effead`. No artifact was moved or renamed.

A second copy exists **on another branch**. `origin/seahomebatumi-ai-patch-1` (`5d0f069`,
parent `c11161d`) uploads TZ-39 and TZ-40 again. `git diff origin/main
origin/seahomebatumi-ai-patch-1` is empty, so the two copies are byte-identical and the
TZ was not replaced in place. Nothing was done to that branch.

## Scope Executed

**Class: branch TZ** (contract §8). `## Scope` names two files outside
`CryptoReports/**`.

Scope A and Scope B are in `bench/backtest_bench.py`; Scope C is in
`bench/backtest_guard_bench.py`. Nothing else was written.
`.github/workflows/backtest_bench.yml` was not touched (hard floor item 8), and no bench
file was added (item 12).

## Files Created

None.

## Files Modified

| File | Before | After |
|---|---|---|
| `bench/backtest_bench.py` | 4555 lines, `deac9dd8a53f2047c25c2d6fb24f09b4` | 4572 lines, `ce38ef842b60699b9ea34dad4f322a29` |
| `bench/backtest_guard_bench.py` | 1726 lines, `ce08dd99edebfa90d8fce3dd6b7ba472` | 1986 lines, `1580b9a02b7d4453cd3eebd0b25e33ad` |

`git diff --stat origin/main` on the implementation branch:

```
 bench/backtest_bench.py       |  67 +++++++----
 bench/backtest_guard_bench.py | 266 +++++++++++++++++++++++++++++++++++++++++-
 2 files changed, 305 insertions(+), 28 deletions(-)
```

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

Line numbers below refer to the pushed branch, `396f961`.

### Scope A — `_http` decides its outcome after the last step that can fail

**A1.** In the non-retry branch (`bench/backtest_bench.py:1058-1068`) the body is read,
then parsed (`:1063`), and only then is the record written with `ok = True` (`:1065`).
If the parse raises, control reaches the caught branch before `ok` exists. Under
`requests` 2.31 (measured in this session) `JSONDecodeError`'s MRO includes
`RequestException` and `OSError`, so the parse failure lands in the existing caught set.
A parse failure is therefore a failed ATTEMPT and is retried on the existing ladder. No
constant, field name or helper was added, and `HTTP_TRIES`, `HTTP_BACKOFF`,
`HTTP_RETRY_ST` and `HTTP_BUDGET_S` are unchanged (A6).

**A2 — the record's fields and `_http`'s exit paths.**

The record carries seven fields: `ok`, `status`, `content`, `json`, `tries`, `slept`,
`why`. Five describe an ATTEMPT (`ok`, `status`, `content`, `json`, `why`). Two describe
the CALL: `tries` is written at the top of every attempt and `slept` on every backoff
rung, so both are current at every exit.

| Exit | Reached when | Writes |
|---|---|---|
| E1 — success, `:1065-1067` | the reply's status is not in `HTTP_RETRY_ST`, and the parse (where one runs) returned | `ok=True`, `status`, `content`, `json` (parsed, or `None`), `why=""`. All five, in one place, after the parse |
| E2 — failure, `:1081-1083` | every attempt ended in a caught exception (transport or parse) or a retry status | `ok=False`, `status` (the last attempt's: `None` after an exception, the status after `HTTP 5xx ×N`), `content=b""`, `json=None`, `why` (the last attempt's). All five |
| E3 — propagation | an exception outside `(RequestException, OSError)` — e.g. H10's `TypeError` | no record leaves `_http`, so no field can stand beside the failure |

The budget-spent branch (`tries = 1`) is not an exit: it narrows the loop and enters it.
Before this TZ, E1 wrote `status` and `content` BEFORE its outcome was known and set `ok`
BEFORE the parse, and E2 wrote only `content`. That is how `ok = True` from the pre-parse
stage outlived the parse failure. Each attempt now holds its `status` and `why` in
locals, and only E1 and E2 write the record.

**A3 — the one place a reading was needed, recorded rather than chosen silently.** The
body is parsed "only where the status says a payload is there". The code takes that to
be `status == 200` (`:1063`). That is the status every `want_json` caller reads `json`
under: `_rest_rows` returns on `status != 200` before reading `json` (`:1290`), and
`fetch_cg` does the same (`:1567`). A wider set such as 2xx was considered and rejected
on the TZ's own rule in A4, inv. 20. It would be a second definition of "a payload
status", and it would disagree with the callers' own. The effect is that a `404` page
served as text is answered with `status: 404`, `tries: 1`, `json: None`, and is never
retried or folded as exhausted (H-p3). A `404` whose body happens to be JSON is also not
parsed (H-x4).

**A4.** `_tx_add` is unchanged. It reads `not ok`, and with `ok` correct it folds
exactly the exhausted requests.

**A5 — the three callers, verified and not rewritten.** Each receives `ok: False` from
H-p1's stub and takes the exhaustion path it already had. **No line was added to any
caller.**

| Caller | Exhaustion path it takes | Proof | Before this TZ (C4 variant b) |
|---|---|---|---|
| `_rest_rows` | `if not r["ok"]: return None, None, tx` (`:1287`) — `tx` = `{exhausted: 1, url: host+path, why: _FakeJSONDecodeError}`, `HTTP_TRIES` requests, no second page | H-c1, 4 assertions | returned `(None, None, tx)` with an EMPTY `tx`; red on the transport-record assertion |
| `fetch_cg` | `if not r["ok"]: print("… чанк -> связь исчерпана (%s)"); time.sleep(2); continue` (`:1564`) — per chunk, no raise, no cache document | H-c2, 4 assertions | `TypeError: %d format: a real number is required, not NoneType`; red on 3 |
| `reconcile` | `if not _r["ok"]: sys.exit("СТОП: живой coeffs.json не получен: %s")` (`:1691`) — exits before `live` is bound, nothing dereferenced | H-c3, 3 assertions | `AttributeError: 'NoneType' object has no attribute 'get'`; red on 2 |

### Scope B — the retry budget prints on every pass

`fetch_prices` (`:1522`) and `fetch_funding` (`:2601`) now print the existing line
outside `if dead:`, once per pass, before the `ok < 8` exit. The string, its arguments,
`_http_spent()` and `HTTP_BUDGET_S` are verbatim (B2). The two edits are a dedent and a
comment each.

**B4 — the mode that reaches `fetch_funding`: `--fetch-funding`** (`ap.add_argument`,
`:4392`; dispatch `if a.fetch_funding: return fetch_funding(a.html, a.years)`, `:4410`).
**Map §3.10's mode list does not carry it.** The list reads `--probe · --selftest ·
--fetch · --verify · --run · --regimes · --stops · --res7 · --funding · --target ·
--lab-selftest`. **A second argparse mode is missing from it too: `--regime-gate`.** The
map names `--regime-gate` only in its §10 row for TZ-40, and `--fetch-funding` appears
nowhere in the map at all. Both are the Architect's to repair.

Offline demonstration, measured by `/tmp/tz39/b_demo.py`. This scratch file was not
committed. It stubs `requests`, redirects `CACHE` to a scratch directory and drives one
pass against the baseline file and against the edited file:

| Pass | Baseline (`origin/main`) | This branch |
|---|---|---|
| `fetch_prices`, all 31 cached | `монет в кэше: 31 из 31`, **no budget line** | `монет в кэше: 31 из 31` + `связь исчерпана на 0 монет(ах):  — ретраи потратили 0.0 с из 600` |
| `fetch_funding`, all 30 cached | `funding в кэше: 30 из 30`, **no budget line** | `funding в кэше: 30 из 30` + `связь исчерпана на 0 монет(ах):  — ретраи потратили 0.0 с из 600` |
| `fetch_funding`, SUI's URLs raise | `…29 из 30` + `связь исчерпана на 1 монет(ах): SUI — ретраи потратили 10.0 с из 600` | identical, byte for byte |

B5 holds: this scope moved no check count. The whole gate delta is section H's delta
(below).

### Scope C — section H gains the fixture that can fail

**C1 — the stub.** `_FakeJSONDecodeError(_FakeRequestException, ValueError)`
(`bench/backtest_guard_bench.py:219`) carries the same two bases as
`requests.exceptions.JSONDecodeError`. `Archive` gains `bodies={"substring": [(status,
raw), …]}` (`:249`): one reply per request in order, the last one repeating. The reply
is a `_RawResp` (`:320`), whose `json()` really runs `json.loads` on its body. So a
zero-length, truncated or non-JSON body raises the way production's does. `_Resp` and
every existing route are unchanged.

**H1–H12 keep their expectations byte-identical.** `git diff -U0` on the guard removes
exactly three lines: the `import` line (adds `json`), the closing line of `Archive`'s
docstring, and `Archive.__init__`'s signature (adds `bodies=None`). None of them is an
assertion.

**C2 — the new fixtures**, inserted after H12 and before the section's own zero-guard
(`:1741-1962`). Every one calls a production function by name on synthetic input, and
every assertion is one `ok(...)` call, counted where it compares:

| Id | Assertions | What it reads |
|---|---:|---|
| H-p1 | 14 | a truncated body and a non-JSON body, each on 200: not answered · `json` None · `why` names `JSONDecodeError` · no status, no body · `HTTP_TRIES` attempts, ladder `[2.0, 8.0]` · `_tx_add` folds `exhausted: 1` · `_fetch_best` with that leg returns no rows and `won_clean` false |
| H-p2 | 3 | 200, body parses: answered, 1 attempt, status/body/payload/`why` as today, not exhausted |
| H-p3 | 8 | 404 served as text: answered · 404 preserved · not parsed · not retried · not exhausted · plus H6's census world with the absent month's 404 served as text: transport-clean, `gone == 1`, dailies refill every hour |
| H-p4 | 3 | no reply at all: not answered after the full ladder · no status/body/payload · `why == '_FakeRequestException'` · exhausted |
| H-p5 | 4 | non-JSON on attempt 1, parses on attempt 2: answered on attempt 2 · `why` empty · `content`, `json` and `status` are attempt 2's |
| H-x1 | 1 | item 7: zero-length body on 200 — not answered, and says why |
| H-x2 | 2 | item 7: valid JSON of the wrong shape — answered as it came; not a transport failure |
| H-x3 | 1 | item 7: truncated first reply, then a DIFFERENT payload — the record equals the second attempt's, whole (`==` on all seven fields) |
| H-x4 | 1 | item 7: a 404 whose body is JSON — answered, not retried, not parsed |
| H-c1 | 4 | `_rest_rows`, H-p1's stub — see A5 |
| H-c2 | 4 | `fetch_cg`, H-p1's stub — see A5 |
| H-c3 | 3 | `reconcile`, H-p1's stub — see A5 |
| H13 | 2 | the host set of every archive the new fixtures installed is EXACTLY `{data.binance.vision, data-api.binance.vision, api.coingecko.com, gist.githubusercontent.com}`, and non-empty |
| **total** | **50** | |

H12 audits the TZ-38 fixtures and keeps its expectation of two hosts. `fetch_cg` and
`reconcile` must reach two more hosts, so the new block audits its own record in H13
instead of widening H12.

H-c2 needs two process-level rebinds for the one call, both restored in a `finally`.
`bb.CACHE` points at a scratch directory under the guard's own `tmp`, and `time.sleep`
is replaced by a recorder, because `fetch_cg` paces with `time.sleep(2)` per failed
chunk and not with the rebindable `_SLEEP`. `reconcile` exits with `SystemExit`, which
the existing `caught()` helper does not catch (it reads `Exception`). H-c3 therefore
wraps it locally, and `caught()` is unchanged.

**C3 — the section letter: H.** The subject is H's own. The letter is read off the file,
whose `H. TRANSPORT` header stands at the section's start. No new section was opened.

## Validation

Baselines were taken on the checkout at `8c3392f` before any edit.

**1. `python3 -m py_compile bench/backtest_bench.py bench/backtest_guard_bench.py`** →
`py_compile exit 0`.

**2. `python3 bench/backtest_guard_bench.py`** → exit 0.

| | Before | After |
|---|---:|---:|
| section H (`H. transport: N comparisons`) | 57 | **107** |
| step 14 total (`checks run`) | 323, FAIL 0 | **373, FAIL 0** |

Delta 373 − 323 = **50** = 107 − 57, section H's own delta. No other section moved:
E 32, F 29 and G 63 are the same before and after.

The gate total against **1 335 964**, term by term. `bench.yml` has 14 steps.

| Term | Figure | Source |
|---|---:|---|
| the 12 steps other than 4 and 14 | 1 335 601 | TZ §0 (1 335 964 − 40 − 323). **Not re-measured.** None of those steps imports either changed file: only `bench/verify_bench.py` and `bench/backtest_guard_bench.py` import `backtest_bench.py` among the gate's steps (`grep -ln backtest_bench bench/*.py bench/*.js analyst/*.sh` also lists `exhaustion_calib.py`, which is `calib.yml`'s, not a `bench.yml` step) |
| step 4, `verify_bench.py` | 40 | measured, before and after |
| step 14, `backtest_guard_bench.py` | 373 | measured |
| **new total** | **1 336 014** | 1 335 601 + 40 + 373; delta **+50** |

**3. `python3 bench/verify_bench.py`** → exit 0, `checks run: 40   FAIL 0`, identical
before and after. Its `FakeResp` answers 200 with a stored payload, so the A3 gate
parses exactly what it parsed before.

**4. The negative control of C4.** The implementation was committed first (`396f961`),
so every variant is a mutation of the committed file, followed by `git checkout --
bench/backtest_bench.py`. Three variants were run, because the literal one flips nothing:

- **a** — the success flag moved back before the parse, and nothing else
  (`+ rec["ok"] = True` above `:1063`). A2's failure exit still writes `ok = False`, so
  the defect does not come back.
- **b** — **TZ-38's ordering exactly**: a, plus the failure exit no longer writes `ok`
  (`- rec["ok"], rec["status"], rec["content"] = False, status, b""` → `+
  rec["status"], rec["content"] = status, b""`). The flag is set before the parse and
  never cleared by a failure, which is the defect as map §10 describes it. **This is the
  control C4 asks for.**
- **c** — `_http` replaced by the baseline commit's text verbatim (19 insertions, 32
  deletions).

| Fixture | C4 expects | a | **b** | c |
|---|---|---|---|---|
| H-p1 | RED | green | **RED** (6 of 14) | RED (6 of 14) |
| H-p5 | RED | green | **green** | green |
| H-c1 | RED | green | **RED** (1 of 4) | RED (1 of 4) |
| H-c2 | RED | green | **RED** (3 of 4) | RED (3 of 4) |
| H-c3 | RED | green | **RED** (2 of 3) | RED (2 of 3) |
| H-p2 | GREEN | green | **green** | green |
| H-p3 | GREEN | green | **green** | RED (3 of 8) |
| H-p4 | GREEN | green | **green** | green |
| H-x1 | — | green | RED (1 of 1) | RED |
| H-x2, H-x3 | — | green | green | green |
| H-x4 | — | green | green | RED (1 of 1) |
| H1–H12, H13, sections A–G | — | green | green | green |
| `checks run` | | 373, FAIL 0, exit 0 | 373, **FAIL 13**, exit 1 | 373, FAIL 17, exit 1 |

Under b, the red H-p1 lines are the three that read the outcome — `NOT answered`,
`_tx_add folds it as exhausted`, `won_clean is false` — once per body, and nothing else
in H-p1. The flip list matches C4 on seven of eight fixtures. **H-p5 is the exception and
is recorded as Deviation 1.** Variant c turns H-p3 and H-x4 red as well: the baseline
parsed a `404` body on every `want_json` call, retried a text 404 three times and
returned `status: None`. Map §10 already named "a `404` page served as text" among the
defect's triggers, and A3 closes it.

After each variant: `git checkout -- bench/backtest_bench.py`, then
`git status --porcelain` printed an empty line. After all three: guard exit 0,
`373   FAIL 0`, `porcelain lines: 0`, `HEAD = 396f961f413599d3c9f10d9252119af2e74a2f74`.

**5. No socket.** Every request any H fixture makes goes through the stub's
`Archive.get`, which appends the URL to `arch.urls` BEFORE it answers or raises. The fake
`requests` module in `sys.modules` has no transport at all. H12 reads the union of
`arch.urls` over every archive the TZ-38 fixtures installed (`H_ARCHES`), and H13 does
the same over every archive this TZ's fixtures installed (`H_ARCHES[HP0:]`). Both assert
the host set.

**The limit of that method:** a reach to the network through anything other than
`requests` never passes through the stub and is invisible to the record — `urllib`,
`http.client`, a raw `socket`, or a subprocess. For this run the limit was closed by a
second measurement:

```
unshare -rn sh -c 'ip -o link | cut -d: -f2; python3 bench/backtest_guard_bench.py'
→  lo
   H. transport: 107 comparisons
   checks run: 373   FAIL 0        (exit 0)
```

That run had a network namespace whose only interface is loopback, so a connection to
any real host would have failed. What it covers is this run of this file; it is not a
control over future edits, and loopback itself remained available.

**6. `git diff --name-only origin/main`** on the branch →

```
bench/backtest_bench.py
bench/backtest_guard_bench.py
```

The four `## 0` files, re-measured on the branch after the change: `index.html` 3799
`4e71da9badca3ccae85b656fdc3773e8` · `main.py` 518 `0e3ead8c300d2ee6783303c4bf2fb6b5` ·
`catalysts.json` 17 `f9b2dd4a3594134b2b7b603de19075c3` ·
`bench/exhaustion-calibration.txt` 175 `3b8730b254467c9df4c0a845a0f3cfb3`. All four are
unchanged.

**7. Extremes**, each its own fixture with its own assertion, all green: H-x1
(zero-length 200), H-x2 (valid JSON, wrong shape — data), H-x3 (truncated, then a
different payload — the second, whole), and H-x4 (404 carrying valid JSON). See the C2
table.

**8. The mode reaching `fetch_funding` is `--fetch-funding`, and it is absent from map
§3.10's mode list.** `--regime-gate` is absent from it as well (B4).

## Test Results

| Command | Where | Result |
|---|---|---|
| `python3 -m py_compile …` | local | exit 0 |
| `python3 bench/backtest_guard_bench.py` | local | exit 0, `373 FAIL 0` (baseline `323 FAIL 0`) |
| same, inside `unshare -rn` | local | exit 0, `373 FAIL 0` |
| `python3 bench/verify_bench.py` | local | exit 0, `40 FAIL 0` (baseline `40 FAIL 0`) |
| C4 a / b / c | local | 0 / 13 / 17 FAIL, then reverted to `373 FAIL 0` |
| `Bench gate`, push | runner, run `34657215614` | **success**, all 19 job steps |
| `Bench gate`, pull_request | runner, run `34657291190` | **success**, all 19 job steps |

## Deviations

**1. H-p5 does not turn red under C4, and no measured revert makes it.** C4 lists it as
must-turn-RED. Its record ends in SUCCESS on attempt 2. TZ-38's success exit wrote `ok`,
`why`, `json`, `status` and `content`, which is every per-attempt field, and so does this
repair's. So a value from the failed attempt 1 cannot survive into it under either
ordering, and there is nothing for the old ordering to leak. The defect lives only on
records that END in failure, which is where H-p1, H-x1 and H-c1–c3 look. The fixture was
built as specified, and it was not reshaped to force a flip. It remains a regression
guard over the success exit: a future edit that stops writing any of the five fields
there turns it red. That was not measured here, because no such variant was run.

**2. H-c1 does not assert that the transport record names the coin.** `_rest_rows` folds
its requests with `_tx_add(tx, u, r)` (`:1286`) where `u = host + path` (`:1281`) —
both lines unchanged by this TZ. The pair travels in `params` and never enters the record, so
`tx["url"]` is `https://data-api.binance.vision/api/v3/klines` for every coin. The coin
is named one level up, on the `fetch_prices` census line, which prints `sym` beside
`tx["why"]`. Making the record itself name the coin means editing a caller that already
has its exhaustion path. A5 forbids that ("add handling only to a caller that has none
… a narrow fix that looks incomplete is reported, never widened"). H-c1 therefore
asserts that the record is POPULATED (`exhausted == 1`, its URL, the parse failure) and
that the first page was the last. The coin-naming reading is left to the Architect.

**3. C4 was run as three variants, not one.** The literal "restore the old ordering" (a)
is masked by A2 and flips nothing, which means it cannot tell the defect from the repair
(inv. 22). b is the control; a and c are reported because each measures something the
Architect may want. a shows the repair has two independent layers, and c shows what the
shipped baseline did.

**4. Four assertion ids that the TZ does not name.** H-x1–H-x4 carry item 7's extremes,
so that each has its own id and its own assertion. H13 carries the new block's host
audit, so that H12's expectation stays byte-identical (C1).

## Pre-existing Issues

**1. A coin whose legs all ANSWER with no rows is reported as exhausted.**
`_fetch_best` sets `won_clean = bool(rows) and … exhausted == 0` (`:851`), so an empty
winner is "not clean" even with zero exhausted requests. `fetch_prices` then takes the
transport branch (`:1497`), printing `СВЯЗЬ ИСЧЕРПАНА: 0 запрос(ов) без ответа () —
монета НЕ сохранена` and appending the coin to `dead`. Measured offline:

```
_fetch_best((False, True), attempt → ([], 'нет 3 месячных файлов', 'XUSDT', '', _tx()), …)
→ rows=0 won_clean=False exhausted=0 why=''
```

This is inv. 70 merged in the other direction: an ABSENCE is reported as a network
failure. The `НЕТ ДАННЫХ` branch below it is unreachable for `rows == []`. It is present
on `origin/main` (TZ-38) and untouched here, because A4, A5 and §7 close this TZ to it.
It did not fire on the dispatch of 09.09 (31 of 31), but a newly listed or delisted pair
would trigger it. Scope B makes the `dead` line print on every pass, so such a coin now
appears in a line that is always read.

**2. `reconcile` checks `ok` and never `status`.** An answered non-200 gist reaches
`live.get(...)` on `None`. Measured offline with a `404` text body:

```
baseline  gist 404 text -> _http: ok=True status=None tries=3 json=None why='JDE'
baseline  reconcile RAISES AttributeError: 'NoneType' object has no attribute 'get'
TZ-39     gist 404 text -> _http: ok=True status=404 tries=1 json=None why=''
TZ-39     reconcile RAISES AttributeError: 'NoneType' object has no attribute 'get'
```

Same traceback before and after. What changed is that `_http` now reports the 404 as
the answer it is, instead of retrying it three times into `status: None`. The traceback
TZ-38 §6 set out to remove survives on this path. It is not the exhaustion path, so A5
gives no licence to add handling.

**3. `_rest_rows` validates no shape.** A 200 whose body is valid JSON but an object
raises inside the list comprehension. Measured:
`_rest_rows, 200 object body RAISES ValueError: invalid literal for int() with base 10:
'c'`. The TZ assigns this to the caller ("the caller's own validation owns it",
item 7), and the caller has none. It propagates as a code error and not as a network
verdict, which is the correct side of inv. 70, but it ends the fetch.

**4. Map §3.10's mode list is missing two argparse modes: `--fetch-funding` and
`--regime-gate`** (B4).

**5. The `--source cg` pass prints no budget line.** `fetch_prices` returns into
`fetch_cg` (`if source == "cg": return fetch_cg(...)`) before the line, and `fetch_cg`
prints only `вызовов CoinGecko: N`. It is not named by B1 or B4, so nothing was changed.

**6. `bench/verify_bench.py`'s `FakeResp` carries no `content` attribute.** `_http`'s
`getattr(r, "content", b"")` already covers that, unchanged. It is named because A3's
status gate relies on that stub's `status_code = 200`, which it does carry.

## Remaining Risks

1. **The parse runs only on 200.** A future `want_json` caller that reads an error object
   under a 4xx will receive `json: None`. No current caller does, because all three read
   `json` only under 200, but the rule lives in `_http`'s docstring, where such a caller
   would have to look.
2. **The caught set now carries the parse failure by inheritance.** In `requests` ≥ 2.27,
   `JSONDecodeError` is a `RequestException`. Older versions raise a plain `ValueError`,
   which `_http` does not catch, so it would propagate as a traceback rather than an
   exhaustion. Both workflows install `requests` unpinned (`pip install numpy requests`,
   `backtest_bench.yml:36`, `bench.yml:71`), so the runner gets a current version, but
   nothing asserts that.
3. **A clean pass now opens its budget line with «связь исчерпана».** B2 keeps the
   string verbatim, so a pass that lost nothing prints `связь исчерпана на 0 монет(ах):
    — ретраи потратили 0.0 с из 600`, with an empty list and a double space. The figure
   is the one inv. 70 asked for. The wording reads as an alarm on the runs where nothing
   happened, and changing it is a wording decision this TZ withholds.
4. **The repair is proven against a stub, by design** (§7). How often a real archive or
   mirror serves a truncated 200 is unmeasured. The budget line is now what will show
   it, on the next `backtest_bench.yml` dispatch.
5. **H-c2 rebinds `time.sleep` process-wide for the length of one call.** It is restored
   in a `finally`, but anything else sleeping in that window would sleep for zero
   seconds. Nothing in the guard does.

## Commit

Implementation, on `claude/tz-39-transport-outcome-and-budget`, pushed before this report
was written and therefore measured — `396f961f413599d3c9f10d9252119af2e74a2f74`:

```
TZ-39: decide the transport outcome after the last failing step; print the retry budget on every fetch
```

The subject is the TZ's `## Commit Message` verbatim, followed by the `Co-Authored-By`
trailer.

This report's own commit carries the message

```
docs(reports): TZ-39 — transport outcome after the last failing step, retry budget on every pass (TZ-39)
```

Nothing is stated here about its outcome: it has not happened as this section is
written (inv. 54).

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/35** —
`claude/tz-39-transport-outcome-and-budget` → `main`. Not merged. Merging is the Boss's
decision after the Architect's audit.

## CI Execution

`Bench gate` ran on the runner against `396f961` twice, and both runs concluded
**success**:

| Run | Event | Conclusion |
|---|---|---|
| `34657215614` | `push` | **success** |
| `34657291190` | `pull_request` | **success** |

All 19 job steps of both runs are `success` (`gh run view <id> --json jobs`). That
includes job step 9, `verify_bench.py` (gate step 4), and job step 19,
`backtest_guard_bench.py` (gate step 14). The runner's check COUNTS live only in the job
logs, which were not read, so the figures 40 and 373 above are local measurements and
are not offered as runner ones.

`calib.yml` did not run: its `paths` filter names only `bench/exhaustion_calib.py` and
itself. `main.yml` did not run: its allow-list names `main.py` and itself.
`backtest_bench.yml` is dispatch-only and was not dispatched. It is not named by this
TZ, and it needs the archive, which §7 forbids this session to fetch.

## Final Repository State

**NOT IN EFFECT UNTIL MERGED.**

This session leaves the branch `claude/tz-39-transport-outcome-and-budget` at
`396f961f413599d3c9f10d9252119af2e74a2f74`: pushed, green on both hosted runs, and
carrying exactly the two modified files. `bench/backtest_bench.py` and
`bench/backtest_guard_bench.py` on `main` are unchanged until PR #35 is merged.

The working tree was left clean. `git status --porcelain` printed nothing after C4's last
revert, and `__pycache__` was removed after every run. The scratch files (`b_demo.py`,
`c4.py`, the before/after copies of `backtest_bench.py`, and the C4 outputs) are under
`/tmp/tz39/`, outside the repository.

## Fingerprints

Map revision string, as carried in its `## 0. Fingerprint` block:
`**Revision 2026-09-10-a.**`

The seven content anchors of TZ §0, each matched as an exact substring on `origin/main`
at `8c3392f` (`grep -cF`; every anchor occurs twice, once in the map's own anchor table
and once at its site):

| Anchor | Matched substring |
|---|---|
| revision | `**Revision 2026-09-10-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `70. **A transport failure is NOT an absence of data.**` |

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2590 | `86dac370fb4e3e096cb24e23dec1aa1c` |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

All six match what the TZ requires, and the four `## 0` files are identical on the
branch after the edits.

Added by this TZ's gate table, measured **before** the edits and matching it exactly:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4555 | `deac9dd8a53f2047c25c2d6fb24f09b4` |
| `bench/backtest_guard_bench.py` | 1726 | `ce08dd99edebfa90d8fce3dd6b7ba472` |

The same two files **after** the edits, on the pushed branch at `396f961`:

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 4572 | `ce38ef842b60699b9ea34dad4f322a29` |
| `bench/backtest_guard_bench.py` | 1986 | `1580b9a02b7d4453cd3eebd0b25e33ad` |

`bench/verify_bench.py`, named under `## Touches`: 388 lines,
`06036d8c3d39ccec6be21d2158ef3ce1`, unchanged.
