# Implementation Report — TZ-01

> **Reconstructed record.** TZ-01 was executed before `CryptoReports/` existed and
> before `EXECUTOR-INSTRUCTIONS.md` Version 2 defined this format, so no report was
> written at the time. This file was reconstructed on **2026-08-20 under TZ-02 scope F**
> from repository evidence only — `git log`, `git diff --name-status -M`, the committed
> contents of `bench.yml` and `main.yml`, and a fresh execution of every bench. It is
> not backdated and it is not a transcription of the original session.
>
> Implementation commit: `30dfd85`, authored 2026-08-20.

## Status

**COMPLETED** — all three scopes (A, B, C) delivered. Not in effect on `main` at the
time of writing; see `## Final Repository State`.

## Inbound Filing

None. TZ-01 predates the §3 filing rules. The TZ arrived as a session attachment named
`TZ01repohardening.md` and was not committed to the repository. TZ-02 scope C
establishes `CryptoTZ/`; TZ-01's own specification text is therefore not archived, and
this record stands in its place.

## Scope Executed

| Scope | Description | Result |
|---|---|---|
| A | Canonical filename for the architecture document | Completed |
| B | Restrict the bot workflow's `push` trigger | Completed |
| C | Bench gate on push and pull request | Completed |

## Files Created

- `.github/workflows/bench.yml` — 62 lines, MD5 `c2dc4556fb1688a344372005b73b7be1`.

## Files Modified

- `.github/workflows/main.yml` — 10 lines added, 0 removed, 0 modified. The entire diff
  falls inside the `push:` trigger block.

## Files Renamed

- `SYSTEM MAP CRYPTOCALCUL.md` → `SYSTEM_MAP_CRYPTOCALCUL.md`

Recorded by git as **`R100`** — a rename at 100 % similarity, so history is preserved
and no content changed. Evidence:

```
$ git diff --name-status -M fe24061..30dfd85
A	.github/workflows/bench.yml
M	.github/workflows/main.yml
R100	SYSTEM MAP CRYPTOCALCUL.md	SYSTEM_MAP_CRYPTOCALCUL.md
```

The underscored form was chosen because the old name contained spaces, which break
unquoted paths in shell steps, `grep` pipelines and CI commands. (TZ-02 scope B has
since moved this file again, to the hyphenated `SYSTEM-MAP-CRYPTOCALCUL.md`, which is
the current canonical name.)

**Reference updates: none were required.** A repository-wide search for both
`SYSTEM MAP CRYPTOCALCUL` and `SYSTEM_MAP_CRYPTOCALC` returned zero hits outside the
document itself. The only `SYSTEM_MAP` occurrences are section references, which remain
correct: `bench/direction_bench.py:2` (`SYSTEM_MAP §3.12`) and
`bench/backtest_bench.py:4` (`SYSTEM_MAP §10 п.1`). `README.md` is a zero-byte file.

## Files Deleted

**None.** Verified:

```
$ git diff --name-status -M fe24061..30dfd85 | grep '^D' | wc -l
0
```

`image.PNG` remains tracked, as required — `index.html` line 8 references it as
`<link rel="apple-touch-icon" href="image.PNG">`.

## Implementation Summary

### A — Canonical filename

`git mv` of the architecture document. Content byte-identical before and after
(MD5 `813fa95f1512806ebcad057a84d4dcce` on both sides of the rename). The variant
`SYSTEM_MAP_CRYPTOCALC.md` (missing `UL`) that appears in older documentation was not
adopted.

### B — Push trigger

`main.yml`'s `push` trigger gained a `paths-ignore` list so that commits touching only
consumers of `coeffs.json` do not start a 28-coin CoinGecko pass from a keyless shared
runner and rewrite the live Gist mid-development. The list as committed:

```yaml
paths-ignore:
  - 'bench/**'
  - '**/*.md'
  - 'index.html'
  - '.github/workflows/bench.yml'
  - '.github/workflows/backtest_bench.yml'
```

`main.py` and `main.yml` are deliberately absent from the list — a change to either is a
genuine reason to re-run the bot, and continues to trigger it. The `workflow_dispatch`
trigger, `env`, secrets, permissions and every step inside the job were untouched.

### C — Bench gate

`.github/workflows/bench.yml` runs on `push` to `main` and on `pull_request`. Every step
runs under `shell: bash -euo pipefail {0}`, set once via `defaults.run.shell`, and **no
step contains a pipe** — so invariant 25 is satisfied structurally rather than by
discipline: no interpreter exit code can be masked by a downstream `tee`.

No bench file was modified to fit CI. Invocations were read from each bench's own source
(its `argparse` block, its usage docstring, or its `process.argv` handling).

## Validation

| # | TZ-01 validation item | Result |
|---|---|---|
| 1 | `git ls-files` shows the renamed map; no tracked name contains a space | PASS |
| 2 | Repository search for the old names returns zero hits | PASS — 0 hits |
| 3 | `python3 -m py_compile main.py` | PASS |
| 4 | `node --check` on the `<script>` block of `index.html` | PASS |
| 5 | Every gated bench green, counts recorded | PASS — see `## Test Results` |
| 6 | Negative test: a forced bench failure turns the job red | PASS — see `## Deviations` |
| 7 | `main.yml` diff touches only the `push` trigger block | PASS — 10 added, 0 removed |
| 8 | `index.html`, `main.py`, document contents byte-identical | PASS — hashes below |

## Test Results

### Benches gated by `bench.yml` — five, all green

Re-executed at the current HEAD on 2026-08-20 during TZ-02:

| Bench | Invocation | Checks | Failures | Exit |
|---|---|---|---|---|
| `verify_board.js` | `node bench/verify_board.js` | 108 | 0 | 0 |
| `board2_bench.js` | `node bench/board2_bench.js` | 129 | 0 | 0 |
| `prot_bench.js` | `node bench/prot_bench.js index.html` | 167 | 0 | 0 |
| `verify_bench.py` | `python3 bench/verify_bench.py` | 35 | 0 | 0 |
| `direction_bench.py` | `--props --fixtures --control --sim` | 489 786 | 0 blocks | 0 |

`direction_bench.py` is deterministic — its randomised suites are seeded
(`random.Random(20260819)` at line 419, `random.Random(4242)` at line 658), and a repeat
run produced byte-identical output. It is not a flake risk in CI.

### Benches left out — four, plus two modes

TZ-01 requirement C.3 excluded `backtest_bench.py` by name, so it is not counted among
the four omitted by executor judgment. Listed here for completeness.

| Left out | Reason |
|---|---|
| `badge_bench.js` | Requires `index.html.prev`, a pre-edit baseline that is not tracked. Fails at load: `Error: ENOENT: no such file or directory, open '…/index.html.prev'`, exit 1, before any check runs. |
| `clean_bench.py` | Requires two positional arguments `<before.html> <after.html>`; neither baseline exists in the repository. Fails at `bef_path, aft_path = sys.argv[1], sys.argv[2]` with `IndexError`, exit 1. |
| `display_bench.py` | **Red against the current `index.html`**: 24 598 checks, **6 796 failures**, exit 1. Pre-existing defect, see below. |
| `render_bench.py` | **Red against the current `index.html`**: 123 scenarios, 12 795 checks, **1 565 failures**, exit 1. Pre-existing defect, see below. |
| `direction_bench.py --identity` | Requires `orig.html`, a pre-direction-engine baseline absent from the repository. `FileNotFoundError: …/orig.html`, exit 1. |
| `direction_bench.py --display` | **Red**: 57 661 checks, 1 block failure, exit 1. Same root cause as the two above. |
| `backtest_bench.py` | Excluded by TZ-01 C.3 itself — needs the `data.binance.vision` archive or a warm cache. Already served by `.github/workflows/backtest_bench.yml`, which was not modified. |

## Deviations

1. **The negative test was run on all five gated benches, although TZ-01 validation item
   6 specified one.** The concern is per-bench exit-code honesty, and proving it for one
   bench does not prove it for the other four. Each was forced to fail in the working
   tree, one at a time, and reverted; each turned the job red at its own step and halted
   the run. None of the injections was committed, and `git diff -- bench/` was empty
   afterwards.

2. **The TZ-01 negative test was a local replay of workflow semantics, not a runner
   execution.** The `run:` commands were extracted from `bench.yml` and executed under
   `bash -euo pipefail` with GitHub's fail-fast step ordering. That is a faithful replay
   of the shell contract but it is not GitHub's runner, and the report of the time said
   so. *(Superseded during TZ-02: Bench gate run #1 on
   `claude/new-session-113so9` executed on a real `ubuntu-latest` runner and concluded
   `success`, with all five bench steps individually green. The gate is now proven on
   the runner.)*

3. **No pull request was opened at the time.** TZ-01 as delivered did not request one and
   the session's operating rules forbade opening one unsolicited. TZ-02 §1 assumed a PR
   existed; it did not — `list_pull_requests` returned an empty set. The PR was opened
   during TZ-02.

## Pre-existing Issues

1. **Three benches encode a superseded badge layout — not a product defect.**
   `display_bench.py`, `render_bench.py` and `direction_bench.py --display` all fail
   against the shipping `index.html` for one shared reason.

   Production emits the badge as `Word #N — score`:

   - `index.html:1680–1685`, `tierOf` returns `Фон` (`Фон`) for the
     lowest tier.
   - `index.html:1925–1934`, `tierBadge` composes
     `tier.n + (row.no > 0 ? ' #' + row.no : '') + ' — ' + Math.round(row.sc.score)`.

   The benches expect the pre-19.08 wording and ordering:

   - `display_bench.py:156`, `TIER_WORDS` expects `Наблюдать` for the lowest tier, a word
     production no longer emits.
   - `display_bench.py:153`, `RANK_RE = r'>#(\d+) '` requires `#N` to follow a `>`, i.e.
     the rank *before* the tier word.
   - `render_bench.py:274`, `NUM_RE = r'^(?:#(\d+)\s+)?(\S+)\s+(\d+)'` expects
     `#N Word score`.
   - `direction_bench.py --display` reports it directly:
     `tierOf(34.99) = Фон, ждали Наблюдать`.

   All three exit non-zero when they fail, so **invariant 29 is not violated** — they are
   honest, merely outdated. Closing this requires editing either the benches or
   `index.html`; both were out of TZ-01's scope, and editing a bench to make it pass is
   forbidden by hard-floor rule 2 regardless. Reserved for TZ-03.

2. **`main.yml` had no `schedule` trigger — discovered during TZ-01, resolved by TZ-02.**
   TZ-01 observed that `main.yml` carried only `push` and `workflow_dispatch`, while map
   §1 describes the data flow as `GitHub Actions (cron ~1 раз/час)` and invariant 4 pairs
   `STALE_WARN_MIN 75` / `STALE_CRIT_MIN 130` with an hourly run. Because TZ-01 narrowed
   the `push` trigger, it also removed the last accidental refresh path. Adding a cron was
   outside TZ-01's scope, so it was reported rather than implemented. TZ-02 scope D adds
   `cron: '0 * * * *'`, and TZ-02's forensics found the fuller picture: no revision of
   `main.yml` has ever contained a schedule, and the hourly cadence has been supplied by
   an external agent calling the `workflow_dispatch` API.

3. **The branch was never merged, which is why this record is retroactive.** TZ-01's work
   sat on `claude/new-session-113so9` at `30dfd85` with no pull request while `main`
   advanced by five commits, so the bench gate, the scoped push trigger and the map
   rename were in effect nowhere. The divergence produced the System Map rename/modify
   collision that TZ-02 scope A had to resolve deliberately.

## Remaining Risks

1. **`bench.yml` pins `node-version: "20"` and `python-version: "3.12"` without a
   lockfile.** The benches were validated on Node 22 locally and on Node 20 on the
   runner. A future runtime bump could change floating-point formatting or `Math.round`
   edge behaviour in a way no bench asserts against directly.
2. **`verify_bench.py` imports `backtest_bench.py`, which imports `numpy` and `requests`
   at module level.** The gate therefore installs both even though the suite is offline
   (`requests` is stubbed inside the bench). A dependency resolution failure on PyPI
   turns the gate red for a reason unrelated to the code under test.
3. **The `bench/` suite has no coverage of `main.py`.** Every gated bench exercises
   `index.html`. The bot's own metric computation is covered only by
   `backtest_bench.py --verify`, which is outside the gate because it needs the archive.

## Commit

```
30dfd85 chore(repo): canonical system map filename, scoped bot push trigger, bench CI gate
```

Diff against the merge base:

```
 .github/workflows/bench.yml                        | 62 ++++++++++++++++++++++
 .github/workflows/main.yml                         | 10 ++++
 ...P CRYPTOCALCUL.md => SYSTEM_MAP_CRYPTOCALCUL.md |  0
 3 files changed, 72 insertions(+)
```

## Pull Request

None at the time of TZ-01. The work is carried to `main` by the pull request opened
under TZ-02: **https://github.com/seahomebatumi-ai/crypto-auto/pull/1**

CI conclusion on that pull request: **Bench gate — success** (run #1, all five bench
steps green on `ubuntu-latest`).

**NOT IN EFFECT UNTIL MERGED**

## Final Repository State

At the close of TZ-01, `30dfd85` was pushed to `origin/claude/new-session-113so9` and
`main` was untouched. TZ-01's changes were in effect nowhere. That remained true until
TZ-02 merged `main` into the branch and opened pull request #1, which is still open.

## Fingerprints

State as delivered by TZ-01 at `30dfd85`:

| File | Lines | MD5 |
|---|---|---|
| `SYSTEM_MAP_CRYPTOCALCUL.md` | 1136 | `813fa95f1512806ebcad057a84d4dcce` |
| `index.html` | 3413 | `20a12f527e6b78a7a661791bbbd89261` |
| `main.py` | 485 | `064c9dba8313141d1d267316b2da7a39` |

Newest entry under `## 9. Журнал миграций` in the TZ-01-era map: **2026-08-14c**.

That map copy is **stale and has since been superseded.** The current canonical map is
`SYSTEM-MAP-CRYPTOCALCUL.md`, 1461 lines, MD5 `9590fd08d149fb05d4db0d0179b54a50`, newest
migration entry **2026-08-20** — landed by TZ-02 scope A. `index.html` and `main.py` are
unchanged between the two states.
