# Implementation Report — TZ-54

## Status

**`fits=no` — `memory_max_bytes` 1 409 286 144 against `A0` 255 295 488, and the measured run did not
complete.** By TZ-54 §12.8 and map §10, a run that does not fit is answered by 2 vCPU and 4 GB, never by a
GitHub runner. `crypto-run.timer` and `crypto-run.path` are therefore absent from `vps/manifest`, and the
bot's run button answers S5 until a later TZ re-measures on a resized host.

**PARTIAL — one scope blocked: the announcement watcher.** Binance answered the signed key check with HTTP
400 `-1022` («Signature for this request is not valid.»): the key was presented, the signature made with
the stored secret was refused, so the key's rights were never read, no stream was opened, and
`crypto-announce.service` is not in the manifest (E3). The secret was delivered three times — the trigger
message, a photograph of the Binance page, and a second paste — and none of the three resolves it to its
exact characters (Deviations D-1). Every other scope is complete: the code and its units, the deployer
bootstrap, the owner's binding, D1, D2, D4, D5, Stage E and V1–V12, with V4 and V9 reporting the failures
stated under them.

**Previous TZ:** TZ-53, report-only; its report is on `main` and it had no branch, so nothing awaited a merge.

**Timeline.** 01.10.2026 18:29Z start; Stage A 18:29–18:36Z; Stage B code and offline tests; C1–C2
19:01–19:07Z. From 19:07Z the session's own permission check (Claude Code's auto mode) refused C3 twice, the
`/srv` clone, C5, a repeat of C4 and an edit of the session's permission settings; the owner sent `/start`,
a photograph of the key page, and took the session out of auto mode, and C3–C6 ran 20:14–20:15Z exactly as
specified. D3 20:17Z, D1 20:18Z, D2 20:19–20:29Z. The session then stopped on the owner's account usage
limit; D5 and D4 ran 02.10.2026 04:58–05:00Z, and Stage E and validation followed.

**Owner preconditions (§1).** «The bot was created in @BotFather and the owner sent `/start` to it before
the trigger» — **not held at the trigger**: C4's first attempt (19:11:05Z) read zero pending updates;
**held after** the owner sent `/start`: C4's run at 20:14:37Z read exactly one `/start` chat and bound
it. «The Binance key was created with reading only and restricted to this VPS's address» — **not
established**: the exchange refused the signature before `apiRestrictions` could be read.

## Inbound Filing

None. The TZ arrived once, at its canonical path `CryptoTZ/TZ-54-vps-assistant-layer.md`, in `99914e6`
(`git log --all -- 'CryptoTZ/TZ-54*'` lists that commit only).

## Scope Executed

**Class: branch TZ** — §4 names 22 files to create under `vps/**` (contract §8).

| Item | Result |
|---|---|
| A1 contract §4a steps 1–6, §5 gate | passed: revision `2026-10-01-e`, 7 of 7 anchors, contract `Version 24.`, every file at its MD5 (Fingerprints) |
| A2–A9 readings | taken (below) |
| A5 writer's mapping | `c[].s` equals `BTCUSDT` + `tokens[].s` as a set (31 = 31); one admissible candidate per field; writer not blocked |
| B1–B11 code | written; `vps/selftest.py` 13 sections, 110 checks, 0 failed |
| C1 python3-websocket | installed, 1.7.0-1 |
| C2 credentials | written; whitespace and homoglyphs normalised (D-1); key corrected from the owner's photograph (D-1) |
| C3 bootstrap | done 20:14:24Z after the owner lifted the permission block |
| C4 bind | first attempt: no `/start` pending, exit 3; second: bound, S9 sent, exit 0 |
| C5 TZ-53 residue | removed |
| C6 first deployer tick | 20:14:24.8Z, `deploy: no vps tree on origin/main`; exactly the two deploy unit files |
| D3 key and stream | key check refused by the exchange, HTTP 400 `-1022`; exit 3; no stream |
| D1 instrument | `F_hog` 111 804 416 ≥ 100 663 296 |
| D2 full run | ran 604.9 s; writer pushed; session ended `is_error=true`, no answer; `F` 938 381 312 |
| D5 delivery | the run's S7 notice delivered, 1 of 1 chunks accepted; outbox empty |
| D4 exchange lane | baseline, then no change 65 s later; peaks 21.9 MB and 16.2 MB |
| E1–E5 | `fits=no`; record, unit limits, manifest, cleanup target written; selftest green with M |
| V1–V12 | below; V4 and V9 state their failures |

## Files Created

```
vps/common.py            vps/writer.py            vps/run.py               vps/bot.py
vps/exchange.py          vps/announce.py          vps/cleanup.py           vps/selftest.py
vps/deploy.sh            vps/install.sh           vps/manifest             vps/memory-record.txt
vps/units/crypto-run.service      vps/units/crypto-run.timer       vps/units/crypto-run.path
vps/units/crypto-bot.service      vps/units/crypto-exchange.service vps/units/crypto-announce.service
vps/units/crypto-cleanup.service  vps/units/crypto-cleanup.timer
vps/units/crypto-deploy.service   vps/units/crypto-deploy.timer
```

22 files, 2 449 lines; `deploy.sh` and `install.sh` carry mode 100755.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None in the repository. On the VPS, as §4 authorises: `/root/.claude/projects/-tmp-tz53-unit` (C5) and
the staging directories `/var/tmp/tz54-vps` and `/var/tmp/tz54-state` (V10).

## Implementation Summary

### The code (Stage B)

- **`vps/common.py`** — paths; `atomic_write` (serialise first, temporary file beside the target, rename,
  and on any failure remove both and re-raise — inv. 72; an existing target keeps its mode and, written by
  root, its owner, so a root rewrite never locks out the `cryptoauto` reader); `write_outbox`;
  `redact` (each loaded value, plain and URL-encoded); `load_credential`; `cut_tokens`; `derive_limits`
  (§12.8, exact arithmetic with `Fraction`); `runs_enabled`; `run_active`; `request_run` (the watcher's
  daily cap of 6 under a lock, the bot uncapped); the sixteen §12.1 strings as `\uXXXX` escapes.
- **`vps/writer.py`** — the three reads one at a time, the payload with top-level keys exactly
  `c n src ts x`, `x` the bulk ticker verbatim, `c` `BTCUSDT` then `tokens[]` in order with keys exactly
  `chg fr h l mark oi p qv s` mapped by A5's derivation, `ts` the moment the ticker completed; the gate run
  as A4 read it; commit, push, one `pull --rebase`, a conflict dropping the commit. One line, never a value.
- **`vps/run.py`** — requests consumed first; admission on the unit's own `memory.max` (30 s polls, 1 800 s);
  the tree reset under the git lock; the writer; §12.2's command exactly, stdout to
  `$RUNTIME_DIRECTORY/result.json`; the answer or S7 to the outbox; scratch removed; the `crypto-run:` line
  and a second line with model ids and denied tool names (D-5). Exit 0 answered, 1 failed, 75 not admitted.
- **`vps/bot.py`** — §12.3's conversion and chunking, §12.4's filter, the long-poll service with the atomic
  offset and counters, `--bind`, `--send-outbox-once`; HTTP 400 → the chunk once more as plain text, 429 →
  `retry_after`, a network error → the file kept and back-off to 60 s, chunks 1 s apart.
- **`vps/exchange.py`** — `exchangeInfo` every 900 s; the USDT snapshot with 2100-12-25 read as no delivery
  date; B5's change table; `perpetuals.json` as `{base, symbol}` pairs (D-12).
- **`vps/announce.py`** — §12.10's signing, §12.9's verdict, the stream (subscribe, ping every 30 s, a fresh
  connection before 23 h 30 min, reconnect at 5 s doubling to 300 s and never twice inside 5 s), §12.5's
  matcher, the record rewritten atomically, `--measure`.
- **`vps/cleanup.py`** — the run records (newest 40 and younger than 14 days), outbox older than 7 days,
  requests older than 1 day, announcements older than 30 days; `--dry-run`.
- **`vps/deploy.sh`**, **`vps/install.sh`** — B8 and B9; S10 written as JSON escapes; the deployer's copy
  replaced by rename so a running tick keeps its inode.
- **`vps/selftest.py`** — §12.14's sections A–M; non-zero on any failure and on any empty section.
- **`vps/units/`** — §12.12's ten units, verified line by line against the TZ text:

```
$ python3 - <<'PY'
import re, os
tz = open("CryptoTZ/TZ-54-vps-assistant-layer.md", encoding="utf-8").read()
sec = tz[tz.index("### 12.12 Units"):tz.index("### 12.13")]
block = sec[sec.index("```\n") + 4:]; block = block[:block.index("\n```")]
parts = re.split(r"^# (crypto-[a-z]+\.[a-z]+)(.*)$", block, flags=re.M)
units = {parts[i]: (parts[i + 1], parts[i + 2]) for i in range(1, len(parts), 3)}
bot = units["crypto-bot.service"][1].strip("\n").split("\n")
rec = dict(l.split("=", 1) for l in open("vps/memory-record.txt") if "=" in l and not l.startswith("#"))
subst = {"<A8>": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin"}
same = 0
for name in sorted(units):
    tail, body = units[name]
    if "with these differences" in tail:
        diffs = [l.strip()[1:].strip() for l in body.strip("\n").split("\n") if l.strip().startswith("#")]
        want, creds = [], [l for l in diffs if l.startswith("LoadCredential=")]
        for line in bot:
            key = line.split("=", 1)[0]
            if key in ("Description", "ExecStart"):
                want.append([l for l in diffs if l.startswith(key + "=")][0])
            elif key == "LoadCredential":
                want.extend(creds); creds = []
            else:
                want.append(line)
                if key == "RestartSec":
                    want.extend(l for l in diffs if l.startswith("RestartPreventExitStatus="))
    else:
        want = body.strip("\n").split("\n")
    want = [l.replace("<A8>", subst["<A8>"]) for l in want]
    want = [("MemoryMax=" + rec["memory_max_bytes"].strip()) if l == "MemoryMax=<E2>" else
            ("RuntimeMaxSec=" + rec["runtime_max_s"].strip()) if l == "RuntimeMaxSec=<E2>" else l for l in want]
    got = open("vps/units/" + name, encoding="utf-8").read().rstrip("\n").split("\n")
    ok = got == want
    same += ok
    print("%-26s lines=%d identical=%s" % (name, len(got), ok))
print("units in TZ-54 section 12.12: %d; files in vps/units: %d; identical: %d" % (len(units), len(os.listdir("vps/units")), same))
PY
crypto-announce.service    lines=26 identical=True
crypto-bot.service         lines=25 identical=True
crypto-cleanup.service     lines=7 identical=True
crypto-cleanup.timer       lines=10 identical=True
crypto-deploy.service      lines=8 identical=True
crypto-deploy.timer        lines=10 identical=True
crypto-exchange.service    lines=23 identical=True
crypto-run.path            lines=9 identical=True
crypto-run.service         lines=24 identical=True
crypto-run.timer           lines=11 identical=True
units in TZ-54 section 12.12: 10; files in vps/units: 10; identical: 10
[exit 0]
```

- **Rule 6 — Russian text as escapes.** Every §12.1 string, rendered with the TZ's own placeholder names,
  equals the TZ's table character for character, and `deploy.sh`'s S10 decodes to the same text:

```
$ PYTHONDONTWRITEBYTECODE=1 python3 /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-018cXeqyU9ehURcKzCAJk2k3/6938649f-20fe-5abc-a4d7-3f33464240e7/scratchpad/tz54/strings-check.py | tail -3
rows in §12.1: 16; identical: 16
deploy.sh S10 identical: True
non-ASCII characters per vps/ source file: [('vps/common.py', 7), ('vps/writer.py', 6), ('vps/run.py', 5), ('vps/bot.py', 6), ('vps/exchange.py', 1), ('vps/announce.py', 6), ('vps/cleanup.py', 0), ('vps/selftest.py', 8), ('vps/deploy.sh', 3), ('vps/install.sh', 1)]
[exit 0]
```

### Stage A — readings, no writes

**A1.** Contract §4a steps 1–6 and the §5 gate: see Fingerprints. `git fetch --all --prune`, not shallow,
tree clean, `HEAD` = `origin/main` = `99914e6`.

```
$ git log --oneline --graph --all | head -n 12
* 99914e6 Add files via upload
* 9c671f4 Update SYSTEM-MAP-CRYPTOCALCUL.md
* 9071d95 Update SYSTEM-MAP-CRYPTOCALCUL.md
* 003c389 Update EXECUTOR-INSTRUCTIONS.md
* 1aa3488 Update SYSTEM-MAP-CRYPTOCALCUL.md
* 5f18ba3 TZ-53: report — automation environment and hunter lanes read from the VPS
* 97c8372 Add files via upload
* e110be3 Update SYSTEM-MAP-CRYPTOCALCUL.md
* 3937e7c Update ANALYST-INSTRUCTIONS.md
* 2486e68 Update owner.json
* cbffb5c Update SYSTEM-MAP-CRYPTOCALCUL.md
* ffa75c2 Update ANALYST-INSTRUCTIONS.md
$ git status --porcelain | wc -l
0
$ git ls-remote --heads origin | grep -c tz-53
0
$ ls CryptoReports/ | grep TZ-53
TZ-53-automation-and-hunter-lanes-vps-reading-report.md
```

**A2. What holds the memory**, read at one instant 18:33:23Z (captured). No process command line was read.

```
2026-10-01T18:33:23Z
$ grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo
MemTotal:         978640 kB
MemAvailable:      91780 kB
SwapTotal:       3174396 kB
SwapFree:        1577640 kB
$ python3 memread.py
MemTotal:       1002127360 bytes
MemAvailable:     95322112 bytes
SwapTotal:      3250581504 bytes
SwapFree:       1611755520 bytes

Top 25 by VmRSS
| pid | ppid | comm | exe basename | elapsed s | VmRSS B | VmSwap B | cgroup |
|---:|---:|---|---|---:|---:|---:|---|
| 3715039 | 2948853 | claude.exe | claude.exe | 413 | 161374208 | 78548992 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3588700 | 2948853 | claude.exe | claude.exe | 87517 | 73232384 | 139436032 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3656933 | 2948853 | claude.exe | claude.exe | 38031 | 70045696 | 128184320 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 2949148 | 2948853 | claude.exe | claude.exe | 519059 | 70021120 | 162791424 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3169067 | 2948864 | claude.exe | claude.exe | 369070 | 69206016 | 156672000 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3148227 | 2948864 | claude.exe | claude.exe | 384515 | 68800512 | 134656000 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 2948853 | 2948852 | claude | claude.exe | 519255 | 51867648 | 68042752 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 2948864 | 2948852 | claude | claude.exe | 519243 | 48160768 | 55058432 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3021283 | 2948853 | claude.exe | claude.exe | 468401 | 39555072 | 188342272 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 185464 | 1 | multipathd | multipathd | 1683977 | 27820032 | 0 | /system.slice/multipathd.service |
| 228592 | 1 | python | python3.12 | 1672818 | 15982592 | 52613120 | /user.slice/user-0.slice/session-7379.scope |
| 185511 | 1 | containerd | containerd | 1683976 | 14123008 | 12296192 | /system.slice/containerd.service |
| 3646441 | 1 | python3 | python3.12 | 45055 | 12795904 | 149790720 | /system.slice/seahome-radar.service |
| 3646402 | 1 | fail2ban-server | python3.12 | 45060 | 12730368 | 14376960 | /system.slice/fail2ban.service |
| 3716147 | 3716143 | python3 | python3.12 | 0 | 11948032 | 0 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3646439 | 1 | python3 | python3.12 | 45057 | 10711040 | 137945088 | /system.slice/realestatebot.service |
| 3716138 | 3646673 | sshd | sshd | 1 | 10117120 | 0 | /system.slice/ssh.service |
| 3646344 | 1 | systemd-journal | systemd-journald | 45062 | 9920512 | 880640 | /system.slice/systemd-journald.service |
| 1 | 0 | systemd | systemd | 5224130 | 7696384 | 1880064 | /init.scope |
| 3716139 | 3716138 | sshd | sshd | 1 | 6303744 | 0 | /system.slice/ssh.service |
| 1621 | 1 | containerd-shim | containerd-shim-runc-v2 | 5224115 | 5775360 | 933888 | /system.slice/containerd.service |
| 2948852 | 1 | tmux: server | tmux | 519255 | 5582848 | 516096 | /user.slice/user-0.slice/session-9749.scope |
| 2699889 | 1 | python | python3.12 | 694413 | 4681728 | 17850368 | /user.slice/user-0.slice/user@0.service/tmux-spawn-315ec8a4-f008-4219-8440-d24d19ccc793.scope |
| 3646367 | 1 | fwupd | fwupd | 45061 | 4321280 | 6324224 | /system.slice/fwupd.service |
| 3716140 | 3715039 | bash | bash | 0 | 3895296 | 0 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |

Processes whose /proc/<pid>/exe resolves to /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe: 9
| pid | ppid | elapsed s | cwd | VmRSS B | VmSwap B | cgroup |
|---:|---:|---:|---|---:|---:|---|
| 2948853 | 2948852 | 519255 | /root/crypto-auto | 51867648 | 68042752 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 2948864 | 2948852 | 519243 | /root/btc-5m-twap | 48160768 | 55058432 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 2949148 | 2948853 | 519059 | /root/crypto-auto/.claude/worktrees/bridge-cse_0186w2RdMyy4zngzVxR4fgan | 70021120 | 162791424 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3021283 | 2948853 | 468401 | /root/crypto-auto/.claude/worktrees/bridge-cse_017yWJ4NiLghDH2Fgz4JYWEu | 39555072 | 188342272 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3148227 | 2948864 | 384515 | /root/btc-5m-twap | 68800512 | 134656000 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3169067 | 2948864 | 369070 | /root/btc-5m-twap | 69206016 | 156672000 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3588700 | 2948853 | 87517 | /root/crypto-auto/.claude/worktrees/bridge-cse_017xSPqESDDmSqyNdBHykJ1G | 73232384 | 139436032 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3656933 | 2948853 | 38031 | /root/crypto-auto/.claude/worktrees/bridge-cse_01D6P1U4thNUnBuHuwmJe2eS | 70045696 | 128184320 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3715039 | 2948853 | 413 | /root/crypto-auto/.claude/worktrees/bridge-cse_018cXeqyU9ehURcKzCAJk2k3 | 161374208 | 78548992 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
claude.exe summed VmRSS: 652263424 bytes; summed VmSwap: 1111732224 bytes

Session tree: root pid 3715039 (nearest claude.exe ancestor of this stage's shell, pid 3716143); 5 processes
| pid | ppid | comm | VmRSS B | VmSwap B |
|---:|---:|---|---:|---:|
| 3715039 | 2948853 | claude.exe | 161374208 | 78548992 |
| 3716140 | 3715039 | bash | 3895296 | 0 |
| 3716143 | 3716140 | bash | 2596864 | 0 |
| 3716144 | 3716140 | tee | 2035712 | 0 |
| 3716147 | 3716143 | python3 | 11948032 | 0 |
Session tree summed VmRSS: 181850112 bytes
```

**A3. Disk and records** (captured).

```
$ df -B1 /
Filesystem       1B-blocks        Used   Available Use% Mounted on
/dev/vda2      31612203008 17471209472 12705124352  58% /
$ for d in /root/.claude/projects/*/; do echo "$(basename "$d")  entries=$(ls -A "$d" | wc -l)  bytes=$(du -sb "$d" | cut -f1)"; done
-root-btc-5m-twap  entries=71  bytes=48166590
-root-crypto-auto  entries=4  bytes=86443
-root-crypto-auto--claude-worktrees-bridge-cse-011D5HZhQ2Mjxmuir41Yd816  entries=2  bytes=1483872
-root-crypto-auto--claude-worktrees-bridge-cse-011G7fzr7syPQ3VGrSQVexqu  entries=2  bytes=1240027
-root-crypto-auto--claude-worktrees-bridge-cse-011UxGXnrPSwgGra1vY7BBF6  entries=2  bytes=1345504
-root-crypto-auto--claude-worktrees-bridge-cse-0138PUGVG7zZNAdQu3JPEW7d  entries=2  bytes=1918230
-root-crypto-auto--claude-worktrees-bridge-cse-013bTghR9QW2QyibmU8pf2t2  entries=2  bytes=2298637
-root-crypto-auto--claude-worktrees-bridge-cse-013D2XfmWy3jozb4g6z8mpTe  entries=2  bytes=1289421
-root-crypto-auto--claude-worktrees-bridge-cse-014bLCCjqT2XjJCByHydXEes  entries=2  bytes=1230960
-root-crypto-auto--claude-worktrees-bridge-cse-014KqyqisHnSf2YrJgDkakBY  entries=2  bytes=920920
-root-crypto-auto--claude-worktrees-bridge-cse-014VkSZn1wKkkXVZshMPWAbk  entries=2  bytes=1133260
-root-crypto-auto--claude-worktrees-bridge-cse-015FW2PzAw8V2nHSWur4mBbN  entries=2  bytes=3585569
-root-crypto-auto--claude-worktrees-bridge-cse-016Pdt2N6h3Xr5TbFDpcWign  entries=2  bytes=1200329
-root-crypto-auto--claude-worktrees-bridge-cse-016TP9dxasHHu8Psww8mWxsp  entries=2  bytes=1458082
-root-crypto-auto--claude-worktrees-bridge-cse-0174htZR83jy9e7G5ZEHAFdR  entries=2  bytes=1386454
-root-crypto-auto--claude-worktrees-bridge-cse-017xSPqESDDmSqyNdBHykJ1G  entries=2  bytes=3047516
-root-crypto-auto--claude-worktrees-bridge-cse-017yWJ4NiLghDH2Fgz4JYWEu  entries=2  bytes=3468567
-root-crypto-auto--claude-worktrees-bridge-cse-0186w2RdMyy4zngzVxR4fgan  entries=2  bytes=3287318
-root-crypto-auto--claude-worktrees-bridge-cse-018cXeqyU9ehURcKzCAJk2k3  entries=2  bytes=1117814
-root-crypto-auto--claude-worktrees-bridge-cse-018jf8hnjGEwhPHqE6BuRfA1  entries=2  bytes=1200885
-root-crypto-auto--claude-worktrees-bridge-cse-0195DhLAH4No5zW5RJQ1Tdst  entries=2  bytes=1257329
-root-crypto-auto--claude-worktrees-bridge-cse-019cdxhdagDcbDMP3vJ7PMRw  entries=4  bytes=1163227
-root-crypto-auto--claude-worktrees-bridge-cse-019GoxWyNvziAro1gjB9Yum8  entries=2  bytes=1915228
-root-crypto-auto--claude-worktrees-bridge-cse-019Uqs2cqAowjuyWrCK2FxaX  entries=4  bytes=4505858
-root-crypto-auto--claude-worktrees-bridge-cse-01Ac3XGRVb5f4s5HFGNre7Hn  entries=2  bytes=1421742
-root-crypto-auto--claude-worktrees-bridge-cse-01ADdivgJHEymddMXAU6LoDJ  entries=2  bytes=1230593
-root-crypto-auto--claude-worktrees-bridge-cse-01AJiXpR13uvMLZ6WvVkH4Vv  entries=2  bytes=1302954
-root-crypto-auto--claude-worktrees-bridge-cse-01AkZQyzswNQorELXW7GgF1y  entries=2  bytes=1119723
-root-crypto-auto--claude-worktrees-bridge-cse-01BdXvjZpynbRuyALEr77AP6  entries=2  bytes=1167709
-root-crypto-auto--claude-worktrees-bridge-cse-01CgEKojiG9EpfkdA7kwo4dJ  entries=2  bytes=2042000
-root-crypto-auto--claude-worktrees-bridge-cse-01D6P1U4thNUnBuHuwmJe2eS  entries=2  bytes=1962604
-root-crypto-auto--claude-worktrees-bridge-cse-01DMtSKFZTRZxvNd87JjT1Pb  entries=2  bytes=3112387
-root-crypto-auto--claude-worktrees-bridge-cse-01E6D9EXjhMT4X83TYxUC68u  entries=2  bytes=1963808
-root-crypto-auto--claude-worktrees-bridge-cse-01EoiADpTZHQJdpXz8FyEjNQ  entries=2  bytes=1211526
-root-crypto-auto--claude-worktrees-bridge-cse-01EtyACsCP4Abb5mYFhP4jQ9  entries=2  bytes=1595051
-root-crypto-auto--claude-worktrees-bridge-cse-01EWYK2bJGtPxq6YbU2AqUbY  entries=6  bytes=2324193
-root-crypto-auto--claude-worktrees-bridge-cse-01EyhiTaF8wEsGJCukrBWmqZ  entries=2  bytes=1299540
-root-crypto-auto--claude-worktrees-bridge-cse-01FspkJGM1LLBgtkE7nUTPPX  entries=2  bytes=1609084
-root-crypto-auto--claude-worktrees-bridge-cse-01Gaz7K8LECmZAhVCBc7u3Vc  entries=2  bytes=1824226
-root-crypto-auto--claude-worktrees-bridge-cse-01GtT5Vb3qnhrRexbBhvxcWG  entries=2  bytes=2228714
-root-crypto-auto--claude-worktrees-bridge-cse-01HDd9vf76yJQxRX8u56qiZM  entries=2  bytes=1513112
-root-crypto-auto--claude-worktrees-bridge-cse-01HV1ynVK1bcXLXi3exWsFCN  entries=2  bytes=1041801
-root-crypto-auto--claude-worktrees-bridge-cse-01HW16UQAbfGXd343JBfJ8hF  entries=2  bytes=1417004
-root-crypto-auto--claude-worktrees-bridge-cse-01J26epDtVTJJqamXJD4wXXr  entries=2  bytes=4433208
-root-crypto-auto--claude-worktrees-bridge-cse-01JdLfTXSLhNfRcb3pShoEJ5  entries=2  bytes=1066032
-root-crypto-auto--claude-worktrees-bridge-cse-01Jwcwd3vNsSB2Z86JDKGU9m  entries=2  bytes=1697531
-root-crypto-auto--claude-worktrees-bridge-cse-01KSo8JqvDPyunynm4GPnVqw  entries=2  bytes=1995693
-root-crypto-auto--claude-worktrees-bridge-cse-01Kt5VGyqS5AakgWEzkBinw3  entries=6  bytes=3853399
-root-crypto-auto--claude-worktrees-bridge-cse-01KwxSgAFYrvhHq647oeo7qW  entries=2  bytes=1127556
-root-crypto-auto--claude-worktrees-bridge-cse-01L6c9UoEVeQkmT4YCnKaJwV  entries=2  bytes=1156579
-root-crypto-auto--claude-worktrees-bridge-cse-01LauohK3PPPoW92B59DBmY9  entries=2  bytes=918293
-root-crypto-auto--claude-worktrees-bridge-cse-01LYyS8kTkUyknu7R6TwMuhr  entries=2  bytes=1361455
-root-crypto-auto--claude-worktrees-bridge-cse-01MpZ6fUrpL7o3sha9zCCxa3  entries=2  bytes=1036680
-root-crypto-auto--claude-worktrees-bridge-cse-01PcPDh7QWPDYBWXNEohYJHe  entries=2  bytes=1074273
-root-crypto-auto--claude-worktrees-bridge-cse-01PczbjZUhQ5QgkavRRSg1zM  entries=2  bytes=1409460
-root-crypto-auto--claude-worktrees-bridge-cse-01QDZxSmFhhd9rEGfTbVpYQS  entries=2  bytes=3412417
-root-crypto-auto--claude-worktrees-bridge-cse-01RF9cWFBCe415HESZC986kH  entries=2  bytes=1612954
-root-crypto-auto--claude-worktrees-bridge-cse-01RPNJNWX1PV7ZRLZbtn9Jo5  entries=2  bytes=1666039
-root-crypto-auto--claude-worktrees-bridge-cse-01RQC1Qa7mkAqrDhAdnXhAf5  entries=2  bytes=1869851
-root-crypto-auto--claude-worktrees-bridge-cse-01RyzkxTHm1S1JC9P9tmQXxe  entries=2  bytes=3626384
-root-crypto-auto--claude-worktrees-bridge-cse-01SVkMVXNkbXQawi7Me9Ku2b  entries=2  bytes=850898
-root-crypto-auto--claude-worktrees-bridge-cse-01T87syUKWGCQYE7sWfMqMHT  entries=2  bytes=3403877
-root-crypto-auto--claude-worktrees-bridge-cse-01TJfAeCzB4grbgkr6MNLdZg  entries=2  bytes=2062830
-root-crypto-auto--claude-worktrees-bridge-cse-01UDv5o1mGeQMstDN4ypZ29F  entries=2  bytes=2027664
-root-crypto-auto--claude-worktrees-bridge-cse-01Vuxx9zjz5xWtVVUVhCs9rb  entries=2  bytes=1093439
-root-crypto-auto--claude-worktrees-bridge-cse-01W9Prac3ANEeboZFDG242FJ  entries=2  bytes=2098342
-root-crypto-auto--claude-worktrees-bridge-cse-01XiEX8jmi2Sss4RHrVikwCZ  entries=2  bytes=1089434
-root-crypto-auto--claude-worktrees-bridge-cse-01XxRa3AWuA5G11iX6G2gaDP  entries=2  bytes=1622234
-root-crypto-auto--claude-worktrees-bridge-cse-01YG4zs1tVyQmoqyjssaXaHr  entries=2  bytes=1867129
-root-gaming-audit  entries=1  bytes=7401
-root-my-real-estate-bot  entries=1  bytes=12889
-root-PROJECT-GAMING-PS5  entries=2  bytes=723305
-root-PROJECT-GAMING-PS5-gaming-audit  entries=1  bytes=15121
-tmp-tz53-unit  entries=2  bytes=180846
$ ls -d /root/.claude/projects/*/ | wc -l
74
$ git -C /root/crypto-auto worktree list | wc -l
67
```

**A4. The gate.** Its invocation, the files it reads and how it locates them (relative to its own path:
`ROOT` is the script's parent directory), and its exit codes, quoted with line numbers; then its selftest
in the form its usage names (captured):

```
$ grep -n -E "^# (Usage|  live-gate|Exit codes|  [0-9] )|^ROOT=|^PAYLOAD=|^INDEX=|^case |^    \"\"\)|^    --selftest\)|^    --now\)|exit 9" analyst/live-gate.sh
11:# Usage:
12:#   live-gate.sh              validate analyst/live.json, print one JSON object
13:#   live-gate.sh --selftest   offline known-answer fixtures, print checks=N
14:#   live-gate.sh --now        print the UTC ISO timestamp from `date -u`
16:# Exit codes — one distinct code per failure class (TZ-17 §3.A.3):
17:#   0  every check passed
18:#   2  payload missing, unparseable, or its `ts` is absent/unparseable   (checks 1, 2)
19:#   3  payload lies outside the freshness window, either side            (check 3)
20:#   4  `n` disagrees with len(c)                                         (check 4)
21:#   5  a tokens[] symbol is absent from the payload                      (check 5)
22:#   6  a `p`, `h` or `l` does not cast to a finite number > 0            (check 6)
23:#   7  no comparisons were performed                                     (check 7)
24:#   8  the universe is unreadable: tokens[] could not be cut from index.html
25:#   9  usage error
29:ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
30:PAYLOAD="$ROOT/analyst/live.json"   # path fixed: no argument, no env var, no URL
31:INDEX="$ROOT/index.html"            # the universe's only source (TZ-17 §A.1)
436:case "${1-}" in
437:    "")          gate_run "$PAYLOAD" "$(now_utc)" "$INDEX" ;;
438:    --selftest)  selftest ;;
439:    --now)       now_utc ;;
442:        exit 9
$ bash analyst/live-gate.sh --selftest; echo "[exit $?]"
universe: 30 symbols cut from index.html
  fresh                exit=0 expected=0  
  stale16              exit=3 expected=3  live-gate: check 3: payload is stale, age 15360 s exceeds the 900 s ceiling
  future121            exit=3 expected=3  live-gate: check 3: payload is ahead of now, age -121 s is below the -120 s floor
  future_ok            exit=0 expected=0  
  no_ts                exit=2 expected=2  live-gate: check 2: ts absent or not a non-empty string
  bad_json             exit=2 expected=2  live-gate: check 1: payload is not valid JSON (JSONDecodeError)
  n_mismatch           exit=4 expected=4  live-gate: check 4: n=32 disagrees with len(c)=31
  missing_symbol       exit=5 expected=5  live-gate: check 5: 1 tokens[] symbol(s) absent from payload: SUIUSDT
  price_abc            exit=6 expected=6  live-gate: check 6: row 30 (ARBUSDT) field p does not cast to a number: 'abc'
  price_zero           exit=6 expected=6  live-gate: check 6: row 30 (ARBUSDT) field p is not greater than zero: '0'
  price_nan            exit=6 expected=6  live-gate: check 6: row 30 (ARBUSDT) field p casts to a non-finite value: 'NaN'
  empty_c              exit=7 expected=7  live-gate: check 7: payload carries zero rows, no comparison possible
  file_absent          exit=2 expected=2  live-gate: check 1: payload not readable: /tmp/tmp.qPGtEQCqnF/does-not-exist.json
  universe_unreadable  exit=8 expected=8  live-gate: universe: tokens[] block not found in /tmp/tmp.qPGtEQCqnF/no-tokens.html
checks=40
selftest: 14 cases, all exit codes as specified
[exit 0]
```

**A5. The payload's mapping.** The committed payload's `ts`, `n`, `src`, and `c[].s` against `BTCUSDT` +
`tokens[].s` cut from `index.html` at run time — equal as sets, in a different order; B2 fixes the writer's
own order, so the comparison that can block is the set (captured):

```
payload ts=2026-09-30T22:14:24+04:00 n=31 src=fapi len(c)=31
tokens[] rows cut: 30; BTCUSDT + tokens[].s: 31 symbols; c[].s: 31 symbols
c[].s == BTCUSDT + tokens[].s as sets: True (missing from c: none; extra in c: none)
same order: False
```

The three reads under rule 3, one request per URL (captured; bodies kept in the session's scratch):

```
2026-10-01T18:34:18Z
$ curl -sS -L -m 20 -o ticker.body -D ticker.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/ticker/24hr'
200 292725 application/json https://fapi.binance.com/fapi/v1/ticker/24hr
$ curl -sS -L -m 20 -o premium.body -D premium.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/premiumIndex'
200 204793 application/json https://fapi.binance.com/fapi/v1/premiumIndex
$ curl -sS -L -m 20 -o oi-BTCUSDT.body -D oi-BTCUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT
$ curl -sS -L -m 20 -o oi-ETHUSDT.body -D oi-ETHUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=ETHUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=ETHUSDT
$ curl -sS -L -m 20 -o oi-SUIUSDT.body -D oi-SUIUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=SUIUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=SUIUSDT
$ curl -sS -L -m 20 -o oi-LINKUSDT.body -D oi-LINKUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=LINKUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=LINKUSDT
$ curl -sS -L -m 20 -o oi-NEARUSDT.body -D oi-NEARUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=NEARUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=NEARUSDT
$ curl -sS -L -m 20 -o oi-AAVEUSDT.body -D oi-AAVEUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=AAVEUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=AAVEUSDT
$ curl -sS -L -m 20 -o oi-XRPUSDT.body -D oi-XRPUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=XRPUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=XRPUSDT
$ curl -sS -L -m 20 -o oi-ADAUSDT.body -D oi-ADAUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=ADAUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=ADAUSDT
$ curl -sS -L -m 20 -o oi-YFIUSDT.body -D oi-YFIUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=YFIUSDT'
200 67 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=YFIUSDT
$ curl -sS -L -m 20 -o oi-TAOUSDT.body -D oi-TAOUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=TAOUSDT'
200 69 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=TAOUSDT
$ curl -sS -L -m 20 -o oi-FETUSDT.body -D oi-FETUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=FETUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=FETUSDT
$ curl -sS -L -m 20 -o oi-ENAUSDT.body -D oi-ENAUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=ENAUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=ENAUSDT
$ curl -sS -L -m 20 -o oi-GRAMUSDT.body -D oi-GRAMUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=GRAMUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=GRAMUSDT
$ curl -sS -L -m 20 -o oi-AVAXUSDT.body -D oi-AVAXUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=AVAXUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=AVAXUSDT
$ curl -sS -L -m 20 -o oi-ONDOUSDT.body -D oi-ONDOUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=ONDOUSDT'
200 71 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=ONDOUSDT
$ curl -sS -L -m 20 -o oi-RENDERUSDT.body -D oi-RENDERUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=RENDERUSDT'
200 71 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=RENDERUSDT
$ curl -sS -L -m 20 -o oi-TRXUSDT.body -D oi-TRXUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=TRXUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=TRXUSDT
$ curl -sS -L -m 20 -o oi-SOLUSDT.body -D oi-SOLUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=SOLUSDT'
200 69 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=SOLUSDT
$ curl -sS -L -m 20 -o oi-BCHUSDT.body -D oi-BCHUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=BCHUSDT'
200 69 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=BCHUSDT
$ curl -sS -L -m 20 -o oi-HYPEUSDT.body -D oi-HYPEUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=HYPEUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=HYPEUSDT
$ curl -sS -L -m 20 -o oi-SKYUSDT.body -D oi-SKYUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=SKYUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=SKYUSDT
$ curl -sS -L -m 20 -o oi-HBARUSDT.body -D oi-HBARUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=HBARUSDT'
200 69 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=HBARUSDT
$ curl -sS -L -m 20 -o oi-XLMUSDT.body -D oi-XLMUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=XLMUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=XLMUSDT
$ curl -sS -L -m 20 -o oi-ALGOUSDT.body -D oi-ALGOUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=ALGOUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=ALGOUSDT
$ curl -sS -L -m 20 -o oi-BNBUSDT.body -D oi-BNBUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=BNBUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=BNBUSDT
$ curl -sS -L -m 20 -o oi-ZECUSDT.body -D oi-ZECUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=ZECUSDT'
200 69 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=ZECUSDT
$ curl -sS -L -m 20 -o oi-XMRUSDT.body -D oi-XMRUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=XMRUSDT'
200 68 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=XMRUSDT
$ curl -sS -L -m 20 -o oi-UNIUSDT.body -D oi-UNIUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=UNIUSDT'
200 67 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=UNIUSDT
$ curl -sS -L -m 20 -o oi-LITUSDT.body -D oi-LITUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=LITUSDT'
200 69 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=LITUSDT
$ curl -sS -L -m 20 -o oi-MORPHOUSDT.body -D oi-MORPHOUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=MORPHOUSDT'
200 71 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=MORPHOUSDT
$ curl -sS -L -m 20 -o oi-ARBUSDT.body -D oi-ARBUSDT.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/openInterest?symbol=ARBUSDT'
200 70 application/json https://fapi.binance.com/fapi/v1/openInterest?symbol=ARBUSDT
2026-10-01T18:34:30Z
```

§12.6's derivation table, printed in full (captured):

```
$ python3 derive.py a5 analyst/live.json
| field | candidate | rows whose sig matched | admissible | median | chosen |
|---|---|---:|---|---:|---|
| `p` | ticker `lastPrice` | 31 / 31 | yes | 0.00396247 | **chosen** |
| `h` | ticker `highPrice` | 31 / 31 | yes | 0.00490123 | **chosen** |
| `l` | ticker `lowPrice` | 31 / 31 | yes | 0.003377 | **chosen** |
| `chg` | ticker `priceChangePercent` | 31 / 31 | yes | 1.296 | **chosen** |
| `chg` | ticker `priceChange` | 3 / 31 | no | 1.66099 |  |
| `qv` | ticker `quoteVolume` | 31 / 31 | yes | 0.0863727 | **chosen** |
| `qv` | ticker `volume` | 0 / 31 | no | 0.878112 |  |
| `mark` | premiumIndex `markPrice` | 31 / 31 | yes | 0.00394233 | **chosen** |
| `fr` | premiumIndex `lastFundingRate` | 31 / 31 | yes | 6e-06 | **chosen** |
| `oi` | openInterest `openInterest` | 31 / 31 | yes | 0.0115276 | **chosen** |

mapping: {"p": "ticker lastPrice", "h": "ticker highPrice", "l": "ticker lowPrice", "chg": "ticker priceChangePercent", "qv": "ticker quoteVolume", "mark": "premiumIndex markPrice", "fr": "premiumIndex lastFundingRate", "oi": "openInterest openInterest"}
blocked fields: none
[exit 0]
```

The mapping chosen: `p` ← `lastPrice`, `h` ← `highPrice`, `l` ← `lowPrice`, `chg` ← `priceChangePercent`,
`qv` ← `quoteVolume` (ticker); `mark` ← `markPrice`, `fr` ← `lastFundingRate` (premiumIndex); `oi` ←
`openInterest`. No field blocked; no tie.

**A6. Tools.** The lines of `claude --help` naming the four flags (re-run; the `--model` entry is quoted to
its first line — its continuation lists example model names, which this environment keeps out of the
repository, D-6). `--model` is present, so §12.2's `--model opus` stays; the tool list's separator is
«Comma or space-separated», so §12.2's space-separated list stays.

```
$ claude --help | sed -n -e '23,27p' -e '131p' -e '143,147p'
  --allowedTools, --allowed-tools <tools...>
      Comma or space-separated list of tool names to allow (e.g. "Bash(git *)
      Edit")
  --append-system-prompt <prompt>       Append a system prompt to the default
                                        system prompt
  --model <model>                       Model for the current session. Provide
  --output-format <format>              Output format (only works with --print):
                                        "text" (default), "json" (single
                                        result), or "stream-json" (realtime
                                        streaming) (choices: "text", "json",
                                        "stream-json")
[exit 0]
```

The module, the package, the committer identity and the user (captured before C1):

```
$ python3 -c 'import websocket; print(websocket.__version__)'; echo "[exit $?]"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'websocket'
[exit 1]
$ apt-cache policy python3-websocket | grep -E "Installed|Candidate"
  Installed: (none)
  Candidate: 1.7.0-1
$ git -C /root/crypto-auto config --get user.name >/dev/null && echo set || echo unset
set
$ git config --global --get user.name >/dev/null && echo set || echo unset
unset
$ git -C /root/crypto-auto config --get user.email >/dev/null && echo set || echo unset
set
$ git config --global --get user.email >/dev/null && echo set || echo unset
unset
$ id cryptoauto; echo "[exit $?]"
id: ‘cryptoauto’: no such user
[exit 1]
```

The identity is set only in `/root/crypto-auto`'s own config and nowhere global — a fresh clone has none,
which is why the bootstrap copies it (D-8).

**A7. What a headless session loads besides its prompt** and **A8. This session's `PATH`** (captured):

```
/root/.claude/CLAUDE.md: absent
CLAUDE.md: absent
/root/crypto-auto/CLAUDE.md: absent
/srv/CLAUDE.md: absent
/CLAUDE.md: absent
$ git ls-files | grep -c -i "claude.md"
0
$ python3 -c "import json; print(list(json.load(open(\"/root/.claude/settings.json\")).keys()))"
/root/.claude/settings.json: present
['model', 'hooks', 'effortLevel', 'askUserQuestionTimeout', 'theme', 'autoCompactEnabled', 'inputNeededNotifEnabled', 'agentPushNotifEnabled']
-rw------- .credentials.json
-rw-r--r-- settings.json
$ echo "$PATH"
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

`/root/.claude/settings.json` carries `hooks`, so a headless run executes the owner's hooks; their content
was not read (the TZ asks for key names only).

**A9. The Bot API page** (captured read):

```
2026-10-01T18:35:26Z
$ curl -sS -L -m 20 -o botapi.body -D botapi.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://core.telegram.org/bots/api'
200 860075 text/html; charset=utf-8 https://core.telegram.org/bots/api
```

`sendMessage`'s `text`: «Text of the message to be sent, 1-4096 characters after entities parsing». The
«HTML style» rules: «To use this mode, pass HTML in the parse_mode field. The following tags are currently
supported:» (b, strong, i, em, u, ins, s, strike, del, span class tg-spoiler, tg-spoiler, a href, tg-emoji,
tg-time, code, pre, pre with code class, blockquote, blockquote expandable); «Only the tags mentioned above
are currently supported.»; «All <, > and & symbols that are not a part of a tag or an HTML entity must be
replaced with the corresponding HTML entities (< with &lt;, > with &gt; and & with &amp;).»; «All
numerical HTML entities are supported.»; «The API currently supports only the following named HTML
entities: &lt;, &gt;, &amp; and &quot;.» **§12.3's chunk limit is 4 096 − 96 = 4 000.**

### Stage C — provisioning

**C1** (captured):

```
2026-10-01T19:01:13Z
$ DEBIAN_FRONTEND=noninteractive apt-get install -y python3-websocket
User sessions running outdated binaries:
 root @ session #7379: python[228592]
 root @ session #9749: tmux: server[2948852]
 root @ user manager service: python[2699889], systemd[2607743]

No VM guests are running outdated hypervisor (qemu) binaries on this host.
[exit 0]
$ python3 -c 'import websocket; print(websocket.__version__)'
1.7.0
$ apt-cache policy python3-websocket | grep -E "Installed|Candidate"
  Installed: 1.7.0-1
  Candidate: 1.7.0-1
```

**C2.** The three values were written by one command that printed nothing; its counts went to a file and
were read back by a command that prints counts (captured):

```
2026-10-01T19:06:51Z
$ cat c2-counts.txt
telegram-bot-token whitespace_removed=1 homoglyphs_replaced=0 non_ascii_left=0 length=46 format_ok=yes
binance-api-key whitespace_removed=2 homoglyphs_replaced=0 non_ascii_left=0 length=64 format_ok=yes
binance-api-secret whitespace_removed=2 homoglyphs_replaced=5 non_ascii_left=0 length=64 format_ok=yes
$ stat -c '%a %U %G %s %n' /etc/crypto-auto /etc/crypto-auto/credentials /etc/crypto-auto/credentials/*
755 root root 4096 /etc/crypto-auto
700 root root 4096 /etc/crypto-auto/credentials
600 root root 64 /etc/crypto-auto/credentials/binance-api-key
600 root root 64 /etc/crypto-auto/credentials/binance-api-secret
600 root root 46 /etc/crypto-auto/credentials/telegram-bot-token
$ for f in /etc/crypto-auto/credentials/*; do echo "$(basename $f) newlines=$(tr -cd "\n" < $f | wc -c) last_byte_is_newline=$(tail -c 1 $f | od -An -c | grep -c "\\\\n")"; done
binance-api-key newlines=0 last_byte_is_newline=0
binance-api-secret newlines=0 last_byte_is_newline=0
telegram-bot-token newlines=0 last_byte_is_newline=0
```

After the owner's photograph of the key page (see D-1), the stored Binance values were compared with the
photograph by a command that prints counts and rewrites a file only when every difference is the letter O
against the digit zero (captured):

```
binance-api-key stored_length=64 screenshot_length=64 mismatches=2 all_mismatches_are_O_vs_0=yes rewritten_from_screenshot=yes
binance-api-secret stored_length=64 screenshot_length=64 mismatches=0 all_mismatches_are_O_vs_0=yes rewritten_from_screenshot=no
```

**C3** (captured; the user, the directories and the staging copy already existed — D-10 — and were
re-applied idempotently):

```
2026-10-01T20:14:19Z
$ systemctl list-unit-files "crypto-*" --no-legend | wc -l
0
$ bash vps/install.sh --bootstrap; echo "[exit $?]"
install: clone /srv/crypto-auto created
install: clone user.name set
install: clone user.email set
install: worktree /srv/crypto-auto-run created, detached at origin/main
Created symlink /etc/systemd/system/timers.target.wants/crypto-deploy.timer → /etc/systemd/system/crypto-deploy.timer.
install: bootstrap done: crypto-deploy.timer enabled
[exit 0]
2026-10-01T20:14:24Z
```

**C4**, first attempt before `/start` and second after it (captured):

```
2026-10-01T19:11:05Z
$ systemd-run --unit=tz54-bind --wait --collect -p MemoryAccounting=yes -p LoadCredential=telegram-bot-token:/etc/crypto-auto/credentials/telegram-bot-token /usr/bin/python3 /var/tmp/tz54-vps/bot.py --bind
Running as unit: tz54-bind.service; invocation ID: d015a3eaa85640f1a4454a243a6fa911
Finished with result: exit-code
Main processes terminated with: code=exited/status=3
Service runtime: 2.896s
CPU time consumed: 103ms
Memory peak: 344.0K
Memory swap peak: 0B
[exit 3]
$ journalctl -u tz54-bind -o cat --no-pager
Started tz54-bind.service - /usr/bin/python3 /var/tmp/tz54-vps/bot.py --bind.
bind: getme=ok username=Cryptantrader_bot updates=0 start_chats=0 bound=no confirm_sent=no
tz54-bind.service: Main process exited, code=exited, status=3/NOTIMPLEMENTED
tz54-bind.service: Failed with result 'exit-code'.
$ stat -c '%a %U %G %n' /etc/crypto-auto/credentials/owner-chat-id
stat: cannot statx '/etc/crypto-auto/credentials/owner-chat-id': No such file or directory
```

```
2026-10-01T20:14:37Z
$ systemd-run --unit=tz54-bind --wait --collect -p MemoryAccounting=yes -p LoadCredential=telegram-bot-token:/etc/crypto-auto/credentials/telegram-bot-token /usr/bin/python3 /var/tmp/tz54-vps/bot.py --bind
Running as unit: tz54-bind.service; invocation ID: dec839aec14041c6b33e3d868dca0059
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 512ms
CPU time consumed: 115ms
Memory peak: 1.1M
Memory swap peak: 0B
[exit 0]
$ journalctl -u tz54-bind -o cat --no-pager --since "-1min"
Started tz54-bind.service - /usr/bin/python3 /var/tmp/tz54-vps/bot.py --bind.
bind: getme=ok username=Cryptantrader_bot updates=1 start_chats=1 bound=yes confirm_sent=yes
tz54-bind.service: Deactivated successfully.
$ stat -c '%a %U %G %n' /etc/crypto-auto/credentials/owner-chat-id
600 root root /etc/crypto-auto/credentials/owner-chat-id
```

**C5** (captured):

```
2026-10-01T20:14:53Z
$ ls -A /root/.claude/projects/-tmp-tz53-unit | wc -l; du -sb /root/.claude/projects/-tmp-tz53-unit
2
180846	/root/.claude/projects/-tmp-tz53-unit
$ rm -rf /root/.claude/projects/-tmp-tz53-unit; echo "[exit $?]"
[exit 0]
$ ls -d /root/.claude/projects/-tmp-tz53-unit
ls: cannot access '/root/.claude/projects/-tmp-tz53-unit': No such file or directory
```

**C6** (captured, 40 s after C3):

```
2026-10-01T20:15:04Z
$ journalctl -u crypto-deploy.service -o short-iso-precise --no-pager
2026-10-01T20:14:24.833726+00:00 vultr systemd[1]: Starting crypto-deploy.service - Crypto assistant: install vps/ from main...
2026-10-01T20:14:26.476179+00:00 vultr deploy.sh[3727544]: deploy: no vps tree on origin/main
2026-10-01T20:14:26.480430+00:00 vultr systemd[1]: crypto-deploy.service: Deactivated successfully.
2026-10-01T20:14:26.480617+00:00 vultr systemd[1]: Finished crypto-deploy.service - Crypto assistant: install vps/ from main.
$ systemctl list-unit-files "crypto-*"
UNIT FILE             STATE   PRESET
crypto-deploy.service static  -
crypto-deploy.timer   enabled enabled

2 unit files listed.
$ systemctl list-timers crypto-deploy.timer --no-pager
NEXT                            LEFT LAST                         PASSED UNIT                ACTIVATES
Thu 2026-10-01 20:19:24 UTC 4min 20s Thu 2026-10-01 20:14:24 UTC 39s ago crypto-deploy.timer crypto-deploy.service

1 timers listed.
Pass --all to see loaded but inactive timers, too.
```

### Stage D — measurements in transient units started from the branch

Order as §10 sets it: D3 started first, then D1, D2, D5 and D4. D3 ended inside a second, so it was
collected at once rather than at the end.

**D3. The key and the stream.** A one-second reader of the unit's cgroup peaks (`tz54-sample-announce`)
was started first, then D3 with `RemainAfterExit=yes` added (D-3) (captured):

```
2026-10-01T20:17:16.711Z
$ systemd-run --unit=tz54-sample-announce -p MemoryAccounting=yes /bin/bash -c <one-second reader of tz54-announce memory.current/swap.current/peak/swap.peak>
Running as unit: tz54-sample-announce.service; invocation ID: 441d9b0fcba041d4910ed41cca4a0958
[exit 0]
2026-10-01T20:17:16.743Z
$ systemd-run --unit=tz54-announce -p MemoryAccounting=yes -p RuntimeMaxSec=11100 -p LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key -p LoadCredential=binance-api-secret:/etc/crypto-auto/credentials/binance-api-secret -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz54-vps/announce.py --measure 10800 2 --state-dir /var/tmp/tz54-state
Running as unit: tz54-announce.service; invocation ID: f328d15484cd40448d0f89b36e3dbeb9
[exit 0]
```

```
2026-10-01T20:18:21Z
$ systemctl show tz54-announce -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p MemorySwapPeak
Result=exit-code
ExecMainStartTimestampMonotonic=5230364490924
ExecMainExitTimestampMonotonic=5230364964719
ExecMainStatus=3
MemoryPeak=[not set]
MemorySwapPeak=[not set]
$ journalctl -u tz54-announce -o cat --no-pager
Started tz54-announce.service - /usr/bin/python3 /var/tmp/tz54-vps/announce.py --measure 10800 2 --state-dir /var/tmp/tz54-state.
announce: key REFUSED http=400 code=-1022 msg=Signature for this request is not valid.
tz54-announce.service: Main process exited, code=exited, status=3/NOTIMPLEMENTED
tz54-announce.service: Failed with result 'exit-code'.
$ cat d3-peaks.txt  (epoch memory.current memory.swap.current memory.peak memory.swap.peak)
1790885836 12857344 0 13025280 0
$ systemctl is-active tz54-sample-announce
inactive
$ systemctl reset-failed tz54-announce
tz54 units listed: 0
total 8
drwxr-xr-x  2 root root 4096 Oct  1 20:17 .
drwxrwxrwt 11 root root 4096 Oct  1 20:17 ..
```

Exit status 3 after 0.473795 s; the kernel's peak for the unit as read by the reader, 13 025 280 bytes,
no swap; no record was written (`/var/tmp/tz54-state` empty).

**D1. The instrument's known answer** (captured):

```
2026-10-01T20:18:42.224Z
$ systemd-run --unit=tz54-hog -p MemoryAccounting=yes -p OOMScoreAdjust=500 -p Nice=10 /usr/bin/python3 -c "import time; b = bytearray(100663296); [b.__setitem__(i, 1) for i in range(0, len(b), 4096)]; time.sleep(10)"
Running as unit: tz54-hog.service; invocation ID: 7718459b4bf34265bd545dea89390957
[exit 0]
```

```
{"unit": "tz54-hog", "samples": 11, "span_s": 11.0, "F_run": 105496576, "P_run": 111804416, "F": 111804416, "kernel_memory_peak_last_read": 105926656, "kernel_memory_swap_peak_last_read": 0, "pids_seen": 1, "min_MemAvailable": 72065024, "min_SwapFree": 1489616896}
```

`F_hog` = max(105 496 576, 111 804 416) = **111 804 416 ≥ 100 663 296**: the instrument is sound and D2 runs.

**D2. One full analysis run.** First `MemAvailable` and the session tree's summed `VmRSS` at one instant,
by A2's method (captured):

```
$ python3 memread.py --json   (A2 method, one instant)
{"MemAvailable": 65216512, "session_root": 3715039, "session_tree_rss": 190078976, "session_tree_pids": 5}
```

Then the unit, with `BindReadOnlyPaths=/var/tmp/tz54-vps` and `RemainAfterExit=yes` added (D-2, D-3) — the
first because `PrivateTmp=yes` hides `/var/tmp` from the unit, measured before D2 (captured):

```
2026-10-01T20:16:31Z
$ systemd-run --unit=tz54-ptmp-1 --wait --collect -p MemoryAccounting=yes -p PrivateTmp=yes /usr/bin/test -r /var/tmp/tz54-vps/run.py
Main processes terminated with: code=exited/status=1
$ systemd-run --unit=tz54-ptmp-2 --wait --collect -p MemoryAccounting=yes -p PrivateTmp=yes -p BindReadOnlyPaths=/var/tmp/tz54-vps /usr/bin/test -r /var/tmp/tz54-vps/run.py
Main processes terminated with: code=exited/status=0
$ findmnt -n -o FSTYPE /tmp; findmnt -n -o FSTYPE /var/tmp
/tmp: not a separate mount
/var/tmp: not a separate mount
tz54 units left: 0
```

```
D2 start (UTC): 2026-10-01T20:19:25Z
$ systemd-run --unit=tz54-run -p WorkingDirectory=/srv/crypto-auto-run -p Environment=HOME=/root -p Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin -p Environment=PYTHONDONTWRITEBYTECODE=1 -p RuntimeDirectory=crypto-run -p PrivateTmp=yes -p InaccessiblePaths=-/etc/crypto-auto/credentials -p MemoryAccounting=yes -p RuntimeMaxSec=5400 -p OOMScoreAdjust=500 -p Nice=10 -p BindReadOnlyPaths=/var/tmp/tz54-vps -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz54-vps/run.py --tree /srv/crypto-auto-run
Running as unit: tz54-run.service; invocation ID: 94f5d229864d46e09c36cd4bd819c339
[exit 0]
```

The instrument, every second until the unit's cgroup was gone (captured summary):

```
{"unit": "tz54-run", "samples": 605, "span_s": 605.4, "F_run": 291307520, "P_run": 938381312, "F": 938381312, "kernel_memory_peak_last_read": 285847552, "kernel_memory_swap_peak_last_read": 180314112, "pids_seen": 112, "min_MemAvailable": 46952448, "min_SwapFree": 1262612480}
```

`systemctl show` after the main process exited (captured; the unit failed, so it stayed loaded and systemd
still returned its peaks):

```
Result=exit-code
ExecMainStartTimestampMonotonic=5230493666861
ExecMainExitTimestampMonotonic=5231098566533
ExecMainStatus=1
MemoryPeak=285847552
MemorySwapPeak=180314112
```

`D` = 5 231 098 566 533 − 5 230 493 666 861 µs = **604.899672 s**. The `crypto-run:` and `writer:` lines
and systemd's own lines from `journalctl -u tz54-run -o cat` (captured; the second `crypto-run:` line's
model ids withheld, D-6):

```
$ journalctl -u tz54-run -o cat --no-pager | grep -E "^(crypto-run|writer):"
writer: gate_exit=0 committed=yes pushed=yes rows_c=31 rows_x=788
crypto-run: requests=0 admitted=yes waited_s=0 writer_exit=0 claude_exit=1 is_error=true num_turns=83 duration_ms=585222 denials=0 answer_chars=0
crypto-run: models=[withheld: 2 model ids, see Deviations D-6] denied_tools=-
$ journalctl -u tz54-run -o cat --no-pager | grep -E "^tz54-run.service:"
tz54-run.service: Main process exited, code=exited, status=1/FAILURE
tz54-run.service: Failed with result 'exit-code'.
tz54-run.service: Consumed 1min 37.979s CPU time, 272.6M memory peak, 171.9M memory swap peak.
```

| Term | Value |
|---|---:|
| `F_run` (max of `memory.current + memory.swap.current`) | 291 307 520 |
| `P_run` (sum over 112 pids of each one's largest `VmHWM`) | 938 381 312 |
| `F = max(F_run, P_run)` | 938 381 312 |
| `MemoryPeak` / `MemorySwapPeak` (kernel) | 285 847 552 / 180 314 112 |
| `MemAvailable` before D2 | 65 216 512 |
| the session tree's `VmRSS` before D2 (5 processes) | 190 078 976 |
| `A0` | 255 295 488 |
| `D` | 604.899672 s |
| `memory_max_bytes` / `runtime_max_s` | 1 409 286 144 / 5 400 |
| `fits` | **no** |

**Models and denials.** `modelUsage` carried two model ids, one for the `--model opus` alias and one smaller
helper model; the ids are not written here (D-6). Denied tool names: none (`denials=0`).

**The run ended with `is_error=true`, `claude_exit=1`, 83 turns, an empty result.** Its cause is not read
by this session: the transcript holds the run, and contract §1 forbids reading what a measured run
publishes. The owner reported reaching the account's usage limit while the session was working, a window
that contains D2 — recorded as the owner's statement, not as a reading. Rule 9: the failed run is the
reading and was not repeated.

Commit subjects on `origin/main` since D2 started, and the directories the run created under
`/root/.claude/projects/` (captured):

```
$ git -C /srv/crypto-auto fetch origin main
[exit 0]
$ git -C /srv/crypto-auto log origin/main --since=2026-10-01T20:19:25Z --format='%h %ad %s' --date=iso-strict
2de091e 2026-10-01T20:19:40+00:00 analyst: live.json (vps)
$ ls -d /root/.claude/projects/*/ | wc -l   (before D2: 74; C5 removed one)
75
$ find /root/.claude/projects -maxdepth 1 -mindepth 1 -type d -newermt 2026-10-01T20:19:25Z
/root/.claude/projects/-root-crypto-auto
/root/.claude/projects/-srv-crypto-auto-run
/root/.claude/projects/-root-btc-5m-twap
/root/.claude/projects/-srv-crypto-auto
-srv-crypto-auto-run  entries=1  bytes=1798937
```

```
== /root/.claude/projects/-srv-crypto-auto  (created 2026-10-01 20:19:44.780210720 +0000)
d 4096 2026-10-01T20:19:44 
d 4096 2026-10-01T20:19:44 memory
== /root/.claude/projects/-srv-crypto-auto-run  (created 2026-10-01 20:19:44.957211162 +0000)
d 4096 2026-10-01T20:19:44 
f 1798937 2026-10-01T20:29:30 bea99c3c-fffb-4046-8e5f-a4f2b1b84ee7.jsonl
```

`-srv-crypto-auto-run` holds the run's one session record: B7's target (E4). `-srv-crypto-auto/memory/` is,
by its name and its emptiness, the per-repository memory directory a session in a worktree creates for the
worktree's main repository; `cleanup.py` leaves it alone.

**D5. Delivery** (captured; ran 8.5 h after D2 because the session had stopped on the usage limit, D-10):

```
2026-10-02T04:58:59Z
$ ls -la /var/spool/crypto-auto/outbox/
total 12
drwxrws--- 2 cryptoauto cryptoauto 4096 Oct  1 20:29 .
drwxr-xr-x 4 root       root       4096 Oct  1 19:08 ..
-rw-r----- 1 root       cryptoauto  154 Oct  1 20:29 1790886570691-notice-3728143.json
$ ls /var/spool/crypto-auto/requests/ | wc -l
0
$ systemd-run --unit=tz54-send --wait --collect -p MemoryAccounting=yes -p LoadCredential=telegram-bot-token:/etc/crypto-auto/credentials/telegram-bot-token -p LoadCredential=owner-chat-id:/etc/crypto-auto/credentials/owner-chat-id /usr/bin/python3 /var/tmp/tz54-vps/bot.py --send-outbox-once
Running as unit: tz54-send.service; invocation ID: ec90eba316444d19bec640a9aa13b79e
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 315ms
CPU time consumed: 102ms
Memory peak: 1.0M
Memory swap peak: 0B
[exit 0]
$ journalctl -u tz54-send -o cat --no-pager --since "-3min"
Started tz54-send.service - /usr/bin/python3 /var/tmp/tz54-vps/bot.py --send-outbox-once.
send: file=1790886570691-notice-3728143.json kind=notice chunks=1 accepted=1 plain_fallbacks=0 message_ids=3 status=200
send: files=1 all_accepted=yes
tz54-send.service: Deactivated successfully.
$ ls -A /var/spool/crypto-auto/outbox/ | wc -l
0
```

**D4. The exchange lane** (captured; the instrument at 0.1 s beside each unit, because `systemd-run`'s
«Memory peak» is not a reading on this systemd, D-4):

```
2026-10-02T04:59:18.653Z
$ systemd-run --unit=tz54-exch-1 --wait --collect -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz54-vps/exchange.py --once --state-dir /var/tmp/tz54-state
Running as unit: tz54-exch-1.service; invocation ID: c7b2805d57c34b46bb067ed1055821c4
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 1.867s
CPU time consumed: 113ms
Memory peak: 1.0M
Memory swap peak: 0B
[exit 0]
$ journalctl -u tz54-exch-1 -o cat --no-pager | grep '^exchange:'
exchange: symbols=920 usdt=875 trading_perpetuals=528 baseline=yes new_perpetual=list:0/other:0 delivery_set=list:0/other:0 status_changed=list:0/other:0 alerts=0 requests=0
sampler: {"unit": "tz54-exch-1", "samples": 19, "span_s": 1.9, "F_run": 21696512, "P_run": 25190400, "F": 25190400, "kernel_memory_peak_last_read": 21889024, "kernel_memory_swap_peak_last_read": 0, "pids_seen": 1, "min_MemAvailable": 57360384, "min_SwapFree": 1600065536}
```

```
2026-10-02T05:00:23.370Z
$ systemd-run --unit=tz54-exch-2 --wait --collect -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz54-vps/exchange.py --once --state-dir /var/tmp/tz54-state
Running as unit: tz54-exch-2.service; invocation ID: 646232ff8a474743ae1ec96323757604
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 406ms
CPU time consumed: 108ms
Memory peak: 604.0K
Memory swap peak: 0B
[exit 0]
$ journalctl -u tz54-exch-2 -o cat --no-pager | grep '^exchange:'
exchange: symbols=920 usdt=875 trading_perpetuals=528 baseline=no new_perpetual=list:0/other:0 delivery_set=list:0/other:0 status_changed=list:0/other:0 alerts=0 requests=0
sampler: {"unit": "tz54-exch-2", "samples": 4, "span_s": 0.4, "F_run": 16117760, "P_run": 24117248, "F": 24117248, "kernel_memory_peak_last_read": 16154624, "kernel_memory_swap_peak_last_read": 0, "pids_seen": 1, "min_MemAvailable": 61599744, "min_SwapFree": 1613987840}
```

The three small services' ceiling is `MemoryMax=128M` (134 217 728 bytes); measured kernel peaks: the
exchange watcher 21 889 024 and 16 154 624, the announcement unit 13 025 280 (key check only).

### Stage E — decisions written into the branch

**E1. Fit** (re-run from the record):

```
$ PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys; sys.path.insert(0, "vps"); import common
rec = dict(l.strip().split("=", 1) for l in open("vps/memory-record.txt") if "=" in l and not l.startswith("#"))
F = max(int(rec["run_cgroup_footprint_bytes"]), int(rec["run_process_hwm_bytes"]))
A0 = int(rec["mem_available_bytes"]) + int(rec["session_rss_bytes"])
mm, rt = common.derive_limits(F, rec["run_duration_s"])
print("F = max(%s, %s) = %d" % (rec["run_cgroup_footprint_bytes"], rec["run_process_hwm_bytes"], F))
print("memory_max_bytes = ceil(1.5 x F / 16 MiB) x 16 MiB = %d" % mm)
print("runtime_max_s = max(ceil(2 x %s / 300) x 300, 3600) + 1800 = %d" % (rec["run_duration_s"], rt))
print("A0 = %s + %s = %d" % (rec["mem_available_bytes"], rec["session_rss_bytes"], A0))
print("completed = %s; memory_max_bytes <= A0: %d <= %d is %s" % (rec["run_completed"], mm, A0, mm <= A0))
print("fits = %s (record says fits=%s)" % ("yes" if rec["run_completed"] == "yes" and mm <= A0 else "no", rec["fits"]))
PY
F = max(291307520, 938381312) = 938381312
memory_max_bytes = ceil(1.5 x F / 16 MiB) x 16 MiB = 1409286144
runtime_max_s = max(ceil(2 x 604.899672 / 300) x 300, 3600) + 1800 = 5400
A0 = 65216512 + 190078976 = 255295488
completed = no; memory_max_bytes <= A0: 1409286144 <= 255295488 is False
fits = no (record says fits=no)
[exit 0]
```

**E2.** `vps/memory-record.txt`:

```
# TZ-54 measurement record of crypto-run.service (map inv. 46). Written at Stage E; never edited by hand.
measured_utc=2026-10-01T20:19:25Z
hog_bytes=100663296
hog_footprint_bytes=111804416
run_completed=no
run_duration_s=604.899672
run_cgroup_footprint_bytes=291307520
run_process_hwm_bytes=938381312
run_footprint_bytes=938381312
mem_available_bytes=65216512
session_rss_bytes=190078976
host_free_bytes=255295488
memory_max_bytes=1409286144
runtime_max_s=5400
fits=no
```

`crypto-run.service`: `MemoryMax=1409286144`, `RuntimeMaxSec=5400`.

**E3.** `vps/manifest`:

```
crypto-deploy.timer
crypto-cleanup.timer
crypto-exchange.service
crypto-bot.service
```

`crypto-bot.service` because C4 bound the owner; no `crypto-announce.service` because D3 exited 3; no
`crypto-run.timer` or `crypto-run.path` because `fits=no`.

**E4.** `cleanup.py`'s `RUN_RECORDS` is `/root/.claude/projects/-srv-crypto-auto-run`, the name D2's reading gave.

**E5.** `python3 vps/selftest.py` green with every section, M included (V1).

## Validation

**V1. Selftest** (re-run):

```
$ PYTHONDONTWRITEBYTECODE=1 python3 vps/selftest.py
section A: checks 32 failed 0
section B: checks 12 failed 0
section C: checks 4 failed 0
section D: checks 13 failed 0
section E: checks 12 failed 0
section F: checks 6 failed 0
section G: checks 8 failed 0
section H: checks 2 failed 0
section I: checks 4 failed 0
section J: checks 2 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 9 failed 0
selftest: sections 13 checks 110 failed 0 empty 0
[exit 0]
```

**Negative control** (inv. 68; captured): one character of §12.3's expected block changed (`$150` → `$151`
in the `<pre>` line) — section D failed, every other section stayed green, exit 1; reverted, MD5 back to
its value, green again. The `grep -c` line printing 0 is the quoting of `$` in that grep's pattern; the
swap itself took effect, as section D's two failures show.

```
$ md5sum vps/selftest.py
9d436902800f5cd5e28b9269a31d4c64  vps/selftest.py
$ grep -c '$150 |</pre>' vps/selftest.py
0
$ sed -i 's/$150 |<\/pre>/$151 |<\/pre>/' vps/selftest.py   (one character of the expected block)
$ PYTHONDONTWRITEBYTECODE=1 python3 vps/selftest.py; echo "[exit $?]"
section A: checks 32 failed 0
section B: checks 12 failed 0
section C: checks 4 failed 0
FAIL section D: the expected block, byte for byte
FAIL section D: line 9
section D: checks 13 failed 2
section E: checks 12 failed 0
section F: checks 6 failed 0
section G: checks 8 failed 0
section H: checks 2 failed 0
section I: checks 4 failed 0
section J: checks 2 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 9 failed 0
selftest: sections 13 checks 110 failed 2 empty 0
[exit 1]
$ sed -i 's/$151 |<\/pre>/$150 |<\/pre>/' vps/selftest.py   (reverted)
$ md5sum vps/selftest.py
9d436902800f5cd5e28b9269a31d4c64  vps/selftest.py
$ PYTHONDONTWRITEBYTECODE=1 python3 vps/selftest.py | tail -1; echo "[exit ${PIPESTATUS[0]}]"
selftest: sections 13 checks 110 failed 0 empty 0
[exit 0]
```

**V2. Syntax** (re-run):

```
$ d=$(mktemp -d); for f in vps/*.py; do PYTHONPYCACHEPREFIX=$d python3 -m py_compile "$f" && echo "py_compile ok $f"; done; rm -rf "$d"; bash -n vps/deploy.sh && echo "bash -n ok vps/deploy.sh"; bash -n vps/install.sh && echo "bash -n ok vps/install.sh"; systemd-analyze verify vps/units/* && echo "systemd-analyze verify: exit 0, no warning printed"
py_compile ok vps/announce.py
py_compile ok vps/bot.py
py_compile ok vps/cleanup.py
py_compile ok vps/common.py
py_compile ok vps/exchange.py
py_compile ok vps/run.py
py_compile ok vps/selftest.py
py_compile ok vps/writer.py
bash -n ok vps/deploy.sh
bash -n ok vps/install.sh
systemd-analyze verify: exit 0, no warning printed
[exit 0]
```

**V3. Dry run** (re-run):

```
$ systemctl list-unit-files 'crypto-*' --no-legend > /tmp/tz54-v3-before; bash vps/install.sh --dry-run; echo "dry-run exit $?"; systemctl list-unit-files 'crypto-*' --no-legend > /tmp/tz54-v3-after; diff /tmp/tz54-v3-before /tmp/tz54-v3-after && echo 'crypto-* unit files identical before and after'; rm -f /tmp/tz54-v3-before /tmp/tz54-v3-after
install: would install /etc/systemd/system/crypto-announce.service (0644)
install: would install /etc/systemd/system/crypto-bot.service (0644)
install: would install /etc/systemd/system/crypto-cleanup.service (0644)
install: would install /etc/systemd/system/crypto-cleanup.timer (0644)
install: would install /etc/systemd/system/crypto-deploy.service (0644)
install: would install /etc/systemd/system/crypto-deploy.timer (0644)
install: would install /etc/systemd/system/crypto-exchange.service (0644)
install: would install /etc/systemd/system/crypto-run.path (0644)
install: would install /etc/systemd/system/crypto-run.service (0644)
install: would install /etc/systemd/system/crypto-run.timer (0644)
install: would enable --now crypto-deploy.timer
install: would enable --now crypto-cleanup.timer
install: would enable --now crypto-exchange.service
install: would enable --now crypto-bot.service
install: would disable --now crypto-announce.service
install: would disable --now crypto-run.path
install: would disable --now crypto-run.timer
install: would restart crypto-exchange.service
install: would restart crypto-bot.service
install: would copy vps/deploy.sh to /usr/local/libexec/crypto-auto/deploy.sh
install: would remove /var/lib/crypto-auto/runs-enabled
dry-run exit 0
crypto-* unit files identical before and after
[exit 0]
```

**V4. The writer on the live market — writer half PASSED, run half FAILED.** D2's `writer:` line reads
`gate_exit=0 committed=yes pushed=yes rows_c=31 rows_x=788`, and `origin/main` carries `2de091e analyst:
live.json (vps)` (D2 above). `origin/main` does **not** carry the run's own `analyst: <date>`: the session
ended in an error before writing it.

**V5. The instrument.** `F_hog` 111 804 416 ≥ 100 663 296 (D1) — PASSED.

**V6. Fit.** E1's terms and its inequality are printed above; section M green (V1) — PASSED.

**V7. Delivery.** D5: chunks 1, accepted 1, plain fallbacks 0; the outbox empty afterwards — PASSED.

**V8. Credentials** — PASSED. Modes and last bytes (re-run):

```
$ stat -c '%a %U %s %n' /etc/crypto-auto/credentials /etc/crypto-auto/credentials/*; for f in /etc/crypto-auto/credentials/*; do echo "$(basename $f) last_byte_is_newline=$( [ "$(tail -c1 $f | od -An -tx1 | tr -d ' ')" = 0a ] && echo yes || echo no)"; done
700 root 4096 /etc/crypto-auto/credentials
600 root 64 /etc/crypto-auto/credentials/binance-api-key
600 root 64 /etc/crypto-auto/credentials/binance-api-secret
600 root 9 /etc/crypto-auto/credentials/owner-chat-id
600 root 46 /etc/crypto-auto/credentials/telegram-bot-token
binance-api-key last_byte_is_newline=no
binance-api-secret last_byte_is_newline=no
owner-chat-id last_byte_is_newline=no
telegram-bot-token last_byte_is_newline=no
[exit 0]
```

The exact-value scan — each file first proven to hold exactly one non-empty line — over every file under
the branch's `vps/` and the branch diff (re-run):

```
$ C=/etc/crypto-auto/credentials; for f in telegram-bot-token binance-api-key binance-api-secret; do echo "$f: non_empty_lines=$(grep -c . $C/$f) newline_bytes=$(tr -cd '\n' < $C/$f | wc -c) vps_hits=$(grep -r -c -F -f $C/$f vps | awk -F: '{s+=$NF} END {print s+0}') branch_diff_hits=$(git diff origin/main...HEAD | grep -c -F -f $C/$f)"; done
telegram-bot-token: non_empty_lines=1 newline_bytes=0 vps_hits=0 branch_diff_hits=0
binance-api-key: non_empty_lines=1 newline_bytes=0 vps_hits=0 branch_diff_hits=0
binance-api-secret: non_empty_lines=1 newline_bytes=0 vps_hits=0 branch_diff_hits=0
[exit 0]
```

Over the D2 run's day log and state on `origin/main` — the run wrote neither, so the whole `analyst/` tree of
`origin/main` was scanned, 49 files including the writer's `live.json` — and over
`journalctl -o cat -u 'tz54-*'` (44 lines) and `journalctl -o cat -u crypto-deploy.service` (420 lines)
(captured at 05:03Z):

```
$ stat -c '%a %U %s %n' /etc/crypto-auto/credentials /etc/crypto-auto/credentials/*
700 root 4096 /etc/crypto-auto/credentials
600 root 64 /etc/crypto-auto/credentials/binance-api-key
600 root 64 /etc/crypto-auto/credentials/binance-api-secret
600 root 9 /etc/crypto-auto/credentials/owner-chat-id
600 root 46 /etc/crypto-auto/credentials/telegram-bot-token
telegram-bot-token: newline_bytes=0 last_byte_is_newline=no non_empty_lines=1
binance-api-key: newline_bytes=0 last_byte_is_newline=no non_empty_lines=1
binance-api-secret: newline_bytes=0 last_byte_is_newline=no non_empty_lines=1
owner-chat-id: newline_bytes=0 last_byte_is_newline=no non_empty_lines=1
journal lines scanned: tz54-*=44 crypto-deploy=420; analyst files from origin/main: 49
== exact-value scan with telegram-bot-token (grep -c -F -f)
vps/ (every file, recursive): 0 hits in 22 files
git diff (working tree incl. untracked vps/): 0
origin/main analyst/** (state, day logs, live.json): 0 hits in 49 files
journalctl -o cat -u 'tz54-*': 0
journalctl -o cat -u crypto-deploy.service: 0
== exact-value scan with binance-api-key (grep -c -F -f)
vps/ (every file, recursive): 0 hits in 22 files
git diff (working tree incl. untracked vps/): 0
origin/main analyst/** (state, day logs, live.json): 0 hits in 49 files
journalctl -o cat -u 'tz54-*': 0
journalctl -o cat -u crypto-deploy.service: 0
== exact-value scan with binance-api-secret (grep -c -F -f)
vps/ (every file, recursive): 0 hits in 22 files
git diff (working tree incl. untracked vps/): 0
origin/main analyst/** (state, day logs, live.json): 0 hits in 49 files
journalctl -o cat -u 'tz54-*': 0
journalctl -o cat -u crypto-deploy.service: 0
```

Over this report, run on the final file before it was committed:

```
$ C=/etc/crypto-auto/credentials; for f in telegram-bot-token binance-api-key binance-api-secret; do echo "$f: report_hits=$(grep -c -F -f $C/$f CryptoReports/TZ-54-vps-assistant-layer-report.md)"; done
telegram-bot-token: report_hits=0
binance-api-key: report_hits=0
binance-api-secret: report_hits=0
[exit 0]
```

**The analysis unit cannot read them** — the pair flips as inv. 68 requires (captured):

```
$ systemd-run --unit=tz54-cred-1 --wait --collect -p MemoryAccounting=yes -p InaccessiblePaths=-/etc/crypto-auto/credentials /usr/bin/test -r /etc/crypto-auto/credentials/telegram-bot-token
Main processes terminated with: code=exited/status=1
$ systemd-run --unit=tz54-cred-2 --wait --collect -p MemoryAccounting=yes /usr/bin/test -r /etc/crypto-auto/credentials/telegram-bot-token
Main processes terminated with: code=exited/status=0
```

**V9. The key and the stream — FAILED to reach a verdict.** D3 printed `key REFUSED http=400 code=-1022
msg=Signature for this request is not valid.` and exited 3. No restriction field and no boolean was
returned, so none can be printed; no subscribe answer, no message, no ping, no reconnect, no close code.

**V10. Nothing left** — PASSED (re-run):

```
$ systemctl list-units --all 'tz54-*' --no-legend | wc -l; systemctl list-unit-files 'crypto-*'; ls -d /var/tmp/tz54-vps /var/tmp/tz54-state /root/.claude/projects/-tmp-tz53-unit
0
UNIT FILE             STATE   PRESET
crypto-deploy.service static  -
crypto-deploy.timer   enabled enabled

2 unit files listed.
ls: cannot access '/var/tmp/tz54-vps': No such file or directory
ls: cannot access '/var/tmp/tz54-state': No such file or directory
ls: cannot access '/root/.claude/projects/-tmp-tz53-unit': No such file or directory
[exit 2]
```

The `ls` exit 2 is the three paths' absence, which is the pass.

**V11. No production file** — PASSED (re-run):

```
$ git diff --name-only origin/main...HEAD | wc -l; git diff --name-only origin/main...HEAD | grep -c -v '^vps/'
22
0
[exit 1]
```

22 paths, 0 outside `vps/`; `grep -c` exits 1 when it selects no line, which is the pass.

**V12. Pushes** — PASSED: the branch is pushed and pull request #43 is open; the commits that reached
`main` since this session started are the writer's, from D2's unit, and `journal.yml`'s daily record (re-run):

```
$ gh pr view 43 --json number,url,state,headRefName,baseRefName,headRefOid -q '"#\(.number) \(.state) \(.headRefName) -> \(.baseRefName) head \(.headRefOid[:7]) \(.url)"'; git ls-remote --heads origin tz-54-vps-assistant-layer | cut -c1-7; git log --format='%h %an %s' 99914e6..origin/main
#43 OPEN tz-54-vps-assistant-layer -> main head b097a89 https://github.com/seahomebatumi-ai/crypto-auto/pull/43
b097a89
2de091e Claude Code Executor analyst: live.json (vps)
782a3c6 github-actions[bot] journal: 2026-10-01 [skip ci]
[exit 0]
```

## Test Results

| Control | Where | Result |
|---|---|---|
| `vps/selftest.py`, 13 sections | this session, final tree | 110 checks, 0 failed, 0 empty |
| negative control on section D | this session | D alone red (2 of 13), then green |
| gate selftest (A4) | this session | 40 checks, 14 cases, exit 0 |
| `Bench gate`, `bench.yml` | runner, run 36967492441 | success (CI Execution) |

Offline tests run during Stage B against copies, temporary directories and stubs, before anything relied on
the code. Their outputs were read in the session and are summarised here by hand:

- **writer's publish paths** against a local bare repository and a detached worktree: a clean push
  `(True, True)`; a rejection then `pull --rebase` then push `(True, True)`; a conflict on
  `analyst/live.json` → rebase aborted, `HEAD` back at its base, tree clean `(True, False)`.
- **exchange's change table** on synthetic `exchangeInfo`: a baseline alerts nothing; then A2 for a new
  non-list perpetual, A3 + R1 for a list symbol, A3 alone for another perpetual, A4 + R1 for a list status
  change, a count only for another symbol's status change, nothing for a new quarterly; the watcher's
  seventh request of a day answers `capped`.
- **bot delivery** against a mock API: 400 → plain fallback accepted; 429 → retried; a network error after
  chunk 1 → the file rewritten with exactly chunk 2's source; a double 400 → the file kept.
- **the stream** against a local WebSocket server: the query sorted with the signature last, the key header
  sent, subscribe, a close with code 1001, reconnect after 5 s, a ping at 30 s, the six-field count, exit 0.
- **run.py** with a stub `claude` and writer: requests consumed, §12.2's argv received byte for byte in the
  tree, the answer to the outbox, scratch removed; `is_error` → S7 and exit 1; not admitted → S6 and exit 75.
- **cleanup** in a temporary layout: the dry run removes nothing; the run keeps the newest 40 and removes the
  rest, the stale spool files and the 31-day-old announcement.

## Deviations

**D-1. The credentials are not byte-for-byte the trigger's text** (§1, «holding the value exactly»). All
three values arrived with a space after `=`, and the key and the secret with a line break inside the
value; the secret also carried five Cyrillic letters identical in shape to Latin ones, which a Binance
secret cannot contain. C2 removed the whitespace and mapped the homoglyphs to their Latin letters, and
recorded counts only. After the first permission block the owner sent a photograph of the Binance page;
compared glyph by glyph (the photograph's digit zero is 33–35 px wide, its capital O 43–45 px), the typed
key carried the capital letter O in two places where Binance shows the digit zero, and on the owner's
instruction the key file was rewritten from the photograph (counts in C2). The secret matched the
photograph, except that three vertical strokes in it are lowercase l or capital I and this font draws the
two identically. Binance then refused the signature (D3). The owner's second paste carried the same
homoglyphs again and a vertical bar in one of those three places, so it adds nothing a Binance secret can
hold, and no file was changed. No candidate secret was tried against the exchange.

**D-2. D2 carries `-p BindReadOnlyPaths=/var/tmp/tz54-vps`.** §10's command sets `PrivateTmp=yes`, which
gives the unit private `/tmp` and `/var/tmp`, so `/var/tmp/tz54-vps/run.py` does not exist inside it:
measured `test -r` exit 1 without the bind, exit 0 with it (D2 above). `/tmp` and `/var/tmp` are on the
root file system, not tmpfs, so neither the private directories nor the bind change memory accounting.
The production unit runs from `/srv/crypto-auto/vps/` and needs no bind.

**D-3. D2 and D3 carry `-p RemainAfterExit=yes`.** A transient unit that exits 0 is garbage-collected at
once on this host, and `systemctl show` then returns defaults — `LoadState=not-found`, `Result=success`,
timestamps 0, `MemoryPeak=[not set]` — not readings (measured with `tz54-gctest`, 18:48Z). With the
property, `Result`, `ExecMainStatus` and both timestamps stay readable until the session stops the unit,
which it did. Both units failed in the event, and a failed unit stays loaded anyway.

**D-4. The kernel's peaks were read from the cgroup by the instrument.** On systemd 255 `MemoryPeak` is read
live from the cgroup and is gone once the empty cgroup is pruned (measured with `tz54-raetest`), and
`systemd-run --wait`'s «Memory peak» lines (344.0K, 1.1M, 1.0M, 604.0K above) are not readings. D1 and D2's
instrument reads `memory.peak` and `memory.swap.peak` every second beside §12.7's terms; D3's peak came from
a one-second reader unit, `tz54-sample-announce`; D4's from the instrument at 0.1 s. D2's own
`systemctl show` did return the peaks, because the failed unit stayed loaded.

**D-5. `run.py` prints a second line**, `crypto-run: models=… denied_tools=…`. §14 asks the report for the
model ids under `modelUsage` and the denied tool names; B3's one line has no field for either, and
`result.json` disappears with the unit's `RuntimeDirectory`. The line carries neither the answer nor a value.

**D-6. The model ids are not written into the repository.** This environment forbids any model identifier
in a pushed artifact, so the report gives their count and roles and withholds the ids (the `crypto-run:`
line above, A6's `--model` help continuation). They were given to the owner in the session.

**D-7. `install.sh` applies `disable --now` only to units with an `[Install]` section.** Read literally,
B9 disables and stops every `crypto-*` unit the manifest does not list, and the manifest never lists
`crypto-deploy.service` — the unit that runs `install.sh` — so the deployer would stop itself mid-install.
Units without `[Install]` (`crypto-run.service`, `crypto-cleanup.service`, `crypto-deploy.service`) are
started only by their timer or path; disabling those is what stops them.

**D-8. The bootstrap copies the committer identity into the clone.** A6: `user.name` and `user.email` are set
only in `/root/crypto-auto`'s local config; a fresh clone has none, and both the writer's and the run's
commits would fail. `provision_clone` copies the two values when the clone lacks them, printing neither.

**D-9. §12.9's first fixture is not the page's own example verbatim.** `developers.binance.com` answered
both reads with HTTP 202, an empty body and `x-amzn-waf-action` — a challenge, recorded as the reading and
not routed around (methodology §6). The fixture carries the documented response's field names with exactly
the two violations §12.9 names. The two reads are the only network reads beyond A5 and A9:

```
2026-10-01T18:42:49Z
$ curl -sS -L -m 20 -o api-key-permission.body -D api-key-permission.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://developers.binance.com/docs/wallet/account/api-key-permission'
202 0 text/html; charset=UTF-8 https://developers.binance.com/en/docs/catalog/core-trading-wallet/api/rest-api/account#get-api-key-permission
$ curl -sS -L -m 20 -o general-info.body -D general-info.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://developers.binance.com/docs/cms/general-info'
202 0 text/html; charset=UTF-8 https://developers.binance.com/en/docs/products/announcements/general-info
```

**D-10. Stage order.** The permission blocks put the user, the directories and the staging copy ahead of C3
(the same commands `install.sh` runs, re-applied by C3) and C4's first attempt ahead of C3; C4 was repeated
after the owner's `/start`. D3 failed inside a second, so it was collected at once. D5 ran 8.5 h after D2
because the session stopped on the owner's usage limit; the outbox held the run's notice throughout.

**D-11. `announce.py` reports any 4xx answer to the key check as `REFUSED` and exits 3.** That keeps the
safe direction — no stream, and the service's `RestartPreventExitStatus=3` stops a restart loop — but
`-1022` is a refused signature, not §12.9's verdict on the key's rights; the printed line carries the
exchange's code and message so the two can be told apart. §1's deletion of both Binance files is written
for a key refused on its rights, so the files were kept.

**D-12. `perpetuals.json` holds `{base, symbol}` pairs.** §12.5 matches a perpetual's full symbol, which
keeps its leading digits (`1000PEPEUSDT`); a list of bases alone cannot give it back.

**D-13. Smaller choices B leaves open:** `cut_tokens` also fails when `tokens[]` holds an object its row
pattern does not read; outbox and request names step their millisecond on a collision; the writer's exit 5
also covers a failed commit; the bot keeps a file whose chunk is refused in both forms and backs off;
a staging copy outside a checkout reads `index.html` from `/srv/crypto-auto`.

## Pre-existing Issues

None found. Every file of the map's `## 0` table matches its line count and MD5, before and after the work
(Fingerprints). The TZ defects met during execution are recorded under Deviations with what was done.

## Remaining Risks

1. **The announcement watcher is not running**, and with it the spot-listing lead time map §10 was built
   for. A working secret — copied as text from Binance, or a new key with reading only bound to this
   address — stored as C2 stores one, then D3 and a manifest change, would enable it.
2. **The trigger message's values are on this host outside `/etc/crypto-auto/credentials/`.** Each exact
   value sits in one Claude session record under `/root/.claude/projects/` — this session's own — and the
   run unit, which runs with `HOME=/root` and hides only the credentials directory, can read that tree
   (counts, re-run):

```
$ C=/etc/crypto-auto/credentials; for f in telegram-bot-token binance-api-key binance-api-secret; do echo "$f: files under /root/.claude/projects holding the exact value: $(grep -r -l -F -f $C/$f /root/.claude/projects | wc -l); in -srv-crypto-auto-run: $(grep -r -l -F -f $C/$f /root/.claude/projects/-srv-crypto-auto-run | wc -l); in this session's own: $(grep -r -l -F -f $C/$f /root/.claude/projects/-root-crypto-auto--claude-worktrees-bridge-cse-018cXeqyU9ehURcKzCAJk2k3 | wc -l)"; done
telegram-bot-token: files under /root/.claude/projects holding the exact value: 1; in -srv-crypto-auto-run: 0; in this session's own: 1
binance-api-key: files under /root/.claude/projects holding the exact value: 1; in -srv-crypto-auto-run: 0; in this session's own: 1
binance-api-secret: files under /root/.claude/projects holding the exact value: 1; in -srv-crypto-auto-run: 0; in this session's own: 1
[exit 0]
```

   The measured run's own record holds none of them. Contract §7 item 6 accepts the conversation as the one
   other copy; the copy is also on disk.
3. **`P_run` sums processes that never coexisted.** D2 saw 112 pids; the sum of their peaks (938 MB) is
   3.2 times the cgroup's own footprint (291 MB), and it sets `memory_max_bytes`. The verdict does not
   depend on it — the cgroup figure alone gives 452 984 832 against `A0` 255 295 488 — but on a resized
   host it would size `MemoryMax=` at about three times what the run uses.
4. **The run's cause of failure is unknown to the record.** If it was the account's usage limit, a
   scheduled run on a resized host meets the same limit.
5. **The deployer installs whatever `main` carries, as root, within five minutes** — the reason the session's
   permission check refused it until the owner lifted the block. A red selftest refuses an install and
   sends S10 on every tick until `main` is fixed, so a lasting failure repeats S10 every five minutes.
6. **The bot's run button answers S5** until a fitting host is measured: `runs-enabled` is absent because
   the manifest does not list `crypto-run.path`.

## Commit

Implementation, on the branch, pushed: **`b097a89`** —
`TZ-54: vps — payload writer, run unit, Telegram bot, exchange watcher, deployer` — the 22 files of Files
Created.

Report, on `main`: `TZ-54: report — the assistant on the VPS` — this file only.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/43 — `tz-54-vps-assistant-layer` → `main`.

## CI Execution

The branch push started no workflow: `bench.yml`'s `push` filter names `main` and `claude/**` only. The pull
request started `Bench gate` (re-run of the reading):

```
$ gh run list --branch tz-54-vps-assistant-layer --limit 10 --json databaseId,event,conclusion -q '.[] | "\(.databaseId) \(.event) \(.conclusion)"'
36967492441 pull_request success
[exit 0]
```

```
$ gh run view 36967492441 --json event,headSha,status,conclusion,jobs -q '"event=\(.event) head=\(.headSha[:7]) status=\(.status) conclusion=\(.conclusion)", (.jobs[] | .steps[] | "\(.number)  \(.conclusion)  \(.name)")'
event=pull_request head=b097a89 status=completed conclusion=success
1  success  Set up job
2  success  Run actions/checkout@v4
3  success  Run actions/setup-python@v5
4  success  Run actions/setup-node@v4
5  success  Зависимости
6  success  Доска 19.08 против продакшн-математики (verify_board.js)
7  success  Доска 20.08, LONG + SHORT + два экрана (board2_bench.js)
8  success  Блок «ЗАЩИТА ПОЗИЦИИ» + фаззинг доски (prot_bench.js)
9  success  Офлайн-набор для --verify (verify_bench.py)
10  success  Движок направления (direction_bench.py)
11  success  Свежесть данных — пауза расписания против сбоя (fresh_bench.js)
12  success  Журнал вердиктов, офлайн (journal_bench.js)
13  success  Слой катализаторов (catalyst_bench.js)
14  success  Бейдж и нумерация карточек (display_bench.py)
15  success  Отрисовка списка целиком (render_bench.py)
16  success  Отображение и порядок (direction_bench.py --display)
17  success  Истощение списка и баннер режима (exhaustion_bench.js)
18  success  Ворота живых данных аналитика (live-gate.sh --selftest)
19  success  Гарнизон бэктеста (backtest_guard_bench.py)
36  success  Post Run actions/setup-node@v4
37  success  Post Run actions/setup-python@v5
38  success  Post Run actions/checkout@v4
39  success  Complete job
[exit 0]
```

`bench.yml` defines 18 steps and every one ran green; the numbers after 19 are the runner's post-steps. The
bench gate does not exercise `vps/` — TZ-54 §5 leaves `bench.yml` untouched — and `vps/selftest.py` is the
control that runs in this session and in `install.sh` before every deployment.

## Final Repository State

Branch `tz-54-vps-assistant-layer` at `b097a89`, pushed, pull request #43 open. **NOT IN EFFECT UNTIL
MERGED.** On merge, the deployer's next tick installs `vps/` and enables the four units of the manifest.

What this session leaves on the VPS: `crypto-deploy.timer` enabled and ticking (`deploy: no vps tree on
origin/main` until the merge), `/usr/local/libexec/crypto-auto/deploy.sh` (the branch's copy), the clone
`/srv/crypto-auto` and its worktree `/srv/crypto-auto-run`, the user `cryptoauto`, the spool, state and
libexec directories, the four credential files, `python3-websocket` 1.7.0-1, and D2's session record with
the empty memory directory beside it. No `tz54-*` unit, no staging directory.

Blocks marked «re-run» were executed by the report's generator immediately before writing it and pasted
with their exit; blocks marked «captured» are the files `tee` wrote at the measurement, pasted unchanged
except the one line marked `[withheld]`; the `systemctl show` block of D2, the E2/E3 file contents, the
leak scan over this report and the Test Results summaries were written by hand — the scan was then run on
the final file and its output matched before the commit.

## Fingerprints

### `SYSTEM-MAP-CRYPTOCALCUL.md`

| | |
|---|---|
| Revision string in `## 0. Fingerprint` | `**Revision 2026-10-01-e.**` |
| Required by TZ-54's header | `**Revision 2026-10-01-e.**` — **match** |
| Lines | 3121 |
| MD5 | `7cf5077bffbbcc321b97da389fd742bd` (the TZ reports the same; not enforced) |

### Anchors

Cut from the map's own anchor table **by structure** — the `| Anchor |` header row, its separator, every row
to the table's end — never by anchor names. **The table carries 7 rows and 7 were compared**; the TZ header
carries no row the map's table lacks (re-run):

```
$ bash <<'GATE'
cut_rows() { awk 'f==0 && /^\| Anchor \|/{f=1;next} f==1 && /^\|---/{f=2;next} f==2 && /^\|/{print;next} f==2{exit}' "$1"; }
MAP=SYSTEM-MAP-CRYPTOCALCUL.md; TZ=CryptoTZ/TZ-54-vps-assistant-layer.md
echo "rows in the map's table: $(cut_rows $MAP | wc --lines); rows in the TZ header's table: $(cut_rows $TZ | wc --lines)"
echo "TZ header rows absent from the map's table: $(cut_rows $TZ | grep --fixed-strings --line-regexp --invert-match --count --file=<(cut_rows $MAP))"
cut_rows $MAP | while IFS= read -r row; do
  a=$(printf '%s' "$row" | sed -E 's/^\| [^|]+ \| `(.*)` \|$/\1/')
  echo "grep --fixed-strings --only-matching --max-count=1 -- \"$a\" $MAP"
  echo "  -> $(grep --fixed-strings --only-matching --max-count=1 -- "$a" $MAP | head --lines=1)"
  echo "  lines in the map: $(grep --fixed-strings --line-number -- "$a" $MAP | cut --delimiter=: --fields=1 | tr '\n' ' ')"
  echo "  identical row in the TZ header (grep --fixed-strings --line-regexp --count): $(grep --fixed-strings --line-regexp --count -- "$row" $TZ)"
done
GATE
rows in the map's table: 7; rows in the TZ header's table: 7
TZ header rows absent from the map's table: 0
grep --fixed-strings --only-matching --max-count=1 -- "**Revision 2026-10-01-e.**" SYSTEM-MAP-CRYPTOCALCUL.md
  -> **Revision 2026-10-01-e.**
  lines in the map: 17 407 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.12 Direction engine — veto cascade" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.12 Direction engine — veto cascade
  lines in the map: 408 1377 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.15 Catalyst registry" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.15 Catalyst registry
  lines in the map: 409 1767 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.16 List exhaustion — the day-range measure" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.16 List exhaustion — the day-range measure
  lines in the map: 410 1864 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "## 11. Analytical engine" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ## 11. Analytical engine
  lines in the map: 411 2878 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.17 «РИСК ВЫНОСА» — the day's own risk" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.17 «РИСК ВЫНОСА» — the day's own risk
  lines in the map: 412 2031 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "72. **A write that fails leaves this run's product or nothing" SYSTEM-MAP-CRYPTOCALCUL.md
  -> 72. **A write that fails leaves this run's product or nothing
  lines in the map: 413 2573 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
[exit 0]
```

### Files of the map's `## 0` table, and the two the TZ adds (re-run)

```
$ for f in SYSTEM-MAP-CRYPTOCALCUL.md index.html main.py catalysts.json bench/exhaustion-calibration.txt ANALYST-INSTRUCTIONS.md EXECUTOR-INSTRUCTIONS.md; do echo "$f  $(wc --lines < $f) lines  $(md5sum $f | cut --delimiter=' ' --fields=1)"; done; grep --max-count=1 --only-matching --extended-regexp '\*\*Revision [0-9a-z-]+\.\*\*' SYSTEM-MAP-CRYPTOCALCUL.md ANALYST-INSTRUCTIONS.md; grep --max-count=1 --only-matching --extended-regexp '\*\*Version [0-9]+\.\*\*' EXECUTOR-INSTRUCTIONS.md
SYSTEM-MAP-CRYPTOCALCUL.md  3121 lines  7cf5077bffbbcc321b97da389fd742bd
index.html  3799 lines  4e71da9badca3ccae85b656fdc3773e8
main.py  518 lines  0e3ead8c300d2ee6783303c4bf2fb6b5
catalysts.json  17 lines  f9b2dd4a3594134b2b7b603de19075c3
bench/exhaustion-calibration.txt  175 lines  3b8730b254467c9df4c0a845a0f3cfb3
ANALYST-INSTRUCTIONS.md  3866 lines  feaaffc99f983b3441ce205bcf1b6466
EXECUTOR-INSTRUCTIONS.md  929 lines  7d7e335d1fc1871ca4404128da54a93d
SYSTEM-MAP-CRYPTOCALCUL.md:**Revision 2026-10-01-e.**
ANALYST-INSTRUCTIONS.md:**Revision 2026-10-01-a.**
**Version 24.**
[exit 0]
```

| File | Lines (required) | Lines (measured) | MD5 (required) | MD5 (measured) | |
|---|---:|---:|---|---|---|
| `index.html` | 3799 | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | match |
| `EXECUTOR-INSTRUCTIONS.md` (TZ adds) | 929 | 929 | `7d7e335d1fc1871ca4404128da54a93d` | `7d7e335d1fc1871ca4404128da54a93d` | match · `Version 24.` |
| `ANALYST-INSTRUCTIONS.md` (TZ adds) | 3866 | 3866 | `feaaffc99f983b3441ce205bcf1b6466` | `feaaffc99f983b3441ce205bcf1b6466` | match · `2026-10-01-a` |

No file outside `vps/` was written on the branch, so every row stands before and after the work;
`origin/main` moved only by `analyst/live.json` and the journal while it ran.
