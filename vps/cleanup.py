#!/usr/bin/env python3
"""Retention of run records and the spool (TZ-54 B7, TZ-55 B6).

    cleanup.py [--dry-run]

Touches exactly: the run unit's own record directory under the run user's
/var/lib/cryptorun/.claude/projects/, the outbox and requests spools (a .dead
outbox file ages out like any other), and announcements.jsonl. No other
directory under any .claude/ and no clone. --dry-run prints what would be
removed and removes nothing.
"""
import argparse
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

# The directory the headless run of crypto-run.service creates as cryptorun (TZ-55 E4:
# the directory TZ-55 D2's reading named).
RUN_RECORDS = "/var/lib/cryptorun/.claude/projects/-var-lib-cryptorun-crypto-auto"
# [Architect's decision: about 20 runs, two weeks]
KEEP_NEWEST = 40
KEEP_AGE_S = 14 * 86400
OUTBOX_MAX_AGE_S = 7 * 86400
REQUEST_MAX_AGE_S = 86400
ANNOUNCEMENT_MAX_AGE_MS = 30 * 86400 * 1000
ANNOUNCEMENTS = os.path.join(common.STATE_DIR, "announcements.jsonl")


def select_records(entries, now):
    """entries: (name, mtime). Kept while among the newest KEEP_NEWEST by mtime
    AND younger than KEEP_AGE_S. Returns (kept, removed), each sorted by name."""
    newest = sorted(entries, key=lambda e: e[1], reverse=True)
    kept = {name for rank, (name, mtime) in enumerate(newest) if rank < KEEP_NEWEST and now - mtime < KEEP_AGE_S}
    return sorted(kept), sorted(name for name, _ in entries if name not in kept)


def remove(path, dry_run):
    print(("cleanup: would remove %s" if dry_run else "cleanup: remove %s") % path, flush=True)
    if dry_run:
        return
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    else:
        os.unlink(path)


def old_files(directory, max_age_s, now):
    try:
        names = sorted(os.listdir(directory))
    except FileNotFoundError:
        return []
    out = []
    for name in names:
        path = os.path.join(directory, name)
        if os.path.isfile(path) and now - os.path.getmtime(path) > max_age_s:
            out.append(path)
    return out


def trim_announcements(path, now_ms, dry_run):
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except FileNotFoundError:
        return 0
    keep, dropped = [], 0
    for line in lines:
        try:
            published = json.loads(line).get("publishDate")
        except (ValueError, AttributeError):
            published = None
        if isinstance(published, int) and now_ms - published > ANNOUNCEMENT_MAX_AGE_MS:
            dropped += 1
        else:
            keep.append(line)
    if dropped and not dry_run:
        common.atomic_write(path, "".join(line + "\n" for line in keep))
    return dropped


def main(argv=None):
    parser = argparse.ArgumentParser(description="retention of run records and spool")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    now = time.time()
    kept = removed = 0
    if os.path.isdir(RUN_RECORDS):
        entries = [(name, os.lstat(os.path.join(RUN_RECORDS, name)).st_mtime) for name in os.listdir(RUN_RECORDS)]
        keep, drop = select_records(entries, now)
        kept, removed = len(keep), len(drop)
        for name in drop:
            remove(os.path.join(RUN_RECORDS, name), args.dry_run)
    outbox = old_files(common.OUTBOX_DIR, OUTBOX_MAX_AGE_S, now)
    requests = old_files(common.REQUESTS_DIR, REQUEST_MAX_AGE_S, now)
    for path in outbox + requests:
        remove(path, args.dry_run)
    trimmed = trim_announcements(ANNOUNCEMENTS, int(now * 1000), args.dry_run)
    print("cleanup: run_records kept=%d removed=%d outbox_removed=%d requests_removed=%d "
          "announcements_removed=%d dry_run=%s"
          % (kept, removed, len(outbox), len(requests), trimmed, "yes" if args.dry_run else "no"), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
