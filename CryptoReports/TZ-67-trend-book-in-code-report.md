# Implementation Report — TZ-67

## Status

**COMPLETED.**

1. **The code.** B1's patch extracted from `origin/main:CryptoTZ/TZ-67-trend-book-in-code.md` by the one command the
   TZ gives: MD5 `b66517c27fb4cd4b745833be34b58477`, **437 lines** — the known answer; `git apply --check` and
   `git apply` both exit 0 (`apply=0`), nothing was retyped. B2: `vps/book.py` **282** lines, MD5
   `f7ef81fceac48c69335a157e8c87f90f`; `vps/run.py` **364** lines, MD5 `988f6f4955072f6429def95d3957d974`;
   `vps/selftest.py` **1915** lines, MD5 `2f966893b69ccc5981f35e83a370d5a9` — all three equal to B2's known answers.
   B3: `git diff --cached --summary origin/main` printed exactly `create mode 100644 vps/book.py`.
2. **The checks.** V1: exit 0, `selftest: sections 24 checks 452 failed 0 empty 0`, `section O: checks 33 failed 0`,
   `section X: checks 14 failed 0`. The five negative controls, each applied alone and reverted, produced exactly the
   TZ's partitions: control 1 → `failed 1` (`a short stopped through a gap fills at the open`); control 2 → `failed 4`
   (`the stop sits 2 ATR(20) below the entry: 105 - 2 x 2.2`, `its R after fees and slippage`, `funding counts the
   prints after the entry and up to the exit, paid by the long`, `its stop: 103 - 2 x 2.55`); control 3 → `failed 1`
   (`live bars drop the day still open`); control 4 → `failed 1` (`funding counts the prints after the entry and up to
   the exit, paid by the long`); control 5 → `failed 1` (section O's `run.PINS resolves haiku to
   claude-haiku-4-5-20251001`). In each, every other check of all twenty-four sections stayed green, each revert was
   followed by a digest comparison against B2 (`True` five times), and the final run read `failed 0` with B2's digests.
3. **The pins.** V3, line 1: `{'ANTHROPIC_DEFAULT_OPUS_MODEL': 'claude-opus-5-5', 'ANTHROPIC_DEFAULT_SONNET_MODEL':
   'claude-sonnet-5', 'ANTHROPIC_DEFAULT_HAIKU_MODEL': 'claude-haiku-4-5-20251001'}`; line 2: `True`.

The hosted gate read: Bench gate run **`39403916625`** on headSha `c336d4d849a54321afee14bc81762a3ffae39165` — the
implementation commit — event `pull_request`, status `completed`, conclusion **`success`**, 23 of 23 job steps `success`.

---

## Inbound Filing

Nothing was moved and nothing was renamed. The TZ arrived at its own canonical path,
`CryptoTZ/TZ-67-trend-book-in-code.md`, on `origin/main` in commit `1b3bab5` ("Add files via upload"), 713 lines, MD5
`937b2c82e7f1cda8d43d55656be60bb6`. No copy landed in the repository root and no filename was mangled. No credential
arrived under the trigger line, and the TZ names none (its §1).

The session's checkout was behind: it stood at `c86719a` and `git fetch --all --prune` brought `origin/main` to `1b3bab5`
before the TZ was visible — the case §3 describes. `git rev-parse --is-shallow-repository` → `false`.

The previous TZ's branch was merged: `git merge-base --is-ancestor d9cd3c7 origin/main` → exit `0` (A1.2; pull request
#54, TZ-66).

## Scope Executed

**Class: branch TZ** (contract §8) — the scope names `vps/book.py`, `vps/run.py` and `vps/selftest.py`, all outside
`CryptoReports/**`. Stage A (readings), Stage B (B1–B4) and V1–V5 were executed. B1's patch created one file and modified
two; no other file was touched on the branch. No VPS was read or changed, no unit was started and no model session was
opened (§1, rule 1): `vps/book.py` was run only through the selftest, against stubs, and neither `--live` nor
`--archive` was run against a market host.

## Files Created

- `vps/book.py` (282 lines).

## Files Modified

- `vps/run.py` — `HELPER_MODEL = "claude-haiku-4-5-20251001"` and the third entry of `PINS` (`+5 −1`, with the comment).
- `vps/selftest.py` — `import book`, section X (fourteen checks, two worlds, the live path's stubs), section O's one
  new check, the stub session's third recorded variable and the third decoy.

`git diff --stat origin/main...HEAD` → `vps/book.py | 282 +`, `vps/run.py | 6 +-`, `vps/selftest.py | 89 +-`;
`3 files changed, 374 insertions(+), 3 deletions(-)`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

`vps/book.py` carries the Donchian 55/20 trend system with a 2 × ATR(20) stop over closed UTC daily bars. One function,
`replay`, makes every trade; `levels` states what the next close decides; `result_r` prices a closed trade in R after
0.10 % a side and the funding prints after the entry and up to the exit. `--live` and `--archive` are the two modes the
TZ names. The merge installs the program and nothing calls it: `run.PROMPT`, `run.APPEND`, `run.CLAUDE`, `run.MODEL`,
`run.EFFORT` and `run.HUNTER_MODEL` did not move (TZ §5), which V3's second line proves for the command line.

## Validation

**A1 (baseline, on `origin/main`'s tree, before any change).**

| # | Command | Result | Known answer |
|---|---|---|---|
| 1 | `git rev-parse origin/main:vps` | `d013f2d9ac9209c9ac71dc7c6397696080b871aa` | equal |
| 2 | `git merge-base --is-ancestor d9cd3c7 origin/main; echo $?` | `0` | equal |
| 3 | `python3 vps/selftest.py` (Python 3.12.3) | exit 0, `selftest: sections 23 checks 437 failed 0 empty 0` | equal |

**B1–B3.** As in Status 1. Commands: the TZ's B1 block verbatim, then `for f in vps/book.py vps/run.py vps/selftest.py;
do echo "$f $(wc -l < $f) $(md5sum < $f)"; done`, then `git add -A vps/ && git diff --cached --summary origin/main`.
B4: `rm -r /tmp/tz67` run after the apply; the directory is gone.

**V1.** `python3 vps/selftest.py > out; echo exit=$?` → `exit=0`; last line `selftest: sections 24 checks 452 failed 0
empty 0`; `section O: checks 33 failed 0`; `section X: checks 14 failed 0`. Controls: a script replaced the TZ's exact
string in the named file (each string occurred exactly once — asserted), ran `python3 vps/selftest.py`, restored the
file and compared its MD5 with B2:

| Control | File | Exit | Summary line | FAIL lines |
|---|---|---:|---|---|
| 1 | `vps/book.py` | 1 | `checks 452 failed 1 empty 0` | section X: `a short stopped through a gap fills at the open` |
| 2 | `vps/book.py` | 1 | `checks 452 failed 4 empty 0` | section X ×4, the four named in Status 2 |
| 3 | `vps/book.py` | 1 | `checks 452 failed 1 empty 0` | section X: `live bars drop the day still open` |
| 4 | `vps/book.py` | 1 | `checks 452 failed 1 empty 0` | section X: `funding counts the prints after the entry and up to the exit, paid by the long` |
| 5 | `vps/run.py` | 1 | `checks 452 failed 1 empty 0` | section O: `run.PINS resolves haiku to claude-haiku-4-5-20251001` |

Final run after control 5's revert: exit 0, `failed 0 empty 0`, all three digests equal to B2.

**V2.** `python3 -m py_compile vps/book.py vps/run.py vps/selftest.py` → exit 0 (`pycompile=0`).

**V3.** The TZ's command, verbatim — output in Status 3.

**V4.** `git diff --cached --name-only origin/main` before the commit, and `git diff --name-only origin/main...HEAD` after
it, each listed exactly `vps/book.py`, `vps/run.py`, `vps/selftest.py`.

**V5.** Branch `tz-67-trend-book-in-code` pushed; pull request #55 opened (Pull Request, below). Nothing is pushed to
`main` by this session but this report.

## Test Results

- V1: 452 checks, 0 failed, 0 empty, 24 sections. Section O 33 (was 32), section X 14 (new); sections A–W otherwise keep
  their counts (437 → 452 is O's one plus X's fourteen).
- V1 controls: 5 of 5 failed exactly the TZ's partitions and recovered.
- V2: exit 0. V3: both lines equal to the known answers. V4: exact scope. Hosted gate: run `39403916625`, `success`.

## Deviations

None.

## Pre-existing Issues

None found. The only difference between the session's starting checkout and the TZ's baseline was the stale snapshot
(`c86719a` against `1b3bab5`), resolved by §3's fetch; every figure the TZ's gate measures matched on `origin/main`.

## Remaining Risks

- **Python 3.11 and 3.13 were not run.** The TZ's derived figures include those versions; this session had Python 3.12.3
  only, which is the version the TZ's Host line names. The selftest figures above are 3.12's.
- **The archive's figures were not re-run here.** `--archive` and `--live` were never run against a market host (rule 1,
  contract §7 item 9); everything about the program's behaviour on real data is the Architect's reading in the map's row
  and the audit's re-run, not this report's measurement.
- **`vps/book.py` has no caller after the merge.** That is TZ §5's design; the deployer will run the selftest, which now
  imports `book`, before it installs the tree.

## Commit

Implementation, on the branch `tz-67-trend-book-in-code`, pushed — `c336d4d849a54321afee14bc81762a3ffae39165`, one commit
on top of `1b3bab54317709f25141377899ad741b49b11b81`, touching `vps/book.py` (created), `vps/run.py` and
`vps/selftest.py` (`3 files changed, 374 insertions(+), 3 deletions(-)`):

```
TZ-67: vps — the book in code: the Donchian trend system, one replay live and over the archive; the CLI's helper model pinned
```

Report, on `main`, the message this session is authorised to carry:

```
TZ-67: report — the book in code
```

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/55 — base `main`, head `tz-67-trend-book-in-code`, state `OPEN`,
`mergeable` `MERGEABLE` when read. The Architect's verdict precedes the merge (contract §8).

## CI Execution

`gh run list --branch tz-67-trend-book-in-code` returned exactly one run: **Bench gate**, id **`39403916625`**, event
`pull_request`, headSha `c336d4d849a54321afee14bc81762a3ffae39165`, conclusion **`success`**; `gh run view --json jobs`
lists one job, `bench`, `completed` / `success`, 23 of 23 steps `success`.

No other workflow has a run on the branch. Read from the files: `bench.yml` triggers on `push` to `main` and `claude/**`
and on `pull_request`, so this branch name was covered by `pull_request` only; `main.yml` triggers on `push` to `main`
with the two literal paths `main.py` and `.github/workflows/main.yml`, and on `workflow_dispatch`. No workflow names
`vps/selftest.py` (`grep -rn -E 'vps/selftest|selftest\.py' .github/workflows/` → no output, exit `1`), so none of the
gate's 23 steps is this TZ's selftest: every selftest figure in this report is this session's local run, not a runner
run.

Before the direct push to `main`, §8's two facts were read: `main.yml`'s `on.push` is a `paths` allow-list of two literal
paths (lines 29–31) with no `paths-ignore` key (its one occurrence of the string is inside a comment, line 25), and
`bench.yml`'s `paths-ignore` carries `**.md`.

## Final Repository State

The branch `tz-67-trend-book-in-code`, pushed before this report was written: head
`c336d4d849a54321afee14bc81762a3ffae39165` on `origin`, one commit above `1b3bab54317709f25141377899ad741b49b11b81`, the
commit the fingerprints were taken against. `git diff --stat origin/main...HEAD` → `3 files changed, 374 insertions(+),
3 deletions(-)`; `vps/book.py` is `100644`. `/tmp/tz67` is gone, no unit was started, stopped, restarted, enabled or
disabled, and no model session was opened. `vps/__pycache__/`, which the selftest and `py_compile` runs generated and
`.gitignore` excludes, is not tracked.

**NOT IN EFFECT UNTIL MERGED.** Merge is deployment on the VPS (contract §7 item 15): the deployer runs the selftest and
installs the change after the merge.

---

## Fingerprints

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — **2789** lines, MD5 `4e7388e346e79a4715af79a2fafa9e40`; revision string
`**Revision 2026-10-20-a.**` (the TZ requires the same). Reported, not enforced; equal to the TZ's figure.

**Anchors (contract §5 step 2).** The anchor table was cut by structure — every row between the separator line under
`| Anchor | Exact string that must be present |` and the first blank line — from the map. **Table's own row count: 7.
Compared against the TZ's `§0`: 7. Matched: 7.** Each anchor was matched with `grep -n -F` and `grep -n -o -F -m1`, which
print the matched text itself:

| Anchor | Text the first match returned | Every line carrying the string |
|---|---|---|
| revision | `17:**Revision 2026-10-20-a.**` | 17, 75 |
| direction engine | `76:### 3.12 Direction engine — veto cascade` | 76, 1045 |
| catalyst registry | `77:### 3.15 Catalyst registry` | 77, 1435 |
| exhaustion measure | `78:### 3.16 List exhaustion — the day-range measure` | 78, 1532 |
| analytical engine | `79:## 11. Analytical engine` | 79, 2521 |
| squeeze block | `80:### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 80, 1699 |
| newest invariant | `81:72. **A write that fails leaves this run's product or nothing` | 81, 2241 |

**Files the map's `## 0` table lists**, measured on `origin/main` at `1b3bab5`:

| File | Lines | MD5 | Stated |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**Files the TZ's gate adds**, measured on `origin/main` at `1b3bab5`:

| File | Lines | MD5 | Stated |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | equal; version line `**Version 30.**` |
| `vps/run.py` (before the patch) | 360 | `07f672e5bcea06be27508db66aa3a8e0` | equal |
| `vps/selftest.py` (before the patch) | 1830 | `ce6220cdf2a45709bd1f09596e209ee9` | equal |

After the patch: `vps/book.py` 282 / `f7ef81fceac48c69335a157e8c87f90f`; `vps/run.py` 364 /
`988f6f4955072f6429def95d3957d974`; `vps/selftest.py` 1915 / `2f966893b69ccc5981f35e83a370d5a9`.

**The `vps` tree:** `git rev-parse origin/main:vps` → `d013f2d9ac9209c9ac71dc7c6397696080b871aa` — the tree the TZ was
written against.
