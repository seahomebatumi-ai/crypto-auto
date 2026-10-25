# TZ-72 — The run's own Claude Code, pinned by version and hash and installed by the deployer; the hunter and the page reader on the current models

**Canonical filename:** `CryptoTZ/TZ-72-run-cli-and-models.md`
**Report:** `CryptoReports/TZ-72-run-cli-and-models-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine**, because A3 runs the pinned CLI under the run's own Claude login, which lives there.
**Class:** branch TZ (contract §8) — it modifies three files under `vps/**` and nothing else.
**Branch:** `tz-72-run-cli-and-models`, from `origin/main` · **Model:** Opus
**Trigger:** `EXECUTE TZ-72`, with nothing under it: no credential arrives.
**Precondition:** pull request #59 (TZ-71) merged. A1 stops BLOCKED on any other `vps` tree.
**Written against:** contract v31, map `2026-10-25-a` uploaded with this TZ, and the `vps` tree
`6c11ac85ad9712477ff1f963e17e65f39e21012f` — TZ-71's branch at `f8a4f14`, which is `main`'s tree once pull request #59
is merged — read by the Architect from the repository on 24.10.2026, where §11's patch was built, applied and run through
the selftest and the five controls of V3.

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
| `vps/install.sh` | 272 | `57f874a6ea816abeaad7f1fd3cec3972` | equal, or A1 stops: §11's patch is written against these bytes |
| `vps/run.py` | 364 | `988f6f4955072f6429def95d3957d974` | equal, or A1 stops, on the same ground |
| `vps/selftest.py` | 2265 | `2fbba2579fdebd452e185ddf00a719bc` | equal, or A1 stops, on the same ground — TZ-71's version |
| `vps/bot.py` | 496 | `2bf99362c01bf0fc638c7352c64aea91` | equal, or A1 stops: TZ-71's version, which this TZ does not touch |

The map itself: 2797 lines, MD5 `ba303ec6a08414d3bd8e041d15086719` — reported, not enforced.

---

## 1. Credentials

**None arrives.** A3 is the one step that touches a credential: the run's own Claude login,
`/etc/crypto-auto/credentials/claude-oauth-token`, reaches each of A3's four transient units as a systemd credential
(`LoadCredential=`) under the run's own user, and is read inside the unit into the environment of the CLI child alone.
**No value is printed, logged, committed or quoted** — in the report, a commit, a check's label or the chat — and no
other credential is read: neither the deploy key, nor the bot's token, nor any other. Nothing is sent to Telegram from
the branch.

---

## 2. Contract, map and outside text this TZ obeys

> **Contract §7 item 15:** «Code under `vps/` runs on the VPS only from `main`: the deployer fast-forwards its own
> clone and installs what changed, and nothing else installs anything. An implementation session never enables, starts
> or leaves running a persistent unit, timer or service from a branch; it may start TRANSIENT units from its branch for a
> measurement its TZ names, and its report proves none is left behind.» — the run's CLI becomes a thing the deployer
> installs from the repository. A2's download is a measurement's material: it lives under `/var/tmp`, is removed by A4,
> and is never put where the run looks for its CLI.

> **Contract §7 item 6:** «A unit that runs a model session runs as its own unprivileged user, never root, and holds
> exactly two credentials: its own Claude login and the deploy key» — A3's units hold one of the two, the login, and run
> as `cryptorun`, the run unit's own user (`vps/units/crypto-run.service`, `User=cryptorun`).

> **Contract §9:** «Any TZ touching CI requires a **negative test**: force a real failure in the working tree, confirm
> the job turns red, revert, confirm the tree is clean. A gate never proven to fail is not a gate.» — this TZ touches no
> workflow; V3 holds the selftest, which the deployer runs before it installs anything, to the same standard.

> **Map §10 row «Two model pins lag a generation» (`2026-10-25-a`):** «**The defect is the CLI's place, not its
> age:** the run calls the host's `/usr/bin/claude`, an npm global install of 24.09.2026 that no file in the repository
> declares, that every other session on the host shares, and that no merge can move — so this row named two ids as
> current without a reading of the program that has to know them. TZ-72 gives the run its own CLI,
> `/usr/local/libexec/crypto-auto/claude-code/2.1.308/claude`, pinned by version and by the SHA-256 of its one file in
> `vps/install.sh`, fetched and checked by the deployer and by nothing else, and moves the two pins with it.»

> **Claude Code's changelog (`anthropics/claude-code`, `CHANGELOG.md`, read 24.10.2026):** 2.1.284 — «Added Claude
> Sonnet 5.5 (`claude-sonnet-5-5`), now the default Sonnet model on the Anthropic API»; 2.1.293 — «Added Claude Haiku
> 5.5 (`claude-haiku-5-5`), now the default Haiku model on the Anthropic API». **npm's registry, read 24.10.2026:**
> dist-tags `stable` 2.1.308 (published 22.10.2026), `latest` 2.1.310. `@anthropic-ai/claude-code-linux-x64@2.1.308` is
> one program file, `package/claude`, 292 232 560 bytes, SHA-256
> `356733f185fa988e6bf3aa9a555269fdd167982a2e2a80d3c8a78037bb92ad58`, in a tarball whose SHA-512 equals the registry's
> `dist.integrity`. The same package at 2.1.282 is 238 767 288 bytes — the size TZ-53 read of the VPS's `claude.exe` —
> SHA-256 `3afe8535c0cc33f0e24f7b25dab7a1727b8b592196f8496a8bc302ba2161eed3`.

> **The Architect's readings of 24 and 25.10.2026**, each file run from an empty home outside any npm tree: with the
> pin for its alias set, the 2.1.282 file printed
> `[claude-code:unrecognized_model] {"model":"claude-sonnet-5-5","query_source":"sdk"}`, and the same for
> `claude-haiku-5-5` — TZ-71's A2 line, verbatim — while the 2.1.308 file printed `False success ['claude-sonnet-5-5'] ok`
> and `False success ['claude-haiku-5-5'] ok`; with all three pins set, as in A3, the 2.1.308 file printed
> `False success ['claude-opus-5-5'] 0` for probe 3 and
> `False success ['claude-haiku-5-5', 'claude-opus-5-5', 'claude-sonnet-5-5'] 0` for probe 4, which returned
> `Example Domain` in two turns — the subagent on the hunter's pin and the page it read through the page reader's;
> `--version` printed `2.1.308 (Claude Code)`.

---

## 3. What is built, and why

**A — the run's own CLI.** `vps/install.sh` pins `CLI_VERSION=2.1.308` and `CLI_SHA256` (§2), and its default mode —
after the selftest and the provisioning, before any unit is verified — calls `install_cli`. A file at
`/usr/local/libexec/crypto-auto/claude-code/2.1.308/claude` that hashes to the pin stays; any other file there is
removed first, so no run starts it; npm's linux-x64 tarball is fetched into a directory beside the target, its one file
is hashed, and only a file that hashed to the pin is renamed into place; every other version under `claude-code/` then
goes. A CLI not in place stops the install before any unit moves: the deployer tells the Boss once (its notice S10) and
tries again on every tick. `--dry-run` prints whether the pinned CLI is in place. `vps/run.py` names the CLI by that
absolute path, and a CLI that is not executable is a session that never starts — the notice «Анализ не завершён.», as
for a missing login, never a traceback. **Why:** TZ-71's A2 read both new ids refused by the run's CLI, which is the
host's `/usr/bin/claude` at 2.1.282 — an npm global install of 24.09.2026 that no file declares and every session on
the host shares. Merge is deployment (contract §7 item 15), so the program the run executes must be one the repository
names, the deployer installs and the selftest holds; a version string alone does not say which bytes run, so the pin is
the hash of the one file. `/usr/bin/claude` is not touched: other sessions on the host run on it.

**B — the two pins.** `vps/run.py`: `HUNTER_MODEL` `claude-sonnet-5` → `claude-sonnet-5-5`, `HELPER_MODEL`
`claude-haiku-4-5-20251001` → `claude-haiku-5-5` — TZ-71's part A, now on a CLI that knows both, each read answering on
this host through the pinned file first (A3). `PINS`, `MODEL` and `EFFORT` are not touched.

**One change, all or nothing.** The CLI is what makes the pins work, and the pins are why the CLI moves now: §11's
patch is applied whole where A2 and A3 read as §7 requires, and not at all otherwise.

---

## 4. Scope

### Files to Create
- `CryptoReports/TZ-72-run-cli-and-models-report.md` — on `main` (contract §8).

### Files to Modify
- `vps/install.sh` — §11's hunks: the header, `CLI_VERSION`, `CLI_SHA256`, `CLI_URL`, `cli_in_place`, `install_cli`,
  the `--dry-run` lines and the default mode's call.
- `vps/run.py` — §11's hunks: the two pins, `CLI_VERSION`, `CLI`, the first element of `CLAUDE`, and the guard after
  the login is read.
- `vps/selftest.py` — §11's hunks: the module docstring and three imports; section O's pins and its stub at the head of
  `run.CLAUDE`; the same stub in sections S and U; `stub_cli`; section AA with its entry in `SECTIONS`.

### Files to Delete
- None.

### On the VPS, outside the repository — authorised, and nothing else
- A2's download into `/var/tmp/tz72-cli/` and A3's scratch home `/var/tmp/tz72-home/`, both removed by A4; A3's four
  probes, each a transient unit collected when it exits; V7's `--dry-run`, which changes nothing. **Nothing is
  installed, enabled, started or restarted, and nothing is written under `/usr/local/libexec/crypto-auto/`:** the
  deployer installs the merge, the CLI with it (contract §7 item 15).

### On `main`
- The report only.

---

## 5. What this TZ does not decide and does not build

- No methodology text: `ANALYST-INSTRUCTIONS.md` is the Architect's, and no TZ writes it (contract §7 item 14).
- No change to `MODEL`, `EFFORT`, the sheriff, any unit file, `vps/deploy.sh`, `vps/bot.py`, or anything `run.py` does
  but the changes of §4.
- `/usr/bin/claude` and the npm global install behind it are not touched — A0 reads one hash of it and nothing else.
- No other version, model id or probe than §7's.
- No message is sent to Telegram from the branch, and the bot's token is not read.

---

## 6. Rules — binding in every stage

- **The patch of §11 is the implementation.** Apply it as it stands; a hunk that does not apply, or a validation item
  that fails with it applied, is reported — never repaired by a change of your own design (contract §6).
- **Minimal diff:** three files, §11's hunks and nothing else (V5).
- **No credential printed** (§1). A3 prints one summary line per probe, built from the JSON result — never the result
  whole, and never the environment.
- **No probe touches the run's home.** A3's units run with `HOME=/var/tmp/tz72-home`: a newer CLI may rewrite the
  settings it finds, and `/var/lib/cryptorun/.claude` belongs to the production CLI until the merge.
- **Nothing persistent from the branch** (contract §7 item 15); the report proves every probe unit gone and both scratch
  directories removed (V6).
- **The selftest is never edited to make it pass** (contract §7 item 2): sections O, S and U move only where the run's
  CLI and pins move, and nothing else of any section changes.

---

## 7. Stage A — readings, no writes to the repository

- **A0. The host.** `systemctl cat crypto-run.service` prints `User=cryptorun`, the line
  `LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token`, `MemoryMax=167772160` and
  `MemorySwapMax=536870912`; `uname -m` prints `x86_64`; `command -v curl tar sha256sum` prints three paths;
  `df -Pk /usr/local/libexec/crypto-auto /var/tmp` shows at least 1 048 576 KiB available on each — A2 and the
  deployer's first tick each need about 425 MB there — the 132 MB tarball beside its 292 MB file. Any of these not so → BLOCKED.
  `sha256sum /usr/lib/node_modules/@anthropic-ai/claude-code/bin/claude.exe` is recorded: the registry's linux-x64
  build of 2.1.282 is `3afe8535c0cc33f0e24f7b25dab7a1727b8b592196f8496a8bc302ba2161eed3` (§2); another value is
  reported and decides nothing by itself — A3 decides.
- **A1. The baseline.** `git fetch --all --prune`; the fingerprints of §0 at `origin/main`, and
  `git rev-parse origin/main:vps` equal to `6c11ac85ad9712477ff1f963e17e65f39e21012f`. Another `vps` tree, or another
  value for any of §0's four `vps` files → STOP, BLOCKED, the found values in the report: §11 is written against these
  bytes, and a tree without TZ-71's means pull request #59 is not merged. `python3 vps/selftest.py` at `origin/main`
  prints its last line `selftest: sections 26 checks 534 failed 0 empty 0` (the Architect's reading of that tree,
  24.10.2026); another line is recorded and reported, and decides nothing by itself.
- **A2. The package, read on this host.**

  ```
  install -d -m 0755 /var/tmp/tz72-cli
  curl -fsS -o /var/tmp/tz72-cli/cli.tgz https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.308.tgz
  tar --no-same-owner -xzf /var/tmp/tz72-cli/cli.tgz -C /var/tmp/tz72-cli package/claude
  chmod 0755 /var/tmp/tz72-cli/package /var/tmp/tz72-cli/package/claude
  sha256sum /var/tmp/tz72-cli/package/claude
  install -d -m 0700 -o cryptorun -g cryptorun /var/tmp/tz72-home
  runuser -u cryptorun -- env HOME=/var/tmp/tz72-home /var/tmp/tz72-cli/package/claude --version
  ```

  The hash prints `356733f185fa988e6bf3aa9a555269fdd167982a2e2a80d3c8a78037bb92ad58` and the version
  `2.1.308 (Claude Code)`. Another hash → A4, then STOP, BLOCKED: nothing runs a file the pin refuses, and §11 would
  refuse it too.
- **A3. The three ids and the hunter's path, read on this host through that file.** Four transient units, each run
  once:

  ```
  systemd-run --wait --pipe --collect --quiet --unit=tz72-probe-<n> \
    -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/tmp/tz72-home \
    -p Environment=HOME=/var/tmp/tz72-home -p Environment=DISABLE_AUTOUPDATER=1 \
    -p Environment=CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 -p Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1 \
    -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
    -p Environment=ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5-5 \
    -p Environment=ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5 \
    -p Environment=ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-5-5 \
    -p MemoryMax=167772160 -p MemorySwapMax=536870912 \
    -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
    /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec /var/tmp/tz72-cli/package/claude -p "<prompt>" --output-format json --max-turns <turns> --model <model> <flags>' \
    | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), sorted((d.get("modelUsage") or {}).keys()), len(d.get("permission_denials") or []), d.get("total_cost_usd"))'
  ```

  | n | `<model>` | `<flags>` | `<turns>` | `<prompt>` | Passes where its line prints |
  |---|---|---|---|---|---|
  | 1 | `sonnet` | none | 1 | `Reply with the one word: ok` | `False`, a subtype, a list naming `claude-sonnet-5-5`, `0` |
  | 2 | `haiku` | none | 1 | the same | `False`, a subtype, a list naming `claude-haiku-5-5`, `0` |
  | 3 | `claude-opus-5-5` | `--effort high` | 1 | the same | `False`, a subtype, a list naming `claude-opus-5-5`, `0` |
  | 4 | `claude-opus-5-5` | `--effort high --allowedTools "Bash Read Write Edit Glob Grep WebSearch WebFetch"` | 5 | `Call the Agent tool exactly once, with model sonnet, and ask the subagent to read https://example.com with WebFetch and reply with the title of that page. Then reply with that title alone.` | `False`, a subtype, a list naming `claude-opus-5-5` and `claude-sonnet-5-5`, `0` |

  In every probe each id the list names is one of the three pins. *Derived: the Architect's runs of the four prompts on
  the same file with the same pins (§2); the memory limits and the run's login are what only this host adds.* Probe 4
  may run a second time where the first names no `claude-sonnet-5-5`; the report carries both lines. The report carries the four commands as run, every printed
  line and every exit code, and `systemctl list-units --all 'tz72-probe-*'` printing no unit afterwards. **Any probe
  not passing leaves §11 out whole** (§3): A4, then no branch, the report BLOCKED with the line that decided it. The
  probes' memory limits are the unit file's own; the run's are set at each start by `run.py --limits`, and the first
  run's journal reads them (§10).
- **A4. Clean-up, whatever A2 and A3 read.** `rm -rf /var/tmp/tz72-cli /var/tmp/tz72-home`, then
  `ls -d /var/tmp/tz72-cli /var/tmp/tz72-home` exits 2.

---

## 8. Stage B — the code, on the branch

- **B1.** Branch `tz-72-run-cli-and-models` from `origin/main`; `git apply` §11's patch.
- **B2.** Validation (§9), then one implementation commit with the message of `## Commit Message`, the branch pushed, a
  pull request opened — or contract §8's fallback.
- **B3.** The report on `main` (§10), then the closing message (contract §11).

---

## 9. Validation

Every item names its command and its known answer; each answer was derived where it says.

- **V1.** `python3 -m py_compile vps/run.py vps/bot.py vps/selftest.py` → exit 0; `bash -n vps/install.sh` → exit 0.
- **V2.** `python3 vps/selftest.py` → exit 0 and the last line `selftest: sections 27 checks 560 failed 0 empty 0`;
  section O `checks 33 failed 0`, section S `checks 35 failed 0`, section U `checks 18 failed 0`, section Z
  `checks 23 failed 0`, section AA `checks 26 failed 0`. *Derived: the Architect's run of §11's patch on the tree
  `6c11ac85…`, 24.10.2026.*
- **V3. Five controls, each on the committed branch, each reverted before the next** — apply, confirm the file changed,
  run the selftest, record the section's line and the exit code, then `git checkout -- vps/` and
  `git status --porcelain` printing nothing:
  - C1 `sed -i 's/^CLI_VERSION=2.1.308$/CLI_VERSION=2.1.307/' vps/install.sh` → `section AA: checks 26 failed 1`,
    exit non-zero;
  - C2 `sed -i 's/^    if \[ "$got" != "$CLI_SHA256" \]; then$/    if false; then/' vps/install.sh` →
    `section AA: checks 26 failed 2`, exit non-zero;
  - C3 `sed -i 's/^    if env is not None and not os.access(CLAUDE\[0\], os.X_OK):$/    if False:/' vps/run.py` →
    `section AA: checks 21 failed 1` and the stderr line `FAIL section AA raised FileNotFoundError: …`, exit non-zero;
  - C4 `sed -i 's/^HUNTER_MODEL = "claude-sonnet-5-5"$/HUNTER_MODEL = "claude-sonnet-5"/' vps/run.py` →
    `section O: checks 33 failed 2`, exit non-zero;
  - C5 `sed -i 's/^    rm -f -- "$dir\/claude"$/    :/' vps/install.sh` → `section AA: checks 26 failed 3`, exit non-zero.

  *Derived: the Architect's runs of the five controls on the patched tree, 24.10.2026.* A control that changes nothing,
  or leaves the selftest green, fails this item.
- **V4.** The files after B1, lines and MD5: `vps/install.sh` 336 `6abc43fb0ba6620a123cf732ef761466`, `vps/run.py` 375
  `36dc8f3bf39b44168674677c85aecd44`, `vps/selftest.py` 2430 `1f207b2dce474439924b1ef22c82e918`, `vps/bot.py` as in §0;
  `git rev-parse HEAD:vps` → `dce795d17056cae7a22ee57dd0daa24dd4b3f808`. *Derived: the Architect's build.* A different
  value is a finding: the patch applied differently.
- **V5.** `git diff --stat origin/main...HEAD` names `vps/install.sh`, `vps/run.py` and `vps/selftest.py` and nothing
  else.
- **V6.** A2's and A3's lines and exit codes, the empty unit listing, and A4's exit 2.
- **V7. The installer, read on this host and changing nothing:** `bash vps/install.sh --dry-run` from the branch's
  checkout → exit 0 and one line `install: would install claude-code 2.1.308 to
  /usr/local/libexec/crypto-auto/claude-code/2.1.308/claude`; then `ls -d /usr/local/libexec/crypto-auto/claude-code`
  exits 2. *Derived: the Architect's run of the patched `--dry-run` on a machine without the CLI in place, 25.10.2026 —
  the line stands between `would restart …` and `would copy vps/deploy.sh …`.*
- **No regression:** every section but O, S, U and AA keeps its count and its result from A1 (V2).

---

## 10. The report

`CryptoReports/TZ-72-run-cli-and-models-report.md`, in contract §10's format, committed to `main`. `## Fingerprints`
carries the map, §0's four files at the required revision, and the five files §0's gate adds — and per anchor the
command and the text the match returned, with the anchor table's row count beside the number compared (contract §5).
`## Implementation Summary` gives, one line each, A2's hash, A3's four lines and whether §11 was applied.
`## Remaining Risks` names what this TZ cannot measure from the branch: the deployer's first tick after the merge fetches
the package from npm's registry — a failure is told once and retried on every tick, and no run starts on a CLI not in
place; the CLI moves twenty-six releases at once, so the first run after the merge is the first full session on it, and
its journal's `models=`, `unpinned=` and `memory_peak=` lines are the reading map §10 names; the run's memory limits are
set at each start, not the probes' fixed ones.

---

## Commit Message

```
TZ-72: vps — the run's own Claude Code 2.1.308, pinned by version and SHA-256 and installed by the deployer; the hunter and the CLI's page reader on claude-sonnet-5-5 and claude-haiku-5-5, each read on this host first
```

---

## 11. The patch

Applies to the `vps` tree `6c11ac85ad9712477ff1f963e17e65f39e21012f`. The text between the fences below, written to a
file with a final newline, has MD5 `fac7b81bbb9a011299ea6a460319f99f`.

````diff
diff --git a/vps/install.sh b/vps/install.sh
index 47d60d9..646cad1 100755
--- a/vps/install.sh
+++ b/vps/install.sh
@@ -1,9 +1,11 @@
 #!/usr/bin/env bash
 #
-# vps/install.sh — installs the VPS assistant from the checkout it sits in (TZ-54 B9, TZ-55 B5, TZ-64 B3).
+# vps/install.sh — installs the VPS assistant from the checkout it sits in (TZ-54 B9, TZ-55 B5, TZ-64 B3,
+# TZ-72 B1).
 #
 #   install.sh              called by the deployer from /srv/crypto-auto: selftest, provision,
-#                           verify, install units, enable the manifest, disable the rest
+#                           the run's own CLI, verify, install units, enable the manifest,
+#                           disable the rest
 #   install.sh --bootstrap  once, from the TZ-54 branch: users, directories, clone,
 #                           deploy.sh, crypto-deploy.service and .timer, the timer enabled
 #   install.sh --provision  users, groups, directories, the run's and the paper test's own
@@ -35,6 +37,12 @@ RUN_CLONE="$RUN_HOME/crypto-auto"
 RUN_FETCH=https://github.com/seahomebatumi-ai/crypto-auto.git
 PAPER_HOME=/var/lib/cryptopaper
 ROOT_KNOWN_HOSTS=/root/.ssh/known_hosts
+# TZ-72: the run's own Claude Code -- npm's linux-x64 build at this version, whose one file must hash to this
+# SHA-256 -- installed by this script and by nothing else, at $LIBEXEC/claude-code/$CLI_VERSION/claude
+# (contract §7 item 15). vps/run.py names the same version; selftest section AA holds the two equal.
+CLI_VERSION=2.1.308
+CLI_SHA256=356733f185fa988e6bf3aa9a555269fdd167982a2e2a80d3c8a78037bb92ad58
+CLI_URL="https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-$CLI_VERSION.tgz"
 
 mode="${1-}"
 case "$mode" in
@@ -167,6 +175,53 @@ copy_deploy() {
     mv -f -- "$LIBEXEC/.deploy.sh.new" "$LIBEXEC/deploy.sh"
 }
 
+# TZ-72: true when the pinned CLI is in place and hashes to the pin.
+cli_in_place() {
+    local cli="$LIBEXEC/claude-code/$CLI_VERSION/claude"
+    [ -f "$cli" ] && [ "$(sha256sum -- "$cli" | cut -d ' ' -f 1)" = "$CLI_SHA256" ]
+}
+
+# TZ-72: the pinned CLI put in place. A file at its path that does not hash to the pin is removed first, so
+# no run starts it; the package is fetched into a directory beside the target, its one file is checked
+# against the pin, and only a file that passed is renamed into place -- then every other version goes.
+# Every step is checked where it stands: the caller's `if` switches `set -e` off inside this function.
+install_cli() {
+    local base="$LIBEXEC/claude-code" dir="$LIBEXEC/claude-code/$CLI_VERSION" tmp got old
+    if cli_in_place; then
+        return 0
+    fi
+    rm -f -- "$dir/claude"
+    if ! install -d -m 0755 -- "$dir" || ! tmp="$(mktemp -d "$base/.fetch.XXXXXX")"; then
+        say "claude-code $CLI_VERSION: no directory under $base"
+        return 1
+    fi
+    if ! curl -fsS --max-time 900 -o "$tmp/cli.tgz" "$CLI_URL" \
+        || ! tar --no-same-owner -xzf "$tmp/cli.tgz" -C "$tmp" package/claude; then
+        rm -rf -- "$tmp"
+        say "claude-code $CLI_VERSION not fetched"
+        return 1
+    fi
+    got="$(sha256sum -- "$tmp/package/claude" | cut -d ' ' -f 1)"
+    if [ "$got" != "$CLI_SHA256" ]; then
+        rm -rf -- "$tmp"
+        say "claude-code $CLI_VERSION refused: sha256 $got, pinned $CLI_SHA256"
+        return 1
+    fi
+    if ! chmod 0755 -- "$tmp/package/claude" || ! mv -f -- "$tmp/package/claude" "$dir/claude"; then
+        rm -rf -- "$tmp"
+        say "claude-code $CLI_VERSION not placed"
+        return 1
+    fi
+    rm -rf -- "$tmp"
+    for old in "$base"/*; do
+        if [ "$old" != "$dir" ]; then
+            rm -rf -- "$old"
+            say "removed $old"
+        fi
+    done
+    say "claude-code $CLI_VERSION installed"
+}
+
 installable() { grep -q '^\[Install\]' "$UNITS/$1"; }
 
 listed_units() { grep -v -E '^[[:space:]]*(#|$)' "$MANIFEST"; }
@@ -215,6 +270,11 @@ if [ "$mode" = "--dry-run" ]; then
         if installable "$u" && ! is_listed "$u"; then say "would disable --now $u"; fi
     done
     for u in "${listed[@]}"; do case "$u" in *.service) say "would restart $u" ;; esac; done
+    if cli_in_place; then
+        say "claude-code $CLI_VERSION in place"
+    else
+        say "would install claude-code $CLI_VERSION to $LIBEXEC/claude-code/$CLI_VERSION/claude"
+    fi
     say "would copy vps/deploy.sh to $LIBEXEC/deploy.sh"
     if is_listed crypto-run.path; then say "would create $RUNS_ENABLED"; else say "would remove $RUNS_ENABLED"; fi
     exit 0
@@ -229,6 +289,10 @@ provision_user
 provision_dirs
 provision_run_clone
 provision_paper_clone
+if ! install_cli; then
+    say "claude-code not in place, nothing installed"
+    exit 1
+fi
 if ! systemd-analyze verify "$UNITS"/*; then
     say "systemd-analyze verify red, nothing installed"
     exit 1
diff --git a/vps/run.py b/vps/run.py
index 3e5bfb5..bce0fb3 100644
--- a/vps/run.py
+++ b/vps/run.py
@@ -52,13 +52,19 @@ EFFORT = "high"
 # TZ-66: each alias a subagent call can name resolves to one full id in the session's environment. The Agent
 # tool's per-call model outranks any agent definition (Claude Code docs, "Subagents", read 19.10.2026), and the
 # methodology names the hunter's as `sonnet`; the sheriff runs on MODEL, the session's own.
-HUNTER_MODEL = "claude-sonnet-5"
+# TZ-72: the hunter and the CLI's page reader on the current generation, which CLI_VERSION knows and 2.1.282
+# did not (TZ-71's A2) -- each id read answering on this host first.
+HUNTER_MODEL = "claude-sonnet-5-5"
 # TZ-67: the CLI's own helper model -- the one that reads every fetched page for the hunter -- named by
-# TZ-66's A3 in every run since 09.10.2026 and pinned to that id.
-HELPER_MODEL = "claude-haiku-4-5-20251001"
+# TZ-66's A3 in every run since 09.10.2026 and pinned to that id; TZ-72 moves the pin.
+HELPER_MODEL = "claude-haiku-5-5"
 PINS = {"ANTHROPIC_DEFAULT_OPUS_MODEL": MODEL, "ANTHROPIC_DEFAULT_SONNET_MODEL": HUNTER_MODEL,
         "ANTHROPIC_DEFAULT_HAIKU_MODEL": HELPER_MODEL}
-CLAUDE = ["claude", "-p", PROMPT,
+# TZ-72: the run's own Claude Code, which vps/install.sh fetches from npm's registry at this version and
+# installs only where its SHA-256 is the one that script pins -- never the host's shared /usr/bin/claude.
+CLI_VERSION = "2.1.308"
+CLI = "/usr/local/libexec/crypto-auto/claude-code/" + CLI_VERSION + "/claude"
+CLAUDE = [CLI, "-p", PROMPT,
           "--output-format", "json", "--model", MODEL, "--effort", EFFORT,
           "--allowedTools", "Bash Read Write Edit Glob Grep WebSearch WebFetch",
           "--append-system-prompt", APPEND]
@@ -310,6 +316,11 @@ def main(argv=None):
     except common.CredentialMissing:
         env = None
         common.log("crypto-run: credential %s absent, no session started" % LOGIN_CREDENTIAL)
+    # TZ-72: a CLI the deployer has not put in place is a session that never starts, told as one, never a
+    # traceback.
+    if env is not None and not os.access(CLAUDE[0], os.X_OK):
+        env = None
+        common.log("crypto-run: %s not executable, no session started" % CLAUDE[0])
     in_session["on"] = True
     if env is not None:
         with open(result_path, "wb") as out:
diff --git a/vps/selftest.py b/vps/selftest.py
index b4d9614..86fdc68 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1,7 +1,8 @@
 #!/usr/bin/env python3
 """The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
-TZ-62 B2, TZ-64 B4, TZ-65 B1, TZ-69 B1, TZ-71 B2): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's,
-TZ-57 §12.8's, TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's, TZ-64's, TZ-65's, TZ-69's and TZ-71's changed and new ones, each printing
+TZ-62 B2, TZ-64 B4, TZ-65 B1, TZ-69 B1, TZ-71 B2, TZ-72 B1): the sections of TZ-54 §12.14 with TZ-55 §12.7's,
+TZ-56 §12.6's, TZ-57 §12.8's, TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's, TZ-64's, TZ-65's, TZ-69's, TZ-71's and
+TZ-72's changed and new ones, each printing
 `section <X>: checks <n> failed <m>`, then the total.
 
     python3 vps/selftest.py
@@ -12,14 +13,17 @@ Offline: every fixture is built here or read from the checkout this file sits in
 import array
 import contextlib
 import copy
+import hashlib
 import io
 import json
 import os
 import re
+import shlex
 import shutil
 import signal
 import subprocess
 import sys
+import tarfile
 import tempfile
 import time
 import tracemalloc
@@ -558,6 +562,12 @@ def o_fixtures(tmp, stub_claude, planted):
     return paths, tree, _git(tree, "push", "-q", "origin", "main")
 
 
+def stub_cli(paths):
+    """run.CLAUDE with the fixtures' stub at its head: since TZ-72 the run names its CLI by an absolute path,
+    never through PATH."""
+    return [os.path.join(paths["bin"], "claude")] + run.CLAUDE[1:]
+
+
 def section_o(s):
     cmd = run.CLAUDE
     s.check("run.CLAUDE carries --model immediately followed by claude-opus-5-5",
@@ -566,11 +576,11 @@ def section_o(s):
             any(cmd[i] == "--effort" and cmd[i + 1] == "high" for i in range(len(cmd) - 1)))
     s.check("no element of run.CLAUDE equals opus", "opus" not in cmd)
     # TZ-66: each alias a subagent call can name is pinned to one full id.
-    s.check("run.PINS resolves sonnet to claude-sonnet-5",
-            run.PINS.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-sonnet-5")
+    s.check("run.PINS resolves sonnet to claude-sonnet-5-5",
+            run.PINS.get("ANTHROPIC_DEFAULT_SONNET_MODEL") == "claude-sonnet-5-5")
     s.check("run.PINS resolves opus to run.MODEL", run.PINS.get("ANTHROPIC_DEFAULT_OPUS_MODEL") == run.MODEL)
-    s.check("run.PINS resolves haiku to claude-haiku-4-5-20251001",
-            run.PINS.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") == "claude-haiku-4-5-20251001")
+    s.check("run.PINS resolves haiku to claude-haiku-5-5",
+            run.PINS.get("ANTHROPIC_DEFAULT_HAIKU_MODEL") == "claude-haiku-5-5")
     tmp = tempfile.mkdtemp(prefix="vps-selftest-o.")
     env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", run.LOGIN_ENV,
                 "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW", "SELFTEST_O_RESULT",
@@ -578,7 +588,7 @@ def section_o(s):
     saved_env = {k: os.environ.get(k) for k in env_keys}
     patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (run, "WRITER"), (run, "own_memory_max"),
                (run, "own_swap_max"), (run, "mem_available"), (run, "swap_free"), (run, "ADMISSION_POLL_S"),
-               (run, "ADMISSION_MAX_S")]
+               (run, "ADMISSION_MAX_S"), (run, "CLAUDE")]
     saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
     saved_term = signal.getsignal(signal.SIGTERM)
     try:
@@ -599,10 +609,11 @@ def section_o(s):
                            "ANTHROPIC_DEFAULT_OPUS_MODEL": "selftest-decoy-opus",
                            "ANTHROPIC_DEFAULT_SONNET_MODEL": "selftest-decoy-sonnet",
                            "ANTHROPIC_DEFAULT_HAIKU_MODEL": "selftest-decoy-haiku",
-                           "SELFTEST_O_MODELS": json.dumps({"claude-opus-5-5": {}, "claude-sonnet-5": {},
+                           "SELFTEST_O_MODELS": json.dumps({"claude-opus-5-5": {}, "claude-sonnet-5-5": {},
                                                             "claude-haiku-selftest": {}})})
         common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
         run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
+        run.CLAUDE = stub_cli(paths)
         run.own_memory_max = run.own_swap_max = lambda: None
         with contextlib.redirect_stdout(io.StringIO()) as out:
             code = run.main(["--tree", tree])
@@ -629,7 +640,7 @@ def section_o(s):
         second = [l for l in summary.splitlines() if l.startswith("crypto-run: models=")]
         s.check("the second summary line names every id used, then the one outside run.PINS",
                 len(second) == 1 and second[0].startswith(
-                    "crypto-run: models=claude-haiku-selftest,claude-opus-5-5,claude-sonnet-5 "
+                    "crypto-run: models=claude-haiku-selftest,claude-opus-5-5,claude-sonnet-5-5 "
                     "unpinned=claude-haiku-selftest denied_tools="))
         # TZ-56 §12.4: the third summary line carries the stub's usage and cost.
         third = [l for l in summary.splitlines() if l.startswith("crypto-run: memory_max=")]
@@ -988,7 +999,7 @@ def section_s(s):
         env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", "SELFTEST_O_WRITER_SAW")
         saved_env = {k: os.environ.get(k) for k in env_keys}
         patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (common, "STOP_ACTIVE"), (run, "WRITER"),
-                   (run, "own_memory_max"), (run, "own_swap_max")]
+                   (run, "own_memory_max"), (run, "own_swap_max"), (run, "CLAUDE")]
         saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
         saved_term = signal.getsignal(signal.SIGTERM)
         label = "SIGTERM with STOP_ACTIVE %s: " % ("present" if stopping else "absent")
@@ -1000,6 +1011,7 @@ def section_s(s):
             common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
             common.STOP_ACTIVE = tmp if stopping else os.path.join(tmp, "absent")
             run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
+            run.CLAUDE = stub_cli(paths)
             run.own_memory_max = run.own_swap_max = lambda: None
             code = None
             with contextlib.redirect_stdout(io.StringIO()) as out:
@@ -1154,7 +1166,7 @@ def section_u(s):
     env_keys = ("PATH", "CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", "SELFTEST_O_WRITER_SAW", "SELFTEST_U_RESULT")
     saved_env = {k: os.environ.get(k) for k in env_keys}
     patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (run, "WRITER"), (run, "own_memory_max"),
-               (run, "own_swap_max")]
+               (run, "own_swap_max"), (run, "CLAUDE")]
     saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
     saved_term = signal.getsignal(signal.SIGTERM)
     want_line = "crypto-run: final message is not an answer chars=%d" % len(U_STATUS)
@@ -1165,6 +1177,7 @@ def section_u(s):
                            "SELFTEST_O_WRITER_SAW": os.path.join(tmp, "writer-saw"), "SELFTEST_U_RESULT": U_STATUS})
         common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
         run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
+        run.CLAUDE = stub_cli(paths)
         run.own_memory_max = run.own_swap_max = lambda: None
         with contextlib.redirect_stdout(io.StringIO()) as out:
             code = run.main(["--tree", tree])
@@ -2236,12 +2249,164 @@ def section_z(s):
                                    "<blockquote>three</blockquote>"])
 
 
+# --- AA: the run's own CLI, pinned by vps/install.sh and named by vps/run.py (TZ-72) ---------------
+CLI_FUNCTIONS = re.compile(r"^(?:cli_in_place|install_cli)\(\) \{\n.*?^\}\n", re.M | re.S)
+
+
+def install_text():
+    with open(os.path.join(HERE, "install.sh"), encoding="utf-8") as fh:
+        return fh.read()
+
+
+def aa_package(path, member, body):
+    """A gzipped tarball at path holding body, mode 0755, under member."""
+    with tarfile.open(path, "w:gz") as tar:
+        info = tarfile.TarInfo(member)
+        info.size, info.mode = len(body), 0o755
+        tar.addfile(info, io.BytesIO(body))
+
+
+def aa_install(libexec, version, pin, url):
+    """install.sh's own cli_in_place and install_cli, run by bash as its default mode calls them -- inside an
+    `if`, under `set -euo pipefail` -- with LIBEXEC, CLI_VERSION, CLI_SHA256 and CLI_URL set here: (exit, output)."""
+    functions = "".join(m.group(0) for m in CLI_FUNCTIONS.finditer(install_text()))
+    script = ("set -euo pipefail\nsay() { echo \"install: $*\"; }\nLIBEXEC=%s\nCLI_VERSION=%s\nCLI_SHA256=%s\n"
+              "CLI_URL=%s\n%sif install_cli; then exit 0; fi\nexit 1\n"
+              % (shlex.quote(libexec), shlex.quote(version), shlex.quote(pin), shlex.quote(url), functions))
+    done = subprocess.run(["bash", "-c", script], capture_output=True, text=True)
+    return done.returncode, done.stdout + done.stderr
+
+
+def read_bytes(path):
+    with open(path, "rb") as fh:
+        return fh.read()
+
+
+def section_aa(s):
+    text = install_text()
+    lines = text.splitlines()
+    s.check("run.CLAUDE starts with run.CLI", run.CLAUDE[0] == run.CLI)
+    s.check("run.CLI is /usr/local/libexec/crypto-auto/claude-code/<run.CLI_VERSION>/claude",
+            run.CLI == "/usr/local/libexec/crypto-auto/claude-code/%s/claude" % run.CLI_VERSION)
+    s.check("install.sh pins CLI_VERSION to run.CLI_VERSION, once",
+            [l for l in lines if l.startswith("CLI_VERSION=")] == ["CLI_VERSION=" + run.CLI_VERSION])
+    pins = [l[len("CLI_SHA256="):] for l in lines if l.startswith("CLI_SHA256=")]
+    s.check("install.sh pins one CLI_SHA256 of 64 lowercase hex digits",
+            len(pins) == 1 and re.fullmatch(r"[0-9a-f]{64}", pins[0]) is not None)
+    s.check("install.sh fetches npm's linux-x64 package at CLI_VERSION",
+            'CLI_URL="https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/'
+            'claude-code-linux-x64-$CLI_VERSION.tgz"' in lines)
+    s.check("install.sh's LIBEXEC is /usr/local/libexec/crypto-auto",
+            "LIBEXEC=/usr/local/libexec/crypto-auto" in lines)
+    s.check("install.sh carries cli_in_place and install_cli, once each",
+            [m.group(0).split("(")[0] for m in CLI_FUNCTIONS.finditer(text)] == ["cli_in_place", "install_cli"])
+    steps = ("provision_paper_clone", "if ! install_cli; then", 'if ! systemd-analyze verify "$UNITS"/*; then')
+    at = [[i for i, l in enumerate(lines) if l == step] for step in steps]
+    s.check("the default mode puts the CLI in place after provisioning and before any unit is verified",
+            all(len(x) == 1 for x in at) and at[0][0] < at[1][0] < at[2][0])
+
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-aa.")
+    try:
+        body = b"#!/bin/sh\necho selftest-cli\n" + os.urandom(32)
+        pin = hashlib.sha256(body).hexdigest()
+        good, wrong, bare = (os.path.join(tmp, n) for n in ("good.tgz", "wrong.tgz", "bare.tgz"))
+        aa_package(good, "package/claude", body)
+        aa_package(wrong, "package/claude", body + b"x")
+        aa_package(bare, "package/README.md", b"no binary\n")
+        libexec = os.path.join(tmp, "libexec")
+        base = os.path.join(libexec, "claude-code")
+        target = os.path.join(base, "9.9.9", "claude")
+        os.makedirs(os.path.join(base, "1.0.0"))
+        with open(os.path.join(base, "1.0.0", "claude"), "wb") as fh:
+            fh.write(b"an older version")
+        absent = "file://" + os.path.join(tmp, "absent.tgz")
+
+        code, out = aa_install(libexec, "9.9.9", pin, "file://" + good)
+        s.check("a package whose file hashes to the pin: exit 0", code == 0)
+        s.check("a package whose file hashes to the pin: the file in place, byte for byte",
+                os.path.isfile(target) and read_bytes(target) == body)
+        s.check("a package whose file hashes to the pin: mode 0755",
+                os.path.isfile(target) and os.stat(target).st_mode & 0o777 == 0o755)
+        s.check("a package whose file hashes to the pin: every other version removed", os.listdir(base) == ["9.9.9"])
+        s.check("a package whose file hashes to the pin: one line says it installed",
+                out.splitlines().count("install: claude-code 9.9.9 installed") == 1)
+
+        code, out = aa_install(libexec, "9.9.9", pin, absent)
+        s.check("the pinned file already in place: exit 0, nothing fetched, the file unchanged",
+                code == 0 and out == "" and read_bytes(target) == body)
+
+        with open(target, "ab") as fh:
+            fh.write(b"changed")
+        code, out = aa_install(libexec, "9.9.9", pin, absent)
+        s.check("a file in place that no longer hashes to the pin, nothing to fetch: exit 1", code == 1)
+        s.check("a file in place that no longer hashes to the pin: removed, so no run starts it",
+                not os.path.exists(target))
+        s.check("a file in place that no longer hashes to the pin: one line says not fetched",
+                out.splitlines().count("install: claude-code 9.9.9 not fetched") == 1)
+
+        code, out = aa_install(libexec, "9.9.9", pin, "file://" + wrong)
+        s.check("a package whose file does not hash to the pin: exit 1, nothing in place",
+                code == 1 and not os.path.exists(target))
+        s.check("a package whose file does not hash to the pin: the line names the hash read and the pin",
+                out.splitlines().count("install: claude-code 9.9.9 refused: sha256 %s, pinned %s"
+                                       % (hashlib.sha256(body + b"x").hexdigest(), pin)) == 1)
+        code, out = aa_install(libexec, "9.9.9", pin, "file://" + bare)
+        s.check("a package without package/claude: exit 1, nothing in place", code == 1 and not os.path.exists(target))
+        s.check("no fetch directory left behind by any case", [n for n in os.listdir(base) if n.startswith(".")] == [])
+    finally:
+        shutil.rmtree(tmp, ignore_errors=True)
+
+    # run.py: a CLI not in place is a session that never starts, told as one (TZ-72).
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-aa-run.")
+    env_keys = ("CREDENTIALS_DIRECTORY", "RUNTIME_DIRECTORY", "SELFTEST_O_CLAUDE_SAW", "SELFTEST_O_WRITER_SAW",
+                "SELFTEST_O_RESULT")
+    saved_env = {k: os.environ.get(k) for k in env_keys}
+    patched = [(common, "OUTBOX_DIR"), (common, "REQUESTS_DIR"), (run, "WRITER"), (run, "own_memory_max"),
+               (run, "own_swap_max"), (run, "CLAUDE")]
+    saved_attrs = [(mod, name, getattr(mod, name)) for mod, name in patched]
+    saved_term = signal.getsignal(signal.SIGTERM)
+    try:
+        paths, tree, _ = o_fixtures(tmp, STUB_CLAUDE, "sk-ant-oat01-selftest-planted-" + os.urandom(6).hex())
+        claude_saw = os.path.join(tmp, "claude-saw")
+        os.environ.update({"CREDENTIALS_DIRECTORY": paths["creds"], "RUNTIME_DIRECTORY": paths["runtime"],
+                           "SELFTEST_O_CLAUDE_SAW": claude_saw, "SELFTEST_O_WRITER_SAW": os.path.join(tmp, "writer-saw"),
+                           "SELFTEST_O_RESULT": run.ANSWER_HEAD + " SELFTEST-AA-RESULT"})
+        common.OUTBOX_DIR, common.REQUESTS_DIR = paths["outbox"], paths["requests"]
+        run.WRITER = os.path.join(paths["bin"], "writer-stub.py")
+        missing = os.path.join(tmp, "claude-code", "9.9.9", "claude")
+        run.CLAUDE = [missing] + run.CLAUDE[1:]
+        run.own_memory_max = run.own_swap_max = lambda: None
+        with contextlib.redirect_stdout(io.StringIO()) as out:
+            code = run.main(["--tree", tree])
+        printed = out.getvalue().splitlines()
+        first = [l for l in printed if l.startswith("crypto-run: requests=")]
+        s.check("the CLI absent: exit 1", code == 1)
+        s.check("the CLI absent: one line naming its path",
+                printed.count("crypto-run: %s not executable, no session started" % missing) == 1)
+        s.check("the CLI absent: no session started", not os.path.exists(claude_saw))
+        s.check("the CLI absent: one notice S7 and no answer",
+                notices(paths["outbox"]) == [common.S7]
+                and [n for n in os.listdir(paths["outbox"]) if "-answer-" in n] == [])
+        s.check("the CLI absent: the summary reads claude_exit=- is_error=true",
+                len(first) == 1 and " claude_exit=- is_error=true " in first[0])
+    finally:
+        for mod, name, value in saved_attrs:
+            setattr(mod, name, value)
+        for k, v in saved_env.items():
+            if v is None:
+                os.environ.pop(k, None)
+            else:
+                os.environ[k] = v
+        signal.signal(signal.SIGTERM, saved_term)
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
             ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
             ("T", section_t), ("U", section_u), ("V", section_v), ("W", section_w), ("X", section_x),
-            ("Y", section_y), ("Z", section_z))
+            ("Y", section_y), ("Z", section_z), ("AA", section_aa))
 
 
 def main():
````
