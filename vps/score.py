#!/usr/bin/env python3
"""The book's signal and its forward ledger (TZ-79, TZ-80, TZ-81, TZ-84, TZ-85). It runs no model and reads no
credential.

    score.py [--state DIR] [--outbox DIR]              the daily close
    score.py --forming [--state DIR] [--outbox DIR]    the look at the day still forming

The daily close: every entry, target and exit of the book the owner holds reaches him as one alert -- each
entry with its stop, its target and its size at his medium risk, and the plan's entries his ceilings leave no
room for named on one line -- and every trade the book, the plan and the rule have closed since the book went
into code is written once to a ledger that no later run rewrites.

The look: once a day, hours before the close, what the day has already done to the book's positions -- a stop
reached, a target reached -- and the entry its close would make if it came at the last price reach him as one
alert, the entry named a candidate, because the close may still take it back. The look writes no ledger and
opens no trade: the daily close alone does.

The book is book.state_of() on one read of each symbol: the rule's state, which `book.py --live` prints, and
the plan's, which `book.py --live --scale 2` prints; the look's is the plan's on the same bars with the day
still forming appended as it stands. The book held is book.hold() over the plan's positions entered since
GO_LIVE, under the owner's ceilings (TZ-81): what he is told and what the gate scores are one book, and a run
that cannot read his ceilings writes nothing. A trade's result is book.result_r() on the funding prints the
exchange publishes for its span; a trade whose prints did not arrive whole is not written, and the next run asks
again (map inv. 70). The size and the ceilings are the owner's, read from analyst/owner.json through paper.py
(inv. 38).

    score-held/           the book held's ledger, which the gate reads: one closed trade a file, as
                          score-ledger/ below
    score-plan/           the plan's every entry, the same way
    score-ledger/         one closed trade a file, <SYMBOL>-<entry stamp>.json, written once and within
                          RETRY_DAYS of its close, and never reopened (map inv. 38): a later replay that
                          reads its trade differently is counted, and a close found later than that is
                          counted and never written -- the replay's window slides, and the ledger takes
                          no file about a past it did not see
    score-cards/          every card the analysis answer printed (TZ-84), from the CARD| lines of the day
                          logs this checkout carries, followed as its card says from the minute its answer
                          reached main (TZ-85): one trade a coin, side and fill however many runs print it,
                          one closed trade a file, <SYMBOL>-<long|short>-<fill stamp>.json, written once on its
                          close and never reopened
    score-cards-done/     one card a file, <stem>-<rank>.json, written once where the card made no trade or
                          the trade it made stands closed under an earlier card (TZ-85): a card that has its
                          file, or a closed trade of its own, is never read again
    score-forming/        one look a file, <YYYY-MM-DD>.json, written once: what the look named, so that
                          the next close counts how much of it came true; a day that has its file is not
                          looked at again
    score.json            the daily close's reading: the day it stands on, the ceilings, the book held's open
                          positions and the plan's it leaves out, the three ledgers' totals, the look's count
                          for that day, and the cards' -- their totals, the cards still open and the counts

Prints one line, and one before it for each trade it could not price; never a price.
Exit 0 the reading is written, or the day was already looked at · 4 no symbol was read, or the read is older
than the record: nothing written · 5 a file of the ledger is not a trade: nothing written · 6 the owner's
ceilings are unread: nothing written.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time
import urllib.error
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book  # noqa: E402
import common  # noqa: E402
import paper  # noqa: E402
import writer  # noqa: E402

# Methodology 2026-10-21-a: the first day every level the answer prints is this book's.
GO_LIVE = "2026-10-21"
# book.MAJORS, totalled apart from the first forward day, so that the lead is read on trades it has not seen.
MAJORS = book.MAJORS
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
PLAN = "score-plan"
HELD = "score-held"
FORMING = "score-forming"
RECORD = "score.json"
LEDGER_KEYS = ("symbol", "side", "t_entry", "entry", "stop", "t_exit", "exit", "why", "r", "seen")
# TZ-84: the card ledger -- every card the answer printed, the record the trust line scores.
CARDS = "score-cards"
CARD_KEYS = ("symbol", "side", "kind", "stem", "rank", "t_entry", "entry", "stop", "target", "t_exit", "exit",
             "why", "r", "seen")
CARD_FIELDS = 16                                 # ANALYST-INSTRUCTIONS.md section 12's CARD| line
CARD_KINDS = ("now", "wait", "limit")
MINUTES_URL = "https://fapi.binance.com/fapi/v1/klines?symbol=%s&interval=1m&startTime=%d&endTime=%d&limit=1500"
MINUTE_MS = 60_000
# TZ-85: a card resolved for good -- no trade, or the trade of an earlier card that stands closed.
CARDS_DONE = "score-cards-done"
DONE_KEYS = ("stem", "rank", "symbol", "side", "kind", "why", "seen")
# TZ-85: the exchange's answers to an address it limits (429) and bans (418); after either, the pass asks no more.
REFUSED_CODES = (418, 429)
GIT_TIMEOUT_S = 30

# The alert, in the owner's words; a number he may type prints as a code span (the bot of TZ-71).
T_HEAD = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410** \u00b7 "
          "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
T_HEAD_BASE = ("\U0001f4c8 **\u0421\u0414\u0415\u041b\u041a\u0418 \u041f\u0420\u0410\u0412\u0418\u041b\u0410 "
               "\u2014 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u043e** \u00b7 "
               "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 \u0434\u043d\u044f {d}")
T_ENTRY = ("{dot} **{side} {sym}** \u00b7 \u0432\u0445\u043e\u0434 `{entry}` \u00b7 \u0441\u0442\u043e\u043f "
           "`{stop}` ({dist}%)")
T_LATE = " \u00b7 \u0432\u0445\u043e\u0434 \u0431\u044b\u043b {date}"
T_PLAN = "\U0001f3af \u0446\u0435\u043b\u044c `{target}` ({tdist}%)"
T_PLAN_SIZE = (" \u00b7 \u043e\u0431\u044a\u0451\u043c `{notional}` USDT \u00b7 \u043c\u0430\u0440\u0436\u0430 "
               "`{margin}` \u043f\u0440\u0438 {lev}x")
T_SCALED = ("\U0001f3af **\u0426\u0435\u043b\u044c \u0432\u0437\u044f\u0442\u0430:** {sym} {side} \u2014 "
            "\u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0430 "
            "\u043f\u043e `{px}`, \u0441\u0442\u043e\u043f \u043e\u0441\u0442\u0430\u0442\u043a\u0430 "
            "\u0442\u0435\u043f\u0435\u0440\u044c `{stop}`")
T_CLOSING = ("\U0001f6aa **\u0412\u044b\u0445\u043e\u0434 \u0441\u0435\u0433\u043e\u0434\u043d\u044f:** {sym} "
             "{side} \u2014 \u043f\u043e \u043e\u0442\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f")
T_CLOSED = ("\u2705 **\u0421\u0434\u0435\u043b\u043a\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0430:** {sym} "
            "{side} \u2014 {why} \u00b7 **{r} R**")
T_SCORE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: \u0437\u0430\u043a\u0440\u044b\u0442\u043e **{n}** "
           "\u00b7 **{total} R** \u00b7 \u0432 \u043f\u043b\u044e\u0441\u0435 {wins}")
T_SCORE_NONE = ("\U0001f4ca \u0421\u0447\u0451\u0442 \u0441 {since}: "
                "\u0437\u0430\u043a\u0440\u044b\u0442\u044b\u0445 \u0441\u0434\u0435\u043b\u043e\u043a "
                "\u043f\u043e\u043a\u0430 \u043d\u0435\u0442")
T_GROUPS = ("BTC ETH SOL BNB XRP: {n1} \u00b7 {r1} R \u00b7 "
            "\u043e\u0441\u0442\u0430\u043b\u044c\u043d\u044b\u0435: {n2} \u00b7 {r2} R")
T_OPEN_NOW = ("\u0412 \u0441\u0434\u0435\u043b\u043a\u0435 {n}: \u043b\u043e\u043d\u0433 {nl} \u00b7 "
              "\u0448\u043e\u0440\u0442 {ns} \u00b7 \u043f\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044e "
              "\u0434\u043d\u044f {r} R")
T_HELD = ("{dot} **{side} {sym}** \u00b7 \u0441\u0442\u043e\u043f `{stop}` \u00b7 \u0446\u0435\u043b\u044c "
          "`{target}`")
T_HELD_DONE = ("{dot} **{side} {sym}** \u00b7 \u0446\u0435\u043b\u044c \u0432\u0437\u044f\u0442\u0430 \u00b7 "
               "\u0441\u0442\u043e\u043f \u043e\u0441\u0442\u0430\u0442\u043a\u0430 `{stop}`")
T_HOW = ("\u0426\u0435\u043b\u044c: \u0437\u0430\u043a\u0440\u044b\u0442\u044c "
         "\u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0443, \u0441\u0442\u043e\u043f "
         "\u043e\u0441\u0442\u0430\u0442\u043a\u0430 \u043f\u0435\u0440\u0435\u043d\u0435\u0441\u0442\u0438 "
         "\u043d\u0430 \u0432\u0445\u043e\u0434; \u043e\u0441\u0442\u0430\u0442\u043e\u043a \u2014 \u0434\u043e "
         "\u0441\u0438\u0433\u043d\u0430\u043b\u0430 \u00ab\u0412\u044b\u0445\u043e\u0434 "
         "\u0441\u0435\u0433\u043e\u0434\u043d\u044f\u00bb.")
T_WHEN = ("\u0412\u0445\u043e\u0434 \u2014 \u043f\u043e \u0440\u044b\u043d\u043a\u0443 \u0432 "
          "\u0442\u0435\u0447\u0435\u043d\u0438\u0435 \u0434\u043d\u044f, \u043f\u043e\u043a\u0430 "
          "\u0446\u0435\u043d\u0430 \u043d\u0435 \u0434\u043e\u0448\u043b\u0430 \u0434\u043e "
          "\u0441\u0442\u043e\u043f\u0430.")
T_LIMIT = ("\u26a0\ufe0f \u0412\u0430\u0448 \u043b\u0438\u043c\u0438\u0442: {side_n} "
           "\u0441\u0434\u0435\u043b\u043e\u043a \u0432 \u043e\u0434\u043d\u0443 "
           "\u0441\u0442\u043e\u0440\u043e\u043d\u0443 \u0438 {book_n} \u0432\u0441\u0435\u0433\u043e, "
           "\u043a\u0430\u0436\u0434\u0430\u044f \u0434\u043e \u2212{risk} USDT \u2014 "
           "\u0441\u0447\u0438\u0442\u0430\u0439\u0442\u0435 \u0432\u043c\u0435\u0441\u0442\u0435 \u0441 "
           "\u043e\u0442\u043a\u0440\u044b\u0442\u044b\u043c\u0438.")
T_OUT = "\u23f8 **\u0412\u043d\u0435 \u043b\u0438\u043c\u0438\u0442\u0430:** {items}"
T_LEGEND = ("R \u2014 \u043e\u0434\u0438\u043d \u0440\u0438\u0441\u043a \u043d\u0430 "
            "\u0441\u0434\u0435\u043b\u043a\u0443.")
# The look at the day still forming (TZ-80): what has happened is told as it is, what the close may still
# take back is told as a candidate.
F_HEAD = ("\u23f1 **\u0421\u041d\u0418\u041c\u041e\u041a \u0414\u041d\u042f** \u00b7 {d} \u00b7 \u0434\u043e "
          "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0434\u043d\u044f {h} \u0447")
F_STOP = ("\u26d4 **\u0421\u0442\u043e\u043f \u0441\u0440\u0430\u0431\u043e\u0442\u0430\u043b:** {sym} {side} "
          "\u2014 \u043f\u043e `{px}`")
F_SCALE = ("\U0001f3af **\u0426\u0435\u043b\u044c \u0434\u043e\u0441\u0442\u0438\u0433\u043d\u0443\u0442\u0430:** "
           "{sym} {side} \u2014 \u043f\u043e\u043b\u043e\u0432\u0438\u043d\u0430 "
           "\u0437\u0430\u043a\u0440\u044b\u0432\u0430\u0435\u0442\u0441\u044f \u043f\u043e `{px}`")
F_ENTRY = ("\u23f3 **\u041a\u0430\u043d\u0434\u0438\u0434\u0430\u0442 \u0432 {side}:** {sym} \u00b7 "
           "\u0441\u0435\u0439\u0447\u0430\u0441 `{last}`")
F_LEVEL = " \u00b7 \u0443\u0440\u043e\u0432\u0435\u043d\u044c `{level}`"
F_ENTRY_PLAN = "\u0441\u0442\u043e\u043f \u2248 `{stop}` \u00b7 \u0446\u0435\u043b\u044c \u2248 `{target}`"
F_FOOT = ("\u041a\u0430\u043d\u0434\u0438\u0434\u0430\u0442 \u2014 \u0435\u0449\u0451 \u043d\u0435 "
          "\u0441\u0434\u0435\u043b\u043a\u0430: \u0435\u0433\u043e "
          "\u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0430\u0435\u0442 "
          "\u0442\u043e\u043b\u044c\u043a\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u0435 "
          "\u0434\u043d\u044f \u0432 04:00, \u0442\u043e\u0433\u0434\u0430 \u043f\u0440\u0438\u0434\u0451\u0442 "
          "\u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 \u0441 "
          "\u0442\u043e\u0447\u043d\u044b\u043c\u0438 \u0447\u0438\u0441\u043b\u0430\u043c\u0438.")
SIDE = {1: "\u043b\u043e\u043d\u0433", -1: "\u0448\u043e\u0440\u0442"}
SIDE_HEAD = {1: "\u041b\u043e\u043d\u0433", -1: "\u0428\u043e\u0440\u0442"}
DOT = {1: "\U0001f7e2", -1: "\U0001f534"}
WHY = {"stop": "\u043f\u043e \u0441\u0442\u043e\u043f\u0443", "channel": "\u043f\u043e \u043f\u0440\u0430\u0432\u0438\u043b\u0443 \u0432\u044b\u0445\u043e\u0434\u0430"}
MINUS = "\u2212"


def list_symbols():
    """The list as the payload carries it: BTCUSDT, then tokens[] in its own order."""
    return writer.payload_symbols(os.path.dirname(common.index_html_path()))


def day(ms):
    """The UTC date of a millisecond stamp, YYYY-MM-DD."""
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime("%Y-%m-%d")


def day_ms(iso):
    """The millisecond stamp at which a UTC date, YYYY-MM-DD, begins."""
    return int(datetime.fromisoformat(iso).replace(tzinfo=timezone.utc).timestamp() * 1000)


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


def entry_lines(o, own):
    """An entry in two lines: the side, the entry and the stop; then the target, the size that loses the owner's
    medium risk at that stop and its margin at the leverage paper.copy_size names."""
    side = side_of(o)
    line = T_ENTRY.format(dot=DOT[side], side=SIDE_HEAD[side], sym=name(o["symbol"]), entry=px(o["entry"]),
                          stop=px(o["stop"]), dist=signed((o["stop"] / o["entry"] - 1) * 100, 1))
    notional, margin, lev, _ = paper.copy_size(own, abs(o["stop"] / o["entry"] - 1))
    plan = (T_PLAN.format(target=px(o["target"]), tdist=signed((o["target"] / o["entry"] - 1) * 100, 1))
            + T_PLAN_SIZE.format(notional="%d" % round(notional), margin="%d" % round(margin), lev=lev))
    return [line if o["entry_due"] else line + T_LATE.format(date=ddmm(o["entry_date"])), plan]


def majors_first(rows):
    return sorted(rows, key=lambda o: o["symbol"] not in MAJORS)


def compose(asof, baseline, opened, skipped, scaled, closing, closed, rows, open_rows, own):
    """The daily close's alert: one event to a line -- an entry in two, the majors first, then on one line the
    plan's entries the ceilings leave out -- then the book's record since GO_LIVE, and under an entry what the
    target means, when to enter and the owner's ceilings. The baseline also prints every position held, with its
    stop and its target, one to a line."""
    lines = [(T_HEAD_BASE if baseline else T_HEAD).format(d=ddmm(asof))]
    for o in majors_first(opened):
        lines += entry_lines(o, own)
    if skipped:
        lines.append(T_OUT.format(items=" \u00b7 ".join(
            SIDE[side] + " " + ", ".join(name(o["symbol"]) for o in majors_first(skipped) if side_of(o) == side)
            for side in (1, -1) if any(side_of(o) == side for o in skipped))))
    for o in scaled:
        lines.append(T_SCALED.format(sym=name(o["symbol"]), side=SIDE[side_of(o)], px=px(o["scale_px"]),
                                     stop=px(o["stop_now"])))
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
    held = majors_first(o for o in open_rows if o not in opened) if baseline else []
    for o in held:
        side = side_of(o)
        if o.get("stop_now") is not None:
            lines.append(T_HELD_DONE.format(dot=DOT[side], side=SIDE_HEAD[side], sym=name(o["symbol"]),
                                            stop=px(o["stop_now"])))
        else:
            lines.append(T_HELD.format(dot=DOT[side], side=SIDE_HEAD[side], sym=name(o["symbol"]),
                                       stop=px(o["stop"]), target=px(o["target"])))
    if opened or held:
        lines.append(T_HOW)
    if opened:
        lines.append(T_WHEN)
    if opened or skipped:
        side_n, book_n = paper.ceilings(own)
        lines.append(T_LIMIT.format(side_n=side_n, book_n=book_n, risk="%d" % round(
            paper.risk_usdt(own["capital_usdt"], own["risk_pct"] / 100))))
    if baseline:
        lines.append(T_LEGEND)
    return "\n".join(lines)


def compose_look(day_now, hours, stopped, scaled, entries):
    """The look's alert: what the day has done first -- a stop, a target -- then each entry its close would make
    at the last price, named a candidate, with the stop and the target it would take."""
    lines = [F_HEAD.format(d=ddmm(day_now), h=hours)]
    for symbol, side, price in stopped:
        lines.append(F_STOP.format(sym=name(symbol), side=SIDE[side], px=px(price)))
    for o in scaled:
        lines.append(F_SCALE.format(sym=name(o["symbol"]), side=SIDE[side_of(o)], px=px(o["scale_px"])))
    for o, last, level in entries:
        line = F_ENTRY.format(side=SIDE[side_of(o)], sym=name(o["symbol"]), last=px(last))
        lines.append(line if level is None else line + F_LEVEL.format(level=px(level)))
        lines.append(F_ENTRY_PLAN.format(stop=px(o["stop"]), target=px(o["target"])))
    if entries:
        lines.append(F_FOOT)
    return "\n".join(lines)


def log_dir():
    """The day logs of the checkout this vps/ directory sits in (ANALYST-INSTRUCTIONS.md section 12)."""
    return os.path.join(os.path.dirname(common.index_html_path()), "analyst", "log")


def card_lines(path):
    """Every CARD| line of the day logs under path (TZ-84), each a card, in the order of their freezes, stems and
    ranks: (cards, skipped), a line that does not read as a card -- its fields, its side, its kind, three prices
    standing as a card's must -- counted and left out."""
    try:
        names = sorted(n for n in os.listdir(path) if n.endswith(".md") and not n.endswith(".hunt.md"))
    except FileNotFoundError:
        return [], 0
    cards, skipped = [], 0
    for name in names:
        with open(os.path.join(path, name), encoding="utf-8") as fh:
            for line in fh:
                if not line.startswith("CARD|"):
                    continue
                f = line.rstrip("\n").split("|")
                try:
                    if len(f) != CARD_FIELDS or f[6] not in ("long", "short") or f[7] not in CARD_KINDS:
                        raise ValueError("not a card")
                    side = 1 if f[6] == "long" else -1
                    anchor, stop, target = float(f[9]), float(f[10]), float(f[11])
                    if not all(math.isfinite(v) and v > 0 for v in (anchor, stop, target)) \
                            or side * (anchor - stop) <= 0 or side * (target - anchor) <= 0:
                        raise ValueError("not a card's prices")
                    freeze = int(datetime.strptime(f[2], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                                 .timestamp() * 1000)
                    cards.append(dict(stem=f[1], freeze=freeze, rank=int(f[3]), symbol=f[5], side=side, kind=f[7],
                                      anchor=anchor, stop=stop, target=target))
                except (ValueError, IndexError):
                    skipped += 1
    cards.sort(key=lambda c: (c["freeze"], c["stem"], c["rank"]))
    return cards, skipped


def delivered(stem, logs=None):
    """The moment the answer of day log <stem> reached main, in ms (TZ-85): the committer time of the commit that
    added analyst/log/<stem>.md -- the earliest, should the path have been added twice -- read with git in the
    checkout the logs sit in, a clone another user owns (install.sh's own_git). Raises where git names none."""
    checkout = os.path.dirname(os.path.dirname(os.path.abspath(logs or log_dir())))
    proc = subprocess.run(["git", "-c", "safe.directory=" + checkout, "-C", checkout, "log", "--diff-filter=A",
                           "--format=%ct", "--", "analyst/log/%s.md" % stem],
                          capture_output=True, text=True, timeout=GIT_TIMEOUT_S)
    stamps = proc.stdout.split()
    if proc.returncode != 0 or not stamps or not all(s.isdigit() for s in stamps):
        raise ValueError("the day log has no commit")
    return int(stamps[-1]) * 1000


def refused(exc):
    """Whether an error is the exchange limiting or banning this address (TZ-85)."""
    return isinstance(exc, urllib.error.HTTPError) and exc.code in REFUSED_CODES


class Refused(Exception):
    """The exchange refused this address: the card pass asks no more today (TZ-85)."""


def read_done(path):
    """The (stem, rank) of every card resolved for good (TZ-85); a file that is not the card its name says raises,
    as read_ledger()."""
    try:
        names = sorted(name for name in os.listdir(path) if name.endswith(".json") and not name.startswith("."))
    except FileNotFoundError:
        return set()
    out = set()
    for name in names:
        with open(os.path.join(path, name), encoding="utf-8") as fh:
            row = json.load(fh)
        if not isinstance(row, dict) or any(key not in row for key in DONE_KEYS) \
                or "%s-%d.json" % (row["stem"], row["rank"]) != name:
            raise ValueError("a card's done file is not a card")
        out.add((row["stem"], row["rank"]))
    return out


def card_minutes(symbol, after):
    """The one-minute bars of the UTC day of `after` from the minute after its minute to the day's last minute,
    (t, open, high, low, close) oldest first (TZ-84; TZ-85 reads them from the moment the answer reached main);
    refused unless they run from the first to the last."""
    start = after - after % MINUTE_MS + MINUTE_MS
    end = after - after % book.DAY_MS + book.DAY_MS - MINUTE_MS
    if start > end:
        return []
    rows = json.loads(book._get(MINUTES_URL % (symbol, start, end)))
    out = [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4])) for r in rows]
    if not out or out[0][0] != start or out[-1][0] != end:
        raise ValueError("the minutes do not cover the freeze day")
    return out


def card_trade(card, bars, minutes, plan, sent):
    """The trade one card makes (TZ-84) on its symbol's closed daily bars, the minutes of its freeze day after the
    minute its answer reached main, `sent` (TZ-85), and the plan's replay of those bars, (trades, position) of
    book.replay at SCALE_R: ("waiting", None) while the freeze day has not closed, ("lapsed", None) where the card
    made no trade the owner could take, else ("open", position) or ("closed", trade). No card fills before the
    owner read it: a `now` card at the first minute's open after `sent`, unless that price stands past its void
    price -- `STOP_ATR / 2` atr20 inside its stop, its «не выше / не ниже» line, atr20 the book's on the days before
    the freeze day -- or at or past its target; a `limit` card at its limit on the first of those minutes that
    reaches it before the next recalculation, the day's end, or at that minute's open where it opened beyond, unless
    that fill stands at or past its stop; a `wait` card is the plan's own entry on its side at the next open, which
    the book makes only where the freeze day closed beyond the trigger, unless that open came before `sent`. An
    answer that reached main after its freeze day ended fills no `now` or `limit` card. A `now` or `limit` card's
    fill day is the part after its fill -- the later minutes' high and low, the fill minute's side toward the
    stop, the day's close -- and from it the card is followed by book.manage(): its stop on a touch, half at its
    target and the rest's stop at its entry, the rest by the channel; an event of the fill day is stamped no
    earlier than the fill."""
    day0 = card["freeze"] - card["freeze"] % book.DAY_MS
    if not bars or bars[-1][0] < day0:
        return "waiting", None
    k = next((i for i, b in enumerate(bars) if b[0] == day0), None)
    if k is None:
        raise ValueError("the freeze day is not a bar of the read")
    side = card["side"]
    if card["kind"] == "wait":
        trades, pos = plan
        for tr in trades + ([pos] if pos is not None else []):
            if tr["t_entry"] == day0 + book.DAY_MS and tr["side"] == side:
                if tr["t_entry"] < sent:
                    return "lapsed", None
                return ("open", tr) if "t_exit" not in tr else ("closed", tr)
        return "lapsed", None
    if sent >= day0 + book.DAY_MS - MINUTE_MS or not minutes:
        return "lapsed", None
    if card["kind"] == "now":
        a = book.atr(bars, k - 1) if k > 0 else None
        if not a:
            raise ValueError("no atr20 on the days before the freeze day")
        fill, t_fill, later, toward = minutes[0][1], minutes[0][0], minutes, None
        void = card["stop"] + side * book.STOP_ATR / 2 * a
        if side * (fill - void) < 0 or side * (card["target"] - fill) <= 0:
            return "lapsed", None
    else:
        j = next((i for i, m in enumerate(minutes)
                  if (side < 0 and m[2] >= card["anchor"]) or (side > 0 and m[3] <= card["anchor"])), None)
        if j is None:
            return "lapsed", None
        m = minutes[j]
        fill = max(m[1], card["anchor"]) if side < 0 else min(m[1], card["anchor"])
        if side * (fill - card["stop"]) <= 0:
            return "lapsed", None
        t_fill, later, toward = m[0], minutes[j + 1:], m[2] if side < 0 else m[3]
    highs = [b[2] for b in later] + ([toward] if toward is not None and side < 0 else []) + [fill]
    lows = [b[3] for b in later] + ([toward] if toward is not None and side > 0 else []) + [fill]
    path = bars[:k] + [(bars[k][0], fill, max(highs), min(lows), bars[k][4])] + bars[k + 1:]
    pos = dict(side=side, entry=fill, stop=card["stop"], target=card["target"], t_entry=t_fill, k_entry=k)
    done = None
    while pos is not None and k < len(path):
        done, pos, _ = book.manage(pos, path, k)
        k += 1
    tr = done if done is not None else pos
    for key in ("t_exit", "t_scale"):
        if key in tr:
            tr[key] = max(tr[key], t_fill)
    return ("closed", tr) if done is not None else ("open", tr)


def card_funding(symbol, t_entry, t_exit):
    """A card's funding prints (TZ-84): funding_prints() from the start of its fill day, at least FUNDING_GAP_MS
    long, so that a card filled and closed between two settlements asks for a span that holds one; result_r()
    counts the prints after the fill alone."""
    lo = t_entry - t_entry % book.DAY_MS
    return funding_prints(symbol, lo, max(t_exit, lo + FUNDING_GAP_MS))


def card_name(row):
    """The file a closed card trade is written to: its symbol, its side and the stamp of its fill."""
    return "%s-%s-%d.json" % (row["symbol"], "long" if row["side"] > 0 else "short", row["t_entry"])


def read_cards(path):
    """Every trade of the card ledger, in the order of the file names; a file that is not the trade its name says
    raises, as read_ledger()."""
    try:
        names = sorted(name for name in os.listdir(path) if name.endswith(".json") and not name.startswith("."))
    except FileNotFoundError:
        return []
    rows = []
    for name in names:
        with open(os.path.join(path, name), encoding="utf-8") as fh:
            row = json.load(fh)
        if not isinstance(row, dict) or any(key not in row for key in CARD_KEYS) or card_name(row) != name:
            raise ValueError("a card ledger file is not a trade")
        rows.append(row)
    return rows


def cards_pass(path, ledger, cards, now_ms, seen, symbols):
    """The card ledger's run (TZ-84): every card followed on one read of its symbol, the earliest card of a coin,
    side and fill making its one trade, each new close written as a new file (inv. 38) once its funding prints
    arrive whole. A card resolved for good -- a closed trade of its own, or a file under CARDS_DONE beside `path`
    -- is never read again, and a card that made no trade, or whose trade stands closed under an earlier card,
    is written there once (TZ-85); a symbol whose every card is resolved is not read. An answer of the exchange
    limiting or banning this address ends the pass: no further request, the cards not reached unread.
    (the ledger's trades, the record's block)."""
    done_path = os.path.join(os.path.dirname(path), CARDS_DONE)
    done = read_done(done_path) | {(row["stem"], row["rank"]) for row in ledger}
    known = {(row["symbol"], row["side"], row["t_entry"]) for row in ledger}
    counts = dict(read=len(cards), done=0, waiting=0, lapsed=0, pending=0, unread=0)
    added, opened, finished, taken, sent_at, stopped = [], [], [], set(), {}, None

    def finish(card, why):
        finished.append({"stem": card["stem"], "rank": card["rank"], "symbol": card["symbol"],
                         "side": card["side"], "kind": card["kind"], "why": why, "seen": seen})

    for symbol in sorted({c["symbol"] for c in cards}):
        group = [c for c in cards if c["symbol"] == symbol and (c["stem"], c["rank"]) not in done]
        counts["done"] += sum(1 for c in cards if c["symbol"] == symbol) - len(group)
        if not group:
            continue
        if stopped is not None:
            counts["unread"] += len(group)
            continue
        try:
            bars, open_now = book.live_bars(symbol, now_ms)
        except Exception as exc:          # one symbol's failure never hides the others
            stopped = exc.code if refused(exc) else None
            counts["unread"] += len(group)
            continue
        plan = book.replay(bars, open_now, book.SCALE_R)
        for card in group:
            if stopped is not None:
                counts["unread"] += 1
                continue
            try:
                day0 = card["freeze"] - card["freeze"] % book.DAY_MS
                closed_day = bool(bars) and bars[-1][0] >= day0
                sent = card["freeze"]
                if closed_day:
                    if card["stem"] not in sent_at:
                        sent_at[card["stem"]] = delivered(card["stem"])
                    sent = max(sent_at[card["stem"]], card["freeze"])
                minutes = (card_minutes(symbol, sent) if closed_day and card["kind"] != "wait"
                           and sent < day0 + book.DAY_MS - MINUTE_MS else [])
                status, tr = card_trade(card, bars, minutes, plan, sent)
            except Exception as exc:      # asked again tomorrow
                if refused(exc):
                    stopped = exc.code
                    counts["unread"] += 1
                    continue
                counts["pending"] += 1
                common.log("score: pending %s %s %s" % (CARDS, symbol, exc.__class__.__name__))
                continue
            if status in ("waiting", "lapsed"):
                counts[status] += 1
                if status == "lapsed":
                    finish(card, "lapsed")
                continue
            key = (symbol, card["side"], tr["t_entry"])
            if key in known:
                if status == "closed":
                    finish(card, "same")
                continue
            if key in taken:
                continue
            taken.add(key)
            if status == "open":
                opened.append({"symbol": symbol, "side": card["side"], "kind": card["kind"], "stem": card["stem"],
                               "rank": card["rank"], "t_entry": tr["t_entry"], "entry": tr["entry"],
                               "stop": tr["stop"], "target": tr.get("target"), "scaled": "t_scale" in tr,
                               "exit_due": bool(tr.get("exit_due"))})
                continue
            try:
                r = book.result_r(tr, card_funding(symbol, tr["t_entry"], tr["t_exit"]))
                if not math.isfinite(r):
                    raise ValueError("the result is not finite")
            except Exception as exc:      # not written: the next run asks for the prints again (inv. 70)
                if refused(exc):
                    stopped = exc.code
                    counts["unread"] += 1
                    continue
                counts["pending"] += 1
                common.log("score: pending %s %s %s" % (CARDS, symbol, exc.__class__.__name__))
                continue
            known.add(key)
            added.append({"symbol": symbol, "side": tr["side"], "kind": card["kind"], "stem": card["stem"],
                          "rank": card["rank"], "t_entry": tr["t_entry"], "entry": tr["entry"], "stop": tr["stop"],
                          "target": tr.get("target"), "t_exit": tr["t_exit"], "exit": tr["exit"], "why": tr["why"],
                          "r": r, "seen": seen})
    if stopped is not None:
        common.log("score: cards refused %d" % stopped)
    if added:
        os.makedirs(path, mode=0o750, exist_ok=True)
        for row in added:                 # a new file each: nothing that stands is opened (inv. 38)
            common.atomic_write(os.path.join(path, card_name(row)), row, mode=0o640)
    if finished:
        os.makedirs(done_path, mode=0o750, exist_ok=True)
        for row in finished:              # the same: a card's file is written once
            name = os.path.join(done_path, "%s-%d.json" % (row["stem"], row["rank"]))
            if not os.path.exists(name):
                common.atomic_write(name, row, mode=0o640)
    rows = ledger + added
    on_list = set(symbols)
    return rows, dict(counts, added=len(added), finished=len(finished), refused=stopped, closed=totals(rows),
                      list=totals([row for row in rows if row["symbol"] in on_list]),
                      outside=totals([row for row in rows if row["symbol"] not in on_list]), open=opened)


def record_of(state_dir):
    """The daily close's last record, or None where there is none or it does not parse."""
    try:
        with open(os.path.join(state_dir, RECORD), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def holds(prev, ceilings):
    """Whether the last record holds a book under these ceilings (TZ-81): its v is 3 and its ceilings are these."""
    return isinstance(prev, dict) and prev.get("v") == 3 and prev.get("ceilings") == ceilings


def book_held(books, symbols, unread, ceilings, prev):
    """The book held (TZ-81): the spans book.hold() takes of the plan's, entered since GO_LIVE. Where the last
    record holds a book under these ceilings, what it decided stands -- each entry up to the open it told is taken
    if that record took it and left out if not -- and the spans it held on a symbol unread today stand as it
    recorded them."""
    fixed, carried = None, []
    if holds(prev, ceilings):
        told = day_ms(prev["asof"]) + book.DAY_MS
        carried = [(s, side, t, None if free is None else tuple(free)) for s, side, t, free in prev["held"]
                   if s in unread]
        took = {(s, t) for s, _, t, _ in prev["held"]}
        fixed = {(s, t): (s, t) in took for s, _, t, _ in books + carried if t <= told}
    taken = book.hold(books + carried, book.rank(symbols), *ceilings, fixed)
    return [sp for sp in books + carried if (sp[0], sp[2]) in taken]


def look_of(state_dir, day_iso):
    """The look's record of a day as (the entries it named, as (symbol, side) pairs), or None where the day was
    not looked at or its file is not a look."""
    try:
        with open(os.path.join(state_dir, FORMING, day_iso + ".json"), encoding="utf-8") as fh:
            doc = json.load(fh)
        if doc["v"] != 2 or doc["day"] != day_iso:
            return None
        return {(str(e["symbol"]), int(e["side"])) for e in doc["entries"]}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


def forming(args, now_ms):
    """The look at the day still forming: one read of each symbol, the plan's state at the last close and its
    state if the day closed at the last price. Told as it is: a stop the day has reached, a target it has
    reached -- neither can be taken back. Told as a candidate: the entry a close at the last price would make.
    An exit that close would make is not told: nothing is done about it before the close, which tells it. Only
    the book held is told (TZ-81): a stop or a target of a position it holds, and a candidate it would take at
    the next open. One look a UTC day; the alert is written before the record, so that a look that died between
    them is made again."""
    day_now = day(now_ms)
    path = os.path.join(args.state, FORMING, day_now + ".json")
    if os.path.exists(path):
        common.log("score: forming day=%s already looked at, nothing written" % day_now)
        return 0
    own = paper.owner_now()
    if own is None:
        common.log("score: forming day=%s the owner's ceilings are unread, nothing written" % day_now)
        return 6
    symbols, go = list_symbols(), day_ms(GO_LIVE)
    read, books, unread = [], [], []
    for symbol in symbols:
        try:
            bars, today = book.live_day(symbol, now_ms)
            if day(today[0]) != day_now:
                raise ValueError("the day still forming is not today")
            now = book.state_of(symbol, bars, today[1], book.SCALE_R)[0]
            then, trades, pos = book.state_of(symbol, bars + [today], today[4], book.SCALE_R)
        except Exception:                 # one symbol's failure never hides the others
            unread.append(symbol)
            continue
        read.append((symbol, today, now, then, trades, pos))
        books += [sp for sp in book.spans(symbol, trades, pos, today[0] + book.DAY_MS) if sp[2] >= go]
    if len(unread) == len(symbols):
        common.log("score: forming day=%s symbols=%d read=0 nothing written" % (day_now, len(symbols)))
        return 4
    taken = {(s, t) for s, _, t, _ in book_held(books, symbols, unread, list(paper.ceilings(own)),
                                                record_of(args.state))}
    stopped, scaled, entries = [], [], []
    for symbol, today, now, then, trades, pos in read:
        stopped += [(symbol, tr["side"], tr["exit"]) for tr in trades
                    if tr["t_exit"] == today[0] and tr["why"] == "stop" and (symbol, tr["t_entry"]) in taken]
        if then["state"] not in ("long", "short") or (symbol, pos["t_entry"]) not in taken:
            continue
        if then.get("scale_date") == day_now:
            scaled.append(then)
        if then["entry_due"]:         # the level the close must cross is the last close's trigger
            entries.append((then, today[4], now.get("long_trigger" if side_of(then) > 0 else "short_trigger")))
    stopped.sort(key=lambda item: item[0] not in MAJORS)
    scaled = majors_first(scaled)
    entries.sort(key=lambda item: item[0]["symbol"] not in MAJORS)
    alert = bool(stopped or scaled or entries)
    if alert:
        hours = max(1, int(round((book.DAY_MS - now_ms % book.DAY_MS) / 3600000.0)))
        common.write_outbox("alert", compose_look(day_now, hours, stopped, scaled, entries),
                            outbox_dir=args.outbox)
    os.makedirs(os.path.dirname(path), mode=0o750, exist_ok=True)
    common.atomic_write(path, {
        "v": 2, "k": "score-forming", "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000)),
        "day": day_now, "symbols": len(symbols), "unread": sorted(unread),
        "stopped": [symbol for symbol, _, _ in stopped], "scaled": [o["symbol"] for o in scaled],
        "entries": [{"symbol": o["symbol"], "side": side_of(o)} for o, _, _ in entries]}, mode=0o640)
    common.log("score: forming day=%s symbols=%d read=%d unread=%d stopped=%d scaled=%d entries=%d alert=%s"
               % (day_now, len(symbols), len(symbols) - len(unread), len(unread), len(stopped), len(scaled),
                  len(entries), "yes" if alert else "no"))
    return 0


def ledger_pass(path, ledger, live, asof, seen, priced=None):
    """One ledger's run: (added, pending, late, disagree). live is (state, trades) per symbol read today; a trade
    is written as the module's docstring says, each a new file (inv. 38). priced, shared by the ledgers of one
    replay, keeps each trade's R so that a trade two of them write is priced once (TZ-81)."""
    known = {(row["symbol"], row["t_entry"]): row for row in ledger}
    floor = GO_LIVE if not ledger else (date.fromisoformat(asof) - timedelta(days=RETRY_DAYS)).isoformat()
    added, pending, late, disagree = [], 0, 0, 0
    for state, trades in live:
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
                r = (priced or {}).get(key)
                if r is None:
                    r = book.result_r(tr, funding_prints(state["symbol"], tr["t_entry"], tr["t_exit"]))
                if not math.isfinite(r):
                    raise ValueError("the result is not finite")
            except Exception as exc:      # not written: the next run asks for the prints again (inv. 70)
                pending += 1
                common.log("score: pending %s %s %s" % (os.path.basename(path), state["symbol"], exc.__class__.__name__))
                continue
            if priced is not None:
                priced[key] = r
            known[key] = {"symbol": state["symbol"], "side": tr["side"], "t_entry": tr["t_entry"],
                          "entry": tr["entry"], "stop": tr["stop"], "t_exit": tr["t_exit"], "exit": tr["exit"],
                          "why": tr["why"], "r": r, "seen": seen}
            added.append(known[key])
    if added:
        os.makedirs(path, mode=0o750, exist_ok=True)
        for row in added:                 # a new file each: nothing that stands is opened (inv. 38)
            common.atomic_write(os.path.join(path, row_name(row)), row, mode=0o640)
    return added, pending, late, disagree


def main(argv=None, now_ms=None):
    parser = argparse.ArgumentParser(description="the trend book's daily signal and forward ledger")
    parser.add_argument("--state", default=common.STATE_DIR)
    parser.add_argument("--outbox", default=None, help="where the alert is written; the bot's outbox by default")
    parser.add_argument("--forming", action="store_true", help="the look at the day still forming")
    args = parser.parse_args(argv)
    now_ms = int(time.time() * 1000) if now_ms is None else now_ms
    if args.forming:
        return forming(args, now_ms)
    own = paper.owner_now()
    if own is None:
        common.log("score: the owner's ceilings are unread, nothing written")
        return 6
    ceilings = list(paper.ceilings(own))
    rule_path, plan_path = os.path.join(args.state, LEDGER), os.path.join(args.state, PLAN)
    held_path, record_path = os.path.join(args.state, HELD), os.path.join(args.state, RECORD)
    cards_path = os.path.join(args.state, CARDS)
    try:
        rule_ledger, plan_ledger, held_ledger = read_ledger(rule_path), read_ledger(plan_path), read_ledger(held_path)
        card_ledger = read_cards(cards_path)
    except (OSError, ValueError, TypeError):
        common.log("score: a file of the ledger is not a trade, nothing written")
        return 5
    prev = record_of(args.state)
    try:
        prev_asof, prev_ts = str(prev["asof"]), str(prev["ts"])
    except (KeyError, TypeError, AttributeError):
        prev = prev_asof = prev_ts = None
    # A record before TZ-81's (v 3) held no book, and one under other ceilings held another: the first run after
    # it is the book's baseline, and tells no close.
    baseline = not holds(prev, ceilings)

    symbols = list_symbols()
    read, unread = [], []
    for symbol in symbols:
        try:
            bars, open_now = book.live_bars(symbol, now_ms)
            read.append((book.state_of(symbol, bars, open_now), book.state_of(symbol, bars, open_now, book.SCALE_R)))
        except Exception:                 # one symbol's failure never hides the others
            unread.append(symbol)
    asof = max((rule[0]["asof"] for rule, _ in read if "asof" in rule[0]), default=None)
    if asof is None or (prev_asof is not None and asof < prev_asof):
        common.log("score: asof=%s symbols=%d read=%d nothing written" % (asof or "-", len(symbols), len(read)))
        return 4
    # A symbol whose last closed day is not the day the others stand on is not read today.
    unread += [rule[0]["symbol"] for rule, _ in read if rule[0].get("asof", asof) != asof]
    live = [item for item in read if item[0][0].get("asof", asof) == asof]
    fresh = baseline or asof > prev_asof
    seen = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now_ms / 1000))

    go, t_next = day_ms(GO_LIVE), day_ms(asof) + book.DAY_MS
    held = book_held([sp for _, plan in live for sp in book.spans(plan[0]["symbol"], plan[1], plan[2], t_next)
                      if sp[2] >= go], symbols, unread, ceilings, prev)
    taken = {(s, t) for s, _, t, _ in held}
    priced = {}
    rule_added, rule_pending, rule_late, rule_disagree = ledger_pass(
        rule_path, rule_ledger, [(rule[0], rule[1]) for rule, _ in live], asof, seen)
    plan_added, plan_pending, plan_late, plan_disagree = ledger_pass(
        plan_path, plan_ledger, [(plan[0], plan[1]) for _, plan in live], asof, seen, priced)
    added, pending, late, disagree = ledger_pass(
        held_path, held_ledger, [(plan[0], [tr for tr in plan[1] if (plan[0]["symbol"], tr["t_entry"]) in taken])
                                 for _, plan in live], asof, seen, priced)
    rule_rows, plan_rows, rows = rule_ledger + rule_added, plan_ledger + plan_added, held_ledger + added

    plan_open = [plan for _, plan in live if plan[0]["state"] in ("long", "short")]
    open_rows = [plan[0] for plan in plan_open if (plan[0]["symbol"], plan[2]["t_entry"]) in taken]
    outside = [plan[0] for plan in plan_open if (plan[0]["symbol"], plan[2]["t_entry"]) not in taken]
    if baseline:
        opened = [o for o in open_rows if o["entry_due"] or (prev_asof is not None and o["entry_date"] > prev_asof)]
        skipped = list(outside)
    else:
        after = (date.fromisoformat(prev_asof) + timedelta(days=1)).isoformat()
        opened = [o for o in open_rows if fresh and o["entry_date"] > after]
        skipped = [o for o in outside if fresh and o["entry_date"] > after]
    scaled = [] if baseline else [o for o in open_rows if fresh and o.get("scale_date", "") > prev_asof]
    closing = [o for o in open_rows if fresh and o["exit_due"]]
    # A closed trade is told once: the rows written since the record this run replaces.
    closed = [] if baseline else [row for row in rows if row["seen"] > prev_ts]
    alert = baseline or bool(opened or skipped or scaled or closing or closed)
    # What the look at the day that has just closed named, against the entries that close made.
    named = look_of(args.state, asof)
    due = {(o["symbol"], side_of(o)) for o in open_rows if o["entry_due"]}
    look = None if named is None else {"named": len(named), "hit": len(named & due), "entries": len(due)}
    if alert:
        common.write_outbox("alert", compose(asof, baseline, opened, skipped, scaled, closing, closed, rows,
                                             open_rows, own), outbox_dir=args.outbox)

    try:
        cards, unparsed = card_lines(log_dir())
        card_rows, card_block = cards_pass(cards_path, card_ledger, cards, now_ms, seen, symbols)
        card_block["skipped"] = unparsed
    except Exception as exc:              # the card ledger never stops the book's
        common.log("score: cards unread %s" % exc.__class__.__name__)
        card_rows, card_block = card_ledger, None

    def by_group(group):
        return {"all": totals(group), "majors": totals([row for row in group if row["symbol"] in MAJORS]),
                "others": totals([row for row in group if row["symbol"] not in MAJORS])}
    common.atomic_write(record_path, {
        "v": 3, "k": "score", "ts": seen, "asof": asof, "since": GO_LIVE, "symbols": len(symbols),
        "unread": sorted(unread), "ceilings": ceilings,
        "held": sorted([s, side, t, None if free is None else list(free)] for s, side, t, free in held),
        "open": [{key: o.get(key) for key in ("symbol", "state", "entry_date", "entry", "stop", "target", "exit_level",
                                              "r_open", "entry_due", "exit_due", "scale_date", "stop_now")}
                 for o in open_rows],
        "outside": [{key: o.get(key) for key in ("symbol", "state", "entry_date")} for o in majors_first(outside)],
        "closed": by_group(rows), "pending": pending, "late": late, "disagree": disagree, "look": look,
        "plan": {"open": len(plan_open), "closed": by_group(plan_rows), "pending": plan_pending, "late": plan_late,
                 "disagree": plan_disagree},
        "rule": {"open": sum(1 for rule, _ in live if rule[0]["state"] in ("long", "short")), "closed": by_group(rule_rows),
                 "pending": rule_pending, "late": rule_late, "disagree": rule_disagree},
        "cards": card_block}, mode=0o640)
    common.log("score: asof=%s symbols=%d read=%d unread=%d open=%d outside=%d opened=%d skipped=%d scaled=%d "
               "closing=%d closed=%d pending=%d late=%d disagree=%d ledger=%d plan=%d rule=%d look=%s alert=%s "
               "cards=%s"
               % (asof, len(symbols), len(symbols) - len(unread), len(unread), len(open_rows), len(outside),
                  len(opened), len(skipped), len(scaled), len(closing), len(closed), pending, late, disagree,
                  len(rows), len(plan_rows), len(rule_rows),
                  "-" if look is None else "%d/%d/%d" % (look["hit"], look["named"], look["entries"]),
                  "yes" if alert else "no",
                  "-" if card_block is None else "%d/%d/%d" % (len(card_rows), len(card_block["open"]),
                                                               card_block["pending"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
