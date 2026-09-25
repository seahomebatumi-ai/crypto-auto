# Implementation Report — TZ-52

## Status

**COMPLETED.** Report-only TZ. Stages A–F ran from this session's own machine on 25.09.2026,
from 11:09:07Z to 11:23:54Z. That was **245 requests, one per URL**, and E2's declared read is
the TZ's one named exception. The reads were strictly sequential, and the CoinGecko reads stood
12.50 s apart. **V1** passed 5 of 5, and its inverted run swapped a and b. **V2** matched both known
answers with no host changed. V3–V6 pass. Nothing here is admitted as a lane.

- **A** — `tokens[]` and `TOKENS` both hold 30 coins and their symmetric difference is empty. Five
  rows carry `fut:true`. The coverage record reads 11 `охвачена`, 14 `неохваченная` and
  5 `неизмерима`.
- **B** — All 30 of 30 coins were attempted: 54 candidate pages on 46 origins, and 95 lane
  readings (39 `dated`, 19 `undated`, 37 no channel or refused). **Screened against the recorded
  move, 8 coins have a dated lane that carried it**: SUI, LINK, AAVE, ADA, SOL, ETH, XLM and UNI.
  Two read `window short` (XRP, ZEC) and five `not carried` (FET, ENA, SKY, HBAR, ALGO). Ten
  have no dated lane, and five have `no move recorded`. Medium's platform-wide post sitemaps are
  excluded from this count, because 0 of their 42 693 URLs lie under any coin's publication
  path. Counted in, they would add 7 `carried` verdicts that no record of those coins supports.
- **C** — All four reporter feeds answered 200. Their union window runs from
  2026-09-23T10:43:46Z to 2026-09-25T11:11:33Z, 48.5 h. List yield is 14 titles. Book yield is
  15 titles: 4 name the crypto asset they matched, 2 name IBM the company, and 9 match only
  through word collisions.
- **D** — Upbit lists 855 markets, 289 of them `KRW-`. Of the `KRW-` bases, 23 are symbols of A2
  and 225 are bases of `x` rows. `warning` is true on 18 markets. The A2 symbols carrying a
  flag are GRAM, RENDER, ENA and LIT (`GLOBAL_PRICE_DIFFERENCES`) and MORPHO
  (`TRADING_VOLUME_SOARING`).
- **E** — The Federal Register answered 200 with `count` 10000. Its 20 newest SEC documents span
  24–25.09: 2 `Longer Period`, 1 `Proceedings`, and 0 crypto terms as whole words. SEC full-text
  search refused the rule-1 form with **403, «Your Request Originates from an Undeclared
  Automated Tool»**. The declared form answered **200 JSON with `hits.total.value` 1215**. This
  reproduces the Architect's reading of 25.09 from this machine.
- **F** — `fapi.binance.com` answered 200 for all five declared perpetuals: 3 rows of 12 fields
  each. The last row opens at 2026-09-25T11:00:00Z, the hour in which the reads were made.

The previous TZ, TZ-51, is merged: PR #42 at merge commit `e8b8681`, implementation `065ba72`.

---

## Inbound Filing

`CryptoTZ/TZ-52-catalyst-lanes-vps-measurement.md` arrived under its canonical name in the Boss's
upload commit `1d0cda9`. That is the only commit touching a `*TZ-52*` path on any ref:

```
$ git log --all --format='%h' --name-only -- '*TZ-52*' '*TZ 52*' '*TZ_52*' | sort --unique

1d0cda9
CryptoTZ/TZ-52-catalyst-lanes-vps-measurement.md
```

(The empty first line is `--name-only`'s separator, sorted first.)

Nothing was moved or renamed. No second copy exists in the root or on any branch, and no
earlier revision of the file was deleted and re-uploaded.

---

## Scope Executed

**Class: report-only TZ** (contract §8). The TZ's `## Scope` names exactly one written file,
this report, on the `CryptoReports/**` direct-push path. Files to Modify and Files to Delete
are both `none`.

Run order under contract §4a:

1. Contract v23 was read in full: 864 lines, MD5 `02abb1969626d2af150a0d1f6e02f2a7`.
2. `git fetch --all --prune` exited 0, and `git rev-parse --is-shallow-repository` printed
   `false`. `git rev-parse HEAD origin/main` printed `1d0cda91f1fd6717c72fb51b6e98a52a7b042b04`
   twice, and `git status --porcelain` printed nothing, so no merge was needed.
3. The TZ was found in `CryptoTZ/` on `origin/main` and read in full.
4. The fingerprint gate (contract v23 §5) passed. The anchor list was cut from the map's own
   table by its structure. **The table carries 7 rows and 7 were compared. All 7 appear
   character for character in the TZ header, and all 7 are exact substrings of the map.** The
   text each match returned is under `## Fingerprints`.
5. The six blockquotes under the TZ's «Contract text this TZ obeys» were checked against their
   sources, whitespace-normalised because the sources wrap lines. **All 6 are verbatim**, each
   inside the section it names: contract §7 item 9 at `EXECUTOR-INSTRUCTIONS.md:518`, map
   inv. 44 at `SYSTEM-MAP-CRYPTOCALCUL.md:1983`, methodology §6a at
   `ANALYST-INSTRUCTIONS.md:2322`, `:2351` and `:2525`, and methodology §11 at `:3286`.
6. Repository state was read with `git log --oneline --graph --all`. TZ-51 is merged (PR #42,
   merge commit `e8b8681` over `065ba72`), and no `*tz-51*` or `*tz-52*` branch remains.
   `main.yml` is still a `paths` allow-list of exactly `main.py` and `.github/workflows/main.yml`,
   read before the first push as contract §8 requires. Two `analyst:` commits, `8ced0e3` and
   `369cc03`, sit on other harness worktree branches and not on `main`. They are not this TZ's
   and are recorded only as state.
7. Stages A–F ran, then V1–V6.

**Not done, because the scope forbids it:** nothing was written under `analyst/`, to
`catalysts.json`, or to any production, bench, workflow or contract file. No lane is admitted.
No date, figure or event read here entered any file except this report, where each appears as
evidence about a channel and never as a catalyst. **The only requests made** are the 243 of
Stages B–F plus V2's two, listed in full under `### Reading ledger`. No request was retried.
No user-agent, header, proxy or cookie was set, except E2 (b)'s single `-A`. The only other
network traffic was `git fetch` to the repository's own remote.

---

## Files Created

- `CryptoReports/TZ-52-catalyst-lanes-vps-measurement-report.md` — this report.

## Files Modified

None.

## Files Renamed

None.

## Files Deleted

None.

---

## Implementation Summary

### Client and environment (A4, rule 1)

```
$ curl --version | head --lines=1
curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10
$ git config --get user.email >/dev/null && echo "address returned: yes"
address returned: yes
$ env | grep --ignore-case --extended-regexp '^(https?_proxy|no_proxy|all_proxy)=' | wc --lines
0
$ ls ~/.curlrc /etc/curlrc
ls: cannot access '/root/.curlrc': No such file or directory
ls: cannot access '/etc/curlrc': No such file or directory
```

The session is a managed cloud container: Ubuntu 24.04.4 LTS, kernel 6.8.0-136-generic, Python
3.12.3. No proxy variable and no curl configuration file exist, so every read below is curl's
own default client. The address `git config` returns is printed only masked, as
`d***@yahoo.com`. It is used in exactly one request, E2 (b), and appears in no file this
session wrote (V4).

### Instrument

The probe lives in `/tmp/tz52/`, outside the repository:

- `probe.py` (394 lines, MD5 `cbd35dbfd212f541cef232f415574772`) holds the fetch layer, robots.txt under RFC 9309, the parsers,
  and B6/B7 as functions.
- `stages.py` (633 lines, MD5 `ec763f91999cc2b42d65dc506bcfa053`) runs one command per stage.
- `selftest.py` (180 lines, MD5 `9d35e6b40c5f9f42356dd295ca3b3fa1`) is an offline test of every parser and of the fetch layer
  against a localhost server, with its own ledger.
- `report.py` (243 lines, MD5 `5c3dfba63fc4632a9446312bce5983c8`) builds every table in this report from the saved results. It
  makes no request.
- `replay.py` (40 lines, MD5 `62118dd7b4babd9126e3710585764b30`) re-runs every stage with the final text of `probe.py` and
  `stages.py`. It replaces `fetch()` with a ledger lookup that aborts on any URL not already
  read.

**How it reads.** `fetch()` runs the rule-1 form as an argv list, so no shell parses a URL taken
from a page. It records the shell-equivalent command, and it appends each read to an
append-only ledger before returning. A `(url, form)` pair already in the ledger is returned from
the ledger and never requested again. One process lock covers every network stage, so reads
cannot run in parallel. CoinGecko reads wait 12.5 s from the end of the previous CoinGecko read.
A 1 s courtesy gap separates consecutive reads to one host. Every body and header dump is kept,
and each stage writes its result to `out/<stage>.json`. So every classification below can be,
and in three cases was, recomputed from saved bodies with no request.

**Robots.txt (rule 4) follows RFC 9309, in the TZ's silence on the details.** A file binds one
scheme, host and port, so the cache key is the origin. The group is chosen by product token
`curl`, falling back to `*`, and no file here carried a `curl` group. The longest matching
pattern wins and `Allow` wins a tie. A 4xx robots.txt is «unavailable» and imposes no
restriction; a 5xx or unreachable one would impose a complete disallow, and none occurred.
When a robots.txt redirects, its rules bind the requesting origin (RFC 9309 §2.3.1.2). Where it
landed on another origin's `/robots.txt`, that file is reused for the landing origin. This saved
one request (`forum.algorand.co`).

**Defects found and fixed before the numbers below were taken.** Both are recorded because the
instrument is part of the evidence.

1. The self-test's first run found robots.txt keyed by bare host, which dropped scheme and port.
   The localhost fixture's robots file read as unreachable, and the whole origin became
   disallowed. It was fixed before any external request. The self-test now passes 63 of 63
   (last block of `## Validation`).
2. The placeholder quote took a comment's first twenty words. In NEAR's comment the words that
   state the placeholders come later, after a sentence naming a person. The quote now takes the
   sentence that says «placeholder», at most twenty words of it. It was re-derived from the
   saved body (`r157`) by `b-classify` with no request.

The Upbit reading was also extended offline, to list every `caution` key and Upbit's own name
for each A2 symbol, again with no request (`d-offline` made 0 reads).

**The two sources below are the final text, and the final text reproduces every result.** The
network stages ran under the same fetch layer. The edits made after reads had begun are
analysis applied to saved bodies: defect 2, B7's in-window count, V2's stage and the Upbit
extension. `replay.py` re-ran all stages on the final text with any new request made fatal.
The ledger did not grow, and all 13 result files the tables are built from came back
byte-identical:

```
A4 git config --get user.email returns an address: yes
ledger unchanged: True (245 lines)
a.json     identical  68869f033e130cca6f956e84aac19921
b1.json    identical  c7c85a5c9a6bd05b32d1941e7827aec5
b2.json    identical  c4d0ec0f95bdd9445fc332029c29e963
b3.json    identical  8e578842c55c49255293f32fe4adfd75
b4.json    identical  639f183fe397884711e5d5da3ba1c8b0
b5.json    identical  000da67e17f8caca2b7434257c67681b
b6.json    identical  b7ae1cfe7dd4afd7c354272be9bdddaf
c.json     identical  67aabc58cdbed5acaec6314559d199f0
d.json     identical  425c5437dd580242a20bb98a138db181
e1.json    identical  e09a9b7c2acb9d3a46bc529b7c7db6b3
e2.json    identical  2669c21f7ecbc0ebd80bc5f4ab72f4cd
f.json     identical  9b8c39b116b29929966f41a21c6118dd
v2.json    identical  3df42e6d9faf6bdd3a64ce62f8bea220
result files compared 13, identical 13, differing 0
```

<details><summary><code>/tmp/tz52/probe.py</code>, verbatim, final text</summary>

```python
#!/usr/bin/env python3
# TZ-52 probe. One curl per URL in the TZ's rule-1 form, sequential, no retry, no
# second client (E2 (b) is the TZ's single named exception). Every body and header
# dump is kept under /tmp/tz52 so any parser fix is re-applied offline, never by
# re-fetching.
import sys, os, re, json, time, gzip, html, fcntl, subprocess, datetime as dt
from urllib.parse import urlparse, urljoin
from email.utils import parsedate_to_datetime

ROOT = '/tmp/tz52'
REPO = '/root/crypto-auto/.claude/worktrees/bridge-cse_01T87syUKWGCQYE7sWfMqMHT'
BODY, HDR, OUT = ROOT + '/body', ROOT + '/hdr', ROOT + '/out'
LEDGER = ROOT + '/ledger.jsonl'
W = '%{http_code} %{size_download} %{content_type} %{url_effective}\\n'  # backslash-n, as typed
KEYWORDS = ('blog', 'news', 'post', 'press', 'announce', 'update', 'insight')
CG_GAP = 12.5
SAME_HOST_GAP = 1.0

# ---------------------------------------------------------------- fetch layer

def utcnow():
    return dt.datetime.now(dt.timezone.utc)

def iso(t):
    return t.strftime('%Y-%m-%dT%H:%M:%SZ')

def ledger():
    if not os.path.exists(LEDGER):
        return []
    return [json.loads(l) for l in open(LEDGER, encoding='utf-8') if l.strip()]

def qurl(u):
    return "'" + u + "'" if "'" not in u else "'" + u.replace("'", "'\\''") + "'"

def hop_statuses(hp):
    try:
        return [l.split()[1] for l in open(hp, errors='replace') if l.startswith('HTTP/') and len(l.split()) > 1]
    except OSError:
        return []

def fetch(url, stage, purpose, form='rule1', extra=None, extra_display=None):
    """One request per (url, form), ever. Returns the ledger record; a URL already
    read is returned from the ledger with reused=True and no request is made."""
    led = ledger()
    for r in led:
        if r['url'] == url and r['form'] == form:
            r = dict(r); r['reused'] = True
            return r
    host = urlparse(url).hostname or ''
    # pacing: sequential by construction (one process, lock held); CoinGecko >= 12 s apart
    if host == 'api.coingecko.com':
        prev = [r for r in led if urlparse(r['url']).hostname == 'api.coingecko.com']
        if prev:
            wait = CG_GAP - (time.time() - prev[-1]['t_end'])
            if wait > 0:
                time.sleep(wait)
    samehost = [r for r in led if urlparse(r['url']).hostname == host]
    if samehost:
        wait = SAME_HOST_GAP - (time.time() - samehost[-1]['t_end'])
        if wait > 0:
            time.sleep(wait)
    rid = 'r%03d' % (len(led) + 1)
    bp, hp = BODY + '/' + rid, HDR + '/' + rid
    argv = ['curl', '-sS', '-L', '-m', '20', '-o', bp, '-D', hp, '-w', W] + (extra or []) + [url]
    disp = "curl -sS -L -m 20 -o %s -D %s -w '%s' %s%s" % (bp, hp, W, (extra_display + ' ') if extra_display else '', qurl(url))
    t0 = time.time(); ts = iso(utcnow())
    p = subprocess.run(argv, capture_output=True, text=True)
    t1 = time.time()
    line = p.stdout.rstrip('\n').split('\n')[-1] if p.stdout else ''
    code, size, rest = (line.split(' ', 2) + ['', '', ''])[:3]
    ctype, landing = (rest.rsplit(' ', 1) + [''])[:2] if ' ' in rest else ('', rest)
    rec = dict(id=rid, stage=stage, purpose=purpose, form=form, url=url, cmd=disp, ts=ts,
               t_end=t1, secs=round(t1 - t0, 2), exit=p.returncode, code=code, bytes=size,
               ctype=ctype.strip(), landing=landing.strip(), stderr=p.stderr.strip()[:300],
               hops=hop_statuses(hp), reused=False)
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec, ensure_ascii=False) + '\n')
    print('READ %s [%s] %s -> %s %s %s %s (exit %d%s) %.1fs' % (
        rid, stage, disp, code, size, ctype.strip() or '-', landing.strip(), p.returncode,
        (', ' + p.stderr.strip()[:120]) if p.stderr.strip() else '', t1 - t0), flush=True)
    return rec

def body_of(rec):
    """Body bytes, gunzipped locally when the payload is gzip (rule 1)."""
    try:
        b = open(BODY + '/' + rec['id'], 'rb').read()
    except OSError:
        return b''
    if b[:2] == b'\x1f\x8b':
        try:
            b = gzip.decompress(b)
        except Exception:
            pass
    return b

def headers_of(rec):
    try:
        return open(HDR + '/' + rec['id'], errors='replace').read()
    except OSError:
        return ''

def challenge(rec):
    h = headers_of(rec).lower()
    low = body_of(rec)[:30000].decode('utf-8', 'replace').lower()
    return ('cf-mitigated: challenge' in h or 'challenge-platform' in low
            or '<title>just a moment' in low or 'attention required! | cloudflare' in low
            or '_incapsula_resource' in low or 'captcha-delivery' in low)

def outcome(rec):
    """Reading class of one request, before any parsing."""
    c = rec['code']
    if c in ('000', ''):
        return 'unreachable (curl exit %d)' % rec['exit']
    if challenge(rec):
        return 'refused (challenge, HTTP %s)' % c
    if c in ('401', '403', '407', '429', '451'):
        return 'refused (HTTP %s)' % c
    if c in ('404', '410'):
        return 'absent (HTTP %s)' % c
    if not c.startswith('2'):
        return 'error (HTTP %s)' % c
    return 'ok'

# ---------------------------------------------------------------- robots (RFC 9309)

def robots_parse(text):
    groups, cur, in_rules, sitemaps = [], None, False, []
    for raw in text.replace('\r', '\n').split('\n'):
        line = raw.split('#', 1)[0].strip()
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k, v = k.strip().lower(), v.strip()
        if k == 'sitemap':
            if v:
                sitemaps.append(v)
            continue
        if k in ('user-agent', 'useragent'):
            if cur is None or in_rules:
                cur = {'agents': [], 'rules': []}
                groups.append(cur)
                in_rules = False
            cur['agents'].append(v)
        elif k in ('allow', 'disallow') and cur is not None:
            cur['rules'].append((k, v, raw.strip()))
            in_rules = True
    return groups, sitemaps

def robots_group(groups, token='curl'):
    mine = [g for g in groups if any(a.lower().split('/')[0].strip() == token for a in g['agents'])]
    if mine:
        return token, [r for g in mine for r in g['rules']]
    star = [g for g in groups if any(a.strip() == '*' for a in g['agents'])]
    if star:
        return '*', [r for g in star for r in g['rules']]
    return None, []

def rule_match(pattern, path):
    if not pattern:
        return False
    anchored = pattern.endswith('$')
    body = pattern[:-1] if anchored else pattern
    rx = ''.join('.*' if ch == '*' else re.escape(ch) for ch in body)
    return re.match(rx + ('$' if anchored else ''), path) is not None

def robots_decide(rules, path):
    """Longest match wins, allow wins a tie; /robots.txt is always allowed."""
    if path == '/robots.txt':
        return True, []
    hits = [(k, v, raw) for (k, v, raw) in rules if rule_match(v, path)]
    if not hits:
        return True, []
    best = max(hits, key=lambda h: (len(h[1]), h[0] == 'allow'))
    return best[0] == 'allow', [h[2] for h in hits]

ROBOTS = {}   # origin (scheme://host[:port]) -> dict(rec_id, status, group, rules, sitemaps, basis)

def origin_of(url):
    u = urlparse(url)
    return '%s://%s' % (u.scheme.lower(), (u.netloc or '').lower())

def robots_for(host, stage):
    """host is an origin, scheme://host[:port]: robots.txt binds one protocol, host and port (RFC 9309 2.3)."""
    if host in ROBOTS:
        return ROBOTS[host]
    url = '%s/robots.txt' % host
    rec = fetch(url, stage, 'robots.txt of %s' % host)
    oc = outcome(rec)
    ent = dict(host=host, rec=rec['id'], code=rec['code'], landing=rec['landing'], outcome=oc,
               group=None, rules=[], sitemaps=[], basis='')
    if oc == 'ok':
        groups, sm = robots_parse(body_of(rec).decode('utf-8', 'replace'))
        g, rules = robots_group(groups)
        ent.update(group=g, rules=rules, sitemaps=sm,
                   basis='parsed: %d group(s), governing group %s, %d rule line(s)' % (len(groups), g or 'none', len(rules)))
    elif oc.startswith('absent') or oc.startswith('refused'):
        ent['basis'] = 'RFC 9309 2.3.1.3: robots.txt %s -> no restriction' % oc
    else:
        ent['basis'] = 'RFC 9309 2.3.1.4: robots.txt %s -> complete disallow' % oc
        ent['rules'] = [('disallow', '/', '(robots.txt unreachable: complete disallow)')]
    ROBOTS[host] = ent
    lh = origin_of(rec['landing']) if rec['landing'] else None
    if lh and lh != host and urlparse(rec['landing']).path == '/robots.txt' and lh not in ROBOTS and oc == 'ok':
        ROBOTS[lh] = dict(ent, host=lh, basis=ent['basis'] + ' (landing of %s)' % url)
    return ROBOTS[host]

def permitted(url, stage):
    u = urlparse(url)
    ent = robots_for(origin_of(url), stage)
    path = (u.path or '/') + (('?' + u.query) if u.query else '')
    ok, lines = robots_decide(ent['rules'], path)
    return ok, dict(host=origin_of(url), robots=ent['rec'], group=ent['group'], path=path,
                    matched=lines, decision='allow' if ok else 'disallow')

def guarded(url, stage, purpose):
    """Rule 4: robots.txt first; a disallowed path is not requested."""
    ok, perm = permitted(url, stage)
    if not ok:
        print('SKIP [%s] %s -> refused on permission %s' % (stage, url, perm['matched']), flush=True)
        return None, perm
    return fetch(url, stage, purpose), perm

# ---------------------------------------------------------------- dates

def parse_date(s):
    s = html.unescape((s or '').strip())
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)
        if d is not None:
            return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
    except Exception:
        pass
    t = s.replace('Z', '+00:00')
    t = re.sub(r'\.(\d{1,6})\d*', lambda m: '.' + m.group(1), t)
    try:
        d = dt.datetime.fromisoformat(t)
        return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)
    except Exception:
        pass
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        try:
            return dt.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), tzinfo=dt.timezone.utc)
        except ValueError:
            return None
    return None

def uday(d):
    return d.astimezone(dt.timezone.utc).date()

# ---------------------------------------------------------------- parsers

def text_of(frag):
    frag = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', frag, flags=re.S)
    frag = re.sub(r'<[^>]+>', '', frag)
    return re.sub(r'\s+', ' ', html.unescape(frag)).strip()

ATTR = re.compile(r'([A-Za-z_:][\w:.-]*)\s*=\s*("([^"]*)"|\'([^\']*)\'|([^\s"\'>]+))')

def feed_links(page_html, base):
    b = re.search(r'<base\b[^>]*\bhref\s*=\s*["\']([^"\']+)', page_html, re.I)
    if b:
        base = urljoin(base, html.unescape(b.group(1)))
    out = []
    for tag in re.findall(r'<link\b[^>]*>', page_html, flags=re.I):
        a = {m.group(1).lower(): (m.group(3) if m.group(3) is not None else (m.group(4) if m.group(4) is not None else m.group(5)))
             for m in ATTR.finditer(tag)}
        rel = (a.get('rel') or '').lower().split()
        typ = (a.get('type') or '').strip().lower()
        if 'alternate' in rel and typ in ('application/rss+xml', 'application/atom+xml') and a.get('href'):
            u = urljoin(base, html.unescape(a['href'].strip()))
            if u not in [x[0] for x in out]:
                out.append((u, typ))
    return out

def parse_feed(b):
    t = b.decode('utf-8', 'replace')
    head = t[:4000].lower()
    if not re.search(r'<(rss|feed|rdf:rdf)[\s>]', head):
        return None
    items = re.findall(r'<item\b[^>]*>(.*?)</item>', t, flags=re.S | re.I) + \
            re.findall(r'<entry\b[^>]*>(.*?)</entry>', t, flags=re.S | re.I)
    recs = []
    for it in items:
        d, raw = None, None
        for tag in ('pubDate', 'published', 'updated'):
            m = re.search(r'<%s\b[^>]*>(.*?)</%s>' % (tag, tag), it, flags=re.S)
            if m:
                raw = text_of(m.group(1)); d = parse_date(raw)
                break
        tm = re.search(r'<title\b[^>]*>(.*?)</title>', it, flags=re.S)
        recs.append(dict(date=d, raw=raw, title=text_of(tm.group(1)) if tm else ''))
    return recs

def parse_sitemap(b):
    t = b.decode('utf-8', 'replace')
    comments = [re.sub(r'\s+', ' ', c).strip() for c in re.findall(r'<!--(.*?)-->', t, flags=re.S)]
    low = t[:20000].lower()
    if '<sitemapindex' in low:
        kind, blocks = 'index', re.findall(r'<sitemap\b[^>]*>(.*?)</sitemap>', t, flags=re.S | re.I)
    elif '<urlset' in low:
        kind, blocks = 'urlset', re.findall(r'<url(?:\s[^>]*)?>(.*?)</url>', t, flags=re.S | re.I)
    else:
        return dict(kind='not a sitemap', entries=[], comments=comments)
    ents = []
    for blk in blocks:
        loc = re.search(r'<loc\b[^>]*>(.*?)</loc>', blk, flags=re.S | re.I)
        lm = re.search(r'<lastmod\b[^>]*>(.*?)</lastmod>', blk, flags=re.S | re.I)
        raw = text_of(lm.group(1)) if lm else None
        ents.append(dict(loc=text_of(loc.group(1)) if loc else '', raw=raw, date=parse_date(raw) if raw else None))
    return dict(kind=kind, entries=ents, comments=comments)

def kw_path(u):
    p = urlparse(u).path.lower()
    return any(k in p for k in KEYWORDS)

def placeholder_quotes(comments):
    """The sentence of a comment that states placeholders, at most twenty words of it."""
    out = []
    for c in comments:
        for sent in re.split(r'(?<=[.!?])\s+', c):
            if 'placeholder' in sent.lower():
                w = sent.split()
                out.append(' '.join(w[:20]) + (' …' if len(w) > 20 else ''))
    return out

# ---------------------------------------------------------------- B6 / B7

def classify(dates, invert=False):
    """B6: dated iff at least one record carries a date and the dates take at least
    two distinct calendar days; invert=True flips that comparison (negative control)."""
    days = {uday(d) for d in dates if d is not None}
    if not days:
        return 'undated', 0
    two = len(days) >= 2
    if invert:
        two = not two
    return ('dated' if two else 'undated'), len(days)

def screen(dates, move_day):
    """B7, for a dated lane: carried / window short / not carried."""
    days = sorted({uday(d) for d in dates if d is not None})
    win = {move_day - dt.timedelta(days=k) for k in (0, 1, 2)}
    if any(x in win for x in days):
        return 'carried'
    if days and days[0] > move_day - dt.timedelta(days=2):
        return 'window short'
    return 'not carried'

MOVE_DATE = re.compile(r'(\d{4}-\d{2}-\d{2})')

def move_day_of(move):
    if not isinstance(move, str):
        return None
    m = MOVE_DATE.search(move)
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None

HOST = re.compile(r'^[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$')

def carried_by_host(cb):
    if not isinstance(cb, str) or not cb.strip():
        return None
    tok = cb.strip().split()[0].split('/')[0].lower()
    return tok if HOST.match(tok) else None

def norm_url(u):
    p = urlparse(u.strip())
    path = p.path or '/'
    return '%s://%s%s%s' % (p.scheme.lower(), (p.netloc or '').lower(), path, ('?' + p.query) if p.query else '')

# ---------------------------------------------------------------- io helpers

def save(name, obj):
    with open(OUT + '/' + name, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, default=str)

def load(name):
    return json.load(open(OUT + '/' + name, encoding='utf-8'))

def lock():
    fd = open(ROOT + '/.lock', 'w')
    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    return fd

if __name__ == '__main__':
    import stages
    stages.main(sys.argv[1:])
```

</details>

<details><summary><code>/tmp/tz52/stages.py</code>, verbatim, final text</summary>

```python
#!/usr/bin/env python3
# TZ-52 stages. Each stage saves its result under /tmp/tz52/out and can be re-run:
# a URL already in the ledger is never requested again.
import sys, os, re, json, ast, subprocess, datetime as dt
from urllib.parse import urlparse
import probe as P

TZ_ORDER = None

# ---------------------------------------------------------------- Stage A

def stage_a():
    src = open(P.REPO + '/index.html', encoding='utf-8').read()
    blk = src[src.index('var tokens = ['):]
    blk = blk[:blk.index('];') + 2]
    rows = re.findall(r"\{name:'([A-Z0-9]+)',\s*s:'([A-Z0-9]+)'(\s*,\s*fut:true)?\}", blk)
    n_name = len(re.findall(r'\bname:', blk))
    toks = [dict(sym=a, pair=b, fut=bool(c)) for a, b, c in rows]
    tree = ast.parse(open(P.REPO + '/main.py', encoding='utf-8').read())
    TOK = None
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'TOKENS' for t in node.targets):
            TOK = ast.literal_eval(node.value)
    s1, s2 = {t['sym'] for t in toks}, set(TOK)
    print('A2 tokens[] rows parsed: %d (name: occurrences in the literal: %d)' % (len(toks), n_name))
    print('A2 tokens[] fut:true: %d -> %s' % (sum(t['fut'] for t in toks), ' '.join(t['pair'] for t in toks if t['fut'])))
    print('A2 TOKENS entries: %d' % len(TOK))
    print('A2 symmetric difference: %s' % (sorted(s1 ^ s2) or 'empty'))
    st = json.load(open(P.REPO + '/analyst/state.json', encoding='utf-8'))
    coins = st.get('sweeps', {}).get('coins', {})
    cov, per = {}, {}
    for t in toks:
        c = coins.get(t['sym'], {}).get('coverage')
        cov[t['sym']] = c if c is not None else 'absent'
        k = c.get('status') if isinstance(c, dict) else 'absent'
        per[k] = per.get(k, 0) + 1
    print('A3 state.json v=%s d=%s ts=%s; sweeps.coins entries: %d' % (st.get('v'), st.get('d'), st.get('ts'), len(coins)))
    for t in toks:
        print('A3 %-7s %s' % (t['sym'], json.dumps(cov[t['sym']], ensure_ascii=False)))
    print('A3 per status: %s' % json.dumps(per, ensure_ascii=False))
    cv = subprocess.run(['curl', '--version'], capture_output=True, text=True).stdout.split('\n')[0]
    em = subprocess.run(['git', '-C', P.REPO, 'config', '--get', 'user.email'], capture_output=True, text=True)
    has = em.returncode == 0 and '@' in em.stdout.strip()
    print('A4 curl --version (first line): %s' % cv)
    print('A4 git config --get user.email returns an address: %s' % ('yes' if has else 'no'))
    P.save('a.json', dict(tokens=toks, TOKENS=TOK, symdiff=sorted(s1 ^ s2), n_name=n_name,
                          coverage=cov, per_status=per, state_d=st.get('d'), state_ts=st.get('ts'),
                          curl=cv, has_email=has))

# ---------------------------------------------------------------- Stage B1

CG = ('https://api.coingecko.com/api/v3/coins/%s?localization=false&tickers=false'
      '&market_data=false&community_data=false&developer_data=false&sparkline=false')

def stage_b1():
    a = P.load('a.json')
    res = {}
    for t in a['tokens']:
        sym = t['sym']; cid = a['TOKENS'].get(sym)
        if not cid:
            res[sym] = dict(cid=None, served=False, why='no CoinGecko id in TOKENS'); continue
        rec = P.fetch(CG % cid, 'B1', 'CoinGecko coin %s' % cid)
        oc = P.outcome(rec)
        ent = dict(cid=cid, rec=rec['id'], outcome=oc, served=False)
        if oc == 'ok':
            try:
                j = json.loads(P.body_of(rec))
                links = j.get('links') or {}
                hp = [h.strip() for h in (links.get('homepage') or []) if isinstance(h, str) and h.strip()]
                an = [h.strip() for h in (links.get('announcement_url') or []) if isinstance(h, str) and h.strip()]
                ent.update(name=j.get('name'), homepage=hp[0] if hp else None, announcement=an, served=True)
            except Exception as e:
                ent.update(outcome='ok but not parseable: %s' % e)
        print('B1 %-7s %s' % (sym, json.dumps({k: ent.get(k) for k in ('cid', 'outcome', 'name', 'homepage', 'announcement')}, ensure_ascii=False)), flush=True)
        res[sym] = ent
    P.save('b1.json', res)
    print('B1 attempted %d of A2 %d; answered %d' % (sum(1 for v in res.values() if v.get('rec')), len(a['tokens']),
                                                   sum(1 for v in res.values() if v.get('served'))))

# ---------------------------------------------------------------- Stage B2..B5 (reads)

def candidates():
    a, b1 = P.load('a.json'), P.load('b1.json')
    out = {}
    for t in a['tokens']:
        sym = t['sym']; e = b1[sym]
        cands = []
        if e.get('served'):
            if e.get('homepage'):
                cands.append(('homepage', e['homepage']))
            for u in e.get('announcement') or []:
                cands.append(('announcement', u))
        cov = a['coverage'].get(sym)
        cb = cov.get('carried_by') if isinstance(cov, dict) else None
        h = P.carried_by_host(cb)
        if h:
            cands.append(('carried_by root', 'https://%s/' % h))
        seen, dd = set(), []
        for kind, u in cands:
            n = P.norm_url(u)
            if n in seen:
                continue
            seen.add(n); dd.append(dict(kind=kind, raw=u, url=n))
        out[sym] = dict(served=e.get('served'), cands=dd, cb_host=h, cb_raw=cb)
    return out

def stage_b_reads(phase):
    a = P.load('a.json')
    cand = candidates()
    P.save('b2.json', cand)
    hosts = []
    for sym in [t['sym'] for t in a['tokens']]:
        for c in cand[sym]['cands']:
            h = P.origin_of(c['url'])
            if h not in hosts:
                hosts.append(h)
    if phase == 'robots':                                   # B3
        for h in hosts:
            P.robots_for(h, 'B3')
        P.save('b3.json', {h: P.ROBOTS[h] for h in P.ROBOTS})
        print('B3 candidate hosts %d; robots.txt read for %d hosts (incl. landing aliases %d)' % (
            len(hosts), len(hosts), len(P.ROBOTS) - len(hosts)))
        return
    for h in hosts:                                         # re-derive robots from the ledger, no request
        P.robots_for(h, 'B3')
    if phase == 'pages':                                    # B4
        pages, feeds, budget = {}, {}, {}
        for sym in [t['sym'] for t in a['tokens']]:
            for c in cand[sym]['cands']:
                u = c['url']
                if u in pages:
                    continue
                rec, perm = P.guarded(u, 'B4', 'candidate page (%s of %s)' % (c['kind'], sym))
                ent = dict(url=u, perm=perm, rec=rec['id'] if rec else None,
                           outcome=P.outcome(rec) if rec else 'refused on permission',
                           landing=rec['landing'] if rec else None, feeds=[], self_feed=False)
                if rec and ent['outcome'] == 'ok':
                    body = P.body_of(rec)
                    if P.parse_feed(body) is not None:
                        ent['self_feed'] = True
                    links = P.feed_links(body.decode('utf-8', 'replace'), rec['landing'] or u)
                    ent['feeds'] = [dict(url=x, type=t) for x, t in links]
                pages[u] = ent
                host = P.origin_of(u)
                for fl in ent['feeds']:
                    if fl['url'] in feeds:
                        fl['read'] = 'already read'; continue
                    if budget.get(host, 0) >= 2:
                        fl['read'] = 'not read (two per host)'; continue
                    budget[host] = budget.get(host, 0) + 1
                    frec, fperm = P.guarded(fl['url'], 'B4', 'advertised feed on %s' % host)
                    fl['read'] = 'read' if frec else 'refused on permission'
                    feeds[fl['url']] = dict(url=fl['url'], host=host, perm=fperm, rec=frec['id'] if frec else None)
        P.save('b4.json', dict(pages=pages, feeds=feeds, budget=budget))
        P.save('b3.json', {h: P.ROBOTS[h] for h in P.ROBOTS})
        print('B4 candidate pages %d (requested %d, refused on permission %d); advertised feeds %d; feeds requested %d' % (
            len(pages), sum(1 for p in pages.values() if p['rec']), sum(1 for p in pages.values() if not p['rec']),
            sum(len(p['feeds']) for p in pages.values()), sum(1 for f in feeds.values() if f['rec'])))
        return
    if phase == 'sitemaps':                                 # B5
        sm = {}
        for h in hosts:
            rob = P.ROBOTS[h]
            declared = list(dict.fromkeys(rob['sitemaps']))
            urls = declared if declared else ['%s/sitemap.xml' % h]
            ent = dict(host=h, declared=declared, basis='declared' if declared else '/sitemap.xml (none declared)', docs=[])
            for u in urls:
                ent['docs'].append(read_sitemap(u, h, depth=0))
            sm[h] = ent
        P.save('b5.json', sm)
        P.save('b3.json', {h: P.ROBOTS[h] for h in P.ROBOTS})
        print('B5 hosts %d; top-level sitemap documents %d' % (len(sm), sum(len(e['docs']) for e in sm.values())))
        return

def read_sitemap(u, host, depth):
    rec, perm = P.guarded(u, 'B5', 'sitemap for %s' % host)
    d = dict(url=u, perm=perm, rec=rec['id'] if rec else None,
             outcome=P.outcome(rec) if rec else 'refused on permission', kind=None, children=[])
    if not rec or d['outcome'] != 'ok':
        return d
    ps = P.parse_sitemap(P.body_of(rec))
    d['kind'] = ps['kind']
    if ps['kind'] == 'index':
        kids = [e for e in ps['entries'] if e['loc'] and P.kw_path(e['loc'])]
        order = sorted(range(len(kids)), key=lambda i: (0 if kids[i]['date'] else 1,
                                                        -kids[i]['date'].timestamp() if kids[i]['date'] else 0, i))
        d['index_entries'] = len(ps['entries'])
        d['index_kw_entries'] = len(kids)
        if depth == 0:
            for i in order[:3]:
                d['children'].append(read_sitemap(kids[i]['loc'], host, depth=1))
        else:
            d['nested'] = True
    return d

# ---------------------------------------------------------------- Stage B6/B7 (offline)

def lane_from_feed(rec_id):
    rec = [r for r in P.ledger() if r['id'] == rec_id][0]
    oc = P.outcome(rec)
    if oc != 'ok':
        return dict(kind='feed', outcome=oc, rec=rec_id, landing=rec['landing'])
    items = P.parse_feed(P.body_of(rec))
    if items is None:
        return dict(kind='feed', outcome='no channel (not a feed: %s)' % (rec['ctype'] or '-'), rec=rec_id, landing=rec['landing'])
    dates = [i['date'] for i in items if i['date'] is not None]
    cls, nd = P.classify(dates)
    return dict(kind='feed', outcome=cls, rec=rec_id, landing=rec['landing'], records=len(items), dated=len(dates),
                days=nd, newest=max(dates).isoformat() if dates else None, oldest=min(dates).isoformat() if dates else None,
                _dates=dates)

def lane_from_urlset(rec_id):
    rec = [r for r in P.ledger() if r['id'] == rec_id][0]
    ps = P.parse_sitemap(P.body_of(rec))
    ents = ps['entries']
    kw = [e for e in ents if P.kw_path(e['loc'])]
    cons = kw if kw else ents
    dates = [e['date'] for e in cons if e['date'] is not None]
    cls, nd = P.classify(dates)
    return dict(kind='sitemap', outcome=cls, rec=rec_id, landing=rec['landing'], urls=len(ents),
                basis='keyword paths' if kw else 'every URL (no keyword path)', considered=len(cons),
                with_lastmod=len(dates), days=nd,
                newest=max(dates).isoformat() if dates else None, oldest=min(dates).isoformat() if dates else None,
                placeholders=P.placeholder_quotes(ps['comments']), comments=len(ps['comments']), _dates=dates)

def sitemap_lanes(doc):
    """Flatten one top-level sitemap read into lanes: a urlset is a lane; an index
    contributes its children; a failed read is a lane carrying its outcome."""
    if doc['outcome'] != 'ok':
        return [dict(kind='sitemap', url=doc['url'], outcome=doc['outcome'], rec=doc['rec'])]
    if doc['kind'] == 'urlset':
        l = lane_from_urlset(doc['rec']); l['url'] = doc['url']; return [l]
    if doc['kind'] == 'index':
        if doc.get('nested'):
            return [dict(kind='sitemap', url=doc['url'], outcome='no channel (nested index, not descended: %d entries)' % (
                doc.get('index_entries', 0)), rec=doc['rec'])]
        if not doc['children']:
            return [dict(kind='sitemap', url=doc['url'], outcome='no channel (index: %d entries, %d keyword children)' % (
                doc.get('index_entries', 0), doc.get('index_kw_entries', 0)), rec=doc['rec'])]
        out = []
        for c in doc['children']:
            for l in sitemap_lanes(c):
                l['parent'] = doc['url']; out.append(l)
        return out
    rec = [r for r in P.ledger() if r['id'] == doc['rec']][0]
    return [dict(kind='sitemap', url=doc['url'], outcome='no channel (%s: %s)' % (doc['kind'], rec['ctype'] or '-'), rec=doc['rec'])]

def stage_b_classify():
    a, b1, cand = P.load('a.json'), P.load('b1.json'), P.load('b2.json')
    b4, b5 = P.load('b4.json'), P.load('b5.json')
    rows = []
    for t in a['tokens']:
        sym = t['sym']; c = cand[sym]
        cov = a['coverage'].get(sym)
        move = cov.get('move') if isinstance(cov, dict) else None
        D = P.move_day_of(move)
        lanes, hosts_done = [], []
        for cd in c['cands']:
            pg = b4['pages'].get(cd['url'])
            h = P.origin_of(cd['url'])
            if pg and pg.get('self_feed'):
                l = lane_from_feed(pg['rec']); l['url'] = cd['url']; l['from'] = cd['kind'] + ' (the page is a feed)'
                lanes.append(l)
            for fl in (pg or {}).get('feeds', []):
                f = b4['feeds'].get(fl['url'])
                if not f or fl.get('read') == 'not read (two per host)':
                    continue
                if f['rec'] is None:
                    l = dict(kind='feed', url=fl['url'], outcome='refused on permission')
                else:
                    l = lane_from_feed(f['rec']); l['url'] = fl['url']
                l['from'] = 'feed advertised by %s' % cd['url']
                if l['url'] not in [x.get('url') for x in lanes]:
                    lanes.append(l)
            if h not in hosts_done:
                hosts_done.append(h)
                for doc in b5[h]['docs']:
                    for l in sitemap_lanes(doc):
                        l['from'] = 'sitemap of %s (%s)' % (h, b5[h]['basis'])
                        l['origin'] = h
                        if not any(x.get('url') == l['url'] and x.get('rec') == l.get('rec') for x in lanes):
                            lanes.append(l)
        for l in lanes:
            if l['outcome'] == 'dated':
                l['b7'] = P.screen(l['_dates'], D) if D else 'no move recorded'
                if D:
                    win = [P.uday(x) for x in l['_dates'] if D - dt.timedelta(days=2) <= P.uday(x) <= D]
                    l['hits'] = len(win)
                    l['hit_days'] = sorted({str(x) for x in win})
            else:
                l['b7'] = '-'
        verdicts = [l['b7'] for l in lanes if l['outcome'] == 'dated']
        if not c['cands']:
            coin = 'Stage B unserved (no candidate)'
        elif D is None:
            coin = 'no move recorded'
        elif 'carried' in verdicts:
            coin = 'carried'
        elif 'window short' in verdicts:
            coin = 'window short'
        elif verdicts:
            coin = 'not carried'
        else:
            coin = 'no dated lane'
        home = b1[sym].get('homepage')
        rows.append(dict(sym=sym, name=b1[sym].get('name'), site=urlparse(home).hostname if home else None,
                         move=move, D=str(D) if D else None, cands=c['cands'],
                         lanes=[{k: v for k, v in l.items() if k != '_dates'} for l in lanes], coin=coin))
    P.save('b6.json', rows)
    for r in rows:
        print('B %-7s site=%s move=%s -> %s' % (r['sym'], r['site'], r['move'], r['coin']))
        for l in r['lanes']:
            print('     %-7s %-60s %-28s win %s .. %s  B7 %s' % (l['kind'], (l.get('landing') or l['url'])[:60], l['outcome'][:28],
                                                            (l.get('oldest') or '-')[:10], (l.get('newest') or '-')[:10], l['b7']))
    print('B attempted coins %d of A2 %d' % (len(rows), len(a['tokens'])))

# ---------------------------------------------------------------- Stage C

FEEDS = ['https://www.coindesk.com/arc/outboundfeeds/rss/', 'https://www.theblock.co/rss.xml',
         'https://decrypt.co/feed', 'https://cointelegraph.com/rss']

def word_rx(s, ci):
    return re.compile(r'(?<![A-Za-z0-9])' + re.escape(s) + r'(?![A-Za-z0-9])', re.I if ci else 0)

def stage_c(read=True):
    a, b1 = P.load('a.json'), P.load('b1.json')
    res = {}
    for u in FEEDS:
        if read:
            rec, perm = P.guarded(u, 'C', 'reporter feed')
        else:
            rs = [r for r in P.ledger() if r['url'] == u]
            rec = rs[0] if rs else None
            ok, perm = P.permitted(u, 'C') if rec else (False, None)
        ent = dict(url=u, perm=perm, rec=rec['id'] if rec else None, outcome=P.outcome(rec) if rec else 'refused on permission')
        if rec and ent['outcome'] == 'ok':
            items = P.parse_feed(P.body_of(rec))
            if items is None:
                ent['outcome'] = 'not a feed'
            else:
                dates = [i['date'] for i in items if i['date']]
                ent.update(landing=rec['landing'], items=len(items), dated=len(dates),
                           newest=max(dates).isoformat() if dates else None, oldest=min(dates).isoformat() if dates else None,
                           _items=items)
        res[u] = ent
    # list yield
    ly = []
    for u, e in res.items():
        for it in e.get('_items', []):
            hit = []
            for t in a['tokens']:
                if word_rx(t['sym'], False).search(it['title']):
                    hit.append(t['sym'])
                nm = b1[t['sym']].get('name')
                if nm and word_rx(nm, True).search(it['title']) and t['sym'] not in hit:
                    hit.append(t['sym'] + '(name)')
            if hit:
                ly.append(dict(feed=urlparse(u).hostname, date=it['date'].astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%MZ') if it['date'] else None,
                               title=it['title'][:100], hit=hit))
    # book yield
    lv = json.load(open(P.REPO + '/analyst/live.json', encoding='utf-8'))
    top = list(lv.keys())
    tsk = [k for k in top if k.lower() in ('ts', 'time', 'timestamp', 'generated', 'generated_at', 'asof', 'as_of', 'updated', 'updated_at', 'd')]
    x = lv.get('x') or []
    first = x[0] if x and isinstance(x[0], dict) else {}
    symk = next((k for k in ('s', 'sym', 'symbol', 'pair') if k in first), None)
    bases = sorted({r[symk][:-4] for r in x if isinstance(r, dict) and isinstance(r.get(symk), str) and r[symk].endswith('USDT')}) if symk else []
    per, nt = {}, 0
    for u, e in res.items():
        for it in e.get('_items', []):
            got = [b for b in bases if word_rx(b, False).search(it['title'])]
            if got:
                nt += 1
                for b in got:
                    per[b] = per.get(b, 0) + 1
    alld = [d for e in res.values() for d in [i['date'] for i in e.get('_items', []) if i['date']]]
    out = dict(feeds={u: {k: v for k, v in e.items() if k != '_items'} for u, e in res.items()}, list_yield=ly,
               live=dict(top=top, ts_fields={k: lv[k] for k in tsk}, x_rows=len(x), x_first_keys=list(first.keys()), sym_key=symk,
                         usdt_bases=len(bases)),
               book_yield=dict(titles=nt, per_base=per),
               union=dict(oldest=min(alld).isoformat() if alld else None, newest=max(alld).isoformat() if alld else None,
                          items=sum(e.get('items', 0) for e in res.values())))
    P.save('c.json', out)
    for u, e in out['feeds'].items():
        print('C %s -> %s items=%s dated=%s window %s .. %s' % (u, e['outcome'], e.get('items'), e.get('dated'), e.get('oldest'), e.get('newest')))
    print('C list yield %d titles; book yield %d titles over %d USDT bases' % (len(ly), nt, len(bases)))
    print('C live.json top keys %s; ts fields %s; first x keys %s' % (top, out['live']['ts_fields'], out['live']['x_first_keys']))
    print('C union window %s .. %s' % (out['union']['oldest'], out['union']['newest']))
    print('C attempted %d feeds; reported %d' % (len(FEEDS), len(res)))

# ---------------------------------------------------------------- Stage D

def stage_d(read=True):
    a = P.load('a.json')
    u = 'https://api.upbit.com/v1/market/all?isDetails=true'
    rec = P.fetch(u, 'D', 'Upbit market list') if read else [r for r in P.ledger() if r['url'] == u][0]
    out = dict(rec=rec['id'], outcome=P.outcome(rec))
    if out['outcome'] == 'ok':
        j = json.loads(P.body_of(rec))
        lv = json.load(open(P.REPO + '/analyst/live.json', encoding='utf-8'))
        x = lv.get('x') or []
        first = x[0] if x and isinstance(x[0], dict) else {}
        symk = next((k for k in ('s', 'sym', 'symbol', 'pair') if k in first), None)
        xb = {r[symk][:-4] for r in x if isinstance(r, dict) and isinstance(r.get(symk), str) and r[symk].endswith('USDT')} if symk else set()
        a2 = {t['sym'] for t in a['tokens']}
        krw = [m for m in j if m.get('market', '').startswith('KRW-')]
        kb = {m['market'][4:] for m in krw}
        warn = [m for m in j if (m.get('market_event') or {}).get('warning') is True]
        ckeys = {}
        for m in j:
            for k, v in ((m.get('market_event') or {}).get('caution') or {}).items():
                if v is True:
                    ckeys[k] = ckeys.get(k, 0) + 1
        flagged = []
        for m in j:
            base = m.get('market', '').split('-', 1)[-1]
            me = m.get('market_event') or {}
            cs = [k for k, v in (me.get('caution') or {}).items() if v is True]
            if base in a2 and (me.get('warning') is True or cs):
                flagged.append(dict(market=m['market'], warning=me.get('warning'), caution=cs))
        allkeys = sorted({k for m in j for k in ((m.get('market_event') or {}).get('caution') or {}).keys()})
        for k in allkeys:
            ckeys.setdefault(k, 0)
        names = {}
        for m in j:
            base = m.get('market', '').split('-', 1)[-1]
            if base in a2:
                names.setdefault(base, []).append('%s (%s)' % (m['market'], m.get('english_name')))
        out.update(caution_keys=allkeys, a2_markets=names)
        out.update(markets=len(j), krw=len(krw), krw_in_a2=len(kb & a2), krw_a2=sorted(kb & a2), a2_not_krw=sorted(a2 - kb),
                   krw_in_x=len(kb & xb), x_bases=len(xb), warning=len(warn), caution=ckeys, flagged=flagged,
                   has_event=sum(1 for m in j if 'market_event' in m))
    P.save('d.json', out)
    print('D %s' % json.dumps(out, ensure_ascii=False))

# ---------------------------------------------------------------- Stage E

FR = ('https://www.federalregister.gov/api/v1/documents.json?per_page=20&order=newest'
      '&conditions%5Bagencies%5D%5B%5D=securities-and-exchange-commission')
EFTS = 'https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1'
T1 = ['Longer Period', 'Proceedings', 'Approving', 'Disapproving']
T2 = ['bitcoin', 'ether', 'crypto', 'digital asset', 'solana', 'xrp', 'trust']

def stage_e1(read=True):
    rec = P.fetch(FR, 'E1', 'Federal Register SEC documents') if read else [r for r in P.ledger() if r['url'] == FR][0]
    out = dict(rec=rec['id'], outcome=P.outcome(rec))
    if out['outcome'] == 'ok':
        j = json.loads(P.body_of(rec))
        rs = j.get('results') or []
        out.update(count=j.get('count'), results=len(rs),
                   rows=[dict(date=r.get('publication_date'), type=r.get('type'), title=(r.get('title') or '')[:100]) for r in rs])
        titles = [r.get('title') or '' for r in rs]
        out['t1'] = {t: dict(cs=sum(t in s for s in titles), ci=sum(t.lower() in s.lower() for s in titles)) for t in T1}
        out['t2'] = {t: dict(substr=sum(t in s.lower() for s in titles), word=sum(bool(word_rx(t, True).search(s)) for s in titles)) for t in T2}
        out['t2_any'] = dict(substr=sum(any(t in s.lower() for t in T2) for s in titles),
                             word=sum(any(word_rx(t, True).search(s) for t in T2) for s in titles))
    P.save('e1.json', out)
    print('E1 %s' % json.dumps({k: v for k, v in out.items() if k != 'rows'}, ensure_ascii=False))
    for r in out.get('rows', []):
        print('E1   %s  %-14s %s' % (r['date'], r['type'], r['title']))

def stage_e2(read=True):
    em = subprocess.run(['git', '-C', P.REPO, 'config', '--get', 'user.email'], capture_output=True, text=True)
    addr = em.stdout.strip() if em.returncode == 0 and '@' in em.stdout else None
    mask = (addr[0] + '***@' + addr.split('@', 1)[1]) if addr else None
    out = {}
    ra = P.fetch(EFTS, 'E2a', 'SEC full-text search, rule-1 form') if read else [r for r in P.ledger() if r['url'] == EFTS and r['form'] == 'rule1'][0]
    out['a'] = efts_read(ra)
    if addr:
        if read:
            rb = P.fetch(EFTS, 'E2b', 'SEC full-text search, declared client', form='declared',
                         extra=['-A', 'crypto-auto ' + addr], extra_display='-A "crypto-auto %s"' % mask)
        else:
            rb = [r for r in P.ledger() if r['url'] == EFTS and r['form'] == 'declared'][0]
        out['b'] = efts_read(rb)
    else:
        out['b'] = 'not made: A4 found no address'
    out['contact_masked'] = mask
    P.save('e2.json', out)
    print('E2 %s' % json.dumps(out, ensure_ascii=False))

def efts_read(rec):
    d = dict(rec=rec['id'], outcome=P.outcome(rec), code=rec['code'], bytes=rec['bytes'], ctype=rec['ctype'])
    try:
        j = json.loads(P.body_of(rec))
        d['json'] = True
        d['hits_total'] = ((j.get('hits') or {}).get('total') or {}).get('value')
    except Exception:
        d['json'] = False
    return d

# ---------------------------------------------------------------- Stage F

FAPI = 'https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1h&limit=3'

def stage_f(read=True):
    a = P.load('a.json')
    out = []
    for t in [t for t in a['tokens'] if t['fut']]:
        u = FAPI % t['pair']
        rec = P.fetch(u, 'F', 'USDS-M klines %s' % t['pair']) if read else [r for r in P.ledger() if r['url'] == u][0]
        e = dict(pair=t['pair'], rec=rec['id'], outcome=P.outcome(rec), code=rec['code'], bytes=rec['bytes'], ctype=rec['ctype'])
        try:
            j = json.loads(P.body_of(rec))
            if isinstance(j, list):
                e['rows'] = len(j)
                e['row_len'] = len(j[-1]) if j else None
                if j:
                    e['last_open'] = dt.datetime.fromtimestamp(j[-1][0] / 1000, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            elif isinstance(j, dict):
                e['json_keys'] = sorted(j.keys())
                e['code_field'] = j.get('code')
                e['msg'] = (j.get('msg') or '')[:160]
        except Exception:
            e['json'] = False
        out.append(e)
        print('F %s' % json.dumps(e, ensure_ascii=False), flush=True)
    P.save('f.json', out)
    print('F attempted %d of fut:true %d' % (len(out), sum(t['fut'] for t in a['tokens'])))

# ---------------------------------------------------------------- V1

def v1():
    import pathlib
    d = pathlib.Path(P.ROOT + '/v1'); d.mkdir(exist_ok=True)
    (d / 'a.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                             '<url><loc>https://x.test/news/one</loc><lastmod>2026-09-20</lastmod></url>'
                             '<url><loc>https://x.test/news/two</loc><lastmod>2026-09-21T10:00:00Z</lastmod></url></urlset>')
    (d / 'b.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                             '<url><loc>https://x.test/a</loc><lastmod>2026-08-15</lastmod></url>'
                             '<url><loc>https://x.test/b</loc><lastmod>2026-08-15</lastmod></url>'
                             '<url><loc>https://x.test/c</loc><lastmod>2026-08-15</lastmod></url></urlset>')
    (d / 'c.xml').write_text('<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                             '<url><loc>https://x.test/a</loc></url><url><loc>https://x.test/b</loc></url></urlset>')
    D = dt.date(2026, 9, 17)
    fx = {'d': dict(move=str(D), records=[str(D - dt.timedelta(days=1)), str(D - dt.timedelta(days=10)), str(D - dt.timedelta(days=5))]),
          'e': dict(move=str(D), records=[str(D + dt.timedelta(days=1)), str(D + dt.timedelta(days=3))])}
    (d / 'de.json').write_text(json.dumps(fx, indent=1))
    exp = {'a': 'dated', 'b': 'undated', 'c': 'undated', 'd': 'carried', 'e': 'window short'}
    got, inv, ok = {}, {}, 0
    for f in 'abc':
        ps = P.parse_sitemap((d / (f + '.xml')).read_bytes())
        dates = [e['date'] for e in ps['entries'] if e['date']]
        got[f] = P.classify(dates)[0]
        inv[f] = P.classify(dates, invert=True)[0]
    for f in 'de':
        recs = [P.parse_date(s) for s in fx[f]['records']]
        got[f] = P.screen(recs, dt.date.fromisoformat(fx[f]['move']))
    print('V1 run 1 (B6/B7 as written):')
    for f in 'abcde':
        m = got[f] == exp[f]; ok += m
        print('  fixture %s  expected %-12s got %-12s %s' % (f, exp[f], got[f], 'PASS' if m else 'FAIL'))
    print('V1 run 2 (B6 comparison inverted, a-c):')
    for f in 'abc':
        print('  fixture %s  run1 %-9s inverted %-9s' % (f, got[f], inv[f]))
    swap = inv['a'] == got['b'] and inv['b'] == got['a'] and inv['a'] != got['a']
    print('V1 checks run %d, PASS %d, FAIL %d; negative control a<->b swapped: %s' % (5, ok, 5 - ok, 'yes' if swap else 'NO'))
    return ok == 5 and swap

def stage_v2(read=True):
    """V2: live known-answer pair. NEAR's half is Stage B's own read; Ondo's names a host
    Stage B did not reach, so its two URLs are read here, robots.txt first, once each."""
    a = P.load('a.json')
    L = {r['url']: r for r in P.ledger()}
    out = {}
    # NEAR: the Stage B read of https://www.near.org/sitemap.xml
    nu = 'https://www.near.org/sitemap.xml'
    nrec = L.get(nu) or next((r for r in P.ledger() if r['landing'] == nu), None)
    near = dict(url=nu, rec=nrec['id'] if nrec else None, source='Stage B read' if nrec else 'not read')
    if nrec:
        ps = P.parse_sitemap(P.body_of(nrec))
        dates = [e['date'] for e in ps['entries'] if e['date']]
        kw = [e for e in ps['entries'] if P.kw_path(e['loc'])]
        cons = kw if kw else ps['entries']
        cdates = [e['date'] for e in cons if e['date']]
        near.update(kind=ps['kind'], urls=len(ps['entries']), with_lastmod=len(dates),
                    distinct_days_all=sorted({str(P.uday(d)) for d in dates}), considered=len(cons),
                    b6=P.classify(cdates)[0], placeholders=P.placeholder_quotes(ps['comments']))
    out['NEAR'] = near
    # Ondo: https://ondo.finance/sitemap.xml, declared in that host's robots.txt (per V2)
    ou = 'https://ondo.finance/sitemap.xml'
    if read:
        rob = P.robots_for('https://ondo.finance', 'V2')
        orec, perm = P.guarded(ou, 'V2', 'V2 known answer: Ondo sitemap')
    else:
        rob = P.robots_for('https://ondo.finance', 'V2')
        orec = L.get(ou); ok, perm = P.permitted(ou, 'V2')
    ondo = dict(url=ou, robots=rob['rec'], robots_code=rob['code'], declared=ou in rob['sitemaps'], declared_list=rob['sitemaps'],
                perm=perm, rec=orec['id'] if orec else None, outcome=P.outcome(orec) if orec else 'refused on permission')
    if orec and ondo['outcome'] == 'ok':
        ps = P.parse_sitemap(P.body_of(orec))
        ents = ps['entries']
        dates = [e['date'] for e in ents if e['date']]
        kw = [e for e in ents if P.kw_path(e['loc'])]
        cons = kw if kw else ents
        cdates = [e['date'] for e in cons if e['date']]
        blog = [e for e in ents if 'blog' in P.urlparse(e['loc']).path.lower() and e['date']]
        nb = max(blog, key=lambda e: e['date']) if blog else None
        D = P.move_day_of((a['coverage'].get('ONDO') or {}).get('move') if isinstance(a['coverage'].get('ONDO'), dict) else None)
        ondo.update(kind=ps['kind'], urls=len(ents), with_lastmod=len(dates), considered=len(cons),
                    basis='keyword paths' if kw else 'every URL', considered_with_lastmod=len(cdates),
                    days=len({P.uday(d) for d in cdates}), b6=P.classify(cdates)[0],
                    newest_blog=nb['raw'] if nb else None, newest_blog_loc=nb['loc'] if nb else None,
                    newest=max(cdates).isoformat() if cdates else None, oldest=min(cdates).isoformat() if cdates else None,
                    placeholders=P.placeholder_quotes(ps['comments']),
                    b7_aux=(P.screen(cdates, D) if D and P.classify(cdates)[0] == 'dated' else None), D=str(D) if D else None,
                    b7_hits=sorted({str(P.uday(x)) for x in cdates if D and D - dt.timedelta(days=2) <= P.uday(x) <= D}))
    out['Ondo'] = ondo
    exp = {'NEAR': 'undated', 'Ondo': 'dated'}
    for k in ('NEAR', 'Ondo'):
        got = out[k].get('b6')
        out[k]['expected'] = exp[k]
        out[k]['verdict'] = 'match' if got == exp[k] else 'MISMATCH'
    out['NEAR']['host_changed'] = not (out['NEAR'].get('placeholders') and out['NEAR'].get('distinct_days_all') == ['2026-08-15'])
    out['Ondo']['host_changed'] = not (out['Ondo'].get('declared') and out['Ondo'].get('urls') == 198 and out['Ondo'].get('with_lastmod') == 186
                                       and out['Ondo'].get('newest_blog') == '2026-09-24T12:30:00.000Z')
    P.save('v2.json', out)
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str))

def main(argv):
    cmd = argv[0]
    fn = {'a': stage_a, 'b1': stage_b1, 'b-robots': lambda: stage_b_reads('robots'),
          'b-pages': lambda: stage_b_reads('pages'), 'b-sitemaps': lambda: stage_b_reads('sitemaps'),
          'b-classify': stage_b_classify, 'c': stage_c, 'c-offline': lambda: stage_c(False),
          'd': stage_d, 'd-offline': lambda: stage_d(False), 'e1': stage_e1, 'e1-offline': lambda: stage_e1(False),
          'e2': stage_e2, 'e2-offline': lambda: stage_e2(False), 'f': stage_f, 'f-offline': lambda: stage_f(False),
          'v1': v1, 'v2': stage_v2, 'v2-offline': lambda: stage_v2(False)}[cmd]
    held = None
    if cmd not in ('v1', 'a', 'b-classify') and not cmd.endswith('-offline'):
        held = P.lock()            # one probe process at a time: reads are sequential, never parallel
    r = fn()
    if cmd == 'v1':
        sys.exit(0 if r else 1)
```

</details>

### Stage A — Baseline and the engine's own coverage record

**A2.** `tokens[]` was cut from `index.html` by regex over the literal between `var tokens = [`
and `];`. The regex matched 30 rows, and `name:` occurs 30 times in the literal. `TOKENS` was
read from `main.py` with `ast.literal_eval` on the module's own assignment. Both counts are 30,
the symmetric difference is **empty**, and `fut:true` rows number 5: HYPE, XMR, LIT, MORPHO
and ARB.

| # | Symbol | Pair | `fut:true` | CoinGecko id (`TOKENS`) |
|---:|---|---|---|---|
| 1 | SUI | `SUIUSDT` |  | `sui` |
| 2 | ONDO | `ONDOUSDT` |  | `ondo-finance` |
| 3 | LINK | `LINKUSDT` |  | `chainlink` |
| 4 | RENDER | `RENDERUSDT` |  | `render-token` |
| 5 | NEAR | `NEARUSDT` |  | `near` |
| 6 | YFI | `YFIUSDT` |  | `yearn-finance` |
| 7 | AAVE | `AAVEUSDT` |  | `aave` |
| 8 | AVAX | `AVAXUSDT` |  | `avalanche-2` |
| 9 | FET | `FETUSDT` |  | `fetch-ai` |
| 10 | ENA | `ENAUSDT` |  | `ethena` |
| 11 | TAO | `TAOUSDT` |  | `bittensor` |
| 12 | GRAM | `GRAMUSDT` |  | `the-open-network` |
| 13 | XRP | `XRPUSDT` |  | `ripple` |
| 14 | ADA | `ADAUSDT` |  | `cardano` |
| 15 | TRX | `TRXUSDT` |  | `tron` |
| 16 | SOL | `SOLUSDT` |  | `solana` |
| 17 | BCH | `BCHUSDT` |  | `bitcoin-cash` |
| 18 | HYPE | `HYPEUSDT` | yes | `hyperliquid` |
| 19 | SKY | `SKYUSDT` |  | `sky` |
| 20 | ETH | `ETHUSDT` |  | `ethereum` |
| 21 | HBAR | `HBARUSDT` |  | `hedera-hashgraph` |
| 22 | XLM | `XLMUSDT` |  | `stellar` |
| 23 | ALGO | `ALGOUSDT` |  | `algorand` |
| 24 | BNB | `BNBUSDT` |  | `binancecoin` |
| 25 | ZEC | `ZECUSDT` |  | `zcash` |
| 26 | UNI | `UNIUSDT` |  | `uniswap` |
| 27 | XMR | `XMRUSDT` | yes | `monero` |
| 28 | LIT | `LITUSDT` | yes | `lighter` |
| 29 | MORPHO | `MORPHOUSDT` | yes | `morpho` |
| 30 | ARB | `ARBUSDT` | yes | `arbitrum` |

**A3.** `analyst/state.json` is at `v` 2, `d` 2026-09-24, `ts` 2026-09-24T21:30:56Z, with 30
`sweeps.coins` entries. Every A2 symbol has a `coverage` record, and **0 are `absent`**. Per
status: **`охвачена` 11 · `неохваченная` 14 · `неизмерима` 5**, with the status word printed as
the file holds it (see Pre-existing Issues 1).

| Symbol | `d` | `status` | `move` | `carried_by` (verbatim) |
|---|---|---|---|---|
| SUI | 2026-09-21 | охвачена | +9.55% 2026-09-03 | forums.sui.io |
| ONDO | 2026-09-21 | неохваченная | +14.04% 2026-09-17 | канала у ONDO нет — §6a объявляет его необслуженным |
| LINK | 2026-09-21 | неохваченная | +6.89% 2026-09-18 | — *(field absent)* |
| RENDER | 2026-09-21 | неохваченная | +10.02% 2026-09-17 | — *(field absent)* |
| NEAR | 2026-09-21 | охвачена | +26.30% 2026-09-18 | gov.near.org |
| YFI | 2026-09-21 | неохваченная | +6.48% 2026-09-18 | — *(field absent)* |
| AAVE | 2026-09-23 | охвачена | +11.99% 2026-09-17 | governance.aave.com — 9 записей в 48 ч до хода, в т.ч. «[ARFC] Revision of ETH & BTC Collateral Efficiency on Aave» 16.09 и «Risk Stewards: Cap and IRM Changes on Aave V3 / 2026.09.16» |
| AVAX | 2026-09-21 | неохваченная | +18.67% 2026-09-19 | — *(field absent)* |
| FET | 2026-09-21 | охвачена | +11.98% 2026-09-17 | api.github.com |
| ENA | 2026-09-21 | неохваченная | +20.92% 2026-09-19 | — *(field absent)* |
| TAO | 2026-09-23 | охвачена | +10.25% 2026-09-22 | api.github.com/repos/opentensor/subtensor — релизы v468 (21.09) и v469 (22.09) внутри 48 ч до хода |
| GRAM | 2026-09-21 | неохваченная | -6.17% 2026-09-01 | — *(field absent)* |
| XRP | 2026-09-21 | неохваченная | -9.62% 2026-09-16 | — *(field absent)* |
| ADA | 2026-09-21 | неохваченная | +13.52% 2026-09-03 | — *(field absent)* |
| TRX | 2026-09-21 | неохваченная | -3.12% 2026-09-01 | — *(field absent)* |
| SOL | 2026-09-21 | охвачена | +10.19% 2026-09-18 | forum.solana.com |
| BCH | 2026-09-21 | неохваченная | -12.26% 2026-09-10 | — *(field absent)* |
| HYPE | 2026-09-23 | неизмерима | нет структурной строки | канала у монеты §6a не устанавливает (HYPE: releases hyperliquid-dex/node пуст, форума нет, токен-контракта нет; LIT: протокол за тикером в репозитории не установлен) И объявленный фьючерсный актив без cd — измерять нечем и не на чем |
| SKY | 2026-09-21 | охвачена | +16.69% 2026-09-18 | forum.skyeco.com |
| ETH | 2026-09-21 | охвачена | +5.33% 2026-09-11 | blog.ethereum.org |
| HBAR | 2026-09-21 | неохваченная | +9.93% 2026-09-03 | — *(field absent)* |
| XLM | 2026-09-21 | неохваченная | -9.23% 2026-09-16 | — *(field absent)* |
| ALGO | 2026-09-21 | охвачена | +12.05% 2026-09-20 | forum.algorand.co |
| BNB | 2026-09-21 | неохваченная | +7.26% 2026-09-05 | — *(field absent)* |
| ZEC | 2026-09-23 | охвачена | +18.14% 2026-09-17 | forum.zcashcommunity.com — тема 57655 «NU7 Timeline», пост #1 ebfull 17.09, в день хода. ОГОВОРКА: страница latest.json этого чтения достаёт только до 22.09, то есть окно страницы до даты хода НЕ ДОСТАЁТ; запись установлена прямым чтением темы (t/57655.json 200, 31376 байт). |
| UNI | 2026-09-21 | охвачена | +23.04% 2026-09-17 | gov.uniswap.org |
| XMR | 2026-09-23 | неизмерима | нет структурной строки | объявленный фьючерсный актив (fut:true): запись k:"x" без px и без cd — крупнейший однодневный ход инструментом §6a не вычисляется (map §3.14, инв. 41) |
| LIT | 2026-09-23 | неизмерима | нет структурной строки | канала у монеты §6a не устанавливает (HYPE: releases hyperliquid-dex/node пуст, форума нет, токен-контракта нет; LIT: протокол за тикером в репозитории не установлен) И объявленный фьючерсный актив без cd — измерять нечем и не на чем |
| MORPHO | 2026-09-23 | неизмерима | нет структурной строки | объявленный фьючерсный актив (fut:true): запись k:"x" без px и без cd — крупнейший однодневный ход инструментом §6a не вычисляется (map §3.14, инв. 41) |
| ARB | 2026-09-23 | неизмерима | нет структурной строки | объявленный фьючерсный актив (fut:true): journal/data пишет для него запись k:"x" без px и без cd, поэтому крупнейший однодневный ход по инструменту §6a не вычисляется (map §3.14, инв. 41) |

```
A2 tokens[] rows parsed: 30 (name: occurrences in the literal: 30)
A2 tokens[] fut:true: 5 -> HYPEUSDT XMRUSDT LITUSDT MORPHOUSDT ARBUSDT
A2 TOKENS entries: 30
A2 symmetric difference: empty
A3 state.json v=2 d=2026-09-24 ts=2026-09-24T21:30:56Z; sweeps.coins entries: 30
A3 SUI     {"d": "2026-09-21", "status": "охвачена", "move": "+9.55% 2026-09-03", "carried_by": "forums.sui.io"}
A3 ONDO    {"d": "2026-09-21", "status": "неохваченная", "move": "+14.04% 2026-09-17", "carried_by": "канала у ONDO нет — §6a объявляет его необслуженным"}
A3 LINK    {"d": "2026-09-21", "status": "неохваченная", "move": "+6.89% 2026-09-18"}
A3 RENDER  {"d": "2026-09-21", "status": "неохваченная", "move": "+10.02% 2026-09-17"}
A3 NEAR    {"d": "2026-09-21", "status": "охвачена", "move": "+26.30% 2026-09-18", "carried_by": "gov.near.org"}
A3 YFI     {"d": "2026-09-21", "status": "неохваченная", "move": "+6.48% 2026-09-18"}
A3 AAVE    {"d": "2026-09-23", "status": "охвачена", "move": "+11.99% 2026-09-17", "carried_by": "governance.aave.com — 9 записей в 48 ч до хода, в т.ч. «[ARFC] Revision of ETH & BTC Collateral Efficiency on Aave» 16.09 и «Risk Stewards: Cap and IRM Changes on Aave V3 / 2026.09.16»"}
A3 AVAX    {"d": "2026-09-21", "status": "неохваченная", "move": "+18.67% 2026-09-19"}
A3 FET     {"d": "2026-09-21", "status": "охвачена", "move": "+11.98% 2026-09-17", "carried_by": "api.github.com"}
A3 ENA     {"d": "2026-09-21", "status": "неохваченная", "move": "+20.92% 2026-09-19"}
A3 TAO     {"d": "2026-09-23", "status": "охвачена", "move": "+10.25% 2026-09-22", "carried_by": "api.github.com/repos/opentensor/subtensor — релизы v468 (21.09) и v469 (22.09) внутри 48 ч до хода"}
A3 GRAM    {"d": "2026-09-21", "status": "неохваченная", "move": "-6.17% 2026-09-01"}
A3 XRP     {"d": "2026-09-21", "status": "неохваченная", "move": "-9.62% 2026-09-16"}
A3 ADA     {"d": "2026-09-21", "status": "неохваченная", "move": "+13.52% 2026-09-03"}
A3 TRX     {"d": "2026-09-21", "status": "неохваченная", "move": "-3.12% 2026-09-01"}
A3 SOL     {"d": "2026-09-21", "status": "охвачена", "move": "+10.19% 2026-09-18", "carried_by": "forum.solana.com"}
A3 BCH     {"d": "2026-09-21", "status": "неохваченная", "move": "-12.26% 2026-09-10"}
A3 HYPE    {"d": "2026-09-23", "status": "неизмерима", "move": "нет структурной строки", "carried_by": "канала у монеты §6a не устанавливает (HYPE: releases hyperliquid-dex/node пуст, форума нет, токен-контракта нет; LIT: протокол за тикером в репозитории не установлен) И объявленный фьючерсный актив без cd — измерять нечем и не на чем"}
A3 SKY     {"d": "2026-09-21", "status": "охвачена", "move": "+16.69% 2026-09-18", "carried_by": "forum.skyeco.com"}
A3 ETH     {"d": "2026-09-21", "status": "охвачена", "move": "+5.33% 2026-09-11", "carried_by": "blog.ethereum.org"}
A3 HBAR    {"d": "2026-09-21", "status": "неохваченная", "move": "+9.93% 2026-09-03"}
A3 XLM     {"d": "2026-09-21", "status": "неохваченная", "move": "-9.23% 2026-09-16"}
A3 ALGO    {"d": "2026-09-21", "status": "охвачена", "move": "+12.05% 2026-09-20", "carried_by": "forum.algorand.co"}
A3 BNB     {"d": "2026-09-21", "status": "неохваченная", "move": "+7.26% 2026-09-05"}
A3 ZEC     {"d": "2026-09-23", "status": "охвачена", "move": "+18.14% 2026-09-17", "carried_by": "forum.zcashcommunity.com — тема 57655 «NU7 Timeline», пост #1 ebfull 17.09, в день хода. ОГОВОРКА: страница latest.json этого чтения достаёт только до 22.09, то есть окно страницы до даты хода НЕ ДОСТАЁТ; запись установлена прямым чтением темы (t/57655.json 200, 31376 байт)."}
A3 UNI     {"d": "2026-09-21", "status": "охвачена", "move": "+23.04% 2026-09-17", "carried_by": "gov.uniswap.org"}
A3 XMR     {"d": "2026-09-23", "status": "неизмерима", "move": "нет структурной строки", "carried_by": "объявленный фьючерсный актив (fut:true): запись k:\"x\" без px и без cd — крупнейший однодневный ход инструментом §6a не вычисляется (map §3.14, инв. 41)"}
A3 LIT     {"d": "2026-09-23", "status": "неизмерима", "move": "нет структурной строки", "carried_by": "канала у монеты §6a не устанавливает (HYPE: releases hyperliquid-dex/node пуст, форума нет, токен-контракта нет; LIT: протокол за тикером в репозитории не установлен) И объявленный фьючерсный актив без cd — измерять нечем и не на чем"}
A3 MORPHO  {"d": "2026-09-23", "status": "неизмерима", "move": "нет структурной строки", "carried_by": "объявленный фьючерсный актив (fut:true): запись k:\"x\" без px и без cd — крупнейший однодневный ход инструментом §6a не вычисляется (map §3.14, инв. 41)"}
A3 ARB     {"d": "2026-09-23", "status": "неизмерима", "move": "нет структурной строки", "carried_by": "объявленный фьючерсный актив (fut:true): journal/data пишет для него запись k:\"x\" без px и без cd, поэтому крупнейший однодневный ход по инструменту §6a не вычисляется (map §3.14, инв. 41)"}
A3 per status: {"охвачена": 11, "неохваченная": 14, "неизмерима": 5}
A4 curl --version (first line): curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.10
A4 git config --get user.email returns an address: yes
```

### Stage B — The protocol's own site channels, per coin

**B1: CoinGecko, 30 reads, 12.50 s apart, 30 answered 200.** No coin's Stage B went unserved
for want of a registration.

| Coin | CoinGecko id | Read | HTTP | `name` | first `links.homepage` | `links.announcement_url` (non-empty) |
|---|---|---|---|---|---|---|
| SUI | `sui` | r001 | 200 | Sui | `https://sui.io/` | — |
| ONDO | `ondo-finance` | r002 | 200 | Ondo | `https://ondo.foundation/` | — |
| LINK | `chainlink` | r003 | 200 | Chainlink | `https://chain.link/` | `https://blog.chain.link/` |
| RENDER | `render-token` | r004 | 200 | Render | `http://renderfoundation.com` | `https://medium.com/render-token` |
| NEAR | `near` | r005 | 200 | NEAR Protocol | `https://near.org/` | `https://near.org/blog/`<br>`https://medium.com/nearprotocol` |
| YFI | `yearn-finance` | r006 | 200 | yearn.finance | `https://yearn.fi/` | `https://medium.com/iearn` |
| AAVE | `aave` | r007 | 200 | Aave | `https://aave.com/` | — |
| AVAX | `avalanche-2` | r008 | 200 | Avalanche | `https://www.avax.network` | `https://www.linkedin.com/company/avalancheavax` |
| FET | `fetch-ai` | r009 | 200 | Artificial Superintelligence Alliance | `https://www.superintelligence.io/` | `https://medium.com/fetch-ai` |
| ENA | `ethena` | r010 | 200 | Ethena | `https://www.ethena.fi/` | — |
| TAO | `bittensor` | r011 | 200 | Bittensor | `https://bittensor.com/` | — |
| GRAM | `the-open-network` | r012 | 200 | Gram (prev. Toncoin) | `https://ton.org/` | — |
| XRP | `ripple` | r013 | 200 | XRP | `https://ripple.com/currency/` | — |
| ADA | `cardano` | r014 | 200 | Cardano | `https://cardano.org/` | — |
| TRX | `tron` | r015 | 200 | TRON | `https://tron.network` | `https://medium.com/tron-foundation` |
| SOL | `solana` | r016 | 200 | Solana | `https://solana.com/` | — |
| BCH | `bitcoin-cash` | r017 | 200 | Bitcoin Cash | `https://bch.info/` | — |
| HYPE | `hyperliquid` | r018 | 200 | Hyperliquid | `https://app.hyperliquid.xyz/trade` | — |
| SKY | `sky` | r019 | 200 | Sky | `https://sky.money/` | — |
| ETH | `ethereum` | r020 | 200 | Ethereum | `https://www.ethereum.org/` | — |
| HBAR | `hedera-hashgraph` | r021 | 200 | Hedera | `https://www.hedera.com/` | `https://medium.com/hashgraph` |
| XLM | `stellar` | r022 | 200 | Stellar | `https://www.stellar.org/` | `https://stellarcommunity.org/`<br>`https://bitcointalk.org/index.php?topic=1428573.0` |
| ALGO | `algorand` | r023 | 200 | Algorand | `https://algorand.foundation/` | `https://medium.com/algorand`<br>`https://forum.algorand.org/` |
| BNB | `binancecoin` | r024 | 200 | BNB | `https://www.binance.com?ref=37754157` | — |
| ZEC | `zcash` | r025 | 200 | Zcash | `https://z.cash/` | — |
| UNI | `uniswap` | r026 | 200 | Uniswap | `https://uniswap.org/` | `https://uniswap.org/blog/` |
| XMR | `monero` | r027 | 200 | Monero | `https://www.getmonero.org/` | — |
| LIT | `lighter` | r028 | 200 | Lighter | `https://lighter.xyz/` | — |
| MORPHO | `morpho` | r029 | 200 | Morpho | `https://morpho.org/` | — |
| ARB | `arbitrum` | r030 | 200 | Arbitrum | `https://arbitrum.io/` | — |

**B2: candidates.** Each coin's list holds its homepage, its announcement URLs, and the root of
A3's `carried_by` host. The host is the first whitespace token of the field, cut at `/`, when it
has the shape of a hostname. Six `carried_by` values name no host: ONDO, HYPE, LIT, XMR, MORPHO
and ARB are prose. Thirteen coins carry no `carried_by` field. URLs were deduplicated after
lower-casing the scheme and host and turning an empty path into `/`. The query is kept, so
BNB's registered homepage keeps its `?ref=37754157`.

| Coin | Candidates after dedup (kind → URL as read) |
|---|---|
| SUI | homepage → `https://sui.io/`<br>carried_by root → `https://forums.sui.io/` |
| ONDO | homepage → `https://ondo.foundation/` · `carried_by` names no host (канала у ONDO нет — §6a объявляет его необслуженным) |
| LINK | homepage → `https://chain.link/`<br>announcement → `https://blog.chain.link/` · `carried_by` names no host (field absent) |
| RENDER | homepage → `http://renderfoundation.com/`<br>announcement → `https://medium.com/render-token` · `carried_by` names no host (field absent) |
| NEAR | homepage → `https://near.org/`<br>announcement → `https://near.org/blog/`<br>announcement → `https://medium.com/nearprotocol`<br>carried_by root → `https://gov.near.org/` |
| YFI | homepage → `https://yearn.fi/`<br>announcement → `https://medium.com/iearn` · `carried_by` names no host (field absent) |
| AAVE | homepage → `https://aave.com/`<br>carried_by root → `https://governance.aave.com/` |
| AVAX | homepage → `https://www.avax.network/`<br>announcement → `https://www.linkedin.com/company/avalancheavax` · `carried_by` names no host (field absent) |
| FET | homepage → `https://www.superintelligence.io/`<br>announcement → `https://medium.com/fetch-ai`<br>carried_by root → `https://api.github.com/` |
| ENA | homepage → `https://www.ethena.fi/` · `carried_by` names no host (field absent) |
| TAO | homepage → `https://bittensor.com/`<br>carried_by root → `https://api.github.com/` |
| GRAM | homepage → `https://ton.org/` · `carried_by` names no host (field absent) |
| XRP | homepage → `https://ripple.com/currency/` · `carried_by` names no host (field absent) |
| ADA | homepage → `https://cardano.org/` · `carried_by` names no host (field absent) |
| TRX | homepage → `https://tron.network/`<br>announcement → `https://medium.com/tron-foundation` · `carried_by` names no host (field absent) |
| SOL | homepage → `https://solana.com/`<br>carried_by root → `https://forum.solana.com/` |
| BCH | homepage → `https://bch.info/` · `carried_by` names no host (field absent) |
| HYPE | homepage → `https://app.hyperliquid.xyz/trade` · `carried_by` names no host (канала у монеты §6a не устанавливает (HYPE: releases hyperli…) |
| SKY | homepage → `https://sky.money/`<br>carried_by root → `https://forum.skyeco.com/` |
| ETH | homepage → `https://www.ethereum.org/`<br>carried_by root → `https://blog.ethereum.org/` |
| HBAR | homepage → `https://www.hedera.com/`<br>announcement → `https://medium.com/hashgraph` · `carried_by` names no host (field absent) |
| XLM | homepage → `https://www.stellar.org/`<br>announcement → `https://stellarcommunity.org/`<br>announcement → `https://bitcointalk.org/index.php?topic=1428573.0` · `carried_by` names no host (field absent) |
| ALGO | homepage → `https://algorand.foundation/`<br>announcement → `https://medium.com/algorand`<br>announcement → `https://forum.algorand.org/`<br>carried_by root → `https://forum.algorand.co/` |
| BNB | homepage → `https://www.binance.com/?ref=37754157` · `carried_by` names no host (field absent) |
| ZEC | homepage → `https://z.cash/`<br>carried_by root → `https://forum.zcashcommunity.com/` |
| UNI | homepage → `https://uniswap.org/`<br>announcement → `https://uniswap.org/blog/`<br>carried_by root → `https://gov.uniswap.org/` |
| XMR | homepage → `https://www.getmonero.org/` · `carried_by` names no host (объявленный фьючерсный актив (fut:true): запись k:"x" без px…) |
| LIT | homepage → `https://lighter.xyz/` · `carried_by` names no host (канала у монеты §6a не устанавливает (HYPE: releases hyperli…) |
| MORPHO | homepage → `https://morpho.org/` · `carried_by` names no host (объявленный фьючерсный актив (fut:true): запись k:"x" без px…) |
| ARB | homepage → `https://arbitrum.io/` · `carried_by` names no host (объявленный фьючерсный актив (fut:true): journal/data пишет …) |

**B3: robots.txt, 46 candidate origins, 45 requests.** `https://forum.algorand.co`
cost none, because `https://forum.algorand.org/robots.txt` landed on it. Four origins answered
404 and so carry no restriction: `ondo.foundation`, `api.github.com`, `ton.org` and
`tron.network`. Two origins govern this client with `Disallow: /`: `www.linkedin.com` and
`forum.skyeco.com`, the latter being SKY's §6a lane host. `blog.chain.link/robots.txt` lands on
an HTML page at `chain.link/blog`, which carries no directive. `www.getmonero.org` serves only
Cloudflare's content-signals comment preamble, with no directive and no signal set.
`bitcointalk.org` serves a lone `Sitemap:` line.

| Candidate origin | Read | HTTP (hops) | Landed | Governing group | Rule lines in it | `Sitemap:` lines | Basis |
|---|---|---|---|---|---:|---|---|
| `https://sui.io` | r031 | 301 → 200 | `https://www.sui.io/robots.txt` | `*` | 2 | `https://sui.io/sitemap.xml`<br>`https://www.sui.io/sitemap.xml` | parsed: 15 group(s), governing group *, 2 rule line(s) |
| `https://forums.sui.io` | r032 | 200 | `https://forums.sui.io/robots.txt` | `*` | 15 | `https://forums.sui.io/sitemap.xml` | parsed: 7 group(s), governing group *, 15 rule line(s) |
| `https://ondo.foundation` | r033 | 404 | `https://ondo.foundation/robots.txt` | `none` | 0 | — | RFC 9309 2.3.1.3: robots.txt absent (HTTP 404) -> no restriction |
| `https://chain.link` | r034 | 200 | `https://chain.link/robots.txt` | `*` | 16 | `https://chain.link/sitemap.xml` | parsed: 1 group(s), governing group *, 16 rule line(s) |
| `https://blog.chain.link` | r035 | 301 → 103 → 200 | `https://chain.link/blog` | `none` | 0 | — | parsed: 0 group(s), governing group none, 0 rule line(s) |
| `http://renderfoundation.com` | r036 | 308 → 200 | `https://renderfoundation.com/robots.txt` | `*` | 1 | `https://renderfoundation.com/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://medium.com` | r037 | 200 | `https://medium.com/robots.txt` | `*` | 20 | `https://medium.com/sitemap/sitemap.xml` | parsed: 2 group(s), governing group *, 20 rule line(s) |
| `https://near.org` | r038 | 307 → 200 | `https://www.near.org/robots.txt` | `*` | 2 | `https://www.near.org/sitemap.xml` | parsed: 8 group(s), governing group *, 2 rule line(s) |
| `https://gov.near.org` | r039 | 200 | `https://gov.near.org/robots.txt` | `*` | 16 | — | parsed: 8 group(s), governing group *, 16 rule line(s) |
| `https://yearn.fi` | r040 | 200 | `https://yearn.fi/robots.txt` | `*` | 10 | `https://yearn.fi/sitemap.xml` | parsed: 1 group(s), governing group *, 10 rule line(s) |
| `https://aave.com` | r041 | 200 | `https://aave.com/robots.txt` | `*` | 7 | `https://aave.com/sitemap.xml`<br>`https://aave.com/docs/sitemap.xml` | parsed: 3 group(s), governing group *, 7 rule line(s) |
| `https://governance.aave.com` | r042 | 200 | `https://governance.aave.com/robots.txt` | `*` | 15 | `https://governance.aave.com/sitemap.xml` | parsed: 7 group(s), governing group *, 15 rule line(s) |
| `https://www.avax.network` | r043 | 301 → 200 | `https://www.avalanche.com/robots.txt` | `*` | 1 | `https://www.avax.network/sitemap-index.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://www.linkedin.com` | r044 | 200 | `https://www.linkedin.com/robots.txt` | `*` | 1 | — | parsed: 77 group(s), governing group *, 1 rule line(s) |
| `https://www.superintelligence.io` | r045 | 301 → 200 | `https://superintelligence.io/robots.txt` | `*` | 0 | — | parsed: 1 group(s), governing group *, 0 rule line(s) |
| `https://api.github.com` | r046 | 404 | `https://api.github.com/robots.txt` | `none` | 0 | — | RFC 9309 2.3.1.3: robots.txt absent (HTTP 404) -> no restriction |
| `https://www.ethena.fi` | r047 | 308 → 200 | `https://ethena.fi/robots.txt` | `*` | 3 | `https://ethena.fi/sitemap.xml` | parsed: 13 group(s), governing group *, 3 rule line(s) |
| `https://bittensor.com` | r048 | 308 → 200 | `https://www.bittensor.com/robots.txt` | `*` | 2 | `https://www.bittensor.com/sitemap.xml` | parsed: 1 group(s), governing group *, 2 rule line(s) |
| `https://ton.org` | r049 | 404 | `https://ton.org/robots.txt` | `none` | 0 | — | RFC 9309 2.3.1.3: robots.txt absent (HTTP 404) -> no restriction |
| `https://ripple.com` | r050 | 200 | `https://ripple.com/robots.txt` | `*` | 4 | `https://ripple.com/sitemap.xml` | parsed: 1 group(s), governing group *, 4 rule line(s) |
| `https://cardano.org` | r051 | 200 | `https://cardano.org/robots.txt` | `*` | 1 | `https://cardano.org/sitemap.xml`<br>`https://cardano.org/de/sitemap.xml`<br>`https://cardano.org/ja/sitemap.xml`<br>`https://cardano.org/es/sitemap.xml`<br>`https://cardano.org/vi/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://tron.network` | r052 | 404 | `https://tron.network/robots.txt` | `none` | 0 | — | RFC 9309 2.3.1.3: robots.txt absent (HTTP 404) -> no restriction |
| `https://solana.com` | r053 | 200 | `https://solana.com/robots.txt` | `*` | 1 | `https://solana.com/sitemap.xml`<br>`https://solana.com/news/sitemap-news.xml`<br>`https://solana.com/podcasts/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://forum.solana.com` | r054 | 200 | `https://forum.solana.com/robots.txt` | `*` | 15 | `https://forum.solana.com/sitemap.xml` | parsed: 7 group(s), governing group *, 15 rule line(s) |
| `https://bch.info` | r055 | 200 | `https://bch.info/robots.txt` | `*` | 1 | — | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://app.hyperliquid.xyz` | r056 | 200 | `https://app.hyperliquid.xyz/robots.txt` | `*` | 10 | — | parsed: 1 group(s), governing group *, 10 rule line(s) |
| `https://sky.money` | r057 | 200 | `https://sky.money/robots.txt` | `*` | 1 | `https://sky.money/sitemap.xml` | parsed: 11 group(s), governing group *, 1 rule line(s) |
| `https://forum.skyeco.com` | r058 | 200 | `https://forum.skyeco.com/robots.txt` | `*` | 1 | — | parsed: 2 group(s), governing group *, 1 rule line(s) |
| `https://www.ethereum.org` | r059 | 301 → 200 | `https://ethereum.org/robots.txt` | `*` | 1 | `https://ethereum.org/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://blog.ethereum.org` | r060 | 200 | `https://blog.ethereum.org/robots.txt` | `*` | 1 | `https://blog.ethereum.org/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://www.hedera.com` | r061 | 301 → 200 | `https://hedera.com/robots.txt` | `*` | 1 | `https://hedera.com/sitemap_index.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://www.stellar.org` | r062 | 308 → 200 | `https://stellar.org/robots.txt` | `*` | 23 | — | parsed: 1 group(s), governing group *, 23 rule line(s) |
| `https://stellarcommunity.org` | r063 | 301 → 200 | `https://galactictalk.org/robots.txt` | `*` | 1 | `https://galactictalk.org/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://bitcointalk.org` | r064 | 200 | `https://bitcointalk.org/robots.txt` | `none` | 0 | `https://bitcointalk.org/sitemap.php` | parsed: 0 group(s), governing group none, 0 rule line(s) |
| `https://algorand.foundation` | r065 | 301 → 200 | `https://algorand.co/robots.txt` | `*` | 5 | — | parsed: 1 group(s), governing group *, 5 rule line(s) |
| `https://forum.algorand.org` | r066 | 301 → 200 | `https://forum.algorand.co/robots.txt` | `*` | 15 | `https://forum.algorand.co/sitemap.xml` | parsed: 7 group(s), governing group *, 15 rule line(s) |
| `https://forum.algorand.co` | r066 *(landing of https://forum.algorand.org/robots.txt)* | 301 → 200 | `https://forum.algorand.co/robots.txt` | `*` | 15 | `https://forum.algorand.co/sitemap.xml` | parsed: 7 group(s), governing group *, 15 rule line(s) (landing of https://forum.algorand.org/robots.txt) |
| `https://www.binance.com` | r067 | 200 | `https://www.binance.com/robots.txt` | `*` | 28 | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Trade_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Nft_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Futures_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Earn_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Loan_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Market_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Default_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Fiat_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Crypto_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Square_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Academy_New_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Muses_index.xml`<br>`https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Growth_index.xml` | parsed: 3 group(s), governing group *, 28 rule line(s) |
| `https://z.cash` | r068 | 200 | `https://z.cash/robots.txt` | `*` | 2 | `https://z.cash/sitemap.xml` | parsed: 1 group(s), governing group *, 2 rule line(s) |
| `https://forum.zcashcommunity.com` | r069 | 200 | `https://forum.zcashcommunity.com/robots.txt` | `*` | 15 | `https://forum.zcashcommunity.com/sitemap.xml` | parsed: 7 group(s), governing group *, 15 rule line(s) |
| `https://uniswap.org` | r070 | 200 | `https://uniswap.org/robots.txt` | `*` | 1 | `https://uniswap.org/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://gov.uniswap.org` | r071 | 200 | `https://gov.uniswap.org/robots.txt` | `*` | 15 | `https://gov.uniswap.org/sitemap.xml` | parsed: 7 group(s), governing group *, 15 rule line(s) |
| `https://www.getmonero.org` | r072 | 200 | `https://www.getmonero.org/robots.txt` | `none` | 0 | — | parsed: 0 group(s), governing group none, 0 rule line(s) |
| `https://lighter.xyz` | r073 | 200 | `https://lighter.xyz/robots.txt` | `*` | 1 | `https://lighter.xyz/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://morpho.org` | r074 | 200 | `https://morpho.org/robots.txt` | `*` | 1 | `https://morpho.org/sitemap.xml` | parsed: 1 group(s), governing group *, 1 rule line(s) |
| `https://arbitrum.io` | r075 | 200 | `https://arbitrum.io/robots.txt` | `*` | 3 | `https://arbitrum.io/sitemap.xml` | parsed: 1 group(s), governing group *, 3 rule line(s) |

**B4: 54 candidate pages.** 52 were read and 2 were refused on permission. **18 advertised feeds
were found on 11 pages and all 18 were read.** No origin advertised more than two, so the
two-per-host cap never bound. No candidate page was itself a feed.

| Candidate page | Robots | Read | HTTP (hops) | Bytes | Content type | Landed | Advertised RSS/Atom feeds → read |
|---|---|---|---|---:|---|---|---|
| `https://sui.io/` | allow — `Allow: /` | r076 | 301 → 103 → 200 | 380936 | `text/html; charset=utf-8` | `https://www.sui.io/` | `https://www.sui.io/blog/rss.xml` → r077 (read) |
| `https://forums.sui.io/` | allow | r078 | 200 | 21108 | `text/html; charset=utf-8` | `https://forums.sui.io/` | none |
| `https://ondo.foundation/` | allow | r079 | 200 | 24183 | `text/html; charset=utf-8` | `https://ondo.foundation/` | none |
| `https://chain.link/` | allow | r080 | 103 → 200 | 416896 | `text/html; charset=utf-8` | `https://chain.link/` | none |
| `https://blog.chain.link/` | allow | r081 | 301 → 103 → 200 | 354988 | `text/html; charset=utf-8` | `https://chain.link/blog` | none |
| `http://renderfoundation.com/` | allow — `Allow: /` | r082 | 308 → 200 | 217817 | `text/html` | `https://renderfoundation.com/` | none |
| `https://medium.com/render-token` | allow | r083 | 403 **refused (challenge, HTTP 403)** | 5018 | `text/html; charset=UTF-8` | `https://medium.com/render-token` | none |
| `https://near.org/` | allow — `Allow: /` | r084 | 307 → 200 | 153100 | `text/html; charset=utf-8` | `https://www.near.org/` | none |
| `https://near.org/blog/` | allow — `Allow: /` | r085 | 307 → 308 → 200 | 65304 | `text/html; charset=utf-8` | `https://www.near.org/blog` | none |
| `https://medium.com/nearprotocol` | allow | r086 | 403 **refused (challenge, HTTP 403)** | 5018 | `text/html; charset=UTF-8` | `https://medium.com/nearprotocol` | none |
| `https://gov.near.org/` | allow | r087 | 200 | 21893 | `text/html; charset=utf-8` | `https://gov.near.org/` | none |
| `https://yearn.fi/` | allow — `Allow: /` | r088 | 200 | 70806 | `text/html; charset=utf-8` | `https://yearn.fi/` | none |
| `https://medium.com/iearn` | allow | r089 | 403 **refused (challenge, HTTP 403)** | 5018 | `text/html; charset=UTF-8` | `https://medium.com/iearn` | none |
| `https://aave.com/` | allow — `Allow: /` | r090 | 200 | 113269 | `text/html; charset=utf-8` | `https://aave.com/` | none |
| `https://governance.aave.com/` | allow | r091 | 200 | 76928 | `text/html; charset=utf-8` | `https://governance.aave.com/` | `https://governance.aave.com/posts.rss` → r092 (read)<br>`https://governance.aave.com/latest.rss` → r093 (read) |
| `https://www.avax.network/` | allow — `Allow: /` | r094 | 301 → 200 | 216874 | `text/html; charset=utf-8` | `https://www.avalanche.com/` | none |
| `https://www.linkedin.com/company/avalancheavax` | disallow — `Disallow: /` | — | **refused on permission** | | | | — |
| `https://www.superintelligence.io/` | allow | r095 | 301 → 200 | 196939 | `text/html; charset=UTF-8` | `https://superintelligence.io/` | `https://superintelligence.io/feed/` → r096 (read)<br>`https://superintelligence.io/comments/feed/` → r097 (read) |
| `https://medium.com/fetch-ai` | allow | r098 | 403 **refused (challenge, HTTP 403)** | 5018 | `text/html; charset=UTF-8` | `https://medium.com/fetch-ai` | none |
| `https://api.github.com/` | allow | r099 | 200 | 2396 | `application/json; charset=utf-8` | `https://api.github.com/` | none |
| `https://www.ethena.fi/` | allow — `Allow: /` | r100 | 308 → 200 | 108381 | `text/html; charset=utf-8` | `https://ethena.fi/` | none |
| `https://bittensor.com/` | allow — `Allow: /` | r101 | 308 → 200 | 18708 | `text/html; charset=utf-8` | `https://www.bittensor.com/` | none |
| `https://ton.org/` | allow | r102 | 200 | 1437359 | `text/html` | `https://ton.org/` | none |
| `https://ripple.com/currency/` | allow — `Allow: /` | r103 | 308 → 200 | 302815 | `text/html; charset=utf-8` | `https://ripple.com/products/cross-border-payments/` | none |
| `https://cardano.org/` | allow — `Allow: /` | r104 | 200 | 44613 | `text/html; charset=UTF-8` | `https://cardano.org/` | `https://cardano.org/news/rss.xml` → r105 (read)<br>`https://cardano.org/news/atom.xml` → r106 (read) |
| `https://tron.network/` | allow | r107 | 200 | 7728 | `text/html` | `https://tron.network/` | none |
| `https://medium.com/tron-foundation` | allow | r108 | 403 **refused (challenge, HTTP 403)** | 5018 | `text/html; charset=UTF-8` | `https://medium.com/tron-foundation` | none |
| `https://solana.com/` | allow — `Allow: /` | r109 | 200 | 936863 | `text/html; charset=utf-8` | `https://solana.com/` | none |
| `https://forum.solana.com/` | allow | r110 | 200 | 18259 | `text/html; charset=utf-8` | `https://forum.solana.com/` | none |
| `https://bch.info/` | allow | r111 | 301 → 200 | 61263 | `text/html; charset=UTF-8` | `https://bch.info/_/` | none |
| `https://app.hyperliquid.xyz/trade` | allow — `Allow: /` | r112 | 200 | 6845 | `text/html` | `https://app.hyperliquid.xyz/trade` | none |
| `https://sky.money/` | allow — `allow: /` | r113 | 103 → 200 | 140499 | `text/html; charset=utf-8` | `https://sky.money/` | none |
| `https://forum.skyeco.com/` | disallow — `Disallow: /` | — | **refused on permission** | | | | — |
| `https://www.ethereum.org/` | allow — `Allow: /` | r114 | 301 → 200 | 322930 | `text/html; charset=utf-8` | `https://ethereum.org/` | none |
| `https://blog.ethereum.org/` | allow — `Allow: /` | r115 | 200 | 791575 | `text/html; charset=utf-8` | `https://blog.ethereum.org/` | `https://blog.ethereum.org/en/feed.xml` → r116 (read) |
| `https://www.hedera.com/` | allow | r117 | 301 → 200 | 463158 | `text/html; charset=UTF-8` | `https://hedera.com/` | `https://hedera.com/feed/` → r118 (read)<br>`https://hedera.com/comments/feed/` → r119 (read) |
| `https://medium.com/hashgraph` | allow | r120 | 403 **refused (challenge, HTTP 403)** | 5018 | `text/html; charset=UTF-8` | `https://medium.com/hashgraph` | none |
| `https://www.stellar.org/` | allow | r121 | 308 → 200 | 695437 | `text/html; charset=utf-8` | `https://stellar.org/` | none |
| `https://stellarcommunity.org/` | allow — `Allow: /` | r122 | 301 → 200 | 119745 | `text/html; charset=utf-8` | `https://galactictalk.org/` | none |
| `https://bitcointalk.org/index.php?topic=1428573.0` | allow | r123 | 200 | 166524 | `text/html; charset=ISO-8859-1` | `https://bitcointalk.org/index.php?topic=1428573.0` | `https://bitcointalk.org/index.php?type=rss;action=.xml` → r124 (read) |
| `https://algorand.foundation/` | allow | r125 | 301 → 103 → 200 | 320175 | `text/html; charset=UTF-8` | `https://algorand.co/` | none |
| `https://medium.com/algorand` | allow | r126 | 403 **refused (challenge, HTTP 403)** | 5018 | `text/html; charset=UTF-8` | `https://medium.com/algorand` | none |
| `https://forum.algorand.org/` | allow | r127 | 301 → 200 | 16554 | `text/html; charset=utf-8` | `https://forum.algorand.co/` | none |
| `https://forum.algorand.co/` | allow | r128 | 200 | 16554 | `text/html; charset=utf-8` | `https://forum.algorand.co/` | none |
| `https://www.binance.com/?ref=37754157` | allow — `Allow: /` | r129 | 202 | 0 | `text/html; charset=UTF-8` | `https://www.binance.com/?ref=37754157` | none |
| `https://z.cash/` | allow | r130 | 200 | 588900 | `text/html; charset=UTF-8` | `https://z.cash/` | `https://z.cash/feed/` → r131 (read)<br>`https://z.cash/comments/feed/` → r132 (read) |
| `https://forum.zcashcommunity.com/` | allow | r133 | 200 | 86862 | `text/html; charset=utf-8` | `https://forum.zcashcommunity.com/` | `https://forum.zcashcommunity.com/posts.rss` → r134 (read)<br>`https://forum.zcashcommunity.com/latest.rss` → r135 (read) |
| `https://uniswap.org/` | allow — `Allow: /` | r136 | 302 → 200 | 87110 | `text/html; charset=utf-8` | `https://app.uniswap.org/` | none |
| `https://uniswap.org/blog/` | allow — `Allow: /` | r137 | 302 → 200 | 87110 | `text/html; charset=utf-8` | `https://app.uniswap.org/` | none |
| `https://gov.uniswap.org/` | allow | r138 | 200 | 79732 | `text/html; charset=utf-8` | `https://gov.uniswap.org/` | `https://gov.uniswap.org/posts.rss` → r139 (read)<br>`https://gov.uniswap.org/latest.rss` → r140 (read) |
| `https://www.getmonero.org/` | allow | r141 | 200 | 33593 | `text/html` | `https://www.getmonero.org/` | `https://www.getmonero.org/feed.xml` → r142 (read) |
| `https://lighter.xyz/` | allow — `Allow: /` | r143 | 200 | 2034548 | `text/html` | `https://lighter.xyz/` | none |
| `https://morpho.org/` | allow | r144 | 200 | 550949 | `text/html; charset=utf-8` | `https://morpho.org/` | none |
| `https://arbitrum.io/` | allow — `Allow: /` | r145 | 403 **refused (challenge, HTTP 403)** | 5317 | `text/html; charset=UTF-8` | `https://arbitrum.io/` | none |

Every `medium.com` publication page, seven in all, and `arbitrum.io` answered a **managed
challenge**: HTTP 403 with Cloudflare's challenge platform in the body. Medium's sitemap index
answered the same client 200. Four Discourse roots advertise no RSS: `forums.sui.io`,
`gov.near.org`, `forum.solana.com` and `forum.algorand.co`. They serve a 16–22 KB application
shell whose only `alternate` link is `type="text/markdown"` → `/latest.md`. The saved bodies
were re-read to rule out a parser miss: `governance.aave.com`'s 77 KB page carries both RSS
links, and the parser took both.

**B5–B7: lanes, classes and the screen, one block per coin.** A lane is one feed read or one
urlset read. An index contributes the children it selected, at most three whose path carries a
keyword, newest `lastmod` first. The class vocabulary is B6's: `dated`, `undated`, and beside
them, as read, `no channel`, `refused` and `refused on permission`. A 404 is recorded as
`no channel (HTTP 404)`. `bitcointalk.org`'s advertised feed answered 400 with the body
«action=.xml is disabled due to slowness…», and is recorded as `no channel (HTTP 400)`. The
last column counts the records B7 found dated D−2…D. D is the UTC day in A3's `move`, which is
never recomputed (inv. 38).

| Coin · move (state, verbatim) · D | Lane (as landed) | Kind · via | B6 class | Considered / carrying a date | Distinct days | Window, UTC days | B7 | Records dated D−2…D |
|---|---|---|---|---|---:|---|---|---|
| **SUI** · +9.55% 2026-09-03 · D = 2026-09-03 | `https://www.sui.io/blog/rss.xml` | feed · advertised | dated | 100 / 100 | 83 | 2025-10-30 … 2026-09-24 | carried | 4 (2026-09-02) |
|  | `https://www.sui.io/sitemap.xml` *(requested `https://sui.io/sitemap.xml`)* | sitemap · declared | dated | 572 of 641 (keyword paths) / 572 | 22 | 2026-07-10 … 2026-09-21 | carried | 3 (2026-09-02, 2026-09-03) |
|  | `https://www.sui.io/sitemap.xml` | sitemap · declared | dated | 572 of 641 (keyword paths) / 572 | 22 | 2026-07-10 … 2026-09-21 | carried | 3 (2026-09-02, 2026-09-03) |
|  | `https://forums.sui.io/sitemap.xml` | sitemap · declared | no channel (index: 2 entries, 0 keyword children) | — |  | — … — | - |  |
| **ONDO** · +14.04% 2026-09-17 · D = 2026-09-17 | `https://ondo.foundation/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (HTTP 404) | — |  | — … — | - |  |
| **LINK** · +6.89% 2026-09-18 · D = 2026-09-18 | `https://chain.link/sitemap.xml` | sitemap · declared | dated | 371 of 1325 (keyword paths) / 371 | 33 | 2026-03-27 … 2026-09-18 | carried | 2 (2026-09-18) |
|  | `https://blog.chain.link/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (not a sitemap: text/html; charset=utf-8) | — |  | — … — | - |  |
| **RENDER** · +10.02% 2026-09-17 · D = 2026-09-17 | `https://renderfoundation.com/sitemap.xml` | sitemap · declared | undated | 2 of 52 (keyword paths) / 0 | 0 | — … — | - |  |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 319 of 12317 (keyword paths) / 319 | 20 | 2026-08-13 … 2026-09-20 | carried | 2 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 360 of 14283 (keyword paths) / 360 | 22 | 2026-07-24 … 2026-09-20 | carried | 1 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | undated · *Medium platform index — 0 URLs under this coin's publication path* | 403 of 16093 (keyword paths) / 403 | 1 | 2026-09-24 … 2026-09-24 | - |  |
| **NEAR** · +26.30% 2026-09-18 · D = 2026-09-18 | `https://www.near.org/sitemap.xml` | sitemap · declared | undated · placeholder comment: «lastmod values are placeholders dated 2026-08-15; generate them at build time.» | 1 of 13 (keyword paths) / 1 | 1 | 2026-08-15 … 2026-08-15 | - |  |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 319 of 12317 (keyword paths) / 319 | 20 | 2026-08-13 … 2026-09-20 | carried | 2 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 360 of 14283 (keyword paths) / 360 | 22 | 2026-07-24 … 2026-09-20 | carried | 1 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | undated · *Medium platform index — 0 URLs under this coin's publication path* | 403 of 16093 (keyword paths) / 403 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://gov.near.org/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (index: 3 entries, 0 keyword children) | — |  | — … — | - |  |
| **YFI** · +6.48% 2026-09-18 · D = 2026-09-18 | `https://yearn.fi/sitemap.xml` | sitemap · declared | undated | 1549 of 1549 (all) / 1549 | 1 | 2026-09-25 … 2026-09-25 | - |  |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 319 of 12317 (keyword paths) / 319 | 20 | 2026-08-13 … 2026-09-20 | carried | 2 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 360 of 14283 (keyword paths) / 360 | 22 | 2026-07-24 … 2026-09-20 | carried | 1 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | undated · *Medium platform index — 0 URLs under this coin's publication path* | 403 of 16093 (keyword paths) / 403 | 1 | 2026-09-24 … 2026-09-24 | - |  |
| **AAVE** · +11.99% 2026-09-17 · D = 2026-09-17 | `https://aave.com/sitemap.xml` | sitemap · declared | dated | 56 of 130 (keyword paths) / 55 | 52 | 2025-06-12 … 2026-09-15 | carried | 1 (2026-09-15) |
|  | `https://aave.com/docs/sitemap.xml` | sitemap · declared | undated | 102 of 102 (all) / 102 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://governance.aave.com/posts.rss` | feed · advertised | dated | 50 / 50 | 9 | 2026-09-16 … 2026-09-25 | carried | 7 (2026-09-16, 2026-09-17) |
|  | `https://governance.aave.com/latest.rss` | feed · advertised | dated | 30 / 30 | 10 | 2026-09-11 … 2026-09-25 | carried | 11 (2026-09-15, 2026-09-16, 2026-09-17) |
|  | `https://governance.aave.com/sitemap.xml` | sitemap · declared | no channel (index: 2 entries, 0 keyword children) | — |  | — … — | - |  |
| **AVAX** · +18.67% 2026-09-19 · D = 2026-09-19 | `https://www.avax.network/sitemap-index.xml` | sitemap · declared | no channel (index: 1 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.linkedin.com/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | refused on permission | — |  | — … — | - |  |
| **FET** · +11.98% 2026-09-17 · D = 2026-09-17 | `https://superintelligence.io/feed/` | feed · advertised | dated | 10 / 10 | 10 | 2025-08-20 … 2026-06-23 | not carried | 0 |
|  | `https://superintelligence.io/comments/feed/` | feed · advertised | undated | 0 / 0 | 0 | — … — | - |  |
|  | `https://superintelligence.io/wp-sitemap-posts-post-1.xml` | sitemap · child of `https://www.superintelligence.io/sitemap.xml` | undated | 1 of 35 (keyword paths) / 1 | 1 | 2025-04-23 … 2025-04-23 | - |  |
|  | `https://superintelligence.io/wp-sitemap-posts-page-1.xml` | sitemap · child of `https://www.superintelligence.io/sitemap.xml` | undated | 1 of 22 (keyword paths) / 1 | 1 | 2025-04-24 … 2025-04-24 | - |  |
|  | `https://superintelligence.io/wp-sitemap-posts-portfolio-1.xml` | sitemap · child of `https://www.superintelligence.io/sitemap.xml` | dated | 11 of 11 (all) / 11 | 2 | 2025-04-23 … 2025-04-24 | not carried | 0 |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 319 of 12317 (keyword paths) / 319 | 20 | 2026-08-13 … 2026-09-20 | carried | 2 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 360 of 14283 (keyword paths) / 360 | 22 | 2026-07-24 … 2026-09-20 | carried | 1 (2026-09-16) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | undated · *Medium platform index — 0 URLs under this coin's publication path* | 403 of 16093 (keyword paths) / 403 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://api.github.com/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (HTTP 404) | — |  | — … — | - |  |
| **ENA** · +20.92% 2026-09-19 · D = 2026-09-19 | `https://ethena.fi/sitemap.xml` | sitemap · declared | dated | 86 of 89 (keyword paths) / 85 | 28 | 2025-11-21 … 2026-09-03 | not carried | 0 |
| **TAO** · +10.25% 2026-09-22 · D = 2026-09-22 | `https://www.bittensor.com/sitemap.xml` | sitemap · declared | undated | 16 of 737 (keyword paths) / 0 | 0 | — … — | - |  |
|  | `https://api.github.com/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (HTTP 404) | — |  | — … — | - |  |
| **GRAM** · -6.17% 2026-09-01 · D = 2026-09-01 | `https://ton.org/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (HTTP 404) | — |  | — … — | - |  |
| **XRP** · -9.62% 2026-09-16 · D = 2026-09-16 | `https://ripple.com/sitemap/press-release.xml` | sitemap · child of `https://ripple.com/sitemap.xml` | undated | 235 of 235 (keyword paths) / 235 | 1 | 2026-09-22 … 2026-09-22 | - |  |
|  | `https://ripple.com/sitemap/post.xml` | sitemap · child of `https://ripple.com/sitemap.xml` | dated | 641 of 641 (keyword paths) / 641 | 2 | 2026-09-22 … 2026-09-25 | window short | 0 |
| **ADA** · +13.52% 2026-09-03 · D = 2026-09-03 | `https://cardano.org/news/rss.xml` | feed · advertised | dated | 20 / 20 | 17 | 2026-07-16 … 2026-09-04 | carried | 1 (2026-09-02) |
|  | `https://cardano.org/news/atom.xml` | feed · advertised | dated | 20 / 20 | 17 | 2026-07-16 … 2026-09-04 | carried | 1 (2026-09-02) |
|  | `https://cardano.org/sitemap.xml` | sitemap · declared | dated | 465 of 841 (keyword paths) / 460 | 33 | 2024-03-30 … 2026-09-11 | not carried | 0 |
|  | `https://cardano.org/de/sitemap.xml` | sitemap · declared | dated | 8 of 176 (keyword paths) / 6 | 5 | 2026-03-17 … 2026-07-31 | not carried | 0 |
|  | `https://cardano.org/ja/sitemap.xml` | sitemap · declared | dated | 8 of 176 (keyword paths) / 6 | 5 | 2026-03-17 … 2026-07-31 | not carried | 0 |
|  | `https://cardano.org/es/sitemap.xml` | sitemap · declared | dated | 8 of 176 (keyword paths) / 6 | 5 | 2026-03-17 … 2026-07-31 | not carried | 0 |
|  | `https://cardano.org/vi/sitemap.xml` | sitemap · declared | dated | 8 of 176 (keyword paths) / 6 | 5 | 2026-03-17 … 2026-07-31 | not carried | 0 |
| **TRX** · -3.12% 2026-09-01 · D = 2026-09-01 | `https://tron.network/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (HTTP 404) | — |  | — … — | - |  |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 319 of 12317 (keyword paths) / 319 | 20 | 2026-08-13 … 2026-09-20 | carried | 4 (2026-08-30, 2026-08-31, 2026-09-01) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 360 of 14283 (keyword paths) / 360 | 22 | 2026-07-24 … 2026-09-20 | not carried | 0 |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | undated · *Medium platform index — 0 URLs under this coin's publication path* | 403 of 16093 (keyword paths) / 403 | 1 | 2026-09-24 … 2026-09-24 | - |  |
| **SOL** · +10.19% 2026-09-18 · D = 2026-09-18 | `https://solana.com/sitemap.xml` | sitemap · declared | dated | 6404 of 18409 (keyword paths) / 6194 | 288 | 2018-04-18 … 2026-09-25 | carried | 19 (2026-09-16) |
|  | `https://solana.com/news/sitemap-news.xml` | sitemap · declared | dated | 10 of 10 (keyword paths) / 10 | 8 | 2026-09-07 … 2026-09-24 | carried | 1 (2026-09-16) |
|  | `https://solana.com/podcasts/sitemap.xml` | sitemap · declared | dated | 44 of 1276 (keyword paths) / 44 | 44 | 2023-03-24 … 2026-09-21 | not carried | 0 |
|  | `https://forum.solana.com/sitemap.xml` | sitemap · declared | no channel (index: 2 entries, 0 keyword children) | — |  | — … — | - |  |
| **BCH** · -12.26% 2026-09-10 · D = 2026-09-10 | `https://bch.info/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (HTTP 404) | — |  | — … — | - |  |
| **HYPE** · нет структурной строки · D = — | `https://app.hyperliquid.xyz/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | no channel (not a sitemap: text/html) | — |  | — … — | - |  |
| **SKY** · +16.69% 2026-09-18 · D = 2026-09-18 | `https://sky.money/sitemap.xml` | sitemap · declared | dated | 13 of 21 (keyword paths) / 13 | 7 | 2026-08-10 … 2026-09-11 | not carried | 0 |
|  | `https://forum.skyeco.com/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | refused on permission | — |  | — … — | - |  |
| **ETH** · +5.33% 2026-09-11 · D = 2026-09-11 | `https://ethereum.org/sitemap.xml` | sitemap · declared | no channel (index: 25 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://blog.ethereum.org/en/feed.xml` | feed · advertised | dated | 639 / 639 | 597 | 2013-12-31 … 2026-09-09 | carried | 1 (2026-09-09) |
|  | `https://blog.ethereum.org/sitemap.xml` | sitemap · declared | no channel (index: 1 entries, 0 keyword children) | — |  | — … — | - |  |
| **HBAR** · +9.93% 2026-09-03 · D = 2026-09-03 | `https://hedera.com/feed/` | feed · advertised | dated | 10 / 10 | 10 | 2026-07-08 … 2026-09-24 | not carried | 0 |
|  | `https://hedera.com/comments/feed/` | feed · advertised | undated | 0 / 0 | 0 | — … — | - |  |
|  | `https://hedera.com/post-sitemap.xml` | sitemap · child of `https://hedera.com/sitemap_index.xml` | dated | 587 of 587 (keyword paths) / 587 | 60 | 2024-12-04 … 2026-09-24 | not carried | 0 |
|  | `https://hedera.com/post_tag-sitemap.xml` | sitemap · child of `https://hedera.com/sitemap_index.xml` | dated | 17 of 17 (keyword paths) / 17 | 11 | 2025-12-08 … 2026-09-24 | not carried | 0 |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 319 of 12317 (keyword paths) / 319 | 20 | 2026-08-13 … 2026-09-20 | carried | 1 (2026-09-01) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 360 of 14283 (keyword paths) / 360 | 22 | 2026-07-24 … 2026-09-20 | carried | 2 (2026-09-02) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | undated · *Medium platform index — 0 URLs under this coin's publication path* | 403 of 16093 (keyword paths) / 403 | 1 | 2026-09-24 … 2026-09-24 | - |  |
| **XLM** · -9.23% 2026-09-16 · D = 2026-09-16 | `https://stellar.org/sitemap.xml` *(requested `https://www.stellar.org/sitemap.xml`)* | sitemap · `/sitemap.xml`, none declared | dated | 702 of 1209 (keyword paths) / 677 | 73 | 2025-10-28 … 2026-09-24 | carried | 1 (2026-09-14) |
|  | `https://galactictalk.org/sitemap.xml` | sitemap · declared | no channel (HTTP 404) | — |  | — … — | - |  |
|  | `https://bitcointalk.org/index.php?type=rss;action=.xml` | feed · advertised | no channel (HTTP 400) | — |  | — … — | - |  |
|  | `https://bitcointalk.org/sitemap.php` | sitemap · declared | no channel (index: 8062 entries, 0 keyword children) | — |  | — … — | - |  |
| **ALGO** · +12.05% 2026-09-20 · D = 2026-09-20 | `https://algorand.co/sitemap.xml` *(requested `https://algorand.foundation/sitemap.xml`)* | sitemap · `/sitemap.xml`, none declared | dated | 380 of 518 (keyword paths) / 380 | 147 | 2024-06-21 … 2026-09-17 | not carried | 0 |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 319 of 12317 (keyword paths) / 319 | 20 | 2026-08-13 … 2026-09-20 | carried | 1 (2026-09-20) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | dated · *Medium platform index — 0 URLs under this coin's publication path* | 360 of 14283 (keyword paths) / 360 | 22 | 2026-07-24 … 2026-09-20 | carried | 1 (2026-09-20) |
|  | `https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml` | sitemap · child of `https://medium.com/sitemap/sitemap.xml` | undated · *Medium platform index — 0 URLs under this coin's publication path* | 403 of 16093 (keyword paths) / 403 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://forum.algorand.co/sitemap.xml` | sitemap · declared | no channel (index: 2 entries, 0 keyword children) | — |  | — … — | - |  |
| **BNB** · +7.26% 2026-09-05 · D = 2026-09-05 | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Trade_index.xml` | sitemap · declared | no channel (index: 42 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_ja_0.xml` | sitemap · child of `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_index.xml` | undated | 1051 of 1051 (keyword paths) / 1051 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_lo-LA_0.xml` | sitemap · child of `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_index.xml` | undated | 2 of 2 (keyword paths) / 2 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_ru-UA_0.xml` | sitemap · child of `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_index.xml` | undated | 2197 of 2197 (keyword paths) / 2197 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Nft_index.xml` | sitemap · declared | no channel (index: 42 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_es-MX_1.xml` | sitemap · child of `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml` | undated | 5 of 1963 (keyword paths) / 5 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_ru_1.xml` | sitemap · child of `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml` | undated | 1071 of 3212 (keyword paths) / 1071 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en-KZ_1.xml` | sitemap · child of `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml` | undated | 89 of 2099 (keyword paths) / 89 | 1 | 2026-09-24 … 2026-09-24 | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Futures_index.xml` | sitemap · declared | no channel (index: 59 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Earn_index.xml` | sitemap · declared | no channel (index: 41 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Loan_index.xml` | sitemap · declared | no channel (index: 37 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Market_index.xml` | sitemap · declared | no channel (index: 42 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Default_index.xml` | sitemap · declared | no channel (index: 86 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Fiat_index.xml` | sitemap · declared | no channel (index: 42 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Crypto_index.xml` | sitemap · declared | no channel (index: 42 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Square_index.xml` | sitemap · declared | no channel (index: 40 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Academy_New_index.xml` | sitemap · declared | no channel (index: 41 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Muses_index.xml` | sitemap · declared | no channel (index: 37 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Growth_index.xml` | sitemap · declared | no channel (index: 160 entries, 0 keyword children) | — |  | — … — | - |  |
| **ZEC** · +18.14% 2026-09-17 · D = 2026-09-17 | `https://z.cash/feed/` | feed · advertised | dated | 10 / 10 | 9 | 2023-04-28 … 2023-06-14 | not carried | 0 |
|  | `https://z.cash/comments/feed/` | feed · advertised | undated | 0 / 0 | 0 | — … — | - |  |
|  | `https://z.cash/sitemap.xml` | sitemap · declared | dated | 49 of 570 (keyword paths) / 49 | 30 | 2016-01-21 … 2025-04-09 | not carried | 0 |
|  | `https://forum.zcashcommunity.com/posts.rss` | feed · advertised | dated | 50 / 50 | 2 | 2026-09-24 … 2026-09-25 | window short | 0 |
|  | `https://forum.zcashcommunity.com/latest.rss` | feed · advertised | dated | 30 / 30 | 7 | 2026-09-18 … 2026-09-25 | window short | 0 |
|  | `https://forum.zcashcommunity.com/sitemap.xml` | sitemap · declared | no channel (index: 3 entries, 0 keyword children) | — |  | — … — | - |  |
| **UNI** · +23.04% 2026-09-17 · D = 2026-09-17 | `https://uniswap.org/sitemap.xml` | sitemap · declared | no channel (index: 1 entries, 0 keyword children) | — |  | — … — | - |  |
|  | `https://gov.uniswap.org/posts.rss` | feed · advertised | dated | 50 / 50 | 36 | 2026-07-23 … 2026-09-23 | carried | 2 (2026-09-15, 2026-09-16) |
|  | `https://gov.uniswap.org/latest.rss` | feed · advertised | dated | 30 / 30 | 23 | 2026-03-06 … 2026-09-18 | not carried | 0 |
|  | `https://gov.uniswap.org/sitemap.xml` | sitemap · declared | no channel (index: 2 entries, 0 keyword children) | — |  | — … — | - |  |
| **XMR** · нет структурной строки · D = — | `https://www.getmonero.org/feed.xml` | feed · advertised | dated | 20 / 20 | 11 | 2025-07-25 … 2026-07-21 | no move recorded |  |
|  | `https://www.getmonero.org/sitemap.xml` | sitemap · `/sitemap.xml`, none declared | dated | 39 of 611 (keyword paths) / 39 | 6 | 2020-09-14 … 2025-09-01 | no move recorded |  |
| **LIT** · нет структурной строки · D = — | `https://lighter.xyz/sitemap.xml` | sitemap · declared | undated | 2 of 14 (keyword paths) / 0 | 0 | — … — | - |  |
| **MORPHO** · нет структурной строки · D = — | `https://morpho.org/sitemap.xml` | sitemap · declared | dated | 112 of 159 (keyword paths) / 112 | 102 | 2023-06-14 … 2026-09-24 | no move recorded |  |
| **ARB** · нет структурной строки · D = — | `https://arbitrum.io/sitemap.xml` | sitemap · declared | refused (challenge, HTTP 403) | — |  | — … — | - |  |

**The three `medium.com` children are Medium's platform-wide post index, not a coin's
channel.** They reached seven coins because seven announcement URLs are Medium publications,
and B5 reads a candidate host's sitemap. **0 of their 12 317, 14 283 and 16 093 URLs lie under
any of the seven publication paths** (`/render-token`, `/nearprotocol`, `/iearn`, `/fetch-ai`,
`/tron-foundation`, `/hashgraph`, `/algorand`). Their `carried` therefore describes other
publishers' posts:

```
medium publication slugs per coin: {'RENDER': ['render-token'], 'NEAR': ['nearprotocol'], 'YFI': ['iearn'], 'FET': ['fetch-ai'], 'TRX': ['tron-foundation'], 'HBAR': ['hashgraph'], 'ALGO': ['algorand']}
r154 https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml urls=12317 keyword=319
    RENDER  slug render-token       URLs under the slug: all 0, keyword-considered 0
    NEAR    slug nearprotocol       URLs under the slug: all 0, keyword-considered 0
    YFI     slug iearn              URLs under the slug: all 0, keyword-considered 0
    FET     slug fetch-ai           URLs under the slug: all 0, keyword-considered 0
    TRX     slug tron-foundation    URLs under the slug: all 0, keyword-considered 0
    HBAR    slug hashgraph          URLs under the slug: all 0, keyword-considered 0
    ALGO    slug algorand           URLs under the slug: all 0, keyword-considered 0
    sample considered paths: ['/@hemantprajapati921136/ai-blog-e115c48ccb00', '/@spotlighterspost_52146/from-silent-myths-to-surgical-strik', '/@divinetusks/gen-x-y-stopped-posting-and-the-internet-got-w']
r155 https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml urls=14283 keyword=360
    RENDER  slug render-token       URLs under the slug: all 0, keyword-considered 0
    NEAR    slug nearprotocol       URLs under the slug: all 0, keyword-considered 0
    YFI     slug iearn              URLs under the slug: all 0, keyword-considered 0
    FET     slug fetch-ai           URLs under the slug: all 0, keyword-considered 0
    TRX     slug tron-foundation    URLs under the slug: all 0, keyword-considered 0
    HBAR    slug hashgraph          URLs under the slug: all 0, keyword-considered 0
    ALGO    slug algorand           URLs under the slug: all 0, keyword-considered 0
    sample considered paths: ['/@sushilaDevi/nvidias-ceo-just-joined-x-his-first-post-start', '/@rohangharate/update-e6ae48956fe9', '/@analytics.huimorgpt/ai-video-character-micro-expression-pr']
r156 https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml urls=16093 keyword=403
    RENDER  slug render-token       URLs under the slug: all 0, keyword-considered 0
    NEAR    slug nearprotocol       URLs under the slug: all 0, keyword-considered 0
    YFI     slug iearn              URLs under the slug: all 0, keyword-considered 0
    FET     slug fetch-ai           URLs under the slug: all 0, keyword-considered 0
    TRX     slug tron-foundation    URLs under the slug: all 0, keyword-considered 0
    HBAR    slug hashgraph          URLs under the slug: all 0, keyword-considered 0
    ALGO    slug algorand           URLs under the slug: all 0, keyword-considered 0
    sample considered paths: ['/@3stans.rundown/a-chatbot-nearly-sent-troops-onto-a-chinese', '/@aadilamanat44/building-a-dynamic-filter-system-in-postgres', '/@gout_news/gout-season-️-campaign-tasks-deadlines-e1992298b']
```

**Per coin, the dated lanes that carried the move.** The coin summary is this report's own
aggregation, because B7 is defined per lane. It reads `carried` if any dated lane carried, then
`window short`, then `not carried`, otherwise `no dated lane`. Coins without a parseable move
are `no move recorded`. The first summary column leaves out Medium's platform index for the
reason above. The second counts it in, and marks in bold where that changes the word.

| Coin | Site (homepage host) | Dated lanes that carried the move (without Medium's platform index) | Coin summary | With Medium's platform index |
|---|---|---|---|---|
| SUI | `sui.io` | `https://www.sui.io/blog/rss.xml`<br>`https://www.sui.io/sitemap.xml` | carried | carried |
| ONDO | `ondo.foundation` | — | no dated lane | no dated lane |
| LINK | `chain.link` | `https://chain.link/sitemap.xml` | carried | carried |
| RENDER | `renderfoundation.com` | — | no dated lane | **carried** |
| NEAR | `near.org` | — | no dated lane | **carried** |
| YFI | `yearn.fi` | — | no dated lane | **carried** |
| AAVE | `aave.com` | `https://aave.com/sitemap.xml`<br>`https://governance.aave.com/latest.rss`<br>`https://governance.aave.com/posts.rss` | carried | carried |
| AVAX | `www.avax.network` | — | no dated lane | no dated lane |
| FET | `www.superintelligence.io` | — | not carried | **carried** |
| ENA | `www.ethena.fi` | — | not carried | not carried |
| TAO | `bittensor.com` | — | no dated lane | no dated lane |
| GRAM | `ton.org` | — | no dated lane | no dated lane |
| XRP | `ripple.com` | — | window short | window short |
| ADA | `cardano.org` | `https://cardano.org/news/atom.xml`<br>`https://cardano.org/news/rss.xml` | carried | carried |
| TRX | `tron.network` | — | no dated lane | **carried** |
| SOL | `solana.com` | `https://solana.com/news/sitemap-news.xml`<br>`https://solana.com/sitemap.xml` | carried | carried |
| BCH | `bch.info` | — | no dated lane | no dated lane |
| HYPE | `app.hyperliquid.xyz` | — | no move recorded | no move recorded |
| SKY | `sky.money` | — | not carried | not carried |
| ETH | `www.ethereum.org` | `https://blog.ethereum.org/en/feed.xml` | carried | carried |
| HBAR | `www.hedera.com` | — | not carried | **carried** |
| XLM | `www.stellar.org` | `https://stellar.org/sitemap.xml` | carried | carried |
| ALGO | `algorand.foundation` | — | not carried | **carried** |
| BNB | `www.binance.com` | — | no dated lane | no dated lane |
| ZEC | `z.cash` | — | window short | window short |
| UNI | `uniswap.org` | `https://gov.uniswap.org/posts.rss` | carried | carried |
| XMR | `www.getmonero.org` | — | no move recorded | no move recorded |
| LIT | `lighter.xyz` | — | no move recorded | no move recorded |
| MORPHO | `morpho.org` | — | no move recorded | no move recorded |
| ARB | `arbitrum.io` | — | no move recorded | no move recorded |

Tally without Medium's platform index: `{"carried": 8, "no dated lane": 10, "not carried": 5, "window short": 2, "no move recorded": 5}`. With it: `{"carried": 15, "no dated lane": 6, "not carried": 2, "window short": 2, "no move recorded": 5}`.

### Stage C — Reporter feeds

Rule 4 held on all four paths: the `*` group of each host has no line matching the feed's path.

| Feed | Robots (group · decision · matching lines) | Read | HTTP (hops) | Bytes | Content type | Landed | Items | Dated | Window (UTC) |
|---|---|---|---|---:|---|---|---:|---:|---|
| `https://www.coindesk.com/arc/outboundfeeds/rss/` | robots r229 · `*` · allow · no line matches the path | r230 | 308 → 200 | 30822 | `application/xml` | `https://www.coindesk.com/arc/outboundfeeds/rss` | 25 | 25 | 2026-09-24T11:20Z … 2026-09-25T09:59Z |
| `https://www.theblock.co/rss.xml` | robots r231 · `*` · allow · no line matches the path | r232 | 200 | 29564 | `text/xml; charset=UTF-8` | `https://www.theblock.co/rss.xml` | 19 | 19 | 2026-09-23T13:00Z … 2026-09-25T11:00Z |
| `https://decrypt.co/feed` | robots r233 · `*` · allow · no line matches the path | r234 | 200 | 38751 | `application/xml` | `https://decrypt.co/feed` | 35 | 35 | 2026-09-23T10:43Z … 2026-09-25T11:09Z |
| `https://cointelegraph.com/rss` | robots r235 · `*` · allow · no line matches the path | r236 | 200 | 52282 | `application/xml; charset=utf-8` | `https://cointelegraph.com/rss` | 30 | 30 | 2026-09-24T04:52Z … 2026-09-25T11:11Z |

Per-feed windows are **22.7 h** (CoinDesk), **46.0 h** (The Block), **48.4 h** (Decrypt) and
**30.3 h** (Cointelegraph). The **union window is 2026-09-23T10:43:46Z to
2026-09-25T11:11:33Z, 48.46 h**. All 109 items carry a date.

**List yield: 14 titles.** A title is taken when it names an A2 symbol as a whole uppercase word
(case-sensitive), or the coin's B1 `name` as a whole word (case-insensitive). Only one title
matched by symbol, Cointelegraph's `ONDO`. The rest matched by name. `(name)` marks a
name-only match.

| Feed | Date (UTC) | Matched | Title (≤ 100 characters) |
|---|---|---|---|
| cointelegraph.com | 2026-09-24T13:00Z | SOL(name) | Solana Foundation hires ex-Binance CMO and payments exec as new partnerships expand |
| cointelegraph.com | 2026-09-24T20:04Z | HYPE(name) | DoubleZero brings dedicated fiber market data to Hyperliquid traders |
| cointelegraph.com | 2026-09-24T20:32Z | ONDO | Bitcoin price steadies, ONDO rallies as US Treasury yields hit 2007 highs |
| cointelegraph.com | 2026-09-25T04:41Z | ZEC(name) | Researchers propose Zcash-style private Bitcoin transfers without a soft fork |
| decrypt.co | 2026-09-23T18:15Z | MORPHO(name) | Borrow Against Your Bitcoin at a Fixed Rate: Coinbase Expands Morpho Loans |
| decrypt.co | 2026-09-23T19:36Z | ZEC(name) | Zcash's Wall Street Moment Reaches Europe With Its First ETP Listing |
| decrypt.co | 2026-09-24T13:03Z | SOL(name) | Solana Foundation Hires Binance's Former Global CMO for Institutional Push |
| decrypt.co | 2026-09-25T09:50Z | ZEC(name) | Researchers Publish 'Zcash-Style' Design for Private Bitcoin Transfers |
| www.coindesk.com | 2026-09-24T13:00Z | SOL(name) | Solana Foundation hires Binance, Polygon veterans as it ramps up tokenized finance push |
| www.coindesk.com | 2026-09-24T20:13Z | ONDO(name) | Someone was trying to sell Ondo Finance after founder Nathan Allman's death |
| www.theblock.co | 2026-09-24T13:00Z | SOL(name) | Solana Foundation taps Binance, Polygon vets to drive institutional adoption and payments |
| www.theblock.co | 2026-09-24T14:27Z | ONDO(name) | Ondo launches onchain portfolio tokens based on BlackRock-developed strategies |
| www.theblock.co | 2026-09-24T19:17Z | SOL(name) | Solana treasury firm SkyAI keeps board after shareholder protest, loses equity plan vote |
| www.theblock.co | 2026-09-25T11:00Z | ENA(name) | Ethena expands USDe backing strategy into bStocks and equity perpetuals on Binance |

**Book yield: 15 titles** name the base of an `x` row ending in `USDT` as a whole uppercase word,
over 728 such bases. Per base: `BTC` 3, `US` 3, `GENIUS` 2, `S` 2, `ARK` 2, `IBM` 2, `A` 1,
`Q` 1, `ONDO` 1. **4 titles name the crypto asset they matched**: `BTC` three times and `ONDO`
once. **2 name IBM, the company**, which is also the base of an `x` row. **9 match only through
word collisions**: `GENIUS` (the Act), `S` and `US` (the country), `ARK` (ARK Invest), `A`
(«Series A») and `Q` («Q-Day»). `analyst/live.json` was read by command and never whole: top-level keys
`ts, src, n, c, x`; its own timestamp field `ts` = `2026-09-25T01:28:17+04:00`; the first `x`
row's keys `highPrice, openTime, volume, count, symbol, lastId, priceChange, firstId, openPrice,
weightedAvgPrice, lastQty, closeTime, lowPrice, lastPrice, priceChangePercent, quoteVolume`; 776
`x` rows.

```
READ r229 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r229 -D /tmp/tz52/hdr/r229 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.coindesk.com/robots.txt' -> 200 4345 text/plain https://www.coindesk.com/robots.txt (exit 0) 0.1s
READ r230 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r230 -D /tmp/tz52/hdr/r230 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.coindesk.com/arc/outboundfeeds/rss/' -> 200 30822 application/xml https://www.coindesk.com/arc/outboundfeeds/rss (exit 0) 0.1s
READ r231 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r231 -D /tmp/tz52/hdr/r231 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.theblock.co/robots.txt' -> 200 890 text/plain; charset=utf-8 https://www.theblock.co/robots.txt (exit 0) 0.0s
READ r232 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r232 -D /tmp/tz52/hdr/r232 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.theblock.co/rss.xml' -> 200 29564 text/xml; charset=UTF-8 https://www.theblock.co/rss.xml (exit 0) 0.0s
READ r233 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r233 -D /tmp/tz52/hdr/r233 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://decrypt.co/robots.txt' -> 200 160 text/plain; charset=UTF-8 https://decrypt.co/robots.txt (exit 0) 0.2s
READ r234 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r234 -D /tmp/tz52/hdr/r234 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://decrypt.co/feed' -> 200 38751 application/xml https://decrypt.co/feed (exit 0) 0.0s
READ r235 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r235 -D /tmp/tz52/hdr/r235 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cointelegraph.com/robots.txt' -> 200 384 text/plain https://cointelegraph.com/robots.txt (exit 0) 0.0s
READ r236 [C] curl -sS -L -m 20 -o /tmp/tz52/body/r236 -D /tmp/tz52/hdr/r236 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cointelegraph.com/rss' -> 200 52282 application/xml; charset=utf-8 https://cointelegraph.com/rss (exit 0) 0.0s
C https://www.coindesk.com/arc/outboundfeeds/rss/ -> ok items=25 dated=25 window 2026-09-24T11:20:12+00:00 .. 2026-09-25T09:59:45+00:00
C https://www.theblock.co/rss.xml -> ok items=19 dated=19 window 2026-09-23T13:00:00+00:00 .. 2026-09-25T11:00:00+00:00
C https://decrypt.co/feed -> ok items=35 dated=35 window 2026-09-23T10:43:46+00:00 .. 2026-09-25T11:09:52+00:00
C https://cointelegraph.com/rss -> ok items=30 dated=30 window 2026-09-24T04:52:40+00:00 .. 2026-09-25T11:11:33+00:00
C list yield 14 titles; book yield 15 titles over 728 USDT bases
C live.json top keys ['ts', 'src', 'n', 'c', 'x']; ts fields {'ts': '2026-09-25T01:28:17+04:00'}; first x keys ['highPrice', 'openTime', 'volume', 'count', 'symbol', 'lastId', 'priceChange', 'firstId', 'openPrice', 'weightedAvgPrice', 'lastQty', 'closeTime', 'lowPrice', 'lastPrice', 'priceChangePercent', 'quoteVolume']
C union window 2026-09-23T10:43:46+00:00 .. 2026-09-25T11:11:33+00:00
C attempted 4 feeds; reported 4
```

### Stage D — Upbit's documented market list

One read, `r237`: 200, 243 205 bytes, `application/json;charset=UTF-8`.

| Reading | Value |
|---|---|
| markets | 855, every one carrying `market_event` |
| `KRW-` markets | 289 |
| `KRW-` bases that are A2 symbols | 23: AAVE, ADA, ALGO, ARB, AVAX, BCH, ENA, ETH, HBAR, LINK, LIT, MORPHO, NEAR, ONDO, RENDER, SKY, SOL, SUI, TAO, TRX, UNI, XLM, XRP |
| A2 symbols with no `KRW-` market | 7: BNB, FET, GRAM, HYPE, XMR, YFI, ZEC |
| `KRW-` bases that are bases of `x` rows | 225, of 728 `USDT` bases |
| `market_event.warning` true | 18 markets |
| `market_event.caution.GLOBAL_PRICE_DIFFERENCES` true | 171 |
| `market_event.caution.TRADING_VOLUME_SOARING` true | 15 |
| `market_event.caution.DEPOSIT_AMOUNT_SOARING` true | 15 |
| `market_event.caution.PRICE_FLUCTUATIONS` true | 13 |
| `market_event.caution.CONCENTRATION_OF_SMALL_ACCOUNTS` true | 0 |
| A2 symbols carrying either | GRAM (`USDT-GRAM`: `GLOBAL_PRICE_DIFFERENCES`) · RENDER (`USDT-RENDER`: `GLOBAL_PRICE_DIFFERENCES`) · ENA (`BTC-ENA`: `GLOBAL_PRICE_DIFFERENCES`) · MORPHO (`KRW-MORPHO`: `TRADING_VOLUME_SOARING`) · LIT (`BTC-LIT`: `GLOBAL_PRICE_DIFFERENCES`); none carries `warning` |

Upbit's own `english_name` for the symbols most open to a ticker collision: `LIT` «Lighter»
(the asset `main.py` names, not Litentry), `GRAM` «Gram», `SKY` «Sky Protocol» and `XLM`
«Lumen». The names are Upbit's. No identity beyond the name was checked.

```
D {"rec": "r237", "outcome": "ok", "caution_keys": ["CONCENTRATION_OF_SMALL_ACCOUNTS", "DEPOSIT_AMOUNT_SOARING", "GLOBAL_PRICE_DIFFERENCES", "PRICE_FLUCTUATIONS", "TRADING_VOLUME_SOARING"], "a2_markets": {"BCH": ["BTC-BCH (Bitcoin Cash)", "KRW-BCH (Bitcoin Cash)", "USDT-BCH (Bitcoin Cash)"], "GRAM": ["USDT-GRAM (Gram)", "BTC-GRAM (Gram)"], "RENDER": ["USDT-RENDER (Render Token)", "BTC-RENDER (Render Token)", "KRW-RENDER (Render Token)"], "SKY": ["BTC-SKY (Sky Protocol)", "KRW-SKY (Sky Protocol)", "USDT-SKY (Sky Protocol)"], "ALGO": ["KRW-ALGO (Algorand)", "BTC-ALGO (Algorand)"], "UNI": ["KRW-UNI (Uniswap)", "BTC-UNI (Uniswap)", "USDT-UNI (Uniswap)"], "HBAR": ["KRW-HBAR (Hedera)"], "AAVE": ["KRW-AAVE (Aave)", "BTC-AAVE (Aave)"], "TRX": ["KRW-TRX (TRON)", "BTC-TRX (TRON)", "USDT-TRX (TRON)"], "SUI": ["BTC-SUI (Sui)", "KRW-SUI (Sui)"], "NEAR": ["USDT-NEAR (NEAR Protocol)", "KRW-NEAR (NEAR Protocol)", "BTC-NEAR (NEAR Protocol)"], "SOL": ["BTC-SOL (Solana)", "USDT-SOL (Solana)", "KRW-SOL (Solana)"], "ETH": ["KRW-ETH (Ethereum)", "BTC-ETH (Ethereum)", "USDT-ETH (Ethereum)"], "ARB": ["KRW-ARB (Arbitrum)", "BTC-ARB (Arbitrum)"], "LIT": ["KRW-LIT (Lighter)", "BTC-LIT (Lighter)", "USDT-LIT (Lighter)"], "AVAX": ["KRW-AVAX (Avalanche)", "BTC-AVAX (Avalanche)"], "ONDO": ["USDT-ONDO (Ondo Finance)", "KRW-ONDO (Ondo Finance)", "BTC-ONDO (Ondo Finance)"], "XLM": ["KRW-XLM (Lumen)", "BTC-XLM (Lumen)", "USDT-XLM (Lumen)"], "TAO": ["USDT-TAO (Bittensor)", "BTC-TAO (Bittensor)", "KRW-TAO (Bittensor)"], "LINK": ["KRW-LINK (Chainlink)", "BTC-LINK (Chainlink)"], "XRP": ["KRW-XRP (XRP)", "BTC-XRP (XRP)", "USDT-XRP (XRP)"], "ENA": ["KRW-ENA (Ethena)", "BTC-ENA (Ethena)", "USDT-ENA (Ethena)"], "MORPHO": ["BTC-MORPHO (Morpho)", "USDT-MORPHO (Morpho)", "KRW-MORPHO (Morpho)"], "ADA": ["USDT-ADA (Ada)", "BTC-ADA (Ada)", "KRW-ADA (Ada)"]}, "markets": 855, "krw": 289, "krw_in_a2": 23, "krw_a2": ["AAVE", "ADA", "ALGO", "ARB", "AVAX", "BCH", "ENA", "ETH", "HBAR", "LINK", "LIT", "MORPHO", "NEAR", "ONDO", "RENDER", "SKY", "SOL", "SUI", "TAO", "TRX", "UNI", "XLM", "XRP"], "a2_not_krw": ["BNB", "FET", "GRAM", "HYPE", "XMR", "YFI", "ZEC"], "krw_in_x": 225, "x_bases": 728, "warning": 18, "caution": {"GLOBAL_PRICE_DIFFERENCES": 171, "TRADING_VOLUME_SOARING": 15, "PRICE_FLUCTUATIONS": 13, "DEPOSIT_AMOUNT_SOARING": 15, "CONCENTRATION_OF_SMALL_ACCOUNTS": 0}, "flagged": [{"market": "USDT-GRAM", "warning": false, "caution": ["GLOBAL_PRICE_DIFFERENCES"]}, {"market": "USDT-RENDER", "warning": false, "caution": ["GLOBAL_PRICE_DIFFERENCES"]}, {"market": "BTC-ENA", "warning": false, "caution": ["GLOBAL_PRICE_DIFFERENCES"]}, {"market": "KRW-MORPHO", "warning": false, "caution": ["TRADING_VOLUME_SOARING"]}, {"market": "BTC-LIT", "warning": false, "caution": ["GLOBAL_PRICE_DIFFERENCES"]}], "has_event": 855}
```

### Stage E — Publishers of record for scheduled systemic events

**E1 — Federal Register API**, one read, `r238`: 200, 19 528 bytes, `count` **10000**, 20
results.

| # | `publication_date` | `type` | `title`, first 100 characters |
|---:|---|---|---|
| 1 | 2026-09-25 | Notice | Self-Regulatory Organizations; NYSE Arca, Inc.; Notice of Filing and Immediate Effectiveness of Prop |
| 2 | 2026-09-25 | Notice | Self-Regulatory Organizations; NYSE Arca, Inc.; Notice of Filing and Immediate Effectiveness of a Pr |
| 3 | 2026-09-25 | Notice | Self-Regulatory Organizations; NYSE American LLC; Notice of Filing and Immediate Effectiveness of Pr |
| 4 | 2026-09-25 | Notice | Self-Regulatory Organizations; New York Stock Exchange LLC; Notice of Filing and Immediate Effective |
| 5 | 2026-09-25 | Notice | Self-Regulatory Organizations; NYSE National, Inc.; Notice of Filing and Immediate Effectiveness of  |
| 6 | 2026-09-25 | Notice | Self-Regulatory Organizations; NYSE Texas, Inc.; Notice of Filing and Immediate Effectiveness of Pro |
| 7 | 2026-09-25 | Notice | Self-Regulatory Organizations; New York Stock Exchange LLC; Notice of Filing and Immediate Effective |
| 8 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 9 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 10 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 11 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 12 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 13 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 14 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 15 | 2026-09-25 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 16 | 2026-09-24 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 17 | 2026-09-24 | Notice | Agency Information Collection Activities; Submission for OMB Review; Comment Request; Extension: Rul |
| 18 | 2026-09-24 | Notice | Self-Regulatory Organizations; Texas Stock Exchange LLC; Notice of Filing and Immediate Effectivenes |
| 19 | 2026-09-24 | Notice | Self-Regulatory Organizations; Nasdaq ISE, LLC; Notice of Designation of a Longer Period for Commiss |
| 20 | 2026-09-24 | Notice | Self-Regulatory Organizations; Cboe Exchange, Inc.; Notice of Designation of a Longer Period for Com |

Term counts over the 20 full titles:

| Term | Titles containing it |
|---|---:|
| `Longer Period` | 2 (case-sensitive and case-insensitive alike) |
| `Proceedings` | 1 (alike) |
| `Approving` | 0 (alike) — the one «Proceedings» title reads «…Whether To Approve or Disapprove…» |
| `Disapproving` | 0 (alike) |
| `bitcoin`, `crypto`, `digital asset`, `solana`, `xrp`, `trust` | 0 each, as substring and as whole word |
| `ether` | 1 as a substring, **0 as a whole word** — the hit is «Wh**ether**» at character 145 |

The 20 newest documents cover publication dates 2026-09-24 and 2026-09-25 only.

**E2 — SEC full-text search**, one URL in two forms:

| Form | Read | HTTP | Bytes | Content type | JSON | `hits.total.value` |
|---|---|---|---:|---|---|---:|
| (a) rule-1 form, exactly | `r239` | **403** | 4 819 | `text/html` | no | — |
| (b) rule-1 form + `-A "crypto-auto d***@yahoo.com"` | `r240` | **200** | 57 822 | `application/json` | yes | **1215** |

(a)'s body is SEC's own page. It is served by `AkamaiGHost`, titled «SEC.gov | Your Request
Originates from an Undeclared Automated Tool», and says: «Please declare your traffic by
updating your user agent to include company specific information.» The refusal is addressed
to the undeclared client and names what it wants, which is the Architect's reading. The
contact is printed masked everywhere: first character of the local part, `***@`, then the
domain.

```
READ r239 [E2a] curl -sS -L -m 20 -o /tmp/tz52/body/r239 -D /tmp/tz52/hdr/r239 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1' -> 403 4819 text/html https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1 (exit 0) 0.1s
READ r240 [E2b] curl -sS -L -m 20 -o /tmp/tz52/body/r240 -D /tmp/tz52/hdr/r240 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' -A "crypto-auto d***@yahoo.com" 'https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1' -> 200 57822 application/json https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1 (exit 0) 0.7s
E2 {"a": {"rec": "r239", "outcome": "refused (HTTP 403)", "code": "403", "bytes": "4819", "ctype": "text/html", "json": false}, "b": {"rec": "r240", "outcome": "ok", "code": "200", "bytes": "57822", "ctype": "application/json", "json": true, "hits_total": 1215}, "contact_masked": "d***@yahoo.com"}
```

### Stage F — Binance USDⓈ-M klines for the declared perpetuals

| Pair | Read | HTTP | Bytes | Content type | Rows | Fields per row | First element of the last row (open time, ISO UTC) |
|---|---|---|---:|---|---:|---:|---|
| `HYPEUSDT` | r241 | 200 | 437 | `application/json` | 3 | 12 | 2026-09-25T11:00:00Z |
| `XMRUSDT` | r242 | 200 | 388 | `application/json` | 3 | 12 | 2026-09-25T11:00:00Z |
| `LITUSDT` | r243 | 200 | 427 | `application/json` | 3 | 12 | 2026-09-25T11:00:00Z |
| `MORPHOUSDT` | r244 | 200 | 440 | `application/json` | 3 | 12 | 2026-09-25T11:00:00Z |
| `ARBUSDT` | r245 | 200 | 439 | `application/json` | 3 | 12 | 2026-09-25T11:00:00Z |

All five reads were made between 11:23:49Z and 11:23:54Z. The last row's open time,
**11:00:00Z, is therefore the hour that had not yet closed**. No price is printed. Each row has
the 12 fields Binance documents, and the first is the open time.

### Findings for the Architect

Measurements, not proposals. What each one decides is the Architect's (TZ §«What this TZ does
not decide»).

1. **NEAR's own site offers no dated channel to this client.** `www.near.org/sitemap.xml` holds
   13 URLs, all `lastmod` 2026-08-15, under a comment that says so: «lastmod values are
   placeholders dated 2026-08-15; generate them at build time.» `near.org/` and
   `near.org/blog/` advertise no feed. `medium.com/nearprotocol` answers a challenge.
   `gov.near.org`'s root advertises only `latest.md`, and its sitemap index names no keyword
   child. **So Stage B finds no dated lane for NEAR**, the coin whose miss opened this TZ.
2. **ONDO's registered homepage is not where it publishes.** CoinGecko gives
   `ondo.foundation`, whose robots.txt and `/sitemap.xml` both answer 404 and which advertises
   no feed. `ondo.finance/sitemap.xml`, read only for V2, is `dated`: 198 URLs, 186 with
   `lastmod`; 181 on keyword paths, 179 of them dated, across 167 distinct days; newest
   2026-09-24T12:30:00.000Z. It
   holds a record dated **2026-09-16, D−1 of the recorded move (+14.04 % on 2026-09-17)**, so
   by B7's rule it would read `carried`. It stays outside Stage B's table because no B2
   candidate names that host.
3. **Where a coin's own site carried its move**, the lane was a sitemap or an RSS/Atom feed:
   - SUI: `www.sui.io/blog/rss.xml`, 4 records on 09-02, and `www.sui.io/sitemap.xml`.
   - LINK: `chain.link/sitemap.xml`, 2 records on 09-18.
   - AAVE: `aave.com/sitemap.xml`, plus `governance.aave.com`'s `posts.rss` and `latest.rss`.
   - ADA: `cardano.org/news/rss.xml` and `atom.xml`.
   - SOL: `solana.com/sitemap.xml` and `/news/sitemap-news.xml`.
   - ETH: `blog.ethereum.org/en/feed.xml`.
   - XLM: `stellar.org/sitemap.xml`.
   - UNI: `gov.uniswap.org/posts.rss`.

   Three of these sit on hosts §6a already reads, in another form: AAVE's forum, ETH's blog feed
   and UNI's forum.
4. **`window short`** means the lane exists but its page does not reach back to the move.
   `ripple.com/sitemap/post.xml` restamps its records: its oldest `lastmod` is 2026-09-22.
   `forum.zcashcommunity.com`'s two feeds reach back only to 09-24 and 09-18.
5. **`not carried`, and where each lane's newest record stood**:
   - FET: `superintelligence.io/feed/`, newest 2026-06-23.
   - ENA: `ethena.fi/sitemap.xml`, newest 09-03, against a move on 09-19.
   - SKY: `sky.money/sitemap.xml`, newest 09-11, against 09-18.
   - HBAR: `hedera.com/feed/` and two sitemaps span the move, but hold nothing dated 09-01 to
     09-03.
   - ALGO: `algorand.co/sitemap.xml`, newest 09-17, against D−2 = 09-18.
6. **`undated` has two causes, and neither is a quiet channel.**
   - Stamps written at build or serve time, one value over the whole file:
     - `yearn.fi`: 1 549 URLs, all 2026-09-25, the day of the read.
     - `aave.com/docs`: all 09-24.
     - The six Binance `Blog` and `SupportAndAnnouncement` children: all 09-24.
     - `ripple.com/sitemap/press-release.xml`: all 09-22.
     - NEAR's placeholders.
   - No `lastmod` at all: `renderfoundation.com`, `bittensor.com` and `lighter.xyz`.
7. **B5's keyword rule selects no child from the most common index shapes met here.**
   - Discourse indexes name their children `sitemap_1.xml`, `sitemap_recent.xml` and
     `sitemap_2.xml`. This covers all seven forums read: Sui, NEAR, Aave, Solana, Algorand,
     Zcash and Uniswap.
   - `blog.ethereum.org`, `uniswap.org` and `www.avax.network` each index one `sitemap-0.xml`.
   - `ethereum.org` indexes 25 language files, and 13 of Binance's 15 indexes carry no keyword.

   Each of these reads `no channel` whatever its children hold. This is the TZ's rule, read
   as written.
8. **Refusals, as read.**
   - Managed challenges came from every `medium.com` page and from `arbitrum.io`'s page and
     sitemap.
   - `Disallow: /` for `*` came from `www.linkedin.com` and from `forum.skyeco.com`, SKY's §6a
     lane host (Pre-existing Issues 2).
   - `bitcointalk.org` disables its own advertised feed.
9. **The candidates are only as good as CoinGecko's `links`.**
   - BNB's homepage is a Binance referral URL, `?ref=37754157`, read as registered.
   - HYPE's is the trading application, `app.hyperliquid.xyz/trade`, and its `/sitemap.xml` is
     the application's HTML.
   - XRP's is `ripple.com/currency/`, which lands on a product page.
   - FET's is `superintelligence.io`, whose feed has been silent since 2026-06-23.
   - ONDO's is item 2.
10. **Stage E's two publishers answer this machine.** The Federal Register's 20 newest SEC
    documents span two publication days, so one page of that API is a one-to-two-day window.
    SEC's search answers a declared client and refuses an undeclared one, which the Architect's
    reading stated and this session reproduced.
11. **Stage F**: `fapi.binance.com` answers this session 200 on all five pairs. Contract hard
    floor item 9 (inv. 24) is about runners, and nothing here speaks to a runner. The last
    row of a `limit=3` read is the forming hour.

### Reading ledger

Every request of this session, in order. Each entry is a numbered read line in a fixed format:
id, UTC start, stage, command, then status with redirect hops, bytes, content type, landing URL
and curl's exit code. V4 checks it.

```
r001 2026-09-25T11:09:07Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r001 -D /tmp/tz52/hdr/r001 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/sui?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 4787 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/sui?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r002 2026-09-25T11:09:20Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r002 -D /tmp/tz52/hdr/r002 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/ondo-finance?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3113 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/ondo-finance?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r003 2026-09-25T11:09:32Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r003 -D /tmp/tz52/hdr/r003 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/chainlink?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 28921 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/chainlink?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r004 2026-09-25T11:09:45Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r004 -D /tmp/tz52/hdr/r004 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/render-token?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 4266 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/render-token?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r005 2026-09-25T11:09:58Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r005 -D /tmp/tz52/hdr/r005 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/near?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3337 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/near?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r006 2026-09-25T11:10:10Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r006 -D /tmp/tz52/hdr/r006 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/yearn-finance?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 8077 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/yearn-finance?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r007 2026-09-25T11:10:23Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r007 -D /tmp/tz52/hdr/r007 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/aave?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 7263 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/aave?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r008 2026-09-25T11:10:36Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r008 -D /tmp/tz52/hdr/r008 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/avalanche-2?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 2868 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/avalanche-2?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r009 2026-09-25T11:10:49Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r009 -D /tmp/tz52/hdr/r009 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/fetch-ai?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 6862 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/fetch-ai?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r010 2026-09-25T11:11:01Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r010 -D /tmp/tz52/hdr/r010 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/ethena?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 7846 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/ethena?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r011 2026-09-25T11:11:14Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r011 -D /tmp/tz52/hdr/r011 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/bittensor?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3111 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/bittensor?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r012 2026-09-25T11:11:27Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r012 -D /tmp/tz52/hdr/r012 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/the-open-network?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3650 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/the-open-network?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r013 2026-09-25T11:11:39Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r013 -D /tmp/tz52/hdr/r013 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/ripple?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3939 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/ripple?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r014 2026-09-25T11:11:52Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r014 -D /tmp/tz52/hdr/r014 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/cardano?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 10584 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/cardano?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r015 2026-09-25T11:12:05Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r015 -D /tmp/tz52/hdr/r015 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/tron?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 5312 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/tron?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r016 2026-09-25T11:12:18Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r016 -D /tmp/tz52/hdr/r016 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/solana?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 4457 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/solana?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r017 2026-09-25T11:12:30Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r017 -D /tmp/tz52/hdr/r017 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/bitcoin-cash?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3571 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/bitcoin-cash?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r018 2026-09-25T11:12:43Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r018 -D /tmp/tz52/hdr/r018 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/hyperliquid?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 2797 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/hyperliquid?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r019 2026-09-25T11:12:56Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r019 -D /tmp/tz52/hdr/r019 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/sky?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 4158 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/sky?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r020 2026-09-25T11:13:08Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r020 -D /tmp/tz52/hdr/r020 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/ethereum?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 5910 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/ethereum?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r021 2026-09-25T11:13:21Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r021 -D /tmp/tz52/hdr/r021 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/hedera-hashgraph?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3893 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/hedera-hashgraph?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r022 2026-09-25T11:13:34Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r022 -D /tmp/tz52/hdr/r022 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/stellar?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 4502 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/stellar?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r023 2026-09-25T11:13:47Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r023 -D /tmp/tz52/hdr/r023 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/algorand?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3867 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/algorand?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r024 2026-09-25T11:13:59Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r024 -D /tmp/tz52/hdr/r024 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/binancecoin?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 5864 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/binancecoin?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r025 2026-09-25T11:14:12Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r025 -D /tmp/tz52/hdr/r025 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/zcash?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 9683 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/zcash?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r026 2026-09-25T11:14:25Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r026 -D /tmp/tz52/hdr/r026 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/uniswap?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 6649 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/uniswap?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r027 2026-09-25T11:14:37Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r027 -D /tmp/tz52/hdr/r027 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/monero?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 8262 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/monero?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r028 2026-09-25T11:14:50Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r028 -D /tmp/tz52/hdr/r028 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/lighter?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 2689 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/lighter?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r029 2026-09-25T11:15:03Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r029 -D /tmp/tz52/hdr/r029 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/morpho?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 4250 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/morpho?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r030 2026-09-25T11:15:16Z [B1] curl -sS -L -m 20 -o /tmp/tz52/body/r030 -D /tmp/tz52/hdr/r030 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.coingecko.com/api/v3/coins/arbitrum?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false'
     -> status 200 (hops 200) | bytes 3803 | type application/json; charset=utf-8 | landed https://api.coingecko.com/api/v3/coins/arbitrum?localization=false&tickers=false&market_data=false&community_data=false&developer_data=false&sparkline=false | curl exit 0
r031 2026-09-25T11:15:32Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r031 -D /tmp/tz52/hdr/r031 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://sui.io/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 1248 | type text/plain; charset=utf-8 | landed https://www.sui.io/robots.txt | curl exit 0
r032 2026-09-25T11:15:32Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r032 -D /tmp/tz52/hdr/r032 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forums.sui.io/robots.txt'
     -> status 200 (hops 200) | bytes 1026 | type text/plain; charset=utf-8 | landed https://forums.sui.io/robots.txt | curl exit 0
r033 2026-09-25T11:15:32Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r033 -D /tmp/tz52/hdr/r033 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ondo.foundation/robots.txt'
     -> status 404 (hops 404) | bytes 21534 | type text/html; charset=utf-8 | landed https://ondo.foundation/robots.txt | curl exit 0
r034 2026-09-25T11:15:32Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r034 -D /tmp/tz52/hdr/r034 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://chain.link/robots.txt'
     -> status 200 (hops 200) | bytes 551 | type text/plain; charset=utf-8 | landed https://chain.link/robots.txt | curl exit 0
r035 2026-09-25T11:15:32Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r035 -D /tmp/tz52/hdr/r035 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://blog.chain.link/robots.txt'
     -> status 200 (hops 301 → 103 → 200) | bytes 354988 | type text/html; charset=utf-8 | landed https://chain.link/blog | curl exit 0
r036 2026-09-25T11:15:32Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r036 -D /tmp/tz52/hdr/r036 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'http://renderfoundation.com/robots.txt'
     -> status 200 (hops 308 → 200) | bytes 73 | type text/plain | landed https://renderfoundation.com/robots.txt | curl exit 0
r037 2026-09-25T11:15:33Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r037 -D /tmp/tz52/hdr/r037 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/robots.txt'
     -> status 200 (hops 200) | bytes 884 | type text/plain | landed https://medium.com/robots.txt | curl exit 0
r038 2026-09-25T11:15:33Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r038 -D /tmp/tz52/hdr/r038 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://near.org/robots.txt'
     -> status 200 (hops 307 → 200) | bytes 2267 | type text/plain; charset=utf-8 | landed https://www.near.org/robots.txt | curl exit 0
r039 2026-09-25T11:15:33Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r039 -D /tmp/tz52/hdr/r039 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.near.org/robots.txt'
     -> status 200 (hops 200) | bytes 842 | type text/plain; charset=utf-8 | landed https://gov.near.org/robots.txt | curl exit 0
r040 2026-09-25T11:15:33Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r040 -D /tmp/tz52/hdr/r040 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://yearn.fi/robots.txt'
     -> status 200 (hops 200) | bytes 273 | type text/plain; charset=utf-8 | landed https://yearn.fi/robots.txt | curl exit 0
r041 2026-09-25T11:15:33Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r041 -D /tmp/tz52/hdr/r041 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://aave.com/robots.txt'
     -> status 200 (hops 200) | bytes 2101 | type text/plain; charset=utf-8 | landed https://aave.com/robots.txt | curl exit 0
r042 2026-09-25T11:15:33Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r042 -D /tmp/tz52/hdr/r042 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://governance.aave.com/robots.txt'
     -> status 200 (hops 200) | bytes 1000 | type text/plain; charset=utf-8 | landed https://governance.aave.com/robots.txt | curl exit 0
r043 2026-09-25T11:15:34Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r043 -D /tmp/tz52/hdr/r043 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.avax.network/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 78 | type text/plain; charset=utf-8 | landed https://www.avalanche.com/robots.txt | curl exit 0
r044 2026-09-25T11:15:34Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r044 -D /tmp/tz52/hdr/r044 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.linkedin.com/robots.txt'
     -> status 200 (hops 200) | bytes 120190 | type text/plain | landed https://www.linkedin.com/robots.txt | curl exit 0
r045 2026-09-25T11:15:34Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r045 -D /tmp/tz52/hdr/r045 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.superintelligence.io/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 66 | type text/plain | landed https://superintelligence.io/robots.txt | curl exit 0
r046 2026-09-25T11:15:35Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r046 -D /tmp/tz52/hdr/r046 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.github.com/robots.txt'
     -> status 404 (hops 404) | bytes 106 | type application/json; charset=utf-8 | landed https://api.github.com/robots.txt | curl exit 0
r047 2026-09-25T11:15:35Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r047 -D /tmp/tz52/hdr/r047 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ethena.fi/robots.txt'
     -> status 200 (hops 308 → 200) | bytes 674 | type text/plain | landed https://ethena.fi/robots.txt | curl exit 0
r048 2026-09-25T11:15:35Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r048 -D /tmp/tz52/hdr/r048 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bittensor.com/robots.txt'
     -> status 200 (hops 308 → 200) | bytes 87 | type text/plain; charset=utf-8 | landed https://www.bittensor.com/robots.txt | curl exit 0
r049 2026-09-25T11:15:35Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r049 -D /tmp/tz52/hdr/r049 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ton.org/robots.txt'
     -> status 404 (hops 404) | bytes 555 | type text/html | landed https://ton.org/robots.txt | curl exit 0
r050 2026-09-25T11:15:35Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r050 -D /tmp/tz52/hdr/r050 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ripple.com/robots.txt'
     -> status 200 (hops 200) | bytes 173 | type text/plain; charset=utf-8 | landed https://ripple.com/robots.txt | curl exit 0
r051 2026-09-25T11:15:36Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r051 -D /tmp/tz52/hdr/r051 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/robots.txt'
     -> status 200 (hops 200) | bytes 241 | type text/plain; charset=UTF-8 | landed https://cardano.org/robots.txt | curl exit 0
r052 2026-09-25T11:15:36Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r052 -D /tmp/tz52/hdr/r052 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://tron.network/robots.txt'
     -> status 404 (hops 404) | bytes 7034 | type text/html | landed https://tron.network/robots.txt | curl exit 0
r053 2026-09-25T11:15:37Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r053 -D /tmp/tz52/hdr/r053 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://solana.com/robots.txt'
     -> status 200 (hops 200) | bytes 163 | type text/plain | landed https://solana.com/robots.txt | curl exit 0
r054 2026-09-25T11:15:37Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r054 -D /tmp/tz52/hdr/r054 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.solana.com/robots.txt'
     -> status 200 (hops 200) | bytes 997 | type text/plain; charset=utf-8 | landed https://forum.solana.com/robots.txt | curl exit 0
r055 2026-09-25T11:15:37Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r055 -D /tmp/tz52/hdr/r055 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bch.info/robots.txt'
     -> status 200 (hops 200) | bytes 23 | type text/plain; charset=UTF-8 | landed https://bch.info/robots.txt | curl exit 0
r056 2026-09-25T11:15:38Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r056 -D /tmp/tz52/hdr/r056 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://app.hyperliquid.xyz/robots.txt'
     -> status 200 (hops 200) | bytes 335 | type text/plain | landed https://app.hyperliquid.xyz/robots.txt | curl exit 0
r057 2026-09-25T11:15:38Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r057 -D /tmp/tz52/hdr/r057 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://sky.money/robots.txt'
     -> status 200 (hops 200) | bytes 384 | type text/plain; charset=utf-8 | landed https://sky.money/robots.txt | curl exit 0
r058 2026-09-25T11:15:38Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r058 -D /tmp/tz52/hdr/r058 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.skyeco.com/robots.txt'
     -> status 200 (hops 200) | bytes 80 | type text/plain; charset=utf-8 | landed https://forum.skyeco.com/robots.txt | curl exit 0
r059 2026-09-25T11:15:39Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r059 -D /tmp/tz52/hdr/r059 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ethereum.org/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 264 | type text/plain; charset=utf-8 | landed https://ethereum.org/robots.txt | curl exit 0
r060 2026-09-25T11:15:39Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r060 -D /tmp/tz52/hdr/r060 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://blog.ethereum.org/robots.txt'
     -> status 200 (hops 200) | bytes 126 | type text/plain; charset=UTF-8 | landed https://blog.ethereum.org/robots.txt | curl exit 0
r061 2026-09-25T11:15:39Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r061 -D /tmp/tz52/hdr/r061 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.hedera.com/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 184 | type text/plain; charset=utf-8 | landed https://hedera.com/robots.txt | curl exit 0
r062 2026-09-25T11:15:39Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r062 -D /tmp/tz52/hdr/r062 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.stellar.org/robots.txt'
     -> status 200 (hops 308 → 200) | bytes 914 | type text/plain; charset=UTF-8 | landed https://stellar.org/robots.txt | curl exit 0
r063 2026-09-25T11:15:40Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r063 -D /tmp/tz52/hdr/r063 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://stellarcommunity.org/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 70 | type text/plain;charset=UTF-8 | landed https://galactictalk.org/robots.txt | curl exit 0
r064 2026-09-25T11:15:40Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r064 -D /tmp/tz52/hdr/r064 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitcointalk.org/robots.txt'
     -> status 200 (hops 200) | bytes 45 | type text/plain | landed https://bitcointalk.org/robots.txt | curl exit 0
r065 2026-09-25T11:15:40Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r065 -D /tmp/tz52/hdr/r065 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://algorand.foundation/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 165 | type text/plain; charset=utf-8 | landed https://algorand.co/robots.txt | curl exit 0
r066 2026-09-25T11:15:40Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r066 -D /tmp/tz52/hdr/r066 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.algorand.org/robots.txt'
     -> status 200 (hops 301 → 200) | bytes 998 | type text/plain; charset=utf-8 | landed https://forum.algorand.co/robots.txt | curl exit 0
r067 2026-09-25T11:15:41Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r067 -D /tmp/tz52/hdr/r067 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/robots.txt'
     -> status 200 (hops 200) | bytes 6722 | type text/plain; charset=UTF-8 | landed https://www.binance.com/robots.txt | curl exit 0
r068 2026-09-25T11:15:42Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r068 -D /tmp/tz52/hdr/r068 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://z.cash/robots.txt'
     -> status 200 (hops 200) | bytes 104 | type text/plain; charset=utf-8 | landed https://z.cash/robots.txt | curl exit 0
r069 2026-09-25T11:15:42Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r069 -D /tmp/tz52/hdr/r069 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.zcashcommunity.com/robots.txt'
     -> status 200 (hops 200) | bytes 1005 | type text/plain; charset=utf-8 | landed https://forum.zcashcommunity.com/robots.txt | curl exit 0
r070 2026-09-25T11:15:43Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r070 -D /tmp/tz52/hdr/r070 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://uniswap.org/robots.txt'
     -> status 200 (hops 200) | bytes 114 | type text/plain; charset=utf-8 | landed https://uniswap.org/robots.txt | curl exit 0
r071 2026-09-25T11:15:43Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r071 -D /tmp/tz52/hdr/r071 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.uniswap.org/robots.txt'
     -> status 200 (hops 200) | bytes 996 | type text/plain; charset=utf-8 | landed https://gov.uniswap.org/robots.txt | curl exit 0
r072 2026-09-25T11:15:43Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r072 -D /tmp/tz52/hdr/r072 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.getmonero.org/robots.txt'
     -> status 200 (hops 200) | bytes 1248 | type text/plain; charset=utf-8 | landed https://www.getmonero.org/robots.txt | curl exit 0
r073 2026-09-25T11:15:44Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r073 -D /tmp/tz52/hdr/r073 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://lighter.xyz/robots.txt'
     -> status 200 (hops 200) | bytes 64 | type text/plain | landed https://lighter.xyz/robots.txt | curl exit 0
r074 2026-09-25T11:15:44Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r074 -D /tmp/tz52/hdr/r074 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://morpho.org/robots.txt'
     -> status 200 (hops 200) | bytes 64 | type text/plain | landed https://morpho.org/robots.txt | curl exit 0
r075 2026-09-25T11:15:44Z [B3] curl -sS -L -m 20 -o /tmp/tz52/body/r075 -D /tmp/tz52/hdr/r075 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://arbitrum.io/robots.txt'
     -> status 200 (hops 200) | bytes 98 | type text/plain; charset=utf-8 | landed https://arbitrum.io/robots.txt | curl exit 0
r076 2026-09-25T11:16:23Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r076 -D /tmp/tz52/hdr/r076 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://sui.io/'
     -> status 200 (hops 301 → 103 → 200) | bytes 380936 | type text/html; charset=utf-8 | landed https://www.sui.io/ | curl exit 0
r077 2026-09-25T11:16:23Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r077 -D /tmp/tz52/hdr/r077 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.sui.io/blog/rss.xml'
     -> status 200 (hops 200) | bytes 77247 | type application/rss+xml; charset=utf-8 | landed https://www.sui.io/blog/rss.xml | curl exit 0
r078 2026-09-25T11:16:23Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r078 -D /tmp/tz52/hdr/r078 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forums.sui.io/'
     -> status 200 (hops 200) | bytes 21108 | type text/html; charset=utf-8 | landed https://forums.sui.io/ | curl exit 0
r079 2026-09-25T11:16:23Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r079 -D /tmp/tz52/hdr/r079 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ondo.foundation/'
     -> status 200 (hops 200) | bytes 24183 | type text/html; charset=utf-8 | landed https://ondo.foundation/ | curl exit 0
r080 2026-09-25T11:16:23Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r080 -D /tmp/tz52/hdr/r080 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://chain.link/'
     -> status 200 (hops 103 → 200) | bytes 416896 | type text/html; charset=utf-8 | landed https://chain.link/ | curl exit 0
r081 2026-09-25T11:16:23Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r081 -D /tmp/tz52/hdr/r081 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://blog.chain.link/'
     -> status 200 (hops 301 → 103 → 200) | bytes 354988 | type text/html; charset=utf-8 | landed https://chain.link/blog | curl exit 0
r082 2026-09-25T11:16:24Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r082 -D /tmp/tz52/hdr/r082 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'http://renderfoundation.com/'
     -> status 200 (hops 308 → 200) | bytes 217817 | type text/html | landed https://renderfoundation.com/ | curl exit 0
r083 2026-09-25T11:16:24Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r083 -D /tmp/tz52/hdr/r083 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/render-token'
     -> status 403 (hops 403) | bytes 5018 | type text/html; charset=UTF-8 | landed https://medium.com/render-token | curl exit 0
r084 2026-09-25T11:16:24Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r084 -D /tmp/tz52/hdr/r084 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://near.org/'
     -> status 200 (hops 307 → 200) | bytes 153100 | type text/html; charset=utf-8 | landed https://www.near.org/ | curl exit 0
r085 2026-09-25T11:16:25Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r085 -D /tmp/tz52/hdr/r085 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://near.org/blog/'
     -> status 200 (hops 307 → 308 → 200) | bytes 65304 | type text/html; charset=utf-8 | landed https://www.near.org/blog | curl exit 0
r086 2026-09-25T11:16:25Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r086 -D /tmp/tz52/hdr/r086 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/nearprotocol'
     -> status 403 (hops 403) | bytes 5018 | type text/html; charset=UTF-8 | landed https://medium.com/nearprotocol | curl exit 0
r087 2026-09-25T11:16:26Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r087 -D /tmp/tz52/hdr/r087 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.near.org/'
     -> status 200 (hops 200) | bytes 21893 | type text/html; charset=utf-8 | landed https://gov.near.org/ | curl exit 0
r088 2026-09-25T11:16:26Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r088 -D /tmp/tz52/hdr/r088 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://yearn.fi/'
     -> status 200 (hops 200) | bytes 70806 | type text/html; charset=utf-8 | landed https://yearn.fi/ | curl exit 0
r089 2026-09-25T11:16:27Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r089 -D /tmp/tz52/hdr/r089 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/iearn'
     -> status 403 (hops 403) | bytes 5018 | type text/html; charset=UTF-8 | landed https://medium.com/iearn | curl exit 0
r090 2026-09-25T11:16:27Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r090 -D /tmp/tz52/hdr/r090 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://aave.com/'
     -> status 200 (hops 200) | bytes 113269 | type text/html; charset=utf-8 | landed https://aave.com/ | curl exit 0
r091 2026-09-25T11:16:27Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r091 -D /tmp/tz52/hdr/r091 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://governance.aave.com/'
     -> status 200 (hops 200) | bytes 76928 | type text/html; charset=utf-8 | landed https://governance.aave.com/ | curl exit 0
r092 2026-09-25T11:16:28Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r092 -D /tmp/tz52/hdr/r092 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://governance.aave.com/posts.rss'
     -> status 200 (hops 200) | bytes 441809 | type application/rss+xml; charset=utf-8 | landed https://governance.aave.com/posts.rss | curl exit 0
r093 2026-09-25T11:16:30Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r093 -D /tmp/tz52/hdr/r093 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://governance.aave.com/latest.rss'
     -> status 200 (hops 200) | bytes 285107 | type application/rss+xml; charset=utf-8 | landed https://governance.aave.com/latest.rss | curl exit 0
r094 2026-09-25T11:16:30Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r094 -D /tmp/tz52/hdr/r094 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.avax.network/'
     -> status 200 (hops 301 → 200) | bytes 216874 | type text/html; charset=utf-8 | landed https://www.avalanche.com/ | curl exit 0
r095 2026-09-25T11:16:30Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r095 -D /tmp/tz52/hdr/r095 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.superintelligence.io/'
     -> status 200 (hops 301 → 200) | bytes 196939 | type text/html; charset=UTF-8 | landed https://superintelligence.io/ | curl exit 0
r096 2026-09-25T11:16:33Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r096 -D /tmp/tz52/hdr/r096 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://superintelligence.io/feed/'
     -> status 200 (hops 200) | bytes 139118 | type application/rss+xml; charset=UTF-8 | landed https://superintelligence.io/feed/ | curl exit 0
r097 2026-09-25T11:16:34Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r097 -D /tmp/tz52/hdr/r097 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://superintelligence.io/comments/feed/'
     -> status 200 (hops 200) | bytes 842 | type application/rss+xml; charset=UTF-8 | landed https://superintelligence.io/comments/feed/ | curl exit 0
r098 2026-09-25T11:16:34Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r098 -D /tmp/tz52/hdr/r098 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/fetch-ai'
     -> status 403 (hops 403) | bytes 5018 | type text/html; charset=UTF-8 | landed https://medium.com/fetch-ai | curl exit 0
r099 2026-09-25T11:16:34Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r099 -D /tmp/tz52/hdr/r099 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.github.com/'
     -> status 200 (hops 200) | bytes 2396 | type application/json; charset=utf-8 | landed https://api.github.com/ | curl exit 0
r100 2026-09-25T11:16:34Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r100 -D /tmp/tz52/hdr/r100 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ethena.fi/'
     -> status 200 (hops 308 → 200) | bytes 108381 | type text/html; charset=utf-8 | landed https://ethena.fi/ | curl exit 0
r101 2026-09-25T11:16:35Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r101 -D /tmp/tz52/hdr/r101 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bittensor.com/'
     -> status 200 (hops 308 → 200) | bytes 18708 | type text/html; charset=utf-8 | landed https://www.bittensor.com/ | curl exit 0
r102 2026-09-25T11:16:35Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r102 -D /tmp/tz52/hdr/r102 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ton.org/'
     -> status 200 (hops 200) | bytes 1437359 | type text/html | landed https://ton.org/ | curl exit 0
r103 2026-09-25T11:16:35Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r103 -D /tmp/tz52/hdr/r103 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ripple.com/currency/'
     -> status 200 (hops 308 → 200) | bytes 302815 | type text/html; charset=utf-8 | landed https://ripple.com/products/cross-border-payments/ | curl exit 0
r104 2026-09-25T11:16:35Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r104 -D /tmp/tz52/hdr/r104 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/'
     -> status 200 (hops 200) | bytes 44613 | type text/html; charset=UTF-8 | landed https://cardano.org/ | curl exit 0
r105 2026-09-25T11:16:37Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r105 -D /tmp/tz52/hdr/r105 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/news/rss.xml'
     -> status 200 (hops 200) | bytes 33861 | type application/xml | landed https://cardano.org/news/rss.xml | curl exit 0
r106 2026-09-25T11:16:38Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r106 -D /tmp/tz52/hdr/r106 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/news/atom.xml'
     -> status 200 (hops 200) | bytes 36009 | type application/xml | landed https://cardano.org/news/atom.xml | curl exit 0
r107 2026-09-25T11:16:38Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r107 -D /tmp/tz52/hdr/r107 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://tron.network/'
     -> status 200 (hops 200) | bytes 7728 | type text/html | landed https://tron.network/ | curl exit 0
r108 2026-09-25T11:16:38Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r108 -D /tmp/tz52/hdr/r108 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/tron-foundation'
     -> status 403 (hops 403) | bytes 5018 | type text/html; charset=UTF-8 | landed https://medium.com/tron-foundation | curl exit 0
r109 2026-09-25T11:16:38Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r109 -D /tmp/tz52/hdr/r109 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://solana.com/'
     -> status 200 (hops 200) | bytes 936863 | type text/html; charset=utf-8 | landed https://solana.com/ | curl exit 0
r110 2026-09-25T11:16:39Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r110 -D /tmp/tz52/hdr/r110 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.solana.com/'
     -> status 200 (hops 200) | bytes 18259 | type text/html; charset=utf-8 | landed https://forum.solana.com/ | curl exit 0
r111 2026-09-25T11:16:40Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r111 -D /tmp/tz52/hdr/r111 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bch.info/'
     -> status 200 (hops 301 → 200) | bytes 61263 | type text/html; charset=UTF-8 | landed https://bch.info/_/ | curl exit 0
r112 2026-09-25T11:16:40Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r112 -D /tmp/tz52/hdr/r112 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://app.hyperliquid.xyz/trade'
     -> status 200 (hops 200) | bytes 6845 | type text/html | landed https://app.hyperliquid.xyz/trade | curl exit 0
r113 2026-09-25T11:16:41Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r113 -D /tmp/tz52/hdr/r113 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://sky.money/'
     -> status 200 (hops 103 → 200) | bytes 140499 | type text/html; charset=utf-8 | landed https://sky.money/ | curl exit 0
r114 2026-09-25T11:16:41Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r114 -D /tmp/tz52/hdr/r114 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.ethereum.org/'
     -> status 200 (hops 301 → 200) | bytes 322930 | type text/html; charset=utf-8 | landed https://ethereum.org/ | curl exit 0
r115 2026-09-25T11:16:41Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r115 -D /tmp/tz52/hdr/r115 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://blog.ethereum.org/'
     -> status 200 (hops 200) | bytes 791575 | type text/html; charset=utf-8 | landed https://blog.ethereum.org/ | curl exit 0
r116 2026-09-25T11:16:42Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r116 -D /tmp/tz52/hdr/r116 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://blog.ethereum.org/en/feed.xml'
     -> status 200 (hops 200) | bytes 527621 | type application/xml | landed https://blog.ethereum.org/en/feed.xml | curl exit 0
r117 2026-09-25T11:16:43Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r117 -D /tmp/tz52/hdr/r117 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.hedera.com/'
     -> status 200 (hops 301 → 200) | bytes 463158 | type text/html; charset=UTF-8 | landed https://hedera.com/ | curl exit 0
r118 2026-09-25T11:16:43Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r118 -D /tmp/tz52/hdr/r118 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://hedera.com/feed/'
     -> status 200 (hops 200) | bytes 120892 | type application/rss+xml; charset=UTF-8 | landed https://hedera.com/feed/ | curl exit 0
r119 2026-09-25T11:16:44Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r119 -D /tmp/tz52/hdr/r119 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://hedera.com/comments/feed/'
     -> status 200 (hops 200) | bytes 734 | type application/rss+xml; charset=UTF-8 | landed https://hedera.com/comments/feed/ | curl exit 0
r120 2026-09-25T11:16:44Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r120 -D /tmp/tz52/hdr/r120 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/hashgraph'
     -> status 403 (hops 403) | bytes 5018 | type text/html; charset=UTF-8 | landed https://medium.com/hashgraph | curl exit 0
r121 2026-09-25T11:16:44Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r121 -D /tmp/tz52/hdr/r121 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.stellar.org/'
     -> status 200 (hops 308 → 200) | bytes 695437 | type text/html; charset=utf-8 | landed https://stellar.org/ | curl exit 0
r122 2026-09-25T11:16:45Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r122 -D /tmp/tz52/hdr/r122 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://stellarcommunity.org/'
     -> status 200 (hops 301 → 200) | bytes 119745 | type text/html; charset=utf-8 | landed https://galactictalk.org/ | curl exit 0
r123 2026-09-25T11:16:46Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r123 -D /tmp/tz52/hdr/r123 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitcointalk.org/index.php?topic=1428573.0'
     -> status 200 (hops 200) | bytes 166524 | type text/html; charset=ISO-8859-1 | landed https://bitcointalk.org/index.php?topic=1428573.0 | curl exit 0
r124 2026-09-25T11:16:47Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r124 -D /tmp/tz52/hdr/r124 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitcointalk.org/index.php?type=rss;action=.xml'
     -> status 400 (hops 400) | bytes 101 | type text/html; charset=UTF-8 | landed https://bitcointalk.org/index.php?type=rss;action=.xml | curl exit 0
r125 2026-09-25T11:16:47Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r125 -D /tmp/tz52/hdr/r125 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://algorand.foundation/'
     -> status 200 (hops 301 → 103 → 200) | bytes 320175 | type text/html; charset=UTF-8 | landed https://algorand.co/ | curl exit 0
r126 2026-09-25T11:16:47Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r126 -D /tmp/tz52/hdr/r126 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/algorand'
     -> status 403 (hops 403) | bytes 5018 | type text/html; charset=UTF-8 | landed https://medium.com/algorand | curl exit 0
r127 2026-09-25T11:16:48Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r127 -D /tmp/tz52/hdr/r127 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.algorand.org/'
     -> status 200 (hops 301 → 200) | bytes 16554 | type text/html; charset=utf-8 | landed https://forum.algorand.co/ | curl exit 0
r128 2026-09-25T11:16:49Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r128 -D /tmp/tz52/hdr/r128 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.algorand.co/'
     -> status 200 (hops 200) | bytes 16554 | type text/html; charset=utf-8 | landed https://forum.algorand.co/ | curl exit 0
r129 2026-09-25T11:16:49Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r129 -D /tmp/tz52/hdr/r129 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/?ref=37754157'
     -> status 202 (hops 202) | bytes 0 | type text/html; charset=UTF-8 | landed https://www.binance.com/?ref=37754157 | curl exit 0
r130 2026-09-25T11:16:49Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r130 -D /tmp/tz52/hdr/r130 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://z.cash/'
     -> status 200 (hops 200) | bytes 588900 | type text/html; charset=UTF-8 | landed https://z.cash/ | curl exit 0
r131 2026-09-25T11:16:52Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r131 -D /tmp/tz52/hdr/r131 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://z.cash/feed/'
     -> status 200 (hops 200) | bytes 10141 | type application/rss+xml; charset=UTF-8 | landed https://z.cash/feed/ | curl exit 0
r132 2026-09-25T11:16:53Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r132 -D /tmp/tz52/hdr/r132 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://z.cash/comments/feed/'
     -> status 200 (hops 200) | bytes 691 | type application/rss+xml; charset=UTF-8 | landed https://z.cash/comments/feed/ | curl exit 0
r133 2026-09-25T11:16:53Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r133 -D /tmp/tz52/hdr/r133 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.zcashcommunity.com/'
     -> status 200 (hops 200) | bytes 86862 | type text/html; charset=utf-8 | landed https://forum.zcashcommunity.com/ | curl exit 0
r134 2026-09-25T11:16:55Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r134 -D /tmp/tz52/hdr/r134 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.zcashcommunity.com/posts.rss'
     -> status 200 (hops 200) | bytes 141468 | type application/rss+xml; charset=utf-8 | landed https://forum.zcashcommunity.com/posts.rss | curl exit 0
r135 2026-09-25T11:16:58Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r135 -D /tmp/tz52/hdr/r135 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.zcashcommunity.com/latest.rss'
     -> status 200 (hops 200) | bytes 242084 | type application/rss+xml; charset=utf-8 | landed https://forum.zcashcommunity.com/latest.rss | curl exit 0
r136 2026-09-25T11:16:59Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r136 -D /tmp/tz52/hdr/r136 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://uniswap.org/'
     -> status 200 (hops 302 → 200) | bytes 87110 | type text/html; charset=utf-8 | landed https://app.uniswap.org/ | curl exit 0
r137 2026-09-25T11:17:01Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r137 -D /tmp/tz52/hdr/r137 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://uniswap.org/blog/'
     -> status 200 (hops 302 → 200) | bytes 87110 | type text/html; charset=utf-8 | landed https://app.uniswap.org/ | curl exit 0
r138 2026-09-25T11:17:01Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r138 -D /tmp/tz52/hdr/r138 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.uniswap.org/'
     -> status 200 (hops 200) | bytes 79732 | type text/html; charset=utf-8 | landed https://gov.uniswap.org/ | curl exit 0
r139 2026-09-25T11:17:03Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r139 -D /tmp/tz52/hdr/r139 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.uniswap.org/posts.rss'
     -> status 200 (hops 200) | bytes 113051 | type application/rss+xml; charset=utf-8 | landed https://gov.uniswap.org/posts.rss | curl exit 0
r140 2026-09-25T11:17:06Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r140 -D /tmp/tz52/hdr/r140 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.uniswap.org/latest.rss'
     -> status 200 (hops 200) | bytes 378641 | type application/rss+xml; charset=utf-8 | landed https://gov.uniswap.org/latest.rss | curl exit 0
r141 2026-09-25T11:17:07Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r141 -D /tmp/tz52/hdr/r141 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.getmonero.org/'
     -> status 200 (hops 200) | bytes 33593 | type text/html | landed https://www.getmonero.org/ | curl exit 0
r142 2026-09-25T11:17:08Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r142 -D /tmp/tz52/hdr/r142 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.getmonero.org/feed.xml'
     -> status 200 (hops 200) | bytes 131381 | type text/xml | landed https://www.getmonero.org/feed.xml | curl exit 0
r143 2026-09-25T11:17:08Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r143 -D /tmp/tz52/hdr/r143 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://lighter.xyz/'
     -> status 200 (hops 200) | bytes 2034548 | type text/html | landed https://lighter.xyz/ | curl exit 0
r144 2026-09-25T11:17:08Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r144 -D /tmp/tz52/hdr/r144 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://morpho.org/'
     -> status 200 (hops 200) | bytes 550949 | type text/html; charset=utf-8 | landed https://morpho.org/ | curl exit 0
r145 2026-09-25T11:17:09Z [B4] curl -sS -L -m 20 -o /tmp/tz52/body/r145 -D /tmp/tz52/hdr/r145 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://arbitrum.io/'
     -> status 403 (hops 403) | bytes 5317 | type text/html; charset=UTF-8 | landed https://arbitrum.io/ | curl exit 0
r146 2026-09-25T11:17:46Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r146 -D /tmp/tz52/hdr/r146 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://sui.io/sitemap.xml'
     -> status 200 (hops 301 → 200) | bytes 95947 | type application/rss+xml; charset=utf-8 | landed https://www.sui.io/sitemap.xml | curl exit 0
r147 2026-09-25T11:17:46Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r147 -D /tmp/tz52/hdr/r147 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.sui.io/sitemap.xml'
     -> status 200 (hops 200) | bytes 95947 | type application/rss+xml; charset=utf-8 | landed https://www.sui.io/sitemap.xml | curl exit 0
r148 2026-09-25T11:17:47Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r148 -D /tmp/tz52/hdr/r148 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forums.sui.io/sitemap.xml'
     -> status 200 (hops 200) | bytes 403 | type application/xml; charset=utf-8 | landed https://forums.sui.io/sitemap.xml | curl exit 0
r149 2026-09-25T11:17:47Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r149 -D /tmp/tz52/hdr/r149 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ondo.foundation/sitemap.xml'
     -> status 404 (hops 404) | bytes 21534 | type text/html; charset=utf-8 | landed https://ondo.foundation/sitemap.xml | curl exit 0
r150 2026-09-25T11:17:47Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r150 -D /tmp/tz52/hdr/r150 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://chain.link/sitemap.xml'
     -> status 200 (hops 200) | bytes 200812 | type application/rss+xml; charset=utf-8 | landed https://chain.link/sitemap.xml | curl exit 0
r151 2026-09-25T11:17:47Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r151 -D /tmp/tz52/hdr/r151 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://blog.chain.link/sitemap.xml'
     -> status 200 (hops 301 → 103 → 200) | bytes 354988 | type text/html; charset=utf-8 | landed https://chain.link/blog | curl exit 0
r152 2026-09-25T11:17:47Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r152 -D /tmp/tz52/hdr/r152 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://renderfoundation.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 3537 | type text/xml | landed https://renderfoundation.com/sitemap.xml | curl exit 0
r153 2026-09-25T11:17:47Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r153 -D /tmp/tz52/hdr/r153 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/sitemap/sitemap.xml'
     -> status 200 (hops 200) | bytes 3359674 | type binary/octet-stream | landed https://medium.com/sitemap/sitemap.xml | curl exit 0
r154 2026-09-25T11:17:49Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r154 -D /tmp/tz52/hdr/r154 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml'
     -> status 200 (hops 200) | bytes 2512146 | type binary/octet-stream | landed https://medium.com/sitemap/posts/2026/posts-2026-08-13.xml | curl exit 0
r155 2026-09-25T11:17:51Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r155 -D /tmp/tz52/hdr/r155 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml'
     -> status 200 (hops 200) | bytes 2917539 | type binary/octet-stream | landed https://medium.com/sitemap/posts/2026/posts-2026-07-24.xml | curl exit 0
r156 2026-09-25T11:17:53Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r156 -D /tmp/tz52/hdr/r156 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml'
     -> status 200 (hops 200) | bytes 3251014 | type binary/octet-stream | landed https://medium.com/sitemap/posts/2026/posts-2026-09-24.xml | curl exit 0
r157 2026-09-25T11:17:55Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r157 -D /tmp/tz52/hdr/r157 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.near.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 2470 | type application/xml | landed https://www.near.org/sitemap.xml | curl exit 0
r158 2026-09-25T11:17:55Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r158 -D /tmp/tz52/hdr/r158 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.near.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 538 | type application/xml; charset=utf-8 | landed https://gov.near.org/sitemap.xml | curl exit 0
r159 2026-09-25T11:17:55Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r159 -D /tmp/tz52/hdr/r159 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://yearn.fi/sitemap.xml'
     -> status 200 (hops 200) | bytes 311814 | type application/xml; charset=utf-8 | landed https://yearn.fi/sitemap.xml | curl exit 0
r160 2026-09-25T11:17:55Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r160 -D /tmp/tz52/hdr/r160 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://aave.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 13720 | type application/xml; charset=utf-8 | landed https://aave.com/sitemap.xml | curl exit 0
r161 2026-09-25T11:17:58Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r161 -D /tmp/tz52/hdr/r161 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://aave.com/docs/sitemap.xml'
     -> status 200 (hops 200) | bytes 13567 | type application/xml | landed https://aave.com/docs/sitemap.xml | curl exit 0
r162 2026-09-25T11:17:59Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r162 -D /tmp/tz52/hdr/r162 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://governance.aave.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 415 | type application/xml; charset=utf-8 | landed https://governance.aave.com/sitemap.xml | curl exit 0
r163 2026-09-25T11:17:59Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r163 -D /tmp/tz52/hdr/r163 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.avax.network/sitemap-index.xml'
     -> status 200 (hops 301 → 200) | bytes 187 | type application/xml | landed https://www.avalanche.com/sitemap-index.xml | curl exit 0
r164 2026-09-25T11:17:59Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r164 -D /tmp/tz52/hdr/r164 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.superintelligence.io/sitemap.xml'
     -> status 200 (hops 301 → 301 → 200) | bytes 1162 | type application/xml; charset=UTF-8 | landed https://superintelligence.io/wp-sitemap.xml | curl exit 0
r165 2026-09-25T11:18:00Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r165 -D /tmp/tz52/hdr/r165 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://superintelligence.io/wp-sitemap-posts-post-1.xml'
     -> status 200 (hops 200) | bytes 5881 | type application/xml; charset=UTF-8 | landed https://superintelligence.io/wp-sitemap-posts-post-1.xml | curl exit 0
r166 2026-09-25T11:18:02Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r166 -D /tmp/tz52/hdr/r166 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://superintelligence.io/wp-sitemap-posts-page-1.xml'
     -> status 200 (hops 200) | bytes 2582 | type application/xml; charset=UTF-8 | landed https://superintelligence.io/wp-sitemap-posts-page-1.xml | curl exit 0
r167 2026-09-25T11:18:03Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r167 -D /tmp/tz52/hdr/r167 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://superintelligence.io/wp-sitemap-posts-portfolio-1.xml'
     -> status 200 (hops 200) | bytes 1806 | type application/xml; charset=UTF-8 | landed https://superintelligence.io/wp-sitemap-posts-portfolio-1.xml | curl exit 0
r168 2026-09-25T11:18:03Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r168 -D /tmp/tz52/hdr/r168 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.github.com/sitemap.xml'
     -> status 404 (hops 404) | bytes 106 | type application/json; charset=utf-8 | landed https://api.github.com/sitemap.xml | curl exit 0
r169 2026-09-25T11:18:04Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r169 -D /tmp/tz52/hdr/r169 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ethena.fi/sitemap.xml'
     -> status 200 (hops 200) | bytes 13586 | type application/xml | landed https://ethena.fi/sitemap.xml | curl exit 0
r170 2026-09-25T11:18:04Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r170 -D /tmp/tz52/hdr/r170 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.bittensor.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 103617 | type application/xml | landed https://www.bittensor.com/sitemap.xml | curl exit 0
r171 2026-09-25T11:18:04Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r171 -D /tmp/tz52/hdr/r171 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ton.org/sitemap.xml'
     -> status 404 (hops 404) | bytes 153 | type text/html | landed https://ton.org/sitemap.xml | curl exit 0
r172 2026-09-25T11:18:04Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r172 -D /tmp/tz52/hdr/r172 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ripple.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 400 | type application/xml | landed https://ripple.com/sitemap.xml | curl exit 0
r173 2026-09-25T11:18:05Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r173 -D /tmp/tz52/hdr/r173 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ripple.com/sitemap/press-release.xml'
     -> status 200 (hops 200) | bytes 54415 | type application/xml | landed https://ripple.com/sitemap/press-release.xml | curl exit 0
r174 2026-09-25T11:18:07Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r174 -D /tmp/tz52/hdr/r174 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ripple.com/sitemap/post.xml'
     -> status 200 (hops 200) | bytes 132436 | type application/xml | landed https://ripple.com/sitemap/post.xml | curl exit 0
r175 2026-09-25T11:18:07Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r175 -D /tmp/tz52/hdr/r175 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 371190 | type application/xml | landed https://cardano.org/sitemap.xml | curl exit 0
r176 2026-09-25T11:18:11Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r176 -D /tmp/tz52/hdr/r176 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/de/sitemap.xml'
     -> status 200 (hops 200) | bytes 118246 | type application/xml | landed https://cardano.org/de/sitemap.xml | curl exit 0
r177 2026-09-25T11:18:13Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r177 -D /tmp/tz52/hdr/r177 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/ja/sitemap.xml'
     -> status 200 (hops 200) | bytes 118246 | type application/xml | landed https://cardano.org/ja/sitemap.xml | curl exit 0
r178 2026-09-25T11:18:14Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r178 -D /tmp/tz52/hdr/r178 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/es/sitemap.xml'
     -> status 200 (hops 200) | bytes 118246 | type application/xml | landed https://cardano.org/es/sitemap.xml | curl exit 0
r179 2026-09-25T11:18:16Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r179 -D /tmp/tz52/hdr/r179 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cardano.org/vi/sitemap.xml'
     -> status 200 (hops 200) | bytes 118246 | type application/xml | landed https://cardano.org/vi/sitemap.xml | curl exit 0
r180 2026-09-25T11:18:16Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r180 -D /tmp/tz52/hdr/r180 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://tron.network/sitemap.xml'
     -> status 404 (hops 404) | bytes 7034 | type text/html | landed https://tron.network/sitemap.xml | curl exit 0
r181 2026-09-25T11:18:17Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r181 -D /tmp/tz52/hdr/r181 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://solana.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 3376951 | type application/xml | landed https://solana.com/sitemap.xml | curl exit 0
r182 2026-09-25T11:18:18Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r182 -D /tmp/tz52/hdr/r182 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://solana.com/news/sitemap-news.xml'
     -> status 200 (hops 200) | bytes 2080 | type application/xml; charset=utf-8 | landed https://solana.com/news/sitemap-news.xml | curl exit 0
r183 2026-09-25T11:18:19Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r183 -D /tmp/tz52/hdr/r183 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://solana.com/podcasts/sitemap.xml'
     -> status 200 (hops 200) | bytes 241145 | type application/xml; charset=utf-8 | landed https://solana.com/podcasts/sitemap.xml | curl exit 0
r184 2026-09-25T11:18:20Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r184 -D /tmp/tz52/hdr/r184 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.solana.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 409 | type application/xml; charset=utf-8 | landed https://forum.solana.com/sitemap.xml | curl exit 0
r185 2026-09-25T11:18:20Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r185 -D /tmp/tz52/hdr/r185 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bch.info/sitemap.xml'
     -> status 404 (hops 404) | bytes 9757 | type text/html; charset=utf-8 | landed https://bch.info/sitemap.xml | curl exit 0
r186 2026-09-25T11:18:20Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r186 -D /tmp/tz52/hdr/r186 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://app.hyperliquid.xyz/sitemap.xml'
     -> status 200 (hops 200) | bytes 6845 | type text/html | landed https://app.hyperliquid.xyz/sitemap.xml | curl exit 0
r187 2026-09-25T11:18:21Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r187 -D /tmp/tz52/hdr/r187 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://sky.money/sitemap.xml'
     -> status 200 (hops 200) | bytes 2961 | type application/rss+xml; charset=utf-8 | landed https://sky.money/sitemap.xml | curl exit 0
r188 2026-09-25T11:18:21Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r188 -D /tmp/tz52/hdr/r188 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ethereum.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 1975 | type application/xml; charset=utf-8 | landed https://ethereum.org/sitemap.xml | curl exit 0
r189 2026-09-25T11:18:21Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r189 -D /tmp/tz52/hdr/r189 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://blog.ethereum.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 215 | type application/xml | landed https://blog.ethereum.org/sitemap.xml | curl exit 0
r190 2026-09-25T11:18:21Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r190 -D /tmp/tz52/hdr/r190 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://hedera.com/sitemap_index.xml'
     -> status 200 (hops 200) | bytes 1259 | type text/xml; charset=UTF-8 | landed https://hedera.com/sitemap_index.xml | curl exit 0
r191 2026-09-25T11:18:22Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r191 -D /tmp/tz52/hdr/r191 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://hedera.com/post-sitemap.xml'
     -> status 200 (hops 200) | bytes 316306 | type text/xml; charset=UTF-8 | landed https://hedera.com/post-sitemap.xml | curl exit 0
r192 2026-09-25T11:18:24Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r192 -D /tmp/tz52/hdr/r192 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://hedera.com/post_tag-sitemap.xml'
     -> status 200 (hops 200) | bytes 2657 | type text/xml; charset=UTF-8 | landed https://hedera.com/post_tag-sitemap.xml | curl exit 0
r193 2026-09-25T11:18:24Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r193 -D /tmp/tz52/hdr/r193 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.stellar.org/sitemap.xml'
     -> status 200 (hops 308 → 200) | bytes 203604 | type text/xml | landed https://stellar.org/sitemap.xml | curl exit 0
r194 2026-09-25T11:18:25Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r194 -D /tmp/tz52/hdr/r194 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://galactictalk.org/sitemap.xml'
     -> status 404 (hops 404) | bytes 153 | type text/html | landed https://galactictalk.org/sitemap.xml | curl exit 0
r195 2026-09-25T11:18:25Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r195 -D /tmp/tz52/hdr/r195 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://bitcointalk.org/sitemap.php'
     -> status 200 (hops 200) | bytes 1087263 | type text/xml;charset=UTF-8 | landed https://bitcointalk.org/sitemap.php | curl exit 0
r196 2026-09-25T11:18:25Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r196 -D /tmp/tz52/hdr/r196 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://algorand.foundation/sitemap.xml'
     -> status 200 (hops 301 → 200) | bytes 914065 | type application/xml | landed https://algorand.co/sitemap.xml | curl exit 0
r197 2026-09-25T11:18:26Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r197 -D /tmp/tz52/hdr/r197 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.algorand.co/sitemap.xml'
     -> status 200 (hops 200) | bytes 411 | type application/xml; charset=utf-8 | landed https://forum.algorand.co/sitemap.xml | curl exit 0
r198 2026-09-25T11:18:26Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r198 -D /tmp/tz52/hdr/r198 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Trade_index.xml'
     -> status 200 (hops 200) | bytes 6942 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Trade_index.xml | curl exit 0
r199 2026-09-25T11:18:28Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r199 -D /tmp/tz52/hdr/r199 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_index.xml'
     -> status 200 (hops 200) | bytes 6900 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_index.xml | curl exit 0
r200 2026-09-25T11:18:30Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r200 -D /tmp/tz52/hdr/r200 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_ja_0.xml'
     -> status 200 (hops 200) | bytes 133879 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_ja_0.xml | curl exit 0
r201 2026-09-25T11:18:32Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r201 -D /tmp/tz52/hdr/r201 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_lo-LA_0.xml'
     -> status 200 (hops 200) | bytes 361 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_lo-LA_0.xml | curl exit 0
r202 2026-09-25T11:18:34Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r202 -D /tmp/tz52/hdr/r202 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_ru-UA_0.xml'
     -> status 200 (hops 200) | bytes 287811 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Blog_ru-UA_0.xml | curl exit 0
r203 2026-09-25T11:18:36Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r203 -D /tmp/tz52/hdr/r203 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Nft_index.xml'
     -> status 200 (hops 200) | bytes 6858 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Nft_index.xml | curl exit 0
r204 2026-09-25T11:18:38Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r204 -D /tmp/tz52/hdr/r204 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml'
     -> status 200 (hops 200) | bytes 13536 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_index.xml | curl exit 0
r205 2026-09-25T11:18:40Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r205 -D /tmp/tz52/hdr/r205 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_es-MX_1.xml'
     -> status 200 (hops 200) | bytes 274568 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_es-MX_1.xml | curl exit 0
r206 2026-09-25T11:18:42Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r206 -D /tmp/tz52/hdr/r206 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_ru_1.xml'
     -> status 200 (hops 200) | bytes 456283 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_ru_1.xml | curl exit 0
r207 2026-09-25T11:18:45Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r207 -D /tmp/tz52/hdr/r207 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en-KZ_1.xml'
     -> status 200 (hops 200) | bytes 293365 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_en-KZ_1.xml | curl exit 0
r208 2026-09-25T11:18:47Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r208 -D /tmp/tz52/hdr/r208 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Futures_index.xml'
     -> status 200 (hops 200) | bytes 9800 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Futures_index.xml | curl exit 0
r209 2026-09-25T11:18:49Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r209 -D /tmp/tz52/hdr/r209 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Earn_index.xml'
     -> status 200 (hops 200) | bytes 6739 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Earn_index.xml | curl exit 0
r210 2026-09-25T11:18:51Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r210 -D /tmp/tz52/hdr/r210 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Loan_index.xml'
     -> status 200 (hops 200) | bytes 6098 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Loan_index.xml | curl exit 0
r211 2026-09-25T11:18:53Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r211 -D /tmp/tz52/hdr/r211 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Market_index.xml'
     -> status 200 (hops 200) | bytes 6984 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Market_index.xml | curl exit 0
r212 2026-09-25T11:18:55Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r212 -D /tmp/tz52/hdr/r212 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Default_index.xml'
     -> status 200 (hops 200) | bytes 14200 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Default_index.xml | curl exit 0
r213 2026-09-25T11:18:56Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r213 -D /tmp/tz52/hdr/r213 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Fiat_index.xml'
     -> status 200 (hops 200) | bytes 6900 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Fiat_index.xml | curl exit 0
r214 2026-09-25T11:18:58Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r214 -D /tmp/tz52/hdr/r214 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Crypto_index.xml'
     -> status 200 (hops 200) | bytes 6984 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Crypto_index.xml | curl exit 0
r215 2026-09-25T11:18:59Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r215 -D /tmp/tz52/hdr/r215 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Square_index.xml'
     -> status 200 (hops 200) | bytes 6584 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Square_index.xml | curl exit 0
r216 2026-09-25T11:19:01Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r216 -D /tmp/tz52/hdr/r216 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Academy_New_index.xml'
     -> status 200 (hops 200) | bytes 6774 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Academy_New_index.xml | curl exit 0
r217 2026-09-25T11:19:03Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r217 -D /tmp/tz52/hdr/r217 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Muses_index.xml'
     -> status 200 (hops 200) | bytes 5904 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Muses_index.xml | curl exit 0
r218 2026-09-25T11:19:05Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r218 -D /tmp/tz52/hdr/r218 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Growth_index.xml'
     -> status 200 (hops 200) | bytes 25171 | type application/xml | landed https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_Growth_index.xml | curl exit 0
r219 2026-09-25T11:19:06Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r219 -D /tmp/tz52/hdr/r219 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://z.cash/sitemap.xml'
     -> status 200 (hops 200) | bytes 79564 | type text/xml; charset=utf-8 | landed https://z.cash/sitemap.xml | curl exit 0
r220 2026-09-25T11:19:07Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r220 -D /tmp/tz52/hdr/r220 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://forum.zcashcommunity.com/sitemap.xml'
     -> status 200 (hops 200) | bytes 574 | type application/xml; charset=utf-8 | landed https://forum.zcashcommunity.com/sitemap.xml | curl exit 0
r221 2026-09-25T11:19:08Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r221 -D /tmp/tz52/hdr/r221 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://uniswap.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 185 | type application/xml | landed https://uniswap.org/sitemap.xml | curl exit 0
r222 2026-09-25T11:19:08Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r222 -D /tmp/tz52/hdr/r222 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://gov.uniswap.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 407 | type application/xml; charset=utf-8 | landed https://gov.uniswap.org/sitemap.xml | curl exit 0
r223 2026-09-25T11:19:09Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r223 -D /tmp/tz52/hdr/r223 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.getmonero.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 111068 | type text/xml | landed https://www.getmonero.org/sitemap.xml | curl exit 0
r224 2026-09-25T11:19:09Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r224 -D /tmp/tz52/hdr/r224 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://lighter.xyz/sitemap.xml'
     -> status 200 (hops 200) | bytes 881 | type text/xml | landed https://lighter.xyz/sitemap.xml | curl exit 0
r225 2026-09-25T11:19:09Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r225 -D /tmp/tz52/hdr/r225 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://morpho.org/sitemap.xml'
     -> status 200 (hops 200) | bytes 18103 | type application/xml | landed https://morpho.org/sitemap.xml | curl exit 0
r226 2026-09-25T11:19:09Z [B5] curl -sS -L -m 20 -o /tmp/tz52/body/r226 -D /tmp/tz52/hdr/r226 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://arbitrum.io/sitemap.xml'
     -> status 403 (hops 403) | bytes 5371 | type text/html; charset=UTF-8 | landed https://arbitrum.io/sitemap.xml | curl exit 0
r227 2026-09-25T11:22:04Z [V2] curl -sS -L -m 20 -o /tmp/tz52/body/r227 -D /tmp/tz52/hdr/r227 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ondo.finance/robots.txt'
     -> status 200 (hops 200) | bytes 66 | type text/plain; charset=utf-8 | landed https://ondo.finance/robots.txt | curl exit 0
r228 2026-09-25T11:22:05Z [V2] curl -sS -L -m 20 -o /tmp/tz52/body/r228 -D /tmp/tz52/hdr/r228 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ondo.finance/sitemap.xml'
     -> status 200 (hops 200) | bytes 38042 | type application/xml | landed https://ondo.finance/sitemap.xml | curl exit 0
r229 2026-09-25T11:22:14Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r229 -D /tmp/tz52/hdr/r229 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.coindesk.com/robots.txt'
     -> status 200 (hops 200) | bytes 4345 | type text/plain | landed https://www.coindesk.com/robots.txt | curl exit 0
r230 2026-09-25T11:22:16Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r230 -D /tmp/tz52/hdr/r230 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.coindesk.com/arc/outboundfeeds/rss/'
     -> status 200 (hops 308 → 200) | bytes 30822 | type application/xml | landed https://www.coindesk.com/arc/outboundfeeds/rss | curl exit 0
r231 2026-09-25T11:22:16Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r231 -D /tmp/tz52/hdr/r231 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.theblock.co/robots.txt'
     -> status 200 (hops 200) | bytes 890 | type text/plain; charset=utf-8 | landed https://www.theblock.co/robots.txt | curl exit 0
r232 2026-09-25T11:22:17Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r232 -D /tmp/tz52/hdr/r232 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.theblock.co/rss.xml'
     -> status 200 (hops 200) | bytes 29564 | type text/xml; charset=UTF-8 | landed https://www.theblock.co/rss.xml | curl exit 0
r233 2026-09-25T11:22:17Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r233 -D /tmp/tz52/hdr/r233 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://decrypt.co/robots.txt'
     -> status 200 (hops 200) | bytes 160 | type text/plain; charset=UTF-8 | landed https://decrypt.co/robots.txt | curl exit 0
r234 2026-09-25T11:22:18Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r234 -D /tmp/tz52/hdr/r234 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://decrypt.co/feed'
     -> status 200 (hops 200) | bytes 38751 | type application/xml | landed https://decrypt.co/feed | curl exit 0
r235 2026-09-25T11:22:18Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r235 -D /tmp/tz52/hdr/r235 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cointelegraph.com/robots.txt'
     -> status 200 (hops 200) | bytes 384 | type text/plain | landed https://cointelegraph.com/robots.txt | curl exit 0
r236 2026-09-25T11:22:19Z [C] curl -sS -L -m 20 -o /tmp/tz52/body/r236 -D /tmp/tz52/hdr/r236 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://cointelegraph.com/rss'
     -> status 200 (hops 200) | bytes 52282 | type application/xml; charset=utf-8 | landed https://cointelegraph.com/rss | curl exit 0
r237 2026-09-25T11:22:43Z [D] curl -sS -L -m 20 -o /tmp/tz52/body/r237 -D /tmp/tz52/hdr/r237 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://api.upbit.com/v1/market/all?isDetails=true'
     -> status 200 (hops 200) | bytes 243205 | type application/json;charset=UTF-8 | landed https://api.upbit.com/v1/market/all?isDetails=true | curl exit 0
r238 2026-09-25T11:23:09Z [E1] curl -sS -L -m 20 -o /tmp/tz52/body/r238 -D /tmp/tz52/hdr/r238 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://www.federalregister.gov/api/v1/documents.json?per_page=20&order=newest&conditions%5Bagencies%5D%5B%5D=securities-and-exchange-commission'
     -> status 200 (hops 200) | bytes 19528 | type application/json; charset=utf-8 | landed https://www.federalregister.gov/api/v1/documents.json?per_page=20&order=newest&conditions%5Bagencies%5D%5B%5D=securities-and-exchange-commission | curl exit 0
r239 2026-09-25T11:23:30Z [E2a] curl -sS -L -m 20 -o /tmp/tz52/body/r239 -D /tmp/tz52/hdr/r239 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1'
     -> status 403 (hops 403) | bytes 4819 | type text/html | landed https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1 | curl exit 0
r240 2026-09-25T11:23:31Z [E2b] curl -sS -L -m 20 -o /tmp/tz52/body/r240 -D /tmp/tz52/hdr/r240 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' -A "crypto-auto d***@yahoo.com" 'https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1'
     -> status 200 (hops 200) | bytes 57822 | type application/json | landed https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1 | curl exit 0
r241 2026-09-25T11:23:49Z [F] curl -sS -L -m 20 -o /tmp/tz52/body/r241 -D /tmp/tz52/hdr/r241 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/klines?symbol=HYPEUSDT&interval=1h&limit=3'
     -> status 200 (hops 200) | bytes 437 | type application/json | landed https://fapi.binance.com/fapi/v1/klines?symbol=HYPEUSDT&interval=1h&limit=3 | curl exit 0
r242 2026-09-25T11:23:50Z [F] curl -sS -L -m 20 -o /tmp/tz52/body/r242 -D /tmp/tz52/hdr/r242 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/klines?symbol=XMRUSDT&interval=1h&limit=3'
     -> status 200 (hops 200) | bytes 388 | type application/json | landed https://fapi.binance.com/fapi/v1/klines?symbol=XMRUSDT&interval=1h&limit=3 | curl exit 0
r243 2026-09-25T11:23:51Z [F] curl -sS -L -m 20 -o /tmp/tz52/body/r243 -D /tmp/tz52/hdr/r243 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/klines?symbol=LITUSDT&interval=1h&limit=3'
     -> status 200 (hops 200) | bytes 427 | type application/json | landed https://fapi.binance.com/fapi/v1/klines?symbol=LITUSDT&interval=1h&limit=3 | curl exit 0
r244 2026-09-25T11:23:53Z [F] curl -sS -L -m 20 -o /tmp/tz52/body/r244 -D /tmp/tz52/hdr/r244 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/klines?symbol=MORPHOUSDT&interval=1h&limit=3'
     -> status 200 (hops 200) | bytes 440 | type application/json | landed https://fapi.binance.com/fapi/v1/klines?symbol=MORPHOUSDT&interval=1h&limit=3 | curl exit 0
r245 2026-09-25T11:23:54Z [F] curl -sS -L -m 20 -o /tmp/tz52/body/r245 -D /tmp/tz52/hdr/r245 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://fapi.binance.com/fapi/v1/klines?symbol=ARBUSDT&interval=1h&limit=3'
     -> status 200 (hops 200) | bytes 439 | type application/json | landed https://fapi.binance.com/fapi/v1/klines?symbol=ARBUSDT&interval=1h&limit=3 | curl exit 0
```

---

## Validation

**V1 — Classifier fixtures in `/tmp`.** The fixtures are files under `/tmp/tz52/v1/`: `a.xml`,
`b.xml` and `c.xml` are urlsets, and `de.json` holds d and e. They run through the same
`parse_sitemap`, `classify` and `screen` that classified every lane above. The negative control
inverts B6's day comparison (`>= 2` becomes `< 2`), and **a and b swap**. c stays `undated`
because it carries no date at all, which the TZ leaves unconstrained.

```
V1 run 1 (B6/B7 as written):
  fixture a  expected dated        got dated        PASS
  fixture b  expected undated      got undated      PASS
  fixture c  expected undated      got undated      PASS
  fixture d  expected carried      got carried      PASS
  fixture e  expected window short got window short PASS
V1 run 2 (B6 comparison inverted, a-c):
  fixture a  run1 dated     inverted undated  
  fixture b  run1 undated   inverted dated    
  fixture c  run1 undated   inverted undated  
V1 checks run 5, PASS 5, FAIL 0; negative control a<->b swapped: yes
```

**V2 — Live known-answer pair, reported, not blocking: 2 of 2 match, no host changed.**

| | Expected | Read | Evidence |
|---|---|---|---|
| NEAR `https://www.near.org/sitemap.xml` | `undated`, a comment declaring placeholders dated 2026-08-15 | **`undated`** — 13 URLs, 13 with `lastmod`, one distinct day 2026-08-15; comment: «lastmod values are placeholders dated 2026-08-15; generate them at build time.» | Stage B read `r157` (declared in `near.org`'s robots.txt) |
| Ondo `https://ondo.finance/sitemap.xml` | `dated`, declared in robots.txt, `lastmod` on 186 of 198, newest blog record `2026-09-24T12:30:00.000Z` | **`dated`** — declared: yes; 198 URLs, 186 with `lastmod`; newest blog record `2026-09-24T12:30:00.000Z` | V2 reads `r227` (robots.txt, 200, 66 bytes) and `r228` (sitemap, 200, 38 042 bytes) |

```
READ r227 [V2] curl -sS -L -m 20 -o /tmp/tz52/body/r227 -D /tmp/tz52/hdr/r227 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ondo.finance/robots.txt' -> 200 66 text/plain; charset=utf-8 https://ondo.finance/robots.txt (exit 0) 0.1s
READ r228 [V2] curl -sS -L -m 20 -o /tmp/tz52/body/r228 -D /tmp/tz52/hdr/r228 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'https://ondo.finance/sitemap.xml' -> 200 38042 application/xml https://ondo.finance/sitemap.xml (exit 0) 0.3s
{
 "NEAR": {
  "url": "https://www.near.org/sitemap.xml",
  "rec": "r157",
  "source": "Stage B read",
  "kind": "urlset",
  "urls": 13,
  "with_lastmod": 13,
  "distinct_days_all": [
   "2026-08-15"
  ],
  "considered": 1,
  "b6": "undated",
  "placeholders": [
   "lastmod values are placeholders dated 2026-08-15; generate them at build time."
  ],
  "expected": "undated",
  "verdict": "match",
  "host_changed": false
 },
 "Ondo": {
  "url": "https://ondo.finance/sitemap.xml",
  "robots": "r227",
  "robots_code": "200",
  "declared": true,
  "declared_list": [
   "https://ondo.finance/sitemap.xml"
  ],
  "perm": {
   "host": "https://ondo.finance",
   "robots": "r227",
   "group": "*",
   "path": "/sitemap.xml",
   "matched": [
    "Allow: /"
   ],
   "decision": "allow"
  },
  "rec": "r228",
  "outcome": "ok",
  "kind": "urlset",
  "urls": 198,
  "with_lastmod": 186,
  "considered": 181,
  "basis": "keyword paths",
  "considered_with_lastmod": 179,
  "days": 167,
  "b6": "dated",
  "newest_blog": "2026-09-24T12:30:00.000Z",
  "newest_blog_loc": "https://ondo.finance/blog/introducing-ondo-intelligent-portfolios",
  "newest": "2026-09-24T12:30:00+00:00",
  "oldest": "2021-07-27T19:33:00+00:00",
  "placeholders": [],
  "b7_aux": "carried",
  "D": "2026-09-17",
  "b7_hits": [
   "2026-09-16"
  ],
  "expected": "dated",
  "verdict": "match",
  "host_changed": false
 }
}
```

**V3 — Counts are counts.** Attempted is shown beside reported for every stage. No stage
attempted zero.

| Stage | Attempted | Reported |
|---|---|---|
| A | A2: 30 rows (30 `name:` occurrences); A3: 30 symbols | 30 · 30 coverage records, 0 absent |
| B (coins) | **30, A2's count is 30** | 30 coin rows |
| B1 | 30 CoinGecko reads | 30 answered 200 |
| B3 | 46 candidate origins | 45 reads + 1 covered by a redirect landing = 46 |
| B4 | 54 candidate pages; 18 advertised feeds | 52 read + 2 refused on permission; 18 read |
| B5 | 84 sitemap documents referenced (68 top-level, 16 children) | 81 reads + 2 refused on permission + 1 document shared by two origins = 84 |
| B6/B7 | 95 lane readings | 95 classified: 39 `dated` · 19 `undated` · 34 `no channel` · 1 `refused` · 2 `refused on permission` |
| V2 | 2 reads | 2 |
| C | 4 feeds (4 robots.txt + 4 feeds = 8 reads) | 4 feeds; 109 items, 109 dated |
| D | 1 read | 855 markets |
| E1 | 1 read | 20 results |
| E2 | 2 reads | 2 |
| F | 5 `fut:true` pairs | 5 reads |
| **All** | **245 reads** | B1 30 + B3 45 + B4 70 + B5 81 + V2 2 + C 8 + D 1 + E1 1 + E2 2 + F 5 = 245 |

**V4 — Evidence.** Every ledger line carries command, status, bytes, content type and landing
URL. The same pass checks the client rules:

```
ledger reads: 245
per stage: {'B1': 30, 'B3': 45, 'B4': 70, 'B5': 81, 'V2': 2, 'C': 8, 'D': 1, 'E1': 1, 'E2a': 1, 'E2b': 1, 'F': 5}
(url, form) pairs requested more than once: 0
URLs requested in two forms (E2 exception): ['https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1']
reads overlapping the previous read: 0 of 244 consecutive pairs
CoinGecko reads: 30 ; end-to-start gaps: min 12.50 s, max 12.50 s
ledger lines missing command/status/bytes/landing: 0 []
ledger lines with empty content type: 0 []
commands not in rule-1 form: 0 [] ; commands carrying -A: ['r240']
landing URLs reached by more than one request: 5
    https://chain.link/blog <- ['r035 https://blog.chain.link/robots.txt', 'r081 https://blog.chain.link/', 'r151 https://blog.chain.link/sitemap.xml']
    https://forum.algorand.co/ <- ['r127 https://forum.algorand.org/', 'r128 https://forum.algorand.co/']
    https://app.uniswap.org/ <- ['r136 https://uniswap.org/', 'r137 https://uniswap.org/blog/']
    https://www.sui.io/sitemap.xml <- ['r146 https://sui.io/sitemap.xml', 'r147 https://www.sui.io/sitemap.xml']
    https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1 <- ['r239 https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1', 'r240 https://efts.sec.gov/LATEST/search-index?q=%22Solana%22&forms=S-1']
first read ts: 2026-09-25T11:09:07Z  last read ts: 2026-09-25T11:23:54Z
```

The five landing URLs reached by more than one request are redirects from distinct requested
URLs. Four are:

- `sui.io` declares both `https://sui.io/sitemap.xml` and `https://www.sui.io/sitemap.xml`.
- ALGO's announcement `forum.algorand.org/` and its `carried_by` root `forum.algorand.co/`.
- `uniswap.org/` and `uniswap.org/blog/` both land on `app.uniswap.org/`.
- `blog.chain.link` sends its robots.txt, root and sitemap all to `chain.link/blog`.

The fifth is E2's named exception. No requested URL was requested twice in one form. The
masked contact is the only form of the address in any file this session wrote. The check
below covers all 556 scratch files, bodies and headers included, plus this report, and was
run from the repository root before V6:

```
$ e=$(git config --get user.email); grep --recursive --fixed-strings --files-with-matches -- "$e" /tmp/tz52 CryptoReports/TZ-52-catalyst-lanes-vps-measurement-report.md | wc --lines
0
$ find /tmp/tz52 -type f | wc --lines
556
```

**V5 — Nothing but the report.** Run from the repository root after a fresh
`git fetch origin main`. The fetch found `origin/main` still at `1d0cda9`, the commit HEAD
stands on.

```
$ git status --porcelain
?? CryptoReports/TZ-52-catalyst-lanes-vps-measurement-report.md
$ git status --porcelain | wc --lines
1
$ git diff --stat HEAD -- . ':(exclude)CryptoReports/'
$ git diff --stat HEAD -- . ':(exclude)CryptoReports/' | wc --lines
0
```

No production file, bench or workflow is touched, so no bench ran. The empty diff outside
`CryptoReports/` is the no-regression evidence.

**V6 — Hygiene.** The scratch was removed after the last result had been rendered into this
report and V5 had run. The count is three files higher than in V4's check, because the replay
added its own script and two logs after that check.

```
$ du --summarize --human-readable /tmp/tz52; find /tmp/tz52 -type f | wc --lines
39M	/tmp/tz52
559
$ ls --directory /tmp/tz52*
/tmp/tz52
$ rm --recursive --force /tmp/tz52; echo "rm exit=$?"
rm exit=0
$ ls /tmp/tz52; echo "ls exit=$?"
ls: cannot access '/tmp/tz52': No such file or directory
ls exit=2
$ ls --directory /tmp/tz52* 2>/dev/null | wc --lines
0
```

The V5/V6 blocks were pasted in after the removal, so they are the one place in this report
that `report.py` did not fill. Nothing else was committed. The commit carries this file alone
(`## Commit`).

**Additionally — the instrument's own self-test** (not a TZ item). It uses localhost only and a
separate ledger, and ran before the first external request and again after each parser change:

```
PASS  robots groups                                              got=2
PASS  robots sitemaps                                            got=['https://ex.test/sitemap.xml', 'https://cdn.ex.test/news-sitemap.xml']
PASS  robots governing group for curl                            got='*'
PASS  robots allow /                                             got=True
PASS  robots /blog/x allowed                                     got=True
PASS  robots /blog/private disallowed (longer)                   got=False
PASS  robots /a.pdf disallowed ($)                               got=False
PASS  robots /a.pdfx allowed ($ anchors)                         got=True
PASS  robots /tmp/ok allowed (longer allow)                      got=True
PASS  robots /tmp/no disallowed                                  got=False
PASS  robots matched lines listed                                got=['Disallow: /tmp', 'Allow: /tmp/ok']
PASS  robots curl-specific group wins                            got='curl'
PASS  robots empty disallow allows                               got=True
PASS  robots tie -> allow                                        got=True
PASS  feed links                                                 got=[('https://ex.test/feed.xml', 'application/rss+xml'), ('https://other.test/atom.xml?x=1&y=2', 'application/atom+xml'), ('https://ex.test/path/rel/feed2', 'application/rss+xml')]
PASS  rss items                                                  got=3
PASS  rss dated                                                  got=2
PASS  rss title cdata+entity                                     got='SOL rallies & ETH'
PASS  rss tz -> UTC day                                          got='2026-09-24'
PASS  atom published preferred over updated                      got='2026-09-19'
PASS  atom updated when no published                             got='2026-09-21'
PASS  html is not a feed                                         got=None
PASS  index kind                                                 got='index'
PASS  index keyword children, latest first, top 3                got=['News', 'sitemap-updates.xml', 'sitemap-blog.xml']
PASS  urlset kind                                                got='urlset'
PASS  urlset loc not the image loc                               got='https://ex.test/blog/a'
PASS  placeholder quote                                          got=['lastmod values are placeholders set to 2026-08-15 until the CMS migration completes']
PASS  placeholder quote is the stating sentence                  got=['lastmod values are placeholders dated 2026-08-15; regenerate.']
PASS  gzip sitemap parsed                                        got='urlset'
PASS  date 2026-09-24T12:30:00.000Z                              got='2026-09-24'
PASS  date 2026-09-24                                            got='2026-09-24'
PASS  date 2026-09-24T23:30:00-04:00                             got='2026-09-25'
PASS  date Thu, 25 Sep 2026 01:00:00 +0400                       got='2026-09-24'
PASS  date 2026-09-24T12:30:00.1234567+00:00                     got='2026-09-24'
PASS  date 2026-09-24 12:30:00                                   got='2026-09-24'
PASS  date garbage                                               got=None
PASS  cb host plain                                              got='gov.near.org'
PASS  cb host with path+prose                                    got='api.github.com'
PASS  cb host with dash prose                                    got='governance.aave.com'
PASS  cb prose -> none                                           got=None
PASS  cb prose (fut) -> none                                     got=None
PASS  move day                                                   got='2026-09-18'
PASS  move none                                                  got=None
PASS  norm url                                                   got='https://sui.io/'
PASS  B6 two days dated                                          got='dated'
PASS  B6 one day undated                                         got='undated'
PASS  B6 none undated                                            got='undated'
PASS  B7 D-2 carried                                             got='carried'
PASS  B7 D-3 and D+1 not carried                                 got='not carried'
PASS  B7 oldest D-1? carried                                     got='carried'
PASS  B7 oldest D+1 window short                                 got='window short'
READ r001 [T] curl -sS -L -m 20 -o /tmp/tz52/selftest/body/r001 -D /tmp/tz52/selftest/hdr/r001 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'http://127.0.0.1:49583/robots.txt' -> 200 80 text/plain http://127.0.0.1:49583/robots.txt (exit 0) 0.0s
PASS  fetch robots sitemap line                                  got=['http://127.0.0.1:49583/sitemap.xml.gz']
SKIP [T] http://127.0.0.1:49583/private/x -> refused on permission ['Disallow: /private']
PASS  guarded disallowed not requested                           got=(None, 'disallow', ['Disallow: /private'])
READ r002 [T] curl -sS -L -m 20 -o /tmp/tz52/selftest/body/r002 -D /tmp/tz52/selftest/hdr/r002 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'http://127.0.0.1:49583/page.html' -> 200 361 text/html http://127.0.0.1:49583/page.html (exit 0) 0.0s
PASS  fetch code/ctype/landing                                   got=('200', 'text/html', 'http://127.0.0.1:49583/page.html')
PASS  fetch bytes = file size                                    got=361
PASS  fetch display form                                         got="curl -sS -L -m 20 -o /tmp/tz52/selftest/body/r002 -D /tmp/tz52/selftest/hdr/r002 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\\n' 'http://127.0.0.1:49583/page.html'"
PASS  second fetch of one URL reuses the ledger                  got=(True, 'r002')
PASS  ledger lines (robots + page)                               got=2
READ r003 [T] curl -sS -L -m 20 -o /tmp/tz52/selftest/body/r003 -D /tmp/tz52/selftest/hdr/r003 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'http://127.0.0.1:49583/sitemap.xml.gz' -> 200 258 application/gzip http://127.0.0.1:49583/sitemap.xml.gz (exit 0) 0.0s
PASS  gz body decompressed locally                               got='urlset'
READ r004 [T] curl -sS -L -m 20 -o /tmp/tz52/selftest/body/r004 -D /tmp/tz52/selftest/hdr/r004 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'http://127.0.0.1:49583/nope.xml' -> 404 335 text/html;charset=utf-8 http://127.0.0.1:49583/nope.xml (exit 0) 0.0s
PASS  404 outcome                                                got='absent (HTTP 404)'
READ r005 [T] curl -sS -L -m 20 -o /tmp/tz52/selftest/body/r005 -D /tmp/tz52/selftest/hdr/r005 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' 'http://127.0.0.1:1/x' -> 000 0 - http://127.0.0.1:1/x (exit 7, curl: (7) Failed to connect to 127.0.0.1 port 1 after 0 ms: Couldn't connect to server) 0.0s
PASS  unreachable outcome                                        got=True
READ r006 [T] curl -sS -L -m 20 -o /tmp/tz52/selftest/body/r006 -D /tmp/tz52/selftest/hdr/r006 -w '%{http_code} %{size_download} %{content_type} %{url_effective}\n' -A "crypto-auto s***@example.test" 'http://127.0.0.1:49583/page.html' -> 200 361 text/html http://127.0.0.1:49583/page.html (exit 0) 0.0s
PASS  declared form is a distinct ledger key                     got=False
PASS  declared display masks contact                             got=(False, True)
selftest checks run 63, PASS 63, FAIL 0
```

---

## Test Results

| Item | Result |
|---|---|
| V1 classifier fixtures | **5 of 5 PASS**; negative control swapped a ↔ b |
| V2 known-answer pair | **2 of 2 match**, no host changed |
| V3 counts | every stage attempted > 0; B coins 30 = A2 30; 245 reads, summed per stage |
| V4 evidence | 245 of 245 ledger lines complete; 0 duplicate `(url, form)`; 0 overlapping reads; CoinGecko gaps 12.50 s; every command in rule-1 form, `-A` on `r240` only |
| V5 nothing but the report | `git status --porcelain` lists exactly the report |
| V6 hygiene | `/tmp/tz52` removed; `ls` confirms |
| Self-test (extra) | 63 of 63 PASS |
| Replay on final text (extra) | 13 of 13 result files identical; ledger unchanged at 245 |

---

## Deviations

1. **V2's Ondo half cost two requests outside Stage B.** Stage B reaches Ondo only through
   CoinGecko's registered homepage, `ondo.foundation`. V2 names `ondo.finance`, which no B2
   candidate reaches. Without reading it, V2 could not run, and an item that cannot run fails.
   The two reads are the TZ's own named URL and its host's robots.txt (rule 4), each in the
   rule-1 form, once: `r227` and `r228`. They feed V2 and Finding 2 only, never Stage B's table.
2. **Where the TZ is silent, these readings were chosen and applied uniformly**, so the
   Architect can overrule any one in a line:
   - robots.txt per RFC 9309, detailed under `### Instrument`.
   - B4's «at most two per host», read per candidate origin. It never bound: the maximum
     advertised was 2.
   - A nested sitemap index would not be descended. None occurred.
   - The date of a feed record is `pubDate`, else `published`, else `updated`, in the TZ's
     order.
   - A B6 404 is recorded as `no channel`, as is the 400 of `bitcointalk.org`'s disabled feed,
     with the status printed beside the word.
   - E1's first term list is counted case-sensitively and insensitively, and the second as
     substring and as whole word. Both are printed, and they differ only on «Whether».
   - D's «A2 symbol carrying either» is read across all of Upbit's quote markets.
   - Stage C's name match uses CoinGecko's `name` verbatim, so «Gram (prev. Toncoin)» and
     «Artificial Superintelligence Alliance» match only as whole phrases.
3. **The per-coin summary is this report's aggregation.** B7 is defined per lane, and the TZ's
   output line asks for one row per coin. Medium's platform index is left out of the summary on
   a measured ground: 0 URLs under any of the seven publication paths. It is kept in the lane
   table with its own B7, and the tally including it is printed beside.

---

## Pre-existing Issues

1. **Status vocabulary.** Methodology §11 lists `неизмеримо` (neuter) among `coverage.status`'s
   three values. `analyst/state.json` holds **`неизмерима`** (feminine) on 5 coins: HYPE, XMR,
   LIT, MORPHO and ARB. A reader matching §11's word exactly finds `неизмеримо` in none of the
   30 records. This TZ forbids writing under `analyst/`, so it is not acted on.
2. **SKY's §6a lane host disallows every path to this client.** `forum.sky.money` redirects to
   `forum.skyeco.com` (§6a's own table). That host's robots.txt (`r058`) gives `googlebot`
   `Allow: /` and every other client, `User-agent: *`, `Disallow: /`. §6a reads `latest.json`
   there under no robots rule, while TZ-52's rule 4 would refuse the same path. Recorded, not
   acted on.
3. **The TZ's narrative and the state disagree on NEAR.** TZ §Objective dates NEAR's move 17.09.
   A3's record reads `+26.30% 2026-09-18`, `охвачена`, `carried_by` `gov.near.org`. B7 used the
   state's date, as the TZ requires.
4. **The map's §0 prose pairs for the three benches predate TZ-51's merge.** The map gives
   5830 / `a1b1ce27…`, 2513 / `622b844e…` and 540 / `28eb1949…`. The tree holds 5929 /
   `ac203e2dc54104b79e08186644337832`, 2578 / `101ec7304467ef966c661a1f5349ae14` and 643 /
   `ec82368f44356c34c656ebcbcb5733da`, which are TZ-51's post-change figures. None of the three
   is in §0's file table. Reported, not enforced, not acted on.

---

## Remaining Risks

- **A sitemap's `lastmod` may record an edit rather than a publication.** `ripple.com`'s post
  sitemap starts on 09-22, and whole files carry one serve-time stamp (Finding 6). A `dated`
  class and a `carried` verdict built on `lastmod` can therefore rest on an edit made after the
  event.
- **A reporter feed's window is one to two days.** Here it runs from 22.7 h to 48.4 h, with a
  union of 48.46 h. An event older than that is not in any of the four feeds, whatever it was.
- **Matching by symbol and name admits false hits.** In book yield, 9 of 15 titles match only
  through word collisions.
  Names like «Sky», «Render» and «Lighter» are common words, while «Gram (prev. Toncoin)» will
  almost never match.
- **Every reading is one sample.** A challenge, a 404 or a stamp read at 11:09–11:24Z on 25.09
  may differ the next day. The rule that forbids a retry is also the reason no second sample
  exists.
- **B7 inherits A3's move date.** A wrong date in the state becomes a wrong verdict here, and
  Pre-existing Issues 3 shows that the dates are not unanimous.
- **The candidates inherit CoinGecko's `links`** (Finding 9). A registry pointing at a trading
  app, a referral URL or a stale site produces a Stage B row that says nothing about where the
  protocol publishes.
- **This machine is not a runner.** Stage F's 200 from `fapi.binance.com` says nothing about
  what a GitHub-hosted runner receives (contract §7 item 9, inv. 24).

---

## Commit

A report commit, direct to `main` on the `CryptoReports/**` path (contract §8). Its contents are
this file only. The message is the TZ's `## Commit Message`, verbatim:

```
TZ-52: report — catalyst lanes and perpetual klines measured from the VPS

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
```

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

## CI Execution

**No workflow ran for this TZ.** No branch was pushed and no code path moved. The five
workflows' triggers, as read from the working tree in this session:

- `main.yml`: `push` to `main` with a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`, plus `workflow_dispatch`.
- `bench.yml`: `push` on `main` and `claude/**` with `'**.md'` in `paths-ignore`, plus
  `pull_request`.
- `calib.yml`: `workflow_dispatch`, plus `claude/**` pushes touching `bench/exhaustion_calib.py`
  or its own file.
- `journal.yml`: `schedule` (`0 13 * * *`) and `workflow_dispatch` only.
- `backtest_bench.yml`: `workflow_dispatch` only.

A commit that changes one `.md` file under `CryptoReports/` matches none of these triggers.

## Final Repository State

The fingerprints were taken against harness worktree branch
`worktree-bridge-cse_01T87syUKWGCQYE7sWfMqMHT`, which has no upstream. It stood at
`1d0cda91f1fd6717c72fb51b6e98a52a7b042b04`, the same commit as `origin/main` after the fetch. At
validation time its working tree differed from that commit only by this untracked report (V5).
The probe's scratch lived under `/tmp/tz52/`, outside the repository, and was removed before
this report was committed (V6).

**Where each block came from.** `report.py` filled these from their files, not by
transcription: every stage table, the reading ledger, the stage logs, the self-test and replay
output, and the two instrument sources. Byte identity of the sources was checked by MD5 before
V6. A short set of command blocks was copied from this session's terminal output into the
template. That set is V4's address check, V5 and V6. After V6, three more blocks were re-run
from the repository root and pasted as printed: Inbound Filing's `git log`, the client
identity, and the per-anchor block under `## Fingerprints`. All three are local and read-only,
and none makes a request. With the sources reproduced verbatim, each classification can be
re-derived from this report alone.

## Fingerprints

### `SYSTEM-MAP-CRYPTOCALCUL.md`

| | |
|---|---|
| Revision string in `## 0. Fingerprint` | `**Revision 2026-09-22-b.**` |
| Required by TZ-52's header | `**Revision 2026-09-22-b.**` — **match** |
| Lines | 2924 |
| MD5 | `48164d91da50acee233dcc810741cdd9` |

### Anchors

The list was cut from the map's own anchor table **by structure**: the header row at line 269,
its `|---|---|` separator, then every row up to the first non-table line. It was not cut by
matching anchor names. **The table carries 7 rows and 7 were compared.** Each row was confirmed
present in the TZ header as an identical table row, with `grep --fixed-strings --line-regexp`.
Each anchor was confirmed an exact, case-sensitive substring of the map with
`grep --fixed-strings --only-matching`, which prints the text it matched. Each anchor occurs
twice in the map: once as its own table row and once at its site. The TZ header carries no row
the map's table lacks.

| Anchor | In TZ header | In map | Lines in map (table · site) | Text the match returned |
|---|---|---|---|---|
| revision | yes | yes | 271 · 17 | `**Revision 2026-09-22-b.**` |
| direction engine | yes | yes | 272 · 1221 | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | yes | yes | 273 · 1611 | `### 3.15 Catalyst registry` |
| exhaustion measure | yes | yes | 274 · 1708 | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | yes | yes | 275 · 2700 | `## 11. Analytical engine` |
| squeeze block | yes | yes | 276 · 1875 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | yes | yes | 277 · 2417 | `72. **A write that fails leaves this run's product or nothing` |

The gate ran before any work, from `/tmp/tz52/gate.sh`, which V6 removed, and printed
`compared: 7   table rows: 7   in TZ header: 7   in map: 7` and
`TZ header rows not in map table: 0`. **Per anchor, the command and the text it returned**:
the block below re-runs the same cut and the same two matches from the repository root, with
each command printed with its anchor in place.

```
$ bash <<'EOF'
cut_rows() { awk 'f==0 && /^\| Anchor \|/{f=1;next} f==1 && /^\|---/{f=2;next} f==2 && /^\|/{print;next} f==2{exit}' "$1"; }
MAP=SYSTEM-MAP-CRYPTOCALCUL.md; TZ=CryptoTZ/TZ-52-catalyst-lanes-vps-measurement.md
echo "rows in the map's table: $(cut_rows $MAP | wc --lines); rows in the TZ header's table: $(cut_rows $TZ | wc --lines)"
cut_rows $MAP | while IFS= read -r row; do
  a=$(printf '%s' "$row" | sed -E 's/^\| [^|]+ \| `(.*)` \|$/\1/')
  echo "grep --fixed-strings --only-matching --max-count=1 -- \"$a\" $MAP"
  echo "  -> $(grep --fixed-strings --only-matching --max-count=1 -- "$a" $MAP | head --lines=1)"
  echo "  identical row in the TZ header (grep --fixed-strings --line-regexp --count): $(grep --fixed-strings --line-regexp --count -- "$row" $TZ)"
done
EOF
rows in the map's table: 7; rows in the TZ header's table: 7
grep --fixed-strings --only-matching --max-count=1 -- "**Revision 2026-09-22-b.**" SYSTEM-MAP-CRYPTOCALCUL.md
  -> **Revision 2026-09-22-b.**
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.12 Direction engine — veto cascade" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.12 Direction engine — veto cascade
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.15 Catalyst registry" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.15 Catalyst registry
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.16 List exhaustion — the day-range measure" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.16 List exhaustion — the day-range measure
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "## 11. Analytical engine" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ## 11. Analytical engine
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "### 3.17 «РИСК ВЫНОСА» — the day's own risk" SYSTEM-MAP-CRYPTOCALCUL.md
  -> ### 3.17 «РИСК ВЫНОСА» — the day's own risk
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
grep --fixed-strings --only-matching --max-count=1 -- "72. **A write that fails leaves this run's product or nothing" SYSTEM-MAP-CRYPTOCALCUL.md
  -> 72. **A write that fails leaves this run's product or nothing
  identical row in the TZ header (grep --fixed-strings --line-regexp --count): 1
```

### Files of the map's `## 0` table

Measured before the first read and unchanged by this work: no file outside `CryptoReports/`
was written.

| File | Lines (map) | Lines (measured) | MD5 (map) | MD5 (measured) | |
|---|---:|---:|---|---|---|
| `index.html` | 3799 | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

### Files TZ-52's header adds to the gate table (reported, not enforced)

| File | Lines (TZ) | Lines (measured) | MD5 (TZ) | MD5 (measured) | Revision line (TZ · measured) | |
|---|---:|---:|---|---|---|---|
| `ANALYST-INSTRUCTIONS.md` | 3465 | 3465 | `c72986bf15e70dcefe1256c4c0ac6126` | `c72986bf15e70dcefe1256c4c0ac6126` | `2026-09-30-a` · `**Revision 2026-09-30-a.**` | match |
| `EXECUTOR-INSTRUCTIONS.md` | 864 | 864 | `02abb1969626d2af150a0d1f6e02f2a7` | `02abb1969626d2af150a0d1f6e02f2a7` | `Version 23` · `**Version 23.**` | match |

Both match, so no quote in the TZ has moved. The six quotes were also checked as text (Scope
Executed, item 5).
