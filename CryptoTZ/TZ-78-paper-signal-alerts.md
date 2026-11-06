# TZ-78 — The paper test's signals: a whale's new position opens with «(NEW SIGNAL)», carries his entry, leverage, resting stop and take-profit, and prints the copy sized to the owner's capital and ceilings

**Canonical filename:** `CryptoTZ/TZ-78-paper-signal-alerts.md`
**Report:** `CryptoReports/TZ-78-paper-signal-alerts-report.md`
**Class:** branch TZ (contract §8) — it authorises two repository files besides its report.
**Branch:** `claude/tz-78-paper-signal-alerts`
**Host:** the VPS, for stage C; stages A–B run on any clone.
**Model:** Sonnet — the change is the patch of §10, written by the Architect and executed by it against the live API
before this TZ shipped; the session applies it, proves its bytes and runs the validation. Nothing in it is diagnosis or
design.
**Trigger:** `EXECUTE TZ-78`, with nothing under it: no credential arrives and the Boss is asked for nothing.
**Previous TZ:** TZ-77, accepted 06.11.2026 and merged at `c49e7f2` (pull request #63), in effect; no branch on the
remote is ahead of `main`. A first TZ-78 delivered earlier on 06.11.2026 was never uploaded; this one replaces it.
**Issued:** 06.11.2026, by the Architect.
**Written against:** contract v31, map `2026-11-06-f`, `analyst/owner.json` of 06.11.2026, and `main` at `bd3a838`,
read from the repository on 06.11.2026.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-06-f.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-06-f.**` |
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
| `analyst/owner.json` | 27 | `dc7dd911c8d0f262cf749ce9c2aa1e03` | equal, or A1 stops: the copy line sizes on the owner's declaration of 06.11.2026, `capital.usdt` 30000 |
| `vps/paper.py` | 1785 | `2d814305c3e2883c79dbcf1c6fa14068` | equal, or A1 stops: §10 is written against these bytes, TZ-77's merged file |
| `vps/selftest.py` | 3063 | `505efb7dc01c40dd09c9c9008e49345b` | equal, or A1 stops: §10 is written against these bytes |

The map itself: 2804 lines, MD5 `c257b761bf1775d9abdab74a48262b9f` — reported, not enforced.

---

## 1. What changes, and the evidence for it

**The owner, 06.11.2026, verbatim — first message**, on his screenshot of pick 1's alerts, the leverage «5x», the
volume «469 USDT» and the risk «0.5%» circled, «Бумажный тест» crossed out for «signal»:

- «I WANT TO RECEIVE PRECISE INFORMATION ABOUT THE TRADES OPENED BY THE WHALES, ESPECIALLY THE ENTRY PRICE AND
  LEVERAGE / STOP LOSS, IF ONE IS SET / TAKE PROFIT, ALSO IF ONE IS SET!»
- «Ideally, the number 1️⃣ should appear next to the 🐋 symbol.»
- «when an informational message from the Whales arrives in Telegram, it must be labeled at the beginning of the text
  as (SIGNAL). Only these specific messages should be labeled this way!» — and «All other informational SMS messages
  should remain PAPER TEST!»

**Second message, after the Architect's reply:**

- «I usually open a LONG or SHORT order with my personal margin starting from 1,000 USDT and leverage ranging from X3 to
  X11, depending on my level of confidence. Sometimes I have to add margin to move the liquidation price further away!»
- «The total amount of capital I have is up to 30,000 USDT.»
- «a whale might have opened a trade, for example, two weeks ago, and might currently be adding to that position […]
  Therefore, one option would be to label new whale trades as (NEW SIGNAL).»
- «alerts should arrive without stop-loss levels, BUT WHEN THE SYSTEM DETECTS A STOP LOSS, IT SHOULD THEN INCLUDE THAT
  FACT IN THE ALERT!»
- «The system must intelligently copy WHALE signals based on our capabilities and budget!»

**What the open alert printed, and why it misled.** `P_OPEN` printed the fill's price, the position's leverage setting,
the test's 2σ stop and «объём {notional} USDT при риске {risk}% капитала» — the test's own size: 0.5 % of the
10 000 USDT `analyst/owner.json` declared at the selection, frozen there, at the 2σ stop: 50 USDT over 10.7 % = 469
USDT of notional on ENA. It is the rule's size on a capital the owner no longer holds — never the whale's, never a
size for his account. The whale's own entry, stop and take-profit were never read.

**Read 06.11.2026 at 14:11 UTC from the Architect's session, keyless, `api.hyperliquid.xyz/info`:**

- `clearinghouseState` answers each position's `szi`, `entryPx`, `positionValue` and `leverage {type, value}`, and the
  account's `marginSummary.accountValue` and `totalNtlPos` — the fields `read_leverage` read, and three more.
- `frontendOpenOrders` answers each resting order's `coin`, `side` (`A` sells, `B` buys), `orderType` — `Stop Market`,
  `Take Profit Market`, `Take Profit Limit` and `Limit` seen — `isTrigger`, `triggerPx`, `limitPx`, `reduceOnly`, `oid`
  and `children`: an unfilled entry's attached exits, which the answer also lists at top level.
- Pick 1 held 27 positions on an account of 1.20 M USDT at 2.8x, leverage settings from 2x to 40x, with 473 resting
  orders: 441 entry limits, 28 exits on a closing side (22 reduce-only limits, 6 Take Profit triggers), the four
  children of a resting BTC entry, **and no active stop**. Pick 2 held five positions at 0.2x and no order.
- Three of pick 1's reduce-only limits rest **below** a long's entry — KAITO 0.42 from 0.44, XRP 1.48 from 1.481294,
  PONS 0.65 from 0.658425: exits on a recovery, not stops. **An exit is therefore classed by its `orderType`, never by
  its side of the entry.** *[Architect's decision. Discarded: classing by the entry's side, which would have printed
  those three as the whale's stop.]*
- The 333 rows the recorder wrote under TZ-77 into `analyst/paper/orders/` carry the same types.

**Decided:**

1. **A new position opens with «(NEW SIGNAL)», its close with «(SIGNAL)».** `apply_fill` opens an episode only from a
   flat position or by a flip, so a fill that adds to, trims or averages a position the whale already holds has never
   sent a message and does not now. Then the time, 🐋 with the whale's number beside it, his address. Every other
   message — start, new-whale notice, rescan, run-on, verdict — stays «Бумажный тест»; the new-whale notice puts the
   number beside 🐋 too.
2. **The open reads the whale's account at the signal:** his average entry; his leverage setting beside the account's
   notional over its value; the position's value and its share of his account; his resting stops and targets on the
   closing side, each as he placed it, with its result from his entry, in the order they would trigger — «нет» where
   none rests, «н/д» where his orders cannot be read. A read of the other side, or of a position a later fill of the
   same poll closes, is no read. *[Architect's decision. Discarded: a second alert when the whale rests a stop after the
   signal — §10's standing decision keeps an alert on a resting order for the pilot; pick 1 rested no active stop on 27
   positions; a whale's stop that triggers reaches the owner as the close.]*
3. **The copy's stop** is the test's 2σ, printed as «Стоп копии» to at least five significant digits — a fill's price
   string drops its trailing zeros, and a stop from a fill at «0.44» printed 0.4136 as «0.41».
4. **The copy line replaces the test's size.** It sizes the copy exactly as the booking sizes an episode —
   `risk_usdt(capital, risk_pct_medium / 100)` over the stop's distance — but on `analyst/owner.json` as the file stands
   at the signal, so the owner's next declaration reaches the next signal: at 30 000 USDT, 150 USDT to the stop. It
   prints the order's notional, its margin at 3x — the owner's lowest leverage — and the copy's place among the open
   signals of its side; where the open signals on its side, this one counted, would pass `side_max_pct`, or all of
   them `book_max_pct`, each holding as many copies as its ceiling holds `risk_pct_medium`, it prints a skip instead.
   **A copy's loss is its notional's move to the stop, which no leverage changes;** the margin is the collateral the
   order locks, and adding margin moves the liquidation and nothing the stop decides. *[Architect's decision.
   Discarded: the owner's margins of 2 500 and 5 000 USDT at the whale's leverage — on ENA a loss to one stop of 1 346
   and 2 691 USDT, nine and eighteen times the 150 USDT his policy sets at 30 000, at a leverage that is the whale's
   margin setting, not his risk; a confidence grade, none being measured (inv. 49); a leverage ceiling or a liquidation price, `lMoney` and `liqPrice` being the system's only
   ones (inv. 20, 38).]*
5. **`read_leverage` leaves:** `read_whale` reads the same leverage through `leverage_in`, which the two shared; its four
   checks leave with it, their cases kept as `read_whale`'s. `load_rule` reads the capital and the medium risk through
   `owner_book`, which also reads the two ceilings.

**Nothing else moves:** the selection and its constants, the frozen rule — 0.5 % of 10 000 USDT at the 2σ stop, which
the booking keeps bit for bit through `risk_usdt` — the fee, the funding, the verdict, every record already written,
the alerts' own rule — a pick, a fill fresher than `ALERT_MAX_AGE_S`, inside the window — and the outbox's kinds.

---

## 2. Text this TZ obeys

- Contract §7 item 1: «**No change to scoring, leverage, liquidation or geometry math** unless the TZ explicitly cites a
  completed backtest» — no function the item names is touched; the copy line's notional is the booking's own sizing,
  and its margin is that notional over 3; nothing computes a leverage, a ceiling of one, or a liquidation.
- Contract §7 item 2: «**Never edit a bench to make it pass.**» — the eight checks §3 lists as re-specified assert the
  text this TZ changes, and the Architect wrote their new expectations before execution, each derived in §3; the four
  `read_leverage` checks leave with the function, their cases kept by `read_whale`'s. The session edits no check.
- Contract §7 item 9: «**A program in this repository that a VPS unit runs, and whose output that unit commits, has a
  workflow step's standing on the same terms**» — the recorder's reads of the info API stand there. V5's reads measure
  this session's environment, are recorded beside their command, write nothing and produce no product fact.
- Contract §7 item 15: «An implementation session never enables, starts or leaves running a persistent unit, timer or
  service from a branch; it may start TRANSIENT units from its branch for a measurement its TZ names, and its report
  proves none is left behind.»
- Map inv. 38: «**A second implementation of any rule, threshold or formula is banned in any language and any file.**»
  — the copy and the booking share `risk_usdt`; the read guard applies the poll's later fills with `apply_fill` itself,
  on a scratch copy; one `result()` serves the close's gain test, the exits and the whale's stop; the ceilings are
  `owner.json`'s, read through one `owner_book`, and the leverage parse is `leverage_in`.
- Map inv. 49: «**An admissibility band is derived from a null computed in the same run.**» — the signal prints no grade
  and no band; the ceilings are the owner's standing policy.
- Map inv. 22: «**A check that passes with no data is forbidden.**» — V5 fails on zero positions read.

---

## 3. The signal — registered

Each item names what derived it. §10 implements this section and nothing else.

**The open**, line by line, `{}` a field:

```text
**(NEW SIGNAL)** {HH:MM} Тбилиси · 🐋{N} {addr} открыл {LONG|SHORT} {🟢|🔴} {SYMBOL}
Вход кита: `{entry}` · плечо {L}x (весь счёт {A}x) · позиция {value} = {share}% счёта кита
Стоп кита: {stop} · тейк кита: {target}
Стоп копии: `{price}` (−{2σ}%)
Копия: объём `{notional}` USDT · маржа `{margin}` при 3x · до стопа −{risk} USDT ({pct}% от {capital}) · {SIDE}: {n}-я из {cap}
```

**A skip in place of the last line:** `Копия: пропустить — в {SIDE} уже {n} из {cap}, это {side_max_pct}% депозита`, or
`Копия: пропустить — открыто уже {n} из {cap}, это {book_max_pct}% депозита`.

**The close:** `**(SIGNAL)** {HH:MM} Тбилиси · 🐋{N} {addr} {❎|❌} Закрыл {LONG|SHORT} {SYMBOL} по {px} · в позиции 🕚 {held}.`
— the rule of ❎ and ❌ unchanged.

- **Entry** — the whale's `entryPx` as his account answers it, or the fill's price without a read. Without a read the
  entry line ends at «плечо н/д» and the exits line reads «Стоп и тейк кита: н/д». **What derived it:** §1's answers.
- **Value and share** — `positionValue` in «млн» or «тыс.» to one decimal, under 1 000 in whole USDT; its share of
  `accountValue` to one decimal, two below 0.1 %, «<0.01» below that.
- **Exits** — on the closing side only (`A` for a long, `B` for a short), a child of a resting parent left out: a
  **stop** is a trigger whose `orderType` begins `Stop`, a **target** a trigger whose `orderType` begins `Take Profit`
  or a reduce-only `Limit` that is no trigger; an opening order is neither. Each side prints its first to trigger — a
  long's highest stop and lowest target, a short's lowest stop and highest target — as the whale placed it, with its
  result from his entry, negative for a loss, then «и ещё N»; «нет» where the side has none. **What derived it:** §1's
  three reduce-only limits below a long's entry.
- **The copy's stop** — the fill's price moved 2σ against the side (`INV_FLOOR_SD` × σ, the rule's), printed with the
  fill price's decimals and never fewer than five significant digits; «Стоп копии: не рассчитан — нет дневных свечей
  Binance» with no σ, or where a long's stop would not be above zero — and then no copy line.
- **The copy line** — with `owner.json` readable at the signal: `risk = capital × risk_pct_medium / 100`; `notional =
  risk / 2σ` and `margin = notional / 3`, both rounded to whole USDT and printed ungrouped for copying; the side's
  count `n` is the open pick episodes on that side — the other picks' and this account's, this one counted — and its
  ceiling `cap = side_max_pct / risk_pct_medium`; the book's the same over both sides with `book_max_pct`. The side's
  ceiling is read first. **What derived it:** the booking's sizing in `book_delay` and the owner's policy in
  `owner.json`, `side_max_pct` 3.0 and `book_max_pct` 5.0 at `risk_pct_medium` 0.5: six to a side, ten in all.

**Known answers, derived by hand** — W11's fixture: a HYPE long filled at 80.021 on 16.10.2026 10:05 UTC (14:05 in
Tbilisi), σ 0.02 so 2σ = 4.0 %, the owner's book `capital_usdt` 30 000, `risk_pct` 0.5, ceilings 3.0 and 5.0:

| Case | Derivation | Prints |
|---|---|---|
| the copy, first LONG | risk 30 000 × 0.005 = 150; 150 / 0.04 = 3 750; / 3 = 1 250 | `` объём `3750` USDT · маржа `1250` при 3x · до стопа −150 USDT (0.5% от 30 000) · LONG: 1-я из 6 `` |
| the whale's stop 76.5 and targets 85, 90 | 76.5 / 80.021 − 1 = −4.40 %; 85: +6.22 % | `` `76.5` (−4.4%) · тейк кита: `85` (+6.2%) и ещё 1 `` |
| the copy's stop | 80.021 × 0.96 = 76.82016 | `` `76.820` (−4.0%) `` |
| ENA filled at 0.17419, σ 0.0535, two LONG already | 2σ = 10.7 %; 0.17419 × 0.893 = 0.155552; 150 / 0.107 = 1 401.9; / 3 = 467.3 | `` `0.15555` (−10.7%) `` · `` объём `1402` USDT · маржа `467` `` · `LONG: 3-я из 6` |
| six LONG open, a seventh LONG | LONG 7 > 3.0 / 0.5 = 6 | `Копия: пропустить — в LONG уже 6 из 6, это 3% депозита` |
| four LONG and six SHORT open, a LONG | LONG 5 ≤ 6; all 11 > 5.0 / 0.5 = 10 | `Копия: пропустить — открыто уже 10 из 10, это 5% депозита` |
| six LONG open, a SHORT | SHORT 1 ≤ 6; all 7 ≤ 10 | `SHORT: 1-я из 6` |
| short, whale 2, no read | 80.021 × 1.04 = 83.22184 | `` `83.222` (−4.0%) `` and the copy line, `SHORT: 1-я из 6` |
| short, his stops 82 and 84, target 78 | 82: +2.47 % against a short; 78: −2.53 % for it | `` `82` (−2.5%) и ещё 1 · тейк кита: `78` (+2.5%) `` |
| filled at «0.44», σ 0.03 | 0.44 × 0.94 = 0.4136 | `` `0.41360` (−6.0%) `` |
| close at 82.10 after 6 h 12 min | the TZ-75 rule, unchanged | `**(SIGNAL)** 20:17 Тбилиси · 🐋1️⃣ 0xf97a…ddd1 ❎ Закрыл LONG HYPEUSDT по 82.10 · в позиции 🕚 6.2 ч.` |

The reader's fixture, a LIT long at 3.10: stops `2.95`, `2.9` (Stop triggers, highest first) and targets `3.5`, `3.6`
(a reduce-only limit and a Take Profit trigger), with the non-reduce-only limit at 3.7, the buying side's limit, BTC's
order and the child at 2.7 of a resting entry at 3.05 left out; the same as a short reads stops `3.3`, `3.4` and targets
`2.9`, `2.8` on the buying side. The flow's fixture: an account already holding a LONG episode on ETH, the other picks
holding one LONG and one SHORT, and a LONG opened on BTC: `LONG: 3-я из 6`. **Probed:** every line above passes on the
patched tree, and §1's 11 live positions of the two picks render through `read_whale` with none failed (V5's script,
run by the Architect at 16:27 UTC).

**The checks of `vps/selftest.py`, section W:**

- **Re-specified, the expectation moving with the text (8):** «the open signal, character for character: the whale's
  facts and the copy sized at 0.5% of 30 000», «the open signal without a sigma or a whale read: no stop, no copy»,
  «the short open: red dot, the copy's stop above, whale 2, a short copy», «the close signal in gain after 6 h 12 min:
  green cross», «a move inside the fee both ways is a loss: red cross», «the flow's open signal: whale 1, no leverage
  without a reader», «_apply asks the reader for the fill's coin and prints its answer» and «the notice of a whale
  added, character for character».
- **Added (23):** «no owner book: no copy line», «no stop of the whale: the copy's stop alone», «a 10.7% stop sizes the
  copy at 1402 USDT, the third LONG of six», «six open LONG signals already: the seventh is a skip», «ten open signals
  already: the eleventh is a skip whatever its side», «a full LONG side leaves a SHORT copy open», «a short's stop above
  and target below, each a result from the entry», «a computed stop keeps five significant digits when the fill's price
  string is short», «a long's stop beyond its price is no stop and no copy», «a whale read of the other side is no
  read», «money and grouped», «share_text: one decimal, two below 0.1, then a floor», «a new whale's notice: its number
  beside the whale»; six of `read_whale` — the position and its exits in trigger order, a short's exits, open orders
  refused, no position, no `marginSummary`, a refused read; «owner_book: the owner file's capital, medium risk and side
  and book ceilings; owner_now None without it»; and three of the flow: «the copy line counts the account's open
  episodes, this one and the other picks'», «closed later in the same poll: the signal reads no position» and «added to
  later in the same poll: the signal reads the position».
- **Removed with `read_leverage` (4):** its four checks — the setting and the notional, no position, no
  `marginSummary`, a refused read.

Section W therefore moves from 185 to 204 checks, and no other section moves.

---

## 4. Scope

### Files to Create
None in the repository but the report.

### Files to Modify
- `vps/paper.py` — §10.
- `vps/selftest.py` — §10: the eight re-specified checks, the twenty-three added and the four removed with
  `read_leverage`, as §3 lists them.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
One transient unit started from the branch's clone for V5, gone before the report. No unit, timer or file under `/etc`
or `/var/lib/cryptopaper` is created, changed or restarted: **the running paper test is not touched**, and the signal
takes effect when the deployer installs the merge.

### Not touched
`index.html`, `main.py`, `vps/bot.py`, every unit and the manifest, `bench.yml`, `analyst/**`, the map, the contracts.

---

## 5. Stages

### Stage A — readings, no writes
- **A0.** Contract §4a steps 1–6; the gate of §0, every anchor cut from the map's own table.
- **A1.** The four added files of §0 at their lines and MD5; any difference stops the TZ, BLOCKED, naming the file.
- **A2.** On the VPS, the baseline from `main`: `python3 vps/selftest.py` prints `selftest: sections 27 checks 643
  failed 0 empty 0` and `section W: checks 185 failed 0`. *Measured by the Architect on `bd3a838`'s tree; the owner
  file's new capital moves no count, the checks reading it compare it with the file.* A different baseline is recorded
  per section and the TZ goes on: stage C compares against what A2 read.
- **A3.** `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service`, kept for V8.

### Stage B — the code, on the branch
- **B1.** Branch `claude/tz-78-paper-signal-alerts` from `origin/main`. Extract §10's patch with the one command

  ```sh
  awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-78-paper-signal-alerts.md > /tmp/tz78.patch
  ```

  and record its lines and MD5 — 561 and `f2168d62d6d97e1c89a94a96a107f6a0` as written; an upload that strips the
  patch's blank context lines changes the hash and not the result, which B2 decides.
- **B2.** `git apply /tmp/tz78.patch`. **Required:** `vps/paper.py` 1947 lines, MD5 `60018d258594aa629e6f8d5f0dc5c6d9`;
  `vps/selftest.py` 3173 lines, MD5 `f79b05657550180ad9f18603cda5cec1`. Any other result is BLOCKED: the patch did not
  arrive as written, and no hand edit replaces it.
- **B3.** Commit with §7's implementation message, **locally, before stage C**, so that V4's restore returns the
  changed file. Not pushed yet.

### Stage C — validation, on the VPS, on the committed branch
§6, in full.

### Stage D — push, pull request, report
Push; a pull request to `main` titled `TZ-78: paper — a whale's new position as a (NEW SIGNAL) with his entry, leverage,
resting stop and take-profit, and the copy sized to the owner's capital and ceilings`, its body naming this TZ, or the
§8 fallback. Then the report.

---

## 6. Validation

| # | Check | Required |
|---|---|---|
| V1 | `python3 -m py_compile vps/paper.py vps/selftest.py` | exit 0 |
| V2 | B2's two files | the lines and MD5s of B2 |
| V3 | `python3 vps/selftest.py` on the branch, on the VPS | `selftest: sections 27 checks 662 failed 0 empty 0`; `section W: checks 204 failed 0`; **every other section's count equal to A2's**. *Measured by the Architect on the patched tree, 06.11.2026: W moves by exactly 19 — 23 added, 4 removed — and the 458 checks outside W do not move.* If A2 read another baseline, A2's total + 19 and A2's W + 19 |
| V4a | Negative control: in the working tree replace `("A" if side > 0 else "B") or o["oid"] in waiting:` with `("A" if side > 0 else "B"):` in `vps/paper.py`; run the selftest; restore with `git checkout -- vps/paper.py` | exit 1 with exactly one `FAIL` line, `FAIL section W: read_whale: the position, and the closing side's stops and targets in trigger order; an opening order and one waiting on a resting parent out`, and `selftest: sections 27 checks 662 failed 1 empty 0`; then `git status --porcelain` prints nothing. *Measured by the Architect, 06.11.2026* |
| V4b | Negative control: replace `any(kind != "open"` with `any(kind == "lost"` in `vps/paper.py`; run; restore the same way | exit 1 with exactly two `FAIL` lines, `FAIL section W: closed later in the same poll: the signal reads no position` and `FAIL section W: added to later in the same poll: the signal reads the position`, and `selftest: sections 27 checks 662 failed 2 empty 0`; then `git status --porcelain` prints nothing. *Measured by the Architect, 06.11.2026* |
| V4c | Negative control: replace `    if n_side > cap_side:` with `    if n_side > cap_side + 1:` in `vps/paper.py`; run; restore the same way | exit 1 with exactly one `FAIL` line, `FAIL section W: six open LONG signals already: the seventh is a skip`, and `selftest: sections 27 checks 662 failed 1 empty 0`; then `git status --porcelain` prints nothing. *Measured by the Architect, 06.11.2026* |
| V5 | **The reader against the picks' live accounts.** §9's script, extracted with the one command `awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-78-paper-signal-alerts.md > /tmp/tz78-v5.py` — 19 lines, MD5 `bbb8cb0a1b445af2d18312ffb60983a9` as written — and run from the branch's clone as a transient unit: `systemd-run --wait --pipe --collect -p MemoryMax=128M -p WorkingDirectory=<clone> /usr/bin/python3 /tmp/tz78-v5.py` | exit 0; last line `v5: positions N read N failed 0`, N at least 1 and at most six per pick of `analyst/paper/selection.json`; every other line one rendered signal, recorded verbatim. **Any `failed`, or N = 0: BLOCKED, nothing pushed.** *Run by the Architect at 16:27 UTC from its session: `v5: positions 11 read 11 failed 0`* |
| V6 | `git diff --numstat origin/main...HEAD` | exactly two lines, tab-separated: `206`, `44`, `vps/paper.py` and `135`, `25`, `vps/selftest.py` |
| V7 | `systemctl list-units --all 'run-*'` after V5 | none of the session's transient units is left |
| V8 | `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service` after the session | equal to A3 — the live test was not restarted |
| V9 | `bench.yml` | `index.html` and `main.py` are untouched, so the standing checks do not apply; report which workflows ran on the branch, from the runner where the session can, and that no step of the hosted gate runs `vps/selftest.py`, which the deployer runs before it installs |

**No regression:** every check outside the eight re-specified and the four removed is unchanged and green (V3) — W14's
flow, W15's booking memory, W16's rescan, W17's spans and W18–W20 of TZ-77 among them, every booked number of W included,
the booking's sizing being bit for bit the old expression — and the four removed leave only with the function they
tested.

---

## 7. Commit Message

Implementation: `TZ-78: vps — a whale's new position reaches the owner as a (NEW SIGNAL) with his entry, leverage, resting stop and take-profit, and the copy sized to the owner's capital within his side and book ceilings`

Report: `TZ-78: report — the paper test's signals`

---

## 8. The report

Contract §10 in full. Beside it: B1's command and the patch's lines and MD5; B2's lines and MD5s; A2's and V3's
per-section counts side by side; V4a's, V4b's and V4c's `FAIL` lines verbatim; V5's command and every line it printed;
A3's and V8's readings. The map's row «Hyperliquid's large accounts» is the Architect's to update after the audit, not
this TZ's.

---

## 9. The probe script (V5)

Run from the clone's root, which holds `vps/` and `analyst/paper/selection.json`. It writes nothing, reads at most six
positions per pick, and spends the info API at the rescan's share of the budget, so the running recorder keeps its own.

```python
import json, sys, time
sys.path.insert(0, "vps")
import paper
sel = json.load(open("analyst/paper/selection.json", encoding="utf-8"))
limiter, read, failed = paper.Limiter(paper.RESCAN_WEIGHT_PER_MIN), 0, 0
for pick in sel["picks"]:
    addr, rank = pick["address"], pick["rank"]
    held = paper.info({"type": "clearinghouseState", "user": addr}, limiter)["assetPositions"]
    for coin in [p["position"]["coin"] for p in held][:6]:
        w = paper.read_whale(addr, coin, limiter)
        if w is None or w["stops"] is None:
            failed += 1
            print(rank, coin, "failed")
            continue
        read += 1
        ep = {"a": addr, "coin": coin, "symbol": coin, "side": w["side"], "t_open": int(time.time() * 1000), "px_open": w["entry"]}
        print(paper.alert_open(ep, rank, sel["rule"], None, w).replace("\n", " | "))
print("v5: positions %d read %d failed %d" % (read + failed, read, failed))
sys.exit(1 if failed or not read else 0)
```

---

## 10. The patch

Against `main` at `bd3a838`: `vps/paper.py` 1785 → 1947 lines, `vps/selftest.py` 3063 → 3173.

```diff
diff --git a/vps/paper.py b/vps/paper.py
index 895a3b9..10b4058 100644
--- a/vps/paper.py
+++ b/vps/paper.py
@@ -101,11 +101,27 @@ RECORD_DIR = "analyst/paper"
 DEPLOYED_TREE = os.path.join(common.STATE_DIR, "deployed-vps-tree")
 REPO = os.path.dirname(common.VPS_DIR)
 
-# --- TZ-64 section 12.5.2 as TZ-75 A1 restyles it, character for character.
-P_HEAD = "\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 {num} \U0001f40b\u2022 {addr} "
-P_OPEN = P_HEAD + "\u043e\u0442\u043a\u0440\u044b\u043b {side} {dot} {symbol} \u043f\u043e {px} \u00b7 \u043f\u043b\u0435\u0447\u043e {lev} \u00b7 \u0441\u0442\u043e\u043f {dist}% \u2192 {stop} \u00b7 \u043e\u0431\u044a\u0451\u043c {notional} USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a\u0435 {risk}% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430."
-P_OPEN_BARE = P_HEAD + "\u043e\u0442\u043a\u0440\u044b\u043b {side} {dot} {symbol} \u043f\u043e {px} \u00b7 \u043f\u043b\u0435\u0447\u043e {lev} \u00b7 \u0441\u0442\u043e\u043f \u0438 \u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: \u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance."
-P_CLOSE = P_HEAD + "{mark} \u0417\u0430\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \U0001f55a {held}."
+# --- TZ-64 section 12.5.2 as TZ-75 A1 and TZ-78 restyle it, character for character: a pick's own trade is a
+# signal, first word (SIGNAL), the whale's number beside the whale; every other message stays a paper-test notice.
+P_SIGNAL = "**(SIGNAL)** {hhmm} \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \U0001f40b{num} {addr} "
+P_NEW = "**(NEW SIGNAL)** {hhmm} \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \U0001f40b{num} {addr} "
+P_OPEN_LINE = "\u043e\u0442\u043a\u0440\u044b\u043b {side} {dot} {symbol}"
+P_ENTRY = "\u0412\u0445\u043e\u0434 \u043a\u0438\u0442\u0430: `{px}` \u00b7 \u043f\u043b\u0435\u0447\u043e {lev}{pos}"
+P_POS = " \u00b7 \u043f\u043e\u0437\u0438\u0446\u0438\u044f {value} = {share}% \u0441\u0447\u0451\u0442\u0430 \u043a\u0438\u0442\u0430"
+P_EXITS = "\u0421\u0442\u043e\u043f \u043a\u0438\u0442\u0430: {sl} \u00b7 \u0442\u0435\u0439\u043a \u043a\u0438\u0442\u0430: {tp}"
+P_EXITS_NONE = "\u0421\u0442\u043e\u043f \u0438 \u0442\u0435\u0439\u043a \u043a\u0438\u0442\u0430: \u043d/\u0434"
+P_EXIT = "`{px}` ({pct}%)"
+P_MORE = " \u0438 \u0435\u0449\u0451 {n}"
+P_NO = "\u043d\u0435\u0442"
+P_GUARD = "\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: `{stop}` (\u2212{dist}%)"
+P_GUARD_NONE = "\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d \u2014 \u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance"
+P_CLOSE = "{mark} \u0417\u0430\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \U0001f55a {held}."
+MLN, THS = "\u043c\u043b\u043d", "\u0442\u044b\u0441."
+P_COPY = ("\u041a\u043e\u043f\u0438\u044f: \u043e\u0431\u044a\u0451\u043c `{size}` USDT \u00b7 \u043c\u0430\u0440\u0436\u0430 `{margin}` \u043f\u0440\u0438 {lev}x \u00b7 \u0434\u043e \u0441\u0442\u043e\u043f\u0430 \u2212{risk} USDT ({pct}% \u043e\u0442 {capital})"
+          " \u00b7 {side}: {n}-\u044f \u0438\u0437 {cap}")
+P_SKIP_SIDE = "\u041a\u043e\u043f\u0438\u044f: \u043f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u2014 \u0432 {side} \u0443\u0436\u0435 {n} \u0438\u0437 {cap}, \u044d\u0442\u043e {pct}% \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u0430"
+P_SKIP_BOOK = "\u041a\u043e\u043f\u0438\u044f: \u043f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u2014 \u043e\u0442\u043a\u0440\u044b\u0442\u043e \u0443\u0436\u0435 {n} \u0438\u0437 {cap}, \u044d\u0442\u043e {pct}% \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u0430"
+COPY_LEV = 3   # TZ-78: the owner's lowest leverage, his statement of 06.11.2026; a copy's loss does not depend on it
 P_LEV = "{lev}x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 {acct}x)"
 P_LEV_NONE = "\u043d/\u0434"
 SIDE_DOT = {1: "\U0001f7e2", -1: "\U0001f534"}
@@ -128,7 +144,7 @@ N_VERDICT = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u044
              "\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0438\u0442\u043e\u0433 \u0437\u0430\u043f\u0438\u0441"
              "\u0430\u043d \u0438 \u0436\u0434\u0451\u0442 \u0440\u0430\u0437\u0431\u043e\u0440\u0430 \u0410\u0440"
              "\u0445\u0438\u0442\u0435\u043a\u0442\u043e\u0440\u0430.")
-N_ADDED = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442: \u043d\u043e\u0432\u044b\u0439 \u043a\u0438\u0442 {num} \U0001f40b\u2022 {addr} \u2014 \u043f\u0440\u043e\u0448\u0451\u043b \u0442\u043e \u0436\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u0431\u043e\u0440\u0430 \u043d\u0430 {date}, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u0434\u043e {end}."
+N_ADDED = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442: \u043d\u043e\u0432\u044b\u0439 \u043a\u0438\u0442 \U0001f40b{num} {addr} \u2014 \u043f\u0440\u043e\u0448\u0451\u043b \u0442\u043e \u0436\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u0431\u043e\u0440\u0430 \u043d\u0430 {date}, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u0434\u043e {end}."
 N_RESCAN_NONE = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 \u043f\u043e\u0438\u0441\u043a \u043a\u0438\u0442\u043e\u0432 {date}: \u043f\u0440\u0430\u0432\u0438\u043b\u043e 12 \u043c\u0435\u0441\u044f\u0446\u0435\u0432 \u043f\u0440\u043e\u0448\u043b\u0438 {r12} \u0438\u0437 {eligible} \u0441\u0447\u0435\u0442\u043e\u0432, \u043d\u043e\u0432\u044b\u0445 \u043a\u043e\u043f\u0438\u0440\u0443\u0435\u043c\u044b\u0445 \u043d\u0435\u0442."
 # --- TZ-77 (1): the window that runs on past thirteen weeks.
 N_RUN_ON = "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0441\u0434\u0435\u043b\u043e\u043a \u043a\u0438\u0442\u043e\u0432 \u0437\u0430 13 \u043d\u0435\u0434\u0435\u043b\u044c \u2014 {n} \u0438\u0437 30 \u043d\u0443\u0436\u043d\u044b\u0445, \u043e\u043a\u043d\u043e \u043f\u0440\u043e\u0434\u043b\u0435\u043d\u043e \u0434\u043e 30-\u0439, \u043d\u043e \u043d\u0435 \u0434\u043e\u043b\u044c\u0448\u0435 {date}."
@@ -189,14 +205,30 @@ def minute(ms):
 
 
 # --- the rule's inputs read from the checkout ---------------------------------
-def load_rule(repo=REPO):
-    """Capital and medium risk from analyst/owner.json; INV_FLOOR_SD and FEE_TAKER cut from
-    index.html (inv. 20: one number per threshold, system-wide)."""
+def owner_book(repo=REPO):
+    """TZ-78: the owner's capital, medium risk, and side and book ceilings, from analyst/owner.json as it stands."""
     with open(os.path.join(repo, "analyst", "owner.json"), encoding="utf-8") as fh:
         owner = json.load(fh)
+    return {"capital_usdt": float(owner["capital"]["usdt"]), "risk_pct": float(owner["risk"]["risk_pct_medium"]),
+            "side_max_pct": float(owner["risk"]["side_max_pct"]), "book_max_pct": float(owner["risk"]["book_max_pct"])}
+
+
+def owner_now(repo=REPO):
+    """TZ-78: owner_book at the signal, so the owner's next declaration reaches the next signal; None when the file
+    cannot be read, and the signal then prints no copy line."""
+    try:
+        return owner_book(repo)
+    except (OSError, ValueError, KeyError, TypeError):
+        return None
+
+
+def load_rule(repo=REPO):
+    """Capital and medium risk from analyst/owner.json, through owner_book; INV_FLOOR_SD and FEE_TAKER cut from
+    index.html (inv. 20: one number per threshold, system-wide)."""
+    own = owner_book(repo)
     with open(os.path.join(repo, "index.html"), encoding="utf-8") as fh:
         page = fh.read()
-    return {"capital_usdt": float(owner["capital"]["usdt"]), "risk_pct": float(owner["risk"]["risk_pct_medium"]),
+    return {"capital_usdt": own["capital_usdt"], "risk_pct": own["risk_pct"],
             "inv_floor_sd": common.cut_number(page, "INV_FLOOR_SD"), "fee_taker": common.cut_number(page, "FEE_TAKER")}
 
 
@@ -532,6 +564,11 @@ def daily_sigma(closes):
     return statistics.pstdev([closes[i + 1] / closes[i] - 1 for i in range(len(closes) - 1)])
 
 
+def risk_usdt(capital, risk_frac):
+    """TZ-78: what one copy may lose to its stop -- the booking's size and the signal's copy line alike (inv. 38)."""
+    return risk_frac * capital
+
+
 def book_delay(ep, delay_s, dist, kl, capital, risk_frac, fee, window_end):
     """One episode copied at one delay. kl = (open times ascending, rows (o, h, l, c)). Entry at
     the close of the minute containing t_open + delay; exit at the close of the minute containing
@@ -549,7 +586,7 @@ def book_delay(ep, delay_s, dist, kl, capital, risk_frac, fee, window_end):
     if i < 0:
         raise Absent("no kline at or before the entry minute")
     entry = rows[i][3]
-    qty = risk_frac * capital / (entry * dist)
+    qty = risk_usdt(capital, risk_frac) / (entry * dist)
     stop = entry * (1 - side * dist)
     hit = None
     for k in range(i + 1, j + 1):
@@ -1048,48 +1085,158 @@ def number(rank):
     return ("%d\ufe0f\u20e3" % rank) if 1 <= rank <= 9 else ("#%d" % rank)
 
 
-def read_leverage(addr, coin, limiter):
-    """(the position's leverage setting, the account's notional over its value) from clearinghouseState,
-    or None: the coin holds no position, or any read or shape failure. Never raises."""
+READ_FAILED = (StopIteration, Transport, KeyError, TypeError, ValueError, ArithmeticError, AttributeError)
+
+
+def leverage_in(doc, coin):
+    """((the position's leverage setting, the account's notional over its value), the position, the account's
+    value) of coin in one clearinghouseState answer; raises on no position or a malformed answer."""
+    pos = next(p["position"] for p in doc["assetPositions"] if p["position"]["coin"] == coin)
+    lev = int(pos["leverage"]["value"])
+    value = float(doc["marginSummary"]["accountValue"])
+    ntl = float(doc["marginSummary"]["totalNtlPos"])
+    if lev < 1 or not value > 0 or not math.isfinite(ntl):
+        raise ValueError("leverage")
+    return (lev, ntl / value), pos, value
+
+
+def read_whale(addr, coin, limiter):
+    """TZ-78: the whale's own position in coin as his account answers at the signal -- its side, leverage as
+    leverage_in reads it, his average entry, the position's value and its share of his account -- and his
+    resting exits in it, each price as he placed it, in the order they would trigger: stops (Stop triggers on the
+    closing side) and targets (Take Profit triggers and reduce-only limits on the closing side), an order waiting
+    on a resting parent excluded; both None when his open orders cannot be read. None when the position cannot
+    be. Never raises."""
     try:
-        doc = info({"type": "clearinghouseState", "user": addr}, limiter)
-        pos = next(p["position"] for p in doc["assetPositions"] if p["position"]["coin"] == coin)
-        lev = int(pos["leverage"]["value"])
-        value = float(doc["marginSummary"]["accountValue"])
-        ntl = float(doc["marginSummary"]["totalNtlPos"])
-        if lev < 1 or not value > 0 or not math.isfinite(ntl):
-            return None
-        return lev, ntl / value
-    except (StopIteration, Transport, KeyError, TypeError, ValueError, ArithmeticError, AttributeError):
+        lev, pos, account = leverage_in(info({"type": "clearinghouseState", "user": addr}, limiter), coin)
+        size, entry, value = float(pos["szi"]), float(pos["entryPx"]), float(pos["positionValue"])
+        if size == 0 or not (entry > 0 and math.isfinite(entry) and value >= 0 and math.isfinite(value)):
+            raise ValueError("position")
+        side = 1 if size > 0 else -1
+        out = {"side": side, "lev": lev, "entry": pos["entryPx"], "value": value, "share": value / account}
+    except READ_FAILED:
         return None
+    try:
+        orders = info({"type": "frontendOpenOrders", "user": addr}, limiter)
+        waiting = {c["oid"] for o in orders for c in o.get("children") or ()}
+        stops, targets = [], []
+        for o in orders:
+            if o["coin"] != coin or o["side"] != ("A" if side > 0 else "B") or o["oid"] in waiting:
+                continue
+            px = o["triggerPx"] if o["isTrigger"] else o["limitPx"]
+            if not (float(px) > 0 and math.isfinite(float(px))):
+                continue
+            if o["isTrigger"] and o["orderType"].startswith("Stop"):
+                stops.append(px)
+            elif (o["orderType"].startswith("Take Profit") if o["isTrigger"]
+                  else o["reduceOnly"] and o["orderType"] == "Limit"):
+                targets.append(px)
+        out["stops"] = sorted(stops, key=lambda p: -side * float(p))
+        out["targets"] = sorted(targets, key=lambda p: side * float(p))
+    except READ_FAILED:
+        out["stops"] = out["targets"] = None
+    return out
 
 
 def lev_text(lev):
     return P_LEV_NONE if lev is None else P_LEV.format(lev=lev[0], acct="%.1f" % lev[1])
 
 
-def alert_open(ep, rank, rule, sigma, lev=None):
-    base = {"hhmm": hhmm(ep["t_open"]), "num": number(rank), "addr": addr_short(ep["a"]),
-            "side": side_word(ep["side"]), "dot": SIDE_DOT[ep["side"]], "symbol": ep["symbol"], "px": ep["px_open"],
-            "lev": lev_text(lev)}
-    if sigma is None or not sigma > 0:
-        return P_OPEN_BARE.format(**base)
-    dist = rule["inv_floor_sd"] * sigma
-    stop = float(ep["px_open"]) * (1 - ep["side"] * dist)
-    notional = rule["risk_pct"] / 100 * rule["capital_usdt"] / dist
-    return P_OPEN.format(dist="%.1f" % (dist * 100), stop="%.*f" % (decimals(ep["px_open"]), stop),
-                         notional="%d" % round(notional), risk=("%g" % rule["risk_pct"]), **base)
+def money(usdt):
+    """A position's value in millions or thousands of USDT, one decimal."""
+    if usdt >= 1e6:
+        return "%.1f %s USDT" % (usdt / 1e6, MLN)
+    if usdt >= 1e3:
+        return "%.1f %s USDT" % (usdt / 1e3, THS)
+    return "%d USDT" % round(usdt)
+
+
+def grouped(n):
+    """A whole number with a space between thousands: 1 850."""
+    return "{:,}".format(int(round(n))).replace(",", " ")
+
+
+def price_text(px, nd):
+    """A computed price: the decimals of the price it derives from, and never fewer than five significant digits --
+    a fill's price string drops its trailing zeros."""
+    return "%.*f" % (max(nd, 4 - int(math.floor(math.log10(px)))), px)
+
+
+def share_text(share):
+    """A position's share of the account, in percent: one decimal, two below 0.1."""
+    pct = 100 * share
+    return "%.1f" % pct if pct >= 0.1 else "%.2f" % pct if pct >= 0.01 else "<0.01"
+
+
+def exit_text(prices, entry, side):
+    """The first of a side's resting exits to trigger, as the whale placed it, with its result from his entry, and
+    how many more; or none."""
+    if not prices:
+        return P_NO
+    pct = 100 * result(side, prices[0], entry)
+    text = P_EXIT.format(px=prices[0], pct=("\u2212" if pct < 0 else "+") + "%.1f" % abs(pct))
+    return text + (P_MORE.format(n=len(prices) - 1) if len(prices) > 1 else "")
+
+
+def copy_text(own, dist, side, sides):
+    """TZ-78: the copy line -- sized as the test sizes, the owner's capital at his medium risk to the copy's stop; or
+    a skip, where the open signals on its side or in all, this one counted, would pass his side or book ceiling,
+    each holding as many copies as its ceiling holds his medium risk."""
+    name, n_side, n_all = side_word(side), list(sides).count(side), len(sides)
+    cap_side = int(round(own["side_max_pct"] / own["risk_pct"], 9))
+    cap_all = int(round(own["book_max_pct"] / own["risk_pct"], 9))
+    if n_side > cap_side:
+        return P_SKIP_SIDE.format(side=name, n=n_side - 1, cap=cap_side, pct="%g" % own["side_max_pct"])
+    if n_all > cap_all:
+        return P_SKIP_BOOK.format(n=n_all - 1, cap=cap_all, pct="%g" % own["book_max_pct"])
+    risk = risk_usdt(own["capital_usdt"], own["risk_pct"] / 100)
+    return P_COPY.format(size="%d" % round(risk / dist), margin="%d" % round(risk / dist / COPY_LEV), lev=COPY_LEV,
+                         risk=grouped(risk), pct="%g" % own["risk_pct"], capital=grouped(own["capital_usdt"]),
+                         side=name, n=n_side, cap=cap_side)
+
+
+def alert_open(ep, rank, rule, sigma, whale=None, own=None, sides=()):
+    """TZ-78: the signal of a pick's new position -- the whale's own entry, leverage, position, and resting stop
+    and target as his account answers at the signal; the copy's stop, the test's 2 sigma; and, with the owner's book,
+    the copy line over sides, the open signals' sides with this one. A whale read of another side than the fill's
+    is no read."""
+    side = ep["side"]
+    w = whale if whale is not None and whale.get("side") == side else None
+    nd = decimals(ep["px_open"])
+    px = ep["px_open"] if w is None else w["entry"]
+    entry = float(px)
+    lines = [P_NEW.format(hhmm=hhmm(ep["t_open"]), num=number(rank), addr=addr_short(ep["a"]))
+             + P_OPEN_LINE.format(side=side_word(side), dot=SIDE_DOT[side], symbol=ep["symbol"]),
+             P_ENTRY.format(px=px, lev=lev_text(None if w is None else w["lev"]), pos="" if w is None else P_POS.format(
+                 value=money(w["value"]), share=share_text(w["share"])))]
+    if w is None or w["stops"] is None:
+        lines.append(P_EXITS_NONE)
+    else:
+        lines.append(P_EXITS.format(sl=exit_text(w["stops"], entry, side), tp=exit_text(w["targets"], entry, side)))
+    dist = rule["inv_floor_sd"] * sigma if sigma is not None and sigma > 0 else None
+    if dist is None or float(ep["px_open"]) * (1 - side * dist) <= 0:
+        lines.append(P_GUARD_NONE)
+        return "\n".join(lines)
+    lines.append(P_GUARD.format(stop=price_text(float(ep["px_open"]) * (1 - side * dist), nd), dist="%.1f" % (dist * 100)))
+    if own is not None:
+        lines.append(copy_text(own, dist, side, sides))
+    return "\n".join(lines)
+
+
+def result(side, px, entry):
+    """A side's move from entry to px, as a fraction: positive is a gain."""
+    return side * (float(px) / float(entry) - 1)
 
 
 def gained(ep, rule):
     """The copy's move from the account's opening price to its closing price beats the taker fee both ways."""
-    return ep["side"] * (float(ep["px_close"]) / float(ep["px_open"]) - 1) > 2 * rule["fee_taker"]
+    return result(ep["side"], ep["px_close"], ep["px_open"]) > 2 * rule["fee_taker"]
 
 
 def alert_close(ep, rank, rule):
-    return P_CLOSE.format(hhmm=hhmm(ep["t_close"]), num=number(rank), addr=addr_short(ep["a"]),
-                          mark=MARK_GAIN if gained(ep, rule) else MARK_LOSS, side=side_word(ep["side"]),
-                          symbol=ep["symbol"], px=ep["px_close"], held=held_text(ep["t_close"] - ep["t_open"]))
+    return P_SIGNAL.format(hhmm=hhmm(ep["t_close"]), num=number(rank), addr=addr_short(ep["a"])) + P_CLOSE.format(
+        mark=MARK_GAIN if gained(ep, rule) else MARK_LOSS, side=side_word(ep["side"]), symbol=ep["symbol"],
+        px=ep["px_close"], held=held_text(ep["t_close"] - ep["t_open"]))
 
 
 def pick_joins(state, sel):
@@ -1168,19 +1315,30 @@ def new_state(sel):
             "next_publish_ms": 0, "closed_notice": False}
 
 
-def poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for):
+def poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for, others=()):
     """New fills since the account's last time, through apply_fill; alerts for a pick's fresh events.
     The account's state changes only when the whole poll succeeded."""
     fills = fills_since(addr, acct["last_ms"], limiter)
     work = json.loads(json.dumps(acct))
-    _apply(addr, work, fills, sel, symbols, now, rule, inputs_for, lambda coin: read_leverage(addr, coin, limiter))
+    _apply(addr, work, fills, sel, symbols, now, rule, inputs_for, lambda coin: read_whale(addr, coin, limiter),
+           owner_now, others)
     acct.clear()
     acct.update(work)
 
 
-def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for, leverage_for=lambda coin: None):
+def closes_later(fills, i, ep):
+    """TZ-78: whether the poll's later fills on ep's coin, applied by apply_fill to a scratch copy holding ep alone,
+    close or lose it -- the whale's account then answers for another position than the signal's, so the signal
+    reads none of it."""
+    scratch = {ep["coin"]: ep}
+    return any(kind != "open" for g in fills[i + 1:] if g["coin"] == ep["coin"]
+               for kind, _ in apply_fill(scratch, g, ep["symbol"]))
+
+
+def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for, whale_for=lambda coin: None, own_for=lambda: None,
+           others=()):
     window_end = sel["window_end_ms"]
-    for f in fills:
+    for i, f in enumerate(fills):
         t = int(f["time"])
         if (t == acct["last_ms"] and f["tid"] in acct["last_tids"]) or t >= window_end:
             continue
@@ -1204,7 +1362,9 @@ def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for, leverage_for=
                         sigma = sigma_for(inputs_for(), sym, t)
                     except (NotReady, Absent, Transport, ValueError, ZeroDivisionError):
                         sigma = None
-                    common.write_outbox("alert", alert_open(ep, acct["rank"], rule, sigma, leverage_for(f["coin"])))
+                    whale = None if closes_later(fills, i, ep) else whale_for(f["coin"])
+                    sides = list(others) + [e["side"] for e in acct["coins"].values() if e is not None]
+                    common.write_outbox("alert", alert_open(ep, acct["rank"], rule, sigma, whale, own_for(), sides))
                 else:
                     common.write_outbox("alert", alert_close(ep, acct["rank"], rule))
     kept = [f for f in fills if int(f["time"]) < window_end]   # TZ-77 (1): a fill past the end as it stands stays
@@ -1631,7 +1791,9 @@ def service(state_dir, tree):
                     continue
                 acct["due_ms"] = now + 1000 * (PICK_POLL_S if acct["role"] == "pick" else NULL_POLL_S)
                 try:
-                    poll(addr, acct, view, symbols, limiter, now, rule, inputs_for)
+                    others = [e["side"] for a, other in state["accounts"].items() if a != addr and other["role"] == "pick"
+                              for e in other["coins"].values() if e is not None]   # TZ-78: the copy line's ceilings
+                    poll(addr, acct, view, symbols, limiter, now, rule, inputs_for, others)
                     if acct["failing"]:
                         common.log("paper: poll %s answered again" % addr_short(addr))
                     acct["failing"] = False
diff --git a/vps/selftest.py b/vps/selftest.py
index df60fc4..eb4eb13 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1569,16 +1569,62 @@ def section_w(s):
     t_open = int(datetime(2026, 10, 16, 10, 5, tzinfo=timezone.utc).timestamp() * 1000)
     ep = {"a": "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1", "coin": "HYPE", "symbol": "HYPEUSDT", "side": 1,
           "t_open": t_open, "px_open": "80.021"}
-    head = "\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 14:05 \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 "
-    whale = "1\ufe0f\u20e3 \U0001f40b\u2022 0xf97a\u2026ddd1 "
-    s.check("the open alert, character for character", paper.alert_open(ep, 1, rule, 0.02, (20, 3.04)) == head + whale + (
-        "\u043e\u0442\u043a\u0440\u044b\u043b LONG \U0001f7e2 HYPEUSDT \u043f\u043e 80.021 \u00b7 \u043f\u043b\u0435\u0447\u043e 20x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 3.0x) \u00b7 \u0441\u0442\u043e\u043f 4.0% \u2192 76.820 \u00b7 \u043e\u0431\u044a\u0451\u043c 1250 USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a\u0435 0.5% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430."))
-    s.check("the open alert without a sigma or a leverage", paper.alert_open(ep, 1, rule, None) == head + whale + (
-        "\u043e\u0442\u043a\u0440\u044b\u043b LONG \U0001f7e2 HYPEUSDT \u043f\u043e 80.021 \u00b7 \u043f\u043b\u0435\u0447\u043e \u043d/\u0434 \u00b7 \u0441\u0442\u043e\u043f \u0438 \u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: \u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance."))
-    s.check("the short open: red dot, stop above, whale 2", paper.alert_open(dict(ep, side=-1), 2, rule, 0.02) == head + (
-        "2\ufe0f\u20e3 \U0001f40b\u2022 0xf97a\u2026ddd1 \u043e\u0442\u043a\u0440\u044b\u043b SHORT \U0001f534 HYPEUSDT \u043f\u043e 80.021 \u00b7 \u043f\u043b\u0435\u0447\u043e \u043d/\u0434 \u00b7 \u0441\u0442\u043e\u043f 4.0% \u2192 83.222 \u00b7 \u043e\u0431\u044a\u0451\u043c 1250 USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a\u0435 0.5% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430."))
+    head = "**(SIGNAL)** 14:05 \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 "   # TZ-78: the close's first word
+    new_head = "**(NEW SIGNAL)** 14:05 \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 "   # TZ-78: a new position's first word
+    whale = "\U0001f40b1\ufe0f\u20e3 0xf97a\u2026ddd1 "
+    read = {"side": 1, "lev": (20, 3.04), "entry": "80.021", "value": 1260000.0, "share": 0.125, "stops": ["76.5"],
+            "targets": ["85", "90"]}
+    own = {"capital_usdt": 30000.0, "risk_pct": 0.5, "side_max_pct": 3.0, "book_max_pct": 5.0}
+    opened = "\u043e\u0442\u043a\u0440\u044b\u043b LONG \U0001f7e2 HYPEUSDT\n\u0412\u0445\u043e\u0434 \u043a\u0438\u0442\u0430: `80.021` \u00b7 \u043f\u043b\u0435\u0447\u043e "
+    copy = "\u041a\u043e\u043f\u0438\u044f: \u043e\u0431\u044a\u0451\u043c `3750` USDT \u00b7 \u043c\u0430\u0440\u0436\u0430 `1250` \u043f\u0440\u0438 3x \u00b7 \u0434\u043e \u0441\u0442\u043e\u043f\u0430 \u2212150 USDT (0.5% \u043e\u0442 30 000) \u00b7 "
+    full = paper.alert_open(ep, 1, rule, 0.02, read, own, [1])
+    s.check("the open signal, character for character: the whale's facts and the copy sized at 0.5% of 30 000", full == new_head + whale + opened + (
+        "20x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 3.0x) \u00b7 \u043f\u043e\u0437\u0438\u0446\u0438\u044f 1.3 \u043c\u043b\u043d USDT = 12.5% \u0441\u0447\u0451\u0442\u0430 \u043a\u0438\u0442\u0430\n"
+        "\u0421\u0442\u043e\u043f \u043a\u0438\u0442\u0430: `76.5` (\u22124.4%) \u00b7 \u0442\u0435\u0439\u043a \u043a\u0438\u0442\u0430: `85` (+6.2%) \u0438 \u0435\u0449\u0451 1\n"
+        "\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: `76.820` (\u22124.0%)\n" + copy + "LONG: 1-\u044f \u0438\u0437 6"))
+    s.check("no owner book: no copy line", paper.alert_open(ep, 1, rule, 0.02, read) == full.rsplit("\n", 1)[0])
+    s.check("the open signal without a sigma or a whale read: no stop, no copy", paper.alert_open(ep, 1, rule, None, None, own, [1])
+            == new_head + whale + opened + ("\u043d/\u0434\n\u0421\u0442\u043e\u043f \u0438 \u0442\u0435\u0439\u043a \u043a\u0438\u0442\u0430: \u043d/\u0434\n"
+                                            "\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d \u2014 \u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance"))
+    s.check("the short open: red dot, the copy's stop above, whale 2, a short copy",
+            paper.alert_open(dict(ep, side=-1), 2, rule, 0.02, None, own, [-1]) == new_head + (
+                "\U0001f40b2\ufe0f\u20e3 0xf97a\u2026ddd1 \u043e\u0442\u043a\u0440\u044b\u043b SHORT \U0001f534 HYPEUSDT\n\u0412\u0445\u043e\u0434 \u043a\u0438\u0442\u0430: `80.021` \u00b7 \u043f\u043b\u0435\u0447\u043e \u043d/\u0434\n"
+                "\u0421\u0442\u043e\u043f \u0438 \u0442\u0435\u0439\u043a \u043a\u0438\u0442\u0430: \u043d/\u0434\n\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: `83.222` (\u22124.0%)\n" + copy + "SHORT: 1-\u044f \u0438\u0437 6"))
+    s.check("no stop of the whale: the copy's stop alone",
+            paper.alert_open(ep, 1, rule, 0.02, dict(read, lev=(3, 0.2), stops=[], targets=[])).endswith(
+                "\u0421\u0442\u043e\u043f \u043a\u0438\u0442\u0430: \u043d\u0435\u0442 \u00b7 \u0442\u0435\u0439\u043a \u043a\u0438\u0442\u0430: \u043d\u0435\u0442\n\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: `76.820` (\u22124.0%)"))
+    ena = dict(ep, symbol="ENAUSDT", px_open="0.17419")
+    s.check("a 10.7% stop sizes the copy at 1402 USDT, the third LONG of six",
+            paper.alert_open(ena, 1, rule, 0.0535, dict(read, lev=(5, 2.8), entry="0.17419", stops=[], targets=[]), own,
+                             [1, 1, 1]).endswith(
+                "\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: `0.15555` (\u221210.7%)\n"
+                "\u041a\u043e\u043f\u0438\u044f: \u043e\u0431\u044a\u0451\u043c `1402` USDT \u00b7 \u043c\u0430\u0440\u0436\u0430 `467` \u043f\u0440\u0438 3x \u00b7 \u0434\u043e \u0441\u0442\u043e\u043f\u0430 \u2212150 USDT (0.5% \u043e\u0442 30 000) \u00b7 LONG: 3-\u044f \u0438\u0437 6"))
+    s.check("six open LONG signals already: the seventh is a skip",
+            paper.alert_open(ep, 1, rule, 0.02, None, own, [1] * 7).endswith(
+                "\u041a\u043e\u043f\u0438\u044f: \u043f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u2014 \u0432 LONG \u0443\u0436\u0435 6 \u0438\u0437 6, \u044d\u0442\u043e 3% \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u0430"))
+    s.check("ten open signals already: the eleventh is a skip whatever its side",
+            paper.alert_open(ep, 1, rule, 0.02, None, own, [1] * 5 + [-1] * 6).endswith(
+                "\u041a\u043e\u043f\u0438\u044f: \u043f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u044c \u2014 \u043e\u0442\u043a\u0440\u044b\u0442\u043e \u0443\u0436\u0435 10 \u0438\u0437 10, \u044d\u0442\u043e 5% \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u0430"))
+    s.check("a full LONG side leaves a SHORT copy open",
+            paper.alert_open(dict(ep, side=-1), 2, rule, 0.02, None, own, [1] * 6 + [-1]).endswith(copy + "SHORT: 1-\u044f \u0438\u0437 6"))
+    s.check("a short's stop above and target below, each a result from the entry",
+            paper.alert_open(dict(ep, side=-1), 2, rule, 0.02, dict(read, side=-1, stops=["82", "84"], targets=["78"]))
+            .split("\n")[2] == "\u0421\u0442\u043e\u043f \u043a\u0438\u0442\u0430: `82` (\u22122.5%) \u0438 \u0435\u0449\u0451 1 \u00b7 \u0442\u0435\u0439\u043a \u043a\u0438\u0442\u0430: `78` (+2.5%)")
+    s.check("a computed stop keeps five significant digits when the fill's price string is short",
+            paper.alert_open(dict(ep, px_open="0.44"), 1, rule, 0.03).endswith("`0.41360` (\u22126.0%)")
+            and paper.price_text(76.82016, 3) == "76.820" and paper.price_text(74708.31, 1) == "74708.3")
+    s.check("a long's stop beyond its price is no stop and no copy", paper.alert_open(ep, 1, rule, 0.6, None, own, [1]).endswith(
+        "\u0421\u0442\u043e\u043f \u043a\u043e\u043f\u0438\u0438: \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d \u2014 \u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance"))
+    s.check("a whale read of the other side is no read", paper.alert_open(ep, 1, rule, 0.02, dict(read, side=-1), own, [1])
+            == paper.alert_open(ep, 1, rule, 0.02, None, own, [1]))
+    s.check("money and grouped", (paper.money(1260000.0), paper.money(23794.87), paper.money(950.4), paper.grouped(1850.4),
+                                  paper.grouped(12345678)) == ("1.3 \u043c\u043b\u043d USDT", "23.8 \u0442\u044b\u0441. USDT", "950 USDT", "1 850", "12 345 678"))
+    s.check("share_text: one decimal, two below 0.1, then a floor",
+            [paper.share_text(x) for x in (0.125, 0.00145, 0.00034, 0.00004)] == ["12.5", "0.1", "0.03", "<0.01"])
+    s.check("a new whale's notice: its number beside the whale",
+            "\u043a\u0438\u0442 \U0001f40b{num} {addr} \u2014" in paper.N_ADDED and "\u2022" not in paper.N_ADDED)
     closed = dict(ep, t_close=t_open + (6 * 60 + 12) * 60000, px_close="82.10")
-    s.check("the close alert in gain after 6 h 12 min: green cross", paper.alert_close(closed, 1, rule) == (
+    s.check("the close signal in gain after 6 h 12 min: green cross", paper.alert_close(closed, 1, rule) == (
         head.replace("14:05", "20:17") + whale + "\u274e \u0417\u0430\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 82.10 \u00b7 \u0432 \u043f\u043e\u0437\u0438\u0446\u0438\u0438 \U0001f55a 6.2 \u0447."))
     s.check("a move inside the fee both ways is a loss: red cross",
             paper.alert_close(dict(closed, px_close="80.090"), 1, rule) == head.replace("14:05", "20:17") + whale + (
@@ -1588,25 +1634,59 @@ def section_w(s):
     s.check("held 45 min", paper.held_text(45 * 60000) == "45 \u043c\u0438\u043d")
     s.check("number: keycaps 1 to 9, then #10", paper.number(1) == "1\ufe0f\u20e3" and paper.number(9) == "9\ufe0f\u20e3"
             and paper.number(10) == "#10")
+    s.check("lev_text: both numbers, or n/a", paper.lev_text((7, 1.5)) == "7x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 1.5x)" and paper.lev_text(None) == "\u043d/\u0434")
     saved_info = paper.info
     try:
-        doc = {"marginSummary": {"accountValue": "1000000.0", "totalNtlPos": "3000000.0"},
-               "assetPositions": [{"type": "oneWay", "position": {"coin": "LIT", "szi": "10.0",
-                                                                  "leverage": {"type": "isolated", "value": 4}}}]}
-        paper.info = lambda body, limiter: doc if body == {"type": "clearinghouseState", "user": "0xa"} else None
-        s.check("read_leverage: the coin's setting and the account's notional over its value",
-                paper.read_leverage("0xa", "LIT", None) == (4, 3.0))
-        s.check("read_leverage: a coin with no position is None", paper.read_leverage("0xa", "BTC", None) is None)
-        paper.info = lambda body, limiter: {"assetPositions": doc["assetPositions"]}
-        s.check("read_leverage: an answer without marginSummary is None", paper.read_leverage("0xa", "LIT", None) is None)
+        state_doc = {"marginSummary": {"accountValue": "1000000.0", "totalNtlPos": "3000000.0"},
+                     "assetPositions": [{"type": "oneWay", "position": {"coin": "LIT", "szi": "10.0", "entryPx": "3.10",
+                                                                        "positionValue": "31.0",
+                                                                        "leverage": {"type": "isolated", "value": 4}}}]}
+
+        def order(coin, side, kind, px, ro, trig, oid, children=()):
+            return {"coin": coin, "side": side, "orderType": kind, "limitPx": "0.0" if trig else px, "oid": oid,
+                    "triggerPx": px if trig else "0.0", "isTrigger": trig, "reduceOnly": ro, "children": list(children)}
+        waiting = order("LIT", "A", "Stop Market", "2.7", True, True, 8)
+        orders = [order("LIT", "A", "Stop Market", "2.9", True, True, 1),
+                  order("LIT", "A", "Take Profit Market", "3.6", True, True, 2), order("LIT", "A", "Limit", "3.5", True, False, 3),
+                  order("LIT", "A", "Limit", "3.7", False, False, 4), order("LIT", "B", "Limit", "3.0", True, False, 5),
+                  order("BTC", "A", "Limit", "99000.0", True, False, 6), order("LIT", "B", "Limit", "3.05", False, False, 7, [waiting]),
+                  waiting, order("LIT", "A", "Stop Market", "2.95", True, True, 9)]
+
+        def answers(body, limiter):
+            return {"clearinghouseState": state_doc, "frontendOpenOrders": orders}[body["type"]]
+        paper.info = answers
+        want = {"side": 1, "lev": (4, 3.0), "entry": "3.10", "value": 31.0, "share": 31.0 / 1000000.0,
+                "stops": ["2.95", "2.9"], "targets": ["3.5", "3.6"]}
+        s.check("read_whale: the position, and the closing side's stops and targets in trigger order; an opening order "
+                "and one waiting on a resting parent out", paper.read_whale("0xa", "LIT", None) == want)
+        short_doc = json.loads(json.dumps(state_doc))
+        short_doc["assetPositions"][0]["position"]["szi"] = "-10.0"
+        short_orders = [order("LIT", "B", "Stop Market", "3.4", True, True, 11),
+                        order("LIT", "B", "Take Profit Market", "2.8", True, True, 12),
+                        order("LIT", "B", "Limit", "2.9", True, False, 13), order("LIT", "B", "Stop Market", "3.3", True, True, 14),
+                        order("LIT", "A", "Limit", "3.6", True, False, 15)]
+        paper.info = lambda body, limiter: {"clearinghouseState": short_doc, "frontendOpenOrders": short_orders}[body["type"]]
+        s.check("read_whale: a short's exits on the buying side, in trigger order",
+                paper.read_whale("0xa", "LIT", None) == dict(want, side=-1, stops=["3.3", "3.4"], targets=["2.9", "2.8"]))
+
+        def orders_refused(body, limiter):
+            if body["type"] == "frontendOpenOrders":
+                raise paper.Transport("HTTP 429")
+            return state_doc
+        paper.info = orders_refused
+        s.check("read_whale: open orders refused, the position kept and its exits None",
+                paper.read_whale("0xa", "LIT", None) == dict(want, stops=None, targets=None))
+        paper.info = answers
+        s.check("read_whale: a coin with no position is None", paper.read_whale("0xa", "BTC", None) is None)
+        paper.info = lambda body, limiter: {"assetPositions": state_doc["assetPositions"]}
+        s.check("read_whale: an answer without marginSummary is None", paper.read_whale("0xa", "LIT", None) is None)
 
         def refused(body, limiter):
             raise paper.Transport("HTTP 429")
         paper.info = refused
-        s.check("read_leverage: a refused read is None, never raised", paper.read_leverage("0xa", "LIT", None) is None)
+        s.check("read_whale: a refused read is None, never raised", paper.read_whale("0xa", "LIT", None) is None)
     finally:
         paper.info = saved_info
-    s.check("lev_text: both numbers, or n/a", paper.lev_text((7, 1.5)) == "7x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 1.5x)" and paper.lev_text(None) == "\u043d/\u0434")
     # W12. the constants cut from index.html
     page = "var INV_FLOOR_SD = 2.0;   // x\nvar FEE_TAKER   = 0.0005;\n"
     s.check("cut_number on a page", common.cut_number(page, "INV_FLOOR_SD") == 2.0
@@ -1624,6 +1704,16 @@ def section_w(s):
     s.check("load_rule reads owner.json's capital and medium risk",
             rule_live["capital_usdt"] == float(owner["capital"]["usdt"])
             and rule_live["risk_pct"] == float(owner["risk"]["risk_pct_medium"]))
+    empty = tempfile.mkdtemp(prefix="vps-selftest-owner.")
+    try:
+        s.check("owner_book: the owner file's capital, medium risk and side and book ceilings; owner_now None without it",
+                paper.owner_book(REPO) == {"capital_usdt": float(owner["capital"]["usdt"]),
+                                           "risk_pct": float(owner["risk"]["risk_pct_medium"]),
+                                           "side_max_pct": float(owner["risk"]["side_max_pct"]),
+                                           "book_max_pct": float(owner["risk"]["book_max_pct"])}
+                and paper.owner_now(empty) is None)
+    finally:
+        shutil.rmtree(empty, ignore_errors=True)
     s.check("load_rule cuts two positive numbers from index.html",
             rule_live["inv_floor_sd"] > 0 and 0 < rule_live["fee_taker"] < 0.01)
     # W13. the unit and the manifest
@@ -1705,18 +1795,38 @@ def section_w_flow(s):
         for name in alerts:
             with open(os.path.join(outbox, name), encoding="utf-8") as fh:
                 texts.append(json.load(fh)["text"])
-        s.check("the flow's open alert: whale 1, no leverage without a reader", len(texts) == 2
-                and "1\ufe0f\u20e3 \U0001f40b\u2022 " in texts[0] and "\u043f\u043b\u0435\u0447\u043e \u043d/\u0434" in texts[0])
+        s.check("the flow's open signal: whale 1, no leverage without a reader", len(texts) == 2
+                and "\U0001f40b1\ufe0f\u20e3 " in texts[0] and "\u043f\u043b\u0435\u0447\u043e \u043d/\u0434" in texts[0])
         s.check("the flow's close at the opening price: red cross", len(texts) == 2 and "\u274c \u0417\u0430\u043a\u0440\u044b\u043b" in texts[1])
         asked, lone = [], paper.new_state(sel)
         paper._apply(p, lone["accounts"][p], [w_fill(ff + h, 0, "B", 1, tid=1)], sel, {"BTCUSDT"}, ff + h + 10000,
-                     rule, lambda: inputs, lambda coin: asked.append(coin) or (7, 1.5))
+                     rule, lambda: inputs, lambda coin: asked.append(coin) or {"side": 1, "lev": (7, 1.5), "entry": "100.0",
+                                                                               "value": 25000.0, "share": 0.02, "stops": [],
+                                                                               "targets": []})
         fresh = sorted(x for x in os.listdir(outbox) if "-alert-" in x and x not in alerts)
         with open(os.path.join(outbox, fresh[-1]), encoding="utf-8") as fh:
             lone_text = json.load(fh)["text"]
         s.check("_apply asks the reader for the fill's coin and prints its answer",
                 asked == ["BTC"] and "\u043f\u043b\u0435\u0447\u043e 7x (\u0432\u0435\u0441\u044c \u0441\u0447\u0451\u0442 1.5x)" in lone_text)
-        for name in fresh:
+        mine = paper.new_state(sel)["accounts"][p]
+        mine["coins"]["ETH"] = {"coin": "ETH", "symbol": "ETHUSDT", "side": 1, "t_open": ff, "px_open": "2000.0", "n": 1}
+        before = set(os.listdir(outbox))
+        paper._apply(p, mine, [w_fill(ff + h, 0, "B", 1, tid=6)], sel, {"BTCUSDT"}, ff + h + 70000, rule, lambda: inputs,
+                     lambda coin: None, lambda: {"capital_usdt": 30000.0, "risk_pct": 0.5, "side_max_pct": 3.0,
+                                                 "book_max_pct": 5.0}, [1, -1])
+        made = sorted(set(os.listdir(outbox)) - before)
+        with open(os.path.join(outbox, made[-1]), encoding="utf-8") as fh:
+            counted = json.load(fh)["text"]
+        s.check("the copy line counts the account's open episodes, this one and the other picks'",
+                len(made) == 1 and counted.endswith("LONG: 3-\u044f \u0438\u0437 6"))
+        asked = []
+        paper._apply(p, paper.new_state(sel)["accounts"][p], [w_fill(ff + h, 0, "B", 1, tid=2), w_fill(ff + h + 60000, 1, "A", 1, tid=3)],
+                     sel, {"BTCUSDT"}, ff + h + 70000, rule, lambda: inputs, lambda coin: asked.append(coin))
+        s.check("closed later in the same poll: the signal reads no position", asked == [])
+        paper._apply(p, paper.new_state(sel)["accounts"][p], [w_fill(ff + h, 0, "B", 1, tid=4), w_fill(ff + h + 60000, 1, "B", 1, tid=5)],
+                     sel, {"BTCUSDT"}, ff + h + 70000, rule, lambda: inputs, lambda coin: asked.append(coin))
+        s.check("added to later in the same poll: the signal reads the position", asked == ["BTC"])
+        for name in [x for x in os.listdir(outbox) if "-alert-" in x and x not in alerts]:
             os.remove(os.path.join(outbox, name))
         for acct in state["accounts"].values():
             acct["polled_ms"] = we + paper.DAY_SETTLE_S * 1000
@@ -2534,7 +2644,7 @@ def section_w_rescan(s):
             note = json.load(fh)
         end = datetime.fromtimestamp(sel["window_end_ms"] / 1000, tz=announce.TBILISI).strftime("%d.%m.%Y")
         s.check("the notice of a whale added, character for character",
-                note["kind"] == "notice" and note["text"] == "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442: \u043d\u043e\u0432\u044b\u0439 \u043a\u0438\u0442 3\ufe0f\u20e3 \U0001f40b\u2022 0xcccc\u2026cccc \u2014 \u043f\u0440\u043e\u0448\u0451\u043b \u0442\u043e \u0436\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u0431\u043e\u0440\u0430 \u043d\u0430 07.01.2026, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u0434\u043e " + end + ".")
+                note["kind"] == "notice" and note["text"] == "\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442: \u043d\u043e\u0432\u044b\u0439 \u043a\u0438\u0442 \U0001f40b3\ufe0f\u20e3 0xcccc\u2026cccc \u2014 \u043f\u0440\u043e\u0448\u0451\u043b \u0442\u043e \u0436\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u0431\u043e\u0440\u0430 \u043d\u0430 07.01.2026, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u0434\u043e " + end + ".")
         none = paper.new_state(sel)
         paper.adopt(none, tmp, sel, dict(found, t0_ms=W_T0 + 28 * paper.DAY_MS, picks=[]), 2, now)
         with open(os.path.join(outbox, sorted(os.listdir(outbox))[-1]), encoding="utf-8") as fh:
```
