#!/usr/bin/env bash
#
# vps/deploy.sh — the deployer's tick (TZ-54 B8). Installed as
# /usr/local/libexec/crypto-auto/deploy.sh and run by crypto-deploy.timer.
# Merge is deployment (contract §7 item 15): this acts on origin/main only.
#
set -euo pipefail
export HOME="${HOME:-/root}"

CLONE=/srv/crypto-auto
LOCK=/run/lock/crypto-auto-git.lock
MARKER=/var/lib/crypto-auto/deployed-vps-tree
OUTBOX=/var/spool/crypto-auto/outbox
# S10 of TZ-54 §12.1, as JSON \u escapes (TZ-54 rule 6).
S10_JSON='\u041e\u0431\u043d\u043e\u0432\u043b\u0435\u043d\u0438\u0435 \u0441\u0435\u0440\u0432\u0435\u0440\u0430 \u043d\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e: \u0441\u0430\u043c\u043e\u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043d\u0435 \u043f\u0440\u043e\u0448\u043b\u0430.'

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

# 1. A run is active: the tick is skipped.
if [ -e /run/crypto-run ]; then
    echo "deploy: run active, tick skipped"
    exit 0
fi

# 2. Under the git lock run.py shares: fetch, read the vps tree, fast-forward.
exec 9>"$LOCK"
flock 9
git -C "$CLONE" fetch -q origin main
tree="$(git -C "$CLONE" rev-parse -q --verify 'origin/main:vps' 2>/dev/null || true)"
if [ -z "$tree" ]; then
    echo "deploy: no vps tree on origin/main"
fi
git -C "$CLONE" merge -q --ff-only origin/main
if [ -z "$tree" ]; then
    exit 0
fi

# 3. Install only when the vps tree moved.
deployed="$(cat "$MARKER" 2>/dev/null || true)"
if [ "$tree" = "$deployed" ]; then
    echo "deploy: vps tree $tree already installed"
    exit 0
fi
if bash "$CLONE/vps/install.sh"; then
    atomic_write "$MARKER" "$tree" 0644
    echo "deploy: installed vps tree $tree"
    exit 0
fi
ms="$(date +%s%3N)"
atomic_write "$OUTBOX/$ms-notice-$$.json" "{\"kind\":\"notice\",\"text\":\"$S10_JSON\",\"created_ms\":$ms}" 0640 || true
echo "deploy: install refused for vps tree $tree"
exit 1
