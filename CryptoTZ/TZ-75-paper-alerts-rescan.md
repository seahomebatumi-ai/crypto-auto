# TZ-75 — The paper test: the whale's number, its leverage and a coloured close in every alert; the selection rule re-applied every four weeks until three whales are followed

**Canonical filename:** `CryptoTZ/TZ-75-paper-alerts-rescan.md`
**Report:** `CryptoReports/TZ-75-paper-alerts-rescan-report.md`
**Class:** branch TZ (contract §8) — it authorises two repository files besides its report.
**Branch:** `claude/tz-75-paper-alerts-rescan`
**Host:** the VPS, for stage C's selftest and probe; stages A–B run on any clone.
**Model:** Sonnet — the change is the patch of §9, written and executed by the Architect; the session applies it,
proves its bytes and runs the validation.
**Trigger:** `EXECUTE TZ-75`, with nothing under it: no credential arrives and the Boss is asked for nothing.
**Previous TZ:** TZ-74, COMPLETED, report-only; nothing of it awaits a merge. No branch on the remote is ahead of `main`.
**Issued:** 29.10.2026, by the Architect.
**Written against:** contract v31, map `2026-10-26-a`, and `main` at `92ebce3`, read from the repository on 29.10.2026.

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
| `vps/paper.py` | 1281 | `057440a4b5c9c277cc99062f768464ac` | equal, or A1 stops: §9 is written against these bytes, which are also the running service's (`analyst/paper/selection.json` `fp.paper_md5`) |
| `vps/selftest.py` | 2430 | `1f207b2dce474439924b1ef22c82e918` | equal, or A1 stops: §9 is written against these bytes |
| `vps/units/crypto-paper.service` | 30 | `082a64f8f3a11ca4d4fab6a3974a97e8` | equal, or A1 stops: §3 B3's memory bound rests on its `MemoryMax=128M`, and this TZ does not touch it |

The map itself: 2796 lines, MD5 `e911fceb5f07444fe306f116a550b9cf` — reported, not enforced.

---

## 1. What changes, and the evidence for it

**The owner, 29.10.2026, verbatim:** «I want the leverage multiplier (x leverage) to be displayed in incoming SMS
notifications when a 🐋 opens a trade!» · «Notifications must arrive in exactly the same format, with the symbols styled
exactly as shown!» · «if the trade closes in profit, the cross should be displayed in green!» · «we should have at least
three whales in total.» The format he showed is his own three messages to the bot of 29.10.2026, reproduced in §3 A1.

**A — the alerts.** Every alert names the whale by a number and a whale, a LONG by 🟢 and a SHORT by 🔴; an open carries
the whale's leverage; a close carries ❎ when the copy gained and ❌ when it did not, and a clock before the time held.

**B — the rescan.** The selection of 17.10.2026 asked for three picks (TZ-64 12.1.7) and found two: of 4 033 accounts in
the pool, 146 eligible and 9 passing the twelve-month rule, 7 failed copyability — three hold a median episode under a
minute, three trade more than a fifth of their notional off Binance, and one closed no episode in the window
(`analyst/paper/selection.json`). **Two measurements
make the gap a defect of the test, not of the market:**

1. **Its verdict is out of reach.** From 17.10 to 28.10 the two picks closed **2** episodes (`analyst/paper/episodes/`);
   the verdict is readable only at **30** booked pick episodes at 1 800 s (TZ-64 12.4.2), and the map's own row
   «Hyperliquid's large accounts» already records that it is «not in sight at this pace».
2. **The rule's answer moves with its date.** TZ-64's reading at T0 = 16.10 found **one** copyable account; the
   service's selection at T0 = 17.10 found **two**. The same rule applied at a later T0 reads a 52-week record and a
   91-day copyability window that have moved, so it can admit an account the first pass could not.

So the rule is re-applied — **its every constant unchanged, only T0 moves** — every four weeks while picks are short of
three and four weeks of the window remain, and an account it admits joins the running test as a pick from that moment.
Nothing else of TZ-64 or TZ-65 moves: thresholds, delays, sizing, the stop, the booking, the null and `decide()`.

**Other platforms are not added** [Architect's decision]. The map's row records that Binance offers no documented
per-trader route; a copy-trading profile on any exchange shows the record its trader chose to publish, and the
twelve-month rule needs every fill of an account, which Hyperliquid alone serves.

---

## 2. Text this TZ obeys

- Contract §7 item 15: «An implementation session never enables, starts or leaves running a persistent unit, timer or
  service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its report
  proves none is left behind.»
- Contract §7 item 2: «**Never edit a bench to make it pass.**» — section W11's expected alert texts change in §9
  **because the product's text changes by this TZ**; that edit is named here and is the only expectation §9 rewrites.
  Every other existing check of `vps/selftest.py` stands byte for byte.
- Contract §8: «The paper-test recorder pushes `analyst/paper/**` on the same path under the same rules (since v30); it
  adds only files `main` does not hold». The rescan record `analyst/paper/rescan/<date>.json` is such a file.
- Map inv. 38 (1): «**A second implementation of any rule, threshold or formula is banned in any language and any
  file.**» — the rescan is `select()` itself, called with parameters (§3 B2).
- Map inv. 49: «**An admissibility band is derived from a null computed in the same run.**» — unchanged (§3 B5).
- Map inv. 70: «**A transport failure is NOT an absence of data.**» — a leverage read that fails prints «н/д» and
  changes no record (§3 A2).
- Map inv. 22: «**A check that passes with no data is forbidden.**»

---

## 3. The rule as this TZ amends it — registered

Each item names what derived it. §9 implements this section and nothing else.

### A. The alerts (amends TZ-64 12.5.2)

**A1. The texts, character for character** (the code holds them as `\u` escapes, §9):

```
📋 Бумажный тест · {hhmm} Тбилиси · {num} 🐋• {addr} открыл {side} {dot} {symbol} по {px} · плечо {lev} · стоп {dist}% → {stop} · объём {notional} USDT при риске {risk}% капитала.
📋 Бумажный тест · {hhmm} Тбилиси · {num} 🐋• {addr} открыл {side} {dot} {symbol} по {px} · плечо {lev} · стоп и объём не рассчитаны: нет дневных свечей Binance.
📋 Бумажный тест · {hhmm} Тбилиси · {num} 🐋• {addr} {mark} Закрыл {side} {symbol} по {px} · в позиции 🕚 {held}.
```

`{num}` is the rank as a keycap digit, `1` + U+FE0F + U+20E3 for 1 … 9, else `#` and the rank; 🐋 is U+1F40B followed
by `•` U+2022 with no space; `{dot}` is 🟢 U+1F7E2 for LONG and 🔴 U+1F534 for SHORT; 🕚 is U+1F55A; every other field
is TZ-64 12.5.2's. *Derived from the owner's three messages to the bot of 29.10.2026, measured on his screenshot: the gap
after the whale is 11 px against 17 px for a word space, so no space; the clock is the eleven o'clock face; the close
carries no dot; every text ends in a full stop.* [Architect's decision: the keycap — his «1» is a Telegram Premium custom
emoji, which a bot may send only through a `custom_emoji` entity, its owner's Premium and an emoji id (Bot API 9.4);
discarded: changing the bot's delivery path, which carries every message, for one glyph.]

**A2. `{lev}`** is `{L}x (весь счёт {E}x)`: `{L}` the `leverage.value` of the account's position on the fill's coin
in Hyperliquid's `clearinghouseState`, `{E}` that answer's `marginSummary.totalNtlPos` over
`marginSummary.accountValue` to one decimal; «н/д» when the coin holds no position or the read or its shape fails. The
read is made once per pick open that is alerted, through the service's limiter at `INFO_WEIGHT`; **it never raises**,
so it can neither fail a poll nor change a record. *Read from the Architect's session on 29.10.2026: pick 1 holds LIT at
an isolated setting of 4 and BTC at a cross setting of 40, while its account carries 4 079 239 USD of positions on
1 356 478 USD of value — 3.0.* [Architect's decision: both numbers — on cross margin the setting is a margin parameter,
not exposure, and «40x» alone would tell the owner the account trades at 40; discarded: the setting alone.]

**A3. `{mark}`** is ❎ U+274E when `side · (px_close / px_open − 1) > 2 · FEE_TAKER`, the frozen rule's taker fee, and
❌ U+274C otherwise. [Architect's decision: the COPY's move — the copy enters at the account's first price and holds
one size to its close; discarded: the account's own realised PnL, which includes averaging the copy never does.] The
book stays the record of every result; the mark is the alert's.

### B. The rescan (amends TZ-64 12.1, 12.4)

**B1. When:** first at `follow_from` + 14 days, then 28 days after the previous rescan was adopted, and only while the
picks number fewer than `TOP_K` (3) and `window_end` is at least 28 days away. For the running test: first due
31.10.2026 12:51 UTC — at the service's first start after the merge — and none may start after 19.12.2026 12:51 UTC, so
at most two run. *[Architect's decision: two weeks shift the 52-week record by two of its weeks; a pick joining with
under four weeks left adds a week's handful of episodes.]*

**B2. What:** `select()` itself on its own work file `rescan-<n>-work.jsonl`: T0 the day it starts, the pool, every
measure and the twelve-month rule exactly as 12.1.1–12.1.6; **the selection's frozen Binance list**, so the
copyability it measures is the following's own; the walk down the ranking skips every account already followed, pick
or null; it takes `TOP_K` minus the picks; no null is drawn. Resumable from its work file with the same T0 (12.1.9).

**B3. How it runs:** in a daemon thread of the service, with its own limiter at 300 per minute while the service's holds
300 — together TZ-64 12.2.1's 600 — and 600 again once it ends. A rescan that ends with no result, `retrying()`'s
`sys.exit` included, resumes from its work file an hour later under the same number. *Memory, one process under
`MemoryMax=128M`: TZ-64's probe peaked at 37 880 KiB through the same leaderboard pass, and TZ-65's own figures put the
booking's peak at 35–39 MiB — an upper bound of 77 MiB, the two figures counting the interpreter twice.*

**B4. Adoption:** each account the rescan picks joins as a pick numbered after the last, followed from the adoption
instant `join_ms`; a position it holds at that instant has no episode until flat (12.2.2, unchanged). The record
`analyst/paper/rescan/<T0's date>.json` is written once. The owner is told, once per rescan:

```
Бумажный тест: новый кит {num} 🐋• {addr} — прошёл то же правило отбора на {date}, оповещения до {end}.
Бумажный тест · поиск китов {date}: правило 12 месяцев прошли {r12} из {eligible} счетов, новых копируемых нет.
```

`{date}` the rescan's T0 and `{end}` `window_end`, both `DD.MM.YYYY` in Tbilisi.

**B5. The verdict:** each pick's `R` is over its own span — from `follow_from` for the selection's, from `join_ms` for
a rescan's. A null account's value is **the mean, over the picks, of its `R` over each pick's span** — its episodes
with `t_open` at or after that span's start. With one span this is its `R` itself, so the verdict of a test no rescan
added to is TZ-64 12.4.1 exactly. Readable counts the booked episodes of every pick. `verdict.json` gains
`joined` per pick; `decide()` does not change. *Derived: if picks are no better than random eligible accounts, a pick's
`R` and a null account's `R` over the same span have one expectation, so the two sides of every comparison average the
same spans. Discarded [Architect's decision]: counting a late pick against the null's whole window — its shorter span
pulls its result toward zero, and a losing late pick could then turn a failing TOP positive.*

---

## 4. Scope

### Files to Create
None in the repository but the report.

### Files to Modify
- `vps/paper.py` — §9.
- `vps/selftest.py` — §9: W11's texts as A1, new checks in W11 and W14, new parts W16 and W17.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
Transient units started from the branch's clone for stage C's selftest and probe, each stopped before the report. No
unit, timer or file under `/etc` or `/var/lib/cryptopaper` is created, changed or restarted: **the running paper test is
not touched**, and its first rescan starts only when the deployer installs the merge.

### Not touched
`index.html`, `main.py`, `vps/bot.py`, every unit and the manifest, `analyst/**`, the map, the contracts.

---

## 5. Stages

### Stage A — readings, no writes
- **A0.** Contract §4a steps 1–6; the gate of §0, every anchor cut from the map's own table.
- **A1.** The four added files of §0 at their lines and MD5; any difference stops the TZ, BLOCKED, naming the file.
- **A2.** On the VPS, the baseline from `main`: `python3 vps/selftest.py` prints `selftest: sections 27 checks 560
  failed 0 empty 0` and `section W: checks 102 failed 0`. *Measured by the Architect on `main` at `92ebce3`, 29.10.2026.*
  A different baseline is recorded per section and the TZ goes on: stage C compares against what A2 read.

### Stage B — the code, on the branch
- **B1.** Branch `claude/tz-75-paper-alerts-rescan` from `origin/main`. Extract §9's patch with the one command

  ```sh
  awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-75-paper-alerts-rescan.md > /tmp/tz75.patch
  ```

  and record its lines and MD5 — 614 and `acb0d618ace0be21278f9a782ee2f5eb` as written; an upload that strips trailing
  blanks changes the hash and not the result, which B2 decides.
- **B2.** `git apply /tmp/tz75.patch`. **Required:** `vps/paper.py` 1413 lines, MD5 `a709359a86f630c464fd92ee93f6ae2c`;
  `vps/selftest.py` 2627 lines, MD5 `76e814ccbe18551a8f47d6f7eae09669`. Any other result is BLOCKED: the patch did not
  arrive as written, and no hand edit replaces it.

### Stage C — validation, on the VPS, from the branch
§6, in full.

### Stage D — commit, push, pull request, report
One implementation commit with §7's message; push; a pull request to `main` titled
`TZ-75: paper alerts — whale number, leverage, coloured close; four-weekly rescan`, its body naming this TZ, or the
§8 fallback. Then the report.

---

## 6. Validation

| # | Check | Required |
|---|---|---|
| V1 | `python3 -m py_compile vps/paper.py vps/selftest.py` | exit 0 |
| V2 | B2's two files | the lines and MD5s of B2 |
| V3 | `python3 vps/selftest.py` on the branch, on the VPS | `selftest: sections 27 checks 592 failed 0 empty 0`; `section W: checks 134 failed 0`; **every other section's count equal to A2's**. *Measured by the Architect on the patched tree, 29.10.2026: W grows by exactly 32 — 9 in W11, 3 in W14, 17 in W16, 3 in W17 — and the 458 checks outside W do not move.* If A2 read another baseline, the requirement is A2's total + 32 and A2's W + 32 |
| V4 | Negative control: in the working tree replace `> 2 * rule["fee_taker"]` with `> 0` in `vps/paper.py`; run the selftest; restore with `git checkout -- vps/paper.py` | exit non-zero with exactly one `FAIL` line, `FAIL section W: a move inside the fee both ways is a loss: red cross`; then `git status --porcelain` prints nothing. *Measured by the Architect, 29.10.2026.* |
| V5 | `paper.py --probe` from the branch's clone as a transient unit, as TZ-64 C2 ran it | exit 0; eight step lines — `paper: probe` leaderboard, portfolio, exchange, **leverage**, fills, klines_1m, klines_1d, funding — none `failed (…)`, the new one reading `leverage positions=<n>`; then the `peak_rss_kib` line, reported |
| V6 | `git diff --name-only origin/main...HEAD` | exactly `vps/paper.py` and `vps/selftest.py` |
| V7 | `crypto-paper.service` before and after the session: `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service` | equal — the live test was not restarted; and no transient unit of the session is left (`systemctl list-units --all 'run-*'`) |
| V8 | `bench.yml` | `index.html` and `main.py` are untouched, so the standing checks do not apply; report which workflows ran on the branch, from the runner, and that `vps/**` is outside the hosted gate by its own comment |

**No regression:** every existing check outside W11's four rewritten texts is unchanged and green (V3), and the
verdict of a test no rescan added to is TZ-64's (W17's first check).

---

## 7. Commit Message

Implementation: `TZ-75: vps — paper alerts carry the whale's number, its leverage and a coloured close; the selection rule re-applied every four weeks until three whales are followed`

Report: `TZ-75: report — paper alerts and the four-weekly rescan`

---

## 8. The report

Contract §10 in full. Beside it: B1's command and the patch's lines and MD5; B2's lines and MD5s; A2's and V3's per-section
counts side by side; V4's FAIL line verbatim; V5's nine probe lines and the transient unit's command; V7's two readings.
The map's row «Hyperliquid's large accounts» is the Architect's to update after the audit, not this TZ's.

---

## 9. The patch

Against `main` at `92ebce3`: `vps/paper.py` 1281 → 1413 lines, `vps/selftest.py` 2430 → 2627.

```diff
diff --git a/vps/paper.py b/vps/paper.py
index d051633..2a98e2e 100644
--- a/vps/paper.py
+++ b/vps/paper.py
@@ -27,6 +27,7 @@ import resource
 import shutil
 import statistics
 import sys
+import threading
 import time
 import urllib.error
 import urllib.request
@@ -63,6 +64,9 @@ SIGMA_DAYS = 30
 EPISODES_MIN = 30
 NULL_MIN = 10
 ALERT_MAX_AGE_S = 600
+RESCAN_FIRST_DAYS = 14        # TZ-75 B: the rule re-applied two weeks after follow_from,
+RESCAN_EVERY_DAYS = 28        # then every four weeks while picks are short of TOP_K
+RESCAN_MIN_LEFT_DAYS = 28     # and only while at least four weeks of the window remain
 PROBE_ACCOUNT = "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1"   # the reading's first account
 
 # --- Operation.
@@ -75,7 +79,8 @@ PICK_POLL_S = 30
 NULL_POLL_S = 600
 DAY_SETTLE_S = 600            # a day is written once every account was polled this long after it ended
 ABSENT_AFTER_DAYS = 3         # a 404 for a file dated further back is an absence, nearer is unpublished
-WORK_EVERY_S = 3600           # booking, funding and the verdict are attempted hourly
+WORK_EVERY_S = 3600           # booking, funding and the verdict are attempted hourly; a failed rescan resumes as often
+RESCAN_WEIGHT_PER_MIN = 300   # a rescan's share of WEIGHT_PER_MIN; the service holds the rest while one runs
 PUBLISH_EVERY_S = 300
 TRANSPORT_MAX = 30            # consecutive transport failures on one selection step
 TRANSPORT_WAIT_S = 60
@@ -88,21 +93,15 @@ RECORD_DIR = "analyst/paper"
 DEPLOYED_TREE = os.path.join(common.STATE_DIR, "deployed-vps-tree")
 REPO = os.path.dirname(common.VPS_DIR)
 
-# --- TZ-64 section 12.1, character for character.
-P_OPEN = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
-          "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
-          "\u043e\u0442\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0441\u0442\u043e\u043f "
-          "{dist}% \u2192 {stop} \u00b7 \u043e\u0431\u044a\u0451\u043c {notional} USDT \u043f\u0440\u0438 "
-          "\u0440\u0438\u0441\u043a\u0435 {risk}% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430")
-P_OPEN_BARE = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
-               "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
-               "\u043e\u0442\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0441\u0442\u043e\u043f "
-               "\u0438 \u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: "
-               "\u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance")
-P_CLOSE = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
-           "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
-           "\u0437\u0430\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0432 "
-           "\u043f\u043e\u0437\u0438\u0446\u0438\u0438 {held}")
+# --- TZ-64 section 12.5.2 as TZ-75 A1 restyles it, character for character.
+P_HEAD = "\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 {num} \U0001f40b\u2022 {addr} "
+P_OPEN = P_HEAD + "\u043e\u0442\u043a\u0440\u044b\u043b {side} {dot} {symbol} \u043f\u043e {px} \u00b7 \u043f\u043b\u0435\u0447\u043e {lev} \u00b7 \u0441\u0442\u043e\u043f {dist}% \u2192 {stop} \u00b7 \u043e\u0431\u044a\u0451\u043c {notional} USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a\u0435 {risk}% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430."
+P_OPEN_BARE = P_HEAD + "\u043e\u0442\u043a\u0440\u044b\u043b {side} {dot} {symbol} \u043f\u043e {px} \u00b7 \u043f\u043b\u0435\u0447\u043e {lev} \u00b7 \u0441\u0442\u043e\u043f \u0438 \u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: \u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance."
+P_CLOSE = P_HEAD + "{mark} \u0417\u0430\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \U0001f55a {held}."
+P_LEV = "{lev}x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 {acct}x)"
+P_LEV_NONE = "\u043d/\u0434"
+SIDE_DOT = {1: "\U0001f7e2", -1: "\U0001f534"}
+MARK_GAIN, MARK_LOSS = "\u274e", "\u274c"
 N_START = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440"
            "\u043e\u0432\u0430\u043d\u0438\u044f \u043d\u0430\u0447\u0430\u0442: \u043e\u0442\u043e\u0431\u0440\u0430"
            "\u043d\u043e \u0441\u0447\u0435\u0442\u043e\u0432 Hyperliquid \u2014 {k}, \u043e\u043a\u043d\u043e 13 "
@@ -121,6 +120,8 @@ N_VERDICT = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u044
              "\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0438\u0442\u043e\u0433 \u0437\u0430\u043f\u0438\u0441"
              "\u0430\u043d \u0438 \u0436\u0434\u0451\u0442 \u0440\u0430\u0437\u0431\u043e\u0440\u0430 \u0410\u0440"
              "\u0445\u0438\u0442\u0435\u043a\u0442\u043e\u0440\u0430.")
+N_ADDED = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442: \u043d\u043e\u0432\u044b\u0439 \u043a\u0438\u0442 {num} \U0001f40b\u2022 {addr} \u2014 \u043f\u0440\u043e\u0448\u0451\u043b \u0442\u043e \u0436\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u0431\u043e\u0440\u0430 \u043d\u0430 {date}, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u0434\u043e {end}."
+N_RESCAN_NONE = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 \u043f\u043e\u0438\u0441\u043a \u043a\u0438\u0442\u043e\u0432 {date}: \u043f\u0440\u0430\u0432\u0438\u043b\u043e 12 \u043c\u0435\u0441\u044f\u0446\u0435\u0432 \u043f\u0440\u043e\u0448\u043b\u0438 {r12} \u0438\u0437 {eligible} \u0441\u0447\u0435\u0442\u043e\u0432, \u043d\u043e\u0432\u044b\u0445 \u043a\u043e\u043f\u0438\u0440\u0443\u0435\u043c\u044b\u0445 \u043d\u0435\u0442."
 MINUTES = "\u043c\u0438\u043d"
 HOURS = "\u0447"
 
@@ -820,10 +821,13 @@ def retrying(call, *args, give_up=False):
     sys.exit(4)
 
 
-def select(state_dir, rule, limiter, clock=now_ms):
+def select(state_dir, rule, limiter, clock=now_ms, work="selection-work.jsonl", symbols=None, exclude=(), k=TOP_K,
+           draw_null=True):
     """The selection, resumable: T0, the pool, every pool account's measures, the Binance list, the
-    picks walked down the ranking and the null walked down its order, each step kept in the work file."""
-    path = os.path.join(state_dir, "selection-work.jsonl")
+    picks walked down the ranking and the null walked down its order, each step kept in the work file.
+    A rescan (TZ-75 B) runs this same function on its own work file with the selection's frozen Binance
+    list, the accounts already followed excluded from the walk, k the picks still missing and no null."""
+    path = os.path.join(state_dir, work)
     work = read_work(path)
     head = next((w for w in work if "t0_ms" in w), None)
     if head is None:
@@ -849,7 +853,7 @@ def select(state_dir, rule, limiter, clock=now_ms):
         append_work(path, {"a": addr, "m": m})
         if len(measured) % 500 == 0:
             common.log("paper: measured %d of %d" % (len(measured), len(pool["pool"])))
-    symbols = next((w["symbols"] for w in work if "symbols" in w), None)
+    symbols = symbols or next((w["symbols"] for w in work if "symbols" in w), None)
     if symbols is None:
         symbols = sorted(p["symbol"] for p in exchange.perpetuals(retrying(fetch_exchange)))
         append_work(path, {"symbols": symbols})
@@ -871,12 +875,13 @@ def select(state_dir, rule, limiter, clock=now_ms):
     ranked = sorted((a for a, m in measured.items() if m.get("r12")), key=lambda a: (-measured[a]["sharpe"], a))
     picks, rejected = [], []
     for addr in ranked:
-        if len(picks) == TOP_K:
+        if len(picks) == k:
             break
-        (picks if check(addr)["copyable"] else rejected).append(addr)
+        if addr not in exclude:
+            (picks if check(addr)["copyable"] else rejected).append(addr)
     eligible = sorted(a for a, m in measured.items() if m.get("eligible"))
     null = []
-    for addr in null_order(t0, [a for a in eligible if a not in picks]):
+    for addr in null_order(t0, [a for a in eligible if a not in picks]) if draw_null else ():
         if len(null) == NULL_M:
             break
         if check(addr)["copyable"]:
@@ -890,7 +895,7 @@ def select(state_dir, rule, limiter, clock=now_ms):
                        "unreadable": sum(1 for m in measured.values() if m.get("unreadable")),
                        "eligible": len(eligible), "r12": len(ranked), "checked": len(checked)},
             "picks": [dict(entry(a), rank=i + 1) for i, a in enumerate(picks)],
-            "rejected": [entry(a) for a in rejected], "null": [entry(a) for a in null],
+            "rejected": [entry(a) for a in rejected], "null": [entry(a) for a in null], "ranked": ranked,
             "eligible": eligible, "symbols": symbols, "fp": fingerprint()}
 
 
@@ -930,9 +935,35 @@ def sigma_for(inputs, sym, t_open):
     return daily_sigma([inputs.close_on(sym, add_days(first, -k)) for k in range(SIGMA_DAYS + 2, 1, -1)])
 
 
-def alert_open(ep, rank, rule, sigma):
-    base = {"hhmm": hhmm(ep["t_open"]), "rank": rank, "addr": addr_short(ep["a"]), "side": side_word(ep["side"]),
-            "symbol": ep["symbol"], "px": ep["px_open"]}
+def number(rank):
+    """The whale's number: a keycap digit for 1 ... 9, else #rank."""
+    return ("%d\ufe0f\u20e3" % rank) if 1 <= rank <= 9 else ("#%d" % rank)
+
+
+def read_leverage(addr, coin, limiter):
+    """(the position's leverage setting, the account's notional over its value) from clearinghouseState,
+    or None: the coin holds no position, or any read or shape failure. Never raises."""
+    try:
+        doc = info({"type": "clearinghouseState", "user": addr}, limiter)
+        pos = next(p["position"] for p in doc["assetPositions"] if p["position"]["coin"] == coin)
+        lev = int(pos["leverage"]["value"])
+        value = float(doc["marginSummary"]["accountValue"])
+        ntl = float(doc["marginSummary"]["totalNtlPos"])
+        if lev < 1 or not value > 0 or not math.isfinite(ntl):
+            return None
+        return lev, ntl / value
+    except (StopIteration, Transport, KeyError, TypeError, ValueError, ArithmeticError, AttributeError):
+        return None
+
+
+def lev_text(lev):
+    return P_LEV_NONE if lev is None else P_LEV.format(lev=lev[0], acct="%.1f" % lev[1])
+
+
+def alert_open(ep, rank, rule, sigma, lev=None):
+    base = {"hhmm": hhmm(ep["t_open"]), "num": number(rank), "addr": addr_short(ep["a"]),
+            "side": side_word(ep["side"]), "dot": SIDE_DOT[ep["side"]], "symbol": ep["symbol"], "px": ep["px_open"],
+            "lev": lev_text(lev)}
     if sigma is None or not sigma > 0:
         return P_OPEN_BARE.format(**base)
     dist = rule["inv_floor_sd"] * sigma
@@ -942,11 +973,76 @@ def alert_open(ep, rank, rule, sigma):
                          notional="%d" % round(notional), risk=("%g" % rule["risk_pct"]), **base)
 
 
-def alert_close(ep, rank):
-    return P_CLOSE.format(hhmm=hhmm(ep["t_close"]), rank=rank, addr=addr_short(ep["a"]), side=side_word(ep["side"]),
+def gained(ep, rule):
+    """The copy's move from the account's opening price to its closing price beats the taker fee both ways."""
+    return ep["side"] * (float(ep["px_close"]) / float(ep["px_open"]) - 1) > 2 * rule["fee_taker"]
+
+
+def alert_close(ep, rank, rule):
+    return P_CLOSE.format(hhmm=hhmm(ep["t_close"]), num=number(rank), addr=addr_short(ep["a"]),
+                          mark=MARK_GAIN if gained(ep, rule) else MARK_LOSS, side=side_word(ep["side"]),
                           symbol=ep["symbol"], px=ep["px_close"], held=held_text(ep["t_close"] - ep["t_open"]))
 
 
+def pick_joins(state, sel):
+    """Every pick, the selection's in rank order then the rescans' by rank, and the instant each is followed
+    from: follow_from for the selection's, its own join for a rescan's."""
+    own = [p["address"] for p in sel["picks"]]
+    added = sorted((a for a, x in state["accounts"].items() if x["role"] == "pick" and a not in own),
+                   key=lambda a: state["accounts"][a]["rank"])
+    return own + added, {a: state["accounts"].get(a, {}).get("join_ms", sel["follow_from_ms"]) for a in own + added}
+
+
+def rescan_state(state, sel):
+    """The rescan's own entry of the state, added to a state written before TZ-75 with its first rescan due
+    RESCAN_FIRST_DAYS after follow_from."""
+    return state.setdefault("rescan", {"n": 0, "due_ms": sel["follow_from_ms"] + RESCAN_FIRST_DAYS * DAY_MS,
+                                       "running": False})
+
+
+def rescan_due(state, sel, now):
+    """A rescan starts, or resumes, when it is due, picks are short of TOP_K and four weeks of the window remain."""
+    rs = state["rescan"]
+    return (rs["due_ms"] is not None and now >= rs["due_ms"] and len(pick_joins(state, sel)[0]) < TOP_K
+            and sel["window_end_ms"] - now >= RESCAN_MIN_LEFT_DAYS * DAY_MS)
+
+
+def rescan_run(box, state_dir, rule, sel, exclude, k, n):
+    """The thread: select() on rescan n's own work file and limiter; its result, or the name of what ended it."""
+    try:
+        box["result"] = select(state_dir, rule, Limiter(RESCAN_WEIGHT_PER_MIN), work="rescan-%d-work.jsonl" % n,
+                               symbols=sel["symbols"], exclude=exclude, k=k, draw_null=False)
+    except BaseException as exc:   # noqa: B036 -- retrying() ends a step it cannot do without by sys.exit
+        box["error"] = exc.__class__.__name__
+
+
+def tbilisi_date(ms):
+    return datetime.fromtimestamp(ms / 1000, tz=announce.TBILISI).strftime("%d.%m.%Y")
+
+
+def adopt(state, state_dir, sel, res, n, now):
+    """Rescan n's picks join as picks from now, numbered after the last; the record, written once; a notice per
+    whale added, or one notice that none was."""
+    have = len(pick_joins(state, sel)[0])
+    added = []
+    for i, row in enumerate(res["picks"]):
+        rank = have + i + 1
+        state["accounts"][row["address"]] = {"role": "pick", "rank": rank, "join_ms": now, "last_ms": now,
+                                             "last_tids": [], "polled_ms": 0, "due_ms": 0, "coins": {}, "fills": {},
+                                             "lost": {}, "failing": False}
+        added.append(dict(row, rank=rank))
+    doc = {"v": 1, "k": "paper-rescan", "n": n, "t0": res["t0"], "t0_ms": res["t0_ms"], "joined": iso(now),
+           "joined_ms": now, "counts": res["counts"], "ranked": res["ranked"], "added": added,
+           "rejected": res["rejected"], "fp": fingerprint()}
+    write_record(state, state_dir, "rescan/%s.json" % utc_date(res["t0_ms"]), doc=doc)
+    for row in added:
+        common.write_outbox("notice", N_ADDED.format(num=number(row["rank"]), addr=addr_short(row["address"]),
+                                                     date=tbilisi_date(res["t0_ms"]), end=tbilisi_date(sel["window_end_ms"])))
+    if not added:
+        common.write_outbox("notice", N_RESCAN_NONE.format(date=tbilisi_date(res["t0_ms"]), r12=res["counts"]["r12"],
+                                                           eligible=res["counts"]["eligible"]))
+
+
 def starts(sel):
     """The test follows only when it can be read: at least one pick and NULL_MIN null accounts."""
     return len(sel["picks"]) >= 1 and len(sel["null"]) >= NULL_MIN
@@ -969,12 +1065,12 @@ def poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for):
     The account's state changes only when the whole poll succeeded."""
     fills = fills_since(addr, acct["last_ms"], limiter)
     work = json.loads(json.dumps(acct))
-    _apply(addr, work, fills, sel, symbols, now, rule, inputs_for)
+    _apply(addr, work, fills, sel, symbols, now, rule, inputs_for, lambda coin: read_leverage(addr, coin, limiter))
     acct.clear()
     acct.update(work)
 
 
-def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for):
+def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for, leverage_for=lambda coin: None):
     window_end = sel["window_end_ms"]
     for f in fills:
         t = int(f["time"])
@@ -1000,9 +1096,9 @@ def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for):
                         sigma = sigma_for(inputs_for(), sym, t)
                     except (NotReady, Absent, Transport, ValueError, ZeroDivisionError):
                         sigma = None
-                    common.write_outbox("alert", alert_open(ep, acct["rank"], rule, sigma))
+                    common.write_outbox("alert", alert_open(ep, acct["rank"], rule, sigma, leverage_for(f["coin"])))
                 else:
-                    common.write_outbox("alert", alert_close(ep, acct["rank"]))
+                    common.write_outbox("alert", alert_close(ep, acct["rank"], rule))
     if fills:
         acct["last_ms"] = max(acct["last_ms"], max(int(f["time"]) for f in fills))
         acct["last_tids"] = [f["tid"] for f in fills if int(f["time"]) == acct["last_ms"]]
@@ -1101,9 +1197,11 @@ def produce_verdict(state, state_dir, sel, rule):
         return False
     root = os.path.join(state_dir, "records", RECORD_DIR)
     days = days_between(utc_date(sel["follow_from_ms"]), last)
-    picks = [p["address"] for p in sel["picks"]]
+    picks, joins = pick_joins(state, sel)
     null = [p["address"] for p in sel["null"]]
-    results = {a: {d: {"src": 0.0, "stop": 0.0} for d in DELAYS_S} for a in picks + null}
+    spans = sorted(set(joins.values()))
+    results = {a: {d: {"src": 0.0, "stop": 0.0} for d in DELAYS_S} for a in picks}
+    spanned = {a: {j: {d: {"src": 0.0, "stop": 0.0} for d in DELAYS_S} for j in spans} for a in null}
     booked = {d: {"pick": 0, "null": 0} for d in DELAYS_S}
     lags, unbookable, absent = [], 0, 0
     for day in days:
@@ -1127,10 +1225,19 @@ def produce_verdict(state, state_dir, sel, rule):
                     continue
                 booked[d][role] += 1
                 for v in ("src", "stop"):
-                    results[f["a"]][d][v] += (cell[v]["gross"] - cell[v]["fee"] - f["d"][str(d)][v]) / rule["capital_usdt"]
+                    net = (cell[v]["gross"] - cell[v]["fee"] - f["d"][str(d)][v]) / rule["capital_usdt"]
+                    if role == "pick":
+                        results[f["a"]][d][v] += net
+                    else:
+                        for j in spans:
+                            if f["t_open"] >= j:
+                                spanned[f["a"]][j][d][v] += net
+    for a in null:   # a null account's result over every pick's own span, averaged over the picks (TZ-75 B5)
+        results[a] = spanned[a][spans[0]] if len(spans) == 1 else {d: {v: statistics.fmean(
+            spanned[a][joins[p]][d][v] for p in picks) for v in ("src", "stop")} for d in DELAYS_S}
     verdict = decide(picks, null, results, booked[1800]["pick"])
     doc = {"v": 1, "k": "paper-verdict", "follow_from": sel["follow_from"], "window_end": sel["window_end"],
-           "picks": picks, "null": null, "booked": {str(d): booked[d] for d in DELAYS_S}, "unbookable": unbookable,
+           "picks": picks, "joined": {a: iso(joins[a]) for a in picks}, "null": null, "booked": {str(d): booked[d] for d in DELAYS_S}, "unbookable": unbookable,
            "funding_absent": absent, "lag_s": {"n": len(lags), "p50": nearest_rank(lags, 0.5),
                                                  "p95": nearest_rank(lags, 0.95)}, "fp": fingerprint()}
     doc.update(verdict)
@@ -1177,6 +1284,8 @@ def service(state_dir, tree):
         common.log("paper: selection done picks=%d null=%d" % (len(sel["picks"]), len(sel["null"])))
     rule = sel["rule"]    # frozen at the selection: a later change of owner.json moves nothing here
     state = load_state(state_path, sel)
+    rescan_state(state, sel)
+    box, thread = {}, None
     written = None
     symbols = set(sel["symbols"])
     inputs_box = {}
@@ -1204,6 +1313,27 @@ def service(state_dir, tree):
                         common.log("paper: poll %s failed (%s)" % (addr_short(addr), exc.__class__.__name__))
                     acct["failing"] = True
             gather_closed(state)
+            rs = state["rescan"]
+            if thread is None and rescan_due(state, sel, now):
+                picks = pick_joins(state, sel)[0]
+                if not rs["running"]:
+                    rs.update(n=rs["n"] + 1, running=True)
+                box = {}
+                thread = threading.Thread(target=rescan_run, daemon=True, args=(
+                    box, state_dir, rule, sel, set(picks) | {p["address"] for p in sel["null"]}, TOP_K - len(picks),
+                    rs["n"]))
+                limiter.per_min = WEIGHT_PER_MIN - RESCAN_WEIGHT_PER_MIN
+                thread.start()
+                common.log("paper: rescan %d started" % rs["n"])
+            elif thread is not None and not thread.is_alive():
+                thread, limiter.per_min = None, WEIGHT_PER_MIN
+                if "result" in box:
+                    adopt(state, state_dir, sel, box["result"], rs["n"], now)
+                    rs.update(running=False, due_ms=now + RESCAN_EVERY_DAYS * DAY_MS)
+                    common.log("paper: rescan %d adopted picks=%d" % (rs["n"], len(box["result"]["picks"])))
+                else:
+                    rs["due_ms"] = now + WORK_EVERY_S * 1000
+                    common.log("paper: rescan %d ended (%s), resumes later" % (rs["n"], box.get("error", "-")))
             if now >= sel["window_end_ms"] and all(a["polled_ms"] >= sel["window_end_ms"] + DAY_SETTLE_S * 1000
                                                     for a in state["accounts"].values()):
                 cut_open(state, sel)
@@ -1249,6 +1379,8 @@ def probe():
         ("portfolio", lambda: " ".join("%s=%s" % (k, v) for k, v in sorted(
             metrics(info({"type": "portfolio", "user": PROBE_ACCOUNT}, limiter), t0).items()))),
         ("exchange", lambda: "perpetuals=%d" % len(exchange.perpetuals(fetch_exchange()))),
+        ("leverage", lambda: "positions=%d" % len(info({"type": "clearinghouseState", "user": PROBE_ACCOUNT},
+                                                         limiter)["assetPositions"])),
         ("fills", lambda: (lambda fl: "fills=%d first=%s" % (len(fl), iso(int(fl[0]["time"])) if fl else "-"))(
             fills_since(PROBE_ACCOUNT, t0 - WINDOW_DAYS * DAY_MS, limiter, t0 - 1))),
         ("klines_1m", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1m/BTCUSDT-1m-%s.zip" % yesterday))),
diff --git a/vps/selftest.py b/vps/selftest.py
index 86fdc68..97d1365 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1564,26 +1564,49 @@ def section_w(s):
         paper.TRANSPORT_WAIT_S = saved_wait
     s.check("nearest_rank: median 3, p95 5 of 1..5",
             paper.nearest_rank([5, 1, 3, 2, 4], 0.5) == 3 and paper.nearest_rank([5, 1, 3, 2, 4], 0.95) == 5)
-    # W11. the alert texts
+    # W11. the alert texts (TZ-75 A)
     rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
     t_open = int(datetime(2026, 10, 16, 10, 5, tzinfo=timezone.utc).timestamp() * 1000)
     ep = {"a": "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1", "coin": "HYPE", "symbol": "HYPEUSDT", "side": 1,
           "t_open": t_open, "px_open": "80.021"}
-    head = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 14:05 "
-            "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #1 0xf97a\u2026ddd1 ")
-    s.check("the open alert, character for character", paper.alert_open(ep, 1, rule, 0.02) == head + (
-        "\u043e\u0442\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 80.021 \u00b7 \u0441\u0442\u043e\u043f 4.0% "
-        "\u2192 76.820 \u00b7 \u043e\u0431\u044a\u0451\u043c 1250 USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a"
-        "\u0435 0.5% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430"))
-    s.check("the open alert without a sigma", paper.alert_open(ep, 1, rule, None) == head + (
-        "\u043e\u0442\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 80.021 \u00b7 \u0441\u0442\u043e\u043f \u0438 "
-        "\u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: "
-        "\u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance"))
+    head = "\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 14:05 \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 "
+    whale = "1\ufe0f\u20e3 \U0001f40b\u2022 0xf97a\u2026ddd1 "
+    s.check("the open alert, character for character", paper.alert_open(ep, 1, rule, 0.02, (20, 3.04)) == head + whale + (
+        "\u043e\u0442\u043a\u0440\u044b\u043b LONG \U0001f7e2 HYPEUSDT \u043f\u043e 80.021 \u00b7 \u043f\u043b\u0435\u0447\u043e 20x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 3.0x) \u00b7 \u0441\u0442\u043e\u043f 4.0% \u2192 76.820 \u00b7 \u043e\u0431\u044a\u0451\u043c 1250 USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a\u0435 0.5% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430."))
+    s.check("the open alert without a sigma or a leverage", paper.alert_open(ep, 1, rule, None) == head + whale + (
+        "\u043e\u0442\u043a\u0440\u044b\u043b LONG \U0001f7e2 HYPEUSDT \u043f\u043e 80.021 \u00b7 \u043f\u043b\u0435\u0447\u043e \u043d/\u0434 \u00b7 \u0441\u0442\u043e\u043f \u0438 \u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: \u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance."))
+    s.check("the short open: red dot, stop above, whale 2", paper.alert_open(dict(ep, side=-1), 2, rule, 0.02) == head + (
+        "2\ufe0f\u20e3 \U0001f40b\u2022 0xf97a\u2026ddd1 \u043e\u0442\u043a\u0440\u044b\u043b SHORT \U0001f534 HYPEUSDT \u043f\u043e 80.021 \u00b7 \u043f\u043b\u0435\u0447\u043e \u043d/\u0434 \u00b7 \u0441\u0442\u043e\u043f 4.0% \u2192 83.222 \u00b7 \u043e\u0431\u044a\u0451\u043c 1250 USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a\u0435 0.5% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430."))
     closed = dict(ep, t_close=t_open + (6 * 60 + 12) * 60000, px_close="82.10")
-    s.check("the close alert after 6 h 12 min", paper.alert_close(closed, 1) == head.replace("14:05", "20:17") + (
-        "\u0437\u0430\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 82.10 \u00b7 \u0432 \u043f\u043e\u0437"
-        "\u0438\u0446\u0438\u0438 6.2 \u0447"))
+    s.check("the close alert in gain after 6 h 12 min: green cross", paper.alert_close(closed, 1, rule) == (
+        head.replace("14:05", "20:17") + whale + "\u274e \u0417\u0430\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 82.10 \u00b7 \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \U0001f55a 6.2 \u0447."))
+    s.check("a move inside the fee both ways is a loss: red cross",
+            paper.alert_close(dict(closed, px_close="80.090"), 1, rule) == head.replace("14:05", "20:17") + whale + (
+                "\u274c \u0417\u0430\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 80.090 \u00b7 \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \U0001f55a 6.2 \u0447."))
+    s.check("a short closed lower is a gain: green cross",
+            paper.alert_close(dict(closed, side=-1, px_close="79.90"), 1, rule).endswith("\u274e \u0417\u0430\u043a\u0440\u044b\u043b SHORT HYPEUSDT \u043f\u043e 79.90 \u00b7 \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \U0001f55a 6.2 \u0447."))
     s.check("held 45 min", paper.held_text(45 * 60000) == "45 \u043c\u0438\u043d")
+    s.check("number: keycaps 1 to 9, then #10", paper.number(1) == "1\ufe0f\u20e3" and paper.number(9) == "9\ufe0f\u20e3"
+            and paper.number(10) == "#10")
+    saved_info = paper.info
+    try:
+        doc = {"marginSummary": {"accountValue": "1000000.0", "totalNtlPos": "3000000.0"},
+               "assetPositions": [{"type": "oneWay", "position": {"coin": "LIT", "szi": "10.0",
+                                                                  "leverage": {"type": "isolated", "value": 4}}}]}
+        paper.info = lambda body, limiter: doc if body == {"type": "clearinghouseState", "user": "0xa"} else None
+        s.check("read_leverage: the coin's setting and the account's notional over its value",
+                paper.read_leverage("0xa", "LIT", None) == (4, 3.0))
+        s.check("read_leverage: a coin with no position is None", paper.read_leverage("0xa", "BTC", None) is None)
+        paper.info = lambda body, limiter: {"assetPositions": doc["assetPositions"]}
+        s.check("read_leverage: an answer without marginSummary is None", paper.read_leverage("0xa", "LIT", None) is None)
+
+        def refused(body, limiter):
+            raise paper.Transport("HTTP 429")
+        paper.info = refused
+        s.check("read_leverage: a refused read is None, never raised", paper.read_leverage("0xa", "LIT", None) is None)
+    finally:
+        paper.info = saved_info
+    s.check("lev_text: both numbers, or n/a", paper.lev_text((7, 1.5)) == "7x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 1.5x)" and paper.lev_text(None) == "\u043d/\u0434")
     # W12. the constants cut from index.html
     page = "var INV_FLOOR_SD = 2.0;   // x\nvar FEE_TAKER   = 0.0005;\n"
     s.check("cut_number on a page", common.cut_number(page, "INV_FLOOR_SD") == 2.0
@@ -1625,6 +1648,10 @@ def section_w(s):
     section_w_flow(s)
     # W15. the booking's memory (TZ-65): one symbol's minutes at a time, compact, dropped after the pass
     section_w_memory(s)
+    # W16. the rescan (TZ-75 B): the selection's own function, the schedule, the adoption
+    section_w_rescan(s)
+    # W17. the verdict over each pick's own span (TZ-75 B5)
+    section_w_spans(s)
 
 
 def w_rows(path):
@@ -1668,6 +1695,23 @@ def section_w_flow(s):
         paper.gather_closed(state)
         alerts = sorted(x for x in os.listdir(outbox) if "-alert-" in x)
         s.check("two fresh alerts for the pick, none for the null, none late", len(alerts) == 2)
+        texts = []
+        for name in alerts:
+            with open(os.path.join(outbox, name), encoding="utf-8") as fh:
+                texts.append(json.load(fh)["text"])
+        s.check("the flow's open alert: whale 1, no leverage without a reader", len(texts) == 2
+                and "1\ufe0f\u20e3 \U0001f40b\u2022 " in texts[0] and "\u043f\u043b\u0435\u0447\u043e \u043d/\u0434" in texts[0])
+        s.check("the flow's close at the opening price: red cross", len(texts) == 2 and "\u274c \u0417\u0430\u043a\u0440\u044b\u043b" in texts[1])
+        asked, lone = [], paper.new_state(sel)
+        paper._apply(p, lone["accounts"][p], [w_fill(ff + h, 0, "B", 1, tid=1)], sel, {"BTCUSDT"}, ff + h + 10000,
+                     rule, lambda: inputs, lambda coin: asked.append(coin) or (7, 1.5))
+        fresh = sorted(x for x in os.listdir(outbox) if "-alert-" in x and x not in alerts)
+        with open(os.path.join(outbox, fresh[-1]), encoding="utf-8") as fh:
+            lone_text = json.load(fh)["text"]
+        s.check("_apply asks the reader for the fill's coin and prints its answer",
+                asked == ["BTC"] and "\u043f\u043b\u0435\u0447\u043e 7x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 1.5x)" in lone_text)
+        for name in fresh:
+            os.remove(os.path.join(outbox, name))
         for acct in state["accounts"].values():
             acct["polled_ms"] = we + paper.DAY_SETTLE_S * 1000
         paper.produce_days(state, tmp, sel, we)
@@ -2401,6 +2445,159 @@ def section_aa(s):
         shutil.rmtree(tmp, ignore_errors=True)
 
 
+def section_w_rescan(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-w16.")
+    saved = (paper.info, paper.leaderboard_chunks, paper.fetch_exchange, common.OUTBOX_DIR)
+    try:
+        a1, a2, a3, a4 = ("0x%040d" % i for i in (1, 2, 3, 4))
+        blob = json.dumps({"leaderboardRows": [{"ethAddress": a, "windowPerformances": [["allTime", {"vlm": "3e8"}]]}
+                                               for a in (a1, a2, a3, a4)]}).encode("utf-8")
+        worlds = {a1: w_portfolio([0.02, 0.0] * 26), a2: w_portfolio([0.03, -0.01] * 26),
+                  a3: w_portfolio([0.025, -0.005] * 26), a4: w_portfolio([-0.01] * 16 + [0.02, 0.0] * 18)}
+        w0, h = W_T0 - 91 * paper.DAY_MS, 3600000
+        good = [w_fill(w0 + h, 0, "B", 10), w_fill(w0 + 4 * h, 10, "A", 10), w_fill(w0 + 5 * h, 0, "A", 10),
+                w_fill(w0 + 6 * h, -10, "B", 10), w_fill(w0 + 8 * h, 0, "B", 10, coin="xyz:CL")]
+        fills = {a1: good, a2: good, a3: [], a4: good}
+        reads = []
+
+        def fake(body, limiter):
+            reads.append((body["type"], body["user"]))
+            if body["type"] == "portfolio":
+                return worlds[body["user"]]
+            return [f for f in fills[body["user"]] if body["startTime"] <= f["time"] <= body.get("endTime", f["time"])]
+        paper.info, paper.leaderboard_chunks = fake, lambda: [blob]
+        paper.fetch_exchange = lambda: reads.append(("exchange", "-")) or {"symbols": []}
+        clock = lambda: W_T0 + 5 * h  # noqa: E731
+        ranks = sorted((a1, a2, a3), key=lambda a: -paper.metrics(worlds[a], W_T0)["sharpe"])
+        s.check("the fixture ranks a1, a3, a2 and leaves a4 eligible, short of the rule", ranks == [a1, a3, a2]
+                and not paper.metrics(worlds[a4], W_T0)["r12"] and paper.metrics(worlds[a4], W_T0)["eligible"])
+        res = paper.select(tmp, {}, None, clock, work="rescan-1-work.jsonl", symbols=sorted(W_SYMBOLS),
+                           exclude={a1}, k=1, draw_null=False)
+        s.check("rescan: a1 excluded, a3 rejected, a2 picked, no null",
+                [p["address"] for p in res["picks"]] == [a2] and [r["address"] for r in res["rejected"]] == [a3]
+                and res["null"] == [] and res["ranked"] == [a1, a3, a2])
+        s.check("rescan: the excluded account's fills are never read, nor Binance's list",
+                ("userFillsByTime", a1) not in reads and ("exchange", "-") not in reads)
+        s.check("rescan: its T0 is the day it started, and the frozen list is the one used",
+                res["t0_ms"] == W_T0 and res["symbols"] == sorted(W_SYMBOLS))
+        reads.clear()
+        again = paper.select(tmp, {}, None, lambda: W_T0 + 40 * paper.DAY_MS, work="rescan-1-work.jsonl",
+                             symbols=sorted(W_SYMBOLS), exclude={a1}, k=1, draw_null=False)
+        s.check("rescan: resumed from its work file, same T0, no read",
+                reads == [] and again["t0_ms"] == W_T0 and again["picks"] == res["picks"])
+        whole = paper.select(tmp, {}, None, clock, work="selection-work.jsonl", symbols=sorted(W_SYMBOLS))
+        s.check("the selection's defaults: the first TOP_K copyable down the ranking, the null drawn",
+                [p["address"] for p in whole["picks"]] == [a1, a2] and [n["address"] for n in whole["null"]] == [a4])
+        # the schedule
+        sel = {"picks": [{"address": a1, "rank": 1}, {"address": a2, "rank": 2}], "null": [{"address": a4}],
+               "follow_from_ms": W_T0, "window_end_ms": W_T0 + 91 * paper.DAY_MS, "symbols": sorted(W_SYMBOLS)}
+        state = paper.new_state(sel)
+        s.check("a state written before TZ-75: its first rescan is due 14 days after follow_from",
+                paper.rescan_state(state, sel) == {"n": 0, "due_ms": W_T0 + 14 * paper.DAY_MS, "running": False}
+                and state["rescan"]["due_ms"] == W_T0 + 14 * paper.DAY_MS)
+        now = W_T0 + 10 * paper.DAY_MS
+        state["rescan"] = {"n": 0, "due_ms": now, "running": False}
+        s.check("due: two picks, 81 days left", paper.rescan_due(state, sel, now))
+        s.check("not due before its time, nor with no time set",
+                not paper.rescan_due(state, sel, now - 1)
+                and not paper.rescan_due(dict(state, rescan=dict(state["rescan"], due_ms=None)), sel, now))
+        anytime = dict(state, rescan={"n": 0, "due_ms": 0, "running": False})
+        s.check("due with exactly 28 days left, not one millisecond later",
+                paper.rescan_due(anytime, sel, W_T0 + 63 * paper.DAY_MS)
+                and not paper.rescan_due(anytime, sel, W_T0 + 63 * paper.DAY_MS + 1))
+        # the adoption
+        outbox = os.path.join(tmp, "outbox")
+        os.makedirs(outbox)
+        common.OUTBOX_DIR = outbox
+        a5 = "0x" + "c" * 40
+        found = {"t0": paper.iso(W_T0), "t0_ms": W_T0, "counts": {"r12": 5, "eligible": 40}, "ranked": [a1, a5],
+                 "picks": [{"address": a5, "rank": 1, "sharpe": 0.4}], "rejected": []}
+        paper.adopt(state, tmp, sel, found, 1, now)
+        acct = state["accounts"][a5]
+        s.check("adopted: a pick numbered 3, followed from now",
+                (acct["role"], acct["rank"], acct["join_ms"], acct["last_ms"], acct["polled_ms"]) == ("pick", 3, now, now, 0))
+        s.check("pick_joins: the selection's two at follow_from, the third at its join",
+                paper.pick_joins(state, sel) == ([a1, a2, a5], {a1: W_T0, a2: W_T0, a5: now}))
+        s.check("three picks: no rescan is due", not paper.rescan_due(state, sel, now))
+        rel = "rescan/2026-01-07.json"
+        with open(os.path.join(tmp, "records", paper.RECORD_DIR, rel), encoding="utf-8") as fh:
+            doc = json.load(fh)
+        s.check("the rescan record, pending once", state["pending"] == [rel] and doc["k"] == "paper-rescan"
+                and doc["n"] == 1 and [x["rank"] for x in doc["added"]] == [3] and doc["joined_ms"] == now)
+        with open(os.path.join(outbox, sorted(os.listdir(outbox))[-1]), encoding="utf-8") as fh:
+            note = json.load(fh)
+        end = datetime.fromtimestamp(sel["window_end_ms"] / 1000, tz=announce.TBILISI).strftime("%d.%m.%Y")
+        s.check("the notice of a whale added, character for character",
+                note["kind"] == "notice" and note["text"] == "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442: \u043d\u043e\u0432\u044b\u0439 \u043a\u0438\u0442 3\ufe0f\u20e3 \U0001f40b\u2022 0xcccc\u2026cccc \u2014 \u043f\u0440\u043e\u0448\u0451\u043b \u0442\u043e \u0436\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u0431\u043e\u0440\u0430 \u043d\u0430 07.01.2026, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u0434\u043e " + end + ".")
+        none = paper.new_state(sel)
+        paper.adopt(none, tmp, sel, dict(found, t0_ms=W_T0 + 28 * paper.DAY_MS, picks=[]), 2, now)
+        with open(os.path.join(outbox, sorted(os.listdir(outbox))[-1]), encoding="utf-8") as fh:
+            note = json.load(fh)
+        s.check("the notice of a search that added none, character for character",
+                note["text"] == "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 \u043f\u043e\u0438\u0441\u043a \u043a\u0438\u0442\u043e\u0432 07.01.2026: \u043f\u0440\u0430\u0432\u0438\u043b\u043e 12 \u043c\u0435\u0441\u044f\u0446\u0435\u0432 \u043f\u0440\u043e\u0448\u043b\u0438 5 \u0438\u0437 40 \u0441\u0447\u0435\u0442\u043e\u0432, \u043d\u043e\u0432\u044b\u0445 \u043a\u043e\u043f\u0438\u0440\u0443\u0435\u043c\u044b\u0445 \u043d\u0435\u0442.".replace("07.01.2026", "04.02.2026"))
+        s.check("no pick added when none was found", paper.pick_joins(none, sel)[0] == [a1, a2])
+    finally:
+        paper.info, paper.leaderboard_chunks, paper.fetch_exchange, common.OUTBOX_DIR = saved
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
+def section_w_spans(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-w17.")
+    try:
+        near = lambda x, y: x is not None and abs(x - y) <= 1e-12  # noqa: E731
+        p1, p2, n1, n2 = ("0x%040d" % i for i in (11, 12, 21, 22))
+        ff = paper.day_start("2026-01-05") + 3600000
+        we, j2, h = ff + 2 * paper.DAY_MS, ff + paper.DAY_MS, 3600000
+        sel = {"picks": [{"address": p1, "rank": 1}], "null": [{"address": n1}, {"address": n2}],
+               "follow_from_ms": ff, "window_end_ms": we, "follow_from": paper.iso(ff), "window_end": paper.iso(we)}
+        rule = {"capital_usdt": 10000.0}
+        root = os.path.join(tmp, "records", paper.RECORD_DIR)
+        days = ["2026-01-05", "2026-01-06", "2026-01-07"]
+        # (account, t_open, net in USDT): n1's first episode opens before p2 joins, its second after.
+        eps = [(p1, ff + h, 100.0), (n1, ff + 2 * h, 300.0), (p2, j2 + h, 200.0), (n1, j2 + 2 * h, -100.0)]
+
+        def run(with_p2):
+            state = paper.new_state(sel)
+            if with_p2:
+                state["accounts"][p2] = {"role": "pick", "rank": 2, "join_ms": j2}
+            for d in days:
+                os.makedirs(os.path.join(root, "episodes"), exist_ok=True)
+                with open(os.path.join(root, "episodes", d + ".jsonl"), "w", encoding="utf-8") as fh:
+                    fh.write(json.dumps({"k": "day", "date": d}) + "\n")
+                books, funds = [], []
+                for a, t, net in eps:
+                    if paper.utc_date(t) != d or (a == p2 and not with_p2):
+                        continue
+                    leg = {"gross": net, "fee": 0.0}
+                    books.append({"k": "book", "a": a, "coin": "BTC", "t_open": t,
+                                  "d": {str(x): {"src": leg, "stop": leg} for x in paper.DELAYS_S}})
+                    funds.append({"k": "funding", "a": a, "coin": "BTC", "t_open": t, "absent": False,
+                                  "d": {str(x): {"src": 0.0, "stop": 0.0} for x in paper.DELAYS_S}})
+                for sub, lines in (("book", books), ("funding", funds)):
+                    os.makedirs(os.path.join(root, sub), exist_ok=True)
+                    with open(os.path.join(root, sub, d + ".jsonl"), "w", encoding="utf-8") as fh:
+                        fh.write("".join(json.dumps(x) + "\n" for x in [{"k": "day", "date": d}] + lines))
+            state["written"]["funding"] = days[-1]
+            paper.produce_verdict(state, tmp, sel, rule)
+            with open(os.path.join(root, "verdict.json"), encoding="utf-8") as fh:
+                return json.load(fh)
+
+        one = run(False)
+        c = one["cells"]["1800/stop"]
+        s.check("one span: the registered verdict -- TOP 0.01, the null's median of 0.02 and 0", near(c["top"], 0.01)
+                and near(c["null_median"], 0.01) and one["joined"] == {p1: paper.iso(ff)})
+        two = run(True)
+        c = two["cells"]["1800/stop"]
+        # n1 over p1's span: 0.03 - 0.01 = 0.02; over p2's: -0.01; averaged: 0.005. n2: 0. One pair: 0.0025.
+        s.check("two spans: TOP 0.015 and the null pair's mean 0.0025",
+                near(c["top"], 0.015) and near(c["null_median"], 0.0025) and c["null_share_at_or_above"] == 0.0)
+        s.check("two spans: both picks with their joins, two pick episodes booked",
+                two["picks"] == [p1, p2] and two["joined"] == {p1: paper.iso(ff), p2: paper.iso(j2)}
+                and two["booked"]["1800"] == {"pick": 2, "null": 2})
+    finally:
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
```
