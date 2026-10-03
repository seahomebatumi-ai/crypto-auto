#!/usr/bin/env python3
"""The run unit's program (TZ-54 B3, TZ-55 B2, TZ-56 B2, TZ-59 B1): the writer, then one
headless role-2 session, admitted only when the host's available memory less
RESERVE_BYTES covers this unit's ceiling and its free swap covers this unit's swap
ceiling; the answer goes to the outbox. The run has its own user and its own clone.

    run.py [--tree <dir>]          default /var/lib/cryptorun/crypto-auto
    run.py --limits                the unit's ExecStartPre=, as root: this start's
                                   MemoryMax= and MemorySwapMax= (TZ-56 12.2); exits 0

The run's own Claude login is read from $CREDENTIALS_DIRECTORY and placed in the
environment of the claude child alone. Never prints the answer. Exit 0 answer
handed to the outbox · 1 the session failed (notice S7) · 75 not admitted
(notice S6; SuccessExitStatus=75).
"""
import argparse
import json
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

ADMISSION_POLL_S = 30
ADMISSION_MAX_S = 1800
EXIT_NOT_ADMITTED = 75
WRITER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "writer.py")
LOGIN_CREDENTIAL = "claude-oauth-token"   # TZ-55 B2.3: the run's own Claude login
LOGIN_ENV = "CLAUDE_CODE_OAUTH_TOKEN"
# TZ-55 B2.4: categorical fields of result.json for the second summary line; never `result`.
RESULT_CATEGORIES = ("subtype", "api_error_status", "terminal_reason", "stop_reason")

# TZ-54 §12.2, exactly: the production trigger verbatim, one appended sentence
# naming the contract (contract §4), nothing else.
PROMPT = ("ANALYZE TODAY'S CRYPTO MARKET AND DETERMINE THE STRATEGY FOR ENTERING ALTCOINS "
          "ON BINANCE FUTURES.")
APPEND = ("Read EXECUTOR-INSTRUCTIONS.md at the repository root in full before anything else: "
          "it is your contract, and the user message is a trigger from its \u00a74.")
MODEL  = "claude-opus-5-5"
EFFORT = "high"
CLAUDE = ["claude", "-p", PROMPT,
          "--output-format", "json", "--model", MODEL, "--effort", EFFORT,
          "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch",
          "--append-system-prompt", APPEND]


def consume_requests():
    """Step 1, before anything that can fail, so a path unit cannot loop."""
    n = 0
    try:
        names = os.listdir(common.REQUESTS_DIR)
    except FileNotFoundError:
        return 0
    for name in names:
        if name.endswith(".req") and not name.startswith("."):
            try:
                os.unlink(os.path.join(common.REQUESTS_DIR, name))
                n += 1
            except FileNotFoundError:
                pass
    return n


def _own_cgroup():
    """This process's own cgroup path, relative to /sys/fs/cgroup."""
    with open("/proc/self/cgroup", encoding="utf-8") as fh:
        return fh.read().strip().splitlines()[-1].split("::", 1)[-1]


def _own_cgroup_limit(name):
    """One file of this unit's own cgroup: an int, the string `max`, or None when
    unreadable."""
    try:
        with open("/sys/fs/cgroup" + _own_cgroup() + "/" + name, encoding="utf-8") as fh:
            value = fh.read().strip()
        return value if value == "max" else int(value)
    except (OSError, ValueError, IndexError):
        return None


def own_memory_max():
    """This unit's memory.max from its cgroup: an int, `max`, or None when unreadable."""
    return _own_cgroup_limit("memory.max")


def own_swap_max():
    """This unit's memory.swap.max from its cgroup: an int, `max`, or None when unreadable."""
    return _own_cgroup_limit("memory.swap.max")


def _meminfo(key):
    with open("/proc/meminfo", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith(key + ":"):
                return int(line.split()[1]) * 1024
    raise RuntimeError("%s absent from /proc/meminfo" % key)


def mem_available():
    return _meminfo("MemAvailable")


def swap_free():
    return _meminfo("SwapFree")


def admissible(available, free_swap, ceiling, swap_ceiling):
    """TZ-56 B2.2 (12.2): MemAvailable less RESERVE_BYTES covers memory.max and,
    where memory.swap.max is a number above 0, SwapFree covers that number. A
    limit that is `max` or unreadable sets no condition."""
    if isinstance(ceiling, int) and available - common.RESERVE_BYTES < ceiling:
        return False
    if isinstance(swap_ceiling, int) and swap_ceiling > 0 and free_swap < swap_ceiling:
        return False
    return True


def admit(seen=None):
    """Step 2: wait until admissible(), polling every 30 s for at most 1 800 s.
    Returns (admitted, waited_s). `seen`, a dict, receives the limits admission
    read and the meminfo values of the poll that admitted, or of the last poll."""
    ceiling, swap_ceiling = own_memory_max(), own_swap_max()
    if seen is not None:
        seen.update(memory_max=ceiling, memory_swap_max=swap_ceiling)
    start = time.monotonic()
    while True:
        waited = int(time.monotonic() - start)
        available, free_swap = mem_available(), swap_free()
        if seen is not None:
            seen.update(mem_available=available, swap_free=free_swap)
        if admissible(available, free_swap, ceiling, swap_ceiling):
            return True, waited
        if waited + ADMISSION_POLL_S > ADMISSION_MAX_S:
            return False, waited
        time.sleep(ADMISSION_POLL_S)


def set_limits():
    """--limits, run as root by the unit's ExecStartPre= and doing nothing else:
    this start's MemoryMax= and MemorySwapMax= from the host at this instant
    (TZ-56 12.2), set on this unit for the runtime. One log line; always 0 — a
    failure leaves the pair already in force, and admission still holds the run
    to it. Reads no credential, consumes no request, touches no tree."""
    f = {"unit": "-", "mem_available": "-", "swap_free": "-", "budget": "-",
         "memory_max": "-", "memory_swap_max": "-", "set": "-"}
    try:
        f["unit"] = _own_cgroup().rstrip("/").rsplit("/", 1)[-1] or "-"
        f["mem_available"], f["swap_free"] = mem_available(), swap_free()
        f["budget"] = int(common.read_record()["budget_bytes"])
        f["memory_max"], f["memory_swap_max"] = common.start_limits(f["mem_available"], f["budget"])
        # A process outside a service (a session, a scope) sets nothing.
        if f["unit"].endswith(".service"):
            f["set"] = subprocess.run(["systemctl", "set-property", "--runtime", f["unit"],
                                       "MemoryMax=%d" % f["memory_max"],
                                       "MemorySwapMax=%d" % f["memory_swap_max"]]).returncode
    except Exception:
        pass
    common.log("crypto-run: limits unit=%(unit)s mem_available=%(mem_available)s swap_free=%(swap_free)s "
               "budget=%(budget)s memory_max=%(memory_max)s memory_swap_max=%(memory_swap_max)s set=%(set)s" % f)
    return 0


def git(tree, *args, capture=False):
    proc = subprocess.run(["git", "-C", tree] + list(args), capture_output=True, text=True)
    return proc.stdout if capture else proc.returncode


def prepare_tree(tree):
    """Step 3, in the run's own clone: no lock is shared with the deployer (TZ-55 B2.1)."""
    git(tree, "fetch", "-q", "origin", "main")
    for subject in git(tree, "log", "--format=%s", "origin/main..HEAD", capture=True).splitlines():
        common.log("crypto-run: commit absent from origin/main:", subject)
    git(tree, "reset", "-q", "--hard", "origin/main")
    git(tree, "clean", "-q", "-fdx")


def writer_env():
    """The writer's environment: this unit's, never carrying the Claude login."""
    return {k: v for k, v in os.environ.items() if k != LOGIN_ENV}


def claude_env():
    """The environment of the claude child alone: this unit's, plus the run's own
    Claude login read from $CREDENTIALS_DIRECTORY (TZ-55 B2.3). Raises
    common.CredentialMissing when the login is absent."""
    env = writer_env()
    env[LOGIN_ENV] = common.load_credential(LOGIN_CREDENTIAL)
    return env


def category(value):
    """A categorical result.json field as one token for the summary line."""
    if value is None or value == "":
        return "-"
    return re.sub(r"[^A-Za-z0-9_.:-]", "_", str(value))[:64]


def limit_text(value):
    """A cgroup limit for the summary line: the number, `max`, or `-` when unreadable."""
    return "-" if value is None else str(value)


def integer(value):
    """An integer for the summary line, `-` otherwise."""
    return str(value) if isinstance(value, int) and not isinstance(value, bool) else "-"


def finite(value):
    """A finite number for the summary line, `-` otherwise."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return "-"
    return str(value)


def main(argv=None):
    parser = argparse.ArgumentParser(description="one headless analysis run")
    parser.add_argument("--tree", default=common.RUN_TREE)
    parser.add_argument("--limits", action="store_true", help="set this start's limits and exit 0")
    args = parser.parse_args(argv)
    if args.limits:
        return set_limits()
    tree = os.path.abspath(args.tree)
    line = {"requests": 0, "admitted": "no", "waited_s": 0, "writer_exit": "-", "claude_exit": "-",
            "is_error": "true", "num_turns": 0, "duration_ms": 0, "denials": 0, "answer_chars": 0}
    extra = {"models": "-", "denied_tools": "-"}
    extra.update((name, "-") for name in RESULT_CATEGORIES)
    # TZ-56 12.4: the limits the run ran under, its peaks and its token usage.
    seen = {"memory_max": None, "memory_swap_max": None, "mem_available": "-", "swap_free": "-"}
    usage = {"input_tokens": "-", "output_tokens": "-", "cache_read_tokens": "-",
             "cache_creation_tokens": "-", "cost_usd": "-"}
    in_session = {"on": False, "notified": False}

    def summary():
        common.log("crypto-run: requests=%(requests)s admitted=%(admitted)s waited_s=%(waited_s)s "
                   "writer_exit=%(writer_exit)s claude_exit=%(claude_exit)s is_error=%(is_error)s "
                   "num_turns=%(num_turns)s duration_ms=%(duration_ms)s denials=%(denials)s "
                   "answer_chars=%(answer_chars)s" % line)
        # Model ids, denied tool names and result.json's categorical fields (TZ-54 §14,
        # TZ-55 B2.4); never the answer.
        common.log("crypto-run: models=%(models)s denied_tools=%(denied_tools)s subtype=%(subtype)s "
                   "api_error_status=%(api_error_status)s terminal_reason=%(terminal_reason)s "
                   "stop_reason=%(stop_reason)s" % extra)
        # TZ-56 12.4, every path; never `result`.
        common.log("crypto-run: memory_max=%s memory_swap_max=%s mem_available=%s swap_free=%s memory_peak=%s "
                   "memory_swap_peak=%s input_tokens=%s output_tokens=%s cache_read_tokens=%s "
                   "cache_creation_tokens=%s cost_usd=%s"
                   % (limit_text(seen["memory_max"]), limit_text(seen["memory_swap_max"]), seen["mem_available"],
                      seen["swap_free"], integer(_own_cgroup_limit("memory.peak")),
                      integer(_own_cgroup_limit("memory.swap.peak")), usage["input_tokens"],
                      usage["output_tokens"], usage["cache_read_tokens"], usage["cache_creation_tokens"],
                      usage["cost_usd"]))

    def on_term(signum, frame):
        if in_session["on"] and not in_session["notified"]:
            in_session["notified"] = True
            common.write_outbox("notice", common.S7)
        summary()
        sys.exit(128 + signum)

    signal.signal(signal.SIGTERM, on_term)

    line["requests"] = consume_requests()
    admitted, waited = admit(seen)
    line["admitted"], line["waited_s"] = ("yes" if admitted else "no"), waited
    if not admitted:
        common.write_outbox("notice", common.S6)
        summary()
        return EXIT_NOT_ADMITTED

    prepare_tree(tree)
    line["writer_exit"] = subprocess.run([sys.executable, WRITER, "--tree", tree], env=writer_env()).returncode

    runtime_dir = os.environ.get("RUNTIME_DIRECTORY") or tempfile.mkdtemp(prefix="crypto-run.")
    result_path = os.path.join(runtime_dir, "result.json")
    try:
        env = claude_env()
    except common.CredentialMissing:
        env = None
        common.log("crypto-run: credential %s absent, no session started" % LOGIN_CREDENTIAL)
    in_session["on"] = True
    if env is not None:
        with open(result_path, "wb") as out:
            line["claude_exit"] = subprocess.run(CLAUDE, cwd=tree, stdin=subprocess.DEVNULL, stdout=out,
                                                 env=env).returncode
    in_session["on"] = False
    env = None

    try:
        with open(result_path, encoding="utf-8") as fh:
            doc = json.load(fh)
        if not isinstance(doc, dict):
            doc = {}
    except (OSError, ValueError):
        doc = {}
    result = doc.get("result")
    is_error = doc.get("is_error") is not False
    denials = doc.get("permission_denials") or []
    line["is_error"] = "true" if is_error else "false"
    line["num_turns"] = doc.get("num_turns", 0)
    line["duration_ms"] = doc.get("duration_ms", 0)
    line["denials"] = len(denials)
    extra["models"] = ",".join(sorted(doc.get("modelUsage") or {})) or "-"
    extra["denied_tools"] = ",".join(sorted({str(d.get("tool_name")) for d in denials if isinstance(d, dict)})) or "-"
    for name in RESULT_CATEGORIES:
        extra[name] = category(doc.get(name))
    tokens = doc.get("usage") if isinstance(doc.get("usage"), dict) else {}
    for field, key in (("input_tokens", "input_tokens"), ("output_tokens", "output_tokens"),
                       ("cache_read_tokens", "cache_read_input_tokens"),
                       ("cache_creation_tokens", "cache_creation_input_tokens")):
        usage[field] = integer(tokens.get(key))
    usage["cost_usd"] = finite(doc.get("total_cost_usd"))
    answered =(not is_error) and isinstance(result, str) and result.strip() != ""
    if answered:
        common.write_outbox("answer", result)
        line["answer_chars"] = len(result)
    else:
        common.write_outbox("notice", common.S7)

    # Step 7: the run's own scratch; commits stay where the session put them.
    git(tree, "clean", "-q", "-fdx")
    git(tree, "checkout", "-q", "--", ".")
    summary()
    return 0 if answered else 1


if __name__ == "__main__":
    sys.exit(main())
