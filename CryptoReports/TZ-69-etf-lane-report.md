# Implementation Report — TZ-69

## Status

**COMPLETED.**

1. **The reach** (A3, from the VPS `vultr`, one request per type): `us-btc-spot` — HTTP `200`, `code 0`, `300` rows,
   greatest date `2026-10-20`; `us-eth-spot` — `200`, `code 0`, `300` rows, `2026-10-20`; `us-sol-spot` — `200`, `code 0`,
   `246` rows, `2026-10-20`. The row carrying each greatest date has keys
   `cumNetInflow, date, totalNetAssets, totalNetInflow, totalValueTraded`.
2. **The record** (V4): `etf: read=3 refused=0 written=yes newest=2026-10-20`. Per type, date and net flow in USD:
   `us-btc-spot` 2026-10-20, `23162422.509999998` (+23.16 M); `us-eth-spot` 2026-10-20, `-26134272.7` (−26.13 M);
   `us-sol-spot` 2026-10-20, `-2649009.0` (−2.65 M).
3. **The checks** (V1): `selftest: sections 25 checks 501 failed 0 empty 0`; section Y **44** checks. Controls: (1)
   newest by first row → 4 section-Y checks fail; (2) key in the printed line → 4; (3) mode `0o644` → 1; (4) a second
   `LoadCredential=` → 1. Sections A–X are green in every control. The failing checks are named under `## Validation`.

The previous TZ's branch was merged: TZ-68's `tz-68-book-due-entry` reached `main` as `b130341` (PR #56).

## Inbound Filing

None. `CryptoTZ/TZ-69-etf-lane.md` is on `origin/main` at its canonical filename (blob `30cfd05d`), filed by the
upload `ad0ac70`.

## Scope Executed

**Class: branch TZ** (contract §8) — `## Scope` names five files under `vps/**`, all outside `CryptoReports/**`.

- Stage A: A0–A4, all at their known answers (below).
- Stage B: §3's five files on branch `tz-69-etf-lane` from `origin/main` (`4148a6a`); V1–V7 run; commit, push, pull
  request #57.
- On the VPS: `/etc/crypto-auto/credentials/sosovalue-api-key` written (A2); V4's transient unit run once, its
  measurement record and its scratch copy removed.

## Files Created

| File | Lines | MD5 |
|---|---:|---|
| `vps/etf.py` | 146 | `3a1f4303273efdc82f49d80c3a119063` |
| `vps/units/crypto-etf.service` | 21 | `0728d10a0d67994468db6c1facc9c41a` |
| `vps/units/crypto-etf.timer` | 10 | `6f0aba48aa01439e0e4d790c95edbd0e` |

Outside the repository (TZ §4 «On the VPS»): `/etc/crypto-auto/credentials/sosovalue-api-key`, `600 root root`.

## Files Modified

| File | Lines before → after | MD5 after |
|---|---|---|
| `vps/manifest` | 8 → 9 (`crypto-etf.timer` appended) | `75a0f5a71f6111ecca0553620f1eea4c` |
| `vps/selftest.py` | 1965 → 2179 (section Y, its import, its `SECTIONS` row, the docstring's TZ list) | `a67871ef4f25a76ccce41aadcbe7cf13` |

## Files Renamed

None.

## Files Deleted

None in the repository. On the VPS, V4's own record `/var/lib/crypto-auto/etf-tz69.json` and its scratch directory
`/tmp/tz69-etf.MidaBQ` were removed, as TZ §4 and V4 require.

## Implementation Summary

**`vps/etf.py`** — standard library and `vps/common.py` only.

- `etf.py [--out PATH]`, default `common.STATE_DIR + "/etf.json"` = `/var/lib/crypto-auto/etf.json`.
- The key through `common.load_credential("sosovalue-api-key")`: `$CREDENTIALS_DIRECTORY/sosovalue-api-key`, whitespace
  stripped; absent directory, absent file or empty value → `CredentialMissing` → the printed line, exit `3`, no request
  made, nothing written. `load_credential` also registers the value with `common.redact`, and the line is printed
  through `common.log`, which redacts — defence in depth; the selftest proves the line carries neither the key nor
  `<redacted>`.
- Per type of `TYPES = ("us-btc-spot", "us-eth-spot", "us-sol-spot")`, `read_type()` makes one
  `POST https://openapi.sosovalue.com/openapi/v2/etf/historicalInflowChart`, headers `Content-Type: application/json`
  and `x-soso-api-key`, body `{"type": "<type>"}`, `timeout=ETF_TIMEOUT_S` (`40`), no retry.
- `entry()` accepts an answer only where it parses, `code` is `0` and `data` is a list; `newest()` returns the row with
  the greatest `YYYY-MM-DD` `date` whose `totalNetInflow` casts to a finite float, comparing dates and never using a
  position. The entry is `{"date", "net", "traded", "assets", "cum", "rows"}` from `totalNetInflow`, `totalValueTraded`,
  `totalNetAssets`, `cumNetInflow` cast by `finite()` (finite float or `null`) and `rows = len(data)`.
- Refusals in the closed vocabulary: `HTTP <status>`, `transport <exception class>`, `unparseable`, `code <value>`,
  `no row`.
- The record `{"v": 1, "k": "etf", "ts", "provider": "SoSoValue", "host": "openapi.sosovalue.com", "types", "refused"}`
  through `common.atomic_write(out, record, mode=0o640)` only when `types` is non-empty; otherwise nothing is written
  and the exit is `4`.
- One line `etf: read=<n> refused=<n> written=<yes|no> newest=<date|->`, exit `0` when written.

**`vps/units/crypto-etf.service`** — `Type=oneshot`, no `[Install]`, `User=`/`Group=cryptoauto`, one
`LoadCredential=sosovalue-api-key:/etc/crypto-auto/credentials/sosovalue-api-key`,
`ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/etf.py`, `Environment=PYTHONDONTWRITEBYTECODE=1`, `NoNewPrivileges=yes`,
`CapabilityBoundingSet=`, `ProtectSystem=strict`, `ProtectHome=yes`, `PrivateTmp=yes`,
`ReadWritePaths=/var/lib/crypto-auto`, `MemoryAccounting=yes`, `MemoryMax=64M`, `TimeoutStartSec=300`,
`Wants=`/`After=network-online.target` — §3 item 2's list and nothing else.

**`vps/units/crypto-etf.timer`** — `OnCalendar=*-*-* *:07:00 UTC`, `Persistent=true`, `Unit=crypto-etf.service`,
`[Install] WantedBy=timers.target`.

**`vps/manifest`** — `crypto-etf.timer` appended once; `crypto-etf.service` not listed.

**`vps/selftest.py`** — section Y, 44 checks against stubbed `urlopen` answers, no network: the newest row from a
newest-first and an oldest-first list, and past rows whose net is absent or NaN or whose date is malformed; each
refusal of the vocabulary from its own stubbed answer (`HTTP 503`, `transport TimeoutError`, `unparseable` for a
non-JSON body, `code 40001`, `no row`, plus `unparseable` for a non-list `data` and `HTTP 204` for a non-200 status);
none read → exit 4, nothing written, and a standing record left byte-identical; one read and two refused → a record of
one type with `HTTP 429` and `no row`, every field and its cast, key order, `ts` shape, mode `0640`; three requests,
one per type in order, each a POST to the exact URL with timeout 40, the key in `x-soso-api-key` and in no URL or body;
the fake key absent from the printed line and the record; key absent, empty, or no `CREDENTIALS_DIRECTORY` → exit 3, no
request, nothing written; the unit's user and group, its one credential line, `Type=oneshot`, no `[Install]`, its
`ExecStart`; the timer's calendar, `Persistent`, unit and `[Install]`; the manifest naming the timer once and the
service not at all.

## Validation

**Stage A.**

- **A0** (first command of the session):
  ```
  $ hostname; systemctl is-active crypto-bot.service crypto-exchange.service; test -d /srv/crypto-auto/.git && echo clone; id -u cryptorun
  vultr
  active
  active
  clone
  995
  ```
  Known answers. The session's own `hostname`: `vultr`.
- **A1.** Contract §4a steps 1–6 and the §5 gate (see `## Fingerprints`) passed: anchors 7 of 7, map table rows 7,
  TZ header table byte-identical to the map's; every file pair at the required value; `EXECUTOR-INSTRUCTIONS.md`
  `**Version 31.**`. `git rev-parse --is-shallow-repository` → `false`.
  1. `git rev-parse origin/main:vps` → `11bb152889801388df439537b66e2a52732150b4` (known answer).
  2. `grep -c '^crypto-etf' vps/manifest; ls vps/units | grep -c '^crypto-etf'` → `0`, `0` (known answers).
  3. `python3 vps/selftest.py` on `origin/main` (`4148a6a`, Python 3.12.3) → exit 0,
     `selftest: sections 24 checks 457 failed 0 empty 0` (known answer). Per section: A 32 · B 12 · C 4 · D 13 · E 12 ·
     F 14 · G 8 · H 2 · I 4 · J 26 · K 2 · L 4 · M 19 · N 10 · O 33 · P 21 · Q 3 · R 9 · S 35 · T 39 · U 18 · V 16 ·
     W 102 · X 19.
- **A2.** The trigger message carried the `SOSOVALUE_API_KEY=` line. The value was written to
  `/etc/crypto-auto/credentials/sosovalue-api-key` by the session's file-write tool (no shell command line carried it;
  the directory is `700 root root`, so the file was never readable by another user), then `chown root:root`,
  `chmod 600`. `stat -c '%a %U %G'` → `600 root root`; `wc -c <` → `37` (known answers: mode and owner, count > 0).
- **A3.** One `python3 -c` run as root reading the key from its file, three requests as §3 item 1 makes them:
  ```
  us-btc-spot status 200 code 0 rows 300 newest 2026-10-20 keys ['cumNetInflow', 'date', 'totalNetAssets', 'totalNetInflow', 'totalValueTraded'] first 2026-10-20
  us-eth-spot status 200 code 0 rows 300 newest 2026-10-20 keys ['cumNetInflow', 'date', 'totalNetAssets', 'totalNetInflow', 'totalValueTraded'] first 2026-10-20
  us-sol-spot status 200 code 0 rows 246 newest 2026-10-20 keys ['cumNetInflow', 'date', 'totalNetAssets', 'totalNetInflow', 'totalValueTraded'] first 2026-10-20
  ```
  Known answer on all three. (`first` is the date of `data[0]`: the provider serves newest-first today; the code does
  not rely on it.)
- **A4.** `stat -c '%a %U %G' /var/lib/crypto-auto` → `750 cryptoauto cryptoauto`;
  `grep -n 'installable()' vps/install.sh` → `170:installable() { grep -q '^\[Install\]' "$UNITS/$1"; }` (known
  answers).

**SoSoValue calls by this session: 6 of the 9 allowed** — A3's three and V4's three; the reserve was not used, and no
call was made in a loop.

**V1. Selftest** on the branch (`4d07801`): exit 0,
```
section A: checks 32 failed 0 … section X: checks 19 failed 0
section Y: checks 44 failed 0
selftest: sections 25 checks 501 failed 0 empty 0
```
Every section A–X at its A1.3 count (`501 = 457 + 44`). Negative controls, each applied alone, then reverted (the
pre-control files restored from a copy and compared with `cmp`) and V1 re-run green (`sections 25 checks 501 failed 0
empty 0`, exit 0) after each:

| # | Control, as applied | Exit | Failing checks (all in section Y; A–X `failed 0`) |
|---|---|---:|---|
| 1 | `newest()`: `if best is None or date > best["date"]:` → `if best is None:` — the first row of `data` that passes the date/finite filter is taken, whatever its date | 1 | `newest row from an oldest-first list: 2026-10-20, net 125.5` · `a later date whose net is absent, NaN or whose date is not YYYY-MM-DD is passed over` · `the line reads read=1 refused=2 written=yes newest=2026-10-20` · `the type's entry: date, net, traded, assets, cum, rows cast, an absent field null` |
| 2 | the printed line given ` key=%s` with the key | 1 | `none read: the line reads read=0 refused=3 written=no newest=-` · `the line reads read=1 refused=2 written=yes newest=2026-10-20` · `the printed line is exactly one line of the fixed shape` · `the key is absent from the printed line` |
| 3 | `atomic_write(..., mode=0o644)` | 1 | `the record's mode is 0640` |
| 4 | a second line `LoadCredential=binance-api-key:/etc/crypto-auto/credentials/binance-api-key` in `crypto-etf.service` | 1 | `service carries exactly one LoadCredential=, the SoSoValue key's` |

**V2. Syntax.** `python3 -m py_compile vps/etf.py vps/selftest.py` → silent, exit 0.

**V3. Units.** `systemd-analyze verify vps/units/crypto-etf.service vps/units/crypto-etf.timer` → silent, exit 0. Also
the installer's own form, `systemd-analyze verify vps/units/*` → silent, exit 0.
`systemd-analyze calendar '*-*-* *:07:00 UTC'` at `Wed Oct 21 20:23:26 UTC 2026` →
`Normalized form: *-*-* *:07:00 UTC`, `Next elapse: Wed 2026-10-21 21:07:00 UTC`, `From now: 43min left`.

**V4. The lane, measured on the VPS.** `vps/etf.py` and `vps/common.py` of the branch installed `0644` into
`/tmp/tz69-etf.MidaBQ` (`0755`), then:
```
$ systemd-run --wait --collect --pipe --uid=cryptoauto --gid=cryptoauto -p LoadCredential=sosovalue-api-key:/etc/crypto-auto/credentials/sosovalue-api-key /usr/bin/python3 /tmp/tz69-etf.MidaBQ/etf.py --out /var/lib/crypto-auto/etf-tz69.json
Running as unit: run-u4895.service
etf: read=3 refused=0 written=yes newest=2026-10-20
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 1.054s
...
systemd-run exit 0
$ stat -c '%a %U %G' /var/lib/crypto-auto/etf-tz69.json
640 cryptoauto cryptoauto
```
The record: keys `v, k, ts, provider, host, types, refused`; `v 1`, `k etf`, `provider SoSoValue`,
`host openapi.sosovalue.com`, **`ts 2026-10-21T20:23:48Z`**, `refused {}`.

| Type | `date` | `net` | `rows` |
|---|---|---:|---:|
| `us-btc-spot` | 2026-10-20 | 23162422.509999998 | 300 |
| `us-eth-spot` | 2026-10-20 | -26134272.7 | 300 |
| `us-sol-spot` | 2026-10-20 | -2649009.0 | 246 |

Known answer: exit 0, the line with A3's date, mode `640 cryptoauto cryptoauto`, A3's three dates. Then
`rm -f /var/lib/crypto-auto/etf-tz69.json; rm -rf /tmp/tz69-etf.MidaBQ` → both absent (`ls` → `No such file or
directory`). `systemctl list-units --all --no-legend 'run-*'` → 12 lines before V4 and 12 after, the same pre-existing
mounts (`run-credentials-*`, `run-docker-netns-*`, `run-user-0.mount`); `systemctl list-units --all --no-legend
'run-u[0-9]*'` → 0 lines; `systemctl status run-u4895.service` → `Unit run-u4895.service could not be found.` No unit of
this session is left (contract §7 item 15).

**V5. The value's absence.** Known answer: no match. Result: **no match** anywhere searched; command and output under `## Test Results`. `<scratch>` is the session's scratch directory, which held this report's draft, V4's captured output and every other output file the session wrote. The journal's two lines are systemd's own start and stop lines; `--pipe` carried the program's line to the session, where V4 quotes it.

**V6. Scope.** `git diff --name-only origin/main...HEAD` →
```
vps/etf.py
vps/manifest
vps/selftest.py
vps/units/crypto-etf.service
vps/units/crypto-etf.timer
```
exactly §4's five files; `5 files changed, 395 insertions(+), 3 deletions(-)`.

**V7. Nothing in effect before the merge.** `systemctl list-timers --all --no-legend crypto-etf.timer` → no output
(0 lines); `ls /etc/systemd/system | grep -c etf` → `0`.

## Test Results

**V5**, run after this file was complete, the pattern read from the key's own file by `grep -f` and never printed:
```
$ K=/etc/crypto-auto/credentials/sosovalue-api-key   # pattern file: 1 line, no empty line (1 line, 0 empty)
$ git log -p --format=fuller origin/main..origin/tz-69-etf-lane | grep -cF -f $K
0
$ git diff origin/main...origin/tz-69-etf-lane | grep -cF -f $K
0
$ grep -lF -f $K vps/etf.py vps/selftest.py vps/manifest vps/units/crypto-etf.service vps/units/crypto-etf.timer | wc -l
0
$ grep -rlF -f $K <scratch>/ | wc -l   # report, V4 output, A1.3/A3/V1/control outputs, PR body, anchor tables: 17 files
0
$ journalctl -u run-u4895.service --no-pager | grep -cF -f $K
0
$ gh pr view 57 --json title,body | grep -cF -f $K
0
$ ls /a13.txt ../v1.out /var/lib/crypto-auto/etf-tz69.json 2>&1 | grep -c 'No such'
3
$ grep -cF -f $K $K   # positive control: the search finds the value where it is
1
$ journalctl -u run-u4895.service --no-pager | wc -l   # the journal searched above is not empty
2
$ grep -cF -f $K CryptoReports/TZ-69-etf-lane-report.md   # this report, final text
0
```

**Hosted gate.** See `## CI Execution`.

## Deviations

None from the specification's requirements. Readings the TZ left to the Executor, stated so the audit can check them:

1. **Control 1 as applied** takes the first row of `data` that passes the date and finite-net filter, not literally
   `data[0]`. On the selftest's fixtures the two coincide except in the «passed over» fixture, which the literal form
   would also fail.
2. **The exit-3 line** is §3's one printed line with nothing read, nothing refused: `etf: read=0 refused=0 written=no
   newest=-`; no request was made, so no type is counted as refused.
3. **`data` present but not a list is `unparseable`**, the answer not parsing into the shape §3 accepts; `no row` is kept
   for a list holding no qualifying row. A final status other than 200 without an `HTTPError` is `HTTP <status>`.
   `code` is accepted as the integer `0` or the string `"0"` (A3 printed `0`; a bool is never a code).
4. **`ts`** is taken when the three reads are complete, before the write.
5. **The commit message** is the TZ's string verbatim followed by a blank line and a `Co-Authored-By:` trailer, as
   TZ-67's and TZ-68's commits carry one.

## Pre-existing Issues

None found. The §0 file table and the added-files table measured at their stated values.

## Remaining Risks

- **The run reads the record by group.** `/var/lib/crypto-auto` is `750 cryptoauto cryptoauto` and the record `640
  cryptoauto cryptoauto`; `crypto-run.service`'s user `cryptorun` is a member of `cryptoauto` (`vps/install.sh`
  provisions it so): `id cryptorun` → `uid=995(cryptorun) gid=987(cryptorun) groups=987(cryptorun),988(cryptoauto)`.
  Read access by `cryptorun` follows from the modes; no read was made as that user.
- **An hour with every type refused leaves `crypto-etf.service` in the `failed` state** (exit 4, or 3 without a key)
  until the next successful hour; `systemctl --failed` will show it meanwhile. The record standing carries its own `ts`.
- **`Persistent=true`** makes one catch-up read after the host was down over a :07 mark — at most one extra set of three
  calls, inside the 10 000-a-month and 10-a-minute limits read on 16.10.2026.
- **The provider's figures are carried as served:** `23162422.509999998` is the provider's own float for BTC's net flow
  on 2026-10-20, kept unrounded.
- **The value's other copy** is the conversation that carried the trigger, and the session's file-write call that put
  the value into its file is part of that same conversation (contract §7 item 6). No shell command line, environment
  variable, unit file, commit or log line carried it (V5).
- **Two stray scratch files.** Saving A1.3's selftest output, a shell mistake (an empty `$OLDPWD`) wrote it to `/a13.txt`;
  later V1's output went to `../v1.out` (inside `.claude/worktrees/`). Both held only `section … checks … failed …`
  lines, were moved into the session's scratch directory within the same minute, and are covered by V5.
- **The ETF read is not yet used by the run:** `ANALYST-INSTRUCTIONS.md` §16 step D moves onto this record at the
  audit (TZ §5).

## Commit

Implementation, on branch `tz-69-etf-lane`, pushed: **`4d078014012e5d6bcb3b8ea0f622e35648d14307`**
```
TZ-69: vps — the ETF lane: SoSoValue's daily net flows for the US BTC, ETH and SOL spot ETFs, read hourly by a unit that runs no model into /var/lib/crypto-auto/etf.json

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```
Contents: `vps/etf.py` (A), `vps/units/crypto-etf.service` (A), `vps/units/crypto-etf.timer` (A), `vps/manifest` (M),
`vps/selftest.py` (M).

Report, on `main`, contents `CryptoReports/TZ-69-etf-lane-report.md` only:
```
TZ-69: report — the ETF lane
```

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/57 — `tz-69-etf-lane` → `main`, title `TZ-69: vps — the ETF
lane`. Not merged by this session.

## CI Execution

**Bench gate** (`.github/workflows/bench.yml`), event `pull_request` on PR #57, head
`4d078014012e5d6bcb3b8ea0f622e35648d14307`: run **39670101249**, status `completed`, conclusion **`success`**
(`gh run view 39670101249`; job `bench` `pass`, 1m9s). The branch push itself starts no workflow: `bench.yml`'s `push`
filter takes `main` and `claude/**` only, and `main.yml`'s `paths` allow-list names `main.py` and its own file only.
No other workflow ran.

`vps/selftest.py` is not a step of the hosted gate; its control is the deployer, whose `vps/install.sh` runs it before
installing anything (`if ! python3 "$HERE/selftest.py"; then say "selftest red, nothing installed"`). V1 above is a
local run on the VPS, not a runner run.

## Final Repository State

Branch `tz-69-etf-lane` on `origin` at `4d078014012e5d6bcb3b8ea0f622e35648d14307`, one commit on `origin/main`
`4148a6afb26ab6e92e190442577d0a5418396378`, its `vps` tree `9e51983fa9e2b39a821a68e07d8f69fc410ff3c6`; working tree
clean. Pull request #57 open. **NOT IN EFFECT UNTIL MERGED** — `crypto-etf.timer` is neither installed nor enabled
(V7); the deployer installs and enables it from `main` once merged. The key's file stays at
`/etc/crypto-auto/credentials/sosovalue-api-key`, `600 root root`.

## Fingerprints

Measured on `origin/main` `4148a6a` after `git fetch --all --prune`.

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — **2788** lines, MD5 **`01818e7f4c9ee26ada455d153d7eee00`** (TZ: 2788,
`01818e7f…` — equal). Revision string: `**Revision 2026-10-21-b.**` (required: the same).

**Anchors** — the list cut from the map's anchor table by its structure (every `|` row between the separator line
following `| Anchor | Exact string that must be present |` and the table's end), **table rows: 7, compared: 7**; the
TZ header's table cut the same way: 7 rows, `diff` empty. Per anchor, `grep -F -m1 -o -- '<anchor>'
SYSTEM-MAP-CRYPTOCALCUL.md` returned:

| Anchor | Returned |
|---|---|
| revision | `**Revision 2026-10-21-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

**Map §0 file table** (`wc -l`, `md5sum`):

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**The TZ's added files** (on `origin/main`, before the change):

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | equal; version line `**Version 31.**` |
| `vps/selftest.py` | 1965 | `18f1a8a38dade5a2f73fd89353ca8f67` | equal |
| `vps/manifest` | 8 | `36b72e41d6f2e6f49f4f033126aa2a23` | equal |

After the change, on the branch: `vps/selftest.py` 2179 `a67871ef4f25a76ccce41aadcbe7cf13`; `vps/manifest` 9
`75a0f5a71f6111ecca0553620f1eea4c` (see `## Files Modified`).
