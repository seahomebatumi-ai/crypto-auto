#!/usr/bin/env python3
"""The copy-trading paper test (TZ-64; map section 10, row \u00abHyperliquid's large accounts\u00bb):
Hyperliquid accounts selected once by their twelve-month record, followed in real time,
every copied episode booked on Binance USD-M prices at four delays, and the verdict
read at week 13 against random eligible accounts copied the same way.

    paper.py [--state-dir <dir>] [--tree <dir>]      the service
    paper.py --probe                                  one read of every interface; counts only

Python 3.12's standard library only. Holds no credential but the deploy key its unit
passes to git, and prints no value. Alerts the owner through the outbox for the
selected accounts only, and requests no run. Its records are written under
analyst/paper/ of its own clone and pushed to main (contract v30 section 8); a record
is written once and never reopened.
"""
import argparse
import bisect
import codecs
import hashlib
import http.client
import io
import json
import math
import os
import resource
import shutil
import statistics
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import announce  # noqa: E402
import common  # noqa: E402
import exchange  # noqa: E402

INFO_URL = "https://api.hyperliquid.xyz/info"
LEADERBOARD_URL = "https://stats-data.hyperliquid.xyz/Mainnet/leaderboard"
VISION = "https://data.binance.vision/data/futures/um"

# --- The rule, registered by TZ-64 before any data: moved only by a TZ, never after a reading.
POOL_VOLUME_MIN = 200e6       # all-time volume on the leaderboard, USD
LOOKBACK_WEEKS = 52
BLOCK_WEEKS = 4               # thirteen blocks of four weeks
BLOCKS_MIN = 10               # positive blocks of thirteen
DRAWDOWN_MAX = 0.25
VALUE_MIN_WEEK = 10000.0      # account value at every lookback week's start, USD
VALUE_MIN_T0 = 50000.0        # account value at T0, USD
TURNOVER_MAX = 10.0           # perpetual volume per day over the mean account value, last month
TOP_K = 3
NULL_M = 30
WINDOW_DAYS = 91              # thirteen weeks: the follow window, and the copyability window before T0
VENUE_SHARE_MIN = 0.80
DELAYS_S = (5, 300, 1800, 7200)
DECIDING_S = (1800, 7200)
SIGMA_DAYS = 30
EPISODES_MIN = 30
NULL_MIN = 10
ALERT_MAX_AGE_S = 600
PROBE_ACCOUNT = "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1"   # the reading's first account

# --- Operation.
WEIGHT_PER_MIN = 600          # half the info API's documented 1 200 per IP per minute: at 900 the
                              # Architect's workspace met runs of 429 answers on 16.10.2026
INFO_WEIGHT = 20              # documented weight of portfolio and userFillsByTime
FILLS_PAGE = 2000             # documented maximum fills per userFillsByTime answer
FILL_KEYS = ("coin", "px", "sz", "side", "time", "startPosition", "tid")   # all a fill is read for
PICK_POLL_S = 30
NULL_POLL_S = 600
DAY_SETTLE_S = 600            # a day is written once every account was polled this long after it ended
ABSENT_AFTER_DAYS = 3         # a 404 for a file dated further back is an absence, nearer is unpublished
WORK_EVERY_S = 3600           # booking, funding and the verdict are attempted hourly
PUBLISH_EVERY_S = 300
TRANSPORT_MAX = 30            # consecutive transport failures on one selection step
TRANSPORT_WAIT_S = 60
LOOP_S = 5
DAY_MS = 86400000
WEEK_MS = 7 * DAY_MS
STATE_DIR = "/var/lib/cryptopaper"
TREE = STATE_DIR + "/crypto-auto"
RECORD_DIR = "analyst/paper"
DEPLOYED_TREE = os.path.join(common.STATE_DIR, "deployed-vps-tree")
REPO = os.path.dirname(common.VPS_DIR)

# --- TZ-64 section 12.1, character for character.
P_OPEN = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
          "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
          "\u043e\u0442\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0441\u0442\u043e\u043f "
          "{dist}% \u2192 {stop} \u00b7 \u043e\u0431\u044a\u0451\u043c {notional} USDT \u043f\u0440\u0438 "
          "\u0440\u0438\u0441\u043a\u0435 {risk}% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430")
P_OPEN_BARE = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
               "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
               "\u043e\u0442\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0441\u0442\u043e\u043f "
               "\u0438 \u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: "
               "\u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance")
P_CLOSE = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
           "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
           "\u0437\u0430\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0432 "
           "\u043f\u043e\u0437\u0438\u0446\u0438\u0438 {held}")
N_START = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440"
           "\u043e\u0432\u0430\u043d\u0438\u044f \u043d\u0430\u0447\u0430\u0442: \u043e\u0442\u043e\u0431\u0440\u0430"
           "\u043d\u043e \u0441\u0447\u0435\u0442\u043e\u0432 Hyperliquid \u2014 {k}, \u043e\u043a\u043d\u043e 13 "
           "\u043d\u0435\u0434\u0435\u043b\u044c, \u0434\u043e {date}. \u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438"
           "\u044f \u0441 \u043f\u043e\u043c\u0435\u0442\u043a\u043e\u0439 \u00ab\u0411\u0443\u043c\u0430\u0436\u043d"
           "\u044b\u0439 \u0442\u0435\u0441\u0442\u00bb \u2014 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 "
           "\u043c\u0435\u0442\u043e\u0434\u0430 \u0434\u043e \u0440\u0435\u0448\u0435\u043d\u0438\u044f \u043e "
           "\u043f\u0438\u043b\u043e\u0442\u0435.")
N_NONE = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043d\u0435 \u043d\u0430\u0447\u0430\u0442: \u043e\u0442\u0431\u043e\u0440 Hyperliquid \u043d\u0435 \u0434\u0430\u043b \u043d\u0443\u0436\u043d\u043e\u0433\u043e \u0447\u0438\u0441\u043b\u0430 \u0441\u0447\u0435\u0442\u043e\u0432.")
N_CLOSED = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440"
            "\u043e\u0432\u0430\u043d\u0438\u044f: 13 \u043d\u0435\u0434\u0435\u043b\u044c \u043f\u0440\u043e\u0448"
            "\u043b\u0438, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u043e\u0441\u0442\u0430\u043d"
            "\u043e\u0432\u043b\u0435\u043d\u044b. \u0418\u0442\u043e\u0433 \u2014 \u043f\u043e\u0441\u043b\u0435 "
            "\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 \u0434\u0430\u043d\u043d\u044b\u0445 Binance.")
N_VERDICT = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438"
             "\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0438\u0442\u043e\u0433 \u0437\u0430\u043f\u0438\u0441"
             "\u0430\u043d \u0438 \u0436\u0434\u0451\u0442 \u0440\u0430\u0437\u0431\u043e\u0440\u0430 \u0410\u0440"
             "\u0445\u0438\u0442\u0435\u043a\u0442\u043e\u0440\u0430.")
MINUTES = "\u043c\u0438\u043d"
HOURS = "\u0447"


class Transport(Exception):
    """A request that produced no readable answer: a fact about the network, never an absence (inv. 70)."""


class NotPublished(Exception):
    """data.binance.vision answered 404."""


class NotReady(Exception):
    """An input is not yet published; the pass is retried later."""


class Absent(Exception):
    """An input that should have been published by now and was not."""


# --- time --------------------------------------------------------------------
def now_ms():
    return int(time.time() * 1000)


def utc_date(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")


def day_start(date):
    return int(datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)


def add_days(date, n):
    return (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=n)).strftime("%Y-%m-%d")


def days_between(first, last):
    """Every date from first to last inclusive."""
    out, d = [], first
    while d <= last:
        out.append(d)
        d = add_days(d, 1)
    return out


def iso(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def minute(ms):
    return ms // 60000 * 60000


# --- the rule's inputs read from the checkout ---------------------------------
def load_rule(repo=REPO):
    """Capital and medium risk from analyst/owner.json; INV_FLOOR_SD and FEE_TAKER cut from
    index.html (inv. 20: one number per threshold, system-wide)."""
    with open(os.path.join(repo, "analyst", "owner.json"), encoding="utf-8") as fh:
        owner = json.load(fh)
    with open(os.path.join(repo, "index.html"), encoding="utf-8") as fh:
        page = fh.read()
    return {"capital_usdt": float(owner["capital"]["usdt"]), "risk_pct": float(owner["risk"]["risk_pct_medium"]),
            "inv_floor_sd": common.cut_number(page, "INV_FLOOR_SD"), "fee_taker": common.cut_number(page, "FEE_TAKER")}


def fingerprint():
    """The installed vps tree and this file's MD5 (inv. 38(3))."""
    try:
        with open(DEPLOYED_TREE, encoding="utf-8") as fh:
            tree = fh.read().strip() or "-"
    except OSError:
        tree = "-"
    with open(os.path.abspath(__file__), "rb") as fh:
        md5 = hashlib.md5(fh.read()).hexdigest()
    return {"vps_tree": tree, "paper_md5": md5}


# --- HTTP ----------------------------------------------------------------------
def http_get(url):
    """One GET; the body, or NotPublished on 404, or Transport."""
    try:
        with urllib.request.urlopen(url, timeout=common.HTTP_TIMEOUT_S) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise NotPublished(url) from None
        raise Transport("HTTP %d" % exc.code) from None
    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
        raise Transport(exc.__class__.__name__) from None


def http_post(url, body):
    """One POST of a JSON body; the parsed answer, or Transport. The outcome is decided
    after the parse, the last step that can fail (inv. 70)."""
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=common.HTTP_TIMEOUT_S) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        raise Transport("HTTP %d" % exc.code) from None
    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
        raise Transport(exc.__class__.__name__) from None
    try:
        return json.loads(raw)
    except ValueError:
        raise Transport("unparseable") from None


class Limiter:
    """The weight spent in the last 60 s, held at or under per_min."""

    def __init__(self, per_min=WEIGHT_PER_MIN, clock=time.monotonic, sleep=time.sleep):
        self.per_min, self.clock, self.sleep, self.spent = per_min, clock, sleep, []

    def spend(self, weight):
        while True:
            now = self.clock()
            self.spent = [(t, w) for t, w in self.spent if now - t < 60]
            if not self.spent or sum(w for _, w in self.spent) + weight <= self.per_min:
                self.spent.append((now, weight))
                return
            self.sleep(60 - (now - self.spent[0][0]) + 0.01)


def info(body, limiter):
    limiter.spend(INFO_WEIGHT)
    doc = http_post(INFO_URL, body)
    if body.get("type") == "userFillsByTime" and isinstance(doc, list):
        limiter.spend(len(doc) // 20)    # documented: one more per 20 items returned
    return doc


def iter_fills(addr, start_ms, limiter, end_ms=None):
    """Every fill of addr from start_ms (inclusive; to end_ms inclusive when given) the API returns,
    ascending, each tid once, holding only FILL_KEYS and one page at a time: an account with a
    hundred thousand fills never sits in memory whole. Pages of FILLS_PAGE continue from the last
    page's last time, which the API repeats; a full page inside one millisecond cannot advance and
    raises."""
    t, tids_at_t = start_ms, set()
    while True:
        asked = t
        body = {"type": "userFillsByTime", "user": addr, "startTime": t}
        if end_ms is not None:
            body["endTime"] = end_ms
        page = info(body, limiter)
        if not isinstance(page, list):
            raise ValueError("fills: not a list")
        for f in sorted(page, key=lambda f: (int(f["time"]), int(f["tid"]))):
            ft = int(f["time"])
            if ft < t or (ft == t and f["tid"] in tids_at_t):
                continue
            if ft > t:
                t, tids_at_t = ft, set()
            tids_at_t.add(f["tid"])
            yield {k: f[k] for k in FILL_KEYS}
        if len(page) < FILLS_PAGE:
            return
        if t == asked:
            raise ValueError("fills: a full page inside one millisecond")


def fills_since(addr, start_ms, limiter, end_ms=None):
    """iter_fills as a list, for reads that are short by construction: a poll, the probe."""
    return list(iter_fills(addr, start_ms, limiter, end_ms))


# --- the leaderboard, one row at a time ---------------------------------------
def iter_rows(chunks):
    """Each object of the "leaderboardRows" array, decoded one at a time from an iterable of
    bytes: the 39 MB document never exists as one Python object."""
    decoder = json.JSONDecoder()
    utf8 = codecs.getincrementaldecoder("utf-8")()
    chunks = iter(chunks)
    buf, pos, rows, eof = "", 0, False, False
    while True:
        if not rows:
            i = buf.find('"leaderboardRows"', pos)
            j = buf.find("[", i) if i >= 0 else -1
            if j >= 0:
                pos, rows = j + 1, True
                continue
            pos = i if i >= 0 else max(0, len(buf) - 32)
        else:
            while pos < len(buf) and buf[pos] in " \t\r\n,":
                pos += 1
            if pos < len(buf):
                if buf[pos] == "]":
                    return
                try:
                    obj, end = decoder.raw_decode(buf, pos)
                except json.JSONDecodeError:
                    obj = None
                if obj is not None:
                    pos = end
                    yield obj
                    continue
        if eof:
            raise ValueError("leaderboard: the document ended before its rows did")
        try:
            chunk = next(chunks)
        except StopIteration:
            chunk, eof = b"", True
        buf = buf[pos:] + utf8.decode(chunk, final=eof)
        pos = 0


def leaderboard_chunks():
    try:
        resp = urllib.request.urlopen(LEADERBOARD_URL, timeout=common.HTTP_TIMEOUT_S)
    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
        raise Transport(exc.__class__.__name__) from None
    with resp:
        while True:
            try:
                chunk = resp.read(65536)
            except (OSError, http.client.HTTPException) as exc:
                raise Transport(exc.__class__.__name__) from None
            if not chunk:
                return
            yield chunk


def pool_of(rows):
    """(sorted addresses with all-time volume >= POOL_VOLUME_MIN, rows read, rows unreadable)."""
    pool, n, bad = set(), 0, 0
    for row in rows:
        n += 1
        try:
            vlm = float(dict(row["windowPerformances"])["allTime"]["vlm"])
            addr = row["ethAddress"].lower()
        except (KeyError, TypeError, ValueError, AttributeError):
            bad += 1
            continue
        if vlm >= POOL_VOLUME_MIN:
            pool.add(addr)
    return sorted(pool), n, bad


# --- the twelve-month record ----------------------------------------------------
def step_at(history, t):
    """The value of the last point at or before t, or None: the series steps between points."""
    value = None
    for ms, v in history:
        if ms > t:
            break
        value = v
    return value


def series(points):
    return sorted((int(ms), float(v)) for ms, v in points)


def weekly(pf, t0_ms):
    """Account value and cumulative PnL of perpAllTime at the 53 grid instants T0 - 52 weeks ... T0."""
    w = pf["perpAllTime"]
    av, pn = series(w["accountValueHistory"]), series(w["pnlHistory"])
    grid = [t0_ms - (LOOKBACK_WEEKS - j) * WEEK_MS for j in range(LOOKBACK_WEEKS + 1)]
    return [step_at(av, g) for g in grid], [step_at(pn, g) for g in grid]


def weekly_returns(values, pnls):
    """r_j = (P_j - P_{j-1}) / V_{j-1}, j = 1 ... 52; None when an input is missing or a value is not positive."""
    out = []
    for j in range(1, len(values)):
        if None in (values[j - 1], pnls[j - 1], pnls[j]) or values[j - 1] <= 0:
            return None
        out.append((pnls[j] - pnls[j - 1]) / values[j - 1])
    return out


def turnover(pf):
    """perpMonth volume per day over the mean of perpMonth's account values; None when undefined."""
    w = pf["perpMonth"]
    pts = series(w["accountValueHistory"])
    if len(pts) < 2:
        return None
    span = (pts[-1][0] - pts[0][0]) / DAY_MS
    mean = sum(v for _, v in pts) / len(pts)
    if span < 1 or mean <= 0:
        return None
    return float(w["vlm"]) / mean / span


def record(returns):
    """(passes, positive blocks, maximum drawdown, weekly Sharpe or None, 52-week return)."""
    blocks = sum(1 for b in range(LOOKBACK_WEEKS // BLOCK_WEEKS)
                 if math.prod(1 + r for r in returns[b * BLOCK_WEEKS:(b + 1) * BLOCK_WEEKS]) - 1 > 0)
    wealth, peak, dd = 1.0, 1.0, 0.0
    for r in returns:
        wealth *= 1 + r
        peak = max(peak, wealth)
        dd = max(dd, 1 - wealth / peak)
    sd = statistics.pstdev(returns)
    sharpe = statistics.fmean(returns) / sd if sd > 0 else None
    return blocks >= BLOCKS_MIN and dd <= DRAWDOWN_MAX, blocks, dd, sharpe, wealth - 1


def metrics(pf, t0_ms):
    """The selection's measures of one account's portfolio answer."""
    pf = dict(pf)
    values, pnls = weekly(pf, t0_ms)
    to = turnover(pf)
    m = {"value_t0": values[-1], "turnover": to, "eligible": False, "r12": False}
    if (to is None or to > TURNOVER_MAX or values[-1] is None or values[-1] < VALUE_MIN_T0
            or any(v is None or v < VALUE_MIN_WEEK for v in values[:-1])):
        return m
    rets = weekly_returns(values, pnls)
    if rets is None:
        return m
    passes, blocks, dd, sharpe, ret = record(rets)
    m.update(eligible=True, r12=passes and sharpe is not None, blocks=blocks, drawdown=dd, sharpe=sharpe, ret52=ret)
    return m


# --- episodes -------------------------------------------------------------------
def sign(x):
    return (x > 0) - (x < 0)


def symbol_for(coin, symbols):
    """The Binance USD-M symbol a Hyperliquid perpetual is copied on, or None: spot, a builder
    market and a coin without that exact symbol are not copyable; a "k" coin is the 1000 contract."""
    if "/" in coin or ":" in coin or coin.startswith("@"):
        return None
    base = "1000" + coin[1:] if coin[:1] == "k" and coin[1:2].isupper() else coin
    sym = base + "USDT"
    return sym if sym in symbols else None


def apply_fill(coins, fill, symbol):
    """One fill on one copyable coin against coins[coin], the open episode or None. The position
    before the fill is the fill's own startPosition, so a coin first seen with a position open has
    no episode until it is flat. Returns the events in order: ("lost", ep) when the episode held
    disagrees with startPosition, ("close", ep) when the fill flattens or flips it, ("open", ep)
    when the fill opens from flat or by the flip."""
    coin = fill["coin"]
    start = Decimal(fill["startPosition"])
    size = Decimal(fill["sz"])
    after = start + size if fill["side"] == "B" else start - size
    t, px = int(fill["time"]), fill["px"]
    ep, events = coins.get(coin), []
    if ep is not None and ep["side"] != sign(start):
        events.append(("lost", ep))
        ep = None
    if ep is not None and sign(after) != ep["side"]:
        events.append(("close", dict(ep, t_close=t, px_close=px, n=ep["n"] + 1)))
        ep = None
    elif ep is not None:
        ep = dict(ep, n=ep["n"] + 1)
    if ep is None and after != 0 and sign(start) != sign(after):
        ep = {"coin": coin, "symbol": symbol, "side": sign(after), "t_open": t, "px_open": px, "n": 1}
        events.append(("open", ep))
    coins[coin] = ep
    return events


def copyability(fills, symbols, t_from, t_to):
    """Venue share of perpetual notional on copyable coins and the median closed-episode
    duration, over fills in [t_from, t_to); copyable when the share is at least VENUE_SHARE_MIN
    and the median is at least the longest delay."""
    total = copyable = 0.0
    coins, durations = {}, []
    for f in fills:
        t, coin = int(f["time"]), f["coin"]
        if not t_from <= t < t_to or "/" in coin or coin.startswith("@"):
            continue
        notional = float(f["px"]) * float(f["sz"])
        total += notional
        sym = symbol_for(coin, symbols)
        if sym is None:
            continue
        copyable += notional
        for kind, ep in apply_fill(coins, f, sym):
            if kind == "close":
                durations.append((ep["t_close"] - ep["t_open"]) / 1000)
    share = copyable / total if total > 0 else 0.0
    median = statistics.median(durations) if durations else None
    return {"share": share, "median_episode_s": median, "closed_episodes": len(durations),
            "copyable": share >= VENUE_SHARE_MIN and median is not None and median >= max(DELAYS_S)}


def null_order(t0_ms, addresses):
    """The null's draw order: by SHA-256 of T0's ISO instant and the address, reproducible anywhere."""
    stamp = iso(t0_ms)
    return sorted(addresses, key=lambda a: hashlib.sha256((stamp + a).encode("ascii")).hexdigest())


# --- booking ----------------------------------------------------------------------
def daily_sigma(closes):
    """Population standard deviation of the daily simple returns of consecutive closes."""
    return statistics.pstdev([closes[i + 1] / closes[i] - 1 for i in range(len(closes) - 1)])


def book_delay(ep, delay_s, dist, kl, capital, risk_frac, fee, window_end):
    """One episode copied at one delay. kl = (open times ascending, rows (o, h, l, c)). Entry at
    the close of the minute containing t_open + delay; exit at the close of the minute containing
    t_close + delay, or of window_end's minute for a cut episode; the stop variant leaves at
    entry -/+ dist on the first later minute through the exit minute that touches it, at the stop
    or at that minute's open when it opened beyond. None when the copier would enter after its exit."""
    times, rows = kl
    side = ep["side"]
    entry_m = minute(ep["t_open"] + delay_s * 1000)
    exit_m = minute(window_end) if ep.get("cut") else minute(ep["t_close"] + delay_s * 1000)
    if entry_m > exit_m:
        return None
    i = bisect.bisect_right(times, entry_m) - 1
    j = bisect.bisect_right(times, exit_m) - 1
    if i < 0:
        raise Absent("no kline at or before the entry minute")
    entry = rows[i][3]
    qty = risk_frac * capital / (entry * dist)
    stop = entry * (1 - side * dist)
    hit = None
    for k in range(i + 1, j + 1):
        o, h, low, _ = rows[k]
        if side > 0 and low <= stop:
            hit = (times[k], min(o, stop))
            break
        if side < 0 and h >= stop:
            hit = (times[k], max(o, stop))
            break

    def leg(exit_ms, px):
        return {"exit_ms": exit_ms, "px": px, "gross": side * qty * (px - entry), "fee": fee * qty * (entry + px)}

    src = leg(exit_m, rows[j][3])
    return {"entry_ms": entry_m, "entry_px": entry, "qty": qty, "stop_px": stop, "stopped": hit is not None,
            "src": src, "stop": leg(*hit) if hit else dict(src)}


def funding_paid(side, qty, entry_px, hold_from, hold_to, rates):
    """side * qty * entry_px * the sum of rates at hold_from < t <= hold_to: positive is paid.
    The notional is the entry's, not the mark at each event (a stated simplification)."""
    return side * qty * entry_px * sum(r for t, r in rates if hold_from < t <= hold_to)


def vision_rows(path):
    """The CSV rows of one data.binance.vision zip, a header line dropped."""
    blob = http_get(VISION + path)
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            text = z.read(z.namelist()[0]).decode("utf-8")
    except (zipfile.BadZipFile, IndexError, UnicodeDecodeError):
        raise Transport("unreadable zip") from None
    rows = [line.split(",") for line in text.splitlines() if line.strip()]
    return rows[1:] if rows and not rows[0][0].strip().isdigit() else rows


class Inputs:
    """data.binance.vision inputs of one pass: 1m klines by symbol and day, daily closes kept on
    disk, funding rates by symbol and month. A 404 dated more than ABSENT_AFTER_DAYS before today is
    Absent; nearer is NotReady."""

    def __init__(self, state_dir, today, rows=vision_rows):
        self.today, self.rows, self.klines, self.rates_by = today, rows, {}, {}
        self.closes_path = os.path.join(state_dir, "closes.json")
        try:
            with open(self.closes_path, encoding="utf-8") as fh:
                self.closes = json.load(fh)
        except (OSError, ValueError):
            self.closes = {}

    def fetch(self, path, ref_date):
        try:
            return self.rows(path)
        except NotPublished:
            gap = (datetime.strptime(self.today, "%Y-%m-%d") - datetime.strptime(ref_date, "%Y-%m-%d")).days
            raise (Absent if gap > ABSENT_AFTER_DAYS else NotReady)(path) from None

    def minutes(self, sym, date):
        key = (sym, date)
        if key not in self.klines:
            rows = self.fetch("/daily/klines/%s/1m/%s-1m-%s.zip" % (sym, sym, date), date)
            self.klines[key] = [(int(r[0]), (float(r[1]), float(r[2]), float(r[3]), float(r[4]))) for r in rows]
        return self.klines[key]

    def kl(self, sym, first, last):
        merged = sorted(row for d in days_between(first, last) for row in self.minutes(sym, d))
        return [t for t, _ in merged], [r for _, r in merged]

    def close_on(self, sym, date):
        have = self.closes.setdefault(sym, {})
        if date not in have:
            rows = self.fetch("/daily/klines/%s/1d/%s-1d-%s.zip" % (sym, sym, date), date)
            have[date] = float(rows[0][4])
            common.atomic_write(self.closes_path, self.closes, mode=0o640)
        return have[date]

    def rates(self, sym, month):
        key = (sym, month)
        if key not in self.rates_by:
            last_day = add_days((datetime.strptime(month + "-01", "%Y-%m-%d") + timedelta(days=32))
                                .strftime("%Y-%m-01"), -1)
            rows = self.fetch("/monthly/fundingRate/%s/%s-fundingRate-%s.zip" % (sym, sym, month), last_day)
            self.rates_by[key] = [(int(r[0]), float(r[2])) for r in rows]
        return self.rates_by[key]


def book_episode(ep, inputs, rule, window_end):
    """The book line of one episode: sigma_for, the stop distance INV_FLOOR_SD sigma, and every
    delay; or an unbookable line."""
    line = {"k": "book", "a": ep["a"], "coin": ep["coin"], "symbol": ep["symbol"], "side": ep["side"],
            "t_open": ep["t_open"]}
    first = utc_date(ep["t_open"])
    try:
        sigma = sigma_for(inputs, ep["symbol"], ep["t_open"])
        dist = rule["inv_floor_sd"] * sigma
        if not dist > 0:
            raise Absent("sigma is zero")
        last = utc_date(window_end if ep.get("cut") else ep["t_close"] + max(DELAYS_S) * 1000)
        kl = inputs.kl(ep["symbol"], first, last)
        line.update(sigma_d=sigma, dist=dist, d={
            str(d): book_delay(ep, d, dist, kl, rule["capital_usdt"], rule["risk_pct"] / 100, rule["fee_taker"],
                               window_end) for d in DELAYS_S})
    except Absent as exc:
        line["unbookable"] = str(exc)
    return line


def funding_line(book, inputs):
    """The funding of one booked episode, per delay and variant, from the monthly archives."""
    line = {"k": "funding", "a": book["a"], "coin": book["coin"], "t_open": book["t_open"], "absent": False, "d": {}}
    if "d" not in book:
        line["unbooked"] = True
        return line
    spans = [(b["entry_ms"] + 60000, b[v]["exit_ms"] + 60000) for b in book["d"].values() if b for v in ("src", "stop")]
    rates = []
    if spans:
        month, end = utc_date(min(s for s, _ in spans))[:7], utc_date(max(e for _, e in spans))[:7]
        while month <= end:
            try:
                rates += inputs.rates(book["symbol"], month)
            except Absent:
                line["absent"] = True
            month = (datetime.strptime(month + "-01", "%Y-%m-%d") + timedelta(days=32)).strftime("%Y-%m")
    for d, b in book["d"].items():
        line["d"][d] = None if b is None else {
            v: funding_paid(book["side"], b["qty"], b["entry_px"], b["entry_ms"] + 60000, b[v]["exit_ms"] + 60000, rates)
            for v in ("src", "stop")}
    return line


# --- the verdict -----------------------------------------------------------------
def decide(picks, null, results, pick_episodes):
    """results[a][d][v]: net over capital. TOP is the picks' mean; the null is every k-subset of the
    null accounts. Readable with at least one pick, NULL_MIN null accounts and EPISODES_MIN booked
    pick episodes at 1 800 s; passed when readable and, at every deciding delay on the stop
    variant, TOP > 0 and TOP > the null subsets' median."""
    k, out = len(picks), {}
    subsets = list(combinations(null, k)) if 0 < k <= len(null) else []
    for d in DELAYS_S:
        for v in ("stop", "src"):
            top = statistics.fmean(results[a][d][v] for a in picks) if k else None
            means = [statistics.fmean(results[a][d][v] for a in c) for c in subsets]
            med = statistics.median(means) if means else None
            share = sum(1 for x in means if x >= top) / len(means) if means else None
            out["%d/%s" % (d, v)] = {"top": top, "null_median": med, "null_share_at_or_above": share,
                                     "picks": {a: results[a][d][v] for a in picks}}
    readable = k >= 1 and len(null) >= NULL_MIN and pick_episodes >= EPISODES_MIN
    passed = readable and all(out["%d/stop" % d]["top"] > 0 and out["%d/stop" % d]["top"] > out["%d/stop" % d]["null_median"]
                              for d in DECIDING_S)
    return {"readable": readable, "passed": passed, "cells": out}


def nearest_rank(values, q):
    if not values:
        return None
    ordered = sorted(values)
    return ordered[max(0, math.ceil(q * len(ordered)) - 1)]


# --- records ---------------------------------------------------------------------
def write_record(state, state_dir, rel, lines=None, doc=None):
    """One record into the local mirror, atomically, and onto the pending list (inv. 72)."""
    path = os.path.join(state_dir, "records", RECORD_DIR, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if doc is not None:
        data = json.dumps(doc, separators=(",", ":"), allow_nan=False, sort_keys=True) + "\n"
    else:
        data = "".join(json.dumps(x, separators=(",", ":"), allow_nan=False, sort_keys=True) + "\n" for x in lines)
    common.atomic_write(path, data, mode=0o644)
    state["pending"] = sorted(set(state["pending"]) | {rel})


def read_jsonl(path):
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def publish(state, state_dir, tree):
    """Pending records into the clone at origin/main and pushed (contract v30 section 8). A path
    main already holds leaves the list unchanged on main: equal bytes are done, different bytes are
    logged and main's copy stands \u2014 a record is never reopened."""
    git = lambda *a: common.git_quiet(tree, *a)  # noqa: E731
    if git("fetch", "-q", "origin", "main") != 0:
        return "fetch failed"
    git("reset", "-q", "--hard", "origin/main")
    git("clean", "-q", "-fdx", "--", RECORD_DIR)
    copied, done = [], []
    for rel in state["pending"]:
        src = os.path.join(state_dir, "records", RECORD_DIR, rel)
        dst = os.path.join(tree, RECORD_DIR, rel)
        if os.path.exists(dst):
            with open(src, "rb") as a, open(dst, "rb") as b:
                if a.read() != b.read():
                    common.log("paper: %s differs from main; main's copy stands" % rel)
            done.append(rel)
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        copied.append(rel)
    pushed = None
    if copied:
        _, pushed = common.publish(tree, [os.path.join(RECORD_DIR, r) for r in copied], "paper: " + ", ".join(copied))
        if pushed:
            done += copied
    state["pending"] = [r for r in state["pending"] if r not in done]
    return "copied=%d pushed=%s left=%d" % (len(copied), "-" if pushed is None else ("yes" if pushed else "no"),
                                            len(state["pending"]))


# --- selection ----------------------------------------------------------------------
def read_work(path):
    """The work file's lines; a torn last line is dropped."""
    out = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    break
    except FileNotFoundError:
        pass
    return out


def append_work(path, obj):
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, separators=(",", ":"), allow_nan=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def retrying(call, *args, give_up=False):
    """call(*args), waiting TRANSPORT_WAIT_S after each Transport. After TRANSPORT_MAX in a row, a step
    the selection can do without -- one account -- is given up: None, which the caller records as
    unreadable for transport, never as absent (inv. 70); a step it cannot do without ends the process,
    which its unit restarts, and the selection resumes from its work file."""
    for attempt in range(TRANSPORT_MAX):
        try:
            return call(*args)
        except Transport as exc:
            common.log("paper: transport %s, attempt %d of %d" % (exc, attempt + 1, TRANSPORT_MAX))
            time.sleep(TRANSPORT_WAIT_S)
    if give_up:
        return None
    sys.exit(4)


def select(state_dir, rule, limiter, clock=now_ms):
    """The selection, resumable: T0, the pool, every pool account's measures, the Binance list, the
    picks walked down the ranking and the null walked down its order, each step kept in the work file."""
    path = os.path.join(state_dir, "selection-work.jsonl")
    work = read_work(path)
    head = next((w for w in work if "t0_ms" in w), None)
    if head is None:
        head = {"t0_ms": day_start(utc_date(clock()))}
        append_work(path, head)
    t0 = head["t0_ms"]
    pool = next((w for w in work if "pool" in w), None)
    if pool is None:
        pool_list, n, bad = retrying(lambda: pool_of(iter_rows(leaderboard_chunks())))
        pool = {"pool": pool_list, "rows": n, "bad_rows": bad}
        append_work(path, pool)
        common.log("paper: pool rows=%d pool=%d bad=%d" % (n, len(pool_list), bad))
    measured = {w["a"]: w["m"] for w in work if "a" in w}
    for addr in pool["pool"]:
        if addr in measured:
            continue
        doc = retrying(info, {"type": "portfolio", "user": addr}, limiter, give_up=True)
        try:
            m = metrics(doc, t0) if doc is not None else {"unreadable": "transport", "eligible": False, "r12": False}
        except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, OverflowError):
            m = {"unreadable": "shape", "eligible": False, "r12": False}
        measured[addr] = m
        append_work(path, {"a": addr, "m": m})
        if len(measured) % 500 == 0:
            common.log("paper: measured %d of %d" % (len(measured), len(pool["pool"])))
    symbols = next((w["symbols"] for w in work if "symbols" in w), None)
    if symbols is None:
        symbols = sorted(p["symbol"] for p in exchange.perpetuals(retrying(fetch_exchange)))
        append_work(path, {"symbols": symbols})
    symbol_set = set(symbols)
    checked = {w["c"]: w["r"] for w in work if "c" in w}

    def check(addr):
        if addr not in checked:
            start = t0 - WINDOW_DAYS * DAY_MS
            try:
                found = retrying(lambda: copyability(iter_fills(addr, start, limiter, t0 - 1), symbol_set, start, t0),
                                 give_up=True)
                checked[addr] = found if found is not None else {"unreadable": "transport", "copyable": False}
            except (KeyError, TypeError, ValueError, ArithmeticError):
                checked[addr] = {"unreadable": "shape", "copyable": False}
            append_work(path, {"c": addr, "r": checked[addr]})
        return checked[addr]

    ranked = sorted((a for a, m in measured.items() if m.get("r12")), key=lambda a: (-measured[a]["sharpe"], a))
    picks, rejected = [], []
    for addr in ranked:
        if len(picks) == TOP_K:
            break
        (picks if check(addr)["copyable"] else rejected).append(addr)
    eligible = sorted(a for a, m in measured.items() if m.get("eligible"))
    null = []
    for addr in null_order(t0, [a for a in eligible if a not in picks]):
        if len(null) == NULL_M:
            break
        if check(addr)["copyable"]:
            null.append(addr)
    follow_from = clock()
    entry = lambda a: {**measured[a], **checked.get(a, {}), "address": a}  # noqa: E731
    return {"v": 1, "k": "paper-selection", "t0": iso(t0), "t0_ms": t0, "follow_from": iso(follow_from),
            "follow_from_ms": follow_from, "window_end": iso(follow_from + WINDOW_DAYS * DAY_MS),
            "window_end_ms": follow_from + WINDOW_DAYS * DAY_MS, "rule": dict(rule, delays_s=list(DELAYS_S)),
            "counts": {"rows": pool["rows"], "bad_rows": pool["bad_rows"], "pool": len(pool["pool"]),
                       "unreadable": sum(1 for m in measured.values() if m.get("unreadable")),
                       "eligible": len(eligible), "r12": len(ranked), "checked": len(checked)},
            "picks": [dict(entry(a), rank=i + 1) for i, a in enumerate(picks)],
            "rejected": [entry(a) for a in rejected], "null": [entry(a) for a in null],
            "eligible": eligible, "symbols": symbols, "fp": fingerprint()}


def fetch_exchange():
    try:
        return exchange.fetch_info()
    except (urllib.error.URLError, OSError, http.client.HTTPException, ValueError) as exc:
        raise Transport(exc.__class__.__name__) from None


# --- following ----------------------------------------------------------------------
def addr_short(addr):
    return addr[:6] + "\u2026" + addr[-4:]


def side_word(side):
    return "LONG" if side > 0 else "SHORT"


def decimals(px):
    return len(px.split(".", 1)[1]) if "." in px else 0


def hhmm(ms):
    return datetime.fromtimestamp(ms / 1000, tz=announce.TBILISI).strftime("%H:%M")


def held_text(ms):
    minutes = ms / 60000
    return ("%d " % round(minutes) + MINUTES) if minutes < 60 else ("%.1f " % (minutes / 60) + HOURS)


def sigma_for(inputs, sym, t_open):
    """sigma of the 31 daily closes of days D-32 ... D-2, D the opening day: every one is published
    by the time any episode of day D opens."""
    first = utc_date(t_open)
    return daily_sigma([inputs.close_on(sym, add_days(first, -k)) for k in range(SIGMA_DAYS + 2, 1, -1)])


def alert_open(ep, rank, rule, sigma):
    base = {"hhmm": hhmm(ep["t_open"]), "rank": rank, "addr": addr_short(ep["a"]), "side": side_word(ep["side"]),
            "symbol": ep["symbol"], "px": ep["px_open"]}
    if sigma is None or not sigma > 0:
        return P_OPEN_BARE.format(**base)
    dist = rule["inv_floor_sd"] * sigma
    stop = float(ep["px_open"]) * (1 - ep["side"] * dist)
    notional = rule["risk_pct"] / 100 * rule["capital_usdt"] / dist
    return P_OPEN.format(dist="%.1f" % (dist * 100), stop="%.*f" % (decimals(ep["px_open"]), stop),
                         notional="%d" % round(notional), risk=("%g" % rule["risk_pct"]), **base)


def alert_close(ep, rank):
    return P_CLOSE.format(hhmm=hhmm(ep["t_close"]), rank=rank, addr=addr_short(ep["a"]), side=side_word(ep["side"]),
                          symbol=ep["symbol"], px=ep["px_close"], held=held_text(ep["t_close"] - ep["t_open"]))


def starts(sel):
    """The test follows only when it can be read: at least one pick and NULL_MIN null accounts."""
    return len(sel["picks"]) >= 1 and len(sel["null"]) >= NULL_MIN


def new_state(sel):
    accounts = {}
    for role, rows in (("pick", sel["picks"]), ("null", sel["null"])):
        for row in rows:
            accounts[row["address"]] = {"role": role, "rank": row.get("rank"), "last_ms": sel["follow_from_ms"],
                                        "last_tids": [], "polled_ms": 0, "due_ms": 0, "coins": {}, "fills": {},
                                        "lost": {}, "failing": False}
    return {"v": 1, "accounts": accounts, "closed": [], "cut": False, "written": {"episodes": None, "book": None,
            "funding": None}, "verdict": False, "pending": [], "next_work_ms": 0, "next_publish_ms": 0,
            "closed_notice": False}


def poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for):
    """New fills since the account's last time, through apply_fill; alerts for a pick's fresh events.
    The account's state changes only when the whole poll succeeded."""
    fills = fills_since(addr, acct["last_ms"], limiter)
    work = json.loads(json.dumps(acct))
    _apply(addr, work, fills, sel, symbols, now, rule, inputs_for)
    acct.clear()
    acct.update(work)


def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for):
    window_end = sel["window_end_ms"]
    for f in fills:
        t = int(f["time"])
        if (t == acct["last_ms"] and f["tid"] in acct["last_tids"]) or t >= window_end:
            continue
        sym = symbol_for(f["coin"], symbols)
        if sym is None:
            continue
        day = utc_date(t)
        acct["fills"][day] = acct["fills"].get(day, 0) + 1
        for kind, ep in apply_fill(acct["coins"], f, sym):
            if kind == "lost":
                acct["lost"][day] = acct["lost"].get(day, 0) + 1
                continue
            if kind == "open":
                ep.update(a=addr, role=acct["role"], rank=acct["rank"], seen_open_ms=now)
            else:
                ep.update(seen_close_ms=now, cut=False)
                acct["closed_buffer"] = acct.get("closed_buffer", []) + [ep]
            if acct["role"] == "pick" and now - t <= ALERT_MAX_AGE_S * 1000 and now < window_end:
                if kind == "open":
                    try:
                        sigma = sigma_for(inputs_for(), sym, t)
                    except (NotReady, Absent, Transport, ValueError, ZeroDivisionError):
                        sigma = None
                    common.write_outbox("alert", alert_open(ep, acct["rank"], rule, sigma))
                else:
                    common.write_outbox("alert", alert_close(ep, acct["rank"]))
    if fills:
        acct["last_ms"] = max(acct["last_ms"], max(int(f["time"]) for f in fills))
        acct["last_tids"] = [f["tid"] for f in fills if int(f["time"]) == acct["last_ms"]]
    acct["polled_ms"] = now


def gather_closed(state):
    for acct in state["accounts"].values():
        state["closed"] += acct.pop("closed_buffer", [])


def cut_open(state, sel):
    """At window_end, once every account was polled DAY_SETTLE_S past it: every open episode closes at
    window_end, cut, and following stops."""
    for addr, acct in state["accounts"].items():
        for coin, ep in list(acct["coins"].items()):
            if ep is not None:
                state["closed"].append(dict(ep, t_close=sel["window_end_ms"], px_close=None, seen_close_ms=None,
                                            cut=True))
            acct["coins"][coin] = None
    state["cut"] = True


def next_date(written, first):
    return first if written is None else add_days(written, 1)


def produce_days(state, state_dir, sel, now):
    """Episode files, in date order, for every day all accounts were polled DAY_SETTLE_S past; an
    episode that closed on a day already written goes into the next file, never lost."""
    first, last = utc_date(sel["follow_from_ms"]), utc_date(sel["window_end_ms"])
    settled = min(a["polled_ms"] for a in state["accounts"].values())
    while True:
        day = next_date(state["written"]["episodes"], first)
        if day > last or (day == last and not state["cut"]):
            return
        if day < last and settled < day_start(day) + DAY_MS + DAY_SETTLE_S * 1000:
            return
        eps = sorted((e for e in state["closed"] if utc_date(e["t_close"]) <= day),
                     key=lambda e: (e["t_close"], e["a"], e["coin"], e["t_open"]))
        head = {"k": "day", "date": day, "episodes": len(eps), "accounts": {
            a: {"fills": acct["fills"].get(day, 0), "lost": acct["lost"].get(day, 0)}
            for a, acct in sorted(state["accounts"].items())}}
        write_record(state, state_dir, "episodes/%s.jsonl" % day, [head] + [dict(e, k="ep") for e in eps])
        state["closed"] = [e for e in state["closed"] if utc_date(e["t_close"]) > day]
        state["written"]["episodes"] = day


def produce_books(state, state_dir, sel, rule, inputs):
    first = utc_date(sel["follow_from_ms"])
    while True:
        day = next_date(state["written"]["book"], first)
        if state["written"]["episodes"] is None or day > state["written"]["episodes"]:
            return
        eps = [e for e in read_jsonl(os.path.join(state_dir, "records", RECORD_DIR, "episodes", day + ".jsonl"))
               if e["k"] == "ep"]
        lines = [book_episode(e, inputs, rule, sel["window_end_ms"]) for e in eps]   # NotReady ends the pass
        head = {"k": "day", "date": day, "booked": sum(1 for x in lines if "d" in x),
                "unbookable": sum(1 for x in lines if "unbookable" in x)}
        write_record(state, state_dir, "book/%s.jsonl" % day, [head] + lines)
        state["written"]["book"] = day


def produce_funding(state, state_dir, sel, inputs):
    first = utc_date(sel["follow_from_ms"])
    while True:
        day = next_date(state["written"]["funding"], first)
        if state["written"]["book"] is None or day > state["written"]["book"]:
            return
        books = [b for b in read_jsonl(os.path.join(state_dir, "records", RECORD_DIR, "book", day + ".jsonl"))
                 if b["k"] == "book"]
        lines = [funding_line(b, inputs) for b in books]
        head = {"k": "day", "date": day, "lines": len(lines), "absent": sum(1 for x in lines if x["absent"])}
        write_record(state, state_dir, "funding/%s.jsonl" % day, [head] + lines)
        state["written"]["funding"] = day


def produce_verdict(state, state_dir, sel, rule):
    last = utc_date(sel["window_end_ms"])
    if state["verdict"] or state["written"]["funding"] != last:
        return False
    root = os.path.join(state_dir, "records", RECORD_DIR)
    days = days_between(utc_date(sel["follow_from_ms"]), last)
    picks = [p["address"] for p in sel["picks"]]
    null = [p["address"] for p in sel["null"]]
    results = {a: {d: {"src": 0.0, "stop": 0.0} for d in DELAYS_S} for a in picks + null}
    booked = {d: {"pick": 0, "null": 0} for d in DELAYS_S}
    lags, unbookable, absent = [], 0, 0
    for day in days:
        for e in read_jsonl(os.path.join(root, "episodes", day + ".jsonl")):
            if e["k"] == "ep" and e["role"] == "pick" and e.get("seen_open_ms"):
                lags.append((e["seen_open_ms"] - e["t_open"]) / 1000)
        books = {(b["a"], b["coin"], b["t_open"]): b for b in read_jsonl(os.path.join(root, "book", day + ".jsonl"))
                 if b["k"] == "book"}
        for f in read_jsonl(os.path.join(root, "funding", day + ".jsonl")):
            if f["k"] != "funding":
                continue
            b = books[(f["a"], f["coin"], f["t_open"])]
            if "d" not in b:
                unbookable += 1
                continue
            absent += 1 if f["absent"] else 0
            role = "pick" if f["a"] in picks else "null"
            for d in DELAYS_S:
                cell = b["d"][str(d)]
                if cell is None:
                    continue
                booked[d][role] += 1
                for v in ("src", "stop"):
                    results[f["a"]][d][v] += (cell[v]["gross"] - cell[v]["fee"] - f["d"][str(d)][v]) / rule["capital_usdt"]
    verdict = decide(picks, null, results, booked[1800]["pick"])
    doc = {"v": 1, "k": "paper-verdict", "follow_from": sel["follow_from"], "window_end": sel["window_end"],
           "picks": picks, "null": null, "booked": {str(d): booked[d] for d in DELAYS_S}, "unbookable": unbookable,
           "funding_absent": absent, "lag_s": {"n": len(lags), "p50": nearest_rank(lags, 0.5),
                                                 "p95": nearest_rank(lags, 0.95)}, "fp": fingerprint()}
    doc.update(verdict)
    write_record(state, state_dir, "verdict.json", doc=doc)
    state["verdict"] = True
    return True


# --- the service ---------------------------------------------------------------------
def load_state(path, sel):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return new_state(sel)


def stored_selection(state_dir, tree):
    """The selection from the local mirror, else from main."""
    for root in (os.path.join(state_dir, "records"), tree):
        try:
            with open(os.path.join(root, RECORD_DIR, "selection.json"), encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            continue
    return None


def service(state_dir, tree):
    rule = load_rule()
    limiter = Limiter()
    common.git_quiet(tree, "fetch", "-q", "origin", "main")
    common.git_quiet(tree, "reset", "-q", "--hard", "origin/main")
    sel = stored_selection(state_dir, tree)
    state_path = os.path.join(state_dir, "state.json")
    if sel is None:
        common.log("paper: selection started")
        sel = select(state_dir, rule, limiter)
        state = new_state(sel)
        write_record(state, state_dir, "selection.json", doc=sel)
        end = datetime.fromtimestamp(sel["window_end_ms"] / 1000, tz=announce.TBILISI).strftime("%d.%m.%Y")
        common.write_outbox("notice", N_START.format(k=len(sel["picks"]), date=end) if starts(sel) else N_NONE)
        common.atomic_write(state_path, state, mode=0o640)
        common.log("paper: selection done picks=%d null=%d" % (len(sel["picks"]), len(sel["null"])))
    rule = sel["rule"]    # frozen at the selection: a later change of owner.json moves nothing here
    state = load_state(state_path, sel)
    written = None
    symbols = set(sel["symbols"])
    inputs_box = {}

    def inputs_for():
        today = utc_date(now_ms())
        if inputs_box.get("today") != today:
            inputs_box.update(today=today, inputs=Inputs(state_dir, today))
        return inputs_box["inputs"]

    while True:
        now = now_ms()
        if starts(sel) and not state["cut"]:
            for addr, acct in state["accounts"].items():
                if now < acct["due_ms"]:
                    continue
                acct["due_ms"] = now + 1000 * (PICK_POLL_S if acct["role"] == "pick" else NULL_POLL_S)
                try:
                    poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for)
                    if acct["failing"]:
                        common.log("paper: poll %s answered again" % addr_short(addr))
                    acct["failing"] = False
                except (Transport, KeyError, TypeError, ValueError, ArithmeticError) as exc:
                    if not acct["failing"]:
                        common.log("paper: poll %s failed (%s)" % (addr_short(addr), exc.__class__.__name__))
                    acct["failing"] = True
            gather_closed(state)
            if now >= sel["window_end_ms"] and all(a["polled_ms"] >= sel["window_end_ms"] + DAY_SETTLE_S * 1000
                                                    for a in state["accounts"].values()):
                cut_open(state, sel)
                if not state["closed_notice"]:
                    common.write_outbox("notice", N_CLOSED)
                    state["closed_notice"] = True
        if starts(sel):
            try:
                produce_days(state, state_dir, sel, now)
            except (OSError, ValueError) as exc:
                common.log("paper: day file failed (%s)" % exc.__class__.__name__)
            if now >= state["next_work_ms"]:
                state["next_work_ms"] = now + WORK_EVERY_S * 1000
                try:
                    produce_books(state, state_dir, sel, rule, inputs_for())
                    produce_funding(state, state_dir, sel, inputs_for())
                    if produce_verdict(state, state_dir, sel, rule):
                        common.write_outbox("notice", N_VERDICT)
                except NotReady:
                    pass
                except (Transport, OSError, ValueError, KeyError, ArithmeticError) as exc:
                    common.log("paper: booking failed (%s)" % exc.__class__.__name__)
        if state["pending"] and now >= state["next_publish_ms"]:
            state["next_publish_ms"] = now + PUBLISH_EVERY_S * 1000
            common.log("paper: publish " + publish(state, state_dir, tree))
        text = json.dumps(state, separators=(",", ":"), allow_nan=False)
        if text != written:
            common.atomic_write(state_path, text + "\n", mode=0o640)
            written = text
        time.sleep(LOOP_S)


# --- the probe -----------------------------------------------------------------------
def probe():
    """One read of every interface the service uses; one line each, counts only. Exit 0 when every
    read answered."""
    ok, limiter, t0 = True, Limiter(), day_start(utc_date(now_ms()))
    yesterday = add_days(utc_date(now_ms()), -1)
    prev_month = add_days(utc_date(now_ms())[:8] + "01", -1)[:7]
    steps = (
        ("leaderboard", lambda: "rows=%d pool=%d bad=%d" % (lambda p: (p[1], len(p[0]), p[2]))(
            pool_of(iter_rows(leaderboard_chunks())))),
        ("portfolio", lambda: " ".join("%s=%s" % (k, v) for k, v in sorted(
            metrics(info({"type": "portfolio", "user": PROBE_ACCOUNT}, limiter), t0).items()))),
        ("exchange", lambda: "perpetuals=%d" % len(exchange.perpetuals(fetch_exchange()))),
        ("fills", lambda: (lambda fl: "fills=%d first=%s" % (len(fl), iso(int(fl[0]["time"])) if fl else "-"))(
            fills_since(PROBE_ACCOUNT, t0 - WINDOW_DAYS * DAY_MS, limiter, t0 - 1))),
        ("klines_1m", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1m/BTCUSDT-1m-%s.zip" % yesterday))),
        ("klines_1d", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1d/BTCUSDT-1d-%s.zip" % yesterday))),
        ("funding", lambda: "rows=%d" % len(vision_rows(
            "/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-%s.zip" % prev_month))),
    )
    for name, step in steps:
        try:
            line = step()
        except Exception as exc:
            ok, line = False, "failed (%s)" % exc.__class__.__name__
        common.log("paper: probe %s %s" % (name, line))
    common.log("paper: probe peak_rss_kib=%d" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="the copy-trading paper test")
    parser.add_argument("--state-dir", default=STATE_DIR)
    parser.add_argument("--tree", default=TREE)
    parser.add_argument("--probe", action="store_true")
    args = parser.parse_args(argv)
    if args.probe:
        return probe()
    return service(args.state_dir, args.tree)


if __name__ == "__main__":
    sys.exit(main())
