# Implementation Report — TZ-74

Previous TZ: TZ-73 opened no branch and no pull request. Its report, `f99d6fd`, is on `main`, and
`git ls-remote --heads origin` lists no `tz-73` head and no `tz-74` head. Nothing unmerged lies under this session.

## Status

**COMPLETED.** A1's gate passed: the file was `600 root root 113`, born `2026-10-25 07:33:14 UTC`, and both counts were `1`.
B1 cut it to 108 bytes (`truncate exit=0`), and B2 read it as required. Both probes on the cut login answered, thirty
seconds apart, on the program the run executes today (2.1.282):

```
False success None ['claude-haiku-4-5-20251001'] 0 'ok'
exit=0 0
```

D's nine numbers are the known answers, and E and V6 left nothing behind. **The run's Claude login answers again.** The
113-byte string TZ-73 placed was the login plus `Store`, and its first 108 bytes are a login the server accepts.

TZ-72 re-runs next (`EXECUTE TZ-72`, `-report-2`), against the same map revision.

## Inbound Filing

None. The TZ was already at its canonical path, `CryptoTZ/TZ-74-run-login-cut.md`, on `origin/main`. It was added by
`81a81c8 Add files via upload`. Nothing was moved or renamed.

## Scope Executed

**Class: report-only TZ** (contract §8). `## Scope` names no file under `Files to Modify`, `Files to Create` or
`Files to Delete`. The host paths of `### On the VPS, outside the repository` are outside the repository.

- A0 — executed. Every reading was as required, the gate passed, and the probes' home was made.
- A1 — executed. The gate passed → B.
- B1, B2 — executed. One `truncate`, then the three readings as required → C.
- C — executed. Two probes (`tz74-probe-1`, `tz74-probe-2`) both fell in row 1 of §7's table. The third probe the TZ
  allows was not needed and not run.
- D — executed against the draft of this report, with every heading present.
- E — executed; V6 then read nothing left behind.

## Files Created

None in the repository but this report. On the host: `/var/tmp/tz74-home/` (A0) and `/var/tmp/tz74-scan/` (D). Each
one's removal is under `## Final Repository State`.

## Files Modified

None in the repository. On the host: `/etc/crypto-auto/credentials/claude-oauth-token`, cut once in place by B1's
`truncate` from 113 to 108 bytes. Its owner and mode are unchanged.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

One line each (TZ §9):

- **A1:** `600 root root 113 2026-10-25 07:33:14.587401244 +0000 /etc/crypto-auto/credentials/claude-oauth-token`, then
  `1`, then `1`. **The login's birth is 2026-10-25 07:33:14 UTC**, the same as TZ-73's C1.
- **B1:** `truncate exit=0`.
- **B2:** `600 root root 108 2026-10-25 08:18:07.869655000 +0000 /etc/crypto-auto/credentials/claude-oauth-token`;
  `length=108 newline_bytes=0 non_empty_lines=1 prefix_ok=1`; `1`. The cut time is 08:18:07 UTC.
- **Probe 1 (n = 1):** `False success None ['claude-haiku-4-5-20251001'] 0 'ok'`, `exit=0 0`, row 1 of §7's table
  («the login answers»). It ran between 08:18:07 and 08:18:19 UTC.
- **Probe 2 (n = 2):** `False success None ['claude-haiku-4-5-20251001'] 0 'ok'`, `exit=0 0`, row 1. It started after
  the thirty-second wait, 08:18:31 → 08:19:01 UTC, and ended by 08:19:04 UTC.
- **D:** `1`, `0`, `1`, `2352`, `0`, `6`, `0`, `2399`, `0`, and `present` for all six places.
- **E:** two «No such file or directory» lines, then `ls exit=2`.

### A0 — the host and the baseline

Run as root in this worktree under `bash`. Before it, `git merge --ff-only origin/main` brought the worktree from
`f99d6fd` to `81a81c8`, the commit that uploaded the TZ.

```
$ id -un
root
$ systemctl cat crypto-run.service | /usr/bin/grep -nE "^(User=|LoadCredential=claude-oauth-token:)"
11:User=cryptorun
22:LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token
$ systemctl is-active crypto-run.service
inactive
$ command -v python3 systemd-run truncate journalctl stat awk md5sum /usr/bin/find
/usr/bin/python3
/usr/bin/systemd-run
/usr/bin/truncate
/usr/bin/journalctl
/usr/bin/stat
/usr/bin/awk
/usr/bin/md5sum
/usr/bin/find
$ /usr/bin/grep --version | head -1
grep (GNU grep) 3.11
$ /usr/bin/claude --version
2.1.282 (Claude Code)
$ git fetch --all --prune
[exit 0]
$ git rev-parse --is-shallow-repository
false
$ git status --porcelain
(nothing)
```

- The first reading is `root`.
- The second is `User=cryptorun` and the `LoadCredential=` line, at 11 and 22, as TZ-73's A0 read them.
- The third is `inactive`. That is reported and decides nothing (§7 A0).
- The fourth prints eight paths, so no tool is missing.
- The fifth is `grep (GNU grep) 3.11`, and the sixth is `2.1.282 (Claude Code)`.
- The seventh exited 0, the eighth is `false`, and the ninth is empty.
- `date -u` after the block: `Sun Oct 25 08:17:35 AM UTC 2026`.

In this session's shell `grep` and `find` are both functions (`type grep`, `type find` → `grep is a function`,
`find is a function`), as §6 warns. Every host `grep` and `find` was written `/usr/bin/grep` and `/usr/bin/find`.

Contract §5's gate ran against `origin/main` and passed (`## Fingerprints`). Then the one write of A0:

```
$ install -d -m 0700 -o cryptorun -g cryptorun /var/tmp/tz74-home
install exit=0
$ stat -c '%a %U %G %n' /var/tmp/tz74-home
700 cryptorun cryptorun /var/tmp/tz74-home
```

### A1 — the gate

```
$ stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
600 root root 113 2026-10-25 07:33:14.587401244 +0000 /etc/crypto-auto/credentials/claude-oauth-token
$ /usr/bin/grep -cE '^sk-ant-oat01-[A-Za-z0-9_-]{95}Store$' /etc/crypto-auto/credentials/claude-oauth-token
1
$ /usr/bin/grep -c . /etc/crypto-auto/credentials/claude-oauth-token
1
```

The readings were taken at 08:17:57 UTC. All three are as TZ-73's report measured: size 113, the pattern count `1`, and
the non-empty-line count `1`. The modified time equals TZ-73's to the nanosecond. **The gate passed.**

### B — the cut

B1:

```
$ truncate -s 108 /etc/crypto-auto/credentials/claude-oauth-token; echo "truncate exit=$?"
truncate exit=0
```

It printed that line and nothing else.

B2:

```
$ stat -c '%a %U %G %s %y %n' /etc/crypto-auto/credentials/claude-oauth-token
600 root root 108 2026-10-25 08:18:07.869655000 +0000 /etc/crypto-auto/credentials/claude-oauth-token
$ python3 -I -c 'd=open("/etc/crypto-auto/credentials/claude-oauth-token","rb").read(); print("length=%d newline_bytes=%d non_empty_lines=%d prefix_ok=%d" % (len(d), d.count(b"\n"), len([l for l in d.split(b"\n") if l]), d.startswith(b"sk-ant-oat01-")))'
length=108 newline_bytes=0 non_empty_lines=1 prefix_ok=1
$ /usr/bin/grep -cE '^sk-ant-oat01-[A-Za-z0-9_-]{95}$' /etc/crypto-auto/credentials/claude-oauth-token
1
```

All three are as required. The mode and owner are unchanged (`600 root root`). The modified time moved to the cut,
08:18:07 UTC, so the login's birth is the time A1 read: **07:33:14 UTC**.

### C — the probes

Probe 1, run under `bash` with `<n>` = 1, character for character as §7 C gives it:

```
$ systemd-run --wait --pipe --collect --quiet --unit=tz74-probe-1 \
    -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/tmp/tz74-home \
    -p Environment=HOME=/var/tmp/tz74-home -p Environment=DISABLE_AUTOUPDATER=1 \
    -p Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 -p Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
    -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
    -p MemoryMax=167772160 -p MemorySwapMax=536870912 -p RuntimeMaxSec=180 \
    -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
    /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /usr/bin/claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model claude-haiku-4-5-20251001' \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), d.get("api_error_status"), sorted((d.get("modelUsage") or {}).keys()), len(d.get("permission_denials") or []), repr(str(d.get("result"))[:120]))'
False success None ['claude-haiku-4-5-20251001'] 0 'ok'
$ echo "exit=${PIPESTATUS[0]} ${PIPESTATUS[1]}"
exit=0 0
$ date -u
Sun Oct 25 08:18:19 AM UTC 2026
```

The line starts `False`, its models list is not empty, and `systemd-run` exited 0. That is row 1 of §7's table, «the
login answers». `api_error_status` is `None`, and the model answered `'ok'`.

The wait, then probe 2, in one `bash` block:

```
$ date -u
Sun Oct 25 08:18:31 AM UTC 2026
$ for i in $(seq 1 15); do sleep 2; done
$ date -u
Sun Oct 25 08:19:01 AM UTC 2026
$ systemd-run --wait --pipe --collect --quiet --unit=tz74-probe-2 \
    … (the same command, with <n> = 2 and nothing else changed) …
False success None ['claude-haiku-4-5-20251001'] 0 'ok'
$ echo "exit=${PIPESTATUS[0]} ${PIPESTATUS[1]}"
exit=0 0
$ date -u
Sun Oct 25 08:19:04 AM UTC 2026
```

Probe 2 is row 1 again, so both probes answered and probing stopped. Two of the three allowed probes were used. Neither
the 401 rows, the memory row nor the «anything else» row arose.

### D — the scan

Run under `bash` from the root of this worktree, after the draft of this report existed with every heading. `$HOME` is
`/root` and the host's time zone is UTC (`date +%Z` → `UTC`).

```
$ F=/etc/crypto-auto/credentials/claude-oauth-token
$ P="/var/tmp/tz74-home $HOME/.claude $HOME/.claude.json $HOME/.bash_history /tmp/claude-0 ."
$ /usr/bin/grep -c . $F
1
$ /usr/bin/grep -c '^$' $F
0
$ install -d -m 0700 /var/tmp/tz74-scan/dir
$ printf '%s\n' "dummy-$RANDOM-$RANDOM-$RANDOM" > /var/tmp/tz74-scan/pattern
$ cp /var/tmp/tz74-scan/pattern /var/tmp/tz74-scan/dir/holds
$ printf 'nothing here\n' > /var/tmp/tz74-scan/dir/lacks
$ /usr/bin/grep -rlFs -D skip -f /var/tmp/tz74-scan/pattern /var/tmp/tz74-scan/dir | wc -l
1
$ /usr/bin/find $P -type f 2>/dev/null | wc -l
2352
$ /usr/bin/grep -rlFs -D skip -f $F $P | wc -l
0
$ /usr/bin/find /var/log -type f -not -path '/var/log/journal/*' -newermt '2026-10-25 07:25:00 UTC' | wc -l
6
$ /usr/bin/find /var/log -type f -not -path '/var/log/journal/*' -newermt '2026-10-25 07:25:00 UTC' -exec /usr/bin/grep -lFs -f $F {} + | wc -l
0
$ journalctl --no-pager -o cat --since "$(date -d '2026-10-25 07:25:00 UTC' '+%Y-%m-%d %H:%M:%S')" | wc -l
2399
$ journalctl --no-pager -o cat --since "$(date -d '2026-10-25 07:25:00 UTC' '+%Y-%m-%d %H:%M:%S')" | /usr/bin/grep -cF -f $F
0
$ for p in $P; do [ -e "$p" ] && echo "present $p" || echo "absent $p"; done
present /var/tmp/tz74-home
present /root/.claude
present /root/.claude.json
present /root/.bash_history
present /tmp/claude-0
present .
$ date -u
Sun Oct 25 08:20:55 AM UTC 2026
```

Each of the nine numbers is the known answer:
- `1` and `0`: the credential file is one line with no empty line, so as a pattern file it cannot match every line.
- `1`: the dummy pattern finds the file that holds it and not the one that lacks it.
- `2352` files were examined in the session's places, and `0` of them hold the value. The places are:
  - the probes' home;
  - `/root/.claude` with this session's transcripts, and `/root/.claude.json`;
  - `/root/.bash_history`;
  - the session's scratch `/tmp/claude-0`;
  - this worktree, with the report as drafted.
- `6` log files under `/var/log` were modified since 07:25 UTC, and `0` of them hold the value.
- `2399` journal lines were written since 07:25 UTC, and `0` of them hold the value.

All six places read `present`, including the three §7 D requires: `/var/tmp/tz74-home`, `$HOME/.claude` and `.`.
**No hit**, so contract §7 item 6's revocation clause is not triggered.

The pattern file is the cut file itself. So this scan searches for the 108-character login, the value the server
accepted. This is the scan TZ-73's report could run only as a second, stricter pass.

### E — clean-up

```
$ rm -rf /var/tmp/tz74-home /var/tmp/tz74-scan
$ ls -d /var/tmp/tz74-home /var/tmp/tz74-scan; echo "ls exit=$?"
ls: cannot access '/var/tmp/tz74-home': No such file or directory
ls: cannot access '/var/tmp/tz74-scan': No such file or directory
ls exit=2
```

This is the known answer. The two probe units had been `--collect`ed when they exited (V6).

## Validation

- **V1 — PASS.** A0's readings as required (`### A0`). The gate of contract §5 passed with 7 of 7 anchors and every
  file equal (`## Fingerprints`). The clone was clean (`git status --porcelain` empty).
- **V2 — PASS.** A1's three readings are `600 root root 113 …`, `1` and `1`. The birth time to the second is
  `2026-10-25 07:33:14` UTC (`### A1`).
- **V3 — PASS.** `truncate exit=0`. Then `600 root root 108 2026-10-25 08:18:07.869655000 +0000
  /etc/crypto-auto/credentials/claude-oauth-token`, `length=108 newline_bytes=0 non_empty_lines=1 prefix_ok=1`, and `1`
  (`### B`).
- **V4 — PASS.** The first line starts `False` with the models list `['claude-haiku-4-5-20251001']`, `exit=0 0`. The
  second, after a thirty-second wait, is the same line with `exit=0 0` (`### C`).
- **V5 — PASS.** `1`, `0`, `1`, `2352`, `0`, `6`, `0`, `2399`, `0`. Each count required to be above 0 is, and each
  required `0` is. `present` for `/var/tmp/tz74-home`, `/root/.claude` and `.` (`### D`).
- **V6 — PASS.**

  ```
  $ ls -d /var/tmp/tz74-home /var/tmp/tz74-scan; echo "ls exit=$?"
  ls: cannot access '/var/tmp/tz74-home': No such file or directory
  ls: cannot access '/var/tmp/tz74-scan': No such file or directory
  ls exit=2
  $ systemctl list-units --all --no-legend 'tz74-*' | wc -l
  0
  $ ls -1 /etc/crypto-auto/credentials/ | /usr/bin/grep -c '\.new$'
  0
  ```

  These are the known answers.
- **V7 — PASS as far as a record can read it.** Before the report was added, `git status --porcelain` printed nothing
  (A0). After E, it prints one line, `?? CryptoReports/TZ-74-run-login-cut-report.md`, so the report is the tree's
  only change. The report's own commit is stated under `## Commit`. Its `git show --stat` is that commit's
  outcome, which this record cannot contain (inv. 54).

## Test Results

No repository test was in scope: the TZ changes no repository file, and no bench or selftest was run. The tests of this
TZ are V1–V7 above, and all seven passed.

## Deviations

- **D-1. Each stage's block was handed to `bash` as one `bash -c '…'` argument from the Executor's tool.** The commands
  are the TZ's own, and §6 requires `bash`. Inside D's block and V6's, the TZ's single-quoted strings were written in
  double quotes, because the block's outer quotes were single. The strings are `'^$'`, `'%s\n'`, `'nothing here\n'`,
  `'/var/log/journal/*'`, `'2026-10-25 07:25:00 UTC'`, `date`'s format and `'tz74-*'`. None holds a `$` followed by a
  name, a backquote or a backslash that double quotes would change, so the shell passed the same bytes. `$` closing
  `"^$"` is literal. A0's and A1's blocks also echoed each command as a label before running it. C's probe kept the TZ's
  single quotes, written `'"'"'` inside the outer argument, so it ran character for character.
- **D-2. Readings outside §7's list, none of them a write or a probe:**
  - `type grep` and `type find`, which established the functions §6 warns of;
  - `stat` on `/var/tmp/tz74-home` after A0's `install`;
  - `date -u` beside each stage, and `date +%Z` before D's window;
  - `git ls-remote --heads origin`, for the previous TZ's state;
  - `git show origin/main:` of the five workflows' triggers, before the push (`## CI Execution`);
  - `systemctl is-active crypto-run.service` and the credential file's `stat` again after E, for
    `## Final Repository State`.

  One more count ran on the credential file, after E, over the finished report, which D had scanned only as a draft.
  The report gained D's numbers, E's lines and these sections after D, so the scan was repeated over it:

  ```
  $ /usr/bin/grep -cF -f /etc/crypto-auto/credentials/claude-oauth-token CryptoReports/TZ-74-run-login-cut-report.md
  0
  ```

  The exit code was 1, GNU's for no match. §1 and §6 admit counts as a reading of the file, and this one prints one
  number. After it, only this `0` and this sentence were written into the report.

## Pre-existing Issues

- In this session's shell `grep` and `find` are functions (`### A0`). TZ-73 reported the same of `grep`. A host command
  that relies on GNU's exit codes or output reads otherwise there. This TZ's §6 already requires the full paths.
- The helper of TZ-73 §10 is still defective: it strips cursor movements before matching the token. This TZ did not run
  it and did not repair it (§5). The next mint needs a corrected helper.

## Remaining Risks

- **The cause of the earlier revocations is unmeasured, and this login may be refused again.** The reading is the
  journal's next 401, set against the login's birth at 07:33:14 UTC on 25.10.2026. The file's modified time is now the
  cut's, 08:18:07 UTC, so the birth is kept here and in TZ-73's report.
- Production runs go on the host's 2.1.282 until TZ-72's merge. The probes measured the host's CLI. TZ-72's A3 measures
  the pinned file under the same limits.
- The code the Boss returned in TZ-73 sits in that session's conversation. It is single-use and was consumed at 07:33.
- Both probes ran at the limits of §7 C (`MemoryMax=167772160`, `MemorySwapMax=536870912`) and answered with one
  model. A production run starts two subagents and three models, which these probes do not measure.
- No production run was started (§4). So it has not been measured whether the next scheduled run answers rather than
  ending «Анализ не завершён.». The probes measured only that the login answers.

## Commit

Report, on `main`, message as `## Commit Message` gives it:

```
TZ-74: report — the run's Claude login cut to its 108 characters and probed on the host
```

Contents: `CryptoReports/TZ-74-run-login-cut-report.md`, and nothing else.

## Pull Request

None — report-only TZ; direct push on the CryptoReports/** path (§8).

## CI Execution

No branch exists and no workflow ran for this TZ. The report's path clears every push trigger, read from `origin/main`
before the push:
- `main.yml`'s push trigger is a `paths` allow-list of `main.py` and `.github/workflows/main.yml`.
- `bench.yml` ignores `**.md`.
- `calib.yml` triggers on `claude/**` only.
- `journal.yml` and `backtest_bench.yml` have no push trigger.

## Final Repository State

The checkout the fingerprints were taken against: this worktree (branch
`worktree-bridge-cse_01AnacDwZMjuVVyMMhJUFBe3`) at `81a81c8993c653ce2c790dc3b2e8c67b8ed3c2c3`, equal to `origin/main`
at the last fetch. Its only change is this report, untracked.

The host:
- No `tz74-*` unit, and neither `/var/tmp/tz74-home` nor `/var/tmp/tz74-scan` (V6).
- Nothing was installed, enabled, disabled, started, stopped or restarted.
- `crypto-run.service` read `inactive` before and after the session, and no run was started or requested.
- Nothing was sent to Telegram.
- The credential file is the one path under `/etc/crypto-auto/` this session wrote, with no `.new` beside it:

```
600 root root 108 2026-10-25 08:18:07.869655000 +0000 /etc/crypto-auto/credentials/claude-oauth-token
```

It holds the login minted at 07:33:14 UTC, which both probes found answering (`## Status`).

## Fingerprints

Taken against `origin/main` at `81a81c8993c653ce2c790dc3b2e8c67b8ed3c2c3`, which is also this worktree's checkout.

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — 2797 lines, MD5 `ba303ec6a08414d3bd8e041d15086719`, revision string
`**Revision 2026-10-25-a.**` (map line 17). This equals the TZ header.

**Anchors.** The map's anchor table was cut by structure, inside `## 0. Fingerprint`: every row between the separator
after `| Anchor |` and the first non-table line.

```
awk '/^## 0\. Fingerprint/{z=1} z&&/^\| Anchor \|/{h=1;next} h&&/^\|---/{r=1;next} r&&/^\|/{print;next} r{exit}'
```

The same cut was applied to the TZ's `## 0. Fingerprint required`, both read by `git show origin/main:`. **The map's
table has 7 rows and the TZ's has 7. The two cuts are byte-identical (`cmp exit=0`), and 7 anchors were compared.** Per
anchor, the command was `/usr/bin/grep -oF -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md`. The table gives the first line it
returned and the `-cF` count:

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

**Files** (from `git show origin/main:<path> | wc -l` and `| md5sum`). The map's own `## 0` file table lists the same
four files at the same values.

| File | Lines | MD5 | Required | Result |
|---|---:|---|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | 3799 / `4e71da9b…` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 / `0e3ead8c…` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a…` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b2…` | equal |
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | `**Version 31.**` (line 3) | equal; version 31 |
| `vps/units/crypto-run.service` | 38 | `9355ee94131624ff3fcdafe409183f38` | 38 / `9355ee94…`, enforced | equal |

No file differs, so nothing goes under `## Pre-existing Issues` from the fingerprints.
