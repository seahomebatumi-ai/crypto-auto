#!/usr/bin/env python3
"""The engine's book in code (TZ-67): the Donchian trend system over closed UTC daily bars of Binance
USD-M perpetuals. One function, replay(), decides every trade -- live and over the archive alike
(map inv. 21, 38), so the archive's record is the record of exactly the rules the run publishes.

    book.py --live SYMBOL...                    each symbol's state today, one JSON object per line,
                                                from fapi.binance.com's daily klines (the run's role 2)
    book.py --archive [--from D] [--to D] SYMBOL...
                                                every trade the rules made over data.binance.vision's
                                                archive, with fees, slippage and the actual funding,
                                                and the table of in-sample and out-of-sample results

The rules (Architect's decision, TZ-67, on the study of 20.10.2026):
  a daily close above the prior ENTRY_N days' highest high opens a long at the next day's open, a close
  below their lowest low a short; the stop sits STOP_ATR x ATR(ATR_N) from the entry; a daily close
  beyond the prior EXIT_N days' opposite extreme closes the trade at the next day's open, and the stop
  closes it intraday. No target and no time limit: the winners run.

The plan the owner trades (TZ-80): the same entries, exits and stop, and in addition, where the price reaches
SCALE_R times the initial risk from the entry, half the position closes there and the rest's stop moves to the
entry. replay(..., scale=SCALE_R) makes the plan's trades and replay(...) the rule's, from one loop.

The book the owner can hold (TZ-81): the plan's entries taken in time, each only while his side ceiling and his
book ceiling have room for it, the MAJORS first at one open and then the list's in its order. hold() decides it
from every symbol's spans() -- live and over the archive alike.

    book.py --archive --scale 2 --hold SIDE,BOOK SYMBOL...
                                                the plan held under those ceilings, the symbols in the
                                                list's order

Python 3.12's standard library only. Time is UTC everywhere.
"""
import argparse
import concurrent.futures
import csv
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import date, datetime, timedelta, timezone

ENTRY_N = 55          # a close beyond the prior 55 days' extreme opens a trend
EXIT_N = 20           # a close beyond the prior 20 days' opposite extreme closes it
ATR_N = 20            # the average true range's window, in days
STOP_ATR = 2.0        # the initial stop, in ATRs from the entry
COST_SIDE = 0.001     # taker fee 0.05 % + slippage 0.05 %, a fraction of notional per side
OOS_START = date(2025, 1, 1)
# The plan's target, in R from the entry: the owner's request of 24.10.2026 and methodology 2026-10-24-c, measured
# on the archive by the Architect on 24.10.2026 (map section 10, row "The book prints no target").
SCALE_R = 2.0
# Map section 10, row "The book's out-of-sample loss sits in the alts": the five symbols its lead names. At one
# open the book takes them before the others, and the alert prints them first (TZ-80, TZ-81).
MAJORS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT")
# At one open (TZ-81): an exit at the open frees its slot before the entries, which are taken in rank order; a
# stop fills inside the day and frees its slot after them.
AT_OPEN, ENTRY, IN_DAY = 0, 1, 2
DAY_MS = 86_400_000
HTTP_TIMEOUT_S = 20
FAPI_KLINES = "https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1d&limit=400"
ARCHIVE = "https://data.binance.vision/data/futures/um"


def atr(bars, k):
    """The mean true range of the ATR_N days ending at day k (inclusive), or None before day ATR_N."""
    if k < ATR_N:
        return None
    total = 0.0
    for j in range(k - ATR_N + 1, k + 1):
        h, l, pc = bars[j][2], bars[j][3], bars[j - 1][4]
        total += max(h - l, abs(h - pc), abs(l - pc))
    return total / ATR_N


def replay(bars, open_now=None, scale=None):
    """bars: closed daily bars (t_open_ms, open, high, low, close), oldest first, one per UTC day.
    Returns (trades, position): each closed trade as a dict, and the open position after the last bar
    or None. A signal at day k's close fills at day k+1's open; a stop fills at the stop, or at the open
    when the day opened beyond it; a channel exit at day k's close fills at day k+1's open. A signal at
    the last bar's close fills at open_now, the open of the day still forming, and its position carries
    entry_due; without open_now (the archive) that signal has no fill yet and opens nothing (TZ-68).
    With scale (TZ-80), a position carries its target, the entry plus scale times the initial risk; a day
    that reaches it, and does not reach the stop, closes half at that price -- or at the open where the day
    opened beyond it -- and sets the rest's stop to the entry from the next day on; the position and its
    trade then carry t_scale and scale_px, and "stop" stays the initial stop, the one the trade's R is
    measured in. Without scale no position carries a target and nothing here moves."""
    trades, pos = [], None
    for k in range(len(bars)):
        t, o, h, l, c = bars[k]
        if pos is not None and k >= pos["k_entry"]:
            side, stop = pos["side"], pos.get("stop_now", pos["stop"])
            if (side > 0 and l <= stop) or (side < 0 and h >= stop):
                px = o if (side > 0 and o < stop) or (side < 0 and o > stop) else stop
                trades.append(dict(pos, k_exit=k, t_exit=t, exit=px, why="stop"))
                pos = None
            elif "target" in pos and "t_scale" not in pos:
                tgt = pos["target"]
                if (side > 0 and h >= tgt) or (side < 0 and l <= tgt):
                    pos.update(t_scale=t, k_scale=k, stop_now=pos["entry"],
                               scale_px=o if (side > 0 and o > tgt) or (side < 0 and o < tgt) else tgt)
            if pos is not None and k >= EXIT_N:
                lo = min(b[3] for b in bars[k - EXIT_N:k]); hi = max(b[2] for b in bars[k - EXIT_N:k])
                if (side > 0 and c < lo) or (side < 0 and c > hi):
                    if k + 1 < len(bars):
                        nxt = bars[k + 1]
                        trades.append(dict(pos, k_exit=k + 1, t_exit=nxt[0], exit=nxt[1], why="channel"))
                        pos = None
                        continue          # the exit day's own close cannot also open a trade
                    pos["exit_due"] = True
        if pos is None and k >= ENTRY_N and (k + 1 < len(bars) or open_now is not None):
            a = atr(bars, k)
            if a is None or a <= 0:
                continue
            hi = max(b[2] for b in bars[k - ENTRY_N:k]); lo = min(b[3] for b in bars[k - ENTRY_N:k])
            side = 1 if c > hi else (-1 if c < lo else 0)
            if side:
                t_entry, entry = bars[k + 1][:2] if k + 1 < len(bars) else (t + DAY_MS, open_now)
                pos = dict(side=side, k_signal=k, k_entry=k + 1, t_entry=t_entry, entry=entry, atr=a,
                           stop=entry - side * STOP_ATR * a, entry_due=k + 1 == len(bars))
                if scale:
                    pos["target"] = entry + side * scale * STOP_ATR * a
    return trades, pos


def levels(bars, pos):
    """What the next close decides, from the last closed bar: the trigger and the stop a new trade would
    take, or the open position's exit level. A position whose entry is due has no open R yet. A position
    of the plan (TZ-80) also carries its target and, once half has closed there, the day it did and the
    stop the rest now stands on."""
    k = len(bars) - 1
    t, o, h, l, c = bars[k]
    a = atr(bars, k)
    out = dict(asof=datetime.fromtimestamp(t / 1000, timezone.utc).strftime("%Y-%m-%d"), close=c,
               atr20=a, state="flat")
    if pos is not None:
        side = pos["side"]
        out.update(state="long" if side > 0 else "short",
                   entry_date=datetime.fromtimestamp(pos["t_entry"] / 1000, timezone.utc).strftime("%Y-%m-%d"),
                   entry=pos["entry"], stop=pos["stop"],
                   exit_level=(min(b[3] for b in bars[k - EXIT_N + 1:k + 1]) if side > 0
                               else max(b[2] for b in bars[k - EXIT_N + 1:k + 1])),
                   r_open=None if pos.get("entry_due") else side * (c - pos["entry"]) / abs(pos["entry"] - pos["stop"]),
                   entry_due=bool(pos.get("entry_due")), exit_due=bool(pos.get("exit_due")))
        if "target" in pos:
            out.update(target=pos["target"])
        if "stop_now" in pos:
            risk = abs(pos["entry"] - pos["stop"])
            out.update(stop_now=pos["stop_now"], scale_px=pos["scale_px"],
                       scale_date=datetime.fromtimestamp(pos["t_scale"] / 1000, timezone.utc).strftime("%Y-%m-%d"),
                       r_open=0.5 * side * (pos["scale_px"] - pos["entry"]) / risk + 0.5 * side * (c - pos["entry"]) / risk)
    elif k >= ENTRY_N - 1 and a:
        hi = max(b[2] for b in bars[k - ENTRY_N + 1:k + 1]); lo = min(b[3] for b in bars[k - ENTRY_N + 1:k + 1])
        out.update(long_trigger=hi, short_trigger=lo, long_stop=hi - STOP_ATR * a, short_stop=lo + STOP_ATR * a)
    return out


def result_r(tr, funding):
    """A closed trade in R after fees, slippage and funding. funding: sorted list of (t_ms, rate). A trade
    that closed half at its target (TZ-80) gains half its move to the target and half its move to the exit,
    pays the whole position's funding up to the day of the target and half of it after, and the same
    costs, since it trades the same notional."""
    side, e, x = tr["side"], tr["entry"], tr["exit"]
    dist = abs(e - tr["stop"]) / e
    if "t_scale" not in tr:
        paid = side * sum(r for t, r in funding if tr["t_entry"] < t <= tr["t_exit"])
        return (side * (x / e - 1) - paid - 2 * COST_SIDE) / dist
    paid = side * (sum(r for t, r in funding if tr["t_entry"] < t <= tr["t_scale"])
                   + 0.5 * sum(r for t, r in funding if tr["t_scale"] < t <= tr["t_exit"]))
    gain = 0.5 * side * (tr["scale_px"] / e - 1) + 0.5 * side * (x / e - 1)
    return (gain - paid - 2 * COST_SIDE) / dist


def rank(symbols):
    """The order the book takes one open's entries in (TZ-81): the MAJORS first, then the others, each in the
    order given -- the list's. A symbol's rank by name."""
    return {s: k for k, s in enumerate(sorted(symbols, key=lambda s: s not in MAJORS))}


def spans(symbol, trades, pos, t_next=None):
    """One symbol's positions as hold() reads them (TZ-81): (symbol, side, t_entry, free) each, free the (time,
    phase) at which the position's slot frees, or None while it stands. A position whose exit is due frees its
    slot at t_next, the open of the day still forming."""
    out = [(symbol, tr["side"], tr["t_entry"], (tr["t_exit"], AT_OPEN if tr["why"] == "channel" else IN_DAY))
           for tr in trades]
    if pos is not None:
        out.append((symbol, pos["side"], pos["t_entry"],
                    (t_next, AT_OPEN) if pos.get("exit_due") and t_next is not None else None))
    return out


def hold(books, ranks, side_max, book_max, fixed=None):
    """The book the owner can hold (TZ-81): the (symbol, t_entry) of each span it takes. Walked in time from an
    empty book, an entry is taken where, at its open, fewer than side_max positions are held on its side and
    fewer than book_max in all, and a position taken keeps its slot until its own exit -- after its target as
    before it. An entry not taken at its own open is never taken. fixed maps an entry already decided to whether
    it was taken, and the walk takes or leaves it so whatever the room."""
    events = []
    for symbol, side, t_entry, free in books:
        events.append(((t_entry, ENTRY, ranks[symbol]), (symbol, t_entry), side))
        if free is not None:
            events.append((free + (ranks[symbol],), (symbol, t_entry), side))
    now, taken = {}, set()
    for (_, phase, _), key, side in sorted(events):
        if phase != ENTRY:
            now.pop(key, None)
        elif (fixed or {}).get(key, list(now.values()).count(side) < side_max and len(now) < book_max):
            now[key] = side
            taken.add(key)
    return taken


def _get(url):
    with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_S) as r:
        return r.read()


def live_day(symbol, now_ms):
    """The closed daily bars, oldest first, and the day still forming as a bar of its own, its close the last
    price (TZ-80). A read without that day is refused rather than replayed without it (TZ-68)."""
    rows = json.loads(_get(FAPI_KLINES % symbol))
    bars = [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) < now_ms]
    forming = [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) >= now_ms]
    if not forming:
        raise ValueError("the read holds no day still forming")
    return bars, forming[0]


def live_bars(symbol, now_ms):
    """The closed daily bars, oldest first, and the open of the day still forming: the fill of a signal at
    the last close (TZ-68)."""
    bars, today = live_day(symbol, now_ms)
    return bars, today[1]


def state_of(symbol, bars, open_now, scale=None):
    """One symbol's state on these bars and the replay behind it: (state, trades, position). A history of
    ENTRY_N days or fewer carries none but short-history (TZ-79); scale makes the plan's (TZ-80)."""
    trades, pos = replay(bars, open_now, scale)
    out = dict(symbol=symbol, **levels(bars, pos)) if len(bars) > ENTRY_N else dict(symbol=symbol, state="short-history")
    return out, trades, pos


def live_state(symbol, now_ms, scale=None):
    """One symbol's state today and the replay behind it: (state, trades, position). The state is the object
    --live prints (TZ-79), the plan's with scale (TZ-80)."""
    bars, open_now = live_bars(symbol, now_ms)
    return state_of(symbol, bars, open_now, scale)


def _csv_rows(blob):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for name in z.namelist():
            for r in csv.reader(io.TextIOWrapper(z.open(name), "utf-8")):
                if r and r[0][:1].isdigit():
                    yield r


def _archive_blob(path, cache):
    """One archive file, read once: kept in the cache, and a 404 kept as an empty marker beside it."""
    local = os.path.join(cache, path.replace("/", "_"))
    if os.path.exists(local + ".404"):
        return None
    if os.path.exists(local):
        with open(local, "rb") as fh:
            return fh.read()
    try:
        blob = _get(ARCHIVE + "/" + path)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            open(local + ".404", "w").close()
            return None
        raise
    tmp = local + ".part"
    with open(tmp, "wb") as fh:
        fh.write(blob)
    os.replace(tmp, local)
    return blob


def _ms(t):
    t = int(t)
    return t // 1000 if t > 10 ** 14 else t       # the archive moved to microseconds in 2025


def archive_series(symbol, start, end, cache):
    """Daily bars and funding prints of one symbol from the archive, start..end inclusive (UTC dates). A day
    missing between two bars -- the exchange's gap, or a month the cache remembers as a 404 from before it
    was published -- is refused, never replayed over: replay() reads one bar per UTC day (TZ-68)."""
    bars, funding = {}, {}
    m = date(start.year, start.month, 1)
    last_month = date(end.year, end.month, 1)
    while m <= last_month:
        tag = "%d-%02d" % (m.year, m.month)
        blob = _archive_blob("monthly/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, tag), cache)
        if blob is None and m == last_month:          # the current month has daily files only
            d = m
            while d <= end:
                b = _archive_blob("daily/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, d.isoformat()), cache)
                for r in _csv_rows(b) if b else ():
                    bars[_ms(r[0])] = (_ms(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]))
                d += timedelta(days=1)
        for r in _csv_rows(blob) if blob else ():
            bars[_ms(r[0])] = (_ms(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]))
        fb = _archive_blob("monthly/fundingRate/%s/%s-fundingRate-%s.zip" % (symbol, symbol, tag), cache)
        for r in _csv_rows(fb) if fb else ():
            funding[_ms(r[0])] = float(r[2])
        m = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    lo = datetime(start.year, start.month, start.day, tzinfo=timezone.utc).timestamp() * 1000
    hi = datetime(end.year, end.month, end.day, tzinfo=timezone.utc).timestamp() * 1000
    out = [bars[t] for t in sorted(bars) if lo <= t <= hi]
    for a, b in zip(out, out[1:]):
        if b[0] - a[0] != DAY_MS:
            raise ValueError("%s: the archive has no daily bar between %s and %s" % (
                symbol, datetime.fromtimestamp(a[0] / 1000, timezone.utc).date(),
                datetime.fromtimestamp(b[0] / 1000, timezone.utc).date()))
    return out, sorted(funding.items())


def summary(rs):
    """n, win share, mean R, total R, profit factor, max drawdown in R over the trades in exit order."""
    if not rs:
        return dict(n=0)
    wins = sum(r for r in rs if r > 0); losses = -sum(r for r in rs if r < 0)
    peak = run = dd = 0.0
    for r in rs:
        run += r; peak = max(peak, run); dd = max(dd, peak - run)
    return dict(n=len(rs), win=sum(1 for r in rs if r > 0) / len(rs), mean=sum(rs) / len(rs), total=sum(rs),
                pf=(wins / losses) if losses > 0 else float("inf"), maxdd=dd)


def archive_paths(symbol, start, end):
    """Every archive file archive_series may read for one symbol."""
    paths = []
    m = date(start.year, start.month, 1)
    last_month = date(end.year, end.month, 1)
    while m <= last_month:
        tag = "%d-%02d" % (m.year, m.month)
        paths.append("monthly/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, tag))
        paths.append("monthly/fundingRate/%s/%s-fundingRate-%s.zip" % (symbol, symbol, tag))
        m = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    d = last_month
    while d <= end:
        paths.append("daily/klines/%s/1d/%s-1d-%s.zip" % (symbol, symbol, d.isoformat()))
        d += timedelta(days=1)
    return paths


def archive(symbols, start, end, cache, workers=8, scale=None, ceilings=None):
    """Every trade over the archive and its table; with ceilings, (side, book), only the trades hold() takes, the
    symbols ranked in the order given (TZ-81)."""
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda path: _archive_blob(path, cache),
                    [path for s in symbols for path in archive_paths(s, start, end)]))
    rows, books = [], []
    for s in symbols:
        bars, funding = archive_series(s, start, end, cache)
        trades, pos = replay(bars, scale=scale)
        books += spans(s, trades, pos)
        for tr in trades:
            rows.append((tr["t_exit"], s, tr["side"], tr["t_entry"], result_r(tr, funding), tr["why"]))
    if ceilings is not None:
        taken = hold(books, rank(symbols), *ceilings)
        rows = [r for r in rows if (r[1], r[3]) in taken]
    rows.sort()
    oos = datetime(OOS_START.year, OOS_START.month, OOS_START.day, tzinfo=timezone.utc).timestamp() * 1000
    out = {}
    for name, keep in (("in-sample", lambda r: r[3] < oos), ("out-of-sample", lambda r: r[3] >= oos),
                       ("all", lambda r: True)):
        part = [r for r in rows if keep(r)]
        out[name] = dict(summary([r[4] for r in part]),
                         long=summary([r[4] for r in part if r[2] > 0]), short=summary([r[4] for r in part if r[2] < 0]))
    return rows, out


def main(argv=None):
    ap = argparse.ArgumentParser(description="the trend book: live states or the archive's record")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--archive", action="store_true")
    ap.add_argument("--from", dest="start", default="2023-01-01")
    ap.add_argument("--to", dest="end", default=None)
    ap.add_argument("--cache", default=os.path.join(os.path.expanduser("~"), ".cache", "crypto-book"))
    ap.add_argument("--scale", type=float, default=None, help="the plan: half closes at this many R (TZ-80)")
    ap.add_argument("--hold", default=None, metavar="SIDE,BOOK",
                    help="the archive's trades the book holds under these ceilings (TZ-81)")
    ap.add_argument("symbols", nargs="+")
    a = ap.parse_args(argv)
    if a.live == a.archive:
        ap.error("exactly one of --live and --archive")
    if a.hold is not None and (a.live or not re.fullmatch(r"[1-9]\d*,[1-9]\d*", a.hold)):
        ap.error("--hold SIDE,BOOK reads the archive; the live book held is score.py's")
    if a.live:
        now_ms = int(time.time() * 1000)
        for s in a.symbols:
            try:
                out = live_state(s, now_ms, a.scale)[0]
            except Exception as exc:          # one symbol's failure never hides the others
                out = dict(symbol=s, state="unread", error=exc.__class__.__name__)
            print(json.dumps(out, sort_keys=True), flush=True)
        return 0
    os.makedirs(a.cache, exist_ok=True)
    end = date.fromisoformat(a.end) if a.end else (datetime.now(timezone.utc).date() - timedelta(days=2))
    rows, out = archive(a.symbols, date.fromisoformat(a.start), end, a.cache, scale=a.scale,
                        ceilings=None if a.hold is None else tuple(int(n) for n in a.hold.split(",")))
    for name, s in out.items():
        if not s["n"]:
            print("%-14s no trades" % name); continue
        print("%-14s trades %4d  win %.2f  mean R %+.3f  total R %+8.2f  PF %.2f  max DD %6.2f R  "
              "long %d (%+.2f R)  short %d (%+.2f R)" % (name, s["n"], s["win"], s["mean"], s["total"], s["pf"],
                                                         s["maxdd"], s["long"].get("n", 0), s["long"].get("total", 0.0),
                                                         s["short"].get("n", 0), s["short"].get("total", 0.0)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
