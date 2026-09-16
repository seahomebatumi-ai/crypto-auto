# Implementation Report — TZ-46

## Status

**COMPLETED.** Report-only TZ. Of TZ §4's three class-2 candidates, **two were requested and
both answered `primary-dated`**: ETH-c2a (`blog.ethereum.org`, an RSS feed) and ADA-c2a
(`api.github.com`, the `IntersectMBO/cardano-node` releases). ETH-c2b was **not requested**,
because the stop rule ended ETH at ETH-c2a. **2 requests · 2 `primary-dated` · 0
`primary-undated` · 0 `refused` · 0 `unreachable` · 0 `none-found` · 1
`not requested — stop rule`.** No title, date or other content value from either response is
recorded here. The previous TZ, TZ-45, was report-only and left no branch (its report is
commit `aa9f5ab`, on `main`).

---

## Inbound Filing

`CryptoTZ/TZ-46-eth-ada-release-channels.md` arrived under its canonical name in the Boss's
upload commit `e04eb3f`, the only commit touching that path (`git log --all -- <path>`).
Nothing was moved or renamed, and no second copy exists in the root or on any branch.

---

## Scope Executed

**Class: report-only TZ** (contract §8). TZ §2 authorises exactly one written file, this
report, on the `CryptoReports/**` direct-push path. Files to Modify, Rename and Delete are all
`None`.

Run order under contract §4a:

1. `git fetch --all --prune` exited 0; the only ref change was the pruned
   `origin/claude/tz-44-verify-comparability-i9-union`. `git rev-parse --is-shallow-repository`
   → `false`.
2. The harness worktree branch was already at `origin/main` (`git rev-parse HEAD origin/main`
   printed `e04eb3f8b07f935b5d505225233260002683567d` twice), and `git status --porcelain`
   printed nothing. No merge was needed.
3. Fingerprint gate (contract v22 §5). The anchor list came from the map's own `## 0` table:
   **7 anchors compared. The TZ header's cell was identical for 7 of 7, and 7 of 7 were
   present in the map as exact, case-sensitive substrings.** The text each match returned is
   recorded under `## Fingerprints`. The map's revision is `2026-09-16-a`, which is what TZ-46
   §0 requires. All four file-table rows in the TZ header are identical to the map's, and all
   four files match.
4. Repository state: TZ-45 is report-only, and no `*tz-45*` or `*tz45*` branch exists
   (`git branch --all --list '*tz-45*' '*tz45*' | wc -l` → `0`). `main.yml` is still a `paths` allow-list of exactly
   `main.py` and `.github/workflows/main.yml` (read before the first push, contract §8).
5. TZ §5: the instrument was rebuilt from TZ-45's report. §4: one request per candidate, in
   order. §6: this report. §7: V1–V7.

Not done, because it is out of scope (TZ §8): no record's title, date or content was read into
this report; no host, class, symbol or page outside §4 was requested; no request was retried;
and nothing was written to `analyst/**`, `ANALYST-INSTRUCTIONS.md`, `catalysts.json`, or any
production, bench or workflow file. **No HTTP request other than the two candidate requests
was made in this session**: no egress check and no rate-limit read. The only other network
traffic was `git fetch` to the repository's own remote, which contract §3 requires.

---

## Files Created

- `CryptoReports/TZ-46-eth-ada-release-channels-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Instrument (TZ §5)

`/tmp/tz46/probe.py` is TZ-45's `probe.py`, taken by command from the fenced block under
`### Instrument` in `CryptoReports/TZ-45-coin-catalyst-channels-report.md`. Its only change is
that every `/tmp/tz45` became `/tmp/tz46`:

````
$ mkdir -p /tmp/tz46/body /tmp/tz46/hdr && R=CryptoReports/TZ-45-coin-catalyst-channels-report.md
$ awk 'index($0,"`/tmp/tz45/probe.py`, verbatim")==1{f=1;next} f==1&&/^```python$/{f=2;next} f==2&&/^```$/{exit} f==2' $R > /tmp/tz46/probe.tz45.py
$ sed 's#/tmp/tz45#/tmp/tz46#g' /tmp/tz46/probe.tz45.py > /tmp/tz46/probe.py
$ wc -l /tmp/tz46/probe.tz45.py /tmp/tz46/probe.py
  97 /tmp/tz46/probe.tz45.py
  97 /tmp/tz46/probe.py
 194 total
$ md5sum /tmp/tz46/probe.tz45.py /tmp/tz46/probe.py
bc428d3e169e0eca91114915c1951190  /tmp/tz46/probe.tz45.py
e9fa46c89139cff05477b5be0e35aae1  /tmp/tz46/probe.py
$ diff -U0 /tmp/tz46/probe.tz45.py /tmp/tz46/probe.py; echo "diff exit=$?"
--- /tmp/tz46/probe.tz45.py	2026-09-16 09:22:51.959568488 +0000
+++ /tmp/tz46/probe.py	2026-09-16 09:22:51.960568497 +0000
@@ -59 +59 @@
-    bp, hp = '/tmp/tz45/body/' + pid, '/tmp/tz45/hdr/' + pid
+    bp, hp = '/tmp/tz46/body/' + pid, '/tmp/tz46/hdr/' + pid
@@ -82 +82 @@
-        cmd = ("curl -sS -L -m 20 -o /tmp/tz45/body/%s -D /tmp/tz45/hdr/%s "
+        cmd = ("curl -sS -L -m 20 -o /tmp/tz46/body/%s -D /tmp/tz46/hdr/%s "
diff exit=1
$ echo "tz45 paths in quoted=$(grep -o /tmp/tz45 /tmp/tz46/probe.tz45.py | wc -l), tz46 paths in run=$(grep -o /tmp/tz46 /tmp/tz46/probe.py | wc -l), tz45 left in run=$(grep -o /tmp/tz45 /tmp/tz46/probe.py | wc -l)"
tz45 paths in quoted=4, tz46 paths in run=4, tz45 left in run=0
$ python3 -m py_compile /tmp/tz46/probe.py && echo compiled; rm -rf /tmp/tz46/__pycache__
compiled
$ curl --version | head -1
curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10
$ python3 --version
Python 3.12.3
````

`-U0` shows one hunk per edited line. There are two hunks, and both change a `/tmp/tz45` path
and nothing else. The classifier, the verdict rule and the five verdict words are unchanged.

`/tmp/tz46/probe.py`, verbatim as run (copied from the file, not transcribed):

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
    bp, hp = '/tmp/tz46/body/' + pid, '/tmp/tz46/hdr/' + pid
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
        cmd = ("curl -sS -L -m 20 -o /tmp/tz46/body/%s -D /tmp/tz46/hdr/%s "
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

### Probe runs — one request per candidate, one at a time (TZ §4)

Each candidate file held one row. The next command was issued only after the previous verdict
had been printed and read. Run from `/tmp/tz46`:

```
$ printf 'ETH-c2a\tETH\t2\thttps://blog.ethereum.org/feed.xml\n' > c-ETH-c2a.tsv && python3 probe.py c-ETH-c2a.tsv | tee r-ETH-c2a.out | tr '\t' '\n' | nl -ba
$ printf 'ADA-c2a\tADA\t2\thttps://api.github.com/repos/IntersectMBO/cardano-node/releases?per_page=5\n' > c-ADA-c2a.tsv && python3 probe.py c-ADA-c2a.tsv | tee r-ADA-c2a.out | tr '\t' '\n' | nl -ba
```

Each command printed its row's 13 fields, one per line, and exited 0. The decisions were made
on field 12. For ETH-c2a it read `primary-dated`, so ETH stopped and ETH-c2b was never sent
(§4.2). The ADA command was issued only after that. For ADA-c2a it also read
`primary-dated`, and §4 names no further ADA candidate.

The probe's result rows, verbatim (`cat r-ETH-c2a.out r-ADA-c2a.out`). The fields are
tab-separated in `row()` order: id · symbol · class · host requested · host answered ·
command · HTTP · content type · body kind · record list · date keys · verdict · note.

```
ETH-c2a	ETH	2	blog.ethereum.org	blog.ethereum.org	curl -sS -L -m 20 -o /tmp/tz46/body/ETH-c2a -D /tmp/tz46/hdr/ETH-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://blog.ethereum.org/feed.xml'	200	application/xml	xml	items[639]	pubDate	primary-dated	curl exit 0
ADA-c2a	ADA	2	api.github.com	api.github.com	curl -sS -L -m 20 -o /tmp/tz46/body/ADA-c2a -D /tmp/tz46/hdr/ADA-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/IntersectMBO/cardano-node/releases?per_page=5'	200	application/json; charset=utf-8	json	$[5]	created_at,published_at,updated_at	primary-dated	curl exit 0
```

### Candidate table (TZ §6.1)

| Id | Symbol | Class | Command | HTTP | Host requested | Host answered | Content type | Record list | Date keys | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ETH-c2a | ETH | 2 | `curl -sS -L -m 20 -o /tmp/tz46/body/ETH-c2a -D /tmp/tz46/hdr/ETH-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://blog.ethereum.org/feed.xml'` | 301 → 200 | blog.ethereum.org | blog.ethereum.org | `application/xml` | `items[639]` | `pubDate` | primary-dated |
| ETH-c2b | ETH | 2 | — | — | — | — | — | — | — | not requested — stop rule |
| ADA-c2a | ADA | 2 | `curl -sS -L -m 20 -o /tmp/tz46/body/ADA-c2a -D /tmp/tz46/hdr/ADA-c2a -w '%{http_code} %{url_effective} %{content_type}' 'https://api.github.com/repos/IntersectMBO/cardano-node/releases?per_page=5'` | 200 | api.github.com | api.github.com | `application/json; charset=utf-8` | `$[5]` | `created_at`, `published_at`, `updated_at` | primary-dated |

**ETH-c2a was redirected once, on the same host.** The probe prints the final status (`200`)
and the answering host, which equals the requested one. The `301` and its target come from the
saved header dump. No request was made to read them (Deviations 1):

```
$ grep -i -E '^(HTTP/|location:)' /tmp/tz46/hdr/ETH-c2a | tr -d '\r'
HTTP/2 301 
location: /en/feed.xml
HTTP/2 200 
```

The request went to path `/feed.xml`, and the `200` is the answer at path `/en/feed.xml` on
`blog.ethereum.org`. ADA-c2a's header dump holds one status block (`schema.py`, below) and no
`location` line:

```
$ grep -i '^location:' /tmp/tz46/hdr/ADA-c2a | wc -l
0
```

### The date field of each `primary-dated` row (TZ §6.2, schema, never a value)

- ETH-c2a (`blog.ethereum.org`) — `rss > channel > item > pubDate` — RFC-822 string, on 639 of 639 items; no other date-shaped tag on an item
- ADA-c2a (`api.github.com`) — `[].published_at` — ISO-8601 string, on 5 of 5 records; `created_at` and `updated_at` beside it, same type

The name and type claims come from an offline reading of the two saved bodies. It made no
request and printed names, types and counts only (Deviations 2).

`/tmp/tz46/schema.py`, verbatim as run:

```python
#!/usr/bin/env python3
# TZ-46 offline schema check on the SAVED bodies: no request. Prints tag/key NAMES,
# types and counts only -- never a value from a body.
import json, re, email.utils, xml.etree.ElementTree as ET
B = '/tmp/tz46/body/'
ISO = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$')
RFC822 = re.compile(r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun), \d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) '
                    r'\d{4} \d{2}:\d{2}(:\d{2})? (GMT|UT|[A-Z]{1,3}|[+-]\d{4})$')
DATEY = ('pubDate', 'published', 'updated', 'date', 'lastBuildDate')

def local(t):
    return t.split('}', 1)[-1]

# ETH-c2a -- RSS/Atom feed
root = ET.parse(B + 'ETH-c2a').getroot()
chans = [e for e in root if local(e.tag) == 'channel']
items = [e for e in root.iter() if local(e.tag) in ('item', 'entry')]
print('ETH-c2a root=%s channel-children=%d items(parsed)=%d' % (local(root.tag), len(chans), len(items)))
print('ETH-c2a item parents:', sorted({local(p.tag) for p in root.iter() for c in p if local(c.tag) in ('item', 'entry')}))
kids = sorted({local(c.tag) for i in items for c in i if any(d.lower() in local(c.tag).lower() for d in DATEY)})
print('ETH-c2a date-shaped child tags of item:', kids)
for k in kids:
    vals = [c.text or '' for i in items for c in i if local(c.tag) == k]
    print('ETH-c2a %s: on-items=%d/%d rfc822-regex=%d parsedate-ok=%d' % (
        k, sum(1 for i in items if any(local(c.tag) == k for c in i)), len(items),
        sum(1 for v in vals if RFC822.match(v.strip())),
        sum(1 for v in vals if email.utils.parsedate_tz(v.strip()) is not None)))

# ADA-c2a -- GitHub releases array
d = json.load(open(B + 'ADA-c2a'))
print('ADA-c2a top-level=%s length=%d all-dicts=%s' % (type(d).__name__, len(d), all(isinstance(r, dict) for r in d)))
for k in ('published_at', 'created_at', 'updated_at'):
    print('ADA-c2a [].%s: present=%d iso8601-str=%d null=%d other=%d' % (
        k, sum(1 for r in d if k in r), sum(1 for r in d if isinstance(r.get(k), str) and ISO.match(r[k])),
        sum(1 for r in d if k in r and r[k] is None),
        sum(1 for r in d if k in r and r[k] is not None and not (isinstance(r[k], str) and ISO.match(r[k])))))
print('ADA-c2a boolean keys present: draft=%d prerelease=%d' % (sum(1 for r in d if isinstance(r.get('draft'), bool)),
                                                                  sum(1 for r in d if isinstance(r.get('prerelease'), bool))))
# redirect hops: HTTP status lines per header dump (status codes only)
for pid in ('ETH-c2a', 'ADA-c2a'):
    st = [l.split()[1] for l in open('/tmp/tz46/hdr/' + pid, errors='replace') if l.startswith('HTTP/')]
    print('%s header blocks=%d statuses=%s' % (pid, len(st), st))
```

```
$ python3 /tmp/tz46/schema.py
ETH-c2a root=rss channel-children=1 items(parsed)=639
ETH-c2a item parents: ['channel']
ETH-c2a date-shaped child tags of item: ['pubDate']
ETH-c2a pubDate: on-items=639/639 rfc822-regex=639 parsedate-ok=639
ADA-c2a top-level=list length=5 all-dicts=True
ADA-c2a [].published_at: present=5 iso8601-str=5 null=0 other=0
ADA-c2a [].created_at: present=5 iso8601-str=5 null=0 other=0
ADA-c2a [].updated_at: present=5 iso8601-str=5 null=0 other=0
ADA-c2a boolean keys present: draft=5 prerelease=5
ETH-c2a header blocks=2 statuses=['301', '200']
ADA-c2a header blocks=1 statuses=['200']
```

These fields date the **record**: a blog post's publication or a release's publication. They
do not date the network upgrade a record may announce, because reading that would mean reading
content, which TZ §8 forbids (Remaining Risks 1).

### Tallies (TZ §6.3)

| | Count |
|---|---:|
| Candidates named in TZ §4 | 3 |
| Requests made (probe result rows) | 2 |
| Rows with a command | 2 |
| `primary-dated` | 2 — ETH-c2a, ADA-c2a |
| `primary-undated` | 0 |
| `refused` | 0 |
| `unreachable` | 0 |
| `none-found` | 0 |
| `not requested — stop rule` | 1 — ETH-c2b |

By symbol: **ETH** stopped at its first candidate, class 2 on the Ethereum Foundation blog's
feed. **ADA** stopped at its only candidate, class 2 on the `cardano-node` releases.

### Measurement window (TZ §6.4)

Taken from the modification times of the first and last body files. Run from `/tmp/tz46`:

```
$ for f in $(ls -tr body); do echo "$f $(date -u -r body/$f +%FT%T.%NZ) $(stat --format=%s body/$f) bytes"; done
ETH-c2a 2026-09-16T09:23:06.648691014Z 527621 bytes
ADA-c2a 2026-09-16T09:23:17.430781073Z 253618 bytes
```

**Window: 16.09.2026, 09:23:06Z to 09:23:17Z UTC**, from the first body file `ETH-c2a` to
the last, `ADA-c2a`.

---

## Validation

Result: **V1 PASS · V2 PASS · V3 PASS · V4 PASS · V5 PASS · V6 PASS · V7 PASS**.

**V1 — rows.**

```
$ python3 /tmp/tz46/validate.py   # candidate table vs TZ §4
TZ §4 ids, in order:     ETH-c2a, ETH-c2b, ADA-c2a
table ids, in order:     ETH-c2a, ETH-c2b, ADA-c2a
rows: 3
rows with a command: 2
rows not requested: 1 (ETH-c2b)
rows neither command+verdict nor not-requested: none
not-requested rows without an earlier primary-dated row of the same symbol: none
rows whose symbol differs from TZ §4: none
```

Three rows in §4 order; the one `not requested` row, ETH-c2b, follows ETH-c2a, which is `primary-dated` → **PASS**.

**V2 — verdict words.**

```
rows checked (rows carrying a verdict): 2
rows excluded as `not requested — stop rule`: 1
inadmissible: none
primary-dated    2
primary-undated  0
refused          0
unreachable      0
none-found       0
```

→ **PASS**.

**V3 — one request per candidate.**

```
$ python3 /tmp/tz46/validate.py   # reads r-ETH-c2a.out and r-ADA-c2a.out: one line per request
requests made (probe result rows): 2
rows with a command: 2
table Command cells equal to the command the probe executed, same id: 2
probe ids: 2, distinct 2; probe URLs: 2, distinct 2; table ids: 3, distinct 3
$ ls /tmp/tz46/body /tmp/tz46/hdr
/tmp/tz46/body:
ADA-c2a
ETH-c2a

/tmp/tz46/hdr:
ADA-c2a
ETH-c2a
commands scanned for URLs: 20 (Command cells 2 + `$ ` lines in non-python blocks 16 + probe rows 2)
distinct URLs in all commands: 2
TZ §4 URLs: 3
(URLs in commands) minus (TZ §4 URLs): empty (0)
```

Two requests for two commanded rows, each id and URL once, and every URL in every command is one of §4's three → **PASS**.

**V4 — no evasion.** TZ-45's V6 flag pattern, over every line of this report outside a python block (prose, every table row including the Command cells, and every line of every command/output block), the command each probe row executed, every line of `probe.py` containing `curl`, and the commands this validation prints.

```
flag pattern: (^|\s)(-A|--user-agent|-H|--header|-x|--proxy|--socks\w*|--preproxy|--retry[\w-]*|-b|--cookie|-c|--cookie-jar)(\s|=|$)|user-agent
report lines scanned: 463 (prose 365 + non-python block lines 98); python block lines not scanned: 139
probe result commands: 2
probe.py lines containing curl: 3
validation commands: 7
lines scanned in total: 475
hits: none
quoted python block byte-identical to the file as run: probe.py True, schema.py True
quoted output block identical to the saved output: probe.out True, schema.out True
```

No user-agent, header, proxy, cookie or retry flag anywhere. The `flag pattern:` line above is the pattern itself and matches itself; it is written after the scan → **PASS**.

**V5 — no product fact.** TZ-45's V5 patterns over every table row of this report (all four tables, header rows included, separator rows excluded) and every date-field line.

```
ISO date           \b(19|20)\d{2}-\d{2}-\d{2}\b
dd.mm.yyyy date    \b\d{1,2}\.\d{1,2}\.(19|20)\d{2}\b
month name         \b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d
currency amount    [$€£]\s?\d|\d\s?(USD|USDT|BTC|ETH)\b
numeric percent    \d+(\.\d+)?\s?%
epoch-like number  \b\d{10,13}\b
large figure       \b\d{1,3}([ ,]\d{3}){2,}\b
table rows scanned: 28
date-field lines scanned: 2
lines scanned: 30
hits: none
```

Every cell is an id, a symbol, a class, a command, an HTTP status, a host, a content type, a record-list shape, a key name, a verdict, a count or a fingerprint; the date-field lines name fields and types only → **PASS**.

**V6 — nothing else written.**

```
$ git status --porcelain
?? CryptoReports/TZ-46-eth-ada-release-channels-report.md
$ git diff --name-only HEAD
(empty — no output)
```

One untracked path, this report; no tracked file differs from `HEAD` → **PASS**.

**V7 — scratch removed.**

```
$ rm -rf /tmp/tz46
(exit 0)
$ ls -d /tmp/tz46*
ls: cannot access '/tmp/tz46*': No such file or directory
(exit 2)
```

The glob matches nothing and `ls` fails with the error above → **PASS**. This script had read itself before the removal, which is how it is quoted below.

<details><summary><code>/tmp/tz46/validate.py</code>, verbatim</summary>

```python
#!/usr/bin/env python3
# TZ-46 §7 validation: runs V1-V7 against the report, the probe records and the tree, and
# splices the evidence (commands + outputs) into the report's @@VALIDATION@@ placeholder.
#   validate.py --dry   -> V1-V6 printed; nothing removed, nothing written
#   validate.py         -> V1-V7; V7 removes /tmp/tz46, then the block is written
import sys, subprocess, re, collections, hashlib
REPO = '/root/crypto-auto/.claude/worktrees/bridge-cse_011UxGXnrPSwgGra1vY7BBF6'
REL = 'CryptoReports/TZ-46-eth-ada-release-channels-report.md'
REPORT = REPO + '/' + REL
TZ = REPO + '/CryptoTZ/TZ-46-eth-ada-release-channels.md'
T = '/tmp/tz46/'
DRY = '--dry' in sys.argv
SELF = open(__file__).read()          # read now: V7 deletes this file
VER = ['primary-dated', 'primary-undated', 'refused', 'unreachable', 'none-found']
NR = 'not requested — stop rule'
PRINTED = ['python3 /tmp/tz46/validate.py', 'python3 /tmp/tz46/validate.py --dry',
           'ls /tmp/tz46/body /tmp/tz46/hdr', 'git status --porcelain', 'git diff --name-only HEAD',
           'rm -rf /tmp/tz46', 'ls -d /tmp/tz46*']
ok = lambda b: 'PASS' if b else 'FAIL'

def sh(cmd):
    r = subprocess.run(cmd, shell=True, cwd=REPO, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).rstrip('\n')

t = open(REPORT).read()
assert t.count('@@VALIDATION@@') == 1

def split_md(text):
    """(prose lines, [(info, lines)]) -- a fence closes on its own char at >= its length."""
    prose, blocks, fence, cur = [], [], None, None
    for l in text.splitlines():
        if fence is None:
            m = re.match(r'^(`{3,}|~{3,})(\S*)\s*$', l)
            if m:
                fence, cur = m.group(1), (m.group(2), [])
            else:
                prose.append(l)
            continue
        s = l.strip()
        if s and set(s) == {fence[0]} and len(s) >= len(fence):
            blocks.append(cur)
            fence = cur = None
        else:
            cur[1].append(l)
    assert fence is None, 'unclosed fence'
    return prose, blocks

SEP = re.compile(r'^\|[-|: ]+\|$')
def rows(lines):
    return [[c.strip() for c in l.strip()[1:-1].split('|')]
            for l in lines if l.startswith('|') and not SEP.match(l.strip())]
def between(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]

prose, blocks = split_md(t)
csec_prose, _ = split_md(between(t, '### Candidate table (TZ §6.1)', '\n### '))
ctab = rows(csec_prose)
hdr, cand = ctab[0], ctab[1:]
I, S, C, V = hdr.index('Id'), hdr.index('Symbol'), hdr.index('Command'), hdr.index('Verdict')
tz4 = rows(between(open(TZ).read(), '## 4. Candidates', '\n1. ').splitlines())[1:]
ids4, sym4, urls4 = [r[0] for r in tz4], [r[1] for r in tz4], [r[3].strip('`') for r in tz4]
res = [l.rstrip('\n').split('\t') for f in ('r-ETH-c2a.out', 'r-ADA-c2a.out') for l in open(T + f)]
out = []

# V1 -- rows
ids = [r[I] for r in cand]
withcmd = [r for r in cand if r[C].startswith('`curl ')]
notreq = [r for r in cand if r[V] == NR]
malformed = [r[I] for r in cand if not ((r[C].startswith('`curl ') and r[V] and r[V] != NR)
                                        or (r[V] == NR and not r[C].startswith('`curl ')))]
misplaced = [r[I] for k, r in enumerate(cand) if r[V] == NR
             and not any(p[S] == r[S] and p[V] == 'primary-dated' for p in cand[:k])]
symbad = [r[I] for r in cand if r[I] not in ids4 or sym4[ids4.index(r[I])] != r[S]]
v1 = ok(len(cand) == 3 and ids == ids4 and not malformed and not misplaced and not symbad)
out.append('**V1 — rows.**\n\n```\n$ python3 /tmp/tz46/validate.py   # candidate table vs TZ §4\n'
           'TZ §4 ids, in order:     %s\ntable ids, in order:     %s\nrows: %d\nrows with a command: %d\n'
           'rows not requested: %d (%s)\nrows neither command+verdict nor not-requested: %s\n'
           'not-requested rows without an earlier primary-dated row of the same symbol: %s\n'
           'rows whose symbol differs from TZ §4: %s\n```\n\n'
           'Three rows in §4 order; the one `not requested` row, ETH-c2b, follows ETH-c2a, which is '
           '`primary-dated` → **%s**.'
           % (', '.join(ids4), ', '.join(ids), len(cand), len(withcmd), len(notreq),
              ', '.join(r[I] for r in notreq) or '-', malformed or 'none', misplaced or 'none',
              symbad or 'none', v1))

# V2 -- verdict words
judged = [r for r in cand if r[V] != NR]
dist = collections.Counter(r[V] for r in judged)
inad = [r[I] + ':' + r[V] for r in judged if r[V] not in VER]
v2 = ok(judged and not inad)
out.append('**V2 — verdict words.**\n\n```\nrows checked (rows carrying a verdict): %d\n'
           'rows excluded as `%s`: %d\ninadmissible: %s\n%s\n```\n\n→ **%s**.'
           % (len(judged), NR, len(notreq), inad or 'none',
              '\n'.join('%-16s %d' % (v, dist.get(v, 0)) for v in VER), v2))

# V3 -- one request per candidate
URL = re.compile(r"https?://[^\s'\"`|)\\]+")    # a backslash ends a URL: printf's \n is not part of it
dollar = [l[2:] for info, ls in blocks if info != 'python' for l in ls if l.startswith('$ ')]
cmds_all = [r[C].strip('`') for r in withcmd] + dollar + [r[5] for r in res]
urls_all = {u for c in cmds_all for u in URL.findall(c)}
res_ids = [r[0] for r in res]
res_urls = [re.search(r"'(https?://[^']+)'$", r[5]).group(1) for r in res]
cellmatch = sum(1 for r in withcmd for p in res if p[0] == r[I] and p[5] == r[C].strip('`'))
_, bodies = sh('ls /tmp/tz46/body /tmp/tz46/hdr')
diff = sorted(urls_all - set(urls4))
v3 = ok(res and len(res) == len(withcmd) == cellmatch and len(set(res_ids)) == len(res_ids)
        and len(set(res_urls)) == len(res_urls) and len(set(ids)) == len(ids) and not diff)
out.append('**V3 — one request per candidate.**\n\n```\n$ python3 /tmp/tz46/validate.py   # reads r-ETH-c2a.out and r-ADA-c2a.out: one line per request\n'
           'requests made (probe result rows): %d\nrows with a command: %d\n'
           'table Command cells equal to the command the probe executed, same id: %d\n'
           'probe ids: %d, distinct %d; probe URLs: %d, distinct %d; table ids: %d, distinct %d\n'
           '$ ls /tmp/tz46/body /tmp/tz46/hdr\n%s\n'
           'commands scanned for URLs: %d (Command cells %d + `$ ` lines in non-python blocks %d + probe rows %d)\n'
           'distinct URLs in all commands: %d\nTZ §4 URLs: %d\n(URLs in commands) minus (TZ §4 URLs): %s\n```\n\n'
           'Two requests for two commanded rows, each id and URL once, and every URL in every command is one of '
           '§4\'s three → **%s**.'
           % (len(res), len(withcmd), cellmatch, len(res_ids), len(set(res_ids)), len(res_urls),
              len(set(res_urls)), len(ids), len(set(ids)), bodies, len(cmds_all), len(withcmd), len(dollar),
              len(res), len(urls_all), len(urls4), diff or 'empty (0)', v3))

# V4 -- no evasion
flag = re.compile(r'(^|\s)(-A|--user-agent|-H|--header|-x|--proxy|--socks\w*|--preproxy|--retry[\w-]*|-b|--cookie|-c|--cookie-jar)(\s|=|$)|user-agent', re.I)
nonpy = [l for info, ls in blocks if info != 'python' for l in ls]
pyn = sum(len(ls) for info, ls in blocks if info == 'python')
curl_lines = [l.rstrip('\n') for l in open(T + 'probe.py') if 'curl' in l]
scan = prose + nonpy + [r[5] for r in res] + curl_lines + PRINTED
fhits = [l for l in scan if flag.search(l)]
md5 = lambda s: hashlib.md5(s.encode()).hexdigest()
pyblocks = ['\n'.join(ls) + '\n' for info, ls in blocks if info == 'python']
quoted = {f: md5(open(T + f).read()) in {md5(b) for b in pyblocks} for f in ('probe.py', 'schema.py')}
txtblocks = {'\n'.join(l for l in ls if not l.startswith('$ ')) for info, ls in blocks if info != 'python'}
qout = {f: open(T + f).read().rstrip('\n') in txtblocks for f in ('probe.out', 'schema.out')}
v4 = ok(scan and not fhits and all(quoted.values()) and all(qout.values()))
out.append('**V4 — no evasion.** TZ-45\'s V6 flag pattern, over every line of this report outside a python '
           'block (prose, every table row including the Command cells, and every line of every command/output '
           'block), the command each probe row executed, every line of `probe.py` containing `curl`, and the '
           'commands this validation prints.\n\n```\nflag pattern: %s\n'
           'report lines scanned: %d (prose %d + non-python block lines %d); python block lines not scanned: %d\n'
           'probe result commands: %d\nprobe.py lines containing curl: %d\nvalidation commands: %d\n'
           'lines scanned in total: %d\nhits: %s\n'
           'quoted python block byte-identical to the file as run: probe.py %s, schema.py %s\n'
           'quoted output block identical to the saved output: probe.out %s, schema.out %s\n```\n\n'
           'No user-agent, header, proxy, cookie or retry flag anywhere. The `flag pattern:` line above is the '
           'pattern itself and matches itself; it is written after the scan → **%s**.'
           % (flag.pattern, len(prose) + len(nonpy), len(prose), len(nonpy), pyn, len(res), len(curl_lines),
              len(PRINTED), len(scan), fhits or 'none', quoted['probe.py'], quoted['schema.py'],
              qout['probe.out'], qout['schema.out'], v4))

# V5 -- no product fact
tab = [l for l in prose if l.startswith('|') and not SEP.match(l.strip())]
dsec, _ = split_md(between(t, '### The date field of each `primary-dated` row', '\n### '))
dlines = [l for l in dsec if l.startswith('- ')]
pats = collections.OrderedDict([
    ('ISO date', r'\b(19|20)\d{2}-\d{2}-\d{2}\b'),
    ('dd.mm.yyyy date', r'\b\d{1,2}\.\d{1,2}\.(19|20)\d{2}\b'),
    ('month name', r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d'),
    ('currency amount', r'[$€£]\s?\d|\d\s?(USD|USDT|BTC|ETH)\b'),
    ('numeric percent', r'\d+(\.\d+)?\s?%'),
    ('epoch-like number', r'\b\d{10,13}\b'),
    ('large figure', r'\b\d{1,3}([ ,]\d{3}){2,}\b'),
])
hits = [(k, m.group(0)) for k, p in pats.items() for l in tab + dlines for m in re.finditer(p, l)]
v5 = ok(tab and dlines and not hits)
out.append('**V5 — no product fact.** TZ-45\'s V5 patterns over every table row of this report (all four '
           'tables, header rows included, separator rows excluded) and every date-field line.\n\n```\n%s\n'
           'table rows scanned: %d\ndate-field lines scanned: %d\nlines scanned: %d\nhits: %s\n```\n\n'
           'Every cell is an id, a symbol, a class, a command, an HTTP status, a host, a content type, a record-list '
           'shape, a key name, a verdict, a count or a fingerprint; the date-field lines name fields and types only '
           '→ **%s**.'
           % ('\n'.join('%-18s %s' % (k, p) for k, p in pats.items()), len(tab), len(dlines),
              len(tab) + len(dlines), hits or 'none', v5))

# V6 -- nothing else written
_, st = sh('git status --porcelain')
_, df = sh('git diff --name-only HEAD')
v6 = ok(st == '?? ' + REL and df == '')
out.append('**V6 — nothing else written.**\n\n```\n$ git status --porcelain\n%s\n$ git diff --name-only HEAD\n%s\n```\n\n'
           'One untracked path, this report; no tracked file differs from `HEAD` → **%s**.'
           % (st, df or '(empty — no output)', v6))

# V7 -- scratch removed
if DRY:
    v7, block7 = 'NOT RUN (dry)', ''
else:
    rc_rm, o_rm = sh('rm -rf /tmp/tz46')
    rc_ls, o_ls = sh('ls -d /tmp/tz46*')
    v7 = ok(rc_rm == 0 and rc_ls != 0 and 'No such file' in o_ls)
    out.append('**V7 — scratch removed.**\n\n```\n$ rm -rf /tmp/tz46\n(exit %d)\n$ ls -d /tmp/tz46*\n%s\n(exit %d)\n```\n\n'
               'The glob matches nothing and `ls` fails with the error above → **%s**. This script had read itself '
               'before the removal, which is how it is quoted below.' % (rc_rm, o_ls, rc_ls, v7))

summary = ' · '.join('V%d %s' % (k + 1, v) for k, v in enumerate([v1, v2, v3, v4, v5, v6, v7]))
block = ('Result: **%s**.\n\n' % summary + '\n\n'.join(out) +
         '\n\n<details><summary><code>/tmp/tz46/validate.py</code>, verbatim</summary>\n\n```python\n' +
         SELF.rstrip('\n') + '\n```\n\n</details>')
if DRY:
    print(block)
else:
    open(REPORT, 'w').write(t.replace('@@VALIDATION@@', block))
print(summary)
```

</details>

---

## Test Results

No bench ran and no standing check applied. No production file, bench or workflow moved (V6),
and TZ-46 §0 requires no bench figure. The gate figures in the map's `## 0` block were not
re-measured. They are unchanged by construction, because no file they read appears in this
session's diff. The five bench files named in the map's `## 0` prose were fingerprinted
anyway, and all five match (`## Fingerprints`).

---

## Deviations

1. **ETH-c2a's redirect target was read from the saved header dump, not from the probe.**
   TZ §5 lists "the effective URL and its host" among the fields the probe prints. The
   instrument §5 mandates — TZ-45's `probe.py` with one change only — prints only the host,
   because `row()` keeps `urlparse(eff).netloc` and discards the rest. The probe was
   therefore left unchanged. Because the answering host matched the requested one, the
   redirect was invisible in its output. The `301` status and the `location` path were
   read offline with the `grep` quoted under the candidate table. No request was made, and
   the only value carried is the path.
2. **An offline schema reading was added for §6.2.** The probe prints date-key names but not
   their types, and §6.2 asks for "name and type". `schema.py` parses the two saved bodies
   and prints tag and key names, types and counts. It makes no request. **Its first version
   also printed how many ADA records had the `draft` and `prerelease` flags set to true.**
   That count is response content, so it is not carried here. The line was changed to print
   only whether each key is present as a boolean, and the script was re-run offline. The
   version quoted above is the one whose output is quoted. Both runs gave the same result
   for every other line.
3. **Four local reads were re-run with long-form options before this report quoted them.**
   All four first used the short options `-c` (count, for `grep` and `wc`) or `-a` (all
   branches, for `git branch`). TZ-45's V6 flag pattern matches a flag without regard to the
   tool it belongs to, so it would read these as curl's cookie-jar option (`-c`) and, because
   it ignores case, as the UA option (`-A`). None of the four makes a request. Each
   was re-run offline with a flag-free equivalent: `grep -o … | wc -l`,
   `stat --format=%s`, `git branch --all`. Every re-run printed the same output as the
   original, and only the re-runs are quoted. V4 therefore scans every line of this report
   and finds zero hits because no such flag remains, not because any line was left out of
   the scan. The pattern's blindness to tools is recorded as Remaining Risks 9.
4. **The validation script was corrected before its recorded run, and no correction changed a
   reading.** A dry run (`--dry` runs V1–V6 and neither removes nor writes anything) returned
   FAIL on V3 and V4, both because of parsing bugs in the script:
   - **V3:** the URL tokeniser treated the `\n` escape at the end of the two `printf`
     candidate lines as part of the URL, so two URLs appeared to fall outside §4's three.
   - **V4:** the comparison of the quoted `schema.py` output included the
     `$ python3 /tmp/tz46/schema.py` line above it.

   Fixes: the tokeniser now ends a URL at a backslash, and the output comparison drops
   `$ ` lines. V3's output label, which named a `cat` the script does not run, was also
   corrected. The next dry run returned V1–V6 PASS. The script quoted under `## Validation`
   is the corrected version. No pattern, threshold or expected value changed.
5. **The report commit carries the TZ's `## Commit Message` verbatim as its subject, followed
   by a `Co-Authored-By` trailer line.** This is the form of every report commit since
   TZ-43 (`git log -3 --format='%h %s%n%b' -- CryptoReports/`).

---

## Pre-existing Issues

None found. Contract v22 is 849 lines with MD5 `ba6ef34b108d70c287e02412dd84955e`, which is
what the map's `## 0` prose records, so the gap TZ-45 reported as its Pre-existing Issue 1 is
closed. The five bench figures in that prose also match (`## Fingerprints`).

---

## Remaining Risks

1. **`primary-dated` establishes a dated STREAM, not an upgrade date.** `pubDate` dates a blog
   post and `published_at` dates a release. The fork date, and on Cardano the on-chain
   governance action that triggers a hard fork, sit in content that TZ §8 forbids reading.
   Whether either stream carries upgrade dates in its content is unmeasured.
2. **Neither stream is upgrade-only.** The Ethereum Foundation feed returned 639 items in one
   response. That is the whole blog, not only upgrade announcements, and the feed has no
   filter parameter, so selecting upgrade posts would require reading titles or bodies. The
   `cardano-node` releases stream mixes versions, and its records carry `draft` and
   `prerelease` boolean keys (present on 5 of 5) that a consumer can filter on. Which release
   corresponds to a hard fork can be decided only from content.
3. **ETH-c2a lands on a different path from the one requested.** The request went to
   `/feed.xml`, and `curl -L` landed on `/en/feed.xml` on the same host. Methodology §6a's
   channel table has an `Answers from` column, and TZ-45's report recommended naming where a
   request lands rather than where it was sent. That column records hosts only, so this
   redirect would not appear in it. Whether §6a names the requested path or the landed path
   is the Architect's decision. The command recorded here is the form that was measured.
4. **The ETH feed is heavy.** 527621 bytes in one response, compared with 253618 for five
   releases. That is the cost of every coin-horizon refresh that reads it, and the feed has
   no page parameter to cap it.
5. **ADA-c2a adds a lane to the shared unauthenticated `api.github.com` quota.** TZ-45 counted
   11 coin lanes on that host (10 dated rows and HYPE). If §6a names ADA-c2a, a refresh of
   the coin horizon costs 12 of the 60 requests per hour allowed per client address. This
   session did not read the quota.
6. **ETH-c2b is unmeasured, not negative.** The stop rule withheld the request, so this report
   says nothing about the go-ethereum releases channel.
7. **Ownership was checked structurally, not against a registry.** TZ §4 names both candidates
   and their owners. Each response had the expected shape for its class: an RSS `channel` of
   `item`s, and a JSON array of release objects. This session added no evidence that
   `blog.ethereum.org` or the `IntersectMBO` organisation is the protocol's own channel beyond
   the TZ's naming.
8. **One reading at one moment**, 09:23:06Z to 09:23:17Z on 16.09.2026. A host that answered
   here may refuse on the next run, and vice versa (map inv. 52). The command in each row is
   what re-measures it.
9. **The no-evasion pattern matches flag letters without regard to the tool.** It matches
   short options such as `-c`, `-b`, `-x` and, because it ignores case, `-a` and `-h`,
   whatever command they belong to. Scanned over every command in a report, as TZ-46 V4
   asks, it flags ordinary local counting options, which is why Deviations 3 was needed.
   A pattern limited to `curl` invocations would test the same property without that
   noise. Whether the next TZ's version is limited that way is the Architect's decision.
   Re-scanning this committed report with the same pattern, outside its python blocks as V4
   does, would also match two lines inside `## Validation`. Both were written after the scan: the line that prints the
   pattern, and the V4 verdict sentence, which names one of the flags it rules out.

---

## Commit

Report commit, direct to `main` on the `CryptoReports/**` path (contract §8). Contents: this
file only.

```
docs(reports): TZ-46 — class-2 release channels probed for ETH and ADA (TZ-46)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

## CI Execution

**No workflow ran for this TZ.** No branch was pushed and no code path moved. The five
workflows' triggers, as read from the working tree in this session:

- `main.yml`: `push` to `main` with a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`, plus `workflow_dispatch`. This is the allow-list contract §8
  requires to be verified before a session's first direct push.
- `bench.yml`: `push` on `main` and `claude/**` with `'**.md'` in `paths-ignore`, plus
  `pull_request`.
- `calib.yml`: `workflow_dispatch`, plus `claude/**` pushes touching
  `bench/exhaustion_calib.py` or its own file.
- `journal.yml`: `schedule` and `workflow_dispatch` only.
- `backtest_bench.yml`: `workflow_dispatch` only.

A commit that changes one `.md` file under `CryptoReports/` matches none of these triggers.

## Final Repository State

The fingerprints were taken against harness worktree branch
`worktree-bridge-cse_011UxGXnrPSwgGra1vY7BBF6`, which has no upstream. It stood at
`e04eb3f8b07f935b5d505225233260002683567d`, the same commit as `origin/main` after the fetch.
At validation time its working tree differed from that commit only by this untracked report
(V6).

The probe scratch lived under `/tmp/tz46/`, outside the repository: response bodies, header
dumps, candidate and result files, the instrument, the TZ-45 copy it was cut from, and the
schema and validation scripts. It was removed during validation,
before this report was committed (V7). The four `@@…@@` blocks above were filled by copying
the files byte for byte, not by transcription. V4 checks each quoted block against its file:
the two scripts by MD5, and the two outputs as exact text. Every script is quoted verbatim, so each reading can be reproduced from this
report alone.

## Fingerprints

Measured on `e04eb3f`, the tree of `origin/main` after the fetch.

**Anchor gate (contract v22 §5 step 2).** The anchor list was cut from the map's own `## 0`
table. Each anchor's cell in the TZ header was compared character for character with the map's
cell. Each anchor string was then matched in the map with a fixed-string, case-sensitive
`grep -o`, which prints the matched text:

The gate script, verbatim as run from the repository root:

```bash
MAP=SYSTEM-MAP-CRYPTOCALCUL.md; TZ=CryptoTZ/TZ-46-eth-ada-release-channels.md
# anchor list from the map's own ## 0 anchor table (not from the TZ)
awk '/^## 0\. Fingerprint/{f=1} f&&/^## 1\./{exit} f' $MAP | awk -F'|' '/^\| (revision|direction engine|catalyst registry|exhaustion measure|analytical engine|squeeze block|newest invariant) \|/{print $2"\t"$3}' | sed 's/^ //; s/ \t /\t/; s/ $//' > /tmp/tz46-anchors.tsv
echo "anchors in map table: $(wc -l < /tmp/tz46-anchors.tsv)"
# TZ header = §0 section of the TZ
awk '/^## 0\. Fingerprint/{f=1} f&&/^## 1\./{exit} f' $TZ > /tmp/tz46-tzhdr.md
n=0; hdr=0; inmap=0
while IFS=$'\t' read -r name cell; do
  n=$((n+1)); s=$(printf '%s' "$cell" | sed 's/^`//; s/`$//')
  # TZ header row for the same anchor, compared cell for cell
  tzrow=$(grep -F "| $name |" /tmp/tz46-tzhdr.md | awk -F'|' '{print $3}' | sed 's/^ //; s/ $//')
  if [ "$tzrow" = "$cell" ]; then hdr=$((hdr+1)); h=identical; else h="DIFFERS: [$tzrow]"; fi
  echo "[$n] $name — TZ header cell: $h"
  echo "    \$ grep -F -o -- '$s' $MAP"
  out=$(grep -F -o -- "$s" $MAP | head -1); [ -n "$out" ] && inmap=$((inmap+1))
  echo "    returned: $out"
done < /tmp/tz46-anchors.tsv
echo "compared=$n header-identical=$hdr present-in-map=$inmap"
rm -f /tmp/tz46-anchors.tsv /tmp/tz46-tzhdr.md
```

Its output, verbatim:

```
anchors in map table: 7
[1] revision — TZ header cell: identical
    $ grep -F -o -- '**Revision 2026-09-16-a.**' SYSTEM-MAP-CRYPTOCALCUL.md
    returned: **Revision 2026-09-16-a.**
[2] direction engine — TZ header cell: identical
    $ grep -F -o -- '### 3.12 Direction engine — veto cascade' SYSTEM-MAP-CRYPTOCALCUL.md
    returned: ### 3.12 Direction engine — veto cascade
[3] catalyst registry — TZ header cell: identical
    $ grep -F -o -- '### 3.15 Catalyst registry' SYSTEM-MAP-CRYPTOCALCUL.md
    returned: ### 3.15 Catalyst registry
[4] exhaustion measure — TZ header cell: identical
    $ grep -F -o -- '### 3.16 List exhaustion — the day-range measure' SYSTEM-MAP-CRYPTOCALCUL.md
    returned: ### 3.16 List exhaustion — the day-range measure
[5] analytical engine — TZ header cell: identical
    $ grep -F -o -- '## 11. Analytical engine' SYSTEM-MAP-CRYPTOCALCUL.md
    returned: ## 11. Analytical engine
[6] squeeze block — TZ header cell: identical
    $ grep -F -o -- '### 3.17 «РИСК ВЫНОСА» — the day's own risk' SYSTEM-MAP-CRYPTOCALCUL.md
    returned: ### 3.17 «РИСК ВЫНОСА» — the day's own risk
[7] newest invariant — TZ header cell: identical
    $ grep -F -o -- '71. **A measurement that is not RETAINED was not taken,' SYSTEM-MAP-CRYPTOCALCUL.md
    returned: 71. **A measurement that is not RETAINED was not taken,
compared=7 header-identical=7 present-in-map=7
```

The gate's two temporary files were deleted by its last line. The map's revision string is **`2026-09-16-a`**, and TZ-46 §0 requires
**`2026-09-16-a`**.

The file table: TZ header rows compared with map rows by `diff` → identical (4 rows).

| File | Lines | MD5 | Required by | Match |
|---|---:|---|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 2734 | `aeedd62851712c997cd0f4c09c661055` | TZ-46 §0 revision | revision ✓, 7/7 anchors ✓; lines and MD5 reported, not enforced |
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | map §0 / TZ-46 §0 | ✓ |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | map §0 / TZ-46 §0 | ✓ |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | map §0 / TZ-46 §0 | ✓ |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | map §0 / TZ-46 §0 | ✓ |
| `bench/backtest_bench.py` | 5102 | `ba633202f43845ba0fdafbc1b92d9c04` | map §0 prose | ✓ |
| `bench/backtest_guard_bench.py` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` | map §0 prose | ✓ |
| `bench/verify_bench.py` | 540 | `28eb1949f21d0afadb062303108f7101` | map §0 prose | ✓ |
| `journal/write.js` | 849 | `19722fb53d75b6d25a8f957f74f97422` | map §0 prose | ✓ |
| `bench/journal_bench.js` | 1177 | `993271f44995c8ae21c54935a3f80adf` | map §0 prose | ✓ |
| `EXECUTOR-INSTRUCTIONS.md` | 849 | `ba6ef34b108d70c287e02412dd84955e` | map §0 prose: v22 | ✓ |
| `ANALYST-INSTRUCTIONS.md` | 2991 | `6d5030b9fa53852937992c7f642f129d` | — | reported |
| `CryptoTZ/TZ-46-eth-ada-release-channels.md` | 191 | `717e21913c540698cd53f1fa761a6db5` | — | reported |

Each row above was produced with `wc -l < <file>` and `md5sum < <file>`. The methodology's
header carries revision `2026-09-16-b`. `sed -n '/^## 6\./,/^## 7\./p' ANALYST-INSTRUCTIONS.md | md5sum`
→ `a121c493be25b8a7a25c505a600b1a95` is the checksum of the §6 and §6a text in force when these
two channels were measured. That text lists ETH and ADA as `2 owed`.
