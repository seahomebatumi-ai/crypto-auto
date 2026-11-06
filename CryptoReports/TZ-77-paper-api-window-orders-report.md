# Implementation Report — TZ-77

## Status

**COMPLETED.** Stages A–D executed on the VPS (`hostname` → `vultr`). Every validation item V1–V10 met its required
result. V6, this TZ's gate, printed `v6: symbols 54 differing 0` and exited 0, so the branch was pushed and a pull
request opened.

The previous TZ's branch was merged: `f3bd75a` (`Merge pull request #62 from
seahomebatumi-ai/claude/tz-76-paper-absence-margin`) is an ancestor of `origin/main`
(`git merge-base --is-ancestor f3bd75a origin/main` → exit 0). No remote branch is ahead of `origin/main`: a loop
over all 67 remote branches with `git rev-list --count origin/main..<branch>` printed none.

## Inbound Filing

None. The Boss's upload `e8463bd` (`Add files via upload`) added `CryptoTZ/TZ-77-paper-api-window-orders.md` at the
canonical path its header states (1564 lines, MD5 `b56f51f396218daa7cb51766f26a5407`). No other copy exists in the
root or on any branch, so nothing was moved.

## Scope Executed

**Class: branch TZ** (contract §8). `## Scope` names two written files outside `CryptoReports/**`: `vps/paper.py` and
`vps/selftest.py`.

- Stage A: readings only. A0 is contract §4a steps 1–6 and the §5 gate; A1 is the four added files; A2 is the
  baseline selftest on `main`; A3 reads the live service.
- Stage B: branch `claude/tz-77-paper-api-window-orders` cut from `origin/main` (`e8463bd`). The §10 patch was
  extracted with the TZ's own `awk` command and applied with `git apply`. The result was committed locally before
  stage C.
- Stage C: V1–V10 run on the VPS against the committed branch.
- Stage D: branch pushed, pull request #63 opened, this report.
- On the VPS: two transient units were started from the branch's clone, `run-u5738.service` (V5) and
  `run-u5739.service` (V6). Both were collected on exit. No unit, timer or file under `/etc` or `/var/lib/cryptopaper`
  was created, changed or restarted.

## Files Created

None in the repository besides this report.

## Files Modified

- `vps/paper.py`: 1413 → 1785 lines, MD5 `dd4bab0209f99e1da430c87042a92b9c` → `2d814305c3e2883c79dbcf1c6fa14068`.
- `vps/selftest.py`: 2627 → 3063 lines, MD5 `76e814ccbe18551a8f47d6f7eae09669` → `505efb7dc01c40dd09c9c9008e49345b`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

The change is the Architect's §10 patch applied byte-exact. Nothing was hand-edited. The patch implements §3 and nothing
else:

- **A (the archive's missing day).**
  - `fapi_klines()` reads `fapi.binance.com/fapi/v1/klines` for one symbol-day, in the archive's column order. No
    klines, or HTTP 400, is `Absent`; any other failure is `Transport`.
  - `Inputs` takes a `fallback`. With one, an `Absent` 1m or 1d archive day is read from the API instead, and the
    symbol-day is kept in `<state>/api-days.json`.
  - `book_episode()` names the days it read from the API (`api`).
  - `produce_rebooks()` books again, once, every written line whose `unbookable` names `/daily/klines/…`. The new
    lines go into `rebook/<day>.jsonl`.
  - `book_lines()` substitutes those lines for the funding and the verdict. Funding waits for a day with a rebook
    still pending.
  - The service builds `Inputs` with `fallback=fapi_klines`.
- **B (the window).**
  - `window_view()` returns the window as it stands.
  - `at_window_end()` decides at thirteen weeks. The window closes when the pick episodes seen, less those unbookable
    for good, reach `EPISODES_MIN`. Otherwise it runs on to `follow_from + RUN_ON_MAX_DAYS` (182 days), with the
    `N_RUN_ON` notice.
  - While it runs on, `fix_end()` fixes the end on `follow_from`'s daily grid once the written book holds
    `EPISODES_MIN` pick episodes booked at `READABLE_AT_S` (1 800 s). This sends the `N_END_SET` notice.
  - `_apply()` no longer passes a fill at or after the end as it stands.
  - `verdict.json` records `window`, `rebooked` and `api`. A window that ran on closes with `N_CLOSED_RUN_ON`.
- **C (the orders, deciding nothing).**
  - `FILL_KEYS` adds `oid`, and episodes carry `oid_open` and `oid_close`.
  - `produce_orders()` writes `orders/<day>.jsonl`. `book_episode()` adds `x` for closed, uncut pick episodes.
  - `produce_readout()` writes `orders-readout.json` once, after the verdict and the window's last orders file.
- **D (the probe).** The klines steps read two days back. New `api` and `orders` steps.
- **Selftest.** W18 (`section_w_api`), W19 (`section_w_window`) and W20 (`section_w_orders`) are added, with their
  three calls at the end of `section_w`. No existing line changes (V7: 0 lines removed).

## Validation

### A0 — contract §4a steps 1–6 and the §5 gate

- `git fetch --all --prune`; `git rev-parse --is-shallow-repository` → `false`. `git status --porcelain` printed
  nothing. `HEAD` = `origin/main` = `e8463bd34cd20c420c07d1b6b07b7728aafa58e9`.
- The anchor table was cut by structure: every row after the separator line that follows the `| Anchor |` header,
  up to the first non-table line.
  - Command: `awk '/^\| Anchor \|/{h=1;next} h&&/^\|---/{f=1;h=0;next} f&&!/^\|/{exit} f'`, applied to the map's
    `## 0` block and to the TZ.
  - **Map table rows: 7. Rows compared: 7.** `diff` of the two cuts was empty: the TZ header quotes every row of the
    map's table, character for character.
  - Per-anchor results are under `## Fingerprints`.

### A1 — the four added files

All four are equal to the TZ's table (see `## Fingerprints`). `EXECUTOR-INSTRUCTIONS.md` line 3 reads
`**Version 31.**`, and `vps/units/crypto-paper.service` line 26 reads `MemoryMax=128M`.

### A2 — baseline on `main` (`e8463bd`, whose `vps/` is identical to `c03f428`'s)

`python3 vps/selftest.py` → exit 0, `selftest: sections 27 checks 592 failed 0 empty 0`, `section W: checks 134
failed 0`, equal to the TZ's figures. The per-section counts are in the table under `## Test Results`.

### A3 — the live service

```
$ systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service
MainPID=3360383
ActiveEnterTimestamp=Fri 2026-10-30 00:29:35 UTC
```

### B1 — the patch

```
$ awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-77-paper-api-window-orders.md > /tmp/tz77.patch
patch lines 1195 md5 1cc2ffdb1ae1f90ef6fa6120a645305d
```

The patch is equal to the TZ's figures as written.

### B2 — `git apply /tmp/tz77.patch`

`git apply --check` exited 0, then `git apply` exited 0. The resulting files:

```
vps/paper.py 1785 2d814305c3e2883c79dbcf1c6fa14068
vps/selftest.py 3063 505efb7dc01c40dd09c9c9008e49345b
```

Both are equal to the required lines and MD5s.

### B3

The implementation commit `1934bcb` was made locally before stage C, and pushed only after V6 passed.

### V1–V10

| # | Command / reading | Result | Required | Verdict |
|---|---|---|---|---|
| V1 | `python3 -m py_compile vps/paper.py vps/selftest.py` | exit 0 | exit 0 | met |
| V2 | `wc -l`, `md5sum` | `vps/paper.py` 1785 `2d814305c3e2883c79dbcf1c6fa14068`; `vps/selftest.py` 3063 `505efb7dc01c40dd09c9c9008e49345b` | B2's | met |
| V3 | `python3 vps/selftest.py` on the branch, on the VPS | exit 0; `selftest: sections 27 checks 643 failed 0 empty 0`; `section W: checks 185 failed 0`; the other 26 sections equal to A2 | 643 / W 185 / others equal | met |
| V4 | `>=` → `>` in `at_window_end`, selftest, `git checkout -- vps/paper.py` | exit 1; one `FAIL` line (below); `selftest: sections 27 checks 643 failed 1 empty 0`; then `git status --porcelain` printed nothing | as stated | met |
| V5 | `--probe` as a transient unit | exit 0; ten steps, none `failed (…)`; `api` and `orders` lines as required (below) | as stated | met |
| V6 | §9's script as a transient unit | exit 0; `v6: symbols 54 differing 0`; 54 ≥ 54 | N ≥ 54, 0 differing, exit 0 | met |
| V7 | `git diff --numstat origin/main...HEAD` | `416⇥44⇥vps/paper.py`, `436⇥0⇥vps/selftest.py` (tabs confirmed with `cat -A`) | exactly those two lines | met |
| V8 | `systemctl list-units --all 'run-*'` after V5–V6 | no `run-u5738` or `run-u5739` unit listed (a filter on both names printed 0 lines) | none of the session's left | met |
| V9 | `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service` | `MainPID=3360383`, `ActiveEnterTimestamp=Fri 2026-10-30 00:29:35 UTC`; `diff` against A3 empty | equal to A3 | met |
| V10 | `bench.yml` and runner | `index.html` and `main.py` are untouched (V7), so the standing checks do not apply. `bench.yml` has no step naming `vps/`, so `vps/**` is outside the hosted gate. The runs on the branch are under `## CI Execution` | report | met |

**V4 — the one `FAIL` line, verbatim:**

```
FAIL section W: thirteen weeks that can still make the verdict: the window closes at them, as the selection has it
```

Before the mutation, `grep -c '^    if seen - final >= EPISODES_MIN:$' vps/paper.py` → `1`. After it, `git diff
--numstat` → `1	1	vps/paper.py`. After the restore, `md5sum vps/paper.py` → `2d814305c3e2883c79dbcf1c6fa14068`.

**V5 — the command and its eleven lines** (started 11:24:20 UTC on 06.11.2026):

```
$ systemd-run --wait --pipe --collect -p MemoryMax=128M -p Nice=5 /usr/bin/python3 /root/crypto-auto/.claude/worktrees/bridge-cse_01KgRjgxjqnFxwjWKkuPkCH6/vps/paper.py --probe
paper: probe leaderboard rows=48256 pool=4135 bad=0
paper: probe portfolio blocks=11 drawdown=0.1793019000590501 eligible=True r12=True ret52=1.8346584175626885 sharpe=0.3921895617034479 turnover=1.2643955247171668 value_t0=719428.170206
paper: probe exchange perpetuals=522
paper: probe leverage positions=1
paper: probe fills fills=13695 first=2026-08-07T01:39:56Z
paper: probe klines_1m rows=1440
paper: probe klines_1d rows=1
paper: probe funding rows=93
paper: probe api BTCUSDT 2026-11-04 archive=1440 api=1440 equal=1440 close=equal
paper: probe orders rows=1813
paper: probe peak_rss_kib=41652
exit 0
```

systemd's stderr: `Running as unit: run-u5738.service`, `Finished with result: success`, `Main processes terminated
with: code=exited/status=0`, `Service runtime: 1min 11.263s`, `Memory peak: 944.0K`. `peak_rss_kib=41652` is
reported, as the TZ asks; nothing is required of it.

**V6 — the command and every line it printed.** The script was extracted with
`awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-77-paper-api-window-orders.md > /tmp/tz77-v6.py`
→ 20 lines, MD5 `a0b32dbad9666123cfaeca2bc66cbff6`, equal to the TZ's figures as written.

The book on the branch's tree was `main`'s at `e8463bd`, with no paper commit after `c03f428`. Before the run,
`git fetch origin main` confirmed `origin/main` was still `e8463bd`. A count with `paper.awaits_rebook()` over that
book read 320 lines across 54 symbols. Per day, the lines awaiting a rebook were: 27.10 2, 28.10 32, 29.10 32,
30.10 44, 31.10 22, 01.11 24, 02.11 41, 03.11 41, 04.11 82.

The run started at 11:25:55 UTC and finished at 11:29:19 UTC.

```
$ systemd-run --wait --pipe --collect -p MemoryMax=128M -p WorkingDirectory=/root/crypto-auto/.claude/worktrees/bridge-cse_01KgRjgxjqnFxwjWKkuPkCH6 /usr/bin/python3 /tmp/tz77-v6.py
targets 54
1000PEPEUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0050307
ADAUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.20590
AEROUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.6974000
ARBUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.172080
AVAXUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=9.0010
AZTECUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0170100
BCHUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=288.91
BNBUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=760.140
BTCUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=81308.80
CCUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.1003600
CRVUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.337400
DOGEUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.079730
DOTUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=1.010900
ENAUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.2096500
ETHUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=2358.55
FARTCOINUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.1335000
FETUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.1842000
FILUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.914300
GRAMUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=1.240000
GRASSUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.6822000
HBARUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.07492
HYPEUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=80.64800
INITUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.2231000
INJUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=8.149000
JUPUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.2818000
LINKUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=11.814
LITUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=2.935700
LTCUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=59.20
MEGAUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0504500
MONUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0213200
MORPHOUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=2.2507000
NEARUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=4.7330
ONDOUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.4218000
PAXGUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=4053.4400
PENDLEUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=1.9923000
PENGUUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0079480
PONSUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.2903000
PUMPUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0045350
SOLUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=102.3800
STRKUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0470200
SUIUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.942900
TAOUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=257.38
TIAUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.5533000
TRUMPUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=1.728000
TRXUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.32960
UNIUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=7.2480
USELESSUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.1693000
VIRTUALUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.6265000
WLDUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.4377000
XMRUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=598.84
XPLUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=0.0767700
XRPUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=1.3255
ZECUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=1310.46
ZROUSDT 2026-10-27 archive=1440 api=1440 equal=1440 close=equal | 2026-10-28 api=1440 close=1.6983000
v6: symbols 54 differing 0
exit 0
```

systemd's stderr: `Running as unit: run-u5739.service`, `Finished with result: success`, `Main processes terminated
with: code=exited/status=0`, `Service runtime: 3min 24.303s`, `Memory peak: 708.0K`.

The run made 216 requests to `fapi.binance.com` (54 symbols × 1m and 1d × 27.10 and 28.10), weight 10 each per the
TZ's §1 (0), over 3 min 24 s. None was refused.

## Test Results

A2 (`main`, `e8463bd`) against V3 (the branch, `1934bcb`), per section, both on the VPS:

| Section | A2 checks | A2 failed | V3 checks | V3 failed |
|---|---:|---:|---:|---:|
| A | 32 | 0 | 32 | 0 |
| B | 12 | 0 | 12 | 0 |
| C | 4 | 0 | 4 | 0 |
| D | 13 | 0 | 13 | 0 |
| E | 12 | 0 | 12 | 0 |
| F | 14 | 0 | 14 | 0 |
| G | 8 | 0 | 8 | 0 |
| H | 2 | 0 | 2 | 0 |
| I | 4 | 0 | 4 | 0 |
| J | 26 | 0 | 26 | 0 |
| K | 2 | 0 | 2 | 0 |
| L | 4 | 0 | 4 | 0 |
| M | 19 | 0 | 19 | 0 |
| N | 10 | 0 | 10 | 0 |
| O | 33 | 0 | 33 | 0 |
| P | 21 | 0 | 21 | 0 |
| Q | 3 | 0 | 3 | 0 |
| R | 9 | 0 | 9 | 0 |
| S | 35 | 0 | 35 | 0 |
| T | 39 | 0 | 39 | 0 |
| U | 18 | 0 | 18 | 0 |
| V | 16 | 0 | 16 | 0 |
| W | 134 | 0 | 185 | 0 |
| X | 19 | 0 | 19 | 0 |
| Y | 54 | 0 | 54 | 0 |
| Z | 23 | 0 | 23 | 0 |
| AA | 26 | 0 | 26 | 0 |
| **total** | **592** | **0** | **643** | **0** |

A2: `selftest: sections 27 checks 592 failed 0 empty 0`. V3: `selftest: sections 27 checks 643 failed 0 empty 0`. W
grew by exactly 51 (134 → 185). The other 26 sections, 458 checks, are unchanged. No `FAIL` line in either run
(`grep -c FAIL` → `0`, `0`).

## Deviations

- **Commit message trailer.** Both commits carry the TZ's `## Commit Message` string verbatim as their subject line,
  followed by one `Co-Authored-By:` trailer. This is the form TZ-76's commits `62a99eb` and `0d0030f` carry on
  `main`.
- No other deviation.

## Pre-existing Issues

- **The TZ header's base commit and map revision do not belong together.** The header reads «Written against:
  contract v31, map `2026-11-06-c`, and `main` at `c03f428`». At `c03f428` the map carries `**Revision
  2026-11-06-b.**` (`git show c03f428:SYSTEM-MAP-CRYPTOCALCUL.md | grep -m1 -E '^\*\*Revision'`). Revision `-c`
  arrived one commit later, at `984f6bf` (`Update SYSTEM-MAP-CRYPTOCALCUL.md`), followed by the TZ upload at
  `e8463bd`.
  - It did not affect execution. The enforced gate runs against `origin/main` (`e8463bd`), whose map carries `-c`.
  - `git diff --quiet c03f428 e8463bd -- vps/` exited 0, so every file the patch and the gate read is identical at
    both commits.
  - No paper record was added between them, so V6's targets are those «at `c03f428`».
  - Reported for the Architect; nothing acted on.
- **V8's glob matches more than transient services.** `systemctl list-units --all 'run-*'` also lists the mount
  units `run-credentials-crypto\x2d{announce,bot,etf,paper,run}.service.mount`, six
  `run-credentials-systemd\x2d….mount`, `run-docker-netns-d239c2286cab.mount` and `run-user-0.mount`. These belong
  to the installed services and the system, not to this session. Neither of the session's units (`run-u5738.service`,
  `run-u5739.service`) is listed. The check is met, but a reader of the raw listing has to filter it by name.

## Remaining Risks

- **The first pass after the merge does the rebook in one go.** The 320 lines across 54 symbols are rebooked on the
  first hourly pass after the deployer installs the merge. Its 1m and 1d reads of 28.10 from `fapi.binance.com` pass
  through no limiter in `paper.py`: `fapi_klines()` spends no `Limiter` weight. They share the VPS's address with
  `vps/book.py` and `vps/exchange.py`.
  - V6 made the same 216 requests in 3 min 24 s with none refused, and the rebook needs at most the 108 for 28.10.
  - This is a measurement of 06.11.2026, not a guarantee.
  - A refusal is `Transport`, which ends that pass's rebook and retries it at the next (§3 A1, inv. 70).
- **The API's answer is measured, not frozen.** The rebook books from whatever `fapi.binance.com` answers when it runs. V6
  measured that answer equal to the archive on 27.10 for every target symbol, and recorded the 28.10 rows and closes
  above. It cannot measure a later answer.
- **Nothing is in effect yet.** The running paper test (`MainPID=3360383`, active since 30.10.2026 00:29:35 UTC)
  still runs TZ-76's code. A–C take effect only when the deployer installs the merge.

## Commit

- Implementation: `1934bcb6efbd0390efdf2283a180e58cfecba400`, on `claude/tz-77-paper-api-window-orders`, pushed.
  - Message: `TZ-77: vps — the paper test books the archive's missing day from the exchange's own klines, runs its
    window on past thirteen weeks only when they cannot make the verdict, and records the picks' orders`, plus the
    trailer under `## Deviations`.
  - Contents: `vps/paper.py` (+416 −44), `vps/selftest.py` (+436 −0).
- Report: message `TZ-77: report — the paper test's missing day, window and orders`, plus the same trailer.
  Contents: this file, direct to `main` on the `CryptoReports/**` path (§8).

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/63, titled `TZ-77: paper — the archive's missing day from the
API, the window run on to the thirtieth pick episode, the picks' orders recorded`. Base `main`, head
`claude/tz-77-paper-api-window-orders`. Its body names this TZ.

## CI Execution

Read from the runner with `gh run list --branch claude/tz-77-paper-api-window-orders`, after both runs completed:

| Run id | Workflow | Event | Head | Conclusion |
|---|---|---|---|---|
| 42210671821 | Bench gate (`bench.yml`) | push | `1934bcb` | success |
| 42210732897 | Bench gate (`bench.yml`) | pull_request | `1934bcb` | success |

No other workflow ran on the branch:
- `main.yml`'s `push` filter is a `paths` allow-list of `main.py` and `.github/workflows/main.yml`, on `main` only.
- `calib.yml`'s filter names only `bench/exhaustion_calib.py` and itself.
- `journal.yml` and `backtest_bench.yml` are scheduled or dispatched only.

`bench.yml` holds no step that names `vps/`, so the hosted gate does not exercise this change. Its control is
`vps/selftest.py` on the VPS (V3, V4).

The direct push of this report was checked against the same filters:
- `main.yml`'s allow-list names neither `CryptoReports/**` nor any `.md`.
- `bench.yml`'s `paths-ignore` carries `'**.md'`.
- Pages serves `index.html`, which is untouched.

## Final Repository State

- Branch `claude/tz-77-paper-api-window-orders` is at `1934bcb6efbd0390efdf2283a180e58cfecba400`, one commit ahead
  of `origin/main` (`e8463bd`). It was pushed before this report was written:
  `git ls-remote origin refs/heads/claude/tz-77-paper-api-window-orders` →
  `1934bcb6efbd0390efdf2283a180e58cfecba400`.
- The working tree on the branch is clean. `vps/__pycache__` was removed, and `git status --porcelain --ignored`
  printed nothing.
- On the VPS:
  - No transient unit of this session remains (V8).
  - `crypto-paper.service` was not restarted (V9).
  - No unit, timer, or file under `/etc` or `/var/lib/cryptopaper` was touched.
  - The TZ-named scratch files `/tmp/tz77.patch` and `/tmp/tz77-v6.py` were removed once their lines and MD5s
    were recorded above (`ls /tmp/tz77*` → no such file).

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

### `SYSTEM-MAP-CRYPTOCALCUL.md` (on `origin/main` = `e8463bd`)

- Revision string: `**Revision 2026-11-06-c.**`, at line 17. It equals the TZ's required revision.
- 2803 lines, MD5 `c7bbb8d1ced39ae5e525955ad181742e`. Both equal the TZ's reported figures.
- Anchor table: **7 rows in the map's table, 7 compared, 7 present.** Each was checked with
  `grep -noF -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md`. Each anchor matches twice: once in the `## 0` table and once
  in the body. The `## 0` block ends before line 171. The body match below is the first match outside that table,
  except for the revision, whose line 17 is itself the revision line.

| Anchor | Matched text, as `grep -noF` printed it (body) | Count |
|---|---|---:|
| revision | `17:**Revision 2026-11-06-c.**` | 2 |
| direction engine | `1056:### 3.12 Direction engine — veto cascade` | 2 |
| catalyst registry | `1446:### 3.15 Catalyst registry` | 2 |
| exhaustion measure | `1543:### 3.16 List exhaustion — the day-range measure` | 2 |
| analytical engine | `2535:## 11. Analytical engine` | 2 |
| squeeze block | `1710:### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 |
| newest invariant | `2252:72. **A write that fails leaves this run's product or nothing` | 2 |

### The map's `## 0` file table (`wc -l`, `md5sum`)

| File | Lines | MD5 | Map states |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

### Files the TZ's gate adds (measured on `origin/main` before the patch)

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | equal; `**Version 31.**` at line 3 |
| `vps/paper.py` | 1413 | `dd4bab0209f99e1da430c87042a92b9c` | equal |
| `vps/selftest.py` | 2627 | `76e814ccbe18551a8f47d6f7eae09669` | equal |
| `vps/units/crypto-paper.service` | 30 | `082a64f8f3a11ca4d4fab6a3974a97e8` | equal; `MemoryMax=128M` at line 26 |

### After the patch (the branch, `1934bcb`)

| File | Lines | MD5 |
|---|---:|---|
| `vps/paper.py` | 1785 | `2d814305c3e2883c79dbcf1c6fa14068` |
| `vps/selftest.py` | 3063 | `505efb7dc01c40dd09c9c9008e49345b` |

The TZ itself: `CryptoTZ/TZ-77-paper-api-window-orders.md`, 1564 lines, MD5 `b56f51f396218daa7cb51766f26a5407`.
