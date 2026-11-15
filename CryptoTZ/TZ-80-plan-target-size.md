# TZ-80 — The plan the owner trades, and a look at the day still forming: every entry reaches him with its target, its size and his ceilings, the plan is scored apart from the rule, and at 15:10 UTC a stop reached, a target reached and each entry the close would make reach him with no model

**Canonical filename:** `CryptoTZ/TZ-80-plan-target-size.md`
**Report:** `CryptoReports/TZ-80-plan-target-size-report.md`
**Class:** branch TZ (contract §8) — it authorises seven repository files besides its report.
**Branch:** `claude/tz-80-plan-target-size`
**Host:** the VPS, for stage C; stages A–B run on any clone.
**Model:** Sonnet — the change is the patch of §10, written by the Architect and run by it under Python 3.11, 3.12 and
3.13 before this TZ shipped; the session applies it, proves its bytes and runs the validation. Nothing in it is
diagnosis or design.
**Trigger:** `EXECUTE TZ-80`, with nothing under it: no credential arrives and the Boss is asked for nothing.
**Previous TZ:** TZ-79, accepted 13.11.2026 and merged at `97145c1` (pull request #65); no branch on the remote is
ahead of `main`.
**Issued:** 15.11.2026, by the Architect. A first text under this number was handed to the Boss on 13.11.2026 and never
uploaded — no `CryptoTZ/TZ-80-*` and no report exist on the remote — so no execution began and this text replaces it
whole (the precedent is TZ-78).
**Written against:** contract v31, map `2026-11-13-a`, methodology `2026-10-26-a`, and `main` at `de3763c` — its
`vps` tree `07e379d51aa3ceab931917306525ff3d4a5a4878` — read from the repository on 15.11.2026.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-13-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-13-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `73. **An Architect-owned document never grows` |

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
| `vps/book.py` | 304 | `4b64b856fb80cfa810dcac015eb60b20` | equal, or A1 stops: §10 is written against these bytes |
| `vps/paper.py` | 1947 | `60018d258594aa629e6f8d5f0dc5c6d9` | equal, or A1 stops |
| `vps/score.py` | 317 | `308c8661b54d843a682747e46752bd4e` | equal, or A1 stops |
| `vps/selftest.py` | 3553 | `4816f38d10aa2711cc56fff29203c7a7` | equal, or A1 stops |
| `vps/manifest` | 10 | `73d8fd4022bcf24996d4d3c41c6444c5` | equal, or A1 stops |
| `vps/units/crypto-score.service` | 20 | `ca1e8d926d9ce2d9e2f2eabb4d7db41d` | reported: the look's service is this file with two lines changed |
| `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` | reported: the patch does not touch it and V5 copies it |
| `vps/writer.py` | 154 | `c07b1f71ef014e18448eb9313e185b73` | reported: the patch does not touch it and V5 copies it |

The map itself: 2802 lines, MD5 `9d10f8da578b060db902c286323bdde3` — reported, not enforced.

---

## 1. What changes, and the evidence for it

**The defect, found by the owner on the alert of 13.11.2026 at 04:10:** five entries, each with its fill and its stop,
and no target. The analysis has printed a target on every entry since methodology `2026-10-24-c` — half the position
closes at twice its risk and the rest's stop moves to the entry, the owner's request of 24.10.2026 — and TZ-79's alert
printed none: the owner was told two different trades for one entry, and the ledger scored the one he was not told to
trade. The same alert held seventeen shorts at once and named no size and no ceiling.

**The owner's request of 13.11.2026:** a second look at the market each day, near the United States open, that tells
him of new long and short candidates without his button.

**The evidence, measured by the Architect on 13–15.11.2026** on `data.binance.vision`, the 31 symbols of the payload's
list, fees, slippage and the actual funding, nothing fitted. Every state in it was made by production's own functions.

*The plan* — `vps/book.py --archive`, with and without `--scale 2`:

| Book, 2023-01-01 → 2026-10-22 | In sample (2023–24) | Out of sample (2025 →) | Largest drawdown |
|---|---|---|---|
| the rule as built | 228 trades, +222.79 R | 284 trades, −26.19 R | 54.93 R |
| the plan — half at 2 R, the rest's stop at the entry | 229 trades, +136.30 R | 291 trades, −16.97 R | 43.03 R |

These reproduce map §10's research of 24.10.2026 — +222.8, −26.0 and 54.9 R; +136.3, −16.8 and 43.0 R — with the
book's own `replay()`, so the plan this TZ builds is the plan that research measured. **The plan gives up two fifths of
the in-sample gain for a fifth less drawdown and a third less out-of-sample loss; no variant carries an edge out of
sample** (inv. 32). On BTC, ETH, SOL, BNB and XRP alone, to 2026-11-11, the plan read 45 trades and +18.13 R out of
sample, profit factor 1.92 and a drawdown of 5.04 R, against the rule's 44, +14.20 R, 1.71 and 7.02 R — a lead read
after the per-coin results were seen (map §10, row «The book's out-of-sample loss sits in the alts»): it orders the
alert's entries and decides nothing else.

*The look* — this TZ's `score.py --forming` and `score.py`, run one after the other on every day from 2023-03-01 to
2026-10-30, the day still forming rebuilt from the hourly klines as it stood at 15:00 UTC, only the transport
replaced:

| The look at 15:10 UTC, 1 340 days | Count |
|---|---:|
| entries it named as candidates | 339 |
| of them, entries the close made | 249 — 73 % |
| entries the close made in all | 536 — the look named 46 % of them |
| targets it told as reached | 106 — all 106 stood at the close |
| stops it told as reached | 197 |
| days it sent an alert | 339 |

Hour by hour, the share of candidates the close confirms rises from 57 % at 04:00 UTC to 73 % at 15:00, 82 % at 18:00
and 95 % at 23:00; an exit the close would make was right 74 times in 120 at 15:00. **Entering on the candidate
at 15:00 instead of at the next open** — the plan's own trade from the earlier price where the close confirms, out at
the next open where it does not — added +4.38 R to the plan in sample over 154 candidates and +10.49 R out of sample over
185: positive in both halves and inside their noise, so the look tells the owner what is coming and does
not tell him to enter.

*The entry's hour* — the plan's trades entered by market later on the entry day, the size as the alert states it,
while the stop was not reached: +128.19 to +141.45 R in sample against +134.48 at the open, and −27.89 to −8.10 R out of sample
against −23.44, for entries 2 to 16 hours late — no cost that grows with the hour.

*The stop's distance* — over the plan's 527 archive entries the stop stands a median 11.9 % from the entry;
24 stand beyond a quarter of it and 3 beyond a third, where an isolated position at 3x is closed by the
exchange before its stop.

**What is built — no model:**

1. **`vps/book.py`** — `replay(bars, open_now=None, scale=None)`: with `scale`, a day that reaches the entry plus
   `scale` times the initial risk, and does not reach the stop, closes half there — or at the open where the day opened
   beyond it — and the rest's stop moves to the entry from the next day on. `SCALE_R = 2.0`. `result_r()` prices such a
   trade. `levels()` gives a position of the plan its target and, once half has closed, the day, the price, the rest's
   stop and an open R with the closed half in it. `live_day()` returns the closed days and the day still forming;
   `state_of()` is the state of one symbol's bars; `--live --scale 2` and `--archive --scale 2` print the plan.
   **Without `scale` nothing the rule does or prints moves.**
2. **`vps/score.py`** — the daily close: one read of each symbol, the rule's and the plan's state from it, two
   ledgers, and an alert driven by the plan. `--forming`: the look. §3.
3. **`vps/paper.py`** — `ceilings(own)`, `copy_lev(dist)` and `copy_size(own, dist)`: the ceilings, the leverage and
   the size of one trade at the owner's medium risk, moved out of `copy_text()` so that the copy line and the book
   alert share them.
4. **`vps/selftest.py`** — section AB re-specified for the plan and the look, 62 checks to 117.
5. **`vps/units/crypto-score-forming.service`**, **`vps/units/crypto-score-forming.timer`** and one line of
   **`vps/manifest`** — the look, daily at 15:10 UTC.

*[Architect's decisions, TZ-80.* **The alert follows the plan, and the plan is what the gate reads,** because a
record of a trade the owner is not told to take measures nothing he does; the rule's ledger stays beside it as the
reference the archive is read against. **The look runs no model:** a model on a timer spends the limit the owner's
button needs, and map §10's row «The assistant's build sequence» keeps a run to that button; the look is the book's
arithmetic and costs nothing. **Its hour is 15:10 UTC — 19:10 in Tbilisi, the later of the two hours the owner
named.** Later is more accurate and farther from the United States open; the close's line counts every look, and that
count moves the hour, not an opinion. **A candidate carries no size, and no exit is told as a candidate:** nothing is
done about either before the close, and a line that changes no action is not printed. **The look is not persistent:**
a look not made at its hour is not made at another, or its count would mix hours. **The margin is stated at the
owner's lowest leverage, lowered where the stop is wide** — `copy_lev()`: one leverage less than the one whose whole
margin the distance to the stop would take. **The ceilings are stated, not applied:** the engine does not know what he
holds (owner's decision of 24.09.2026). **A day that reaches both the stop and the target is a stop,** and the moved
stop acts from the next day: the daily bar does not say which came first, and the stop-first reading is the one that
does not flatter the plan.*]*

---

## 2. Text this TZ obeys

- Contract §7 item 1: «**No change to scoring, leverage, liquidation or geometry math** unless the TZ explicitly cites a
  completed backtest» — none of the functions that item closes is touched, and neither is `index.html`. The plan's
  exit is geometry, and this TZ cites its completed backtest: map §10, row «The book prints no target», measured
  24.10.2026, and the Architect's re-run in §1. `copy_lev()` computes no liquidation price and decides no leverage of
  the calculator: it lowers the leverage at which two alerts STATE a margin, and §1's measurement of the stop's
  distance is what it stands on. The rule's path — `scale` left `None` — does not move, and section X proves it.
- Contract §7 item 2: «**Never edit a bench to make it pass.**» — the checks of section AB that read the alert, the
  record and the printed line are re-specified because this TZ changes what they assert. The Architect wrote every new
  expectation before execution and derived each in the check's own text; the session edits no check.
- Contract §7 item 15: «An implementation session never enables, starts or leaves running a persistent unit, timer or
  service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its report
  proves none is left behind.» — the look's timer is enabled by the deployer, from `main`, through the manifest.
- Map inv. 38: «**A second implementation of any rule, threshold or formula is banned in any language and any file.**»
  — one `replay()` makes the rule, the plan and the look's reading; the size, the leverage and the ceilings are
  `paper.py`'s, which the copy line now calls too; «A file once written is never reopened» — both ledgers and the
  look's record write a new file each.
- Map inv. 70: «**A transport failure is NOT an absence of data.**» — a span of funding prints that did not arrive whole
  prices nothing in either ledger; a symbol the look could not read is named unread and nothing is told of it.
- Map inv. 72: «**A write that fails leaves this run's product or nothing — never a partial file and never the previous
  run's.**» — every file is written by `common.atomic_write`.
- Map inv. 22: «**A check that passes with no data is forbidden.**» — V5 fails on `read=0`.

---

## 3. What the two runs do — registered

### The daily close — `score.py`, 00:10 UTC, TZ-79's timer

- **The plan's ledger** is `<state>/score-plan/`, one closed trade a file, under every rule TZ-79 gave
  `<state>/score-ledger/`, which keeps the rule's. A trade's `r` is `book.result_r()` of the plan's trade: half the move
  to the target and half the move to the exit, the whole position's funding up to the target's day and half of it
  after, the same costs. A failed read of the prints writes nothing in either ledger and prints
  `score: pending <ledger> <SYMBOL> <exception class>`.
- **An entry** prints two lines, the five symbols of `MAJORS` first and the others in the list's order: the side, the
  fill and the stop with its distance, and the entry's day where it is not today's; then the target with its distance
  and — where `analyst/owner.json` reads — the notional that loses the owner's medium risk at that stop, in USDT, and
  its margin at the leverage `paper.copy_lev()` names.
- **Under the entries**, once each: what the target means — «закрыть половину, стоп остатка перенести на вход;
  остаток — до сигнала «Выход сегодня»»; when to enter — «по рынку в течение дня, пока цена не дошла до стопа»; and,
  where the owner's file reads, his ceilings — `paper.ceilings()`, with «считайте вместе с открытыми».
- **A target reached** since the last record prints «Цель взята» with the price and the rest's stop. **An exit due**,
  **a close** with the plan's R, **the plan's record** — the five symbols apart — and **the open positions by side**
  follow as TZ-79 printed them.
- **The baseline** — the first run, or the first after a record of `v` 1, TZ-79's, which knew no plan — tells no close
  it fills, prints in full every entry made since that record's day, and prints every other open position on one line
  with its stop and target, or with «цель взята» and the rest's stop.
- **The record** is `v` 2: TZ-79's keys, `open` and `closed` now the plan's, `open` naming each position's target, the
  day its half closed and the rest's stop; a key `look` — `null`, or `{"named", "hit", "entries"}`: how many entries
  the look at the day that has just closed named, how many of them the close made, and how many the close made in
  all; and a key `rule` with the rule's open count, totals, `pending`, `late` and `disagree`.
- **The line** is `score: asof=… symbols=… read=… unread=… open=… opened=… scaled=… closing=… closed=… pending=…
  late=… disagree=… ledger=… rule=… look=… alert=yes|no` — the counts the plan's but `rule=`, the rule ledger's size;
  `look=` is `hit/named/entries`, or `-` where that day was not looked at.

### The look — `score.py --forming`, 15:10 UTC, a timer of its own

- **One read of each symbol**, `book.live_day()`: the closed days and the day still forming. The plan's state at the
  last close, and its state on the same days with the forming day appended as it stands — as if it closed at the last
  price. A symbol whose read fails, or whose forming day is not today's, is unread.
- **Told as it is:** a stop the day has reached — «Стоп сработал», with the price; a target it has reached — «Цель
  достигнута», with the price. Neither can be taken back, and the look moves no stop: the daily close does.
- **Told as a candidate:** each entry the close would make at the last price — «Кандидат в лонг» or «Кандидат в
  шорт», the last price, the level the close must hold beyond, and the stop and the target that entry would take,
  marked «≈»; the five symbols of `MAJORS` first. The alert then ends «Кандидат — ещё не сделка: его подтверждает
  только закрытие дня в 04:00, тогда придёт сообщение с точными числами».
- **No alert** where the day has done nothing and would open nothing. An exit the close would make is not told.
- **The look's record** is `<state>/score-forming/<YYYY-MM-DD>.json`, written once, after the alert, mode 0640: `v` 1,
  `k` `score-forming`, `ts`, `day`, `symbols`, `unread`, `stopped`, `scaled`, `entries` — the last a list of
  `{"symbol", "side"}`. **A day that has its record is not looked at again:** the run prints
  `score: forming day=… already looked at, nothing written` and exits 0.
- **The look writes nothing else:** no ledger, no `score.json`, no trade.
- **The line** is `score: forming day=… symbols=… read=… unread=… stopped=… scaled=… entries=… alert=yes|no`. Exit 0;
  exit 4 with `… read=0 nothing written` where no symbol was read.
- **The units:** `crypto-score-forming.service` is `crypto-score.service` with its description and
  `ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/score.py --forming`; `crypto-score-forming.timer` fires at
  `OnCalendar=*-*-* 15:10:00 UTC`, carries no `Persistent=`, and is the manifest's eleventh line.

### What does not move

TZ-79's timer and units, `GO_LIVE`, `RETRY_DAYS`, the funding reads, and the rule: `book.py --live` without `--scale`
prints what it printed, key for key. The copy line of `paper.py` prints what it printed for every copy whose stop
stands within a quarter of its entry; beyond that its margin is stated at 2x, and beyond a third at 1x.

---

## 4. Scope

### Files to Create
- `vps/units/crypto-score-forming.service`, `vps/units/crypto-score-forming.timer` — §10.

### Files to Modify
- `vps/book.py`, `vps/paper.py`, `vps/score.py`, `vps/selftest.py`, `vps/manifest` — §10.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
The scratch directory `/var/lib/crypto-auto/tz80` and the transient units of V5, all gone before the report. Nothing
under `/var/lib/crypto-auto` but that directory is written, no unit is created, changed, enabled or restarted, and the
bot's outbox receives nothing from this session: the plan and the look take effect when the deployer installs the merge.

### Not touched
`index.html`, `main.py`, every other unit, `bench.yml`, `analyst/**`, the map, the contracts.

---

## 5. Stages

### Stage A — readings, no writes
- **A0.** Contract §4a steps 1–6; the gate of §0, every anchor cut from the map's own table.
- **A1.** The added files of §0 at their lines and MD5. A difference in any of the five files §10 modifies stops the
  TZ, BLOCKED, naming the file.
- **A2.** On the VPS, the baseline from `main`: `python3 vps/selftest.py` prints `selftest: sections 28 checks 724
  failed 0 empty 0`, `section AB: checks 62 failed 0` and `section W: checks 204 failed 0`. *Measured by the Architect
  on `de3763c`'s tree.* A different baseline is recorded per section and the TZ goes on.
- **A3.** `python3 -c "import json; d=json.load(open('/var/lib/crypto-auto/score.json')); print(d['v'], d['asof'])"`,
  `ls /var/lib/crypto-auto/score-ledger | wc -l`, `test -e /var/lib/crypto-auto/score-plan; echo $?`,
  `test -e /var/lib/crypto-auto/score-forming; echo $?` and `systemctl list-timers --all --no-legend | grep -c
  crypto-score`, kept for V7. *Expected:* `1` and a date, a count, `1`, `1`, and `1` — TZ-79's record and timer, no
  plan ledger and no look.

### Stage B — the code, on the branch
- **B1.** Branch `claude/tz-80-plan-target-size` from `origin/main`. Extract §10's patch with the one command

  ```sh
  awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-80-plan-target-size.md > /tmp/tz80.patch
  ```

  and record its lines and MD5 — 1404 and `2fe51ecd677d5f4ac18825c85072cb2f` as written; an upload that strips the patch's
  blank context lines changes the hash and not the result, which B2 decides.
- **B2.** `git apply /tmp/tz80.patch`. **Required:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/book.py` | 354 | `33c764fa584507fa8a6a121a18f571d8` |
  | `vps/manifest` | 11 | `0a2518c1fc7fd989ef2dfd8aa770beef` |
  | `vps/paper.py` | 1967 | `f6970999e177fae27bfa78ef9d252b17` |
  | `vps/score.py` | 528 | `91503ec6cecb05d094dc0b8ff47a7889` |
  | `vps/selftest.py` | 3882 | `5963c21b6c869b49d9a151b3aeac0ce7` |
  | `vps/units/crypto-score-forming.service` | 20 | `6c1e8efc1b969929351a9276906139e8` |
  | `vps/units/crypto-score-forming.timer` | 9 | `2ab7dda47812ca79212c74e49cf14c18` |

  Any other result is BLOCKED: the patch did not arrive as written, and no hand edit replaces it.
- **B3.** Commit with §7's implementation message, **locally, before stage C**. Not pushed yet.

### Stage C — validation, on the VPS, on the committed branch
§6, in full.

### Stage D — push, pull request, report
Push; a pull request to `main` titled `TZ-80: vps — the plan the owner trades, and the look`, its body naming this
TZ, or the contract's §8 fallback. Then the report.

---

## 6. Validation

- **V1. Syntax.** `python3 -m py_compile vps/book.py vps/paper.py vps/score.py vps/selftest.py` — exit 0.
- **V2. The bytes.** B2's seven files at B2's lines and MD5s; and

  ```sh
  python3 -c "print(sum(0x400 <= ord(c) <= 0x4ff for f in ('vps/book.py', 'vps/score.py') for c in open(f, encoding='utf-8').read()))"
  ```

  prints `0`.
- **V3. Selftest**, on the VPS, on the branch: `python3 vps/selftest.py` — exit 0, `selftest: sections 28 checks
  779 failed 0 empty 0`, `section AB: checks 117 failed 0`, `section W: checks 204 failed 0`,
  `section X: checks 19 failed 0`, **every other section's count equal to A2's**. *Measured by the Architect under
  Python 3.11, 3.12 and 3.13.*
- **V4. Negative controls** (inv. 22). Extract §9's script with the one command

  ```sh
  awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-80-plan-target-size.md > /tmp/tz80-controls.py
  ```

  — 80 lines, MD5 `e652d6c9672fc0b62ce494066aa64f1a` as written — and run `python3 /tmp/tz80-controls.py` from the clone's
  root. **Required:** exactly the 147 lines §9 prints after the script — MD5 `74f92aa4687831cb7da67cec6ffd7e15` — and then
  `git status --porcelain` prints nothing. *Measured by the Architect under Python 3.11, 3.12 and 3.13, the three
  outputs identical.*
- **V5. The exchange, read from this machine, on a copy of the live state.** As root:

  ```sh
  install -d -o cryptoauto -g cryptoauto -m 0750 /var/lib/crypto-auto/tz80 /var/lib/crypto-auto/tz80/vps \
      /var/lib/crypto-auto/tz80/state /var/lib/crypto-auto/tz80/outbox /var/lib/crypto-auto/tz80/analyst
  install -o cryptoauto -g cryptoauto -m 0640 vps/*.py /var/lib/crypto-auto/tz80/vps/
  install -o cryptoauto -g cryptoauto -m 0640 analyst/owner.json /var/lib/crypto-auto/tz80/analyst/
  install -o cryptoauto -g cryptoauto -m 0640 index.html /var/lib/crypto-auto/tz80/
  cp -a /var/lib/crypto-auto/score.json /var/lib/crypto-auto/score-ledger /var/lib/crypto-auto/tz80/state/
  ls -li --time-style=full-iso /var/lib/crypto-auto/tz80/state/score-ledger > /tmp/tz80-rule-before.txt
  run80() { systemd-run --wait --collect --pipe --uid=cryptoauto --gid=cryptoauto -p ProtectSystem=strict \
      -p ReadWritePaths=/var/lib/crypto-auto/tz80 -p MemoryMax=64M -p Environment=PYTHONDONTWRITEBYTECODE=1 \
      /usr/bin/python3 /var/lib/crypto-auto/tz80/vps/score.py \
      --state /var/lib/crypto-auto/tz80/state --outbox /var/lib/crypto-auto/tz80/outbox "$@"; }
  run80; run80; run80 --forming; run80 --forming
  ```

  The scratch tree carries every program of `vps/` — `score.py` imports `paper.py`, which imports `announce.py` and
  `exchange.py` — and `index.html` and `analyst/owner.json` beside it, so the program reads the list and the owner's
  file there; the unit can write nothing but the scratch directory. **Required, by shape:**
  - *the first run:* exit 0; the last line printed is §3's line with `symbols=31`, `read` at least 1 (inv. 22),
    `asof` the UTC day before the run, `look=-` and `alert=yes`; exactly one file in the scratch outbox, of kind
    `alert`, whose first line carries «СДЕЛКИ ПРАВИЛА — подключено»; every line of it that names an entry with «вход»
    is followed by a line beginning «🎯 цель» that carries «объём» and «маржа»; `state/score.json` parses with `v` 2,
    a key `rule` and a key `look` that is `null`; `state/score-plan` holds as many files as the line's `ledger=`, each
    parsing to the ten keys of TZ-79 §3; and every file listed in `/tmp/tz80-rule-before.txt` is in the rule ledger
    after the run with the same inode and modification time;
  - *the second:* `opened=0 scaled=0 closing=0 closed=0 alert=no` and no second file in the scratch outbox;
  - *the third, the look:* exit 0; one line, §3's, with `symbols=31` and `read` at least 1;
    `state/score-forming/<today, UTC>.json` parses to the nine keys of §3 in their order; the scratch outbox holds one
    more file exactly where the line reads `alert=yes`, its first line carrying «СНИМОК ДНЯ»; and `state/score.json`,
    `state/score-plan` and `state/score-ledger` are byte for byte what the second run left;
  - *the fourth:* exit 0, the one line `score: forming day=<today> already looked at, nothing written`, and no new
    file anywhere under the scratch directory.

  The report quotes every line the four runs printed and the text of every alert in full — the first message the owner
  receives after the merge differs from the first run's only by the day. Then, once, from the scratch tree as
  `cryptoauto`: `python3 /var/lib/crypto-auto/tz80/vps/book.py --live --scale 2 BTCUSDT ETHUSDT` — two lines, each
  carrying `target` where its state is `long` or `short` — and the same command without `--scale 2` — two lines,
  neither carrying `target`; the report quotes the four. Then `rm -r /var/lib/crypto-auto/tz80`, and
  `systemctl list-units --all --no-legend 'run-*'` shows no unit of this session.
- **V6. The units.** `systemd-analyze verify vps/units/crypto-score-forming.service
  vps/units/crypto-score-forming.timer` — exit 0 and no output; and `systemd-analyze verify vps/units/*` — exit 0, as
  the installer requires before it installs anything.
- **V7. Scope.** `git diff --numstat origin/main...HEAD` prints exactly seven lines, tab-separated:

  ```text
  71	21	vps/book.py
  1	0	vps/manifest
  24	4	vps/paper.py
  305	94	vps/score.py
  390	61	vps/selftest.py
  20	0	vps/units/crypto-score-forming.service
  9	0	vps/units/crypto-score-forming.timer
  ```
- **V8. Nothing in effect before the merge.** A3's five commands again: `1` and a date, a count, `1`, `1`, and `1` —
  the live record is still TZ-79's, no plan ledger and no look exist, and one score timer is known to systemd. The day
  in the first line may have moved, if the timer ran during the session; the report says so.
- **V9. `bench.yml`.** `index.html` and `main.py` are untouched, so the standing checks do not apply; the report names
  the workflows that ran on the branch, from the runner where the session can.

**No regression:** every section but AB keeps A2's count, green (V3) — W's 204 among them, with the copy line on the
shared functions, and X's 19, with the rule's replay unchanged — and no file outside §4 moves (V7).

---

## 7. Commit Message

Implementation: `TZ-80: vps — the plan the owner trades, and a look at the day still forming: every entry with its target, its size and his ceilings, the plan scored apart from the rule, and at 15:10 UTC what the day has done and each entry its close would make`

Report: `TZ-80: report — the plan the owner trades, and the look`

---

## 8. The report

Contract §10 in full. Beside it: B1's command and the patch's lines and MD5; B2's lines and MD5s; A2's and V3's
per-section counts side by side; V4's output verbatim; V5's commands, every line they printed and every alert's text;
V6's two commands and their exit codes; A3's and V8's readings. The map's rows are the Architect's to update after the
audit, not this TZ's.

---

## 9. The controls script (V4)

```python
#!/usr/bin/env python3
"""TZ-80, V4: twenty-one negative controls. Each is one exact string replaced in one file of the working tree,
the selftest run, the file restored and its digest compared. Run from the repository root, on the branch."""
import hashlib
import subprocess
import sys

CONTROLS = (
    ("vps/book.py", "                    pos.update(t_scale=t, k_scale=k, stop_now=pos[\"entry\"],\n",
     "                    pos.update(t_scale=t, k_scale=k, stop_now=pos[\"stop\"],\n"),
    ("vps/book.py", "                   + 0.5 * sum(r for t, r in funding if tr[\"t_scale\"] < t <= tr[\"t_exit\"]))\n",
     "                   + sum(r for t, r in funding if tr[\"t_scale\"] < t <= tr[\"t_exit\"]))\n"),
    ("vps/book.py", "    trades, pos = replay(bars, open_now, scale)\n", "    trades, pos = replay(bars, open_now)\n"),
    ("vps/book.py", "                    pos[\"target\"] = entry + side * scale * STOP_ATR * a\n",
     "                    pos[\"target\"] = entry + side * (scale + 1) * STOP_ATR * a\n"),
    ("vps/score.py", "    fresh = baseline or asof > prev_asof\n", "    fresh = True\n"),
    ("vps/score.py", "            if key in known:\n", "            if key in known and False:\n"),
    ("vps/score.py", "            if day(tr[\"t_exit\"]) < floor:\n", "            if False:\n"),
    ("vps/score.py", "    if not inside or any(b - a > FUNDING_GAP_MS for a, b in zip(edges, edges[1:])):\n",
     "    if not inside:\n"),
    ("vps/score.py", "            if day(tr[\"t_entry\"]) < GO_LIVE:\n", "            if day(tr[\"t_exit\"]) < GO_LIVE:\n"),
    ("vps/score.py", "    scaled = [] if baseline else [o for o in open_rows if fresh and o.get(\"scale_date\", \"\") > prev_asof]\n",
     "    scaled = [] if baseline else [o for o in open_rows if fresh and o.get(\"scale_date\", \"\") >= prev_asof]\n"),
    ("vps/score.py", "    for o in majors_first(opened):\n", "    for o in opened:\n"),
    ("vps/score.py", "    baseline = prev_asof is None or prev_v != 2\n", "    baseline = prev_asof is None\n"),
    ("vps/paper.py", "    return int(round(own[\"side_max_pct\"] / own[\"risk_pct\"], 9)), int(round(own[\"book_max_pct\"] / own[\"risk_pct\"], 9))\n",
     "    return int(round(own[\"side_max_pct\"] / own[\"risk_pct\"], 9)) + 1, int(round(own[\"book_max_pct\"] / own[\"risk_pct\"], 9))\n"),
    ("vps/paper.py", "    return max(1, min(COPY_LEV, int(1 / dist) - 1))\n", "    return COPY_LEV\n"),
    ("vps/score.py", "    if os.path.exists(path):\n", "    if False:\n"),
    ("vps/score.py", "            then, trades, _ = book.state_of(symbol, bars + [today], today[4], book.SCALE_R)\n",
     "            then, trades, _ = book.state_of(symbol, bars, today[4], book.SCALE_R)\n"),
    ("vps/score.py", "            if day(today[0]) != day_now:\n", "            if False:\n"),
    ("vps/score.py", "                    if tr[\"t_exit\"] == today[0] and tr[\"why\"] == \"stop\"]\n",
     "                    if tr[\"why\"] == \"stop\"]\n"),
    ("vps/score.py", "    if len(unread) == len(symbols):\n", "    if False:\n"),
    ("vps/score.py", "{\"named\": len(named), \"hit\": len(named & due), \"entries\": len(due)}\n",
     "{\"named\": len(named), \"hit\": len(named), \"entries\": len(due)}\n"),
    ("vps/score.py", "        if then[\"entry_due\"]:         # the level the close must cross is the last close's trigger\n",
     "        if then[\"entry_due\"] and now.get(\"state\") == \"flat\":\n"),
)


def md5(path):
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def selftest():
    return subprocess.run([sys.executable, "vps/selftest.py"], capture_output=True, text=True)


def main():
    for number, (path, old, new) in enumerate(CONTROLS, 1):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        digest = md5(path)
        if text.count(old) != 1:
            print("CONTROL %d %s: the string occurs %d times, nothing run" % (number, path, text.count(old)))
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new))
        try:
            run = selftest()
        finally:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        print("CONTROL %d %s exit=%d restored=%s" % (number, path, run.returncode, "yes" if md5(path) == digest else "NO"))
        print("  " + run.stdout.strip().splitlines()[-1])
        for line in run.stdout.splitlines():
            if line.startswith("section ") and not line.endswith(" failed 0"):
                print("  " + line)
        for line in run.stderr.splitlines():
            if line.startswith("FAIL"):
                print("  " + line)
    run = selftest()
    print("FINAL exit=%d %s" % (run.returncode, run.stdout.strip().splitlines()[-1]))


if __name__ == "__main__":
    main()
```

Its required output:

```text
CONTROL 1 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 8 empty 0
  section AB: checks 117 failed 8
  FAIL section AB: the day the target is reached: one alert, half closed at 113.8 and the rest's stop at the entry
  FAIL section AB: record's open position after the target: its day, the stop now at the entry, half its R banked
  FAIL section AB: after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop
  FAIL section AB: the close after it tells the target with the rest's stop, which the look does not move
  FAIL section AB: a day that has reached the rest's stop at the entry: told as done, at 105
  FAIL section AB: the plan's trade: half at the target the day it is reached, its stop the initial one
  FAIL section AB: after the target, a day through the entry closes the rest at the entry; its R is half the target's
  FAIL section AB: --live --scale 2 prints the plan's state: the target's day and the stop at the entry
CONTROL 2 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: the plan's R: half the move to the target and half to the exit, the whole funding to the target's day and half after it
  FAIL section AB: the close is told with the plan's R, and the plan's record follows it
  FAIL section AB: the record totals the plan and the rule apart: one trade each, a null profit factor where nothing lost
CONTROL 3 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 668 failed 1 empty 0
  section AB: checks 6 failed 1
  FAIL section AB raised KeyError: 'target'
CONTROL 4 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 21 empty 0
  section AB: checks 117 failed 21
  FAIL section AB: baseline: the entry due today, two lines -- fill and stop 105 - 2 x 2.2; the target 105 + 2 x 4.4, and 150 USDT over 4.4 of 105 as 3580 USDT, 1193 of margin at 3x
  FAIL section AB: record's open position: the entry due, its stop and target, no open R, no target reached
  FAIL section AB: the day the target is reached: one alert, half closed at 113.8 and the rest's stop at the entry
  FAIL section AB: record's open position after the target: its day, the stop now at the entry, half its R banked
  FAIL section AB: a close below the 20-day low: the exit due today is told once, with no row yet
  FAIL section AB: the plan's R: half the move to the target and half to the exit, the whole funding to the target's day and half after it
  FAIL section AB: the close is told with the plan's R, and the plan's record follows it
  FAIL section AB: the record totals the plan and the rule apart: one trade each, a null profit factor where nothing lost
  FAIL section AB: after TZ-79's record: an entry since its day prints in full, with its target, the majors first
  FAIL section AB: after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop
  FAIL section AB: an entry without the owner's file: two lines, the target alone on the second, no size, no ceilings
  FAIL section AB: the look: a close below the 55-day low would open a short -- the last price, the level it crossed, the stop 2 x 2.15 above it and the target 4 x 2.15 below, BTC before the others
  FAIL section AB: the look: a close above the 55-day high would open a long -- the stop 2 x 2.1 below the last price, the target 4 x 2.1 above
  FAIL section AB: a day that has reached the target: told as done, half closing at 113.8, with no candidate's last line
  FAIL section AB: the close after it tells the target with the rest's stop, which the look does not move
  FAIL section AB: a day that has reached the rest's stop at the entry: told as done, at 105
  FAIL section AB: a day that opened beyond the short's stop and would close above the 55-day high: the stop told at the open, and the long a candidate with the stop 2 x 2.55 below the last price
  FAIL section AB: the plan's trade: half at the target the day it is reached, its stop the initial one
  FAIL section AB: the moved stop acts from the next day: the target's day reaching below the entry closes nothing more
  FAIL section AB: after the target, a day through the entry closes the rest at the entry; its R is half the target's
  FAIL section AB: --live --scale 2 prints the plan's state: the target's day and the stop at the entry
CONTROL 5 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: the exit due is not told twice on its day
CONTROL 6 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 4 empty 0
  section AB: checks 117 failed 4
  FAIL section AB: a written trade is neither written, told nor asked about again
  FAIL section AB: a replay that disagrees with a written trade: its file stands byte for byte, and is counted
  FAIL section AB: a file that stands is never reopened: the same inode and the same modification time
  FAIL section AB: a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told
CONTROL 7 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 2 empty 0
  section AB: checks 117 failed 2
  FAIL section AB: a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written and told
CONTROL 8 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: prints with a day missing inside the span: nothing written, the trade pending
  FAIL section AB: an answer that is not a list of prints: nothing written, the trade pending
  FAIL section AB: the prints read in three pages give the same R, and the late close is told once
CONTROL 9 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a trade entered before GO_LIVE is no file of the ledger
CONTROL 10 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: the target is told once: the next day says nothing
CONTROL 11 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: after TZ-79's record: an entry since its day prints in full, with its target, the majors first
  FAIL section AB: the day's entries print BTC ETH SOL BNB XRP first, then the others in the list's order
  FAIL section AB: the close after it: both candidates are entries, and the close counts the look -- 2 of 2 named, 2 made
CONTROL 12 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: after TZ-79's record: one alert under the baseline's head, the plan's closes filled and none told
  FAIL section AB: after TZ-79's record: the plan's record is in the score line, the legend once
  FAIL section AB: after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop
CONTROL 13 vps/paper.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 8 empty 0
  section W: checks 204 failed 6
  section AB: checks 117 failed 2
  FAIL section W: the open signal, character for character: the whale's facts and the copy sized at 0.5% of 30 000
  FAIL section W: the short open: red dot, the copy's stop above, whale 2, a short copy
  FAIL section W: a 10.7% stop sizes the copy at 1402 USDT, the third LONG of six
  FAIL section W: six open LONG signals already: the seventh is a skip
  FAIL section W: a full LONG side leaves a SHORT copy open
  FAIL section W: the copy line counts the account's open episodes, this one and the other picks'
  FAIL section AB: under an entry: what the target means, when to enter, the owner's ceilings, each once and in that order
  FAIL section AB: the ceilings are paper.ceilings: 3 % and 5 % at 0.5 % hold 6 and 10
CONTROL 14 vps/paper.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: the leverage is COPY_LEV while the stop stands within a quarter of the entry, 2x to a third, 1x beyond
  FAIL section AB: an entry whose stop stands 30 % away: 500 USDT, its margin 250 at 2x, since 3x would liquidate first
  FAIL section AB: the copy line's margin is the same function's: a copy whose stop is 30 % away is stated at 2x
CONTROL 15 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a day already looked at: exit 0, nothing read, nothing told, its record not reopened
CONTROL 16 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 13 empty 0
  section AB: checks 117 failed 13
  FAIL section AB: the look: the line reads day=1970-03-02 symbols=3 read=2 unread=1, two entries and nothing else, alert=yes
  FAIL section AB: the look: one alert, of kind alert, its head the day and the nine hours to its close
  FAIL section AB: the look: a close below the 55-day low would open a short -- the last price, the level it crossed, the stop 2 x 2.15 above it and the target 4 x 2.15 below, BTC before the others
  FAIL section AB: the look: a close above the 55-day high would open a long -- the stop 2 x 2.1 below the last price, the target 4 x 2.1 above
  FAIL section AB: the look: a candidate is named one, and the last line says the close alone confirms it
  FAIL section AB: the look's record: v 1, k score-forming, its day, the unread symbol, the entries it named with their sides
  FAIL section AB: the close after it: both candidates are entries, and the close counts the look -- 2 of 2 named, 2 made
  FAIL section AB: a stop of an earlier day is not the look's to tell, nor an entry made at today's open a candidate
  FAIL section AB: a candidate the close took back: no entry is told, and the close counts 0 of 1 named, 0 made
  FAIL section AB: a day that has reached the target: told as done, half closing at 113.8, with no candidate's last line
  FAIL section AB: a day that has reached the rest's stop at the entry: told as done, at 105
  FAIL section AB: an entry made at today's open and stopped today is a stop told, at 100.6
  FAIL section AB: a day that opened beyond the short's stop and would close above the 55-day high: the stop told at the open, and the long a candidate with the stop 2 x 2.55 below the last price
CONTROL 17 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 2 empty 0
  section AB: checks 117 failed 2
  FAIL section AB: an entry made at today's open and stopped today is a stop told, at 100.6
  FAIL section AB: a symbol whose forming day is not today is unread, and nothing of it is told
CONTROL 18 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a stop of an earlier day is not the look's to tell, nor an entry made at today's open a candidate
CONTROL 19 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: the look with no symbol read: exit 4, nothing written, nothing told
CONTROL 20 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a candidate the close took back: no entry is told, and the close counts 0 of 1 named, 0 made
CONTROL 21 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a day that opened beyond the short's stop and would close above the 55-day high: the stop told at the open, and the long a candidate with the stop 2 x 2.55 below the last price
FINAL exit=0 selftest: sections 28 checks 779 failed 0 empty 0
```

---

## 10. The patch

Against `main` at `de3763c`. B1 extracts the lines between the fences, and B2 applies them.

```diff
diff --git a/vps/book.py b/vps/book.py
index cfd9880..c7ecf00 100644
--- a/vps/book.py
+++ b/vps/book.py
@@ -16,6 +16,10 @@ The rules (Architect's decision, TZ-67, on the study of 20.10.2026):
   beyond the prior EXIT_N days' opposite extreme closes the trade at the next day's open, and the stop
   closes it intraday. No target and no time limit: the winners run.
 
+The plan the owner trades (TZ-80): the same entries, exits and stop, and in addition, where the price reaches
+SCALE_R times the initial risk from the entry, half the position closes there and the rest's stop moves to the
+entry. replay(..., scale=SCALE_R) makes the plan's trades and replay(...) the rule's, from one loop.
+
 Python 3.12's standard library only. Time is UTC everywhere.
 """
 import argparse
@@ -37,6 +41,9 @@ ATR_N = 20            # the average true range's window, in days
 STOP_ATR = 2.0        # the initial stop, in ATRs from the entry
 COST_SIDE = 0.001     # taker fee 0.05 % + slippage 0.05 %, a fraction of notional per side
 OOS_START = date(2025, 1, 1)
+# The plan's target, in R from the entry: the owner's request of 24.10.2026 and methodology 2026-10-24-c, measured
+# on the archive by the Architect on 24.10.2026 (map section 10, row "The book prints no target").
+SCALE_R = 2.0
 DAY_MS = 86_400_000
 HTTP_TIMEOUT_S = 20
 FAPI_KLINES = "https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1d&limit=400"
@@ -54,23 +61,33 @@ def atr(bars, k):
     return total / ATR_N
 
 
-def replay(bars, open_now=None):
+def replay(bars, open_now=None, scale=None):
     """bars: closed daily bars (t_open_ms, open, high, low, close), oldest first, one per UTC day.
     Returns (trades, position): each closed trade as a dict, and the open position after the last bar
     or None. A signal at day k's close fills at day k+1's open; a stop fills at the stop, or at the open
     when the day opened beyond it; a channel exit at day k's close fills at day k+1's open. A signal at
     the last bar's close fills at open_now, the open of the day still forming, and its position carries
-    entry_due; without open_now (the archive) that signal has no fill yet and opens nothing (TZ-68)."""
+    entry_due; without open_now (the archive) that signal has no fill yet and opens nothing (TZ-68).
+    With scale (TZ-80), a position carries its target, the entry plus scale times the initial risk; a day
+    that reaches it, and does not reach the stop, closes half at that price -- or at the open where the day
+    opened beyond it -- and sets the rest's stop to the entry from the next day on; the position and its
+    trade then carry t_scale and scale_px, and "stop" stays the initial stop, the one the trade's R is
+    measured in. Without scale no position carries a target and nothing here moves."""
     trades, pos = [], None
     for k in range(len(bars)):
         t, o, h, l, c = bars[k]
         if pos is not None and k >= pos["k_entry"]:
-            side, stop = pos["side"], pos["stop"]
+            side, stop = pos["side"], pos.get("stop_now", pos["stop"])
             if (side > 0 and l <= stop) or (side < 0 and h >= stop):
                 px = o if (side > 0 and o < stop) or (side < 0 and o > stop) else stop
                 trades.append(dict(pos, k_exit=k, t_exit=t, exit=px, why="stop"))
                 pos = None
-            elif k >= EXIT_N:
+            elif "target" in pos and "t_scale" not in pos:
+                tgt = pos["target"]
+                if (side > 0 and h >= tgt) or (side < 0 and l <= tgt):
+                    pos.update(t_scale=t, k_scale=k, stop_now=pos["entry"],
+                               scale_px=o if (side > 0 and o > tgt) or (side < 0 and o < tgt) else tgt)
+            if pos is not None and k >= EXIT_N:
                 lo = min(b[3] for b in bars[k - EXIT_N:k]); hi = max(b[2] for b in bars[k - EXIT_N:k])
                 if (side > 0 and c < lo) or (side < 0 and c > hi):
                     if k + 1 < len(bars):
@@ -89,12 +106,16 @@ def replay(bars, open_now=None):
                 t_entry, entry = bars[k + 1][:2] if k + 1 < len(bars) else (t + DAY_MS, open_now)
                 pos = dict(side=side, k_signal=k, k_entry=k + 1, t_entry=t_entry, entry=entry, atr=a,
                            stop=entry - side * STOP_ATR * a, entry_due=k + 1 == len(bars))
+                if scale:
+                    pos["target"] = entry + side * scale * STOP_ATR * a
     return trades, pos
 
 
 def levels(bars, pos):
     """What the next close decides, from the last closed bar: the trigger and the stop a new trade would
-    take, or the open position's exit level. A position whose entry is due has no open R yet."""
+    take, or the open position's exit level. A position whose entry is due has no open R yet. A position
+    of the plan (TZ-80) also carries its target and, once half has closed there, the day it did and the
+    stop the rest now stands on."""
     k = len(bars) - 1
     t, o, h, l, c = bars[k]
     a = atr(bars, k)
@@ -109,6 +130,13 @@ def levels(bars, pos):
                                else max(b[2] for b in bars[k - EXIT_N + 1:k + 1])),
                    r_open=None if pos.get("entry_due") else side * (c - pos["entry"]) / abs(pos["entry"] - pos["stop"]),
                    entry_due=bool(pos.get("entry_due")), exit_due=bool(pos.get("exit_due")))
+        if "target" in pos:
+            out.update(target=pos["target"])
+        if "stop_now" in pos:
+            risk = abs(pos["entry"] - pos["stop"])
+            out.update(stop_now=pos["stop_now"], scale_px=pos["scale_px"],
+                       scale_date=datetime.fromtimestamp(pos["t_scale"] / 1000, timezone.utc).strftime("%Y-%m-%d"),
+                       r_open=0.5 * side * (pos["scale_px"] - pos["entry"]) / risk + 0.5 * side * (c - pos["entry"]) / risk)
     elif k >= ENTRY_N - 1 and a:
         hi = max(b[2] for b in bars[k - ENTRY_N + 1:k + 1]); lo = min(b[3] for b in bars[k - ENTRY_N + 1:k + 1])
         out.update(long_trigger=hi, short_trigger=lo, long_stop=hi - STOP_ATR * a, short_stop=lo + STOP_ATR * a)
@@ -116,11 +144,19 @@ def levels(bars, pos):
 
 
 def result_r(tr, funding):
-    """A closed trade in R after fees, slippage and funding. funding: sorted list of (t_ms, rate)."""
+    """A closed trade in R after fees, slippage and funding. funding: sorted list of (t_ms, rate). A trade
+    that closed half at its target (TZ-80) gains half its move to the target and half its move to the exit,
+    pays the whole position's funding up to the day of the target and half of it after, and the same
+    costs, since it trades the same notional."""
     side, e, x = tr["side"], tr["entry"], tr["exit"]
     dist = abs(e - tr["stop"]) / e
-    paid = side * sum(r for t, r in funding if tr["t_entry"] < t <= tr["t_exit"])
-    return (side * (x / e - 1) - paid - 2 * COST_SIDE) / dist
+    if "t_scale" not in tr:
+        paid = side * sum(r for t, r in funding if tr["t_entry"] < t <= tr["t_exit"])
+        return (side * (x / e - 1) - paid - 2 * COST_SIDE) / dist
+    paid = side * (sum(r for t, r in funding if tr["t_entry"] < t <= tr["t_scale"])
+                   + 0.5 * sum(r for t, r in funding if tr["t_scale"] < t <= tr["t_exit"]))
+    gain = 0.5 * side * (tr["scale_px"] / e - 1) + 0.5 * side * (x / e - 1)
+    return (gain - paid - 2 * COST_SIDE) / dist
 
 
 def _get(url):
@@ -128,26 +164,39 @@ def _get(url):
         return r.read()
 
 
-def live_bars(symbol, now_ms):
-    """The closed daily bars, oldest first, and the open of the day still forming: the fill of a signal at
-    the last close. A read without that day is refused rather than replayed without it (TZ-68)."""
+def live_day(symbol, now_ms):
+    """The closed daily bars, oldest first, and the day still forming as a bar of its own, its close the last
+    price (TZ-80). A read without that day is refused rather than replayed without it (TZ-68)."""
     rows = json.loads(_get(FAPI_KLINES % symbol))
     bars = [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) < now_ms]
-    forming = [float(r[1]) for r in rows if int(r[6]) >= now_ms]
+    forming = [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) >= now_ms]
     if not forming:
         raise ValueError("the read holds no day still forming")
     return bars, forming[0]
 
 
-def live_state(symbol, now_ms):
-    """One symbol's state today and the replay behind it: (state, trades, position). The state is the object
-    --live prints, and a history of ENTRY_N days or fewer carries none but short-history (TZ-79)."""
-    bars, open_now = live_bars(symbol, now_ms)
-    trades, pos = replay(bars, open_now)
+def live_bars(symbol, now_ms):
+    """The closed daily bars, oldest first, and the open of the day still forming: the fill of a signal at
+    the last close (TZ-68)."""
+    bars, today = live_day(symbol, now_ms)
+    return bars, today[1]
+
+
+def state_of(symbol, bars, open_now, scale=None):
+    """One symbol's state on these bars and the replay behind it: (state, trades, position). A history of
+    ENTRY_N days or fewer carries none but short-history (TZ-79); scale makes the plan's (TZ-80)."""
+    trades, pos = replay(bars, open_now, scale)
     out = dict(symbol=symbol, **levels(bars, pos)) if len(bars) > ENTRY_N else dict(symbol=symbol, state="short-history")
     return out, trades, pos
 
 
+def live_state(symbol, now_ms, scale=None):
+    """One symbol's state today and the replay behind it: (state, trades, position). The state is the object
+    --live prints (TZ-79), the plan's with scale (TZ-80)."""
+    bars, open_now = live_bars(symbol, now_ms)
+    return state_of(symbol, bars, open_now, scale)
+
+
 def _csv_rows(blob):
     with zipfile.ZipFile(io.BytesIO(blob)) as z:
         for name in z.namelist():
@@ -246,14 +295,14 @@ def archive_paths(symbol, start, end):
     return paths
 
 
-def archive(symbols, start, end, cache, workers=8):
+def archive(symbols, start, end, cache, workers=8, scale=None):
     with concurrent.futures.ThreadPoolExecutor(workers) as ex:
         list(ex.map(lambda path: _archive_blob(path, cache),
                     [path for s in symbols for path in archive_paths(s, start, end)]))
     rows = []
     for s in symbols:
         bars, funding = archive_series(s, start, end, cache)
-        trades, _ = replay(bars)
+        trades, _ = replay(bars, scale=scale)
         for tr in trades:
             rows.append((tr["t_exit"], s, tr["side"], tr["t_entry"], result_r(tr, funding), tr["why"]))
     rows.sort()
@@ -274,6 +323,7 @@ def main(argv=None):
     ap.add_argument("--from", dest="start", default="2023-01-01")
     ap.add_argument("--to", dest="end", default=None)
     ap.add_argument("--cache", default=os.path.join(os.path.expanduser("~"), ".cache", "crypto-book"))
+    ap.add_argument("--scale", type=float, default=None, help="the plan: half closes at this many R (TZ-80)")
     ap.add_argument("symbols", nargs="+")
     a = ap.parse_args(argv)
     if a.live == a.archive:
@@ -282,14 +332,14 @@ def main(argv=None):
         now_ms = int(time.time() * 1000)
         for s in a.symbols:
             try:
-                out = live_state(s, now_ms)[0]
+                out = live_state(s, now_ms, a.scale)[0]
             except Exception as exc:          # one symbol's failure never hides the others
                 out = dict(symbol=s, state="unread", error=exc.__class__.__name__)
             print(json.dumps(out, sort_keys=True), flush=True)
         return 0
     os.makedirs(a.cache, exist_ok=True)
     end = date.fromisoformat(a.end) if a.end else (datetime.now(timezone.utc).date() - timedelta(days=2))
-    rows, out = archive(a.symbols, date.fromisoformat(a.start), end, a.cache)
+    rows, out = archive(a.symbols, date.fromisoformat(a.start), end, a.cache, scale=a.scale)
     for name, s in out.items():
         if not s["n"]:
             print("%-14s no trades" % name); continue
diff --git a/vps/manifest b/vps/manifest
index de95e23..0cf6795 100644
--- a/vps/manifest
+++ b/vps/manifest
@@ -8,3 +8,4 @@ crypto-stop.path
 crypto-paper.service
 crypto-etf.timer
 crypto-score.timer
+crypto-score-forming.timer
diff --git a/vps/paper.py b/vps/paper.py
index 10b4058..9298575 100644
--- a/vps/paper.py
+++ b/vps/paper.py
@@ -1178,19 +1178,39 @@ def exit_text(prices, entry, side):
     return text + (P_MORE.format(n=len(prices) - 1) if len(prices) > 1 else "")
 
 
+def ceilings(own):
+    """TZ-80: how many trades at the owner's medium risk his side ceiling and his book ceiling each hold -- the
+    copy line's and the book alert's alike (inv. 38)."""
+    return int(round(own["side_max_pct"] / own["risk_pct"], 9)), int(round(own["book_max_pct"] / own["risk_pct"], 9))
+
+
+def copy_lev(dist):
+    """TZ-80: the leverage a trade's margin is stated at -- COPY_LEV, or the highest below it at which a stop
+    dist of the entry away still stands inside the liquidation distance of one leverage more: an isolated
+    position must reach its stop before its liquidation."""
+    return max(1, min(COPY_LEV, int(1 / dist) - 1))
+
+
+def copy_size(own, dist):
+    """TZ-80: (notional, margin, leverage, risk) of one trade at the owner's medium risk whose stop stands dist
+    of the entry away -- the copy line's and the book alert's alike (inv. 38)."""
+    risk = risk_usdt(own["capital_usdt"], own["risk_pct"] / 100)
+    lev = copy_lev(dist)
+    return risk / dist, risk / dist / lev, lev, risk
+
+
 def copy_text(own, dist, side, sides):
     """TZ-78: the copy line -- sized as the test sizes, the owner's capital at his medium risk to the copy's stop; or
     a skip, where the open signals on its side or in all, this one counted, would pass his side or book ceiling,
     each holding as many copies as its ceiling holds his medium risk."""
     name, n_side, n_all = side_word(side), list(sides).count(side), len(sides)
-    cap_side = int(round(own["side_max_pct"] / own["risk_pct"], 9))
-    cap_all = int(round(own["book_max_pct"] / own["risk_pct"], 9))
+    cap_side, cap_all = ceilings(own)
     if n_side > cap_side:
         return P_SKIP_SIDE.format(side=name, n=n_side - 1, cap=cap_side, pct="%g" % own["side_max_pct"])
     if n_all > cap_all:
         return P_SKIP_BOOK.format(n=n_all - 1, cap=cap_all, pct="%g" % own["book_max_pct"])
-    risk = risk_usdt(own["capital_usdt"], own["risk_pct"] / 100)
-    return P_COPY.format(size="%d" % round(risk / dist), margin="%d" % round(risk / dist / COPY_LEV), lev=COPY_LEV,
+    size, margin, lev, risk = copy_size(own, dist)
+    return P_COPY.format(size="%d" % round(size), margin="%d" % round(margin), lev=lev,
                          risk=grouped(risk), pct="%g" % own["risk_pct"], capital=grouped(own["capital_usdt"]),
                          side=name, n=n_side, cap=cap_side)
 
diff --git a/vps/score.py b/vps/score.py
index 65a5012..617fc61 100644
--- a/vps/score.py
+++ b/vps/score.py
@@ -1,24 +1,40 @@
 #!/usr/bin/env python3
-"""The book's signal and its forward ledger (TZ-79): once a day, after the daily close, every entry and
-exit the trend book made on the list reaches the owner as one alert, and every trade the book has closed
-since it went into code is written once to a ledger that no later run rewrites. It runs no model and
-reads no credential.
+"""The book's signal and its forward ledger (TZ-79, TZ-80). It runs no model and reads no credential.
 
-    score.py [--state DIR] [--outbox DIR]     default /var/lib/crypto-auto and the bot's outbox
+    score.py [--state DIR] [--outbox DIR]              the daily close
+    score.py --forming [--state DIR] [--outbox DIR]    the look at the day still forming
 
-The book is book.live_state() and nothing else -- the function `book.py --live` prints from, on the same
-reads -- and a trade's result is book.result_r() on the funding prints the exchange publishes for its
-span. A trade whose prints did not arrive whole is not written: the next run asks again (map inv. 70).
+The daily close: every entry, target and exit of the plan the owner trades on the list reaches him as one
+alert -- each entry with its stop, its target and its size at his medium risk -- and every trade the plan and
+the rule have closed since the book went into code is written once to a ledger that no later run rewrites.
 
+The look: once a day, hours before the close, what the day has already done to the plan's positions -- a stop
+reached, a target reached -- and the entry its close would make if it came at the last price reach him as one
+alert, the entry named a candidate, because the close may still take it back. The look writes no ledger and
+opens no trade: the daily close alone does.
+
+The book is book.state_of() on one read of each symbol: the rule's state, which `book.py --live` prints, and
+the plan's, which `book.py --live --scale 2` prints; the look's is the plan's on the same bars with the day
+still forming appended as it stands. A trade's result is book.result_r() on the funding prints the exchange
+publishes for its span; a trade whose prints did not arrive whole is not written, and the next run asks again
+(map inv. 70). The size and the ceilings are the owner's, read from analyst/owner.json through paper.py
+(inv. 38).
+
+    score-plan/           the plan's ledger: one closed trade a file, as score-ledger/ below
     score-ledger/         one closed trade a file, <SYMBOL>-<entry stamp>.json, written once and within
                           RETRY_DAYS of its close, and never reopened (map inv. 38): a later replay that
                           reads its trade differently is counted, and a close found later than that is
                           counted and never written -- the replay's window slides, and the ledger takes
                           no file about a past it did not see
-    score.json            this run's reading: the day it stands on, the open positions, the totals
-
-Prints one line, and one before it for each trade it could not price; never a price. Exit 0 the reading is written · 4 no symbol was read, or the read is
-older than the record: nothing written · 5 a file of the ledger is not a trade: nothing written.
+    score-forming/        one look a file, <YYYY-MM-DD>.json, written once: what the look named, so that
+                          the next close counts how much of it came true; a day that has its file is not
+                          looked at again
+    score.json            the daily close's reading: the day it stands on, the plan's open positions, both
+                          totals, and the look's count for that day
+
+Prints one line, and one before it for each trade it could not price; never a price.
+Exit 0 the reading is written, or the day was already looked at · 4 no symbol was read, or the read is older
+than the record: nothing written · 5 a file of the ledger is not a trade: nothing written.
 """
 import argparse
 import json
@@ -31,6 +47,7 @@ from datetime import date, datetime, timedelta, timezone
 sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 import book  # noqa: E402
 import common  # noqa: E402
+import paper  # noqa: E402
 import writer  # noqa: E402
 
 # Methodology 2026-10-21-a: the first day every level the answer prints is this book's.
@@ -50,39 +67,88 @@ FUNDING_GAP_MS = 8 * 3600 * 1000 + 60 * 1000
 # 200 days 21, 0 and 0; at 120, 60 and 30 none, every trade equal to the full history's.
 RETRY_DAYS = 60
 LEDGER = "score-ledger"
+PLAN = "score-plan"
+FORMING = "score-forming"
 RECORD = "score.json"
 LEDGER_KEYS = ("symbol", "side", "t_entry", "entry", "stop", "t_exit", "exit", "why", "r", "seen")
 
 # The alert, in the owner's words; a number he may type prints as a code span (the bot of TZ-71).
-T_HEAD = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410** "
-          "\u00b7 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
-T_HEAD_BASE = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410 \u2014 "
-               "\u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043e** \u00b7 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
-T_OPEN = ("{dot} **\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u043a\u0440\u044b\u043b\u043e {side}:** "
-          "{sym} \u00b7 \u0432\u0445\u043e\u0434 `{entry}` \u00b7 \u0441\u0442\u043e\u043f `{stop}` ({dist}%)")
+T_HEAD = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410** \u00b7 "
+          "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
+T_HEAD_BASE = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410 "
+               "\u2014 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043e** \u00b7 "
+               "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
+T_ENTRY = ("{dot} **{side} {sym}** \u00b7 \u0432\u0445\u043e\u0434 `{entry}` \u00b7 \u0441\u0442\u043e\u043f "
+           "`{stop}` ({dist}%)")
 T_LATE = " \u00b7 \u0432\u0445\u043e\u0434 \u0431\u044b\u043b {date}"
-T_CLOSING = ("\U0001f6aa **\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u0432\u044b\u0445\u043e\u0434\u0438\u0442 \u0441\u0435\u0433\u043e\u0434\u043d\u044f:** "
-             "{sym} {side} \u2014 \u043f\u043e \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f")
-T_CLOSED = ("\u2705 **\u0421\u0434\u0435\u043b\u043a\u0430 "
-            "\u0437\u0430\u043a\u0440\u044b\u0442\u0430:** {sym} {side} \u2014 {why} \u00b7 **{r} R**")
-T_SCORE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u043e "
-           "**{n}** \u00b7 **{total} R** \u00b7 \u0432 \u043f\u043b\u044e\u0441\u0435 {wins}")
-T_SCORE_NONE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u044b\u0445 "
-                "\u0441\u0434\u0435\u043b\u043e\u043a \u043f\u043e\u043a\u0430 \u043d\u0435\u0442")
+T_PLAN = "\U0001f3af \u0446\u0435\u043b\u044c `{target}` ({tdist}%)"
+T_PLAN_SIZE = (" \u00b7 \u043e\u0431\u044a\u0451\u043c `{notional}` USDT \u00b7 \u043c\u0430\u0440\u0436\u0430 "
+               "`{margin}` \u043f\u0440\u0438 {lev}x")
+T_SCALED = ("\U0001f3af **\u0426\u0435\u043b\u044c \u0432\u0437\u044f\u0442\u0430:** {sym} {side} \u2014 "
+            "\u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0430 "
+            "\u043f\u043e `{px}`, \u0441\u0442\u043e\u043f \u043e\u0441\u0442\u0430\u0442\u043a\u0430 "
+            "\u0442\u0435\u043f\u0435\u0440\u044c `{stop}`")
+T_CLOSING = ("\U0001f6aa **\u0412\u044b\u0445\u043e\u0434 \u0441\u0435\u0433\u043e\u0434\u043d\u044f:** {sym} "
+             "{side} \u2014 \u043f\u043e \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f")
+T_CLOSED = ("\u2705 **\u0421\u0434\u0435\u043b\u043a\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0430:** {sym} "
+            "{side} \u2014 {why} \u00b7 **{r} R**")
+T_SCORE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u043e **{n}** "
+           "\u00b7 **{total} R** \u00b7 \u0432 \u043f\u043b\u044e\u0441\u0435 {wins}")
+T_SCORE_NONE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: "
+                "\u0437\u0430\u043a\u0440\u044b\u0442\u044b\u0445 \u0441\u0434\u0435\u043b\u043e\u043a "
+                "\u043f\u043e\u043a\u0430 \u043d\u0435\u0442")
 T_GROUPS = ("BTC ETH SOL BNB XRP: {n1} \u00b7 {r1} R \u00b7 "
             "\u043e\u0441\u0442\u0430\u043b\u044c\u043d\u044b\u0435: {n2} \u00b7 {r2} R")
-T_OPEN_NOW = ("\u0412 \u0441\u0434\u0435\u043b\u043a\u0435 {n}: \u043b\u043e\u043d\u0433 {nl} \u00b7 \u0448\u043e\u0440\u0442 "
-              "{ns} \u00b7 \u043f\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f {r} R")
-T_HELD = "\u041c\u043e\u043d\u0435\u0442\u044b: {rows}"
-T_LEGEND = ("R \u2014 \u043e\u0434\u0438\u043d \u0440\u0438\u0441\u043a "
-            "\u043d\u0430 \u0441\u0434\u0435\u043b\u043a\u0443.")
-T_FOOT = ("\u0420\u0430\u0437\u043c\u0435\u0440 \u0438 \u043f\u043b\u0435\u0447\u043e \u2014 "
-          "\u043a\u043d\u043e\u043f\u043a\u043e\u0439 \u0430\u043d\u0430\u043b\u0438\u0437\u0430.")
+T_OPEN_NOW = ("\u0412 \u0441\u0434\u0435\u043b\u043a\u0435 {n}: \u043b\u043e\u043d\u0433 {nl} \u00b7 "
+              "\u0448\u043e\u0440\u0442 {ns} \u00b7 \u043f\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044e "
+              "\u0434\u043d\u044f {r} R")
+T_HELD = ("{dot} **{side} {sym}** \u00b7 \u0441\u0442\u043e\u043f `{stop}` \u00b7 \u0446\u0435\u043b\u044c "
+          "`{target}`")
+T_HELD_DONE = ("{dot} **{side} {sym}** \u00b7 \u0446\u0435\u043b\u044c \u0432\u0437\u044f\u0442\u0430 \u00b7 "
+               "\u0441\u0442\u043e\u043f \u043e\u0441\u0442\u0430\u0442\u043a\u0430 `{stop}`")
+T_HOW = ("\u0426\u0435\u043b\u044c: \u0437\u0430\u043a\u0440\u044b\u0442\u044c "
+         "\u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0443, \u0441\u0442\u043e\u043f "
+         "\u043e\u0441\u0442\u0430\u0442\u043a\u0430 \u043f\u0435\u0440\u0435\u043d\u0435\u0441\u0442\u0438 "
+         "\u043d\u0430 \u0432\u0445\u043e\u0434; \u043e\u0441\u0442\u0430\u0442\u043e\u043a \u2014 \u0434\u043e "
+         "\u0441\u0438\u0433\u043d\u0430\u043b\u0430 \u00ab\u0412\u044b\u0445\u043e\u0434 "
+         "\u0441\u0435\u0433\u043e\u0434\u043d\u044f\u00bb.")
+T_WHEN = ("\u0412\u0445\u043e\u0434 \u2014 \u043f\u043e \u0440\u044b\u043d\u043a\u0443 \u0432 "
+          "\u0442\u0435\u0447\u0435\u043d\u0438\u0435 \u0434\u043d\u044f, \u043f\u043e\u043a\u0430 "
+          "\u0446\u0435\u043d\u0430 \u043d\u0435 \u0434\u043e\u0448\u043b\u0430 \u0434\u043e "
+          "\u0441\u0442\u043e\u043f\u0430.")
+T_LIMIT = ("\u26a0\ufe0f \u0412\u0430\u0448 \u043b\u0438\u043c\u0438\u0442: {side_n} "
+           "\u0441\u0434\u0435\u043b\u043e\u043a \u0432 \u043e\u0434\u043d\u0443 "
+           "\u0441\u0442\u043e\u0440\u043e\u043d\u0443 \u0438 {book_n} \u0432\u0441\u0435\u0433\u043e, "
+           "\u043a\u0430\u0436\u0434\u0430\u044f \u0434\u043e \u2212{risk} USDT \u2014 "
+           "\u0441\u0447\u0438\u0442\u0430\u0439\u0442\u0435 \u0432\u043c\u0435\u0441\u0442\u0435 \u0441 "
+           "\u043e\u0442\u043a\u0440\u044b\u0442\u044b\u043c\u0438.")
+T_LEGEND = ("R \u2014 \u043e\u0434\u0438\u043d \u0440\u0438\u0441\u043a \u043d\u0430 "
+            "\u0441\u0434\u0435\u043b\u043a\u0443.")
+# The look at the day still forming (TZ-80): what has happened is told as it is, what the close may still
+# take back is told as a candidate.
+F_HEAD = ("\u23f1 **\u0421\u041d\u0418\u041c\u041e\u041a \u0414\u041d\u042f** \u00b7 {d} \u00b7 \u0434\u043e "
+          "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0434\u043d\u044f {h} \u0447")
+F_STOP = ("\u26d4 **\u0421\u0442\u043e\u043f \u0441\u0440\u0430\u0431\u043e\u0442\u0430\u043b:** {sym} {side} "
+          "\u2014 \u043f\u043e `{px}`")
+F_SCALE = ("\U0001f3af **\u0426\u0435\u043b\u044c \u0434\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442\u0430:** "
+           "{sym} {side} \u2014 \u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0430 "
+           "\u0437\u0430\u043a\u0440\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u043f\u043e `{px}`")
+F_ENTRY = ("\u23f3 **\u041a\u0430\u043d\u0434\u0438\u0434\u0430\u0442 \u0432 {side}:** {sym} \u00b7 "
+           "\u0441\u0435\u0439\u0447\u0430\u0441 `{last}`")
+F_LEVEL = " \u00b7 \u0443\u0440\u043e\u0432\u0435\u043d\u044c `{level}`"
+F_ENTRY_PLAN = "\u0441\u0442\u043e\u043f \u2248 `{stop}` \u00b7 \u0446\u0435\u043b\u044c \u2248 `{target}`"
+F_FOOT = ("\u041a\u0430\u043d\u0434\u0438\u0434\u0430\u0442 \u2014 \u0435\u0449\u0451 \u043d\u0435 "
+          "\u0441\u0434\u0435\u043b\u043a\u0430: \u0435\u0433\u043e "
+          "\u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u0435\u0442 "
+          "\u0442\u043e\u043b\u044c\u043a\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 "
+          "\u0434\u043d\u044f \u0432 04:00, \u0442\u043e\u0433\u0434\u0430 \u043f\u0440\u0438\u0434\u0451\u0442 "
+          "\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u0441 "
+          "\u0442\u043e\u0447\u043d\u044b\u043c\u0438 \u0447\u0438\u0441\u043b\u0430\u043c\u0438.")
 SIDE = {1: "\u043b\u043e\u043d\u0433", -1: "\u0448\u043e\u0440\u0442"}
+SIDE_HEAD = {1: "\u041b\u043e\u043d\u0433", -1: "\u0428\u043e\u0440\u0442"}
 DOT = {1: "\U0001f7e2", -1: "\U0001f534"}
 WHY = {"stop": "\u043f\u043e \u0441\u0442\u043e\u043f\u0443", "channel": "\u043f\u043e \u043f\u0440\u0430\u0432\u0438\u043b\u0443 \u0432\u044b\u0445\u043e\u0434\u0430"}
 MINUS = "\u2212"
-SEP = " \u00b7 "
 
 
 def list_symbols():
@@ -179,14 +245,33 @@ def side_of(state):
     return 1 if state["state"] == "long" else -1
 
 
-def compose(asof, baseline, opened, closing, closed, rows, open_rows):
-    """The alert's text: one event to a line, then the rule's record since GO_LIVE."""
+def entry_lines(o, own):
+    """An entry in two lines: the side, the entry and the stop; then the target and, with the owner's book,
+    the size that loses his medium risk at that stop and its margin at the leverage paper.copy_size names."""
+    side = side_of(o)
+    line = T_ENTRY.format(dot=DOT[side], side=SIDE_HEAD[side], sym=name(o["symbol"]), entry=px(o["entry"]),
+                          stop=px(o["stop"]), dist=signed((o["stop"] / o["entry"] - 1) * 100, 1))
+    plan = T_PLAN.format(target=px(o["target"]), tdist=signed((o["target"] / o["entry"] - 1) * 100, 1))
+    if own is not None:
+        notional, margin, lev, _ = paper.copy_size(own, abs(o["stop"] / o["entry"] - 1))
+        plan += T_PLAN_SIZE.format(notional="%d" % round(notional), margin="%d" % round(margin), lev=lev)
+    return [line if o["entry_due"] else line + T_LATE.format(date=ddmm(o["entry_date"])), plan]
+
+
+def majors_first(rows):
+    return sorted(rows, key=lambda o: o["symbol"] not in MAJORS)
+
+
+def compose(asof, baseline, opened, scaled, closing, closed, rows, open_rows, own):
+    """The daily close's alert: one event to a line -- an entry in two, the majors first -- then the plan's
+    record since GO_LIVE, and under an entry what the target means, when to enter and the owner's ceilings.
+    The baseline also prints every position held, with its stop and its target, one to a line."""
     lines = [(T_HEAD_BASE if baseline else T_HEAD).format(d=ddmm(asof))]
-    for o in opened:
-        side = side_of(o)
-        line = T_OPEN.format(dot=DOT[side], side=SIDE[side], sym=name(o["symbol"]), entry=px(o["entry"]),
-                             stop=px(o["stop"]), dist=signed((o["stop"] / o["entry"] - 1) * 100, 1))
-        lines.append(line if o["entry_due"] else line + T_LATE.format(date=ddmm(o["entry_date"])))
+    for o in majors_first(opened):
+        lines += entry_lines(o, own)
+    for o in scaled:
+        lines.append(T_SCALED.format(sym=name(o["symbol"]), side=SIDE[side_of(o)], px=px(o["scale_px"]),
+                                     stop=px(o["stop_now"])))
     for o in closing:
         lines.append(T_CLOSING.format(sym=name(o["symbol"]), side=SIDE[side_of(o)]))
     for row in closed:
@@ -206,56 +291,120 @@ def compose(asof, baseline, opened, closing, closed, rows, open_rows):
     lines.append(T_OPEN_NOW.format(n=len(open_rows), nl=sum(1 for o in open_rows if side_of(o) > 0),
                                    ns=sum(1 for o in open_rows if side_of(o) < 0),
                                    r=signed(sum(o["r_open"] for o in open_rows if o["r_open"] is not None), 2)))
-    if baseline and open_rows:
-        lines.append(T_HELD.format(rows=SEP.join(DOT[side_of(o)] + " " + name(o["symbol"]) for o in open_rows)))
+    held = majors_first(o for o in open_rows if o not in opened) if baseline else []
+    for o in held:
+        side = side_of(o)
+        if o.get("stop_now") is not None:
+            lines.append(T_HELD_DONE.format(dot=DOT[side], side=SIDE_HEAD[side], sym=name(o["symbol"]),
+                                            stop=px(o["stop_now"])))
+        else:
+            lines.append(T_HELD.format(dot=DOT[side], side=SIDE_HEAD[side], sym=name(o["symbol"]),
+                                       stop=px(o["stop"]), target=px(o["target"])))
+    if opened or held:
+        lines.append(T_HOW)
+    if opened:
+        lines.append(T_WHEN)
+        if own is not None:
+            side_n, book_n = paper.ceilings(own)
+            lines.append(T_LIMIT.format(side_n=side_n, book_n=book_n, risk="%d" % round(
+                paper.risk_usdt(own["capital_usdt"], own["risk_pct"] / 100))))
     if baseline:
         lines.append(T_LEGEND)
-    if opened:
-        lines.append(T_FOOT)
     return "\n".join(lines)
 
 
-def main(argv=None, now_ms=None):
-    parser = argparse.ArgumentParser(description="the trend book's daily signal and forward ledger")
-    parser.add_argument("--state", default=common.STATE_DIR)
-    parser.add_argument("--outbox", default=None, help="where the alert is written; the bot's outbox by default")
-    args = parser.parse_args(argv)
-    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
-    ledger_path, record_path = os.path.join(args.state, LEDGER), os.path.join(args.state, RECORD)
-    try:
-        ledger = read_ledger(ledger_path)
-    except (OSError, ValueError, TypeError):
-        common.log("score: a file of the ledger is not a trade, nothing written")
-        return 5
-    try:
-        with open(record_path, encoding="utf-8") as fh:
-            prev = json.load(fh)
-        prev_asof, prev_ts = str(prev["asof"]), str(prev["ts"])
-    except (OSError, ValueError, KeyError, TypeError):
-        prev_asof = prev_ts = None
-    baseline = prev_asof is None
+def compose_look(day_now, hours, stopped, scaled, entries):
+    """The look's alert: what the day has done first -- a stop, a target -- then each entry its close would make
+    at the last price, named a candidate, with the stop and the target it would take."""
+    lines = [F_HEAD.format(d=ddmm(day_now), h=hours)]
+    for symbol, side, price in stopped:
+        lines.append(F_STOP.format(sym=name(symbol), side=SIDE[side], px=px(price)))
+    for o in scaled:
+        lines.append(F_SCALE.format(sym=name(o["symbol"]), side=SIDE[side_of(o)], px=px(o["scale_px"])))
+    for o, last, level in entries:
+        line = F_ENTRY.format(side=SIDE[side_of(o)], sym=name(o["symbol"]), last=px(last))
+        lines.append(line if level is None else line + F_LEVEL.format(level=px(level)))
+        lines.append(F_ENTRY_PLAN.format(stop=px(o["stop"]), target=px(o["target"])))
+    if entries:
+        lines.append(F_FOOT)
+    return "\n".join(lines)
 
+
+def look_of(state_dir, day_iso):
+    """The look's record of a day as (the entries it named, as (symbol, side) pairs), or None where the day was
+    not looked at or its file is not a look."""
+    try:
+        with open(os.path.join(state_dir, FORMING, day_iso + ".json"), encoding="utf-8") as fh:
+            doc = json.load(fh)
+        if doc["day"] != day_iso:
+            return None
+        return {(str(e["symbol"]), int(e["side"])) for e in doc["entries"]}
+    except (OSError, ValueError, KeyError, TypeError, AttributeError):
+        return None
+
+
+def forming(args, now_ms):
+    """The look at the day still forming: one read of each symbol, the plan's state at the last close and its
+    state if the day closed at the last price. Told as it is: a stop the day has reached, a target it has
+    reached -- neither can be taken back. Told as a candidate: the entry a close at the last price would make.
+    An exit that close would make is not told: nothing is done about it before the close, which tells it. One
+    look a UTC day; the alert is written before the record, so that a look that died between them is made
+    again."""
+    day_now = day(now_ms)
+    path = os.path.join(args.state, FORMING, day_now + ".json")
+    if os.path.exists(path):
+        common.log("score: forming day=%s already looked at, nothing written" % day_now)
+        return 0
     symbols = list_symbols()
-    read, unread = [], []
+    stopped, scaled, entries, unread = [], [], [], []
     for symbol in symbols:
         try:
-            read.append(book.live_state(symbol, now_ms))
+            bars, today = book.live_day(symbol, now_ms)
+            if day(today[0]) != day_now:
+                raise ValueError("the day still forming is not today")
+            now = book.state_of(symbol, bars, today[1], book.SCALE_R)[0]
+            then, trades, _ = book.state_of(symbol, bars + [today], today[4], book.SCALE_R)
         except Exception:                 # one symbol's failure never hides the others
             unread.append(symbol)
-    asof = max((state["asof"] for state, _, _ in read if "asof" in state), default=None)
-    if asof is None or (not baseline and asof < prev_asof):
-        common.log("score: asof=%s symbols=%d read=%d nothing written" % (asof or "-", len(symbols), len(read)))
+            continue
+        stopped += [(symbol, tr["side"], tr["exit"]) for tr in trades
+                    if tr["t_exit"] == today[0] and tr["why"] == "stop"]
+        if then["state"] not in ("long", "short"):
+            continue
+        if then.get("scale_date") == day_now:
+            scaled.append(then)
+        if then["entry_due"]:         # the level the close must cross is the last close's trigger
+            entries.append((then, today[4], now.get("long_trigger" if side_of(then) > 0 else "short_trigger")))
+    if len(unread) == len(symbols):
+        common.log("score: forming day=%s symbols=%d read=0 nothing written" % (day_now, len(symbols)))
         return 4
-    # A symbol whose last closed day is not the day the others stand on is not read today.
-    unread += [state["symbol"] for state, _, _ in read if state.get("asof", asof) != asof]
-    live = [item for item in read if item[0].get("asof", asof) == asof]
-    fresh = baseline or asof > prev_asof
-    seen = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000))
+    stopped.sort(key=lambda item: item[0] not in MAJORS)
+    scaled = majors_first(scaled)
+    entries.sort(key=lambda item: item[0]["symbol"] not in MAJORS)
+    alert = bool(stopped or scaled or entries)
+    if alert:
+        hours = max(1, int(round((book.DAY_MS - now_ms % book.DAY_MS) / 3600000.0)))
+        common.write_outbox("alert", compose_look(day_now, hours, stopped, scaled, entries),
+                            outbox_dir=args.outbox)
+    os.makedirs(os.path.dirname(path), mode=0o750, exist_ok=True)
+    common.atomic_write(path, {
+        "v": 1, "k": "score-forming", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000)),
+        "day": day_now, "symbols": len(symbols), "unread": sorted(unread),
+        "stopped": [symbol for symbol, _, _ in stopped], "scaled": [o["symbol"] for o in scaled],
+        "entries": [{"symbol": o["symbol"], "side": side_of(o)} for o, _, _ in entries]}, mode=0o640)
+    common.log("score: forming day=%s symbols=%d read=%d unread=%d stopped=%d scaled=%d entries=%d alert=%s"
+               % (day_now, len(symbols), len(symbols) - len(unread), len(unread), len(stopped), len(scaled),
+                  len(entries), "yes" if alert else "no"))
+    return 0
+
 
+def ledger_pass(path, ledger, live, asof, seen):
+    """One ledger's run: (added, pending, late, disagree). live is (state, trades) per symbol read today; a trade
+    is written as the module's docstring says, each a new file (inv. 38)."""
     known = {(row["symbol"], row["t_entry"]): row for row in ledger}
     floor = GO_LIVE if not ledger else (date.fromisoformat(asof) - timedelta(days=RETRY_DAYS)).isoformat()
     added, pending, late, disagree = [], 0, 0, 0
-    for state, trades, _ in live:
+    for state, trades in live:
         for tr in trades:
             if day(tr["t_entry"]) < GO_LIVE:
                 continue
@@ -273,43 +422,105 @@ def main(argv=None, now_ms=None):
                     raise ValueError("the result is not finite")
             except Exception as exc:      # not written: the next run asks for the prints again (inv. 70)
                 pending += 1
-                common.log("score: pending %s %s" % (state["symbol"], exc.__class__.__name__))
+                common.log("score: pending %s %s %s" % (os.path.basename(path), state["symbol"], exc.__class__.__name__))
                 continue
             known[key] = {"symbol": state["symbol"], "side": tr["side"], "t_entry": tr["t_entry"],
                           "entry": tr["entry"], "stop": tr["stop"], "t_exit": tr["t_exit"], "exit": tr["exit"],
                           "why": tr["why"], "r": r, "seen": seen}
             added.append(known[key])
     if added:
-        os.makedirs(ledger_path, mode=0o750, exist_ok=True)
+        os.makedirs(path, mode=0o750, exist_ok=True)
         for row in added:                 # a new file each: nothing that stands is opened (inv. 38)
-            common.atomic_write(os.path.join(ledger_path, row_name(row)), row, mode=0o640)
-    rows = ledger + added
+            common.atomic_write(os.path.join(path, row_name(row)), row, mode=0o640)
+    return added, pending, late, disagree
 
-    open_rows = [state for state, _, _ in live if state["state"] in ("long", "short")]
+
+def main(argv=None, now_ms=None):
+    parser = argparse.ArgumentParser(description="the trend book's daily signal and forward ledger")
+    parser.add_argument("--state", default=common.STATE_DIR)
+    parser.add_argument("--outbox", default=None, help="where the alert is written; the bot's outbox by default")
+    parser.add_argument("--forming", action="store_true", help="the look at the day still forming")
+    args = parser.parse_args(argv)
+    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
+    if args.forming:
+        return forming(args, now_ms)
+    rule_path, plan_path = os.path.join(args.state, LEDGER), os.path.join(args.state, PLAN)
+    record_path = os.path.join(args.state, RECORD)
+    try:
+        rule_ledger, plan_ledger = read_ledger(rule_path), read_ledger(plan_path)
+    except (OSError, ValueError, TypeError):
+        common.log("score: a file of the ledger is not a trade, nothing written")
+        return 5
+    try:
+        with open(record_path, encoding="utf-8") as fh:
+            prev = json.load(fh)
+        prev_asof, prev_ts, prev_v = str(prev["asof"]), str(prev["ts"]), prev.get("v")
+    except (OSError, ValueError, KeyError, TypeError, AttributeError):
+        prev_asof = prev_ts = prev_v = None
+    # TZ-79's record (v 1) knew no plan: the first run after it is the plan's baseline, and tells no close.
+    baseline = prev_asof is None or prev_v != 2
+
+    symbols = list_symbols()
+    read, unread = [], []
+    for symbol in symbols:
+        try:
+            bars, open_now = book.live_bars(symbol, now_ms)
+            read.append((book.state_of(symbol, bars, open_now), book.state_of(symbol, bars, open_now, book.SCALE_R)))
+        except Exception:                 # one symbol's failure never hides the others
+            unread.append(symbol)
+    asof = max((rule[0]["asof"] for rule, _ in read if "asof" in rule[0]), default=None)
+    if asof is None or (prev_asof is not None and asof < prev_asof):
+        common.log("score: asof=%s symbols=%d read=%d nothing written" % (asof or "-", len(symbols), len(read)))
+        return 4
+    # A symbol whose last closed day is not the day the others stand on is not read today.
+    unread += [rule[0]["symbol"] for rule, _ in read if rule[0].get("asof", asof) != asof]
+    live = [item for item in read if item[0][0].get("asof", asof) == asof]
+    fresh = baseline or asof > prev_asof
+    seen = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000))
+
+    rule_added, rule_pending, rule_late, rule_disagree = ledger_pass(
+        rule_path, rule_ledger, [(rule[0], rule[1]) for rule, _ in live], asof, seen)
+    plan_added, pending, late, disagree = ledger_pass(
+        plan_path, plan_ledger, [(plan[0], plan[1]) for _, plan in live], asof, seen)
+    rule_rows, rows = rule_ledger + rule_added, plan_ledger + plan_added
+
+    open_rows = [plan[0] for _, plan in live if plan[0]["state"] in ("long", "short")]
     if baseline:
-        opened = [o for o in open_rows if o["entry_due"]]
+        opened = [o for o in open_rows if o["entry_due"] or (prev_asof is not None and o["entry_date"] > prev_asof)]
     else:
         after = (date.fromisoformat(prev_asof) + timedelta(days=1)).isoformat()
         opened = [o for o in open_rows if fresh and o["entry_date"] > after]
+    scaled = [] if baseline else [o for o in open_rows if fresh and o.get("scale_date", "") > prev_asof]
     closing = [o for o in open_rows if fresh and o["exit_due"]]
     # A closed trade is told once: the rows written since the record this run replaces.
     closed = [] if baseline else [row for row in rows if row["seen"] > prev_ts]
-    alert = baseline or bool(opened or closing or closed)
+    alert = baseline or bool(opened or scaled or closing or closed)
+    # What the look at the day that has just closed named, against the entries that close made.
+    named = look_of(args.state, asof)
+    due = {(o["symbol"], side_of(o)) for o in open_rows if o["entry_due"]}
+    look = None if named is None else {"named": len(named), "hit": len(named & due), "entries": len(due)}
     if alert:
-        common.write_outbox("alert", compose(asof, baseline, opened, closing, closed, rows, open_rows),
-                            outbox_dir=args.outbox)
+        common.write_outbox("alert", compose(asof, baseline, opened, scaled, closing, closed, rows, open_rows,
+                                             paper.owner_now()), outbox_dir=args.outbox)
+
+    def by_group(group):
+        return {"all": totals(group), "majors": totals([row for row in group if row["symbol"] in MAJORS]),
+                "others": totals([row for row in group if row["symbol"] not in MAJORS])}
     common.atomic_write(record_path, {
-        "v": 1, "k": "score", "ts": seen, "asof": asof, "since": GO_LIVE, "symbols": len(symbols),
+        "v": 2, "k": "score", "ts": seen, "asof": asof, "since": GO_LIVE, "symbols": len(symbols),
         "unread": sorted(unread),
-        "open": [{key: o[key] for key in ("symbol", "state", "entry_date", "entry", "stop", "exit_level",
-                                          "r_open", "entry_due", "exit_due")} for o in open_rows],
-        "closed": {"all": totals(rows), "majors": totals([row for row in rows if row["symbol"] in MAJORS]),
-                   "others": totals([row for row in rows if row["symbol"] not in MAJORS])},
-        "pending": pending, "late": late, "disagree": disagree}, mode=0o640)
-    common.log("score: asof=%s symbols=%d read=%d unread=%d open=%d opened=%d closing=%d closed=%d pending=%d "
-               "late=%d disagree=%d ledger=%d alert=%s" % (asof, len(symbols), len(symbols) - len(unread), len(unread),
-                                                           len(open_rows), len(opened), len(closing), len(closed),
-                                                           pending, late, disagree, len(rows), "yes" if alert else "no"))
+        "open": [{key: o.get(key) for key in ("symbol", "state", "entry_date", "entry", "stop", "target", "exit_level",
+                                              "r_open", "entry_due", "exit_due", "scale_date", "stop_now")}
+                 for o in open_rows],
+        "closed": by_group(rows), "pending": pending, "late": late, "disagree": disagree, "look": look,
+        "rule": {"open": sum(1 for rule, _ in live if rule[0]["state"] in ("long", "short")), "closed": by_group(rule_rows),
+                 "pending": rule_pending, "late": rule_late, "disagree": rule_disagree}}, mode=0o640)
+    common.log("score: asof=%s symbols=%d read=%d unread=%d open=%d opened=%d scaled=%d closing=%d closed=%d "
+               "pending=%d late=%d disagree=%d ledger=%d rule=%d look=%s alert=%s"
+               % (asof, len(symbols), len(symbols) - len(unread), len(unread), len(open_rows), len(opened),
+                  len(scaled), len(closing), len(closed), pending, late, disagree, len(rows), len(rule_rows),
+                  "-" if look is None else "%d/%d/%d" % (look["hit"], look["named"], look["entries"]),
+                  "yes" if alert else "no"))
     return 0
 
 
diff --git a/vps/selftest.py b/vps/selftest.py
index bb5998a..99a667e 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -3145,16 +3145,23 @@ def section_w_orders(s):
         shutil.rmtree(tmp, ignore_errors=True)
 
 
-# --- AB: the book's signal and its forward ledger (TZ-79) ------------------------------------------
-AB_LINE = re.compile(r"score: asof=\d{4}-\d\d-\d\d symbols=\d+ read=\d+ unread=\d+ open=\d+ opened=\d+ closing=\d+ "
-                     r"closed=\d+ pending=\d+ late=\d+ disagree=\d+ ledger=\d+ alert=(yes|no)")
+# --- AB: the book's signal and its forward ledger (TZ-79), the plan's (TZ-80) -----------------------------
+AB_LINE = re.compile(r"score: asof=\d{4}-\d\d-\d\d symbols=\d+ read=\d+ unread=\d+ open=\d+ opened=\d+ scaled=\d+ "
+                     r"closing=\d+ closed=\d+ pending=\d+ late=\d+ disagree=\d+ ledger=\d+ rule=\d+ "
+                     r"look=(-|\d+/\d+/\d+) alert=(yes|no)")
+AB_LOOK = re.compile(r"score: forming day=\d{4}-\d\d-\d\d symbols=\d+ read=\d+ unread=\d+ stopped=\d+ scaled=\d+ "
+                     r"entries=\d+ alert=(yes|no)")
+AB_LOOK_MS = 15 * 3600 * 1000 + 10 * 60 * 1000          # the look's hour: 15:10 UTC
+AB_OWN = {"capital_usdt": 30000.0, "risk_pct": 0.5, "side_max_pct": 3.0, "book_max_pct": 5.0}
 AB_H8 = 8 * 3600 * 1000
 
 
-def ab_klines(bars, fill):
-    """What fapi's daily klines answer for these closed bars and a forming day that opened at fill."""
+def ab_klines(bars, fill, part=None):
+    """What fapi's daily klines answer for these closed bars and a forming day that opened at fill -- or, with
+    part, a forming day that stands at (open, high, low, last)."""
     closed = [[b[0], str(b[1]), str(b[2]), str(b[3]), str(b[4]), "0", b[0] + book.DAY_MS - 1] for b in bars]
-    forming = [bars[-1][0] + book.DAY_MS, str(fill), str(fill + 1), str(fill - 1), str(fill + 0.25), "0", 10 ** 15]
+    o, h, l, c = part or (fill, fill + 1, fill - 1, fill + 0.25)
+    forming = [bars[-1][0] + book.DAY_MS, str(o), str(h), str(l), str(c), "0", 10 ** 15]
     return json.dumps(closed + [forming]).encode()
 
 
@@ -3170,14 +3177,15 @@ def ab_funding(url, rate="0.0001", hole=None):
 class AbHost:
     """The exchange and the state directory of one test: worlds maps a symbol to its bars, or to an
     exception its read raises; run(n) reads the day whose forming bar is bar n of every world, each run a
-    second after the one before it."""
+    second after the one before it; look(n, part) looks at that day at 15:10 UTC, each symbol of part standing at
+    its (open, high, low, last)."""
 
-    def __init__(self, tmp, worlds, funding=ab_funding):
-        self.tmp, self.worlds, self.funding = tmp, worlds, funding
+    def __init__(self, tmp, worlds, funding=ab_funding, own=AB_OWN):
+        self.tmp, self.worlds, self.funding, self.own = tmp, worlds, funding, own
         self.state, self.outbox = os.path.join(tmp, "state"), os.path.join(tmp, "outbox")
         os.makedirs(self.state)
         os.makedirs(self.outbox)
-        self.sent, self.urls, self.runs = set(), [], 0
+        self.sent, self.urls, self.runs, self.part = set(), [], 0, {}
 
     def get(self, url):
         self.urls.append(url)
@@ -3188,29 +3196,47 @@ class AbHost:
         if isinstance(world, Exception):
             raise world
         bars = world[:self.n + self.shift.get(symbol, 0)]
-        return ab_klines(bars, world[len(bars)][1] if len(bars) < len(world) else bars[-1][4])
+        return ab_klines(bars, world[len(bars)][1] if len(bars) < len(world) else bars[-1][4], self.part.get(symbol))
 
-    def run(self, n, shift=None):
-        """(exit code, printed line, the alerts written by this run, the ledger's text, the record or None)."""
-        self.n, self.shift, self.runs = n, shift or {}, self.runs + 1
-        saved = book._get, score.list_symbols, common.OUTBOX_DIR
+    def call(self, argv, n, shift, part, at_ms):
+        """(exit code, what it printed, the alerts it wrote) of one score.py call on day n."""
+        self.n, self.shift, self.part, self.runs = n, shift or {}, part or {}, self.runs + 1
+        saved = book._get, score.list_symbols, common.OUTBOX_DIR, paper.owner_now
         book._get, score.list_symbols, common.OUTBOX_DIR = self.get, lambda: list(self.worlds), self.outbox
+        paper.owner_now = lambda: self.own
         try:
             with contextlib.redirect_stdout(io.StringIO()) as out:
-                code = score.main(["--state", self.state], now_ms=n * book.DAY_MS + self.runs * 1000)
+                code = score.main(["--state", self.state] + argv, now_ms=n * book.DAY_MS + at_ms + self.runs * 1000)
         finally:
-            book._get, score.list_symbols, common.OUTBOX_DIR = saved
+            book._get, score.list_symbols, common.OUTBOX_DIR, paper.owner_now = saved
+            self.part = {}
         texts = []
         for name in sorted(set(os.listdir(self.outbox)) - self.sent):
             self.sent.add(name)
             with open(os.path.join(self.outbox, name), encoding="utf-8") as fh:
                 doc = json.load(fh)
             texts.append((doc["kind"], doc["text"]))
-        return code, out.getvalue(), texts, self.ledger(), self.record()
+        return code, out.getvalue(), texts
+
+    def run(self, n, shift=None):
+        """(exit code, printed line, the alerts written by this run, the ledger's text, the record or None)."""
+        return self.call([], n, shift, None, 0) + (self.ledger(), self.record())
+
+    def look(self, n, part=None, shift=None):
+        """(exit code, printed line, the alerts written by this look, the look's record of day n or None)."""
+        return self.call(["--forming"], n, shift, part, AB_LOOK_MS) + (self.looked(n),)
+
+    def looked(self, n):
+        try:
+            with open(os.path.join(self.state, score.FORMING, score.day(n * book.DAY_MS) + ".json"), encoding="utf-8") as fh:
+                return json.load(fh)
+        except FileNotFoundError:
+            return None
 
-    def ledger(self):
-        """The ledger's files joined in name order, a trade a line; None while there is none."""
-        folder = os.path.join(self.state, score.LEDGER)
+    def ledger(self, which=None):
+        """A ledger's files joined in name order, a trade a line; None while there is none. The rule's by default,
+        the plan's with which=score.PLAN."""
+        folder = os.path.join(self.state, which or score.LEDGER)
         try:
             names = sorted(os.listdir(folder))
         except FileNotFoundError:
@@ -3221,9 +3247,9 @@ class AbHost:
                 parts.append(fh.read())
         return "".join(parts) or None
 
-    def stamps(self):
+    def stamps(self, which=None):
         """Each ledger file's name, inode, modification time and mode."""
-        folder = os.path.join(self.state, score.LEDGER)
+        folder = os.path.join(self.state, which or score.LEDGER)
         return sorted((name, st.st_ino, st.st_mtime_ns, st.st_mode & 0o7777)
                       for name, st in ((name, os.stat(os.path.join(folder, name))) for name in os.listdir(folder)))
 
@@ -3278,37 +3304,52 @@ def section_ab(s):
         code, printed, alerts, ledger, record = h.run(61)
         s.check("baseline: exit 0, one line of the fixed shape",
                 code == 0 and printed.count("\n") == 1 and AB_LINE.fullmatch(printed.rstrip("\n")) is not None)
-        s.check("baseline: the line reads symbols=2 read=1 unread=1 open=1 opened=1 ledger=0 alert=yes",
-                [ab_field(printed, f) for f in ("asof", "symbols", "read", "unread", "open", "opened", "closing",
-                                                "closed", "pending", "late", "disagree", "ledger", "alert")]
-                == ["1970-03-02", "2", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0", "yes"])
+        s.check("baseline: the line reads symbols=2 read=1 unread=1 open=1 opened=1 ledger=0 rule=0 look=- alert=yes",
+                [ab_field(printed, f) for f in ("asof", "symbols", "read", "unread", "open", "opened", "scaled",
+                                                "closing", "closed", "pending", "late", "disagree", "ledger", "rule",
+                                                "look", "alert")]
+                == ["1970-03-02", "2", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "-", "yes"])
         text = alerts[0][1] if alerts else ""
         s.check("baseline: one alert, of kind alert", len(alerts) == 1 and alerts[0][0] == "alert")
         s.check("baseline: its head names the day the book stands on",
                 text.split("\n")[0] == score.T_HEAD_BASE.format(d="02.03"))
-        s.check("baseline: the entry due today prints its fill and its stop, 105 - 2 x 2.2, as code spans",
-                score.T_OPEN.format(dot=score.DOT[1], side=score.SIDE[1], sym="AAA", entry="105", stop="100.6",
-                                    dist="\u22124.2") in text.split("\n"))
-        s.check("baseline: no closed trade yet, one open, the held line and the foot",
+        s.check("baseline: the entry due today, two lines -- fill and stop 105 - 2 x 2.2; the target 105 + 2 x 4.4, "
+                "and 150 USDT over 4.4 of 105 as 3580 USDT, 1193 of margin at 3x", text.split("\n")[1:3] == [
+                    score.T_ENTRY.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="AAA", entry="105", stop="100.6",
+                                         dist="\u22124.2"),
+                    score.T_PLAN.format(target="113.8", tdist="+8.4")
+                    + score.T_PLAN_SIZE.format(notional="3580", margin="1193", lev=3)])
+        held_aaa = score.T_HELD.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="AAA", stop="100.6", target="113.8")
+        s.check("baseline: no closed trade yet, one open, no second line for the entry printed in full",
                 score.T_SCORE_NONE.format(since="01.01.1970") in text and score.T_OPEN_NOW.format(n=1, nl=1, ns=0, r="+0.00") in text
-                and score.T_HELD.format(rows=score.DOT[1] + " AAA") in text and text.split("\n")[-1] == score.T_FOOT)
+                and held_aaa not in text)
+        s.check("under an entry: what the target means, when to enter, the owner's ceilings, each once and in that order",
+                text.split("\n")[-4:] == [score.T_HOW, score.T_WHEN, score.T_LIMIT.format(side_n=6, book_n=10, risk="150"),
+                                          score.T_LEGEND]
+                and "6" in score.T_LIMIT.format(side_n=6, book_n=10, risk="150"))
         s.check("baseline: the legend of R is printed once, and on no later alert",
                 text.split("\n").count(score.T_LEGEND) == 1)
-        s.check("baseline: no ledger file is written while no trade has closed", ledger is None)
-        s.check("record keys v k ts asof since symbols unread open closed pending late disagree, in order",
+        s.check("baseline: no ledger file is written while no trade has closed",
+                ledger is None and h.ledger(score.PLAN) is None)
+        s.check("record keys v k ts asof since symbols unread open closed pending late disagree look rule, in order",
                 record is not None and list(record) == ["v", "k", "ts", "asof", "since", "symbols", "unread", "open",
-                                                        "closed", "pending", "late", "disagree"])
-        s.check("record v 1, k score, asof the last closed day, the unread symbol named",
+                                                        "closed", "pending", "late", "disagree", "look", "rule"])
+        s.check("a day nobody looked at carries no look's count", record is not None and record["look"] is None)
+        s.check("record v 2, k score, asof the last closed day, the unread symbol named",
                 record is not None and (record["v"], record["k"], record["asof"], record["unread"])
-                == (1, "score", "1970-03-02", ["BADUSDT"]))
+                == (2, "score", "1970-03-02", ["BADUSDT"]))
         held = ((record or {}).get("open") or [{}])[0]
-        s.check("record's open position: the entry due, its stop, no open R",
+        s.check("record's open position: the entry due, its stop and target, no open R, no target reached",
                 record is not None and len(record["open"]) == 1 and abs(held.get("stop", 0) - 100.6) < eps
-                and {key: value for key, value in held.items() if key != "stop"}
+                and abs(held.get("target", 0) - 113.8) < eps
+                and {key: value for key, value in held.items() if key not in ("stop", "target")}
                 == {"symbol": "AAAUSDT", "state": "long", "entry_date": "1970-03-03", "entry": 105.0,
-                    "exit_level": 99.0, "r_open": None, "entry_due": True, "exit_due": False})
-        s.check("record's closed totals are three empty summaries",
-                record is not None and record["closed"] == {"all": {"n": 0}, "majors": {"n": 0}, "others": {"n": 0}})
+                    "exit_level": 99.0, "r_open": None, "entry_due": True, "exit_due": False, "scale_date": None,
+                    "stop_now": None})
+        s.check("record's closed totals, the plan's and the rule's, are empty summaries",
+                record is not None and record["closed"] == {"all": {"n": 0}, "majors": {"n": 0}, "others": {"n": 0}}
+                and record["rule"] == {"open": 1, "closed": {"all": {"n": 0}, "majors": {"n": 0}, "others": {"n": 0}},
+                                       "pending": 0, "late": 0, "disagree": 0})
         s.check("the record's mode is 0640",
                 os.stat(os.path.join(h.state, score.RECORD)).st_mode & 0o7777 == 0o640)
         code, printed, alerts, ledger, record = h.run(62)
@@ -3317,6 +3358,18 @@ def section_ab(s):
                 and ab_field(printed, "opened") == "0")
         code, printed, alerts, ledger, record = h.run(62)
         s.check("the same day read twice: no alert and nothing told again", code == 0 and alerts == [])
+        code, printed, alerts, ledger, record = h.run(69)
+        text = alerts[0][1] if alerts else ""
+        s.check("the day the target is reached: one alert, half closed at 113.8 and the rest's stop at the entry",
+                len(alerts) == 1 and text.split("\n")[1] == score.T_SCALED.format(
+                    sym="AAA", side=score.SIDE[1], px="113.8", stop="105")
+                and ab_field(printed, "scaled") == "1" and ab_field(printed, "opened") == "0")
+        held = ((record or {}).get("open") or [{}])[0]
+        s.check("record's open position after the target: its day, the stop now at the entry, half its R banked",
+                held.get("scale_date") == "1970-03-10" and held.get("stop_now") == 105.0 and abs(held.get("stop", 0) - 100.6) < eps
+                and abs(held.get("r_open", 0) - (0.5 * 8.8 + 0.5 * 8.0) / 4.4) < eps)
+        code, printed, alerts, ledger, record = h.run(70)
+        s.check("the target is told once: the next day says nothing", alerts == [] and ab_field(printed, "scaled") == "0")
         code, printed, alerts, ledger, record = h.run(101)
         text = alerts[0][1] if alerts else ""
         s.check("a close below the 20-day low: the exit due today is told once, with no row yet",
@@ -3327,6 +3380,15 @@ def section_ab(s):
         code, printed, alerts, ledger, record = h.run(102)
         rows = [json.loads(line) for line in (ledger or "").split("\n") if line]
         want = (122.0 / 105.0 - 1 - 120 * 0.0001 - 2 * book.COST_SIDE) / (4.4 / 105.0)
+        want_plan = (0.5 * (113.8 / 105.0 - 1) + 0.5 * (122.0 / 105.0 - 1) - 21 * 0.0001 - 0.5 * 99 * 0.0001
+                     - 2 * book.COST_SIDE) / (4.4 / 105.0)
+        plan_rows = [json.loads(line) for line in (h.ledger(score.PLAN) or "").split("\n") if line]
+        s.check("the plan's ledger holds the same trade with its target: half at 113.8 on 10.03, half at 122",
+                len(plan_rows) == 1 and list(plan_rows[0]) == list(score.LEDGER_KEYS)
+                and [x[0] for x in h.stamps(score.PLAN)] == ["AAAUSDT-%d.json" % (61 * book.DAY_MS)]
+                and (plan_rows[0]["exit"], plan_rows[0]["why"]) == (122.0, "channel"))
+        s.check("the plan's R: half the move to the target and half to the exit, the whole funding to the target's day "
+                "and half after it", bool(plan_rows) and abs(plan_rows[0]["r"] - want_plan) < eps)
         s.check("the closed trade is one ledger file, AAAUSDT-<its entry stamp>.json, with the ten keys in order",
                 len(rows) == 1 and list(rows[0]) == list(score.LEDGER_KEYS)
                 and [x[0] for x in h.stamps()] == ["AAAUSDT-%d.json" % (61 * book.DAY_MS)])
@@ -3338,17 +3400,19 @@ def section_ab(s):
         s.check("its R is book.result_r on the 120 prints after the entry and up to the exit",
                 abs(row.get("r", 0) - want) < eps)
         text = alerts[0][1] if alerts else ""
-        s.check("an alert after the baseline carries no legend and no list of coins",
-                score.T_LEGEND not in text and not [x for x in text.split("\n") if x.startswith(score.T_HELD.split("{")[0])])
-        s.check("the close is told with its R, and the record of the rule follows it",
+        s.check("an alert after the baseline with no entry carries no legend, no held position and no line about entries",
+                score.T_LEGEND not in text and held_aaa not in text and "AAA** \u00b7 " + score.T_HELD.split("** \u00b7 ")[1].split("`")[0] not in text
+                and score.T_HOW not in text and score.T_WHEN not in text and score.T_LIMIT.split("{")[0] not in text)
+        s.check("the close is told with the plan's R, and the plan's record follows it",
                 len(alerts) == 1 and text.split("\n")[1] == score.T_CLOSED.format(
-                    sym="AAA", side=score.SIDE[1], why=score.WHY["channel"], r=score.signed(want, 2))
-                and score.T_SCORE.format(since="01.01.1970", n=1, total=score.signed(want, 2), wins=1) in text
-                and score.T_GROUPS.format(n1=0, r1="+0.00", n2=1, r2=score.signed(want, 2)) in text)
-        s.check("the record totals it: one trade, a null profit factor where nothing lost",
+                    sym="AAA", side=score.SIDE[1], why=score.WHY["channel"], r=score.signed(want_plan, 2))
+                and score.T_SCORE.format(since="01.01.1970", n=1, total=score.signed(want_plan, 2), wins=1) in text
+                and score.T_GROUPS.format(n1=0, r1="+0.00", n2=1, r2=score.signed(want_plan, 2)) in text)
+        s.check("the record totals the plan and the rule apart: one trade each, a null profit factor where nothing lost",
                 record["closed"]["all"]["n"] == 1 and record["closed"]["all"]["pf"] is None
-                and abs(record["closed"]["all"]["total"] - want) < eps and record["closed"]["majors"] == {"n": 0}
-                and record["closed"]["others"]["n"] == 1 and record["open"] == [])
+                and abs(record["closed"]["all"]["total"] - want_plan) < eps and record["closed"]["majors"] == {"n": 0}
+                and record["closed"]["others"]["n"] == 1 and record["open"] == []
+                and abs(record["rule"]["closed"]["all"]["total"] - want) < eps and record["rule"]["open"] == 0)
         s.check("the trade's file has mode 0640", [x[3] for x in h.stamps()] == [0o640])
         funding_calls, written = len([u for u in h.urls if "fundingRate" in u]), h.stamps()
         code, printed, alerts, again, record = h.run(103)
@@ -3373,9 +3437,11 @@ def section_ab(s):
         s.check("prints that did not arrive: nothing written, the trade pending, nothing told",
                 code == 0 and ledger is None and ab_field(printed, "pending") == "1" and record["pending"] == 1
                 and alerts == [])
-        s.check("a trade it could not price is named on a line of its own, with the failure's class and no price",
-                printed.split("\n")[0] == "score: pending AAAUSDT OSError" and printed.count("\n") == 2
-                and AB_LINE.fullmatch(printed.split("\n")[1]) is not None)
+        s.check("a trade it could not price is named on a line of its own per ledger, with the failure's class and no price",
+                printed.split("\n")[:2] == ["score: pending score-ledger AAAUSDT OSError",
+                                            "score: pending score-plan AAAUSDT OSError"]
+                and printed.count("\n") == 3 and AB_LINE.fullmatch(printed.split("\n")[2]) is not None
+                and record["rule"]["pending"] == 1)
         h.funding = lambda url: ab_funding(url, hole=(70 * book.DAY_MS, 71 * book.DAY_MS))
         code, printed, alerts, ledger, record = h.run(102)
         s.check("prints with a day missing inside the span: nothing written, the trade pending",
@@ -3386,11 +3452,12 @@ def section_ab(s):
                 ledger is None and ab_field(printed, "pending") == "1")
         score.FUNDING_PAGE = 50
         h.funding = ab_funding
+        asked = len(h.urls)
         code, printed, alerts, ledger, record = h.run(102)
         rows = [json.loads(line) for line in (ledger or "").split("\n") if line]
         s.check("the prints read in three pages give the same R, and the late close is told once",
                 len(rows) == 1 and abs(rows[0]["r"] - want) < eps and len(alerts) == 1
-                and len([u for u in h.urls[-4:] if "fundingRate" in u]) == 3
+                and len([u for u in h.urls[asked:] if "fundingRate" in u]) == 6
                 and alerts[0][1].split("\n")[1].startswith(score.T_CLOSED.split("{sym}")[0]))
         score.FUNDING_PAGE = saved_page
 
@@ -3412,8 +3479,8 @@ def section_ab(s):
         text = alerts[0][1] if alerts else ""
         s.check("one alert carries the long opened today and both closes, a line each",
                 len(alerts) == 1
-                and score.T_OPEN.format(dot=score.DOT[1], side=score.SIDE[1], sym="BTC", entry="103", stop="97.9",
-                                        dist="\u22125.0") in text.split("\n")
+                and score.T_ENTRY.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="BTC", entry="103", stop="97.9",
+                                         dist="\u22125.0") in text.split("\n")
                 and score.T_CLOSED.format(sym="BTC", side=score.SIDE[-1], why=score.WHY["stop"],
                                           r=score.signed(want_short, 2)) in text.split("\n")
                 and score.T_CLOSED.format(sym="DAY", side=score.SIDE[1], why=score.WHY["stop"],
@@ -3425,7 +3492,8 @@ def section_ab(s):
                 in text)
         s.check("no number of the alert carries a float's tail or an exponent, and no symbol its USDT",
                 all(re.fullmatch(r"\d+(\.\d{1,8})?", span) for span in re.findall(r"`([^`]*)`", text))
-                and "USDT" not in text and "e-" not in text and bool(re.findall(r"`([^`]*)`", text)))
+                and "BTCUSDT" not in text and "DAYUSDT" not in text and "e-" not in text
+                and bool(re.findall(r"`([^`]*)`", text)))
 
         # Days the unit did not run, an older read, a stale symbol, an unreadable list and a broken ledger.
         h = AbHost(os.path.join(tmp, "d"), {"AAAUSDT": long_world, "BBBUSDT": long_world})
@@ -3485,6 +3553,189 @@ def section_ab(s):
         s.check("--outbox: the alert is written there and nowhere else",
                 code == 0 and len(os.listdir(aside)) == 1 and os.listdir(aside)[0].endswith("-alert-%d.json" % os.getpid())
                 and os.listdir(h.outbox) == [])
+        # TZ-79's record (v 1) knew no plan: the next run is the plan's baseline and tells no close it fills.
+        h = AbHost(os.path.join(tmp, "k"), {"AAAUSDT": long_world, "BBBUSDT": long_world})
+        with open(os.path.join(h.state, score.RECORD), "w", encoding="utf-8") as fh:
+            json.dump({"v": 1, "k": "score", "ts": "1970-03-04T00:10:00Z", "asof": "1970-03-03"}, fh)
+        h.worlds["BBBUSDT"] = long_world[:70] + [(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(70, 105)]
+        code, printed, alerts, ledger, record = h.run(102)
+        text = alerts[0][1] if alerts else ""
+        plan_files = [x[0] for x in h.stamps(score.PLAN)]
+        s.check("after TZ-79's record: one alert under the baseline's head, the plan's closes filled and none told",
+                code == 0 and len(alerts) == 1 and text.split("\n")[0] == score.T_HEAD_BASE.format(d="12.04")
+                and len(plan_files) == 2 and score.T_CLOSED.split("{sym}")[0] not in text and record["v"] == 2)
+        s.check("after TZ-79's record: the plan's record is in the score line, the legend once",
+                score.T_SCORE.split("{n}")[0].format(since="01.01.1970") in text and text.split("\n").count(score.T_LEGEND) == 1)
+        h = AbHost(os.path.join(tmp, "m"), {"AAAUSDT": long_world, "BTCUSDT": long_world})
+        with open(os.path.join(h.state, score.RECORD), "w", encoding="utf-8") as fh:
+            json.dump({"v": 1, "k": "score", "ts": "1970-03-02T00:10:00Z", "asof": "1970-03-01"}, fh)
+        code, printed, alerts, ledger, record = h.run(70)
+        text = alerts[0][1] if alerts else ""
+        s.check("after TZ-79's record: an entry since its day prints in full, with its target, the majors first",
+                text.split("\n")[1:3] == [score.T_ENTRY.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="BTC",
+                                                                entry="105", stop="100.6", dist="\u22124.2")
+                                          + score.T_LATE.format(date="03.03"),
+                                          score.T_PLAN.format(target="113.8", tdist="+8.4")
+                                          + score.T_PLAN_SIZE.format(notional="3580", margin="1193", lev=3)])
+        with open(os.path.join(h.state, score.RECORD), "w", encoding="utf-8") as fh:
+            json.dump({"v": 1, "k": "score", "ts": "1970-03-05T00:10:00Z", "asof": "1970-03-04"}, fh)
+        code, printed, alerts, ledger, record = h.run(70)
+        text = alerts[0][1] if alerts else ""
+        s.check("after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop",
+                score.T_HELD_DONE.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="BTC", stop="105")
+                in text.split("\n") and score.T_ENTRY.split("**")[0] not in "\n".join(text.split("\n")[1:2]))
+        # The owner's file unreadable: no size and no ceilings; majors first among the day's entries.
+        h = AbHost(os.path.join(tmp, "j"), {"AAAUSDT": long_world, "ETHUSDT": long_world}, own=None)
+        h.run(60)
+        code, printed, alerts, ledger, record = h.run(62)
+        text = alerts[0][1] if alerts else ""
+        heads = [x for x in text.split("\n") if x.startswith(score.DOT[1] + " **")]
+        s.check("an entry without the owner's file: two lines, the target alone on the second, no size, no ceilings",
+                code == 0 and len(heads) == 2 and score.T_PLAN_SIZE.split("`")[0] not in text
+                and score.T_LIMIT.split("{")[0] not in text
+                and text.split("\n").count(score.T_PLAN.format(target="113.8", tdist="+8.4")) == 2
+                and text.split("\n")[-2:] == [score.T_HOW, score.T_WHEN])
+        s.check("the day's entries print BTC ETH SOL BNB XRP first, then the others in the list's order",
+                [x.split("**")[1] for x in heads] == [score.SIDE_HEAD[1] + " ETH", score.SIDE_HEAD[1] + " AAA"])
+        # The look at the day still forming (TZ-80): what the day has done, and what its close would do.
+        h = AbHost(os.path.join(tmp, "n"), {"AAAUSDT": long_world, "BTCUSDT": short_world, "BADUSDT": OSError("refused")})
+        h.run(60)
+        before = sorted(os.listdir(h.state)), h.record(), sorted(os.listdir(h.outbox))
+        rising, falling = (100.0, 104.0, 100.0, 103.5), (100.0, 100.0, 95.0, 96.0)
+        code, printed, alerts, looked = h.look(60, {"AAAUSDT": rising, "BTCUSDT": falling})
+        s.check("the look: exit 0, one line of the fixed shape",
+                code == 0 and printed.count("\n") == 1 and AB_LOOK.fullmatch(printed.rstrip("\n")) is not None)
+        s.check("the look: the line reads day=1970-03-02 symbols=3 read=2 unread=1, two entries and nothing else, alert=yes",
+                [ab_field(printed, f) for f in ("day", "symbols", "read", "unread", "stopped", "scaled", "entries",
+                                                "alert")]
+                == ["1970-03-02", "3", "2", "1", "0", "0", "2", "yes"])
+        text = alerts[0][1] if alerts else ""
+        s.check("the look: one alert, of kind alert, its head the day and the nine hours to its close",
+                len(alerts) == 1 and alerts[0][0] == "alert" and text.split("\n")[0] == score.F_HEAD.format(d="02.03", h=9))
+        s.check("the look: a close below the 55-day low would open a short -- the last price, the level it crossed, "
+                "the stop 2 x 2.15 above it and the target 4 x 2.15 below, BTC before the others",
+                text.split("\n")[1:3] == [
+                    score.F_ENTRY.format(side=score.SIDE[-1], sym="BTC", last="96") + score.F_LEVEL.format(level="99"),
+                    score.F_ENTRY_PLAN.format(stop="100.3", target="87.4")])
+        s.check("the look: a close above the 55-day high would open a long -- the stop 2 x 2.1 below the last price, "
+                "the target 4 x 2.1 above",
+                text.split("\n")[3:5] == [
+                    score.F_ENTRY.format(side=score.SIDE[1], sym="AAA", last="103.5") + score.F_LEVEL.format(level="101"),
+                    score.F_ENTRY_PLAN.format(stop="99.3", target="111.9")])
+        s.check("the look: a candidate is named one, and the last line says the close alone confirms it",
+                text.split("\n")[5:] == [score.F_FOOT] and text.count(score.F_ENTRY.split("{side}")[0]) == 2
+                and score.T_ENTRY.split("{entry}")[0].split("\u00b7")[1] not in text
+                and score.T_PLAN_SIZE.split("`")[0] not in text)
+        s.check("the look's record: keys v k ts day symbols unread stopped scaled entries, in order, mode 0640",
+                looked is not None and list(looked) == ["v", "k", "ts", "day", "symbols", "unread", "stopped", "scaled",
+                                                        "entries"]
+                and os.stat(os.path.join(h.state, score.FORMING, "1970-03-02.json")).st_mode & 0o7777 == 0o640)
+        s.check("the look's record: v 1, k score-forming, its day, the unread symbol, the entries it named with their sides",
+                looked is not None and (looked["v"], looked["k"], looked["day"], looked["symbols"], looked["unread"])
+                == (1, "score-forming", "1970-03-02", 3, ["BADUSDT"])
+                and looked["entries"] == [{"symbol": "BTCUSDT", "side": -1}, {"symbol": "AAAUSDT", "side": 1}]
+                and (looked["stopped"], looked["scaled"]) == ([], [])
+                and looked["ts"] == "1970-03-02T15:10:02Z")
+        s.check("the look opens no trade and writes no ledger: the daily close's record stands, one directory is new",
+                sorted(os.listdir(h.state)) == sorted(before[0] + [score.FORMING]) and h.record() == before[1]
+                and h.ledger() is None and h.ledger(score.PLAN) is None
+                and os.listdir(os.path.join(h.state, score.FORMING)) == ["1970-03-02.json"])
+        stamp = os.stat(os.path.join(h.state, score.FORMING, "1970-03-02.json"))
+        asked = len(h.urls)
+        code, printed, alerts, again = h.look(60, {"AAAUSDT": rising, "BTCUSDT": falling})
+        s.check("a day already looked at: exit 0, nothing read, nothing told, its record not reopened",
+                code == 0 and alerts == [] and len(h.urls) == asked and again == looked
+                and printed == "score: forming day=1970-03-02 already looked at, nothing written\n"
+                and (stamp.st_ino, stamp.st_mtime_ns)
+                == tuple(getattr(os.stat(os.path.join(h.state, score.FORMING, "1970-03-02.json")), k)
+                         for k in ("st_ino", "st_mtime_ns")))
+        code, printed, alerts, ledger, record = h.run(61)
+        text = alerts[0][1] if alerts else ""
+        s.check("the close after it: both candidates are entries, and the close counts the look -- 2 of 2 named, 2 made",
+                code == 0 and ab_field(printed, "look") == "2/2/2" and record["look"] == {"named": 2, "hit": 2, "entries": 2}
+                and ab_field(printed, "opened") == "2"
+                and [x.split("**")[1] for x in text.split("\n") if x.startswith((score.DOT[1], score.DOT[-1]))]
+                == [score.SIDE_HEAD[-1] + " BTC", score.SIDE_HEAD[1] + " AAA"])
+        code, printed, alerts, looked = h.look(63, {"BTCUSDT": (103.0, 104.0, 102.0, 103.0), "AAAUSDT": (107.0, 109.0, 106.0, 108.0)})
+        s.check("a stop of an earlier day is not the look's to tell, nor an entry made at today's open a candidate",
+                code == 0 and alerts == [] and (looked["stopped"], looked["entries"]) == ([], [])
+                and ab_field(printed, "alert") == "no")
+        taken = list(long_world)
+        taken[60] = (60 * book.DAY_MS, 100.0, 104.0, 99.5, 100.5)
+        h = AbHost(os.path.join(tmp, "o"), {"AAAUSDT": taken})
+        h.run(60)
+        code, printed, alerts, looked = h.look(60, {"AAAUSDT": rising})
+        named = ab_field(printed, "entries")
+        code, printed, alerts, ledger, record = h.run(61)
+        s.check("a candidate the close took back: no entry is told, and the close counts 0 of 1 named, 0 made",
+                named == "1" and alerts == [] and ab_field(printed, "look") == "0/1/0"
+                and record["look"] == {"named": 1, "hit": 0, "entries": 0} and record["open"] == [])
+        h = AbHost(os.path.join(tmp, "p"), {"AAAUSDT": long_world})
+        h.run(60)
+        code, printed, alerts, looked = h.look(60, {"AAAUSDT": (100.0, 100.8, 99.6, 100.4)})
+        s.check("a day that has done nothing and would do nothing: no alert, and still a record, with nothing named",
+                code == 0 and alerts == [] and ab_field(printed, "alert") == "no" and looked is not None
+                and (looked["stopped"], looked["scaled"], looked["entries"]) == ([], [], []))
+        code, printed, alerts, ledger, record = h.run(61)
+        s.check("an entry the look did not name: the close counts 0 of 0 named, 1 made",
+                ab_field(printed, "look") == "0/0/1" and record["look"] == {"named": 0, "hit": 0, "entries": 1})
+        code, printed, alerts, looked = h.look(68, {"AAAUSDT": (112.0, 114.0, 111.0, 113.5)})
+        text = alerts[0][1] if alerts else ""
+        s.check("a day that has reached the target: told as done, half closing at 113.8, with no candidate's last line",
+                code == 0 and text.split("\n")[1:] == [score.F_SCALE.format(sym="AAA", side=score.SIDE[1], px="113.8")]
+                and ab_field(printed, "scaled") == "1" and looked["scaled"] == ["AAAUSDT"] and looked["entries"] == [])
+        code, printed, alerts, ledger, record = h.run(69)
+        text = alerts[0][1] if alerts else ""
+        s.check("the close after it tells the target with the rest's stop, which the look does not move",
+                len(alerts) == 1 and text.split("\n")[1] == score.T_SCALED.format(sym="AAA", side=score.SIDE[1], px="113.8",
+                                                                                   stop="105")
+                and score.T_SCALED.split("`{stop}`")[0].split(", ")[1] not in score.F_SCALE
+                and ab_field(printed, "look") == "0/0/0")
+        code, printed, alerts, looked = h.look(70, {"AAAUSDT": (114.0, 114.5, 104.0, 104.5)})
+        text = alerts[0][1] if alerts else ""
+        s.check("a day that has reached the rest's stop at the entry: told as done, at 105",
+                code == 0 and text.split("\n")[1:] == [score.F_STOP.format(sym="AAA", side=score.SIDE[1], px="105")]
+                and ab_field(printed, "stopped") == "1" and looked["stopped"] == ["AAAUSDT"])
+        code, printed, alerts, looked = h.look(100, {"AAAUSDT": (144.0, 144.5, 121.0, 122.0)})
+        text = alerts[0][1] if alerts else ""
+        s.check("a close below the 20-day low would leave the long: the look tells nothing of it, the close does",
+                code == 0 and alerts == [] and ab_field(printed, "alert") == "no"
+                and (looked["stopped"], looked["scaled"], looked["entries"]) == ([], [], []))
+        h = AbHost(os.path.join(tmp, "s"), {"DAYUSDT": long_world, "BBBUSDT": long_world})
+        code, printed, alerts, looked = h.look(61, {"DAYUSDT": (105.0, 107.0, 100.0, 101.0), "BBBUSDT": (105.0, 106.0, 104.5, 105.5)},
+                                               shift={"BBBUSDT": -1})
+        text = alerts[0][1] if alerts else ""
+        s.check("an entry made at today's open and stopped today is a stop told, at 100.6",
+                code == 0 and text.split("\n")[1:] == [score.F_STOP.format(sym="DAY", side=score.SIDE[1], px="100.6")])
+        s.check("a symbol whose forming day is not today is unread, and nothing of it is told",
+                looked["unread"] == ["BBBUSDT"] and ab_field(printed, "unread") == "1" and "BBB" not in text)
+        s.check("no number of the look carries a float's tail or an exponent, and no symbol its USDT",
+                all(re.fullmatch(r"\d+(\.\d{1,8})?", span) for span in re.findall(r"`([^`]*)`", text))
+                and "USDT" not in text and bool(re.findall(r"`([^`]*)`", text)))
+        h = AbHost(os.path.join(tmp, "v"), {"BTCUSDT": short_world})
+        code, printed, alerts, looked = h.look(62, {"BTCUSDT": (103.0, 104.0, 102.0, 103.0)})
+        text = alerts[0][1] if alerts else ""
+        s.check("a day that opened beyond the short's stop and would close above the 55-day high: the stop told at the "
+                "open, and the long a candidate with the stop 2 x 2.55 below the last price",
+                code == 0 and text.split("\n")[1:] == [
+                    score.F_STOP.format(sym="BTC", side=score.SIDE[-1], px="103"),
+                    score.F_ENTRY.format(side=score.SIDE[1], sym="BTC", last="103"),
+                    score.F_ENTRY_PLAN.format(stop="97.9", target="113.2"), score.F_FOOT]
+                and looked["entries"] == [{"symbol": "BTCUSDT", "side": 1}] and looked["stopped"] == ["BTCUSDT"])
+        h = AbHost(os.path.join(tmp, "t"), {"BADUSDT": OSError("refused"), "WORSEUSDT": ValueError("no day")})
+        code, printed, alerts, looked = h.look(61)
+        s.check("the look with no symbol read: exit 4, nothing written, nothing told",
+                code == 4 and alerts == [] and looked is None and os.listdir(h.state) == []
+                and printed == "score: forming day=1970-03-03 symbols=2 read=0 nothing written\n")
+        saved_get = book._get
+        try:
+            book._get = lambda url: ab_klines(long_world[:61], 105.0, (105.0, 107.5, 104.0, 106.5))
+            bars, today = book.live_day("AAAUSDT", 61 * book.DAY_MS + AB_LOOK_MS)
+            s.check("live_day: the closed days, and the day still forming as a bar whose close is the last price",
+                    bars == long_world[:61] and today == (61 * book.DAY_MS, 105.0, 107.5, 104.0, 106.5)
+                    and book.live_bars("AAAUSDT", 61 * book.DAY_MS + AB_LOOK_MS) == (bars, 105.0))
+        finally:
+            book._get = saved_get
         # GO_LIVE cuts the ledger by the entry's day.
         score.GO_LIVE = "1970-03-04"
         h = AbHost(os.path.join(tmp, "g"), {"AAAUSDT": long_world})
@@ -3495,8 +3746,68 @@ def section_ab(s):
     finally:
         score.GO_LIVE, score.FUNDING_PAGE = saved_live, saved_page
         shutil.rmtree(tmp, ignore_errors=True)
+    # The plan's replay (TZ-80): one loop with the rule's, the target its only difference.
+    eps_r = 1e-9
+    rule_trades, _ = book.replay(long_world)
+    plan_trades, _ = book.replay(long_world, scale=book.SCALE_R)
+    s.check("SCALE_R is 2.0, and the rule's replay carries no target",
+            book.SCALE_R == 2.0 and len(rule_trades) == 1 and "t_scale" not in rule_trades[0] and "stop_now" not in rule_trades[0])
+    pt = plan_trades[0] if plan_trades else {}
+    s.check("the plan's trade: half at the target the day it is reached, its stop the initial one",
+            len(plan_trades) == 1 and pt.get("t_scale") == 68 * book.DAY_MS and abs(pt.get("scale_px", 0) - 113.8) < eps_r
+            and abs(pt.get("stop", 0) - 100.6) < eps_r and pt.get("stop_now") == 105.0
+            and (pt.get("exit"), pt.get("why")) == (122.0, "channel"))
+    gap = list(long_world)
+    gap[62] = (62 * book.DAY_MS, 120.0, 121.0, 119.0, 120.0)
+    pt = (book.replay(gap, scale=book.SCALE_R)[0] or [{}])[0]
+    s.check("a day that opens beyond the target closes half at its open",
+            pt.get("t_scale") == 62 * book.DAY_MS and pt.get("scale_px") == 120.0)
+    both = list(long_world)
+    both[62] = (62 * book.DAY_MS, 105.0, 115.0, 100.0, 106.0)
+    tr = (book.replay(both, scale=book.SCALE_R)[0] or [{}])[0]
+    s.check("a day that reaches the stop and the target is a stop: nothing closes at the target",
+            tr.get("why") == "stop" and tr.get("exit") == 100.6 and "t_scale" not in tr)
+    same = list(long_world)
+    same[68] = (68 * book.DAY_MS, 112.0, 114.0, 104.5, 113.0)
+    tr = (book.replay(same, scale=book.SCALE_R)[0] or [{}])[0]
+    s.check("the moved stop acts from the next day: the target's day reaching below the entry closes nothing more",
+            tr.get("t_scale") == 68 * book.DAY_MS and (tr.get("exit"), tr.get("why")) == (122.0, "channel"))
+    back = list(long_world)
+    back[69] = (69 * book.DAY_MS, 112.0, 113.0, 104.0, 106.0)
+    tr = (book.replay(back, scale=book.SCALE_R)[0] or [{}])[0]
+    want_back = (0.5 * (113.8 / 105.0 - 1) - 2 * book.COST_SIDE) / (4.4 / 105.0)
+    s.check("after the target, a day through the entry closes the rest at the entry; its R is half the target's",
+            (tr.get("exit"), tr.get("why"), tr.get("k_exit")) == (105.0, "stop", 69)
+            and abs(book.result_r(tr, []) - want_back) < eps_r)
+    saved_get = book._get
+    try:
+        book._get = lambda url: ab_klines(long_world[:70], long_world[70][1])
+        with contextlib.redirect_stdout(io.StringIO()) as out:
+            book.main(["--live", "--scale", "2", "AAAUSDT"])
+        live_plan = json.loads(out.getvalue())
+        s.check("--live --scale 2 prints the plan's state: the target's day and the stop at the entry",
+                live_plan.get("scale_date") == "1970-03-10" and live_plan.get("stop_now") == 105.0
+                and live_plan == json.loads(json.dumps(book.live_state("AAAUSDT", 70 * book.DAY_MS + 5, 2.0)[0],
+                                                       sort_keys=True)))
+    finally:
+        book._get = saved_get
+    s.check("the ceilings are paper.ceilings: 3 % and 5 % at 0.5 % hold 6 and 10", paper.ceilings(AB_OWN) == (6, 10))
+    size = paper.copy_size(AB_OWN, 4.4 / 105.0)
+    s.check("the size is paper.copy_size: 150 USDT over a stop 4.4 of 105 away is 3579.5 USDT, a third of it at 3x",
+            abs(size[0] - 150 * 105.0 / 4.4) < 1e-6 and abs(size[1] - 50 * 105.0 / 4.4) < 1e-6 and size[2:] == (3, 150.0))
+    s.check("the leverage is COPY_LEV while the stop stands within a quarter of the entry, 2x to a third, 1x beyond",
+            paper.COPY_LEV == 3 and [paper.copy_lev(d) for d in (0.022, 0.25, 0.2501, 1 / 3.0, 0.34, 0.6)] == [3, 3, 2, 2, 1, 1])
+    wide = score.entry_lines({"symbol": "WIDEUSDT", "state": "short", "entry": 100.0, "stop": 130.0, "target": 40.0,
+                              "entry_due": True}, AB_OWN)
+    s.check("an entry whose stop stands 30 % away: 500 USDT, its margin 250 at 2x, since 3x would liquidate first",
+            wide[1] == score.T_PLAN.format(target="40", tdist="\u221260.0")
+            + score.T_PLAN_SIZE.format(notional="500", margin="250", lev=2))
+    s.check("the copy line's margin is the same function's: a copy whose stop is 30 % away is stated at 2x",
+            "`500` USDT" in paper.copy_text(AB_OWN, 0.30, -1, [-1]) and "`250`" in paper.copy_text(AB_OWN, 0.30, -1, [-1])
+            and "2x" in paper.copy_text(AB_OWN, 0.30, -1, [-1]) and "3x" in paper.copy_text(AB_OWN, 0.10, -1, [-1]))
     s.check("the default state is /var/lib/crypto-auto, the ledger score-ledger/ and the record score.json",
-            common.STATE_DIR == "/var/lib/crypto-auto" and (score.LEDGER, score.RECORD) == ("score-ledger", "score.json"))
+            common.STATE_DIR == "/var/lib/crypto-auto" and (score.LEDGER, score.RECORD) == ("score-ledger", "score.json")
+            and (score.PLAN, score.FORMING) == ("score-plan", "score-forming"))
     # The units and the manifest.
     service, timer = unit_lines("crypto-score.service"), unit_lines("crypto-score.timer")
     s.check("service runs as User=cryptoauto, Group=cryptoauto",
@@ -3520,8 +3831,26 @@ def section_ab(s):
         listed = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
     s.check("the manifest lists crypto-score.timer once and not its service",
             listed.count("crypto-score.timer") == 1 and "crypto-score.service" not in listed)
-    s.check("no unit of vps/units starts a model from a timer: crypto-score.service names no claude",
-            not [x for x in service if "claude" in x.lower()])
+    look_service, look_timer = unit_lines("crypto-score-forming.service"), unit_lines("crypto-score-forming.timer")
+    s.check("the look's service runs /usr/bin/python3 /srv/crypto-auto/vps/score.py --forming",
+            [x for x in look_service if x.startswith("ExecStart")]
+            == ["ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/score.py --forming"])
+    s.check("the look's service is the close's but for its description and its command: the same user, the same "
+            "confinement, no credential",
+            [x for x in look_service if not x.startswith(("Description=", "ExecStart="))]
+            == [x for x in service if not x.startswith(("Description=", "ExecStart="))]
+            and len([x for x in look_service if x.startswith(("Description=", "ExecStart="))]) == 2)
+    s.check("the look's timer fires at OnCalendar=*-*-* 15:10:00 UTC and is not Persistent: a look not made at its "
+            "hour is not made at another",
+            [x for x in look_timer if x.startswith("OnCalendar")] == ["OnCalendar=*-*-* 15:10:00 UTC"]
+            and not [x for x in look_timer if x.startswith("Persistent")])
+    s.check("the look's timer's unit is crypto-score-forming.service, WantedBy=timers.target",
+            [x for x in look_timer if x.startswith("Unit=")] == ["Unit=crypto-score-forming.service"]
+            and "[Install]" in look_timer and "WantedBy=timers.target" in look_timer)
+    s.check("the manifest lists crypto-score-forming.timer once and not its service",
+            listed.count("crypto-score-forming.timer") == 1 and "crypto-score-forming.service" not in listed)
+    s.check("no unit of vps/units starts a model from a timer: neither score service names a claude",
+            not [x for x in service + look_service if "claude" in x.lower()])
 
 
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
diff --git a/vps/units/crypto-score-forming.service b/vps/units/crypto-score-forming.service
new file mode 100644
index 0000000..a3b7658
--- /dev/null
+++ b/vps/units/crypto-score-forming.service
@@ -0,0 +1,20 @@
+[Unit]
+Description=Crypto assistant: the book's look at the day still forming
+Wants=network-online.target
+After=network-online.target
+
+[Service]
+Type=oneshot
+User=cryptoauto
+Group=cryptoauto
+ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/score.py --forming
+Environment=PYTHONDONTWRITEBYTECODE=1
+NoNewPrivileges=yes
+CapabilityBoundingSet=
+ProtectSystem=strict
+ProtectHome=yes
+PrivateTmp=yes
+ReadWritePaths=/var/spool/crypto-auto /var/lib/crypto-auto
+MemoryAccounting=yes
+MemoryMax=64M
+TimeoutStartSec=900
diff --git a/vps/units/crypto-score-forming.timer b/vps/units/crypto-score-forming.timer
new file mode 100644
index 0000000..caa341e
--- /dev/null
+++ b/vps/units/crypto-score-forming.timer
@@ -0,0 +1,9 @@
+[Unit]
+Description=Crypto assistant: the book's look at the day still forming, 15:10 UTC
+
+[Timer]
+OnCalendar=*-*-* 15:10:00 UTC
+Unit=crypto-score-forming.service
+
+[Install]
+WantedBy=timers.target
```
