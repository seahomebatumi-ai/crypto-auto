#!/usr/bin/env python3
"""Paths and the shared helpers of the VPS assistant (TZ-54 B1, TZ-55 B1), and nothing else.

Python 3.12's standard library only. Every Russian string is written as \\uXXXX
escapes (TZ-54 rule 6, hard floor item 7's rule) and equals TZ-54 §12.1 or
TZ-55 §12.1 character for character. Time is UTC everywhere (rule 8).
"""
import fcntl
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
RUNS_ENABLED = STATE_DIR + "/runs-enabled"
RUN_ACTIVE = "/run/crypto-run"            # crypto-run.service's RuntimeDirectory
CREDENTIALS_ROOT = "/etc/crypto-auto/credentials"
OWNER_BINDING = CREDENTIALS_ROOT + "/owner-chat-id"
DEPLOY_CLONE = "/srv/crypto-auto"
# The run's own user and its own clone (TZ-55 B1): crypto-run.service runs as cryptorun.
RUN_HOME = "/var/lib/cryptorun"
RUN_TREE = RUN_HOME + "/crypto-auto"
GIT_LOCK = "/run/lock/crypto-auto-git.lock"

HTTP_TIMEOUT_S = 20                       # rule 3: every program read times out at 20 s
MiB = 1048576
# TZ-55 §12.4. [Architect's decision: headroom left to the host's page cache and the small
# services, whose ceilings are 128M each and whose measured peaks were 13-22 MB.]
RESERVE_BYTES = 64 * MiB
# TZ-55 §12.4, derived: the measuring session's own Claude process held 161 374 208 bytes
# resident at TZ-54 A2, and a ceiling below one Claude process cannot hold the run's.
MEMORY_MAX_FLOOR_BYTES = 160 * MiB
OUTBOX_KINDS = ("answer", "alert", "notice")
# [Architect's decision: a budget on the owner's subscription, not a statistic]
WATCHER_DAILY_CAP = 6

# --- TZ-54 §12.1, character for character --------------------------------
S1 = "\u25b6 \u0410\u043d\u0430\u043b\u0438\u0437 \u0440\u044b\u043d\u043a\u0430"
S2 = ("\u0413\u043e\u0442\u043e\u0432. \u041a\u043d\u043e\u043f\u043a\u0430 \u0432\u043d\u0438\u0437\u0443 "
      "\u0437\u0430\u043f\u0443\u0441\u043a\u0430\u0435\u0442 \u0430\u043d\u0430\u043b\u0438\u0437 "
      "\u0440\u044b\u043d\u043a\u0430.")
S3 = ("\u0410\u043d\u0430\u043b\u0438\u0437 \u0437\u0430\u043f\u0443\u0449\u0435\u043d \u2014 "
      "\u043e\u0442\u0432\u0435\u0442 \u043f\u0440\u0438\u0434\u0451\u0442 \u0441\u044e\u0434\u0430.")
S4 = ("\u0410\u043d\u0430\u043b\u0438\u0437 \u0443\u0436\u0435 \u0438\u0434\u0451\u0442 \u2014 "
      "\u043e\u0442\u0432\u0435\u0442 \u043f\u0440\u0438\u0434\u0451\u0442 \u0441\u044e\u0434\u0430.")
S5 = ("\u0417\u0430\u043f\u0443\u0441\u043a \u0441 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 "
      "\u043f\u043e\u043a\u0430 \u0432\u044b\u043a\u043b\u044e\u0447\u0435\u043d.")
S6 = ("\u0410\u043d\u0430\u043b\u0438\u0437 \u043d\u0435 \u0437\u0430\u043f\u0443\u0449\u0435\u043d: "
      "\u043f\u0430\u043c\u044f\u0442\u044c \u0441\u0435\u0440\u0432\u0435\u0440\u0430 "
      "\u0437\u0430\u043d\u044f\u0442\u0430 \u0434\u0440\u0443\u0433\u043e\u0439 "
      "\u0441\u0435\u0441\u0441\u0438\u0435\u0439.")
S7 = "\u0410\u043d\u0430\u043b\u0438\u0437 \u043d\u0435 \u0437\u0430\u0432\u0435\u0440\u0448\u0451\u043d."
S8 = "\u041a\u043e\u043c\u0430\u043d\u0434\u0430 \u043e\u0434\u043d\u0430: " + S1
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
# Alert templates: TZ-54 §12.1's placeholders (the Tbilisi time, the date, SYMBOL, OLD,
# NEW, catalogName and title) are the format fields below.
A1 = ("\u26a1 Binance \u00b7 {hhmm} \u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 "
      "{catalog_name}: {title}")
A2 = "\u26a1 Binance Futures \u00b7 {symbol}: \u043d\u043e\u0432\u044b\u0439 \u043a\u043e\u043d\u0442\u0440\u0430\u043a\u0442"
A3 = ("\u26a1 Binance Futures \u00b7 {symbol}: \u0434\u0430\u0442\u0430 "
      "\u0434\u0435\u043b\u0438\u0441\u0442\u0438\u043d\u0433\u0430 {ddmmyyyy}")
A4 = "\u26a1 Binance Futures \u00b7 {symbol}: \u0441\u0442\u0430\u0442\u0443\u0441 {old} \u2192 {new}"
R1 = "\u2192 \u0430\u043d\u0430\u043b\u0438\u0437 \u0437\u0430\u043f\u0443\u0449\u0435\u043d"
R2 = ("\u2192 \u043b\u0438\u043c\u0438\u0442 \u0437\u0430\u043f\u0443\u0441\u043a\u043e\u0432 "
      "\u043d\u0430 \u0441\u0435\u0433\u043e\u0434\u043d\u044f \u0438\u0441\u0447\u0435\u0440\u043f\u0430\u043d")


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


# --- runs ---------------------------------------------------------------------
def runs_enabled():
    return os.path.exists(RUNS_ENABLED)


def run_active():
    return os.path.exists(RUN_ACTIVE)


def utc_now():
    return datetime.now(timezone.utc)


def request_run(source):
    """One .req file into the requests directory when runs are enabled. The
    watcher's requests are counted per UTC day under a lock and refused past
    WATCHER_DAILY_CAP; the bot's are uncapped. Returns requested, capped or
    disabled."""
    if not runs_enabled():
        return "disabled"
    if source != "watcher":
        _write_request(source)
        return "requested"
    count_path = os.path.join(STATE_DIR, "run-requests-" + utc_now().strftime("%Y-%m-%d"))
    with open(os.path.join(STATE_DIR, "run-requests.lock"), "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            with open(count_path, encoding="utf-8") as fh:
                count = int(fh.read().strip() or "0")
        except FileNotFoundError:
            count = 0
        if count >= WATCHER_DAILY_CAP:
            return "capped"
        atomic_write(count_path, "%d\n" % (count + 1))
        _write_request(source)
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
