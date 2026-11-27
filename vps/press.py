#!/usr/bin/env python3
"""The press (TZ-87): every number an analysis run prints, computed in code before the model starts, and the
mechanical checks its answer passes before it leaves -- map section 10, rows "A run rewrites its own programs",
"The run spends its account on reading" and "The gate's hundred trades are out of reach of the presses".

    press.py [--tree DIR] [--now ISO]       the press: analyst/press/<stem>.json, the record, and <stem>.md, the
                                            brief the trader reads; one line on stdout
    press.py brief [--tree DIR]             the brief of the press younger than FRESH_S, pressing first where
                                            there is none
    press.py final [--tree DIR] STEM        the cards ranked on stdin, sized: money lines, CARD lines, tickets
    press.py hunter [--tree DIR] STEM       the hunter's prompt lines of this press (methodology section 15)
    press.py state [--tree DIR] STEM [--write]
                                            analyst/state.json as the trader needs it: --write applies the
                                            lifecycle and writes oi and regime (section 11); without, its view
    press.py scale [--tree DIR] STEM ITEM...
                                            per ITEM -- SYMBOL[@ISO][:YYYY-MM-DD,...] -- a verdict's measured
                                            range and the move since a publication
    press.py check [--tree DIR] STEM LOG    the day log's answer and its scoring lines, checked mechanically;
                                            exit 0 every check passed (ANSWER LOG, two files, also reads)

Every rule is the methodology's (ANALYST-INSTRUCTIONS.md sections 2-5 and 16) or production's: the functions
marketRegime, sigmaDay, lStruct and liqPrice and their constants are cut by NAME from the tree's index.html and run
under node, never copied (inv. 21, 38); the book is vps/book.py. A lane that fails is unread in the record and never
stops the press. Python 3.12's standard library and the host's node. Time is UTC everywhere. No credential is read.
Exit 0 written or passed - 1 a check failed - 2 a wrong argument - 4 the payload unread: nothing written.
"""
import argparse
import concurrent.futures
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book  # noqa: E402
import common  # noqa: E402
import radar  # noqa: E402

PRESS_DIR = "analyst/press"
SCORE_JSON = common.STATE_DIR + "/score.json"
SCORE_HELD = common.STATE_DIR + "/score-held"
ETF_JSON = common.STATE_DIR + "/etf.json"
FAPI = "https://fapi.binance.com"
TBILISI = timezone(timedelta(hours=4))
DAY_MS = book.DAY_MS
HOUR_MS = 3_600_000
PRESS_S = 420                 # the press's own budget inside the run unit; a lane past it is unread
FRESH_S = 900                 # methodology section 5: the gate holds the payload within fifteen minutes
WORKERS = 8
HTTP_S = common.HTTP_TIMEOUT_S
HOLD_CODES = (403, 418, 429, 451)      # methodology section 16: a refusal ends that endpoint's reads

# Methodology section 3, filters 1, 2 and 4.
TURNOVER_MIN = 10_000_000
CG_URL = ("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc"
          "&per_page=100&page=1")
CG_ROWS = 100
CG_PREFIXES = ("1000000", "10000", "1000", "1M")
# Methodology section 15's hunter prompt.
MOVERS = 3
FORWARD_MAX = 3
# Methodology section 16, the positioning read.
POS_LIMIT, POS_K, POS_MIN, POS_DAY, POS_FUND_D, FUND_LOOKBACK_D = 180, 42, 84, 6, 14, 30
# Methodology section 4: the BTC map, the verdict's scale and the market verdict.
MAP_LIMIT, MAP_W, CORRIDOR_H = 181, 42, 48
SCALE_DAYS, CLASS_DAYS, CLASS_MIN = 30, 365, 4
FUNDING_HOT = 0.0001           # 0.01 %
QQQ_BAND = 1.0                 # per cent
WORLD = ("BZUSDT", "XAUUSDT", "QQQUSDT", "SPYUSDT")
# Methodology section 2, the score record.
SCORE_DAYS = 7
# Methodology section 16 step D: the ETF record stands within these ages; a US session closed twelve hours or
# more before the freeze and missing from it is searched for (a session closes 21:00 UTC at the latest).
ETF_TS_H, ETF_DATE_D, ETF_CAUGHT_H, US_CLOSE_H = 2, 4, 12, 21
ETF_TYPES = (("BTC", "us-btc-spot"), ("ETH", "us-eth-spot"), ("SOL", "us-sol-spot"))
# Methodology section 16 step E.
DERIV_URLS = {
    "binance_oi": FAPI + "/fapi/v1/openInterest?symbol=BTCUSDT",
    "binance_hist": FAPI + "/futures/data/openInterestHist?symbol=BTCUSDT&period=1h&limit=25",
    "binance_taker": FAPI + "/futures/data/takerlongshortRatio?symbol=BTCUSDT&period=1h&limit=24",
    "bybit_ticker": "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT",
    "bybit_hist": "https://api.bybit.com/v5/market/open-interest?category=linear&symbol=BTCUSDT&intervalTime=1h&limit=25",
    "okx_oi": "https://www.okx.com/api/v5/public/open-interest?instType=SWAP&instId=BTC-USDT-SWAP",
    "okx_funding": "https://www.okx.com/api/v5/public/funding-rate?instId=BTC-USDT-SWAP",
    "okx_hist": "https://www.okx.com/api/v5/rubik/stat/contracts/open-interest-volume?ccy=BTC&period=1H",
    "okx_taker": "https://www.okx.com/api/v5/rubik/stat/taker-volume?ccy=BTC&instType=CONTRACTS&period=1H",
}
OKX_LIQ = "https://www.okx.com/api/v5/public/liquidation-orders?instType=SWAP&uly=BTC-USDT&state=filled&limit=100"
OKX_CT = 0.01                  # BTC per BTC-USDT-SWAP contract (step E)
LIQ_PAGES = 60
JS_VARS = ("EFF_TREND", "REG_STRESS_Z", "H_NOISE", "VOL_HARD", "ENTRY_CHASE_SD", "RISK_Z", "H_REACT", "LIQ_MMR",
           "L_CAP", "L_MIN", "VOL_STOP", "FEE_TAKER")
JS_FUNCS = ("has", "marketRegime", "sigmaDay", "lStruct", "liqPrice")

MINUS, NBSP, BREAK = "\u2212", "\u00a0", "\u2063"
WEEKDAYS = ("\u043f\u043d", "\u0432\u0442", "\u0441\u0440", "\u0447\u0442", "\u043f\u0442", "\u0441\u0431", "\u0432\u0441")
SIDE_RU = {1: "\u043b\u043e\u043d\u0433", -1: "\u0448\u043e\u0440\u0442"}
DOT = {1: "\U0001f7e2", -1: "\U0001f534"}
COLOUR = {"red": "\U0001f534", "white": "\u26aa", "green": "\U0001f7e2", "unread": "\u26aa"}
REGIME_RU = {"up": "\u0440\u043e\u0441\u0442", "down": "\u043f\u0430\u0434\u0435\u043d\u0438\u0435", "range": "\u0431\u043e\u043a\u043e\u0432\u0438\u043a", "hot": "\u043f\u0435\u0440\u0435\u0433\u0440\u0435\u0432",
             "stress": "\u0441\u0442\u0440\u0435\u0441\u0441 \u2014 \u0440\u0435\u0437\u043a\u043e\u0435 \u0434\u0432\u0438\u0436\u0435\u043d\u0438\u0435"}
VERDICT_RU = {"bear": "\u041c\u0415\u0414\u0412\u0415\u0416\u0418\u0419", "bull": "\u0411\u042b\u0427\u0418\u0419", "flat": "\u041d\u0415\u0419\u0422\u0420\u0410\u041b\u042c\u041d\u042b\u0419"}
INDICATORS = ("BTC \u0437\u0430 2 \u043d\u0435\u0434\u0435\u043b\u0438", "BTC \u0437\u0430 \u043d\u0435\u0434\u0435\u043b\u044e", "BTC \u0437\u0430 \u0441\u0443\u0442\u043a\u0438", "\u0422\u0440\u0435\u043d\u0434-\u0441\u0438\u0441\u0442\u0435\u043c\u0430", "ETF", "\u0414\u0435\u043d\u044c\u0433\u0438 \u043d\u0430 \u0444\u044c\u044e\u0447\u0435\u0440\u0441\u0430\u0445",
              "Funding", "\u041a\u0440\u0443\u043f\u043d\u044b\u0435 \u0438\u0433\u0440\u043e\u043a\u0438 BTC", "\u0422\u043e\u043b\u043f\u0430 BTC", "\u0410\u043a\u0446\u0438\u0438 \u0421\u0428\u0410")
REFUSAL_RU = {"forming-day": "\u0441\u0442\u043e\u043f \u0443\u0436\u0435 \u0437\u0430\u0434\u0435\u0442", "half-way": "\u0432\u0445\u043e\u0434 \u0443\u0448\u0451\u043b", "liquidation": "\u0432\u043e\u043b\u0430\u0442\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c",
              "large": "\u043a\u0440\u0443\u043f\u043d\u044b\u0435 \u0438\u0433\u0440\u043e\u043a\u0438 \u043f\u0440\u043e\u0442\u0438\u0432"}
CROWD_WARN = {1: "\u0422\u043e\u043b\u043f\u0430 \u0443\u0436\u0435 \u0432 \u043b\u043e\u043d\u0433\u0435", -1: "\u0422\u043e\u043b\u043f\u0430 \u0443\u0436\u0435 \u0432 \u0448\u043e\u0440\u0442\u0435"}
LIQUIDITY_WARN = "\u041c\u0430\u043b\u043e \u043b\u0438\u043a\u0432\u0438\u0434\u043d\u043e\u0441\u0442\u0438"
GATE_SENTENCE = "\u041d\u0443\u0436\u0435\u043d \u0441\u0432\u0435\u0436\u0438\u0439 \u0441\u043d\u0438\u043c\u043e\u043a \u2014 \u0437\u0430\u043f\u0443\u0441\u0442\u0438 LIVE SNAP."
ANSWER_MARK, APPENDIX_MARK = "## Answer as sent", "## Appendix"
BANNED = ("\u0438\u043d\u0442\u0435\u0440\u0435\u0441\u043d\u043e", "\u0441\u0442\u043e\u0438\u0442 \u0441\u043b\u0435\u0434\u0438\u0442\u044c", "\u043f\u043e\u0442\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u0439 \u0441\u0435\u0442\u0430\u043f", "\u043c\u043e\u0436\u0435\u0442 \u0434\u0432\u0438\u043d\u0443\u0442\u044c\u0441\u044f", "\u043f\u043e\u0434\u043e\u0436\u0434\u0451\u043c \u0438 \u043f\u043e\u0441\u043c\u043e\u0442\u0440\u0438\u043c",
          "\u0432\u043e\u0437\u043c\u043e\u0436\u043d\u043e \u0431\u044b\u0447\u0438\u0439")


class Refused(Exception):
    """An endpoint answered with a refusal: no further read of it this press."""


class Net:
    """Every read of the press: one GET, 20 s, no retry; a host's refusal is remembered per endpoint (section 16)."""

    def __init__(self, get=None, deadline=None):
        self._get = get or self._urlopen
        self.deadline = deadline
        self.refused = {}
        self.reads = 0

    @staticmethod
    def _urlopen(url):
        try:
            with urllib.request.urlopen(url, timeout=HTTP_S) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as exc:
            return exc.code, b""

    def json(self, url, key=None):
        key = key or url.split("?")[0]
        if key in self.refused:
            raise Refused(key)
        if self.deadline is not None and time.monotonic() > self.deadline:
            raise TimeoutError("the press's budget is spent")
        self.reads += 1
        status, body = self._get(url)
        if status in HOLD_CODES:
            self.refused[key] = status
            raise Refused("%s %s" % (key, status))
        if status != 200:
            raise ValueError("%s answered %s" % (key, status))
        return json.loads(body)


# ------------------------------------------------------------------ numbers and text

def fnum(value):
    """A finite float or None."""
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def decimals(text):
    """The decimals a price string of the payload carries, its trailing zeros counted."""
    text = str(text)
    return len(text.split(".", 1)[1]) if "." in text else 0


def half_up(value, places=0):
    """value rounded half away from zero at `places` decimals, from its shortest repr: 0.308295 to five places is
    0.30830, as the price reads it, never the binary neighbour's 0.30829."""
    return Decimal(repr(float(value))).quantize(Decimal(1).scaleb(-max(0, places)), rounding=ROUND_HALF_UP)


def px(value, places):
    """A price rounded as the frozen price it belongs to, trailing zeros dropped (methodology section 2)."""
    text = "%.*f" % (max(0, places), half_up(value, places))
    return text.rstrip("0").rstrip(".") if "." in text else text


def group(n):
    """An integer, thousands grouped with U+00A0 from four digits (section 2, Numbers); the minus U+2212."""
    sign = MINUS if n < 0 else ""
    digits = "%d" % abs(n)
    if len(digits) >= 4:
        parts = []
        while digits:
            parts.insert(0, digits[-3:])
            digits = digits[:-3]
        digits = NBSP.join(parts)
    return sign + digits


def num1(value):
    """A signed figure to one decimal, its thousands grouped with U+00A0, the minus U+2212."""
    q = half_up(abs(value), 1)
    whole_part, frac = ("%.1f" % q).split(".")
    return ("+" if value > 0 else MINUS if value < 0 else "") + group(int(whole_part)) + "." + frac


def pct(value, places=1, plus=True):
    """A per-cent figure with its sign, the minus U+2212."""
    text = ("%+.*f" if plus else "%.*f") % (places, value)
    return text.replace("-", MINUS)


def whole(value):
    return int(half_up(value))


def usd(value):
    """A dollar price to the whole unit, grouped (the BTC map)."""
    return group(whole(value))


def quartile(values, q):
    """The value at rank ceil(q m) of the m sorted values (section 16's convention), or None."""
    vals = sorted(values)
    if not vals:
        return None
    return vals[max(1, math.ceil(q * len(vals))) - 1]


def median(values):
    vals = sorted(values)
    if not vals:
        return None
    n = len(vals)
    return vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2


def base_name(symbol):
    return symbol[:-4] if symbol.endswith("USDT") else symbol


def tbilisi(dt):
    return dt.astimezone(TBILISI)


def iso_z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ms_of(dt):
    return int(dt.timestamp() * 1000)


def utc_day(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).date()


# ------------------------------------------------------------------ production, cut by name

def _cut(js, start, opening, closing, stop_at_semicolon):
    """The end of the statement or block opening at `start`: brackets of `opening`/`closing` matched outside strings
    and line comments; with stop_at_semicolon, the first `;` at depth zero ends it, else the bracket closing depth one."""
    depth, j, in_s, in_c, esc = 0, start, None, False, False
    while j < len(js):
        ch = js[j]
        if in_c:
            if ch == "\n":
                in_c = False
        elif in_s:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == in_s:
                in_s = None
        elif ch == "/" and js[j + 1:j + 2] == "/":
            in_c = True
        elif ch in "'\"":
            in_s = ch
        elif ch in opening:
            depth += 1
        elif ch in closing:
            depth -= 1
            if depth == 0 and not stop_at_semicolon:
                return j + 1
        elif ch == ";" and depth == 0 and stop_at_semicolon:
            return j + 1
        j += 1
    raise ValueError("unbalanced source")


def cut_function(js, name):
    """`function NAME(...) {...}` by brace matching; none or several fail (inv. 22)."""
    found = list(re.finditer(r"^function %s\s*\(" % re.escape(name), js, re.M))
    if len(found) != 1:
        raise ValueError("function %s: %d definitions" % (name, len(found)))
    m = found[0]
    return js[m.start():_cut(js, js.index("{", m.end()), "{", "}", False)]


def cut_var(js, name):
    """`var NAME = ...;` to its statement's end; none or several fail."""
    found = list(re.finditer(r"^var %s\s*=" % re.escape(name), js, re.M))
    if len(found) != 1:
        raise ValueError("var %s: %d definitions" % (name, len(found)))
    m = found[0]
    return js[m.start():_cut(js, m.end(), "{[(", "}])", True)]


DRIVER = r"""
var input = JSON.parse(require('fs').readFileSync(0, 'utf8'));
var consts = {};
NAMES.forEach(function (n) { consts[n] = eval(n); });
var out = input.map(function (c) {
    if (c[0] === 'regime') return marketRegime(c[1]);
    if (c[0] === 'sigmaDay') return sigmaDay(c[1]);
    if (c[0] === 'lStruct') return lStruct(c[1], c[2]);
    if (c[0] === 'liqPrice') return liqPrice(c[1], c[2], c[3]);
    return null;
});
process.stdout.write(JSON.stringify({consts: consts, out: out}));
"""


def production(index_html, calls):
    """(constants, results): production's functions and constants cut from index_html and run once under node,
    every call of `calls` -- ['regime', stats] | ['sigmaDay', vol] | ['lStruct', dist, vol] | ['liqPrice', E, L,
    isLong] -- in order (methodology section 4)."""
    parts = [cut_var(index_html, n) for n in JS_VARS] + [cut_function(index_html, n) for n in JS_FUNCS]
    code = "\n".join(parts) + "\nvar NAMES = " + json.dumps(list(JS_VARS)) + ";\n" + DRIVER
    proc = subprocess.run(["node", "-e", code], input=json.dumps(calls), capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError("node exited %d" % proc.returncode)
    doc = json.loads(proc.stdout)
    return doc["consts"], doc["out"]


# ------------------------------------------------------------------ the tree's inputs

def read_payload(tree):
    """(ts, c rows, x rows, decimals by symbol): c the list and BTC, x the whole perpetual book (section 5)."""
    with open(os.path.join(tree, "analyst", "live.json"), encoding="utf-8") as fh:
        doc = json.load(fh)
    places, c, x = {}, [], []
    for row in doc.get("c") or []:
        p, h, l, qv = fnum(row.get("p")), fnum(row.get("h")), fnum(row.get("l")), fnum(row.get("qv"))
        if not row.get("s") or not all(v is not None and v > 0 for v in (p, h, l, qv)):
            continue
        c.append(dict(s=row["s"], p=p, h=h, l=l, qv=qv, chg=fnum(row.get("chg")), fr=fnum(row.get("fr")),
                      oi=fnum(row.get("oi")), mark=fnum(row.get("mark"))))
        places[row["s"]] = decimals(row["p"])
    for row in doc.get("x") or []:
        p, qv = fnum(row.get("lastPrice")), fnum(row.get("quoteVolume"))
        if not row.get("symbol") or p is None or p <= 0 or qv is None:
            continue
        x.append(dict(s=row["symbol"], p=p, qv=qv, chg=fnum(row.get("priceChangePercent")),
                      open=fnum(row.get("openPrice"))))
        places.setdefault(row["symbol"], decimals(row["lastPrice"]))
    if not c:
        raise ValueError("the payload holds no list row")
    return doc.get("ts"), c, x, places


def run_gate(tree):
    """The live-data gate exactly as the writer runs it; its exit code (section 5 step 2)."""
    try:
        return subprocess.run([os.path.join(".", "analyst", "live-gate.sh")], cwd=tree, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL, timeout=120).returncode
    except (OSError, subprocess.SubprocessError):
        return 127


def stem_of(tree, day):
    """The run's stem: the day, or day-N where that day's log or press record exists (section 5 step 4)."""
    taken = set()
    for sub, ext in (("log", ".md"), ("press", ".json")):
        try:
            taken |= {n[:-len(ext)] for n in os.listdir(os.path.join(tree, "analyst", sub)) if n.endswith(ext)}
        except FileNotFoundError:
            pass
    if day not in taken:
        return day
    n = 2
    while "%s-%d" % (day, n) in taken:
        n += 1
    return "%s-%d" % (day, n)


def structural(tree, freeze):
    """The newest journal/data/<date>.jsonl's btc object where dated the freeze's UTC day or the day before, else
    None -- a GAP (section 5)."""
    folder = os.path.join(tree, "journal", "data")
    try:
        names = sorted(n for n in os.listdir(folder) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.jsonl", n))
    except FileNotFoundError:
        return None, None
    if not names:
        return None, None
    newest = names[-1]
    day = date.fromisoformat(newest[:10])
    if day not in (freeze.date(), freeze.date() - timedelta(days=1)):
        return newest, None
    with open(os.path.join(folder, newest), encoding="utf-8") as fh:
        for line in fh:
            try:
                btc = json.loads(line).get("btc")
            except ValueError:
                continue
            if isinstance(btc, dict) and all(fnum(btc.get(k)) is not None for k in
                                             ("min_price", "max_price", "price_pos", "volatility", "r7", "r14")):
                return newest, {k: fnum(btc[k]) for k in ("min_price", "max_price", "price_pos", "volatility",
                                                           "r7", "r14")}
    return newest, None


def read_owner(tree):
    try:
        with open(os.path.join(tree, "analyst", "owner.json"), encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


# ------------------------------------------------------------------ the book and its cards

def cg_symbols(net):
    """CoinGecko's top 100 by capitalisation, read once: upper-cased symbols; a short or malformed read admits no
    outside row (section 3, filter 4)."""
    doc = net.json(CG_URL)
    if not isinstance(doc, list) or len(doc) < CG_ROWS:
        raise ValueError("CoinGecko answered %s rows" % (len(doc) if isinstance(doc, list) else "no"))
    return {str(o.get("symbol", "")).upper() for o in doc if isinstance(o, dict)}


def underlying(symbol):
    base = base_name(symbol)
    for prefix in CG_PREFIXES:
        if base.startswith(prefix) and len(base) > len(prefix):
            return base[len(prefix):]
    return base


def outside_rows(x, list_symbols, top):
    """Rows of x passing filters 1, 2 and 4 that are not list symbols, by descending turnover."""
    rows = [r for r in x if r["s"].endswith("USDT") and "_" not in r["s"] and r["s"] not in list_symbols
            and r["qv"] >= TURNOVER_MIN and underlying(r["s"]).upper() in top]
    return sorted(rows, key=lambda r: -r["qv"])


def read_book(symbols, prices, now_ms, day_of, workers=WORKERS):
    """Each symbol's rule state on its 400 daily rows and the card it gives at the frozen price, as `book.py --live
    --payload` prints them (TZ-84): a hold gives none. {symbol: (state, card, bars, today)}; a failed read is
    `unread` with its error class."""
    def one(s):
        try:
            bars, today = day_of(s, now_ms)
            state = book.state_of(s, bars, today[1])[0]
            card = None
            if state.get("state") != "short-history" and prices.get(s) is not None:
                card = book.card_of(state, prices[s], today)
                if card is not None and card.get("kind") == "late":
                    card = None
            return s, (state, card, bars, today)
        except Exception as exc:              # one symbol's failure never hides the others
            return s, (dict(symbol=s, state="unread", error=exc.__class__.__name__), None, None, None)
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        return dict(ex.map(one, symbols))


def vol_hour(atr20, anchor):
    """Section 4: vol_h = atr20 / (anchor x sqrt(8/pi) x sqrt(24))."""
    return atr20 / (anchor * math.sqrt(8 / math.pi) * math.sqrt(24))


def lmax_of(lstruct, vol_h, consts, card):
    """Section 4: floor(min(lStruct(d, vol_h), card.lev_max)), at most 2 where vol_h >= VOL_HARD."""
    if lstruct is None:
        return 0
    lm = int(math.floor(min(lstruct, card["lev_max"])))
    return min(lm, 2) if vol_h >= consts["VOL_HARD"] else lm


def candidates(rows, book_read, prices, places, turnover):
    """Every card the book's states give (section 4): an entry due at the frozen price, and a flat symbol's trigger
    within the week's reach; the forming-day and half-way refusals named."""
    out = []
    for s in rows:
        state, card, _bars, _today = book_read.get(s, (None, None, None, None))
        if state is None or card is None:
            continue
        p = prices[s]
        if card["kind"] == "entry":
            side = 1 if state["state"] == "long" else -1
            refusal = ("forming-day" if card.get("touched") or card.get("band") == "closed"
                       else "half-way" if card.get("band") == "near" else None)
            out.append(dict(sym=s, side=side, kind="now", anchor=p, stop=card["stop"], target=card.get("target"),
                            void=card.get("void"), exit_level=state.get("exit_level"), fill=state.get("entry"),
                            atr20=state["atr20"], d=card["d"], refusal=refusal, places=places.get(s, 8),
                            qv=turnover.get(s, 0.0)))
        elif card["kind"] == "trigger":
            for name, side in (("long", 1), ("short", -1)):
                t = card[name]
                if not t["reach"]:
                    continue
                out.append(dict(sym=s, side=side, kind="wait", anchor=t["anchor"],
                                stop=t["stop"], target=t["target"], void=None, exit_level=None, fill=None,
                                atr20=state["atr20"], d=t["d"], refusal=None, places=places.get(s, 8),
                                qv=turnover.get(s, 0.0), price=p))
    return out


def liquidation(cards, owner_card, index_html):
    """Section 4's liquidation test on every card: production's lStruct at the card's own distance and hourly
    volatility; a card refused where vol_h >= VOL_STOP or Lmax falls under card.lev_min."""
    calls = []
    for c in cards:
        c["dist"] = abs(c["anchor"] - c["stop"]) / c["anchor"]
        c["vol_h"] = vol_hour(c["atr20"], c["anchor"])
        calls.append(["lStruct", c["dist"], c["vol_h"]])
    consts, out = production(index_html, calls)
    for c, ls in zip(cards, out):
        c["lstruct"] = ls
        if owner_card is None:
            c["lmax"] = None
            continue
        c["lmax"] = lmax_of(ls, c["vol_h"], consts, owner_card)
        if c["refusal"] is None and (c["vol_h"] >= consts["VOL_STOP"] or c["lmax"] < owner_card["lev_min"]):
            c["refusal"] = "liquidation"
    return consts


# ------------------------------------------------------------------ positioning, flow and the derivatives

def _rows(doc, keys):
    if not isinstance(doc, list):
        raise ValueError("shape")
    out = []
    for r in doc:
        if not isinstance(r, dict) or any(k not in r for k in keys):
            raise ValueError("shape")
        vals = [fnum(r[k]) for k in keys]
        if any(v is None for v in vals):
            continue
        out.append(vals)
    return out


def positioning_one(sym, net, freeze_ms):
    """Section 16's positioning read of one perpetual: its large and crowd classes and its flow."""
    base = FAPI + "/futures/data/"
    q = "?symbol=%s&period=4h&limit=%d" % (sym, POS_LIMIT)
    try:
        oi = _rows(net.json(base + "openInterestHist" + q), ("timestamp", "sumOpenInterest"))
        large = _rows(net.json(base + "topLongShortPositionRatio" + q), ("timestamp", "longShortRatio"))
        crowd = _rows(net.json(base + "globalLongShortAccountRatio" + q), ("timestamp", "longShortRatio"))
        start = freeze_ms - FUND_LOOKBACK_D * DAY_MS
        fund = _rows(net.json(FAPI + "/fapi/v1/fundingRate?symbol=%s&startTime=%d&limit=1000" % (sym, start)),
                     ("fundingTime", "fundingRate"))
        taker = _rows(net.json(base + "takerlongshortRatio" + q), ("timestamp", "buyVol", "sellVol"))
    except Refused as exc:
        return dict(large="unread", crowd="unread", why="refused " + str(exc))
    except ValueError as exc:
        return dict(large="unread", crowd="unread", why=str(exc))
    except Exception as exc:
        return dict(large="unread", crowd="unread", why=exc.__class__.__name__)
    keep = lambda rows: sorted((r for r in rows if r[0] <= freeze_ms), key=lambda r: r[0])  # noqa: E731
    oi, large, crowd, fund, taker = keep(oi), keep(large), keep(crowd), keep(fund), keep(taker)
    out = dict(large="unread", crowd="unread", oi24=None, buy=None, rows=[len(oi), len(large), len(crowd),
                                                                         len(fund), len(taker)])
    if len(oi) >= POS_DAY + 1 and oi[-1 - POS_DAY][1] > 0:
        out["oi24"] = (oi[-1][1] / oi[-1 - POS_DAY][1] - 1) * 100
    if len(taker) >= POS_DAY:
        b = sum(r[1] for r in taker[-POS_DAY:])
        s = sum(r[2] for r in taker[-POS_DAY:])
        out["buy"] = b / (b + s) * 100 if b + s > 0 else None
    span = (fund[-1][0] - fund[0][0]) / DAY_MS if len(fund) >= 2 else 0
    if min(len(oi), len(large), len(crowd)) < POS_MIN or span < POS_FUND_D or out["oi24"] is None:
        return out

    def changes(series):
        vals = [r[1] for r in series]
        return [math.log(vals[t] / vals[t - POS_K]) for t in range(POS_K, len(vals))
                if vals[t] > 0 and vals[t - POS_K] > 0]
    dL, dC, dQ = changes(large), changes(crowd), changes(oi)
    if not dL or not dC or not dQ:
        return out
    d1L = math.log(large[-1][1] / large[-1 - POS_DAY][1])
    crowd_vals = [r[1] for r in crowd]
    fund_vals = [r[1] for r in fund]
    up = dL[-1] >= quartile(dL, 0.75) and dL[-1] > 0 and d1L > 0 and dC[-1] <= quartile(dC, 0.5)
    down = dL[-1] <= quartile(dL, 0.25) and dL[-1] < 0 and d1L < 0 and dC[-1] >= quartile(dC, 0.5)
    fresh = dQ[-1] > 0 and out["oi24"] > 0
    out["large"] = "long" if up and fresh else "short" if down and fresh else "none"
    out["crowd"] = ("long" if crowd_vals[-1] >= quartile(crowd_vals, 0.75) and fund_vals[-1] >= quartile(fund_vals, 0.75)
                    else "short" if crowd_vals[-1] <= quartile(crowd_vals, 0.25)
                    and fund_vals[-1] <= quartile(fund_vals, 0.25) else "none")
    out.update(dL=dL[-1], d1L=d1L, dC=dC[-1], dQ=dQ[-1])
    return out


def read_positioning(symbols, net, freeze_ms, workers=WORKERS):
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        return dict(zip(symbols, ex.map(lambda s: positioning_one(s, net, freeze_ms), symbols)))


def _okx(net, url):
    doc = net.json(url)
    if not isinstance(doc, dict) or str(doc.get("code")) != "0" or not isinstance(doc.get("data"), list):
        raise ValueError("shape")
    return doc["data"]


def read_deriv(net, freeze_ms, btc_mark, btc_open, btc_fr, btc_chg):
    """Section 16 step E: BTC's open interest, funding and takers on each venue that answers, the block's sums and
    its class, and OKX's liquidations of the 24 hours before the freeze."""
    then_ms = freeze_ms - 24 * HOUR_MS
    venues, notes = {}, []

    def at_or_before(rows, t):
        older = [r for r in rows if r[0] <= t]
        return max(older, key=lambda r: r[0]) if older else None
    try:
        oi_coins = fnum(net.json(DERIV_URLS["binance_oi"]).get("openInterest"))
        hist = [r for r in _rows(net.json(DERIV_URLS["binance_hist"]), ("timestamp", "sumOpenInterestValue"))
                if r[0] <= freeze_ms]
        tk = [r for r in _rows(net.json(DERIV_URLS["binance_taker"]), ("timestamp", "buyVol", "sellVol"))
              if then_ms < r[0] <= freeze_ms]
        then = at_or_before(hist, then_ms)
        venues["binance"] = dict(now=oi_coins * btc_mark, then=then[1] if then else None, fr=btc_fr,
                                 buy=sum(r[1] for r in tk), sell=sum(r[2] for r in tk), at=max(r[0] for r in hist))
    except Exception as exc:
        notes.append("binance " + exc.__class__.__name__)
    try:
        doc = net.json(DERIV_URLS["bybit_ticker"])
        row = doc["result"]["list"][0]
        hist_doc = net.json(DERIV_URLS["bybit_hist"])
        hist = [(fnum(r["timestamp"]), fnum(r["openInterest"])) for r in hist_doc["result"]["list"]]
        hist = [r for r in hist if r[0] is not None and r[1] is not None and r[0] <= freeze_ms]
        then = at_or_before(hist, then_ms)
        venues["bybit"] = dict(now=fnum(row["openInterestValue"]), then=then[1] * btc_open if then else None,
                               fr=fnum(row["fundingRate"]), buy=None, sell=None, at=max(r[0] for r in hist))
    except Exception as exc:
        notes.append("bybit " + exc.__class__.__name__)
    try:
        now = fnum(_okx(net, DERIV_URLS["okx_oi"])[0]["oiUsd"])
        fr = fnum(_okx(net, DERIV_URLS["okx_funding"])[0]["fundingRate"])
        hist = [(fnum(r[0]), fnum(r[1])) for r in _okx(net, DERIV_URLS["okx_hist"])]
        hist = [r for r in hist if r[0] is not None and r[1] is not None and r[0] <= freeze_ms]
        tk = [(fnum(r[0]), fnum(r[1]), fnum(r[2])) for r in _okx(net, DERIV_URLS["okx_taker"])]
        tk = [r for r in tk if None not in r and then_ms < r[0] <= freeze_ms]
        then = at_or_before(hist, then_ms)
        venues["okx"] = dict(now=now, then=then[1] if then else None, fr=fr, buy=sum(r[2] for r in tk),
                             sell=sum(r[1] for r in tk), at=max(r[0] for r in hist))
    except Exception as exc:
        notes.append("okx " + exc.__class__.__name__)
    liq = None
    try:
        longs = shorts = 0.0
        after, done, pages = None, False, 0
        while not done and pages < LIQ_PAGES:
            data = _okx(net, OKX_LIQ + ("" if after is None else "&after=%d" % after))
            details = data[0].get("details", []) if data else []
            pages += 1
            if not details:
                break
            for d in details:
                t, sz, bk = fnum(d.get("ts")), fnum(d.get("sz")), fnum(d.get("bkPx"))
                if None in (t, sz, bk):
                    continue
                if t <= then_ms:
                    done = True
                    continue
                if t > freeze_ms:
                    continue
                if d.get("posSide") == "long":
                    longs += sz * OKX_CT * bk
                elif d.get("posSide") == "short":
                    shorts += sz * OKX_CT * bk
            after = int(min(fnum(d.get("ts")) for d in details if fnum(d.get("ts")) is not None))
        liq = dict(long=longs, short=shorts, source="okx", complete=done)
    except Exception as exc:
        notes.append("liq " + exc.__class__.__name__)
    if not venues:
        return dict(venues={}, notes=notes, liq=liq)
    both = [v for v in venues.values() if v["now"] and v["then"]]
    total_now = sum(v["now"] for v in venues.values() if v["now"])
    change = (sum(v["now"] for v in both) / sum(v["then"] for v in both) - 1) * 100 if both else None
    weighted = [(v["now"], v["fr"]) for v in venues.values() if v["now"] and v["fr"] is not None]
    funding = sum(w * f for w, f in weighted) / sum(w for w, _ in weighted) if weighted else None
    buys = sum(v["buy"] for v in venues.values() if v["buy"] is not None)
    sells = sum(v["sell"] for v in venues.values() if v["sell"] is not None)
    buy = buys / (buys + sells) * 100 if buys + sells > 0 else None
    cls = None
    if change is not None:
        if change > 0 and buy is not None:
            cls = "\u043d\u043e\u0432\u044b\u0445 \u0448\u043e\u0440\u0442\u043e\u0432" if buy < 50 else "\u043d\u043e\u0432\u044b\u0445 \u043b\u043e\u043d\u0433\u043e\u0432" if buy > 50 else None
        elif change < 0 and btc_chg is not None:
            cls = "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u043b\u043e\u043d\u0433\u043e\u0432" if btc_chg <= 0 else "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0448\u043e\u0440\u0442\u043e\u0432"
    at = max(v["at"] for v in venues.values())
    return dict(venues=venues, notes=notes, liq=liq, oi=total_now, change=change, funding=funding, buy=buy,
                cls=cls, at=at)


def deriv_block(dv):
    """Section 2's derivatives block of BTC from step E's figures: (lines, colour of indicator 6, of 7)."""
    if not dv or not dv.get("venues"):
        return ["\u26a0\ufe0f \u0414\u0435\u0440\u0438\u0432\u0430\u0442\u0438\u0432\u044b: \u0434\u0430\u043d\u043d\u044b\u0435 \u043d\u0435 \u043f\u043e\u043b\u0443\u0447\u0435\u043d\u044b"], "unread", "unread"
    names = {"binance": "Binance", "bybit": "Bybit", "okx": "OKX"}
    at = datetime.fromtimestamp(dv["at"] / 1000, timezone.utc).strftime("%H:%M")
    head = " \u00b7 ".join(names[k] for k in ("binance", "bybit", "okx") if k in dv["venues"]) + " \u00b7 \u0434\u0430\u043d\u043d\u044b\u0435 \u043d\u0430 %s UTC" % at
    no = "\u043d\u0435\u0442 \u0434\u0430\u043d\u043d\u044b\u0445"
    liq = dv.get("liq")
    rows = [("\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0438\u043d\u0442\u0435\u0440\u0435\u0441", "$%.1f \u043c\u043b\u0440\u0434" % (dv["oi"] / 1e9)),
            ("OI \u0437\u0430 \u0441\u0443\u0442\u043a\u0438", pct(dv["change"]) + "%" if dv["change"] is not None else no),
            ("\u0420\u043e\u0441\u0442 OI \u0437\u0430 \u0441\u0447\u0451\u0442:" if (dv["change"] or 0) >= 0 else "\u041f\u0430\u0434\u0435\u043d\u0438\u0435 OI:", dv["cls"] or no),
            ("\u041f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u0438/\u043f\u0440\u043e\u0434\u0430\u0432\u0446\u044b", "%d%%/%d%%" % (whole(dv["buy"]), 100 - whole(dv["buy"]))
             if dv["buy"] is not None else no),
            ("Funding, \u0441\u0440\u0435\u0434\u043d\u0438\u0439 8\u0447", pct(dv["funding"] * 100, 4) + "%" if dv["funding"] is not None else no)]
    if liq:
        label = "\u041b\u0438\u043a\u0432\u0438\u0434\u0430\u0446\u0438\u0438 24\u0447 (OKX)" if liq["source"] == "okx" else "\u041b\u0438\u043a\u0432\u0438\u0434\u0430\u0446\u0438\u0438 24\u0447"
        rows += [(label, "$%.1f \u043c\u043b\u043d" % ((liq["long"] + liq["short"]) / 1e6)),
                 ("  \u043b\u043e\u043d\u0433\u043e\u0432", "$%.1f \u043c\u043b\u043d" % (liq["long"] / 1e6)), ("  \u0448\u043e\u0440\u0442\u043e\u0432", "$%.1f \u043c\u043b\u043d" % (liq["short"] / 1e6))]
    else:
        rows.append(("\u041b\u0438\u043a\u0432\u0438\u0434\u0430\u0446\u0438\u0438 24\u0447", no))
    width = max(len(a) + len(b) for a, b in rows) + 1
    table = ["```"] + [a + " " * (width - len(a) - len(b)) + b for a, b in rows] + ["```"]
    facts = {"\u043d\u043e\u0432\u044b\u0445 \u0448\u043e\u0440\u0442\u043e\u0432": "\U0001f534 \u041d\u043e\u0432\u044b\u0435 \u0434\u0435\u043d\u044c\u0433\u0438 \u0438\u0434\u0443\u0442 \u0432 \u0448\u043e\u0440\u0442: OI \u0440\u0430\u0441\u0442\u0451\u0442, \u043f\u0440\u043e\u0434\u0430\u0432\u0446\u044b \u0441\u0438\u043b\u044c\u043d\u0435\u0435",
             "\u043d\u043e\u0432\u044b\u0445 \u043b\u043e\u043d\u0433\u043e\u0432": "\U0001f7e2 \u041d\u043e\u0432\u044b\u0435 \u0434\u0435\u043d\u044c\u0433\u0438 \u0438\u0434\u0443\u0442 \u0432 \u043b\u043e\u043d\u0433: OI \u0440\u0430\u0441\u0442\u0451\u0442, \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u0438 \u0441\u0438\u043b\u044c\u043d\u0435\u0435",
             "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u043b\u043e\u043d\u0433\u043e\u0432": "\U0001f534 \u041b\u043e\u043d\u0433\u0438 \u0432\u044b\u0445\u043e\u0434\u044f\u0442: OI \u043f\u0430\u0434\u0430\u0435\u0442 \u0432\u043c\u0435\u0441\u0442\u0435 \u0441 \u0446\u0435\u043d\u043e\u0439",
             "\u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044f \u0448\u043e\u0440\u0442\u043e\u0432": "\U0001f7e2 \u0428\u043e\u0440\u0442\u044b \u0432\u044b\u0445\u043e\u0434\u044f\u0442: OI \u043f\u0430\u0434\u0430\u0435\u0442, \u0446\u0435\u043d\u0430 \u0440\u0430\u0441\u0442\u0451\u0442"}
    lines = [head] + table
    if dv["cls"] in facts:
        fact = facts[dv["cls"]]
        if liq and liq["long"] != liq["short"]:
            fact += ", \u043b\u043e\u043d\u0433\u0438 \u043b\u0438\u043a\u0432\u0438\u0434\u0438\u0440\u0443\u044e\u0442 \u0447\u0430\u0449\u0435" if liq["long"] > liq["short"] else ", \u0448\u043e\u0440\u0442\u044b \u043b\u0438\u043a\u0432\u0438\u0434\u0438\u0440\u0443\u044e\u0442 \u0447\u0430\u0449\u0435"
        lines.append(fact)
    six = {"\u043d\u043e\u0432\u044b\u0445 \u0448\u043e\u0440\u0442\u043e\u0432": "red", "\u043d\u043e\u0432\u044b\u0445 \u043b\u043e\u043d\u0433\u043e\u0432": "green"}.get(dv["cls"], "white" if dv["cls"] else "unread")
    seven = ("unread" if dv["funding"] is None else "red" if dv["funding"] > FUNDING_HOT
             else "green" if dv["funding"] < 0 else "white")
    return lines, six, seven


def read_etf(path, freeze):
    """Section 16 step D's record: whether it stands, and the newest three sessions per asset."""
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except (OSError, ValueError) as exc:
        return dict(stands=False, why="record unread " + exc.__class__.__name__)
    try:
        ts = datetime.fromisoformat(str(d["ts"]).replace("Z", "+00:00"))
        btc = d["types"]["us-btc-spot"]
        newest = date.fromisoformat(str(btc["date"])[:10])
    except (KeyError, TypeError, ValueError):
        return dict(stands=False, why="record shape")
    if d.get("k") != "etf" or freeze - ts > timedelta(hours=ETF_TS_H) or freeze.date() - newest > timedelta(days=ETF_DATE_D):
        return dict(stands=False, why="record stale")

    def days_of(t):
        e = d["types"].get(t) or {}
        days = e.get("days")
        if isinstance(days, list) and days:
            return {str(x.get("date"))[:10]: fnum(x.get("net")) for x in days if isinstance(x, dict)}
        return {str(e.get("date"))[:10]: fnum(e.get("net"))} if e.get("date") else {}
    btc_days = sorted(days_of("us-btc-spot"), reverse=True)[:3]
    table = {name: days_of(t) for name, t in ETF_TYPES}
    edge = freeze - timedelta(hours=ETF_CAUGHT_H)
    missing, day = [], newest + timedelta(days=1)
    while datetime(day.year, day.month, day.day, US_CLOSE_H, tzinfo=timezone.utc) <= edge:
        if day.weekday() < 5:
            missing.append(day.isoformat())
        day += timedelta(days=1)
    return dict(stands=True, provider=d.get("provider"), host=d.get("host"), ts=d.get("ts"), days=btc_days,
                net={name: [table[name].get(day) for day in btc_days] for name, _ in ETF_TYPES}, missing=missing)


def etf_block(etf):
    """Section 2's ETF table, in USD millions, newest session first (the figures of the record are dollars)."""
    if not etf.get("stands"):
        return [], "unread"

    def cell(v):
        return "\u2014" if v is None else "0.0" if round(v / 1e6, 1) == 0 else num1(v / 1e6)
    rows = []
    for i, day in enumerate(etf["days"]):
        d = date.fromisoformat(day)
        rows.append([WEEKDAYS[d.weekday()] + " " + d.strftime("%d.%m")] + [cell(etf["net"][n][i]) for n, _ in ETF_TYPES])
    sums = []
    for n, _ in ETF_TYPES:
        vals = [v for v in etf["net"][n] if v is not None]
        sums.append(cell(sum(vals)) if vals else "\u2014")
    rows.append(["\u0417\u0430 %d \u0434\u043d\u044f" % len(etf["days"])] + sums)
    widths = [max(len(r[i]) for r in rows + [["\u0414\u0430\u0442\u0430", "BTC", "ETH", "SOL"]]) for i in range(4)]
    head = ["\u0414\u0430\u0442\u0430".ljust(widths[0])] + [h.rjust(widths[i + 1] + 1) for i, h in enumerate(("BTC", "ETH", "SOL"))]
    lines = ["```", "".join(head)] + ["".join([r[0].ljust(widths[0])] + [r[i + 1].rjust(widths[i + 1] + 1)
                                                                          for i in range(3)]) for r in rows] + ["```"]
    btc = [v for v in etf["net"]["BTC"] if v is not None]
    colour = ("unread" if etf.get("missing") else "red" if len(btc) == 3 and all(v < 0 for v in btc) else
              "green" if len(btc) == 3 and all(v > 0 for v in btc) else "white")
    return lines, colour


# ------------------------------------------------------------------ BTC: the map, the scale, the regime

def closes(bars):
    return [b[4] for b in bars]


def scale_of(bars, dates=None):
    """Section 4's measured scale on closed daily bars (oldest first, one a UTC day): `ordinary`, two-day's median
    and upper quartile over the thirty closed days, and with `dates` the class -- two-day of the UTC day after each
    dated instance in the 365 days before -- or two-day standing in under four instances. Per cent."""
    cl = closes(bars)
    if len(cl) < SCALE_DAYS + 3:
        return None
    day = [abs(cl[i] / cl[i - 1] - 1) for i in range(len(cl) - SCALE_DAYS, len(cl))]
    two = [abs(cl[i] / cl[i - 2] - 1) for i in range(len(cl) - SCALE_DAYS, len(cl))]
    out = dict(ordinary=median(day) * 100, two_med=median(two) * 100, two_q75=quartile(two, 0.75) * 100)
    cls = []
    if dates:
        index = {utc_day(b[0]): i for i, b in enumerate(bars)}
        last = utc_day(bars[-1][0])
        for d in dates:
            if not (last - timedelta(days=CLASS_DAYS) <= d <= last):
                continue
            i = index.get(d)
            if i is None or i < 1 or i + 1 >= len(cl):
                continue
            cls.append(abs(cl[i + 1] / cl[i - 1] - 1))
    if len(cls) >= CLASS_MIN:
        out.update(lo=median(cls) * 100, hi=quartile(cls, 0.75) * 100, n=len(cls), stand_in=False)
    else:
        out.update(lo=out["two_med"], hi=out["two_q75"], n=len(cls), stand_in=True)
    return out


def btc_map(p, payload_hl, daily_closed, bars4, vol, sigma_day, chase_sd):
    """Section 4's BTC map: named levels, zones of width w, the zone holding P, two zones a side, the cancel prices
    and the corridor; every price computed, none drawn."""
    closed = bars4[-(MAP_LIMIT - 1):]
    levels = [("H", "max", payload_hl[0]), ("H", "min", payload_hl[1])]
    prev = daily_closed[-1]
    levels += [("D", "max", prev[2]), ("D", "min", prev[3])]
    w42 = closed[-MAP_W:]
    levels += [("W", "max", max(b[2] for b in w42)), ("W", "min", min(b[3] for b in w42))]
    levels += [("M", "max", max(b[2] for b in closed)), ("M", "min", min(b[3] for b in closed))]
    for i in range(2, len(closed) - 2):
        if closed[i][2] > max(closed[i - 2][2], closed[i - 1][2], closed[i + 1][2], closed[i + 2][2]):
            levels.append(("S", "max", closed[i][2]))
        if closed[i][3] < min(closed[i - 2][3], closed[i - 1][3], closed[i + 1][3], closed[i + 2][3]):
            levels.append(("S", "min", closed[i][3]))
    width = chase_sd * sigma_day * p
    zones, cur = [], []
    for lv in sorted(levels, key=lambda t: t[2]):
        if cur and lv[2] - cur[0][2] <= width:
            cur.append(lv)
        else:
            if len(cur) >= 2:
                zones.append(cur)
            cur = [lv]
    if len(cur) >= 2:
        zones.append(cur)
    zones = [dict(lo=z[0][2], hi=z[-1][2], names=sorted({n + "-" + k for n, k, _ in z})) for z in zones]
    inzone = next((z for z in zones if z["lo"] <= p <= z["hi"]), None)
    below = sorted((z for z in zones if z["hi"] < p), key=lambda z: -z["hi"])[:2]
    above = sorted((z for z in zones if z["lo"] > p), key=lambda z: z["lo"])[:2]
    lo, hi = p * math.exp(-vol * math.sqrt(CORRIDOR_H)), p * math.exp(vol * math.sqrt(CORRIDOR_H))
    bull = inzone["lo"] if inzone else below[0]["lo"] if below else lo
    bear = inzone["hi"] if inzone else above[0]["hi"] if above else hi
    return dict(p=p, width=width, levels=[dict(name=n, kind=k, price=v) for n, k, v in levels], zones=zones,
                inzone=inzone, S=below, R=above, bull=bull, bear=bear, corridor=[lo, hi])


def regime_of(btc, p, index_html):
    """The regime word, produced: marketRegime on the structural btc object re-expressed at the frozen price, and
    the four prices that go to the state (section 2)."""
    pp = btc["min_price"] + btc["price_pos"] / 100 * (btc["max_price"] - btc["min_price"])
    r7 = (1 + btc["r7"]) * p / pp - 1
    r14 = (1 + btc["r14"]) * p / pp - 1
    vol = btc["volatility"]
    consts, out = production(index_html, [["regime", {"volatility": vol, "r7": r7, "r14": r14}],
                                          ["sigmaDay", vol]])
    reg = out[0]
    if reg["mode"] == "stress":
        word = "hot" if reg.get("z") is not None and reg["z"] >= consts["REG_STRESS_Z"] else "stress"
    elif reg["mode"] == "trend":
        word = "up" if reg["dir"] > 0 else "down"
    else:
        word = "range"
    p14, p7 = pp / (1 + btc["r14"]), pp / (1 + btc["r7"])
    st = dict(bull=p14 * (1 + consts["EFF_TREND"] * vol * math.sqrt(2 * consts["H_NOISE"])),
              bear=p14 * (1 - consts["EFF_TREND"] * vol * math.sqrt(2 * consts["H_NOISE"])))
    if vol < consts["VOL_HARD"]:
        st.update(hot=p7 * (1 + consts["REG_STRESS_Z"] * vol * math.sqrt(consts["H_NOISE"])),
                  cold=p7 * (1 - consts["REG_STRESS_Z"] * vol * math.sqrt(consts["H_NOISE"])))
    return dict(word=word, mode=reg["mode"], dir=reg["dir"], eff=reg.get("eff"), z=reg.get("z"), r7=r7, r14=r14,
                sigma_day=out[1], consts=consts, state=st)


def klines(net, sym, interval, limit):
    rows = net.json(FAPI + "/fapi/v1/klines?symbol=%s&interval=%s&limit=%d" % (sym, interval, limit))
    return [(int(r[0]), float(r[1]), float(r[2]), float(r[3]), float(r[4]), int(r[6])) for r in rows]


def world_rows(x_by, net, now_ms):
    """Section 2's world table: lastPrice, the day's change and the week over field 4 of the first of eight daily
    rows; a symbol absent from x drops its row."""
    out = []
    for s in WORLD:
        row = x_by.get(s)
        if row is None:
            continue
        week = None
        try:
            rows = klines(net, s, "1d", 8)
            if rows and rows[0][4] > 0:
                week = (row["p"] / rows[0][4] - 1) * 100
        except Exception:
            week = None
        out.append(dict(sym=s, price=row["p"], day=row["chg"], week=week))
    return out


def world_block(rows):
    names = {"BZUSDT": "\u041d\u0435\u0444\u0442\u044c Brent", "XAUUSDT": "\u0417\u043e\u043b\u043e\u0442\u043e", "QQQUSDT": "Nasdaq (QQQ)", "SPYUSDT": "S&P 500(SPY)"}
    if not rows:
        return []
    cells = []
    for r in rows:
        price = "%.2f" % r["price"] if r["price"] < 1000 else group(whole(r["price"]))
        cells.append((names[r["sym"]], price, pct(r["day"]) + "%" if r["day"] is not None else "\u2014",
                      pct(r["week"]) + "%" if r["week"] is not None else "\u2014"))
    w = [max(len(c[i]) for c in cells) for i in range(4)]
    out = ["```", " " * (w[0] + 1) + "\u0426\u0435\u043d\u0430".rjust(w[1]) + " " + "\u0421\u0443\u0442\u043a\u0438".rjust(w[2]) + " " + "\u041d\u0435\u0434\u0435\u043b\u044f".rjust(w[3])]
    out += [c[0].ljust(w[0]) + " " + c[1].rjust(w[1]) + " " + c[2].rjust(w[2]) + " " + c[3].rjust(w[3]) for c in cells]
    return out + ["```"]


# ------------------------------------------------------------------ the market verdict and the score record

def band_colour(value, band):
    if value is None or band is None:
        return "unread"
    return "red" if value < -band else "green" if value > band else "white"


def market(ind):
    """Section 4: ten indicators counted. ind: ten colours. (word key, confidence text, gauge)."""
    red, green = ind.count("red"), ind.count("green")
    unread = ind.count("unread")
    if unread >= 3:
        key, conf = "flat", "\u0434\u0430\u043d\u043d\u044b\u0445 \u043c\u0430\u043b\u043e"
    elif red >= 5 and red - green >= 3:
        key, conf = "bear", "%d/10" % red
    elif green >= 5 and green - red >= 3:
        key, conf = "bull", "%d/10" % green
    else:
        key, conf = "flat", "\u043f\u0435\u0440\u0435\u0432\u0435\u0441\u0430 \u043d\u0435\u0442"
    gauge = "".join(COLOUR[c] for c in sorted(ind, key=lambda c: {"red": 0, "white": 1, "unread": 1, "green": 2}[c]))
    return key, conf, gauge


def score_block(doc, held, prices, owner, freeze):
    """Section 2's score section, from the score record and the held ledger, R in USDT at capital times the first
    card.risk_other_pct (section 2)."""
    import score as score_mod
    if doc is None or owner is None:
        return ["\u26a0\ufe0f \u0421\u0447\u0451\u0442 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d: \u0437\u0430\u043f\u0438\u0441\u044c \u0441\u0438\u0441\u0442\u0435\u043c\u044b \u043d\u0435 \u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u0430"]
    try:
        r_usdt = owner["capital"]["usdt"] * owner["card"]["risk_other_pct"][0] / 100
        lines, hits = ["**\U0001f3af \u0426\u0435\u043b\u0438 \u0432\u0437\u044f\u0442\u044b:**"], []
        for o in doc.get("open") or []:
            if not o.get("scale_date"):
                continue
            side = 1 if o["state"] == "long" else -1
            p = prices.get(o["symbol"])
            now = (" \u00b7 \u0441\u0435\u0439\u0447\u0430\u0441 $%s (%s%%)" % (score_mod.px(p), pct((p / o["entry"] - 1) * 100))) if p else ""
            hits.append("%s **%s** \u00b7 %s \u043e\u0442 $%s \u2192 \u0446\u0435\u043b\u044c \u0432\u0437\u044f\u0442\u0430%s" % (DOT[side], base_name(o["symbol"]), SIDE_RU[side],
                                                                  score_mod.px(o["entry"]), now))
        week = ms_of(freeze) - SCORE_DAYS * DAY_MS
        recent = [r for r in held if r["t_exit"] >= week]
        wins = [r for r in recent if r["r"] > 0]
        losses = [r for r in recent if r["r"] <= 0]
        if hits:
            lines += hits + ["\u041f\u043e\u043b\u043e\u0432\u0438\u043d\u0430 \u0437\u0430\u043a\u0440\u044b\u0442\u0430 \u0441 \u043f\u0440\u0438\u0431\u044b\u043b\u044c\u044e, \u043e\u0441\u0442\u0430\u0442\u043e\u043a \u2014 \u0431\u0435\u0437 \u0440\u0438\u0441\u043a\u0430"]
        win_lines = ["%s **%s** \u00b7 %s \u043e\u0442 $%s \u2192 \u0437\u0430\u043a\u0440\u044b\u0442\u0430 \u0441 \u043f\u0440\u0438\u0431\u044b\u043b\u044c\u044e: +%s USDT" % (
            DOT[r["side"]], base_name(r["symbol"]), SIDE_RU[r["side"]], score_mod.px(r["entry"]),
            group(whole(r["r"] * r_usdt))) for r in wins]
        lines += win_lines
        if not hits and not win_lines:
            lines = ["\U0001f3af \u0426\u0435\u043b\u0435\u0439 \u043f\u043e\u043a\u0430 \u043d\u0435\u0442"]
        if losses:
            lines.append("**\U0001f6d1 \u0417\u0430\u043a\u0440\u044b\u0442\u044b \u0432 \u0443\u0431\u044b\u0442\u043e\u043a \u2014 \u0437\u0430 7 \u0434\u043d\u0435\u0439:**")
            for r in losses:
                how = "\u043f\u043e \u0441\u0442\u043e\u043f\u0443" if r["why"] == "stop" else "\u043f\u043e \u043f\u0440\u0430\u0432\u0438\u043b\u0443 \u0432\u044b\u0445\u043e\u0434\u0430"
                lines.append("%s **%s** \u00b7 %s \u043e\u0442 $%s \u2192 %s: %s USDT" % (DOT[r["side"]], base_name(r["symbol"]),
                                                                    SIDE_RU[r["side"]], score_mod.px(r["entry"]), how,
                                                                    group(whole(r["r"] * r_usdt))))
        closed = doc["closed"]["all"]
        n = closed.get("n", 0)
        tot = closed.get("total", 0.0) if n else 0.0
        opened = doc.get("open") or []
        r_open = sum(o["r_open"] for o in opened if isinstance(o.get("r_open"), (int, float)))
        since = date.fromisoformat(str(doc["since"])[:10]).strftime("%d.%m")
        asof = date.fromisoformat(str(doc["asof"])[:10]).strftime("%d.%m")
        lines.append("\u0418\u0442\u043e\u0433 \u0441 %s (\u043d\u0430 %s): \u0437\u0430\u043a\u0440\u044b\u0442\u043e %d (%s USDT) \u00b7 \u043e\u0442\u043a\u0440\u044b\u0442\u043e %d (%s USDT \u043f\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044e \u0434\u043d\u044f)" % (
            since, asof, n, signed_usdt(tot * r_usdt), len(opened), signed_usdt(r_open * r_usdt)))
        return lines
    except (KeyError, TypeError, ValueError, IndexError):
        return ["\u26a0\ufe0f \u0421\u0447\u0451\u0442 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d: \u0437\u0430\u043f\u0438\u0441\u044c \u0441\u0438\u0441\u0442\u0435\u043c\u044b \u043d\u0435 \u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u0430"]


def signed_usdt(v):
    n = whole(v)
    return ("+" if n > 0 else "") + group(n) if n else "0"


def read_score(score_json, held_dir):
    try:
        with open(score_json, encoding="utf-8") as fh:
            doc = json.load(fh)
    except (OSError, ValueError):
        return None, []
    held = []
    try:
        names = sorted(n for n in os.listdir(held_dir) if n.endswith(".json") and not n.startswith("."))
    except FileNotFoundError:
        names = []
    for n in names:
        try:
            with open(os.path.join(held_dir, n), encoding="utf-8") as fh:
                row = json.load(fh)
            if all(k in row for k in ("symbol", "side", "entry", "t_exit", "r", "why")):
                held.append(row)
        except (OSError, ValueError):
            continue
    return doc, held


# ------------------------------------------------------------------ the press

def press(tree, now=None, net=None, day_of=None, score_paths=(SCORE_JSON, SCORE_HELD), etf_path=ETF_JSON):
    """The whole press of one run. Returns the record; raises only when the payload is unread."""
    started = time.monotonic()
    now = now or datetime.now(timezone.utc)
    freeze = now.replace(microsecond=0)
    net = net or Net(deadline=started + PRESS_S)
    day_of = day_of or book.live_day
    lanes = {}
    ts, c, x, places = read_payload(tree)
    gate = run_gate(tree)
    list_symbols = [r["s"] for r in c]
    prices = {r["s"]: r["p"] for r in x}
    prices.update({r["s"]: r["p"] for r in c})
    turnover = {r["s"]: r["qv"] for r in x}
    turnover.update({r["s"]: r["qv"] for r in c})
    x_by = {r["s"]: r for r in x}
    c_by = {r["s"]: r for r in c}
    with open(os.path.join(tree, "index.html"), encoding="utf-8") as fh:
        index_html = fh.read()
    owner = read_owner(tree)
    owner_card = (owner or {}).get("card")
    stem = stem_of(tree, freeze.strftime("%Y-%m-%d"))
    rec = dict(v=1, k="press", stem=stem, freeze=iso_z(freeze), payload_ts=ts, gate=gate, lanes=lanes)

    try:
        top = cg_symbols(net)
        lanes["coingecko"] = "ok"
    except Exception as exc:
        top, lanes["coingecko"] = set(), "unread " + exc.__class__.__name__
    outside = outside_rows(x, set(list_symbols), top)
    now_ms = ms_of(freeze)
    read = read_book(list_symbols + [r["s"] for r in outside], prices, now_ms, day_of)
    asof = max((st.get("asof") for st, *_ in read.values() if st.get("asof")), default=None)
    lanes["book"] = "list %d/%d outside %d/%d" % (
        sum(1 for s in list_symbols if read[s][0]["state"] not in ("unread",)), len(list_symbols),
        sum(1 for r in outside if read[r["s"]][0]["state"] not in ("unread",)), len(outside))
    rec["states"] = {s: {k: v for k, v in read[s][0].items() if k != "symbol"} for s in read}

    # BTC is the market's measure and the answer's forecast, never a card: the trigger names altcoins, and the list
    # is tokens[] (section 3A); it counts in the trend-system indicator as a row of c (section 4).
    cards_list = candidates([s for s in list_symbols if s != "BTCUSDT"], read, prices, places, turnover)
    cards_out = candidates([r["s"] for r in outside], read, prices, places, turnover)
    consts = {}
    try:
        consts = liquidation(cards_list + cards_out, owner_card, index_html)
        lanes["production"] = "ok"
    except Exception as exc:
        lanes["production"] = "unread " + exc.__class__.__name__
        for cd in cards_list + cards_out:
            cd.setdefault("refusal", None)
    for cd in cards_list:
        cd["list"] = True
    for cd in cards_out:
        cd["list"] = False
    # Positioning and flow (section 16) before any slot: the list, BTC included, and every outside row a card stands
    # on, so that the classes refuse and warn before the hunter is asked anything.
    pos_syms = list_symbols + sorted({cd["sym"] for cd in cards_out}, key=lambda s: -turnover.get(s, 0))
    try:
        pos = read_positioning(pos_syms, net, now_ms)
        lanes["positioning"] = "read %d unread %d" % (sum(1 for v in pos.values() if v["large"] != "unread"),
                                                      sum(1 for v in pos.values() if v["large"] == "unread"))
    except Exception as exc:
        pos, lanes["positioning"] = {}, "unread " + exc.__class__.__name__
    rec["positioning"] = pos
    against = {1: "short", -1: "long"}
    for cd in cards_list + cards_out:
        p = pos.get(cd["sym"], {})
        cd.update(large=p.get("large", "unread"), crowd=p.get("crowd", "unread"), oi24=p.get("oi24"), buy=p.get("buy"))
        # Section 4: an entry is refused where the large players stand against its side with the crowd on it;
        # section 3B: an outside candidate is refused where its large players stand against its side at all.
        if cd["refusal"] is None and cd["kind"] == "now" and cd["large"] == against[cd["side"]] and (
                not cd["list"] or cd["crowd"] == against[-cd["side"]]):
            cd["refusal"] = "large"
        # Section 2's two causes of the warning this run's figures decide: the crowd on the card's side, and a
        # turnover under filter 4's.
        cd["warn"] = ([CROWD_WARN[cd["side"]]] if cd["crowd"] == against[-cd["side"]] else []) + (
            [LIQUIDITY_WARN] if cd["qv"] < TURNOVER_MIN else [])
    # Outside rows: an entry passing every test is a book row of its lane; a flat row's trigger within the week's
    # reach a forward row, nearest first, three a side (section 15's prompt lines).
    book_rows = {1: [], -1: []}
    forward = {1: [], -1: []}
    for cd in cards_out:
        if cd["kind"] == "now" and cd["refusal"] is None:
            book_rows[cd["side"]].append(cd)
        if cd["kind"] == "wait" and cd["refusal"] is None:
            forward[cd["side"]].append(cd)
    for side in (1, -1):
        # Section 3B's slots after a dated event, which the hunt brings: the large players building the lane's
        # side first, then turnover.
        book_rows[side] = [cd["sym"] for cd in sorted(book_rows[side], key=lambda cd: (cd["large"] != against[-side],
                                                                                     -cd["qv"]))]
        forward[side] = [cd["sym"] for cd in sorted(forward[side], key=lambda cd: cd["d"])[:FORWARD_MAX]]
    cards = list(cards_list)
    cards += [cd for cd in cards_out if cd["kind"] == "now" or cd["sym"] in forward[cd["side"]]]
    for cd in cards:
        # An entry the forming day or the half-way test refused carries no target: book.card_of prices none.
        cd["pct_stop"] = (cd["stop"] / cd["anchor"] - 1) * 100
        cd["pct_target"] = None if cd["target"] is None else (cd["target"] / cd["anchor"] - 1) * 100
        if cd["kind"] == "wait":
            cd["need"] = (cd["anchor"] / prices[cd["sym"]] - 1) * 100
    rec["cards"] = cards
    rec["prices"] = {s: prices[s] for s in list_symbols + [r["s"] for r in outside]}
    rec["list"] = list_symbols

    btc = c_by.get("BTCUSDT")
    btc_read = read.get("BTCUSDT", (None, None, None, None))
    rec["btc"] = dict(p=btc["p"] if btc else None, chg=btc["chg"] if btc else None)
    newest, sbtc = structural(tree, freeze)
    lanes["structural"] = newest + (" ok" if sbtc else " GAP") if newest else "absent"
    reg = None
    if btc and sbtc:
        try:
            reg = regime_of(sbtc, btc["p"], index_html)
        except Exception as exc:
            lanes["regime"] = "unread " + exc.__class__.__name__
    rec["regime"] = reg
    scale = scale_of(btc_read[2]) if btc_read[2] else None
    rec["btc"]["scale"] = scale
    if btc and sbtc and reg and btc_read[2]:
        try:
            bars4 = [b for b in klines(net, "BTCUSDT", "4h", MAP_LIMIT) if b[5] < now_ms]
            rec["btc"]["map"] = btc_map(btc["p"], (btc["h"], btc["l"]), btc_read[2], bars4, sbtc["volatility"],
                                        reg["sigma_day"], reg["consts"]["ENTRY_CHASE_SD"])
            lanes["map"] = "ok %d bars" % len(bars4)
        except Exception as exc:
            lanes["map"] = "unread " + exc.__class__.__name__
    else:
        lanes["map"] = "not drawn"

    try:
        dv = read_deriv(net, now_ms, btc["mark"], (x_by.get("BTCUSDT") or {}).get("open") or btc["p"],
                        btc["fr"], btc["chg"])
        lanes["deriv"] = ",".join(sorted(dv["venues"])) or "none"
    except Exception as exc:
        dv, lanes["deriv"] = None, "unread " + exc.__class__.__name__
    rec["deriv"] = dv
    etf = read_etf(etf_path, freeze)
    lanes["etf"] = "stands" if etf["stands"] else etf["why"]
    rec["etf"] = etf
    rec["world"] = world_rows(x_by, net, now_ms)

    # The ten indicators (section 4).
    ind, figures = [], {}
    o = scale["ordinary"] if scale else None
    if reg and o is not None:
        figures[1], figures[2] = reg["r14"] * 100, reg["r7"] * 100
        ind += [band_colour(reg["r14"] * 100, o * math.sqrt(14)), band_colour(reg["r7"] * 100, o * math.sqrt(7))]
    else:
        ind += ["unread", "unread"]
    figures[3] = btc["chg"] if btc else None
    ind.append(band_colour(figures[3], o))
    held = [read[s][0]["state"] for s in list_symbols if read[s][0]["state"] in ("long", "short", "flat")]
    n_short, n_long = held.count("short"), held.count("long")
    figures[4] = [n_short, n_long, len(held)]
    ind.append("unread" if not held else "red" if n_short * 3 >= 2 * len(held) else
               "green" if n_long * 3 >= 2 * len(held) else "white")
    etf_lines, etf_colour = etf_block(etf)
    ind.append(etf_colour)
    dv_lines, six, seven = deriv_block(dv)
    ind += [six, seven]
    bp = pos.get("BTCUSDT", {})
    ind.append({"long": "green", "short": "red", "none": "white"}.get(bp.get("large"), "unread"))
    ind.append({"long": "red", "short": "green", "none": "white"}.get(bp.get("crowd"), "unread"))
    qqq = next((w for w in rec["world"] if w["sym"] == "QQQUSDT"), None)
    figures[10] = qqq["week"] if qqq else None
    ind.append(band_colour(figures[10], QQQ_BAND))
    key, conf, gauge = market(ind)
    alts = median([r["chg"] for r in c if r["s"] != "BTCUSDT" and r["chg"] is not None])
    rec["market"] = dict(ind=ind, figures=figures, word=key, confidence=conf, gauge=gauge, alts=alts)
    try:
        doc, held_rows = read_score(*score_paths)
        rec["score"] = score_block(doc, held_rows, prices, owner, freeze)
        lanes["score"] = "ok" if doc else "unread"
    except Exception as exc:
        rec["score"], lanes["score"] = ["\u26a0\ufe0f \u0421\u0447\u0451\u0442 \u043d\u0435\u0434\u043e\u0441\u0442\u0443\u043f\u0435\u043d: \u0437\u0430\u043f\u0438\u0441\u044c \u0441\u0438\u0441\u0442\u0435\u043c\u044b \u043d\u0435 \u043f\u0440\u043e\u0447\u0438\u0442\u0430\u043d\u0430"], "unread " + exc.__class__.__name__
    rec["blocks"] = dict(deriv=dv_lines, etf=etf_lines, world=world_block(rec["world"]),
                         positions=positions_block(pos, list_symbols, turnover))
    rec["head"] = head_lines(freeze, asof) if asof else None
    rec["hunter"] = hunter_prompt(stem, freeze, c, x, outside, read, cards_list, book_rows, forward, turnover,
                                  ("stands" + (", sessions not caught: " + " ".join(etf["missing"]) if etf["missing"]
                                               else "")) if etf["stands"] else "does not stand: " + etf["why"])
    rec["refused"] = [dict(sym=cd["sym"], side=cd["side"], why=cd["refusal"]) for cd in cards_list + cards_out
                      if cd["refusal"]]
    rec["consts"] = consts
    rec["reads"] = net.reads
    rec["seconds"] = round(time.monotonic() - started, 1)
    return rec


def positions_block(pos, list_symbols, turnover):
    """Section 2's positions section: BTC's two classes, the list's crowd breadth, up to three coins a side the
    large players build, by turnover; a read refused whole drops the section."""
    read = {s: v for s, v in pos.items() if v.get("large") != "unread"}
    if not read:
        return []
    b = pos.get("BTCUSDT", {})
    large = {"long": "\U0001f7e2 \u043d\u0430\u0431\u0438\u0440\u0430\u044e\u0442 \u043b\u043e\u043d\u0433", "short": "\U0001f534 \u043d\u0430\u0431\u0438\u0440\u0430\u044e\u0442 \u0448\u043e\u0440\u0442", "none": "\u26aa \u0431\u0435\u0437 \u043f\u0435\u0440\u0435\u043a\u043e\u0441\u0430"}
    crowd = {"long": "\U0001f534 \u0432 \u043b\u043e\u043d\u0433\u0435", "short": "\U0001f7e2 \u0432 \u0448\u043e\u0440\u0442\u0435", "none": "\u26aa \u0431\u0435\u0437 \u043f\u0435\u0440\u0435\u043a\u043e\u0441\u0430"}
    lines = []
    if b.get("large") in large:
        lines.append("BTC: \u043a\u0440\u0443\u043f\u043d\u044b\u0435 \u0438\u0433\u0440\u043e\u043a\u0438 %s \u00b7 \u0442\u043e\u043b\u043f\u0430 %s" % (large[b["large"]], crowd.get(b.get("crowd"), "\u26aa \u0431\u0435\u0437 \u043f\u0435\u0440\u0435\u043a\u043e\u0441\u0430")))
    coins = [s for s in list_symbols if s != "BTCUSDT" and s in read]
    lines.append("\u041c\u043e\u043d\u0435\u0442\u044b \u0441\u043f\u0438\u0441\u043a\u0430: \u0442\u043e\u043b\u043f\u0430 \u0432 \u0448\u043e\u0440\u0442\u0435 \u2014 **%d \u0438\u0437 %d** \u00b7 \u0432 \u043b\u043e\u043d\u0433\u0435 \u2014 %d" % (
        sum(1 for s in coins if read[s]["crowd"] == "short"), len(coins), sum(1 for s in coins if read[s]["crowd"] == "long")))
    for side, word, dot in (("long", "\u043b\u043e\u043d\u0433", "\U0001f7e2"), ("short", "\u0448\u043e\u0440\u0442", "\U0001f534")):
        syms = sorted((s for s in read if s != "BTCUSDT" and read[s]["large"] == side), key=lambda s: -turnover.get(s, 0))
        if syms:
            lines.append("\u041a\u0440\u0443\u043f\u043d\u044b\u0435 \u0438\u0433\u0440\u043e\u043a\u0438 \u043d\u0430\u0431\u0438\u0440\u0430\u044e\u0442 %s: %s %s" % (word, dot, " \u00b7 ".join(base_name(s) for s in syms[:3])))
    return lines


def head_lines(freeze, asof):
    """Section 2's head: the freeze minute and the book's close, the next UTC midnight in Tbilisi."""
    t = tbilisi(freeze)
    nxt = tbilisi(datetime(freeze.year, freeze.month, freeze.day, tzinfo=timezone.utc) + timedelta(days=1))
    a = date.fromisoformat(asof)
    return ["\u0412\u0440\u0435\u043c\u044f \u0430\u043d\u0430\u043b\u0438\u0437\u0430: %s %s \u00b7 %s \u0422\u0431\u0438\u043b\u0438\u0441\u0438" % (WEEKDAYS[t.weekday()], t.strftime("%d.%m"), t.strftime("%H:%M")),
            "\u0423\u0440\u043e\u0432\u043d\u0438 \u2014 \u043f\u043e \u0437\u0430\u043a\u0440\u044b\u0442\u0438\u044e %s \u00b7 \u043f\u0435\u0440\u0435\u0441\u0447\u0451\u0442 %s %s %s" % (a.strftime("%d.%m"), WEEKDAYS[nxt.weekday()],
                                                           nxt.strftime("%d.%m"), nxt.strftime("%H:%M"))]


def hunter_prompt(stem, freeze, c, x, outside, read, cards_list, book_rows, forward, turnover, etf_state):
    """Methodology section 15's hunter prompt, every line filled from the press."""
    med = median([r["chg"] for r in c if r["chg"] is not None]) or 0.0
    movers = sorted((r for r in c if r["chg"] is not None), key=lambda r: -abs(r["chg"] - med))[:MOVERS]
    out_movers = sorted((r for r in outside if r["chg"] is not None), key=lambda r: -abs(r["chg"]))[:MOVERS]
    signal = []
    seen = set()
    for cd in cards_list:
        if cd["kind"] in ("now", "wait") and (cd["sym"], cd["side"]) not in seen:
            seen.add((cd["sym"], cd["side"]))
            signal.append("%s %s" % (cd["sym"], "long" if cd["side"] > 0 else "short"))

    def names(rows):
        return " ".join(rows) if rows else "none"

    def mv(rows):
        return ", ".join("%s %+.3f%%" % (r["s"], r["chg"]) for r in rows) if rows else "none"
    read_outside = [r["s"] for r in outside if read.get(r["s"], ({},))[0].get("state") not in ("unread", None)]
    return "\n".join([
        "You are the HUNTER of analysis run %s, freeze %s, in the repository at the working" % (stem, iso_z(freeze)),
        "directory. Run: sed -n '/^## 16\\./,/^## 17\\./p' ANALYST-INSTRUCTIONS.md",
        "Read what it prints and do exactly what it says. Read nothing of that file it does not name.",
        "List coins: " + names([r["s"] for r in c]),
        "Turnover order: " + names([r["s"] for r in sorted(c, key=lambda r: -r["qv"])]),
        "Movers, list: " + mv(movers),
        "Movers, outside: " + mv(out_movers),
        "Book rows, long lane: " + names(book_rows[1]),
        "Book rows, short lane: " + names(book_rows[-1]),
        "Outside rows: " + names(read_outside),
        "Forward rows, long lane: " + names(forward[1]),
        "Forward rows, short lane: " + names(forward[-1]),
        "Signal coins: " + (", ".join(signal) if signal else "none"),
        "ETF record: " + etf_state,
        "Return the HUNT REPORT of that section as your final message."])


# ------------------------------------------------------------------ the brief

def card_line(cd):
    """One card's book numbers for the brief, every price as the card prints it."""
    p = cd["places"]
    side = SIDE_RU[cd["side"]]
    tag = ("\u0441\u043f\u0438\u0441\u043e\u043a" if cd["list"] else "\u0432\u043d\u0435 \u0441\u043f\u0438\u0441\u043a\u0430 \u00b7 \u0436\u0434\u0451\u0442 \u0444\u0438\u043b\u044c\u0442\u0440 3 \u0438 \u0440\u0430\u0437\u043b\u043e\u043a" if cd["kind"] == "now"
           else "\u0432\u043d\u0435 \u0441\u043f\u0438\u0441\u043a\u0430 \u00b7 \u0442\u043e\u043b\u044c\u043a\u043e \u0441 \u0441\u043e\u0431\u044b\u0442\u0438\u0435\u043c \u043d\u0430 \u044d\u0442\u0443 \u0441\u0442\u043e\u0440\u043e\u043d\u0443")
    cls = "large %s \u00b7 crowd %s \u00b7 flow %s" % (cd.get("large"), cd.get("crowd"),
                                             "oi24 %s%% buy %d%%" % (pct(cd["oi24"]), whole(cd["buy"]))
                                             if cd.get("oi24") is not None and cd.get("buy") is not None else "unread")
    tail = " | d %.2f atr20 | \u043e\u0431\u043e\u0440\u043e\u0442 $%.1fM | %s" % (cd["d"], cd["qv"] / 1e6, cls)
    if cd["kind"] == "now":
        body = "\u26a1 %s %s %s | \u0412\u0445\u043e\u0434 $`%s` \u00b7 \u043d\u0435 %s $`%s` | \u0421\u0442\u043e\u043f $`%s` (%s%%) | \u0426\u0435\u043b\u044c $`%s` (%s%%) | \u041e\u0441\u0442\u0430\u0442\u043e\u043a $`%s`%s" % (
            base_name(cd["sym"]), side, tag, px(cd["anchor"], p), "\u0432\u044b\u0448\u0435" if cd["side"] < 0 else "\u043d\u0438\u0436\u0435",
            px(cd["void"], p), px(cd["stop"], p), pct(cd["pct_stop"]), px(cd["target"], p), pct(cd["pct_target"]),
            px(cd["exit_level"], p), " (\u0437\u0430 \u0441\u0442\u043e\u043f\u043e\u043c)" if cd["side"] * (cd["exit_level"] - cd["stop"]) < 0 else "")
    else:
        body = "\u23f3 %s %s %s | \u0434\u0435\u043d\u044c \u0437\u0430\u043a\u0440\u043e\u0435\u0442\u0441\u044f %s $`%s` \u00b7 \u0441\u0435\u0439\u0447\u0430\u0441 $%s \u00b7 \u043d\u0443\u0436\u043d\u043e \u0435\u0449\u0451 %s%% | \u0421\u0442\u043e\u043f \u2248 $`%s` (%s%%) | \u0426\u0435\u043b\u044c \u2248 $`%s` (%s%%)" % (
            base_name(cd["sym"]), side, tag, "\u0432\u044b\u0448\u0435" if cd["side"] > 0 else "\u043d\u0438\u0436\u0435", px(cd["anchor"], p),
            px(cd["price"], p), pct(cd["need"]), px(cd["stop"], p), pct(cd["pct_stop"]), px(cd["target"], p),
            pct(cd["pct_target"]))
    if cd["refusal"]:
        body += " | \u041e\u0422\u041a\u0410\u0417: %s (%s)" % (REFUSAL_RU[cd["refusal"]], cd["refusal"])
    if cd.get("warn"):
        body += " | \u26a0\ufe0f " + " \u00b7 ".join(cd["warn"]) + " \u2014 \u0440\u0438\u0441\u043a \u0443\u043c\u0435\u043d\u044c\u0448\u0435\u043d \u0432\u0434\u0432\u043e\u0435 (warn)"
    return body + tail


def brief(rec):
    """The trader's read of this press: every block it prints as given and every number it may print."""
    out = ["PRESS %s \u00b7 freeze %s \u00b7 gate %s \u00b7 record %s/%s.json" % (rec["stem"], rec["freeze"], rec["gate"], PRESS_DIR,
                                                                    rec["stem"]),
           "lanes short: " + (" \u00b7 ".join("%s %s" % kv for kv in sorted(rec["lanes"].items())
                                         if not str(kv[1]).startswith(("ok", "stands", "list", "read", "binance")) and not str(kv[1]).endswith(" ok"))
                                         or "none")]
    if rec["gate"] != 0:
        out.append("GATE FAILED: no level of any kind prints; the answer's first line is \u00ab%s\u00bb" % GATE_SENTENCE)
    out += ["", "## HEAD"] + (rec["head"] or ["unread: no list symbol read"])
    m = rec["market"]
    out += ["", "## MARKET %s \u00b7 %s \u00b7 %s \u00b7 regime %s" % (
        VERDICT_RU[m["word"]], m["confidence"], m["gauge"],
        REGIME_RU[rec["regime"]["word"]] if rec.get("regime") else "\u0414\u0418\u0410\u041f\u0410\u0417\u041e\u041d (no structural file)")]
    btc = rec["btc"]
    if btc.get("p"):
        out.append("BTC **$%s** \u00b7 **%s%%** \u0437\u0430 \u0441\u0443\u0442\u043a\u0438 \u00b7 \u0410\u043b\u044c\u0442\u043a\u043e\u0438\u043d\u044b \u0441\u043f\u0438\u0441\u043a\u0430: **%s%%** \u0437\u0430 \u0441\u0443\u0442\u043a\u0438" % (
            group(whole(btc["p"])), pct(btc["chg"]), pct(m["alts"]) if m["alts"] is not None else "\u2014"))
    f = m["figures"]
    words = {1: "%s%%" % pct(f[1]) if f.get(1) is not None else "unread",
             2: "%s%%" % pct(f[2]) if f.get(2) is not None else "unread",
             3: "%s%% vs ordinary %.2f%%" % (pct(f[3]), btc["scale"]["ordinary"]) if btc.get("scale") and f.get(3) is not None else "unread",
             4: "%d \u0438\u0437 %d \u0432 \u0448\u043e\u0440\u0442\u0435 \u00b7 %d \u0432 \u043b\u043e\u043d\u0433\u0435" % (f[4][0], f[4][2], f[4][1]) if f[4][2] else "unread",
             10: "%s%%" % pct(f[10]) if f.get(10) is not None else "absent"}
    for i, (name, colour) in enumerate(zip(INDICATORS, m["ind"]), 1):
        out.append(" %d %s %s: %s" % (i, COLOUR[colour], name, words.get(i, colour)))
    out += rec["blocks"]["world"]
    out += ["", "## BTC MAP"]
    mp = btc.get("map")
    if mp:
        sc = btc["scale"]
        out.append("P %s \u00b7 \u043e\u0436\u0438\u0434\u0430\u0435\u043c\u044b\u0439 \u0445\u043e\u0434 \u00b1%.1f%% (ordinary %.2f%% \u00b7 two-day median %.2f%% \u00b7 q75 %.2f%%) \u00b7 \u041a\u043e\u0440\u0438\u0434\u043e\u0440 $%s \u2013 $%s" % (
            usd(mp["p"]), sc["two_med"], sc["ordinary"], sc["two_med"], sc["two_q75"], usd(mp["corridor"][0]),
            usd(mp["corridor"][1])))
        zone = lambda z: "%s\u2013%s [%s]" % (usd(z["hi"]), usd(z["lo"]), ",".join(z["names"]))  # noqa: E731
        out.append("zones: " + " \u00b7 ".join(["R%d %s" % (i + 1, zone(z)) for i, z in reversed(list(enumerate(mp["R"])))]
                                          + (["\u0412 \u0417\u041e\u041d\u0415 %s" % zone(mp["inzone"])] if mp["inzone"] else ["no zone holds P"])
                                          + ["S%d %s" % (i + 1, zone(z)) for i, z in enumerate(mp["S"])]))
        out.append("cancel: bull %s (\u041f\u0430\u0434\u0435\u043d\u0438\u0435 \u043d\u0438\u0436\u0435) \u00b7 bear %s (\u0420\u043e\u0441\u0442 \u0432\u044b\u0448\u0435) \u00b7 next resistance %s \u00b7 next support %s" % (
            usd(mp["bull"]), usd(mp["bear"]), usd(mp["R"][0]["lo"]) if mp["R"] else "\u2014",
            usd(mp["S"][0]["hi"]) if mp["S"] else "\u2014"))
        out.append("named: " + " \u00b7 ".join("%s-%s %s" % (lv["name"], lv["kind"], usd(lv["price"]))
                                          for lv in sorted(mp["levels"], key=lambda lv: -lv["price"]) if lv["name"] != "S"))
    else:
        out.append("not drawn: %s" % rec["lanes"].get("map"))
    out += ["", "## \u0414\u0415\u0420\u0418\u0412\u0410\u0422\u0418\u0412\u042b"] + rec["blocks"]["deriv"]
    e = rec["etf"]
    out += ["", "## ETF " + ("record stands \u00b7 %s \u00b7 %s" % (e.get("provider"), e.get("ts")) + (
        " \u00b7 sessions not caught: %s \u2014 the hunt's ETF line adds them and decides indicator 5 (press.py final "
        "MARKET|etf=\u2026)" % " ".join(e["missing"]) if e.get("missing") else "") if e["stands"] else
        "record does not stand: %s \u2014 the hunt's ETF line decides indicator 5 (press.py final MARKET|etf=\u2026)" % e["why"])]
    out += rec["blocks"]["etf"]
    out += ["", "## \u041f\u041e\u0417\u0418\u0426\u0418\u0418"] + (rec["blocks"]["positions"] or ["read refused whole: the section drops"])
    out += ["", "## CARDS \u2014 the book's, every number final but the size (press.py final)"]
    shown = [cd for cd in rec["cards"] if not cd["refusal"]]
    out += [card_line(cd) for cd in shown] or ["none"]
    refused = [cd for cd in rec["cards"] if cd["refusal"]]
    if refused:
        out += ["", "## REFUSED by the book's tests (a list coin's line goes to \u00ab\u26d4 \u041d\u0435 \u0432\u0445\u043e\u0434\u0438\u0442\u044c\u00bb)"]
        out += ["%s \u0432 %s \u2014 %s" % (base_name(cd["sym"]), SIDE_RU[cd["side"]], REFUSAL_RU[cd["refusal"]])
                + ("" if cd["list"] else " (\u0432\u043d\u0435 \u0441\u043f\u0438\u0441\u043a\u0430: appendix only)") for cd in refused]
    out += ["", "## SCORE \u2014 print as given"] + rec["score"]
    out += ["", "## HUNTER \u2014 \u00a715's prompt with stem %s and freeze %s; its lines: press.py hunter %s" % (
        rec["stem"], rec["freeze"], rec["stem"])]
    return "\n".join(out) + "\n"


def write_press(tree, rec):
    folder = os.path.join(tree, PRESS_DIR)
    os.makedirs(folder, exist_ok=True)
    blob = json.dumps(rec, sort_keys=True, ensure_ascii=False, allow_nan=False, default=str).encode("utf-8") + b"\n"
    common.atomic_write(os.path.join(folder, rec["stem"] + ".json"), blob, mode=0o644)
    text = brief(rec)
    common.atomic_write(os.path.join(folder, rec["stem"] + ".md"), text, mode=0o644)
    return hashlib.sha256(blob).hexdigest(), len(text.encode("utf-8"))


def load_press(tree, stem):
    with open(os.path.join(tree, PRESS_DIR, stem + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def newest_press(tree, now):
    """The stem of the newest press record whose freeze lies within FRESH_S of now and whose payload is the one the
    tree holds, or None."""
    folder = os.path.join(tree, PRESS_DIR)
    try:
        names = [n[:-5] for n in os.listdir(folder) if n.endswith(".json") and not n.endswith("-usage.json")]
        ts_now = read_payload(tree)[0]
    except (OSError, ValueError):
        return None
    best = None
    for stem in names:
        try:
            rec = load_press(tree, stem)
            age = (now - datetime.fromisoformat(rec["freeze"].replace("Z", "+00:00"))).total_seconds()
        except (OSError, ValueError, KeyError):
            continue
        if 0 <= age <= FRESH_S and rec.get("payload_ts") == ts_now and (best is None or age < best[0]):
            best = (age, stem)
    return best[1] if best else None


# ------------------------------------------------------------------ final: the sizes of the ranked cards

def size_card(cd, tier, rank, cut, owner, consts):
    """Section 4's ladder for one card: (margin, L, qty, position, loss, gain, liq per cent)."""
    card, capital = owner["card"], owner["capital"]["usdt"]
    margins = card["margin_strong_usdt"] if tier == "STRONG" else card["margin_other_usdt"]
    risks = card["risk_strong_pct"] if tier == "STRONG" else card["risk_other_pct"]
    tier_margin = margins[min(rank, len(margins)) - 1]
    risk = risks[min(rank, len(risks)) - 1] * (owner["risk"]["risk_mult_high"] if cut else 1.0)
    r_usd = capital * risk / 100
    a = cd["anchor"]
    f = cd["dist"] + 2 * consts["FEE_TAKER"]
    top = min(tier_margin, card["margin_max_usdt"])
    margin = max(card["margin_min_usdt"], top)
    lev = min(cd["lmax"], int(math.floor(r_usd / (margin * f))))
    if lev < card["lev_min"]:
        lev = card["lev_min"]
        margin = max(card["margin_min_usdt"], r_usd / (lev * f))
    margin = max(card["margin_min_usdt"], min(margin, top))
    notional = margin * lev
    raw = notional / a
    digits = 3 - int(math.floor(math.log10(raw))) - 1
    qty = math.floor(raw * 10 ** digits) / 10 ** digits
    position = qty * a
    loss = position * f
    gain = qty / 2 * abs(cd["target"] - a) - qty / 2 * a * 2 * consts["FEE_TAKER"]
    return dict(margin=margin, lev=lev, qty=qty, qty_text=qty_text(qty, digits), position=position, loss=loss,
                gain=gain, r_usd=r_usd, capital=capital)


def qty_text(qty, digits):
    return ("%.*f" % (max(0, digits), qty)) if digits > 0 else "%d" % round(qty)


def money_lines(cd, sz):
    approx = "\u2248 " if cd["kind"] == "wait" else ""
    return ["**\u041c\u0430\u0440\u0436\u0430:** `%d` USDT \u00b7 **\u043f\u043b\u0435\u0447\u043e:** `%d`\u00d7" % (whole(sz["margin"]), sz["lev"]),
            "**\u041f\u043e\u0437\u0438\u0446\u0438\u044f:** %s%s USDT \u00b7 `%s` %s" % (approx, group(whole(sz["position"])), sz["qty_text"],
                                                  base_name(cd["sym"])),
            "**\u041f\u0440\u0438 \u0441\u0442\u043e\u043f\u0435:** %s\u2212%s USDT (\u2212%.1f%% \u0434\u0435\u043f\u043e\u0437\u0438\u0442\u0430)" % (approx, group(whole(sz["loss"])),
                                                             sz["loss"] / sz["capital"] * 100),
            "**\u041d\u0430 \u0446\u0435\u043b\u0438:** %s+%s USDT, \u043e\u0441\u0442\u0430\u0442\u043e\u043a \u2014 \u0431\u0435\u0437 \u0440\u0438\u0441\u043a\u0430" % (approx, group(whole(sz["gain"])))]


def parse_final(text):
    """The trader's ranking: `<rank>|<STRONG or the other tier's word>|<SYMBOL>|<long|short>|<flags>`, flags `-` or warn,cut; and
    `MARKET|etf=<red|white|green|unread>`."""
    rows, etf = [], None
    for line in text.splitlines():
        parts = [p.strip() for p in line.strip().split("|")]
        if not parts or not parts[0]:
            continue
        if parts[0] == "MARKET":
            m = re.fullmatch(r"etf=(red|white|green|unread)", parts[1] if len(parts) > 1 else "")
            if not m:
                raise ValueError("MARKET line: %s" % line)
            etf = m.group(1)
            continue
        if len(parts) != 5 or not parts[0].isdigit() or parts[1] not in ("STRONG", "\u041f\u0415\u0420\u0421\u041f") \
                or parts[3] not in ("long", "short"):
            raise ValueError("card line: %s" % line)
        flags = set() if parts[4] in ("-", "") else set(parts[4].split(","))
        if not flags <= {"warn", "cut"}:
            raise ValueError("flags: %s" % line)
        rows.append(dict(rank=int(parts[0]), tier=parts[1], sym=parts[2], side=1 if parts[3] == "long" else -1,
                         flags=flags))
    return rows, etf


def final(rec, rows, etf, owner, index_html):
    """The ranked cards sized and their CARD lines and tickets; the market verdict with the hunt's ETF colour."""
    out, problems = [], []
    by = {(cd["sym"], cd["side"]): cd for cd in rec["cards"]}
    group_rank = {"STRONG": 0, "\u041f\u0415\u0420\u0421\u041f": 0}
    calls, sized = [], []
    consts = rec.get("consts") or {}
    for row in rows:
        cd = by.get((row["sym"], row["side"]))
        if cd is None:
            problems.append("%s %s: no card of the press" % (row["sym"], SIDE_RU[row["side"]]))
            continue
        if cd["refusal"]:
            problems.append("%s %s: refused by the press (%s)" % (row["sym"], SIDE_RU[row["side"]], cd["refusal"]))
            continue
        if cd.get("lmax") is None:
            problems.append("%s %s: no leverage \u2014 production unread" % (row["sym"], SIDE_RU[row["side"]]))
            continue
        group_rank[row["tier"]] += 1
        sz = size_card(cd, row["tier"], group_rank[row["tier"]], bool(row["flags"]), owner, consts)
        sized.append((row, cd, sz))
        calls.append(["liqPrice", cd["anchor"], sz["lev"], cd["side"] > 0])
    liq = production(index_html, calls)[1] if calls else []
    for (row, cd, sz), lq in zip(sized, liq):
        p = cd["places"]
        out.append("T%d %s %s" % (row["rank"], base_name(cd["sym"]), SIDE_RU[cd["side"]]))
        out += money_lines(cd, sz)
        out.append("CARD|%s|%s|%d|%s|%s|%s|%s|fresh|%s|%s|%s|%s|%d|%d|%s" % (
            rec["stem"], rec["freeze"], row["rank"], row["tier"], cd["sym"], "long" if cd["side"] > 0 else "short",
            cd["kind"], px(cd["anchor"], p), px(cd["stop"], p), px(cd["target"], p),
            px(cd["fill"], p) if cd.get("fill") else "\u2014", whole(sz["margin"]), sz["lev"], sz["qty_text"]))
        out.append("ticket: entry %s | stop %s (%s%%)%s | target %s%s | exit %s | size %s ($%d), margin %d, L%d, "
                   "at stop \u2212$%d, at target +$%d | large %s | crowd %s | turnover24h $%.1fM | liq@L %s%% | flow %s" % (
                       px(cd["anchor"], p), px(cd["stop"], p), pct(cd["pct_stop"]), " \u2248" if cd["kind"] == "wait" else "",
                       px(cd["target"], p), " \u2248" if cd["kind"] == "wait" else "",
                       ("close %s %s" % ("below" if cd["side"] > 0 else "above", px(cd["exit_level"], p)))
                       if cd.get("exit_level") else "\u2014", sz["qty_text"], whole(sz["position"]), whole(sz["margin"]),
                       sz["lev"], whole(sz["loss"]), whole(sz["gain"]), cd.get("large"), cd.get("crowd"),
                       cd["qv"] / 1e6, pct((lq / cd["anchor"] - 1) * 100),
                       "oi24 %s%% taker buy %d%%" % (pct(cd["oi24"]), whole(cd["buy"]))
                       if cd.get("oi24") is not None and cd.get("buy") is not None else "unread"))
    pos = rec.get("positioning") or {}
    coins = [s for s in rec.get("list", []) if s != "BTCUSDT" and pos.get(s, {}).get("large", "unread") != "unread"]
    states = rec.get("states") or {}
    holds = [states[s].get("state") for s in rec.get("list", []) if s in states
             and states[s].get("state") in ("long", "short") and not states[s].get("entry_due")]
    margin = sum(sz["margin"] for _, _, sz in sized)
    loss = sum(sz["loss"] for _, _, sz in sized)
    capital = owner["capital"]["usdt"]
    out.append("head: list crowd short %d/%d \u00b7 crowd long %d/%d | book holds long %d \u00b7 short %d | portfolio margin %s "
               "USDT \u00b7 loss at every stop %s USDT (%.1f%% of capital) \u00b7 cards %d (STRONG %d)" % (
                   sum(1 for s in coins if pos[s].get("crowd") == "short"), len(coins),
                   sum(1 for s in coins if pos[s].get("crowd") == "long"), len(coins), holds.count("long"),
                   holds.count("short"), group(whole(margin)), group(whole(loss)), loss / capital * 100, len(sized),
                   sum(1 for row, _, _ in sized if row["tier"] == "STRONG")))
    ind = list(rec["market"]["ind"])
    if etf is not None:
        ind[4] = etf
    key, conf, gauge = market(ind)
    out.append("MARKET %s \u00b7 %s \u00b7 %s" % (VERDICT_RU[key], conf, gauge))
    out.append("VERDICT|MARKET|7d|%s|\u2014|\u2014|%s|%s @ %s" % (VERDICT_RU[key], conf if "/" in conf else "\u2014",
                                                       px(rec["btc"]["p"], 2), rec["freeze"]))
    return out, problems, sized


# ------------------------------------------------------------------ scale: a verdict's range

def parse_item(text):
    m = re.fullmatch(r"([A-Z0-9]+)(?:@([0-9T:\-]+Z?))?(?::([0-9,\-]+))?", text)
    if not m:
        raise ValueError("item: %s" % text)
    dates = [date.fromisoformat(d) for d in m.group(3).split(",")] if m.group(3) else []
    at = datetime.fromisoformat(m.group(2).replace("Z", "+00:00")) if m.group(2) else None
    if at is not None and at.tzinfo is None:
        at = at.replace(tzinfo=timezone.utc)
    return m.group(1), at, dates, bool(m.group(2)) and "T" not in m.group(2)


def scale_lines(rec, items, net):
    """Per item: the range in per cent (section 4) and, with @ISO, the move since that publication -- the frozen
    price over the close of that hour -- and its age."""
    out = []
    freeze = datetime.fromisoformat(rec["freeze"].replace("Z", "+00:00"))
    fms = ms_of(freeze)
    prices = rec.get("prices") or {}
    for text in items:
        sym, at, dates, day_only = parse_item(text)
        try:
            rows = klines(net, sym, "1d", 400)
            sc = scale_of([r[:5] for r in rows if r[5] < fms], dates)
            if sc is None:
                out.append("%s: unread (short history)" % sym)
                continue
            line = "%s: \u2248 \u00b1%.1f%% \u00b7 range %.1f\u2026%.1f%% (%s) \u00b7 ordinary %.2f%% \u00b7 two-day %.2f%%/%.2f%%" % (
                sym, sc["lo"], sc["lo"], sc["hi"], ("two-day stands in, %d instances" % sc["n"]) if sc["stand_in"]
                else "%d instances" % sc["n"], sc["ordinary"], sc["two_med"], sc["two_q75"])
            p = prices.get(sym)
            if at is not None and p:
                h = (klines_at(net, sym, ms_of(at), "1d", 1) if day_only
                     else klines_at(net, sym, ms_of(at.replace(minute=0, second=0, microsecond=0))))
                if h:
                    age = (freeze - at).total_seconds()
                    line += " \u00b7 \u0441 \u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 %s%% (%s)" % (
                        pct((p / h - 1) * 100), "%d \u0434\u043d." % (age // 86400) if age >= 86400 else
                        "%d \u0447" % (age // 3600) if age >= 3600 else "<1 \u0447")
            out.append(line)
        except Exception as exc:
            out.append("%s: unread %s" % (sym, exc.__class__.__name__))
    return out


def klines_at(net, sym, start_ms, interval="1h", field=4):
    """Section 4's reference of a publication: field 4 of its hour's row, or field 1 of its day's where the record has
    no time."""
    rows = net.json(FAPI + "/fapi/v1/klines?symbol=%s&interval=%s&startTime=%d&limit=1" % (sym, interval, start_ms))
    return float(rows[0][field]) if rows else None


# ------------------------------------------------------------------ check: the answer before it leaves

NUM = r"[0-9]+(?:\.[0-9]+)?"


def parse_cards(answer):
    """Every card of the best-trades section: rank, tier, side, coin, kind and its printed lines."""
    cards, cur = [], None
    for line in answer.splitlines():
        m = re.match(r"\*\*(\d+)\. (\u2b50 STRONG \u00b7 )?(\U0001f534 \u0428\u041e\u0420\u0422|\U0001f7e2 \u041b\u041e\u041d\u0413) ([A-Z0-9]+)\*\*", line)
        if m:
            cur = dict(rank=int(m.group(1)), tier="STRONG" if m.group(2) else "\u041f\u0415\u0420\u0421\u041f",
                       side=-1 if "\u0428\u041e\u0420\u0422" in m.group(3) else 1, coin=m.group(4), lines=[], kind=None)
            cards.append(cur)
            continue
        if line.startswith("# "):
            cur = None
        if cur is not None:
            cur["lines"].append(line)
            if line.startswith("\u26a1"):
                cur["kind"] = "now"
            elif line.startswith("\u23f3"):
                cur["kind"] = "wait"
    return cards


def spans(line):
    return re.findall(r"`([^`]*)`", line)


def check(rec, answer, log_text, state, owner, index_html):
    """The mechanical half of methodology sections 7 and 14: (passed, failed) lines."""
    ok, bad = [], []

    def c(label, cond, detail=""):
        (ok if cond else bad).append(label + ("" if cond or not detail else ": " + detail))
    lines = answer.splitlines()
    breaks = sum(1 for l in lines if l == BREAK)
    c("three messages: two break lines", breaks == 2, "%d" % breaks)
    low = answer.lower()
    found = [w for w in BANNED if w in low]
    c("no banned phrase", not found, ", ".join(found))
    plain = re.sub(r"`[^`]*`", "", answer)
    ascii_groups = re.findall(r"(?<![\d.,])\d{1,3}(?: \d{3})+(?![\d])", plain)
    c("no number grouped with an ASCII space", not ascii_groups, ", ".join(ascii_groups[:5]))
    long_bare = [n for n in re.findall(r"(?<![\w.,\u00a0])(\d{4,})(?![\w%])", plain)
                 if not re.match(r"^(19|20)\d\d$", n)]
    c("every number of four or more digits grouped with U+00A0", not long_bare, ", ".join(long_bare[:5]))
    if rec["gate"] != 0:
        c("the gate failed: its sentence prints", GATE_SENTENCE in answer)
        c("the gate failed: no level prints", "$`" not in answer)
        return ok, bad
    head = rec.get("head") or []
    c("the head's two lines are the press's", len(head) == 2 and head[0] in lines and head[1] in lines)
    cards = parse_cards(answer)
    by = {(base_name(cd["sym"]), cd["side"]): cd for cd in rec["cards"]}
    ranks = [cd["rank"] for cd in cards]
    c("cards numbered 1..n in order", ranks == list(range(1, len(cards) + 1)), str(ranks))
    rows = []
    for card in cards:
        cd = by.get((card["coin"], card["side"]))
        label = "card %d %s" % (card["rank"], card["coin"])
        if cd is None:
            c(label + ": a card of the press", False)
            continue
        c(label + ": not refused by the press", not cd["refusal"], cd["refusal"] or "")
        c(label + ": its kind is the press's", card["kind"] == cd["kind"], "%s/%s" % (card["kind"], cd["kind"]))
        p = cd["places"]
        text = "\n".join(card["lines"])
        want = {"anchor": px(cd["anchor"], p), "stop": px(cd["stop"], p), "target": px(cd["target"], p)}
        if cd["kind"] == "now":
            want.update(void=px(cd["void"], p), exit=px(cd["exit_level"], p))
        got = set(sum((spans(l) for l in card["lines"]), []))
        missing = [k for k, v in want.items() if v not in got]
        c(label + ": every level the press's", not missing, ", ".join("%s %s" % (k, want[k]) for k in missing))
        warns = [l for l in card["lines"] if l.startswith("\u26a0\ufe0f")]
        warn = bool(warns)
        unsaid = [w for w in cd.get("warn") or [] if not any(w in l for l in warns)]
        c(label + ": the press's warning prints", not unsaid, " \u00b7 ".join(unsaid))
        rows.append(dict(rank=card["rank"], tier=card["tier"], sym=cd["sym"], side=card["side"],
                         flags={"cut"} if warn else set(), text=text, cd=cd))
    if rows and owner:
        consts = rec.get("consts") or {}
        g = {"STRONG": 0, "\u041f\u0415\u0420\u0421\u041f": 0}
        for r in rows:
            if r["cd"]["refusal"]:
                continue
            g[r["tier"]] += 1
            sz = size_card(r["cd"], r["tier"], g[r["tier"]], bool(r["flags"]), owner, consts)
            missing = [l for l in money_lines(r["cd"], sz) if l not in r["text"]]
            c("card %d: money lines the ladder's" % r["rank"], not missing, " | ".join(missing))
    main = [l for l in lines if l.startswith("\u26a1 **\u0412\u043e\u0439\u0442\u0438 \u0441\u0435\u0439\u0447\u0430\u0441:**") or l.startswith("\u23f3 **\u0416\u0434\u0430\u0442\u044c \u0441\u0438\u0433\u043d\u0430\u043b\u0430:**")]
    now_names = " \u00b7 ".join("%s %s" % (cd["coin"], SIDE_RU[cd["side"]]) for cd in cards if cd["kind"] == "now") or "\u043d\u0435\u0442"
    wait_names = " \u00b7 ".join("%s %s" % (cd["coin"], SIDE_RU[cd["side"]]) for cd in cards if cd["kind"] == "wait") or "\u043d\u0435\u0442"
    c("\u0413\u041b\u0410\u0412\u041d\u041e\u0415 names every \u26a1 card in rank order", ("\u26a1 **\u0412\u043e\u0439\u0442\u0438 \u0441\u0435\u0439\u0447\u0430\u0441:** " + now_names) in main)
    c("\u0413\u041b\u0410\u0412\u041d\u041e\u0415 names every \u23f3 card in rank order", ("\u23f3 **\u0416\u0434\u0430\u0442\u044c \u0441\u0438\u0433\u043d\u0430\u043b\u0430:** " + wait_names) in main)
    for name, block in (("\u0421\u0427\u0401\u0422 \u0421\u0418\u0421\u0422\u0415\u041c\u042b", rec["score"]), ("the world table", rec["blocks"]["world"]),
                        ("\u0414\u0415\u0420\u0418\u0412\u0410\u0422\u0418\u0412\u042b", rec["blocks"]["deriv"]), ("\u041f\u041e\u0417\u0418\u0426\u0418\u0418", rec["blocks"]["positions"]),
                        ("the ETF table", [] if rec["etf"].get("missing") else rec["blocks"]["etf"])):
        missing = [b for b in block if b not in lines]
        c("%s prints the press's lines" % name, not missing, " | ".join(missing[:2]))
    mp = rec["btc"].get("map")
    if mp:
        allowed = {usd(v) for v in [lv["price"] for lv in mp["levels"]] + mp["corridor"] + [mp["bull"], mp["bear"], mp["p"]]
                   + [z[k] for z in mp["zones"] for k in ("lo", "hi")]}
        sect, on = [], False
        for l in lines:
            if l.startswith("# "):
                on = l.startswith("# \u20bf BTC")
            elif on:
                sect.append(l)
        found_prices = re.findall(r"(?<![\d.])(\d{1,3}(?:\u00a0\d{3})+|\d{4,})(?![\d.%])", "\n".join(sect))
        stray = [v for v in found_prices if v not in allowed]
        c("every BTC price is the map's", bool(sect) and not stray, ", ".join(stray[:4]) or "no BTC section")
    m = rec["market"]
    words = {VERDICT_RU[market([*m["ind"][:4], e, *m["ind"][5:]])[0]] for e in
             (["red", "white", "green", "unread"] if not rec["etf"]["stands"] else [m["ind"][4]])}
    printed = [l for l in lines if l.startswith("\U0001f30d **\u0420\u044b\u043d\u043e\u043a:**")]
    c("the market word is the count's", bool(printed) and any(w.lower() in printed[0].lower() for w in words),
      printed[0] if printed else "no \u00ab\U0001f30d \u0420\u044b\u043d\u043e\u043a:\u00bb line")
    if log_text is not None:
        card_lines = [l for l in log_text.splitlines() if l.startswith("CARD|")]
        c("one CARD line per card", len(card_lines) == len(cards), "%d/%d" % (len(card_lines), len(cards)))
        c("CARD lines in rank order", [l.split("|")[3] for l in card_lines] == [str(r) for r in ranks])
        c("one VERDICT|MARKET line", sum(1 for l in log_text.splitlines() if l.startswith("VERDICT|MARKET|")) == 1)
    if state is not None:
        freeze_day = rec["freeze"][:10]
        passed = [h.get("id") for h in state.get("horizon") or [] if str(h.get("d", "9999"))[:10] < freeze_day]
        c("the state holds no passed date", not passed, ", ".join(map(str, passed[:5])))
        trade = [k for k in ("trades", "positions", "fills", "book", "cards") if k in state]
        c("the state holds no trade object", not trade, ", ".join(trade))
    del index_html
    return ok, bad


# ------------------------------------------------------------------ state: the file the trader never opens

def sec6_md5(meth_text):
    """The digest of `sed -n '/^## 6\\./,/^## 7\\./p' ANALYST-INSTRUCTIONS.md | md5sum` (methodology section 6a)."""
    lines = meth_text.split("\n")
    start = next((i for i, l in enumerate(lines) if re.match(r"## 6\.", l)), None)
    if start is None:
        return None
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"## 7\.", lines[i])), len(lines) - 1)
    return hashlib.md5(("\n".join(lines[start:end + 1]) + "\n").encode("utf-8")).hexdigest()


def state_write(state, rec, payload_c):
    """Section 11's lifecycle at step 3, and `oi` and `regime` from this press: (state, deleted ids)."""
    day = rec["freeze"][:10]
    horizon = state.get("horizon") or []
    deleted = [h.get("id") for h in horizon if str(h.get("d", ""))[:10] < day]
    state["horizon"] = [h for h in horizon if str(h.get("d", ""))[:10] >= day]
    state["d"], state["ts"] = day, rec["freeze"]
    state["oi"] = {r["s"][:-4] if r["s"].endswith("USDT") else r["s"]: {"ts": rec["freeze"], "oi": r["oi"]}
                   for r in payload_c if r.get("oi") is not None}
    reg, mp = rec.get("regime"), rec["btc"].get("map")
    if reg:
        regime = {"ts": rec["freeze"], "word": VERDICT_RU[rec["market"]["word"]], "btc": rec["btc"]["p"]}
        regime.update({k: round(v, 2) for k, v in reg["state"].items()})
        if mp:
            regime.update(cond_dn=round(mp["bull"], 2), cond_up=round(mp["bear"], 2))
        state["regime"] = regime
    return state, deleted


def state_view(state, rec, sec6):
    """What the trader checks against the file after the hunt (items 91, 99 and 104), in a few lines."""
    freeze = datetime.fromisoformat(rec["freeze"].replace("Z", "+00:00"))
    lo, hi = (freeze - timedelta(hours=24)).date(), (freeze + timedelta(days=7)).date()
    out = ["STATE v%s \u00b7 d %s \u00b7 ts %s \u00b7 sec6_md5 now %s" % (state.get("v"), state.get("d"), state.get("ts"), sec6)]
    hz = state.get("horizon") or []
    inside = [h for h in hz if lo <= date.fromisoformat(str(h.get("d"))[:10]) <= hi] if hz else []
    out.append("horizon %d \u00b7 in the window %d:" % (len(hz), len(inside)))
    out += ["  %s \u00b7 %s \u00b7 %s%s \u00b7 %s \u00b7 %s" % (h.get("id"), h.get("sym") or "\u2014", h.get("d"), " " + h["t"] if h.get("t") else "",
                                            h.get("dclass"), h.get("cls")) for h in sorted(inside, key=lambda h: str(h.get("d")))]
    sw = state.get("sweeps") or {}

    def age(d):
        try:
            return (freeze.date() - date.fromisoformat(str(d)[:10])).days
        except ValueError:
            return None
    for lane in ("horizon", "coins"):
        rows = sw.get(lane) or {}
        stale = ["%s(%s%s)" % (k, "%sd" % age(v.get("d")) if age(v.get("d")) else "",
                               ",md5" if v.get("sec6_md5") and v.get("sec6_md5") != sec6 else "")
                 for k, v in sorted(rows.items()) if isinstance(v, dict) and (age(v.get("d")) or
                                                                              (v.get("sec6_md5") and v.get("sec6_md5") != sec6))]
        out.append("lanes %s: %d \u00b7 read this run %d \u00b7 not: %s" % (lane, len(rows), len(rows) - len(stale),
                                                                  " ".join(stale) or "none"))
    un = sw.get("unlock") or {}
    by = {}
    for k, v in sorted(un.items()):
        if isinstance(v, dict):
            by.setdefault(v.get("status"), []).append((k, v))
    old = [k for k, v in un.items() if isinstance(v, dict) and str(v.get("d", ""))[:10] < rec["freeze"][:10]]
    out.append("unlock: next %s \u00b7 no cliff %d \u00b7 not covered %s \u00b7 refused %s \u00b7 read before this run: %s" % (
        " ".join("%s %s %s%% %s" % (k, v.get("ud"), v.get("pct"), v.get("to")) for k, v in by.get("next", [])) or "none",
        len(by.get("no cliff", [])), " ".join(k for k, _ in by.get("not covered", [])) or "none",
        " ".join(k for k, _ in by.get("refused", [])) or "none", " ".join(sorted(old)) or "none"))
    disc = sw.get("discovery") or {}
    today = [k for k, v in disc.items() if isinstance(v, dict) and str(v.get("d", ""))[:10] == rec["freeze"][:10]]
    out.append("discovery: searched this run %d \u00b7 not: %s" % (len(today), " ".join(sorted(set(disc) - set(today))) or "none"))
    return out


def state_items(state, rec, meth_text, list_bases):
    """Methodology section 7's items 91, 99 and 104 as the file shows them, one line each: what is short."""
    day, sw = rec["freeze"][:10], state.get("sweeps") or {}
    hz, un, disc = sw.get("horizon") or {}, sw.get("unlock") or {}, sw.get("discovery") or {}
    sec6 = sec6_md5(meth_text)
    late = [lane for lane in ("outside-list", "exchange-info") if str((hz.get(lane) or {}).get("ts", "")) < rec["freeze"]]
    out = ["item 99: " + ("both exchange reads after the freeze" if not late else "short: " + " ".join(late))]
    window, material = radar.cut_window(meth_text), radar.cut_material(meth_text)
    edge = (datetime.fromisoformat(rec["freeze"].replace("Z", "+00:00")) + timedelta(days=window)).isoformat()
    unread = [b for b in list_bases if str((un.get(b) or {}).get("d", ""))[:10] < day]
    cliffs = sorted("%s %s %s%%" % (k, str(v.get("ud"))[:10], v.get("pct")) for k, v in un.items() if isinstance(v, dict)
                    and v.get("status") == "next" and fnum(v.get("pct")) is not None and fnum(v["pct"]) >= material
                    and rec["freeze"] <= str(v.get("ud", "")) <= edge)
    blind = sorted(k for k, v in un.items() if isinstance(v, dict) and v.get("status") in ("refused", "not covered"))
    out.append("item 104: list coins without this run's unlock read: %s \u00b7 cliffs at or above %s%% in the window, their "
               "longs closed: %s \u00b7 refused or not covered, a long needs its search: %s" % (
                   " ".join(unread) or "none", material, " \u00b7 ".join(cliffs) or "none", " ".join(blind) or "none"))
    md5 = sorted(k for lane in ("horizon", "coins") for k, v in (sw.get(lane) or {}).items()
                 if isinstance(v, dict) and v.get("sec6_md5") and v.get("sec6_md5") != sec6)
    nosearch = sorted(b for b in list_bases if str((disc.get(b) or {}).get("d", ""))[:10] != day)
    out.append("item 91: lanes read under another text: %s \u00b7 list coins without this run's discovery search: %s \u00b7 "
               "exchange reads short: %s \u00b7 unlock reads short: %s \u2014 the line \u00ab\u26a0\ufe0f \u041f\u043e\u0438\u0441\u043a \u0441\u043e\u0431\u044b\u0442\u0438\u0439 \u043d\u0435\u043f\u043e\u043b\u043d\u044b\u0439\u00bb names them, "
               "with the lanes the view shows unread" % (" ".join(md5) or "none", " ".join(nosearch) or "none",
                                                          " ".join(late) or "none", " ".join(unread) or "none"))
    return out


# ------------------------------------------------------------------ the command line

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    mode = argv.pop(0) if argv and argv[0] in ("brief", "final", "scale", "check", "state", "hunter") else "press"
    ap = argparse.ArgumentParser(prog="press.py " + mode)
    ap.add_argument("--tree", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if mode == "press":
        ap.add_argument("--now", default=None)
    if mode in ("final", "scale", "check", "state", "hunter"):
        ap.add_argument("stem")
    if mode == "state":
        ap.add_argument("--write", action="store_true")
    if mode == "scale":
        ap.add_argument("items", nargs="+")
    if mode == "check":
        ap.add_argument("answer")
        ap.add_argument("log", nargs="?")
    a = ap.parse_args(argv)
    tree = os.path.abspath(a.tree)
    if mode == "press":
        now = datetime.fromisoformat(a.now.replace("Z", "+00:00")) if a.now else None
        try:
            rec = press(tree, now)
        except (OSError, ValueError) as exc:
            print("press: payload unread %s" % exc.__class__.__name__, flush=True)
            return 4
        digest, size = write_press(tree, rec)
        print("press: stem=%s gate=%s cards=%d refused=%d reads=%d seconds=%s brief_bytes=%d sha256=%s %s" % (
            rec["stem"], rec["gate"], sum(1 for cd in rec["cards"] if not cd["refusal"]), len(rec["refused"]),
            rec["reads"], rec["seconds"], size, digest[:12], " ".join("%s=%s" % (k, v.replace(" ", "_"))
                                                                      for k, v in sorted(rec["lanes"].items()))),
              flush=True)
        return 0
    if mode == "brief":
        stem = newest_press(tree, datetime.now(timezone.utc))
        if stem is None:
            try:
                rec = press(tree)
            except (OSError, ValueError) as exc:
                print("press: payload unread %s" % exc.__class__.__name__, flush=True)
                return 4
            write_press(tree, rec)
            stem = rec["stem"]
        with open(os.path.join(tree, PRESS_DIR, stem + ".md"), encoding="utf-8") as fh:
            sys.stdout.write(fh.read())
        return 0
    rec = load_press(tree, a.stem)
    if mode == "hunter":
        print("\n".join(rec["hunter"].splitlines()[3:]), flush=True)
        return 0
    owner = read_owner(tree)
    with open(os.path.join(tree, "index.html"), encoding="utf-8") as fh:
        index_html = fh.read()
    if mode == "final":
        try:
            rows, etf = parse_final(sys.stdin.read())
        except ValueError as exc:
            print("final: %s" % exc, flush=True)
            return 2
        if owner is None or not owner.get("card"):
            print("final: \u00ab\u041c\u0430\u0440\u0436\u0430: \u043d\u0435\u0442 \u0434\u0430\u043d\u043d\u044b\u0445\u00bb \u2014 analyst/owner.json card unread", flush=True)
            return 1
        out, problems, _ = final(rec, rows, etf, owner, index_html)
        print("\n".join(problems + out), flush=True)
        return 1 if problems else 0
    if mode == "scale":
        print("\n".join(scale_lines(rec, a.items, Net())), flush=True)
        return 0
    if mode == "state":
        path = os.path.join(tree, "analyst", "state.json")
        try:
            with open(path, encoding="utf-8") as fh:
                state = json.load(fh)
        except (OSError, ValueError):
            print("state: analyst/state.json unreadable \u2014 the run stops in one line (contract section 4b)", flush=True)
            return 1
        if a.write:
            state, deleted = state_write(state, rec, read_payload(tree)[1])
            common.atomic_write(path, json.dumps(state, ensure_ascii=False, indent=1) + "\n", mode=0o644)
            print("state: written \u00b7 deleted %d: %s" % (len(deleted), " ".join(map(str, deleted)) or "none"))
        with open(os.path.join(tree, "ANALYST-INSTRUCTIONS.md"), encoding="utf-8") as fh:
            meth = fh.read()
        bases = [base_name(r["s"]) for r in read_payload(tree)[1] if r["s"] != "BTCUSDT"]
        print("\n".join(state_view(state, rec, sec6_md5(meth)) + ([] if a.write else state_items(state, rec, meth, bases))),
              flush=True)
        return 0
    with open(a.answer, encoding="utf-8") as fh:
        answer = fh.read()
    log_text = None
    if a.log:
        with open(a.log, encoding="utf-8") as fh:
            log_text = fh.read()
    elif ANSWER_MARK in answer:
        # A day log (section 12): the answer as sent, then the appendix that carries the scoring lines.
        log_text = answer
        answer = answer.split(ANSWER_MARK, 1)[1].split(APPENDIX_MARK, 1)[0].strip("\n") + "\n"
    try:
        with open(os.path.join(tree, "analyst", "state.json"), encoding="utf-8") as fh:
            state = json.load(fh)
    except (OSError, ValueError):
        state = None
    ok, bad = check(rec, answer, log_text, state, owner, index_html)
    for line in bad:
        print("FAIL " + line)
    print("check: %d passed %d failed" % (len(ok), len(bad)), flush=True)
    return 1 if bad or not ok else 0


if __name__ == "__main__":
    sys.exit(main())
