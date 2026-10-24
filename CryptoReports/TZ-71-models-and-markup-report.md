# Implementation Report — TZ-71

Previous TZ's branch: `tz-70-etf-three-days` was merged into `main` by PR #58 (`e874c2d`). This TZ builds on a merged base.

## Status

**COMPLETED, without part A.** Part B (the markup) is implemented, validated and in PR #59. Part A (the two model pins) is
**not applied**. On this host, under the run's own login, A2 found that neither `claude-sonnet-5-5` nor
`claude-haiku-5-5` answers. TZ §3 and §7 A2 cover this case: «Either id not answering leaves part A out».

## Inbound Filing

None. The TZ was already at its canonical path, `CryptoTZ/TZ-71-models-and-markup.md`, on `origin/main`
(added by `6dfa321 Add files via upload`). Nothing was moved or renamed.

## Scope Executed

**Class: branch TZ** (contract §8). `## Scope` names files outside `CryptoReports/**`: `vps/run.py`, `vps/bot.py` and
`vps/selftest.py`.

- A0 host check: passed.
- A1 baseline: passed.
- A2 two model-id probes: both ids failed to answer, so part A is out.
- A3 CLI version: recorded.
- B1: the patch was applied without its `vps/run.py` hunk and without section O's three hunks.
- B2: validation, one implementation commit, branch pushed, PR #59 opened.
- B3: this report.

On the host: two transient units ran and were collected. Nothing was installed, enabled, started or restarted.

## Files Created

- `CryptoReports/TZ-71-models-and-markup-report.md` (this report, on `main`).

## Files Modified

On branch `tz-71-models-and-markup`:
- `vps/bot.py`: §11's three hunks, whole.
- `vps/selftest.py`: §11's module-docstring hunk and its section Z hunk. Section O's three hunks were left out (part A).

**Not modified:** `vps/run.py`. Its hunk is part A.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**Part A not applied. Deciding line:** A2 probe 1 printed `True success [] 0` for `claude-sonnet-5-5`, after the
CLI's stderr line `[claude-code:unrecognized_model] {"model":"claude-sonnet-5-5","query_source":"sdk"}`. Probe 2 printed
the same for `claude-haiku-5-5`. `HUNTER_MODEL` stays `claude-sonnet-5` and `HELPER_MODEL` stays
`claude-haiku-4-5-20251001`.

**Part B applied as §11 states it.** `vps/bot.py` gains `_CODE`, `FENCE`, `QUOTE`, `FOLD`, `_quote_kind`, `_inline`,
`quote_block` and `_block`. `_units` and `convert_line` now call them. The new conversions are:

| Markdown | Telegram HTML |
|---|---|
| `` `…` `` | `<code>…</code>` |
| a block between two ```` ``` ```` lines | one `<pre>` |
| a run of `> ` lines | one `<blockquote>` |
| a run of `>> ` lines | one `<blockquote expandable>` |

The table-splitting loop has moved into `_block`, and fenced blocks and quotes use the same helper. Section D's input
still converts byte for byte as before; selftest section Z checks this directly.

### Stage A readings

**A0.** `systemctl cat crypto-run.service`, on host `vultr` as root, printed both required lines, among others:
```
User=cryptorun
LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token
```

**A1.**
- `git fetch --all --prune`, then `git rev-parse origin/main` → `6dfa321c45f510598a014bc4ce6dae0190b7d256`.
- `git rev-parse origin/main:vps` → `0eeac7c1b7310e86a454c72c4201246b1c96b97a`, equal to the required tree.
- The three `vps` files equal §0's pairs (see `## Fingerprints`).
- `python3 vps/selftest.py` at `origin/main` → exit 0, last line `selftest: sections 25 checks 511 failed 0 empty 0`,
  equal to the Architect's reading.

**A2.** Both commands as run. Only `<n>`, `<PIN>`, `<id>` and `<alias>` were filled in from TZ §7.

Unit 1:
```
systemd-run --wait --pipe --collect --quiet --unit=tz71-probe-1 \
  -p User=cryptorun -p Group=cryptorun -p WorkingDirectory=/var/lib/cryptorun \
  -p Environment=HOME=/var/lib/cryptorun -p Environment=DISABLE_AUTOUPDATER=1 \
  -p "Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin" \
  -p Environment=ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5 \
  -p LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token \
  /bin/sh -c 'CLAUDE_CODE_OAUTH_TOKEN="$(cat "$CREDENTIALS_DIRECTORY/claude-oauth-token")" exec claude -p "Reply with the one word: ok" --output-format json --max-turns 1 --model sonnet' \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("is_error"), d.get("subtype"), sorted((d.get("modelUsage") or {}).keys()), d.get("total_cost_usd"))'
```
Printed:
```
[claude-code:unrecognized_model] {"model":"claude-sonnet-5-5","query_source":"sdk"}
True success [] 0
```
Exit codes (`PIPESTATUS`): `systemd-run` **1**, the summary `python3` 0.

Unit 2: the same command with `--unit=tz71-probe-2`, `-p Environment=ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-5-5`
and `--model haiku`. Printed:
```
[claude-code:unrecognized_model] {"model":"claude-haiku-5-5","query_source":"sdk"}
True success [] 0
```
Exit codes: `systemd-run` **1**, the summary `python3` 0.

In both lines, `is_error` is `True` and the model list is empty, so **neither id answers** by TZ §7 A2's definition.

After both units, `systemctl list-units --all 'tz71-probe-*'` printed `0 loaded units listed.` (exit 0). A second run at
the end of the session, with `--no-legend | wc -l`, printed `0`.

No credential value was printed. The summary prints only four fields of the JSON result. The `[claude-code:…]` line is
the CLI's own stderr and names only the model id.

**A3.** `runuser -u cryptorun -- env HOME=/var/lib/cryptorun claude --version` → `2.1.282 (Claude Code)`, exit 0.

### B1: the command

The patch was extracted from TZ §11 with
`awk '/^````diff$/{f=1;next} /^````$/{f=0} f' CryptoTZ/TZ-71-models-and-markup.md > tz71-full.patch` (277 lines).
`git apply --check tz71-full.patch` reported the whole patch clean.

Part A's hunks were removed from a copy. That copy keeps:
- lines 1–138: `vps/bot.py`'s three hunks
- lines 158–171: `vps/selftest.py`'s header and docstring hunk
- lines 206–277: the section Z hunk

It drops:
- lines 139–157: `vps/run.py`
- lines 172–205: section O's three hunks

Command: `sed -n '1,138p;158,171p;206,277p' tz71-full.patch > tz71-partA-out.patch`. It was then applied with
`git apply --check tz71-partA-out.patch && git apply tz71-partA-out.patch`, which reported clean and applied.

## Validation

- **V1.** `python3 -B -m py_compile vps/run.py vps/bot.py vps/selftest.py` → exit 0.
- **V2.** `python3 -B vps/selftest.py` → exit 0. Last line `selftest: sections 26 checks 534 failed 0 empty 0`.
  Sections D, E, O and Z read exactly as registered:
  ```
  section D: checks 13 failed 0
  section E: checks 12 failed 0
  section O: checks 33 failed 0
  section Z: checks 23 failed 0
  ```
  Every `section` line was diffed against A1's run with
  `diff <(grep "^section" st0.txt) <(grep "^section" st1.txt)`. The only difference is the added line
  `> section Z: checks 23 failed 0`, so every other section's count and result is as at A1.
- **V3.** Each control ran on the committed branch (`f8a4f14`) and was reverted with `git checkout -- vps/`. After each
  one, `git status --porcelain` printed nothing.
  - **C1** (the `<blockquote expandable>` tag) → `section Z: checks 23 failed 4`, exit 1. **Red as registered.**
  - **C2** (`HUNTER_MODEL`) → the `sed` matched nothing (`git diff | wc -l` → 0). Result: `section O: checks 33 failed
    0`, exit 0. The TZ marks C2 «part A applied only». Part A is out, so the line it targets,
    `HUNTER_MODEL = "claude-sonnet-5-5"`, is not in the tree and the control has nothing to change. See
    `## Deviations`.
  - **C3** (`HELPER_MODEL`) → the same as C2: `sed` changed nothing, `section O: checks 33 failed 0`, exit 0. The TZ
    marks C3 «part A applied only». See `## Deviations`.
  - **C4** (`<code>` in `_inline`) → `section Z: checks 23 failed 2`, exit 1. **Red as registered.**
- **V4.** Measured after B1:

  | File | Lines | MD5 | Compared with |
  |---|---:|---|---|
  | `vps/run.py` | 364 | `988f6f4955072f6429def95d3957d974` | equal to §0's pair, as required with part A out |
  | `vps/bot.py` | 496 | `2bf99362c01bf0fc638c7352c64aea91` | equal to the Architect's build |
  | `vps/selftest.py` | 2265 | `2fbba2579fdebd452e185ddf00a719bc` | reported as found. It differs from the whole-patch pair, `c6ba603e…`, by section O's three left-out hunks, which change no line count |

- **V5.** `git diff --stat origin/main...HEAD`:
  ```
   vps/bot.py      | 92 +++++++++++++++++++++++++++++++++++++++++++++------------
   vps/selftest.py | 64 +++++++++++++++++++++++++++++++++++++--
   2 files changed, 134 insertions(+), 22 deletions(-)
  ```
  Nothing outside the scope is touched. `vps/run.py` is absent because its only hunk is part A. See `## Deviations`.
- **V6.** See A2 above: both lines, both exit codes (1 and 1), and the empty unit listing.
- **V7.** The TZ's command printed, with exit 0:
  ```
  ['Вход <code>$1.231</code> · <b>стоп</b> <code>$1.3593</code>', '<blockquote expandable>ETF 23.10 · 22.10\nBTC -137.9 · -635.5</blockquote>']
  ```
  This is identical to the expected output.
- **No regression.** Section D still reads `checks 13 failed 0`. Section Z's check «section D's input converts as
  before» passes. Every other section's line is unchanged from A1 (see V2).

## Test Results

| Run | Where | Result |
|---|---|---|
| selftest at `origin/main` (A1) | VPS, local | sections 25 checks 511 failed 0 empty 0, exit 0 |
| selftest on the branch (V2) | VPS, local | sections 26 checks 534 failed 0 empty 0, exit 0 |
| C1 / C4 | VPS, local | section Z failed 4 / failed 2, exit 1 / 1 |
| C2 / C3 | VPS, local | `sed` no-op (part A out), exit 0 / 0 |
| Bench gate on PR #59 | GitHub runner | run `40135182270`, event `pull_request`, head `f8a4f14`, **success** |

## Deviations

These follow from part A being out. Each is read off the TZ's own wording, not chosen.

- **V3's C2 and C3 did not turn red.** Both are marked «(part A applied only)», and part A is not applied. Their `sed`
  patterns target the part-A pins, which are not in the tree, so the selftest stays green. This item's sentence «A
  control that leaves the selftest green fails this item» would, read literally, fail them. The TZ's own qualifier
  makes them not applicable here. No substitute control of my own design was run (TZ §6, contract §6).
  **For the Architect:** with part A out, section O's existing expectations of the old pins have no registered
  negative control in this TZ.
- **V5 names `vps/run.py`, but the diff does not.** V5 does not qualify for part A out. Without part A, `vps/run.py` has
  no hunk, and V4 requires it to keep §0's pair. So its absence from the diff is what V4 requires.
- **The commit message is TZ §12's part-A-out variant**, as the TZ prescribes.

## Pre-existing Issues

- **The map's row «Two model pins lag a generation» names ids this host's CLI does not recognise.** The row says
  `claude-sonnet-5-5` and `claude-haiku-5-5` are «the current generation». On Claude Code `2.1.282`, under the run's
  login, both returned `unrecognized_model`, with an empty `modelUsage` and cost 0. This was measured once per id.
  Nothing was acted on. Whether the ids are wrong or not yet available to this CLI or login is the Architect's to
  resolve.
- The TZ header says it was written against `main` at `15b29b9`. At execution, `origin/main` was `6dfa321`, three
  commits later: `55bcb7c` journal, `169a852` map, `97ed1bc` methodology, and `6dfa321` uploading this TZ. The `vps`
  tree and every fingerprinted file equal the TZ's values, so the patch applied against the bytes it was written for.

## Remaining Risks

- **Telegram's acceptance of the new tags is not measured from the branch.** No message was sent and the bot token was
  not read (TZ §5). Acceptance will first be read on the first answer the methodology prints in `<code>`, `<pre>` from
  a fence, `<blockquote>` or `<blockquote expandable>`. If Telegram refuses a chunk there, that chunk falls back to
  plain text (`send_chunk`, TZ-54).
- **The methodology prints none of the new forms yet** (map row «The answer's markup is bold and headings only»). Until
  a revision after this merge, the answer looks as it does today, so the new code paths will not run in production
  until then.
- **The hunter and the page reader stay a generation behind**, as before. Moving them needs ids that answer on this
  host, which is a new TZ.

## Commit

Implementation commit, on branch `tz-71-models-and-markup`, already pushed: `f8a4f14`.
```
TZ-71: vps — the bot renders code spans, fenced blocks, quotes and folding quotes, every block split whole; the model pins stay, A2 did not read both ids
```
Contents: `vps/bot.py` and `vps/selftest.py`, as under `## Files Modified`.

This report's commit, on `main`. Its message:
```
TZ-71: report — the bot's markup; the model pins stay
```
Contents: `CryptoReports/TZ-71-models-and-markup-report.md` only.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/59 (base `main`, head `tz-71-models-and-markup`).

## CI Execution

- **Bench gate** (`bench.yml`): ran on the runner for the `pull_request` event. Run `40135182270`, head `f8a4f14`,
  conclusion **success**. It did not run on the branch push, because `bench.yml`'s push filter is
  `branches: [ main, 'claude/**' ]`.
- **`main.yml`**: did not run, and cannot be triggered by this branch. Its `push` filter is an allow-list of `main.py`
  and `.github/workflows/main.yml` on `main` only. That allow-list was confirmed by reading the workflow this session.
- **`calib.yml`, `backtest_bench.yml`, `journal.yml`**: did not run. Their triggers are dispatch, schedule, or pushes to
  `claude/**` on paths this TZ does not touch.

## Final Repository State

- Branch `tz-71-models-and-markup` was pushed at `f8a4f14`, one commit on `origin/main` `6dfa321`. PR #59 is open.
- The working tree was clean after the controls (`git status --porcelain` empty). `vps/__pycache__` from V1 was
  removed.
- No `tz71-probe-*` unit exists on the host. Nothing was installed, enabled, started or restarted.
- **NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Measured against `origin/main` at `6dfa321c45f510598a014bc4ce6dae0190b7d256`, each with
`git show origin/main:<file> | wc -l` and `| md5sum`.

**Map.** `SYSTEM-MAP-CRYPTOCALCUL.md`: 2800 lines, MD5 `167140f2528337adda68fe103403b38c`, equal to the TZ's reported
pair. Revision string: `grep -F -m1 -o '**Revision 2026-10-24-c.**' map.md` → `**Revision 2026-10-24-c.**`, equal to
the required one.

**Anchors.** The list was cut from the map's own table by structure: every line after the separator at line 80, up to
the first line not opening with `|`, using `awk 'NR>80{ if ($0 !~ /^\|/) exit; print }' map.md`. **The table has 7
rows, and 7 were compared.** For each row:
- `grep -F -o -m1 -f <anchor> map.md` returned the matched text, shown below.
- `grep -Fc` counted the map lines containing the anchor. Each count is 2: the table row and the heading or text it
  names.
- `grep -Fxc -- "<row>" TZ-71.md` checked that the TZ header quotes the row character for character. Each result is 1.

| # | Anchor | Matched text returned | Map lines | TZ header quotes row |
|---|---|---|---:|---:|
| 1 | revision | `**Revision 2026-10-24-c.**` | 2 | 1 |
| 2 | direction engine | `### 3.12 Direction engine — veto cascade` | 2 | 1 |
| 3 | catalyst registry | `### 3.15 Catalyst registry` | 2 | 1 |
| 4 | exhaustion measure | `### 3.16 List exhaustion — the day-range measure` | 2 | 1 |
| 5 | analytical engine | `## 11. Analytical engine` | 2 | 1 |
| 6 | squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 | 1 |
| 7 | newest invariant | `72. **A write that fails leaves this run's product or nothing` | 2 | 1 |

The map's file table, cut the same way after its separator at line 92, is identical to the TZ's: `diff` printed
nothing.

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
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | equal. Version line `**Version 31.**` |
| `vps/run.py` | 364 | `988f6f4955072f6429def95d3957d974` | equal |
| `vps/bot.py` | 442 | `d1ebb118c78413f62418dd1c331f9196` | equal |
| `vps/selftest.py` | 2207 | `55eed34fa003c2e7ea51826d438b55ce` | equal |
