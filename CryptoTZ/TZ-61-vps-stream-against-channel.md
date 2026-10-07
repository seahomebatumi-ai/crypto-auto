# TZ-61 — On the VPS, read-only: the announcement stream's record against Binance's own channel

**Canonical filename:** `CryptoTZ/TZ-61-vps-stream-against-channel.md`
**Report:** `CryptoReports/TZ-61-vps-stream-against-channel-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the announcement stream. **A0 stops
BLOCKED on any other machine, before the gate and before any other work.**
**Class:** report-only TZ (contract §8) — it authorises exactly one written file, its own report.
**Model:** Opus
**Previous TZ:** TZ-60, COMPLETED and merged at `6e58aea` on 05.10.2026; its report is on `main`.
**Written against:** contract v26, map `2026-10-07-a`, methodology `2026-10-05-a`, and `main` at
`ce684bb` — its `vps` tree `81c33f881d4728eda33444e7840ecf9110d616d3` — read by the Architect from the
repository on 07.10.2026. Map §10 row «The engine's exchange-announcement read is a path its own §6
forbids», with the decision of `2026-10-07-a`, is what this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-07-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-07-a.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | its version line reads `**Version 26.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `vps/announce.py` | 405 | `cb4f9dfc6e3a428283652c4d21468af5` | reported; a different file is a finding, never a block |
| `vps/bot.py` | 442 | `d1ebb118c78413f62418dd1c331f9196` | reported; as above |
| `vps/common.py` | 364 | `62e3e688cfce21e3e9887e057e461fef` | reported; as above |
| `vps/cleanup.py` | 110 | `5772afa56f9e3432346672f692527589` | reported; as above |

The map itself: 3252 lines, MD5 `3ae97a5ebb96a92a97f542fcb9b15166` — reported, not enforced. The tree
`origin/main:vps` is reported beside them; `81c33f881d4728eda33444e7840ecf9110d616d3` is the one this TZ
was written against, and a different one is a finding, never a block.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened, the `claude` binary is not
run, and no connection to Binance or to Telegram is opened:** the stream is read from its own record and
journal, and the reference is §12.1, frozen in this text.

---

## 2. Contract, map and code text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section or file named.

> A **report-only TZ** authorises exactly one written file — its own report — on the `CryptoReports/**` direct-push path.

— contract §8.

> **No value is ever printed, logged, committed or quoted**

— contract §7 item 6. This TZ reads no credential; the rule is quoted because the journals it reads are
printed.

> an implementation session that starts either for a measurement its TZ names never reads, relays or edits the answer that run publishes

— contract §1. Of the bot's journal only its `kind=alert` delivery lines are read.

> a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work

— map §10, row «The assistant's build sequence».

> so a post absent from a subscribed stream is a miss and an empty channel proves nothing

— map §10, row «The engine's exchange-announcement read is a path its own §6 forbids».

> TZ-61 reads the stream's whole record against the posts of 02.10–07.10 frozen in its own text, with no fetch of its own

— map §10, the same row.

> A list match → A1; a perpetual match in a listing catalogue → A1; anything else is recorded only.

— `vps/announce.py`, the docstring of `act`. It is why most records never reach the owner's chat.

---

## 3. What is read, and why

The owner asks why the announcement stream is silent while its subscription is confirmed. TZ-60 classed it
`D0`, «silent», against the exchange's announcement sitemap, and the map withdraws that verdict at
`2026-10-07-a`: both of TZ-60's windows lay inside two and a half days in which Binance published no English
announcement, and the sitemap's `new=` counts entries, not publications. **This TZ answers the question on
a reference that can be joined to the stream:** each post of Binance's own English channel against the
stream's record by title, the stream's connection read from its own journal, and each record's alert outcome
read from the same journal, because a record reaches the owner's chat only on the match quoted in §2.

---

## 4. Scope

### Files to Modify

None.

### Files to Create

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- the scratch directory `/root/tz61`, mode `0700`, holding §12.3's script and the two journal extracts of
  A2, and gone at the end;
- reading, never writing: the journals of `crypto-deploy.service`, `crypto-announce.service` and
  `crypto-bot.service`; `/var/lib/crypto-auto/deployed-vps-tree`; `/var/lib/crypto-auto/announcements.jsonl`
  — every field but `body`, which is never printed; `systemctl` state; `dpkg-query`'s record of
  `python3-websocket`.

**No unit is started, stopped, restarted, enabled or disabled; no run is started, requested or stopped;
and nothing under `/etc/crypto-auto/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or
`/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The cause of a miss.** Under `W0` the report names each missed post and the connection around it; what
  the stream did with it is the next TZ's, written on this reading.
- **The alert rule** (§2): its outcomes are read and never changed.
- **Admitting the stream's record into the methodology** — the Architect's edit (map §10).
- **The list reader's removal** from `vps/exchange.py` (map §10, the same row).
- **The size.** The run unit's journal is not read here.
- **Any file in the repository but the report.**

---

## 6. Rules — binding in every stage

1. **No model session**, and the `claude` binary is not run.
2. **No unit changes state** because of this session: `systemctl` and `journalctl` are used to read.
3. **The session's own network reads are `git`'s, and nothing else.** The reference is §12.1.
4. **A record's `body` is never printed.** Its `title` is printed in full: it is the exchange's own public
   headline and the join key.
5. **Python 3.12's standard library and bash only.** §12.3's script is the one program this TZ runs.
6. **Time is UTC everywhere,** every `journalctl` runs under `TZ=UTC`, and every `--since` and `--until`
   names `UTC`.
7. **Nothing of a run's answer is read:** of `crypto-bot.service`'s journal, only lines carrying
   `kind=alert`.

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`; `systemctl
  is-active crypto-bot.service crypto-exchange.service`; `test -d /srv/crypto-auto/.git && echo clone`; `id
  -u cryptorun`. **Known answers:** `vultr`; `active` twice; `clone`; `995`. **Derived:** TZ-60's report
  read exactly these on this host at 2026-10-05T10:40:16Z. **Any other answer: BLOCKED.** The session writes
  a report carrying A0's lines and its own `hostname`, commits it to `main`, and does nothing else (map §10,
  quoted in §2).
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git merge-base --is-ancestor c019a5b657ee778396f52ef1598b79ee82d587d4 origin/main` → exit 0.
     **Exit 1: BLOCKED** — TZ-60's implementation is not merged, and this TZ is written against its tree.
  2. `git rev-parse origin/main:vps`; `cat /var/lib/crypto-auto/deployed-vps-tree`; `systemctl
     list-unit-files 'crypto-*' --no-pager`; and `TZ=UTC journalctl -u crypto-deploy.service --since
     '2026-10-05 12:21:54 UTC' -o short-iso-precise --no-pager | grep -E 'deploy: (installed vps tree|install
     refused|unsigned)|install: (removed|enabled|disabled|restarted|installed)'`. **Known answers:** the marker equals
     `origin/main:vps`, `81c33f881d4728eda33444e7840ecf9110d616d3`; the journal carries exactly one `deploy:
     installed vps tree` line, for that tree, and before it `install: enabled crypto-stop.path` and
     `install: restarted crypto-announce.service`; `list-unit-files` lists 11 unit files, `crypto-stop.path`
     `enabled` and `crypto-stop.service` `static` among them. **Derived:** `git rev-parse 6e58aea:vps`
     returns that tree, and `6e58aea` — TZ-60's merge — is dated 2026-10-05T12:21:54Z, with no later commit
     changing `vps/`; `vps/manifest` lists `crypto-stop.path`, and `vps/install.sh` installs every file of
     `vps/units` (eleven, two of them TZ-60's), enables every listed unit and then restarts every listed
     service, each step logged through `say` as TZ-60's A1 printed it; the deployer ticks every five
     minutes (`crypto-deploy.timer`). **Its time is `T3`.** A missing line is a finding, never a block, and
     the report's first line says whether the STOP stands installed.
- **A2. The stream's own record.**
  1. `date -u +%FT%TZ` — the reading instant `R`, the script's first argument; `<R′>` below is the same
     instant written `YYYY-MM-DD HH:MM:SS`, the form `journalctl` takes. Then `install -d -m 0700 /root/tz61`.
  2. `systemctl show crypto-announce.service -p ActiveState -p SubState -p NRestarts -p
     ActiveEnterTimestamp -p ExecMainPID`; `dpkg-query -W -f='${Version}\n' python3-websocket`; and `TZ=UTC
     journalctl -u crypto-announce.service -o short-iso-precise --no-pager | head -1` — how far back the
     stream's journal reaches. **Known answers:** `ActiveState=active`; the first line is dated at or before
     2026-10-03T20:37:17Z. **Derived:** TZ-60's A3 read the unit active and its journal from that instant
     on, and the unit carries `Restart=always`. A later first line is a finding: every window before it
     classes `G` under §12.2, never `M`.
  3. `TZ=UTC journalctl -u crypto-announce.service --since '2026-10-03 20:37:17 UTC' --until '<R′> UTC' -o
     short-iso-precise --no-pager > /root/tz61/announce.journal` and `TZ=UTC journalctl -u
     crypto-bot.service --since '2026-10-03 20:37:17 UTC' --until '<R′> UTC' -o short-iso-precise --no-pager
     | grep -F 'kind=alert' > /root/tz61/bot.journal`, each followed by `wc -l` of its file.
  4. §12.3's script written to `/root/tz61/tz61_join.py` and checked with `md5sum` → **`78f37d1f2c37b58452c43e1afba7fa72`**
     and `wc -l` → **274**. **A different MD5 is BLOCKED for A3:** the file is not the dictated program.
- **A3. The join.** `python3 -I /root/tz61/tz61_join.py <R> /root/tz61/announce.journal
  /root/tz61/bot.journal /var/lib/crypto-auto/announcements.jsonl`, its exit code, and its output printed in
  full in the report. **Known answers:**
  - **K1:** three records whose `publishDate` is 2026-10-05T02:00:01Z, 03:00:01Z and 09:00:01Z, each
    `present, Latest Activities`. **Derived:** TZ-60's A3.5 read exactly these, and `vps/cleanup.py` drops a
    record only 30 days after its `publishDate` (`ANNOUNCEMENT_MAX_AGE_MS`).
  - **K2 — the control:** post 9021 classes `unmatched`. **Derived:** the channel posted it at
    2026-10-02T09:02:01Z, 35 hours before the stream subscribed at `T1`; the stream delivers on publication
    and holds nothing older, and TZ-60 read the whole file as three records of 05.10. **`matched` makes the
    verdict `void`:** the join is broken and nothing it classed stands.
  - **K3:** one record titled `Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards!`,
    `catalogName` `Latest Activities`, `publishDate` inside [2026-10-07T09:00:00Z, 09:01:00Z), outcome `list
    alerted`; and one bot alert line in the same minute. **Derived:** the owner's screenshot of his chat, sent
    to the Architect on 07.10.2026, shows at 13:00 the message «⚡ Binance · 13:00 Тбилиси · Latest
    Activities: Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards!» — `common.A1`, whose time
    is the record's `publishDate` in Asia/Tbilisi, UTC+4; `announce.act` writes `A1` only on the matches
    quoted in §2, and `BNB` is a name of `tokens[]` (`common.read_tokens` on `index.html` at `ce684bb`:
    thirty names), so the match is `list`; the bot long-polls every 10 s (`bot.POLL_TIMEOUT_S`) and the
    message's own time in the chat is 13:00. A miss of any part of K3 is a finding, and A3's output is
    still printed in full.

  **The verdict and the classes of posts 9022–9028 are not registered:** they are what this TZ exists to
  read.

---

## 8. Validation

- **V1. The program.** A2.4's MD5 and line count equal; A3 exits 0 and its first line counts journal lines,
  records in the file and records at or after `T1`, none of them zero — an `EMPTY INPUT` exit 2 is a
  finding and the verdict is `open`.
- **V2. The negative control** (inv. 68), printed by the script's `NEGATIVE CONTROL` line: with every record
  removed, every post classed `R` or `R~` must FLIP to `M` or `G`, every post classed `M` or `G` must NOT
  move, the control must stay `unmatched` and the up intervals must stay unchanged (`True`). Any other
  outcome is a finding beside the verdict.
- **V3. Nothing touched.** `systemctl show crypto-announce.service -p NRestarts -p ExecMainPID` read again
  after A3 equals A2.2's — a difference is a finding, beside the session's own commands showing it caused
  none; `systemctl list-unit-files 'crypto-*' --no-pager` after A3 equals A1's.
- **V4. Scope.** `git status --porcelain` in the session's clone is empty before the report is written, and
  `main` receives the report and nothing else from this session.

---

## 9. Nothing left behind

`rm -rf /root/tz61`, then `test ! -e /root/tz61 && echo gone`. **Known answer:** `gone`.

---

## 10. The report

Contract §10's template, with the report-only TZ's fixed line under `## Pull Request`. **The first five lines
after `## Status`:**

1. **The STOP** — A1.2's install line for `81c33f881d4728eda33444e7840ecf9110d616d3` and `T3`, or that it is
   absent.
2. **The verdict** — `W1`, `W2`, `W0`, `open` or `void`, with the counts of `R`, `R~`, `M` and `G` and the
   control's class.
3. **The known answers** — K1, K2 and K3, each met or not.
4. **The alerts** — the records at or after `T1`, their count per outcome, and the bot's alert lines since
   `T1`.
5. **The connection** — the number of up intervals, and the seconds between `T1` and `R` that no up
   interval covers.

---

## 11. Commit message

Report, on `main`:

```
TZ-61: report — the announcement stream's record against Binance's own channel
```

---

## 12. Dictated blocks

### 12.1 The reference — Binance's English announcement channel, frozen

Read by the Architect's session at 2026-10-07T17:25:34Z with `curl -sS -m 20
https://t.me/s/binance_announcements` — HTTP 200, 134 372 bytes, MD5 `65884a9dbf2805753c0a218342ed8cf7` —
after `https://t.me/robots.txt` answered 404, so nothing is disallowed. Per post: the post number of its
`data-post` attribute; Telegram's own UTC time, the `datetime` of the post's date link; the article id of
its one `https://www.binance.com/en/support/announcement/detail/<id>` link; and the title, the first
non-empty line of the message text once `<br>` is a line break, tags are removed, entities are unescaped and
whitespace is collapsed. Posts 9021 to 9028 are every post of the page from 9021 on, and the numbers run
without a gap.

| Post | Time (UTC) | Article id | Title |
|---:|---|---|---|
| 9021 | 2026-10-02T09:02:01Z | `7b65382a718f45a4979035bfdb0e6115` | Binance Will Support Scheduled Upgrade for Stock Trading Services - 2026-10-03 |
| 9022 | 2026-10-05T02:04:14Z | `7996a0800e93462b8373ec9f9bc24d09` | Binance Lite Loan Promotion Extended: Enjoy Simple Borrowing with 50% Off Service Fee! |
| 9023 | 2026-10-06T05:02:43Z | `857a0d3d304045c4bf633885d4ec4707` | Binance Will Support Marvell Technology (MRVL) and Oracle Corporation (ORCL) Cash Dividend Distribution via bStocks |
| 9024 | 2026-10-06T09:03:33Z | `2e9c4a3d133947f1b6a24daa43952256` | APAC Exclusive: Win a Fully Hosted Trip to Binance Blockchain Week 2026 |
| 9025 | 2026-10-06T09:32:08Z | `74c7657a53f141e8b2d584bf44e6dd87` | Update on the Collateral Ratio Under Cross Margin and Portfolio Margin (2026-10-09) |
| 9026 | 2026-10-07T03:02:46Z | `9c34999b27234dfe9c43d2ac33cebde4` | Binance Exchange Adds JPMorgan Chase (JPMB), Eli Lilly (LLYB), Securitize Corp (SECZB) and StablecoinX Inc (USDEB) bStocks Trading Pairs on Binance Spot/Convert - 2026-10-07 |
| 9027 | 2026-10-07T04:01:38Z | `a1a7996170f246da90ea49f199a61bcd` | Binance Will Add 4 bStocks Tokenized Securities as Collateral Asset - 2026-10-07 |
| 9028 | 2026-10-07T08:01:40Z | `b109477116f6463a91151946e9ac0fdf` | Binance Has Completed the Stargate Finance (STG) Token Merge to LayerZero (ZRO) |

**Derivation of the role of each row.** Post 9021 is the control (K2). Posts 9022 to 9028 are the classed
set: each was posted after `T1` and is a publication the stream should have carried if it was subscribed
when it was published. The channel relays an announcement minutes after it is published — every post above
lands one to four minutes after an hour or a half hour — and it is a subset: on 05.10 it posted once, while
TZ-60 read three records of that day in the stream. The engine's own day log of 06.10 names article `74c7657a…`, post 9025, on the exchange's own list.

### 12.2 The classes and the verdict

```
T1           = 2026-10-03T20:37:17Z: crypto-announce.service first answered SUBSCRIBE/SUCCESS on TZ-58's
               tree at 20:37:18Z (TZ-60's A3)
R            = A2.1's reading instant
up interval  = from a journal line «announce: subscribe answer <json>» whose json has data SUCCESS, to the
               first later line that is a systemd line of the unit, a «subscribe answer» whose data is not
               SUCCESS, or begins «announce: connection lost», «announce: close frame», «announce: planned
               refresh», «announce: ping failed», «announce: connect failed», «announce: key » or
               «announce: data_messages=» — or to R
N(title)     = every run of whitespace one space, stripped
Q(title)     = the letters and digits alone, case-folded
for each post p of 12.1 with time t_p:
  R          = some record of the file has N(title) equal to the post's
  R~         = no R, and some record has Q(title) equal to the post's: printed with both titles
  M          = neither, and one up interval covers the whole of [t_p − 1800 s, t_p]
  G          = neither, and no up interval covers it
  the control, post 9021, classes matched (R or R~) or unmatched, and is in no count
void         = the control is matched
W1 — delivers = not void, and every classed post is R or R~
W2 — gaps    = not void, no M, at least one G
W0 — misses  = not void, at least one M: the stream was subscribed and recorded nothing for a publication
open         = no classed post
outcome      = per record at or after T1: the «match=<class> <outcome>» of the earliest unused
               «announce: data catalogId=<id> …» line whose time lies in [received − 1 s, received + 5 s]
               and whose id equals the record's catalogId; «-» when none
```

**Derivations.** The journal lines and the record's fields are `vps/announce.py`'s own, as TZ-60 printed
them: `connect` logs the `SUBSCRIBE` answer, `frames` logs every loss, close frame, planned refresh and
failed ping, `main` logs `key` at each start and `data_messages=` at each exit, and the service's data line
is `announce: data catalogId=%s match=%s %s lag_ms=%s`, written right after the record. **Every closing
event shortens an up interval and never lengthens one, so an unclear connection classes `G` and never `M`:**
a miss is asserted only where the stream was subscribed throughout. The window of 1 800 s is wider than the
channel's relay delay seen in §12.1. `N` is the join; `Q` absorbs a dash, quote or emoji the relay may
render differently, and its rows print both titles for the Architect. **No class is registered for posts
9022–9028.**

### 12.3 The script — `/root/tz61/tz61_join.py`

The file is exactly the block's lines, each ending in a newline: 274 lines, ASCII only, MD5
`78f37d1f2c37b58452c43e1afba7fa72`. **Probed:** the Architect's session ran it on a fixture built from
TZ-60's journal lines and record shape — seven classed posts covering `R`, `R~`, `M` and `G`, a control
planted as matched, and an empty journal — and it printed `W0`, `W2`, `W1`, `void` and `EMPTY INPUT` with
exit 2 on the five, and the negative control flipped every `R` and `R~` and moved nothing else.

```python
#!/usr/bin/env python3
"""TZ-61 section 12.3: the announcement stream's record against Binance's own channel.

    python3 -I tz61_join.py <R> <announce.journal> <bot.journal> <announcements.jsonl>

Reads the three files and the reference below, writes nothing, prints the tables and
the verdict of TZ-61 section 12.2. Python 3.12's standard library only."""
import json
import re
import sys
from datetime import datetime, timedelta, timezone

T1 = datetime(2026, 10, 3, 20, 37, 17, tzinfo=timezone.utc)
WINDOW = timedelta(seconds=1800)
JOIN = timedelta(seconds=5)
# TZ-61 section 12.1: post, Telegram's own time, the article id of the post's link, the title.
REFERENCE = [
    (9021, "2026-10-02T09:02:01+00:00", "7b65382a718f45a4979035bfdb0e6115",
     "Binance Will Support Scheduled Upgrade for Stock Trading Services - 2026-10-03"),
    (9022, "2026-10-05T02:04:14+00:00", "7996a0800e93462b8373ec9f9bc24d09",
     "Binance Lite Loan Promotion Extended: Enjoy Simple Borrowing with 50% Off Service Fee!"),
    (9023, "2026-10-06T05:02:43+00:00", "857a0d3d304045c4bf633885d4ec4707",
     "Binance Will Support Marvell Technology (MRVL) and Oracle Corporation (ORCL) Cash Dividend Distribution via bStocks"),
    (9024, "2026-10-06T09:03:33+00:00", "2e9c4a3d133947f1b6a24daa43952256",
     "APAC Exclusive: Win a Fully Hosted Trip to Binance Blockchain Week 2026"),
    (9025, "2026-10-06T09:32:08+00:00", "74c7657a53f141e8b2d584bf44e6dd87",
     "Update on the Collateral Ratio Under Cross Margin and Portfolio Margin (2026-10-09)"),
    (9026, "2026-10-07T03:02:46+00:00", "9c34999b27234dfe9c43d2ac33cebde4",
     "Binance Exchange Adds JPMorgan Chase (JPMB), Eli Lilly (LLYB), Securitize Corp (SECZB) and StablecoinX Inc (USDEB) bStocks Trading Pairs on Binance Spot/Convert - 2026-10-07"),
    (9027, "2026-10-07T04:01:38+00:00", "a1a7996170f246da90ea49f199a61bcd",
     "Binance Will Add 4 bStocks Tokenized Securities as Collateral Asset - 2026-10-07"),
    (9028, "2026-10-07T08:01:40+00:00", "b109477116f6463a91151946e9ac0fdf",
     "Binance Has Completed the Stargate Finance (STG) Token Merge to LayerZero (ZRO)"),
]
CONTROL = 9021
K1 = ("2026-10-05T02:00:01Z", "2026-10-05T03:00:01Z", "2026-10-05T09:00:01Z")
K3_TITLE = "Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards!"
K3_FROM = datetime(2026, 10, 7, 9, 0, 0, tzinfo=timezone.utc)
CLOSERS = ("announce: connection lost", "announce: close frame", "announce: planned refresh",
           "announce: ping failed", "announce: connect failed", "announce: key ",
           "announce: data_messages=")
SUBSCRIBE = "announce: subscribe answer "
LINE = re.compile(r"^(\d{4}-\d\d-\d\dT\S+) \S+ (\S+?): (.*)$")
DATA = re.compile(r"^announce: data catalogId=(\S+) match=(\S+) (\S+) lag_ms=(\S+)$")


def norm(text):
    """N: every run of whitespace one space, stripped."""
    return " ".join(str(text or "").split())


def reduced(text):
    """Q: the letters and digits alone, case-folded."""
    return "".join(ch for ch in str(text or "").casefold() if ch.isalnum())


def utc(when):
    return when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def from_ms(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def read_journal(path):
    out, skipped = [], 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            m = LINE.match(raw.rstrip("\n"))
            if not m:
                skipped += 1
                continue
            out.append((datetime.fromisoformat(m.group(1)), m.group(2), m.group(3)))
    return out, skipped


def up_intervals(lines, end):
    """[(opened, closed, closing text)]: a SUBSCRIBE answer whose data is SUCCESS opens,
    the next CLOSERS line, non-SUCCESS SUBSCRIBE answer or systemd line closes, R closes
    the last."""
    out, opened = [], None
    for when, ident, msg in lines:
        if msg.startswith(SUBSCRIBE):
            try:
                answer = json.loads(msg[len(SUBSCRIBE):])
            except ValueError:
                answer = None
            if isinstance(answer, dict) and answer.get("data") == "SUCCESS":
                if opened is None:
                    opened = when
                continue
            if opened is not None:
                out.append((opened, when, msg))
                opened = None
            continue
        if opened is not None and (ident.startswith("systemd") or msg.startswith(CLOSERS)):
            out.append((opened, when, msg))
            opened = None
    if opened is not None:
        out.append((opened, end, "R"))
    return out


def up_through(intervals, start, stop):
    return any(o <= start and stop <= c for o, c, _ in intervals)


def read_records(path):
    out, bad = [], 0
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                doc = json.loads(raw)
            except ValueError:
                bad += 1
                continue
            if not isinstance(doc, dict) or not isinstance(doc.get("received_ms"), int):
                bad += 1
                continue
            out.append(doc)
    return out, bad


def join_outcomes(records, lines):
    """Each record's 'announce: data' line: the earliest unused one inside
    [received, received + 5 s] carrying the record's catalogId."""
    data = [(when, DATA.match(msg)) for when, _ident, msg in lines]
    data = [(when, m) for when, m in data if m]
    used, out = set(), {}
    for i, rec in enumerate(records):
        got = from_ms(rec["received_ms"])
        for j, (when, m) in enumerate(data):
            if j in used or not (got - timedelta(seconds=1) <= when <= got + JOIN):
                continue
            if m.group(1) != str(rec.get("catalogId")):
                continue
            used.add(j)
            out[i] = "%s %s" % (m.group(2), m.group(3))
            break
    return out, len(data), len(data) - len(used)


def classify(records, intervals):
    rows = []
    for post, tp_text, article, title in REFERENCE:
        tp = datetime.fromisoformat(tp_text)
        exact = [r for r in records if norm(r.get("title")) == norm(title)]
        near = [] if exact else [r for r in records if reduced(r.get("title")) == reduced(title)]
        if post == CONTROL:
            cls = "matched" if exact or near else "unmatched"
        elif exact:
            cls = "R"
        elif near:
            cls = "R~"
        elif up_through(intervals, tp - WINDOW, tp):
            cls = "M"
        else:
            cls = "G"
        hit = (exact or near or [None])[0]
        window = [r for r in records if isinstance(r.get("publishDate"), int)
                  and tp - WINDOW <= from_ms(r["publishDate"]) <= tp]
        rows.append((post, tp, article, title, cls, hit, window))
    return rows


def verdict(rows):
    if any(r[4] == "matched" for r in rows):
        return "void"
    classes = [r[4] for r in rows if r[0] != CONTROL]
    if not classes:
        return "open"
    if "M" in classes:
        return "W0"
    if "G" in classes:
        return "W2"
    return "W1"


def cell(text):
    return str(text).replace("|", "\\|")


def main(argv):
    end = datetime.fromisoformat(argv[1].replace("Z", "+00:00"))
    lines, skipped = read_journal(argv[2])
    bot, _ = read_journal(argv[3])
    every, bad = read_records(argv[4])
    records = [r for r in every if from_ms(r["received_ms"]) >= T1]
    print("journal lines %d, unparsed %d; records in file %d, unparseable %d, at or after T1 %d"
          % (len(lines), skipped, len(every), bad, len(records)))
    if not lines or not every:
        print("EMPTY INPUT")
        return 2

    print("\n### Connection events (every journal line but 'announce: data ')\n")
    for when, ident, msg in lines:
        if not DATA.match(msg):
            print("%s %s %s" % (when.isoformat(), ident, msg))

    intervals = up_intervals(lines, end)
    print("\n### Up intervals\n\n| opened | closed | closed by | seconds |\n|---|---|---|---:|")
    for o, c, why in intervals:
        print("| %s | %s | %s | %d |" % (utc(o), utc(c), cell(why[:60]), (c - o).total_seconds()))

    outcomes, data_lines, unjoined = join_outcomes(records, lines)
    print("\n### Records at or after T1\n\n| # | received | publishDate | lag s | catalogId | catalogName | title | outcome |\n|---:|---|---|---:|---|---|---|---|")
    for i, rec in enumerate(records):
        pub = rec.get("publishDate")
        pub_text = utc(from_ms(pub)) if isinstance(pub, int) else "-"
        lag = "%.3f" % ((rec["received_ms"] - pub) / 1000) if isinstance(pub, int) else "-"
        print("| %d | %s | %s | %s | %s | %s | %s | %s |"
              % (i + 1, utc(from_ms(rec["received_ms"])), pub_text, lag, rec.get("catalogId"),
                 cell(rec.get("catalogName")), cell(norm(rec.get("title"))), outcomes.get(i, "-")))
    print("\ndata lines %d, joined %d, unjoined data lines %d, records with no line %d"
          % (data_lines, len(outcomes), unjoined, len(records) - len(outcomes)))

    rows = classify(every, intervals)
    print("\n### The reference\n\n| post | t_p | class | record publishDate | t_p - publishDate s | candidates in [t_p - 1800 s, t_p] |\n|---:|---|---|---|---:|---|")
    for post, tp, article, title, cls, hit, window in rows:
        pub = hit.get("publishDate") if hit else None
        pub_text = utc(from_ms(pub)) if isinstance(pub, int) else "-"
        ahead = "%d" % (tp - from_ms(pub)).total_seconds() if isinstance(pub, int) else "-"
        cands = "-" if cls in ("R", "unmatched") else "; ".join(
            "%s %s" % (utc(from_ms(r["publishDate"])), norm(r.get("title"))) for r in window) or "none"
        print("| %d | %s | %s | %s | %s | %s |" % (post, utc(tp), cls, pub_text, ahead, cell(cands)))
    counts = {c: sum(1 for r in rows if r[4] == c and r[0] != CONTROL) for c in ("R", "R~", "M", "G")}
    print("\nclassed %d: R %d, R~ %d, M %d, G %d; control %d: %s"
          % (sum(counts.values()), counts["R"], counts["R~"], counts["M"], counts["G"],
             CONTROL, [r[4] for r in rows if r[0] == CONTROL][0]))
    print("VERDICT %s" % verdict(rows))

    empty = classify([], intervals)
    flipped = sum(1 for a, b in zip(rows, empty) if a[0] != CONTROL and a[4] in ("R", "R~") and b[4] in ("M", "G"))
    held = sum(1 for a, b in zip(rows, empty) if a[0] != CONTROL and a[4] in ("M", "G") and b[4] == a[4])
    print("NEGATIVE CONTROL (no records): R/R~ rows %d, flipped to M/G %d; M/G rows %d, unchanged %d; "
          "control %s; up intervals %d unchanged %s"
          % (counts["R"] + counts["R~"], flipped, counts["M"] + counts["G"], held,
             [r[4] for r in empty if r[0] == CONTROL][0], len(intervals),
             up_intervals(lines, end) == intervals))

    print("\n### Known answers\n")
    pubs = {utc(from_ms(r["publishDate"])): r for r in every if isinstance(r.get("publishDate"), int)}
    for stamp in K1:
        rec = pubs.get(stamp)
        print("K1 %s: %s" % (stamp, "present, %s" % rec.get("catalogName") if rec else "ABSENT"))
    minute = timedelta(seconds=60)
    k3 = [(i, r) for i, r in enumerate(records) if reduced(r.get("title")) == reduced(K3_TITLE)
          and isinstance(r.get("publishDate"), int)
          and K3_FROM <= from_ms(r["publishDate"]) < K3_FROM + minute]
    for i, rec in k3:
        print("K3 record: publishDate %s, catalogName %s, title %s, outcome %s"
              % (utc(from_ms(rec["publishDate"])), rec.get("catalogName"), norm(rec.get("title")),
                 outcomes.get(i, "-")))
    if not k3:
        print("K3 record: ABSENT")
    sent = [(w, m) for w, _i, m in bot if "kind=alert" in m and m.startswith("bot: sent ")]
    in_minute = [w for w, _m in sent if K3_FROM <= w < K3_FROM + minute]
    print("K3 alert lines in [2026-10-07T09:00:00Z, 09:01:00Z): %d" % len(in_minute))

    print("\n### Alerts\n")
    tally = {}
    for value in outcomes.values():
        tally[value] = tally.get(value, 0) + 1
    for key in sorted(tally):
        print("outcome %s: %d" % (key, tally[key]))
    print("bot alert lines since T1: %d" % len(sent))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```
