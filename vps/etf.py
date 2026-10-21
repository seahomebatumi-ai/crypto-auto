#!/usr/bin/env python3
"""The ETF lane (TZ-69 B1): SoSoValue's daily net flows for the US BTC, ETH and SOL
spot ETFs, read hourly by crypto-etf.service into a record the analysis run reads.
It runs no model and reads one credential, the SoSoValue API key.

    etf.py [--out PATH]    default /var/lib/crypto-auto/etf.json

Per type one POST, no retry: the next hour is the retry. The newest row of a type
is the greatest date, never a position. The record is written whole through
common.atomic_write where at least one type was read, and not at all otherwise.

Prints one line, and of what an answer carried only the date; never the key, a
header or a request body. Exit 0 written · 3 key absent or empty, no request made
· 4 no type read, nothing written.
"""
import argparse
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

CREDENTIAL = "sosovalue-api-key"
PROVIDER = "SoSoValue"
HOST = "openapi.sosovalue.com"
URL = "https://" + HOST + "/openapi/v2/etf/historicalInflowChart"
TYPES = ("us-btc-spot", "us-eth-spot", "us-sol-spot")
# Derived: the Architect's reading of 16.10.2026, where one call timed out at 25 s and answered within 40 s.
ETF_TIMEOUT_S = 40
OUT = common.STATE_DIR + "/etf.json"
# The record's field for each of the answer's fields, in the record's order.
FIELDS = (("net", "totalNetInflow"), ("traded", "totalValueTraded"), ("assets", "totalNetAssets"),
          ("cum", "cumNetInflow"))
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


class Refused(Exception):
    """One type refused; the message is its reason, in the closed vocabulary
    HTTP <status> · transport <exception class> · unparseable · code <value> · no row."""


def finite(value):
    """value cast to a finite float, or None. A bool is not a number here."""
    if value is None or isinstance(value, bool):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if math.isfinite(out) else None


def newest(data):
    """The row of data with the greatest date of form YYYY-MM-DD whose
    totalNetInflow casts to a finite float, whatever order data arrives in;
    None when there is none."""
    best = None
    for row in data:
        if not isinstance(row, dict):
            continue
        date = row.get("date")
        if not isinstance(date, str) or not _DATE.fullmatch(date) or finite(row.get("totalNetInflow")) is None:
            continue
        if best is None or date > best["date"]:
            best = row
    return best


def entry(answer):
    """The record's entry for one parsed answer, or Refused."""
    if not isinstance(answer, dict):
        raise Refused("unparseable")
    code = answer.get("code")
    if not ((code == 0 and not isinstance(code, bool)) or code == "0"):
        raise Refused("code %s" % (code,))
    data = answer.get("data")
    if not isinstance(data, list):
        raise Refused("unparseable")
    row = newest(data)
    if row is None:
        raise Refused("no row")
    out = {"date": row["date"]}
    for name, field in FIELDS:
        out[name] = finite(row.get(field))
    out["rows"] = len(data)
    return out


def read_type(etf_type, key, urlopen):
    """One POST for etf_type: its entry, or Refused."""
    req = urllib.request.Request(URL, data=json.dumps({"type": etf_type}).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "x-soso-api-key": key},
                                 method="POST")
    try:
        with urlopen(req, timeout=ETF_TIMEOUT_S) as resp:
            status, body = resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        raise Refused("HTTP %d" % exc.code) from None
    except Exception as exc:
        raise Refused("transport %s" % exc.__class__.__name__) from None
    if status != 200:
        raise Refused("HTTP %d" % status)
    try:
        answer = json.loads(body.decode("utf-8"))
    except ValueError:
        raise Refused("unparseable") from None
    return entry(answer)


def main(argv=None, urlopen=None):
    parser = argparse.ArgumentParser(description="SoSoValue's US spot ETF daily net flows into a record")
    parser.add_argument("--out", default=OUT)
    args = parser.parse_args(argv)
    urlopen = urlopen or urllib.request.urlopen
    try:
        key = common.load_credential(CREDENTIAL)
    except common.CredentialMissing:
        common.log("etf: read=0 refused=0 written=no newest=-")
        return 3
    types, refused = {}, {}
    for etf_type in TYPES:
        try:
            types[etf_type] = read_type(etf_type, key, urlopen)
        except Refused as exc:
            refused[etf_type] = str(exc)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    written = False
    if types:
        record = {"v": 1, "k": "etf", "ts": ts, "provider": PROVIDER, "host": HOST,
                  "types": types, "refused": refused}
        common.atomic_write(args.out, record, mode=0o640)
        written = True
    top = max((e["date"] for e in types.values()), default="-")
    common.log("etf: read=%d refused=%d written=%s newest=%s"
               % (len(types), len(refused), "yes" if written else "no", top))
    return 0 if written else 4


if __name__ == "__main__":
    sys.exit(main())
