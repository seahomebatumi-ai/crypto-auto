# TZ-50 — the agreement table becomes a two-level map, and a failed artifact write leaves no file

**Canonical filename: `TZ-50-agree-map-and-artifact-write.md`.** Commit the file under this
name, in `CryptoTZ/`, whatever name it arrived under (contract §3).

**This TZ corrects `TZ-49-raw-json-and-prod-pin.md`, which was BLOCKED.** The block was
upheld: §4.1's record shape and §5 item 5 could not both hold. TZ-49 is superseded whole —
implement from this file alone, and do not read a clause from it into here.

**Model: Opus.** Three files, a serialisation shape, a workflow step order and a gate
assertion whose expected set is written here.

---

## 0. Fingerprint gate — blocking, before any work

**Required System Map revision: `**Revision 2026-09-16-b.**`**

Anchors, quoted in full from the map's `## 0` anchor table — the list is cut from that
table's own rows, never from the names below (contract §5 step 2):

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-09-16-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `71. **A measurement that is not RETAINED was not taken,` |

The map's file table, quoted in full:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this gate adds, because this TZ edits all three. **Every pair below was measured by
the Architect on the file itself, not carried from a report:**

| File | Lines | MD5 |
|---|---:|---|
| `bench/backtest_bench.py` | 5795 | `ed4db7c2bab9076e92982c664c6fc2f6` |
| `bench/backtest_guard_bench.py` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` |
| `.github/workflows/backtest_bench.yml` | 171 | `703330829c377a15fc0df71e25df92a7` |

**Known map lag, reported and not acted on (contract §5).** The map's `## 0` prose still
gives `bench/backtest_bench.py` as **5102 / `ba633202f43845ba0fdafbc1b92d9c04`**, the
pre-TZ-48 pair. Revision `2026-09-16-b` predates the merge of pull request #40. The map
revision that clears it is the Architect's and is pending. Record the difference under
`## Pre-existing Issues` and proceed — the enforced figure is the table above.

Every line number in this TZ is read from `bench/backtest_bench.py` at
`ed4db7c2bab9076e92982c664c6fc2f6`.

---

## 1. Why

On a dispatch of `backtest_bench.yml` with `regime_gate: true`:

- `regime_gate_summary` stores the two-annotator agreement in a dict keyed by
  `(word, word)` tuples (`_rg_agree`, `:4050`), so `json.dump` raises `TypeError` and
  `regime_gate_raw.json` has never been written. The step then exits non-zero under
  `bash -euo pipefail`, and the four steps after it carry no `if:` and are skipped —
  `--res7`, `--funding`, `Прогон` and `Сверка`. One measurement failing costs four
  unrelated readings.
- The failed dump leaves a truncated file behind and the artifact uploads it. On `main`
  that is 36 735 bytes ending `… "agree": {`. A partial JSON in an artifact reads as
  data, which is why this survived unobserved (inv. 70).
- TZ-48's `own` field landed inside `prod` (`:3341`), where the guard's check 33 does not
  reach: that check pins the driver answer's **top-level** key set, and check 43 tests
  `prod` only as a superset. TZ-36 was the first field to take that path and TZ-48 the
  second. On every push the answer's shape is pinned one level short of where fields are
  being added.

---

## 2. Scope sentence

This TZ makes the `--regime-gate` artifact writable, makes a failed artifact write leave
no file at that path, returns the driver's answer to a push-time pin, and moves the
regime-gate step out of the path of four unrelated readings. **It adds no formula, no
threshold, no quorum and no bar, and it moves exactly one printed figure**, named in §5
item 5. Anything beyond that is out of scope.

---

## 3. Scope — the complete authorisation

**Files to Modify**

- `bench/backtest_bench.py`
- `bench/backtest_guard_bench.py`
- `.github/workflows/backtest_bench.yml`

**Files to Create** — none besides the report.
**Files to Delete** — none.

Class: branch TZ. `index.html`, `main.py`, `catalysts.json`, every other bench and every
other workflow stay out of the diff.

---

## 4. Implementation

### 4.1 The agreement table becomes a two-level map

`sm["agree"]` becomes a nested map, **`{marketRegime word: {btc_regimes word: count}}`**,
built sorted at both levels so the artifact is deterministic. The unmarked-date literal
stays exactly as it is.

**Its readers, all four, read from the file at the pair in §0:**

| Site | Line | What it does |
|---|---:|---|
| `_rg_agree` | `:4050` | builds the table |
| `regime_gate_summary` | `:4167` | assigns `out["agree"], out["agree_dates"]` |
| `report_regime_gate` | `:4309` | `for (w1, w2), n in sorted(sm["agree"].items())` — becomes a two-level walk |
| `_out_diff` → `_out_fields` | `:5065`, `:4793` | lab section E control E3 reaches every leaf of the whole summary |

The fourth is why TZ-49 was blocked, and it decides the shape. `_out_fields` (`:4793`)
turns each dict key into a path segment and returns one leaf per scalar:

- a tuple key gives the path `('agree', "('range', 'trend')")` — **one leaf per pair**;
- a two-level map gives `('agree', "'range'", "'trend'")` — **one leaf per pair**;
- a record carrying three scalars gives three paths — **three leaves per pair**, which
  moves E3's field count and section E's comparison total by 2 per record.

A two-level map therefore leaves every count where it is. **Do not use a list of
records** (three leaves) and **do not join the pair into a delimited string** — the words
are free text from two sources and a delimiter is a parse waiting to be wrong. Do not
convert the shape at the write site either: a converter at the boundary would silently
launder any future unserialisable key, which is the class this TZ repairs.

`report_regime_gate` prints the **same table, in the same order, with the same text.** Its
output is byte-identical before and after, and that is a validation item.

Detection is unchanged: under both shapes a changed word appears through
`_out_diff`'s `missing` and `added`, never as a silent pass.

`agree_dates` is untouched.

### 4.2 One artifact write, and a failure that leaves nothing

Add one module-level helper — name it `_dump_raw` — taking the object and the artifact's
file name. It must, in this order:

1. serialise with `json.dumps` **before touching the filesystem**;
2. on success, write to a temporary path in the same directory and `os.replace` it onto
   the target, so no reader ever sees a half-written file;
3. **on failure, remove any existing file at the target path, then re-raise.**

Step 3 is the point, and it is what TZ-49 got wrong. Truncate-then-serialise left an
unparseable stub; serialise-then-write would leave the **previous run's complete
artifact** in place, and a stale complete file reads as the new one more convincingly than
a stub does. Either way the reader is told something false. After this change the path
carries this run's artifact or nothing.

Route all six artifact JSON writes through it:

| Artifact | Line |
|---|---:|
| `regimes.json` | `:723` |
| `stops_raw.json` | `:5626` |
| `target_raw.json` | `:5671` |
| `regime_gate_raw.json` | `:5720` |
| `res7_dates.json` | `:5745` |
| `run_raw.json` | `:5789` |

**Four writes stay untouched:** `JsScorer.score` (`:217`) and `JsBridge` (`:2726`), both
hot-path bridge job files carrying `allow_nan=False`, and the two cache writes (`:938`,
`:3113`), which carry no such flag. None is an artifact.

Exit behaviour is unchanged: serialisation still raises and the step still exits non-zero.

**NaN stays bare.** `json.dumps` writes `NaN` by default and Python reads it back.
Section D's world produces 27 such tokens, and `target_raw.json` already carries the same
class. Do **not** add `allow_nan=False`, which would make the artifact unwritable again,
and do **not** map NaN to `null`, which would move two artifacts this TZ does not touch.
A strict third-party reader refusing the file is a known property, recorded in the map,
not a defect to fix here.

### 4.3 The driver's answer returns under a push-time pin

In `bench/backtest_guard_bench.py`, at check 33 — which already holds `r_no` and already
asserts the top-level key set — add **one** assertion, numbered 33, pinning the key set of
`prod` on the same no-grid answer:

```
['anchor', 'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt', 'waiting']
```

**Derivation:** these are the nine keys of the `prod` literal in `TARGET_DRIVER`, read by
the Architect at `:3334`–`:3343` in the file at the pair in §0, sorted by `sorted()`. The
literal's own comment states why `own` sits there.

Give the assertion its neighbours' `info` discipline: on failure it reports the key list
it actually read.

**If the driver's `prod` does not carry exactly those nine, do not adjust the expected
list.** Report BLOCKED, name the list you read, and stop — an expected set edited to match
what it found asserts nothing (hard floor item 2).

Nothing else in the guard moves: no check renumbered, no section relabelled, and check
43's superset test untouched. A superset assertion and an exact-set assertion answer
different questions and both are wanted.

### 4.4 The regime-gate step leaves the middle of the chain

In `.github/workflows/backtest_bench.yml`, move the `Ворота режима на архиве
(--regime-gate)` step so it runs **after** `Деление по режиму BTC` and immediately before
the artifact upload, and change its condition to:

```yaml
if: ${{ inputs.regime_gate && !cancelled() }}
```

Both properties are required, and the second is why the condition changes with the move:

- nothing downstream depends on it any more, so its failure — or its timeout, and it is
  the most expensive step in the job — costs no other reading;
- `--verify` returns 1 on every `coverage` / `unexplained` class, so a step placed after
  `Сверка` without `!cancelled()` would be skipped on exactly the runs the reading is most
  wanted. This is the argument the file already makes for `--attrib`.

The step's command, its `tee` target and both artifact paths are unchanged. No other step
moves and no other step's condition changes. Russian comment lines above the moved step
are in the file's own style and are welcome; a YAML parser does not see them.

### 4.5 The reading states its own comparison structure

Under the market word every date belonged to exactly one population, so the two
populations `_rg_below` compares were disjoint. Under the coin word one date contributes
observations to all three populations at once, while the two confidence intervals are
still built as if independent. Positive covariance makes non-overlap harder to reach, so
**`range` strictly below `trend` remains strong evidence, and the thesis holding is weaker
evidence than the same reading under the market word.**

Print that as one sentence in the header of the coin-word section — the section
`report_own_regime` prints, called at `:5071` and after `report_regime_gate` in the mode.
It is a caveat attached to the reading, because the reading is read from an artifact months
after this text.

The lab concatenates that section as `printed(report_own_regime, own_w)[1:]`, so its first
printed line is dropped there but not in the mode. Report **both** the number of lines you
print and the delta the lab measures; they may differ by one and that is the reason.

No number, no verdict word and no threshold changes here.

---

## 5. What must be true after the change — shapes, not figures

The Architect cannot execute production, so these are the shapes the run must exhibit.
Derive the fixtures yourself and report what they gave.

1. `regime_gate_raw.json` is written, parses, and **re-serialises to the file's exact
   text.** Equality is as JSON, not as Python objects: `trunc` and `pop_dates` are keyed by
   int horizons and return as strings, every CI tuple returns as a list, and NaN is unequal
   to itself, so whole-object `==` is false for any non-empty summary and is not the test.
   `sm["agree"]` alone must also compare equal under `==`.
2. The same object on the **pre-fix** module raises `TypeError`. A repair that cannot be
   shown to have had something to repair has not been shown to work (inv. 45).
3. `report_regime_gate`'s printed text is byte-identical before and after.
4. The guard's total rises by **exactly one** — §4.3's assertion — to `checks run: 488`,
   and no other check's result changes.
5. `--lab-selftest` moves in **exactly one figure**: E3's `добавлено раздела слова монеты`,
   by the lines §4.5 prints as the lab measures them. `E сравнений` stays **4254** at three
   seeds and **4562** at ten; E3's `--regime-gate: полей` stays **1649**. Every other lab
   figure, every section's comparison count and the lab verdict are unchanged.
6. On a failed serialisation **no file exists at the artifact's path — including when a
   complete file was there beforehand.**

---

## 6. Controls

1. **The new pin fires.** With `own` removed from §4.3's expected list, the guard reports
   FAIL on that assertion and on nothing else.
2. **The dump control fires, and localises the write.** Revert `_rg_agree` **and**
   `report_regime_gate`'s loop together, in a scratch copy: the write must raise inside
   `_dump_raw` and leave no file, while `--lab-selftest` stays green. Reverting `_rg_agree`
   alone is **not** this control — the printer dies first and the red localises the
   printer, not the serialisation (inv. 68).
3. **The stale-file control.** Write the artifact successfully, then force a serialisation
   failure at the same path in the same directory, and confirm no file remains. This is the
   only control that proves §4.2 step 3, and without it that step is untested.
4. **Negative test on CI** (contract §9). Force a real failure in the working tree,
   confirm the hosted job turns red, revert, confirm `git status --porcelain` is empty.
5. **Extremes of the agreement table:** no dates at all; every date unmarked by the
   labeller; a single pair. Each must serialise, reload and print.

**Written partition for the inverted runs (inv. 68).**

| | Item | Required |
|---|---|---|
| Must turn red | §4.3's pin under a wrong expected list | red |
| Must turn red | §5 item 1's round-trip under the paired revert of control 2 | red, inside `_dump_raw` |
| Must turn red | control 3's second write | no file at the path |
| Must NOT fire | every other guard check, in every inversion | green |
| Must NOT fire | `--lab-selftest` and `--selftest`, in every inversion | green |

---

## 7. Reading items — report only, edit nothing

1. **Are the other five artifact JSONs actually writable?** `target_raw.json` is known to
   be. `stops_raw.json`, `run_raw.json`, `regimes.json` and `res7_dates.json` have never
   been shown to serialise, and the same class of defect would be equally invisible in
   each. Build each summary on a synthetic world the way `main()` builds it, serialise it,
   and report which succeed, which raise and with what. Name the world, and say which of
   the four could carry a NaN or a numpy scalar that your world did not produce. **Do not
   repair anything you find** — it is the next TZ.
2. **What the coin-word section costs.** From the run you already make: the wall time of
   `regime_gate_summary` with the census against the same call without it, and the peak
   resident size of the process. The archive figure is not asked for and is not inferable
   from this; state the local pair and stop.

---

## Touches

`bench/backtest_bench.py` — `_rg_agree`, `regime_gate_summary`'s assignment,
`report_regime_gate`'s agreement loop, the six artifact writes, `report_own_regime`'s
header.
`bench/backtest_guard_bench.py` — one added assertion at check 33.
`.github/workflows/backtest_bench.yml` — one step moved, one condition changed.

Everything else is a defect of this change: any other moved printed figure, any renumbered
check, any edited assertion, any change to `--target`'s or `--selftest`'s output, any edit
to `_out_fields`, `_out_diff` or the lab's comparators.

---

## Validation

Run every item. An item that cannot be run has failed (contract §9).

1. `python3 -m py_compile bench/backtest_bench.py` and the same on
   `bench/backtest_guard_bench.py` — exit 0 each.
2. The workflow parses: load `.github/workflows/backtest_bench.yml` with a YAML parser and
   print the ordered list of step names with each step's `if:` expression, before and
   after. The diff must be one moved step and one changed condition.
3. `bench/backtest_guard_bench.py` against the changed bench: **`checks run: 488 FAIL 0`**,
   with the delta against 487 attributed to the one added assertion by name.
4. `bench/verify_bench.py`: 59, FAIL 0, output unchanged.
5. `--selftest --seeds 10`: exit 0, stdout byte-identical before and after, comparison
   count stated.
6. `--lab-selftest` at default seeds and at `--lab-seeds 10`: exit 0 both. **Compare
   stdout only, and compare stderr separately** — numpy prints
   `RuntimeWarning: All-NaN slice encountered` twice per lab run, and under `2>&1` it lands
   at buffer-dependent offsets, so a raw merged comparison can differ where the text does
   not. Every differing stdout line is quoted and accounted for by §5 item 5.
7. `regime_gate_summary` on a synthetic world: dump, reload, re-serialise — report bytes,
   the JSON-text equality of §5 item 1, the `==` result for `agree` alone, and the number
   of pairs in the table at both levels.
8. The same on the pre-change module: report the exception and the bytes on disk afterwards
   (§5 item 2).
9. Every control of §6, each reported against the written partition row by row, with the
   tree clean afterwards and the file hashes restored.
10. Hosted `Bench gate` on the implementation commit: run ids, event, conclusion. Read the
    runner's own counts from the log and state the command and the log size; if it answers
    `403`, say so and state that instead.
11. An explicit no-regression statement naming what did not move: `index.html`, `main.py`,
    every other bench, every other workflow, and every printed figure of `--target`,
    `--stops`, `--run` and `--regimes`.

A prototype is not built to discover whether this TZ holds. If a clause cannot hold,
report BLOCKED with the reading that shows it; measure only what the block itself needs.

---

## Commit Message

```
TZ-50: the agreement table becomes a two-level map, a failed artifact write leaves no file, and the driver's answer returns under the push-time gate
```
