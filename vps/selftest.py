#!/usr/bin/env python3
"""The VPS assistant's selftest (TZ-54 B10): the sections of TZ-54 §12.14, each
printing `section <X>: checks <n> failed <m>`, then the total.

    python3 vps/selftest.py

Exit non-zero on any failure and on any section that compared nothing (inv. 22).
Offline: every fixture is built here or read from the checkout this file sits in.
"""
import copy
import json
import os
import re
import shutil
import sys
import tempfile
import time
import urllib.parse
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import announce  # noqa: E402
import bot  # noqa: E402
import cleanup  # noqa: E402
import common  # noqa: E402
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


# --- J: derive_limits ---------------------------------------------------------------
def section_j(s):
    s.check("derive_limits(400 MiB, 1200 s)", common.derive_limits(400 * MiB, 1200) == (637534208, 5400))
    s.check("derive_limits(100 MiB, 2100 s)", common.derive_limits(100 * MiB, 2100) == (167772160, 6000))


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
def read_record(path):
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                out[key] = value
    return out


def unit_value(path, key):
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith(key + "="):
                return line.strip().split("=", 1)[1]
    return None


def section_m(s):
    record_path = os.path.join(HERE, "memory-record.txt")
    unit_path = os.path.join(HERE, "units", "crypto-run.service")
    manifest_path = os.path.join(HERE, "manifest")
    if not (os.path.exists(record_path) and os.path.exists(unit_path) and os.path.exists(manifest_path)):
        sys.stderr.write("section M: memory-record.txt, crypto-run.service or manifest absent\n")
        return
    r = read_record(record_path)
    n = {k: int(v) for k, v in r.items() if re.fullmatch(r"-?\d+", v)}
    with open(manifest_path, encoding="utf-8") as fh:
        listed = {line.strip() for line in fh if line.strip() and not line.startswith("#")}
    s.check("run_footprint_bytes = max(cgroup, hwm)",
            n["run_footprint_bytes"] == max(n["run_cgroup_footprint_bytes"], n["run_process_hwm_bytes"]))
    s.check("host_free_bytes = mem_available + session_rss",
            n["host_free_bytes"] == n["mem_available_bytes"] + n["session_rss_bytes"])
    limits = common.derive_limits(n["run_footprint_bytes"], r["run_duration_s"])
    s.check("derive_limits(run_footprint, run_duration) equals the record",
            limits == (n["memory_max_bytes"], n["runtime_max_s"]))
    s.check("MemoryMax= equals memory_max_bytes", unit_value(unit_path, "MemoryMax") == str(limits[0]))
    s.check("RuntimeMaxSec= equals runtime_max_s", unit_value(unit_path, "RuntimeMaxSec") == str(limits[1]))
    fits = "yes" if r["run_completed"] == "yes" and n["memory_max_bytes"] <= n["host_free_bytes"] else "no"
    s.check("fits equals the rule", r["fits"] == fits)
    s.check("hog_footprint_bytes >= hog_bytes", n["hog_footprint_bytes"] >= n["hog_bytes"])
    for unit in ("crypto-run.timer", "crypto-run.path"):
        s.check("manifest lists %s exactly when fits=yes" % unit, (unit in listed) == (r["fits"] == "yes"))


SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
            ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
            ("K", section_k), ("L", section_l), ("M", section_m))


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
