#!/usr/bin/env bash
#
# vps/install.sh — installs the VPS assistant from the checkout it sits in (TZ-54 B9, TZ-55 B5).
#
#   install.sh              called by the deployer from /srv/crypto-auto: selftest, provision,
#                           verify, install units, enable the manifest, disable the rest
#   install.sh --bootstrap  once, from the TZ-54 branch: users, directories, clone,
#                           deploy.sh, crypto-deploy.service and .timer, the timer enabled
#   install.sh --provision  users, groups, directories, the run's own clone and its
#                           known_hosts — nothing installed, enabled, copied or removed
#   install.sh --dry-run    prints what the default mode would do and changes nothing
#
# The run has its own unprivileged user, cryptorun, and its own clone under its home
# (contract §7 item 6, since v25); nothing creates /srv/crypto-auto-run any more.
#
# `disable --now` applies to units that carry an [Install] section: a unit without one
# (crypto-run.service, crypto-stop.service, crypto-cleanup.service, crypto-deploy.service) is
# started only by its timer or path, and stopping crypto-deploy.service would stop this very script.
#
set -euo pipefail

HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(dirname -- "$HERE")"
UNITS="$HERE/units"
MANIFEST="$HERE/manifest"
SYSTEMD=/etc/systemd/system
LIBEXEC=/usr/local/libexec/crypto-auto
CLONE=/srv/crypto-auto
REMOTE=git@github.com:seahomebatumi-ai/crypto-auto.git
IDENTITY_SOURCE=/root/crypto-auto
RUNS_ENABLED=/var/lib/crypto-auto/runs-enabled
RUN_HOME=/var/lib/cryptorun
RUN_CLONE="$RUN_HOME/crypto-auto"
RUN_FETCH=https://github.com/seahomebatumi-ai/crypto-auto.git
ROOT_KNOWN_HOSTS=/root/.ssh/known_hosts

mode="${1-}"
case "$mode" in
    ""|--bootstrap|--provision|--dry-run) ;;
    *) echo "usage: install.sh [--bootstrap|--provision|--dry-run]" >&2; exit 9 ;;
esac

say() { echo "install: $*"; }

dir_as() {   # <mode> <owner> <group> <dir>
    mkdir -p -- "$4"
    chown "$2:$3" -- "$4"
    chmod "$1" -- "$4"
}

provision_user() {
    if ! id -u cryptoauto >/dev/null 2>&1; then
        useradd --system --no-create-home --home-dir /nonexistent --shell /usr/sbin/nologin cryptoauto
        say "user cryptoauto created"
    fi
    if ! getent group cryptorun >/dev/null; then
        groupadd --system cryptorun
        say "group cryptorun created"
    fi
    if ! id -u cryptorun >/dev/null 2>&1; then
        useradd --system --gid cryptorun --groups cryptoauto --no-create-home --home-dir "$RUN_HOME" \
            --shell /usr/sbin/nologin cryptorun
        say "user cryptorun created"
    fi
    case " $(id -nG cryptorun) " in
        *" cryptoauto "*) ;;
        *) usermod -a -G cryptoauto cryptorun; say "user cryptorun added to group cryptoauto" ;;
    esac
}

provision_dirs() {
    dir_as 0755 root root /etc/crypto-auto
    dir_as 0700 root root /etc/crypto-auto/credentials
    dir_as 0755 root root /var/spool/crypto-auto
    dir_as 2770 cryptoauto cryptoauto /var/spool/crypto-auto/outbox
    dir_as 2770 cryptoauto cryptoauto /var/spool/crypto-auto/requests
    dir_as 2770 cryptoauto cryptoauto /var/spool/crypto-auto/stop
    dir_as 0750 cryptoauto cryptoauto /var/lib/crypto-auto
    dir_as 0755 root root "$LIBEXEC"
    dir_as 0750 cryptorun cryptorun "$RUN_HOME"
}

provision_clone() {
    if [ ! -d "$CLONE/.git" ]; then
        git clone -q "$REMOTE" "$CLONE"
        say "clone $CLONE created"
    fi
    # The writer and the run commit from this clone; its committer identity is
    # taken from the clone that already commits on this host, values never printed.
    local key value
    for key in user.name user.email; do
        if ! git -C "$CLONE" config --local --get "$key" >/dev/null; then
            value="$(git -C "$IDENTITY_SOURCE" config --get "$key" || true)"
            if [ -n "$value" ]; then
                git -C "$CLONE" config --local "$key" "$value"
                say "clone $key set"
            fi
        fi
    done
}

# Root works on the clone cryptorun owns, so git's ownership check is told this one path.
run_git() { git -c safe.directory="$RUN_CLONE" -C "$RUN_CLONE" "$@"; }

provision_run_clone() {
    if [ ! -d "$RUN_CLONE/.git" ]; then
        git clone -q "$RUN_FETCH" "$RUN_CLONE"
        say "run clone $RUN_CLONE created"
    fi
    if ! run_git config --local --get remote.origin.pushurl >/dev/null; then
        run_git config --local remote.origin.pushurl "$REMOTE"
        say "run clone push URL set"
    fi
    # The writer and the session commit from this clone; its committer identity is taken
    # from the clone that already commits on this host, values never printed (TZ-54 D-8).
    local key value
    for key in user.name user.email; do
        if ! run_git config --local --get "$key" >/dev/null; then
            value="$(git -C "$IDENTITY_SOURCE" config --get "$key" || true)"
            if [ -n "$value" ]; then
                run_git config --local "$key" "$value"
                say "run clone $key set"
            fi
        fi
    done
    chown -R cryptorun:cryptorun "$RUN_CLONE"
    # GitHub's host keys for cryptorun's pushes: root's own github.com lines.
    if [ ! -e "$RUN_HOME/.ssh/known_hosts" ]; then
        local lines tmp
        lines="$(ssh-keygen -F github.com -f "$ROOT_KNOWN_HOSTS" | grep -v '^#' || true)"
        if [ -z "$lines" ]; then
            say "no github.com line in $ROOT_KNOWN_HOSTS; known_hosts for cryptorun not written"
            return 1
        fi
        dir_as 0700 cryptorun cryptorun "$RUN_HOME/.ssh"
        tmp="$(mktemp "$RUN_HOME/.ssh/.known_hosts.XXXXXX")"
        if printf '%s\n' "$lines" > "$tmp" && chown cryptorun:cryptorun "$tmp" && chmod 0644 "$tmp" \
            && mv -f -- "$tmp" "$RUN_HOME/.ssh/known_hosts"; then
            say "known_hosts for cryptorun written: $(printf '%s\n' "$lines" | wc -l) github.com lines"
        else
            rm -f -- "$tmp"
            return 1
        fi
    fi
}

copy_deploy() {
    install -m 0755 -o root -g root "$HERE/deploy.sh" "$LIBEXEC/.deploy.sh.new"
    mv -f -- "$LIBEXEC/.deploy.sh.new" "$LIBEXEC/deploy.sh"
}

installable() { grep -q '^\[Install\]' "$UNITS/$1"; }

listed_units() { grep -v -E '^[[:space:]]*(#|$)' "$MANIFEST"; }

if [ "$mode" = "--provision" ]; then
    provision_user
    provision_dirs
    provision_run_clone
    say "provision done"
    exit 0
fi

if [ "$mode" = "--bootstrap" ]; then
    provision_user
    provision_dirs
    provision_clone
    copy_deploy
    install -m 0644 -o root -g root "$UNITS/crypto-deploy.service" "$SYSTEMD/crypto-deploy.service"
    install -m 0644 -o root -g root "$UNITS/crypto-deploy.timer" "$SYSTEMD/crypto-deploy.timer"
    systemctl daemon-reload
    systemctl enable --now crypto-deploy.timer
    say "bootstrap done: crypto-deploy.timer enabled"
    exit 0
fi

if [ ! -f "$MANIFEST" ]; then
    say "no vps/manifest; nothing is enabled without one"
    exit 1
fi
mapfile -t listed < <(listed_units)
for u in "${listed[@]}"; do
    [ -f "$UNITS/$u" ] || { say "manifest names $u, absent from vps/units"; exit 1; }
done
is_listed() { local x; for x in "${listed[@]}"; do [ "$x" = "$1" ] && return 0; done; return 1; }

if [ "$mode" = "--dry-run" ]; then
    for f in "$UNITS"/*; do say "would install $SYSTEMD/$(basename -- "$f") (0644)"; done
    for f in "$SYSTEMD"/crypto-*; do
        [ -e "$f" ] || continue
        [ -e "$UNITS/$(basename -- "$f")" ] || say "would remove $f"
    done
    for u in "${listed[@]}"; do say "would enable --now $u"; done
    for f in "$UNITS"/*; do
        u="$(basename -- "$f")"
        if installable "$u" && ! is_listed "$u"; then say "would disable --now $u"; fi
    done
    for u in "${listed[@]}"; do case "$u" in *.service) say "would restart $u" ;; esac; done
    say "would copy vps/deploy.sh to $LIBEXEC/deploy.sh"
    if is_listed crypto-run.path; then say "would create $RUNS_ENABLED"; else say "would remove $RUNS_ENABLED"; fi
    exit 0
fi

cd -- "$REPO"
if ! python3 "$HERE/selftest.py"; then
    say "selftest red, nothing installed"
    exit 1
fi
provision_user
provision_dirs
provision_run_clone
if ! systemd-analyze verify "$UNITS"/*; then
    say "systemd-analyze verify red, nothing installed"
    exit 1
fi
for f in "$UNITS"/*; do
    install -m 0644 -o root -g root "$f" "$SYSTEMD/$(basename -- "$f")"
done
for f in "$SYSTEMD"/crypto-*; do
    [ -e "$f" ] || continue
    u="$(basename -- "$f")"
    if [ ! -e "$UNITS/$u" ]; then
        systemctl disable --now "$u" || true
        rm -f -- "$f"
        say "removed $u"
    fi
done
systemctl daemon-reload
for u in "${listed[@]}"; do
    systemctl enable --now "$u"
    say "enabled $u"
done
for f in "$UNITS"/*; do
    u="$(basename -- "$f")"
    if installable "$u" && ! is_listed "$u"; then
        systemctl disable --now "$u"
        say "disabled $u"
    fi
done
for u in "${listed[@]}"; do
    case "$u" in *.service) systemctl restart "$u"; say "restarted $u" ;; esac
done
copy_deploy
if is_listed crypto-run.path; then
    : > "$RUNS_ENABLED"
    chown cryptoauto:cryptoauto "$RUNS_ENABLED"
    say "runs enabled"
else
    rm -f -- "$RUNS_ENABLED"
    say "runs disabled"
fi
say "installed"
