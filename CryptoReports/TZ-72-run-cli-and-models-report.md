# Implementation Report — TZ-72

Previous TZ's branch: `tz-71-models-and-markup` was merged into `main` by PR #59 (`328fdf3`). This TZ's precondition
holds, and it builds on a merged base.

## Status

**BLOCKED at A3. §11 is not applied: no branch, no implementation commit, no pull request.** All four probes printed
`True success [] 0 0`. The run's own Claude login was refused before any model ran. Each probe's transcript carries the
same synthetic message: `error=authentication_failed`, «Failed to authenticate: OAuth token revoked. Please log in again
or contact your administrator.» The pinned CLI itself was read correctly at A2: the hash equals the pin and the version
is `2.1.308`. Because the login was refused, A3 measured nothing about the three model ids or the hunter's path. TZ §7
A3: «Any probe not passing leaves §11 out whole (§3): A4, then no branch, the report BLOCKED with the line that decided
it.»

**What unblocks it:** a working Claude login for the run, in `/etc/crypto-auto/credentials/claude-oauth-token`, minted on
the VPS by `claude setup-token` (contract §7 item 6). Then `EXECUTE TZ-72` again, which produces `-report-2.md`. A0, A1
and A2 gave the TZ's known answers, and §11's patch was checked to apply to the current tree. Nothing else stands in the
way that this session could read.

## Inbound Filing

None. The TZ was already at its canonical path, `CryptoTZ/TZ-72-run-cli-and-models.md`, on `origin/main`. It was added
by `ec066f4 Add files via upload`. Nothing was moved or renamed.

## Scope Executed

**Class: branch TZ** (contract §8). `## Scope` names three files outside `CryptoReports/**`: `vps/install.sh`,
`vps/run.py` and `vps/selftest.py`.

- **A0** (the host): passed.
- **A1** (the baseline): passed. The `vps` tree, all §0 pairs and the selftest line equal the TZ's values.
- **A2** (the package): passed. SHA-256 equals the pin, and `--version` prints `2.1.308 (Claude Code)`.
- **A3** (four probes): **all four failed**, and that decided BLOCKED. No probe unit is left.
- **A4** (clean-up): done. `ls -d` exits 2.
- **B1–B2:** not run. TZ §7 A3 sends a failed probe to A4, then to no branch.
- **B3:** this report, then the closing message.

On the host: four transient units ran and were collected. Nothing was installed, enabled, started or restarted, and
nothing was written under `/usr/local/libexec/crypto-auto/`.

## Files Created

- `CryptoReports/TZ-72-run-cli-and-models-report.md` (this report, on `main`).

## Files Modified

None. `vps/install.sh`, `vps/run.py` and `vps/selftest.py` are untouched (§11 left out whole).

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**§11 not applied.**

- **A2's hash:** `356733f185fa988e6bf3aa9a555269fdd167982a2e2a80d3c8a78037bb92ad58`, equal to the pin.
- **A3's four lines**, each followed by `systemd-run` exit **1** and summary `python3` exit 0:
  - probe 1: `True success [] 0 0`
  - probe 2: `True success [] 0 0`
  - probe 3: `True success [] 0 0`
  - probe 4: `True success [] 0 0`
- **Deciding line:** probe 1's `True success [] 0 0`. `is_error` is `True`, and the list names no model, where the pass
  needs `False` and `claude-sonnet-5-5`. Probes 2–4 failed the same way.
- **Why:** the run's Claude login was refused with «OAuth token revoked» (see `### What the probes read` below). No
  request reached a model, so `modelUsage` is empty and the cost is 0.

### Stage A readings

**A0.** On host `vultr`, as root:

```
$ systemctl cat crypto-run.service | grep -nE "^(User=|LoadCredential=claude-oauth-token|MemoryMax=|MemorySwapMax=)"
11:User=cryptorun
22:LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token
34:MemoryMax=167772160
35:MemorySwapMax=536870912
45:MemoryMax=318767104
51:MemorySwapMax=385875968
exit=0
$ systemctl cat crypto-run.service | grep -n "^# /"
1:# /etc/systemd/system/crypto-run.service
41:# /run/systemd/system.control/crypto-run.service.d/50-MemoryMax.conf
47:# /run/systemd/system.control/crypto-run.service.d/50-MemorySwapMax.conf
$ uname -m
x86_64
$ command -v curl tar sha256sum
/usr/bin/curl
/usr/bin/tar
/usr/bin/sha256sum
exit=0
$ df -Pk /usr/local/libexec/crypto-auto /var/tmp
Filesystem     1024-blocks     Used Available Capacity Mounted on
/dev/vda2         30871292 17621564  11847512      60% /
/dev/vda2         30871292 17621564  11847512      60% /
exit=0
$ sha256sum /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
3afe8535c0cc33f0e24f7b25dab7a1727b8b592196f8496a8bc302ba2161eed3  /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe
```

- The four required lines are in the unit file itself (lines 11, 22, 34, 35).
- `systemctl cat` also prints two runtime drop-ins under `/run/systemd/system.control/`: `MemoryMax=318767104` and
  `MemorySwapMax=385875968`. These are the limits `run.py --limits` set at the last run's start (TZ §7 A3: «the run's
  are set at each start by `run.py --limits`»). They are reported here, not acted on.
- 11 847 512 KiB is available on each path, against the 1 048 576 KiB required. Both paths are on one filesystem.
- The host's `claude.exe` hash equals the registry's 2.1.282 build (§2). It is 238 767 288 bytes, dated 2026-09-24
  21:21:34 UTC, and `/usr/bin/claude --version` prints `2.1.282 (Claude Code)`.

**A1.**
- `git fetch --all --prune` → exit 0. `git rev-parse --is-shallow-repository` → `false`.
- `git rev-parse origin/main` → `ec066f4b066baaea3cc8a3ba6cfc42b018fb40fe`.
- `git rev-parse origin/main:vps` → `6c11ac85ad9712477ff1f963e17e65f39e21012f`, equal to the required tree.
- All four `vps` files equal §0's pairs (see `## Fingerprints`).
- `python3 vps/selftest.py` at `origin/main` → exit 0, no stderr. Last line
  `selftest: sections 26 checks 534 failed 0 empty 0`, equal to the Architect's reading.

**A2.** The commands as the TZ writes them, run as root:

```
$ install -d -m 0755 /var/tmp/tz72-cli
exit=0
$ curl -fsS -o /var/tmp/tz72-cli/cli.tgz https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.308.tgz
exit=0
$ tar --no-same-owner -xzf /var/tmp/tz72-cli/cli.tgz -C /var/tmp/tz72-cli package/claude
exit=0
$ chmod 0755 /var/tmp/tz72-cli/package /var/tmp/tz72-cli/package/claude
exit=0
$ sha256sum /var/tmp/tz72-cli/package/claude
356733f185fa988e6bf3aa9a555269fdd167982a2e2a80d3c8a78037bb92ad58  /var/tmp/tz72-cli/package/claude
exit=0
$ install -d -m 0700 -o cryptorun -g cryptorun /var/tmp/tz72-home
exit=0
$ runuser -u cryptorun -- env HOME=/var/tmp/tz72-home /var/tmp/tz72-cli/package/claude --version
2.1.308 (Claude Code)
exit=0
```

`stat -c %s` measured the file at 292 232 560 bytes and the tarball at 132 044 055 bytes. Both match §2 and §7 A0.

**A3.** The four commands as run. Only `<n>`, `<model>`, `<flags>`, `<turns>` and `<prompt>` were filled in, from TZ
§7's table. Probe 1:

```
systemd-run --wait --pipe --collect --quiet --unit=tz72-probe-1 \
  -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/tmp/tz72-home \
  -p Environment=HOME=/var/tmp/tz72-home -p Environment=DISABLE_AUTOUPDATER=1 \
  -p Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 -p Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
  -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
  -p Environment=ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5-5 \
  -p Environment=ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5 \
  -p Environment=ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-5-5 \
  -p MemoryMax=167772160 -p MemorySwapMax=536870912 \
  -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
  /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /var/tmp/tz72-cli/package/claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model sonnet' \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), sorted((d.get("modelUsage") or {}).keys()), len(d.get("permission_denials") or []), d.get("total_cost_usd"))'
```

Probes 2–4 use the same command with `--unit=tz72-probe-<n>`. Only the `/bin/sh -c` line differs:

- probe 2:
  ```
  /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /var/tmp/tz72-cli/package/claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model haiku' \
  ```
- probe 3:
  ```
  /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /var/tmp/tz72-cli/package/claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model claude-opus-5-5 --effort high' \
  ```
- probe 4:
  ```
  /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /var/tmp/tz72-cli/package/claude -p "Call the Agent tool exactly once, with model sonnet, and ask the subagent to read https://example.com with WebFetch and reply with the title of that page. Then reply with that title alone." --output-format json --max-turns 5 --model claude-opus-5-5 --effort high --allowedTools "Bash Read Write Edit Glob Grep WebSearch WebFetch"' \
  ```

Every printed line and exit code (`PIPESTATUS`):

| n | Printed | `systemd-run` | `python3` | Pass needs | Result |
|---|---|---:|---:|---|---|
| 1 | `True success [] 0 0` | 1 | 0 | `False`, list naming `claude-sonnet-5-5`, `0` | **fail** |
| 2 | `True success [] 0 0` | 1 | 0 | `False`, list naming `claude-haiku-5-5`, `0` | **fail** |
| 3 | `True success [] 0 0` | 1 | 0 | `False`, list naming `claude-opus-5-5`, `0` | **fail** |
| 4 | `True success [] 0 0` | 1 | 0 | `False`, list naming `claude-opus-5-5` and `claude-sonnet-5-5`, `0` | **fail** |

- Each probe ran once. Probe 4 was not run a second time (see `## Deviations`).
- Afterwards, `systemctl list-units --all 'tz72-probe-*'` printed `0 loaded units listed.` (exit 0). At the end of the
  session, `systemctl list-units --all --no-legend 'tz72-probe-*' | wc -l` printed `0`.

### What the probes read

**These readings go beyond §7; see `## Deviations`.** The summary line says only that every probe failed. To name the
obstacle, I read the one file each probe left in its scratch home before A4 removed it.

The scratch home held `.claude.json`, one backup of it, and four transcripts under
`.claude/projects/-var-tmp-tz72-home/`, one per probe in run order. Before anything was printed, each of those six files
was checked for the login's value by a count, with the file as the pattern:
`grep -cF -f /etc/crypto-auto/credentials/claude-oauth-token <file>`. Every count was `0`. The check itself was proven
first:
- the credential file holds one pattern line and no empty one (so the pattern cannot match every line);
- the same command with a dummy pattern counted `1` on a file holding that pattern, and `0` on a file without it.

A script then printed, per transcript:
- the count of entries by type;
- the user prompt (first 200 characters);
- for each `system` and `assistant` entry, the fields `subtype`/`level`, `model`, `isApiErrorMessage`, `error` and the
  text (first 400 characters).

Its output was counted for the login the same way (`0`) before it was read. For every probe it read:

```
user prompt='Reply with the one word: ok'          (probe 4: its own prompt)
system subtype=api_error level=error content='None'
system subtype=api_error level=error content='None'
assistant model=<synthetic> isApiErrorMessage=True error=authentication_failed text='Failed to authenticate: OAuth token revoked. Please log in again or contact your administrator.'
```

The CLI made two API requests per probe (`api-request: 2`), and each came back as an error. The final message is
synthetic: the CLI wrote it, not a model.

**The production run on the same login, read from the journal.** I ran
`journalctl -u crypto-run.service --since "2026-10-20" -o short-iso --no-pager`, kept only the start, end and summary
lines (20 lines, login count `0`), and read them:

| Started (UTC) | CLI | `claude_exit` | `is_error` | `api_error_status` | `models=` |
|---|---|---:|---|---|---|
| 2026-10-21 12:04:24 | 2.1.282 | 1 | true | 401 | `-` |
| 2026-10-21 12:20:16 | 2.1.282 | 0 | false | `-` | `claude-haiku-4-5-20251001,claude-opus-5-5,claude-sonnet-5` |
| 2026-10-24 07:34:19 | 2.1.282 | 1 | true | 401 | `-` |
| 2026-10-24 07:58:47 | 2.1.282 | 0 | false | `-` | the same three |
| 2026-10-24 14:16:32 | 2.1.282 | 0 | false | `-` | the same three |

The CLI column comes from two readings. `run.py` at `origin/main` line 61 starts `CLAUDE = ["claude", …`, and under the
unit's `PATH` (`env PATH=<that PATH> sh -c 'command -v claude; readlink -f "$(command -v claude)"'`) `claude` resolves to
`/usr/bin/claude` → `/usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe`. That is the 2.1.282 file A0 hashed,
dated 24.09.

I also ran `stat` on the login file, reading only its metadata:
`109 bytes, mode 600, owner root, modified 2026-10-24 07:58:12.696914869 +0000`.

This shows the login was replaced between the 401 at 07:34 and the run that succeeded at 07:58:47. The login minted
then answered twice on 24.10, at 07:58 and 14:16. By A3, on 25.10 at about 06:08 UTC, it was refused as revoked.

**What this establishes, and what it does not:**
- The refusal comes from the authentication step: the CLI wrote the message itself, and no model was billed.
- The journal shows the run's login of the day refused with 401 on 2.1.282 on two earlier days. On 24.10 the refusal
  was followed by a success once a new login file was in place.
- **I did not measure whether 2.1.282 is refused with this login today.** That would be a probe §5 does not authorise
  («No other version, model id or probe than §7's»).

## Validation

V1–V5 and V7 test §11's patch on the branch. TZ §7 A3 sends a failed probe to A4, then no branch, so **none of them was
run. Each is recorded here as not run, for that reason. Under contract §9 an item that cannot be run fails, and these
are counted as failed.**

- **V1** `py_compile` / `bash -n`: not run (no patched files).
- **V2** selftest on the branch: not run. The baseline from A1 stands: `sections 26 checks 534 failed 0 empty 0`.
- **V3** controls C1–C5: not run (no committed branch).
- **V4** patched lines and MD5, and `HEAD:vps`: not run (no branch).
- **V5** `git diff --stat origin/main...HEAD`: not run (no branch).
- **V6:** done.
  - A2's seven commands all exited 0. The hash and the version are as required.
  - A3's four lines and their exit codes are above, and the unit listing is empty.
  - A4:
    ```
    $ rm -rf /var/tmp/tz72-cli /var/tmp/tz72-home
    exit=0
    $ ls -d /var/tmp/tz72-cli /var/tmp/tz72-home
    ls: cannot access '/var/tmp/tz72-cli': No such file or directory
    ls: cannot access '/var/tmp/tz72-home': No such file or directory
    exit=2
    ```
- **V7** `install.sh --dry-run` from the branch: not run (no branch). `/usr/local/libexec/crypto-auto/` holds only
  `deploy.sh`, as it did before A2. There is no `claude-code` directory.
- **No regression:** nothing was changed, so nothing could regress.

**Readings of the patch, which write nothing.** §11 was cut from the TZ with
`awk '/^````diff$/{f=1;next} /^````$/{f=0} f' CryptoTZ/TZ-72-run-cli-and-models.md` (441 lines). Its MD5 is
`fac7b81bbb9a011299ea6a460319f99f`, equal to §11's. `git apply --check --verbose` against `origin/main`'s tree printed
`Checking patch vps/install.sh...`, `Checking patch vps/run.py...` and `Checking patch vps/selftest.py...`, and exited 0.
Afterwards `git status --porcelain` printed nothing. So the patch applies to the bytes it was written for, but it was
not applied.

## Test Results

| Run | Where | Result |
|---|---|---|
| selftest at `origin/main` (A1) | VPS, local | sections 26 checks 534 failed 0 empty 0, exit 0 |
| A2 hash and version | VPS, local | pin matched, `2.1.308 (Claude Code)` |
| A3 probes 1–4 | VPS, transient units as `cryptorun` | all `True success [] 0 0`, `systemd-run` exit 1. **Fail** |
| `git apply --check` of §11 | VPS, local, nothing applied | exit 0 |
| V1–V5, V7 | — | not run (no branch) |

## Deviations

- **The obstacle was read from outside the summary line.** I read the probes' transcripts in the scratch home, the
  production run's journal, and the login file's metadata, as described in `### What the probes read`. §7 names none of
  these readings. TZ §6 binds A3's output: «one summary line per probe, built from the JSON result — never the result
  whole». I kept to that: the summary lines are exactly the TZ's.
  - The added readings are all reads. Each extract printed bounded named fields only, and was checked by a login count
    before it was read.
  - They were run because contract §12 asks a BLOCKED report for «the precise obstacle and what would unblock it»,
    which `True success [] 0 0` does not name.
  - No extra probe was run, and the CLI was not executed again.
- **Probe 4 was not run a second time.** TZ §7 A3 allows a second run «where the first names no `claude-sonnet-5-5`».
  Its first run names none, so the letter would allow it. But its failure is a refused login, the same as probes 1–3,
  which had already decided BLOCKED. A second run could only repeat that line, so it was not run.
- **V1–V5 and V7 were not run**, because TZ §7 A3 sends a failed probe to no branch. Contract §9 counts each as failed,
  so the work is BLOCKED, not PARTIAL.

## Pre-existing Issues

- **The run's Claude login is refused as revoked, and this is not the first refusal of the run's login.** The journal
  shows 401 refusals on 21.10 and 24.10. On 24.10 a new login file is dated 24 minutes after the refusal, just before
  the run that succeeded. The login minted on 24.10 answered twice that day and is refused on 25.10. Why logins minted by
  `claude setup-token` stop being accepted is not readable from this host. **Nothing was acted on, and no login was
  minted or changed** (contract §7 item 6: the login is minted only while the Boss approves in his own browser).
- `systemctl cat crypto-run.service` prints two runtime drop-ins beside the unit file's limits (A0). They are what
  `run.py --limits` sets at a run's start, and they disappear at reboot. Reported because A0 names the unit file's
  values, which `systemctl cat` prints first.
- The TZ header says it was written against the `vps` tree `6c11ac85…` once PR #59 is merged. At execution
  `origin/main` was `ec066f4`, and the `vps` tree and every fingerprinted file equal the TZ's values.

## Remaining Risks

- **Until the login is replaced, every production run will fail at authentication.** `crypto-run.service` hands the
  same file to the host's 2.1.282. If the server refuses the login, as the 401 lines of 21.10 and 24.10 show it has
  before, that run ends with the notice «Анализ не завершён.». This was not measured today (see
  `### What the probes read`).
- **On a re-run, A3's ids and the hunter's path are still unmeasured.** This session established only that the 2.1.308
  file is the pinned one and runs under `cryptorun` (A2). It did not establish that `claude-sonnet-5-5`,
  `claude-haiku-5-5` and `claude-opus-5-5` answer through it on this host.
- After a later merge, the risks TZ §10 names stand unchanged:
  - the deployer's first tick fetches the package from npm's registry, and a failure is told once and retried each tick;
  - the CLI moves twenty-six releases at once, so the first run after the merge is its first full session, read through
    the journal's `models=`, `unpinned=` and `memory_peak=` lines;
  - the run's memory limits are set at each start, not fixed like the probes'.

## Commit

No implementation commit exists, and no branch was opened.

This report's commit goes to `main` on the `CryptoReports/**` direct-push path (contract §8). Its message:

```
TZ-72: report — BLOCKED at A3, the run's Claude login refused as revoked; §11 not applied
```

Contents: `CryptoReports/TZ-72-run-cli-and-models-report.md` only.

## Pull Request

None. By class this is a branch TZ, but TZ §7 A3 stopped it before any branch («A4, then no branch»). No implementation
commit, branch or pull request exists. The report-only fixed line is not used, because it would assert a class this TZ
does not have.

## CI Execution

No workflow ran on a runner for this task, and no branch was pushed. Before the report's push, every workflow's trigger
was read:
- `bench.yml`'s `push` carries `'**.md'` under `paths-ignore`.
- `main.yml`'s `push` is a `paths` allow-list of exactly `main.py` and `.github/workflows/main.yml`, on `main`.
- `calib.yml`'s `push` fires only on `claude/**` branches, for two named paths.
- `journal.yml` runs on a schedule and `workflow_dispatch`; `backtest_bench.yml` on `workflow_dispatch` only.

Every selftest and probe reading in this report is a local run on the VPS.

## Final Repository State

- This session leaves its checkout at `origin/main`, `ec066f4b066baaea3cc8a3ba6cfc42b018fb40fe`, the commit the
  fingerprints were taken against. Before this report was added, the working tree was clean:
  `git status --porcelain --ignored` printed nothing, after A1's `vps/__pycache__/` was removed.
- No `tz-72` branch exists, and `git ls-remote --heads origin 'tz-72*'` printed nothing at the start.
- On the host:
  - no `tz72-probe-*` unit exists;
  - `/var/tmp/tz72-cli` and `/var/tmp/tz72-home` are gone;
  - `/usr/local/libexec/crypto-auto/` holds only `deploy.sh`, which predates this session;
  - `/usr/bin/claude` was read, not touched;
  - nothing was installed, enabled, started or restarted;
  - the login file was read only by `grep -c`, `stat` and the probes' `LoadCredential=`.

## Fingerprints

Each file was measured against `origin/main` at `ec066f4b066baaea3cc8a3ba6cfc42b018fb40fe` with
`git show origin/main:<file> | wc -l` and `| md5sum`.

**Map.** `SYSTEM-MAP-CRYPTOCALCUL.md`: 2797 lines, MD5 `ba303ec6a08414d3bd8e041d15086719`, equal to the TZ's reported
pair. Revision string: `grep -noF -- '**Revision 2026-10-25-a.**' map.md` returned `17:**Revision 2026-10-25-a.**`
(and line 78, the table row). This equals the required one.

**Anchors.**
- **Cutting the table.** The list was cut from the map's own table by its structure: inside `## 0`, every line after the
  separator that follows the header `| Anchor | Exact string that must be present |` (header at line 76, separator at
  line 77), up to the first line not opening with `|`. Command:
  `awk '/^## 0\. Fingerprint/{z=1} z&&/^## 1\./{exit} z&&/^\| Anchor \|/{h=1;next} h&&/^\|---/{t=1;next} t&&/^\|/{print;next} t{exit}' map.md`.
  **The table has 7 rows, and 7 were compared.**
- **The TZ header.** The same cut of the TZ header's table gave 7 rows, and `diff` printed nothing: the header quotes
  every row character for character.
- **Matching.** Each anchor was taken from its row's backticks and matched with `grep -noF -- '<anchor>' map.md`. The
  text it returned is below. Every anchor matches twice: once in the table row and once in the heading or text it names.

| # | Anchor | Matched text returned | Lines |
|---|---|---|---|
| 1 | revision | `**Revision 2026-10-25-a.**` | 17, 78 |
| 2 | direction engine | `### 3.12 Direction engine — veto cascade` | 79, 1048 |
| 3 | catalyst registry | `### 3.15 Catalyst registry` | 80, 1438 |
| 4 | exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | 81, 1535 |
| 5 | analytical engine | `## 11. Analytical engine` | 82, 2529 |
| 6 | squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 83, 1702 |
| 7 | newest invariant | `72. **A write that fails leaves this run's product or nothing` | 84, 2244 |

The map's file table was cut the same way (header at line 88, separator at line 89). It has 4 rows, the TZ header's has
4, and `diff` printed nothing.

**The map's `## 0` files, at the required revision:**

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**The files TZ §0's gate adds:**

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | equal. Version line `**Version 31.**` (line 3) |
| `vps/install.sh` | 272 | `57f874a6ea816abeaad7f1fd3cec3972` | equal |
| `vps/run.py` | 364 | `988f6f4955072f6429def95d3957d974` | equal |
| `vps/selftest.py` | 2265 | `2fbba2579fdebd452e185ddf00a719bc` | equal |
| `vps/bot.py` | 496 | `2bf99362c01bf0fc638c7352c64aea91` | equal |

`git rev-parse origin/main:vps` → `6c11ac85ad9712477ff1f963e17e65f39e21012f`, equal.
