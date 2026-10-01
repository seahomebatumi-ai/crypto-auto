# TZ-53 — Automation environment and hunter lanes, read from the VPS

**Canonical filename:** `CryptoTZ/TZ-53-automation-and-hunter-lanes-vps-reading.md`
**Report:** `CryptoReports/TZ-53-automation-and-hunter-lanes-vps-reading-report.md`
**Class:** report-only TZ (contract §8) — the one file this session writes is its report.
**Model:** Opus
**Issued:** 01.10.2026, by the Architect.

---

## Required System Map fingerprint

Quoted in full from `SYSTEM-MAP-CRYPTOCALCUL.md` `## 0. Fingerprint`. Cut the anchor list
from the map's own table by its structure and print the table's row count beside the number
compared (contract §5 step 2).

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-01-a.**` |
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
| `ANALYST-INSTRUCTIONS.md` | 3866 | `feaaffc99f983b3441ce205bcf1b6466` | `2026-10-01-a` |
| `EXECUTOR-INSTRUCTIONS.md` | 864 | `02abb1969626d2af150a0d1f6e02f2a7` | `Version 23` |

---

## Objective

Read, from the Executor's own machine, everything the next TZ needs to build the delivery layer
the owner confirmed on 01.10.2026 — a scheduler, a payload written by the VPS, a Telegram bot and
the hunter's own schedule (map §10, row «The assistant's build sequence»). **Nothing is built,
installed, enabled or admitted here.** The next TZ is written against this report, and a lane is
admitted only by an Architect edit to `ANALYST-INSTRUCTIONS.md`.

Four questions, one stage each after the baseline: what this machine is and whether a scheduled
job can run a headless session on it (B); whether it can produce the payload the engine reads,
and what Binance itself publishes about listings (C); whether it can reach Telegram (D); and which
liquidity, flow and calendar publishers answer it (E).

**Owner's decision of 25.09.2026 still binds: free sources only.** Every read below is keyless.

---

## Contract text this TZ obeys

Contract §7 item 6:

> **Never commit secrets.** Credentials live only in GitHub Actions environment variables (inv. 7).

Map inv. 7:

> 7. The client-side password is decoration. Secrets live only in GitHub Actions env.

Contract §7 item 9:

> **Measuring the session's own environment is a DIFFERENT act and is permitted** — egress, tool availability, host reachability — provided the command is recorded beside its result, because there the artifact IS the measurement and re-running the command is the reproduction. Such a probe produces no product fact and may be re-run at will. It is still bounded by item 2 and by `ANALYST-INSTRUCTIONS.md` §6: a managed challenge or a refusal is the reading, never an obstacle to route around, and no evasion technique appears in any command.

Map inv. 44:

> **Permitted in a session** — measuring the session's OWN ENVIRONMENT (egress, tool availability, host reachability), because the artifact IS the measurement, the command is recorded beside its result, and re-running the command is the reproduction; this class produces no product fact.

Contract §8, the class:

> A **report-only TZ** authorises exactly one written file — its own report — on the `CryptoReports/**` direct-push path.

Methodology §6a, the client:

> **The command is part of the channel.** A host answers a client and not only a URL (map inv. 52), and every row was measured in one form: `curl -sS -L -m 20` on the row's request. Flags that change nothing on the wire — `-o`, `-D`, `-w` — are free; a user-agent, a header, a proxy, a cookie or a retry makes a different client, and a read through any other client or tool is a lane nobody measured: it refreshes no lane and its silence proves nothing, and a document it returns is judged by its publisher like any discovery hit (§6).

Map §10, row «The assistant's build sequence» — why no credential is created here:

> **TZ-54 waits on one floor edit** (inv. 59): contract §7 item 6 and inv. 7 place every credential in GitHub Actions

**So this TZ reads whether credentials EXIST and never what they contain**, creates none, asks the
owner for none, and prints nothing a credential could hide in without passing the mask of V1.

---

## Scope

- **Files to Create:** `CryptoReports/TZ-53-automation-and-hunter-lanes-vps-reading-report.md` — nothing else.
- **Files to Modify:** none.
- **Files to Delete:** none.
- **Read-only inputs:** `analyst/live.json` (by command, never whole), the checkout's git configuration.
- **Forbidden:** any write under `analyst/`, to `catalysts.json`, to a production file, bench,
  workflow or contract; installing, enabling or configuring anything — a package, a service, a
  timer, a crontab line, a git setting; creating a branch, a ref or a remote; reading the content
  of any credential file; running `claude` inside this session (Stage B6 says where it runs and
  why). No date, figure or event read here enters any file except the report, and the report
  carries them as evidence about a channel, never as a catalyst or a price.
- Scratch lives in `/tmp/tz53` and is removed before the commit.

---

## Client rules — every read

1. **One form:** `curl -sS -L -m 20 -o <file> -D <headers> -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' '<url>'`.
   Free flags only.
2. **One request per URL. No retry, no second client**, no user-agent, header, proxy, cookie,
   browser or headless renderer. A refusal, a challenge or a timeout is the reading.
3. **Site hosts: `robots.txt` first.** Record the group that governs this client (`*` for curl)
   and every `Allow`/`Disallow` line matching a path about to be read. A disallowed path is not
   requested and is recorded `refused on permission`; a 4xx `robots.txt` imposes no restriction
   (RFC 9309 §2.3.1.3). Documented APIs — Binance, Telegram's Bot API, the Treasury's Fiscal Data,
   DefiLlama's stablecoin API, Coinbase Exchange, ipinfo — are governed by their documentation
   instead.
4. **Pacing:** reads are sequential, never parallel; FRED reads stand at least 1 s apart (its own
   `Crawl-delay: 1`).
5. **Every reading prints** its command, HTTP status, bytes, content type and landing URL.
6. **No price, rate, balance, holding or flow figure is printed.** Statuses, counts, key sets,
   dates and freshness are — they describe the channel, and the channel is what is measured.
7. **Every printed line passes the mask first.** The filter is `/tmp/tz53/mask.sed`, exactly these
   five expressions, applied with `sed -E -f`:

   ```
   s#(https?://)[^/@[:space:]]+@#\1***@#g
   s#[0-9]{6,12}:[A-Za-z0-9_-]{30,}#***#g
   s#gh[pousr]_[A-Za-z0-9]{20,}#***#g
   s#github_pat_[A-Za-z0-9_]{20,}#***#g
   s#sk-ant-[A-Za-z0-9_-]{8,}#***#g
   ```

   (URL userinfo, a Telegram bot token, GitHub tokens, an Anthropic key.) The owner's email, where
   any command prints one, is masked as TZ-52 masked it: first character of the local part, `***@`,
   the domain.

---

### Stage A — Baseline

A1. Contract §4a steps 1–6 and the §5 gate above.

A2. **The payload, by command.** From `analyst/live.json` print its top-level keys, `ts`, `src`,
`n`, the length and key set of `c`, and the length and key set of `x[0]`. Never print a row.

A3. **The session.** `id -un`, `id -u`; whether `CLAUDECODE` is set in this session's environment
(set / unset — the value is not printed); `git rev-parse --show-toplevel`.

### Stage B — The machine and its scheduler

B1. **Identity.** `PRETTY_NAME` from `/etc/os-release`; `uname -r`; `systemd-detect-virt` (value
and exit code); `cat /proc/1/comm`; `uptime -s`; `nproc`; `free -m` (memory total and available,
swap total); `df -h --output=size,avail,target /`; `timedatectl show -p Timezone -p NTPSynchronized`.

B2. **Hosting provider.** One read of `https://ipinfo.io/org` by rule 1. Print its one line — an
autonomous system and its holder. **The address itself is never requested and never printed.**

B3. **Persistence.** The checkout of A3: the date of its oldest reflog entry
(`git reflog --date=iso | tail -1`), and `stat -c '%w | %y'` of its `.git` directory.

B4. **Service manager and cron.** `systemctl --version | head -1`; `systemctl is-system-running`
(value, exit code); for a non-root user of A3 also `systemctl --user is-system-running`,
`loginctl show-user "$(id -un)" -p Linger` and `sudo -n true` (exit code only);
`systemctl is-active cron` (value, exit code); `crontab -l` — **exit code and the count of
non-empty, non-comment lines only; the lines are never printed.**

B5. **Toolchain and credentials — existence only.** `python3 --version`, `node --version`,
`npm --version`, `git --version`, `jq --version`, `gh --version | head -1`, `command -v tmux`;
`command -v claude`, or where that is empty, which of `~/.local/bin/claude`, `/usr/local/bin/claude`,
`/usr/bin/claude` exists; `gh auth status` — exit code only; whether
`"$HOME/.claude/.credentials.json"` exists (present / absent); whether `ANTHROPIC_API_KEY` is set
(`[ -n "${ANTHROPIC_API_KEY+x}" ]`, set / unset); `git remote get-url origin` through the mask;
`git config --get credential.helper` through the mask.

B6. **The scheduler's environment — one transient unit.** A scheduled job does not run inside this
session, so what it can do is read by starting one. **`claude` is never run inside this session:**
a nested session shares the running one's state, and it answers about this session's environment,
which is not the scheduler's. Write `/tmp/tz53/unit/probe.sh`:

```
#!/bin/sh
cd /tmp/tz53/unit
"$CLAUDE_BIN" --version >version.out 2>version.err; echo $? >version.rc
"$CLAUDE_BIN" --help >help.out 2>help.err; echo $? >help.rc
timeout 180 "$CLAUDE_BIN" -p "Reply with exactly: HEADLESS-OK" --output-format json >headless.json 2>headless.err; echo $? >headless.rc
GIT_TERMINAL_PROMPT=0 git -C "$REPO" push --dry-run origin HEAD:refs/heads/tz-53-push-probe >push.out 2>push.err; echo $? >push.rc
```

and start it once, as root with `systemd-run`, as a non-root user with `systemd-run --user`:

```
timeout 330 systemd-run [--user] --unit=tz53-probe --wait --collect --property=RuntimeMaxSec=300 \
  --setenv=HOME="$HOME" --setenv=PATH="$PATH" \
  --setenv=CLAUDE_BIN="<B5 path>" --setenv=REPO="<A3 path>" /tmp/tz53/unit/probe.sh
```

Record `systemd-run`'s exit code and its closing lines. Then, through the mask: each `.rc`;
`version.out`; for each of `--output-format`, `--permission-mode`, `--allowedTools`, `--max-turns`,
`--append-system-prompt`, `--mcp-config` and `--dangerously-skip-permissions`, whether it occurs in
`help.out`; the key set of `headless.json`, its `is_error`, `num_turns` and `duration_ms`, and
whether `result` equals `HEADLESS-OK` exactly; the first line of `push.err`. **A dry-run push
creates nothing**: it authenticates and stops. Where the unit cannot start, record the exit code and
the first line of stderr, and B6 is `not measurable here` — it is never replaced by another way of
running `claude`.

### Stage C — Binance: the payload and the listing state

C1. `https://fapi.binance.com/fapi/v1/ping`; then `https://fapi.binance.com/fapi/v1/time` — print
the skew, `serverTime` minus the local epoch milliseconds taken when the response returned.

C2. `https://fapi.binance.com/fapi/v1/ticker/24hr` — rows, and the row key set compared with A2's
`x[0]` key set: `equal`, or both differences.

C3. `https://fapi.binance.com/fapi/v1/premiumIndex` — rows and the row key set; whether
`markPrice` and `lastFundingRate` are among the keys.

C4. `https://fapi.binance.com/fapi/v1/openInterest?symbol=BTCUSDT` — the key set.

C5. `https://fapi.binance.com/fapi/v1/exchangeInfo` — symbol count; count per `contractType` and
per `status`; among `PERPETUAL` rows, the five most frequent `deliveryDate` values with their counts,
as ISO UTC dates; every symbol whose `onboardDate` lies in the seven days before the read, with that
date. **This is Binance's documented record of what it lists and when it delists**, and C5 reads
whether it carries the dates.

C6. Positioning, one read each, `symbol=BTCUSDT&period=1h&limit=2`:
`https://fapi.binance.com/futures/data/topLongShortPositionRatio`,
`https://fapi.binance.com/futures/data/globalLongShortAccountRatio`,
`https://fapi.binance.com/futures/data/takerlongshortRatio`,
`https://fapi.binance.com/futures/data/openInterestHist` — status, rows, key set.

C7. `https://api.binance.com/api/v3/ping` — status.

C8. **The announcement site.** `https://www.binance.com/robots.txt` under rule 3: print the `*`
group's lines that decide `/bapi/composite/v1/public/cms/article/list/query` and
`/sitemap_output/`, and the decision for each. A disallowed path is `refused on permission` and is
not requested. Where `/sitemap_output/` is allowed: the `robots.txt`-declared
`sitemap_SupportAndAnnouncement_index.xml`, then its English child whose name ends `_en_0.xml` —
URLs, URLs with `lastmod`, distinct `lastmod` dates, the newest, and the hours between it and the
read; then one read of the first `<loc>` of that child that contains `/support/announcement/` —
status, bytes, content type.

### Stage D — Telegram, with no token

D1. `https://api.telegram.org/` — status and landing.

D2. `https://api.telegram.org/bot0:invalid/getMe` — status and the body verbatim. **No token
exists and none is created or requested**; this reads whether the host answers this machine.

### Stage E — The hunter's candidate lanes: liquidity, flows, the calendar

E1. **FRED.** `https://fred.stlouisfed.org/robots.txt` under rule 3, then
`https://fred.stlouisfed.org/graph/fredgraph.csv?id=<ID>` for `WALCL`, `WTREGEN`, `RRPONTSYD` and
`WRESBAL` — status, rows, header line, the date of the last observation. No value.

E2. **Federal Reserve.** `https://www.federalreserve.gov/robots.txt`, then
`https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm` — the count of meetings under the
heading `2026 FOMC Meetings`, parsed from the page's `fomc-meeting__month` and
`fomc-meeting__date` blocks, and the meetings as read; then
`https://www.federalreserve.gov/releases/h41/current/h41.htm` — status, bytes, the first date after
`Release Date:`.

E3. **Treasury cash.**
`https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/dts/operating_cash_balance?sort=-record_date&page%5Bsize%5D=2`
— status, the newest `record_date`, the row key set.

E4. **Stablecoin supply.** `https://stablecoins.llama.fi/stablecoins?includePrices=false` — status,
bytes, the count of `peggedAssets`, the key set of the first; `https://stablecoins.llama.fi/stablecoincharts/all`
— rows and the newest `date` as ISO UTC.

E5. **ETF holdings at their issuers.** `robots.txt` of each origin under rule 3, then one read each:
`https://www.ishares.com/us/products/333011/ishares-bitcoin-trust-etf`,
`https://www.ishares.com/us/products/337614/ishares-ethereum-trust-etf`,
`https://bitbetf.com/`, `https://www.grayscale.com/funds/grayscale-bitcoin-trust`. Per page: status,
bytes, landing; whether the served HTML carries a shares-outstanding datum — on iShares the
`keyFundFacts-sharesOutstanding` datapoint, elsewhere the label «Shares Outstanding» — and, where
the page states one, its as-of date as read after HTML unescaping. The figure is not printed.

E6. **Aggregated ETF flows.** `https://farside.co.uk/robots.txt` under rule 3, then
`https://farside.co.uk/btc/` and `https://farside.co.uk/eth/` — status, the `cf-mitigated` header
where present, and whether the body contains `<table`.

E7. **Coinbase Exchange.** `https://api.exchange.coinbase.com/products/BTC-USD/ticker` and
`.../ETH-USD/ticker` — status, key set, and the seconds between the body's `time` and the read.

---

## Validation

Written by the Architect; every item runs, and an item that cannot run fails.

**V1 — The mask, on a fixture, with its negative control.** Derived from: rule 7's expressions and
the Architect's probe of them on this fixture on 01.10.2026 — 4 leak lines unmasked, 0 masked, the
clean line intact, and 0 hits of the leak pattern below across all 98 files of `CryptoReports/` and
`analyst/log/` at `cbffb5c`, so a hit in this report is a leak and never a false positive.
Write `/tmp/tz53/leak.re` as this one line:

```
x-access-token:|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-ant-[A-Za-z0-9_-]{8,}|[0-9]{6,12}:[A-Za-z0-9_-]{30,}|-----BEGIN|://[^/@[:space:]*][^/@[:space:]]*@
```

and `/tmp/tz53/fixture.txt` as these five lines — every credential in them is invented, and each is
shorter than the real format it imitates, so no secret scanner mistakes this file for a leak:

```
origin https://x-access-token:ghs_FAKEFAKEFAKEFAKEFAKE0000@github.com/seahomebatumi-ai/crypto-auto.git (fetch)
GET https://api.telegram.org/bot123456789:AAFAKEfakeFAKEfakeFAKEfakeFAKE/getMe
token ghp_FAKEFAKEFAKEFAKEFAKE0000
key sk-ant-api03-FAKEfakeFAKEfake
https://fapi.binance.com/fapi/v1/ping 200 2 application/json
```

| Check | Expected |
|---|---|
| `grep -cE -f /tmp/tz53/leak.re /tmp/tz53/fixture.txt` — the negative control: the scan can fire | `4` |
| the same scan over `sed -E -f /tmp/tz53/mask.sed /tmp/tz53/fixture.txt` | `0` |
| the fifth line survives the mask byte for byte (`grep -cxF`) | `1` |

The report prints the three counts and cites the pattern by this TZ; it does not reprint the
pattern or the fixture, which would make the report scan itself.

**V2 — The report is clean.** `grep -cE -f /tmp/tz53/leak.re` over the final report, run before
the commit, prints `0`. V1's first row is this check's negative control.

**V3 — Counts are counts.** Every stage prints attempted beside answered. A stage that attempted
zero fails (inv. 22).

**V4 — Evidence.** Every reading line carries command, status, bytes, content type and landing
URL, through the mask.

**V5 — Known answers, reported, not blocking.** A host that changed since is printed as read and
marked `host changed`; the reading wins.

| Reading | Expected | Derived from |
|---|---|---|
| C1 ping | `200` | TZ-52 report, Stage F, 25.09.2026: `fapi.binance.com` answered 200 for all five declared perpetuals from this machine |
| C8 decision for `/bapi/composite/v1/public/cms/article/list/query` | disallowed — `Disallow: */bapi/` in the `*` group, `*/bapi/fe/` the only carve-out | the Architect's reading of `https://www.binance.com/robots.txt`, 01.10.2026, its own environment |
| C8 decision for `/sitemap_output/` | allowed — `Allow: */sitemap_output/` | the same reading |
| D1 | `302` to `https://core.telegram.org/bots` | the Architect's reading, 01.10.2026, its own environment |
| D2 | `401`, body `{"ok":false,"error_code":401,"description":"Unauthorized: invalid token specified"}` | the same |
| E1 `robots.txt` | `/graph/fredgraph.csv` not disallowed for `*`; `Crawl-delay: 1` | the same |
| E2 meetings under `2026 FOMC Meetings` | `8` | the same |
| E5 iShares pages | the shares-outstanding datapoint present, with an as-of date | the same: both pages stated «Sep 29, 2026» on 01.10.2026 |

**V6 — Nothing but the report, and nothing left behind.** `git status --porcelain` before the
commit lists exactly the report. `systemctl [--user] list-units --all 'tz53-*' --no-legend | wc -l`
prints `0`, and `git ls-remote origin 'refs/heads/tz-53-*'` prints nothing: the unit was collected
and the dry-run push created no ref. No production file, bench or workflow is touched, so no bench
runs; the empty diff outside `CryptoReports/` is the no-regression evidence.

**V7 — Hygiene.** `/tmp/tz53` removed; nothing else committed.

---

## Report

The contract §10 template, plus one table per stage. `## Remaining Risks` names at least: the
transient unit reproduces a scheduler's environment and not a finished service's; a dry-run push
proves authentication, not permission to push to `main`; D proves the host answers, not that a
message is delivered; the hosting line is a lookup, not a contract; a host answering today may
refuse tomorrow (inv. 52). `## Pull Request` carries the fixed report-only line.

## Commit Message

`TZ-53: report — automation environment and hunter lanes read from the VPS`

## What this TZ does not decide

Where the scheduler runs and in what form, how the bot token is stored — after the floor edit the
map names — and what the payload writer, the bot and the hunter's schedule look like: TZ-54,
written against this report. Which of the lanes read in C and E the engine admits, in what class
and with what command: an Architect edit to `ANALYST-INSTRUCTIONS.md` after the audit. Nothing here
changes what an analysis run publishes.
