# TZ-73 — The run's Claude login: the refusal re-read, a new login minted where the server refuses the old one, and one probe on it

**Canonical filename:** `CryptoTZ/TZ-73-run-login-remint.md`
**Report:** `CryptoReports/TZ-73-run-login-remint-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine**, because the run's login lives on it and is minted on it.
**Class:** report-only TZ (contract §8) — it authorises exactly one written repository file, its own report. Its
`## Scope` names no other repository file; the host paths of §4 are outside the repository, as TZ-61's were. **No branch
and no pull request exist for it:** a branch carries repository files and nothing else, and the login cannot travel
through git.
**Model:** Opus
**Trigger:** `EXECUTE TZ-73`, with nothing under it: no credential arrives (§1). Where A1 reads a 401, B asks the Boss
for one approval in his own browser and one code, and the session waits for them.
**Previous TZ:** TZ-72, BLOCKED at A3 on 25.10.2026; its report is on `main`. It opened no branch and no pull request, so
nothing of it awaits a merge, and it re-runs after this TZ (§3).
**Issued:** 25.10.2026, by the Architect.
**Written against:** contract v31, map `2026-10-25-a` as it stands on `main` — this TZ moves no map revision, so that TZ-72
re-runs against the same one (§3) — and `main` at `4f89440`, read by the Architect from the repository on 25.10.2026,
TZ-72's report included.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-25-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-25-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this TZ's gate adds:

| Added file | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | its version line reads `**Version 31.**` — a lower version is BLOCKED; lines and MD5 reported |
| `vps/units/crypto-run.service` | 38 | `9355ee94131624ff3fcdafe409183f38` | equal, or A0 stops: A0's reading of its `LoadCredential=` line is written against these bytes |

The map itself: 2797 lines, MD5 `ba303ec6a08414d3bd8e041d15086719` — reported, not enforced.

---

## 1. Credentials

**None arrives.** The new login is minted on the VPS by `claude setup-token` while the Boss approves in his own browser;
the code he passes back is single-use and sits only in the conversation that carried it (contract §7 item 6). The token
goes from the command's typescript to its file through the helper of §10, in one rename, and is never displayed.

**No command in this session prints the typescript, the tmux pane, the old credential file or the new one.** The only
readings of those are counts (`grep -c`, `grep -rl … | wc -l`), file metadata (`stat`) and the helper's own lines. The
helper's `screen` prints the typescript with every run of 32 or more characters masked, and is the only way the
typescript's text is read. No value is printed, logged, committed or quoted — in the report, a commit, a check's label
or the chat — and no other credential is read: neither the deploy key, nor the bot's token, nor the Binance key, nor the
SoSoValue key. Nothing is sent to Telegram.

---

## 2. Contract, map and outside text this TZ obeys

Contract §7 item 6:

> **A unit that runs a model session runs as its own unprivileged user, never root, and holds exactly two credentials: its own Claude login and the deploy key** (since v25)

— A1 and C2 run their probes as `cryptorun`, the run unit's own user, never as root, and hand the login to the CLI the
unit's own way (`LoadCredential=`, read inside the unit into the environment of the CLI child alone).

> **The Claude login never travels at all:** `claude setup-token` mints it on the VPS while the Boss approves in his own browser, the code he passes back is single-use, and the token goes from the command's output to its file without being displayed.

— B is that mint, on the VPS, with the Boss's approval in his own browser.

> **No value is ever printed, logged, committed or quoted** — in a report, a day log, a commit, a unit file or the chat.

> A value that appears anywhere else is revoked and replaced, never cleaned up

> The conversation that carried it is the one other copy

> a report proves every value absent from everything the session wrote by searching for the value itself

— C3 is that search, run against everything this session wrote; a value found where it should not be is revoked and
replaced by a new mint, and the report says so.

Contract §7 item 15:

> it may start TRANSIENT units from its branch for a measurement its TZ names, and its report proves none is left behind

— A1 and C2 start transient units for a measurement this TZ names, and V8 proves none is left behind.

Contract §8, the class:

> A **report-only TZ** authorises exactly one written file — its own report — on the `CryptoReports/**` direct-push path.

— the credential file is on the host, outside the repository, and a pull request cannot carry it; §4 authorises it by
name under `### On the VPS, outside the repository`, the heading TZ-61's scope used for its scratch directory, and the
class is read off the three repository lists, all of which are `None`. The report's `## Pull Request` carries the
contract §10 line:

> `None — report-only TZ; direct push on the CryptoReports/** path (§8).`

Contract §12, blocked tasks:

> Report BLOCKED with the precise obstacle and what would unblock it.

TZ-55 §12.8 (C4), the procedure this TZ repeats with three changes (§3):

> The owner opens it, approves, and sends back the code shown. The session sends it with `tmux send-keys -t tz55-token -l '<code>'` and then `Enter`. The code is single-use.

> A script reads the file, takes the token by the pattern `sk-ant-oat01-[A-Za-z0-9_-]+`, writes it to `/etc/crypto-auto/credentials/claude-oauth-token` (`0600 root:root`, no newline) and prints only `length=<n> matched=<yes|no>`.

**TZ-72's report** (`CryptoReports/TZ-72-run-cli-and-models-report.md`, on `main` at `4f89440`), which this TZ acts on:

> All four probes printed `True success [] 0 0`. The run's own Claude login was refused before any model ran.

> Each probe's transcript carries the same synthetic message: `error=authentication_failed`, «Failed to authenticate: OAuth token revoked. Please log in again or contact your administrator.»

The login file, read by that report with `stat` and nothing else:

> `109 bytes, mode 600, owner root, modified 2026-10-24 07:58:12.696914869 +0000`

> **I did not measure whether 2.1.282 is refused with this login today.**

— A1 is that reading, on the program the run executes today.

**The Architect's readings of 25.10.2026**, none of them the host's. In `anthropics/claude-code`: issue 29497 reports an
interactive login revoked at once after a fresh `/login` («OAuth token revoked», version 2.1.62); issue 57320 reports a
`claude setup-token` token that stays active after it is deleted in the web settings (closed as a duplicate); issue
52202 asks the documentation to explain the server revoking a token before its local expiry and lists server-side
revocation, clock skew and stale cached credentials as possibilities. None states a cause of a `setup-token` login being
refused early. The cause is therefore not read here and not guessed.

---

## 3. What is done, and why

**What happened.** TZ-72 ran on 25.10.2026 and stopped BLOCKED at A3: its four probes ended `True success [] 0 0` on the
pinned CLI, the CLI itself wrote the refusal («OAuth token revoked»), and no model answered. The production journal,
which that report read, shows the run's login refused with 401 on 21.10.2026 at 12:04 and on 24.10.2026 at 07:34, each
followed by a run that succeeded, sixteen and twenty-four minutes later — the second after the login file was replaced at
07:58:12. That is two logins and three refusals in five days: the first, minted on 02.10.2026 by TZ-55 and labelled
«1-year» by `claude setup-token`, was refused 19 and 22 days after its minting; the second, minted on 24.10.2026,
answered at 07:58 and 14:16 and was refused at about 06:08 UTC on 25.10.2026, less than a day old.

**What it means.** The refusal is not TZ-72's fault: the Architect's audit of 25.10.2026 applied its patch to `main`
(`git apply --check` exit 0) and ran the selftest, which reads `sections 27 checks 560 failed 0 empty 0` with the patch and
`sections 26 checks 534 failed 0 empty 0` without it. The CLI writes the error before any model answers, and
`crypto-run.service` hands the same file to the host's `/usr/bin/claude`, so **while the server refuses that file every
run ends in the notice «Анализ не завершён.»** — before TZ-72 and after it, and no merge repairs that. TZ-72's report did
not measure whether the host's CLI is refused today (its `### What the probes read`); A1 is that measurement.

**What this TZ does.**
- **A** reads the refusal again, with one probe on the program the run executes today (2.1.282). A refusal that has gone
  needs no new login, and one that is not the server's 401 is not repaired by one.
- **B**, only where A1 reads a 401, mints a new login by TZ-55's C4 with three changes: the terminal is 1000 columns
  wide, because at 80 the authorization URL wraps and cannot be read whole (TZ-55's report, D-3); the typescript is
  handled by one helper that never prints a token (§10), where TZ-55's script was written in the session; and the post
  the Boss receives names the code he must return — a long string with `#`, not a six-digit number, which is what
  TZ-55's first attempt sent.
- **C** proves the new file well formed and answering, on the same probe, and the token absent from every file the
  session touched.
- **D** removes everything the session made.

TZ-72 then re-runs unchanged — `EXECUTE TZ-72`, which writes `-report-2` (contract §13) — against the same map revision,
which this TZ leaves where it is for that reason.

**What this TZ cannot decide.** Why the server revoked the login (§2). It restores the run for as long as the new login
lasts, and the report records the new file's modified time to the second (C1), so that the journal's next 401 dates its
life — the second login lasted under a day. **If the new login is refused at its first probe, or again within days, the
credential class is the defect: the run moves to an API key — a contract revision and the Architect's, never a third
mint by TZ.**

---

## 4. Scope

### Files to Modify

None.

### Files to Create

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- `/var/tmp/tz73-tools/` — the helper and the controls cut from §10 and §11, and the controls' scratch; made in A0,
  removed in D.
- `/var/tmp/tz73-home/` — the probes' scratch home (`0700`, `cryptorun`); made in A1, removed in D. No probe touches the
  run's own home, `/var/lib/cryptorun`.
- Transient units `tz73-probe-1` to `tz73-probe-4`, numbered in the order the probes run, at most four (§7: A1 one or
  two, C2 one or two) — each collected when it exits.
- **Only where A1 reads a 401:** `/root/tz73-token/` (`0700`), the tmux session `tz73-token`, and **one** replacement of
  `/etc/crypto-auto/credentials/claude-oauth-token`, by the helper's `take`, in one rename. That file is the only path
  under `/etc/crypto-auto/` this session writes.
- Reading, never writing: `systemctl cat crypto-run.service`; `stat` of the credential file; `/usr/bin/claude --version`.

**Nothing is installed, enabled, disabled, started, stopped or restarted: `/usr/bin/claude` and the npm global install
behind it are run and read, never changed; no persistent unit is touched; no run is started or requested; and nothing
under `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or `/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- No file of the repository is changed: not `vps/**`, not a unit, not the deployer, not the map or the contract. TZ-72's
  patch and stages are not touched, and no probe is made on the pinned CLI — that is TZ-72's A3.
- No other login, key or token is minted, read or replaced. An API key for the run is a contract revision (§3) and is not
  built here.
- The old login is not revoked: no command does that, and the server has already refused it.
- No message is sent to Telegram, and nothing is scheduled.
- No other version, model id or probe than §7's.

---

## 6. Rules — binding in every stage

- **The helper is the only program that touches the token** (§1, §10). It is cut from this file and its MD5 compared
  before its first use (A0, V1); a helper that differs by a byte is not run.
- **The old file is replaced only by `take`, in one rename**, and `take` replaces it only for exactly one distinct token
  of 100 to 130 characters. Where `take` prints `matched=no` the old file is untouched, and the report says so.
- **A refusal by the session's permission mode is not a blocker of this TZ and is not worked around:** report the command
  and the label at once, in the session, and continue when the Boss has changed the mode there (TZ-55's report, D-2: the
  classifier refused `setup-token`, labelled «Unauthorized Persistence», and the owner took the session out of automatic
  mode).
- **The Boss is addressed in chat only by the posts quoted in B**, and by nothing else; no technical question is put to
  him.
- **No probe but §7's is made:** A1 once, or twice where its table says so, and C2 once, or twice where C2 says so — four
  at most. The report carries every printed line and every `exit=` line.
- **Nothing persistent.** The report proves every unit, session, directory and process gone (V8).
- **A control that changes nothing, or leaves its harness green, fails its item** (contract §9).

---

## 7. Stages

- **A0. The host and the baseline — readings; the only write is the tools directory.**

  ```sh
  id -un
  systemctl cat crypto-run.service | grep -nE "^(User=|LoadCredential=claude-oauth-token:)"
  command -v tmux script python3 shred systemd-run grep pgrep stat install cmp awk sed md5sum ps
  stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
  /usr/bin/claude --version
  git fetch --all --prune
  git rev-parse --is-shallow-repository
  git status --porcelain
  ```

  The first prints `root` — the login file is replaced by root alone; the second prints `User=cryptorun` and
  `LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token` (with `systemctl cat`'s own line
  numbers; TZ-72's A0 read them at 11 and 22); the third prints fourteen paths — any missing → BLOCKED; the fourth prints
  `600 root root <n> <modified> <path>` — TZ-72's report read 109 bytes, mode 600, owner root and a modified time of
  24.10.2026 07:58:12, and another value is reported and decides nothing by itself; the fifth prints
  `2.1.282 (Claude Code)`, and another value is reported — A1 decides; the sixth fetches and the seventh prints `false`
  (else `git fetch --unshallow`, contract §3); the eighth prints nothing. Contract §5's gate runs against
  `origin/main` and §0: per anchor the command and the text the match returned, and the table's row count beside the
  number compared. **Any of the first, second or third reading not so, or a gate that fails → BLOCKED.** Then the tools,
  cut from the TZ as `origin/main` holds it:

  ```sh
  install -d -m 0755 /var/tmp/tz73-tools
  git show origin/main:CryptoTZ/TZ-73-run-login-remint.md | awk '/^````python$/{f=1;next} /^````$/{f=0} f' > /var/tmp/tz73-tools/tz73-login.py
  git show origin/main:CryptoTZ/TZ-73-run-login-remint.md | awk '/^````pycheck$/{f=1;next} /^````$/{f=0} f' > /var/tmp/tz73-tools/tz73-controls.py
  md5sum /var/tmp/tz73-tools/tz73-login.py /var/tmp/tz73-tools/tz73-controls.py
  ```

  The two MD5s equal §10's and §11's, or STOP, BLOCKED. **V1 runs here, before A1:** a helper that fails its controls
  stops the TZ before anything else is touched.

- **A1. The refusal, re-read.**

  ```sh
  install -d -m 0700 -o cryptorun -g cryptorun /var/tmp/tz73-home
  ```

  then the probe, n = 1 (n numbers the session's probes in the order they run) — the host's CLI, which is what
  `crypto-run.service` executes today, on the login the unit hands it, with the unit file's own memory limits and a
  three-minute bound on the unit (`RuntimeMaxSec`: TZ-72's A3 set none, and its four probes each printed their line):

  ```sh
  systemd-run --wait --pipe --collect --quiet --unit=tz73-probe-<n> \
    -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/tmp/tz73-home \
    -p Environment=HOME=/var/tmp/tz73-home -p Environment=DISABLE_AUTOUPDATER=1 \
    -p Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 -p Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
    -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
    -p MemoryMax=167772160 -p MemorySwapMax=536870912 -p RuntimeMaxSec=180 \
    -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
    /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /usr/bin/claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model claude-haiku-4-5-20251001' \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), d.get("api_error_status"), sorted((d.get("modelUsage") or {}).keys()), len(d.get("permission_denials") or []), repr(str(d.get("result"))[:80]))'
  echo "exit=${PIPESTATUS[0]} ${PIPESTATUS[1]}"
  ```

  `bash` runs the block, and the `echo` stays directly under the pipeline: it prints the exit codes of `systemd-run` and of
  the summarizer. The line prints `<is_error> <subtype> <api_error_status> <models> <denials> <result, 80 characters>`,
  and the report carries the command as run, the line and the `exit=` line. *Derived: the form of TZ-72's A3 probe, which ran on this host
  and printed `True success [] 0 0` for a refused login; the model id is `HELPER_MODEL` in `vps/run.py`, and TZ-72's
  report reads it in the journal's `models=` field of the runs that answered on 21.10 and 24.10.* The line decides:

  | The line | Means | Then |
  |---|---|---|
  | starts `False`, its models list is not empty, `systemd-run` exits 0 | the login answers | **B and C1–C2 are skipped**; this line stands for C2; Status COMPLETED, and `## Implementation Summary` says nothing was minted. C3 and D still run. |
  | starts `True`, and `api_error_status` is `401`, or the result text contains `revoked`, `expired`, `authenticate`, `log in` or `/login` (any case) | the server refuses the login | B |
  | anything else — another status, a `False` with an empty models list, a traceback, exit 137 | not the refusal this TZ repairs | Where the exit is 137 or the line is empty, run the probe once more as the next n with `-p MemoryMax=318767104 -p MemorySwapMax=385875968` (the last run's own limits, read by TZ-72's A0) in place of the two memory properties, and carry both lines; where the result still reads this row → STOP, BLOCKED with the line. **No login is minted for a refusal that is not the server's 401.** |

- **B. The new login — only where A1 reads a 401.**
  - **B1.** The session:

    ```sh
    install -d -m 0700 /root/tz73-token
    tmux new-session -d -x 1000 -y 50 -s tz73-token "script -q -f -c '/usr/bin/claude setup-token' /root/tz73-token/out"
    ```

  - **B2.** The URL, read out whole:

    ```sh
    for i in $(seq 1 15); do python3 -I /var/tmp/tz73-tools/tz73-login.py url /root/tz73-token/out && break; sleep 2; done
    ```

    On success stdout is the URL and stderr reads `urls_found=1 has_state=yes`. No URL after thirty seconds → the helper's
    `screen` is printed once, B5, and BLOCKED. The Boss receives this post and nothing else, with the URL alone on the
    line after it; the report does not quote the URL:

    > Босс, нужен новый вход Claude для анализа: сервер отозвал старый. 1) Откройте ссылку ниже и подтвердите вход в своём аккаунте. 2) Страница покажет код — длинную строку со знаком #, не шестизначное число. 3) Пришлите мне этот код сюда целиком.

  - **B3.** When the code arrives (single-use; never reproduced in the report), it is sent and the tool is waited for:

    ```sh
    tmux has-session -t tz73-token
    tmux send-keys -t tz73-token -l '<code>'
    tmux send-keys -t tz73-token Enter
    for i in $(seq 1 30); do tmux has-session -t tz73-token 2>/dev/null || break; sleep 2; done
    ```

    A session still alive after sixty seconds is read once with the helper's `screen`. If it shows «Invalid code» and
    «Press Enter to retry» (TZ-55's screen), `tmux send-keys -t tz73-token Enter` brings the same URL back (compare it
    with `url`) and the Boss receives:

    > Код не принят. Нужна длинная строка со знаком #, которую страница показывает после подтверждения. Пришлите её ещё раз целиком.

    **At most two codes go to one session.** A session that ended with no token, or whose URL has gone stale, is cleaned
    by B5 and B1 runs once more; the Boss then receives, with the new URL alone on the next line:

    > Ссылка устарела. Вот новая — откройте её и пришлите новый код целиком.

    **At most two sessions in all**; a third need → BLOCKED.
  - **B4.** The helper places the login:

    ```sh
    python3 -I /var/tmp/tz73-tools/tz73-login.py take /root/tz73-token/out /etc/crypto-auto/credentials/claude-oauth-token
    ```

    It prints `length=<n> matched=yes`, `<n>` between 100 and 130, and exits 0 (TZ-55 read 108, and the file it replaces
    is 109 bytes). `matched=no` → the old file is untouched, the helper's `screen` is printed once, B5, BLOCKED.
  - **B5.** Whatever B1–B4 read:

    ```sh
    tmux kill-session -t tz73-token
    shred -u /root/tz73-token/out
    rmdir /root/tz73-token
    ```

    `kill-session` printing «can't find session: tz73-token» or «no server running» (exit 1) is the tool having already
    ended (TZ-55's report, C4) and is recorded as it is.

- **C. The proofs — where B ran.**
  - **C1.** The file, by metadata and counts only:

    ```sh
    stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
    python3 -I -c 'd=open("/etc/crypto-auto/credentials/claude-oauth-token","rb").read(); print("length=%d newline_bytes=%d non_empty_lines=%d prefix_ok=%d" % (len(d), d.count(b"\n"), len([l for l in d.split(b"\n") if l]), d.startswith(b"sk-ant-oat01-")))'
    ```

    The modified time is the login's birth and goes into the report to the second.
  - **C2.** The probe of A1, unchanged but for n (the next number), with the `exit=` line: it must print a line starting
    `False` with a models list that is not empty, `systemd-run` exit 0. A line starting `True` with `401` may be read once
    more thirty seconds later under the number after, and both lines are carried. **A login the server refuses within a
    minute of its minting is a finding, not noise → BLOCKED, with both lines.**
  - **C3.** The scan — the exact value against everything the session wrote or could have written; the report's draft
    exists by now, with its headings. First the scan is proven, then run:

    ```sh
    grep -c . /etc/crypto-auto/credentials/claude-oauth-token
    grep -c '^$' /etc/crypto-auto/credentials/claude-oauth-token
    install -d -m 0700 /var/tmp/tz73-tools/scan/dir
    printf '%s\n' "dummy-$RANDOM-$RANDOM-$RANDOM" > /var/tmp/tz73-tools/scan/pattern
    cp /var/tmp/tz73-tools/scan/pattern /var/tmp/tz73-tools/scan/dir/holds
    printf 'nothing here\n' > /var/tmp/tz73-tools/scan/dir/lacks
    grep -rlF -f /var/tmp/tz73-tools/scan/pattern /var/tmp/tz73-tools/scan/dir | wc -l
    grep -rlF -f /etc/crypto-auto/credentials/claude-oauth-token /var/tmp/tz73-home /var/tmp/tz73-tools "$HOME/.claude" CryptoReports/TZ-73-run-login-remint-report.md | wc -l
    ```

    Four lines are printed, `1`, `0`, `1`, `0`: the pattern file holds one line and no empty one, so it cannot match every
    line (`grep -c` exits 1 on a count of 0, which is the answer here); the dummy pattern finds the file that holds it and
    not the one that does not; and the value finds nothing in the report as drafted when this runs, the scratch home, the
    tools, or the Executor's own `.claude` with its transcripts. **A hit prints no value**: the file's name alone goes into
    the report, contract §7 item 6 applies — the login is revoked and replaced — and the Architect issues the replacement.

- **D. Clean-up, whatever A and B read.**

  ```sh
  rm -rf /var/tmp/tz73-home /var/tmp/tz73-tools
  ls -d /var/tmp/tz73-home /var/tmp/tz73-tools; echo "ls exit=$?"
  ```

  `ls exit=2`, with two «No such file or directory» lines.

---

## 8. Validation

Every item names its command and its known answer; each answer was derived where it says.

- **V1. The helper against planted fake tokens — in A0, before A1.**
  `python3 -I /var/tmp/tz73-tools/tz73-controls.py /var/tmp/tz73-tools/tz73-login.py /var/tmp/tz73-tools/ctl` → exit 0 and
  the last line `controls: 15 checks, 0 failed`. *Derived: the Architect's run of §11 on §10, 25.10.2026.* **Then four
  controls, each on a copy of the helper with one edit** — the loop below prints one line per control, and a control whose
  edit changed nothing prints `UNCHANGED` and fails the item:

  ```sh
  T=/var/tmp/tz73-tools
  for k in 1 2 3 4; do
    cp $T/tz73-login.py $T/mut.py
    case $k in
      1) sed -i 's/^LENGTH_MIN, LENGTH_MAX = 100, 130$/LENGTH_MIN, LENGTH_MAX = 0, 999/' $T/mut.py ;;
      2) sed -i 's/    if len(tokens) != 1 or not/    if len(tokens) < 1 or not/' $T/mut.py ;;
      3) sed -i 's/0o600/0o644/g' $T/mut.py ;;
      4) sed -i 's/    ok = len(found) == 1 and "state=" in found\[0\]$/    ok = len(found) == 1/' $T/mut.py ;;
    esac
    cmp -s $T/tz73-login.py $T/mut.py && echo "mutation $k: UNCHANGED"
    python3 -I $T/tz73-controls.py $T/mut.py $T/ctl-c$k > $T/mut-$k.out; rc=$?
    echo "mutation $k: exit=$rc $(tail -1 $T/mut-$k.out)"
    rm $T/mut.py
  done
  ```

  Known answers: `mutation 1: exit=1 controls: 15 checks, 2 failed`, and `exit=1 controls: 15 checks, 1 failed` for
  mutations 2, 3 and 4. *Derived: the Architect's run of the four edits on §10 and §11, 25.10.2026.* A harness that stays
  green under an edit, or an edit that changes nothing, fails this item.
- **V2. The baseline.** A0's readings and the gate of contract §5, with the clone clean.
- **V3. A1.** The command as run, the line, the `exit=` line, and the row of §7's table it fell in.
- **V4. The minting, where B ran.** The `url` line `urls_found=1 has_state=yes`; the `take` line
  `length=<n> matched=yes` with `<n>` from 100 to 130; B5's lines and exit codes. The code is not reproduced.
- **V5. The file, where B ran.** C1: `600 root root <n> <modified> /etc/crypto-auto/credentials/claude-oauth-token` with
  `<n>` equal to `take`'s length, and `length=<n> newline_bytes=0 non_empty_lines=1 prefix_ok=1`. *Derived: TZ-55's report
  C4 printed the same facts on 02.10.2026 (`600 root root 108`, then `newline_bytes=0`, `non_empty_lines=1`,
  `prefix_ok=1`); the length is read and not fixed, because the file it replaces is 109 bytes.*
- **V6. C2, where B ran.** A line starting `False` with a models list that is not empty, and `exit=0` for `systemd-run`.
- **V7. C3.** The four lines `1`, `0`, `1`, `0`.
- **V8. Nothing left behind.**

  ```sh
  tmux has-session -t tz73-token; echo "tmux exit=$?"
  ls -d /root/tz73-token /var/tmp/tz73-home /var/tmp/tz73-tools; echo "ls exit=$?"
  systemctl list-units --all --no-legend 'tz73-probe-*' | wc -l
  ps -eo args | awk '($1 ~ /claude$/ && $2 == "setup-token") || ($1 ~ /node$/ && $2 ~ /claude$/ && $3 == "setup-token") {n++} END {print n+0}'
  ```

  Known answers: `tmux exit=1`; `ls exit=2` with three «No such file or directory» lines; `0`; `0`. *Derived: the Architect's
  rehearsal of §7's blocks against a stand-in for `claude setup-token`, 25.10.2026; the `awk` counts only a process whose
  command is `claude setup-token`, so the shell that carries this text is not counted.*
- **V9. No regression.** `git status --porcelain` prints nothing before the report is added, and the report's commit
  touches `CryptoReports/TZ-73-run-login-remint-report.md` and nothing else (`git show --stat`).

---

## 9. The report

`CryptoReports/TZ-73-run-login-remint-report.md`, in contract §10's format, committed to `main`.
- **The top of the report states the previous TZ's state** (contract §8): TZ-72 opened no branch and no pull request, so
  nothing unmerged underlies this session.
- `## Status` is COMPLETED where A1 read an answering login, or where C1–C3 passed after a mint; BLOCKED otherwise, with
  the stage and the line that decided it.
- `## Scope Executed` names the class: report-only.
- `## Implementation Summary` gives, one line each: A1's line and the row of §7's table it fell in; whether a login was
  minted; the `url` and `take` lines; the new file's `stat` line with its modified time to the second; C2's line or lines;
  C3's last count.
- `## Remaining Risks` names at least: the cause of the revocation is unmeasured and the login may be refused again — the
  journal's next 401 against the file's modified time is the reading; production runs go on the host's 2.1.282 until
  TZ-72's merge; the code the Boss returned sits in the conversation that carried it; the probes measured the host's CLI,
  and TZ-72's A3 measures the pinned file under the same limits.
- `## Commit` states the message of `## Commit Message` and no hash (contract §10).
- `## Pull Request` carries the fixed report-only line of §2, and no argument.
- `## CI Execution` states that no branch exists and no workflow ran for this TZ.
- `## Final Repository State` names the checkout the fingerprints were taken against, by commit, and states what the host
  holds: no unit, session, directory or process left (V8), and the credential file's `stat` line.
- `## Fingerprints` carries the map, §0's four files, the two files §0's gate adds, and per anchor the command and the
  text the match returned (contract §5).

---

## Commit Message

Report, on `main`:

```
TZ-73: report — the run's Claude login re-read on the host and, where the server refused it, minted again and probed once
```

---

## 10. The helper — `tz73-login.py`

85 lines, MD5 `fc2b1e506d954ad0700f81e8fcf1edfa`. Cut with `awk '/^````python$/{f=1;next} /^````$/{f=0} f'` (A0); the cut file
is the block below, line for line.

````python
#!/usr/bin/env python3
"""TZ-73: handle `claude setup-token`'s typescript without ever printing a token.

  tz73-login.py url    <typescript>             the authorization URL alone, on stdout
  tz73-login.py screen <typescript>             the screen's text, every run of 32+ characters masked
  tz73-login.py take   <typescript> <target>    the new login into <target>; prints `length=<n> matched=<yes|no>`

`take` writes only when the typescript holds exactly one distinct token of 100 to 130 characters, and writes
it with mode 0600, no newline, through a file beside the target renamed over it. Any other outcome leaves
the target untouched.
"""
import os
import re
import sys

CSI = re.compile(rb"\x1b\[[0-?]*[ -/]*[@-~]")
OSC = re.compile(rb"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")
ESC = re.compile(rb"\x1b[@-Z\\-_]")
TOKEN = re.compile(rb"sk-ant-oat01-[A-Za-z0-9_-]+")
URL = re.compile(r"https://\S+")
LONG = re.compile(r"\S{32,}")
LENGTH_MIN, LENGTH_MAX = 100, 130


def plain(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    for rx in (OSC, CSI, ESC):
        raw = rx.sub(b"", raw)
    return raw.replace(b"\r", b"")


def cmd_url(path):
    text = plain(path).decode("utf-8", "replace")
    found = sorted(set(URL.findall(text)))
    ok = len(found) == 1 and "state=" in found[0]
    sys.stderr.write("urls_found=%d has_state=%s\n" % (len(found), "yes" if found and "state=" in found[0] else "no"))
    if not ok:
        return 1
    sys.stdout.write(found[0] + "\n")
    return 0


def cmd_screen(path):
    text = plain(path).decode("utf-8", "replace")
    sys.stdout.write(LONG.sub("<masked>", text))
    return 0


def cmd_take(path, target):
    tokens = sorted(set(TOKEN.findall(plain(path))))
    if len(tokens) != 1 or not (LENGTH_MIN <= len(tokens[0]) <= LENGTH_MAX):
        print("length=%d matched=no" % (len(tokens[0]) if len(tokens) == 1 else 0))
        return 1
    token = tokens[0]
    tmp = target + ".new"
    try:
        os.unlink(tmp)
    except FileNotFoundError:
        pass
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, token)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.chmod(tmp, 0o600)
    os.replace(tmp, target)
    print("length=%d matched=yes" % len(token))
    return 0


def main(argv):
    if len(argv) == 3 and argv[1] == "url":
        return cmd_url(argv[2])
    if len(argv) == 3 and argv[1] == "screen":
        return cmd_screen(argv[2])
    if len(argv) == 4 and argv[1] == "take":
        return cmd_take(argv[2], argv[3])
    sys.stderr.write("usage: tz73-login.py url|screen <typescript> | take <typescript> <target>\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
````

---

## 11. The controls — `tz73-controls.py`

118 lines, MD5 `26d66cd5e76cb2f8b317751ef01b9bd3`. Cut with `awk '/^````pycheck$/{f=1;next} /^````$/{f=0} f'` (A0). It reads
no credential: its tokens are fake and planted in its own scratch directory.

````pycheck
#!/usr/bin/env python3
"""TZ-73 controls: the login helper against planted FAKE tokens in a scratch directory.

  tz73-controls.py <helper> <scratch-dir>

Prints one PASS or FAIL line per check and a last line `controls: <n> checks, <k> failed`; exits 1 on any
failure. No real credential is read or written.
"""
import os
import random
import stat
import string
import subprocess
import sys

HELPER, T = sys.argv[1], sys.argv[2]
os.makedirs(T, exist_ok=True)
random.seed(7)
ALPHA = string.ascii_letters + string.digits + "_-"


def fake(tail):
    return "sk-ant-oat01-" + "".join(random.choice(ALPHA) for _ in range(tail))


TOK108, TOK109, TOK_B = fake(95), fake(96), fake(95)
URL1 = ("https://claude.ai/oauth/authorize?code=true&client_id=00000000-0000-0000-0000-000000000000"
        "&response_type=code&redirect_uri=https%3A%2F%2Fexample.invalid%2Fcallback&scope=user%3Ainference"
        "&code_challenge=" + "A" * 43 + "&code_challenge_method=S256&state=" + "B" * 43)
URL2 = "https://example.invalid/other?x=1&state=zz"
ESC = b"\x1b"
RESULTS = []


def run(*args):
    p = subprocess.run([sys.executable, "-I", HELPER] + list(args), capture_output=True)
    return p.returncode, p.stdout.decode(), p.stderr.decode()


def put(name, data):
    path = os.path.join(T, name)
    with open(path, "wb") as fh:
        fh.write(data)
    return path


def check(name, cond, extra=""):
    RESULTS.append(bool(cond))
    print(("PASS " if cond else "FAIL ") + name + (("  " + extra) if extra else ""))


def target(content=b"OLDOLDOLD"):
    path = os.path.join(T, "target")
    for p in (path, path + ".new"):
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass
    if content is not None:
        with open(path, "wb") as fh:
            fh.write(content)
        os.chmod(path, 0o644)
    return path


osc = ESC + b"]8;;" + URL1.encode() + b"\x07" + URL1.encode() + ESC + b"]8;;\x07"
t_url = put("t-url", b"Welcome\r\n" + ESC + b"[1m" + b"Browser didn't open? Use the url below" + ESC + b"[0m\r\n"
            + osc + b"\r\nPaste code here if prompted > \r\n")
t_url2 = put("t-url2", URL1.encode() + b"\r\n" + URL2.encode() + b"\r\n")
t_nostate = put("t-nostate", b"https://claude.ai/oauth/authorize?code=true\r\n")
t_tok = put("t-tok", b"Success!\r\nYour OAuth token (valid for 1 year):\r\n" + ESC + b"[32m" + TOK108.encode()
            + ESC + b"[0m\r\nStore this token securely.\r\nexport CLAUDE_CODE_OAUTH_TOKEN=" + TOK108.encode() + b"\r\n")
t_tok109 = put("t-tok109", b"x\r\n" + TOK109.encode() + b"\r\n")
t_none = put("t-none", b"OAuth error: Invalid code. Please make sure the full code was copied\r\nPress Enter to retry.\r\n")
t_two = put("t-two", TOK108.encode() + b"\r\n" + TOK_B.encode() + b"\r\n")
t_short = put("t-short", ("sk-ant-oat01-" + "a" * 40).encode() + b"\r\n")
t_wrap = put("t-wrap", TOK108[:80].encode() + b"\r\n" + TOK108[80:].encode() + b"\r\n")

rc, out, err = run("url", t_url)
check("url: one whole URL printed, exit 0", rc == 0 and out.strip() == URL1 and "urls_found=1 has_state=yes" in err)
rc, out, err = run("url", t_url2)
check("url: two distinct URLs refused", rc == 1 and out == "" and "urls_found=2" in err)
rc, out, err = run("url", t_nostate)
check("url: URL without state refused", rc == 1 and out == "" and "has_state=no" in err)
rc, out, err = run("url", t_none)
check("url: no URL refused", rc == 1 and "urls_found=0" in err)

tgt = target()
rc, out, err = run("take", t_tok, tgt)
data = open(tgt, "rb").read()
check("take: token twice with colour codes and CRLF is placed",
      rc == 0 and out.strip() == "length=108 matched=yes" and data == TOK108.encode())
check("take: mode 0600, no newline, no .new left",
      stat.S_IMODE(os.stat(tgt).st_mode) == 0o600 and not data.endswith(b"\n") and not os.path.exists(tgt + ".new"))
check("take: the token is in neither stdout nor stderr", TOK108 not in out and TOK108 not in err)

tgt = target(None)
rc, out, err = run("take", t_tok109, tgt)
check("take: a 109-character token is placed where no target existed",
      rc == 0 and out.strip() == "length=109 matched=yes" and open(tgt, "rb").read() == TOK109.encode())

for label, path in (("no token", t_none), ("two different tokens", t_two), ("a short token", t_short),
                    ("a token wrapped at 80 columns", t_wrap)):
    tgt = target()
    rc, out, err = run("take", path, tgt)
    check("take: %s is refused and the target is untouched" % label,
          rc == 1 and "matched=no" in out and open(tgt, "rb").read() == b"OLDOLDOLD" and not os.path.exists(tgt + ".new"))

rc, out, err = run("screen", t_tok)
check("screen: the token is masked and the words stay",
      rc == 0 and TOK108 not in out and "<masked>" in out and "Store this token securely." in out)
rc, out, err = run("screen", t_url)
check("screen: the URL is masked", rc == 0 and URL1 not in out and "Paste code here" in out)
check("screen: no run of 32 characters survives", all(len(w) < 32 for w in out.replace("<masked>", " ").split()))

failed = RESULTS.count(False)
print("controls: %d checks, %d failed" % (len(RESULTS), failed))
sys.exit(1 if failed else 0)
````
