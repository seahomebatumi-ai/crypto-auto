# Implementation Report — TZ-55

## Status

**The fit is not decided: no `fits` line was written.** The last D2 ran under `memory_max_bytes`
452 984 832 and `memory_swap_max_bytes` 251 658 240 against `A0` 535 355 392. It stopped on the account's
usage limit (`api_error_status=429`) after 1 088 s, its kernel peak 283 058 176 bytes resident + 39 358 464
swap, inside both limits. The attempt before it ended the same way. By §10 a second failure for another
reason leaves the decision scope BLOCKED, and by map §10 such a run «measures nothing about memory and
decides nothing about size». `crypto-run.timer` and `crypto-run.path` stay out of `vps/manifest`.

**The announcement stream is not enabled.** The new key passed the rights check (`ACCEPTED`: reading only,
bound to the address). The stream's first answer carried `subType: REGISTER`, which TZ-54's `announce.py`
does not accept, so D3 exited 4. `crypto-announce.service` stays out of the manifest (E3).

**PARTIAL — one scope blocked: the decision.** Everything else is complete:
- the deployer: signed deploys, verified against GitHub's key;
- the bot: `.dead` files;
- the run lane as its own user: the C6 probe green on every item;
- the Binance key and the stream, measured;
- Stage E, V1–V13, and the branch, pull request #44 and its bench gate.

The decision scope met three obstacles in order:
1. **The TZ's admission gate.** The first D2 was never admitted: B2.2 compares `MemAvailable` with
   `memory.max`, and §12.4's `A0` counts the measuring session's own resident memory as free while that
   session stays alive (Pre-existing Issues 1).
2. **The owner's instruction**, applied to the measurement's staging copy only, to start the run on swap
   (Deviations D-7).
3. **The account's usage limit**, hit by both admitted attempts.

**Previous TZ:** TZ-54, merged at `966b3f2` on 02.10.2026; its report is on `main`.

**Timeline (02.10.2026, UTC).**
- 10:26 start. Stage A 10:27–10:34. Stage B code from 10:40.
- From 10:43 Claude Code's auto mode refused C4, the `run.py` login edit, C5 and one syntax check. Meanwhile
  C2, the keyring half of C3, D3 and D1 ran (10:48–10:53).
- The owner took the session out of auto mode at about 10:59. Then C4 11:00–11:04, the remaining code
  11:05–11:07, C3, C5 and C6 11:07–11:10.
- D2 attempt 1 11:12–11:42 (not admitted). The owner's instruction about 11:40. Attempt 2 11:43 (account
  limit). Attempt 3 16:10–16:29, after the owner reported the limit reset (account limit again).
- D5, Stage E, validation and the push after 21:01, when the owner reported the limit reset a second time.

## Inbound Filing

None. The TZ arrived once, at its canonical path `CryptoTZ/TZ-55-run-lane-own-user.md`, in the Boss's upload
`97376c9`:

```
$ git log --all --format='%h %ad %s' --date=iso-strict -- 'CryptoTZ/TZ-55*'
97376c9 2026-10-02T14:17:57+04:00 Add files via upload
```

## Scope Executed

**Class: branch TZ.** §4 names ten files to modify under `vps/**` (contract §8).

| Item | Result |
|---|---|
| A1: contract §4a steps 1–6, §5 gate | passed: revision `2026-10-01-f`; 7 of 7 anchors; contract `Version 25.`; every file at its MD5 (Fingerprints) |
| A2–A7 | taken; every known answer matched: the marker `2b66e47f…`, `966b3f2` verifying, `b097a89` not, the first-parent split, the greeting naming the repository |
| B1–B8 | written. `vps/manifest` was rewritten at E3 with the same four lines (no diff); `vps/memory-record.txt` was written at E2 |
| C1 | not needed: `gpg` 2.4.4 present (A4) |
| C2 | both values 64 characters of `[A-Za-z0-9]`, nothing stripped, written |
| C3 | `--provision` created the user, the clone and `known_hosts`; a second run created nothing; deploy key copied; GitHub's key imported |
| C4 | the run's login minted: `length=108 matched=yes`; scratch shredded |
| C5 | TZ-54's worktree and both record directories removed |
| C6 | every item as required: uid not 0, `HEADLESS-OK`, dry-run push exit 0, the flip 5 × exit 1 and 2 × exit 0 |
| D3 | key `ACCEPTED`; stream answer `REGISTER`; exit 4 after 1.5 s |
| D1 | `F` 105 697 280 (one hog); `F` 117 477 376 (three in sequence) |
| D2 | three unit starts, no completed run; decision scope **BLOCKED** (D-7) |
| D5 | `files=0`, exit 2: the live bot had delivered every notice (D-8) |
| E1–E5 | record (no `fits` line), the unit's three lines, the manifest unchanged, the cleanup target, selftest green |
| V1–V13 | below; V4 and V8 state their exceptions |

## Files Created

None.

## Files Modified

```
vps/bot.py  vps/cleanup.py  vps/common.py  vps/deploy.sh  vps/install.sh  vps/memory-record.txt
vps/run.py  vps/selftest.py  vps/units/crypto-run.service
```

9 files, 575 insertions, 115 deletions (`397ab81`). `vps/manifest` was rewritten at E3 with its existing
four lines and is unchanged.

## Files Renamed

None.

## Files Deleted

None in the repository. On the VPS, as §4 authorises: the worktree `/srv/crypto-auto-run`,
`/root/.claude/projects/-srv-crypto-auto-run` and `/root/.claude/projects/-srv-crypto-auto` (C5), and the
scratch `/var/tmp/tz55-vps`, `/var/tmp/tz55-state` and `/root/tz55-token` (V11).

## Implementation Summary

### The code (Stage B)

- **`vps/common.py` (B1).**
  - `RUN_HOME`, and `RUN_TREE = RUN_HOME + "/crypto-auto"`.
  - `RESERVE_BYTES` (64 MiB) and `MEMORY_MAX_FLOOR_BYTES` (160 MiB), each with §12.4's derivation in a comment.
  - `S11` as `\uXXXX` escapes, built from §12.1's own row by a script; it equals the TZ's text: `True`.
  - `test_limits()` built on `derive_limits()`, which is unchanged.
- **`vps/run.py` (B2).**
  - Default tree is the run's clone.
  - Step 3 without the git lock (and without `fcntl`).
  - `admissible()`: `MemAvailable` ≥ `memory.max`, and `SwapFree` ≥ `memory.swap.max` where that is a number above 0.
  - The login is read by `common.load_credential("claude-oauth-token")` into the `claude` child's
    environment alone. `writer_env()` removes `CLAUDE_CODE_OAUTH_TOKEN` from the writer's environment.
  - The second summary line gains `subtype`, `api_error_status`, `terminal_reason` and `stop_reason`.
  - The command list is TZ-54 §12.2's: compared with `HEAD`'s, `True`, 11 arguments.
- **`vps/bot.py` (B3).**
  - A chunk refused as HTML and then as plain text, both HTTP 400, renames its file `<name>.dead`, logged once by name.
  - `deliver_outbox()` is one pass that goes on past a `.dead` file. Any other failure ends the pass, and
    the service backs off as in TZ-54.
- **`vps/deploy.sh` (B4).**
  - §12.9's seven steps in order, and `--check` (steps 2 and 4).
  - One `refused-vps-tree` marker serves S11 and S10, both as JSON escapes that decode to `common`'s strings.
- **`vps/install.sh` (B5).**
  - `provision_user` adds the group and user `cryptorun` (home `/var/lib/cryptorun`, `nologin`, supplementary `cryptoauto`).
  - `provision_run_clone` (https fetch URL, ssh push URL, committer identity copied, `chown -R`), and
    `known_hosts` from root's `github.com` lines.
  - `provision_worktree` is gone; new mode `--provision`.
- **`vps/cleanup.py` (B6/E4).** `RUN_RECORDS` is the run user's record directory.
- **`vps/selftest.py` (B7).** Section J gains §12.4's four answers; M takes §12.7's rule; N and O are new.
- **`vps/units/crypto-run.service` (B8).** Generated from §12.5's block in the TZ itself: `<A7>` is A7's
  `PATH`, and the three `<E2>` lines are set at E2.

Rule 6, Russian text as escapes:

```
$ for f in vps/*.py vps/*.sh; do n=$(grep -c -P '[\x{0400}-\x{04FF}]' "$f"); [ "$n" != 0 ] && echo "RAW CYRILLIC in $f: $n"; done; echo "raw-Cyrillic scan done"
raw-Cyrillic scan done
```

### Stage A — readings, no writes

**A1.** Contract §4a steps 1–6 and the §5 gate (Fingerprints). `git fetch --all --prune`, not shallow,
TZ-54 merged at `966b3f2`, the tree clean on a branch cut from `origin/main` = `97376c9`.

**A2. What holds the memory**, one instant (captured):

```
2026-10-02T10:32:16Z
MemTotal:        1002127360 bytes
MemAvailable:     113217536 bytes
SwapTotal:       3250581504 bytes
SwapFree:        2158039040 bytes

Top 25 by VmRSS
| pid | ppid | comm | exe basename | elapsed s | VmRSS B | VmSwap B | cgroup |
|---:|---:|---|---|---:|---:|---:|---|
| 3715039 | 2948853 | claude.exe | claude.exe | 57947 | 263602176 | 33587200 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3169067 | 2948864 | claude.exe | claude.exe | 426603 | 92241920 | 135737344 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3148227 | 2948864 | claude.exe | claude.exe | 442049 | 88145920 | 132644864 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 2948864 | 2948852 | claude | claude.exe | 576777 | 55521280 | 47689728 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 2948853 | 2948852 | claude | claude.exe | 576789 | 54661120 | 46686208 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 3646441 | 1 | python3 | python3.12 | 102589 | 46940160 | 115671040 | /system.slice/seahome-radar.service |
| 228592 | 1 | python | python3.12 | 1730351 | 40345600 | 27197440 | /user.slice/user-0.slice/session-7379.scope |
| 1184 | 1 | dockerd | dockerd | 5281651 | 20180992 | 12685312 | /system.slice/docker.service |
| 185511 | 1 | containerd | containerd | 1741510 | 15106048 | 7081984 | /system.slice/containerd.service |
| 3803028 | 3803020 | python3 | python3.12 | 0 | 11767808 | 0 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 2699889 | 1 | python | python3.12 | 751946 | 11362304 | 11653120 | /user.slice/user-0.slice/user@0.service/tmux-spawn-315ec8a4-f008-4219-8440-d24d19ccc793.scope |
| 3646439 | 1 | python3 | python3.12 | 102591 | 11235328 | 141287424 | /system.slice/realestatebot.service |
| 3646344 | 1 | systemd-journal | systemd-journald | 102595 | 10555392 | 921600 | /system.slice/systemd-journald.service |
| 3646402 | 1 | fail2ban-server | python3.12 | 102594 | 9084928 | 16572416 | /system.slice/fail2ban.service |
| 3780149 | 1 | python3 | python3.12 | 16181 | 9060352 | 7995392 | /system.slice/crypto-bot.service |
| 1 | 0 | systemd | systemd | 5281664 | 7020544 | 1675264 | /init.scope |
| 3646369 | 3646368 | nginx | nginx | 102595 | 5005312 | 3330048 | /system.slice/nginx.service |
| 3780143 | 1 | python3 | python3.12 | 16181 | 4833280 | 23977984 | /system.slice/crypto-exchange.service |
| 1621 | 1 | containerd-shim | containerd-shim-runc-v2 | 5281648 | 4599808 | 778240 | /system.slice/containerd.service |
| 1737 | 1646 | amneziawg-go | amneziawg-go | 5281648 | 4026368 | 6615040 | /system.slice/docker-17feded3da6ffc739e311e9a4f5b2364b60f3256588d7b3d8bde23bbfad81cc4.scope |
| 3803020 | 3715039 | bash | bash | 0 | 3878912 | 0 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 2948852 | 1 | tmux: server | tmux | 576789 | 3751936 | 442368 | /user.slice/user-0.slice/session-9749.scope |
| 3803029 | 3803020 | tee | tee | 0 | 2007040 | 0 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 185621 | 1 | bash | bash | 1741509 | 1957888 | 413696 | /system.slice/cake-autorate.service |
| 833 | 1 | systemd-logind | systemd-logind | 5281652 | 1806336 | 2879488 | /system.slice/systemd-logind.service |

Processes whose /proc/<pid>/exe resolves to /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe: 5
| pid | ppid | elapsed s | cwd | VmRSS B | VmSwap B | cgroup |
|---:|---:|---:|---|---:|---:|---|
| 2948853 | 2948852 | 576789 | /root/crypto-auto | 54661120 | 46686208 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
| 2948864 | 2948852 | 576777 | /root/btc-5m-twap | 55521280 | 47689728 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3148227 | 2948864 | 442049 | /root/btc-5m-twap | 88145920 | 132644864 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3169067 | 2948864 | 426603 | /root/btc-5m-twap | 92241920 | 135737344 | /user.slice/user-0.slice/user@0.service/tmux-spawn-c08015c5-000f-45ca-8f5b-0302f9779478.scope |
| 3715039 | 2948853 | 57947 | /root/crypto-auto/.claude/worktrees/bridge-cse_018cXeqyU9ehURcKzCAJk2k3 | 263602176 | 33587200 | /user.slice/user-0.slice/user@0.service/tmux-spawn-5efd6e86-847c-439f-a4c3-0a42e49ae219.scope |
claude summed VmRSS: 554172416 bytes; summed VmSwap: 396345344 bytes

Session tree: root pid 3715039 (nearest claude ancestor of this stage's shell, pid 3803020); 4 processes
| pid | ppid | comm | VmRSS B | VmSwap B |
|---:|---:|---|---:|---:|
| 3715039 | 2948853 | claude.exe | 263602176 | 33587200 |
| 3803020 | 3715039 | bash | 3878912 | 0 |
| 3803028 | 3803020 | python3 | 11767808 | 0 |
| 3803029 | 3803020 | tee | 2007040 | 0 |
Session tree summed VmRSS: 281255936 bytes
```

**A3. What TZ-54's merge put into effect** (captured). Repeated identical lines are counted with `uniq -c`;
the install landed at 06:02:35Z:

```
2026-10-02T10:33:24Z
$ journalctl -u crypto-deploy.service --since 2026-10-02 -o cat | grep -E "^(deploy|install):"
     71 deploy: no vps tree on origin/main
      1 install: enabled crypto-deploy.timer
      1 install: enabled crypto-cleanup.timer
      1 install: enabled crypto-exchange.service
      1 install: enabled crypto-bot.service
      1 install: disabled crypto-announce.service
      1 install: disabled crypto-run.path
      1 install: disabled crypto-run.timer
      1 install: restarted crypto-exchange.service
      1 install: restarted crypto-bot.service
      1 install: runs disabled
      1 install: installed
      1 deploy: installed vps tree 2b66e47f47b0e3fcd3f47805f808045c1b4cf9de
     53 deploy: vps tree 2b66e47f47b0e3fcd3f47805f808045c1b4cf9de already installed
$ systemctl list-unit-files "crypto-*"
UNIT FILE               STATE    PRESET
crypto-run.path         disabled enabled
crypto-announce.service disabled enabled
crypto-bot.service      enabled  enabled
crypto-cleanup.service  static   -
crypto-deploy.service   static   -
crypto-exchange.service enabled  enabled
crypto-run.service      static   -
crypto-cleanup.timer    enabled  enabled
crypto-deploy.timer     enabled  enabled
crypto-run.timer        disabled enabled

10 unit files listed.
$ systemctl is-active crypto-bot.service crypto-exchange.service
active
active
$ cat /var/lib/crypto-auto/deployed-vps-tree; git -C /srv/crypto-auto rev-parse origin/main:vps
2b66e47f47b0e3fcd3f47805f808045c1b4cf9de
2b66e47f47b0e3fcd3f47805f808045c1b4cf9de
$ journalctl -u crypto-exchange.service -o cat | grep "^exchange:" | tail -1
exchange: symbols=920 usdt=875 trading_perpetuals=528 baseline=no new_perpetual=list:0/other:0 delivery_set=list:0/other:0 status_changed=list:0/other:0 alerts=0 requests=0
$ journalctl -u crypto-bot.service -o cat | grep -c "^bot:"
2
$ journalctl -u crypto-deploy.service --since 2026-10-02 -o short-iso | grep -E 'deploy: (installed|no vps)' | sed -n '1p;$p'
2026-10-02T00:02:14+00:00 vultr deploy.sh[3747495]: deploy: no vps tree on origin/main
2026-10-02T06:02:35+00:00 vultr deploy.sh[3779548]: deploy: installed vps tree 2b66e47f47b0e3fcd3f47805f808045c1b4cf9de
```

Known answer met: the marker reads `2b66e47f47b0e3fcd3f47805f808045c1b4cf9de`, equal to `origin/main:vps`.

**A4. Tools** and **A7. `PATH`** (captured):

```
$ journalctl -u crypto-deploy.service --since 2026-10-02 -o short-iso | grep -E "(deploy|install): (installed|enabled|disabled|restarted|runs)" 
2026-10-02T00:02:14+00:00 vultr deploy.sh[3747495]: deploy: no vps tree on origin/main
2026-10-02T06:02:35+00:00 vultr deploy.sh[3779548]: deploy: installed vps tree 2b66e47f47b0e3fcd3f47805f808045c1b4cf9de
2026-10-02T10:33:35Z
$ command -v gpg; gpg --version | head -1
/usr/bin/gpg
[exit 0]
gpg (GnuPG) 2.4.4
$ claude --version
2.1.282 (Claude Code)
$ stat -c "%a %U %n" on the binary and each parent up to /usr
755 root /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
755 root /usr/lib/node_modules/@anthropic-ai/claude-code/bin
755 root /usr/lib/node_modules/@anthropic-ai/claude-code
755 root /usr/lib/node_modules/@anthropic-ai
755 root /usr/lib/node_modules
755 root /usr/lib
755 root /usr
$ id cryptorun
id: ‘cryptorun’: no such user
[exit 1]
$ getent group cryptoauto
cryptoauto:x:988:
[exit 0]
$ echo "$PATH"   (A7)
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

**A5. GitHub's signing key** (captured; one request under rule 3):

```
2026-10-02T10:33:45Z
$ curl -sS -L -m 20 -o web-flow.gpg.body -D web-flow.gpg.hdr -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://github.com/web-flow.gpg'
200 2483 text/plain; charset=utf-8 https://github.com/web-flow.gpg
[exit 0]
$ md5sum web-flow.gpg.body; head -1 web-flow.gpg.body; grep -c "" web-flow.gpg.body
1cc8a49f4412c9cf8718ccfb48738353  web-flow.gpg.body
-----BEGIN PGP PUBLIC KEY BLOCK-----
41
2026-10-02T10:34:01Z
$ install -d -m 0700 -o root -g root /var/tmp/tz55-state /var/tmp/tz55-state/gnupg
[exit 0]
$ GNUPGHOME=/var/tmp/tz55-state/gnupg gpg --batch --import web-flow.gpg.body
gpg: keybox '/var/tmp/tz55-state/gnupg/pubring.kbx' created
gpg: /var/tmp/tz55-state/gnupg/trustdb.gpg: trustdb created
gpg: key 4AEE18F83AFDEB23: public key "GitHub (web-flow commit signing) <noreply@github.com>" imported
gpg: key B5690EEEBB952194: public key "GitHub <noreply@github.com>" imported
gpg: Total number processed: 2
gpg:               imported: 2
[exit 0]
$ gpg --list-keys --with-colons | grep -E "^(pub|sub|fpr|uid):"
pub:e:2048:1:4AEE18F83AFDEB23:1502898241:1705435200::-:::sc::::::23::0:
fpr:::::::::5DE3E0509C47EA3CF04A42D34AEE18F83AFDEB23:
uid:e::::1502898241::6686346E4E61A5075892EA649068FCD4A1F3A825::GitHub (web-flow commit signing) <noreply@github.com>::::::::::0:
pub:-:4096:1:B5690EEEBB952194:1705428342:::-:::scSC::::::23::0:
fpr:::::::::968479A1AFF927E37D1A566BB5690EEEBB952194:
uid:-::::1705428342::808C3A1F53E3D885F40E0B5AB639C5EE2BBA0D40::GitHub <noreply@github.com>::::::::::0:
$ git -C /srv/crypto-auto verify-commit 966b3f2; echo exit
gpg: Signature made Fri 02 Oct 2026 05:58:57 AM UTC
gpg:                using RSA key B5690EEEBB952194
gpg: Good signature from "GitHub <noreply@github.com>" [unknown]
gpg: WARNING: This key is not certified with a trusted signature!
gpg:          There is no indication that the signature belongs to the owner.
Primary key fingerprint: 9684 79A1 AFF9 27E3 7D1A  566B B569 0EEE BB95 2194
[exit 0]
$ git -C /srv/crypto-auto verify-commit b097a89; echo exit
[exit 1]
$ git -C /srv/crypto-auto log --first-parent -1 --format=%h origin/main -- vps
966b3f2
$ git -C /srv/crypto-auto log -1 --format=%h origin/main -- vps
b097a89
$ git -C /srv/crypto-auto log --format="%h %G? %GK" -1 966b3f2; same for b097a89 (scratch keyring)
966b3f2 U B5690EEEBB952194
b097a89 N 
$ GNUPGHOME=$(mktemp -d) git -C /srv/crypto-auto log --format="%h %G? %GK" -1 966b3f2   (a reader without the key)
966b3f2 E B5690EEEBB952194
b097a89 N 
$ git -C /srv/crypto-auto rev-parse origin/main; git -C /srv/crypto-auto rev-parse HEAD
97376c9dc49452e91228d077c9d73029665ead96
97376c9dc49452e91228d077c9d73029665ead96
```

Known answers met:
- `verify-commit 966b3f2` exits 0 (signed by `B5690EEEBB952194`); `b097a89` exits 1.
- `--first-parent` gives `966b3f2`, and plain history gives `b097a89`.
- A reader without the key prints `966b3f2 E B5690EEEBB952194` and `b097a89 N`.

The deployer scope is not blocked.

**A6. Root's identity for this repository** (captured):

```
2026-10-02T10:34:20Z
$ ssh -G github.com | grep -i '^identityfile'
Pseudo-terminal will not be allocated because stdin is not a terminal.
identityfile ~/.ssh/crypto-auto
$ ssh -T -v -o BatchMode=yes git@github.com 2>&1 | grep -E 'Server accepts key|Authenticated to|Hi '
debug1: Server accepts key: /root/.ssh/crypto-auto ED25519 SHA256:J9Ig8LfEBkOB3OjcRCmxWQhc7qKCv8o5dTXhaH9QqIM explicit
Authenticated to github.com ([140.82.121.3]:22) using "publickey".
Hi seahomebatumi-ai/crypto-auto! You've successfully authenticated, but GitHub does not provide shell access.
[exit 1]
$ ssh-keygen -F github.com | grep -v '^#' | wc -l
3
$ ssh-keygen -F github.com | grep -v '^#' > github.com.lines; ssh-keygen -lf github.com.lines
256 SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU |1|vMv5NzDAYpJ99+T+wPkCAcYe3zY=|UwlytbS41ut6Zp61fS1fIbP+oYU= (ED25519)
3072 SHA256:uNiVztksCsDhcc0u9e8BujQXVUpKZIDTMczCvj3tD2s |1|CIBStgwvsam/vIdrVUdpCMQ0MxQ=|rpSp9xC5L8xqhcdw0fpePItGBR8= (RSA)
256 SHA256:p2QAMXNIC1TJYWeIOttrVc98/R1BUFWu3/LiyKgUfQM |1|IiW440h2mvPgJ3yruljXBvc6W8M=|6yVEpJlZm5dzZ56+bwcRbW/h+VQ= (ECDSA)
$ ssh-keygen -F github.com | grep '^#'
# Host github.com found: line 3 
# Host github.com found: line 4 
# Host github.com found: line 5 
```

Known answer met: GitHub greets `seahomebatumi-ai/crypto-auto`, so root's accepted key `/root/.ssh/crypto-auto`
is the repository's deploy key. The run scope is not blocked.

**A measurement beside Stage A: a transient unit does not expand `%d`** (captured; Deviations D-4):

```
2026-10-02T10:38:31Z
$ systemd-run --unit=tz55-spec --wait --collect -p MemoryAccounting=yes -p LoadCredential=probe:/etc/hostname -p 'Environment=X=%d/probe' /bin/sh -c 'echo "X=$X"; echo "CREDENTIALS_DIRECTORY=$CREDENTIALS_DIRECTORY"'
Running as unit: tz55-spec.service; invocation ID: 7eba72b1a6b3469fafb308236c739c29
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 14ms
CPU time consumed: 3ms
Memory peak: 436.0K
Memory swap peak: 0B
[exit 0]
X=%d/probe
CREDENTIALS_DIRECTORY=/run/credentials/tz55-spec.service
0
```

### Stage C — provisioning

**C1.** Not run: A4 found `gpg` 2.4.4.

**C2** (captured). One command that printed nothing wrote both files and its counts; the counts are printed here:

```
2026-10-02T10:49:14Z
$ cat c2-counts.txt
binance-api-key length=64 whitespace_stripped=0 alnum64=yes written=yes
binance-api-secret length=64 whitespace_stripped=0 alnum64=yes written=yes
$ stat -c "%a %U %G %s %y %n" /etc/crypto-auto/credentials /etc/crypto-auto/credentials/*
700 root root 4096 2026-10-02 10:49:15.016602021 +0000 /etc/crypto-auto/credentials
600 root root 64 2026-10-02 10:49:15.015602011 +0000 /etc/crypto-auto/credentials/binance-api-key
600 root root 64 2026-10-02 10:49:15.016602021 +0000 /etc/crypto-auto/credentials/binance-api-secret
600 root root 9 2026-10-01 20:14:37.592026038 +0000 /etc/crypto-auto/credentials/owner-chat-id
600 root root 46 2026-10-01 19:06:44.481414443 +0000 /etc/crypto-auto/credentials/telegram-bot-token
binance-api-key newline_bytes=0 last_byte_is_newline=no non_empty_lines=1
binance-api-secret newline_bytes=0 last_byte_is_newline=no non_empty_lines=1
```

**C3.** `install.sh --provision` twice, then the deploy key, then GitHub's key (captured):

```
2026-10-02T11:07:40Z
$ id cryptorun; ls -d /var/lib/cryptorun
id: ‘cryptorun’: no such user
ls: cannot access '/var/lib/cryptorun': No such file or directory
$ systemctl list-unit-files "crypto-*" --no-legend > before
$ bash vps/install.sh --provision; echo exit
install: group cryptorun created
install: user cryptorun created
install: run clone /var/lib/cryptorun/crypto-auto created
install: run clone push URL set
install: run clone user.name set
install: run clone user.email set
install: known_hosts for cryptorun written: 3 github.com lines
install: provision done
[exit 0]
2026-10-02T11:07:42Z
$ bash vps/install.sh --provision; echo exit   (second run)
install: provision done
[exit 0]
$ systemctl list-unit-files "crypto-*" --no-legend | diff before - && echo unit files unchanged
unit files unchanged
$ id cryptorun; getent group cryptorun
uid=995(cryptorun) gid=987(cryptorun) groups=987(cryptorun),988(cryptoauto)
cryptorun:x:987:
$ getent passwd cryptorun
cryptorun:x:995:987::/var/lib/cryptorun:/usr/sbin/nologin
$ stat -c "%a %U %G %n" /var/lib/cryptorun /var/lib/cryptorun/.ssh /var/lib/cryptorun/.ssh/known_hosts /var/lib/cryptorun/crypto-auto /var/lib/cryptorun/crypto-auto/.git
750 cryptorun cryptorun /var/lib/cryptorun
700 cryptorun cryptorun /var/lib/cryptorun/.ssh
644 cryptorun cryptorun /var/lib/cryptorun/.ssh/known_hosts
755 cryptorun cryptorun /var/lib/cryptorun/crypto-auto
755 cryptorun cryptorun /var/lib/cryptorun/crypto-auto/.git
$ find /var/lib/cryptorun/crypto-auto ! -user cryptorun | wc -l
0
$ ssh-keygen -lf /var/lib/cryptorun/.ssh/known_hosts
256 SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU |1|vMv5NzDAYpJ99+T+wPkCAcYe3zY=|UwlytbS41ut6Zp61fS1fIbP+oYU= (ED25519)
3072 SHA256:uNiVztksCsDhcc0u9e8BujQXVUpKZIDTMczCvj3tD2s |1|CIBStgwvsam/vIdrVUdpCMQ0MxQ=|rpSp9xC5L8xqhcdw0fpePItGBR8= (RSA)
256 SHA256:p2QAMXNIC1TJYWeIOttrVc98/R1BUFWu3/LiyKgUfQM |1|IiW440h2mvPgJ3yruljXBvc6W8M=|6yVEpJlZm5dzZ56+bwcRbW/h+VQ= (ECDSA)
$ cmp <(ssh-keygen -F github.com -f /root/.ssh/known_hosts | grep -v "^#") /var/lib/cryptorun/.ssh/known_hosts && echo identical to root lines
identical to root's github.com lines
$ git config: remote.origin.url / pushurl; user.name, user.email set?
https://github.com/seahomebatumi-ai/crypto-auto.git
git@github.com:seahomebatumi-ai/crypto-auto.git
user.name set
user.email set
$ git rev-parse --abbrev-ref HEAD; git rev-parse HEAD origin/main
main
97376c9dc49452e91228d077c9d73029665ead96
97376c9dc49452e91228d077c9d73029665ead96
```

```
2026-10-02T11:07:56Z
$ install -m 0600 -o root -g root /root/.ssh/crypto-auto /etc/crypto-auto/credentials/deploy-key
[exit 0]
$ stat -c "%a %U %G %s %n" /root/.ssh/crypto-auto /etc/crypto-auto/credentials/deploy-key
600 root root 411 /root/.ssh/crypto-auto
600 root root 411 /etc/crypto-auto/credentials/deploy-key
$ cmp /root/.ssh/crypto-auto /etc/crypto-auto/credentials/deploy-key && echo identical
identical
$ ssh-keygen -lf /etc/crypto-auto/credentials/deploy-key
256 SHA256:J9Ig8LfEBkOB3OjcRCmxWQhc7qKCv8o5dTXhaH9QqIM (ED25519)
deploy-key last_byte_is_newline=yes lines=7
```

The keyring import ran at 10:48:13Z (`install -d -m 0700 -o root -g root /etc/crypto-auto/gnupg`, then
`GNUPGHOME=/etc/crypto-auto/gnupg gpg --batch --import` of A5's file, MD5 `1cc8a49f4412c9cf8718ccfb48738353`,
«imported: 2»). Its `tee` target directory did not exist yet, so the keyring is re-read here:

```
$ GNUPGHOME=/etc/crypto-auto/gnupg gpg --list-keys --with-colons | grep -E "^(pub|fpr|uid):"
pub:e:2048:1:4AEE18F83AFDEB23:1502898241:1705435200::-:::sc::::::23::0:
fpr:::::::::5DE3E0509C47EA3CF04A42D34AEE18F83AFDEB23:
uid:e::::1502898241::6686346E4E61A5075892EA649068FCD4A1F3A825::GitHub (web-flow commit signing) <noreply@github.com>::::::::::0:
pub:-:4096:1:B5690EEEBB952194:1705428342:::-:::scSC::::::23::0:
fpr:::::::::968479A1AFF927E37D1A566BB5690EEEBB952194:
uid:-::::1705428342::808C3A1F53E3D885F40E0B5AB639C5EE2BBA0D40::GitHub <noreply@github.com>::::::::::0:
$ stat -c "%a %U %G %n" /etc/crypto-auto/gnupg /etc/crypto-auto/gnupg/pubring.kbx /etc/crypto-auto/gnupg/trustdb.gpg
700 root root /etc/crypto-auto/gnupg
644 root root /etc/crypto-auto/gnupg/pubring.kbx
600 root root /etc/crypto-auto/gnupg/trustdb.gpg
```

**C4.** Ran by §12.8 with one deviation: the tmux window size (D-3).
- Step 1 (captured):

```
2026-10-02T11:00:00Z
$ mkdir -m 0700 /root/tz55-token
[exit 0]
$ tmux new-session -d -x 1000 -y 50 -s tz55-token "script -q -f -c 'claude setup-token' /root/tz55-token/out"
[exit 0]
```

- Step 2: the pattern read one whole URL (`urls_found=1 whole_urls=1`). The screen, printed with every URL and
  long string masked, asked «Paste code here if prompted». The URL alone was posted to the owner.
- Step 3, the code sent (captured; the codes are not reproduced). The owner's first message carried a six-digit
  number, and the tool answered «OAuth error: Invalid code. Please make sure the full code was copied» and
  «Press Enter to retry». One Enter brought back the same URL (compared: `same_as_posted=[True]`). The owner's
  second message carried a code ending in the URL's own `state`:

```
2026-10-02T11:02:14Z
$ tmux has-session -t tz55-token
alive
$ tmux send-keys -t tz55-token -l '<code>'; tmux send-keys -t tz55-token Enter
[exit 0]
[exit 0]
2026-10-02T11:02:48Z
$ tmux send-keys -t tz55-token Enter   (the screen: "Press Enter to retry.")
[exit 0]
2026-10-02T11:04:05Z
$ tmux send-keys -t tz55-token -l '<code>'; tmux send-keys -t tz55-token Enter
[exit 0]
[exit 0]
```

- Steps 4 and 5 (captured):

```
2026-10-02T11:04:21Z
$ python3 c4-token.py /root/tz55-token/out
length=108 matched=yes
[exit 0]
$ stat -c "%a %U %G %s %n" /etc/crypto-auto/credentials/claude-oauth-token
600 root root 108 /etc/crypto-auto/credentials/claude-oauth-token
claude-oauth-token newline_bytes=0 last_byte_is_newline=no non_empty_lines=1 prefix_ok=1
2026-10-02T11:04:32Z
$ tmux kill-session -t tz55-token
can't find session: tz55-token
[exit 1]
$ shred -u /root/tz55-token/out
[exit 0]
$ rmdir /root/tz55-token
[exit 0]
$ ls -d /root/tz55-token; tmux has-session -t tz55-token
ls: cannot access '/root/tz55-token': No such file or directory
can't find session: tz55-token
[exit 1]
$ pgrep -f "claude setup-token" | wc -l
2
```

The tmux session had already ended when the tool exited. No process holds a `setup-token` argument:
`processes with a setup-token argument: 0 []`.

**C5** (captured). The worktree was clean, with no commit absent from `origin/main`:

```
2026-10-02T11:08:18Z
$ git -C /srv/crypto-auto-run status --porcelain | wc -l; git -C /srv/crypto-auto-run log --format=%h origin/main..HEAD | wc -l
0
0
$ git -C /srv/crypto-auto worktree remove --force /srv/crypto-auto-run
[exit 0]
$ rm -rf /root/.claude/projects/-srv-crypto-auto-run /root/.claude/projects/-srv-crypto-auto
[exit 0]
$ git -C /srv/crypto-auto worktree list
/srv/crypto-auto  97376c9 [main]
$ ls -d /srv/crypto-auto-run /root/.claude/projects/-srv-crypto-auto-run /root/.claude/projects/-srv-crypto-auto
ls: cannot access '/srv/crypto-auto-run': No such file or directory
ls: cannot access '/root/.claude/projects/-srv-crypto-auto-run': No such file or directory
ls: cannot access '/root/.claude/projects/-srv-crypto-auto': No such file or directory
```

**C6, the probe** (captured). The staging copy was refreshed from the branch with the probe script beside it.
The unit carried every property of §12.5 except `ExecStart` and the memory limits, plus `RuntimeMaxSec=300`,
`BindReadOnlyPaths=/var/tmp/tz55-vps` and `RemainAfterExit=yes`:

```
2026-10-02T11:09:01Z
$ rm -rf /var/tmp/tz55-vps; cp -r vps /var/tmp/tz55-vps; install -m 0755 probe.sh /var/tmp/tz55-vps/probe.sh; chown -R root:root /var/tmp/tz55-vps; chmod 0755 /var/tmp/tz55-vps
[exit 0]
$ diff -r vps /var/tmp/tz55-vps
Only in /var/tmp/tz55-vps: probe.sh
755 root root /var/tmp/tz55-vps
755 root root /var/tmp/tz55-vps/probe.sh
644 root root /var/tmp/tz55-vps/run.py
bash -n ok probe.sh
2026-10-02T11:09:32Z
$ systemd-run --unit=tz55-probe -p Description=... (all of 12.5 but ExecStart and the memory limits) -p RuntimeMaxSec=300 -p BindReadOnlyPaths=/var/tmp/tz55-vps -p RemainAfterExit=yes /bin/bash /var/tmp/tz55-vps/probe.sh
Running as unit: tz55-probe.service; invocation ID: 8e3a7d6ab16343ada9d0ecde5bba8f6d
[exit 0]
2026-10-02T11:09:49Z
$ journalctl -u tz55-probe -o cat --no-pager
Starting tz55-probe.service - Crypto assistant: one headless analysis run...
Started tz55-probe.service - Crypto assistant: one headless analysis run.
probe: uid_nonzero=true
probe: claude_exit=0 is_error_false=true result_exact=true
probe: push_dry_run_exit=0
probe: test_r telegram-bot-token-file exit=1
probe: test_r binance-api-secret-file exit=1
probe: test_r owner-chat-id-file exit=1
probe: test_r crypto-bot-credential exit=1
probe: test_r root-claude-dir exit=1
probe: test_r own-claude-oauth-token exit=0
probe: test_r own-deploy-key exit=0
$ systemctl show tz55-probe -p Result -p ExecMainStatus -p User -p Group -p SupplementaryGroups -p NoNewPrivileges -p CapabilityBoundingSet -p ProtectSystem -p ProtectHome -p PrivateTmp -p ReadWritePaths -p BindReadOnlyPaths -p RuntimeMaxUSec -p RuntimeDirectory -p OOMScoreAdjust -p Nice -p WorkingDirectory -p LoadCredential -p StartLimitBurst -p StartLimitIntervalUSec -p After -p Wants
RuntimeMaxUSec=5min
Result=success
ExecMainStatus=0
WorkingDirectory=/var/lib/cryptorun/crypto-auto
OOMScoreAdjust=500
Nice=5
CapabilityBoundingSet=
User=cryptorun
Group=cryptorun
LoadCredential=[unprintable]
SupplementaryGroups=cryptoauto
ReadWritePaths=/var/lib/cryptorun /var/spool/crypto-auto
PrivateTmp=yes
ProtectHome=yes
ProtectSystem=strict
NoNewPrivileges=yes
RuntimeDirectory=crypto-run
BindReadOnlyPaths=/var/tmp/tz55-vps:/var/tmp/tz55-vps:rbind
Wants=network-online.target tmp.mount
After=systemd-journald.socket systemd-tmpfiles-setup.service "run-credentials-tz55\\x2dprobe.service.mount" basic.target system.slice network-online.target -.mount tmp.mount sysinit.target
StartLimitIntervalUSec=10min
StartLimitBurst=3
$ systemctl show tz55-probe -p Environment
Environment=HOME=/var/lib/cryptorun PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin PYTHONDONTWRITEBYTECODE=1 DISABLE_AUTOUPDATER=1 "GIT_SSH_COMMAND=ssh -i /run/credentials/tz55-probe.service/deploy-key -o IdentitiesOnly=yes -o UserKnownHostsFile=/var/lib/cryptorun/.ssh/known_hosts"
2026-10-02T11:10:01Z
$ systemctl stop tz55-probe; systemctl reset-failed tz55-probe 2>/dev/null; systemctl list-units --all "tz55-*" --no-legend | wc -l
0
$ ls -d /run/crypto-run
ls: cannot access '/run/crypto-run': No such file or directory
$ find /var/lib/cryptorun -maxdepth 3 -not -path "*/crypto-auto/*" -printf "%y %m %u %P\n" | sort
d 700 cryptorun .claude/sessions
d 700 cryptorun .ssh
d 750 cryptorun 
d 755 cryptorun .claude
d 755 cryptorun .claude/backups
d 755 cryptorun .claude/projects
d 755 cryptorun .claude/projects/-var-lib-cryptorun-crypto-auto
d 755 cryptorun crypto-auto
f 600 cryptorun .claude/backups/.claude.json.backup.1790939372827
f 600 cryptorun .claude.json
f 600 cryptorun .claude/policy-limits.json
f 600 cryptorun .claude/policy-limits.json.stamp.json
f 600 cryptorun .claude/remote-settings.json
f 644 cryptorun .ssh/known_hosts
$ git ls-remote --heads origin tz-55-push-probe | wc -l
0
```

Every item reads as required:
1. uid not 0;
2. `claude -p` with the run's own login: exit 0, `is_error` false, `result` exactly `HEADLESS-OK`;
3. the dry-run push through the credential directory exits 0, and no `tz-55-push-probe` branch exists;
4. the flip: exit 1 on the bot token, the Binance secret, the owner binding, the bot's own credential mount
   and `/root/.claude`, and exit 0 on the run's own login and deploy key.

`CapabilityBoundingSet=` read back empty.

### Stage D — measurements

Order as §10 sets it, with the deviations of D-1:
- D3 started first and was collected at once, because it ended inside two seconds; then D1.
- D2 three times (D-7); then D5.

**D3. The key and the stream** (captured). The one-second reader `tz55-sample-announce` was started first,
and D3 carried `RemainAfterExit=yes` (TZ-54 D-3):

```
2026-10-02T10:50:15Z
$ ls -d /var/tmp/tz55-vps
ls: cannot access '/var/tmp/tz55-vps': No such file or directory
$ cp -r vps /var/tmp/tz55-vps; chown -R root:root /var/tmp/tz55-vps; chmod 0755 /var/tmp/tz55-vps
[exit 0]
$ diff -r vps /var/tmp/tz55-vps && echo identical
identical
$ install -m 0644 sampler.py /var/tmp/tz55-state/sampler.py
[exit 0]
755 root root /var/tmp/tz55-vps
700 root root /var/tmp/tz55-state
644 root root /var/tmp/tz55-state/sampler.py
97376c9dc49452e91228d077c9d73029665ead96
 M vps/bot.py
 M vps/common.py
 M vps/deploy.sh
2026-10-02T10:50:42.816Z
$ systemd-run --unit=tz55-sample-announce -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz55-state/sampler.py tz55-announce /var/tmp/tz55-state/sample-announce.jsonl 1 120
Running as unit: tz55-sample-announce.service; invocation ID: 1536e86cdca64e9e9f3b27f6628d4ac1
[exit 0]
2026-10-02T10:50:42.839Z
$ systemd-run --unit=tz55-announce -p MemoryAccounting=yes -p RuntimeMaxSec=11100 -p LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key -p LoadCredential=binance-api-secret:/etc/crypto-auto/credentials/binance-api-secret -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz55-vps/announce.py --measure 10800 2 --state-dir /var/tmp/tz55-state
Running as unit: tz55-announce.service; invocation ID: 4f26f97f31d64c59a922b3f2fa9568a3
[exit 0]
2026-10-02T10:51:47Z
$ systemctl show tz55-announce -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p MemorySwapPeak
Result=exit-code
ExecMainStartTimestampMonotonic=5282770576082
ExecMainExitTimestampMonotonic=5282772075273
ExecMainStatus=4
MemoryPeak=[not set]
MemorySwapPeak=[not set]
$ journalctl -u tz55-announce -o cat --no-pager
Started tz55-announce.service - /usr/bin/python3 /var/tmp/tz55-vps/announce.py --measure 10800 2 --state-dir /var/tmp/tz55-state.
announce: key ACCEPTED ipRestrict=true enableReading=true enableFutures=false enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableMargin=false
announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
tz55-announce.service: Main process exited, code=exited, status=4/NOPERMISSION
tz55-announce.service: Failed with result 'exit-code'.
$ systemctl is-active tz55-sample-announce; cat /var/tmp/tz55-state/sample-announce.jsonl.summary.json
inactive
{"unit": "tz55-announce", "samples": 2, "span_s": 1.0, "first_t": 1790938242.897, "last_t": 1790938243.897, "F_run": 21544960, "P_peak": 21561344, "F": 21561344, "memory_peak_last_read": 21561344, "memory_swap_peak_last_read": 0, "max_current": 21544960, "max_swap_current": 0, "min_MemAvailable": 145190912, "min_SwapFree": 2086981632}
$ wc -l /var/tmp/tz55-state/sample-announce.jsonl; ls -A /var/tmp/tz55-state
2
gnupg
sample-announce.jsonl
sample-announce.jsonl.summary.json
sampler.py
$ systemctl reset-failed tz55-announce; systemctl list-units --all "tz55-*" --no-legend | wc -l
0
```

Exit 4 after 1.499191 s, with the kernel peak 21 561 344 bytes and no swap. The key's rights were read
before any stream: `ACCEPTED`, so both Binance files stay.

The subscribe answer was `{"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}`.
`announce.py` treats the first `COMMAND` message as the answer and accepts only `subType` `SUBSCRIBE` (TZ-54
§12.10's documented answer), so it closed the stream and exited 4. No message, ping or reconnect followed
(Pre-existing Issues 2).

**D1. The instrument's known answers** (captured):

```
2026-10-02T10:52:10.442Z
$ systemd-run --unit=tz55-sample-hog1 -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz55-state/sampler.py tz55-hog1 /var/tmp/tz55-state/sample-hog1.jsonl
Running as unit: tz55-sample-hog1.service; invocation ID: 1a5607707a8d490691269e6cb0837cea
[exit 0]
$ systemd-run --unit=tz55-hog1 -p MemoryAccounting=yes -p OOMScoreAdjust=500 -p Nice=10 /usr/bin/python3 -c "import time; b = bytearray(100663296); [b.__setitem__(i, 1) for i in range(0, len(b), 4096)]; time.sleep(10)"
Running as unit: tz55-hog1.service; invocation ID: 11302a0c20ee463c99b7daf54c8d0c93
[exit 0]
2026-10-02T10:52:21.550Z
$ cat /var/tmp/tz55-state/sample-hog1.jsonl.summary.json
{"unit": "tz55-hog1", "samples": 11, "span_s": 10.0, "first_t": 1790938330.533, "last_t": 1790938340.535, "F_run": 105275392, "P_peak": 105697280, "F": 105697280, "memory_peak_last_read": 105697280, "memory_swap_peak_last_read": 0, "max_current": 105275392, "max_swap_current": 0, "min_MemAvailable": 129204224, "min_SwapFree": 2033942528}
0
```

```
2026-10-02T10:52:54.851Z
$ systemd-run --unit=tz55-sample-hog3 -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz55-state/sampler.py tz55-hog3 /var/tmp/tz55-state/sample-hog3.jsonl
Running as unit: tz55-sample-hog3.service; invocation ID: 8d00e4876e9a4f8fb3395f1139407f74
[exit 0]
$ systemd-run --unit=tz55-hog3 -p MemoryAccounting=yes -p OOMScoreAdjust=500 -p Nice=10 /bin/sh -c '<three lines>'
    python3 -c "import time; b = bytearray(100663296); [b.__setitem__(i, 1) for i in range(0, len(b), 4096)]; time.sleep(10)"
    python3 -c "import time; b = bytearray(100663296); [b.__setitem__(i, 1) for i in range(0, len(b), 4096)]; time.sleep(10)"
    python3 -c "import time; b = bytearray(100663296); [b.__setitem__(i, 1) for i in range(0, len(b), 4096)]; time.sleep(10)"
Running as unit: tz55-hog3.service; invocation ID: af3d8a07b04a4161ab100f05ea70b903
[exit 0]
2026-10-02T10:53:26.084Z
$ cat /var/tmp/tz55-state/sample-hog3.jsonl.summary.json
{"unit": "tz55-hog3", "samples": 31, "span_s": 30.0, "first_t": 1790938374.926, "last_t": 1790938404.929, "F_run": 107323392, "P_peak": 117477376, "F": 117477376, "memory_peak_last_read": 107753472, "memory_swap_peak_last_read": 9723904, "max_current": 107323392, "max_swap_current": 9723904, "min_MemAvailable": 101691392, "min_SwapFree": 2015899648}
$ per-sample current (MB) and peak (MB)
374.9 16.6 16.7 0.0;375.9 105.3 105.7 0.0;376.9 105.3 105.7 0.0;377.9 105.3 105.7 0.0;378.9 105.3 105.7 0.0;379.9 105.3 105.7 0.0;380.9 105.3 105.7 0.0;381.9 105.3 105.7 0.0;382.9 105.3 105.7 0.0;383.9 105.3 105.7 0.0;384.9 105.3 105.7 0.0;385.9 106.3 106.8 0.0;386.9 106.3 106.8 0.0;387.9 106.3 106.8 0.0;388.9 106.3 106.8 0.0;389.9 106.3 106.8 0.0;390.9 106.3 106.8 0.0;391.9 106.3 106.8 0.0;392.9 106.3 106.8 0.0;393.9 106.3 106.8 0.0;394.9 106.3 106.8 0.0;395.9 107.3 107.8 0.0;396.9 107.3 107.8 0.0;397.9 107.3 107.8 0.0;398.9 107.3 107.8 0.0;399.9 107.0 107.8 0.0;400.9 97.1 107.8 9.2;401.9 96.0 107.8 9.7;402.9 96.0 107.8 9.7;403.9 96.0 107.8 9.7;404.9 96.0 107.8 9.7;
0
```

- One hog: `F` = 105 697 280 ≥ 100 663 296.
- Three in sequence: 100 663 296 ≤ `F` = 117 477 376 < 201 326 592.

The instrument is sound, so D2 runs (V5).

**D2, attempt 1** (`tz55-run`). `A0` and the limits (captured):

```
2026-10-02T11:11:23Z
$ python3 memread.py --json   (A2 method, one instant)
{"ts": "2026-10-02T11:11:23Z", "MemAvailable": 209678336, "SwapFree": 1979699200, "session_root": 3715039, "session_tree_rss": 223211520, "session_tree_pids": 6}
$ grep -E "^(VmRSS|RssAnon|RssFile|RssShmem|VmSwap):" /proc/<session root>/status
VmRSS:	  196140 kB
RssAnon:	  154672 kB
RssFile:	   41468 kB
RssShmem:	       0 kB
VmSwap:	  103208 kB
$ python3 -c "common.test_limits(466161664, 604.899672, A0)"
A0 = 209678336 + 223211520 = 432889856
budget=704643072 memory_max=352321536 memory_swap_max=352321536 runtime_max_s=5400
memory_max >= floor 167772160: True
admission terms now: MemAvailable 209678336 >= memory_max 352321536: False; SwapFree 1979699200 >= memory_swap_max 352321536: True
$ ls -A /var/spool/crypto-auto/outbox /var/spool/crypto-auto/requests | wc -l
/var/spool/crypto-auto/outbox:

/var/spool/crypto-auto/requests:
D2 start (UTC): 2026-10-02T11:12:14Z
$ systemd-run --unit=tz55-sample-run -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz55-state/sampler.py tz55-run /var/tmp/tz55-state/sample-run.jsonl 1 120
Running as unit: tz55-sample-run.service; invocation ID: 146bdc80c8e74df3b2fe37de611a826f
[exit 0]
$ systemd-run --unit=tz55-run <all of 12.5 but ExecStart> -p MemoryMax=352321536 -p MemorySwapMax=352321536 -p RuntimeMaxSec=5400 -p BindReadOnlyPaths=/var/tmp/tz55-vps -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz55-vps/run.py --tree /var/lib/cryptorun/crypto-auto
Running as unit: tz55-run.service; invocation ID: 77225f1d39dc4afb9b4b295802c4a1f3
[exit 0]
```

Collected (captured):

```
2026-10-02T11:42:34Z
$ systemctl show tz55-run -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p MemorySwapPeak
Result=success
ExecMainStartTimestampMonotonic=5284062622075
ExecMainExitTimestampMonotonic=5285862872803
ExecMainStatus=75
MemoryPeak=9203712
MemorySwapPeak=7536640
$ journalctl -u tz55-run -o cat --no-pager
Starting tz55-run.service - Crypto assistant: one headless analysis run...
Started tz55-run.service - Crypto assistant: one headless analysis run.
crypto-run: requests=0 admitted=no waited_s=1800 writer_exit=- claude_exit=- is_error=true num_turns=0 duration_ms=0 denials=0 answer_chars=0
crypto-run: models=[withheld] denied_tools=- subtype=- api_error_status=- terminal_reason=- stop_reason=-
$ cat /var/tmp/tz55-state/sample-run.jsonl.summary.json
{"unit": "tz55-run", "samples": 1801, "span_s": 1800.2, "first_t": 1790939534.937, "last_t": 1790941335.141, "F_run": 15347712, "P_peak": 16740352, "F": 16740352, "memory_peak_last_read": 9203712, "memory_swap_peak_last_read": 7536640, "max_current": 8945664, "max_swap_current": 7536640, "min_MemAvailable": 115003392, "min_SwapFree": 1957392384}
$ ls -A /var/spool/crypto-auto/outbox /var/spool/crypto-auto/requests
/var/spool/crypto-auto/outbox:

/var/spool/crypto-auto/requests:
$ journalctl -u crypto-bot.service --since 11:42 -o short-iso --no-pager | grep -E "bot: (sent|outbox)"
2026-10-02T11:42:15+00:00 vultr python3[3780149]: bot: sent 1790941334995-notice-3807599.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
$ git -C /srv/crypto-auto fetch -q origin main; git -C /srv/crypto-auto log origin/main --since=2026-10-02T11:12:14Z --format="%h %ad %s" --date=iso-strict
$ ls -A /var/lib/cryptorun/.claude/projects/ ; entries per dir
-var-lib-cryptorun-crypto-auto entries=2
```

`D` = 5 285 862 872 803 − 5 284 062 622 075 µs = 1 800.250728 s: the admission wait alone.
- `Result=success`, `ExecMainStatus=75`: not admitted, `waited_s=1800`; no writer, no session.
- The S6 notice reached the owner's chat through the live bot at 11:42:15Z.
- `MemAvailable` moved between 115 and 280 MB during the wait and never reached `memory.max` 352 321 536.

**D2, attempt 2** (`tz55-run2`): `A0` again, the limits again, and the owner's bypass in the staging copy
(captured):

```
2026-10-02T11:43:07Z
$ systemctl stop tz55-run; systemctl list-units --all "tz55-*" --no-legend | wc -l
0
$ python3 bypass.py /var/tmp/tz55-vps/run.py   (the D2 staging copy only)
patched 1 line
[exit 0]
$ diff -u vps/run.py /var/tmp/tz55-vps/run.py
--- vps/run.py	2026-10-02 11:05:30.906407884 +0000
+++ /var/tmp/tz55-vps/run.py	2026-10-02 11:43:07.533224617 +0000
@@ -103,7 +103,7 @@
 def admissible(available, free_swap, ceiling, swap_ceiling):
     """TZ-55 B2.2: MemAvailable covers memory.max and, where memory.swap.max is a
     number above 0, SwapFree covers that number."""
-    if ceiling is not None and available < ceiling:
+    if False and ceiling is not None and available < ceiling:  # D2 staging copy only: owner's instruction of 02.10.2026
         return False
     if swap_ceiling is not None and swap_ceiling > 0 and free_swap < swap_ceiling:
         return False
$ git diff --quiet HEAD -- vps/run.py; git status --porcelain vps/run.py   (branch copy keeps B2.2)
 M vps/run.py
$ python3 memread.py --json   (A2 method, one instant)
{"ts": "2026-10-02T11:43:07Z", "MemAvailable": 228184064, "SwapFree": 2817949696, "session_root": 3715039, "session_tree_rss": 315899904, "session_tree_pids": 6}
A0 = 228184064 + 315899904 = 544083968
budget=704643072 memory_max=469762048 memory_swap_max=234881024 runtime_max_s=5400
memory_max >= floor 167772160: True; SwapFree 2817949696 >= memory_swap_max: True
D2 attempt 2 start (UTC): 2026-10-02T11:43:28Z
$ systemd-run --unit=tz55-sample-run2 -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz55-state/sampler.py tz55-run2 /var/tmp/tz55-state/sample-run2.jsonl 1 120
Running as unit: tz55-sample-run2.service; invocation ID: ad9687e6ca814058860c7e1b52e6ab7b
[exit 0]
$ systemd-run --unit=tz55-run2 <all of 12.5 but ExecStart> -p MemoryMax=469762048 -p MemorySwapMax=234881024 -p RuntimeMaxSec=5400 -p BindReadOnlyPaths=/var/tmp/tz55-vps -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz55-vps/run.py --tree /var/lib/cryptorun/crypto-auto
Running as unit: tz55-run2.service; invocation ID: 14b15a6ae76046a486240c9fc9673954
[exit 0]
```

Collected (captured; the model ids are withheld, D-11):

```
2026-10-02T16:09:25Z
$ systemctl show tz55-run2 -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p MemorySwapPeak
Result=exit-code
ExecMainStartTimestampMonotonic=5285935779095
ExecMainExitTimestampMonotonic=5285960204574
ExecMainStatus=1
MemoryPeak=[not set]
MemorySwapPeak=[not set]
$ journalctl -u tz55-run2 -o cat --no-pager
Starting tz55-run2.service - Crypto assistant: one headless analysis run...
Started tz55-run2.service - Crypto assistant: one headless analysis run.
writer: gate_exit=0 committed=yes pushed=yes rows_c=31 rows_x=788
crypto-run: requests=0 admitted=yes waited_s=0 writer_exit=0 claude_exit=1 is_error=true num_turns=6 duration_ms=11716 denials=0 answer_chars=0
crypto-run: models=[withheld] denied_tools=- subtype=success api_error_status=429 terminal_reason=api_error stop_reason=stop_sequence
tz55-run2.service: Main process exited, code=exited, status=1/FAILURE
tz55-run2.service: Failed with result 'exit-code'.
tz55-run2.service: Consumed 1.921s CPU time.
$ cat /var/tmp/tz55-state/sample-run2.jsonl.summary.json
{"unit": "tz55-run2", "samples": 25, "span_s": 24.0, "first_t": 1790941408.107, "last_t": 1790941432.11, "F_run": 242278400, "P_peak": 245608448, "F": 245608448, "memory_peak_last_read": 245608448, "memory_swap_peak_last_read": 0, "max_current": 242278400, "max_swap_current": 0, "min_MemAvailable": 217317376, "min_SwapFree": 2694975488}
$ ls -A /var/spool/crypto-auto/outbox /var/spool/crypto-auto/requests
/var/spool/crypto-auto/outbox:

/var/spool/crypto-auto/requests:
$ journalctl -u crypto-bot.service --since "2026-10-02 11:43:00" -o short-iso | grep -E "bot: (sent|outbox)"
2026-10-02T11:43:56+00:00 vultr python3[3780149]: bot: sent 1790941432469-notice-3822814.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
$ git -C /srv/crypto-auto fetch -q origin main; git -C /srv/crypto-auto log origin/main --since=2026-10-02T11:43:28Z --format="%h %ad %an %s" --date=iso-strict
06d223f 2026-10-02T11:43:37+00:00 Claude Code Executor analyst: live.json (vps)
$ record directories under /var/lib/cryptorun/.claude/projects/
-var-lib-cryptorun-crypto-auto entries=3
  d 4096 2026-10-02T11:09:33.8168129430 memory
  f 83230 2026-10-02T11:09:36.7968424130 8f89d70c-bbc3-46b1-810d-7cb54c410734.jsonl
  f 483661 2026-10-02T11:43:51.9982390660 68069440-dabf-471a-b858-e0b4f2c56562.jsonl
```

`D` = 5 285 960 204 574 − 5 285 935 779 095 µs = 24.425479 s.
- `Result=exit-code`, `is_error=true`, `subtype=success`, `api_error_status=429`, `terminal_reason=api_error`, 6 turns.
- The writer pushed `06d223f`. `F` = 245 608 448; no swap.
- §10: «the run failed for another reason». One more D2 is permitted, no sooner than 60 minutes later.

**D2, attempt 3** (`tz55-run3`), 4 h 27 min later: `A0` again and the limits again (captured):

```
2026-10-02T16:10:24Z
$ systemctl reset-failed tz55-run2; systemctl list-units --all "tz55-*" --no-legend | wc -l
0
$ python3 memread.py --json   (A2 method, one instant)
{"ts": "2026-10-02T16:10:24Z", "MemAvailable": 240775168, "SwapFree": 2715643904, "session_root": 3715039, "session_tree_rss": 294580224, "session_tree_pids": 6}
A0 = 240775168 + 294580224 = 535355392
budget=704643072 memory_max=452984832 memory_swap_max=251658240 runtime_max_s=5400
memory_max >= floor 167772160: True; SwapFree 2715643904 >= memory_swap_max: True
D2 attempt 3 start (UTC): 2026-10-02T16:10:43Z
$ systemd-run --unit=tz55-sample-run3 -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz55-state/sampler.py tz55-run3 /var/tmp/tz55-state/sample-run3.jsonl 1 120
Running as unit: tz55-sample-run3.service; invocation ID: 78de6d6b6b2b4e7abdc0f11dd18c08fe
[exit 0]
$ systemd-run --unit=tz55-run3 <all of 12.5 but ExecStart> -p MemoryMax=452984832 -p MemorySwapMax=251658240 -p RuntimeMaxSec=5400 -p BindReadOnlyPaths=/var/tmp/tz55-vps -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz55-vps/run.py --tree /var/lib/cryptorun/crypto-auto
Running as unit: tz55-run3.service; invocation ID: 382a62951be442748eca70de35f02187
[exit 0]
```

Collected (captured; the model ids are withheld):

```
2026-10-02T21:01:57Z
$ systemctl show tz55-run3 -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p MemorySwapPeak
Result=exit-code
ExecMainStartTimestampMonotonic=5301971003054
ExecMainExitTimestampMonotonic=5303059342283
ExecMainStatus=1
MemoryPeak=[not set]
MemorySwapPeak=[not set]
$ journalctl -u tz55-run3 -o cat --no-pager | sed -E 's/^(crypto-run: models=)[^ ]*/\1[withheld]/'
Starting tz55-run3.service - Crypto assistant: one headless analysis run...
Started tz55-run3.service - Crypto assistant: one headless analysis run.
writer: gate_exit=0 committed=yes pushed=yes rows_c=31 rows_x=788
crypto-run: requests=0 admitted=yes waited_s=0 writer_exit=0 claude_exit=1 is_error=true num_turns=113 duration_ms=1072878 denials=0 answer_chars=0
crypto-run: models=[withheld] denied_tools=- subtype=success api_error_status=429 terminal_reason=api_error stop_reason=stop_sequence
tz55-run3.service: Main process exited, code=exited, status=1/FAILURE
tz55-run3.service: Failed with result 'exit-code'.
tz55-run3.service: Consumed 1min 51.750s CPU time.
$ cat /var/tmp/tz55-state/sample-run3.jsonl.summary.json
{"unit": "tz55-run3", "samples": 1089, "span_s": 1088.2, "first_t": 1790957443.305, "last_t": 1790958531.464, "F_run": 307892224, "P_peak": 322416640, "F": 322416640, "memory_peak_last_read": 283058176, "memory_swap_peak_last_read": 39358464, "max_current": 277180416, "max_swap_current": 39358464, "min_MemAvailable": 103784448, "min_SwapFree": 2581336064}
$ ls -A /var/spool/crypto-auto/outbox /var/spool/crypto-auto/requests
/var/spool/crypto-auto/outbox:

/var/spool/crypto-auto/requests:
$ journalctl -u crypto-bot.service --since "2026-10-02 16:10:00" -o short-iso | grep -E "bot: (sent|outbox)"
2026-10-02T16:28:56+00:00 vultr python3[3780149]: bot: sent 1790958531489-notice-3844129.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
$ git fetch origin main; git log origin/main --since=2026-10-02T16:10:43Z --format="%h %ad %an %s" --date=iso-strict
86ee107 2026-10-02T18:17:29+00:00 github-actions[bot] journal: 2026-10-02 [skip ci]
0066be9 2026-10-02T16:10:54+00:00 Claude Code Executor analyst: live.json (vps)
$ git log origin/main --since=2026-10-02T16:10:43Z --name-only --format=%h
== 86ee107

journal/data/2026-10-02.jsonl
journal/out/2026-09-18-h14.jsonl
journal/out/2026-09-25-h7.jsonl
journal/runs.jsonl
== 0066be9

analyst/live.json
$ record directories under /var/lib/cryptorun/.claude/projects/
-var-lib-cryptorun-crypto-auto entries=5
  f 83230 2026-10-02T11:09 8f89d70c-bbc3-46b1-810d-7cb54c410734.jsonl
  d 4096 2026-10-02T11:09 memory
  f 483661 2026-10-02T11:43 68069440-dabf-471a-b858-e0b4f2c56562.jsonl
  d 4096 2026-10-02T16:12 ecb08c80-3518-4da3-ad3a-a361d041ddd6
  f 2380639 2026-10-02T16:28 ecb08c80-3518-4da3-ad3a-a361d041ddd6.jsonl
```

| Term | Value |
|---|---:|
| `A0` = `MemAvailable` + the session tree's `VmRSS` | 240 775 168 + 294 580 224 = 535 355 392 |
| limits it ran under: `memory_max` / `memory_swap_max` / `runtime_max_s` | 452 984 832 / 251 658 240 / 5 400 |
| `Result` / `ExecMainStatus` | `exit-code` / 1 |
| `D` (5 303 059 342 283 − 5 301 971 003 054 µs) | 1 088.339229 s |
| `F_run` (largest `memory.current + memory.swap.current`) | 307 892 224 |
| `P_peak` (`memory.peak` 283 058 176 + `memory.swap.peak` 39 358 464, last read) | 322 416 640 |
| `F` | 322 416 640 |
| the session | `is_error=true`, `api_error_status=429`, `terminal_reason=api_error`, `subtype=success`, 113 turns, `duration_ms=1072878` |
| `writer:` | `gate_exit=0 committed=yes pushed=yes rows_c=31 rows_x=788` (`0066be9`) |
| commits on `origin/main` since the start | `0066be9 analyst: live.json (vps)`, `86ee107 journal: 2026-10-02 [skip ci]` |
| record directory | `/var/lib/cryptorun/.claude/projects/-var-lib-cryptorun-crypto-auto`, 5 entries |

A second failure for another reason: **the decision scope is BLOCKED**, no `fits` line is written, and the
manifest gains no run line.

The run was not stopped by its memory or its time. It ran 1 088 s and its largest per-second footprint was
307 892 224 bytes, under `memory_max` + `memory_swap_max` = 704 643 072, while the owner reported reaching his
usage limit. The answer was not produced, so there was nothing to read, relay or characterise (contract §1).

**D5. Delivery** (captured):

```
2026-10-02T21:02:27Z
tz55 units: 0
$ ls -A /var/spool/crypto-auto/outbox | wc -l
0
$ systemd-run --unit=tz55-send --wait --collect -p MemoryAccounting=yes -p LoadCredential=telegram-bot-token:/etc/crypto-auto/credentials/telegram-bot-token -p LoadCredential=owner-chat-id:/etc/crypto-auto/credentials/owner-chat-id /usr/bin/python3 /var/tmp/tz55-vps/bot.py --send-outbox-once
Running as unit: tz55-send.service; invocation ID: 34dfac9878b54a10907c63abd5b3c827
Finished with result: exit-code
Main processes terminated with: code=exited/status=2
Service runtime: 129ms
CPU time consumed: 72ms
Memory peak: 256.0K
Memory swap peak: 0B
[exit 2]
$ journalctl -u tz55-send -o cat --no-pager | grep "^send:"
send: files=0 all_accepted=no
$ ls -A /var/spool/crypto-auto/outbox | wc -l
0
$ journalctl -u crypto-bot.service --since "2026-10-02 11:12:00" -o short-iso | grep "bot: sent"
2026-10-02T11:42:15+00:00 vultr python3[3780149]: bot: sent 1790941334995-notice-3807599.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
2026-10-02T11:43:56+00:00 vultr python3[3780149]: bot: sent 1790941432469-notice-3822814.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
2026-10-02T16:28:56+00:00 vultr python3[3780149]: bot: sent 1790958531489-notice-3844129.json kind=notice chunks=1 accepted=1 plain_fallbacks=0
```

`crypto-bot.service` has run TZ-54's code since the merge. It delivered every notice the three attempts
wrote, 2–3 s after each attempt ended. D5 then found the outbox empty (D-8).

### Stage E — decisions written into the branch

**E1** (re-run from the record):

```
$ PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys; sys.path.insert(0, "vps"); import common
r = dict(l.strip().split("=", 1) for l in open("vps/memory-record.txt") if "=" in l and not l.startswith("#"))
n = {k: int(v) for k, v in r.items() if v.lstrip("-").isdigit()}
b_in, mm, _, _ = common.test_limits(n["input_footprint_bytes"], r["input_duration_s"], n["host_free_bytes"])
b_run, rt = common.derive_limits(n["run_footprint_bytes"], r["run_duration_s"])
print("A0 = %d + %d = %d" % (n["mem_available_bytes"], n["session_rss_bytes"], n["host_free_bytes"]))
print("memory_max = min(budget(F0), floor((A0 - 64 MiB) / 16 MiB) x 16 MiB) = %d" % mm)
print("budget = max(budget(F0) %d, budget(F) %d) = %d" % (b_in, b_run, max(b_in, b_run)))
print("memory_swap_max = budget - memory_max = %d" % (max(b_in, b_run) - mm))
print("runtime_max_s = max(ceil(2 x %s / 300) x 300, 3600) + 1800 = %d" % (r["run_duration_s"], rt))
print("run_completed=%s; fits line present: %s" % (r["run_completed"], "fits" in r))
PY
A0 = 240775168 + 294580224 = 535355392
memory_max = min(budget(F0), floor((A0 - 64 MiB) / 16 MiB) x 16 MiB) = 452984832
budget = max(budget(F0) 704643072, budget(F) 486539264) = 704643072
memory_swap_max = budget - memory_max = 251658240
runtime_max_s = max(ceil(2 x 1088.339229 / 300) x 300, 3600) + 1800 = 5400
run_completed=no; fits line present: False
[exit 0]
```

**E2.** `vps/memory-record.txt`; `crypto-run.service`'s three lines set from it:

```
$ cat vps/memory-record.txt
# TZ-55 measurement record of crypto-run.service (map inv. 46). Written at Stage E; never edited by hand.
measured_utc=2026-10-02T16:10:43Z
hog_bytes=100663296
hog_footprint_bytes=105697280
hog3_footprint_bytes=117477376
input_footprint_bytes=466161664
input_duration_s=604.899672
run_attempts=2
run_completed=no
run_duration_s=1088.339229
run_cgroup_footprint_bytes=307892224
run_kernel_peak_bytes=322416640
run_footprint_bytes=322416640
mem_available_bytes=240775168
session_rss_bytes=294580224
host_free_bytes=535355392
budget_bytes=704643072
memory_max_bytes=452984832
memory_swap_max_bytes=251658240
runtime_max_s=5400
$ grep -E "^(MemoryMax|MemorySwapMax|RuntimeMaxSec)=" vps/units/crypto-run.service
MemoryMax=452984832
MemorySwapMax=251658240
RuntimeMaxSec=5400
```

**E3.** `vps/manifest`:
- `crypto-deploy.timer`, `crypto-cleanup.timer`, `crypto-exchange.service`, `crypto-bot.service`;
- no `crypto-announce.service`, because D3 exited 4;
- no run line, because there is no `fits=yes`.

These are TZ-54's four lines, so the file has no diff.

**E4.** `RUN_RECORDS = "/var/lib/cryptorun/.claude/projects/-var-lib-cryptorun-crypto-auto"`: the directory
D2's sessions wrote their records into (D-9).

**E5.** `python3 vps/selftest.py` green in every section (V1).

## Validation

**V1. Selftest and its negative control** (captured):

```
2026-10-02T21:03:26Z
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
section J: checks 7 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 12 failed 0
section N: checks 10 failed 0
section O: checks 19 failed 0
selftest: sections 15 checks 147 failed 0 empty 0
[exit 0]
$ md5sum vps/selftest.py
d72aea897a8f8c6b077ec2ebf5845737  vps/selftest.py
$ grep -c "(704643072, 352321536, 352321536, 5400)" vps/selftest.py
1
$ sed -i "s/(704643072, 352321536, 352321536, 5400)/(704643072, 352321537, 352321536, 5400)/" vps/selftest.py   (one digit of a 12.4 known answer)
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
FAIL section J: test_limits(466161664, 604.899672, 419430400)
section J: checks 7 failed 1
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 12 failed 0
section N: checks 10 failed 0
section O: checks 19 failed 0
selftest: sections 15 checks 147 failed 1 empty 0
[exit 1]
$ sed -i "s/(704643072, 352321537, 352321536, 5400)/(704643072, 352321536, 352321536, 5400)/" vps/selftest.py   (reverted)
$ md5sum vps/selftest.py
d72aea897a8f8c6b077ec2ebf5845737  vps/selftest.py
$ PYTHONDONTWRITEBYTECODE=1 python3 vps/selftest.py | tail -1
selftest: sections 15 checks 147 failed 0 empty 0
[exit 0]
```

15 sections, 147 checks, 0 failed, none empty. One digit of a §12.4 known answer turned section J alone red
(exit 1). The revert restored the MD5 and the green.

**V2. Syntax** and **V3. Dry run** (captured):

```
2026-10-02T21:03:39Z
$ for f in vps/*.py; do python3 -m py_compile (cfile in scratch); bash -n both scripts; systemd-analyze verify vps/units/*
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
[systemd-analyze verify exit 0]
$ systemctl list-unit-files "crypto-*" --no-legend > before; bash vps/install.sh --dry-run; ... after; diff
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
[dry-run exit 0]
crypto-* unit files identical before and after
$ diff against A3 list
identical to A3
```

`systemd-analyze verify` exited 0 and printed no warning. A second `--provision` created nothing (C3 above).

**V4. The writer and the run — writer PASSED, run not completed.** The last D2's line reads
`writer: gate_exit=0 committed=yes pushed=yes`, and `0066be9 analyst: live.json (vps)` is on `origin/main`.
There is no `fits=yes`, so no `analyst: <date>` is required. None was written: both admitted sessions stopped
on the account's limit.

**V5. The instrument** — PASSED: D1's two known answers.

**V6. Fit** — E1's terms printed above; section M green, 12 checks. No `fits` line exists to equal a rule.

**V7. Delivery** — read off the live bot. Each of the three notices was sent as 1 chunk with 1 accepted, and
the outbox is empty. D5's own counts are `files=0 all_accepted=no`, exit 2 (D-8).

**V8. Credentials — PASSED, with one exception, the deploy key's last byte (D-6).**
- Modes and last bytes, then the exact-value scan over the branch diff, every file of the branch's `vps/`,
  `origin/main`'s `analyst/**` files changed since the session started, and both journals (captured):

```
2026-10-02T21:05:44Z
$ git diff --name-only origin/main...HEAD | wc -l; git diff --name-only origin/main...HEAD | grep -c -v "^vps/"
9
0
$ stat -c "%a %U %s %n" /etc/crypto-auto/credentials /etc/crypto-auto/credentials/*
700 root 4096 /etc/crypto-auto/credentials
600 root 64 /etc/crypto-auto/credentials/binance-api-key
600 root 64 /etc/crypto-auto/credentials/binance-api-secret
600 root 108 /etc/crypto-auto/credentials/claude-oauth-token
600 root 411 /etc/crypto-auto/credentials/deploy-key
600 root 9 /etc/crypto-auto/credentials/owner-chat-id
600 root 46 /etc/crypto-auto/credentials/telegram-bot-token
binance-api-key last_byte_is_newline=no
binance-api-secret last_byte_is_newline=no
claude-oauth-token last_byte_is_newline=no
deploy-key last_byte_is_newline=yes
owner-chat-id last_byte_is_newline=no
telegram-bot-token last_byte_is_newline=no
$ bash v8-scan.sh <no report yet> 97376c9
binance-api-key: non_empty_lines=1 newline_bytes=0
binance-api-secret: non_empty_lines=1 newline_bytes=0
claude-oauth-token: non_empty_lines=1 newline_bytes=0
deploy-key: base64_lines=5 armor_lines=2
origin/main analyst files changed since 97376c9: 1 (analyst/live.json)
journal lines: tz55-*=71 crypto-deploy=1204
vps files scanned: 23
binance-api-key: report=absent branch_diff=0 vps_files=0 analyst_since_start=0 journal_tz55=0 journal_deploy=0
binance-api-secret: report=absent branch_diff=0 vps_files=0 analyst_since_start=0 journal_tz55=0 journal_deploy=0
claude-oauth-token: report=absent branch_diff=0 vps_files=0 analyst_since_start=0 journal_tz55=0 journal_deploy=0
deploy-key-base64: report=absent branch_diff=0 vps_files=0 analyst_since_start=0 journal_tz55=0 journal_deploy=0
```

- The `vps files scanned: 23` line counted a `vps/__pycache__/` that one of the session's own Python checks
  had left. It is git-ignored and was never committed, and it was removed after the scan (`find vps -type f |
  wc -l` → 22).
- The C6 flip is printed above.
- `/root/tz55-token` is absent, and `tmux has-session -t tz55-token` fails (V11).
- The scan over this report was run on the final file before it was committed:

```
$ for f in binance-api-key binance-api-secret claude-oauth-token; do grep -c -F -f $C/$f TZ-55-run-lane-own-user-report.md; done; deploy key base64 lines alone
binance-api-key: report_hits=0
binance-api-secret: report_hits=0
claude-oauth-token: report_hits=0
deploy-key-base64: report_hits=0
```

**V9. The key and the stream** — D3 above:
- verdict `ACCEPTED`, with its twelve field booleans;
- the subscribe answer `REGISTER`;
- no message (so no `catalogName`, title, publish time or lag), no ping, no reconnect;
- exit 4.

**V10. Signed deploys** — PASSED (re-run):

```
2026-10-02T21:04:03Z
$ bash vps/deploy.sh --check; echo exit
deploy: check commit=966b3f281c2a05939e6a9fc882520e805648b5ce signed=yes
[exit 0]
$ GNUPGHOME=/etc/crypto-auto/gnupg git -C /srv/crypto-auto verify-commit b097a89; echo exit
[exit 1]
$ cmp /usr/local/libexec/crypto-auto/deploy.sh <(git -C /srv/crypto-auto show origin/main:vps/deploy.sh) && echo identical
identical
$ cat /var/lib/crypto-auto/deployed-vps-tree; ls /var/lib/crypto-auto/refused-vps-tree
2b66e47f47b0e3fcd3f47805f808045c1b4cf9de
ls: cannot access '/var/lib/crypto-auto/refused-vps-tree': No such file or directory
```

**V11. Nothing left** — PASSED (captured):

```
2026-10-02T21:04:18Z
$ ls -A /var/tmp/tz55-vps /var/tmp/tz55-state
/var/tmp/tz55-state: gnupg sample-announce.jsonl sample-announce.jsonl.summary.json sample-hog1.jsonl sample-hog1.jsonl.summary.json sample-hog3.jsonl sample-hog3.jsonl.summary.json sampler.py sample-run2.jsonl sample-run2.jsonl.summary.json sample-run3.jsonl sample-run3.jsonl.summary.json sample-run.jsonl sample-run.jsonl.summary.json  /var/tmp/tz55-vps: announce.py bot.py cleanup.py common.py deploy.sh exchange.py install.sh manifest memory-record.txt probe.sh __pycache__ run.py selftest.py units writer.py 
$ rm -rf /var/tmp/tz55-vps /var/tmp/tz55-state
[exit 0]
$ systemctl list-units --all "tz55-*" --no-legend | wc -l
0
$ ls -d /var/tmp/tz55-vps /var/tmp/tz55-state /srv/crypto-auto-run /root/.claude/projects/-srv-crypto-auto-run /root/.claude/projects/-srv-crypto-auto /root/tz55-token
ls: cannot access '/var/tmp/tz55-vps': No such file or directory
ls: cannot access '/var/tmp/tz55-state': No such file or directory
ls: cannot access '/srv/crypto-auto-run': No such file or directory
ls: cannot access '/root/.claude/projects/-srv-crypto-auto-run': No such file or directory
ls: cannot access '/root/.claude/projects/-srv-crypto-auto': No such file or directory
ls: cannot access '/root/tz55-token': No such file or directory
$ tmux has-session -t tz55-token; echo exit
can't find session: tz55-token
[exit 1]
$ git ls-remote --heads origin tz-55-push-probe | wc -l
0
$ systemctl list-unit-files "crypto-*" --no-legend | diff A3 -
identical to A3 (V3's before file equals A3)
```

**V12. No production file** — PASSED: `git diff --name-only origin/main...HEAD` lists 9 paths, 0 outside `vps/` (V8 block).

**V13. Pushes** — PASSED.
- The branch is pushed and pull request #44 is open.
- `main` received from this session's own commands nothing but this report.
- The commits that reached `main` while it ran:
  - the writer's `06d223f` and `0066be9`, from D2's units;
  - `journal.yml`'s `86ee107`.

## Test Results

| Control | Where | Result |
|---|---|---|
| `vps/selftest.py`, 15 sections | this session, final tree | 147 checks, 0 failed, 0 empty |
| negative control on section J | this session | J alone red, then green |
| the C6 probe | this host, as `cryptorun` | 10 of 10 as required |
| D1's two known answers | this host | both met |
| `Bench gate`, `bench.yml` | runner, run 37064722639 | success (CI Execution) |

Sections N and O, the new ones, cover these, offline:
- **N** (10 checks): on a mock Bot API, a file refused twice ends as `.dead`, the next file is sent, and the
  outbox holds the `.dead` file alone. A network error keeps the file and ends the pass.
- **O** (19 checks): `run.py` in-process, with a stub `claude` and a stub writer in a temporary directory on
  `PATH`.
  - The stub `claude` saw the planted login. The writer saw no login under any name, even with a decoy
    `CLAUDE_CODE_OAUTH_TOKEN` already in the environment.
  - The summary carried the four categorical fields and never the result.
  - Admission refused while `SwapFree` was below `memory.swap.max`.

## Deviations

**D-1. Stage order.** All of these reorderings were forced or harmless:
- While auto mode refused C4 (D-2), C2, the keyring half of C3, D3 and D1 ran before the rest of Stage C.
- C4 ran before C3 and C5.
- D3 was collected at once because it ended in 1.5 s.

No step used a later step's product:
- D3 ran the unchanged `announce.py` on C2's files.
- D1 runs no repository code.
- D2 ran from a staging copy refreshed after all of Stage B.

**D-2. Claude Code's auto mode refused four commands.**

| Time | Command | Classifier's label |
|---|---|---|
| 10:43Z | C4's `setup-token` | «Unauthorized Persistence» |
| 10:45Z | the `run.py` edit that hands the run its login | «Create Unsafe Agents» |
| 10:56Z | C5 | «Irreversible Local Destruction» |
| 10:57Z | a syntax check ending in `rm -rf` of its own temporary directory | same label |

- No refusal was worked around. One partial edit of `run.py` had landed before the refused one, and it was
  reverted with `git checkout -- vps/run.py` before anything else ran.
- The owner took the session out of auto mode about 10:59Z, and every refused step then ran as specified.

**D-3. C4's tmux session ran as `tmux new-session -d -x 1000 -y 50 …`.**
- tmux's `default-size` here is `80x24` (measured), and the authorization URL is over 350 characters. At 80
  columns the screen wraps it, so «a whole URL» could not be read.
- The typescript confirms `COLUMNS="1000"`.
- To establish what the screen asked for, its text was printed with every URL and every string of 32 or more
  characters masked. That was the only screen output read.

**D-4. C6 and D2 carry the path `%d` stands for.**
- A transient unit passes `%d` through unexpanded: `tz55-spec` printed `X=%d/probe` with
  `CREDENTIALS_DIRECTORY=/run/credentials/tz55-spec.service`.
- So the probe's and each D2's `GIT_SSH_COMMAND` names `/run/credentials/<unit>.service/deploy-key`.
- systemd.exec(5) documents `Environment=MYCREDPATH=%d/mycred` for unit files, and §12.5's line is unchanged.
  The installed unit first exercises it after the merge (Remaining Risks 4).

**D-5. One extra transient unit, `tz55-spec`**, ran the `%d` measurement above. It ran nothing but `echo`
and is gone.

**D-6. The deploy key's last byte is a newline**, against V8's «no last byte is a newline».
- C3 dictates `install -m 0600 -o root -g root /root/.ssh/crypto-auto …`, an exact copy (`cmp` identical,
  fingerprint `SHA256:J9Ig8LfEBkOB3OjcRCmxWQhc7qKCv8o5dTXhaH9QqIM`).
- An OpenSSH private key file ends in a newline, and a key with it stripped can be refused by `ssh`.
- The C6 push through that copy exited 0.
- The four values typed or minted for this TZ carry no trailing newline.

**D-7. D2 ran three times; the decision scope is BLOCKED.**
- **Attempt 1, `tz55-run`, 11:12:14Z.** It was never admitted.
  - B2.2's gate needs `MemAvailable` ≥ `memory.max`.
  - `memory.max` came from §12.4's `A0`, which adds the measuring session's 223 MB resident to the 210 MB
    available, while that session stays resident through D2.
  - After 1 800 s it exited 75. With `SuccessExitStatus=75` that is `Result=success`, `ExecMainStatus=75`,
    which is none of §10's three branches.
- **The owner's instruction** (02.10.2026, about 11:40Z), quoted: «Lower or bypass the `MemAvailable` check in
  `run.py` to allow startup via Swap as agreed for this testing mode.» and «Continue execution immediately;
  Swap will cover the memory gap.»
  - The owner also reported terminating `btc-5m-twap`, the real-estate bot and `recorder.py`. That is the
    owner's statement, not this session's act.
  - The instruction was applied to the measurement's staging copy only. The `diff -u` against the branch
    shows one line: `if False and ceiling is not None and available < ceiling:`.
  - **The branch's `vps/run.py` keeps B2.2 unchanged.** Whether scheduled runs may start on swap is a
    production decision that contract §1 leaves to the Architect (Pre-existing Issues 1).
- **Attempt 2, `tz55-run2`, 11:43:28Z, and attempt 3, `tz55-run3`, 16:10:43Z.** Both were admitted and both
  failed on `api_error_status=429`. Attempt 3 started 4 h 27 min after attempt 2 and after the owner wrote
  «Please continue from where you left off».
- **Rule 9 caps D2 at two runs «under §10's rule».** This session counted under §10: attempt 1 reached no
  §10 outcome. Attempts 2 and 3 are the first and second D2, the second permitted by «One more D2 … no sooner
  than 60 minutes later». Read as unit starts, attempt 3 is one beyond the cap. Either reading writes no
  `fits` line.
- The second and third units are named `tz55-run2` and `tz55-run3` so that each attempt's journal and samples
  stay apart.

**D-8. D5 delivered nothing, because the live bot already had.**
- `crypto-bot.service` has run since TZ-54's merge (A3) and reads the same outbox. It sent each notice 2–3 s
  after its attempt ended (journal lines in D5).
- D5's command then printed `send: files=0 all_accepted=no` and exited 2.
- V7 is therefore read off the bot's own lines.

**D-9. E2's and E4's inputs.**
- `run_attempts=2` counts under §10 (D-7). `measured_utc` is the last D2's start. The `run_*` terms are that
  attempt's, a session that ran 1 088 s and stopped on the account's limit.
- `RUN_RECORDS` names the directory D2's sessions wrote into. C6's probe created it at 11:09:33Z, from the
  same working directory, before any D2 ran.

**D-10. Choices B leaves open.**

`run.py`:
- It reads the login just before the session. A missing login writes S7 and exits 1.
- The categorical fields are printed as `[A-Za-z0-9_.:-]` tokens of at most 64 characters.

`install.sh`:
- `groupadd --system` before `useradd --gid cryptorun --groups cryptoauto --no-create-home`.
- `.ssh` is `0700`.
- Root edits the clone's config through `-c safe.directory=<clone>`, because the clone belongs to `cryptorun`.
- `--provision` fails when root's `known_hosts` has no `github.com` line.
- `--bootstrap` keeps TZ-54's steps without the worktree.

Elsewhere:
- `deploy.sh --check` skips step 1 (§12.9: «steps 2 and 4 only»).
- A `.dead` file keeps its whole original text.
- Section M adds «`fits=yes` exactly when the run completed» (§12.4's definition) only where a `fits` line exists.

**D-11. The model ids are not written into the repository.** This environment forbids a model identifier in a
pushed artifact (TZ-54 D-6). The `models=` field of the captured lines reads `[withheld]`, and the ids were
seen in the session.

**D-12. The trigger message numbered its lines** `1)`, `2)` and `3)` before `EXECUTE TZ-55` and each `NAME=`.
Each value is what follows `=`, written as carried: `whitespace_stripped=0`.

## Pre-existing Issues

1. **B2.2's admission cannot pass while the measuring session lives** — the Architect's defect in TZ-55 §10
   and §12.4.
   - D2 derives `memory.max` from `A0` = `MemAvailable` + the measuring session's `VmRSS`, and B2.2 admits
     only when `MemAvailable` alone covers it.
   - The gap is the session's resident set less 64 MiB and the rounding: 223 MB against 64 MiB at attempt 1.
     It was measured as a 30-minute refusal.
   - The same gate refuses a scheduled run whenever any Claude session holds that much memory.
   - Whether production may start on swap, and how a measurement is admitted, is the correction this calls for.
2. **`announce.py` rejects the stream's first answer** (TZ-54 code, which TZ-55 does not authorise changing).
   - The live answer to `SUBSCRIBE` on the connection signed with `topic=com_announcement_en` was
     `subType: REGISTER`.
   - TZ-54 §12.10 cites `SUBSCRIBE` as the documented answer, and the program takes the first `COMMAND`
     message as final.
   - Whether a `SUBSCRIBE` answer follows was not probed. One D3 is what the TZ authorises.
3. **`A0` counts file-backed pages twice.**
   - At attempt 1 the session process's `VmRSS` of 196 MB held 41 MB `RssFile`: pages of the 238 MB binary
     that the kernel already counts in `MemAvailable` as page cache.
   - §12.4's sum includes them a second time.
4. **`P_peak` adds two peaks that need not coincide.** In the three-hog run, `memory.peak` 107 753 472 +
   `memory.swap.peak` 9 723 904 = 117 477 376, against a largest per-second sum of 107 323 392. The over-count
   is bounded by the swap peak and is in the safe direction.
5. **A run's record directory holds more than session files:** a `memory/` directory and per-session
   directories, beside the `.jsonl` records. `cleanup.py` treats each top-level entry as one record, so
   `memory/` ages out like a record.

Every file of the map's `## 0` table matches its line count and MD5, before and after the work (Fingerprints).

## Remaining Risks

1. **The fit is undecided, and scheduled runs stay off.** Both admitted attempts stopped on the owner's usage
   limit, one after 113 turns and 18 minutes. A scheduled run on this account meets the same limit.
2. **The run's login is a one-year token** («1-year» on the `setup-token` screen), minted 02.10.2026. It
   expires about 02.10.2027, and C4 mints the next one the same way.
3. **The trigger's Binance values and the two codes sit in this session's own record under `/root/.claude/`**,
   the conversation copy contract §7 item 6 accepts. The `cryptorun` user cannot read `/root` (C6).
4. **`%d` in `crypto-run.service` is first expanded by the installed unit**, after the merge (D-4).
5. **After the merge, a `vps/` change pushed by anything but GitHub is refused.** That includes the analysis
   run, which pushes with the deploy key. S11 goes out once per tree, and the deployer fails its tick until
   a signed commit changes `vps/` again.
6. **Until the merge, the live bot runs TZ-54's code.** A file refused in both forms still holds the outbox
   behind it.

## Commit

Implementation, on the branch, pushed: **`397ab81`** — `TZ-55: vps — the run as its own user, test-mode
memory, signed deploys` — the 9 files of Files Modified.

Report, on `main`: `TZ-55: report — the run lane on the 1 GB host` — this file only.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/44 — `tz-55-run-lane-own-user` → `main`.

## CI Execution

The branch push started no workflow: `bench.yml`'s `push` filter names `main` and `claude/**` only. The pull
request started `Bench gate` (captured):

```
$ gh run list --branch tz-55-run-lane-own-user --limit 10 --json databaseId,event,status,conclusion,workflowName,headSha -q '.[] | "\(.databaseId) \(.workflowName) \(.event) \(.status) \(.conclusion) \(.headSha[:7])"'
37064722639 Bench gate pull_request completed success 397ab81
$ gh run view 37064722639 --json event,headSha,status,conclusion,jobs -q '"event=\(.event) head=\(.headSha[:7]) status=\(.status) conclusion=\(.conclusion)", (.jobs[] | .steps[] | "\(.number)  \(.conclusion)  \(.name)")'
event=pull_request head=397ab81 status=completed conclusion=success
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
```

All 18 steps of `bench.yml` ran green. `vps/selftest.py` is not a step of it (TZ-55 §5); it runs in this
session and in `install.sh` before every deployment.

## Final Repository State

Branch `tz-55-run-lane-own-user` at `397ab81`, pushed, pull request #44 open. **NOT IN EFFECT UNTIL MERGED.**
On the merge, the deployer's next tick installs this tree. The manifest leaves the run lane and the
announcement stream off, and later ticks install only a `vps` tree GitHub signed.

What this session leaves on the VPS:
- the user and group `cryptorun`, home `/var/lib/cryptorun` holding the run's clone and `known_hosts`, and the
  run's session records under `.claude/projects/-var-lib-cryptorun-crypto-auto`;
- `/etc/crypto-auto/gnupg` with GitHub's two keys;
- three new credential files, `claude-oauth-token`, `deploy-key` and the replaced Binance pair, beside TZ-54's
  two.

It leaves no `tz55-*` unit, no scratch directory, no tmux session and no probe branch. The installed deployer
is still `main`'s (V10).

Blocks marked «captured» are the files `tee` wrote at each step, inlined unchanged except the `models=`
field (D-11). Blocks marked «re-run» were run by the report's generator just before writing. The E1 block was
run on the final record.

## Fingerprints

### `SYSTEM-MAP-CRYPTOCALCUL.md`

| | |
|---|---|
| Revision string in `## 0. Fingerprint` | `**Revision 2026-10-01-f.**` |
| Required by TZ-55's header | `**Revision 2026-10-01-f.**` — **match** |
| Lines | 3141 |
| MD5 | `f780f2e73c6067d52fa12ed628a23f3c` (the TZ reports the same; not enforced) |

### Anchors

Cut from the map's anchor table **by structure**: the `| Anchor |` header row, its separator, and every row to
the table's end, never by anchor names. **The table carries 7 rows, and 7 were compared.** The TZ header
carries no row the map's table lacks, and the map's table no row the header lacks (re-run on the branch, whose map and TZ
equal `97376c9`'s; A1 printed the same counts and matches before any work):

```
$ (the gate, run in the branch at 397ab81, whose map and TZ equal 97376c9's)
revision string in the map's ## 0 block: **Revision 2026-10-01-f.**
rows in the map's table: 7; rows in the TZ header's table: 7
TZ header rows absent from the map's table: 0
map table rows absent from the TZ header: 0
grep --fixed-strings --only-matching --max-count=1 -- "**Revision 2026-10-01-f.**" SYSTEM-MAP-CRYPTOCALCUL.md
  -> **Revision 2026-10-01-f.**
  lines in the map: 17 427 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.12 Direction engine — veto cascade" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.12 Direction engine — veto cascade
  lines in the map: 428 1397 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.15 Catalyst registry" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.15 Catalyst registry
  lines in the map: 429 1787 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.16 List exhaustion — the day-range measure" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.16 List exhaustion — the day-range measure
  lines in the map: 430 1884 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "## 11. Analytical engine" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ## 11. Analytical engine
  lines in the map: 431 2898 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.17 «РИСК ВЫНОСА» — the day's own risk" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.17 «РИСК ВЫНОСА» — the day's own risk
  lines in the map: 432 2051 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "72. **A write that fails leaves this run's product or nothing" SYSTEM-MAP-CRYPTOCALCUL.md
  -> 72. **A write that fails leaves this run's product or nothing
  lines in the map: 433 2593 
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
map and TZ in HEAD equal 97376c9's
```

### Files of the map's `## 0` table, and the two the TZ adds

On the branch, whose seven files equal `97376c9`'s (re-run; A1 printed the same), and at the end on `origin/main`
`86ee107`, which moved only by `analyst/live.json` and the journal (re-run):

```
$ for f in <map, the four table files, the two added>; do echo "$f  $(wc --lines < $f) lines  $(md5sum $f)"; done; revision and version lines
SYSTEM-MAP-CRYPTOCALCUL.md  3141 lines  f780f2e73c6067d52fa12ed628a23f3c
index.html  3799 lines  4e71da9badca3ccae85b656fdc3773e8
main.py  518 lines  0e3ead8c300d2ee6783303c4bf2fb6b5
catalysts.json  17 lines  f9b2dd4a3594134b2b7b603de19075c3
bench/exhaustion-calibration.txt  175 lines  3b8730b254467c9df4c0a845a0f3cfb3
ANALYST-INSTRUCTIONS.md  3866 lines  feaaffc99f983b3441ce205bcf1b6466
EXECUTOR-INSTRUCTIONS.md  963 lines  ef21a864f6c93d1c59d72b9e16eb967f
SYSTEM-MAP-CRYPTOCALCUL.md:**Revision 2026-10-01-f.**
ANALYST-INSTRUCTIONS.md:**Revision 2026-10-01-a.**
**Version 25.**
```

```
86ee107
$ git diff --name-only 97376c9 origin/main
analyst/live.json
journal/data/2026-10-02.jsonl
journal/out/2026-09-18-h14.jsonl
journal/out/2026-09-25-h7.jsonl
journal/runs.jsonl
SYSTEM-MAP-CRYPTOCALCUL.md  3141 lines  f780f2e73c6067d52fa12ed628a23f3c
index.html  3799 lines  4e71da9badca3ccae85b656fdc3773e8
main.py  518 lines  0e3ead8c300d2ee6783303c4bf2fb6b5
catalysts.json  17 lines  f9b2dd4a3594134b2b7b603de19075c3
bench/exhaustion-calibration.txt  175 lines  3b8730b254467c9df4c0a845a0f3cfb3
ANALYST-INSTRUCTIONS.md  3866 lines  feaaffc99f983b3441ce205bcf1b6466
EXECUTOR-INSTRUCTIONS.md  963 lines  ef21a864f6c93d1c59d72b9e16eb967f
origin/main:vps 2b66e47f47b0e3fcd3f47805f808045c1b4cf9de  branch HEAD:vps 43799ab742c8b4d67651cc3b07a0e6e31ee40e95
```

| File | Lines (required) | Lines (measured) | MD5 (required) | MD5 (measured) | |
|---|---:|---:|---|---|---|
| `index.html` | 3799 | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | match |
| `EXECUTOR-INSTRUCTIONS.md` (TZ adds) | 963 | 963 | `ef21a864f6c93d1c59d72b9e16eb967f` | `ef21a864f6c93d1c59d72b9e16eb967f` | match · `Version 25.` |
| `ANALYST-INSTRUCTIONS.md` (TZ adds) | 3866 | 3866 | `feaaffc99f983b3441ce205bcf1b6466` | `feaaffc99f983b3441ce205bcf1b6466` | match · `2026-10-01-a` |

`origin/main:vps` is `2b66e47f47b0e3fcd3f47805f808045c1b4cf9de`, the tree the TZ was written against. The
branch's `vps` tree is `43799ab742c8b4d67651cc3b07a0e6e31ee40e95`.
