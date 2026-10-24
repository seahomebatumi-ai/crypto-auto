# Implementation Report — TZ-70

## Status

**COMPLETED.**

1. **The record** (V4): `etf: read=3 refused=0 written=yes newest=2026-10-22`; record mode `640 cryptoauto cryptoauto`. Net flows in USD, newest first:
   - `us-btc-spot`: 2026-10-22 `-635492639.395` · 2026-10-21 `528400237.14` · 2026-10-20 `23162422.509999998`
   - `us-eth-spot`: 2026-10-22 `-110503216.84` · 2026-10-21 `14955026.105` · 2026-10-20 `-26134272.7`
   - `us-sol-spot`: 2026-10-22 `-8514997.4` · 2026-10-21 `585297.18` · 2026-10-20 `-2649009.0`
2. **The read** (the methodology's command of TZ §2 on V4's record, path substituted, nothing else changed):
   ```
   etf 2026-10-24T11:54:39Z SoSoValue openapi.sosovalue.com {}
   us-btc-spot 2026-10-22 -635492639.395 300 [{"date": "2026-10-22", "net": -635492639.395}, {"date": "2026-10-21", "net": 528400237.14}, {"date": "2026-10-20", "net": 23162422.509999998}]
   us-eth-spot 2026-10-22 -110503216.84 300 [{"date": "2026-10-22", "net": -110503216.84}, {"date": "2026-10-21", "net": 14955026.105}, {"date": "2026-10-20", "net": -26134272.7}]
   us-sol-spot 2026-10-22 -8514997.4 248 [{"date": "2026-10-22", "net": -8514997.4}, {"date": "2026-10-21", "net": 585297.18}, {"date": "2026-10-20", "net": -2649009.0}]
   ```
3. **The checks** (V1): `selftest: sections 25 checks 511 failed 0 empty 0`; `n = 10`; section Y **54** = 44 + 10. Controls: (1) `days` oldest first → 8 new Y checks fail; (2) last occurrence kept on a repeated date → 2; (3) `ETF_DAYS = 2` → 4. Failing checks are named under `## Validation`. Sections A–X and Y's original 44 are green in every control.

The previous TZ's branch was merged: `tz-69-etf-lane` reached `main` as `eaf2c84` (PR #57).

## Inbound Filing

None. `CryptoTZ/TZ-70-etf-three-days.md` is on `origin/main` at its canonical filename, filed by the upload `ed8c954`.

## Scope Executed

**Class: branch TZ** (contract §8) — `## Scope` names two files under `vps/**`, outside `CryptoReports/**`.

- Stage A: A0 and A1.1–A1.4, all at their known answers.
- Stage B: the two files edited on branch `tz-70-etf-three-days` from `origin/main` (`ed8c954`); V1–V7 run; commit, push, pull request.

## Files Created

None.

## Files Modified

`vps/etf.py` (+18 lines), `vps/selftest.py`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

- `vps/etf.py`: `ETF_DAYS = 3` with the comment the TZ fixes; `recent(data, n)` — rows `newest()` could choose (string date of form `YYYY-MM-DD`, `totalNetInflow` finite by `finite()`), one per date with the first in `data`'s order kept, newest first, first `n`, each `{"date", "net"}`; `entry()` adds `out["days"] = recent(data, ETF_DAYS)` after the fields it wrote. Schema `v` stays 1.
- `vps/selftest.py`, section Y: ten new checks (list below). One existing check — «the type's entry: date, net, traded, assets, cum, rows cast, an absent field null» — compared the whole entry as an exact dict and could not stay as written once the entry carries `days`; it now compares the entry with `days` popped, against the same expected dict, unchanged. Its count is unchanged. See `## Deviations`.

## Validation

**Baseline (A1.3), on `origin/main`:** exit 0, `selftest: sections 25 checks 501 failed 0 empty 0`. Per section: A=32 B=12 C=4 D=13 E=12 F=14 G=8 H=2 I=4 J=26 K=2 L=4 M=19 N=10 O=33 P=21 Q=3 R=9 S=35 T=39 U=18 V=16 W=102 X=19 Y=44.

**A0:** `hostname` → `vultr`; `systemctl is-active crypto-bot.service crypto-exchange.service crypto-etf.timer` → `active` ×3; `test -d /srv/crypto-auto/.git` → `clone`; `id -u cryptorun` → `995`; `stat` of the key file → `600 root root`.

**A1.1:** `git rev-parse origin/main:vps` → `9e51983fa9e2b39a821a68e07d8f69fc410ff3c6` (as known). **A1.2:** `grep -c days vps/etf.py` → `0`. **A1.4:** live record, every type line ending `null`, first line `etf 2026-10-24T11:07:02Z SoSoValue openapi.sosovalue.com {}`.

**V1.** Branch: exit 0, `sections 25 checks 511 failed 0 empty 0`; per-section lines identical to the baseline for A–X, `section Y: checks 54 failed 0`. The ten new checks: ETF_DAYS is 3 · days from four rows newest-first · days from the same four oldest-first · days passes over a bad date, absent net and NaN net · two valid rows give two entries · one gives one · a date given twice carries the first net · its `days[0]` equals the entry's date and net · the written record's `days` (three sessions, newest first, nets) · the written record's `days[0]` equals the entry's date and net.

Negative controls, each applied alone to `vps/etf.py`, then reverted (`cmp` against the saved good copy: identical) and V1 green again:

1. `sorted(seen, reverse=True)` → `sorted(seen)` — `failed 8`, all in Y's new checks: days from four rows newest-first; days from the same four oldest-first; days passes over a bad date…; two valid rows give two entries; a date given twice carries the first net; a date given twice `days[0]`; written record's `days`; written record's `days[0]`.
2. `seen.setdefault(date, net)` → `seen[date] = net` — `failed 2`: a date given twice carries the first net; a date given twice `days[0]`.
3. `ETF_DAYS = 3` → `2` — `failed 4`: ETF_DAYS is 3; days from four rows newest-first; days from the same four oldest-first; written record's `days`.

**V2.** `python3 -m py_compile vps/etf.py vps/selftest.py` → exit 0.

**V3.** `git diff origin/main -- vps/etf.py` is three hunks and nothing else:
```
@@ -33,6 +33,8 @@ URL = ...
 ETF_TIMEOUT_S = 40
+# Derived: the owner's request of 24.10.2026 — the three newest US sessions.
+ETF_DAYS = 3
 OUT = common.STATE_DIR + "/etf.json"
@@ -72,6 +74,21 @@ def newest(data):
+def recent(data, n):
+    """The n newest sessions newest() could choose, one per date (the first in data's order
+    where a date repeats), newest first, each {"date", "net"}."""
+    seen = {}
+    for row in data:
+        if not isinstance(row, dict):
+            continue
+        date = row.get("date")
+        net = finite(row.get("totalNetInflow"))
+        if not isinstance(date, str) or not _DATE.fullmatch(date) or net is None:
+            continue
+        seen.setdefault(date, net)
+    return [{"date": d, "net": seen[d]} for d in sorted(seen, reverse=True)[:n]]
+
@@ -89,6 +106,7 @@ def entry(answer):
     out["rows"] = len(data)
+    out["days"] = recent(data, ETF_DAYS)
     return out
```
No line of `newest()`, `read_type()`, `main()` or `Refused` is touched.

**V4.** Branch `vps/etf.py` and `vps/common.py` copied to a `0755` scratch directory under `/var/tmp`, run once: `systemd-run --wait --collect --pipe --uid=cryptoauto --gid=cryptoauto -p LoadCredential=sosovalue-api-key:/etc/crypto-auto/credentials/sosovalue-api-key /usr/bin/python3 <scratch>/etf.py --out /var/lib/crypto-auto/etf-tz70.json` (unit `run-u5013.service`). Exit 0; printed `etf: read=3 refused=0 written=yes newest=2026-10-22`; record mode `640 cryptoauto cryptoauto`. A structural check of the record: per type `days` holds three entries, distinct dates, newest first, `days[0]` equal to `{"date", "net"}` of the entry, `v` 1. Rows per type 300, 300, 248. The methodology's command is quoted under `## Status`. SoSoValue was called three times (limit six). The record and the scratch directory were then removed; `systemctl list-units --all --no-legend 'run-*'` before and after the run is identical, and the only `run-u*` unit is `run-user-0.mount`.

**V5.** For each of the branch's diff, V1's output, V4's captured output and its read, the scratch record, the scratch copies of both programs and the two edited files: `grep -c -F -f <(tr -d '\n' < /etc/crypto-auto/credentials/sosovalue-api-key) <file>` → `0` for every file. The command reads the value from its file and prints counts only. The report itself, searched by the same command before it was committed, → `0`. No match anywhere.

**V6.** `git diff --name-only origin/main...HEAD` on the branch → `vps/etf.py`, `vps/selftest.py`.

**V7.** At the end of the session the live record still reads `etf 2026-10-24T13:07:01Z SoSoValue openapi.sosovalue.com {}` with every type line ending `null` — the timer wrote that record from `main`'s code; nothing was installed from the branch.

## Test Results

See `## Validation`. Hosted CI was not read by this session (contract §9).

## Deviations

1. One existing section-Y check was edited (see `## Implementation Summary`): its exact-dict comparison could not hold with the new key. The expected dict is untouched and the check still sits among the original 44, green in all three controls. The TZ did not name this edit; it is the minimum that keeps `days` out of an assertion that predates it.
2. The commit message carries a `Co-Authored-By` trailer after the TZ's string, as the session's attribution rule requires.

## Pre-existing Issues

None found.

## Remaining Risks

- `days` is the three newest sessions present in the answer, not three consecutive trading days: a missing session upstream shows as a gap in dates, and the reader sees the dates.
- Nothing is in effect until the deployer installs the merge; until then the run prints one session (methodology §16 step D).

## Commit

Implementation, on the branch: `TZ-70: vps — the ETF record keeps the three newest US sessions of each type as days, the owner's request of 24.10.2026`.

Report, on `main`: `TZ-70: report — the ETF record's three sessions`.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/58 — branch `tz-70-etf-three-days`, implementation commit `0c82bea122cf95b1b661bb9ef12ee2aa1e2814d9` (pushed before this report was written).

## CI Execution

None read by this session. `main.yml`'s trigger is the `paths` allow-list `main.py` and `.github/workflows/main.yml`, so `CryptoReports/**` starts no workflow.

## Final Repository State

Branch `tz-70-etf-three-days` at `0c82bea`, pushed, from `origin/main` `ed8c954`; its diff against `origin/main` is `vps/etf.py` and `vps/selftest.py`. **NOT IN EFFECT UNTIL MERGED.** No unit, timer or service of this session is left running; V4's scratch directory and record are removed.

## Fingerprints

Map `SYSTEM-MAP-CRYPTOCALCUL.md`: **2790 lines**, MD5 `d0b235fe0c94d3a14b7e543f9379e846`; revision `**Revision 2026-10-24-a.**`.

Anchors (table rows 7, compared 7; each match is `grep -F -o` over the map, and each string is also present in the TZ header):

| Anchor | Text returned |
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
| `EXECUTOR-INSTRUCTIONS.md` (`**Version 31.**`) | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` |
| `vps/etf.py` at `origin/main` | 146 | `3a1f4303273efdc82f49d80c3a119063` |
| `vps/selftest.py` at `origin/main` | 2179 | `a67871ef4f25a76ccce41aadcbe7cf13` |

All match the TZ's §0 values.
