# Implementation Report — TZ-22

**Egress measurement: `tokenomist.ai`, `cryptorank.io`**

## Status

COMPLETED.

Both target hosts were probed, both controls read as the TZ requires, and the run
wrote exactly one file — this report. No path was guessed, no evasion technique
appears in any command, and no market fact from any probed body is stated here as a
fact about the market.

---

## Inbound Filing

The TZ was already filed at its canonical path when the session started; nothing was
moved or renamed.

| Item | Value |
|---|---|
| Path | `CryptoTZ/TZ-22-egress-measurement.md` |
| Arrived in | `7dfaa4e` — `Add files via upload`, 2026-08-30 21:28:29 +0400 |
| MD5 | `1a22288269a8a6cf62833aa30c7566b6` (157 lines) |

---

## Scope Executed

TZ §2 authorises exactly one written file and no repository file change. That is what
happened.

- §3.1 — six probes against `tokenomist.ai` and against `cryptorank.io`.
- §3.2 — both mandatory controls.
- §3.3 — one classification label per endpoint, decided by the body.
- §4 — the report, with every command, both controls, the first 400 bytes of every 2xx
  body, the run's UTC timestamp and the machine.
- §6 — hard floor item 9 read from the repository before the first probe (below).

Not executed, because the TZ forbids it: no branch, no pull request, no production
file, no bench, no workflow, nothing under `analyst/`, no market analysis.

---

## Files Created

| File | Purpose |
|---|---|
| `CryptoReports/TZ-22-egress-measurement-report.md` | this report — it **is** the measurement record |

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Gate before the first probe — TZ §6

TZ §0 makes this TZ BLOCKED if the repository's `EXECUTOR-INSTRUCTIONS.md` still
forbids an in-session fetch outright. It does not. The repository copy is **Version
14**, and hard floor item 9 carries the amended clause verbatim:

> **Measuring the session's own environment is a DIFFERENT act and is permitted** —
> egress, tool availability, host reachability — provided the command is recorded beside
> its result, because there the artifact IS the measurement and re-running the command is
> the reproduction.

The same clause is the map's inv. 44 in its rewritten form. The permission is bounded,
and both bounds were held: hard floor item 2 (nothing was edited so that a probe
passed — nothing was edited at all) and `ANALYST-INSTRUCTIONS.md` §6 (a refusal or a
challenge is the reading, never an obstacle to route around).

### Environment — the machine this was measured on

| Fact | Value | Command |
|---|---|---|
| Run start (UTC) | `2026-08-30T18:07:33Z` | `date -u '+%Y-%m-%dT%H:%M:%SZ'` |
| Run end (UTC) | `2026-08-30T18:11:43Z` | `date -u '+%Y-%m-%dT%H:%M:%SZ'` |
| Hostname | `vultr` | `hostname` |
| Kernel | `Linux 6.8.0-136-generic x86_64` | `uname -srm` |
| OS | `Ubuntu 24.04.4 LTS` | `head -2 /etc/os-release` |
| Client | `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13` | `curl --version \| head -2` |
| Proxy | none — no proxy variable is set | `env \| grep -Ei 'proxy'` (no output) |
| DNS tooling | `dig`, `host`, `nslookup`, `getent`, `python3` all present | `command -v <tool>` |

This is the Vultr VPS the map's §11 names, not a runner and not the old cloud sandbox.
A reading here is a fact about **this** machine's egress and about nothing else
(inv. 44, inv. 52).

### Method — what was and was not done

- **Default client only.** No `-A`/`--user-agent`, no browser impersonation, no cookie
  jar, no `--proxy`, no TLS fingerprint manipulation. Every command below is exactly
  what ran.
- **No retry into success.** Every probe ran once. No probe was repeated after a
  disagreeable answer; nothing needed a second attempt.
- **Rate.** Each HTTP request to a given host was issued in its own shell invocation,
  separated by seconds of session turnaround, so the one-request-per-second-per-host
  ceiling was never approached. The whole run is 13 HTTP requests over 4 minutes 10
  seconds.
- **Probe 5 was sourced, never guessed.** For each host the endpoint came from a
  document the host itself serves — its `robots.txt`, or its own linked docs site. The
  sourcing fetches are listed as probes in their own right rather than hidden, because
  they were requests this machine made.
- **A `Disallow` was honoured, not tested.** `tokenomist.ai/robots.txt` names `/api/`
  only to forbid it. Fetching it would have been routing around a refusal the host had
  already stated, which `ANALYST-INSTRUCTIONS.md` §6 forbids — so it was not fetched,
  and the host's own docs site was read instead, where a concrete endpoint is published.

### What the probes established

**`tokenomist.ai`** — DNS resolves apex and `www` to Cloudflare addresses, TLS 1.3
completes with a valid certificate, the rendered page returns 200 with 792 012 bytes of
real Next.js HTML and no challenge marker, `robots.txt` names a sitemap and the sitemap
serves 1 019 179 bytes of `application/xml`. The documented data endpoint —
`https://api.tokenomist.ai/v4/token/list`, published on the host's own docs site —
answers 401 `{"errorMessage":"x-api-key not found"}`. The lane is open for reading the
site; the data API is credentialed and this repository holds no key.

**`cryptorank.io`** — DNS resolves apex and `www` to Cloudflare addresses, TLS 1.2
completes with a valid certificate, the rendered page returns 200 with 397 830 bytes of
real HTML and no challenge marker, `robots.txt` names two sitemaps and no API path. The
host's docs site names `https://api.cryptorank.io/v3/documentation-json`, which answers
200 with a 422 593-byte OpenAPI 3.0.0 document declaring 76 paths, a single security
scheme `X-Api-Key`, and `/v3/ping` as requiring no key. `/v3/ping` answers 200 with
`{"serverTime":…}`. Both the site and its API answer this machine.

Neither host produced a `challenged` or an `unreachable` reading. The distinction §3.3
exists to draw was still exercised — by the controls, and by the 401, which is the one
`refused` reading in the run.

---

## Validation

### 1. System Map fingerprint gate (contract §5) — PASS

Run against `origin/main` after `git fetch --all --prune`. Every anchor matched as an
exact substring:

```
for a in ...; do grep -qF "$a" SYSTEM-MAP-CRYPTOCALCUL.md && echo OK || echo MISS; done
```

| Anchor | Result |
|---|---|
| `**Revision 2026-08-30-c.**` | OK |
| `### 3.12 Direction engine — veto cascade` | OK |
| `### 3.15 Catalyst registry` | OK |
| `### 3.16 List exhaustion — the day-range measure` | OK |
| `## 11. Analytical engine` | OK |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | OK |
| `55. **A specification is checked against the text it must obey, never against memory of it.**` | OK |

File table at revision `2026-08-30-c` — every file matches the map's stated line count
and MD5, so nothing is ahead of anything:

| File | Lines | MD5 | Map states |
|---|---:|---|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | identical |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | identical |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | identical |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | identical |

### 2. Repository state (contract §4a step 6)

```
git log --oneline --graph --all -12
```

TZ-21's branch `claude/tz-21-catalyst-registry-scope-and-basis` was merged into `main`
as `edd650c` (pull request #21); its implementation commit is `8069341`. The base for
this work is therefore merged, not pending. The working tree was clean at start
(`git status --porcelain` — no output) and the session worked from a detached checkout
of `origin/main` at `41386ad`.

### 3. The measurement

#### 3.1 Probe matrix — every cell filled

`tokenomist.ai`:

| # | Probe | Status | Body | Label |
|---:|---|---|---|---|
| 1 | DNS apex | `NOERROR` — `104.20.36.234`, `172.66.155.227` | — | resolved |
| 1 | DNS `www` | `NOERROR` — `172.66.155.227`, `104.20.36.234` | — | resolved |
| 2 | TLS CONNECT :443 | `CONNECTION ESTABLISHED`, TLSv1.3, `CN = tokenomist.ai`, `Verification: OK` | — | connected |
| 3 | `GET /` | 200 · `text/html; charset=utf-8` | 792 012 B | **`open`** |
| 4 | `GET /robots.txt` | 200 · `text/plain` | 1 281 B | **`open`** — names `Sitemap: https://tokenomist.ai/sitemap.xml`; names `/api/` **only as `Disallow`** |
| 5a | `GET /sitemap.xml` (named by `robots.txt`) | 200 · `application/xml` | 1 019 179 B | **`open`** |
| 5b | `GET https://docs.tokenomist.ai/` (linked by the rendered page) | 308 → `/overview` | 91 003 B | redirect |
| 5c | `GET https://docs.tokenomist.ai/overview` | 200 · `text/html; charset=utf-8` | 281 693 B | **`open`** — names `https://api.tokenomist.ai/v4/token/list` and an `x-api-key` header |
| 5d | `GET https://api.tokenomist.ai/v4/token/list` (named by 5c) | 401 · `application/json` | 119 B | **`refused`** |
| 6 | first 400 bytes of every 2xx body | — | — | quoted below |

`cryptorank.io`:

| # | Probe | Status | Body | Label |
|---:|---|---|---|---|
| 1 | DNS apex | `NOERROR` — `172.67.68.214`, `104.26.0.70`, `104.26.1.70` | — | resolved |
| 1 | DNS `www` | `NOERROR` — `104.26.1.70`, `104.26.0.70`, `172.67.68.214` | — | resolved |
| 2 | TLS CONNECT :443 | `CONNECTION ESTABLISHED`, TLSv1.2, `CN = cryptorank.io`, `Verification: OK` | — | connected |
| 3 | `GET /` | 200 · `text/html; charset=utf-8` | 397 830 B | **`open`** |
| 4 | `GET /robots.txt` | 200 · `text/plain; charset=UTF-8` | 1 843 B | **`open`** — names `Sitemap: https://cryptorank.io/sitemap.xml` and `Sitemap: https://cryptorank.io/sitemap-google-news.xml`; **no API path** |
| 5a | `GET https://docs.cryptorank.io/` (linked by the rendered page) | 200 · `text/html; charset=utf-8` | 267 551 B | **`open`** — names `https://api.cryptorank.io/v3/documentation-json` |
| 5b | `GET https://api.cryptorank.io/v3/documentation-json` (named by 5a) | 200 · `application/json; charset=utf-8` | 422 593 B | **`open`** |
| 5c | `GET https://api.cryptorank.io/v3/ping` (named by the OpenAPI document as needing no key) | 200 · `application/json; charset=utf-8` | 28 B | **`open`** |
| 6 | first 400 bytes of every 2xx body | — | — | quoted below |

Nothing is `not run`. No probe was skipped and none was attempted twice.

#### 3.2 The exact commands — copy-pasteable

DNS (probe 1, both hosts and the invalid control):

```
for n in tokenomist.ai www.tokenomist.ai cryptorank.io www.cryptorank.io this-host-does-not-exist-tz22.invalid; do
  dig "$n" A +noall +comments +answer
done
getent hosts this-host-does-not-exist-tz22.invalid
```

TLS CONNECT (probe 2):

```
openssl s_client -connect tokenomist.ai:443 -servername tokenomist.ai -brief </dev/null
openssl s_client -connect cryptorank.io:443 -servername cryptorank.io -brief </dev/null
openssl s_client -connect this-host-does-not-exist-tz22.invalid:443 -servername this-host-does-not-exist-tz22.invalid -brief </dev/null
```

HTTP (probes 3, 4, 5 and both controls). Every one of them is this shape, with no flag
beyond timeouts, output capture and the `-w` format:

```
curl -sS --connect-timeout 15 --max-time 45 -o <outfile> -D <headerfile> \
  -w 'http_code=%{http_code} content_type=%{content_type} size_download=%{size_download} url_effective=%{url_effective}\n' \
  <url>
```

with `<url>` in turn:

```
https://tokenomist.ai/
https://tokenomist.ai/robots.txt
https://tokenomist.ai/sitemap.xml
https://docs.tokenomist.ai/
https://docs.tokenomist.ai/overview
https://api.tokenomist.ai/v4/token/list
https://cryptorank.io/
https://cryptorank.io/robots.txt
https://docs.cryptorank.io/           (this one ran with -sSL; it returned 200 without redirecting)
https://api.cryptorank.io/v3/documentation-json    (--max-time 60)
https://api.cryptorank.io/v3/ping
https://api.llama.fi/protocols                     (--max-time 90)
https://this-host-does-not-exist-tz22.invalid/
```

Body inspection was done on the saved files and issued no further request:

```
head -c 400 <outfile>
grep -c -i -e "just a moment" -e "cf_chl" -e "challenge-platform" -e "Enable JavaScript and cookies" <outfile>
grep -o -m1 "<title>[^<]*</title>" <outfile>
```

#### 3.3 Challenge check — why the two 200 pages are `open` and not `challenged`

`grep -c` over each rendered page for the markers a Cloudflare managed challenge
carries returned **0** for both hosts:

```
grep -c -i -e "just a moment" -e "cf_chl" -e "challenge-platform" -e "Enable JavaScript and cookies" body-tokenomist-root.bin   -> 0
grep -c -i -e "just a moment" -e "cf_chl" -e "challenge-platform" -e "Enable JavaScript and cookies" body-cryptorank-root.bin   -> 0
```

Each page also carries its own product title, which an interstitial does not:

```
<title>Token Unlocks | Vesting Schedules &amp; Release Data</title>
<title>Cryptocurrency prices, Token rates and Altcoin charts ranked by Market Capitalization and Volume | CryptoRank.io</title>
```

#### 3.4 First 400 bytes of every 2xx body — probe 6

`https://tokenomist.ai/` (792 012 B):

```
<!DOCTYPE html><html lang="en" data-scroll-behavior="smooth" class="inter_a286ccd6-module__kdUgHa__variable dm_mono_49de4911-module__mPbA6a__variable scroll-smooth"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><meta name="viewport" content="width=device-width, initial-scale=1"/><link rel="preload" as="image" imageSrcSet="https://imgproxy.tokenom
```

`https://tokenomist.ai/robots.txt` (1 281 B):

```
User-Agent: *
Allow: /
Disallow: /api/
Disallow: /cdn-cgi/

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
User-Agent: Meta-Externa
```

Its last line, quoted because probe 4 asks whether a sitemap is named:

```
Sitemap: https://tokenomist.ai/sitemap.xml
```

`https://tokenomist.ai/sitemap.xml` (1 019 179 B):

```
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url>
<loc>https://tokenomist.ai/</loc>
<lastmod>2026-08-30T18:08:58.208Z</lastmod>
<changefreq>hourly</changefreq>
<priority>1</priority>
</url>
<url>
<loc>https://tokenomist.ai/overview</loc>
<lastmod>2026-08-30T18:08:58.208Z</lastmod>
<changefreq>hourly</changefreq>
<priority>1</priority>
</url>
```

`https://docs.tokenomist.ai/overview` (281 693 B):

```
<!DOCTYPE html><html lang="en" class="inter_1d81deff-module__CYM0aG__variable papermono_89c757f2-module__6aS5zq__variable dark" data-banner-state="visible" data-assistant-state="closed" data-page-mode="none" data-current-path="/"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/><link rel="preload" href="/mintlify-assets/_next/sta
```

`https://cryptorank.io/` (397 830 B):

```
<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1" class="jsx-2713653309"/><meta name="cryptomus" content="2a743b3d" class="jsx-2713653309"/><link rel="preload" href="/static/fonts/inter/latin.woff2" as="font" type="font/woff2" crossorigin="anonymous" class="jsx-2713653309"/><title>Cryptocurrency prices, Token rates and A
```

`https://cryptorank.io/robots.txt` (1 843 B):

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
Allow: /funds/*/rounds?filterKey
```

Its last two lines, quoted for the same reason:

```
Sitemap: https://cryptorank.io/sitemap.xml
Sitemap: https://cryptorank.io/sitemap-google-news.xml
```

`https://docs.cryptorank.io/` (267 551 B):

```
<!DOCTYPE html><html lang="en" class="inter_1d81deff-module__CYM0aG__variable papermono_89c757f2-module__6aS5zq__variable dark" data-banner-state="visible" data-assistant-state="closed" data-page-mode="none" data-current-path="/"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/><link rel="preload" href="/mintlify-assets/_next/sta
```

`https://api.cryptorank.io/v3/documentation-json` (422 593 B):

```
{"openapi":"3.0.0","paths":{"/v3/ping":{"get":{"description":"**Description**\n\nReturns the current server timestamp.\n\n> **Note:** No API key required.\n\n> **Tip:** Use it to verify the API is reachable and to measure response latency before sending production requests.\n\n**Access**\n- Available from: **Sandbox**\n- Cost: Free","operationId":"SystemController_ping","parameters":[],"responses"
```

`https://api.cryptorank.io/v3/ping` (28 B — the whole body):

```
{"serverTime":1788113433657}
```

The 401 body is not 2xx and is quoted anyway, because it is the evidence for the one
`refused` label in the run — `https://api.tokenomist.ai/v4/token/list` (119 B, whole
body):

```
{"metadata":{"queryDate":"2026-08-30T18:09:39Z"},"status":false,"statusCode":401,"errorMessage":"x-api-key not found"}
```

Read locally out of the saved OpenAPI document, no further request:

```
python3 -c 'import json;d=json.load(open("body-cryptorank-api.json"));print(len(d["paths"]),d["components"]["securitySchemes"],d["servers"])'
-> 76 {'X-Api-Key': {'name': 'X-Api-Key', 'type': 'apiKey', 'in': 'header'}} [{'url': 'https://api.cryptorank.io'}]
```

#### 3.5 Both controls (TZ §3.2) — both read as required

| Control | Command | Reading | Required |
|---|---|---|---|
| DeFiLlama | `curl -sS --connect-timeout 15 --max-time 90 -o … -D … -w '…' https://api.llama.fi/protocols` | `http_code=200 content_type=application/json size_download=8693658` → **`open`** | `open` ✔ |
| `.invalid` | `curl -sS --connect-timeout 15 --max-time 45 -o … -D … -w '…' https://this-host-does-not-exist-tz22.invalid/` | `curl: (6) Could not resolve host: this-host-does-not-exist-tz22.invalid`, `http_code=000 size_download=0`, exit 6 → **`unreachable`** | `unreachable` ✔ |

DeFiLlama body, first 400 bytes:

```
[{"id":"2269","name":"Binance CEX","address":null,"symbol":"BNB","url":"https://www.binance.com","description":"Binance is a cryptocurrency exchange which is the largest exchange in the world in terms of daily trading volume of cryptocurrencies","chain":"Multi-Chain","logo":"https://icons.llamao.fi/icons/protocols/binance-cex","audits":"0","gecko_id":null,"cmcId":null,"category":"CEX","chains":["E
```

The `.invalid` host failed at two independent layers, so the negative control is not
resting on curl alone:

```
dig this-host-does-not-exist-tz22.invalid A +noall +comments   ->  status: NXDOMAIN
getent hosts this-host-does-not-exist-tz22.invalid             ->  no output, exit 2
openssl s_client -connect this-host-does-not-exist-tz22.invalid:443 …
   -> BIO_lookup_ex:system lib:…:Name or service not known
      connect:errno=2                                          (exit 1)
```

This instrument has now returned `unreachable` at least once and is therefore known to
be able to (TZ §3.2).

### 4. Tree cleanliness (TZ §5 criterion 6)

```
git status --porcelain
->  ?? CryptoReports/TZ-22-egress-measurement-report.md
```

Exactly one file. All probe artifacts were written to `/tmp/tz22/` and never entered
the repository.

---

## Test Results

| # | TZ §5 acceptance criterion | Result | Evidence |
|---:|---|---|---|
| 1 | Both target hosts carry a label for every probe that ran | **PASS** | §3.1 — two matrices, no cell empty, none `not run` |
| 2 | DeFiLlama control `open`; `.invalid` control `unreachable` | **PASS** | §3.5 — 200 + 8 693 658 B of JSON; curl exit 6 + NXDOMAIN + `getent` exit 2 |
| 3 | Every 2xx label supported by quoted body bytes | **PASS** | §3.4 — nine 2xx bodies quoted, plus the 401 |
| 4 | No path guessed; probe 5 sourced from the host's own documents | **PASS** | tokenomist: `robots.txt` → sitemap; docs site → `/v4/token/list`. cryptorank: rendered page → docs site → `/v3/documentation-json` → `/v3/ping`. `/api/` at tokenomist was named only as `Disallow` and was **not** fetched |
| 5 | No evasion technique in any command | **PASS** | §3.2 — every command printed in full; default UA, no cookie jar, no proxy, no impersonation, no retry |
| 6 | `git status --porcelain` shows exactly one file | **PASS** | §4 |
| 7 | `## Final Repository State` says nothing about its own push | **PASS** | see that section |

### The recommendation lines — TZ §4 item 6

One line per host, in the TZ's vocabulary and no other:

- **`tokenomist.ai` — `usable as a discovery source`.**
- **`cryptorank.io` — `usable as a discovery source`.**

Nothing about what the data says: this TZ measured a network.

---

## Deviations

1. **§8's `NOT IN EFFECT UNTIL MERGED` is absent, and deliberately.** That sentence
   belongs to a change waiting behind a pull request. TZ §2 authorises no branch and no
   pull request, so the sentence would have no referent and would be the one thing a
   record must not carry — a claim about a state that does not exist. Reported here
   rather than silently dropped.
2. **Probe 5 ran as a small chain per host, not as a single request.** The TZ admits a
   path named by `robots.txt`, by a linked docs or OpenAPI page, or by a `Link` header.
   Neither host names a data endpoint in `robots.txt` or in a `Link` header, so the
   linked docs site had to be fetched to source the endpoint. Those sourcing fetches are
   listed as probes (5b/5c at tokenomist, 5a at cryptorank) rather than omitted, because
   this machine made them.
3. **`https://api.cryptorank.io/v3/ping` was probed in addition to the OpenAPI
   document.** It is named by the host's own OpenAPI as requiring no key, so it is
   sourced rather than guessed, and it separates two facts the doc blob alone leaves
   joined: that the docs host answers, and that the data host answers.
4. **`tokenomist.ai/api/` was not probed.** `robots.txt` names it only under `Disallow`.
   Fetching it would have been routing around a refusal the host stated in advance,
   which `ANALYST-INSTRUCTIONS.md` §6 and TZ §3.1 both forbid. Recorded as a decision,
   not as a gap.
5. **The `Link` headers on `tokenomist.ai/` name no endpoint.** They carry three
   `rel=preconnect` hints (`enterprise.tokenomist.ai`, `space.tokenomist.ai`,
   `space.unlocks.app`), which are transport hints and not documented endpoints. None
   was fetched.

---

## Pre-existing Issues

1. **The map's §11 now carries a sentence this run has overtaken.** It reads:

   > **`tokenomist.ai` and `cryptorank.io` are NOT measured and may not be assumed open
   > or closed in either direction (TZ-22).**

   Both are now measured, from the machine §11 describes. The map is the Architect's
   file and is not edited from here; this is the finding that lets it be updated.
2. **No fingerprint drift.** Every file in the map's `## 0` table matches the stated
   line count and MD5 (§Validation 1), so nothing is ahead in either direction.
3. **`ANALYST-INSTRUCTIONS.md` §6a admits an aggregator for discovery on two sweeps and
   names no host for either.** The Vesting sweep says «discovery may come from a vesting
   aggregator» and the Backing sweep speaks of round terms from aggregators, but neither
   names which. This run measured the two the Architect asked about; the methodology
   still contains no list a future run could check itself against. A finding, not a
   change — §6a is binding text this role does not write.

---

## Remaining Risks

1. **A reading is a point in time, and inv. 52 is the reason to say so.** Both hosts sit
   behind Cloudflare, whose posture varies by client, by IP reputation and by ASN. This
   run measured one VPS at one moment with one client. A future session that reads
   `challenged` where this one read `open` has not contradicted this report; it has
   measured a different moment, and that reading replaces this one rather than arguing
   with it.
2. **Both data APIs are credentialed and this repository holds no key.** Tokenomist
   requires `x-api-key` and refused without it; CryptoRank declares `X-Api-Key` as its
   only security scheme, with `/v3/ping` and the OpenAPI document as the keyless
   exceptions. Any future use beyond reading rendered pages needs a credential
   decision that is the Boss's, and a key would live only in Actions environment
   variables (hard floor item 6).
3. **Nothing here authorises putting either host inside CI.** Hard floor item 9's
   closing clause is explicit: the thing the rule protects against is shipping code
   that depends on an egress one environment happens to have. This report measures the
   VPS; it says nothing about a GitHub runner, where the answer has historically been
   different for other hosts (inv. 24).
4. **The rendered pages are JS-hydrated applications.** They classify `open` because the
   host served the document it advertises, which is what §3.3 asks. Whether a given
   figure can be *extracted* from that HTML without executing JavaScript is a different
   question, outside this TZ's scope, and is not answered here.

---

## Commit

One commit, one file, direct to `main` per TZ §7 and contract §8 (`CryptoReports/**` is
one of the two paths that bypass the branch):

```
docs(egress): measure tokenomist.ai and cryptorank.io from the VPS (TZ-22)
```

Contents: `CryptoReports/TZ-22-egress-measurement-report.md`, created. Nothing else.

---

## Pull Request

**None, and none is possible under this TZ.** TZ §2 authorises no branch and no pull
request; the report goes straight to `main` on the `CryptoReports/**` path that
contract §8 opens for exactly this case. There is no compare URL to give and nothing
awaits the Boss's merge.

---

## CI Execution

**No workflow result is claimed, in either direction.** This session has no `gh` binary
and no GitHub token (`command -v gh` → absent; no `GH_TOKEN`/`GITHUB_TOKEN` in the
environment), so it cannot read a runner. What is established is the filter state, read
from the repository:

| Workflow | Relevant filter | Bearing on a `CryptoReports/**` commit |
|---|---|---|
| `main.yml` | `push: branches: [main]`, `paths-ignore:` includes `'**.md'` and `'analyst/**'` | a Markdown-only commit is covered by `'**.md'` |
| `bench.yml` | `push: branches: [main, 'claude/**']`, `paths-ignore:` includes `'**.md'` | same |
| `journal.yml`, `calib.yml`, `backtest_bench.yml` | scheduled / `workflow_dispatch` / `claude/**` | not triggered by a push of Markdown to `main` |

Per inv. 52 a pattern is not a measurement, and the runner history that would settle it
is not readable from here. What the repository does record is that every report now under
`CryptoReports/**` reached `main` on this same path — `93dd62c` (TZ-20) and `d76a6f3`
(TZ-21) are the two most recent — and the map's §0 attributes the gate runs of that
period to the implementation and merge commits, not to the report commits.

No workflow was run locally either: this TZ changes no production file, so the standing
checks of contract §9 (`py_compile main.py`, `node --check` on the `index.html` script
block) have nothing to check and were not run — there is no change for them to cover.

---

## Final Repository State

The session worked from a detached checkout of `origin/main` at `41386ad`, which is the
tip this report's fingerprints were taken against. No branch was created, no branch was
pushed, no pull request exists, and nothing under `analyst/`, `bench/`, `journal/`,
`.github/` or any production file was touched — `index.html`, `main.py`,
`catalysts.json` and `bench/exhaustion-calibration.txt` all still carry the MD5s the map
states at revision `2026-08-30-c`.

The working tree carries exactly one new file, `CryptoReports/TZ-22-egress-measurement-report.md`,
and nothing else: `git status --porcelain` printed one line.

Nothing about this report's own commit or push is stated here (inv. 54, contract §10):
those steps had not run when this text was written, and a forecast inside an immutable
record is indistinguishable from a measurement to whoever reads it next. If that outcome
matters, the next record states it, where it is history.

Nothing in this run changes what GitHub Pages serves.

---

## Fingerprints

Taken on the detached checkout of `origin/main` at `41386ad`, before the report was
committed.

**Map revision string:** `**Revision 2026-08-30-c.**`

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1619 | `b8ca5f8e4855d1b1bb2d6ebdcfb66e64` |
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `EXECUTOR-INSTRUCTIONS.md` | 657 | `d1374bb975759704d4a3089e60002d71` |
| `ANALYST-INSTRUCTIONS.md` | 771 | `63c15842a0d0524e4acf812966bd338d` |
| `CryptoTZ/TZ-22-egress-measurement.md` | 157 | `1a22288269a8a6cf62833aa30c7566b6` |

The last three are not in the map's `## 0` table. They are recorded because this TZ's
gate rests on the contract's version and on the methodology's §6a, and a report that
depends on a text should pin the copy it read.
