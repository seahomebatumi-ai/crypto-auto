# Implementation Report — TZ-79

## Status
COMPLETED

## Inbound Filing
None. The TZ arrived at its canonical path `CryptoTZ/TZ-79-book-signal-and-ledger.md` (commit `6fc3650`, «Add files via upload»); nothing was moved or renamed.

## Scope Executed
**Class: branch TZ** — `## Scope` names six files outside `CryptoReports/**`.

Previous TZ: TZ-78 is merged — `git merge-base --is-ancestor f813ff9 origin/main` succeeded (`f813ff9 Merge pull request #64 from seahomebatumi-ai/claude/tz-78-paper-signal-alerts`), and every remote branch is 0 commits ahead of `origin/main`. Clone not shallow (`git rev-parse --is-shallow-repository` → `false`); tree clean at start.

Note: `origin/main` at execution was `6fc3650` (the TZ's own upload), one commit after the `10f926a` the TZ was written against; `git rev-parse origin/main:vps` → `de6f1c635811b3ee5b24456e8b534edd9c41764b`, the `vps` tree the TZ names.

Stages A–D executed in full, all on the VPS (`hostname` → `vultr`, root, Python 3.12.3, systemd 255).

## Files Created
- `vps/score.py`
- `vps/units/crypto-score.service`
- `vps/units/crypto-score.timer`

## Files Modified
- `vps/book.py` — `live_state()`; `main()`'s `--live` branch calls it
- `vps/selftest.py` — `import score`, section AB, its `SECTIONS` entry
- `vps/manifest` — line `crypto-score.timer`

## Files Renamed
None.

## Files Deleted
None.

## Implementation Summary
The patch of TZ-79 §10 was extracted by B1's command and applied with `git apply`, unmodified; no file was edited by hand. The six resulting files match B2's lines and MD5s exactly. Committed locally before stage C (B3), validated on the committed branch, then pushed.

**B1:**
```
awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-79-book-signal-and-ledger.md > /tmp/tz79.patch
→ 818 lines, MD5 fec59ef4597d7ac2aa372811533d0f95   (required: 818, fec59ef4597d7ac2aa372811533d0f95)
git apply /tmp/tz79.patch → exit 0
```

**B2:**

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `vps/book.py` | 304 | `4b64b856fb80cfa810dcac015eb60b20` | equal |
| `vps/manifest` | 10 | `73d8fd4022bcf24996d4d3c41c6444c5` | equal |
| `vps/score.py` | 317 | `308c8661b54d843a682747e46752bd4e` | equal |
| `vps/selftest.py` | 3553 | `4816f38d10aa2711cc56fff29203c7a7` | equal |
| `vps/units/crypto-score.service` | 20 | `ca1e8d926d9ce2d9e2f2eabb4d7db41d` | equal |
| `vps/units/crypto-score.timer` | 10 | `06850cd5a678a0807bed58dc855cb48d` | equal |

## Validation

**A1 — added files of the TZ's gate** (`grep -c ''` and `md5sum`, on `origin/main`):

| File | Lines | MD5 | Result |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | equal; version line `**Version 31.**` |
| `vps/book.py` | 297 | `8478a66a57ad4c48b2579e8cb0e382d9` | equal |
| `vps/selftest.py` | 3173 | `f79b05657550180ad9f18603cda5cec1` | equal |
| `vps/manifest` | 9 | `75a0f5a71f6111ecca0553620f1eea4c` | equal |
| `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` | equal (reported) |
| `vps/writer.py` | 154 | `c07b1f71ef014e18448eb9313e185b73` | equal (reported) |

**A2 / V3 — selftest per section** (`python3 vps/selftest.py`; A2 exit 0, V3 exit 0, V3 stderr 0 bytes):

| Section | A2 (`main`, `6fc3650`) | V3 (branch, `a1ac59d`) |
|---|---|---|
| A | checks 32 failed 0 | checks 32 failed 0 |
| B | checks 12 failed 0 | checks 12 failed 0 |
| C | checks 4 failed 0 | checks 4 failed 0 |
| D | checks 13 failed 0 | checks 13 failed 0 |
| E | checks 12 failed 0 | checks 12 failed 0 |
| F | checks 14 failed 0 | checks 14 failed 0 |
| G | checks 8 failed 0 | checks 8 failed 0 |
| H | checks 2 failed 0 | checks 2 failed 0 |
| I | checks 4 failed 0 | checks 4 failed 0 |
| J | checks 26 failed 0 | checks 26 failed 0 |
| K | checks 2 failed 0 | checks 2 failed 0 |
| L | checks 4 failed 0 | checks 4 failed 0 |
| M | checks 19 failed 0 | checks 19 failed 0 |
| N | checks 10 failed 0 | checks 10 failed 0 |
| O | checks 33 failed 0 | checks 33 failed 0 |
| P | checks 21 failed 0 | checks 21 failed 0 |
| Q | checks 3 failed 0 | checks 3 failed 0 |
| R | checks 9 failed 0 | checks 9 failed 0 |
| S | checks 35 failed 0 | checks 35 failed 0 |
| T | checks 39 failed 0 | checks 39 failed 0 |
| U | checks 18 failed 0 | checks 18 failed 0 |
| V | checks 16 failed 0 | checks 16 failed 0 |
| W | checks 204 failed 0 | checks 204 failed 0 |
| X | checks 19 failed 0 | checks 19 failed 0 |
| Y | checks 54 failed 0 | checks 54 failed 0 |
| Z | checks 23 failed 0 | checks 23 failed 0 |
| AA | checks 26 failed 0 | checks 26 failed 0 |
| AB | — | checks 62 failed 0 |
| **total** | `selftest: sections 27 checks 662 failed 0 empty 0` | `selftest: sections 28 checks 724 failed 0 empty 0` |

Every one of the 27 sections of `main` is unchanged; AB adds 62 → 724 (= A2's 662 + 62).

**A3** (kept for V7): `systemctl list-unit-files 'crypto-score*' --no-legend` → empty; `ls /var/lib/crypto-auto` →
```
announcements.jsonl
bot-counters.json
bot-offset
deployed-vps-tree
etf.json
exchange-snapshot.json
list-generation.json
perpetuals.json
runs-enabled
```

**V1.** `python3 -m py_compile vps/book.py vps/score.py vps/selftest.py` → exit 0 (the `__pycache__` it produced was removed).

**V2.** B2's six files as above; the Cyrillic count command prints `0`.

**V3.** See the table: exit 0, `selftest: sections 28 checks 724 failed 0 empty 0`, `section AB: checks 62 failed 0`, `section X: checks 19 failed 0`.

**V4 — negative controls.** Extraction command of §6 V4 → `/tmp/tz79-controls.py`, 60 lines, MD5 `a62c97667bf6cc10523e47d678c539fb` (required equal). `python3 /tmp/tz79-controls.py` → exit 0, output 47 lines, MD5 `c5e9c76e981749cadb25781b930c8cde` (required equal). Output verbatim:

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

Afterwards `git status --porcelain` printed nothing.

**V5 — the exchange, read once from this machine.** Run moment `date -u` → `Thu Nov 12 09:42:12 PM UTC 2026`. Commands, as root, exactly as §6 V5:

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

Run 1, every line printed (exit 0):
```
Running as unit: run-u5994.service
score: asof=2026-11-11 symbols=31 read=31 unread=0 open=12 opened=1 closing=0 closed=0 pending=0 late=0 disagree=0 ledger=3 alert=yes
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 10.996s
CPU time consumed: 275ms
Memory peak: 1004.0K
Memory swap peak: 0B
```

Shape checks, run 1:
- exit 0; last `score:` line has `symbols=31`, `read=31` (≥ 1), `asof=2026-11-11` (the UTC day before the run), `alert=yes` — pass.
- scratch outbox: exactly one file, `1794519743753-alert-1321404.json`, `"kind":"alert"`; first line ends with `11.11` → `True`; carries «СДЕЛКИ ПРАВИЛА — подключено» → `True` — pass.
- `state/score.json` parses; `stat -c '%a'` → `640`; `k` `score`, `since` `2026-10-21`, `symbols` 31, `v` 1, `ts` `2026-11-12T21:42:12Z` — pass.
- `state/score-ledger`: 3 files = `ledger=3`, each parsing to the ten keys of §3 in order (`True` ×3) — pass:
  - `LITUSDT-1793318400000.json` — short, `stop`, r −1.003
  - `TRXUSDT-1793318400000.json` — long, `stop`, r −1.070
  - `TRXUSDT-1793491200000.json` — short, `stop`, r −1.035
- record: `unread` `[]`, `pending` 0, `late` 0, `disagree` 0; `closed.all` = `{"n": 3, "win": 0.0, "mean": -1.035868009769178, "total": -3.1076040293075335, "pf": 0.0, "maxdd": 3.107604029307533}`, `closed.majors` = `{"n": 0}`, `closed.others` = equal to `all`.

The alert's text in full (decoded from the outbox file):

```text
📈 **СДЕЛКИ ПРАВИЛА — подключено** · закрытие дня 11.11
🔴 **Правило открыло шорт:** UNI · вход `6.229` · стоп `7.382` (+18.5%)
📊 Счёт с 21.10.2026: закрыто **3** · **−3.11 R** · в плюсе 0
BTC ETH SOL BNB XRP: 0 · +0.00 R · остальные: 3 · −3.11 R
В сделке 12: лонг 0 · шорт 12 · по закрытию дня +5.29 R
Монеты: 🔴 YFI · 🔴 FET · 🔴 GRAM · 🔴 XRP · 🔴 ADA · 🔴 SOL · 🔴 HYPE · 🔴 ETH · 🔴 HBAR · 🔴 XLM · 🔴 ZEC · 🔴 UNI
R — один риск на сделку.
Размер и плечо — кнопкой анализа.
```

Run 2 (same command), every line printed (exit 0):
```
Running as unit: run-u5995.service; invocation ID: 9a8513e0b6b447efbb0e49ad85d15613
score: asof=2026-11-11 symbols=31 read=31 unread=0 open=12 opened=0 closing=0 closed=0 pending=0 late=0 disagree=0 ledger=3 alert=no
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 9.676s
CPU time consumed: 277ms
Memory peak: 312.0K
Memory swap peak: 0B
```

Shape checks, run 2: `opened=0 closing=0 closed=0 alert=no` — pass; `ls outbox | wc -l` → `1` (no second file) — pass; `ls -li --time-style=full-iso` of the ledger directory before and after run 2, `diff` → no difference — pass. The listing:
```
total 12
2085349 -rw-r----- 1 cryptoauto cryptoauto 190 2026-11-12 21:42:23.753341135 +0000 LITUSDT-1793318400000.json
2085347 -rw-r----- 1 cryptoauto cryptoauto 192 2026-11-12 21:42:23.751341111 +0000 TRXUSDT-1793318400000.json
2085348 -rw-r----- 1 cryptoauto cryptoauto 215 2026-11-12 21:42:23.752341123 +0000 TRXUSDT-1793491200000.json
```

`pending` was 0, so the conditional `curl` probe was not required and was not run.

Cleanup: `rm -r /var/lib/crypto-auto/tz79`; `systemctl list-units --all --no-legend 'run-*'` lists only pre-existing `run-credentials-*`, `run-docker-netns-*` and `run-user-0` mounts — no `run-u5994.service`, no `run-u5995.service`, no unit of this session.

**V6.** `git diff --numstat origin/main...HEAD`:
```text
10	3	vps/book.py
1	0	vps/manifest
317	0	vps/score.py
382	2	vps/selftest.py
20	0	vps/units/crypto-score.service
10	0	vps/units/crypto-score.timer
```
Exactly the six required lines.

**V7.** A3's two commands again: `systemctl list-unit-files 'crypto-score*' --no-legend` → empty; `ls /var/lib/crypto-auto` → the same nine entries; `diff` against A3 → identical for both. No `score.json`, no `score-ledger`.

**V8.** `systemd-analyze verify vps/units/crypto-score.service vps/units/crypto-score.timer` → exit 0, no output. `systemd-analyze verify vps/units/*` → exit 0, no output.

**V9.** `index.html` and `main.py` untouched (V6), so the standing checks do not apply. No step of the hosted gate runs `vps/selftest.py`: `grep -rn selftest .github/workflows/` finds only `backtest_bench.py --selftest`/`--lab-selftest` (`backtest_bench.yml`), `live-gate.sh --selftest` (`bench.yml`), `exhaustion_calib.py --selftest` (`calib.yml`), and the `bench.yml` comment at line 45 stating that the VPS selftest, not this gate, is the control. The deployer runs `vps/selftest.py` before it installs.

## Test Results
- V1 pass · V2 pass · V3 pass (724/724) · V4 pass (output MD5 equal) · V5 pass (both runs, all shapes) · V6 pass · V7 pass · V8 pass · V9 as stated.
- Hosted: see `## CI Execution`.

## Deviations
None.

## Pre-existing Issues
None found.

## Remaining Risks
- The ledger lives only on the VPS (`/var/lib/crypto-auto/score-ledger`) in this TZ, as the TZ states; it is not in the repository until step 2 of the build order.
- V5 read the exchange once at 21:42 UTC on 12.11; the first scheduled run after the merge (00:10 UTC) is the baseline the owner receives, and its content will differ from the V5 alert quoted above by whatever the book does at the next close.
- `closed.majors` with no trade is `{"n": 0}` — `book.summary()` of an empty list carries no `total`; `compose()` reads it with `.get("total", 0.0)`, so the alert prints `+0.00 R`. Recorded as observed, not a defect.

## Commit
Implementation (branch `claude/tz-79-book-signal-and-ledger`, pushed): `a1ac59d9ecaa0cc0e7140440f2414d377c55a02a`
```
TZ-79: vps — the book's signal and its forward ledger: every entry and exit the trend book makes on the list reaches the owner after the daily close, with no model, and every trade it closes is scored once
```
Contents: the six files of `## Files Created` / `## Files Modified`.

Report (direct to `main`, `CryptoReports/**` path): message `TZ-79: report — the book's signal and its ledger`; contents: this file.

## Pull Request
https://github.com/seahomebatumi-ai/crypto-auto/pull/65 — `TZ-79: vps — the book's signal and its forward ledger`, base `main`, head `claude/tz-79-book-signal-and-ledger`.

## CI Execution
Read with `gh run list --branch claude/tz-79-book-signal-and-ledger`:
- `Bench gate` (`bench.yml`), event `push`, run `43312994620` — completed, **success** (56s).
- `Bench gate` (`bench.yml`), event `pull_request`, run `43313006031` — completed, **success** (55s).

`main.yml` did not run and is not expected to: its `push` trigger is a `paths` allow-list of `main.py` and `.github/workflows/main.yml`, neither touched. Neither run executes `vps/selftest.py` (V9); that check was run on the VPS (V3, V4).

## Final Repository State
Branch `claude/tz-79-book-signal-and-ledger` pushed at `a1ac59d9ecaa0cc0e7140440f2414d377c55a02a`, one commit ahead of `origin/main` (`6fc3650`), working tree clean. Pull request #65 open.

**NOT IN EFFECT UNTIL MERGED.** On the VPS: no `crypto-score*` unit file, no scratch directory, no transient unit of this session (V5 cleanup, V7).

## Fingerprints
Map `SYSTEM-MAP-CRYPTOCALCUL.md`: **2805 lines, MD5 `7f699795a4ef996a15861167bbcae2d7`**, revision string `**Revision 2026-11-12-a.**` (required: equal).

Anchors — cut by structure from the map's own table (`awk` on the rows between the `| Anchor | Exact string …` header's separator line and the table's end): **table rows 7, compared 7**. Each matched with `grep -oF -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md`, returned text shown; each TZ header row matched verbatim (`grep -cF` → 1):

| # | Anchor | `grep -oF` returned |
|---|---|---|
| 1 | revision | `**Revision 2026-11-12-a.**` |
| 2 | direction engine | `### 3.12 Direction engine — veto cascade` |
| 3 | catalyst registry | `### 3.15 Catalyst registry` |
| 4 | exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| 5 | analytical engine | `## 11. Analytical engine` |
| 6 | squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| 7 | newest invariant | `73. **An Architect-owned document never grows` |

Files of the map's `## 0` table (on `origin/main` `6fc3650`):

| File | Lines | MD5 | vs. map |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

Files the TZ's gate adds: see A1 under `## Validation` — all six equal.
