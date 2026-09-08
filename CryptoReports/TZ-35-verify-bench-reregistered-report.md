# Implementation Report — TZ-35

**The previous TZ's branch is NOT merged.** `claude/tz-34-fetched-venue-observed` is
unmerged at the time of writing (`git merge-base --is-ancestor a73359d origin/main` →
false). This is the premise of TZ-35 rather than a surprise: TZ-34's implementation is
accepted and unmerged only because it left gate step 4 red. This TZ continues that branch
and opens none of its own, so both commits merge together under one pull request (§8 head
note).

## Status

**COMPLETED.**

Every validation item in TZ-35 §5 was run. One sub-item of §5.6 could not be read: the
runner's per-step CHECK COUNTS, including the garrison's, live only in the workflow log
body, and that endpoint answers `403 Must have admin rights to Repository` to this
session. The per-step CONCLUSIONS were read and are reported below. Under contract §9 an
unreadable runner figure is not a PARTIAL — the work is complete — but the gap is stated
here rather than filled with the local number.

## Inbound Filing

None. `CryptoTZ/TZ-35-verify-bench-reregistered.md` arrived on `main` at commit `74c0368`
already carrying its canonical filename; nothing was moved or renamed.

## Scope Executed

**Branch TZ** (contract §8): it authorises one written file outside `CryptoReports/**`,
so it opens a branch and takes the pull-request path. The branch is TZ-34's, continued.

TZ-35 §2.1, §2.2 and §2.3, all in `bench/verify_bench.py` and nothing else.

## Files Created

None.

## Files Modified

- `bench/verify_bench.py` — 287 → 388 lines; `520777380f2ec69a3d05d792d78c7f78` →
  `06036d8c3d39ccec6be21d2158ef3ce1`. Sole file in the diff (`git diff --name-only
  a73359d` prints exactly this path).

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### §2.1 — the fixtures carry an OBSERVED census

`make_cache` now writes a `cov` into every document it creates. The census is built by
calling `bb.census_of_doc` on the document just assembled, never assembled as a literal:
a hand-written census is a second implementation of a production function and drifts from
it silently (inv. 21, 38).

- `t_ref` is the fixture's own last bar (`px[-1][0]`). `census` derives `tail` against the
  close of the last COMPLETE hour, so `tail` is 0, and the series is contiguous hourly, so
  `gaps` is empty. Both were verified by the outcome that depends on them: case 9 still
  classes `AAA` as `unexplained` and not `coverage`, which is exactly the cell a tail
  deficit would have moved.
- The venue is a new per-symbol argument `venues`, defaulting to spot. `census_of_doc`
  rebuilds a census from `prices` and cannot recover a venue from them, so this is the one
  field the fixture must state. A fixture declaring the world it tests is not the
  defaulting TZ-34 §2.2 forbids — that prohibition is on production inventing an
  observation it never made.
- The venue values are read from production's own names, `bb.VENUE_PERP` and
  `bb.VENUE_SPOT`. No venue string literal was introduced into this bench (inv. 65).

### §2.2 — case 10 becomes three lanes

| Lane | Declared `fut:true` | Series venue | Required class | Required exit | Result |
|---|---|---|---|---:|---|
| A | yes | perp | `venue-basis` | 0 | green |
| B | yes | **spot** | `unexplained` | non-zero | green |
| C | **no** | perp | `venue-basis` | 0 | green |

- **A** is the pre-existing lane, now correctly conditioned by a cache in which `AAA` is
  observed on the perpetual. Its assertion that the class set IS the «БАЗИС ПЕРП/СПОТ»
  note — `basis_sets(out)[0] == basis_sets(out)[1]` — is preserved **as written**. TZ-34
  changed that note's text (it now reads «серия качана с перпетуала, справочно, не
  провал»); the parser survives the change unmodified, which is confirmed by lane A being
  green rather than assumed.
- **B** is the behaviour TZ-34 introduced and which nothing asserted end-to-end before: a
  declaration no longer buys a licence. Two checks — non-zero exit, and `AAA unexplained`
  with no basis note printed at all.
- **C** is the UNI/XLM/ZEC shape: a coin never declared, cached on the perpetual, earning
  the licence. Two checks — exit 0, and the class set and the note both equal
  `{('AAA', 'r30')}`.
- **The fourth assertion is the strongest and is the point of the pair.** Lanes A and C
  run the same cache and the same mutation and differ only in the declaration; they must
  produce the same exit code and the same class set, with that set non-empty so the
  equality cannot pass on two empty sets (inv. 22). An equality holding across a varied
  input is what «this input no longer decides» means.

Lane C uses an HTML that names `AAA` WITHOUT `fut` rather than `html=None`. With no file
at all the parse path itself would differ, and the equality would no longer isolate the
declaration as the single varying input.

### §2.3 — the five sites that crash instead of reporting

`out.strip().splitlines()[-1][:150]` appeared five times as the `info` argument of `ok(...)`.
Python evaluates that argument BEFORE `ok` is called, so empty output raises `IndexError`
on a check that was about to PASS and the bench dies mid-run. All five now call one
helper, `last_line(out)`, which returns `''` on empty input. No expected total was added:
a bench asserting a hardcoded count of its own checks is a numeral that stops moving with
the file it judges (inv. 65).

### A defect in the first cut of these fixtures, found by the TZ's own negative control

The first implementation put the two HTML fixtures inside the cache directory, where the
pre-existing `html_fut` already lived. That was safe before this change — no `make_cache`
call followed it — but the lanes require a `make_cache` between them, and `make_cache`
**empties the directory it writes to**. The declaration was therefore deleted before any
lane ran, and all three lanes passed with nothing declared at all.

The bench was green. It was green while asserting nothing about the input it exists to
vary — precisely the failure direction TZ-35's own header names ("a fixture built
carelessly re-greens the gate while asserting nothing, which is worse than the red it
replaces"). It was caught by §5.3, which read lane A red and lane B green — the exact
inverse of the specified control — rather than by inspection.

The repair: the HTML fixtures move to a second temporary directory, `tmp_in`, because a
token list is not a cache document. Both directories are removed at the end of the run.
After the repair the control reads exactly as §5.3 specifies.

## Validation

### §5.0 — fingerprint gate (contract §5), run before any work

Fetched first; `origin/main` moved `76fa86e..74c0368` and the worktree was brought to it.
`git diff --stat 76fa86e 74c0368` shows the TZ file added and nothing else — no TZ was
replaced in place.

- Map revision string: **`**Revision 2026-09-08-a.**`** — present, matches the TZ header.
- All seven content anchors present as exact substrings, including
  `66. **A published level and the price it was computed at are one fact.**`.
- The map is byte-identical on `origin/main` and on the branch (both blob
  `2189140278dc005fff040b95350fc82759a0d7e2`), as the TZ states.
- Every file in the map's `## 0` table matches its stated line count and MD5 exactly (four
  of four; table read from the repository, not from the TZ quote).

**Branch-head gate table — both figures matched exactly**, so the branch is where the
TZ-34 report left it:

| File | Required | Measured | |
|---|---|---|---|
| `bench/backtest_bench.py` | 3881 · `45e2294c5fc82f96a7e66b84c2a094c2` | 3881 · `45e2294c5fc82f96a7e66b84c2a094c2` | match |
| `bench/backtest_guard_bench.py` | 971 · `19427e79133d48870d76eb0c908c69f6` | 971 · `19427e79133d48870d76eb0c908c69f6` | match |

**`bench/verify_bench.py` ANCHORS — all six present at the exact required count:**

| Anchor | Required | Found |
|---|---:|---:|
| `json.dump({'prices': px, 'volumes': vol, 'src': 'synthetic'},` | 1 | 1 |
| `out.strip().splitlines()[-1][:150]` | 5 | 5 |
| `ok('fut basis: return gap exits 0 with html', code == 0, 'exit=%s' % code)` | 1 | 1 |
| `ok('single outlier exits non-zero and is classified unexplained',` | 1 | 1 |
| `def basis_sets(text):` | 1 | 1 |
| `print('checks run: %d   FAIL %d' % (checks[0], len(fails)))` | 1 | 1 |

The bench reported **35 checks** at the specification, as the TZ states.

### §5.1 — compile and scope

- `python3 -m py_compile bench/verify_bench.py` → clean, exit 0.
- `git diff --name-only` against the branch head → exactly `bench/verify_bench.py`.
- Four files against the branch head, all **unchanged**:

| File | Branch head | After | |
|---|---|---|---|
| `index.html` | `4e71da9badca3ccae85b656fdc3773e8` | `4e71da9badca3ccae85b656fdc3773e8` | unchanged |
| `main.py` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | unchanged |
| `bench/backtest_bench.py` | `45e2294c5fc82f96a7e66b84c2a094c2` | `45e2294c5fc82f96a7e66b84c2a094c2` | unchanged |
| `bench/backtest_guard_bench.py` | `19427e79133d48870d76eb0c908c69f6` | `19427e79133d48870d76eb0c908c69f6` | unchanged |

No lane required a production-side edit, so §3.1's BLOCKED branch was never reached.

### §5.2 — the bench itself

`python3 bench/verify_bench.py` → **`checks run: 40   FAIL 0`**, exit 0.

The count is published as measured; no total was predicted beforehand (inv. 43). Delta
against 35 is **+5**, attributed lane by lane:

| Added check | Lane | Δ |
|---|---|---:|
| `lane C: an UNDECLARED coin cached on the perpetual still exits 0` | C | +1 |
| `lane C: it is classified venue-basis and named in the basis note` | C | +1 |
| `lanes A and C agree exactly — the declaration decides nothing` | A≡C | +1 |
| `lane B: a declaration over a SPOT series buys no licence — exits non-zero` | B | +1 |
| `lane B: the cell is unexplained and no basis note is printed` | B | +1 |
| | **total** | **+5** |

Lane A contributed no new check: its three checks are the pre-existing ones, re-conditioned
and not renamed. `ok(` call sites went 26 → 31, the same +5.

### §5.3 — the lanes assert something (negative control, inv. 23, 45, 65)

A scratch copy of `backtest_bench.py` was written to `/tmp/tz35_ctl_backtest.py` — never
the repository's — with the pre-TZ-34 licence restored: the `_cell_class` call site in
`reconcile` replaced by the `if sym in fut:` block taken verbatim from commit `b5757f9`.
Re-running this bench against it:

`checks run: 40   FAIL 5`, exit 1.

| Lane | §5.3 requires | Read |
|---|---|---|
| A | stays GREEN | **green** — all three checks pass |
| B | goes RED | **red** — both checks: `exit=0 — the declaration granted a licence again` |
| C | goes RED | **red** — both checks: `exit=1`, `AAA unexplained` |
| A≡C equality | (follows) | **red** — `A exit=0 {('AAA', 'r30')} · C exit=1 set()` |

This is the localisation the TZ asked for rather than an all-flip: lane A is the one cell
on which the two rules agree, and it is the one lane that does not move. Every check
outside case 10 also stayed green, so the control moved the licence and nothing else.

### §5.4 — the crash repair is proven, not asserted

A second scratch copy, `/tmp/tz35_mute_backtest.py`, returns from `verify_against_live`
before printing anything. Both benches were run against that same input.

- **Before the repair** (branch-head `verify_bench.py`, restored from `a73359d`):
  ```
  Traceback (most recent call last):
    File "/tmp/tz35_verify_prerepair.py", line 166, in <module>
      out.strip().splitlines()[-1][:150])
      ~~~~~~~~~~~~~~~~~~~~~~~~^^^^
  IndexError: list index out of range
  ```
  The run dies at the first of the five sites. **No count is printed at all** — every check
  after it is lost, and the summary line never runs.
- **After the repair:** runs to completion, prints `checks run: 40   FAIL 23`, lists all
  23 failures by name, exits 1.

The repair converts a silent truncation into 23 named failures and an honest count.

### §5.5 — gate replay, `bench.yml` steps 1–14, before and after

Before = the branch head `a73359d`, materialised clean via `git archive` to
`/tmp/tz35_before` (its `verify_bench.py` MD5 confirmed equal to the branch-head blob).
After = this commit. Each of the 14 steps was run independently on both trees, so a step
after the red one still produces a reading — a hosted run would have skipped it.

| Step | Bench | Before | After | Δ |
|---:|---|---|---|---|
| 1 | `verify_board.js` | 109, exit 0 | 109, exit 0 | 0 |
| 2 | `board2_bench.js` | 130, exit 0 | 130, exit 0 | 0 |
| 3 | `prot_bench.js` | PASS 372, exit 0 | PASS 372, exit 0 | 0 |
| **4** | **`verify_bench.py`** | **35, FAIL 8, exit 1 — RED** | **40, FAIL 0, exit 0 — GREEN** | **+5** |
| 5 | `direction_bench.py --props --fixtures --control --sim` | exit 1 | exit 1 | 0 (see below) |
| 6 | `fresh_bench.js` | 3 424, exit 0 | 3 424, exit 0 | 0 |
| 7 | `journal_bench.js` | 691 836, exit 0 | 691 836, exit 0 | 0 |
| 8 | `catalyst_bench.js` | 24 692, exit 0 | 24 692, exit 0 | 0 |
| 9 | `display_bench.py` | 24 598, exit 0 | 24 598, exit 0 | 0 |
| 10 | `render_bench.py` | 16 171 (123 scenarios), exit 0 | 16 171 (123 scenarios), exit 0 | 0 |
| 11 | `direction_bench.py --display` | 15 629, exit 0 | 15 629, exit 0 | 0 |
| 12 | `exhaustion_bench.js` | 220 598, exit 0 | 220 598, exit 0 | 0 |
| 13 | `live-gate.sh --selftest` | 40, exit 0 | 40, exit 0 | 0 |
| 14 | `backtest_guard_bench.py` | 174, exit 0 | 174, exit 0 | 0 |

**Step 4 moves RED → GREEN and its count rises by exactly the five lane checks. Every
other step reads delta zero.** Step 14 reads **174 on both sides**: the garrison was not
touched, so there is no §3.1 breach.

Step 5 is red on BOTH sides and is environmental, not this change. It fails in the
`--control`/`--sim` arm with a V8 heap allocation failure
(`v8::internal::Factory::CopyFixedDoubleArray`, `Runtime_CreateArrayLiteral`, then `node
failed`) on a machine with 955 MB of RAM. Its `--props` (60 000 scenarios) and `--fixtures`
sub-stages both print `[OK ]` before the OOM. The same step is **green on the hosted
runner** for this commit (§5.6), which settles it: the local red is the machine, not the
repository.

### §5.6 — the hosted run

The branch was pushed and `Bench gate` **#143** ran on branch head `b13fb71`:
**conclusion `success`**, run id `34259812506`.

`https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/34259812506`

The premise of §5.6 is confirmed by the previous run. **#142** on `a73359d` concluded
`failure`, and its per-step reading shows the gate halting exactly where the TZ says:

- job step 9 (`Офлайн-набор для --verify (verify_bench.py)`) → `failure`
- job steps 10–19 (gate steps 5–14, including the garrison) → **`skipped`**

So gate steps 5–14 had never had a runner reading on this branch, as §5.6 states. On
**#143** all 23 job steps read `success`, gate steps 1–14 among them:

| Gate step | Job step | Conclusion |
|---:|---|---|
| 1 | `verify_board.js` | success |
| 2 | `board2_bench.js` | success |
| 3 | `prot_bench.js` | success |
| 4 | `verify_bench.py` | **success** |
| 5 | `direction_bench.py` | success |
| 6 | `fresh_bench.js` | success |
| 7 | `journal_bench.js` | success |
| 8 | `catalyst_bench.js` | success |
| 9 | `display_bench.py` | success |
| 10 | `render_bench.py` | success |
| 11 | `direction_bench.py --display` | success |
| 12 | `exhaustion_bench.js` | success |
| 13 | `live-gate.sh --selftest` | success |
| 14 | `backtest_guard_bench.py` (garrison) | success |

**The garrison's runner-measured CHECK COUNT could not be read, and no substitute is
offered.** Per-step conclusions come from the jobs API, which answers unauthenticated;
check counts exist only in the log body, and both
`/actions/runs/34259812506/logs` and `/actions/jobs/102174655519/logs` answer
`403 {"message": "Must have admin rights to Repository."}`. This session has no `gh` and
no token. The local reading of step 14 remains 174 on both sides of the replay, but that
is a local number and does not supersede anything — the runner figure the TZ asked for is
unread, and the actor who opens the run page can read it (contract §9).

### §3 — negative assertions, each checked

1. **`backtest_bench.py` and `backtest_guard_bench.py` byte-identical to the branch head** —
   confirmed by MD5 in §5.1. No lane needed a production-side edit.
2. **`index.html` and `main.py` byte-identical** — confirmed by MD5 in §5.1.
3. **The check count does not fall** — 35 → 40. The floor holds; the change only adds.
4. **The `SPEC` metric loop is untouched** — the ten-check loop region is **byte-identical**
   to the branch head (`diff` of the extracted region returns empty). Neither moved nor
   renumbered.
5. **Case 9 still classes `AAA` as `unexplained`** — `single outlier exits non-zero and is
   classified unexplained` is green, asserting both `code != 0` and the literal string
   `AAA unexplained`. The census §2.1 introduced did not move that cell into `coverage`.
6. **«systemic breach (all coins) still fails after v3» stays green throughout** — green in
   the baseline (not among the 8 failures) and green after. Its two source lines, mutation
   `bump_level` and expectation `code != 0`, are **byte-identical** to the branch head.
7. **No threshold, class name or `SPEC` entry moves** — the diff contains no threshold
   literal, no `SPEC` line and no class name in changed code; the only matches for
   "threshold" in the diff are the English words inside new comments.

### Standing checks

Not applicable in the sense that matters and stated rather than skipped: contract §9's
`py_compile main.py` / `node --check` on `index.html` are required **whenever a production
file changes**, and no production file changed here (§5.1). `py_compile` was nevertheless
run on the one file that did change, and is clean.

## Test Results

| Item | Result |
|---|---|
| §5.1 compile | `py_compile bench/verify_bench.py` clean |
| §5.1 scope | `git diff --name-only` = `bench/verify_bench.py`, one path |
| §5.1 four hashes | all four unchanged vs branch head |
| §5.2 the bench | **40 checks, FAIL 0, exit 0** (was 35 / FAIL 8 / exit 1) |
| §5.3 negative control | 40 checks, FAIL 5 — A green, B red, C red, as specified |
| §5.4 crash repair | before: `IndexError`, no count · after: 40 checks, FAIL 23, exit 1 |
| §5.5 gate replay 1–14 | step 4 RED → GREEN (+5); all 13 other steps delta zero |
| §5.6 hosted run | `Bench gate` #143, `b13fb71`, **success**, 14/14 gate steps green |
| §5.6 garrison runner count | **NOT READ** — log endpoint 403, no credential |

Working tree clean; no scratch artifact committed (`bench/__pycache__` is ignored by
`.gitignore:19`). The scratch copies used by §5.3 and §5.4 were written under `/tmp` and
never in the repository.

## Deviations

None from the specification.

One implementation choice not dictated by the TZ, recorded because a reader would
otherwise have to infer it: lane C uses an HTML declaring `AAA` **without** `fut` rather
than `html=None`. Both satisfy "Declared `fut:true`: no". The file was chosen so that the
declaration is the only difference between lanes A and C — with no file at all the parse
path itself would differ, and §2.2's equality assertion would no longer isolate the
declaration.

## Pre-existing Issues

1. **Gate step 5 cannot run in this session's environment.** `direction_bench.py --props
   --fixtures --control --sim` dies with a V8 heap OOM on a 955 MB machine, identically on
   both sides of the replay, on trees whose only difference is `verify_bench.py`. It is
   **green on the hosted runner** for this commit. Environmental; not a repository defect
   and not caused by this TZ. Recorded so a future local replay is not misread as a
   regression.
2. **`R["fut"]` is computed, returned and read by nobody.** Verified against the
   repository rather than taken from the TZ-34 report: `reconcile` returns
   `"fut": sorted(fut)` at `bench/backtest_bench.py:1512`, and a repository-wide search for
   a read of that key returns nothing. TZ-35 §6 places it out of scope and it was not
   touched. It belongs to a cleanup, not to a TZ that must turn a gate green without
   editing the file it lives in.
3. **Step 7 reads 691 836 on this branch, against the 691 109 / 693 895 recorded in the
   map's `## 0`.** Both sides of the replay read the same figure, so it is not this TZ's.
   The map calls step 7 "the first figure to read after TZ-33" and predicts a FALL from
   693 895; the reading is 2 059 below that, so it moves in the predicted direction. **The
   magnitude is NOT attributed here** — attribution is outside this TZ's scope, the map
   requires a fall to be attributed rather than assumed benign, and a guess would be worse
   than a stated gap. Note also that the recorded figures are runner readings and this one
   is local. Flagged for the Architect.

## Remaining Risks

1. **The lanes assert the licence through `--verify`'s exit code and printed output, not
   through `_cell_class` directly.** That is what the TZ asked for — end-to-end is the gap
   it names — but it means a refactor that changed the printed note's shape could turn
   lanes B or C red for a presentational reason. `basis_sets` is the shared parser and
   lane A's preserved assertion is the guard against that reading drifting unnoticed.
2. **`make_cache` empties the directory it writes to, and that is now load-bearing.** The
   HTML fixtures are outside the cache directory for exactly this reason. A future fixture
   placed inside `tmp` after a `make_cache` call would be deleted silently — the failure
   this TZ hit once. The comment at `tmp_in` states the constraint at the site.
3. **The venue fixture states an observation production cannot verify.** `make_cache` sets
   `cov['venue']` directly because `census_of_doc` cannot recover it. That is correct for a
   fixture, but it means these lanes test the CLASSIFIER's reading of the field and not the
   FETCHER's writing of it. The fetcher's side is the garrison's (step 14, section E,
   "venue-as-observation: 32 comparisons").

## Commit

One implementation commit, on `claude/tz-34-fetched-venue-observed`, already pushed when
this section was written:

**`b13fb716761144b35484f0daec044d37217b99f2`** — `TZ-35: verify_bench re-registered
against the observation`

Contents: `bench/verify_bench.py` only, 114 insertions, 13 deletions. The TZ carries no
`## Commit Message` section, so the message was composed in the style of the branch's
first commit; its body states the three changes, the fixture-directory repair, the
35/8/exit 1 → 40/0/exit 0 movement, and that no production file was touched.

This report's own commit is not described here and carries no hash (inv. 54, contract §10).

## Pull Request

**No pull request exists.** This session cannot open one: `gh` is absent and no
`GH_TOKEN`/`GITHUB_TOKEN` is present in the environment. Under contract §8 this is the
defined fallback and not a blocker.

- Branch: **`claude/tz-34-fetched-venue-observed`**
- Compare URL: **https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-34-fetched-venue-observed**

The branch carries **both** commits — TZ-34's `a73359d` and TZ-35's `b13fb71` — and merges
once, as the TZ specifies. The Boss opens and merges from that link in one action, after
the Architect's verdict.

## CI Execution

**`Bench gate` executed on a GitHub runner for this commit.**

| | |
|---|---|
| Workflow | `Bench gate` (`.github/workflows/bench.yml`) |
| Run | **#143**, id `34259812506` |
| Head SHA | `b13fb71` |
| Status | completed |
| **Conclusion** | **`success`** |
| Gate steps | 14 of 14 green (all 23 job steps `success`) |
| URL | https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/34259812506 |

Prior run on the same branch, read for the before-side: **#142**, id `34239183167`, head
`a73359d`, conclusion **`failure`**, halting at `verify_bench.py` with gate steps 5–14
`skipped`.

Read over the REST API (`/actions/runs`, `/actions/runs/{id}/jobs`), which answers
unauthenticated for this public repository. **Log bodies were not readable** (403, admin
rights required), so no runner-measured check count is reported for any step. No other
workflow ran: `main.yml`'s trigger is a two-path `paths` allow-list (`main.py`,
`.github/workflows/main.yml`) and this change touches neither.

## Final Repository State

**NOT IN EFFECT UNTIL MERGED.**

The branch `claude/tz-34-fetched-venue-observed` at **`b13fb71`**, pushed before this
report was written and therefore measured, not forecast. It carries two commits ahead of
`main`: `a73359d` (TZ-34) and `b13fb71` (TZ-35). Working tree clean at the time of the
push. `main` is untouched by the implementation; the direct-push path used for this report
is `CryptoReports/**` under contract §8, and `main.yml`'s `paths` allow-list was read and
confirmed to be an allow-list of two literal paths before that push, so nothing here can
start the bot or change what Pages executes.

## Fingerprints

Measured at the branch head `b13fb71`.

**System Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — **2384 lines**,
MD5 `7807a6787f5db7b0d52eb9916b781ffe`, revision string **`Revision 2026-09-08-a`**.

Every file the map's `## 0` table lists, read from that table at authoring time:

| File | Lines | MD5 | vs map |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

Files the TZ's gate table adds:

| File | Lines | MD5 | vs TZ |
|---|---:|---|---|
| `bench/backtest_bench.py` | 3881 | `45e2294c5fc82f96a7e66b84c2a094c2` | match |
| `bench/backtest_guard_bench.py` | 971 | `19427e79133d48870d76eb0c908c69f6` | match |

The file this TZ wrote, and the contract it was executed under:

| File | Lines | MD5 |
|---|---:|---|
| `bench/verify_bench.py` (after) | 388 | `06036d8c3d39ccec6be21d2158ef3ce1` |
| `bench/verify_bench.py` (branch head, before) | 287 | `520777380f2ec69a3d05d792d78c7f78` |
| `EXECUTOR-INSTRUCTIONS.md` (v20) | 814 | `9a257890e9db663eb0fc74129f4841e0` |
