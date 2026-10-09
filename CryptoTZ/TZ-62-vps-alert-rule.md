# TZ-62 — On the VPS: the alert rule — no promotion reaches the owner; new coins, list coins and contract notices do

**Canonical filename:** `CryptoTZ/TZ-62-vps-alert-rule.md`
**Report:** `CryptoReports/TZ-62-vps-alert-rule-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the announcement stream. **A0 stops
BLOCKED on any other machine, before the gate and before any other work.**
**Class:** branch TZ (contract §8) — it modifies two files under `vps/**`.
**Branch:** `tz-62-vps-alert-rule` · **Model:** Opus
**Previous TZ:** TZ-61, COMPLETED, report-only — no branch; its report is on `main` (`0e96f3f`).
**Written against:** contract v26, map `2026-10-09-a`, methodology `2026-10-08-a`, and `main` at `450e12a`
— its `vps` tree `81c33f881d4728eda33444e7840ecf9110d616d3` — read by the Architect from the repository on
09.10.2026. Map §10 row «The owner's alert channel carries promotions and misses contract notices», with
the decision of `2026-10-09-a`, is what this TZ executes.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-09-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-09-a.**` |
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
| `EXECUTOR-INSTRUCTIONS.md` | 991 | `d7bd23785656896a119e0cb7f0fddad5` | its version line reads `**Version 26.**` — a lower version is BLOCKED (inv. 59); lines and MD5 reported |
| `vps/announce.py` | 405 | `cb4f9dfc6e3a428283652c4d21468af5` | reported; a different file is a finding, never a block |
| `vps/selftest.py` | 1022 | `40b6a609bbbc3e75acca7614c4241b7a` | reported; as above |
| `vps/common.py` | 364 | `62e3e688cfce21e3e9887e057e461fef` | reported; as above |

The map itself: 3308 lines, MD5 `aff11ff251052fc6dde514070bef2c3a` — reported, not enforced. The tree `origin/main:vps`
is reported beside them; `81c33f881d4728eda33444e7840ecf9110d616d3` is the one this TZ was written against,
and a different one is a finding, never a block.

---

## 1. Credentials

None arrives, none is read and none is written. **No model session is opened, the `claude` binary is not
run, and no connection to Binance or to Telegram is opened:** the code under change is exercised offline by
the selftest, and the stream's record is read from its file.

---

## 2. Contract, map and code text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section or file named.

> Code under `vps/` runs on the VPS only from `main`: the deployer fast-forwards its own clone and installs what changed, and nothing else installs anything.

— contract §7 item 15. The merge installs the rule; this session restarts nothing.

> **No value is ever printed, logged, committed or quoted**

— contract §7 item 6. This TZ reads no credential; the rule is quoted because the record it reads holds
each article's text, which is never printed either (§6 rule 4).

> a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work

— map §10, row «The assistant's build sequence».

> the promotions catalogue (`catalogId` 93, «Latest Activities») and wallet maintenance (157, «Maintenance Updates») never alert

> **Every pattern is case-sensitive**, because Binance writes headlines in Title Case and tickers in capitals

> **What reaches him stays the exchange's own publication:** the record is untouched, the run the button starts still reads all of it (methodology §6a), and A1's text is unchanged but for the appended contracts.

— map §10, row «The owner's alert channel carries promotions and misses contract notices», which states
the whole rule §12.2 implements.

> **The exchange's own publications are read on EVERY run, first, in two reads, and neither is cached**

— `ANALYST-INSTRUCTIONS.md` §6a. The engine reads the record whatever the alert rule decides.

> A list match → A1; a perpetual match in a listing catalogue → A1; anything else is recorded only.

— `vps/announce.py`, the docstring of `act` — the rule this TZ replaces.

> A negative control names which items must FLIP and which must NOT.

— map inv. 68. V1's three controls name both.

> A check that passes with no data is forbidden.

— map inv. 22. §12.5's script exits 2 on an empty input.

---

## 3. What is built and what is read

**The owner's request of 09.10.2026**, sent with his screenshot of the alert of 08.10 «⚡ Binance · 13:00
Тбилиси · Latest Activities: MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers»: useless information
in the form of promotions must strictly be removed, and what bears on the strategy on Binance Futures, or on
a candidate for his spot portfolio, must reach him. **The rule quoted last in §2 is the defect.** BNB is a
name of `tokens[]` and the currency of Binance's rewards, so both alerts known to have reached him from the
stream were promotions — TZ-61's K3 on 07.10 and the screenshot of 08.10 — while a Futures notice that names
its contracts only in its body can never alert.

**Built:** `announce.alert_rule`, a pure function of one record that decides by the catalogue and the kind of
notice before the ticker (§12.2), and `announce.act` deciding through it and appending to A1 the list
contracts a contract notice's body names (§12.3); the selftest gains section T (§12.4). **Read on the VPS,
with the branch's code and no write:** the rule replayed on the stream's whole record (§12.5, C1), beside
the old rule's alert count from the stream's own journal (C2), and the exchange watcher's contract types
(C3).

---

## 4. Scope

### Files to Modify

```
vps/announce.py    vps/selftest.py
```

### Files to Create

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- the scratch directory `/root/tz62`, mode `0700`, holding §12.5's script, and gone at the end;
- reading, never writing: `/var/lib/crypto-auto/announcements.jsonl` — through §12.5's script alone, which
  prints no record's `body`; `/var/lib/crypto-auto/perpetuals.json`; `/var/lib/crypto-auto/exchange-snapshot.json`;
  `/var/lib/crypto-auto/deployed-vps-tree`; the journal of `crypto-announce.service`; `systemctl` state.

**No unit is started, stopped, restarted, enabled or disabled — `crypto-announce.service` included: the
deployer installs the merge (§2). No run is started, requested or stopped, and nothing under
`/etc/crypto-auto/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or
`/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The record and the stream.** `record`, the key check, the subscription and the journal's `announce: data` line do not move, and the run the button starts reads the whole record as before (§2).
- **The matcher.** `match_title` and selftest section G do not move.
- **The alert texts.** `common.A1`–`A4` do not move; A1 gains the appended contracts only on a contract
  notice (§12.3).
- **`vps/exchange.py`.** A2, A3 and A4 do not move. C3 reads its snapshot; the map decides on the reading.
- **An alert on a funding level, on order-book depth or on an unlock** — not alerts, each for the reason the
  map's row states.
- **Installing the change** — the deployer does it after the merge, behind the selftest (§2).

---

## 6. Rules — binding in every stage

1. **No model session**, and the `claude` binary is not run.
2. **No unit changes state** because of this session: `systemctl` and `journalctl` are used to read.
3. **The session's own network reads are `git`'s and `gh`'s, and nothing else.**
4. **A record's `body` is never printed** — not by §12.5's script and not by any command of the session. A
   `title` is the exchange's own public headline and is printed in full.
5. **Python 3.12's standard library and bash only.**
6. **Time is UTC everywhere;** every `journalctl` runs under `TZ=UTC` and every `--since` names `UTC`.
7. **§12's blocks are copied byte for byte, never retyped:** each block is the lines between its opening
   fence and the next closing fence, each ending in a newline. §12.2–§12.5 are ASCII only; a non-ASCII
   character inside a string literal is written as the escape `vps/common.py` uses for its Russian strings.

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`;
  `test -d /srv/crypto-auto/.git && echo clone`; `id -u cryptorun`. **Known answers:** `vultr`; `active`
  twice; `clone`; `995`. **Derived:** TZ-61's report read exactly these on this host at
  2026-10-07T22:28:24Z. **Any other answer: BLOCKED.** The session writes a report carrying A0's lines and its own `hostname`, commits it to
  `main`, and does nothing else (map §10, quoted in §2).
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/main:vps` and `cat /var/lib/crypto-auto/deployed-vps-tree`. **Known answer:**
     both `81c33f881d4728eda33444e7840ecf9110d616d3`. **Derived:** `git rev-parse 6e58aea:vps` returns it,
     `git log --oneline 6e58aea..450e12a -- vps/` lists no commit, and TZ-61 read the marker equal to it. A
     different value is a finding, never a block.
  2. On `origin/main`, `grep -c -F` of each line §12.1 edits at: `def act(data, cls, ticker):` and
     `                outcome = act(data, cls, ticker)` and the line beginning `# --- the stream ---` in
     `vps/announce.py`; `SECTIONS = (("A", section_a),` and `("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s))` in `vps/selftest.py`. **Known answer:** `1` each. **Derived:** the
     Architect's session counted each at `450e12a`. **Any other count: BLOCKED** — §12 is written against
     those lines.
  3. `systemctl show crypto-announce.service -p ActiveState -p NRestarts -p ExecMainPID` and
     `systemctl list-unit-files 'crypto-*' --no-pager` — the values V4 compares. Not registered.
  4. `python3 vps/selftest.py` on the branch before any edit. **Known answer:** exit 0 and `selftest: sections 19 checks 257 failed 0 empty 0`. **Derived:** TZ-60's report
     printed exactly that line from this host for its implementation commit `c019a5b`, whose `vps/` is
     `origin/main`'s (`git diff --stat c019a5b 450e12a -- vps/` is empty), and the Architect's session read
     the same line at `450e12a`.

---

## 8. Stage B — the code, on the branch

### B1. `vps/announce.py` — §12.1, §12.2 and §12.3

### B2. `vps/selftest.py` — §12.1 and §12.4

**Known answers after both:** `md5sum vps/announce.py` → `4f8724e2ce801470d1a071cb2429cbfe` and `wc -l` → `452`;
`md5sum vps/selftest.py` → `53045fb9aafcf1c26252a4f76da2babe` and `wc -l` → `1107`. **Derived:** the Architect's session
applied §12.1–§12.4 to both files at `450e12a` and read these. A different MD5 is a finding: the report
prints `git diff --stat` and every hunk that differs from §12, and V1 still runs.

---

## 9. Stage C — on the VPS, on the branch's code, read-only

- **C0.** `install -d -m 0700 /root/tz62`, then §12.5's block written to `/root/tz62/tz62_replay.py` and
  checked with `md5sum` → **`eb12746c5624da302e762c3811db1a4d`** and `wc -l` → **78**. **A different MD5 is BLOCKED for
  C1:** the file is not the dictated program.
- **C1. The rule on the record.** From the branch checkout's root: `python3 -I /root/tz62/tz62_replay.py "$PWD/vps" /var/lib/crypto-auto/announcements.jsonl /var/lib/crypto-auto/perpetuals.json`, its exit code,
  and its output printed in full in the report. **Known answers:**
  - **K1:** the twelve records of TZ-61's table, by `publishDate`: `2026-10-05T02:00:01Z`, `03:00:01Z`,
    `09:00:01Z`, `2026-10-06T01:00:00Z`, `09:00:02Z` and `2026-10-07T09:00:08Z` read `93`, `Latest Activities`, reason `catalogue`; `2026-10-07T08:00:04Z` reads `157`, `Maintenance Updates`,
    `catalogue`; `2026-10-06T05:00:01Z`, `06:15:28Z`, `2026-10-07T03:00:06Z` and `04:00:08Z` read
    `non-crypto`; `2026-10-06T09:30:01Z` reads `noise`. Every one of the twelve is `record`. **Derived:**
    TZ-61's report printed each record's `catalogId`, `catalogName` and title, and the Architect's session
    ran §12.2 on exactly those as §12.4's rows 1–12. These reasons rest on the catalogue and the title
    alone, so the perpetual list on the day of the reading cannot move them.
  - **K2:** one record titled `MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers`, its
    `publishDate` inside [2026-10-08T09:00:00Z, 09:01:00Z): `93`, `Latest Activities`, `catalogue`,
    `record`. **Derived:** the owner's screenshot prints `common.A1`, whose catalogue is the record's
    `catalogName` and whose time is its `publishDate` in Tbilisi, 13:00; the engine's day log of 08.10
    (`analyst/log/2026-10-08.md`, line 167) dates it 08.10 09:00; every `Latest Activities` record TZ-61
    printed carries `catalogId` 93. Another id is a finding: the reason is then `noise` and the decision
    still `record` (§12.4, row 15).
  - **K3:** `records` at least 18 and `unparseable` 0. **Derived:** the same day log read the file at 18
    lines at 19:02:10Z; `vps/cleanup.py` drops a record only 30 days after its `publishDate`; TZ-61 read 0
    unparseable.
  - **K4:** the census line for `Latest Activities` reads `catalogue 93 Latest Activities: <n>`, and no
    other census line names `Latest Activities`. **Derived:** TZ-61's six rows of that name carry `93`. A
    second id beside that name is a finding, because `SILENT_CATALOGS` reads the id.

  **Not registered:** every other row, and the count of alerts — they are what this reading exists to read.
  Each row whose decision is `alert` is named in the report's `## Implementation Summary` with its title,
  its reason and its contracts.
- **C2. The old rule over the same record.** `TZ=UTC journalctl -u crypto-announce.service --since '2026-10-03 20:37:17 UTC' -o cat --no-pager | grep -c ' alerted lag_ms='`. **Known answer:** at least 2.
  **Derived:** the service logs `announce: data catalogId=%s match=%s %s lag_ms=%s` after each record, the
  outcome `alerted` or `recorded`; TZ-61 read one `alerted` record, K3 of 07.10, and the owner's screenshot
  shows the alert of 08.10.
- **C3. The exchange watcher's contract types.** This command, its output in full:

```
python3 -I -c 'import json, sys, collections; s = json.load(open(sys.argv[1]))["symbols"]; print("usdt symbols", len(s)); [print("type", t, n) for t, n in sorted(collections.Counter(str(v[1]) for v in s.values()).items())]; [print("onboard", k, s[k][0], s[k][1], s[k][3]) for k in sorted(s) if isinstance(s[k][3], int) and s[k][3] >= 1791244800000]' /var/lib/crypto-auto/exchange-snapshot.json
```

  One line, so no indentation reaches Python. **Not registered.** **Derived:** `exchange.snapshot` stores
  `[status, contractType, deliveryDate, onboardDate]` per USDT symbol; `exchange.changes` and `exchange.act`
  send A2 only for a new symbol of type `PERPETUAL` off the list; `1791244800000` is 2026-10-06T00:00:00Z,
  the day of the TradFi notice in TZ-61's row 6. **Probed:** the Architect's session ran the line on a
  five-symbol snapshot of that shape and read the counts per type and the two symbols onboarded after that
  instant.
- **C4. Nothing left.** `rm -rf /root/tz62`, then `test ! -e /root/tz62 && echo gone`. **Known answer:**
  `gone`.

---

## 10. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0, `selftest: sections 20 checks 296 failed 0 empty 0`, and `section T: checks 39 failed 0`. **Derived:** A1.4's 257 checks plus section T's
  39 — §12.4's 32 rows and its 7 `act()` checks — read by the Architect's session on §12's files. **Negative
  controls** (inv. 68), each applied to `vps/announce.py` alone, then reverted, its MD5 restored and V1 green
  again:
  1. `SILENT_CATALOGS = ("93", "157")` → `SILENT_CATALOGS = ()`: exit non-zero, and **exactly 10** checks of
     section T fail — rows 1, 2, 3, 4, 7, 11, 12, 13, 21 and 31 of §12.4, every `catalogue` row.
  2. `    if NOISE.search(title):` → `    if False:`: **exactly 5** fail — rows 8, 14, 15, 30 and 32, every
     `noise` row.
  3. `        symbols = [symbol for _ticker, symbol in list_pairs if _word(symbol).search(body)]` →
     `        symbols = []`: **exactly 4** fail — rows 26 and 28 and the two `act()` checks on the funding
     notice.

  In each, every other check of section T and all nineteen other sections stay green. **Derived:** the
  Architect's session ran all three on §12's files and read exactly these partitions.
- **V2. Syntax.** `python3 -m py_compile vps/announce.py vps/selftest.py`.
- **V3. Scope.** `git diff --name-only origin/main...HEAD` lists exactly the two files of §4.
- **V4. Nothing touched.** After C, `systemctl show crypto-announce.service -p NRestarts -p ExecMainPID`
  equals A1.3's, and `systemctl list-unit-files 'crypto-*' --no-pager` equals A1.3's.
- **V5. Pushes.** The branch pushed and a pull request opened (or contract §8's fallback); `main` receives
  nothing from this session but its report.

No regression: every section of `vps/selftest.py` at `origin/main` stays green with its own checks
unchanged; section T is the only new one.

---

## 11. The report

Contract §10's template. **The first five lines after `## Status`:**

1. **The rule** — built, V1's total, section T's count, and the three controls' partitions.
2. **The replay** — C1's `records`, its `alerts N of M` line and its count per reason.
3. **The known answers** — K1 to K4, each met or not.
4. **Old against new** — C2's count of alerts the old rule sent beside C1's count of alerts the rule would
   send over the same record.
5. **The contract types** — C3's type counts, and every symbol onboarded since 2026-10-06 with its type.

---

## 12. Dictated blocks

### 12.1 What moves, exactly

**`vps/announce.py` — five edits; nothing else in the file moves.**

1. In the module docstring's first line, `(TZ-54 B6, TZ-56 B3, TZ-57 B2)` becomes `(TZ-54 B6, TZ-56 B3, TZ-57 B2, TZ-62 B1)`.
2. The docstring's two lines beginning `Alerts only (TZ-57): a matched announcement` become the four lines of
   block A.
3. §12.2's block is inserted directly before the line beginning `# --- the stream ---`, so that
   `perpetual_pairs` is followed by its two blank lines, the block, and that line.
4. The function `act` is replaced whole by §12.3's block; two blank lines stay before `def main`.
5. In `main`, `outcome = act(data, cls, ticker)` becomes `outcome = act(data, cls, ticker, list_tickers)`.

Block A:

```
Alerts only (TZ-57), by the alert rule (TZ-62): a promotion, a maintenance notice or
a non-crypto listing never reaches the owner; a new coin, a list coin, a perpetual's
listing or delisting, or a contract notice on a list contract does, and he decides
whether to press the button; this program requests no run.
```

**`vps/selftest.py` — three edits; nothing else in the file moves.**

1. The docstring's first three lines become the three lines of block B.
2. §12.4's block is inserted directly before the line beginning `SECTIONS = (("A", section_a),`, after the
   two blank lines that close section S.
3. The last line of `SECTIONS`, the one ending `("S", section_s))`, becomes the two lines of block C.

Block B:

```
"""The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
TZ-62 B2): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's, TZ-57 §12.8's,
TZ-58 §12.7's, TZ-60 §12.11's and TZ-62 §12.4's changed and new ones, each printing `section <X>:
```

Block C:

```
            ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
            ("T", section_t))
```

### 12.2 `announce.alert_rule` — inserted before the stream section

```python
# --- TZ-62 section 12.2: the alert rule -------------------------------------------
# Case-sensitive throughout: Binance writes its headlines in Title Case and its tickers
# in capitals, so "Win" is a promotion's word and "WIN" a coin's ticker.
SILENT_CATALOGS = ("93", "157")          # catalogId as text: Latest Activities, Maintenance Updates
NEW_COIN_CATALOG = "48"                  # New Cryptocurrency Listing
NON_CRYPTO = re.compile(r"\bbStocks\b|\bTradFi\b|\bTokenized Securities\b|\bStocks?\b")
NEW_COIN = re.compile(r"\bWill List\b|^Introducing\b|\bWill Launch\b.*\bPerpetual\b")
NOISE = re.compile(r"\bRewards?\b|\bVouchers?\b|\bTournament\b|\bCompetition\b|\bCampaign\b|\bPrize\b"
                   r"|\bPromotion\b|\bWin\b|\bBonus\b|\bExclusive\b|\bAPR\b|\bSimple Earn\b|\bBinance Earn\b"
                   r"|\bBinance Alpha\b|\bPairs?\b|\bCollateral\b|\bQuarterly\b")
DELIST = re.compile(r"\bDelist|\bMonitoring Tag\b")
CONTRACT = re.compile(r"\bFutures\b|\bPerpetual\b")
CONTRACT_TERMS = re.compile(r"\bDelist|\bFunding\b|\bLeverage\b|\bMargin Tiers?\b|\bTick Size\b|\bPrice Protection\b")
ALERT_REASONS = ("new-coin", "list", "perpetual", "contract")


def alert_rule(data, cls, list_pairs):
    """(reason, symbols) for one record: the first rule below that applies. A reason in
    ALERT_REASONS alerts and any other is recorded only; symbols are the list contracts
    a contract notice's body names, else []. Reads the record and nothing else."""
    catalog_id = str(data.get("catalogId"))
    title = str(data.get("title") or "")
    if catalog_id in SILENT_CATALOGS:
        return "catalogue", []
    if NON_CRYPTO.search(title):
        return "non-crypto", []
    if catalog_id == NEW_COIN_CATALOG and NEW_COIN.search(title):
        return "new-coin", []
    if NOISE.search(title):
        return "noise", []
    if cls == "list":
        return "list", []
    if cls == "perpetual" and ("listing" in str(data.get("catalogName") or "").lower() or DELIST.search(title)):
        return "perpetual", []
    if CONTRACT.search(title) and CONTRACT_TERMS.search(title):
        body = str(data.get("body") or "")
        symbols = [symbol for _ticker, symbol in list_pairs if _word(symbol).search(body)]
        if symbols:
            return "contract", symbols
    return "none", []


```

**Derivations — every pattern, and where it was read.** «The channel» is Binance's English announcement
channel, read by the Architect's session at 2026-10-08T20:26Z with
`curl -sS -m 20 https://t.me/s/binance_announcements` — HTTP 200, 134 429 bytes, MD5 `ae286b3a33439b183962bf2364b6752d`,
`https://t.me/robots.txt` 404 — posts 9012 to 9032 with 9018 absent from the page, each title cut as TZ-61
§12.1 cuts it.

| Name | Derived from |
|---|---|
| `SILENT_CATALOGS` `93` | TZ-61's rows 1–4, 7 and 12 — all `93` — and the screenshot of 08.10: every record of «Latest Activities» whose title is known is a promotion |
| `SILENT_CATALOGS` `157` | TZ-61's row 11, a completed token merge: wallet maintenance, which moves no Futures position |
| `NEW_COIN_CATALOG` `48` | TZ-61's rows 6, 9 and 10 carry `48` with `New Cryptocurrency Listing` |
| `NON_CRYPTO` | TZ-61's rows 4, 5, 6, 9 and 10, and the channel's posts 9012, 9017, 9021 and 9029 |
| `NEW_COIN` | TZ-54 §12.5's titles in section G — `Will List`, `Introducing … Launchpool`, `Will Launch … Perpetual` — and the HYPE listing of 24.09 (`analyst/log/2026-09-24-2.md`, line 231) |
| `NOISE`, the promotional words | every promotion title known: TZ-61's rows 1–4, 7 and 12, the screenshot, and the channel's posts 9013, 9014, 9015, 9016, 9017, 9019, 9020, 9022, 9024, 9030, 9031 and 9032 |
| `NOISE`, `Pairs?`, `Collateral` | TZ-61's rows 8, 9 and 10, and section G's `ARB/EUR` pair |
| `NOISE`, `Quarterly` | a quarterly contract is not a perpetual (`analyst/log/2026-09-25.md`, line 217) |
| `NOISE`, `Binance Alpha` | the channel's posts 9015, 9020 and 9031: Alpha is not a venue the owner trades |
| `DELIST` | section G's `Binance Will Delist Sonic (S)`, and the monitoring tag the engine's day log of 26.09 names (line 208) |
| `CONTRACT_TERMS` and the body read | the Futures delisting of 05.10 named its three contracts only in its article (`analyst/log/2026-10-04.md`, line 242); `Funding` and `Tick Size` are the owner's request — funding and the order book; `Price Protection` governs when a stop fires, and the board publishes stops (map §3.11); `Leverage` and `Margin Tiers` move the maintenance margin `index.html` holds at `LIQ_MMR = 0.0125` |
| case-sensitivity | Binance's titles in TZ-61's table and the channel are Title Case and their tickers capitals: `Win` is a promotion's word — the channel's post 9016 carries no other — and `WIN` a ticker (§12.4, row 24) |

### 12.3 `announce.act` — replaces the function whole

```python
def act(data, cls, ticker, list_pairs=()):
    """alert_rule decides (TZ-62): an alerting reason writes A1, with the list contracts
    a contract notice's body names appended; any other reason is recorded only. Alerts
    only: no run is requested (TZ-57)."""
    reason, symbols = alert_rule(data, cls, list_pairs)
    if reason not in ALERT_REASONS:
        return "recorded"
    hhmm = datetime.fromtimestamp(int(data.get("publishDate") or time.time() * 1000) / 1000,
                                  tz=TBILISI).strftime("%H:%M")
    text = common.A1.format(hhmm=hhmm, catalog_name=str(data.get("catalogName") or ""),
                            title=str(data.get("title") or ""))
    if symbols:
        text += " \u00b7 " + ", ".join(symbols)
    common.write_outbox("alert", text)
    return "alerted"
```

The separator is `common.A1`'s own middle dot, written as the same escape.

### 12.4 Selftest — section T, inserted before `SECTIONS`

```python
# --- T: the alert rule on the stream's records (TZ-62 section 12.4) ------------------
T_LA, T_LBN, T_NCL = "Latest Activities", "Latest Binance News", "New Cryptocurrency Listing"
T_PERPS = [("PEPE", "1000PEPEUSDT"), ("S", "SUSDT"), ("ZRO", "ZROUSDT"), ("STG", "STGUSDT"),
           ("MET", "METUSDT"), ("USDC", "USDCUSDT"), ("WIN", "WINUSDT")]
T_DELIST_MANY = "Binance Futures Will Delist Multiple USD\u24c8-M Perpetual Contracts (2026-10-05)"
T_FUNDING_MANY = "Binance Futures Will Adjust the Funding Rate Interval of Multiple USD\u24c8-M Perpetual Contracts (2026-10-10)"
T_PROMO_FUTURES = "Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards!"
T_PROMO_MET = "MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers"
# (catalogId, catalogName, title, body, reason, symbols). Rows 1-13 are the stream's own
# records: TZ-61's report, table "Records at or after T1", and the owner's screenshot of
# 08.10.2026; every other row's catalogue is the fixture's.
T_ROWS = (
    (93, T_LA, "Binance Lite Loan Promotion Extended: Enjoy Simple Borrowing with 50% Off Service Fee!", None, "catalogue", []),
    (93, T_LA, "Word of the Day: Test Your Knowledge on \u201cProactive Security Wins\u201d to Unlock USDC Rewards!", None, "catalogue", []),
    (93, T_LA, "Binance Pay Exclusive: Get up to 20% Off Mobile Top-Ups in Selected Regions!", None, "catalogue", []),
    (93, T_LA, "New User bStocks Convert Campaign: Join and Share a Reward Pool of Up to 110 SPCXB", None, "catalogue", []),
    (49, T_LBN, "Binance Will Support Marvell Technology (MRVL) and Oracle Corporation (ORCL) Cash Dividend Distribution via bStocks", None, "non-crypto", []),
    (48, T_NCL, "Binance Futures Will Launch Multiple TradFi USD\u24c8-Margined Perpetual Contracts (2026-10-06)", None, "non-crypto", []),
    (93, T_LA, "APAC Exclusive: Win a Fully Hosted Trip to Binance Blockchain Week 2026", None, "catalogue", []),
    (49, T_LBN, "Update on the Collateral Ratio Under Cross Margin and Portfolio Margin (2026-10-09)", None, "noise", []),
    (48, T_NCL, "Binance Exchange Adds JPMorgan Chase (JPMB), Eli Lilly (LLYB), Securitize Corp (SECZB) and StablecoinX Inc (USDEB) bStocks Trading Pairs on Binance Spot/Convert - 2026-10-07", None, "non-crypto", []),
    (48, T_NCL, "Binance Will Add 4 bStocks Tokenized Securities as Collateral Asset - 2026-10-07", None, "non-crypto", []),
    (157, "Maintenance Updates", "Binance Has Completed the Stargate Finance (STG) Token Merge to LayerZero (ZRO)", None, "catalogue", []),
    (93, T_LA, T_PROMO_FUTURES, None, "catalogue", []),
    (93, T_LA, T_PROMO_MET, None, "catalogue", []),
    (49, T_LBN, T_PROMO_FUTURES, None, "noise", []),
    (49, T_LBN, T_PROMO_MET, None, "noise", []),
    (48, T_NCL, "Binance Will List Hyperliquid (HYPE) with Seed Tag Applied", None, "new-coin", []),
    (48, T_NCL, "Introducing ETHFI on Binance Launchpool", None, "new-coin", []),
    (48, T_NCL, "Binance Futures Will Launch USD\u24c8-Margined SUIUSDT Perpetual Contract", None, "new-coin", []),
    (48, T_NCL, "Introducing Plasma (XPL) on Binance HODLer Airdrops! Earn XPL With Retroactive BNB Simple Earn Subscriptions", None, "new-coin", []),
    (48, T_NCL, "Binance Will List Bitcoin (BTC)", None, "new-coin", []),
    (93, T_LA, "Binance Will List Bitcoin (BTC)", None, "catalogue", []),
    (161, "Delisting", "Binance Will Delist Sonic (S)", None, "perpetual", []),
    (49, T_LBN, "Binance Will Extend Monitoring Tag to Include Sonic (S)", None, "perpetual", []),
    (49, T_LBN, "Binance Will Delist WIN on 2026-10-20", None, "perpetual", []),
    (49, T_LBN, "Binance Futures Will Update the Leverage and Margin Tiers of XRPUSDT Perpetual Contract (2026-10-10)", None, "list", []),
    (49, T_LBN, T_DELIST_MANY, "Positions in XRPUSDT will be closed at 2026-10-05 09:00 (UTC).", "contract", ["XRPUSDT"]),
    (49, T_LBN, T_DELIST_MANY, "PROMPTUSDT, PUMPBTCUSDT and 1000000BOBUSDT at 2026-10-05 09:00 (UTC).", "none", []),
    (49, T_LBN, T_FUNDING_MANY, "ENAUSDT and BTCUSDT will settle funding every 4 hours.", "contract", ["BTCUSDT", "ENAUSDT"]),
    (49, T_LBN, T_FUNDING_MANY, None, "none", []),
    (50, "New Fiat Listings", "Binance Adds ARB/EUR Trading Pair", None, "noise", []),
    (157, "Maintenance Updates", "Binance Will Support the BNB Smart Chain (BSC) Network Upgrade & Hard Fork", None, "catalogue", []),
    (48, T_NCL, "Binance Futures Will Launch USD\u24c8-M BTCUSDT Quarterly 1226 Futures Contract", None, "noise", []),
)


def section_t(s):
    lists = [("BTC", "BTCUSDT")] + [(row["name"], row["s"]) for row in checkout_tokens()]
    for cid, cname, title, body, reason, symbols in T_ROWS:
        cls, _ticker = announce.match_title(title, lists, T_PERPS)
        data = {"catalogId": cid, "catalogName": cname, "title": title, "body": body}
        s.check("%s %s -> %s" % (cid, title, reason), announce.alert_rule(data, cls, lists) == (reason, symbols))
    hhmm = datetime.fromtimestamp(1700000000, tz=announce.TBILISI).strftime("%H:%M")
    tmp = tempfile.mkdtemp(prefix="vps-selftest-t.")
    try:
        with spool_in(tmp, True) as paths:
            def alerts():
                return sorted(n for n in os.listdir(paths["OUTBOX_DIR"]) if "-alert-" in n)

            def text_of(name):
                with open(os.path.join(paths["OUTBOX_DIR"], name), encoding="utf-8") as fh:
                    return json.load(fh)["text"]

            promo = {"catalogId": 93, "catalogName": T_LA, "title": T_PROMO_MET, "publishDate": 1700000000000}
            s.check("act(): the promotion of 08.10 is recorded", announce.act(promo, "list", "BNB", lists) == "recorded")
            s.check("act(): no alert for it", alerts() == [])
            listing = {"catalogId": 48, "catalogName": T_NCL, "publishDate": 1700000000000,
                       "title": "Binance Will List Hyperliquid (HYPE) with Seed Tag Applied"}
            s.check("act(): a new coin alerts", announce.act(listing, "list", "HYPE", lists) == "alerted")
            first = alerts()
            s.check("act(): one alert, A1 exactly", len(first) == 1 and text_of(first[0]) == common.A1.format(
                hhmm=hhmm, catalog_name=T_NCL, title=listing["title"]))
            funding = {"catalogId": 49, "catalogName": T_LBN, "title": T_FUNDING_MANY, "publishDate": 1700000000000,
                       "body": "ENAUSDT and BTCUSDT will settle funding every 4 hours."}
            s.check("act(): a contract notice on list contracts alerts", announce.act(funding, "none", None, lists) == "alerted")
            second = [n for n in alerts() if n not in first]
            s.check("act(): A1 with the contracts appended", len(second) == 1 and text_of(second[0]) == common.A1.format(
                hhmm=hhmm, catalog_name=T_LBN, title=T_FUNDING_MANY) + " \u00b7 BTCUSDT, ENAUSDT")
            s.check("act(): no request", os.listdir(paths["REQUESTS_DIR"]) == [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


```

**The rows and their known answers.** Each reason is the first rule of §12.2 that applies, read by the
Architect's session on §12's files; rows 1–13 carry the stream's own catalogue and title, every other row's
catalogue is the fixture's.

| # | catalogId, catalogName | title | body | reason, contracts | source |
|---:|---|---|---|---|---|
| 1 | `93` Latest Activities | Binance Lite Loan Promotion Extended: Enjoy Simple Borrowing with 50% Off Service Fee! | — | `catalogue` | TZ-61 row 1 |
| 2 | `93` Latest Activities | Word of the Day: Test Your Knowledge on “Proactive Security Wins” to Unlock USDC Rewards! | — | `catalogue` | TZ-61 row 2 |
| 3 | `93` Latest Activities | Binance Pay Exclusive: Get up to 20% Off Mobile Top-Ups in Selected Regions! | — | `catalogue` | TZ-61 row 3 |
| 4 | `93` Latest Activities | New User bStocks Convert Campaign: Join and Share a Reward Pool of Up to 110 SPCXB | — | `catalogue` | TZ-61 row 4 |
| 5 | `49` Latest Binance News | Binance Will Support Marvell Technology (MRVL) and Oracle Corporation (ORCL) Cash Dividend Distribution via bStocks | — | `non-crypto` | TZ-61 row 5 |
| 6 | `48` New Cryptocurrency Listing | Binance Futures Will Launch Multiple TradFi USDⓈ-Margined Perpetual Contracts (2026-10-06) | — | `non-crypto` | TZ-61 row 6 |
| 7 | `93` Latest Activities | APAC Exclusive: Win a Fully Hosted Trip to Binance Blockchain Week 2026 | — | `catalogue` | TZ-61 row 7 |
| 8 | `49` Latest Binance News | Update on the Collateral Ratio Under Cross Margin and Portfolio Margin (2026-10-09) | — | `noise` | TZ-61 row 8 |
| 9 | `48` New Cryptocurrency Listing | Binance Exchange Adds JPMorgan Chase (JPMB), Eli Lilly (LLYB), Securitize Corp (SECZB) and StablecoinX Inc (USDEB) bStocks Trading Pairs on Binance Spot/Convert - 2026-10-07 | — | `non-crypto` | TZ-61 row 9 |
| 10 | `48` New Cryptocurrency Listing | Binance Will Add 4 bStocks Tokenized Securities as Collateral Asset - 2026-10-07 | — | `non-crypto` | TZ-61 row 10 |
| 11 | `157` Maintenance Updates | Binance Has Completed the Stargate Finance (STG) Token Merge to LayerZero (ZRO) | — | `catalogue` | TZ-61 row 11 |
| 12 | `93` Latest Activities | Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards! | — | `catalogue` | TZ-61 row 12 — K3 |
| 13 | `93` Latest Activities | MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers | — | `catalogue` | the owner's screenshot of 08.10 |
| 14 | `49` Latest Binance News | Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards! | — | `noise` | row 12's title outside its catalogue: the second line of defence |
| 15 | `49` Latest Binance News | MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers | — | `noise` | row 13's title outside its catalogue |
| 16 | `48` New Cryptocurrency Listing | Binance Will List Hyperliquid (HYPE) with Seed Tag Applied | — | `new-coin` | `analyst/log/2026-09-24-2.md`, line 231 |
| 17 | `48` New Cryptocurrency Listing | Introducing ETHFI on Binance Launchpool | — | `new-coin` | TZ-54 §12.5, section G |
| 18 | `48` New Cryptocurrency Listing | Binance Futures Will Launch USDⓈ-Margined SUIUSDT Perpetual Contract | — | `new-coin` | TZ-54 §12.5, section G |
| 19 | `48` New Cryptocurrency Listing | Introducing Plasma (XPL) on Binance HODLer Airdrops! Earn XPL With Retroactive BNB Simple Earn Subscriptions | — | `new-coin` | a HODLer Airdrops listing, BNB named as the subscription |
| 20 | `48` New Cryptocurrency Listing | Binance Will List Bitcoin (BTC) | — | `new-coin` | section P's message (TZ-57 §12.8) |
| 21 | `93` Latest Activities | Binance Will List Bitcoin (BTC) | — | `catalogue` | row 20 in the promotions catalogue: the catalogue decides first |
| 22 | `161` Delisting | Binance Will Delist Sonic (S) | — | `perpetual` | TZ-54 §12.5, section G |
| 23 | `49` Latest Binance News | Binance Will Extend Monitoring Tag to Include Sonic (S) | — | `perpetual` | the monitoring tag, `analyst/log/2026-09-26.md`, line 208 |
| 24 | `49` Latest Binance News | Binance Will Delist WIN on 2026-10-20 | — | `perpetual` | case: `WIN` is a ticker, not «Win» |
| 25 | `49` Latest Binance News | Binance Futures Will Update the Leverage and Margin Tiers of XRPUSDT Perpetual Contract (2026-10-10) | — | `list` | a margin-tier notice naming its contract in the title |
| 26 | `49` Latest Binance News | Binance Futures Will Delist Multiple USDⓈ-M Perpetual Contracts (2026-10-05) | Positions in XRPUSDT will be closed at 2026-10-05 09:00 (UTC). | `contract` `XRPUSDT` | `analyst/log/2026-10-04.md`, line 242 — the real title, a list contract in the body |
| 27 | `49` Latest Binance News | Binance Futures Will Delist Multiple USDⓈ-M Perpetual Contracts (2026-10-05) | PROMPTUSDT, PUMPBTCUSDT and 1000000BOBUSDT at 2026-10-05 09:00 (UTC). | `none` | the same title with the real article's three contracts — none on the list; A3 dates them |
| 28 | `49` Latest Binance News | Binance Futures Will Adjust the Funding Rate Interval of Multiple USDⓈ-M Perpetual Contracts (2026-10-10) | ENAUSDT and BTCUSDT will settle funding every 4 hours. | `contract` `BTCUSDT`, `ENAUSDT` | a funding notice naming two list contracts in its body; `list_pairs`' order, BTC first |
| 29 | `49` Latest Binance News | Binance Futures Will Adjust the Funding Rate Interval of Multiple USDⓈ-M Perpetual Contracts (2026-10-10) | — | `none` | the same title with no body |
| 30 | `50` New Fiat Listings | Binance Adds ARB/EUR Trading Pair | — | `noise` | TZ-54 §12.5, section G — a list coin in a pair notice |
| 31 | `157` Maintenance Updates | Binance Will Support the BNB Smart Chain (BSC) Network Upgrade & Hard Fork | — | `catalogue` | wallet maintenance naming BNB |
| 32 | `48` New Cryptocurrency Listing | Binance Futures Will Launch USDⓈ-M BTCUSDT Quarterly 1226 Futures Contract | — | `noise` | `analyst/log/2026-09-25.md`, line 217 — a quarterly contract is not a perpetual |

**The seven `act()` checks** run on `spool_in`'s temporary spool: the promotion of 08.10 returns `recorded`
and writes no alert; the HYPE listing returns `alerted` and writes one alert whose text equals `common.A1`
for it; the funding notice of row 28 returns `alerted` and writes one alert whose text equals `common.A1` for
it followed by the separator and `BTCUSDT, ENAUSDT`; and no run request is written. **Derived:** `act`'s
order in §12.3, and `common.write_outbox`'s file name, which carries `-alert-`.

### 12.5 The replay — `/root/tz62/tz62_replay.py`

The file is exactly the block's lines, each ending in a newline: 78 lines, ASCII only, MD5
`eb12746c5624da302e762c3811db1a4d`. **Probed:** the Architect's session ran it on a fixture of fifteen records — TZ-61's twelve,
the record of 08.10 and two that alert, each with a planted `body` — plus one unparseable line, against §12's
`vps/announce.py`: it printed `records 15, unparseable 1`, every reason K1 and K2 register, `alerts 2 of 15`
and none of the planted bodies; on an empty file it printed `EMPTY INPUT` and exited 2.

```python
#!/usr/bin/env python3
"""TZ-62 section 12.5: the alert rule on the stream's own record.

    python3 -I tz62_replay.py <vps dir> <announcements.jsonl> <perpetuals.json>

Imports announce from <vps dir>, reads the two files, writes nothing and prints one row
per record, then the records per catalogue and the decisions per reason. Every record's
body is read by the rule and none is printed."""
import json
import sys
from datetime import datetime, timezone

sys.path.insert(0, sys.argv[1])
import announce  # noqa: E402


def utc(ms):
    if not isinstance(ms, int):
        return "-"
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def cell(text):
    return " ".join(str(text).split()).replace("|", "\\|")


def main(argv):
    lists = announce.list_pairs()
    with open(argv[3], encoding="utf-8") as fh:
        perps = [(row["base"], row["symbol"]) for row in json.load(fh) if row.get("base")]
    records, bad = [], 0
    with open(argv[2], encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            try:
                doc = json.loads(raw)
            except ValueError:
                bad += 1
                continue
            if isinstance(doc, dict):
                records.append(doc)
            else:
                bad += 1
    print("records %d, unparseable %d, list pairs %d, perpetual pairs %d"
          % (len(records), bad, len(lists), len(perps)))
    if not records or not lists or not perps:
        print("EMPTY INPUT")
        return 2
    print("\n| # | publishDate | catalogId | catalogName | title | match | reason | decision | contracts |")
    print("|---:|---|---|---|---|---|---|---|---|")
    tally = {}
    for i, rec in enumerate(records, 1):
        title = str(rec.get("title") or "")
        cls, ticker = announce.match_title(title, lists, perps)
        reason, symbols = announce.alert_rule(rec, cls, lists)
        decision = "alert" if reason in announce.ALERT_REASONS else "record"
        tally[(decision, reason)] = tally.get((decision, reason), 0) + 1
        print("| %d | %s | %s | %s | %s | %s | %s | %s | %s |"
              % (i, utc(rec.get("publishDate")), rec.get("catalogId"), cell(rec.get("catalogName")),
                 cell(title), cls + ("" if ticker is None else " " + ticker), reason, decision,
                 ", ".join(symbols) or "-"))
    print()
    pairs = {}
    for rec in records:
        key = (str(rec.get("catalogId")), cell(rec.get("catalogName")))
        pairs[key] = pairs.get(key, 0) + 1
    for (catalog_id, name), n in sorted(pairs.items()):
        print("catalogue %s %s: %d" % (catalog_id, name, n))
    for (decision, reason), n in sorted(tally.items()):
        print("%s %s: %d" % (decision, reason, n))
    print("alerts %d of %d" % (sum(n for (d, _r), n in tally.items() if d == "alert"), len(records)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

---

## 13. Commit messages

Implementation, on the branch:

```
TZ-62: vps — the alert rule: promotions and maintenance never alert; new coins, list coins and contract notices do
```

Report, on `main`:

```
TZ-62: report — the alert rule, and its replay on the stream's record
```
