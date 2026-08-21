# Implementation Report — TZ-07

## Status

**PARTIAL.**

All four scopes are implemented, all three CI runs executed on GitHub runners,
and the gate has been proven able to fail on the branch. The status is PARTIAL
for exactly one reason, stated here so it cannot be missed:

**Validation item §7.4 bullet 2 — executing `journal/write.js --dry-run` against
live data — could not be run.** This session's network policy refuses
`gist.githubusercontent.com` and `data-api.binance.vision` at the proxy
(`CONNECT tunnel failed, response 403`). Per contract §9 an item that cannot be
run **fails**; it is never "not applicable". Its substance was demonstrated by
replaying the real recorded day `journal/data/2026-08-21.jsonl` through the
production `snapshot()` path, which is evidence of the same fact but is not the
live path, and the difference is not glossed here.

Nothing else was skipped, and no scope was blocked.

---

## Inbound Filing

Nothing to file. `CryptoTZ/TZ-07-controls-restored.md` arrived under its
canonical name (TZ header, contract §3) and no second or mangled copy exists
anywhere in the tree:

```
$ find . -path ./.git -prune -o -iname '*TZ*07*' -print
./CryptoTZ/TZ-07-controls-restored.md
```

The session clone was **shallow** (`git rev-parse --is-shallow-repository` →
`true`, 78-commit truncation class described in contract §3). It was deepened
with `git fetch --unshallow` before anything was assessed; the complete history
is 277 commits. `git fetch --all --prune` was run first, per §4.2.

The previous TZ's branch **was merged**: `c7993a7 Merge pull request #6` carries
TZ-06 into `main`. This work is not stacked on an unmerged base.

### System Map fingerprint gate (§0) — PASSED

| Anchor | Required | Found |
|---|---|---|
| `<!-- EDIT-MARKER 2026-08-22-VENUE-CONTRACT -->` | 1 occurrence | 1 |
| `<!-- EDIT-MARKER 2026-08-22-CATALYST-REGISTRY -->` | 1 occurrence | 1 |
| `### 3.14 Asset venue contract` | present | line 1031 |
| `### 3.15 Catalyst registry as data` | present | line 1088 |
| `## 9. Журнал миграций`, newest entry | `- 2026-08-22:` | `- 2026-08-22:` |
| `## 4. Инварианты`, highest number | 40 | 40 |

### Baseline (§0, §7.1) — recorded before any edit

| File | Lines | MD5 | Required by §0 |
|---|---:|---|---|
| `index.html` | 3522 | `a7b10d80bea67824cf9643842d2e505a` | matches |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | matches |
| `catalysts.json` | 15 | `eb591d2ef2d792ca6a4a25f26442e9b9` | matches |

| File in scope | Lines before | MD5 before |
|---|---:|---|
| `journal/write.js` | 760 | `9797097c442b5030fab8349fb3a44766` |
| `bench/journal_bench.js` | 874 | `86cd1b5afe7e99bd316ecd8f3fd43242` |
| `bench/verify_board.js` | 161 | `c9197b9af293df022f38ae779a1635f9` |
| `bench/board2_bench.js` | 166 | `a1682edf6e574767ffe59ebb78b89549` |
| `bench/prot_bench.js` | 429 | `9a8f85cfaf56e5102831ccf21dadb487` |
| `bench/display_bench.py` | 286 | `fcba16e72dd73c2d7ccacff2189d6f3c` |
| `bench/render_bench.py` | 431 | `bc1547927c1510540fc592084de0fc35` |
| `bench/direction_bench.py` | 765 | `4c6361868e4faa5ed7cc1aff72551458` |
| `.github/workflows/bench.yml` | 89 | `0f51159a65f016da8ef1e6bceb9937b3` |

---

## Scope Executed

| Scope | Subject | Outcome |
|---|---|---|
| A | Coverage semantics keyed on the venue declaration | COMPLETED |
| B | Registry parity in the three board benches | COMPLETED |
| C | Display contract back under an executing control | COMPLETED |
| D | The gate runs on a branch without a pull request | COMPLETED |

---

## Files Created

None.

## Files Modified

| File | Lines after | MD5 after | Scope |
|---|---:|---|---|
| `journal/write.js` | 796 | `25f732ebdfd9efaf13077cf6e4afe2a9` | A |
| `bench/journal_bench.js` | 958 | `50e5a3999e9180cfa4ae219b15525222` | A |
| `bench/verify_board.js` | 190 | `9a371afb1bb3904b4e8fa3b316b64395` | B |
| `bench/board2_bench.js` | 195 | `b18a28ddd40ea8a9524f4f18f53720b5` | B |
| `bench/prot_bench.js` | 458 | `59e1f2af47dd3a75e2f1d954fd58c820` | B |
| `bench/display_bench.py` | 305 | `a6fd12a76c6f1721b0ed0b11839618db` | C |
| `bench/render_bench.py` | 443 | `22a2c790487215ebfa713d072d580668` | C |
| `bench/direction_bench.py` | 784 | `34786b11afccfa5e84ef4158f8435e4c` | C |
| `.github/workflows/bench.yml` | 110 | `cca7f25ad52282c58477f00af0e2178f` | C, D |

```
$ git diff --stat origin/main HEAD
 .github/workflows/bench.yml | 31 +++++++++++++---
 bench/board2_bench.js       | 31 +++++++++++++++-
 bench/direction_bench.py    | 41 +++++++++++++++------
 bench/display_bench.py      | 25 +++++++++++--
 bench/journal_bench.js      | 86 ++++++++++++++++++++++++++++++++++++++++++++-
 bench/prot_bench.js         | 29 +++++++++++++++
 bench/render_bench.py       | 18 ++++++++--
 bench/verify_board.js       | 31 +++++++++++++++-
 journal/write.js            | 44 ++++++++++++++++++++---
 9 files changed, 307 insertions(+), 29 deletions(-)
```

## Files Renamed

None.

## Files Deleted

None. `image.PNG` was left untouched (contract §6 — it is the PWA icon).

---

## Implementation Summary

### Scope A — the venue declaration is read before the degradation ladder

`journal/write.js`, `buildDay()`. A `fut:true` test now short-circuits **ahead of
all five** existing checks (absent row → dead market → no bot row → error flag →
no metrics), so a `fut:true` asset can no longer reach a branch that increments
`hardSkip`. The reason string still records what was **observed**, in three
forms, exactly as §3.2 specifies:

| Observation | Reason string | `hardSkip` |
|---|---|---|
| no row at all | `futures-only: no spot mirror pair` | not incremented |
| row present, dead | `futures-only: delisted spot mirror row` | not incremented |
| row present, alive | `futures-only: spot mirror row unexpectedly alive` | not incremented |

The third case does not pass silently: `buildDay()` collects the symbol in a new
`alive[]` field of its return value, and `snapshot()` pushes
`fut:true asset trading on spot: <SYM>` into the existing `notes` array — one
note per symbol — so the anomaly reaches `runs.jsonl` through the mechanism that
already carried the price-fallback and stale-coeffs notes. A relisting decision
is not taken here; it is reported (contract §7.11).

The non-`fut` path is unchanged in ordering, strings and counters. The `!coin`
branch that used to carry the ternary now reads `'no price data'` with
`hardSkip++` unconditionally, which is exactly what a non-`fut` asset already
did.

`bench/journal_bench.js` gained section **6a** (six cases, §3.5), and its `WHYS`
schema dictionary gained the two new strings. No existing assertion was weakened
or removed. `WHYS` is enforced two ways: an unknown reason fails, **and** a
reason never produced by the bench fails — so both new strings are executed
branches, not dictionary entries (`причины пропуска: 8/8`).

### Scope B — the board benches execute against the real registry

`verify_board.js`, `board2_bench.js` and `prot_bench.js` now read
`catalysts.json` from the checkout through
`require('../journal/write.js').loadCatalysts()` — the mechanism already written
for this, reused rather than reimplemented — and inject `CATALYSTS`,
`CAT_LOADED`, `CAT_ERR` into the sandbox after the script has run, the same way
`loadEngine()` does. No `XMLHttpRequest` stub was added and no second loader
exists. Injection happens **after** `vm.runInContext`, because the production
`var CATALYSTS = {}` would otherwise overwrite it.

A missing or invalid file prints one grep-able line and exits **non-zero**;
there is no fallback to an empty registry. Each bench carries one new assertion
that the registry actually loaded and is non-empty (§4.4).

### Scope C — the display contract re-specified and re-armed

Three expectations were stale — each correct under the 19.08 (3) contract and
reversed by invariant 34 on the same day. Production was checked against §5.1
before anything was touched and **agrees with the TZ, not with the benches**:

```js
// index.html tierBadge(), unmodified
'<span class="tier-badge" style="color:' + (act === 'none' ? '#888' : tier.c) + ';">'
     + tier.n + (row.no > 0 ? ' #' + row.no : '')
     + ' — ' + Math.round(row.sc.score) + stateMark(row) + '</span>'
// index.html assignRanks(), unmodified
r.no = (r.sc && has(r.sc.score) && !r.off) ? (++n) : 0;
// index.html tierOf(), unmodified — lowest tier
return { n: 'Фон', c: '#888' };
```

| Stale expectation | Replaced with | Where |
|---|---|---|
| lowest tier `Наблюдать` | `Фон` | `display_bench.py` `TIER_WORDS` + `want`; `render_bench.py` `TIER_WORDS`; `direction_bench.py` `want` |
| `RANK_RE = r'>#(\d+) '` | `r'#(\d+) — '` (rank after the tier word, before the em dash) | `display_bench.py` |
| `NUM_RE = r'^(?:#(\d+)\s+)?(\S+)\s+(\d+)'` | `r'^(\S+)(?: #(\d+))? — (\d+)'` | `render_bench.py` |
| only actionable rows numbered | `wants = sc !== null && !r.off` — every shown scored row | `direction_bench.py --display` |
| no coin numbered on both sides | permitted and **measured**: 3976 of 284 lists | `direction_bench.py --display` |

**Invariant 30 was not relaxed.** The one-side guarantee is carried by `action`
and asserted by `direction_bench.py --props` (`both` counter, failing on any
coin `trade` on both sides). That assertion was not touched and still passes.
What was reversed is only that the *number* stopped being a trade assertion.

The three benches are wired into `bench.yml` as separate named steps under
`shell: bash -euo pipefail {0}`, and the three corresponding header-comment
exclusions were removed. The remaining four exclusions (`backtest_bench.py`,
`badge_bench.js`, `clean_bench.py`, `direction_bench.py --identity`) stand with
their reasons intact. The inline comment above the `direction_bench.py` step,
which said `--identity` **and** `--display` are excluded, was corrected to name
only `--identity`.

### Scope D — the gate runs on the branch

```yaml
on:
  push:
    branches: [ main, 'claude/**' ]
```

`paths-ignore` and the `pull_request` trigger are unchanged. Not broadened to
`'**'`, per §6.1. This is not an argument on paper — see `## CI Execution`: the
gate executed three times on this branch, with **no pull request open**.

---

## Validation

Every item of §7 was attempted. One failed to run; it is named as failed.

### 7.1 Baseline — DONE
Recorded above, before any edit. All three §0 fingerprints matched exactly.

### 7.2 Syntax — PASSED

```
node --check <script> extracted from index.html : OK
python3 -m py_compile main.py                   : OK
node --check journal/write.js                   : OK
node --check bench/journal_bench.js             : OK
node --check bench/verify_board.js              : OK
node --check bench/board2_bench.js              : OK
node --check bench/prot_bench.js                : OK
python3 -m py_compile bench/display_bench.py    : OK
python3 -m py_compile bench/render_bench.py     : OK
python3 -m py_compile bench/direction_bench.py  : OK
```

### 7.3 No-regression statement — PASSED

**This TZ changed no production logic, and the diff proves it rather than
asserting it.** `index.html`, `main.py` and `catalysts.json` are byte-identical
to the §0 baseline:

```
$ git diff --stat -- index.html main.py catalysts.json
$ git diff --numstat -- index.html main.py catalysts.json | wc -l
0
$ md5sum index.html main.py catalysts.json
a7b10d80bea67824cf9643842d2e505a  index.html
1a5a5d98b2fd76010f202ee3eebaa717  main.py
eb591d2ef2d792ca6a4a25f26442e9b9  catalysts.json
```

The empty `--stat` output and the zero `--numstat` line count are the evidence:
zero changed lines in all three.

### 7.4 Scope A — one bullet of four failed to run

**Bullet 1 — `node bench/journal_bench.js`: PASSED.**

```
--- проверок: 694030  провалов: 0 ---   exit 0
  причины пропуска: 8/8, виды строк: g, o, oh, r, s, x
```
Baseline at unmodified HEAD (`git stash`): `проверок: 683068  провалов: 0`.
Delta +10 962, from section 6a's six new runs and the schema walk over their
files.

**Bullet 2 — live `--dry-run` against current data: FAILED TO RUN.**

```
$ node journal/write.js --dry-run
JOURNAL FAIL 2026-08-21 ... note="coeffs недоступен: http 403"   exit 1
$ curl https://gist.githubusercontent.com/.../coeffs.json
curl: (56) CONNECT tunnel failed, response 403
$ curl https://data-api.binance.vision/api/v3/ticker/24hr?symbol=BTCUSDT
curl: (56) CONNECT tunnel failed, response 403
```

This is the session's outbound network policy, not a defect in the change. Per
contract §9 the item **fails**; it is not "not applicable". It is the sole
reason `## Status` is PARTIAL.

**Substitute evidence, offered as what it is.** The real recorded day
`journal/data/2026-08-21.jsonl` was replayed through the production
`snapshot()` path — same `createJournal`, same classifier, same registry — with
the ticker rebuilt from the record and XMRUSDT/LITUSDT restored as the
zero-volume rows the mirror actually served that day:

```
cov=25  skip=3  status=ok  note=null
  x HYPE  futures-only: no spot mirror pair
  x XMR   futures-only: delisted spot mirror row
  x LIT   futures-only: delisted spot mirror row
hardSkip === 0  <=>  status === "ok"  ->  true
```

The same day, as actually recorded before this change:

```
{"k":"x","d":"2026-08-21","sym":"HYPE","why":"futures-only: no spot mirror pair"}
{"k":"x","d":"2026-08-21","sym":"XMR","why":"dead market"}
{"k":"x","d":"2026-08-21","sym":"LIT","why":"dead market"}
{"k":"r",...,"status":"partial","cov":25,"skip":3,...}
```

`partial` → `ok` on identical inputs, `cov 25`, `skip 3`, `hardSkip 0`. This is
a replay of live data through production code; it is **not** a live fetch, and
the live fetch is still owed. The replay script lived in the session scratchpad
and was not committed.

**Bullet 3 — negative control on each of the three branches: PASSED.** Forced
synthetically in `journal_bench.js` section 6a and, for the third branch, also
in the replay:

```
6a.1 нет пары        -> futures-only: no spot mirror pair            x3, status ok
6a.2 count=0         -> futures-only: delisted spot mirror row       x1, status ok, NOT dead market
6a.3 пустой стакан   -> futures-only: delisted spot mirror row       x1, status ok
6a.4 живая пара      -> futures-only: spot mirror row unexpectedly alive x3, status ok
                        note: "fut:true asset trading on spot: HYPE; ...XMR; ...LIT"
6a.5 все три формы в одном прогоне -> 1 / 1 / 1, skip 3, status ok
                        note: "fut:true asset trading on spot: LIT"
6a.6 мёртвая СПОТОВАЯ пара -> dead market x1, status partial   (§3.3 control)
```

Replay negative control, HYPE's spot row forced alive:
```
cov=25 skip=3 status=ok note="fut:true asset trading on spot: HYPE"
  x HYPE  futures-only: spot mirror row unexpectedly alive
```

Case 6a.6 is the control that matters most: the spot path still hard-skips and
still degrades `status` to `partial`. The change did not eat the degradation
signal, it removed a permanent false one.

**Bullet 4 — the record was never written: PASSED.**

```
$ git status --short journal/
 M journal/write.js
$ git diff --stat -- journal/data journal/runs.jsonl journal/out
$ ls journal/data/
2026-08-21.jsonl
```

No dated file was created, modified or reopened. Every bench and replay run wrote
into a temporary directory (`--dry-run` uses `mkdtemp`; the benches use `tmp()`).
Invariant 38 holds.

### 7.5 Scope B — PASSED

| Bench | Checks before | Checks after | Exit |
|---|---:|---:|---:|
| `verify_board.js` | 108 | **109** | 0 |
| `board2_bench.js` | 129 | **130** | 0 |
| `prot_bench.js index.html` | 167 | **168** | 0 |

**No existing number changed.** Each total rose by exactly the one assertion
§4.4 requires, so the empty registry was masking no difference — as §4.3
predicted, because all three live entries are `disputed` and therefore veto
nothing. Registry actually loaded: `3 coins, updated 2026-08-21` in all three.

Negative control — `catalysts.json` moved aside:

```
verify_board exit=1  FAIL catalyst registry: catalysts.json не прочитан (...): ENOENT
board2_bench exit=1  FAIL catalyst registry: catalysts.json не прочитан (...): ENOENT
prot_bench   exit=1  FAIL catalyst registry: catalysts.json не прочитан (...): ENOENT
```

Second negative control — file present but schema version 2:

```
verify_board exit=1  FAIL catalyst registry: catalysts.json: версия схемы не 1 (...)
board2_bench exit=1  FAIL catalyst registry: catalysts.json: версия схемы не 1 (...)
prot_bench   exit=1  FAIL catalyst registry: catalysts.json: версия схемы не 1 (...)
```

Restored, `md5 eb591d2ef2d792ca6a4a25f26442e9b9` (identical to baseline), all
three green again at 109 / 130 / 168, exit 0.

### 7.6 Scope C — PASSED

| Bench | Checks | Failures | Exit |
|---|---:|---:|---:|
| `display_bench.py` | 24 598 (6 311 card rows compared) | 0 | 0 |
| `render_bench.py` | 15 925 over 123 scenarios | 0 | 0 |
| `direction_bench.py --display` | 57 661 | 0 | 0 |

**Fails on zero comparisons (invariant 22).** None of the three had this guard;
each now does, and each was proven to use it:

```
display_bench.py, cases forced empty     : "0 card rows compared" -> exit 1
render_bench.py, cases forced empty      : "bench compared nothing" -> exit 1
direction_bench.py --display, cnt forced 0: "блок не сверил ничего" -> exit 1
```
Reverted in every case, exit 0 again. (See `## Deviations` — this guard is one
step beyond §5.2 and is flagged as such.)

Negative controls per bench, one deliberate deviation from §5.1 each, all
reverted afterwards with the file restored byte-for-byte:

| Bench | Injected deviation | Result |
|---|---|---|
| `display_bench.py` | lowest tier word back to `Наблюдать` | exit 1, reverted → exit 0 |
| `display_bench.py` | `RANK_RE` back to `>#(\d+) ` | exit 1, reverted → exit 0 |
| `render_bench.py` | `NUM_RE` back to the 19.08 (3) layout | exit 1, reverted → exit 0 |
| `render_bench.py` | lowest tier word back to `Наблюдать` | exit 1, reverted → exit 0 |
| `direction_bench.py --display` | `want[34.99]` back to `Наблюдать` | exit 1, reverted → exit 0 |
| `direction_bench.py --display` | numbering back to actionable-only | exit 1, reverted → exit 0 |

### 7.7 Scope D — the gate is proven to fail — PASSED

Three consecutive pushes to `claude/execute-tz-07-rgd98m`, **no pull request
open at any point**:

| # | Commit | What | Conclusion | URL |
|---|---|---|---|---|
| 28 | `8b78fe6` | the implementation | **success** | https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32535157006 |
| 29 | `ca902ce` | planted `display_bench.py` failure | **failure** | https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32535206722 |
| 30 | `2b8ffc1` | revert of the planted failure | **success** | https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32535228662 |

Run 29 failed on step 14, `Бейдж и нумерация карточек (display_bench.py)` — one
of the three steps this TZ added — and the two steps after it were skipped, so
the job conclusion is `failure` and not a printed failure with exit 0
(invariants 25, 29). Run 30's tree is byte-identical to run 28's
(`git diff 8b78fe6 HEAD --stat` → empty); the planted commit and its revert
remain in branch history on purpose, as the audit trail of this control.

### 7.8 Full gate — PASSED

Every step of `bench.yml`, in order, run locally and confirmed on the runner:

| # | Step | Checks | Exit |
|---:|---|---:|---:|
| 1 | `verify_board.js` | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 0 |
| 3 | `prot_bench.js index.html` | 168 | 0 |
| 4 | `verify_bench.py` | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 489 786 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 0 |
| 7 | `journal_bench.js` | 694 030 | 0 |
| 8 | `catalyst_bench.js` | 23 007 | 0 |
| 9 | `display_bench.py` *(new)* | 24 598 | 0 |
| 10 | `render_bench.py` *(new)* | 15 925 | 0 |
| 11 | `direction_bench.py --display` *(new)* | 57 661 | 0 |
| | **TOTAL** | **1 308 873** | |

Against TZ-06's **1 199 724**, the difference is **+109 149**, fully accounted
for and with nothing unexplained:

| Source | Delta |
|---|---:|
| `verify_board.js` — §4.4 registry assertion | +1 |
| `board2_bench.js` — §4.4 registry assertion | +1 |
| `prot_bench.js` — §4.4 registry assertion | +1 |
| `journal_bench.js` — section 6a and its schema walk | +10 962 |
| `display_bench.py` — newly inside the gate | +24 598 |
| `render_bench.py` — newly inside the gate | +15 925 |
| `direction_bench.py --display` — newly inside the gate | +57 661 |
| **Sum** | **+109 149** |

TZ-06's own total is reproduced exactly by summing the eight steps that were in
the gate then at their pre-change counts
(108+129+167+35+489 786+3 424+683 068+23 007 = 1 199 724), which is what makes
the delta an accounting rather than an estimate.

### 7.9 CI execution — see `## CI Execution`

---

## Test Results

Every bench in the gate, after the change, green on a GitHub runner (run 28) and
locally. Runner-side counts match local counts exactly — `journal_bench` 694 030,
`catalyst_bench` 23 007, `display_bench` 24 598 / 6 311 rows, `render_bench`
15 925, `direction --display` 57 661.

Benches outside the gate were not run and their status is unchanged:
`backtest_bench.py` (needs the archive), `badge_bench.js` (needs
`index.html.prev`), `clean_bench.py` (needs two positional HTML files),
`direction_bench.py --identity` (needs `orig.html`).

---

## Deviations

**One, declared: the invariant-22 zero-comparison guard in Scope C.** §7.6
requires each of the three display benches to "fail on zero comparisons
(invariant 22)". None of them did — all three returned 0 when nothing was
compared. §5.2 does not list this as an expectation change, so adding the guard
is one step beyond the letter of §5.2, taken because §7.6 states the property as
mandatory and contract §7.12 forbids putting anything in the gate that is not a
control. Three to six lines per bench, no assertion changed, no assertion
removed; it can only ever make a bench redder. If the Architect judges this out
of scope it is trivially revertible without touching anything else in the change.

For `display_bench.py` the guard counts **card rows compared**, not `checks`:
block E's eight tier probes are fixed in number and would have kept `checks`
positive on an empty case set, which would have made the guard decorative.

**Language of new text.** §8 requires new bench text in English and carves out
`journal/write.js` because that file is Russian throughout. The same reasoning
was applied to the two other files that are Russian throughout —
`bench/journal_bench.js` and `bench/direction_bench.py` — where edits continue in
Russian; new text in the English files (`verify_board.js`, `prot_bench.js`,
`display_bench.py`, `render_bench.py`) is English, and `board2_bench.js`, whose
section headings are already Russian, keeps them so. `bench.yml` is Russian
throughout and stayed Russian. No new raw Cyrillic entered any JS string literal;
this change introduced no UI strings at all.

Nothing else deviates. No scope was widened, no file outside `## Files Modified`
was touched, no production logic changed.

---

## Pre-existing Issues

These were found while working. They are **not** fixed here.

1. **`journal.yml` will keep writing `status: partial` until this branch is
   merged.** The defect is real today: the run of 21.08 recorded
   `status:"partial"` with `cov:25 skip:3` and no note, because XMRUSDT and
   LITUSDT classified as `dead market`. Every day between now and the merge adds
   another such record, and invariant 38 makes those records immutable — they
   will stay in the journal, permanently, as `partial` days that were healthy.
   Nothing can be done about the ones already written, and nothing should be.

2. **No bench in the gate had a zero-comparison guard except
   `journal_bench.js` and `catalyst_bench.js`.** Scope C's three now do. The
   remaining ones — `verify_board.js`, `board2_bench.js`, `prot_bench.js`,
   `verify_bench.py`, `fresh_bench.js`, `direction_bench.py` in its non-display
   blocks — were not touched, and a version of them that compared nothing would
   still exit 0. Reported, not fixed: their files are in scope for edits this TZ
   authorised, but this hardening is not what this TZ asked for.

3. **`direction_bench.py --display` counts checks as
   `lists * trades + len(tier)`.** That is a product of two unrelated
   quantities, not a count of comparisons, and it will read as ~57 661 whatever
   the fuzz actually verified. The new per-block zero guard makes it fail at
   zero, but the number itself remains an odd metric. Left alone: changing it is
   a specification decision.

4. **`index.html` line 770 still says `LIT — статус спот-пары не подтверждён`.**
   System Map §3.14 replaced that reasoning on 22.08 with a declaration by the
   Boss. The comment is now stale relative to the map. `index.html` is out of
   scope for this TZ (§2), so the comment was not touched.

---

## Remaining Risks

1. **The live path is still unproven from this session.** §7.4 bullet 2 could not
   run. The first genuine proof will be the next scheduled `journal.yml` run on
   `main` after merge, which reaches the mirror natively — the map records that
   path as live from Actions, confirming invariant 24's exception. Until then,
   the evidence for Scope A is a replay of recorded live data through production
   code, which is strong but is not the live path.

2. **The klines fallback will classify `fut:true` pairs as "unexpectedly
   alive" whenever the mirror serves their history.** When the ticker path fails
   and `fetchPrices()` falls back to candles, it requests candles for **every**
   token including the `fut:true` three. If `data-api.binance.vision` returns a
   series for a delisted spot pair, the row is present and non-zero, and §3.2's
   third case fires: the skip is recorded and `run.note` carries
   `fut:true asset trading on spot: XMR`. That is a faithful reading of what was
   observed — §3.2 demands the gap be measured, not assumed — but on a
   fallback day the note may read as an anomaly when it is an artefact of the
   fallback source. The behaviour is visible, bounded to `run.note`, and never
   touches `status`. Flagged rather than special-cased, because suppressing it
   would be exactly the silence §3.2 forbids.

3. **`bench.yml` now spends a runner execution on every `claude/**` push.** This
   change cost three of them (28, 29, 30), one of which was deliberately red.
   That is the accepted cost stated in §6.2 and is recorded here as a fact, not
   a complaint.

4. **A `confirmed` catalyst entry will now move the three board benches.** That
   is the point of Scope B — but it means the next registry change is the first
   one those benches can react to, and their fixtures are live board readings
   from 19-20.08. If a `confirmed` entry lands with a window covering those
   dates, the fixtures will legitimately change and the benches will go red for a
   correct reason. Contract §7.2 will apply then: that is a finding, not a
   licence to edit the assertion.

5. **Node 20 is deprecated on GitHub runners.** Every `bench.yml` run now prints
   `Node.js 20 is deprecated ... actions/checkout@v4, actions/setup-node@v4,
   actions/setup-python@v5 ... forced to run on Node.js 24`. It is a warning
   today, not a failure, and pinning action versions is not in this TZ's scope.

---

## Commit

Implementation, on `claude/execute-tz-07-rgd98m`:

```
8b78fe6 fix(controls): benches that verify nothing are not controls (TZ-07)
```

Two further commits on the same branch are the §7.7 negative CI control and its
revert. They are deliberate audit trail, and the branch head's tree is identical
to `8b78fe6`:

```
ca902ce test(ci): planted display_bench failure — negative control for the gate
2b8ffc1 Revert "test(ci): planted display_bench failure — negative control for the gate"
```

This report is committed directly to `main` (contract §8), never to the branch.

---

## Pull Request

**None exists.** This session runs under a base configuration that forbids
opening a pull request without an explicit instruction, which is the case
contract §8 (Version 6) defines a fallback for. The branch is pushed and
complete:

- **Branch:** `claude/execute-tz-07-rgd98m`
- **Compare URL:** https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-07-rgd98m

The Boss opens and merges from that link in one action.

**A branch with no pull request is a branch with no CI — and that is exactly
what Scope D of this TZ removed.** On TZ-06 that sentence held and cost the
project 1 199 724 checks that ran on nobody's runner. Here it does not: the
`Bench gate` executed three times on this branch with no pull request open, and
the proof is in `## CI Execution`. The missing pull request now costs the merge
button and nothing else.

---

## CI Execution

Workflows that executed on a GitHub runner for this change:

| Workflow | Run | Trigger | Branch | Conclusion |
|---|---|---|---|---|
| `Bench gate` | [28](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32535157006) | `push` (no PR) | `claude/execute-tz-07-rgd98m` | **success** |
| `Bench gate` | [29](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32535206722) | `push` (no PR) | `claude/execute-tz-07-rgd98m` | **failure** (intended, §7.7) |
| `Bench gate` | [30](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32535228662) | `push` (no PR) | `claude/execute-tz-07-rgd98m` | **success** |

All eleven bench steps executed on the runner in run 28, in `bench.yml` order,
each green — including the three steps this TZ added. Runner check counts are
identical to the local ones.

Workflows that did **not** execute, and why:

- `main.yml` (the bot) — not triggered: no push to `main` in this change, and
  `**/*.md` is in its `paths-ignore` so this report cannot start it either.
- `journal.yml` — daily schedule against `main`; it does not run on a branch.
  Its next run after merge is the live proof owed by §7.4 bullet 2.
- `backtest_bench.yml` — not touched and not triggered (contract §7.8).

A local run is not a runner run. Here both happened, and they agree; the one
thing that happened only locally — and imperfectly, because the network was
refused — is §7.4 bullet 2, named as failed above.

---

## Final Repository State

- Branch `claude/execute-tz-07-rgd98m` pushed, 3 commits ahead of `main`, tree
  identical to the implementation commit.
- Working tree clean. No scratch file, no `bench/_*`, no `__pycache__`, no
  duplicate and no superseded copy left behind (contract §13).
- `index.html`, `main.py` and `catalysts.json` byte-identical to `main`.
- `journal/data/**`, `journal/out/**` and `journal/runs.jsonl` untouched.
- No pull request exists; the compare URL above is the merge path.
- `Bench gate` conclusion on the branch head (`2b8ffc1`): **success**.

**NOT IN EFFECT UNTIL MERGED.**

---

## Fingerprints

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1770 | `5cc9fc6a4f618df3c4c02cc27595404e` |
| `index.html` | 3522 | `a7b10d80bea67824cf9643842d2e505a` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 15 | `eb591d2ef2d792ca6a4a25f26442e9b9` |

System Map, newest `## 9. Журнал миграций` entry: **2026-08-22**.

`index.html` and `main.py` are unchanged from the §0 baseline, which is the
point: this TZ restored controls and touched no production logic.
