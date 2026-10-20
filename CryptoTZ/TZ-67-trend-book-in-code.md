# TZ-67 — The book in code: the trend system the run will publish, replayable over the archive

**Canonical filename:** `CryptoTZ/TZ-67-trend-book-in-code.md`
**Report:** `CryptoReports/TZ-67-trend-book-in-code-report.md`
**Host:** any machine with the repository, `git` and Python 3.12 — no stage reads or changes the VPS, and no stage runs
the new program against a market host. The deployer runs the selftest before it installs the merge (contract §7 item 15).
**Class:** branch TZ (contract §8) — it creates one file and modifies two, all under `vps/**`.
**Branch:** `tz-67-trend-book-in-code` · **Model:** Sonnet
**Previous TZ:** TZ-66, COMPLETED; merged at `d9cd3c7` (pull request #54).
**Written against:** contract v30, map `2026-10-20-a`, methodology `2026-10-19-a`, and `main` at `efbb8eb` — its `vps`
tree `d013f2d9ac9209c9ac71dc7c6397696080b871aa` — read by the Architect from the repository on 20.10.2026, with the map
as delivered for upload beside this TZ. Map §10 row «The book is cut by a model and cannot be replayed» is what this TZ
executes, together with the helper pin that row «The hunter runs on a model alias» names.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-20-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-20-a.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | its version line reads `**Version 30.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `vps/run.py` | 360 | `07f672e5bcea06be27508db66aa3a8e0` | reported; a different file is a finding, never a block — B1's `git apply --check` is the block |
| `vps/selftest.py` | 1830 | `ce6220cdf2a45709bd1f09596e209ee9` | reported; as above |

The map itself: 2789 lines, MD5 `4e7388e346e79a4715af79a2fafa9e40` — reported, not enforced. The tree `origin/main:vps` is reported beside
them; `d013f2d9ac9209c9ac71dc7c6397696080b871aa` is the one this TZ was written against, and a different one is a finding,
never a block.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened, no unit is started, and `vps/book.py`
reads no market host in this session:** its live and archive paths run only inside the selftest, against stubs.

---

## 2. Contract and map text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> **Decided at `2026-10-20-a`, on the study of 20.10.2026: the trade leaves the model.**

— map §10, row «The book is cut by a model and cannot be replayed», which states the rule §11's patch builds. §11 builds
it and nothing beside it.

> a stage that needs an external FACT — a price, a date, a figure, an event — exists only as a workflow step, and an implementation TZ asking for such a fetch in-session is BLOCKED before it starts.

— contract §7 item 9. This TZ asks for none: the program's archive figures are the Architect's reading, recorded in that
row and re-run by the audit, and its live states are read by the analysis run, which exists to fetch them (same item).

> Code under `vps/` runs on the VPS only from `main`: the deployer fast-forwards its own clone and installs what changed, and nothing else installs anything.

— contract §7 item 15. The merge installs the program; nothing calls it until the methodology edit that follows this
TZ's audit (the row above).

> The first — the CLI's helper, which reads every fetched page for the hunter — is pinned by TZ-67

— map §10, row «The hunter runs on a model alias».

---

## 3. What is built

1. **`vps/book.py`, new** — the Donchian trend system over closed UTC daily bars, Python 3.12's standard library only:
   a daily close above the prior 55 days' highest high opens a long at the next open, below their lowest low a short; the
   stop sits 2 × ATR(20) from the entry and fills at the stop, or at the open when the day opened beyond it; a close
   beyond the prior 20 days' opposite extreme closes the trade at the next open. No target, no time limit. One function,
   `replay`, makes every trade; `levels` states what the next close decides — the two triggers and their stops when flat,
   the entry, stop, exit level and open R when in a trade; `result_r` prices a closed trade in R after 0.10 % a side and
   the funding prints after the entry and up to the exit. Two modes: `--live SYMBOL...`, one JSON object per symbol from
   `fapi.binance.com`'s daily klines, a symbol whose read fails printed `unread` beside the others; `--archive`, the
   table of every trade over `data.binance.vision`'s archive, in sample to 2024 and out of sample from 2025.
2. **The helper pin** — `run.HELPER_MODEL = "claude-haiku-4-5-20251001"`, joined to `run.PINS` as
   `ANTHROPIC_DEFAULT_HAIKU_MODEL`: the id TZ-66's A3 read in every run since 09.10.2026.
3. **`vps/selftest.py`** — section X, fourteen checks on two known-answer worlds and the live path's stubs; section O
   gains one check on the helper pin, and its stub session records the third pinned variable.

*[Architect's decision, TZ-67: the rule is the textbook Donchian 55/20 with a 2-ATR stop, its parameters fixed before the
study and never tuned; across the neighbourhood the study read — entry 20–100 days, exit 10–50, stop 2–3 ATR — every
variant was strongly positive in 2023–24 and near zero after, so no other point is better supported. Discarded: keeping the
2R / 168 h construction, worse on the list in both windows; a backtest bench under `bench/`, which would need the market
hosts inside the gate.]*

---

## 4. Scope

### Files to Create

```
vps/book.py
```

### Files to Modify

```
vps/run.py    vps/selftest.py
```

### Files to Delete

None.

### On the VPS

Nothing.

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **What the run publishes.** No caller of `vps/book.py` exists after the merge; the methodology edit after this TZ's audit
  moves the trader onto `--live` and decides how its states print, which coins carry a size, and what the hunter's events
  veto.
- **The archive's figures.** They are the Architect's reading of 20.10.2026 in the map's row, re-run by the audit on this
  branch; this session never runs `--archive` (contract §7 item 9).
- **Real money.** The gate of map §10 row «The engine places no order on the exchange» does not move.
- **The session, the hunter and the sheriff.** `run.PROMPT`, `run.APPEND`, `run.CLAUDE`, `run.MODEL`, `run.EFFORT` and
  `run.HUNTER_MODEL` do not move.

---

## 6. Rules — binding in every stage

1. **No VPS, no unit, no model session.** The session's network reads are `git`'s and `gh`'s, and nothing else:
   `vps/book.py` is never run with `--live` or `--archive` outside the selftest.
2. **§11's patch is extracted byte for byte, never retyped** — by the one command B1 gives.
3. **Python 3.12's standard library only.**

---

## 7. Stage A — readings, no writes

- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/main:vps`. **Known answer:** `d013f2d9ac9209c9ac71dc7c6397696080b871aa`. **Derived:** the
     Architect's session read it at `efbb8eb`, after TZ-66's merge at `d9cd3c7`. A different value is a finding, never a
     block — B1's `git apply --check` is the block.
  2. `git merge-base --is-ancestor d9cd3c7 origin/main; echo $?`. **Known answer:** `0`. **Derived:** the Architect's
     session read TZ-66's merge on `main`. `1`: BLOCKED — §11 is written against TZ-66's files.
  3. On `origin/main`'s tree, `python3 vps/selftest.py`. **Known answer:** exit 0 and
     `selftest: sections 23 checks 437 failed 0 empty 0`. **Derived:** TZ-66's V1 read exactly this on that code, and the
     Architect's session read the same line at `efbb8eb`.

---

## 8. Stage B — the code, on the branch

- **B1.** `git checkout -b tz-67-trend-book-in-code origin/main`, then:

  ```
  mkdir -p -m 0700 /tmp/tz67
  git show origin/main:CryptoTZ/TZ-67-trend-book-in-code.md \
      | awk '/^<!-- TZ-67 PATCH BEGIN -->$/{f=1;next} /^<!-- TZ-67 PATCH END -->$/{f=0} f' \
      | sed '1d;$d' > /tmp/tz67/tz67.patch
  md5sum /tmp/tz67/tz67.patch; wc -l < /tmp/tz67/tz67.patch
  git apply --check /tmp/tz67/tz67.patch && git apply /tmp/tz67/tz67.patch
  ```

  **Known answer:** the patch's MD5 is `b66517c27fb4cd4b745833be34b58477` (437 lines), and both `git apply` commands exit 0.
  **Derived:** the Architect's session extracted the patch from this file with exactly these commands and applied it
  to a clean checkout of `efbb8eb`. A different digest means the upload changed the file: BLOCKED, nothing applied.
- **B2.** `md5sum` and `wc -l` of the three files. **Known answer:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/book.py` | 282 | `f7ef81fceac48c69335a157e8c87f90f` |
  | `vps/run.py` | 364 | `988f6f4955072f6429def95d3957d974` |
  | `vps/selftest.py` | 1915 | `2f966893b69ccc5981f35e83a370d5a9` |

  **Derived:** the same application in the Architect's session. Any difference: BLOCKED.
- **B3.** `git add -A vps/ && git diff --cached --summary origin/main` prints exactly one line,
  `create mode 100644 vps/book.py`.
- **B4.** `rm -r /tmp/tz67` once the patch is applied.

---

## 9. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0, `selftest: sections 24 checks 452 failed 0 empty 0`,
  `section O: checks 33 failed 0` and `section X: checks 14 failed 0`. **Derived:** A1.3's 437 checks, plus section O's one
  and section X's fourteen, read by the Architect's session on §11's files under Python 3.11, 3.12 and 3.13.
  **Negative controls** (inv. 68), each applied alone, then reverted, B2's digests restored and V1 green again — in each,
  every other check of all twenty-four sections stays green:
  1. in `vps/book.py`, `                px = o if (side > 0 and o < stop) or (side < 0 and o > stop) else stop` →
     `                px = stop`: exit non-zero, `selftest: sections 24 checks 452 failed 1 empty 0`, and **exactly 1**
     check of section X fails — `a short stopped through a gap fills at the open`;
  2. in `vps/book.py`, `    for j in range(k - ATR_N + 1, k + 1):` → `    for j in range(k - ATR_N, k):`: `failed 4` —
     `the stop sits 2 ATR(20) below the entry: 105 - 2 x 2.2`, `its R after fees and slippage`,
     `funding counts the prints after the entry and up to the exit, paid by the long` and `its stop: 103 - 2 x 2.55`;
  3. in `vps/book.py`, ` for r in rows if int(r[6]) < now_ms]` → ` for r in rows]`: `failed 1` —
     `live bars drop the day still open`;
  4. in `vps/book.py`, `if tr["t_entry"] < t <= tr["t_exit"])` → `if tr["t_entry"] <= t <= tr["t_exit"])`: `failed 1` —
     `funding counts the prints after the entry and up to the exit, paid by the long`;
  5. in `vps/run.py`, `HELPER_MODEL = "claude-haiku-4-5-20251001"` → `HELPER_MODEL = "haiku"`: `failed 1` — section O's
     `run.PINS resolves haiku to claude-haiku-4-5-20251001`.

  **Derived:** the Architect's session ran all five on §11's files under Python 3.12 and 3.13 and read exactly these
  partitions.
- **V2. Syntax.** `python3 -m py_compile vps/book.py vps/run.py vps/selftest.py`.
- **V3. The pins, and a command line that does not move.** On the branch:

  ```
  python3 -c 'import sys; sys.path.insert(0, "vps"); import run; print(run.PINS); print(run.CLAUDE == ["claude", "-p", run.PROMPT, "--output-format", "json", "--model", "claude-opus-5-5", "--effort", "high", "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch", "--append-system-prompt", run.APPEND])'
  ```

  **Known answer:**
  `{'ANTHROPIC_DEFAULT_OPUS_MODEL': 'claude-opus-5-5', 'ANTHROPIC_DEFAULT_SONNET_MODEL': 'claude-sonnet-5', 'ANTHROPIC_DEFAULT_HAIKU_MODEL': 'claude-haiku-4-5-20251001'}`
  and `True`. **Derived:** the Architect's session ran it on §11's files.
- **V4. Scope.** `git diff --name-only origin/main...HEAD` lists exactly `vps/book.py`, `vps/run.py` and `vps/selftest.py`.
- **V5. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main` receives nothing from
  this session but its report.

No regression: sections A–W keep their counts but section O's, which gains one; section O's 32 earlier checks stay green.

---

## 10. The report

Contract §10's template. **The first three lines after `## Status`:**

1. **The code** — B1's patch digest and B2's three digests.
2. **The checks** — V1's total, sections O and X, and the five controls' partitions.
3. **The pins** — V3's two lines.

---

## Commit Message

Implementation, on the branch:

```
TZ-67: vps — the book in code: the Donchian trend system, one replay live and over the archive; the CLI's helper model pinned
```

Report, on `main`:

```
TZ-67: report — the book in code
```

---

## 11. The patch

Against `efbb8eb`. B1 extracts the lines between the two markers, drops the fence lines, and applies the rest.

<!-- TZ-67 PATCH BEGIN -->
```diff
diff --git a/vps/book.py b/vps/book.py
new file mode 100644
index 0000000..55a0b8b
--- /dev/null
+++ b/vps/book.py
@@ -0,0 +1,282 @@
+#!/usr/bin/env python3
+"""The engine's book in code (TZ-67): the Donchian trend system over closed UTC daily bars of Binance
+USD-M perpetuals. One function, replay(), decides every trade -- live and over the archive alike
+(map inv. 21, 38), so the archive's record is the record of exactly the rules the run publishes.
+
+    book.py --live SYMBOL...                    each symbol's state today, one JSON object per line,
+                                                from fapi.binance.com's daily klines (the run's role 2)
+    book.py --archive [--from D] [--to D] SYMBOL...
+                                                every trade the rules made over data.binance.vision's
+                                                archive, with fees, slippage and the actual funding,
+                                                and the table of in-sample and out-of-sample results
+
+The rules (Architect's decision, TZ-67, on the study of 20.10.2026):
+  a daily close above the prior ENTRY_N days' highest high opens a long at the next day's open, a close
+  below their lowest low a short; the stop sits STOP_ATR x ATR(ATR_N) from the entry; a daily close
+  beyond the prior EXIT_N days' opposite extreme closes the trade at the next day's open, and the stop
+  closes it intraday. No target and no time limit: the winners run.
+
+Python 3.12's standard library only. Time is UTC everywhere.
+"""
+import argparse
+import concurrent.futures
+import csv
+import io
+import json
+import os
+import sys
+import time
+import urllib.error
+import urllib.request
+import zipfile
+from datetime import date, datetime, timedelta, timezone
+
+ENTRY_N = 55          # a close beyond the prior 55 days' extreme opens a trend
+EXIT_N = 20           # a close beyond the prior 20 days' opposite extreme closes it
+ATR_N = 20            # the average true range's window, in days
+STOP_ATR = 2.0        # the initial stop, in ATRs from the entry
+COST_SIDE = 0.001     # taker fee 0.05 % + slippage 0.05 %, a fraction of notional per side
+OOS_START = date(2025, 1, 1)
+DAY_MS = 86_400_000
+HTTP_TIMEOUT_S = 20
+FAPI_KLINES = "https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1d&limit=400"
+ARCHIVE = "https://data.binance.vision/data/futures/um"
+
+
+def atr(bars, k):
+    """The mean true range of the ATR_N days ending at day k (inclusive), or None before day ATR_N."""
+    if k < ATR_N:
+        return None
+    total = 0.0
+    for j in range(k - ATR_N + 1, k + 1):
+        h, l, pc = bars[j][2], bars[j][3], bars[j - 1][4]
+        total += max(h - l, abs(h - pc), abs(l - pc))
+    return total / ATR_N
+
+
+def replay(bars):
+    """bars: closed daily bars (t_open_ms, open, high, low, close), oldest first, one per UTC day.
+    Returns (trades, position): each closed trade as a dict, and the open position after the last bar
+    or None. A signal at day k's close fills at day k+1's open; a stop fills at the stop, or at the open
+    when the day opened beyond it; a channel exit at day k's close fills at day k+1's open."""
+    trades, pos = [], None
+    for k in range(len(bars)):
+        t, o, h, l, c = bars[k]
+        if pos is not None and k >= pos["k_entry"]:
+            side, stop = pos["side"], pos["stop"]
+            if (side > 0 and l <= stop) or (side < 0 and h >= stop):
+                px = o if (side > 0 and o < stop) or (side < 0 and o > stop) else stop
+                trades.append(dict(pos, k_exit=k, t_exit=t, exit=px, why="stop"))
+                pos = None
+            elif k >= EXIT_N:
+                lo = min(b[3] for b in bars[k - EXIT_N:k]); hi = max(b[2] for b in bars[k - EXIT_N:k])
+                if (side > 0 and c < lo) or (side < 0 and c > hi):
+                    if k + 1 < len(bars):
+                        nxt = bars[k + 1]
+                        trades.append(dict(pos, k_exit=k + 1, t_exit=nxt[0], exit=nxt[1], why="channel"))
+                        pos = None
+                        continue          # the exit day's own close cannot also open a trade
+                    pos["exit_due"] = True
+        if pos is None and k >= ENTRY_N and k + 1 < len(bars):
+            a = atr(bars, k)
+            if a is None or a <= 0:
+                continue
+            hi = max(b[2] for b in bars[k - ENTRY_N:k]); lo = min(b[3] for b in bars[k - ENTRY_N:k])
+            side = 1 if c > hi else (-1 if c < lo else 0)
+            if side:
+                nxt = bars[k + 1]
+                entry = nxt[1]
+                pos = dict(side=side, k_signal=k, k_entry=k + 1, t_entry=nxt[0], entry=entry, atr=a,
+                           stop=entry - side * STOP_ATR * a)
+    return trades, pos
+
+
+def levels(bars, pos):
+    """What the next close decides, from the last closed bar: the trigger and the stop a new trade would
+    take, or the open position's exit level."""
+    k = len(bars) - 1
+    t, o, h, l, c = bars[k]
+    a = atr(bars, k)
+    out = dict(asof=datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%Y-%m-%d"), close=c,
+               atr20=a, state="flat")
+    if pos is not None:
+        side = pos["side"]
+        out.update(state="long" if side > 0 else "short",
+                   entry_date=datetime.fromtimestamp(pos["t_entry"] / 1000, timezone.utc).strftime("%Y-%m-%d"),
+                   entry=pos["entry"], stop=pos["stop"],
+                   exit_level=(min(b[3] for b in bars[k - EXIT_N + 1:k + 1]) if side > 0
+                               else max(b[2] for b in bars[k - EXIT_N + 1:k + 1])),
+                   r_open=side * (c - pos["entry"]) / abs(pos["entry"] - pos["stop"]),
+                   exit_due=bool(pos.get("exit_due")))
+    elif k >= ENTRY_N - 1 and a:
+        hi = max(b[2] for b in bars[k - ENTRY_N + 1:k + 1]); lo = min(b[3] for b in bars[k - ENTRY_N + 1:k + 1])
+        out.update(long_trigger=hi, short_trigger=lo, long_stop=hi - STOP_ATR * a, short_stop=lo + STOP_ATR * a)
+    return out
+
+
+def result_r(tr, funding):
+    """A closed trade in R after fees, slippage and funding. funding: sorted list of (t_ms, rate)."""
+    side, e, x = tr["side"], tr["entry"], tr["exit"]
+    dist = abs(e - tr["stop"]) / e
+    paid = side * sum(r for t, r in funding if tr["t_entry"] < t <= tr["t_exit"])
+    return (side * (x / e - 1) - paid - 2 * COST_SIDE) / dist
+
+
+def _get(url):
+    with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_S) as r:
+        return r.read()
+
+
+def live_bars(symbol, now_ms):
+    rows = json.loads(_get(FAPI_KLINES % symbol))
+    return [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) < now_ms]
+
+
+def _csv_rows(blob):
+    with zipfile.ZipFile(io.BytesIO(blob)) as z:
+        for name in z.namelist():
+            for r in csv.reader(io.TextIOWrapper(z.open(name), "utf-8")):
+                if r and r[0][:1].isdigit():
+                    yield r
+
+
+def _archive_blob(path, cache):
+    """One archive file, read once: kept in the cache, and a 404 kept as an empty marker beside it."""
+    local = os.path.join(cache, path.replace("/", "_"))
+    if os.path.exists(local + ".404"):
+        return None
+    if os.path.exists(local):
+        with open(local, "rb") as fh:
+            return fh.read()
+    try:
+        blob = _get(ARCHIVE + "/" + path)
+    except urllib.error.HTTPError as exc:
+        if exc.code == 404:
+            open(local + ".404", "w").close()
+            return None
+        raise
+    tmp = local + ".part"
+    with open(tmp, "wb") as fh:
+        fh.write(blob)
+    os.replace(tmp, local)
+    return blob
+
+
+def _ms(t):
+    t = int(t)
+    return t // 1000 if t > 10 ** 14 else t       # the archive moved to microseconds in 2025
+
+
+def archive_series(symbol, start, end, cache):
+    """Daily bars and funding prints of one symbol from the archive, start..end inclusive (UTC dates)."""
+    bars, funding = {}, {}
+    m = date(start.year, start.month, 1)
+    last_month = date(end.year, end.month, 1)
+    while m <= last_month:
+        tag = "%d-%02d" % (m.year, m.month)
+        blob = _archive_blob("monthly/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, tag), cache)
+        if blob is None and m == last_month:          # the current month has daily files only
+            d = m
+            while d <= end:
+                b = _archive_blob("daily/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, d.isoformat()), cache)
+                for r in _csv_rows(b) if b else ():
+                    bars[_ms(r[0])] = (_ms(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]))
+                d += timedelta(days=1)
+        for r in _csv_rows(blob) if blob else ():
+            bars[_ms(r[0])] = (_ms(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]))
+        fb = _archive_blob("monthly/fundingRate/%s/%s-fundingRate-%s.zip" % (symbol, symbol, tag), cache)
+        for r in _csv_rows(fb) if fb else ():
+            funding[_ms(r[0])] = float(r[2])
+        m = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
+    lo = datetime(start.year, start.month, start.day, tzinfo=timezone.utc).timestamp() * 1000
+    hi = datetime(end.year, end.month, end.day, tzinfo=timezone.utc).timestamp() * 1000
+    return ([bars[t] for t in sorted(bars) if lo <= t <= hi], sorted(funding.items()))
+
+
+def summary(rs):
+    """n, win share, mean R, total R, profit factor, max drawdown in R over the trades in exit order."""
+    if not rs:
+        return dict(n=0)
+    wins = sum(r for r in rs if r > 0); losses = -sum(r for r in rs if r < 0)
+    peak = run = dd = 0.0
+    for r in rs:
+        run += r; peak = max(peak, run); dd = max(dd, peak - run)
+    return dict(n=len(rs), win=sum(1 for r in rs if r > 0) / len(rs), mean=sum(rs) / len(rs), total=sum(rs),
+                pf=(wins / losses) if losses > 0 else float("inf"), maxdd=dd)
+
+
+def archive_paths(symbol, start, end):
+    """Every archive file archive_series may read for one symbol."""
+    paths = []
+    m = date(start.year, start.month, 1)
+    last_month = date(end.year, end.month, 1)
+    while m <= last_month:
+        tag = "%d-%02d" % (m.year, m.month)
+        paths.append("monthly/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, tag))
+        paths.append("monthly/fundingRate/%s/%s-fundingRate-%s.zip" % (symbol, symbol, tag))
+        m = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
+    d = last_month
+    while d <= end:
+        paths.append("daily/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, d.isoformat()))
+        d += timedelta(days=1)
+    return paths
+
+
+def archive(symbols, start, end, cache, workers=8):
+    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
+        list(ex.map(lambda path: _archive_blob(path, cache),
+                    [path for s in symbols for path in archive_paths(s, start, end)]))
+    rows = []
+    for s in symbols:
+        bars, funding = archive_series(s, start, end, cache)
+        trades, _ = replay(bars)
+        for tr in trades:
+            rows.append((tr["t_exit"], s, tr["side"], tr["t_entry"], result_r(tr, funding), tr["why"]))
+    rows.sort()
+    oos = datetime(OOS_START.year, OOS_START.month, OOS_START.day, tzinfo=timezone.utc).timestamp() * 1000
+    out = {}
+    for name, keep in (("in-sample", lambda r: r[3] < oos), ("out-of-sample", lambda r: r[3] >= oos),
+                       ("all", lambda r: True)):
+        part = [r for r in rows if keep(r)]
+        out[name] = dict(summary([r[4] for r in part]),
+                         long=summary([r[4] for r in part if r[2] > 0]), short=summary([r[4] for r in part if r[2] < 0]))
+    return rows, out
+
+
+def main(argv=None):
+    ap = argparse.ArgumentParser(description="the trend book: live states or the archive's record")
+    ap.add_argument("--live", action="store_true")
+    ap.add_argument("--archive", action="store_true")
+    ap.add_argument("--from", dest="start", default="2023-01-01")
+    ap.add_argument("--to", dest="end", default=None)
+    ap.add_argument("--cache", default=os.path.join(os.path.expanduser("~"), ".cache", "crypto-book"))
+    ap.add_argument("symbols", nargs="+")
+    a = ap.parse_args(argv)
+    if a.live == a.archive:
+        ap.error("exactly one of --live and --archive")
+    if a.live:
+        now_ms = int(time.time() * 1000)
+        for s in a.symbols:
+            try:
+                bars = live_bars(s, now_ms)
+                trades, pos = replay(bars)
+                out = dict(symbol=s, **levels(bars, pos)) if len(bars) > ENTRY_N else dict(symbol=s, state="short-history")
+            except Exception as exc:          # one symbol's failure never hides the others
+                out = dict(symbol=s, state="unread", error=exc.__class__.__name__)
+            print(json.dumps(out, sort_keys=True), flush=True)
+        return 0
+    os.makedirs(a.cache, exist_ok=True)
+    end = date.fromisoformat(a.end) if a.end else (datetime.now(timezone.utc).date() - timedelta(days=2))
+    rows, out = archive(a.symbols, date.fromisoformat(a.start), end, a.cache)
+    for name, s in out.items():
+        if not s["n"]:
+            print("%-14s no trades" % name); continue
+        print("%-14s trades %4d  win %.2f  mean R %+.3f  total R %+8.2f  PF %.2f  max DD %6.2f R  "
+              "long %d (%+.2f R)  short %d (%+.2f R)" % (name, s["n"], s["win"], s["mean"], s["total"], s["pf"],
+                                                         s["maxdd"], s["long"].get("n", 0), s["long"].get("total", 0.0),
+                                                         s["short"].get("n", 0), s["short"].get("total", 0.0)))
+    return 0
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/vps/run.py b/vps/run.py
index bd79c60..3e5bfb5 100644
--- a/vps/run.py
+++ b/vps/run.py
@@ -53,7 +53,11 @@ EFFORT = "high"
 # tool's per-call model outranks any agent definition (Claude Code docs, "Subagents", read 19.10.2026), and the
 # methodology names the hunter's as `sonnet`; the sheriff runs on MODEL, the session's own.
 HUNTER_MODEL = "claude-sonnet-5"
-PINS = {"ANTHROPIC_DEFAULT_OPUS_MODEL": MODEL, "ANTHROPIC_DEFAULT_SONNET_MODEL": HUNTER_MODEL}
+# TZ-67: the CLI's own helper model -- the one that reads every fetched page for the hunter -- named by
+# TZ-66's A3 in every run since 09.10.2026 and pinned to that id.
+HELPER_MODEL = "claude-haiku-4-5-20251001"
+PINS = {"ANTHROPIC_DEFAULT_OPUS_MODEL": MODEL, "ANTHROPIC_DEFAULT_SONNET_MODEL": HUNTER_MODEL,
+        "ANTHROPIC_DEFAULT_HAIKU_MODEL": HELPER_MODEL}
 CLAUDE = ["claude", "-p", PROMPT,
           "--output-format", "json", "--model", MODEL, "--effort", EFFORT,
           "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch",
diff --git a/vps/selftest.py b/vps/selftest.py
index 46a9505..6dea505 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -31,6 +31,7 @@ HERE = os.path.dirname(os.path.abspath(__file__))
 REPO = os.path.dirname(HERE)
 sys.path.insert(0, HERE)
 import announce  # noqa: E402
+import book  # noqa: E402
 import bot  # noqa: E402
 import cleanup  # noqa: E402
 import common  # noqa: E402
@@ -507,7 +508,8 @@ import json, os, sys
 with open(os.environ["SELFTEST_O_CLAUDE_SAW"], "w") as fh:
     fh.write(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "<absent>"))
 with open(os.environ["SELFTEST_O_CLAUDE_SAW"] + "-pins", "w") as fh:
-    json.dump({k: os.environ.get(k) for k in ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL")}, fh)
+    json.dump({k: os.environ.get(k) for k in ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL",
+                                          "ANTHROPIC_DEFAULT_HAIKU_MODEL")}, fh)
 json.dump({"type": "result", "subtype": "stub_subtype", "is_error": False, "result": os.environ["SELFTEST_O_RESULT"],
            "num_turns": 3, "duration_ms": 1234, "api_error_status": 418, "terminal_reason": "stub_terminal",
            "stop_reason": "stub_stop", "modelUsage": json.loads(os.environ.get("SELFTEST_O_MODELS", "{}")),
@@ -564,6 +566,8 @@ def section_o(s):
     s.check("run.PINS resolves sonnet to claude-sonnet-5",
             run.PINS.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-sonnet-5")
     s.check("run.PINS resolves opus to run.MODEL", run.PINS.get("ANTHROPIC_DEFAULT_OPUS_MODEL") == run.MODEL)
+    s.check("run.PINS resolves haiku to claude-haiku-4-5-20251001",
+            run.PINS.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") == "claude-haiku-4-5-20251001")
     tmp = tempfile.mkdtemp(prefix="vps-selftest-o.")
     env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", run.LOGIN_ENV,
                 "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW", "SELFTEST_O_RESULT",
@@ -591,6 +595,7 @@ def section_o(s):
                            # TZ-66: a value already in the unit's environment is not the pin.
                            "ANTHROPIC_DEFAULT_OPUS_MODEL": "selftest-decoy-opus",
                            "ANTHROPIC_DEFAULT_SONNET_MODEL": "selftest-decoy-sonnet",
+                           "ANTHROPIC_DEFAULT_HAIKU_MODEL": "selftest-decoy-haiku",
                            "SELFTEST_O_MODELS": json.dumps({"claude-opus-5-5": {}, "claude-sonnet-5": {},
                                                             "claude-haiku-selftest": {}})})
         common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
@@ -1802,11 +1807,91 @@ def section_w_memory(s):
         shutil.rmtree(tmp, ignore_errors=True)
 
 
+# --- X: the trend book (TZ-67): one replay decides live and over the archive -----------------
+def x_world_long():
+    """60 flat days, a close above the prior 55-day high, a steady trend, a close below the prior 20-day low."""
+    bars = [(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(60)]
+    bars.append((60 * book.DAY_MS, 100.0, 106.0, 100.0, 105.0))
+    bars.append((61 * book.DAY_MS, 105.0, 107.0, 104.0, 106.0))
+    for k in range(62, 100):
+        c = 106.0 + (k - 61)
+        bars.append((k * book.DAY_MS, c - 1, c + 1, c - 2, c))
+    bars.append((100 * book.DAY_MS, 144.0, 144.5, 120.0, 121.0))
+    for k in range(101, 105):
+        bars.append((k * book.DAY_MS, 122.0, 123.0, 121.0, 122.0))
+    return bars
+
+
+def x_world_short():
+    """60 flat days, a close below the prior 55-day low, a gap through the stop, then a breakout long."""
+    bars = [(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(60)]
+    bars.append((60 * book.DAY_MS, 100.0, 100.0, 94.0, 95.0))
+    bars.append((61 * book.DAY_MS, 95.0, 96.0, 94.0, 95.0))
+    bars.append((62 * book.DAY_MS, 103.0, 104.0, 102.0, 103.0))
+    bars.append((63 * book.DAY_MS, 103.0, 104.0, 102.0, 103.0))
+    bars.append((64 * book.DAY_MS, 103.0, 104.0, 102.0, 103.0))
+    return bars
+
+
+def section_x(s):
+    eps = 1e-9
+    trades, pos = book.replay(x_world_long())
+    s.check("the long world makes exactly one trade", len(trades) == 1)
+    tr = trades[0] if trades else {}
+    s.check("a close above the prior 55-day high opens a long at the next open",
+            tr.get("side") == 1 and tr.get("k_entry") == 61 and abs(tr.get("entry", 0) - 105.0) < eps)
+    s.check("the stop sits 2 ATR(20) below the entry: 105 - 2 x 2.2", abs(tr.get("stop", 0) - 100.6) < eps)
+    s.check("a close below the prior 20-day low closes it at the next open",
+            tr.get("why") == "channel" and tr.get("k_exit") == 101 and abs(tr.get("exit", 0) - 122.0) < eps)
+    s.check("the book ends flat", pos is None)
+    want = (122.0 / 105.0 - 1 - 2 * book.COST_SIDE) / (4.4 / 105.0)
+    s.check("its R after fees and slippage", bool(trades) and abs(book.result_r(tr, []) - want) < eps)
+    t0, t1 = tr.get("t_entry", 0), tr.get("t_exit", 0)
+    funding = [(t0, 0.5), (t0 + 1, 0.0001), (t1, 0.0002), (t1 + 1, 0.9)]
+    want_f = (122.0 / 105.0 - 1 - 0.0003 - 2 * book.COST_SIDE) / (4.4 / 105.0)
+    s.check("funding counts the prints after the entry and up to the exit, paid by the long",
+            bool(trades) and abs(book.result_r(tr, funding) - want_f) < eps)
+    lv = book.levels(x_world_long(), pos)
+    s.check("flat: the next close's triggers are the last 55 days' extremes",
+            lv["state"] == "flat" and lv.get("long_trigger") == 145.0 and lv.get("short_trigger") == 99.0)
+    trades, pos = book.replay(x_world_short())
+    tr = trades[0] if trades else {}
+    s.check("a short stopped through a gap fills at the open",
+            len(trades) == 1 and tr.get("side") == -1 and tr.get("why") == "stop" and abs(tr.get("exit", 0) - 103.0) < eps)
+    s.check("the stop day's close opens the next trade",
+            pos is not None and pos["side"] == 1 and pos["k_entry"] == 63 and abs(pos["entry"] - 103.0) < eps)
+    s.check("its stop: 103 - 2 x 2.55", pos is not None and abs(pos["stop"] - 97.9) < eps)
+    lv = book.levels(x_world_short(), pos)
+    s.check("in a trade: the state, the entry day, and the exit level of the last 20 days",
+            lv["state"] == "long" and lv.get("entry_date") == "1970-03-05" and lv.get("exit_level") == 94.0
+            and abs(lv.get("r_open", 1)) < eps)
+    saved = book._get
+    try:
+        rows = [[k * book.DAY_MS, "1", "2", "0.5", "1.5", "0", (k + 1) * book.DAY_MS - 1] for k in range(3)]
+        book._get = lambda url: json.dumps(rows).encode()
+        s.check("live bars drop the day still open", len(book.live_bars("XUSDT", 2 * book.DAY_MS + 5)) == 2)
+        world = x_world_long()
+        def fake(url):
+            if "BADUSDT" in url:
+                raise OSError("refused")
+            return json.dumps([[b[0], str(b[1]), str(b[2]), str(b[3]), str(b[4]), "0", b[0] + book.DAY_MS - 1]
+                               for b in world]).encode()
+        book._get = fake
+        with contextlib.redirect_stdout(io.StringIO()) as out:
+            code = book.main(["--live", "GOODUSDT", "BADUSDT"])
+        lines = [json.loads(l) for l in out.getvalue().splitlines()]
+        s.check("--live prints one object per symbol and survives one symbol's failure",
+                code == 0 and [l["symbol"] for l in lines] == ["GOODUSDT", "BADUSDT"]
+                and lines[0]["state"] == "flat" and lines[1]["state"] == "unread")
+    finally:
+        book._get = saved
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
             ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
-            ("T", section_t), ("U", section_u), ("V", section_v), ("W", section_w))
+            ("T", section_t), ("U", section_u), ("V", section_v), ("W", section_w), ("X", section_x))
 
 
 def main():
```
<!-- TZ-67 PATCH END -->
