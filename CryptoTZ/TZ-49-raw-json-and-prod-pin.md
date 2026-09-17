# TZ-49 — the regime-gate artifact becomes real, and the driver's answer returns under the gate

**Canonical filename: `TZ-49-raw-json-and-prod-pin.md`.** Commit the file under this name,
in `CryptoTZ/`, whatever name it arrived under (contract §3).

**Model: Opus.** Three files, a serialisation shape, a workflow step order and a gate
assertion whose expected set is written here rather than read from the file.

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

Files this gate adds, because this TZ edits all three:

| File | Lines | MD5 | Where the figure comes from |
|---|---:|---|---|
| `bench/backtest_bench.py` | 5795 | `ed4db7c2bab9076e92982c664c6fc2f6` | TZ-48's committed blob at `4a11c8b`, which the merge of pull request #40 carries unchanged |
| `bench/backtest_guard_bench.py` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` | measured by the Architect on the file itself; the map's `## 0` prose states the same pair |
| `.github/workflows/backtest_bench.yml` | 171 | `703330829c377a15fc0df71e25df92a7` | measured by the Architect on the file itself |

**Sequencing.** This TZ runs on a tree that already carries TZ-48. If
`bench/backtest_bench.py` reads **5102 / `ba633202f43845ba0fdafbc1b92d9c04`**, pull
request #40 is not merged: report BLOCKED, name that pair, and stop. Do not implement
against the pre-TZ-48 file — every section below names a structure TZ-48 created.

---

## 1. Why

TZ-48 turned the existing regime grid toward the coin. The reading it produces is taken
on one dispatch of `backtest_bench.yml` with `regime_gate: true`, and that dispatch
cannot currently deliver it:

- `regime_gate_summary` stores the two-annotator agreement in a dict keyed by
  `(word, word)` tuples, so `json.dump` raises `TypeError` and `regime_gate_raw.json`
  has never been writable. The step then exits non-zero under `bash -euo pipefail`, and
  the four steps that follow it carry no `if:` and are skipped — `--res7`, `--funding`,
  `Прогон` and `Сверка`. One measurement failing costs four unrelated readings.
- The failed dump leaves a truncated file behind, and the artifact uploads it. A partial
  JSON in an artifact reads as data, which is why this survived four map revisions
  unobserved (inv. 70).
- TZ-48's field landed inside `prod`, where the guard's check 33 does not reach: that
  check pins the driver answer's **top-level** key set, and check 43 tests `prod` only as
  a superset. TZ-36 was the first field to use that path and TZ-48 the second. The
  identity evidence for the new field is real but lives in `--lab-selftest` section E,
  which runs only on a dispatch (inv. 62). On every push, the shape of the driver's
  answer is now pinned one level short of where fields are actually being added.

---

## 2. Scope sentence

This TZ makes the `--regime-gate` artifact writable, makes a failed artifact write leave
no file instead of a truncated one, returns the driver's answer to a push-time pin, and
moves the regime-gate step out of the path of four unrelated readings. **It adds no
formula, no threshold, no quorum and no bar, and it moves no printed figure.** Anything
beyond that is out of scope.

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

### 4.1 The agreement table becomes JSON-safe

`_rg_agree` accumulates into a dict keyed by `(w1, w2)` and returns it as `sm["agree"]`.
It has exactly two readers in the repository: the assignment in `regime_gate_summary` and
the loop in `report_regime_gate` that unpacks `for (w1, w2), n in sorted(sm["agree"].items())`.

Return a **list of records** instead, sorted once at build time:

- each record carries the `marketRegime` word, the `btc_regimes` word (or the existing
  literal for a date the labeller did not mark) and the count;
- the list is sorted at build time, so the artifact is deterministic and the printer does
  no sorting of its own;
- `report_regime_gate` iterates the records and prints the **same table, in the same
  order, with the same text.** Its output is byte-identical before and after, and that is
  a validation item, not an aspiration.

Do not encode the pair into a delimited string. The words are free text from two sources
and a delimiter is a parse waiting to be wrong; a record needs no parse.

`agree_dates` is unchanged.

### 4.2 One artifact write, serialised before the file exists

Add one module-level helper — name it `_dump_raw` — that takes the object and the
artifact's file name, serialises with `json.dumps` **first**, and only then opens the
file and writes the string, under `with`.

Route every artifact JSON write through it. In the file as it stands before this TZ the
sites are `regimes.json`, `stops_raw.json`, `target_raw.json`, `regime_gate_raw.json`,
`res7_dates.json` and `run_raw.json` — six `json.dump(obj, open(...))` calls. Report the
count you found; if it is not six, name each site you changed and each you did not.

**Do not touch the two `JsBridge` job writes or the cache writes.** They are hot-path,
they carry `allow_nan=False`, and they are not artifacts.

Behaviour on failure is unchanged: serialisation still raises, the step still exits
non-zero. What changes is that the failure leaves **no file** rather than a plausible one.

### 4.3 The driver's answer returns under a push-time pin

In `bench/backtest_guard_bench.py`, at check 33 — which already holds `r_no` and already
asserts the top-level key set — add **one** assertion, numbered 33, pinning the key set of
`prod` on the same no-grid answer:

```
['anchor', 'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt', 'waiting']
```

**Derivation of that set, since a bar nobody derived is a bar nobody may register
(inv. 61):** the first eight are the keys of the `prod` literal in `TARGET_DRIVER`, read
by the Architect in `bench/backtest_bench.py` at `ba633202f43845ba0fdafbc1b92d9c04`. The
ninth, `own`, is TZ-48's field, and that it sits inside `prod` is established without
reading the merged file: the module raises at import unless the field line occurs exactly
once (`TGT_OWN_JS`), check 33 reads green on two hosted runners so the field is not
top-level, and check 33's first two assertions hold `subs` empty on this path.

Give the assertion the same `info` discipline as its neighbours: on failure it reports the
key list it actually read.

**If the merged driver's `prod` does not carry exactly those nine, do not adjust the
expected list.** Report BLOCKED, name the list you read, and stop — an expected set edited
to match what it found asserts nothing (hard floor item 2).

Nothing else in the guard moves. Do not renumber a check, do not relabel a section, and
do not touch check 43's superset test: a superset assertion and an exact-set assertion
answer different questions and both are wanted.

### 4.4 The regime-gate step leaves the middle of the chain

In `.github/workflows/backtest_bench.yml`, move the `Ворота режима на архиве
(--regime-gate)` step so it runs **after** `Деление по режиму BTC` and immediately before
the artifact upload, and change its condition to:

```yaml
if: ${{ inputs.regime_gate && !cancelled() }}
```

Two properties, both required, and the second is why the condition changes with the move:

- nothing downstream depends on it any more, so its failure — or its timeout, and it is
  the most expensive step in the job — costs no other reading;
- `--verify` returns 1 on every `coverage` / `unexplained` class, so a step placed after
  `Сверка` without `!cancelled()` would be skipped on exactly the runs the reading is
  most wanted. This is the argument the file already makes for `--attrib` at its own
  step, and the same one applies here.

The step's own command, its `tee` target and both artifact paths are unchanged. No other
step moves, and no other step's condition changes.

### 4.5 The reading states its own comparison structure

Under the market word every date belonged to exactly one population, so the two
populations compared by `_rg_below` were disjoint. Under the coin word a single date
contributes observations to all three populations at once, while the two confidence
intervals are still built as if independent. Positive covariance makes non-overlap harder
to reach, so **`range` strictly below `trend` remains strong evidence, and the thesis
holding is weaker evidence than the same reading under the market word.**

Print that as **one sentence** in the header of the coin-word section — the section
TZ-48 added, printed before the dump. It is a caveat attached to the reading, because the
reading is read from an artifact months after this text. Report the exact site you placed
it at.

No number, no verdict word and no threshold changes here.

---

## 5. What must be true after the change — shapes, not figures

The Architect cannot execute production, so these are stated as the shapes the run must
exhibit. Derive the fixtures yourself and report what they gave.

1. `regime_gate_raw.json` is written, parses, and round-trips: the object loaded back
   from the file equals the object that was dumped, the agreement records included.
2. The same object on the **pre-fix** module raises `TypeError`. A repair that cannot be
   shown to have had something to repair has not been shown to work (inv. 45).
3. `report_regime_gate`'s printed text is byte-identical before and after.
4. The guard's total rises by **exactly one** — the assertion of §4.3 — and no other
   check's result changes.
5. `--lab-selftest` moves in exactly one figure: the count of lines the coin-word section
   adds, by the number of lines §4.5 prints. Every other lab figure, every section's
   comparison count and the lab verdict are unchanged.
6. On a failed serialisation no file exists at the artifact's path.

---

## 6. Controls

1. **The new pin fires.** With `own` removed from the expected list of §4.3, the guard
   must report FAIL on that assertion and on nothing else.
2. **The dump control fires.** With `_rg_agree` returning its pre-TZ-49 tuple-keyed dict
   in a scratch copy, the round-trip of §5 item 1 must raise, and `--lab-selftest` must
   stay green — the lab never dumps, and a control that goes red everywhere has localised
   nothing (inv. 68).
3. **Negative test on CI** (contract §9). Force a real failure in the working tree,
   confirm the hosted job turns red, revert, confirm `git status --porcelain` is empty.
4. **Extremes of the agreement table:** no dates at all; every date unmarked by the
   labeller; a single pair. Each must serialise and print.

**Written partition for the inverted runs (inv. 68).**

| | Item | Required |
|---|---|---|
| Must turn red | the §4.3 pin under a wrong expected list | red |
| Must turn red | the §5 item 1 round-trip under tuple keys | red |
| Must NOT fire | every other guard check, in both inversions | green |
| Must NOT fire | `--lab-selftest` and `--selftest`, in both inversions | green |

---

## 7. Reading items — report only, edit nothing

1. **Are the other five artifact JSONs actually writable?** `target_raw.json` is known to
   be: TZ-48's identity probe wrote 9067 bytes on both modules. `stops_raw.json`,
   `run_raw.json`, `regimes.json` and `res7_dates.json` have never been shown to
   serialise, and the same class of defect would be equally invisible in each. Build each
   summary on a synthetic world the way `main()` builds it, serialise it, and report which
   succeed, which raise and with what. **Do not repair anything you find** — it is the
   next TZ.
2. **What the coin-word section costs on the archive.** From the run you already make:
   the wall time of `regime_gate_summary` with the census against the same call without
   it, and the peak resident size of the process. The archive figure is not asked for and
   is not inferable from this; state the local pair and stop.

---

## Touches

`bench/backtest_bench.py` — `_rg_agree`, `report_regime_gate`, the six artifact writes,
the coin-word section header.
`bench/backtest_guard_bench.py` — one added assertion at check 33.
`.github/workflows/backtest_bench.yml` — one step moved, one condition changed.

Everything else is a defect of this change: any moved printed figure, any renumbered
check, any edited assertion, any change to `--target`'s or `--selftest`'s output.

---

## Validation

Run every item. An item that cannot be run has failed (contract §9).

1. `python3 -m py_compile bench/backtest_bench.py` and the same on
   `bench/backtest_guard_bench.py` — exit 0 each.
2. The workflow parses: load `.github/workflows/backtest_bench.yml` with a YAML parser and
   print the ordered list of step names with each step's `if:` expression, before and
   after. The diff must be one moved step and one changed condition.
3. `bench/backtest_guard_bench.py` against the changed bench: **`checks run: 488 FAIL 0`**,
   and the delta against 487 attributed to the one added assertion by name.
4. `bench/verify_bench.py`: 59, FAIL 0, output byte-identical to before.
5. `--selftest --seeds 10`: exit 0, output byte-identical before and after, with the
   comparison count stated.
6. `--lab-selftest` at default seeds and at `--lab-seeds 10`: exit 0 both, section E's
   comparison count unchanged at both, and the full output diffed against the pre-change
   run. Every differing line is quoted and accounted for by §5 item 5.
7. `regime_gate_summary` on a synthetic world: dump, reload, compare — report bytes, the
   round-trip result and the number of agreement records.
8. The same on the pre-change module: report the exception and the bytes on disk
   afterwards (§5 item 2).
9. Both inversions of §6, each reported against the written partition row by row, with the
   tree clean afterwards and the file hashes restored.
10. The CI negative test of contract §9: the forced failure, the red job, the revert, the
    clean tree.
11. Hosted `Bench gate` on the implementation commit: run ids, event, conclusion. Read the
    runner's own counts from the log and state the command and the log size — TZ-48's
    session read both logs in full, which is a measurement inv. 44 does not currently
    allow for; if it answers `403` this time, say so and state that instead.
12. An explicit no-regression statement naming what did not move: `index.html`, `main.py`,
    every other bench, every other workflow, and every printed figure of `--target`,
    `--stops`, `--run` and `--regimes`.

---

## Commit Message

```
TZ-49: the regime-gate artifact becomes writable, and the driver's answer returns under the push-time gate
```
