#!/usr/bin/env python3
"""The announcement watcher (TZ-54 B6, TZ-56 B3): Binance's announcement stream
held on the read-only key, after the key's own rights were read from the exchange.
The topic in the signed query is the subscription: the stream answers
REGISTER/SUCCESS to a connection that sends no command (TZ-56 A5, branch R1).

    announce.py [--state-dir <dir>]                    the service
    announce.py --measure <seconds> <max_data> [...]   key check and stream, no outbox, no requests

--measure exits 0 when at least one message carried all six fields, 2 when none
did, 3 on a refused key, 4 when connecting or subscribing failed. The service
exits 3 on a refused key (RestartPreventExitStatus=3). Imports `websocket` from
Ubuntu's python3-websocket (TZ-54 rule 7); everything else is the standard library.
"""
import argparse
import hashlib
import hmac
import http.client
import json
import os
import re
import secrets
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

RESTRICTIONS_URL = "https://api.binance.com/sapi/v1/account/apiRestrictions"
STREAM_URL = "wss://api.binance.com/sapi/wss"
TOPIC = "com_announcement_en"
# TZ-56 A5, branch R1: the COMMAND answer a connection waits for.
ANSWER_SUBTYPE = "REGISTER"
FIELDS = ("catalogId", "catalogName", "publishDate", "title", "body", "disclaimer")
PING_S = 30
REFRESH_S = 23 * 3600 + 30 * 60          # a fresh connection before 23 h 30 min
RECONNECT_FIRST_S, RECONNECT_MAX_S = 5, 300
RECORD = "announcements.jsonl"
TBILISI = ZoneInfo("Asia/Tbilisi")
EXIT_COMPLETE, EXIT_NONE, EXIT_REFUSED, EXIT_CONNECT = 0, 2, 3, 4


# --- TZ-54 §12.10: signing ------------------------------------------------------
def query_string(params):
    """Parameters sorted by name and joined name=value with &."""
    return "&".join("%s=%s" % (name, params[name]) for name in sorted(params))


def sign(secret, payload):
    """HMAC-SHA256 of exactly the string, under the secret, lowercase hex."""
    return hmac.new(secret.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).hexdigest()


def signed_query(params, secret):
    q = query_string(params)
    return q + "&signature=" + sign(secret, q)


# --- TZ-54 §12.9: the key's rights ---------------------------------------------
def verdict(doc):
    """ACCEPTED only when ipRestrict is true, enableReading is true, and every
    other field named enable* or permits* is false; enableFixReadOnly alone may
    take either value. An unknown field falls under the same rule."""
    if not isinstance(doc, dict) or doc.get("ipRestrict") is not True or doc.get("enableReading") is not True:
        return "REFUSED"
    for name, value in doc.items():
        if name in ("enableReading", "enableFixReadOnly"):
            continue
        if (name.startswith("enable") or name.startswith("permits")) and value is not False:
            return "REFUSED"
    return "ACCEPTED"


def key_check(key, secret):
    """Returns (verdict, printable fields) — verdict ACCEPTED, REFUSED, or ERROR
    when the exchange answered no restrictions object."""
    url = RESTRICTIONS_URL + "?" + signed_query({"recvWindow": 5000, "timestamp": int(time.time() * 1000)}, secret)
    req = urllib.request.Request(url, headers={"X-MBX-APIKEY": key})
    try:
        with urllib.request.urlopen(req, timeout=common.HTTP_TIMEOUT_S) as resp:
            doc = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        try:
            body = json.loads(exc.read())
        except ValueError:
            body = {}
        detail = "http=%d code=%s msg=%s" % (exc.code, body.get("code", "-"), body.get("msg", "-"))
        return ("REFUSED" if 400 <= exc.code < 500 else "ERROR"), common.redact(detail)
    except (OSError, ValueError, http.client.HTTPException) as exc:
        return "ERROR", common.redact(exc.__class__.__name__)
    fields = " ".join("%s=%s" % (k, str(v).lower()) for k, v in doc.items() if isinstance(v, bool))
    return verdict(doc), fields


# --- TZ-54 §12.5: the title matcher --------------------------------------------
def _word(ticker):
    if len(ticker) == 1:
        return re.compile(r"\(" + re.escape(ticker) + r"\)")
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(ticker) + r"(?![A-Za-z0-9])")


def _first(title, pairs):
    best = None
    for ticker, symbol in pairs:
        for pattern in (_word(ticker), _word(symbol) if len(symbol) > 1 else None):
            if pattern is None:
                continue
            m = pattern.search(title)
            if m and (best is None or m.start() < best[0]):
                best = (m.start(), ticker)
    return best


def match_title(title, list_pairs, perpetual_pairs):
    """(class, ticker): a list match wins over a perpetual match."""
    hit = _first(title, list_pairs)
    if hit:
        return "list", hit[1]
    hit = _first(title, perpetual_pairs)
    if hit:
        return "perpetual", hit[1]
    return "none", None


def list_pairs():
    """List tickers are tokens[].name and BTC, with their full symbols."""
    return [("BTC", "BTCUSDT")] + [(row["name"], row["s"]) for row in common.read_tokens()]


def perpetual_pairs(state_dir):
    try:
        with open(os.path.join(state_dir, "perpetuals.json"), encoding="utf-8") as fh:
            return [(row["base"], row["symbol"]) for row in json.load(fh) if row.get("base")]
    except (OSError, ValueError, KeyError, TypeError):
        return []


# --- the stream -----------------------------------------------------------------
def answer_of(frames, sub_type):
    """(answer, pending, skipped) from raw frames: `answer` the first COMMAND frame
    whose subType equals sub_type, or None when the frames end first; `pending` the
    raw non-COMMAND frames before it; `skipped` the COMMAND frames of another
    subType. Reads no frame after the answer."""
    pending, skipped = [], []
    for raw in frames:
        try:
            doc = json.loads(raw) if raw else {}
        except ValueError:
            doc = {}
        if isinstance(doc, dict) and doc.get("type") == "COMMAND":
            if doc.get("subType") == sub_type:
                return doc, pending, skipped
            skipped.append(doc)
            continue
        pending.append(raw)
    return None, pending, skipped


def frames_until(ws, deadline):
    """Text frames of one connection until the monotonic deadline."""
    import websocket  # python3-websocket
    while True:
        left = deadline - time.monotonic()
        if left <= 0:
            return
        ws.settimeout(left)
        try:
            raw = ws.recv()
        except websocket.WebSocketTimeoutException:
            return
        yield raw


class Stream:
    def __init__(self, key, secret):
        self.key, self.secret = key, secret
        self.ws = None
        self.opened = self.last_attempt = self.last_ping = 0.0
        self.pings = self.reconnects = 0
        self.close_codes = []
        self.subscribe_answer = None
        self.pending = []

    def connect(self):
        """Open with the signed query, whose topic is the subscription, and the key
        header; send no command; record the answer. Returns True when the
        ANSWER_SUBTYPE answer arrives inside 20 s with data SUCCESS."""
        import websocket  # python3-websocket
        wait = RECONNECT_FIRST_S - (time.monotonic() - self.last_attempt)
        if self.last_attempt and wait > 0:
            time.sleep(wait)                     # never twice inside 5 s
        self.last_attempt = time.monotonic()
        params = {"random": secrets.token_hex(16), "recvWindow": 60000,
                  "timestamp": int(time.time() * 1000), "topic": TOPIC}
        self.subscribe_answer = None
        try:
            self.ws = websocket.create_connection(STREAM_URL + "?" + signed_query(params, self.secret),
                                                  header=["X-MBX-APIKEY: " + self.key],
                                                  timeout=common.HTTP_TIMEOUT_S)
            deadline = time.monotonic() + common.HTTP_TIMEOUT_S
            answer, pending, skipped = answer_of(frames_until(self.ws, deadline), ANSWER_SUBTYPE)
        except Exception as exc:
            common.log("announce: connect failed (%s)" % common.redact(exc.__class__.__name__))
            self.close()
            return False
        self.pending.extend(pending)
        for doc in skipped:
            common.log("announce: command answer %s" % json.dumps(doc, sort_keys=True))
        self.subscribe_answer = answer
        common.log("announce: subscribe answer %s" % json.dumps(self.subscribe_answer, sort_keys=True))
        if answer is None or answer.get("data") != "SUCCESS":
            self.close()
            return False
        self.ws.settimeout(1.0)
        self.opened = self.last_ping = time.monotonic()
        return True

    def close(self):
        if self.ws is not None:
            try:
                self.ws.close()
            except Exception:
                pass
        self.ws = None

    def take_pending(self):
        pending, self.pending = self.pending, []
        return pending

    def frames(self, stop):
        """Text messages until stop() is true: a ping frame every 30 s, a fresh
        connection before 23 h 30 min, and after a close a reconnect at 5 s
        doubling to 300 s."""
        import websocket
        delay = RECONNECT_FIRST_S
        for raw in self.take_pending():
            yield raw
        while not stop():
            if self.ws is None:
                end = time.monotonic() + delay
                while time.monotonic() < end and not stop():
                    time.sleep(1.0)
                if stop():
                    break
                if self.connect():
                    self.reconnects += 1
                    delay = RECONNECT_FIRST_S
                    for raw in self.take_pending():
                        yield raw
                else:
                    delay = min(RECONNECT_MAX_S, delay * 2)
                continue
            now = time.monotonic()
            if now - self.opened >= REFRESH_S:
                common.log("announce: planned refresh after %d s" % int(now - self.opened))
                self.close()
                continue
            if now - self.last_ping >= PING_S:
                try:
                    self.ws.ping()
                    self.pings += 1
                except Exception as exc:
                    common.log("announce: ping failed (%s)" % exc.__class__.__name__)
                    self.close()
                    continue
                self.last_ping = now
            try:
                opcode, frame = self.ws.recv_data_frame(True)
            except websocket.WebSocketTimeoutException:
                continue
            except Exception as exc:
                common.log("announce: connection lost (%s)" % exc.__class__.__name__)
                self.close()
                continue
            if opcode == websocket.ABNF.OPCODE_CLOSE:
                code = int.from_bytes(frame.data[:2], "big") if len(frame.data) >= 2 else None
                self.close_codes.append(code)
                common.log("announce: close frame code=%s" % code)
                self.close()
            elif opcode == websocket.ABNF.OPCODE_TEXT:
                data = frame.data
                yield data.decode("utf-8", "replace") if isinstance(data, bytes) else data


def parse_data(raw):
    """The inner record of a DATA message, or None."""
    try:
        doc = json.loads(raw)
    except ValueError:
        return None
    if not isinstance(doc, dict) or doc.get("type") != "DATA":
        return None
    inner = doc.get("data")
    try:
        inner = json.loads(inner) if isinstance(inner, str) else inner
    except ValueError:
        return None
    return inner if isinstance(inner, dict) else None


def record(state_dir, received_ms, data):
    path = os.path.join(state_dir, RECORD)
    try:
        with open(path, encoding="utf-8") as fh:
            existing = fh.read()
    except FileNotFoundError:
        existing = ""
    if existing and not existing.endswith("\n"):
        existing += "\n"
    entry = {"received_ms": received_ms}
    for name in ("catalogId", "catalogName", "publishDate", "title", "body"):
        entry[name] = data.get(name)
    common.atomic_write(path, existing + json.dumps(entry, ensure_ascii=False) + "\n")


def utc_text(ms):
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def act(data, cls, ticker):
    """A list match → A1, plus a run request in a listing catalogue; a perpetual
    match in such a catalogue → A1 and a run request; anything else is recorded only."""
    catalog = str(data.get("catalogName") or "")
    listing = "listing" in catalog.lower()
    if cls == "none" or (cls == "perpetual" and not listing):
        return "recorded"
    hhmm = datetime.fromtimestamp(int(data.get("publishDate") or time.time() * 1000) / 1000,
                                  tz=TBILISI).strftime("%H:%M")
    text = common.A1.format(hhmm=hhmm, catalog_name=catalog, title=str(data.get("title") or ""))
    if listing:
        outcome = common.request_run("watcher")
        if outcome == "requested":
            text += "\n" + common.R1
        elif outcome == "capped":
            text += "\n" + common.R2
    common.write_outbox("alert", text)
    return "alerted"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Binance's announcement stream")
    parser.add_argument("--measure", nargs=2, type=int, metavar=("SECONDS", "MAX_DATA"))
    parser.add_argument("--state-dir", default=common.STATE_DIR)
    args = parser.parse_args(argv)
    key = common.load_credential("binance-api-key")
    secret = common.load_credential("binance-api-secret")

    result, fields = key_check(key, secret)
    common.log("announce: key %s %s" % (result, fields))
    if result == "REFUSED":
        return EXIT_REFUSED
    if result != "ACCEPTED":
        return EXIT_CONNECT

    stream = Stream(key, secret)
    if not stream.connect():
        return EXIT_CONNECT
    list_tickers = list_pairs()
    started = time.monotonic()
    seen = complete = 0
    if args.measure:
        seconds, max_data = args.measure
        stop = lambda: time.monotonic() - started >= seconds or seen >= max_data  # noqa: E731
    else:
        stop = lambda: False  # noqa: E731
    try:
        for raw in stream.frames(stop):
            data = parse_data(raw)
            if data is None:
                continue
            received_ms = int(time.time() * 1000)
            seen += 1
            has_all = all(data.get(name) is not None for name in FIELDS)
            complete += 1 if has_all else 0
            record(args.state_dir, received_ms, data)
            cls, ticker = match_title(str(data.get("title") or ""), list_tickers, perpetual_pairs(args.state_dir))
            publish = data.get("publishDate")
            lag = received_ms - publish if isinstance(publish, int) else None
            if args.measure:
                common.log("announce: data catalogName=%s title=%s publish_utc=%s lag_ms=%s match=%s fields=%d/6"
                           % (data.get("catalogName"), data.get("title"),
                              utc_text(publish) if isinstance(publish, int) else "-", lag,
                              cls + ("" if ticker is None else " " + ticker),
                              sum(data.get(name) is not None for name in FIELDS)))
            else:
                outcome = act(data, cls, ticker)
                common.log("announce: data catalogId=%s match=%s %s lag_ms=%s"
                           % (data.get("catalogId"), cls, outcome, lag))
    finally:
        stream.close()
    common.log("announce: data_messages=%d complete=%d pings=%d reconnects=%d close_codes=%s"
               % (seen, complete, stream.pings, stream.reconnects,
                  ",".join(str(c) for c in stream.close_codes) or "-"))
    return EXIT_COMPLETE if complete else EXIT_NONE


if __name__ == "__main__":
    sys.exit(main())
