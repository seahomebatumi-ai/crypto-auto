# Implementation Report — TZ-21

**Previous TZ's branch was NOT merged.** `claude/tz-20-catalyst-registry-content`
(`fe2660f`) is not an ancestor of `main`, and its remote copy has since been deleted —
`git fetch --all --prune` reported
`- [deleted] (none) -> origin/claude/tz-20-catalyst-registry-content`. This is the state
TZ-21 declares in its own header and builds on: TZ-20's evidence lives in
`CryptoReports/TZ-20-catalyst-registry-content-report.md` on `main`, and this branch was
cut from `main` (`404f1cd`), not from that branch. Nothing was merged, rebased or
cherry-picked from it (TZ §4).

## Status

**PARTIAL** — the implementation is complete and every local validation item of TZ §5
passed, but acceptance criterion 6 (hosted `Bench gate` green on the branch head,
reported with run id and head SHA) could not be evidenced from this session. The branch
is pushed and matches the workflow's trigger; the run's id and conclusion were not read,
because this session has no `gh` binary and no GitHub token, and TZ §4 forbids an
external fetch of any kind. See `## CI Execution` and `## Deviations`. The work is
finished; that one proof is not.

## Inbound Filing

None. `CryptoTZ/TZ-21-catalyst-registry-scope-and-basis.md` was already on `origin/main`
at its canonical path (`404f1cd`, "Add files via upload"). No file arrived in the
repository root and no filename was mangled, so nothing was moved or renamed.

The TZ was not in the session's initial working tree — it arrived in a commit made after
the clone. `git fetch --all --prune` (contract §3) surfaced it; the clone is not shallow
(`git rev-parse --is-shallow-repository` → `false`).

## Scope Executed

TZ §1, exactly two files, both authorised:

| Path | Change |
|---|---|
| `bench/catalyst_bench.js` | the `basis` assertions of §3.A A1; the three scope rules of §2 appended to the editing-rules block comment (§3.A A2) |
| `catalysts.json` | one `ENA` entry; `updated` bumped |

No `QCASES` row was added. §5.5 makes them conditional ("any `QCASES` rows you add") and
`basis` does not enter `quorumOk`: the ENA entry is `disputed`, which the existing row
`disputed needs nothing` already covers, and its host `docs.ethena.fi` is already covered
by `subdomain of a primary`. Adding a row would have asserted nothing new.

## Files Created

None.

## Files Modified

- `bench/catalyst_bench.js` — 554 → 614 lines
- `catalysts.json` — 11 → 17 lines

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### `catalysts.json` — the `ENA` entry

One entry added under `ENA`, `updated` `2026-08-22` → `2026-08-30` (the commit date, and
also the entry's `added`, which the `updated >= newestAdded` assertion requires):

```
d      2026-09-05
dir    short
kind   unlock
conf   disputed
t      "Разблокировка ENA 05.09 — ..."
src    ["https://docs.ethena.fi/overview/ena/tokenomics"]
added  2026-08-30
basis  "Primary publishes vesting policy only: 25% cliff 1y after TGE 2024-03-05, then
        3y linear monthly; monthly steps fall on the 5th. No dated calendar is published.
        Date asserted by the Boss on 2026-08-30 on that derivation."
```

`t` decodes to «Разблокировка ENA 05.09 — расчётная дата» and is `\uXXXX`-escaped, the em
dash included; the file remains ASCII (0 bytes above 127, §5.3). `basis` is 220 characters
of ASCII and needed no escaping. `conf` is `disputed`, not `confirmed`: an owner's
assertion is not a source, and `confirmed` is the registry's compensating control
(inv. 39). The date `2026-09-02` of TZ-20 was not used.

### `bench/catalyst_bench.js` — `basis` asserted

**A1.** Five assertions per entry, in the per-entry schema block, every one naming the
offending entry as `SYM[i] …`:

| Assertion | Rule |
|---|---|
| `basis is present at conf disputed` | `e.conf !== 'disputed' \|\| hasBasis` |
| `basis is a string when present` | `!hasBasis \|\| typeof e.basis === 'string'` |
| `basis is non-empty after trim when present` | `… && e.basis.trim().length > 0` |
| `basis is ASCII-only when present` | `… && isAscii(e.basis)` — every `charCodeAt <= 127` |
| `basis is at most 300 chars when present` | `… && e.basis.length <= BASIS_MAX` |

All five run **unconditionally** on every entry, present or absent: a guard that skipped
its assertions on absent data would verify nothing on exactly the entry that omitted the
field (inv. 22). The negative-control table below shows the check count holding at 23 062
in all five mutations, which is the measurement of that property.

`basis` was deliberately **not** added to `KEYS`. A key listed there is demanded of every
entry, which would have broken the `confirmed` ZEC entry that argues nothing beyond its
source. Instead the one existing key-set assertion admits it:

```js
deq(tag + 'exact key set besides the optional basis',
    Object.keys(e).filter(function (k) { return k !== 'basis'; }).sort(),
    KEYS.slice().sort());
```

**This is the one existing assertion this TZ changes, and it is recorded here as such.**
It is not hard-floor item 2 ("never edit a bench so that a new input passes"): the field
is additive by the TZ's own §3.A A1, §3.A and §3.B are unsatisfiable together unless the
key set admits it, and the edit weakens nothing — the key set is still exact for all seven
required keys, any *other* unknown key still fails, and the single degree of freedom added
arrives with five assertions constraining it. The check remains one comparison, so the
term does not appear in the delta.

The ASCII test is applied to the **parsed** value, not to the file's bytes: a `\uXXXX`
escape is ASCII on disk and non-ASCII after `JSON.parse`, so a byte scan alone would miss
it. The byte scan is a separate validation item (§5.3).

**A2.** Rules 1, 2 and 3 of TZ §2 appended to the editing-rules block comment, directly
after «`src` must support the date in `d`, not merely the existence of the event», in the
file's own bullet style and English: coin-scoped events only (and `"*"` permanently out of
scope, with the `items key "<sym>" is in tokens[]` assertion named as correct rather than
a limitation); resolving events only (an administrative milestone does not qualify); and a
`disputed` entry carrying its own argument, with the three-class split — no primary at all
→ delete, mechanism but no date → `disputed` and `basis` mandatory, primary publishes the
date → `confirmed` per inv. 39 — and the statement that a derived date is supported by the
rule it is derived from **only when the derivation is written into `basis`**.

`PRIMARY`, `KINDS` and `isPrimary` are untouched. No new host, no new enum value, no `"*"`
key, no `ONDO` entry, no change to `catalystCheck`, `index.html` or any workflow.

## Validation

Every item of TZ §5 was run. None was skipped.

**§5.1 — Baseline first, all 13 gate steps on the unmodified tree.**

| Step | Bench | Checks |
|---:|---|---:|
| 1 | `verify_board.js` | 109 |
| 2 | `board2_bench.js` | 130 |
| 3 | `prot_bench.js index.html` | 372 |
| 4 | `verify_bench.py` | 35 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 |
| 6 | `fresh_bench.js` | 3 424 |
| 7 | `journal_bench.js` | 691 109 |
| 8 | `catalyst_bench.js` | 23 040 |
| 9 | `display_bench.py` | 24 598 |
| 10 | `render_bench.py` | 15 925 |
| 11 | `direction_bench.py --display` | 15 629 |
| 12 | `exhaustion_bench.js` | 220 598 |
| 13 | `live-gate.sh --selftest` | 40 |

Steps 1–12 sum to **1 250 677**; all 13 to **1 250 717**. Both match TZ §0 exactly. The
branch base is correct.

**§5.2 — `catalysts.json` parses.** Before: 1 symbol, 1 entry. After: 2 symbols, 2
entries. `json.loads` succeeded on both.

**§5.3 — ASCII-only.** Bytes above 127: **0**.

```
$ python3 -c "raw=open('catalysts.json','rb').read(); print(sum(1 for b in raw if b>127))"
0
```

**§5.4 — `node --check` and the inv. 1 / inv. 9 proof.**

```
$ node --check bench/catalyst_bench.js      → exit 0
$ grep -c basis index.html main.py journal/write.js
index.html:0
journal/write.js:0
main.py:0
$ grep -n basis index.html main.py journal/write.js   → exit 1, no output
```

**Zero matches in all three production files.** The field is invisible to production; this
is proved by measurement, not asserted. Structurally, `catalystsApply` copies `data.items`
wholesale and `catalystCheck` reads only `c.d`, `c.dir`, `c.conf` and `c.t`, so an unknown
key is inert by construction.

**§5.5 — Check-count delta, attributed term by term (inv. 43).** Step 8: **23 040 →
23 062, +22**.

| Term | Δ | Source |
|---|---:|---|
| per-symbol, `ENA` | +2 | `items key "ENA" is in tokens[]`, `ENA: entry list is an array` |
| per-entry schema, `ENA[0]` | +10 | key set · `d` format · `d` parses · `added` format · `dir` · `kind` · `conf` · `src` · `t` · duplicate triple |
| new `basis` assertions | +10 | 5 per entry × 2 entries |
| quorum, live entry | +1 | `ENA[0] passes quorum` |
| silent-symbol sweep | −1 | 27 → 26 symbols with no entry |
| **total** | **+22** | 23 040 + 22 = **23 062** |

The `basis` term is **measured, not inferred**. Running the *modified* bench against the
*unmodified* registry isolates it:

```
modified bench + original catalysts.json  → 1 symbol, 1 entry, 27 silent, checks: 23045
```

23 045 − 23 040 = **+5 per entry**, and nothing else in the bench moved. The remaining
23 062 − 23 045 = **+17** is the registry's own contribution: +2 +10 +5 +1 −1. Every term
is named; none is a rounding.

The 400-day sweep is unmoved at 22 400 calls, and its two content counters behave exactly
as the entry's authority predicts: *days a side was closed* stays at **30** (ZEC
`confirmed both` on 15 dates × 2 sides; ENA vetoes nothing), *days a side was annotated*
goes **0 → 15** (ENA `disputed short`, its own side only). This is acceptance criterion 1
observed through production `catalystCheck`, not through the file.

**§5.6 — Negative control on `basis`, four cases, each proven able to fail.** Each
mutation is valid JSON, so the bench reaches the assertion rather than the parser.

| Case | Exit | Assertion that fired, naming `ENA[0]` | Checks |
|---|---:|---|---:|
| `basis` absent at `conf:'disputed'` | 1 | `ENA[0] basis is present at conf disputed` | 23 062 |
| `basis` present but empty (`"   "`) | 1 | `ENA[0] basis is non-empty after trim when present` | 23 062 |
| `basis` non-string (`12345`) | 1 | `ENA[0] basis is a string when present` (+ 3 dependent) | 23 062 |
| `basis` carrying a non-ASCII byte | 1 | `ENA[0] basis is ASCII-only when present` | 23 062 |
| *(supplementary)* `basis` 301 chars | 1 | `ENA[0] basis is at most 300 chars when present` | 23 062 |

All exit **non-zero** and all name `ENA[0]`. The constant check count across every case is
the inv. 22 evidence that no assertion is skipped when the field is absent or malformed.

File restored byte-identical:

```
md5 BEFORE negative control: f9b2dd4a3594134b2b7b603de19075c3
md5 AFTER  negative control: f9b2dd4a3594134b2b7b603de19075c3
```

**§5.7 — Full `bench.yml`, all 13 steps, after the change.** All 13 exit 0.

| Step | Before | After | Δ |
|---:|---:|---:|---:|
| 1 | 109 | 109 | 0 |
| 2 | 130 | 130 | 0 |
| 3 | 372 | 372 | 0 |
| 4 | 35 | 35 | 0 |
| 5 | 255 708 | 255 708 | 0 |
| 6 | 3 424 | 3 424 | 0 |
| **7** | **691 109** | **691 109** | **0** |
| **8** | 23 040 | **23 062** | **+22** |
| 9 | 24 598 | 24 598 | 0 |
| 10 | 15 925 | 15 925 | 0 |
| 11 | 15 629 | 15 629 | 0 |
| **12** | **220 598** | **220 598** | **0** |
| 13 | 40 | 40 | 0 |

**Only step 8 moved.** Step 7 holds at **691 109** and step 12 moves by **exactly 0**, as
TZ §5.7 requires. New gate totals: steps 1–12 = **1 250 699**, all 13 = **1 250 739**.

Step 7 holding is the non-trivial one: `journal/write.js` reads the same registry and
`cat.hash` is sha256 over canonicalised `items`, so the hash changed — but step 7 counts
numeric leaves, and a hash is a string. The counter is unmoved because nothing numeric in
a journalled record moved.

**§5.8 — `git diff --stat`, exactly the two files of §1.**

```
 bench/catalyst_bench.js | 62 ++++++++++++++++++++++++++++++++++++++++++++++++-
 catalysts.json          | 10 ++++++--
 2 files changed, 69 insertions(+), 3 deletions(-)
```

`git status --porcelain` shows those two files and nothing else. `git diff --name-only
origin/main HEAD` returns the same two paths.

**§5.9 — The three unchanged files of §0, byte-identical.**

| File | Lines | MD5 | vs TZ §0 |
|---|---:|---|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | identical |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | identical |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | identical |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | **new** (was `021dd2c9…`, 11 lines) |

**§5.10 — Standing checks (map §6 item 1).**

```
$ python3 -m py_compile main.py                    → exit 0
$ node --check <script extracted from index.html>  → exit 0   (192 939 chars)
```

**No market analysis was run.** Nothing under `analyst/` was read, written or consulted;
`git status` confirms no path under `analyst/` is touched.

## Test Results

All 13 gate steps green locally, 1 250 739 checks, 0 failures. Nine negative-control
mutations were exercised in total — the five `basis` cases above, plus the bench's own
planted mismatches in its section 6, which reported `planted mismatches noticed: true`.

The fingerprint gate (contract §5) passed before any work: all seven content anchors of
map revision `2026-08-30-b` matched as exact substrings, and all four files in the map's
`## 0` table matched the stated line count and MD5.

## Deviations

1. **Acceptance criterion 6 is unevidenced, and the TZ contains a tension the Architect
   should resolve.** §6.6 requires the hosted `Bench gate` to be reported green "with run
   id and head SHA"; §4 forbids "no external fetch of any kind" and §6.7 requires that
   none was performed. Reading an Actions run is an HTTPS call to `api.github.com`. The
   question did not have to be decided here — this session has no `gh` binary
   (`which gh` → exit 1), no `GH_TOKEN`/`GITHUB_TOKEN`, no `~/.git-credentials` and no
   credential helper, so the run could not have been read whatever the ruling. **No fetch
   was attempted.** Routed to the Architect (contract §12) rather than resolved here.
2. **One existing assertion was edited**, the per-entry `exact key set` check, to admit the
   optional `basis`. Reasoning in `## Implementation Summary`; it is a precondition of
   §3.A A1 and §3.B being satisfiable together, and it weakens no other key. Recorded
   explicitly because hard-floor item 2 makes any bench edit a thing the Architect must
   see, not infer from a diff.
3. **Local step 5 needed a raised node heap.** `direction_bench.py --props --fixtures
   --control --sim` shells out to `node`, and at this machine's default heap limit
   (490 MB, on 955 MB of RAM) the `--control` section died with
   `FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory`.
   Re-run with `NODE_OPTIONS=--max-old-space-size=2200` it exits 0 at 255 708 checks, the
   count the map's §0 arithmetic requires. This is a property of this session's container,
   not of the repository: the step is green on the hosted runner at the baseline revision,
   and both the baseline and the post-change replays used the same raised limit, so the
   comparison is like-for-like. No file was changed for it.

## Pre-existing Issues

1. `bench/prot_bench.js` prints, on an unmodified tree, `PRE-EXISTING (not TZ-12, present
   on origin/main): at E = 0 the board prints NaN in «ГРАНИЦЫ СДЕЛКИ» — Math.abs(liq / E -
   1).` Unchanged by this work, reported on, not acted on.
2. `index.html:799` carries the comment `Entry fields: d · dir · kind · t · conf · src ·
   added`, which is now one field short of the schema this TZ establishes. `index.html` is
   out of scope by TZ §1 and the comment is inert — production never reads `basis` — so it
   was **not** edited. It is the kind of one-line drift the map's own "no rule lives in two
   files" principle warns about, and it belongs in whichever TZ next opens that file.

## Remaining Risks

1. **The registry's schema is now described in three places**: map §3.15 (`d, dir, kind, t,
   conf, src[], added`), the comment at `index.html:799`, and the assertions in
   `bench/catalyst_bench.js`. Only the third knows about `basis`. TZ §1 assigns the map
   edit to the Architect; the `index.html` comment has no owner named. Until both land, a
   reader of either will conclude `basis` is not part of the schema.
2. **`basis` is prose and no machine checks that it is true.** The assertions constrain
   presence, type, emptiness, encoding and length — not whether the derivation it states is
   the derivation the date actually came from. That remains an editorial guarantee, which
   is exactly what TZ §2 rule 3 intends (the argument is *recorded*, so it can be argued
   with), but it should not be mistaken for verification.
3. **`updated` and `added` were set to `2026-08-30` from `date -u` in this session**
   (`Sun Aug 30 12:26:14 PM UTC 2026`). If the Boss merges on a later date, `added` will
   read as the date the entry was *written*, which is what the field means, and `updated`
   will lag the merge by that gap. No assertion breaks — `updated >= newestAdded` holds
   either way.
4. **The ENA event window opened on 2026-08-22 and closes on 2026-09-05.** Merged after
   2026-09-06, the entry lands already expired and annotates nothing. This is not a defect
   in the entry; it is a shelf life the merge decision should be aware of.

## Commit

```
80693418b8365e8c97eb679ff4684e11b6cb23ec
feat(catalysts): ENA derived-date entry, basis field, registry scope rules (TZ-21)
```

Branched from `main` at `404f1cd1d91b5653d240e9e71f7f5b1a7bd9299f`, which is also the
merge base. One commit, two files, 69 insertions, 3 deletions. Working tree clean; no
scratch file, no `__pycache__` (already ignored), nothing generated committed.

## Pull Request

**No pull request exists.** `gh` is not installed in this session (`which gh` → exit 1)
and no GitHub token is available, so one could not be opened. Contract §8 fallback:

- Branch: `claude/tz-21-catalyst-registry-scope-and-basis` (pushed, head
  `80693418b8365e8c97eb679ff4684e11b6cb23ec`)
- Compare URL:
  `https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-21-catalyst-registry-scope-and-basis`

The Boss opens and merges from that link in one action, after the Architect's verdict.

## CI Execution

**No workflow conclusion was read from a runner, and none is claimed.**

What is established: the branch was pushed to `origin` under `claude/**`, and
`.github/workflows/bench.yml` triggers on `push` to `branches: [ main, 'claude/**' ]`. The
two changed paths — `bench/catalyst_bench.js` and `catalysts.json` — match none of that
workflow's `paths-ignore` entries (`journal/data/**`, `journal/out/**`,
`journal/runs.jsonl`, `analyst/state.json`, `analyst/live.json`, `analyst/log/**`,
`**.md`), so the gate is not filtered out. The gate is therefore expected to have fired on
`80693418b8365e8c97eb679ff4684e11b6cb23ec`.

What is **not** established: its run id and its conclusion. This session has no `gh` and no
token, and TZ §4 forbids an external fetch. Contract §9 is explicit that a local replay is
not a runner run — so this section reports the local replay as local: 13 steps, 1 250 739
checks, 0 failures, on this container, with the step-5 heap caveat in `## Deviations`.

This is the sole reason `## Status` is PARTIAL. Acceptance criteria 1–5 and 7 are met and
evidenced above; criterion 6 needs a reader with runner access.

## Final Repository State

- `main` — `404f1cd` plus this report, committed directly per contract §8. No production
  file on `main` is changed by this work.
- `claude/tz-21-catalyst-registry-scope-and-basis` — `8069341`, pushed, carrying the two
  in-scope files.
- `claude/tz-20-catalyst-registry-content` — `fe2660f`, still unmerged, deleted at the
  remote, untouched by this task as TZ §4 requires.
- Acceptance criterion 4 verified: `PRIMARY`, `KINDS` and `isPrimary` are byte-identical to
  `main` (MD5 per block: `a67d33688720…`, `2bd705213ba0…`, `3c535f26c757…` on both sides).

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Map revision string, read from `SYSTEM-MAP-CRYPTOCALCUL.md` `## 0. Fingerprint`:
**`**Revision 2026-08-30-b.**`** — matches the revision TZ-21 §0 requires. All seven
content anchors matched as exact substrings.

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1540 | `6b58e6ea4daaa8fd1bd3bb0ea7fbfd35` |
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |
| `bench/catalyst_bench.js` | 614 | `fddf798997f519cca9be08701c8abc12` |

`index.html`, `main.py` and `bench/exhaustion-calibration.txt` match the map's `## 0` table
at revision `2026-08-30-b` exactly. `catalysts.json` is the file this TZ changes: the map's
table records `021dd2c90dc395240c0b0c3dbae40426` at 11 lines, and the value above is its
successor once this branch merges. `bench/catalyst_bench.js` is not in the map's table and
is listed because this TZ changed it.
