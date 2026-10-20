# Implementation Report — TZ-68

## Status

COMPLETED

1. **The base.** `git merge-base --is-ancestor c336d4d origin/main; echo $?` → `1`: **TZ-67's branch
   `tz-67-trend-book-in-code` at `c336d4d849a54321afee14bc81762a3ffae39165` is NOT merged**, pull request #55 is open
   against `main`, and this TZ's work is built on that branch on purpose (contract §8, TZ-68 header). Pull request #56
   carries TZ-67's commit and TZ-68's own and names #55 superseded; this session neither closed nor commented on #55.
   **TZ-67's code is live nowhere, and neither is this TZ's.**
2. **The code.** The patch extracted from §11 by B1's one command: MD5 `b241f2ed6e53cb60b035bcf1803d2dcd`, 208 lines —
   the TZ's known answer. After `git apply`: `vps/book.py` 297 lines, MD5 `8478a66a57ad4c48b2579e8cb0e382d9`;
   `vps/selftest.py` 1965 lines, MD5 `18f1a8a38dade5a2f73fd89353ca8f67` — both B2's known answers, character for
   character.
3. **The checks.** `python3 vps/selftest.py` exit 0, `selftest: sections 24 checks 457 failed 0 empty 0`,
   `section O: checks 33 failed 0`, `section X: checks 19 failed 0`. The five negative controls failed **4, 2, 2, 2, 1**
   checks respectively — every failing check named by §9 and no other, **none outside section X in any of the five** —
   and after each revert `vps/book.py`'s digest was `8478a66a57ad4c48b2579e8cb0e382d9` again and V1 green again.

## Inbound Filing

None. The Boss's upload landed at the canonical path already: `CryptoTZ/TZ-68-book-due-entry.md`, added by `05ea392`
("Add files via upload", 20.10.2026 14:49 +0400) on `main`, which added that file and nothing else
(`git show --stat --name-status 05ea392` → one line, `A CryptoTZ/TZ-68-book-due-entry.md`). No `git mv` was needed and
none was performed. The clone was not shallow (`git rev-parse --is-shallow-repository` → `false`) and
`git fetch --all --prune` ran before anything was assessed (§3).

## Scope Executed

**Branch TZ** (contract §8): the scope names two files outside `CryptoReports/**`, so the class is read off the scope,
not chosen. Executed in full — Stage A (readings), Stage B (the patch, on the branch), V1–V4.

- Stage A: A1 — contract §4a steps 1–6 and the §5 gate against §0 including the added-files table; A1.1 the branch's
  revision; A1.2 the merge test; A1.3 the selftest on TZ-67's tree.
- Stage B: B1 the patch extraction and application, B2 the two digests, B3 the staged name-status, B4 the scratch
  directory removed.
- Nothing on the VPS, nothing started, no unit, no model session, no market host read (§1, §6 rule 1). The session's
  only network reads were `git`'s and `gh`'s.

## Files Created

None.

## Files Modified

```
vps/book.py        282 → 297 lines
vps/selftest.py   1915 → 1965 lines
```

Both on branch `tz-68-book-due-entry`, in commit `24385a6`, by `git apply` of §11's patch — extracted byte for byte by
B1's one command and never retyped (§6 rule 2).

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

§11's patch, applied to `c336d4d` and to nothing else. What it changes, as the TZ §3 names it:

1. **`replay(bars, open_now=None)`** — a signal at the last bar's close now fills at `open_now`, the open of the day
   still forming, with its stop `STOP_ATR` × ATR(20) from that fill, computed in the same statement as every other fill,
   so no second implementation of the stop exists (map inv. 38). The position carries `entry_due`. The guard became
   `if pos is None and k >= ENTRY_N and (k + 1 < len(bars) or open_now is not None):`, so without `open_now` — the
   `--archive` path — a signal at the last bar still opens nothing and **no archive trade moves**.
2. **`live_bars()`** returns the pair `(bars, open_now)` read from one response: the closed bars, and the forming day's
   open taken from field 1 of the row whose close time is not yet past. A read holding no forming day raises, so
   `--live` prints `state: "unread"` for that symbol rather than a state that cannot fill.
3. **`levels()`** prints `entry_due` beside `exit_due`, and `r_open: null` for a due entry, whose fill comes after the
   last close.
4. **`archive_series()`** refuses a day missing between two bars — an exchange gap, or a month the cache remembers as a
   404 from before the pair was listed — naming the symbol and the two dates around the gap, because `replay()` reads
   one bar per UTC day and a silent gap shifts every channel after it.
5. **`vps/selftest.py` section X** — the two live-path checks re-written for `live_bars()`'s pair, five added: the due
   entry in each of the two worlds is the very position the next close records, the due entry's state, `--live`'s due
   line, and the refused gap. Section X 14 → 19; `urllib.error` and `zipfile` imported for the two new stubs.
6. **`main()`'s `--live` branch** takes the pair and passes `open_now` into `replay()`.

No rule moved: entry 55 days, exit 20, stop 2 ATR(20), costs and the in-sample split are untouched, and `vps/run.py` was
not opened (TZ §5). The archive figures in TZ §3 are the audit's reading; this session ran neither `--archive` nor
`--live` against a market host (contract §7 item 9, TZ §5).

## Validation

Every item the TZ lists was run. Python available in this session: **3.12.3 only** (`python3 -V`); `python3.11` and
`python3.13` are not installed on this host. V1 asks for `python3 vps/selftest.py` and that is what ran — the TZ's
"Derived" clauses name the Architect's own runs under 3.11, 3.12 and 3.13 as the provenance of the known answers, not as
a step of this session.

### V1 — selftest, on the branch

```
$ python3 vps/selftest.py
...
section O: checks 33 failed 0
...
section X: checks 19 failed 0
selftest: sections 24 checks 457 failed 0 empty 0
$ echo $?
0
```

Baseline first, on TZ-67's tree (A1.3, `git checkout --detach origin/tz-67-trend-book-in-code`, HEAD
`c336d4d849a54321afee14bc81762a3ffae39165`): exit 0, `selftest: sections 24 checks 452 failed 0 empty 0`,
`section X: checks 14 failed 0`. **No regression:** sections A–W carry identical counts in both runs — A 32, B 12, C 4,
D 13, E 12, F 14, G 8, H 2, I 4, J 26, K 2, L 4, M 19, N 10, O 33, P 21, Q 3, R 9, S 35, T 39, U 18, V 16, W 102 — and
section X alone moved, 14 → 19. `452 + 5 = 457`.

### V1 — negative controls (inv. 68)

Each edit was applied **alone** in `vps/book.py` by exact single-occurrence string replacement (the anchor was asserted
to occur exactly once before each replacement), the selftest run, the file restored to the committed bytes, the digest
re-measured and V1 re-run. Failing check names are read from the selftest's own `FAIL section <N>: <label>` lines on
stderr.

| # | Edit | Exit | Summary line | Failing checks |
|---:|---|---:|---|---|
| 1 | `(k + 1 < len(bars) or open_now is not None)` → `k + 1 < len(bars)` | 1 | `selftest: sections 24 checks 457 failed 4 empty 0` | 4, all section X |
| 2 | `(t + DAY_MS, open_now)` → `(t + DAY_MS, c)` | 1 | `selftest: sections 24 checks 457 failed 2 empty 0` | 2, all section X |
| 3 | `forming = [float(r[1]) ...]` → `float(r[4])` | 1 | `selftest: sections 24 checks 457 failed 2 empty 0` | 2, all section X |
| 4 | `entry_due=bool(pos.get("entry_due"))` → `entry_due=False` | 1 | `selftest: sections 24 checks 457 failed 2 empty 0` | 2, all section X |
| 5 | `if b[0] - a[0] != DAY_MS:` → `if False:` | 1 | `selftest: sections 24 checks 457 failed 1 empty 0` | 1, section X |

The named checks, verbatim from stderr, against what §9 requires:

- **Control 1** — exactly 4, and exactly these: `a breakout close on the last bar is due at the forming open: the
  position the next close records` · `a stop day's close on the last bar is due too: the position the next close
  records` · `a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet` ·
  `--live names the entry due at the forming day's open, and its stop`. **Matches §9 control 1.**
- **Control 2** — `a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet`
  · `--live names the entry due at the forming day's open, and its stop`. **Matches §9 control 2.**
- **Control 3** — `live bars drop the day still open and keep its open` · `--live names the entry due at the forming
  day's open, and its stop`. **Matches §9 control 3.**
- **Control 4** — `a due entry's state: the forming day, the fill at its open, the stop 105.5 - 2 x 2.2, no open R yet`
  · `--live names the entry due at the forming day's open, and its stop`. **Matches §9 control 4.**
- **Control 5** — `a day missing from the archive is refused, never replayed over: the symbol and the days around it`.
  **Matches §9 control 5.**

In all five, the count of failing checks **outside section X was 0**: every other check of all twenty-four sections
stayed green, as §9 requires. After each revert: `vps/book.py` MD5 `8478a66a57ad4c48b2579e8cb0e382d9` restored, and
`python3 vps/selftest.py` exit 0 with `selftest: sections 24 checks 457 failed 0 empty 0`.

### V2 — syntax

```
$ python3 -m py_compile vps/book.py vps/selftest.py
$ echo $?
0
```

Standing checks of map §6 item 1 have no referent here — neither `index.html` nor `main.py` changed — and
`python3 -m py_compile main.py` was run anyway and exits 0. `__pycache__/` is ignored and nothing generated was
committed (`git status --porcelain` empty after the commit).

### V3 — scope

```
$ git diff --name-only origin/tz-67-trend-book-in-code...HEAD
vps/book.py
vps/selftest.py

$ git diff --name-only origin/main...HEAD
vps/book.py
vps/run.py
vps/selftest.py
```

Exactly the two lists the TZ states: this TZ's two files against TZ-67's branch, and the pull request's whole change —
TZ-67's `vps/run.py` included — against `main`. B3's staged check agreed before the commit:
`git diff --cached --name-status origin/tz-67-trend-book-in-code` printed exactly two lines, `M vps/book.py` and
`M vps/selftest.py`.

### V4 — pushes

Branch `tz-68-book-due-entry` pushed to `origin` (`* [new branch]`, tracking set) and pull request **#56** opened
against `main`, its description naming #55 superseded. `main` receives nothing from this session but this report
(contract §7 item 10, §8). Before writing to `main`, §8's standing condition was re-verified rather than assumed:
`.github/workflows/main.yml`'s `push` trigger carries a `paths` **allow-list** of exactly two literal entries,
`'main.py'` and `'.github/workflows/main.yml'`, and the file contains no `paths-ignore` key — its single occurrence of
that word is inside a comment (line 25). `CryptoReports/**` is unnamed, therefore out, so this report cannot start the
bot; Pages serves `index.html`, which this session did not touch.

## Test Results

| Item | Required | Measured | Verdict |
|---|---|---|---|
| A1.1 branch revision | `c336d4d849a54321afee14bc81762a3ffae39165` | `c336d4d849a54321afee14bc81762a3ffae39165` | pass |
| A1.2 merge test exit | `1` | `1` | pass (TZ-67 unmerged) |
| A1.3 selftest on `c336d4d` | exit 0, `sections 24 checks 452 failed 0 empty 0` | exit 0, `sections 24 checks 452 failed 0 empty 0` | pass |
| B1 patch MD5 / lines | `b241f2ed6e53cb60b035bcf1803d2dcd` / 208 | `b241f2ed6e53cb60b035bcf1803d2dcd` / 208 | pass |
| B1 `git apply --check` / `git apply` | exit 0 / exit 0 | exit 0 / exit 0 | pass |
| B2 `vps/book.py` | 297 / `8478a66a57ad4c48b2579e8cb0e382d9` | 297 / `8478a66a57ad4c48b2579e8cb0e382d9` | pass |
| B2 `vps/selftest.py` | 1965 / `18f1a8a38dade5a2f73fd89353ca8f67` | 1965 / `18f1a8a38dade5a2f73fd89353ca8f67` | pass |
| B3 staged name-status | 2 lines, `M` + `M` | 2 lines, `M` + `M` | pass |
| B4 scratch removed | `/tmp/tz68` gone | `ls: cannot access '/tmp/tz68'` | pass |
| V1 selftest | exit 0, `457 failed 0 empty 0`, O 33/0, X 19/0 | exit 0, `457 failed 0 empty 0`, O 33/0, X 19/0 | pass |
| V1 controls 1–5 | failed 4 / 2 / 2 / 2 / 1, named checks only | failed 4 / 2 / 2 / 2 / 1, named checks only, 0 outside X | pass |
| V2 py_compile | exit 0 | exit 0 | pass |
| V3 scope, both diffs | 2 files / 3 files as stated | 2 files / 3 files as stated | pass |
| V4 push + PR | branch pushed, PR naming #55 superseded | branch pushed, PR #56 | pass |

457 is a count of comparisons the selftest itself reports, not an estimate (inv. 43); `empty 0` is its own statement
that no section verified nothing (inv. 22).

## Deviations

None.

Two facts that are not deviations and are stated so they are not mistaken for one:

- The session has Python **3.12.3 only**; 3.11 and 3.13 are absent from this host. V1 names one command and it ran. The
  three-version provenance in the TZ's "Derived" lines is the Architect's session's, not a step asked of this one.
- The TZ's own scratch path `/tmp/tz68` was used verbatim, as §6 rule 2 and B1 require (one command, not retyped),
  rather than this session's scratchpad directory; B4 removed it.

## Pre-existing Issues

None found. Every fingerprint the gate measures matched exactly — the map's four files, the contract, and both `vps`
files on TZ-67's branch — so nothing in §0's table is ahead of anything else, and no file differed from the figure the
map or the TZ states.

Noted without action, because it is the TZ's own design and the audit's decision, not a defect: **pull request #55 is
open and unmerged**, so TZ-67's `vps/book.py`, `vps/run.py` and section X exist on no merged line. #56 supersedes it and
carries both commits; if #55 were merged instead of #56, this TZ's repair would be absent while the output it corrects
would be live.

## Remaining Risks

- **Nothing calls `vps/book.py` after the merge.** The TZ fixes that deliberately in §5: no caller exists, and the
  methodology edit after this TZ's audit moves the trader onto `--live` and decides how a due entry prints and what the
  trader does when the market has already left its fill. Until then the due entry is correct and unread by anybody.
- **The due entry's fill is the forming day's open as the exchange reported it in that one response.** The program
  books it; the market may be far from it by the time a human reads the line. That gap is the methodology edit's
  subject, named in §5, and is not a property of this code.
- **`archive_series()`'s refusal is strict by design and acts on the cache too.** A month cached as a 404 from before a
  pair was listed now raises instead of yielding a short series, so a symbol whose archive genuinely begins mid-range
  will refuse rather than replay. The TZ's discarded alternatives record this as the chosen direction: a silent gap
  shifts every channel after it, and refusing is the cheaper failure.
- **Both halves of the live read come from one response.** If a venue ever returns the forming day without the open
  field, or omits the forming row during a rollover second, the symbol prints `unread` for that tick — the intended
  behaviour, and visible as such only to a caller that distinguishes `unread` from `flat`. No caller exists yet (above).
- The repair is proved by 19 checks of section X against stubs and by the audit's archive measurement quoted in TZ §3;
  this session measured no market host, by §1 and §6 rule 1.

## Commit

Implementation, on branch `tz-68-book-due-entry`, commit `24385a6` — made and pushed before this report was written,
therefore a measurement:

```
TZ-68: vps — the book's morning: a signal at the last close is an entry due at the forming day's open; a day missing from the archive is refused
```

Contents: `vps/book.py` and `vps/selftest.py`, modified; nothing else (V3, B3).

This report's own commit, on `main`, carries the message the TZ authorises and nothing is stated about its outcome
(inv. 54):

```
TZ-68: report — the book's due entry
```

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/56** — `tz-68-book-due-entry` → `main`, carrying TZ-67's commit
`c336d4d` and TZ-68's `24385a6`. Its description names pull request **#55 superseded**. #55 was neither closed nor
commented on by this session (TZ §4).

## CI Execution

`.github/workflows/bench.yml` — the Bench gate — fires on `pull_request`, and opening #56 started it:
**run `39411169878`**, event `pull_request`, branch `tz-68-book-due-entry`. Its conclusion was read from the API and is
stated below; the hosted gate is in any case read by the audit, which opens the pull-request page to merge
(contract §9).

`.github/workflows/main.yml` did **not** run and cannot: its `push` trigger is limited to `branches: [ main ]` with a
two-literal `paths` allow-list that names neither changed file. `backtest_bench.yml`, `calib.yml` and `journal.yml` were
not triggered by this change. The branch's own `push` event does not start the Bench gate either —
`bench.yml`'s push filter is `branches: [ main, 'claude/**' ]` and this branch is named `tz-68-book-due-entry`, outside
that pattern; the `pull_request` trigger is what covers it, which is why #56 existing is what put the gate behind this
work.

**Measured, from the API, not assumed:** run `39411169878`, workflow `Bench gate`, event `pull_request`, branch
`tz-68-book-due-entry`, status **completed**, conclusion **success**, job `bench` (id `118589009682`) green in 56s. All
fourteen bench steps — steps 6 through 19 of the job, `verify_board.js` through `backtest_guard_bench.py` — concluded
`success`; the job's only annotations are the runner's own notices about Node 20's deprecation and the `ubuntu-latest`
label migration, which are not failures and are not this change's. One run exists for this branch and that is it
(`gh run list --branch tz-68-book-due-entry`).

So the gate did execute on a runner, on the pull request's merge ref, and it is green. No part of this report's CI
statement is a forecast.

## Final Repository State

Branch **`tz-68-book-due-entry`** at `24385a6`, pushed to `origin` and tracked, carrying `c336d4d` (TZ-67) as its
parent's line and this TZ's single commit on top. Its tree differs from `origin/tz-67-trend-book-in-code` in exactly
`vps/book.py` and `vps/selftest.py`, and from `origin/main` in exactly those two plus `vps/run.py`. Working tree clean
(`git status --porcelain` empty), no scratch file left: `/tmp/tz68` removed at B4, `__pycache__/` ignored and never
staged. No unit, timer or service was installed, enabled, started or left running anywhere, and the VPS was not read or
changed (contract §7 item 15, TZ §6 rule 1).

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Taken against `origin/main` at `05ea392` after `git fetch --all --prune`, before any work (contract §5). The clone is
not shallow.

**`SYSTEM-MAP-CRYPTOCALCUL.md`** — 2789 lines, MD5 `4e7388e346e79a4715af79a2fafa9e40`, revision string
`**Revision 2026-10-20-a.**`. Required by the TZ header: `**Revision 2026-10-20-a.**` — **equal**. The line count and
MD5 are reported, not enforced, and both equal the figure the map's own §0 states (2789 / `4e7388e346e79a4715af79a2fafa9e40`).

**The anchor table, cut by its STRUCTURE.** The list was taken from the map's own table — every row between its
separator line `|---|---|` and the first line that is not a table row — and never by matching anchor names:

```
$ awk '/^\| Anchor \| Exact string that must be present \|$/{f=1;next} f&&/^\|---\|---\|$/{s=1;next} s&&!/^\|/{exit} s{print}' SYSTEM-MAP-CRYPTOCALCUL.md | wc -l
7
```

**The table's own row count is 7, and the number compared is 7.** All seven rows are quoted in the TZ header character
for character (each row matched with `grep -Fxq` against the TZ file: 7 quoted, 0 missing). Per anchor, the command and
the text the match returned — a fixed-string match printing the matched text itself, never a verdict or a count of
passes:

| Anchor | Command | Hits | Text the match returned |
|---|---|---:|---|
| revision | `grep -o -m1 -F -- '**Revision 2026-10-20-a.**' SYSTEM-MAP-CRYPTOCALCUL.md` | 2 | `**Revision 2026-10-20-a.**` |
| direction engine | `grep -o -m1 -F -- '### 3.12 Direction engine — veto cascade' …` | 2 | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `grep -o -m1 -F -- '### 3.15 Catalyst registry' …` | 2 | `### 3.15 Catalyst registry` |
| exhaustion measure | `grep -o -m1 -F -- '### 3.16 List exhaustion — the day-range measure' …` | 2 | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `grep -o -m1 -F -- '## 11. Analytical engine' …` | 2 | `## 11. Analytical engine` |
| squeeze block | `grep -o -m1 -F -- '### 3.17 «РИСК ВЫНОСА» — the day's own risk' …` | 2 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `grep -o -m1 -F -- '72. **A write that fails leaves this run's product or nothing' …` | 2 | `72. **A write that fails leaves this run's product or nothing` |

Each anchor is present as an exact, case-sensitive substring; two hits each, the anchor table's own row and the text it
points at. Anchors compared: 7 of 7 table rows.

**Every file the map's `## 0` table lists**, measured on `origin/main`:

| File | Required | Measured | Verdict |
|---|---|---|---|
| `index.html` | 3799 / `4e71da9badca3ccae85b656fdc3773e8` | 3799 / `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 / `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 / `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**The files the TZ's gate adds:**

| File | Required | Measured | Verdict |
|---|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 858 / `25fac2ff37d2cb12f4bf0e35ce9c9b06`, version line `**Version 30.**` | 858 / `25fac2ff37d2cb12f4bf0e35ce9c9b06`, line 3 reads `**Version 30.**` | equal, not BLOCKED (inv. 59) |
| `vps/book.py` at `origin/tz-67-trend-book-in-code` | 282 / `f7ef81fceac48c69335a157e8c87f90f` | 282 / `f7ef81fceac48c69335a157e8c87f90f` | equal — §11's patch applied to exactly these bytes |
| `vps/selftest.py` at `origin/tz-67-trend-book-in-code` | 1915 / `2f966893b69ccc5981f35e83a370d5a9` | 1915 / `2f966893b69ccc5981f35e83a370d5a9` | equal — as above |

`main` holds no `vps/book.py`, as the TZ states: `git cat-file -e origin/main:vps/book.py` →
`fatal: path 'vps/book.py' does not exist in 'origin/main'`. The two `vps` figures were measured on the branch with
`git show origin/tz-67-trend-book-in-code:<file>`.

**After this TZ's patch**, for the audit's comparison: `vps/book.py` 297 / `8478a66a57ad4c48b2579e8cb0e382d9`,
`vps/selftest.py` 1965 / `18f1a8a38dade5a2f73fd89353ca8f67`.
