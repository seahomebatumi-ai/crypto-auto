# TZ-74 — The run's Claude login: five stray characters cut off its end, and two probes on it

**Canonical filename:** `CryptoTZ/TZ-74-run-login-cut.md`
**Report:** `CryptoReports/TZ-74-run-login-cut-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine**, because the run's login lives on it.
**Class:** report-only TZ (contract §8) — it authorises exactly one written repository file, its own report. Its
`## Scope` names no other repository file; the host paths of §4 are outside the repository, as TZ-61's and TZ-73's were.
**No branch and no pull request exist for it:** a branch carries repository files and nothing else, and the login cannot
travel through git.
**Model:** Opus
**Trigger:** `EXECUTE TZ-74`, with nothing under it: no credential arrives (§1), and the Boss is asked for nothing during
the session — no approval, no code, no browser.
**Previous TZ:** TZ-73, BLOCKED at C2 on 25.10.2026; its report is on `main` (`f99d6fd`). It opened no branch and no pull
request, so nothing of it awaits a merge. TZ-72 re-runs after this TZ (§3).
**Issued:** 25.10.2026, by the Architect.
**Written against:** contract v31, map `2026-10-25-a` as it stands on `main` — this TZ moves no map revision, so that TZ-72
re-runs against the same one (§3) — and `main` at `f99d6fd`, read by the Architect from the repository on 25.10.2026,
TZ-73's report included.

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

**None arrives.** The login is already on the VPS: TZ-73 minted it at 07:33:14 UTC on 25.10.2026 and it has not been
displayed since. This TZ removes five characters from the end of its file and offers the result to the server in a probe.

**No command in this session prints the credential file.** Its only readings are file metadata (`stat`), counts
(`/usr/bin/grep -c`, `… | wc -l`) and the one-line `python3` of B2, which prints four numbers. The cut itself is
`truncate`, which prints nothing. No value is printed, logged, committed or quoted — in the report, a commit, a check's
label or the chat — and no other credential is read: neither the deploy key, nor the bot's token, nor the Binance key, nor
the SoSoValue key. Nothing is sent to Telegram.

---

## 2. Contract, map and outside text this TZ obeys

Contract §7 item 6:

> **A unit that runs a model session runs as its own unprivileged user, never root, and holds exactly two credentials: its own Claude login and the deploy key** (since v25)

— the probes of C run as `cryptorun`, the run unit's own user, never as root, and hand it the login the unit's own way
(`LoadCredential=`, read inside the unit into the environment of the CLI child alone).

> The session writes each value to its file without echoing it; afterwards the file is read only by a command that prints a count — a check that needs the value compares against the file, and a report proves every value absent from everything the session wrote by searching for the value itself.

— B2, A1 and D are those readings and that search; the cut of B1 writes the value to its file without echoing it.

> **No value is ever printed, logged, committed or quoted** — in a report, a day log, a commit, a unit file or the chat.

> A value that appears anywhere else is revoked and replaced, never cleaned up

> The conversation that carried it is the one other copy

— D is the search; a value found where it should not be is revoked and replaced, and the report says so.

Contract §7 item 15:

> it may start TRANSIENT units from its branch for a measurement its TZ names, and its report proves none is left behind

— C starts transient units for a measurement this TZ names, and V6 proves none is left behind.

Contract §6, scope:

> The TZ's `## Scope` section is the complete authorisation. Anything not authorised is forbidden, however obviously beneficial it looks.

Contract §8, the class:

> A **report-only TZ** authorises exactly one written file — its own report — on the `CryptoReports/**` direct-push path.

— the credential file is on the host, outside the repository, and a pull request cannot carry it; §4 authorises its cut by
name under `### On the VPS, outside the repository`, the heading TZ-61's and TZ-73's scopes used, and the class is read off
the three repository lists, all of which are `None`. The report's `## Pull Request` carries the contract §10 line:

> `None — report-only TZ; direct push on the CryptoReports/** path (§8).`

Contract §9, a check:

> **A validator that passes with no data is a failed validator** (inv. 22). Any check must count what it verified and fail on zero.

Contract §12, blocked tasks:

> Report BLOCKED with the precise obstacle and what would unblock it.

**TZ-73's report** (`CryptoReports/TZ-73-run-login-remint-report.md`, on `main` at `f99d6fd`), which this TZ acts on. The
file the report left:

> `600 root root 113 2026-10-25 07:33:14.587401244 +0000 /etc/crypto-auto/credentials/claude-oauth-token`

and what it measured in it, with two counts that print a number and no part of the value:

> So the file holds a 108-character `sk-ant-oat01-` string with the five letters `Store` glued after it.

> The file is a 108-character `sk-ant-oat01-` string (13 + 95) followed by `Store`.

The server's answer to that file, twice:

> `True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token is invalid.'`

and its answer to the old login, on the program the run executes today, before anything was minted:

> `True success 401 [] 0 'Failed to authenticate. API Error: 401 OAuth access token has been revoked.'`

The report's own words on what unblocks it:

> the file cut to its first 108 bytes by a command that prints nothing, then C1–C3 again; the token minted here was never displayed and is probably still good

**TZ-55's report** (`CryptoReports/TZ-55-run-lane-own-user-report.md`), the first mint of this login class, made at the same
terminal width (1000 columns) — the file it left reads:

> `600 root root 108 /etc/crypto-auto/credentials/claude-oauth-token`

---

## 3. What is done, and why

**What happened.** TZ-73 ran on 25.10.2026 and stopped BLOCKED at C2. Its A1 read the old login refused on the program the
run executes today, 2.1.282 — `401`, «OAuth access token has been revoked», at 07:31:06 UTC — so the refusal that stopped
TZ-72 is the server's and not the pinned CLI's. Its B minted a new login at 07:33:14 UTC with the Boss's approval, and the
helper of TZ-73 §10 placed it in the file: `length=113`. The server refused that value twice within 79 seconds, and with
another word: «is invalid», where the old login read «has been revoked».

**What it means.** The file holds the new login with five characters glued after it, and that is the Architect's defect,
not the Executor's: the helper removed the screen's control codes *before* matching the token, so wherever the CLI moves the
cursor instead of writing a newline, the next word — `Store this token securely.` — joins the token (13 + 95 + 5 = 113).
The Architect ran the helper's own bytes (MD5 `fc2b1e506d954ad0700f81e8fcf1edfa`, cut from TZ-73 with the TZ's own `awk`) on four
synthetic screens on 25.10.2026: it placed 113 bytes ending `Store` for each of the three with a cursor movement after the
token, and 108 for the one with a newline, which is the only kind of screen TZ-73's controls drew; the match on the raw
bytes, which is the step TZ-55's §12.8 describes and which read 108 at the same terminal width, gave 108 for all four. The
login itself was not displayed, and the report's scan found no copy of it in the places it searched; it was never offered to
the server in its true form, so nothing measured says it is refused: the 113-byte string is not a login, and the first 108 bytes may be.

**What this TZ does.**
- **A** reads the host, then reads the file and lets the cut proceed only if it is exactly what TZ-73's report measured.
- **B** cuts the file in place to its first 108 bytes, with one command that prints nothing, and reads the result.
- **C** probes the cut login on the program the run executes today, as TZ-73's A1 did, and once more thirty seconds later.
- **D** proves the value absent from everything the session wrote, and **E** removes what the session made.

TZ-72 then re-runs unchanged — `EXECUTE TZ-72`, which writes `-report-2` (contract §13) — against the same map revision.
**A new mint is not chosen:** it asks the Boss for an approval and a code again, and the login minted at 07:33 would stay
valid on the server with no copy of it anywhere; the cut asks him nothing and tests that same login.

**What this TZ cannot decide.** Whether the server accepts the cut login, and for how long; why the two earlier logins were
revoked is not read here either (TZ-73 §2). Three outcomes, decided in advance:
- **both probes answer** — the run is restored for as long as the login lasts. The login's birth is the file's modified time
  TZ-73 recorded, 07:33:14 UTC; the cut moves the file's modified time to the cut's own, so the report carries both, and the
  journal's next 401 dates the life against the birth;
- **«invalid» again** — the cut did not make a login: BLOCKED, and the Architect reads the lines. This TZ makes no second
  cut and no mint;
- **«revoked», or any other 401 on the cut value** — the server knows this login and refuses it at once: the credential class
  is the defect, and the run moves to an API key — a contract revision and the Architect's, never a third mint by TZ.

---

## 4. Scope

### Files to Modify

None.

### Files to Create

None.

### Files to Delete

None.

### On the VPS, outside the repository — authorised, and nothing else

- `/var/tmp/tz74-home/` — the probes' scratch home (`0700`, `cryptorun`); made in A0, removed in E. No probe touches the
  run's own home, `/var/lib/cryptorun`.
- `/var/tmp/tz74-scan/` — the scan's control files (D); made and removed in this session.
- Transient units `tz74-probe-1` to `tz74-probe-3`, numbered in the order the probes run, at most three — each collected
  when it exits.
- **One cut, in place, of `/etc/crypto-auto/credentials/claude-oauth-token` from 113 to 108 bytes, by `truncate`, and only
  where A1's gate passed.** That file is the only path under `/etc/crypto-auto/` this session writes; its owner and mode are
  not touched.
- Reading, never writing: `systemctl cat` and `systemctl is-active` on `crypto-run.service`; `stat` and counts of the
  credential file; `/usr/bin/claude --version`; `find` and `journalctl` in D.

**Nothing is installed, enabled, disabled, started, stopped or restarted: `/usr/bin/claude` and the npm global install
behind it are run and read, never changed; no persistent unit is touched; no run is started or requested; and nothing
under `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or `/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- No file of the repository is changed: not `vps/**`, not a unit, not the map, not the contract. TZ-72's patch and stages
  are untouched, and no probe is made on the pinned CLI — that is TZ-72's A3.
- No helper, no `claude setup-token`, no tmux session and no mint: the helper of TZ-73 §10 is not run again, and its repair
  is not built here.
- No other login, key or token is minted, read or replaced. An API key for the run is a contract revision (§3).
- The old login is not revoked: no command does that, and the server has already refused it.
- No message is sent to Telegram, and nothing is scheduled.
- No other version, model id or probe than §7's.

---

## 6. Rules — binding in every stage

- **`grep` and `find` in this TZ are `/usr/bin/grep` and `/usr/bin/find`.** In the Executor's shell `grep` is a function that
  hands its arguments to the session's own program (TZ-73's report, D-1), `find` may be one too, and every known answer below
  is GNU's. Each command writes the full path; an unqualified `grep` or `find` in a host command is a deviation.
- **The credential file is written once, by B1's `truncate`, and only after A1's gate passed.** Any other state of the file
  at A1 → no write.
- **The credential file is read only by `stat`, by counts and by B2's one-liner;** no command prints it, and no pattern
  file made from it is written anywhere.
- **Every block runs under `bash`** (`$RANDOM` and `PIPESTATUS` are bash's), and a wait is a loop of two-second sleeps, as
  TZ-73's were, not one long `sleep`.
- **A refusal by the session's permission mode is not a blocker of this TZ and is not worked around:** report the command
  and the label at once, in the session, and continue when the Boss has changed the mode there.
- **No probe but §7's:** three at most. The report carries every printed line and every `exit=` line.
- **Nothing persistent.** The report proves every unit and directory gone (V6).
- **A check that counts nothing fails its item** (contract §9).

---

## 7. Stages

- **A0. The host and the baseline — readings; the only write is the probes' home.**

  ```sh
  id -un
  systemctl cat crypto-run.service | /usr/bin/grep -nE "^(User=|LoadCredential=claude-oauth-token:)"
  systemctl is-active crypto-run.service
  command -v python3 systemd-run truncate journalctl stat awk md5sum /usr/bin/find
  /usr/bin/grep --version | head -1
  /usr/bin/claude --version
  git fetch --all --prune
  git rev-parse --is-shallow-repository
  git status --porcelain
  ```

  The first prints `root`; the second prints `User=cryptorun` and
  `LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token` (with `systemctl cat`'s own line
  numbers; TZ-73's A0 read them at 11 and 22); the third prints the unit's state, one word — any state is reported and decides
  nothing, because a unit that is running holds its own copy of the login; the fourth prints eight paths — any missing →
  BLOCKED; the fifth prints `grep (GNU grep) 3.11`, and another version is reported and decides nothing; the sixth prints
  `2.1.282 (Claude Code)`, and another version is reported — C decides; the seventh fetches and the eighth prints `false`
  (else `git fetch --unshallow`, contract §3); the ninth prints nothing. Contract §5's gate runs against `origin/main` and §0:
  per anchor the command and the text the match returned, and the table's row count beside the number compared. **Any of the
  first, second or fourth reading not so, or a gate that fails → BLOCKED.** Then the probes' home, the only write of A0:

  ```sh
  install -d -m 0700 -o cryptorun -g cryptorun /var/tmp/tz74-home
  ```

  *Derived: TZ-73's report, A0, printed the same readings on this host on 25.10.2026 — `root`; `User=cryptorun` and the
  `LoadCredential=` line at 11 and 22; `python3`, `systemd-run`, `stat`, `awk` and `md5sum` among its fourteen paths;
  `grep (GNU grep) 3.11` behind its function; `2.1.282 (Claude Code)`; `false`; nothing. `truncate` is coreutils, the
  package of `stat`; `journalctl` is systemd, the package of `systemd-run`; `/usr/bin/find` is findutils; none of the three was
  named there, so a missing one is BLOCKED and reported.*

- **A1. The file's state — a gate; readings only.**

  ```sh
  stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
  /usr/bin/grep -cE '^sk-ant-oat01-[A-Za-z0-9_-]{95}Store$' /etc/crypto-auto/credentials/claude-oauth-token
  /usr/bin/grep -c . /etc/crypto-auto/credentials/claude-oauth-token
  ```

  The gate passes only if all three read as the report measured: `600 root root 113 <modified> <path>`, then `1`, then `1`
  (the file is one non-empty line of exactly `sk-ant-oat01-`, 95 token characters and `Store`). The modified time is the
  login's birth and goes into the report to the second; TZ-73 read `2026-10-25 07:33:14.587401244 +0000`, and a different
  time with the same size and counts decides nothing. **Any other size or a count of 0 → no write: skip B, C and D, run E,
  and report BLOCKED with the three readings** — the file has changed since TZ-73's report, and the Architect re-plans.
  *Derived: TZ-73's report, C1, printed `600 root root 113 2026-10-25 07:33:14.587401244 +0000 …` and its
  `### Why C2 refused the new login`, item 4, printed `1` for the second reading's pattern; the third reading repeats the
  first line of its C3. That the extra five characters are the CLI's next word is the Architect's reproduction of
  25.10.2026 (§3), and A1 re-measures what it can: the count.*

- **B. The cut — only where A1's gate passed.**
  - **B1.**

    ```sh
    truncate -s 108 /etc/crypto-auto/credentials/claude-oauth-token; echo "truncate exit=$?"
    ```

    It prints `truncate exit=0` and nothing else.
  - **B2.** The file, by metadata and counts only:

    ```sh
    stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
    python3 -I -c 'd=open("/etc/crypto-auto/credentials/claude-oauth-token","rb").read(); print("length=%d newline_bytes=%d non_empty_lines=%d prefix_ok=%d" % (len(d), d.count(b"\n"), len([l for l in d.split(b"\n") if l]), d.startswith(b"sk-ant-oat01-")))'
    /usr/bin/grep -cE '^sk-ant-oat01-[A-Za-z0-9_-]{95}$' /etc/crypto-auto/credentials/claude-oauth-token
    ```

    The first prints `600 root root 108 <cut time> <path>`; the second `length=108 newline_bytes=0 non_empty_lines=1
    prefix_ok=1`; the third `1`. Anything else → the file stays as it is, skip C, run D and E, and report BLOCKED with the
    readings.

- **C. The probes — only where B2 read as required.** The first, n = 1 (n numbers the session's probes in the order they run)
  — the host's CLI, which is what `crypto-run.service` executes today, on the login the unit hands it, with the unit file's
  own memory limits and a three-minute bound on the unit:

  ```sh
  systemd-run --wait --pipe --collect --quiet --unit=tz74-probe-<n> \
    -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/tmp/tz74-home \
    -p Environment=HOME=/var/tmp/tz74-home -p Environment=DISABLE_AUTOUPDATER=1 \
    -p Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 -p Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
    -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
    -p MemoryMax=167772160 -p MemorySwapMax=536870912 -p RuntimeMaxSec=180 \
    -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
    /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /usr/bin/claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model claude-haiku-4-5-20251001' \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), d.get("api_error_status"), sorted((d.get("modelUsage") or {}).keys()), len(d.get("permission_denials") or []), repr(str(d.get("result"))[:120]))'
  echo "exit=${PIPESTATUS[0]} ${PIPESTATUS[1]}"
  ```

  `bash` runs the block, and the `echo` stays directly under the pipeline: it prints the exit codes of `systemd-run` and of
  the summarizer. The line prints `<is_error> <subtype> <api_error_status> <models> <denials> <result, 120 characters>`, and
  the report carries the command as run, the line and the `exit=` line. *Derived: the command is TZ-73's A1 and C2 probe,
  which ran on this host and printed `True success 401 [] 0 '…'` for the old login and for the 113-byte value; only the
  result's width changed, from 80 to 120 characters, so that the deciding word is never cut. An answering line is read from
  the fields the production run itself reads — `is_error` false and `modelUsage` non-empty — which the journal shows on
  21.10 and 24.10 (`is_error` false, `models=claude-haiku-4-5-20251001,claude-opus-5-5,claude-sonnet-5`, TZ-72's report).*
  The line decides:

  | The line | Means | Then |
  |---|---|---|
  | starts `False`, its models list is not empty, `systemd-run` exits 0 | the login answers | wait thirty seconds with `for i in $(seq 1 15); do sleep 2; done`, then the probe once more as n = 2; both lines are carried. A second line that is not an answer is BLOCKED with both lines. |
  | starts `True`, `api_error_status` is `401` and the result text contains `invalid` | the value is still not a login | **stop probing**; BLOCKED with the line |
  | starts `True` and `api_error_status` is `401` with any other text (`revoked`, `expired`, `authenticate`, `log in`) | the server knows this login and refuses it | **stop probing**; BLOCKED with the line — the credential class is the defect (§3) |
  | exit 137, or an empty line | the unit ran out of memory | run the probe once more as the next n with `-p MemoryMax=318767104 -p MemorySwapMax=385875968` (the last run's own limits, read by TZ-72's A0) in place of the two memory properties, and carry both lines; where it still reads this row → BLOCKED |
  | anything else (another status, 429, 5xx, a traceback) | not decided by this TZ | wait sixty seconds with `for i in $(seq 1 30); do sleep 2; done`, then run the probe once more as the next n; where it is still not an answer → BLOCKED with both lines |

  **At most three probes in all.**

- **D. The scan — the exact value against everything the session wrote or could have written; the report's draft exists by
  now, with its headings.** Run where B ran, whatever C read, from the root of the worktree. First the scan is proven on a dummy, then run:

  ```sh
  F=/etc/crypto-auto/credentials/claude-oauth-token
  P="/var/tmp/tz74-home $HOME/.claude $HOME/.claude.json $HOME/.bash_history /tmp/claude-0 ."
  /usr/bin/grep -c . $F
  /usr/bin/grep -c '^$' $F
  install -d -m 0700 /var/tmp/tz74-scan/dir
  printf '%s\n' "dummy-$RANDOM-$RANDOM-$RANDOM" > /var/tmp/tz74-scan/pattern
  cp /var/tmp/tz74-scan/pattern /var/tmp/tz74-scan/dir/holds
  printf 'nothing here\n' > /var/tmp/tz74-scan/dir/lacks
  /usr/bin/grep -rlFs -D skip -f /var/tmp/tz74-scan/pattern /var/tmp/tz74-scan/dir | wc -l
  /usr/bin/find $P -type f 2>/dev/null | wc -l
  /usr/bin/grep -rlFs -D skip -f $F $P | wc -l
  /usr/bin/find /var/log -type f -not -path '/var/log/journal/*' -newermt '2026-10-25 07:25:00 UTC' | wc -l
  /usr/bin/find /var/log -type f -not -path '/var/log/journal/*' -newermt '2026-10-25 07:25:00 UTC' -exec /usr/bin/grep -lFs -f $F {} + | wc -l
  journalctl --no-pager -o cat --since "$(date -d '2026-10-25 07:25:00 UTC' '+%Y-%m-%d %H:%M:%S')" | wc -l
  journalctl --no-pager -o cat --since "$(date -d '2026-10-25 07:25:00 UTC' '+%Y-%m-%d %H:%M:%S')" | /usr/bin/grep -cF -f $F
  for p in $P; do [ -e "$p" ] && echo "present $p" || echo "absent $p"; done
  ```

  Nine numbers are printed, then one line per place. In order: `1` and `0` — the credential file is one line and no empty one,
  so as a pattern file it cannot match every line; `1` — the dummy pattern finds the file that holds it and not the one that
  does not; **a number above 0** — the files the scan below examines; `0` — the value in the session's places (the probes'
  home, the Executor's own `.claude` with its transcripts and `.claude.json`, its shell history, the session's scratch
  `/tmp/claude-0`, and this worktree with the report as drafted); **a number above 0** and `0` — the log files modified since
  07:25 UTC examined, and the value in them; **a number above 0** and `0` — the journal lines since 07:25 UTC examined, and
  the value in them. A scan that examines nothing proves nothing (contract §9): a zero where a number above 0 is required
  fails the item. `/var/tmp/tz74-home`, `$HOME/.claude` and `.` must read `present`; the others are reported either way.
  **A hit prints no value**: the scan is run again without its `| wc -l`, which prints file names and never the value, and the
  names alone go into the report; contract §7 item 6 applies — the login is revoked and replaced — and the Architect issues
  the replacement.
  *Derived: the answers `1`, `0`, `1` and the scan's `0` are TZ-73's C3 on this host (`1`, `0`, `1`, `0`); the `-D skip` flag, the `find` filters,
  the three `examined` counts and the `journalctl` window are the Architect's rehearsal of this block on stand-ins on
  25.10.2026, including a planted copy of a fake value that turned each `0` into a positive count. 07:25 UTC precedes TZ-73's
  session, which began after the TZ was uploaded at 07:28.*

- **E. Clean-up, whatever A to D read.**

  ```sh
  rm -rf /var/tmp/tz74-home /var/tmp/tz74-scan
  ls -d /var/tmp/tz74-home /var/tmp/tz74-scan; echo "ls exit=$?"
  ```

  `ls exit=2`, with two «No such file or directory» lines.

---

## 8. Validation

Every item names its command and its known answer; each answer was derived where it says.

- **V1. The baseline.** A0's readings and the gate of contract §5, with the clone clean.
- **V2. The gate.** A1's three readings as the report measured, and the birth time to the second.
- **V3. The cut, where B ran.** `truncate exit=0`; B2: `600 root root 108 <cut time> /etc/crypto-auto/credentials/claude-oauth-token`,
  `length=108 newline_bytes=0 non_empty_lines=1 prefix_ok=1`, and `1`. *Derived: the Architect's run of B1 and B2 on a
  stand-in file of 108 token characters plus `Store`, 25.10.2026, which printed those lines; TZ-55's report, C4, printed
  `600 root root 108` and `newline_bytes=0 … non_empty_lines=1 prefix_ok=1` for the first mint of this login class.*
- **V4. The probes, where C ran.** The first line starts `False` with a models list that is not empty and `exit=0 0`, and
  the second, thirty seconds later, the same. *Derived: §7 C.*
- **V5. The scan, where D ran.** `1`, `0`, `1`, a number above 0, `0`, a number above 0, `0`, a number above 0, `0`; and
  `present` for the three places named. *Derived: §7 D.*
- **V6. Nothing left behind.**

  ```sh
  ls -d /var/tmp/tz74-home /var/tmp/tz74-scan; echo "ls exit=$?"
  systemctl list-units --all --no-legend 'tz74-*' | wc -l
  ls -1 /etc/crypto-auto/credentials/ | /usr/bin/grep -c '\.new$'
  ```

  Known answers: `ls exit=2` with two «No such file or directory» lines; `0`; `0`. *Derived: TZ-73's report, D and V8, printed the
  first two forms on this host (`ls exit=2`, `0`); the third counts names only and the directory is listed by name alone,
  as TZ-73's report did for its `.new`.*
- **V7. No regression.** `git status --porcelain` prints nothing before the report is added, and the report's commit
  touches `CryptoReports/TZ-74-run-login-cut-report.md` and nothing else (`git show --stat`).

---

## 9. The report

`CryptoReports/TZ-74-run-login-cut-report.md`, in contract §10's format, committed to `main`.
- **The top of the report states the previous TZ's state** (contract §8): TZ-73 opened no branch and no pull request, so
  nothing unmerged underlies this session.
- `## Status` is COMPLETED where A1's gate passed, B read as required, both probes answered and D's answers are the known
  ones; BLOCKED otherwise, with the stage and the line that decided it.
- `## Scope Executed` names the class: report-only.
- `## Implementation Summary` gives, one line each: A1's three readings and the birth time to the second; B1's line and B2's
  three; each probe's line, its `exit=` line and the row of §7's table it fell in; D's nine numbers; E's lines.
- `## Remaining Risks` names at least: the cause of the earlier revocations is unmeasured and the login may be refused again
  — the journal's next 401 against the birth, 07:33:14 UTC, is the reading; production runs go on the host's 2.1.282 until
  TZ-72's merge; the code the Boss returned in TZ-73 sits in that session's conversation, single-use and consumed; the probes
  measured the host's CLI, and TZ-72's A3 measures the pinned file under the same limits.
- `## Commit` states the message of `## Commit Message` and no hash (contract §10).
- `## Pull Request` carries the fixed report-only line of §2, and no argument.
- `## CI Execution` states that no branch exists and no workflow ran for this TZ.
- `## Final Repository State` names the checkout the fingerprints were taken against, by commit, and states what the host
  holds: no unit or directory left (V6), and the credential file's `stat` line.
- `## Fingerprints` carries the map, §0's four files, the two files §0's gate adds, and per anchor the command and the text
  the match returned (contract §5).

---

## Commit Message

Report, on `main`:

```
TZ-74: report — the run's Claude login cut to its 108 characters and probed on the host
```
