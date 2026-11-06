# TZ-77 — The paper test can answer: the archive's missing day booked from the exchange's own klines, the window run on past thirteen weeks only where they cannot make the verdict, each pick episode's orders recorded

**Canonical filename:** `CryptoTZ/TZ-77-paper-api-window-orders.md`
**Report:** `CryptoReports/TZ-77-paper-api-window-orders-report.md`
**Class:** branch TZ (contract §8) — it authorises two repository files besides its report.
**Branch:** `claude/tz-77-paper-api-window-orders`
**Host:** the VPS, for stage C's selftest, probe and V6; stages A–B run on any clone.
**Model:** Opus — the change is the patch of §10, written and executed by the Architect; the session applies it, proves
its bytes and runs the validation, and V6, the one measurement this TZ rests on that the Architect's session cannot
take, decides whether anything is pushed.
**Trigger:** `EXECUTE TZ-77`, with nothing under it: no credential arrives and the Boss is asked for nothing.
**Previous TZ:** TZ-76, accepted 30.10.2026 and merged at `f3bd75a` (pull request #62); no branch on the remote is
ahead of `main`.
**Issued:** 06.11.2026, by the Architect.
**Written against:** contract v31, map `2026-11-06-c`, and `main` at `c03f428`, read from the repository on 06.11.2026.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-06-c.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-06-c.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this TZ's gate adds:

| Added file | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | version line `**Version 31.**`; a lower version is BLOCKED |
| `vps/paper.py` | 1413 | `dd4bab0209f99e1da430c87042a92b9c` | equal, or A1 stops: §10 is written against these bytes, TZ-76's merged file |
| `vps/selftest.py` | 2627 | `76e814ccbe18551a8f47d6f7eae09669` | equal, or A1 stops: §10 is written against these bytes |
| `vps/units/crypto-paper.service` | 30 | `082a64f8f3a11ca4d4fab6a3974a97e8` | equal, or A1 stops: the memory bound of §3 A rests on its `MemoryMax=128M`, and this TZ does not touch it |

The map itself: 2803 lines, MD5 `c7bbb8d1ced39ae5e525955ad181742e` — reported, not enforced.

---

## 1. What changes, and the evidence for it

**The owner, 06.11.2026, verbatim:** «if you change anything, you must be absolutely certain that it will improve our
copy-trading strategy». The map's row «Hyperliquid's large accounts» applies it at `2026-11-06-c`: a change moves no
rule, no constant and no number the test has booked, and a new capability is relied on only after the record has
measured it. This TZ is that row's decision of 06.11.2026, with the defect its reading had counted wrong.

**(0) The archive's missing day — what decides whether the test can answer at all.** Read by the Architect on
06.11.2026 from `main` at `c03f428` and from `data.binance.vision`:

- Of the four pick episodes closed since 17.10 — INIT, kPEPE and LIT of pick 1, HYPE of pick 2 — **one is booked.**
  INIT, kPEPE and LIT are written unbookable in `analyst/paper/book/`, each naming
  `/daily/klines/<SYM>/1m/<SYM>-1m-2026-10-28.zip`.
- **`data.binance.vision` never published 28.10.2026.** At 10:11 UTC the daily 1 m and 1 d files of `BTCUSDT`, and the
  1 d files of `ETHUSDT` and `HYPEUSDT`, answer 404; 27.10 and 29.10 answer 200; October's monthly 1 m and 1 d files of
  `BTCUSDT` carry 30 of 31 days, 28.10 absent. That day's futures `trades` and `metrics` files answer 200.
- Past TZ-76's seven days the books of 27.10–04.11, written on 05.11 at 00:50 UTC, carry **320 of 784 lines unbookable**
  — the 1 m file of 28.10 for episodes spanning it, the 1 d file of 28.10 for every episode opened from 30.10 — and every
  episode opened up to 29.11 follows, because σ reads the closes of D−32 … D−2 (TZ-64 12.3.3).
- At the picks' pace since 17.10 — 4 closed in 19.5 days, about 0.2 a day — thirteen weeks then book about 11 pick
  episodes and twenty-six about 29, against the verdict's 30 (TZ-64 12.4.2). **The window of (1) alone does not make
  the test readable.**

**Why the exchange's own klines and not the archive's trades.** The `trades` file of 28.10 is whole by trade id — its
first id follows 27.10's last and its last precedes 29.10's first, for `LITUSDT` and `BTCUSDT` — and minutes rebuilt from
a day's trades (first, highest, lowest, last) equalled the published 1 m klines in **7 200 of 7 200 minutes** of 27.10
for `BTCUSDT`, `1000PEPEUSDT`, `HYPEUSDT`, `INITUSDT` and `LITUSDT`, every day close equal. On 29.10 they missed in
**163 of 2 880** minutes (`LITUSDT` 94, `BTCUSDT` 69) and in `LITUSDT`'s close, the archive lacking about 7 % of that
day's trade ids. A source exact on one day and not on the next is no source. *[Architect's decision. Discarded: the
trades rebuild, for that reason, and leaving the lines unbookable — three of the four pick episodes and 317 null lines
lost for a reason the rule does not know.]* `fapi.binance.com/fapi/v1/klines` is the exchange's own series, which the
archive publishes as files: `symbol`, `interval`, `startTime`, `endTime`, `limit` up to 1 500, weight 10 above a
limit of 1 000, each row open time, open, high, low, close in the archive's column order (Binance's documentation, read
06.11.2026). `vps/book.py` reads that endpoint on the VPS every run, `vps/exchange.py` reads the same host from this
recorder's unit, and it answers 451 to the Architect's session — **so V6 measures it against the archive on the VPS,
for every symbol the rebook needs, before anything is pushed.**

**(1) The window.** Thirteen weeks that cannot reach thirty booked pick episodes are run on, to the thirtieth, at most
26 weeks after `follow_from` (17.04.2027 12:51:54 UTC); where thirteen weeks can be readable they stay the test. With
(0), thirty need about 21 weeks at the observed pace.

**(2) The orders.** Read 06.11.2026 from the Architect's session, keyless: `historicalOrders` answers one row per status
an order took — `open` at placement with its attached children, then `triggered`, `filled`, `canceled`,
`reduceOnlyCanceled` and others — 1 588 rows for pick 1's 956 orders back to 18.09.2026, so the latest 2 000 rows reach
about two months; a triggered take-profit's `filled` row carries the trigger time and its `open` row the placement, so
an order's placement is the earliest `order.timestamp` among its rows; every `userFillsByTime` fill names its `oid`.
Both endpoints weigh 20 plus one per 20 rows returned (Hyperliquid's documentation, read 06.11.2026). Pick 1's INIT
entry rested 206 s and LIT's 124 s before their first fill; INIT's and kPEPE's take-profits were attached at entry and
LIT's closing limit was placed 6.6 days before it filled.

**Nothing else moves:** the selection and its constants, the null, the delays, the sizing, the stop, the fee, the
funding rule, `decide()`, the alerts' texts and their rule, and every record already written, which is never reopened.

---

## 2. Text this TZ obeys

- Contract §7 item 2: «**Never edit a bench to make it pass.**» — §10 adds W18, W19 and W20 to `vps/selftest.py` and
  changes none of its existing lines (V7: zero lines removed).
- Contract §7 item 9: «**A program in this repository that a VPS unit runs, and whose output that unit commits, has a
  workflow step's standing on the same terms**» — the recorder's reads of `fapi.binance.com` stand there. V5's and V6's
  reads measure this session's environment, are recorded beside their commands, and produce no product fact.
- Contract §7 item 15: «An implementation session never enables, starts or leaves running a persistent unit, timer or
  service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its report
  proves none is left behind.»
- Contract §8: «The paper-test recorder pushes `analyst/paper/**` on the same path under the same rules (since v30); it
  adds only files `main` does not hold» — `rebook/<day>.jsonl`, `orders/<day>.jsonl` and `orders-readout.json` are such
  files.
- Map inv. 38: «**A second implementation of any rule, threshold or formula is banned in any language and any file.**»
  — the window counts a pick episode as booked by `booked_at()` at `READABLE_AT_S`, which the verdict now reads too; and
  its (2), «A file once written is never reopened» — a rebook is a separate file joined by key, where inv. 38 (2) puts
  an outcome.
- Map inv. 70: «**A transport failure is NOT an absence of data.**» — an API request that never completed is Transport
  and the day waits; only an answer with no klines, or the exchange's own HTTP 400, is Absent.
- Map inv. 22: «**A check that passes with no data is forbidden.**» — V6 fails on zero symbols.

---

## 3. The rule as this TZ amends it — registered

Each item names what derived it. §10 implements this section and nothing else.

### A. The archive's missing day (amends TZ-64 12.3 and TZ-76)

**A1.** `Inputs.minutes` and `Inputs.close_on`: a klines file the archive answers 404 for, dated more than
`ABSENT_AFTER_DAYS` back — TZ-76's `Absent` — is read from
`https://fapi.binance.com/fapi/v1/klines?symbol=<SYM>&interval=<1m|1d>&startTime=<day start>&endTime=<day end − 1 ms>&limit=1500`,
the rows opening inside the day, in the archive's column order. An answer with no klines, or HTTP 400, is `Absent`
named `fapi <SYM> <interval> <date>: …`; any other failure, an unreadable row included, is `Transport` and the pass
waits. A nearer 404 stays `NotReady`, unchanged. *Derived: §1 (0) and V6.* The service passes the fallback; an `Inputs`
built without one behaves exactly as before.

**A2.** Every symbol-day so read is kept in `/var/lib/cryptopaper/api-days.json`; a book line whose inputs include one
names them, `"api": ["1d 2026-10-28", …]`, and the verdict counts such lines, `api`. The request is one per
symbol-day: 1 440 minutes, a few dozen kilobytes, nothing held past its pass — the memory bound of TZ-65 stands.

**A3. The rebook.** A book line whose `unbookable` names an archive klines path (`/daily/klines/…`) was written before
A1 existed. Each written book day holding such lines has them booked again, once, by `book_episode()` itself, one
symbol at a time, into `analyst/paper/rebook/<day>.jsonl` — a head `{"k": "day", "date", "rebooked", "booked",
"unbookable"}` and each line beside `"rebook": true`. `book_lines()` — the reader of the funding and of the verdict —
returns a day's book with each such line replaced by its rebook line; the funding of a day waits while one awaits; the
verdict counts `rebooked`. A line A1 itself writes unbookable names `fapi …` and is final. The rebook is its own step of
the hourly pass, before the booking, so the booking's wait never holds it. *Derived: inv. 38 (2).*

**A4.** The open alert's σ reads the same `Inputs`, so an open alert from 30.10 to 29.11 prints its stop and size again
instead of «стоп и объём не рассчитаны»; its text and its rule do not change.

### B. The window (amends TZ-64 12.2 and 12.4.2, TZ-75 B1)

**B1.** When the end as it stands is reached and every account was polled `DAY_SETTLE_S` past it, the decision: at
thirteen weeks the window **closes** whenever its pick episodes — those in the written episode files, those closed since
and those open — less the pick lines written unbookable for good (a line awaiting a rebook is not counted), number
`EPISODES_MIN` (30) or more; the window is then `selection.json`'s own and everything after is TZ-64's. Otherwise it
**runs on**, its end the cap, `follow_from` + 182 days, and the owner is told once:

```
Бумажный тест копирования: сделок китов за 13 недель — {n} из 30 нужных, окно продлено до 30-й, но не дольше {date}.
```

*Derived: the verdict of thirteen weeks is readable only at 30 booked pick episodes, and they can never exceed the
number B1 counts, so wherever thirteen weeks can be readable they are the test. The one case left — counted 30 or more,
booked fewer — is a thirteen-week test unreadable exactly as the original would be.*

**B2.** While it runs on, each hourly pass counts the pick episodes booked at `READABLE_AT_S` (1 800 s) in the written
book, rebooks applied; at `EPISODES_MIN` the end is fixed at the first instant of `follow_from`'s daily grid after that
pass — thirteen weeks and whole days — the cap at the latest, and the owner is told once:

```
Бумажный тест копирования: учтённых сделок китов — {n} из 30 нужных, окно закроется {date}.
```

*Derived: a count read from immutable book lines only grows, so a window closing on it is readable; an end fixed ahead
of now keeps every fill before it followed as at thirteen weeks, and the cut there is TZ-64's own. [Architect's
decision. Discarded: closing at the thirtieth close itself, which a line booked unbookable afterwards would leave short;
and a weekly grid, which runs on up to a week past the thirtieth.]*

**B3.** A fill at or after the end as it stands is neither applied nor passed — the account's `last_ms` stays before it —
so a window that runs on reads it again and loses none. Until B1 decides, alerts stop at the end as TZ-64's do; once it
runs on, they follow TZ-64's own age rule.

**B4.** Every step reads the window as it stands, `window_view()`: the following, the alerts, the cut, the day files,
the books, the verdict and the rescan, whose own rule is unchanged (TZ-75 B1) and which, once the window runs on, may
run again while picks are short of three and 28 days remain. The decision is kept in the state and written into
`verdict.json` as `window`. A window that ran on closes with:

```
Бумажный тест копирования: окно закрыто {date}, оповещения остановлены. Итог — после публикации данных Binance.
```

A thirteen-week close sends TZ-64's own notice. Every date is `DD.MM.YYYY` in Tbilisi.

### C. The orders (new; deciding nothing)

**C1.** Each fill keeps its `oid`, `None` when the answer names none; each episode names the orders of its opening and
closing fills, `oid_open` and `oid_close`.

**C2.** `analyst/paper/orders/<day>.jsonl`, once per day of the window, after the day ended `DAY_SETTLE_S` ago and its
episode file is written: a head — the rows kept and, per pick, the rows its answer held and `complete`, false when the
answer held `ORDERS_COMPLETE` (2 000) rows and its oldest falls inside the day; an `ep` line per pick episode of that
day's file with both orders — for an episode written before this TZ, read from the account's fills of that coin at that
millisecond; and every row `historicalOrders` answered for a pick whose `statusTimestamp` falls in the day, on a coin
the frozen Binance list copies, as answered, beside `"k": "row"` and the pick. One read per pick per pass; Transport ends
the step and the day waits.

**C3.** Beside every closed pick episode's book line, `x`: the copy entered at each delay and left at the pick's own exit
minute — `book_delay()` on the episode with its close moved back by that delay; `None` where the copy would enter after
the exit. Never for a null account's episode or a cut one.

**C4.** `analyst/paper/orders-readout.json`, once, after `verdict.json` and the window's last orders file, over the picks'
closed episodes inside their spans: the entries, and the exits, whose order was placed at least `ANNOUNCED_S` (30 s, the
pick poll) before the fill, of those whose order is recorded, with the p50 and p95 of that lead; the resting orders able
to open a position — an `open` row, not reduce-only, placed inside the pick's span — and how many opened no episode;
and, for every delay, over the episodes whose exit rested, the sum over capital of gross less fees of `x` and of the
delayed copy, `src` and `stop`. *Derived: §1 (2).* Its failure is logged and touches no other record.

### D. The probe

**D1.** The klines steps read two days back, a day the archive has published in normal operation — TZ-75's V5 failed on
«yesterday» = 28.10.

**D2.** Two steps are added: `api` — `BTCUSDT`'s minutes and close of that day from the API against the archive, one
line of counts; and `orders` — the probe account's `historicalOrders` row count.

---

## 4. Scope

### Files to Create
None in the repository but the report.

### Files to Modify
- `vps/paper.py` — §10.
- `vps/selftest.py` — §10: W18, W19 and W20 added, and their three calls at the end of section W; no existing line
  changes.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
Transient units started from the branch's clone for V5's probe and V6's comparison, each gone before the report. No
unit, timer or file under `/etc` or `/var/lib/cryptopaper` is created, changed or restarted: **the running paper test is
not touched**, and A–C take effect when the deployer installs the merge.

### Not touched
`index.html`, `main.py`, every unit and the manifest, `bench.yml`, `analyst/**`, the map, the contracts.

---

## 5. Stages

### Stage A — readings, no writes
- **A0.** Contract §4a steps 1–6; the gate of §0, every anchor cut from the map's own table.
- **A1.** The four added files of §0 at their lines and MD5; any difference stops the TZ, BLOCKED, naming the file.
- **A2.** On the VPS, the baseline from `main`: `python3 vps/selftest.py` prints `selftest: sections 27 checks 592
  failed 0 empty 0` and `section W: checks 134 failed 0`. *Measured by the Architect on `c03f428`, the figures TZ-76's V3
  read on the VPS.* A different baseline is recorded per section and the TZ goes on: stage C compares against what A2
  read.
- **A3.** `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service`, kept for V9.

### Stage B — the code, on the branch
- **B1.** Branch `claude/tz-77-paper-api-window-orders` from `origin/main`. Extract §10's patch with the one command

  ```sh
  awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-77-paper-api-window-orders.md > /tmp/tz77.patch
  ```

  and record its lines and MD5 — 1195 and `1cc2ffdb1ae1f90ef6fa6120a645305d` as written; an upload that strips the
  patch's blank context lines changes the hash and not the result, which B2 decides.
- **B2.** `git apply /tmp/tz77.patch`. **Required:** `vps/paper.py` 1785 lines, MD5
  `2d814305c3e2883c79dbcf1c6fa14068`; `vps/selftest.py` 3063 lines, MD5 `505efb7dc01c40dd09c9c9008e49345b`. Any other
  result is BLOCKED: the patch did not arrive as written, and no hand edit replaces it.
- **B3.** Commit with §7's implementation message, **locally, before stage C**, so that V4's restore returns the changed
  file. Not pushed yet.

### Stage C — validation, on the VPS, on the committed branch
§6, in full. **V6 is this TZ's gate:** if it fails, nothing is pushed, the status is BLOCKED, and the report carries
every line V6 printed.

### Stage D — push, pull request, report
Push; a pull request to `main` titled `TZ-77: paper — the archive's missing day from the API, the window run on to the
thirtieth pick episode, the picks' orders recorded`, its body naming this TZ, or the §8 fallback. Then the report.

---

## 6. Validation

| # | Check | Required |
|---|---|---|
| V1 | `python3 -m py_compile vps/paper.py vps/selftest.py` | exit 0 |
| V2 | B2's two files | the lines and MD5s of B2 |
| V3 | `python3 vps/selftest.py` on the branch, on the VPS | `selftest: sections 27 checks 643 failed 0 empty 0`; `section W: checks 185 failed 0`; **every other section's count equal to A2's**. *Measured by the Architect on the patched tree, 06.11.2026: W grows by exactly 51 — 21 in W18, 14 in W19, 16 in W20 — and the 458 checks outside W do not move.* If A2 read another baseline, A2's total + 51 and A2's W + 51 |
| V4 | Negative control: in the working tree replace `    if seen - final >= EPISODES_MIN:` with `    if seen - final > EPISODES_MIN:` in `vps/paper.py`; run the selftest; restore with `git checkout -- vps/paper.py` | exit 1 with exactly one `FAIL` line, `FAIL section W: thirteen weeks that can still make the verdict: the window closes at them, as the selection has it`, and `selftest: sections 27 checks 643 failed 1 empty 0`; then `git status --porcelain` prints nothing. *Measured by the Architect, 06.11.2026* |
| V5 | `paper.py --probe` from the branch's clone as a transient unit: `systemd-run --wait --pipe --collect -p MemoryMax=128M -p Nice=5 /usr/bin/python3 <clone>/vps/paper.py --probe` | exit 0; ten step lines — `leaderboard`, `portfolio`, `exchange`, `leverage`, `fills`, `klines_1m`, `klines_1d`, `funding`, `api`, `orders` — none `failed (…)`; the `api` line `api BTCUSDT <date> archive=1440 api=1440 equal=1440 close=equal`; the `orders` line `rows=<n>` with n above 0; then `peak_rss_kib`, reported |
| V6 | **The API against the archive, for every symbol the rebook needs.** §9's script, extracted with the one command `awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-77-paper-api-window-orders.md > /tmp/tz77-v6.py` — 20 lines, MD5 `a0b32dbad9666123cfaeca2bc66cbff6` as written — and run from the branch's clone as a transient unit: `systemd-run --wait --pipe --collect -p MemoryMax=128M -p WorkingDirectory=<clone> /usr/bin/python3 /tmp/tz77-v6.py` | exit 0; last line `v6: symbols N differing 0` with N at least **54** — the symbols of every book line on `main` awaiting a rebook at `c03f428`, more if the recorder has booked days since; each symbol's line `archive=a api=a equal=a close=equal`, then its 28.10 rows and close from the API, recorded. **Any difference, any failure, or N = 0: BLOCKED, nothing pushed.** *The shape is set by the Architect, whose session the API refuses with 451; the counts are the Executor's to read* |
| V7 | `git diff --numstat origin/main...HEAD` | exactly two lines, tab-separated: `416`, `44`, `vps/paper.py` and `436`, `0`, `vps/selftest.py` |
| V8 | `systemctl list-units --all 'run-*'` after V5–V6 | none of the session's transient units is left |
| V9 | `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service` after the session | equal to A3 — the live test was not restarted |
| V10 | `bench.yml` | `index.html` and `main.py` are untouched, so the standing checks do not apply; report which workflows ran on the branch, from the runner where the session can, and that `vps/**` is outside the hosted gate |

**No regression:** every existing check of `vps/selftest.py` is unchanged and green (V3, and V7's zero removed lines) —
W14's flow, W15's booking memory, W16's rescan and W17's spans among them — and a window whose thirteen weeks can be
readable is the selection's own (W19's second check, which V4 turns red).

---

## 7. Commit Message

Implementation: `TZ-77: vps — the paper test books the archive's missing day from the exchange's own klines, runs its window on past thirteen weeks only when they cannot make the verdict, and records the picks' orders`

Report: `TZ-77: report — the paper test's missing day, window and orders`

---

## 8. The report

Contract §10 in full. Beside it: B1's command and the patch's lines and MD5; B2's lines and MD5s; A2's and V3's
per-section counts side by side; V4's `FAIL` line verbatim; V5's eleven lines and its command; V6's command and every
line it printed; A3's and V9's readings. The map's row «Hyperliquid's large accounts» is the Architect's to update after
the audit, not this TZ's.

---

## 9. The comparison script (V6)

Run from the clone's root, which holds `vps/` and `analyst/paper/book/`. It writes nothing.

```python
import glob, json, sys, time
sys.path.insert(0, "vps")
import paper
syms = sorted({b["symbol"] for f in glob.glob("analyst/paper/book/*.jsonl") for b in map(json.loads, open(f))
               if b.get("k") == "book" and paper.awaits_rebook(b)})
print("targets", len(syms))
bad = 0
for s in syms:
    try:
        line = paper.api_against_archive(s, "2026-10-27")
        m, d = paper.fapi_klines(s, "1m", "2026-10-28"), paper.fapi_klines(s, "1d", "2026-10-28")
        print(line, "| 2026-10-28 api=%d close=%s" % (len(m), d[0][4]))
        f = dict(x.split("=") for x in line.split()[2:])
        bad += f["archive"] != f["equal"] or f["close"] != "equal"
    except Exception as exc:
        bad += 1
        print(s, "failed (%s %s)" % (exc.__class__.__name__, exc))
    time.sleep(1)
print("v6: symbols %d differing %d" % (len(syms), bad))
sys.exit(1 if bad or not syms else 0)
```

---

## 10. The patch

Against `main` at `c03f428`: `vps/paper.py` 1413 → 1785 lines, `vps/selftest.py` 2627 → 3063.

```diff
diff --git a/vps/paper.py b/vps/paper.py
index d3d6016..895a3b9 100644
--- a/vps/paper.py
+++ b/vps/paper.py
@@ -2,7 +2,8 @@
 """The copy-trading paper test (TZ-64, TZ-65; map section 10, row \u00abHyperliquid's large accounts\u00bb):
 Hyperliquid accounts selected once by their twelve-month record, followed in real time,
 every copied episode booked on Binance USD-M prices at four delays, and the verdict
-read at week 13 against random eligible accounts copied the same way.
+read at week 13 against random eligible accounts copied the same way -- or, when thirteen
+weeks cannot make it readable, at the thirtieth booked pick episode, by week 26 (TZ-77).
 
     paper.py [--state-dir <dir>] [--tree <dir>]      the service
     paper.py --probe                                  one read of every interface; counts only
@@ -44,6 +45,7 @@ import exchange  # noqa: E402
 INFO_URL = "https://api.hyperliquid.xyz/info"
 LEADERBOARD_URL = "https://stats-data.hyperliquid.xyz/Mainnet/leaderboard"
 VISION = "https://data.binance.vision/data/futures/um"
+FAPI_KLINES = "https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=%s&startTime=%d&endTime=%d&limit=1500"
 
 # --- The rule, registered by TZ-64 before any data: moved only by a TZ, never after a reading.
 POOL_VOLUME_MIN = 200e6       # all-time volume on the leaderboard, USD
@@ -67,6 +69,9 @@ ALERT_MAX_AGE_S = 600
 RESCAN_FIRST_DAYS = 14        # TZ-75 B: the rule re-applied two weeks after follow_from,
 RESCAN_EVERY_DAYS = 28        # then every four weeks while picks are short of TOP_K
 RESCAN_MIN_LEFT_DAYS = 28     # and only while at least four weeks of the window remain
+RUN_ON_MAX_DAYS = 182         # TZ-77 (1): past thirteen weeks the window runs on only to the verdict's thirtieth booked
+                              # pick episode, and never past 26 weeks after follow_from
+READABLE_AT_S = 1800          # the delay whose booked pick episodes make the verdict readable (TZ-64 12.4.2)
 PROBE_ACCOUNT = "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1"   # the reading's first account
 
 # --- Operation.
@@ -74,7 +79,7 @@ WEIGHT_PER_MIN = 600          # half the info API's documented 1 200 per IP per
                               # Architect's workspace met runs of 429 answers on 16.10.2026
 INFO_WEIGHT = 20              # documented weight of portfolio and userFillsByTime
 FILLS_PAGE = 2000             # documented maximum fills per userFillsByTime answer
-FILL_KEYS = ("coin", "px", "sz", "side", "time", "startPosition", "tid")   # all a fill is read for
+FILL_KEYS = ("coin", "px", "sz", "side", "time", "startPosition", "tid", "oid")   # all a fill is read for; oid TZ-77
 PICK_POLL_S = 30
 NULL_POLL_S = 600
 DAY_SETTLE_S = 600            # a day is written once every account was polled this long after it ended
@@ -82,6 +87,9 @@ ABSENT_AFTER_DAYS = 7         # a 404 for a file dated further back is an absenc
 WORK_EVERY_S = 3600           # booking, funding and the verdict are attempted hourly; a failed rescan resumes as often
 RESCAN_WEIGHT_PER_MIN = 300   # a rescan's share of WEIGHT_PER_MIN; the service holds the rest while one runs
 PUBLISH_EVERY_S = 300
+REBOOK_PREFIX = "/daily/klines/"   # TZ-77 (0): an archive file named in a book line written before the API fallback
+ORDERS_COMPLETE = 2000        # TZ-77 (2): historicalOrders answers its latest 2 000 rows; fewer is the whole record
+ANNOUNCED_S = PICK_POLL_S     # TZ-77 (2): an order resting this long before its fill would reach an order poll first
 TRANSPORT_MAX = 30            # consecutive transport failures on one selection step
 TRANSPORT_WAIT_S = 60
 LOOP_S = 5
@@ -122,6 +130,10 @@ N_VERDICT = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u044
              "\u0445\u0438\u0442\u0435\u043a\u0442\u043e\u0440\u0430.")
 N_ADDED = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442: \u043d\u043e\u0432\u044b\u0439 \u043a\u0438\u0442 {num} \U0001f40b\u2022 {addr} \u2014 \u043f\u0440\u043e\u0448\u0451\u043b \u0442\u043e \u0436\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u0431\u043e\u0440\u0430 \u043d\u0430 {date}, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u0434\u043e {end}."
 N_RESCAN_NONE = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 \u043f\u043e\u0438\u0441\u043a \u043a\u0438\u0442\u043e\u0432 {date}: \u043f\u0440\u0430\u0432\u0438\u043b\u043e 12 \u043c\u0435\u0441\u044f\u0446\u0435\u0432 \u043f\u0440\u043e\u0448\u043b\u0438 {r12} \u0438\u0437 {eligible} \u0441\u0447\u0435\u0442\u043e\u0432, \u043d\u043e\u0432\u044b\u0445 \u043a\u043e\u043f\u0438\u0440\u0443\u0435\u043c\u044b\u0445 \u043d\u0435\u0442."
+# --- TZ-77 (1): the window that runs on past thirteen weeks.
+N_RUN_ON = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0441\u0434\u0435\u043b\u043e\u043a \u043a\u0438\u0442\u043e\u0432 \u0437\u0430 13 \u043d\u0435\u0434\u0435\u043b\u044c \u2014 {n} \u0438\u0437 30 \u043d\u0443\u0436\u043d\u044b\u0445, \u043e\u043a\u043d\u043e \u043f\u0440\u043e\u0434\u043b\u0435\u043d\u043e \u0434\u043e 30-\u0439, \u043d\u043e \u043d\u0435 \u0434\u043e\u043b\u044c\u0448\u0435 {date}."
+N_END_SET = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0443\u0447\u0442\u0451\u043d\u043d\u044b\u0445 \u0441\u0434\u0435\u043b\u043e\u043a \u043a\u0438\u0442\u043e\u0432 \u2014 {n} \u0438\u0437 30 \u043d\u0443\u0436\u043d\u044b\u0445, \u043e\u043a\u043d\u043e \u0437\u0430\u043a\u0440\u043e\u0435\u0442\u0441\u044f {date}."
+N_CLOSED_RUN_ON = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u043e\u043a\u043d\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u043e {date}, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u044b. \u0418\u0442\u043e\u0433 \u2014 \u043f\u043e\u0441\u043b\u0435 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 \u0434\u0430\u043d\u043d\u044b\u0445 Binance."
 MINUTES = "\u043c\u0438\u043d"
 HOURS = "\u0447"
 
@@ -251,7 +263,7 @@ class Limiter:
 def info(body, limiter):
     limiter.spend(INFO_WEIGHT)
     doc = http_post(INFO_URL, body)
-    if body.get("type") == "userFillsByTime" and isinstance(doc, list):
+    if body.get("type") in ("userFillsByTime", "historicalOrders") and isinstance(doc, list):
         limiter.spend(len(doc) // 20)    # documented: one more per 20 items returned
     return doc
 
@@ -278,7 +290,7 @@ def iter_fills(addr, start_ms, limiter, end_ms=None):
             if ft > t:
                 t, tids_at_t = ft, set()
             tids_at_t.add(f["tid"])
-            yield {k: f[k] for k in FILL_KEYS}
+            yield {k: f.get(k) if k == "oid" else f[k] for k in FILL_KEYS}   # an answer naming no order: oid None
         if len(page) < FILLS_PAGE:
             return
         if t == asked:
@@ -459,7 +471,8 @@ def apply_fill(coins, fill, symbol):
     before the fill is the fill's own startPosition, so a coin first seen with a position open has
     no episode until it is flat. Returns the events in order: ("lost", ep) when the episode held
     disagrees with startPosition, ("close", ep) when the fill flattens or flips it, ("open", ep)
-    when the fill opens from flat or by the flip."""
+    when the fill opens from flat or by the flip. Each episode names the order of its opening and of
+    its closing fill (TZ-77 (2)), None when the fill names none."""
     coin = fill["coin"]
     start = Decimal(fill["startPosition"])
     size = Decimal(fill["sz"])
@@ -470,12 +483,13 @@ def apply_fill(coins, fill, symbol):
         events.append(("lost", ep))
         ep = None
     if ep is not None and sign(after) != ep["side"]:
-        events.append(("close", dict(ep, t_close=t, px_close=px, n=ep["n"] + 1)))
+        events.append(("close", dict(ep, t_close=t, px_close=px, n=ep["n"] + 1, oid_close=fill.get("oid"))))
         ep = None
     elif ep is not None:
         ep = dict(ep, n=ep["n"] + 1)
     if ep is None and after != 0 and sign(start) != sign(after):
-        ep = {"coin": coin, "symbol": symbol, "side": sign(after), "t_open": t, "px_open": px, "n": 1}
+        ep = {"coin": coin, "symbol": symbol, "side": sign(after), "t_open": t, "px_open": px, "n": 1,
+              "oid_open": fill.get("oid")}
         events.append(("open", ep))
     coins[coin] = ep
     return events
@@ -573,6 +587,36 @@ def vision_rows(path):
     return rows[1:] if rows and not rows[0][0].strip().isdigit() else rows
 
 
+def fapi_klines(sym, interval, date):
+    """TZ-77 (0): sym's klines at interval opening inside UTC day date from the exchange's own API, in the
+    archive's column order -- for a day data.binance.vision never published. Absent when the exchange has
+    none or refuses the request itself (HTTP 400); Transport otherwise (inv. 70)."""
+    start = day_start(date)
+    try:
+        with urllib.request.urlopen(FAPI_KLINES % (sym, interval, start, start + DAY_MS - 1),
+                                    timeout=common.HTTP_TIMEOUT_S) as resp:
+            doc = json.loads(resp.read())
+    except urllib.error.HTTPError as exc:
+        if exc.code == 400:
+            raise Absent("fapi %s %s %s: HTTP 400" % (sym, interval, date)) from None
+        raise Transport("HTTP %d" % exc.code) from None
+    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
+        raise Transport(exc.__class__.__name__) from None
+    except ValueError:
+        raise Transport("unparseable") from None
+    if not isinstance(doc, list):
+        raise Transport("klines: not a list")
+    try:
+        rows = [r for r in doc if start <= int(r[0]) < start + DAY_MS]
+        for r in rows:
+            float(r[1]), float(r[2]), float(r[3]), float(r[4])
+    except (TypeError, ValueError, IndexError, KeyError):
+        raise Transport("klines: unreadable") from None
+    if not rows:
+        raise Absent("fapi %s %s %s: no klines" % (sym, interval, date))
+    return rows
+
+
 class Rows:
     """The (open, high, low, close) of consecutive minutes, four doubles a minute in one array: a
     symbol-day is kept in 63 KiB with its times, against 375 KiB as a list of tuples (12.3.6)."""
@@ -592,16 +636,38 @@ class Rows:
 class Inputs:
     """data.binance.vision inputs of one pass: 1m klines of one symbol at a time by day, daily
     closes kept on disk, funding rates by symbol and month. A 404 dated more than ABSENT_AFTER_DAYS
-    before today is Absent; nearer is NotReady."""
+    before today is Absent; nearer is NotReady. With a fallback (TZ-77 (0)) an Absent day of klines
+    is read from the exchange's own API instead, and every symbol-day so read is kept on disk, so a
+    book line names the days it took from there (`used`, which the caller clears)."""
 
-    def __init__(self, state_dir, today, rows=vision_rows):
+    def __init__(self, state_dir, today, rows=vision_rows, fallback=None):
         self.today, self.rows, self.klines, self.kl_sym, self.rates_by = today, rows, {}, None, {}
+        self.fallback, self.used = fallback, set()
         self.closes_path = os.path.join(state_dir, "closes.json")
         try:
             with open(self.closes_path, encoding="utf-8") as fh:
                 self.closes = json.load(fh)
         except (OSError, ValueError):
             self.closes = {}
+        self.api_path = os.path.join(state_dir, "api-days.json")
+        try:
+            with open(self.api_path, encoding="utf-8") as fh:
+                self.api = set(json.load(fh))
+        except (OSError, ValueError):
+            self.api = set()
+
+    def from_api(self, sym, interval, date):
+        """The fallback's rows for one symbol-day, the day remembered on disk."""
+        rows = self.fallback(sym, interval, date)
+        key = "%s %s %s" % (sym, interval, date)
+        if key not in self.api:
+            self.api.add(key)
+            common.atomic_write(self.api_path, sorted(self.api), mode=0o640)
+        return rows
+
+    def mark(self, sym, interval, date):
+        if "%s %s %s" % (sym, interval, date) in self.api:
+            self.used.add("%s %s" % (interval, date))
 
     def fetch(self, path, ref_date):
         try:
@@ -617,11 +683,17 @@ class Inputs:
             self.klines, self.kl_sym = {}, sym
         if (sym, date) not in self.klines:
             start = day_start(date)
-            rows = sorted(x for x in ((int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in
-                                      self.fetch("/daily/klines/%s/1m/%s-1m-%s.zip" % (sym, sym, date), date))
+            try:
+                got = self.fetch("/daily/klines/%s/1m/%s-1m-%s.zip" % (sym, sym, date), date)
+            except Absent:
+                if self.fallback is None:
+                    raise
+                got = self.from_api(sym, "1m", date)
+            rows = sorted(x for x in ((int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in got)
                           if start <= x[0] < start + DAY_MS)
             self.klines[(sym, date)] = (array.array("q", [x[0] for x in rows]),
                                         array.array("d", [v for x in rows for v in x[1:]]))
+        self.mark(sym, "1m", date)
         return self.klines[(sym, date)]
 
     def kl(self, sym, first, last):
@@ -639,9 +711,15 @@ class Inputs:
     def close_on(self, sym, date):
         have = self.closes.setdefault(sym, {})
         if date not in have:
-            rows = self.fetch("/daily/klines/%s/1d/%s-1d-%s.zip" % (sym, sym, date), date)
+            try:
+                rows = self.fetch("/daily/klines/%s/1d/%s-1d-%s.zip" % (sym, sym, date), date)
+            except Absent:
+                if self.fallback is None:
+                    raise
+                rows = self.from_api(sym, "1d", date)
             have[date] = float(rows[0][4])
             common.atomic_write(self.closes_path, self.closes, mode=0o640)
+        self.mark(sym, "1d", date)
         return have[date]
 
     def rates(self, sym, month):
@@ -662,10 +740,13 @@ def last_day(ep, window_end):
 
 def book_episode(ep, inputs, rule, window_end):
     """The book line of one episode: sigma_for, the stop distance INV_FLOOR_SD sigma, and every
-    delay; or an unbookable line."""
+    delay; or an unbookable line. A pick's episode that closed also books, beside the verdict and
+    deciding nothing, the copy entered at each delay and left at the pick's own exit, `x` (TZ-77 (2));
+    a line whose inputs came from the exchange's API names those days, `api` (TZ-77 (0))."""
     line = {"k": "book", "a": ep["a"], "coin": ep["coin"], "symbol": ep["symbol"], "side": ep["side"],
             "t_open": ep["t_open"]}
     first = utc_date(ep["t_open"])
+    inputs.used = set()
     try:
         sigma = sigma_for(inputs, ep["symbol"], ep["t_open"])
         dist = rule["inv_floor_sd"] * sigma
@@ -675,8 +756,14 @@ def book_episode(ep, inputs, rule, window_end):
         line.update(sigma_d=sigma, dist=dist, d={
             str(d): book_delay(ep, d, dist, kl, rule["capital_usdt"], rule["risk_pct"] / 100, rule["fee_taker"],
                                window_end) for d in DELAYS_S})
+        if ep.get("role") == "pick" and not ep.get("cut"):
+            line["x"] = {str(d): book_delay(dict(ep, t_close=ep["t_close"] - d * 1000), d, dist, kl,
+                                            rule["capital_usdt"], rule["risk_pct"] / 100, rule["fee_taker"], window_end)
+                         for d in DELAYS_S}
     except Absent as exc:
         line["unbookable"] = str(exc)
+    if inputs.used:
+        line["api"] = sorted(inputs.used)
     return line
 
 
@@ -703,6 +790,27 @@ def funding_line(book, inputs):
     return line
 
 
+def booked_at(b, d):
+    """A book line's copy at delay d, or None: unbookable, or entered after its exit."""
+    return b["d"][str(d)] if "d" in b else None
+
+
+def awaits_rebook(b):
+    """TZ-77 (0): a line written unbookable for an archive file before the API fallback, not yet booked again."""
+    return str(b.get("unbookable", "")).startswith(REBOOK_PREFIX)
+
+
+def book_lines(root, day):
+    """The book lines of one day in the book file's order, each replaced by its line in rebook/<day>.jsonl
+    where that file holds one (TZ-77 (0))."""
+    lines = [b for b in read_jsonl(os.path.join(root, "book", day + ".jsonl")) if b["k"] == "book"]
+    path = os.path.join(root, "rebook", day + ".jsonl")
+    if os.path.exists(path):
+        again = {(r["a"], r["coin"], r["t_open"]): r for r in read_jsonl(path) if r["k"] == "book"}
+        lines = [again.get((b["a"], b["coin"], b["t_open"]), b) for b in lines]
+    return lines
+
+
 # --- the verdict -----------------------------------------------------------------
 def decide(picks, null, results, pick_episodes):
     """results[a][d][v]: net over capital. TOP is the picks' mean; the null is every k-subset of the
@@ -1056,8 +1164,8 @@ def new_state(sel):
                                         "last_tids": [], "polled_ms": 0, "due_ms": 0, "coins": {}, "fills": {},
                                         "lost": {}, "failing": False}
     return {"v": 1, "accounts": accounts, "closed": [], "cut": False, "written": {"episodes": None, "book": None,
-            "funding": None}, "verdict": False, "pending": [], "next_work_ms": 0, "next_publish_ms": 0,
-            "closed_notice": False}
+            "funding": None, "rebook": None, "orders": None}, "verdict": False, "pending": [], "next_work_ms": 0,
+            "next_publish_ms": 0, "closed_notice": False}
 
 
 def poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for):
@@ -1099,9 +1207,10 @@ def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for, leverage_for=
                     common.write_outbox("alert", alert_open(ep, acct["rank"], rule, sigma, leverage_for(f["coin"])))
                 else:
                     common.write_outbox("alert", alert_close(ep, acct["rank"], rule))
-    if fills:
-        acct["last_ms"] = max(acct["last_ms"], max(int(f["time"]) for f in fills))
-        acct["last_tids"] = [f["tid"] for f in fills if int(f["time"]) == acct["last_ms"]]
+    kept = [f for f in fills if int(f["time"]) < window_end]   # TZ-77 (1): a fill past the end as it stands stays
+    if kept:                                                     # unread, so a window that runs on applies it
+        acct["last_ms"] = max(acct["last_ms"], max(int(f["time"]) for f in kept))
+        acct["last_tids"] = [f["tid"] for f in kept if int(f["time"]) == acct["last_ms"]]
     acct["polled_ms"] = now
 
 
@@ -1177,14 +1286,44 @@ def produce_books(state, state_dir, sel, rule, inputs):
         state["written"]["book"] = day
 
 
+def produce_rebooks(state, state_dir, sel, rule, inputs):
+    """TZ-77 (0): every written book day holding episodes unbookable for an archive file -- written before the API
+    fallback -- has those episodes booked again, once, one symbol at a time, into rebook/<day>.jsonl; a day without
+    them writes nothing. NotReady ends the pass and the day is booked again whole at the next."""
+    first, window_end = utc_date(sel["follow_from_ms"]), sel["window_end_ms"]
+    root = os.path.join(state_dir, "records", RECORD_DIR)
+    while True:
+        day = next_date(state["written"]["rebook"], first)
+        if state["written"]["book"] is None or day > state["written"]["book"]:
+            return
+        targets = [b for b in read_jsonl(os.path.join(root, "book", day + ".jsonl")) if b["k"] == "book"
+                   and awaits_rebook(b)]
+        if targets:
+            eps = {(e["a"], e["coin"], e["t_open"]): e for e in read_jsonl(os.path.join(root, "episodes", day + ".jsonl"))
+                   if e["k"] == "ep"}
+            lines = [None] * len(targets)
+            try:
+                for i in sorted(range(len(targets)), key=lambda i: (targets[i]["symbol"], i)):
+                    t = targets[i]
+                    lines[i] = dict(book_episode(eps[(t["a"], t["coin"], t["t_open"])], inputs, rule, window_end),
+                                    rebook=True)
+            finally:
+                inputs.drop_minutes()
+            head = {"k": "day", "date": day, "rebooked": len(lines), "booked": sum(1 for x in lines if "d" in x),
+                    "unbookable": sum(1 for x in lines if "unbookable" in x)}
+            write_record(state, state_dir, "rebook/%s.jsonl" % day, [head] + lines)
+        state["written"]["rebook"] = day
+
+
 def produce_funding(state, state_dir, sel, inputs):
     first = utc_date(sel["follow_from_ms"])
     while True:
         day = next_date(state["written"]["funding"], first)
         if state["written"]["book"] is None or day > state["written"]["book"]:
             return
-        books = [b for b in read_jsonl(os.path.join(state_dir, "records", RECORD_DIR, "book", day + ".jsonl"))
-                 if b["k"] == "book"]
+        books = book_lines(os.path.join(state_dir, "records", RECORD_DIR), day)
+        if any(awaits_rebook(b) for b in books):
+            return                               # TZ-77 (0): the day's rebook comes first
         lines = [funding_line(b, inputs) for b in books]
         head = {"k": "day", "date": day, "lines": len(lines), "absent": sum(1 for x in lines if x["absent"])}
         write_record(state, state_dir, "funding/%s.jsonl" % day, [head] + lines)
@@ -1203,13 +1342,14 @@ def produce_verdict(state, state_dir, sel, rule):
     results = {a: {d: {"src": 0.0, "stop": 0.0} for d in DELAYS_S} for a in picks}
     spanned = {a: {j: {d: {"src": 0.0, "stop": 0.0} for d in DELAYS_S} for j in spans} for a in null}
     booked = {d: {"pick": 0, "null": 0} for d in DELAYS_S}
-    lags, unbookable, absent = [], 0, 0
+    lags, unbookable, absent, rebooked, api = [], 0, 0, 0, 0
     for day in days:
         for e in read_jsonl(os.path.join(root, "episodes", day + ".jsonl")):
             if e["k"] == "ep" and e["role"] == "pick" and e.get("seen_open_ms"):
                 lags.append((e["seen_open_ms"] - e["t_open"]) / 1000)
-        books = {(b["a"], b["coin"], b["t_open"]): b for b in read_jsonl(os.path.join(root, "book", day + ".jsonl"))
-                 if b["k"] == "book"}
+        books = {(b["a"], b["coin"], b["t_open"]): b for b in book_lines(root, day)}
+        rebooked += sum(1 for b in books.values() if b.get("rebook"))
+        api += sum(1 for b in books.values() if "api" in b)
         for f in read_jsonl(os.path.join(root, "funding", day + ".jsonl")):
             if f["k"] != "funding":
                 continue
@@ -1220,7 +1360,7 @@ def produce_verdict(state, state_dir, sel, rule):
             absent += 1 if f["absent"] else 0
             role = "pick" if f["a"] in picks else "null"
             for d in DELAYS_S:
-                cell = b["d"][str(d)]
+                cell = booked_at(b, d)
                 if cell is None:
                     continue
                 booked[d][role] += 1
@@ -1235,17 +1375,201 @@ def produce_verdict(state, state_dir, sel, rule):
     for a in null:   # a null account's result over every pick's own span, averaged over the picks (TZ-75 B5)
         results[a] = spanned[a][spans[0]] if len(spans) == 1 else {d: {v: statistics.fmean(
             spanned[a][joins[p]][d][v] for p in picks) for v in ("src", "stop")} for d in DELAYS_S}
-    verdict = decide(picks, null, results, booked[1800]["pick"])
+    verdict = decide(picks, null, results, booked[READABLE_AT_S]["pick"])
     doc = {"v": 1, "k": "paper-verdict", "follow_from": sel["follow_from"], "window_end": sel["window_end"],
            "picks": picks, "joined": {a: iso(joins[a]) for a in picks}, "null": null, "booked": {str(d): booked[d] for d in DELAYS_S}, "unbookable": unbookable,
            "funding_absent": absent, "lag_s": {"n": len(lags), "p50": nearest_rank(lags, 0.5),
-                                                 "p95": nearest_rank(lags, 0.95)}, "fp": fingerprint()}
+                                                 "p95": nearest_rank(lags, 0.95)}, "fp": fingerprint(),
+           "window": state.get("window"), "rebooked": rebooked, "api": api}
     doc.update(verdict)
     write_record(state, state_dir, "verdict.json", doc=doc)
     state["verdict"] = True
     return True
 
 
+# --- TZ-77: the window as it stands, and the picks' orders ----------------------------------
+def window_view(state, sel):
+    """The selection with its window as it stands (TZ-77 (1)): thirteen weeks until the decision at their end,
+    then the end that decision and the booking set. selection.json itself never changes."""
+    w = state.get("window")
+    if w is None:
+        return sel
+    return dict(sel, window_end_ms=w["end_ms"], window_end=iso(w["end_ms"]))
+
+
+def pick_book(state, state_dir, sel, picks):
+    """The written book of the picks' episodes, rebooks applied: (booked at READABLE_AT_S, unbookable for good)."""
+    root = os.path.join(state_dir, "records", RECORD_DIR)
+    booked = final = 0
+    if state["written"]["book"] is not None:
+        for day in days_between(utc_date(sel["follow_from_ms"]), state["written"]["book"]):
+            for b in book_lines(root, day):
+                if b["a"] not in picks:
+                    continue
+                if booked_at(b, READABLE_AT_S) is not None:
+                    booked += 1
+                elif "unbookable" in b and not awaits_rebook(b):
+                    final += 1
+    return booked, final
+
+
+def seen_pick_episodes(state, state_dir, sel, picks):
+    """Every pick episode of the window so far: in the written episode files, closed since, and open."""
+    root = os.path.join(state_dir, "records", RECORD_DIR)
+    n = 0
+    if state["written"]["episodes"] is not None:
+        for day in days_between(utc_date(sel["follow_from_ms"]), state["written"]["episodes"]):
+            n += sum(1 for e in read_jsonl(os.path.join(root, "episodes", day + ".jsonl"))
+                     if e["k"] == "ep" and e["a"] in picks)
+    n += sum(1 for e in state["closed"] if e["a"] in picks)
+    return n + sum(1 for a, acct in state["accounts"].items() if a in picks
+                   for ep in acct["coins"].values() if ep is not None)
+
+
+def at_window_end(state, state_dir, sel, now):
+    """The end as it stands is reached and every account polled DAY_SETTLE_S past it: True when the window closes
+    there (TZ-77 (1)). At thirteen weeks it closes whenever its pick episodes -- written, closed since or open, less
+    those written unbookable for good -- number EPISODES_MIN or more, so wherever the verdict of thirteen weeks can
+    be readable the window is thirteen weeks; otherwise it runs on, to the end fix_end sets or RUN_ON_MAX_DAYS after
+    follow_from. A window that ran on closes at its end."""
+    if state.get("window") is not None:
+        return True
+    picks = pick_joins(state, sel)[0]
+    seen = seen_pick_episodes(state, state_dir, sel, picks)
+    final = pick_book(state, state_dir, sel, picks)[1]
+    w = {"weeks13_ms": sel["window_end_ms"], "seen": seen, "unbookable": final, "decided_ms": now}
+    if seen - final >= EPISODES_MIN:
+        state["window"] = dict(w, run_on=False, end_ms=sel["window_end_ms"], fixed=True)
+        return True
+    cap = sel["follow_from_ms"] + RUN_ON_MAX_DAYS * DAY_MS
+    state["window"] = dict(w, run_on=True, end_ms=cap, fixed=False)
+    common.write_outbox("notice", N_RUN_ON.format(n=seen - final, date=tbilisi_date(cap)))
+    return False
+
+
+def fix_end(state, state_dir, sel, now):
+    """While the window runs on and its end is open: once the written book holds EPISODES_MIN pick episodes booked
+    at READABLE_AT_S, the end is fixed at the first instant after now on follow_from's daily grid, the cap at the
+    latest. Every fill before that end is followed as before, so the window closes there as at thirteen weeks."""
+    w = state.get("window")
+    if not w or not w["run_on"] or w["fixed"]:
+        return False
+    booked = pick_book(state, state_dir, sel, pick_joins(state, sel)[0])[0]
+    if booked < EPISODES_MIN:
+        return False
+    e0 = w["weeks13_ms"]
+    end = min(e0 + ((now - e0) // DAY_MS + 1) * DAY_MS, w["end_ms"])
+    w.update(end_ms=end, fixed=True, booked=booked, fixed_ms=now)
+    common.write_outbox("notice", N_END_SET.format(n=booked, date=tbilisi_date(end)))
+    return True
+
+
+def orders_rows(addr, limiter):
+    """Every row historicalOrders answers for addr -- one per status an order took, the latest ORDERS_COMPLETE."""
+    doc = info({"type": "historicalOrders", "user": addr}, limiter)
+    if not isinstance(doc, list):
+        raise ValueError("historicalOrders: not a list")
+    return doc
+
+
+def episode_oid(e, end, limiter):
+    """The order of an episode's opening (end "open") or closing fill: the episode's own; for an episode written
+    before TZ-77, the order of the account's fill of that coin at that millisecond; None for a cut close or none."""
+    key, t = ("oid_open", e["t_open"]) if end == "open" else ("oid_close", e["t_close"])
+    if e.get(key) is not None or (end == "close" and e.get("cut")):
+        return e.get(key)
+    return next((f["oid"] for f in fills_since(e["a"], t, limiter, t) if f["coin"] == e["coin"]), None)
+
+
+def produce_orders(state, state_dir, sel, limiter, symbols, now):
+    """TZ-77 (2), deciding nothing: for each day of the window over DAY_SETTLE_S ago whose episode file is written,
+    orders/<day>.jsonl, once -- each pick episode of that file with the orders of its opening and closing fills, and
+    every row historicalOrders answered for a pick whose status time falls in the day, on a copyable coin. A pick
+    whose answer may have rolled part of that day off is marked incomplete. Transport ends the pass; the day waits."""
+    first, last = utc_date(sel["follow_from_ms"]), utc_date(sel["window_end_ms"])
+    root = os.path.join(state_dir, "records", RECORD_DIR)
+    picks, answers = pick_joins(state, sel)[0], {}
+    while True:
+        day = next_date(state["written"]["orders"], first)
+        start = day_start(day)
+        if (day > last or state["written"]["episodes"] is None or day > state["written"]["episodes"]
+                or now < start + DAY_MS + DAY_SETTLE_S * 1000):
+            return
+        for a in picks:
+            if a not in answers:
+                answers[a] = orders_rows(a, limiter)
+        eps = [{"k": "ep", "a": e["a"], "coin": e["coin"], "t_open": e["t_open"], "t_close": e["t_close"],
+                "cut": bool(e.get("cut")), "oid_open": episode_oid(e, "open", limiter),
+                "oid_close": episode_oid(e, "close", limiter)}
+               for e in read_jsonl(os.path.join(root, "episodes", day + ".jsonl")) if e["k"] == "ep" and e["a"] in picks]
+        rows, heads = [], {}
+        for a in picks:
+            got = answers[a]
+            oldest = min((int(r["statusTimestamp"]) for r in got), default=None)
+            heads[a] = {"rows": len(got), "complete": len(got) < ORDERS_COMPLETE or (oldest is not None and oldest < start)}
+            rows += [dict(r, k="row", a=a) for r in got if start <= int(r["statusTimestamp"]) < start + DAY_MS
+                     and symbol_for(r["order"]["coin"], symbols) is not None]
+        rows.sort(key=lambda r: (int(r["statusTimestamp"]), r["a"], int(r["order"]["oid"]), r["status"]))
+        write_record(state, state_dir, "orders/%s.jsonl" % day,
+                     [{"k": "day", "date": day, "episodes": len(eps), "rows": len(rows), "picks": heads}] + eps + rows)
+        state["written"]["orders"] = day
+
+
+def produce_readout(state, state_dir, sel, rule):
+    """TZ-77 (2), deciding nothing: once the verdict and the window's last orders file are written, orders-readout.json
+    -- over the picks' closed episodes inside their spans: how many opening, and how many closing, orders rested at
+    least ANNOUNCED_S before their fill, and how long; how many orders able to open a position rested, and how many
+    of those opened no episode; and, where the exit rested, the copy entered at each delay and left at the pick's own
+    exit against the copy left at that delay, each gross less fees over capital."""
+    last = utc_date(sel["window_end_ms"])
+    if state.get("readout") or not state["verdict"] or state["written"]["orders"] != last:
+        return False
+    root = os.path.join(state_dir, "records", RECORD_DIR)
+    picks, joins = pick_joins(state, sel)
+    days = days_between(utc_date(sel["follow_from_ms"]), last)
+    placed, rested, eps, books = {}, set(), [], {}
+    for day in days:
+        for x in read_jsonl(os.path.join(root, "orders", day + ".jsonl")):
+            if x["k"] == "row":
+                o = x["order"]
+                placed[o["oid"]] = min(placed.get(o["oid"], o["timestamp"]), o["timestamp"])
+                if (x["status"] == "open" and not o["reduceOnly"] and x["a"] in joins
+                        and joins[x["a"]] <= o["timestamp"] < sel["window_end_ms"]):
+                    rested.add((x["a"], o["oid"]))
+            elif x["k"] == "ep" and not x["cut"] and x["a"] in joins and x["t_open"] >= joins[x["a"]]:
+                eps.append(x)
+        for b in book_lines(root, day):
+            if b["a"] in joins:
+                books[(b["a"], b["coin"], b["t_open"])] = b
+
+    def leads(t, oid):
+        return [(e, (e[t] - placed[e[oid]]) / 1000) for e in eps if e[oid] in placed]
+
+    doc = {"v": 1, "k": "paper-orders", "picks": picks, "announced_s": ANNOUNCED_S, "episodes": len(eps), "fp": fingerprint()}
+    for name, t, oid in (("entry", "t_open", "oid_open"), ("exit", "t_close", "oid_close")):
+        known = leads(t, oid)
+        ahead = [s for _, s in known if s >= ANNOUNCED_S]
+        doc[name] = {"known": len(known), "rested": len(ahead),
+                     "lead_s": {"p50": nearest_rank(ahead, 0.5), "p95": nearest_rank(ahead, 0.95)}}
+    opened = {e["oid_open"] for e in eps}
+    doc["resting_entries"] = {"rested": len(rested), "opened_no_episode": sum(1 for _, o in rested if o not in opened)}
+    doc["exit_copy"] = {}
+    for d in DELAYS_S:
+        cell = {"n": 0, "at_pick_exit": {"src": 0.0, "stop": 0.0}, "at_delay": {"src": 0.0, "stop": 0.0}}
+        for e, s in leads("t_close", "oid_close"):
+            b = books.get((e["a"], e["coin"], e["t_open"]))
+            if s < ANNOUNCED_S or b is None or booked_at(b, d) is None or (b.get("x") or {}).get(str(d)) is None:
+                continue
+            cell["n"] += 1
+            for v in ("src", "stop"):
+                cell["at_pick_exit"][v] += (b["x"][str(d)][v]["gross"] - b["x"][str(d)][v]["fee"]) / rule["capital_usdt"]
+                cell["at_delay"][v] += (b["d"][str(d)][v]["gross"] - b["d"][str(d)][v]["fee"]) / rule["capital_usdt"]
+        doc["exit_copy"][str(d)] = cell
+    write_record(state, state_dir, "orders-readout.json", doc=doc)
+    state["readout"] = True
+    return True
+
+
 # --- the service ---------------------------------------------------------------------
 def load_state(path, sel):
     try:
@@ -1285,26 +1609,29 @@ def service(state_dir, tree):
     rule = sel["rule"]    # frozen at the selection: a later change of owner.json moves nothing here
     state = load_state(state_path, sel)
     rescan_state(state, sel)
+    state["written"].setdefault("rebook", None)   # TZ-77: a state written before it
+    state["written"].setdefault("orders", None)
     box, thread = {}, None
-    written = None
+    written, window_failed = None, False
     symbols = set(sel["symbols"])
     inputs_box = {}
 
     def inputs_for():
         today = utc_date(now_ms())
         if inputs_box.get("today") != today:
-            inputs_box.update(today=today, inputs=Inputs(state_dir, today))
+            inputs_box.update(today=today, inputs=Inputs(state_dir, today, fallback=fapi_klines))
         return inputs_box["inputs"]
 
     while True:
         now = now_ms()
+        view = window_view(state, sel)   # TZ-77 (1): every step below reads the window as it stands
         if starts(sel) and not state["cut"]:
             for addr, acct in state["accounts"].items():
                 if now < acct["due_ms"]:
                     continue
                 acct["due_ms"] = now + 1000 * (PICK_POLL_S if acct["role"] == "pick" else NULL_POLL_S)
                 try:
-                    poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for)
+                    poll(addr, acct, view, symbols, limiter, now, rule, inputs_for)
                     if acct["failing"]:
                         common.log("paper: poll %s answered again" % addr_short(addr))
                     acct["failing"] = False
@@ -1314,7 +1641,7 @@ def service(state_dir, tree):
                     acct["failing"] = True
             gather_closed(state)
             rs = state["rescan"]
-            if thread is None and rescan_due(state, sel, now):
+            if thread is None and rescan_due(state, view, now):
                 picks = pick_joins(state, sel)[0]
                 if not rs["running"]:
                     rs.update(n=rs["n"] + 1, running=True)
@@ -1328,34 +1655,64 @@ def service(state_dir, tree):
             elif thread is not None and not thread.is_alive():
                 thread, limiter.per_min = None, WEIGHT_PER_MIN
                 if "result" in box:
-                    adopt(state, state_dir, sel, box["result"], rs["n"], now)
+                    adopt(state, state_dir, view, box["result"], rs["n"], now)
                     rs.update(running=False, due_ms=now + RESCAN_EVERY_DAYS * DAY_MS)
                     common.log("paper: rescan %d adopted picks=%d" % (rs["n"], len(box["result"]["picks"])))
                 else:
                     rs["due_ms"] = now + WORK_EVERY_S * 1000
                     common.log("paper: rescan %d ended (%s), resumes later" % (rs["n"], box.get("error", "-")))
-            if now >= sel["window_end_ms"] and all(a["polled_ms"] >= sel["window_end_ms"] + DAY_SETTLE_S * 1000
-                                                    for a in state["accounts"].values()):
-                cut_open(state, sel)
-                if not state["closed_notice"]:
-                    common.write_outbox("notice", N_CLOSED)
-                    state["closed_notice"] = True
+            end = view["window_end_ms"]
+            if now >= end and all(a["polled_ms"] >= end + DAY_SETTLE_S * 1000 for a in state["accounts"].values()):
+                try:
+                    closes = at_window_end(state, state_dir, sel, now)
+                except (OSError, ValueError, KeyError) as exc:   # the decision waits; the window stays as it stands
+                    closes = None
+                    if not window_failed:
+                        common.log("paper: window decision failed (%s)" % exc.__class__.__name__)
+                window_failed = closes is None
+                view = window_view(state, sel)
+                if closes is None:
+                    pass
+                elif closes:
+                    cut_open(state, view)
+                    if not state["closed_notice"]:
+                        common.write_outbox("notice", N_CLOSED if not state["window"]["run_on"] else
+                                            N_CLOSED_RUN_ON.format(date=tbilisi_date(end)))
+                        state["closed_notice"] = True
+                else:
+                    common.log("paper: window runs on to %s" % view["window_end"])
         if starts(sel):
             try:
-                produce_days(state, state_dir, sel, now)
+                produce_days(state, state_dir, view, now)
             except (OSError, ValueError) as exc:
                 common.log("paper: day file failed (%s)" % exc.__class__.__name__)
             if now >= state["next_work_ms"]:
                 state["next_work_ms"] = now + WORK_EVERY_S * 1000
                 try:
-                    produce_books(state, state_dir, sel, rule, inputs_for())
-                    produce_funding(state, state_dir, sel, inputs_for())
-                    if produce_verdict(state, state_dir, sel, rule):
+                    produce_rebooks(state, state_dir, view, rule, inputs_for())   # TZ-77 (0): its wait ends only it
+                except NotReady:
+                    pass
+                except (Transport, OSError, ValueError, KeyError, ArithmeticError) as exc:
+                    common.log("paper: rebooking failed (%s)" % exc.__class__.__name__)
+                try:
+                    produce_books(state, state_dir, view, rule, inputs_for())
+                    produce_funding(state, state_dir, view, inputs_for())
+                    if produce_verdict(state, state_dir, view, rule):
                         common.write_outbox("notice", N_VERDICT)
                 except NotReady:
                     pass
                 except (Transport, OSError, ValueError, KeyError, ArithmeticError) as exc:
                     common.log("paper: booking failed (%s)" % exc.__class__.__name__)
+                try:
+                    if fix_end(state, state_dir, view, now):                       # TZ-77 (1)
+                        common.log("paper: window ends %s" % window_view(state, sel)["window_end"])
+                except (OSError, ValueError, KeyError) as exc:
+                    common.log("paper: window failed (%s)" % exc.__class__.__name__)
+                try:
+                    produce_orders(state, state_dir, window_view(state, sel), limiter, symbols, now)   # TZ-77 (2)
+                    produce_readout(state, state_dir, window_view(state, sel), rule)
+                except (Transport, OSError, ValueError, KeyError, TypeError, ArithmeticError) as exc:
+                    common.log("paper: orders failed (%s)" % exc.__class__.__name__)
         if state["pending"] and now >= state["next_publish_ms"]:
             state["next_publish_ms"] = now + PUBLISH_EVERY_S * 1000
             common.log("paper: publish " + publish(state, state_dir, tree))
@@ -1367,11 +1724,24 @@ def service(state_dir, tree):
 
 
 # --- the probe -----------------------------------------------------------------------
+def api_against_archive(sym, date):
+    """TZ-77 (0): the API fallback against the archive on a day both hold -- minutes compared on (o, h, l, c) and
+    the day's close; one line of counts."""
+    def by_minute(rows):
+        return {int(r[0]): tuple(float(x) for x in r[1:5]) for r in rows}
+    arch = by_minute(vision_rows("/daily/klines/%s/1m/%s-1m-%s.zip" % (sym, sym, date)))
+    api = by_minute(fapi_klines(sym, "1m", date))
+    close_a = float(vision_rows("/daily/klines/%s/1d/%s-1d-%s.zip" % (sym, sym, date))[0][4])
+    close_b = float(fapi_klines(sym, "1d", date)[0][4])
+    return "%s %s archive=%d api=%d equal=%d close=%s" % (sym, date, len(arch), len(api), sum(
+        1 for t, v in arch.items() if api.get(t) == v), "equal" if close_a == close_b else "differs")
+
+
 def probe():
     """One read of every interface the service uses; one line each, counts only. Exit 0 when every
     read answered."""
     ok, limiter, t0 = True, Limiter(), day_start(utc_date(now_ms()))
-    yesterday = add_days(utc_date(now_ms()), -1)
+    published = add_days(utc_date(now_ms()), -2)   # TZ-77: two days back, a day the archive has published by now
     prev_month = add_days(utc_date(now_ms())[:8] + "01", -1)[:7]
     steps = (
         ("leaderboard", lambda: "rows=%d pool=%d bad=%d" % (lambda p: (p[1], len(p[0]), p[2]))(
@@ -1383,10 +1753,12 @@ def probe():
                                                          limiter)["assetPositions"])),
         ("fills", lambda: (lambda fl: "fills=%d first=%s" % (len(fl), iso(int(fl[0]["time"])) if fl else "-"))(
             fills_since(PROBE_ACCOUNT, t0 - WINDOW_DAYS * DAY_MS, limiter, t0 - 1))),
-        ("klines_1m", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1m/BTCUSDT-1m-%s.zip" % yesterday))),
-        ("klines_1d", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1d/BTCUSDT-1d-%s.zip" % yesterday))),
+        ("klines_1m", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1m/BTCUSDT-1m-%s.zip" % published))),
+        ("klines_1d", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1d/BTCUSDT-1d-%s.zip" % published))),
         ("funding", lambda: "rows=%d" % len(vision_rows(
             "/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-%s.zip" % prev_month))),
+        ("api", lambda: api_against_archive("BTCUSDT", published)),
+        ("orders", lambda: "rows=%d" % len(orders_rows(PROBE_ACCOUNT, limiter))),
     )
     for name, step in steps:
         try:
diff --git a/vps/selftest.py b/vps/selftest.py
index 97d1365..df60fc4 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1652,6 +1652,12 @@ def section_w(s):
     section_w_rescan(s)
     # W17. the verdict over each pick's own span (TZ-75 B5)
     section_w_spans(s)
+    # W18. the exchange's own klines for a day the archive never published, and the rebook (TZ-77 (0))
+    section_w_api(s)
+    # W19. the window as it stands: thirteen weeks, or run on to the thirtieth booked pick episode (TZ-77 (1))
+    section_w_window(s)
+    # W20. the picks' orders and their readout, deciding nothing (TZ-77 (2))
+    section_w_orders(s)
 
 
 def w_rows(path):
@@ -2598,6 +2604,436 @@ def section_w_spans(s):
         shutil.rmtree(tmp, ignore_errors=True)
 
 
+class W18Answer:
+    """One urlopen answer: a body read once, as a context manager."""
+
+    def __init__(self, body):
+        self.body = body
+
+    def read(self):
+        return self.body
+
+    def __enter__(self):
+        return self
+
+    def __exit__(self, *exc):
+        return False
+
+
+def w18_minutes(date, close="100"):
+    start = paper.day_start(date)
+    return [[str(m), "100", "101", "99", close] for m in range(start, start + paper.DAY_MS, 60000)]
+
+
+def w18_api(calls):
+    """A fallback: flat minutes at 100 and a close of 123.5, every call counted."""
+    def api(sym, interval, date):
+        calls.append((sym, interval, date))
+        if interval == "1m":
+            return w18_minutes(date)
+        return [[str(paper.day_start(date)), "0", "0", "0", "123.5"]]
+    return api
+
+
+def section_w_api(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-w18.")
+    saved = paper.urllib.request.urlopen
+    try:
+        day = "2026-01-05"
+        start, h = paper.day_start(day), 3600000
+        asked, answer = [], {}
+
+        def opener(url, timeout=None):
+            asked.append(url)
+            if isinstance(answer["next"], Exception):
+                raise answer["next"]
+            return W18Answer(json.dumps(answer["next"]).encode("utf-8"))
+        paper.urllib.request.urlopen = opener
+        rows = [[start - 60000, "1", "1", "1", "1"], [start, "100", "101", "99", "100.5"],
+                [start + paper.DAY_MS, "2", "2", "2", "2"]]
+        answer["next"] = rows
+        s.check("fapi_klines: the day's rows alone, in the archive's columns",
+                paper.fapi_klines("BTCUSDT", "1m", day) == [rows[1]])
+        s.check("fapi_klines: the exchange's klines over the day's own milliseconds",
+                asked[-1] == "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1m&startTime=%d&endTime=%d"
+                "&limit=1500" % (start, start + paper.DAY_MS - 1))
+        outcomes = []
+        for got, want in (([], paper.Absent), ({"code": 0}, paper.Transport),
+                          (urllib.error.HTTPError("u", 400, "Bad Request", {}, None), paper.Absent),
+                          (urllib.error.HTTPError("u", 451, "Unavailable", {}, None), paper.Transport),
+                          (urllib.error.URLError("down"), paper.Transport), ([[str(start), "x"]], paper.Transport)):
+            answer["next"] = got
+            try:
+                paper.fapi_klines("BTCUSDT", "1d", day)
+                outcomes.append(False)
+            except (paper.Absent, paper.Transport) as exc:
+                outcomes.append(type(exc) is want)
+        s.check("fapi_klines: none or HTTP 400 is Absent; no list, 451, no answer or an unreadable row is Transport",
+                outcomes == [True] * 6)
+        paper.urllib.request.urlopen = saved
+
+        def archive(path):   # the archive never published the day; every other file is w_rows'
+            if day in path:
+                raise paper.NotPublished(path)
+            return w_rows(path)
+        calls, today = [], paper.add_days(day, 30)
+        inputs = paper.Inputs(tmp, today, rows=archive, fallback=w18_api(calls))
+        times, flat = inputs.minutes("BTCUSDT", day)
+        s.check("minutes: an absent archive day is the fallback's 1 440 minutes",
+                len(times) == 1440 and times[0] == start and paper.Rows(flat)[0] == (100.0, 101.0, 99.0, 100.0))
+        s.check("close_on: an absent archive close is the fallback's", inputs.close_on("BTCUSDT", day) == 123.5)
+        with open(os.path.join(tmp, "api-days.json"), encoding="utf-8") as fh:
+            kept = json.load(fh)
+        s.check("both days kept on disk and marked as used",
+                kept == ["BTCUSDT 1d 2026-01-05", "BTCUSDT 1m 2026-01-05"]
+                and inputs.used == {"1m 2026-01-05", "1d 2026-01-05"} and calls == [("BTCUSDT", "1m", day),
+                                                                                   ("BTCUSDT", "1d", day)])
+        later = paper.Inputs(tmp, today, rows=archive, fallback=w18_api(calls))
+        s.check("a later pass: the close from closes.json, no call, still marked",
+                later.close_on("BTCUSDT", day) == 123.5 and len(calls) == 2 and later.used == {"1d 2026-01-05"})
+        bare_dir = os.path.join(tmp, "bare")
+        os.makedirs(bare_dir)
+        bare = paper.Inputs(bare_dir, today, rows=archive)
+        raised = 0
+        for read in (lambda: bare.minutes("BTCUSDT", day), lambda: bare.close_on("BTCUSDT", day)):
+            try:
+                read()
+            except paper.Absent:
+                raised += 1
+        s.check("without a fallback an absent day stays Absent, minutes and close", raised == 2)
+
+        def refusing(sym, interval, date):
+            raise paper.Absent("fapi %s %s %s: no klines" % (sym, interval, date))
+        refused = paper.Inputs(bare_dir, today, rows=archive, fallback=refusing)
+        try:
+            refused.minutes("ETHUSDT", day)
+            reason = None
+        except paper.Absent as exc:
+            reason = str(exc)
+        s.check("a fallback with no klines is Absent under its own name, never awaiting a rebook",
+                reason == "fapi ETHUSDT 1m 2026-01-05: no klines" and not paper.awaits_rebook({"unbookable": reason}))
+        # book_episode: the API's day named, the copy left at the pick's own exit
+        rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
+        pick = {"a": "0x" + "a" * 40, "role": "pick", "coin": "BTC", "symbol": "BTCUSDT", "side": 1, "t_open": start + h,
+                "t_close": start + 2 * h + 30000, "px_open": "100", "px_close": "100", "cut": False}
+        line = paper.book_episode(pick, inputs, rule, start + 10 * paper.DAY_MS)
+        s.check("a pick's episode on the API's day: booked at four delays, the day named",
+                sorted(line["d"]) == ["1800", "300", "5", "7200"] and line["api"] == ["1m 2026-01-05"])
+        s.check("x: entered at 1 800 s, left at the pick's own exit minute",
+                line["x"]["1800"]["entry_ms"] == start + h + 1800000 and line["x"]["1800"]["src"]["exit_ms"] == start + 2 * h
+                and line["d"]["1800"]["src"]["exit_ms"] == start + 2 * h + 1800000)
+        s.check("x: a copy entering after the pick's exit has none", line["x"]["7200"] is None)
+        null = dict(pick, a="0x" + "b" * 40, role="null")
+        cut = dict(pick, cut=True, t_close=start + 5 * h)
+        s.check("x: never for a null account's episode, nor a cut one",
+                "x" not in paper.book_episode(null, inputs, rule, start + 10 * paper.DAY_MS)
+                and "x" not in paper.book_episode(cut, inputs, rule, start + 5 * h))
+        # the rebook: only the line written unbookable for an archive file, booked again, once
+        root = os.path.join(tmp, "records", paper.RECORD_DIR)
+        for sub in ("episodes", "book"):
+            os.makedirs(os.path.join(root, sub))
+        eps = [dict(pick, k="ep", rank=1, n=2), dict(null, k="ep", rank=None, n=2),
+               dict(null, k="ep", rank=None, n=2, t_open=start + 3 * h, t_close=start + 4 * h)]
+        target = {"k": "book", "a": pick["a"], "coin": "BTC", "symbol": "BTCUSDT", "side": 1, "t_open": pick["t_open"],
+                  "unbookable": "/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2026-01-05.zip"}
+        kept_line = paper.book_episode(eps[1], inputs, rule, start + 10 * paper.DAY_MS)
+        final = {"k": "book", "a": null["a"], "coin": "BTC", "symbol": "BTCUSDT", "side": 1, "t_open": start + 3 * h,
+                 "unbookable": "sigma is zero"}
+        for sub, lines in (("episodes", eps), ("book", [target, kept_line, final])):
+            with open(os.path.join(root, sub, day + ".jsonl"), "w", encoding="utf-8") as fh:
+                fh.write("".join(json.dumps(x) + "\n" for x in [{"k": "day", "date": day}] + lines))
+        sel = {"follow_from_ms": start, "window_end_ms": start + 10 * paper.DAY_MS}
+        state = {"pending": [], "written": {"episodes": day, "book": day, "funding": None, "rebook": None}}
+        before = paper.book_lines(root, day)
+        s.check("before the rebook: the target awaits it, the two others do not",
+                [paper.awaits_rebook(b) for b in before] == [True, False, False])
+        funding_first = copy.deepcopy(state)
+        paper.produce_funding(funding_first, tmp, sel, inputs)
+        s.check("funding waits for a day whose rebook is pending", funding_first["written"]["funding"] is None
+                and not os.path.exists(os.path.join(root, "funding", day + ".jsonl")))
+        paper.produce_rebooks(state, tmp, sel, rule, inputs)
+        again = paper.read_jsonl(os.path.join(root, "rebook", day + ".jsonl"))
+        s.check("rebook/<day>.jsonl: one line, the target, booked again with the API's day",
+                again[0] == {"k": "day", "date": day, "rebooked": 1, "booked": 1, "unbookable": 0} and len(again) == 2
+                and again[1]["rebook"] is True and "d" in again[1] and again[1]["api"] == ["1m 2026-01-05"]
+                and (again[1]["a"], again[1]["t_open"]) == (pick["a"], pick["t_open"]))
+        after = paper.book_lines(root, day)
+        s.check("book_lines: the rebooked line in the target's place, the others untouched",
+                after[0] == again[1] and after[1] == kept_line and after[2] == final)
+        s.check("the rebook is pending once and the day done", state["pending"] == ["rebook/%s.jsonl" % day]
+                and state["written"]["rebook"] == day)
+        paper.produce_rebooks(state, tmp, sel, rule, inputs)
+        s.check("a second pass rebooks nothing", state["pending"] == ["rebook/%s.jsonl" % day])
+        paper.produce_funding(state, tmp, sel, inputs)
+        funding = paper.read_jsonl(os.path.join(root, "funding", day + ".jsonl"))
+        s.check("then funding is written over the rebooked line", state["written"]["funding"] == day
+                and [("unbooked" in f) for f in funding[1:]] == [False, False, True])
+        # the verdict counts the rebooked pick episode as booked
+        vsel = {"picks": [{"address": pick["a"], "rank": 1}], "null": [{"address": null["a"]}], "follow_from_ms": start,
+                "window_end_ms": start + 20 * h, "follow_from": paper.iso(start), "window_end": paper.iso(start + 20 * h)}
+        vstate = paper.new_state(vsel)
+        vstate["written"].update(episodes=day, book=day, funding=day, rebook=day)
+        paper.produce_verdict(vstate, tmp, vsel, rule)
+        with open(os.path.join(root, "verdict.json"), encoding="utf-8") as fh:
+            verdict = json.load(fh)
+        s.check("the verdict reads the rebooked line: one pick episode booked, one rebooked, two from the API",
+                verdict["booked"]["1800"] == {"pick": 1, "null": 1} and verdict["rebooked"] == 1 and verdict["api"] == 2
+                and verdict["unbookable"] == 1 and verdict["window"] is None)
+    finally:
+        paper.urllib.request.urlopen = saved
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
+def w19_write(root, sub, day, lines):
+    os.makedirs(os.path.join(root, sub), exist_ok=True)
+    with open(os.path.join(root, sub, day + ".jsonl"), "w", encoding="utf-8") as fh:
+        fh.write("".join(json.dumps(x) + "\n" for x in [{"k": "day", "date": day}] + lines))
+
+
+def section_w_window(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-w19.")
+    saved = (paper.EPISODES_MIN, common.OUTBOX_DIR)
+    try:
+        paper.EPISODES_MIN = 2
+        outbox = os.path.join(tmp, "outbox")
+        os.makedirs(outbox)
+        common.OUTBOX_DIR = outbox
+        p, n, h = "0x" + "a" * 40, "0x" + "b" * 40, 3600000
+        ff = paper.day_start("2026-01-05") + h
+        we = ff + 2 * paper.DAY_MS
+        cap = ff + paper.RUN_ON_MAX_DAYS * paper.DAY_MS
+        sel = {"picks": [{"address": p, "rank": 1}], "null": [{"address": n}], "follow_from_ms": ff, "window_end_ms": we,
+               "follow_from": paper.iso(ff), "window_end": paper.iso(we), "symbols": ["BTCUSDT"]}
+        rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
+
+        def world(reason):
+            """A pick episode written with its book line unbookable for reason, and one open at the window's end."""
+            root = tempfile.mkdtemp(dir=tmp)
+            records = os.path.join(root, "records", paper.RECORD_DIR)
+            state = paper.new_state(sel)
+            day = paper.utc_date(ff)
+            w19_write(records, "episodes", day, [{"k": "ep", "a": p, "role": "pick", "coin": "BTC", "t_open": ff + h,
+                                                   "t_close": ff + 2 * h}])
+            w19_write(records, "book", day, [{"k": "book", "a": p, "coin": "BTC", "symbol": "BTCUSDT", "side": 1,
+                                              "t_open": ff + h, "unbookable": reason}])
+            state["written"].update(episodes=day, book=day)
+            state["accounts"][p]["coins"]["ETH"] = {"coin": "ETH", "side": 1, "t_open": we - h}
+            return root, state
+
+        s.check("before its end the window is the selection's", paper.window_view(paper.new_state(sel), sel) is sel)
+        root, state = world("/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2026-01-05.zip")
+        s.check("thirteen weeks that can still make the verdict: the window closes at them, as the selection has it",
+                paper.at_window_end(state, root, sel, we + 700000) and state["window"]["run_on"] is False
+                and state["window"]["end_ms"] == we and state["window"]["seen"] == 2 and state["window"]["unbookable"] == 0
+                and paper.window_view(state, sel)["window_end_ms"] == we and os.listdir(outbox) == [])
+        root, state = world("sigma is zero")
+        ran_on = not paper.at_window_end(state, root, sel, we + 700000)
+        s.check("thirteen weeks that cannot: the window runs on to the cap, 182 days after follow_from",
+                ran_on and state["window"]["run_on"] and not state["window"]["fixed"] and state["window"]["end_ms"] == cap
+                and state["window"]["seen"] == 2 and state["window"]["unbookable"] == 1
+                and paper.window_view(state, sel)["window_end"] == paper.iso(cap))
+        with open(os.path.join(outbox, [x for x in sorted(os.listdir(outbox)) if "-notice-" in x][-1]),
+                  encoding="utf-8") as fh:
+            note = json.load(fh)
+        s.check("the notice of the window run on, character for character", note["kind"] == "notice" and note["text"] == (
+            "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0441\u0434\u0435\u043b\u043e\u043a \u043a\u0438\u0442\u043e\u0432 \u0437\u0430 13 \u043d\u0435\u0434\u0435\u043b\u044c \u2014 1 \u0438\u0437 30 \u043d\u0443\u0436\u043d\u044b\u0445, \u043e\u043a\u043d\u043e \u043f\u0440\u043e\u0434\u043b\u0435\u043d\u043e \u0434\u043e 30-\u0439, \u043d\u043e \u043d\u0435 \u0434\u043e\u043b\u044c\u0448\u0435 "
+            + datetime.fromtimestamp(cap / 1000, tz=announce.TBILISI).strftime("%d.%m.%Y") + "."))
+        s.check("a window that ran on closes at its end", paper.at_window_end(state, root, sel, cap + 700000))
+        # a fill past the end as it stands is held, then applied once the window runs on
+        held = paper.new_state(sel)
+        acct = held["accounts"][p]
+        last = acct["last_ms"]
+        fill = w_fill(we + 1000, 0, "B", 1)
+        inputs = paper.Inputs(tmp, "2026-03-01", rows=w_rows)
+        paper._apply(p, acct, [w_fill(we - 1000, 0, "B", 1, coin="ETH"), fill], sel, {"BTCUSDT", "ETHUSDT"},
+                     we + 2000, rule, lambda: inputs)
+        s.check("a fill past the end is not applied and not passed: last_ms stays before the end",
+                acct["coins"].get("BTC") is None and acct["coins"]["ETH"]["t_open"] == we - 1000
+                and acct["last_ms"] == we - 1000 > last)
+        paper._apply(p, acct, [fill], dict(sel, window_end_ms=cap), {"BTCUSDT", "ETHUSDT"}, we + 2000, rule,
+                     lambda: inputs)
+        s.check("read again once the window runs on, it opens its episode", acct["coins"]["BTC"]["t_open"] == we + 1000)
+        # the end fixed once the written book holds EPISODES_MIN pick episodes booked at 1 800 s
+        root, state = world("sigma is zero")
+        paper.at_window_end(state, root, sel, we + 700000)
+        records = os.path.join(root, "records", paper.RECORD_DIR)
+        cell = {"entry_ms": 0, "entry_px": 1.0, "qty": 1.0, "stop_px": 0.9, "stopped": False,
+                "src": {"exit_ms": 0, "px": 1.0, "gross": 0.0, "fee": 0.0}, "stop": {"exit_ms": 0, "px": 1.0, "gross": 0.0,
+                                                                                    "fee": 0.0}}
+        booked_line = lambda t: {"k": "book", "a": p, "coin": "BTC", "symbol": "BTCUSDT", "side": 1, "t_open": t,  # noqa: E731
+                                 "d": {str(d): cell for d in paper.DELAYS_S}}
+        day2 = paper.utc_date(ff + paper.DAY_MS)
+        w19_write(records, "book", day2, [booked_line(ff + paper.DAY_MS)])
+        state["written"]["book"] = day2
+        s.check("one booked pick episode of two: the end stays open",
+                not paper.fix_end(state, root, sel, we + 2 * paper.DAY_MS) and not state["window"]["fixed"])
+        w19_write(records, "book", day2, [booked_line(ff + paper.DAY_MS), booked_line(ff + paper.DAY_MS + h)])
+        now = we + 2 * paper.DAY_MS + paper.DAY_MS // 2
+        s.check("two: the end fixed at the next instant of follow_from's daily grid",
+                paper.fix_end(state, root, sel, now) and state["window"]["fixed"] and state["window"]["booked"] == 2
+                and state["window"]["end_ms"] == we + 3 * paper.DAY_MS
+                and paper.window_view(state, sel)["window_end_ms"] == we + 3 * paper.DAY_MS)
+        with open(os.path.join(outbox, [x for x in sorted(os.listdir(outbox)) if "-notice-" in x][-1]),
+                  encoding="utf-8") as fh:
+            note = json.load(fh)
+        s.check("the notice of the end, character for character", note["text"] == (
+            "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0443\u0447\u0442\u0451\u043d\u043d\u044b\u0445 \u0441\u0434\u0435\u043b\u043e\u043a \u043a\u0438\u0442\u043e\u0432 \u2014 2 \u0438\u0437 30 \u043d\u0443\u0436\u043d\u044b\u0445, \u043e\u043a\u043d\u043e \u0437\u0430\u043a\u0440\u043e\u0435\u0442\u0441\u044f "
+            + datetime.fromtimestamp((we + 3 * paper.DAY_MS) / 1000, tz=announce.TBILISI).strftime("%d.%m.%Y") + "."))
+        s.check("a fixed end is fixed once", not paper.fix_end(state, root, sel, now + paper.DAY_MS)
+                and state["window"]["end_ms"] == we + 3 * paper.DAY_MS)
+        late = copy.deepcopy(state)
+        late["window"].update(fixed=False, end_ms=cap)
+        s.check("within the cap's last day the end is the cap", paper.fix_end(late, root, sel, cap - h)
+                and late["window"]["end_ms"] == cap)
+        s.check("the closing notice of a window that ran on, character for character",
+                paper.N_CLOSED_RUN_ON.format(date="17.04.2027") == "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u043e\u043a\u043d\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u043e 17.04.2027, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u044b. \u0418\u0442\u043e\u0433 \u2014 \u043f\u043e\u0441\u043b\u0435 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 \u0434\u0430\u043d\u043d\u044b\u0445 Binance.")
+        # the verdict over a window that ran on: its days, its end, its record of the decision
+        view = paper.window_view(state, sel)
+        vroot = os.path.join(tmp, "verdict")
+        vrec = os.path.join(vroot, "records", paper.RECORD_DIR)
+        leg = {"gross": 100.0, "fee": 0.0}
+        days = paper.days_between(paper.utc_date(ff), paper.utc_date(view["window_end_ms"]))
+        for i, d in enumerate(days):
+            t = paper.day_start(d) + 2 * h
+            w19_write(vrec, "episodes", d, [])
+            w19_write(vrec, "book", d, [{"k": "book", "a": p, "coin": "BTC", "t_open": t,
+                                         "d": {str(x): {"src": leg, "stop": leg} for x in paper.DELAYS_S}}])
+            w19_write(vrec, "funding", d, [{"k": "funding", "a": p, "coin": "BTC", "t_open": t, "absent": False,
+                                            "d": {str(x): {"src": 0.0, "stop": 0.0} for x in paper.DELAYS_S}}])
+        state["written"]["funding"] = days[-1]
+        paper.produce_verdict(state, vroot, view, rule)
+        with open(os.path.join(vrec, "verdict.json"), encoding="utf-8") as fh:
+            verdict = json.load(fh)
+        s.check("the verdict of a window run on: every day to its end read, the end and the decision recorded",
+                len(days) == 6 and verdict["booked"]["1800"]["pick"] == 6 and verdict["window_end"] == paper.iso(we + 3 * paper.DAY_MS)
+                and verdict["window"]["run_on"] and verdict["window"]["booked"] == 2)
+    finally:
+        paper.EPISODES_MIN, common.OUTBOX_DIR = saved
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
+def section_w_orders(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-w20.")
+    saved = (paper.info, paper.ORDERS_COMPLETE)
+    try:
+        h = 3600000
+        paper.info = lambda body, limiter: [{"coin": "BTC", "px": "1", "sz": "1", "side": "B", "time": 5,
+                                             "startPosition": "0", "tid": 1, "oid": 77}]
+        s.check("iter_fills keeps the fill's order", paper.fills_since("a", 5, None)[0]["oid"] == 77)
+        coins = {}
+        opened = paper.apply_fill(coins, dict(w_fill(1, 0, "B", 1), oid=11), "BTCUSDT")
+        closed = paper.apply_fill(coins, dict(w_fill(2, 1, "A", 1), oid=12), "BTCUSDT")
+        s.check("an episode names the orders of its opening and closing fills",
+                opened[0][1]["oid_open"] == 11 and closed[0][1]["oid_open"] == 11 and closed[0][1]["oid_close"] == 12)
+        bare = paper.apply_fill({}, w_fill(1, 0, "B", 1), "BTCUSDT")
+        s.check("a fill naming no order: None", bare[0][1]["oid_open"] is None)
+        # orders/<day>.jsonl
+        p, n = "0x" + "a" * 40, "0x" + "b" * 40
+        ff = paper.day_start("2026-01-05") + h
+        we = ff + 2 * paper.DAY_MS
+        d1, d2 = "2026-01-05", "2026-01-06"
+        t1, t2 = ff + h, ff + 3 * h
+        sel = {"picks": [{"address": p, "rank": 1}], "null": [{"address": n}], "follow_from_ms": ff, "window_end_ms": we,
+               "follow_from": paper.iso(ff), "window_end": paper.iso(we), "symbols": ["BTCUSDT", "ETHUSDT"]}
+
+        def row(oid, status, st, placed, coin="BTC", reduce_only=False):
+            return {"order": {"coin": coin, "oid": oid, "timestamp": placed, "reduceOnly": reduce_only,
+                              "orderType": "Limit", "tif": "Gtc", "children": []}, "status": status, "statusTimestamp": st}
+        history = [row(11, "open", t1 - 206000, t1 - 206000), row(11, "filled", t1 + 5000, t1 - 206000),
+                   row(12, "open", t1 - 206000, t1 - 206000, reduce_only=True),
+                   row(12, "filled", t1 + 3 * h, t1 + 3 * h, reduce_only=True),
+                   row(21, "filled", t2, t2 - 400), row(22, "filled", t2 + h, t2 + h, reduce_only=True),
+                   row(31, "open", t1 + 5 * h, t1 + 5 * h), row(31, "canceled", t1 + 6 * h, t1 + 5 * h),
+                   row(41, "open", t1 + 7 * h, t1 + 7 * h, reduce_only=True),
+                   row(51, "open", t1 + 8 * h, t1 + 8 * h, coin="xyz:CL"),
+                   row(61, "open", paper.day_start(d2) + h, paper.day_start(d2) + h)]
+        reads = []
+
+        def fake(body, limiter):
+            reads.append(body["type"])
+            if body["type"] == "historicalOrders":
+                return history if body["user"] == p else []
+            return [{"coin": "BTC", "px": "1", "sz": "1", "side": "B", "time": body["startTime"], "startPosition": "0",
+                     "tid": 9, "oid": {t2: 21, t2 + h: 22}[body["startTime"]]}]
+        paper.info = fake
+        root = os.path.join(tmp, "records", paper.RECORD_DIR)
+        w19_write(root, "episodes", d1, [
+            {"k": "ep", "a": p, "role": "pick", "coin": "BTC", "t_open": t1, "t_close": t1 + 3 * h, "oid_open": 11,
+             "oid_close": 12, "cut": False},
+            {"k": "ep", "a": p, "role": "pick", "coin": "BTC", "t_open": t2, "t_close": t2 + h, "cut": False},
+            {"k": "ep", "a": n, "role": "null", "coin": "BTC", "t_open": t1, "t_close": t1 + h, "cut": False}])
+        state = paper.new_state(sel)
+        state["written"]["episodes"] = d1
+        settled = paper.day_start(d2) + paper.DAY_SETTLE_S * 1000
+        paper.produce_orders(state, tmp, sel, None, set(sel["symbols"]), settled - 1)
+        s.check("a day is not written before it ended DAY_SETTLE_S ago", state["written"]["orders"] is None and reads == [])
+        paper.produce_orders(state, tmp, sel, None, set(sel["symbols"]), settled)
+        got = paper.read_jsonl(os.path.join(root, "orders", d1 + ".jsonl"))
+        s.check("orders/<day>.jsonl: the head, the two pick episodes, the day's nine copyable rows",
+                got[0] == {"k": "day", "date": d1, "episodes": 2, "rows": 9, "picks": {p: {"rows": 11, "complete": True}}}
+                and [x["k"] for x in got[1:]] == ["ep"] * 2 + ["row"] * 9)
+        s.check("an episode written before TZ-77 has its orders read at its fills' millisecond",
+                [(x["oid_open"], x["oid_close"]) for x in got[1:3]] == [(11, 12), (21, 22)]
+                and reads.count("userFillsByTime") == 2)
+        s.check("rows in status-time order, another coin's and another day's left out",
+                [(x["order"]["oid"], x["status"]) for x in got[3:]] == [
+                    (11, "open"), (12, "open"), (11, "filled"), (21, "filled"), (12, "filled"), (22, "filled"),
+                    (31, "open"), (31, "canceled"), (41, "open")] and all(x["a"] == p for x in got[3:]))
+        s.check("the next day waits for its episode file; one read of each pick per pass",
+                state["written"]["orders"] == d1 and reads.count("historicalOrders") == 1
+                and state["pending"] == ["orders/%s.jsonl" % d1])
+        paper.ORDERS_COMPLETE = 11
+        w19_write(os.path.join(tmp, "short", "records", paper.RECORD_DIR), "episodes", d1,
+                  paper.read_jsonl(os.path.join(root, "episodes", d1 + ".jsonl"))[1:])
+        short = paper.new_state(sel)
+        short["written"]["episodes"] = d1
+        paper.produce_orders(short, os.path.join(tmp, "short"), sel, None, set(sel["symbols"]), settled)
+        head = paper.read_jsonl(os.path.join(tmp, "short", "records", paper.RECORD_DIR, "orders", d1 + ".jsonl"))[0]
+        s.check("a full answer whose oldest row is inside the day: marked incomplete", head["picks"][p]["complete"] is False)
+        paper.ORDERS_COMPLETE = saved[1]
+
+        def refused(body, limiter):
+            raise paper.Transport("HTTP 429")
+        paper.info = refused
+        down = paper.new_state(sel)
+        down["written"]["episodes"] = d1
+        try:
+            paper.produce_orders(down, os.path.join(tmp, "down"), sel, None, set(sel["symbols"]), settled)
+            raised = False
+        except paper.Transport:
+            raised = True
+        s.check("a refused read writes nothing and the day waits", raised and down["written"]["orders"] is None)
+        # the readout, once the verdict and the window's last orders file are written
+        for d in ("2026-01-06", "2026-01-07"):
+            w19_write(root, "orders", d, [])
+        x_cell = {"src": {"gross": 50.0, "fee": 2.0}, "stop": {"gross": 40.0, "fee": 2.0}}
+        d_cell = {"src": {"gross": 30.0, "fee": 2.0}, "stop": {"gross": 20.0, "fee": 2.0}}
+        for d, lines in ((d1, [{"k": "book", "a": p, "coin": "BTC", "t_open": t1, "d": {str(x): d_cell for x in paper.DELAYS_S},
+                                "x": dict({str(x): x_cell for x in paper.DELAYS_S}, **{"7200": None})}]),
+                         ("2026-01-06", []), ("2026-01-07", [])):
+            w19_write(root, "book", d, lines)
+        rule = {"capital_usdt": 10000.0}
+        s.check("no readout before the verdict", not paper.produce_readout(state, tmp, sel, rule))
+        state["verdict"] = True
+        s.check("nor before the window's last orders file", not paper.produce_readout(state, tmp, sel, rule))
+        state["written"]["orders"] = "2026-01-07"
+        s.check("then once", paper.produce_readout(state, tmp, sel, rule) and not paper.produce_readout(state, tmp, sel, rule))
+        with open(os.path.join(root, "orders-readout.json"), encoding="utf-8") as fh:
+            out = json.load(fh)
+        s.check("the readout: one entry of two rested 206 s, one exit of two rested 3 h 3 min 26 s",
+                out["episodes"] == 2 and out["entry"] == {"known": 2, "rested": 1, "lead_s": {"p50": 206.0, "p95": 206.0}}
+                and out["exit"] == {"known": 2, "rested": 1, "lead_s": {"p50": 11006.0, "p95": 11006.0}})
+        s.check("the readout: two orders able to open rested, one opened no episode",
+                out["resting_entries"] == {"rested": 2, "opened_no_episode": 1})
+        s.check("the readout: the copy left at the pick's own exit against the delayed exit, gross less fees",
+                out["exit_copy"]["1800"] == {"n": 1, "at_pick_exit": {"src": 0.0048, "stop": 0.0038},
+                                             "at_delay": {"src": 0.0028, "stop": 0.0018}}
+                and out["exit_copy"]["7200"]["n"] == 0)
+    finally:
+        paper.info, paper.ORDERS_COMPLETE = saved
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
```
