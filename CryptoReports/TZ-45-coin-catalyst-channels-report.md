# Implementation Report — TZ-45

## Status

**COMPLETED.** Report-only TZ. Every member of `tokens[]` — **30 extracted by command, 30
rows** — was probed class by class under §4. **27 `primary-dated` · 3 `primary-undated`
(ONDO, HYPE, LIT) · 0 `refused` · 0 `unreachable` · 0 `none-found`.** No event, date, price
or supply figure was read into this record. The previous TZ, TZ-44, was merged before this
run started: pull request #39, merge `baec7c9`, implementation commit `99e4b0a`.

---

## Inbound Filing

`CryptoTZ/TZ-45-coin-catalyst-channels.md` arrived under its canonical name in the Boss's
upload commit `57ea70e`, the only commit touching that path (`git log --all -- <path>`).
Nothing was moved or renamed, and no second copy exists.

---

## Scope Executed

**Class: report-only TZ** (contract §8). TZ §2 authorises one written file, this report, on
the `CryptoReports/**` direct-push path.

Run order under contract §4a:

1. `git fetch --all --prune` moved `origin/main` `d469720..57ea70e`;
   `git rev-parse --is-shallow-repository` → `false`.
2. The harness worktree branch had no upstream, so it was brought to `origin/main` with
   `git merge --ff-only origin/main` → `57ea70e`; `git status --porcelain` was empty and
   `git diff --quiet HEAD origin/main` held.
3. Fingerprint gate (contract §5): the revision string plus the seven content anchors of the
   map's `## 0` block, each matched as an exact substring (`grep -qF`) → **7/7 present**.
   Revision `**Revision 2026-09-14-a.**` equals the revision TZ-45 §0 requires. All four
   file-table rows and all three bench anchors match (`## Fingerprints`).
4. Repository state: TZ-44's branch `origin/claude/tz-44-verify-comparability-i9-union` is
   merged (`baec7c9`). TZ-45 has no sequencing clause.
5. §3 extraction → §4 probes → §5 table → §6 validation.

Out of scope and not done: no event record was read (only record counts and date-field
**names** were printed); nothing was written to `analyst/**`, to any data file or to
`ANALYST-INSTRUCTIONS.md`; no evasion flag was used; `tokenomist.ai` and `cryptorank.io`
were not probed.

---

## Files Created

- `CryptoReports/TZ-45-coin-catalyst-channels-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Universe — read from production (§3, map inv. 21)

The list is cut from `index.html` by evaluating the `tokens` array literal exactly as it
stands between `var tokens = [` and the first `];` after it. No symbol was typed.
Every later step iterates over this output and nothing else.

```
$ node /tmp/tz45-extract.js        # cwd: repository root
SUI	SUIUSDT
ONDO	ONDOUSDT
LINK	LINKUSDT
RENDER	RENDERUSDT
NEAR	NEARUSDT
YFI	YFIUSDT
AAVE	AAVEUSDT
AVAX	AVAXUSDT
FET	FETUSDT
ENA	ENAUSDT
TAO	TAOUSDT
GRAM	GRAMUSDT
XRP	XRPUSDT
ADA	ADAUSDT
TRX	TRXUSDT
SOL	SOLUSDT
BCH	BCHUSDT
HYPE	HYPEUSDT	fut
SKY	SKYUSDT
ETH	ETHUSDT
HBAR	HBARUSDT
XLM	XLMUSDT
ALGO	ALGOUSDT
BNB	BNBUSDT
ZEC	ZECUSDT
UNI	UNIUSDT
XMR	XMRUSDT	fut
LIT	LITUSDT	fut
MORPHO	MORPHOUSDT	fut
ARB	ARBUSDT	fut
COUNT 30
```

`/tmp/tz45-extract.js`, verbatim:

```js
var src=require('fs').readFileSync('index.html','utf8');
var i=src.indexOf('var tokens = ['); var j=src.indexOf('];',i);
var tokens=eval(src.slice(i+'var tokens = '.length,j+1));
tokens.forEach(function(t){console.log(t.name+'\t'+t.s+(t.fut?'\tfut':''));});
console.log('COUNT '+tokens.length);
```

### Instrument

Every candidate was fetched **once** by `probe.py`, which runs one `curl` per row and nothing
else: no user-agent override, no proxy, no cookie, no retry. The literal command string it
executes is the string recorded in the `Command` column. The body goes to
`/tmp/tz45/body/<id>`, which is outside the repository. The classifier prints only the path
and length of the record list it chose and the **names** of its date-shaped keys or tags,
never a value.

**How a verdict is assigned:**

- curl produced no HTTP status (`000`) and exited non-zero (DNS, connection refused,
  timeout) → `unreachable`;
- HTTP `403` or `429`, or a managed-challenge marker in the headers or body → `refused`;
- HTTP `2xx` and the response carries a list of records whose fields hold dates →
  `primary-dated`;
- any other response → `primary-undated`, including a `404` (see Remaining Risks 5).

The HTTP column also records a redirect: `a → b` means the request went to `a` and
`curl -L` landed on `b`, and `b` answered.

`/tmp/tz45/probe.py`, verbatim, in the version that produced every verdict below. Its
`--reanalyse` mode re-classifies from the saved bodies and makes no request (Deviations 2):

```python
#!/usr/bin/env python3
# TZ-45 one-shot channel probe. One curl per candidate, no retry, no UA/proxy/cookie
# flags. Prints SCHEMA only (record count, names of date-shaped keys/tags) and never
# a value from the body.
#   probe.py candidates.tsv            -> fetch once per row, classify, print row
#   probe.py --reanalyse results.tsv   -> re-classify from the SAVED bodies, no fetch
import sys, subprocess, json, re, os
from urllib.parse import urlparse

ISO = re.compile(r'^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}.*)?$')
DKEY = re.compile(r'(date|time|_at$|At$|^published|^updated|^created)', re.I)

def is_datey(k, v):
    if isinstance(v, str) and ISO.match(v):
        return True
    if isinstance(v, (int, float)) and not isinstance(v, bool) and DKEY.search(k):
        return 1e9 <= v <= 2e9 or 1e12 <= v <= 2e12
    return False

def lists_of_dicts(o, depth=0, path='$'):
    """Every list of dicts within depth 3, as (path, list)."""
    out = []
    if isinstance(o, list) and o and all(isinstance(x, dict) for x in o):
        out.append((path, o))
    elif depth < 3:
        items = o.items() if isinstance(o, dict) else (enumerate(o) if isinstance(o, list) else [])
        for k, v in items:
            out += lists_of_dicts(v, depth + 1, '%s.%s' % (path, k))
    return out

def date_keys(recs):
    return sorted({k for r in recs for k, v in r.items() if is_datey(k, v)})

def analyse(body, hdr):
    low = body[:20000].decode('utf-8', 'replace').lower()
    challenge = ('cf-mitigated: challenge' in hdr.lower() or 'challenge-platform' in low
                 or '<title>just a moment' in low or 'attention required! | cloudflare' in low)
    try:
        doc = json.loads(body)
        cands = lists_of_dicts(doc)
        # Prefer the record list that carries dates; among equals, the longest.
        cands.sort(key=lambda pl: (bool(date_keys(pl[1])), len(pl[1])), reverse=True)
        if not cands:
            return challenge, 'json', 'no-record-list', [], False
        path, recs = cands[0]
        keys = date_keys(recs)
        return challenge, 'json', '%s[%d]' % (path, len(recs)), keys, bool(keys)
    except Exception:
        pass
    txt = body.decode('utf-8', 'replace')
    items = len(re.findall(r'<(item|entry)[\s>]', txt))
    if items and re.search(r'<(rss|feed)[\s>]', txt[:4000]):
        tags = sorted({t for t in ('pubDate', 'published', 'updated', 'dc:date') if '<%s>' % t in txt or '<%s ' % t in txt})
        return challenge, 'xml', 'items[%d]' % items, tags, bool(tags)
    kind = 'html' if '<html' in low else ('empty' if not body else 'other')
    return challenge, kind, 'n/a', [], False

def classify(pid, code, rc):
    bp, hp = '/tmp/tz45/body/' + pid, '/tmp/tz45/hdr/' + pid
    body = open(bp, 'rb').read() if os.path.exists(bp) else b''
    hdr = open(hp, 'r', errors='replace').read() if os.path.exists(hp) else ''
    note = 'curl exit %d' % rc
    if rc != 0 and code in ('000', ''):
        return 'unreachable', '-', '-', [], note
    ch, kind, recs, keys, dated = analyse(body, hdr)
    if ch or code in ('403', '429'):
        return 'refused', kind, recs, keys, note + (' challenge' if ch else '')
    if code.startswith('2') and dated:
        return 'primary-dated', kind, recs, keys, note
    return 'primary-undated', kind, recs, keys, note

def row(pid, sym, cls, host, effhost, cmd, code, ctype, rc):
    verdict, kind, recs, keys, note = classify(pid, code, rc)
    return '\t'.join([pid, sym, cls, host, effhost, cmd, code, ctype,
                      kind, recs, ','.join(keys) or '-', verdict, note])

def main():
    for line in open(sys.argv[1]):
        if not line.strip() or line.startswith('#'):
            continue
        pid, sym, cls, url = line.rstrip('\n').split('\t')
        cmd = ("curl -sS -L -m 20 -o /tmp/tz45/body/%s -D /tmp/tz45/hdr/%s "
               "-w '%%{http_code} %%{url_effective} %%{content_type}' '%s'") % (pid, pid, url)
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        w = (r.stdout.strip() + '  ').split(' ', 2)
        code, eff, ctype = w[0], w[1], w[2].strip()
        effhost = urlparse(eff).netloc if eff and eff != '-' else '-'
        print(row(pid, sym, cls, urlparse(url).netloc, effhost, cmd, code, ctype, r.returncode), flush=True)

def reanalyse():
    for line in open(sys.argv[2]):
        f = line.rstrip('\n').split('\t')
        rc = int(f[12].split()[2])
        print(row(f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], rc), flush=True)

if __name__ == '__main__':
    reanalyse() if sys.argv[1] == '--reanalyse' else main()
```

Class 4 is a list that spans the whole exchange. The command used returns it unfiltered,
so the §4 filter "to the coin's own symbol" is applied to the saved response by a
count-only script. It prints no title and no date:

```python
# Count dated announcement records whose title names the symbol as a whole word.
# Prints counts only -- never a title, never a date.
import json, re, sys
d = json.load(open('/tmp/tz45/body/BINANCE-c4a'))
recs = []
def walk(o):
    if isinstance(o, dict):
        if 'title' in o and 'releaseDate' in o: recs.append(o)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(d)
print('dated records (title+releaseDate):', len(recs))
for s in sys.argv[1:]:
    print(s, 'matching:', sum(1 for r in recs if re.search(r'\b%s\b' % s, r['title'])))
```

### Measurement table (§5)

**How to read `Class tried`:** it lists the classes considered for the coin, in §4 order.
`(none)` means no candidate channel exists for that class, so no request was made. The
**bold** class is the attempt this row's Host, Command, HTTP and Verdict belong to.
**Which attempt a row carries:** the first attempt that returned `primary-dated`. If there
was none, the earliest attempt answered `2xx`. Every other attempt is listed under
*Attempts not carried in a row* below, so none is dropped.

| Symbol | Class tried | Host | Command | HTTP | Verdict |
|---|---|---|---|---|---|
| SUI | **1** | forums.sui.io | `curl -sS -L -m 20 -o /tmp/tz45/body/SUI-c1a -D /tmp/tz45/hdr/SUI-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forums.sui.io/latest.json'` | 200 | primary-dated |
| ONDO | 1 · 2 · **3** · 4 | eth.blockscout.com | `curl -sS -L -m 20 -o /tmp/tz45/body/ONDO-c3a -D /tmp/tz45/hdr/ONDO-c3a -w '%{http_code} %{url_effective} %{content_type}' 'https://eth.blockscout.com/api/v2/tokens/0xfAbA6f8e4a5E8Ab82F62fe7C39859FA577269BE3'` | 200 | primary-undated |
| LINK | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/LINK-c2a -D /tmp/tz45/hdr/LINK-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/smartcontractkit/chainlink/releases?per_page=5'` | 200 | primary-dated |
| RENDER | 1 (none) · **2** | rendernetwork.medium.com | `curl -sS -L -m 20 -o /tmp/tz45/body/RENDER-c2a -D /tmp/tz45/hdr/RENDER-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://rendernetwork.medium.com/feed'` | 200 | primary-dated |
| NEAR | **1** | gov.near.org | `curl -sS -L -m 20 -o /tmp/tz45/body/NEAR-c1a -D /tmp/tz45/hdr/NEAR-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://gov.near.org/latest.json'` | 200 | primary-dated |
| YFI | **1** | gov.yearn.fi | `curl -sS -L -m 20 -o /tmp/tz45/body/YFI-c1a -D /tmp/tz45/hdr/YFI-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://gov.yearn.fi/latest.json'` | 200 | primary-dated |
| AAVE | **1** | governance.aave.com | `curl -sS -L -m 20 -o /tmp/tz45/body/AAVE-c1a -D /tmp/tz45/hdr/AAVE-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://governance.aave.com/latest.json'` | 200 | primary-dated |
| AVAX | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/AVAX-c2a -D /tmp/tz45/hdr/AVAX-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/ava-labs/avalanchego/releases?per_page=5'` | 200 | primary-dated |
| FET | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/FET-c2a -D /tmp/tz45/hdr/FET-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/fetchai/fetchd/releases?per_page=5'` | 200 | primary-dated |
| ENA | **1** | gov.ethenafoundation.com | `curl -sS -L -m 20 -o /tmp/tz45/body/ENA-c1a -D /tmp/tz45/hdr/ENA-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://gov.ethenafoundation.com/latest.json'` | 200 | primary-dated |
| TAO | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/TAO-c2a -D /tmp/tz45/hdr/TAO-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/opentensor/subtensor/releases?per_page=5'` | 200 | primary-dated |
| GRAM | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/GRAM-c2a -D /tmp/tz45/hdr/GRAM-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/ton-blockchain/ton/releases?per_page=5'` | 200 | primary-dated |
| XRP | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/XRP-c2a -D /tmp/tz45/hdr/XRP-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/XRPLF/rippled/releases?per_page=5'` | 200 | primary-dated |
| ADA | **1** | forum.cardano.org | `curl -sS -L -m 20 -o /tmp/tz45/body/ADA-c1a -D /tmp/tz45/hdr/ADA-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.cardano.org/latest.json'` | 200 | primary-dated |
| TRX | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/TRX-c2a -D /tmp/tz45/hdr/TRX-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/tronprotocol/java-tron/releases?per_page=5'` | 200 | primary-dated |
| SOL | **1** | forum.solana.com | `curl -sS -L -m 20 -o /tmp/tz45/body/SOL-c1a -D /tmp/tz45/hdr/SOL-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.solana.com/latest.json'` | 200 | primary-dated |
| BCH | 1 (none) · **2** | gitlab.com | `curl -sS -L -m 20 -o /tmp/tz45/body/BCH-c2a -D /tmp/tz45/hdr/BCH-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://gitlab.com/api/v4/projects/bitcoin-cash-node%2Fbitcoin-cash-node/releases?per_page=5'` | 200 | primary-dated |
| HYPE | 1 (none) · **2** · 3 (none) · 4 | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/HYPE-c2a -D /tmp/tz45/hdr/HYPE-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/hyperliquid-dex/node/releases?per_page=5'` | 200 | primary-undated |
| SKY | **1** | forum.sky.money → forum.skyeco.com | `curl -sS -L -m 20 -o /tmp/tz45/body/SKY-c1a -D /tmp/tz45/hdr/SKY-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.sky.money/latest.json'` | 200 | primary-dated |
| ETH | **1** | ethereum-magicians.org | `curl -sS -L -m 20 -o /tmp/tz45/body/ETH-c1a -D /tmp/tz45/hdr/ETH-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://ethereum-magicians.org/latest.json'` | 200 | primary-dated |
| HBAR | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/HBAR-c2a -D /tmp/tz45/hdr/HBAR-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/hiero-ledger/hiero-consensus-node/releases?per_page=5'` | 200 | primary-dated |
| XLM | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/XLM-c2a -D /tmp/tz45/hdr/XLM-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/stellar/stellar-core/releases?per_page=5'` | 200 | primary-dated |
| ALGO | **1** | forum.algorand.org → forum.algorand.co | `curl -sS -L -m 20 -o /tmp/tz45/body/ALGO-c1a -D /tmp/tz45/hdr/ALGO-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.algorand.org/latest.json'` | 200 | primary-dated |
| BNB | **1** | forum.bnbchain.org | `curl -sS -L -m 20 -o /tmp/tz45/body/BNB-c1a -D /tmp/tz45/hdr/BNB-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.bnbchain.org/latest.json'` | 200 | primary-dated |
| ZEC | **1** | forum.zcashcommunity.com | `curl -sS -L -m 20 -o /tmp/tz45/body/ZEC-c1a -D /tmp/tz45/hdr/ZEC-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.zcashcommunity.com/latest.json'` | 200 | primary-dated |
| UNI | **1** | gov.uniswap.org | `curl -sS -L -m 20 -o /tmp/tz45/body/UNI-c1a -D /tmp/tz45/hdr/UNI-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://gov.uniswap.org/latest.json'` | 200 | primary-dated |
| XMR | 1 (none) · **2** | api.github.com | `curl -sS -L -m 20 -o /tmp/tz45/body/XMR-c2a -D /tmp/tz45/hdr/XMR-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/monero-project/monero/releases?per_page=5'` | 200 | primary-dated |
| LIT | 1 (none) · 2 (none) · 3 (none) · **4** | www.binance.com | `curl -sS -L -m 20 -o /tmp/tz45/body/BINANCE-c4a -D /tmp/tz45/hdr/BINANCE-c4a -w '%{http_code} %{url_effective} %{content_type}' 'https://www.binance.com/bapi/composite/v1/public/cms/article/list/query?type=1&pageNo=1&pageSize=50'` then `python3 binfilter.py HYPE LIT` (cwd `/tmp/tz45`) | 200; LIT-filtered dated records: 0 | primary-undated |
| MORPHO | **1** | forum.morpho.org | `curl -sS -L -m 20 -o /tmp/tz45/body/MORPHO-c1a -D /tmp/tz45/hdr/MORPHO-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.morpho.org/latest.json'` | 200 | primary-dated |
| ARB | **1** | forum.arbitrum.foundation | `curl -sS -L -m 20 -o /tmp/tz45/body/ARB-c1a -D /tmp/tz45/hdr/ARB-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.arbitrum.foundation/latest.json'` | 200 | primary-dated |

### The date field of each `primary-dated` row (schema, never a value)

- SUI (`forums.sui.io`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- LINK (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- RENDER (`rendernetwork.medium.com`) — `rss > channel > item > pubDate` — RFC-822 string, present on every item
- NEAR (`gov.near.org`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- YFI (`gov.yearn.fi`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- AAVE (`governance.aave.com`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- AVAX (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- FET (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- ENA (`gov.ethenafoundation.com`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- TAO (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- GRAM (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- XRP (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- ADA (`forum.cardano.org`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- TRX (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- SOL (`forum.solana.com`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- BCH (`gitlab.com`) — `[].released_at` — ISO-8601 string; `created_at` beside it
- SKY (`forum.skyeco.com`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- ETH (`ethereum-magicians.org`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- HBAR (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- XLM (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- ALGO (`forum.algorand.co`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- BNB (`forum.bnbchain.org`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- ZEC (`forum.zcashcommunity.com`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- UNI (`gov.uniswap.org`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- XMR (`api.github.com`) — `[].published_at` — ISO-8601 string; `created_at` and `updated_at` beside it
- MORPHO (`forum.morpho.org`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it
- ARB (`forum.arbitrum.foundation`) — `topic_list.topics[].created_at` — ISO-8601 string; `bumped_at` and `last_posted_at` beside it

These fields date the **record**: a topic's creation, a release's publication, a post's
publication. They do not date the event a record may announce. Reading that date would
mean reading content, which §2 forbids (Remaining Risks 1).

### Attempts not carried in a row

| Symbol | Class | Host | Command | HTTP | Verdict |
|---|---|---|---|---|---|
| ONDO | 1 | forum.ondo.foundation | `curl -sS -L -m 20 -o /tmp/tz45/body/ONDO-c1a -D /tmp/tz45/hdr/ONDO-c1a -w '%{http_code} %{url_effective} %{content_type}' 'https://forum.ondo.foundation/latest.json'` | 000 (curl exit 6) | unreachable |
| ONDO | 2 | blog.ondo.finance → ondo.finance | `curl -sS -L -m 20 -o /tmp/tz45/body/ONDO-c2a -D /tmp/tz45/hdr/ONDO-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://blog.ondo.finance/rss/'` | 404; `text/html; charset=utf-8` | primary-undated |
| ONDO | 4 | www.binance.com | no new request — the saved `BINANCE-c4a` response (row LIT), then `python3 binfilter.py ONDO HYPE LIT` (cwd `/tmp/tz45`) | 200; ONDO-filtered dated records: 0 | primary-undated |
| HYPE | 4 | www.binance.com | the `BINANCE-c4a` request of row LIT, then `python3 binfilter.py HYPE LIT` (cwd `/tmp/tz45`) | 200; HYPE-filtered dated records: 0 | primary-undated |

Per §4, the stop rule means no further class was attempted for any coin once a class
returned `primary-dated`.

### Classes with no candidate (no request made)

- **Class 1, governance forum:** 14 coins have none — LINK, RENDER, AVAX, FET, TAO, GRAM,
  XRP, TRX, BCH, HYPE, HBAR, XLM, XMR and LIT. Each of these protocols runs its proposal
  process elsewhere (a GitHub proposals repository, a chat server, or nothing public),
  and no Discourse instance of its own is known to the Executor (Remaining Risks 2). Probing an invented forum host is exactly
  what map inv. 44 names, so none was probed.
- **Class 2, release channel:** LIT. No canonical protocol repository with releases, and
  no protocol blog feed, is established for Lighter. Its public repositories are client
  SDKs, whose releases are not protocol upgrades.
- **Class 3, token contract state:** HYPE is the native asset of its own L1 and has no
  token contract to read. For LIT, no contract address is established in this repository
  or in any source this session read, and searching an explorer for one would be
  discovery, not a channel probe.

### Requests outside the candidate list (environment measurements)

Three requests were made before the candidate list existed. None fed a verdict:

| Command | HTTP | Purpose |
|---|---|---|
| `curl -sS -o /dev/null -m 15 -w '%{http_code}\n' "$u"` with `u=https://api.github.com/zen` | 200 | egress check |
| the same command with `u=https://gov.uniswap.org/latest.json` | 200 | egress check; the body was discarded (Deviations 1) |
| `curl -sS -m 15 https://api.github.com/rate_limit` | 200 | unauthenticated core quota before the probes: limit 60, remaining 59 |

Tool: `curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13`. **Measurement
window:** 2026-09-15T22:35:34Z to 22:39:01Z UTC, from the mtimes of the first and last
body files (`SUI-c1a`, `ONDO-c3a`).

### Tallies

| | Count |
|---|---:|
| `tokens[]` members extracted (§3 command, `COUNT` line) | **30** |
| Rows in the measurement table | **30** |
| `primary-dated` | **27** — 15 via class 1 (Discourse), 12 via class 2 (10 GitHub releases, 1 GitLab releases, 1 Medium feed) |
| `primary-undated` | **3** — ONDO (class 3), HYPE (class 2), LIT (class 4) |
| `refused` | **0** |
| `unreachable` | **0** |
| `none-found` | **0** |

Attempts, counted per coin and class: **34**, made with **32** HTTP requests, because one
Binance request served the class-4 attempts of ONDO, HYPE and LIT. By verdict: 27
`primary-dated`, 6 `primary-undated` (ONDO c2 `404`, ONDO c3, ONDO c4, HYPE c2, HYPE c4,
LIT c4), 1 `unreachable` (ONDO c1, DNS), 0 `refused`. With the three environment requests
above, this session sent **35** HTTP requests in total.

---

## Validation

Result: **V1 N/A · V2 PASS · V3 PASS · V4 PASS · V5 PASS · V6 PASS · V7 PASS · V8 PASS**.

**V1 — `py_compile` / `node --check`: not applicable.** No code moves in this TZ (TZ §6.1); the verdict is N/A by the TZ's own item, stated rather than omitted.

**V2 — row count equals the §3 extraction count.**

```
$ node /tmp/tz45-extract.js | tail -1
COUNT 30
$ python3 /tmp/tz45/validate.py   # measurement-table rows
measurement-table rows: 30
```

Extracted **30** == table **30** → **PASS**.

**V3 — every row carries all six columns.**

```
rows checked: 30
rows with 6 non-empty cells: 30
rows failing: none
empty Command cells: none
```

→ **PASS**.

**V4 — every Verdict is one of the five admissible words.**

```
rows checked: 30
inadmissible: none
primary-dated    27
primary-undated  3
refused          0
unreachable      0
none-found       0
```

→ **PASS**.

**V5 — no row carries a product fact.** Pattern scan over every row of the measurement table, every row of the attempts table and every date-field line, then read by eye.

```
ISO date           \b(19|20)\d{2}-\d{2}-\d{2}\b
dd.mm.yyyy date    \b\d{1,2}\.\d{1,2}\.(19|20)\d{2}\b
month name         \b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d
currency amount    [$€£]\s?\d|\d\s?(USD|USDT|BTC|ETH)\b
numeric percent    \d+(\.\d+)?\s?%
epoch-like number  \b\d{10,13}\b
large figure       \b\d{1,3}([ ,]\d{3}){2,}\b
hits: none
```

Read: every cell is a symbol, a class number, a host, a command, an HTTP status or a verdict; the date-field lines name fields and types only. No date, event name, price or supply figure → **PASS**.

**V6 — no command contains an evasion technique, and each candidate was fetched once.**

```
flag pattern: (^|\s)(-A|--user-agent|-H|--header|-x|--proxy|--socks\w*|--preproxy|--retry[\w-]*|-b|--cookie|-c|--cookie-jar)(\s|=|$)|user-agent
commands scanned: 66 (probe result rows 32 + table Command cells 34) + probe.py curl template lines 2
hits: none
probe result rows: 32, distinct ids: 32, distinct URLs: 32
body files present: 31; ids without a body: ['ONDO-c1a']
```

No user-agent, header, proxy, cookie or retry flag in any command. Every id and every URL occurs once (one attempt per candidate; the only repeat in the session is the UNI egress check, Deviations 1). An id without a body is a request that received no response: curl writes no output file on a DNS failure → **PASS**.

**V7 — `git status --porcelain` is empty apart from the report.**

```
$ git status --porcelain
?? CryptoReports/TZ-45-coin-catalyst-channels-report.md
```

No file under `analyst/**`, no production file, no bench, no workflow → **PASS**.

**V8 — no-regression: no file of the §0 table is in the diff.**

```
$ git status --porcelain | cut -c4- | grep -x -F -e index.html -e main.py -e catalysts.json -e bench/exhaustion-calibration.txt -e bench/backtest_bench.py -e bench/verify_bench.py -e bench/backtest_guard_bench.py | wc -l
0
$ git diff --name-only HEAD
(empty)
```

Zero §0 files changed and no tracked file changed at all, so every bench figure and gate count TZ-45 §0 pins is unchanged by construction → **PASS**.

<details><summary><code>/tmp/tz45/validate.py</code>, verbatim</summary>

```python
#!/usr/bin/env python3
# TZ-45 §6 validation: runs V1-V8 against the report and the probe records, and splices
# the evidence (commands + outputs) into the report's @@VALIDATION@@ placeholder.
import subprocess, re, collections, glob, os
REPO = '/root/crypto-auto/.claude/worktrees/bridge-cse_013D2XfmWy3jozb4g6z8mpTe'
REPORT = REPO + '/CryptoReports/TZ-45-coin-catalyst-channels-report.md'
T = '/tmp/tz45/'
VER = ['primary-dated', 'primary-undated', 'refused', 'unreachable', 'none-found']

def sh(cmd):
    r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True)
    return (r.stdout + r.stderr).rstrip('\n')

t = open(REPORT).read()
def section(title):
    return t.split(title, 1)[1].split('\n### ', 1)[0]
def table(sec):
    rs = [[c.strip() for c in l.strip()[1:-1].split('|')]
          for l in sec.splitlines() if l.startswith('|') and not l.startswith('|---')]
    return rs[1:]

main = table(section('### Measurement table (§5)'))
att = table(section('### Attempts not carried in a row'))
datesec = section('### The date field of each `primary-dated` row')
out = []

# V1
out.append('**V1 — `py_compile` / `node --check`: not applicable.** No code moves in this TZ '
           '(TZ §6.1); the verdict is N/A by the TZ\'s own item, stated rather than omitted.')

# V2
cnt = sh('node /tmp/tz45-extract.js | tail -1')
n = int(cnt.split()[1])
v2 = 'PASS' if n == len(main) else 'FAIL'
out.append('**V2 — row count equals the §3 extraction count.**\n\n```\n$ node /tmp/tz45-extract.js | tail -1\n%s\n'
           '$ python3 /tmp/tz45/validate.py   # measurement-table rows\nmeasurement-table rows: %d\n```\n\n'
           'Extracted **%d** == table **%d** → **%s**.' % (cnt, len(main), n, len(main), v2))

# V3
bad = [r[0] for r in main if len(r) != 6 or not all(r)]
emptycmd = [r[0] for r in main if len(r) < 4 or not r[3]]
v3 = 'PASS' if not bad and not emptycmd and main else 'FAIL'
out.append('**V3 — every row carries all six columns.**\n\n```\nrows checked: %d\nrows with 6 non-empty cells: %d\n'
           'rows failing: %s\nempty Command cells: %s\n```\n\n→ **%s**.'
           % (len(main), len(main) - len(bad), bad or 'none', emptycmd or 'none', v3))

# V4
dist = collections.Counter(r[5] for r in main)
inad = [r[0] + ':' + r[5] for r in main if r[5] not in VER]
v4 = 'PASS' if not inad and main else 'FAIL'
out.append('**V4 — every Verdict is one of the five admissible words.**\n\n```\nrows checked: %d\ninadmissible: %s\n%s\n```\n\n→ **%s**.'
           % (len(main), inad or 'none', '\n'.join('%-16s %d' % (v, dist.get(v, 0)) for v in VER), v4))

# V5
scan = '\n'.join(' | '.join(r) for r in main + att) + '\n' + datesec
pats = collections.OrderedDict([
    ('ISO date', r'\b(19|20)\d{2}-\d{2}-\d{2}\b'),
    ('dd.mm.yyyy date', r'\b\d{1,2}\.\d{1,2}\.(19|20)\d{2}\b'),
    ('month name', r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d'),
    ('currency amount', r'[$€£]\s?\d|\d\s?(USD|USDT|BTC|ETH)\b'),
    ('numeric percent', r'\d+(\.\d+)?\s?%'),
    ('epoch-like number', r'\b\d{10,13}\b'),
    ('large figure', r'\b\d{1,3}([ ,]\d{3}){2,}\b'),
])
hits = [(k, m.group(0)) for k, p in pats.items() for m in re.finditer(p, scan)]
v5 = 'PASS' if not hits else 'FAIL'
out.append('**V5 — no row carries a product fact.** Pattern scan over every row of the measurement table, '
           'every row of the attempts table and every date-field line, then read by eye.\n\n```\n%s\nhits: %s\n```\n\n'
           'Read: every cell is a symbol, a class number, a host, a command, an HTTP status or a verdict; the '
           'date-field lines name fields and types only. No date, event name, price or supply figure → **%s**.'
           % ('\n'.join('%-18s %s' % (k, p) for k, p in pats.items()), hits or 'none', v5))

# V6
flag = re.compile(r'(^|\s)(-A|--user-agent|-H|--header|-x|--proxy|--socks\w*|--preproxy|--retry[\w-]*|-b|--cookie|-c|--cookie-jar)(\s|=|$)|user-agent', re.I)
res = [l.rstrip('\n').split('\t') for f in ('wave1.re', 'wave2a.re', 'wave2b.out', 'wave3.out', 'wave4.out') for l in open(T + f)]
cmds = [r[5] for r in res] + [r[3] for r in main + att]
tpl = [l for l in open(T + 'probe.py') if 'curl ' in l and not l.lstrip().startswith('#')]
fhits = [c for c in cmds + tpl if flag.search(c)]
ids = [r[0] for r in res]
urls = [re.search(r"'(https?://[^']+)'$", r[5]).group(1) for r in res]
bodies = sorted(os.path.basename(p) for p in glob.glob(T + 'body/*'))
nobody = sorted(set(ids) - set(bodies))
v6 = 'PASS' if not fhits and len(set(ids)) == len(ids) and len(set(urls)) == len(urls) else 'FAIL'
out.append('**V6 — no command contains an evasion technique, and each candidate was fetched once.**\n\n```\n'
           'flag pattern: %s\ncommands scanned: %d (probe result rows %d + table Command cells %d) + probe.py curl template lines %d\n'
           'hits: %s\nprobe result rows: %d, distinct ids: %d, distinct URLs: %d\nbody files present: %d; ids without a body: %s\n```\n\n'
           'No user-agent, header, proxy, cookie or retry flag in any command. Every id and every URL occurs once '
           '(one attempt per candidate; the only repeat in the session is the UNI egress check, Deviations 1). '
           'An id without a body is a request that received no response: curl writes no output file on a DNS failure → **%s**.'
           % (flag.pattern, len(cmds), len(res), len(main) + len(att), len(tpl), fhits or 'none', len(res), len(set(ids)),
              len(set(urls)), len(bodies), nobody or 'none', v6))

# V7
st = sh('git status --porcelain')
v7 = 'PASS' if st == '?? CryptoReports/TZ-45-coin-catalyst-channels-report.md' else 'FAIL'
out.append('**V7 — `git status --porcelain` is empty apart from the report.**\n\n```\n$ git status --porcelain\n%s\n```\n\n'
           'No file under `analyst/**`, no production file, no bench, no workflow → **%s**.' % (st, v7))

# V8
f0 = ['index.html', 'main.py', 'catalysts.json', 'bench/exhaustion-calibration.txt',
      'bench/backtest_bench.py', 'bench/verify_bench.py', 'bench/backtest_guard_bench.py']
c8 = "git status --porcelain | cut -c4- | grep -x -F %s | wc -l" % ' '.join('-e ' + f for f in f0)
o8, d8 = sh(c8), sh('git diff --name-only HEAD')
v8 = 'PASS' if o8.strip() == '0' and d8 == '' else 'FAIL'
out.append('**V8 — no-regression: no file of the §0 table is in the diff.**\n\n```\n$ %s\n%s\n$ git diff --name-only HEAD\n%s\n```\n\n'
           'Zero §0 files changed and no tracked file changed at all, so every bench figure and gate count TZ-45 §0 '
           'pins is unchanged by construction → **%s**.' % (c8, o8, d8 or '(empty)', v8))

summary = 'V1 N/A · ' + ' · '.join('V%d %s' % (i + 2, v) for i, v in enumerate([v2, v3, v4, v5, v6, v7, v8]))
block = ('Result: **%s**.\n\n' % summary + '\n\n'.join(out) +
         '\n\n<details><summary><code>/tmp/tz45/validate.py</code>, verbatim</summary>\n\n```python\n' +
         open(__file__).read().rstrip('\n') + '\n```\n\n</details>')
assert t.count('@@VALIDATION@@') == 1
open(REPORT, 'w').write(t.replace('@@VALIDATION@@', block))
print(summary)
```

</details>

---

## Test Results

No bench ran and no standing check applied: no production file, bench or workflow moved
(V8). The gate figures TZ-45 §0 pins — `bench.yml` 14 steps, 1 336 147 checks; step 14 487,
step 4 59, step 7 774 130 — were not re-measured. They are unchanged by construction,
because none of the files they read appears in this session's diff.

---

## Deviations

1. **UNI's forum endpoint was requested twice.** The first request, to
   `https://gov.uniswap.org/latest.json`, was the egress check listed above. It ran before
   the candidate list existed, printed only the status, and discarded the body
   (`-o /dev/null`). The second is row UNI, the only UNI request that was classified.
   Every other candidate was requested exactly once (V6).
2. **First-pass classifier defect, corrected offline and without re-fetching.** On a
   Discourse `latest.json` response, the first version of `probe.py` chose the longest
   list of objects, which is `users[]` and carries no dates. It therefore called 15 of the
   16 class-1 rows `primary-undated`; ONDO's DNS failure was unaffected. The analyser was
   rewritten to prefer the record list that carries dates (the version quoted above).
   Waves 1 and 2a were then re-classified from the **saved bodies** with
   `probe.py --reanalyse`, which issues no request. 15 class-1 verdicts moved to
   `primary-dated`, and wave 2a's 13 verdicts were identical in both passes. Every verdict
   in this report comes from the corrected analyser.
3. **Class 4 was measured with one unfiltered request.** The list endpoint used takes no
   symbol parameter, so the three coins that reached class 4 were served by one request.
   The symbol filter was then applied client-side to the saved response, printing counts
   only. This made fewer requests than one per coin and read no content.
4. **Discourse was read at `/latest.json`.** §4 names `<topic-url>.json` and
   `/c/<slug>.json` as the two Discourse JSON endpoints. `/latest.json` is the same
   `topic_list` schema across every category of the instance, and it needs no category
   slug, which would itself have to be guessed.
5. **TZ-45 carries no `## Commit Message` section**, while contract §8 requires the commit
   message verbatim from it. The report commit uses the established form of every report
   commit since TZ-38: `docs(reports): TZ-NN — <summary> (TZ-NN)`.

---

## Pre-existing Issues

1. **The map's `## 0` block records a contract version the repository no longer carries.**
   The map reads «Contract **v20** — 814 lines, MD5 `9a257890e9db663eb0fc74129f4841e0` — is
   unchanged at this revision». `EXECUTOR-INSTRUCTIONS.md` on `origin/main` is **v21**, 831
   lines, `5b125d9a39bc4ccd4e935d01ed1aa1e8`, uploaded in `f5cd53a` after revision
   `2026-09-14-a`. That line of the map is not a gate anchor. Under contract §5 the
   difference is reported and not acted on; which side is ahead is the Architect's call.
2. **TZ-45's §0 quotes the revision string and the file table, but none of the map's six other content anchors.** Contract §5 requires every TZ header to quote the `## 0` block «in full … never a subset». Counted by `grep -qF` of each of the six anchors against each TZ file: TZ-42, TZ-43 and TZ-44 quote **6/6**, TZ-45 quotes **0/6**. The gate stops on a MISMATCH, and nothing TZ-45 quotes mismatches. To leave no anchor unchecked, the gate was run against all seven anchors taken from the map's own block, and all 7 are present (`## Scope Executed` step 3). The gap is in the header's completeness, which is the Architect's; it is recorded here and did not stop the run.

---

## Remaining Risks

1. **`primary-dated` establishes a dated STREAM, not class-A event dates.** Each date field
   named above dates the record: when a topic was opened, a release published, a post
   written. The date of the vote, upgrade or unlock a record announces sits in its
   content, which this TZ forbids reading. Whether each channel actually carries class-A
   dates in its content is unmeasured.
2. **The candidate hosts come from the Executor's knowledge, and so do the 17 `(none)` slots
   (14 in class 1, 1 in class 2, 2 in class 3); ownership was verified structurally, not by a
   registry.** Each host answered with the schema expected of its
   class: Discourse `topic_list`, a releases array, an RSS feed, or an explorer's token
   object whose `symbol` equalled `ONDO` and whose `type` equalled `ERC-20`. Four hosts
   deserve the Architect's judgement before §6a names them as the protocol's own:
   - `forum.cardano.org`: the Cardano community forum;
   - `ethereum-magicians.org`: the EIP discussion forum, not a foundation's governance
     forum;
   - `rendernetwork.medium.com`: the protocol's publication on a third-party host;
   - `gov.ethenafoundation.com`.
   Two class-1 hosts redirected, and §6a should name where the request landed rather than
   where it was sent: SKY `forum.sky.money → forum.skyeco.com`, ALGO
   `forum.algorand.org → forum.algorand.co`.
3. **LIT = Lighter is an inference.** The repository names no protocol behind the symbol:
   the map says only that it has no usable spot leg. The empty class 1–3 candidate set was
   reasoned for Lighter. Row LIT's own reading, class 4, is keyed to the symbol and does
   not depend on the identity. GRAM = TON is backed by the repository: the map records the
   `TON → GRAM` rename joint.
4. **The contract-state lane returns state, not dated records.** `eth.blockscout.com`
   answered ONDO's token contract keyless, with a single object and no record list. A
   plain ERC-20 token contract holds no schedule. The dates §6 wants from this lane (a
   cliff, a vesting release) live in separate vesting contracts, whose addresses are
   protocol-specific and were not probed. This lane was measured on one coin only.
5. **The closed verdict set cannot tell apart two readings that both land on
   `primary-undated`.** One is a candidate URL that does not exist (ONDO c2, HTTP `404`);
   the other is a live channel that serves nothing dated for this coin (HYPE c2, an empty
   `[]`; the class-4 symbol filters returning 0). The verdict followed the letter of the
   definition, «the host answered; no dated records», and the HTTP column carries the
   difference.
6. **Eleven coin lanes share one unauthenticated quota.** The 10 dated rows on
   `api.github.com` plus HYPE draw on its core limit of 60 requests an hour per client
   address, so one refresh of the coin horizon costs 11 of them.
7. **The class-4 window is shallow.** `pageSize=50` returns the latest 50 records per
   catalogue. A filter count of 0 means none inside that window, not that the exchange
   never announces the symbol.
8. **A release is not an upgrade by construction.** GitHub and GitLab release streams
   include client patch releases. Which release is a class-A protocol upgrade is
   decidable only from content.
9. **One reading at one moment** (22:35Z to 22:39Z, 15.09.2026). A host that answered here
   may refuse on the next run and the reverse (map inv. 52); the command beside each row
   is what re-measures it.

---

## Commit

Report commit, direct to `main` on the `CryptoReports/**` path (contract §8). Contents:
this file only.

```
docs(reports): TZ-45 — one catalyst channel per tokens[] member: 27 of 30 primary-dated, ONDO/HYPE/LIT primary-undated (TZ-45)
```

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

## CI Execution

**No workflow ran for this TZ.** No branch was pushed and no code path moved. The five
workflows' triggers were read from the working tree:

- `main.yml`: `push` to `main` with a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`, plus `workflow_dispatch`. This confirms the allow-list
  contract §8 requires verified before the first direct push of a session.
- `bench.yml`: `push` on `main` and `claude/**` with `'**.md'` in `paths-ignore`, plus
  `pull_request`.
- `calib.yml`: `claude/**` pushes touching `bench/exhaustion_calib.py` or its own file,
  plus dispatch.
- `journal.yml`: schedule and dispatch only.
- `backtest_bench.yml`: dispatch only.

A commit that changes one `.md` file under `CryptoReports/` clears none of these filters.

## Final Repository State

The checkout the fingerprints were taken against is harness worktree branch
`worktree-bridge-cse_013D2XfmWy3jozb4g6z8mpTe`. It was fast-forwarded to `57ea70e`
(`57ea70e37f88946c84b264fc51224162a346e388`), whose tree was identical to `origin/main`
when the gate ran. At validation time its working tree differed from that commit by this
one untracked report (V7). The probe scratch — response bodies, header dumps, result files
and scripts under `/tmp/tz45/` and `/tmp/tz45-*` — lived outside the repository.
It was removed after validation and before this report was committed:
`rm -rf /tmp/tz45 /tmp/tz45-*`, then `ls -d /tmp/tz45*` → `ls: cannot access '/tmp/tz45*': No such file or directory`. Every script it held is
quoted verbatim above, so each reading reproduces from this report alone.

## Fingerprints

Measured on `57ea70e`, which is the tree of `origin/main` after the fetch.

| File | Lines | MD5 | Required by | Match |
|---|---:|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2723 | `060c25c0273f6ec527ad21f91bf9342d` | revision `2026-09-14-a` (TZ-45 §0) | revision ✓, 7/7 anchors ✓; lines and MD5 reported, not enforced |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | map §0 / TZ-45 §0 | ✓ |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | map §0 / TZ-45 §0 | ✓ |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | map §0 / TZ-45 §0 | ✓ |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | map §0 / TZ-45 §0 | ✓ |
| `bench/backtest_bench.py` | 5102 | `ba633202f43845ba0fdafbc1b92d9c04` | TZ-45 §0 bench anchor | ✓ |
| `bench/verify_bench.py` | 540 | `28eb1949f21d0afadb062303108f7101` | TZ-45 §0 bench anchor | ✓ |
| `bench/backtest_guard_bench.py` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` | TZ-45 §0 bench anchor | ✓ |
| `journal/write.js` | 849 | `19722fb53d75b6d25a8f957f74f97422` | map §0 prose | ✓ |
| `bench/journal_bench.js` | 1177 | `993271f44995c8ae21c54935a3f80adf` | map §0 prose | ✓ |
| `EXECUTOR-INSTRUCTIONS.md` | 831 | `5b125d9a39bc4ccd4e935d01ed1aa1e8` | map §0 prose: v20, 814, `9a257890…` | ✗, Pre-existing Issues 1 |
| `ANALYST-INSTRUCTIONS.md` | 2854 | `b3004b68bf195f42885e41ca2110ca29` | — | reported |
| `CryptoTZ/TZ-45-coin-catalyst-channels.md` | 172 | `b610eeaa4d52826c087ef70ac16c1509` | — | reported |

`sed -n '/^## 6\./,/^## 7\./p' ANALYST-INSTRUCTIONS.md | md5sum` → `ed0b4981c5fb71cdc96dc99bdada0daf`: the
`sec6_md5` of the §6 and §6a text these channels were measured under (methodology §6a).
