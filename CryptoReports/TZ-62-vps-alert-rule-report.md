# Implementation Report — TZ-62

## Status

**COMPLETED.** The session ran on the VPS. `hostname` returned `vultr`, and every A0 answer was the known one.

1. **The rule is built.** `vps/announce.py` and `vps/selftest.py` match the TZ's MD5s. V1 exited 0 with `selftest: sections 20 checks 296 failed 0 empty 0` and `section T: checks 39 failed 0`. The three negative controls failed exactly the checks the TZ registers. Control 1 failed **10**: rows 1, 2, 3, 4, 7, 11, 12, 13, 21 and 31. Control 2 failed **5**: rows 8, 14, 15, 30 and 32. Control 3 failed **4**: rows 26 and 28, plus the two `act()` checks on the funding notice. No check outside section T failed in any control.
2. **The replay finds nothing to alert on.** C1 exited 0 and read `records 19, unparseable 0`. Its last line is `alerts 0 of 19`. By reason: `record catalogue: 14`, `record non-crypto: 4`, `record noise: 1`.
3. **K1 to K4 are all met.** K1: all twelve of TZ-61's records have the registered catalogue, reason and `record`. K2: the MET tournament record, published 2026-10-08T09:00:19Z, reads `93`, `Latest Activities`, `catalogue`, `record`. K3: 19 records (at least 18 required) and 0 unparseable. K4: `catalogue 93 Latest Activities: 12`, and no other census line names `Latest Activities`.
4. **Old rule against new.** Over the same record, the old rule sent **2** alerts (C2). Both were `catalogId=93 match=list`, at 2026-10-07T09:00:10Z and 2026-10-08T09:00:21Z. These are the two BNB promotions. The new rule would send **0** (C1).
5. **The contract types.** The snapshot holds 879 USDT symbols: `PERPETUAL` 659, `TRADIFI_PERPETUAL` 216, `CURRENT_QUARTER` 2 and `NEXT_QUARTER` 2. Four symbols were onboarded after 2026-10-06T00:00:00Z. All four are `TRADING` and `TRADIFI_PERPETUAL`: `USDEXUSDT` (2026-10-06T09:00:00Z), `VKTXUSDT` (09:05:00Z), `MCDUSDT` (09:10:00Z) and `AKAMUSDT` (09:15:00Z).

The previous TZ, TZ-61, was report-only and opened no branch. Its report is on `main` at `0e96f3f`; `git merge-base --is-ancestor 0e96f3f origin/main` exited 0. The last branch TZ, TZ-60, is merged: `git merge-base --is-ancestor c019a5b origin/main` exited 0, and `git diff --stat c019a5b 450e12a -- vps/` is empty.

## Inbound Filing

Nothing was moved. `CryptoTZ/TZ-62-vps-alert-rule.md` is at its canonical path on `origin/main`, in one copy: 691 lines, blob `2ca5d487d28f8e52794eccd258cb8a55c2a7ad04`, uploaded in `030a598`. It was found after `git fetch --all --prune`. The clone is not shallow: `git rev-parse --is-shallow-repository` returned `false`.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names two files under `vps/`. The branch `tz-62-vps-alert-rule` was opened from `origin/main` at `030a598`. Its `vps` tree before the change was `81c33f881d4728eda33444e7840ecf9110d616d3`.

| Stage | Executed | Outcome |
|---|---|---|
| A0 | yes | all four known answers |
| A1 (§4a 1–6, §5 gate, A1.1–A1.4) | yes | Gate passed 7 of 7. All five edit lines counted `1`. Selftest baseline 19 / 257 / 0 / 0. |
| B1, B2 | yes | Both files at the TZ's MD5 and line count. |
| C0–C4 | yes | Every known answer met. Nothing was left behind. |
| V1–V5 | yes | see `## Validation` |

No credential arrived, was read or was written. No model session was opened and the `claude` binary was not run. The session's only network reads were `git` (fetch, push) and `gh` (`pr create`, `pr list`, `run list`, `run view`, `run watch`, `auth status`). No record's `body` was printed by any command. `announcements.jsonl` was read only by `stat`, `wc -l` and §12.5's script.

### A0 — the host, before the gate

`date -u +%Y-%m-%dT%H:%M:%SZ` printed `2026-10-09T06:03:44Z` right after the four checks.

```
$ hostname
vultr
$ systemctl is-active crypto-bot.service crypto-exchange.service
active
active
$ test -d /srv/crypto-auto/.git && echo clone
clone
$ id -u cryptorun
995
```

### A1 — after the gate

The gate is under `## Fingerprints`.

A1.1, the vps tree. Both values equal the known answer:

```
$ git rev-parse origin/main:vps
81c33f881d4728eda33444e7840ecf9110d616d3
$ cat /var/lib/crypto-auto/deployed-vps-tree
81c33f881d4728eda33444e7840ecf9110d616d3
$ git rev-parse 6e58aea:vps
81c33f881d4728eda33444e7840ecf9110d616d3
$ git log --oneline 6e58aea..450e12a -- vps/ | wc -l
0
$ git log --oneline 450e12a..origin/main -- vps/ | wc -l
0
```

A1.2, the edit points on `origin/main`. Each is counted with `git show origin/main:<file> | grep -c -F -- '<line>'`. The stream header is counted with `grep -c '^# --- the stream ---'`.

| File | Line | Count |
|---|---|---:|
| `vps/announce.py` | `def act(data, cls, ticker):` | 1 |
| `vps/announce.py` | `                outcome = act(data, cls, ticker)` | 1 |
| `vps/announce.py` | line beginning `# --- the stream ---` | 1 |
| `vps/selftest.py` | `SECTIONS = (("A", section_a),` | 1 |
| `vps/selftest.py` | `("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s))` | 1 |

A1.3, the values V4 compares:

```
$ systemctl show crypto-announce.service -p ActiveState -p NRestarts -p ExecMainPID
NRestarts=0
ExecMainPID=34888
ActiveState=active
$ systemctl list-unit-files 'crypto-*' --no-pager
UNIT FILE               STATE   PRESET
crypto-run.path         enabled enabled
crypto-stop.path        enabled enabled
crypto-announce.service enabled enabled
crypto-bot.service      enabled enabled
crypto-cleanup.service  static  -
crypto-deploy.service   static  -
crypto-exchange.service enabled enabled
crypto-run.service      static  -
crypto-stop.service     static  -
crypto-cleanup.timer    enabled enabled
crypto-deploy.timer     enabled enabled

11 unit files listed.
```

A1.4, the selftest on the branch before any edit. Python 3.12.3. The run exited `0`, and its last line matches the known answer:

```
selftest: sections 19 checks 257 failed 0 empty 0
```

### B — the code

A script took every dictated block out of `CryptoTZ/TZ-62-vps-alert-rule.md` as read from `origin/main`. Each block is the lines between its opening fence and the next closing fence, so nothing was retyped (rule 7). The script asserted each opening fence's text and found each edit point exactly once before writing. Block sizes: A 4 lines, B 3, C 2, §12.2 42, §12.3 15, §12.4 84 and §12.5 78. It applied §12.1's five edits to `vps/announce.py` and its three edits to `vps/selftest.py`, and nothing else.

```
$ md5sum vps/announce.py vps/selftest.py; wc -l vps/announce.py vps/selftest.py
4f8724e2ce801470d1a071cb2429cbfe  vps/announce.py
53045fb9aafcf1c26252a4f76da2babe  vps/selftest.py
  452 vps/announce.py
 1107 vps/selftest.py
```

Both MD5s and both line counts equal §8's known answers, so no hunk differs from §12.

### C — on the VPS, on the branch's code, read-only

**C0.** `/root/tz62` did not exist beforehand (`test ! -e /root/tz62` was true). `install -d -m 0700 /root/tz62` created it. §12.5's block, taken from the TZ by the same script, was installed as `/root/tz62/tz62_replay.py` with mode `0600`. The ASCII check `LC_ALL=C grep -c -P '[^\x00-\x7F]'` returned 0.

```
$ md5sum /root/tz62/tz62_replay.py
eb12746c5624da302e762c3811db1a4d  /root/tz62/tz62_replay.py
$ wc -l /root/tz62/tz62_replay.py
78 /root/tz62/tz62_replay.py
```

**C1.** Run from the branch checkout at `42ecda3b9aa85c90d6c5be3cee43e1718af42e5c`, at 2026-10-09T06:07:09Z. When read, the record was 126 118 bytes and 19 lines, last modified 2026-10-09 03:00:14 UTC.

```
$ python3 -I /root/tz62/tz62_replay.py "$PWD/vps" /var/lib/crypto-auto/announcements.jsonl /var/lib/crypto-auto/perpetuals.json; echo $?
```

Exit code: **0**. The output, in full:

```
records 19, unparseable 0, list pairs 31, perpetual pairs 524

| # | publishDate | catalogId | catalogName | title | match | reason | decision | contracts |
|---:|---|---|---|---|---|---|---|---|
| 1 | 2026-10-05T02:00:01Z | 93 | Latest Activities | Binance Lite Loan Promotion Extended: Enjoy Simple Borrowing with 50% Off Service Fee! | none | catalogue | record | - |
| 2 | 2026-10-05T03:00:01Z | 93 | Latest Activities | Word of the Day: Test Your Knowledge on “Proactive Security Wins” to Unlock USDC Rewards! | perpetual USDC | catalogue | record | - |
| 3 | 2026-10-05T09:00:01Z | 93 | Latest Activities | Binance Pay Exclusive: Get up to 20% Off Mobile Top-Ups in Selected Regions! | none | catalogue | record | - |
| 4 | 2026-10-06T01:00:00Z | 93 | Latest Activities | New User bStocks Convert Campaign: Join and Share a Reward Pool of Up to 110 SPCXB | none | catalogue | record | - |
| 5 | 2026-10-06T05:00:01Z | 49 | Latest Binance News | Binance Will Support Marvell Technology (MRVL) and Oracle Corporation (ORCL) Cash Dividend Distribution via bStocks | none | non-crypto | record | - |
| 6 | 2026-10-06T06:15:28Z | 48 | New Cryptocurrency Listing | Binance Futures Will Launch Multiple TradFi USDⓈ-Margined Perpetual Contracts (2026-10-06) | none | non-crypto | record | - |
| 7 | 2026-10-06T09:00:02Z | 93 | Latest Activities | APAC Exclusive: Win a Fully Hosted Trip to Binance Blockchain Week 2026 | none | catalogue | record | - |
| 8 | 2026-10-06T09:30:01Z | 49 | Latest Binance News | Update on the Collateral Ratio Under Cross Margin and Portfolio Margin (2026-10-09) | none | noise | record | - |
| 9 | 2026-10-07T03:00:06Z | 48 | New Cryptocurrency Listing | Binance Exchange Adds JPMorgan Chase (JPMB), Eli Lilly (LLYB), Securitize Corp (SECZB) and StablecoinX Inc (USDEB) bStocks Trading Pairs on Binance Spot/Convert - 2026-10-07 | none | non-crypto | record | - |
| 10 | 2026-10-07T04:00:08Z | 48 | New Cryptocurrency Listing | Binance Will Add 4 bStocks Tokenized Securities as Collateral Asset - 2026-10-07 | none | non-crypto | record | - |
| 11 | 2026-10-07T08:00:04Z | 157 | Maintenance Updates | Binance Has Completed the Stargate Finance (STG) Token Merge to LayerZero (ZRO) | perpetual ZRO | catalogue | record | - |
| 12 | 2026-10-07T09:00:08Z | 93 | Latest Activities | Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards! | list BNB | catalogue | record | - |
| 13 | 2026-10-08T03:00:16Z | 157 | Maintenance Updates | Binance Will Support Scheduled Upgrade for Stock Trading Services - 2026-10-10 | none | catalogue | record | - |
| 14 | 2026-10-08T08:00:03Z | 93 | Latest Activities | Africa Exclusive: Merchant Referral Campaign - Earn 50 USDT Each on Binance P2P | none | catalogue | record | - |
| 15 | 2026-10-08T08:30:03Z | 93 | Latest Activities | Next Stop - BBW: Bring Qualified Referrals to Earn Your Spot at Binance Blockchain Week 2026! | none | catalogue | record | - |
| 16 | 2026-10-08T09:00:19Z | 93 | Latest Activities | MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers | list BNB | catalogue | record | - |
| 17 | 2026-10-08T11:00:05Z | 93 | Latest Activities | Binance Alpha Trading Competition: Trade Zest Protocol (ZEST) and Share $200K Worth of Rewards (2026-10-08) | perpetual ZEST | catalogue | record | - |
| 18 | 2026-10-08T12:00:07Z | 93 | Latest Activities | New Users Exclusive: Subscribe to USDT Simple Earn Flexible Products to Enjoy 30% Bonus APR! | perpetual APR | catalogue | record | - |
| 19 | 2026-10-09T03:00:12Z | 93 | Latest Activities | Binance Earn: Enjoy Up to 5% APR on USDC Flexible Products — Exclusive 5.5% APR for VIP Users with 200,000 USDC Tier (2026-10-09) | perpetual APR | catalogue | record | - |

catalogue 157 Maintenance Updates: 2
catalogue 48 New Cryptocurrency Listing: 3
catalogue 49 Latest Binance News: 2
catalogue 93 Latest Activities: 12
record catalogue: 14
record noise: 1
record non-crypto: 4
alerts 0 of 19
```

The known answers, each against the output above:

| K | Registered | Read | Met |
|---|---|---|---|
| K1 | Six `93`/`Latest Activities` `catalogue` records: 05.10 02:00:01Z, 03:00:01Z, 09:00:01Z; 06.10 01:00:00Z, 09:00:02Z; 07.10 09:00:08Z | rows 1, 2, 3, 4, 7, 12: each `93`, `Latest Activities`, `catalogue`, `record` | yes |
| K1 | 07.10 08:00:04Z: `157`, `Maintenance Updates`, `catalogue` | row 11: `157`, `Maintenance Updates`, `catalogue`, `record` | yes |
| K1 | `non-crypto` records: 06.10 05:00:01Z, 06:15:28Z; 07.10 03:00:06Z, 04:00:08Z | rows 5, 6, 9, 10: each `non-crypto`, `record` | yes |
| K1 | 06.10 09:30:01Z: `noise` | row 8: `noise`, `record` | yes |
| K2 | the MET tournament title, published in [2026-10-08T09:00:00Z, 09:01:00Z): `93`, `Latest Activities`, `catalogue`, `record` | row 16, 2026-10-08T09:00:19Z: `93`, `Latest Activities`, `catalogue`, `record` | yes |
| K3 | `records` at least 18, `unparseable` 0 | `records 19, unparseable 0` | yes |
| K4 | `catalogue 93 Latest Activities: <n>` and no other census line naming `Latest Activities` | `catalogue 93 Latest Activities: 12`; the other three census lines name 157, 48 and 49 | yes |

**C2.**

```
$ TZ=UTC journalctl -u crypto-announce.service --since '2026-10-03 20:37:17 UTC' -o cat --no-pager | grep -c ' alerted lag_ms='
2
```

The registered minimum is 2, so the answer is met. The same window has 19 `announce: data catalogId=` lines, one for each record C1 read. Here they are with their journal time, as `-o short-iso` printed them with the host prefix cut. These lines carry no title and no body.

```
2026-10-05T02:00:02+00:00 announce: data catalogId=93 match=none recorded lag_ms=1278
2026-10-05T03:00:03+00:00 announce: data catalogId=93 match=perpetual recorded lag_ms=1675
2026-10-05T09:00:03+00:00 announce: data catalogId=93 match=none recorded lag_ms=1272
2026-10-06T01:00:32+00:00 announce: data catalogId=93 match=none recorded lag_ms=32414
2026-10-06T05:00:03+00:00 announce: data catalogId=49 match=none recorded lag_ms=1662
2026-10-06T06:15:30+00:00 announce: data catalogId=48 match=none recorded lag_ms=1553
2026-10-06T09:00:03+00:00 announce: data catalogId=93 match=none recorded lag_ms=1496
2026-10-06T09:30:02+00:00 announce: data catalogId=49 match=none recorded lag_ms=1383
2026-10-07T03:00:08+00:00 announce: data catalogId=48 match=none recorded lag_ms=1691
2026-10-07T04:00:09+00:00 announce: data catalogId=48 match=none recorded lag_ms=1404
2026-10-07T08:00:06+00:00 announce: data catalogId=157 match=perpetual recorded lag_ms=2496
2026-10-07T09:00:10+00:00 announce: data catalogId=93 match=list alerted lag_ms=1878
2026-10-08T03:00:17+00:00 announce: data catalogId=157 match=none recorded lag_ms=1309
2026-10-08T08:00:04+00:00 announce: data catalogId=93 match=none recorded lag_ms=1685
2026-10-08T08:30:05+00:00 announce: data catalogId=93 match=none recorded lag_ms=1586
2026-10-08T09:00:21+00:00 announce: data catalogId=93 match=list alerted lag_ms=1843
2026-10-08T11:00:07+00:00 announce: data catalogId=93 match=perpetual recorded lag_ms=2130
2026-10-08T12:00:09+00:00 announce: data catalogId=93 match=perpetual recorded lag_ms=1738
2026-10-09T03:00:14+00:00 announce: data catalogId=93 match=perpetual recorded lag_ms=2064
```

Both `alerted` lines line up with C1's rows 12 and 16, the two BNB promotions. Both rows are `catalogue`/`record` under the new rule.

**C3.** The snapshot was 50 717 bytes, last modified 2026-10-09 05:56:40 UTC. The command is the TZ's one line, verbatim.

```
usdt symbols 879
type CURRENT_QUARTER 2
type NEXT_QUARTER 2
type PERPETUAL 659
type TRADIFI_PERPETUAL 216
onboard AKAMUSDT TRADING TRADIFI_PERPETUAL 1791278100000
onboard MCDUSDT TRADING TRADIFI_PERPETUAL 1791277800000
onboard USDEXUSDT TRADING TRADIFI_PERPETUAL 1791277200000
onboard VKTXUSDT TRADING TRADIFI_PERPETUAL 1791277500000
```

Exit code 0. In UTC, the onboard instants are: AKAMUSDT 2026-10-06T09:15:00Z, MCDUSDT 09:10:00Z, USDEXUSDT 09:00:00Z and VKTXUSDT 09:05:00Z. The threshold `1791244800000` is 2026-10-06T00:00:00Z.

**C4.**

```
$ rm -rf /root/tz62; test ! -e /root/tz62 && echo gone
gone
```

## Files Created

None.

## Files Modified

| File | Before (lines, MD5) | After (lines, MD5) |
|---|---|---|
| `vps/announce.py` | 405, `cb4f9dfc6e3a428283652c4d21468af5` | 452, `4f8724e2ce801470d1a071cb2429cbfe` |
| `vps/selftest.py` | 1022, `40b6a609bbbc3e75acca7614c4241b7a` | 1107, `53045fb9aafcf1c26252a4f76da2babe` |

`git diff --stat origin/main...HEAD`: `2 files changed, 147 insertions(+), 15 deletions(-)`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

- **`announce.alert_rule(data, cls, list_pairs)`** (§12.2) returns `(reason, symbols)` for one record. The first rule that applies wins: the silent catalogues `93` and `157` give `catalogue`; then `NON_CRYPTO` on the title gives `non-crypto`; `48` with `NEW_COIN` gives `new-coin`; `NOISE` gives `noise`; a list match gives `list`; a perpetual match in a listing catalogue, or with `DELIST` in the title, gives `perpetual`; a Futures/Perpetual title with a contract term, whose body names list contracts, gives `contract` with those contracts; anything else gives `none`. All patterns are case-sensitive.
- **`announce.act(data, cls, ticker, list_pairs=())`** (§12.3) alerts only on a reason in `ALERT_REASONS`. It writes `common.A1` unchanged and appends ` · ` and the contracts when there are any. `main` now passes `list_tickers` to it. `record`, `match_title`, the subscription, the journal's `announce: data` line and `common.A1`–`A4` did not move.
- **Section T** (§12.4) adds 32 rule rows and 7 `act()` checks on `spool_in`'s temporary spool.
- **Rows whose decision is `alert` in C1: none.** All 19 records of the stream are `record`, so no title, reason or contract set is named here.
- **C3's reading, for the map.** All 216 `TRADIFI_PERPETUAL` symbols, and all four symbols onboarded since 2026-10-06, are of a type `exchange.act` does not alert on: A2 goes only to a new `PERPETUAL` off the list. The TZ (§5) leaves this decision to the map.

## Validation

**V1, the selftest.** Run on the branch:

```
$ python3 vps/selftest.py; echo $?
...
section S: checks 35 failed 0
section T: checks 39 failed 0
selftest: sections 20 checks 296 failed 0 empty 0
0
```

Sections A–S have the same per-section counts as A1.4's baseline: `diff` of the `section ` lines shows only the added `section T: checks 39 failed 0`. So nothing regressed, and T is the only new section.

**V1, the negative controls.** One script did all three. For each control it checked that the text occurs exactly once in `vps/announce.py`, wrote the mutated file, and ran the selftest. It mapped each `FAIL section T:` label back to §12.4's row number by its `"<cid> <title> -> <reason>"` label, which is unique for all 32 rows. Then it wrote the saved original back, re-read its MD5 and ran the selftest again.

| # | Mutation in `vps/announce.py` | Exit | Section T failures | Outside T | MD5 after revert | V1 after |
|---|---|---:|---|---:|---|---|
| 1 | `SILENT_CATALOGS = ("93", "157")` → `SILENT_CATALOGS = ()` | 1 | **10**: rows 1, 2, 3, 4, 7, 11, 12, 13, 21, 31 | 0 | `4f8724e2…`, equal | exit 0, 296 / 0 / 0 |
| 2 | `    if NOISE.search(title):` → `    if False:` | 1 | **5**: rows 8, 14, 15, 30, 32 | 0 | `4f8724e2…`, equal | exit 0, 296 / 0 / 0 |
| 3 | `        symbols = [symbol for _ticker, symbol in list_pairs if _word(symbol).search(body)]` → `        symbols = []` | 1 | **4**: rows 26, 28; `act(): a contract notice on list contracts alerts`; `act(): A1 with the contracts appended` | 0 | `4f8724e2…`, equal | exit 0, 296 / 0 / 0 |

Each partition is exactly the one V1 registers. In each control the selftest printed `section T: checks 39 failed N`, with every other section at `failed 0`. Its stderr carried nothing besides the `FAIL` lines.

The script's first invocation stopped on its own assertion before writing anything. It had looked for control 1's text as a whole line, but that line carries a trailing comment (`# catalogId as text: …`). The assertion comes before the write, and `md5sum vps/announce.py` read `4f8724e2ce801470d1a071cb2429cbfe` afterwards. The second invocation matched each control's exact text, once, as a substring. It replaced only that text and kept the comment.

**V2, syntax.** `python3 -m py_compile vps/announce.py vps/selftest.py` exited 0. The `vps/__pycache__/` that runs create is git-ignored, and it was removed before the commit.

**V3, scope.**

```
$ git diff --name-only origin/main...HEAD
vps/announce.py
vps/selftest.py
```

**V4, nothing touched.** These readings were taken after C4 (2026-10-09T06:07:56Z):

```
$ systemctl show crypto-announce.service -p NRestarts -p ExecMainPID
NRestarts=0
ExecMainPID=34888
```

`diff` against A1.3's values printed nothing, and the same holds for `systemctl list-unit-files 'crypto-*' --no-pager` (11 unit files, same states). `/var/lib/crypto-auto/deployed-vps-tree` still reads `81c33f881d4728eda33444e7840ecf9110d616d3`.

**V5, pushes.** The branch `tz-62-vps-alert-rule` was pushed to `origin` and pull request #50 was opened. `main` receives nothing from this session except this report.

## Test Results

| Check | Where | Result |
|---|---|---|
| `python3 vps/selftest.py`, before the edit (A1.4) | VPS, branch at `030a598` | exit 0; 19 sections, 257 checks, 0 failed, 0 empty |
| `python3 vps/selftest.py`, after (V1) | VPS, branch at `42ecda3` | exit 0; 20 sections, 296 checks, 0 failed, 0 empty; section T 39 / 0 |
| Negative controls 1–3 | VPS | 10 / 5 / 4 failures, all inside section T, as registered; green after each revert |
| `py_compile` | VPS | exit 0 |
| C1 replay | VPS, record of 19 | exit 0; 0 alerts of 19; K1–K4 met |
| `bench.yml` ("Bench gate"), run `37891973536` | GitHub runner, `pull_request` | `success` (see `## CI Execution`) |

## Deviations

- **D-1, the commit message carries a trailer.** The implementation commit's first line is §13's string, verbatim. It is followed by a blank line and `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, as TZ-60's `c019a5b` and TZ-61's `0e96f3f` carry.

Nothing else deviates from the TZ.

## Pre-existing Issues

- **The hosted gate does not run `vps/selftest.py`.** `grep -n -i 'vps\|selftest' .github/workflows/bench.yml` matches only the step running `analyst/live-gate.sh --selftest`, lines 142 and 144. Section T's proof for this branch is therefore the local run above. The deployer's `install.sh` runs the selftest again before it installs the merge.

## Remaining Risks

- **R-1, the perpetual `APR` reads as noise.** `NOISE` carries `\bAPR\b` in capitals, and `APR` is also a perpetual's base (`APRUSDT`, in `/var/lib/crypto-auto/perpetuals.json`). Case-sensitivity separates `Win` from `WIN` but cannot separate these. This probe tested every list and perpetual base as `(<BASE>)` against `NOISE`, `NON_CRYPTO`, `DELIST`, `CONTRACT` and `CONTRACT_TERMS`. Out of 31 list pairs and 524 perpetual pairs, exactly one base matched: `perpetual APR APRUSDT ticker matched by NOISE`. `alert_rule` on `{"catalogId": 161, "catalogName": "Delisting", "title": "Binance Will Delist APR (APR)"}` returned `('noise', [])`. Under the old rule (`origin/main`, `vps/announce.py` lines 336–339), a perpetual match in a catalogue whose name contains `listing` alerted, so for this one ticker the change takes away an alert the old rule would have sent. The probe was read-only, and the code was not changed (§6); the decision is the Architect's.
- **R-2, no alerting path has a live case yet.** All 19 records in the stream are `record` under the new rule, so `new-coin`, `list`, `perpetual`, `contract` and A1's appended contracts are proven only by section T's fixtures. The first alert under the rule will be its first live reading.
- **R-3, the old rule runs until the merge is installed.** `crypto-announce.service` still runs `vps` tree `81c33f88…` (V4). A promotion that names a list coin will keep reaching the owner until the deployer installs this branch from `main` (contract §7 item 15).
- **R-4, a contract notice needs the record's `body`.** A Futures notice that names its contracts only in an article the stream delivers without a `body` reads `none` (§12.4, row 29). All 19 records were read without printing their bodies. The session did not measure how many of them carry a non-empty `body`.

## Commit

Implementation, on the branch, already pushed: `42ecda3b9aa85c90d6c5be3cee43e1718af42e5c`.

```
TZ-62: vps — the alert rule: promotions and maintenance never alert; new coins, list coins and contract notices do

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

Contents: `vps/announce.py`, `vps/selftest.py`.

Report, on `main`:

```
TZ-62: report — the alert rule, and its replay on the stream's record
```

Contents: `CryptoReports/TZ-62-vps-alert-rule-report.md`.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/50. Base `main`, head `tz-62-vps-alert-rule`, opened by this session.

## CI Execution

- **`bench.yml` ("Bench gate"), run `37891973536`, event `pull_request`, head `42ecda3b9aa85c90d6c5be3cee43e1718af42e5c`: completed, conclusion `success`.** This was read with `gh run view 37891973536 --json conclusion,status,headSha,event,databaseId,workflowName`. The workflow has no step that runs `vps/selftest.py` (`## Pre-existing Issues`), so the run proves nothing about `vps/`.
- `bench.yml` on `push` did not run: its `push` trigger names `main` and `claude/**`, and this branch is neither.
- `main.yml` did not run and cannot run from this branch. Its `push` filter is an allow-list of `main.py` and `.github/workflows/main.yml`, confirmed before this report's push. `calib.yml` filters on `bench/exhaustion_calib.py`, its own file and `claude/**`. `journal.yml` and `backtest_bench.yml` are schedule- or dispatch-only.
- **What runs `vps/selftest.py` is the VPS deployer's `install.sh`, at the merge.** The local runs on this host are under `## Validation`.

## Final Repository State

The branch `tz-62-vps-alert-rule` is at `42ecda3b9aa85c90d6c5be3cee43e1718af42e5c`, pushed to `origin`, with a clean working tree (`git status --porcelain --ignored` returned 0 lines). It is one commit ahead of `030a598`, and its `vps` tree is `d65dfbd5d1830b477a084e2f288a851e377d6947`. The VPS outside the repository is as A1 found it: the same 11 unit files and states, `crypto-announce.service` with the same `NRestarts` and `ExecMainPID`, and no `/root/tz62`. No unit changed state. No run was started, requested or stopped. Nothing under `/etc/crypto-auto/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or `/var/spool/crypto-auto` was written.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

The gate read `SYSTEM-MAP-CRYPTOCALCUL.md` and the TZ from `origin/main` with `git show`. It cut each anchor table by its structure: every `|` row after the `|---|---|` separator that follows `| Anchor | Exact string that must be present |`, up to the first line not starting with `|`. The map's table and the TZ header's table were cut the same way and compared with `diff`, which found them identical row for row. Each anchor was then matched against the map with `grep -F -m1 -o -- <anchor>`.

- Revision string, the first in `## 0. Fingerprint`: `**Revision 2026-10-09-a.**`. The TZ requires `**Revision 2026-10-09-a.**`.
- **Map anchor table rows: 7. Compared: 7. Passed: 7.** The TZ header's anchor rows: 7.

| Anchor | TZ row identical | `grep -F -m1 -o` exit | Text the match returned |
|---|---|---:|---|
| revision | yes | 0 | `**Revision 2026-10-09-a.**` |
| direction engine | yes | 0 | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | yes | 0 | `### 3.15 Catalyst registry` |
| exhaustion measure | yes | 0 | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | yes | 0 | `## 11. Analytical engine` |
| squeeze block | yes | 0 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | yes | 0 | `72. **A write that fails leaves this run's product or nothing` |

Each anchor except the revision string also occurs outside the table. `grep -n -F` finds them at map lines 1554, 1944, 2041, 3060, 2208 and 2750. The revision string's first occurrence is line 17.

The map's file table and the TZ's file table were cut the same way and are identical (4 rows each). Files at `origin/main` (`030a598`):

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 3308 | `aff11ff251052fc6dde514070bef2c3a` | 3308 / `aff11ff2…`, equal (reported, not enforced) |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | equal; version line `**Version 26.**` (line 3) |
| `vps/announce.py` | 405 | `cb4f9dfc6e3a428283652c4d21468af5` | equal |
| `vps/selftest.py` | 1022 | `40b6a609bbbc3e75acca7614c4241b7a` | equal |
| `vps/common.py` | 364 | `62e3e688cfce21e3e9887e057e461fef` | equal |

`origin/main:vps` is `81c33f881d4728eda33444e7840ecf9110d616d3`. That equals the tree this TZ was written against and the deployed marker. The branch's files after the change are under `## Files Modified`.
