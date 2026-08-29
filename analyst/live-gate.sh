#!/usr/bin/env bash
#
# analyst/live-gate.sh — the analyst's live-data gate (TZ-17 Stage A).
#
# It READS A FILE. It opens no socket: there is no curl, no wget, no netcat and
# no HTTP client anywhere below, and adding one is a scope violation. TZ-16
# measured every market host refusing this session at CONNECT, so the engine
# does not fetch prices at all — the payload is delivered into the repository by
# the Boss's Shortcut and read from disk here.
#
# Usage:
#   live-gate.sh              validate analyst/live.json, print one JSON object
#   live-gate.sh --selftest   offline known-answer fixtures, print checks=N
#   live-gate.sh --now        print the UTC ISO timestamp from `date -u`
#
# Exit codes — one distinct code per failure class (TZ-17 §3.A.3):
#   0  every check passed
#   2  payload missing, unparseable, or its `ts` is absent/unparseable   (checks 1, 2)
#   3  payload lies outside the freshness window, either side            (check 3)
#   4  `n` disagrees with len(c)                                         (check 4)
#   5  a tokens[] symbol is absent from the payload                      (check 5)
#   6  a `p`, `h` or `l` does not cast to a finite number > 0            (check 6)
#   7  no comparisons were performed                                     (check 7)
#   8  the universe is unreadable: tokens[] could not be cut from index.html
#   9  usage error
#
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
PAYLOAD="$ROOT/analyst/live.json"   # path fixed: no argument, no env var, no URL
INDEX="$ROOT/index.html"            # the universe's only source (TZ-17 §A.1)

# The clock. `--now` prints this same value, so a run has exactly one clock.
now_utc() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# ---------------------------------------------------------------------------
# The validator. ONE copy, used by real input and by every selftest fixture
# alike (inv. 21 — a selftest that exercises a second validator proves nothing
# about the first). Arguments: <payload> <now-iso> <index.html>, or
# `--universe <index.html>` to print the symbol list the same parser produces.
# ---------------------------------------------------------------------------
VALIDATOR='
import json, math, re, sys
from datetime import datetime

E_PARSE, E_STALE, E_COUNT, E_COVER, E_PRICE, E_NODATA, E_UNIVERSE = 2, 3, 4, 5, 6, 7, 8

# The freshness window, both sides, declared once each (inv. 20): no comparison
# site below carries either number as a literal. The floor exists because the
# producer and the reader are different machines with independent clocks, and a
# ceiling alone accepts every payload stamped in the future (TZ-18 §2).
LIVE_MAX_AGE_SEC = 900   # ceiling: how far behind now the payload may be, in seconds
LIVE_SKEW_SEC = 120      # floor: how far ahead of now the producer may plausibly be

def die(code, msg):
    sys.stderr.write("live-gate: " + msg + "\n")
    raise SystemExit(code)

def iso(text):
    """ISO-8601, offset form accepted; a trailing Z is an offset of +00:00."""
    text = text.strip()
    if text.endswith("Z") or text.endswith("z"):
        text = text[:-1] + "+00:00"
    return datetime.fromisoformat(text)

def universe(index_path):
    """Cut tokens[] out of index.html at run time. A hard-coded list of coins is
    banned (inv. 21, TZ-17 §A.1)."""
    try:
        with open(index_path, encoding="utf-8", errors="replace") as fh:
            html = fh.read()
    except OSError as exc:
        die(E_UNIVERSE, "universe: cannot read %s (%s)" % (index_path, exc.__class__.__name__))
    block = re.search(r"var\s+tokens\s*=\s*\[(.*?)\]\s*;", html, re.S)
    if block is None:
        die(E_UNIVERSE, "universe: tokens[] block not found in %s" % index_path)
    body = re.sub(r"//[^\n]*", "", block.group(1))
    syms = re.findall(r"s\s*:\s*[\x27\"]([^\x27\"]+)[\x27\"]", body)
    if not syms:
        die(E_UNIVERSE, "universe: tokens[] parsed to zero symbols")
    return syms

if len(sys.argv) == 3 and sys.argv[1] == "--universe":
    sys.stdout.write("\n".join(universe(sys.argv[2])) + "\n")
    raise SystemExit(0)

if len(sys.argv) != 4:
    die(9, "internal: expected <payload> <now-iso> <index.html>")

payload_path, now_iso, index_path = sys.argv[1], sys.argv[2], sys.argv[3]

checked = 0    # every comparison, counted at its site (inv. 43)
compared = 0   # row-level comparisons only — the input to check 7 (inv. 22)

tokens = universe(index_path)

# --- check 1: the file exists and parses as JSON ---------------------------
try:
    with open(payload_path, encoding="utf-8") as fh:
        raw = fh.read()
except OSError:
    die(E_PARSE, "check 1: payload not readable: %s" % payload_path)
checked += 1
try:
    doc = json.loads(raw)
except ValueError as exc:
    die(E_PARSE, "check 1: payload is not valid JSON (%s)" % exc.__class__.__name__)
checked += 1
if not isinstance(doc, dict):
    die(E_PARSE, "check 1: payload top level is %s, not a JSON object" % type(doc).__name__)
checked += 1

# --- check 2: ts present and parseable, offset form accepted ---------------
ts_raw = doc.get("ts")
checked += 1
if not isinstance(ts_raw, str) or not ts_raw.strip():
    die(E_PARSE, "check 2: ts absent or not a non-empty string")
try:
    ts = iso(ts_raw)
except ValueError:
    die(E_PARSE, "check 2: ts is not parseable ISO-8601: %r" % ts_raw)
checked += 1
if ts.tzinfo is None:
    die(E_PARSE, "check 2: ts carries no UTC offset, its age is undefined: %r" % ts_raw)
checked += 1

# --- check 3: -LIVE_SKEW_SEC <= now - ts <= LIVE_MAX_AGE_SEC --------------
# now comes from `date -u`. Both sides fail as E_STALE: no caller distinguishes
# "too old" from "too new", both mean the payload is not usable as now. The
# stderr line names the side, so the day log records them as different
# observations (TZ-18 §2). age_sec keeps its sign and is never clamped.
try:
    now = iso(now_iso)
except ValueError:
    die(9, "internal: --now value is not parseable ISO-8601: %r" % now_iso)
age = (now - ts).total_seconds()
checked += 1
if age > LIVE_MAX_AGE_SEC:
    die(E_STALE, "check 3: payload is stale, age %.0f s exceeds the %d s ceiling"
        % (age, LIVE_MAX_AGE_SEC))
checked += 1
if age < -LIVE_SKEW_SEC:
    die(E_STALE, "check 3: payload is ahead of now, age %.0f s is below the -%d s floor"
        % (age, LIVE_SKEW_SEC))

# --- check 4: n equals len(c) ----------------------------------------------
# Not redundant: TZ-16 used it to prove a whole file had been delivered rather
# than a truncated one, and it costs one comparison.
rows = doc.get("c")
if not isinstance(rows, list):
    die(E_COUNT, "check 4: c is absent or not an array")
n = doc.get("n")
if isinstance(n, bool) or not isinstance(n, int):
    die(E_COUNT, "check 4: n is absent or not an integer")
checked += 1
if n != len(rows):
    die(E_COUNT, "check 4: n=%d disagrees with len(c)=%d" % (n, len(rows)))

# A payload with no rows is the zero-data case, and it is check 7 rather than a
# coverage failure: with nothing to compare, "symbols missing" and "no data at
# all" are the same observation, and inv. 22 names the second one.
if not rows:
    die(E_NODATA, "check 7: payload carries zero rows, no comparison possible")

# --- check 5: every tokens[] symbol present in c ---------------------------
# One-directional: extra symbols in the payload are allowed and counted.
present = set()
for idx, row in enumerate(rows):
    if not isinstance(row, dict):
        die(E_COVER, "check 5: row %d is not a JSON object" % idx)
    sym = row.get("s")
    if not isinstance(sym, str) or not sym:
        die(E_COVER, "check 5: row %d carries no symbol field s" % idx)
    present.add(sym)

missing = []
for sym in tokens:
    checked += 1
    compared += 1
    if sym not in present:
        missing.append(sym)
if missing:
    die(E_COVER, "check 5: %d tokens[] symbol(s) absent from payload: %s"
        % (len(missing), ",".join(sorted(missing))))
known = set(tokens)
extra = 0
for sym in sorted(present):
    checked += 1
    compared += 1
    if sym not in known:
        extra += 1

# --- check 6: p, h, l cast to a finite number > 0, for every row -----------
# The string trap. Every price in the payload is a JSON string; float("NaN")
# returns nan without raising, and nan compared with anything is false, so a
# corrupt row passes a naive range check by failing it quietly. The cast is
# therefore explicit and the result is tested for finiteness before magnitude.
for idx, row in enumerate(rows):
    sym = row.get("s")
    for field in ("p", "h", "l"):
        value = row.get(field)
        checked += 1
        compared += 1
        if value is None:
            die(E_PRICE, "check 6: row %d (%s) has no field %s" % (idx, sym, field))
        if isinstance(value, bool):
            die(E_PRICE, "check 6: row %d (%s) field %s is a boolean" % (idx, sym, field))
        try:
            number = float(value)
        except (TypeError, ValueError):
            die(E_PRICE, "check 6: row %d (%s) field %s does not cast to a number: %r"
                % (idx, sym, field, value))
        if not math.isfinite(number):
            die(E_PRICE, "check 6: row %d (%s) field %s casts to a non-finite value: %r"
                % (idx, sym, field, value))
        if not number > 0:
            die(E_PRICE, "check 6: row %d (%s) field %s is not greater than zero: %r"
                % (idx, sym, field, value))

# --- check 7: comparisons performed > 0 ------------------------------------
# A validator that passes with no data is a failed validator (inv. 22).
checked += 1
if compared <= 0:
    die(E_NODATA, "check 7: zero comparisons performed")

sys.stdout.write(json.dumps({"ts": ts_raw, "age_sec": int(round(age)),
                             "n": n, "checked": checked},
                            separators=(",", ":")) + "\n")
'

# Run the validator. stdout is forwarded ONLY on success: a partial payload on
# stdout is the exact shape a caller mistakes for a good one, so a failing run
# prints nothing there and names the failed check on stderr instead.
gate_run() {   # <payload> <now-iso> <index.html>
    local out rc=0
    out="$(python3 -c "$VALIDATOR" "$1" "$2" "$3")" || rc=$?
    if [ "$rc" -eq 0 ]; then
        printf '%s\n' "$out"
    fi
    return "$rc"
}

# ---------------------------------------------------------------------------
# Fixture builder. It writes files; it never decides whether one is valid —
# every fixture is judged by gate_run above, the same path real input takes.
# The complete payload is generated FROM tokens[], never from a list typed into
# this file, so a change to the universe cannot leave the selftest behind.
# ---------------------------------------------------------------------------
FIXTURES='
import json, sys

case, out_path, ts_text = sys.argv[1], sys.argv[2], sys.argv[3]
tokens = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]

def row(sym, price="100.5"):
    return {"s": sym, "p": price, "h": "110.25", "l": "90.75", "chg": "-2.624",
            "qv": "17258974316.00", "mark": "100.60", "fr": "0.00009267",
            "oi": "107001.448"}

# The regime reference BTCUSDT is in the payload and not in tokens[]: an extra
# symbol, allowed and counted (TZ-17 §A.1).
rows = [row("BTCUSDT")] + [row(sym) for sym in tokens]
doc = {"ts": ts_text, "src": "fapi", "n": len(rows), "c": rows}

if case == "fresh":
    pass
elif case == "stale16":
    pass                                   # caller supplies a ts 16 minutes old
elif case == "future121":
    pass                                   # caller supplies a ts 121 s ahead of now
elif case == "future_ok":
    pass                                   # caller supplies a ts 60 s ahead of now
elif case == "no_ts":
    del doc["ts"]
elif case == "n_mismatch":
    doc["n"] = len(rows) + 1
elif case == "missing_symbol":
    doc["c"] = [r for r in rows if r["s"] != tokens[0]]
    doc["n"] = len(doc["c"])
elif case == "price_abc":
    doc["c"][-1]["p"] = "abc"
elif case == "price_zero":
    doc["c"][-1]["p"] = "0"
elif case == "price_nan":
    doc["c"][-1]["p"] = "NaN"
elif case == "empty_c":
    doc["c"] = []
    doc["n"] = 0
else:
    sys.stderr.write("fixture: unknown case %s\n" % case)
    raise SystemExit(9)

with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(doc, fh)
'

# Each case asserts the EXACT exit code, that stdout is empty on failure and one
# JSON object carrying exactly ts/age_sec/n/checked on success, and that a
# failure names a check on stderr. Every assertion increments checks.
CASES=(
    "fresh:0"
    "stale16:3"
    "future121:3"
    "future_ok:0"
    "no_ts:2"
    "bad_json:2"
    "n_mismatch:4"
    "missing_symbol:5"
    "price_abc:6"
    "price_zero:6"
    "price_nan:6"
    "empty_c:7"
    "file_absent:2"
    "universe_unreadable:8"
)

# Global, not local: the EXIT trap runs after selftest() has returned, and a
# `local` is out of scope by then — under `set -u` that turns a passing selftest
# into exit 1, which is the failure mode inv. 25 names, wearing the other face.
SELFTEST_TMP=""
cleanup_selftest() { [ -n "$SELFTEST_TMP" ] && rm -rf "$SELFTEST_TMP"; }

selftest() {
    local checks=0 failures=0 syms
    SELFTEST_TMP="$(mktemp -d)"
    trap cleanup_selftest EXIT
    local tmp="$SELFTEST_TMP"

    # One clock for the whole selftest, from the same source a real run uses.
    local now fresh_ts stale_ts future_ts skew_ts
    now="$(now_utc)"
    fresh_ts="$(date -u -d "$now" +%Y-%m-%dT%H:%M:%S+00:00)"
    stale_ts="$(date -u -d "$now - 16 minutes" +%Y-%m-%dT%H:%M:%S+04:00)"
    # stale_ts deliberately carries a +04:00 offset, the form TZ-16 measured, so
    # the offset path is exercised rather than only the Z form.
    # The two future stamps straddle the floor by one second and are written in
    # UTC: the assertion is about the window, and an offset here would move the
    # instant rather than only its spelling.
    future_ts="$(date -u -d "$now + 121 seconds" +%Y-%m-%dT%H:%M:%S+00:00)"
    skew_ts="$(date -u -d "$now + 60 seconds" +%Y-%m-%dT%H:%M:%S+00:00)"

    syms="$(python3 -c "$VALIDATOR" --universe "$INDEX")"
    printf 'universe: %d symbols cut from %s\n' \
        "$(printf '%s\n' "$syms" | grep -c .)" "${INDEX#"$ROOT/"}"

    local entry name want payload index_for_case ts_for_case
    local rc out_file err_file out
    for entry in "${CASES[@]}"; do
        name="${entry%%:*}"
        want="${entry##*:}"
        payload="$tmp/$name.json"
        index_for_case="$INDEX"
        ts_for_case="$fresh_ts"

        case "$name" in
            stale16)   ts_for_case="$stale_ts" ;;
            future121) ts_for_case="$future_ts" ;;
            future_ok) ts_for_case="$skew_ts" ;;
            bad_json)  : ;;
            file_absent) : ;;
            universe_unreadable) : ;;
        esac

        case "$name" in
            bad_json)
                printf '%s' '{"ts":"2026-08-28T22:18:50+04:00","n":1,"c":[' > "$payload" ;;
            file_absent)
                payload="$tmp/does-not-exist.json" ;;
            universe_unreadable)
                # A readable file with no tokens[] block in it: the universe is
                # unreadable for the parser, not for the filesystem.
                printf '%s\n' '<html><body>no tokens here</body></html>' > "$tmp/no-tokens.html"
                index_for_case="$tmp/no-tokens.html"
                printf '%s\n' "$syms" | python3 -c "$FIXTURES" fresh "$payload" "$ts_for_case" ;;
            *)
                printf '%s\n' "$syms" | python3 -c "$FIXTURES" "$name" "$payload" "$ts_for_case" ;;
        esac

        out_file="$tmp/$name.out"; err_file="$tmp/$name.err"
        rc=0
        gate_run "$payload" "$now" "$index_for_case" >"$out_file" 2>"$err_file" || rc=$?

        # assertion 1 — the exact exit code
        checks=$((checks + 1))
        if [ "$rc" -ne "$want" ]; then
            printf 'FAIL %-20s expected exit %s, got %s\n' "$name" "$want" "$rc" >&2
            failures=$((failures + 1))
        fi

        # assertion 2 — stdout discipline
        checks=$((checks + 1))
        if [ "$want" -eq 0 ]; then
            out="$(cat "$out_file")"
            if ! printf '%s' "$out" | python3 -c '
import json, sys
doc = json.loads(sys.stdin.read())
assert list(doc.keys()) == ["ts", "age_sec", "n", "checked"], doc
' 2>/dev/null; then
                printf 'FAIL %-20s stdout is not one {ts,age_sec,n,checked} object: %s\n' \
                    "$name" "$out" >&2
                failures=$((failures + 1))
            fi
        elif [ -s "$out_file" ]; then
            printf 'FAIL %-20s failure wrote %s bytes to stdout, expected none\n' \
                "$name" "$(wc -c < "$out_file")" >&2
            failures=$((failures + 1))
        fi

        # assertion 3 — a failure names its check on stderr, on exactly one line
        if [ "$want" -ne 0 ]; then
            checks=$((checks + 1))
            if [ "$(grep -c . "$err_file")" -ne 1 ]; then
                printf 'FAIL %-20s expected one stderr line, got %s\n' \
                    "$name" "$(grep -c . "$err_file")" >&2
                failures=$((failures + 1))
            fi
        fi

        printf '  %-20s exit=%s expected=%s  %s\n' \
            "$name" "$rc" "$want" "$(head -c 96 "$err_file" | tr -d '\n')"
    done

    printf 'checks=%d\n' "$checks"
    if [ "$checks" -eq 0 ]; then
        printf 'selftest: zero checks performed — a selftest that compares nothing is not evidence\n' >&2
        return 1
    fi
    if [ "$failures" -ne 0 ]; then
        printf 'selftest: %d assertion(s) failed\n' "$failures" >&2
        return 1
    fi
    printf 'selftest: %d cases, all exit codes as specified\n' "${#CASES[@]}"
    return 0
}

case "${1-}" in
    "")          gate_run "$PAYLOAD" "$(now_utc)" "$INDEX" ;;
    --selftest)  selftest ;;
    --now)       now_utc ;;
    *)
        printf 'usage: %s [--selftest|--now]\n' "${0##*/}" >&2
        exit 9
        ;;
esac
