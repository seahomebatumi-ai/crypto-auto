# TZ-60 — On the VPS: the owner's STOP, and the runs the button started after TZ-57's merge

**Canonical filename:** `CryptoTZ/TZ-60-vps-stop-and-six-runs.md`
**Report:** `CryptoReports/TZ-60-vps-stop-and-six-runs-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on
any other machine, before the gate and before any other work.**
**Class:** branch TZ (contract §8) — it modifies and creates files under `vps/**`.
**Branch:** `tz-60-vps-stop-and-six-runs` · **Model:** Opus
**Previous TZ:** TZ-59, COMPLETED and merged at `07126c0`; its report is on `main`.
**Written against:** contract v26, map `2026-10-05-a`, methodology `2026-10-05-a`, and `main` at
`df3484b` — its `vps` tree `36f06177a8899162865e17157d57d643c58e1adc` — read by the Architect from the
repository on 05.10.2026. Map §10 row «The assistant's build sequence», item (18) with the decision of
`2026-10-05-a`, and row «The engine's exchange-announcement read is a path its own §6 forbids» are what
this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-05-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-05-a.**` |
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
| `vps/bot.py` | 422 | `d3d8da0a43f807a2d5d86472df328156` | reported; a different file is a finding, never a block |
| `vps/common.py` | 329 | `0a54ae9169cc06e36465413d198f2c4b` | reported; as above |
| `vps/run.py` | 333 | `10165bc8d4d79e92db30147a76eec48f` | reported; as above |
| `vps/install.sh` | 251 | `d0a26e04d520501f0dea68f67fc14cc3` | reported; as above |
| `vps/manifest` | 6 | `279e5f1b479b5cfdf1ec7582ac382054` | reported; as above |
| `vps/selftest.py` | 817 | `c728b6fd74d1aaad269a1fb2a6de886e` | reported; as above |

The map itself: 3230 lines, MD5 `6ae8807f25f54981562074f3262efd2b` — reported, not enforced. The tree
`origin/main:vps` is reported beside them; `36f06177a8899162865e17157d57d643c58e1adc` is the one this TZ
was written against, and a different one is a finding, never a block.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened and the `claude` binary is
not run:** every run this TZ reads is read from its journal, never repeated, and Stage C's transient units
read no credential.

---

## 2. Contract and map text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> it may start TRANSIENT units from its branch for a measurement its TZ names, and its report proves none is left behind.

— contract §7 item 15.

> **A unit that runs a model session runs as its own unprivileged user, never root, and holds exactly two credentials: its own Claude login and the deploy key**

— contract §7 item 6. `crypto-stop.service` runs no model session and holds no credential.

> a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work

— map §10, row «The assistant's build sequence».

> **The size is re-read on the first six runs the button starts after TZ-57's merge:** one killed by a limit, or more than one not admitted for memory, answers the host by 1 vCPU and 2 GB

— map §10, row «The assistant's build sequence».

> A run that fails for any other reason, the account's limit included, measures nothing about memory and decides nothing about size.

— map §10, row «The assistant's build sequence».

> **Decided at `2026-10-05-a`: a word stops the run.**

— map §10, row «The assistant's build sequence», item (18), which specifies the behaviour §3 restates.

> a silent stream beside a growing list is the defect three measurements could not see

— map §10, row «The engine's exchange-announcement read is a path its own §6 forbids».

---

## 3. What is built and what is read

**The owner's STOP.** On 04.10 the owner pressed the button by accident while reading an answer, and
nothing could stop the run it started. After this TZ's merge, «СТОП», «STOP» or `/stop` in his chat stops
an analysis completely: the bot answers «Останавливаю анализ…» and leaves a stop request in the spool;
`crypto-stop.path` starts `crypto-stop.service`, a root oneshot that holds no credential and starts no
model; `vps/stop.py` consumes the stop requests first, removes every pending run request, stops
`crypto-run.service` with systemd's own stop — which signals every process of the unit's cgroup, the
session and its tools included — clears the unit's failed state and start counter, and writes one notice.
While it runs, its runtime directory `/run/crypto-stop` tells `run.py` that the stop is the owner's, so the
run logs that and writes no «Анализ не завершён.». The messages that confirm a start name the word. **Root,
because stopping a system unit is root's; the bot gains no privilege:** it asks through a path unit, the
shape that already starts a run.

**The reading TZ-58 and TZ-59 deferred.** The run unit's journal is read from TZ-57's install onward and
every invocation is classed under a table registered before the reading (§12.2): the size by the six-run
rule, the usage of every run at `high` beside the run of 03.10 at the default effort (§12.3), and the
announcement stream's own record against the exchange's own list (§12.4). `main` shows two writer commits
since TZ-57's merge — `b4ff2fc` at 16:43:21Z and `0d2566d` at 17:15:12Z on 04.10 — and one analysis,
`6c9645e` at 17:08:41Z; the journal says what the second run did.

---

## 4. Scope

### Files to Modify

```
vps/common.py      vps/bot.py         vps/run.py
vps/install.sh     vps/manifest       vps/selftest.py
```

### Files to Create

```
vps/stop.py        vps/units/crypto-stop.path        vps/units/crypto-stop.service
```

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- transient units named `tz60-*`;
- the scratch directories `/var/lib/tz60-vps` and `/var/lib/tz60-spool`, gone at the end;
- reading, never writing: the journals of `crypto-deploy.service`, `crypto-run.service`,
  `crypto-bot.service`, `crypto-announce.service` and `crypto-exchange.service`;
  `/var/lib/crypto-auto/deployed-vps-tree`; `/var/lib/crypto-auto/announcements.jsonl`;
  `/var/lib/crypto-auto/list-generation.json` — its `generation`, `read`, `children` and the COUNT of its
  `articles`, never the ids; `/proc/meminfo`; `nproc`; `systemctl` state.

**No run is started, requested or stopped; `crypto-run.service` is never the target of a `systemctl`
command of this session other than a read; no Claude session is opened or stopped; and nothing under
`/etc/crypto-auto/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or
`/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The host's resize.** Under §12.2's `Z1` the report's first line states it and the Architect's verdict
  routes it to the owner; nothing on the host changes.
- **The record.** `vps/memory-record.txt` and `vps/units/crypto-run.service` do not move: this TZ is
  report-only on the size.
- **The run's model and effort.** Usage at `high` is read and never acted on here.
- **Admitting the stream's record into the methodology** — the Architect's edit after this reading (map
  §10) — and any alert on the stream's delivery.
- **A confirmation step before a run** — decided against at `2026-10-05-a` (map §10, item (18)).
- **The role split** (map §10, row «One agent executes the whole methodology in one run»).
- **`vps/deploy.sh`, `vps/announce.py`, `vps/exchange.py`, `vps/writer.py`, `vps/cleanup.py`, every unit
  file other than the two created, `bench.yml`, the methodology, any key with trading rights.**

---

## 6. Rules — binding in every stage

1. **No model session**, and the `claude` binary is not run.
2. **No run is started, requested or stopped.** The one unit Stage C stops is its own `tz60-dummy.service`.
3. **The session's own network reads** are `git`'s and `gh`'s, and nothing else.
4. **Atomic writes** (inv. 72) for every file a later reader treats as current: the stop request and the
   notice go through `common.atomic_write`.
5. **Russian text in `vps/` code** is `\uXXXX` escapes and equals §12.1 character for character.
6. **Python 3.12's standard library and bash only.**
7. **Time is UTC everywhere,** and every `--since` names `UTC`.
8. **Every transient unit** is named `tz60-*`, runs with `MemoryAccounting=yes`, and is gone at the end.
9. **A run's answer is never read, quoted or characterised** (contract §1): of the run unit's journal,
   only its `crypto-run:` lines and systemd's own lines are printed, and `models=` reads `[withheld]` with
   §12.3's two derived fields beside it.
10. **An announcement's `title` is the exchange's own public text** and is printed only inside §12.4's
    engine window; nothing of any record's `body` is printed.

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`; `test -d /srv/crypto-auto/.git && echo
  clone`; `id -u cryptorun`. **Known answers:** `vultr`; `active` twice; `clone`; `995`. **Derived:**
  TZ-58's report-2 read exactly these on this host at 2026-10-03T19:50:43Z. **Any other answer: BLOCKED.**
  The session writes a report carrying A0's lines and its own `hostname`, commits it to `main`, and does
  nothing else (map §10, quoted in §2).
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git merge-base --is-ancestor 9c1af521e0958a95b902b6e19e7c782729a754de origin/main` → exit 0.
     **Exit 1: BLOCKED** — TZ-59's implementation is not merged, and this TZ is written against its tree.
  2. `git rev-parse origin/main:vps`, `cat /var/lib/crypto-auto/deployed-vps-tree`, `systemctl
     list-unit-files 'crypto-*' --no-pager`, and `journalctl -u crypto-deploy.service --since '2026-10-03
     19:00:00 UTC' -o short-iso-precise --no-pager | grep -E 'deploy: installed vps tree|install:
     (removed|enabled|disabled|installed)'`. **Known answers:** the marker equals `origin/main:vps`; the
     journal carries `deploy: installed vps tree` for `c4eef2b1d03991c05a27464038f60d2a3307c14a`,
     `94a55b6f07d6aa6b2290eb3b4646f1740cd1a47e` and `36f06177a8899162865e17157d57d643c58e1adc`, in that
     order. **Derived:** TZ-57, TZ-58 and TZ-59 merged at `075de0e`, `2416e3f` and `07126c0` — 19:35Z,
     20:34Z and 21:01Z on 03.10.2026 — with those `vps` trees (`git rev-parse <merge>:vps`), and the
     deployer ticks every five minutes. **Their times are `T0`, `T1` and `T2`.** A missing line is a
     finding, and the stage that needs its time uses the merge commit's time instead and says so; a marker
     that differs from `origin/main:vps` is a finding, never a block.
- **A2. The runs since `T0`.**
  1. `date -u +%FT%TZ` — the reading instant `R`.
  2. `journalctl -u crypto-run.service --since '<T0> UTC' --until '<R> UTC' -o short-iso-precise
     --no-pager`, piped through `grep -E 'crypto-run:|systemd\[1\]:'` and §12.3's rewrite of `models=`,
     printed in full.
  3. `journalctl -u crypto-bot.service --since '<T0> UTC' -o short-iso --no-pager | grep -E 'bot: (sent
     |updates=)'`.
  4. `git log origin/main --since '<T0> UTC' --format='%h %cI %s' -- analyst/`.
  5. `grep -E '^(MemTotal|MemAvailable|SwapTotal|SwapFree):' /proc/meminfo` and `nproc`.

  Each invocation is classed by §12.2 and printed as one table: start time, class, `memory_max`,
  `memory_swap_max`, `memory_peak`, `memory_swap_peak`, footprint, duration, `requests`, `num_turns`, the
  four token counts, `cost_usd`, `pinned_present`, `other_models`. Then the size verdict by §12.2 and the
  usage table by §12.3. **Known answer, derived from `main` and the owner's message:** at least two
  invocations after `T2` read `admitted=yes` and `writer_exit=0`, because only `run.py` runs the writer,
  after admission, and the writer committed `b4ff2fc` at 16:43:21Z and `0d2566d` at 17:15:12Z on 04.10;
  the earlier of the two is class `C`, because `6c9645e` landed at 17:08:41Z and the owner was reading
  its answer in the chat when he pressed again (his message of 05.10.2026), and only a `C` writes an
  answer to the outbox. Fewer is a finding, never a block. **The second's class is not registered:** it
  is what this reading exists to read.
- **A3. The stream against the list.**
  1. `systemctl is-active crypto-announce.service crypto-exchange.service` and `systemctl show
     crypto-announce.service -p ActiveEnterTimestamp -p NRestarts`.
  2. `journalctl -u crypto-announce.service --since '<T1> UTC' -o short-iso --no-pager | grep -E
     'announce: (key|subscribe answer|command answer|connect failed|connection lost|close frame|planned
     refresh|data_messages)'`, printed in full, and the count of `announce: data ` lines per UTC day.
  3. `journalctl -u crypto-exchange.service --since '<T1> UTC' -o short-iso --no-pager | grep -F
     'exchange: list'`, printed in full.
  4. `/var/lib/crypto-auto/list-generation.json`, read with `python3`'s `json`: `generation`, `read`,
     `children` and `len(articles)`.
  5. `/var/lib/crypto-auto/announcements.jsonl`, read with `python3`'s `json` one line at a time: every
     record with `received_ms` at or after `T1`. Printed: per UTC day, the count by `catalogName`; the lag
     `received_ms − publishDate` as minimum, median and maximum in seconds; and the records §12.4 names
     inside the engine window, each with its `publishDate` as UTC, its `catalogName` and its `title`.

  Classed by §12.4. **The classes are not registered:** they are what this reading exists to read.

---

## 8. Stage B — the code, on the branch

### B1. `vps/common.py` — §12.5

### B2. `vps/bot.py` — §12.6

### B3. `vps/run.py` — §12.7

### B4. `vps/stop.py` — §12.8, created

### B5. `vps/units/crypto-stop.path` and `vps/units/crypto-stop.service` — §12.9, created

### B6. `vps/install.sh` and `vps/manifest` — §12.10

### B7. `vps/selftest.py` — §12.11

---

## 9. Stage C — on the VPS, on the branch's code

- **C0. Scratch.** `install -d -m 0755 /var/lib/tz60-vps` and `cp -a vps/. /var/lib/tz60-vps/` from the
  branch's checkout; `install -d -m 0770 /var/lib/tz60-spool/outbox /var/lib/tz60-spool/requests
  /var/lib/tz60-spool/stop`. **Derived:** `PrivateTmp=yes` gives a unit its own `/tmp` and `/var/tmp`, and
  `ProtectHome=yes` hides `/root` and `/home`, so the copy lives under `/var/lib`.
- **C1. The units.** `systemd-analyze verify vps/units/*` from the branch. **Known answer:** exit 0.
  **Derived:** the deployer runs this command before every install (`vps/install.sh`), and the
  Architect's session read exit 0 for §12.9's two files on systemd 255, this host's version (TZ-53).
- **C2. A live stop.** `systemd-run --unit tz60-dummy -p MemoryAccounting=yes /bin/sleep 600`, then
  `systemctl is-active tz60-dummy.service` → `active`; plant `{}` as `/var/lib/tz60-spool/requests/1-bot-1.req`
  and `/var/lib/tz60-spool/stop/1-bot-1.stop`; then

  ```
  systemd-run --unit tz60-stop --wait --collect -p Type=oneshot -p MemoryAccounting=yes \
    -p ProtectSystem=strict -p ProtectHome=yes -p PrivateTmp=yes -p NoNewPrivileges=yes \
    -p ReadWritePaths=/var/lib/tz60-spool -p RuntimeDirectory=tz60-stop \
    -p Environment=PYTHONDONTWRITEBYTECODE=1 \
    /usr/bin/python3 /var/lib/tz60-vps/stop.py --unit tz60-dummy.service --spool /var/lib/tz60-spool
  ```

  then `journalctl -u tz60-stop.service -o cat --no-pager | grep 'crypto-stop:'`, `systemctl is-active
  tz60-dummy.service`, `ls -A` of the three spool directories, and the outbox file's `kind` and whether
  its `text` equals `common.S13`. **Known answers:** `systemd-run` exits 0; one line beginning
  `crypto-stop: stops=1 requests_removed=1 before=active stop_exit=0` and ending `after=inactive
  notice=S13`; `tz60-dummy.service` is not active; `requests/` and `stop/` are empty; the outbox holds one
  file, `kind` `notice`, text equal to `S13`. **Derived:** §12.8's steps on §12.9's own properties, with
  the scratch spool in place of the real one; `systemctl stop` stops a unit's whole cgroup and returns
  when it is stopped. `reset_exit` is not registered: a transient unit is unloaded once stopped, and
  `reset-failed` on it may answer non-zero.
- **C3. Nothing to stop.** The same command with the three spool directories empty and `tz60-dummy.service`
  gone. **Known answers:** exit 0; one line with `stops=0 requests_removed=0 before=inactive` and ending
  `notice=S14`; one notice, text equal to `S14`. **Derived:** §12.8's choice; `systemctl is-active` prints
  `inactive` for a unit that is not loaded. `stop_exit` is not registered here: `systemctl stop` of a unit
  that is not loaded answers non-zero, while `crypto-run.service` is always loaded.
- **C4. Nothing left.** `systemctl reset-failed 'tz60-*'`; `systemctl list-units --all 'tz60-*'
  --no-pager` → none; `rm -rf /var/lib/tz60-vps /var/lib/tz60-spool`; both paths absent.

---

## 10. Validation

- **V1. Selftest.** `python3 vps/selftest.py`: exit 0, every section non-empty, the total printed; section
  F carries §12.11's rows and section S exists. **Negative controls** (inv. 68), each reverted with its MD5
  restored and the selftest green again:
  1. `"стоп"` removed from `bot.STOP_WORDS` → exit non-zero, section F failing;
  2. in `stop.choose`, `"S13"` replaced by `"S14"` → exit non-zero, section S failing;
  3. in `run.py`'s `on_term`, the `common.STOP_ACTIVE` test removed so that every SIGTERM writes `S7` →
     exit non-zero, section S failing.
- **V2. Syntax.** `python3 -m py_compile vps/common.py vps/bot.py vps/run.py vps/stop.py vps/selftest.py`
  and `bash -n vps/install.sh`.
- **V3. The strings.** `python3 -c` printing `S3`, `S4`, `S8` and `S12`–`S15` decoded, each compared with
  §12.1 — `equal` per id.
- **V4. The units.** C1.
- **V5. Scope.** `git diff --name-only origin/main...HEAD` lists exactly the nine files of §4.
- **V6. Nothing left.** C4, and `systemctl list-unit-files 'crypto-*'` unchanged from A1's.
- **V7. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main` receives
  nothing from this session but its report.

No regression: every section of `vps/selftest.py` that exists at `origin/main` stays green with its own
checks unchanged; F and S are the only sections that gain checks.

---

## 11. The report

Contract §10's template. **The first five lines after `## Status`:** (1) the STOP built and proven on this
host by C2 and C3, in effect when the merge is installed; (2) the size — how many of the six were read,
each class, and `Z1`, `Z0` or `open`; (3) the usage of every run at `high`, beside the reference; (4) the
stream — `D1`, `D0` or `open`, with both counts of every covered window; (5) the engine window — `E1` or
`E0`, with the count of records in it.

---

## 12. Dictated blocks

### 12.1 Russian strings — character for character

| Id | Where | Text |
|---|---|---|
| S3 | the bot: a run requested (changed) | «Анализ запущен — ответ придёт сюда. Остановить: СТОП.» |
| S4 | the bot: a run already active (changed) | «Анализ уже идёт — ответ придёт сюда. Остановить: СТОП.» |
| S8 | the bot: any other text (changed) | «Команды: ▶ Анализ рынка · СТОП» |
| S12 | the bot: a stop requested | «Останавливаю анализ…» |
| S13 | `stop.py`: the run stopped | «Анализ остановлен.» |
| S14 | the bot or `stop.py`: nothing to stop | «Анализ не идёт — останавливать нечего.» |
| S15 | `stop.py`: the unit still runs after the stop | «Остановить анализ не удалось.» |

`S8` is written as `"Команды: " + S1 + " · СТОП"`;
the ellipsis of `S12` is the one character U+2026.

### 12.2 The runs — classes and the size

```
T0, T1, T2   = the times of A1's install lines of TZ-57's, TZ-58's and TZ-59's trees
invocation   = the lines of crypto-run.service from one systemd line containing «Starting crypto-run.service»
               up to the next such line, or to R, after T0
active       = an invocation with neither «Deactivated successfully» nor «Failed with result» before R:
               printed, and excluded from every count below
K-oom        = it carries «Failed with result 'oom-kill'»
K-timeout    = it carries «Failed with result 'timeout'»
S            = it carries «crypto-run: stopped by the owner»
N            = its first summary line reads admitted=no
L            = its second summary line reads api_error_status=429
C            = its first summary line reads claude_exit=0 and is_error=false, with answer_chars above 0
F            = any other
precedence   = K-oom, K-timeout, S, N, L, C, F — the first that applies is the class

the six      = the first six invocations after T0 that are not active, in start order
Z1 — resize  = one of the six is K-oom or K-timeout, or more than one is N:
               the host is answered by 1 vCPU and 2 GB
Z0 — stays   = six are read, none is K-oom or K-timeout, at most one is N, at least one is C:
               the host stays at 1 vCPU and 1 GB, and the size is decided
open         = neither: the report names how many of the six it read, and nothing is decided

footprint    = memory_peak + memory_swap_peak of the third summary line; "-" when either reads "-"
duration_s   = the time of its third summary line − the time of its «Starting» line, in seconds
```

**Derivations.** The classes K-oom to F and their lines are TZ-58 §12.2's, read on this host. **`S` is
new:** no invocation can carry it before this TZ's merge, and it is registered so that every later
reading classes a stop the owner sent as measuring nothing about memory, as the account's refusal measures
nothing (map §10, quoted in §2); it precedes `N` because a stop during admission prints `admitted=no`.
`Z1` is map §10's rule, quoted in §2. `Z0` asks for a `C` because six runs that never completed one have
measured no fit.

### 12.3 Usage at `high`, and the `models=` field

```
at high        = an invocation whose «Starting» line is after T2: the run on claude-opus-5-5 at --effort high
reached        = its first summary line's claude_exit is not "-"
printed        = per reached invocation at high: class, num_turns, duration_ms, input_tokens, output_tokens,
                 cache_read_tokens, cache_creation_tokens, cost_usd, pinned_present, other_models
the reference  = map §10 item (17): the completed run of 03.10.2026 started 11:37:53Z, on the alias opus at
                 its default effort — 58 turns, 1 238 s, 83 752 output tokens, 11 941 234 cache-read
                 tokens, 10.09 USD — printed as the table's first row
models=        = printed as [withheld]; beside it pinned_present=yes when run.MODEL is one of the
                 comma-separated ids the field held and no otherwise, and other_models=<the count of
                 the other ids>
```

**Derivation.** The fields are `run.py`'s second and third summary lines (TZ-55 B2.4, TZ-56 §12.4); the
reference is TZ-58's report-2 as the map records it. **No bar is registered on the usage:** it is the
measurement the account's question waits on (inv. 49).

### 12.4 The stream against the list, and the engine window

```
the stream       = the records of /var/lib/crypto-auto/announcements.jsonl with received_ms at or after T1
generations      = the stamps g of the «exchange: list generation=…» lines after T1, in order, the
                   baseline line's included
window i         = (g_{i-1}, g_i] for consecutive generations; COVERED when g_{i-1} is at or after T1
list_new_i       = the new= of g_i's line
stream_i         = the count of the stream's records whose publishDate lies in window i
D0 — silent      = some covered window has list_new_i ≥ 1 and stream_i = 0
D1 — delivered   = no covered window is silent, and some covered window has list_new_i ≥ 1 and stream_i ≥ 1
open             = no covered window, or list_new_i = 0 in every covered one
the engine window = [T1, 2026-10-04T16:48:25Z]: the run of 04.10 read the exchange's list at 16:48:25Z and
                   its newest record was dated 02.10 13:00 (its appendix, «EXCHANGE LIST»)
E1 — stale       = at least one record of the stream has its publishDate in the engine window: each is
                   printed with its publishDate as UTC, its catalogName and its title
E0               = none
```

**Derivation.** The list's line and its `new=` are `exchange.list_poll`'s (TZ-58 §12.5); the record's
fields are `announce.record`'s; the comparison is map §10's, quoted in §2. A window that opened before the
stream was listed cannot be compared, so it is printed and never classed. The engine window starts at
`T1` because the stream delivers on publication and holds nothing published before it was listed.

### 12.5 `vps/common.py`

```
STOP_DIR    = SPOOL_DIR + "/stop"
STOP_ACTIVE = "/run/crypto-stop"          # crypto-stop.service's RuntimeDirectory
RUN_UNIT    = "crypto-run.service"
```

- `pending_requests()` — true when `REQUESTS_DIR` holds a file ending `.req` whose name does not start
  with `.`; a missing directory is false.
- `request_stop(source)` — one `<created_ms>-<source>-<pid>.stop` file, `{"source": …, "created_ms": …}`,
  into `STOP_DIR` through `atomic_write` with mode `0o660`, named the way `_write_request` names a request;
  returns `requested`. **It never consults `runs_enabled()`:** a stop is always allowed.
- `S3`, `S4` and `S8` change and `S12`–`S15` are added, by §12.1. The module docstring names TZ-60, and
  its sentence on §12.1 names TZ-60 §12.1 beside TZ-54's and TZ-55's.

### 12.6 `vps/bot.py`

```
STOP_WORDS = ("stop", "/stop", "стоп")


def is_stop(text):
    """The owner's stop: the text with surrounding whitespace and a trailing «!» or «.» removed,
    case-folded, is one of STOP_WORDS."""
    return isinstance(text, str) and text.strip().rstrip("!.").strip().casefold() in STOP_WORDS
```

- `classify` returns `"stop"` where `is_stop(text)` holds, after its `/start` and request tests and before
  `S8`; every other path of it is unchanged, the owner filter and the ten-minute age included.
- **The branch on the verdict leaves `service()` unchanged into `respond(api, owner, verdict)`**, which
  `service()` calls once per acted update, and gains one branch after the `S8` branch:

  ```
  elif verdict == "stop":
      if common.run_active() or common.pending_requests():
          common.request_stop("bot")
          api.send(owner, common.S12, keyboard=True)
      else:
          api.send(owner, common.S14, keyboard=True)
  ```

- The module docstring names TZ-60. `KEYBOARD` does not change: the stop is typed, never a button, so a
  stray tap cannot stop a run the owner wanted.

### 12.7 `vps/run.py`

`on_term` becomes exactly:

```
    def on_term(signum, frame):
        if os.path.exists(common.STOP_ACTIVE):
            common.log("crypto-run: stopped by the owner")
        elif in_session["on"] and not in_session["notified"]:
            in_session["notified"] = True
            common.write_outbox("notice", common.S7)
        summary()
        sys.exit(128 + signum)
```

The module docstring names TZ-60. Nothing else in the file moves.

### 12.8 `vps/stop.py` — created

```
stop.py [--unit <name>] [--spool <dir>]        defaults common.RUN_UNIT and common.SPOOL_DIR

RUNNING = ("active", "activating", "deactivating", "reloading", "refreshing")

consume(directory, suffix)  delete every file of directory ending with suffix whose name does not start
                            with "."; returns the count; a missing directory counts 0
unit_state(unit)            the first line of `systemctl is-active <unit>`'s stdout, stripped; "-" when empty
choose(before, requests_removed, after)
                            "S13" when before is in RUNNING or requests_removed > 0, and after is not in RUNNING
                            "S15" when before is in RUNNING or requests_removed > 0, and after is in RUNNING
                            "S14" otherwise
main(argv)                  in this order:
  1. stops    = consume(<spool>/stop, ".stop")          first, so that its path unit cannot loop
  2. requests = consume(<spool>/requests, ".req")
  3. before   = unit_state(unit)
  4. stop_exit  = the return code of `systemctl stop <unit>`
  5. reset_exit = the return code of `systemctl reset-failed <unit>`, its output captured and dropped
  6. after    = unit_state(unit)
  7. notice   = choose(before, requests, after); common.write_outbox("notice", <that string>,
                outbox_dir=<spool>/outbox)
  8. one line: crypto-stop: stops=<n> requests_removed=<n> before=<s> stop_exit=<n> reset_exit=<n>
               after=<s> notice=<S13|S14|S15>
  returns 1 under S15 and 0 otherwise
```

The module docstring names TZ-60 and states that the program reads no credential and starts no model.
**Derivations, probed by the Architect on a prototype of `choose`:** `(active, 0, inactive)` → `S13`;
`(activating, 0, failed)` → `S13`; `(inactive, 1, inactive)` → `S13`; `(inactive, 0, inactive)` → `S14`;
`(failed, 0, failed)` → `S14`; `(active, 0, active)` → `S15`; `(inactive, 1, activating)` → `S15`.
`reset-failed` clears the unit's failed state and start counter, so a stopped run neither stays failed nor
spends the run unit's `StartLimitBurst=3` against the next press.

### 12.9 The two units — created, exactly

`vps/units/crypto-stop.path`:

```
[Unit]
Description=Crypto assistant: a stop requested by the owner

[Path]
PathExistsGlob=/var/spool/crypto-auto/stop/*.stop
Unit=crypto-stop.service

[Install]
WantedBy=paths.target
```

`vps/units/crypto-stop.service`:

```
[Unit]
Description=Crypto assistant: stop the analysis run

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/stop.py
Environment=PYTHONDONTWRITEBYTECODE=1
RuntimeDirectory=crypto-stop
TimeoutStartSec=300
NoNewPrivileges=yes
ProtectSystem=strict
ProtectHome=yes
PrivateTmp=yes
ReadWritePaths=/var/spool/crypto-auto
MemoryAccounting=yes
MemoryMax=128M
```

**Derivations.** No `User=`: stopping a system unit is root's, and the unit holds no credential and runs
no model, so contract §7 item 6's clause on model sessions does not reach it. `TimeoutStartSec=300` covers
the run unit's default stop timeout of 90 s and the kill after it; `128M` is the ceiling of every other
small service of this host. The Architect's session read `systemd-analyze verify` exit 0 on these two files
under systemd 255.

### 12.10 `vps/install.sh` and `vps/manifest`

- `provision_dirs` gains `dir_as 2770 cryptoauto cryptoauto /var/spool/crypto-auto/stop` directly after the
  `requests` line; the header comment's list of units without `[Install]` names `crypto-stop.service`.
  Nothing else in the file moves.
- `vps/manifest` gains the line `crypto-stop.path`, after `crypto-announce.service`.

### 12.11 Selftest

**Section F gains eight rows** (`bot.classify`, the owner's private chat at `now` unless stated):

| Row | Known answer |
|---|---|
| `STOP` | `stop` |
| `стоп` | `stop` |
| `СТОП` | `stop` |
| `" Stop! "` | `stop` |
| `/stop` | `stop` |
| `стоп анализ` | `S8` |
| `STOP` from another private chat | `dropped` |
| `STOP` at `now − 601 s` | `dropped` |

**Section S is new — the owner's stop:**

1. `common.request_stop("bot")` with `common.STOP_DIR` at a temporary directory → returns `requested` and
   writes exactly one file ending `.stop`; `common.pending_requests()` is false on an empty requests
   directory and true with one `.req` in it.
2. `bot.respond` on section N's `MockApi`, `common.STOP_DIR` and `common.REQUESTS_DIR` at temporary
   directories: with `common.run_active` true → one `.stop` file and one message whose text is `S12`;
   with `run_active` false and no `.req` → no `.stop` file and one message `S14`; with `run_active` false
   and one `.req` → one `.stop` file and `S12`; the verdict `S8` → one message `S8`.
3. `stop.choose` on the seven rows of §12.8's derivation.
4. `stop.main(["--unit", "selftest-stop.service", "--spool", <tmp>])` with a stub `systemctl` first on
   `PATH` that records every argument list and answers `is-active` from a scripted sequence of states, every
   other command with exit 0:
   - states `active`, `inactive`, one `.req` and one `.stop` planted → returns 0; the stub saw, in order,
     `is-active`, `stop`, `reset-failed`, `is-active`, each on `selftest-stop.service`; `requests/` and
     `stop/` empty; one outbox file, `kind` `notice`, text `S13`; one printed line beginning `crypto-stop:
     stops=1 requests_removed=1 before=active stop_exit=0 reset_exit=0 after=inactive notice=S13`;
   - states `inactive`, `inactive`, nothing planted → returns 0, one notice `S14`;
   - states `active`, `active` → returns 1, one notice `S15`.
5. `run.main` under section O's fixtures with a stub `claude` that sends SIGTERM to its parent and then
   sleeps — caught as `SystemExit` with code 143, the SIGTERM handler restored afterwards:
   - `common.STOP_ACTIVE` at an existing temporary directory → the line `crypto-run: stopped by the owner`
     printed once, the three summary lines printed, no notice in the outbox;
   - `common.STOP_ACTIVE` at a path that does not exist → one notice whose text is `S7`, the line absent.

**Derivations.** The rows of F follow `is_stop`'s definition, probed by the Architect on a prototype: every
`stop` row reads `stop`, `стоп анализ` does not, and the filter's own rows are TZ-54 §12.4's. Item 5's
mechanism was probed by the Architect's session on Python 3.13: a SIGTERM a child sends its parent while
the parent waits in `subprocess.run` reaches the handler at once and leaves the call as `SystemExit(143)`.
Every other section keeps its checks unchanged.

---

## 13. Commit messages

Implementation, on the branch:

```
TZ-60: vps — the owner's STOP: the word stops the run, its session and every process it started
```

Report, on `main`:

```
TZ-60: report — the STOP, and the runs the button started after TZ-57's merge
```
