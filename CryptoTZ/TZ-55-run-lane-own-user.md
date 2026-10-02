# TZ-55 — The run lane on the 1 GB host: its own user, test-mode memory, signed deploys, the new key

**Canonical filename:** `CryptoTZ/TZ-55-run-lane-own-user.md`
**Report:** `CryptoReports/TZ-55-run-lane-own-user-report.md`
**Class:** branch TZ (contract §8) — it modifies files under `vps/**` and creates none.
**Branch:** `tz-55-run-lane-own-user` · **Model:** Opus
**Previous TZ:** TZ-54, merged at `966b3f2` on 02.10.2026; its report is on `main`.
**Written against:** contract v25, map `2026-10-01-f`, methodology `2026-10-01-a`, TZ-54's report, and
the `vps` tree of `966b3f2` (`2b66e47f47b0e3fcd3f47805f808045c1b4cf9de`), read by the Architect on
02.10.2026. Map §10 row «The assistant's build sequence», items (6) to (8) and the decision of
`2026-10-01-f`, is what this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-01-f.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-01-f.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 963 | `ef21a864f6c93d1c59d72b9e16eb967f` | its version line reads `**Version 25.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `ANALYST-INSTRUCTIONS.md` | 3866 | `feaaffc99f983b3441ce205bcf1b6466` | reported |

The map itself: 3141 lines, MD5 `f780f2e73c6067d52fa12ed628a23f3c` — reported, not enforced. The tree `origin/main:vps`
is reported beside them; `2b66e47f47b0e3fcd3f47805f808045c1b4cf9de` is the tree this TZ was written
against, and a different one is a finding, never a block.

---

## 1. Credentials

| Name | How it arrives | File on the VPS | Read only by |
|---|---|---|---|
| `BINANCE_API_KEY`, `BINANCE_API_SECRET` | the trigger message, one `NAME=value` line each under `EXECUTE TZ-55` | `/etc/crypto-auto/credentials/binance-api-key`, `binance-api-secret` — TZ-54's files replaced | `crypto-announce.service`; D3's unit |
| the run's Claude login | **never arrives**: minted at C4 by §12.8 | `/etc/crypto-auto/credentials/claude-oauth-token` | `crypto-run.service`; C6's and D2's units |
| the deploy key | already on the VPS, root's identity for this repository (A6) | copied at C3 to `/etc/crypto-auto/credentials/deploy-key`; root's copy stays | `crypto-run.service`; C6's and D2's units |

- **Each file `0600 root:root`, no trailing newline, written by a command that prints nothing**
  (contract §7 item 6). A credential file is read afterwards only by a command that prints a count.
- **A Binance value is written exactly as the trigger carries it:** surrounding whitespace stripped
  and nothing else. A value that is not 64 characters of `[A-Za-z0-9]` after that is **not written**,
  and the announce scope is BLOCKED — no letter is mapped, guessed or corrected. TZ-54 D-1
  normalised look-alike letters, and the exchange refused the result (map §10, row «The engine's
  exchange-announcement read is a path its own §6 forbids»).
- **The owner acts twice in this session and nowhere else:** the two lines under the trigger, and
  at C4 the authorization link — he opens it, approves, and sends the code it shows back to the
  session. The session posts the link and nothing else of the flow.
- **The key's rights are read before any stream is opened** (TZ-54 §12.9, unchanged). A key with any
  right beyond reading, or with no address binding, is refused, both Binance files are deleted and
  the report's first line says the key must be revoked in Binance.

---

## 2. Contract and map text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> **A unit that runs a model session runs as its own unprivileged user, never root, and holds exactly two credentials: its own Claude login and the deploy key** (since v25)

— contract §7 item 6.

> **The Claude login never travels at all:** `claude setup-token` mints it on the VPS while the Boss approves in his own browser, the code he passes back is single-use, and the token goes from the command's output to its file without being displayed.

— contract §7 item 6.

> **The deployer installs a `vps` tree only from a commit GitHub signed** (since v25): the newest commit on `main`'s first-parent line that changed `vps/` must carry GitHub's own signature

— contract §7 item 15.

> A tree that fails the check is neither fast-forwarded into the deployer's clone, whose files the services run, nor installed, and the Boss is told once per tree.

— contract §7 item 15.

> it may start TRANSIENT units from its branch for a measurement its TZ names, and its report proves none is left behind.

— contract §7 item 15.

> an implementation session that starts either for a measurement its TZ names never reads, relays or edits the answer that run publishes, and edits nothing it writes.

— contract §1.

> and the run fits when it completes under those limits, which TZ-55 measures as the run's own user.

— map §10, row «The assistant's build sequence».

> A run that fails for any other reason, the account's limit included, measures nothing about memory and decides nothing about size

— map §10, row «The assistant's build sequence».

---

## 3. What is built

The run lane, made safe and made to fit the host as it is. **`crypto-run.service` runs as its own
user `cryptorun`**, from its own clone, holding its own Claude login and the deploy key and able to
read no other credential. **Its memory runs in test mode:** the budget stays one and a half times
the run's footprint, the resident part is capped at what the host frees, and the rest is the run's
own swap, so the run pays for the shortage and the owner's other services do not. **One complete
run, measured under exactly those limits, decides whether the timers are enabled.** Around it: the
instrument stops summing processes that never coexisted; the deployer installs only a `vps` tree
GitHub signed and tells the Boss once per refused tree; the bot no longer lets one undeliverable
file hold every later answer; and the announcement stream is measured on the new key.

---

## 4. Scope

### Files to Modify

```
vps/common.py      vps/run.py        vps/bot.py         vps/cleanup.py     vps/selftest.py
vps/deploy.sh      vps/install.sh    vps/manifest       vps/memory-record.txt
vps/units/crypto-run.service
```

### Files to Create

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- the system group and user `cryptorun` — home `/var/lib/cryptorun` (`0750 cryptorun:cryptorun`),
  shell `/usr/sbin/nologin`, supplementary group `cryptoauto`;
- `/var/lib/cryptorun/.ssh/known_hosts` (`0644 cryptorun:cryptorun`), holding root's `github.com`
  host-key lines;
- the clone `/var/lib/cryptorun/crypto-auto`, owned by `cryptorun`: fetched from
  `https://github.com/seahomebatumi-ai/crypto-auto.git`, `remote.origin.pushurl` set to
  `git@github.com:seahomebatumi-ai/crypto-auto.git`, its committer identity copied as TZ-54 D-8 did;
- the credential files of §1, and `/etc/crypto-auto/gnupg` (`0700 root:root`) holding GitHub's
  web-flow public key;
- Ubuntu's `gnupg`, only where A4 finds `gpg` absent;
- removal of TZ-54's leftovers: the worktree `/srv/crypto-auto-run` (`git -C /srv/crypto-auto
  worktree remove --force /srv/crypto-auto-run`), `/root/.claude/projects/-srv-crypto-auto-run` and
  `/root/.claude/projects/-srv-crypto-auto`;
- transient units named `tz55-*`, the tmux session `tz55-token` during C4, and the scratch
  directories `/var/tmp/tz55-vps`, `/var/tmp/tz55-state` and `/root/tz55-token` — all gone at the end.

**No other Claude session is stopped and no file of the owner's other projects is touched** (owner's
message of 02.10.2026: «I didn't terminate the other sessions»).

### On `main`, written by programs during Stage D

`analyst/live.json` by the writer, and `analyst/state.json` and `analyst/log/**` by D2's run. The
session itself writes nothing under `analyst/` (contract §1); its only direct push is its report.

---

## 5. What this TZ does not decide and does not build

- **The host's size.** D2 decides fit; map §10 decides the answer to a run that does not fit, and the
  owner resizes. This TZ resizes nothing.
- **The six sentences** map §10 lists — an Architect edit after the merge that enables runs.
- **The hunter's schedule, and the watcher's calendar and regime conditions** (map §10).
- **Any order, and any key with trading rights.**
- **`crypto-bot.service`, `crypto-exchange.service`, `crypto-announce.service` and their timers'
  unit files** are unchanged; `bench.yml` is not touched.

---

## 6. Rules — binding in every stage

1. **Credentials** follow §1 and contract §7 item 6; C4 follows §12.8 and nothing else.
2. **Redaction.** `common.redact()` covers every credential a program loads, the Claude login
   included; the deploy key is read by `ssh` alone and by no program of this repository.
3. **The session's own network read** is A5's, in TZ-53's form: `curl -sS -L -m 20 -o <body> -D
   <headers> -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' '<url>'` — one
   request, no retry, no user agent, header, proxy or cookie.
4. **A challenge or a refusal is a reading** (`ANALYST-INSTRUCTIONS.md` §6).
5. **Atomic writes** (inv. 72) for every file a later reader treats as current, the two new markers
   of §12.9 included.
6. **Russian text in `vps/` code** is `\uXXXX` escapes and equals §12.1 character for character.
7. **Python 3.12's standard library and bash only**; `gpg` is reached through `git verify-commit`.
8. **Time is UTC everywhere.**
9. **D2 runs at most twice**, under §10's rule; a run stopped by its memory or time limit is the
   reading and is never repeated.
10. **Every transient unit** is named `tz55-*`, runs with `MemoryAccounting=yes`, and is gone at the end.

---

## 7. Stage A — readings, no writes

- **A1.** Contract §4a steps 1–6, and the §5 gate against §0 including the added-files table.
- **A2. What holds the memory,** read at one instant by TZ-54 A2's method and tables.
- **A3. What TZ-54's merge put into effect:** `journalctl -u crypto-deploy.service --since
  2026-10-02 -o cat` lines beginning `deploy:` or `install:`; `systemctl list-unit-files 'crypto-*'`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`; `cat
  /var/lib/crypto-auto/deployed-vps-tree` beside `git -C /srv/crypto-auto rev-parse origin/main:vps`;
  the last `exchange:` line of `crypto-exchange.service`'s journal and the count of `bot:` lines of
  `crypto-bot.service`'s. Known answer: the marker reads
  `2b66e47f47b0e3fcd3f47805f808045c1b4cf9de` — derived from the Architect's read of `966b3f2:vps`.
- **A4. Tools:** `command -v gpg` and `gpg --version | head -1`; `claude --version`; `stat -c '%a %U
  %n'` on `readlink -f "$(command -v claude)"` and on each of its parent directories up to `/usr`;
  `id cryptorun`, expected absent; `getent group cryptoauto`.
- **A5. GitHub's signing key:** one read of `https://github.com/web-flow.gpg` under rule 3, imported
  into the scratch `GNUPGHOME=/var/tmp/tz55-state/gnupg`; its keys' fingerprints printed from `gpg
  --list-keys --with-colons`. Then, with that `GNUPGHOME`: `git -C /srv/crypto-auto verify-commit
  966b3f2` exits 0 and `git -C /srv/crypto-auto verify-commit b097a89` exits non-zero; `git -C
  /srv/crypto-auto log --first-parent -1 --format=%h origin/main -- vps` prints `966b3f2` and the same
  command without `--first-parent` prints `b097a89`. **Known answers, derived from the Architect's
  read on 02.10.2026:** `git log --format='%h %G? %GK'` shows `966b3f2 E B5690EEEBB952194` — signed,
  by a key the reader lacked — and `b097a89 N`, unsigned; the merge is the first-parent commit that
  changed `vps/`, and the branch commit is the one plain history reaches. If `966b3f2` does not
  verify, the deployer scope is BLOCKED.
- **A6. Root's identity for this repository:** `ssh -G github.com | grep -i '^identityfile'`; then
  `ssh -T -v -o BatchMode=yes git@github.com 2>&1 | grep -E 'Server accepts key|Authenticated to|Hi '`
  — the accepted key's path and GitHub's greeting, neither a secret; `ssh-keygen -F github.com` over
  root's `known_hosts`, its line count, and `ssh-keygen -lf` on those lines. **Known answer:** the
  greeting names `seahomebatumi-ai/crypto-auto` — derived from TZ-53's push over «the deploy key
  `crypto-auto-vps`» (map §10, row «Executor has no GitHub API access»), and GitHub greets a deploy
  key by its repository's full name. A greeting naming an account instead means root's key is not a
  deploy key: it is never handed to a model session, and the run scope is BLOCKED.
- **A7.** This session's `PATH`, printed. It is the run unit's `PATH`.

---

## 8. Stage B — the code, on the branch

### B1. `vps/common.py`

- `RUN_HOME = "/var/lib/cryptorun"`; `RUN_TREE = RUN_HOME + "/crypto-auto"`.
- `S11`, §12.1's string.
- `RESERVE_BYTES = 64 MiB`, `MEMORY_MAX_FLOOR_BYTES = 160 MiB`, each with §12.4's derivation in a
  comment; `test_limits(footprint_bytes, duration_s, host_free_bytes)` → `(budget, memory_max,
  memory_swap_max, runtime_max_s)` by §12.4, the one implementation, built on `derive_limits`, which
  stays as it is.

### B2. `vps/run.py`

1. Default `--tree` is `common.RUN_TREE`. Step 3 no longer takes the deployer's git lock — the run
   has its own clone — and is otherwise unchanged: fetch, the subjects of local commits absent from
   `origin/main` logged, `reset --hard origin/main`, `clean -fdx`.
2. **Admission** waits until `MemAvailable` ≥ this unit's `memory.max` **and**, where its
   `memory.swap.max` is a number above 0, `SwapFree` ≥ that number; the poll, the 1 800 s and S6 are
   unchanged.
3. **The Claude login** is read with `common.load_credential("claude-oauth-token")` and placed in
   the environment of the `claude` child alone, as `CLAUDE_CODE_OAUTH_TOKEN`; the writer's
   environment does not carry it. The command list is TZ-54 §12.2's, byte for byte.
4. The second summary line gains `subtype`, `api_error_status`, `terminal_reason` and `stop_reason`
   from `result.json` — categorical fields, never `result`.

### B3. `vps/bot.py`

A file one of whose chunks is refused in both forms — HTML, then plain text, both HTTP 400 — is
renamed `<name>.dead` beside itself, logged once by name, and the loop goes on to the next file. A
network error and a 429 keep TZ-54's behaviour. `outbox_files()` already ignores `.dead`, and
`cleanup.py` removes it after 7 days like any outbox file.

### B4. `vps/deploy.sh` — §12.9

### B5. `vps/install.sh`

- `provision_user` also creates `cryptorun` as §4 states, idempotently.
- `provision_run_clone`: the clone of §4 when `/var/lib/cryptorun/crypto-auto/.git` is absent; the
  push URL and the committer identity set where missing, printing no value; `chown -R
  cryptorun:cryptorun`. `known_hosts` for `cryptorun` written from `ssh-keygen -F github.com` over
  root's file when absent.
- `provision_worktree` is removed: nothing creates `/srv/crypto-auto-run` again.
- **New mode `--provision`:** users, groups, directories, the run clone and `known_hosts` — nothing
  installed, enabled, copied or removed. Default mode calls the same functions.

### B6. `vps/cleanup.py`

`RUN_RECORDS` is the directory E4 names.

### B7. `vps/selftest.py` — §12.7

### B8. `vps/units/crypto-run.service` — §12.5

`vps/manifest` and `vps/memory-record.txt` are written at Stage E and at no other time.

---

## 9. Stage C — provisioning on the VPS

- **C1.** `apt-get install -y gnupg` only when A4 found `gpg` absent; its version recorded.
- **C2.** The Binance files of §1, by §1's rule; per value the printed counts are its length, the
  whitespace stripped and whether it is 64 characters of `[A-Za-z0-9]`.
- **C3.** `bash vps/install.sh --provision` from the branch. Then the deploy key: `install -m 0600
  -o root -g root <A6's accepted key path> /etc/crypto-auto/credentials/deploy-key`, only when A6's
  greeting named the repository. Then GitHub's key: A5's file imported into
  `GNUPGHOME=/etc/crypto-auto/gnupg` (`0700 root:root`), its fingerprints listed.
- **C4.** The Claude login, by §12.8.
- **C5.** TZ-54's leftovers removed, as §4 names them.
- **C6. The probe**, in `tz55-probe`: every property of §12.5's unit except `ExecStart`, the memory
  limits, which it does not set, and `RuntimeMaxSec=300`, plus `BindReadOnlyPaths=/var/tmp/tz55-vps`
  and `RemainAfterExit=yes`; `/var/tmp/tz55-vps` is a `0755 root:root` copy of the branch's `vps/`
  with the probe script beside it. The script prints exit codes and booleans only:
  1. `id -u` is not 0;
  2. `claude -p "Reply with exactly HEADLESS-OK" --output-format json --model opus`, with
     `CLAUDE_CODE_OAUTH_TOKEN` read from `$CREDENTIALS_DIRECTORY/claude-oauth-token`: `is_error`
     false and `result` exactly `HEADLESS-OK` — the known answer of TZ-53's probe (map §10);
  3. `git -C /var/lib/cryptorun/crypto-auto push --dry-run origin HEAD:refs/heads/tz-55-push-probe`
     exits 0 — TZ-53's form, which creates nothing;
  4. **the flip** (inv. 68): `test -r` exits 1 on `/etc/crypto-auto/credentials/telegram-bot-token`,
     `/etc/crypto-auto/credentials/binance-api-secret`, `/etc/crypto-auto/credentials/owner-chat-id`,
     `/run/credentials/crypto-bot.service/telegram-bot-token` and `/root/.claude`, and exits 0 on
     `$CREDENTIALS_DIRECTORY/claude-oauth-token` and `$CREDENTIALS_DIRECTORY/deploy-key`.
  Any other result BLOCKS the run scope; the deployer, the bot and the announce scopes go on.

---

## 10. Stage D — measurements in transient units started from the branch

In this order: D3 is **started** first, because it holds up to three hours; then D1, D2 and D5; then
D3 is collected.

- **D3. The key and the stream:** TZ-54 D3's command with `tz55-` names and `RemainAfterExit=yes`
  (TZ-54 D-3), the state directory `/var/tmp/tz55-state`; collected at the end: exit status, the
  peaks read by a one-second reader as TZ-54 D-4 did, and its journal.
- **D1. The instrument's known answers,** by §12.3: `tz55-hog1` runs TZ-54's hog once, and `F` ≥
  100 663 296; `tz55-hog3` runs it three times in sequence in one unit — `/bin/sh -c` with three
  `python3 -c` lines — and 100 663 296 ≤ `F` < 201 326 592. Either failing means the instrument is
  broken: D2 does not run and the decision scope is BLOCKED.
- **D2. One complete run under the limits it will run with.** First `A0` at one instant, by TZ-54
  A2's method. Then §12.4's limits from `F0` = 466 161 664 and `D0` = 604.899672. Where `memory_max`
  is below 160 MiB, D2 does not run and `fits=no`. Otherwise `tz55-run`: every property of §12.5's
  unit except `ExecStart`, with `MemoryMax=`, `MemorySwapMax=` and `RuntimeMaxSec=` set to those
  limits, plus `BindReadOnlyPaths=/var/tmp/tz55-vps`, `RemainAfterExit=yes`, and `ExecStart`
  `/usr/bin/python3 /var/tmp/tz55-vps/run.py --tree /var/lib/cryptorun/crypto-auto`; not waited on,
  sampled by §12.3 until inactive. Then `systemctl show tz55-run -p Result -p ExecMainStatus -p
  ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p
  MemorySwapPeak`; the `crypto-run:` and `writer:` lines of its journal; the commit subjects on
  `origin/main` since D2 started; and the directory the run created under
  `/var/lib/cryptorun/.claude/projects/`, with its entry count.
  - **`Result=oom-kill` or `Result=timeout`:** the run did not fit; `fits=no`; never repeated.
  - **`Result=exit-code` with `is_error=true`:** the run failed for another reason; its `subtype`
    and `api_error_status` are printed. **One more D2 is permitted, no sooner than 60 minutes
    later,** with `A0` read again and the limits derived again. A second such failure leaves the
    decision scope BLOCKED: no `fits` line is written and the manifest gains no run line.
  - **Success:** `fits=yes`.
- **D5. Delivery**, at once after the last D2: TZ-54 D5's command with `tz55-send`. The file D2
  wrote reaches the owner's chat. **The session never reads, quotes or characterises it** (contract
  §1): it prints the counts `--send-outbox-once` prints and nothing else.

---

## 11. Stage E — decisions written into the branch

- **E1. Limits.** `memory_max` as the last D2 ran it; `budget` = the larger of §12.4's budget from
  `F0` and from that D2's own `F`; `memory_swap_max` = `budget` − `memory_max`; `runtime_max_s` from
  that D2's `D`.
- **E2.** `vps/memory-record.txt` in §12.6's form; `crypto-run.service`'s `MemoryMax=`,
  `MemorySwapMax=` and `RuntimeMaxSec=` set from it.
- **E3. `vps/manifest`:** always `crypto-deploy.timer`, `crypto-cleanup.timer`,
  `crypto-exchange.service` and `crypto-bot.service`; `crypto-announce.service` when D3 exited 0;
  `crypto-run.timer` and `crypto-run.path` when the record says `fits=yes`.
- **E4.** `cleanup.py`'s `RUN_RECORDS` set to the directory D2's reading named.
- **E5.** `python3 vps/selftest.py` green in every section.

---

## 12. Dictated blocks

### 12.1 Russian string — character for character

| Id | Where | Text |
|---|---|---|
| S11 | a `vps` tree refused for its signature | «Обновление сервера не установлено: изменение не подписано GitHub.» |

### 12.2 The headless session

TZ-54 §12.2, unchanged. The Claude login reaches it through its environment and through nothing
else; nothing is added to the command.

### 12.3 The memory instrument

Every second until the unit is inactive, from `/sys/fs/cgroup/system.slice/<unit>.service/`:
`memory.current`, `memory.swap.current`, `memory.peak` and `memory.swap.peak`; with `MemAvailable`
and `SwapFree` from `/proc/meminfo`. `F_run` is the largest `memory.current + memory.swap.current`
of any second; `P_peak` is `memory.peak + memory.swap.peak` at the last read before the cgroup is
gone; `F = max(F_run, P_peak)`. **No per-process term:** TZ-54's sum of every pid's largest
`VmHWM` added 112 processes that never coexisted — 938 MB against the cgroup's 291 MB. The hog is
TZ-54 §12.7's line. **Known answers, derived from the definition:** one hog — `F` ≥ 100 663 296,
because `memory.peak` holds the hog's allocation; three hogs in sequence — 100 663 296 ≤ `F` <
201 326 592, because no term adds processes whose lifetimes did not overlap.

### 12.4 Limits and fit — the test mode

```
MiB             = 1 048 576 ; step = 16 MiB
budget          = ceil(1.5 × F / step) × step                         # TZ-54 §12.8, unchanged
memory_max      = min(budget, floor((A0 − 64 MiB) / step) × step)     # the resident ceiling
memory_swap_max = budget − memory_max                                 # 0 when memory_max = budget
runtime_max_s   = max(ceil(2 × D / 300) × 300, 3600) + 1800
A0              = MemAvailable + the measuring session tree's summed VmRSS, at one instant before D2
D2 runs           only when memory_max ≥ 160 MiB
fits            = D2 completed under memory_max, memory_swap_max and runtime_max_s
completed       = Result=success, ExecMainStatus=0, is_error false, result non-empty
```

**Derivations.** 64 MiB is [Architect's decision: headroom left to the host's page cache and the
small services, whose ceilings are 128M each and whose measured peaks were 13–22 MB]. 160 MiB is
derived: the measuring session's own Claude process held 161 374 208 bytes resident at TZ-54 A2,
and a ceiling below one Claude process cannot hold the run's. `F0` = 466 161 664 is TZ-54 D2's
`MemoryPeak` 285 847 552 plus its `MemorySwapPeak` 180 314 112 — §12.3's `P_peak` for that run —
and `D0` = 604.899672 s is TZ-54's record. A run that does not fit is answered by map §10, never by
this TZ.

**Known answers, computed by the Architect:**
`test_limits(466161664, 604.899672, 419430400)` = `(704643072, 352321536, 352321536, 5400)`;
`test_limits(291307520, 604.899672, 1073741824)` = `(452984832, 452984832, 0, 5400)`;
`test_limits(466161664, 604.899672, 379584512)` = `(704643072, 301989888, 402653184, 5400)`;
`test_limits(466161664, 604.899672, 209715200)` gives `memory_max` 134 217 728, below the floor of
167 772 160, so D2 does not run.

### 12.5 `vps/units/crypto-run.service` — exactly these lines

```
[Unit]
Description=Crypto assistant: one headless analysis run
Wants=network-online.target
After=network-online.target
StartLimitIntervalSec=600
StartLimitBurst=3

[Service]
Type=exec
User=cryptorun
Group=cryptorun
SupplementaryGroups=cryptoauto
WorkingDirectory=/var/lib/cryptorun/crypto-auto
Environment=HOME=/var/lib/cryptorun
Environment=PATH=<A7>
Environment=PYTHONDONTWRITEBYTECODE=1
Environment=DISABLE_AUTOUPDATER=1
Environment="GIT_SSH_COMMAND=ssh -i %d/deploy-key -o IdentitiesOnly=yes -o UserKnownHostsFile=/var/lib/cryptorun/.ssh/known_hosts"
LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token
LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key
ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/run.py
RuntimeDirectory=crypto-run
NoNewPrivileges=yes
CapabilityBoundingSet=
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/var/lib/cryptorun /var/spool/crypto-auto
MemoryAccounting=yes
MemoryMax=<E2>
MemorySwapMax=<E2>
RuntimeMaxSec=<E2>
OOMScoreAdjust=500
Nice=5
SuccessExitStatus=75
```

`%d` is systemd's credentials directory; C6 proves the push works through it before D2 relies on it.

### 12.6 `vps/memory-record.txt`

```
# TZ-55 measurement record of crypto-run.service (map inv. 46). Written at Stage E; never edited by hand.
measured_utc=<YYYY-MM-DDTHH:MM:SSZ of the last D2>
hog_bytes=100663296
hog_footprint_bytes=<F of tz55-hog1>
hog3_footprint_bytes=<F of tz55-hog3>
input_footprint_bytes=466161664
input_duration_s=604.899672
run_attempts=<1|2>
run_completed=<yes|no>
run_duration_s=<D>
run_cgroup_footprint_bytes=<F_run>
run_kernel_peak_bytes=<P_peak>
run_footprint_bytes=<F>
mem_available_bytes=<MemAvailable before the last D2>
session_rss_bytes=<the session tree's VmRSS then>
host_free_bytes=<A0>
budget_bytes=<E1>
memory_max_bytes=<E1>
memory_swap_max_bytes=<E1>
runtime_max_s=<E1>
fits=<yes|no>
```

### 12.7 Selftest sections — changed and new

| Section | What it compares | Known answer and its source |
|---|---|---|
| J | `derive_limits` and `test_limits` | TZ-54 §12.8's two answers and §12.4's four |
| M | `vps/memory-record.txt` against `crypto-run.service` and `vps/manifest` | `run_footprint_bytes` = max(cgroup, kernel peak); `host_free_bytes` = mem_available + session_rss; `memory_max_bytes` = `test_limits(input_footprint, input_duration, host_free)`'s second term; `budget_bytes` = the larger budget of input and run footprints; `memory_swap_max_bytes` = budget − memory_max; `runtime_max_s` from `run_duration_s`; the unit's three lines equal the record; `hog_footprint_bytes` ≥ `hog_bytes` > `hog3_footprint_bytes` / 2; the manifest lists both run lines exactly when `fits=yes` |
| N | the bot on a mock API | a file whose chunk is refused twice ends as `<name>.dead`, the next file is sent, and the outbox holds the `.dead` file alone |
| O | `run.py` with a stub `claude` and a stub writer on `PATH` | the stub `claude` sees `CLAUDE_CODE_OAUTH_TOKEN` equal to a planted credential and the stub writer does not; the summary carries the stub's `subtype`, `api_error_status`, `terminal_reason` and `stop_reason` and never its `result`; admission refuses while `SwapFree` is below `memory.swap.max` |

Every other section is TZ-54's and stays green; section M's TZ-54 rule is replaced by this one.

### 12.8 The Claude login — C4, step by step

1. `mkdir -m 0700 /root/tz55-token`; `tmux new-session -d -s tz55-token "script -q -f -c 'claude
   setup-token' /root/tz55-token/out"` — the command's output goes into that file and nowhere else.
2. The authorization URL is read out of the file with a pattern matching `https://` up to the next
   whitespace, and posted to the owner — the URL alone. If no whole URL can be read, or the screen
   asks for something other than a code, the screen's text is reported with no value in it and the
   run scope is BLOCKED.
3. The owner opens it, approves, and sends back the code shown. The session sends it with `tmux
   send-keys -t tz55-token -l '<code>'` and then `Enter`. The code is single-use.
4. A script reads the file, takes the token by the pattern `sk-ant-oat01-[A-Za-z0-9_-]+`, writes it
   to `/etc/crypto-auto/credentials/claude-oauth-token` (`0600 root:root`, no newline) and prints
   only `length=<n> matched=<yes|no>`.
5. `tmux kill-session -t tz55-token`; `shred -u /root/tz55-token/out`; `rmdir /root/tz55-token`.

**No command in this session prints the file, the pane or the token.** C6's probe proves the token.

### 12.9 `vps/deploy.sh` — in this order

1. `/run/crypto-run` exists → exit 0, the tick skipped.
2. Under `flock /run/lock/crypto-auto-git.lock`: `git -C /srv/crypto-auto fetch origin main`.
3. `origin/main:vps` absent → TZ-54's behaviour: log it, fast-forward, exit 0.
4. `c` = `git log --first-parent -1 --format=%H origin/main -- vps`; `GNUPGHOME=/etc/crypto-auto/gnupg
   git verify-commit "$c"`. **Not verified** → log `deploy: unsigned vps commit <c>, not installed`;
   S11 to the outbox only when `/var/lib/crypto-auto/refused-vps-tree` differs from the tree, then
   the tree written there atomically; exit 1 — **no fast-forward and no install** (contract §7
   item 15).
5. `git merge --ff-only origin/main`.
6. The `vps` tree equals `/var/lib/crypto-auto/deployed-vps-tree` → exit 0.
7. `install.sh`; success → the tree written to that marker; failure → S10 to the outbox only when
   `/var/lib/crypto-auto/refused-vps-tree` differs from the tree, then the tree written there; exit 1.
   One refused-tree marker serves both refusals, so the Boss is told once per tree, whichever the
   reason (contract §7 item 15).

**`--check`** runs steps 2 and 4 only, prints `deploy: check commit=<h> signed=<yes|no>`, and exits
0 when signed and 1 otherwise; it fast-forwards, writes and installs nothing.

---

## 13. Validation

- **V1. Selftest.** `python3 vps/selftest.py` after Stage E: exit 0, every section non-empty, the
  total printed. **Negative control** (inv. 68): one digit of a §12.4 known answer in section J
  changed in the working tree → exit non-zero with section J alone failing; reverted; green again.
- **V2. Syntax.** `python3 -m py_compile` on every `vps/*.py`; `bash -n` on both scripts;
  `systemd-analyze verify` on every file of `vps/units/`, exit 0, warnings printed.
- **V3. Dry run.** `bash vps/install.sh --dry-run` prints what it would do, and `systemctl
  list-unit-files 'crypto-*'` reads the same before and after; a second `--provision` creates nothing.
- **V4. The writer and the run.** The last D2's `writer:` line shows `gate_exit=0 committed=yes
  pushed=yes`; with `fits=yes`, `origin/main` carries the run's own `analyst: <date>`.
- **V5. The instrument.** D1's two known answers.
- **V6. Fit.** E1's terms printed; section M green.
- **V7. Delivery.** D5's accepted chunks equal its chunks; the outbox empty afterwards.
- **V8. Credentials.** `stat -c '%a %U %s %n'` on the directory and its six files; no last byte is
  a newline; C6's flip as printed. **The exact-value scan** — `grep -c -F -f` with each of
  `binance-api-key`, `binance-api-secret` and `claude-oauth-token`, each proven first to hold one
  non-empty line, and with the deploy key's base64 lines alone — over this report, `git diff
  origin/main...HEAD`, every file under the branch's `vps/`, `origin/main`'s `analyst/**` files
  written since the session started, `journalctl -o cat -u 'tz55-*'` and `journalctl -o cat -u
  crypto-deploy.service`: every count 0. `/root/tz55-token` is absent and `tmux has-session -t
  tz55-token` fails.
- **V9. The key and the stream.** D3's verdict with its field booleans, the subscribe answer, every
  message's `catalogName`, title, publish time and lag, pings, reconnects and the exit code.
- **V10. Signed deploys.** `bash vps/deploy.sh --check` from the branch prints `commit=966b3f2…
  signed=yes` and exits 0, with `GNUPGHOME=/etc/crypto-auto/gnupg` in place; `git -C /srv/crypto-auto
  verify-commit b097a89` under the same `GNUPGHOME` exits non-zero; `cmp` of
  `/usr/local/libexec/crypto-auto/deploy.sh` with `git -C /srv/crypto-auto show origin/main:vps/deploy.sh`
  reports them identical — the session installed no deployer.
- **V11. Nothing left.** `systemctl list-units --all 'tz55-*'` empty; `systemctl list-unit-files
  'crypto-*'` identical to A3's; `/var/tmp/tz55-vps`, `/var/tmp/tz55-state`, `/srv/crypto-auto-run`
  and the two record directories of §4 absent; `git ls-remote --heads origin tz-55-push-probe` empty.
- **V12. No production file.** `git diff --name-only origin/main...HEAD` lists only `vps/` paths.
- **V13. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main`
  receives nothing from this session but its report.

---

## 14. The report

Contract §10's template, with: A2's tables; A3's lines and marker; A4–A7 as printed; C2's counts;
C3's fingerprints; C4's `length=… matched=…` line; C6's results; D1's two `F`; each D2's `A0` and its
terms, the limits it ran under, `Result`, `ExecMainStatus`, `D`, `F_run`, `P_peak`, `F`, the
`crypto-run:` and `writer:` lines, the commit subjects and the record directory; D3 and D5 as
printed; E's record and manifest; V1–V13. **The first line after `## Status` states the fit** —
`fits`, with `memory_max_bytes` and `memory_swap_max_bytes` against `A0` — because it decides
whether the host is resized; **the second states whether the announcement stream is enabled.** The
answer D2 produced is not quoted, summarised or characterised (contract §1).

---

## 15. Commit messages

Implementation, on the branch:

```
TZ-55: vps — the run as its own user, test-mode memory, signed deploys
```

Report, on `main`:

```
TZ-55: report — the run lane on the 1 GB host
```
