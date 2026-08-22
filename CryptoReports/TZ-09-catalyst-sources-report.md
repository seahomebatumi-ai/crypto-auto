# Implementation Report — TZ-09

## Status

COMPLETED.

Both scopes executed. All eleven gate steps pass locally and on a GitHub runner.
The two mandatory negative controls of §4.10 were run red-then-green on the live
path. `index.html` and `main.py` are byte-identical to their pre-task state.

The previous TZ's branch **was merged** before this work started: `TZ-08` reached
`main` as PR #8 (`7874dda`, "Merge pull request #8 from
seahomebatumi-ai/claude/execute-tz-08-lpkhu2"). This branch is based on the
current `origin/main` tip (`93c2343`) — 1 commit ahead, 0 behind. This work is
not stacked on an unmerged base.

---

## Inbound Filing

None required. The specification arrived under its canonical name
`CryptoTZ/TZ-09-catalyst-sources.md` (§3 of the contract) and needed no `git mv`.

`git fetch --all --prune` was run before assessing anything (contract §4.2). The
clone was **shallow** (`git rev-parse --is-shallow-repository` → `true`), so
`git fetch --unshallow` was run before any historical assessment (contract §3);
history went from a truncated snapshot to 288 commits.

---

## Scope Executed

| Scope | Subject | Result |
|---|---|---|
| A | `catalysts.json` — the registry | completed |
| B | `bench/catalyst_bench.js` — quorum, enum, authority table, guards | completed |

Neither scope was blocked, so the §6/§2 fallback ("complete the other and report
the blocked one") did not apply.

---

## Files Created

None.

## Files Modified

- `catalysts.json`
- `bench/catalyst_bench.js`

## Files Renamed

None.

## Files Deleted

None. The AVAX and SOL **entries** were removed from `catalysts.json` per §3.1;
no file was deleted.

---

## Implementation Summary

### Scope A — the registry

`catalysts.json` was replaced with the byte-exact file specified in §3.1. The
three verification targets were reproduced independently:

| Property | Required | Measured |
|---|---|---|
| lines | 11 | 11 |
| MD5 | `021dd2c90dc395240c0b0c3dbae40426` | `021dd2c90dc395240c0b0c3dbae40426` |
| `t` decodes to | «итоги голосования NU7 14.09» | «итоги голосования NU7 14.09» |
| `cat.hash` | `629681cf148e6199` | `629681cf148e6199` |

The file is ASCII-only (0 bytes > 127) and `t` remains `\uXXXX`-escaped. The
`cat.hash` was computed twice: once through the journal's own exported
`loadCatalysts()` (`journal/write.js`), and once by an independent recompute of
`sha16(canon(items))` — both returned `629681cf148e6199`.

The ZEC entry's date moved from the day the NU7 vote **opens** to the day it
**resolves**, its `dir` moved from an opinion about the outcome to `both`, its
`conf` to `confirmed`, and it gained the primary `src` that earns that. AVAX and
SOL were deleted, not demoted: a `disputed` entry still annotates its own side,
so keeping them would have kept printing an argument built on a date no host
confirms.

### Scope B — the bench

Seven changes, all inside the functions §4 names:

1. **§4.1 quorum.** `quorumOk` replaced with the primary-source rule; the
   two-host branch deleted entirely. New helper `isPrimary` does dot-boundary
   suffix matching. `hostOf` unchanged. The paragraph above the function was
   rewritten to say that authority, not repetition, is the bar; the ENA sentence
   was kept and is now supported by the AVAX and HYPE probes from §1.
2. **§4.2 `PRIMARY`.** `'zfnd.org'` added, and nothing else. The comment states
   that the list is the registry's trust root and **changes only through a TZ**.
3. **§3.4 registry-edit rules.** Written into the file's header comment, where
   the next editor meets them, since JSON carries no comments.
4. **§4.3 case table.** Thirteen cases, replacing eight.
5. **§4.4 `DIRS`.** `['long', 'short', 'both']`. Schema version stays `1`;
   `KINDS`, `CONFS` and the key set untouched.
6. **§4.5 section 3 rewritten** from a fixed expectation into an authority table
   derived per entry. **§4.6** overlap guard and **§4.7** `updated` guard added.
7. **§4.4 `both` cases** added to section 4, proving through the production
   `catalystCheck` that the new enum value costs zero production changes.

**Not one line of production logic changed.** See `## Test Results` → §5.

---

## Validation

Every item of §6 was run. Nothing was marked "not applicable".

### §6.1 Baseline — recorded before any edit

System Map fingerprint gate (§0), all five anchors — **PASS**:

| Anchor | Required | Found |
|---|---|---|
| `<!-- EDIT-MARKER 2026-08-22-CATALYST-REGISTRY -->` | exactly 1 | 1 |
| `<!-- EDIT-MARKER 2026-08-22-GATE-COMPOSITION -->` | exactly 1 | 1 |
| `## 4. Инварианты`, highest number | 43 | 43 |
| `## 9. Журнал миграций`, newest entry | `- 2026-08-22 (2):` | `- 2026-08-22 (2):` |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1807 lines, MD5 `476339934c9dcf14e0f4bf2353900d89` | 1807, `476339934c9dcf14e0f4bf2353900d89` |

Scope-file baseline, before any edit:

| File | Lines required | Lines found | MD5 required | MD5 found |
|---|---:|---:|---|---|
| `catalysts.json` | 15 | 15 | `eb591d2ef2d792ca6a4a25f26442e9b9` | `eb591d2ef2d792ca6a4a25f26442e9b9` |
| `bench/catalyst_bench.js` | 392 | 392 | `06ae385e8e424a1a26aa51487a751b6c` | `06ae385e8e424a1a26aa51487a751b6c` |
| `index.html` | 3522 | 3522 | `68eebc9b5e40c7afd09a7d00d3fd1d21` | `68eebc9b5e40c7afd09a7d00d3fd1d21` |
| `main.py` | 506 | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | `1a5a5d98b2fd76010f202ee3eebaa717` |

All eight match. No mismatch, so no BLOCKED report.

### §6.2 Syntax and integrity

| Command | Exit |
|---|---:|
| `node --check bench/catalyst_bench.js` | 0 |
| `python3 -c "import json;json.load(open('catalysts.json'))"` | 0 |
| `node --check` on the `<script>` extracted from the untouched `index.html` | 0 |
| `python3 -m py_compile main.py` on the untouched file | 0 |

The §3.1 table (11 lines, MD5, decoded `t`, `cat.hash`) is reproduced in
`## Implementation Summary` above, with the commands used:

```
wc -l < catalysts.json                  -> 11
md5sum catalysts.json                   -> 021dd2c90dc395240c0b0c3dbae40426
python3 -c "...json.load(...)['items']['ZEC'][0]['t']"
                                        -> итоги голосования NU7 14.09
node -e "console.log(require('./journal/write.js').loadCatalysts().hash)"
                                        -> 629681cf148e6199
```

### §6.3 No-regression, proven not asserted

```
$ git diff --stat
 bench/catalyst_bench.js | 278 ++++++++++++++++++++++++++++++++++++++----------
 catalysts.json          |  16 ++-
 2 files changed, 226 insertions(+), 68 deletions(-)
```

Exactly two paths. `git diff --name-only` returns exactly `bench/catalyst_bench.js`
and `catalysts.json`; `index.html` and `main.py` appear 0 times.

`git diff -- catalysts.json` in full:

```diff
diff --git a/catalysts.json b/catalysts.json
index 12d06ba..720259c 100644
--- a/catalysts.json
+++ b/catalysts.json
@@ -1,15 +1,11 @@
 {
   "v": 1,
-  "updated": "2026-08-21",
+  "updated": "2026-08-22",
   "items": {
-    "ZEC":  [{ "d": "2026-08-25", "dir": "long",  "kind": "protocol",
-               "t": "голосование NU7 25.08",
-               "conf": "disputed", "src": [], "added": "2026-08-21" }],
-    "AVAX": [{ "d": "2026-09-18", "dir": "short", "kind": "unlock",
-               "t": "разлок 10.69M AVAX",
-               "conf": "disputed", "src": [], "added": "2026-08-21" }],
-    "SOL":  [{ "d": "2026-10-01", "dir": "long",  "kind": "protocol",
-               "t": "Alpenglow в октябре",
-               "conf": "disputed", "src": [], "added": "2026-08-21" }]
+    "ZEC": [{ "d": "2026-09-14", "dir": "both", "kind": "protocol",
+              "t": "итоги голосования NU7 14.09",
+              "conf": "confirmed",
+              "src": ["https://forum.zcashcommunity.com/t/nu7-coinholder-vote/56912"],
+              "added": "2026-08-22" }]
   }
 }
```

### §6.4 Scope B, rule level

**The thirteen §4.3 cases.** Executed against the shipped function text in
`bench/catalyst_bench.js`. **0 mismatches.**

| # | Expected | Actual | | Case | `src` |
|---:|---|---|---|---|---|
| 1 | pass | pass | MATCH | one primary source | `["https://zips.z.cash/zip-0253"]` |
| 2 | **block** | **block** | MATCH | **two independent aggregators — was `pass` before ТЗ-09** | `["https://tokenomist.ai/x","https://cryptorank.io/y"]` |
| 3 | block | block | MATCH | one aggregator alone | `["https://tokenomist.ai/x"]` |
| 4 | block | block | MATCH | no source at all | `[]` |
| 5 | block | block | MATCH | same aggregator twice | `["https://tokenomist.ai/x","https://www.tokenomist.ai/y"]` |
| 6 | block | block | MATCH | not a URL | `["со слов"]` |
| 7 | pass | pass | MATCH | `disputed` needs nothing | `[]` |
| 8 | pass | pass | MATCH | primary plus aggregator | `["https://github.com/zcash/zips/pull/1","https://cryptorank.io/y"]` |
| 9 | pass | pass | MATCH | subdomain of a primary | `["https://docs.ethena.fi/ena/tokenomics"]` |
| 10 | pass | pass | MATCH | `www.` and port stripped | `["https://WWW.Binance.com:443/en/support/announcement/detail/x"]` |
| 11 | block | block | MATCH | suffix lookalike | `["https://notethena.fi/x"]` |
| 12 | block | block | MATCH | primary as a left label | `["https://ethena.fi.attacker.com/x"]` |
| 13 | pass | pass | MATCH | the live ZEC entry | `["https://forum.zcashcommunity.com/t/nu7-coinholder-vote/56912"]` |

Row 2 is the change. The same `src` under the **old** two-host rule returns
`PASS`; under the new rule it returns `BLOCK`. Both were measured, not reasoned
about.

**The `both` semantics from §1**, reproduced by executing the production
`<script>` through node `vm` with the registry injected, no file edited —
`CAT_WINDOW_D` read from production = **14**. All six `conf`×`dir` combinations:

| `conf` / `dir` | LONG | SHORT | note LONG | note SHORT | §1 says |
|---|---|---|---|---|---|
| `confirmed` / `both` | veto | veto | — | — | veto / veto — **matches** |
| `confirmed` / `long` | — | veto | `X` | — | — / veto — **matches** |
| `confirmed` / `short` | veto | — | — | `X` | veto / — — **matches** |
| `disputed` / `both` | — | — | — | — | — / — — **matches** |
| `disputed` / `long` | — | — | `X` | — | — / — — **matches** |
| `disputed` / `short` | — | — | — | `X` | — / — — **matches** |

Outside the window (event 400 days out), all six combinations return
`{"veto":null,"note":null}` on both sides — **matches** §1's last row.

The four window edges, measured on `confirmed`/`both`:

| Offset | Result | §1 requires | |
|---|---|---|---|
| 14.00 days ahead | inside | inside | MATCH |
| 14.01 days ahead | outside | outside | MATCH |
| 1.00 day past | inside | inside | MATCH |
| 1.01 days past | outside | outside | MATCH |

**`dir:'both'` required zero production changes**, exactly as §1 claimed.

### §6.5 Scope B, file level

- **§4.6 overlap guard:** zero overlaps. The bench prints no `OVERLAP` line and
  `eq('no coin has two entries whose windows overlap', 0, 0)` passes.
- **§4.7 `updated` check:** `updated` = `2026-08-22`, newest `added` =
  `2026-08-22` → not older. Passes.
- **§4.9 count reconciliation:** see `## Test Results`.

### §6.6 Negative controls (§4.10) — both mandatory, both run

| # | Mutation on the live path | Exit | Failing check |
|---:|---|---:|---|
| 1 | ZEC `src` blanked to `[]` | **1** | `FAIL ZEC[0] passes quorum: got false want true` |
| 1 | restored | **0** | — (23 040 checks, 0 fails) |
| 2 | ZEC `src` → two aggregators | **1** | `FAIL ZEC[0] passes quorum: got false want true` |
| 2 | restored | **0** | — (23 040 checks, 0 fails) |

Control 2 is the case that passed before ТЗ-09 and is the whole point of §4.1.

Final `catalysts.json` MD5 after both controls: `021dd2c90dc395240c0b0c3dbae40426`
— equal to §3.1, and `cmp` reports the file byte-identical to the specified
content.

### §6.7 Full gate — all eleven steps of `bench.yml`, in order

See `## Test Results`.

### §6.8 CI

See `## CI Execution`.

---

## Test Results

### Full gate, local, in `bench.yml` order

| # | Step | Exit | Checks | §5 requires |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 0 | 109 | 109 ✓ |
| 2 | `board2_bench.js` | 0 | 130 | 130 ✓ |
| 3 | `prot_bench.js index.html` | 0 | 168 | 168 ✓ |
| 4 | `verify_bench.py` | 0 | 35 | 35 ✓ |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 0 | 188 577 | 188 577 ✓ |
| 6 | `fresh_bench.js` | 0 | 3 424 | 3 424 ✓ |
| 7 | `journal_bench.js` | 0 | 694 030 | 694 030 ✓ |
| 8 | `catalyst_bench.js` | 0 | **23 040** | (this TZ) |
| 9 | `display_bench.py` | 0 | 24 598 | 24 598 ✓ |
| 10 | `render_bench.py` | 0 | 15 925 | 15 925 ✓ |
| 11 | `direction_bench.py --display` | 0 | 15 629 | 15 629 ✓ |

**All ten fixed steps returned the numbers TZ-08 recorded, exactly.** No
deviation, no rounding difference.

**Gate total: 965 665.** §6.7 states it against **965 632**; the difference is
**+33**, which is exactly the `catalyst_bench.js` delta below. No other step
moved.

### §4.9 count reconciliation for `catalyst_bench.js`, by term

Baseline **23 007** (measured by running the unmodified bench against the
unmodified registry at `HEAD`, exit 0). New total **23 040**. Delta **+33**.

Per-section counts were measured, not estimated, by instrumenting throwaway
copies of both versions:

| Section | Old | New | Δ |
|---|---:|---:|---:|
| 0. Production surface | 20 | 20 | 0 |
| 1. Schema | 37 | 14 | −23 |
| 2. Quorum | 11 | 14 | +3 |
| 3. Sweep | 22 440 | 22 429 | −11 |
| 4. Window identity | 53 | 117 | +64 |
| 5. Degraded load | 445 | 445 | 0 |
| 6. Negative control | 1 | 1 | 0 |
| **Total** | **23 007** | **23 040** | **+33** |

By term:

| Term | Δ |
|---|---:|
| §4.3 new quorum cases (8 → 13 synthetic) | +5 |
| §4.4 new `both` cases (2 blocks × 8 edges × 4) | +64 |
| §4.6 overlap guard | +1 |
| §4.7 `updated` guard | +1 |
| swept-range coverage guard (see `## Deviations`) | +1 |
| notes that no longer exist (per-entry note assertions, 3 entries × 5) | −15 |
| registry: symbols 3 → 1, schema checks (2 per symbol) | −4 |
| registry: entries 3 → 1, schema checks (10 per entry) | −20 |
| registry: live quorum checks 3 → 1 | −2 |
| registry: symbols with no entry 25 → 27 | +2 |
| comparisons that replaced the sweep's bare `checks++` (22 400 → 22 400 `deq`) | 0 |
| **Net** | **+33** |

The reconciliation was cross-checked by separating the two causes. Running the
**new** bench against the **old** registry gives **23 064**, exit 0:

- bench-only delta (registry held constant): 23 064 − 23 007 = **+57**
- registry-only delta (bench held constant): 23 040 − 23 064 = **−24**
- +57 − 24 = **+33** ✓

That the new bench is **green on both editions of the registry** is the point of
§4.5: the expectation is derived from the data, not a snapshot of it. On the old
registry it independently reproduces what the old literal asserted — 0 days a
side was closed (all `disputed`), 45 days annotated (3 entries × 15 days on the
supporting side).

### §4.9 counts stay counts (инв. 43)

The sweep's bare `checks++`, which incremented outside any comparison, is gone.
Every increment in section 3 now happens inside `deq` at the comparison site.
The zero-comparison guard is unchanged:

```js
if (checks === 0) { console.log('FAIL bench verified nothing'); process.exit(1); }
```

### §4.8 no assertion depends on the current date

Proved by execution, not by inspection. The bench was run under a shifted wall
clock (`Date.now` offset by ±400 days):

| Clock offset | Exit | Checks | Fails |
|---:|---:|---:|---:|
| −400 days | 0 | 23 040 | 0 |
| 0 | 0 | 23 040 | 0 |
| +30 days | 0 | 23 040 | 0 |
| +200 days | 0 | 23 040 | 0 |
| +400 days | 0 | 23 040 | 0 |

Identical in every case. The three remaining `Date.now()` call sites are the
legal ones: section 0 against the pending (empty) registry, and section 5
against a registry that failed to load — both assert **silence**, which no date
can change.

### §5 what must not change

| Claim | Proof |
|---|---|
| `index.html` not edited | absent from `git diff --name-only`; MD5 `68eebc9b5e40c7afd09a7d00d3fd1d21` unchanged; 3522 lines |
| `main.py` not edited | absent from `git diff --name-only`; MD5 `1a5a5d98b2fd76010f202ee3eebaa717` unchanged; 506 lines |
| `SYSTEM-MAP-CRYPTOCALCUL.md` not touched | absent from the diff; MD5 unchanged |
| workflows not touched | absent from the diff |
| `dir:'both'` needs no production change | §6.4 matrix, executed through production `catalystCheck` (инв. 21), plus the diff |

No production change was found to be necessary, so the §5 / contract §7.2
"stop and report" path did not apply.

---

## Deviations

**One addition beyond the four terms §4.9 names.** Section 3 gained a
**swept-range coverage guard** (+1 check):

```js
ok('every entry window falls inside the swept range ' + firstDay + '..' + lastDay, ...)
```

§4.5 requires the authority table to hold "on all fifteen calendar dates ending
on `d`". The sweep proves that only for dates the sweep actually reaches: an
entry whose window fell outside `START..START+399` would satisfy every `deq` in
section 3 by comparing `null` against `null` — passing while verifying nothing,
which is the inv. 22 failure mode this file exists to catch. The guard asserts
the premise instead of assuming it.

It is called out here rather than folded silently into the reconciliation
because §4.9 enumerated four terms and this is a fifth. If the Architect
considers it out of scope, removing it costs one line and moves the bench total
to 23 039 and the gate total to 965 664.

No other deviation. No assertion was edited to make a bench pass, no gate step
was removed, no scope was widened.

---

## Pre-existing Issues

**None found that this task did not cause, and none fixed.**

For the record, one thing that *looks* like a defect and is not: the bench was
red on `main` at the moment this task began — but only against the §3.1
registry, never against the registry that was committed. The unmodified bench
against the unmodified registry exits 0 with 23 007 checks. The redness was
entirely §4.5's stale-expectation problem (`dir in enum` rejecting `both`, and
section 3's hard-coded "no live entry may veto"), which this TZ exists to fix.
It is not a product defect and was not treated as one.

---

## Remaining Risks

1. **From 31.08 to 15.09 the board refuses both sides of ZEC, by design.**
   `CAT_WINDOW_D = 14`, so the veto is live from **2026-08-31 00:00 UTC to
   2026-09-15 00:00 UTC**. On those fifteen calendar dates ZEC prints
   «нет сделки: итоги голосования NU7 14.09» on **both** LONG and SHORT, with no
   catalyst note anywhere. This was measured, not predicted: the sweep reports
   30 side-days closed (15 dates × 2 sides) and 0 annotated, and the first
   closed date is day 91 from `START` = **2026-08-31**. Nothing else on the
   board moves — score, rank, tier, leverage, liquidation and range position are
   computed exactly as before (инв. 31: a catalyst may only veto). **If this is
   read as a bug during those fifteen days, it is not.**

2. **The System Map still carries the pre-ТЗ-09 wording.** Invariant 39 and
   §3.15 still state the old source quorum ("два НЕЗАВИСИМЫХ хоста либо один
   первичный источник"), and invariant 43 still names ТЗ-08 as the next TZ. The
   map is one edition behind on purpose and **the Executor did not touch it**.
   Until the Architect republishes it, the repository's normative description of
   the quorum contradicts the code that enforces it. Code comments cite
   «§3.15 / инв. 39, изменён ТЗ-09» rather than a bare invariant number that does
   not exist yet.

3. **The trust root is now a single list.** With the two-host branch gone, an
   entry is `confirmed` if and only if one host in `PRIMARY` (or a subdomain of
   one) stands behind it. That is the intent, and it concentrates the authority:
   adding a host to `PRIMARY` promotes every future entry citing it. The comment
   states the list changes only through a TZ, but nothing mechanically enforces
   that — it is a convention held by review.

4. **`kind` is unconstrained by the quorum rule.** `KINDS` still accepts
   `unlock`, and §1's finding is that aggregated unlock data is not evidence.
   An `unlock` entry can still reach `confirmed` if a primary source publishes an
   unlock calendar. That is correct as specified; it is noted only so the next
   registry edit does not read the AVAX deletion as a ban on the `kind`.

5. **Not in effect until merged.** See `## Final Repository State`.

---

## Commit

```
c28ed19  feat(catalysts): sources, primary-source quorum, two-sided event risk (TZ-09)
```

Commit message used verbatim from §8. Two files, exactly the implementation:
`catalysts.json` and `bench/catalyst_bench.js`. The working tree is clean; the
scratch files the benches generate (`bench/_*`, `__pycache__/`) were removed and
are gitignored in any case.

Branch: `claude/execute-tz-09-u6irz8`, based on `origin/main` at `93c2343`,
1 commit ahead and 0 behind.

---

## Pull Request

**No pull request exists.** This session runs under a base configuration that
forbids opening one without an explicit instruction, and the Boss's trigger was
`EXECUTE TZ-09` and nothing else. Per contract Version 6 §8 this is a defined
fallback, not a blocker and not a question for the Boss.

- **Branch:** `claude/execute-tz-09-u6irz8`
- **Compare URL:** https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/execute-tz-09-u6irz8

The Boss opens and merges from that link in one action, after the Architect's
audit returns ПРИНЯТО.

**The CI consequence contract §8 warns about does NOT apply here: this branch
has CI.** §8's rule — "a branch with no pull request is a branch with no CI" —
described the trigger set as it stood at ТЗ-06, when `bench.yml` fired only on
`push` to `main` and on `pull_request`. **ТЗ-07 §6 closed exactly that hole by
adding `claude/**` to the push triggers**, and it worked: the `Bench gate`
executed on this branch push, on a GitHub runner, with no pull request in
existence. Details under `## CI Execution`.

---

## CI Execution

| Workflow | Ran on a runner | Run | Conclusion |
|---|---|---|---|
| `Bench gate` (`bench.yml`) | **yes** | #41 | **success** |
| `main.yml` (bot) | no | — | not triggered: `**/*.md` and the bot's paths-ignore, plus this push is to a `claude/**` branch, not `main` |
| `journal.yml` | no | — | scheduled workflow, writes `journal/**` on `main`; nothing in this change triggers it |
| `backtest_bench.yml` | no | — | needs the `data.binance.vision` archive and a warmed cache; deliberately outside this gate |

- **Run number:** 41
- **Run URL:** https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/32569888495
- **Conclusion:** success
- **Head SHA:** `c28ed19c502c9bb9313befd7253321133ddcbe7c`
- **Trigger:** `push` to `claude/execute-tz-09-u6irz8`

All eleven bench steps reported `success` on the runner, including
`Слой катализаторов (catalyst_bench.js)`. Counts observed **in the runner log**,
confirming the local run rather than merely resembling it:

```
--- проверок: 694030  провалов: 0 ---            (journal_bench.js)
--- checks: 23040  fails: 0 ---                  (catalyst_bench.js)
display_bench: 24598 checks, 0 failures
render_bench: 123 scenarios, 15925 checks, 0 failures
ИТОГО проверок: 15629 | провалов блоков: 0       (direction_bench.py --display)
```

The runner's `catalyst_bench.js` section banners also match the local run
line for line — `symbols: 1, entries: 1`, `synthetic cases: 13, live confirmed
entries: 1`, `calls: 22400, days a side was closed: 30, days a side was
annotated: 0`, `symbols with no entry stay silent: 27` — so the 30 closed
side-days of §3.2 are a fact established on a runner, not only locally.

Independent corroboration of the registry hash from a different bench on the
same runner: `journal_bench` printed
`journal_bench: движок 70d0a02082a44341, реестр 629681cf148e6199, монет 28`.
That `реестр` value is the `cat.hash` required by §3.1, produced by the journal's
own loader on a clean checkout.

One pre-existing, non-blocking runner warning, unrelated to this change:
`actions/checkout@v4`, `actions/setup-node@v4` and `actions/setup-python@v5`
target Node.js 20, which GitHub is deprecating, so the runner forced them onto
Node.js 24. The job still concluded `success`. `bench.yml` is out of scope for
this TZ and was not touched; this is noted for the Architect, not acted on.

**No failure was planted in CI**, per §6.8. §4.10 already supplies two
red-then-green controls on the live path, and both were exercised locally with
their exit codes recorded above.

The local gate and the runner gate are distinct facts and are reported as such:
the eleven-step table under `## Test Results` is a **local** run, and this
section is the **runner** run. Both are green.

---

## Final Repository State

- `main` is unchanged by this task except for this report.
- The implementation lives on `claude/execute-tz-09-u6irz8`, pushed, with the
  `Bench gate` green on a runner.
- No pull request exists; the compare URL is above.
- **NOT IN EFFECT UNTIL MERGED.**

GitHub Pages serves `index.html` from `main`, so the calculator continues to run
the pre-ТЗ-09 registry and quorum rule until the Boss merges. This report is on
`main` under `CryptoReports/`, which cannot reach the live calculator
(Pages serves `index.html`) and cannot start the bot (`**/*.md` is in
`main.yml`'s `paths-ignore`). Both facts were re-checked and still hold.

---

## Fingerprints

| File | Lines | MD5 |
|---|---:|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1807 | `476339934c9dcf14e0f4bf2353900d89` |
| `index.html` | 3522 | `68eebc9b5e40c7afd09a7d00d3fd1d21` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/catalyst_bench.js` | 554 | `80da4fb4935bf42df10141da1db3145f` |

- `SYSTEM-MAP-CRYPTOCALCUL.md` newest `## 9. Журнал миграций` entry:
  **`- 2026-08-22 (2):`** — unchanged, the map was not touched.
- `catalysts.json` MD5: **`021dd2c90dc395240c0b0c3dbae40426`**
- `catalysts.json` `cat.hash`: **`629681cf148e6199`**

`index.html` and `main.py` carry the same line counts and MD5s as the §0
baseline, which is the arithmetic proof that no production logic changed.
