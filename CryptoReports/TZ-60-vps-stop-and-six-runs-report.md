# Implementation Report — TZ-60

## Status

**COMPLETED.** The session ran on the VPS. `hostname` returned `vultr`, and every A0 answer was the known one.

1. **The STOP is built, and C2 and C3 proved it on this host.** C2 read `crypto-stop: stops=1 requests_removed=1 before=active stop_exit=0 reset_exit=1 after=inactive notice=S13`, and the dummy unit was no longer active afterwards. C3 read `crypto-stop: stops=0 requests_removed=0 before=inactive stop_exit=5 reset_exit=1 after=inactive notice=S14`. The STOP takes effect when the deployer installs the merge of pull request #49.
2. **The size is `open`.** Two of the six runs were read. They are class **C** (started 2026-10-04T16:43:11Z) and class **L** (started 17:14:30Z, `api_error_status=429`). Neither is K-oom or K-timeout, and neither is N. Nothing is decided until four more runs are read.
3. **Usage at `high`.** Both runs reached a session. The C run took 64 turns, 1 551.510 s, 97 177 output tokens, 13 026 278 cache-read tokens and 11.0167892 USD. The reference run took 58 turns, 1 238 s, 83 752 output tokens, 11 941 234 cache-read tokens and 10.09 USD. That is +10.3 % turns, +25.3 % time, +16.0 % output, +9.1 % cache-read and +9.2 % cost. The L run took 109 turns, 561.986 s, 36 677 output tokens, 10 052 898 cache-read tokens and 6.8113856 USD before the account's 429.
4. **The stream is `D0`, silent.** Window 1, (2026-10-03T02:02:14Z, 2026-10-04T02:00:57Z], is not covered: list_new 19, stream 0. Window 2, (2026-10-04T02:00:57Z, 2026-10-05T01:58:16Z], is covered: list_new 14, stream 0. The other reading of «stamps g» (the journal read times) is also `D0`, with covered windows of 19/0 and 14/2 (Deviations D-3).
5. **The engine window is `E0`.** [T1, 2026-10-04T16:48:25Z] holds 0 stream records.

The previous TZ is merged. `git merge-base --is-ancestor 9c1af521e0958a95b902b6e19e7c782729a754de origin/main` exited 0: TZ-59's implementation reached `main` through `07126c0`, pull request #48.

## Inbound Filing

None moved. `CryptoTZ/TZ-60-vps-stop-and-six-runs.md` is at its canonical path on `origin/main`, in one copy: 652 lines, blob `988aafa0897834b0834b728d59f8cdb13df1577b`, uploaded in `f8070a2`. It was found after `git fetch --all --prune`. The clone is not shallow: `git rev-parse --is-shallow-repository` returned `false`.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names files under `vps/`. The branch is `tz-60-vps-stop-and-six-runs`, opened from `origin/main` at `f8070a2`.

| Stage | Executed | Outcome |
|---|---|---|
| A0 | yes | all four known answers |
| A1 (§4a 1–6, §5 gate, merge check, deploy lines) | yes | gate passed 7/7. TZ-59 is merged. The marker equals `origin/main:vps`. All three install lines are present. |
| A2 | yes | 2 invocations: C, then L. Size `open`. |
| A3 | yes | **D0**, **E0** |
| B1–B7 | yes | §12.5–§12.11 built |
| C0–C4 | yes | every known answer met; nothing left behind |
| V1–V7 | yes | see `## Validation` |

### A0 — the host, before the gate

`date -u +%FT%TZ` printed `2026-10-05T10:40:16Z` right after the four checks.

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

### A1 — the gate and the installed trees

The gate is under `## Fingerprints`. The rest of A1:

```
$ git merge-base --is-ancestor 9c1af521e0958a95b902b6e19e7c782729a754de origin/main; echo $?
0
$ git rev-parse origin/main:vps
36f06177a8899162865e17157d57d643c58e1adc
$ cat /var/lib/crypto-auto/deployed-vps-tree
36f06177a8899162865e17157d57d643c58e1adc
$ systemctl list-unit-files 'crypto-*' --no-pager
UNIT FILE               STATE   PRESET
crypto-run.path         enabled enabled
crypto-announce.service enabled enabled
crypto-bot.service      enabled enabled
crypto-cleanup.service  static  -
crypto-deploy.service   static  -
crypto-exchange.service enabled enabled
crypto-run.service      static  -
crypto-cleanup.timer    enabled enabled
crypto-deploy.timer     enabled enabled

9 unit files listed.
$ journalctl -u crypto-deploy.service --since '2026-10-03 19:00:00 UTC' -o short-iso-precise --no-pager \
    | grep -E 'deploy: installed vps tree|install: (removed|enabled|disabled|installed)'
2026-10-03T19:36:15.075437+00:00 vultr deploy.sh[3997695]: install: removed crypto-run.timer
2026-10-03T19:36:15.613514+00:00 vultr deploy.sh[3997695]: install: enabled crypto-deploy.timer
2026-10-03T19:36:15.880830+00:00 vultr deploy.sh[3997695]: install: enabled crypto-cleanup.timer
2026-10-03T19:36:16.150123+00:00 vultr deploy.sh[3997695]: install: enabled crypto-exchange.service
2026-10-03T19:36:16.425700+00:00 vultr deploy.sh[3997695]: install: enabled crypto-bot.service
2026-10-03T19:36:16.706545+00:00 vultr deploy.sh[3997695]: install: enabled crypto-run.path
2026-10-03T19:36:17.006954+00:00 vultr deploy.sh[3997695]: install: disabled crypto-announce.service
2026-10-03T19:36:17.133708+00:00 vultr deploy.sh[3997695]: install: installed
2026-10-03T19:36:17.147753+00:00 vultr deploy.sh[3997677]: deploy: installed vps tree c4eef2b1d03991c05a27464038f60d2a3307c14a
2026-10-03T20:37:15.259086+00:00 vultr deploy.sh[4005531]: install: enabled crypto-deploy.timer
2026-10-03T20:37:15.544303+00:00 vultr deploy.sh[4005531]: install: enabled crypto-cleanup.timer
2026-10-03T20:37:15.889514+00:00 vultr deploy.sh[4005531]: install: enabled crypto-exchange.service
2026-10-03T20:37:16.170118+00:00 vultr deploy.sh[4005531]: install: enabled crypto-bot.service
2026-10-03T20:37:16.459042+00:00 vultr deploy.sh[4005531]: install: enabled crypto-run.path
2026-10-03T20:37:16.782380+00:00 vultr deploy.sh[4005531]: install: enabled crypto-announce.service
2026-10-03T20:37:17.026695+00:00 vultr deploy.sh[4005531]: install: installed
2026-10-03T20:37:17.046805+00:00 vultr deploy.sh[4005513]: deploy: installed vps tree 94a55b6f07d6aa6b2290eb3b4646f1740cd1a47e
2026-10-03T21:02:33.164237+00:00 vultr deploy.sh[4009173]: install: enabled crypto-deploy.timer
2026-10-03T21:02:33.439554+00:00 vultr deploy.sh[4009173]: install: enabled crypto-cleanup.timer
2026-10-03T21:02:33.710664+00:00 vultr deploy.sh[4009173]: install: enabled crypto-exchange.service
2026-10-03T21:02:33.988544+00:00 vultr deploy.sh[4009173]: install: enabled crypto-bot.service
2026-10-03T21:02:34.266016+00:00 vultr deploy.sh[4009173]: install: enabled crypto-run.path
2026-10-03T21:02:34.547440+00:00 vultr deploy.sh[4009173]: install: enabled crypto-announce.service
2026-10-03T21:02:34.733762+00:00 vultr deploy.sh[4009173]: install: installed
2026-10-03T21:02:34.754033+00:00 vultr deploy.sh[4009155]: deploy: installed vps tree 36f06177a8899162865e17157d57d643c58e1adc
```

The three trees are installed in the registered order. They match `git rev-parse <merge>:vps` of `075de0e`, `2416e3f` and `07126c0`, which carry those trees with commit times 19:35:23Z, 20:34:35Z and 21:01:10Z on 03.10. This gives:

- **T0 = 2026-10-03T19:36:17.147753Z**
- **T1 = 2026-10-03T20:37:17.046805Z**
- **T2 = 2026-10-03T21:02:34.754033Z**

No line is missing. The marker equals `origin/main:vps`.

### A2 — the runs since T0

The reading instant is **R = 2026-10-05T10:41:28Z** (`date -u +%FT%TZ`). The run unit's journal reaches back to 2026-10-03T10:56:28Z (`journalctl -u crypto-run.service | head -1`), so nothing between T0 and R was rotated away.

A2.2 is printed in full. The pipeline was `journalctl -u crypto-run.service --since '2026-10-03 19:36:17 UTC' --until '2026-10-05 10:41:28 UTC' -o short-iso-precise --no-pager | grep -E 'crypto-run:|systemd\[1\]:'`, then §12.3's rewrite, which replaces `models=<ids>` with `models=[withheld] pinned_present=<yes|no> other_models=<n>` against `run.MODEL` = `claude-opus-5-5`. That gave 17 lines:

```
2026-10-04T16:43:11.949335+00:00 vultr systemd[1]: Starting crypto-run.service - Crypto assistant: one headless analysis run...
2026-10-04T16:43:12.016734+00:00 vultr python3[4112602]: crypto-run: limits unit=crypto-run.service mem_available=389570560 swap_free=2854244352 budget=704643072 memory_max=318767104 memory_swap_max=385875968 set=0
2026-10-04T16:43:12.035804+00:00 vultr systemd[1]: Started crypto-run.service - Crypto assistant: one headless analysis run.
2026-10-04T17:09:16.724382+00:00 vultr python3[4112606]: crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=0 is_error=false num_turns=64 duration_ms=1551510 denials=0 answer_chars=5843
2026-10-04T17:09:16.724950+00:00 vultr python3[4112606]: crypto-run: models=[withheld] pinned_present=yes other_models=1 denied_tools=- subtype=success api_error_status=- terminal_reason=completed stop_reason=end_turn
2026-10-04T17:09:16.726106+00:00 vultr python3[4112606]: crypto-run: memory_max=318767104 memory_swap_max=385875968 mem_available=388734976 swap_free=2854244352 memory_peak=318914560 memory_swap_peak=37048320 input_tokens=118 output_tokens=97177 cache_read_tokens=13026278 cache_creation_tokens=333412 cost_usd=11.016789199999995
2026-10-04T17:09:16.822855+00:00 vultr systemd[1]: crypto-run.service: Deactivated successfully.
2026-10-04T17:09:16.823395+00:00 vultr systemd[1]: crypto-run.service: Consumed 3min 44.276s CPU time.
2026-10-04T17:14:30.024889+00:00 vultr systemd[1]: Starting crypto-run.service - Crypto assistant: one headless analysis run...
2026-10-04T17:14:30.182507+00:00 vultr python3[4116782]: crypto-run: limits unit=crypto-run.service mem_available=439943168 swap_free=2835742720 budget=704643072 memory_max=369098752 memory_swap_max=335544320 set=0
2026-10-04T17:14:30.224809+00:00 vultr systemd[1]: Started crypto-run.service - Crypto assistant: one headless analysis run.
2026-10-04T17:24:37.518367+00:00 vultr python3[4116827]: crypto-run: requests=1 admitted=yes waited_s=30 writer_exit=0 claude_exit=1 is_error=true num_turns=109 duration_ms=561986 denials=0 answer_chars=0
2026-10-04T17:24:37.518888+00:00 vultr python3[4116827]: crypto-run: models=[withheld] pinned_present=yes other_models=1 denied_tools=- subtype=success api_error_status=429 terminal_reason=api_error stop_reason=stop_sequence
2026-10-04T17:24:37.520559+00:00 vultr python3[4116827]: crypto-run: memory_max=369098752 memory_swap_max=335544320 mem_available=441335808 swap_free=2836529152 memory_peak=369098752 memory_swap_peak=8105984 input_tokens=96 output_tokens=36677 cache_read_tokens=10052898 cache_creation_tokens=318562 cost_usd=6.811385600000003
2026-10-04T17:24:37.616386+00:00 vultr systemd[1]: crypto-run.service: Main process exited, code=exited, status=1/FAILURE
2026-10-04T17:24:37.616547+00:00 vultr systemd[1]: crypto-run.service: Failed with result 'exit-code'.
2026-10-04T17:24:37.617139+00:00 vultr systemd[1]: crypto-run.service: Consumed 1min 51.215s CPU time.
```

A2.3, the bot:

```
$ journalctl -u crypto-bot.service --since '2026-10-03 19:36:17 UTC' -o short-iso --no-pager | grep -E 'bot: (sent |updates=)'
2026-10-04T16:43:12+00:00 vultr python3[4009698]: bot: updates=1 acted_total=4 dropped_total=0
2026-10-04T17:09:25+00:00 vultr python3[4009698]: bot: sent 1791133756687-answer-4112606.json kind=answer chunks=2 accepted=2 plain_fallbacks=0
2026-10-04T17:14:30+00:00 vultr python3[4009698]: bot: updates=1 acted_total=5 dropped_total=0
2026-10-04T17:15:05+00:00 vultr python3[4009698]: bot: updates=1 acted_total=6 dropped_total=0
2026-10-04T17:24:40+00:00 vultr python3[4009698]: bot: sent 1791134677477-notice-4116827.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
```

A2.4, the analyst commits, and A2.5, the host:

```
$ git log origin/main --since '2026-10-03 19:36:17 UTC' --format='%h %cI %s' -- analyst/
0d2566d 2026-10-04T17:15:12+00:00 analyst: live.json (vps)
6c9645e 2026-10-04T17:08:41+00:00 analyst: 2026-10-04
b4ff2fc 2026-10-04T16:43:21+00:00 analyst: live.json (vps)
$ grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo; nproc
MemTotal:         978640 kB
MemAvailable:     323632 kB
SwapTotal:       3174396 kB
SwapFree:        2627068 kB
1
```

Every invocation, classed by §12.2. A script applied the definitions and precedence to the 17 lines above:

| start (UTC) | class | memory_max | memory_swap_max | memory_peak | memory_swap_peak | footprint | duration_s | requests | num_turns | input | output | cache_read | cache_creation | cost_usd | pinned_present | other_models |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 2026-10-04T16:43:11.949335Z | **C** | 318767104 | 385875968 | 318914560 | 37048320 | 355962880 | 1564.777 | 1 | 64 | 118 | 97177 | 13026278 | 333412 | 11.016789199999995 | yes | 1 |
| 2026-10-04T17:14:30.024889Z | **L** | 369098752 | 335544320 | 369098752 | 8105984 | 377204736 | 607.496 | 1 | 109 | 96 | 36677 | 10052898 | 318562 | 6.811385600000003 | yes | 1 |

There are no `active` invocations. The first run is C: `claude_exit=0 is_error=false answer_chars=5843`. The second is L: `api_error_status=429` on its second summary line. No higher class applies to it, since it has neither `oom-kill` nor `timeout`, no `stopped by the owner`, and `admitted=yes`.

**The size verdict is `open`.** The six read so far are 2 (C, L). K-oom/K-timeout: 0. N: 0, so there are not more than one. C: 1. That is fewer than six, so this is neither `Z1` nor `Z0`. The host stays as it is, and nothing is decided.

**The registered known answer is met.** Exactly two invocations after T2 read `admitted=yes writer_exit=0`, and the earlier one is class C. The second one's class was not registered. It is **L**: the account's limit stopped it after 109 turns and 562 s of session. Map §10 says such a run «measures nothing about memory and decides nothing about size».

**Usage at `high`** (§12.3). Both invocations start after T2, and both reached a session (`claude_exit` is not `-`). The reference row comes first:

| run | class | num_turns | duration_ms | input | output | cache_read | cache_creation | cost_usd | pinned_present | other_models |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---:|
| reference: 2026-10-03T11:37:53Z, alias `opus`, default effort | C | 58 | 1 238 s | — | 83 752 | 11 941 234 | — | 10.09 | — | — |
| 2026-10-04T16:43:11Z, `claude-opus-5-5` at `high` | C | 64 | 1551510 | 118 | 97177 | 13026278 | 333412 | 11.016789199999995 | yes | 1 |
| 2026-10-04T17:14:30Z, `claude-opus-5-5` at `high` | L | 109 | 561986 | 96 | 36677 | 10052898 | 318562 | 6.811385600000003 | yes | 1 |

The two runs at `high` cost 17.83 USD together. No bar is registered (§12.3), so nothing here is judged.

### A3 — the stream against the list

```
$ systemctl is-active crypto-announce.service crypto-exchange.service
active
active
$ systemctl show crypto-announce.service -p ActiveEnterTimestamp -p NRestarts
NRestarts=0
ActiveEnterTimestamp=Sat 2026-10-03 21:02:34 UTC
$ journalctl -u crypto-announce.service --since '2026-10-03 20:37:17 UTC' -o short-iso --no-pager | grep -E 'announce: (key|subscribe answer|command answer|connect failed|connection lost|close frame|planned refresh|data_messages)'
2026-10-03T20:37:17+00:00 vultr python3[4006064]: announce: key ACCEPTED ipRestrict=true enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableReading=true enableFutures=false enableMargin=false
2026-10-03T20:37:18+00:00 vultr python3[4006064]: announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-03T20:37:18+00:00 vultr python3[4006064]: announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-03T21:02:35+00:00 vultr python3[4009704]: announce: key ACCEPTED ipRestrict=true enableReading=true enableFutures=false enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableMargin=false
2026-10-03T21:02:36+00:00 vultr python3[4009704]: announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-03T21:02:36+00:00 vultr python3[4009704]: announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-04T17:31:21+00:00 vultr python3[4009704]: announce: connection lost (WebSocketConnectionClosedException)
2026-10-04T17:31:27+00:00 vultr python3[4009704]: announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-04T17:31:27+00:00 vultr python3[4009704]: announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
$ journalctl -u crypto-announce.service --since '2026-10-03 20:37:17 UTC' -o short-iso --no-pager | grep -F 'announce: data ' | cut -c1-10 | sort | uniq -c
      3 2026-10-05
$ journalctl -u crypto-exchange.service --since '2026-10-03 20:37:17 UTC' -o short-iso --no-pager | grep -F 'exchange: list'
2026-10-03T20:37:21+00:00 vultr python3[4006053]: exchange: list generation=2026-10-03T02:02:14Z read=2026-10-03T20:37:21Z children=3 articles=8329 new=- gone=- baseline=yes
2026-10-04T02:32:40+00:00 vultr python3[4009692]: exchange: list generation=2026-10-04T02:00:57Z read=2026-10-04T02:32:40Z children=3 articles=8344 new=19 gone=4 baseline=no
2026-10-05T03:02:40+00:00 vultr python3[4009692]: exchange: list generation=2026-10-05T01:58:16Z read=2026-10-05T03:02:40Z children=3 articles=8348 new=14 gone=10 baseline=no
```

A3.4, read with `python3`'s `json`: `generation=2026-10-05T01:58:16Z read=2026-10-05T03:02:40Z children=3 len(articles)=8348`.

A3.5 reads `/var/lib/crypto-auto/announcements.jsonl` one line at a time. No `body` was printed and no `title` outside the engine window:

```
file lines: 3  unparseable: 0  stream records (received_ms >= T1): 3
received 2026-10-05 {'Latest Activities': 3}
lag s: min 1.272 median 1.278 max 1.675 (n=3)
publishDate per record (UTC): 2026-10-05T02:00:01Z, 2026-10-05T03:00:01Z, 2026-10-05T09:00:01Z
```

**Classed by §12.4.** The generations are the `generation=` values of the three list lines, the baseline's included:

| window | (g_{i-1}, g_i] | covered | list_new_i | stream_i |
|---|---|---|---:|---:|
| 1 | (2026-10-03T02:02:14Z, 2026-10-04T02:00:57Z] | no: g_0 is before T1 | 19 | 0 |
| 2 | (2026-10-04T02:00:57Z, 2026-10-05T01:58:16Z] | yes | 14 | 0 |

**D0, silent.** Covered window 2 has `list_new = 14` and `stream = 0`. The stream's whole file holds three records. All were received on 05.10, all are under `Latest Activities`, and the earliest was published at 02:00:01Z, after window 2 closed. So from T1, 2026-10-03T20:37:17Z, to 2026-10-05T02:00:01Z, the stream recorded nothing. Over the same period the list gained 19 and then 14 articles. The connection stayed subscribed throughout: each connect and the one reconnect at 17:31:27Z read `SUBSCRIBE`/`SUCCESS`.

**E0.** The engine window [T1, 2026-10-04T16:48:25Z] holds 0 records. No title is printed.

## Files Created

| File | Lines | MD5 |
|---|---:|---|
| `vps/stop.py` | 75 | `e06bbfc8d8c85bd00be73a11a124cdc2` |
| `vps/units/crypto-stop.path` | 9 | `b85e6e2f1993d3945c18327bf6915276` |
| `vps/units/crypto-stop.service` | 16 | `0d85e3247a98f07f1ac958d32dff7653` |

## Files Modified

| File | Lines before → after | MD5 after |
|---|---|---|
| `vps/common.py` | 329 → 364 | `62e3e688cfce21e3e9887e057e461fef` |
| `vps/bot.py` | 422 → 442 | `d1ebb118c78413f62418dd1c331f9196` |
| `vps/run.py` | 333 → 336 | `beb420d158630b8e5801badf26aee2b4` |
| `vps/install.sh` | 251 → 252 | `eef7e6ac5bfda2b17227f6c40a6767df` |
| `vps/manifest` | 6 → 7 | `4ab0ef7d67fa531eeaad7d0d6e6b7310` |
| `vps/selftest.py` | 817 → 1022 | `40b6a609bbbc3e75acca7614c4241b7a` |

`git diff --stat origin/main...HEAD`: 9 files changed, 418 insertions(+), 53 deletions(-). The branch's `vps` tree is `81c33f881d4728eda33444e7840ecf9110d616d3`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

- **B1 `vps/common.py`** (§12.5). Adds `STOP_DIR = SPOOL_DIR + "/stop"`, `STOP_ACTIVE = "/run/crypto-stop"` and `RUN_UNIT = "crypto-run.service"`. `pending_requests()` lists `REQUESTS_DIR` for a `.req` file not starting with `.`, and a missing directory is false. `request_stop(source)` writes `<created_ms>-<source>-<pid>.stop` with `{"source", "created_ms"}` through `atomic_write` at mode `0o660`, uses the same name-collision loop as `_write_request`, never reads `runs_enabled()`, and returns `requested`. S3 and S4 gain « Остановить: СТОП.». S8 is `"Команды: " + S1 + " · СТОП"`. S12–S15 are added. Every string is `\uXXXX` escapes and equals §12.1 (V3). The docstring names TZ-60 B1 and TZ-60 §12.1.
- **B2 `vps/bot.py`** (§12.6). Adds `STOP_WORDS` and `is_stop` exactly as dictated. `classify` returns `stop` after the `/start` and request tests and before `S8`, with the owner filter and the 600 s age unchanged. The verdict branch moves out of `service()` unchanged into `respond(api, owner, verdict)`, which `service()` calls once per acted update, and gains the `stop` branch after `S8`. `KEYBOARD` is unchanged. The docstring names TZ-60 B2.
- **B3 `vps/run.py`** (§12.7). `on_term` is exactly the dictated body. The docstring names TZ-60 B3, and nothing else in the file moves.
- **B4 `vps/stop.py`** (§12.8). Has `RUNNING`, `consume`, `unit_state`, `choose` and `main`, with steps 1–8 in the dictated order, and `systemctl reset-failed`'s output captured and dropped. It returns 1 under S15 and 0 otherwise. The docstring names TZ-60 and states that the program reads no credential and starts no model.
- **B5** (§12.9). The two units match the dictated text byte for byte.
- **B6** (§12.10). `provision_dirs` gains `dir_as 2770 cryptoauto cryptoauto /var/spool/crypto-auto/stop` after the `requests` line. The header comment's list of units without `[Install]` names `crypto-stop.service`. `vps/manifest` gains `crypto-stop.path` after `crypto-announce.service`.
- **B7 `vps/selftest.py`** (§12.11). Section F gains the eight rows. New section S has items 1–5. Item 4's stub `systemctl` records each argument list as one JSON line and answers `is-active` from a scripted sequence (exit 0 for `active`, 3 otherwise, as systemd does), and every other command with exit 0. Item 5's stub `claude` sends SIGTERM to its parent and sleeps 30 s. `subprocess.run` kills it on the way out, and no stub process was left (`pgrep` found none). To share section O's fixtures, their construction moved into `o_fixtures()`, which both sections call (Deviations D-2).

The stop works in this order. The bot (`cryptoauto`) writes a `.stop` file into `/var/spool/crypto-auto/stop`, which its unit's `ReadWritePaths=/var/spool/crypto-auto` already covers. `crypto-stop.path` starts the root oneshot. `RuntimeDirectory=crypto-stop` creates `/run/crypto-stop` for the oneshot's lifetime. `systemctl stop crypto-run.service` signals the run unit's whole cgroup. `run.py`'s handler finds `/run/crypto-stop` and logs instead of writing S7. `stop.py` then writes one notice, which the bot delivers.

## Validation

**V1, selftest.** `python3 vps/selftest.py` on the committed branch: exit 0.

```
section A: checks 32 failed 0
section B: checks 12 failed 0
section C: checks 4 failed 0
section D: checks 13 failed 0
section E: checks 12 failed 0
section F: checks 14 failed 0
section G: checks 8 failed 0
section H: checks 2 failed 0
section I: checks 4 failed 0
section J: checks 26 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 19 failed 0
section N: checks 10 failed 0
section O: checks 27 failed 0
section P: checks 21 failed 0
section Q: checks 3 failed 0
section R: checks 9 failed 0
section S: checks 35 failed 0
selftest: sections 19 checks 257 failed 0 empty 0
```

The baseline at `origin/main`, before any change, was 18 sections, 214 checks, 0 failed. Every section kept its count except F, which went from 6 to 14 (+8 rows), and S, which is new with 35 checks: item 1 has 4, item 2 has 8, item 3 has 7, item 4 has 9 and item 5 has 7. 214 + 8 + 35 = 257.

Negative controls (inv. 68). The pre-control MD5s were `bot.py d1ebb118…`, `stop.py e06bbfc8…` and `run.py beb420d1…`.

1. **`"стоп"` removed from `bot.STOP_WORDS`** (`STOP_WORDS = ("stop", "/stop")`). Exit 1, with `FAIL section F: private, owner, now, стоп`, `FAIL section F: private, owner, now, СТОП`, `section F: checks 14 failed 2`, and section S at 0 failed. Reverted, MD5 `d1ebb118c78413f62418dd1c331f9196` restored, and the selftest green again at 257/0. The revert itself went wrong first (Deviations D-1).
2. **In `stop.choose`, `"S13"` replaced by `"S14"`.** Exit 1, `section S: checks 35 failed 5`: the three S13 rows of item 3, plus item 4's notice and line checks. Reverted from a saved copy, MD5 restored, green.
3. **In `run.py`'s `on_term`, the `common.STOP_ACTIVE` test removed** (every SIGTERM writes S7). Exit 1, `section S: checks 35 failed 2`: `SIGTERM with STOP_ACTIVE present: the owner's line printed once` and `… no notice in the outbox`. Reverted from a saved copy, MD5 restored, green.

After all three: `md5sum -c` read `OK` on the three files, and the selftest was `sections 19 checks 257 failed 0 empty 0`, exit 0.

**V2, syntax.** `python3 -m py_compile vps/common.py vps/bot.py vps/run.py vps/stop.py vps/selftest.py` exited 0. `bash -n vps/install.sh` exited 0. The `__pycache__` it wrote was removed. A `grep -P '[\x{0400}-\x{04FF}]'` over the five Python files found 0 lines with raw Cyrillic.

**V3, the strings.** `python3 -c` decoding each string from `vps/common.py`:

```
S3 'Анализ запущен — ответ придёт сюда. Остановить: СТОП.' equal
S4 'Анализ уже идёт — ответ придёт сюда. Остановить: СТОП.' equal
S8 'Команды: ▶ Анализ рынка · СТОП' equal
S12 'Останавливаю анализ…' equal
S13 'Анализ остановлен.' equal
S14 'Анализ не идёт — останавливать нечего.' equal
S15 'Остановить анализ не удалось.' equal
S12 ends with U+2026: True ; S8 == "Команды: " + S1 + " · СТОП": True
```

**V4, the units (C1).** `systemd-analyze verify vps/units/*` on systemd 255 (`255.4-1ubuntu8.17`): exit 0, no output.

**V5, scope.** `git diff --name-only origin/main...HEAD` listed exactly the nine §4 files: `vps/bot.py`, `vps/common.py`, `vps/install.sh`, `vps/manifest`, `vps/run.py`, `vps/selftest.py`, `vps/stop.py`, `vps/units/crypto-stop.path`, `vps/units/crypto-stop.service`. `wc -l` gave 9.

**V6, nothing left.** See C4 below. `systemctl list-unit-files 'crypto-*'` after Stage C listed the same 9 unit files with the same states as A1's.

**V7, pushes.** The branch was pushed (`* [new branch] tz-60-vps-stop-and-six-runs -> tz-60-vps-stop-and-six-runs`), and pull request #49 is open. `main` receives only this report from this session.

## Test Results

Stage C ran on this host, on the branch's code at `c019a5b`.

**C0.** `install -d -m 0755 /var/lib/tz60-vps && cp -a vps/. /var/lib/tz60-vps/ && install -d -m 0770 /var/lib/tz60-spool/{outbox,requests,stop}` exited 0. Neither path existed beforehand, and `systemctl list-units --all 'tz60-*'` listed 0 units. The copy's `stop.py` and `common.py` MD5s equal the branch's.

**C1.** `systemd-analyze verify vps/units/*`: exit 0.

**C2, a live stop.**

```
$ systemd-run --unit tz60-dummy -p MemoryAccounting=yes /bin/sleep 600
Running as unit: tz60-dummy.service; invocation ID: 8a121b7201d44552add55d34e000bd78
$ systemctl is-active tz60-dummy.service
active
(planted {} as requests/1-bot-1.req and stop/1-bot-1.stop)
$ systemd-run --unit tz60-stop --wait --collect -p Type=oneshot -p MemoryAccounting=yes \
    -p ProtectSystem=strict -p ProtectHome=yes -p PrivateTmp=yes -p NoNewPrivileges=yes \
    -p ReadWritePaths=/var/lib/tz60-spool -p RuntimeDirectory=tz60-stop \
    -p Environment=PYTHONDONTWRITEBYTECODE=1 \
    /usr/bin/python3 /var/lib/tz60-vps/stop.py --unit tz60-dummy.service --spool /var/lib/tz60-spool
Running as unit: tz60-stop.service; invocation ID: 34bea7dce2074399a4acd0c61e11962e
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 76ms
exit=0
$ journalctl -u tz60-stop.service -o cat --no-pager | grep 'crypto-stop:'
crypto-stop: stops=1 requests_removed=1 before=active stop_exit=0 reset_exit=1 after=inactive notice=S13
$ systemctl is-active tz60-dummy.service
inactive
ls -A outbox: [1791197305196-notice-25281.json]   requests: []   stop: []
outbox files: 1 — kind=notice, text == common.S13: True
```

Every known answer is met. `reset_exit=1` is not registered: the transient unit is unloaded once stopped, as §9 C2 predicts.

**C3, nothing to stop.** The outbox notice from C2 was removed, so all three spool directories were empty, and `tz60-dummy.service` was not loaded. The same command:

```
Running as unit: tz60-stop.service; invocation ID: d196b57a586d421da14008bc557a1cb6
Finished with result: success
exit=0
crypto-stop: stops=0 requests_removed=0 before=inactive stop_exit=5 reset_exit=1 after=inactive notice=S14
outbox files: 1 — kind=notice, text == common.S14: True
```

Every known answer is met. `stop_exit=5` is not registered, as §9 C3 says: `systemctl stop` of a unit that is not loaded.

**C4, nothing left.** `systemctl reset-failed 'tz60-*'` exited 0. `systemctl list-units --all 'tz60-*' --no-pager` listed 0 units. After `rm -rf /var/lib/tz60-vps /var/lib/tz60-spool`, both paths are absent. `/var/spool/crypto-auto` still holds only `outbox` and `requests`.

**CI.** See `## CI Execution`.

## Deviations

- **D-1, the first negative control's revert.** I reverted control 1 with `git checkout -- vps/bot.py`. That restored the index's copy, which is `origin/main`'s file (MD5 `d3d8da0a43f807a2d5d86472df328156`), so B2 was undone along with the control. I re-applied B2 with the same replacement script, read the pre-control MD5 `d1ebb118c78413f62418dd1c331f9196` back with `md5sum -c`, and got a green selftest (257/0). Controls 2 and 3 were reverted from copies saved beforehand. The committed `vps/bot.py` is the one that passed every later check, at the MD5 under `## Files Modified`.
- **D-2, section O's fixture construction is shared.** §12.11 item 5 runs `run.main` «under section O's fixtures». The directories, planted login, stubs, request and local origin are now built by `o_fixtures(tmp, stub_claude, planted)`, which section O and section S both call. Section O's 27 checks keep their labels, order and conditions. Its count is 27 before and after, and it is green.
- **D-3, «the stamps g».** §12.4 defines the generations as «the stamps g of the «exchange: list generation=…» lines». I read g as the `generation=` value, which is the list's own rebuild time. That is the instant `new=` counts from, and under it the baseline window opens before T1 and is uncovered. Under the other reading, the journal time of each line, the windows are (20:37:21Z 03.10, 02:32:40Z 04.10] with 19 new and 0 in the stream, then (02:32:40Z 04.10, 03:02:40Z 05.10] with 14 new and 2 in the stream. Both are covered and the first is silent, so it is also **D0**. Both readings were computed by one script, and the verdict does not depend on the choice.
- **D-4, the per-day count.** §7 A3.5 asks for «per UTC day, the count by `catalogName`» without naming whose day. I counted by the day of `received_ms`. All three records were received and published on 05.10, so the publication day gives the same count.
- **D-5, docstrings and comments.** These were not dictated. The `run.py` docstring gains one sentence that says what a SIGTERM during the owner's stop does. `vps/selftest.py`'s docstring names TZ-60 B7 and §12.11, as earlier TZs' did. `vps/common.py` carries one-line comments citing TZ-60 §12.1 and §12.5 at the changed strings and the new path. No code outside §12 moved.

## Pre-existing Issues

- **`crypto-run.service` reads `failed`.** It has `ActiveState=failed`, `Result=exit-code` and `InactiveEnterTimestamp=Sun 2026-10-04 17:24:37 UTC`: the L run's exit 1. It was in this state before the session, and this session never targeted it except with reads. A failed state does not stop `crypto-run.path` from starting the next run. After this merge, `stop.py`'s `reset-failed` clears such a state on each stop. Nothing was done.
- **The L run's resident peak equals its ceiling.** `memory_peak=369098752` and `memory_max=369098752`, with `memory_swap_peak=8105984`. The run held its whole resident allowance and paid the rest with its own swap, as TZ-56's design intends, and was not killed. The C run's `memory_peak` (318 914 560) exceeds its `memory_max` (318 767 104) by 147 456 bytes, a charge in flight that the kernel can record above the limit. Both are reported, not acted on.
- **A third acted update during the second run.** The bot logged `updates=1 acted_total=6` at 17:15:05Z, 35 s after the second run started, while it waited for admission (`waited_s=30`). The bot's log names no verdict, and its direct replies are not logged, so the journal cannot say what that message was or what the bot answered.
- **The announcement journal has no `planned refresh` and no `data_messages` line since T1.** The only `announce: data ` lines are the three of 05.10.

## Remaining Risks

- **R-1, the size is `open`.** Two of six runs were read. The next four presses decide it under §12.2's rule, and an `S` run, the owner's stop, now also measures nothing about memory.
- **R-2, the stream is `D0`.** For about 29 hours after T1 the stream recorded nothing, while the exchange's list gained 33 articles over its two rebuilds. Only `Latest Activities` records have arrived since. Map §10 calls this «the defect three measurements could not see», and the decision on it is the Architect's (§5).
- **R-3, `S12` promises a stop that a root unit performs.** If `crypto-stop.service` fails before step 7, the owner has read «Останавливаю анализ…» and receives no S13, S14 or S15. Its failure is visible only in the journal, and no alert is in scope (§5).
- **R-4, the hosted gate does not run `vps/selftest.py`.** `bench.yml` has no step for it. The deployer's `install.sh` runs it before every install and refuses a red tree (S10). So section S's proof for this branch is the local run recorded above, and the gate on the VPS will run it again at the merge.
- **R-5, the stop on the real unit is proven by parts, never whole.** C2 stopped a transient unit, and section S item 5 proved `run.py`'s handler. §4 forbids stopping `crypto-run.service` itself in this session. A read of the unit (`systemctl show crypto-run.service -p KillMode -p TimeoutStopUSec -p SendSIGKILL`) gives `KillMode=control-group`, `TimeoutStopUSec=1min 30s` and `SendSIGKILL=yes`. So the stop signals every process of its cgroup and kills them after 90 s, inside `crypto-stop.service`'s `TimeoutStartSec=300`. The first stop the owner sends is the first whole run of it. A run's commits that reached `main` before the stop stay there, and §3 does not ask for them to be undone.

## Commit

Implementation, on the branch, already pushed: `c019a5b657ee778396f52ef1598b79ee82d587d4`.

```
TZ-60: vps — the owner's STOP: the word stops the run, its session and every process it started
```

Contents: the nine files under `## Files Created` and `## Files Modified`.

Report, on `main`:

```
TZ-60: report — the STOP, and the runs the button started after TZ-57's merge
```

Contents: `CryptoReports/TZ-60-vps-stop-and-six-runs-report.md`.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/49. Base `main`, head `tz-60-vps-stop-and-six-runs`, opened by this session.

## CI Execution

- **`bench.yml` ("Bench gate"), run `37299045989`, event `pull_request`: completed, conclusion `success`, on head `c019a5b657ee778396f52ef1598b79ee82d587d4`.** Read with `gh run view 37299045989 --json conclusion,status,headSha,event,databaseId`. The workflow has no step that runs `vps/selftest.py` (`grep -n -i 'vps\|selftest' .github/workflows/bench.yml` matches only `analyst/live-gate.sh --selftest`), so this run proves nothing about `vps/`.
- `bench.yml` on `push` did not run: its `push` trigger names `main` and `claude/**`, and this branch is neither.
- `main.yml` did not run, and cannot from this branch: its `push` filter is an allow-list of `main.py` and `.github/workflows/main.yml`, confirmed before the report's push. `calib.yml` filters on `bench/exhaustion_calib.py` and its own file, plus `claude/**`. `journal.yml` and `backtest_bench.yml` are schedule- or dispatch-only.
- **The runner that executes `vps/selftest.py` is the VPS deployer's `install.sh`, at the merge.** The local runs on this host are under `## Validation`.

## Final Repository State

The branch `tz-60-vps-stop-and-six-runs` is at `c019a5b657ee778396f52ef1598b79ee82d587d4`, pushed to `origin`, with a clean working tree (`git status --porcelain` → 0 lines). It is one commit ahead of `f8070a2`, and its `vps` tree is `81c33f881d4728eda33444e7840ecf9110d616d3`. The VPS outside the repository is as A1 found it: the same 9 unit files and states, no `tz60-*` unit, and no scratch path. No run was started, requested or stopped, and nothing under `/etc/crypto-auto/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or `/var/spool/crypto-auto` was written.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

The gate script read `SYSTEM-MAP-CRYPTOCALCUL.md` and the TZ from `origin/main` with `git show`. It cut the map's anchor table by its structure: every `|` row after the `|---|---|` separator that follows `| Anchor | Exact string that must be present |`, up to the first line not starting with `|`. Each anchor was matched with `grep -F -m1 -o -- <anchor>` against the map.

- Revision string, the first in `## 0. Fingerprint`: `**Revision 2026-10-05-a.**`. The TZ requires `**Revision 2026-10-05-a.**`.
- **Map anchor table rows: 7. Compared: 7. Passed: 7.** The TZ header's anchor rows: 7.

| Anchor | TZ quote identical | `grep -F -m1 -o` exit | Text the match returned |
|---|---|---:|---|
| revision | yes | 0 | `**Revision 2026-10-05-a.**` |
| direction engine | yes | 0 | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | yes | 0 | `### 3.15 Catalyst registry` |
| exhaustion measure | yes | 0 | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | yes | 0 | `## 11. Analytical engine` |
| squeeze block | yes | 0 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | yes | 0 | `72. **A write that fails leaves this run's product or nothing` |

Files at `origin/main` (`f8070a2`):

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 3230 | `6ae8807f25f54981562074f3262efd2b` | 3230 / `6ae8807f…`, equal (reported, not enforced) |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | equal; version line `**Version 26.**` |
| `vps/bot.py` | 422 | `d3d8da0a43f807a2d5d86472df328156` | equal |
| `vps/common.py` | 329 | `0a54ae9169cc06e36465413d198f2c4b` | equal |
| `vps/run.py` | 333 | `10165bc8d4d79e92db30147a76eec48f` | equal |
| `vps/install.sh` | 251 | `d0a26e04d520501f0dea68f67fc14cc3` | equal |
| `vps/manifest` | 6 | `279e5f1b479b5cfdf1ec7582ac382054` | equal |
| `vps/selftest.py` | 817 | `c728b6fd74d1aaad269a1fb2a6de886e` | equal |

`origin/main:vps` is `36f06177a8899162865e17157d57d643c58e1adc`, which equals the tree this TZ was written against and the deployed marker. The branch's files after the change are under `## Files Created` and `## Files Modified`.
