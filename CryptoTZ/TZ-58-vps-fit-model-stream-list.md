# TZ-58 — On the VPS: the fit from the product's own runs, the pinned model, the stream's handshake, the exchange's own list

**Canonical filename:** `CryptoTZ/TZ-58-vps-fit-model-stream-list.md`
**Report:** `CryptoReports/TZ-58-vps-fit-model-stream-list-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on
any other machine, before the gate and before any other work.**
**Class:** branch TZ (contract §8) — it modifies files under `vps/**`.
**Branch:** `tz-58-vps-fit-model-stream-list` · **Model:** Opus
**Previous TZ:** TZ-57, PARTIAL — its branch `claude/vibrant-albattani-ddmwh1` at `895d1dc` is accepted and
**must be merged before this TZ starts** (A1); its report is on `main`.
**Written against:** contract v26, map `2026-10-03-d`, methodology `2026-10-03-a`, TZ-57's report, and
TZ-57's branch at `895d1dc` — its `vps` tree `c4eef2b1d03991c05a27464038f60d2a3307c14a` — read by the
Architect from the repository on 03.10.2026. Map §10 row «The assistant's build sequence», items (14) to
(16) with the decisions of `2026-10-03-c` and `2026-10-03-d`, and row «The engine's
exchange-announcement read is a path its own §6 forbids», the decision of `2026-10-03-c`, are what this TZ
executes. **It carries TZ-57's host stages unchanged**; what TZ-57 built off the host is on `main` and is
not rebuilt.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-03-d.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-03-d.**` |
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
| `ANALYST-INSTRUCTIONS.md` | 3921 | `7f19dc64a596ee07ad8298ee2a59c8a4` | reported, with its revision line; `**Revision 2026-10-03-a.**` is the one this TZ was written against, and a different one is a finding, never a block |

The map itself: 3193 lines, MD5 `b5a4478afd3afebd24c4ec12897514dc` — reported, not enforced. The tree
`origin/main:vps` is reported beside them; `c4eef2b1d03991c05a27464038f60d2a3307c14a`, TZ-57's branch's
tree, is the one this TZ was written against, and a different one is a finding, never a block.

---

## 1. Credentials

None arrives and none is written. C1's transient unit reads the Binance pair as systemd credentials,
exactly as TZ-56's A5 and D3 did. **This session opens no model session:** the `claude` binary runs only
with `--version` and `--help` (A4), which open none, and the product's runs are read from their
journal, never repeated.

---

## 2. Contract and map text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> it may start TRANSIENT units from its branch for a measurement its TZ names, and its report proves none is left behind.

— contract §7 item 15.

> **Measuring the session's own environment is a DIFFERENT act and is permitted** — egress, tool availability, host reachability — provided the command is recorded beside its result

— contract §7 item 9.

> a managed challenge or a refusal is the reading, never an obstacle to route around, and no evasion technique appears in any command.

— contract §7 item 9.

> **No value is ever printed, logged, committed or quoted**

— contract §7 item 6.

> a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work

— map §10, row «The assistant's build sequence».

> TZ-58 carries TZ-57's host stages unchanged — the fit and the record, the model's pin, the stream's handshake and the list reader — written against that tree, and starts only after it is merged

— map §10, row «The assistant's build sequence».

> A run that fails for any other reason, the account's limit included, measures nothing about memory and decides nothing about size.

— map §10, row «The assistant's build sequence».

> A kill writes `fits=no` and the host is answered by 1 vCPU and 2 GB as `-f` decided; no kill and a completion write `fits=yes` and the host stays as it is; neither decides anything.

— map §10, row «The assistant's build sequence».

> `claude-opus-5-5` at `--effort high`.

— map §10, row «The assistant's build sequence».

> the service is enabled once the branch's own connection is answered `SUBSCRIBE`/`SUCCESS`.

— map §10, row «The engine's exchange-announcement read is a path its own §6 forbids».

> The exchange watcher reads the index hourly and, on each new generation, logs the articles it added and removed

— map §10, row «The engine's exchange-announcement read is a path its own §6 forbids».

---

## 3. What is built

**On the server, the four things only the server can answer.** The run unit has run since TZ-56's tree
was installed on 03.10.2026 — the writer committed for two runs, at 10:56:38Z and 11:38:03Z, and the
session pushed `analyst: 2026-10-03` at 11:58:00Z — and every run logged its limits, its peaks and its
usage. This TZ reads those lines from the VPS's journal, classes every run by them under a table
registered before the reading (§12.2), and writes the result into the branch: the record's `fits` and
the product's own block, the budget re-derived by `common.record_limits`, which TZ-57 put on `main`, and
the run unit's two derived lines. **The run's model is pinned and its effort set:** `claude-opus-5-5` at
`--effort high`, in place of the alias `opus` at the model's default `medium`, once the binary the run
unit reaches is read to accept both. **The stream's documented handshake is proved on the server's own
connection**, and the service is listed exactly when it is answered `SUBSCRIBE`/`SUCCESS`. **The list
reader is built:** the exchange watcher reads Binance's English announcement sitemap — a path `robots.txt`
permits — hourly, and logs every new generation's added and removed articles beside the stream's own
data lines, so the TZ that reads the first six runs after TZ-57's merge reads both series too.

---

## 4. Scope

### Files to Modify

```
vps/exchange.py    vps/run.py         vps/selftest.py
vps/memory-record.txt                 vps/units/crypto-run.service      vps/manifest
```

`vps/memory-record.txt`, `vps/units/crypto-run.service` and `vps/manifest` are written at Stage E and at
no other time; `crypto-run.service` changes only in its `MemorySwapMax=` and `RuntimeMaxSec=` lines, and
only where §12.4 moves them — an unchanged file is reported unchanged.

### Files to Create

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- transient units named `tz58-*`;
- the scratch directories `/var/tmp/tz58-vps` and `/var/tmp/tz58-state`, gone at the end;
- reading, never writing: the journals of `crypto-deploy.service`, `crypto-run.service` and
  `crypto-bot.service`; `/var/lib/crypto-auto/deployed-vps-tree`; `/proc/meminfo`; `systemctl` state;
  `/etc/systemd/system/crypto-run.timer`'s absence; the `claude` binary's `--version` and `--help` (A4).

**No file of the owner's other projects is read or touched, no Claude session is stopped, no run is
started or requested, and nothing under `/etc/crypto-auto/`, `/srv/crypto-auto`, `/var/lib/cryptorun`,
`/var/lib/crypto-auto` or `/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The size's second reading.** The first six runs the button starts after TZ-57's merge — their kills
  and admissions — and the stream's delivery against the list are read by the TZ after them (map §10).
- **Any alert about the stream's delivery.** This TZ builds the list's record; the reading of the two
  series is the next TZ's.
- **The host's resize.** Where §12.2 writes `fits=no`, the report's first line states the answer and the
  Architect's verdict routes it to the owner; this session changes nothing on the host.
- **What TZ-57 built:** `vps/common.py`, `vps/announce.py`, `exchange.act` and the selftest's sections J,
  M, P and the alerts half of R are not edited.
- **TZ-55's measured lines** of `vps/memory-record.txt` — every line except `budget_bytes`,
  `memory_swap_max_bytes` and `runtime_max_s`, which §12.4 derives.
- **`bench.yml`, every unit file other than `crypto-run.service`, `vps/install.sh`, `vps/deploy.sh`,
  `vps/bot.py`, `vps/writer.py`, `vps/cleanup.py`.**
- **Any order, any key with trading rights, the methodology.**

---

## 6. Rules — binding in every stage

1. **No model session** is opened by this session or by any unit it starts: the `claude` binary runs only
   with `--version` and `--help`.
2. **Redaction.** `common.redact()` covers every credential a program loads; no reading of this TZ
   prints a credential, a signature or a query string.
3. **The session's own network reads,** besides `git`'s and `gh`'s, are A3's reads, C1's key check and one
   stream connection, and C2's reads; nothing else. Each is recorded beside its command (contract §7
   item 9).
4. **A challenge or a refusal is a reading** (contract §7 item 9). No header, client or route is varied
   to obtain a different answer.
5. **Atomic writes** (inv. 72) for every file a later reader treats as current.
6. **No new Russian text.** Any Russian string touched stays `\uXXXX` escapes.
7. **Python 3.12's standard library and bash only.**
8. **Time is UTC everywhere,** and every `--since` names `UTC` (TZ-56 D-1).
9. **Every transient unit** is named `tz58-*`, runs with `MemoryAccounting=yes`, and is gone at the end.
10. **A run's answer is never read, quoted or characterised** (contract §1): of the run unit's journal,
    only its `crypto-run:` lines and systemd's own lines are printed, `models=` withheld exactly as
    TZ-55's report withheld it.

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`; `test -d /srv/crypto-auto/.git && echo
  clone`; `id -u cryptorun`. **Known answers:** `vultr`; `active` twice; `clone`; a number. **Derived:**
  TZ-56's report carries this host's journal lines under the name `vultr` and read both services
  `active`, and its probe ran as `cryptorun`, uid 995. **Any other answer: BLOCKED.** The session writes
  a report carrying A0's lines and its own `hostname`, commits it to `main`, and does nothing else — no
  gate, no branch, no reading — because every later stage reads or changes this host (map §10, quoted
  in §2).
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git merge-base --is-ancestor 895d1dc93ef57bc8298c4aa7560f93141a8354fa origin/main` → exit 0.
     **Exit 1: BLOCKED** — TZ-57's accepted implementation is not merged, and this TZ is written against
     its tree; the report says so and nothing else is done.
  2. `git rev-parse origin/main:vps`, `cat /var/lib/crypto-auto/deployed-vps-tree`, `ls
     /etc/systemd/system/crypto-run.timer`, and `journalctl -u crypto-deploy.service --since '2026-10-03
     05:00:00 UTC' -o short-iso --no-pager | grep -E 'deploy: installed vps tree|install: (removed|enabled|disabled|installed)'`.
     **Known answers:** the marker equals `origin/main:vps`; `crypto-run.timer` is absent; the journal
     carries `install: removed crypto-run.timer` and `deploy: installed vps tree <origin/main:vps>`.
     **Derived:** `vps/install.sh` disables and removes every installed `crypto-*` unit file absent from
     `vps/units/` and logs `removed <unit>`; TZ-57 deleted `crypto-run.timer`; the deployer ticks every
     five minutes. Where the marker still names the tree before the merge, the session waits up to ten
     minutes and reads again; **a marker that never reaches `origin/main:vps`, or a deploy line refusing
     the tree, leaves this TZ BLOCKED with those lines as the reading**, because every later stage is
     written against the merged tree.
- **A2. TZ-56's install and the product's runs.**
  1. `journalctl -u crypto-deploy.service --since '2026-10-03 05:00:00 UTC' -o short-iso --no-pager |
     grep -F 'deploy: installed vps tree b9f97526335fa2a12f60bab9bd164ded1250dd7c'`. **Known answer:** one
     line after 05:06:59Z. **Derived:** `4c67ebe`, the merge of TZ-56, is dated 05:06:59Z and carries that
     tree. That line's time is `T0`.
  2. `date -u +%FT%TZ` — the reading instant `R` — then `journalctl -u crypto-run.service --since
     '<T0> UTC' --until '<R> UTC' -o short-iso-precise --no-pager`, piped through
     `grep -E 'crypto-run:|systemd\[1\]:'` and then
     `sed -E 's/(crypto-run: models=)[^ ]*/\1[withheld]/'`, printed in full.
  3. `journalctl -u crypto-bot.service --since '<T0> UTC' -o short-iso --no-pager | grep -F 'bot: sent '`.
  4. `git log origin/main --since '<T0> UTC' --format='%h %cI %s' -- analyst/`.
  5. `grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo`, `nproc`, and
     `systemctl list-unit-files 'crypto-*' --no-pager`.

  Each invocation is then classed by §12.2, and the classes, the decision and the chosen invocation are
  printed as a table: start time, class, `memory_max`, `memory_swap_max`, `memory_peak`,
  `memory_swap_peak`, footprint, duration, `requests`, the four token counts and `cost_usd`. **Known
  answer, derived from `main`:** at least two invocations read `admitted=yes` and `writer_exit=0`, because
  only `run.py` runs the writer, after admission, and the writer committed `bc0cdd9` at 10:56:38Z and
  `729b6d0` at 11:38:03Z. Fewer is a finding, never a block. **The classes themselves are not registered:**
  they are what this reading exists to read.
- **A3. The list, read by the program's own client from the VPS** — an in-session `python3` with
  `urllib.request`'s default headers and a 20 s timeout, the same client §12.5 builds on:
  1. `https://www.binance.com/robots.txt` — status, and the `User-agent: *` group's lines that contain
     `sitemap_output` or `bapi`;
  2. §12.5's `LIST_INDEX_URL` — status, `Content-Type`, bytes, `Last-Modified`, and the children
     `list_children` would return;
  3. each such child — status, `Content-Type`, bytes, `Last-Modified`, and the count `list_articles`'
     pattern returns; then the union's count.

  Nothing of a body beyond those counts is printed. **Outcomes, registered before the reading:**
  - **L1** — every answer is 200 with an XML `Content-Type`, the group carries `Allow:
    */sitemap_output/`, the index names at least one English child and the union holds at least one
    article: B1 is built and C2 runs.
  - **Anything else:** the list scope is BLOCKED — B1 is not built, C2 does not run, the answers are the
    reading — and every other scope goes on.

  **Derivation.** The Architect's session read these URLs at 2026-10-03T14:03Z with `curl` from its own
  environment: `Allow: */sitemap_output/` and `Disallow: */bapi/` in the `*` group; the index 200
  `application/xml`, rebuilt at 02:02:14Z, naming three English children; the children 200
  `application/xml` with one `lastmod`, 2026-10-02, holding 8 329 articles by §12.5's pattern. TZ-53 read
  the first child from the VPS with `curl`. Python's own client from the VPS is unread, hence this
  reading; the counts move with every rebuild and are therefore never registered as a bar.
- **A4. The command line the run will use** — `tz58-cli`: `User=cryptorun`, `Group=cryptorun`,
  `MemoryAccounting=yes`, `RemainAfterExit=yes`, the run unit's own `Environment=HOME=`, `PATH=` and
  `DISABLE_AUTOUPDATER=1` lines (TZ-56 §12.3, unchanged by this TZ), running `/bin/sh -c 'command -v
  claude; claude --version; claude --help | grep -E -- "--(model|effort)"'`. **Outcomes, registered
  before the reading:**
  - **M1** — the version is 2.1.280 or later and the `--effort` line offers `high`: B2 is built.
  - **Anything else:** the model scope is BLOCKED — `run.py` keeps `--model opus` — and every other
    scope goes on.

  **Derivation.** Claude Code's «Model configuration» page, read by the Architect's session on
  03.10.2026: Opus 5.5 requires v2.1.280 or later; `--effort` takes `low`, `medium`, `high`, `xhigh`,
  `max`; Opus 5.5 offers all five and defaults to `medium`; the alias `opus` resolves to Opus 5.5 on the
  Anthropic API, and a full model name pins it. TZ-53 read v2.1.282 on the VPS; the binary the run unit
  reaches today is unread, hence this reading.

The stream's handshake needs no reading before C1: TZ-56 A5's second connection sent `SUBSCRIBE` and was
answered `REGISTER`/`SUCCESS` at 7 ms and `SUBSCRIBE`/`SUCCESS` at 246 ms, and `main`'s `announce.py`
sends exactly that command since TZ-57. C1 is written against that reading.

---

## 8. Stage B — the code, on the branch

### B1. `vps/exchange.py` — §12.5, only under A3's L1

### B2. `vps/run.py` — §12.6, only under A4's M1

### B3. `vps/selftest.py` — §12.7

---

## 9. Stage C — on the VPS, on the branch's code

`/var/tmp/tz58-vps` is a `0755 root:root` copy of the branch's `vps/` after Stage B; `/var/tmp/tz58-state`
is created `0770 cryptoauto:cryptoauto`.

- **C1. The handshake**, `tz58-subscribe`: `MemoryAccounting=yes`, `RuntimeMaxSec=120`,
  `RemainAfterExit=yes`, `LoadCredential=` of the two Binance files, running `/usr/bin/python3
  /var/tmp/tz58-vps/announce.py --measure 60 1 --state-dir /var/tmp/tz58-state`. Collected: its journal
  and `systemctl show tz58-subscribe -p Result -p ExecMainStatus`. **Known answers, derived from TZ-56 A5's
  second connection and TZ-56 D3's key line:** `announce: key ACCEPTED`; exactly one `announce: command
  answer` line, whose JSON carries `"subType": "REGISTER"` and `"data": "SUCCESS"`; one `announce:
  subscribe answer` line whose JSON carries `"subType": "SUBSCRIBE"` and `"data": "SUCCESS"`; exit 0 or 2
  — 2 means only that no message arrived in the minute, which decides nothing. **Any other answer leaves
  the stream scope BLOCKED:** E3 does not list `crypto-announce.service`.
- **C2. The list reader**, only under L1 — `tz58-list`, `User=cryptoauto`, `Group=cryptoauto`,
  `MemoryAccounting=yes`, `RemainAfterExit=yes`, running `/usr/bin/python3 /var/tmp/tz58-vps/exchange.py
  --list-once --state-dir /var/tmp/tz58-state`; within the same minute, the independent count —
  `curl -sS -m 20` of the index and of each English child it names, `grep -o -E '<loc>https://www\.binance\.com/en/support/announcement/detail/[0-9A-Za-z]+</loc>'`,
  `sort -u | wc -l` over all children together; then, at least 60 s after the first, `tz58-list2`, the same
  unit again. **Known answers, derived from §12.5:** the first prints one `exchange: list generation=`
  line with `baseline=yes`, `new=-`, `gone=-`, its `children` equal to the English children `curl` read
  and its `articles` equal to `curl`'s count; `/var/tmp/tz58-state/list-generation.json` holds that many
  ids; the second prints `exchange: list unchanged` with the same `articles`. Where the index's
  `Last-Modified` differs between the program's read and `curl`'s, a rebuild fell between them: both are
  repeated once and the repeat is the reading. **A mismatch that survives the repeat leaves the list
  scope BLOCKED** and B1 is reverted on the branch before Stage E.

---

## 10. Stage E — decisions written into the branch

- **E1. `vps/memory-record.txt`:** under `fits=yes` or `fits=no`, §12.3's block appended after TZ-55's
  lines, and `budget_bytes`, `runtime_max_s` and `memory_swap_max_bytes` rewritten by §12.4; under neither,
  unchanged.
- **E2. `vps/units/crypto-run.service`:** `MemorySwapMax=` = `budget_bytes` − 167 772 160 and
  `RuntimeMaxSec=` = `runtime_max_s`, both from E1's record; every other line unchanged.
- **E3. `vps/manifest`:** `crypto-deploy.timer`, `crypto-cleanup.timer`, `crypto-exchange.service`,
  `crypto-bot.service` and `crypto-run.path`, in that order; then `crypto-announce.service` exactly when C1
  met every known answer.
- **E4.** `python3 vps/selftest.py` green in every section.

---

## 11. Validation

- **V1. Selftest.** `python3 vps/selftest.py` after Stage E: exit 0, every section non-empty, the total
  printed. **Negative control** (inv. 68): under L1, one character of one §12.7 list known answer in
  section R changed in the working tree → exit non-zero with section R alone failing; otherwise one
  digit of one row of J's `record_limits` checks, with section J alone failing; reverted; green again,
  MD5 restored.
- **V2. Syntax.** `python3 -m py_compile` on every `vps/*.py`; `bash -n` on both scripts;
  `systemd-analyze verify` on every file of `vps/units/`, exit 0, warnings printed.
- **V3. Dry run.** `bash vps/install.sh --dry-run` prints no line naming `crypto-run.timer`, and `would
  enable --now crypto-announce.service` exactly when E3 listed it; `systemctl list-unit-files 'crypto-*'`
  reads the same before and after, and the same as A2's.
- **V4. The fit.** A2's lines against §12.2's table, invocation by invocation; E1's product block against
  the chosen invocation's own lines, field by field; `common.record_limits(<E1's record>)` printed
  beside the record's `budget_bytes` and `runtime_max_s`, and E2's two unit lines beside them.
- **V5. The model.** `python3 -c 'import sys; sys.path.insert(0, "vps"); import run; print(run.CLAUDE[3:])'`:
  under M1 it carries `--model claude-opus-5-5` and `--effort high`, and no element equals `opus`; A4's
  lines beside it.
- **V6. The stream.** C1's journal and `systemctl show` lines against C1's known answers.
- **V7. The list.** A3's answers and outcome; C2's three readings against C2's known answers.
- **V8. Credentials.** The exact-value scan of TZ-56 V7 — `grep -c -F -f` with each of
  `binance-api-key`, `binance-api-secret` and `claude-oauth-token`, each proven first to hold one
  non-empty line — over this report, `git diff origin/main...HEAD`, every file under the branch's `vps/`,
  and `journalctl -o cat -u 'tz58-*'`: every count 0.
- **V9. Nothing left.** `systemctl list-units --all 'tz58-*'` empty; no `tz58-*` entry under
  `/run/systemd/system.control/` or `/run/systemd/transient/`; `/var/tmp/tz58-vps` and
  `/var/tmp/tz58-state` absent; `systemctl list-unit-files 'crypto-*'` identical to A2's.
- **V10. No production file.** `git diff --name-only origin/main...HEAD` lists only `vps/` paths.
- **V11. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main`
  receives nothing from this session but its report.

---

## 12. Dictated blocks

### 12.1 Russian strings

None is added or changed.

### 12.2 The product's runs — classes and the fit

```
invocation   = the lines of crypto-run.service from one systemd line containing
               «Starting crypto-run.service» up to the next such line, or to R
active       = an invocation with neither «Deactivated successfully» nor «Failed with result» before R:
               printed, and excluded from every count below
K-oom        = it carries «Failed with result 'oom-kill'»
K-timeout    = it carries «Failed with result 'timeout'»
N            = its first summary line reads admitted=no
L            = its second summary line reads api_error_status=429
C            = its first summary line reads claude_exit=0 and is_error=false, with answer_chars above 0
F            = any other
precedence   = K-oom, K-timeout, N, L, C, F — the first that applies is the class

fits = no      when any invocation is K-oom or K-timeout
fits = yes     when none is, and at least one is C
no fits line   when neither — the fit scope is BLOCKED: the record and the run unit are unchanged,
               and the report names every class it read

footprint    = memory_peak + memory_swap_peak of the invocation's third summary line;
               "-" when either reads "-"
duration_s   = the time of its third summary line − the time of its «Starting» line, in seconds
chosen       = under fits=yes the C with the largest footprint; under fits=no the K with the largest
               footprint; ties, or no integer footprint, → the earliest
```

**Derivations.** The classes are the run's own lines — `run.py`'s three summary lines, TZ-54 §14,
TZ-55 B2.4 and TZ-56 §12.4 — and systemd's own result lines. A kill answers the host, a refusal by the
account or any other failure answers nothing about size, and a completion fits: map §10, decisions
`2026-10-01-f` and `2026-10-03-c`, quoted in §2. `api_error_status=429` is how TZ-55's report recorded
the account's limit on both of its admitted runs. The largest footprint is the conservative choice
because the budget is derived from it.

### 12.3 The record's product block — appended after TZ-55's lines

```
# TZ-58: the product's own runs since TZ-56's install (map §10). Written at Stage E; never edited by hand.
product_read_utc=<R, YYYY-MM-DDTHH:MM:SSZ>
product_invocations=<invocations counted>
product_killed=<K-oom + K-timeout>
product_not_admitted=<N>
product_account_limited=<L>
product_completed=<C>
product_class=<C | K-oom | K-timeout, of the chosen invocation>
product_run_utc=<the chosen invocation's «Starting» time, YYYY-MM-DDTHH:MM:SSZ>
product_memory_max_bytes=<its memory_max>
product_memory_swap_max_bytes=<its memory_swap_max>
product_memory_peak_bytes=<its memory_peak>
product_memory_swap_peak_bytes=<its memory_swap_peak>
product_footprint_bytes=<its footprint>
product_duration_s=<its duration_s, six decimals>
fits=<yes | no>
```

Each value is copied from the chosen invocation's own lines; `-` stays `-`. The keys are TZ-57 §12.3's,
which `main`'s section M already checks as `PRODUCT_KEYS`.

### 12.4 What E1 and E2 write

```
E1:  budget_bytes, runtime_max_s = common.record_limits(record) ;  memory_swap_max_bytes = budget_bytes − memory_max_bytes
E2:  MemorySwapMax= budget_bytes − 167 772 160 ;  RuntimeMaxSec= runtime_max_s
```

`common.record_limits` is `main`'s since TZ-57, the one implementation of the rule TZ-57 §12.4 dictated;
section J checks its five known answers and section M checks the record against it. 167 772 160 is
`MEMORY_MAX_FLOOR_BYTES`, and the unit carries the floor and the budget's rest by TZ-56 §12.3.

### 12.5 `vps/exchange.py` — the exchange's own list, only under A3's L1

```
LIST_INDEX_URL = "https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml"
LIST_CHILD     = re.compile(r"<loc>\s*(https://www\.binance\.com/sitemap_output/domain=www\.binance\.com/sitemap_SupportAndAnnouncement_en_[0-9]+\.xml)\s*</loc>")
LIST_ARTICLE   = re.compile(r"<loc>\s*https://www\.binance\.com/en/support/announcement/detail/([0-9A-Za-z]+)\s*</loc>")
LIST_STATE     = "list-generation.json"
LIST_POLL_S    = 3600
```

- `list_children(index_text)` → the `LIST_CHILD` URLs in order of first appearance, each once.
- `list_articles(child_text)` → the set of `LIST_ARTICLE` ids.
- `list_diff(prev_ids, cur_ids)` → `(added, removed)` counts, or `("-", "-")` when `prev_ids` is `None`.
- `list_poll(state_dir)` → the line it would log. One GET of the index — `urllib.request`, default
  headers, `common.HTTP_TIMEOUT_S`. When the SHA-256 of its body equals the stored `digest`, it returns
  `exchange: list unchanged generation=<stored generation> articles=<stored count>` and reads nothing
  more. Otherwise: no child, a non-200 answer, or an empty union raises `ListUnreadable` and the stored
  state stays; else every child is read, the union diffed against the stored ids, the state written
  atomically, and the line is
  `exchange: list generation=<G> read=<UTC> children=<n> articles=<n> new=<n|-> gone=<n|-> baseline=<yes|no>`,
  where `G` is the index's `Last-Modified` as `YYYY-MM-DDTHH:MM:SSZ` (`email.utils.parsedate_to_datetime`),
  or `-` when absent or unparseable.
- The state, `list-generation.json` in the state directory:
  `{"digest": <hex>, "generation": <G>, "read": <UTC>, "children": <n>, "articles": [<ids, sorted>]}`.
- **The service:** after each exchangeInfo poll, `list_poll` runs when none has run in this process or at
  least `LIST_POLL_S` have passed since the last attempt; its line is logged unless it is `unchanged`;
  any exception logs `exchange: list read failed (<exception class>)` and never stops the exchangeInfo
  poll.
- **`--list-once`:** one `list_poll`, its line printed whatever it is; exit 0, or 1 after printing the
  failure line. `--once` is unchanged.
- The module docstring names the list and TZ-58. `act()` and the poll line are TZ-57's and do not move.

**Derivation.** The patterns are the Architect's read of 2026-10-03T14:03Z: the index's children are
`…_<locale>_<n>.xml`, three of them English; the English children's article URLs end in a 32-character
lowercase hexadecimal id (7 740) or a 12-digit one (589), beside 144 catalogue pages
(`…/announcement/list/<n>`) and FAQ pages, which the pattern excludes. Hourly is the cadence because the
generation is rebuilt about once a day and the index is 13 536 bytes; the children, 1.6 MB together, are
read only when the index changed. The digest of the body, never a header, decides «changed», because no
header's behaviour across rebuilds has been read.

### 12.6 `vps/run.py` — the pinned model and its effort, only under A4's M1

```
MODEL  = "claude-opus-5-5"
EFFORT = "high"
CLAUDE = ["claude", "-p", PROMPT,
          "--output-format", "json", "--model", MODEL, "--effort", EFFORT,
          "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch",
          "--append-system-prompt", APPEND]
```

Nothing else in `run.py` moves. **Derivation:** the owner proposed Opus 5.5 at high effort on
03.10.2026 and the map keeps it (§2): the method's measured failure is a run that stops short of its
last steps, effort governs how much a run reads and verifies before it stops, Opus 5.5's default is
`medium`, and a full model name moves only by a TZ where the alias would move with the next release.

### 12.7 Selftest sections — changed

| Section | What it compares | Known answer and its source |
|---|---|---|
| O | `run.py` | the checks it carries; under M1, `run.CLAUDE` carries `--model` followed by `claude-opus-5-5` and `--effort` followed by `high`, and no element equals `opus` |
| R | under L1, `exchange.list_children`, `list_articles`, `list_diff` on the texts below, beside TZ-57's alerts-only checks | as stated below |

Section R's texts, exactly:

```python
SM = "https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_"
EN0, EN1, RU0 = SM + "en_0.xml", SM + "en_1.xml", SM + "ru_0.xml"
INDEX = "<sitemapindex>" + "".join("<sitemap><loc>%s</loc><lastmod>2026-10-02</lastmod></sitemap>" % u
                                   for u in (EN1, RU0, EN0, EN1)) + "</sitemapindex>"
A, B, C, D = "a" * 32, "0123456789abcdef" * 2, "115000483751", "d" * 32
DETAIL = "https://www.binance.com/en/support/announcement/detail/"
def urlset(urls):
    return "<urlset>" + "".join("<url><loc>%s</loc><lastmod>2026-10-02</lastmod></url>" % u for u in urls) + "</urlset>"
CHILD0 = urlset([DETAIL + A, DETAIL + B, "https://www.binance.com/en/support/faq/x1",
                 "https://www.binance.com/en/support/announcement/list/48",
                 "https://www.binance.com/zh-CN/support/announcement/detail/" + D])
CHILD1 = "<urlset><url><loc>\n    " + DETAIL + B + "\n  </loc></url>" + urlset([DETAIL + C])[8:]
```

Known answers, computed by the Architect on a prototype of §12.5's patterns: `list_children(INDEX) ==
[EN1, EN0]`; `list_articles(CHILD0) == {A, B}`; `list_articles(CHILD1) == {B, C}`; `list_diff(None, {A,
B, C}) == ("-", "-")`; `list_diff({A, B, D}, {A, B, C}) == (1, 1)`; `list_diff({A, B, C}, {A, B, C}) ==
(0, 0)`. The same prototype on the Architect's three English children of 03.10.2026 returned 3 children
and 8 329 articles.

Every other section is `main`'s and stays green.

---

## 13. The report

Contract §10's template, with: A0's lines; A1's merge check and the deploy lines; A2's lines, the
classification table and the decision; A3's and A4's answers and outcomes; C1's and C2's journals and
`systemctl show` lines; E's record diff, unit diff and manifest; V1–V11. **The first four lines after
`## Status` state:** the fit — `fits`, the chosen invocation's class, its footprint beside `budget_bytes`,
and the host's answer: as it is, or 1 vCPU and 2 GB; the run's model and effort, or the model scope
BLOCKED with A4's answer; whether `crypto-announce.service` is listed, with C1's answer; and whether the
list reader is built, with C2's baseline line. No analysis answer is quoted.

---

## 14. Commit messages

Implementation, on the branch:

```
TZ-58: vps — the fit from the product's own runs, the pinned model, the stream listed, the exchange's own list
```

Report, on `main`:

```
TZ-58: report — on the VPS: the fit, the model, the stream and the list
```
