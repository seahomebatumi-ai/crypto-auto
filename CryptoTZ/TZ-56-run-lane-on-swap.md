# TZ-56 — The run lane on swap: limits set at each start, every run its own measurement, every signed commit verified, the stream as the exchange answers it

**Canonical filename:** `CryptoTZ/TZ-56-run-lane-on-swap.md`
**Report:** `CryptoReports/TZ-56-run-lane-on-swap-report.md`
**Class:** branch TZ (contract §8) — it modifies files under `vps/**` and creates `.claude/settings.json`.
**Branch:** `tz-56-run-lane-on-swap` · **Model:** Opus
**Previous TZ:** TZ-55, merged at `2aaa74f` on 03.10.2026; its report is on `main`.
**Written against:** contract v26, map `2026-10-03-a`, methodology `2026-10-01-a`, TZ-55's report, and
the `vps` tree of `2aaa74f` (`43799ab742c8b4d67651cc3b07a0e6e31ee40e95`), read by the Architect from
the repository on 03.10.2026. Map §10 row «The assistant's build sequence», items (9) to (13) and the
decision of `2026-10-03-a`, is what this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-03-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-03-a.**` |
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
| `ANALYST-INSTRUCTIONS.md` | 3866 | `feaaffc99f983b3441ce205bcf1b6466` | reported |

The map itself: 3161 lines, MD5 `605e4f53306c7971b77b94c2e38207a1` — reported, not enforced. The tree
`origin/main:vps` is reported beside them; `43799ab742c8b4d67651cc3b07a0e6e31ee40e95` is the tree this
TZ was written against, and a different one is a finding, never a block.

---

## 1. Credentials

None arrives and none is written. The run unit keeps TZ-55's two (`claude-oauth-token`, `deploy-key`);
the Binance pair is read by A5's unit and D3's unit as systemd credentials and by nothing else. **This
session starts no `claude` process:** no step of this TZ runs an analysis, so the owner's account carries
nothing but this session.

---

## 2. Contract and map text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> each commit on `main`'s first-parent line that changed `vps/` since the commit the deployer last accepted — its own clone's `HEAD` — must carry GitHub's own signature

— contract §7 item 15.

> **Every commit, never the newest alone:** a signed merge's tree carries whatever reached `main` before it, so a check of the newest commit would install an unsigned change at the next legitimate merge.

— contract §7 item 15.

> it may start TRANSIENT units from its branch for a measurement its TZ names, and its report proves none is left behind.

— contract §7 item 15.

> **`.claude/settings.json` holds `"autoMemoryEnabled": false` and is the one Claude Code setting this repository carries**

— contract §2.

> the resident ceiling is set at each start from the host at that instant — what it frees less 64 MiB, in 16 MiB steps, never below 160 MiB and never above the budget — and the rest of the budget is the run's own swap

— map §10, row «The assistant's build sequence».

> a run starts when the host frees its ceiling plus 64 MiB and the free swap holds the rest.

— map §10, row «The assistant's build sequence».

> the bot's button and the watcher's requests are enabled before the fit is decided, the timers wait for one completed run

— map §10, row «The assistant's build sequence».

---

## 3. What is built

**A run starts on swap and never asks the owner to stop a service.** The budget stays TZ-55's measured
one; at each start, before the session, a step running as root reads what the host frees at that instant
and sets this run's resident ceiling to it, less a 64 MiB reserve, and its swap ceiling to the rest of the
budget — so the run's own pages go to swap before any other service's do. **Every run is its own
measurement:** its journal carries the limits it ran under, its cgroup's resident and swap peaks and its
token usage, so the fit is decided by the product's first completed run with no Claude session watching
it. The bot's button and the watcher's run requests are enabled; the timers are not. Around it: **the
deployer verifies every signed commit since the one it last accepted**, so an unsigned change can no longer
ride in on a later merge; **the announcement stream accepts the answer the exchange actually sends**,
read first; and **Claude Code's auto memory is off** for every session in this repository.

---

## 4. Scope

### Files to Modify

```
vps/common.py      vps/run.py        vps/announce.py    vps/deploy.sh      vps/selftest.py
vps/manifest       vps/units/crypto-run.service
```

### Files to Create

```
.claude/settings.json
```

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- transient units named `tz56-*`;
- the scratch directories `/var/tmp/tz56-vps`, `/var/tmp/tz56-state` and `/var/tmp/tz56-sig`, and inside
  `/var/tmp/tz56-state/gnupg` alone a throwaway signing key generated for V6 — all gone at the end;
- reading, never content: names, sizes, line counts and modification times under the `memory/`
  directories of this repository's own project directories (A4).

**No file of the owner's other projects is read or touched, no Claude session is stopped, and nothing
under `/etc/crypto-auto/`, `/srv/crypto-auto` or `/var/lib/cryptorun` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The fit.** No analysis run happens here. The first run after the merge — from the bot's button or a
  watcher request — is the measurement, and the TZ after it reads its journal, writes the record's `fits`
  and decides the timers (map §10).
- **`crypto-run.timer`.** It is never listed by this TZ.
- **`vps/memory-record.txt`** is TZ-55's measurement and is not edited.
- **`crypto-bot.service`, `crypto-exchange.service`, `crypto-cleanup.*`, `crypto-deploy.*`,
  `crypto-announce.service`, `crypto-run.path`, `crypto-run.timer`** — their unit files are unchanged;
  `bench.yml` is not touched.
- **Any order, any key with trading rights, the methodology.**

---

## 6. Rules — binding in every stage

1. **No `claude` process** is started by this session or by any unit it starts.
2. **Redaction.** `common.redact()` covers every credential a program loads; the reading script of A5
   prints no credential, no signature and no query string.
3. **The session's own network reads** are A5's two stream connections and D3, through the transient
   units named; nothing else.
4. **A challenge or a refusal is a reading** (`ANALYST-INSTRUCTIONS.md` §6).
5. **Atomic writes** (inv. 72) for every file a later reader treats as current.
6. **No new Russian text.** Any Russian string touched stays `\uXXXX` escapes.
7. **Python 3.12's standard library and bash only.** `gpg` is reached through `git verify-commit`,
   except V6's throwaway key, generated and used inside `/var/tmp/tz56-state/gnupg` alone.
8. **Time is UTC everywhere.**
9. **Every transient unit** is named `tz56-*`, runs with `MemoryAccounting=yes`, and is gone at the end.

---

## 7. Stage A — readings, no writes

- **A1.** Contract §4a steps 1–6, and the §5 gate against §0 including the added-files table.
- **A2. What TZ-55's merge put into effect:** `journalctl -u crypto-deploy.service --since 2026-10-03 -o
  cat` lines beginning `deploy:` or `install:`; `systemctl list-unit-files 'crypto-*'`; `systemctl
  is-active crypto-bot.service crypto-exchange.service`; `cat /var/lib/crypto-auto/deployed-vps-tree`
  beside `git -C /srv/crypto-auto rev-parse origin/main:vps`; `bash
  /usr/local/libexec/crypto-auto/deploy.sh --check`. **Known answers, derived from the Architect's read
  of `main` on 03.10.2026:** the marker reads `43799ab742c8b4d67651cc3b07a0e6e31ee40e95`, the tree of
  `2aaa74f`; the installed deployer prints `deploy: check commit=2aaa74fa7866145aab54c8295032ac4625ebbe28
  signed=yes` — `2aaa74f` is the newest first-parent commit that changed `vps/`, and it carries the
  signature of key `B5690EEEBB952194`.
- **A3. Tools:** `systemctl --version | head -1` — known answer `systemd 255`, map §10 item (1);
  `ls -A /run/systemd/system.control/ 2>/dev/null` — what runtime drop-ins exist before this TZ.
- **A4. The auto memory that existed** — reading only, never content: `find /root/.claude/projects
  /var/lib/cryptorun/.claude/projects -mindepth 2 -maxdepth 2 -type d -name memory`, kept only where
  the project directory's name begins `-root-crypto-auto` or `-var-lib-cryptorun-crypto-auto`; for each
  kept directory every file's name, size, line count and modification time. A file's text is never
  printed, read into the session or quoted.
- **A5. The stream, read before the program changes** — in `tz56-subscribe`: `MemoryAccounting=yes`,
  `RuntimeMaxSec=120`, `RemainAfterExit=yes`, `LoadCredential=` of the two Binance files, running
  `/usr/bin/python3 /var/tmp/tz56-state/subscribe-read.py`, a scratch script that imports
  `/var/tmp/tz56-vps/announce.py` and `common.py` — a copy of `main`'s `vps/`, made before Stage B —
  for `signed_query`, `STREAM_URL`, `TOPIC`, `SUBSCRIBE` and `load_credential`. Two connections, the
  second at least 5 s after the first closes, each opened exactly as `Stream.connect()` opens one — the
  signed query with `topic`, the key header, a 20 s timeout — and each read for 20 s:
  1. **connection 1 sends no command;**
  2. **connection 2 sends `SUBSCRIBE`** right after opening, as `connect()` does today.

  Per frame it prints `conn=<1|2> n=<i> t_ms=<since open> type=<type>` and, for a `COMMAND` frame,
  `subType=`, `data=` and `code=`; for any other frame its `type` and its length in bytes; a frame that
  is not JSON prints `type=non-json`. Nothing else of a frame is printed. **Outcomes, registered
  before the reading:**
  - **R1** — connection 1 receives a `COMMAND` frame with `subType` `REGISTER` and `data` `SUCCESS`:
    the topic in the signed query is the subscription. B3 takes branch R1.
  - **R2** — connection 1 receives no `COMMAND` frame, and connection 2 receives one with `subType`
    `SUBSCRIBE` and `data` `SUCCESS`: B3 takes branch R2.
  - **Anything else:** the announce scope is BLOCKED, the frames are the reading, and D3 does not run.

  **Derivation.** TZ-55 D3 received `REGISTER` / `SUCCESS` as the first `COMMAND` frame of a connection
  that had already sent `SUBSCRIBE`, so whether the signed query or the command produced it is unread;
  Binance's documentation shows only `SUBSCRIBE`'s answer. Each outcome follows from which connection
  carries the answer.

---

## 8. Stage B — the code, on the branch

### B1. `vps/common.py`

- `RECORD_PATH`, the `memory-record.txt` beside `common.py`, and `read_record(path=RECORD_PATH)` → a
  dict of the record's `name=value` lines, comments skipped — the one parser; `selftest.py` section M
  uses it.
- `start_limits(available_bytes, budget_bytes)` → `(memory_max, memory_swap_max)` by §12.2, the one
  implementation, built on `RESERVE_BYTES` and `MEMORY_MAX_FLOOR_BYTES`. `derive_limits` and
  `test_limits` stay as they are.

### B2. `vps/run.py`

1. **New mode `--limits`**, run as root by the unit's `ExecStartPre=` (§12.3) and doing nothing else:
   `MemAvailable` and `SwapFree` from `/proc/meminfo`; `budget_bytes` from `common.read_record()`;
   `common.start_limits(MemAvailable, budget_bytes)`; the unit's name, the last component of this
   process's own cgroup path in `/proc/self/cgroup`; then `systemctl set-property --runtime <unit>
   MemoryMax=<memory_max> MemorySwapMax=<memory_swap_max>`. It logs one line — `crypto-run: limits
   unit=<unit> mem_available=<n> swap_free=<n> budget=<n> memory_max=<n> memory_swap_max=<n>
   set=<exit code of systemctl, or - when it never ran>` — and **exits 0 whatever happened**: a failure
   leaves the pair already in force — §12.3's floor and the budget's rest, or the pair the last
   successful start set, which `--runtime` keeps until the host reboots — and the admission of step 2
   still holds the run to it. It reads no credential, consumes no request and touches no tree.
2. **Admission** (§12.2): `MemAvailable − RESERVE_BYTES` ≥ this unit's `memory.max` **and**, where its
   `memory.swap.max` is a number above 0, `SwapFree` ≥ that number. The poll, the 1 800 s and S6 are
   unchanged. The values of the poll that admitted — or of the last poll — are kept for §12.4.
3. **The third summary line** — §12.4, printed by `summary()` on every path, never carrying `result`.

### B3. `vps/announce.py` — the branch A5 chose

One pure function decides the answer: `answer_of(frames, sub_type)` takes an iterable of raw frames and
returns `(answer, pending, skipped)` — `answer` the first `COMMAND` frame whose `subType` equals
`sub_type`, or `None` when the frames end first; `pending` the raw non-`COMMAND` frames before it, kept
exactly as `pending` keeps them today; `skipped` the `COMMAND` frames of another `subType`, each logged
`announce: command answer <json, sorted keys>`. `Stream.connect()` feeds it the frames received until
its 20 s deadline and succeeds iff `answer` is not `None` and its `data` is `SUCCESS`. The log line
`announce: subscribe answer <json>` is unchanged.

- **R1:** `ANSWER_SUBTYPE = "REGISTER"`; `connect()` sends no command, and the `SUBSCRIBE` constant and
  its send are removed.
- **R2:** `ANSWER_SUBTYPE = "SUBSCRIBE"`; `connect()` sends `SUBSCRIBE` as today.

### B4. `vps/deploy.sh` — §12.5

### B5. `vps/selftest.py` — §12.6

### B6. `vps/units/crypto-run.service` — §12.3

### B7. `.claude/settings.json` — §12.7

`vps/manifest` is written at Stage E and at no other time.

---

## 9. Stage C — the limits, proved on the VPS

`/var/tmp/tz56-vps` is refreshed as a `0755 root:root` copy of the branch's `vps/` after Stage B, with
`/var/tmp/tz56-state/limits-read.py` beside it in the state directory: a script that prints only `uid=`,
and its own cgroup's `memory.max` and `memory.swap.max`.

- **C1. The probe**, `tz56-limits`: `User=cryptorun`, `Group=cryptorun`, `SupplementaryGroups=cryptoauto`,
  `MemoryAccounting=yes`, `MemoryMax=167772160`, `MemorySwapMax=536870912` — §12.3's pair —
  `RemainAfterExit=yes`, `ExecStartPre=-+/usr/bin/python3 /var/tmp/tz56-vps/run.py --limits`, and
  `ExecStart=/usr/bin/python3 /var/tmp/tz56-state/limits-read.py`. Collected: its journal, and
  `systemctl show tz56-limits -p MemoryMax -p MemorySwapMax -p Result -p ExecMainStatus`. **Known
  answers, derived from §12.2 and §12.3:** the `crypto-run: limits` line names
  `unit=tz56-limits.service` and `set=0`; the main process's `memory.max` and `memory.swap.max` equal that
  line's `memory_max` and `memory_swap_max`; their sum is the record's `budget_bytes`, 704 643 072;
  `memory_max` equals `common.start_limits(<its mem_available>, 704643072)[0]`, recomputed in the
  session; `uid` is not 0. **If `systemd-run` refuses the property, or any answer differs, the run
  scope is BLOCKED:** E1 lists no run line, and the deployer, the stream and the memory scopes go on.

---

## 10. Stage D — the stream, on the branch's code

- **D3.** Only under R1 or R2. TZ-55 D3's command with `tz56-` names — `announce.py --measure 10800 2
  --state-dir /var/tmp/tz56-state` from `/var/tmp/tz56-vps`, `RuntimeMaxSec=11100`,
  `RemainAfterExit=yes`, the Binance pair as credentials — beside a one-second sampler of TZ-55's
  form, rebuilt in `/var/tmp/tz56-state`. Started
  as soon as C1 is collected, collected last: exit status, the peaks, and its journal — the key's
  verdict, the subscribe answer, every `command answer` line, and per data message its `catalogName`,
  title, publish time, lag and match.

---

## 11. Stage E — decisions written into the branch

- **E1. `vps/manifest`:** always `crypto-deploy.timer`, `crypto-cleanup.timer`,
  `crypto-exchange.service` and `crypto-bot.service`; `crypto-run.path` when C1 met every known answer;
  `crypto-announce.service` when D3 exited 0; **never `crypto-run.timer`** (§5).
- **E2.** `python3 vps/selftest.py` green in every section.

---

## 12. Dictated blocks

### 12.1 Russian strings

None is added or changed.

### 12.2 The start limits and the admission

```
MiB             = 1 048 576 ; step = 16 MiB
budget          = budget_bytes of vps/memory-record.txt              # TZ-55's measurement
memory_max      = min(budget, max(160 MiB, floor((MemAvailable − 64 MiB) / step) × step))
memory_swap_max = budget − memory_max
admitted        ⇔ MemAvailable − 64 MiB ≥ memory.max
                  and (memory.swap.max is max, 0 or absent, or SwapFree ≥ memory.swap.max)
```

**Derivations.** 64 MiB and 160 MiB are TZ-55's `RESERVE_BYTES` and `MEMORY_MAX_FLOOR_BYTES`, unchanged,
with their recorded derivations. Setting the ceiling from the instant of the start is the owner's
decision of 03.10.2026 (map §10): the run takes what the host frees at that moment and nothing a service
holds, and the reserve moves into the admission so that a ceiling lifted to the floor is still never
started into the last 64 MiB.

**Known answers, computed by the Architect:**
`start_limits(535355392, 704643072)` = `(452984832, 251658240)` — TZ-55's `A0`, and its E1 pair;
`start_limits(240775168, 704643072)` = `(167772160, 536870912)`, admitted at once — TZ-55 attempt 3's
`MemAvailable` with the measuring session alive;
`start_limits(209678336, 704643072)` = `(167772160, 536870912)`, not admitted, because 209 678 336 −
67 108 864 = 142 569 472 < 167 772 160 — TZ-55 attempt 1's;
`start_limits(2147483648, 704643072)` = `(704643072, 0)`.

### 12.3 `vps/units/crypto-run.service` — exactly these lines

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
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
Environment=PYTHONDONTWRITEBYTECODE=1
Environment=DISABLE_AUTOUPDATER=1
Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
Environment="GIT_SSH_COMMAND=ssh -i %d/deploy-key -o IdentitiesOnly=yes -o UserKnownHostsFile=/var/lib/cryptorun/.ssh/known_hosts"
LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token
LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key
ExecStartPre=-+/usr/bin/python3 /srv/crypto-auto/vps/run.py --limits
ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/run.py
RuntimeDirectory=crypto-run
NoNewPrivileges=yes
CapabilityBoundingSet=
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/var/lib/cryptorun /var/spool/crypto-auto
MemoryAccounting=yes
MemoryMax=167772160
MemorySwapMax=536870912
RuntimeMaxSec=5400
OOMScoreAdjust=500
Nice=5
SuccessExitStatus=75
```

`MemoryMax=` is the floor and `MemorySwapMax=` the budget's rest, 704 643 072 − 167 772 160: the pair a
run keeps when the step before it fails on a host that has not yet run one. `-` makes that failure non-fatal and `+` runs the step as root,
outside the sandbox, because only root may set a unit's limits. `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` is
Claude Code's documented switch (code.claude.com/docs/en/memory); `.claude/settings.json` turns the same
feature off for every other session in the repository.

### 12.4 The run's third summary line

```
crypto-run: memory_max=<m> memory_swap_max=<m> mem_available=<n> swap_free=<n> memory_peak=<n> memory_swap_peak=<n> input_tokens=<n> output_tokens=<n> cache_read_tokens=<n> cache_creation_tokens=<n> cost_usd=<x>
```

- `memory_max`, `memory_swap_max`: this unit's own cgroup files when admission read them — a number,
  `max`, or `-` when unreadable.
- `mem_available`, `swap_free`: `/proc/meminfo` at the poll that admitted, or at the last poll.
- `memory_peak`, `memory_swap_peak`: this unit's own `memory.peak` and `memory.swap.peak`, read after the
  session ends, `-` when unreadable.
- the tokens: `result.json`'s `usage.input_tokens`, `usage.output_tokens`,
  `usage.cache_read_input_tokens` and `usage.cache_creation_input_tokens`; `cost_usd` is
  `total_cost_usd`. Integers and finite numbers only, `-` otherwise.

### 12.5 `vps/deploy.sh` — the range, in place of step 4's single commit

- **Step 4:** `base` = `git -C "$CLONE" rev-parse HEAD`; every commit `git -C "$CLONE" log
  --first-parent --format=%H "$base..origin/main" -- vps` lists is verified with `GNUPGHOME="$SIGNERS"
  git -C "$CLONE" verify-commit`. **Any one unverified** → log `deploy: unsigned vps commit <the newest
  unverified>, not installed`; S11 by TZ-55's `tell_once`; exit 1 — no fast-forward, no install. An
  empty list passes.
- **`--check [<clone> <gnupghome>]`:** with no argument, steps 2 and 4 on the deployer's clone as today;
  with both, no fetch and no lock, step 4 on `<clone>` with `<gnupghome>` as the signers. It prints
  `deploy: check base=<h> commits=<n> unsigned=<k> signed=<yes|no>`, exits 0 when `unsigned=0` and 1
  otherwise, and fast-forwards, writes and installs nothing.

Every other step is TZ-55 §12.9's, unchanged.

### 12.6 Selftest sections — changed and new

| Section | What it compares | Known answer and its source |
|---|---|---|
| J | `derive_limits`, `test_limits`, `start_limits` | TZ-54 §12.8's two answers, TZ-55 §12.4's four, §12.2's four; and `start_limits` never below 160 MiB nor above the budget on ten values from 0 to 4 GiB |
| M | `vps/memory-record.txt` against `crypto-run.service` and `vps/manifest` | TZ-55's record rules on the record's own terms, read by `common.read_record`; the unit's `MemoryMax=` equals `MEMORY_MAX_FLOOR_BYTES` and its `MemorySwapMax=` equals `budget_bytes` − that floor; `RuntimeMaxSec=` equals `runtime_max_s`; exactly one `ExecStartPre=-+/usr/bin/python3 /srv/crypto-auto/vps/run.py --limits` and one `Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`; the manifest lists `crypto-run.timer` only when `fits=yes` |
| O | `run.py` with a stub `claude` and a stub writer | TZ-55's checks; the stub's `usage` and `total_cost_usd` reach §12.4's line — `input_tokens=11 output_tokens=22 cache_read_tokens=33 cache_creation_tokens=44 cost_usd=0.5` — and `result` never does; admission at `MemAvailable` = `memory.max` + 64 MiB admits and at one byte less refuses |
| P | `announce.answer_of` on lists of frames, under the branch's `ANSWER_SUBTYPE` | R1: `REGISTER`/`SUCCESS` answers; `REGISTER`/`FAIL` answers and does not succeed; a `DATA` frame before the answer stays in `pending`; no frame gives `None`. R2: `REGISTER`/`SUCCESS` then `SUBSCRIBE`/`SUCCESS` answers with `REGISTER` in `skipped`; `REGISTER`/`SUCCESS` alone gives `None`; `SUBSCRIBE`/`FAIL` answers and does not succeed |
| Q | the repository's `.claude/settings.json` | valid JSON whose only key is `autoMemoryEnabled`, `false` |

Every other section is TZ-55's and stays green.

### 12.7 `.claude/settings.json` — exactly these lines

```
{
  "autoMemoryEnabled": false
}
```

---

## 13. Validation

- **V1. Selftest.** `python3 vps/selftest.py` after Stage E: exit 0, every section non-empty, the total
  printed. **Negative control** (inv. 68): one digit of a §12.2 known answer in section J changed in the
  working tree → exit non-zero with section J alone failing; reverted; green again, MD5 restored.
- **V2. Syntax.** `python3 -m py_compile` on every `vps/*.py`; `bash -n` on both scripts;
  `systemd-analyze verify` on every file of `vps/units/`, exit 0, warnings printed; `python3 -m
  json.tool .claude/settings.json`.
- **V3. Dry run.** `bash vps/install.sh --dry-run` prints `would enable --now crypto-run.path` and
  `would create /var/lib/crypto-auto/runs-enabled` exactly when E1 listed the path, and never
  `would enable --now crypto-run.timer`; `systemctl list-unit-files 'crypto-*'` reads the same before
  and after.
- **V4. The limits.** C1's journal and `systemctl show` lines against C1's known answers.
- **V5. The stream.** A5's frames; D3's verdict with its field booleans, the subscribe answer, every
  `command answer` line, every data message's `catalogName`, title, publish time and lag, pings,
  reconnects and the exit code.
- **V6. Signed deploys.**
  1. `bash vps/deploy.sh --check` from the branch, on the deployer's clone: `commits=0 unsigned=0
     signed=yes`, exit 0 — **derived:** no first-parent commit after `2aaa74f` changed `vps/` when the
     Architect read `main`; any commit that has since is printed with its `%G? %GK`.
  2. **The chain the old rule passed.** `/var/tmp/tz56-sig`: `git clone -q /srv/crypto-auto`.
     `/var/tmp/tz56-state/gnupg`: a copy of `/etc/crypto-auto/gnupg` plus a throwaway key —
     `gpg --batch --passphrase '' --quick-gen-key 'tz56 <tz56@invalid>' ed25519 sign never` with that
     `GNUPGHOME`. In the scratch clone, from its `HEAD` `B`: commit `X`, unsigned, adding
     `vps/tz56-probe.txt`; then commit `M` on `X`, signed with the throwaway key, changing that file;
     `git update-ref refs/remotes/origin/main M`; `git checkout -q --detach B`. Then: `bash
     vps/deploy.sh --check /var/tmp/tz56-sig /var/tmp/tz56-state/gnupg` prints `commits=2 unsigned=1
     signed=no`, exit 1; `GNUPGHOME=/var/tmp/tz56-state/gnupg git -C /var/tmp/tz56-sig verify-commit M`
     exits 0 — the newest commit alone, which TZ-55's rule read, verifies; and after `git checkout -q
     --detach X`, the same `--check` prints `commits=1 unsigned=0 signed=yes`, exit 0. **Derived from
     §12.5:** the range from `B` holds `M` and `X`, `X` unverified; from `X` it holds `M` alone.
  3. `cmp` of `/usr/local/libexec/crypto-auto/deploy.sh` with `git -C /srv/crypto-auto show
     origin/main:vps/deploy.sh` reports them identical — this session installed no deployer.
- **V7. Credentials.** The exact-value scan of TZ-55 V8 — `grep -c -F -f` with each of
  `binance-api-key`, `binance-api-secret` and `claude-oauth-token`, each proven first to hold one
  non-empty line — over this report, `git diff origin/main...HEAD`, every file under the branch's `vps/`
  and `.claude/`, and `journalctl -o cat -u 'tz56-*'`: every count 0.
- **V8. The memory that existed.** A4's listing as printed; no text of any file.
- **V9. Nothing left.** `systemctl list-units --all 'tz56-*'` empty; no `tz56-*` entry under
  `/run/systemd/system.control/` or `/run/systemd/transient/`; `/var/tmp/tz56-vps`, `/var/tmp/tz56-state`
  and `/var/tmp/tz56-sig` absent, the throwaway key with them; `systemctl list-unit-files 'crypto-*'`
  identical to A2's.
- **V10. No production file.** `git diff --name-only origin/main...HEAD` lists only `vps/` paths and
  `.claude/settings.json`.
- **V11. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main`
  receives nothing from this session but its report.

---

## 14. The report

Contract §10's template, with: A2's lines and both known answers; A3; A4's listing; A5's frames and the
outcome it selected; C1's journal and `systemctl show` lines; D3 as printed; E's manifest; V1–V11.
**The first line after `## Status` states whether a run will start on swap** — C1's `memory_max` and
`memory_swap_max` beside their sum — **and the second whether the announcement stream is enabled.**
No analysis answer exists in this TZ, so none is quoted.

---

## 15. Commit messages

Implementation, on the branch:

```
TZ-56: vps — the run on swap, each run its own measurement, every signed commit verified
```

Report, on `main`:

```
TZ-56: report — the run lane on swap
```
