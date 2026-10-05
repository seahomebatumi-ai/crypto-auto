#!/usr/bin/env python3
"""The owner's stop (TZ-60 B4): crypto-stop.service's program, started by
crypto-stop.path when the bot leaves a .stop file in the spool. It consumes the
stop requests, removes every pending run request, stops the run unit with
systemd's own stop — every process of its cgroup, the session and its tools
included — clears the unit's failed state and start counter, and writes one
notice. It reads no credential and starts no model.

    stop.py [--unit <name>] [--spool <dir>]    defaults crypto-run.service and /var/spool/crypto-auto

Exit 0, or 1 when the unit still runs after the stop (notice S15).
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

RUNNING = ("active", "activating", "deactivating", "reloading", "refreshing")


def consume(directory, suffix):
    """Delete every file of directory ending with suffix whose name does not
    start with "."; returns the count. A missing directory counts 0."""
    n = 0
    try:
        names = os.listdir(directory)
    except FileNotFoundError:
        return 0
    for name in names:
        if name.endswith(suffix) and not name.startswith("."):
            try:
                os.unlink(os.path.join(directory, name))
                n += 1
            except FileNotFoundError:
                pass
    return n


def unit_state(unit):
    """The first line of `systemctl is-active <unit>`'s stdout, stripped; "-" when empty."""
    out = subprocess.run(["systemctl", "is-active", unit], capture_output=True, text=True).stdout
    lines = out.strip().splitlines()
    return lines[0].strip() if lines and lines[0].strip() else "-"


def choose(before, requests_removed, after):
    """The notice's id: S13 stopped, S15 still running, S14 nothing to stop."""
    if before in RUNNING or requests_removed > 0:
        return "S15" if after in RUNNING else "S13"
    return "S14"


def main(argv=None):
    parser = argparse.ArgumentParser(description="the owner's stop")
    parser.add_argument("--unit", default=common.RUN_UNIT)
    parser.add_argument("--spool", default=common.SPOOL_DIR)
    args = parser.parse_args(argv)
    stops = consume(os.path.join(args.spool, "stop"), ".stop")   # first, so that its path unit cannot loop
    requests = consume(os.path.join(args.spool, "requests"), ".req")
    before = unit_state(args.unit)
    stop_exit = subprocess.run(["systemctl", "stop", args.unit]).returncode
    reset_exit = subprocess.run(["systemctl", "reset-failed", args.unit], capture_output=True).returncode
    after = unit_state(args.unit)
    notice = choose(before, requests, after)
    common.write_outbox("notice", getattr(common, notice), outbox_dir=os.path.join(args.spool, "outbox"))
    common.log("crypto-stop: stops=%d requests_removed=%d before=%s stop_exit=%d reset_exit=%d after=%s notice=%s"
               % (stops, requests, before, stop_exit, reset_exit, after, notice))
    return 1 if notice == "S15" else 0


if __name__ == "__main__":
    sys.exit(main())
