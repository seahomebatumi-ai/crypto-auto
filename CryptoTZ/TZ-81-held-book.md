# TZ-81 — The book the owner can hold: the plan's entries taken under his ceilings — six a side and ten in all, the majors first at one open — in the alert, the look and a ledger of their own, so that what he is told and what the gate scores are one book

**Canonical filename:** `CryptoTZ/TZ-81-held-book.md`
**Report:** `CryptoReports/TZ-81-held-book-report.md`
**Class:** branch TZ (contract §8) — it authorises three repository files besides its report.
**Branch:** `claude/tz-81-held-book`
**Host:** the VPS, for stage C; stages A–B run on any clone.
**Model:** Sonnet — the change is the patch of §10, written by the Architect and run by it under Python 3.11, 3.12 and
3.13 before this TZ shipped; the session applies it, proves its bytes and runs the validation. Nothing in it is
diagnosis or design.
**Trigger:** `EXECUTE TZ-81`, with nothing under it: no credential arrives and the Boss is asked for nothing.
**Previous TZ:** TZ-80, accepted 15.11.2026 and merged at `eb52dca` (pull request #66); no branch on the remote is
ahead of `main`.
**Issued:** 15.11.2026, by the Architect, for map §10's row «The ledger scores a book the owner cannot hold».
**Written against:** contract v31, map `2026-11-15-a`, methodology `2026-10-26-a`, and `main` at `23a003d` — its
`vps` tree `825713831ce434ae0d8a9e05a62124694d510938` — read from the repository on 15.11.2026.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-15-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-15-a.**` |
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
| `vps/book.py` | 354 | `33c764fa584507fa8a6a121a18f571d8` | equal, or A1 stops: §10 is written against these bytes |
| `vps/score.py` | 528 | `91503ec6cecb05d094dc0b8ff47a7889` | equal, or A1 stops |
| `vps/selftest.py` | 3882 | `5963c21b6c869b49d9a151b3aeac0ce7` | equal, or A1 stops |
| `vps/paper.py` | 1967 | `f6970999e177fae27bfa78ef9d252b17` | reported: the patch does not touch it, `score.py` imports it and V5 copies it |
| `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` | reported: the patch does not touch it and V5 copies it |
| `vps/writer.py` | 154 | `c07b1f71ef014e18448eb9313e185b73` | reported: the patch does not touch it and V5 copies it |

The map itself: 2804 lines, MD5 `6dc9ce680dbbf791a51d7411d155c80d` — reported, not enforced.

---

## 1. What changes, and the evidence for it

**The defect, found by the audit of TZ-80 on 15.11.2026.** The alert TZ-80's V5 composed on the close of 14.11 — the
shape of the first message the owner receives after that merge — told nine new shorts and twenty more held, «В сделке 29: лонг 0 ·
шорт 29», under the line «Ваш лимит: 6 сделок в одну сторону и 10 всего». The plan's ledger, which the gate of map §10's
row «The engine places no order on the exchange» reads, scores all twenty-nine. He is told one book, can hold another,
and the record that decides real money is a record of neither.

**What the ceilings make, measured by the Architect on 15.11.2026** — this TZ's `vps/book.py --archive` on
`data.binance.vision`, the 31 symbols of the payload's list in its order, 2023-01-01 → 2026-10-31, fees, slippage and
the actual funding, nothing fitted; the two rows are `--scale 2` and `--scale 2 --hold 6,10`, and the last column and
the random orders are §11's study, retained there:

| The plan, 2023-01-01 → 2026-10-31 | In sample (2023–24) | Out of sample (2025 →) | Largest drawdown, IS / OOS | Most open at once |
|---|---|---|---|---:|
| every entry | 229 trades, +136.30 R | 298 trades, −9.09 R | 33.82 / 43.03 R | 26 |
| held under 6 a side and 10 in all | 115 trades, +38.66 R | 119 trades, +28.10 R | 19.43 / 26.34 R | 10 |

Under 200 random orders of the list, the same walk gives +14.14 to +27.03 R out of sample, 5th to 95th percentile,
median +20.20, none below zero; in sample +38.70 to +50.24, median +44.16. The list's order stands just under the 5th
percentile in sample and above the 95th out of it: **the order is not where the result comes from — the ceilings are.**

**The row's own figures are not these, and these replace them at the audit.** Its walk of 15.11.2026 — 117 and 124
trades, +36.61 and +18.37 R, random orders +7.63 to +19.74 R — was not retained (inv. 71), and `book.hold()` does not
reproduce it. Every entry's line reproduces the row's trades, totals and peak of 26; its out-of-sample drawdown, 44.04 R
there, is 43.03 R by `book.summary()`.

**No edge is claimed** (inv. 32). The ceilings cost the book nearly three quarters of its in-sample gain — the trends of
2023–24 paid the wide book — and turn its out-of-sample loss into a gain; neither is why they apply. They apply because the
owner holds six a side and ten in all, and a record of more than he can hold measures nothing he does.

**What is built — no model:**

1. **`vps/book.py`** — `MAJORS`, moved here from `score.py`; `rank(symbols)`, the order one open's entries are taken
   in; `spans(symbol, trades, pos, t_next)`, each position as the walk reads it; `hold(books, ranks, side_max, book_max,
   fixed=None)`, the walk; `archive(..., ceilings=None)` and `--archive --hold SIDE,BOOK`. **Without `--hold` nothing
   `--live` or `--archive` prints moves.**
2. **`vps/score.py`** — the book held, in the daily close and in the look; its ledger `score-held/`; the record `v` 3;
   exit 6 where the owner's ceilings are unread. §3.
3. **`vps/selftest.py`** — section AB re-specified for the book held, 117 checks to 145.

*[Architect's decisions, TZ-81.* **The ceilings are applied to the book the engine tells, and to nothing else.** TZ-80
stated them and applied none; its audit found the ledger then scores a book the owner cannot hold. The engine still
cannot know what he holds (owner's decision of 24.09.2026), so the line of his ceilings and «считайте вместе с
открытыми» stay, for what he holds beyond the book. **One open's entries are taken in the order the alert prints
them** — the five `MAJORS`, then the list's — which is the order the row names; **across opens, first come:** an entry
left out at its own open is never taken later, because the plan's entry is a fill at that open and a later fill is
another trade. **A position keeps its slot until its own exit, after its target as before it:** his line counts
«сделок», and the rest of a position past its target is still a position on his account.
**At one open, an exit at the open frees its slot before that open's entries, and a stop frees it after them,** because
a stop fills inside the day, after the open's fills. **What a record told stands:** each entry up to the open the last
record told keeps that record's decision, taken or left out, and a symbol unread today keeps the spans the record held
for it — re-deciding the past from today's replay would turn an entry he was told to take into one the ledger never
scores, or the reverse, on one failed read. Run every day, the close holds exactly the book `hold()` takes over the same
days at once — section AB proves it — so the archive's measurement is the live book's. Ceilings that change start the
book again from `GO_LIVE` under the new ones, and that run is a baseline. **The plan's entries the ceilings leave out
reach him on one line, «⏸ Вне лимита:», the day they are made** — a «no» names its cause — and the baseline names every
plan position the book does not hold, so the first message after the merge tells him which positions are the book's.
**Three ledgers, one gate:** `score-held/` is the book he is told and the one the gate counts; `score-plan/` keeps every
entry as `--scale 2` replays it, and `score-ledger/` the rule's as `--archive` replays it, so the forward reading of
the row's finding is the first against the second; a trade two ledgers write is priced once. **A run that cannot read
his ceilings writes nothing (exit 6):** a book without them is not his book. **The analysis answer's budget — one
object a side until the gate, methodology §4 — is step 2's;** no line of the methodology moves here.*]*

---

## 2. Text this TZ obeys

- Contract §7 item 1: «**No change to scoring, leverage, liquidation or geometry math** unless the TZ explicitly cites a
  completed backtest» — none of the functions that item closes is touched, and neither is `index.html`. The ceilings
  choose which of the plan's trades are told and scored, and this TZ cites its completed backtest: §1, by the code of §10.
- Contract §7 item 2: «**Never edit a bench to make it pass.**» — the checks of section AB that read the record, the
  line, the ledgers and the look are re-specified because this TZ changes what they assert. The Architect wrote every
  new expectation before execution and derived each in the check's own text; the session edits no check.
- Contract §7 item 9: «**A session fetch may not stand behind a product fact**» — §1's figures are the Architect's
  measurement, retained in §11; no stage of this TZ reads the archive, and V5 runs the program on its own host and its
  own exchange reads, as TZ-80's V5 did.
- Contract §7 item 15: «An implementation session never enables, starts or leaves running a persistent unit, timer or
  service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its report
  proves none is left behind.» — no unit moves; the book takes effect when the deployer installs the merge.
- Map inv. 38: «**A second implementation of any rule, threshold or formula is banned in any language and any file.**»
  — one `hold()` makes the live book and the archive's; the ceilings are `paper.ceilings()`, which the alert already
  prints; «A file once written is never reopened» — the book held's ledger writes a new file per closed trade, and the
  files TZ-79 and TZ-80 wrote stand.
- Map inv. 70: «**A transport failure is NOT an absence of data.**» — a symbol unread today keeps the spans the last
  record held for it, and never frees a slot by failing to answer.
- Map inv. 72: «**A write that fails leaves this run's product or nothing — never a partial file and never the previous
  run's.**» — every file is written by `common.atomic_write`.
- Map inv. 22: «**A check that passes with no data is forbidden.**» — V5 fails on `read=0`.

---

## 3. What the two runs do — registered

### The book held — both runs

- **The spans:** each of the plan's positions entered since `GO_LIVE` — its symbol, its side, its entry's open, and the
  moment its slot frees: a channel exit at its open, before that open's entries; a stop inside its day, after them; a
  position whose exit is due at the next open, at that open; a position that stands, never.
- **The walk:** in time, from an empty book, an entry is taken where fewer than `side` positions are held on its side
  and fewer than `book` in all — `paper.ceilings()` of the owner's file, 6 and 10 at his current file — the `MAJORS`
  first at one open and the others in the list's order.
- **What stands:** where the last record is `v` 3 under the same ceilings, each entry up to the open that record told
  is taken if that record took it and left out if not, and the spans that record held on a symbol unread today stand as
  it recorded them.
- **The owner's file unread:** nothing is read from the exchange, nothing written, nothing told, and the run exits 6 —
  `score: the owner's ceilings are unread, nothing written`, or for the look `score: forming day=<day> the owner's
  ceilings are unread, nothing written`.

### The daily close — `score.py`, 00:10 UTC, TZ-79's timer

- **Three ledgers,** each under TZ-79's rules: `<state>/score-held/` the book held's — the gate's; `<state>/score-plan/`
  the plan's every entry; `<state>/score-ledger/` the rule's. A failed read of the prints writes nothing in any of them
  and prints `score: pending <ledger> <SYMBOL> <exception class>` for each.
- **The alert tells the book held:** its entries, two lines each, the `MAJORS` first, as TZ-80 printed them; then, once,
  `⏸ **Вне лимита:** <side> <names> · <side> <names>` — the plan's entries the ceilings leave out, long before short, the
  `MAJORS` first in each; its targets reached, its exits due and its closes with the book's R; the book's record since
  `GO_LIVE`; its open positions by side. Under an entry, what the target means and when to enter; under an entry or a
  line of entries left out, the owner's ceilings. **An entry left out is an event:** it alone sends the alert.
- **The baseline** — the first run, or the first after a record that is not `v` 3, or after a record under other
  ceilings — tells no close it fills, prints in full the book's entries made since that record's day, every other
  position the book holds on one line, and every position of the plan it does not hold on the line of entries left out.
- **The record** is `v` 3, its keys in this order: `v`, `k`, `ts`, `asof`, `since`, `symbols`, `unread`, `ceilings` —
  `[side, book]` —, `held` — each span the book holds since `GO_LIVE`, `[symbol, side, entry stamp, [free stamp,
  phase] or null]`, sorted —, `open` — the book's positions read today, TZ-80's twelve keys —, `outside` — the plan's
  open positions the book does not hold, `{"symbol", "state", "entry_date"}`, the `MAJORS` first —, `closed`,
  `pending`, `late`, `disagree` and `look` — the book's —, `plan` — `{"open", "closed", "pending", "late",
  "disagree"}` of every entry — and `rule`, TZ-80's.
- **The line** is `score: asof=… symbols=… read=… unread=… open=… outside=… opened=… skipped=… scaled=… closing=…
  closed=… pending=… late=… disagree=… ledger=… plan=… rule=… look=… alert=yes|no` — `open`, `opened`, `scaled`,
  `closing`, `closed`, `pending`, `late`, `disagree` and `ledger=` the book's; `outside=` the plan's positions it does
  not hold; `skipped=` the entries left out it tells; `plan=` and `rule=` those ledgers' sizes; `look=` the look's
  count, `hit/named/entries`, over the book's entries.

### The look — `score.py --forming`, 15:10 UTC, TZ-80's timer

- **The same walk** over the plan's spans with the day still forming appended, the last record's decisions standing:
  a stop or a target the day has reached is told only of a position the book holds, and a candidate only where the
  book would take it at the next open.
- **Its record** is `v` 2, TZ-80's nine keys. A look of `v` 1, which named the plan's candidates, is counted by no
  close: that close prints `look=-`.
- **Its line, its hour and its alert's shape** are TZ-80's.

### What does not move

TZ-79's and TZ-80's timers and units, the manifest, `GO_LIVE`, `RETRY_DAYS`, the funding reads, the rule and the
plan's `replay()`, `paper.py`, and every line of the alert but the one this TZ adds. `book.py --live` and
`book.py --archive` without `--hold` print what they printed, key for key; `--hold` with `--live`, or a value that is
not two positive counts, is refused with exit 2.

---

## 4. Scope

### Files to Create
None.

### Files to Modify
- `vps/book.py`, `vps/score.py`, `vps/selftest.py` — §10.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
The scratch directory `/var/lib/crypto-auto/tz81` and the transient units of V5, all gone before the report. Nothing
under `/var/lib/crypto-auto` but that directory is written, no unit is created, changed, enabled or restarted, and the
bot's outbox receives nothing from this session: the book takes effect when the deployer installs the merge.

### Not touched
`index.html`, `main.py`, `vps/paper.py`, every unit, the manifest, `bench.yml`, `analyst/**`, the map, the contracts.

---

## 5. Stages

### Stage A — readings, no writes
- **A0.** Contract §4a steps 1–6; the gate of §0, every anchor cut from the map's own table.
- **A1.** The added files of §0 at their lines and MD5. A difference in any of the three files §10 modifies stops the
  TZ, BLOCKED, naming the file.
- **A2.** On the VPS, the baseline from `main`: `python3 vps/selftest.py` prints `selftest: sections 28 checks 779
  failed 0 empty 0` and `section AB: checks 117 failed 0`. *Measured by the Architect on `23a003d`'s tree under Python
  3.11, 3.12 and 3.13.* A different baseline is recorded per section and the TZ goes on.
- **A3.** As root:

  ```sh
  python3 -c "import json; d=json.load(open('/var/lib/crypto-auto/score.json')); print(d['v'], d['asof'])"
  test -e /var/lib/crypto-auto/score-held; echo $?
  ls /var/lib/crypto-auto/score-ledger | wc -l
  test -d /var/lib/crypto-auto/score-plan && ls /var/lib/crypto-auto/score-plan | wc -l
  ```

  kept for V7. *Expected:* `2` and a date — or `1`, where the deployer has not yet installed TZ-80's merge, which the
  report says —; `1`; a count; and a count, or nothing where `score-plan` does not exist yet.

### Stage B — the code, on the branch
- **B1.** Branch `claude/tz-81-held-book` from `origin/main`. Extract §10's patch with the one command

  ```sh
  awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-81-held-book.md > /tmp/tz81.patch
  ```

  and record its lines and MD5 — 1048 and `24af804041772e14205749784937adcd` as written; an upload that strips the patch's
  blank context lines changes the hash and not the result, which B2 decides.
- **B2.** `git apply /tmp/tz81.patch`. **Required:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/book.py` | 419 | `4e283c02783b4f959c49b613b4e518a5` |
  | `vps/score.py` | 613 | `eb76418a35e4c9389a80e61b1d449387` |
  | `vps/selftest.py` | 4101 | `25136248a1fba37be97af33b1e9a598c` |

  Any other result is BLOCKED: the patch did not arrive as written, and no hand edit replaces it.
- **B3.** Commit with §7's implementation message, **locally, before stage C**. Not pushed yet.

### Stage C — validation, on the VPS, on the committed branch
§6, in full.

### Stage D — push, pull request, report
Push; a pull request to `main` titled `TZ-81: vps — the book the owner can hold`, its body naming this TZ, or the
contract's §8 fallback. Then the report.

---

## 6. Validation

- **V1. Syntax.** `python3 -m py_compile vps/book.py vps/score.py vps/selftest.py` — exit 0.
- **V2. The bytes.** B2's three files at B2's lines and MD5s; and

  ```sh
  python3 -c "print(sum(0x400 <= ord(c) <= 0x4ff for f in ('vps/book.py', 'vps/score.py', 'vps/selftest.py') for c in open(f, encoding='utf-8').read()))"
  ```

  prints `0`.
- **V3. Selftest**, on the VPS, on the branch: `python3 vps/selftest.py` — exit 0, `selftest: sections 28 checks
  807 failed 0 empty 0`, `section AB: checks 145 failed 0`, **every other section's count equal to A2's**. *Measured by
  the Architect under Python 3.11, 3.12 and 3.13.*
- **V4. Negative controls** (inv. 22). Extract §9's script with the one command

  ```sh
  awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-81-held-book.md > /tmp/tz81-controls.py
  ```

  — 82 lines, MD5 `64bc4c5bc20d81ac211b1be97a4f5dd8` as written — and run `python3 /tmp/tz81-controls.py` from the
  clone's root. **Required:** exactly the 119 lines §9 prints after the script — MD5 `7e9a8f160d6e4c8f5ce0a1242981df47` — and then
  `git status --porcelain` prints nothing. *Measured by the Architect under Python 3.11, 3.12 and 3.13, the three
  outputs identical.*
- **V5. The exchange, read from this machine, on a copy of the live state.** As root:

  ```sh
  install -d -o cryptoauto -g cryptoauto -m 0750 /var/lib/crypto-auto/tz81 /var/lib/crypto-auto/tz81/vps \
      /var/lib/crypto-auto/tz81/state /var/lib/crypto-auto/tz81/outbox /var/lib/crypto-auto/tz81/analyst
  install -o cryptoauto -g cryptoauto -m 0640 vps/*.py /var/lib/crypto-auto/tz81/vps/
  install -o cryptoauto -g cryptoauto -m 0640 analyst/owner.json /var/lib/crypto-auto/tz81/analyst/
  install -o cryptoauto -g cryptoauto -m 0640 index.html /var/lib/crypto-auto/tz81/
  cp -a /var/lib/crypto-auto/score.json /var/lib/crypto-auto/score-ledger /var/lib/crypto-auto/tz81/state/
  if [ -d /var/lib/crypto-auto/score-plan ]; then cp -a /var/lib/crypto-auto/score-plan /var/lib/crypto-auto/tz81/state/; fi
  ls -li --time-style=full-iso /var/lib/crypto-auto/tz81/state/score-* > /tmp/tz81-before.txt
  run81() { systemd-run --wait --collect --pipe --uid=cryptoauto --gid=cryptoauto -p ProtectSystem=strict \
      -p ReadWritePaths=/var/lib/crypto-auto/tz81 -p MemoryMax=64M -p Environment=PYTHONDONTWRITEBYTECODE=1 \
      /usr/bin/python3 /var/lib/crypto-auto/tz81/vps/score.py \
      --state /var/lib/crypto-auto/tz81/state --outbox /var/lib/crypto-auto/tz81/outbox "$@"; }
  run81; run81; run81 --forming; run81 --forming
  ```

  The scratch tree carries every program of `vps/` — `score.py` imports `paper.py`, which imports `announce.py` and
  `exchange.py` — and `index.html` and `analyst/owner.json` beside it, so the program reads the list and the owner's
  file there; the unit can write nothing but the scratch directory. **Required, by shape:**
  - *the first run — the baseline, the live record being `v` 1 or 2:* exit 0; the last line printed is §3's line with
    `symbols=31`, `read` at least 1 (inv. 22), `asof` the UTC day before the run, `look=-` and `alert=yes`; exactly one
    file in the scratch outbox, of kind `alert`, whose first line carries «СДЕЛКИ ПРАВИЛА — подключено»; `state/score.json`
    parses with `v` 3, the eighteen keys of §3 in their order and `ceilings` `[6, 10]`; its `open`, less the positions
    whose `exit_due` is true, holds at most 6 positions of each `state` and 10 in all, and the counts of `open` and
    `outside` add up to `plan.open`; where `unread` is empty, every position of `open` has its span in `held`, by symbol
    and entry day, and every span of `held` whose last element is `null` is a position of `open`; the line's `opened`
    equals the number of the alert's lines carrying «· вход `», each followed by a
    line beginning «🎯 цель» that carries «объём» and «маржа»; a line beginning «⏸ **Вне лимита:**» exists exactly where
    `outside` is not 0, and the names on it are exactly the symbols of the record's `outside`, without `USDT`;
    `state/score-held` holds as many files as the line's `ledger=` — and does not exist where that is 0 —, each with a
    file of the same name in
    `state/score-plan` whose keys but `seen` equal its own; `state/score-plan` holds as many files as the line's `plan=`;
    and every file listed in `/tmp/tz81-before.txt` is in its directory after the run with the same inode and
    modification time;
  - *the second:* `opened=0 skipped=0 scaled=0 closing=0 closed=0 alert=no`, no second file in the scratch outbox, and
    `state/score.json`'s `held` equal to the first run's;
  - *the third, the look:* exit 0; one line, §3's, with `symbols=31` and `read` at least 1;
    `state/score-forming/<today, UTC>.json` parses to the nine keys of TZ-80 §3 in their order with `v` 2; each symbol
    its `stopped` and `scaled` name has a span in `state/score.json`'s `held`; the scratch outbox holds one more file
    exactly where the line reads `alert=yes`, its first line carrying «СНИМОК ДНЯ»; and `state/score.json`,
    `state/score-held`, `state/score-plan` and `state/score-ledger` are byte for byte what the second run left;
  - *the fourth:* exit 0, the one line `score: forming day=<today> already looked at, nothing written`, and no new file
    anywhere under the scratch directory.

  The report quotes every line the four runs printed and the text of every alert in full — the first message the owner
  receives after the merge is the first run's, on its own day. Then, once, from the scratch tree as `cryptoauto`:
  `python3 /var/lib/crypto-auto/tz81/vps/book.py --live --hold 6,10 BTCUSDT` — exit 2 and a usage error naming
  `--hold`, no read made — and `python3 /var/lib/crypto-auto/tz81/vps/book.py --live --scale 2 BTCUSDT ETHUSDT` — two
  lines, each carrying `target` where its state is `long` or `short`; the report quotes the three. Then
  `rm -r /var/lib/crypto-auto/tz81`, and `systemctl list-units --all --no-legend 'run-*'` shows no unit of this session.
- **V6. Scope.** `git diff --numstat origin/main...HEAD` prints exactly three lines, tab-separated:

  ```text
  69	4	vps/book.py
  153	68	vps/score.py
  271	52	vps/selftest.py
  ```
- **V7. Nothing in effect before the merge.** A3's four commands again: the same `v`, `1` — no `score-held` —, and the
  ledgers as they stood, unless the timer ran during the session, which the report says.
- **V8. `bench.yml`.** `index.html` and `main.py` are untouched, so the standing checks do not apply; the report names
  the workflows that ran on the branch, from the runner where the session can.

**No regression:** every section but AB keeps A2's count, green (V3) — X's 19 among them, with the rule's replay
unchanged — and no file outside §4 moves (V6).

---

## 7. Commit Message

Implementation: `TZ-81: vps — the book the owner can hold: the plan's entries taken under his ceilings, six a side and ten in all, the majors first at one open, in the alert, the look and a ledger of their own`

Report: `TZ-81: report — the book the owner can hold`

---

## 8. The report

Contract §10 in full. Beside it: B1's command and the patch's lines and MD5; B2's lines and MD5s; A2's and V3's
per-section counts side by side; V4's output verbatim; V5's commands, every line they printed and every alert's text;
A3's and V7's readings. The map's rows are the Architect's to update after the audit, not this TZ's.

---

## 9. The controls script (V4)

```python
#!/usr/bin/env python3
"""TZ-81, V4: eighteen negative controls. Each is one exact string replaced in one file of the working tree,
the selftest run, the file restored and its digest compared. Run from the repository root, on the branch."""
import hashlib
import subprocess
import sys

CONTROLS = (
    ("vps/book.py", "        elif (fixed or {}).get(key, list(now.values()).count(side) < side_max and len(now) < book_max):\n",
     "        elif (fixed or {}).get(key, len(now) < book_max):\n"),
    ("vps/book.py", "        elif (fixed or {}).get(key, list(now.values()).count(side) < side_max and len(now) < book_max):\n",
     "        elif (fixed or {}).get(key, list(now.values()).count(side) < side_max):\n"),
    ("vps/book.py", "        elif (fixed or {}).get(key, list(now.values()).count(side) < side_max and len(now) < book_max):\n",
     "        elif {}.get(key, list(now.values()).count(side) < side_max and len(now) < book_max):\n"),
    ("vps/book.py", "    return {s: k for k, s in enumerate(sorted(symbols, key=lambda s: s not in MAJORS))}\n",
     "    return {s: k for k, s in enumerate(symbols)}\n"),
    ("vps/book.py", "(tr[\"t_exit\"], AT_OPEN if tr[\"why\"] == \"channel\" else IN_DAY))\n",
     "(tr[\"t_exit\"], AT_OPEN))\n"),
    ("vps/book.py", "(tr[\"t_exit\"], AT_OPEN if tr[\"why\"] == \"channel\" else IN_DAY))\n",
     "(tr[\"t_exit\"], IN_DAY))\n"),
    ("vps/book.py", "                    (t_next, AT_OPEN) if pos.get(\"exit_due\") and t_next is not None else None))\n",
     "                    None))\n"),
    ("vps/book.py", "        rows = [r for r in rows if (r[1], r[3]) in taken]\n", "        rows = list(rows)\n"),
    ("vps/score.py", "    return isinstance(prev, dict) and prev.get(\"v\") == 3 and prev.get(\"ceilings\") == ceilings\n",
     "    return isinstance(prev, dict) and prev.get(\"v\") == 3\n"),
    ("vps/score.py", "                   if s in unread]\n", "                   if False]\n"),
    ("vps/score.py", "        fixed = {(s, t): (s, t) in took for s, _, t, _ in books + carried if t <= told}\n",
     "        fixed = None\n"),
    ("vps/score.py", "                      if sp[2] >= go], symbols, unread, ceilings, prev)\n",
     "                      ], symbols, unread, ceilings, prev)\n"),
    ("vps/score.py", "        held_path, held_ledger, [(plan[0], [tr for tr in plan[1] if (plan[0][\"symbol\"], tr[\"t_entry\"]) in taken])\n",
     "        held_path, held_ledger, [(plan[0], plan[1])\n"),
    ("vps/score.py", "    open_rows = [plan[0] for plan in plan_open if (plan[0][\"symbol\"], plan[2][\"t_entry\"]) in taken]\n",
     "    open_rows = [plan[0] for plan in plan_open]\n"),
    ("vps/score.py", "    alert = baseline or bool(opened or skipped or scaled or closing or closed)\n",
     "    alert = baseline or bool(opened or scaled or closing or closed)\n"),
    ("vps/score.py", "        if then[\"state\"] not in (\"long\", \"short\") or (symbol, pos[\"t_entry\"]) not in taken:\n",
     "        if then[\"state\"] not in (\"long\", \"short\"):\n"),
    ("vps/score.py", "                    if tr[\"t_exit\"] == today[0] and tr[\"why\"] == \"stop\" and (symbol, tr[\"t_entry\"]) in taken]\n",
     "                    if tr[\"t_exit\"] == today[0] and tr[\"why\"] == \"stop\"]\n"),
    ("vps/score.py", "                r = (priced or {}).get(key)\n", "                r = None\n"),
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
  selftest: sections 28 checks 807 failed 16 empty 0
  section AB: checks 145 failed 16
  FAIL section AB: one a side and two in all: the baseline tells the major's long and the short in full, and names the two longs left out on one line under them
  FAIL section AB: its line: open=2 outside=2 opened=2 skipped=2; its record: the ceilings 1 and 2, the two held, the two left out with their side and day, the plan's four open
  FAIL section AB: the short stopped inside its day is the book's trade, in its ledger as in the plan's; the long its stop day opened finds the long side full: named left out with the ceilings, and no entry told
  FAIL section AB: a target reached is told of the position held alone, not of the plan's two left out
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: the book held's ledger takes the trades it held, the plan's every entry: two files against four
  FAIL section AB: the close is told of the position held and of none left out, and the score is the book held's
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
  FAIL section AB: the look names the candidate the book would take, the major's long, and not the long it would leave out
  FAIL section AB: a stop the day has reached on a position the book left out is not the look's to tell
  FAIL section AB: hold: one open's entries are taken in rank order while their side has room -- the major's, then the list's
  FAIL section AB: hold: a stop frees its slot inside its day, after that open's entries -- the next open's entry is taken
  FAIL section AB: hold: an entry stopped on its own day held its slot through that open
  FAIL section AB: hold: an entry not taken at its own open is never taken, though a slot frees while it stands
CONTROL 2 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: hold: the book's ceiling binds across the sides -- two longs leave no room for a short at two in all
CONTROL 3 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written -- and, its entry never told, not the book's: nothing told, no file of the book held
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
CONTROL 4 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 15 empty 0
  section AB: checks 145 failed 15
  FAIL section AB: one a side and two in all: the baseline tells the major's long and the short in full, and names the two longs left out on one line under them
  FAIL section AB: its line: open=2 outside=2 opened=2 skipped=2; its record: the ceilings 1 and 2, the two held, the two left out with their side and day, the plan's four open
  FAIL section AB: a target reached is told of the position held alone, not of the plan's two left out
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: the book held's ledger takes the trades it held, the plan's every entry: two files against four
  FAIL section AB: the close is told of the position held and of none left out, and the score is the book held's
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
  FAIL section AB: the look names the candidate the book would take, the major's long, and not the long it would leave out
  FAIL section AB: a stop the day has reached on a position the book left out is not the look's to tell
  FAIL section AB: rank: the MAJORS first, then the others, each in the order given -- the list's
  FAIL section AB: hold: one open's entries are taken in rank order while their side has room -- the major's, then the list's
  FAIL section AB: hold: an entry stopped on its own day held its slot through that open
  FAIL section AB: the archive with ceilings keeps hold()'s trades: of two longs at one open, the major's alone
CONTROL 5 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: spans: a channel exit frees its slot at the open, a stop inside the day, a position that stands never, and one whose exit is due at the next open
CONTROL 6 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: the close run every day holds the very spans hold() takes over all the days at once
  FAIL section AB: spans: a channel exit frees its slot at the open, a stop inside the day, a position that stands never, and one whose exit is due at the next open
CONTROL 7 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 3 empty 0
  section AB: checks 145 failed 3
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: the close run every day holds the very spans hold() takes over all the days at once
  FAIL section AB: spans: a channel exit frees its slot at the open, a stop inside the day, a position that stands never, and one whose exit is due at the next open
CONTROL 8 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: the archive with ceilings keeps hold()'s trades: of two longs at one open, the major's alone
CONTROL 9 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: ceilings that change make the next run a baseline: the book re-read under them from GO_LIVE, the trades they hold now written and none told
CONTROL 10 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
CONTROL 11 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written -- and, its entry never told, not the book's: nothing told, no file of the book held
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
CONTROL 12 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: a position entered before GO_LIVE holds no slot: it is named left out, and the long it would block is held
CONTROL 13 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 3 empty 0
  section AB: checks 145 failed 3
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written -- and, its entry never told, not the book's: nothing told, no file of the book held
  FAIL section AB: the book held's ledger takes the trades it held, the plan's every entry: two files against four
  FAIL section AB: the close is told of the position held and of none left out, and the score is the book held's
CONTROL 14 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 9 empty 0
  section AB: checks 145 failed 9
  FAIL section AB: one a side and two in all: the baseline tells the major's long and the short in full, and names the two longs left out on one line under them
  FAIL section AB: its line: open=2 outside=2 opened=2 skipped=2; its record: the ceilings 1 and 2, the two held, the two left out with their side and day, the plan's four open
  FAIL section AB: the short stopped inside its day is the book's trade, in its ledger as in the plan's; the long its stop day opened finds the long side full: named left out with the ceilings, and no entry told
  FAIL section AB: a target reached is told of the position held alone, not of the plan's two left out
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
  FAIL section AB: a position entered before GO_LIVE holds no slot: it is named left out, and the long it would block is held
CONTROL 15 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
CONTROL 16 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: the look names the candidate the book would take, the major's long, and not the long it would leave out
CONTROL 17 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: a stop the day has reached on a position the book left out is not the look's to tell
CONTROL 18 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: the prints read in three pages give the same R, the plan's trade priced once for both its ledgers, and the late close is told once
FINAL exit=0 selftest: sections 28 checks 807 failed 0 empty 0
```

---

## 10. The patch

Against `main` at `23a003d`. B1 extracts the lines between the fences, and B2 applies them.

```diff
diff --git a/vps/book.py b/vps/book.py
index c7ecf00..39f4d9f 100644
--- a/vps/book.py
+++ b/vps/book.py
@@ -20,6 +20,14 @@ The plan the owner trades (TZ-80): the same entries, exits and stop, and in addi
 SCALE_R times the initial risk from the entry, half the position closes there and the rest's stop moves to the
 entry. replay(..., scale=SCALE_R) makes the plan's trades and replay(...) the rule's, from one loop.
 
+The book the owner can hold (TZ-81): the plan's entries taken in time, each only while his side ceiling and his
+book ceiling have room for it, the MAJORS first at one open and then the list's in its order. hold() decides it
+from every symbol's spans() -- live and over the archive alike.
+
+    book.py --archive --scale 2 --hold SIDE,BOOK SYMBOL...
+                                                the plan held under those ceilings, the symbols in the
+                                                list's order
+
 Python 3.12's standard library only. Time is UTC everywhere.
 """
 import argparse
@@ -28,6 +36,7 @@ import csv
 import io
 import json
 import os
+import re
 import sys
 import time
 import urllib.error
@@ -44,6 +53,12 @@ OOS_START = date(2025, 1, 1)
 # The plan's target, in R from the entry: the owner's request of 24.10.2026 and methodology 2026-10-24-c, measured
 # on the archive by the Architect on 24.10.2026 (map section 10, row "The book prints no target").
 SCALE_R = 2.0
+# Map section 10, row "The book's out-of-sample loss sits in the alts": the five symbols its lead names. At one
+# open the book takes them before the others, and the alert prints them first (TZ-80, TZ-81).
+MAJORS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT")
+# At one open (TZ-81): an exit at the open frees its slot before the entries, which are taken in rank order; a
+# stop fills inside the day and frees its slot after them.
+AT_OPEN, ENTRY, IN_DAY = 0, 1, 2
 DAY_MS = 86_400_000
 HTTP_TIMEOUT_S = 20
 FAPI_KLINES = "https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1d&limit=400"
@@ -159,6 +174,45 @@ def result_r(tr, funding):
     return (gain - paid - 2 * COST_SIDE) / dist
 
 
+def rank(symbols):
+    """The order the book takes one open's entries in (TZ-81): the MAJORS first, then the others, each in the
+    order given -- the list's. A symbol's rank by name."""
+    return {s: k for k, s in enumerate(sorted(symbols, key=lambda s: s not in MAJORS))}
+
+
+def spans(symbol, trades, pos, t_next=None):
+    """One symbol's positions as hold() reads them (TZ-81): (symbol, side, t_entry, free) each, free the (time,
+    phase) at which the position's slot frees, or None while it stands. A position whose exit is due frees its
+    slot at t_next, the open of the day still forming."""
+    out = [(symbol, tr["side"], tr["t_entry"], (tr["t_exit"], AT_OPEN if tr["why"] == "channel" else IN_DAY))
+           for tr in trades]
+    if pos is not None:
+        out.append((symbol, pos["side"], pos["t_entry"],
+                    (t_next, AT_OPEN) if pos.get("exit_due") and t_next is not None else None))
+    return out
+
+
+def hold(books, ranks, side_max, book_max, fixed=None):
+    """The book the owner can hold (TZ-81): the (symbol, t_entry) of each span it takes. Walked in time from an
+    empty book, an entry is taken where, at its open, fewer than side_max positions are held on its side and
+    fewer than book_max in all, and a position taken keeps its slot until its own exit -- after its target as
+    before it. An entry not taken at its own open is never taken. fixed maps an entry already decided to whether
+    it was taken, and the walk takes or leaves it so whatever the room."""
+    events = []
+    for symbol, side, t_entry, free in books:
+        events.append(((t_entry, ENTRY, ranks[symbol]), (symbol, t_entry), side))
+        if free is not None:
+            events.append((free + (ranks[symbol],), (symbol, t_entry), side))
+    now, taken = {}, set()
+    for (_, phase, _), key, side in sorted(events):
+        if phase != ENTRY:
+            now.pop(key, None)
+        elif (fixed or {}).get(key, list(now.values()).count(side) < side_max and len(now) < book_max):
+            now[key] = side
+            taken.add(key)
+    return taken
+
+
 def _get(url):
     with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_S) as r:
         return r.read()
@@ -295,16 +349,22 @@ def archive_paths(symbol, start, end):
     return paths
 
 
-def archive(symbols, start, end, cache, workers=8, scale=None):
+def archive(symbols, start, end, cache, workers=8, scale=None, ceilings=None):
+    """Every trade over the archive and its table; with ceilings, (side, book), only the trades hold() takes, the
+    symbols ranked in the order given (TZ-81)."""
     with concurrent.futures.ThreadPoolExecutor(workers) as ex:
         list(ex.map(lambda path: _archive_blob(path, cache),
                     [path for s in symbols for path in archive_paths(s, start, end)]))
-    rows = []
+    rows, books = [], []
     for s in symbols:
         bars, funding = archive_series(s, start, end, cache)
-        trades, _ = replay(bars, scale=scale)
+        trades, pos = replay(bars, scale=scale)
+        books += spans(s, trades, pos)
         for tr in trades:
             rows.append((tr["t_exit"], s, tr["side"], tr["t_entry"], result_r(tr, funding), tr["why"]))
+    if ceilings is not None:
+        taken = hold(books, rank(symbols), *ceilings)
+        rows = [r for r in rows if (r[1], r[3]) in taken]
     rows.sort()
     oos = datetime(OOS_START.year, OOS_START.month, OOS_START.day, tzinfo=timezone.utc).timestamp() * 1000
     out = {}
@@ -324,10 +384,14 @@ def main(argv=None):
     ap.add_argument("--to", dest="end", default=None)
     ap.add_argument("--cache", default=os.path.join(os.path.expanduser("~"), ".cache", "crypto-book"))
     ap.add_argument("--scale", type=float, default=None, help="the plan: half closes at this many R (TZ-80)")
+    ap.add_argument("--hold", default=None, metavar="SIDE,BOOK",
+                    help="the archive's trades the book holds under these ceilings (TZ-81)")
     ap.add_argument("symbols", nargs="+")
     a = ap.parse_args(argv)
     if a.live == a.archive:
         ap.error("exactly one of --live and --archive")
+    if a.hold is not None and (a.live or not re.fullmatch(r"[1-9]\d*,[1-9]\d*", a.hold)):
+        ap.error("--hold SIDE,BOOK reads the archive; the live book held is score.py's")
     if a.live:
         now_ms = int(time.time() * 1000)
         for s in a.symbols:
@@ -339,7 +403,8 @@ def main(argv=None):
         return 0
     os.makedirs(a.cache, exist_ok=True)
     end = date.fromisoformat(a.end) if a.end else (datetime.now(timezone.utc).date() - timedelta(days=2))
-    rows, out = archive(a.symbols, date.fromisoformat(a.start), end, a.cache, scale=a.scale)
+    rows, out = archive(a.symbols, date.fromisoformat(a.start), end, a.cache, scale=a.scale,
+                        ceilings=None if a.hold is None else tuple(int(n) for n in a.hold.split(",")))
     for name, s in out.items():
         if not s["n"]:
             print("%-14s no trades" % name); continue
diff --git a/vps/score.py b/vps/score.py
index 617fc61..be317ae 100644
--- a/vps/score.py
+++ b/vps/score.py
@@ -1,26 +1,31 @@
 #!/usr/bin/env python3
-"""The book's signal and its forward ledger (TZ-79, TZ-80). It runs no model and reads no credential.
+"""The book's signal and its forward ledger (TZ-79, TZ-80, TZ-81). It runs no model and reads no credential.
 
     score.py [--state DIR] [--outbox DIR]              the daily close
     score.py --forming [--state DIR] [--outbox DIR]    the look at the day still forming
 
-The daily close: every entry, target and exit of the plan the owner trades on the list reaches him as one
-alert -- each entry with its stop, its target and its size at his medium risk -- and every trade the plan and
-the rule have closed since the book went into code is written once to a ledger that no later run rewrites.
+The daily close: every entry, target and exit of the book the owner holds reaches him as one alert -- each
+entry with its stop, its target and its size at his medium risk, and the plan's entries his ceilings leave no
+room for named on one line -- and every trade the book, the plan and the rule have closed since the book went
+into code is written once to a ledger that no later run rewrites.
 
-The look: once a day, hours before the close, what the day has already done to the plan's positions -- a stop
+The look: once a day, hours before the close, what the day has already done to the book's positions -- a stop
 reached, a target reached -- and the entry its close would make if it came at the last price reach him as one
 alert, the entry named a candidate, because the close may still take it back. The look writes no ledger and
 opens no trade: the daily close alone does.
 
 The book is book.state_of() on one read of each symbol: the rule's state, which `book.py --live` prints, and
 the plan's, which `book.py --live --scale 2` prints; the look's is the plan's on the same bars with the day
-still forming appended as it stands. A trade's result is book.result_r() on the funding prints the exchange
-publishes for its span; a trade whose prints did not arrive whole is not written, and the next run asks again
-(map inv. 70). The size and the ceilings are the owner's, read from analyst/owner.json through paper.py
+still forming appended as it stands. The book held is book.hold() over the plan's positions entered since
+GO_LIVE, under the owner's ceilings (TZ-81): what he is told and what the gate scores are one book, and a run
+that cannot read his ceilings writes nothing. A trade's result is book.result_r() on the funding prints the
+exchange publishes for its span; a trade whose prints did not arrive whole is not written, and the next run asks
+again (map inv. 70). The size and the ceilings are the owner's, read from analyst/owner.json through paper.py
 (inv. 38).
 
-    score-plan/           the plan's ledger: one closed trade a file, as score-ledger/ below
+    score-held/           the book held's ledger, which the gate reads: one closed trade a file, as
+                          score-ledger/ below
+    score-plan/           the plan's every entry, the same way
     score-ledger/         one closed trade a file, <SYMBOL>-<entry stamp>.json, written once and within
                           RETRY_DAYS of its close, and never reopened (map inv. 38): a later replay that
                           reads its trade differently is counted, and a close found later than that is
@@ -29,12 +34,14 @@ publishes for its span; a trade whose prints did not arrive whole is not written
     score-forming/        one look a file, <YYYY-MM-DD>.json, written once: what the look named, so that
                           the next close counts how much of it came true; a day that has its file is not
                           looked at again
-    score.json            the daily close's reading: the day it stands on, the plan's open positions, both
-                          totals, and the look's count for that day
+    score.json            the daily close's reading: the day it stands on, the ceilings, the book held's open
+                          positions and the plan's it leaves out, the three ledgers' totals, and the look's
+                          count for that day
 
 Prints one line, and one before it for each trade it could not price; never a price.
 Exit 0 the reading is written, or the day was already looked at · 4 no symbol was read, or the read is older
-than the record: nothing written · 5 a file of the ledger is not a trade: nothing written.
+than the record: nothing written · 5 a file of the ledger is not a trade: nothing written · 6 the owner's
+ceilings are unread: nothing written.
 """
 import argparse
 import json
@@ -52,9 +59,8 @@ import writer  # noqa: E402
 
 # Methodology 2026-10-21-a: the first day every level the answer prints is this book's.
 GO_LIVE = "2026-10-21"
-# Map section 10, row "The book's out-of-sample loss sits in the alts": the five symbols its lead names,
-# totalled apart from the first forward day, so that the lead is read on trades it has not seen.
-MAJORS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT")
+# book.MAJORS, totalled apart from the first forward day, so that the lead is read on trades it has not seen.
+MAJORS = book.MAJORS
 FUNDING_URL = "https://fapi.binance.com/fapi/v1/fundingRate?symbol=%s&startTime=%d&endTime=%d&limit=1000"
 FUNDING_PAGE = 1000                              # the endpoint's own ceiling of rows an answer
 FUNDING_PAGES_MAX = 20
@@ -68,6 +74,7 @@ FUNDING_GAP_MS = 8 * 3600 * 1000 + 60 * 1000
 RETRY_DAYS = 60
 LEDGER = "score-ledger"
 PLAN = "score-plan"
+HELD = "score-held"
 FORMING = "score-forming"
 RECORD = "score.json"
 LEDGER_KEYS = ("symbol", "side", "t_entry", "entry", "stop", "t_exit", "exit", "why", "r", "seen")
@@ -122,6 +129,7 @@ T_LIMIT = ("\u26a0\ufe0f \u0412\u0430\u0448 \u043b\u0438\u043c\u0438\u0442: {sid
            "\u043a\u0430\u0436\u0434\u0430\u044f \u0434\u043e \u2212{risk} USDT \u2014 "
            "\u0441\u0447\u0438\u0442\u0430\u0439\u0442\u0435 \u0432\u043c\u0435\u0441\u0442\u0435 \u0441 "
            "\u043e\u0442\u043a\u0440\u044b\u0442\u044b\u043c\u0438.")
+T_OUT = "\u23f8 **\u0412\u043d\u0435 \u043b\u0438\u043c\u0438\u0442\u0430:** {items}"
 T_LEGEND = ("R \u2014 \u043e\u0434\u0438\u043d \u0440\u0438\u0441\u043a \u043d\u0430 "
             "\u0441\u0434\u0435\u043b\u043a\u0443.")
 # The look at the day still forming (TZ-80): what has happened is told as it is, what the close may still
@@ -161,6 +169,11 @@ def day(ms):
     return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")
 
 
+def day_ms(iso):
+    """The millisecond stamp at which a UTC date, YYYY-MM-DD, begins."""
+    return int(datetime.fromisoformat(iso).replace(tzinfo=timezone.utc).timestamp() * 1000)
+
+
 def funding_prints(symbol, t_entry, t_exit):
     """The symbol's funding prints of a trade's span as sorted (t_ms, rate) pairs, read page by page and
     refused unless whole: a list of rows with a finite rate each, the first print inside the span within
@@ -246,15 +259,14 @@ def side_of(state):
 
 
 def entry_lines(o, own):
-    """An entry in two lines: the side, the entry and the stop; then the target and, with the owner's book,
-    the size that loses his medium risk at that stop and its margin at the leverage paper.copy_size names."""
+    """An entry in two lines: the side, the entry and the stop; then the target, the size that loses the owner's
+    medium risk at that stop and its margin at the leverage paper.copy_size names."""
     side = side_of(o)
     line = T_ENTRY.format(dot=DOT[side], side=SIDE_HEAD[side], sym=name(o["symbol"]), entry=px(o["entry"]),
                           stop=px(o["stop"]), dist=signed((o["stop"] / o["entry"] - 1) * 100, 1))
-    plan = T_PLAN.format(target=px(o["target"]), tdist=signed((o["target"] / o["entry"] - 1) * 100, 1))
-    if own is not None:
-        notional, margin, lev, _ = paper.copy_size(own, abs(o["stop"] / o["entry"] - 1))
-        plan += T_PLAN_SIZE.format(notional="%d" % round(notional), margin="%d" % round(margin), lev=lev)
+    notional, margin, lev, _ = paper.copy_size(own, abs(o["stop"] / o["entry"] - 1))
+    plan = (T_PLAN.format(target=px(o["target"]), tdist=signed((o["target"] / o["entry"] - 1) * 100, 1))
+            + T_PLAN_SIZE.format(notional="%d" % round(notional), margin="%d" % round(margin), lev=lev))
     return [line if o["entry_due"] else line + T_LATE.format(date=ddmm(o["entry_date"])), plan]
 
 
@@ -262,13 +274,18 @@ def majors_first(rows):
     return sorted(rows, key=lambda o: o["symbol"] not in MAJORS)
 
 
-def compose(asof, baseline, opened, scaled, closing, closed, rows, open_rows, own):
-    """The daily close's alert: one event to a line -- an entry in two, the majors first -- then the plan's
-    record since GO_LIVE, and under an entry what the target means, when to enter and the owner's ceilings.
-    The baseline also prints every position held, with its stop and its target, one to a line."""
+def compose(asof, baseline, opened, skipped, scaled, closing, closed, rows, open_rows, own):
+    """The daily close's alert: one event to a line -- an entry in two, the majors first, then on one line the
+    plan's entries the ceilings leave out -- then the book's record since GO_LIVE, and under an entry what the
+    target means, when to enter and the owner's ceilings. The baseline also prints every position held, with its
+    stop and its target, one to a line."""
     lines = [(T_HEAD_BASE if baseline else T_HEAD).format(d=ddmm(asof))]
     for o in majors_first(opened):
         lines += entry_lines(o, own)
+    if skipped:
+        lines.append(T_OUT.format(items=" \u00b7 ".join(
+            SIDE[side] + " " + ", ".join(name(o["symbol"]) for o in majors_first(skipped) if side_of(o) == side)
+            for side in (1, -1) if any(side_of(o) == side for o in skipped))))
     for o in scaled:
         lines.append(T_SCALED.format(sym=name(o["symbol"]), side=SIDE[side_of(o)], px=px(o["scale_px"]),
                                      stop=px(o["stop_now"])))
@@ -304,10 +321,10 @@ def compose(asof, baseline, opened, scaled, closing, closed, rows, open_rows, ow
         lines.append(T_HOW)
     if opened:
         lines.append(T_WHEN)
-        if own is not None:
-            side_n, book_n = paper.ceilings(own)
-            lines.append(T_LIMIT.format(side_n=side_n, book_n=book_n, risk="%d" % round(
-                paper.risk_usdt(own["capital_usdt"], own["risk_pct"] / 100))))
+    if opened or skipped:
+        side_n, book_n = paper.ceilings(own)
+        lines.append(T_LIMIT.format(side_n=side_n, book_n=book_n, risk="%d" % round(
+            paper.risk_usdt(own["capital_usdt"], own["risk_pct"] / 100))))
     if baseline:
         lines.append(T_LEGEND)
     return "\n".join(lines)
@@ -330,13 +347,43 @@ def compose_look(day_now, hours, stopped, scaled, entries):
     return "\n".join(lines)
 
 
+def record_of(state_dir):
+    """The daily close's last record, or None where there is none or it does not parse."""
+    try:
+        with open(os.path.join(state_dir, RECORD), encoding="utf-8") as fh:
+            return json.load(fh)
+    except (OSError, ValueError):
+        return None
+
+
+def holds(prev, ceilings):
+    """Whether the last record holds a book under these ceilings (TZ-81): its v is 3 and its ceilings are these."""
+    return isinstance(prev, dict) and prev.get("v") == 3 and prev.get("ceilings") == ceilings
+
+
+def book_held(books, symbols, unread, ceilings, prev):
+    """The book held (TZ-81): the spans book.hold() takes of the plan's, entered since GO_LIVE. Where the last
+    record holds a book under these ceilings, what it decided stands -- each entry up to the open it told is taken
+    if that record took it and left out if not -- and the spans it held on a symbol unread today stand as it
+    recorded them."""
+    fixed, carried = None, []
+    if holds(prev, ceilings):
+        told = day_ms(prev["asof"]) + book.DAY_MS
+        carried = [(s, side, t, None if free is None else tuple(free)) for s, side, t, free in prev["held"]
+                   if s in unread]
+        took = {(s, t) for s, _, t, _ in prev["held"]}
+        fixed = {(s, t): (s, t) in took for s, _, t, _ in books + carried if t <= told}
+    taken = book.hold(books + carried, book.rank(symbols), *ceilings, fixed)
+    return [sp for sp in books + carried if (sp[0], sp[2]) in taken]
+
+
 def look_of(state_dir, day_iso):
     """The look's record of a day as (the entries it named, as (symbol, side) pairs), or None where the day was
     not looked at or its file is not a look."""
     try:
         with open(os.path.join(state_dir, FORMING, day_iso + ".json"), encoding="utf-8") as fh:
             doc = json.load(fh)
-        if doc["day"] != day_iso:
+        if doc["v"] != 2 or doc["day"] != day_iso:
             return None
         return {(str(e["symbol"]), int(e["side"])) for e in doc["entries"]}
     except (OSError, ValueError, KeyError, TypeError, AttributeError):
@@ -347,37 +394,48 @@ def forming(args, now_ms):
     """The look at the day still forming: one read of each symbol, the plan's state at the last close and its
     state if the day closed at the last price. Told as it is: a stop the day has reached, a target it has
     reached -- neither can be taken back. Told as a candidate: the entry a close at the last price would make.
-    An exit that close would make is not told: nothing is done about it before the close, which tells it. One
-    look a UTC day; the alert is written before the record, so that a look that died between them is made
-    again."""
+    An exit that close would make is not told: nothing is done about it before the close, which tells it. Only
+    the book held is told (TZ-81): a stop or a target of a position it holds, and a candidate it would take at
+    the next open. One look a UTC day; the alert is written before the record, so that a look that died between
+    them is made again."""
     day_now = day(now_ms)
     path = os.path.join(args.state, FORMING, day_now + ".json")
     if os.path.exists(path):
         common.log("score: forming day=%s already looked at, nothing written" % day_now)
         return 0
-    symbols = list_symbols()
-    stopped, scaled, entries, unread = [], [], [], []
+    own = paper.owner_now()
+    if own is None:
+        common.log("score: forming day=%s the owner's ceilings are unread, nothing written" % day_now)
+        return 6
+    symbols, go = list_symbols(), day_ms(GO_LIVE)
+    read, books, unread = [], [], []
     for symbol in symbols:
         try:
             bars, today = book.live_day(symbol, now_ms)
             if day(today[0]) != day_now:
                 raise ValueError("the day still forming is not today")
             now = book.state_of(symbol, bars, today[1], book.SCALE_R)[0]
-            then, trades, _ = book.state_of(symbol, bars + [today], today[4], book.SCALE_R)
+            then, trades, pos = book.state_of(symbol, bars + [today], today[4], book.SCALE_R)
         except Exception:                 # one symbol's failure never hides the others
             unread.append(symbol)
             continue
+        read.append((symbol, today, now, then, trades, pos))
+        books += [sp for sp in book.spans(symbol, trades, pos, today[0] + book.DAY_MS) if sp[2] >= go]
+    if len(unread) == len(symbols):
+        common.log("score: forming day=%s symbols=%d read=0 nothing written" % (day_now, len(symbols)))
+        return 4
+    taken = {(s, t) for s, _, t, _ in book_held(books, symbols, unread, list(paper.ceilings(own)),
+                                                record_of(args.state))}
+    stopped, scaled, entries = [], [], []
+    for symbol, today, now, then, trades, pos in read:
         stopped += [(symbol, tr["side"], tr["exit"]) for tr in trades
-                    if tr["t_exit"] == today[0] and tr["why"] == "stop"]
-        if then["state"] not in ("long", "short"):
+                    if tr["t_exit"] == today[0] and tr["why"] == "stop" and (symbol, tr["t_entry"]) in taken]
+        if then["state"] not in ("long", "short") or (symbol, pos["t_entry"]) not in taken:
             continue
         if then.get("scale_date") == day_now:
             scaled.append(then)
         if then["entry_due"]:         # the level the close must cross is the last close's trigger
             entries.append((then, today[4], now.get("long_trigger" if side_of(then) > 0 else "short_trigger")))
-    if len(unread) == len(symbols):
-        common.log("score: forming day=%s symbols=%d read=0 nothing written" % (day_now, len(symbols)))
-        return 4
     stopped.sort(key=lambda item: item[0] not in MAJORS)
     scaled = majors_first(scaled)
     entries.sort(key=lambda item: item[0]["symbol"] not in MAJORS)
@@ -388,7 +446,7 @@ def forming(args, now_ms):
                             outbox_dir=args.outbox)
     os.makedirs(os.path.dirname(path), mode=0o750, exist_ok=True)
     common.atomic_write(path, {
-        "v": 1, "k": "score-forming", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000)),
+        "v": 2, "k": "score-forming", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000)),
         "day": day_now, "symbols": len(symbols), "unread": sorted(unread),
         "stopped": [symbol for symbol, _, _ in stopped], "scaled": [o["symbol"] for o in scaled],
         "entries": [{"symbol": o["symbol"], "side": side_of(o)} for o, _, _ in entries]}, mode=0o640)
@@ -398,9 +456,10 @@ def forming(args, now_ms):
     return 0
 
 
-def ledger_pass(path, ledger, live, asof, seen):
+def ledger_pass(path, ledger, live, asof, seen, priced=None):
     """One ledger's run: (added, pending, late, disagree). live is (state, trades) per symbol read today; a trade
-    is written as the module's docstring says, each a new file (inv. 38)."""
+    is written as the module's docstring says, each a new file (inv. 38). priced, shared by the ledgers of one
+    replay, keeps each trade's R so that a trade two of them write is priced once (TZ-81)."""
     known = {(row["symbol"], row["t_entry"]): row for row in ledger}
     floor = GO_LIVE if not ledger else (date.fromisoformat(asof) - timedelta(days=RETRY_DAYS)).isoformat()
     added, pending, late, disagree = [], 0, 0, 0
@@ -417,13 +476,17 @@ def ledger_pass(path, ledger, live, asof, seen):
                 late += 1
                 continue
             try:
-                r = book.result_r(tr, funding_prints(state["symbol"], tr["t_entry"], tr["t_exit"]))
+                r = (priced or {}).get(key)
+                if r is None:
+                    r = book.result_r(tr, funding_prints(state["symbol"], tr["t_entry"], tr["t_exit"]))
                 if not math.isfinite(r):
                     raise ValueError("the result is not finite")
             except Exception as exc:      # not written: the next run asks for the prints again (inv. 70)
                 pending += 1
                 common.log("score: pending %s %s %s" % (os.path.basename(path), state["symbol"], exc.__class__.__name__))
                 continue
+            if priced is not None:
+                priced[key] = r
             known[key] = {"symbol": state["symbol"], "side": tr["side"], "t_entry": tr["t_entry"],
                           "entry": tr["entry"], "stop": tr["stop"], "t_exit": tr["t_exit"], "exit": tr["exit"],
                           "why": tr["why"], "r": r, "seen": seen}
@@ -444,21 +507,26 @@ def main(argv=None, now_ms=None):
     now_ms = int(time.time() * 1000) if now_ms is None else now_ms
     if args.forming:
         return forming(args, now_ms)
+    own = paper.owner_now()
+    if own is None:
+        common.log("score: the owner's ceilings are unread, nothing written")
+        return 6
+    ceilings = list(paper.ceilings(own))
     rule_path, plan_path = os.path.join(args.state, LEDGER), os.path.join(args.state, PLAN)
-    record_path = os.path.join(args.state, RECORD)
+    held_path, record_path = os.path.join(args.state, HELD), os.path.join(args.state, RECORD)
     try:
-        rule_ledger, plan_ledger = read_ledger(rule_path), read_ledger(plan_path)
+        rule_ledger, plan_ledger, held_ledger = read_ledger(rule_path), read_ledger(plan_path), read_ledger(held_path)
     except (OSError, ValueError, TypeError):
         common.log("score: a file of the ledger is not a trade, nothing written")
         return 5
+    prev = record_of(args.state)
     try:
-        with open(record_path, encoding="utf-8") as fh:
-            prev = json.load(fh)
-        prev_asof, prev_ts, prev_v = str(prev["asof"]), str(prev["ts"]), prev.get("v")
-    except (OSError, ValueError, KeyError, TypeError, AttributeError):
-        prev_asof = prev_ts = prev_v = None
-    # TZ-79's record (v 1) knew no plan: the first run after it is the plan's baseline, and tells no close.
-    baseline = prev_asof is None or prev_v != 2
+        prev_asof, prev_ts = str(prev["asof"]), str(prev["ts"])
+    except (KeyError, TypeError, AttributeError):
+        prev = prev_asof = prev_ts = None
+    # A record before TZ-81's (v 3) held no book, and one under other ceilings held another: the first run after
+    # it is the book's baseline, and tells no close.
+    baseline = not holds(prev, ceilings)
 
     symbols = list_symbols()
     read, unread = [], []
@@ -478,47 +546,64 @@ def main(argv=None, now_ms=None):
     fresh = baseline or asof > prev_asof
     seen = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000))
 
+    go, t_next = day_ms(GO_LIVE), day_ms(asof) + book.DAY_MS
+    held = book_held([sp for _, plan in live for sp in book.spans(plan[0]["symbol"], plan[1], plan[2], t_next)
+                      if sp[2] >= go], symbols, unread, ceilings, prev)
+    taken = {(s, t) for s, _, t, _ in held}
+    priced = {}
     rule_added, rule_pending, rule_late, rule_disagree = ledger_pass(
         rule_path, rule_ledger, [(rule[0], rule[1]) for rule, _ in live], asof, seen)
-    plan_added, pending, late, disagree = ledger_pass(
-        plan_path, plan_ledger, [(plan[0], plan[1]) for _, plan in live], asof, seen)
-    rule_rows, rows = rule_ledger + rule_added, plan_ledger + plan_added
-
-    open_rows = [plan[0] for _, plan in live if plan[0]["state"] in ("long", "short")]
+    plan_added, plan_pending, plan_late, plan_disagree = ledger_pass(
+        plan_path, plan_ledger, [(plan[0], plan[1]) for _, plan in live], asof, seen, priced)
+    added, pending, late, disagree = ledger_pass(
+        held_path, held_ledger, [(plan[0], [tr for tr in plan[1] if (plan[0]["symbol"], tr["t_entry"]) in taken])
+                                 for _, plan in live], asof, seen, priced)
+    rule_rows, plan_rows, rows = rule_ledger + rule_added, plan_ledger + plan_added, held_ledger + added
+
+    plan_open = [plan for _, plan in live if plan[0]["state"] in ("long", "short")]
+    open_rows = [plan[0] for plan in plan_open if (plan[0]["symbol"], plan[2]["t_entry"]) in taken]
+    outside = [plan[0] for plan in plan_open if (plan[0]["symbol"], plan[2]["t_entry"]) not in taken]
     if baseline:
         opened = [o for o in open_rows if o["entry_due"] or (prev_asof is not None and o["entry_date"] > prev_asof)]
+        skipped = list(outside)
     else:
         after = (date.fromisoformat(prev_asof) + timedelta(days=1)).isoformat()
         opened = [o for o in open_rows if fresh and o["entry_date"] > after]
+        skipped = [o for o in outside if fresh and o["entry_date"] > after]
     scaled = [] if baseline else [o for o in open_rows if fresh and o.get("scale_date", "") > prev_asof]
     closing = [o for o in open_rows if fresh and o["exit_due"]]
     # A closed trade is told once: the rows written since the record this run replaces.
     closed = [] if baseline else [row for row in rows if row["seen"] > prev_ts]
-    alert = baseline or bool(opened or scaled or closing or closed)
+    alert = baseline or bool(opened or skipped or scaled or closing or closed)
     # What the look at the day that has just closed named, against the entries that close made.
     named = look_of(args.state, asof)
     due = {(o["symbol"], side_of(o)) for o in open_rows if o["entry_due"]}
     look = None if named is None else {"named": len(named), "hit": len(named & due), "entries": len(due)}
     if alert:
-        common.write_outbox("alert", compose(asof, baseline, opened, scaled, closing, closed, rows, open_rows,
-                                             paper.owner_now()), outbox_dir=args.outbox)
+        common.write_outbox("alert", compose(asof, baseline, opened, skipped, scaled, closing, closed, rows,
+                                             open_rows, own), outbox_dir=args.outbox)
 
     def by_group(group):
         return {"all": totals(group), "majors": totals([row for row in group if row["symbol"] in MAJORS]),
                 "others": totals([row for row in group if row["symbol"] not in MAJORS])}
     common.atomic_write(record_path, {
-        "v": 2, "k": "score", "ts": seen, "asof": asof, "since": GO_LIVE, "symbols": len(symbols),
-        "unread": sorted(unread),
+        "v": 3, "k": "score", "ts": seen, "asof": asof, "since": GO_LIVE, "symbols": len(symbols),
+        "unread": sorted(unread), "ceilings": ceilings,
+        "held": sorted([s, side, t, None if free is None else list(free)] for s, side, t, free in held),
         "open": [{key: o.get(key) for key in ("symbol", "state", "entry_date", "entry", "stop", "target", "exit_level",
                                               "r_open", "entry_due", "exit_due", "scale_date", "stop_now")}
                  for o in open_rows],
+        "outside": [{key: o.get(key) for key in ("symbol", "state", "entry_date")} for o in majors_first(outside)],
         "closed": by_group(rows), "pending": pending, "late": late, "disagree": disagree, "look": look,
+        "plan": {"open": len(plan_open), "closed": by_group(plan_rows), "pending": plan_pending, "late": plan_late,
+                 "disagree": plan_disagree},
         "rule": {"open": sum(1 for rule, _ in live if rule[0]["state"] in ("long", "short")), "closed": by_group(rule_rows),
                  "pending": rule_pending, "late": rule_late, "disagree": rule_disagree}}, mode=0o640)
-    common.log("score: asof=%s symbols=%d read=%d unread=%d open=%d opened=%d scaled=%d closing=%d closed=%d "
-               "pending=%d late=%d disagree=%d ledger=%d rule=%d look=%s alert=%s"
-               % (asof, len(symbols), len(symbols) - len(unread), len(unread), len(open_rows), len(opened),
-                  len(scaled), len(closing), len(closed), pending, late, disagree, len(rows), len(rule_rows),
+    common.log("score: asof=%s symbols=%d read=%d unread=%d open=%d outside=%d opened=%d skipped=%d scaled=%d "
+               "closing=%d closed=%d pending=%d late=%d disagree=%d ledger=%d plan=%d rule=%d look=%s alert=%s"
+               % (asof, len(symbols), len(symbols) - len(unread), len(unread), len(open_rows), len(outside),
+                  len(opened), len(skipped), len(scaled), len(closing), len(closed), pending, late, disagree,
+                  len(rows), len(plan_rows), len(rule_rows),
                   "-" if look is None else "%d/%d/%d" % (look["hit"], look["named"], look["entries"]),
                   "yes" if alert else "no"))
     return 0
diff --git a/vps/selftest.py b/vps/selftest.py
index 99a667e..d0f8243 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -3145,17 +3145,24 @@ def section_w_orders(s):
         shutil.rmtree(tmp, ignore_errors=True)
 
 
-# --- AB: the book's signal and its forward ledger (TZ-79), the plan's (TZ-80) -----------------------------
-AB_LINE = re.compile(r"score: asof=\d{4}-\d\d-\d\d symbols=\d+ read=\d+ unread=\d+ open=\d+ opened=\d+ scaled=\d+ "
-                     r"closing=\d+ closed=\d+ pending=\d+ late=\d+ disagree=\d+ ledger=\d+ rule=\d+ "
-                     r"look=(-|\d+/\d+/\d+) alert=(yes|no)")
+# --- AB: the book's signal and its forward ledger (TZ-79), the plan's (TZ-80), the book held (TZ-81) -------------
+AB_LINE = re.compile(r"score: asof=\d{4}-\d\d-\d\d symbols=\d+ read=\d+ unread=\d+ open=\d+ outside=\d+ opened=\d+ "
+                     r"skipped=\d+ scaled=\d+ closing=\d+ closed=\d+ pending=\d+ late=\d+ disagree=\d+ ledger=\d+ "
+                     r"plan=\d+ rule=\d+ look=(-|\d+/\d+/\d+) alert=(yes|no)")
 AB_LOOK = re.compile(r"score: forming day=\d{4}-\d\d-\d\d symbols=\d+ read=\d+ unread=\d+ stopped=\d+ scaled=\d+ "
                      r"entries=\d+ alert=(yes|no)")
 AB_LOOK_MS = 15 * 3600 * 1000 + 10 * 60 * 1000          # the look's hour: 15:10 UTC
 AB_OWN = {"capital_usdt": 30000.0, "risk_pct": 0.5, "side_max_pct": 3.0, "book_max_pct": 5.0}
+AB_TIGHT = {"capital_usdt": 30000.0, "risk_pct": 0.5, "side_max_pct": 0.5, "book_max_pct": 1.0}   # 1 a side, 2 in all
 AB_H8 = 8 * 3600 * 1000
 
 
+def ab_later(world, days):
+    """The same world `days` days later: as many flat days first, every bar after them re-timed."""
+    return ([(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(days)]
+            + [(b[0] + days * book.DAY_MS,) + tuple(b[1:]) for b in world])
+
+
 def ab_klines(bars, fill, part=None):
     """What fapi's daily klines answer for these closed bars and a forming day that opened at fill -- or, with
     part, a forming day that stands at (open, high, low, last)."""
@@ -3235,7 +3242,7 @@ class AbHost:
 
     def ledger(self, which=None):
         """A ledger's files joined in name order, a trade a line; None while there is none. The rule's by default,
-        the plan's with which=score.PLAN."""
+        the plan's with which=score.PLAN, the book held's with which=score.HELD."""
         folder = os.path.join(self.state, which or score.LEDGER)
         try:
             names = sorted(os.listdir(folder))
@@ -3269,9 +3276,9 @@ def ab_field(printed, name):
 def section_ab(s):
     eps = 1e-9
     long_world, short_world = x_world_long(), x_world_short()
-    s.check("GO_LIVE is 2026-10-21 and MAJORS are BTC, ETH, SOL, BNB, XRP",
-            score.GO_LIVE == "2026-10-21"
-            and score.MAJORS == ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"))
+    s.check("GO_LIVE is 2026-10-21 and MAJORS, the book's, are BTC, ETH, SOL, BNB, XRP",
+            score.GO_LIVE == "2026-10-21" and score.MAJORS is book.MAJORS
+            and book.MAJORS == ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"))
     s.check("the list is BTCUSDT and then tokens[], as the payload carries it",
             score.list_symbols() == writer.payload_symbols(REPO) and score.list_symbols()[0] == "BTCUSDT"
             and len(score.list_symbols()) == len(checkout_tokens()) + 1)
@@ -3304,11 +3311,13 @@ def section_ab(s):
         code, printed, alerts, ledger, record = h.run(61)
         s.check("baseline: exit 0, one line of the fixed shape",
                 code == 0 and printed.count("\n") == 1 and AB_LINE.fullmatch(printed.rstrip("\n")) is not None)
-        s.check("baseline: the line reads symbols=2 read=1 unread=1 open=1 opened=1 ledger=0 rule=0 look=- alert=yes",
-                [ab_field(printed, f) for f in ("asof", "symbols", "read", "unread", "open", "opened", "scaled",
-                                                "closing", "closed", "pending", "late", "disagree", "ledger", "rule",
-                                                "look", "alert")]
-                == ["1970-03-02", "2", "1", "1", "1", "1", "0", "0", "0", "0", "0", "0", "0", "0", "-", "yes"])
+        s.check("baseline: the line reads symbols=2 read=1 unread=1 open=1 outside=0 opened=1 ledger=0 plan=0 rule=0 "
+                "look=- alert=yes",
+                [ab_field(printed, f) for f in ("asof", "symbols", "read", "unread", "open", "outside", "opened",
+                                                "skipped", "scaled", "closing", "closed", "pending", "late", "disagree",
+                                                "ledger", "plan", "rule", "look", "alert")]
+                == ["1970-03-02", "2", "1", "1", "1", "0", "1", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "-",
+                    "yes"])
         text = alerts[0][1] if alerts else ""
         s.check("baseline: one alert, of kind alert", len(alerts) == 1 and alerts[0][0] == "alert")
         s.check("baseline: its head names the day the book stands on",
@@ -3330,14 +3339,18 @@ def section_ab(s):
         s.check("baseline: the legend of R is printed once, and on no later alert",
                 text.split("\n").count(score.T_LEGEND) == 1)
         s.check("baseline: no ledger file is written while no trade has closed",
-                ledger is None and h.ledger(score.PLAN) is None)
-        s.check("record keys v k ts asof since symbols unread open closed pending late disagree look rule, in order",
-                record is not None and list(record) == ["v", "k", "ts", "asof", "since", "symbols", "unread", "open",
-                                                        "closed", "pending", "late", "disagree", "look", "rule"])
+                ledger is None and h.ledger(score.PLAN) is None and h.ledger(score.HELD) is None)
+        s.check("record keys v k ts asof since symbols unread ceilings held open outside closed pending late disagree "
+                "look plan rule, in order",
+                record is not None and list(record) == ["v", "k", "ts", "asof", "since", "symbols", "unread", "ceilings",
+                                                        "held", "open", "outside", "closed", "pending", "late",
+                                                        "disagree", "look", "plan", "rule"])
         s.check("a day nobody looked at carries no look's count", record is not None and record["look"] is None)
-        s.check("record v 2, k score, asof the last closed day, the unread symbol named",
-                record is not None and (record["v"], record["k"], record["asof"], record["unread"])
-                == (2, "score", "1970-03-02", ["BADUSDT"]))
+        s.check("record v 3, k score, asof the last closed day, the unread symbol named, the ceilings 6 and 10, the "
+                "book's one span: the long due at the open, standing",
+                record is not None and (record["v"], record["k"], record["asof"], record["unread"], record["ceilings"])
+                == (3, "score", "1970-03-02", ["BADUSDT"], [6, 10])
+                and record["held"] == [["AAAUSDT", 1, 61 * book.DAY_MS, None]])
         held = ((record or {}).get("open") or [{}])[0]
         s.check("record's open position: the entry due, its stop and target, no open R, no target reached",
                 record is not None and len(record["open"]) == 1 and abs(held.get("stop", 0) - 100.6) < eps
@@ -3346,10 +3359,11 @@ def section_ab(s):
                 == {"symbol": "AAAUSDT", "state": "long", "entry_date": "1970-03-03", "entry": 105.0,
                     "exit_level": 99.0, "r_open": None, "entry_due": True, "exit_due": False, "scale_date": None,
                     "stop_now": None})
-        s.check("record's closed totals, the plan's and the rule's, are empty summaries",
+        s.check("record's closed totals, the book held's, the plan's and the rule's, are empty summaries; nothing outside",
                 record is not None and record["closed"] == {"all": {"n": 0}, "majors": {"n": 0}, "others": {"n": 0}}
                 and record["rule"] == {"open": 1, "closed": {"all": {"n": 0}, "majors": {"n": 0}, "others": {"n": 0}},
-                                       "pending": 0, "late": 0, "disagree": 0})
+                                       "pending": 0, "late": 0, "disagree": 0}
+                and record["plan"] == record["rule"] and record["outside"] == [])
         s.check("the record's mode is 0640",
                 os.stat(os.path.join(h.state, score.RECORD)).st_mode & 0o7777 == 0o640)
         code, printed, alerts, ledger, record = h.run(62)
@@ -3389,6 +3403,9 @@ def section_ab(s):
                 and (plan_rows[0]["exit"], plan_rows[0]["why"]) == (122.0, "channel"))
         s.check("the plan's R: half the move to the target and half to the exit, the whole funding to the target's day "
                 "and half after it", bool(plan_rows) and abs(plan_rows[0]["r"] - want_plan) < eps)
+        s.check("the book held's ledger holds the trade it held, byte for byte the plan's file of it",
+                h.ledger(score.HELD) == h.ledger(score.PLAN) and [x[0] for x in h.stamps(score.HELD)]
+                == ["AAAUSDT-%d.json" % (61 * book.DAY_MS)] and [x[3] for x in h.stamps(score.HELD)] == [0o640])
         s.check("the closed trade is one ledger file, AAAUSDT-<its entry stamp>.json, with the ten keys in order",
                 len(rows) == 1 and list(rows[0]) == list(score.LEDGER_KEYS)
                 and [x[0] for x in h.stamps()] == ["AAAUSDT-%d.json" % (61 * book.DAY_MS)])
@@ -3408,10 +3425,12 @@ def section_ab(s):
                     sym="AAA", side=score.SIDE[1], why=score.WHY["channel"], r=score.signed(want_plan, 2))
                 and score.T_SCORE.format(since="01.01.1970", n=1, total=score.signed(want_plan, 2), wins=1) in text
                 and score.T_GROUPS.format(n1=0, r1="+0.00", n2=1, r2=score.signed(want_plan, 2)) in text)
-        s.check("the record totals the plan and the rule apart: one trade each, a null profit factor where nothing lost",
+        s.check("the record totals the book held, the plan and the rule apart: one trade each, a null profit factor "
+                "where nothing lost",
                 record["closed"]["all"]["n"] == 1 and record["closed"]["all"]["pf"] is None
                 and abs(record["closed"]["all"]["total"] - want_plan) < eps and record["closed"]["majors"] == {"n": 0}
                 and record["closed"]["others"]["n"] == 1 and record["open"] == []
+                and record["plan"]["closed"] == record["closed"] and record["plan"]["open"] == 0
                 and abs(record["rule"]["closed"]["all"]["total"] - want) < eps and record["rule"]["open"] == 0)
         s.check("the trade's file has mode 0640", [x[3] for x in h.stamps()] == [0o640])
         funding_calls, written = len([u for u in h.urls if "fundingRate" in u]), h.stamps()
@@ -3438,10 +3457,11 @@ def section_ab(s):
                 code == 0 and ledger is None and ab_field(printed, "pending") == "1" and record["pending"] == 1
                 and alerts == [])
         s.check("a trade it could not price is named on a line of its own per ledger, with the failure's class and no price",
-                printed.split("\n")[:2] == ["score: pending score-ledger AAAUSDT OSError",
-                                            "score: pending score-plan AAAUSDT OSError"]
-                and printed.count("\n") == 3 and AB_LINE.fullmatch(printed.split("\n")[2]) is not None
-                and record["rule"]["pending"] == 1)
+                printed.split("\n")[:3] == ["score: pending score-ledger AAAUSDT OSError",
+                                            "score: pending score-plan AAAUSDT OSError",
+                                            "score: pending score-held AAAUSDT OSError"]
+                and printed.count("\n") == 4 and AB_LINE.fullmatch(printed.split("\n")[3]) is not None
+                and record["rule"]["pending"] == 1 and record["plan"]["pending"] == 1)
         h.funding = lambda url: ab_funding(url, hole=(70 * book.DAY_MS, 71 * book.DAY_MS))
         code, printed, alerts, ledger, record = h.run(102)
         s.check("prints with a day missing inside the span: nothing written, the trade pending",
@@ -3455,7 +3475,8 @@ def section_ab(s):
         asked = len(h.urls)
         code, printed, alerts, ledger, record = h.run(102)
         rows = [json.loads(line) for line in (ledger or "").split("\n") if line]
-        s.check("the prints read in three pages give the same R, and the late close is told once",
+        s.check("the prints read in three pages give the same R, the plan's trade priced once for both its ledgers, and "
+                "the late close is told once",
                 len(rows) == 1 and abs(rows[0]["r"] - want) < eps and len(alerts) == 1
                 and len([u for u in h.urls[asked:] if "fundingRate" in u]) == 6
                 and alerts[0][1].split("\n")[1].startswith(score.T_CLOSED.split("{sym}")[0]))
@@ -3532,13 +3553,16 @@ def section_ab(s):
             code, printed, alerts, ledger, record = h.run(104)
         finally:
             score.RETRY_DAYS = saved_retry
-        s.check("a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told",
-                code == 0 and ab_field(printed, "late") == "1" and record["late"] == 1 and alerts == []
+        s.check("a close found more than RETRY_DAYS after its day: counted late by the plan's and the rule's ledgers, no "
+                "file written, nothing told",
+                code == 0 and record["plan"]["late"] == 1 and record["rule"]["late"] == 1 and alerts == []
                 and (ledger or "").count("\n") == 1 and "BBBUSDT" not in (ledger or ""))
         code, printed, alerts, ledger, record = h.run(104)
-        s.check("the same close inside RETRY_DAYS, which is 60: written and told",
-                score.RETRY_DAYS == 60 and ab_field(printed, "late") == "0" and (ledger or "").count("\n") == 2
-                and "BBBUSDT" in (ledger or "") and len(alerts) == 1)
+        s.check("the same close inside RETRY_DAYS, which is 60: written -- and, its entry never told, not the book's: "
+                "nothing told, no file of the book held",
+                score.RETRY_DAYS == 60 and record["plan"]["late"] == 0 and (ledger or "").count("\n") == 2
+                and "BBBUSDT" in (ledger or "") and "BBBUSDT" in (h.ledger(score.PLAN) or "")
+                and "BBBUSDT" not in (h.ledger(score.HELD) or "") and alerts == [])
         # --outbox names where the alert goes; without it, the bot's outbox.
         h = AbHost(os.path.join(tmp, "i"), {"AAAUSDT": long_world})
         aside = os.path.join(tmp, "aside")
@@ -3553,48 +3577,53 @@ def section_ab(s):
         s.check("--outbox: the alert is written there and nowhere else",
                 code == 0 and len(os.listdir(aside)) == 1 and os.listdir(aside)[0].endswith("-alert-%d.json" % os.getpid())
                 and os.listdir(h.outbox) == [])
-        # TZ-79's record (v 1) knew no plan: the next run is the plan's baseline and tells no close it fills.
+        # TZ-80's record (v 2) held no book: the next run is the book's baseline and tells no close it fills.
         h = AbHost(os.path.join(tmp, "k"), {"AAAUSDT": long_world, "BBBUSDT": long_world})
         with open(os.path.join(h.state, score.RECORD), "w", encoding="utf-8") as fh:
-            json.dump({"v": 1, "k": "score", "ts": "1970-03-04T00:10:00Z", "asof": "1970-03-03"}, fh)
+            json.dump({"v": 2, "k": "score", "ts": "1970-03-04T00:10:00Z", "asof": "1970-03-03"}, fh)
         h.worlds["BBBUSDT"] = long_world[:70] + [(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(70, 105)]
         code, printed, alerts, ledger, record = h.run(102)
         text = alerts[0][1] if alerts else ""
-        plan_files = [x[0] for x in h.stamps(score.PLAN)]
-        s.check("after TZ-79's record: one alert under the baseline's head, the plan's closes filled and none told",
+        held_files = [x[0] for x in h.stamps(score.HELD)]
+        s.check("after TZ-80's record: one alert under the baseline's head, the book's closes filled and none told",
                 code == 0 and len(alerts) == 1 and text.split("\n")[0] == score.T_HEAD_BASE.format(d="12.04")
-                and len(plan_files) == 2 and score.T_CLOSED.split("{sym}")[0] not in text and record["v"] == 2)
-        s.check("after TZ-79's record: the plan's record is in the score line, the legend once",
+                and len(held_files) == 2 and score.T_CLOSED.split("{sym}")[0] not in text and record["v"] == 3)
+        s.check("after TZ-80's record: the book's record is in the score line, the legend once",
                 score.T_SCORE.split("{n}")[0].format(since="01.01.1970") in text and text.split("\n").count(score.T_LEGEND) == 1)
         h = AbHost(os.path.join(tmp, "m"), {"AAAUSDT": long_world, "BTCUSDT": long_world})
         with open(os.path.join(h.state, score.RECORD), "w", encoding="utf-8") as fh:
-            json.dump({"v": 1, "k": "score", "ts": "1970-03-02T00:10:00Z", "asof": "1970-03-01"}, fh)
+            json.dump({"v": 2, "k": "score", "ts": "1970-03-02T00:10:00Z", "asof": "1970-03-01"}, fh)
         code, printed, alerts, ledger, record = h.run(70)
         text = alerts[0][1] if alerts else ""
-        s.check("after TZ-79's record: an entry since its day prints in full, with its target, the majors first",
+        s.check("after TZ-80's record: an entry since its day prints in full, with its target, the majors first",
                 text.split("\n")[1:3] == [score.T_ENTRY.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="BTC",
                                                                 entry="105", stop="100.6", dist="\u22124.2")
                                           + score.T_LATE.format(date="03.03"),
                                           score.T_PLAN.format(target="113.8", tdist="+8.4")
                                           + score.T_PLAN_SIZE.format(notional="3580", margin="1193", lev=3)])
         with open(os.path.join(h.state, score.RECORD), "w", encoding="utf-8") as fh:
-            json.dump({"v": 1, "k": "score", "ts": "1970-03-05T00:10:00Z", "asof": "1970-03-04"}, fh)
+            json.dump({"v": 2, "k": "score", "ts": "1970-03-05T00:10:00Z", "asof": "1970-03-04"}, fh)
         code, printed, alerts, ledger, record = h.run(70)
         text = alerts[0][1] if alerts else ""
-        s.check("after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop",
+        s.check("after TZ-80's record: a position it had told prints on one line, its target reached and the rest's stop",
                 score.T_HELD_DONE.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="BTC", stop="105")
                 in text.split("\n") and score.T_ENTRY.split("**")[0] not in "\n".join(text.split("\n")[1:2]))
-        # The owner's file unreadable: no size and no ceilings; majors first among the day's entries.
+        # The owner's file unreadable: no ceilings, so no book -- nothing read, written or told (TZ-81).
         h = AbHost(os.path.join(tmp, "j"), {"AAAUSDT": long_world, "ETHUSDT": long_world}, own=None)
+        code, printed, alerts, ledger, record = h.run(61)
+        s.check("the owner's file unreadable at the close: exit 6, one line, nothing read, written or told",
+                code == 6 and printed == "score: the owner's ceilings are unread, nothing written\n" and h.urls == []
+                and alerts == [] and os.listdir(h.state) == [])
+        code, printed, alerts, looked = h.look(61)
+        s.check("the owner's file unreadable at the look: exit 6, one line, nothing read, written or told",
+                code == 6 and printed == "score: forming day=1970-03-03 the owner's ceilings are unread, nothing written\n"
+                and h.urls == [] and alerts == [] and os.listdir(h.state) == [])
+        # Majors first among the day's entries.
+        h = AbHost(os.path.join(tmp, "j2"), {"AAAUSDT": long_world, "ETHUSDT": long_world})
         h.run(60)
         code, printed, alerts, ledger, record = h.run(62)
         text = alerts[0][1] if alerts else ""
         heads = [x for x in text.split("\n") if x.startswith(score.DOT[1] + " **")]
-        s.check("an entry without the owner's file: two lines, the target alone on the second, no size, no ceilings",
-                code == 0 and len(heads) == 2 and score.T_PLAN_SIZE.split("`")[0] not in text
-                and score.T_LIMIT.split("{")[0] not in text
-                and text.split("\n").count(score.T_PLAN.format(target="113.8", tdist="+8.4")) == 2
-                and text.split("\n")[-2:] == [score.T_HOW, score.T_WHEN])
         s.check("the day's entries print BTC ETH SOL BNB XRP first, then the others in the list's order",
                 [x.split("**")[1] for x in heads] == [score.SIDE_HEAD[1] + " ETH", score.SIDE_HEAD[1] + " AAA"])
         # The look at the day still forming (TZ-80): what the day has done, and what its close would do.
@@ -3630,9 +3659,9 @@ def section_ab(s):
                 looked is not None and list(looked) == ["v", "k", "ts", "day", "symbols", "unread", "stopped", "scaled",
                                                         "entries"]
                 and os.stat(os.path.join(h.state, score.FORMING, "1970-03-02.json")).st_mode & 0o7777 == 0o640)
-        s.check("the look's record: v 1, k score-forming, its day, the unread symbol, the entries it named with their sides",
+        s.check("the look's record: v 2, k score-forming, its day, the unread symbol, the entries it named with their sides",
                 looked is not None and (looked["v"], looked["k"], looked["day"], looked["symbols"], looked["unread"])
-                == (1, "score-forming", "1970-03-02", 3, ["BADUSDT"])
+                == (2, "score-forming", "1970-03-02", 3, ["BADUSDT"])
                 and looked["entries"] == [{"symbol": "BTCUSDT", "side": -1}, {"symbol": "AAAUSDT", "side": 1}]
                 and (looked["stopped"], looked["scaled"]) == ([], [])
                 and looked["ts"] == "1970-03-02T15:10:02Z")
@@ -3736,6 +3765,135 @@ def section_ab(s):
                     and book.live_bars("AAAUSDT", 61 * book.DAY_MS + AB_LOOK_MS) == (bars, 105.0))
         finally:
             book._get = saved_get
+        # A look TZ-80 wrote (v 1) named the plan's entries, not the book's: the close counts no look of it.
+        h = AbHost(os.path.join(tmp, "w"), {"AAAUSDT": long_world})
+        h.run(60)
+        os.makedirs(os.path.join(h.state, score.FORMING))
+        with open(os.path.join(h.state, score.FORMING, "1970-03-02.json"), "w", encoding="utf-8") as fh:
+            json.dump({"v": 1, "k": "score-forming", "day": "1970-03-02",
+                       "entries": [{"symbol": "AAAUSDT", "side": 1}]}, fh)
+        code, printed, alerts, ledger, record = h.run(61)
+        s.check("a look of TZ-80's record (v 1) is counted by no close", ab_field(printed, "look") == "-"
+                and record["look"] is None and ab_field(printed, "opened") == "1")
+        # The book held under the owner's ceilings (TZ-81): one a side and two in all.
+        dd = short_world + [(k * book.DAY_MS, 103.0, 104.0, 102.0, 103.0) for k in range(65, 105)]
+        h = AbHost(os.path.join(tmp, "q"), {"AAAUSDT": long_world, "BTCUSDT": long_world, "CCCUSDT": long_world,
+                                            "DDDUSDT": dd, "EEEUSDT": ab_later(long_world, 10),
+                                            "FFFUSDT": ab_later(long_world, 40)}, own=AB_TIGHT)
+        code, printed, alerts, ledger, record = h.run(61)
+        text = alerts[0][1] if alerts else ""
+        s.check("one a side and two in all: the baseline tells the major's long and the short in full, and names the "
+                "two longs left out on one line under them",
+                len(alerts) == 1
+                and [x.split("**")[1] for x in text.split("\n") if x.startswith((score.DOT[1], score.DOT[-1]))]
+                == [score.SIDE_HEAD[1] + " BTC", score.SIDE_HEAD[-1] + " DDD"]
+                and text.split("\n")[5] == score.T_OUT.format(items=score.SIDE[1] + " AAA, CCC")
+                and score.T_OPEN_NOW.format(n=2, nl=1, ns=1, r="+0.00") in text.split("\n")
+                and text.split("\n")[-2] == score.T_LIMIT.format(side_n=1, book_n=2, risk="150"))
+        s.check("its line: open=2 outside=2 opened=2 skipped=2; its record: the ceilings 1 and 2, the two held, the two "
+                "left out with their side and day, the plan's four open",
+                [ab_field(printed, f) for f in ("open", "outside", "opened", "skipped")] == ["2", "2", "2", "2"]
+                and record["ceilings"] == [1, 2] and [o["symbol"] for o in record["open"]] == ["BTCUSDT", "DDDUSDT"]
+                and record["outside"] == [{"symbol": "AAAUSDT", "state": "long", "entry_date": "1970-03-03"},
+                                          {"symbol": "CCCUSDT", "state": "long", "entry_date": "1970-03-03"}]
+                and record["plan"]["open"] == 4)
+        code, printed, alerts, ledger, record = h.run(63)
+        text = alerts[0][1] if alerts else ""
+        s.check("the short stopped inside its day is the book's trade, in its ledger as in the plan's; the long its stop "
+                "day opened finds the long side full: named left out with the ceilings, and no entry told",
+                h.ledger(score.HELD) == h.ledger(score.PLAN) is not None
+                and [x[0] for x in h.stamps(score.HELD)] == ["DDDUSDT-%d.json" % (61 * book.DAY_MS)]
+                and len(alerts) == 1 and text.split("\n")[1] == score.T_OUT.format(items=score.SIDE[1] + " DDD")
+                and text.split("\n")[-1] == score.T_LIMIT.format(side_n=1, book_n=2, risk="150")
+                and score.T_WHEN not in text and score.T_HOW not in text
+                and [ab_field(printed, f) for f in ("open", "outside", "opened", "skipped", "closed")]
+                == ["1", "3", "0", "1", "1"])
+        code, printed, alerts, ledger, record = h.run(69)
+        text = alerts[0][1] if alerts else ""
+        s.check("a target reached is told of the position held alone, not of the plan's two left out",
+                len(alerts) == 1
+                and text.split("\n")[1] == score.T_SCALED.format(sym="BTC", side=score.SIDE[1], px="113.8", stop="105")
+                and text.count(score.T_SCALED.split("{sym}")[0]) == 1 and ab_field(printed, "scaled") == "1")
+        code, printed, alerts, ledger, record = h.run(71)
+        text = alerts[0][1] if alerts else ""
+        s.check("a position past its target keeps its slot: the next long is left out",
+                ab_field(printed, "skipped") == "1" and len(alerts) == 1
+                and text.split("\n")[1] == score.T_OUT.format(items=score.SIDE[1] + " EEE")
+                and [o["symbol"] for o in record["open"]] == ["BTCUSDT"])
+        code, printed, alerts, ledger, record = h.run(101)
+        text = alerts[0][1] if alerts else ""
+        s.check("an exit at an open frees its slot for that open's entry: the long due is told beside the exit due",
+                (ab_field(printed, "opened"), ab_field(printed, "closing"), ab_field(printed, "skipped")) == ("1", "1", "0")
+                and score.T_ENTRY.format(dot=score.DOT[1], side=score.SIDE_HEAD[1], sym="FFF", entry="105", stop="100.6",
+                                         dist="\u22124.2") in text.split("\n")
+                and score.T_CLOSING.format(sym="BTC", side=score.SIDE[1]) in text.split("\n"))
+        code, printed, alerts, ledger, record = h.run(102)
+        text = alerts[0][1] if alerts else ""
+        s.check("the book held's ledger takes the trades it held, the plan's every entry: two files against four",
+                [x[0] for x in h.stamps(score.HELD)] == ["BTCUSDT-%d.json" % (61 * book.DAY_MS),
+                                                        "DDDUSDT-%d.json" % (61 * book.DAY_MS)]
+                and [x[0] for x in h.stamps(score.PLAN)] == ["%sUSDT-%d.json" % (c, 61 * book.DAY_MS)
+                                                             for c in ("AAA", "BTC", "CCC", "DDD")]
+                and record["closed"]["all"]["n"] == 2 and record["plan"]["closed"]["all"]["n"] == 4
+                and (ab_field(printed, "ledger"), ab_field(printed, "plan"), ab_field(printed, "closed")) == ("2", "4", "1"))
+        s.check("the close is told of the position held and of none left out, and the score is the book held's",
+                len(alerts) == 1 and text.count(score.T_CLOSED.split("{sym}")[0]) == 1 and text.split("\n")[1].startswith(
+                    score.T_CLOSED.split("{sym}")[0] + "BTC ")
+                and score.T_SCORE.split("{total}")[0].format(since="01.01.1970", n=2) in text)
+        h.own = AB_OWN
+        code, printed, alerts, ledger, record = h.run(103)
+        text = alerts[0][1] if alerts else ""
+        s.check("ceilings that change make the next run a baseline: the book re-read under them from GO_LIVE, the trades "
+                "they hold now written and none told",
+                text.split("\n")[0] == score.T_HEAD_BASE.format(d="13.04") and record["ceilings"] == [6, 10]
+                and [o["symbol"] for o in record["open"]] == ["DDDUSDT", "EEEUSDT", "FFFUSDT"] and record["outside"] == []
+                and (ab_field(printed, "ledger"), ab_field(printed, "closed")) == ("4", "0")
+                and score.T_CLOSED.split("{sym}")[0] not in text)
+        # Run every day, the close holds the book hold() holds over the same bars at once -- live and archive alike.
+        worlds = {"AAAUSDT": long_world, "BTCUSDT": long_world, "CCCUSDT": long_world, "DDDUSDT": dd,
+                  "EEEUSDT": ab_later(long_world, 10), "FFFUSDT": ab_later(long_world, 40)}
+        h = AbHost(os.path.join(tmp, "y"), worlds, own=AB_TIGHT)
+        for n in range(61, 105):
+            h.run(n)
+        whole = [sp for symbol, world in worlds.items()
+                 for sp in book.spans(symbol, *book.replay(world[:104], world[104][1], book.SCALE_R), 104 * book.DAY_MS)]
+        s.check("the close run every day holds the very spans hold() takes over all the days at once",
+                {(sp[0], sp[2]) for sp in h.record()["held"]} == book.hold(whole, book.rank(list(worlds)), 1, 2)
+                and len(h.record()["held"]) == 3)
+        # What a record decided stands: an entry left out stays out, a position held on an unread symbol keeps its slot.
+        h = AbHost(os.path.join(tmp, "x"), {"AAAUSDT": long_world, "BTCUSDT": long_world,
+                                            "EEEUSDT": ab_later(long_world, 10)}, own=AB_TIGHT)
+        h.run(61)
+        h.worlds["BTCUSDT"] = OSError("refused")
+        code, printed, alerts, ledger, record = h.run(71)
+        text = alerts[0][1] if alerts else ""
+        s.check("a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and "
+                "the record keeps the span",
+                record["unread"] == ["BTCUSDT"] and len(alerts) == 1
+                and text.split("\n")[1] == score.T_OUT.format(items=score.SIDE[1] + " EEE")
+                and ["BTCUSDT", 1, 61 * book.DAY_MS, None] in record["held"]
+                and [o["symbol"] for o in record["outside"]] == ["AAAUSDT", "EEEUSDT"])
+        h.worlds["BTCUSDT"] = [(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(105)]
+        code, printed, alerts, ledger, record = h.run(72)
+        s.check("an entry once left out is never taken: the long that held the slot gone from the replay, the two "
+                "left out stay out and nothing is told",
+                alerts == [] and record["open"] == [] and [o["symbol"] for o in record["outside"]] == ["AAAUSDT", "EEEUSDT"]
+                and record["held"] == [] and (ab_field(printed, "opened"), ab_field(printed, "skipped")) == ("0", "0"))
+        # The look tells the book held alone.
+        h = AbHost(os.path.join(tmp, "u"), {"AAAUSDT": long_world, "BTCUSDT": long_world}, own=AB_TIGHT)
+        h.run(60)
+        code, printed, alerts, looked = h.look(60, {"AAAUSDT": rising, "BTCUSDT": rising})
+        text = alerts[0][1] if alerts else ""
+        s.check("the look names the candidate the book would take, the major's long, and not the long it would leave out",
+                looked["entries"] == [{"symbol": "BTCUSDT", "side": 1}] and ab_field(printed, "entries") == "1"
+                and len(alerts) == 1
+                and text.split("\n")[1].startswith(score.F_ENTRY.format(side=score.SIDE[1], sym="BTC", last="103.5"))
+                and "AAA" not in text)
+        h.run(61)
+        code, printed, alerts, looked = h.look(61, {"AAAUSDT": (105.0, 107.0, 100.0, 101.0),
+                                                    "BTCUSDT": (105.0, 107.0, 104.0, 106.0)})
+        s.check("a stop the day has reached on a position the book left out is not the look's to tell",
+                code == 0 and alerts == [] and looked["stopped"] == [] and ab_field(printed, "stopped") == "0")
         # GO_LIVE cuts the ledger by the entry's day.
         score.GO_LIVE = "1970-03-04"
         h = AbHost(os.path.join(tmp, "g"), {"AAAUSDT": long_world})
@@ -3743,6 +3901,11 @@ def section_ab(s):
         code, printed, alerts, ledger, record = h.run(102)
         s.check("a trade entered before GO_LIVE is no file of the ledger",
                 code == 0 and ledger is None and record["closed"]["all"] == {"n": 0} and record["since"] == "1970-03-04")
+        h = AbHost(os.path.join(tmp, "r"), {"BTCUSDT": long_world, "EEEUSDT": ab_later(long_world, 10)}, own=AB_TIGHT)
+        code, printed, alerts, ledger, record = h.run(71)
+        s.check("a position entered before GO_LIVE holds no slot: it is named left out, and the long it would block is held",
+                [o["symbol"] for o in record["open"]] == ["EEEUSDT"]
+                and [o["symbol"] for o in record["outside"]] == ["BTCUSDT"])
     finally:
         score.GO_LIVE, score.FUNDING_PAGE = saved_live, saved_page
         shutil.rmtree(tmp, ignore_errors=True)
@@ -3791,6 +3954,62 @@ def section_ab(s):
                                                        sort_keys=True)))
     finally:
         book._get = saved_get
+    # The book held (TZ-81): one walk, hold(), live and over the archive alike.
+    d = book.DAY_MS
+    s.check("rank: the MAJORS first, then the others, each in the order given -- the list's",
+            book.rank(["AAAUSDT", "XRPUSDT", "BTCUSDT", "BBBUSDT", "ETHUSDT"])
+            == {"XRPUSDT": 0, "BTCUSDT": 1, "ETHUSDT": 2, "AAAUSDT": 3, "BBBUSDT": 4})
+    s.check("spans: a channel exit frees its slot at the open, a stop inside the day, a position that stands never, and "
+            "one whose exit is due at the next open",
+            book.spans("AUSDT", [{"side": 1, "t_entry": 5 * d, "t_exit": 9 * d, "why": "channel"},
+                                 {"side": -1, "t_entry": 2 * d, "t_exit": 4 * d, "why": "stop"}],
+                       {"side": 1, "t_entry": 10 * d}, 20 * d)
+            == [("AUSDT", 1, 5 * d, (9 * d, book.AT_OPEN)), ("AUSDT", -1, 2 * d, (4 * d, book.IN_DAY)),
+                ("AUSDT", 1, 10 * d, None)]
+            and book.spans("AUSDT", [], {"side": -1, "t_entry": 10 * d, "exit_due": True}, 20 * d)
+            == [("AUSDT", -1, 10 * d, (20 * d, book.AT_OPEN))]
+            and book.AT_OPEN < book.ENTRY < book.IN_DAY)
+    ranks = book.rank(["AUSDT", "BUSDT", "CUSDT", "BTCUSDT"])
+    longs = [(symbol, 1, 5 * d, None) for symbol in ("AUSDT", "BUSDT", "CUSDT", "BTCUSDT")]
+    s.check("hold: one open's entries are taken in rank order while their side has room -- the major's, then the list's",
+            book.hold(longs, ranks, 2, 10) == {("BTCUSDT", 5 * d), ("AUSDT", 5 * d)})
+    s.check("hold: the book's ceiling binds across the sides -- two longs leave no room for a short at two in all",
+            book.hold(longs[:2] + [("CUSDT", -1, 6 * d, None)], ranks, 6, 2) == {("AUSDT", 5 * d), ("BUSDT", 5 * d)})
+    s.check("hold: an exit at an open frees its slot for that open's entry",
+            book.hold([("AUSDT", 1, 5 * d, (8 * d, book.AT_OPEN)), ("BUSDT", 1, 8 * d, None)], ranks, 1, 10)
+            == {("AUSDT", 5 * d), ("BUSDT", 8 * d)})
+    s.check("hold: a stop frees its slot inside its day, after that open's entries -- the next open's entry is taken",
+            book.hold([("AUSDT", 1, 5 * d, (8 * d, book.IN_DAY)), ("BUSDT", 1, 8 * d, None), ("CUSDT", 1, 9 * d, None)],
+                      ranks, 1, 10) == {("AUSDT", 5 * d), ("CUSDT", 9 * d)})
+    s.check("hold: an entry stopped on its own day held its slot through that open",
+            book.hold([("BTCUSDT", 1, 5 * d, (5 * d, book.IN_DAY)), ("AUSDT", 1, 5 * d, None), ("BUSDT", 1, 6 * d, None)],
+                      ranks, 1, 10) == {("BTCUSDT", 5 * d), ("BUSDT", 6 * d)})
+    s.check("hold: an entry not taken at its own open is never taken, though a slot frees while it stands",
+            book.hold([("AUSDT", 1, 5 * d, (8 * d, book.AT_OPEN)), ("BUSDT", 1, 6 * d, None)], ranks, 1, 10)
+            == {("AUSDT", 5 * d)})
+    saved_blob, saved_series = book._archive_blob, book.archive_series
+    book._archive_blob = lambda path, cache: None
+    book.archive_series = lambda symbol, start, end, cache: (long_world, [])
+    try:
+        every, _ = book.archive(["AUSDT", "BTCUSDT"], book.date(1970, 1, 1), book.date(1970, 4, 15), "-",
+                                scale=book.SCALE_R)
+        held, table = book.archive(["AUSDT", "BTCUSDT"], book.date(1970, 1, 1), book.date(1970, 4, 15), "-",
+                                   scale=book.SCALE_R, ceilings=(1, 1))
+    finally:
+        book._archive_blob, book.archive_series = saved_blob, saved_series
+    s.check("the archive with ceilings keeps hold()'s trades: of two longs at one open, the major's alone",
+            [r[1] for r in every] == ["AUSDT", "BTCUSDT"] and [r[1] for r in held] == ["BTCUSDT"]
+            and table["all"]["n"] == 1 and held[0][4] == every[1][4])
+    codes = []
+    for argv in (["--live", "--hold", "6,10", "AUSDT"], ["--archive", "--hold", "6", "AUSDT"],
+                 ["--archive", "--hold", "0,10", "AUSDT"]):
+        try:
+            with contextlib.redirect_stderr(io.StringIO()):
+                book.main(argv)
+            codes.append(0)
+        except SystemExit as exc:
+            codes.append(exc.code)
+    s.check("--hold reads the archive alone, with two positive counts", codes == [2, 2, 2])
     s.check("the ceilings are paper.ceilings: 3 % and 5 % at 0.5 % hold 6 and 10", paper.ceilings(AB_OWN) == (6, 10))
     size = paper.copy_size(AB_OWN, 4.4 / 105.0)
     s.check("the size is paper.copy_size: 150 USDT over a stop 4.4 of 105 away is 3579.5 USDT, a third of it at 3x",
@@ -3807,7 +4026,7 @@ def section_ab(s):
             and "2x" in paper.copy_text(AB_OWN, 0.30, -1, [-1]) and "3x" in paper.copy_text(AB_OWN, 0.10, -1, [-1]))
     s.check("the default state is /var/lib/crypto-auto, the ledger score-ledger/ and the record score.json",
             common.STATE_DIR == "/var/lib/crypto-auto" and (score.LEDGER, score.RECORD) == ("score-ledger", "score.json")
-            and (score.PLAN, score.FORMING) == ("score-plan", "score-forming"))
+            and (score.PLAN, score.FORMING, score.HELD) == ("score-plan", "score-forming", "score-held"))
     # The units and the manifest.
     service, timer = unit_lines("crypto-score.service"), unit_lines("crypto-score.timer")
     s.check("service runs as User=cryptoauto, Group=cryptoauto",
```

---

## 11. The study of §1 — retained, not run by this TZ

`python3 study.py CACHE_DIR` from the repository root on §10's tree, `CACHE_DIR` the cache `book.py --archive` filled
with the 31 symbols' files of 2023-01 → 2026-10 — 56 lines, MD5 `4a134be2d6c88088c5330fbf2154d518`. Kept so that the next reader
reproduces §1's last column and its random orders instead of meeting a figure nobody can re-derive (inv. 71). No stage
of this TZ runs it.

```py
#!/usr/bin/env python3
"""TZ-81, section 1's study, retained (map inv. 71): the plan every entry and held under 6 a side and 10 in all, the
most it holds at once, and the held book under 200 random orders of the list. Production's own functions on
data.binance.vision's archive, read through book.py's cache. Run from the repository root:
python3 study.py CACHE_DIR."""
import random
import sys

sys.path.insert(0, "vps")
import book  # noqa: E402
import writer  # noqa: E402
from datetime import date, datetime, timezone  # noqa: E402

symbols = writer.payload_symbols(".")
oos = datetime(2025, 1, 1, tzinfo=timezone.utc).timestamp() * 1000
books, rows = [], []
for s in symbols:
    bars, funding = book.archive_series(s, date(2023, 1, 1), date(2026, 10, 31), sys.argv[1])
    trades, pos = book.replay(bars, scale=book.SCALE_R)
    books += book.spans(s, trades, pos)
    rows += [(tr["t_exit"], s, tr["side"], tr["t_entry"], book.result_r(tr, funding)) for tr in trades]
rows.sort()


def table(taken):
    out = []
    for name, keep in (("IS", lambda r: r[3] < oos), ("OOS", lambda r: r[3] >= oos)):
        part = book.summary([r[4] for r in rows if keep(r) and (taken is None or (r[1], r[3]) in taken)])
        out.append("%s %d trades %+.2f R drawdown %.2f R" % (name, part["n"], part["total"], part["maxdd"]))
    return " | ".join(out)


def most(taken):
    events = sorted([((t, book.ENTRY), 1) for s, _, t, _ in books if taken is None or (s, t) in taken]
                    + [(free, -1) for s, _, t, free in books if free is not None and (taken is None or (s, t) in taken)])
    level = peak = 0
    for _, step in events:
        level += step
        peak = max(peak, level)
    return peak


held = book.hold(books, book.rank(symbols), 6, 10)
print("every entry  %s | at once %d" % (table(None), most(None)))
print("held 6,10    %s | at once %d" % (table(held), most(held)))
totals = []
for seed in range(200):
    order = list(symbols)
    random.Random(seed).shuffle(order)
    taken = book.hold(books, {s: k for k, s in enumerate(order)}, 6, 10)
    totals.append([sum(r[4] for r in rows if (r[1], r[3]) in taken and keep(r))
                   for keep in (lambda r: r[3] < oos, lambda r: r[3] >= oos)])
for half, name in ((0, "IS"), (1, "OOS")):
    v = sorted(t[half] for t in totals)
    print("200 orders %-3s p5 %+.2f  median %+.2f  p95 %+.2f  below zero %d" % (name, v[10], v[100], v[189],
                                                                           sum(x < 0 for x in v)))
```

Its output on 15.11.2026:

```text
every entry  IS 229 trades +136.30 R drawdown 33.82 R | OOS 298 trades -9.09 R drawdown 43.03 R | at once 26
held 6,10    IS 115 trades +38.66 R drawdown 19.43 R | OOS 119 trades +28.10 R drawdown 26.34 R | at once 10
200 orders IS  p5 +38.70  median +44.16  p95 +50.24  below zero 0
200 orders OOS p5 +14.14  median +20.20  p95 +27.03  below zero 0
```
