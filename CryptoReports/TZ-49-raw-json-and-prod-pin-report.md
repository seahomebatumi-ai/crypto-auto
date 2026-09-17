# Implementation Report — TZ-49

## Status

**BLOCKED.**

The fingerprint gate passed, and so did the sequencing clause: pull request #40 is merged and
`bench/backtest_bench.py` reads **5795 / `ed4db7c2bab9076e92982c664c6fc2f6`**, not the
5102 / `ba633202…` pair §0 names as the stop.

All five §4 sections were built as a prototype and measured (contract §12 disclosure under
`## Deviations`). Four of the five hold exactly as written: §4.2's write helper, §4.3's pin,
§4.4's step move and §4.5's sentence. **What cannot hold is §4.1's record shape together with
§5 item 5 and validation item 6.**

§4.1 requires `agree` to become a list of records. Each record carries the `marketRegime`
word, the `btc_regimes` word and the count. §5 item 5 and validation item 6 then say:

> `--lab-selftest` moves in exactly one figure: the count of lines the coin-word section adds,
> by the number of lines §4.5 prints. Every other lab figure, **every section's comparison
> count** and the lab verdict are unchanged.

> 6. `--lab-selftest` at default seeds and at `--lab-seeds 10`: exit 0 both, **section E's
> comparison count unchanged at both** …

(Emphasis added in both quotations.)

**Why they cannot both hold.** §4.1 says `_rg_agree`'s output "has exactly two readers in the
repository". There is a third. TZ-48's lab section E, control E3, diffs the whole
`--regime-gate` summary, `agree` included (`bench/backtest_bench.py:5065`):

```python
    gq = _out_diff(sg0, sg)
    f5 += [chk_n(tq["cmp"], tq["diff"]), chk(tq["missing"] == 0 and tq["added"] == 0),
           chk_n(gq["cmp"], gq["diff"]), chk(gq["missing"] == 0 and gq["added"] == 0)]
```

`_out_diff` counts every leaf `_out_fields` reaches, and `chk_n` adds that count to section
E's comparison total. A tuple key was one leaf (the count under `repr((w1, w2))`). A record is
three leaves (two words and a count). So E3's field count and section E's total both rise by
**2 per agreement record**. That follows from §4.1's shape itself, not from how the prototype
wrote it:

| Reading | Pristine | Prototype | Δ |
|---|---:|---:|---:|
| E3 `--regime-gate: полей`, 3 seeds | 1649 | 1661 | +12 |
| **`E сравнений`, 3 seeds** | **4254** | **4266** | **+12** |
| E3 `--regime-gate: полей`, 10 seeds | 1649 | 1661 | +12 |
| **`E сравнений`, 10 seeds** | **4562** | **4574** | **+12** |
| E3 `добавлено раздела слова монеты` (the figure §5 item 5 licenses) | 233 | 237 | +4 |

Section D's world carries **6 agreement records**, and 6 × (3 − 1) = 12. This was measured, not
inferred: `/tmp/tz49/h/e3_attrib.py` rebuilt that world exactly as the lab does and read
`_out_fields` directly. The pristine module has 6 leaves under `agree` and 1649 in total. The
prototype has 18 and 1661. The prototype's summary with `agree` put back into tuple keys reads
1649 again (item 6). Every other line of both lab runs is byte-identical, both runs exit 0, and
the verdict is unchanged (`## Validation`, item 6).

**No shape satisfies both clauses.**

- Any record carrying three scalars is three leaves to `_out_fields`, whether it is a dict, a
  list or a tuple.
- One leaf per pair needs either a joined string, which §4.1 forbids in so many words, or a
  nested map `{w1: {w2: n}}`, which is not a list of records. The nested map was measured on a
  scratch copy. There `--lab-selftest` moves in exactly the one licensed figure: E3 `полей`
  stays 1649, `E сравнений` stays 4254, and `добавлено раздела` goes 233 → 237 (output MD5
  `936cc1e2…`). The copy also writes, reloads and prints all four extremes.
- Changing what `_out_fields` counts would edit the lab's comparator. That file region is
  outside `## Touches`, and editing a bench's comparator to keep a count is hard-floor item 2.

The choice between the two readings produces different code and belongs to the Architect
(contract §12).

**Two more findings with the same root.** Neither blocks on its own, but a corrected TZ needs
both clauses amended:

1. **§6 control 2, as written, cannot keep `--lab-selftest` green.** Reverting only `_rg_agree`
   leaves `report_regime_gate` iterating records over a tuple-keyed dict. Lab E3 prints that
   table (`printed(report_regime_gate, sg0)`, `:5070`), so the lab dies there. Measured: exit 1
   with `TypeError: tuple indices must be integers or slices, not str` at
   `printed(report_regime_gate, sg0)`, after sections A–D and E0–E2 printed byte-identically,
   and no verdict line. Through `main()`, the same scratch copy goes red in the printer
   (`TypeError: tuple indices must be integers or slices, not str`) before the write is
   reached. That red localises the printer, not the serialisation (inv. 68). Reverting the
   printer loop as well gives the partition exactly as registered. Measured: the write raises
   `TypeError … not tuple` inside `_dump_raw` and leaves no file, the guard reads 488 / FAIL 0,
   `--selftest` is byte-identical, and `--lab-selftest` exits 0 moving only the licensed
   figure.
2. **§5 item 1's "the object loaded back from the file equals the object that was dumped"** is
   false under Python equality for any non-empty summary, and the cause is not `agree`:
   - `trunc` and `pop_dates` are keyed by int horizons, and JSON returns them as strings;
   - every `*_ci` tuple returns as a list;
   - NaN is unequal to itself.

   Measured on the prototype's own `main()` write: whole-object `==` False (2 int-keyed dicts,
   96 tuples, 27 NaN), `agree` `==` **True**, the reloaded object re-serialises to the
   file's exact text **True**. The satisfiable reading is equality as JSON.

**What unblocks it:** the Architect chooses one of these and re-issues the TZ.

- **(A) Keep §4.1.** Register section E's total and E3's field count as moving by 2 per
  agreement record (+12 on section D's world, at both seed counts), amend control 2 to revert
  the printer loop with `_rg_agree`, and state §5 item 1 as JSON equality. The prototype diff
  (`/tmp/tz49/proto.diff`, 187 lines, MD5 `19ac76813d064198b92fb4f4180f17b0`, full text under
  `## Implementation Summary`) applies to `d9934f6` unchanged under (A).
- **(B) Re-shape §4.1** to a map with one leaf per pair. §5 item 5 then holds as written.

Apart from those clauses, every item that could run without a pushed branch read as registered
on the prototype. Items 10 and 11 need the implementation commit and were not run (`## Validation`).

## Inbound Filing

None. `CryptoTZ/TZ-49-raw-json-and-prod-pin.md` arrived at its canonical path in `d9934f6`
("Add files via upload"). `git log --oneline --all -- 'CryptoTZ/TZ-49*'` lists that commit
alone, so nothing was moved and no earlier revision exists under that number.

## Scope Executed

**Class: branch TZ** (contract §8). `## 3` names three files outside `CryptoReports/**`:
`bench/backtest_bench.py`, `bench/backtest_guard_bench.py` and
`.github/workflows/backtest_bench.yml`.

Contract §4a, step by step:

- **Steps 1–5 (read, fetch, locate, read the TZ, fingerprint gate):** done in full. `git fetch`
  moved `origin/main` from `ad3b996` to `d9934f6`, and the worktree was fast-forwarded to it.
  `git rev-parse --is-shallow-repository` printed `false`.
- **Step 6 (repository state):** the tree was clean at `d9934f6`.
  - `gh pr view 40` printed `MERGED 2026-09-17T01:43:48Z 074c4231176fc617471695ce0bc9b4254e9eab18`.
  - `git merge-base --is-ancestor 4a11c8b origin/main` succeeded.
  - **The previous TZ's branch is merged; this work was not stacked on an unmerged base.**
- **Step 7 (implement):** entered as a measurement. All five §4 sections were written into the
  working tree as a prototype, saved outside the repository, measured from a separate extract,
  and discarded with `git checkout --`.
- **Step 8 (validate):** every item that does not need a pushed branch was run against the
  prototype (`## Validation`). Items 10 and 11 need an implementation commit on a runner, and
  none was made.
- **Step 9 (branch and pull request):** not reached.
- **Step 10:** this report.

**Why §4.2–§4.5 were not shipped alone.** Contract §6 keeps independent scopes independent.
TZ-49 names no independent scopes: one scope sentence, one `## Touches` and one commit
message, which §8 requires verbatim. The message says "the regime-gate artifact becomes
writable", and that is false without §4.1. The validation also binds the sections together:

- items 7 and 9 and controls 2 and 4 read §4.1 through §4.2's write;
- §5 item 5 reads §4.1 and §4.5 through one lab line;
- items 10 and 11 are defined on the implementation commit of the whole TZ.

TZ-11 and TZ-27 went PARTIAL only because their TZs named stages or scopes. If the Architect
prefers §4.2–§4.5 shipped now, that change is control 2b's module (item 9), and it measured
green on every row. It keeps §4.1's docstring paragraph, which a shipped version would drop.

## Files Created

- `CryptoReports/TZ-49-raw-json-and-prod-pin-report.md` — this report.

## Files Modified

None. After the discard, all three files in scope read their §0 baselines:

- `bench/backtest_bench.py`: 5795 lines, `ed4db7c2…`;
- `bench/backtest_guard_bench.py`: 2503 lines, `bfc984b1…`;
- `.github/workflows/backtest_bench.yml`: 171 lines, `70333082…`.

## Files Renamed

None.

## Files Deleted

None from the repository. `py_compile` (item 1) created `bench/__pycache__/` in the working
tree, and it was removed. It is ignored and was never tracked. Every bench run happened in the
`/tmp` extracts, not in the worktree.

## Implementation Summary

Everything below describes the **discarded prototype**. The repository carries none of it.

**Provenance.** The edits were made in the worktree at `d9934f6` and saved with
`git diff > /tmp/tz49/proto.diff` (187 lines, MD5 `19ac76813d064198b92fb4f4180f17b0`). They
were applied with `patch -p1` to a fresh `git archive HEAD` extract at `/tmp/tz49/proto`,
after `git apply --check` printed nothing. `cmp` confirmed the extract's
`bench/backtest_bench.py` equals the worktree file. Every prototype reading was taken from
that extract, and every pre-change reading from a second extract at `/tmp/tz49/pristine`. The
worktree was then restored with `git checkout --`.

| File | Before (lines / MD5) | Prototype (lines / MD5) | `-U0` hunks | +/− |
|---|---|---|---:|---|
| `bench/backtest_bench.py` | 5795 / `ed4db7c2bab9076e92982c664c6fc2f6` | 5815 / `113000c5cf39c2eef0f9c470a5453292` | 11 | 32 / 12 |
| `bench/backtest_guard_bench.py` | 2503 / `bfc984b1d22ec1ad89cf536a1a47c529` | 2512 / `4065b19848b7b848ca4eab652a6f9d0e` | 1 | 9 / 0 |
| `.github/workflows/backtest_bench.yml` | 171 / `703330829c377a15fc0df71e25df92a7` | 175 / `4fb0d30e27280b7a3a5f2f57a2e5af77` | 2 | 14 / 10 |

The default diff shows the same hunk counts; no two edits sit within six lines of each other.

### §4.1 — `_rg_agree` returns records; `report_regime_gate` iterates them

- `_rg_agree` (`:4050`) builds its dict exactly as before, then returns
  `[{"marketRegime": w1, "btc_regimes": w2, "n": n} for (w1, w2), n in sorted(cell.items())]`.
  The dict keys are unique, so sorting the items orders the records by `(w1, w2)`. That is the
  order the printer's own `sorted(sm["agree"].items())` produced, and the sort now happens
  once, at build time.
- A sort at build time cannot raise where the printer's could not. `_rg_word` returns a
  non-empty word. `btc_regimes` (`:641`) labels only `тренд` or `диапазон`, and `_rg_agree`
  substitutes the literal `нет метки` for an unlabelled date. Every key is therefore a pair of
  strings.
- The printer (`:4309`) prints `r["marketRegime"]`, `r["btc_regimes"]` and `r["n"]` through the
  unchanged format string. `agree_dates` is untouched.
- The record keys are the names of the two functions the words come from, so an artifact read
  months later names its sources.

### §4.2 — `_dump_raw`, and the six sites

The helper was placed immediately above `main()`, because five of the six writes live in it:

```python
def _dump_raw(obj, name):
    """ТЗ-49 · the one write of a run artifact, `name` under HERE. The text is
    built BEFORE the file is opened, so an object json cannot serialise raises
    with no file on disk: a truncated file uploads with the artifact and reads
    as data (inv. 70). The bridge job writes and the cache writes do not come
    here — they are not artifacts."""
    text = json.dumps(obj)
    with open(os.path.join(HERE, name), "w") as f:
        f.write(text)
```

`grep -n "json.dump(" bench/backtest_bench.py` on the pristine file prints **ten** sites:

| Line | Write | Routed |
|---:|---|---|
| 217 | `JsScorer.score` job file, `allow_nan=False` | no — job write |
| 723 | `run_regimes` → `regimes.json` | **yes** |
| 938 | `fetch_prices` → `cache/<sym>.json` | no — cache write |
| 2726 | `JsBridge.call` job file, `allow_nan=False` | no — job write |
| 3113 | `fetch_funding` → funding cache file | no — cache write |
| 5626 | `--stops` → `stops_raw.json` | **yes** |
| 5671 | `--target` → `target_raw.json` | **yes** |
| 5720 | `--regime-gate` → `regime_gate_raw.json` | **yes** |
| 5745 | `--res7` → `res7_dates.json` | **yes** |
| 5789 | `--run` → `run_raw.json` | **yes** |

**Six artifact writes, as §4.2 counts.** Two corrections to its gloss, neither of which changes
a site:

- one of "the two `JsBridge` job writes" is `JsScorer.score`'s (`:217`);
- only the job writes carry `allow_nan=False`; the two cache writes do not.

`json.dumps(obj)` followed by one `write` produces the same bytes as `json.dump(obj, fp)`. The
proof is item 12's table: five artifacts byte-identical pre/post through `main()`, 388 645
bytes the largest.

### §4.3 — the pin at check 33

The assertion is added directly under check 33's top-level key assertion
(`backtest_guard_bench.py:888`), reads the same two no-grid answers `r_no[0]` and `r_no[1]`,
and carries its neighbour's `info` discipline:

```python
# ТЗ-49 · one level down. Fields now land INSIDE `prod` (ТЗ-36, ТЗ-48), where
# check 43 tests a superset only, so the exact set is pinned here as well. The
# list is written, never read off the driver (inv. 61).
ok('33. and the key set of `prod` on the same answer is exactly the registered one',
   r_no[0] is not None and r_no[1] is not None
   and sorted(r_no[0]['prod']) == sorted(r_no[1]['prod'])
   == ['anchor', 'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt',
       'waiting'],
   None if not r_no[0] else sorted(r_no[0]['prod']))
```

The expected list is §4.3's, character for character. **The merged driver carries exactly
those nine.** The prototype guard reads `488 / FAIL 0`, and control 1 prints the list the call
actually returned (item 9). No check was renumbered, no section relabelled, and check 43 is
untouched.

### §4.4 — the step moves last, with `!cancelled()`

The step block moved with its own three ТЗ-32 comment lines. It now sits after
`Деление по режиму BTC` and immediately before `actions/upload-artifact@v4`. Its condition
changed to `${{ inputs.regime_gate && !cancelled() }}`. The command, the `tee` target and both
artifact paths are unchanged.

Four comment lines were added above the step. They are in Russian, per the contract's
workflow-comment exception, and they carry the reason for the position and the condition, as
the `--attrib` step's comment does for its own `!cancelled()`:

```yaml
      # ТЗ-49. Шаг последний перед артефактом: после него ничего не идёт, и его
      # падение или таймаут не стоит ни одного другого чтения. !cancelled() —
      # по той же причине, что у --attrib: --verify возвращает 1 на
      # coverage/unexplained, и без условия шаг пропускался бы ровно тогда.
```

### §4.5 — the sentence and its site

**Site:** `report_own_regime` (`:4480`). The sentence goes after the paragraph ending «Блоки
бутстрапа — по-прежнему даты; сетка, кворум и планка — те же.» (`:4488–4490`) and before the
«Кворум: …» line (`:4491`). That puts it in the section's header, before its cells, its census
and its verdict. It is one sentence, printed on four lines:

```
ОГОВОРКА: одна дата кладёт наблюдения сразу в несколько популяций, а два
ДИ95 строятся как независимые, и положительная ковариация мешает им
разойтись, поэтому `range` строго ниже `trend` — по-прежнему сильное
свидетельство, а «тезис устоял» — слабее того же чтения под словом рынка.
```

It contains no number, no verdict word and no threshold. It also contains neither substring
lab E1 W1 reads from this printer (`decidable: false`, `дат в популяции 0`), so it cannot turn
a false check true.

### The full prototype diff

```diff
diff --git a/.github/workflows/backtest_bench.yml b/.github/workflows/backtest_bench.yml
index 8f0e2b6..24a67de 100644
--- a/.github/workflows/backtest_bench.yml
+++ b/.github/workflows/backtest_bench.yml
@@ -83,16 +83,6 @@ jobs:
           python backtest_bench.py --target \
             --html ../index.html --bot ../main.py 2>&1 | tee target.txt
 
-      # ТЗ-32. Сетка H × RR, делённая словом marketRegime на дате входа.
-      # Шаг включается входом запуска и по умолчанию не идёт: прогон стоит
-      # шести проходов run_target и нужен не каждому запуску стенда.
-      - name: Ворота режима на архиве (--regime-gate)
-        if: ${{ inputs.regime_gate }}
-        run: |
-          cd bench
-          python backtest_bench.py --regime-gate \
-            --html ../index.html --bot ../main.py 2>&1 | tee regime_gate.txt
-
       - name: Фактор res7 (--res7, первичный — 7д)
         run: |
           cd bench
@@ -144,6 +134,20 @@ jobs:
           python backtest_bench.py --regimes --horizon 7 --step 7 \
             --html ../index.html --bot ../main.py 2>&1 | tee regimes.txt
 
+      # ТЗ-32. Сетка H × RR, делённая словом marketRegime на дате входа.
+      # Шаг включается входом запуска и по умолчанию не идёт: прогон стоит
+      # шести проходов run_target и нужен не каждому запуску стенда.
+      # ТЗ-49. Шаг последний перед артефактом: после него ничего не идёт, и его
+      # падение или таймаут не стоит ни одного другого чтения. !cancelled() —
+      # по той же причине, что у --attrib: --verify возвращает 1 на
+      # coverage/unexplained, и без условия шаг пропускался бы ровно тогда.
+      - name: Ворота режима на архиве (--regime-gate)
+        if: ${{ inputs.regime_gate && !cancelled() }}
+        run: |
+          cd bench
+          python backtest_bench.py --regime-gate \
+            --html ../index.html --bot ../main.py 2>&1 | tee regime_gate.txt
+
       - uses: actions/upload-artifact@v4
         if: always()
         with:
diff --git a/bench/backtest_bench.py b/bench/backtest_bench.py
index 06d5fe4..abcd257 100644
--- a/bench/backtest_bench.py
+++ b/bench/backtest_bench.py
@@ -720,8 +720,7 @@ def run_regimes(html, bot, horizon=7, step=7):
             m = metrics(sub, key, sg, level=REG_LEVEL)
             report_regime("%s · режим «%s»%s" % (nm, r, "" if primary else " (разведка)"),
                           m, primary)
-    json.dump([{"t": x["t"], "reg": x["reg"]} for x in d],
-              open(os.path.join(HERE, "regimes.json"), "w"))
+    _dump_raw([{"t": x["t"], "reg": x["reg"]} for x in d], "regimes.json")
 def tokens_from_html(html_path):
     """Список пар — из фронта, а не из отдельной копии (инвариант 2: список монет
     живёт в одном месте). Разбирается настоящим node, а не регуляркой."""
@@ -4052,7 +4051,11 @@ def _rg_agree(by_H, btc):
     слово btc_regimes) по датам, которые сетка реально посчитала. Ничего не
     решает и никуда не подключается — btc_regimes не трогается и тезисом не
     является (§3.3). Даты без метки btc_regimes названы, а не отброшены:
-    исчезнувшая строка читалась бы как согласие."""
+    исчезнувшая строка читалась бы как согласие.
+
+    ТЗ-49: the cells leave as a LIST OF RECORDS, sorted by the two words once,
+    here. A tuple key is not JSON, and a pair joined into one string would be a
+    parse over free text from two sources; a record needs none."""
     times = sorted(set(d["t"] for ds in by_H.values() for d in ds))
     lab = btc_regimes(btc, times)
     cell, seen = {}, set()
@@ -4064,7 +4067,8 @@ def _rg_agree(by_H, btc):
             w2 = lab.get(d["t"])
             cell[(_rg_word(d), w2[0] if w2 else "нет метки")] = \
                 cell.get((_rg_word(d), w2[0] if w2 else "нет метки"), 0) + 1
-    return cell, len(seen)
+    return ([{"marketRegime": w1, "btc_regimes": w2, "n": n}
+             for (w1, w2), n in sorted(cell.items())], len(seen))
 
 
 def _rg_trunc(by_H):
@@ -4306,8 +4310,8 @@ def report_regime_gate(sm):
           % sm["agree_dates"])
     print("Счёт, и только счёт: btc_regimes не тронут, тезисом не является и\n"
           "ничего не подключает (§3.3).")
-    for (w1, w2), n in sorted(sm["agree"].items()):
-        print("  %-8s × %-10s %d" % (w1, w2, n))
+    for r in sm["agree"]:
+        print("  %-8s × %-10s %d" % (r["marketRegime"], r["btc_regimes"], r["n"]))
 
     v = sm["verdict"]
     print("\n" + "═" * 62)
@@ -4488,6 +4492,12 @@ def report_own_regime(sm):
     print("Популяция — подмножество НАБЛЮДЕНИЙ, а не дат: слово монеты меняется\n"
           "внутри даты, и дата входит в каждую популяцию, где у неё есть слово.\n"
           "Блоки бутстрапа — по-прежнему даты; сетка, кворум и планка — те же.")
+    # ТЗ-49 §4.5. The reading is read from an artifact long after this text,
+    # so the comparison structure travels with it as one sentence.
+    print("ОГОВОРКА: одна дата кладёт наблюдения сразу в несколько популяций, а два\n"
+          "ДИ95 строятся как независимые, и положительная ковариация мешает им\n"
+          "разойтись, поэтому `range` строго ниже `trend` — по-прежнему сильное\n"
+          "свидетельство, а «тезис устоял» — слабее того же чтения под словом рынка.")
     print("Кворум: %d сетапов и %d дат — на КАЖДОЙ из двух популяций."
           % (sm["quorum"][0], sm["quorum"][1]))
     print(_excl_line(sm))
@@ -5583,6 +5593,17 @@ def lab_selftest(html, bot, seeds=3):
     return 0 if ok else 1
 
 # ─────────────────────────────────────────────────────────────────────────────
+def _dump_raw(obj, name):
+    """ТЗ-49 · the one write of a run artifact, `name` under HERE. The text is
+    built BEFORE the file is opened, so an object json cannot serialise raises
+    with no file on disk: a truncated file uploads with the artifact and reads
+    as data (inv. 70). The bridge job writes and the cache writes do not come
+    here — they are not artifacts."""
+    text = json.dumps(obj)
+    with open(os.path.join(HERE, name), "w") as f:
+        f.write(text)
+
+
 def main():
     ap = argparse.ArgumentParser()
     ap.add_argument("--selftest", action="store_true")
@@ -5623,7 +5644,7 @@ def main():
             sys.exit("СТОП: в кэше %d монет." % len(ser))
         sm = stops_summary(run_stops(ser, a.bot, a.html, a.horizon, a.step))
         report_stops(sm)
-        json.dump(sm, open(os.path.join(HERE, "stops_raw.json"), "w"))
+        _dump_raw(sm, "stops_raw.json")
         return 0
     if a.target:
         # --horizon/--step are NOT read here: the mode's horizon is H_NOISE cut
@@ -5668,7 +5689,7 @@ def main():
                                        betawalk=BetaWalk(a.bot, btc["prices"])),
                             a.html, excluded=excluded)
         report_target(sm)
-        json.dump(sm, open(os.path.join(HERE, "target_raw.json"), "w"))
+        _dump_raw(sm, "target_raw.json")
         pl, ps = sm["arms"]["prod"]["long"], sm["arms"]["prod"]["short"]
         if not (pl and pl["quorum"]) and not (ps and ps["quorum"]):
             # A run that compared too little must not look like a run that
@@ -5717,7 +5738,7 @@ def main():
         # dump so the reading reaches regime_gate.txt without depending on
         # anything after it (inv. 71); `sm` and its file are not touched.
         report_own_regime(own_regime_summary(by_H, a.html, excluded=excluded))
-        json.dump(sm, open(os.path.join(HERE, "regime_gate_raw.json"), "w"))
+        _dump_raw(sm, "regime_gate_raw.json")
         if not sm["verdict"]["decidable"]:
             # Прогон, сравнивший слишком мало, не должен выглядеть как прогон,
             # который ничего не нашёл (инв. 22, 37).
@@ -5742,8 +5763,7 @@ def main():
                              ("r30 · контр (лонг)", "r30c", 1.0)):
             factor_report("%s · %dд" % (ttl, a.horizon),
                           metrics(d, key, sg, level=EXPL_LEVEL), False)
-        json.dump([{"t": x["t"]} for x in d],
-                  open(os.path.join(HERE, "res7_dates.json"), "w"))
+        _dump_raw([{"t": x["t"]} for x in d], "res7_dates.json")
         return 0
     if a.funding:
         ser = load_cache()
@@ -5786,7 +5806,7 @@ def main():
                    % (side.upper(), a.horizon,
                       " · ранг/оборот сегодняшние" if qc else ""),
                    metrics(d, side, 1.0 if side == "long" else -1.0))
-        json.dump(d, open(os.path.join(HERE, "run_raw.json"), "w"))
+        _dump_raw(d, "run_raw.json")
         return 0
     ap.print_help()
 
diff --git a/bench/backtest_guard_bench.py b/bench/backtest_guard_bench.py
index d1c5bf1..4e7019c 100644
--- a/bench/backtest_guard_bench.py
+++ b/bench/backtest_guard_bench.py
@@ -890,6 +890,15 @@ ok('33. and the untouched keys of the answer are unchanged',
    and sorted(r_no[0]) == sorted(r_no[1]) == ['dist', 'moneyBelowMin', 'ok',
                                               'prod', 'reg', 'stop', 'subs'],
    None if not r_no[0] else sorted(r_no[0]))
+# ТЗ-49 · one level down. Fields now land INSIDE `prod` (ТЗ-36, ТЗ-48), where
+# check 43 tests a superset only, so the exact set is pinned here as well. The
+# list is written, never read off the driver (inv. 61).
+ok('33. and the key set of `prod` on the same answer is exactly the registered one',
+   r_no[0] is not None and r_no[1] is not None
+   and sorted(r_no[0]['prod']) == sorted(r_no[1]['prod'])
+   == ['anchor', 'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt',
+       'waiting'],
+   None if not r_no[0] else sorted(r_no[0]['prod']))
 # ═══════════════════════════════════════════════════════════════════════════
 # E. The venue actually fetched is an OBSERVATION (ТЗ-34)
 # ═══════════════════════════════════════════════════════════════════════════
```

## Validation

Every command below was run in this session's container, one bench at a time. "Pristine" is a
`git archive HEAD` extract of `d9934f6` at `/tmp/tz49/pristine`, and "prototype" is the same
extract with the diff applied, at `/tmp/tz49/proto`. `diff -rq` between the two lists exactly
the three files in scope. `index.html` (`4e71da9b…`) and `main.py` (`0e3ead8c…`) are identical
in both.

### Item 1 — `py_compile`

Run on the prototype in the worktree, before the discard:

```
$ python3 -m py_compile bench/backtest_bench.py; echo "py_compile bb exit $?"
py_compile bb exit 0
$ python3 -m py_compile bench/backtest_guard_bench.py; echo "py_compile guard exit $?"
py_compile guard exit 0
```

### Item 2 — the workflow, parsed before and after

`python3 /tmp/tz49/h/steps.py <pristine yml> <prototype yml>` (PyYAML 6.0.1), which prints
each step's name, or its `uses` / `run` when unnamed, with its `if:`:

```
== before: /tmp/tz49/pristine/.github/workflows/backtest_bench.yml — 19 steps
   1  actions/checkout@v4                                          if: —
   2  actions/setup-python@v5                                      if: —
   3  pip install numpy requests                                   if: —
   4  actions/cache@v4                                             if: —
   5  Диагностика источников                                       if: —
   6  Самопроверка стенда (офлайн)                                 if: —
   7  Самопроверка лаборатории (офлайн, миры с известным ответом)  if: —
   8  Закачка истории                                              if: —
   9  Закачка funding (архив, монтные ZIP)                         if: —
  10  Слой инвалидации (--stops)                                   if: —
  11  Цель сделки — экстремум 90д против канала продолжения (--target) if: —
  12  Ворота режима на архиве (--regime-gate)                      if: ${{ inputs.regime_gate }}
  13  Фактор res7 (--res7, первичный — 7д)                         if: —
  14  Фактор funding (--funding, первичный — 7д)                   if: —
  15  Прогон                                                       if: —
  16  Сверка восстановления с живым coeffs.json                    if: —
  17  Разложение расхождения доходностей (--attrib)                if: ${{ !cancelled() }}
  18  Деление по режиму BTC                                        if: ${{ !cancelled() }}
  19  actions/upload-artifact@v4                                   if: always()
== after: /tmp/tz49/proto/.github/workflows/backtest_bench.yml — 19 steps
   1  actions/checkout@v4                                          if: —
   2  actions/setup-python@v5                                      if: —
   3  pip install numpy requests                                   if: —
   4  actions/cache@v4                                             if: —
   5  Диагностика источников                                       if: —
   6  Самопроверка стенда (офлайн)                                 if: —
   7  Самопроверка лаборатории (офлайн, миры с известным ответом)  if: —
   8  Закачка истории                                              if: —
   9  Закачка funding (архив, монтные ZIP)                         if: —
  10  Слой инвалидации (--stops)                                   if: —
  11  Цель сделки — экстремум 90д против канала продолжения (--target) if: —
  12  Фактор res7 (--res7, первичный — 7д)                         if: —
  13  Фактор funding (--funding, первичный — 7д)                   if: —
  14  Прогон                                                       if: —
  15  Сверка восстановления с живым coeffs.json                    if: —
  16  Разложение расхождения доходностей (--attrib)                if: ${{ !cancelled() }}
  17  Деление по режиму BTC                                        if: ${{ !cancelled() }}
  18  Ворота режима на архиве (--regime-gate)                      if: ${{ inputs.regime_gate && !cancelled() }}
  19  actions/upload-artifact@v4                                   if: always()
```

The structural comparison of the two parsed documents:

```
steps before 19, after 19; same set True
moved step position: 12 -> 18
the other 18 steps: same order True, equal as parsed True
moved step equal apart from if: True
if: '${{ inputs.regime_gate }}' -> '${{ inputs.regime_gate && !cancelled() }}'
next step after it: actions/upload-artifact@v4
job and document equal apart from steps: True
```

**One moved step and one changed condition.** Six other steps show a new index only because
the moved step left position 12; their relative order and content are unchanged. The text
diff is two `-U0` hunks: the block removed, and the block plus four comment lines added.

### Item 3 — the guard: 487 → 488, attributed by name

`python3 bench/backtest_guard_bench.py`, from each extract's root:

| | Exit | Seconds | Output MD5 | Last line |
|---|---:|---:|---|---|
| pristine | 0 | 5 | `d91178acbed79648100d6b07b2f88c2c` | `checks run: 487   FAIL 0` |
| prototype | 0 | 5 | `dce1626ab1b43ac21afd3d526b65ed3b` | `checks run: 488   FAIL 0` |

`diff` of the two outputs is one line, the total. Section lines E–K (32, 29, 63, 107, 95, 8, 11)
are identical. Check 33 sits in the ТЗ-32 regime-gate block, which prints no section line of
its own.

`/tmp/tz49/h/guard_names.py` runs a copy of each guard with `ok()` recording every check's
name and result, and nothing else changed. Each copy sat in a repository-shaped tree, because
the guard reads `HERE/../main.py`. Both copies printed the same totals as the real runs (487 /
FAIL 0 and 488 / FAIL 0). Compared as multisets and as sequences:

```
recorded ok() calls: pristine 487, prototype 488
failing: pristine 0, prototype 0
names only in prototype (multiset): ['33. and the key set of `prod` on the same answer is exactly the registered one']
names only in pristine (multiset): []
first divergence at call #143: '33. and the key set of `prod` on the same answer is exactly the registered one'
rest aligned after the insertion: True
results aligned (pass/fail) apart from the insertion: True
prototype call #143 result: True
```

**The +1 is §4.3's assertion, by name, at position 143, and it passes.** Every other check has
the same name, position and result.

### Item 4 — `verify_bench.py`

`python3 bench/verify_bench.py`: pristine exit 0, prototype exit 0. Both outputs are
`checks run: 59   FAIL 0`, MD5 `4dff115f3f0595d2fe74d99cf4052422` on both sides, so they are
**byte-identical**.

### Item 5 — `--selftest --seeds 10`

`cd bench && python3 backtest_bench.py --selftest --seeds 10 --html ../index.html --bot ../main.py`

| | Exit | Seconds | Output MD5 |
|---|---:|---:|---|
| pristine | 0 | 90 | `888b31de3f1f77380b23e179bca32c2a` |
| prototype | 0 | 92 | `888b31de3f1f77380b23e179bca32c2a` |

The output is **byte-identical**. `--selftest` prints no count of its own. Counted at its
comparison sites in `selftest()` (`:2483`), which is outside the diff, it makes **36
comparisons on both sides**:

- Т2: 1, record identity;
- Т3: 1, monotonicity;
- Т4: 30, the sign or 2·SE test, 10 seeds × 3 worlds;
- ИТОГ: 4, `ok_null` twice and `ok_pow` twice.

### Item 6 — `--lab-selftest` at 3 and 10 seeds — **fails as registered**

`cd bench && python3 backtest_bench.py --lab-selftest [--lab-seeds 10] --html ../index.html --bot ../main.py`

| | Exit | Seconds | Peak RSS (KB) | Output MD5 | `E сравнений` | Verdict line |
|---|---:|---:|---:|---|---:|---|
| pristine, 3 seeds | 0 | 369 | 389 344 | `c05f2a83e0c168c8cd7777ce5393be24` | 4254 / 0 | «измеряет то, что должна» |
| prototype, 3 seeds | 0 | 377 | 398 244 | `e945abf0f9665d3461941b7bfba139ec` | **4266** / 0 | «измеряет то, что должна» |
| pristine, 10 seeds | 0 | 564 | — | `ecb32dfb6e70c617234ec91657cd3e07` | 4562 / 0 | «измеряет то, что должна» |
| prototype, 10 seeds | 0 | 560 | — | `d594c835bd0628991f8f44de7bd3e188` | **4574** / 0 | «измеряет то, что должна» |

The pristine 3-seed MD5 equals the "after" reading TZ-48's report recorded for its own
committed file.

**The full diffs.** `python3 /tmp/tz49/h/cmp.py pre post` compares the outputs raw, then with
the interleaved numpy `RuntimeWarning` removed. That warning goes to stderr and lands at a
buffer-dependent offset. It occurs twice on every side, and the stripped comparison is the
readable one. 3 seeds:

```
raw: /tmp/tz49/base_lab3.txt 133 lines md5 c05f2a83e0c168c8cd7777ce5393be24 | /tmp/tz49/proto_lab3.txt 133 lines md5 e945abf0f9665d3461941b7bfba139ec | identical False
warning occurrences: 2 | 2
stripped: identical False
stripped diff lines (-/+ only): 4
--- pre
+++ post
@@ -122 +122 @@
-     --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 233
+     --regime-gate: полей 1661, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 237
@@ -127 +127 @@
-  E сравнений 4254, отказов 0 ОК
+  E сравнений 4266, отказов 0 ОК
```

10 seeds:

```
raw: /tmp/tz49/base_lab10.txt 231 lines md5 ecb32dfb6e70c617234ec91657cd3e07 | /tmp/tz49/proto_lab10.txt 231 lines md5 d594c835bd0628991f8f44de7bd3e188 | identical False
warning occurrences: 2 | 2
stripped: identical False
stripped diff lines (-/+ only): 4
--- pre
+++ post
@@ -220 +220 @@
-     --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 233
+     --regime-gate: полей 1661, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 237
@@ -225 +225 @@
-  E сравнений 4562, отказов 0 ОК
+  E сравнений 4574, отказов 0 ОК
```

**Accounting against §5 item 5, figure by figure:**

| Figure | Move | Accounted for by §5 item 5? |
|---|---|---|
| `добавлено раздела слова монеты` | 233 → 237 | **yes**: §4.5 prints 4 lines |
| `--regime-gate: полей` | 1649 → 1661 | **no**: §4.1's records, 6 × 2 extra leaves |
| `E сравнений` | 4254 → 4266 and 4562 → 4574 | **no**: the same 12, added by `chk_n(gq["cmp"], …)` |
| every other figure, every other section, exit code, verdict | none | — |

**The +12 attributed** (`python3 /tmp/tz49/h/e3_attrib.py <bench dir>`, section D's world
built exactly as `lab_selftest` builds it). Pristine:

```
module /tmp/tz49/pristine/bench · agree type dict · len 6 · agree_dates 83
agree as built: {"('trend', 'диапазон')": 44, "('range', 'диапазон')": 33, "('stress', 'диапазон')": 3, "('stress', 'тренд')": 1, "('trend', 'тренд')": 1, "('range', 'тренд')": 1}
_out_fields leaves: total 1649 · under agree 6 · _out_diff(sg, sg) cmp 1649
```

Prototype:

```
module /tmp/tz49/proto/bench · agree type list · len 6 · agree_dates 83
agree as built: [{"marketRegime": "range", "btc_regimes": "диапазон", "n": 33}, {"marketRegime": "range", "btc_regimes": "тренд", "n": 1}, {"marketRegime": "stress", "btc_regimes": "диапазон", "n": 3}, {"marketRegime": "stress", "btc_regimes": "тренд", "n": 1}, {"marketRegime": "trend", "btc_regimes": "диапазон", "n": 44}, {"marketRegime": "trend", "btc_regimes": "тренд", "n": 1}]
_out_fields leaves: total 1661 · under agree 18 · _out_diff(sg, sg) cmp 1661
same summary, agree in the pre-TZ-49 tuple-keyed shape: total 1649 · under agree 6
difference in leaves: 12 = 6 records × (3 − 1)
```

1649 and 1661 are exactly the two E3 readings. **Every unit of the moved count lives under
`agree`.**

**§4.2–§4.5 without §4.1 move the lab exactly as §5 item 5 says.** Control 2b's module is the
prototype with §4.1 undone (item 9). Its 3-seed lab against the pristine run:

```
raw: /tmp/tz49/base_lab3.txt 133 lines md5 c05f2a83e0c168c8cd7777ce5393be24 | /tmp/tz49/c2b_lab3.txt 133 lines md5 936cc1e2ff907bede4cbe0f84e98c4ff | identical False
warning occurrences: 2 | 2
stripped: identical False
stripped diff lines (-/+ only): 2
--- pre
+++ post
@@ -122 +122 @@
-     --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 233
+     --regime-gate: полей 1649, расхождений 0, пропало 0, добавлено 0 · строк отчёта 250, расхождений 0, добавлено раздела слова монеты 237
```

The nested-map copy (reading B) produced the **same bytes** (`936cc1e2…`).

**The item fails**: section E's comparison count is not unchanged at either seed count. This
is the block (`## Status`).

### Item 7 — `regime_gate_summary` on a synthetic world: dump, reload, compare (prototype)

**The world** is section D's own: `synth_hl("normal")`, 16 coins × 16 000 h, seed 3, with its
first coin `C00` written as `BTC`. It was written as a cache by `/tmp/tz49/h/mkcache.py`,
using each module's own generator, and the cache MD5 lists of the two sides are identical.

**The run** is `python3 /tmp/tz49/h/harness.py <module dir> --regime-gate`. It calls the
module's own `main()` with `--html`/`--bot` pointed at the extract, with **one substitution**:
`reconcile`, which fetches the live gist, returns every cached symbol as `clean`. The summary,
both printers and the write are all `main()`'s. A wrapper records the object
`regime_gate_summary` returned.

```
HARNESS: {"mode": "--regime-gate", "extra": [], "exit": 0, "exc": null, "wall_s": 109.7, "artifact": "regime_gate_raw.json", "exists": true, "bytes": 37390, "md5": "ddf168ec5ed033285377a4b2e4858bb3", "parses": true, "nonfinite_tokens": 27, "t_market_rgs_s": 31.4, "t_coin_rgs_s": 34.87, "t_census_s": 0.29, "agree_type": "list", "agree_len": 6, "agree_dates": 83, "strict_equal": false, "agree_strict_equal": true, "text_roundtrip": true, "redump_equal": true, "strict_diff_kinds": {"keys(int->str)": 2, "nan": 27, "tuple": 96}, "strict_diff_first": [["trunc", "keys [48, 72, 96] vs ['48', '72', '96']"], ["cells/48|1.5|long|range/omega", "nan vs nan"], ["cells/48|1.5|long|range/omega_ci", "tuple vs list"], ["cells/48|1.5|long|range/omega_ci/0", "nan vs nan"], ["cells/48|1.5|long|range/omega_ci/1", "nan vs nan"], ["cells/48|1.5|long|range/calib_ci", "tuple vs list"]], "maxrss_self_kb": 302304, "maxrss_children_kb": 302304}
```

- **Written, 37 390 bytes, and it parses.** `main()` returned 0.
- **Agreement records: 6** over 83 dates. They reload `==` to the records dumped. The printed
  table is:

  ```
  СОГЛАСИЕ РАЗМЕТЧИКОВ · marketRegime × btc_regimes · дат 83
  Счёт, и только счёт: btc_regimes не тронут, тезисом не является и
  ничего не подключает (§3.3).
    range    × диапазон   33
    range    × тренд      1
    stress   × диапазон   3
    stress   × тренд      1
    trend    × диапазон   44
    trend    × тренд      1
  ```

- **Round trip, as JSON: holds.** `json.dumps(json.load(file))` is the file's text, and
  `json.dumps(summary)` is the file's text.
- **Round trip, as Python `==` on the whole object: does not hold, and cannot on any non-empty
  summary.** The comparison records 125 differences, none under `agree`:
  - the int horizon keys of `trunc` and `pop_dates` come back as strings (2);
  - every `*_ci` tuple comes back as a list (96);
  - NaN is unequal to itself (27).

  This is finding 2 under `## Status`.

The four extremes of control 4 were also written, reloaded and printed on the prototype (§6 control 4 below).

### Item 8 — the same on the pre-change module

The same harness, cache and command, with the pristine module:

```
HARNESS: {"mode": "--regime-gate", "extra": [], "exit": 1, "exc": "TypeError: keys must be str, int, float, bool or None, not tuple", "wall_s": 109.6, "artifact": "regime_gate_raw.json", "exists": true, "bytes": 36735, "md5": "4409608aa3c5ed0c206a27914dc4a89d", "parses": "JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 36736 (char 36735)", "nonfinite_tokens": 27, "t_market_rgs_s": 31.96, "t_coin_rgs_s": 34.85, "t_census_s": 0.33, "agree_type": "dict", "agree_len": 6, "agree_dates": 83, "maxrss_self_kb": 302788, "maxrss_children_kb": 302788}
```

- **The exception is `TypeError: keys must be str, int, float, bool or None, not tuple`.** It
  is raised from `json.dump` at `backtest_bench.py:5720`.
- **The file left on disk is 36 735 bytes and does not parse.** It stops at the first byte of
  the tuple-keyed `agree`, so the file ends `… "agree": {`. Everything before `agree` is there;
  `agree`, `agree_dates` and `verdict` are not.

So the repair had something to repair (§5 item 2, inv. 45). The stdout of the two sides differs
in exactly two places: the four §4.5 lines (added) and the 15-line traceback the harness
printed for the exception (gone). Both runs print the same agreement table and the same two
verdicts: «ТЕЗИС УСТОЯЛ на 19 сравнениях» for the market word, and «decidable: true — тезис
устоял на 18» for the coin word.

The pre-change module fails the same way on control 4's two non-empty extremes. It raises
`TypeError … not tuple` and leaves 3 359 and 2 504 bytes of unparseable JSON. **On a world with
no dates it does not raise at all**, because an empty dict serialises. A pre-fix control needs a
non-empty world to show the defect.

### Item 9 — both §6 inversions, against the written partition

Each inversion is an exact-string mutation of the **prototype** file, written by
`/tmp/tz49/h/mutate.py <variant> <src> <dst>`. The script asserts that each replaced string
occurs exactly once, so a mutation that matched nothing would have stopped it.

**Inversion 1 — the pin under a wrong expected list** (`own` removed). The scratch guard differs
from the prototype guard in one line
(`diff /tmp/tz49/c1tree/bench/backtest_guard_bench.py /tmp/tz49/proto/bench/backtest_guard_bench.py`):

```
899c899
<    == ['anchor', 'anchorDist', 'anchorStop', 'g', 'p', 'pA', 'tgt',
---
>    == ['anchor', 'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt',
```

Command, from a repository-shaped copy: `python3 /tmp/tz49/c1tree/bench/backtest_guard_bench.py
/tmp/tz49/proto/bench/backtest_bench.py /tmp/tz49/proto/index.html`. Exit 1, 4 s:

```
E. venue-as-observation: 32 comparisons
F. anchored production arm: 29 comparisons
G. D4 partition: 63 comparisons
H. transport: 107 comparisons
I. attribution: 95 comparisons
J. gap in UTC: 8 comparisons
K. comparability: 11 comparisons
checks run: 488   FAIL 1
  FAIL: 33. and the key set of `prod` on the same answer is exactly the registered one  [['anchor', 'anchorDist', 'anchorStop', 'g', 'own', 'p', 'pA', 'tgt', 'waiting']]
```

**Red on the pin, and on nothing else.** The section lines equal the prototype's. The `info`
field prints the key list the driver actually returned, which is §4.3's nine. Inversion 1
changes only the guard, and `--selftest` and `--lab-selftest` do not read the guard. Their
readings for this inversion are therefore the prototype's own runs on the unchanged module
(items 5 and 6): byte-identical selftest, and a lab at exit 0 with its verdict line.

(The first attempt, with the scratch guard outside a repository-shaped tree, died in section I
on `FileNotFoundError: '/tmp/tz49/c1/../main.py'`. `## Deviations` item 3.)

**Inversion 2 — `_rg_agree` returns its pre-TZ-49 tuple-keyed dict.** Two variants were run,
because the literal one cannot satisfy the partition:

- **2a, as §6 writes it:** only `_rg_agree`'s return reverted to `return cell, len(seen)`.
- **2b:** 2a plus `report_regime_gate`'s loop reverted to
  `for (w1, w2), n in sorted(sm["agree"].items())`. Measured with `diff`, 2b's `_rg_agree` body
  and `report_regime_gate` from its first line to `v = sm["verdict"]` equal the pristine file's,
  apart from the added docstring paragraph. 2b is §4.1 undone, with §4.2–§4.5 in place.

**The runs, per variant.**

- **Round trip:** `main --regime-gate` through the item 7 harness on the same cache.
- **Guard:** the prototype guard against the scratch module.
- **`--selftest --seeds 10` and `--lab-selftest`:** run from the scratch directory.

| Run | 2a — `_rg_agree` only (as written) | 2b — `_rg_agree` + printer loop |
|---|---|---|
| round trip through `main()` | exit 1, **`TypeError: tuple indices must be integers or slices, not str` in `report_regime_gate`**, before the write; no file | exit 1, **`TypeError: keys must be str, int, float, bool or None, not tuple` in `_dump_raw`**; no file; stdout up to the write byte-identical to the prototype's |
| direct write of control 4's two non-empty worlds | `TypeError … not tuple`, no file | `TypeError … not tuple`, no file |
| guard | 488 / FAIL 0 (output = prototype's, `dce1626a…`) | 488 / FAIL 0 (output = prototype's, `dce1626a…`) |
| `--selftest --seeds 10` | exit 0, byte-identical (`888b31de…`) | exit 0, byte-identical (`888b31de…`) |
| `--lab-selftest` | **exit 1** at E3 `printed(report_regime_gate, sg0)`, `TypeError: tuple indices must be integers or slices, not str`; A–D and E0–E2 printed, no verdict line | exit 0, «измеряет то, что должна»; `E сравнений 4254` |

**Against the written partition:**

| | Item | Required | Inversion 1 | Inversion 2a (as written) | Inversion 2b |
|---|---|---|---|---|---|
| Must turn red | the §4.3 pin under a wrong expected list | red | **red** (FAIL 1, that check) | — | — |
| Must turn red | the §5 item 1 round-trip under tuple keys | red | — | **red**, but in the printer (`main()`); red at the write when written directly | **red, at the write** |
| Must NOT fire | every other guard check | green | **green** (487 others) | **green** (488 / 0) | **green** (488 / 0) |
| Must NOT fire | `--selftest` | green | **green** (module unchanged) | **green** | **green** |
| Must NOT fire | `--lab-selftest` | green | **green** (module unchanged) | **RED — exit 1 in E3** | **green** |

Inversion 2 as §6 writes it breaks one row, and the break is the printer rather than the
serialisation. The lab cannot stay green while its E3 prints a tuple-keyed table through a
printer that reads records. **2b satisfies every row.** The tree was never touched by either
inversion, which ran on scratch copies outside the repository. Their MD5s are under
`## Fingerprints`, and the three files in scope read their §0 fingerprints at the end.

### Item 10 — the CI negative test (contract §9) — **not run, therefore failed**

A negative test forces a real failure in a pushed implementation and reads the hosted job red.
The run was BLOCKED before an implementation commit or a branch existed, so there was nothing
to push a forced failure onto. Contract §9 counts an item that was not run as failed, and it is
reported as failed here.

### Item 11 — hosted `Bench gate` on the implementation commit — **not run, therefore failed**

There is no implementation commit, so no run exists to read. `gh` is present and logged in as
`seahomebatumi-ai` (`gh auth status`). It was used here only to read pull request #40's state.

### Item 12 — no-regression statement

**In the repository: nothing moved.** No file was modified, and the report is the only file
this session adds.

**On the prototype**, the statement the TZ asks for:

- **`index.html` and `main.py` did not move.** Their MD5s are identical in both extracts and
  equal the map's table (`4e71da9b…`, `0e3ead8c…`).
- **No other bench and no other workflow moved.** `diff -rq` between the extracts names only
  `bench/backtest_bench.py`, `bench/backtest_guard_bench.py` and
  `.github/workflows/backtest_bench.yml`.
- **Every printed figure of `--target`, `--stops`, `--run` and `--regimes` did not move**, and
  neither did `--res7`'s. Each mode ran through `main()` on section D's world as a cache, once
  per module, with the harness of item 7. Stdout and artifact bytes were then compared
  (`python3 /tmp/tz49/h/cli_table.py`):

| Mode (`main()` argv) | Exit pre / post | Stdout pre = post | Stdout lines | Artifact | Bytes | Artifact MD5 pre = post |
|---|---|---|---:|---|---:|---|
| `--stops --horizon 7 --step 7` | 0 / 0 | **identical** (`8d2200f2…`) | 27 | `stops_raw.json` | 2 540 | **identical** (`7a147a3d…`) |
| `--run --horizon 7 --step 7` | 0 / 0 | **identical** (`1f22443f…`) | 33 | `run_raw.json` | 388 645 | **identical** (`210ceb1c…`) |
| `--regimes --horizon 7 --step 7` | 0 / 0 | **identical** (`bedaa2ba…`) | 29 | `regimes.json` | 6 588 | **identical** (`7aa04c74…`) |
| `--res7 --horizon 7 --step 7` | 0 / 0 | **identical** (`6754e6e2…`) | 33 | `res7_dates.json` | 1 804 | **identical** (`45b7b6c5…`) |
| `--target` | 0 / 0 | **identical** (`71a1b585…`) | 105 | `target_raw.json` | 9 139 | **identical** (`ef816191…`) |
| `--regime-gate` | **1 / 0** | differs by the §4.5 lines and the traceback (item 8) | 513 / 502 | `regime_gate_raw.json` | 36 735 / 37 390 | differs: truncated pre, whole post |

The runs are real rather than refusals:

- `--stops`: 1215 setups per side;
- `--run` and `--regimes`: 82 dates × 15 coins;
- `--target`: «сверено монет 16 · исключено 0 · в рукава идёт 15». The 16 is the harness's
  `reconcile` stub counting the cache, not a reconciliation.

`--selftest` did not move either (item 5).

### §5 — the six shapes, on the prototype

| # | Shape | Reading |
|---|---|---|
| 1 | `regime_gate_raw.json` written, parses, round-trips, agreement records included | written (37 390 B), parses, records `==`, text round-trips; **whole-object Python `==` false** (item 7, finding 2) |
| 2 | the same object raises `TypeError` on the pre-fix module | **holds**: `TypeError: keys must be str, int, float, bool or None, not tuple`, 36 735 B truncated (item 8) |
| 3 | `report_regime_gate`'s text byte-identical | **holds**: lab E3 `строк отчёта 250, расхождений 0` compares it inside one module; across modules, the `--regime-gate` stdout differs only by §4.5's lines and the pre side's traceback (item 8); and on all four control 4 extremes the whole printed text is byte-identical between the pristine and prototype modules |
| 4 | guard total +1 exactly, no other result changes | **holds**: 487 → 488, FAIL 0 both, one added check, by name, every other name and result aligned (item 3) |
| 5 | lab moves in exactly one figure | **does not hold**: two more figures move, +12 each (item 6) — the block |
| 6 | a failed serialisation leaves no file | **holds**: `_dump_raw({'agree': {('range', 'тренд'): 1}}, 'regime_gate_raw.json')` in an empty directory raised `TypeError … not tuple` and left the directory empty (`[]`); through `main()`, control 2b's write raised and no file existed |

### §6 control 4 — extremes of the agreement table

`python3 /tmp/tz49/h/extremes.py <module dir>`. Each world is built with the guard's own
fixture shape (`rg_obs` / `rg_date`, copied from `backtest_guard_bench.py:659–672`), then
summarised by `regime_gate_summary`, written through the module's artifact write into a fresh
directory, reloaded and printed through `report_regime_gate`:

| World | Module | Summary `agree` | Write | File after | Reload / text round trip | `report_regime_gate` |
|---|---|---|---|---|---|---|
| no dates (`by_H` = `{}`) | prototype | `[]`, 0 dates | ok | 299 B | `==` / yes | ok, MD5 `d496cb83…` |
| no dates (every horizon `[]`) | prototype | `[]`, 0 dates | ok | 13 962 B | `==` / yes | ok, MD5 `05b20176…` |
| every date unmarked (12 dates, `btc` without prices) | prototype | `[{range, нет метки, 6}, {trend, нет метки, 6}]` | ok | 3 659 B | `==` / yes | ok, MD5 `b10012a1…` |
| a single pair (1 date, labelled) | prototype | `[{range, диапазон, 1}]` | ok | 2 699 B | `==` / yes | ok, MD5 `e7d996cd…` |
| no dates (`{}`) | pristine | `{}` | ok | 299 B | `==` / yes | ok, `d496cb83…` |
| no dates (every horizon `[]`) | pristine | `{}` | ok | 13 962 B | `==` / yes | ok, `05b20176…` |
| every date unmarked | pristine | tuple-keyed, 2 keys | **`TypeError … not tuple`** | **3 359 B, unparseable** | — | ok, `b10012a1…` |
| a single pair | pristine | tuple-keyed, 1 key | **`TypeError … not tuple`** | **2 504 B, unparseable** | — | ok, `e7d996cd…` |

**Each extreme serialises and prints on the prototype.** The printed text of
`report_regime_gate` is byte-identical to the pristine module's on all four worlds, and the
MD5s cover the whole printed text, not only the agreement block. Printed agreement blocks,
prototype:

```
СОГЛАСИЕ РАЗМЕТЧИКОВ · marketRegime × btc_regimes · дат 0
Счёт, и только счёт: btc_regimes не тронут, тезисом не является и
ничего не подключает (§3.3).
---
СОГЛАСИЕ РАЗМЕТЧИКОВ · marketRegime × btc_regimes · дат 12
Счёт, и только счёт: btc_regimes не тронут, тезисом не является и
ничего не подключает (§3.3).
  range    × нет метки  6
  trend    × нет метки  6
---
СОГЛАСИЕ РАЗМЕТЧИКОВ · marketRegime × btc_regimes · дат 1
Счёт, и только счёт: btc_regimes не тронут, тезисом не является и
ничего не подключает (§3.3).
  range    × диапазон   1
```

(Both no-date worlds print the first block.)

### §7 reading item 1 — are the other five artifact JSONs writable?

Yes, all five, on this world, through `main()`, on both modules (item 12's table). Every file
was written in full and parses, and none carries a non-finite token:

| Artifact | Bytes | Parses | Bare `NaN`/`Infinity` tokens |
|---|---:|---|---:|
| `stops_raw.json` | 2 540 | yes | 0 |
| `run_raw.json` | 388 645 | yes | 0 |
| `regimes.json` | 6 588 | yes | 0 |
| `res7_dates.json` | 1 804 | yes | 0 |
| `target_raw.json` | 9 139 | yes | 0 |
| *`regime_gate_raw.json` (prototype)* | *37 390* | *yes* | ***27*** |

**What this does and does not show.** It covers one world. `run_raw.json` is 388 KB of
per-date records, so a numpy integer anywhere in `run_walk`'s output would have raised, and
none did. It does not show that no world can produce a non-finite value in `stops_raw.json` or
`target_raw.json`: the map's watched row (§10) already records `NaN` for a pooled arm with zero
stop touches, and this world has none. **Nothing was repaired.**

**One new fact for the next TZ.** Once `regime_gate_raw.json` becomes writable, it carries bare
`NaN`: 27 tokens here. They are Ω and both of its interval bounds on 9 pooled cells, all at RR
1.5 on the long side, where no setup touched a stop or a target (`n_stop` 0, `n_tgt` 0).
Python's `json` reads it back. A strict parser does not. This is the same class as the watched
`target_raw.json` row, now on a second artifact.

### §7 reading item 2 — what the coin-word section costs, locally

From the item 7 run: the prototype `--regime-gate` on section D's world as a cache, 15 coins
in the grid, 83 dates, six horizons. Timings are wrappers around the module's own functions:

| Call | Seconds |
|---|---:|
| `regime_gate_summary(by_H, btc, …)`, the market word | 31.40 |
| `regime_gate_summary(by_H, None, …, splitter=_own_split)`, the coin word **without** the census | 34.87 |
| `own_census(…)` alone | 0.29 |
| `own_regime_summary`, the coin word **with** the census (sum of the two above) | 35.16 |

The pre-change module read 31.96 / 34.85 / 0.33 on the same world.

**Peak resident size: 302 304 KB** (`resource.getrusage(RUSAGE_SELF).ru_maxrss`) for the whole
process, which includes the six `run_regime_grid` passes. `RUSAGE_CHILDREN` printed the same
figure. That is expected: a child forked from Python carries the parent's resident pages until
`exec`, so the children figure is not a node measurement.

The archive figure is not asked for and is not inferable from this pair.

## Test Results

| Item | What | Result |
|---|---|---|
| 1 | `py_compile`, both files | exit 0, exit 0 |
| 2 | workflow step list | one step moved (12 → 18), one condition changed; the other 18 steps equal as parsed |
| 3 | guard | 487 → **488 / FAIL 0**, +1 attributed by name (one added check, call #143) |
| 4 | `verify_bench.py` | 59 / FAIL 0, byte-identical |
| 5 | `--selftest --seeds 10` | exit 0, byte-identical, 36 comparisons both sides |
| 6 | `--lab-selftest`, 3 and 10 seeds | exit 0 both; **section E 4254 → 4266 and 4562 → 4574 — FAILS as registered** |
| 7 | round trip, prototype | written 37 390 B, parses, 6 records `==`, text round-trips; whole-object `==` false for reasons outside `agree` |
| 8 | pre-change module | `TypeError` (tuple keys), 36 735 B truncated on disk |
| 9 | both inversions | inversion 1 red on the pin alone (488 / FAIL 1); inversion 2 as written turns the round trip red but **crashes `--lab-selftest`** (2a); with the printer reverted too (2b), every row reads as registered |
| 10 | CI negative test | **not run — failed** (no implementation commit) |
| 11 | hosted `Bench gate` | **not run — failed** (no implementation commit) |
| 12 | no-regression | nothing in the repository moved; on the prototype, five modes byte-identical in stdout and artifact |

## Deviations

Four, all disclosed.

1. **A prototype was built and measured, then discarded** (contract §12: "Do not partially
   implement around a blocker without saying so"). The blocker is a property of §4.1's shape
   against §5 item 5. Measuring it on the whole prototype confirmed it and checked every other
   item, so a corrected TZ can change the two clauses and apply the rest. The diff is saved at
   `/tmp/tz49/proto.diff` (187 lines, MD5 `19ac76813d064198b92fb4f4180f17b0`), and every file in
   scope is back at its §0 fingerprint.
2. **Items 7, 8 and 12 ran `main()` with `reconcile` replaced.** `reconcile` fetches the live
   gist, and a session fetch may not stand behind a product fact (hard-floor item 9). The
   substitute returns every cached symbol as `clean` and touches nothing else. None of these
   runs produces a product figure: the world is synthetic and the purpose is a pre/post
   comparison.
3. **Control 2 was run in two variants, and control 1 twice.**
   - Control 2 as written cannot satisfy its partition row, so a second variant that also
     reverts the printer loop was run, and both are reported.
   - Control 1's first run placed the scratch guard outside a repository-shaped tree. The guard
     reads `HERE/../main.py` (`:2001`), so that run died with `FileNotFoundError` in section I
     (`/tmp/tz49/c1_guard.txt`). That is a harness error, not a reading. The re-run placed the
     copy at `/tmp/tz49/c1tree/bench/` beside copies of `main.py` and `index.html`.
4. **§4.4 added four Russian comment lines** above the moved step, beyond the step and its
   condition. A YAML parser does not see them, and item 2 compares the parsed documents.

## Pre-existing Issues

- **The defect TZ-49 §1 describes is live on `main`.** Item 8 re-measured it on `d9934f6`: the
  `--regime-gate` write raises `TypeError` and leaves 36 735 bytes of unparseable JSON, ending
  `… "agree": {`.
- **The map's `## 0` prose still gives `bench/backtest_bench.py` as 5102 lines /
  `ba633202…`.** That is the pre-TZ-48 figure. The file reads 5795 / `ed4db7c2…` since pull
  request #40 merged, which is TZ-49 §0's own figure. The map's revision `2026-09-16-b`
  predates that merge. It is reported, not acted on (contract §5). Every other bench figure the
  prose carries reads as stated: `backtest_guard_bench.py` 2503 / `bfc984b1…`, `verify_bench.py`
  540 / `28eb1949…`, `journal/write.js` 849 / `19722fb5…`, `journal_bench.js` 1177 / `993271f4…`.
- **TZ-49 §4.1's reader census is short by one.** Lab E3 reads `agree` twice: through
  `_out_fields` (`:5065`) and by printing it (`:5070`). That is the root of the block and of
  finding 1.
- **TZ-49 §4.2's gloss is imprecise in two places.** One of "the two `JsBridge` job writes" is
  `JsScorer.score` (`:217`), and the two cache writes (`:938`, `:3113`) do not carry
  `allow_nan=False`. The site count, six, is exact.
- **`--lab-selftest` and the guard print a numpy `RuntimeWarning: All-NaN slice encountered`
  on stderr**, twice per lab run and once per guard run. Under `2>&1` it lands at
  buffer-dependent offsets, so a raw byte comparison of two lab outputs can differ where the
  stdout text does not.

## Remaining Risks

- **`_dump_raw` leaves a stale file intact on failure.** The old `open(path, "w")` truncated the
  target before serialising. The new helper opens the file only after `json.dumps` succeeds, so
  a failed run leaves any earlier file at that path untouched. On a runner the checkout is fresh
  and §5 item 6 holds literally. In a directory where an earlier run succeeded, a later failed
  run leaves the earlier artifact, which can be read as the new one. §4.2 specifies exactly this
  helper, so the prototype did not add a removal.
- **`regime_gate_raw.json` will carry bare `NaN` once it is writable** (27 tokens on section D's
  world). It is the same class as the map's watched `target_raw.json` row, and a strict JSON
  reader will refuse the artifact.
- **Reading item 1 covers one synthetic world.** A world that produces `NaN` or a numpy scalar
  in `stops_raw.json`, `run_raw.json`, `regimes.json` or `res7_dates.json` was not constructed.
- **The prototype's `!cancelled()` condition has no runner reading.** `backtest_bench.yml` runs
  only on dispatch, and none was made.

## Commit

One commit, on `main`, on the `CryptoReports/**` direct-push path (contract §8). The workflow
filters were read before the push:

- `bench.yml`'s `push` carries `'**.md'` under `paths-ignore`;
- `main.yml`'s `push` is a `paths` allow-list of exactly `main.py` and
  `.github/workflows/main.yml`;
- `calib.yml`'s `push` fires only on `claude/**` branches, for two named paths;
- `journal.yml` triggers on `schedule` and `workflow_dispatch`, and `backtest_bench.yml` on
  `workflow_dispatch` only.

Message:

```
docs(reports): TZ-49 — BLOCKED, §4.1's agreement records move section E's comparison count, which §5 item 5 registers as unchanged (TZ-49)

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

Contents: `CryptoReports/TZ-49-raw-json-and-prod-pin-report.md`, added.

No hash appears here. This report's own commit has not been made at the time of writing
(inv. 54, contract §10).

## Pull Request

None. By class this is a branch TZ, but the run was BLOCKED before any deliverable was
committed. No implementation commit, branch or pull request exists. The report-only fixed line
is not used, because it would assert a class this TZ does not have.

## CI Execution

No workflow ran on a runner for this task. No branch was pushed, so nothing could trigger one.
Every bench reading in this report is a local run in this session's container. That includes
the guard's 488, `verify_bench`'s 59, both lab runs and every `main()` mode.

## Final Repository State

This session leaves the working tree clean at `eb7c18c24bb74bfd5338760331791022a8e4a35d`, which
is `origin/main` after the second `git fetch --all --prune`. `git status --porcelain --ignored`
printed nothing.

Main moved once during the session, `d9934f6` → `eb7c18c` ("update live.json"). The worktree
was fast-forwarded to it. `git diff --stat d9934f6 eb7c18c` names `analyst/live.json` alone,
which no fingerprinted file, bench or prototype reads. Every figure in this report was measured
on `d9934f6`. The fingerprint tables and the gate output were re-measured at `eb7c18c` and are
identical (`/tmp/tz49/q/fingerprints_eb7c18c.txt`, `/tmp/tz49/q/gate_eb7c18c.txt`).

The prototype was discarded with `git checkout --`, and `bench/__pycache__/`, the one ignored
artifact this session created, was removed. Everything measured lives outside the repository,
under `/tmp/tz49`:

- the prototype diff, both extracts, the harness and the probes;
- every run output.

The MD5s are listed under `## Fingerprints`. No branch was created or pushed.

Nothing awaits a merge from this TZ, so "NOT IN EFFECT UNTIL MERGED" has no referent and is not
written.

## Fingerprints

Measured on `d9934f6c3e6acf4ce4542788b9f8516b3490e9e9` (`origin/main` after the first fetch),
after the prototype was discarded. Re-measured on `eb7c18c24bb74bfd5338760331791022a8e4a35d`
(`origin/main` after the second fetch), where every figure below is identical.

**System Map.** `SYSTEM-MAP-CRYPTOCALCUL.md`: **2759 lines, MD5
`7f8fd2e8e553109cb7cffed329bd56e1`**. Revision string in its `## 0`: `**Revision 2026-09-16-b.**`.
TZ-49 requires `**Revision 2026-09-16-b.**`, so they are **equal**.

**Anchors (contract §5 step 2).** The list was cut from the map's anchor table by structure: the
header row beginning `| Anchor |`, its separator, and every following line that begins with `|`.
**The table has 7 rows, and 7 anchors were compared.** `python3 /tmp/tz49/gate.py .` (MD5
`b5efc63b04ba02853efe240aa77bd5fe`) printed, per anchor, the offset and text each fixed-string
match returned in the map and in the TZ, and whether the TZ carries the map's row verbatim:

```
$ python3 /tmp/tz49/gate.py .
anchor table rows (structural cut): 7
map revision string: **Revision 2026-09-16-b.**
TZ requires: **Revision 2026-09-16-b.**
--- revision
  map  find: 622 -> '**Revision 2026-09-16-b.**'
  TZ   find: 505 -> '**Revision 2026-09-16-b.**' | TZ row verbatim: True
--- direction engine
  map  find: 13661 -> '### 3.12 Direction engine — veto cascade'
  TZ   find: 814 -> '### 3.12 Direction engine — veto cascade' | TZ row verbatim: True
--- catalyst registry
  map  find: 13728 -> '### 3.15 Catalyst registry'
  TZ   find: 881 -> '### 3.15 Catalyst registry' | TZ row verbatim: True
--- exhaustion measure
  map  find: 13782 -> '### 3.16 List exhaustion — the day-range measure'
  TZ   find: 935 -> '### 3.16 List exhaustion — the day-range measure' | TZ row verbatim: True
--- analytical engine
  map  find: 13857 -> '## 11. Analytical engine'
  TZ   find: 1010 -> '## 11. Analytical engine' | TZ row verbatim: True
--- squeeze block
  map  find: 13904 -> "### 3.17 «РИСК ВЫНОСА» — the day's own risk"
  TZ   find: 1057 -> "### 3.17 «РИСК ВЫНОСА» — the day's own risk" | TZ row verbatim: True
--- newest invariant
  map  find: 13973 -> '71. **A measurement that is not RETAINED was not taken,'
  TZ   find: 1126 -> '71. **A measurement that is not RETAINED was not taken,' | TZ row verbatim: True
anchors compared: 7 of table rows: 7
file table rows: 4
  map row: | `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | | quoted in TZ: True
  map row: | `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | | quoted in TZ: True
  map row: | `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | | quoted in TZ: True
  map row: | `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | | quoted in TZ: True
```

The same seven, by `grep -nF` against the map (each match prints the matched line):

```
$ grep -nF -- '**Revision 2026-09-16-b.**' SYSTEM-MAP-CRYPTOCALCUL.md
17:**Revision 2026-09-16-b.** Baseline: one report-only TZ, one methodology revision and one
189:| revision | `**Revision 2026-09-16-b.**` |
$ grep -nF -- '### 3.12 Direction engine — veto cascade' SYSTEM-MAP-CRYPTOCALCUL.md
190:| direction engine | `### 3.12 Direction engine — veto cascade` |
1101:### 3.12 Direction engine — veto cascade
$ grep -nF -- '### 3.15 Catalyst registry' SYSTEM-MAP-CRYPTOCALCUL.md
191:| catalyst registry | `### 3.15 Catalyst registry` |
1484:### 3.15 Catalyst registry — `catalysts.json`
$ grep -nF -- '### 3.16 List exhaustion — the day-range measure' SYSTEM-MAP-CRYPTOCALCUL.md
192:| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
1581:### 3.16 List exhaustion — the day-range measure
$ grep -nF -- '## 11. Analytical engine' SYSTEM-MAP-CRYPTOCALCUL.md
193:| analytical engine | `## 11. Analytical engine` |
2535:## 11. Analytical engine — `analyst/**`
$ grep -nF -- '### 3.17 «РИСК ВЫНОСА» — the day's own risk' SYSTEM-MAP-CRYPTOCALCUL.md
194:| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
1748:### 3.17 «РИСК ВЫНОСА» — the day's own risk
$ grep -nF -- '71. **A measurement that is not RETAINED was not taken,' SYSTEM-MAP-CRYPTOCALCUL.md
195:| newest invariant | `71. **A measurement that is not RETAINED was not taken,` |
2254:71. **A measurement that is not RETAINED was not taken, and a step that is not CONDITIONED
```

Each anchor matches twice: once in the `## 0` table itself (lines 189–195) and once in the text.
The text matches are the revision at line 17 and the six content anchors at lines 1101,
1484, 1581, 2535, 1748 and 2254. `gate.py`'s offsets are the first match, which is the table
row, so the `grep` lines are the ones that show each anchor present outside the table.

**The map's file table** (all four rows quoted verbatim by the TZ; `wc -l` and `md5sum`):

| File | Lines | MD5 | Map states |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**The files TZ-49's gate adds:**

| File | Lines | MD5 | TZ states |
|---|---:|---|---|
| `bench/backtest_bench.py` | 5795 | `ed4db7c2bab9076e92982c664c6fc2f6` | equal (and `git show 4a11c8b:bench/backtest_bench.py \| md5sum` prints the same) |
| `bench/backtest_guard_bench.py` | 2503 | `bfc984b1d22ec1ad89cf536a1a47c529` | equal |
| `.github/workflows/backtest_bench.yml` | 171 | `703330829c377a15fc0df71e25df92a7` | equal |

**Also read:**

| File | Lines | MD5 |
|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` (Version 23) | 864 | `02abb1969626d2af150a0d1f6e02f2a7` |
| `CryptoTZ/TZ-49-raw-json-and-prod-pin.md` | 320 | `ec33e1ba6b689bd43ef62ff96208c6f9` |
| `bench/verify_bench.py` | 540 | `28eb1949f21d0afadb062303108f7101` |
| `journal/write.js` | 849 | `19722fb53d75b6d25a8f957f74f97422` |
| `bench/journal_bench.js` | 1177 | `993271f44995c8ae21c54935a3f80adf` |

**The prototype and the evidence under `/tmp/tz49`:**

| File | MD5 | What it is |
|---|---|---|
| `/tmp/tz49/proto.diff` | `19ac76813d064198b92fb4f4180f17b0` | the prototype, 187 lines |
| `/tmp/tz49/base_guard.txt` | `d91178acbed79648100d6b07b2f88c2c` | guard, pristine |
| `/tmp/tz49/proto_guard.txt` | `dce1626ab1b43ac21afd3d526b65ed3b` | guard, prototype (and 2a, 2b: same bytes) |
| `/tmp/tz49/c1_guard.txt` | `f8c40d4d93198e37ec370ff53b2e1e85` | inversion 1, first attempt (harness error) |
| `/tmp/tz49/c1_guard_rerun.txt` | `7bbd06696b26fcdce1c68fee22d222ce` | inversion 1 |
| `/tmp/tz49/base_verify.txt` | `4dff115f3f0595d2fe74d99cf4052422` | verify_bench, pristine |
| `/tmp/tz49/proto_verify.txt` | `4dff115f3f0595d2fe74d99cf4052422` | verify_bench, prototype |
| `/tmp/tz49/base_selftest.txt` | `888b31de3f1f77380b23e179bca32c2a` | selftest, pristine |
| `/tmp/tz49/proto_selftest.txt` | `888b31de3f1f77380b23e179bca32c2a` | selftest, prototype |
| `/tmp/tz49/base_lab3.txt` | `c05f2a83e0c168c8cd7777ce5393be24` | lab, 3 seeds, pristine |
| `/tmp/tz49/proto_lab3.txt` | `e945abf0f9665d3461941b7bfba139ec` | lab, 3 seeds, prototype |
| `/tmp/tz49/base_lab10.txt` | `ecb32dfb6e70c617234ec91657cd3e07` | lab, 10 seeds, pristine |
| `/tmp/tz49/proto_lab10.txt` | `d594c835bd0628991f8f44de7bd3e188` | lab, 10 seeds, prototype |
| `/tmp/tz49/c2a_rt.txt` | `6c9baf7a287d94b8eff429dab6884af3` | inversion 2a, main --regime-gate |
| `/tmp/tz49/c2a_selftest.txt` | `888b31de3f1f77380b23e179bca32c2a` | inversion 2a, selftest |
| `/tmp/tz49/c2a_lab3.txt` | `9022a688e3f5d5c96596802c76f78566` | inversion 2a, lab |
| `/tmp/tz49/c2b_rt.txt` | `c67d1e93f038a086e6a1dac3fb8046e8` | inversion 2b, main --regime-gate |
| `/tmp/tz49/c2b_selftest.txt` | `888b31de3f1f77380b23e179bca32c2a` | inversion 2b, selftest |
| `/tmp/tz49/c2b_lab3.txt` | `936cc1e2ff907bede4cbe0f84e98c4ff` | inversion 2b, lab |
| `/tmp/tz49/optB_lab3.txt` | `936cc1e2ff907bede4cbe0f84e98c4ff` | nested map, lab |
| `/tmp/tz49/cli/pre_regimegate.txt` | `eb6eff30cc3e9668bd9b08c328f9d859` | main --regime-gate, pristine |
| `/tmp/tz49/cli/post_regimegate.txt` | `8c90d2bd2d3df96a23991b1944d20b9c` | main --regime-gate, prototype |
| `/tmp/tz49/cli_pre/regime_gate_raw.json` | `4409608aa3c5ed0c206a27914dc4a89d` | the truncated artifact, pristine |
| `/tmp/tz49/cli_post/regime_gate_raw.json` | `ddf168ec5ed033285377a4b2e4858bb3` | the written artifact, prototype |
| `/tmp/tz49/extremes_pristine.txt` | `97c4128aa0e20e8a5644b6342c436f5f` | control 4, pristine |
| `/tmp/tz49/extremes_proto.txt` | `dc01b9f5d9c3dff81d778be8294a1235` | control 4, prototype |
| `/tmp/tz49/extremes_c2a.txt` | `d7e604d77720487ab5083794addbeb2e` | control 4, inversion 2a |
| `/tmp/tz49/extremes_c2b.txt` | `0562e6da20614d5860f130582dcd2ae4` | control 4, inversion 2b |
| `/tmp/tz49/extremes_optB.txt` | `844754e7e19aca80ad30f584fbbc32f7` | control 4, nested map |
| `/tmp/tz49/e3_attrib_pristine.txt` | `f141f66ce5ae83c44e5012b01f16eba3` | E3 leaf count, pristine |
| `/tmp/tz49/e3_attrib_proto.txt` | `d55bc0b00011abe9b6d4ec293742d6e4` | E3 leaf count, prototype |
| `/tmp/tz49/gn/names_pristine.json` | `a119d4498fc6e5dfcee14c661053606c` | guard check names, pristine |
| `/tmp/tz49/gn/names_proto.json` | `742d61487bb3e9a8c40ee347763cce75` | guard check names, prototype |
| `/tmp/tz49/v2_steps.txt` | `4a191d42364681315d57ab939bbf2280` | item 2 step listing |
| `/tmp/tz49/gate.txt` | `3976bdb08a1f4180ee02671e684f1cae` | fingerprint gate |
| `/tmp/tz49/gate_grep.txt` | `a5671c7687b061bc2f36f99c89454dd3` | anchor greps |
| `/tmp/tz49/c2a/backtest_bench.py` | `c1747d53fb90474220a728fbc5974c65` | inversion 2a module |
| `/tmp/tz49/c2b/backtest_bench.py` | `62b91a38cefb20ce50a21585529586fd` | inversion 2b module |
| `/tmp/tz49/optB/backtest_bench.py` | `5b3ddbe2f42eeed6ce926f6d0013c45a` | nested-map module |
| `/tmp/tz49/c1tree/bench/backtest_guard_bench.py` | `cef7296aed116e72731733efce821042` | inversion 1 guard |
| `/tmp/tz49/h/harness.py` | `e4c45148fecdedfbb7a60f1aa7939e9a` | main() harness |
| `/tmp/tz49/h/mkcache.py` | `f151fc65d5bc6f984c257dc05080e1ac` | section D world as a cache |
| `/tmp/tz49/h/extremes.py` | `e32ee556f54e89ced560b64da4c57f31` | control 4 and §5 item 6 |
| `/tmp/tz49/h/mutate.py` | `b42a875cdc78292159bf15a737f17ed8` | inversion writer |
| `/tmp/tz49/h/e3_attrib.py` | `12a78c170881c911900b38d9588f9e6f` | E3 leaf attribution |
| `/tmp/tz49/h/guard_names.py` | `a8949a0a70ee3c755cd4d8d9d8e9d0b1` | guard check-name recorder |
| `/tmp/tz49/h/cmp.py` | `b11852ab3e905d3f5b234e9445f86e55` | output comparator |
| `/tmp/tz49/h/cli_table.py` | `985d33beab0b1ce372f70d5aea0aabad` | item 12 table |
| `/tmp/tz49/h/steps.py` | `438787944b4e65865877757a899cd674` | item 2 listing |
| `/tmp/tz49/gate.py` | `b5efc63b04ba02853efe240aa77bd5fe` | fingerprint gate |
| `/tmp/tz49/q/v1_pycompile.txt` | `6ee643858881481fcb567ea3385f6839` | item 1 output |
| `/tmp/tz49/q/v2_struct.txt` | `fbe3dd47ef88dea6a94706f06d4f33f7` | item 2 structural comparison |
| `/tmp/tz49/q/names_cmp.txt` | `7ed4a0fe3ae6759469234a301ed0960f` | item 3 name comparison |
| `/tmp/tz49/q/cmp_lab3.txt` | `12cfb0f1f05798438e669d08d14b44fa` | item 6 diff, 3 seeds |
| `/tmp/tz49/q/cmp_lab10.txt` | `28b375863148ec609bcd86293d3c44c3` | item 6 diff, 10 seeds |
| `/tmp/tz49/q/cmp_c2b.txt` | `d9cd7a0ae0d27f8ef0da61ba846cbec8` | item 6, inversion 2b against pristine |
| `/tmp/tz49/q/c1_diff.txt` | `9c9d16c3cfbb80d140338cb55f93cb75` | inversion 1 guard diff |
| `/tmp/tz49/q/extreme_blocks.txt` | `fb1b5dcf42925931ea92802fa9e2947b` | control 4 printed blocks |
| `/tmp/tz49/q/fingerprints_eb7c18c.txt` | `4f6d9de3aa63af75949235d01a05859f` | fingerprints re-measured after the second fetch |
| `/tmp/tz49/q/gate_eb7c18c.txt` | `99bec96f2f6668f20b7b3b5e811fdc27` | gate re-run after the second fetch |
| `/tmp/tz49/verify_quotes.py` | `44f40d8553d50b05b1ab0d76901a91e9` | checks every fenced block of this report against the files above |
