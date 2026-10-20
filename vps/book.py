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

Python 3.12's standard library only. Time is UTC everywhere.
"""
import argparse
import concurrent.futures
import csv
import io
import json
import os
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


def replay(bars, open_now=None):
    """bars: closed daily bars (t_open_ms, open, high, low, close), oldest first, one per UTC day.
    Returns (trades, position): each closed trade as a dict, and the open position after the last bar
    or None. A signal at day k's close fills at day k+1's open; a stop fills at the stop, or at the open
    when the day opened beyond it; a channel exit at day k's close fills at day k+1's open. A signal at
    the last bar's close fills at open_now, the open of the day still forming, and its position carries
    entry_due; without open_now (the archive) that signal has no fill yet and opens nothing (TZ-68)."""
    trades, pos = [], None
    for k in range(len(bars)):
        t, o, h, l, c = bars[k]
        if pos is not None and k >= pos["k_entry"]:
            side, stop = pos["side"], pos["stop"]
            if (side > 0 and l <= stop) or (side < 0 and h >= stop):
                px = o if (side > 0 and o < stop) or (side < 0 and o > stop) else stop
                trades.append(dict(pos, k_exit=k, t_exit=t, exit=px, why="stop"))
                pos = None
            elif k >= EXIT_N:
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
    return trades, pos


def levels(bars, pos):
    """What the next close decides, from the last closed bar: the trigger and the stop a new trade would
    take, or the open position's exit level. A position whose entry is due has no open R yet."""
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
    elif k >= ENTRY_N - 1 and a:
        hi = max(b[2] for b in bars[k - ENTRY_N + 1:k + 1]); lo = min(b[3] for b in bars[k - ENTRY_N + 1:k + 1])
        out.update(long_trigger=hi, short_trigger=lo, long_stop=hi - STOP_ATR * a, short_stop=lo + STOP_ATR * a)
    return out


def result_r(tr, funding):
    """A closed trade in R after fees, slippage and funding. funding: sorted list of (t_ms, rate)."""
    side, e, x = tr["side"], tr["entry"], tr["exit"]
    dist = abs(e - tr["stop"]) / e
    paid = side * sum(r for t, r in funding if tr["t_entry"] < t <= tr["t_exit"])
    return (side * (x / e - 1) - paid - 2 * COST_SIDE) / dist


def _get(url):
    with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT_S) as r:
        return r.read()


def live_bars(symbol, now_ms):
    """The closed daily bars, oldest first, and the open of the day still forming: the fill of a signal at
    the last close. A read without that day is refused rather than replayed without it (TZ-68)."""
    rows = json.loads(_get(FAPI_KLINES % symbol))
    bars = [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows if int(r[6]) < now_ms]
    forming = [float(r[1]) for r in rows if int(r[6]) >= now_ms]
    if not forming:
        raise ValueError("the read holds no day still forming")
    return bars, forming[0]


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


def archive(symbols, start, end, cache, workers=8):
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda path: _archive_blob(path, cache),
                    [path for s in symbols for path in archive_paths(s, start, end)]))
    rows = []
    for s in symbols:
        bars, funding = archive_series(s, start, end, cache)
        trades, _ = replay(bars)
        for tr in trades:
            rows.append((tr["t_exit"], s, tr["side"], tr["t_entry"], result_r(tr, funding), tr["why"]))
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
    ap.add_argument("symbols", nargs="+")
    a = ap.parse_args(argv)
    if a.live == a.archive:
        ap.error("exactly one of --live and --archive")
    if a.live:
        now_ms = int(time.time() * 1000)
        for s in a.symbols:
            try:
                bars, open_now = live_bars(s, now_ms)
                trades, pos = replay(bars, open_now)
                out = dict(symbol=s, **levels(bars, pos)) if len(bars) > ENTRY_N else dict(symbol=s, state="short-history")
            except Exception as exc:          # one symbol's failure never hides the others
                out = dict(symbol=s, state="unread", error=exc.__class__.__name__)
            print(json.dumps(out, sort_keys=True), flush=True)
        return 0
    os.makedirs(a.cache, exist_ok=True)
    end = date.fromisoformat(a.end) if a.end else (datetime.now(timezone.utc).date() - timedelta(days=2))
    rows, out = archive(a.symbols, date.fromisoformat(a.start), end, a.cache)
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
