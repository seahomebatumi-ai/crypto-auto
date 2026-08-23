# Implementation Report — TZ-10

List-level exhaustion state in the regime banner.

## Status

**PARTIAL.**

Stage A is implemented in full. Stage B's instrument is built, self-tested and
negative-controlled, but **the calibration run itself could not execute**: every
archive host is refused by this session's egress policy. Stage C therefore has
**no constant to write** and is **not implemented** — nothing on screen changes
at this revision.

This is the outcome TZ-10 §2 Stage B already anticipates for a blocked
calibration ("the stage is ЗАБЛОКИРОВАНО and reported **without a production
change**"), reached by a different route: not a percentile outside the
registered window, but no percentile at all.

The one thing that would unblock it: run
`python3 bench/exhaustion_calib.py --years 3` from a host where
`data.binance.vision` answers — a GitHub Actions runner does (inv. 24).

## Inbound Filing

None. `CryptoTZ/TZ-10-exhaustion-state.md` was already present on `origin/main`
under its canonical filename after `git fetch --all --prune`. No artifact
arrived under a mangled name, nothing was moved or renamed.

One clone-state note, recorded because contract §3 makes it binding: the session
clone was **shallow** (`git rev-parse --is-shallow-repository` → `true`).
`git fetch --unshallow` was run before any history was assessed; the complete
clone carries 295 commits. Related: the local `main` branch in the fresh clone
pointed at `ffb4a8e`, which is **not** `origin/main` (`3a92fb2`). Every baseline
comparison in this report is taken from `origin/main`, and the MD5 below proves
which file was compared.

## Scope Executed

| Stage | TZ requirement | Outcome |
|---|---|---|
| A | `dayRangeRatio`, `listExhaustion`, no consumer | **Executed in full** |
| B | `bench/exhaustion_calib.py`, run once, number recorded | **Instrument built; run BLOCKED** — no number exists |
| C | `DAY_RANGE_ABNORMAL`, `update()` call site, banner text/colour | **Not implemented** — strictly downstream of B |
| — | `bench/exhaustion_bench.js` + `bench.yml` wiring | **Executed**, covering every case well-defined without Stage C |

Stages A and C are not independent: Stage C step 1 is
`DAY_RANGE_ABNORMAL <value from Stage B>`. Contract §6 says to complete what is
independent and report what is blocked; A is independent, C is not. Writing a
guessed constant would violate the rule TZ-10 registered under inv. 23 before
the number was known, so no constant was written.

Nothing from §3 Non-goals was implemented or is proposed here.

## Files Created

| File | Lines | Purpose |
|---|---:|---|
| `bench/exhaustion_bench.js` | 404 | Control for the new measure; wired into `bench.yml` |
| `bench/exhaustion_calib.py` | 381 | Stage B calibration; manual, deliberately NOT in `bench.yml` |
| `CryptoReports/TZ-10-exhaustion-state-report.md` | — | This report (direct to `main`, contract §8) |

## Files Modified

| File | Change | Diff |
|---|---|---|
| `index.html` | `dayRangeRatio`, `listExhaustion` added next to `sigmaDay` | **+47, −0** |
| `.github/workflows/bench.yml` | one step added (the 12th bench step) | **+10, −0** |

`git diff --numstat` on the commit:

```
47   0   index.html
10   0   .github/workflows/bench.yml
404  0   bench/exhaustion_bench.js
381  0   bench/exhaustion_calib.py
```

Every change is an insertion. **Zero lines were removed or altered in any
existing file.** No change to `main.py`, `catalysts.json`, `journal/**`,
`SYSTEM-MAP-CRYPTOCALCUL.md`, or any other workflow.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

### Fingerprint gate — PASSED

Run before any work, against the repository copy of the map.

| Anchor | Required | Found |
|---|---|---|
| revision | `**Revision 2026-08-22-b.**` | present |
| direction engine | `### 3.12 Direction engine — veto cascade` | present |
| catalyst registry | `### 3.15 Catalyst registry` | present |
| newest invariant | `43. **A check count must be a count.**` | present |

Map revision string: **Revision 2026-08-22-b** — equal to the revision TZ-10
requires, not older. Baseline `index.html` measured **3522 lines**, MD5
`68eebc9b5e40c7afd09a7d00d3fd1d21` — identical to both the TZ header and the
map's `## 0. Fingerprint` block. `main.py` (506 / `1a5a5d98…`) and
`catalysts.json` (11 / `021dd2c9…`) also match the map exactly. No file is
ahead of the map; nothing to report under §5's divergence rule.

Baseline confirmed: TZ-09 merged as PR #9 (`ae47103`), and its report
`CryptoReports/TZ-09-catalyst-sources-report.md` is on `main`. The previous TZ's
branch **was** merged, so this work is not stacked on an unmerged base.

### Stage A — the measure, with no consumer

Both functions were inserted immediately after `sigmaDay` (now `index.html:1246`
onward), which is the site TZ-10 names.

`dayRangeRatio(hi, lo, cur, vol)` returns the day's range divided by the range a
driftless walk would produce over the same day. The comment block is the TZ's
own text, verbatim.

- The daily-sigma conversion goes through **`sigmaDay(vol)`** (inv. 20). The
  function never recomputes `vol * Math.sqrt(24)`. This is asserted by
  *behaviour*, not by reading the source: the bench swaps the production
  `sigmaDay` for a ×4 variant and requires the ratio to move by exactly ¼.
- `Math.sqrt(8 / Math.PI)` appears **once**, inside the function.
- Returns `null` — never `0`, never `Infinity` — on any missing or non-finite
  argument, on `cur <= 0`, on `vol <= 0`, and on `hi <= lo` (so `hi === lo` is
  null too). Two extra guards catch arithmetic the domain checks do not: a
  denominator that **underflows** to zero, and a ratio that **overflows** to
  Infinity. Both return `null`.
- ES5 only: `var`, string concatenation, no arrow functions, no `let`/`const`,
  no template literals.

`listExhaustion(rows)` returns `{ median, n, abnormal }` over the assembled row
list.

- Reads each row's `hi24`, `lo24`, `cur` and `cd.volatility` and calls
  `dayRangeRatio` per row.
- `n` counts only rows that produced a non-null ratio. Rows with no metrics, no
  pair or a dead market carry no `cd` and contribute nothing.
- `median` is `null` and `abnormal` is `false` when `n < 8`. `n` itself is still
  reported truthfully below quorum.
- Sorting is numeric, not lexicographic (asserted: `10` must not sort between
  `1` and `2`).
- It is a separate named function so a bench can call it (inv. 34).
- **`abnormal` is left permanently `false`**, exactly as Stage A specifies.

**No consumer exists.** `update()` was not touched. `marketRegime` was not
touched. `regimeBanner` was not modified. Evidence under *Validation* below.

### Stage B — the instrument, and why it did not run

`bench/exhaustion_calib.py` is complete and runnable:

- **Universe** resolved correctly to **25 spot pairs of 28 declared tokens**.
  The three `fut:true` assets (HYPE, XMR, LIT) are excluded **by declaration**
  (inv. 41), not by observation — the script filters `tokens[]` on the flag and
  never asks a host whether they answer. Its own output line states the
  coverage as 25 of 28.
- **No second implementation of anything.** `dayRangeRatio` and `sigmaDay` (and
  `has`, which `dayRangeRatio` calls) are cut out of `index.html` by brace
  matching and executed by **node** (inv. 21, inv. 38(1)), using
  `backtest_bench._skip_to_matching_brace` so the cut itself has one
  implementation in the repository rather than two. `volatility` is not
  computed here either: it comes from `main.py`'s own metric block through
  `backtest_bench.CdBuilder`, the same path `backtest_bench.py` uses.
- **No new dependency, no new host** (inv. 24). Data comes through
  `backtest_bench.fetch_prices(..., source="vision")` — the same
  `data.binance.vision` monthly hourly ZIPs and the same `bench/cache`.
- **The registered rule is enforced by the script, not by its operator.** The
  window `1.60 .. 4.00` is a module constant; a rounded p90 outside it prints
  `BLOCKED`, states that Stage C makes no production change, and returns
  non-zero. The number cannot be quietly nudged by whoever runs it.
- Per coin-day it takes `hi`/`lo` from that day's **24** hourly candles (a day
  with fewer is skipped — a partial day has a partial range), `cur` as the
  day's last close, and `vol` as the trailing 90-day hourly volatility at that
  day's last candle.
- Output is `n`, the full decile table (p0…p100, linear interpolation, stated
  in-code so the number is reproducible), per-coin `n`/p50/p90, and the pooled
  p90 raw and rounded.

**The run is blocked by network policy.** Every archive host is refused at
CONNECT by this environment's egress proxy:

```
$ python3 bench/exhaustion_calib.py --years 3
Universe: 25 spot of 28 declared tokens (fut:true excluded by declaration, inv. 41): HYPE, XMR, LIT
Cut out of index.html: has, sigmaDay, dayRangeRatio

Cache incomplete (0 of 25) — the archive is needed.
Source availability:
  архив data.binance.vision        нет связи — ProxyError
  зеркало data-api.binance.vision  нет связи — ProxyError
  боевой api.binance.com           нет связи — ProxyError
  боевой fapi.binance.com          нет связи — ProxyError
  api.coingecko.com                нет связи — ProxyError

BLOCKED: 'vision' does not answer from this host, and the cache is cold.
The calibration cannot run without the archive. This is an environment blocker,
not a defect in the measure: run it where data.binance.vision is reachable.
EXIT=2
```

The underlying error is `OSError: Tunnel connection failed: 403 Forbidden`, and
the proxy's own diagnostic endpoint records it as
`connect_rejected … gateway answered 403 to CONNECT (policy denial)` for
`data.binance.vision:443`, `data-api.binance.vision:443` and
`api.binance.com:443`. The environment's documentation states plainly that a 403
from the proxy is an organisation egress denial and must be **reported, not
retried or routed around**. `bench/cache` does not exist in the container and is
`.gitignore`d, so there is no warm cache to fall back on.

**No route around it was taken, and one was available and rejected.** The
archive answers from a GitHub Actions runner. Reaching it would have required
wiring `exhaustion_calib.py` into a workflow — but TZ-10 §4 states the file is
"**NOT** wired into `bench.yml` (one-shot calibration, not a control)",
`bench.yml`'s own header excludes benches needing the external archive, and
`backtest_bench.yml` is closed to edits by hard floor §7.8 because TZ-10 does
not name it. Adding the step anyway would have produced the number by breaking
the specification that asked for it.

**`DAY_RANGE_ABNORMAL` therefore does not exist, and Stage C was not written.**

### Stage C — not implemented

No constant was added to the constants block. `update()` has no new call site.
`regimeBanner` is byte-for-byte the function that is on `main`. The amber
`#e0a02a` does not appear anywhere in `index.html`, and the bench asserts that
it does not.

## Validation

Every item TZ-10 §5 lists, with its outcome.

### §5.1 — Syntax

| Check | Result |
|---|---|
| `node --check` on the extracted `<script>` block | **OK** |
| `node --check bench/exhaustion_bench.js` | **OK** |
| `python3 -m py_compile bench/exhaustion_calib.py` | **OK** |
| `python3 -m py_compile main.py` (standing check) | **OK** |

ES5 guard on the added lines: no `=>`, no `let`, no `const`, no template
literal. Cyrillic guard: **0** lines of raw Cyrillic added to `index.html`, and
**0** in `bench/exhaustion_bench.js` — the one Russian word the bench needs is
written `'\u0410\u041D\u041E\u041C\u0410\u041B\u042C\u041D\u042B\u0419'` (hard floor §7.7).

### §5.2 — `bench/exhaustion_bench.js`

Cuts `dayRangeRatio`, `sigmaDay`, `listExhaustion` and `regimeBanner` out of
`index.html` and executes them (inv. 21). Non-zero exit on any failure, on zero
comparisons, **and** on a per-section counter sum that disagrees with the check
total (inv. 22, inv. 43).

| §5.2 case | Status | Where |
|---|---|---|
| Identity, ≥ 200 000 random finite inputs, 1e-12 | **Covered** | A (200 000) |
| Routes through `sigmaDay` (inv. 20) | **Covered**, added | A1 (2) |
| Nulls: never `0`, never `Infinity` | **Covered** | B (20 027) |
| Median and quorum, even/odd, exclusion, `n < 8` | **Covered** | C (65) |
| **Threshold edge (`median === DAY_RANGE_ABNORMAL` fires)** | **NOT WRITTEN** | needs Stage C |
| Banner, 8 × `abnormal === false` | **Covered** (10, a superset) | D (52) |
| **Banner, 8 × `abnormal === true`** | **NOT WRITTEN** | needs Stage C |
| Purity: same frozen `reg` → identical string, no mutation | **Covered** | F (22) |
| Inertness: the measure reaches no consumer | **Covered**, added | E (30) |
| Negative control: the bench can fail | **Covered** | G (1) |

The two omitted cases are omitted because the code they assert against does not
exist. Inventing a threshold to test against is exactly the retune inv. 23
forbids. The bench's own header records this and names the sections that extend
when Stage C lands.

Two cases were **added** beyond §5.2 because Stage A's contract needs them:
A1 proves the inv. 20 routing behaviourally, and E proves the new measure is
inert — `regimeBanner` returns an identical string whether `reg.day` is absent,
set with `abnormal: true`, or set below quorum.

Section D covers **ten** combinations rather than eight: the four banner
branches with `trend` split by direction, because the branch picks a different
colour for each. It is a strict superset of the eight §5.2 requires.

### §5.3 — Replay on the live journal (a measurement, not a check)

Counted separately from the check total, as §5.3 requires. The recorded
`px.hi`, `px.lo`, `px.cur` and `cd.volatility` from the checkout were fed into
the **extracted production functions**.

| Date | rows | n | median | fires? |
|---|---:|---:|---:|---|
| `journal/data/2026-08-21.jsonl` | 25 | 25 | **1.6878** | no threshold exists |
| `journal/data/2026-08-22.jsonl` | 25 | 25 | **2.4298** | no threshold exists |

Neither date can fire: `abnormal` is permanently `false` at this revision and
`DAY_RANGE_ABNORMAL` does not exist. The medians are reported as measurements.

**The 2026-08-22 replay independently reproduces the TZ's own figures**, which
is the strongest available evidence that `dayRangeRatio` computes the quantity
the Architect measured:

| TZ §1 statistic | TZ states | This implementation measures |
|---|---:|---:|
| median ratio, 25 covered coins | 2.43 | **2.4298** |
| coins above 2.0 | 20 / 25 | **20 / 25** |
| `GRAM` the lowest ratio in the list | 1.34 | **1.34, and lowest** |

Full 2026-08-22 distribution, ascending:
`GRAM 1.34 · ETH 1.61 · SKY 1.67 · TRX 1.92 · XLM 1.97 · ENA 2.11 · YFI 2.23 ·
BNB 2.23 · UNI 2.26 · ALGO 2.32 · RENDER 2.36 · TAO 2.40 · AAVE 2.43 ·
BCH 2.44 · NEAR 2.52 · ZEC 2.59 · FET 2.72 · LINK 2.77 · AVAX 2.93 ·
HBAR 2.96 · ONDO 2.96 · SOL 3.20 · ADA 3.27 · SUI 3.54 · XRP 4.26`

2026-08-21 for contrast: median 1.6878, only 6 of 25 above 2.0.

### §5.4 — No-regression statement, explicit

**With `abnormal === false` the rendered board is byte-identical to
`origin/main`, and no output of the new code reaches `scoreCandidate`,
`tradeGeometry`, `leverageDecision`, `directionVerdict` or the journal writer.**

Four independent lines of evidence establish it.

**1. The diff cannot change behaviour.** `git diff --numstat index.html` →
`47  0`. Forty-seven insertions, **zero deletions**; `git diff -U0 | grep -c '^-[^-]'` → `0`.
No existing line was altered. The two new functions are top-level declarations.

**2. Neither function is reachable.** A full-file scan finds `listExhaustion`
exactly once — its own definition, called from nowhere. `dayRangeRatio` appears
twice: its definition, and one call from inside `listExhaustion`. A brace-matched
scan of each named consumer's body:

```
scoreCandidate       calls new code: no
tradeGeometry        calls new code: no
leverageDecision     calls new code: no
directionVerdict     calls new code: no
journal/write.js     calls new code: 0 occurrences
```

`reg.day` is referenced nowhere in `index.html`.

**3. Whole boards, real data, byte for byte.** Both revisions were loaded into
identical sandboxes and driven through the production `boardHtml` with the same
**real** inputs — all 50 recorded journal snapshots from 2026-08-21 and
2026-08-22 — across side × leverage × stress. No section was stripped; this is a
true byte comparison.

```
boards compared      : 900   (50 journal snapshots x side x leverage x stress)
bytes compared       : 12 827 013
boards differing     : 0
regimeBanner compared: 30    (5 states x isLong x {no day, abnormal:true, below quorum})
banners differing    : 0
EXIT=0
```

The baseline is `origin/main`'s `index.html`, MD5
`68eebc9b5e40c7afd09a7d00d3fd1d21` — the file the TZ header names.

**4. Every pre-existing bench reports the same check count as before.** See the
term-by-term table below: the eleven prior steps sum to **exactly 965 665**, the
map's stated total, unchanged to the unit.

### §5.5 — Full gate, 12 steps, term-by-term delta

The eleven pre-existing steps are unchanged, and their counts are the evidence:

| # | Step | Checks | Δ |
|---:|---|---:|---:|
| 1 | `verify_board.js` | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 0 |
| 3 | `prot_bench.js index.html` | 168 | 0 |
| 4 | `verify_bench.py` | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 188 577 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 0 |
| 7 | `journal_bench.js` | 694 030 | 0 |
| 8 | `catalyst_bench.js` | 23 040 | 0 |
| 9 | `display_bench.py` | 24 598 | 0 |
| 10 | `render_bench.py` | 15 925 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 0 |
| | **subtotal, eleven prior steps** | **965 665** | **0** |
| 12 | `exhaustion_bench.js` *(new)* | **220 199** | **+220 199** |
| | **TOTAL, twelve steps** | **1 185 864** | **+220 199** |

The subtotal equals the map's `965 665` exactly. The whole delta is the new
step, and the new step's own total decomposes into per-comparison counters the
bench prints and cross-checks (inv. 43):

| Section | Comparisons |
|---|---:|
| A. identity vs the closed form (200 000) + A1. `sigmaDay` routing (2) | 200 002 |
| B. nulls: 27 enumerated cases + 20 000 out-of-domain fuzz | 20 027 |
| C. `listExhaustion` median, exclusion, quorum, shape | 65 |
| D. `regimeBanner`, every `abnormal === false` case | 52 |
| E. inertness — the measure reaches no consumer | 30 |
| F. purity — deterministic, no mutation | 22 |
| G. negative control | 1 |
| **SUM** | **220 199** |

The bench fails hard if this sum does not equal its own check total.

### §5.6 — Extremes

Covered inside the bench rather than asserted in prose: `reg.known === false`
(the `unknown` banner state) is one of the ten combinations in sections D and E,
including with `reg.day` attached — so the "`btcStats` absent + exhaustion
clause" combination is exercised. Dead-market rows, no-pair rows, rows with a
`cd` lacking `volatility` and rows that are `null`/`undefined` are all in
section C's exclusion fixture. Truncated-Gist and HTTP-400-ticker handling is
untouched by this change: no code on those paths was modified, and the 900-board
comparison above renders from the recorded snapshots without divergence.

### Negative tests (contract §9 — a gate never proven to fail is not a gate)

Five real defects were planted in `index.html`, one at a time, and the new gate
step was run against each. The tree was restored after every one.

| # | Planted defect | Result |
|---|---|---|
| 1 | `dayRangeRatio` bypasses `sigmaDay` (numerically identical today) | **exit 1**, 1 fail |
| 2 | quorum lowered from 8 to 3 | **exit 1**, 5 fails |
| 3 | a null return becomes `0` | **exit 1**, 2 338 fails |
| 4 | trend banner colour changed to amber | **exit 1**, 4 fails |
| 5 | even-`n` median stops averaging | **exit 1**, 1 fail |

Defect 1 matters most: it is invisible to any numeric comparison, because
`cur * vol * sqrt(24) * K` and `cur * sigmaDay(vol) * K` are the same number
today. Section A1 catches it behaviourally.

After restoring, `git diff --numstat index.html` → `47  0` and the bench returns
**220 199 checks, 0 fails, exit 0**.

The Stage B self-test was negative-controlled the same way: a 1 % error planted
in the production denominator turned it red (2 fails, exit 1); reverted, it
returns 12 checks, 0 fails, exit 0.

## Test Results

Full local run of all twelve gate steps, in `bench.yml` order:

```
verify_board      EXIT=0    109 checks
board2            EXIT=0    130 checks
prot              EXIT=0    PASS 168  FAIL 0
verify            EXIT=0     35 checks
direction_main    EXIT=0    188 577 checks
fresh             EXIT=0    3 424 checks
journal           EXIT=0    694 030 checks
catalyst          EXIT=0    23 040 checks
display           EXIT=0    24 598 checks
render            EXIT=0    123 scenarios, 15 925 checks
direction_disp    EXIT=0    15 629 checks
exhaustion        EXIT=0    220 199 checks     <- new
```

Twelve of twelve green, 0 failures, **1 185 864 checks**.

`bench/exhaustion_calib.py --selftest` — 12 checks, 0 fails, exit 0. It proves
the cut, the node hop, null preservation across the JSON boundary, day grouping
(24 stamps make a day, 23 make none) and the percentile path. It does **not**
substitute for the calibration run and is not claimed to.

A local run is not a runner run. See `## CI Execution`.

## Deviations

1. **Stage C not implemented, and Stage B's run not performed.** Cause and
   reasoning are in `## Status` and *Stage B* above. This is the report's
   central deviation.

2. **Two §5.2 bench cases not written** — the threshold edge and the eight
   `abnormal === true` banner cases. Both assert against Stage C code. Recorded
   in the bench's own header so the omission is visible at the file, not only
   here.

3. **Two bench sections added beyond §5.2** (A1 `sigmaDay` routing, E
   inertness). Neither changes production; both exist because Stage A's contract
   — "routes through `sigmaDay`", "no consumer" — is otherwise asserted nowhere.

4. **A resolved ambiguity the Architect should confirm before Stage C.** TZ-10
   says `listExhaustion` "reads each row's already-parsed `hi24`, `lo24`, `cur`
   and `cd.volatility`". Two readings exist: the row carries `hi24`/`lo24`/`cur`
   as fields, or `listExhaustion` re-parses them from `row.coin.highPrice` and
   friends. **The first was implemented**, because `cd.volatility` is written as
   a property path on the row and symmetry makes `hi24`/`lo24`/`cur` property
   paths too, and because "already-parsed" excludes parsing inside the function.
   It is not reported BLOCKED because both readings produce identical numbers on
   screen and the choice is not yet load-bearing: nothing calls the function.
   **It becomes load-bearing in Stage C.** Under the implemented reading,
   Stage C's `update()` work is one added line inside the existing `if (sideOn)`
   block, where `hi24` and `lo24` are already parsed:
   `row.cur = curP; row.hi24 = hi24; row.lo24 = lo24;`
   If the Architect intended the other reading, `listExhaustion` changes and
   `update()` does not.

5. **`bench/exhaustion_calib.py` gained a pre-flight host probe** beyond the
   TZ's description, so a closed host reports itself as a blocker and exits 2
   instead of surfacing as a stack trace 25 pairs later. It changes no number.

6. **No `## Commit Message` section exists in TZ-10**, so the message was
   composed following the repository's established convention
   (`type(scope): summary (TZ-NN)`).

## Pre-existing Issues

**1. `prot_bench.js`'s optional baseline suite fails against any baseline,
including a byte-identical one.**

Found while gathering §5.4 evidence. `suiteNoRegression` strips the
`ЗАЩИТА ПОЗИЦИИ` section from the **candidate** before comparing, on the
assumption — correct when it was written — that the baseline predates that
section. Both revisions now contain it, so the comparison is guaranteed to
differ by exactly that section.

Proof it is not caused by this change:

| Run | Candidate | Baseline | Result |
|---|---|---|---|
| A | this branch | `origin/main` | PASS 1885, **FAIL 6** |
| B | `origin/main` | `origin/main` *(the same file)* | PASS 1885, **FAIL 6** |
| C | this branch | *(none — how the gate runs it)* | PASS 168, **FAIL 0**, exit 0 |

Run B is the control: a file compared against itself fails identically. The six
failures are a **stale expectation**, the same category TZ-07 dealt with, not a
product defect and not a regression.

**It does not affect the gate.** `bench.yml` invokes
`node bench/prot_bench.js index.html` with no baseline argument, so the suite is
skipped and the step is green on the runner. Not fixed: hard floor §7.2 forbids
editing a bench to make it pass, and `prot_bench.js` is outside TZ-10's scope.

**2. `bench.yml` pins `node-version: "20"`, which GitHub has deprecated.** The
runner reports it as a warning on every job: `actions/checkout@v4`,
`actions/setup-node@v4` and `actions/setup-python@v5` "are being forced to run
on Node.js 24". Nothing fails today and the gate is green, but the pin is a
scheduled breakage. Not touched: TZ-10 authorises one added step in
`bench.yml`, not a version bump.

**2. `main` in a fresh session clone does not point at `origin/main`.** The
local `main` was `ffb4a8e`; `origin/main` is `3a92fb2`. Any comparison taken
against local `main` is against the wrong file — this was caught mid-run when a
board comparison failed for reasons unrelated to the change, and every result in
this report is taken from `origin/main`. Recorded because it is a live trap for
the next session, not because anything in the repository is wrong.

## Remaining Risks

1. **The board carries no exhaustion state.** The defect TZ-10 exists to close
   is still open: on a session like 2026-08-22 the banner still reads
   `ТРЕНД ВВЕРХ — счёт по каналу импульса` in green with a measured list median
   of 2.43. Stage A only makes the number computable.

2. **`DAY_RANGE_ABNORMAL` is unknown, and the replay does not bound it.** Two
   days are not a distribution. The p90 could still land outside `1.60 .. 4.00`,
   in which case TZ-10's own registered rule makes Stage C blocked on the
   merits rather than on the environment. Nothing here pre-empts that.

3. **`listExhaustion` currently reads row fields nothing sets.** By design —
   Stage A has no consumer — but it means the row-field contract of Deviation 4
   is exercised only by hand-built bench fixtures, never by a production row.

4. **The exhaustion bench will need extending, not just enabling, at Stage C.**
   Its section E asserts today's inertness. When Stage C wires the comparison,
   E's `abnormal: true` assertions must invert rather than be deleted, or the
   inversion will look like a regression.

5. **`bench/exhaustion_calib.py` has never fetched a byte.** Its offline path is
   proven; its network path — month enumeration, the daily-file tail, cache
   warming — is `backtest_bench.py`'s own well-exercised code, but the
   composition has not run end to end. Budget for one shakeout run.

## Commit

```
c6d2bb5  feat(display): list-level exhaustion measure, no consumer yet (TZ-10)
```

Four files, 842 insertions, 0 deletions. Branch: `claude/execute-tz-10-b5ln3k`.
Working tree clean; no scratch file, cache or `__pycache__` committed. The
replay and board-comparison scripts used for evidence were run from a scratch
directory outside the repository and are deliberately not committed — TZ-10 §4
does not authorise them, and they are measurements, not controls.

This report is committed separately, directly to `main` (contract §8).

## Pull Request

**No pull request exists.** This session's configuration does not open one
without an explicit instruction, and the contract's §8 fallback applies.

- Branch: **`claude/execute-tz-10-b5ln3k`** (pushed)
- Compare URL: **https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-10-b5ln3k**

Unlike TZ-06, **CI did run on a runner for this branch**: `bench.yml`'s triggers
include `push` to `claude/**`, which TZ-07 added for exactly this reason. See
`## CI Execution`.

## CI Execution

**`Bench gate` executed on a GitHub Actions runner and its conclusion is
SUCCESS.**

| | |
|---|---|
| Workflow | `Bench gate` (`.github/workflows/bench.yml`) |
| Run | [32607941756](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32607941756), run number 48, attempt 1 |
| Trigger | `push` to `claude/execute-tz-10-b5ln3k` |
| Commit | `c6d2bb5ea84aa11e198dedaea9b662e423677eab` |
| Runner | `ubuntu-latest` |
| Conclusion | **success** |
| Duration | 00:28:20 → 00:29:20 UTC (60 s) |

All 12 bench steps returned success on the runner, the new step among them:

```
 6  Доска 19.08 против продакшн-математики (verify_board.js)      success
 7  Доска 20.08, LONG + SHORT + два экрана (board2_bench.js)      success
 8  Блок «ЗАЩИТА ПОЗИЦИИ» + фаззинг доски (prot_bench.js)         success
 9  Офлайн-набор для --verify (verify_bench.py)                   success
10  Движок направления (direction_bench.py)                       success
11  Свежесть данных — пауза расписания против сбоя (fresh_bench.js) success
12  Журнал вердиктов, офлайн (journal_bench.js)                   success
13  Слой катализаторов (catalyst_bench.js)                        success
14  Бейдж и нумерация карточек (display_bench.py)                 success
15  Отрисовка списка целиком (render_bench.py)                    success
16  Отображение и порядок (direction_bench.py --display)          success
17  Истощение списка и баннер режима (exhaustion_bench.js)        success   <- new
```

The runner's own output for step 17 is identical to the local run, counter for
counter — the check total is a runner fact, not a laptop fact:

```
--- per-section comparison counters ---
  identity: 200002
  nulls: 20027
  quorum: 65
  banner: 52
  inert: 30
  purity: 22
  control: 1
  SUM: 220199

--- checks: 220199  fails: 0 ---
```

**Workflows that did not run, and why.** `main.yml` did not run: it is the data
bot, `**/*.md` is in its `paths-ignore`, and no branch push triggers it.
`journal.yml` did not run: it is scheduled at 13:00 UTC and writes journal
records, which this change does not touch. `backtest_bench.yml` did not run: it
is `workflow_dispatch`-only, needs the archive, and TZ-10 does not name it —
hard floor §7.8 keeps it closed.

**`bench/exhaustion_calib.py` did not execute on a runner either**, and that is
the blocker in `## Status`, not an omission: TZ-10 §4 forbids wiring it into
`bench.yml`, and it is the one place the archive would have been reachable.

## Final Repository State

- `main`: unchanged by the implementation. It receives only this report under
  `CryptoReports/`, which cannot reach the live calculator — GitHub Pages serves
  `index.html`, and `**/*.md` is in `main.yml`'s `paths-ignore`. Both facts were
  re-checked and still hold.
- `claude/execute-tz-10-b5ln3k`: carries the implementation, one commit ahead of
  `main`.
- No pull request open. Merging is the Boss's action, after the Architect's
  verdict.

**NOT IN EFFECT UNTIL MERGED.**

And even once merged, nothing changes on screen: Stage C is not implemented, so
the board at this revision is byte-identical to `main` by construction.

## Fingerprints

Measured on the branch at commit `c6d2bb5`.

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1017 | `661a1c3eb9532887b9ffa3e5ee587839` |
| `index.html` | **3569** | `56af2e274e5568527a6bb0e5cb4e3456` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |

System Map revision string: **`Revision 2026-08-22-b.`**

`index.html` moved from 3522 to 3569 lines (+47) and its MD5 changed
accordingly; that is the only intended fingerprint change. `main.py`,
`catalysts.json` and the System Map are byte-unchanged and still match the map's
`## 0. Fingerprint` block exactly.

On `main`, `index.html` remains 3522 lines / `68eebc9b5e40c7afd09a7d00d3fd1d21`
until the branch is merged.
