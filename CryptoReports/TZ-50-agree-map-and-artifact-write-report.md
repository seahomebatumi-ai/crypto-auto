# Implementation Report — TZ-50

**Previous TZ state, checked before any work (contract §8).** TZ-49 was BLOCKED (report
`8d0badb` on `main`) and opened no branch. TZ-48's branch was merged as pull request #40 (merge
commit `074c423`). This implementation is built on `origin/main` at `728129a`, the Boss's upload of
this specification. That upload is the only commit after TZ-49's report.

## Status

**COMPLETED.**

- Every validation item was run, and every control matched its written partition.
- The hosted `Bench gate` concluded `success` on the implementation commit, both push and pull
  request, with the runner's own counts `488 / FAIL 0` and `59 / FAIL 0`.
- The hosted negative test turned the gate red at the guard step alone.

## Inbound Filing

None. The specification arrived at its canonical path,
`CryptoTZ/TZ-50-agree-map-and-artifact-write.md`, in `728129a` (381 lines,
`12431c2e1a23d261e0ed363abf77f1f6`). `git ls-tree -r origin/main --name-only | grep -i "TZ-50"`
returns that one path, and the repository root holds no copy.

## Scope Executed

**Class: branch TZ** (contract §8). `## Scope` names three files outside `CryptoReports/**`.

| TZ clause | Executed |
|---|---|
| §4.1 agreement table → two-level map | yes: `_rg_agree`, and `report_regime_gate`'s loop walks two levels |
| §4.2 `_dump_raw`, six artifact writes | yes; the four non-artifact writes are untouched |
| §4.3 guard pin on `prod` at check 33 | yes; one assertion |
| §4.4 regime-gate step moved, condition changed | yes |
| §4.5 caveat sentence in the coin-word header | yes |
| §5 items 1–6 | all hold (Validation) |
| §6 controls 1–5 | all run against the written partition (Validation 9) |
| §7 reading items 1–2 | reported; nothing edited |

## Files Created

- `CryptoReports/TZ-50-agree-map-and-artifact-write-report.md` (this report, direct to `main`).

## Files Modified

| File | Before (lines / MD5) | After (lines / MD5) | `-U0` hunks | +/− |
|---|---|---|---:|---|
| `bench/backtest_bench.py` | 5795 / `ed4db7c2bab9076e92982c664c6fc2f6` | 5830 / `a1b1ce27773332e5630bba4189bd4d69` | 11 | +49 / −14 |
| `bench/backtest_guard_bench.py` | 2503 / `bfc984b1d22ec1ad89cf536a1a47c529` | 2513 / `622b844efcca4292df2a157680ca4324` | 1 | +10 / −0 |
| `.github/workflows/backtest_bench.yml` | 171 / `703330829c377a15fc0df71e25df92a7` | 175 / `84efa8826db35837a810e3ad884dfa4b` | 2 | +14 / −10 |

`git diff --name-only 728129a 2ecefc7` names exactly those three files. The `-U0` and default
hunk counts are equal for all three.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

**Where the code came from.** TZ-49's report records its prototype as `/tmp/tz49/proto.diff`,
187 lines, MD5 `19ac76813d064198b92fb4f4180f17b0`. The file was still in the container and
matched that hash. `git apply --check` and then `git apply` succeeded on `728129a`. Only what
TZ-50 amends was then rewritten:

- the record shape became a two-level map;
- `_dump_raw` gained the temporary-file write and the remove-on-failure branch;
- the caveat wording changed;
- the guard comment changed (below);
- every `ТЗ-49` tag became `ТЗ-50`.

Every figure below was measured in this session. None is carried from TZ-49's report.

**§4.1 — `_rg_agree` (`bench/backtest_bench.py:4050`).**
- The loop now fills `cell.setdefault(word, {})[label] += 1`. The unmarked literal
  `w2[0] if w2 else "нет метки"` is kept verbatim.
- It returns `{w1: dict(sorted(cell[w1].items())) for w1 in sorted(cell)}`, so insertion order
  is sorted at both levels.
- `report_regime_gate` now reads `for w1, row in sorted(sm["agree"].items()): for w2, n in
  sorted(row.items()):` with the same format string. Sorting by `w1` and then by `w2` is the
  order that `sorted()` gave over the `(w1, w2)` tuples.
- `regime_gate_summary`'s assignment (`:4167`) needed no edit, because the function still
  returns a pair. `agree_dates` is untouched.

**§4.2 — `_dump_raw(obj, name)`** is module-level and sits just before `main()`. In order, it:
1. calls `json.dumps(obj)` before any filesystem call;
2. writes the text to `HERE/_<name>.<pid>.tmp` (the same directory, covered by `.gitignore`'s
   `bench/_*`), then `os.replace` puts it onto `HERE/<name>`;
3. on failure, removes the temporary file if present, then removes the target if present, then
   re-raises.

```python
def _dump_raw(obj, name):
    path = os.path.join(HERE, name)
    tmp = os.path.join(HERE, "_%s.%d.tmp" % (name, os.getpid()))
    try:
        text = json.dumps(obj)
        with open(tmp, "w") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        for p in (tmp, path):
            if os.path.exists(p):
                os.remove(p)
        raise
```

(The docstring, eight lines, is omitted here.)

All six artifact writes go through it: `regimes.json`, `stops_raw.json`, `target_raw.json`,
`regime_gate_raw.json`, `res7_dates.json` and `run_raw.json`. The two bridge job writes (`:217`,
`:2726`) and the two cache writes (`:938`, `:3113`) are untouched. `allow_nan` is not passed.

**§4.3 — guard, after the existing third check 33 (`bench/backtest_guard_bench.py:893–902`).**

```python
ok('33. and the key set of `prod` on the same answer is exactly the registered one',
   r_no[0] is not None and r_no[1] is not None
   and sorted(r_no[0].get('prod') or {}) == sorted(r_no[1].get('prod') or {})
   == ['anchor', 'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt',
       'waiting'],
   None if not r_no[0] else sorted(r_no[0].get('prod') or {}))
```

- **The expected list was checked before it was written, and it was not adjusted.**
  - I parsed the `prod` literal of `TARGET_DRIVER` at `:3334–3343` on the pristine extract,
    with comments stripped. `sorted()` gave `['anchor', 'anchorDist', 'anchorStop', 'g', 'own',
    'p', 'pA', 'tgt', 'waiting']`, exactly the nine keys in §4.3.
  - The live driver answers the same nine: the post-change guard passes, and control 1's info
    field prints what it read.
- **The prototype's comment was changed.** It justified the written list with «(inv. 61)».
  Inv. 61 says the opposite: a bar is derived from production at run time, never assumed. The
  comment now gives the TZ's reason instead: a set taken from the thing it checks asserts
  nothing.
- No other check was renumbered, relabelled or edited, and check 43 is untouched.

**§4.4 — workflow.**
- The `Ворота режима на архиве (--regime-gate)` step moved from position 12 to 18, after
  `Деление по режиму BTC` and immediately before `actions/upload-artifact@v4`.
- Its condition is now `${{ inputs.regime_gate && !cancelled() }}`.
- Its `run` block, `tee` target and both upload paths are unchanged.
- It carries its three original `ТЗ-32` comment lines, plus four Russian `ТЗ-50` lines giving the
  two reasons from §4.4.

**§4.5 — caveat.** One sentence, printed as four lines right after the existing «Популяция —
подмножество НАБЛЮДЕНИЙ…» paragraph in `report_own_regime`'s header:

```
ОГОВОРКА: одна дата может класть наблюдения сразу во все три популяции,
а два ДИ95 строятся как независимые; положительная ковариация мешает им
разойтись, поэтому `range` строго ниже `trend` — по-прежнему сильное
свидетельство, а «тезис устоял» — слабее того же чтения под словом рынка.
```

**The change, `git diff -U0 728129a 2ecefc7 -- bench/backtest_bench.py`, hunks 1–5 of 11.**
Hunks 6–11 are `_dump_raw` (quoted in §4.2 above) and the five one-line `json.dump` →
`_dump_raw` swaps in `main()`:

```diff
@@ -723,2 +723 @@ def run_regimes(html, bot, horizon=7, step=7):
-    json.dump([{"t": x["t"], "reg": x["reg"]} for x in d],
-              open(os.path.join(HERE, "regimes.json"), "w"))
+    _dump_raw([{"t": x["t"], "reg": x["reg"]} for x in d], "regimes.json")
@@ -4065,3 +4070,5 @@ def _rg_agree(by_H, btc):
-            cell[(_rg_word(d), w2[0] if w2 else "нет метки")] = \
-                cell.get((_rg_word(d), w2[0] if w2 else "нет метки"), 0) + 1
-    return cell, len(seen)
+            row = cell.setdefault(_rg_word(d), {})
+            row[w2[0] if w2 else "нет метки"] = \
+                row.get(w2[0] if w2 else "нет метки", 0) + 1
+    return ({w1: dict(sorted(cell[w1].items())) for w1 in sorted(cell)},
+            len(seen))
@@ -4309,2 +4316,3 @@ def report_regime_gate(sm):
-    for (w1, w2), n in sorted(sm["agree"].items()):
-        print("  %-8s × %-10s %d" % (w1, w2, n))
+    for w1, row in sorted(sm["agree"].items()):
+        for w2, n in sorted(row.items()):
+            print("  %-8s × %-10s %d" % (w1, w2, n))
```

The other two hunks in that range are the `_rg_agree` docstring paragraph (`@@ -4055`) and the
caveat print (`@@ -4490,0`).

## Validation

Every run was serial (one bench at a time). **Pristine** means a `git archive origin/main`
extract at `/tmp/tz50/origin`. **Post** means the working tree at `2ecefc7`. Offline `main()` modes
ran through `/tmp/tz50/h/harness.py`, which imports the module from a scratch directory and
replaces exactly one function, `reconcile`, which fetches the live gist. The stub returns every
cached symbol as `clean`. The world is **section D's: `synth_hl("normal")`, 16 documents, first
coin `C00` written as `BTC`**. Each side's cache was built by its own module's generator, and the
two `md5sum` lists are identical (16 files).

### 1. `py_compile`

`python3 -m py_compile bench/backtest_bench.py` → exit 0.
`python3 -m py_compile bench/backtest_guard_bench.py` → exit 0.

### 2. The workflow parses: steps and `if:` before and after (PyYAML 6.0.1)

| # | Before | `if:` | After | `if:` |
|---:|---|---|---|---|
| 1–11 | checkout … `--target` | — | identical | — |
| 12 | **Ворота режима на архиве (--regime-gate)** | `${{ inputs.regime_gate }}` | Фактор res7 | — |
| 13 | Фактор res7 | — | Фактор funding | — |
| 14 | Фактор funding | — | Прогон | — |
| 15 | Прогон | — | Сверка восстановления с живым coeffs.json | — |
| 16 | Сверка восстановления с живым coeffs.json | — | Разложение расхождения доходностей (--attrib) | `${{ !cancelled() }}` |
| 17 | Разложение расхождения доходностей (--attrib) | `${{ !cancelled() }}` | Деление по режиму BTC | `${{ !cancelled() }}` |
| 18 | Деление по режиму BTC | `${{ !cancelled() }}` | **Ворота режима на архиве (--regime-gate)** | `${{ inputs.regime_gate && !cancelled() }}` |
| 19 | actions/upload-artifact@v4 | `always()` | actions/upload-artifact@v4 | `always()` |

A structural comparison of the two parsed files gave:
- same step multiset (19 = 19);
- the other 18 steps in identical order;
- field changes across all steps: exactly one, `if` on the moved step;
- `on`, `name` and every job key other than `steps` identical.

**One moved step and one changed condition.**

### 3. Guard against the changed bench

`python3 bench/backtest_guard_bench.py` → exit 0, **`checks run: 488   FAIL 0`**. Pristine gives
`487   FAIL 0`. The two outputs differ in that one line only (`diff`); sections E–K print the same
counts.

**Attribution by name.** Both guards ran through a wrapper that records every `ok()` call
(`guard_names.py`):
- pre: 487 calls; post: 488 calls; 0 failures on either side;
- names added: `{'33. and the key set of `prod` on the same answer is exactly the registered
  one': 1}`; names removed: `{}`;
- the first divergence is call **#143**, the new pin (result `True`), directly after
  `33. and the untouched keys of the answer are unchanged`;
- `pre[142:] == post[143:]` and `pre[:142] == post[:142]` are both `True`, so every other check
  keeps its name, position and result.

### 4. `bench/verify_bench.py`

Exit 0, `checks run: 59   FAIL 0`. The output is identical to pristine, MD5
`4dff115f3f0595d2fe74d99cf4052422` on both sides.

### 5. `--selftest --seeds 10`

Command from `bench/`: `python3 backtest_bench.py --selftest --seeds 10 --html ../index.html
--bot ../main.py`.

| | Exit | Seconds | stdout lines / MD5 | stderr bytes |
|---|---:|---:|---|---:|
| pristine | 0 | 93 | 30 / `888b31de3f1f77380b23e179bca32c2a` | 0 |
| post | 0 | 91 | 30 / `888b31de3f1f77380b23e179bca32c2a` | 0 |

`cmp` confirms the stdout is byte-identical. **Comparison count.** The mode prints no total. The
comparisons it does print are:
- closure of `_score_bridge.js`: 45 lookups over 11 names, 0 missing;
- T1, T2 and T3: three checks;
- three worlds × 10 seeds of sign agreement (10/10, 10/10, 10/10);
- the two verdict conditions (`ДА`, `ДА`).

The byte comparison itself covered 30 of 30 lines, with 0 differing.

### 6. `--lab-selftest`, 3 seeds and `--lab-seeds 10` (stdout and stderr compared separately)

| | Exit | Seconds | stdout lines / MD5 | stderr MD5 | `E сравнений` | Verdict |
|---|---:|---:|---|---|---:|---|
| pristine, 3 seeds | 0 | 371 | 129 / `9b957785bff958308e38aac406b7a108` | `279a86e61b7a0af798e59c599764bdac` | 4254, 0 | измеряет то, что должна |
| post, 3 seeds | 0 | 351 | 129 / `be87f87e870237265b4856755ad25929` | `279a86e61b7a0af798e59c599764bdac` | 4254, 0 | измеряет то, что должна |
| pristine, 10 seeds | 0 | 544 | 227 / `781619a9b0b544e61ce454cc5e060964` | `279a86e61b7a0af798e59c599764bdac` | 4562, 0 | измеряет то, что должна |
| post, 10 seeds | 0 | 551 | 227 / `1c09d5b07645228677fc202e702bc4c9` | `279a86e61b7a0af798e59c599764bdac` | 4562, 0 | измеряет то, что должна |

- **stderr** is identical on all four runs: the two NumPy `RuntimeWarning: All-NaN slice
  encountered` pairs and nothing else.
- **stdout, `diff pristine post`, 3 seeds.** Exactly one line differs (line 122):
  ```
  <      --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 233
  >      --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 237
  ```
- **stdout, 10 seeds.** The same single line differs (line 220), with the same 233 → 237.

This is §5 item 5's licensed move: `добавлено раздела слова монеты` +4. `полей` stays 1649, `E
сравнений` stays 4254 and 4562, and `строк отчёта 250, расхождений 0` does not move. The other
128 lines (3 seeds) and 226 lines (10 seeds) are byte-identical, and they include every figure of
sections A–D, every other E figure and the lab verdict. Peak RSS at 3 seeds was 389 096 KB
pristine and 398 652 KB post (`/usr/bin/time -v`).

**The lines printed against the lab's delta (§4.5).** On section D's world (`e3_attrib.py`, the
lab's own construction):

| | `report_own_regime` newlines printed (mode) | `split('\n')` elements | Lab `[1:]` elements | Lab `добавлено раздела` |
|---|---:|---:|---:|---:|
| pristine | 233 | 234 | 233 | 233 |
| post | 237 | 238 | 237 | 237 |

- **In the mode**, `report_own_regime` prints four more lines. Its section is 237 lines, and the
  first of them is the blank line produced by `"\n" + "═" * 62`.
- **The lab drops that first element** (`[1:]`). The trailing empty element that `split` leaves
  after the final newline cancels the drop. So on this function the lab's count equals the
  printed line count, and **the delta is +4 in both**.
- The "differ by one" the TZ anticipates is the relation between split elements (238) and the
  lab's count (237).

### 7. `regime_gate_summary` on the synthetic world: dump, reload, re-serialise (post)

`--regime-gate` ran through `main()` (harness) with post `bench/backtest_bench.py`:
- exit 0, wall 108.6 s;
- `regime_gate_raw.json` **written**: 37 140 bytes, MD5 `194acec01eec5b3c67aa7a7991fb1628`;
- **parses**; no temporary file left;
- 27 bare `NaN` tokens and no other non-finite token.

| Check | Result |
|---|---|
| `json.dumps(json.loads(file)) == file text` (§5 item 1) | **True** |
| `json.dumps(sm) == file text` (the object handed to the write) | **True** |
| `json.loads(file)["agree"] == sm["agree"]` | **True** |
| `json.loads(file) == sm` (whole object) | False, as §5 item 1 anticipates: `int`→`str` keys ×2 (`trunc`, `pop_dates`), NaN ≠ NaN ×27, tuple→list ×96 |
| level 1 (marketRegime words) | 3, sorted: `range`, `stress`, `trend` |
| level 2 (pairs) | 6, each row sorted |
| `agree_dates` | 83 |

`agree` as written: `{"range": {"диапазон": 33, "тренд": 1}, "stress": {"диапазон": 3, "тренд":
1}, "trend": {"диапазон": 44, "тренд": 1}}`.

**Printed text (§5 item 3).**
- The mode's stdout up to the coin-word header is byte-identical pre and post: 15 572 characters, MD5
  `b12ebb63308835ba9431bb75167ffa69`.
- `report_regime_gate` on section D's world is also identical (`e3_attrib.py`), MD5
  `64fed52a642d9dfce630556ab88ea93e`, 250 elements.
- It prints identically on all four extreme worlds as well (item 9, control 5).
- The mode's full stdout pre versus post differs in exactly two places: the four caveat lines
  after line 276, and the pre-change traceback (15 lines) at the end.

### 8. The same on the pre-change module (§5 item 2)

Pristine `bench/backtest_bench.py` on the same cache, through `main()`:
- **`TypeError: keys must be str, int, float, bool or None, not tuple`**;
- traceback frames `main` → `json.dump` → `_iterencode` → `_iterencode_dict` ×2; exit 1;
- **36 735 bytes on disk** afterwards, MD5 `4409608aa3c5ed0c206a27914dc4a89d`, ending
  `, "range": 33, "stress": 4}}, "agree": {`;
- `json.loads` → `JSONDecodeError: Expecting property name enclosed in double quotes: line 1
  column 36736 (char 36735)`;
- the `agree` built there has six tuple keys, including `('trend', 'диапазон')`.

### 9. Controls (§6) against the written partition

The controls ran on scratch copies under `/tmp/tz50`:
- **control 1:** `c1/`, the post bench plus a mutated guard;
- **control 2:** `c2/`, a mutated bench plus the post guard.

Each mutation is an exact-string replacement whose match count is asserted to be 1
(`mutate.py`). Mutated file MD5s: control 1 guard `44e97765e43dac0c06baadca4fc19637`, control 2
bench `bf6a7d0746589703033ba302d7ff65bd`.

**Control 1 — the new pin fires.**
- `own` was removed from §4.3's expected list in the guard copy.
- Guard: exit 1, **`checks run: 488   FAIL 1`**:
  `FAIL: 33. and the key set of `prod` on the same answer is exactly the registered one  [['anchor',
  'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt', 'waiting']]`.
- By name against the post run: 488 calls, the same names in the same order, and **exactly one
  result differs, call #143, `True → False`.**

**Control 2 — `_rg_agree` and `report_regime_gate`'s loop reverted together.**
- The two post hunks were replaced with the pristine text. `diff` against pristine shows only
  `_dump_raw`, the six write swaps, the caveat and the docstring paragraph.
- `--regime-gate` through `main()`, **with no file beforehand**:
  - `TypeError: keys must be str, int, float, bool or None, not tuple`;
  - frames `main` → `_cap_dump` → **`_dump_raw`** → `dumps` → `encode` → `iterencode`
    (`_cap_dump` is the harness's one-line pass-through that records the object; it is not
    repository code);
  - exit 1; **no file at the path**; no temporary file;
  - the printed report before the traceback is byte-identical to the post run's stdout
    (30 074 characters).
- **Seeded run.** The post run's complete 37 140-byte artifact (`194acec0…`, parses) was copied
  to the path first. Same exception, same frames, and afterwards **no file at the path** and no
  temporary file.
- The variant §6 says is not this control, reverting `_rg_agree` alone, raised
  `AttributeError: 'int' object has no attribute 'items'` in frames `main` → `report_regime_gate`
  after 72 s. The printer dies before any write, as §6 predicts.

**Control 3 — the stale-file control** (`extremes.py`, post module, a fresh temporary `HERE`).
- First write: `_dump_raw(sm, "regime_gate_raw.json")` on the single-pair world's summary →
  exists, 2663 bytes, MD5 `547a10e3fec99998540285f95cbcf729`, reloads with `agree ==`; directory
  listing `['regime_gate_raw.json']`.
- Second write at the same path in the same directory: the same summary with
  `agree = {('range', 'trend'): 1}` → `TypeError: keys must be str, int, float, bool or None, not
  tuple`, raised in `_dump_raw` → `dumps` → `encode` → `iterencode`.
- Afterwards: **`exists_after: false`, directory listing `[]`.**

**Control 4 — negative test on CI (contract §9).**
1. On a throwaway branch `claude/tz-50-negative-control` cut from `2ecefc7`, the working-tree
   guard got control 1's mutation (MD5 `44e97765…`, one `-U0` hunk). Local guard: `488   FAIL 1`.
2. Committed as `b7c9350` and pushed. `Bench gate` run
   [35225366648](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/35225366648),
   event `push`, conclusion **`failure`**:
   - steps 1–18 `success`, **step 19 `Гарнизон бэктеста (backtest_guard_bench.py)` `failure`**;
   - the log (`gh run view 35225366648 --log`, 86 511 bytes) reads `checks run: 488   FAIL 1`, the
     same `FAIL: 33. … [['anchor', … 'waiting']]` line and `##[error]Process completed with exit
     code 1.`;
   - step 9's `checks run: 59   FAIL 0` and sections E–K are unchanged.
3. Reverted: I checked out `claude/tz-50-agree-map-and-artifact-write`, ran `git branch -D
   claude/tz-50-negative-control` and `git push origin --delete claude/tz-50-negative-control`.
   `git ls-remote --heads origin claude/tz-50-negative-control` now returns 0 lines.
4. `git status --porcelain` is empty, HEAD is `2ecefc7`, and the three file MD5s are restored
   (`a1b1ce27…`, `622b844e…`, `84efa882…`).

**Control 5 — extremes of the agreement table** (`extremes.py`). Worlds use the guard's check-27
observation fixtures. Each summary goes through `regime_gate_summary`, the module's write and
`report_regime_gate`.

| World | Module | `agree` | Pairs | Write | Reload `agree ==` / text round-trip | Print (MD5 of whole report) |
|---|---|---|---:|---|---|---|
| no dates (`by_H = {}`) | post | `{}` | 0 | ok, 299 B | True / True | ok, `d496cb83…` |
| no dates (every horizon `[]`) | post | `{}` | 0 | ok, 13 962 B | True / True | ok, `05b20176…` |
| every date unmarked (BTC `prices: []`, 12 dates) | post | `{"range": {"нет метки": 6}, "trend": {"нет метки": 6}}` | 2 | ok, 3587 B | True / True | ok, `b10012a1…` |
| single pair | post | `{"range": {"диапазон": 1}}` | 1 | ok, 2663 B | True / True | ok, `e7d996cd…` |
| every date unmarked | pristine | tuple-keyed, 2 | 2 | `TypeError`, 3359 B stub left | `JSONDecodeError` | ok, `b10012a1…` (same) |
| single pair | pristine | tuple-keyed, 1 | 1 | `TypeError`, 2504 B stub left | `JSONDecodeError` | ok, `e7d996cd…` (same) |

Both empty worlds also wrote on the pristine module with identical bytes and print MD5s: an empty
dict serialises. The printed agreement blocks are identical pre and post in all four worlds, for
example `  range    × нет метки  6` / `  trend    × нет метки  6`.

**The written partition, row by row.**

| | Item | Required | Measured |
|---|---|---|---|
| Must turn red | §4.3's pin under a wrong expected list | red | **red**: `488 / FAIL 1`, call #143 only, locally and on runner 35225366648 |
| Must turn red | §5 item 1's round-trip under control 2's paired revert | red, inside `_dump_raw` | **red**: `TypeError` in `_dump_raw` → `dumps`, no file (unseeded and seeded) |
| Must turn red | control 3's second write | no file at the path | **no file**, directory empty |
| Must NOT fire | every other guard check, in every inversion | green | control 1: the other 487 results equal post's; control 2 tree: `488 / FAIL 0`; runner: only step 19 failed, with one FAIL line |
| Must NOT fire | `--lab-selftest` and `--selftest`, in every inversion | green | control 1 and control 2 trees: selftest exit 0, stdout `cmp`-identical to post; lab (3 seeds) exit 0, `E сравнений 4254, отказов 0 ОК`, verdict `измеряет то, что должна`, stdout and stderr `cmp`-identical to post |

Control 3 mutates no file, so it has no guard or lab reading of its own. The post runs in items 3,
5 and 6 are the readings on its tree. Control 4's tree is control 1's guard, read on a runner.

### 10. Hosted `Bench gate` on the implementation commit `2ecefc77838fa68e2dc0c330a18e777650d6dcd7`

See `## CI Execution`: two runs, `push` and `pull_request`, both `success`. The runner's own counts
were read from the logs: `checks run: 59   FAIL 0` and `checks run: 488   FAIL 0`.

### 11. No-regression statement

- **`index.html`, `main.py`, `catalysts.json`, `bench/exhaustion-calibration.txt` did not move.**
  Their line counts and MD5s on `2ecefc7` equal the map's table (`## Fingerprints`), and none
  appears in `git diff --name-only 728129a 2ecefc7`.
- **Every other bench did not move**, for example `bench/verify_bench.py` 540 /
  `28eb1949f21d0afadb062303108f7101`, the map's figure. **Every other workflow did not move**
  (`bench.yml`, `calib.yml`, `journal.yml`, `main.yml`).
- **`--target`, `--stops`, `--run` and `--regimes` did not move.** Through `main()` on the same
  cache, pristine against post:

| Mode (argv) | Exit pre / post | stdout identical | stdout lines | Artifact bytes | Artifact MD5 pre = post |
|---|---|---|---:|---:|---|
| `--stops --horizon 7 --step 7` | 0 / 0 | yes (`8d2200f2…`) | 27 | 2540 | yes, `7a147a3d…` |
| `--run --horizon 3 --step 7` | 0 / 0 | yes (`aca27fe0…`) | 33 | 388 474 | yes, `7c5599cb…` |
| `--run --horizon 7 --step 7` | 0 / 0 | yes (`1f22443f…`) | 33 | 388 645 | yes, `210ceb1c…` |
| `--run --horizon 14 --step 7` | 0 / 0 | yes (`dd2bbe11…`) | 33 | 383 569 | yes, `a5804179…` |
| `--regimes --horizon 7 --step 7` | 0 / 0 | yes (`bedaa2ba…`) | 29 | 6588 | yes, `7aa04c74…` |
| `--target` | 0 / 0 | yes (`71a1b585…`) | 105 | 9139 | yes, `ef816191…` |
| `--res7 --horizon 3 / 7 / 14 --step 7` | 0 / 0 each | yes each | 33 each | 1804 / 1804 / 1782 | yes each |
| `--regime-gate` | **1 / 0** | no: +4 caveat lines, −15 traceback lines | 513 / 502 | 36 735 stub / 37 140 | no (the repair) |

`--selftest` did not move (item 5).

## Test Results

| Item | Result |
|---|---|
| py_compile ×2 | exit 0, exit 0 |
| workflow parse | one step moved (12 → 18), one `if:` changed, nothing else |
| guard | 487 → **488 / FAIL 0**; +1 = the §4.3 pin, call #143 |
| verify_bench | **59 / FAIL 0**, output identical |
| `--selftest --seeds 10` | exit 0, stdout byte-identical |
| `--lab-selftest` 3 / 10 seeds | exit 0 / 0; one stdout line moved, 233 → 237; `E сравнений` 4254 / 4562; `полей` 1649; stderr identical |
| §5 item 1 round-trip | JSON-text equal; `agree ==` True; 3 × 6 |
| §5 item 2 pre-fix | `TypeError`; 36 735-byte stub |
| §5 item 3 printer | byte-identical |
| §5 item 6 failed write | no file, including over a complete one |
| controls 1–5 | all as partitioned |
| hosted gate | `success` ×2; negative run `failure` at step 19 alone |

## Reading items (§7) — report only, nothing edited

### 7.1 Are the other five artifact JSONs writable?

**World:** section D's (`synth_hl("normal")`, 16 documents, `C00` as `BTC`), built through each
mode's own `main()` branch, with `reconcile` stubbed as clean. The harness wrapped `_dump_raw` to
census the leaf types of the exact object handed to it.

| Artifact | Serialised? | Leaf types this world produced | Non-finite |
|---|---|---|---:|
| `stops_raw.json` | **yes**, 2540 B, parses | `float` 80, `numpy.float64` 8, `int` 8, `tuple` 24 | 0 |
| `run_raw.json` (H = 3, 7, 14) | **yes**, 388 474 / 388 645 / 383 569 B, parse | `float` 12 286, `str` 1230, `int` 96 (H = 7) | 0 |
| `regimes.json` | **yes**, 6588 B, parses | `int` 82, `str` 82 | 0 |
| `res7_dates.json` (H = 3, 7, 14) | **yes**, 1804 / 1804 / 1782 B, parse | `int` 82 / 82 / 81 | 0 |
| `target_raw.json` (known) | **yes**, 9139 B, parses | `float` 206, `int` 180, `bool` 17, `str` 15, `None` 6, `tuple` 31 | 0 |

None raised. All four serialised byte-identically through the pristine write as well
(Validation 11), so none of them was writable only because of this change.

**What this world did not produce**, read from the code at `ed4db7c2…`:

- **`stops_raw.json` can carry NaN.** In `stops_summary.pool.agg`:
  - `hit` and `med_dist` are `float("nan")` when a pool has no finite `p`;
  - `ratio_ci` takes `np.nan` for every bootstrap draw with `mo <= 0`, and `np.nanpercentile` over
    an all-NaN list gives NaN.

  These become bare `NaN` tokens and do not raise. It already carries `numpy.float64` (`whip`,
  from `np.mean`), which serialises because it subclasses `float`. No `np.int64`, `np.bool_` or
  `np.float32` path was found: `n` is `len(f)`, and every other scalar is wrapped in `float()`.
- **`run_raw.json` can carry NaN, and is the one of the four that could carry a non-float numpy
  scalar.**
  - `f_low` divides by `cd["volatility"] * sqrt(24) or 1e-9`; a NaN volatility is truthy and
    propagates.
  - `f_r7` is `cd["r7"]` passed through unchanged from `main.py`'s coeffs block, executed by
    `CdBuilder`, so its type is whatever the bot's code returns. Here that was always a Python
    `float`.
  - A NumPy integer, boolean or `float32` there would raise `TypeError` inside `_dump_raw`, and the
    file would now be absent rather than truncated.
  - The scorer outputs (`long`, `short`, `long_nopen`) arrive through a JSON bridge and are Python
    floats or `None`.
- **`regimes.json` and `res7_dates.json` cannot carry either.** `t` comes from a Python
  `range()` in `run_walk` / `walk_grid`, and `reg` is a `str` label or `None` from
  `btc_regimes`.

### 7.2 What the coin-word section costs (local pair, the post `--regime-gate` run above)

| Call | Wall (s) |
|---|---:|
| `regime_gate_summary(by_H, btc, …)`, market word (for scale) | 31.65 |
| coin word: `regime_gate_summary(…, splitter=_own_split)` **without** the census | 34.91 |
| coin word **with** the census (`own_regime_summary` = the call above + `own_census` 0.31) | **35.22** |
| whole mode | 108.6 |

**Peak resident size of the process: 306 588 KB** (`/usr/bin/time -v`; `ru_maxrss` agrees),
against 306 424 KB for the pre-change process. No archive figure is inferred from this.

## Deviations

These are recorded readings, not changes to a registered figure. None of them moves a count.

1. **`_dump_raw` empties the path on any failure, not only a serialisation failure.**
   - §4.2 step 3 says «on failure». Read beside step 2 («on success, write…»), that could mean a
     failed `json.dumps` only.
   - The same section ends: «After this change the path carries this run's artifact or nothing».
     A failed temporary write or `os.replace` that left the target alone would leave the previous
     run's complete file, which is the case §4.2 names as the worse one.
   - So one `try` covers all three operations, catching `BaseException` so an interrupt
     mid-write is covered too, and the temporary file is removed as well.
   - Only the serialisation branch was exercised (controls 2 and 3).
2. **The guard assertion reads `r_no[i].get('prod') or {}` instead of `r_no[i]['prod']`.** If a
   future driver dropped `prod`, `['prod']` would raise `KeyError` while evaluating `ok()`'s
   arguments and stop the guard before sections E–K. `.get` turns that case into this check's
   FAIL with `[]` as the key list read. The expected list, the condition's logic and the `info`
   discipline are §4.3's.
3. **The caveat says «может класть наблюдения сразу во все три популяции»** where §4.5 says one
   date «contributes observations to all three populations at once». The paragraph just above it
   in the same header says a date enters each population in which it has a word. A date whose
   coins all carry one word contributes to one population, so «может» keeps the two statements
   consistent. The sentence's comparison claim is §4.5's.
4. **Controls 1–3 and 5 ran on `/tmp` scratch copies; control 4 ran in the working tree on a
   throwaway branch** that was pushed, read and deleted. That branch is the only way to put a red
   commit in front of the hosted gate without adding it to the implementation branch.

## Pre-existing Issues

1. **Map `## 0` prose lags for `bench/backtest_bench.py`** (known and named in TZ-50 §0; not acted
   on). The map at `2026-09-16-b` still gives «**5102 lines**, `ba633202f43845ba0fdafbc1b92d9c04`»
   (map line 154). The file at `728129a` measured **5795 / `ed4db7c2bab9076e92982c664c6fc2f6`**,
   TZ-50's enforced figure. The map revision that clears this is the Architect's.
2. **A misplaced workflow comment, now one step further from what it describes.**
   `# Артефакт нужен именно тогда, когда что-то упало.` sits above `Деление по режиму BTC`, but
   describes the upload step's `if: always()` (first reported by TZ-41). After §4.4 the moved step
   sits between that comment and the upload. It was left untouched: §4.4 authorises one move and
   one condition.
3. **NumPy prints `RuntimeWarning: All-NaN slice encountered` twice per lab run** (stderr), on
   pristine and post alike, identical MD5 `279a86e6…`.
4. **`backtest_bench.py`'s argparse defaults `DEF_HTML` and `DEF_BOT` name two files that do not
   exist.** Every mode here ran with the workflow's explicit `--html ../index.html --bot
   ../main.py`.
5. **`gh run view <id> --log` exits 1 with an empty body when run outside a git checkout**
   («failed to determine base repo»). With `-R seahomebatumi-ai/crypto-auto` it returns the full
   log. This is a fact about the session's tooling, not the repository.

## Remaining Risks

- **The moved step has no dispatch reading.** `backtest_bench.yml` runs only on
  `workflow_dispatch`, so the new step position and `inputs.regime_gate && !cancelled()` have never
  executed on a runner. What stands behind them is the parsed-YAML comparison in Validation 2.
  Nothing here forecasts what the next dispatch will show (inv. 54).
- **The artifact carries bare `NaN`** (27 tokens on section D's world). Python reads it back, but a
  strict JSON reader refuses it. That is a property §4.2 accepts and leaves to the map.
- **Reading 7.1's open path.** `run_raw.json` would now fail by absence rather than truncation if
  `main.py`'s coeffs block ever returned a non-float NumPy scalar in `r7`. No world here produced
  one. The repair is the next TZ's, by §7.
- **The map's bench figures move on merge.** Its prose gives `bench/backtest_guard_bench.py` as
  2503 / `bfc984b1…`, which becomes **2513 / `622b844efcca4292df2a157680ca4324`**.
  `bench/backtest_bench.py` becomes **5830 / `a1b1ce27773332e5630bba4189bd4d69`** and
  `.github/workflows/backtest_bench.yml` **175 / `84efa8826db35837a810e3ad884dfa4b`**.
- **Temporary file names.** A write that dies between `open(tmp)` and the `except` handler, for
  example under a SIGKILL from the job's timeout, could leave `bench/_<name>.<pid>.tmp` behind.
  That path is ignored by `bench/_*` and is not among the upload paths, so it cannot reach the
  artifact.
- **No artifact in the old shape exists to be misread.** Every `--regime-gate` run before this
  change failed at the dump (Validation 8), so no reader of a tuple-keyed `agree` ever had a file.

## Commit

Implementation commit on `claude/tz-50-agree-map-and-artifact-write`, already pushed when this
section was written: **`2ecefc77838fa68e2dc0c330a18e777650d6dcd7`**. It contains the three files
under `## Files Modified`.

```
TZ-50: the agreement table becomes a two-level map, a failed artifact write leaves no file, and the driver's answer returns under the push-time gate

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

This report's commit, direct to `main`, containing only this file:

```
docs(reports): TZ-50 — the agreement table becomes a two-level map, a failed artifact write leaves no file, and the driver's answer returns under the push-time gate (TZ-50)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/41, base `main`, head
`claude/tz-50-agree-map-and-artifact-write`. It was opened with `gh pr create`.

## CI Execution

**`Bench gate` ran twice on a runner for `2ecefc77838fa68e2dc0c330a18e777650d6dcd7`, and both runs
concluded `success`.** Per-step conclusions come from `gh run view <id> --json jobs`:

| Run | Event | Conclusion | Steps |
|---|---|---|---|
| [35223415269](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/35223415269) | `push` to `claude/tz-50-agree-map-and-artifact-write` | `success` | 1–19 `success` |
| [35223439860](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/35223439860) | `pull_request` #41 | `success` | 1–19 `success` |

**The runner's own counts**, read with `gh run view <id> -R seahomebatumi-ai/crypto-auto --log |
grep -E "checks run:|comparisons$"`:

| Run | Log size | Step 9 `verify_bench.py` | Step 19 `backtest_guard_bench.py` |
|---|---:|---|---|
| 35223415269 | 87 802 bytes | `checks run: 59   FAIL 0` | E 32 · F 29 · G 63 · H 107 · I 95 · J 8 · K 11 comparisons · **`checks run: 488   FAIL 0`** |
| 35223439860 | 89 096 bytes | `checks run: 59   FAIL 0` | the same section lines · **`checks run: 488   FAIL 0`** |

**Negative run (control 4):**
[35225366648](https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/35225366648), `push`
to the deleted branch `claude/tz-50-negative-control` at `b7c935002f1032be5017559abac5868083b43dd7`,
conclusion **`failure`**. Only step 19 failed. Its log (86 511 bytes) reads `checks run: 488   FAIL
1`, with the one check-33 `prod` FAIL line.

**Not executed on a runner:** `.github/workflows/backtest_bench.yml`, which is
`workflow_dispatch` only and was not dispatched. Its `--selftest`, `--lab-selftest` and six mode
readings above are local runs in this container, not runner executions.

## Final Repository State

- Branch `claude/tz-50-agree-map-and-artifact-write` is at `2ecefc77838fa68e2dc0c330a18e777650d6dcd7`.
  It was pushed before this report was written, and `git ls-remote --heads origin` returns that
  hash.
- The working tree on that branch is clean (`git status --porcelain` empty). The generated
  `bench/_*` and `bench/__pycache__` files from this session's local runs, all ignored, were
  removed.
- The throwaway branch `claude/tz-50-negative-control` no longer exists locally or on `origin`.
- Pull request #41 is open.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Measured on a `git archive origin/main` extract at `728129a`.
`SYSTEM-MAP-CRYPTOCALCUL.md`: **2759 lines, `7f8fd2e8e553109cb7cffed329bd56e1`**. Revision string
in `## 0`: **`**Revision 2026-09-16-b.**`**, the revision TZ-50 requires.

**Anchors.** The list was cut by structure: the rows between the `| Anchor |` table's separator
line and the first line not starting with `|` (`/tmp/tz50/gate.py`). **The table has 7 rows, and 7
anchors were compared.** Every TZ row is quoted verbatim (`| name | `anchor` |` found in the TZ
text for all 7). Each fixed-string match, with the text it returned:

```
$ grep -n -o -F -- '**Revision 2026-09-16-b.**' SYSTEM-MAP-CRYPTOCALCUL.md
17:**Revision 2026-09-16-b.**
189:**Revision 2026-09-16-b.**
$ grep -n -o -F -- '### 3.12 Direction engine — veto cascade' SYSTEM-MAP-CRYPTOCALCUL.md
190:### 3.12 Direction engine — veto cascade
1101:### 3.12 Direction engine — veto cascade
$ grep -n -o -F -- '### 3.15 Catalyst registry' SYSTEM-MAP-CRYPTOCALCUL.md
191:### 3.15 Catalyst registry
1484:### 3.15 Catalyst registry
$ grep -n -o -F -- '### 3.16 List exhaustion — the day-range measure' SYSTEM-MAP-CRYPTOCALCUL.md
192:### 3.16 List exhaustion — the day-range measure
1581:### 3.16 List exhaustion — the day-range measure
$ grep -n -o -F -- '## 11. Analytical engine' SYSTEM-MAP-CRYPTOCALCUL.md
193:## 11. Analytical engine
2535:## 11. Analytical engine
$ grep -n -o -F -- '### 3.17 «РИСК ВЫНОСА» — the day'\''s own risk' SYSTEM-MAP-CRYPTOCALCUL.md
194:### 3.17 «РИСК ВЫНОСА» — the day's own risk
1748:### 3.17 «РИСК ВЫНОСА» — the day's own risk
$ grep -n -o -F -- '71. **A measurement that is not RETAINED was not taken,' SYSTEM-MAP-CRYPTOCALCUL.md
195:71. **A measurement that is not RETAINED was not taken,
2254:71. **A measurement that is not RETAINED was not taken,
```

The same seven commands against `CryptoTZ/TZ-50-agree-map-and-artifact-write.md` returned each
anchor at TZ lines 24–30; the revision also appears at line 17.

**The map's file table** has 4 rows, all quoted verbatim in TZ-50 §0. Measured values:

| File | Lines | MD5 | Map |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | match |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | match |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | match |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | match |

The same four values hold on `2ecefc7`.

**Files TZ-50's gate adds**, measured before the change and on the implementation commit:

| File | TZ §0 | Measured at `728129a` | At `2ecefc7` |
|---|---|---|---|
| `bench/backtest_bench.py` | 5795 / `ed4db7c2bab9076e92982c664c6fc2f6` | 5795 / `ed4db7c2bab9076e92982c664c6fc2f6` | 5830 / `a1b1ce27773332e5630bba4189bd4d69` |
| `bench/backtest_guard_bench.py` | 2503 / `bfc984b1d22ec1ad89cf536a1a47c529` | 2503 / `bfc984b1d22ec1ad89cf536a1a47c529` | 2513 / `622b844efcca4292df2a157680ca4324` |
| `.github/workflows/backtest_bench.yml` | 171 / `703330829c377a15fc0df71e25df92a7` | 171 / `703330829c377a15fc0df71e25df92a7` | 175 / `84efa8826db35837a810e3ad884dfa4b` |

Contract `EXECUTOR-INSTRUCTIONS.md`: 864 lines, `02abb1969626d2af150a0d1f6e02f2a7`, Version 23.

**Session artifacts** (`/tmp/tz50`, not committed): `gate.py` `915e644c…`, `baseline.sh`
`08fb5c36…`, `post.sh` `6d59a281…`, `h/harness.py` `17e6fda3…`, `h/extremes.py` `31761228…`,
`h/mutate.py` `291dec4c…`, `h/e3_attrib.py` `658b2fcb…`, `h/guard_names.py` `a8949a0a…`,
`h/mkcache.py` `f151fc65…`, `h/steps.py` `43878794…`. Run outputs are in `base/` and `post/`.
