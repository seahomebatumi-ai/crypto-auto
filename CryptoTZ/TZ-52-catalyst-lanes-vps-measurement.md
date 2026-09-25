# TZ-52 — Catalyst lanes and perpetual klines, measured from the VPS

**Canonical filename:** `CryptoTZ/TZ-52-catalyst-lanes-vps-measurement.md`
**Report:** `CryptoReports/TZ-52-catalyst-lanes-vps-measurement-report.md`
**Class:** report-only TZ (contract §8) — the one file this session writes is its report.
**Model:** Opus
**Issued:** 25.09.2026, by the Architect.

---

## Required System Map fingerprint

Quoted in full from `SYSTEM-MAP-CRYPTOCALCUL.md` `## 0. Fingerprint`. Cut the anchor list
from the map's own table by its structure and print the table's row count beside the number
compared (contract §5 step 2).

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-22-b.**` |
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

**Files this TZ adds to the gate table — reported, not enforced.** This TZ quotes both
contracts, so a difference between these values and the repository means a quote below may
have moved; report the difference under `## Pre-existing Issues` and do not act on it.

| File | Lines | MD5 | Revision line |
|---|---:|---|---|
| `ANALYST-INSTRUCTIONS.md` | 3465 | `c72986bf15e70dcefe1256c4c0ac6126` | `2026-09-30-a` |
| `EXECUTOR-INSTRUCTIONS.md` | 864 | `02abb1969626d2af150a0d1f6e02f2a7` | `Version 23` |

---

## Objective

Measure, from the Executor's own machine, the catalyst lanes the analysis engine does not have,
and the one host the next TZ needs. **Nothing here is admitted as a lane**: admission is an
Architect edit to `ANALYST-INSTRUCTIONS.md` written against this report.

The engine's own records name the gap. NEAR's move of 17.09 came from a launch announced on the
protocol's own site while NEAR's only lane is a governance forum (methodology §6, §6a); ONDO's
release of 24.09 went out after the freeze, ONDO was not searched that run and has no channel
(§5 step 5, §6a). **Neither miss was a refusal.** The one refusal this TZ addresses is
`sec.gov`, and the Architect's reading of 25.09.2026 shows it was the engine's own undeclared
client, not a denial (Stage E).

**Owner's decision of 25.09.2026: free sources only.** Every read below is keyless and free. A
host that answers only with payment or a credential is recorded as such and goes no further.

---

## Contract text this TZ obeys

Contract §7 item 9:

> **Measuring the session's own environment is a DIFFERENT act and is permitted** — egress, tool availability, host reachability — provided the command is recorded beside its result, because there the artifact IS the measurement and re-running the command is the reproduction. Such a probe produces no product fact and may be re-run at will. It is still bounded by item 2 and by `ANALYST-INSTRUCTIONS.md` §6: a managed challenge or a refusal is the reading, never an obstacle to route around, and no evasion technique appears in any command.

Map inv. 44:

> **Permitted in a session** — measuring the session's OWN ENVIRONMENT (egress, tool availability, host reachability), because the artifact IS the measurement, the command is recorded beside its result, and re-running the command is the reproduction; this class produces no product fact.

Methodology §6a, the client:

> **The command is part of the channel.** A host answers a client and not only a URL (map inv. 52), and every row was measured in one form: `curl -sS -L -m 20` on the row's request. Flags that change nothing on the wire — `-o`, `-D`, `-w` — are free; a user-agent, a header, a proxy, a cookie or a retry makes a different client, and a read through any other client or tool is a lane nobody measured: it refreshes no lane and its silence proves nothing, and a document it returns is judged by its publisher like any discovery hit (§6).

Methodology §6a, the coverage test the engine runs itself:

> take the coin's largest single-day move of the last thirty days from the structural file the run reads every day (§5), and ask whether any lane this table gives that coin holds a record dated inside the forty-eight hours before it.

Methodology §6a, the publisher of record when a host refuses:

> for a regulatory proceeding is the register the agency is required to publish in, for a statistical release the issuing body's own machine-readable feed, and for a legislative calendar the chamber's own

Methodology §11, the record Stage A reads:

> Its `d` is the day it was measured, `status` is `охвачена`, `неохваченная` or `неизмеримо`, `move` the coin's largest single-day move of the last thirty days with its date — at `неизмеримо`, the reason the measurement cannot be computed (item 90) — and `carried_by` the host that did carry the announcement, where one was found.

---

## Scope

- **Files to Create:** `CryptoReports/TZ-52-catalyst-lanes-vps-measurement-report.md` — nothing else.
- **Files to Modify:** none.
- **Files to Delete:** none.
- **Read-only inputs:** `index.html`, `main.py`, `analyst/state.json`, `analyst/live.json`.
- **Forbidden:** any write under `analyst/`, to `catalysts.json`, to a production file, bench,
  workflow or contract. No date, figure or event read here enters any file except the report,
  and the report carries them as evidence about a channel, never as a catalyst.
- Scratch lives in `/tmp` and is removed before the commit.

---

## Client rules — every read

1. **One form:** `curl -sS -L -m 20 -o <file> -D <headers> -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' '<url>'`.
   Free flags only. A `.gz` body is decompressed locally after the read.
2. **One request per URL. No retry, no second client**, no user-agent, header, proxy, cookie,
   browser or headless renderer. A refusal, a challenge or a timeout is the reading.
3. **The one exception is Stage E2**, and it is not evasion: SEC's own published access policy
   asks every automated client to declare itself — «Please declare your user agent in request
   headers» (`https://www.sec.gov/os/accessing-edgar-data`). The declared read adds exactly one
   flag and nothing else. No other stage may declare, disguise or alter the client.
4. **Site hosts: `robots.txt` first.** Record the group that governs this client (`*` for curl)
   and every `Allow`/`Disallow` line matching a path about to be read. A disallowed path is not
   requested and is recorded `refused on permission`. Documented APIs (CoinGecko, Federal
   Register, SEC full-text search, Upbit, Binance) are governed by their documentation instead.
5. **Pacing:** reads are sequential, never parallel; CoinGecko reads stand at least 12 s apart.
6. **Every reading prints** its command, HTTP status, bytes, content type and landing URL. A
   lane is recorded where it LANDS (methodology §6a).

---

### Stage A — Baseline and the engine's own coverage record

A1. Contract §4a steps 1–6 and the §5 gate above.

A2. **Universe, cut at run time and never retyped.** Parse `tokens[]` from `index.html`
(symbol, pair, `fut:true`) and the `TOKENS` literal from `main.py` (symbol → CoinGecko id).
Print both counts and their symmetric difference.

A3. **Read `analyst/state.json`.** For every symbol of A2 print
`sweeps.coins.<SYM>.coverage` verbatim — `d`, `status`, `move`, `carried_by` — or `absent`.
Print the count per status.

A4. **Client identity.** `curl --version` (first line), and whether
`git config --get user.email` returns an address — yes or no; the address itself is used only
in E2 and is never printed unmasked.

### Stage B — The protocol's own site channels, per coin

B1. **Registered sites.** For each CoinGecko id of A2, one read of
`https://api.coingecko.com/api/v3/coins/<id>?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false`.
Record `name`, the first non-empty `links.homepage`, and every non-empty
`links.announcement_url`. A refused read leaves that coin's Stage B unserved; nothing is guessed.

B2. **Candidates per coin:** the homepage, each announcement URL, and the root of A3's
`carried_by` host where one is recorded — deduplicated by URL.

B3. **Per candidate host:** `robots.txt` (rule 4), and its `Sitemap:` lines.

B4. **Advertised feeds.** Read each candidate page once and extract every
`<link rel="alternate" type="application/rss+xml">` and `application/atom+xml` href. Read at
most two per host. Record items, items carrying a date (`pubDate`, `published` or `updated`),
the newest and the oldest date.

B5. **Sitemaps.** Read the `robots.txt`-declared sitemaps, or `/sitemap.xml` where none is
declared. From an index, read at most three children whose path contains `blog`, `news`, `post`,
`press`, `announce`, `update` or `insight` (case-insensitive), latest `lastmod` first. In a
urlset, consider the URLs whose path contains one of those words, or every URL where none does.
Record: URLs considered, URLs with `lastmod`, distinct `lastmod` calendar dates, newest, oldest,
and any comment inside the file stating that its dates are placeholders (quote at most twenty
words).

B6. **Classification per lane.** `dated` if at least one record carries a date and the dates
take at least two distinct calendar days; otherwise `undated`. Beside it: `refused`,
`refused on permission`, `no channel`, as read.

B7. **Screening — not item 90.** Once a lane is admitted the engine measures coverage by its own
rule, because the row changed (methodology §6a); this is only the evidence for admitting it. For
a coin whose A3 `move` carries a parseable date, with D the move's UTC day, a `dated` lane is
`carried` if it holds a record dated D−2, D−1 or D; `window short` if its oldest record is later
than D−2; otherwise `not carried`. A coin without a parseable move is `no move recorded`, with the
raw field printed. **The move is never recomputed here** (inv. 38).

Output: one row per coin — site host, candidate lanes with class and window, B7 verdict.

### Stage C — Reporter feeds: discovery, never primary

One read each:

- `https://www.coindesk.com/arc/outboundfeeds/rss/`
- `https://www.theblock.co/rss.xml`
- `https://decrypt.co/feed`
- `https://cointelegraph.com/rss`

Per feed: rule 4 on its path, status, landing, items, dated items, window. **List yield:** every
item whose title names a symbol of A2 as a whole uppercase word, or the coin's B1 `name` as a
whole word (case-insensitive) — feed, date in UTC, title up to 100 characters. **Book yield:**
read `analyst/live.json` by command, never whole — print its top-level keys, its own timestamp
field and the key set of the first `x` row — then count titles naming, as a whole uppercase word,
the base asset of any `x` row whose symbol ends in `USDT`. Print the union window of the four
feeds.

### Stage D — Exchange state: Upbit's documented market list

One read of `https://api.upbit.com/v1/market/all?isDetails=true`. Record status, markets, `KRW-`
markets; how many `KRW-` bases are symbols of A2, and how many are bases of `x` rows; how many
markets carry `market_event.warning` true, and how many carry each `market_event.caution` key
true. List every A2 symbol carrying either.

### Stage E — Publishers of record for scheduled systemic events

E1. **Federal Register API.** One read of
`https://www.federalregister.gov/api/v1/documents.json?per_page=20&order=newest&conditions%5Bagencies%5D%5B%5D=securities-and-exchange-commission`.
Record status and `count`; per result `publication_date`, `type` and the first 100 characters of
`title`. Count the titles containing `Longer Period`, `Proceedings`, `Approving`, `Disapproving`,
and those naming `bitcoin`, `ether`, `crypto`, `digital asset`, `solana`, `xrp` or `trust`
(case-insensitive).

E2. **SEC full-text search, two forms of one URL:**
`https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1`

- (a) the rule-1 form, exactly;
- (b) the rule-1 form plus exactly `-A "crypto-auto <contact>"`, where `<contact>` is A4's
  address.

Record status and bytes for each, and `hits.total.value` for any JSON answer. Print the contact
masked — first character of the local part, `***@`, then the domain. Where A4 found no address,
(b) is not made, and the report says so; no address is substituted.

### Stage F — Binance USDⓈ-M klines for the declared perpetuals

This is a reading for the next TZ, which must choose the source of the five declared
perpetuals' structural rows (map §10). For each `fut:true` row of A2, one read of
`https://fapi.binance.com/fapi/v1/klines?symbol=<pair>&interval=1h&limit=3`. Record status, bytes,
the number of rows, and the first element of the last row, which Binance documents as its open
time, as ISO UTC. **No price is printed.** The shape is reported as read.

---

## Validation

Written by the Architect; every item runs, and an item that cannot run fails.

**V1 — Classifier fixtures in `/tmp`.** Derived from: the definitions in B6 and B7; no host is
involved.

| Fixture | Shape | Expected |
|---|---|---|
| a | urlset, two news URLs, `lastmod` on two different days | `dated` |
| b | urlset, three URLs, one identical `lastmod` | `undated` |
| c | urlset, no `lastmod` | `undated` |
| d | move on day D; a record dated D−1; oldest record D−10 | `carried` |
| e | move on day D; oldest record D+1 | `window short` |

**Negative control:** run a–c once more with B6's comparison inverted; a and b must swap. Print
both runs. A classifier never shown to fail is not a control.

**V2 — Live known-answer pair, reported, not blocking.** Expected: NEAR's sitemap `undated`,
Ondo's `dated`. Derived from: the Architect's reading of 25.09.2026 from its own environment,
not the VPS — `https://www.near.org/sitemap.xml` carries a comment declaring its `lastmod` values
placeholders dated 2026-08-15, and `https://ondo.finance/sitemap.xml`, declared in that host's
`robots.txt`, carries `lastmod` on 186 of 198 URLs, newest blog record
`2026-09-24T12:30:00.000Z`. A host that changed since is printed as read and marked
`host changed`; the reading wins.

**V3 — Counts are counts.** Every stage prints attempted beside reported. Coins attempted in
Stage B equal A2's count, printed beside it. A stage that attempted zero fails (inv. 22).

**V4 — Evidence.** Every reading line carries command, status, bytes, content type and landing
URL.

**V5 — Nothing but the report.** `git status --porcelain` before the commit lists exactly the
report. No production file, bench or workflow is touched, so no bench runs; the empty diff
outside `CryptoReports/` is the no-regression evidence.

**V6 — Hygiene.** `/tmp` scratch removed; nothing else committed.

---

## Report

The contract §10 template, plus one table per stage. `## Remaining Risks` names at least: a
sitemap's `lastmod` may record an edit rather than publication; a reporter feed's window is one to
two days; matching by symbol and name admits false hits. `## Pull Request` carries the fixed
report-only line.

## Commit Message

`TZ-52: report — catalyst lanes and perpetual klines measured from the VPS`

## What this TZ does not decide

Which lanes are admitted, in what class and with what command — an Architect edit to
`ANALYST-INSTRUCTIONS.md` after the audit. The source of the perpetuals' structural rows — the
next TZ, written against Stage F. Nothing here changes what an analysis run publishes.
