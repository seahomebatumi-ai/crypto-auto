# TZ-76 — The paper test's booking waits seven days, not three, before it calls an unpublished Binance file absent

**Canonical filename:** `CryptoTZ/TZ-76-paper-absence-margin.md`
**Report:** `CryptoReports/TZ-76-paper-absence-margin-report.md`
**Class:** branch TZ (contract §8) — it authorises one repository file besides its report.
**Branch:** `claude/tz-76-paper-absence-margin`
**Host:** the VPS, so that A2 and V3 compare counts on one machine, as TZ-75's did.
**Model:** Sonnet — one constant, its change given as §7's patch and executed by the Architect.
**Trigger:** `EXECUTE TZ-76`, with nothing under it: no credential arrives and the Boss is asked for nothing.
**Previous TZ:** TZ-75, PARTIAL on V5 alone, **accepted by the Architect on 29.10.2026**; its pull request #61 is merged
before this TZ starts, and A1 proves it by the bytes of `vps/paper.py`.
**Issued:** 29.10.2026, by the Architect. **Deadline:** in effect before **01.11.2026 00:00 UTC** (§1).
**Written against:** contract v31, map `2026-10-26-a`, and `main` with pull request #61 merged — TZ-75's branch at
`4d914c4`, read from the repository on 29.10.2026.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-26-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-26-a.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | version line `**Version 31.**`; a lower version is BLOCKED |
| `vps/paper.py` | 1413 | `a709359a86f630c464fd92ee93f6ae2c` | equal — TZ-75's merged bytes. **`057440a4b5c9c277cc99062f768464ac` means pull request #61 is not merged: BLOCKED, and the closing message says «слить pull request #61, затем снова `EXECUTE TZ-76`»** |
| `vps/selftest.py` | 2627 | `76e814ccbe18551a8f47d6f7eae09669` | equal — TZ-75's merged bytes |

The map itself: 2796 lines, MD5 `e911fceb5f07444fe306f116a550b9cf` — reported, not enforced. **This TZ moves no map
revision:** the Architect writes TZ-75's and TZ-76's changes into the map in one revision at this TZ's audit.

---

## 1. Why — measured

TZ-64 12.3.1 registered, verbatim: «Read 16.10.2026 from the bucket listing: a day's klines are published about 08:00
UTC the next day, a month's funding about 08:00 UTC on the 1st — so a 404 for a file dated more than 3 days back is an
absence, nearer is a wait.» `paper.Inputs.fetch` implements it as `ABSENT_AFTER_DAYS = 3`.

**The premise failed on 28.10.2026.** At 19:54 UTC on 29.10 — about 36 hours after the day ended — every daily
kline file of 28.10 the Architect's session asked `data.binance.vision` for answered **404**: `BTCUSDT`, `INITUSDT` and
`1000PEPEUSDT`, 1 m and 1 d; the same files of 27.10 answered 200, and 29.10 answered 404. TZ-75's session read the same
at 19:46 UTC for `BTCUSDT`, `ETHUSDT` and `SOLUSDT` (its report, V5 and Pre-existing Issues).

**What the 3-day rule does with that lag.** Books are written in date order, and `book/2026-10-26.jsonl` is the last on
`main`: 27.10's book reads 28.10's minutes for every episode closing after 22:00 UTC, and 28.10's for all of its own. If
28.10 is still unpublished on 01.11.2026, the first booking pass of that day finds the gap at 4 days, `Absent`, and
writes **every episode of 28.10 unbookable — permanently**, because a record is never reopened (inv. 38 (2)). Among them
are **both pick episodes the test has** — pick 1's INIT and kPEPE longs, both closed on 28.10 — of the 30 its verdict
needs (TZ-64 12.4.2). The lag would destroy exactly the data TZ-75 exists to multiply.

**The amendment:** a 404 for a file dated more than **7** days back is an absence; nearer is a wait. *[Architect's
decision. Seven is the largest margin the standing selftest admits unchanged: W15's waiting check reads a gap of 1 day
and its absence check a gap of 10, so any value from 1 to 9 keeps both, and §6 V4 proves 10 breaks the second.
Discarded: 14, which edits a check for no measured gain. The cost of the longer wait arises only in a genuine absence:
the books after that day wait up to seven days, and the verdict already waits for the window's last month of funding,
published on the 1st of the month after it.]*

Nothing else moves: what a 404 means, the funding rule's months, every other constant and every record.

---

## 2. Text this TZ obeys

- Contract §7 item 2: «**Never edit a bench to make it pass.**» — no check of `vps/selftest.py` changes (§1).
- Contract §7 item 15: «An implementation session never enables, starts or leaves running a persistent unit, timer or
  service from a branch» — this TZ starts no unit at all.
- Map inv. 70: «**A transport failure is NOT an absence of data.**» — the same reasoning, one step further: a file the
  publisher is late with is not an absent file, and calling it absent destroys what a wait would have kept.
- Map inv. 38 (2): a file once written is never reopened — the reason an early verdict of absence is irreversible.

---

## 3. Scope

### Files to Create
None in the repository but the report.

### Files to Modify
- `vps/paper.py` — one line, §7.

### Files to Delete
None.

### On the VPS
Nothing: no unit is started, and the running `crypto-paper.service` is not touched. The change takes effect when the
deployer installs the merge.

---

## 4. Stages

### Stage A — readings, no writes
- **A0.** Contract §4a steps 1–6; the gate of §0, every anchor cut from the map's own table.
- **A1.** The three added files at their lines and MD5. `vps/paper.py` at `057440a4…` is pull request #61 unmerged:
  BLOCKED as §0 says.
- **A2.** Baseline on `main`, on the VPS: `python3 vps/selftest.py` — `selftest: sections 27 checks 592 failed 0
  empty 0`, `section W: checks 134 failed 0` (*TZ-75's V3, the same bytes*); recorded per section.

### Stage B — the change, on the branch
- **B1.** Branch `claude/tz-76-paper-absence-margin` from `origin/main`. Extract §7's patch with the one command

  ```sh
  awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-76-paper-absence-margin.md > /tmp/tz76.patch
  ```

  — 13 lines, MD5 `4eabfe2a3c439e64462e03b7a0022d72` as written — and `git apply /tmp/tz76.patch`.
- **B2. Required:** `vps/paper.py` 1413 lines, MD5 `dd4bab0209f99e1da430c87042a92b9c`. Any other result is BLOCKED, and
  no hand edit replaces the patch.
- **B3.** Commit with §5's implementation message, **locally, before stage C**, so that V4's restore returns the
  changed file. Not pushed yet.

### Stage C — validation, on the VPS, on the committed branch
§6, in full.

### Stage D — push, pull request, report
Push; a pull request to `main` titled `TZ-76: paper booking — absence after seven days, not three`, its body naming this
TZ and the deadline of §1, or the §8 fallback. Then the report.

---

## 5. Commit Message

Implementation: `TZ-76: vps — the paper test's booking waits seven days, not three, before calling an unpublished Binance file absent`

Report: `TZ-76: report — the booking's absence margin`

---

## 6. Validation

| # | Check | Required |
|---|---|---|
| V1 | `python3 -m py_compile vps/paper.py` | exit 0 |
| V2 | B2's file | 1413 lines, `dd4bab0209f99e1da430c87042a92b9c` |
| V3 | `python3 vps/selftest.py` on the branch | exit 0; every section's count equal to A2's — `selftest: sections 27 checks 592 failed 0 empty 0` on TZ-75's bytes. *Measured by the Architect on the changed tree, 29.10.2026* |
| V4 | Negative control: in the working tree set `ABSENT_AFTER_DAYS = 10`; run the selftest; restore with `git checkout -- vps/paper.py` | exit 1 with exactly one `FAIL` line, `FAIL section W raised NotReady: /daily/klines/KAITOUSDT/1m/KAITOUSDT-1m-2026-01-20.zip`, and `selftest: sections 27 checks 571 failed 1 empty 0` — W15's absence check, at a gap of 10, now waits and ends the section. Then `git status --porcelain` prints nothing and `vps/paper.py` is back at `dd4bab02…`. *Measured by the Architect, 29.10.2026* |
| V5 | `git diff --numstat origin/main...HEAD` | exactly one line: one added, one removed, `vps/paper.py` |
| V6 | `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service` before and after the session | equal |
| V7 | `bench.yml` on the branch | its runs, read from the runner where the session can; no step of it executes `vps/**` code |

---

## 7. The patch

Against `vps/paper.py` at `a709359a86f630c464fd92ee93f6ae2c`:

```diff
diff --git a/vps/paper.py b/vps/paper.py
index 2a98e2e..d3d6016 100644
--- a/vps/paper.py
+++ b/vps/paper.py
@@ -78,7 +78,7 @@ FILL_KEYS = ("coin", "px", "sz", "side", "time", "startPosition", "tid")   # all
 PICK_POLL_S = 30
 NULL_POLL_S = 600
 DAY_SETTLE_S = 600            # a day is written once every account was polled this long after it ended
-ABSENT_AFTER_DAYS = 3         # a 404 for a file dated further back is an absence, nearer is unpublished
+ABSENT_AFTER_DAYS = 7         # a 404 for a file dated further back is an absence, nearer is unpublished (TZ-76)
 WORK_EVERY_S = 3600           # booking, funding and the verdict are attempted hourly; a failed rescan resumes as often
 RESCAN_WEIGHT_PER_MIN = 300   # a rescan's share of WEIGHT_PER_MIN; the service holds the rest while one runs
 PUBLISH_EVERY_S = 300
```
