#!/usr/bin/env python3
"""The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
TZ-62 B2, TZ-64 B4, TZ-65 B1, TZ-69 B1): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's,
TZ-57 §12.8's, TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's, TZ-64's, TZ-65's and TZ-69's changed and new ones, each printing
`section <X>: checks <n> failed <m>`, then the total.

    python3 vps/selftest.py

Exit non-zero on any failure and on any section that compared nothing (inv. 22).
Offline: every fixture is built here or read from the checkout this file sits in.
"""
import array
import contextlib
import copy
import io
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import tracemalloc
import types
import urllib.error
import urllib.parse
import zipfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import announce  # noqa: E402
import book  # noqa: E402
import bot  # noqa: E402
import cleanup  # noqa: E402
import common  # noqa: E402
import etf  # noqa: E402
import exchange  # noqa: E402
import paper  # noqa: E402
import run  # noqa: E402
import stop  # noqa: E402
import writer  # noqa: E402

MiB = common.MiB


class Section:
    def __init__(self, name):
        self.name, self.checks, self.failed = name, 0, 0

    def check(self, label, ok):
        self.checks += 1
        if not ok:
            self.failed += 1
            sys.stderr.write("FAIL section %s: %s\n" % (self.name, label))
        return ok


def checkout_tokens():
    with open(os.path.join(REPO, "index.html"), encoding="utf-8") as fh:
        return common.cut_tokens(fh.read())


# --- A: cut_tokens on the checkout's index.html ----------------------------------
def section_a(s):
    rows = checkout_tokens()
    s.check("rows > 0", len(rows) > 0)
    for row in rows:
        s.check("symbol %s matches ^[A-Z0-9]+USDT$" % row["s"], re.fullmatch(r"[A-Z0-9]+USDT", row["s"]) is not None)
    names = [row["name"] for row in rows]
    s.check("names unique", len(names) == len(set(names)))


# --- B: the writer on synthetic sources, judged by the gate ----------------------
def synthetic_sources(symbols):
    ticker = []
    for k, sym in enumerate(symbols + ["ZZZUSDT"]):
        ticker.append({"symbol": sym, "priceChange": "1.25", "priceChangePercent": "1.%03d" % k,
                       "weightedAvgPrice": "100.10", "lastPrice": "100.%02d" % (k % 100), "lastQty": "1.000",
                       "openPrice": "99.25", "highPrice": "110.25", "lowPrice": "90.75", "volume": "1000.000",
                       "quoteVolume": "100500.%02d" % (k % 100), "openTime": 1, "closeTime": 2, "firstId": 1,
                       "lastId": 2, "count": 1})
    premium = [{"symbol": sym, "markPrice": "100.60000000", "indexPrice": "100.50000000",
                "estimatedSettlePrice": "100.40000000", "lastFundingRate": "0.00010000",
                "interestRate": "0.00010000", "nextFundingTime": 0, "time": 0} for sym in symbols]
    oi = {sym: {"openInterest": "1234.5", "symbol": sym, "time": 0} for sym in symbols}
    return ticker, premium, oi


def section_b(s):
    tmp = tempfile.mkdtemp(prefix="vps-selftest-b.")
    try:
        os.makedirs(os.path.join(tmp, "analyst"))
        shutil.copy2(os.path.join(REPO, "index.html"), os.path.join(tmp, "index.html"))
        shutil.copy2(os.path.join(REPO, "analyst", "live-gate.sh"), os.path.join(tmp, "analyst", "live-gate.sh"))
        symbols = writer.payload_symbols(tmp)
        tokens = [row["s"] for row in checkout_tokens()]
        s.check("c symbols are BTCUSDT then tokens[] in order", symbols == ["BTCUSDT"] + tokens)
        ticker, premium, oi = synthetic_sources(symbols)
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        payload = writer.build_payload(ticker, premium, oi, symbols, ts)
        s.check("top-level keys exactly c n src ts x", list(payload) == ["c", "n", "src", "ts", "x"])
        s.check("c row keys exactly chg fr h l mark oi p qv s",
                all(list(row) == ["chg", "fr", "h", "l", "mark", "oi", "p", "qv", "s"] for row in payload["c"]))
        s.check("n is len(c)", payload["n"] == len(payload["c"]) == len(symbols))
        s.check("src is fapi", payload["src"] == "fapi")
        s.check("ts is UTC YYYY-MM-DDTHH:MM:SS+00:00",
                re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00", payload["ts"]) is not None)
        s.check("x is the bulk ticker verbatim, in served order", payload["x"] == ticker)
        s.check("p h l chg qv come from the ticker row of the same symbol",
                all(row["p"] == t["lastPrice"] and row["h"] == t["highPrice"] and row["l"] == t["lowPrice"]
                    and row["chg"] == t["priceChangePercent"] and row["qv"] == t["quoteVolume"]
                    for row, t in zip(payload["c"], ticker)))
        try:
            writer.build_payload(ticker, premium[1:], oi, symbols, ts)
            built = True
        except writer.BuildError:
            built = False
        s.check("a symbol missing from a source builds no payload", not built)

        writer.write_payload(tmp, payload)
        s.check("the gate passes the writer's payload: exit 0", writer.run_gate(tmp) == 0)
        short = copy.deepcopy(payload)
        short["c"] = [row for row in short["c"] if row["s"] != tokens[0]]
        short["n"] = len(short["c"])
        writer.write_payload(tmp, short)
        s.check("one tokens[] symbol removed from c: exit 5", writer.run_gate(tmp) == 5)
        long_n = copy.deepcopy(payload)
        long_n["n"] = len(long_n["c"]) + 1
        writer.write_payload(tmp, long_n)
        s.check("n one too large: exit 4", writer.run_gate(tmp) == 4)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- C: atomic_write twice at one path, the second failing while serialising ------
def section_c(s):
    tmp = tempfile.mkdtemp(prefix="vps-selftest-c.")
    try:
        target = os.path.join(tmp, "artifact.json")
        common.atomic_write(target, {"run": 1})
        with open(target, encoding="utf-8") as fh:
            s.check("first write lands whole", json.load(fh) == {"run": 1})
        try:
            common.atomic_write(target, {"run": 2, "unserialisable": object()})
            raised = False
        except TypeError:
            raised = True
        s.check("second write re-raises", raised)
        s.check("target absent after the failed write", not os.path.exists(target))
        s.check("no temporary file left", os.listdir(tmp) == [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- D: TZ-54 §12.3's conversion, byte for byte -----------------------------------
D_INPUT = ("\u0412\u0440\u0435\u043c\u044f \u0430\u043d\u0430\u043b\u0438\u0437\u0430: 10:00 "
           "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 06:00 UTC \u00b7 02:00 ET \u00b7 Binance Futures\n"
           "\n"
           "# \u0420\u0415\u0416\u0418\u041c\n"
           "**\u0414\u0418\u0410\u041f\u0410\u0417\u041e\u041d** \u2014 \u0430\u043b\u044c\u0442\u044b "
           "\u0431\u0435\u0437 \u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f.\n"
           "## **\u0421\u0422\u0410\u0422\u0423\u0421** \u043e\u043a\n"
           "\n"
           "| \u041c\u043e\u043d\u0435\u0442\u0430 | \u0412\u0445\u043e\u0434 |\n"
           "|---|---|\n"
           "| SOL | $150 |\n"
           "\n"
           "R&D <\u0442\u0435\u0441\u0442> **\u043d\u0435** \u0437\u0430\u043a\u0440\u044b\u0442 **")
D_EXPECTED = ("\u0412\u0440\u0435\u043c\u044f \u0430\u043d\u0430\u043b\u0438\u0437\u0430: 10:00 "
              "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 06:00 UTC \u00b7 02:00 ET \u00b7 Binance Futures\n"
              "\n"
              "<b>\u0420\u0415\u0416\u0418\u041c</b>\n"
              "<b>\u0414\u0418\u0410\u041f\u0410\u0417\u041e\u041d</b> \u2014 \u0430\u043b\u044c\u0442\u044b "
              "\u0431\u0435\u0437 \u043d\u0430\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u0438\u044f.\n"
              "<b>\u0421\u0422\u0410\u0422\u0423\u0421 \u043e\u043a</b>\n"
              "\n"
              "<pre>| \u041c\u043e\u043d\u0435\u0442\u0430 | \u0412\u0445\u043e\u0434 |\n"
              "|---|---|\n"
              "| SOL | $150 |</pre>\n"
              "\n"
              "R&amp;D &lt;\u0442\u0435\u0441\u0442&gt; <b>\u043d\u0435</b> \u0437\u0430\u043a\u0440\u044b\u0442 **")


def section_d(s):
    got = "\n".join(bot.convert(D_INPUT))
    s.check("the expected block, byte for byte", got.encode("utf-8") == D_EXPECTED.encode("utf-8"))
    got_lines, want_lines = got.split("\n"), D_EXPECTED.split("\n")
    s.check("line count", len(got_lines) == len(want_lines))
    for k, want in enumerate(want_lines):
        s.check("line %d" % (k + 1), k < len(got_lines) and got_lines[k] == want)


# --- E: TZ-54 §12.3's chunking ------------------------------------------------------
def section_e(s):
    limit = 4000
    s.check("the chunk limit is the text limit minus 96", bot.CHUNK_LIMIT == limit)
    plain = "\n".join(("L%02d " % k) + "x" * 96 for k in range(50))
    chunks = bot.chunk(plain, limit)
    sizes = [c[0].count("\n") + 1 for c in chunks]
    s.check("fifty 100-character lines split 39 + 11", sizes == [39, 11])
    s.check("no line lost or reordered", "\n".join(c[0] for c in chunks) == plain)
    table = ["| %02d | " % k + "y" * 62 + " |" for k in range(15)]
    text = "\n".join(["P%02d " % k + "z" * 96 for k in range(30)] + table)
    chunks = bot.chunk(text, limit)
    holders = [c for c in chunks if "<pre>" in c[0]]
    s.check("one chunk holds the <pre> block", len(holders) == 1)
    s.check("the <pre> block within the limit is never split",
            len(holders) == 1 and holders[0][0].count("<pre>") == 1 and holders[0][0].count("</pre>") == 1
            and all(line in holders[0][0] for line in table))
    s.check("the block moved whole to the next chunk", [c[0].count("\n") + 1 for c in chunks][:1] == [30])
    s.check("its plain fallback is its source lines", holders and holders[0][1] == "\n".join(table))
    big = "\n".join("| %03d | " % k + "w" * 62 + " |" for k in range(100))
    chunks = bot.chunk(big, limit)
    s.check("a <pre> block longer than the limit is split at its line breaks",
            len(chunks) >= 2 and all(c[0].startswith("<pre>") and c[0].endswith("</pre>") for c in chunks))
    s.check("every split block within the limit", all(bot.visible_len(c[0]) <= limit for c in chunks))
    long_line = "v" * 9000
    chunks = bot.chunk(long_line, limit)
    s.check("a longer plain line is cut in its source text", "".join(c[1] for c in chunks) == long_line)
    s.check("every cut piece within the limit", all(bot.visible_len(c[0]) <= limit for c in chunks))
    s.check("blank chunks are dropped", bot.chunk("\n\n  \n", limit) == [])


# --- F: TZ-54 §12.4's owner filter ---------------------------------------------------
def section_f(s):
    owner, other, now = 4242, 4343, 1700000000

    def update(chat_type, chat_id, date, text):
        return {"update_id": 1, "message": {"chat": {"type": chat_type, "id": chat_id}, "date": date, "text": text}}

    rows = (
        ("private, owner, now, /start", update("private", owner, now, "/start"), "S2"),
        ("private, owner, now, S1", update("private", owner, now, common.S1), "request"),
        ("private, another id, now, /start", update("private", other, now, "/start"), "dropped"),
        ("private, owner, now - 601 s, /run", update("private", owner, now - 601, "/run"), "dropped"),
        ("group, owner's id, now, /run", update("group", owner, now, "/run"), "dropped"),
        ("private, owner, now, \u043f\u0440\u0438\u0432\u0435\u0442",
         update("private", owner, now, "\u043f\u0440\u0438\u0432\u0435\u0442"), "S8"),
        # TZ-60 §12.11: the owner's stop.
        ("private, owner, now, STOP", update("private", owner, now, "STOP"), "stop"),
        ("private, owner, now, \u0441\u0442\u043e\u043f",
         update("private", owner, now, "\u0441\u0442\u043e\u043f"), "stop"),
        ("private, owner, now, \u0421\u0422\u041e\u041f",
         update("private", owner, now, "\u0421\u0422\u041e\u041f"), "stop"),
        ("private, owner, now, ' Stop! '", update("private", owner, now, " Stop! "), "stop"),
        ("private, owner, now, /stop", update("private", owner, now, "/stop"), "stop"),
        ("private, owner, now, \u0441\u0442\u043e\u043f \u0430\u043d\u0430\u043b\u0438\u0437",
         update("private", owner, now, "\u0441\u0442\u043e\u043f \u0430\u043d\u0430\u043b\u0438\u0437"), "S8"),
        ("private, another id, now, STOP", update("private", other, now, "STOP"), "dropped"),
        ("private, owner, now - 601 s, STOP", update("private", owner, now - 601, "STOP"), "dropped"),
    )
    for label, upd, want in rows:
        s.check(label, bot.classify(upd, owner, now) == want)


# --- G: TZ-54 §12.5's matcher ---------------------------------------------------------
def section_g(s):
    lists = [("BTC", "BTCUSDT")] + [(row["name"], row["s"]) for row in checkout_tokens()]
    perps = [("PEPE", "1000PEPEUSDT"), ("S", "SUSDT")]
    rows = (
        ("Binance Will List Hyperliquid (HYPE) with Seed Tag Applied", ("list", "HYPE")),
        ("Binance Futures Will Launch USD\u24c8-Margined SUIUSDT Perpetual Contract", ("list", "SUI")),
        ("Introducing ETHFI on Binance Launchpool", ("none", None)),
        ("Binance Adds ARB/EUR Trading Pair", ("list", "ARB")),
        ("LITHIUM Network Airdrop Notice", ("none", None)),
        ("Binance Will List Pepe (PEPE)", ("perpetual", "PEPE")),
        ("Notice on S Token Migration", ("none", None)),
        ("Binance Will Delist Sonic (S)", ("perpetual", "S")),
    )
    for title, want in rows:
        s.check(title, announce.match_title(title, lists, perps) == want)


# --- H: TZ-54 §12.10's query and signature -------------------------------------------
def section_h(s):
    q = announce.query_string({"timestamp": 1700000000000, "topic": "com_announcement_en",
                               "random": "abc", "recvWindow": 5000})
    s.check("sorted query string", q == "random=abc&recvWindow=5000&timestamp=1700000000000&topic=com_announcement_en")
    s.check("RFC 4231 test case 2", announce.sign("Jefe", "what do ya want for nothing?")
            == "5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843")


# --- I: TZ-54 §12.9's verdict ---------------------------------------------------------
# The documented example response's fields with the two violations TZ-54 §12.9
# names (ipRestrict false, enablePortfolioMarginTrading true). The page itself
# answered this host with an AWS WAF challenge (report, Deviations).
EXAMPLE = {"ipRestrict": False, "createTime": 1698645219000, "enableReading": True, "enableWithdrawals": False,
           "enableInternalTransfer": False, "enableMargin": False, "enableFutures": False,
           "permitsUniversalTransfer": False, "enableVanillaOptions": False, "enableFixApiTrade": False,
           "enableFixReadOnly": True, "enableSpotAndMarginTrading": False, "enablePortfolioMarginTrading": True}


def section_i(s):
    s.check("the example response: REFUSED", announce.verdict(EXAMPLE) == "REFUSED")
    accepted = dict(EXAMPLE, ipRestrict=True, enablePortfolioMarginTrading=False)
    s.check("ipRestrict true, enablePortfolioMarginTrading false: ACCEPTED", announce.verdict(accepted) == "ACCEPTED")
    s.check("plus enableFoo true: REFUSED", announce.verdict(dict(accepted, enableFoo=True)) == "REFUSED")
    s.check("enableReading false: REFUSED", announce.verdict(dict(accepted, enableReading=False)) == "REFUSED")


# --- J: derive_limits, test_limits, start_limits and record_limits ------------------
# TZ-57 §12.4's base: the record's TZ-55 lines at 4c67ebe.
J_BASE = {"input_footprint_bytes": "466161664", "input_duration_s": "604.899672",
          "run_footprint_bytes": "322416640", "run_duration_s": "1088.339229"}
def section_j(s):
    s.check("derive_limits(400 MiB, 1200 s)", common.derive_limits(400 * MiB, 1200) == (637534208, 5400))
    s.check("derive_limits(100 MiB, 2100 s)", common.derive_limits(100 * MiB, 2100) == (167772160, 6000))
    # TZ-55 §12.4's four known answers, computed by the Architect.
    s.check("test_limits(466161664, 604.899672, 419430400)",
            common.test_limits(466161664, 604.899672, 419430400) == (704643072, 352321536, 352321536, 5400))
    s.check("test_limits(291307520, 604.899672, 1073741824)",
            common.test_limits(291307520, 604.899672, 1073741824) == (452984832, 452984832, 0, 5400))
    s.check("test_limits(466161664, 604.899672, 379584512)",
            common.test_limits(466161664, 604.899672, 379584512) == (704643072, 301989888, 402653184, 5400))
    low = common.test_limits(466161664, 604.899672, 209715200)
    s.check("test_limits(466161664, 604.899672, 209715200): memory_max 134217728", low[1] == 134217728)
    s.check("that memory_max is below the floor of 167772160, so D2 does not run",
            common.MEMORY_MAX_FLOOR_BYTES == 167772160 and low[1] < common.MEMORY_MAX_FLOOR_BYTES)
    # TZ-56 §12.2's four known answers, computed by the Architect.
    s.check("start_limits(535355392, 704643072)", common.start_limits(535355392, 704643072) == (452984832, 251658240))
    s.check("start_limits(240775168, 704643072)", common.start_limits(240775168, 704643072) == (167772160, 536870912))
    s.check("start_limits(209678336, 704643072)", common.start_limits(209678336, 704643072) == (167772160, 536870912))
    s.check("start_limits(2147483648, 704643072)", common.start_limits(2147483648, 704643072) == (704643072, 0))
    budget = 704643072
    for k in range(10):
        available = k * 4096 * MiB // 9
        memory_max, swap_max = common.start_limits(available, budget)
        s.check("start_limits(%d, %d) within [160 MiB, budget]" % (available, budget),
                common.MEMORY_MAX_FLOOR_BYTES <= memory_max <= budget and memory_max + swap_max == budget)
    # TZ-57 §12.4's five known answers, computed by the Architect.
    rows = ((None, None, None, (704643072, 5400)),
            ("C", "524288000", "1200", (788529152, 5400)),
            ("C", "400000000", "2500", (704643072, 6900)),
            ("K-oom", "704643072", "300", (1056964608, 5400)),
            ("K-timeout", "704643072", "5400", (704643072, 5400)))
    for product_class, footprint, duration, want in rows:
        record = dict(J_BASE)
        if product_class is not None:
            record.update(product_class=product_class, product_footprint_bytes=footprint,
                          product_duration_s=duration)
        s.check("record_limits: product block %s" % ("none" if product_class is None else
                                                      "%s, footprint %s, duration %s" % (product_class, footprint, duration)),
                common.record_limits(record) == want)


# --- K: cleanup's selection -----------------------------------------------------------
def section_k(s):
    now = 1700000000.0
    entries = [("e%02d" % h, now - h * 3600) for h in range(45)]
    entries += [("o15", now - 15 * 86400), ("o16", now - 16 * 86400), ("o20", now - 20 * 86400)]
    kept, removed = cleanup.select_records(entries, now)
    s.check("kept e00..e39", kept == ["e%02d" % h for h in range(40)])
    s.check("removed e40..e44, o15, o16, o20", removed == ["e%02d" % h for h in range(40, 45)] + ["o15", "o16", "o20"])


# --- L: redact with a planted value ---------------------------------------------------
def section_l(s):
    planted = "7000000001:planted-value/for+selftest"
    common.remember_secret(planted)
    for label, text in (("plain", "GET https://api.telegram.org/bot" + planted + "/getMe failed"),
                        ("URL-encoded", "url=" + urllib.parse.quote(planted, safe=""))):
        out = common.redact(text)
        s.check(label + ": <redacted> present", "<redacted>" in out)
        s.check(label + ": the value absent", planted not in out and "planted-value" not in out)


# --- M: the measurement record against the run unit and the manifest ----------------
def unit_value(path, key):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith(key + "="):
                return line.strip().split("=", 1)[1]
    return None


PRODUCT_KEYS = ("product_read_utc", "product_invocations", "product_killed", "product_not_admitted",
                "product_account_limited", "product_completed", "product_class", "product_run_utc",
                "product_memory_max_bytes", "product_memory_swap_max_bytes", "product_memory_peak_bytes",
                "product_memory_swap_peak_bytes", "product_footprint_bytes", "product_duration_s", "fits")


def section_m(s):
    record_path = os.path.join(HERE, "memory-record.txt")
    unit_path = os.path.join(HERE, "units", "crypto-run.service")
    manifest_path = os.path.join(HERE, "manifest")
    if not (os.path.exists(record_path) and os.path.exists(unit_path) and os.path.exists(manifest_path)):
        sys.stderr.write("section M: memory-record.txt, crypto-run.service or manifest absent\n")
        return
    r = common.read_record(record_path)
    n = {k: int(v) for k, v in r.items() if re.fullmatch(r"-?\d+", v)}
    with open(manifest_path, encoding="utf-8") as fh:
        listed = {line.strip() for line in fh if line.strip() and not line.startswith("#")}
    # TZ-55 §12.7's rule, which replaces TZ-54's.
    s.check("run_footprint_bytes = max(cgroup, kernel peak)",
            n["run_footprint_bytes"] == max(n["run_cgroup_footprint_bytes"], n["run_kernel_peak_bytes"]))
    s.check("host_free_bytes = mem_available + session_rss",
            n["host_free_bytes"] == n["mem_available_bytes"] + n["session_rss_bytes"])
    budget_in, memory_max, _, _ = common.test_limits(n["input_footprint_bytes"], r["input_duration_s"],
                                                     n["host_free_bytes"])
    s.check("memory_max_bytes = test_limits(input_footprint, input_duration, host_free)'s second term",
            n["memory_max_bytes"] == memory_max)
    # TZ-57 §12.8: the record's budget rule is common.record_limits, which replaces TZ-55's.
    budget, runtime_max = common.record_limits(r)
    s.check("budget_bytes = record_limits(record)[0]", n["budget_bytes"] == budget)
    s.check("runtime_max_s = record_limits(record)[1]", n["runtime_max_s"] == runtime_max)
    s.check("memory_swap_max_bytes = budget - memory_max",
            n["memory_swap_max_bytes"] == n["budget_bytes"] - n["memory_max_bytes"])
    s.check("hog_footprint_bytes >= hog_bytes > hog3_footprint_bytes / 2",
            n["hog_footprint_bytes"] >= n["hog_bytes"] and 2 * n["hog_bytes"] > n["hog3_footprint_bytes"])
    fits = r.get("fits")
    if fits is not None:
        s.check("fits present: every TZ-57 12.3 key present", all(k in r for k in PRODUCT_KEYS))
        killed, completed = n.get("product_killed"), n.get("product_completed")
        s.check("fits=no exactly when product_killed >= 1",
                (fits == "no") == (killed is not None and killed >= 1))
        s.check("fits=yes exactly when product_killed = 0 and product_completed >= 1",
                (fits == "yes") == (killed == 0 and completed is not None and completed >= 1))
        s.check("product_class is C under yes and a K- class under no",
                (fits == "yes" and r.get("product_class") == "C")
                or (fits == "no" and r.get("product_class") in ("K-oom", "K-timeout")))
        peaks = (n.get("product_memory_peak_bytes"), n.get("product_memory_swap_peak_bytes"))
        if None not in peaks:
            s.check("product_footprint_bytes = the sum of the two peaks",
                    n.get("product_footprint_bytes") == peaks[0] + peaks[1])
    # TZ-56 §12.6: the unit carries the floor and the budget's rest; each start sets its own pair.
    s.check("MemoryMax= equals MEMORY_MAX_FLOOR_BYTES",
            unit_value(unit_path, "MemoryMax") == str(common.MEMORY_MAX_FLOOR_BYTES))
    s.check("MemorySwapMax= equals budget_bytes - MEMORY_MAX_FLOOR_BYTES",
            unit_value(unit_path, "MemorySwapMax") == str(n["budget_bytes"] - common.MEMORY_MAX_FLOOR_BYTES))
    s.check("RuntimeMaxSec= equals runtime_max_s", unit_value(unit_path, "RuntimeMaxSec") == str(n["runtime_max_s"]))
    with open(unit_path, encoding="utf-8") as fh:
        unit_lines = [line.rstrip("\n") for line in fh]
    s.check("exactly one ExecStartPre=-+/usr/bin/python3 /srv/crypto-auto/vps/run.py --limits",
            unit_lines.count("ExecStartPre=-+/usr/bin/python3 /srv/crypto-auto/vps/run.py --limits") == 1)
    s.check("exactly one Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1",
            unit_lines.count("Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1") == 1)
    # TZ-57 §12.8: only the owner's button starts a run.
    s.check("vps/units/ holds no crypto-run.timer", not os.path.exists(os.path.join(HERE, "units", "crypto-run.timer")))
    s.check("the manifest names no crypto-run.timer", "crypto-run.timer" not in listed)


# --- N: the bot on a mock API: one undeliverable file holds nothing behind it ----
class MockApi(bot.Api):
    """Answers sendMessage like the Bot API: HTTP 400 for any text carrying the
    refused marker, a network error (status 0) for the cut marker, 200 otherwise."""
    REFUSED, CUT = "SELFTEST-REFUSED", "SELFTEST-CUT"

    def __init__(self):
        bot.Api.__init__(self, "selftest-token")
        self.sent = []

    def call(self, method, params, timeout=common.HTTP_TIMEOUT_S):
        text = params.get("text", "")
        self.sent.append((params.get("parse_mode"), text))
        if self.REFUSED in text:
            return 400, {"ok": False, "error_code": 400, "description": "Bad Request: selftest"}
        if self.CUT in text:
            return 0, {"description": "URLError"}
        return 200, {"ok": True, "result": {"message_id": len(self.sent)}}


def outbox_doc(directory, name, kind, text):
    with open(os.path.join(directory, name), "w", encoding="utf-8") as fh:
        json.dump({"kind": kind, "text": text, "created_ms": 1}, fh)


def section_n(s):
    saved = (common.OUTBOX_DIR, bot.CHUNK_SPACING_S)
    tmp = tempfile.mkdtemp(prefix="vps-selftest-n.")
    try:
        common.OUTBOX_DIR, bot.CHUNK_SPACING_S = tmp, 0
        refused, nxt = "1000-answer-1.json", "1001-notice-1.json"
        outbox_doc(tmp, refused, "answer", "first line\n" + MockApi.REFUSED + " <b>bad</b>")
        outbox_doc(tmp, nxt, "notice", "the next file")
        api = MockApi()
        with contextlib.redirect_stdout(io.StringIO()) as out:
            ran_through = bot.deliver_outbox(api, 4242)
        s.check("the refused file ends as <name>.dead", os.path.exists(os.path.join(tmp, refused + ".dead")))
        s.check("refused in both forms: HTML, then plain text",
                [mode for mode, text in api.sent if MockApi.REFUSED in text] == ["HTML", None])
        s.check("the next file is sent", any(text == "the next file" for _, text in api.sent)
                and not os.path.exists(os.path.join(tmp, nxt)))
        s.check("the pass ran through", ran_through is True)
        s.check("the outbox holds the .dead file alone", sorted(os.listdir(tmp)) == [refused + ".dead"])
        s.check("outbox_files() does not list it", bot.outbox_files() == [])
        s.check("logged once by name", out.getvalue().count(refused + " refused in both forms") == 1)
        # A network error keeps TZ-54's behaviour: the file is kept and the pass ends.
        for name in os.listdir(tmp):
            os.unlink(os.path.join(tmp, name))
        outbox_doc(tmp, "2000-answer-1.json", "answer", MockApi.CUT)
        outbox_doc(tmp, "2001-notice-1.json", "notice", "behind the cut")
        api = MockApi()
        with contextlib.redirect_stdout(io.StringIO()):
            ran_through = bot.deliver_outbox(api, 4242)
        s.check("network error: the pass ends", ran_through is False)
        s.check("network error: both files kept, no .dead",
                sorted(os.listdir(tmp)) == ["2000-answer-1.json", "2001-notice-1.json"])
        s.check("network error: the file behind it is not sent", not any("behind the cut" in t for _, t in api.sent))
    finally:
        common.OUTBOX_DIR, bot.CHUNK_SPACING_S = saved
        shutil.rmtree(tmp, ignore_errors=True)


# --- O: run.py with a stub claude and a stub writer on PATH --------------------------
STUB_CLAUDE = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["SELFTEST_O_CLAUDE_SAW"], "w") as fh:
    fh.write(os.environ.get("CLAUDE_CODE_OAUTH_TOKEN", "<absent>"))
with open(os.environ["SELFTEST_O_CLAUDE_SAW"] + "-pins", "w") as fh:
    json.dump({k: os.environ.get(k) for k in ("ANTHROPIC_DEFAULT_OPUS_MODEL", "ANTHROPIC_DEFAULT_SONNET_MODEL",
                                          "ANTHROPIC_DEFAULT_HAIKU_MODEL")}, fh)
json.dump({"type": "result", "subtype": "stub_subtype", "is_error": False, "result": os.environ["SELFTEST_O_RESULT"],
           "num_turns": 3, "duration_ms": 1234, "api_error_status": 418, "terminal_reason": "stub_terminal",
           "stop_reason": "stub_stop", "modelUsage": json.loads(os.environ.get("SELFTEST_O_MODELS", "{}")),
           "permission_denials": [],
           "usage": {"input_tokens": 11, "output_tokens": 22, "cache_read_input_tokens": 33,
                     "cache_creation_input_tokens": 44}, "total_cost_usd": 0.5}, sys.stdout)
"""
STUB_WRITER = """#!/usr/bin/env python3
import json, os
with open(os.environ["SELFTEST_O_WRITER_SAW"], "w") as fh:
    json.dump(dict(os.environ), fh)
"""


def _git(cwd, *args):
    return subprocess.run(["git", "-c", "user.name=selftest", "-c", "user.email=selftest@invalid"] + list(args),
                          cwd=cwd, capture_output=True, text=True).returncode


def o_fixtures(tmp, stub_claude, planted):
    """Section O's fixtures under tmp: bin/ with the given stub claude and the stub
    writer, creds/ holding the planted login, runtime/, outbox/, requests/ with one
    request, and a tree with a local origin. Returns (paths, tree, the push's exit)."""
    paths = {k: os.path.join(tmp, k) for k in ("bin", "creds", "runtime", "outbox", "requests")}
    for p in paths.values():
        os.makedirs(p)
    with open(os.path.join(paths["creds"], run.LOGIN_CREDENTIAL), "w") as fh:
        fh.write(planted)
    for name, body in (("claude", stub_claude), ("writer-stub.py", STUB_WRITER)):
        with open(os.path.join(paths["bin"], name), "w") as fh:
            fh.write(body)
        os.chmod(os.path.join(paths["bin"], name), 0o755)
    with open(os.path.join(paths["requests"], "1-bot-1.req"), "w") as fh:
        fh.write("{}")
    origin, tree = os.path.join(tmp, "origin.git"), os.path.join(tmp, "tree")
    _git(tmp, "init", "-q", "--bare", "-b", "main", origin)
    _git(tmp, "init", "-q", "-b", "main", tree)
    with open(os.path.join(tree, "README"), "w") as fh:
        fh.write("selftest\n")
    _git(tree, "add", "README")
    _git(tree, "commit", "-q", "-m", "init")
    _git(tree, "remote", "add", "origin", origin)
    return paths, tree, _git(tree, "push", "-q", "origin", "main")


def section_o(s):
    cmd = run.CLAUDE
    s.check("run.CLAUDE carries --model immediately followed by claude-opus-5-5",
            any(cmd[i] == "--model" and cmd[i + 1] == "claude-opus-5-5" for i in range(len(cmd) - 1)))
    s.check("run.CLAUDE carries --effort immediately followed by high",
            any(cmd[i] == "--effort" and cmd[i + 1] == "high" for i in range(len(cmd) - 1)))
    s.check("no element of run.CLAUDE equals opus", "opus" not in cmd)
    # TZ-66: each alias a subagent call can name is pinned to one full id.
    s.check("run.PINS resolves sonnet to claude-sonnet-5",
            run.PINS.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-sonnet-5")
    s.check("run.PINS resolves opus to run.MODEL", run.PINS.get("ANTHROPIC_DEFAULT_OPUS_MODEL") == run.MODEL)
    s.check("run.PINS resolves haiku to claude-haiku-4-5-20251001",
            run.PINS.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") == "claude-haiku-4-5-20251001")
    tmp = tempfile.mkdtemp(prefix="vps-selftest-o.")
    env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", run.LOGIN_ENV,
                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW", "SELFTEST_O_RESULT",
                "SELFTEST_O_MODELS") + tuple(run.PINS)
    saved_env = {k: os.environ.get(k) for k in env_keys}
    patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (run, "WRITER"), (run, "own_memory_max"),
               (run, "own_swap_max"), (run, "mem_available"), (run, "swap_free"), (run, "ADMISSION_POLL_S"),
               (run, "ADMISSION_MAX_S")]
    saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
    saved_term = signal.getsignal(signal.SIGTERM)
    try:
        planted = "sk-ant-oat01-selftest-planted-" + os.urandom(6).hex()
        decoy = "sk-ant-oat01-selftest-decoy-" + os.urandom(6).hex()
        paths, tree, pushed = o_fixtures(tmp, STUB_CLAUDE, planted)
        s.check("a local origin to fetch from", pushed == 0)

        claude_saw = os.path.join(tmp, "claude-saw")
        writer_saw = os.path.join(tmp, "writer-saw")
        os.environ.update({"PATH": paths["bin"] + os.pathsep + (saved_env["PATH"] or ""),
                           "CREDENTIALS_DIRECTORY": paths["creds"], "RUNTIME_DIRECTORY": paths["runtime"],
                           run.LOGIN_ENV: decoy,          # a value already in the unit's environment is not the login
                           "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": writer_saw,
                           # TZ-63: the stub's final message is an answer, opening with run's own head.
                           "SELFTEST_O_RESULT": run.ANSWER_HEAD + " SELFTEST-O-RESULT-TEXT",
                           # TZ-66: a value already in the unit's environment is not the pin.
                           "ANTHROPIC_DEFAULT_OPUS_MODEL": "selftest-decoy-opus",
                           "ANTHROPIC_DEFAULT_SONNET_MODEL": "selftest-decoy-sonnet",
                           "ANTHROPIC_DEFAULT_HAIKU_MODEL": "selftest-decoy-haiku",
                           "SELFTEST_O_MODELS": json.dumps({"claude-opus-5-5": {}, "claude-sonnet-5": {},
                                                            "claude-haiku-selftest": {}})})
        common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
        run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
        run.own_memory_max = run.own_swap_max = lambda: None
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = run.main(["--tree", tree])
        summary = out.getvalue()
        with open(claude_saw) as fh:
            seen_by_claude = fh.read()
        with open(writer_saw) as fh:
            writer_env = json.load(fh)
        s.check("the run answered: exit 0", code == 0)
        s.check("the stub claude sees CLAUDE_CODE_OAUTH_TOKEN equal to the planted credential", seen_by_claude == planted)
        s.check("the stub writer does not see CLAUDE_CODE_OAUTH_TOKEN", run.LOGIN_ENV not in writer_env)
        s.check("the stub writer holds neither value under any name",
                not any(planted in v or decoy in v for v in writer_env.values()))
        s.check("run.py put no login into its own environment", os.environ.get(run.LOGIN_ENV) == decoy)
        with open(claude_saw + "-pins") as fh:
            pins_seen = json.load(fh)
        s.check("the stub claude sees every pin of run.PINS, not the unit's own values", pins_seen == run.PINS)
        s.check("run.py put no pin into its own environment",
                os.environ.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "selftest-decoy-sonnet")
        for field, value in (("subtype", "stub_subtype"), ("api_error_status", "418"),
                             ("terminal_reason", "stub_terminal"), ("stop_reason", "stub_stop")):
            s.check("the summary carries %s=%s" % (field, value), (" %s=%s" % (field, value)) in summary)
        s.check("the summary never carries the result", "SELFTEST-O-RESULT-TEXT" not in summary)
        second = [l for l in summary.splitlines() if l.startswith("crypto-run: models=")]
        s.check("the second summary line names every id used, then the one outside run.PINS",
                len(second) == 1 and second[0].startswith(
                    "crypto-run: models=claude-haiku-selftest,claude-opus-5-5,claude-sonnet-5 "
                    "unpinned=claude-haiku-selftest denied_tools="))
        # TZ-56 §12.4: the third summary line carries the stub's usage and cost.
        third = [l for l in summary.splitlines() if l.startswith("crypto-run: memory_max=")]
        s.check("one third summary line", len(third) == 1)
        s.check("it carries input_tokens=11 output_tokens=22 cache_read_tokens=33 cache_creation_tokens=44 "
                "cost_usd=0.5", len(third) == 1 and third[0].endswith(
                    " input_tokens=11 output_tokens=22 cache_read_tokens=33 cache_creation_tokens=44 cost_usd=0.5"))
        s.check("the summary never carries the login", planted not in summary and decoy not in summary)
        s.check("the request was consumed first", "requests=1 " in summary and os.listdir(paths["requests"]) == [])
        answers = [n for n in os.listdir(paths["outbox"]) if "-answer-" in n]
        s.check("the answer went to the outbox", len(answers) == 1)

        # Admission (TZ-56 B2.2, §12.2), decided at once: one poll, no wait.
        run.ADMISSION_POLL_S, run.ADMISSION_MAX_S = 1, 0
        cases = ((512 * MiB, 64 * MiB, 256 * MiB, 128 * MiB, False, "SwapFree below memory.swap.max: refused"),
                 (512 * MiB, 128 * MiB, 256 * MiB, 128 * MiB, True, "SwapFree covering memory.swap.max: admitted"),
                 (128 * MiB, 4096 * MiB, 256 * MiB, 128 * MiB, False, "MemAvailable below memory.max: refused"),
                 (512 * MiB, 0, 256 * MiB, 0, True, "memory.swap.max 0: no swap condition"),
                 (512 * MiB, 0, 256 * MiB, "max", True, "memory.swap.max `max`: no swap condition"),
                 (512 * MiB, 0, 256 * MiB, None, True, "memory.swap.max absent: no swap condition"),
                 (256 * MiB + 64 * MiB, 4096 * MiB, 256 * MiB, 128 * MiB, True,
                  "MemAvailable = memory.max + 64 MiB: admitted"),
                 (256 * MiB + 64 * MiB - 1, 4096 * MiB, 256 * MiB, 128 * MiB, False,
                  "MemAvailable = memory.max + 64 MiB - 1: refused"))
        for available, free_swap, ceiling, swap_ceiling, want, label in cases:
            run.mem_available, run.swap_free = (lambda v=available: v), (lambda v=free_swap: v)
            run.own_memory_max, run.own_swap_max = (lambda v=ceiling: v), (lambda v=swap_ceiling: v)
            s.check(label, run.admit() == (want, 0))
    finally:
        for mod, name, value in saved_attrs:
            setattr(mod, name, value)
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        signal.signal(signal.SIGTERM, saved_term)
        shutil.rmtree(tmp, ignore_errors=True)


# --- P: the documented subscription, announce.act and common.request_run (TZ-57 §12.8) --
def command(sub_type, data):
    return json.dumps({"type": "COMMAND", "subType": sub_type, "data": data, "code": "00000000"})


class FakeSocket:
    """Hands out the given frames, then times out; records what is sent."""

    def __init__(self, frames, timeout_exc):
        self.frames, self.timeout_exc, self.sent, self.closed = list(frames), timeout_exc, [], False

    def settimeout(self, value):
        pass

    def recv(self):
        if not self.frames:
            raise self.timeout_exc()
        return self.frames.pop(0)

    def send(self, data):
        self.sent.append(data)

    def close(self):
        self.closed = True


def connect_on(frames):
    """Stream.connect() against a fake websocket module: (returned, sent, pending)."""
    fake = types.ModuleType("websocket")
    fake.WebSocketTimeoutException = type("WebSocketTimeoutException", (Exception,), {})
    sock = FakeSocket(frames, fake.WebSocketTimeoutException)
    fake.create_connection = lambda url, header=None, timeout=None: sock
    saved = sys.modules.get("websocket")
    sys.modules["websocket"] = fake
    try:
        stream = announce.Stream("selftest-key", "selftest-secret")
        with contextlib.redirect_stdout(io.StringIO()):
            returned = stream.connect()
    finally:
        if saved is None:
            sys.modules.pop("websocket", None)
        else:
            sys.modules["websocket"] = saved
    return returned, sock.sent, stream.pending


@contextlib.contextmanager
def spool_in(tmp, enabled):
    """common's state, spool, outbox and requests paths pointed at tmp, runs enabled
    or not there; restored on exit."""
    names = ("STATE_DIR", "SPOOL_DIR", "OUTBOX_DIR", "REQUESTS_DIR", "RUNS_ENABLED")
    saved = {name: getattr(common, name) for name in names}
    paths = {"STATE_DIR": os.path.join(tmp, "state"), "SPOOL_DIR": os.path.join(tmp, "spool")}
    paths.update(OUTBOX_DIR=os.path.join(paths["SPOOL_DIR"], "outbox"),
                 REQUESTS_DIR=os.path.join(paths["SPOOL_DIR"], "requests"),
                 RUNS_ENABLED=os.path.join(paths["STATE_DIR"], "runs-enabled"))
    for name in ("STATE_DIR", "OUTBOX_DIR", "REQUESTS_DIR"):
        os.makedirs(paths[name], exist_ok=True)
    if enabled:
        open(paths["RUNS_ENABLED"], "w").close()
    elif os.path.exists(paths["RUNS_ENABLED"]):
        os.unlink(paths["RUNS_ENABLED"])
    try:
        for name, value in paths.items():
            setattr(common, name, value)
        yield paths
    finally:
        for name, value in saved.items():
            setattr(common, name, value)


def section_p(s):
    sub = announce.ANSWER_SUBTYPE
    s.check("ANSWER_SUBTYPE is SUBSCRIBE", sub == "SUBSCRIBE")
    s.check("SUBSCRIBE is the documented command",
            getattr(announce, "SUBSCRIBE", None) == json.dumps({"command": "SUBSCRIBE", "value": "com_announcement_en"}))
    data = json.dumps({"type": "DATA", "data": "{}"})
    answer, pending, skipped = announce.answer_of([command("REGISTER", "SUCCESS"), command("SUBSCRIBE", "SUCCESS")], sub)
    s.check("REGISTER/SUCCESS then SUBSCRIBE/SUCCESS answers, REGISTER in skipped",
            answer is not None and answer.get("subType") == "SUBSCRIBE" and answer.get("data") == "SUCCESS"
            and pending == [] and [d.get("subType") for d in skipped] == ["REGISTER"])
    answer, pending, skipped = announce.answer_of([command("REGISTER", "SUCCESS")], sub)
    s.check("REGISTER/SUCCESS alone gives None", answer is None)
    answer, pending, skipped = announce.answer_of([command("SUBSCRIBE", "FAIL")], sub)
    s.check("SUBSCRIBE/FAIL answers", answer is not None and answer.get("data") == "FAIL")
    answer, pending, skipped = announce.answer_of([data, command("SUBSCRIBE", "SUCCESS")], sub)
    s.check("a DATA frame before the answer stays in pending", answer is not None and pending == [data])
    answer, pending, skipped = announce.answer_of([], sub)
    s.check("no frame gives None", answer is None and pending == [] and skipped == [])
    returned, sent, pending = connect_on([command("REGISTER", "SUCCESS"), command("SUBSCRIBE", "SUCCESS")])
    s.check("connect(): REGISTER, SUBSCRIBE both SUCCESS succeeds", returned is True)
    s.check("connect(): sent exactly [SUBSCRIBE]", sent == [announce.SUBSCRIBE])
    returned, sent, pending = connect_on([command("REGISTER", "SUCCESS")])
    s.check("connect(): REGISTER alone does not succeed", returned is False)
    returned, sent, pending = connect_on([command("REGISTER", "SUCCESS"), command("SUBSCRIBE", "FAIL")])
    s.check("connect(): SUBSCRIBE/FAIL does not succeed", returned is False)
    returned, sent, pending = connect_on([])
    s.check("connect(): no frame does not succeed", returned is False)

    tmp = tempfile.mkdtemp(prefix="vps-selftest-p.")
    try:
        with spool_in(tmp, True) as paths:
            message = {"catalogId": 48, "catalogName": "New Cryptocurrency Listing",
                       "publishDate": 1700000000000, "title": "Binance Will List Bitcoin (BTC)"}
            lists = [("BTC", "BTCUSDT")] + [(row["name"], row["s"]) for row in checkout_tokens()]
            s.check("the message is classed list BTC", announce.match_title(message["title"], lists, []) == ("list", "BTC"))
            outcome = announce.act(message, "list", "BTC")
            alerts = [n for n in os.listdir(paths["OUTBOX_DIR"]) if "-alert-" in n]
            s.check("act(): alerted", outcome == "alerted")
            s.check("act(): one alert", len(alerts) == 1)
            s.check("act(): no request", os.listdir(paths["REQUESTS_DIR"]) == [])
            s.check("request_run('bot') returns requested", common.request_run("bot") == "requested")
            s.check("request_run('bot') writes one request",
                    len([n for n in os.listdir(paths["REQUESTS_DIR"]) if n.endswith(".req")]) == 1)
        shutil.rmtree(tmp)
        with spool_in(tmp, False) as paths:
            s.check("runs disabled: request_run('bot') returns disabled", common.request_run("bot") == "disabled")
            s.check("runs disabled: no request written", os.listdir(paths["REQUESTS_DIR"]) == [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    s.check("common has no WATCHER_DAILY_CAP, R1 or R2",
            not any(hasattr(common, name) for name in ("WATCHER_DAILY_CAP", "R1", "R2")))


# --- Q: the repository's .claude/settings.json (contract §2, TZ-56 §12.7) -------------
def section_q(s):
    path = os.path.join(REPO, ".claude", "settings.json")
    try:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        valid = True
    except (OSError, ValueError):
        doc, valid = None, False
    s.check(".claude/settings.json is valid JSON", valid)
    s.check("its only key is autoMemoryEnabled", isinstance(doc, dict) and list(doc) == ["autoMemoryEnabled"])
    s.check("autoMemoryEnabled is false", isinstance(doc, dict) and doc.get("autoMemoryEnabled") is False)


# --- R: exchange.act, alerts only (TZ-57 §12.8), and the list (TZ-58 §12.7) ----------
# TZ-58 §12.7's texts, exactly.
SM = "https://www.binance.com/sitemap_output/domain=www.binance.com/sitemap_SupportAndAnnouncement_"
EN0, EN1, RU0 = SM + "en_0.xml", SM + "en_1.xml", SM + "ru_0.xml"
INDEX = "<sitemapindex>" + "".join("<sitemap><loc>%s</loc><lastmod>2026-10-02</lastmod></sitemap>" % u
                                   for u in (EN1, RU0, EN0, EN1)) + "</sitemapindex>"
A, B, C, D = "a" * 32, "0123456789abcdef" * 2, "115000483751", "d" * 32
DETAIL = "https://www.binance.com/en/support/announcement/detail/"
def urlset(urls):
    return "<urlset>" + "".join("<url><loc>%s</loc><lastmod>2026-10-02</lastmod></url>" % u for u in urls) + "</urlset>"
CHILD0 = urlset([DETAIL + A, DETAIL + B, "https://www.binance.com/en/support/faq/x1",
                 "https://www.binance.com/en/support/announcement/list/48",
                 "https://www.binance.com/zh-CN/support/announcement/detail/" + D])
CHILD1 = "<urlset><url><loc>\n    " + DETAIL + B + "\n  </loc></url>" + urlset([DETAIL + C])[8:]


def section_r(s):
    tmp = tempfile.mkdtemp(prefix="vps-selftest-r.")
    try:
        with spool_in(tmp, True) as paths:
            found = {"new_perpetual": ([], []), "delivery_set": ([], []),
                     "status_changed": ([("BTCUSDT", "TRADING", "SETTLING")], [])}
            cur = {"BTCUSDT": ["SETTLING", "PERPETUAL", None, 0]}
            returned = exchange.act(found, cur)
            s.check("act() returns 1", returned == 1)
            s.check("act() writes one alert",
                    len([n for n in os.listdir(paths["OUTBOX_DIR"]) if "-alert-" in n]) == 1)
            s.check("act() writes no request", os.listdir(paths["REQUESTS_DIR"]) == [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # TZ-58 §12.7's known answers, computed by the Architect on a prototype of §12.5's patterns.
    s.check("list_children(INDEX) == [EN1, EN0]", exchange.list_children(INDEX) == [EN1, EN0])
    s.check("list_articles(CHILD0) == {A, B}", exchange.list_articles(CHILD0) == {A, B})
    s.check("list_articles(CHILD1) == {B, C}", exchange.list_articles(CHILD1) == {B, C})
    s.check("list_diff(None, {A, B, C}) == ('-', '-')", exchange.list_diff(None, {A, B, C}) == ("-", "-"))
    s.check("list_diff({A, B, D}, {A, B, C}) == (1, 1)", exchange.list_diff({A, B, D}, {A, B, C}) == (1, 1))
    s.check("list_diff({A, B, C}, {A, B, C}) == (0, 0)", exchange.list_diff({A, B, C}, {A, B, C}) == (0, 0))


# --- S: the owner's stop (TZ-60 §12.11) ----------------------------------------------
STUB_SYSTEMCTL = """#!/usr/bin/env python3
import json, os, sys
with open(os.environ["SELFTEST_S_SYSTEMCTL_SAW"], "a") as fh:
    fh.write(json.dumps(sys.argv[1:]) + "\\n")
if sys.argv[1:2] == ["is-active"]:
    with open(os.environ["SELFTEST_S_STATES"]) as fh:
        states = fh.read().split()
    with open(os.environ["SELFTEST_S_STATES"], "w") as fh:
        fh.write(" ".join(states[1:]))
    print(states[0] if states else "unknown")
    sys.exit(0 if states[:1] == ["active"] else 3)
sys.exit(0)
"""
STUB_CLAUDE_TERM = """#!/usr/bin/env python3
import os, signal, time
os.kill(os.getppid(), signal.SIGTERM)
time.sleep(30)
"""


def notices(directory):
    """The texts of the notice files of an outbox directory, in name order."""
    out = []
    for name in sorted(n for n in os.listdir(directory) if n.endswith(".json")):
        with open(os.path.join(directory, name), encoding="utf-8") as fh:
            doc = json.load(fh)
        if doc.get("kind") == "notice":
            out.append(doc.get("text"))
    return out


def files_ending(directory, suffix):
    return [n for n in os.listdir(directory) if n.endswith(suffix)]


def section_s(s):
    tmp = tempfile.mkdtemp(prefix="vps-selftest-s.")
    saved = (common.STOP_DIR, common.REQUESTS_DIR, common.run_active, bot.CHUNK_SPACING_S)
    try:
        # 1. request_stop and pending_requests.
        stop_dir, requests_dir = os.path.join(tmp, "stop"), os.path.join(tmp, "requests")
        os.makedirs(stop_dir)
        os.makedirs(requests_dir)
        common.STOP_DIR, common.REQUESTS_DIR, bot.CHUNK_SPACING_S = stop_dir, requests_dir, 0
        s.check("request_stop('bot') returns requested", common.request_stop("bot") == "requested")
        s.check("request_stop('bot') writes exactly one .stop file",
                len(os.listdir(stop_dir)) == 1 and len(files_ending(stop_dir, ".stop")) == 1)
        s.check("pending_requests() is false on an empty requests directory", common.pending_requests() is False)
        with open(os.path.join(requests_dir, "1-bot-1.req"), "w") as fh:
            fh.write("{}")
        s.check("pending_requests() is true with one .req", common.pending_requests() is True)

        # 2. bot.respond on section N's MockApi.
        cases = ((True, False, "stop", 1, common.S12, "run active"),
                 (False, False, "stop", 0, common.S14, "no run, no request"),
                 (False, True, "stop", 1, common.S12, "no run, one request"),
                 (False, False, "S8", 0, common.S8, "the verdict S8"))
        for active, request, verdict, stops, text, label in cases:
            for directory in (stop_dir, requests_dir):
                for name in os.listdir(directory):
                    os.unlink(os.path.join(directory, name))
            if request:
                with open(os.path.join(requests_dir, "1-bot-1.req"), "w") as fh:
                    fh.write("{}")
            common.run_active = lambda v=active: v
            api = MockApi()
            bot.respond(api, 4242, verdict)
            s.check("respond, %s: %d .stop file(s)" % (label, stops), len(files_ending(stop_dir, ".stop")) == stops)
            s.check("respond, %s: one message, the expected text" % label, [t for _, t in api.sent] == [text])
    finally:
        common.STOP_DIR, common.REQUESTS_DIR, common.run_active, bot.CHUNK_SPACING_S = saved
        shutil.rmtree(tmp, ignore_errors=True)

    # 3. stop.choose on TZ-60 §12.8's seven rows, probed by the Architect.
    for before, removed, after, want in (("active", 0, "inactive", "S13"), ("activating", 0, "failed", "S13"),
                                         ("inactive", 1, "inactive", "S13"), ("inactive", 0, "inactive", "S14"),
                                         ("failed", 0, "failed", "S14"), ("active", 0, "active", "S15"),
                                         ("inactive", 1, "activating", "S15")):
        s.check("choose(%s, %d, %s) == %s" % (before, removed, after, want), stop.choose(before, removed, after) == want)

    # 4. stop.main with a stub systemctl first on PATH.
    env_keys = ("PATH", "SELFTEST_S_SYSTEMCTL_SAW", "SELFTEST_S_STATES")
    saved_env = {k: os.environ.get(k) for k in env_keys}
    unit = "selftest-stop.service"
    try:
        for states, plant, want_code, want_notice in ((["active", "inactive"], True, 0, "S13"),
                                                      (["inactive", "inactive"], False, 0, "S14"),
                                                      (["active", "active"], False, 1, "S15")):
            tmp = tempfile.mkdtemp(prefix="vps-selftest-s.")
            try:
                spool = os.path.join(tmp, "spool")
                for d in ("bin", "spool/outbox", "spool/requests", "spool/stop"):
                    os.makedirs(os.path.join(tmp, d))
                with open(os.path.join(tmp, "bin", "systemctl"), "w") as fh:
                    fh.write(STUB_SYSTEMCTL)
                os.chmod(os.path.join(tmp, "bin", "systemctl"), 0o755)
                with open(os.path.join(tmp, "states"), "w") as fh:
                    fh.write(" ".join(states))
                if plant:
                    for d, name in (("requests", "1-bot-1.req"), ("stop", "1-bot-1.stop")):
                        with open(os.path.join(spool, d, name), "w") as fh:
                            fh.write("{}")
                saw = os.path.join(tmp, "saw")
                os.environ.update({"PATH": os.path.join(tmp, "bin") + os.pathsep + (saved_env["PATH"] or ""),
                                   "SELFTEST_S_SYSTEMCTL_SAW": saw, "SELFTEST_S_STATES": os.path.join(tmp, "states")})
                with contextlib.redirect_stdout(io.StringIO()) as out:
                    code = stop.main(["--unit", unit, "--spool", spool])
                label = "stop.main, states %s: " % ",".join(states)
                s.check(label + "returns %d" % want_code, code == want_code)
                s.check(label + "one notice %s" % want_notice,
                        notices(os.path.join(spool, "outbox")) == [getattr(common, want_notice)]
                        and len(os.listdir(os.path.join(spool, "outbox"))) == 1)
                if plant:
                    with open(saw) as fh:
                        calls = [json.loads(line) for line in fh]
                    s.check(label + "is-active, stop, reset-failed, is-active, each on the unit",
                            calls == [["is-active", unit], ["stop", unit], ["reset-failed", unit], ["is-active", unit]])
                    s.check(label + "requests/ and stop/ empty",
                            os.listdir(os.path.join(spool, "requests")) == [] and os.listdir(os.path.join(spool, "stop")) == [])
                    lines = [l for l in out.getvalue().splitlines() if l.startswith("crypto-stop:")]
                    s.check(label + "one line crypto-stop: stops=1 requests_removed=1 before=active stop_exit=0 "
                            "reset_exit=0 after=inactive notice=S13",
                            len(lines) == 1 and lines[0].startswith(
                                "crypto-stop: stops=1 requests_removed=1 before=active stop_exit=0 reset_exit=0 "
                                "after=inactive notice=S13"))
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    finally:
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    # 5. run.main under section O's fixtures, a stub claude sending SIGTERM to its parent.
    for stopping in (True, False):
        tmp = tempfile.mkdtemp(prefix="vps-selftest-s.")
        env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", "SELFTEST_O_WRITER_SAW")
        saved_env = {k: os.environ.get(k) for k in env_keys}
        patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (common, "STOP_ACTIVE"), (run, "WRITER"),
                   (run, "own_memory_max"), (run, "own_swap_max")]
        saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
        saved_term = signal.getsignal(signal.SIGTERM)
        label = "SIGTERM with STOP_ACTIVE %s: " % ("present" if stopping else "absent")
        try:
            paths, tree, _ = o_fixtures(tmp, STUB_CLAUDE_TERM, "sk-ant-oat01-selftest-planted-" + os.urandom(6).hex())
            os.environ.update({"PATH": paths["bin"] + os.pathsep + (saved_env["PATH"] or ""),
                               "CREDENTIALS_DIRECTORY": paths["creds"], "RUNTIME_DIRECTORY": paths["runtime"],
                               "SELFTEST_O_WRITER_SAW": os.path.join(tmp, "writer-saw")})
            common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
            common.STOP_ACTIVE = tmp if stopping else os.path.join(tmp, "absent")
            run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
            run.own_memory_max = run.own_swap_max = lambda: None
            code = None
            with contextlib.redirect_stdout(io.StringIO()) as out:
                try:
                    run.main(["--tree", tree])
                except SystemExit as exc:
                    code = exc.code
            printed = out.getvalue().splitlines()
            s.check(label + "SystemExit 143", code == 143)
            owner_lines = printed.count("crypto-run: stopped by the owner")
            if stopping:
                s.check(label + "the owner's line printed once", owner_lines == 1)
                s.check(label + "the three summary lines printed",
                        all(len([l for l in printed if l.startswith(p)]) == 1
                            for p in ("crypto-run: requests=", "crypto-run: models=", "crypto-run: memory_max=")))
                s.check(label + "no notice in the outbox", notices(paths["outbox"]) == [])
            else:
                s.check(label + "one notice S7", notices(paths["outbox"]) == [common.S7])
                s.check(label + "the owner's line absent", owner_lines == 0)
        finally:
            signal.signal(signal.SIGTERM, saved_term)
            for mod, name, value in saved_attrs:
                setattr(mod, name, value)
            for k, v in saved_env.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
            shutil.rmtree(tmp, ignore_errors=True)


# --- T: the alert rule on the stream's records (TZ-62 section 12.4) ------------------
T_LA, T_LBN, T_NCL = "Latest Activities", "Latest Binance News", "New Cryptocurrency Listing"
T_PERPS = [("PEPE", "1000PEPEUSDT"), ("S", "SUSDT"), ("ZRO", "ZROUSDT"), ("STG", "STGUSDT"),
           ("MET", "METUSDT"), ("USDC", "USDCUSDT"), ("WIN", "WINUSDT")]
T_DELIST_MANY = "Binance Futures Will Delist Multiple USD\u24c8-M Perpetual Contracts (2026-10-05)"
T_FUNDING_MANY = "Binance Futures Will Adjust the Funding Rate Interval of Multiple USD\u24c8-M Perpetual Contracts (2026-10-10)"
T_PROMO_FUTURES = "Trade Futures & Win: Complete Tasks to Share 200 BNB in Rewards!"
T_PROMO_MET = "MET Trading Tournament: Trade to Share Up to 400 BNB Token Vouchers"
# (catalogId, catalogName, title, body, reason, symbols). Rows 1-13 are the stream's own
# records: TZ-61's report, table "Records at or after T1", and the owner's screenshot of
# 08.10.2026; every other row's catalogue is the fixture's.
T_ROWS = (
    (93, T_LA, "Binance Lite Loan Promotion Extended: Enjoy Simple Borrowing with 50% Off Service Fee!", None, "catalogue", []),
    (93, T_LA, "Word of the Day: Test Your Knowledge on \u201cProactive Security Wins\u201d to Unlock USDC Rewards!", None, "catalogue", []),
    (93, T_LA, "Binance Pay Exclusive: Get up to 20% Off Mobile Top-Ups in Selected Regions!", None, "catalogue", []),
    (93, T_LA, "New User bStocks Convert Campaign: Join and Share a Reward Pool of Up to 110 SPCXB", None, "catalogue", []),
    (49, T_LBN, "Binance Will Support Marvell Technology (MRVL) and Oracle Corporation (ORCL) Cash Dividend Distribution via bStocks", None, "non-crypto", []),
    (48, T_NCL, "Binance Futures Will Launch Multiple TradFi USD\u24c8-Margined Perpetual Contracts (2026-10-06)", None, "non-crypto", []),
    (93, T_LA, "APAC Exclusive: Win a Fully Hosted Trip to Binance Blockchain Week 2026", None, "catalogue", []),
    (49, T_LBN, "Update on the Collateral Ratio Under Cross Margin and Portfolio Margin (2026-10-09)", None, "noise", []),
    (48, T_NCL, "Binance Exchange Adds JPMorgan Chase (JPMB), Eli Lilly (LLYB), Securitize Corp (SECZB) and StablecoinX Inc (USDEB) bStocks Trading Pairs on Binance Spot/Convert - 2026-10-07", None, "non-crypto", []),
    (48, T_NCL, "Binance Will Add 4 bStocks Tokenized Securities as Collateral Asset - 2026-10-07", None, "non-crypto", []),
    (157, "Maintenance Updates", "Binance Has Completed the Stargate Finance (STG) Token Merge to LayerZero (ZRO)", None, "catalogue", []),
    (93, T_LA, T_PROMO_FUTURES, None, "catalogue", []),
    (93, T_LA, T_PROMO_MET, None, "catalogue", []),
    (49, T_LBN, T_PROMO_FUTURES, None, "noise", []),
    (49, T_LBN, T_PROMO_MET, None, "noise", []),
    (48, T_NCL, "Binance Will List Hyperliquid (HYPE) with Seed Tag Applied", None, "new-coin", []),
    (48, T_NCL, "Introducing ETHFI on Binance Launchpool", None, "new-coin", []),
    (48, T_NCL, "Binance Futures Will Launch USD\u24c8-Margined SUIUSDT Perpetual Contract", None, "new-coin", []),
    (48, T_NCL, "Introducing Plasma (XPL) on Binance HODLer Airdrops! Earn XPL With Retroactive BNB Simple Earn Subscriptions", None, "new-coin", []),
    (48, T_NCL, "Binance Will List Bitcoin (BTC)", None, "new-coin", []),
    (93, T_LA, "Binance Will List Bitcoin (BTC)", None, "catalogue", []),
    (161, "Delisting", "Binance Will Delist Sonic (S)", None, "perpetual", []),
    (49, T_LBN, "Binance Will Extend Monitoring Tag to Include Sonic (S)", None, "perpetual", []),
    (49, T_LBN, "Binance Will Delist WIN on 2026-10-20", None, "perpetual", []),
    (49, T_LBN, "Binance Futures Will Update the Leverage and Margin Tiers of XRPUSDT Perpetual Contract (2026-10-10)", None, "list", []),
    (49, T_LBN, T_DELIST_MANY, "Positions in XRPUSDT will be closed at 2026-10-05 09:00 (UTC).", "contract", ["XRPUSDT"]),
    (49, T_LBN, T_DELIST_MANY, "PROMPTUSDT, PUMPBTCUSDT and 1000000BOBUSDT at 2026-10-05 09:00 (UTC).", "none", []),
    (49, T_LBN, T_FUNDING_MANY, "ENAUSDT and BTCUSDT will settle funding every 4 hours.", "contract", ["BTCUSDT", "ENAUSDT"]),
    (49, T_LBN, T_FUNDING_MANY, None, "none", []),
    (50, "New Fiat Listings", "Binance Adds ARB/EUR Trading Pair", None, "noise", []),
    (157, "Maintenance Updates", "Binance Will Support the BNB Smart Chain (BSC) Network Upgrade & Hard Fork", None, "catalogue", []),
    (48, T_NCL, "Binance Futures Will Launch USD\u24c8-M BTCUSDT Quarterly 1226 Futures Contract", None, "noise", []),
)


def section_t(s):
    lists = [("BTC", "BTCUSDT")] + [(row["name"], row["s"]) for row in checkout_tokens()]
    for cid, cname, title, body, reason, symbols in T_ROWS:
        cls, _ticker = announce.match_title(title, lists, T_PERPS)
        data = {"catalogId": cid, "catalogName": cname, "title": title, "body": body}
        s.check("%s %s -> %s" % (cid, title, reason), announce.alert_rule(data, cls, lists) == (reason, symbols))
    hhmm = datetime.fromtimestamp(1700000000, tz=announce.TBILISI).strftime("%H:%M")
    tmp = tempfile.mkdtemp(prefix="vps-selftest-t.")
    try:
        with spool_in(tmp, True) as paths:
            def alerts():
                return sorted(n for n in os.listdir(paths["OUTBOX_DIR"]) if "-alert-" in n)

            def text_of(name):
                with open(os.path.join(paths["OUTBOX_DIR"], name), encoding="utf-8") as fh:
                    return json.load(fh)["text"]

            promo = {"catalogId": 93, "catalogName": T_LA, "title": T_PROMO_MET, "publishDate": 1700000000000}
            s.check("act(): the promotion of 08.10 is recorded", announce.act(promo, "list", "BNB", lists) == "recorded")
            s.check("act(): no alert for it", alerts() == [])
            listing = {"catalogId": 48, "catalogName": T_NCL, "publishDate": 1700000000000,
                       "title": "Binance Will List Hyperliquid (HYPE) with Seed Tag Applied"}
            s.check("act(): a new coin alerts", announce.act(listing, "list", "HYPE", lists) == "alerted")
            first = alerts()
            s.check("act(): one alert, A1 exactly", len(first) == 1 and text_of(first[0]) == common.A1.format(
                hhmm=hhmm, catalog_name=T_NCL, title=listing["title"]))
            funding = {"catalogId": 49, "catalogName": T_LBN, "title": T_FUNDING_MANY, "publishDate": 1700000000000,
                       "body": "ENAUSDT and BTCUSDT will settle funding every 4 hours."}
            s.check("act(): a contract notice on list contracts alerts", announce.act(funding, "none", None, lists) == "alerted")
            second = [n for n in alerts() if n not in first]
            s.check("act(): A1 with the contracts appended", len(second) == 1 and text_of(second[0]) == common.A1.format(
                hhmm=hhmm, catalog_name=T_LBN, title=T_FUNDING_MANY) + " \u00b7 BTCUSDT, ENAUSDT")
            s.check("act(): no request", os.listdir(paths["REQUESTS_DIR"]) == [])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- U: the delivery test (TZ-63) ----------------------------------------------------
STUB_CLAUDE_U = """#!/usr/bin/env python3
import json, os, sys
json.dump({"type": "result", "subtype": "success", "is_error": False, "result": os.environ["SELFTEST_U_RESULT"],
           "num_turns": 2, "duration_ms": 10, "modelUsage": {}, "permission_denials": [], "usage": {},
           "total_cost_usd": 0.1}, sys.stdout)
"""
# The final message the run of 09.10.2026 delivered, two of its lines verbatim.
U_STATUS = ("The hunter is still running the catalyst, unlock and positioning hunt. Here's where the run stands:\n"
            "\n"
            "When the report arrives, I'll read it and do my four allowed lookups.\n")


def section_u(s):
    head = run.ANSWER_HEAD
    with open(os.path.join(REPO, "ANALYST-INSTRUCTIONS.md"), encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]
    starts = [i for i, line in enumerate(lines) if line.startswith("## 2. ")]
    fence = None
    if len(starts) == 1:
        fence = next((i for i in range(starts[0] + 1, len(lines)) if lines[i] == "`" * 3), None)
    s.check("ANALYST-INSTRUCTIONS.md section 2's skeleton opens with run.ANSWER_HEAD",
            fence is not None and fence + 1 < len(lines) and lines[fence + 1].startswith(head + " "))
    cases = ((head + " 22:59 Tbilisi\n\n# R\n", True, "an answer"),
             ("\n\n  " + head + " 22:59\n", True, "an answer after blank lines and indentation"),
             ("**" + head + "** 22:59\n", True, "an answer under emphasis"),
             ("Note.\n\n" + head + " 22:59\n", True, "an answer after a line before it"),
             (U_STATUS, False, "the status the run of 09.10.2026 delivered"),
             (common.S7, False, "notice S7"),
             ("Soon: " + head + " 22:59\n", False, "the head inside a line"),
             ("", False, "an empty string"),
             (None, False, "None"),
             (42, False, "a number"))
    for result, want, label in cases:
        s.check("is_answer: %s is %s" % (label, want), run.is_answer(result) is want)
    tmp = tempfile.mkdtemp(prefix="vps-selftest-u.")
    env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", "SELFTEST_O_WRITER_SAW", "SELFTEST_U_RESULT")
    saved_env = {k: os.environ.get(k) for k in env_keys}
    patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (run, "WRITER"), (run, "own_memory_max"),
               (run, "own_swap_max")]
    saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
    saved_term = signal.getsignal(signal.SIGTERM)
    want_line = "crypto-run: final message is not an answer chars=%d" % len(U_STATUS)
    try:
        paths, tree, _ = o_fixtures(tmp, STUB_CLAUDE_U, "sk-ant-oat01-selftest-planted-" + os.urandom(6).hex())
        os.environ.update({"PATH": paths["bin"] + os.pathsep + (saved_env["PATH"] or ""),
                           "CREDENTIALS_DIRECTORY": paths["creds"], "RUNTIME_DIRECTORY": paths["runtime"],
                           "SELFTEST_O_WRITER_SAW": os.path.join(tmp, "writer-saw"), "SELFTEST_U_RESULT": U_STATUS})
        common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
        run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
        run.own_memory_max = run.own_swap_max = lambda: None
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = run.main(["--tree", tree])
        summary = out.getvalue()
        s.check("a status as the final message: exit 1", code == 1)
        s.check("a status as the final message: one notice S7", notices(paths["outbox"]) == [common.S7])
        s.check("a status as the final message: no answer in the outbox",
                [n for n in os.listdir(paths["outbox"]) if "-answer-" in n] == [])
        s.check("one line " + want_line, summary.splitlines().count(want_line) == 1)
        s.check("the summary carries answer_chars=0", " answer_chars=0" in summary)
        s.check("the summary never carries the status", "The hunter is still running" not in summary)
    finally:
        signal.signal(signal.SIGTERM, saved_term)
        for mod, name, value in saved_attrs:
            setattr(mod, name, value)
        for k, v in saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(tmp, ignore_errors=True)
    with open(os.path.join(HERE, "units", "crypto-run.service"), encoding="utf-8") as fh:
        unit_lines = [line.rstrip("\n") for line in fh]
    s.check("exactly one Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1",
            unit_lines.count("Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1") == 1)


# --- V: common.publish on a local remote, through the writer and for new files (TZ-64) ----
def _v_git(cwd, *args):
    return subprocess.run(["git", "-C", cwd] + list(args), capture_output=True, text=True)


def _v_head(cwd, ref="HEAD"):
    return _v_git(cwd, "rev-parse", ref).stdout.strip()


def section_v(s):
    tmp = tempfile.mkdtemp(prefix="vps-selftest-v.")
    try:
        remote, a, b = (os.path.join(tmp, n) for n in ("remote.git", "a", "b"))
        _v_git(tmp, "init", "-q", "--bare", "-b", "main", remote)
        reject = os.path.join(tmp, "reject")
        hook = os.path.join(remote, "hooks", "pre-receive")
        with open(hook, "w", encoding="utf-8") as fh:
            fh.write("#!/bin/sh\n[ -e '%s' ] && exit 1\nexit 0\n" % reject)
        os.chmod(hook, 0o755)
        _v_git(tmp, "clone", "-q", remote, b)
        for clone in (b,):
            _v_git(clone, "config", "user.name", "selftest")
            _v_git(clone, "config", "user.email", "selftest@localhost")
        os.makedirs(os.path.join(b, "analyst"))
        with open(os.path.join(b, writer.PAYLOAD), "w", encoding="utf-8") as fh:
            fh.write("{}\n")
        _v_git(b, "add", "-A")
        _v_git(b, "commit", "-q", "-m", "base")
        _v_git(b, "push", "-q", "origin", "HEAD:main")
        _v_git(tmp, "clone", "-q", "-b", "main", remote, a)
        _v_git(a, "config", "user.name", "selftest")
        _v_git(a, "config", "user.email", "selftest@localhost")

        def fresh():
            _v_git(a, "fetch", "-q", "origin", "main")
            _v_git(a, "reset", "-q", "--hard", "origin/main")

        def payload(clone, text):
            with open(os.path.join(clone, writer.PAYLOAD), "w", encoding="utf-8") as fh:
                fh.write(text)

        def other_writer(path, text):
            _v_git(b, "pull", "-q", "origin", "main")
            with open(os.path.join(b, path), "w", encoding="utf-8") as fh:
                fh.write(text)
            _v_git(b, "add", "-A")
            _v_git(b, "commit", "-q", "-m", "other")
            _v_git(b, "push", "-q", "origin", "HEAD:main")

        # 1. accepted
        fresh()
        payload(a, '{"n":1}\n')
        s.check("writer: accepted -> (True, True)", writer.publish(a) == (True, True))
        s.check("writer: accepted -> remote main is the clone's HEAD", _v_head(remote, "main") == _v_head(a))
        s.check("writer: the commit message is COMMIT_MESSAGE",
                _v_git(remote, "log", "-1", "--format=%s", "main").stdout.strip() == writer.COMMIT_MESSAGE)
        # 2. rejected once, rebased, pushed
        fresh()
        other_writer("other.txt", "x\n")
        payload(a, '{"n":2}\n')
        s.check("writer: one rejection -> rebase -> (True, True)", writer.publish(a) == (True, True))
        s.check("writer: after the rebase remote main carries both commits",
                _v_git(remote, "log", "--format=%s", "-2", "main").stdout.split("\n")[:2]
                == [writer.COMMIT_MESSAGE, "other"])
        # 3. a rebase that conflicts drops the commit
        fresh()
        base = _v_head(a)
        other_writer(writer.PAYLOAD, '{"other":3}\n')
        theirs = _v_head(remote, "main")
        payload(a, '{"n":3}\n')
        s.check("writer: a conflicting rebase -> (True, False)", writer.publish(a) == (True, False))
        s.check("writer: the clone is back at its base", _v_head(a) == base)
        s.check("writer: remote main is the other writer's", _v_head(remote, "main") == theirs)
        s.check("writer: no rebase is left in progress",
                not os.path.exists(os.path.join(a, ".git", "rebase-merge"))
                and not os.path.exists(os.path.join(a, ".git", "rebase-apply")))
        # 4. a second rejection drops the commit
        fresh()
        base = _v_head(a)
        with open(reject, "w", encoding="utf-8") as fh:
            fh.write("1")
        payload(a, '{"n":4}\n')
        s.check("writer: two rejections -> (True, False)", writer.publish(a) == (True, False))
        s.check("writer: two rejections leave the clone at its base", _v_head(a) == base)
        os.unlink(reject)
        # 5. nothing to commit
        fresh()
        s.check("writer: nothing changed -> (False, False)", writer.publish(a) == (False, False))
        s.check("writer: nothing changed leaves the tree clean", _v_git(a, "status", "--porcelain").stdout == "")
        # 6. new, untracked files
        fresh()
        os.makedirs(os.path.join(a, "analyst", "paper", "book"))
        rels = ["analyst/paper/x.json", "analyst/paper/book/2026-01-01.jsonl"]
        for rel in rels:
            with open(os.path.join(a, rel), "w", encoding="utf-8") as fh:
                fh.write(rel + "\n")
        s.check("new files -> (True, True)", common.publish(a, rels, "paper: x") == (True, True))
        s.check("new files: both on remote main",
                _v_git(remote, "ls-tree", "-r", "--name-only", "main").stdout.split() ==
                sorted(["analyst/live.json", "other.txt"] + rels))
        s.check("new files: the message is the one given",
                _v_git(remote, "log", "-1", "--format=%s", "main").stdout.strip() == "paper: x")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- W: the paper test (TZ-64) -----------------------------------------------------------
W_T0 = paper.day_start("2026-01-07")
W_SYMBOLS = {"BTCUSDT", "1000PEPEUSDT", "KAITOUSDT", "ETHUSDT"}


def w_portfolio(rets, values=None, turnover=1.0, month_value=100000.0):
    """A portfolio answer: perpAllTime with a point at every grid instant (and one wild point off the
    grid, which no grid instant may read), perpMonth over exactly 30 days at month_value."""
    grid = [W_T0 - (52 - j) * paper.WEEK_MS for j in range(53)]
    vals = values or [100000.0] * 53
    pnl = [0.0]
    for j, r in enumerate(rets):
        pnl.append(pnl[-1] + r * vals[j])
    av = [[g, repr(v)] for g, v in zip(grid, vals)] + [[grid[10] + 3 * paper.DAY_MS, "1.0"]]
    pn = [[g, repr(p)] for g, p in zip(grid, pnl)] + [[grid[10] + 3 * paper.DAY_MS, "-999999.0"]]
    month = [[W_T0 - 30 * paper.DAY_MS, repr(month_value)], [W_T0, repr(month_value)]]
    return [["perpAllTime", {"accountValueHistory": av[::-1], "pnlHistory": pn[::-1], "vlm": "1"}],
            ["perpMonth", {"accountValueHistory": month, "pnlHistory": month,
                           "vlm": repr(turnover * month_value * 30)}]]


def w_fill(t, start, side, sz, coin="BTC", px="100", tid=None):
    return {"coin": coin, "px": px, "sz": str(sz), "side": side, "time": t, "startPosition": str(start),
            "tid": tid if tid is not None else t}


W_LEADERBOARD = ('{"leaderboardRows": [{"ethAddress": "0xAA", "accountValue": "1", "windowPerformances": '
                 '[["day", {"vlm": "1"}], ["allTime", {"pnl": "0", "vlm": "300000000"}]], '
                 '"displayName": "a}{\\"],\\u0416 \u0416"}, \n {"ethAddress": "0xbb", "windowPerformances": '
                 '[["allTime", {"vlm": "199999999.99"}]], "displayName": null}, {"ethAddress": "0xcc"}, '
                 '{"ethAddress": "0xDd", "windowPerformances": [["allTime", {"vlm": "200000000"}]]}]}')


def w_kl(t, prices, missing=()):
    """Minute rows from t - 10 min to t + 6 h; prices(m) -> (o, h, l, c)."""
    times = [m for m in range(t - 600000, t + 6 * 3600000 + 60000, 60000) if m not in missing]
    return times, [prices(m) for m in times]


def section_w(s):
    near = lambda x, y: x is not None and y is not None and abs(x - y) <= 1e-9 * max(1.0, abs(y))  # noqa: E731
    # W1. the leaderboard, one row at a time, on every chunking
    blob = W_LEADERBOARD.encode("utf-8")
    for size in (1, 7, 64, len(blob)):
        chunks = [blob[i:i + size] for i in range(0, len(blob), size)]
        s.check("pool_of(iter_rows(chunks of %d)) == (['0xaa', '0xdd'], 4, 1)" % size,
                paper.pool_of(paper.iter_rows(chunks)) == (["0xaa", "0xdd"], 4, 1))
    try:
        list(paper.iter_rows([blob[:-40]]))
        truncated = False
    except ValueError:
        truncated = True
    s.check("a truncated document raises ValueError", truncated)
    # W2. the twelve-month record
    worlds = {
        "A": w_portfolio([0.02, 0.0] * 26),
        "B": w_portfolio([0.03, -0.01] * 26),
        "C": w_portfolio([-0.01] * 16 + [0.02, 0.0] * 18),
        "D": w_portfolio([0.02] * 9 + [-0.30] + [0.02] * 42),
        "E": w_portfolio([0.02, 0.0] * 26, values=[100000.0] * 5 + [9000.0] + [100000.0] * 47),
        "F": w_portfolio([0.02, 0.0] * 26, values=[100000.0] * 52 + [40000.0]),
        "G": w_portfolio([0.02, 0.0] * 26, turnover=11.0),
        "H": w_portfolio([0.02, 0.0] * 26, turnover=10.0),
    }
    m = {k: paper.metrics(v, W_T0) for k, v in worlds.items()}
    s.check("A: eligible, passes, 13 blocks, drawdown 0, Sharpe 1.0",
            m["A"]["eligible"] and m["A"]["r12"] and m["A"]["blocks"] == 13 and m["A"]["drawdown"] == 0.0
            and near(m["A"]["sharpe"], 1.0))
    s.check("B: passes, 13 blocks, drawdown 0.01, Sharpe 0.5",
            m["B"]["r12"] and m["B"]["blocks"] == 13 and near(m["B"]["drawdown"], 0.01) and near(m["B"]["sharpe"], 0.5))
    s.check("C: eligible, 9 blocks, fails", m["C"]["eligible"] and m["C"]["blocks"] == 9 and not m["C"]["r12"])
    s.check("D: eligible, drawdown 0.30, fails", m["D"]["eligible"] and near(m["D"]["drawdown"], 0.30)
            and not m["D"]["r12"])
    s.check("E: a week at 9 000 is ineligible", not m["E"]["eligible"] and not m["E"]["r12"])
    s.check("F: 40 000 at T0 is ineligible", not m["F"]["eligible"] and m["F"]["value_t0"] == 40000.0)
    s.check("G: turnover 11 is ineligible", not m["G"]["eligible"] and near(m["G"]["turnover"], 11.0))
    s.check("H: turnover 10 is eligible", m["H"]["eligible"] and near(m["H"]["turnover"], 10.0))
    s.check("step_at reads the last point at or before t",
            paper.step_at([(1, 10.0), (5, 50.0)], 4) == 10.0 and paper.step_at([(1, 10.0), (5, 50.0)], 5) == 50.0
            and paper.step_at([(1, 10.0)], 0) is None)
    s.check("ranking: A before B", sorted(("B", "A"), key=lambda k: -m[k]["sharpe"]) == ["A", "B"])
    # W3. the Binance symbol
    cases = (("BTC", "BTCUSDT"), ("kPEPE", "1000PEPEUSDT"), ("KAITO", "KAITOUSDT"), ("xyz:CL", None),
             ("PURR/USDC", None), ("@151", None), ("SOL", None))
    for coin, want in cases:
        s.check("symbol_for(%r) == %r" % (coin, want), paper.symbol_for(coin, W_SYMBOLS) == want)
    s.check("symbol_for('kPEPE') is None without 1000PEPEUSDT", paper.symbol_for("kPEPE", {"PEPEUSDT"}) is None)
    # W4. episodes from fills
    coins, seq = {}, []
    fills = [w_fill(1, 5, "A", 5), w_fill(2, 0, "B", 1), w_fill(3, 1, "B", 1), w_fill(4, 2, "A", 1),
             w_fill(5, 1, "A", 3, px="101"), w_fill(6, -2, "B", 2, px="99"), w_fill(7, 0, "B", 1), w_fill(8, -1, "B", 1)]
    for f in fills:
        seq.append(paper.apply_fill(coins, f, "BTCUSDT"))
    kinds = [[k for k, _ in ev] for ev in seq]
    s.check("event kinds: [], open, [], [], close+open, close, open, lost",
            kinds == [[], ["open"], [], [], ["close", "open"], ["close"], ["open"], ["lost"]])
    long_ep, short_ep = seq[4][0][1], seq[5][0][1]
    s.check("the long: side 1, opened at 2, closed at 5 at 101 after 4 fills",
            (long_ep["side"], long_ep["t_open"], long_ep["t_close"], long_ep["px_close"], long_ep["n"]) == (1, 2, 5, "101", 4))
    s.check("the short: side -1, opened at 5, closed at 6 at 99 after 2 fills",
            (short_ep["side"], short_ep["t_open"], short_ep["t_close"], short_ep["px_close"], short_ep["n"]) == (-1, 5, 6, "99", 2))
    s.check("a lost episode leaves the coin flat", coins["BTC"] is None)
    # W5. copyability
    w0, h = W_T0 - 91 * paper.DAY_MS, 3600000
    base = [w_fill(w0 + h, 0, "B", 10), w_fill(w0 + 4 * h, 10, "A", 10), w_fill(w0 + 5 * h, 0, "A", 10),
            w_fill(w0 + 6 * h, -10, "B", 10), w_fill(w0 + 7 * h, 0, "B", 1, coin="PURR/USDC", px="100000"),
            w_fill(W_T0, 0, "B", 1000, coin="xyz:CL")]
    c = paper.copyability(base + [w_fill(w0 + 8 * h, 0, "B", 10, coin="xyz:CL")], W_SYMBOLS, w0, W_T0)
    s.check("share 0.8 exactly and median 2 h: copyable", c["copyable"] and near(c["share"], 0.8)
            and c["median_episode_s"] == 7200 and c["closed_episodes"] == 2)
    c = paper.copyability(base + [w_fill(w0 + 8 * h, 0, "B", 10, coin="xyz:CL", px="100.0001")], W_SYMBOLS, w0, W_T0)
    s.check("share just under 0.8: not copyable", not c["copyable"] and c["share"] < 0.8)
    short_close = [dict(f) for f in base]
    short_close[3]["time"] = w0 + 5 * h + 59 * 60000
    c = paper.copyability(short_close + [w_fill(w0 + 8 * h, 0, "B", 10, coin="xyz:CL")], W_SYMBOLS, w0, W_T0)
    s.check("median 1 h 59.5 min: not copyable", not c["copyable"] and c["median_episode_s"] == 7170)
    # W5b. fills, page by page
    saved_info = paper.info

    def pages(body, limiter):
        t = body["startTime"]
        if body["user"] == "stuck":
            return [{"coin": "BTC", "px": "1", "sz": "1", "side": "B", "time": 5, "startPosition": "0", "tid": i,
                     "extra": 0} for i in range(paper.FILLS_PAGE)]
        last = min(t + paper.FILLS_PAGE, 4000)
        return [{"coin": "BTC", "px": "1", "sz": "1", "side": "B", "time": m, "startPosition": "0", "tid": m,
                 "extra": 0} for m in range(t, last)]

    try:
        paper.info = pages
        got = paper.fills_since("a", 1, None)
        s.check("pages of 2 000 repeating their boundary: each fill once, ascending, 3 999 in all",
                [f["tid"] for f in got] == list(range(1, 4000)))
        s.check("a fill keeps only FILL_KEYS", set(got[0]) == set(paper.FILL_KEYS))
        try:
            paper.fills_since("stuck", 5, None)
            stuck = False
        except ValueError:
            stuck = True
        s.check("a full page inside one millisecond raises ValueError", stuck)
    finally:
        paper.info = saved_info
    # W6. the null's order
    addrs = ["0x%040x" % i for i in range(20)]
    order = paper.null_order(W_T0, addrs)
    s.check("null_order is a permutation, independent of input order",
            sorted(order) == sorted(addrs) and paper.null_order(W_T0, addrs[::-1]) == order)
    s.check("null_order moves with T0", paper.null_order(W_T0 + paper.DAY_MS, addrs) != order)
    # W7. booking
    t = paper.day_start("2026-01-05") + 10 * h
    rise = w_kl(t, lambda mm: (100.0,) * 4 if mm < t + h else (110.0,) * 4)
    ep = {"side": 1, "t_open": t + 30000, "t_close": t + 3 * h + 30000}
    b = paper.book_delay(ep, 5, 0.04, rise, 10000.0, 0.005, 0.0005, t + 10 * h)
    s.check("rise, 5 s: entry minute t at 100, qty 12.5, exit t + 3 h at 110, gross 125, fee 1.3125",
            b["entry_ms"] == t and b["entry_px"] == 100.0 and near(b["qty"], 12.5) and b["src"]["exit_ms"] == t + 3 * h
            and b["src"]["px"] == 110.0 and near(b["src"]["gross"], 125.0) and near(b["src"]["fee"], 1.3125))
    s.check("rise, 5 s: not stopped, the stop variant equals the source", not b["stopped"] and b["stop"] == b["src"])
    b = paper.book_delay(ep, 7200, 0.04, rise, 10000.0, 0.005, 0.0005, t + 10 * h)
    s.check("rise, 7 200 s: entry t + 2 h at 110, exit t + 5 h, gross 0, fee 1.25",
            b["entry_ms"] == t + 2 * h and b["entry_px"] == 110.0 and b["src"]["exit_ms"] == t + 5 * h
            and near(b["src"]["gross"], 0.0) and near(b["src"]["fee"], 1.25))
    dip = w_kl(t, lambda mm: (97.0, 97.0, 95.5, 96.5) if mm == t + 30 * 60000 else (100.0,) * 4)
    b = paper.book_delay(ep, 5, 0.04, dip, 10000.0, 0.005, 0.0005, t + 10 * h)
    s.check("dip: stopped at t + 30 min at 96, gross -50 (the risk), fee 1.225",
            b["stopped"] and b["stop"]["exit_ms"] == t + 30 * 60000 and b["stop"]["px"] == 96.0
            and near(b["stop"]["gross"], -50.0) and near(b["stop"]["fee"], 1.225))
    s.check("dip: the source variant holds to t + 3 h at 100, gross 0", b["src"]["px"] == 100.0
            and near(b["src"]["gross"], 0.0))
    b = paper.book_delay(dict(ep, t_close=t + 30 * 60000 + 10000), 5, 0.04, dip, 10000.0, 0.005, 0.0005, t + 10 * h)
    s.check("dip in the exit minute: the stop variant leaves at 96, the source at that minute's close 96.5",
            b["stopped"] and b["stop"]["px"] == 96.0 and b["src"]["exit_ms"] == t + 30 * 60000 and b["src"]["px"] == 96.5)
    gap = w_kl(t, lambda mm: (95.0, 95.0, 94.0, 94.5) if mm == t + 30 * 60000 else (100.0,) * 4)
    b = paper.book_delay(ep, 5, 0.04, gap, 10000.0, 0.005, 0.0005, t + 10 * h)
    s.check("gap: exits at the open 95, gross -62.5", b["stop"]["px"] == 95.0 and near(b["stop"]["gross"], -62.5))
    spike = w_kl(t, lambda mm: (103.0, 104.5, 103.0, 104.0) if mm == t + 30 * 60000 else (100.0,) * 4)
    b = paper.book_delay(dict(ep, side=-1), 5, 0.04, spike, 10000.0, 0.005, 0.0005, t + 10 * h)
    s.check("short spike: stopped at 104, gross -50", b["stopped"] and b["stop"]["px"] == 104.0
            and near(b["stop"]["gross"], -50.0))
    hole = w_kl(t, lambda mm: (100.0,) * 4 if mm < t + h else (110.0,) * 4, missing=(t,))
    b = paper.book_delay(ep, 5, 0.04, hole, 10000.0, 0.005, 0.0005, t + 10 * h)
    s.check("a missing entry minute: nominal entry t, the previous close", b["entry_ms"] == t and b["entry_px"] == 100.0)
    cut = {"side": 1, "t_open": t + 4 * h, "t_close": None, "cut": True}
    s.check("cut, 7 200 s past the window's end: None",
            paper.book_delay(cut, 7200, 0.04, rise, 10000.0, 0.005, 0.0005, t + 5 * h) is None)
    b = paper.book_delay(cut, 5, 0.04, rise, 10000.0, 0.005, 0.0005, t + 5 * h + 30000)
    s.check("cut, 5 s: exits at the window end's minute", b["src"]["exit_ms"] == t + 5 * h)
    b = paper.book_delay({"side": 1, "t_open": t + 10000, "t_close": t + 20000}, 5, 0.04, rise, 10000.0, 0.005, 0.0005,
                         t + 10 * h)
    s.check("an episode inside one minute: gross 0, fee 1.25", near(b["src"]["gross"], 0.0) and near(b["src"]["fee"], 1.25))
    # W8. funding
    rates = [(t + h, 0.0001), (t + 3 * h, 0.0002), (t + 9 * h, 0.5)]
    s.check("funding: two events, long pays 0.375",
            near(paper.funding_paid(1, 12.5, 100.0, t + 60000, t + 3 * h + 60000, rates), 0.375))
    s.check("funding: the short receives 0.375",
            near(paper.funding_paid(-1, 12.5, 100.0, t + 60000, t + 3 * h + 60000, rates), -0.375))
    s.check("funding: an event at hold_from is excluded, one at hold_to included",
            near(paper.funding_paid(1, 12.5, 100.0, t + h, t + 3 * h, rates), 0.25))
    # W9. sigma
    closes = [100.0]
    for i in range(30):
        closes.append(closes[-1] * (1.02 if i % 2 == 0 else 0.98))
    s.check("daily_sigma of alternating +-2 %: 0.02", near(paper.daily_sigma(closes), 0.02))
    # W10. the verdict rule
    picks, null10 = ["p1", "p2", "p3"], ["n%d" % i for i in range(10)]

    def res(values):
        return {a: {d: {"src": v, "stop": v} for d in paper.DELAYS_S} for a, v in values.items()}

    r = res(dict({a: 0.02 for a in picks}, **{a: 0.01 for a in null10}))
    v = paper.decide(picks, null10, r, 30)
    s.check("picks 0.02, null 0.01, 30 episodes: readable and passed", v["readable"] and v["passed"])
    s.check("120 subsets, share at or above TOP 0", v["cells"]["1800/stop"]["null_share_at_or_above"] == 0.0
            and near(v["cells"]["1800/stop"]["null_median"], 0.01))
    v = paper.decide(picks, null10, res(dict({a: -0.01 for a in picks}, **{a: -0.02 for a in null10})), 30)
    s.check("picks negative: readable, not passed", v["readable"] and not v["passed"])
    v = paper.decide(picks, null10, res(dict({a: 0.02 for a in picks}, **{a: 0.03 for a in null10})), 30)
    s.check("picks under the null: not passed, share 1.0", not v["passed"]
            and v["cells"]["7200/stop"]["null_share_at_or_above"] == 1.0)
    s.check("29 episodes: unreadable", not paper.decide(picks, null10, r, 29)["readable"])
    s.check("nine null accounts: unreadable", not paper.decide(picks, null10[:9], r, 30)["readable"])
    mixed = res(dict({a: 0.02 for a in picks}, **{a: 0.01 for a in null10}))
    for a in picks:
        mixed[a][7200]["stop"] = -0.01
    s.check("passing at 1 800 s and failing at 7 200 s: not passed", not paper.decide(picks, null10, mixed, 30)["passed"])
    s.check("starts: one pick and ten null accounts", paper.starts({"picks": picks[:1], "null": null10}))
    s.check("starts: not with nine null accounts or no pick",
            not paper.starts({"picks": picks, "null": null10[:9]}) and not paper.starts({"picks": [], "null": null10}))
    saved_wait, calls = paper.TRANSPORT_WAIT_S, []

    def flaky(n):
        calls.append(1)
        if len(calls) <= n:
            raise paper.Transport("HTTP 429")
        return "answer"

    try:
        paper.TRANSPORT_WAIT_S = 0
        with contextlib.redirect_stdout(io.StringIO()):
            s.check("retrying: an answer after two transport failures", paper.retrying(flaky, 2) == "answer")
            del calls[:]
            given = paper.retrying(flaky, 10 ** 6, give_up=True)
            s.check("retrying: one account is given up after TRANSPORT_MAX failures, None",
                    given is None and len(calls) == paper.TRANSPORT_MAX)
            try:
                paper.retrying(flaky, 10 ** 6)
                code = None
            except SystemExit as exc:
                code = exc.code
            s.check("retrying: a step the selection needs ends the process with 4", code == 4)
    finally:
        paper.TRANSPORT_WAIT_S = saved_wait
    s.check("nearest_rank: median 3, p95 5 of 1..5",
            paper.nearest_rank([5, 1, 3, 2, 4], 0.5) == 3 and paper.nearest_rank([5, 1, 3, 2, 4], 0.95) == 5)
    # W11. the alert texts
    rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
    t_open = int(datetime(2026, 10, 16, 10, 5, tzinfo=timezone.utc).timestamp() * 1000)
    ep = {"a": "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1", "coin": "HYPE", "symbol": "HYPEUSDT", "side": 1,
          "t_open": t_open, "px_open": "80.021"}
    head = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 14:05 "
            "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #1 0xf97a\u2026ddd1 ")
    s.check("the open alert, character for character", paper.alert_open(ep, 1, rule, 0.02) == head + (
        "\u043e\u0442\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 80.021 \u00b7 \u0441\u0442\u043e\u043f 4.0% "
        "\u2192 76.820 \u00b7 \u043e\u0431\u044a\u0451\u043c 1250 USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a"
        "\u0435 0.5% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430"))
    s.check("the open alert without a sigma", paper.alert_open(ep, 1, rule, None) == head + (
        "\u043e\u0442\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 80.021 \u00b7 \u0441\u0442\u043e\u043f \u0438 "
        "\u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: "
        "\u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance"))
    closed = dict(ep, t_close=t_open + (6 * 60 + 12) * 60000, px_close="82.10")
    s.check("the close alert after 6 h 12 min", paper.alert_close(closed, 1) == head.replace("14:05", "20:17") + (
        "\u0437\u0430\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 82.10 \u00b7 \u0432 \u043f\u043e\u0437"
        "\u0438\u0446\u0438\u0438 6.2 \u0447"))
    s.check("held 45 min", paper.held_text(45 * 60000) == "45 \u043c\u0438\u043d")
    # W12. the constants cut from index.html
    page = "var INV_FLOOR_SD = 2.0;   // x\nvar FEE_TAKER   = 0.0005;\n"
    s.check("cut_number on a page", common.cut_number(page, "INV_FLOOR_SD") == 2.0
            and common.cut_number(page, "FEE_TAKER") == 0.0005)
    for bad, label in ((page + "var FEE_TAKER = 0.001;\n", "twice"), ("var X = 1;\n", "absent")):
        try:
            common.cut_number(bad, "FEE_TAKER")
            raised = False
        except ValueError:
            raised = True
        s.check("cut_number raises on a constant defined %s" % label, raised)
    rule_live = paper.load_rule(REPO)
    with open(os.path.join(REPO, "analyst", "owner.json"), encoding="utf-8") as fh:
        owner = json.load(fh)
    s.check("load_rule reads owner.json's capital and medium risk",
            rule_live["capital_usdt"] == float(owner["capital"]["usdt"])
            and rule_live["risk_pct"] == float(owner["risk"]["risk_pct_medium"]))
    s.check("load_rule cuts two positive numbers from index.html",
            rule_live["inv_floor_sd"] > 0 and 0 < rule_live["fee_taker"] < 0.01)
    # W13. the unit and the manifest
    unit_path = os.path.join(HERE, "units", "crypto-paper.service")
    with open(unit_path, encoding="utf-8") as fh:
        lines = [line.rstrip("\n") for line in fh]
    creds = [line for line in lines if line.startswith("LoadCredential=")]
    s.check("crypto-paper.service runs as cryptopaper", "User=cryptopaper" in lines and "Group=cryptopaper" in lines)
    s.check("crypto-paper.service loads exactly the deploy key",
            creds == ["LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key"])
    s.check("crypto-paper.service runs paper.py from the deployer's clone, MemoryMax=128M",
            "ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/paper.py" in lines and "MemoryMax=128M" in lines)
    with open(os.path.join(HERE, "manifest"), encoding="utf-8") as fh:
        listed = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    s.check("the manifest lists crypto-paper.service once", listed.count("crypto-paper.service") == 1)
    with open(os.path.join(HERE, "units", "crypto-run.service"), encoding="utf-8") as fh:
        run_creds = [line.strip() for line in fh if line.startswith("LoadCredential=")]
    s.check("crypto-run.service still loads exactly its login and the deploy key", run_creds == [
        "LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token",
        "LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key"])
    # W14. the flow, offline: polls, the cut, three days of episodes, books, funding and the verdict
    section_w_flow(s)
    # W15. the booking's memory (TZ-65): one symbol's minutes at a time, compact, dropped after the pass
    section_w_memory(s)


def w_rows(path):
    """Synthetic data.binance.vision rows: 1m at a flat 100, daily closes alternating +-2 %, funding 0.0001 / 8 h."""
    name = path.rsplit("/", 1)[1][:-4]
    date = name.rsplit("-", 3)[-3:] if "-1m-" in name or "-1d-" in name else None
    if "-1m-" in name:
        start = paper.day_start("-".join(date))
        return [[str(m), "100", "100", "100", "100"] for m in range(start, start + paper.DAY_MS, 60000)]
    if "-1d-" in name:
        k = (paper.day_start("-".join(date)) // paper.DAY_MS) % 2
        return [[str(paper.day_start("-".join(date))), "0", "0", "0", "102" if k else "100"]]
    month = name.rsplit("-", 2)[-2:]
    start = paper.day_start("-".join(month) + "-01")
    return [[str(m), "8", "0.0001"] for m in range(start, start + 28 * paper.DAY_MS, 8 * 3600000)]


def section_w_flow(s):
    tmp = tempfile.mkdtemp(prefix="vps-selftest-w.")
    saved = common.OUTBOX_DIR
    try:
        outbox = os.path.join(tmp, "outbox")
        os.makedirs(outbox)
        common.OUTBOX_DIR = outbox
        p, n = "0x" + "a" * 40, "0x" + "b" * 40
        ff = paper.day_start("2026-01-05") + 3600000
        we = ff + 2 * paper.DAY_MS
        sel = {"picks": [{"address": p, "rank": 1}], "null": [{"address": n}], "follow_from_ms": ff,
               "window_end_ms": we, "follow_from": paper.iso(ff), "window_end": paper.iso(we), "symbols": ["BTCUSDT"]}
        state = paper.new_state(sel)
        rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
        inputs = paper.Inputs(tmp, "2026-03-01", rows=w_rows)
        h = 3600000
        # (account, fill, seen after): the pick's short is seen 601 s late and raises no alert; the
        # fill after the window's end is never applied.
        flow = ((p, w_fill(ff + h, 0, "B", 1), 10000), (p, w_fill(ff + 3 * h, 1, "A", 1), 10000),
                (n, w_fill(ff + 25 * h, 0, "B", 1), 10000), (n, w_fill(ff + 27 * h, 1, "A", 1), 10000),
                (p, w_fill(ff + 33 * h, 0, "A", 1), 601000), (p, w_fill(we + h, -1, "B", 1), 10000))
        for addr, f, late in flow:
            paper._apply(addr, state["accounts"][addr], [f], sel, {"BTCUSDT"}, f["time"] + late, rule, lambda: inputs)
        paper.gather_closed(state)
        alerts = sorted(x for x in os.listdir(outbox) if "-alert-" in x)
        s.check("two fresh alerts for the pick, none for the null, none late", len(alerts) == 2)
        for acct in state["accounts"].values():
            acct["polled_ms"] = we + paper.DAY_SETTLE_S * 1000
        paper.produce_days(state, tmp, sel, we)
        s.check("before the cut, the window's last day is not written", state["written"]["episodes"] == "2026-01-06")
        paper.cut_open(state, sel)
        paper.produce_days(state, tmp, sel, we)
        root = os.path.join(tmp, "records", paper.RECORD_DIR)
        days = ["2026-01-05", "2026-01-06", "2026-01-07"]
        eps = {d: [e for e in paper.read_jsonl(os.path.join(root, "episodes", d + ".jsonl")) if e["k"] == "ep"]
               for d in days}
        s.check("day 1: the pick's long", [(e["a"], e["side"], e["cut"]) for e in eps[days[0]]] == [(p, 1, False)])
        s.check("day 2: the null's long", [(e["a"], e["side"]) for e in eps[days[1]]] == [(n, 1)])
        s.check("day 3: the pick's short, cut at the window end with no price",
                [(e["a"], e["side"], e["cut"], e["t_close"], e["px_close"]) for e in eps[days[2]]] == [(p, -1, True, we, None)])
        paper.produce_books(state, tmp, sel, rule, inputs)
        paper.produce_funding(state, tmp, sel, inputs)
        s.check("the verdict is written once", paper.produce_verdict(state, tmp, sel, rule)
                and not paper.produce_verdict(state, tmp, sel, rule))
        with open(os.path.join(root, "verdict.json"), encoding="utf-8") as fh:
            verdict = json.load(fh)
        s.check("the verdict: two pick episodes and one null episode booked at 1 800 s",
                verdict["booked"]["1800"] == {"pick": 2, "null": 1})
        s.check("the verdict: unreadable, not passed", verdict["readable"] is False and verdict["passed"] is False)
        s.check("the verdict: on a flat price every cell is the fees and funding, negative",
                all(c["top"] < 0 for c in verdict["cells"].values()))
        s.check("ten records pending, each once", sorted(state["pending"]) == sorted(
            ["episodes/%s.jsonl" % d for d in days] + ["book/%s.jsonl" % d for d in days]
            + ["funding/%s.jsonl" % d for d in days] + ["verdict.json"]))
        paper.produce_days(state, tmp, sel, we)
        s.check("a second pass writes nothing", len(state["pending"]) == 10)
    finally:
        common.OUTBOX_DIR = saved
        shutil.rmtree(tmp, ignore_errors=True)


def w_counted_rows(reads, unpublished_from=None):
    """w_rows with every read counted by path; a 1m file dated unpublished_from or later is not
    published, and the day's rows come shuffled, with one row of each neighbouring day."""
    def rows(path):
        reads[path] = reads.get(path, 0) + 1
        name = path.rsplit("/", 1)[1][:-4]
        if "-1m-" not in name:
            return w_rows(path)
        date = "-".join(name.rsplit("-", 3)[-3:])
        if unpublished_from is not None and date >= unpublished_from:
            raise paper.NotPublished(path)
        start = paper.day_start(date)
        out = [[str(m), "100", "101", "99", repr(100 + (m - start) / 60000000.0)]
               for m in range(start, start + paper.DAY_MS, 60000)]
        stray = [[str(start - 60000), "1", "1", "1", "1"], [str(start + paper.DAY_MS), "1", "1", "1", "1"]]
        return out[1::2] + out[0::2] + stray
    return rows


def section_w_memory(s):
    tmp = tempfile.mkdtemp(prefix="vps-selftest-w15.")
    try:
        rows = paper.Rows(array.array("d", [1, 2, 3, 4, 5, 6, 7, 8]))
        s.check("Rows: two minutes of four doubles, read back as tuples",
                len(rows) == 2 and rows[0] == (1.0, 2.0, 3.0, 4.0) and rows[1] == (5.0, 6.0, 7.0, 8.0))
        raised = 0
        for k in (2, -1):
            try:
                rows[k]
            except IndexError:
                raised += 1
        s.check("Rows: a minute before the first or past the last raises IndexError", raised == 2)
        reads = {}
        inputs = paper.Inputs(tmp, "2026-03-01", rows=w_counted_rows(reads))
        times, flat = inputs.minutes("BTCUSDT", "2026-01-05")
        start = paper.day_start("2026-01-05")
        s.check("minutes: one day's 1 440 minutes ascending, the neighbouring days' rows left out",
                list(times) == list(range(start, start + paper.DAY_MS, 60000)))
        s.check("minutes: a minute's (o, h, l, c) where its time is",
                paper.Rows(flat)[731] == (100.0, 101.0, 99.0, 100 + 731 * 60000 / 60000000.0))
        tracemalloc.start()
        try:
            before = tracemalloc.get_traced_memory()[0]
            inputs.minutes("BTCUSDT", "2026-01-06")
            kept = tracemalloc.get_traced_memory()[0] - before
        finally:
            tracemalloc.stop()
        s.check("minutes: one symbol-day is kept in under 128 KiB", kept < 128 * 1024)
        kt, kr = inputs.kl("BTCUSDT", "2026-01-05", "2026-01-07")
        s.check("kl over three days: 4 320 minutes, ascending, each day where it belongs",
                len(kt) == 4320 == len(kr) and all(kt[k] < kt[k + 1] for k in range(len(kt) - 1))
                and kt[1440] == start + paper.DAY_MS and kr[1440][3] == 100.0)
        inputs.minutes("ETHUSDT", "2026-01-05")
        s.check("asking for another symbol drops the first one's days",
                inputs.kl_sym == "ETHUSDT" and list(inputs.klines) == [("ETHUSDT", "2026-01-05")])
        # a day file of three symbols, interleaved, five days each
        we = paper.day_start("2026-01-20") + 12 * 3600000
        sel = {"follow_from_ms": we - 14 * paper.DAY_MS, "window_end_ms": we}
        rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
        day = paper.utc_date(we)
        eps = []
        for k, sym in enumerate(["BTC", "ETH", "KAITO"] * 2):
            t_open = we - (5 - k % 2) * paper.DAY_MS + k * 60000
            eps.append({"k": "ep", "a": "0x%040x" % k, "role": "null", "rank": None, "coin": sym,
                        "symbol": sym + "USDT", "side": 1 if k % 2 else -1, "t_open": t_open, "px_open": "100",
                        "n": 1, "seen_open_ms": t_open, "t_close": we, "px_close": None, "seen_close_ms": None,
                        "cut": True})
        root = os.path.join(tmp, "records", paper.RECORD_DIR)
        os.makedirs(os.path.join(root, "episodes"))
        with open(os.path.join(root, "episodes", day + ".jsonl"), "w", encoding="utf-8") as fh:
            fh.write(json.dumps({"k": "day", "date": day}) + "\n" + "".join(json.dumps(e) + "\n" for e in eps))
        prev = paper.add_days(day, -1)

        def fresh_state():
            return {"pending": [], "written": {"episodes": day, "book": prev, "funding": prev}}

        reads, held = {}, []
        inputs = paper.Inputs(tmp, "2026-03-01", rows=w_counted_rows(reads))
        minutes = inputs.minutes

        def watched(sym, date):
            out = minutes(sym, date)
            held.append(len(inputs.klines))
            return out
        inputs.minutes = watched
        state = fresh_state()
        paper.produce_books(state, tmp, sel, rule, inputs)
        ones = [n for p, n in reads.items() if "/1m/" in p]
        s.check("a pass holds one symbol's days at most: six, of eighteen read", max(held) == 6 and len(ones) == 18)
        s.check("each minute file is read once in a pass", ones == [1] * 18)
        s.check("after the pass no minute is kept", inputs.klines == {} and inputs.kl_sym is None)
        with open(os.path.join(root, "book", day + ".jsonl"), encoding="utf-8") as fh:
            book = [json.loads(line) for line in fh][1:]
        s.check("the book keeps the episode file's order, all six booked",
                [(b["a"], b["coin"], b["t_open"]) for b in book] == [(e["a"], e["coin"], e["t_open"]) for e in eps]
                and all("d" in b for b in book))
        # the latest day not yet published: one minute read, then NotReady, nothing written, nothing kept
        reads = {}
        inputs = paper.Inputs(tmp, paper.add_days(day, 1), rows=w_counted_rows(reads, unpublished_from=day))
        state = fresh_state()
        try:
            paper.produce_books(state, tmp, sel, rule, inputs)
            waited = False
        except paper.NotReady:
            waited = True
        s.check("a latest day not yet published ends the pass after one read, nothing written or kept",
                waited and sum(reads.values()) == 1 and state["written"]["book"] == prev and inputs.klines == {})
        # the latest day absent (dated past ABSENT_AFTER_DAYS): the pass goes on, those episodes unbookable
        reads = {}
        inputs = paper.Inputs(tmp, paper.add_days(day, 10), rows=w_counted_rows(reads, unpublished_from=day))
        state = fresh_state()
        paper.produce_books(state, tmp, sel, rule, inputs)
        with open(os.path.join(root, "book", day + ".jsonl"), encoding="utf-8") as fh:
            head = json.loads(fh.readline())
        s.check("an absent latest day is no wait: the day is written, its six episodes unbookable",
                state["written"]["book"] == day and head["booked"] == 0 and head["unbookable"] == 6)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- X: the trend book (TZ-67): one replay decides live and over the archive -----------------
def x_world_long():
    """60 flat days, a close above the prior 55-day high, a steady trend, a close below the prior 20-day low."""
    bars = [(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(60)]
    bars.append((60 * book.DAY_MS, 100.0, 106.0, 100.0, 105.0))
    bars.append((61 * book.DAY_MS, 105.0, 107.0, 104.0, 106.0))
    for k in range(62, 100):
        c = 106.0 + (k - 61)
        bars.append((k * book.DAY_MS, c - 1, c + 1, c - 2, c))
    bars.append((100 * book.DAY_MS, 144.0, 144.5, 120.0, 121.0))
    for k in range(101, 105):
        bars.append((k * book.DAY_MS, 122.0, 123.0, 121.0, 122.0))
    return bars


def x_world_short():
    """60 flat days, a close below the prior 55-day low, a gap through the stop, then a breakout long."""
    bars = [(k * book.DAY_MS, 100.0, 101.0, 99.0, 100.0) for k in range(60)]
    bars.append((60 * book.DAY_MS, 100.0, 100.0, 94.0, 95.0))
    bars.append((61 * book.DAY_MS, 95.0, 96.0, 94.0, 95.0))
    bars.append((62 * book.DAY_MS, 103.0, 104.0, 102.0, 103.0))
    bars.append((63 * book.DAY_MS, 103.0, 104.0, 102.0, 103.0))
    bars.append((64 * book.DAY_MS, 103.0, 104.0, 102.0, 103.0))
    return bars


def section_x(s):
    eps = 1e-9
    trades, pos = book.replay(x_world_long())
    s.check("the long world makes exactly one trade", len(trades) == 1)
    tr = trades[0] if trades else {}
    s.check("a close above the prior 55-day high opens a long at the next open",
            tr.get("side") == 1 and tr.get("k_entry") == 61 and abs(tr.get("entry", 0) - 105.0) < eps)
    s.check("the stop sits 2 ATR(20) below the entry: 105 - 2 x 2.2", abs(tr.get("stop", 0) - 100.6) < eps)
    s.check("a close below the prior 20-day low closes it at the next open",
            tr.get("why") == "channel" and tr.get("k_exit") == 101 and abs(tr.get("exit", 0) - 122.0) < eps)
    s.check("the book ends flat", pos is None)
    want = (122.0 / 105.0 - 1 - 2 * book.COST_SIDE) / (4.4 / 105.0)
    s.check("its R after fees and slippage", bool(trades) and abs(book.result_r(tr, []) - want) < eps)
    t0, t1 = tr.get("t_entry", 0), tr.get("t_exit", 0)
    funding = [(t0, 0.5), (t0 + 1, 0.0001), (t1, 0.0002), (t1 + 1, 0.9)]
    want_f = (122.0 / 105.0 - 1 - 0.0003 - 2 * book.COST_SIDE) / (4.4 / 105.0)
    s.check("funding counts the prints after the entry and up to the exit, paid by the long",
            bool(trades) and abs(book.result_r(tr, funding) - want_f) < eps)
    lv = book.levels(x_world_long(), pos)
    s.check("flat: the next close's triggers are the last 55 days' extremes",
            lv["state"] == "flat" and lv.get("long_trigger") == 145.0 and lv.get("short_trigger") == 99.0)
    trades, pos = book.replay(x_world_short())
    tr = trades[0] if trades else {}
    s.check("a short stopped through a gap fills at the open",
            len(trades) == 1 and tr.get("side") == -1 and tr.get("why") == "stop" and abs(tr.get("exit", 0) - 103.0) < eps)
    s.check("the stop day's close opens the next trade",
            pos is not None and pos["side"] == 1 and pos["k_entry"] == 63 and abs(pos["entry"] - 103.0) < eps)
    s.check("its stop: 103 - 2 x 2.55", pos is not None and abs(pos["stop"] - 97.9) < eps)
    lv = book.levels(x_world_short(), pos)
    s.check("in a trade: the state, the entry day, and the exit level of the last 20 days",
            lv["state"] == "long" and lv.get("entry_date") == "1970-03-05" and lv.get("exit_level") == 94.0
            and abs(lv.get("r_open", 1)) < eps)
    # TZ-68: the morning after a signal's close, the entry is due at the forming day's open -- the very
    # position the next close records, so the live state and the archive's record are one book.
    for name, world, n, fill in (("a breakout close on the last bar is due at the forming open", x_world_long(), 61, 105.0),
                                 ("a stop day's close on the last bar is due too", x_world_short(), 63, 103.0)):
        due, then = book.replay(world[:n], fill)[1], book.replay(world[:n + 1])[1]
        s.check(name + ": the position the next close records",
                due is not None and then is not None and due.get("entry_due") is True and then.get("entry_due") is False
                and all(due[f] == then[f] for f in ("side", "k_entry", "t_entry", "entry", "stop")))
    lv = book.levels(x_world_long()[:61], book.replay(x_world_long()[:61], 105.5)[1])
    s.check("a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet",
            lv["state"] == "long" and lv.get("entry_due") is True and lv.get("entry_date") == "1970-03-03"
            and lv.get("entry") == 105.5 and abs(lv.get("stop", 0) - 101.1) < eps and lv.get("r_open", 0) is None)
    saved = book._get
    tmp = tempfile.mkdtemp(prefix="vps-selftest-x.")
    try:
        rows = [[k * book.DAY_MS, str(k + 1), "9", "0.5", "1.5", "0", (k + 1) * book.DAY_MS - 1] for k in range(3)]
        book._get = lambda url: json.dumps(rows).encode()
        bars, open_now = book.live_bars("XUSDT", 2 * book.DAY_MS + 5)
        s.check("live bars drop the day still open and keep its open", len(bars) == 2 and open_now == 3.0)
        world = x_world_long()

        def as_rows(bars, fill):
            closed = [[b[0], str(b[1]), str(b[2]), str(b[3]), str(b[4]), "0", b[0] + book.DAY_MS - 1] for b in bars]
            forming = [bars[-1][0] + book.DAY_MS, str(fill), str(fill + 1), str(fill - 1), str(fill + 0.25), "0", 10 ** 15]
            return json.dumps(closed + [forming]).encode()

        def fake(url):
            if "BADUSDT" in url:
                raise OSError("refused")
            return as_rows(world[:61], 105.5) if "DUEUSDT" in url else as_rows(world, 122.0)
        book._get = fake
        with contextlib.redirect_stdout(io.StringIO()) as out:
            code = book.main(["--live", "GOODUSDT", "BADUSDT", "DUEUSDT"])
        lines = [json.loads(l) for l in out.getvalue().splitlines()]
        s.check("--live prints one object per symbol and survives one symbol's failure",
                code == 0 and [l["symbol"] for l in lines] == ["GOODUSDT", "BADUSDT", "DUEUSDT"]
                and lines[0]["state"] == "flat" and lines[1]["state"] == "unread")
        s.check("--live names the entry due at the forming day's open, and its stop",
                len(lines) == 3 and lines[2]["state"] == "long" and lines[2].get("entry_due") is True
                and lines[2].get("entry") == 105.5 and abs(lines[2].get("stop", 0) - 101.1) < eps)
        served = {}

        def vision(url):
            if url in served:
                return served[url]
            raise urllib.error.HTTPError(url, 404, "Not Found", None, None)

        def january(skip):
            t0 = int(datetime(2023, 1, 1, tzinfo=timezone.utc).timestamp() * 1000)
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as z:
                z.writestr("k.csv", "open_time,open,high,low,close\n" + "".join(
                    "%d,1,2,0.5,1.5\n" % (t0 + d * book.DAY_MS) for d in range(31) if d != skip))
            return buf.getvalue()
        book._get = vision
        served[book.ARCHIVE + "/monthly/klines/XUSDT/1d/XUSDT-1d-2023-01.zip"] = january(None)
        served[book.ARCHIVE + "/monthly/klines/YUSDT/1d/YUSDT-1d-2023-01.zip"] = january(14)
        whole = len(book.archive_series("XUSDT", book.date(2023, 1, 1), book.date(2023, 1, 31), tmp)[0]) == 31
        try:
            book.archive_series("YUSDT", book.date(2023, 1, 1), book.date(2023, 1, 31), tmp)
            refused = ""
        except ValueError as exc:
            refused = str(exc)
        s.check("a day missing from the archive is refused, never replayed over: the symbol and the days around it",
                whole and refused == "YUSDT: the archive has no daily bar between 2023-01-14 and 2023-01-16")
    finally:
        book._get = saved
        shutil.rmtree(tmp, ignore_errors=True)


# --- Y: the ETF lane (TZ-69) against stubbed answers, no network ---------------------------
Y_KEY = "SOSO-selftest-fake-key-0123456789abcdef"
Y_LINE = re.compile(r"etf: read=\d+ refused=\d+ written=(yes|no) newest=(\d{4}-\d\d-\d\d|-)")


class YAnswer:
    def __init__(self, status, body):
        self.status, self.body = status, body

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def read(self):
        return self.body


def y_row(date, net, traded="1000.5", assets="2000.25", cum="-300"):
    row = {"date": date, "totalNetInflow": net, "totalValueTraded": traded, "cumNetInflow": cum}
    if assets is not None:
        row["totalNetAssets"] = assets
    return row


def y_opener(answer):
    """A stub urlopen serving one answer: (status, body), or an exception it raises."""
    def urlopen(req, timeout=None):
        if isinstance(answer, BaseException):
            raise answer
        return YAnswer(*answer)
    return urlopen


def y_refusal(etf_type, answer):
    """read_type's refusal for one stubbed answer, or None when it reads."""
    try:
        etf.read_type(etf_type, Y_KEY, y_opener(answer))
    except etf.Refused as exc:
        return str(exc)
    return None


def y_body(data, code=0):
    return 200, json.dumps({"code": code, "msg": "success", "data": data}).encode("utf-8")


def y_run(tmp, answers, key=Y_KEY, out_name="etf.json"):
    """etf.main against answers {type: (status, body) or an exception}: (exit, printed, calls, out)."""
    creds = os.path.join(tmp, "creds")
    os.makedirs(creds, exist_ok=True)
    cred = os.path.join(creds, etf.CREDENTIAL)
    if os.path.exists(cred):
        os.unlink(cred)
    if key is not None:
        with open(cred, "w", encoding="utf-8") as fh:
            fh.write(key + "\n")
    calls = []

    def urlopen(req, timeout=None):
        calls.append((req, timeout))
        return y_opener(answers[json.loads(req.data.decode("utf-8"))["type"]])(req, timeout)

    out = os.path.join(tmp, out_name)
    saved = os.environ.get("CREDENTIALS_DIRECTORY")
    os.environ["CREDENTIALS_DIRECTORY"] = creds
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = etf.main(["--out", out], urlopen=urlopen)
    finally:
        if saved is None:
            os.environ.pop("CREDENTIALS_DIRECTORY", None)
        else:
            os.environ["CREDENTIALS_DIRECTORY"] = saved
    return code, buf.getvalue(), calls, out


def unit_lines(name):
    with open(os.path.join(HERE, "units", name), encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


def section_y(s):
    btc, eth, sol = etf.TYPES
    s.check("TYPES are us-btc-spot, us-eth-spot, us-sol-spot", etf.TYPES == ("us-btc-spot", "us-eth-spot", "us-sol-spot"))
    rows = [y_row("2026-10-20", "125.5"), y_row("2026-10-17", "-40"), y_row("2026-10-16", "7")]
    first = etf.entry({"code": 0, "data": rows})
    last = etf.entry({"code": 0, "data": list(reversed(rows))})
    s.check("newest row from a newest-first list: 2026-10-20, net 125.5",
            first["date"] == "2026-10-20" and first["net"] == 125.5)
    s.check("newest row from an oldest-first list: 2026-10-20, net 125.5",
            last["date"] == "2026-10-20" and last["net"] == 125.5)
    skipped = etf.entry({"code": 0, "data": [y_row("2026-10-16", "7"), y_row("2026-10-21", None),
                                             y_row("2026-10-22", "NaN"), y_row("2026/10/23", "1"),
                                             y_row("2026-10-18", 3)]})
    s.check("a later date whose net is absent, NaN or whose date is not YYYY-MM-DD is passed over",
            skipped["date"] == "2026-10-18" and skipped["net"] == 3.0 and skipped["rows"] == 5)
    s.check("ETF_DAYS is 3", etf.ETF_DAYS == 3)
    four = [y_row("2026-10-20", "125.5"), y_row("2026-10-19", "-40"), y_row("2026-10-17", "7"),
            y_row("2026-10-16", "9")]
    want = [{"date": "2026-10-20", "net": 125.5}, {"date": "2026-10-19", "net": -40.0},
            {"date": "2026-10-17", "net": 7.0}]
    s.check("days from four rows newest-first: the three greatest dates, newest first, each with its net",
            etf.entry({"code": 0, "data": four})["days"] == want)
    s.check("days from the same four rows oldest-first: the same three, newest first",
            etf.entry({"code": 0, "data": list(reversed(four))})["days"] == want)
    s.check("days passes over a date not YYYY-MM-DD, an absent net and a NaN net: valid rows only, newest first",
            skipped["days"] == [{"date": "2026-10-18", "net": 3.0}, {"date": "2026-10-16", "net": 7.0}])
    s.check("days from two valid rows holds two entries",
            etf.entry({"code": 0, "data": four[:2]})["days"] == want[:2])
    s.check("days from one valid row holds one entry",
            etf.entry({"code": 0, "data": four[:1]})["days"] == want[:1])
    twice = etf.entry({"code": 0, "data": [y_row("2026-10-20", "1"), y_row("2026-10-20", "2"),
                                           y_row("2026-10-19", "5")]})
    s.check("a date given twice with two nets: one entry for it, carrying the first one's net",
            twice["days"] == [{"date": "2026-10-20", "net": 1.0}, {"date": "2026-10-19", "net": 5.0}])
    s.check("a date given twice: days[0] equals the entry's date and net",
            twice["days"][0] == {"date": twice["date"], "net": twice["net"]})
    tmp = tempfile.mkdtemp(prefix="vps-selftest-y.")
    try:
        # Each refusal of the closed vocabulary from its own stubbed answer; none read.
        code, printed, calls, out = y_run(tmp, {
            btc: urllib.error.HTTPError(etf.URL, 503, "unavailable", {}, None),
            eth: TimeoutError("timed out"),
            sol: (200, b"<html>challenge</html>")})
        s.check("none read: exit 4", code == 4)
        s.check("none read: nothing written", not os.path.exists(out))
        s.check("none read: the line reads read=0 refused=3 written=no newest=-",
                printed == "etf: read=0 refused=3 written=no newest=-\n")
        s.check("an HTTP error is refused as HTTP 503",
                y_refusal(btc, urllib.error.HTTPError(etf.URL, 503, "unavailable", {}, None)) == "HTTP 503")
        s.check("a transport failure is refused as transport TimeoutError",
                y_refusal(eth, TimeoutError("timed out")) == "transport TimeoutError")
        s.check("a body that does not parse is refused as unparseable",
                y_refusal(sol, (200, b"<html>challenge</html>")) == "unparseable")
        standing = os.path.join(tmp, "standing.json")
        with open(standing, "w", encoding="utf-8") as fh:
            fh.write('{"v":1,"ts":"2026-10-20T10:07:00Z"}\n')
        code, printed, calls, out = y_run(tmp, {btc: y_body(rows, code=40001), eth: y_body([]),
                                                sol: (200, json.dumps({"code": 0, "data": {"x": 1}}).encode())},
                                          out_name="standing.json")
        with open(standing, encoding="utf-8") as fh:
            kept = fh.read()
        s.check("none read over a standing record: exit 4 and the record left as it stood",
                code == 4 and kept == '{"v":1,"ts":"2026-10-20T10:07:00Z"}\n')
        s.check("a code other than 0 is refused as code 40001", y_refusal(btc, y_body(rows, code=40001)) == "code 40001")
        s.check("an empty data list is refused as no row", y_refusal(eth, y_body([])) == "no row")
        s.check("data that is not a list is refused as unparseable",
                y_refusal(sol, (200, b'{"code":0,"data":{}}')) == "unparseable")
        s.check("a status other than 200 is refused as HTTP 204", y_refusal(btc, (204, b"")) == "HTTP 204")
        # One type read and two refused.
        code, printed, calls, out = y_run(tmp, {
            btc: y_body([y_row("2026-10-17", "-40"), y_row("2026-10-20", "125.5", assets=None), y_row("2026-10-16", 7)]),
            eth: urllib.error.HTTPError(etf.URL, 429, "too many", {}, None),
            sol: y_body([y_row("2026-10-20", "NaN"), y_row("2026-10-19", None)])})
        with open(out, encoding="utf-8") as fh:
            text = fh.read()
        record = json.loads(text)
        s.check("one read, two refused: exit 0", code == 0)
        s.check("the line reads read=1 refused=2 written=yes newest=2026-10-20",
                printed == "etf: read=1 refused=2 written=yes newest=2026-10-20\n")
        s.check("the printed line is exactly one line of the fixed shape",
                printed.count("\n") == 1 and Y_LINE.fullmatch(printed.rstrip("\n")) is not None)
        s.check("record keys v k ts provider host types refused, in order",
                list(record) == ["v", "k", "ts", "provider", "host", "types", "refused"])
        s.check("record v 1, k etf, provider SoSoValue, host openapi.sosovalue.com",
                (record["v"], record["k"], record["provider"], record["host"])
                == (1, "etf", "SoSoValue", "openapi.sosovalue.com"))
        s.check("record ts is ISO-8601 Z", re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", record["ts"]) is not None)
        s.check("types holds the one type read, refused the two others",
                list(record["types"]) == [btc] and record["refused"] == {eth: "HTTP 429", sol: "no row"})
        read_entry = dict(record["types"][btc])
        read_days = read_entry.pop("days", None)
        s.check("the type's entry: date, net, traded, assets, cum, rows cast, an absent field null",
                read_entry == {"date": "2026-10-20", "net": 125.5, "traded": 1000.5, "assets": None,
                               "cum": -300.0, "rows": 3})
        s.check("the written record's entry carries days: three sessions, newest first, each with its net",
                read_days == [{"date": "2026-10-20", "net": 125.5}, {"date": "2026-10-17", "net": -40.0},
                              {"date": "2026-10-16", "net": 7.0}])
        s.check("the written record's days[0] equals that entry's date and net",
                bool(read_days) and read_days[0] == {"date": read_entry["date"], "net": read_entry["net"]})
        s.check("the record's mode is 0640", os.stat(out).st_mode & 0o7777 == 0o640)
        s.check("three requests, one per type, in TYPES order",
                [json.loads(req.data.decode("utf-8")) for req, _ in calls] == [{"type": t} for t in etf.TYPES])
        s.check("each request is a POST to the historicalInflowChart URL with timeout 40",
                len(calls) == 3 and all(req.get_method() == "POST" and req.full_url == etf.URL
                    == "https://openapi.sosovalue.com/openapi/v2/etf/historicalInflowChart" and timeout == 40
                    for req, timeout in calls))
        s.check("the key travels in the x-soso-api-key header, with Content-Type application/json",
                len(calls) == 3 and all(req.get_header("X-soso-api-key") == Y_KEY
                    and req.get_header("Content-type") == "application/json" for req, _ in calls))
        s.check("the key is in no URL and no body",
                len(calls) == 3 and all(Y_KEY not in req.full_url and Y_KEY.encode() not in req.data
                                        for req, _ in calls))
        s.check("the key is absent from the printed line", Y_KEY not in printed and "<redacted>" not in printed)
        s.check("the key is absent from the record", Y_KEY not in text)
        # The key absent or empty: exit 3, no request made, nothing written.
        for label, key in (("absent", None), ("empty", " \n")):
            code, printed, calls, out = y_run(tmp, {}, key=key, out_name="nokey.json")
            s.check("key %s: exit 3, no request made, nothing written" % label,
                    code == 3 and calls == [] and not os.path.exists(out))
        saved = os.environ.pop("CREDENTIALS_DIRECTORY", None)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                code = etf.main(["--out", os.path.join(tmp, "nodir.json")],
                                urlopen=lambda *a, **k: calls.append(a))
        finally:
            if saved is not None:
                os.environ["CREDENTIALS_DIRECTORY"] = saved
        s.check("no CREDENTIALS_DIRECTORY: exit 3, no request made",
                code == 3 and calls == [] and not os.path.exists(os.path.join(tmp, "nodir.json")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    s.check("the default record is /var/lib/crypto-auto/etf.json", etf.OUT == "/var/lib/crypto-auto/etf.json")
    # The units and the manifest.
    service, timer = unit_lines("crypto-etf.service"), unit_lines("crypto-etf.timer")
    s.check("service runs as User=cryptoauto, Group=cryptoauto",
            service.count("User=cryptoauto") == 1 and service.count("Group=cryptoauto") == 1
            and len([x for x in service if x.startswith(("User=", "Group="))]) == 2)
    s.check("service carries exactly one LoadCredential=, the SoSoValue key's",
            [x for x in service if x.startswith("LoadCredential")]
            == ["LoadCredential=sosovalue-api-key:/etc/crypto-auto/credentials/sosovalue-api-key"])
    s.check("service is Type=oneshot",
            [x for x in service if x.startswith("Type=")] == ["Type=oneshot"])
    s.check("service has no [Install] section", "[Install]" not in service)
    s.check("service runs /usr/bin/python3 /srv/crypto-auto/vps/etf.py",
            [x for x in service if x.startswith("ExecStart")] == ["ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/etf.py"])
    s.check("timer fires at OnCalendar=*-*-* *:07:00 UTC, Persistent=true",
            [x for x in timer if x.startswith("OnCalendar")] == ["OnCalendar=*-*-* *:07:00 UTC"]
            and "Persistent=true" in timer)
    s.check("timer's unit is crypto-etf.service", [x for x in timer if x.startswith("Unit=")] == ["Unit=crypto-etf.service"])
    s.check("timer has [Install] WantedBy=timers.target", "[Install]" in timer and "WantedBy=timers.target" in timer)
    with open(os.path.join(HERE, "manifest"), encoding="utf-8") as fh:
        listed = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    s.check("the manifest lists crypto-etf.timer once", listed.count("crypto-etf.timer") == 1)
    s.check("the manifest does not list crypto-etf.service", "crypto-etf.service" not in listed)


SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
            ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
            ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
            ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
            ("T", section_t), ("U", section_u), ("V", section_v), ("W", section_w), ("X", section_x),
            ("Y", section_y))


def main():
    total = failed = empty = 0
    for name, fn in SECTIONS:
        s = Section(name)
        try:
            fn(s)
        except Exception as exc:
            s.failed += 1
            sys.stderr.write("FAIL section %s raised %s: %s\n" % (name, exc.__class__.__name__, common.redact(exc)))
        print("section %s: checks %d failed %d" % (name, s.checks, s.failed), flush=True)
        total += s.checks
        failed += s.failed
        empty += 1 if s.checks == 0 else 0
    print("selftest: sections %d checks %d failed %d empty %d" % (len(SECTIONS), total, failed, empty), flush=True)
    return 1 if failed or empty else 0


if __name__ == "__main__":
    sys.exit(main())
