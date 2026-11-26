#!/usr/bin/env python3
"""The radar (TZ-86): twice a day, without the button, the list coins' own publications and the unlock index, read
by a program that runs no model and holds no credential. What is new since its previous read goes into a record,
and one alert reaches the owner when a read found something: a release or a post of the protocol's own site whose
title names a kind of the STRONG sweep -- partnership, integration, listing, mainnet, upgrade --, with the book's view
of the coin at its last price, and a material cliff inside the holding window. A forum topic is recorded and never
alerted: a forum carries its participants' posts, not the protocol's own record (methodology section 6a). The alert
starts no run: the owner decides whether to press.
    radar.py [--state-dir DIR] [--outbox DIR] [--tree DIR]   the pass; crypto-radar.timer, 08:00 and 20:00 Tbilisi
    radar.py --probe [--tree DIR]                             one read of every lane, its counts printed; writes nothing
What a pass decides by is cut at run time from the file that owns it and typed nowhere here: section 6a's channel
table, its sitemap words and UNLOCK_MATERIAL, the holding window and the STRONG sweep's words from
ANALYST-INSTRUCTIONS.md; the CoinGecko ids from main.py's TOKENS; the perpetuals from index.html's tokens[]. Every
read is the methodology's measured command, curl -sS -L -m <s>, its timeouts and refusal codes the constants below,
one request a channel, taken only where it lands on the row's own host and where its host's robots.txt, read first,
permits the path (RFC 9309). The book's view is
book.card_of() on book.state_of() -- the run's own cards' function (methodology section 4). A channel's first read
is its baseline and reports nothing new. Python 3.12's standard library and curl.
Exit 0 a lane read, the record written \u00b7 4 no lane read, the record written with every refusal \u00b7 2 the tree unread.
"""
import argparse
import ast
import email.utils
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.robotparser
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import announce  # noqa: E402
import book  # noqa: E402
import common  # noqa: E402
import score  # noqa: E402

METHODOLOGY = "ANALYST-INSTRUCTIONS.md"
RECORD = "radar.json"
STATE = "radar-state.json"
CHANNEL_S = 20                 # methodology section 6a: every channel row was measured as curl -sS -L -m 20
INDEX_S = 60                   # section 6a's unlock command: curl -sS -L -m 60
INDEX_URL = "https://defillama-datasets.llama.fi/emissionsIndex"
INDEX_HOST = "defillama-datasets.llama.fi"
WRITE_OUT = "%{http_code} %{url_effective} %{size_download}"
ROBOTS_AGENT = "curl"          # the product token of the measured client
HOLD_CODES = (403, 418, 429, 451)   # a host refusing so is asked nothing more this pass (methodology section 16)
SLACK_MS = 86_400_000          # a sitemap dates a record by its day, so a record a day older than the last read is new
DAY_MS = 86_400_000

R_HEAD = "\U0001f4e1 **\u0420\u0410\u0414\u0410\u0420** \u00b7 {ddmm} {hhmm} \u0422\u0431\u0438\u043b\u0438\u0441\u0438"
R_POST = "\U0001f7e2 **{sym}** \u00b7 {kinds} \u00b7 {host} \u00b7 {when} UTC"
R_CLIFF = "\U0001f534 **{sym}** \u00b7 \u0440\u0430\u0437\u043b\u043e\u043a {pct}% \u043f\u0440\u0435\u0434\u043b\u043e\u0436\u0435\u043d\u0438\u044f \u00b7 {when} UTC \u00b7 {to}"
R_FOOT = "\u041d\u0435 \u0441\u0434\u0435\u043b\u043a\u0430: \u043f\u043e\u0432\u043e\u0434 \u043d\u0430\u0436\u0430\u0442\u044c \u00ab\u0410\u043d\u0430\u043b\u0438\u0437 \u0440\u044b\u043d\u043a\u0430\u00bb."
KIND_RU = {"partnership": "\u043f\u0430\u0440\u0442\u043d\u0451\u0440\u0441\u0442\u0432\u043e", "integration": "\u0438\u043d\u0442\u0435\u0433\u0440\u0430\u0446\u0438\u044f", "listing": "\u043b\u0438\u0441\u0442\u0438\u043d\u0433",
           "mainnet": "\u043c\u0435\u0439\u043d\u043d\u0435\u0442", "upgrade": "\u043e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435"}
H_UNREAD = "\u21b3 \u0446\u0435\u043d\u0430 \u043d\u0435 \u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u0430"
H_SHORT = "\u21b3 \u0438\u0441\u0442\u043e\u0440\u0438\u044f \u043a\u043e\u0440\u043e\u0447\u0435 \u043e\u043a\u043d\u0430 \u043a\u043d\u0438\u0433\u0438 \u2014 \u043a\u043d\u0438\u0433\u0430 \u043c\u043e\u043b\u0447\u0438\u0442"
H_EXIT = "\u21b3 \u0442\u0440\u0435\u043d\u0434 \u0437\u0430\u043a\u0440\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u0441\u0435\u0433\u043e\u0434\u043d\u044f \u2014 \u0432\u0445\u043e\u0434\u0430 \u043d\u0435\u0442"
H_FLAT = "\u21b3 \u0432\u043d\u0435 \u0442\u0440\u0435\u043d\u0434\u0430 \u00b7 \u043b\u043e\u043d\u0433 \u2014 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f \u0432\u044b\u0448\u0435 `{trigger}`, {d} ATR \u043e\u0442 \u0446\u0435\u043d\u044b"
H_BREAK = "\u21b3 \u043f\u0440\u043e\u0431\u043e\u0439 \u0438\u0434\u0451\u0442: \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f \u0432\u044b\u0448\u0435 `{trigger}` \u043e\u0442\u043a\u0440\u043e\u0435\u0442 \u043b\u043e\u043d\u0433"
H_ENTRY = "\u21b3 \u0441\u0438\u0433\u043d\u0430\u043b: {side} \u0441\u0435\u0433\u043e\u0434\u043d\u044f \u00b7 \u0432\u0445\u043e\u0434 \u043e\u0442\u043a\u0440\u044b\u0442, {bound} `{void}` \u00b7 \u0441\u0442\u043e\u043f `{stop}`"
H_NEAR = "\u21b3 \u0441\u0438\u0433\u043d\u0430\u043b: {side} \u0441\u0435\u0433\u043e\u0434\u043d\u044f, \u043d\u043e \u0446\u0435\u043d\u0430 \u0443 \u0441\u0442\u043e\u043f\u0430 \u2014 \u0432\u0445\u043e\u0434 \u043f\u043e \u043f\u0440\u0430\u0432\u0438\u043b\u0443 \u0437\u0430\u043a\u0440\u044b\u0442"
H_CLOSED = "\u21b3 \u0446\u0435\u043d\u0430 \u0437\u0430 \u0441\u0442\u043e\u043f\u043e\u043c \u0441\u0438\u0433\u043d\u0430\u043b\u0430 \u2014 \u0432\u0445\u043e\u0434\u0430 \u043d\u0435\u0442"
H_HOLD = "\u21b3 \u0443\u0436\u0435 \u0432 \u0442\u0440\u0435\u043d\u0434\u0435: {side} \u0441 {date} \u2014 \u043f\u043e\u0437\u0434\u043d\u0438\u0439 \u0432\u0445\u043e\u0434 \u043d\u0430 \u0438\u0441\u0442\u043e\u0440\u0438\u0438 \u0443\u0431\u044b\u0442\u043e\u0447\u0435\u043d, \u043a\u043d\u0438\u0433\u0430 \u0435\u0433\u043e \u043d\u0435 \u0434\u0430\u0451\u0442"
BOUND = {1: "\u043d\u0435 \u043d\u0438\u0436\u0435", -1: "\u043d\u0435 \u0432\u044b\u0448\u0435"}


class TreeUnreadable(Exception):
    pass


class Refused(Exception):
    """One lane refused: the reason, in the closed vocabulary HTTP <status> \u00b7 held HTTP <status> \u00b7 transport \u00b7
    landed <host> \u00b7 robots \u00b7 robots unreachable \u00b7 unparseable \u00b7 shape \u00b7 sitemap index; and the host it landed on,
    where it landed."""

    def __init__(self, reason, host=None):
        super().__init__(reason)
        self.host = host


# --- the rules, cut from the files that own them (inv. 21, 38) -----------------------------------------
_CHANNEL_HEAD = "| Coin | Class | Request | Answers from |"
_CHANNEL_ROW = re.compile(r"^\| ([A-Z0-9]+) \| ([1-3]) \u00b7 ([a-z]+) \| `(https://[^`\s]+)` \| \*{0,2}`([a-z0-9.-]+)`")
_NUMBERS = {w: i for i, w in enumerate("one two three four five six seven eight nine ten eleven twelve thirteen "
                                       "fourteen".split(), 1)}


def cut_channels(text):
    """Section 6a's channel table in its order: each row's coin, class, request and the host it answers from, and
    its lane, <coin>|<k> for the coin's k-th row. A table absent or twice, or a row the pattern does not read,
    fails (inv. 22)."""
    lines = text.splitlines()
    if lines.count(_CHANNEL_HEAD) != 1:
        raise TreeUnreadable("channel table: %d headers" % lines.count(_CHANNEL_HEAD))
    i = lines.index(_CHANNEL_HEAD) + 2
    rows, per = [], {}
    while i < len(lines) and lines[i].startswith("| "):
        m = _CHANNEL_ROW.match(lines[i])
        if m is None:
            raise TreeUnreadable("channel table: row %d unread" % (len(rows) + 1))
        coin, n, kind, request, host = m.groups()
        per[coin] = per.get(coin, 0) + 1
        rows.append(dict(coin=coin, cls=int(n), kind=kind, request=request, host=host,
                         lane="%s|%d" % (coin, per[coin])))
        i += 1
    if not rows:
        raise TreeUnreadable("channel table: no row")
    return rows


def _one(pattern, text, what):
    found = re.findall(pattern, text, re.M)
    if len(found) != 1:
        raise TreeUnreadable("%s: %d definitions" % (what, len(found)))
    return found[0]


def cut_window(text):
    """The holding window, in days (methodology section 6)."""
    word = _one(r"the holding window, ([a-z]+) days from the freeze", text, "the holding window")
    if word not in _NUMBERS:
        raise TreeUnreadable("the holding window: %r" % word)
    return _NUMBERS[word]


def cut_material(text):
    """UNLOCK_MATERIAL, in per cent of the supply the dataset counts as circulating (section 6a)."""
    return float(_one(r"\*\*`UNLOCK_MATERIAL` = ([0-9]+(?:\.[0-9]+)?) %", text, "UNLOCK_MATERIAL"))


def cut_kinds(text):
    """The STRONG sweep's words (section 16 S), in its order."""
    query = _one(r"\u00ab<project> ([a-z]+(?:\s+OR\s+[a-z]+)+)\u00bb", text, "the STRONG sweep's query")
    return re.split(r"\s+OR\s+", query)


def cut_paths(text):
    """The record list's sitemap words (section 6a): a sitemap's records are its urls whose lower-cased path
    contains one of them, and every url where none does."""
    cell = _one(r"^\| 3 \u00b7 site, sitemap \| [^|]*?contains ([^|]*?) \u2014", text, "the sitemap row")
    words = re.findall(r"`([a-z]+)`", cell)
    if not words:
        raise TreeUnreadable("the sitemap row names no word")
    return words


def cut_ids(main_py):
    """main.py's TOKENS, coin -> CoinGecko id, read by the parser and never executed."""
    for node in ast.parse(main_py).body:
        if isinstance(node, ast.Assign) and [getattr(t, "id", None) for t in node.targets] == ["TOKENS"]:
            ids = ast.literal_eval(node.value)
            if isinstance(ids, dict) and ids and all(isinstance(k, str) and isinstance(v, str)
                                                    for k, v in ids.items()):
                return ids
    raise TreeUnreadable("main.py: TOKENS unread")


def read_rules(tree):
    with open(os.path.join(tree, METHODOLOGY), encoding="utf-8") as fh:
        text = fh.read()
    with open(os.path.join(tree, "main.py"), encoding="utf-8") as fh:
        ids = cut_ids(fh.read())
    with open(os.path.join(tree, "index.html"), encoding="utf-8") as fh:
        symbols = {row["name"]: row["s"] for row in common.cut_tokens(fh.read())}
    return dict(channels=cut_channels(text), window=cut_window(text), material=cut_material(text),
                kinds=cut_kinds(text), paths=cut_paths(text), ids=ids, symbols=symbols)


# --- one read, in the measured form -------------------------------------------------------------------------
def fetch(url, timeout, path):
    """One request as methodology section 6a measured it, curl -sS -L -m <timeout>, the body to path: (status, the
    URL it landed on, bytes). Status 0 is curl's own failure, a refusal by transport."""
    try:
        proc = subprocess.run(["curl", "-sS", "-L", "-m", str(timeout), "-o", path, "-w", WRITE_OUT, url],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=timeout + 15)
    except (OSError, subprocess.TimeoutExpired):
        return 0, url, 0
    parts = proc.stdout.split()
    if proc.returncode != 0 or len(parts) != 3 or not parts[0].isdigit():
        return 0, parts[1] if len(parts) == 3 else url, 0
    return int(parts[0]), parts[1], int(parts[2]) if parts[2].isdigit() else 0


def host_of(url):
    return urllib.parse.urlsplit(url).hostname or ""


def robots(host, tmp, cache):
    """What this pass may read on host (RFC 9309), from one read of its robots.txt a pass: a parser on 200, True --
    every path -- on another 4xx, None -- no path -- on a 5xx or no answer."""
    if host not in cache:
        path = os.path.join(tmp, "robots")
        status, _landed, _n = fetch("https://%s/robots.txt" % host, CHANNEL_S, path)
        if status == 200:
            rule = urllib.robotparser.RobotFileParser()
            with open(path, encoding="utf-8", errors="replace") as fh:
                rule.parse(fh.read().splitlines())
            rule.modified()
            cache[host] = rule
        else:
            cache[host] = True if 400 <= status < 500 else None
    return cache[host]


def allowed(rule, url):
    """True, False, or None where the host's robots.txt did not answer."""
    if rule is None or rule is True:
        return rule
    return rule.can_fetch(ROBOTS_AGENT, url)


# --- a page's records (section 6a's record list) ----------------------------------------------------------------
def when(text):
    """An ISO 8601 date or time, UTC where it names no zone, in ms; None where it is not one."""
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        t = datetime.fromisoformat(text.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return int(t.timestamp() * 1000)


def when_rfc822(text):
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        t = email.utils.parsedate_to_datetime(text.strip())
    except (TypeError, ValueError, IndexError):
        return None
    if t is None:
        return None
    if t.tzinfo is None:
        t = t.replace(tzinfo=timezone.utc)
    return int(t.timestamp() * 1000)


def _json(blob):
    try:
        return json.loads(blob.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise Refused("unparseable") from None


def _slug_title(url):
    parts = [p for p in urllib.parse.urlsplit(url).path.split("/") if p]
    return re.sub(r"[-_]+", " ", parts[-1]) if parts else url


def parse_page(row, host, blob, paths):
    """One page of one channel: (records, the oldest window date in ms or None). A record is a dict of key, ms --
    its record date --, title and url; a record with no date is not one."""
    out, window = [], []
    if row["cls"] == 1:
        doc = _json(blob)
        topics = (doc.get("topic_list") or {}).get("topics") if isinstance(doc, dict) else None
        if not isinstance(topics, list):
            raise Refused("shape", host)
        for t in topics:
            if not isinstance(t, dict) or t.get("pinned") or t.get("pinned_globally"):
                continue
            ms, tid = when(t.get("created_at")), t.get("id")
            if ms is None or not isinstance(tid, int) or isinstance(tid, bool):
                continue
            out.append(dict(key=str(tid), ms=ms, title=str(t.get("title") or ""),
                            url="https://%s/t/%s/%d" % (host, t.get("slug") or "-", tid)))
            bumped = when(t.get("bumped_at"))
            window.append(ms if bumped is None else bumped)
    elif row["cls"] == 2:
        doc = _json(blob)
        if not isinstance(doc, list):
            raise Refused("shape", host)
        gitlab = host == "gitlab.com"
        for r in doc:
            if not isinstance(r, dict) or r.get("draft"):
                continue
            ms = when(r.get("released_at" if gitlab else "published_at"))
            if ms is None:
                continue
            url = ((r.get("_links") or {}).get("self") if gitlab else r.get("html_url")) or row["request"]
            out.append(dict(key=str(r.get("tag_name") or url), ms=ms,
                            title=str(r.get("name") or r.get("tag_name") or ""), url=str(url)))
            window.append(ms)
    else:
        try:
            root = ET.fromstring(blob)
        except ET.ParseError:
            raise Refused("unparseable", host) from None
        tag = root.tag.rsplit("}", 1)[-1]
        ns = root.tag[:len(root.tag) - len(tag)]
        if tag == "rss":
            for item in root.findall("./channel/item"):
                ms, link = when_rfc822(item.findtext("pubDate")), (item.findtext("link") or "").strip()
                if ms is None or not link:
                    continue
                out.append(dict(key=(item.findtext("guid") or link).strip(), ms=ms,
                                title=(item.findtext("title") or "").strip(), url=link))
                window.append(ms)
        elif tag == "urlset":
            urls = []
            for u in root.findall(ns + "url"):
                loc, ms = (u.findtext(ns + "loc") or "").strip(), when(u.findtext(ns + "lastmod"))
                if loc and ms is not None:
                    urls.append((loc, ms))
            picked = [x for x in urls if any(w in urllib.parse.urlsplit(x[0]).path.lower() for w in paths)] or urls
            for loc, ms in picked:
                out.append(dict(key=loc, ms=ms, title=_slug_title(loc), url=loc))
                window.append(ms)
        elif tag == "sitemapindex":
            raise Refused("sitemap index", host)
        else:
            raise Refused("shape", host)
    return out, (min(window) if window else None)


def read_channel(row, tmp, cache, paths, held=None):
    """One read of one channel row: (records, window, the host it landed on, bytes), or Refused. A host that
    refused with a code of HOLD_CODES is held for the pass: its next rows are refused unasked -- the eleven GitHub
    rows are one host with one quota (section 6a)."""
    held = {} if held is None else held
    asked = host_of(row["request"])
    if asked in held:
        raise Refused("held HTTP %d" % held[asked], asked)
    permitted = allowed(robots(asked, tmp, cache), row["request"])
    if permitted is None:
        raise Refused("robots unreachable")
    if not permitted:
        raise Refused("robots")
    path = os.path.join(tmp, "page")
    status, landed, size = fetch(row["request"], CHANNEL_S, path)
    host = host_of(landed)
    if status == 0:
        raise Refused("transport", host)
    if status in HOLD_CODES:
        held[asked] = status
    if status != 200:
        raise Refused("HTTP %d" % status, host)
    if host != row["host"]:
        raise Refused("landed %s" % host, host)
    with open(path, "rb") as fh:
        blob = fh.read()
    records, frm = parse_page(row, host, blob, paths)
    return records, frm, host, size


def digest(key):
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:12]


def fresh(records, prev):
    """The records a channel did not carry at its previous read and dated after a day before it; none at a first
    read, which is the channel's baseline."""
    if not prev:
        return []
    seen = set(prev.get("seen") or ())
    return [r for r in records if digest(r["key"]) not in seen and r["ms"] > prev["d"] - SLACK_MS]


def stem(word):
    for suffix in ("ship", "ion", "ing"):
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            word = word[:-len(suffix)]
            break
    return word[:-1] if word.endswith("e") else word


def kinds_of(title, kinds):
    """The kinds a title names: a word of it beginning with the kind's stem."""
    words = re.findall(r"[a-z0-9]+", title.lower())
    return [k for k in kinds if any(w.startswith(stem(k)) for w in words)]


# --- the unlock lane (section 6a), row by row -----------------------------------------------------------------
def finite(value):
    if value is None or isinstance(value, bool):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def index_rows(text):
    """Every element of the document's "data" array, one json.JSONDecoder.raw_decode at a time and never the whole
    document at once (section 6a)."""
    m = re.match(r'\s*\{\s*"data"\s*:\s*\[', text)
    if m is None:
        raise Refused("shape", INDEX_HOST)
    decoder, pos, skip = json.JSONDecoder(), m.end(), re.compile(r"[\s,]*")
    while True:
        pos = skip.match(text, pos).end()
        if pos >= len(text):
            raise Refused("unparseable", INDEX_HOST)
        if text[pos] == "]":
            return
        try:
            row, pos = decoder.raw_decode(text, pos)
        except ValueError:
            raise Refused("unparseable", INDEX_HOST) from None
        yield row


def iso_s(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def unlocks(rows, ids, now_s):
    """Each coin's next cliff: the earliest unlockEvents[] entry after now with cliffAllocations not empty, on the
    row whose gecko_id is the coin's id -- next, no cliff or not covered. A document in which no row carries
    gecko_id and unlockEvents has changed shape (inv. 22)."""
    by_id, out, shaped = {}, {}, False
    for sym, gid in ids.items():
        by_id.setdefault(gid, []).append(sym)
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("gecko_id"), str) \
                or not isinstance(row.get("unlockEvents"), list):
            continue
        shaped = True
        for sym in by_id.get(row["gecko_id"], ()):
            nxt = None
            for e in row["unlockEvents"]:
                ts = e.get("timestamp") if isinstance(e, dict) else None
                if isinstance(ts, bool) or not isinstance(ts, (int, float)) or ts <= now_s \
                        or not e.get("cliffAllocations"):
                    continue
                if nxt is None or ts < nxt["timestamp"]:
                    nxt = e
            prev = out.get(sym)
            if nxt is None:
                out.setdefault(sym, {"status": "no cliff"})
                continue
            if prev is not None and prev["status"] == "next" and prev["t"] <= nxt["timestamp"]:
                continue
            n, rel = finite((nxt.get("summary") or {}).get("totalTokensCliff")), finite(row.get("circSupply"))
            names = []
            for a in nxt["cliffAllocations"]:
                name = a.get("recipient") if isinstance(a, dict) else None
                if isinstance(name, str) and name and name not in names:
                    names.append(name)
            out[sym] = {"status": "next", "t": int(nxt["timestamp"]), "ud": iso_s(nxt["timestamp"]), "n": n,
                        "to": ", ".join(names), "rel": rel,
                        "pct": round(n / rel * 100, 1) if n is not None and rel and rel > 0 else None}
    if not shaped:
        raise Refused("shape", INDEX_HOST)
    for sym in ids:
        out.setdefault(sym, {"status": "not covered"})
    return out


def read_unlocks(ids, now_ms, tmp):
    path = os.path.join(tmp, "index")
    status, landed, size = fetch(INDEX_URL, INDEX_S, path)
    host = host_of(landed)
    if status == 0:
        raise Refused("transport", host)
    if status != 200:
        raise Refused("HTTP %d" % status, host)
    if host != INDEX_HOST:
        raise Refused("landed %s" % host, host)
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    os.unlink(path)
    return {"host": host, "bytes": size, "coins": unlocks(index_rows(text), ids, now_ms // 1000)}


# --- the book's view of a coin at its last price ------------------------------------------------------------------
def heat(symbol, now_ms):
    """card_of() on the rule's state, at the forming day's last price -- the function every card of the run comes
    from (book.py, methodology section 4)."""
    try:
        bars, today = book.live_day(symbol, now_ms)
        state, _trades, _pos = book.state_of(symbol, bars, today[1])
    except Exception as exc:
        return {"state": "unread", "error": exc.__class__.__name__}
    card = book.card_of(state, today[4], today) if state.get("state") in ("long", "short", "flat") else None
    return {"state": state.get("state"), "p": today[4], "card": card,
            "entry_date": state.get("entry_date"), "exit_due": bool(state.get("exit_due"))}


def heat_text(h):
    st, card = h.get("state"), h.get("card")
    if st == "unread" or st is None:
        return H_UNREAD
    if st == "short-history":
        return H_SHORT
    side = 1 if st == "long" else -1
    if st == "flat":
        if not card:
            return H_SHORT
        if h["p"] >= card["long"]["anchor"]:
            return H_BREAK.format(trigger=score.px(card["long"]["anchor"]))
        return H_FLAT.format(trigger=score.px(card["long"]["anchor"]), d="%.1f" % card["long"]["d"])
    if h.get("exit_due") or not card:
        return H_EXIT
    if card["kind"] == "late":
        return H_HOLD.format(side=score.SIDE[side], date=score.ddmm(h.get("entry_date") or "0000-00-00"))
    if card.get("band") == "closed":
        return H_CLOSED
    if card.get("band") == "near":
        return H_NEAR.format(side=score.SIDE[side])
    return H_ENTRY.format(side=score.SIDE[side], bound=BOUND[side], void=score.px(card["void"]),
                          stop=score.px(card["stop"]))


# --- the pass ------------------------------------------------------------------------------------------------
def iso(ms):
    return None if ms is None else datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_pass(rules, state, now_ms, tmp):
    """Every lane once: (the record, the count of lanes read). state is updated in place: each channel read keeps
    its page's digests and the moment, and every cliff alerted is kept until it passes."""
    record = {"v": 1, "k": "radar", "ts": iso(now_ms), "window": rules["window"], "material": rules["material"],
              "kinds": rules["kinds"], "channels": {}, "unlock": None, "found": []}
    channels = state.setdefault("channels", {})
    cache, held, read = {}, {}, 0
    for row in rules["channels"]:
        lane = row["lane"]
        try:
            records, frm, host, size = read_channel(row, tmp, cache, rules["paths"], held)
        except Refused as exc:
            record["channels"][lane] = {"host": exc.host, "refused": str(exc)}
            continue
        read += 1
        new = fresh(records, channels.get(lane))
        record["channels"][lane] = {"host": host, "bytes": size, "n": len(records), "from": iso(frm),
                                    "new": len(new), "baseline": lane not in channels}
        channels[lane] = {"d": now_ms, "seen": sorted({digest(r["key"]) for r in records})}
        for r in sorted(new, key=lambda r: r["ms"]):
            k = kinds_of(r["title"], rules["kinds"])
            record["found"].append({"lane": lane, "sym": row["coin"], "class": row["kind"], "host": host,
                                    "date": iso(r["ms"]), "title": r["title"], "url": r["url"], "kinds": k,
                                    "alert": bool(k) and row["cls"] != 1})
    alerted = {key: t for key, t in (state.get("alerted") or {}).items() if t * 1000 > now_ms}
    try:
        record["unlock"] = read_unlocks(rules["ids"], now_ms, tmp)
        read += 1
    except Refused as exc:
        record["unlock"] = {"host": exc.host, "refused": str(exc)}
    for sym, e in sorted((record["unlock"] or {}).get("coins", {}).items()):
        if e["status"] != "next" or e["pct"] is None or e["pct"] < rules["material"] \
                or e["t"] * 1000 > now_ms + rules["window"] * DAY_MS:
            continue
        key = "%s|%d" % (sym, e["t"])
        record["found"].append({"lane": "unlock", "sym": sym, "date": e["ud"], "pct": e["pct"], "to": e["to"],
                                "alert": key not in alerted})
        alerted[key] = e["t"]
    state["alerted"] = alerted
    views = {}
    for f in record["found"]:
        if f["lane"] != "unlock" and f["alert"]:
            if f["sym"] not in views:
                sym = rules["symbols"].get(f["sym"])
                views[f["sym"]] = heat(sym, now_ms) if sym else {"state": "unread", "error": "no perpetual"}
            f["heat"] = views[f["sym"]]
    return record, read


def when_text(iso_text):
    return iso_text[8:10] + "." + iso_text[5:7] + " " + iso_text[11:16]


def alert_text(record, now_ms):
    """The one alert of a pass, or None where nothing it found is alerted."""
    lines = []
    for f in record["found"]:
        if not f["alert"]:
            continue
        if f["lane"] == "unlock":
            lines.append(R_CLIFF.format(sym=f["sym"], pct=("%.1f" % f["pct"]), when=when_text(f["date"]),
                                        to=f["to"] or "\u2014"))
            continue
        lines.append(R_POST.format(sym=f["sym"], kinds=", ".join(KIND_RU.get(k, k) for k in f["kinds"]),
                                   host=f["host"], when=when_text(f["date"])))
        lines.extend([f["title"], f["url"], heat_text(f["heat"])])
    if not lines:
        return None
    local = datetime.fromtimestamp(now_ms / 1000, tz=announce.TBILISI)
    return "\n".join([R_HEAD.format(ddmm=local.strftime("%d.%m"), hhmm=local.strftime("%H:%M"))] + lines + [R_FOOT])


def load_state(path):
    try:
        with open(path, encoding="utf-8") as fh:
            state = json.load(fh)
    except FileNotFoundError:
        return {}
    except (OSError, ValueError):
        common.log("radar: state unreadable, every channel reads as a baseline")
        return {}
    return state if isinstance(state, dict) else {}


def main(argv=None):
    parser = argparse.ArgumentParser(description="The radar: publications and unlocks, twice a day, no model")
    parser.add_argument("--state-dir", default=common.STATE_DIR)
    parser.add_argument("--outbox", default=None)
    parser.add_argument("--tree", default=os.path.dirname(common.index_html_path()))
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args(argv)
    try:
        rules = read_rules(args.tree)
    except (OSError, ValueError, SyntaxError, TreeUnreadable, common.TokensUnreadable) as exc:
        common.log("radar: tree unread: %s" % exc)
        return 2
    now_ms = int(time.time() * 1000)
    state_path = os.path.join(args.state_dir, STATE)
    state = {} if args.probe else load_state(state_path)
    with tempfile.TemporaryDirectory(prefix="radar-") as tmp:
        record, read = run_pass(rules, state, now_ms, tmp)
    refused = sum(1 for c in record["channels"].values() if "refused" in c)
    unlock = record["unlock"].get("refused") or "read"
    if args.probe:
        for lane, c in record["channels"].items():
            common.log("radar-probe:", lane, c.get("host") or "-", c.get("refused") or "200",
                       "n=%s" % c.get("n", "-"), "from=%s" % c.get("from", "-"))
        coins = (record["unlock"] or {}).get("coins") or {}
        counts = {}
        for e in coins.values():
            counts[e["status"]] = counts.get(e["status"], 0) + 1
        common.log("radar-probe: unlock", record["unlock"].get("host") or "-", unlock,
                   " ".join("%s=%d" % kv for kv in sorted(counts.items())))
        common.log("radar-probe: channels=%d read=%d refused=%d unlock=%s"
                   % (len(record["channels"]), len(record["channels"]) - refused, refused, unlock))
        return 0 if read else 4
    text = alert_text(record, now_ms)
    common.atomic_write(os.path.join(args.state_dir, RECORD), record, mode=0o640)
    if text:
        common.write_outbox("alert", text, args.outbox)
    common.atomic_write(state_path, state, mode=0o640)
    common.log("radar: channels=%d refused=%d found=%d alerted=%d unlock=%s"
               % (len(record["channels"]), refused, len(record["found"]),
                  sum(1 for f in record["found"] if f["alert"]), unlock))
    return 0 if read else 4


if __name__ == "__main__":
    sys.exit(main())
