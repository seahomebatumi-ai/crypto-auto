# TZ-22 — Egress measurement: `tokenomist.ai`, `cryptorank.io`

**Do not start before revision `2026-08-30-c` is on `main`.** This TZ performs an
in-session fetch, which the previous hard floor item 9 forbade outright. The rewritten
item 9 permits it as an environment measurement. If the repository copy of
`EXECUTOR-INSTRUCTIONS.md` still carries the old wording, this TZ is **BLOCKED**.

---

## 0. Baseline fingerprint

Quote §0 of `SYSTEM-MAP-CRYPTOCALCUL.md` in full and match every anchor as an exact
substring before any work (contract §5). Expected at this baseline:

| Anchor | Exact string |
|---|---|
| revision | `**Revision 2026-08-30-c.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `55. **A specification is checked against the text it must obey, never against memory of it.**` |

File table and gate figures: as §0 states at revision `2026-08-30-c`. Report any mismatch
as BLOCKED rather than proceeding.

---

## 1. Why this exists

`ANALYST-INSTRUCTIONS.md` §6a makes three supply sweeps mandatory before any setup is
written. Two of them — Vesting and Backing — admit an aggregator as a **discovery**
source. Map §11 lists the lanes measured from the VPS and neither `tokenomist.ai` nor
`cryptorank.io` is on it.

A mandatory sweep whose host is unreachable fails every run. The question is answered by
measurement and never by reading a pattern or reusing an old result (inv. 52).

---

## 2. Scope — no repository file changes

This TZ writes **exactly one file**: its own report,
`CryptoReports/TZ-22-egress-measurement-report.md`, committed directly to `main` per
contract §8. No branch, no pull request, no production file, no bench, no workflow,
nothing under `analyst/`.

The report **is** the measurement record. That is the whole deliverable.

---

## 3. What to measure

Six probes per host, plus two controls. Nothing is guessed and nothing is retried into
success.

### 3.1 Per target host — `tokenomist.ai`, `cryptorank.io`

| # | Probe | Record |
|---:|---|---|
| 1 | DNS resolution of the apex and of `www` | resolved addresses, or the resolver error verbatim |
| 2 | TLS CONNECT on 443 | success, or the failure verbatim |
| 3 | `GET /` — the rendered page | status · `content-type` · body bytes · **classification (§3.3)** |
| 4 | `GET /robots.txt` | status · whether it names a sitemap or an API path |
| 5 | Documented machine-readable endpoint, **only if the site itself names one** | status · `content-type` · body bytes · classification |
| 6 | First 400 bytes of every 2xx body | verbatim in the report, so the classification can be checked by a reader |

**Probe 5 does not guess paths.** A path is admissible only if the host's own
`robots.txt`, a linked OpenAPI or docs page, or a `Link` header names it. If none does,
record `no documented endpoint found` — that is a result. TZ-20 spent three probe rounds
guessing `/api/...` paths at Cboe and Fidelity and collected four 404s that meant nothing.

**No evasion, at any point.** Default `curl` user agent, no browser impersonation, no
cookie jar, no proxy, no retry past the second attempt, at most one request per second per
host. A managed challenge has declined to serve this client; that is the measurement, not
an obstacle to route around (`ANALYST-INSTRUCTIONS.md` §6). A run that routes around one
produces a lane that will close again without warning.

### 3.2 Two controls, both mandatory (inv. 23)

| Control | Must read | Proves |
|---|---|---|
| `https://api.llama.fi/protocols` | `open` | the probe can detect an open lane — §11 already measured this API as answering |
| `https://this-host-does-not-exist-tz22.invalid/` | `unreachable` | the probe can detect and report failure |

A probe that has never returned `unreachable` is not yet known to be able to.

### 3.3 Classification — status code alone is not the answer

Each endpoint gets exactly one of four labels, and the label is decided by the **body**,
not by the code:

| Label | Condition |
|---|---|
| `open` | 2xx, and the body is the expected content type carrying plausible payload |
| `challenged` | 2xx, but the body is a bot challenge, a JS interstitial or a consent wall |
| `refused` | 4xx or 5xx |
| `unreachable` | DNS failure or CONNECT failure |

This distinction is load-bearing and is the reason probe 6 exists. §11 already records the
two shapes it exists to separate: `defillama.com` refuses its rendered page with 403 while
serving its API, so **a 403 on a page whose API answers is not a closed lane**; and
`farside.co.uk` answers a managed challenge, so **200 is not an open lane**.

---

## 4. Report

Contract §4a, plus:

1. A table: host × probe × status × label, every cell filled or explicitly `not run` with
   the reason.
2. The exact command for every probe, copy-pasteable, so a reader reproduces the run
   rather than trusting it (inv. 44, second class).
3. The first 400 bytes of every 2xx body.
4. Both controls, with their readings.
5. The UTC timestamp of the run and the machine it ran on.
6. **One recommendation line per host**, in this vocabulary and no other:
   `usable as a discovery source` · `usable only through the named endpoint` ·
   `not usable`. Nothing about what the data says — this TZ measures a network, not a
   market.

**Do not run a market analysis.** Nothing under `analyst/` is read, written or consulted.
No price, date, figure or event from any probed body enters the report as a fact about the
market; a body is quoted only as evidence of what the host served.

---

## 5. Acceptance criteria

1. Both target hosts carry a label for every probe that ran.
2. The DeFiLlama control reads `open`; the `.invalid` control reads `unreachable`.
3. Every 2xx label is supported by quoted body bytes in the report.
4. No path was guessed; probe 5 is either sourced from the host's own documents or
   recorded as `no documented endpoint found`.
5. No evasion technique appears in any command.
6. `git status --porcelain` shows exactly one file: the report.
7. The `Final Repository State` section describes nothing about its own push (inv. 54,
   contract §4a as amended in v14).

---

## 6. Hard floor

Item 9 as amended in v14 is the clause this TZ depends on. Read it from the repository
before starting; if it still forbids an in-session fetch outright, report **BLOCKED** and
stop. Every other item binds unchanged — in particular item 2: no bench, no filter and no
threshold is edited so that a probe passes.

---

## 7. Commit

Direct to `main`, one commit, one file:

`docs(egress): measure tokenomist.ai and cryptorank.io from the VPS (TZ-22)`
