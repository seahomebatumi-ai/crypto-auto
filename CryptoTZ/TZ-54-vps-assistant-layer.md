# TZ-54 — The assistant on the VPS: payload writer, run unit, Telegram bot, exchange watcher

**Canonical filename:** `CryptoTZ/TZ-54-vps-assistant-layer.md`
**Report:** `CryptoReports/TZ-54-vps-assistant-layer-report.md`
**Class:** branch TZ (contract §8) — it creates files under `vps/**` and modifies none.
**Branch:** `tz-54-vps-assistant-layer` · **Model:** Opus
**Previous TZ:** TZ-53, report-only; its report is on `main` and it had no branch.
**Written against:** contract v24, map `2026-10-01-e`, methodology `2026-10-01-a` and TZ-53's report
(this machine, 01.10.2026, 08:02–08:08Z). Map §10 rows «The assistant's build sequence» and «The
engine's exchange-announcement read is a path its own §6 forbids» are the decisions this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-01-e.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-01-e.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 929 | `7d7e335d1fc1871ca4404128da54a93d` | its version line reads `**Version 24.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `ANALYST-INSTRUCTIONS.md` | 3866 | `feaaffc99f983b3441ce205bcf1b6466` | reported |

The map itself: 3121 lines, MD5 `7cf5077bffbbcc321b97da389fd742bd` — reported, not enforced.

---

## 1. Credentials this TZ installs

| Name in the trigger message | File on the VPS | Read only by |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | `/etc/crypto-auto/credentials/telegram-bot-token` | `crypto-bot.service`; the one-shot units of C4 and D5 |
| `BINANCE_API_KEY` | `/etc/crypto-auto/credentials/binance-api-key` | `crypto-announce.service`; the one-shot unit of D3 |
| `BINANCE_API_SECRET` | `/etc/crypto-auto/credentials/binance-api-secret` | `crypto-announce.service`; the one-shot unit of D3 |
| — written by C4 | `/etc/crypto-auto/credentials/owner-chat-id` | `crypto-bot.service`; the one-shot unit of D5 |

- **They arrive in the trigger message**, one `NAME=value` line each under `EXECUTE TZ-54` (contract §7
  item 6). They are written at C2 and at no other step: the directory `0700 root:root`, each file
  `0600 root:root` holding the value exactly, with no trailing newline, written by a command that
  prints nothing. No value is echoed, displayed, logged or quoted anywhere, ever.
- **A name missing from the trigger message blocks the scopes that need it and nothing else**
  (contract §6): the token → C4, D5 and `crypto-bot.service`; either Binance name → D3 and
  `crypto-announce.service`.
- **Two owner preconditions**, which the report states as held or not: the bot was created in
  @BotFather and the owner sent `/start` to it before the trigger; the Binance key was created with
  reading only and restricted to this VPS's address.
- **The key's rights are read from the exchange before any stream is opened** (D3, §12.9). A key with
  any right beyond reading, or with no address binding, is refused: both Binance files are deleted, the
  announce scope is BLOCKED, and the report's first line says the key must be revoked in Binance.

---

## 2. Contract text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> **Never commit secrets.** Credentials live only in GitHub Actions environment variables (inv. 7), **with exactly two exceptions, both on the VPS and both since v24:**

— contract §7 item 6.

> **A value arrives once, from the Boss, in the trigger message of the TZ that names it** — one `NAME=value` line under the trigger line — and that message is the only place a credential is ever typed.

— contract §7 item 6.

> **A program in this repository that a VPS unit runs, and whose output that unit commits, has a workflow step's standing on the same terms** (inv. 44, since v24)

— contract §7 item 9.

> An implementation session never enables, starts or leaves running a persistent unit, timer or service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its report proves none is left behind.

— contract §7 item 15.

> It passes one of the three full-cycle strings, verbatim, as the prompt of a headless session, beside one appended system-prompt sentence that names this file as the session's contract; it passes nothing else

— contract §4.

> an implementation session that starts either for a measurement its TZ names never reads, relays or edits the answer that run publishes, and edits nothing it writes.

— contract §1.

> The rule is therefore one writer per artifact class — serialise the whole object BEFORE touching the filesystem, write a temporary file beside the target, rename it over, and on any failure remove both and re-raise.

— map §4, inv. 72.

> a daily timer keeps the newest records by age and count and removes the rest, every run removes its own scratch when it ends, and every run executes in its own unit under a `MemoryMax` set from the measured peak and under `RuntimeMaxSec`, so a run that overruns is stopped by the host and never takes the host down

— map §10, row «The assistant's build sequence».

> can write `analyst/live.json` in the Shortcut's own schema, committed and gated exactly as the Shortcut's payload is (inv. 44), and the engine keeps reading a file, never a host (§11)

— map §10, row «The engine runs only when the Boss types a trigger».

> **Bot protection is a refusal and is respected as one.** A host answering with a managed challenge has declined to serve this client; it is not an obstacle to route around, and no run attempts to.

— `ANALYST-INSTRUCTIONS.md` §6.

---

## 3. What is built

Four programs and their units, deployed from `main` by a deployer this session bootstraps. **The
writer** builds `analyst/live.json` from `fapi.binance.com` in the Shortcut's schema, proves it with
the unmodified gate, commits it and pushes it. **The run unit** runs the writer and then one headless
role-2 session, under a memory ceiling and a runtime ceiling set from this TZ's measurement, admitted
only when the host's available memory covers that ceiling, and hands the answer to an outbox. **The
bot** answers the owner's chat and nothing else, starts a run from one button and delivers the outbox.
**The exchange watcher** — `exchangeInfo` polled every 15 minutes and Binance's announcement stream
held on the read-only key — alerts, and requests a run on the conditions §8 names. A cleanup timer
keeps the run records and the spool bounded. The session measures a full run's memory and the stream
before anything relies on either, and writes what it measured into the branch as the run unit's
limits and as the manifest of what the deployer enables after the merge.

---

## 4. Scope

### Files to Create

```
vps/common.py          vps/writer.py          vps/run.py             vps/bot.py
vps/exchange.py        vps/announce.py        vps/cleanup.py         vps/selftest.py
vps/deploy.sh          vps/install.sh         vps/manifest           vps/memory-record.txt
vps/units/crypto-run.service       vps/units/crypto-run.timer       vps/units/crypto-run.path
vps/units/crypto-bot.service       vps/units/crypto-exchange.service vps/units/crypto-announce.service
vps/units/crypto-cleanup.service   vps/units/crypto-cleanup.timer
vps/units/crypto-deploy.service    vps/units/crypto-deploy.timer
```

### Files to Modify

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- the system user `cryptoauto` — no home, shell `/usr/sbin/nologin`;
- `/etc/crypto-auto/credentials/` (`0700 root:root`) and the four files of §1;
- `/var/spool/crypto-auto/outbox/` and `/var/spool/crypto-auto/requests/` (`2770 cryptoauto:cryptoauto`),
  `/var/lib/crypto-auto/` (`0750 cryptoauto:cryptoauto`), `/usr/local/libexec/crypto-auto/` (`0755 root:root`);
- the clone `/srv/crypto-auto` of `git@github.com:seahomebatumi-ai/crypto-auto.git` and its worktree
  `/srv/crypto-auto-run`, detached at `origin/main`;
- Ubuntu's `python3-websocket`, only where A6 finds `import websocket` failing;
- the deployer's bootstrap: `/usr/local/libexec/crypto-auto/deploy.sh` and
  `/etc/systemd/system/crypto-deploy.service` and `.timer`, the timer enabled — nothing else enabled;
- transient units named `tz54-*` and the staging directories `/var/tmp/tz54-vps` and
  `/var/tmp/tz54-state` for Stage D, all gone at the end (V10);
- removal of `/root/.claude/projects/-tmp-tz53-unit`, the record TZ-53's probe left (C5).

### On `main`, written by programs during Stage D

`analyst/live.json` by the writer, and `analyst/state.json` and `analyst/log/**` by the headless role-2
run D2 starts. **The session itself writes nothing under `analyst/`** (contract §1), and its only
direct push is its report.

---

## 5. What this TZ does not decide and does not build

- **The hunter's own schedule** — it follows the methodology edit that splits the hunter (map §10).
- **The watcher's regime and class-B conditions** — the state names neither a boundary nor a print's
  class and minute (map §10, row «The watcher has no calendar and no regime input»).
- **Admitting the announcement record to the method** — an Architect edit after this TZ's reading.
- **The six sentences** map §10 lists as false from this TZ's merge — an Architect edit after it.
- **The host's size.** §12.8's rule decides fit; the owner resizes; this TZ resizes nothing.
- **Any order, and any key with trading rights** (map §10, row «The engine places no order on the exchange»).
- **`bench.yml`** is not touched: `vps/selftest.py` runs in this session and in `install.sh` before
  every deployment, and a red selftest refuses the deployment.
- **The Shortcut** is unchanged and stays the manual path.

---

## 6. Rules — binding in every stage

1. **Credentials** follow §1. A program reads a credential only from `$CREDENTIALS_DIRECTORY`; the
   session reads a credential file only through a command that prints a count (V8).
2. **Redaction.** Every log line a program builds from an exception or a URL passes through
   `common.redact()`, which replaces each loaded credential value with `<redacted>`. The Bot API URL
   carries the token, so this is not optional.
3. **The session's own network reads** (A5, A9) use TZ-53's form: `curl -sS -L -m 20 -o <body> -D
   <headers> -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' '<url>'` — one
   request per URL, no retry, no user agent, header, proxy or cookie. Programs use Python's `urllib`
   with a 20 s timeout and no header but the one §12 names (`X-MBX-APIKEY`).
4. **A challenge or a refusal is a reading** (§2, methodology §6).
5. **Atomic writes** (inv. 72, §2) for every file a later reader treats as current:
   `analyst/live.json`, outbox and request files, the exchange snapshot, the perpetual list, the
   announcement record, the bot offset, the counters, the deployed-tree marker, the owner binding.
6. **Russian text in `vps/` code** is written as `\uXXXX` escapes, as hard floor item 7 requires of
   JavaScript, and equals §12.1 character for character.
7. **Python 3.12's standard library and bash only**, except `announce.py`, which imports `websocket`
   from Ubuntu's `python3-websocket`.
8. **Time is UTC everywhere**; Tbilisi time appears only inside alert text, through `zoneinfo`
   `Asia/Tbilisi`.
9. **One full analysis run is measured, once** (D2). A failed or killed run is the reading and is not
   repeated.
10. **Every transient unit** is named `tz54-*`, runs with `MemoryAccounting=yes`, and is gone at the end.

---

## 7. Stage A — readings, no writes

- **A1.** Contract §4a steps 1–6, and the §5 gate against §0 including the added-files table.
- **A2. What holds the memory**, read at one instant: `grep -E
  '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo`; the 25 processes with the largest
  `VmRSS` — pid, ppid, `comm`, the basename of `/proc/<pid>/exe`, elapsed time, `VmRSS`, `VmSwap`,
  cgroup — never their full command lines; every process whose `/proc/<pid>/exe` resolves to the
  binary TZ-53 read (`/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`) — pid, ppid,
  elapsed time, cwd, `VmRSS`, `VmSwap`, cgroup; and **the session tree** — the nearest ancestor of the
  stage's own shell whose `exe` resolves to that binary, plus every descendant of it — with its summed
  `VmRSS`. No such ancestor is a reading: it is stated, and §12.8's `A0` then takes `MemAvailable` alone.
- **A3. Disk and records:** `df -B1 /`; each top-level directory under `/root/.claude/projects/` with
  its entry count and bytes; `git -C /root/crypto-auto worktree list | wc -l`.
- **A4. The gate:** the lines of `analyst/live-gate.sh` stating how it is invoked, which files it reads
  and how it locates them, and its exit codes, quoted with their line numbers; then its own selftest,
  in the form its usage names, with the exit code and the count line.
- **A5. The payload's mapping:** the `c` rows of the committed `analyst/live.json`, read by command and
  never `x` in full, with its `ts`, `n` and `src`; `c[].s` against `tokens[].s` plus `BTCUSDT`, cut from
  `index.html` at run time — equal, or the writer's scope is BLOCKED. Then three reads under rule 3:
  `https://fapi.binance.com/fapi/v1/ticker/24hr`, `https://fapi.binance.com/fapi/v1/premiumIndex`, and
  `https://fapi.binance.com/fapi/v1/openInterest?symbol=<s>` for each `c` symbol, one at a time. Then
  §12.6's derivation table, printed in full.
- **A6. Tools:** the lines of `claude --help` naming `--model`, `--allowedTools`,
  `--append-system-prompt` and `--output-format`, quoted; `python3 -c 'import websocket;
  print(websocket.__version__)'`; `apt-cache policy python3-websocket` (`Installed` and `Candidate`);
  `git -C /root/crypto-auto config --get user.name` and `user.email`, printed only as set or unset;
  `id cryptoauto`, expected absent.
- **A7. What a headless session loads besides its prompt:** for `/root/.claude/CLAUDE.md` and the
  repository root's `CLAUDE.md` — present or absent, lines, MD5, and `grep -c EXECUTOR-INSTRUCTIONS`;
  for `/root/.claude/settings.json` — present or absent, and its top-level key names only.
- **A8.** This session's `PATH`, printed. It is the run unit's `PATH`.
- **A9. The Bot API page**, one read under rule 3 of `https://core.telegram.org/bots/api`: the sentence
  giving `sendMessage`'s `text` limit and the «HTML style» rules — tags and escaping — quoted. §12.3's
  chunk limit is that `text` limit minus 96.

---

## 8. Stage B — the code, on the branch

### B1. `vps/common.py`

Paths and the shared helpers, and nothing else: `atomic_write(path, data)` (rule 5);
`write_outbox(kind, text)` — `kind` ∈ `answer · alert · notice`, one JSON file
`{"kind","text","created_ms"}` named `<created_ms>-<kind>-<pid>.json`; `redact(text)` (rule 2);
`load_credential(name)` — the file under `$CREDENTIALS_DIRECTORY`, surrounding whitespace stripped;
`cut_tokens(index_html)` — every `{name:'…', s:'…'[, fut:true]}` inside `var tokens = [ … ];`, failing
non-zero on zero rows (inv. 22); `derive_limits(footprint_bytes, duration_s)` (§12.8, the one
implementation); `runs_enabled()` — `/var/lib/crypto-auto/runs-enabled` exists; `run_active()` —
`/run/crypto-run` exists; `request_run(source)` — writes one `.req` file into the requests directory
when `runs_enabled()`, and for `source == 'watcher'` first takes a `flock`-guarded count in
`/var/lib/crypto-auto/run-requests-<UTC date>` and refuses past **6 a day** [Architect's decision: a
budget on the owner's subscription, not a statistic]; the bot's requests are uncapped.

### B2. `vps/writer.py` — `--tree <dir>`

1. Reads, one at a time, with rule 3's client limits: the bulk `ticker/24hr`, the bulk
   `premiumIndex`, and `openInterest` for each `c` symbol.
2. Builds the payload. **Top-level keys exactly `c`, `n`, `src`, `ts`, `x`.** `x` is the bulk ticker
   response, every row verbatim, in served order. `c` is one row per symbol of `BTCUSDT` followed by
   `tokens[].s` in `tokens[]` order, keys exactly `chg fr h l mark oi p qv s`, each value the verbatim
   string of the source field §12.6's derivation mapped it to, and `s` the symbol — `p`, `h`, `l`,
   `chg` and `qv` from the same bulk ticker as `x`. `n` is `len(c)`, the only number; `src` is `"fapi"`;
   `ts` is the moment the bulk ticker response completed, UTC, `YYYY-MM-DDTHH:MM:SS+00:00`. A symbol
   missing from any source writes no payload at all — never a partial row.
3. Writes `<tree>/analyst/live.json` atomically and runs the gate in `<tree>` exactly as A4 read its
   invocation. Exit 0 → commit `analyst: live.json (vps)` and `git push origin HEAD:main`; one rejection
   → `git pull --rebase` and push again; a rebase conflict → abort it and drop the writer's commit (the
   payload on `main` is gated on `ts` like this one, contract §8). Non-zero → the file is restored from
   `HEAD` and nothing is committed.
4. Prints one line, `writer: gate_exit=<n> committed=<yes|no> pushed=<yes|no> rows_c=<n> rows_x=<n>`,
   and never a value. Exit 0 pushed · 3 gate refused · 4 read or build failed · 5 push failed twice.

### B3. `vps/run.py` — `--tree <dir>` (default `/srv/crypto-auto-run`)

1. **Consume every request file first**, before anything that can fail, so a path unit cannot loop.
2. **Admission.** Read this unit's own `memory.max` from its cgroup; `max` means no ceiling (D2).
   Wait until `MemAvailable` ≥ that ceiling, reading `/proc/meminfo` every 30 s for at most 1 800 s;
   never admitted → outbox notice S6, exit 75.
3. **Tree.** Under `flock /run/lock/crypto-auto-git.lock`: `git fetch origin main`; commits on `HEAD`
   absent from `origin/main` are logged by subject; `git reset --hard origin/main`; `git clean -fdx`.
4. **Writer** — `writer.py --tree <dir>` from run.py's own directory; any exit continues the run, and
   the gate inside the session decides as always.
5. **The headless session**, §12.2's command exactly, cwd `<dir>`, stdout to
   `$RUNTIME_DIRECTORY/result.json`.
6. **The result.** `is_error` false and a non-empty `result` → outbox `answer` holding `result`
   verbatim; anything else → outbox notice S7.
7. **Scratch.** `git clean -fdx` and `git checkout -- .` in `<dir>`; commits stay where the session put them.
8. One line: `crypto-run: requests=<n> admitted=<yes|no> waited_s=<n> writer_exit=<n> claude_exit=<n>
   is_error=<true|false> num_turns=<n> duration_ms=<n> denials=<n> answer_chars=<n>` — never the answer.

### B4. `vps/bot.py`

- **Service** (default): long poll `getUpdates` with `timeout=10`, `allowed_updates=["message"]`, the
  offset kept atomically in `/var/lib/crypto-auto/bot-offset`; every update passes §12.4's filter;
  between polls it sends the outbox oldest first (§12.3), deleting a file only once every chunk was
  accepted and rewriting it atomically with the unsent chunks after a partial send. HTTP 400 on a chunk
  → that chunk once more as plain text with no `parse_mode`; 429 → wait `retry_after`; a network error
  → keep the file and back off up to 60 s. Chunks at least 1 s apart. Every reply to an owner command
  carries the persistent reply keyboard of §12.1's button.
- **`--bind`**: `getMe`; one `getUpdates` with `timeout=0`; the private chats whose message text is
  `/start`. Exactly one distinct chat → its id written atomically to
  `/etc/crypto-auto/credentials/owner-chat-id` (`0600 root:root`), the read confirmed with
  `offset = highest update_id + 1`, and S9 sent there. Zero or several → nothing written, exit 3.
  Prints `bind: getme=<ok|failed> username=<bot username> updates=<n> start_chats=<n> bound=<yes|no>
  confirm_sent=<yes|no>` — never the chat id.
- **`--send-outbox-once`**: sends every outbox file once and prints per file `kind`, chunks, accepted,
  plain fallbacks, message ids received; exit 0 only when every chunk was accepted.

### B5. `vps/exchange.py` — `--once`, `--state-dir <dir>` (default `/var/lib/crypto-auto`)

Every 900 s (once with `--once`): `GET https://fapi.binance.com/fapi/v1/exchangeInfo`. The snapshot is,
per symbol whose `quoteAsset` is `USDT`, `[status, contractType, deliveryDate, onboardDate]`; a
`deliveryDate` whose UTC date is 2100-12-25 means none (TZ-53, C5). The first poll stores a baseline
and alerts nothing; each later poll compares with the stored one:

| Change | List symbol (`tokens[].s` or `BTCUSDT`) | Any other symbol |
|---|---|---|
| a `PERPETUAL` symbol that was absent | — | alert A2 |
| `deliveryDate` set to a date | alert A3 + `request_run('watcher')` | alert A3 if `PERPETUAL` |
| `status` changed | alert A4 + `request_run('watcher')` | logged count only |

It writes the snapshot and `perpetuals.json` — the sorted bases of `TRADING` `PERPETUAL` `USDT`
symbols, a leading run of digits removed (`1000PEPE` → `PEPE`) — atomically, both in the state
directory. `--once` prints counts — symbols, `USDT`, trading perpetuals, and changes by row of the table.

### B6. `vps/announce.py` — `--measure <seconds> <max_data>`, `--state-dir <dir>`

1. **Key check first** (§12.9): signed `GET https://api.binance.com/sapi/v1/account/apiRestrictions`
   with `X-MBX-APIKEY`; REFUSED → print the field names with their booleans, exit 3, no stream.
2. **Stream** (§12.10): connect to `wss://api.binance.com/sapi/wss` with the signed query and the
   header, send `{"command":"SUBSCRIBE","value":"com_announcement_en"}` and record the answer; a ping
   frame every 30 s; a fresh connection before 23 h 30 min; after a close, reconnect at 5 s doubling to
   300 s and never twice inside 5 s.
3. **Each `DATA` message**: the inner `data` string parsed; `catalogId`, `catalogName`, `publishDate`,
   `title`, `body`, `disclaimer`. The record `{received_ms, catalogId, catalogName, publishDate, title,
   body}` is added to `announcements.jsonl` in the state directory, the file rewritten atomically.
4. **Action** by §12.5's matcher: a list match → alert A1, plus `request_run('watcher')` when
   `catalogName` contains `listing` (case-insensitive, so «Delisting» too); a perpetual match in such a
   catalogue → alert A1 + `request_run('watcher')`; anything else is recorded only.
5. **`--measure`**: the key check, the stream, no outbox and no requests; per message it prints
   `catalogName`, `title`, publish time UTC, the lag from `publishDate` to receipt in ms and the match
   class; it stops after `<max_data>` messages or `<seconds>`, prints pings sent, reconnects and close
   codes, and exits 0 when at least one message carried all six fields, 2 when none did, 3 on a refused
   key, 4 when connecting or subscribing failed.

### B7. `vps/cleanup.py` — `--dry-run`

The run records: the directory D2 creates under `/root/.claude/projects/` — the reading taken after D2
names it — whose top-level entries are kept only while among the newest 40 by mtime **and** younger
than 14 days [Architect's decision: about 20 runs, two weeks]. The spool: outbox files older than
7 days, request files older than 1 day. `announcements.jsonl`: records whose `publishDate` is older
than 30 days, the file rewritten atomically. No other directory under `/root/.claude/` and no worktree
is touched. `--dry-run` prints what would be removed and removes nothing.

### B8. `vps/deploy.sh`

1. `/run/crypto-run` exists → exit 0, the tick skipped.
2. Under `flock /run/lock/crypto-auto-git.lock`: `git -C /srv/crypto-auto fetch origin main`; read
   `git -C /srv/crypto-auto rev-parse origin/main:vps` — absent → log `deploy: no vps tree on origin/main`;
   then `git -C /srv/crypto-auto merge --ff-only origin/main`.
3. The `vps` tree hash differs from `/var/lib/crypto-auto/deployed-vps-tree` → run
   `/srv/crypto-auto/vps/install.sh`; success → write the hash there atomically; failure → outbox notice
   S10 and exit 1.

### B9. `vps/install.sh` — default, `--bootstrap`, `--dry-run`

- **Default**, called by the deployer from `/srv/crypto-auto`: `python3 vps/selftest.py` — red → exit 1;
  provision idempotently (user, directories, worktree); `systemd-analyze verify` on every file of
  `vps/units/` — red → exit 1; install each into `/etc/systemd/system/` with mode `0644`, remove any
  `crypto-*` unit there that `vps/units/` no longer carries, `systemctl daemon-reload`;
  `systemctl enable --now` each unit `vps/manifest` lists and `disable --now` each `crypto-*` unit it
  does not; restart the enabled services so they load the new code; copy `vps/deploy.sh` to
  `/usr/local/libexec/crypto-auto/deploy.sh`; create `/var/lib/crypto-auto/runs-enabled` when the
  manifest lists `crypto-run.path`, and remove it when it does not.
- **`--bootstrap`**, called once by this session from the branch: the user, the directories, the clone
  and the worktree; `deploy.sh` copied; `crypto-deploy.service` and `.timer` installed;
  `systemctl daemon-reload`; `systemctl enable --now crypto-deploy.timer`. Nothing else.
- **`--dry-run`**: prints what the default mode would install, remove, enable and disable, and changes nothing.

### B10. `vps/selftest.py`

The sections of §12.14, each printing `section <X>: checks <n> failed <m>`, then the total. Exit
non-zero on any failure **and on any section that compared nothing** (inv. 22).

### B11. Units, manifest and record

`vps/units/` holds §12.12 exactly. `vps/memory-record.txt` and `vps/manifest` are written at Stage E
and at no other time.

---

## 9. Stage C — provisioning on the VPS

- **C1.** `apt-get install -y python3-websocket` only when A6's import failed; its version is recorded.
- **C2.** The credential files of §1 (rule 1).
- **C3.** `bash vps/install.sh --bootstrap` from the branch.
- **C4.** `systemd-run --unit=tz54-bind --wait --collect -p MemoryAccounting=yes -p
  LoadCredential=telegram-bot-token:/etc/crypto-auto/credentials/telegram-bot-token /usr/bin/python3
  /var/tmp/tz54-vps/bot.py --bind`, where `/var/tmp/tz54-vps` is a copy of the branch's `vps/`
  (`0755 root:root`) made for Stage C and D, because the worktree under `/root` is not a path a unit
  should run from.
- **C5.** `rm -rf /root/.claude/projects/-tmp-tz53-unit`.
- **C6.** The deployer's first tick, at most 7 minutes after C3: its journal line reads
  `deploy: no vps tree on origin/main`, and `systemctl list-unit-files 'crypto-*'` lists exactly
  `crypto-deploy.service` and `crypto-deploy.timer`.

---

## 10. Stage D — measurements in transient units started from the branch

In this order: D3 is **started** first, because it holds up to three hours; then D1, D2, D5 and D4;
then D3 is collected.

- **D3. The key and the stream:** `systemd-run --unit=tz54-announce -p MemoryAccounting=yes -p
  RuntimeMaxSec=11100 -p LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key
  -p LoadCredential=binance-api-secret:/etc/crypto-auto/credentials/binance-api-secret
  /usr/bin/python3 /var/tmp/tz54-vps/announce.py --measure 10800 2 --state-dir /var/tmp/tz54-state`,
  not waited on. Collected at the end: exit status, `MemoryPeak`, and its journal through
  `journalctl -u tz54-announce -o cat`.
- **D1. The instrument's known answer:** `systemd-run --unit=tz54-hog -p MemoryAccounting=yes -p
  OOMScoreAdjust=500 -p Nice=10 /usr/bin/python3 -c "<§12.7's hog>"`, sampled by §12.7.
  `F_hog` ≥ 100 663 296 bytes, or the instrument is broken: D2 does not run and the decision scope is
  BLOCKED.
- **D2. One full analysis run.** First, at one instant, `MemAvailable` and the session tree's summed
  `VmRSS` (A2's method). Then, not waited on: `systemd-run --unit=tz54-run -p
  WorkingDirectory=/srv/crypto-auto-run -p Environment=HOME=/root -p Environment=PATH=<A8> -p
  Environment=PYTHONDONTWRITEBYTECODE=1 -p RuntimeDirectory=crypto-run -p PrivateTmp=yes -p
  InaccessiblePaths=-/etc/crypto-auto/credentials -p MemoryAccounting=yes -p RuntimeMaxSec=5400 -p
  OOMScoreAdjust=500 -p Nice=10 /usr/bin/python3 /var/tmp/tz54-vps/run.py --tree /srv/crypto-auto-run`,
  sampled by §12.7 until it is inactive. Then `systemctl show tz54-run -p Result -p ExecMainStatus -p
  ExecMainStartTimestampMonotonic -p ExecMainExitTimestampMonotonic -p MemoryPeak -p MemorySwapPeak`,
  then `systemctl reset-failed tz54-run` where it is still listed. `D` is the exit timestamp minus the
  start timestamp, in seconds. The `crypto-run:` and `writer:` lines come from `journalctl -u tz54-run
  -o cat`. Then `git -C /srv/crypto-auto fetch origin main` and `git -C /srv/crypto-auto log
  origin/main --since=<D2 start> --format='%h %s'` — subjects only — and the name of the directory the
  run created under `/root/.claude/projects/` with its entry count, which fixes B7's target.
- **D5. Delivery**, at once after D2: `systemd-run --unit=tz54-send --wait --collect -p
  MemoryAccounting=yes -p LoadCredential=telegram-bot-token:/etc/crypto-auto/credentials/telegram-bot-token
  -p LoadCredential=owner-chat-id:/etc/crypto-auto/credentials/owner-chat-id /usr/bin/python3
  /var/tmp/tz54-vps/bot.py --send-outbox-once`. Without the token or the binding, the outbox file D2
  wrote is deleted unsent, and the report says so.
- **D4. The exchange lane:** `exchange.py --once --state-dir /var/tmp/tz54-state` in `tz54-exch-1`, and
  again at least 60 s later in `tz54-exch-2`, each with `--wait --collect -p MemoryAccounting=yes`;
  counts and `MemoryPeak` of each.

---

## 11. Stage E — decisions written into the branch

- **E1. Fit**, by §12.8 from D1 and D2.
- **E2.** `vps/memory-record.txt` in §12.13's form; `crypto-run.service`'s `MemoryMax=` and
  `RuntimeMaxSec=` set to the record's `memory_max_bytes` and `runtime_max_s`.
- **E3. `vps/manifest`**, one unit per line: always `crypto-deploy.timer`, `crypto-cleanup.timer`,
  `crypto-exchange.service`; `crypto-bot.service` when C4 bound the owner; `crypto-announce.service`
  when D3 exited 0; `crypto-run.timer` and `crypto-run.path` when the record says `fits=yes`.
- **E4.** B7's run-record directory set to the name D2's reading gave.
- **E5.** `python3 vps/selftest.py` green with every section, M included.

---

## 12. Dictated blocks

### 12.1 Russian strings — character for character

| Id | Where | Text |
|---|---|---|
| S1 | the keyboard's one button | «▶ Анализ рынка» |
| S2 | reply to `/start` | «Готов. Кнопка внизу запускает анализ рынка.» |
| S3 | run requested | «Анализ запущен — ответ придёт сюда.» |
| S4 | a run is already active | «Анализ уже идёт — ответ придёт сюда.» |
| S5 | `runs_enabled()` false | «Запуск с сервера пока выключен.» |
| S6 | not admitted after 1 800 s | «Анализ не запущен: память сервера занята другой сессией.» |
| S7 | the session failed | «Анализ не завершён.» |
| S8 | any other owner text | «Команда одна: ▶ Анализ рынка» |
| S9 | binding confirmed | «Связь с сервером установлена.» |
| S10 | deployment refused | «Обновление сервера не установлено: самопроверка не прошла.» |
| A1 | announcement | «⚡ Binance · {ЧЧ:ММ} Тбилиси · {catalogName}: {title}» |
| A2 | new perpetual | «⚡ Binance Futures · {SYMBOL}: новый контракт» |
| A3 | delivery date set | «⚡ Binance Futures · {SYMBOL}: дата делистинга {ДД.ММ.ГГГГ}» |
| A4 | status changed | «⚡ Binance Futures · {SYMBOL}: статус {OLD} → {NEW}» |
| R1 | second alert line, run requested | «→ анализ запущен» |
| R2 | second alert line, daily cap reached | «→ лимит запусков на сегодня исчерпан» |

`/run` and S1's text request a run: S5 when runs are disabled, S4 when `run_active()`, otherwise
`request_run('bot')` and S3. `/start` → S2. Any other owner text → S8.

### 12.2 The headless session

```
claude -p "ANALYZE TODAY'S CRYPTO MARKET AND DETERMINE THE STRATEGY FOR ENTERING ALTCOINS ON BINANCE FUTURES." \
  --output-format json --model opus \
  --allowedTools "Bash Read Write Edit Glob Grep WebSearch WebFetch" \
  --append-system-prompt "Read EXECUTOR-INSTRUCTIONS.md at the repository root in full before anything else: it is your contract, and the user message is a trigger from its §4."
```

The appended text is one sentence that names the contract, as contract §4 requires, and the prompt is
the production trigger verbatim; what happens to the final message is contract §4's, not the prompt's.

`--model opus` stays only where A6 found `--model` in the help; otherwise it is dropped and the report
says so. The tool list takes the separator A6's help line names. Nothing else is added.

### 12.3 Telegram text

Conversion, line by line, in this order: a maximal run of lines whose first non-space character is `|`
becomes one `<pre>…</pre>` holding those lines escaped and nothing more; every other line has `&`, `<`
and `>` escaped, then a line matching `^#{1,6} (.+)$` becomes `<b>` + the rest with every `**` removed
+ `</b>`, and in any other line each non-overlapping `**text**` becomes `<b>text</b>` while an unpaired
`**` stays as it is. Sent with `parse_mode` `HTML` and link previews disabled.

Chunking: the units are the lines and the `<pre>` blocks; a unit's visible length is its length with
tags removed and `&lt;` `&gt;` `&amp;` read as one character each, plus one for the joining newline.
Units are packed in order while a chunk's visible length stays within the limit A9 derives; a `<pre>`
block longer than the limit is split at its own line breaks into several blocks; a longer plain line is
cut in its source text before conversion. Chunks that are empty or blank are dropped. A chunk's plain
fallback is its source lines unconverted.

Known answers — derived by applying the rules above, and probed by the Architect:

```
input:
Время анализа: 10:00 Тбилиси · 06:00 UTC · 02:00 ET · Binance Futures

# РЕЖИМ
**ДИАПАЗОН** — альты без направления.
## **СТАТУС** ок

| Монета | Вход |
|---|---|
| SOL | $150 |

R&D <тест> **не** закрыт **

expected:
Время анализа: 10:00 Тбилиси · 06:00 UTC · 02:00 ET · Binance Futures

<b>РЕЖИМ</b>
<b>ДИАПАЗОН</b> — альты без направления.
<b>СТАТУС ок</b>

<pre>| Монета | Вход |
|---|---|
| SOL | $150 |</pre>

R&amp;D &lt;тест&gt; <b>не</b> закрыт **
```

With the limit at 4 000, fifty plain lines of 100 characters split 39 + 11, because `101·n − 1 ≤ 4000`
holds up to `n = 39`.

### 12.4 Owner filter

An update acts only when `message.chat.type` is `private`, `message.chat.id` equals the bound id, and
`message.date` is at most 600 s old at receipt; every other update is dropped with no reply and counted.
Known answers, `now` the fixture's clock:

| Update | Expected |
|---|---|
| private, owner, now, `/start` | S2 |
| private, owner, now, «▶ Анализ рынка» | request |
| private, another id, now, `/start` | dropped |
| private, owner, now − 601 s, `/run` | dropped |
| group, owner's id, now, `/run` | dropped |
| private, owner, now, «привет» | S8 |

### 12.5 Title matcher

A ticker matches when it stands in the title as a whole word — the character before and after it is
not `[A-Za-z0-9]` — case-sensitively, or when its full perpetual symbol does; a ticker of one character
matches only as `(X)`. List tickers are `tokens[].name` and `BTC`; perpetual tickers come from
`perpetuals.json`, whose bases already dropped a leading run of digits, while the full symbol keeps
it. A list match wins over a perpetual match. Known answers, with `PEPE` (from `1000PEPEUSDT`) and `S`
among the perpetuals:

| Title | Match |
|---|---|
| Binance Will List Hyperliquid (HYPE) with Seed Tag Applied | list HYPE |
| Binance Futures Will Launch USDⓈ-Margined SUIUSDT Perpetual Contract | list SUI |
| Introducing ETHFI on Binance Launchpool | none |
| Binance Adds ARB/EUR Trading Pair | list ARB |
| LITHIUM Network Airdrop Notice | none |
| Binance Will List Pepe (PEPE) | perpetual PEPE |
| Notice on S Token Migration | none |
| Binance Will Delist Sonic (S) | perpetual S |

### 12.6 The payload's derivation

| `c` field | Candidates |
|---|---|
| `p` | ticker `lastPrice` |
| `h` · `l` | ticker `highPrice` · ticker `lowPrice` |
| `chg` | ticker `priceChangePercent` · ticker `priceChange` |
| `qv` | ticker `quoteVolume` · ticker `volume` |
| `mark` | premiumIndex `markPrice` |
| `fr` | premiumIndex `lastFundingRate` |
| `oi` | openInterest `openInterest` |

Per row, `sig(v)` is the count of digits after the decimal point of the string `v`, zero when it has
none. A candidate is admissible for a field when `sig` of the committed `c` value equals `sig` of the
candidate's fresh value **on every row**. Among admissible candidates the field takes the one with
the smallest median over rows of `|log10(c/candidate)|` for `p h l qv mark oi` and of `|c − candidate|`
for `chg fr`. No admissible candidate, or two at an equal median → the writer's scope is BLOCKED with
the table printed. The printed table carries, per field and candidate, the rows whose `sig` matched and
the median.

### 12.7 The memory instrument

Every second until the unit is inactive, from `/sys/fs/cgroup/system.slice/<unit>.service/`:
`memory.current`, `memory.swap.current`, and for every pid in `cgroup.procs` its `VmRSS`, `VmHWM` and
`VmSwap`; with `MemAvailable` and `SwapFree` from `/proc/meminfo`. `F_run` is the largest
`memory.current + memory.swap.current` of any second; `P_run` is the sum over every pid ever seen of
its largest `VmHWM`; `F = max(F_run, P_run)`. The kernel's `MemoryPeak` and `MemorySwapPeak` are
printed beside them. The hog of D1:

```
import time; b = bytearray(100663296); [b.__setitem__(i, 1) for i in range(0, len(b), 4096)]; time.sleep(10)
```

### 12.8 Limits and fit

```
MiB = 1 048 576
memory_max_bytes = ceil(1.5 × F / (16 MiB)) × 16 MiB
runtime_max_s    = max(ceil(2 × D / 300) × 300, 3600) + 1800      # 1 800 s is B3's admission wait
A0               = MemAvailable + the session tree's summed VmRSS, read at one instant before D2
fits             = D2 completed  and  memory_max_bytes ≤ A0
completed        = Result=success, ExecMainStatus=0, is_error false, result non-empty
```

**A run that does not fit is answered by 2 vCPU and 4 GB, never by a GitHub runner** (map §10). Known
answers, computed by the Architect: `derive_limits(400 MiB, 1200 s)` = `(637534208, 5400)`;
`derive_limits(100 MiB, 2100 s)` = `(167772160, 6000)`.

### 12.9 The key's rights

`GET https://api.binance.com/sapi/v1/account/apiRestrictions?recvWindow=5000&timestamp=<ms>&signature=<hex>`
with `X-MBX-APIKEY` (developers.binance.com, «Get API Key Permission (USER_DATA)», weight 1). ACCEPTED
only when `ipRestrict` is true, `enableReading` is true, and every other field whose name begins with
`enable` or `permits` is false — `enableFixReadOnly` alone may take either value. A field nobody has
seen yet is covered by the same rule, in the safe direction. Known answers: the page's own example
response → REFUSED (`ipRestrict` false, `enablePortfolioMarginTrading` true); the same with `ipRestrict`
true and `enablePortfolioMarginTrading` false → ACCEPTED; that plus `"enableFoo": true` → REFUSED; the
accepted one with `enableReading` false → REFUSED.

### 12.10 Signing and the stream

The query string is the parameters sorted by name and joined `name=value` with `&`, and the signature
is HMAC-SHA256 of exactly that string under the secret, as lowercase hex, appended as `&signature=`.
Sorting makes the documentation's stated rule and the order sent one and the same (developers.binance.com,
«Announcements», general info, last modified 01.10.2026). The stream's parameters are `random` (32 hex
characters), `recvWindow=60000`, `timestamp` and `topic=com_announcement_en`. The subscribe answer the
page documents is `{"type":"COMMAND","data":"SUCCESS","subType":"SUBSCRIBE","code":"00000000"}`.
Known answers: `random=abc`, `recvWindow=5000`, `timestamp=1700000000000`, `topic=com_announcement_en`
→ `random=abc&recvWindow=5000&timestamp=1700000000000&topic=com_announcement_en`; and the signing
function with key `Jefe` over `what do ya want for nothing?` →
`5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843` (RFC 4231, test case 2).

### 12.11 Cleanup's known answer

Forty-five entries `e00`…`e44` aged 0…44 hours and three `o15`, `o16`, `o20` aged 15, 16 and 20 days:
kept `e00`…`e39`, removed `e40`…`e44`, `o15`, `o16`, `o20`.

### 12.12 Units — exactly these lines

```
# crypto-run.service
[Unit]
Description=Crypto assistant: one headless analysis run
Wants=network-online.target
After=network-online.target
StartLimitIntervalSec=600
StartLimitBurst=3

[Service]
Type=exec
WorkingDirectory=/srv/crypto-auto-run
Environment=HOME=/root
Environment=PATH=<A8>
Environment=PYTHONDONTWRITEBYTECODE=1
ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/run.py
RuntimeDirectory=crypto-run
PrivateTmp=yes
InaccessiblePaths=-/etc/crypto-auto/credentials
MemoryAccounting=yes
MemoryMax=<E2>
MemorySwapMax=0
RuntimeMaxSec=<E2>
OOMScoreAdjust=500
Nice=5
SuccessExitStatus=75

# crypto-run.timer
[Unit]
Description=Crypto assistant: scheduled analysis runs

[Timer]
OnCalendar=*-*-* 06:00:00 UTC
OnCalendar=*-*-* 14:30:00 UTC
Persistent=true
Unit=crypto-run.service

[Install]
WantedBy=timers.target

# crypto-run.path
[Unit]
Description=Crypto assistant: a run requested by the bot or the watcher

[Path]
PathExistsGlob=/var/spool/crypto-auto/requests/*.req
Unit=crypto-run.service

[Install]
WantedBy=paths.target

# crypto-bot.service
[Unit]
Description=Crypto assistant: Telegram bot
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
User=cryptoauto
Group=cryptoauto
ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/bot.py
LoadCredential=telegram-bot-token:/etc/crypto-auto/credentials/telegram-bot-token
LoadCredential=owner-chat-id:/etc/crypto-auto/credentials/owner-chat-id
Environment=PYTHONDONTWRITEBYTECODE=1
Restart=always
RestartSec=15
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/var/spool/crypto-auto /var/lib/crypto-auto
MemoryAccounting=yes
MemoryMax=128M

[Install]
WantedBy=multi-user.target

# crypto-exchange.service — as crypto-bot.service, with these differences:
#   Description=Crypto assistant: exchangeInfo watcher
#   ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/exchange.py
#   no LoadCredential= line

# crypto-announce.service — as crypto-bot.service, with these differences:
#   Description=Crypto assistant: Binance announcement stream
#   ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/announce.py
#   LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key
#   LoadCredential=binance-api-secret:/etc/crypto-auto/credentials/binance-api-secret
#   RestartPreventExitStatus=3

# crypto-cleanup.service
[Unit]
Description=Crypto assistant: retention of run records and spool

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/cleanup.py
Environment=PYTHONDONTWRITEBYTECODE=1

# crypto-cleanup.timer
[Unit]
Description=Crypto assistant: daily retention

[Timer]
OnCalendar=*-*-* 03:17:00 UTC
Persistent=true
Unit=crypto-cleanup.service

[Install]
WantedBy=timers.target

# crypto-deploy.service
[Unit]
Description=Crypto assistant: install vps/ from main
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/libexec/crypto-auto/deploy.sh

# crypto-deploy.timer
[Unit]
Description=Crypto assistant: deployer tick

[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
Unit=crypto-deploy.service

[Install]
WantedBy=timers.target
```

`MemoryMax=128M` on the three small services is a ceiling chosen, not measured [Architect's decision];
the report prints the peaks D3 and D4 measured beside it. The two scheduled times put the second run
after the journal's 13:00 UTC write, so the structural file it reads is hours old rather than a day.

### 12.13 `vps/memory-record.txt`

```
# TZ-54 measurement record of crypto-run.service (map inv. 46). Written at Stage E; never edited by hand.
measured_utc=<YYYY-MM-DDTHH:MM:SSZ>
hog_bytes=100663296
hog_footprint_bytes=<F_hog>
run_completed=<yes|no>
run_duration_s=<D>
run_cgroup_footprint_bytes=<F_run>
run_process_hwm_bytes=<P_run>
run_footprint_bytes=<F>
mem_available_bytes=<MemAvailable before D2>
session_rss_bytes=<session tree VmRSS before D2>
host_free_bytes=<A0>
memory_max_bytes=<derived>
runtime_max_s=<derived>
fits=<yes|no>
```

### 12.14 Selftest sections

| Section | What it compares | Known answer and its source |
|---|---|---|
| A | `cut_tokens` on the checkout's `index.html` | rows > 0, every `s` matches `^[A-Z0-9]+USDT$`, names unique |
| B | the writer on synthetic sources for `BTCUSDT` and `tokens[]`, judged by the gate run as A4 read it, in a temporary directory laid out like the repository | exit 0; one `tokens[]` symbol removed from `c` → exit 5; `n` one too large → exit 4 (map §11's classes) |
| C | `atomic_write` twice at one path, the second failing while serialising | the target and every temporary file absent afterwards (inv. 72) |
| D | §12.3's conversion | the expected block, byte for byte |
| E | §12.3's chunking | 39 + 11; a `<pre>` block within the limit never split |
| F | §12.4's filter | the table |
| G | §12.5's matcher | the table |
| H | §12.10's query and signature | both strings |
| I | §12.9's verdict | the four verdicts |
| J | `derive_limits` | §12.8's two answers |
| K | cleanup's selection | §12.11 |
| L | `redact` with a planted value | `<redacted>` present, the value absent |
| M | `vps/memory-record.txt` against `crypto-run.service` and `vps/manifest` | `run_footprint_bytes = max(cgroup, hwm)`; `host_free_bytes = mem_available + session_rss`; `derive_limits(run_footprint, run_duration)` equals the record and the unit's `MemoryMax=` and `RuntimeMaxSec=`; `fits` equals the rule; `hog_footprint_bytes ≥ hog_bytes`; the manifest lists both `crypto-run.timer` and `crypto-run.path` exactly when `fits=yes` |

---

## 13. Validation

- **V1. Selftest.** `python3 vps/selftest.py` after Stage E: exit 0, every section above zero, the total
  printed. **Negative control** (inv. 68): one character of §12.3's expected block changed in the
  working tree → exit non-zero with section D failing and every other section green; reverted;
  green again.
- **V2. Syntax.** `python3 -m py_compile` on every `vps/*.py`; `bash -n` on both scripts;
  `systemd-analyze verify` on every file of `vps/units/` after C3, exit 0, warnings printed.
- **V3. Dry run.** `bash vps/install.sh --dry-run` from the branch prints what it would install and
  enable, and `systemctl list-unit-files 'crypto-*'` reads the same before and after.
- **V4. The writer on the live market.** D2's `writer:` line shows `gate_exit=0 committed=yes
  pushed=yes`, and `origin/main` carries `analyst: live.json (vps)` and the run's own `analyst: <date>`.
- **V5. The instrument.** `F_hog` ≥ 100 663 296.
- **V6. Fit.** E1's terms and its inequality, printed; section M green.
- **V7. Delivery.** D5's accepted chunks equal its chunks; the outbox is empty afterwards.
- **V8. Credentials.** `stat -c '%a %U %s %n'` on the directory and the four files; the last byte of
  each file is not a newline; **the exact-value scan** — `grep -c -F -f <file>` for each of the three
  credential files, with the file proven to hold exactly one non-empty line first — over this report,
  `git diff origin/main...HEAD`, every file under the branch's `vps/`, the D2 run's day log and state on
  `origin/main`, `journalctl -o cat -u 'tz54-*'` and `journalctl -o cat -u crypto-deploy.service`:
  every count 0. **The analysis unit cannot read them:** a transient unit with
  `InaccessiblePaths=-/etc/crypto-auto/credentials` running `test -r
  /etc/crypto-auto/credentials/telegram-bot-token` exits 1, and the same unit without the property
  exits 0 (inv. 68).
- **V9. The key and the stream.** D3's verdict with its field booleans, the subscribe answer, every
  message's `catalogName`, title, publish time and lag, pings, reconnects and the exit code.
- **V10. Nothing left.** `systemctl list-units --all 'tz54-*'` empty; `systemctl list-unit-files
  'crypto-*'` exactly `crypto-deploy.service` and `crypto-deploy.timer`, the timer `enabled`;
  `/var/tmp/tz54-vps`, `/var/tmp/tz54-state` and `/root/.claude/projects/-tmp-tz53-unit` absent.
- **V11. No production file.** `git diff --name-only origin/main...HEAD` lists only `vps/` paths.
- **V12. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main`
  receives nothing from this session but its report.

---

## 14. The report

Contract §10's template, with: A2's memory tables; A4's quoted lines; A5's derivation table and the
mapping it chose; A6–A9; C4's `bind:` line; D1's `F_hog`; D2's `F_run`, `P_run`, `F`, `MemoryPeak`,
`MemorySwapPeak`, `MemAvailable`, the session tree's `VmRSS`, `A0`, `D`, `memory_max_bytes`,
`runtime_max_s`, `fits`, the `crypto-run:` and `writer:` lines, the model ids under `modelUsage`, the
denied tool names, and the commit subjects on `origin/main`; D3, D4 and D5 as printed; E's record and
manifest; V1–V12. **The first line after `## Status` states the fit** — `fits` with `memory_max_bytes`
against `A0` — because it decides whether the host is resized. The answer D2 produced is not quoted,
summarised or characterised (contract §1).

---

## 15. Commit messages

Implementation, on the branch:

```
TZ-54: vps — payload writer, run unit, Telegram bot, exchange watcher, deployer
```

Report, on `main`:

```
TZ-54: report — the assistant on the VPS
```
