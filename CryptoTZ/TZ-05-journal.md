# TZ-05 — Verdict journal: entry → board verdict → outcome

**Canonical filename: `TZ-05-journal.md`.** Commit the file under this exact name
in `CryptoTZ/`, regardless of the name it arrived with. If the name you received
contains spaces or underscores, rename it from this line — the header is the
identifier, not the transport (System Map, Appendix A item 16 of the project
contract).

**Claude Code model: Opus.** Four new files, one CI edit, network fallback logic
and an append-only data format whose mistakes are permanent — a wrong field name
in record #1 cannot be fixed in record #900 without splitting the sample.

---

## 0. Fingerprint gate — verify BEFORE any work

Run `git fetch --all --prune` first. "Not in my working tree" is not "not in the
repository" — TZ-02 was declared missing from a clone that had never fetched.

Then verify all six anchors. Any mismatch → stop, do nothing, report
**ЗАБЛОКИРОВАНО** naming the failed anchor.

| # | Anchor | Where |
|---|---|---|
| 1 | `<!-- EDIT-MARKER 2026-08-21b-JOURNAL -->` present | `SYSTEM-MAP-CRYPTOCALCUL.md` |
| 2 | Newest migration entry is dated `2026-08-21 (2)` | `SYSTEM-MAP-CRYPTOCALCUL.md` §9 |
| 3 | Invariants **37** and **38** exist | `SYSTEM-MAP-CRYPTOCALCUL.md` §4 |
| 4 | `function freshnessState(` present | `index.html` |
| 5 | `def run_line(` present | `main.py` |
| 6 | `origin/main` is checked out and clean | git |

Anchors 4–5 are TZ-04 landing on `main`. TZ-05 records the sample whose
integrity TZ-04 guarantees; building the journal on top of a bot that can fail
silently produces holes indistinguishable from "no events" (inv. 37).

Record in the report: line count and `sha256` of `index.html`, `main.py` and
`SYSTEM-MAP-CRYPTOCALCUL.md` as checked out.

---

## 1. Objective

Record, once per calendar day, what the board actually said about every coin —
its inputs, its verdict, the catalyst registry that was in force and the engine
that produced it — and, 7 and 14 days later, what the price actually did.

This is a **measuring instrument, not a feature**. Nothing in it is displayed,
nothing in it feeds back into any calculation, no user-facing behaviour changes
by one pixel.

**Why it is urgent enough to precede everything else in the §10 queue:** the
verdict is not reconstructible after the fact. `history.json` keeps betas, R²
and rank only — no price, no `min/max`, no `volatility`, no volume — and
`scoreCandidate`, `tradeGeometry` and `leverageDecision` all require exactly the
fields it does not keep. Every un-journaled day is lost permanently.

---

## 2. Hard constraints

1. **The verdict is produced by EXECUTING the production script (inv. 21).** The
   writer extracts the single `<script>` block from the checked-out `index.html`,
   executes it in a Node `vm` context with a DOM stub, and calls the production
   functions by name. **A second implementation of any verdict rule, threshold or
   formula — in any language, in any file — is an automatic ОТКЛОНЕНО.** If a
   value is not obtainable by calling a production function, it is not recorded;
   see §4.6 for the one deliberate omission and its reason.
2. **`index.html` and `main.py` are not modified by this TZ. Not one byte.** The
   `git diff` on those two paths must be empty in the report.
3. **Records are append-only at the filesystem level.** The writer never opens an
   existing file for modification and never deletes one. If a target file exists,
   that item is skipped as a duplicate and logged as such (inv. 38).
4. **No new API load on CoinGecko and no change to the bot's trigger.** The
   journal reads the Gist and Binance market-data mirrors only.
5. **Binance production hosts are HTTP 451 from GitHub Actions (inv. 24).** Only
   `data-api.binance.vision` and `data.binance.vision` are usable. Any call to
   `api.binance.com` or `fapi.binance.com` from the workflow is a defect.
6. **Clock-dependent presentation state is not recorded.** The runner's clock is
   UTC; the board's schedule is the Boss's local time. Record `generated_at` and
   the raw age in minutes; do **not** call `freshnessState` in the writer — the
   state is derived at analysis time by whoever holds the right clock.

---

## 3. Files

| Path | Kind | Note |
|---|---|---|
| `journal/write.js` | new | writer + outcome resolver, Node, no dependencies outside the standard library |
| `journal/README.md` | new | ≤ 40 lines: schema pointer to map §3.13, how to run locally, what the modes do |
| `.github/workflows/journal.yml` | new | `schedule` + `workflow_dispatch` only — never `push` |
| `bench/journal_bench.js` | new | offline validator, no network |
| `.github/workflows/bench.yml` | edit | wire in `fresh_bench.js` **and** `journal_bench.js` |
| `journal/data/`, `journal/out/`, `journal/runs.jsonl` | runtime | written by the workflow, not by you |

Modes of `journal/write.js`:

- `--probe` — reachability and shape of every endpoint; writes nothing; exits
  non-zero if the mandatory sources are unreachable.
- `--dry-run` — full pipeline into a temp directory; writes nothing into
  `journal/`; prints the record it would have written.
- `--snapshot` — today's snapshot + gap backfill.
- `--resolve` — outcome files that have come due.
- default (no flag) — `--snapshot` then `--resolve`, which is what the workflow runs.

---

## 4. Record schema — normative

One JSON object per line, UTF-8, `\n`-terminated, no pretty-printing. Field
names are frozen by this section and by map §3.13; do not add, rename or
reorder. Absent values are the JSON literal `null` — never `undefined`, never
`NaN`, never an empty string standing in for a number.

### 4.1 Snapshot file — `journal/data/YYYY-MM-DD.jsonl`

Written once per date, never touched again. One line per covered coin:

```
{"k":"s","d":"2026-08-21","ts":"2026-08-21T13:00:07Z","sym":"SUI","pair":"SUIUSDT",
 "gen":"2026-08-21T12:41:03Z","age":19,
 "px":{"src":"ticker","cur":2.02,"p24":-3.1,"qv":91000000,"hi":2.11,"lo":1.98,"cnt":118432},
 "reg":{"mode":"range","dir":0,"eff":0.1474,"z":0.4170,"known":true},
 "cd":{ ...the coin's analysis_data row, verbatim and unrounded... },
 "btc":{ ...coeffs.btc, verbatim and unrounded... },
 "rp":12.4,
 "long":{ ...side block... },
 "short":{ ...side block... },
 "cat":{"acting":[{"d":"2026-08-25","dir":"long","t":"…"}],"hash":"a1b2c3d4e5f60718"},
 "fp":{"script":"ebc3a85d8548765f","commit":"1a2b3c4d5e6f"}}
```

Side block, identical shape for `long` and `short`:

```
{"rel":true,"score":20.4,"tier":"Фон","ch":"возврат","action":"wait","why":"",
 "note":null,"verdict":"ждать $1.9873 — вход далеко от суточной опоры",
 "wait":1.9873,"tgt":3.40,
 "geo":{"rr":9.33,"reward":0.683,"risk":0.0732,"tgtSig":4.19},
 "dec":{"ok":true,"L":3,"binding":"структура","moneyBelowMin":false,
        "parts":{"struct":6.1,"noise":4.8,"btc":9.2,"money":4.7}},
 "inv":{"dist":0.0732,"price":1.8721,"dStruct":0.0732,"capped":false,"floored":false,
        "sd":0.0294,"ref":1.9010,"src":"мин30"}}
```

Field provenance — every one of these comes from a production call, and no
other way:

| Field | Source |
|---|---|
| `reg` | `marketRegime(btc)`, called **once per run** for the whole list |
| `rp` | `rangePos(cd, cur)` |
| `rel` | `sideRelevant(rp, isLong)` |
| `dec`, `inv` | `leverageDecision(cd, cur, isLong, btc)`; `inv` is its `.inv` object recorded **verbatim, all eight fields** |
| `score`, `ch`, `action`, `why`, `note`, `wait`, `geo` | `directionVerdict(cd, pair, sym, cur, p24, qv, isLong, reg, dec, hi, lo, residual7(cd, btc), tsMs)` |
| `tier` | `tierOf(score).n` |
| `verdict` | `verdictNote(row)` on a row built from the same `vd`/`cd`/`coin` objects |
| `tgt` | `cd.max_price` for long, `cd.min_price` for short — read, not recomputed |

Where a production function returns an object — `reg`, `geo`, `dec.parts`, `inv` —
record **every field it returns**, verbatim and unrounded. A field left out today
cannot be recovered from a record written a year ago, and the cost of carrying it
is bytes.

`tsMs` is the snapshot instant passed explicitly as `nowMs`, so the catalyst
window is reproducible. Production passes `null` there and falls back to
`Date.now()`; the journal must not, or a re-run of the same date would produce a
different verdict.

`cat.acting` is the subset of `CATALYSTS[sym]` inside the live window at `tsMs`
— the same `days < -1 || days > CAT_WINDOW_D` filter, obtained by reading the
registry, not by re-deriving `catalystCheck`'s decision (the decision is already
recorded in `why`/`note`). `cat.hash` is `sha256` of the whole `CATALYSTS`
literal as extracted, first 16 hex chars: it identifies the registry version even
for coins with no events, which is what makes the coming `catalysts.json` step
measurable.

`fp.script` is `sha256` of the extracted `<script>` block, first 16 hex chars.
`fp.commit` is `GITHUB_SHA`, first 12. Together they pin the exact engine that
produced the verdict; pooling records across engine versions without checking
them is how a journal starts lying.

### 4.2 Skip lines

A coin that cannot be covered still gets a line, in the same file:

```
{"k":"x","d":"2026-08-21","sym":"XMR","why":"futures-only: no spot mirror pair"}
```

Reasons, exactly these strings: `futures-only: no spot mirror pair` ·
`no price data` · `bot error flag` · `no bot row` · `dead market` ·
`no metrics`. **Silent omission of a coin is a defect**: the count of snapshot
lines plus skip lines must equal the length of `tokens[]`, and the bench asserts
that identity.

### 4.3 Run log — `journal/runs.jsonl`

Appended once per run, and once per backfilled gap date:

```
{"k":"r","ts":"2026-08-21T13:00:07Z","d":"2026-08-21","status":"ok",
 "cov":25,"skip":3,"px":"ticker","gen":"2026-08-21T12:41:03Z","age":19,
 "resolved":[{"d":"2026-08-14","h":7,"n":25},{"d":"2026-08-07","h":14,"n":25}],
 "note":null}
{"k":"g","d":"2026-08-20","why":"no run","found":"2026-08-21T13:00:07Z"}
```

`status` ∈ `ok` · `partial` (some coins skipped beyond the standing
futures-only three) · `dup` (the date's file already existed) · `fail` (nothing
written; `note` carries the reason).

### 4.4 Gap backfill — the arithmetic that makes a hole impossible to hide

On every run, for every calendar date strictly between the newest date present
in `journal/data/` and today, write one `k:"g"` line. A missing scheduled run
therefore leaves a labelled hole, not an absence.

The identity the bench enforces, and the reason this rule exists:

```
count(distinct snapshot dates) + count(gap dates) == calendar days from first run to today
```

A sample with unexplained holes cannot support a single statistical claim, and
"no record" is otherwise indistinguishable from "no events". Same family as
inv. 22: count the observations before judging them.

### 4.5 Outcome files — `journal/out/YYYY-MM-DD-h7.jsonl`, `…-h14.jsonl`

One file per (snapshot date × horizon), written once, never rewritten. First
line is the BTC header, then one line per coin that has a snapshot line:

```
{"k":"oh","d":"2026-08-14","h":7,"asof":"2026-08-21T13:00:00Z","src":"klines",
 "btc":{"p0":69727,"p1":71110,"hi":72540,"lo":67980}}
{"k":"o","d":"2026-08-14","h":7,"sym":"SUI","p0":2.02,"p1":2.31,"hi":2.44,"lo":1.93,
 "long":{"tgt":null,"stop":null,"wait":"2026-08-15T04:00:00Z","first":null},
 "short":{"tgt":null,"stop":"2026-08-16T11:00:00Z","wait":null,"first":"stop"}}
```

- `p0` is the snapshot's `px.cur`, carried across — not re-fetched, so the
  outcome is measured from exactly the price the verdict saw.
- `p1`, `hi`, `lo` come from hourly klines over `[ts, ts + h·24h]`.
- `tgt` / `stop` / `wait` are the **ISO hour of first touch** of that side's
  recorded target, invalidation price and wait price, or `null` if never
  touched. `first` ∈ `tgt` · `stop` · `tie` · `null`, where `tie` means both
  levels fell inside the same hourly candle and the order is genuinely
  unresolvable at this data granularity. Recording `tie` rather than guessing is
  mandatory — a guessed ordering is a fabricated outcome.
- Levels are taken from the snapshot line. **They are never recomputed**: a
  target recomputed from today's `cd` is a different target.

### 4.6 Deliberate omission — the rank `#N` is not recorded

The board's `#N` is produced inside `update()` by sorting with `byScore`,
filtering rows into the collapsed strip (`score < TIER_MIN`, then
`sideRelevant`), and numbering with `assignRanks`. That chain lives in the
render function and is not callable in isolation, so recording `#N` would
require reimplementing it — exactly what inv. 21 forbids. It is fully derivable
at analysis time from the recorded `score`, `rp`, `rel` and `tier` using the same
production functions. Do not record it, and do not approximate it.

---

## 5. Writer behaviour — `--snapshot`

1. Read `index.html` from the working tree; extract the single `<script>` block;
   execute it in `vm` with a DOM stub. `GIST_URL`, `STALE_CRIT_MIN`,
   `CAT_WINDOW_D`, `TIER_MIN`, `CATALYSTS` and `tokens[]` are **read out of that
   context** — none of them is retyped into the writer (inv. 20).
2. Fetch `coeffs.json` from the production `GIST_URL`. On failure: run line
   `status:"fail"`, exit non-zero, write nothing.
3. Fetch prices. Preferred path: `GET https://data-api.binance.vision/api/v3/ticker/24hr?symbols=[…]`
   for every non-`fut` pair in one request → `px.src = "ticker"`.
   Fallback, used only when that endpoint is unusable:
   `GET …/api/v3/klines?symbol=<pair>&interval=1h&limit=25` per pair →
   `px.src = "klines"`, with `cur` = last close, `hi`/`lo` = extremes of the last
   24 candles, `p24` = last close against the open 24 candles back, `qv` and
   `cnt` = sums over those 24. The fallback is a documented approximation of the
   exchange's rolling window, which is why `px.src` is recorded on every line.
   Never silently mix sources inside one file: one source per run.
4. `fut:true` pairs (`HYPE`, `XMR`, `LIT`) have no spot mirror. **Attempt them
   anyway** — coverage is measured, not assumed — and on failure emit the
   `futures-only: no spot mirror pair` skip line. Do not add a futures endpoint.
5. Degrade exactly as the board degrades (inv. 11–12): no bot row, `error`
   flag, `count === 0` or an empty book → the matching skip line, never a
   partial record.
6. `marketRegime(btc)` once; then per coin per side, the call chain of §4.
7. Write `journal/data/<today>.jsonl` **only if it does not exist**; otherwise
   log `status:"dup"` and exit 0.
8. Backfill gap lines per §4.4; append the run line.

## 6. Outcome resolver — `--resolve`

For each horizon `h ∈ {7, 14}` and each snapshot date `d` with
`d + h ≤ today` and no `journal/out/<d>-h<h>.jsonl`: fetch hourly klines for the
window, compute §4.5, write the file once. A resolution that cannot fetch its
data writes **nothing** and leaves the file absent, so the next run retries —
a partial outcome file is worse than none, because it is immutable.

Resolve oldest-first, and cap the work at 4 outcome files per run so a long
outage cannot produce a request storm.

## 7. CI wiring — `.github/workflows/bench.yml`

Add two steps in the file's existing style, each with
`shell: bash -euo pipefail` (inv. 25 — a step piping to `tee` returns `tee`'s
code and a failed bench looks green):

- `node bench/fresh_bench.js`
- `node bench/journal_bench.js`

Both must fail the job on a non-zero exit, and both must print their check
count. **A bench that is not wired into `bench.yml` never executes and is
therefore not a control** — `fresh_bench.js` has been in that state since
TZ-04. If `bench.yml` triggers on `push`, add `paths-ignore: ['journal/**']`
so the journal's own data commits do not re-run the suite.

## 8. `.github/workflows/journal.yml`

```
on:
  schedule: [{cron: '0 13 * * *'}]     # 13:00 UTC — inside the Shortcuts window
  workflow_dispatch:
permissions: {contents: write}
concurrency: {group: journal, cancel-in-progress: false}
```

No `push` trigger, under any condition — the job commits to the branch it runs
on, and a push trigger closes that loop. Steps: checkout `main` with full
history · Node 20 · `node journal/write.js` · commit **only** paths under
`journal/` with `git add journal` (never `git add -A`) · `git pull --rebase`
before push, one retry on non-fast-forward · commit message
`journal: <date> [skip ci]`. If nothing changed, exit 0 without committing.

The cron hour is chosen so the snapshot lands inside the Boss's active
schedule (Shortcuts run hourly 09:00–01:50 local, §1) under any offset from
UTC+0 to UTC+4, ~4 h after the day's first bot run at the earliest offset. This
adds no CoinGecko calls and does not touch the bot's trigger; the Boss's
Shortcuts automation is untouched and undiscussed here (Appendix A item 17).

## 9. Validation — `bench/journal_bench.js`, offline, no network

Written by the Architect; run it, do not redesign it. Fixtures are synthetic
`coeffs.json` payloads and synthetic ticker/kline payloads injected through an
explicit fetch seam in `write.js` — the seam exists so this bench needs no
network, and it is the only concession the writer makes to testability.

Minimum coverage, each one asserting and counting:

1. **Verdict identity — ≥ 5 000 records.** For randomised coin metrics, BTC
   stats spanning all three regimes, and both sides: every recorded verdict
   field equals a direct call to the production function on the same inputs.
   This is the control against a second implementation creeping in, so it must
   compare the record against a fresh call, not against a stored expectation.
2. **Determinism.** The same inputs and the same `tsMs` produce a byte-identical
   file across two runs, including key order.
3. **Immutability.** Running `--snapshot` twice on one date: the second run
   modifies no file (compare content hashes and mtimes), logs `status:"dup"`,
   exits 0.
4. **Gap arithmetic.** Simulated 3-day outage: exactly 3 gap lines with the
   correct dates, and the §4.4 identity holds over a 30-date simulated span,
   including a run that fails mid-way.
5. **Coverage identity.** `snapshot lines + skip lines == tokens[].length` on
   every fixture, including one where half the coins are degraded.
6. **Degraded inputs, one case each:** empty `analysis_data`, missing `btc`
   block, `error:true` coin, `count:0`, empty book, coeffs older than
   `STALE_CRIT_MIN`, a `coeffs.json` missing every field added since 08.08
   (inv. 9 — the writer must survive an old bot exactly as the frontend does),
   truncated JSON, HTTP 400 from the ticker endpoint with the kline fallback
   taking over.
7. **Schema conformance.** Every line: required keys present, no `undefined`,
   no `NaN`, every numeric finite or `null`, `k` ∈ the allowed set, `d` parses
   as a date.
8. **Outcome correctness.** Synthetic kline paths with constructed touches:
   first-touch hours are exactly the constructed ones for `tgt`, `stop` and
   `wait`, on both sides; a path touching both levels inside one candle yields
   `first:"tie"`; a path touching neither yields all `null`.
9. **No look-ahead.** The resolver over klines truncated at `d + h` produces a
   byte-identical file to the resolver over the full series — the same control
   `backtest_bench.py` already applies to its own record builder.
10. **Fail-closed.** Zero comparisons performed → the bench **fails**, and it
    prints the number of checks it actually ran (inv. 22, 29: a validator that
    passes on no data is the third way of lying green).

Also required, and stated in the report with their outputs:

- `node --check` on `journal/write.js` and `bench/journal_bench.js`;
- `node bench/fresh_bench.js` and every pre-existing bench in `bench.yml`, all
  green, with check counts — this TZ must not move a single existing number;
- `git diff --stat origin/main -- index.html main.py` → **empty**;
- `node journal/write.js --probe` and `--dry-run` against the **live** Gist from
  your environment, with the resulting record line pasted verbatim into the
  report. State explicitly that the probe was run outside GitHub Actions, so
  inv. 24 remains unverified for this workflow until the first scheduled run.

## 10. Report

`CryptoReports/TZ-05-journal-report.md`, committed directly to `main`, path
stated in your closing message in Russian. Contents: the six fingerprint anchors
with their measured values · line counts and `sha256` of `index.html`,
`main.py`, the System Map · every file added or edited with its diff stat · all
bench outputs with check counts · the probe result naming which price path is
live · one full snapshot record line and one full outcome record line from the
dry run · pull-request number and CI status · anything you found and did not
change.

## 11. Out of scope — do not implement, do not propose inside this TZ

`catalysts.json` (that is the next step, and it is gated on this one) · any
change to `scoreCandidate`, weights, thresholds or constants · any display of
journal data · any statistical analysis of the collected records · Open
Interest (closed permanently, §8) · adding coins · touching the bot's schedule
or the Boss's Shortcuts automation.
