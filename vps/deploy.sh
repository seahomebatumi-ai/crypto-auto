#!/usr/bin/env bash
#
# vps/deploy.sh — the deployer's tick (TZ-54 B8, TZ-55 §12.9). Installed as
# /usr/local/libexec/crypto-auto/deploy.sh and run by crypto-deploy.timer.
# Merge is deployment (contract §7 item 15): this acts on origin/main only, and
# installs a vps tree only from a commit GitHub signed.
#
#   deploy.sh           one tick
#   deploy.sh --check   steps 2 and 4 only: prints `deploy: check commit=<h> signed=<yes|no>`
#                       and exits 0 when signed, 1 otherwise; it fast-forwards, writes and
#                       installs nothing
#
set -euo pipefail
export HOME="${HOME:-/root}"

CLONE=/srv/crypto-auto
LOCK=/run/lock/crypto-auto-git.lock
MARKER=/var/lib/crypto-auto/deployed-vps-tree
REFUSED=/var/lib/crypto-auto/refused-vps-tree
OUTBOX=/var/spool/crypto-auto/outbox
# GitHub's own signing key, installed outside the repository and never read from
# the tree it verifies (contract §7 item 15).
SIGNERS=/etc/crypto-auto/gnupg
# S10 of TZ-54 §12.1 and S11 of TZ-55 §12.1, as JSON \u escapes (rule 6).
S10_JSON='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 \u043d\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e: \u0441\u0430\u043c\u043e\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043d\u0435 \u043f\u0440\u043e\u0448\u043b\u0430.'
S11_JSON='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 \u043d\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e: \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435 \u043d\u0435 \u043f\u043e\u0434\u043f\u0438\u0441\u0430\u043d\u043e GitHub.'

mode="${1-}"
case "$mode" in
    ""|--check) ;;
    *) echo "usage: deploy.sh [--check]" >&2; exit 9 ;;
esac

# Writes <content> to <target> through a temporary file beside it and a rename;
# on failure both are removed (inv. 72).
atomic_write() {   # <target> <content> <mode>
    local tmp
    tmp="$(mktemp "$(dirname -- "$1")/.$(basename -- "$1").XXXXXX")" || return 1
    if printf '%s' "$2" > "$tmp" && chmod "$3" "$tmp" && mv -f -- "$tmp" "$1"; then
        return 0
    fi
    rm -f -- "$tmp" "$1"
    return 1
}

# The Boss is told once per refused tree, whichever the reason: the notice goes to
# the outbox only when the refused-tree marker differs from <tree>, and <tree> is
# then written there.
tell_once() {   # <tree> <JSON-escaped text>
    local refused ms
    refused="$(cat "$REFUSED" 2>/dev/null || true)"
    if [ "$refused" != "$1" ]; then
        ms="$(date +%s%3N)"
        atomic_write "$OUTBOX/$ms-notice-$$.json" "{\"kind\":\"notice\",\"text\":\"$2\",\"created_ms\":$ms}" 0640 || true
        atomic_write "$REFUSED" "$1" 0644
    fi
}

# The newest commit on origin/main's first-parent line that changed vps/: a merged
# pull request or a Boss upload, never a branch's own commit.
vps_commit() {
    git -C "$CLONE" log --first-parent -1 --format=%H origin/main -- vps
}

signed() {   # <commit>
    [ -n "$1" ] && GNUPGHOME="$SIGNERS" git -C "$CLONE" verify-commit "$1" >/dev/null 2>&1
}

# 1. A run is active: the tick is skipped.
if [ "$mode" != "--check" ] && [ -e /run/crypto-run ]; then
    echo "deploy: run active, tick skipped"
    exit 0
fi

# 2. Under the git lock: fetch.
exec 9>"$LOCK"
flock 9
git -C "$CLONE" fetch -q origin main

if [ "$mode" = "--check" ]; then
    c="$(vps_commit)"
    if signed "$c"; then
        echo "deploy: check commit=$c signed=yes"
        exit 0
    fi
    echo "deploy: check commit=${c:--} signed=no"
    exit 1
fi

# 3. No vps tree on origin/main: log it, fast-forward (TZ-54's behaviour).
tree="$(git -C "$CLONE" rev-parse -q --verify 'origin/main:vps' 2>/dev/null || true)"
if [ -z "$tree" ]; then
    echo "deploy: no vps tree on origin/main"
    git -C "$CLONE" merge -q --ff-only origin/main
    exit 0
fi

# 4. The commit that put this vps tree on main must carry GitHub's signature;
#    otherwise no fast-forward and no install (contract §7 item 15).
c="$(vps_commit)"
if ! signed "$c"; then
    echo "deploy: unsigned vps commit ${c:--}, not installed"
    tell_once "$tree" "$S11_JSON"
    exit 1
fi

# 5. Fast-forward.
git -C "$CLONE" merge -q --ff-only origin/main

# 6. Install only when the vps tree moved.
deployed="$(cat "$MARKER" 2>/dev/null || true)"
if [ "$tree" = "$deployed" ]; then
    echo "deploy: vps tree $tree already installed"
    exit 0
fi

# 7. Install; the refused-tree marker serves this refusal and step 4's.
if bash "$CLONE/vps/install.sh"; then
    atomic_write "$MARKER" "$tree" 0644
    echo "deploy: installed vps tree $tree"
    exit 0
fi
tell_once "$tree" "$S10_JSON"
echo "deploy: install refused for vps tree $tree"
exit 1
