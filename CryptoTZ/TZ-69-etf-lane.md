# TZ-69 — The ETF lane: SoSoValue's daily net flows for the US spot ETFs, read hourly on the VPS by a unit that runs no model, into a record the analysis run reads

**Canonical filename:** `CryptoTZ/TZ-69-etf-lane.md`
**Report:** `CryptoReports/TZ-69-etf-lane-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine**, because A2 writes a credential there and A3 and V4 read SoSoValue from there.
**Class:** branch TZ (contract §8) — it creates and modifies files under `vps/**` only.
**Branch:** `tz-69-etf-lane`, from `origin/main` · **Model:** Opus
**Trigger:** `EXECUTE TZ-69`, with one line under it: `SOSOVALUE_API_KEY=<the owner's key>` (contract §7 item 6).
**Written against:** contract v31, map `2026-10-21-b` and methodology `2026-10-21-a`, all three uploaded with this TZ, and
`main` at `ed0de2d` — its `vps` tree `11bb152889801388df439537b66e2a52732150b4` — read by the Architect from the
repository on 21.10.2026. The map's row «ETF flow figures have no reachable primary lane» decides this lane; the
methodology moves the hunter's ETF read onto its record only at this TZ's audit, against the record's real fields.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-21-b.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-21-b.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | its version line reads `**Version 31.**` — a lower version is BLOCKED (inv. 59): v30 does not admit the key; lines and MD5 reported |
| `vps/selftest.py` | 1965 | `18f1a8a38dade5a2f73fd89353ca8f67` | reported; a different value is a finding, and A1.3 decides |
| `vps/manifest` | 8 | `36b72e41d6f2e6f49f4f033126aa2a23` | reported; a different value is a finding |

The map itself: 2788 lines, MD5 `01818e7f4c9ee26ada455d153d7eee00` — reported, not enforced.

---

## 1. Credentials

**One arrives: `SOSOVALUE_API_KEY`, the owner's SoSoValue API key, on the line under the trigger** — the only place it is
ever typed (contract §7 item 6). A2 writes it to `/etc/crypto-auto/credentials/sosovalue-api-key`, mode `0600`, owned by
root, without echoing it; from then on it is read only by a command that prints a count, by A3's one-liner, and by the
unit this TZ builds, which receives it as a systemd credential. **No value is printed, logged, committed or quoted** —
in the report, a commit, a unit file, a check's label or the chat — and V5 proves it absent from everything the session
wrote. No other credential is read or written, no model session is opened, and nothing is enabled from the branch.

---

## 2. Contract and map text this TZ obeys

Contract v31, §7 item 6, quoted:

> **Never commit secrets.** Credentials live only in GitHub Actions environment
> variables (inv. 7), **with exactly five exceptions, all on the VPS:**

> that run alone; and, since v31, the SoSoValue API key, read only by the ETF lane's unit, which runs no model.

> **A value arrives once, from the Boss, in the trigger message of the TZ that names it** —
> one `NAME=value` line under the trigger line — and that message is the only place a
> credential is ever typed.

**A unit that runs a model session holds exactly two credentials** (the same item): the run unit's own Claude login and
the deploy key. `crypto-run.service` does not change, and the record reaches the run as a file, never as a credential.

Contract §7 item 15: an implementation session «may start TRANSIENT units from its branch for a measurement its TZ names,
and its report proves none is left behind»; merge is deployment, so the timer this TZ adds runs only once the deployer
installs the merge.

Map inv. 72: «A write that fails leaves this run's product or nothing» — the record is written whole through
`common.atomic_write` or not at all.

Map §10, row «ETF flow figures have no reachable primary lane», decided at `2026-10-21-b`: `vps/etf.py`, run hourly by
`crypto-etf.timer` as the announcement stream's user with the key as its one credential, reads SoSoValue's
`historicalInflowChart` for the US BTC, ETH and SOL spot types and writes the newest US session of each to
`/var/lib/crypto-auto/etf.json` — not into the payload, which keeps the Shortcut's schema (`vps/writer.py`).

---

## 3. What is built, and why

**The owner's ETF section has printed nothing on runs whose two searches found no publication naming the day and the
provider** — the run of 21.10.2026 among them — while the provider's own API answers his key. This TZ builds the read;
the methodology edit at its audit makes the run use it.

1. **`vps/etf.py`, new** — Python 3.12's standard library and `vps/common.py` only:
   - `etf.py [--out PATH]`, default `common.STATE_DIR` + `/etf.json`, i.e. `/var/lib/crypto-auto/etf.json`;
   - the key: `$CREDENTIALS_DIRECTORY/sosovalue-api-key`, whitespace stripped; absent or empty → the printed line, exit
     `3`, no request made and nothing written;
   - per type of `TYPES = ("us-btc-spot", "us-eth-spot", "us-sol-spot")`, one request, no retry — the next hour is the
     retry: `POST https://openapi.sosovalue.com/openapi/v2/etf/historicalInflowChart`, headers `Content-Type:
     application/json` and `x-soso-api-key: <key>`, body `{"type": "<type>"}`, timeout `ETF_TIMEOUT_S = 40` — **Derived:**
     the Architect's reading of 16.10.2026, where one call timed out at 25 s and answered within 40 s;
   - an answer is accepted only where it parses, `code` is `0` and `data` is a list; its row is the one with the
     greatest `date` of form `YYYY-MM-DD` whose `totalNetInflow` casts to a finite float, and the type is recorded as
     `{"date", "net", "traded", "assets", "cum", "rows"}` — `totalNetInflow`, `totalValueTraded`, `totalNetAssets` and
     `cumNetInflow` cast to finite floats or `null`, `rows` the length of `data`. **The newest row is chosen by `date`,
     never by position**, whatever order the list arrives in;
   - anything else refuses that type and names why, in a closed vocabulary: `HTTP <status>`, `transport <exception
     class>`, `unparseable`, `code <value>`, `no row`;
   - the record, written through `common.atomic_write(out, record, mode=0o640)` only where at least one type was read:
     ```
     {"v": 1, "k": "etf", "ts": "<read moment, ISO-8601 Z>", "provider": "SoSoValue", "host": "openapi.sosovalue.com",
      "types": {"<type>": {"date", "net", "traded", "assets", "cum", "rows"}, …},
      "refused": {"<type>": "<reason>", …}}
     ```
     every type read stands in `types`, every other in `refused`; with none read nothing is written — the record left
     standing carries its own `ts` — and the exit is `4`;
   - one printed line, `etf: read=<n> refused=<n> written=<yes|no> newest=<the greatest date read, or ->`, exit `0` when
     written. **The key, the header and the request body are never printed**, nor anything the answer carried but the
     date.
2. **`vps/units/crypto-etf.service`, new**, in `crypto-cleanup.service`'s shape — `Type=oneshot` and no `[Install]`
   section, so the installer's `installable()` never disables it — running as the announcement stream does:
   `User=cryptoauto`, `Group=cryptoauto`, exactly one
   `LoadCredential=sosovalue-api-key:/etc/crypto-auto/credentials/sosovalue-api-key`,
   `ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/etf.py`, `Environment=PYTHONDONTWRITEBYTECODE=1`,
   `NoNewPrivileges=yes`, `CapabilityBoundingSet=`, `ProtectSystem=strict`, `ProtectHome=yes`, `PrivateTmp=yes`,
   `ReadWritePaths=/var/lib/crypto-auto`, `MemoryAccounting=yes`, `MemoryMax=64M`, `TimeoutStartSec=300`, and
   `Wants=`/`After=network-online.target`.
3. **`vps/units/crypto-etf.timer`, new** — `OnCalendar=*-*-* *:07:00 UTC`, `Persistent=true`,
   `Unit=crypto-etf.service`, `[Install]` `WantedBy=timers.target`. **Three calls an hour is about 2 200 a month against
   the key's 10 000 and 10 a minute** (the reading of 16.10.2026), and an hourly read holds the newest session at most an
   hour behind its publication whenever the owner presses.
4. **`vps/manifest`** — `crypto-etf.timer` added, once; `crypto-etf.service` not listed, as `crypto-cleanup.service`
   is not.
5. **`vps/selftest.py`** — a new section `Y`, against stubs, no network: the newest row chosen from a list newest-first
   and from one oldest-first; each refusal of the vocabulary from its own stubbed answer; one type read and two refused
   writes a record of one type with two named refusals; none read writes nothing and exits `4`; an absent key exits `3`
   with no request made; the key travels in the `x-soso-api-key` header and in no URL or body; a known fake key absent
   from the printed line and from the record; the record's mode `0640`; the unit file's user, its one credential line,
   its oneshot type and its missing `[Install]`; the timer's calendar, its unit and its `[Install]`; the manifest listing
   the timer once and the service not at all. **The section's check count is the Executor's to derive and to report**
   (canon: a known answer the Architect has not probed is specified by its shape).

*[Architect's decision, TZ-69: the record beside the stream's, on the stream's user — the payload keeps the Shortcut's
schema and the run already reads that directory. Discarded: the payload, which would change `vps/writer.py`'s fixed
keys and the gate's input; a GitHub Actions secret and a workflow, whose schedule lands hours late on this repository
(map §10, row «The journal lands four to seven hours after its schedule»); a credential in the run unit, which the floor
forbids.]*

---

## 4. Scope

### Files to Create

```
vps/etf.py    vps/units/crypto-etf.service    vps/units/crypto-etf.timer
```

### Files to Modify

```
vps/manifest    vps/selftest.py
```

### Files to Delete

None.

### On the VPS

`/etc/crypto-auto/credentials/sosovalue-api-key` (A2), and V4's transient unit, its measurement record and its scratch
copy, the last two removed before the report.

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **How the run uses the record.** `ANALYST-INSTRUCTIONS.md` is the Architect's, and its §16 step D moves onto the record at
  this TZ's audit, against the fields V4 reads.
- **The XRP and BNB types.** They answered `code` 0 with no rows on 16.10.2026; adding them is one line once they carry rows.
- **The payload, the writer, the gate and every unit but the two new ones.** None moves.

---

## 6. Rules — binding in every stage

1. **The key never appears on a command line, in a shell variable echoed, in a file but its own, or in any output.** It is
   read from its file by the program that needs it.
2. **SoSoValue is called at most nine times by this session** — A3's three and V4's three, with three in reserve for one
   repeat of either — and never in a loop.
3. **Nothing is enabled, started or left running from the branch** but V4's transient unit (contract §7 item 15).
4. **Python 3.12's standard library only.**

---

## 7. Stage A — readings, no writes but A2's

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`; `test -d /srv/crypto-auto/.git && echo clone`;
  `id -u cryptorun`. **Known answers:** `vultr`; `active` twice; `clone`; `995`. **Derived:** TZ-66's A0, which TZ-64's
  report read on this host on 16.10.2026. **Any other answer: BLOCKED.** The session writes a report carrying A0's lines
  and its own `hostname`, commits it to `main`, and does nothing else.
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/main:vps`. **Known answer:** `11bb152889801388df439537b66e2a52732150b4`. **Derived:** the
     Architect read it at `ed0de2d`. A different value is a finding, never a block — this TZ adds files.
  2. `grep -c '^crypto-etf' vps/manifest; ls vps/units | grep -c '^crypto-etf'`. **Known answers:** `0` and `0`.
     **Derived:** the Architect's reading of both at `ed0de2d`. Anything else: BLOCKED — the lane exists already.
  3. On `origin/main`'s tree, `python3 vps/selftest.py`. **Known answer:** exit 0 and
     `selftest: sections 24 checks 457 failed 0 empty 0`. **Derived:** the Architect's session read exactly this on
     21.10.2026, on `main`'s `vps` tree with methodology `2026-10-21-a`.
- **A2. The key.** The trigger message's `SOSOVALUE_API_KEY=` line written to
  `/etc/crypto-auto/credentials/sosovalue-api-key` under rule 1; then `stat -c '%a %U %G' <file>` and `wc -c < <file>`.
  **Known answers:** `600 root root`, and a count above zero. **Derived:** contract §7 item 6's mode and owner. **No
  such line in the trigger message: BLOCKED**, and the report says the line was absent, never what the message held.
- **A3. The reach from the VPS.** One request per type of §3's `TYPES`, as §3 item 1 makes it, by one Python one-liner
  run as root that reads the key from its file; recorded per type: the HTTP status, `code`, the length of `data`, the
  greatest `date`, and the keys of the row carrying it — never the key, never a header. **Known answer:** `200`, `0`, at
  least one row for each of the three types, and keys including `date` and `totalNetInflow`. **Derived:** the Architect's
  reading of 16.10.2026 from its own workspace — the VPS's reach is unmeasured, which is why this is read before code.
  **A refusal by the host on all three — a 403, a challenge page or a timeout: BLOCKED**, with the reading in the report;
  the route is then the Architect's. A type answering otherwise is a finding and the work goes on.
- **A4.** `stat -c '%a %U %G' /var/lib/crypto-auto` and `grep -n 'installable()' vps/install.sh`. **Known answers:**
  `750 cryptoauto cryptoauto`, and `installable() { grep -q '^\[Install\]' "$UNITS/$1"; }`. **Derived:** `vps/install.sh`
  as the Architect read it at `ed0de2d` — `dir_as 0750 cryptoauto cryptoauto /var/lib/crypto-auto` and line 170.

---

## 8. Stage B — the code, on the branch

- **B1.** `git checkout -b tz-69-etf-lane origin/main`; §3's five files written; V1–V3 green.
- **B2.** V4 and V5 on the VPS.
- **B3.** Commit, push the branch, open the pull request (contract §8); `main` receives only the report.

---

## 9. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0, `selftest: sections 25 checks <457 + Y> failed 0
  empty 0`, every section A–X at its A1.3 count, and section Y's count reported. **Negative controls** (inv. 68), each
  applied alone in `vps/etf.py` or the unit file, then reverted and V1 green again — in each, a named non-empty set of
  section Y's checks fails and every check of sections A–X stays green; the report names each control's failing checks:
  1. the newest row chosen as the first row of `data` rather than by `date`;
  2. the key added to the printed line;
  3. the record written with mode `0o644`;
  4. a second `LoadCredential=` line in `crypto-etf.service`.
- **V2. Syntax.** `python3 -m py_compile vps/etf.py vps/selftest.py`.
- **V3. Units.** `systemd-analyze verify vps/units/crypto-etf.service vps/units/crypto-etf.timer` silent;
  `systemd-analyze calendar '*-*-* *:07:00 UTC'` prints a next elapse within the hour.
- **V4. The lane, measured on the VPS.** The branch's `vps/etf.py` and `vps/common.py` copied to a scratch directory
  `cryptoauto` can read, then run once as a transient unit — `systemd-run --wait --collect --pipe --uid=cryptoauto
  --gid=cryptoauto -p LoadCredential=sosovalue-api-key:/etc/crypto-auto/credentials/sosovalue-api-key /usr/bin/python3
  <scratch>/etf.py --out /var/lib/crypto-auto/etf-tz69.json`. **Known answer:** exit 0, the line
  `etf: read=3 refused=0 written=yes newest=<A3's greatest date>`, and a record of mode `640 cryptoauto cryptoauto`
  whose `types` carry A3's three dates. **Derived:** A3's reading on the same host the same day. The report quotes the
  printed line, the record's `ts`, and per type `date`, `net` and `rows`; then the record and the scratch are removed and
  `systemctl list-units --all --no-legend 'run-*'` shows no unit of this session left (contract §7 item 15).
- **V5. The value's absence.** One search for the key's value — read from its file by the search command and never
  printed — across the branch's diff, the report, V4's captured output and every file the session wrote. **Known answer:**
  no match. The report states the command and the result, never the value.
- **V6. Scope.** `git diff --name-only origin/main...HEAD` lists exactly §4's five files.
- **V7. Nothing in effect before the merge.** `systemctl list-timers --all --no-legend crypto-etf.timer` prints nothing.

No regression: sections A–X keep their counts, and no file outside §4 moves.

---

## 10. The report

Contract §10's template. **The first three lines after `## Status`:**

1. **The reach** — A3 per type: status, `code`, rows and the greatest date.
2. **The record** — V4's printed line, and per type the date and the net flow in USD.
3. **The checks** — V1's total, section Y's count, and each control's failing checks.

---

## Commit Message

Implementation, on the branch:

```
TZ-69: vps — the ETF lane: SoSoValue's daily net flows for the US BTC, ETH and SOL spot ETFs, read hourly by a unit that runs no model into /var/lib/crypto-auto/etf.json
```

Report, on `main`:

```
TZ-69: report — the ETF lane
```
