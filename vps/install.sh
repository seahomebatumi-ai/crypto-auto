#!/usr/bin/env bash
#
# vps/install.sh — installs the VPS assistant from the checkout it sits in (TZ-54 B9, TZ-55 B5, TZ-64 B3,
# TZ-72 B1).
#
#   install.sh              called by the deployer from /srv/crypto-auto: selftest, provision,
#                           the run's own CLI, verify, install units, enable the manifest,
#                           disable the rest
#   install.sh --bootstrap  once, from the TZ-54 branch: users, directories, clone,
#                           deploy.sh, crypto-deploy.service and .timer, the timer enabled
#   install.sh --provision  users, groups, directories, the run's and the paper test's own
#                           clones and known_hosts — nothing installed, enabled, copied or removed
#   install.sh --dry-run    prints what the default mode would do and changes nothing
#
# The run has its own unprivileged user, cryptorun, and its own clone under its home
# (contract §7 item 6, since v25); nothing creates /srv/crypto-auto-run any more. The paper
# test has its own, cryptopaper, the same way (contract §7 item 6, since v30).
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
PAPER_HOME=/var/lib/cryptopaper
ROOT_KNOWN_HOSTS=/root/.ssh/known_hosts
# TZ-72: the run's own Claude Code -- npm's linux-x64 build at this version, whose one file must hash to this
# SHA-256 -- installed by this script and by nothing else, at $LIBEXEC/claude-code/$CLI_VERSION/claude
# (contract §7 item 15). vps/run.py names the same version; selftest section AA holds the two equal.
CLI_VERSION=2.1.308
CLI_SHA256=356733f185fa988e6bf3aa9a555269fdd167982a2e2a80d3c8a78037bb92ad58
CLI_URL="https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-$CLI_VERSION.tgz"

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
    if ! getent group cryptopaper >/dev/null; then
        groupadd --system cryptopaper
        say "group cryptopaper created"
    fi
    if ! id -u cryptopaper >/dev/null 2>&1; then
        useradd --system --gid cryptopaper --groups cryptoauto --no-create-home --home-dir "$PAPER_HOME" \
            --shell /usr/sbin/nologin cryptopaper
        say "user cryptopaper created"
    fi
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
    dir_as 0750 cryptopaper cryptopaper "$PAPER_HOME"
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

# Root works on a clone another user owns, so git's ownership check is told that one path.
own_git() { local clone="$1"; shift; git -c safe.directory="$clone" -C "$clone" "$@"; }

# A user's own clone under its home: fetched over HTTPS, pushed over SSH with the deploy key its
# unit loads, its committer identity taken from the clone that already commits on this host
# (values never printed), and GitHub's host keys from root's own github.com lines (TZ-54 D-8,
# TZ-55 B5; generalised by TZ-64 B3 for cryptopaper, messages unchanged for cryptorun).
provision_own_clone() {   # <user> <home> <label>
    local user="$1" home="$2" label="$3" clone="$2/crypto-auto"
    if [ ! -d "$clone/.git" ]; then
        git clone -q "$RUN_FETCH" "$clone"
        say "$label clone $clone created"
    fi
    if ! own_git "$clone" config --local --get remote.origin.pushurl >/dev/null; then
        own_git "$clone" config --local remote.origin.pushurl "$REMOTE"
        say "$label clone push URL set"
    fi
    local key value
    for key in user.name user.email; do
        if ! own_git "$clone" config --local --get "$key" >/dev/null; then
            value="$(git -C "$IDENTITY_SOURCE" config --get "$key" || true)"
            if [ -n "$value" ]; then
                own_git "$clone" config --local "$key" "$value"
                say "$label clone $key set"
            fi
        fi
    done
    chown -R "$user:$user" "$clone"
    if [ ! -e "$home/.ssh/known_hosts" ]; then
        local lines tmp
        lines="$(ssh-keygen -F github.com -f "$ROOT_KNOWN_HOSTS" | grep -v '^#' || true)"
        if [ -z "$lines" ]; then
            say "no github.com line in $ROOT_KNOWN_HOSTS; known_hosts for $user not written"
            return 1
        fi
        dir_as 0700 "$user" "$user" "$home/.ssh"
        tmp="$(mktemp "$home/.ssh/.known_hosts.XXXXXX")"
        if printf '%s\n' "$lines" > "$tmp" && chown "$user:$user" "$tmp" && chmod 0644 "$tmp" \
            && mv -f -- "$tmp" "$home/.ssh/known_hosts"; then
            say "known_hosts for $user written: $(printf '%s\n' "$lines" | wc -l) github.com lines"
        else
            rm -f -- "$tmp"
            return 1
        fi
    fi
}

provision_run_clone() { provision_own_clone cryptorun "$RUN_HOME" run; }

provision_paper_clone() { provision_own_clone cryptopaper "$PAPER_HOME" paper; }

copy_deploy() {
    install -m 0755 -o root -g root "$HERE/deploy.sh" "$LIBEXEC/.deploy.sh.new"
    mv -f -- "$LIBEXEC/.deploy.sh.new" "$LIBEXEC/deploy.sh"
}

# TZ-72: true when the pinned CLI is in place and hashes to the pin.
cli_in_place() {
    local cli="$LIBEXEC/claude-code/$CLI_VERSION/claude"
    [ -f "$cli" ] && [ "$(sha256sum -- "$cli" | cut -d ' ' -f 1)" = "$CLI_SHA256" ]
}

# TZ-72: the pinned CLI put in place. A file at its path that does not hash to the pin is removed first, so
# no run starts it; the package is fetched into a directory beside the target, its one file is checked
# against the pin, and only a file that passed is renamed into place -- then every other version goes.
# Every step is checked where it stands: the caller's `if` switches `set -e` off inside this function.
install_cli() {
    local base="$LIBEXEC/claude-code" dir="$LIBEXEC/claude-code/$CLI_VERSION" tmp got old
    if cli_in_place; then
        return 0
    fi
    rm -f -- "$dir/claude"
    if ! install -d -m 0755 -- "$dir" || ! tmp="$(mktemp -d "$base/.fetch.XXXXXX")"; then
        say "claude-code $CLI_VERSION: no directory under $base"
        return 1
    fi
    if ! curl -fsS --max-time 900 -o "$tmp/cli.tgz" "$CLI_URL" \
        || ! tar --no-same-owner -xzf "$tmp/cli.tgz" -C "$tmp" package/claude; then
        rm -rf -- "$tmp"
        say "claude-code $CLI_VERSION not fetched"
        return 1
    fi
    got="$(sha256sum -- "$tmp/package/claude" | cut -d ' ' -f 1)"
    if [ "$got" != "$CLI_SHA256" ]; then
        rm -rf -- "$tmp"
        say "claude-code $CLI_VERSION refused: sha256 $got, pinned $CLI_SHA256"
        return 1
    fi
    if ! chmod 0755 -- "$tmp/package/claude" || ! mv -f -- "$tmp/package/claude" "$dir/claude"; then
        rm -rf -- "$tmp"
        say "claude-code $CLI_VERSION not placed"
        return 1
    fi
    rm -rf -- "$tmp"
    for old in "$base"/*; do
        if [ "$old" != "$dir" ]; then
            rm -rf -- "$old"
            say "removed $old"
        fi
    done
    say "claude-code $CLI_VERSION installed"
}

installable() { grep -q '^\[Install\]' "$UNITS/$1"; }

listed_units() { grep -v -E '^[[:space:]]*(#|$)' "$MANIFEST"; }

if [ "$mode" = "--provision" ]; then
    provision_user
    provision_dirs
    provision_run_clone
    provision_paper_clone
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
    if cli_in_place; then
        say "claude-code $CLI_VERSION in place"
    else
        say "would install claude-code $CLI_VERSION to $LIBEXEC/claude-code/$CLI_VERSION/claude"
    fi
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
provision_paper_clone
if ! install_cli; then
    say "claude-code not in place, nothing installed"
    exit 1
fi
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
