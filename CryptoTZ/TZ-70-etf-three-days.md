# TZ-70 — The ETF record carries the three newest US sessions of each type

**Canonical filename:** `CryptoTZ/TZ-70-etf-three-days.md`
**Report:** `CryptoReports/TZ-70-etf-three-days-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine**, because V4 reads SoSoValue from there with the key that lives there.
**Class:** branch TZ (contract §8) — it modifies two files under `vps/**` and nothing else.
**Branch:** `tz-70-etf-three-days`, from `origin/main` · **Model:** Sonnet
**Trigger:** `EXECUTE TZ-70`, with nothing under it: no credential arrives, and the key TZ-69 wrote stays where it is.
**Written against:** contract v31, map `2026-10-24-a` and methodology `2026-10-24-a`, the last two uploaded with this TZ,
and `main` at `2384361` — its `vps` tree `9e51983fa9e2b39a821a68e07d8f69fc410ff3c6` — read by the Architect from the
repository on 24.10.2026. Methodology `2026-10-24-a` §16 step D already reads the key this TZ adds, and prints one
session until the record carries three.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-24-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-24-a.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | its version line reads `**Version 31.**` — a lower version is BLOCKED; lines and MD5 reported |
| `vps/etf.py` | 146 | `3a1f4303273efdc82f49d80c3a119063` | reported; a different value is a finding, and A1.2 decides |
| `vps/selftest.py` | 2179 | `a67871ef4f25a76ccce41aadcbe7cf13` | reported; a different value is a finding, and A1.3 decides |

The map itself: 2790 lines, MD5 `d0b235fe0c94d3a14b7e543f9379e846` — reported, not enforced.

---

## 1. Credentials

**None arrives.** The one this session touches is the SoSoValue API key TZ-69 wrote to
`/etc/crypto-auto/credentials/sosovalue-api-key`, and it touches it only by V4's transient unit, which receives it as a
systemd credential, and by V5's search, which reads it from its file and prints nothing of it. **No value is printed,
logged, committed or quoted** — in the report, a commit, a check's label or the chat. No other credential is read, no
model session is opened, and nothing is enabled from the branch.

---

## 2. Contract, map and methodology text this TZ obeys

Contract v31, §7 item 6, quoted:

> Each value lives in its own file under `/etc/crypto-auto/credentials/`,
> outside the repository, mode `0600`, owned by root

> **No value is ever
> printed, logged, committed or quoted** — in a report, a day log, a commit, a unit file or
> the chat.

Contract v31, §7 item 15, quoted: «An implementation session never enables, starts or leaves running a persistent unit,
timer or service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its
report proves none is left behind.»

Map inv. 72, quoted: «A write that fails leaves this run's product or nothing — never a partial file and never the
previous run's.» The record stays written whole through `common.atomic_write` or not at all.

Map §10, row «ETF flow figures have no reachable primary lane», at `2026-10-24-a`, quoted: «**Open since 24.10.2026 —
TZ-70:** the owner asked for the last three sessions, and the record keeps per type `days`, the three newest US sessions
newest first, each `{"date", "net"}`, beside the newest one's own fields — schema `v` 1, the key additive».

Methodology `2026-10-24-a` §16 step D, the read this TZ serves — its command, quoted:

```
python3 -c 'import json;d=json.load(open("/var/lib/crypto-auto/etf.json"));print(d["k"],d["ts"],d["provider"],d["host"],d["refused"]);[print(t,e["date"],e["net"],e["rows"],json.dumps(e.get("days"))) for t,e in d["types"].items()]'
```

and its rule: «the trading days are the dates of `us-btc-spot`'s `days`, newest first — its `date` alone where its
`days` prints `null`».

---

## 3. What is built, and why

**The owner asked on 24.10.2026 for the US ETF flows of the last three days; the record holds one.** `vps/etf.py` already
receives every session of every type — 300, 300 and 248 rows on 24.10.2026 — and keeps only the newest. This TZ keeps
three; the methodology prints them.

1. **`vps/etf.py`:**
   - `ETF_DAYS = 3`, with the comment `# Derived: the owner's request of 24.10.2026 — the three newest US sessions.`;
   - a function `recent(data, n)`: the rows of `data` that `newest()` could choose — a `dict` whose `date` is a string
     of form `YYYY-MM-DD` and whose `totalNetInflow` casts to a finite float by `finite()` — **one per date, the first
     in `data`'s order where a date is given twice** (the row `newest()` keeps, since it replaces only on a greater
     date), ordered by date newest first, the first `n` of them, each `{"date": <date>, "net": <the finite float>}`;
   - `entry()` adds `out["days"] = recent(data, ETF_DAYS)` after the fields it writes now. **Nothing else in the file
     moves** — `newest()`, `read_type()`, `main()`, the refusals, the printed line, the write, the mode and the exits —
     and `days[0]` is always `{"date": out["date"], "net": out["net"]}`;
   - the record keeps `"v": 1`: the key is additive, and every reader of the other keys reads them unchanged.
2. **`vps/selftest.py`, section Y** — new checks, against stubs, no network:
   - `etf.ETF_DAYS` is 3;
   - from a newest-first list of four valid rows and from the same list oldest-first: `days` is the three greatest
     dates newest first, each with its net;
   - from the existing `skipped` fixture (a date not of form `YYYY-MM-DD`, an absent net, a `NaN` net beside valid
     rows): `days` holds only the valid rows, newest first;
   - from two valid rows, two entries; from one, one;
   - a date given twice with two nets: one entry for it, carrying the first one's net, and `days[0]` equal to the
     entry's `date` and `net`;
   - end to end through `y_run`: the written record's entry for a type read carries `days`, its first element equal to
     that entry's `date` and `net`.
   **The checks' count is the Executor's to derive and to report** (a known answer the Architect has not probed is
   specified by its shape); section Y rises from 44 by exactly that count, and no other section moves.

*[Architect's decision, TZ-70: three sessions in the record beside the newest one's fields, the schema version kept.
Discarded: the whole `data` array, which the run would read through a command that prints it — 300 rows a type in
the hunter's context for three it uses; a `v` 2 record, which no reader needs; a second file, a second writer for one
artifact (inv. 72).]*

---

## 4. Scope

### Files to Create

None.

### Files to Modify

```
vps/etf.py    vps/selftest.py
```

### Files to Delete

None.

### On the VPS

V4's transient unit, its measurement record and its scratch copy, the last two removed before the report.

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **How the run prints the days.** `ANALYST-INSTRUCTIONS.md` is the Architect's, and `2026-10-24-a` already prints them
  from `days`.
- **The XRP and BNB types, the unit, the timer, the manifest and every other file under `vps/`.** None moves.
- **The search that stands in where the record does not** (methodology §16 step D). It stays one session.

---

## 6. Rules — binding in every stage

1. **The key never appears on a command line, in a shell variable echoed, in a file but its own, or in any output.** It is
   read from its file by the program that needs it.
2. **SoSoValue is called at most six times by this session** — V4's three, with three in reserve for one repeat — and
   never in a loop.
3. **Nothing is enabled, started or left running from the branch** but V4's transient unit (contract §7 item 15).
4. **Python 3.12's standard library only.**

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service crypto-etf.timer`;
  `test -d /srv/crypto-auto/.git && echo clone`; `id -u cryptorun`;
  `stat -c '%a %U %G' /etc/crypto-auto/credentials/sosovalue-api-key`. **Known answers:** `vultr`; `active` three times;
  `clone`; `995`; `600 root root`. **Derived:** TZ-69's A0 and A2 on this host, and the run of 24.10.2026, whose hunt
  read a record the timer wrote at 08:07:01Z. **Any other answer: BLOCKED.** The session writes a report carrying A0's
  lines and its own `hostname`, commits it to `main`, and does nothing else.
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/main:vps`. **Known answer:** `9e51983fa9e2b39a821a68e07d8f69fc410ff3c6`. **Derived:** the
     Architect read it at `2384361`. A different value is a finding, never a block on its own.
  2. `grep -c 'days' vps/etf.py`. **Known answer:** `0`. **Derived:** the Architect's reading of `vps/etf.py` at
     `2384361`. Anything else: BLOCKED — the key exists already, and the change is the Architect's to re-read.
  3. On `origin/main`'s tree, `python3 vps/selftest.py`. **Known answer:** exit 0 and
     `selftest: sections 25 checks 501 failed 0 empty 0`, section Y at `44`. **Derived:** the Architect's session ran
     exactly this on 24.10.2026 on `main`'s `vps` tree, with methodology `2026-10-24-a` in place and with `2026-10-22-b`.
  4. As root, the methodology's command of §2 on the live record. **Known answer:** a first line beginning `etf ` and
     ending `SoSoValue openapi.sosovalue.com {}`, then three lines, one per type, each ending `null`. **Derived:**
     methodology `2026-10-24-a` §16 step D and `vps/etf.py` at `2384361`, whose `entry()` writes no `days` — the read
     already runs on the record as it stands.

---

## 8. Stage B — the code, on the branch

- **B1.** `git checkout -b tz-70-etf-three-days origin/main`; §3's two files edited; V1–V3 green.
- **B2.** V4 and V5 on the VPS.
- **B3.** Commit, push the branch, open the pull request (contract §8); `main` receives only the report.

---

## 9. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0, `selftest: sections 25 checks <501 + n> failed 0
  empty 0`, every section A–X at its A1.3 count and section Y at `44 + n`, `n` reported. **Negative controls**
  (inv. 68), each applied alone in `vps/etf.py`, then reverted and V1 green again — in each, a named non-empty set of
  section Y's new checks fails and every check of sections A–X and of Y's 44 stays green; the report names each
  control's failing checks:
  1. `days` ordered oldest first;
  2. on a date given twice, the last occurrence kept;
  3. `ETF_DAYS = 2`.
- **V2. Syntax.** `python3 -m py_compile vps/etf.py vps/selftest.py`.
- **V3. Nothing else moves.** `git diff origin/main...HEAD -- vps/etf.py`: its hunks add `ETF_DAYS`, `recent()` and the
  one line of `entry()`, and touch no line of `newest()`, `read_type()`, `main()` or `Refused`. The report quotes the
  hunks.
- **V4. The record, measured on the VPS.** The branch's `vps/etf.py` and `vps/common.py` copied to a scratch directory
  `cryptoauto` can read, then run once as a transient unit — `systemd-run --wait --collect --pipe --uid=cryptoauto
  --gid=cryptoauto -p LoadCredential=sosovalue-api-key:/etc/crypto-auto/credentials/sosovalue-api-key /usr/bin/python3
  <scratch>/etf.py --out /var/lib/crypto-auto/etf-tz70.json`. **Known answer:** exit 0, the line
  `etf: read=3 refused=0 written=yes newest=<a date>`, and a record of mode `640 cryptoauto cryptoauto` whose three
  types each carry `days` of three entries, newest first, the first equal to that type's `date` and `net`.
  **Derived:** SoSoValue answered 300, 300 and 246 rows per type to TZ-69's V4 on 21.10.2026 and the record read on
  24.10.2026 carried 300, 300 and 248 — three sessions stand on every type. Then the methodology's command of §2, with
  `/var/lib/crypto-auto/etf.json` replaced by the scratch record's path and nothing else changed, run once: **known
  answer** three type lines each ending in a JSON list of three `{"date", "net"}` objects — the report quotes its
  output. Then the record and the scratch are removed, and `systemctl list-units --all --no-legend 'run-*'` shows no
  unit of this session left (contract §7 item 15).
- **V5. The value's absence.** One search for the key's value — read from its file by the search command and never
  printed — across the branch's diff, the report, V4's captured output and every file the session wrote. **Known
  answer:** no match. The report states the command and the result, never the value.
- **V6. Scope.** `git diff --name-only origin/main...HEAD` lists exactly `vps/etf.py` and `vps/selftest.py`.
- **V7. Nothing in effect before the merge.** A1.4's command on the live record, run again at the end of the session:
  every type line still ends `null` — the deployer installs the change only from `main`.

No regression: sections A–X keep their counts, section Y's 44 checks stay green, and no file outside §4 moves.

---

## 10. The report

Contract §10's template. **The first three lines after `## Status`:**

1. **The record** — V4's printed line, and per type the three dates and net flows in USD.
2. **The read** — the methodology's command on V4's record, its three type lines quoted.
3. **The checks** — V1's total, `n`, and each control's failing checks.

---

## Commit Message

Implementation, on the branch:

```
TZ-70: vps — the ETF record keeps the three newest US sessions of each type as days, the owner's request of 24.10.2026
```

Report, on `main`:

```
TZ-70: report — the ETF record's three sessions
```
