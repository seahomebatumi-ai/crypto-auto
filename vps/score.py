#!/usr/bin/env python3
"""The book's signal and its forward ledger (TZ-79): once a day, after the daily close, every entry and
exit the trend book made on the list reaches the owner as one alert, and every trade the book has closed
since it went into code is written once to a ledger that no later run rewrites. It runs no model and
reads no credential.

    score.py [--state DIR] [--outbox DIR]     default /var/lib/crypto-auto and the bot's outbox

The book is book.live_state() and nothing else -- the function `book.py --live` prints from, on the same
reads -- and a trade's result is book.result_r() on the funding prints the exchange publishes for its
span. A trade whose prints did not arrive whole is not written: the next run asks again (map inv. 70).

    score-ledger/         one closed trade a file, <SYMBOL>-<entry stamp>.json, written once and within
                          RETRY_DAYS of its close, and never reopened (map inv. 38): a later replay that
                          reads its trade differently is counted, and a close found later than that is
                          counted and never written -- the replay's window slides, and the ledger takes
                          no file about a past it did not see
    score.json            this run's reading: the day it stands on, the open positions, the totals

Prints one line, and one before it for each trade it could not price; never a price. Exit 0 the reading is written · 4 no symbol was read, or the read is
older than the record: nothing written · 5 a file of the ledger is not a trade: nothing written.
"""
import argparse
import json
import math
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book  # noqa: E402
import common  # noqa: E402
import writer  # noqa: E402

# Methodology 2026-10-21-a: the first day every level the answer prints is this book's.
GO_LIVE = "2026-10-21"
# Map section 10, row "The book's out-of-sample loss sits in the alts": the five symbols its lead names,
# totalled apart from the first forward day, so that the lead is read on trades it has not seen.
MAJORS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT")
FUNDING_URL = "https://fapi.binance.com/fapi/v1/fundingRate?symbol=%s&startTime=%d&endTime=%d&limit=1000"
FUNDING_PAGE = 1000                              # the endpoint's own ceiling of rows an answer
FUNDING_PAGES_MAX = 20
# No USD-M perpetual settles less often than every eight hours: a wider gap is a span read in part.
FUNDING_GAP_MS = 8 * 3600 * 1000 + 60 * 1000
# A close is written while it is this recent, so that prints refused today are asked for again and a
# unit that was down catches up; the first files of an empty ledger reach back to GO_LIVE.
# Derived: the Architect's probe of 12.11.2026 -- twelve random markets, 455 daily runs on a 400-row
# window, three seeds: unbounded, the ledger took 266, 253 and 296 trades the full history never made; at
# 200 days 21, 0 and 0; at 120, 60 and 30 none, every trade equal to the full history's.
RETRY_DAYS = 60
LEDGER = "score-ledger"
RECORD = "score.json"
LEDGER_KEYS = ("symbol", "side", "t_entry", "entry", "stop", "t_exit", "exit", "why", "r", "seen")

# The alert, in the owner's words; a number he may type prints as a code span (the bot of TZ-71).
T_HEAD = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410** "
          "\u00b7 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
T_HEAD_BASE = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410 \u2014 "
               "\u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043e** \u00b7 \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
T_OPEN = ("{dot} **\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u043e\u0442\u043a\u0440\u044b\u043b\u043e {side}:** "
          "{sym} \u00b7 \u0432\u0445\u043e\u0434 `{entry}` \u00b7 \u0441\u0442\u043e\u043f `{stop}` ({dist}%)")
T_LATE = " \u00b7 \u0432\u0445\u043e\u0434 \u0431\u044b\u043b {date}"
T_CLOSING = ("\U0001f6aa **\u041f\u0440\u0430\u0432\u0438\u043b\u043e \u0432\u044b\u0445\u043e\u0434\u0438\u0442 \u0441\u0435\u0433\u043e\u0434\u043d\u044f:** "
             "{sym} {side} \u2014 \u043f\u043e \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f")
T_CLOSED = ("\u2705 **\u0421\u0434\u0435\u043b\u043a\u0430 "
            "\u0437\u0430\u043a\u0440\u044b\u0442\u0430:** {sym} {side} \u2014 {why} \u00b7 **{r} R**")
T_SCORE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u043e "
           "**{n}** \u00b7 **{total} R** \u00b7 \u0432 \u043f\u043b\u044e\u0441\u0435 {wins}")
T_SCORE_NONE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u044b\u0445 "
                "\u0441\u0434\u0435\u043b\u043e\u043a \u043f\u043e\u043a\u0430 \u043d\u0435\u0442")
T_GROUPS = ("BTC ETH SOL BNB XRP: {n1} \u00b7 {r1} R \u00b7 "
            "\u043e\u0441\u0442\u0430\u043b\u044c\u043d\u044b\u0435: {n2} \u00b7 {r2} R")
T_OPEN_NOW = ("\u0412 \u0441\u0434\u0435\u043b\u043a\u0435 {n}: \u043b\u043e\u043d\u0433 {nl} \u00b7 \u0448\u043e\u0440\u0442 "
              "{ns} \u00b7 \u043f\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f {r} R")
T_HELD = "\u041c\u043e\u043d\u0435\u0442\u044b: {rows}"
T_LEGEND = ("R \u2014 \u043e\u0434\u0438\u043d \u0440\u0438\u0441\u043a "
            "\u043d\u0430 \u0441\u0434\u0435\u043b\u043a\u0443.")
T_FOOT = ("\u0420\u0430\u0437\u043c\u0435\u0440 \u0438 \u043f\u043b\u0435\u0447\u043e \u2014 "
          "\u043a\u043d\u043e\u043f\u043a\u043e\u0439 \u0430\u043d\u0430\u043b\u0438\u0437\u0430.")
SIDE = {1: "\u043b\u043e\u043d\u0433", -1: "\u0448\u043e\u0440\u0442"}
DOT = {1: "\U0001f7e2", -1: "\U0001f534"}
WHY = {"stop": "\u043f\u043e \u0441\u0442\u043e\u043f\u0443", "channel": "\u043f\u043e \u043f\u0440\u0430\u0432\u0438\u043b\u0443 \u0432\u044b\u0445\u043e\u0434\u0430"}
MINUS = "\u2212"
SEP = " \u00b7 "


def list_symbols():
    """The list as the payload carries it: BTCUSDT, then tokens[] in its own order."""
    return writer.payload_symbols(os.path.dirname(common.index_html_path()))


def day(ms):
    """The UTC date of a millisecond stamp, YYYY-MM-DD."""
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")


def funding_prints(symbol, t_entry, t_exit):
    """The symbol's funding prints of a trade's span as sorted (t_ms, rate) pairs, read page by page and
    refused unless whole: a list of rows with a finite rate each, the first print inside the span within
    FUNDING_GAP_MS of the entry, the last within it of the exit, no wider gap between two. A trade that
    closed on its entry day has no span and asks for nothing."""
    if t_exit <= t_entry:
        return []
    out, start = {}, t_entry
    for _ in range(FUNDING_PAGES_MAX):
        rows = json.loads(book._get(FUNDING_URL % (symbol, start, t_exit)))
        if not isinstance(rows, list):
            raise ValueError("fundingRate answered no list")
        for row in rows:
            t, rate = int(row["fundingTime"]), float(row["fundingRate"])
            if not math.isfinite(rate):
                raise ValueError("a funding rate is not finite")
            out[t] = rate
        if len(rows) < FUNDING_PAGE:
            break
        start = max(out) + 1
    else:
        raise ValueError("fundingRate did not end in %d pages" % FUNDING_PAGES_MAX)
    inside = sorted(t for t in out if t_entry < t <= t_exit)
    edges = [t_entry] + inside + [t_exit]
    if not inside or any(b - a > FUNDING_GAP_MS for a, b in zip(edges, edges[1:])):
        raise ValueError("the funding prints do not cover the trade's span")
    return sorted(out.items())


def row_name(row):
    """The file a closed trade is written to: its symbol and the stamp of its entry day."""
    return "%s-%d.json" % (row["symbol"], row["t_entry"])


def read_ledger(path):
    """Every trade of the ledger directory, in the order of the file names. A missing directory is an empty
    ledger; a file that is not the trade its name says raises."""
    try:
        names = sorted(name for name in os.listdir(path) if name.endswith(".json") and not name.startswith("."))
    except FileNotFoundError:
        return []
    rows = []
    for name in names:
        with open(os.path.join(path, name), encoding="utf-8") as fh:
            row = json.load(fh)
        if not isinstance(row, dict) or any(key not in row for key in LEDGER_KEYS) or row_name(row) != name:
            raise ValueError("a ledger file is not a trade")
        rows.append(row)
    return rows


def totals(rows):
    """book.summary over the rows in the order their trades closed; a profit factor with no loss is null."""
    out = book.summary([row["r"] for row in sorted(rows, key=lambda row: (row["t_exit"], row["symbol"]))])
    if "pf" in out and not math.isfinite(out["pf"]):
        out["pf"] = None
    return out


def px(value):
    """A price to six significant figures, trailing zeros dropped, never in exponent form."""
    if not value:
        return "0"
    text = "%.*f" % (max(0, 5 - int(math.floor(math.log10(abs(value))))), value)
    return text.rstrip("0").rstrip(".") if "." in text else text


def signed(value, digits):
    """A number with its sign, the minus as the answer prints it."""
    return ("%+.*f" % (digits, value)).replace("-", MINUS)


def ddmm(iso):
    return iso[8:10] + "." + iso[5:7]


def name(symbol):
    return symbol[:-4] if symbol.endswith("USDT") else symbol


def side_of(state):
    return 1 if state["state"] == "long" else -1


def compose(asof, baseline, opened, closing, closed, rows, open_rows):
    """The alert's text: one event to a line, then the rule's record since GO_LIVE."""
    lines = [(T_HEAD_BASE if baseline else T_HEAD).format(d=ddmm(asof))]
    for o in opened:
        side = side_of(o)
        line = T_OPEN.format(dot=DOT[side], side=SIDE[side], sym=name(o["symbol"]), entry=px(o["entry"]),
                             stop=px(o["stop"]), dist=signed((o["stop"] / o["entry"] - 1) * 100, 1))
        lines.append(line if o["entry_due"] else line + T_LATE.format(date=ddmm(o["entry_date"])))
    for o in closing:
        lines.append(T_CLOSING.format(sym=name(o["symbol"]), side=SIDE[side_of(o)]))
    for row in closed:
        lines.append(T_CLOSED.format(sym=name(row["symbol"]), side=SIDE[row["side"]],
                                     why=WHY.get(row["why"], row["why"]), r=signed(row["r"], 2)))
    since = GO_LIVE[8:10] + "." + GO_LIVE[5:7] + "." + GO_LIVE[:4]
    every = totals(rows)
    if every["n"]:
        majors = totals([row for row in rows if row["symbol"] in MAJORS])
        others = totals([row for row in rows if row["symbol"] not in MAJORS])
        lines.append(T_SCORE.format(since=since, n=every["n"], total=signed(every["total"], 2),
                                    wins=sum(1 for row in rows if row["r"] > 0)))
        lines.append(T_GROUPS.format(n1=majors["n"], r1=signed(majors.get("total", 0.0), 2),
                                     n2=others["n"], r2=signed(others.get("total", 0.0), 2)))
    else:
        lines.append(T_SCORE_NONE.format(since=since))
    lines.append(T_OPEN_NOW.format(n=len(open_rows), nl=sum(1 for o in open_rows if side_of(o) > 0),
                                   ns=sum(1 for o in open_rows if side_of(o) < 0),
                                   r=signed(sum(o["r_open"] for o in open_rows if o["r_open"] is not None), 2)))
    if baseline and open_rows:
        lines.append(T_HELD.format(rows=SEP.join(DOT[side_of(o)] + " " + name(o["symbol"]) for o in open_rows)))
    if baseline:
        lines.append(T_LEGEND)
    if opened:
        lines.append(T_FOOT)
    return "\n".join(lines)


def main(argv=None, now_ms=None):
    parser = argparse.ArgumentParser(description="the trend book's daily signal and forward ledger")
    parser.add_argument("--state", default=common.STATE_DIR)
    parser.add_argument("--outbox", default=None, help="where the alert is written; the bot's outbox by default")
    args = parser.parse_args(argv)
    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
    ledger_path, record_path = os.path.join(args.state, LEDGER), os.path.join(args.state, RECORD)
    try:
        ledger = read_ledger(ledger_path)
    except (OSError, ValueError, TypeError):
        common.log("score: a file of the ledger is not a trade, nothing written")
        return 5
    try:
        with open(record_path, encoding="utf-8") as fh:
            prev = json.load(fh)
        prev_asof, prev_ts = str(prev["asof"]), str(prev["ts"])
    except (OSError, ValueError, KeyError, TypeError):
        prev_asof = prev_ts = None
    baseline = prev_asof is None

    symbols = list_symbols()
    read, unread = [], []
    for symbol in symbols:
        try:
            read.append(book.live_state(symbol, now_ms))
        except Exception:                 # one symbol's failure never hides the others
            unread.append(symbol)
    asof = max((state["asof"] for state, _, _ in read if "asof" in state), default=None)
    if asof is None or (not baseline and asof < prev_asof):
        common.log("score: asof=%s symbols=%d read=%d nothing written" % (asof or "-", len(symbols), len(read)))
        return 4
    # A symbol whose last closed day is not the day the others stand on is not read today.
    unread += [state["symbol"] for state, _, _ in read if state.get("asof", asof) != asof]
    live = [item for item in read if item[0].get("asof", asof) == asof]
    fresh = baseline or asof > prev_asof
    seen = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000))

    known = {(row["symbol"], row["t_entry"]): row for row in ledger}
    floor = GO_LIVE if not ledger else (date.fromisoformat(asof) - timedelta(days=RETRY_DAYS)).isoformat()
    added, pending, late, disagree = [], 0, 0, 0
    for state, trades, _ in live:
        for tr in trades:
            if day(tr["t_entry"]) < GO_LIVE:
                continue
            key = (state["symbol"], tr["t_entry"])
            if key in known:
                row = known[key]
                disagree += (row["t_exit"], row["exit"], row["why"]) != (tr["t_exit"], tr["exit"], tr["why"])
                continue
            if day(tr["t_exit"]) < floor:
                late += 1
                continue
            try:
                r = book.result_r(tr, funding_prints(state["symbol"], tr["t_entry"], tr["t_exit"]))
                if not math.isfinite(r):
                    raise ValueError("the result is not finite")
            except Exception as exc:      # not written: the next run asks for the prints again (inv. 70)
                pending += 1
                common.log("score: pending %s %s" % (state["symbol"], exc.__class__.__name__))
                continue
            known[key] = {"symbol": state["symbol"], "side": tr["side"], "t_entry": tr["t_entry"],
                          "entry": tr["entry"], "stop": tr["stop"], "t_exit": tr["t_exit"], "exit": tr["exit"],
                          "why": tr["why"], "r": r, "seen": seen}
            added.append(known[key])
    if added:
        os.makedirs(ledger_path, mode=0o750, exist_ok=True)
        for row in added:                 # a new file each: nothing that stands is opened (inv. 38)
            common.atomic_write(os.path.join(ledger_path, row_name(row)), row, mode=0o640)
    rows = ledger + added

    open_rows = [state for state, _, _ in live if state["state"] in ("long", "short")]
    if baseline:
        opened = [o for o in open_rows if o["entry_due"]]
    else:
        after = (date.fromisoformat(prev_asof) + timedelta(days=1)).isoformat()
        opened = [o for o in open_rows if fresh and o["entry_date"] > after]
    closing = [o for o in open_rows if fresh and o["exit_due"]]
    # A closed trade is told once: the rows written since the record this run replaces.
    closed = [] if baseline else [row for row in rows if row["seen"] > prev_ts]
    alert = baseline or bool(opened or closing or closed)
    if alert:
        common.write_outbox("alert", compose(asof, baseline, opened, closing, closed, rows, open_rows),
                            outbox_dir=args.outbox)
    common.atomic_write(record_path, {
        "v": 1, "k": "score", "ts": seen, "asof": asof, "since": GO_LIVE, "symbols": len(symbols),
        "unread": sorted(unread),
        "open": [{key: o[key] for key in ("symbol", "state", "entry_date", "entry", "stop", "exit_level",
                                          "r_open", "entry_due", "exit_due")} for o in open_rows],
        "closed": {"all": totals(rows), "majors": totals([row for row in rows if row["symbol"] in MAJORS]),
                   "others": totals([row for row in rows if row["symbol"] not in MAJORS])},
        "pending": pending, "late": late, "disagree": disagree}, mode=0o640)
    common.log("score: asof=%s symbols=%d read=%d unread=%d open=%d opened=%d closing=%d closed=%d pending=%d "
               "late=%d disagree=%d ledger=%d alert=%s" % (asof, len(symbols), len(symbols) - len(unread), len(unread),
                                                           len(open_rows), len(opened), len(closing), len(closed),
                                                           pending, late, disagree, len(rows), "yes" if alert else "no"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
