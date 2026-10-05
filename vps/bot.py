#!/usr/bin/env python3
"""The Telegram bot (TZ-54 B4, TZ-55 B3, TZ-60 B2): answers the owner's chat and
nothing else, starts a run from one button, asks for the owner's typed stop and
delivers the outbox. An outbox file one of whose chunks is refused in both forms
is set aside as <name>.dead, so it never holds the files behind it.

    bot.py                       the service: long poll, owner filter, outbox delivery
    bot.py --bind                bind the one private chat that sent /start (exit 3: zero or several)
    bot.py --send-outbox-once    send every outbox file once (exit 0 only when every chunk was accepted)

Reads its token and the owner binding only from $CREDENTIALS_DIRECTORY and
prints neither, nor the chat id.
"""
import argparse
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

API = "https://api.telegram.org/bot%s/%s"
TEXT_LIMIT = 4096                     # sendMessage `text`, 1-4096 characters (report A9)
CHUNK_LIMIT = TEXT_LIMIT - 96         # TZ-54 §12.3
MAX_AGE_S = 600                       # TZ-54 §12.4
POLL_TIMEOUT_S = 10
CHUNK_SPACING_S = 1.0
BACKOFF_MAX_S = 60
OFFSET_FILE = os.path.join(common.STATE_DIR, "bot-offset")
COUNTERS_FILE = os.path.join(common.STATE_DIR, "bot-counters.json")
KEYBOARD = {"keyboard": [[{"text": common.S1}]], "resize_keyboard": True, "is_persistent": True}
NO_PREVIEW = {"is_disabled": True}
DEAD_SUFFIX = ".dead"                 # TZ-55 B3: outbox_files() never lists it; cleanup.py ages it out
STOP_WORDS = ("stop", "/stop", "\u0441\u0442\u043e\u043f")   # TZ-60 §12.6


# --- TZ-54 §12.3: conversion ---------------------------------------------------
_HEADER = re.compile(r"^#{1,6} (.+)$")
_BOLD = re.compile(r"\*\*(.+?)\*\*")


def _escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _is_table(line):
    return line.lstrip(" \t").startswith("|")


def convert_line(line):
    escaped = _escape(line)
    head = _HEADER.match(escaped)
    if head:
        return "<b>" + head.group(1).replace("**", "") + "</b>"
    return _BOLD.sub(r"<b>\1</b>", escaped)


def pre_block(lines):
    return "<pre>" + "\n".join(_escape(line) for line in lines) + "</pre>"


def visible_len(unit_html):
    """Length with tags removed and &lt; &gt; &amp; read as one character each."""
    text = re.sub(r"<[^>]*>", "", unit_html)
    return len(text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&"))


def convert(text):
    """The whole conversion, line by line: (html, source) per unit."""
    return [html_ for html_, _ in _units(text.split("\n"), None)]


def _units(lines, limit):
    """Units in order: a maximal run of table lines is one <pre> block, every
    other line is one unit. With a limit, a <pre> block longer than it is split
    at its own line breaks, and a longer plain line is cut in its source text
    before conversion. Each unit is (html, source)."""
    out = []
    i = 0
    while i < len(lines):
        if _is_table(lines[i]):
            j = i
            while j < len(lines) and _is_table(lines[j]):
                j += 1
            block = lines[i:j]
            if limit is None or visible_len(pre_block(block)) <= limit:
                out.append((pre_block(block), "\n".join(block)))
            else:
                group = []
                for line in block:
                    for piece in _cut(line, limit):
                        if group and visible_len(pre_block(group + [piece])) > limit:
                            out.append((pre_block(group), "\n".join(group)))
                            group = []
                        group.append(piece)
                if group:
                    out.append((pre_block(group), "\n".join(group)))
            i = j
            continue
        line = lines[i]
        if limit is not None and visible_len(convert_line(line)) > limit:
            for piece in _cut(line, limit):
                out.append((convert_line(piece), piece))
        else:
            out.append((convert_line(line), line))
        i += 1
    return out


def _cut(source, limit):
    return [source[k:k + limit] for k in range(0, len(source), limit)] or [source]


def chunk(text, limit=CHUNK_LIMIT):
    """Units packed in order while a chunk's visible length — each unit's
    visible length plus one for the joining newline — stays within the limit.
    Empty or blank chunks are dropped. Each chunk is (html, plain fallback)."""
    chunks, units, size = [], [], 0
    for unit in _units(text.split("\n"), limit):
        cost = visible_len(unit[0]) + 1
        if units and size + cost - 1 > limit:
            chunks.append(units)
            units, size = [], 0
        units.append(unit)
        size += cost
    if units:
        chunks.append(units)
    result = []
    for group in chunks:
        body = "\n".join(u[0] for u in group)
        plain = "\n".join(u[1] for u in group)
        if plain.strip() == "" and re.sub(r"<[^>]*>", "", body).strip() == "":
            continue
        result.append((body, plain))
    return result


# --- TZ-54 §12.4: the owner filter ---------------------------------------------
def is_stop(text):
    """The owner's stop: the text with surrounding whitespace and a trailing «!» or «.» removed,
    case-folded, is one of STOP_WORDS."""
    return isinstance(text, str) and text.strip().rstrip("!.").strip().casefold() in STOP_WORDS


def classify(update, owner_id, now):
    """S2, request, stop, S8 or dropped."""
    msg = update.get("message") if isinstance(update, dict) else None
    if not isinstance(msg, dict):
        return "dropped"
    chat = msg.get("chat") if isinstance(msg.get("chat"), dict) else {}
    if chat.get("type") != "private" or chat.get("id") != owner_id:
        return "dropped"
    date = msg.get("date")
    if not isinstance(date, int) or now - date > MAX_AGE_S:
        return "dropped"
    text = msg.get("text")
    if text == "/start":
        return "S2"
    if text in ("/run", common.S1):
        return "request"
    if is_stop(text):
        return "stop"
    return "S8"


# --- the Bot API ---------------------------------------------------------------
class Api:
    def __init__(self, token):
        self.token = token
        self.last_send = 0.0

    def call(self, method, params, timeout=common.HTTP_TIMEOUT_S):
        """POST form-encoded (urllib adds the form content type; no header of
        ours). Returns (status, doc); status 0 is a network error."""
        form = {}
        for key, value in params.items():
            form[key] = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list, bool)) else value
        req = urllib.request.Request(API % (self.token, method), data=urllib.parse.urlencode(form).encode("utf-8"))
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            try:
                return exc.code, json.loads(exc.read())
            except ValueError:
                return exc.code, {}
        except (OSError, ValueError, http.client.HTTPException) as exc:
            return 0, {"description": common.redact(exc.__class__.__name__)}

    def send(self, chat_id, text, parse_mode=None, keyboard=False):
        wait = CHUNK_SPACING_S - (time.monotonic() - self.last_send)
        if wait > 0:
            time.sleep(wait)
        params = {"chat_id": chat_id, "text": text, "link_preview_options": NO_PREVIEW}
        if parse_mode:
            params["parse_mode"] = parse_mode
        if keyboard:
            params["reply_markup"] = KEYBOARD
        status, doc = self.call("sendMessage", params)
        self.last_send = time.monotonic()
        return status, doc


def send_chunk(api, chat_id, html_text, plain):
    """One chunk: HTML, then once more as plain text on 400; 429 waits
    retry_after. Returns (accepted, plain_used, message_id, status)."""
    plain_used = False
    while True:
        if plain_used:
            status, doc = api.send(chat_id, plain)
        else:
            status, doc = api.send(chat_id, html_text, parse_mode="HTML")
        if status == 200 and doc.get("ok"):
            return True, plain_used, doc.get("result", {}).get("message_id"), status
        if status == 429:
            time.sleep(int((doc.get("parameters") or {}).get("retry_after", 5)) + 1)
            continue
        if status == 400 and not plain_used:
            plain_used = True
            continue
        return False, plain_used, None, status


def send_file(api, chat_id, path):
    """Every chunk of one outbox file. The file is deleted only once every chunk
    was accepted, and rewritten atomically with the unsent chunks after a
    partial send. A chunk refused in both forms — HTML, then plain text, both
    HTTP 400 — renames the file <name>.dead beside itself, logged once by name
    (TZ-55 B3). Returns a stats dict."""
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    chunks = chunk(doc.get("text", ""))
    stats = {"kind": doc.get("kind", "-"), "chunks": len(chunks), "accepted": 0, "plain": 0,
             "ids": [], "complete": False, "dead": False, "status": 200}
    for index, (html_text, plain) in enumerate(chunks):
        accepted, plain_used, message_id, status = send_chunk(api, chat_id, html_text, plain)
        if not accepted:
            stats["status"] = status
            if status == 400 and plain_used:
                os.replace(path, path + DEAD_SUFFIX)
                stats["dead"] = True
                name = os.path.basename(path)
                common.log("bot: outbox file %s refused in both forms, renamed %s%s" % (name, name, DEAD_SUFFIX))
                return stats
            if index > 0:
                rest = "\n".join(p for _, p in chunks[index:])
                common.atomic_write(path, {"kind": doc.get("kind"), "text": rest,
                                           "created_ms": doc.get("created_ms")})
            return stats
        stats["accepted"] += 1
        stats["plain"] += 1 if plain_used else 0
        stats["ids"].append(message_id)
    os.unlink(path)
    stats["complete"] = True
    return stats


def deliver_outbox(api, owner):
    """One pass over the outbox, oldest first. A file set aside as .dead lets the
    pass go on to the next file; any other failure — a network error, a refusal
    that is not a double 400 — ends the pass and returns False, so the caller
    backs off with the file kept (TZ-54's behaviour). True when the pass ran through."""
    for path in outbox_files():
        try:
            stats = send_file(api, owner, path)
        except (OSError, ValueError) as exc:
            common.log("bot: outbox file %s unreadable (%s)" % (os.path.basename(path), exc.__class__.__name__))
            continue
        common.log("bot: sent %s kind=%s chunks=%d accepted=%d plain_fallbacks=%d"
                   % (os.path.basename(path), stats["kind"], stats["chunks"], stats["accepted"], stats["plain"]))
        if stats["dead"]:
            continue
        if not stats["complete"]:
            return False
    return True


def outbox_files():
    try:
        names = sorted(n for n in os.listdir(common.OUTBOX_DIR) if n.endswith(".json") and not n.startswith("."))
    except FileNotFoundError:
        return []
    return [os.path.join(common.OUTBOX_DIR, n) for n in names]


def owner_id_from_credentials():
    return int(common.load_credential("owner-chat-id"))


# --- modes ---------------------------------------------------------------------
def bind():
    api = Api(common.load_credential("telegram-bot-token"))
    out = {"getme": "failed", "username": "-", "updates": 0, "start_chats": 0, "bound": "no", "confirm_sent": "no"}

    def report(code):
        print("bind: getme=%(getme)s username=%(username)s updates=%(updates)s start_chats=%(start_chats)s "
              "bound=%(bound)s confirm_sent=%(confirm_sent)s" % out, flush=True)
        return code

    status, me = api.call("getMe", {})
    if status == 200 and me.get("ok"):
        out["getme"] = "ok"
        out["username"] = me.get("result", {}).get("username", "-")
    else:
        return report(4)
    status, doc = api.call("getUpdates", {"timeout": 0})
    if not (status == 200 and doc.get("ok")):
        return report(4)
    updates = [u for u in doc.get("result", []) if isinstance(u, dict)]
    out["updates"] = len(updates)
    chats = set()
    for update in updates:
        msg = update.get("message") or {}
        chat = msg.get("chat") or {}
        if chat.get("type") == "private" and msg.get("text") == "/start":
            chats.add(chat.get("id"))
    out["start_chats"] = len(chats)
    if len(chats) != 1:
        return report(3)
    chat_id = chats.pop()
    common.remember_secret(str(chat_id))
    common.atomic_write(common.OWNER_BINDING, str(chat_id), mode=0o600)
    out["bound"] = "yes"
    api.call("getUpdates", {"offset": max(u["update_id"] for u in updates) + 1, "timeout": 0})
    status, sent = api.send(chat_id, common.S9, keyboard=True)
    if status == 200 and sent.get("ok"):
        out["confirm_sent"] = "yes"
        return report(0)
    return report(5)


def send_outbox_once():
    api = Api(common.load_credential("telegram-bot-token"))
    chat_id = owner_id_from_credentials()
    files = outbox_files()
    all_ok = bool(files)
    for path in files:
        stats = send_file(api, chat_id, path)
        all_ok = all_ok and stats["complete"]
        print("send: file=%s kind=%s chunks=%d accepted=%d plain_fallbacks=%d message_ids=%s status=%s"
              % (os.path.basename(path), stats["kind"], stats["chunks"], stats["accepted"], stats["plain"],
                 ",".join(str(i) for i in stats["ids"]) or "-", stats["status"]), flush=True)
    print("send: files=%d all_accepted=%s" % (len(files), "yes" if all_ok else "no"), flush=True)
    if not files:
        return 2
    return 0 if all_ok else 1


def respond(api, owner, verdict):
    """The answer to one acted update (TZ-60 §12.6)."""
    if verdict == "S2":
        api.send(owner, common.S2, keyboard=True)
    elif verdict == "S8":
        api.send(owner, common.S8, keyboard=True)
    elif verdict == "stop":
        if common.run_active() or common.pending_requests():
            common.request_stop("bot")
            api.send(owner, common.S12, keyboard=True)
        else:
            api.send(owner, common.S14, keyboard=True)
    elif not common.runs_enabled():
        api.send(owner, common.S5, keyboard=True)
    elif common.run_active():
        api.send(owner, common.S4, keyboard=True)
    elif common.request_run("bot") == "requested":
        api.send(owner, common.S3, keyboard=True)
    else:
        api.send(owner, common.S5, keyboard=True)


def read_offset():
    try:
        with open(OFFSET_FILE, encoding="utf-8") as fh:
            return int(fh.read().strip())
    except (OSError, ValueError):
        return 0


def service():
    api = Api(common.load_credential("telegram-bot-token"))
    owner = owner_id_from_credentials()
    offset = read_offset()
    counters = {"acted": 0, "dropped": 0}
    try:
        with open(COUNTERS_FILE, encoding="utf-8") as fh:
            counters.update(json.load(fh))
    except (OSError, ValueError):
        pass
    backoff = 0
    common.log("bot: service started")
    while True:
        status, doc = api.call("getUpdates", {"offset": offset, "timeout": POLL_TIMEOUT_S,
                                              "allowed_updates": ["message"]},
                               timeout=POLL_TIMEOUT_S + common.HTTP_TIMEOUT_S)
        if status == 200 and doc.get("ok"):
            backoff = 0
            updates = [u for u in doc.get("result", []) if isinstance(u, dict) and "update_id" in u]
            if updates:
                offset = max(u["update_id"] for u in updates) + 1
                common.atomic_write(OFFSET_FILE, "%d\n" % offset)
            now = int(time.time())
            for update in updates:
                verdict = classify(update, owner, now)
                if verdict == "dropped":
                    counters["dropped"] += 1
                    continue
                counters["acted"] += 1
                respond(api, owner, verdict)
            if updates:
                common.atomic_write(COUNTERS_FILE, counters)
                common.log("bot: updates=%d acted_total=%d dropped_total=%d"
                           % (len(updates), counters["acted"], counters["dropped"]))
        else:
            common.log("bot: getUpdates status=%s" % status)
            backoff = min(BACKOFF_MAX_S, max(5, backoff * 2))
            time.sleep(backoff)
        if not deliver_outbox(api, owner):
            backoff = min(BACKOFF_MAX_S, max(5, backoff * 2))
            time.sleep(backoff)


def main(argv=None):
    parser = argparse.ArgumentParser(description="the owner's Telegram bot")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--bind", action="store_true")
    group.add_argument("--send-outbox-once", action="store_true")
    args = parser.parse_args(argv)
    if args.bind:
        return bind()
    if args.send_outbox_once:
        return send_outbox_once()
    return service()


if __name__ == "__main__":
    sys.exit(main())
