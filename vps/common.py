#!/usr/bin/env python3
"""Paths and the shared helpers of the VPS assistant (TZ-54 B1, TZ-55 B1, TZ-56 B1, TZ-57 B1, TZ-60 B1), and nothing else.

Python 3.12's standard library only. Every Russian string is written as \\uXXXX
escapes (TZ-54 rule 6, hard floor item 7's rule) and equals TZ-54 §12.1,
TZ-55 §12.1 or TZ-60 §12.1 character for character. Time is UTC everywhere (rule 8).
"""
import json
import math
import os
import re
import tempfile
import time
import urllib.parse
from datetime import datetime, timezone
from fractions import Fraction

VPS_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = "/var/lib/crypto-auto"
SPOOL_DIR = "/var/spool/crypto-auto"
OUTBOX_DIR = SPOOL_DIR + "/outbox"
REQUESTS_DIR = SPOOL_DIR + "/requests"
STOP_DIR = SPOOL_DIR + "/stop"            # TZ-60 §12.5: the owner's stop requests
RUNS_ENABLED = STATE_DIR + "/runs-enabled"
RUN_ACTIVE = "/run/crypto-run"            # crypto-run.service's RuntimeDirectory
STOP_ACTIVE = "/run/crypto-stop"          # crypto-stop.service's RuntimeDirectory
RUN_UNIT = "crypto-run.service"
CREDENTIALS_ROOT = "/etc/crypto-auto/credentials"
OWNER_BINDING = CREDENTIALS_ROOT + "/owner-chat-id"
DEPLOY_CLONE = "/srv/crypto-auto"
# The run's own user and its own clone (TZ-55 B1): crypto-run.service runs as cryptorun.
RUN_HOME = "/var/lib/cryptorun"
RUN_TREE = RUN_HOME + "/crypto-auto"
GIT_LOCK = "/run/lock/crypto-auto-git.lock"
# TZ-55's measurement record (map inv. 46), beside this file.
RECORD_PATH = os.path.join(VPS_DIR, "memory-record.txt")

HTTP_TIMEOUT_S = 20                       # rule 3: every program read times out at 20 s
MiB = 1048576
# TZ-55 §12.4. [Architect's decision: headroom left to the host's page cache and the small
# services, whose ceilings are 128M each and whose measured peaks were 13-22 MB.]
RESERVE_BYTES = 64 * MiB
# TZ-55 §12.4, derived: the measuring session's own Claude process held 161 374 208 bytes
# resident at TZ-54 A2, and a ceiling below one Claude process cannot hold the run's.
MEMORY_MAX_FLOOR_BYTES = 160 * MiB
OUTBOX_KINDS = ("answer", "alert", "notice")

# --- TZ-54 §12.1, character for character --------------------------------
S1 = "\u25b6 \u0410\u043d\u0430\u043b\u0438\u0437 \u0440\u044b\u043d\u043a\u0430"
S2 = ("\u0413\u043e\u0442\u043e\u0432. \u041a\u043d\u043e\u043f\u043a\u0430 \u0432\u043d\u0438\u0437\u0443 "
      "\u0437\u0430\u043f\u0443\u0441\u043a\u0430\u0435\u0442 \u0430\u043d\u0430\u043b\u0438\u0437 "
      "\u0440\u044b\u043d\u043a\u0430.")
# S3 and S4 as TZ-60 §12.1 changes them: the messages that confirm a start name the word.
S3 = ("\u0410\u043d\u0430\u043b\u0438\u0437 \u0437\u0430\u043f\u0443\u0449\u0435\u043d \u2014 "
      "\u043e\u0442\u0432\u0435\u0442 \u043f\u0440\u0438\u0434\u0451\u0442 \u0441\u044e\u0434\u0430. "
      "\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c: \u0421\u0422\u041e\u041f.")
S4 = ("\u0410\u043d\u0430\u043b\u0438\u0437 \u0443\u0436\u0435 \u0438\u0434\u0451\u0442 \u2014 "
      "\u043e\u0442\u0432\u0435\u0442 \u043f\u0440\u0438\u0434\u0451\u0442 \u0441\u044e\u0434\u0430. "
      "\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c: \u0421\u0422\u041e\u041f.")
S5 = ("\u0417\u0430\u043f\u0443\u0441\u043a \u0441 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 "
      "\u043f\u043e\u043a\u0430 \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d.")
S6 = ("\u0410\u043d\u0430\u043b\u0438\u0437 \u043d\u0435 \u0437\u0430\u043f\u0443\u0449\u0435\u043d: "
      "\u043f\u0430\u043c\u044f\u0442\u044c \u0441\u0435\u0440\u0432\u0435\u0440\u0430 "
      "\u0437\u0430\u043d\u044f\u0442\u0430 \u0434\u0440\u0443\u0433\u043e\u0439 "
      "\u0441\u0435\u0441\u0441\u0438\u0435\u0439.")
S7 = "\u0410\u043d\u0430\u043b\u0438\u0437 \u043d\u0435 \u0437\u0430\u0432\u0435\u0440\u0448\u0451\u043d."
S8 = "\u041a\u043e\u043c\u0430\u043d\u0434\u044b: " + S1 + " \u00b7 \u0421\u0422\u041e\u041f"   # TZ-60 §12.1
S9 = ("\u0421\u0432\u044f\u0437\u044c \u0441 \u0441\u0435\u0440\u0432\u0435\u0440\u043e\u043c "
      "\u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u0430.")
S10 = ("\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 "
       "\u043d\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e: "
       "\u0441\u0430\u043c\u043e\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 "
       "\u043d\u0435 \u043f\u0440\u043e\u0448\u043b\u0430.")
# TZ-55 §12.1, character for character: a vps tree refused for its signature.
S11 = ("\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 "
       "\u043d\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e: "
       "\u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u043d\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u0430\u043d\u043e GitHub.")
# TZ-60 §12.1, character for character: the owner's stop.
S12 = "\u041e\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u044e \u0430\u043d\u0430\u043b\u0438\u0437\u2026"
S13 = "\u0410\u043d\u0430\u043b\u0438\u0437 \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d."
S14 = ("\u0410\u043d\u0430\u043b\u0438\u0437 \u043d\u0435 \u0438\u0434\u0451\u0442 \u2014 "
       "\u043e\u0441\u0442\u0430\u043d\u0430\u0432\u043b\u0438\u0432\u0430\u0442\u044c \u043d\u0435\u0447\u0435\u0433\u043e.")
S15 = ("\u041e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0430\u043d\u0430\u043b\u0438\u0437 "
       "\u043d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c.")
# Alert templates: TZ-54 §12.1's placeholders (the Tbilisi time, the date, SYMBOL, OLD,
# NEW, catalogName and title) are the format fields below.
A1 = ("\u26a1 Binance \u00b7 {hhmm} \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 "
      "{catalog_name}: {title}")
A2 = "\u26a1 Binance Futures \u00b7 {symbol}: \u043d\u043e\u0432\u044b\u0439 \u043a\u043e\u043d\u0442\u0440\u0430\u043a\u0442"
A3 = ("\u26a1 Binance Futures \u00b7 {symbol}: \u0434\u0430\u0442\u0430 "
      "\u0434\u0435\u043b\u0438\u0441\u0442\u0438\u043d\u0433\u0430 {ddmmyyyy}")
A4 = "\u26a1 Binance Futures \u00b7 {symbol}: \u0441\u0442\u0430\u0442\u0443\u0441 {old} \u2192 {new}"


# --- rule 5: atomic writes (inv. 72) ----------------------------------------
def atomic_write(path, data, mode=0o640):
    """Serialise the whole object BEFORE touching the filesystem, write a
    temporary file beside the target, rename it over; on any failure remove
    both and re-raise (inv. 72). bytes and str are written as they are; any
    other object is serialised as JSON. An existing target keeps its mode and,
    when root writes, its owner."""
    path = os.path.abspath(path)
    tmp = None
    try:
        if isinstance(data, bytes):
            blob = data
        elif isinstance(data, str):
            blob = data.encode("utf-8")
        else:
            blob = (json.dumps(data, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
        try:
            keep = os.stat(path)
        except FileNotFoundError:
            keep = None
        fd, tmp = tempfile.mkstemp(prefix="." + os.path.basename(path) + ".", suffix=".tmp",
                                   dir=os.path.dirname(path))
        with os.fdopen(fd, "wb") as fh:
            fh.write(blob)
            fh.flush()
            os.fsync(fh.fileno())
        if keep is not None:
            os.chmod(tmp, keep.st_mode & 0o7777)
            if os.geteuid() == 0:
                os.chown(tmp, keep.st_uid, keep.st_gid)
        else:
            os.chmod(tmp, mode)
        os.replace(tmp, path)
        tmp = None
    except BaseException:
        for leftover in (tmp, path):
            if leftover:
                try:
                    os.unlink(leftover)
                except FileNotFoundError:
                    pass
        raise


def write_outbox(kind, text, outbox_dir=None):
    """One JSON file {"kind","text","created_ms"} named <created_ms>-<kind>-<pid>.json."""
    outbox_dir = outbox_dir or OUTBOX_DIR
    if kind not in OUTBOX_KINDS:
        raise ValueError("outbox kind %r" % (kind,))
    created_ms = int(time.time() * 1000)
    while os.path.exists(os.path.join(outbox_dir, "%d-%s-%d.json" % (created_ms, kind, os.getpid()))):
        created_ms += 1
    name = "%d-%s-%d.json" % (created_ms, kind, os.getpid())
    atomic_write(os.path.join(outbox_dir, name),
                 {"kind": kind, "text": text, "created_ms": created_ms})
    return name


# --- rules 1 and 2: credentials and redaction --------------------------------
class CredentialMissing(Exception):
    pass


_LOADED = []


def load_credential(name):
    """The file under $CREDENTIALS_DIRECTORY, surrounding whitespace stripped.
    The value is remembered so that redact() can remove it from any text."""
    base = os.environ.get("CREDENTIALS_DIRECTORY")
    if not base:
        raise CredentialMissing(name)
    try:
        with open(os.path.join(base, name), encoding="utf-8") as fh:
            value = fh.read().strip()
    except OSError:
        raise CredentialMissing(name) from None
    if not value:
        raise CredentialMissing(name)
    remember_secret(value)
    return value


def remember_secret(value):
    for form in (value, urllib.parse.quote(value, safe=""), urllib.parse.quote_plus(value)):
        if form and form not in _LOADED:
            _LOADED.append(form)


def redact(text):
    """Every loaded credential value, plain or URL-encoded, becomes <redacted>."""
    out = text if isinstance(text, str) else str(text)
    for value in sorted(_LOADED, key=len, reverse=True):
        out = out.replace(value, "<redacted>")
    return out


# --- the universe: tokens[] cut from index.html (inv. 21) ---------------------
class TokensUnreadable(Exception):
    pass


_TOKENS_BLOCK = re.compile(r"var\s+tokens\s*=\s*\[(.*?)\]\s*;", re.S)
_TOKEN_ROW = re.compile(r"\{\s*name\s*:\s*'([^']+)'\s*,\s*s\s*:\s*'([^']+)'\s*(,\s*fut\s*:\s*true\s*)?\}")


def cut_tokens(index_html):
    """Every {name:'…', s:'…'[, fut:true]} inside `var tokens = [ … ];`.
    Zero rows, or an object the row pattern does not read, fails (inv. 22)."""
    block = _TOKENS_BLOCK.search(index_html)
    if block is None:
        raise TokensUnreadable("tokens[] block not found")
    body = re.sub(r"//[^\n]*", "", block.group(1))
    rows = [{"name": name, "s": sym, "fut": bool(fut)} for name, sym, fut in _TOKEN_ROW.findall(body)]
    if not rows:
        raise TokensUnreadable("tokens[] parsed to zero rows")
    if body.count("{") != len(rows):
        raise TokensUnreadable("tokens[] holds %d objects, %d read" % (body.count("{"), len(rows)))
    return rows


def index_html_path():
    """The checkout this vps/ directory sits in; a staging copy outside a
    checkout reads the deployer's clone."""
    here = os.path.join(os.path.dirname(VPS_DIR), "index.html")
    return here if os.path.exists(here) else os.path.join(DEPLOY_CLONE, "index.html")


def read_tokens(path=None):
    with open(path or index_html_path(), encoding="utf-8") as fh:
        return cut_tokens(fh.read())


# --- TZ-54 §12.8, the one implementation ------------------------------------
def derive_limits(footprint_bytes, duration_s):
    """(memory_max_bytes, runtime_max_s) from a footprint and a duration."""
    step = 16 * MiB
    footprint = Fraction(footprint_bytes)
    duration = Fraction(str(duration_s)) if isinstance(duration_s, (float, str)) else Fraction(duration_s)
    memory_max = math.ceil(Fraction(3, 2) * footprint / step) * step
    runtime_max = max(math.ceil(2 * duration / 300) * 300, 3600) + 1800   # 1 800 s: B3's admission wait
    return int(memory_max), int(runtime_max)


# --- TZ-55 §12.4, the test mode: the one implementation ------------------------
def test_limits(footprint_bytes, duration_s, host_free_bytes):
    """(budget, memory_max, memory_swap_max, runtime_max_s). The budget is
    derive_limits' ceiling, unchanged; the resident part is the smaller of the
    budget and what the host frees less RESERVE_BYTES, rounded down to 16 MiB;
    the rest of the budget is the run's own swap."""
    step = 16 * MiB
    budget, runtime_max = derive_limits(footprint_bytes, duration_s)
    memory_max = min(budget, ((int(host_free_bytes) - RESERVE_BYTES) // step) * step)
    return budget, memory_max, budget - memory_max, runtime_max


# --- TZ-56 §12.2, the start limits: the one implementation ----------------------
def start_limits(available_bytes, budget_bytes):
    """(memory_max, memory_swap_max) set at each start: what the host frees less
    RESERVE_BYTES, rounded down to 16 MiB, never below MEMORY_MAX_FLOOR_BYTES and
    never above the budget; the rest of the budget is the run's own swap."""
    step = 16 * MiB
    budget = int(budget_bytes)
    memory_max = min(budget, max(MEMORY_MAX_FLOOR_BYTES, ((int(available_bytes) - RESERVE_BYTES) // step) * step))
    return memory_max, budget - memory_max


# --- TZ-57 §12.4, the record's budget rule: the one implementation -----------------
def _record_int(value):
    """An integer field of the record, or None when absent or not an integer ("-")."""
    text = "" if value is None else str(value).strip()
    return int(text) if re.fullmatch(r"\d+", text) else None


def _record_number(value):
    """A numeric field of the record, or None when absent or not a number ("-")."""
    text = "" if value is None else str(value).strip()
    return text if re.fullmatch(r"\d+(\.\d+)?", text) else None


def record_limits(record):
    """(budget_bytes, runtime_max_s) of the record dict read_record() returns:
    the larger of derive_limits' budgets for TZ-54's input and TZ-55's run, then
    the product's own chosen run (TZ-57 §12.3) when it completed or was killed by
    memory, never one killed by time, whose figures are its limits rather than its
    need; runtime_max_s takes a completed run's duration the same way. An absent
    product key is an absent term."""
    budget_in, _ = derive_limits(record["input_footprint_bytes"], record["input_duration_s"])
    budget_run, runtime = derive_limits(record["run_footprint_bytes"], record["run_duration_s"])
    budget = max(budget_in, budget_run)
    product_class = record.get("product_class")
    footprint = _record_int(record.get("product_footprint_bytes"))
    if product_class in ("C", "K-oom") and footprint is not None:
        budget = max(budget, derive_limits(footprint, 0)[0])
    duration = _record_number(record.get("product_duration_s"))
    if product_class == "C" and duration is not None:
        runtime = max(runtime, derive_limits(0, duration)[1])
    return budget, runtime


def read_record(path=RECORD_PATH):
    """The record's name=value lines as a dict, blank lines and comments skipped:
    the one parser of vps/memory-record.txt."""
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line and not line.startswith("#"):
                key, _, value = line.partition("=")
                out[key] = value
    return out


# --- runs ---------------------------------------------------------------------
def runs_enabled():
    return os.path.exists(RUNS_ENABLED)


def run_active():
    return os.path.exists(RUN_ACTIVE)


def pending_requests():
    """True when the requests directory holds a .req file whose name does not
    start with "."; a missing directory is false (TZ-60 §12.5)."""
    try:
        names = os.listdir(REQUESTS_DIR)
    except FileNotFoundError:
        return False
    return any(name.endswith(".req") and not name.startswith(".") for name in names)


def utc_now():
    return datetime.now(timezone.utc)


def request_run(source):
    """One .req file into the requests directory when runs are enabled: returns
    requested, or disabled when they are not. Only the owner's button requests a
    run (TZ-57, the owner's decision of 03.10.2026): the bot is the one caller,
    the watchers alert and request nothing, and no timer starts a run."""
    if not runs_enabled():
        return "disabled"
    _write_request(source)
    return "requested"


def request_stop(source):
    """One .stop file into the stop directory, named the way a request is named;
    returns requested. A stop is always allowed: runs_enabled() is never
    consulted (TZ-60 §12.5)."""
    created_ms = int(time.time() * 1000)
    while os.path.exists(os.path.join(STOP_DIR, "%d-%s-%d.stop" % (created_ms, source, os.getpid()))):
        created_ms += 1
    name = "%d-%s-%d.stop" % (created_ms, source, os.getpid())
    atomic_write(os.path.join(STOP_DIR, name), {"source": source, "created_ms": created_ms}, mode=0o660)
    return "requested"


def _write_request(source):
    created_ms = int(time.time() * 1000)
    while os.path.exists(os.path.join(REQUESTS_DIR, "%d-%s-%d.req" % (created_ms, source, os.getpid()))):
        created_ms += 1
    name = "%d-%s-%d.req" % (created_ms, source, os.getpid())
    atomic_write(os.path.join(REQUESTS_DIR, name), {"source": source, "created_ms": created_ms}, mode=0o660)


def log(*parts):
    """One redacted line on stdout, flushed (the unit's journal)."""
    print(redact(" ".join(str(p) for p in parts)), flush=True)
