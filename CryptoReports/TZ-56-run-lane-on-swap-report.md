# Implementation Report — TZ-56

## Status

**COMPLETED. A run will start on swap.** C1's `crypto-run: limits` line set `memory_max=167772160` and `memory_swap_max=536870912` on the probe's own unit. Their sum is 704 643 072, the record's `budget_bytes`. The unprivileged main process (uid 995) read exactly that pair from its cgroup. C1b started from a different pair (134 217 728 / 570 425 344) and the main process again read 167 772 160 / 536 870 912, so the start sets the pair and does not inherit it. `crypto-run.path` is in the manifest, so the bot's button and the watcher's run requests take effect when PR #45 is merged. `crypto-run.timer` stays off.

**The announcement stream is not enabled.** A5 selected R1: the connection that sent no command was answered `REGISTER`/`SUCCESS`. D3, on the branch's code, accepted that answer and held the connection for 10 802 s with 356 pings, no reconnect and no close frame. It received **0 data messages** and exited 2, so under E1 `crypto-announce.service` is not listed. Whether R1's reading of `REGISTER` is right remains open (Remaining Risks R-1).

No `claude` process was started by this session or by any unit it started. Every `tz56-*` unit and scratch directory is gone (V9). The previous TZ is merged: TZ-55's PR #44 is `closed`, `merged: true`, merge commit `2aaa74f` (A1).

## Inbound Filing

None. `CryptoTZ/TZ-56-run-lane-on-swap.md` is at its canonical path on `origin/main` (added by `4f51201`), in one copy and under one name.

## Scope Executed

**Class: branch TZ** (contract §8). The scope names `vps/**` and `.claude/settings.json`, which are outside `CryptoReports/**`.

| Stage | Executed | Outcome |
|---|---|---|
| A1 | §4a steps 1–6; §5 gate | gate passed: revision `2026-10-03-a`, 7 of 7 anchor rows, 4 of 4 files, contract `**Version 26.**` |
| A2 | what TZ-55's merge put into effect | marker `43799ab7…` = `origin/main:vps`; `deploy: check commit=2aaa74fa… signed=yes` — both known answers met; the literal `--since 2026-10-03` read nothing (D-1) |
| A3 | tools | `systemd 255 (255.4-1ubuntu8.17)`; `/run/systemd/system.control/` absent |
| A4 | the auto memory that existed | 2 kept directories, 45 and 0 files: names, sizes, line counts and mtimes only |
| A5 | the stream, on `main`'s code | **R1** |
| B1–B7 | the code, on the branch | 7 files modified, 1 created |
| C1 | the limits, on the VPS | every known answer met; C1b added (D-3) |
| D3 | the stream, on the branch's code | exit 2: 0 data messages in 10 800 s |
| E1 | `vps/manifest` | `crypto-run.path` added; `crypto-announce.service` not added; `crypto-run.timer` never |
| E2 / V1–V11 | validation | every item run; results in `## Test Results` |

Out of scope and untouched: `crypto-run.timer`, `vps/memory-record.txt`, every other unit file, `bench.yml`, and everything under `/etc/crypto-auto/`, `/srv/crypto-auto` (except the fetches of the TZ-dictated `deploy.sh --check`; see D-8) and `/var/lib/cryptorun`.

## Files Created

| File | Lines | MD5 |
|---|---:|---|
| `.claude/settings.json` | 3 | `a2fa8dc4d37414161e16a305dad1e6f9` |

## Files Modified

| File | Hunks (`git diff -U0`) | Lines after | MD5 after |
|---|---:|---:|---|
| `vps/announce.py` | 8 | 402 | `56131f9ab089bca8682882500f596202` |
| `vps/common.py` | 3 | 316 | `bb48e9c459597b6dc9a86266a46fd6a5` |
| `vps/deploy.sh` | 10 | 147 | `04cfb9a75d99e0d6b3a90ec16799a21a` |
| `vps/manifest` | 1 | 5 | `4368b19c14fa75cb5289526592f66096` |
| `vps/run.py` | 24 | 331 | `4be5ada20662f7876715b15b5250722d` |
| `vps/selftest.py` | 14 | 680 | `4b09818d510f0dfa97d795f2d6512f2b` |
| `vps/units/crypto-run.service` | 3 | 37 | `dc6ac1073c42b03c1a2f3b754e28bca0` |

The branch's `vps` tree is `b9f97526335fa2a12f60bab9bd164ded1250dd7c`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**B1 `vps/common.py`.**
- `RECORD_PATH` is the `memory-record.txt` beside the module.
- `read_record(path=RECORD_PATH)` is now the one parser of the record. Selftest section M uses it, and the selftest's own copy is removed.
- `start_limits(available_bytes, budget_bytes)` implements §12.2 on `RESERVE_BYTES` and `MEMORY_MAX_FLOOR_BYTES`: `min(budget, max(160 MiB, floor((available − 64 MiB) / 16 MiB) × 16 MiB))`, with the rest of the budget as swap.
- `derive_limits` and `test_limits` are unchanged.

**B2 `vps/run.py`.**
1. **`--limits`.** `set_limits()` reads `MemAvailable` and `SwapFree`, then `budget_bytes` through `common.read_record()`, then `common.start_limits()`. It takes the unit name from the last component of `/proc/self/cgroup` and runs `systemctl set-property --runtime <unit> MemoryMax=<m> MemorySwapMax=<s>`. It logs the one dictated `crypto-run: limits …` line and returns 0 on every path. A value it could not read prints as `-`, and `set=-` means systemctl never ran. It reads no credential, consumes no request and touches no tree. It sets nothing when its cgroup is not a `.service` (D-2).
2. **Admission.** `admissible()` now requires `available − RESERVE_BYTES ≥ memory.max`; the swap condition is unchanged. A limit that reads `max` or is unreadable sets no condition, as before. `_own_cgroup_limit()` now returns `max` separately from `None` (unreadable), so §12.4 can print either (D-5). `admit(seen)` keeps the limits it read and the meminfo values of the admitting or last poll. The poll, the 1 800 s and S6 are unchanged.
3. **The third summary line.** `summary()` prints §12.4's line on every path, including SIGTERM. The peaks are this cgroup's `memory.peak` and `memory.swap.peak`, read when the summary is written, which is after the session on the session path. Tokens come from `result.json`'s `usage` and are printed only when they are integers. `cost_usd` is `total_cost_usd`, printed only when it is a finite number; otherwise `-`. `result` is never printed.

**B3 `vps/announce.py` — branch R1.**
- `ANSWER_SUBTYPE = "REGISTER"`. The `SUBSCRIBE` constant and its send are removed.
- `answer_of(frames, sub_type)` is pure and returns `(answer, pending, skipped)` exactly as dictated. It reads no frame after the answer.
- `frames_until(ws, deadline)` yields the frames received until the 20 s deadline; a receive timeout ends the frames.
- `connect()` feeds those frames to `answer_of`, extends `pending`, logs each skipped frame as `announce: command answer <json, sorted keys>` (D-6), logs the unchanged `announce: subscribe answer <json>`, and succeeds if and only if the answer exists and its `data` is `SUCCESS`.

**B4 `vps/deploy.sh` — §12.5.**
- `range_check()` sets `base` to the clone's `HEAD`. It lists `git log --first-parent --format=%H "$base..origin/main" -- vps` and verifies every commit with `GNUPGHOME="$SIGNERS" git verify-commit`, counting `commits` and `unsigned` and keeping the newest unverified commit. Both git reads are plain assignments under `set -e`, so a failed read ends the script non-zero and never passes as an empty list.
- In the tick, step 4: any unverified commit → `deploy: unsigned vps commit <newest>, not installed`, S11 through `tell_once`, exit 1.
- `--check` takes no arguments or exactly two. With two it takes neither the lock nor the fetch. It prints `deploy: check base=<h> commits=<n> unsigned=<k> signed=<yes|no>` and exits 0 only when `unsigned=0`.
- Every other step is unchanged.

**B5 `vps/selftest.py` — §12.6.**
- **J:** §12.2's four known answers, plus ten values from 0 to 4 GiB.
- **M:** the record rules through `common.read_record`; the unit's `MemoryMax=` is the floor, `MemorySwapMax=` is the budget less the floor, and `RuntimeMaxSec=` is `runtime_max_s`; exactly one `ExecStartPre=` line and one `CLAUDE_CODE_DISABLE_AUTO_MEMORY` line; `crypto-run.timer` only when `fits=yes`.
- **O:** the stub's `usage` and `total_cost_usd` reach the third line; admission at `memory.max` + 64 MiB admits, and one byte less refuses.
- **P:** `answer_of` under R1.
- **Q:** `.claude/settings.json`.
- Totals: 17 sections, 181 checks. The checks added beyond the table are listed in D-4.

**B6 `vps/units/crypto-run.service`.** This is exactly §12.3's 37 lines. `diff` against the TZ's block printed nothing.

**B7 `.claude/settings.json`.** This is exactly §12.7's three lines.

**E1 `vps/manifest`.** Written by `printf 'crypto-run.path\n' >> vps/manifest` (D-9).

## Validation

Every `$ ` block below was captured by a helper that prints the literal command, runs it, and appends its output and `[exit N]`. Lines without `$ ` are UTC timestamps from `date -u`.

### A1 — §4a steps 1–6

```
2026-10-02T22:35:15Z
$ git fetch --all --prune
[exit 0]
$ git rev-parse --is-shallow-repository
false
[exit 0]
$ git rev-parse HEAD origin/main
4f512019c8513c3fc5b8b2b46d4dec0365037221
4f512019c8513c3fc5b8b2b46d4dec0365037221
[exit 0]
$ git log --oneline -3 -- "CryptoTZ/TZ-56*"
4f51201 Add files via upload
[exit 0]
$ git ls-tree origin/main CryptoTZ/ | grep -F TZ-56
100644 blob aa181e91b12558310592bdd26d4104477c49986d	CryptoTZ/TZ-56-run-lane-on-swap.md
[exit 0]
$ git status --porcelain | wc -l
0
[exit 0]
$ git log --oneline --graph --all | head -12
* 4f51201 Add files via upload
* dd6d0bb Update EXECUTOR-INSTRUCTIONS.md
* f58e342 Update SYSTEM-MAP-CRYPTOCALCUL.md
*   2aaa74f Merge pull request #44 from seahomebatumi-ai/tz-55-run-lane-own-user
|\  
| * 397ab81 TZ-55: vps — the run as its own user, test-mode memory, signed deploys
* | c5b8203 TZ-55: report — the run lane on the 1 GB host
* | 86ee107 journal: 2026-10-02 [skip ci]
* | 0066be9 analyst: live.json (vps)
* | 06d223f analyst: live.json (vps)
|/  
* 97376c9 Add files via upload
[exit 0]
$ git merge-base --is-ancestor 397ab81 origin/main && echo "397ab81 ancestor of origin/main"
397ab81 ancestor of origin/main
[exit 0]
$ curl -s https://api.github.com/repos/seahomebatumi-ai/crypto-auto/pulls/44 | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[\"state\"], d[\"merged\"], d[\"merge_commit_sha\"])"
closed True 2aaa74fa7866145aab54c8295032ac4625ebbe28
[exit 0]
```

The §5 gate's own output is under `## Fingerprints`.

### A2 — what TZ-55's merge put into effect

```
2026-10-02T22:35:34Z
$ journalctl -u crypto-deploy.service --since 2026-10-03 -o cat --no-pager | grep -E '^(deploy|install):'
[exit 1]
$ journalctl -u crypto-deploy.service --since '2026-10-02 20:00:00' -o cat --no-pager | grep -E '^(deploy|install):' | uniq -c
     19 deploy: vps tree 2b66e47f47b0e3fcd3f47805f808045c1b4cf9de already installed
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
      1 deploy: installed vps tree 43799ab742c8b4d67651cc3b07a0e6e31ee40e95
     11 deploy: vps tree 43799ab742c8b4d67651cc3b07a0e6e31ee40e95 already installed
[exit 0]
$ journalctl -u crypto-deploy.service --since 2026-10-02 -o short-iso --no-pager | grep -E 'deploy: installed|install: installed'
2026-10-02T06:02:35+00:00 vultr deploy.sh[3779563]: install: installed
2026-10-02T06:02:35+00:00 vultr deploy.sh[3779548]: deploy: installed vps tree 2b66e47f47b0e3fcd3f47805f808045c1b4cf9de
2026-10-02T21:38:16+00:00 vultr deploy.sh[3888125]: install: installed
2026-10-02T21:38:16+00:00 vultr deploy.sh[3888110]: deploy: installed vps tree 43799ab742c8b4d67651cc3b07a0e6e31ee40e95
[exit 0]
$ systemctl list-unit-files 'crypto-*' --no-pager
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
[exit 0]
$ systemctl is-active crypto-bot.service crypto-exchange.service
active
active
[exit 0]
$ cat /var/lib/crypto-auto/deployed-vps-tree; echo; git -C /srv/crypto-auto rev-parse origin/main:vps
43799ab742c8b4d67651cc3b07a0e6e31ee40e95
43799ab742c8b4d67651cc3b07a0e6e31ee40e95
[exit 0]
$ bash /usr/local/libexec/crypto-auto/deploy.sh --check
deploy: check commit=2aaa74fa7866145aab54c8295032ac4625ebbe28 signed=yes
[exit 0]
$ git -C /srv/crypto-auto log --first-parent -1 --format='%H %G? %GK' origin/main -- vps
2aaa74fa7866145aab54c8295032ac4625ebbe28 E B5690EEEBB952194
[exit 0]
$ GNUPGHOME=/etc/crypto-auto/gnupg git -C /srv/crypto-auto log --first-parent -1 --format='%H %G? %GK' origin/main -- vps
2aaa74fa7866145aab54c8295032ac4625ebbe28 U B5690EEEBB952194
[exit 0]
```

**Known answers.**
- The marker reads `43799ab742c8b4d67651cc3b07a0e6e31ee40e95`, the tree of `2aaa74f`. **Met.**
- The installed deployer prints `deploy: check commit=2aaa74fa7866145aab54c8295032ac4625ebbe28 signed=yes`. **Met.**
- `%G?` reads `E` (key unknown) against root's default keyring and `U` (good signature) against `/etc/crypto-auto/gnupg`, key `B5690EEEBB952194`.

The deployer installed the tree at 2026-10-02T21:38:16Z. The TZ's `--since 2026-10-03` is a Tbilisi date and, in UTC, read nothing (exit 1). The second command reads from Tbilisi midnight of 03.10, which is 2026-10-02T20:00Z (D-1). TZ-55's merge enabled the deploy and cleanup timers, the exchange watcher and the bot, and disabled the announce service, the run path and the run timer. It also logged `runs disabled`.

### A3 — tools

```
2026-10-02T22:35:43Z
$ systemctl --version | head -1
systemd 255 (255.4-1ubuntu8.17)
[exit 0]
$ ls -A /run/systemd/system.control/ 2>/dev/null
[exit 2]
$ ls -A /run/systemd/transient/ 2>/dev/null | grep -c . ; ls -A /run/systemd/transient/ 2>/dev/null | grep -c "^tz56-"
3
0
[exit 1]
```

`/run/systemd/system.control/` did not exist before this TZ (exit 2). `/run/systemd/transient/` held 3 entries, none named `tz56-`.

### A4 / V8 — the auto memory that existed

```
2026-10-02T22:35:53Z
$ bash /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/a4.sh
memory directories found: 7
kept (project name begins -root-crypto-auto or -var-lib-cryptorun-crypto-auto): 2
== /root/.claude/projects/-root-crypto-auto/memory  files=45
analyst-catalyst-primaries-found.md	size=1972	lines=27	mtime=2026-09-26T09:05:40Z
analyst-coverage-remeasure-recipe.md	size=1992	lines=25	mtime=2026-09-30T18:42:58Z
analyst-freeze-before-manual.md	size=2724	lines=33	mtime=2026-09-30T18:42:58Z
analyst-reachability-band-empty.md	size=1258	lines=22	mtime=2026-09-07T07:39:45Z
analyst-red-gate-fetch-first.md	size=1330	lines=24	mtime=2026-09-06T22:05:11Z
analyst-touch-pair-is-constant.md	size=1239	lines=24	mtime=2026-09-07T07:39:45Z
auto-mode-refuses-vps-run-lane.md	size=1497	lines=23	mtime=2026-10-02T10:57:44Z
bench-gate-halts-at-first-failure.md	size=1572	lines=29	mtime=2026-09-08T14:39:43Z
bench-runs-must-be-serial.md	size=1842	lines=33	mtime=2026-09-09T21:14:31Z
bench-scratch-copy-gotchas.md	size=2186	lines=35	mtime=2026-09-17T07:50:24Z
bench-step5-ooms-in-session.md	size=1740	lines=30	mtime=2026-09-09T14:26:27Z
blocked-prototype-seeds-next-tz.md	size=1587	lines=29	mtime=2026-09-13T22:18:36Z
dispatch-artifacts-verify-derivation-rows.md	size=1791	lines=32	mtime=2026-09-22T08:22:49Z
gh-absent-read-ci-via-rest-api.md	size=5277	lines=87	mtime=2026-10-01T08:20:32Z
guard-check33-pins-driver-keys.md	size=1825	lines=32	mtime=2026-09-17T01:12:49Z
journal-bench-step7-attribution.md	size=1507	lines=25	mtime=2026-09-08T07:47:38Z
known-answer-world-probe-with-cut-code.md	size=2287	lines=39	mtime=2026-09-16T12:21:46Z
lab-selftest-d4-red-since-tz33.md	size=2351	lines=34	mtime=2026-09-09T14:26:27Z
map-reserved-tz-is-not-a-spec.md	size=1860	lines=26	mtime=2026-09-09T09:40:19Z
MEMORY.md	size=7858	lines=44	mtime=2026-10-02T21:15:09Z
negative-control-layered-repair-masks-revert.md	size=1731	lines=29	mtime=2026-09-11T23:14:41Z
probe-flag-scan-is-tool-blind.md	size=1602	lines=15	mtime=2026-09-16T10:09:17Z
probe-keep-bodies-reclassify-offline.md	size=1423	lines=21	mtime=2026-09-15T22:49:30Z
regime-gate-json-dump-crash.md	size=2807	lines=44	mtime=2026-09-17T13:16:35Z
report-evidence-blocks-literal.md	size=2062	lines=32	mtime=2026-10-01T08:20:32Z
transient-unit-gc-memory-peak.md	size=1485	lines=24	mtime=2026-10-01T19:12:27Z
tz38-selftests-need-explicit-paths.md	size=1494	lines=29	mtime=2026-09-09T21:14:31Z
tz47-own-regime-blocked.md	size=2167	lines=41	mtime=2026-09-17T01:13:10Z
tz48-own-regime-gate-completed.md	size=2646	lines=42	mtime=2026-09-17T07:50:41Z
tz49-raw-json-blocked.md	size=2597	lines=41	mtime=2026-09-17T13:16:35Z
tz50-agree-map-completed.md	size=2424	lines=40	mtime=2026-09-17T13:16:23Z
tz51-instant-read-completed.md	size=2273	lines=39	mtime=2026-09-25T11:42:49Z
tz52-catalyst-lanes-completed.md	size=2327	lines=36	mtime=2026-09-25T11:42:59Z
tz53-vps-reading-completed.md	size=2717	lines=39	mtime=2026-10-01T08:20:25Z
tz54-paused-on-classifier-denials.md	size=1347	lines=24	mtime=2026-10-02T10:57:38Z
tz55-run-lane-partial.md	size=1661	lines=25	mtime=2026-10-02T21:14:51Z
tz-fixture-table-beats-key-gloss.md	size=2706	lines=43	mtime=2026-09-13T12:04:16Z
tz-header-anchor-subset-not-a-block.md	size=1153	lines=15	mtime=2026-09-15T22:49:25Z
tz-hunk-count-needs-u0.md	size=1090	lines=22	mtime=2026-09-13T09:11:53Z
tz-removed-key-breaks-existing-assertion.md	size=4003	lines=58	mtime=2026-09-17T07:50:41Z
tz-replaced-in-place-on-remote.md	size=2550	lines=40	mtime=2026-09-08T14:39:43Z
tz-sequencing-clause-blocks-on-unmerged.md	size=2005	lines=31	mtime=2026-09-11T23:39:42Z
unlock-lane-misses-announced-releases.md	size=1293	lines=19	mtime=2026-09-30T18:42:58Z
vps-run-lane-measurement-gotchas.md	size=1558	lines=23	mtime=2026-10-02T21:14:57Z
write-tool-decodes-unicode-escapes.md	size=1155	lines=21	mtime=2026-10-01T19:12:31Z
== /var/lib/cryptorun/.claude/projects/-var-lib-cryptorun-crypto-auto/memory  files=0
[exit 0]
```

The script prints names, sizes, `wc -l` counts and modification times, and nothing else. It reads every file only through `stat` and `wc -l`, and no file's text entered the session. Five more `memory` directories exist under other projects' directories. Only their count was printed.

### A5 — the stream, read before the program changes

The staging copy is `main`'s `vps/`, made before Stage B:

```
2026-10-02T22:36:36Z
$ ls -d /var/tmp/tz56-vps /var/tmp/tz56-state /var/tmp/tz56-sig
ls: cannot access '/var/tmp/tz56-vps': No such file or directory
ls: cannot access '/var/tmp/tz56-state': No such file or directory
ls: cannot access '/var/tmp/tz56-sig': No such file or directory
[exit 2]
$ git rev-parse HEAD; git status --porcelain | wc -l
4f512019c8513c3fc5b8b2b46d4dec0365037221
0
[exit 0]
$ install -d -m 0755 -o root -g root /var/tmp/tz56-vps /var/tmp/tz56-state && git archive origin/main vps | tar -x --strip-components=1 -C /var/tmp/tz56-vps && chown -R root:root /var/tmp/tz56-vps && chmod 0755 /var/tmp/tz56-vps
[exit 0]
$ diff -r vps /var/tmp/tz56-vps && echo identical
identical
[exit 0]
$ install -m 0644 -o root -g root /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/subscribe-read.py /var/tmp/tz56-state/subscribe-read.py
[exit 0]
$ stat --format="%a %U:%G %n" /var/tmp/tz56-vps /var/tmp/tz56-state /var/tmp/tz56-state/subscribe-read.py
755 root:root /var/tmp/tz56-vps
755 root:root /var/tmp/tz56-state
644 root:root /var/tmp/tz56-state/subscribe-read.py
[exit 0]
$ grep -c . /etc/crypto-auto/credentials/binance-api-key /etc/crypto-auto/credentials/binance-api-secret
/etc/crypto-auto/credentials/binance-api-key:1
/etc/crypto-auto/credentials/binance-api-secret:1
[exit 0]
```

`subscribe-read.py` imports `/var/tmp/tz56-vps/announce.py` and `common.py` for `signed_query`, `STREAM_URL`, `TOPIC`, `SUBSCRIBE` and `load_credential`. It opens each connection exactly as `Stream.connect()` did: the signed query with `random`, `recvWindow=60000`, `timestamp` and `topic`; the `X-MBX-APIKEY` header; a 20 s timeout. It reads each connection for 20 s. It also reports control frames (none arrived) and prints one `open` and one `end` line per connection, with no frame content (D-7).

```
2026-10-02T22:36:43Z
$ systemd-run --unit=tz56-subscribe -p MemoryAccounting=yes -p RuntimeMaxSec=120 -p RemainAfterExit=yes -p LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key -p LoadCredential=binance-api-secret:/etc/crypto-auto/credentials/binance-api-secret /usr/bin/python3 /var/tmp/tz56-state/subscribe-read.py
Running as unit: tz56-subscribe.service; invocation ID: 87fabffc198045ada4e7434faf8331ba
[exit 0]
2026-10-02T22:37:42Z
$ systemctl show tz56-subscribe -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic
Result=success
ExecMainStartTimestampMonotonic=5325131534092
ExecMainExitTimestampMonotonic=5325179799328
ExecMainStatus=0
[exit 0]
$ journalctl -u tz56-subscribe -o cat --no-pager
Started tz56-subscribe.service - /usr/bin/python3 /var/tmp/tz56-state/subscribe-read.py.
conn=1 open sent_subscribe=no
conn=1 n=1 t_ms=22 type=COMMAND subType=REGISTER data=SUCCESS code=00000000
conn=1 end=timeout frames=1 read_ms=20266
gap_ms=6003
conn=2 open sent_subscribe=yes
conn=2 n=1 t_ms=7 type=COMMAND subType=REGISTER data=SUCCESS code=00000000
conn=2 n=2 t_ms=246 type=COMMAND subType=SUBSCRIBE data=SUCCESS code=00000000
conn=2 end=timeout frames=2 read_ms=20251
[exit 0]
$ systemctl stop tz56-subscribe; systemctl list-units --all "tz56-*" --no-legend | wc -l
0
[exit 0]
```

**Outcome R1.** Connection 1 sent no command and received `COMMAND` `REGISTER` / `SUCCESS` at 22 ms. Connection 2, opened 6 003 ms after connection 1 closed, sent `SUBSCRIBE` and received `REGISTER` / `SUCCESS` at 7 ms, then `SUBSCRIBE` / `SUCCESS` at 246 ms. No connection received a data frame. Under the registered outcomes, R1 holds and R2 does not, because connection 1 received a `COMMAND` frame. B3 took branch R1.

### C — the limits, proved on the VPS

The staging copy was refreshed from the branch's `vps/` after Stage B:

```
2026-10-02T22:43:12Z
$ ls -A /var/tmp/tz56-vps | tr "\n" " "; echo
announce.py bot.py cleanup.py common.py deploy.sh exchange.py install.sh manifest memory-record.txt __pycache__ run.py selftest.py units writer.py 
[exit 0]
$ rm -r /var/tmp/tz56-vps/__pycache__; git ls-files -z vps | xargs -0 tar -c | tar -x --strip-components=1 -C /var/tmp/tz56-vps && chown -R root:root /var/tmp/tz56-vps && chmod 0755 /var/tmp/tz56-vps
[exit 0]
$ diff -r --exclude=__pycache__ vps /var/tmp/tz56-vps && echo identical; ls -A /var/tmp/tz56-vps | tr "\n" " "; echo
identical
announce.py bot.py cleanup.py common.py deploy.sh exchange.py install.sh manifest memory-record.txt run.py selftest.py units writer.py 
[exit 0]
$ install -m 0644 -o root -g root /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/limits-read.py /var/tmp/tz56-state/limits-read.py && stat --format='%a %U:%G %n' /var/tmp/tz56-vps /var/tmp/tz56-state /var/tmp/tz56-state/limits-read.py
755 root:root /var/tmp/tz56-vps
755 root:root /var/tmp/tz56-state
644 root:root /var/tmp/tz56-state/limits-read.py
[exit 0]
$ git status --porcelain; git rev-parse HEAD
 M vps/announce.py
 M vps/common.py
 M vps/deploy.sh
 M vps/run.py
 M vps/selftest.py
 M vps/units/crypto-run.service
?? .claude/
4f512019c8513c3fc5b8b2b46d4dec0365037221
[exit 0]
```

**C1:**

```
2026-10-02T22:43:19Z
$ grep -E '^(MemAvailable|SwapFree):' /proc/meminfo
MemAvailable:     212728 kB
SwapFree:        2445568 kB
[exit 0]
$ systemd-run --unit=tz56-limits -p User=cryptorun -p Group=cryptorun -p SupplementaryGroups=cryptoauto -p MemoryAccounting=yes -p MemoryMax=167772160 -p MemorySwapMax=536870912 -p RemainAfterExit=yes -p 'ExecStartPre=-+/usr/bin/python3 /var/tmp/tz56-vps/run.py --limits' /usr/bin/python3 /var/tmp/tz56-state/limits-read.py
Running as unit: tz56-limits.service; invocation ID: 0d4488f7b5a3490b9f87cc2383eb894e
[exit 0]
2026-10-02T22:43:26Z
$ journalctl -u tz56-limits -o cat --no-pager
Starting tz56-limits.service - /usr/bin/python3 /var/tmp/tz56-state/limits-read.py...
crypto-run: limits unit=tz56-limits.service mem_available=218202112 swap_free=2504261632 budget=704643072 memory_max=167772160 memory_swap_max=536870912 set=0
Started tz56-limits.service - /usr/bin/python3 /var/tmp/tz56-state/limits-read.py.
uid=995 memory.max=167772160 memory.swap.max=536870912
[exit 0]
$ systemctl show tz56-limits -p MemoryMax -p MemorySwapMax -p Result -p ExecMainStatus
Result=success
ExecMainStatus=0
MemoryMax=167772160
MemorySwapMax=536870912
[exit 0]
$ ls -AR /run/systemd/system.control/ 2>/dev/null; ls -A /run/systemd/transient/ | grep "^tz56-"; ls -A /run/systemd/transient/tz56-limits.service.d/ 2>/dev/null
tz56-limits.service
tz56-limits.service.d
50-MemoryMax.conf
50-MemorySwapMax.conf
[exit 0]
$ cat /run/systemd/transient/tz56-limits.service.d/*.conf 2>/dev/null
# This is a drop-in unit file extension, created via "systemctl set-property"
# or an equivalent operation. Do not edit.
[Service]
MemoryMax=167772160
# This is a drop-in unit file extension, created via "systemctl set-property"
# or an equivalent operation. Do not edit.
[Service]
MemorySwapMax=536870912
[exit 0]
2026-10-02T22:43:43Z
$ python3 -B -c 'import sys; sys.path.insert(0, "vps"); import common; m = common.start_limits(218202112, 704643072); print("start_limits(218202112, 704643072) =", m, "sum =", sum(m), "line memory_max == m[0]:", m[0] == 167772160)'
start_limits(218202112, 704643072) = (167772160, 536870912) sum = 704643072 line memory_max == m[0]: True
[exit 0]
$ systemctl stop tz56-limits; systemctl list-units --all "tz56-*" --no-legend | wc -l; ls -A /run/systemd/transient/ | grep -c "^tz56-"; ls -A /run/systemd/system.control/ 2>/dev/null | grep -c "^tz56-"
0
0
0
[exit 1]
```

| Known answer | Read | |
|---|---|---|
| the line names `unit=tz56-limits.service` | `unit=tz56-limits.service` | met |
| `set=0` | `set=0` | met |
| main process `memory.max` = line's `memory_max` | 167772160 = 167772160 | met |
| main process `memory.swap.max` = line's `memory_swap_max` | 536870912 = 536870912 | met |
| sum = `budget_bytes` 704 643 072 | 704 643 072 | met |
| `memory_max` = `start_limits(218202112, 704643072)[0]`, recomputed in the session | 167 772 160 | met |
| `uid` not 0 | 995 | met |

`systemd-run` accepted `ExecStartPre=-+…` as a transient property. `set-property --runtime` on a transient unit wrote `50-MemoryMax.conf` and `50-MemorySwapMax.conf` under `/run/systemd/transient/tz56-limits.service.d/`, not under `system.control/`. Stopping the unit removed both. `MemAvailable` was 218 202 112 at the instant of the start, so the computed pair was the floor pair, which is also the pair the probe started with. **C1 therefore could not tell a start that set the pair from one that set nothing.** C1b was added for that (D-3):

```
2026-10-02T22:43:51Z
$ systemd-run --unit=tz56-limits2 -p User=cryptorun -p Group=cryptorun -p SupplementaryGroups=cryptoauto -p MemoryAccounting=yes -p MemoryMax=134217728 -p MemorySwapMax=570425344 -p RemainAfterExit=yes -p 'ExecStartPre=-+/usr/bin/python3 /var/tmp/tz56-vps/run.py --limits' /usr/bin/python3 /var/tmp/tz56-state/limits-read.py
Running as unit: tz56-limits2.service; invocation ID: 7b4006f97d204908874264491799e4d8
[exit 0]
$ journalctl -u tz56-limits2 -o cat --no-pager
Starting tz56-limits2.service - /usr/bin/python3 /var/tmp/tz56-state/limits-read.py...
crypto-run: limits unit=tz56-limits2.service mem_available=246325248 swap_free=2489057280 budget=704643072 memory_max=167772160 memory_swap_max=536870912 set=0
Started tz56-limits2.service - /usr/bin/python3 /var/tmp/tz56-state/limits-read.py.
uid=995 memory.max=167772160 memory.swap.max=536870912
[exit 0]
$ systemctl show tz56-limits2 -p MemoryMax -p MemorySwapMax -p Result -p ExecMainStatus
Result=success
ExecMainStatus=0
MemoryMax=167772160
MemorySwapMax=536870912
[exit 0]
$ systemctl stop tz56-limits2; systemctl list-units --all "tz56-*" --no-legend | wc -l; ls -A /run/systemd/transient/ | grep -c "^tz56-"
0
0
[exit 1]
```

C1b started at 134 217 728 / 570 425 344. The main process read 167 772 160 / 536 870 912, which is `start_limits(246325248, 704643072)`. The new pair is in force before `ExecStart`.

### D3 — the stream, on the branch's code

The one-second sampler is TZ-55's file, byte for byte (D-7):

```
2026-10-02T22:44:10Z
$ install -m 0644 -o root -g root /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/sampler.py /var/tmp/tz56-state/sampler.py && md5sum /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-018cXeqyU9ehURcKzCAJk2k3/fbeebc8b-3806-4ac4-af11-25da41663224/scratchpad/sampler.py /var/tmp/tz56-state/sampler.py
c85b4096bb5561fc36cb981e35771fb6  /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-018cXeqyU9ehURcKzCAJk2k3/fbeebc8b-3806-4ac4-af11-25da41663224/scratchpad/sampler.py
c85b4096bb5561fc36cb981e35771fb6  /var/tmp/tz56-state/sampler.py
[exit 0]
$ diff -r --exclude=__pycache__ vps /var/tmp/tz56-vps && echo identical
identical
[exit 0]
2026-10-02T22:44:10Z
$ systemd-run --unit=tz56-sample-announce -p MemoryAccounting=yes /usr/bin/python3 /var/tmp/tz56-state/sampler.py tz56-announce /var/tmp/tz56-state/sample-announce.jsonl 1 120
Running as unit: tz56-sample-announce.service; invocation ID: e03a36921ac14145a76274f4afe69f83
[exit 0]
2026-10-02T22:44:10Z
$ systemd-run --unit=tz56-announce -p MemoryAccounting=yes -p RuntimeMaxSec=11100 -p LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key -p LoadCredential=binance-api-secret:/etc/crypto-auto/credentials/binance-api-secret -p RemainAfterExit=yes /usr/bin/python3 /var/tmp/tz56-vps/announce.py --measure 10800 2 --state-dir /var/tmp/tz56-state
Running as unit: tz56-announce.service; invocation ID: f4b9016bc4ee41128463e3468b400144
[exit 0]
```

Collected last:

```
2026-10-03T03:44:07Z
$ systemctl show tz56-announce -p Result -p ExecMainStatus -p ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p MemorySwapPeak
Result=exit-code
ExecMainStartTimestampMonotonic=5325578642056
ExecMainExitTimestampMonotonic=5336380828604
ExecMainStatus=2
MemoryPeak=19009536
MemorySwapPeak=14077952
[exit 0]
$ journalctl -u tz56-announce -o cat --no-pager
Started tz56-announce.service - /usr/bin/python3 /var/tmp/tz56-vps/announce.py --measure 10800 2 --state-dir /var/tmp/tz56-state.
announce: key ACCEPTED ipRestrict=true enableReading=true enableFutures=false enableSpotAndMarginTrading=false enableWithdrawals=false enableInternalTransfer=false permitsUniversalTransfer=false enableVanillaOptions=false enablePortfolioMarginTrading=false enableFixApiTrade=false enableFixReadOnly=false enableMargin=false
announce: subscribe answer {"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}
announce: data_messages=0 complete=0 pings=356 reconnects=0 close_codes=-
tz56-announce.service: Main process exited, code=exited, status=2/INVALIDARGUMENT
tz56-announce.service: Failed with result 'exit-code'.
tz56-announce.service: Consumed 1.408s CPU time, 18.1M memory peak, 13.4M memory swap peak.
[exit 0]
$ systemctl is-active tz56-sample-announce; cat /var/tmp/tz56-state/sample-announce.jsonl.summary.json
inactive
{"unit": "tz56-announce", "samples": 10801, "span_s": 10801.2, "first_t": 1790981050.956, "last_t": 1790991852.146, "F_run": 17772544, "P_peak": 33087488, "F": 33087488, "memory_peak_last_read": 19009536, "memory_swap_peak_last_read": 14077952, "max_current": 17772544, "max_swap_current": 14077952, "min_MemAvailable": 134758400, "min_SwapFree": 2455838720}
[exit 0]
$ wc -l /var/tmp/tz56-state/sample-announce.jsonl; ls -A /var/tmp/tz56-state
10801 /var/tmp/tz56-state/sample-announce.jsonl
gnupg
limits-read.py
sample-announce.jsonl
sample-announce.jsonl.summary.json
sampler.py
subscribe-read.py
[exit 0]
$ echo $(( (5336380828604 - 5325578642056) / 1000 )) ms main process
10802186 ms main process
[exit 0]
$ systemctl reset-failed tz56-announce; systemctl list-units --all "tz56-*" --no-legend | wc -l
0
[exit 0]
$ wc -c < /var/tmp/tz56-state/announcements.jsonl 2>/dev/null || echo "announcements.jsonl absent"
bash: line 1: /var/tmp/tz56-state/announcements.jsonl: No such file or directory
announcements.jsonl absent
[exit 0]
```

- **Key verdict:** `ACCEPTED`, with `ipRestrict=true`, `enableReading=true`, and every other `enable*`/`permits*` field `false`.
- **Subscribe answer:** `{"code": "00000000", "data": "SUCCESS", "subType": "REGISTER", "type": "COMMAND"}`.
- **`command answer` lines:** none, because no `COMMAND` frame of another `subType` arrived before the answer.
- **Data messages:** 0, so there is no `catalogName`, title, publish time, lag or match to print. No `announcements.jsonl` was written.
- **Pings:** 356. **Reconnects:** 0. **Close codes:** none.
- **Exit:** 2, after 10 802 186 ms of main process.
- **Memory:** the unit was `failed`, so systemd kept it loaded and `MemoryPeak=19009536` / `MemorySwapPeak=14077952` were readable. The sampler's 10 801 samples give `F` = 33 087 488.

### E1 — `vps/manifest`

```
2026-10-03T03:44:29Z
$ cat vps/manifest
crypto-deploy.timer
crypto-cleanup.timer
crypto-exchange.service
crypto-bot.service
crypto-run.path
[exit 0]
$ git diff vps/manifest
diff --git a/vps/manifest b/vps/manifest
index dd75b9f..dba0aff 100644
--- a/vps/manifest
+++ b/vps/manifest
@@ -2,3 +2,4 @@ crypto-deploy.timer
 crypto-cleanup.timer
 crypto-exchange.service
 crypto-bot.service
+crypto-run.path
[exit 0]
```

- `crypto-run.path` is listed because C1 met every known answer.
- `crypto-announce.service` is not listed because D3 exited 2.
- `crypto-run.timer` is not listed (§5).

### V1 — selftest, after Stage E, with its negative control

```
2026-10-03T03:44:39Z
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
section J: checks 21 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 13 failed 0
section N: checks 10 failed 0
section O: checks 24 failed 0
section P: checks 11 failed 0
section Q: checks 3 failed 0
selftest: sections 17 checks 181 failed 0 empty 0
[exit 0]
$ md5sum vps/selftest.py
4b09818d510f0dfa97d795f2d6512f2b  vps/selftest.py
[exit 0]
$ grep -n 'common.start_limits(535355392, 704643072) == (452984832, 251658240)' vps/selftest.py
299:    s.check("start_limits(535355392, 704643072)", common.start_limits(535355392, 704643072) == (452984832, 251658240))
[exit 0]
$ sed -i 's/common.start_limits(535355392, 704643072) == (452984832, 251658240)/common.start_limits(535355392, 704643072) == (452984833, 251658240)/' vps/selftest.py && git diff -U0 vps/selftest.py | grep '^[-+] .*start_limits(535355392'
+    s.check("start_limits(535355392, 704643072)", common.start_limits(535355392, 704643072) == (452984833, 251658240))
[exit 0]
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
FAIL section J: start_limits(535355392, 704643072)
section J: checks 21 failed 1
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 13 failed 0
section N: checks 10 failed 0
section O: checks 24 failed 0
section P: checks 11 failed 0
section Q: checks 3 failed 0
selftest: sections 17 checks 181 failed 1 empty 0
[exit 1]
$ sed -i 's/common.start_limits(535355392, 704643072) == (452984833, 251658240)/common.start_limits(535355392, 704643072) == (452984832, 251658240)/' vps/selftest.py && md5sum vps/selftest.py
4b09818d510f0dfa97d795f2d6512f2b  vps/selftest.py
[exit 0]
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
section J: checks 21 failed 0
section K: checks 2 failed 0
section L: checks 4 failed 0
section M: checks 13 failed 0
section N: checks 10 failed 0
section O: checks 24 failed 0
section P: checks 11 failed 0
section Q: checks 3 failed 0
selftest: sections 17 checks 181 failed 0 empty 0
[exit 0]
```

The run is green: 17 sections, 181 checks, none empty. With one digit of a §12.2 known answer changed, the selftest exits 1 and section J alone fails. After the revert it is green again, and the MD5 is `4b09818d510f0dfa97d795f2d6512f2b` both before and after.

### V2 — syntax

```
2026-10-02T22:45:40Z
$ for f in vps/*.py; do python3 -m py_compile "$f" && echo "py_compile $f ok"; done
py_compile vps/announce.py ok
py_compile vps/bot.py ok
py_compile vps/cleanup.py ok
py_compile vps/common.py ok
py_compile vps/exchange.py ok
py_compile vps/run.py ok
py_compile vps/selftest.py ok
py_compile vps/writer.py ok
[exit 0]
$ bash -n vps/deploy.sh && echo "bash -n vps/deploy.sh ok"; bash -n vps/install.sh && echo "bash -n vps/install.sh ok"
bash -n vps/deploy.sh ok
bash -n vps/install.sh ok
[exit 0]
$ systemd-analyze verify vps/units/*
[exit 0]
$ python3 -m json.tool .claude/settings.json
{
    "autoMemoryEnabled": false
}
[exit 0]
```

`systemd-analyze verify` printed no warning for any of the 10 unit files.

### V3 — dry run

```
2026-10-03T03:44:48Z
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
install: would install /etc/systemd/system/crypto-run.timer (0644)
install: would enable --now crypto-deploy.timer
install: would enable --now crypto-cleanup.timer
install: would enable --now crypto-exchange.service
install: would enable --now crypto-bot.service
install: would enable --now crypto-run.path
install: would disable --now crypto-announce.service
install: would disable --now crypto-run.timer
install: would restart crypto-exchange.service
install: would restart crypto-bot.service
install: would copy vps/deploy.sh to /usr/local/libexec/crypto-auto/deploy.sh
install: would create /var/lib/crypto-auto/runs-enabled
[exit 0]
$ bash vps/install.sh --dry-run | grep -c -x -F 'install: would enable --now crypto-run.path'; bash vps/install.sh --dry-run | grep -c -x -F 'install: would create /var/lib/crypto-auto/runs-enabled'; bash vps/install.sh --dry-run | grep -c -F 'would enable --now crypto-run.timer'
1
1
0
[exit 1]
$ diff /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/v/unitfiles-before-v3.txt /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/v/unitfiles-after-v3.txt && echo 'list-unit-files identical before and after'; diff /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/v/unitfiles-after-v3.txt <(sed -n '/^$ systemctl list-unit-files/,/unit files listed/p' /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/a/a2.txt | sed 1d) && echo 'identical to A2'
list-unit-files identical before and after
identical to A2
[exit 0]
```

- `would enable --now crypto-run.path` was printed once.
- `would create /var/lib/crypto-auto/runs-enabled` was printed once.
- `would enable --now crypto-run.timer` was printed 0 times; the count's `[exit 1]` is `grep -c` finding none.
- `list-unit-files` read the same before and after, and the same as in A2.

### V4 — the limits

C1's journal and `systemctl show` lines are above, against every C1 known answer: all met.

### V5 — the stream

A5's frames and D3's output are both above.

### V6 — signed deploys

```
2026-10-02T22:45:06Z
$ bash vps/deploy.sh --check
deploy: check base=4f512019c8513c3fc5b8b2b46d4dec0365037221 commits=0 unsigned=0 signed=yes
[exit 0]
$ git -C /srv/crypto-auto rev-parse HEAD origin/main
4f512019c8513c3fc5b8b2b46d4dec0365037221
4f512019c8513c3fc5b8b2b46d4dec0365037221
[exit 0]
$ base=$(git -C /srv/crypto-auto rev-parse HEAD); GNUPGHOME=/etc/crypto-auto/gnupg git -C /srv/crypto-auto log --first-parent --format='%H %G? %GK' "$base..origin/main" -- vps | wc -l
0
[exit 0]
$ GNUPGHOME=/etc/crypto-auto/gnupg git -C /srv/crypto-auto log --first-parent --format='%h %G? %GK %s' 2aaa74f..origin/main
4f51201 U B5690EEEBB952194 Add files via upload
dd6d0bb U B5690EEEBB952194 Update EXECUTOR-INSTRUCTIONS.md
f58e342 U B5690EEEBB952194 Update SYSTEM-MAP-CRYPTOCALCUL.md
[exit 0]
2026-10-02T22:45:15Z
$ git clone -q /srv/crypto-auto /var/tmp/tz56-sig && git -C /var/tmp/tz56-sig rev-parse HEAD refs/remotes/origin/main
4f512019c8513c3fc5b8b2b46d4dec0365037221
4f512019c8513c3fc5b8b2b46d4dec0365037221
[exit 0]
$ cp -r /etc/crypto-auto/gnupg /var/tmp/tz56-state/gnupg && chmod 0700 /var/tmp/tz56-state/gnupg && ls -A /var/tmp/tz56-state/gnupg | tr "\n" " "; echo
private-keys-v1.d pubring.kbx pubring.kbx~ trustdb.gpg 
[exit 0]
$ GNUPGHOME=/var/tmp/tz56-state/gnupg gpg --batch --passphrase '' --quick-gen-key 'tz56 <tz56@invalid>' ed25519 sign never
gpg: directory '/var/tmp/tz56-state/gnupg/openpgp-revocs.d' created
gpg: revocation certificate stored as '/var/tmp/tz56-state/gnupg/openpgp-revocs.d/1AD4DD7AE148ED06CB74B84D23AB290C6A6D7BFC.rev'
[exit 0]
$ GNUPGHOME=/var/tmp/tz56-state/gnupg gpg --list-keys --with-colons 2>/dev/null | grep -E '^(pub|uid)' | cut -d: -f1,2,5,10
pub:e:4AEE18F83AFDEB23:
uid:e::GitHub (web-flow commit signing) <noreply@github.com>
pub:-:B5690EEEBB952194:
uid:-::GitHub <noreply@github.com>
pub:u:23AB290C6A6D7BFC:
uid:u::tz56 <tz56@invalid>
[exit 0]
2026-10-02T22:45:22Z
$ B=$(git -C /var/tmp/tz56-sig rev-parse HEAD); echo B=$B; echo one > /var/tmp/tz56-sig/vps/tz56-probe.txt && git -C /var/tmp/tz56-sig -c user.name=tz56 -c user.email=tz56@invalid add vps/tz56-probe.txt && git -C /var/tmp/tz56-sig -c user.name=tz56 -c user.email=tz56@invalid commit -q -m 'tz56: X, unsigned' && echo X=$(git -C /var/tmp/tz56-sig rev-parse HEAD)
B=4f512019c8513c3fc5b8b2b46d4dec0365037221
X=0cd025a08cbeec895e192b8264b22b31b8862048
[exit 0]
$ echo two > /var/tmp/tz56-sig/vps/tz56-probe.txt && GNUPGHOME=/var/tmp/tz56-state/gnupg git -C /var/tmp/tz56-sig -c user.name=tz56 -c user.email=tz56@invalid -c user.signingkey=23AB290C6A6D7BFC commit -q -S -a -m 'tz56: M, signed with the throwaway key' && echo M=$(git -C /var/tmp/tz56-sig rev-parse HEAD)
M=b9bb5912022f28a46ea12280405ff76ab0d52930
[exit 0]
$ GNUPGHOME=/var/tmp/tz56-state/gnupg git -C /var/tmp/tz56-sig log --format='%H %G? %GK %s' -3
b9bb5912022f28a46ea12280405ff76ab0d52930 G 23AB290C6A6D7BFC tz56: M, signed with the throwaway key
0cd025a08cbeec895e192b8264b22b31b8862048 N  tz56: X, unsigned
4f512019c8513c3fc5b8b2b46d4dec0365037221 U B5690EEEBB952194 Add files via upload
[exit 0]
2026-10-02T22:45:30Z
$ git -C /var/tmp/tz56-sig update-ref refs/remotes/origin/main b9bb5912022f28a46ea12280405ff76ab0d52930 && git -C /var/tmp/tz56-sig checkout -q --detach 4f512019c8513c3fc5b8b2b46d4dec0365037221 && git -C /var/tmp/tz56-sig rev-parse HEAD refs/remotes/origin/main
4f512019c8513c3fc5b8b2b46d4dec0365037221
b9bb5912022f28a46ea12280405ff76ab0d52930
[exit 0]
$ bash vps/deploy.sh --check /var/tmp/tz56-sig /var/tmp/tz56-state/gnupg
deploy: check base=4f512019c8513c3fc5b8b2b46d4dec0365037221 commits=2 unsigned=1 signed=no
[exit 1]
$ GNUPGHOME=/var/tmp/tz56-state/gnupg git -C /var/tmp/tz56-sig verify-commit b9bb5912022f28a46ea12280405ff76ab0d52930
gpg: Signature made Fri 02 Oct 2026 10:45:22 PM UTC
gpg:                using EDDSA key 1AD4DD7AE148ED06CB74B84D23AB290C6A6D7BFC
gpg: Good signature from "tz56 <tz56@invalid>" [ultimate]
[exit 0]
$ git -C /var/tmp/tz56-sig checkout -q --detach 0cd025a08cbeec895e192b8264b22b31b8862048 && git -C /var/tmp/tz56-sig rev-parse HEAD
0cd025a08cbeec895e192b8264b22b31b8862048
[exit 0]
$ bash vps/deploy.sh --check /var/tmp/tz56-sig /var/tmp/tz56-state/gnupg
deploy: check base=0cd025a08cbeec895e192b8264b22b31b8862048 commits=1 unsigned=0 signed=yes
[exit 0]
$ cmp /usr/local/libexec/crypto-auto/deploy.sh <(git -C /srv/crypto-auto show origin/main:vps/deploy.sh) && echo identical
identical
[exit 0]
```

1. **The deployer's clone.** `bash vps/deploy.sh --check` from the branch printed `commits=0 unsigned=0 signed=yes` and exited 0. No first-parent commit after `2aaa74f` changed `vps/`. The three after it (`f58e342`, `dd6d0bb`, `4f51201`) are Boss uploads that carry `U B5690EEEBB952194`.
2. **The chain the old rule passed.** From `B` (`4f51201`), the check printed `commits=2 unsigned=1 signed=no` and exited 1. `verify-commit M` exited 0: the newest commit alone, which is what TZ-55's rule read, verifies. From `X` it printed `commits=1 unsigned=0 signed=yes` and exited 0. These are the answers derived from §12.5.
3. **The installed deployer.** `cmp` reports it identical to `origin/main:vps/deploy.sh`, so this session installed no deployer.

### V7 — credentials

The exact-value scan was run on this report's final text, on the branch, before the report was committed:

```
$ bash /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/v7-scan.sh CryptoReports/TZ-56-run-lane-on-swap-report.md
binance-api-key: lines=1 non_empty_lines=1
binance-api-secret: lines=1 non_empty_lines=1
claude-oauth-token: lines=1 non_empty_lines=1
branch: tz-56-run-lane-on-swap 16ca733; diff origin/main...HEAD lines: 796
files scanned under vps/ and .claude/: 23
journal lines tz56-*: 34
binance-api-key: report=0 branch_diff=0 vps_and_claude_files=0 journal_tz56=0
binance-api-secret: report=0 branch_diff=0 vps_and_claude_files=0 journal_tz56=0
claude-oauth-token: report=0 branch_diff=0 vps_and_claude_files=0 journal_tz56=0
[exit 0]
```

Each credential file holds one line, and that line is non-empty. Every count is 0. The pattern file is the credential file itself (`grep -F -f`), so no copy of any value was written anywhere.

### V9 — nothing left

```
2026-10-03T03:45:58Z
$ gpgconf --homedir /var/tmp/tz56-state/gnupg --kill all; pgrep -a -f "gpg-agent.*tz56" | grep -v pgrep | wc -l
0
[exit 0]
$ rm -r /var/tmp/tz56-vps /var/tmp/tz56-state /var/tmp/tz56-sig; ls -d /var/tmp/tz56-vps /var/tmp/tz56-state /var/tmp/tz56-sig
ls: cannot access '/var/tmp/tz56-vps': No such file or directory
ls: cannot access '/var/tmp/tz56-state': No such file or directory
ls: cannot access '/var/tmp/tz56-sig': No such file or directory
[exit 2]
$ d=$(gpgconf --homedir /var/tmp/tz56-state/gnupg --list-dirs socketdir); echo "socketdir=$d"; ls -A "$d" 2>&1
socketdir=/run/user/0/gnupg/d.n81y3hxf3nnudts5fuu7akih
[exit 0]
$ rmdir /run/user/0/gnupg/d.n81y3hxf3nnudts5fuu7akih && ls -d /run/user/0/gnupg/d.n81y3hxf3nnudts5fuu7akih
ls: cannot access '/run/user/0/gnupg/d.n81y3hxf3nnudts5fuu7akih': No such file or directory
[exit 2]
2026-10-03T03:46:14Z
$ systemctl list-units --all "tz56-*" --no-legend --no-pager | wc -l
0
[exit 0]
$ ls -A /run/systemd/system.control/ 2>/dev/null | grep -c "^tz56-"; ls -A /run/systemd/transient/ | grep -c "^tz56-"
0
0
[exit 1]
$ ls -d /var/tmp/tz56-vps /var/tmp/tz56-state /var/tmp/tz56-sig 2>&1 | wc -l; ls -d /var/tmp/tz56-* 2>/dev/null | wc -l
3
0
[exit 0]
$ systemctl list-unit-files 'crypto-*' --no-pager
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
[exit 0]
$ diff /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/v/unitfiles-v9.txt <(sed -n '/^$ systemctl list-unit-files/,/unit files listed/p' /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/a/a2.txt | sed 1d) && echo 'identical to A2'
identical to A2
[exit 0]
```

- Every unit started by this session (`tz56-subscribe`, `tz56-limits`, `tz56-limits2`, `tz56-sample-announce`, `tz56-announce`) is gone.
- No `tz56-*` entry remains under `system.control/` or `transient/`.
- The three scratch directories are absent, and the throwaway key went with them: the `3` is `ls`'s three error lines, and the glob count is 0. The throwaway key's agent was killed and its empty socket directory removed (D-8).
- `list-unit-files` is identical to A2's.

### V10 / V11 — the branch and the pull request

```
2026-10-03T03:45:02Z
$ git fetch --all --prune; git rev-parse origin/main; git log --oneline -1 origin/main
4f512019c8513c3fc5b8b2b46d4dec0365037221
4f51201 Add files via upload
[exit 0]
$ git diff --name-only origin/main...HEAD
.claude/settings.json
vps/announce.py
vps/common.py
vps/deploy.sh
vps/manifest
vps/run.py
vps/selftest.py
vps/units/crypto-run.service
[exit 0]
$ git push -u origin tz-56-run-lane-on-swap 2>&1 | grep -v "^remote: *$"
remote: Create a pull request for 'tz-56-run-lane-on-swap' on GitHub by visiting:        
remote:      https://github.com/seahomebatumi-ai/crypto-auto/pull/new/tz-56-run-lane-on-swap        
To github.com:seahomebatumi-ai/crypto-auto.git
 * [new branch]      tz-56-run-lane-on-swap -> tz-56-run-lane-on-swap
branch 'tz-56-run-lane-on-swap' set up to track 'origin/tz-56-run-lane-on-swap'.
[exit 0]
$ gh pr create --base main --head tz-56-run-lane-on-swap --title 'TZ-56: vps — the run on swap, each run its own measurement, every signed commit verified' --body-file /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/pr-body.md
https://github.com/seahomebatumi-ai/crypto-auto/pull/45
[exit 0]
```

`git diff --name-only origin/main...HEAD` lists only `vps/` paths and `.claude/settings.json`. `main` receives nothing from this session except this report.

## Test Results

| Item | Result |
|---|---|
| V1 selftest | **pass** — 17 sections, 181 checks, 0 failed, 0 empty; negative control red in J alone, then green with the MD5 restored |
| V2 syntax | **pass** — 8 `py_compile`, 2 `bash -n`, `systemd-analyze verify` exit 0 with no warning, `json.tool` exit 0 |
| V3 dry run | **pass** — path 1, runs-enabled 1, timer 0; unit files unchanged |
| V4 limits | **pass** — 7 of 7 known answers; C1b discriminating |
| V5 stream | **read** — R1; D3 exit 2, 0 data messages in 10 800 s |
| V6 signed deploys | **pass** — 5 of 5 derived answers (V6.1, three in V6.2, V6.3) |
| V7 credentials | **pass** — 12 counts, all 0 |
| V8 memory | **pass** — listing printed, no text |
| V9 nothing left | **pass** |
| V10 no production file | **pass** — 8 paths, all `vps/` or `.claude/settings.json` |
| V11 pushes | **pass** — branch pushed, PR #45 opened |

The bench gate does not read `vps/`: no workflow step runs `vps/selftest.py`. Every result above for the `vps/` code is local, on this VPS. The runner's result is under `## CI Execution`.

## Deviations

- **D-1. A2's date window.** `--since 2026-10-03` is the Tbilisi date of TZ-55's merge. Rule 8 puts the host in UTC, where that window starts after the install (2026-10-02T21:38:16Z), so the literal command read nothing and exited 1. It is recorded as run. A second read from 2026-10-02T20:00Z, Tbilisi midnight of 03.10, carries the lines.
- **D-2. `--limits` sets nothing outside a service.** `set_limits()` runs `systemctl set-property` only when its own cgroup's last component ends in `.service`, and otherwise logs `set=-`. If the mode were run by hand from a session or scope, it would otherwise set a memory ceiling on that scope. In the unit, which is the only place the TZ runs it, the guard is always true (C1 `set=0`).
- **D-3. C1b, a second probe.** C1's instant gave the floor pair, which equals the pair the probe started with, so C1 alone could not show the start setting anything (inv. 22). `tz56-limits2` repeated C1 with a different starting pair. It is a transient `tz56-*` unit (§4) and is gone (V9).
- **D-4. Checks beyond §12.6's table.**
  - J: each of the ten values also checks `memory_max + memory_swap_max = budget`.
  - O: `memory.swap.max` absent beside `max`.
  - P: `ANSWER_SUBTYPE == "REGISTER"`, no `SUBSCRIBE` attribute, and five `Stream.connect()` runs on a fake `websocket` module. These check success on `REGISTER`/`SUCCESS`, failure on `REGISTER`/`FAIL`, that no command is sent, that a pending `DATA` frame is kept, and failure with no answer. The table's "does not succeed" is decided in `connect()`, so P reads it there.
- **D-5. `_own_cgroup_limit()` returns `max` separately from unreadable.** §12.4 prints `max` and `-` differently, which the earlier `None` for both could not do. Admission treats both as setting no condition, as it did before.
- **D-6. Where `command answer` is logged.** `answer_of` is pure, as dictated, and returns the skipped frames. `connect()` logs each of them.
- **D-7. Instruments.**
  - A5's script prints one `open` and one `end` line per connection (counts and the end reason), plus a line for any control frame. None arrived. No frame content goes beyond §7's fields.
  - D3's sampler is TZ-55's file unchanged (MD5 `c85b4096bb5561fc36cb981e35771fb6`) and was not rewritten under a TZ-56 header.
- **D-8. Writes outside the listed scratch, all incidental.**
  - The dictated `deploy.sh --check` (A2, V6.1) fetches `origin main` into `/srv/crypto-auto` under the lock, as every deployer tick does.
  - Generating the throwaway key started a `gpg-agent` whose empty socket directory `/run/user/0/gnupg/d.n81y3hxf3nnudts5fuu7akih` was removed with `rmdir`.
  - The mtime of `/etc/crypto-auto/gnupg` moved at 22:44:00Z. That was the installed deployer's own tick, which verifies a commit every five minutes, not this session.
- **D-9. The manifest line.** It was written by `printf 'crypto-run.path\n' >> vps/manifest` outside the capture helper. E1 shows the file and its diff afterwards.

## Pre-existing Issues

- **P-1. TZ dates are Tbilisi dates.** The TZ's dates are written on the Boss's clock (`03.10.2026`; commit times `+04:00`), while rule 8 and the host are UTC. A2's window is the one place where the two disagree (D-1).
- **P-2. No hosted check reads `vps/`.** `bench.yml` has no step for `vps/selftest.py`, so a green gate says nothing about the VPS code. This has been the case since TZ-54. It is reported and not acted on.

## Remaining Risks

- **R-1. R1 may have read `REGISTER` wrongly.** A5's registered outcomes put R1 on connection 1's `REGISTER`/`SUCCESS`, and the TZ's derivation reads it as "the topic in the signed query is the subscription". But connection 2, which sent `SUBSCRIBE`, received both `REGISTER`/`SUCCESS` and then `SUBSCRIBE`/`SUCCESS`. So `REGISTER` arrives whatever the client sends, and the frames are equally consistent with `REGISTER` acknowledging only the connection. D3 under R1 received 0 data messages in three hours (2026-10-02T22:44Z–2026-10-03T01:44Z), which cannot separate "nothing was announced in the window" from "this connection is not subscribed". The rule-3 budget allowed no third read, such as R2's send or a window in Binance's publishing hours, to separate the two. Until one does, the stream stays off. TZ-54's and TZ-55's D3 never reached a data message either.
- **R-2. A first run may wait for admission while a session is open.** A run is admitted only when `MemAvailable ≥ memory.max + 64 MiB`, at least 234 881 024 bytes at the floor. With this session alive, `MemAvailable` read 218 202 112 at C1, 246 325 248 at C1b, and its minimum across D3's three hours was 134 758 400. A run started while a Claude session is open may wait up to 1 800 s and end with S6. Started with no session open, it gets more resident memory and less swap. TZ-55's run peaked at 283 MB resident; at the floor, the rest of a run that size goes to its own swap and runs slower.
- **R-3. The production path of `set-property`.** The persistent `crypto-run.service` will write its drop-ins under `/run/systemd/system.control/crypto-run.service.d/`, which C1's transient unit could not exercise, because transient drop-ins go under `transient/`. They are kept until reboot and rewritten at each start. After a reboot, the unit's floor pair applies until the first start's `ExecStartPre=` replaces it.
- **R-4. Merging turns runs on.** `install.sh` will enable `crypto-run.path` and create `runs-enabled`. From then on the bot's button and up to six watcher requests a day each start a full run on the owner's account. The first completed run's three `crypto-run:` lines are the fit measurement the next TZ reads (map §10).
- **R-5. The deployer's first range check.** The deployer that installs this merge is TZ-55's, which checks the newest commit only. The new range check runs from the following tick, with `base` set to the clone's `HEAD` at that time.

## Commit

Implementation, on the branch, already pushed: `16ca733f1757af7a24f2379c72381e7525782c93`, 8 files.

```
TZ-56: vps — the run on swap, each run its own measurement, every signed commit verified
```

Report, on `main`:

```
TZ-56: report — the run lane on swap
```

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/45 — base `main`, head `tz-56-run-lane-on-swap`.

## CI Execution

```
2026-10-03T03:47:02Z
$ gh run list --branch tz-56-run-lane-on-swap --limit 10 --json databaseId,name,event,status,conclusion,headSha
[{"conclusion":"success","databaseId":37094268249,"event":"pull_request","headSha":"16ca733f1757af7a24f2379c72381e7525782c93","name":"Bench gate","status":"completed"}]
[exit 0]
$ gh run view 37094268249 --json jobs -q '.jobs[] | .steps[] | "\(.number)  \(.conclusion)  \(.name)"'
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
$ gh run view 37094268249 --log | grep -E "checks run:|comparisons$" | sed -E "s/^[^\t]*\t[^\t]*\t[0-9TZ:.-]+ //" | head -20
checks run: 74   FAIL 0
E. venue-as-observation: 32 comparisons
F. anchored production arm: 29 comparisons
G. D4 partition: 63 comparisons
H. transport: 107 comparisons
I. attribution: 95 comparisons
J. gap in UTC: 8 comparisons
K. comparability: 11 comparisons
L. reading at production's instant: 18 comparisons
checks run: 506   FAIL 0
[exit 0]
```

`Bench gate` run 37094268249 (`pull_request`, head `16ca733`) completed with `success`. Every listed step succeeded, and the runner's own counts are `checks run: 74 FAIL 0` and `checks run: 506 FAIL 0`. The branch is not `claude/**`, so no push run fired. The gate reads no `vps/` path (P-2), so it shows that the production files are unchanged. It does not test this change. No other workflow ran on the branch.

## Final Repository State

- **Branch:** `tz-56-run-lane-on-swap` at `16ca733`, pushed, with `origin/tz-56-run-lane-on-swap` at the same commit. PR #45 is open. The worktree is clean on the branch.
- **VPS:** no `tz56-*` unit, drop-in, scratch directory or key remains. `list-unit-files 'crypto-*'` reads as in A2. The installed deployer is `main`'s. The deployed tree is still `43799ab7…`.
- **The fingerprints** below were taken on `origin/main` at `4f51201`.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

```
2026-10-02T22:35:18Z
$ bash /tmp/claude-0/-root-crypto-auto--claude-worktrees-bridge-cse-017LhWUiKPtLy2Lzh5SJA6R5/a108fc05-3e4d-5754-8c8e-42777dbf010e/scratchpad/gate.sh
map revision string: **Revision 2026-10-03-a.**
TZ requires:         **Revision 2026-10-03-a.**
anchor table rows: 7
[1] anchor: **Revision 2026-10-03-a.**
    TZ  grep -F -o -m1 -> **Revision 2026-10-03-a.**
    map grep -F -o -m1 -> **Revision 2026-10-03-a.**
[2] anchor: ### 3.12 Direction engine — veto cascade
    TZ  grep -F -o -m1 -> ### 3.12 Direction engine — veto cascade
    map grep -F -o -m1 -> ### 3.12 Direction engine — veto cascade
[3] anchor: ### 3.15 Catalyst registry
    TZ  grep -F -o -m1 -> ### 3.15 Catalyst registry
    map grep -F -o -m1 -> ### 3.15 Catalyst registry
[4] anchor: ### 3.16 List exhaustion — the day-range measure
    TZ  grep -F -o -m1 -> ### 3.16 List exhaustion — the day-range measure
    map grep -F -o -m1 -> ### 3.16 List exhaustion — the day-range measure
[5] anchor: ## 11. Analytical engine
    TZ  grep -F -o -m1 -> ## 11. Analytical engine
    map grep -F -o -m1 -> ## 11. Analytical engine
[6] anchor: ### 3.17 «РИСК ВЫНОСА» — the day's own risk
    TZ  grep -F -o -m1 -> ### 3.17 «РИСК ВЫНОСА» — the day's own risk
    map grep -F -o -m1 -> ### 3.17 «РИСК ВЫНОСА» — the day's own risk
[7] anchor: 72. **A write that fails leaves this run's product or nothing
    TZ  grep -F -o -m1 -> 72. **A write that fails leaves this run's product or nothing
    map grep -F -o -m1 -> 72. **A write that fails leaves this run's product or nothing
compared: 7 of table rows 7; matched both: 7
--- map file table
index.html required 3799 4e71da9badca3ccae85b656fdc3773e8 measured 3799 4e71da9badca3ccae85b656fdc3773e8 MATCH
main.py required 518 0e3ead8c300d2ee6783303c4bf2fb6b5 measured 518 0e3ead8c300d2ee6783303c4bf2fb6b5 MATCH
catalysts.json required 17 f9b2dd4a3594134b2b7b603de19075c3 measured 17 f9b2dd4a3594134b2b7b603de19075c3 MATCH
bench/exhaustion-calibration.txt required 175 3b8730b254467c9df4c0a845a0f3cfb3 measured 175 3b8730b254467c9df4c0a845a0f3cfb3 MATCH
--- added files
EXECUTOR-INSTRUCTIONS.md 991 d7bd23785656896a119e0cb7f0fddad5
ANALYST-INSTRUCTIONS.md 3866 feaaffc99f983b3441ce205bcf1b6466
contract version line: **Version 26.**
map: 3161 605e4f53306c7971b77b94c2e38207a1
origin/main:vps tree: 43799ab742c8b4d67651cc3b07a0e6e31ee40e95
[exit 0]
```

The anchors are cut by the table's structure: every row between the separator line and the table's end. The table has 7 rows and 7 were compared; each anchor's text was returned by both the TZ and the map, as printed.

| File | Required | Measured |
|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | revision `**Revision 2026-10-03-a.**`; 3161, `605e4f53306c7971b77b94c2e38207a1` (reported) | `**Revision 2026-10-03-a.**`; 3161, `605e4f53306c7971b77b94c2e38207a1` |
| `index.html` | 3799, `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518, `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17, `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175, `3b8730b254467c9df4c0a845a0f3cfb3` | match |
| `EXECUTOR-INSTRUCTIONS.md` | `**Version 26.**`; 991, `d7bd23785656896a119e0cb7f0fddad5` | `**Version 26.**`; 991, `d7bd23785656896a119e0cb7f0fddad5` |
| `ANALYST-INSTRUCTIONS.md` | 3866, `feaaffc99f983b3441ce205bcf1b6466` | 3866, `feaaffc99f983b3441ce205bcf1b6466` |
| `origin/main:vps` | written against `43799ab742c8b4d67651cc3b07a0e6e31ee40e95` | `43799ab742c8b4d67651cc3b07a0e6e31ee40e95` |

The capture helper filled every block in this report from the scratch capture files, except the V7 block. That block was written first as the expected output, then compared with the real command run on this file's final text (`diff` printed nothing).
