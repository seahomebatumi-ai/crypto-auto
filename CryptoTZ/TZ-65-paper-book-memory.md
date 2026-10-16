# TZ-65 — The paper test's booking in bounded memory: one symbol's minutes at a time, four doubles a minute, dropped when the pass ends — on TZ-64's branch

**Canonical filename:** `CryptoTZ/TZ-65-paper-book-memory.md`
**Report:** `CryptoReports/TZ-65-paper-book-memory-report.md`
**Host:** any machine with the repository, `git` and Python 3 — no stage touches the VPS. The deployer runs the
selftest before it installs the merge (map §10).
**Class:** branch TZ (contract §8) — it modifies two files, on top of TZ-64's branch.
**Branch:** `claude/tz-65-paper-book-memory`, from `claude/tz-64-paper-test` at `843ba3f` · **Model:** Sonnet
**Previous TZ:** TZ-64, executed 16.10.2026; its audit of 17.10.2026 did not accept it, for the defect §3 names, and
pull request #52 is not merged. **This TZ builds on that branch on purpose** (contract §8): its pull request carries
TZ-64's three commits and its own, and supersedes #52.
**Written against:** contract v30, map `2026-10-16-c`, methodology `2026-10-16-b`, `main` at `7026357` — its `vps`
tree `96d72e8df795c79ad7d77c9ee73d4bbc284534e7` — and `claude/tz-64-paper-test` at `843ba3f`, tree
`91ba4c3647e9d66045d904e511ea8022083fa4ab`, read by the Architect from the repository on 17.10.2026. TZ-64's §12 is
the rule; §12 below adds one item to it and moves no number.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-16-c.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-16-c.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | its version line reads `**Version 30.**`; lines and MD5 reported |
| `ANALYST-INSTRUCTIONS.md` | 4381 | `d665a12f789c9c0a2bb3d090265c22bf` | reported; this TZ reads none of it and changes nothing it reads |
| `vps/paper.py` at `origin/claude/tz-64-paper-test` | 1229 | `cf160b4dd8cfe5d81a1b5d6e682c230a` | equal, or BLOCKED — §13's patch applies to exactly these bytes |
| `vps/selftest.py` at `origin/claude/tz-64-paper-test` | 1683 | `7a876961c3497505da7e08401964bb6b` | equal, or BLOCKED — §13's patch applies to exactly these bytes |

The map itself: 2779 lines, MD5 `4c3c60f0c16ac6d7bd8016c0cb370938` — reported, not enforced. The two `vps` files are
measured on the branch, `git show origin/claude/tz-64-paper-test:<file>`; on `main` neither carries TZ-64's bytes.

---

## 1. Credentials

None arrives, none is read and none is written. No stage runs on the VPS or starts a unit.

---

## 2. Contract, map and code text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section or file named.

> Before starting, check whether the previous TZ's branch was merged. If it was not, say so at the top of your report — building on an unmerged base produces work that is complete and live nowhere.

— contract §8. TZ-64's branch is unmerged by the audit's decision; the report says so first, and this TZ's pull
request is the one whose merge puts both in effect.

> Commit message: the string given in the TZ's `## Commit Message`, verbatim.

— contract §8. The string is under `## Commit Message` below.

> A second implementation of any rule, threshold or formula is banned in any language and any file.

— map inv. 38. `paper.last_day` is the one statement of the last day an episode's book reads; `book_episode` and
`produce_books` both call it.

> 1 CPU, 955 MB, 74 MB available and 1 543 MB of swap in use

— map §10, row «The assistant's build sequence», as that row measured it: the host this unit shares with the
analysis run, whose admission is decided by what the host frees.

> The hosted `bench.yml` does not run `vps/selftest.py`; the deployer runs it before every install, and that is its gate

— map §10. V1 is that selftest, run here before the deployer runs it again.

---

## 3. What is fixed, and why

**The defect is the Architect's, in TZ-64's §13; the Executor applied those bytes exactly, and no check of TZ-64
could see it**, because none bounded what a booking pass holds. TZ-64's `Inputs` kept every 1-minute file its passes
read for a whole UTC day, each minute a tuple of five Python objects — 375 KiB a symbol-day — and an episode's book
reads every day from its opening to its exit, so a day's pass grows with the spans of the episodes that closed that
day, and the window's last day books every episode still open, cut, from the day it opened.

**Measured on 17.10.2026 in the Architect's workspace**, with production's own `produce_books` on zips of Binance's
twelve columns: a pass costs about 26 MiB and 0.43 MiB more for each symbol-day it holds, so the unit's
`MemoryMax=128M` is passed near 235 symbol-days — three cut episodes of 91 days on three symbols peak at 146 MiB.
**On the fills of the 31 accounts the workspace's selection of 16.10.2026 picked, replayed through
`apply_fill` over their last 91 days — 1 501 episodes closed and 223 cut — the window's last day holds
3 423 symbol-days, about 1 512 MiB, and 2 other days hold more than 235, the heaviest
775.**
Above the limit the unit either swaps on a host already at its memory ceiling, taking what the run's admission needs
free, or is killed: the state is saved at the end of a loop, so the restart repeats the polls made before the pass —
a fresh pick event is alerted a second time — and runs the same pass again at once.

**The fix:** (1) the minutes are kept as arrays, one time and four prices a minute — 63 KiB a symbol-day; (2) only one
symbol's minutes are kept — asking for another symbol drops them; (3) a day's episodes are booked symbol by symbol,
the symbol of the latest day first, so each minute file is read once a pass, and the lines are written in the episode
file's order; (4) the latest day any episode reads is asked for first, so a day not yet published ends the pass after
one read instead of after every read before it; (5) the minutes are dropped when a day's pass ends, written or not.
Measured the same way: a peak of 35–39 MiB for one to five symbols of 91 days, 30 MiB for ten of 30, and nothing kept
after the pass.

**No number moves.** On a day of 40 episodes over four symbols — spans from 15 minutes to 60 days, longs and shorts,
cut and closed, stops touched and gapped through, a symbol whose minute files are absent, minute rows served out of
order — the book and funding files written by `843ba3f` and by §13's patch are byte-identical: book MD5
`ff6369e889c7c5086ba1ff5d03e068cd`, funding MD5 `ab341efed9431555f9441c4af96130e3`, 30 booked, 10 unbookable, 51 cells
stopped, 13 of them through a gap. The audit also ran `paper.service` end to end offline — the selection's record,
polls, days, books, funding, the verdict and pushes to a local remote, and a restart that resumed without a second
alert — and found nothing else to reject in TZ-64.

**What happens after the merge, and is not this TZ's to report** (contract §8, inv. 54): TZ-64's §3 paragraph of the
same name, unchanged — the deployer installs the tree, the unit selects once, commits `analyst/paper/selection.json`,
tells the owner and follows.

---

## 4. Scope

### Files to Create

None.

### Files to Modify

```
vps/paper.py    vps/selftest.py
```

### Files to Delete

None.

### On the VPS

Nothing.

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The rule.** TZ-64's §12 stands; §12 below adds item 12.3.6, which moves no number (§3).
- **The poll loop.** A booking pass still runs inside it: on its heaviest day the pass reads each minute file once,
  and a pick's event older than 600 s when the loop returns raises no alert (TZ-64 12.5.2). Nothing booked depends on
  an alert.
- **The map.** TZ-64 §5's two items stale at the merge — §11's path table and its sentence «`bench.yml` ignores FOUR
  paths in this tree» — still stand, and the merge of this TZ's pull request is that merge; the Architect's revision
  after this TZ's audit repairs both, with the §10 row.
- **Pull request #52.** This session neither closes nor comments on it; this TZ's pull request names it superseded.

---

## 6. Rules — binding in every stage

1. **No VPS and no unit**; the session's network reads are `git`'s and `gh`'s, nothing else.
2. **§13's patch is extracted byte for byte, never retyped** — by the one command B1 gives.
3. **Python 3's standard library only.**

---

## 7. Stage A — readings, no writes

- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/claude/tz-64-paper-test 'origin/claude/tz-64-paper-test^{tree}'`. **Known answer:**
     `843ba3ff9faaac66cf458d21d01f94eea88bc171` and `91ba4c3647e9d66045d904e511ea8022083fa4ab`. **Derived:** TZ-64's
     report and the Architect's audit read both. **Any other answer: BLOCKED** — the branch moved after the audit.
  2. `git merge-base --is-ancestor origin/claude/tz-64-paper-test origin/main; echo $?`. **Known answer:** `1`.
     **Derived:** the audit did not accept TZ-64, and #52 was open at `7026357`. **`0` — TZ-64 already merged: BLOCKED**,
     because this TZ's base is then `main` and its pull request would carry nothing of TZ-64.
  3. On a checkout of `origin/claude/tz-64-paper-test`, `python3 vps/selftest.py`. **Known answer:** exit 0 and
     `selftest: sections 23 checks 419 failed 0 empty 0`. **Derived:** TZ-64's V1, and the audit's run on the same
     tree.

---

## 8. Stage B — the code, on the branch

- **B1.** `git checkout -b claude/tz-65-paper-book-memory origin/claude/tz-64-paper-test`, then:

  ```
  mkdir -p -m 0700 /tmp/tz65
  git show origin/main:CryptoTZ/TZ-65-paper-book-memory.md \
      | awk '/^<!-- TZ-65 PATCH BEGIN -->$/{f=1;next} /^<!-- TZ-65 PATCH END -->$/{f=0} f' \
      | sed '1d;$d' > /tmp/tz65/tz65.patch
  md5sum /tmp/tz65/tz65.patch; wc -l < /tmp/tz65/tz65.patch
  git apply --check /tmp/tz65/tz65.patch && git apply /tmp/tz65/tz65.patch
  ```

  **Known answer:** the patch's MD5 is `0626e9f4614abb45a0bf366361def75d` (312 lines), and both `git apply` commands exit 0.
  **Derived:** the Architect's session wrote this TZ, extracted the patch with exactly these commands, and applied it
  to a clean checkout of `843ba3f`. The TZ is read from `origin/main` because the branch, cut from TZ-64's, does not
  carry it. A different digest means the upload changed the file: BLOCKED, nothing applied.
- **B2.** `md5sum` and `wc -l` of the two files. **Known answer:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/paper.py` | 1281 | `057440a4b5c9c277cc99062f768464ac` |
  | `vps/selftest.py` | 1807 | `04d484d41ac49a466ec60c0df3c17dda` |

  **Derived:** the same application in the Architect's session. Any difference: BLOCKED.
- **B3.** `git diff --summary origin/claude/tz-64-paper-test` prints no mode line: both files stay `100644`.
- **B4.** `rm -r /tmp/tz65` once the patch is applied.

---

## 9. Stage C — the gate on the runner

- **C1.** Commit, push the branch, then `gh run list -R seahomebatumi-ai/crypto-auto -w bench.yml
  -b claude/tz-65-paper-book-memory -e push --json headSha,status,conclusion`. **Known answer:** a run for the
  implementation commit's SHA, conclusion `success`. **Derived:** the commit changes `vps/**`, which no entry ignores;
  no step of the gate reads `vps/`, so its outcome is TZ-64's run `38956367050`'s on the rest of the same tree. A read
  `gh` refuses is reported as a gap and the audit reads the run itself (contract §9).

---

## 10. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0,
  `selftest: sections 23 checks 432 failed 0 empty 0` and `section W: checks 102 failed 0`. **Derived:** A1.3's 419
  checks plus the 13 of section W's new part W15, read by the Architect's session on §13's files under Python 3.11,
  3.12 and 3.13. **Negative controls** (inv. 68), each applied alone, then reverted, B2's digests restored and V1 green
  again — in each, every other check of all twenty-three sections stays green:
  1. in `vps/paper.py`, the line `            self.klines, self.kl_sym = {}, sym` → `            self.kl_sym = sym`: exit non-zero, `selftest: sections 23 checks 432 failed 2 empty 0`, and **exactly 2** checks of section W fail — `asking for another symbol drops the first one's days`, `a pass holds one symbol's days at most: six, of eighteen read`;
  2. in `vps/paper.py`, the line `            inputs.drop_minutes()` → `            pass`: exit non-zero, `selftest: sections 23 checks 432 failed 1 empty 0`, and **exactly 1** check of section W fails — `after the pass no minute is kept`;
  3. in `vps/paper.py`, the line `                    inputs.minutes(latest[1], latest[0])   # not yet published: NotReady ends the pass here` → `                    pass`: exit non-zero, `selftest: sections 23 checks 432 failed 1 empty 0`, and **exactly 1** check of section W fails — `a latest day not yet published ends the pass after one read, nothing written or kept`;
  4. in `vps/paper.py`, the line `            for i in sorted(range(len(eps)), key=lambda i: (eps[i]["symbol"] != latest[1], eps[i]["symbol"], i)):` → `            for i in range(len(eps)):`: exit non-zero, `selftest: sections 23 checks 432 failed 1 empty 0`, and **exactly 1** check of section W fails — `each minute file is read once in a pass`;
  5. in `vps/paper.py`, the line `                                        array.array("d", [v for x in rows for v in x[1:]]))` → `                                        [v for x in rows for v in x[1:]])`: exit non-zero, `selftest: sections 23 checks 432 failed 1 empty 0`, and **exactly 1** check of section W fails — `minutes: one symbol-day is kept in under 128 KiB`.

  **Derived:** the Architect's session ran all five on §13's files and read exactly these partitions.
- **V2. Syntax.** `python3 -m py_compile vps/paper.py vps/selftest.py`.
- **V3. Scope.** `git diff --name-only origin/claude/tz-64-paper-test...HEAD` lists exactly `vps/paper.py` and
  `vps/selftest.py`; `git diff --name-only origin/main...HEAD` lists exactly TZ-64's nine files.
- **V4. Pushes.** The branch pushed and a pull request opened against `main` after C1 — its description naming #52
  as superseded — or contract §8's fallback; `main` receives nothing from this session but its report.

No regression: sections A–V keep their counts, W's 89 earlier checks stay green, and `book_delay`, `sigma_for`,
`funding_line` and every number a book carries are unchanged (§3, re-run by the audit).

---

## 11. The report

Contract §10's template. **The first lines after `## Status`:** that TZ-64's branch is unmerged and is this TZ's base
(contract §8); then

1. **The base** — A1.1's two values and A1.2's exit code.
2. **The code** — B1's patch digest and B2's two digests.
3. **The checks** — V1's total and the five controls' partitions.
4. **The gate** — C1's SHA and what its listing showed.

---

## 12. The rule — one item added to TZ-64's §12.3

**12.3.6 Memory.** A booking pass holds the 1-minute klines of one symbol at a time, kept as arrays — one time and
four prices a minute — and drops them when the day's pass ends, written or not. A day's episodes are booked symbol by
symbol, the symbol of the latest day first, so each minute file is read once a pass; that latest day is asked for
before anything else, so a day not yet published ends the pass after one read. The book's lines keep the episode
file's order. *[Architect's decision, TZ-65: TZ-64's pass kept every minute file of a UTC day as Python tuples, which
passes the unit's 128 MiB near 235 symbol-days; the selected accounts' last 91 days put the window's last day at
3 423. Discarded: a higher `MemoryMax`, which moves the unit's load onto the host the analysis run is admitted to.]*

---

## Commit Message

`TZ-65: vps — the paper test's booking in bounded memory: one symbol's minutes at a time, four doubles a minute, dropped when the pass ends`

---

## 13. The patch

Against `843ba3f`. B1 extracts the lines between the two markers, drops the fence lines, and applies the rest.

<!-- TZ-65 PATCH BEGIN -->
```diff
diff --git a/vps/paper.py b/vps/paper.py
index 75a400e..d051633 100644
--- a/vps/paper.py
+++ b/vps/paper.py
@@ -1,5 +1,5 @@
 #!/usr/bin/env python3
-"""The copy-trading paper test (TZ-64; map section 10, row \u00abHyperliquid's large accounts\u00bb):
+"""The copy-trading paper test (TZ-64, TZ-65; map section 10, row \u00abHyperliquid's large accounts\u00bb):
 Hyperliquid accounts selected once by their twelve-month record, followed in real time,
 every copied episode booked on Binance USD-M prices at four delays, and the verdict
 read at week 13 against random eligible accounts copied the same way.
@@ -14,6 +14,7 @@ analyst/paper/ of its own clone and pushed to main (contract v30 section 8); a r
 is written once and never reopened.
 """
 import argparse
+import array
 import bisect
 import codecs
 import hashlib
@@ -571,13 +572,29 @@ def vision_rows(path):
     return rows[1:] if rows and not rows[0][0].strip().isdigit() else rows
 
 
+class Rows:
+    """The (open, high, low, close) of consecutive minutes, four doubles a minute in one array: a
+    symbol-day is kept in 63 KiB with its times, against 375 KiB as a list of tuples (12.3.6)."""
+
+    def __init__(self, flat):
+        self.flat = flat
+
+    def __len__(self):
+        return len(self.flat) // 4
+
+    def __getitem__(self, k):
+        if not 0 <= k < len(self):
+            raise IndexError(k)
+        return tuple(self.flat[4 * k:4 * k + 4])
+
+
 class Inputs:
-    """data.binance.vision inputs of one pass: 1m klines by symbol and day, daily closes kept on
-    disk, funding rates by symbol and month. A 404 dated more than ABSENT_AFTER_DAYS before today is
-    Absent; nearer is NotReady."""
+    """data.binance.vision inputs of one pass: 1m klines of one symbol at a time by day, daily
+    closes kept on disk, funding rates by symbol and month. A 404 dated more than ABSENT_AFTER_DAYS
+    before today is Absent; nearer is NotReady."""
 
     def __init__(self, state_dir, today, rows=vision_rows):
-        self.today, self.rows, self.klines, self.rates_by = today, rows, {}, {}
+        self.today, self.rows, self.klines, self.kl_sym, self.rates_by = today, rows, {}, None, {}
         self.closes_path = os.path.join(state_dir, "closes.json")
         try:
             with open(self.closes_path, encoding="utf-8") as fh:
@@ -593,15 +610,30 @@ class Inputs:
             raise (Absent if gap > ABSENT_AFTER_DAYS else NotReady)(path) from None
 
     def minutes(self, sym, date):
-        key = (sym, date)
-        if key not in self.klines:
-            rows = self.fetch("/daily/klines/%s/1m/%s-1m-%s.zip" % (sym, sym, date), date)
-            self.klines[key] = [(int(r[0]), (float(r[1]), float(r[2]), float(r[3]), float(r[4]))) for r in rows]
-        return self.klines[key]
+        """One day of sym's minutes inside that day, ascending: (open times, Rows' flat array). Only
+        sym's days are kept -- asking for another symbol drops them (12.3.6)."""
+        if sym != self.kl_sym:
+            self.klines, self.kl_sym = {}, sym
+        if (sym, date) not in self.klines:
+            start = day_start(date)
+            rows = sorted(x for x in ((int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in
+                                      self.fetch("/daily/klines/%s/1m/%s-1m-%s.zip" % (sym, sym, date), date))
+                          if start <= x[0] < start + DAY_MS)
+            self.klines[(sym, date)] = (array.array("q", [x[0] for x in rows]),
+                                        array.array("d", [v for x in rows for v in x[1:]]))
+        return self.klines[(sym, date)]
 
     def kl(self, sym, first, last):
-        merged = sorted(row for d in days_between(first, last) for row in self.minutes(sym, d))
-        return [t for t, _ in merged], [r for _, r in merged]
+        """sym's minutes from day first to day last: (open times, Rows), ascending across the days."""
+        times, flat = array.array("q"), array.array("d")
+        for d in days_between(first, last):
+            t, f = self.minutes(sym, d)
+            times.extend(t)
+            flat.extend(f)
+        return times, Rows(flat)
+
+    def drop_minutes(self):
+        self.klines, self.kl_sym = {}, None
 
     def close_on(self, sym, date):
         have = self.closes.setdefault(sym, {})
@@ -621,6 +653,12 @@ class Inputs:
         return self.rates_by[key]
 
 
+def last_day(ep, window_end):
+    """The last day whose minutes the episode's book reads: its exit at the longest delay, or
+    window_end's day for a cut episode."""
+    return utc_date(window_end if ep.get("cut") else ep["t_close"] + max(DELAYS_S) * 1000)
+
+
 def book_episode(ep, inputs, rule, window_end):
     """The book line of one episode: sigma_for, the stop distance INV_FLOOR_SD sigma, and every
     delay; or an unbookable line."""
@@ -632,8 +670,7 @@ def book_episode(ep, inputs, rule, window_end):
         dist = rule["inv_floor_sd"] * sigma
         if not dist > 0:
             raise Absent("sigma is zero")
-        last = utc_date(window_end if ep.get("cut") else ep["t_close"] + max(DELAYS_S) * 1000)
-        kl = inputs.kl(ep["symbol"], first, last)
+        kl = inputs.kl(ep["symbol"], first, last_day(ep, window_end))
         line.update(sigma_d=sigma, dist=dist, d={
             str(d): book_delay(ep, d, dist, kl, rule["capital_usdt"], rule["risk_pct"] / 100, rule["fee_taker"],
                                window_end) for d in DELAYS_S})
@@ -1015,14 +1052,29 @@ def produce_days(state, state_dir, sel, now):
 
 
 def produce_books(state, state_dir, sel, rule, inputs):
-    first = utc_date(sel["follow_from_ms"])
+    """Book files in date order. Per day: the latest day any episode reads is asked for first, so a
+    day not yet published ends the pass after one read; then the episodes are booked one symbol at a
+    time, that symbol first, so each minute file is read once; the lines keep the episode file's
+    order, and the minutes are dropped when the day's pass ends, written or not (12.3.6)."""
+    first, window_end = utc_date(sel["follow_from_ms"]), sel["window_end_ms"]
     while True:
         day = next_date(state["written"]["book"], first)
         if state["written"]["episodes"] is None or day > state["written"]["episodes"]:
             return
         eps = [e for e in read_jsonl(os.path.join(state_dir, "records", RECORD_DIR, "episodes", day + ".jsonl"))
                if e["k"] == "ep"]
-        lines = [book_episode(e, inputs, rule, sel["window_end_ms"]) for e in eps]   # NotReady ends the pass
+        latest = max(((last_day(e, window_end), e["symbol"]) for e in eps), default=None)
+        lines = [None] * len(eps)
+        try:
+            if latest is not None:
+                try:
+                    inputs.minutes(latest[1], latest[0])   # not yet published: NotReady ends the pass here
+                except Absent:
+                    pass                                   # that episode's own book records it unbookable
+            for i in sorted(range(len(eps)), key=lambda i: (eps[i]["symbol"] != latest[1], eps[i]["symbol"], i)):
+                lines[i] = book_episode(eps[i], inputs, rule, window_end)   # NotReady ends the pass
+        finally:
+            inputs.drop_minutes()
         head = {"k": "day", "date": day, "booked": sum(1 for x in lines if "d" in x),
                 "unbookable": sum(1 for x in lines if "unbookable" in x)}
         write_record(state, state_dir, "book/%s.jsonl" % day, [head] + lines)
diff --git a/vps/selftest.py b/vps/selftest.py
index 3963832..e3378da 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1,7 +1,7 @@
 #!/usr/bin/env python3
 """The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
-TZ-62 B2, TZ-64 B4): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's, TZ-57 §12.8's,
-TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's and TZ-64's changed and new ones, each printing
+TZ-62 B2, TZ-64 B4, TZ-65 B1): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's,
+TZ-57 §12.8's, TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's, TZ-64's and TZ-65's changed and new ones, each printing
 `section <X>: checks <n> failed <m>`, then the total.
 
     python3 vps/selftest.py
@@ -9,6 +9,7 @@ TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's and TZ-64's changed and new ones
 Exit non-zero on any failure and on any section that compared nothing (inv. 22).
 Offline: every fixture is built here or read from the checkout this file sits in.
 """
+import array
 import contextlib
 import copy
 import io
@@ -21,6 +22,7 @@ import subprocess
 import sys
 import tempfile
 import time
+import tracemalloc
 import types
 import urllib.parse
 from datetime import datetime, timezone
@@ -1577,6 +1579,8 @@ def section_w(s):
         "LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key"])
     # W14. the flow, offline: polls, the cut, three days of episodes, books, funding and the verdict
     section_w_flow(s)
+    # W15. the booking's memory (TZ-65): one symbol's minutes at a time, compact, dropped after the pass
+    section_w_memory(s)
 
 
 def w_rows(path):
@@ -1655,6 +1659,126 @@ def section_w_flow(s):
         shutil.rmtree(tmp, ignore_errors=True)
 
 
+def w_counted_rows(reads, unpublished_from=None):
+    """w_rows with every read counted by path; a 1m file dated unpublished_from or later is not
+    published, and the day's rows come shuffled, with one row of each neighbouring day."""
+    def rows(path):
+        reads[path] = reads.get(path, 0) + 1
+        name = path.rsplit("/", 1)[1][:-4]
+        if "-1m-" not in name:
+            return w_rows(path)
+        date = "-".join(name.rsplit("-", 3)[-3:])
+        if unpublished_from is not None and date >= unpublished_from:
+            raise paper.NotPublished(path)
+        start = paper.day_start(date)
+        out = [[str(m), "100", "101", "99", repr(100 + (m - start) / 60000000.0)]
+               for m in range(start, start + paper.DAY_MS, 60000)]
+        stray = [[str(start - 60000), "1", "1", "1", "1"], [str(start + paper.DAY_MS), "1", "1", "1", "1"]]
+        return out[1::2] + out[0::2] + stray
+    return rows
+
+
+def section_w_memory(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-w15.")
+    try:
+        rows = paper.Rows(array.array("d", [1, 2, 3, 4, 5, 6, 7, 8]))
+        s.check("Rows: two minutes of four doubles, read back as tuples",
+                len(rows) == 2 and rows[0] == (1.0, 2.0, 3.0, 4.0) and rows[1] == (5.0, 6.0, 7.0, 8.0))
+        raised = 0
+        for k in (2, -1):
+            try:
+                rows[k]
+            except IndexError:
+                raised += 1
+        s.check("Rows: a minute before the first or past the last raises IndexError", raised == 2)
+        reads = {}
+        inputs = paper.Inputs(tmp, "2026-03-01", rows=w_counted_rows(reads))
+        times, flat = inputs.minutes("BTCUSDT", "2026-01-05")
+        start = paper.day_start("2026-01-05")
+        s.check("minutes: one day's 1 440 minutes ascending, the neighbouring days' rows left out",
+                list(times) == list(range(start, start + paper.DAY_MS, 60000)))
+        s.check("minutes: a minute's (o, h, l, c) where its time is",
+                paper.Rows(flat)[731] == (100.0, 101.0, 99.0, 100 + 731 * 60000 / 60000000.0))
+        tracemalloc.start()
+        try:
+            before = tracemalloc.get_traced_memory()[0]
+            inputs.minutes("BTCUSDT", "2026-01-06")
+            kept = tracemalloc.get_traced_memory()[0] - before
+        finally:
+            tracemalloc.stop()
+        s.check("minutes: one symbol-day is kept in under 128 KiB", kept < 128 * 1024)
+        kt, kr = inputs.kl("BTCUSDT", "2026-01-05", "2026-01-07")
+        s.check("kl over three days: 4 320 minutes, ascending, each day where it belongs",
+                len(kt) == 4320 == len(kr) and all(kt[k] < kt[k + 1] for k in range(len(kt) - 1))
+                and kt[1440] == start + paper.DAY_MS and kr[1440][3] == 100.0)
+        inputs.minutes("ETHUSDT", "2026-01-05")
+        s.check("asking for another symbol drops the first one's days",
+                inputs.kl_sym == "ETHUSDT" and list(inputs.klines) == [("ETHUSDT", "2026-01-05")])
+        # a day file of three symbols, interleaved, five days each
+        we = paper.day_start("2026-01-20") + 12 * 3600000
+        sel = {"follow_from_ms": we - 14 * paper.DAY_MS, "window_end_ms": we}
+        rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
+        day = paper.utc_date(we)
+        eps = []
+        for k, sym in enumerate(["BTC", "ETH", "KAITO"] * 2):
+            t_open = we - (5 - k % 2) * paper.DAY_MS + k * 60000
+            eps.append({"k": "ep", "a": "0x%040x" % k, "role": "null", "rank": None, "coin": sym,
+                        "symbol": sym + "USDT", "side": 1 if k % 2 else -1, "t_open": t_open, "px_open": "100",
+                        "n": 1, "seen_open_ms": t_open, "t_close": we, "px_close": None, "seen_close_ms": None,
+                        "cut": True})
+        root = os.path.join(tmp, "records", paper.RECORD_DIR)
+        os.makedirs(os.path.join(root, "episodes"))
+        with open(os.path.join(root, "episodes", day + ".jsonl"), "w", encoding="utf-8") as fh:
+            fh.write(json.dumps({"k": "day", "date": day}) + "\n" + "".join(json.dumps(e) + "\n" for e in eps))
+        prev = paper.add_days(day, -1)
+
+        def fresh_state():
+            return {"pending": [], "written": {"episodes": day, "book": prev, "funding": prev}}
+
+        reads, held = {}, []
+        inputs = paper.Inputs(tmp, "2026-03-01", rows=w_counted_rows(reads))
+        minutes = inputs.minutes
+
+        def watched(sym, date):
+            out = minutes(sym, date)
+            held.append(len(inputs.klines))
+            return out
+        inputs.minutes = watched
+        state = fresh_state()
+        paper.produce_books(state, tmp, sel, rule, inputs)
+        ones = [n for p, n in reads.items() if "/1m/" in p]
+        s.check("a pass holds one symbol's days at most: six, of eighteen read", max(held) == 6 and len(ones) == 18)
+        s.check("each minute file is read once in a pass", ones == [1] * 18)
+        s.check("after the pass no minute is kept", inputs.klines == {} and inputs.kl_sym is None)
+        with open(os.path.join(root, "book", day + ".jsonl"), encoding="utf-8") as fh:
+            book = [json.loads(line) for line in fh][1:]
+        s.check("the book keeps the episode file's order, all six booked",
+                [(b["a"], b["coin"], b["t_open"]) for b in book] == [(e["a"], e["coin"], e["t_open"]) for e in eps]
+                and all("d" in b for b in book))
+        # the latest day not yet published: one minute read, then NotReady, nothing written, nothing kept
+        reads = {}
+        inputs = paper.Inputs(tmp, paper.add_days(day, 1), rows=w_counted_rows(reads, unpublished_from=day))
+        state = fresh_state()
+        try:
+            paper.produce_books(state, tmp, sel, rule, inputs)
+            waited = False
+        except paper.NotReady:
+            waited = True
+        s.check("a latest day not yet published ends the pass after one read, nothing written or kept",
+                waited and sum(reads.values()) == 1 and state["written"]["book"] == prev and inputs.klines == {})
+        # the latest day absent (dated past ABSENT_AFTER_DAYS): the pass goes on, those episodes unbookable
+        reads = {}
+        inputs = paper.Inputs(tmp, paper.add_days(day, 10), rows=w_counted_rows(reads, unpublished_from=day))
+        state = fresh_state()
+        paper.produce_books(state, tmp, sel, rule, inputs)
+        with open(os.path.join(root, "book", day + ".jsonl"), encoding="utf-8") as fh:
+            head = json.loads(fh.readline())
+        s.check("an absent latest day is no wait: the day is written, its six episodes unbookable",
+                state["written"]["book"] == day and head["booked"] == 0 and head["unbookable"] == 6)
+    finally:
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
```
<!-- TZ-65 PATCH END -->
