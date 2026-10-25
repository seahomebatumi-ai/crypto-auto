# Implementation Report — TZ-72 (report-2)

A re-run after the BLOCKED report (`CryptoReports/TZ-72-run-cli-and-models-report.md`). That report stopped at A3
because the run's Claude login was refused as revoked. This run did **not** perform A3; instead it applied and validated
§11's patch token-free and opened the pull request, at the operator's explicit instruction, with the gap recorded below.

## Status

**PARTIAL — not complete to the TZ's own gate.** §11's patch was applied to a branch from `origin/main`, every
code-only validation the TZ names passed (V1–V5, V7), the branch was pushed and pull request #60 was opened. But
**Stage A3 (the four live-login probes) and V6 were not performed in this session**, because the executing agent
declined to read and drive the run's Claude OAuth login (`/etc/crypto-auto/credentials/claude-oauth-token`). TZ §7 A3
makes a passing A3 the gate for applying §11 — "Any probe not passing leaves §11 out whole" — so applying §11 without
A3 is a deviation from the TZ protocol, not a clean completion. The three model ids (`claude-sonnet-5-5`,
`claude-haiku-5-5`, `claude-opus-5-5`) and the hunter's subagent path are therefore **unverified on this host**; A2's
download/hash and A4's clean-up were likewise not run. The operator has stated they will run the host verification
manually.

## Scope Executed

**Class: branch TZ** (contract §8). `## Scope` names three files outside `CryptoReports/**`: `vps/install.sh`,
`vps/run.py`, `vps/selftest.py`.

- **A0** (the host): passed. `crypto-run.service` prints `User=cryptorun`,
  `LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token`, `MemoryMax=167772160`,
  `MemorySwapMax=536870912`; `uname -m` `x86_64`; curl/tar/sha256sum present; ample space; `/usr/bin/claude` is the
  238 767 288-byte 2.1.282 build. The login file exists (108 bytes, mode 600, root).
- **A1** (the baseline): passed. `git rev-parse origin/main:vps` = `6c11ac85ad9712477ff1f963e17e65f39e21012f`; the four
  §0 `vps` files equal §0's pairs (see `## Fingerprints`).
- **A2** (download + hash the package): **not performed.**
- **A3** (four live-login probes): **not performed** (see `## Deviations`).
- **A4** (clean-up): not applicable — A2/A3 wrote no scratch directories and started no probe units.
- **B1**: branch `tz-72-run-cli-and-models` from `origin/main`; `git apply` of §11.
- **B2**: validation (below); implementation commit `c774e07`; branch pushed; pull request #60 opened.
- **B3**: this report on `main`.

## Files Modified (on the branch)

- `vps/install.sh` — `CLI_VERSION=2.1.308`, `CLI_SHA256=356733f1…ad58`, `CLI_URL`; `cli_in_place()` and `install_cli()`;
  the default mode installs the CLI after provisioning and before unit verification; `--dry-run` reports CLI state.
- `vps/run.py` — `HUNTER_MODEL`→`claude-sonnet-5-5`, `HELPER_MODEL`→`claude-haiku-5-5`; `CLI`/`CLAUDE[0]` the absolute
  pinned path; a non-executable CLI is a session that never starts.
- `vps/selftest.py` — new section AA; sections O/S/U moved to the new ids and the absolute-path stub.

## Implementation Summary

- **Patch integrity:** §11 cut from the TZ (441 lines) has MD5 `fac7b81bbb9a011299ea6a460319f99f`, equal to §11's.
  `git apply --check` against `origin/main` exited 0; applied clean.
- **A2's hash:** not measured this run. (The BLOCKED report measured it equal to the pin; unchanged here.)
- **A3's four lines:** none — A3 not performed.
- **Whether §11 was applied:** **yes**, as commit `c774e07`, but **without** the A3 verification the TZ gates it on.

## Validation

Code-only items, run on the host against the committed branch:

- **V1** `python3 -m py_compile vps/run.py vps/bot.py vps/selftest.py` → exit 0; `bash -n vps/install.sh` → exit 0.
- **V2** `python3 vps/selftest.py` → exit 0, last line `selftest: sections 27 checks 560 failed 0 empty 0`; section O
  33/0, S 35/0, U 18/0, Z 23/0, AA 26/0.
- **V3** five controls, each reverted to a clean tree:
  - C1 `CLI_VERSION` 2.1.308→2.1.307 → `section AA: checks 26 failed 1`, exit 1;
  - C2 SHA-256 guard `if false` → `section AA: checks 26 failed 2`, exit 1;
  - C3 `os.access` guard `if False` → `section AA: checks 21 failed 1` and stderr `FAIL section AA raised
    FileNotFoundError: …/claude-code/9.9.9/claude`, exit 1;
  - C4 `HUNTER_MODEL` →`claude-sonnet-5` → `section O: checks 33 failed 2`, exit 1;
  - C5 `rm -f -- "$dir/claude"` → `:` → `section AA: checks 26 failed 3`, exit 1.
- **V4** post-apply: `vps/install.sh` 336 `6abc43fb0ba6620a123cf732ef761466`, `vps/run.py` 375
  `36dc8f3bf39b44168674677c85aecd44`, `vps/selftest.py` 2430 `1f207b2dce474439924b1ef22c82e918`; `git rev-parse HEAD:vps`
  = `dce795d17056cae7a22ee57dd0daa24dd4b3f808`.
- **V5** `git diff --stat origin/main...HEAD` names only the three `vps` files.
- **V6** A2/A3/A4 outputs: **not performed** (A3 not run).
- **V7** `bash vps/install.sh --dry-run` → exit 0, line `install: would install claude-code 2.1.308 to
  /usr/local/libexec/crypto-auto/claude-code/2.1.308/claude` between `would restart …` and `would copy vps/deploy.sh …`;
  `ls -d /usr/local/libexec/crypto-auto/claude-code` exit 2.

## Deviations

- **Stage A3 and V6 were not performed by the executing agent**, and §11 was nonetheless applied and the pull request
  opened. This departs from TZ §7 A3 ("Any probe not passing leaves §11 out whole"). The reason is not a sandbox or
  tooling limitation: the agent declined to read and operate the run's Claude OAuth login to validate and ship continued
  automated use of it. The prior report records that same login being refused by the backend with HTTP 401 "OAuth token
  revoked. Please log in again or contact your administrator," and the sibling tasks TZ-73/TZ-74 exist to re-mint it;
  the agent will not take part in operating or re-minting that credential. Host verification is left to the operator.
- Because A3 is unperformed, the model ids and hunter's path remain **unverified on this host** by this run.

## Commit

Report commit to `main` (contract §8 `CryptoReports/**` direct-push path):

```
TZ-72: report-2 — §11 applied token-free and validated (V1–V5, V7), PR #60; A3/V6 not performed, live-login verification left to the host
```

The implementation commit on the branch is `c774e07`.

## Pull Request

#60 — `tz-72-run-cli-and-models` → `main`. Its body states that A3/V6 were not performed and that §11 is applied without
the live-login verification the TZ requires.

## Remaining Risks

- **The run's Claude login is being revoked by the backend.** The prior report's journal shows repeated 401s with
  "OAuth token revoked," each followed by a freshly-minted token. This is unresolved and is the root cause of the
  TZ-72/73/74 sequence. The supported remedy for an unattended service is an Anthropic API key (`sk-ant-api…`) with its
  own billing, via the same `LoadCredential=` mechanism — not re-minting around the revocation. Until that changes,
  production runs will keep failing at authentication.
- After a merge, TZ §10's risks stand: the deployer's first tick fetches the package from npm (failure told once,
  retried each tick); the CLI jumps twenty-six releases, so the first run is its first full session; the run's memory
  limits are set at each start.

## Fingerprints

Against `origin/main:vps` = `6c11ac85ad9712477ff1f963e17e65f39e21012f`:

| File | Lines | MD5 |
|---|---:|---|
| `vps/install.sh` (base) | 272 | `57f874a6ea816abeaad7f1fd3cec3972` |
| `vps/run.py` (base) | 364 | `988f6f4955072f6429def95d3957d974` |
| `vps/selftest.py` (base) | 2265 | `2fbba2579fdebd452e185ddf00a719bc` |
| `vps/bot.py` (base, untouched) | 496 | `2bf99362c01bf0fc638c7352c64aea91` |

Post-apply on the branch: `vps/install.sh` 336 `6abc43fb0ba6620a123cf732ef761466`, `vps/run.py` 375
`36dc8f3bf39b44168674677c85aecd44`, `vps/selftest.py` 2430 `1f207b2dce474439924b1ef22c82e918`; `HEAD:vps`
`dce795d17056cae7a22ee57dd0daa24dd4b3f808`. §11 patch MD5 `fac7b81bbb9a011299ea6a460319f99f`.
