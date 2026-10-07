# Implementation Report — TZ-61

## Status

**COMPLETED.** The session ran on the VPS. `hostname` returned `vultr`, and every A0 answer was the known one.

1. **The STOP stands installed.** A1.2's journal carries exactly one install line, `2026-10-05T12:26:39.784972+00:00 vultr deploy.sh[34105]: deploy: installed vps tree 81c33f881d4728eda33444e7840ecf9110d616d3`. **`T3` = 2026-10-05T12:26:39.784972Z.** Before it are `install: enabled crypto-stop.path` (12:26:39.415638Z) and `install: restarted crypto-announce.service` (12:26:39.741034Z).
2. **The verdict is `W1`, «delivers».** R 7, R~ 0, M 0, G 0. The control, post 9021, is `unmatched`.
3. **The known answers: K1 met, K2 met, K3 met.** K1: all three records of 05.10 (02:00:01Z, 03:00:01Z, 09:00:01Z) are `present, Latest Activities`. K2: post 9021 is `unmatched`. K3: one record, `publishDate` 2026-10-07T09:00:08Z, `catalogName` `Latest Activities`, the registered title, outcome `list alerted`. There is one bot alert line in [09:00:00Z, 09:01:00Z), at 09:00:10.953901Z.
4. **The alerts.** There are 12 records at or after `T1`, and all 12 joined to a data line. By outcome: `list alerted` 1, `perpetual recorded` 2, `none recorded` 9. The bot's journal has **1** alert line since `T1`, and it is K3's.
5. **The connection.** There are **6** up intervals. **23.988327 s** of the 352 328 s between `T1` and `R` are covered by no up interval. That is six reconnect gaps of 1.5–6.4 s each. At the script's integer precision the figure is 28 s (under `## Validation`).

The previous TZ is merged. `git merge-base --is-ancestor c019a5b657ee778396f52ef1598b79ee82d587d4 origin/main` exited 0, so TZ-60's implementation reached `main` through `6e58aea`, pull request #49.

## Inbound Filing

None moved. `CryptoTZ/TZ-61-vps-stream-against-channel.md` is at its canonical path on `origin/main`, in one copy: 638 lines, blob `31a79e3a6d97219101f8ab65af97e54e52c644b1`, uploaded in `f7d5cde`. It was found after `git fetch --all --prune`, which exited 0. The clone is not shallow: `git rev-parse --is-shallow-repository` returned `false`.

## Scope Executed

**Class: report-only TZ** (contract §8). Under `## Scope`, Files to Modify, Files to Create and Files to Delete are all `None`. The one written file is this report, on the `CryptoReports/**` path.

| Stage | Executed | Outcome |
|---|---|---|
| A0 | yes | all four known answers |
| A1 (§4a 1–6, §5 gate, A1.1, A1.2) | yes | gate 7/7. TZ-60 merged. The marker equals `origin/main:vps`. Every known A1.2 answer met. |
| A2 | yes | unit active, journal from 20:37:16.748664Z. Extracts 42 and 1 lines. Script MD5 and line count equal. |
| A3 | yes | exit 0. **W1**. K1, K2 and K3 met. |
| V1–V4 | yes | all met. V2's «must not move» half has no rows to compare (Remaining Risks R-3). |
| §9 | yes | `gone` |

### A0 — the host, before the gate

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

All four are the known answers: `vultr`, `active` twice, `clone` and `995`. This was read at 2026-10-07T22:28:24Z.

### A1 — the gate and the installed tree

Contract §4a steps 1–6 and the §5 gate ran against `origin/main` at `f7d5cded85f26b376d1ad6291299aad88ede3dd1`. `HEAD` equalled it, and `git status --porcelain` gave 0 lines. The gate passed 7/7 (`## Fingerprints`). Every file in the map's table and the TZ's added-files table matched (`## Fingerprints`). `EXECUTOR-INSTRUCTIONS.md` line 3 reads `**Version 26.**`.

`git log --oneline --graph --all` showed `main` in a straight line from `6e58aea` (the merge of #49, TZ-60) to `f7d5cde`. The commits in between are `analyst:` and `journal:` commits, a map upload (`d51d6c1`) and this TZ's upload (`f7d5cde`).

**A1.1.** `git merge-base --is-ancestor c019a5b657ee778396f52ef1598b79ee82d587d4 origin/main` → exit **0**.

**A1.2.**

```
$ git rev-parse origin/main:vps
81c33f881d4728eda33444e7840ecf9110d616d3
$ cat /var/lib/crypto-auto/deployed-vps-tree
81c33f881d4728eda33444e7840ecf9110d616d3
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
$ TZ=UTC journalctl -u crypto-deploy.service --since '2026-10-05 12:21:54 UTC' -o short-iso-precise --no-pager | grep -E 'deploy: (installed vps tree|install refused|unsigned)|install: (removed|enabled|disabled|restarted|installed)'
2026-10-05T12:26:36.815627+00:00 vultr deploy.sh[34123]: install: enabled crypto-deploy.timer
2026-10-05T12:26:37.109583+00:00 vultr deploy.sh[34123]: install: enabled crypto-cleanup.timer
2026-10-05T12:26:37.457506+00:00 vultr deploy.sh[34123]: install: enabled crypto-exchange.service
2026-10-05T12:26:37.771582+00:00 vultr deploy.sh[34123]: install: enabled crypto-bot.service
2026-10-05T12:26:38.356804+00:00 vultr deploy.sh[34123]: install: enabled crypto-run.path
2026-10-05T12:26:38.888682+00:00 vultr deploy.sh[34123]: install: enabled crypto-announce.service
2026-10-05T12:26:39.415638+00:00 vultr deploy.sh[34123]: install: enabled crypto-stop.path
2026-10-05T12:26:39.568709+00:00 vultr deploy.sh[34123]: install: restarted crypto-exchange.service
2026-10-05T12:26:39.655205+00:00 vultr deploy.sh[34123]: install: restarted crypto-bot.service
2026-10-05T12:26:39.741034+00:00 vultr deploy.sh[34123]: install: restarted crypto-announce.service
2026-10-05T12:26:39.764509+00:00 vultr deploy.sh[34123]: install: installed
2026-10-05T12:26:39.784972+00:00 vultr deploy.sh[34105]: deploy: installed vps tree 81c33f881d4728eda33444e7840ecf9110d616d3
```

Every known answer is met:

- The marker equals `origin/main:vps`.
- There is exactly one `deploy: installed vps tree` line, for that tree.
- `install: enabled crypto-stop.path` and `install: restarted crypto-announce.service` come before it.
- 11 unit files are listed, with `crypto-stop.path` `enabled` and `crypto-stop.service` `static`.
- No `install refused` or `unsigned` line appears.

`git rev-parse 6e58aea:vps` returns `81c33f881d4728eda33444e7840ecf9110d616d3`. `6e58aea` is dated 2026-10-05T16:21:54+04:00, which is 12:21:54Z. `git log --oneline 6e58aea..origin/main -- vps/` lists 0 commits.

### A2 — the stream's own record

**A2.1.** `date -u +%FT%TZ` → **`R` = `2026-10-07T22:29:25Z`**, so `<R′>` = `2026-10-07 22:29:25`. Then `install -d -m 0700 /root/tz61`, and `stat -c '%a %U %n'` → `700 root /root/tz61`.

**A2.2.**

```
$ systemctl show crypto-announce.service -p ActiveState -p SubState -p NRestarts -p ActiveEnterTimestamp -p ExecMainPID
NRestarts=0
ExecMainPID=34888
ActiveState=active
SubState=running
ActiveEnterTimestamp=Mon 2026-10-05 12:26:39 UTC
$ dpkg-query -W -f='${Version}\n' python3-websocket
1.7.0-1
$ TZ=UTC journalctl -u crypto-announce.service -o short-iso-precise --no-pager | head -1
2026-10-03T20:37:16.748664+00:00 vultr systemd[1]: Starting crypto-announce.service - Crypto assistant: Binance announcement stream...
```

Both known answers are met. The unit reads `ActiveState=active`. The journal's first line is dated 2026-10-03T20:37:16.748664Z, which is before `T1` = 20:37:17Z, so no window classes `G` because the journal is missing. `ActiveEnterTimestamp` is `T3`'s second, the deployer's restart.

**A2.3.**

```
$ TZ=UTC journalctl -u crypto-announce.service --since '2026-10-03 20:37:17 UTC' --until '2026-10-07 22:29:25 UTC' -o short-iso-precise --no-pager > /root/tz61/announce.journal   # exit 0
$ wc -l /root/tz61/announce.journal
42 /root/tz61/announce.journal
$ TZ=UTC journalctl -u crypto-bot.service --since '2026-10-03 20:37:17 UTC' --until '2026-10-07 22:29:25 UTC' -o short-iso-precise --no-pager | grep -F 'kind=alert' > /root/tz61/bot.journal   # PIPESTATUS 0 0
$ wc -l /root/tz61/bot.journal
1 /root/tz61/bot.journal
```

The one `kind=alert` line is quoted under K3 below. It names an outbox file and counts, and nothing else. Its format is `bot.py` line 275, `"bot: sent %s kind=%s chunks=%d accepted=%d plain_fallbacks=%d"`.

**A2.4.** The script was extracted from §12.3 of the TZ file on `origin/main`. The extractor took the lines between the `` ```python `` fence that follows `### 12.3 ` and the next closing fence, and wrote them to `/root/tz61/tz61_join.py`.

```
$ md5sum /root/tz61/tz61_join.py
78f37d1f2c37b58452c43e1afba7fa72  /root/tz61/tz61_join.py
$ wc -l /root/tz61/tz61_join.py
274 /root/tz61/tz61_join.py
$ LC_ALL=C grep -c '[^ -~]' /root/tz61/tz61_join.py
0
```

The MD5 equals **`78f37d1f2c37b58452c43e1afba7fa72`**, the file has **274** lines, it is ASCII only, and its last byte is `\n`. This is the dictated program.

### A3 — the join

`python3 --version` → `Python 3.12.3`.

```
$ python3 -I /root/tz61/tz61_join.py 2026-10-07T22:29:25Z /root/tz61/announce.journal /root/tz61/bot.journal /var/lib/crypto-auto/announcements.jsonl
```

**Exit code: 0.** The full output follows. It prints no `body` field: of each record the script prints only `title`, `catalogId`, `catalogName`, `publishDate` and `received_ms`.

````
journal lines 42, unparsed 0; records in file 12, unparseable 0, at or after T1 12

### Connection events (every journal line but 'announce: data ')

2026-10-03T20:37:17.006567+00:00 systemd[1] Started crypto-announce.service - Crypto assistant: Binance announcement stream.
2026-10-03T20:37:17.476508+00:00 python3[4006064] announce: key ACCEPTED ipRestrict=true enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableReading=true enableFutures=false enableMargin=false
2026-10-03T20:37:18.516535+00:00 python3[4006064] announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-03T20:37:18.516535+00:00 python3[4006064] announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-03T21:02:34.664561+00:00 systemd[1] Stopping crypto-announce.service - Crypto assistant: Binance announcement stream...
2026-10-03T21:02:34.668544+00:00 systemd[1] crypto-announce.service: Deactivated successfully.
2026-10-03T21:02:34.668708+00:00 systemd[1] Stopped crypto-announce.service - Crypto assistant: Binance announcement stream.
2026-10-03T21:02:34.680713+00:00 systemd[1] Starting crypto-announce.service - Crypto assistant: Binance announcement stream...
2026-10-03T21:02:34.716350+00:00 systemd[1] Started crypto-announce.service - Crypto assistant: Binance announcement stream.
2026-10-03T21:02:35.172250+00:00 python3[4009704] announce: key ACCEPTED ipRestrict=true enableReading=true enableFutures=false enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableMargin=false
2026-10-03T21:02:36.452507+00:00 python3[4009704] announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-03T21:02:36.452507+00:00 python3[4009704] announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-04T17:31:21.445930+00:00 python3[4009704] announce: connection lost (WebSocketConnectionClosedException)
2026-10-04T17:31:27.821910+00:00 python3[4009704] announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-04T17:31:27.821910+00:00 python3[4009704] announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-05T12:26:39.671943+00:00 systemd[1] Stopping crypto-announce.service - Crypto assistant: Binance announcement stream...
2026-10-05T12:26:39.678719+00:00 systemd[1] crypto-announce.service: Deactivated successfully.
2026-10-05T12:26:39.678942+00:00 systemd[1] Stopped crypto-announce.service - Crypto assistant: Binance announcement stream.
2026-10-05T12:26:39.678975+00:00 systemd[1] crypto-announce.service: Consumed 16.574s CPU time, 16.7M memory peak, 14.6M memory swap peak.
2026-10-05T12:26:39.694801+00:00 systemd[1] Starting crypto-announce.service - Crypto assistant: Binance announcement stream...
2026-10-05T12:26:39.738551+00:00 systemd[1] Started crypto-announce.service - Crypto assistant: Binance announcement stream.
2026-10-05T12:26:40.255212+00:00 python3[34888] announce: key ACCEPTED ipRestrict=true enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableReading=true enableFutures=false enableMargin=false
2026-10-05T12:26:41.280507+00:00 python3[34888] announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-05T12:26:41.280507+00:00 python3[34888] announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-06T07:56:00.198007+00:00 python3[34888] announce: connection lost (WebSocketConnectionClosedException)
2026-10-06T07:56:06.543998+00:00 python3[34888] announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-06T07:56:06.543998+00:00 python3[34888] announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-07T07:26:06.779983+00:00 python3[34888] announce: planned refresh after 84600 s
2026-10-07T07:26:13.133294+00:00 python3[34888] announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-07T07:26:13.133294+00:00 python3[34888] announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}

### Up intervals

| opened | closed | closed by | seconds |
|---|---|---|---:|
| 2026-10-03T20:37:18Z | 2026-10-03T21:02:34Z | Stopping crypto-announce.service - Crypto assistant: Binance | 1516 |
| 2026-10-03T21:02:36Z | 2026-10-04T17:31:21Z | announce: connection lost (WebSocketConnectionClosedExceptio | 73724 |
| 2026-10-04T17:31:27Z | 2026-10-05T12:26:39Z | Stopping crypto-announce.service - Crypto assistant: Binance | 68111 |
| 2026-10-05T12:26:41Z | 2026-10-06T07:56:00Z | announce: connection lost (WebSocketConnectionClosedExceptio | 70158 |
| 2026-10-06T07:56:06Z | 2026-10-07T07:26:06Z | announce: planned refresh after 84600 s | 84600 |
| 2026-10-07T07:26:13Z | 2026-10-07T22:29:25Z | R | 54191 |

### Records at or after T1

| # | received | publishDate | lag s | catalogId | catalogName | title | outcome |
|---:|---|---|---:|---|---|---|---|
| 1 | 2026-10-05T02:00:02Z | 2026-10-05T02:00:01Z | 1.278 | 93 | Latest Activities | Binance Lite Loan Promotion Extended: Enjoy Simple Borrowing with 50% Off Service Fee! | none recorded |
| 2 | 2026-10-05T03:00:03Z | 2026-10-05T03:00:01Z | 1.675 | 93 | Latest Activities | Word of the Day: Test Your Knowledge on “Proactive Security Wins” to Unlock USDC Rewards! | perpetual recorded |
| 3 | 2026-10-05T09:00:03Z | 2026-10-05T09:00:01Z | 1.272 | 93 | Latest Activities | Binance Pay Exclusive: Get up to 20% Off Mobile Top-Ups in Selected Regions! | none recorded |
| 4 | 2026-10-06T01:00:32Z | 2026-10-06T01:00:00Z | 32.414 | 93 | Latest Activities | New User bStocks Convert Campaign: Join and Share a Reward Pool of Up to 110 SPCXB | none recorded |
| 5 | 2026-10-06T05:00:03Z | 2026-10-06T05:00:01Z | 1.662 | 49 | Latest Binance News | Binance Will Support Marvell Technology (MRVL) and Oracle Corporation (ORCL) Cash Dividend Distribution via bStocks | none recorded |
| 6 | 2026-10-06T06:15:29Z | 2026-10-06T06:15:28Z | 1.553 | 48 | New Cryptocurrency Listing | Binance Futures Will Launch Multiple TradFi USDⓈ-Margined Perpetual Contracts (2026-10-06) | none recorded |
| 7 | 2026-10-06T09:00:03Z | 2026-10-06T09:00:02Z | 1.496 | 93 | Latest Activities | APAC Exclusive: Win a Fully Hosted Trip to Binance Blockchain Week 2026 | none recorded |
| 8 | 2026-10-06T09:30:02Z | 2026-10-06T09:30:01Z | 1.383 | 49 | Latest Binance News | Update on the Collateral Ratio Under Cross Margin and Portfolio Margin (2026-10-09) | none recorded |
| 9 | 2026-10-07T03:00:08Z | 2026-10-07T03:00:06Z | 1.691 | 48 | New Cryptocurrency Listing | Binance Exchange Adds JPMorgan Chase (JPMB), Eli Lilly (LLYB), Securitize Corp (SECZB) and StablecoinX Inc (USDEB) bStocks Trading Pairs on Binance Spot/Convert - 2026-10-07 | none recorded |
| 10 | 2026-10-07T04:00:09Z | 2026-10-07T04:00:08Z | 1.404 | 48 | New Cryptocurrency Listing | Binance Will Add 4 bStocks Tokenized Securities as Collateral Asset - 2026-10-07 | none recorded |
| 11 | 2026-10-07T08:00:06Z | 2026-10-07T08:00:04Z | 2.496 | 157 | Maintenance Updates | Binance Has Completed the Stargate Finance (STG) Token Merge to LayerZero (ZRO) | perpetual recorded |
| 12 | 2026-10-07T09:00:10Z | 2026-10-07T09:00:08Z | 1.878 | 93 | Latest Activities | Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards! | list alerted |

data lines 12, joined 12, unjoined data lines 0, records with no line 0

### The reference

| post | t_p | class | record publishDate | t_p - publishDate s | candidates in [t_p - 1800 s, t_p] |
|---:|---|---|---|---:|---|
| 9021 | 2026-10-02T09:02:01Z | unmatched | - | - | - |
| 9022 | 2026-10-05T02:04:14Z | R | 2026-10-05T02:00:01Z | 252 | - |
| 9023 | 2026-10-06T05:02:43Z | R | 2026-10-06T05:00:01Z | 161 | - |
| 9024 | 2026-10-06T09:03:33Z | R | 2026-10-06T09:00:02Z | 210 | - |
| 9025 | 2026-10-06T09:32:08Z | R | 2026-10-06T09:30:01Z | 126 | - |
| 9026 | 2026-10-07T03:02:46Z | R | 2026-10-07T03:00:06Z | 159 | - |
| 9027 | 2026-10-07T04:01:38Z | R | 2026-10-07T04:00:08Z | 89 | - |
| 9028 | 2026-10-07T08:01:40Z | R | 2026-10-07T08:00:04Z | 95 | - |

classed 7: R 7, R~ 0, M 0, G 0; control 9021: unmatched
VERDICT W1
NEGATIVE CONTROL (no records): R/R~ rows 7, flipped to M/G 7; M/G rows 0, unchanged 0; control unmatched; up intervals 6 unchanged True

### Known answers

K1 2026-10-05T02:00:01Z: present, Latest Activities
K1 2026-10-05T03:00:01Z: present, Latest Activities
K1 2026-10-05T09:00:01Z: present, Latest Activities
K3 record: publishDate 2026-10-07T09:00:08Z, catalogName Latest Activities, title Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards!, outcome list alerted
K3 alert lines in [2026-10-07T09:00:00Z, 09:01:00Z): 1

### Alerts

outcome list alerted: 1
outcome none recorded: 9
outcome perpetual recorded: 2
bot alert lines since T1: 1
````

**Known answers.**

- **K1: met.** All three stamps print `present, Latest Activities`. The 02:00:01Z record is the one post 9022 joined to (R, `t_p − publishDate` 252 s).
- **K2: met.** Post 9021 is `unmatched`, so the verdict is not `void`.
- **K3: met, every part.**
  - The record: `publishDate 2026-10-07T09:00:08Z` (inside [09:00:00Z, 09:01:00Z)), `catalogName Latest Activities`, title `Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards!`, outcome `list alerted`.
  - `K3 alert lines in [2026-10-07T09:00:00Z, 09:01:00Z): 1`. The line is `2026-10-07T09:00:10.953901+00:00 vultr python3[34878]: bot: sent 1791363610181-alert-34888.json kind=alert chunks=1 accepted=1 plain_fallbacks=0`. The file name carries the announce process's PID, `34888`, which is A2.2's `ExecMainPID`.
  - The registered chat time follows: 09:00:08Z is 13:00 in Asia/Tbilisi (UTC+4).

## Files Created

- `CryptoReports/TZ-61-vps-stream-against-channel-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

This TZ is read-only. Nothing was built and no unit changed state. These readings come from A3's printed output and the journal lines above. Each is a reading, and none is a decision (§5).

- **Every classed post is in the stream, received while subscribed.** All seven classed posts (9022–9028) joined a record by exact `N(title)`. None needed `R~`. The posts trail the records' `publishDate` by 89 s to 252 s (column `t_p - publishDate s`), inside the 1 800 s window.
  - With the records removed, each of the seven posts' windows [`t_p` − 1 800 s, `t_p`] lies inside one printed up interval. 9022 is in the interval opened 2026-10-04T17:31:27Z. 9023 is in the one opened 2026-10-05T12:26:41Z. 9024–9027 are in the one opened 2026-10-06T07:56:06Z. 9028 is in the one opened 2026-10-07T07:26:13Z, whose window opens at 07:31:40Z.
  - So each would class `M`, not `G`. `W1` therefore rests on seven publications the stream was subscribed throughout, not on gaps that excuse a miss. (This M-not-G split is derived from the printed intervals. The script prints only the flip count.)
- **The channel is a strict subset of the stream here.** Of the 12 records since `T1`, 7 have a channel post. The other 5 have none: #2 `Word of the Day…`, #3 `Binance Pay Exclusive…`, #4 `New User bStocks Convert Campaign…`, #6 `Binance Futures Will Launch Multiple TradFi USDⓈ-Margined Perpetual Contracts (2026-10-06)` and #12 (K3). This agrees with the map's lower-bound reading of the reference.
- **The stream's own delivery lag.** `received − publishDate` is 1.272–2.496 s for 11 records. Record #4 (2026-10-06T01:00:00Z, `Latest Activities`) took 32.414 s.
- **Why the owner's chat is quiet: the alert rule recorded 11 of 12 records and alerted 1.** This is the rule in `announce.act` quoted in §2, read here and not judged.
  - The alert is #12 (K3), a `list` match.
  - Two records are `perpetual recorded`: #2 (`Latest Activities`) and #11 (`Maintenance Updates`). Neither catalogue's name contains `listing`, which `act` requires before a perpetual match alerts. The data line does not name the matched ticker, so this reading does not say which one matched.
  - Nine records are `none recorded`. Among them are three in `New Cryptocurrency Listing`: #6, #9 and #10. #9 and #10 name bStocks tickers (`JPMB`, `LLYB`, `SECZB`, `USDEB` and «4 bStocks»). #6 names no ticker at all. `match_title` (`vps/announce.py` lines 124–132) matches tickers only, so neither branch of the rule could fire on #6.
- **The connection.** 6 up intervals cover `T1`–`R`, split by 6 gaps:
  - 2026-10-03T20:37:17Z → 20:37:18.516535Z, 1.516535 s: `T1` to the first SUBSCRIBE success.
  - 2026-10-03T21:02:34.664561Z → 21:02:36.452507Z, 1.787946 s: a systemd restart. It was the deployer installing tree `36f06177a8899162865e17157d57d643c58e1adc` at 21:02:34.754033Z, as TZ-60's report prints at its lines 92–99. This session did not read that part of the deploy journal.
  - 2026-10-04T17:31:21.445930Z → 17:31:27.821910Z, 6.375980 s: `connection lost (WebSocketConnectionClosedException)`.
  - 2026-10-05T12:26:39.671943Z → 12:26:41.280507Z, 1.608564 s: the deployer's restart at `T3`.
  - 2026-10-06T07:56:00.198007Z → 07:56:06.543998Z, 6.345991 s: `connection lost (WebSocketConnectionClosedException)`.
  - 2026-10-07T07:26:06.779983Z → 07:26:13.133294Z, 6.353311 s: `planned refresh after 84600 s`. That is 84 600 s after the 06.10 07:56:06 reconnect.

  Every reconnect answered `REGISTER` and `SUBSCRIBE` with `SUCCESS` in the same journal second. No `subscribe answer` with data other than `SUCCESS` appears, and no `ping failed`, `close frame`, `connect failed` or `data_messages=` line appears either.

## Validation

- **V1. The program: met.** The MD5 `78f37d1f2c37b58452c43e1afba7fa72` equals the dictated one, and there are 274 lines (A2.4). A3 exited **0**. Its first line is `journal lines 42, unparsed 0; records in file 12, unparseable 0, at or after T1 12`, so the three counts are 42, 12 and 12, and none is zero. There was no `EMPTY INPUT`.
- **V2. The negative control: met, with a caveat.** The script printed `NEGATIVE CONTROL (no records): R/R~ rows 7, flipped to M/G 7; M/G rows 0, unchanged 0; control unmatched; up intervals 6 unchanged True`.
  - Every `R`/`R~` row flipped (7 of 7).
  - The control stayed `unmatched`.
  - The up intervals are unchanged (`True`).
  - The «M/G must not move» half compared **0** rows, because this reading has no `M` or `G` post. That half is a check over an empty set on this run (inv. 22). It is reported here, not counted as a pass (Remaining Risks R-3).
- **V3. Nothing touched: met.** After A3, `systemctl show crypto-announce.service -p NRestarts -p ExecMainPID` read `NRestarts=0` and `ExecMainPID=34888`, equal to A2.2's. A second `systemctl list-unit-files 'crypto-*' --no-pager` gave output identical to A1's (`diff` exit 0, "list-unit-files identical to A1's"), read at 2026-10-07T22:30:43Z.
- **V4. Scope: met.** `git status --porcelain | wc -l` in the session's checkout returned `0` before this report was written. The one file this session adds to the repository is this report.
- **§9. Nothing left behind: met.** `rm -rf /root/tz61`, then `test ! -e /root/tz61 && echo gone` → `gone`.
- **The uncovered seconds (report line 5).** These were computed in bash integer arithmetic over microseconds, from the journal timestamps printed above. `date -u -d` converted each stamp to epoch seconds. The six gaps listed under `## Implementation Summary` sum to **23.988327 s**. The span `T1`–`R` is 352 328.000000 s, and the up intervals cover 352 304.011673 s. The script's `seconds` column truncates each interval to an integer (1516 + 73724 + 68111 + 70158 + 84600 + 54191 = 352 300), and at that precision the uncovered figure is 28 s.

## Test Results

| Check | Comparisons | Result |
|---|---:|---|
| A0 known answers | 5 (hostname, 2 × is-active, clone, uid) | 5 equal |
| §5 anchors (map table rows 7) | 7 | 7 present, 7 identical to the TZ's rows |
| §0 file table | 4 files × (lines, MD5) | 8 equal |
| Added-files table | 5 files × (lines, MD5), plus 1 version line | 11 equal |
| A1.1 ancestry | 1 | exit 0 |
| A1.2 known answers | marker, tree, 1 install line, 2 preceding lines, 11 unit files, 2 states | all equal |
| A2.2 known answers | 2 | 2 met |
| A2.4 MD5 and line count | 2 | 2 equal |
| A3 exit | 1 | 0 |
| K1 / K2 / K3 | 3 + 1 + 5 (record present, catalogName, publishDate minute, outcome, alert line count) | 9 met |
| V2 flips | 7 | 7 flipped. «Unchanged» half 0 of 0 (vacuous). Control held. Intervals held. |
| V3 | 2 values + 1 listing | 3 equal |
| V4 | 1 | 0 lines |

## Deviations

- **D-1, gate scratch under `/tmp`.** §4 authorises one scratch path on the VPS, `/root/tz61`. The TZ orders its creation at A2.1, after A1's gate. The gate and A1.2 wrote these files to `/tmp`:
  - copies of repository text: `map.md`, `map0.md`, `tz61.md`, `map_anchors.txt`, `tz_anchors.txt`, `map_files.txt`, `tz_files.txt`;
  - the session's own read-only outputs: `tz61-units-before.txt` (A1.2's `list-unit-files`), `tz61-show-before.txt` (A2.2's `systemctl show`) and `tz61-R.txt` (`R`).

  None holds a credential or a record's `body`. All ten were removed with `rm -f` together with §9's step: `ls /tmp/map.md /tmp/map0.md /tmp/tz61.md /tmp/map_anchors.txt /tmp/tz_anchors.txt /tmp/map_files.txt /tmp/tz_files.txt /tmp/tz61-units-before.txt /tmp/tz61-show-before.txt /tmp/tz61-R.txt 2>&1 | grep -c 'No such file'` → `10`.
- **D-2, two extra files in `/root/tz61`.** `a3.out` held A3's output, written so that this report could carry it byte for byte and not by transcription. `units-after.txt` held V3's second `list-unit-files`. Both lived only inside the authorised directory and went with it at §9.
- **D-3, tools beside the script.** §6 rule 5 allows Python 3.12's standard library and bash, and names §12.3's script as the one program the TZ runs. The gate, A2.4's extraction and the gap sum used ordinary shell utilities on text: `git show`, `grep -F`, `sed`, `awk`, `diff`, `md5sum`, `wc`, `stat` and `date -u -d`. No other Python ran, and no `claude` binary ran. The session's only network reads were `git fetch` and, at the report's commit, `git push`.

## Pre-existing Issues

None found in what this TZ read.

## Remaining Risks

- **R-1, the reference is a lower bound and is thin.** Seven classed posts cover four days. The channel relayed 7 of the 12 records the stream holds since `T1`. A publication the channel did not relay and the stream also missed cannot be seen by this reading, so `W1` says the stream missed none of the seven. It does not say the stream misses nothing.
- **R-2, a listing-catalogue record with no ticker in its title cannot alert.** Record #6 (`New Cryptocurrency Listing`, «Binance Futures Will Launch Multiple TradFi USDⓈ-Margined Perpetual Contracts (2026-10-06)») is `none recorded`, because `match_title` matches tickers only. Whether such a record should reach the owner belongs to the alert rule, which §5 keeps out of this TZ.
- **R-3, half of V2 had nothing to compare.** With no `M` or `G` post, «every post classed `M` or `G` must NOT move» held over 0 rows. On this reading only the flip half (7 of 7) and the control and interval halves are controls.
- **R-4, the owner's «silence» is the alert rule's output, not the stream's.** 12 records arrived and 1 alert was sent. Whether the other 11 should have reached the chat is not decided here (§5).

## Commit

Report, on `main`:

```
TZ-61: report — the announcement stream's record against Binance's own channel
```

Contents: `CryptoReports/TZ-61-vps-stream-against-channel-report.md`.

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

## CI Execution

None ran from this session, and there is no implementation to gate. `.github/workflows/main.yml` was read on `origin/main` before the report was written. Its `push` filter is the allow-list `paths: ['main.py', '.github/workflows/main.yml']`. `bench.yml`'s `push` carries `paths-ignore` including `'**.md'`. `calib.yml`'s `push` names only `claude/**` branches and two paths. `journal.yml` and `backtest_bench.yml` carry no `push` trigger. This report's path matches none of these push filters.

## Final Repository State

The checkout the fingerprints were taken against is `f7d5cded85f26b376d1ad6291299aad88ede3dd1`, which equalled `origin/main` after `git fetch --all --prune`. It is a harness worktree whose branch was at that commit, with `git status --porcelain` at 0 lines before this report was written.

The VPS outside the repository is as A1 found it:

- the same 11 unit files and states (V3);
- `crypto-announce.service` at `NRestarts=0`, `ExecMainPID=34888`;
- `/root/tz61` gone, and the `/tmp` files of D-1 gone.

No unit changed state, no run was started, requested or stopped, and nothing under `/etc/crypto-auto/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or `/var/spool/crypto-auto` was written. `announcements.jsonl`, the two journals and the marker were only read. No credential was read, so none can appear in anything this session wrote.

## Fingerprints

The gate read `SYSTEM-MAP-CRYPTOCALCUL.md` and the TZ from `origin/main` with `git show`. It cut the map's anchor table by its structure: every `|` row after the `|---` separator that follows `| Anchor | Exact string that must be present |`, up to the first line not starting with `|`. It cut the TZ header's table the same way. `diff` of the two cuts was empty. Each anchor was matched with `grep -F -m1 -o -- <anchor>` against the map.

- Revision string, the first in `## 0. Fingerprint` (map line 17): `**Revision 2026-10-07-a.**`. The TZ requires `**Revision 2026-10-07-a.**`. They are equal.
- **Map anchor table rows: 7. Compared: 7. Passed: 7.** The TZ header's anchor rows: 7.

| Anchor | TZ row identical | `grep -F -m1 -o` exit | Text the match returned | Heading line in map |
|---|---|---:|---|---:|
| revision | yes | 0 | `**Revision 2026-10-07-a.**` | 17 |
| direction engine | yes | 0 | `### 3.12 Direction engine — veto cascade` | 1506 |
| catalyst registry | yes | 0 | `### 3.15 Catalyst registry` | 1896 |
| exhaustion measure | yes | 0 | `### 3.16 List exhaustion — the day-range measure` | 1993 |
| analytical engine | yes | 0 | `## 11. Analytical engine` | 3008 |
| squeeze block | yes | 0 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2160 |
| newest invariant | yes | 0 | `72. **A write that fails leaves this run's product or nothing` | 2702 |

Files at `origin/main` (`f7d5cde`):

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 3252 | `3ae97a5ebb96a92a97f542fcb9b15166` | 3252 / `3ae97a5e…`, equal (reported, not enforced) |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | equal; version line `**Version 26.**` |
| `vps/announce.py` | 405 | `cb4f9dfc6e3a428283652c4d21468af5` | equal |
| `vps/bot.py` | 442 | `d1ebb118c78413f62418dd1c331f9196` | equal |
| `vps/common.py` | 364 | `62e3e688cfce21e3e9887e057e461fef` | equal |
| `vps/cleanup.py` | 110 | `5772afa56f9e3432346672f692527589` | equal |

`origin/main:vps` is `81c33f881d4728eda33444e7840ecf9110d616d3`. It equals the tree this TZ was written against and the deployed marker.
