# Implementation Report — TZ-73

Previous TZ: TZ-72 opened no branch and no pull request (its report, `4f89440`, is on `main`; `git ls-remote --heads
origin` lists no `tz-72` head). Nothing unmerged lies under this session.

## Status

**BLOCKED at C2.** A1 read the server's refusal of the old login, `401 OAuth access token has been revoked.`, so B ran.
A new login was minted on the VPS through the Boss's approval, and `take` placed it (`length=113 matched=yes`). C1 read the
file well formed by the TZ's own tests (`newline_bytes=0 non_empty_lines=1 prefix_ok=1`). C2's probe was then refused
twice, within 26 and 79 seconds of the file's modified time:

```
True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token is invalid.'
```

TZ §7 C2: «A login the server refuses within a minute of its minting is a finding, not noise → BLOCKED, with both lines.»

**The refusal reads *invalid*, not *revoked*, and the file is the reason.** It holds 113 characters, while TZ-55's mint
read 108. Two count-only readings of the file both print `1`. One is `/usr/bin/grep -c 'Store$'`. The other is
`/usr/bin/grep -cE '^sk-ant-oat01-[A-Za-z0-9_-]{95}Store$'`. So the file holds a 108-character `sk-ant-oat01-` string
with the five letters `Store` glued after it. «Store this token securely. You won't be able to see it again.» is the line
the CLI prints under the token (read in the CLI's own bundle). The helper of TZ §10 strips the escape sequences *before*
it matches `sk-ant-oat01-[A-Za-z0-9_-]+`. Where the screen moves the cursor to the next line instead of writing a
newline, the next line's first word joins the token. The controls of §11 plant only `\r\n` between lines, so V1 passed
with this defect present. Details: `### Why C2 refused the new login`.

**What unblocks it** (the Architect's choice; this session made no second write, because §4 authorises one replacement
and that was `take`'s):
- the file cut to its first 108 bytes by a command that prints nothing, then C1–C3 again; the token minted here was
  never displayed and is probably still good; or
- a new mint by a corrected helper. Its `take` would match before stripping, or replace each cursor movement with a
  separator. Its controls would plant the token followed by a cursor movement and a word.

After either, TZ-72 re-runs (`EXECUTE TZ-72`, `-report-2.md`).

## Inbound Filing

None. The TZ was already at its canonical path, `CryptoTZ/TZ-73-run-login-remint.md`, on `origin/main`. It was added by
`f82921f Add files via upload`. Nothing was moved or renamed.

## Scope Executed

**Class: report-only TZ** (contract §8). `## Scope` names no file under `Files to Modify`, `Files to Create` or
`Files to Delete`. The host paths of `### On the VPS, outside the repository` are outside the repository.

- A0 — executed; every reading as required, the gate passed, the tools cut at the TZ's MD5s; V1 ran here and passed.
- A1 — executed, one probe (`tz73-probe-1`), row 2 of §7's table (the server's 401) → B.
- B1–B5 — executed, one tmux session, one code, one `take`. The second code, second session and «Invalid code» paths
  were not needed.
- C1 — executed.
- C2 — executed, two probes (`tz73-probe-2`, `tz73-probe-3`), both refused → **BLOCKED**.
- C3 — executed against the draft of this report. The four lines are `1 0 1 0`, and a stricter second scan printed `0`.
- D — executed; V8 then read nothing left behind.

Three of the four authorised probe units were used.

## Files Created

None in the repository but this report. On the host: `/var/tmp/tz73-tools/` (A0), `/var/tmp/tz73-home/` (A1),
`/root/tz73-token/` and its typescript (B1). The tmux session `tz73-token` existed in B. Each one's removal is under
`## Final Repository State`.

## Files Modified

None in the repository. On the host: `/etc/crypto-auto/credentials/claude-oauth-token`, replaced once by `take` in B4.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

One line each (TZ §9):

- **A1:** `True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token has been revoked.'`,
  `exit=1 0`. Row 2 of §7's table: it starts `True` and `api_error_status` is `401` → B.
- **Minted:** yes, one login, at 2026-10-25 07:33:14 UTC. One tmux session, one code, sent once.
- **`url`:** `urls_found=1 has_state=yes` (second iteration of B2's loop; the first printed `urls_found=0 has_state=no`).
- **`take`:** `length=113 matched=yes`, exit 0.
- **The new file:** `600 root root 113 2026-10-25 07:33:14.587401244 +0000 /etc/crypto-auto/credentials/claude-oauth-token`.
- **C2:** `True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token is invalid.'`, `exit=1 0`,
  twice (probes 2 and 3).
- **C3's last count:** `0`. The stricter scan for the probable 108-character login also printed `0`.

### A0 — the host and the baseline

Run as root in this worktree, after `git merge --ff-only origin/main` brought it from `4f89440` to `f82921f`:

```
$ id -un
root
$ systemctl cat crypto-run.service | grep -nE "^(User=|LoadCredential=claude-oauth-token:)"
11:User=cryptorun
22:LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token
$ command -v tmux script python3 shred systemd-run grep pgrep stat install cmp awk sed md5sum ps
/usr/bin/tmux
/usr/bin/script
/usr/bin/python3
/usr/bin/shred
/usr/bin/systemd-run
grep
/usr/bin/pgrep
/usr/bin/stat
/usr/bin/install
/usr/bin/cmp
/usr/bin/awk
/usr/bin/sed
/usr/bin/md5sum
/usr/bin/ps
$ stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
600 root root 109 2026-10-24 07:58:12.696914869 +0000 /etc/crypto-auto/credentials/claude-oauth-token
$ /usr/bin/claude --version
2.1.282 (Claude Code)
$ git fetch --all --prune
[exit 0]
$ git rev-parse --is-shallow-repository
false
$ git status --porcelain
(nothing)
```

- The first reading is `root`. The second is `User=cryptorun` and the `LoadCredential=` line, at 11 and 22 as TZ-72's A0
  read them.
- The third prints fourteen lines. `grep` prints as a bare name because in this session's shell `grep` is a **function**.
  The function hands its arguments to the session's own CLI binary, unless certain flags are present. GNU grep is
  installed behind it (`/usr/bin/grep`, `/bin/grep`, `grep (GNU grep) 3.11`), so the tool is present and A0 does not
  block. Every `grep` this report shows as run on the host was run as `/usr/bin/grep`, so that the TZ's known answers
  are GNU grep's (`## Deviations`, D-1).
- The fourth reading equals TZ-72's: 109 bytes, mode 600, root, 24.10.2026 07:58:12. The fifth is `2.1.282`. The sixth
  and seventh are as required. The eighth is empty.

Readings beside A0, made with commands §4 lists as readings (`systemctl cat`) or as read-only (the npm install):
- `systemctl cat crypto-run.service` minus its header line, against `vps/units/crypto-run.service`: the fragment
  `/etc/systemd/system/crypto-run.service` equals the repository file. Two runtime drop-ins follow it under
  `/run/systemd/system.control/crypto-run.service.d/`: `50-MemoryMax.conf` (`MemoryMax=318767104`) and
  `50-MemorySwapMax.conf` (`MemorySwapMax=385875968`). These are the «last run's own limits» the TZ cites from TZ-72's
  A0; they decide nothing here.
- `readlink -f /usr/bin/claude` → `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`, an ELF x86-64
  executable.

The tools, cut from `origin/main`:

```
$ install -d -m 0755 /var/tmp/tz73-tools
[exit 0]
$ git show origin/main:CryptoTZ/TZ-73-run-login-remint.md | awk '/^````python$/{f=1;next} /^````$/{f=0} f' > /var/tmp/tz73-tools/tz73-login.py
$ git show origin/main:CryptoTZ/TZ-73-run-login-remint.md | awk '/^````pycheck$/{f=1;next} /^````$/{f=0} f' > /var/tmp/tz73-tools/tz73-controls.py
$ md5sum /var/tmp/tz73-tools/tz73-login.py /var/tmp/tz73-tools/tz73-controls.py
fc2b1e506d954ad0700f81e8fcf1edfa  /var/tmp/tz73-tools/tz73-login.py
26d66cd5e76cb2f8b317751ef01b9bd3  /var/tmp/tz73-tools/tz73-controls.py
$ wc -l ...
  85 /var/tmp/tz73-tools/tz73-login.py
 118 /var/tmp/tz73-tools/tz73-controls.py
```

Both equal §10's and §11's MD5 and line count.

### A1 — the refusal, re-read

```
$ install -d -m 0700 -o cryptorun -g cryptorun /var/tmp/tz73-home
[exit 0]
$ stat -c '%a %U %G %n' /var/tmp/tz73-home
700 cryptorun cryptorun /var/tmp/tz73-home
$ systemd-run --wait --pipe --collect --quiet --unit=tz73-probe-1 \
    -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/tmp/tz73-home \
    -p Environment=HOME=/var/tmp/tz73-home -p Environment=DISABLE_AUTOUPDATER=1 \
    -p Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 -p Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
    -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
    -p MemoryMax=167772160 -p MemorySwapMax=536870912 -p RuntimeMaxSec=180 \
    -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
    /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /usr/bin/claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model claude-haiku-4-5-20251001' \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), d.get("api_error_status"), sorted((d.get("modelUsage") or {}).keys()), len(d.get("permission_denials") or []), repr(str(d.get("result"))[:80]))'
True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token has been revoked.'
$ echo "exit=${PIPESTATUS[0]} ${PIPESTATUS[1]}"
exit=1 0
$ date -u
2026-10-25T07:31:06Z
```

The command was run under `bash`, character for character as §7 gives it, with `<n>` = 1. The line starts `True` and its
`api_error_status` is `401`, which is row 2 of §7's table. The result text also contains `revoked`. **The server refuses
the old login on the program the run executes today (2.1.282).** This is the measurement TZ-72's report said it had not
made.

### B — the new login

```
$ install -d -m 0700 /root/tz73-token
[exit 0]
$ tmux new-session -d -x 1000 -y 50 -s tz73-token "script -q -f -c '/usr/bin/claude setup-token' /root/tz73-token/out"
[exit 0]
$ for i in $(seq 1 15); do python3 -I /var/tmp/tz73-tools/tz73-login.py url /root/tz73-token/out && break; sleep 2; done
urls_found=0 has_state=no
urls_found=1 has_state=yes
<the URL on stdout — posted to the Boss, not reproduced here>
```

- **B2.** The Boss received §7 B2's post verbatim, with the URL alone on the line after it, and nothing else. The URL's
  host was `claude.com`, and its `state=` parameter was present.
- **B3.** One code came back. It is a long string whose part after `#` equals the URL's `state`, and it is not reproduced
  here. It was sent once:

  ```
  $ tmux has-session -t tz73-token
  [exit 0]
  $ tmux send-keys -t tz73-token -l '<code>'
  [exit 0]
  $ tmux send-keys -t tz73-token Enter
  [exit 0]
  $ for i in $(seq 1 30); do tmux has-session -t tz73-token 2>/dev/null || break; sleep 2; done
  (left at i=2: the session had ended about four seconds after Enter)
  ```

  The tool ended by itself, so the 60-second `screen` reading and the «Invalid code» path did not arise. One code went to
  one session.
- **B4.**

  ```
  $ python3 -I /var/tmp/tz73-tools/tz73-login.py take /root/tz73-token/out /etc/crypto-auto/credentials/claude-oauth-token
  length=113 matched=yes
  [exit 0]
  ```

  `113` is within 100–130, so `take` replaced the file in one rename. **The old file is gone.** The server had refused
  it, which is the reason B ran.
- **B5.**

  ```
  $ tmux kill-session -t tz73-token
  can't find session: tz73-token
  [exit 1]
  $ shred -u /root/tz73-token/out
  [exit 0]
  $ rmdir /root/tz73-token
  [exit 0]
  ```

  The first line is the tool having already ended (TZ-55's report, C4) and is recorded as it is.

The helper's `screen` was never run. No B step called for it: the URL came within the 30-second bound, the session ended
by itself, and `take` matched.

### C1 — the file

```
$ stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
600 root root 113 2026-10-25 07:33:14.587401244 +0000 /etc/crypto-auto/credentials/claude-oauth-token
$ python3 -I -c 'd=open("/etc/crypto-auto/credentials/claude-oauth-token","rb").read(); print("length=%d newline_bytes=%d non_empty_lines=%d prefix_ok=%d" % (len(d), d.count(b"\n"), len([l for l in d.split(b"\n") if l]), d.startswith(b"sk-ant-oat01-")))'
length=113 newline_bytes=0 non_empty_lines=1 prefix_ok=1
```

The login's birth is **2026-10-25 07:33:14 UTC**. The size equals `take`'s length. No `claude-oauth-token.new` is left in
the directory (a `grep -c` over its listing printed `0`).

### C2 — the probe on the new login

Probe 2 is A1's command with `<n>` = 2, character for character otherwise:

```
True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token is invalid.'
exit=1 0
$ date -u
2026-10-25T07:33:40Z
```

Probe 3 ran at 07:34:29, the same command with `<n>` = 3, as C2 permits («read once more thirty seconds later under the
number after»):

```
True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token is invalid.'
exit=1 0
$ date -u
2026-10-25T07:34:33Z
```

Both lines start `True` with `401`, so C2 fails and the TZ is BLOCKED (§7 C2).

### C3 — the scan

Run from the worktree, with the report drafted with every heading (D-1: `/usr/bin/grep`; `$HOME` is `/root`):

```
$ /usr/bin/grep -c . /etc/crypto-auto/credentials/claude-oauth-token
1
$ /usr/bin/grep -c '^$' /etc/crypto-auto/credentials/claude-oauth-token
0
$ install -d -m 0700 /var/tmp/tz73-tools/scan/dir
$ printf '%s\n' "dummy-$RANDOM-$RANDOM-$RANDOM" > /var/tmp/tz73-tools/scan/pattern
$ cp /var/tmp/tz73-tools/scan/pattern /var/tmp/tz73-tools/scan/dir/holds
$ printf 'nothing here\n' > /var/tmp/tz73-tools/scan/dir/lacks
$ /usr/bin/grep -rlF -f /var/tmp/tz73-tools/scan/pattern /var/tmp/tz73-tools/scan/dir | wc -l
1
$ /usr/bin/grep -rlF -f /etc/crypto-auto/credentials/claude-oauth-token /var/tmp/tz73-home /var/tmp/tz73-tools "$HOME/.claude" CryptoReports/TZ-73-run-login-remint-report.md | wc -l
0
```

`1`, `0`, `1`, `0`: the known answers.

**The TZ's scan searches for the file's value, and here that value is the login with `Store` glued on.** A copy of the
bare 108-character login would not contain the glued string, so this scan cannot find it. So the scan ran a second
time:
- **Pattern:** the file's first 108 bytes, fed through a pipe (`-f <(head -c 108 …)`), so no file holds the pattern.
  `head -c 108 … | wc -c` printed `108`.
- **Paths:** the TZ's paths and more:
  - the TZ's: `/var/tmp/tz73-home`, `/var/tmp/tz73-tools` and `/root/.claude` with this session's transcripts;
  - added: `/root/.claude.json` (the config `claude setup-token` runs against as root), `/root/.config`, `/root/.cache`,
    the session's scratch `/tmp/claude-0`, this whole worktree, the report included, and `/root/.bash_history`;
  - `/root/.local/state` was named but is absent;
  - the seven files under `/var/log` modified since 07:20 UTC: `syslog`, `wtmp`, `btmp`, `auth.log`, `sysstat/sa25`,
    `nginx/access.log` and the system journal.
- **Proof:** the same pipe form with the dummy's first 15 bytes found `1` file in the scan directory.

```
proof of the prefix form (dummy): 1
prefix length fed: 108
<hits for the 108-character prefix over all of the above>: 0
```

No hit, so contract §7 item 6's revocation clause is not triggered.

### D and V8

```
$ rm -rf /var/tmp/tz73-home /var/tmp/tz73-tools
$ ls -d /var/tmp/tz73-home /var/tmp/tz73-tools; echo "ls exit=$?"
ls: cannot access '/var/tmp/tz73-home': No such file or directory
ls: cannot access '/var/tmp/tz73-tools': No such file or directory
ls exit=2
$ tmux has-session -t tz73-token; echo "tmux exit=$?"
can't find session: tz73-token
tmux exit=1
$ ls -d /root/tz73-token /var/tmp/tz73-home /var/tmp/tz73-tools; echo "ls exit=$?"
ls: cannot access '/root/tz73-token': No such file or directory
ls: cannot access '/var/tmp/tz73-home': No such file or directory
ls: cannot access '/var/tmp/tz73-tools': No such file or directory
ls exit=2
$ systemctl list-units --all --no-legend 'tz73-probe-*' | wc -l
0
$ ps -eo args | awk '($1 ~ /claude$/ && $2 == "setup-token") || ($1 ~ /node$/ && $2 ~ /claude$/ && $3 == "setup-token") {n++} END {print n+0}'
0
```

Beside V8: `ps -eo args | /usr/bin/grep -c '[s]etup-token'` printed `0`, and `systemctl list-units --all --no-legend
'tz73-*' | wc -l` printed `0`. The three probe units were `--collect`ed.

### Why C2 refused the new login

1. **The wording changed.** A1, on the old file, reads «has been revoked». C2, on the new file, reads «is invalid». The
   server does not reject the new value as a revoked login. It rejects it as not being one.
2. **The length is five over the known length.** TZ-55's mint read `length=108 matched=yes` and a 108-byte file. That
   was at 1000 columns too, with its own script (TZ-55's report, C4). The old file was 109 bytes. This `take` read 113.
3. **The CLI's next line.** A read-only search of the installed bundle
   (`grep -aoE '.{0,200}(Store this token securely|valid for 1 year|CLAUDE_CODE_OAUTH_TOKEN=).{0,300}'` over
   `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`) returns «Store this token securely. You won't be
   able to see it again.» as the success screen's text. It also returns «Use this token by setting: export
   CLAUDE_CODE_OAUTH_TOKEN=<token>», with a literal placeholder. That explains why `take` found exactly one distinct
   match.
4. **Two counts on the file**, each printing a number and no part of the value:

   ```
   $ /usr/bin/grep -c 'Store$' /etc/crypto-auto/credentials/claude-oauth-token
   1
   $ /usr/bin/grep -cE '^sk-ant-oat01-[A-Za-z0-9_-]{95}Store$' /etc/crypto-auto/credentials/claude-oauth-token
   1
   ```

   The file is a 108-character `sk-ant-oat01-` string (13 + 95) followed by `Store`.
5. **The mechanism, in the helper's text.** `plain()` removes every CSI, OSC and two-byte escape and every `\r`, and only
   then does `TOKEN.findall` run. CLI 2.1.282 draws its screen with cursor-movement sequences. After the token it moves
   down to the next line rather than writing `\n`, so the sequence's removal leaves the token directly followed by
   `Store this token securely.`. `[A-Za-z0-9_-]+` then extends through `Store` and stops at the space. TZ-55's script
   took 108, so it did not strip before matching in this way, or the screen then was different. Its source is not in
   the repository.
6. **Why V1 passed.** Every fake typescript in §11 separates the token from the next text with `\r\n` (`t-tok`:
   `TOK108 + ESC[0m + \r\nStore this token securely.`). `\r` is removed and `\n` stays, so the match ends at `\n`. No
   control plants a token followed by a cursor movement and a word. The 15 checks and the four mutations measured the
   helper against a screen the CLI does not draw.

So the refusal is not evidence about the credential class. TZ §3's sentence «If the new login is refused at its first
probe … the credential class is the defect» is met in its letter by C2. The measured cause is the file's value, not a
login the server refused. That reading is the Architect's to make. This report states the two facts and makes no
choice between them.

## Validation

- **V1** — PASS. In A0, before A1:

  ```
  $ python3 -I /var/tmp/tz73-tools/tz73-controls.py /var/tmp/tz73-tools/tz73-login.py /var/tmp/tz73-tools/ctl
  PASS url: one whole URL printed, exit 0
  PASS url: two distinct URLs refused
  PASS url: URL without state refused
  PASS url: no URL refused
  PASS take: token twice with colour codes and CRLF is placed
  PASS take: mode 0600, no newline, no .new left
  PASS take: the token is in neither stdout nor stderr
  PASS take: a 109-character token is placed where no target existed
  PASS take: no token is refused and the target is untouched
  PASS take: two different tokens is refused and the target is untouched
  PASS take: a short token is refused and the target is untouched
  PASS take: a token wrapped at 80 columns is refused and the target is untouched
  PASS screen: the token is masked and the words stay
  PASS screen: the URL is masked
  PASS screen: no run of 32 characters survives
  controls: 15 checks, 0 failed
  controls exit=0
  ```

  The four mutations, by §8 V1's loop verbatim:

  ```
  mutation 1: exit=1 controls: 15 checks, 2 failed
  mutation 2: exit=1 controls: 15 checks, 1 failed
  mutation 3: exit=1 controls: 15 checks, 1 failed
  mutation 4: exit=1 controls: 15 checks, 1 failed
  ```

  No `UNCHANGED` line was printed. The failing checks, read from each `mut-<k>.out`:
  - m1: «a short token is refused», «a token wrapped at 80 columns is refused».
  - m2: «two different tokens is refused».
  - m3: «mode 0600, no newline, no .new left».
  - m4: «URL without state refused».

  All equal the known answers. (V1 passed and the helper is still defective in a case the controls do not plant: see
  `### Why C2 refused the new login`, item 6.)
- **V2** — PASS. A0's readings above; the gate under `## Fingerprints`; the clone clean (`git status --porcelain`
  empty).
- **V3** — PASS as a reading. The command as run, the line, `exit=1 0`, row 2 of §7's table (`### A1`).
- **V4** — PASS. `urls_found=1 has_state=yes`; `length=113 matched=yes` (100 ≤ 113 ≤ 130); B5's three lines and exit
  codes (1, 0, 0). The code is not reproduced.
- **V5** — PASS by its letter: `600 root root 113 … /etc/crypto-auto/credentials/claude-oauth-token`, `113` = `take`'s
  length, `length=113 newline_bytes=0 non_empty_lines=1 prefix_ok=1`. The value is still not a login (`### Why C2
  refused the new login`).
- **V6** — **FAIL.** Both C2 lines start `True` with `401`, `exit=1` for `systemd-run`.
- **V7** — PASS. C3's four lines `1`, `0`, `1`, `0` (`### C3`).
- **V8** — PASS. `tmux exit=1`; `ls exit=2` with three «No such file or directory» lines; `0` units; `0` processes
  (`### D and V8`).
- **V9** — PASS as far as a record can read it. `git status --porcelain` prints one line,
  `?? CryptoReports/TZ-73-run-login-remint-report.md`, so the report is the tree's only change. The report's own commit
  is stated under `## Commit`. Its `git show --stat` is that commit's outcome, which this record cannot contain (inv. 54).

## Test Results

No repository test was in scope: the TZ changes no repository file, and no bench or selftest was run. The tests of
this TZ are V1–V9 above. V1–V5 and V7–V9 passed. **V6 failed**, and it decides the status.

## Deviations

- **D-1. `/usr/bin/grep` stands where the TZ writes `grep`.** In this session's shell `grep` is a function that passes
  its arguments to the session's own Claude Code binary (A0, third reading). §7's known answers (`grep -c` exiting 1 on
  a count of 0, `-rlF -f`) are GNU grep's, so every host `grep` of A0's gate, C1, C3 and the diagnosis was run as
  `/usr/bin/grep`. The one exception is A0's second reading, run as written, which printed the TZ's two lines.
- **D-2. Readings outside §7's list, none of them a write or a probe.**
  - `systemctl cat crypto-run.service` compared with the repository unit, and `systemctl show -p FragmentPath`.
  - `readlink -f` and `file -L` on `/usr/bin/claude`, and one string search of the installed bundle (§4: the npm
    install is «run and read»).
  - Two `grep -c` counts on the credential file. §1 admits counts (`grep -c`) as a reading of it, and each printed one
    digit.
  - The C3 scan run a second time with a stricter pattern and wider paths (`### C3`).

  They were made so that the BLOCKED carries its measured cause rather than a guess.
- **D-3. The tools were cut from the TZ by `git show origin/main:…` in this worktree**, which was at `origin/main`
  (`f82921f`). This is the command as §7 gives it, run from the worktree rather than from `/srv/crypto-auto`.

## Pre-existing Issues

- **The helper of TZ §10 glues the CLI's next line onto the token**, and §11's controls do not plant the screen that
  shows it (`### Why C2 refused the new login`). This is a defect of the TZ's own code, not of the repository. It is
  reported, and it was not edited: §6 forbids running a helper that differs from §10 by a byte.
- In this session's shell `grep` is a function wrapping the session's CLI (D-1). A TZ command that relies on GNU grep's
  exit codes reads otherwise in such a session.

## Remaining Risks

- **The run is still down.** `/etc/crypto-auto/credentials/claude-oauth-token` holds a value the server calls invalid,
  so every production run still ends «Анализ не завершён.», as it did on the revoked login. Nothing changed for the
  Boss but the cause.
- **The value in the file is the probable login with five extra bytes.** The 108-character string was minted at
  07:33:14 UTC, was never displayed, and exists nowhere else: the typescript is shredded. Whether the server accepts it
  is unmeasured. Until a TZ cuts the file or mints again, a live one-year credential may be sitting in that file.
- **The cause of the earlier revocations is unmeasured** (TZ §3, §2), and a working login may be refused again. The
  journal's next 401 against the file's modified time is the reading.
- Production runs go on the host's 2.1.282 until TZ-72's merge.
- The code the Boss returned sits in the conversation that carried it. It is single-use and was consumed at 07:33.
- The probes measured the host's CLI. TZ-72's A3 measures the pinned file under the same limits.
- The old login is not recoverable. It was replaced by `take` in B4, and the server had refused it as revoked (A1).

## Commit

Report, on `main`, message as `## Commit Message` gives it:

```
TZ-73: report — the run's Claude login re-read on the host and, where the server refused it, minted again and probed once
```

Contents: `CryptoReports/TZ-73-run-login-remint-report.md`, and nothing else.

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

## CI Execution

No branch exists and no workflow ran for this TZ. The report's path clears every push trigger. `main.yml` is a `paths`
allow-list of `main.py` and `.github/workflows/main.yml`, read before the push. `bench.yml` ignores `**.md`. `calib.yml`
triggers on `claude/**` only. `journal.yml` and `backtest_bench.yml` have no push trigger.

## Final Repository State

The checkout the fingerprints were taken against: this worktree (branch
`worktree-bridge-cse_01JQoRYMr6xjFKA7MgTZewaQ`) at `f82921f8d4c958af92f6fe2d0071fb010ee13b95`, equal to `origin/main`
at the last fetch. Its only change is this report, untracked (`git status --porcelain` above).

The host:
- No `tz73-*` unit, no tmux session `tz73-token`, no `setup-token` process, and none of `/root/tz73-token`,
  `/var/tmp/tz73-home` or `/var/tmp/tz73-tools` (V8).
- Nothing was installed, enabled, started, stopped or restarted. No run was started or requested, and nothing was sent
  to Telegram.
- The credential file, the one path under `/etc/crypto-auto/` this session wrote, with no `.new` beside it:

```
600 root root 113 2026-10-25 07:33:14.587401244 +0000 /etc/crypto-auto/credentials/claude-oauth-token
```

It holds the value C2 found invalid (`## Status`).

## Fingerprints

Taken against `origin/main` at `f82921f8d4c958af92f6fe2d0071fb010ee13b95`, which is also this worktree's checkout.

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — 2797 lines, MD5 `ba303ec6a08414d3bd8e041d15086719`, revision string
`**Revision 2026-10-25-a.**` (map line 17). This equals the TZ header.

**Anchors.** The map's anchor table was cut by structure: every row between the separator after `| Anchor |` and the
first non-table line, inside `## 0. Fingerprint`.

```
awk '/^## 0\. Fingerprint/{z=1} z&&/^\| Anchor \|/{h=1;next} h&&/^\|---/{r=1;next} r&&/^\|/{print;next} r{exit}'
```

The same cut was applied to the TZ's `## 0. Fingerprint required`. **The map's table has 7 rows, the TZ's has 7, and the
two cuts are byte-identical (`cmp` exit 0). 7 anchors were compared.** Per anchor:
`/usr/bin/grep -oF -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md` (from `git show origin/main:`), the first line it returned,
and its `-c` count:

| # | Anchor | Text the match returned | count |
|---:|---|---|---:|
| 1 | revision | `**Revision 2026-10-25-a.**` | 2 |
| 2 | direction engine | `### 3.12 Direction engine — veto cascade` | 2 |
| 3 | catalyst registry | `### 3.15 Catalyst registry` | 2 |
| 4 | exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | 2 |
| 5 | analytical engine | `## 11. Analytical engine` | 2 |
| 6 | squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 |
| 7 | newest invariant | `72. **A write that fails leaves this run's product or nothing` | 2 |

Each count is 2: once in the table row and once in the map's body.

**Files** (from `git show origin/main:<path> | wc -l` and `| md5sum`):

| File | Lines | MD5 | Required | Result |
|---|---:|---|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | 3799 / `4e71da9b…` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 / `0e3ead8c…` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a…` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b2…` | equal |
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | `**Version 31.**` (line 3) | equal; version 31 |
| `vps/units/crypto-run.service` | 38 | `9355ee94131624ff3fcdafe409183f38` | 38 / `9355ee94…`, enforced | equal |

No file differs, so nothing goes under `## Pre-existing Issues` from the fingerprints.
