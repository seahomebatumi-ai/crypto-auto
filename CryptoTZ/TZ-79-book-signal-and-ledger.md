# TZ-79 — The book's signal and its forward ledger: every entry and exit the trend book makes on the list reaches the owner the day it is made, with no model, and every trade it closes is scored once

**Canonical filename:** `CryptoTZ/TZ-79-book-signal-and-ledger.md`
**Report:** `CryptoReports/TZ-79-book-signal-and-ledger-report.md`
**Class:** branch TZ (contract §8) — it authorises six repository files besides its report.
**Branch:** `claude/tz-79-book-signal-and-ledger`
**Host:** the VPS, for stage C; stages A–B run on any clone.
**Model:** Sonnet — the change is the patch of §10, written by the Architect and run by it under Python 3.11, 3.12 and
3.13 before this TZ shipped; the session applies it, proves its bytes and runs the validation. Nothing in it is
diagnosis or design.
**Trigger:** `EXECUTE TZ-79`, with nothing under it: no credential arrives and the Boss is asked for nothing.
**Previous TZ:** TZ-78, accepted 06.11.2026 and merged at `f813ff9` (pull request #64); no branch on the remote is
ahead of `main`.
**Issued:** 13.11.2026, by the Architect.
**Written against:** contract v31, map `2026-11-12-a`, methodology `2026-10-26-a`, and `main` at `10f926a` — its
`vps` tree `de6f1c635811b3ee5b24456e8b534edd9c41764b` — read from the repository on 13.11.2026.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-12-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-12-a.**` |
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
| `vps/book.py` | 297 | `8478a66a57ad4c48b2579e8cb0e382d9` | equal, or A1 stops: §10 is written against these bytes |
| `vps/selftest.py` | 3173 | `f79b05657550180ad9f18603cda5cec1` | equal, or A1 stops: §10 is written against these bytes, TZ-78's merged file |
| `vps/manifest` | 9 | `75a0f5a71f6111ecca0553620f1eea4c` | equal, or A1 stops: §10 is written against these bytes |
| `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` | reported: the patch does not touch it and V5 copies it |
| `vps/writer.py` | 154 | `c07b1f71ef014e18448eb9313e185b73` | reported: the patch does not touch it and V5 copies it |

The map itself: 2805 lines, MD5 `7f699795a4ef996a15861167bbcae2d7` — reported, not enforced.

---

## 1. What changes, and the evidence for it

**This is step 1 of the build order the map fixed at `2026-11-12-a`** (§10, «Standing decisions»): the scorecard and
the book's signal in code. It executes three rows of that section — «The book's signals reach the owner only when he
presses», «The gate's hundred trades are out of reach of the presses» and «The engine's published book had never been
scored».

**The evidence, measured by the Architect on the day logs on 12.11.2026.** The book decides at 00:00 UTC and reaches
the owner only inside an analysis he starts: of the eight positions the book of 06.11.2026 had opened on list coins
since 24.10, the answers carried two as entries, five opened on days with no run, and one lost its budget to the one
object a side. Nothing scores the rule forward: the published book was scored three times by hand, and the gate that
keeps real money out asks for a hundred closed trades which the answers — two funded entries in five presses and
twenty-two days — cannot reach.

**What is built — one program, one timer, no model:**

1. **`vps/book.py` gains `live_state(symbol, now_ms)`** — the three lines `main()` ran for `--live`, moved into one
   function that returns the state `--live` prints together with the replay's trades and position. `--live` prints
   through it. No rule, constant or other function of the file moves.
2. **`vps/score.py`** — §3.
3. **`vps/units/crypto-score.service` and `vps/units/crypto-score.timer`**, the timer named in `vps/manifest`: a oneshot
   as `cryptoauto` at 00:10 UTC every day, `Persistent=true`, reading no credential.
4. **`vps/selftest.py`**: `import score` and section AB — sixty-two checks against stubs, no network.

*[Architect's decisions, TZ-79.* **The gate of map §10, row «The engine places no order on the exchange», reads this
ledger** — the rule on every list coin, entries from 2026-10-21 — because from the day the unit is installed every
entry and exit the rule makes reaches the owner, so the rule's record is the record of what he is told; discarded: the
answers' funded subset, which that arithmetic puts years away. **The book is read live, through the function `--live`
prints from;** discarded: `--archive`, whose files lag the close and whose cache keeps a month's 404 from before the
month was published (`vps/book.py`, `archive_series`). **One file per closed trade;** discarded: one growing file,
reopened at every close (inv. 38). **No size and no leverage in the alert:** production's ceilings live in
`index.html` and reach code at step 2, and the alert says where they are printed. **No alert on a day the book made
nothing.** **The ledger stays on the VPS in this TZ:** its commit to the repository needs a row of the contract's
class table and is the first item of step 2, and the gate reads nothing until it is there.*]*

---

## 2. Text this TZ obeys

- Contract §7 item 1: «**No change to scoring, leverage, liquidation or geometry math** unless the TZ explicitly cites a
  completed backtest» — none is touched. The rule is `book.replay()`, which does not move; `live_state()` is the three
  lines `main()` ran, moved; a trade's R is `book.result_r()` and a total is `book.summary()`.
- Contract §7 item 9: «**A program in this repository that a VPS unit runs, and whose output that unit commits, has a
  workflow step's standing on the same terms**» — the unit of this TZ commits nothing yet, so its ledger has no such
  standing until step 2 commits it, and §1 says so. «**Measuring the session's own environment is a DIFFERENT act and is
  permitted**» — V5's reads measure this machine, are recorded beside their commands, write only a scratch directory
  the session removes, and produce no product fact.
- Contract §7 item 15: «An implementation session never enables, starts or leaves running a persistent unit, timer or
  service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its report
  proves none is left behind.»
- Map inv. 38: «**A second implementation of any rule, threshold or formula is banned in any language and any file.**»
  — the program composes `book.live_state`, `book.result_r`, `book.summary` and `writer.payload_symbols` and implements
  none of them; «A file once written is never reopened» — a closed trade is one file, written once.
- Map inv. 70: «**A transport failure is NOT an absence of data.**» — a span of funding prints that did not arrive whole
  prices nothing: the trade is counted pending and asked for again.
- Map inv. 72: «**A write that fails leaves this run's product or nothing — never a partial file and never the previous
  run's.**» — every file is written by `common.atomic_write`.
- Map inv. 22: «**A check that passes with no data is forbidden.**» — V5 fails on `read=0`.
- Map §10, row «The assistant's build sequence»: «the watchers keep alerting him and he decides whether to press» — the
  unit alerts and starts no run, and no unit of this TZ names a model.
- The tree's own convention, measured on `main` at `10f926a`: no file under `vps/` carries a raw Cyrillic letter; the
  owner's language is written as `\uXXXX` escapes. V2 holds `vps/score.py` to it.

---

## 3. `vps/score.py` — registered

- **Invocation.** `score.py [--state DIR] [--outbox DIR]`; the defaults are `/var/lib/crypto-auto` and the bot's outbox.
- **The list** is `writer.payload_symbols()` on the checkout the program sits in: `BTCUSDT`, then `tokens[]`.
- **The book** is `book.live_state()` for each symbol. A symbol whose read raises, or whose last closed day is not the
  day the others stand on, is unread today and named in the record. No symbol read, or a read older than the record's
  day: exit 4, nothing written.
- **The ledger** is `<state>/score-ledger/<SYMBOL>-<entry stamp>.json`, one closed trade a file with the keys `symbol`,
  `side`, `t_entry`, `entry`, `stop`, `t_exit`, `exit`, `why`, `r`, `seen`, in that order. A trade is written when a run
  finds it closed, its entry day on or after `GO_LIVE`, its key not yet written, and its close no more than
  `RETRY_DAYS` before the day the run stands on; an empty ledger reaches back to `GO_LIVE`. A file that stands is never
  opened for writing: a later replay that reads its trade differently is counted `disagree`, and a close found later
  than `RETRY_DAYS` is counted `late` and never written. A file that is not the trade its name says: exit 5, nothing
  written.
- **The result.** `r` is `book.result_r()` on the funding prints of the trade's span, read from
  `fapi.binance.com/fapi/v1/fundingRate` with `startTime`, `endTime` and `limit=1000`, page by page. The read is refused
  unless whole: a list, every rate finite, the first print inside the span within `FUNDING_GAP_MS` of the entry, the
  last within it of the exit, no wider gap between two. A refused read writes nothing, counts the trade `pending`,
  names it on a line `score: pending <SYMBOL> <exception class>`, and is asked again by the next run. A trade stopped
  on its entry day has no span and asks for nothing.
- **The alert** is of kind `alert` and is written when the run is the first one (the baseline), or the day is new and
  the book opened or is closing a position, or a trade was written since the record the run replaces. One event to a
  line: an entry with its fill and its stop as code spans and the stop's distance; an entry made on a day with no run,
  with that day; an exit due at today's open; a closed trade with its R. Then the rule's record since `GO_LIVE` —
  closed, total R, winners, the five symbols of `MAJORS` and the others apart — and the open positions by side with
  their R at the last close. The baseline names every position held and says what R is. A day read twice tells
  nothing twice.
- **The record** is `<state>/score.json`, replaced whole: `v` 1, `k` `score`, `ts`, `asof`, `since`, `symbols`,
  `unread`, `open`, `closed` — `all`, `majors` and `others`, each `book.summary()` with the profit factor of a record
  without a loss as null — `pending`, `late`, `disagree`.
- **The line** is `score: asof=… symbols=… read=… unread=… open=… opened=… closing=… closed=… pending=… late=…
  disagree=… ledger=… alert=yes|no`, and it never carries a price.
- **The order of writes** is the ledger, the alert, the record: a run that dies between the last two tells the owner
  twice rather than not at all.

| Constant | Value | Derived |
|---|---|---|
| `GO_LIVE` | `2026-10-21` | methodology `2026-10-21-a`: the first day every level the answer prints is this book's |
| `MAJORS` | BTC, ETH, SOL, BNB, XRP | map §10, row «The book's out-of-sample loss sits in the alts»: the five its lead names, totalled apart from the first forward day, so that the lead is read on trades it has not seen |
| `RETRY_DAYS` | 60 | the Architect's probe of 12.11.2026 — twelve random markets, 455 daily runs on a 400-row window, three seeds. Unbounded, the ledger took 266, 253 and 296 trades the full history never made; at 200 days 21, 0 and 0; at 120, 60 and 30 none, and every trade equal to the full history's — 77 of 77, 80 of 80, 71 of 71. The state the window prints equalled the full history's on 5 472 symbol-days of the same markets |
| `FUNDING_GAP_MS` | eight hours and one minute | no USD-M perpetual settles less often than every eight hours, so a wider gap is a span read in part |
| the timer | 00:10 UTC | the daily bar closes at 00:00 UTC and the book fills at the open that follows |
| `TimeoutStartSec` | 900 | thirty-one reads at `book.HTTP_TIMEOUT_S`, 20 s, are 620 s at worst |
| `MemoryMax` | 64M | `crypto-etf.service`'s ceiling, for a program of the same kind |

**What the Architect could not probe, and V5 reads.** `fapi.binance.com` refuses the Architect's session, so no live
read of this program has been taken: stubs stand behind every check of section AB, and the exchange stands behind V5,
whose answers are therefore required by their shape.

---

## 4. Scope

### Files to Create
- `vps/score.py`, `vps/units/crypto-score.service`, `vps/units/crypto-score.timer` — §10.

### Files to Modify
- `vps/book.py` — §10: `live_state()` and the one line of `main()` that calls it.
- `vps/selftest.py` — §10: `import score`, section AB and its entry in `SECTIONS`.
- `vps/manifest` — §10: the line `crypto-score.timer`.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
The scratch directory `/var/lib/crypto-auto/tz79` and the two transient units of V5, all gone before the report. No
unit, timer or file under `/etc` is created, changed or restarted, nothing is enabled from the branch, and the bot's
outbox receives nothing from this session: the signal takes effect when the deployer installs the merge.

### Not touched
`index.html`, `main.py`, `vps/run.py`, `vps/bot.py`, `vps/common.py`, `vps/writer.py`, every other unit, `bench.yml`,
`analyst/**`, the map, the contracts.

---

## 5. Stages

### Stage A — readings, no writes
- **A0.** Contract §4a steps 1–6; the gate of §0, every anchor cut from the map's own table.
- **A1.** The added files of §0 at their lines and MD5. A difference in `vps/book.py`, `vps/selftest.py` or
  `vps/manifest` stops the TZ, BLOCKED, naming the file.
- **A2.** On the VPS, the baseline from `main`: `python3 vps/selftest.py` prints `selftest: sections 27 checks 662
  failed 0 empty 0` and `section X: checks 19 failed 0`. *Measured by the Architect on `10f926a`'s tree under Python
  3.11, 3.12 and 3.13.* A different baseline is recorded per section and the TZ goes on: stage C compares against what
  A2 read.
- **A3.** `systemctl list-unit-files 'crypto-score*' --no-legend` and `ls /var/lib/crypto-auto`, kept for V7.

### Stage B — the code, on the branch
- **B1.** Branch `claude/tz-79-book-signal-and-ledger` from `origin/main`. Extract §10's patch with the one command

  ```sh
  awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-79-book-signal-and-ledger.md > /tmp/tz79.patch
  ```

  and record its lines and MD5 — 818 and `fec59ef4597d7ac2aa372811533d0f95` as written; an upload that strips the patch's
  blank context lines changes the hash and not the result, which B2 decides.
- **B2.** `git apply /tmp/tz79.patch`. **Required:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/book.py` | 304 | `4b64b856fb80cfa810dcac015eb60b20` |
  | `vps/manifest` | 10 | `73d8fd4022bcf24996d4d3c41c6444c5` |
  | `vps/score.py` | 317 | `308c8661b54d843a682747e46752bd4e` |
  | `vps/selftest.py` | 3553 | `4816f38d10aa2711cc56fff29203c7a7` |
  | `vps/units/crypto-score.service` | 20 | `ca1e8d926d9ce2d9e2f2eabb4d7db41d` |
  | `vps/units/crypto-score.timer` | 10 | `06850cd5a678a0807bed58dc855cb48d` |

  Any other result is BLOCKED: the patch did not arrive as written, and no hand edit replaces it.
- **B3.** Commit with §7's implementation message, **locally, before stage C**, so that V4's restores return the
  committed files. Not pushed yet.

### Stage C — validation, on the VPS, on the committed branch
§6, in full.

### Stage D — push, pull request, report
Push; a pull request to `main` titled `TZ-79: vps — the book's signal and its forward ledger`, its body naming this TZ,
or the contract's §8 fallback. Then the report.

---

## 6. Validation

- **V1. Syntax.** `python3 -m py_compile vps/book.py vps/score.py vps/selftest.py` — exit 0.
- **V2. The bytes.** B2's six files at B2's lines and MD5s; and

  ```sh
  python3 -c "print(sum(0x400 <= ord(c) <= 0x4ff for c in open('vps/score.py', encoding='utf-8').read()))"
  ```

  prints `0`.
- **V3. Selftest**, on the VPS, on the branch: `python3 vps/selftest.py` — exit 0, `selftest: sections 28 checks 724
  failed 0 empty 0`, `section AB: checks 62 failed 0`, `section X: checks 19 failed 0`, **every other section's count
  equal to A2's**. *Measured by the Architect on the patched tree under Python 3.11, 3.12 and 3.13: the 662 checks of
  `main` do not move and section AB adds 62.* If A2 read another baseline: A2's total + 62.
- **V4. Negative controls** (inv. 22). Extract §9's script with the one command

  ```sh
  awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-79-book-signal-and-ledger.md > /tmp/tz79-controls.py
  ```

  — 60 lines, MD5 `a62c97667bf6cc10523e47d678c539fb` as written — and run `python3 /tmp/tz79-controls.py` from the clone's
  root. **Required:** exactly the 47 lines §9 prints after the script — MD5 `c5e9c76e981749cadb25781b930c8cde` — and then
  `git status --porcelain` prints nothing. Each control is one string replaced in one file, the selftest run, the file
  restored and its digest compared; all 724 checks run in each. *Measured by the Architect under Python 3.12 and 3.13,
  the two outputs identical.*
- **V5. The exchange, read once from this machine** — the one thing no stub can stand for. As root:

  ```sh
  install -d -o cryptoauto -g cryptoauto -m 0750 /var/lib/crypto-auto/tz79 /var/lib/crypto-auto/tz79/vps \
      /var/lib/crypto-auto/tz79/state /var/lib/crypto-auto/tz79/outbox
  install -o cryptoauto -g cryptoauto -m 0640 vps/score.py vps/book.py vps/common.py vps/writer.py \
      /var/lib/crypto-auto/tz79/vps/
  systemd-run --wait --collect --pipe --uid=cryptoauto --gid=cryptoauto -p ProtectSystem=strict \
      -p ReadWritePaths=/var/lib/crypto-auto/tz79 -p MemoryMax=64M -p Environment=PYTHONDONTWRITEBYTECODE=1 \
      /usr/bin/python3 /var/lib/crypto-auto/tz79/vps/score.py \
      --state /var/lib/crypto-auto/tz79/state --outbox /var/lib/crypto-auto/tz79/outbox
  ```

  The unit can write nothing but the scratch directory, so the bot's outbox is out of its reach. **Required, by shape:**
  exit 0; the last line printed is the line of §3 with `symbols=31`, `read` at least 1 (inv. 22), `asof` the UTC day
  before the run and `alert=yes`; exactly one file in the scratch outbox, of kind `alert`, whose first line ends with
  that day as `DD.MM` and carries «СДЕЛКИ ПРАВИЛА — подключено»; `state/score.json` parses, has mode `640`, `k` `score`, `since`
  `2026-10-21` and `symbols` 31; and the number of files in `state/score-ledger` equals the line's `ledger=`, each one
  parsing to the ten keys of §3. Then the same `systemd-run` command a second time. **Required:** `opened=0 closing=0
  closed=0 alert=no`, no second file in the scratch outbox, and `ls -li --time-style=full-iso` of the ledger directory
  identical to its listing before the second run. The report quotes every line both runs printed, the alert's text in
  full — it is the first message the owner receives after the merge — and the record's `unread`, `pending` and `late`.
  **Where `pending` is not 0** the TZ still completes: for the first symbol a `score: pending` line names, one
  `curl -sS -m 20` of `https://fapi.binance.com/fapi/v1/fundingRate?symbol=<SYMBOL>&limit=3` is recorded with its
  status, its byte count and the keys of its first row, and the audit decides. Then
  `rm -r /var/lib/crypto-auto/tz79`, and `systemctl list-units --all --no-legend 'run-*'` shows no unit of this session.
- **V6. Scope.** `git diff --numstat origin/main...HEAD` prints exactly six lines, tab-separated:

  ```text
  10	3	vps/book.py
  1	0	vps/manifest
  317	0	vps/score.py
  382	2	vps/selftest.py
  20	0	vps/units/crypto-score.service
  10	0	vps/units/crypto-score.timer
  ```
- **V7. Nothing in effect before the merge.** A3's two commands again, their output equal to A3's: no unit file named
  `crypto-score*` and no `score.json` or `score-ledger` under `/var/lib/crypto-auto`.
- **V8. The units.** `systemd-analyze verify vps/units/crypto-score.service vps/units/crypto-score.timer` — exit 0 and
  no output; and `systemd-analyze verify vps/units/*` — exit 0, as the installer requires before it installs anything.
  *The first measured by the Architect on systemd 255.* **A non-zero exit of the second is BLOCKED and nothing is
  pushed:** a merge would stop the deployer at that command.
- **V9. `bench.yml`.** `index.html` and `main.py` are untouched, so the standing checks do not apply; the report names
  the workflows that ran on the branch, from the runner where the session can, and that no step of the hosted gate
  runs `vps/selftest.py`, which the deployer runs before it installs.

**No regression:** the 662 checks of `main` are unchanged and green (V3), section X among them — the checks that read
`--live` through `main()` now read it through `live_state()`, and control 7 turns one of them red — and no file outside
§4 moves (V6).

---

## 7. Commit Message

Implementation: `TZ-79: vps — the book's signal and its forward ledger: every entry and exit the trend book makes on the list reaches the owner after the daily close, with no model, and every trade it closes is scored once`

Report: `TZ-79: report — the book's signal and its ledger`

---

## 8. The report

Contract §10 in full. Beside it: B1's command and the patch's lines and MD5; B2's lines and MD5s; A2's and V3's
per-section counts side by side; V4's output verbatim; V5's commands, every line they printed and the alert's text;
V7's and V8's outputs. The map's rows of step 1 and the gate's row are the Architect's to update after the audit, not
this TZ's.

---

## 9. The controls script (V4)

```python
#!/usr/bin/env python3
"""TZ-79, V4: eight negative controls. Each is one exact string replaced in one file of the working tree,
the selftest run, the file restored and its digest compared. Run from the repository root, on the branch."""
import hashlib
import subprocess
import sys

CONTROLS = (
    ("vps/score.py", "    fresh = baseline or asof > prev_asof\n", "    fresh = True\n"),
    ("vps/score.py", "            if key in known:\n", "            if key in known and False:\n"),
    ("vps/score.py", "            if day(tr[\"t_exit\"]) < floor:\n", "            if False:\n"),
    ("vps/score.py", "    if not inside or any(b - a > FUNDING_GAP_MS for a, b in zip(edges, edges[1:])):\n",
     "    if not inside:\n"),
    ("vps/score.py", "            if day(tr[\"t_entry\"]) < GO_LIVE:\n", "            if day(tr[\"t_exit\"]) < GO_LIVE:\n"),
    ("vps/score.py", "        opened = [o for o in open_rows if fresh and o[\"entry_date\"] > after]\n",
     "        opened = [o for o in open_rows if fresh and o[\"entry_date\"] >= after]\n"),
    ("vps/book.py", "    bars, open_now = live_bars(symbol, now_ms)\n    trades, pos = replay(bars, open_now)\n",
     "    bars, open_now = live_bars(symbol, now_ms)\n    trades, pos = replay(bars)\n"),
    ("vps/manifest", "crypto-score.timer\n", ""),
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
CONTROL 1 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 724 failed 1 empty 0
  section AB: checks 62 failed 1
  FAIL section AB: the exit due is not told twice on its day
CONTROL 2 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 724 failed 4 empty 0
  section AB: checks 62 failed 4
  FAIL section AB: a written trade is neither written, told nor asked about again
  FAIL section AB: a replay that disagrees with a written trade: its file stands byte for byte, and is counted
  FAIL section AB: a file that stands is never reopened: the same inode and the same modification time
  FAIL section AB: a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told
CONTROL 3 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 724 failed 2 empty 0
  section AB: checks 62 failed 2
  FAIL section AB: a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written and told
CONTROL 4 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 724 failed 3 empty 0
  section AB: checks 62 failed 3
  FAIL section AB: prints with a day missing inside the span: nothing written, the trade pending
  FAIL section AB: an answer that is not a list of prints: nothing written, the trade pending
  FAIL section AB: the prints read in three pages give the same R, and the late close is told once
CONTROL 5 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 724 failed 1 empty 0
  section AB: checks 62 failed 1
  FAIL section AB: a trade entered before GO_LIVE is no file of the ledger
CONTROL 6 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 724 failed 1 empty 0
  section AB: checks 62 failed 1
  FAIL section AB: a day with no entry and no exit: no alert, the record moves to that day
CONTROL 7 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 724 failed 8 empty 0
  section X: checks 19 failed 1
  section AB: checks 62 failed 7
  FAIL section X: --live names the entry due at the forming day's open, and its stop
  FAIL section AB: live_state's state is the line --live prints
  FAIL section AB: baseline: the line reads symbols=2 read=1 unread=1 open=1 opened=1 ledger=0 alert=yes
  FAIL section AB: baseline: the entry due today prints its fill and its stop, 105 - 2 x 2.2, as code spans
  FAIL section AB: baseline: no closed trade yet, one open, the held line and the foot
  FAIL section AB: record's open position: the entry due, its stop, no open R
  FAIL section AB: one alert carries the long opened today and both closes, a line each
  FAIL section AB: no number of the alert carries a float's tail or an exponent, and no symbol its USDT
CONTROL 8 vps/manifest exit=1 restored=yes
  selftest: sections 28 checks 724 failed 1 empty 0
  section AB: checks 62 failed 1
  FAIL section AB: the manifest lists crypto-score.timer once and not its service
FINAL exit=0 selftest: sections 28 checks 724 failed 0 empty 0
```

---

## 10. The patch

Against `main` at `10f926a`. B1 extracts the lines between the fences, and B2 applies them.

```diff
diff --git a/vps/book.py b/vps/book.py
index e43e6a9..cfd9880 100644
--- a/vps/book.py
+++ b/vps/book.py
@@ -139,6 +139,15 @@ def live_bars(symbol, now_ms):
     return bars, forming[0]
 
 
+def live_state(symbol, now_ms):
+    """One symbol's state today and the replay behind it: (state, trades, position). The state is the object
+    --live prints, and a history of ENTRY_N days or fewer carries none but short-history (TZ-79)."""
+    bars, open_now = live_bars(symbol, now_ms)
+    trades, pos = replay(bars, open_now)
+    out = dict(symbol=symbol, **levels(bars, pos)) if len(bars) > ENTRY_N else dict(symbol=symbol, state="short-history")
+    return out, trades, pos
+
+
 def _csv_rows(blob):
     with zipfile.ZipFile(io.BytesIO(blob)) as z:
         for name in z.namelist():
@@ -273,9 +282,7 @@ def main(argv=None):
         now_ms = int(time.time() * 1000)
         for s in a.symbols:
             try:
-                bars, open_now = live_bars(s, now_ms)
-                trades, pos = replay(bars, open_now)
-                out = dict(symbol=s, **levels(bars, pos)) if len(bars) > ENTRY_N else dict(symbol=s, state="short-history")
+                out = live_state(s, now_ms)[0]
             except Exception as exc:          # one symbol's failure never hides the others
                 out = dict(symbol=s, state="unread", error=exc.__class__.__name__)
             print(json.dumps(out, sort_keys=True), flush=True)
diff --git a/vps/manifest b/vps/manifest
index 0660048..de95e23 100644
--- a/vps/manifest
+++ b/vps/manifest
@@ -7,3 +7,4 @@ crypto-announce.service
 crypto-stop.path
 crypto-paper.service
 crypto-etf.timer
+crypto-score.timer
diff --git a/vps/score.py b/vps/score.py
new file mode 100644
index 0000000..65a5012
--- /dev/null
+++ b/vps/score.py
@@ -0,0 +1,317 @@
+#!/usr/bin/env python3
+"""The book's signal and its forward ledger (TZ-79): once a day, after the daily close, every entry and
+exit the trend book made on the list reaches the owner as one alert, and every trade the book has closed
+since it went into code is written once to a ledger that no later run rewrites. It runs no model and
+reads no credential.
+
+    score.py [--state DIR] [--outbox DIR]     default /var/lib/crypto-auto and the bot's outbox
+
+The book is book.live_state() and nothing else -- the function `book.py --live` prints from, on the same
+reads -- and a trade's result is book.result_r() on the funding prints the exchange publishes for its
+span. A trade whose prints did not arrive whole is not written: the next run asks again (map inv. 70).
+
+    score-ledger/         one closed trade a file, <SYMBOL>-<entry stamp>.json, written once and within
+                          RETRY_DAYS of its close, and never reopened (map inv. 38): a later replay that
+                          reads its trade differently is counted, and a close found later than that is
+                          counted and never written -- the replay's window slides, and the ledger takes
+                          no file about a past it did not see
+    score.json            this run's reading: the day it stands on, the open positions, the totals
+
+Prints one line, and one before it for each trade it could not price; never a price. Exit 0 the reading is written · 4 no symbol was read, or the read is
+older than the record: nothing written · 5 a file of the ledger is not a trade: nothing written.
+"""
+import argparse
+import json
+import math
+import os
+import sys
+import time
+from datetime import date, datetime, timedelta, timezone
+
+sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
+import book  # noqa: E402
+import common  # noqa: E402
+import writer  # noqa: E402
+
+# Methodology 2026-10-21-a: the first day every level the answer prints is this book's.
+GO_LIVE = "2026-10-21"
+# Map section 10, row "The book's out-of-sample loss sits in the alts": the five symbols its lead names,
+# totalled apart from the first forward day, so that the lead is read on trades it has not seen.
+MAJORS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT")
+FUNDING_URL = "https://fapi.binance.com/fapi/v1/fundingRate?symbol=%s&startTime=%d&endTime=%d&limit=1000"
+FUNDING_PAGE = 1000                              # the endpoint's own ceiling of rows an answer
+FUNDING_PAGES_MAX = 20
+# No USD-M perpetual settles less often than every eight hours: a wider gap is a span read in part.
+FUNDING_GAP_MS = 8 * 3600 * 1000 + 60 * 1000
+# A close is written while it is this recent, so that prints refused today are asked for again and a
+# unit that was down catches up; the first files of an empty ledger reach back to GO_LIVE.
+# Derived: the Architect's probe of 12.11.2026 -- twelve random markets, 455 daily runs on a 400-row
+# window, three seeds: unbounded, the ledger took 266, 253 and 296 trades the full history never made; at
+# 200 days 21, 0 and 0; at 120, 60 and 30 none, every trade equal to the full history's.
+RETRY_DAYS = 60
+LEDGER = "score-ledger"
+RECORD = "score.json"
+LEDGER_KEYS = ("symbol", "side", "t_entry", "entry", "stop", "t_exit", "exit", "why", "r", "seen")
+
+# The alert, in the owner's words; a number he may type prints as a code span (the bot of TZ-71).
+T_HEAD = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410** "
+          "\u00b7 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
+T_HEAD_BASE = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410 \u2014 "
+               "\u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043e** \u00b7 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
+T_OPEN = ("{dot} **\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u043a\u0440\u044b\u043b\u043e {side}:** "
+          "{sym} \u00b7 \u0432\u0445\u043e\u0434 `{entry}` \u00b7 \u0441\u0442\u043e\u043f `{stop}` ({dist}%)")
+T_LATE = " \u00b7 \u0432\u0445\u043e\u0434 \u0431\u044b\u043b {date}"
+T_CLOSING = ("\U0001f6aa **\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u0432\u044b\u0445\u043e\u0434\u0438\u0442 \u0441\u0435\u0433\u043e\u0434\u043d\u044f:** "
+             "{sym} {side} \u2014 \u043f\u043e \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f")
+T_CLOSED = ("\u2705 **\u0421\u0434\u0435\u043b\u043a\u0430 "
+            "\u0437\u0430\u043a\u0440\u044b\u0442\u0430:** {sym} {side} \u2014 {why} \u00b7 **{r} R**")
+T_SCORE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u043e "
+           "**{n}** \u00b7 **{total} R** \u00b7 \u0432 \u043f\u043b\u044e\u0441\u0435 {wins}")
+T_SCORE_NONE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u044b\u0445 "
+                "\u0441\u0434\u0435\u043b\u043e\u043a \u043f\u043e\u043a\u0430 \u043d\u0435\u0442")
+T_GROUPS = ("BTC ETH SOL BNB XRP: {n1} \u00b7 {r1} R \u00b7 "
+            "\u043e\u0441\u0442\u0430\u043b\u044c\u043d\u044b\u0435: {n2} \u00b7 {r2} R")
+T_OPEN_NOW = ("\u0412 \u0441\u0434\u0435\u043b\u043a\u0435 {n}: \u043b\u043e\u043d\u0433 {nl} \u00b7 \u0448\u043e\u0440\u0442 "
+              "{ns} \u00b7 \u043f\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f {r} R")
+T_HELD = "\u041c\u043e\u043d\u0435\u0442\u044b: {rows}"
+T_LEGEND = ("R \u2014 \u043e\u0434\u0438\u043d \u0440\u0438\u0441\u043a "
+            "\u043d\u0430 \u0441\u0434\u0435\u043b\u043a\u0443.")
+T_FOOT = ("\u0420\u0430\u0437\u043c\u0435\u0440 \u0438 \u043f\u043b\u0435\u0447\u043e \u2014 "
+          "\u043a\u043d\u043e\u043f\u043a\u043e\u0439 \u0430\u043d\u0430\u043b\u0438\u0437\u0430.")
+SIDE = {1: "\u043b\u043e\u043d\u0433", -1: "\u0448\u043e\u0440\u0442"}
+DOT = {1: "\U0001f7e2", -1: "\U0001f534"}
+WHY = {"stop": "\u043f\u043e \u0441\u0442\u043e\u043f\u0443", "channel": "\u043f\u043e \u043f\u0440\u0430\u0432\u0438\u043b\u0443 \u0432\u044b\u0445\u043e\u0434\u0430"}
+MINUS = "\u2212"
+SEP = " \u00b7 "
+
+
+def list_symbols():
+    """The list as the payload carries it: BTCUSDT, then tokens[] in its own order."""
+    return writer.payload_symbols(os.path.dirname(common.index_html_path()))
+
+
+def day(ms):
+    """The UTC date of a millisecond stamp, YYYY-MM-DD."""
+    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")
+
+
+def funding_prints(symbol, t_entry, t_exit):
+    """The symbol's funding prints of a trade's span as sorted (t_ms, rate) pairs, read page by page and
+    refused unless whole: a list of rows with a finite rate each, the first print inside the span within
+    FUNDING_GAP_MS of the entry, the last within it of the exit, no wider gap between two. A trade that
+    closed on its entry day has no span and asks for nothing."""
+    if t_exit <= t_entry:
+        return []
+    out, start = {}, t_entry
+    for _ in range(FUNDING_PAGES_MAX):
+        rows = json.loads(book._get(FUNDING_URL % (symbol, start, t_exit)))
+        if not isinstance(rows, list):
+            raise ValueError("fundingRate answered no list")
+        for row in rows:
+            t, rate = int(row["fundingTime"]), float(row["fundingRate"])
+            if not math.isfinite(rate):
+                raise ValueError("a funding rate is not finite")
+            out[t] = rate
+        if len(rows) < FUNDING_PAGE:
+            break
+        start = max(out) + 1
+    else:
+        raise ValueError("fundingRate did not end in %d pages" % FUNDING_PAGES_MAX)
+    inside = sorted(t for t in out if t_entry < t <= t_exit)
+    edges = [t_entry] + inside + [t_exit]
+    if not inside or any(b - a > FUNDING_GAP_MS for a, b in zip(edges, edges[1:])):
+        raise ValueError("the funding prints do not cover the trade's span")
+    return sorted(out.items())
+
+
+def row_name(row):
+    """The file a closed trade is written to: its symbol and the stamp of its entry day."""
+    return "%s-%d.json" % (row["symbol"], row["t_entry"])
+
+
+def read_ledger(path):
+    """Every trade of the ledger directory, in the order of the file names. A missing directory is an empty
+    ledger; a file that is not the trade its name says raises."""
+    try:
+        names = sorted(name for name in os.listdir(path) if name.endswith(".json") and not name.startswith("."))
+    except FileNotFoundError:
+        return []
+    rows = []
+    for name in names:
+        with open(os.path.join(path, name), encoding="utf-8") as fh:
+            row = json.load(fh)
+        if not isinstance(row, dict) or any(key not in row for key in LEDGER_KEYS) or row_name(row) != name:
+            raise ValueError("a ledger file is not a trade")
+        rows.append(row)
+    return rows
+
+
+def totals(rows):
+    """book.summary over the rows in the order their trades closed; a profit factor with no loss is null."""
+    out = book.summary([row["r"] for row in sorted(rows, key=lambda row: (row["t_exit"], row["symbol"]))])
+    if "pf" in out and not math.isfinite(out["pf"]):
+        out["pf"] = None
+    return out
+
+
+def px(value):
+    """A price to six significant figures, trailing zeros dropped, never in exponent form."""
+    if not value:
+        return "0"
+    text = "%.*f" % (max(0, 5 - int(math.floor(math.log10(abs(value))))), value)
+    return text.rstrip("0").rstrip(".") if "." in text else text
+
+
+def signed(value, digits):
+    """A number with its sign, the minus as the answer prints it."""
+    return ("%+.*f" % (digits, value)).replace("-", MINUS)
+
+
+def ddmm(iso):
+    return iso[8:10] + "." + iso[5:7]
+
+
+def name(symbol):
+    return symbol[:-4] if symbol.endswith("USDT") else symbol
+
+
+def side_of(state):
+    return 1 if state["state"] == "long" else -1
+
+
+def compose(asof, baseline, opened, closing, closed, rows, open_rows):
+    """The alert's text: one event to a line, then the rule's record since GO_LIVE."""
+    lines = [(T_HEAD_BASE if baseline else T_HEAD).format(d=ddmm(asof))]
+    for o in opened:
+        side = side_of(o)
+        line = T_OPEN.format(dot=DOT[side], side=SIDE[side], sym=name(o["symbol"]), entry=px(o["entry"]),
+                             stop=px(o["stop"]), dist=signed((o["stop"] / o["entry"] - 1) * 100, 1))
+        lines.append(line if o["entry_due"] else line + T_LATE.format(date=ddmm(o["entry_date"])))
+    for o in closing:
+        lines.append(T_CLOSING.format(sym=name(o["symbol"]), side=SIDE[side_of(o)]))
+    for row in closed:
+        lines.append(T_CLOSED.format(sym=name(row["symbol"]), side=SIDE[row["side"]],
+                                     why=WHY.get(row["why"], row["why"]), r=signed(row["r"], 2)))
+    since = GO_LIVE[8:10] + "." + GO_LIVE[5:7] + "." + GO_LIVE[:4]
+    every = totals(rows)
+    if every["n"]:
+        majors = totals([row for row in rows if row["symbol"] in MAJORS])
+        others = totals([row for row in rows if row["symbol"] not in MAJORS])
+        lines.append(T_SCORE.format(since=since, n=every["n"], total=signed(every["total"], 2),
+                                    wins=sum(1 for row in rows if row["r"] > 0)))
+        lines.append(T_GROUPS.format(n1=majors["n"], r1=signed(majors.get("total", 0.0), 2),
+                                     n2=others["n"], r2=signed(others.get("total", 0.0), 2)))
+    else:
+        lines.append(T_SCORE_NONE.format(since=since))
+    lines.append(T_OPEN_NOW.format(n=len(open_rows), nl=sum(1 for o in open_rows if side_of(o) > 0),
+                                   ns=sum(1 for o in open_rows if side_of(o) < 0),
+                                   r=signed(sum(o["r_open"] for o in open_rows if o["r_open"] is not None), 2)))
+    if baseline and open_rows:
+        lines.append(T_HELD.format(rows=SEP.join(DOT[side_of(o)] + " " + name(o["symbol"]) for o in open_rows)))
+    if baseline:
+        lines.append(T_LEGEND)
+    if opened:
+        lines.append(T_FOOT)
+    return "\n".join(lines)
+
+
+def main(argv=None, now_ms=None):
+    parser = argparse.ArgumentParser(description="the trend book's daily signal and forward ledger")
+    parser.add_argument("--state", default=common.STATE_DIR)
+    parser.add_argument("--outbox", default=None, help="where the alert is written; the bot's outbox by default")
+    args = parser.parse_args(argv)
+    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
+    ledger_path, record_path = os.path.join(args.state, LEDGER), os.path.join(args.state, RECORD)
+    try:
+        ledger = read_ledger(ledger_path)
+    except (OSError, ValueError, TypeError):
+        common.log("score: a file of the ledger is not a trade, nothing written")
+        return 5
+    try:
+        with open(record_path, encoding="utf-8") as fh:
+            prev = json.load(fh)
+        prev_asof, prev_ts = str(prev["asof"]), str(prev["ts"])
+    except (OSError, ValueError, KeyError, TypeError):
+        prev_asof = prev_ts = None
+    baseline = prev_asof is None
+
+    symbols = list_symbols()
+    read, unread = [], []
+    for symbol in symbols:
+        try:
+            read.append(book.live_state(symbol, now_ms))
+        except Exception:                 # one symbol's failure never hides the others
+            unread.append(symbol)
+    asof = max((state["asof"] for state, _, _ in read if "asof" in state), default=None)
+    if asof is None or (not baseline and asof < prev_asof):
+        common.log("score: asof=%s symbols=%d read=%d nothing written" % (asof or "-", len(symbols), len(read)))
+        return 4
+    # A symbol whose last closed day is not the day the others stand on is not read today.
+    unread += [state["symbol"] for state, _, _ in read if state.get("asof", asof) != asof]
+    live = [item for item in read if item[0].get("asof", asof) == asof]
+    fresh = baseline or asof > prev_asof
+    seen = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000))
+
+    known = {(row["symbol"], row["t_entry"]): row for row in ledger}
+    floor = GO_LIVE if not ledger else (date.fromisoformat(asof) - timedelta(days=RETRY_DAYS)).isoformat()
+    added, pending, late, disagree = [], 0, 0, 0
+    for state, trades, _ in live:
+        for tr in trades:
+            if day(tr["t_entry"]) < GO_LIVE:
+                continue
+            key = (state["symbol"], tr["t_entry"])
+            if key in known:
+                row = known[key]
+                disagree += (row["t_exit"], row["exit"], row["why"]) != (tr["t_exit"], tr["exit"], tr["why"])
+                continue
+            if day(tr["t_exit"]) < floor:
+                late += 1
+                continue
+            try:
+                r = book.result_r(tr, funding_prints(state["symbol"], tr["t_entry"], tr["t_exit"]))
+                if not math.isfinite(r):
+                    raise ValueError("the result is not finite")
+            except Exception as exc:      # not written: the next run asks for the prints again (inv. 70)
+                pending += 1
+                common.log("score: pending %s %s" % (state["symbol"], exc.__class__.__name__))
+                continue
+            known[key] = {"symbol": state["symbol"], "side": tr["side"], "t_entry": tr["t_entry"],
+                          "entry": tr["entry"], "stop": tr["stop"], "t_exit": tr["t_exit"], "exit": tr["exit"],
+                          "why": tr["why"], "r": r, "seen": seen}
+            added.append(known[key])
+    if added:
+        os.makedirs(ledger_path, mode=0o750, exist_ok=True)
+        for row in added:                 # a new file each: nothing that stands is opened (inv. 38)
+            common.atomic_write(os.path.join(ledger_path, row_name(row)), row, mode=0o640)
+    rows = ledger + added
+
+    open_rows = [state for state, _, _ in live if state["state"] in ("long", "short")]
+    if baseline:
+        opened = [o for o in open_rows if o["entry_due"]]
+    else:
+        after = (date.fromisoformat(prev_asof) + timedelta(days=1)).isoformat()
+        opened = [o for o in open_rows if fresh and o["entry_date"] > after]
+    closing = [o for o in open_rows if fresh and o["exit_due"]]
+    # A closed trade is told once: the rows written since the record this run replaces.
+    closed = [] if baseline else [row for row in rows if row["seen"] > prev_ts]
+    alert = baseline or bool(opened or closing or closed)
+    if alert:
+        common.write_outbox("alert", compose(asof, baseline, opened, closing, closed, rows, open_rows),
+                            outbox_dir=args.outbox)
+    common.atomic_write(record_path, {
+        "v": 1, "k": "score", "ts": seen, "asof": asof, "since": GO_LIVE, "symbols": len(symbols),
+        "unread": sorted(unread),
+        "open": [{key: o[key] for key in ("symbol", "state", "entry_date", "entry", "stop", "exit_level",
+                                          "r_open", "entry_due", "exit_due")} for o in open_rows],
+        "closed": {"all": totals(rows), "majors": totals([row for row in rows if row["symbol"] in MAJORS]),
+                   "others": totals([row for row in rows if row["symbol"] not in MAJORS])},
+        "pending": pending, "late": late, "disagree": disagree}, mode=0o640)
+    common.log("score: asof=%s symbols=%d read=%d unread=%d open=%d opened=%d closing=%d closed=%d pending=%d "
+               "late=%d disagree=%d ledger=%d alert=%s" % (asof, len(symbols), len(symbols) - len(unread), len(unread),
+                                                           len(open_rows), len(opened), len(closing), len(closed),
+                                                           pending, late, disagree, len(rows), "yes" if alert else "no"))
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/vps/selftest.py b/vps/selftest.py
index eb4eb13..bb5998a 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1,6 +1,6 @@
 #!/usr/bin/env python3
 """The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
-TZ-62 B2, TZ-64 B4, TZ-65 B1, TZ-69 B1, TZ-71 B2, TZ-72 B1): the sections of TZ-54 §12.14 with TZ-55 §12.7's,
+TZ-62 B2, TZ-64 B4, TZ-65 B1, TZ-69 B1, TZ-71 B2, TZ-72 B1, TZ-79 B1): the sections of TZ-54 §12.14 with TZ-55 §12.7's,
 TZ-56 §12.6's, TZ-57 §12.8's, TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's, TZ-64's, TZ-65's, TZ-69's, TZ-71's and
 TZ-72's changed and new ones, each printing
 `section <X>: checks <n> failed <m>`, then the total.
@@ -45,6 +45,7 @@ import etf  # noqa: E402
 import exchange  # noqa: E402
 import paper  # noqa: E402
 import run  # noqa: E402
+import score  # noqa: E402
 import stop  # noqa: E402
 import writer  # noqa: E402
 
@@ -3144,12 +3145,391 @@ def section_w_orders(s):
         shutil.rmtree(tmp, ignore_errors=True)
 
 
+# --- AB: the book's signal and its forward ledger (TZ-79) ------------------------------------------
+AB_LINE = re.compile(r"score: asof=\d{4}-\d\d-\d\d symbols=\d+ read=\d+ unread=\d+ open=\d+ opened=\d+ closing=\d+ "
+                     r"closed=\d+ pending=\d+ late=\d+ disagree=\d+ ledger=\d+ alert=(yes|no)")
+AB_H8 = 8 * 3600 * 1000
+
+
+def ab_klines(bars, fill):
+    """What fapi's daily klines answer for these closed bars and a forming day that opened at fill."""
+    closed = [[b[0], str(b[1]), str(b[2]), str(b[3]), str(b[4]), "0", b[0] + book.DAY_MS - 1] for b in bars]
+    forming = [bars[-1][0] + book.DAY_MS, str(fill), str(fill + 1), str(fill - 1), str(fill + 0.25), "0", 10 ** 15]
+    return json.dumps(closed + [forming]).encode()
+
+
+def ab_funding(url, rate="0.0001", hole=None):
+    """A print every eight hours from the URL's startTime through its endTime, a page of them at most."""
+    q = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
+    start, end = int(q["startTime"][0]), int(q["endTime"][0])
+    rows = [{"symbol": q["symbol"][0], "fundingTime": t, "fundingRate": rate}
+            for t in range(-(-start // AB_H8) * AB_H8, end + 1, AB_H8) if hole is None or not hole[0] <= t <= hole[1]]
+    return json.dumps(rows[:score.FUNDING_PAGE]).encode()
+
+
+class AbHost:
+    """The exchange and the state directory of one test: worlds maps a symbol to its bars, or to an
+    exception its read raises; run(n) reads the day whose forming bar is bar n of every world, each run a
+    second after the one before it."""
+
+    def __init__(self, tmp, worlds, funding=ab_funding):
+        self.tmp, self.worlds, self.funding = tmp, worlds, funding
+        self.state, self.outbox = os.path.join(tmp, "state"), os.path.join(tmp, "outbox")
+        os.makedirs(self.state)
+        os.makedirs(self.outbox)
+        self.sent, self.urls, self.runs = set(), [], 0
+
+    def get(self, url):
+        self.urls.append(url)
+        if "fundingRate" in url:
+            return self.funding(url)
+        symbol = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)["symbol"][0]
+        world = self.worlds[symbol]
+        if isinstance(world, Exception):
+            raise world
+        bars = world[:self.n + self.shift.get(symbol, 0)]
+        return ab_klines(bars, world[len(bars)][1] if len(bars) < len(world) else bars[-1][4])
+
+    def run(self, n, shift=None):
+        """(exit code, printed line, the alerts written by this run, the ledger's text, the record or None)."""
+        self.n, self.shift, self.runs = n, shift or {}, self.runs + 1
+        saved = book._get, score.list_symbols, common.OUTBOX_DIR
+        book._get, score.list_symbols, common.OUTBOX_DIR = self.get, lambda: list(self.worlds), self.outbox
+        try:
+            with contextlib.redirect_stdout(io.StringIO()) as out:
+                code = score.main(["--state", self.state], now_ms=n * book.DAY_MS + self.runs * 1000)
+        finally:
+            book._get, score.list_symbols, common.OUTBOX_DIR = saved
+        texts = []
+        for name in sorted(set(os.listdir(self.outbox)) - self.sent):
+            self.sent.add(name)
+            with open(os.path.join(self.outbox, name), encoding="utf-8") as fh:
+                doc = json.load(fh)
+            texts.append((doc["kind"], doc["text"]))
+        return code, out.getvalue(), texts, self.ledger(), self.record()
+
+    def ledger(self):
+        """The ledger's files joined in name order, a trade a line; None while there is none."""
+        folder = os.path.join(self.state, score.LEDGER)
+        try:
+            names = sorted(os.listdir(folder))
+        except FileNotFoundError:
+            return None
+        parts = []
+        for name in names:
+            with open(os.path.join(folder, name), encoding="utf-8") as fh:
+                parts.append(fh.read())
+        return "".join(parts) or None
+
+    def stamps(self):
+        """Each ledger file's name, inode, modification time and mode."""
+        folder = os.path.join(self.state, score.LEDGER)
+        return sorted((name, st.st_ino, st.st_mtime_ns, st.st_mode & 0o7777)
+                      for name, st in ((name, os.stat(os.path.join(folder, name))) for name in os.listdir(folder)))
+
+    def record(self):
+        try:
+            with open(os.path.join(self.state, score.RECORD), encoding="utf-8") as fh:
+                return json.load(fh)
+        except FileNotFoundError:
+            return None
+
+
+def ab_field(printed, name):
+    found = re.search(r"\b%s=(\S+)" % name, printed)
+    return found.group(1) if found else None
+
+
+def section_ab(s):
+    eps = 1e-9
+    long_world, short_world = x_world_long(), x_world_short()
+    s.check("GO_LIVE is 2026-10-21 and MAJORS are BTC, ETH, SOL, BNB, XRP",
+            score.GO_LIVE == "2026-10-21"
+            and score.MAJORS == ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"))
+    s.check("the list is BTCUSDT and then tokens[], as the payload carries it",
+            score.list_symbols() == writer.payload_symbols(REPO) and score.list_symbols()[0] == "BTCUSDT"
+            and len(score.list_symbols()) == len(checkout_tokens()) + 1)
+    s.check("a price prints to six significant figures, no exponent, no float tail",
+            [score.px(v) for v in (79400.75, 0.20335000000000003, 1699.0, 0.0050827, 1.3593000000000002, 100000.0)]
+            == ["79400.8", "0.20335", "1699", "0.0050827", "1.3593", "100000"])
+    s.check("a negative number prints the typographic minus", score.signed(-1.034, 2) == "\u22121.03"
+            and score.signed(8.94, 1) == "+8.9")
+    # book.live_state is the object --live prints.
+    saved_get = book._get
+    try:
+        book._get = lambda url: ab_klines(long_world[:61], 105.0)
+        with contextlib.redirect_stdout(io.StringIO()) as out:
+            book.main(["--live", "DUEUSDT"])
+        state, trades, pos = book.live_state("DUEUSDT", 61 * book.DAY_MS + 5)
+        s.check("live_state's state is the line --live prints",
+                json.loads(out.getvalue()) == json.loads(json.dumps(state, sort_keys=True))
+                and state.get("entry_due") is True and trades == [] and pos is not None and pos["entry"] == 105.0)
+        book._get = lambda url: ab_klines(long_world[:40], 100.0)
+        s.check("a history of ENTRY_N days or fewer is short-history",
+                book.live_state("NEWUSDT", 40 * book.DAY_MS + 5)[0] == {"symbol": "NEWUSDT", "state": "short-history"})
+    finally:
+        book._get = saved_get
+    saved_live, saved_page = score.GO_LIVE, score.FUNDING_PAGE
+    score.GO_LIVE = "1970-01-01"
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-ab.")
+    try:
+        # One long trade from its signal to its row: the baseline, a quiet day, the exit, the close.
+        h = AbHost(os.path.join(tmp, "a"), {"AAAUSDT": long_world, "BADUSDT": OSError("refused")})
+        code, printed, alerts, ledger, record = h.run(61)
+        s.check("baseline: exit 0, one line of the fixed shape",
+                code == 0 and printed.count("\n") == 1 and AB_LINE.fullmatch(printed.rstrip("\n")) is not None)
+        s.check("baseline: the line reads symbols=2 read=1 unread=1 open=1 opened=1 ledger=0 alert=yes",
+                [ab_field(printed, f) for f in ("asof", "symbols", "read", "unread", "open", "opened", "closing",
+                                                "closed", "pending", "late", "disagree", "ledger", "alert")]
+                == ["1970-03-02", "2", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0", "yes"])
+        text = alerts[0][1] if alerts else ""
+        s.check("baseline: one alert, of kind alert", len(alerts) == 1 and alerts[0][0] == "alert")
+        s.check("baseline: its head names the day the book stands on",
+                text.split("\n")[0] == score.T_HEAD_BASE.format(d="02.03"))
+        s.check("baseline: the entry due today prints its fill and its stop, 105 - 2 x 2.2, as code spans",
+                score.T_OPEN.format(dot=score.DOT[1], side=score.SIDE[1], sym="AAA", entry="105", stop="100.6",
+                                    dist="\u22124.2") in text.split("\n"))
+        s.check("baseline: no closed trade yet, one open, the held line and the foot",
+                score.T_SCORE_NONE.format(since="01.01.1970") in text and score.T_OPEN_NOW.format(n=1, nl=1, ns=0, r="+0.00") in text
+                and score.T_HELD.format(rows=score.DOT[1] + " AAA") in text and text.split("\n")[-1] == score.T_FOOT)
+        s.check("baseline: the legend of R is printed once, and on no later alert",
+                text.split("\n").count(score.T_LEGEND) == 1)
+        s.check("baseline: no ledger file is written while no trade has closed", ledger is None)
+        s.check("record keys v k ts asof since symbols unread open closed pending late disagree, in order",
+                record is not None and list(record) == ["v", "k", "ts", "asof", "since", "symbols", "unread", "open",
+                                                        "closed", "pending", "late", "disagree"])
+        s.check("record v 1, k score, asof the last closed day, the unread symbol named",
+                record is not None and (record["v"], record["k"], record["asof"], record["unread"])
+                == (1, "score", "1970-03-02", ["BADUSDT"]))
+        held = ((record or {}).get("open") or [{}])[0]
+        s.check("record's open position: the entry due, its stop, no open R",
+                record is not None and len(record["open"]) == 1 and abs(held.get("stop", 0) - 100.6) < eps
+                and {key: value for key, value in held.items() if key != "stop"}
+                == {"symbol": "AAAUSDT", "state": "long", "entry_date": "1970-03-03", "entry": 105.0,
+                    "exit_level": 99.0, "r_open": None, "entry_due": True, "exit_due": False})
+        s.check("record's closed totals are three empty summaries",
+                record is not None and record["closed"] == {"all": {"n": 0}, "majors": {"n": 0}, "others": {"n": 0}})
+        s.check("the record's mode is 0640",
+                os.stat(os.path.join(h.state, score.RECORD)).st_mode & 0o7777 == 0o640)
+        code, printed, alerts, ledger, record = h.run(62)
+        s.check("a day with no entry and no exit: no alert, the record moves to that day",
+                code == 0 and alerts == [] and ab_field(printed, "alert") == "no" and record["asof"] == "1970-03-03"
+                and ab_field(printed, "opened") == "0")
+        code, printed, alerts, ledger, record = h.run(62)
+        s.check("the same day read twice: no alert and nothing told again", code == 0 and alerts == [])
+        code, printed, alerts, ledger, record = h.run(101)
+        text = alerts[0][1] if alerts else ""
+        s.check("a close below the 20-day low: the exit due today is told once, with no row yet",
+                len(alerts) == 1 and text.split("\n")[1] == score.T_CLOSING.format(sym="AAA", side=score.SIDE[1])
+                and ledger is None and ab_field(printed, "closing") == "1")
+        code, printed, alerts, ledger, record = h.run(101)
+        s.check("the exit due is not told twice on its day", alerts == [])
+        code, printed, alerts, ledger, record = h.run(102)
+        rows = [json.loads(line) for line in (ledger or "").split("\n") if line]
+        want = (122.0 / 105.0 - 1 - 120 * 0.0001 - 2 * book.COST_SIDE) / (4.4 / 105.0)
+        s.check("the closed trade is one ledger file, AAAUSDT-<its entry stamp>.json, with the ten keys in order",
+                len(rows) == 1 and list(rows[0]) == list(score.LEDGER_KEYS)
+                and [x[0] for x in h.stamps()] == ["AAAUSDT-%d.json" % (61 * book.DAY_MS)])
+        row = rows[0] if rows else {}
+        s.check("its row: the symbol, the side, the entry and exit days and prices, the cause",
+                (row.get("symbol"), row.get("side"), row.get("t_entry"), row.get("entry"), row.get("t_exit"),
+                 row.get("exit"), row.get("why")) == ("AAAUSDT", 1, 61 * book.DAY_MS, 105.0, 101 * book.DAY_MS, 122.0,
+                                                      "channel"))
+        s.check("its R is book.result_r on the 120 prints after the entry and up to the exit",
+                abs(row.get("r", 0) - want) < eps)
+        text = alerts[0][1] if alerts else ""
+        s.check("an alert after the baseline carries no legend and no list of coins",
+                score.T_LEGEND not in text and not [x for x in text.split("\n") if x.startswith(score.T_HELD.split("{")[0])])
+        s.check("the close is told with its R, and the record of the rule follows it",
+                len(alerts) == 1 and text.split("\n")[1] == score.T_CLOSED.format(
+                    sym="AAA", side=score.SIDE[1], why=score.WHY["channel"], r=score.signed(want, 2))
+                and score.T_SCORE.format(since="01.01.1970", n=1, total=score.signed(want, 2), wins=1) in text
+                and score.T_GROUPS.format(n1=0, r1="+0.00", n2=1, r2=score.signed(want, 2)) in text)
+        s.check("the record totals it: one trade, a null profit factor where nothing lost",
+                record["closed"]["all"]["n"] == 1 and record["closed"]["all"]["pf"] is None
+                and abs(record["closed"]["all"]["total"] - want) < eps and record["closed"]["majors"] == {"n": 0}
+                and record["closed"]["others"]["n"] == 1 and record["open"] == [])
+        s.check("the trade's file has mode 0640", [x[3] for x in h.stamps()] == [0o640])
+        funding_calls, written = len([u for u in h.urls if "fundingRate" in u]), h.stamps()
+        code, printed, alerts, again, record = h.run(103)
+        s.check("a written trade is neither written, told nor asked about again",
+                again == ledger and alerts == [] and len([u for u in h.urls if "fundingRate" in u]) == funding_calls)
+        # A later replay that reads the trade differently changes no byte of its line.
+        moved = list(long_world)
+        moved[101] = (101 * book.DAY_MS, 130.0, 131.0, 129.0, 130.0)
+        h.worlds["AAAUSDT"] = moved
+        code, printed, alerts, again, record = h.run(104)
+        s.check("a replay that disagrees with a written trade: its file stands byte for byte, and is counted",
+                again == ledger and ab_field(printed, "disagree") == "1" and record["disagree"] == 1 and alerts == [])
+        s.check("a file that stands is never reopened: the same inode and the same modification time",
+                h.stamps() == written)
+
+        # The prints: a failure writes nothing and is asked again; a hole is a failure; pages add up.
+        def refused(url):
+            raise OSError("refused")
+        h = AbHost(os.path.join(tmp, "b"), {"AAAUSDT": long_world}, funding=refused)
+        h.run(61)
+        code, printed, alerts, ledger, record = h.run(102)
+        s.check("prints that did not arrive: nothing written, the trade pending, nothing told",
+                code == 0 and ledger is None and ab_field(printed, "pending") == "1" and record["pending"] == 1
+                and alerts == [])
+        s.check("a trade it could not price is named on a line of its own, with the failure's class and no price",
+                printed.split("\n")[0] == "score: pending AAAUSDT OSError" and printed.count("\n") == 2
+                and AB_LINE.fullmatch(printed.split("\n")[1]) is not None)
+        h.funding = lambda url: ab_funding(url, hole=(70 * book.DAY_MS, 71 * book.DAY_MS))
+        code, printed, alerts, ledger, record = h.run(102)
+        s.check("prints with a day missing inside the span: nothing written, the trade pending",
+                ledger is None and ab_field(printed, "pending") == "1")
+        h.funding = lambda url: b'{"code":-1121,"msg":"Invalid symbol."}'
+        code, printed, alerts, ledger, record = h.run(102)
+        s.check("an answer that is not a list of prints: nothing written, the trade pending",
+                ledger is None and ab_field(printed, "pending") == "1")
+        score.FUNDING_PAGE = 50
+        h.funding = ab_funding
+        code, printed, alerts, ledger, record = h.run(102)
+        rows = [json.loads(line) for line in (ledger or "").split("\n") if line]
+        s.check("the prints read in three pages give the same R, and the late close is told once",
+                len(rows) == 1 and abs(rows[0]["r"] - want) < eps and len(alerts) == 1
+                and len([u for u in h.urls[-4:] if "fundingRate" in u]) == 3
+                and alerts[0][1].split("\n")[1].startswith(score.T_CLOSED.split("{sym}")[0]))
+        score.FUNDING_PAGE = saved_page
+
+        # A short stopped through a gap, the long its stop day opens, and a trade stopped on its entry day.
+        same_day = list(long_world)
+        same_day[61] = (61 * book.DAY_MS, 105.0, 107.0, 100.0, 101.0)
+        h = AbHost(os.path.join(tmp, "c"), {"BTCUSDT": short_world, "DAYUSDT": same_day})
+        h.run(61)
+        code, printed, alerts, ledger, record = h.run(63)
+        rows = {r["symbol"]: r for r in (json.loads(line) for line in (ledger or "").split("\n") if line)}
+        want_short = (-(103.0 / 95.0 - 1) + 3 * 0.0001 - 2 * book.COST_SIDE) / (4.4 / 95.0)
+        want_day = (100.6 / 105.0 - 1 - 2 * book.COST_SIDE) / (4.4 / 105.0)
+        s.check("the stopped short: its row closes at the open beyond the stop, the short receiving three prints",
+                rows.get("BTCUSDT", {}).get("why") == "stop" and rows["BTCUSDT"]["exit"] == 103.0
+                and rows["BTCUSDT"]["side"] == -1 and abs(rows["BTCUSDT"]["r"] - want_short) < eps)
+        s.check("a trade stopped on its entry day has no span: its R carries no funding, and no print is asked for",
+                abs(rows.get("DAYUSDT", {}).get("r", 0) - want_day) < eps
+                and not [u for u in h.urls if "fundingRate" in u and "DAYUSDT" in u])
+        text = alerts[0][1] if alerts else ""
+        s.check("one alert carries the long opened today and both closes, a line each",
+                len(alerts) == 1
+                and score.T_OPEN.format(dot=score.DOT[1], side=score.SIDE[1], sym="BTC", entry="103", stop="97.9",
+                                        dist="\u22125.0") in text.split("\n")
+                and score.T_CLOSED.format(sym="BTC", side=score.SIDE[-1], why=score.WHY["stop"],
+                                          r=score.signed(want_short, 2)) in text.split("\n")
+                and score.T_CLOSED.format(sym="DAY", side=score.SIDE[1], why=score.WHY["stop"],
+                                          r=score.signed(want_day, 2)) in text.split("\n"))
+        s.check("the five named symbols are totalled apart from the others",
+                record["closed"]["majors"]["n"] == 1 and record["closed"]["others"]["n"] == 1
+                and record["closed"]["all"]["n"] == 2
+                and score.T_GROUPS.format(n1=1, r1=score.signed(want_short, 2), n2=1, r2=score.signed(want_day, 2))
+                in text)
+        s.check("no number of the alert carries a float's tail or an exponent, and no symbol its USDT",
+                all(re.fullmatch(r"\d+(\.\d{1,8})?", span) for span in re.findall(r"`([^`]*)`", text))
+                and "USDT" not in text and "e-" not in text and bool(re.findall(r"`([^`]*)`", text)))
+
+        # Days the unit did not run, an older read, a stale symbol, an unreadable list and a broken ledger.
+        h = AbHost(os.path.join(tmp, "d"), {"AAAUSDT": long_world, "BBBUSDT": long_world})
+        h.run(60)
+        code, printed, alerts, ledger, record = h.run(63)
+        text = alerts[0][1] if alerts else ""
+        s.check("an entry made on a day with no run is told late, with its day",
+                len(alerts) == 1 and text.count(score.T_LATE.format(date="03.03")) == 2
+                and ab_field(printed, "opened") == "2" and text.split("\n")[0] == score.T_HEAD.format(d="04.03"))
+        before = (h.ledger(), h.record())
+        code, printed, alerts, ledger, record = h.run(61)
+        s.check("a read older than the record: exit 4, nothing written, nothing told",
+                code == 4 and alerts == [] and (h.ledger(), h.record()) == before)
+        code, printed, alerts, ledger, record = h.run(64, shift={"BBBUSDT": -1})
+        s.check("a symbol whose last closed day is not the others' is unread today",
+                code == 0 and record["unread"] == ["BBBUSDT"] and ab_field(printed, "unread") == "1"
+                and [o["symbol"] for o in record["open"]] == ["AAAUSDT"])
+        h = AbHost(os.path.join(tmp, "e"), {"BADUSDT": OSError("refused"), "WORSEUSDT": ValueError("no day")})
+        code, printed, alerts, ledger, record = h.run(61)
+        s.check("no symbol read: exit 4, nothing written, nothing told",
+                code == 4 and alerts == [] and ledger is None and record is None and os.listdir(h.state) == [])
+        h = AbHost(os.path.join(tmp, "f"), {"AAAUSDT": long_world})
+        os.makedirs(os.path.join(h.state, score.LEDGER))
+        with open(os.path.join(h.state, score.LEDGER, "AAAUSDT-1.json"), "w", encoding="utf-8") as fh:
+            fh.write('{"symbol": "AAAUSDT"}\n')
+        code, printed, alerts, ledger, record = h.run(102)
+        s.check("a ledger file that is not a trade: exit 5, the file left as it stood, nothing told",
+                code == 5 and alerts == [] and ledger == '{"symbol": "AAAUSDT"}\n' and record is None)
+        # A close found later than RETRY_DAYS is counted and never written; inside them it is written.
+        h = AbHost(os.path.join(tmp, "h"), {"AAAUSDT": long_world})
+        h.run(61)
+        h.run(102)
+        h.worlds["BBBUSDT"] = long_world
+        saved_retry, score.RETRY_DAYS = score.RETRY_DAYS, 1
+        try:
+            code, printed, alerts, ledger, record = h.run(104)
+        finally:
+            score.RETRY_DAYS = saved_retry
+        s.check("a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told",
+                code == 0 and ab_field(printed, "late") == "1" and record["late"] == 1 and alerts == []
+                and (ledger or "").count("\n") == 1 and "BBBUSDT" not in (ledger or ""))
+        code, printed, alerts, ledger, record = h.run(104)
+        s.check("the same close inside RETRY_DAYS, which is 60: written and told",
+                score.RETRY_DAYS == 60 and ab_field(printed, "late") == "0" and (ledger or "").count("\n") == 2
+                and "BBBUSDT" in (ledger or "") and len(alerts) == 1)
+        # --outbox names where the alert goes; without it, the bot's outbox.
+        h = AbHost(os.path.join(tmp, "i"), {"AAAUSDT": long_world})
+        aside = os.path.join(tmp, "aside")
+        os.makedirs(aside)
+        saved_get, saved_list = book._get, score.list_symbols
+        book._get, score.list_symbols, h.n, h.shift = h.get, lambda: ["AAAUSDT"], 61, {}
+        try:
+            with contextlib.redirect_stdout(io.StringIO()):
+                code = score.main(["--state", h.state, "--outbox", aside], now_ms=61 * book.DAY_MS + 1000)
+        finally:
+            book._get, score.list_symbols = saved_get, saved_list
+        s.check("--outbox: the alert is written there and nowhere else",
+                code == 0 and len(os.listdir(aside)) == 1 and os.listdir(aside)[0].endswith("-alert-%d.json" % os.getpid())
+                and os.listdir(h.outbox) == [])
+        # GO_LIVE cuts the ledger by the entry's day.
+        score.GO_LIVE = "1970-03-04"
+        h = AbHost(os.path.join(tmp, "g"), {"AAAUSDT": long_world})
+        h.run(61)
+        code, printed, alerts, ledger, record = h.run(102)
+        s.check("a trade entered before GO_LIVE is no file of the ledger",
+                code == 0 and ledger is None and record["closed"]["all"] == {"n": 0} and record["since"] == "1970-03-04")
+    finally:
+        score.GO_LIVE, score.FUNDING_PAGE = saved_live, saved_page
+        shutil.rmtree(tmp, ignore_errors=True)
+    s.check("the default state is /var/lib/crypto-auto, the ledger score-ledger/ and the record score.json",
+            common.STATE_DIR == "/var/lib/crypto-auto" and (score.LEDGER, score.RECORD) == ("score-ledger", "score.json"))
+    # The units and the manifest.
+    service, timer = unit_lines("crypto-score.service"), unit_lines("crypto-score.timer")
+    s.check("service runs as User=cryptoauto, Group=cryptoauto",
+            service.count("User=cryptoauto") == 1 and service.count("Group=cryptoauto") == 1
+            and len([x for x in service if x.startswith(("User=", "Group="))]) == 2)
+    s.check("service reads no credential", not [x for x in service if x.startswith("LoadCredential")])
+    s.check("service is Type=oneshot and has no [Install] section",
+            [x for x in service if x.startswith("Type=")] == ["Type=oneshot"] and "[Install]" not in service)
+    s.check("service runs /usr/bin/python3 /srv/crypto-auto/vps/score.py",
+            [x for x in service if x.startswith("ExecStart")] == ["ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/score.py"])
+    s.check("service may write the spool and the state directory, and nothing else",
+            [x for x in service if x.startswith("ReadWritePaths")] == ["ReadWritePaths=/var/spool/crypto-auto /var/lib/crypto-auto"]
+            and "ProtectSystem=strict" in service)
+    s.check("timer fires at OnCalendar=*-*-* 00:10:00 UTC, Persistent=true",
+            [x for x in timer if x.startswith("OnCalendar")] == ["OnCalendar=*-*-* 00:10:00 UTC"]
+            and "Persistent=true" in timer)
+    s.check("timer's unit is crypto-score.service, WantedBy=timers.target",
+            [x for x in timer if x.startswith("Unit=")] == ["Unit=crypto-score.service"]
+            and "[Install]" in timer and "WantedBy=timers.target" in timer)
+    with open(os.path.join(HERE, "manifest"), encoding="utf-8") as fh:
+        listed = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
+    s.check("the manifest lists crypto-score.timer once and not its service",
+            listed.count("crypto-score.timer") == 1 and "crypto-score.service" not in listed)
+    s.check("no unit of vps/units starts a model from a timer: crypto-score.service names no claude",
+            not [x for x in service if "claude" in x.lower()])
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
             ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
             ("T", section_t), ("U", section_u), ("V", section_v), ("W", section_w), ("X", section_x),
-            ("Y", section_y), ("Z", section_z), ("AA", section_aa))
+            ("Y", section_y), ("Z", section_z), ("AA", section_aa), ("AB", section_ab))
 
 
 def main():
diff --git a/vps/units/crypto-score.service b/vps/units/crypto-score.service
new file mode 100644
index 0000000..fa8768e
--- /dev/null
+++ b/vps/units/crypto-score.service
@@ -0,0 +1,20 @@
+[Unit]
+Description=Crypto assistant: the trend book's daily signal and forward ledger
+Wants=network-online.target
+After=network-online.target
+
+[Service]
+Type=oneshot
+User=cryptoauto
+Group=cryptoauto
+ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/score.py
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
diff --git a/vps/units/crypto-score.timer b/vps/units/crypto-score.timer
new file mode 100644
index 0000000..28ab86c
--- /dev/null
+++ b/vps/units/crypto-score.timer
@@ -0,0 +1,10 @@
+[Unit]
+Description=Crypto assistant: the book's signal after the daily close
+
+[Timer]
+OnCalendar=*-*-* 00:10:00 UTC
+Persistent=true
+Unit=crypto-score.service
+
+[Install]
+WantedBy=timers.target
```
