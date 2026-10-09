#!/usr/bin/env python3
"""The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
TZ-62 B2): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's, TZ-57 §12.8's,
TZ-58 §12.7's, TZ-60 §12.11's and TZ-62 §12.4's changed and new ones, each printing `section <X>:
checks <n> failed <m>`, then the total.

    python3 vps/selftest.py

Exit non-zero on any failure and on any section that compared nothing (inv. 22).
Offline: every fixture is built here or read from the checkout this file sits in.
"""
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
import types
import urllib.parse
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import announce  # noqa: E402
import bot  # noqa: E402
import cleanup  # noqa: E402
import common  # noqa: E402
import exchange  # noqa: E402
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
json.dump({"type": "result", "subtype": "stub_subtype", "is_error": False, "result": "SELFTEST-O-RESULT-TEXT",
           "num_turns": 3, "duration_ms": 1234, "api_error_status": 418, "terminal_reason": "stub_terminal",
           "stop_reason": "stub_stop", "modelUsage": {}, "permission_denials": [],
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
    tmp = tempfile.mkdtemp(prefix="vps-selftest-o.")
    env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", run.LOGIN_ENV,
                "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW")
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
                           "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": writer_saw})
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
        for field, value in (("subtype", "stub_subtype"), ("api_error_status", "418"),
                             ("terminal_reason", "stub_terminal"), ("stop_reason", "stub_stop")):
            s.check("the summary carries %s=%s" % (field, value), (" %s=%s" % (field, value)) in summary)
        s.check("the summary never carries the result", "SELFTEST-O-RESULT-TEXT" not in summary)
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


SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
            ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
            ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
            ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
            ("T", section_t))


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
