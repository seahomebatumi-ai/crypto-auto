# Implementation Report — TZ-24

## Status

**COMPLETED**

All five stages of the specification ran. Both `robots.txt` files were read in full,
one page was probed per host, all three controls returned their required readings, and
four verdict lines — two per host — are stated in the fixed §4 vocabulary. No value from
any probed page body appears anywhere below.

---

## Inbound Filing

None. `CryptoTZ/TZ-24-discovery-host-permission-and-extractability.md` was already at its
canonical path on `origin/main` when the session fetched. No file was moved or renamed.

---

## Scope Executed

**Class: report-only TZ** (contract §8). The TZ's `## Scope` names exactly one file to
create and it lies under `CryptoReports/**`; no file outside that tree is named under
`Files to Modify` or `Files to Delete`. The class is therefore read off the scope, not
chosen. Every contract clause speaking of a branch, a pull request or a merge is silent
here rather than deviated from.

| Stage | Required | Done |
|---|---|---|
| §3.1 | permission read, both hosts, full file, named-agent group verbatim, own UA recorded | yes |
| §3.2 | one page probed per host, sourced from that host's own documents | yes |
| §3.3 | structure only, no value from any probed body | yes |
| §3.4 | three controls, exit codes distinguishing controls 2 and 3 | yes |
| §3.5 | default client, one request per probe, ≤1 req/s per host, every command printed | yes |

Nothing outside `CryptoReports/**` was written. No branch was opened, no pull request
exists, no production file, bench, workflow or `analyst/**` file was touched, and no
market analysis was performed. Probe artifacts were written to `/tmp/tz24/` — outside the
repository — and are not committed.

---

## Files Created

| File | Lines | Purpose |
|---|---:|---|
| `CryptoReports/TZ-24-discovery-host-permission-and-extractability-report.md` | this file | the TZ's single authorised output |

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### 0. Gates — both passed before the first probe

**Gate 1 — System Map fingerprint (contract §5, TZ §0).** Run against `origin/main`
after `git fetch origin`. All seven anchors matched as exact substrings; each returns a
count of 2, one occurrence in the map's own `## 0` anchor table and one in the body it
points at, which is the expected result and confirms the anchors name live sections
rather than only themselves.

```
while IFS= read -r a; do n=$(grep -Fc -- "$a" SYSTEM-MAP-CRYPTOCALCUL.md); echo "$n  ::  $a"; done < /tmp/anchors.txt
```

```
2  ::  **Revision 2026-08-30-e.**
2  ::  ### 3.12 Direction engine — veto cascade
2  ::  ### 3.15 Catalyst registry
2  ::  ### 3.16 List exhaustion — the day-range measure
2  ::  ## 11. Analytical engine
2  ::  ### 3.17 «РИСК ВЫНОСА» — the day's own risk
2  ::  55. **A specification is checked against the text it must obey, never against memory of it.**
```

The map's four fingerprinted files were measured at the required line count and MD5 and
all four match exactly — see `## Fingerprints`. Revision found `2026-08-30-e`, revision
required `2026-08-30-e`.

**Gate 2 — contract must be v15 (TZ §0, second gate).**

```
sed -n '1,5p' EXECUTOR-INSTRUCTIONS.md
```

The version line reads `**Version 15.**`, and §8 names the two TZ classes in the
sentence `A TZ is one of exactly two classes, and the report names its class in
`## Scope Executed` before any clause reads off it.` The report-only class therefore
exists in the repository copy and this TZ is executable against it.

**Gate 3 — hard floor item 9 (TZ §6).** Read from the repository. It still carries:

> **Measuring the session's own environment is a DIFFERENT act and is permitted** —
> egress, tool availability, host reachability — provided the command is recorded beside
> its result, because there the artifact IS the measurement and re-running the command is
> the reproduction.

The item does not forbid an in-session fetch outright, so the TZ is not BLOCKED and the
probes ran. Item 2 bound throughout: nothing in the repository was edited so that a probe
would pass, and no probe was repeated after a disagreeable answer.

**§6a quotes verified against the repository.** Both clauses the TZ quotes as the text it
serves are present verbatim in `ANALYST-INSTRUCTIONS.md` §6a (`Discovery may come from a
vesting aggregator; **publication requires the protocol's own schedule**…` and `Round
terms from aggregators are frequently partial…`). Neither was edited; this TZ amends
nothing.

**Previous TZ's branch.** TZ-21 is merged: its implementation commit `8069341` is an
ancestor of `origin/main` through merge commit `edd650c` (pull request #21), and
`CryptoReports/TZ-21-catalyst-registry-scope-and-basis-report.md` is present. TZ-22's
report is present as well. This work does not build on an unmerged base.

### 1. Run environment

| Fact | Value | Command |
|---|---|---|
| UTC start | `2026-08-30T20:42:23Z` | `date -u +%Y-%m-%dT%H:%M:%SZ` |
| UTC end | `2026-08-30T20:49:13Z` | `date -u +%Y-%m-%dT%H:%M:%SZ` |
| Hostname | `vultr` | `hostname` |
| Kernel | `Linux 6.8.0-136-generic x86_64 GNU/Linux` | `uname -srmo` |
| OS | `Ubuntu 24.04.4 LTS` | `. /etc/os-release; echo $PRETTY_NAME` |
| Client | `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13` | `curl --version \| head -2` |
| Proxy state | none — no `*_proxy` variable is set in the environment | `env \| grep -iE 'proxy'` (no output) |

This is the same VPS and the same client version TZ-22 measured, so the two runs are
comparable and control 1 is directly so.

---

## Validation

### §3.1 — Permission read, `tokenomist.ai`

**Command, exactly as it ran:**

```
curl -sS -v --connect-timeout 15 --max-time 45 -o tokenomist-robots.txt -D tokenomist-robots.hdr \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download} time_total=%{time_total}\n' \
  https://tokenomist.ai/robots.txt 2> tokenomist-robots.trace
```

**Result:** `http_code=200 content_type=text/plain size_download=1281 time_total=0.609469`,
curl exit `0`. Served by Cloudflare (`server: cloudflare`, `cf-ray: a3369f612ec2eeaf-WAW`),
`x-nextjs-cache: HIT`. MD5 `555e106c25119795f3a40bcc22930ec1`, 1 281 bytes, 57 lines, LF
line endings.

**The exact User-Agent this run sent**, taken from curl's own request trace rather than
from a third party that echoes it back:

```
grep -i "^> user-agent:" tokenomist-robots.trace
> User-Agent: curl/8.5.0
```

**Every group present, and its directives.** The file carries 46 `User-Agent:` lines, 2
`Allow:` lines, 5 `Disallow:` lines, 1 `Sitemap:` line and 3 blank separators, in three
groups:

| Group | `User-Agent:` lines | Directives |
|---:|---:|---|
| 1 | 1 — `*` | `Allow: /` · `Disallow: /api/` · `Disallow: /cdn-cgi/` |
| 2 | 39 — named agents, listed below | `Allow: /` · `Disallow: /api/` · `Disallow: /cdn-cgi/` |
| 3 | 6 — `CCBot`, `Omgilibot`, `Omgili`, `Diffbot`, `ImagesiftBot`, `cohere-ai` | `Disallow: /` |

**The group naming `ClaudeBot`, `Claude-SearchBot` and `anthropic-ai`, quoted verbatim
and in full** — this is group 2, reproduced exactly as served:

```
User-Agent: GPTBot
User-Agent: ChatGPT-User
User-Agent: OAI-SearchBot
User-Agent: ClaudeBot
User-Agent: Claude-SearchBot
User-Agent: anthropic-ai
User-Agent: PerplexityBot
User-Agent: Perplexity-User
User-Agent: Google-Extended
User-Agent: GoogleOther
User-Agent: Google-CloudVertexBot
User-Agent: Applebot-Extended
User-Agent: Meta-ExternalAgent
User-Agent: Meta-ExternalFetcher
User-Agent: facebookexternalhit
User-Agent: GrokBot
User-Agent: XBot
User-Agent: DeepSeekBot
User-Agent: MistralAI-User
User-Agent: Gemini-Deep-Research
User-Agent: Google-NotebookLM
User-Agent: GoogleAgent-Mariner
User-Agent: DuckAssistBot
User-Agent: AzureAI-SearchBot
User-Agent: bedrockbot
User-Agent: Claude-User
User-Agent: Operator
User-Agent: meta-webindexer
User-Agent: TavilyBot
User-Agent: kagi-fetcher
User-Agent: LinkupBot
User-Agent: Bytespider
User-Agent: YouBot
User-Agent: BraveBot
User-Agent: Amazonbot
User-Agent: MicrosoftPreview
User-Agent: AI2Bot
User-Agent: iaskspider
User-Agent: PhindBot
Allow: /
Disallow: /api/
Disallow: /cdn-cgi/
```

Three of the TZ's named agents are in this group — `ClaudeBot`, `Claude-SearchBot` and
`anthropic-ai` — and a fourth, `Claude-User`, is in it as well. TZ-22 saw the first six
lines of the group because its 400-byte quote stopped inside the `User-Agent:` list; the
directives were three lines past the cut, which is why they were unknown until now.

The remaining group boundaries, for completeness — group 1 as served:

```
User-Agent: *
Allow: /
Disallow: /api/
Disallow: /cdn-cgi/
```

group 3 as served:

```
User-Agent: CCBot
User-Agent: Omgilibot
User-Agent: Omgili
User-Agent: Diffbot
User-Agent: ImagesiftBot
User-Agent: cohere-ai
Disallow: /
```

and the file's last directive line:

```
Sitemap: https://tokenomist.ai/sitemap.xml
```

**Which group governed THIS run.** The client sent `curl/8.5.0`. That string matches no
named group, so this run fell into **group 1, `User-Agent: *`** — `Allow: /` with `/api/`
and `/cdn-cgi/` disallowed. The two answers differ in who they are about and agree in
substance: group 1 governed this run's requests, group 2 governs an agent operating under
a Claude name, and both grant the same directives.

### §3.1 — Permission read, `cryptorank.io`

**Command, exactly as it ran:**

```
curl -sS -v --connect-timeout 15 --max-time 45 -o cryptorank-robots.txt -D cryptorank-robots.hdr \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download} time_total=%{time_total}\n' \
  https://cryptorank.io/robots.txt 2> cryptorank-robots.trace
```

**Result:** `http_code=200 content_type=text/plain; charset=UTF-8 size_download=1843 time_total=0.114671`,
curl exit `0`. Cloudflare in front (`cf-ray: a3369fc5ac290d4d-WAW`), origin marked
`x-cr-via: R02`. MD5 `f8dad7387c5ee89ec0fb63ecfa4eea3e`, 1 843 bytes, 39 lines, **CRLF**
line endings (`file` reports `ASCII text, with CRLF line terminators`).

**The exact User-Agent this run sent:**

```
grep -i "^> user-agent:" cryptorank-robots.trace
> User-Agent: curl/8.5.0
```

**Every group present, and its directives.** The file carries exactly **one** group. Its
33 directive lines are 9 `Disallow:` and 24 `Allow:`, plus 2 `Sitemap:` lines and 3 blank
separators. Quoted in full, as served:

```
User-Agent: *

Disallow: /*?*
Disallow: /verify-email/
Disallow: /password-reset/
Disallow: /prediction-markets/wallet-statistic/
Disallow: /*/src/components/*
Disallow: /*/*/src/components/*
Disallow: /*/*/*/src/components/*
Disallow: /*/*/*/*/src/components/*
Disallow: /*/*/*/*/*/src/components/*

Allow: /funds/*/rounds?filterType=coFunds&filterKey=*
Allow: /funds/*/rounds?filterKey=*&filterType=coFunds
Allow: /funds/*/rounds?filterType=leadCoFunds&filterKey=*
Allow: /funds/*/rounds?filterKey=*&filterType=leadCoFunds
Allow: /ru/funds/*/rounds?filterType=coFunds&filterKey=*
Allow: /ru/funds/*/rounds?filterKey=*&filterType=coFunds
Allow: /ru/funds/*/rounds?filterType=leadCoFunds&filterKey=*
Allow: /ru/funds/*/rounds?filterKey=*&filterType=leadCoFunds
Allow: /es/funds/*/rounds?filterType=coFunds&filterKey=*
Allow: /es/funds/*/rounds?filterKey=*&filterType=coFunds
Allow: /es/funds/*/rounds?filterType=leadCoFunds&filterKey=*
Allow: /es/funds/*/rounds?filterKey=*&filterType=leadCoFunds
Allow: /zh/funds/*/rounds?filterType=coFunds&filterKey=*
Allow: /zh/funds/*/rounds?filterKey=*&filterType=coFunds
Allow: /zh/funds/*/rounds?filterType=leadCoFunds&filterKey=*
Allow: /zh/funds/*/rounds?filterKey=*&filterType=leadCoFunds
Allow: /vi/funds/*/rounds?filterType=coFunds&filterKey=*
Allow: /vi/funds/*/rounds?filterKey=*&filterType=coFunds
Allow: /vi/funds/*/rounds?filterType=leadCoFunds&filterKey=*
Allow: /vi/funds/*/rounds?filterKey=*&filterType=leadCoFunds
Allow: /ko/funds/*/rounds?filterType=coFunds&filterKey=*
Allow: /ko/funds/*/rounds?filterKey=*&filterType=coFunds
Allow: /ko/funds/*/rounds?filterType=leadCoFunds&filterKey=*
Allow: /ko/funds/*/rounds?filterKey=*&filterType=leadCoFunds

Sitemap: https://cryptorank.io/sitemap.xml
Sitemap: https://cryptorank.io/sitemap-google-news.xml
```

**The group naming `ClaudeBot`, `Claude-SearchBot` or `anthropic-ai`: no such group
exists on this host.** The file names no agent at all beyond `*`. Verified:

```
grep -c '^User-Agent:' cryptorank-robots.txt   ->  1
```

**Which group governed THIS run.** The client sent `curl/8.5.0` and there is exactly one
group, so this run fell into `User-Agent: *` — the same group that governs every client,
named or not. On this host the two questions collapse into one answer, and that itself is
the finding: nothing here addresses an agent operating under a Claude name.

**Note on the `Disallow: /*?*` line.** Every URL carrying a query string is disallowed by
that pattern, and the 24 `Allow:` lines re-admit exactly one shape — a fund's rounds page
filtered by co-fund or lead-co-fund, in six locales. Under the longest-match rule the
`Allow` wins for that shape and the blanket `Disallow` governs every other query URL. This
is the reading the TZ's §3.2 table already encodes, and the probe below used it.

### §3.2 — Extractability probe, `tokenomist.ai`

**Page source — from the host's own documents, not guessed.** `robots.txt` names one
sitemap; it was fetched, and the probed URL is a `<loc>` taken from it verbatim.

```
curl -sS --connect-timeout 15 --max-time 45 -o tokenomist-sitemap.xml -D tokenomist-sitemap.hdr \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download}\n' \
  https://tokenomist.ai/sitemap.xml
```

`http_code=200 content_type=application/xml size_download=1019179`, exit `0`, 6 064
`<loc>` entries, MD5 `43b2d14de8bad490674f363a8e722b3b`. The sitemap is a flat `<urlset>`
of per-project page sets, nine URLs per project. The `<loc>` chosen is the one whose shape
matches the §6a vesting sweep — an unlock-events page — and it was confirmed present in
the sitemap before it was fetched:

```
grep -c '<loc>https://tokenomist.ai/sui/unlock-events</loc>' tokenomist-sitemap.xml   ->  1
```

Nothing in `robots.txt` disallows it: only `/api/` and `/cdn-cgi/` are disallowed for this
run's group, and the path is under neither.

**Probe command, exactly as it ran:**

```
curl -sS --connect-timeout 15 --max-time 45 -o tokenomist-page.html -D tokenomist-page.hdr \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download} time_total=%{time_total}\n' \
  https://tokenomist.ai/sui/unlock-events
```

**Result:** `http_code=200 content_type=text/html; charset=utf-8 size_download=617540 time_total=1.170300`,
curl exit `0`. MD5 `729cd5350155a4106cd708b260a9891e`. No managed challenge, no
interstitial. Response headers of note: `x-powered-by: Next.js`, `x-nextjs-postponed: 1`,
`x-nextjs-stale-time: 300`, `x-middleware-rewrite: /en/sui/unlock-events`,
`cf-cache-status: DYNAMIC`, `cache-control: private, no-cache, no-store`.

**Does the HTML contain a structured payload, and which kind?** Two kinds, counted in the
served bytes:

```
for pat in '__NEXT_DATA__' 'self.__next_f.push' 'application/ld+json' 'type="application/json"' '<script'; do
  printf '%-28s %s\n' "$pat" "$(grep -o -F "$pat" tokenomist-page.html | wc -l)"; done
```

```
__NEXT_DATA__                0
self.__next_f.push           104
application/ld+json          5
type="application/json"      0
<script                      177
```

- **An RSC flight payload** — 104 `self.__next_f.push([1,"…"])` chunks. Each chunk's
  argument is a JSON string literal; decoding all 104 with `json.loads` and concatenating
  them reconstructs the flight stream. **All 104 decoded**, giving **352 138 bytes**
  (MD5 `dee793fb592fe196b8f34d3eb9c562b7`). No `__NEXT_DATA__` element exists on this
  host; this is the App Router shape.
- **Three `<script type="application/ld+json">` elements.** The literal string
  `application/ld+json` occurs 5 times in the served HTML: 3 are the opening tags of real
  elements, and the other 2 are inside the flight payload, where the RSC stream describes
  those same elements. Verified:
  `grep -oE '<script[^>]*type="application/ld\+json"' -> 3`, and
  `grep -o -F 'application/ld+json' tokenomist-flight.txt | wc -l -> 2`.

**Payload sizes and top-level key names.**

The flight stream is not a single keyed object; it is a sequence of `<id>:<payload>` rows.
There are **202 rows**; **92 parse as JSON (199 971 B)** and 110 do not (145 478 B) —
the latter are React element rows whose payloads are split across `$`-references, which is
the format's normal shape and not a fetch failure. Exactly one row's payload is a
top-level JSON **object**:

| Row | Bytes | Top-level key names |
|---|---:|---|
| `0` | 5 167 | `G` `P` `S` `a` `b` `c` `d` `f` `h` `i` `l` `m` `p` `q` `r` `s` |

Those single letters are the flight module-reference table, not data. Every other parsing
row is a top-level JSON **array** — a React element tree.

The three `ld+json` blocks, with byte size and top-level key names:

| Block | Bytes | Parses | Top-level keys |
|---:|---:|---|---|
| 1 | 900 | yes | `@context`, `@graph` |
| 2 | 245 | yes | `@context`, `@type`, `itemListElement` |
| 3 | 2 867 | yes | `@context`, `@type`, `mainEntity` |

**Does any key path have the shape of a vesting schedule or a funding round?** Every
parsed structure was walked and every key matching
`unlock|vest|cliff|emission|allocat|round|raise|invest|fundrais|schedule|supply|token`
was recorded as a key path with the JSON type of its value. **465 candidate paths** were
found; **406 of them sit under `$47[].messages.*`**, which is the page's i18n message
catalogue — UI label strings, not data. The **59** outside it are the whole of the data
surface, and every one of them is accounted for below — 14 individually, and 45 in three
families whose members share one shape:

| Key path | JSON type | Occurrences |
|---|---|---:|
| `$20[].children[].isUnlockScheduleEmpty` | boolean | 1 |
| `$20[].children[].tokenName` | string | 1 |
| `$1f[].children[][].children[].children[].tokenSummary` | object | 1 |
| `$1f[].children[][].children[].children[].tokenSummary.raiseAmount` | number | 1 |
| `$1f[].children[][].children[].children[].tokenSummary.tokenPrice` | number | 1 |
| `$1f[].children[][].children[].children[].tokenSummary.tokenSlug` | string | 1 |
| `$1f[].children[][].children[].children[].tokenId` | string | 1 |
| `$1f[].children[][].children[].children[].tokenLatestUpdatedAt` | number | 1 |
| `$1f[].children[][].children[].children[].socialLinkList[].tokenId` | string | 2 |
| `$1f[].children[][].tokenUpdatedAt` | number | 1 |
| `$1e[][].children[][].trendingTokenList` | array | 1 |
| `$1e[][].children[][].trendingTokenList[].tokenId` | string | 10 |
| `$1e[][].children[][].trendingTokenList[].tokenName` | string | 10 |
| `$42[].trendingTokenList` | string | 1 |
| **family** — `$54[]…user.permissions.r_*` (33 paths, e.g. `r_token_vesting_schedule_chart`, `r_dashboard_upcoming_unlock`) | boolean | 33 |
| **family** — `…analytic.params.token` under `$77[]`, `$7f[]`, `$8e[]`–`$93[]` (10 paths) | string, one array | 10 |
| **family** — `…style.backgroundColor` under `$30[]` (2 paths) | string | 2 |

- **Funding-round shape: present.** `tokenSummary.raiseAmount` is a number at a stable key
  path in the served HTML.
- **Vesting-schedule shape: absent.** The only unlock-schedule key served is
  `isUnlockScheduleEmpty`, a boolean *about* a schedule, not a schedule. There is no array
  of dated tranches anywhere in the served bytes. Confirmed by a raw key-name search over
  the **full** HTML — which covers the 110 rows that did not parse as well:

```
for k in unlockSchedule vestingSchedule unlocks tranche allocations nextUnlock upcomingUnlock unlockDate emissionSchedule; do
  printf '%-20s %s\n' "$k" "$(grep -o -F "\"$k\"" tokenomist-page.html | wc -l)"; done
```

```
unlockSchedule       0
vestingSchedule      0
unlocks              0
tranche              0
allocations          0
nextUnlock           0
upcomingUnlock       0
unlockDate           0
emissionSchedule     0
```

  The names `unlockEvents`, `fundingRounds` and `investors` DO occur in the flight stream —
  3, 2 and 2 times — and every occurrence is an i18n key under
  `$47[].messages.TokenDetail.*` (`…components.unlockEvents`, `…tabs.unlockEvents`,
  `…fundraisingTab.fundingRounds`, `…fundraisingTab.investors`). They are label
  namespaces, not data containers. The `r_*` permission booleans under `$54[]` name
  vesting and unlock FEATURES — a per-user entitlement map — and carry no schedule either.
- The `ld+json` blocks contain **0** candidate key paths: they are breadcrumb, graph and
  FAQ metadata.

### §3.2 — Extractability probe, `cryptorank.io`

**Page source — composed from two of the host's own documents, no segment guessed.** The
path-and-query SHAPE is the first `Allow:` line of `robots.txt`, verbatim; the two slugs
that fill it are `<loc>` entries from the host's fund sitemap. The sitemap index was
fetched first:

```
curl -sS --connect-timeout 15 --max-time 45 -o cryptorank-sitemap.xml -D cryptorank-sitemap.hdr \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download}\n' \
  https://cryptorank.io/sitemap.xml
```

`http_code=200 content_type=application/xml size_download=6546`, exit `0`, MD5
`7bde03f5967fe87519f74767be802f81` — a `<sitemapindex>` of 90 child sitemaps, of which
`sitemap-fund.xml` is the funds set. It was fetched:

```
curl -sS --connect-timeout 15 --max-time 45 -o cryptorank-sitemap-fund.xml -D cryptorank-sitemap-fund.hdr \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download}\n' \
  https://cryptorank.io/sitemap-fund.xml
```

`http_code=200 content_type=application/xml size_download=7374906`, exit `0`, MD5
`b6d2b9260039670a717138c61adc5f8c`, **7 000** `<loc>` entries in five path shapes:
`<slug>` (1 731), `<slug>/rounds` (1 709), `<slug>/portfolio` (1 711), `<slug>/analytics`
(1 702), `<slug>/team` (147).

**The host publishes no URL of the allowed query shape** — `0` of the 7 000 `<loc>`
entries carry a query string, and the literal `filterKey` appears `0` times in either the
index or the fund sitemap. The probed URL was therefore composed rather than copied, and
each of its three variable parts is sourced:

| Part | Value | Source, verified |
|---|---|---|
| shape | `/funds/*/rounds?filterType=coFunds&filterKey=*` | `robots.txt` `Allow:` line 1, verbatim |
| path slug | `pantera-capital` | `grep -c '<loc>https://cryptorank.io/funds/pantera-capital/rounds</loc>' -> 1` |
| `filterKey` slug | `coinbase-ventures` | `grep -c '<loc>https://cryptorank.io/funds/coinbase-ventures</loc>' -> 1` |

`filterType` is fixed by the `Allow:` pattern itself and admits no choice; `filterKey`'s
value is a `*` in the pattern, and the value used is a fund slug taken from the host's own
sitemap rather than invented. Parameter order follows the `Allow:` line exactly —
`filterType` first — so the URL matches the longest allowed pattern and is not caught by
`Disallow: /*?*`.

**Probe command, exactly as it ran:**

```
curl -sS --connect-timeout 15 --max-time 45 -o cryptorank-page.html -D cryptorank-page.hdr \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download} time_total=%{time_total}\n' \
  'https://cryptorank.io/funds/pantera-capital/rounds?filterType=coFunds&filterKey=coinbase-ventures'
```

**Result:** `http_code=200 content_type=text/html; charset=utf-8 size_download=329900 time_total=0.752045`,
curl exit `0`. MD5 `f9569bdeaca70f04d9bf832c7881d799`. No managed challenge.
`cf-cache-status: BYPASS`, `x-cache-status: MISS`, `x-cr-via: R03`, `x-build-id: 2adc03fd`.

**Does the HTML contain a structured payload, and which kind?**

```
__NEXT_DATA__                1
self.__next_f.push           0
application/ld+json          3
type="application/json"      1
<script                      35
```

- **A `__NEXT_DATA__` payload** — `<script id="__NEXT_DATA__" type="application/json">`,
  the Pages Router shape, the mirror image of the other host. Extracted and parsed with a
  regex and `json.loads`: **43 757 bytes**, parses cleanly, MD5
  `7ab107d1397fc8c627fa870f057242b1`.
- **Three `<script type="application/ld+json">` elements** — here the literal count and
  the element count agree at 3, since there is no flight stream to describe them a second
  time.

**Payload sizes and top-level key names.**

`__NEXT_DATA__`, 43 757 B, 13 top-level keys:

```
assetPrefix · buildId · defaultLocale · dynamicIds · gssp · isExperimentalCompile ·
isFallback · locale · locales · page · props · query · scriptLoader
```

`props` → `__N_SSP`, `pageProps`. `props.pageProps` → four keys, all server-rendered:

| Key path | JSON type | Sub-structure |
|---|---|---|
| `props.pageProps.fallbackRounds` | object | `blocked` (string), `data` (array), `total` (number) |
| `props.pageProps.fund` | object | 17 keys, incl. `investments`, `topInvestments`, `roi`, `tier`, `slug` |
| `props.pageProps.initData` | object | `globalData`, `intlMessages`, `locale`, `routeTemplate`, `seoTemplates`, `theme` |
| `props.pageProps.initialQueryParams` | object | `filters`, `limit`, `skip`, `sortingColumn`, `sortingDirection` |

The three `ld+json` blocks:

| Block | Bytes | Parses | Top-level keys |
|---:|---:|---|---|
| 1 | 513 | yes | `@context`, `@type`, `itemListElement` |
| 2 | 365 | yes | `@context`, `@id`, `@type`, `logo`, `name`, `sameAs`, `url` |
| 3 | 528 | yes | `@context`, `@id`, `@type`, `description`, `image`, `name`, `publisher`, `url` |

**Does any key path have the shape of a vesting schedule or a funding round?** The same
walk, with `amount|valuation|date` added to the candidate expression. **51 candidate
paths**, of which 46 lie under `initData.intlMessages` / `initData.seoTemplates` — again
the label catalogue. The 5 outside it are the data surface:

| Key path | JSON type | Count |
|---|---|---:|
| `$.props.pageProps.fallbackRounds` | object | 1 |
| `$.props.pageProps.fallbackRounds.data[].date` | string | 20 |
| `$.props.pageProps.fund.investments` | number | 1 |
| `$.props.pageProps.fund.topInvestments` | array | 1 |
| `$.props.pageProps.fund.topInvestments[].raise` | number | 5 |

`fallbackRounds.data` is an array with **20 elements served** — the page size named by
`initialQueryParams.limit`, not a count of anything in the world. Every element carries
the same five keys:

| Key path | JSON type |
|---|---|
| `fallbackRounds.data[].category` | object |
| `fallbackRounds.data[].date` | string |
| `fallbackRounds.data[].icon` | string |
| `fallbackRounds.data[].key` | string |
| `fallbackRounds.data[].name` | string |

- **Funding-round shape: present, twice, and the two are not equivalent.**
  `fallbackRounds.data[]` is a list of dated round records — but its element schema has
  **no amount, valuation, or investor key at all**. Round TERMS are absent from this
  array; only the round's date and identity are served. Separately,
  `fund.topInvestments[].raise` IS a number, present five times.
  `fallbackRounds.blocked` exists as a string key alongside the data; its value is not
  reported here, and the structural fact that stands on its own is the missing terms in
  the element schema.
- **Vesting-schedule shape: absent** — as expected on a funds page; no `unlock`, `vest`,
  `cliff` or `schedule` key occurs outside the label catalogue.

### §3.3 — The prohibition, and how it was kept

**No value from either probed page body appears anywhere in this report.** Every figure
above is one of: a byte count, an HTTP status, an element or key count, a JSON type name,
a key name, a key path, an MD5 of a locally stored artifact, or a curl exit code. No date,
no amount, no percentage, no price, no coin symbol paired with a number, rounded or
otherwise, was carried out of either body.

**The first-400-bytes quote TZ-22 used was checked before being reproduced, not assumed
either way.** On both hosts those bytes turn out to be `<head>` boilerplate carrying no
product fact — measured, not asserted:

```
head -c 400 <page> | grep -o -E '<[a-zA-Z!][a-zA-Z0-9-]*' | sort | uniq -c
```

| Page | Tags in the first 400 B | `<title>` | `og:description` | `name="description"` |
|---|---|---:|---:|---:|
| `tokenomist.ai` | `<!DOCTYPE` `<html` `<head` `<meta`×3 `<link` | 0 | 0 | 0 |
| `cryptorank.io` | `<!DOCTYPE` `<html` `<head` `<meta`×3 `<link` `<script` | 0 | 0 | 0 |

Since the quote carries no value on either host, it is reproduced:

```
<!DOCTYPE html><html lang="en" data-scroll-behavior="smooth" class="inter_a286ccd6-module__kdUgHa__variable dm_mono_49de4911-module__mPbA6a__variable scroll-smooth"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="preload" as="image" imageSrcSet="https://imgproxy.tokenom
```

```
<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1" class="jsx-2713653309"/><meta name="cryptomus" content="2a743b3d" class="jsx-2713653309"/><link rel="preload" href="/static/fonts/inter/latin.woff2" as="font" type="font/woff2" crossorigin="anonymous" class="jsx-2713653309"/><script type="application/ld+json">{"@context":
```

**One quote was withheld, and the reason is measured too.** `ld+json` block 3 on
`tokenomist.ai` (2 867 B) is `"@type": "FAQPage"`; its `mainEntity` is a 9-element list of
`Question` objects, each with `name` and `acceptedAnswer.text`. On an unlock-events page
those answer strings carry product facts, so **only the block's byte size, top-level keys
and element schema are stated and no string from it is quoted** — §3.3 exactly.

The two `robots.txt` files are quoted in full, as §3.1 requires. They are permission
documents, not probed bodies in the §3.3 sense, and the TZ mandates the quotation
explicitly.

### §3.4 — Controls

| # | Control | Command, exactly as it ran | Result | Exit | Reading | Required |
|---:|---|---|---|---:|---|---|
| 1 | positive | `curl -sS --connect-timeout 15 --max-time 90 -o ctrl1.out -D ctrl1.hdr -w '…' https://api.llama.fi/protocols` | `http_code=200 content_type=application/json size_download=8692626 time_total=0.101748` | `0` | **`open`** | `open` ✔ |
| 2 | negative, DNS layer | `curl -sS --connect-timeout 15 --max-time 45 -o ctrl2.out -D ctrl2.hdr -w '…' https://this-host-does-not-exist-tz24.invalid/` | `curl: (6) Could not resolve host: this-host-does-not-exist-tz24.invalid`, `http_code=000 size_download=0 time_total=0.001173` | `6` | **`unreachable`** | `unreachable`, at name resolution ✔ |
| 3 | negative, CONNECT layer | `curl -sS --connect-timeout 15 --max-time 45 -o ctrl3.out -D ctrl3.hdr -w '…' https://192.0.2.1/` | `curl: (28) Failed to connect to 192.0.2.1 port 443 after 15002 ms: Timeout was reached`, `http_code=000 size_download=0 time_total=15.002184` | `28` | **`unreachable`** | `unreachable`, at connection ✔ |

**The two negative controls are distinguished by evidence, not by assertion.** Control 2
exits **6** (`CURLE_COULDNT_RESOLVE_HOST`) after 1.2 ms; control 3 exits **28**
(`CURLE_OPERATION_TIMEDOUT`) after 15.002 s, and curl's own message names the phase —
`Failed to connect to 192.0.2.1 port 443`. Control 3's target is a literal address, so no
name lookup occurs at all and resolution cannot be the failing layer; the failure is
inside the TCP connect, bounded by `--connect-timeout 15`. **The codes differ, so control
3 did its job** and the instrument is now known to return `unreachable` for a
connect-layer failure as well as a DNS-layer one — the distinction TZ-22 could not draw.

One precision the Architect should have: the connect failed by **timeout**, not by
refusal. `192.0.2.1` is RFC 5737 TEST-NET-1 and is blackholed rather than actively
rejecting, so the code is 28 and not 7 (`CURLE_COULDNT_CONNECT`). A refused CONNECT — the
old cloud sandbox's signature — would read 7. Control 3 therefore proves the instrument
distinguishes *resolution* from *connection*; it does not, on its own, separate a
blackholed connect from a refused one.

Control 1 is TZ-22's, unchanged: same URL, same flags, same client and same host. It read
200 with 8 692 626 B of JSON here against 8 693 658 B there — a difference in the
publisher's payload between the two runs, not in the instrument.

### §3.5 — Method compliance

| Rule | How it was kept |
|---|---|
| Default client only | No `-A`, no `--user-agent`, no cookie jar, no proxy, no TLS or browser impersonation appears in any command above. Every command is printed in full and can be checked. The UA was read out of curl's own `-v` trace, not by asking a third party to echo it. |
| Every probe runs once | **Ten** requests total, each issued exactly once: 2 `robots.txt` + 3 sitemaps + 2 pages + 3 controls. No request was repeated, no probe was re-run after a disagreeable answer, and nothing was retried. |
| ≤1 request per second per host | Each request was issued in its own shell invocation, separated by seconds of analysis. `tokenomist.ai` received 3 requests over 60 s (`20:42:33` → `20:43:33` by response `date:` headers); `cryptorank.io` received 4 over 223 s (`20:42:48` → `20:46:31`). |
| Commands printed beside results | Every command in this section appears verbatim with its `-w` output and exit code. |
| A challenge or refusal is the reading | Neither host issued one. Had either done so, it would have been recorded as the reading and no second attempt made. |
| `Disallow` honoured, never tested | No disallowed path was fetched on either host. On `cryptorank.io` the query-bearing URL was chosen specifically to match an explicit `Allow:` line rather than to probe the blanket `Disallow: /*?*`. |

---

## Test Results

### Acceptance criteria (TZ §5)

| # | Criterion | Result | Evidence |
|---:|---|---|---|
| 1 | Both `robots.txt` read in full; named-agent group quoted verbatim or its absence stated | **PASS** | 1 281 B / 57 lines and 1 843 B / 39 lines, both quoted end to end; `tokenomist.ai` group 2 reproduced in full; `cryptorank.io` absence stated and verified by `grep -c '^User-Agent:' -> 1` |
| 2 | The run's own User-Agent recorded, and the group it fell into named | **PASS** | `> User-Agent: curl/8.5.0` from curl's `-v` trace on both hosts; group `*` on both |
| 3 | One page probed per host, sourced from the host's own documents, payload structure reported | **PASS** | `tokenomist.ai` `<loc>` verified present before fetch; `cryptorank.io` shape from `robots.txt` `Allow:` line 1 and both slugs verified present in `sitemap-fund.xml` |
| 4 | No value from any probed body in the report | **PASS** | Only counts, sizes, statuses, types, key names, key paths, MD5s and exit codes appear; the one quote withheld (`tokenomist.ai` FAQ block) is named with its reason |
| 5 | All three controls read as §3.4 requires, exit codes proving different layers | **PASS** | `open` / exit 0; `unreachable` / exit 6 at 1.2 ms; `unreachable` / exit 28 at 15.002 s naming port 443 |
| 6 | Two verdict lines per host, in the §4 vocabulary, never combined | **PASS** | four lines below, each answering exactly one question |
| 7 | No path guessed; no evasion technique; every command printed | **PASS** | sourcing table per host above; no UA, cookie, proxy or impersonation flag in any command; 10 commands printed verbatim |
| 8 | `git status --porcelain` shows exactly one file | **PASS** | see `## Final Repository State` |
| 9 | `## Final Repository State` silent on this report's own commit and push; `## Pull Request` carries the fixed report-only line | **PASS** | both sections below |

### Verdicts (TZ §4 item 5) — two per host, never combined

**`tokenomist.ai`**

- **permission: `admitted by name`**
- **extractability: `machine-locatable without JS`**

**`cryptorank.io`**

- **permission: `not addressed by name`**
- **extractability: `machine-locatable without JS`**

**What each verdict does and does not say.** The permission verdict answers only what the
file says about a named agent. The extractability verdict answers only the §3.2 question —
whether a machine can LOCATE a structured payload in the served HTML without executing
JavaScript. On both hosts it can: a `curl` fetch plus a regex plus `json.loads`, no
browser, no JS engine, yields a parsing payload of 352 138 B and 43 757 B respectively.

**The verdict is not a statement that the sweep's data is there, and on `tokenomist.ai` it
is not.** The single most consequential structural finding of this run is that the page
named `/sui/unlock-events` serves **no unlock schedule**: the only schedule-related key in
617 540 bytes is the boolean `isUnlockScheduleEmpty`, and nine independent schedule key
names return zero occurrences across the full HTML. A vesting sweep specified against that
page would locate a payload on every run and find no tranche in it. The corresponding
finding on `cryptorank.io` is narrower and of the same kind: `fallbackRounds.data[]` serves
dated round records whose element schema carries no amount, valuation or investor key, so
round TERMS are not in the served HTML even though round dates are. Both facts are stated
here rather than folded into a label, because combining them with the verdict would be the
methodology decision §4 reserves for the Architect.

---

## Deviations

**None.** The specification was executed as written.

Three method notes, none of which departs from the TZ:

1. **Three sitemap fetches were made in addition to the two page probes.** §3.2 requires
   the page be sourced from the host's own documents; the sitemaps ARE those documents, and
   fetching them is what "never guessed" means in practice. The extractability probe
   remains one page per host, as §3.2 and criterion 3 require.
2. **`cryptorank.io`'s probed URL was composed, not copied.** The host publishes no URL of
   the allowed query shape — 0 of 7 000 `<loc>` entries carry a query — so the shape came
   from `robots.txt` and both slugs from `sitemap-fund.xml`, each verified present before
   the fetch. Every variable part is sourced; nothing was invented.
3. **The session's checkout was moved to `origin/main`'s commit before any work.** It began
   on the merged TZ-21 branch and at a commit predating TZ-22's report; the gates and
   fingerprints demand the current tree. `main` itself is checked out in another worktree
   on this machine, so the move was made in **detached HEAD** at `c3afaf5`. No branch was
   opened — a detached HEAD is not one — and the class of this TZ is unaffected.

---

## Pre-existing Issues

**1. TZ-22's report truncated `tokenomist.ai/robots.txt` mid-group, and the truncation
landed three lines short of the directives.** The 400-byte cut falls inside group 2's
`User-Agent:` list, so the report shows six named agents and none of the three directives
that govern them. This is the defect TZ-24 exists to repair and it is now repaired; it is
recorded here because the earlier report remains in `CryptoReports/` unedited, as §13
requires, and a reader of that file alone would still not know what the group permits.

**2. No workflow gates a `CryptoReports/**` commit, and this is by design, not by
accident.** Verified rather than assumed, per contract §8:

```
grep -n "'\*\*.md'" .github/workflows/main.yml .github/workflows/bench.yml
main.yml:19:      - '**.md'
bench.yml:34:      - '**.md'
```

Both workflows carry `'**.md'` under `paths-ignore`, `calib.yml` triggers only on
`claude/**` pushes touching two named non-Markdown paths, `journal.yml` is cron and
dispatch, and `backtest_bench.yml` is dispatch only. A commit whose only changed path is a
`.md` file under `CryptoReports/` starts nothing, and Pages serves `index.html`, which this
commit does not touch. Both halves of §8's safety claim hold.

**3. `bench/catalyst_bench.js` names neither probed host on its `PRIMARY` allow-list, and
nothing in this run changes that.** Recorded so the boundary is explicit: hard floor item
13 was not approached, no host was added, removed or loosened, and neither aggregator has
gained any standing in the registry from this measurement.

---

## Remaining Risks

1. **The extractability vocabulary has no term for "payload present, sought data absent",
   and this run produced exactly that on both hosts.** `machine-locatable without JS` is
   the accurate answer to the §3.2 question and it is what is recorded — but a reader who
   consults only the verdict lines would conclude that `tokenomist.ai` can serve the
   vesting sweep, and it cannot: no tranche array is in the served HTML. The four permitted
   values cannot express the distinction, so it is stated in prose above instead of being
   compressed into a label. **This is a finding routed to the Architect, not a deviation
   and not a fifth value invented on my own reading** (contract §12): if a fifth term is
   wanted, it belongs in the next TZ's vocabulary table.
2. **`admitted by name` on `tokenomist.ai` is a reading of `robots.txt`, and `robots.txt`
   is not the whole of a host's terms.** The file grants `Allow: /` to a group naming
   `ClaudeBot`, `Claude-SearchBot`, `anthropic-ai` and `Claude-User`. It says nothing about
   the site's terms of service, its API licensing, or the rate at which automated access is
   tolerated. Naming the host in §6a on this reading alone would repeat, one layer up, the
   mistake TZ-22's reachability reading would have made.
3. **`not addressed by name` on `cryptorank.io` is neither permission nor refusal.** The
   host's only group is `*`, which this run fell into and which grants everything outside
   nine `Disallow:` patterns. An agent operating under a Claude name would fall into the
   same group. That is a fact about the file's silence, and the Architect should not read
   it as either an invitation or a denial.
4. **Both readings are a snapshot.** `cryptorank.io`'s file carries
   `last-modified: Fri, 14 Aug 2026 07:36:06 GMT`; `tokenomist.ai`'s is served with
   `cache-control: public, max-age=120` and no stable `last-modified`. A `robots.txt`
   changes without notice, and inv. 52 applies to permission exactly as it applies to
   reachability: a rule resting on a measurement falls with it. If §6a names either host, a
   re-read on a schedule is what keeps the naming honest.
5. **Both payloads are private page structure, not a published contract.** `__NEXT_DATA__`
   key paths and RSC row ids change when the site is rebuilt — `cryptorank.io` served
   `x-build-id: 2adc03fd` on this run. A sweep keyed to `props.pageProps.fallbackRounds`
   would break silently on the host's next deploy, with no version to pin and no
   deprecation notice. This is a property of scraping rendered applications and is not
   improved by either verdict above.
6. **Neither host's data API was touched, and that remains the Boss's decision** (TZ §8).
   Both are credentialed, the repository holds no key, and nothing in this run acquired,
   requested or implied one.

---

## Commit

One commit, one file, direct to `main` on the `CryptoReports/**` path (contract §8).
Message, verbatim from TZ §7:

```
docs(discovery): measure permission and extractability at tokenomist.ai and cryptorank.io (TZ-24)
```

Contents: `CryptoReports/TZ-24-discovery-host-permission-and-extractability-report.md`,
created. No other path is in the commit. Per contract §10 this section carries the message
and the contents and no outcome: the commit that stores this report has not been made at
the time these words are written, so it has no hash to record here (inv. 54).

---

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

---

## CI Execution

**No workflow ran, and none can.** This TZ opened no branch and pushed no code path. The
repository's five workflows and their triggers were read from the working tree and are
quoted under `## Pre-existing Issues` item 2: `main.yml` and `bench.yml` both list
`'**.md'` under `paths-ignore`, `calib.yml` fires only on `claude/**` pushes touching
`bench/exhaustion_calib.py` or its own file, and `journal.yml` and `backtest_bench.yml` are
schedule- and dispatch-driven. A commit changing one `.md` file under `CryptoReports/`
clears no workflow's path filter.

No local bench was run either: no production file changed, so the standing checks
(`python3 -m py_compile main.py`, `node --check` on the extracted `<script>` block) have
nothing to gate. The gate's last recorded state is the one the map's `## 0` block pins —
`bench.yml`, 13 steps, 1 250 739 checks, green on `Bench gate` #110 on head `8069341` — and
this run neither moved it nor re-measured it.

---

## Final Repository State

The session leaves a **detached HEAD at `c3afaf5`** (`Add files via upload`), the tip of
`origin/main` as of this run's fetch. This is the checkout every fingerprint below was
taken against. No branch was created, and the pre-existing local branch
`claude/tz-21-catalyst-registry-scope-and-basis` was left untouched at `8069341`.

The working tree holds exactly one changed path — the report itself:

```
git status --porcelain
?? CryptoReports/TZ-24-discovery-host-permission-and-extractability-report.md
```

All probe artifacts live in `/tmp/tz24/`, outside the repository, and are not committed;
`.gitignore` is unmodified and no scratch file was left in the tree.

---

## Fingerprints

Measured on the checkout named above.

| File | Lines | MD5 | Required by map `## 0` | Match |
|---|---:|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1649 | `c00586e116aa89916ca2ff3f3807d073` | not fingerprinted by itself | — |
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | 3729 / `fdf331906bf205944b25e3635135789c` | ✔ |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | 506 / `1a5a5d98b2fd76010f202ee3eebaa717` | ✔ |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | ✔ |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | ✔ |

Map revision string found: **`Revision 2026-08-30-e.`** — identical to the revision the
TZ header requires. All four fingerprinted files match at both line count and MD5, so
nothing is reported under `## Pre-existing Issues` on that account.

Files this TZ's gates add, fingerprinted for the same reason:

| File | Lines | MD5 | Gate |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 693 | `3d73f4ddbf3bdb8eb0b94547c101b6a0` | TZ §0 second gate — reads `**Version 15.**` ✔ |
| `ANALYST-INSTRUCTIONS.md` | 771 | `63c15842a0d0524e4acf812966bd338d` | TZ §6 — both §6a clauses present verbatim ✔ |

Probe artifacts, fingerprinted so the measurement is reproducible from the commands above.
They are stored in `/tmp/tz24/` and are not part of the repository.

| Artifact | Bytes | MD5 |
|---|---:|---|
| `tokenomist-robots.txt` | 1 281 | `555e106c25119795f3a40bcc22930ec1` |
| `tokenomist-sitemap.xml` | 1 019 179 | `43b2d14de8bad490674f363a8e722b3b` |
| `tokenomist-page.html` | 617 540 | `729cd5350155a4106cd708b260a9891e` |
| `tokenomist-flight.txt` (reconstructed) | 352 138 | `dee793fb592fe196b8f34d3eb9c562b7` |
| `cryptorank-robots.txt` | 1 843 | `f8dad7387c5ee89ec0fb63ecfa4eea3e` |
| `cryptorank-sitemap.xml` | 6 546 | `7bde03f5967fe87519f74767be802f81` |
| `cryptorank-sitemap-fund.xml` | 7 374 906 | `b6d2b9260039670a717138c61adc5f8c` |
| `cryptorank-page.html` | 329 900 | `f9569bdeaca70f04d9bf832c7881d799` |
| `cryptorank-nextdata.json` (extracted) | 43 757 | `7ab107d1397fc8c627fa870f057242b1` |
| `ctrl1.out` (DeFiLlama control body) | 8 692 626 | `9e29d25125c7dae099c1a418c4932ab0` |
