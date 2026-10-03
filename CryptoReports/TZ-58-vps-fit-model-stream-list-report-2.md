# Implementation Report — TZ-58

## Status

**PARTIAL. The model scope is BLOCKED at A4. The fit, the stream and the list are done.** The session ran on the VPS: `hostname` returned `vultr`. Every A0 answer was the known one.

1. **The fit: `fits=yes`.** The chosen invocation is class **C** (the run started at 11:37:53Z). Its footprint is **332 668 928** bytes. `budget_bytes` is **704 643 072**, unchanged, because `record_limits` still takes TZ-54's input term. **The host's answer: it stays as it is.**
2. **The model: BLOCKED.** A4 read `2.1.282 (Claude Code)`. The `--effort` line it printed is `--effort <level>                      Effort level for the current session`. That line offers `<level>`, not `high`. The levels `(low, medium, high, xhigh, max)` are on the help's next, wrapped line, which A4's `grep` does not print. So M1 is not met on the line A4 printed. `run.py` keeps `--model opus` and has no `--effort`.
3. **`crypto-announce.service` is listed.** C1 read `announce: key ACCEPTED`, then one command answer `{"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}`, then the subscribe answer `{"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}`. It exited 2.
4. **The list reader is built.** C2's baseline line: `exchange: list generation=2026-10-03T02:02:14Z read=2026-10-03T19:59:05Z children=3 articles=8329 new=- gone=- baseline=yes`. An independent `curl` count read the same 3 children and 8 329 articles.

**What unblocks the model scope:** a TZ that states which text M1 is judged on: the physical line A4's `grep` prints, or the `--effort` option's whole help entry, which here wraps onto a second line (Deviations D-2, Remaining Risks R-2). The code that reading would build is TZ-58 §12.6, unchanged.

The previous TZ is merged. TZ-57's accepted branch `claude/vibrant-albattani-ddmwh1` at `895d1dc` is an ancestor of `origin/main`. It was merged by `075de0e`, pull request #46 (A1).

## Inbound Filing

None moved. `CryptoTZ/TZ-58-vps-fit-model-stream-list.md` is at its canonical path on `origin/main`, in one copy: 575 lines, MD5 `d5eecb82b6fd9fe2178e969c39b55f25`, uploaded in `505367e`. It was found with contract §3's search after `git fetch`. The clone is not shallow (`git rev-parse --is-shallow-repository` → `false`).

**A report for TZ-58 already exists.** `CryptoReports/TZ-58-vps-fit-model-stream-list-report.md` (`44e4313`) records a session in a cloud container (`hostname` → `vm`). That session stopped BLOCKED at A0. This session ran the TZ again on the VPS. Contract §10 and §13 make a re-run's report `-report-2.md` and forbid overwriting the first, so this file is that report. The first report is unchanged.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names files under `vps/`. The branch is `tz-58-vps-fit-model-stream-list`, opened from `origin/main` at `44e4313`.

| Stage | Executed | Outcome |
|---|---|---|
| A0 | yes | all four known answers |
| A1 (§4a 1–6, §5 gate, merge check, deploy lines) | yes | gate passed; TZ-57 merged; marker = `origin/main:vps` |
| A2 | yes | 2 invocations: 1 L, 1 C → `fits=yes` |
| A3 | yes | **L1** |
| A4 | yes | **M1 not met** → model scope BLOCKED |
| B1 `vps/exchange.py` | yes | §12.5 built (under L1) |
| B2 `vps/run.py` | **no** | model scope BLOCKED |
| B3 `vps/selftest.py` | yes | section R's list checks; section O unchanged (no M1) |
| C1 | yes | every known answer met |
| C2 | yes | every known answer met |
| E1 | yes | product block appended; the three derived lines rewritten with unchanged values |
| E2 | yes | `crypto-run.service` **unchanged** |
| E3 | yes | `crypto-announce.service` listed |
| E4 | yes | selftest green, 18 sections, 211 checks |
| V1–V11 | yes | see `## Validation` |

### A0 — the host, before the gate

The command `date -u +%FT%TZ` printed `2026-10-03T19:50:43Z` just before the four checks.

```
$ hostname
vultr
exit=0
$ systemctl is-active crypto-bot.service crypto-exchange.service
active
active
exit=0
$ test -d /srv/crypto-auto/.git && echo clone
clone
exit=0
$ id -u cryptorun
995
exit=0
```

The known answers are `vultr`; `active` twice; `clone`; a number. All four were read. **This session's own `hostname`: `vultr`.**

### A1 — the gate, the merge check and the deploy lines

The §5 gate passed against `origin/main` at `44e4313`. Its readings are under `## Fingerprints`. Repository state:

- `git log --oneline --graph --all` shows `075de0e Merge pull request #46 from seahomebatumi-ai/claude/vibrant-albattani-ddmwh1`, whose second parent is `895d1dc`.
- The working tree was clean (`git status --porcelain` printed 0 lines).

```
$ git merge-base --is-ancestor 895d1dc93ef57bc8298c4aa7560f93141a8354fa origin/main
merge-base exit=0
$ git rev-parse origin/main:vps
c4eef2b1d03991c05a27464038f60d2a3307c14a
$ cat /var/lib/crypto-auto/deployed-vps-tree
c4eef2b1d03991c05a27464038f60d2a3307c14a
$ ls /etc/systemd/system/crypto-run.timer
ls: cannot access '/etc/systemd/system/crypto-run.timer': No such file or directory
exit=2
$ journalctl -u crypto-deploy.service --since '2026-10-03 05:00:00 UTC' -o short-iso --no-pager | grep -E 'deploy: installed vps tree|install: (removed|enabled|disabled|installed)'
2026-10-03T05:08:03+00:00 vultr deploy.sh[3928732]: install: enabled crypto-deploy.timer
2026-10-03T05:08:03+00:00 vultr deploy.sh[3928732]: install: enabled crypto-cleanup.timer
2026-10-03T05:08:04+00:00 vultr deploy.sh[3928732]: install: enabled crypto-exchange.service
2026-10-03T05:08:04+00:00 vultr deploy.sh[3928732]: install: enabled crypto-bot.service
2026-10-03T05:08:05+00:00 vultr deploy.sh[3928732]: install: enabled crypto-run.path
2026-10-03T05:08:05+00:00 vultr deploy.sh[3928732]: install: disabled crypto-announce.service
2026-10-03T05:08:05+00:00 vultr deploy.sh[3928732]: install: disabled crypto-run.timer
2026-10-03T05:08:05+00:00 vultr deploy.sh[3928732]: install: installed
2026-10-03T05:08:05+00:00 vultr deploy.sh[3928696]: deploy: installed vps tree b9f97526335fa2a12f60bab9bd164ded1250dd7c
2026-10-03T19:36:15+00:00 vultr deploy.sh[3997695]: install: removed crypto-run.timer
2026-10-03T19:36:15+00:00 vultr deploy.sh[3997695]: install: enabled crypto-deploy.timer
2026-10-03T19:36:15+00:00 vultr deploy.sh[3997695]: install: enabled crypto-cleanup.timer
2026-10-03T19:36:16+00:00 vultr deploy.sh[3997695]: install: enabled crypto-exchange.service
2026-10-03T19:36:16+00:00 vultr deploy.sh[3997695]: install: enabled crypto-bot.service
2026-10-03T19:36:16+00:00 vultr deploy.sh[3997695]: install: enabled crypto-run.path
2026-10-03T19:36:17+00:00 vultr deploy.sh[3997695]: install: disabled crypto-announce.service
2026-10-03T19:36:17+00:00 vultr deploy.sh[3997695]: install: installed
2026-10-03T19:36:17+00:00 vultr deploy.sh[3997677]: deploy: installed vps tree c4eef2b1d03991c05a27464038f60d2a3307c14a
exit=0
```

Every known answer was read: the marker equals `origin/main:vps`, `crypto-run.timer` is absent, and the journal carries `install: removed crypto-run.timer` and `deploy: installed vps tree c4eef2b…`. No wait was needed.

### A2 — TZ-56's install and the product's runs

```
$ journalctl -u crypto-deploy.service --since '2026-10-03 05:00:00 UTC' -o short-iso --no-pager | grep -F 'deploy: installed vps tree b9f97526335fa2a12f60bab9bd164ded1250dd7c'
2026-10-03T05:08:05+00:00 vultr deploy.sh[3928696]: deploy: installed vps tree b9f97526335fa2a12f60bab9bd164ded1250dd7c
exit=0
$ date -u +%FT%TZ
2026-10-03T19:52:02Z
```

**T0 = `2026-10-03T05:08:05Z`**: one line, after 05:06:59Z, as the known answer says. **R = `2026-10-03T19:52:02Z`.**

The command below printed 17 lines, which are reproduced in full. Without the `grep`, the same window holds 19 lines. The two lines the filter drops are not printed (rule 10).

```
$ journalctl -u crypto-run.service --since '2026-10-03 05:08:05 UTC' --until '2026-10-03 19:52:02 UTC' -o short-iso-precise --no-pager | grep -E 'crypto-run:|systemd\[1\]:' | sed -E 's/(crypto-run: models=)[^ ]*/\1[withheld]/'
2026-10-03T10:56:28.493566+00:00 vultr systemd[1]: Starting crypto-run.service - Crypto assistant: one headless analysis run...
2026-10-03T10:56:28.565418+00:00 vultr python3[3957917]: crypto-run: limits unit=crypto-run.service mem_available=296714240 swap_free=2807758848 budget=704643072 memory_max=218103808 memory_swap_max=486539264 set=0
2026-10-03T10:56:28.587659+00:00 vultr systemd[1]: Started crypto-run.service - Crypto assistant: one headless analysis run.
2026-10-03T10:56:58.999709+00:00 vultr python3[3957920]: crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=1 is_error=true num_turns=9 duration_ms=16932 denials=0 answer_chars=0
2026-10-03T10:56:58.999709+00:00 vultr python3[3957920]: crypto-run: models=[withheld] denied_tools=- subtype=success api_error_status=429 terminal_reason=api_error stop_reason=stop_sequence
2026-10-03T10:56:59.000960+00:00 vultr python3[3957920]: crypto-run: memory_max=218103808 memory_swap_max=486539264 mem_available=296787968 swap_free=2807758848 memory_peak=218103808 memory_swap_peak=3588096 input_tokens=10 output_tokens=1198 cache_read_tokens=178588 cache_creation_tokens=151736 cost_usd=1.2736056
2026-10-03T10:56:59.049782+00:00 vultr systemd[1]: crypto-run.service: Main process exited, code=exited, status=1/FAILURE
2026-10-03T10:56:59.049919+00:00 vultr systemd[1]: crypto-run.service: Failed with result 'exit-code'.
2026-10-03T10:56:59.050528+00:00 vultr systemd[1]: crypto-run.service: Consumed 2.776s CPU time.
2026-10-03T11:37:53.878546+00:00 vultr systemd[1]: Starting crypto-run.service - Crypto assistant: one headless analysis run...
2026-10-03T11:37:53.986570+00:00 vultr python3[3961675]: crypto-run: limits unit=crypto-run.service mem_available=241364992 swap_free=2720804864 budget=704643072 memory_max=167772160 memory_swap_max=536870912 set=0
2026-10-03T11:37:54.009143+00:00 vultr systemd[1]: Started crypto-run.service - Crypto assistant: one headless analysis run.
2026-10-03T11:58:31.977504+00:00 vultr python3[3961679]: crypto-run: requests=1 admitted=yes waited_s=0 writer_exit=0 claude_exit=0 is_error=false num_turns=58 duration_ms=1224760 denials=0 answer_chars=6182
2026-10-03T11:58:31.978581+00:00 vultr python3[3961679]: crypto-run: models=[withheld] denied_tools=- subtype=success api_error_status=- terminal_reason=completed stop_reason=end_turn
2026-10-03T11:58:31.979967+00:00 vultr python3[3961679]: crypto-run: memory_max=167772160 memory_swap_max=536870912 mem_available=239849472 swap_free=2721067008 memory_peak=167780352 memory_swap_peak=164888576 input_tokens=108 output_tokens=83752 cache_read_tokens=11941234 cache_creation_tokens=321164 cost_usd=10.093022199999986
2026-10-03T11:58:32.060400+00:00 vultr systemd[1]: crypto-run.service: Deactivated successfully.
2026-10-03T11:58:32.060844+00:00 vultr systemd[1]: crypto-run.service: Consumed 2min 46.229s CPU time.
```

```
$ journalctl -u crypto-bot.service --since '2026-10-03 05:08:05 UTC' -o short-iso --no-pager | grep -F 'bot: sent '
2026-10-03T10:57:09+00:00 vultr python3[3929341]: bot: sent 1791025018969-notice-3957920.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
2026-10-03T11:58:34+00:00 vultr python3[3929341]: bot: sent 1791028711941-answer-3961679.json kind=answer chunks=2 accepted=2 plain_fallbacks=0
exit=0
$ git log origin/main --since '2026-10-03 05:08:05 UTC' --format='%h %cI %s' -- analyst/
b43df91 2026-10-03T11:58:00+00:00 analyst: 2026-10-03
729b6d0 2026-10-03T11:38:03+00:00 analyst: live.json (vps)
bc0cdd9 2026-10-03T10:56:38+00:00 analyst: live.json (vps)
$ grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo
MemTotal:         978640 kB
MemAvailable:     345960 kB
SwapTotal:       3174396 kB
SwapFree:        2723392 kB
$ nproc
1
$ systemctl list-unit-files 'crypto-*' --no-pager
UNIT FILE               STATE    PRESET
crypto-run.path         enabled  enabled
crypto-announce.service disabled enabled
crypto-bot.service      enabled  enabled
crypto-cleanup.service  static   -
crypto-deploy.service   static   -
crypto-exchange.service enabled  enabled
crypto-run.service      static   -
crypto-cleanup.timer    enabled  enabled
crypto-deploy.timer     enabled  enabled

9 unit files listed.
```

**Classification, by §12.2.** A script applied §12.2's rules, in their order of precedence, to the 17 lines above. Each invocation runs from its `Starting` line to the next one or to R.

| start (UTC) | class | memory_max | memory_swap_max | memory_peak | memory_swap_peak | footprint | duration_s | requests | input | output | cache_read | cache_creation | cost_usd |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-10-03T10:56:28.493566 | **L** | 218103808 | 486539264 | 218103808 | 3588096 | 221691904 | 30.507394 | 1 | 10 | 1198 | 178588 | 151736 | 1.2736056 |
| 2026-10-03T11:37:53.878546 | **C** | 167772160 | 536870912 | 167780352 | 164888576 | 332668928 | 1238.101421 | 1 | 108 | 83752 | 11941234 | 321164 | 10.093022199999986 |

Why each run has its class:

- **10:56:28.** It carries `Failed with result 'exit-code'`, so it is neither K-oom nor K-timeout. Its first summary line reads `admitted=yes`, so it is not N. Its second line reads `api_error_status=429`, so it is **L**.
- **11:37:53.** It carries `Deactivated successfully`. It was admitted, with `api_error_status=-`. Its first line reads `claude_exit=0 is_error=false answer_chars=6182`, so it is **C**.
- **Active invocations: 0.**

Counts: invocations 2, K-oom 0, K-timeout 0, N 0, L 1, C 1, F 0.

**Decision: `fits=yes`.** No invocation is K, and one is C. **Chosen:** the C with the largest footprint, 11:37:53. It is the only C.

The known answer, "at least two invocations read `admitted=yes` and `writer_exit=0`", was read: both do.

### A3 — the list, by the program's own client from the VPS

This was an in-session `python3` run with `urllib.request`'s default headers and `timeout=20`. Bodies were kept for offline re-reading; none is printed beyond the counts.

```
A3.1 robots.txt read=2026-10-03T19:53:40Z status=200 content_type=text/plain; charset=UTF-8 bytes=6722
  groups=3 star_groups=1
  * group line: Allow: */bapi/fe/
  * group line: Allow: */sitemap_output/
  * group line: Disallow: */bapi/
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Trade_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Nft_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Futures_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Earn_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Loan_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Market_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Default_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Fiat_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Crypto_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Square_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Academy_New_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Muses_index.xml
  * group line: Sitemap: https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Growth_index.xml
A3.2 index read=2026-10-03T19:53:41Z status=200 content_type=application/xml bytes=13536 last_modified=Sat, 03 Oct 2026 02:02:14 GMT sha256=d8726eb4bab581e5fb3571a97403680f29bf450289832b8d4cc2c6092c442c60 children=3
  child https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_2.xml
  child https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml
  child https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_1.xml
A3.3 child sitemap_SupportAndAnnouncement_en_2.xml read=2026-10-03T19:53:41Z status=200 content_type=application/xml bytes=119728 last_modified=Sat, 03 Oct 2026 02:01:16 GMT articles=0
A3.3 child sitemap_SupportAndAnnouncement_en_0.xml read=2026-10-03T19:53:42Z status=200 content_type=application/xml bytes=754121 last_modified=Sat, 03 Oct 2026 02:02:00 GMT articles=4971
A3.3 child sitemap_SupportAndAnnouncement_en_1.xml read=2026-10-03T19:53:42Z status=200 content_type=application/xml bytes=745290 last_modified=Sat, 03 Oct 2026 02:02:04 GMT articles=3358
A3.3 union articles=8329
exit=0
```

The `* group line` entries are the `User-agent: *` group's lines that contain `sitemap_output` or `bapi`. The `Sitemap:` lines contain `sitemap_output`, so they are listed too.

**Outcome: L1.** Every answer is 200, and the four sitemap answers carry `application/xml`. D-1 says how the `Content-Type` clause was applied to robots.txt. The group carries `Allow: */sitemap_output/`. The index names 3 English children, and the union holds 8 329 articles. B1 is built and C2 runs.

These figures match every figure in the Architect's derivation, read at 14:03Z: 3 English children, an index rebuilt at 02:02:14Z, and 8 329 articles. §7 notes that the counts move with every rebuild, so they were never a registered bar. Child `en_2` holds 0 articles under §12.5's pattern. The union comes entirely from `en_0` (4 971) and `en_1` (3 358).

### A4 — the command line the run will use

```
$ systemd-run --unit=tz58-cli -p User=cryptorun -p Group=cryptorun -p MemoryAccounting=yes -p RemainAfterExit=yes -p Environment=HOME=/var/lib/cryptorun -p Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin -p Environment=DISABLE_AUTOUPDATER=1 /bin/sh -c 'command -v claude; claude --version; claude --help | grep -E -- "--(model|effort)"'
Running as unit: tz58-cli.service; invocation ID: 0da99f16014d480f8ef24c0522d4a003
exit=0
$ systemctl show tz58-cli -p Result -p ExecMainStatus -p SubState
Result=success
ExecMainStatus=0
SubState=exited
$ journalctl -u tz58-cli -o short-iso --no-pager
2026-10-03T19:55:06+00:00 vultr systemd[1]: Started tz58-cli.service - /bin/sh -c "command -v claude; claude --version; claude --help | grep -E -- \"--(model|effort)\"".
2026-10-03T19:55:06+00:00 vultr sh[4000518]: /usr/bin/claude
2026-10-03T19:55:06+00:00 vultr sh[4000520]: 2.1.282 (Claude Code)
2026-10-03T19:55:06+00:00 vultr sh[4000524]:   --effort <level>                      Effort level for the current session
2026-10-03T19:55:06+00:00 vultr sh[4000524]:   --model <model>                       Model for the current session. Provide
```

The unit's `Environment=` lines are `crypto-run.service`'s own `HOME=`, `PATH=` and `DISABLE_AUTOUPDATER=1` lines, read from `vps/units/crypto-run.service`.

**Outcome: M1 not met, so the model scope is BLOCKED.**

- The version, 2.1.282, is 2.1.280 or later.
- The `--effort` line A4 printed offers `<level>`, not `high`.

The session's own probe of the same binary is D-2. It ran `/usr/bin/claude` with the same `PATH`, and the binary resolves to `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`. That probe shows the help wrapping the entry at a fixed width, whatever `COLUMNS` is:

```
81:  --effort <level>                      Effort level for the current session
82-                                        (low, medium, high, xhigh, max)
```

**Two readings, which would produce different code** (contract §12):

- **(i) "The `--effort` line" is the physical line A4's `grep` prints.** That line does not offer `high`, so M1 fails. The model scope is BLOCKED, and `run.py` and selftest section O stay as `main` has them.
- **(ii) "The `--effort` line" is the option's help entry.** That entry wraps onto line 82 and offers `high`, so M1 holds. B2 writes §12.6 into `vps/run.py`, and section O gains §12.7's three checks.

The TZ's own fallback for "anything else", together with contract §12, gives BLOCKED. Reading (ii) is not built. TZ-58 §12.6's dictated block is the whole of what it would write, so no prototype is kept.

### Stage B

- **B1 — `vps/exchange.py`** carries §12.5. The five constants are verbatim: a script matched each of the TZ block's 5 lines as a whole line of the file, 5 of 5. The new code is `list_children`, `list_articles`, `list_diff`, `list_poll`, `ListUnreadable`, `--list-once`, and the service's hourly read after each exchangeInfo poll. A failure in that read logs `exchange: list read failed (<class>)` and never stops the poll. `act()` and the poll line did not move.
- **B2 — not built** (A4).
- **B3 — `vps/selftest.py`.** Section R gains §12.7's texts. A script matched each of the TZ block's 12 lines as a whole line of the file, 12 of 12. R also gains the six known answers, beside TZ-57's three alerts-only checks. Section O is unchanged, because M1 was not met. The module docstring names TZ-58.

### Stage C — on the branch's code

`/var/tmp/tz58-vps` was a `0755 root:root` copy of the branch's `vps/`. A `cmp` of every file against the working tree printed no difference. `/var/tmp/tz58-state` was created `0770 cryptoauto:cryptoauto`.

**C1 — the handshake.**

```
$ systemd-run --unit=tz58-subscribe -p MemoryAccounting=yes -p RuntimeMaxSec=120 -p RemainAfterExit=yes -p LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key -p LoadCredential=binance-api-secret:/etc/crypto-auto/credentials/binance-api-secret /usr/bin/python3 /var/tmp/tz58-vps/announce.py --measure 60 1 --state-dir /var/tmp/tz58-state
Running as unit: tz58-subscribe.service; invocation ID: fea3c349eed049c3a952cc432f491e75
exit=0
$ systemctl show tz58-subscribe -p Result -p ExecMainStatus
Result=exit-code
ExecMainStatus=2
$ journalctl -u tz58-subscribe -o short-iso --no-pager
2026-10-03T19:57:29+00:00 vultr systemd[1]: Started tz58-subscribe.service - /usr/bin/python3 /var/tmp/tz58-vps/announce.py --measure 60 1 --state-dir /var/tmp/tz58-state.
2026-10-03T19:57:29+00:00 vultr python3[4000879]: announce: key ACCEPTED ipRestrict=true enableReading=true enableFutures=false enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableMargin=false
2026-10-03T19:57:30+00:00 vultr python3[4000879]: announce: command answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
2026-10-03T19:57:30+00:00 vultr python3[4000879]: announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "SUBSCRIBE", "type": "COMMAND"}
2026-10-03T19:58:31+00:00 vultr python3[4000879]: announce: data_messages=0 complete=0 pings=1 reconnects=0 close_codes=-
2026-10-03T19:58:31+00:00 vultr systemd[1]: tz58-subscribe.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
2026-10-03T19:58:31+00:00 vultr systemd[1]: tz58-subscribe.service: Failed with result 'exit-code'.
```

A second call, `systemctl show tz58-subscribe -p SubState -p MemoryPeak`, read `MemoryPeak=18190336` and `SubState=failed`.

| C1 known answer | Read | Met |
|---|---|---|
| `announce: key ACCEPTED` | `announce: key ACCEPTED ipRestrict=true enableReading=true …` (every other right `false`) | yes |
| exactly one `announce: command answer` line, `"subType": "REGISTER"`, `"data": "SUCCESS"` | one line, `"subType": "REGISTER"`, `"data": "SUCCESS"` | yes |
| one `announce: subscribe answer` line, `"subType": "SUBSCRIBE"`, `"data": "SUCCESS"` | one line, `"subType": "SUBSCRIBE"`, `"data": "SUCCESS"`, 1 s after start | yes |
| exit 0 or 2 | `ExecMainStatus=2`: no message arrived in the minute, which decides nothing | yes |

**C1 met every known answer, so E3 lists `crypto-announce.service`.** The unit was in the `failed` state for exit 2 and was cleared with `systemctl reset-failed tz58-subscribe.service`.

**C2 — the list reader.**

```
$ systemd-run --unit=tz58-list -p User=cryptoauto -p Group=cryptoauto -p MemoryAccounting=yes -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz58-vps/exchange.py --list-once --state-dir /var/tmp/tz58-state
2026-10-03T19:59:04Z
Running as unit: tz58-list.service; invocation ID: e0f46a4419494253b20cdbb02c2b4303
exit=0
$ curl -sS -m 20 -D index.hdr -o index.xml <LIST_INDEX_URL>
curl exit=0
2026-10-03T19:59:06Z
HTTP/2 200 
content-type: application/xml
last-modified: Sat, 03 Oct 2026 02:02:14 GMT
https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_2.xml
https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml
https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_1.xml
$ curl -sS -m 20 -o c0.xml https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_2.xml
curl exit=0 HTTP/2 200  bytes=119728
$ curl -sS -m 20 -o c1.xml https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_0.xml
curl exit=0 HTTP/2 200  bytes=754121
$ curl -sS -m 20 -o c2.xml https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en_1.xml
curl exit=0 HTTP/2 200  bytes=745290
$ cat c*.xml | grep -o -E '<loc>https://www\.binance\.com/en/support/announcement/detail/[0-9A-Za-z]+</loc>' | sort -u | wc -l
8329
2026-10-03T19:59:06Z
$ systemctl show tz58-list -p Result -p ExecMainStatus
Result=success
ExecMainStatus=0
$ journalctl -u tz58-list -o short-iso --no-pager
2026-10-03T19:59:04+00:00 vultr systemd[1]: Started tz58-list.service - /usr/bin/python3 /var/tmp/tz58-vps/exchange.py --list-once --state-dir /var/tmp/tz58-state.
2026-10-03T19:59:05+00:00 vultr python3[4001165]: exchange: list generation=2026-10-03T02:02:14Z read=2026-10-03T19:59:05Z children=3 articles=8329 new=- gone=- baseline=yes
```

The `-D` and `-o` flags, and their actual paths, are D-3. `<LIST_INDEX_URL>` stands for §12.5's literal, which the command carried in full. The English children were cut from `curl`'s index with `grep -o -E` on `LIST_CHILD`'s URL form, de-duplicated in order of first appearance.

The state file holds 8 329 ids. This read printed only the keys and the id count, never the ids:

```
$ python3 -c ... /var/tmp/tz58-state/list-generation.json
{'digest': 'd8726eb4bab581e5fb3571a97403680f29bf450289832b8d4cc2c6092c442c60', 'generation': '2026-10-03T02:02:14Z', 'read': '2026-10-03T19:59:05Z', 'children': 3, 'articles': 8329}
sorted True unique True
-rw-r----- cryptoauto:cryptoauto 279905 /var/tmp/tz58-state/list-generation.json
```

The second read ran 62 s after the first:

```
$ systemd-run --unit=tz58-list2 -p User=cryptoauto -p Group=cryptoauto -p MemoryAccounting=yes -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz58-vps/exchange.py --list-once --state-dir /var/tmp/tz58-state
2026-10-03T20:00:06Z
Running as unit: tz58-list2.service; invocation ID: 64da39931d0b4978a69b02788a9cf108
exit=0
$ systemctl show tz58-list2 -p Result -p ExecMainStatus
Result=success
ExecMainStatus=0
$ journalctl -u tz58-list2 -o short-iso --no-pager
2026-10-03T20:00:06+00:00 vultr systemd[1]: Started tz58-list2.service - /usr/bin/python3 /var/tmp/tz58-vps/exchange.py --list-once --state-dir /var/tmp/tz58-state.
2026-10-03T20:00:06+00:00 vultr python3[4001448]: exchange: list unchanged generation=2026-10-03T02:02:14Z articles=8329
```

| C2 known answer | Read | Met |
|---|---|---|
| one `exchange: list generation=` line with `baseline=yes`, `new=-`, `gone=-` | that line, `baseline=yes new=- gone=-` | yes |
| its `children` equal to the English children `curl` read | `children=3`; `curl` read 3 | yes |
| its `articles` equal to `curl`'s count | `articles=8329`; `curl` counted 8329 | yes |
| `list-generation.json` holds that many ids | 8 329 ids, sorted, unique | yes |
| the second read prints `exchange: list unchanged` with the same `articles` | `exchange: list unchanged generation=2026-10-03T02:02:14Z articles=8329` | yes |
| `Last-Modified` equal between the program's read and `curl`'s | program `generation=2026-10-03T02:02:14Z`; `curl` `Sat, 03 Oct 2026 02:02:14 GMT` | equal, so no repeat was needed |

**C2 met every known answer. The list scope stands, and B1 is not reverted.**

### Stage E

- **E1 — `vps/memory-record.txt`.** §12.3's block was appended after TZ-55's lines. The three derived lines were rewritten by §12.4, and each kept its value: `budget_bytes=704643072`, `runtime_max_s=5400`, `memory_swap_max_bytes=251658240` (704 643 072 − 452 984 832). The diff is under `## Implementation Summary`.
- **E2 — `vps/units/crypto-run.service`: unchanged.** `MemorySwapMax=` is budget − 167 772 160 = 536 870 912, and `RuntimeMaxSec=` is 5400. Both equal the lines already in the file. The file has 37 lines, MD5 `dc6ac1073c42b03c1a2f3b754e28bca0`, on `main` and on the branch.
- **E3 — `vps/manifest`**, in order: `crypto-deploy.timer`, `crypto-cleanup.timer`, `crypto-exchange.service`, `crypto-bot.service`, `crypto-run.path`, `crypto-announce.service`.
- **E4 —** the selftest is green (V1).

## Files Created

None in the repository. This report is the session's only file on `main`.

On the VPS, created and removed again (V9): the transient units `tz58-cli`, `tz58-subscribe`, `tz58-list` and `tz58-list2`, and the directories `/var/tmp/tz58-vps` and `/var/tmp/tz58-state`. The session's own scratchpad is D-4.

## Files Modified

On the branch, in commit `a172529`:

| File | `main` lines · MD5 | branch lines · MD5 | hunks (`-U0`) |
|---|---|---|---:|
| `vps/exchange.py` | 145 · `1f09fe5df3a056e012da9f0e2293bd50` | 262 · `8e434f380c50140cef753dc2ed7705c5` | 11 |
| `vps/selftest.py` | 789 · `8fb4d4ad5ddca12e729a94fbf5210253` | 811 · `dbea50aeec9b30034be9e57f8150a5c2` | 3 |
| `vps/memory-record.txt` | 20 · `9dddbda291d63f14a14a45d2a1c84d03` | 36 · `3c5cecbe156958decf388e4073607ccb` | 1 |
| `vps/manifest` | 5 · `4368b19c14fa75cb5289526592f66096` | 6 · `279e5f1b479b5cfdf1ec7582ac382054` | 1 |

`git diff --stat`: 4 files changed, 166 insertions, 10 deletions.

Named in the scope and **not modified**:

- `vps/run.py`: model scope BLOCKED. It is 331 lines, `4be5ada20662f7876715b15b5250722d`, on both sides.
- `vps/units/crypto-run.service`: E2 moved nothing.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**The fit.** The product's two runs since TZ-56's install were classed from the run unit's own journal. The second completed (C) and no run was killed, so the record carries `fits=yes` and the product block of the chosen run. `common.record_limits` (TZ-57) re-derived the budget from the record. Its terms are:

- input: 704 643 072 / 5 400;
- TZ-55's run: 486 539 264 / 5 400;
- the product's C run: footprint term 503 316 480 and duration term 5 400.

The budget therefore stays at the input term, 704 643 072, and the runtime stays 5 400. Nothing in the run unit moves.

```
@@ -20,0 +21,16 @@ runtime_max_s=5400
+# TZ-58: the product's own runs since TZ-56's install (map §10). Written at Stage E; never edited by hand.
+product_read_utc=2026-10-03T19:52:02Z
+product_invocations=2
+product_killed=0
+product_not_admitted=0
+product_account_limited=1
+product_completed=1
+product_class=C
+product_run_utc=2026-10-03T11:37:53Z
+product_memory_max_bytes=167772160
+product_memory_swap_max_bytes=536870912
+product_memory_peak_bytes=167780352
+product_memory_swap_peak_bytes=164888576
+product_footprint_bytes=332668928
+product_duration_s=1238.101421
+fits=yes
```

**The stream.** C1 proved the documented handshake on this server's own connection, so the manifest lists `crypto-announce.service`:

```
@@ -5,0 +6 @@ crypto-run.path
+crypto-announce.service
```

**The list.** `exchange.py` now reads the English announcement sitemap.

- It reads the index hourly, after an exchangeInfo poll. It reads the children only when the index body's SHA-256 changed.
- It writes `list-generation.json` atomically with `common.atomic_write`.
- It logs every new generation's line, with `new`/`gone` against the stored ids. `list unchanged` lines are not logged by the service.
- `--list-once` prints the line whatever it is. It exits 0, or exits 1 after printing `exchange: list read failed (<class>)`.
- A non-200 answer, an index with no English child, or an empty union raises `ListUnreadable`, and the stored state stays as it was.

**The model.** Not changed (A4).

## Validation

**V1 — Selftest.** The baseline on unmodified `main` was `selftest: sections 18 checks 200 failed 0 empty 0`, exit 0. After Stage E:

```
$ python3 vps/selftest.py
section A: checks 32 failed 0
section B: checks 12 failed 0
section C: checks 4 failed 0
section D: checks 13 failed 0
section E: checks 12 failed 0
section F: checks 6 failed 0
section G: checks 8 failed 0
section H: checks 2 failed 0
section I: checks 4 failed 0
section J: checks 26 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 19 failed 0
section N: checks 10 failed 0
section O: checks 24 failed 0
section P: checks 21 failed 0
section Q: checks 3 failed 0
section R: checks 9 failed 0
selftest: sections 18 checks 211 failed 0 empty 0
exit=0
```

Every section is non-empty. Two sections grew:

- R went from 3 to 9: §12.7's six list checks.
- M went from 14 to 19: the five `fits`-present checks of `main`'s section M, which run only once the record carries `fits`.

**Negative control, under L1.** One character of one §12.7 known answer in section R was changed in the working tree: `list_diff({A, B, D}, {A, B, C}) == (1, 1)` became `== (1, 2)`.

```
$ python3 vps/selftest.py
…
section Q: checks 3 failed 0
FAIL section R: list_diff({A, B, D}, {A, B, C}) == (1, 1)
section R: checks 9 failed 1
selftest: sections 18 checks 211 failed 1 empty 0
exit=1
```

Sections A–Q each printed `failed 0`, so section R alone failed. The change was reverted, and the MD5 was restored to `dbea50aeec9b30034be9e57f8150a5c2`, the same as before the control. The selftest was green again: `selftest: sections 18 checks 211 failed 0 empty 0`, exit 0.

**V2 — Syntax.**

- `python3 -m py_compile` exited 0 on all 8 files: `announce.py`, `bot.py`, `cleanup.py`, `common.py`, `exchange.py`, `run.py`, `selftest.py`, `writer.py`.
- `bash -n` exited 0 on `vps/deploy.sh` and `vps/install.sh`.
- `systemd-analyze verify` exited 0 on each of the 9 files of `vps/units/`, and **printed no warning** on any of them.

**V3 — Dry run.**

```
$ bash vps/install.sh --dry-run
install: would install /etc/systemd/system/crypto-announce.service (0644)
install: would install /etc/systemd/system/crypto-bot.service (0644)
install: would install /etc/systemd/system/crypto-cleanup.service (0644)
install: would install /etc/systemd/system/crypto-cleanup.timer (0644)
install: would install /etc/systemd/system/crypto-deploy.service (0644)
install: would install /etc/systemd/system/crypto-deploy.timer (0644)
install: would install /etc/systemd/system/crypto-exchange.service (0644)
install: would install /etc/systemd/system/crypto-run.path (0644)
install: would install /etc/systemd/system/crypto-run.service (0644)
install: would enable --now crypto-deploy.timer
install: would enable --now crypto-cleanup.timer
install: would enable --now crypto-exchange.service
install: would enable --now crypto-bot.service
install: would enable --now crypto-run.path
install: would enable --now crypto-announce.service
install: would restart crypto-exchange.service
install: would restart crypto-bot.service
install: would restart crypto-announce.service
install: would copy vps/deploy.sh to /usr/local/libexec/crypto-auto/deploy.sh
install: would create /var/lib/crypto-auto/runs-enabled
exit=0
```

- Lines naming `crypto-run.timer`: 0.
- `would enable --now crypto-announce.service` is present, and E3 lists that unit.
- `systemctl list-unit-files 'crypto-*'` before and after the dry run: `cmp` equal. After the dry run it is also `cmp` equal to A2's listing.

**V4 — The fit.**

- **A2's lines against §12.2's table, invocation by invocation:** see the classification under A2. 10:56:28 is L, 11:37:53 is C, there are no active invocations, and `fits=yes`.
- **E1's product block against the chosen invocation's own lines, field by field.** A script parsed the 11:37:53 `Starting` line and its third summary line, then compared each field with `common.read_record`. It printed `fields compared: 15 differ: 0`. The 15 keys are TZ-57 §12.3's `PRODUCT_KEYS`, `fits` included.
- **`common.record_limits(<E1's record>)` = `(704643072, 5400)`.** Beside it, the record's `budget_bytes=704643072` and `runtime_max_s=5400`.
- **E2's two unit lines, `MemorySwapMax=536870912` and `RuntimeMaxSec=5400`.** Beside them, `704643072 − 167772160 = 536870912`.

**V5 — The model.**

```
$ python3 -c 'import sys; sys.path.insert(0, "vps"); import run; print(run.CLAUDE[3:])'
['--output-format', 'json', '--model', 'opus', '--allowedTools', 'Bash Read Write Edit Glob Grep WebSearch WebFetch', '--append-system-prompt', 'Read EXECUTOR-INSTRUCTIONS.md at the repository root in full before anything else: it is your contract, and the user message is a trigger from its §4.']
```

M1 is not met. A4's lines are under A4: `2.1.282 (Claude Code)`, and the `--effort` line offers `<level>`. So `run.CLAUDE` still carries `--model opus` and no `--effort`. **V5's M1 condition has no referent. This is the model scope's BLOCKED state, not a pass.**

**V6 — The stream.** C1's journal and its `systemctl show` lines, against C1's known answers, are under C1: four of four met.

**V7 — The list.** A3's answers are under A3, and the outcome is L1. C2's three readings are the baseline line, the independent count and the second read. All three are under C2, six of six known answers met.

**V8 — Credentials.** Each credential file was proven first to hold one non-empty line. Each was then used as a fixed-string pattern file over four scan sets. Only counts are printed.

```
$ B=origin/tz-58-vps-fit-model-stream-list; echo "vps files in $B: $(git ls-tree -r --name-only $B vps | wc -l)"; for c in binance-api-key binance-api-secret claude-oauth-token; do f=/etc/crypto-auto/credentials/$c; echo "$c: lines=$(grep -c '' $f) non_empty=$(grep -c . $f) | report=$(grep -c -F -f $f CryptoReports/TZ-58-vps-fit-model-stream-list-report-2.md) | diff=$(git diff origin/main...$B | grep -c -F -f $f) | vps_files=$(git ls-tree -r --name-only $B vps | while read p; do git show $B:$p; done | grep -c -F -f $f) | tz58_journal=$(journalctl -o cat -u 'tz58-*' --no-pager | grep -c -F -f $f)"; done
vps files in origin/tz-58-vps-fit-model-stream-list: 21
binance-api-key: lines=1 non_empty=1 | report=0 | diff=0 | vps_files=0 | tz58_journal=0
binance-api-secret: lines=1 non_empty=1 | report=0 | diff=0 | vps_files=0 | tz58_journal=0
claude-oauth-token: lines=1 non_empty=1 | report=0 | diff=0 | vps_files=0 | tz58_journal=0
```

Every count is 0. The scan ran on this file at its final path. It ran once more after the last edit of this file and returned the same twelve zeros.

**V9 — Nothing left.**

```
$ rm -r -- /var/tmp/tz58-vps /var/tmp/tz58-state
rm exit=0
ls: cannot access '/var/tmp/tz58-vps': No such file or directory
ls: cannot access '/var/tmp/tz58-state': No such file or directory
$ systemctl list-units --all 'tz58-*' --no-pager
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
$ ls /run/systemd/system.control/ /run/systemd/transient/ | grep -c tz58
0
```

- `systemctl list-unit-files 'crypto-*'` after the cleanup: `cmp` equal to A2's listing.
- Before removal, `/var/tmp/tz58-vps` held the copied tree plus `__pycache__/common.cpython-312.pyc`, which C1's root unit wrote. `/var/tmp/tz58-state` held `list-generation.json` only.
- How each unit ended:
  - `tz58-cli`, `tz58-list` and `tz58-list2` were stopped with `systemctl stop` after their readings. The journal shows `Deactivated successfully` and `Stopped` for each.
  - `tz58-subscribe` was cleared from `failed` with `systemctl reset-failed`.

**V10 — No production file.**

```
$ git diff --name-only origin/main...HEAD
vps/exchange.py
vps/manifest
vps/memory-record.txt
vps/selftest.py
```

Only `vps/` paths.

**V11 — Pushes.**

- `git push -u origin tz-58-vps-fit-model-stream-list` printed `* [new branch]` and exited 0.
- Pull request #47 was opened (`## Pull Request`).
- When this report was written, `git fetch` followed by `git rev-parse origin/main` gave `44e4313e01cb905351c59aa554bc0cfa02ee9eff`, which is the first report's commit and carries no commit of this session.

## Test Results

| Test | Where | Result |
|---|---|---|
| `python3 vps/selftest.py`, unmodified `main` | VPS, this session | 18 sections, 200 checks, 0 failed, exit 0 |
| `python3 vps/selftest.py`, after Stage B only | VPS, this session | 18 sections, 206 checks, 0 failed, exit 0 |
| `python3 vps/selftest.py`, after Stage E | VPS, this session | 18 sections, 211 checks, 0 failed, exit 0 |
| negative control in section R | VPS, this session | section R alone failed, exit 1; reverted and green |
| §12.5 functions on A3's saved bodies, offline | VPS, this session | 3 children; 0 + 4 971 + 3 358 articles; union 8 329 |
| Bench gate on PR #47 | GitHub runner | run 37150094049, `success` (`## CI Execution`) |

## Deviations

- **D-1. How A3's `Content-Type` clause was applied.** L1 says "every answer is 200 with an XML `Content-Type`".
  - A3 reads a `Content-Type` only for the index (A3.2) and the children (A3.3). For robots.txt (A3.1) it reads the status and the group's lines.
  - The XML condition was therefore judged on the four sitemap answers, all `application/xml`.
  - robots.txt answered 200 `text/plain; charset=UTF-8`.
  - A reading that requires robots.txt to be XML could not be met by any robots.txt, and the Architect's own derivation read the same file as text and expected L1. This note makes the reading taken visible.
- **D-2. The session ran `claude --version` and `claude --help` itself before A4.**
  - It ran them as root, with `env -i`, the run unit's `PATH`, `DISABLE_AUTOUPDATER=1`, and `HOME` set to an empty scratch directory.
  - Purpose: §4 forbids writing under `/var/lib/cryptorun`, and A4 runs with that `HOME`. The probe measured whether the two commands write anything under `HOME`. They wrote nothing: `find` over the directory counted 1 entry, the directory itself.
  - A second pass ran `claude --help | grep -n -A3 -E -- "--(model|effort)"` to read the wrapped `--effort` entry quoted under A4. A third, with `COLUMNS=300`, printed the same `--effort` line, again without the levels. The wrap does not follow the terminal width.
  - This is an own-environment measurement under contract §7 item 9, and rule 1 permits the binary with these two flags. It is the only source of reading (ii)'s line 82. A4's unit output does not carry it.
- **D-3. The form of C2's independent count.**
  - The dictated form is `curl -sS -m 20` of the index and of each English child, then `grep -o -E '<loc>…detail/[0-9A-Za-z]+</loc>'` and `sort -u | wc -l` over all children together.
  - It ran as `curl -sS -m 20 -D <hdr> -o <file>` for each of the four reads, then `cat c*.xml | grep -o -E '…' | sort -u | wc -l`.
  - The header file of the index read supplied the `Last-Modified` C2 compares.
  - The reads, the pattern and the counting pipeline are the dictated ones. Only the bodies passed through files.
- **D-4. Working files outside the two authorised directories.** §4 authorises `/var/tmp/tz58-vps` and `/var/tmp/tz58-state`, "and nothing else".
  - The session also used its own harness scratchpad, `/tmp/claude-0/<session>/scratchpad`. It held the gate and classification scripts, A2's filtered lines, R, A3's saved bodies, C2's `curl` bodies and headers, the unit-file listings, the empty `HOME` of D-2 and this report's draft.
  - It held no credential value: V8's scan sets do not include it, but nothing in it was read from a credential file.
  - Its contents were removed before this report was committed. In the scratchpad directory, `rm -r -- a2-run.txt a2-unitfiles.txt a3 a3.py c2 classes.json classify.py fakehome gate.py R.txt TZ-58-vps-fit-model-stream-list-report-2.md v3-after.txt v3-before.txt v9-unitfiles.txt` exited 0, and `ls -A` then counted 0 entries.
  - This report was copied from that draft into `CryptoReports/` before the removal.
- **D-5. The implementation commit's message names "the pinned model".** Contract §8 makes the message §14's string, verbatim, so the commit carries that text. The commit does not pin the model: the model scope is BLOCKED.

## Pre-existing Issues

- **`bench.yml` has no step that runs `vps/selftest.py`.** `grep -n 'selftest\|vps' .github/workflows/bench.yml` matches only lines 142 and 144. Those are the name and the command of the job's step 18, `analyst/live-gate.sh --selftest`. So the hosted gate's `success` on PR #47 is evidence about the rest of the repository and none about `vps/`. The `vps` selftest runs in a session and in `install.sh` on the deployer, which installs nothing when it is red. This is reported, not acted on: `bench.yml` is outside this TZ's scope (§5).
- **The chosen run's `memory_peak`, 167 780 352, exceeds its `memory_max`, 167 772 160, by 8 192 bytes.** That is the kernel's `memory.peak` against `memory.max` within one reclaim batch. It was copied as read, and the footprint sums it as §12.2 dictates.

## Remaining Risks

- **R-1. Merging PR #47 starts the stream.** The deployer's `install.sh` would run `enable --now crypto-announce.service` (V3).
  - From then on, a service holds the read-only key's stream connection continuously and alerts the owner on matched titles.
  - C1's minute received no data message (`data_messages=0`).
  - Delivery against the exchange's own list is the next TZ's reading (§5). This TZ builds the list's record and judges nothing.
- **R-2. The run's model stays the alias `opus` at its default effort** until a TZ resolves A4's two readings. An analysis run started before then runs on whatever `opus` resolves to.
- **R-3. The list read's memory under the service's `MemoryMax=128M` was not measured.** `tz58-list` was stopped before its `MemoryPeak` was read. C1's root unit peaked at 18 190 336 bytes. The list read holds about 1.6 MB of children and 8 329 ids.
- **R-4. `/var/lib/cryptorun` was not read.** §4 authorises no read there. That A4's unit wrote nothing under it rests on D-2's probe of the same binary and the same two commands, not on a reading of that directory.
- **R-5. The fit rests on one completed run.** The other run was account-limited and answers nothing about size. The first six runs after TZ-57's merge are the next TZ's reading (§5).

## Commit

Implementation, on the branch, already pushed: `a172529`. Message, verbatim from §14:

```
TZ-58: vps — the fit from the product's own runs, the pinned model, the stream listed, the exchange's own list
```

Contents: `vps/exchange.py`, `vps/selftest.py`, `vps/memory-record.txt`, `vps/manifest`.

Report, direct to `main` on the `CryptoReports/**` path (contract §8). Message, from §14:

```
TZ-58: report — on the VPS: the fit, the model, the stream and the list
```

Contents: `CryptoReports/TZ-58-vps-fit-model-stream-list-report-2.md` only.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/47. Base `main`, head `tz-58-vps-fit-model-stream-list` at `a172529`.

## CI Execution

- **`bench.yml`, run 37150094049** (`Bench gate`), event `pull_request`, head `a17252950267c2d0261ee96238784415ddae5453`, conclusion **`success`**, read with `gh` and the REST API.
  - Job `bench` (111281956782): steps 6–19, the 14 bench steps, each `success`. Step 18 is `analyst/live-gate.sh --selftest`, and step 19 is `backtest_guard_bench.py`.
  - No step reads `vps/` (Pre-existing Issues).
- The branch push did not start `bench.yml`'s `push` event. That event's `branches` filter is `[ main, 'claude/**' ]`, and this branch is `tz-58-…`.
- **`main.yml`** did not run. Its `push` trigger is limited to `main`, behind a `paths` allow-list of exactly `main.py` and `.github/workflows/main.yml`. This was re-read before the report's push, and it is still an allow-list. This report's path is on neither list.

## Final Repository State

- The branch `tz-58-vps-fit-model-stream-list` is at `a17252950267c2d0261ee96238784415ddae5453`, pushed: `git rev-parse HEAD origin/tz-58-vps-fit-model-stream-list` gave the same SHA twice.
- Its `vps` tree is `94a55b6f07d6aa6b2290eb3b4646f1740cd1a47e`.
- The working tree was clean (`git status --porcelain` printed 0 lines) after the implementation commit, and `vps/__pycache__` was removed.
- On the host this session leaves no unit, no transient file and no scratch directory (V9).
- `systemctl list-unit-files 'crypto-*'` reads as it did at A2: `crypto-announce.service` is `disabled`. The deployed marker is still `c4eef2b…`.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

All taken at `origin/main` = `44e4313e01cb905351c59aa554bc0cfa02ee9eff`, with `git show origin/main:<file> | wc -l` and `| md5sum`.

| File | Lines | MD5 | TZ-58 §0 requires |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 3193 | `b5a4478afd3afebd24c4ec12897514dc` | 3193 · `b5a4478afd3afebd24c4ec12897514dc` (reported) |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | 3799 · `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 · `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 · `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 · `3b8730b254467c9df4c0a845a0f3cfb3` |
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | 991 · `d7bd23785656896a119e0cb7f0fddad5`; version line `**Version 26.**` |
| `ANALYST-INSTRUCTIONS.md` | 3921 | `7f19dc64a596ee07ad8298ee2a59c8a4` | 3921 · `7f19dc64a596ee07ad8298ee2a59c8a4`; revision `**Revision 2026-10-03-a.**` |

Version and revision lines (`grep -n -m1 -F`):

- The map, line 17: `**Revision 2026-10-03-d.** No file of the table below moves. …`. TZ-58 requires `**Revision 2026-10-03-d.**`, and they are equal.
- `EXECUTOR-INSTRUCTIONS.md`, line 3: `**Version 26.** Permanent operating contract…`.
- `ANALYST-INSTRUCTIONS.md`, line 4: `` `EXECUTOR-INSTRUCTIONS.md`). **Revision 2026-10-03-a.** ``. This is the revision TZ-58 was written against, so there is no finding.

`origin/main:vps` = `c4eef2b1d03991c05a27464038f60d2a3307c14a`. That is TZ-57's branch tree, the one TZ-58 was written against, so there is no finding.

**Anchors.** The list was cut from the map's anchor table by its structure: the rows between the separator line under `| Anchor | Exact string that must be present |` (map line 477) and the table's end. It was compared with the TZ header's table, cut the same way (TZ line 25).

**The map table has 7 rows, and 7 were compared.** The TZ table has 7 rows. TZ anchors absent from the map table: none. Mismatches: 0.

Per anchor, the command is `git show origin/main:SYSTEM-MAP-CRYPTOCALCUL.md | grep -n -o -m1 -F -- '<anchor>'`. Each anchor's TZ quote equals the map's cell character for character. "Lines matched" is a second pass, `grep -n -F`, which lists every line carrying the anchor.

| Anchor | Text the match returned | Lines matched |
|---|---|---|
| revision | `17:**Revision 2026-10-03-d.**` | 17, 479 |
| direction engine | `480:### 3.12 Direction engine — veto cascade` | 480, 1449 |
| catalyst registry | `481:### 3.15 Catalyst registry` | 481, 1839 |
| exhaustion measure | `482:### 3.16 List exhaustion — the day-range measure` | 482, 1936 |
| analytical engine | `483:## 11. Analytical engine` | 483, 2950 |
| squeeze block | `484:### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 484, 2103 |
| newest invariant | `485:72. **A write that fails leaves this run's product or nothing` | 485, 2645 |

Each anchor occurs in the map outside its own table row as well: the second line number in each row. Those lines are the section heading, the invariant itself (line 2645), or for the revision anchor the `## 0` block's revision line (line 17). So no anchor is satisfied only by the table that names it.
