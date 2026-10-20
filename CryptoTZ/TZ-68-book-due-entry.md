# TZ-68 — The book's morning: a signal at the last close is an entry due at the forming day's open, and a day missing from the archive is refused — on TZ-67's branch

**Canonical filename:** `CryptoTZ/TZ-68-book-due-entry.md`
**Report:** `CryptoReports/TZ-68-book-due-entry-report.md`
**Host:** any machine with the repository, `git` and Python 3.12 — no stage reads or changes the VPS, and no stage runs
the program against a market host. The deployer runs the selftest before it installs the merge (contract §7 item 15).
**Class:** branch TZ (contract §8) — it modifies two files under `vps/**`, on top of TZ-67's branch.
**Branch:** `tz-68-book-due-entry`, from `tz-67-trend-book-in-code` at `c336d4d` · **Model:** Sonnet
**Previous TZ:** TZ-67, executed 20.10.2026; its audit of 20.10.2026 did not accept it, for the defect §3 names, and
pull request #55 is not merged. **This TZ builds on that branch on purpose** (contract §8): its pull request carries
TZ-67's commit and its own, and supersedes #55.
**Written against:** contract v30, map `2026-10-20-a`, methodology `2026-10-19-a`, `main` at `a0ac292` — its `vps` tree
`d013f2d9ac9209c9ac71dc7c6397696080b871aa` — and `tz-67-trend-book-in-code` at `c336d4d`, its `vps` tree
`94646e2873d37705aa2497fe0534a4d9765f5130`, read by the Architect from the repository on 20.10.2026. The map is not
revised for this TZ: its row «The book is cut by a model and cannot be replayed» states the rule this TZ keeps, and the
row moves with the methodology edit that follows this TZ's audit.

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
| `vps/book.py` at `origin/tz-67-trend-book-in-code` | 282 | `f7ef81fceac48c69335a157e8c87f90f` | equal, or BLOCKED — §11's patch applies to exactly these bytes |
| `vps/selftest.py` at `origin/tz-67-trend-book-in-code` | 1915 | `2f966893b69ccc5981f35e83a370d5a9` | equal, or BLOCKED — as above |

The map itself: 2789 lines, MD5 `4e7388e346e79a4715af79a2fafa9e40` — reported, not enforced. The two `vps` files are
measured on the branch, `git show origin/tz-67-trend-book-in-code:<file>`; `main` holds no `vps/book.py`.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened, no unit is started, and `vps/book.py`
reads no market host in this session:** its live and archive paths run only inside the selftest, against stubs.

---

## 2. Contract, map and TZ text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section named.

> `vps/book.py` replays it with one function live (`--live`, `fapi.binance.com`'s daily klines) and over the archive (`--archive`, `data.binance.vision`, fees, slippage and funding)

— map §10, row «The book is cut by a model and cannot be replayed». One function is the point: the archive's record is
the record of the book the run publishes only if the two never differ, and §3 names the morning on which they do.

> a daily close above the prior 55 days' highest high opens a long at the next open

— TZ-67 §3 item 1, the rule. This TZ moves no part of it: entry 55 days, exit 20, stop 2 ATR(20), costs and the
in-sample split stay.

> A second implementation of any rule, threshold or formula is banned in any language and any file.

— map inv. 38. The due entry's fill and stop are computed by `replay()` with the expression every archive fill uses,
never left for the trader to derive from the program's other fields.

> Before starting, check whether the previous TZ's branch was merged. If it was not, say so at the top of your report — building on an unmerged base produces work that is complete and live nowhere.

— contract §8. TZ-67's branch is unmerged by the audit's decision; the report says so first, and this TZ's pull request
carries both commits.

> a stage that needs an external FACT — a price, a date, a figure, an event — exists only as a workflow step, and an implementation TZ asking for such a fetch in-session is BLOCKED before it starts.

— contract §7 item 9. This TZ asks for none: the archive figures in §3 are the audit's reading, and the live path is read
by the analysis run, which exists to fetch it.

---

## 3. What is built, and why

**The defect — the Architect's, in TZ-67 §11.** `replay()` opens a position only when the bar after the signal is
already closed (`k + 1 < len(bars)`), and `levels()` takes the flat state's triggers over the last 55 days including the
last closed bar. So on the morning after a breakout close — the one day the rule enters, at that day's open — `--live`
prints `flat`, with triggers above the breakout bar itself, and the position first appears the next morning, dated to an
open that has passed. **Measured by the audit on 20.10.2026** on the archive of the 31 symbols of the payload's `c`,
2023-01-01 → 2026-10-18, at TZ-67's costs: entering one day late, as that output leads to, makes **+84.95 R against the
record's +197.82 R** — in sample +123.00 against +222.79, out of sample −38.05 against −24.97 — and 26 of the 511 trades
are over before the output shows them. The live book and the record would be two systems.

**The repair.**

1. `replay(bars, open_now=None)` — a signal at the last bar's close fills at `open_now`, the open of the day still
   forming, with its stop `STOP_ATR` × ATR(20) from that fill, in the same statement as every other fill, and the
   position carries `entry_due: true`. Without `open_now`, as in `--archive`, that signal opens nothing: no archive trade
   moves.
2. `live_bars()` returns the closed bars and the forming day's open, read from the same response; a read holding no
   forming day is refused, so the symbol prints `unread`, never a state that cannot fill.
3. `levels()` prints `entry_due` beside `exit_due`, and `r_open: null` for a due entry, whose fill comes after the last
   close.
4. `archive_series()` refuses a day missing between two bars — an exchange gap, or a month the cache remembers as a 404
   from before it was published — naming the symbol and the two dates around the gap: `replay()` reads one bar per UTC
   day, and a silent gap shifts every channel after it.
5. `vps/selftest.py` section X: two checks of the live path re-written for `live_bars()`'s pair, and five added — the due
   entry in each world is the position the next close records, its state, `--live`'s due line, and the refused gap.

**Measured on §11's files by the audit (20.10.2026):** `--archive` prints the same table, character for character, on the
31 list symbols and on the 27 outside ones (+197.82 R and +6.58 R); on every one of the 1 063 positions those 58 symbols
opened, the morning state — the bars to the signal close and the forming day's open — names the record's side, entry
day, entry and stop exactly; on all 16 549 mornings of the last 300 days, the 399 closed days `--live` reads give the
state the full history gives; and no day is missing from any of the 58 series.

*[Architect's decision, TZ-68: a due entry fills at the forming day's open, the price the record books, read by the
program from the response that carries the bars. Discarded: printing the stop as a distance for the trader to subtract —
a second implementation of the stop (inv. 38); replaying the forming day as a bar, whose high, low and close are not a
day's; never caching a 404 instead of refusing a gap — every rerun would read the network for every month before a
listing, and a gap from any other source would stay silent.]*

---

## 4. Scope

### Files to Create

None.

### Files to Modify

```
vps/book.py    vps/selftest.py
```

### Files to Delete

None.

### On the VPS

Nothing.

### On `main`

The report, and nothing else from this session.

### Pull request #55

This session neither closes nor comments on it; this TZ's pull request names it superseded.

---

## 5. What this TZ does not decide and does not build

- **What the run publishes.** No caller of `vps/book.py` exists after the merge; the methodology edit after this TZ's audit
  moves the trader onto `--live` and decides how a due entry prints and what the trader does when the market has left its
  fill.
- **The rule.** Entry, exit, stop, costs and the in-sample split do not move, and neither does `vps/run.py`.
- **The archive's figures.** They are the audit's reading of 20.10.2026; this session never runs `--archive` or `--live`
  against a market host (contract §7 item 9).
- **Real money.** The gate of map §10 row «The engine places no order on the exchange» does not move.

---

## 6. Rules — binding in every stage

1. **No VPS, no unit, no model session.** The session's network reads are `git`'s and `gh`'s, and nothing else.
2. **§11's patch is extracted byte for byte, never retyped** — by the one command B1 gives.
3. **Python 3.12's standard library only.**

---

## 7. Stage A — readings, no writes

- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/tz-67-trend-book-in-code`. **Known answer:** `c336d4d849a54321afee14bc81762a3ffae39165`.
     **Derived:** the audit read it on 20.10.2026. **Any other: BLOCKED** — the branch moved after the audit.
  2. `git merge-base --is-ancestor c336d4d origin/main; echo $?`. **Known answer:** `1`. **Derived:** the audit did not
     accept TZ-67, and #55 was open at `a0ac292`. `0` — TZ-67 merged — is a finding, stated first in the report, and the
     work goes on: §11's patch applies to the same bytes either way.
  3. `git checkout --detach origin/tz-67-trend-book-in-code && python3 vps/selftest.py`. **Known answer:** exit 0 and
     `selftest: sections 24 checks 452 failed 0 empty 0`. **Derived:** TZ-67's V1, and the audit's run of that tree under
     Python 3.11, 3.12 and 3.13.

---

## 8. Stage B — the code, on the branch

- **B1.** `git checkout -b tz-68-book-due-entry origin/tz-67-trend-book-in-code`, then:

  ```
  mkdir -p -m 0700 /tmp/tz68
  git show origin/main:CryptoTZ/TZ-68-book-due-entry.md \
      | awk '/^<!-- TZ-68 PATCH BEGIN -->$/{f=1;next} /^<!-- TZ-68 PATCH END -->$/{f=0} f' \
      | sed '1d;$d' > /tmp/tz68/tz68.patch
  md5sum /tmp/tz68/tz68.patch; wc -l < /tmp/tz68/tz68.patch
  git apply --check /tmp/tz68/tz68.patch && git apply /tmp/tz68/tz68.patch
  ```

  **Known answer:** the patch's MD5 is `b241f2ed6e53cb60b035bcf1803d2dcd` (208 lines), and both `git apply` commands exit 0.
  **Derived:** the Architect's session extracted the patch from this file with exactly these commands and applied it to
  a clean checkout of `c336d4d`. The TZ is read from `origin/main` because the branch, cut from TZ-67's, does not carry
  it. A different digest means the upload changed the file: BLOCKED, nothing applied.
- **B2.** `md5sum` and `wc -l` of the two files. **Known answer:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/book.py` | 297 | `8478a66a57ad4c48b2579e8cb0e382d9` |
  | `vps/selftest.py` | 1965 | `18f1a8a38dade5a2f73fd89353ca8f67` |

  **Derived:** the same application in the Architect's session. Any difference: BLOCKED.
- **B3.** `git add -A vps/ && git diff --cached --name-status origin/tz-67-trend-book-in-code` prints exactly two lines,
  status `M` for `vps/book.py` and for `vps/selftest.py`.
- **B4.** `rm -r /tmp/tz68` once the patch is applied.

---

## 9. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0, `selftest: sections 24 checks 457 failed 0 empty 0`,
  `section O: checks 33 failed 0` and `section X: checks 19 failed 0`. **Derived:** A1.3's 452 checks plus section X's
  five new ones, read by the Architect's session on §11's files under Python 3.11, 3.12 and 3.13.
  **Negative controls** (inv. 68), each applied alone in `vps/book.py`, then reverted, B2's digests restored and V1 green
  again — in each, every other check of all twenty-four sections stays green:
  1. `        if pos is None and k >= ENTRY_N and (k + 1 < len(bars) or open_now is not None):` →
     `        if pos is None and k >= ENTRY_N and k + 1 < len(bars):`: exit non-zero,
     `selftest: sections 24 checks 457 failed 4 empty 0`, and **exactly 4** checks of section X fail —
     `a breakout close on the last bar is due at the forming open: the position the next close records`,
     `a stop day's close on the last bar is due too: the position the next close records`,
     `a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet` and
     `--live names the entry due at the forming day's open, and its stop`;
  2. `                t_entry, entry = bars[k + 1][:2] if k + 1 < len(bars) else (t + DAY_MS, open_now)` →
     `                t_entry, entry = bars[k + 1][:2] if k + 1 < len(bars) else (t + DAY_MS, c)`: `failed 2` —
     `a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet` and
     `--live names the entry due at the forming day's open, and its stop`;
  3. `    forming = [float(r[1]) for r in rows if int(r[6]) >= now_ms]` →
     `    forming = [float(r[4]) for r in rows if int(r[6]) >= now_ms]`: `failed 2` —
     `live bars drop the day still open and keep its open` and `--live names the entry due at the forming day's open, and its stop`;
  4. `                   entry_due=bool(pos.get("entry_due")), exit_due=bool(pos.get("exit_due")))` →
     `                   entry_due=False, exit_due=bool(pos.get("exit_due")))`: `failed 2` —
     `a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet` and
     `--live names the entry due at the forming day's open, and its stop`;
  5. `        if b[0] - a[0] != DAY_MS:` → `        if False:`: `failed 1` —
     `a day missing from the archive is refused, never replayed over: the symbol and the days around it`.

  **Derived:** the Architect's session ran all five on §11's files under Python 3.11, 3.12 and 3.13 and read exactly these
  partitions.
- **V2. Syntax.** `python3 -m py_compile vps/book.py vps/selftest.py`.
- **V3. Scope.** `git diff --name-only origin/tz-67-trend-book-in-code...HEAD` lists exactly `vps/book.py` and
  `vps/selftest.py`; `git diff --name-only origin/main...HEAD` lists exactly `vps/book.py`, `vps/run.py` and
  `vps/selftest.py` — the pull request's whole change, TZ-67's and this TZ's. **Derived:** §4 and TZ-67's V4.
- **V4. Pushes.** The branch pushed and a pull request opened against `main`, its description naming #55 superseded — or
  contract §8's fallback; `main` receives nothing from this session but its report.

No regression: sections A–W keep their counts; section X goes from 14 to 19 — the two checks of the live path re-written
for `live_bars()`'s pair, five added — and TZ-67's other twelve checks of section X stay as they are.

---

## 10. The report

Contract §10's template. **The first three lines after `## Status`:**

1. **The base** — A1.2's answer: TZ-67's branch unmerged and this TZ's base, or merged.
2. **The code** — B1's patch digest and B2's two digests.
3. **The checks** — V1's total, sections O and X, and the five controls' partitions.

---

## Commit Message

Implementation, on the branch:

```
TZ-68: vps — the book's morning: a signal at the last close is an entry due at the forming day's open; a day missing from the archive is refused
```

Report, on `main`:

```
TZ-68: report — the book's due entry
```

---

## 11. The patch

Against `c336d4d`. B1 extracts the lines between the two markers, drops the fence lines, and applies the rest.

<!-- TZ-68 PATCH BEGIN -->
```diff
diff --git a/vps/book.py b/vps/book.py
index 55a0b8b..e43e6a9 100644
--- a/vps/book.py
+++ b/vps/book.py
@@ -54,11 +54,13 @@ def atr(bars, k):
     return total / ATR_N
 
 
-def replay(bars):
+def replay(bars, open_now=None):
     """bars: closed daily bars (t_open_ms, open, high, low, close), oldest first, one per UTC day.
     Returns (trades, position): each closed trade as a dict, and the open position after the last bar
     or None. A signal at day k's close fills at day k+1's open; a stop fills at the stop, or at the open
-    when the day opened beyond it; a channel exit at day k's close fills at day k+1's open."""
+    when the day opened beyond it; a channel exit at day k's close fills at day k+1's open. A signal at
+    the last bar's close fills at open_now, the open of the day still forming, and its position carries
+    entry_due; without open_now (the archive) that signal has no fill yet and opens nothing (TZ-68)."""
     trades, pos = [], None
     for k in range(len(bars)):
         t, o, h, l, c = bars[k]
@@ -77,23 +79,22 @@ def replay(bars):
                         pos = None
                         continue          # the exit day's own close cannot also open a trade
                     pos["exit_due"] = True
-        if pos is None and k >= ENTRY_N and k + 1 < len(bars):
+        if pos is None and k >= ENTRY_N and (k + 1 < len(bars) or open_now is not None):
             a = atr(bars, k)
             if a is None or a <= 0:
                 continue
             hi = max(b[2] for b in bars[k - ENTRY_N:k]); lo = min(b[3] for b in bars[k - ENTRY_N:k])
             side = 1 if c > hi else (-1 if c < lo else 0)
             if side:
-                nxt = bars[k + 1]
-                entry = nxt[1]
-                pos = dict(side=side, k_signal=k, k_entry=k + 1, t_entry=nxt[0], entry=entry, atr=a,
-                           stop=entry - side * STOP_ATR * a)
+                t_entry, entry = bars[k + 1][:2] if k + 1 < len(bars) else (t + DAY_MS, open_now)
+                pos = dict(side=side, k_signal=k, k_entry=k + 1, t_entry=t_entry, entry=entry, atr=a,
+                           stop=entry - side * STOP_ATR * a, entry_due=k + 1 == len(bars))
     return trades, pos
 
 
 def levels(bars, pos):
     """What the next close decides, from the last closed bar: the trigger and the stop a new trade would
-    take, or the open position's exit level."""
+    take, or the open position's exit level. A position whose entry is due has no open R yet."""
     k = len(bars) - 1
     t, o, h, l, c = bars[k]
     a = atr(bars, k)
@@ -106,8 +107,8 @@ def levels(bars, pos):
                    entry=pos["entry"], stop=pos["stop"],
                    exit_level=(min(b[3] for b in bars[k - EXIT_N + 1:k + 1]) if side > 0
                                else max(b[2] for b in bars[k - EXIT_N + 1:k + 1])),
-                   r_open=side * (c - pos["entry"]) / abs(pos["entry"] - pos["stop"]),
-                   exit_due=bool(pos.get("exit_due")))
+                   r_open=None if pos.get("entry_due") else side * (c - pos["entry"]) / abs(pos["entry"] - pos["stop"]),
+                   entry_due=bool(pos.get("entry_due")), exit_due=bool(pos.get("exit_due")))
     elif k >= ENTRY_N - 1 and a:
         hi = max(b[2] for b in bars[k - ENTRY_N + 1:k + 1]); lo = min(b[3] for b in bars[k - ENTRY_N + 1:k + 1])
         out.update(long_trigger=hi, short_trigger=lo, long_stop=hi - STOP_ATR * a, short_stop=lo + STOP_ATR * a)
@@ -128,8 +129,14 @@ def _get(url):
 
 
 def live_bars(symbol, now_ms):
+    """The closed daily bars, oldest first, and the open of the day still forming: the fill of a signal at
+    the last close. A read without that day is refused rather than replayed without it (TZ-68)."""
     rows = json.loads(_get(FAPI_KLINES % symbol))
-    return [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) < now_ms]
+    bars = [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) < now_ms]
+    forming = [float(r[1]) for r in rows if int(r[6]) >= now_ms]
+    if not forming:
+        raise ValueError("the read holds no day still forming")
+    return bars, forming[0]
 
 
 def _csv_rows(blob):
@@ -168,7 +175,9 @@ def _ms(t):
 
 
 def archive_series(symbol, start, end, cache):
-    """Daily bars and funding prints of one symbol from the archive, start..end inclusive (UTC dates)."""
+    """Daily bars and funding prints of one symbol from the archive, start..end inclusive (UTC dates). A day
+    missing between two bars -- the exchange's gap, or a month the cache remembers as a 404 from before it
+    was published -- is refused, never replayed over: replay() reads one bar per UTC day (TZ-68)."""
     bars, funding = {}, {}
     m = date(start.year, start.month, 1)
     last_month = date(end.year, end.month, 1)
@@ -190,7 +199,13 @@ def archive_series(symbol, start, end, cache):
         m = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
     lo = datetime(start.year, start.month, start.day, tzinfo=timezone.utc).timestamp() * 1000
     hi = datetime(end.year, end.month, end.day, tzinfo=timezone.utc).timestamp() * 1000
-    return ([bars[t] for t in sorted(bars) if lo <= t <= hi], sorted(funding.items()))
+    out = [bars[t] for t in sorted(bars) if lo <= t <= hi]
+    for a, b in zip(out, out[1:]):
+        if b[0] - a[0] != DAY_MS:
+            raise ValueError("%s: the archive has no daily bar between %s and %s" % (
+                symbol, datetime.fromtimestamp(a[0] / 1000, timezone.utc).date(),
+                datetime.fromtimestamp(b[0] / 1000, timezone.utc).date()))
+    return out, sorted(funding.items())
 
 
 def summary(rs):
@@ -258,8 +273,8 @@ def main(argv=None):
         now_ms = int(time.time() * 1000)
         for s in a.symbols:
             try:
-                bars = live_bars(s, now_ms)
-                trades, pos = replay(bars)
+                bars, open_now = live_bars(s, now_ms)
+                trades, pos = replay(bars, open_now)
                 out = dict(symbol=s, **levels(bars, pos)) if len(bars) > ENTRY_N else dict(symbol=s, state="short-history")
             except Exception as exc:          # one symbol's failure never hides the others
                 out = dict(symbol=s, state="unread", error=exc.__class__.__name__)
diff --git a/vps/selftest.py b/vps/selftest.py
index 6dea505..b690422 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -24,7 +24,9 @@ import tempfile
 import time
 import tracemalloc
 import types
+import urllib.error
 import urllib.parse
+import zipfile
 from datetime import datetime, timezone
 
 HERE = os.path.dirname(os.path.abspath(__file__))
@@ -1865,26 +1867,74 @@ def section_x(s):
     s.check("in a trade: the state, the entry day, and the exit level of the last 20 days",
             lv["state"] == "long" and lv.get("entry_date") == "1970-03-05" and lv.get("exit_level") == 94.0
             and abs(lv.get("r_open", 1)) < eps)
+    # TZ-68: the morning after a signal's close, the entry is due at the forming day's open -- the very
+    # position the next close records, so the live state and the archive's record are one book.
+    for name, world, n, fill in (("a breakout close on the last bar is due at the forming open", x_world_long(), 61, 105.0),
+                                 ("a stop day's close on the last bar is due too", x_world_short(), 63, 103.0)):
+        due, then = book.replay(world[:n], fill)[1], book.replay(world[:n + 1])[1]
+        s.check(name + ": the position the next close records",
+                due is not None and then is not None and due.get("entry_due") is True and then.get("entry_due") is False
+                and all(due[f] == then[f] for f in ("side", "k_entry", "t_entry", "entry", "stop")))
+    lv = book.levels(x_world_long()[:61], book.replay(x_world_long()[:61], 105.5)[1])
+    s.check("a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet",
+            lv["state"] == "long" and lv.get("entry_due") is True and lv.get("entry_date") == "1970-03-03"
+            and lv.get("entry") == 105.5 and abs(lv.get("stop", 0) - 101.1) < eps and lv.get("r_open", 0) is None)
     saved = book._get
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-x.")
     try:
-        rows = [[k * book.DAY_MS, "1", "2", "0.5", "1.5", "0", (k + 1) * book.DAY_MS - 1] for k in range(3)]
+        rows = [[k * book.DAY_MS, str(k + 1), "9", "0.5", "1.5", "0", (k + 1) * book.DAY_MS - 1] for k in range(3)]
         book._get = lambda url: json.dumps(rows).encode()
-        s.check("live bars drop the day still open", len(book.live_bars("XUSDT", 2 * book.DAY_MS + 5)) == 2)
+        bars, open_now = book.live_bars("XUSDT", 2 * book.DAY_MS + 5)
+        s.check("live bars drop the day still open and keep its open", len(bars) == 2 and open_now == 3.0)
         world = x_world_long()
+
+        def as_rows(bars, fill):
+            closed = [[b[0], str(b[1]), str(b[2]), str(b[3]), str(b[4]), "0", b[0] + book.DAY_MS - 1] for b in bars]
+            forming = [bars[-1][0] + book.DAY_MS, str(fill), str(fill + 1), str(fill - 1), str(fill + 0.25), "0", 10 ** 15]
+            return json.dumps(closed + [forming]).encode()
+
         def fake(url):
             if "BADUSDT" in url:
                 raise OSError("refused")
-            return json.dumps([[b[0], str(b[1]), str(b[2]), str(b[3]), str(b[4]), "0", b[0] + book.DAY_MS - 1]
-                               for b in world]).encode()
+            return as_rows(world[:61], 105.5) if "DUEUSDT" in url else as_rows(world, 122.0)
         book._get = fake
         with contextlib.redirect_stdout(io.StringIO()) as out:
-            code = book.main(["--live", "GOODUSDT", "BADUSDT"])
+            code = book.main(["--live", "GOODUSDT", "BADUSDT", "DUEUSDT"])
         lines = [json.loads(l) for l in out.getvalue().splitlines()]
         s.check("--live prints one object per symbol and survives one symbol's failure",
-                code == 0 and [l["symbol"] for l in lines] == ["GOODUSDT", "BADUSDT"]
+                code == 0 and [l["symbol"] for l in lines] == ["GOODUSDT", "BADUSDT", "DUEUSDT"]
                 and lines[0]["state"] == "flat" and lines[1]["state"] == "unread")
+        s.check("--live names the entry due at the forming day's open, and its stop",
+                len(lines) == 3 and lines[2]["state"] == "long" and lines[2].get("entry_due") is True
+                and lines[2].get("entry") == 105.5 and abs(lines[2].get("stop", 0) - 101.1) < eps)
+        served = {}
+
+        def vision(url):
+            if url in served:
+                return served[url]
+            raise urllib.error.HTTPError(url, 404, "Not Found", None, None)
+
+        def january(skip):
+            t0 = int(datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
+            buf = io.BytesIO()
+            with zipfile.ZipFile(buf, "w") as z:
+                z.writestr("k.csv", "open_time,open,high,low,close\n" + "".join(
+                    "%d,1,2,0.5,1.5\n" % (t0 + d * book.DAY_MS) for d in range(31) if d != skip))
+            return buf.getvalue()
+        book._get = vision
+        served[book.ARCHIVE + "/monthly/klines/XUSDT/1d/XUSDT-1d-2023-01.zip"] = january(None)
+        served[book.ARCHIVE + "/monthly/klines/YUSDT/1d/YUSDT-1d-2023-01.zip"] = january(14)
+        whole = len(book.archive_series("XUSDT", book.date(2023, 1, 1), book.date(2023, 1, 31), tmp)[0]) == 31
+        try:
+            book.archive_series("YUSDT", book.date(2023, 1, 1), book.date(2023, 1, 31), tmp)
+            refused = ""
+        except ValueError as exc:
+            refused = str(exc)
+        s.check("a day missing from the archive is refused, never replayed over: the symbol and the days around it",
+                whole and refused == "YUSDT: the archive has no daily bar between 2023-01-14 and 2023-01-16")
     finally:
         book._get = saved
+        shutil.rmtree(tmp, ignore_errors=True)
 
 
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
```
<!-- TZ-68 PATCH END -->
