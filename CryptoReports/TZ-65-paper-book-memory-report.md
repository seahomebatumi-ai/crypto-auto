# Implementation Report — TZ-65

## Status

**COMPLETED.**

**TZ-64's branch is unmerged, and it is this TZ's base** (contract §8). `claude/tz-64-paper-test` is not an
ancestor of `main`; pull request #52 is `OPEN` and was not accepted by the audit of 17.10.2026. This work is
therefore complete and **live nowhere**: it reaches production only when this TZ's pull request — which carries
TZ-64's three commits and TZ-65's one — is merged.

1. **The base.** `git rev-parse origin/claude/tz-64-paper-test 'origin/claude/tz-64-paper-test^{tree}'` →
   `843ba3ff9faaac66cf458d21d01f94eea88bc171` and `91ba4c3647e9d66045d904e511ea8022083fa4ab`, both the known
   answer (A1.1). `git merge-base --is-ancestor origin/claude/tz-64-paper-test origin/main; echo $?` → **`1`**,
   the known answer (A1.2): TZ-64 is not merged, so this TZ's base is the branch and not `main`.
2. **The code.** B1's patch extracted from `origin/main:CryptoTZ/TZ-65-paper-book-memory.md` by the one command
   the TZ gives: MD5 `0626e9f4614abb45a0bf366361def75d`, **312 lines** — the known answer, so nothing was
   blocked and nothing was retyped. After `git apply`: `vps/paper.py` **1281** lines, MD5
   `057440a4b5c9c277cc99062f768464ac`; `vps/selftest.py` **1807** lines, MD5
   `04d484d41ac49a466ec60c0df3c17dda` — both B2's known answers exactly.
3. **The checks.** `python3 vps/selftest.py` → exit 0, `selftest: sections 23 checks 432 failed 0 empty 0`, and
   `section W: checks 102 failed 0` — V1's known answer. The five negative controls, each applied alone and then
   reverted, failed **exactly** the checks the TZ predicted and nothing else: control 1 → `failed 2`, the two
   named checks of W; controls 2, 3, 4 and 5 → `failed 1` each, the one named check of W. No control produced a
   failure outside section W.
4. **The gate.** Bench gate run **`39004909735`** on headSha **`a9ff67dd0daa92882edf3c44c9589c281c3b7f6d`** —
   the implementation commit — event `push`, status `completed`, conclusion **`success`**, 23 of 23 job steps
   non-failing. C1's listing returned exactly one run, for that SHA.

---

## Inbound Filing

Nothing was moved and nothing was renamed. The TZ arrived at its own canonical path,
`CryptoTZ/TZ-65-paper-book-memory.md`, on `origin/main` in commit `9ec8374` ("Add files via upload"), 606 lines.
No copy landed in the repository root and no filename was mangled in transit, so §3's `git mv` clause had no
referent. No credential arrived under the trigger line, and the TZ names none (§1 of the TZ).

`main` advanced from `7026357` — the commit the TZ was written against — to `9ec8374` while this TZ was being
written, and `git diff --stat 7026357 origin/main` shows that advance to be **the upload of TZ-65 itself and
nothing else** (1 file, 606 insertions). `main`'s `vps` tree is unchanged at
`96d72e8df795c79ad7d77c9ee73d4bbc284534e7`, the tree the TZ header states. The gate was therefore run against a
`main` whose only difference from the TZ's baseline is the TZ.

## Scope Executed

**Branch TZ** (contract §8): the TZ's `## Scope` authorises two written files outside `CryptoReports/**`, so the
class is read off the scope, not chosen — a branch and a pull request exist, and the report goes to `main` on the
`CryptoReports/**` direct-push path.

Executed in full: Stage A (A1, including contract §4a steps 1–6 and the §5 gate against the TZ's `§0`, its
added-files table included), Stage B (B1–B4), Stage C (C1) and validation V1–V4. No stage ran on the VPS, no
unit of any kind was started or left behind, and the session's only network reads were `git`'s and `gh`'s
(TZ §6 rule 1). Python 3's standard library only (rule 3); the patch adds `import array` to `vps/paper.py` and
`import array`, `import tracemalloc` to `vps/selftest.py`, all three stdlib.

## Files Created

None.

## Files Modified

On the branch `claude/tz-65-paper-book-memory`, and nowhere else:

```
vps/paper.py
vps/selftest.py
```

`git diff --summary origin/claude/tz-64-paper-test` printed **no mode line** (B3): both files stay `100644`,
confirmed by `git ls-files -s`.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

The change is the Architect's patch in TZ §13, applied byte for byte and **never retyped** (TZ §6 rule 2). The
defect it repairs is the Architect's own, in TZ-64's §13: nothing in TZ-64 bounded what a booking pass holds, so
no check of TZ-64 could see it. `Inputs` kept every 1-minute file a pass read for a whole UTC day as a tuple of
five Python objects a minute — 375 KiB a symbol-day — and because an episode's book reads every day from its
opening to its exit, the window's last day booked every still-open episode from the day it opened.

The patch bounds the pass by five mechanisms, which are rule 12.3.6:

1. **Compact minutes.** A new `Rows` class holds one day's `(open, high, low, close)` as four doubles a minute in
   a single `array.array("d")`, with the open times in an `array.array("q")` beside it — 63 KiB a symbol-day
   against 375 KiB. `Rows.__getitem__` reconstructs a minute's tuple on demand and raises `IndexError` outside
   the day, so every existing reader of a kline row is unchanged.
2. **One symbol at a time.** `Inputs` gains `kl_sym`; `minutes()` drops the whole cache when asked for a symbol
   other than the one held.
3. **One read a file.** `produce_books` books a day's episodes symbol by symbol — the symbol of the latest day
   first — so each minute file is read once a pass, while `lines[i]` is filled by index so the book's lines keep
   the episode file's order.
4. **The latest day first.** The latest day any episode reads is requested before anything else, so a day not
   yet published ends the pass after **one** read instead of after every read before it. An `Absent` latest day
   is deliberately swallowed there, because that episode's own book line records it unbookable.
5. **Dropped at the end.** `inputs.drop_minutes()` runs in a `finally`, so the minutes go whether the day's pass
   was written or not.

`last_day(ep, window_end)` is extracted as the single statement of the last day an episode's book reads, and both
`book_episode` and `produce_books` call it — one statement of one rule (map inv. 38), where TZ-64 computed it
inline in `book_episode` only.

`vps/selftest.py` gains section W15 (`section_w_memory`) and the `w_counted_rows` fixture, which counts every
read by path, serves a day's rows shuffled with one stray row of each neighbouring day, and can refuse to publish
a dated file. Its 13 checks cover `Rows`' round trip and bounds, one day's 1 440 minutes ascending with the
neighbours' strays excluded, the 128 KiB ceiling measured with `tracemalloc`, `kl` across three days, the drop on
a symbol change, the one-symbol/one-read/nothing-kept properties of a real `produce_books` pass over six
episodes on three symbols, the book's order, the unpublished-latest-day early end, and the absent-latest-day case
that writes the day with its episodes unbookable.

**No number moves.** Nothing in the patch touches `book_delay`, `sigma_for`, `funding_line` or any figure a book
carries, and the TZ records the book and funding files as byte-identical to `843ba3f`'s on a 40-episode fixture
(§3). This session did not re-derive those two MD5s; see `## Remaining Risks`.

Procedural note on B1: the TZ makes a wrong patch digest `BLOCKED` with **nothing applied**, so the digest was
measured and read in one invocation and `git apply --check`/`git apply` run in the next, rather than chaining
them — the same commands in the same order, with the stop the TZ requires actually taken before anything was
written. `/tmp/tz65` was removed once the patch was applied (B4) and `ls` confirms it gone.

## Validation

| Item | Command | Result |
|---|---|---|
| §5 gate | see `## Fingerprints` | PASS — revision, 7 of 7 anchors, 4 of 4 map-table files, 4 of 4 added files |
| A1.1 | `git rev-parse origin/claude/tz-64-paper-test 'origin/claude/tz-64-paper-test^{tree}'` | `843ba3ff…bc171`, `91ba4c36…83fa4ab` — known answer |
| A1.2 | `git merge-base --is-ancestor origin/claude/tz-64-paper-test origin/main; echo $?` | `1` — known answer; TZ-64 unmerged |
| A1.3 | `python3 vps/selftest.py` on `843ba3f`'s tree | exit 0, `selftest: sections 23 checks 419 failed 0 empty 0` — known answer |
| B1 | `md5sum /tmp/tz65/tz65.patch; wc -l` | `0626e9f4614abb45a0bf366361def75d`, 312 — known answer; `git apply --check` and `git apply` both exit 0 |
| B2 | `md5sum`, `wc -l` | `vps/paper.py` 1281 / `057440a4b5c9c277cc99062f768464ac`; `vps/selftest.py` 1807 / `04d484d41ac49a466ec60c0df3c17dda` — known answers |
| B3 | `git diff --summary origin/claude/tz-64-paper-test` | no mode line; both `100644` |
| B4 | `rm -r /tmp/tz65` | gone (`ls`: No such file or directory) |
| V1 | `python3 vps/selftest.py` | exit 0, `selftest: sections 23 checks 432 failed 0 empty 0`, `section W: checks 102 failed 0` — known answer |
| V1 controls | five, each alone then reverted | each failed exactly the predicted checks; digests restored and V1 green again |
| V2 | `python3 -m py_compile vps/paper.py vps/selftest.py` | exit 0 |
| V3 | `git diff --name-only origin/claude/tz-64-paper-test...HEAD` | exactly `vps/paper.py`, `vps/selftest.py` (2) |
| V3 | `git diff --name-only origin/main...HEAD` | exactly TZ-64's nine files (9) |
| V4 | branch pushed, pull request opened | branch `claude/tz-65-paper-book-memory`; PR **#53**, naming #52 superseded |
| C1 | `gh run list -R … -w bench.yml -b claude/tz-65-paper-book-memory -e push --json headSha,status,conclusion` | one run, `a9ff67dd…c281c3b7f6d`, `completed`, **`success`** |

§9's standing checks (`py_compile main.py`, `node --check` on `index.html`'s script block) have no referent:
this TZ modifies no production file — `main.py` and `index.html` are untouched and carry their map fingerprints
unchanged (`## Fingerprints`).

§9's negative-test requirement for a CI-touching TZ has no referent either: no workflow file is in scope. The
TZ's own negative controls (V1's five) are the gate proven to fail, and they did.

## Test Results

**Baseline (A1.3), on `843ba3f`'s tree** — `sections 23 checks 419 failed 0 empty 0`, exit 0. Section W: 89.

**After the patch (V1)** — `sections 23 checks 432 failed 0 empty 0`, exit 0. Section W: **102**.

Per section, baseline → after: A 32→32, B 12→12, C 4→4, D 13→13, E 12→12, F 14→14, G 8→8, H 2→2, I 4→4,
J 26→26, K 2→2, L 4→4, M 19→19, N 10→10, O 27→27, P 21→21, Q 3→3, R 9→9, S 35→35, T 39→39, U 18→18, V 16→16,
**W 89→102**. Every section but W is unchanged, so the +13 is W15 alone and nothing regressed; W's 89 earlier
checks stay green. 419 + 13 = 432, the TZ's derivation.

**Negative controls (inv. 68).** Each was applied alone by exact string replacement — the harness asserted the
target line occurred **exactly once** before writing, so no control was silently a no-op — then reverted with
`git checkout --` and the file's MD5 confirmed back at `057440a4b5c9c277cc99062f768464ac`. Failing check labels
were read from the selftest's own `FAIL section <X>: <label>` lines on stderr.

| # | Line changed in `vps/paper.py` | Total line | W | Failing checks of W, as named |
|---|---|---|---:|---|
| 1 | `self.klines, self.kl_sym = {}, sym` → `self.kl_sym = sym` | `sections 23 checks 432 failed 2 empty 0` | 2 | `asking for another symbol drops the first one's days` · `a pass holds one symbol's days at most: six, of eighteen read` |
| 2 | `inputs.drop_minutes()` → `pass` | `… failed 1 empty 0` | 1 | `after the pass no minute is kept` |
| 3 | `inputs.minutes(latest[1], latest[0])   # not yet published…` → `pass` | `… failed 1 empty 0` | 1 | `a latest day not yet published ends the pass after one read, nothing written or kept` |
| 4 | `for i in sorted(range(len(eps)), key=lambda i: (…)):` → `for i in range(len(eps)):` | `… failed 1 empty 0` | 1 | `each minute file is read once in a pass` |
| 5 | `array.array("d", [v for x in rows for v in x[1:]]))` → `[v for x in rows for v in x[1:]])` | `… failed 1 empty 0` | 1 | `minutes: one symbol-day is kept in under 128 KiB` |

In every control the failures were **confined to section W** (0 outside it) and every other check of all
twenty-three sections stayed green — the partitions the TZ states, exactly. After the last revert, V1 returned
`sections 23 checks 432 failed 0 empty 0` with both B2 digests intact and `git status --porcelain` empty.

## Deviations

1. **Model.** The TZ header names **Sonnet**; this session executed on **Opus 5**. Nothing in the TZ's stages
   depends on the model, no stage is a model-dependent measurement, and the contract routes the choice to the
   Architect (§1) — it is recorded here because the header states it and the audit compares it.
2. Nothing else. No scope was widened, no file outside `## Scope` was touched, no rule was substituted, and the
   patch was applied as bytes rather than reimplemented.

**Not a deviation, stated so it is not mistaken for one.** The commit message carries the TZ's
`## Commit Message` string verbatim as its subject — extracted programmatically from
`origin/main:CryptoTZ/TZ-65-paper-book-memory.md` rather than retyped — followed by the
`Co-Authored-By:` trailer this repository has carried on 145 commits, TZ-64's three included. The §8 "verbatim"
requirement is met by the message string; the trailer is the repository's established form, not an addition to
the specified string.

## Pre-existing Issues

1. **TZ-64's branch is unmerged and pull request #52 is open.** Stated at the top of this report under §8. Not
   this session's to resolve: this TZ's pull request supersedes #52, and the session neither closed nor
   commented on it (TZ §5).
2. **Two map items are stale at this merge, both named by TZ §5 as TZ-64 §5's and both left untouched.**
   Measured, not acted on:
   - The map's sentence at line 2708, «`bench.yml` ignores FOUR paths in this tree and only three of them are
     the analyst's», is behind the file. On this branch `bench.yml`'s `paths-ignore` carries **9** entries, **5**
     of them under `analyst/` (`state.json`, `live.json`, `log/**`, `owner.json`, `paper/**`); on `main` it is
     **8** and **4**. TZ-64 added `analyst/paper/**`.
   - §11's path table is the second item. The TZ states that the Architect's revision after this TZ's audit
     repairs both, together with the §10 row, so neither is a finding this session may act on (contract §6).
3. No other difference was found between the repository and the map's `§0` block: all four map-table files and
   all four files the TZ's gate adds matched their required line counts and MD5s exactly (`## Fingerprints`).

## Remaining Risks

1. **The memory figures in TZ §3 were not re-measured in this session, and this report does not assert them.**
   What is verified here is the behaviour the selftest checks: one symbol-day kept under 128 KiB (`tracemalloc`),
   one symbol's days at most held in a pass (6 of 18 files read), each minute file read once, nothing kept after
   the pass, and the one-read early end. The Architect's peak figures — ~26 MiB + 0.43 MiB a symbol-day before,
   35–39 MiB after, the 3 423 symbol-day worst day over 1 501 closed and 223 cut episodes — are the Architect's
   measurements on the workspace's selection, and reproducing them needs the selected accounts' fills, which no
   stage of this TZ reads. They remain the stated basis of rule 12.3.6, not a measurement of this session.
2. **The two book MD5s of TZ §3 (`ff6369e889c7c5086ba1ff5d03e068cd`, `ab341efed9431555f9441c4af96130e3`) were
   likewise not re-derived here.** The TZ names no stage that rebuilds the 40-episode fixture, and inventing one
   would be scope this TZ does not authorise. "No number moves" rests in this report on the unchanged source of
   `book_delay`, `sigma_for` and `funding_line`, on sections A–V holding their counts, and on W's 89 earlier
   checks staying green — not on a byte comparison of the two files.
3. **Merging is deployment** (hard floor 15, map §10). The `vps` tree runs on the VPS only from `main`, and the
   deployer runs `vps/selftest.py` before it installs — that is its gate, and V1 is the same selftest run here
   first. Until the merge, nothing in this branch runs anywhere.
4. **The poll loop is unchanged and still bounds nothing else.** A booking pass now reads each minute file once
   on its heaviest day, but a pick's event older than 600 s when the loop returns still raises no alert
   (TZ-64 12.5.2). The TZ places this outside its scope; nothing booked depends on an alert.
5. **A restart still repeats a pass.** State is saved at the end of a loop, so a unit killed mid-pass repeats the
   polls made before it. TZ-65 removes the memory cause of such a kill; it does not change the restart
   behaviour, which TZ-64's §12 continues to own.

## Commit

One implementation commit on the branch, pushed before this report was written:

`a9ff67dd0daa92882edf3c44c9589c281c3b7f6d`

Message — the TZ's `## Commit Message` string verbatim, then the repository's attribution trailer:

```
TZ-65: vps — the paper test's booking in bounded memory: one symbol's minutes at a time, four doubles a minute, dropped when the pass ends

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: `vps/paper.py` and `vps/selftest.py`, 2 files changed, 194 insertions, 18 deletions. The working tree
was clean at the commit and no generated artifact was committed — `vps/__pycache__`, left by `py_compile`, was
removed and is ignored by `.gitignore` in any case.

This report's own commit is authorised to carry the message
`TZ-65: report — the paper test's booking in bounded memory` and carries no hash, no conclusion and no push
result (§10, inv. 54).

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/53** — `claude/tz-65-paper-book-memory` → `main`, state
`OPEN`, carrying **4** commits: TZ-64's `2ed13b2`, `d6e0c59`, `843ba3f` and TZ-65's `a9ff67d`. Its description
names **#52 as superseded**; #52 was neither closed nor commented on by this session. Merging #53 is what puts
TZ-64 and TZ-65 in effect together.

## CI Execution

**On a GitHub runner.** Workflow `bench.yml` ("Bench gate"), run **`39004909735`**, event `push`, branch
`claude/tz-65-paper-book-memory`, headSha `a9ff67dd0daa92882edf3c44c9589c281c3b7f6d` — the implementation
commit. Status `completed`, conclusion **`success`**; job `bench` `success`, 23 steps, 0 non-successful. C1's
listing returned exactly that one run and no other.

The run fired because the commit changes `vps/**`, which no entry of the workflow's `paths-ignore` covers — the
9 entries on this branch are the three `journal/` paths, five under `analyst/` and `'**.md'`. No step of the
gate reads `vps/`, so the outcome is TZ-64's run on the rest of the same tree, as the TZ derives.

**Local, not on a runner:** V1 (and its five controls), A1.3 and V2 were run in this session on Python 3.12.3.
They are local executions and are reported as such; the 1.3 M-check bench gate is the runner's.

No other workflow ran. `main.yml` cannot have fired: its `push` trigger is a `paths` **allow-list** of exactly
two literal paths — `main.py` and `.github/workflows/main.yml` — read from `origin/main` before any push of this
session, as §8 requires rather than assumes; neither path is in this branch's diff, and `CryptoReports/**` is
not in that list either, so this report's own push to `main` cannot start the bot.

## Final Repository State

**The branch `claude/tz-65-paper-book-memory`**, at `a9ff67dd0daa92882edf3c44c9589c281c3b7f6d`, pushed to
`origin` and measured before this report was written. Its tree differs from `origin/claude/tz-64-paper-test` in
exactly `vps/paper.py` and `vps/selftest.py`, and from `origin/main` in exactly TZ-64's nine files. Working tree
clean; no scratch file, no stray local branch, no `__pycache__`, nothing left on `/tmp`. No unit, timer or
service was created, started or left running anywhere, and no stage touched the VPS.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

**`SYSTEM-MAP-CRYPTOCALCUL.md`** — revision string `**Revision 2026-10-16-c.**`, the one the TZ header requires:
match in both directions. **2779** lines, MD5 `4c3c60f0c16ac6d7bd8016c0cb370938` — reported, not enforced (§5);
both equal the values the TZ header states.

**Anchors.** The list was cut by the **structure** of the map's own anchor table — every row between its
separator line and its end — and never by matching anchor names (§5 step 2). The table's own row count is **7**
and the number compared is **7**; the TZ header quotes **7** rows and every one is character-for-character
identical to the map's, name and string, with no extra row in the header. Each anchor was then matched as an
exact, case-sensitive fixed substring of the repository copy with
`grep -c -F -e "<anchor>" SYSTEM-MAP-CRYPTOCALCUL.md`, and the matched text itself read back with
`grep -o -F -m1 -e "<anchor>" SYSTEM-MAP-CRYPTOCALCUL.md`:

| # | Anchor | Count | Text the match returned |
|---:|---|---:|---|
| 1 | revision | 2 | `**Revision 2026-10-16-c.**` |
| 2 | direction engine | 2 | `### 3.12 Direction engine — veto cascade` |
| 3 | catalyst registry | 2 | `### 3.15 Catalyst registry` |
| 4 | exhaustion measure | 2 | `### 3.16 List exhaustion — the day-range measure` |
| 5 | analytical engine | 2 | `## 11. Analytical engine` |
| 6 | squeeze block | 2 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| 7 | newest invariant | 2 | `72. **A write that fails leaves this run's product or nothing` |

Every anchor returned **2** occurrences — its row in the map's `§0` table and the heading or invariant it names —
so none is a table entry with no referent in the body.

**Files the map's `§0` table lists**, measured on `origin/main` (`9ec8374`). All four equal the required pair:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**Files the TZ's gate table adds.** All four equal the required pair, so neither `vps` file was BLOCKED and
§13's patch applied to exactly the bytes it was written against:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | equal; version line `**Version 30.**` present as an exact substring |
| `ANALYST-INSTRUCTIONS.md` | 4381 | `d665a12f789c9c0a2bb3d090265c22bf` | equal; this TZ reads none of it and changed nothing it reads |
| `vps/paper.py` at `origin/claude/tz-64-paper-test` | 1229 | `cf160b4dd8cfe5d81a1b5d6e682c230a` | equal |
| `vps/selftest.py` at `origin/claude/tz-64-paper-test` | 1683 | `7a876961c3497505da7e08401964bb6b` | equal |

**This TZ's own two files, after the patch** — B2's known answers, and the state the pushed branch carries:

| File | Lines | MD5 |
|---|---:|---|
| `vps/paper.py` | 1281 | `057440a4b5c9c277cc99062f768464ac` |
| `vps/selftest.py` | 1807 | `04d484d41ac49a466ec60c0df3c17dda` |

**The patch** extracted by B1's command: MD5 `0626e9f4614abb45a0bf366361def75d`, 312 lines.

**`CryptoTZ/TZ-65-paper-book-memory.md`** as read from `origin/main`: 606 lines, blob
`438f53188a0b3ff9084833bc359632f74889197b`.
