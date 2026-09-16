# TZ-46 — Class-2 release channel for ETH and ADA

**Canonical filename:** `CryptoTZ/TZ-46-eth-ada-release-channels.md`
**Report:** `CryptoReports/TZ-46-eth-ada-release-channels-report.md`
**Model:** Sonnet
**Class:** report-only (contract §8) — exactly one written file, the report.
**Previous TZ:** TZ-45, report-only; it left no branch to merge (contract §4a step 6).

---

## 0. Fingerprint

Required System Map revision: `**Revision 2026-09-16-a.**`

The map's `## 0. Fingerprint` block, quoted in full — the revision string above, every content
anchor, and the file table (contract §5):

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-16-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `71. **A measurement that is not RETAINED was not taken,` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

No bench figure is required: this TZ reads no bench and moves no file.

---

## 1. Objective

TZ-45 measured one catalyst channel per member of `tokens[]` and stopped each coin at its first
class that answered with dated records. ETH and ADA stopped at class 1 — `ethereum-magicians.org`
and `forum.cardano.org` — and neither forum is where the event that moves either coin is dated:
a network upgrade is scheduled and announced on a release channel. This TZ measures class 2 for
those two coins, from this machine, with TZ-45's instrument, so that the Architect can name a
channel for each or record that none answered. It measures this session's environment and
produces no product fact.

---

## 2. Scope

**Class: report-only** (contract §8).

### Files to Create

- `CryptoReports/TZ-46-eth-ada-release-channels-report.md`

### Files to Modify

None.

### Files to Rename

None.

### Files to Delete

None.

Nothing is written under `analyst/**`, to `ANALYST-INSTRUCTIONS.md`, to `catalysts.json`, or to
any production, bench or workflow file. Probe scratch lives under `/tmp/tz46/`, outside the
repository, and is removed before the report is committed.

---

## 3. The hard-floor text this TZ stands on

Contract §7 item 9, quoted rather than paraphrased (map inv. 55):

> **Measuring the session's own environment is a DIFFERENT act and is permitted** —
> egress, tool availability, host reachability — provided the command is recorded beside
> its result, because there the artifact IS the measurement and re-running the command is
> the reproduction. Such a probe produces no product fact and may be re-run at will. It
> is still bounded by item 2 and by `ANALYST-INSTRUCTIONS.md` §6: a managed challenge or
> a refusal is the reading, never an obstacle to route around, and no evasion technique
> appears in any command.

---

## 4. Candidates — named here, probed in order, none added

| Id | Symbol | Class | URL | Why this candidate |
|---|---|---|---|---|
| ETH-c2a | ETH | 2 | `https://blog.ethereum.org/feed.xml` | the Ethereum Foundation blog's feed, where mainnet upgrades are announced |
| ETH-c2b | ETH | 2 | `https://api.github.com/repos/ethereum/go-ethereum/releases?per_page=5` | releases of go-ethereum, the Foundation-maintained execution client |
| ADA-c2a | ADA | 2 | `https://api.github.com/repos/IntersectMBO/cardano-node/releases?per_page=5` | releases of cardano-node under Intersect |

1. **One request per candidate, one candidate at a time**, in the table's order within a symbol,
   so each stop decision is taken on a printed verdict before the next request is made.
2. **Stop rule:** a symbol stops at its first `primary-dated` candidate. A candidate after it is
   not requested and appears in the report as `not requested — stop rule`.
3. **A candidate that answers 404, returns an empty list, or refuses is a reading**, recorded as
   such; the next candidate of the same symbol is then requested.
4. **No candidate is added, substituted, guessed or discovered**, no class other than 2 is
   probed, no symbol other than ETH and ADA, and no page beyond the first. If both ETH
   candidates fail, the report says so and stops there.

---

## 5. Instrument

The instrument is TZ-45's `probe.py`, as quoted verbatim in
`CryptoReports/TZ-45-coin-catalyst-channels-report.md` under `### Instrument` — the version that
produced every verdict there, date-list preference and `--reanalyse` mode included — with one
change only: every `/tmp/tz45` becomes `/tmp/tz46`. The report quotes the file as run. Its
classifier and its five verdict words are unchanged: `primary-dated` · `primary-undated` ·
`refused` · `unreachable` · `none-found`.

The command form is TZ-45's, and nothing is added to it:

```
curl -sS -L -m 20 -o /tmp/tz46/body/<id> -D /tmp/tz46/hdr/<id> -w '%{http_code} %{url_effective} %{content_type}' '<url>'
```

No user-agent, header, proxy, cookie or retry flag. A channel is reused in the form it was
measured in, so a different form would measure a different client.

The probe prints schema only — the HTTP status, the effective URL and its host, the content
type, the record list chosen and its length, and the NAMES of date-shaped keys or tags — and
never a value. No title, date or other content of any response enters the report.

---

## 6. What the report carries

In addition to the contract §10 template, `## Implementation Summary` carries:

1. **The candidate table of §4**, one row per candidate in §4's order, with: `Command` exactly as
   executed, `HTTP`, host requested and host answered (a redirect written `a → b`), content
   type, record list and its length, date-key names, and `Verdict` — or
   `not requested — stop rule`.
2. **For each `primary-dated` row, its date field by NAME and type**, in the form TZ-45 used
   (for example «`[].published_at` — ISO-8601 string»).
3. **Tallies:** requests made, and rows per verdict.
4. **The measurement window**, from the modification times of the first and last body files,
   in UTC.

---

## 7. Validation

Each item prints its command and output. An item that cannot run fails (contract §9), and every
count is a count of comparisons that fails on zero (inv. 22, 43).

- **V1 — rows.** The candidate table has exactly three rows, in §4's order. Each carries a
  command and a verdict or reads `not requested — stop rule`, and a `not requested` row sits
  only after a `primary-dated` row of the same symbol. Print: rows, rows with a command, rows
  not requested.
- **V2 — verdict words.** Every verdict is one of §5's five. Print the count per verdict and
  the number of rows checked.
- **V3 — one request per candidate.** Requests made equal rows with a command; ids and URLs are
  distinct; the set of URLs in all commands, minus §4's three, is empty. Print both counts and
  the difference.
- **V4 — no evasion.** TZ-45's V6 flag pattern, over every command in the report and every
  `curl` line of the probe as run, returns zero hits. Print the number of lines scanned.
- **V5 — no product fact.** TZ-45's V5 date, currency, percent, epoch and large-figure patterns,
  over every table row and every date-field line, return zero hits. Print the number of lines
  scanned.
- **V6 — nothing else written.** `git status --porcelain` lists only the report as untracked,
  and `git diff --name-only HEAD` is empty.
- **V7 — scratch removed.** After `rm -rf /tmp/tz46`, `ls -d /tmp/tz46*` fails, and its error is
  printed.

---

## 8. Out of scope

- Reading any record's content, title or date value.
- Probing any host, class, symbol or page not named in §4.
- Writing `analyst/**` or `ANALYST-INSTRUCTIONS.md`: naming a channel in the methodology is an
  Architect edit, forced by this report.
- Retrying a candidate, or changing the client after a refusal.

---

## Commit Message

```
docs(reports): TZ-46 — class-2 release channels probed for ETH and ADA (TZ-46)
```
