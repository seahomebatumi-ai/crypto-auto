# TZ-84 — the card ledger: every card the answer printed, followed as its card says; the card a state gives and the late card's replay in `vps/book.py`; the run names a missing log and a spent window; the trader back on `high`

**Contract:** v33 — `EXECUTOR-INSTRUCTIONS.md` at the repository root, read in full before the sections below.
**Canonical filename:** `CryptoTZ/TZ-84-card-ledger.md`
**Report:** `CryptoReports/TZ-84-card-ledger-report.md`
**Class:** branch TZ (contract §8) — it authorises five repository files besides its report.
**Branch:** `claude/tz-84-card-ledger`
**Host:** the VPS — R1 exists only there.
**Model:** Sonnet 5.5 · medium — the code is §6's patch, written and run by the Architect; the session applies it, runs
the checks and takes one reading, and judges nothing.
**Base:** `main` at `8e85d64` with this delivery's uploads — the map `2026-11-26-c`, the methodology `2026-11-26-b`,
`analyst/owner.json` v6; `vps/` unchanged since `895e7ad`.
**Rests on:** map §10 rows «Every card is a recommendation the record follows», «A run that leaves no log» and «The run
spends its account on reading», and the closed row «A held coin's late entry is the methodology's arithmetic»; inv.
38, 59, 70 and 73.
**Previous TZ:** TZ-83, accepted 26.11.2026, merged at `f50acc6` (pull request #68).
**Trigger:** `EXECUTE TZ-84`, with nothing under it: no credential arrives and the Boss is asked for nothing.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-26-c.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-26-c.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `74. **A chat is handed off only under a marker` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this TZ's gate adds:

| Added file | Lines | MD5 | Required |
|---|---:|---|---|
| `vps/book.py` | 419 | `4e283c02783b4f959c49b613b4e518a5` | equal — §6's patch is written against these bytes |
| `vps/score.py` | 613 | `eb76418a35e4c9389a80e61b1d449387` | equal — the same |
| `vps/run.py` | 394 | `870669d4ab7ce889ad619a2595ccfcc2` | equal — the same |
| `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` | equal — the same |
| `vps/selftest.py` | 4130 | `87fb628b69675afb3c878f29040b9f26` | equal — the same |

The map itself: 2783 lines, MD5 `bc26cde00272340bc1ca03173d809f97` — reported, not enforced.

---

## 1. Goal and scope

**Step 2 of the build order, its scorecard half** (map §10): what the trust line scores becomes the cards the owner
reads, where today it is a book he is never shown.

- **The card ledger, `score-cards/`.** `vps/score.py`'s daily close reads every `CARD|` line of the day logs its
  checkout carries (methodology §12) and follows each card as the card says: `now` at its entry at the freeze;
  `limit` on the first minute after the freeze that reaches it before the day ends — the next recalculation — or
  never; `wait` on the plan's own entry at the next open, which the book makes only where the freeze day closed beyond
  the trigger. A filled `now` or `limit` card's fill day is the part after its fill, read from that day's one-minute
  bars, and from it `book.manage()` follows the card: its stop on a touch, half at its target and the rest's stop at
  its entry, the rest by the channel. One trade a coin, side and fill — the earliest card's; each close written once,
  R by `book.result_r()` on the funding prints (inv. 38, 70); outside-list cards included. `score.json` gains a
  `cards` block — the ledger's totals, all, list and outside, the open cards and the counts — and the close's line
  ends `cards=<closed>/<open>/<pending>`.
- **`vps/book.py`.** `replay()`'s day of an open position moves into `manage()`, byte for byte (G3); `card_of()` is
  methodology §4's card at a frozen price; `--live --payload <payload>` prints each line's price and card — an
  entry's, or a flat symbol's two triggers, a hold none; `late_cards()` and `--archive --late` replay the late card
  methodology `2026-11-26-b` withdrew on this replay (G4).
- **`vps/run.py`.** An answer whose day log did not reach `origin/main` is followed by notice S16; a session the API
  refused with 429 — the session of 23.11.2026 — sends S17, the spent window named, in place of S7; the summary's first
  line ends `log=yes|no|-`; the trader back on `high`.
- **One reading:** R1, the run unit's journal from 26.11.2026 — the first press after TZ-83.

### Files to Create
None — `score-cards/` is the daily close's to make.

### Files to Modify
`vps/book.py`, `vps/score.py`, `vps/run.py`, `vps/common.py` and `vps/selftest.py`, by §6's patch and nothing else.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
Reads only: `journalctl -u crypto-run.service`, `data.binance.vision`'s archive through `vps/book.py --archive` into
`/tmp/tz84-cache`, and `git show`. No unit, timer or service is started, enabled or installed (item 15): the deployer
installs the merge.

### Not touched
The methodology, the map, the contract, the kit, `analyst/**`, every other file of `vps/`, `index.html`, `main.py`, the
benches and the workflows.

---

## 2. Gates fixed before the data

| # | Expectation | Derived from |
|---|---|---|
| G1 | Baseline: `selftest: sections 28 checks 813 failed 0 empty 0` | the Architect's run of the base — `8e85d64` with this delivery's uploads — under Python 3.11, 3.12 and 3.13 |
| G2 | After it: `selftest: sections 29 checks 842 failed 0 empty 0` — `section AB: checks 145 failed 0`, `section AC: checks 29 failed 0`, `section O: checks 39 failed 0` | the same run on the patched tree |
| G3 | `arch-base` and `arch-new` (§3) equal byte for byte: 9 lines, SHA-256 `8fc070223eac810b83a725e63c14585475319a83beff2e933992e6e60906ac48`; out of sample the rule 298 trades −15.96 R, the plan 303 −6.09 R, the book held 121 +30.48 R | the Architect's run on 26.11.2026, the archive read that day to 2026-11-24, the list by `score.list_symbols()` |
| G4 | `late`: 9 lines, SHA-256 `ab9a1e9748b6e3363204892d68ffc5ad9015a9e4dcc4d1287e951f94ad022292`, among them `all out-of-sample trades 3435  win 0.29  mean R -0.227  total R  -779.97  PF 0.64` | the same run |
| G5 | V5 prints `cards 10 differ 0` | `card_of()` on the 54 states of `analyst/log/2026-11-26.md` at the payload of `5b82ecb`: the trader's ten cards to their printed digits |
| G6 | R1 registers nothing | a reading |

A G3 or G4 SHA-256 that differs while its figures stand is the archive republished since 26.11, stated; a host that
refuses is stated, and V1–V3 decide.

---

## 3. Run order

1. **`kit open TZ-84`.** Any FAIL is BLOCKED (contract §4a step 3).
2. **Baseline:** `kit log selftest-base -- python3 vps/selftest.py` — G1; then G3's first half, `arch-base` below.
3. **`kit stage TZ-84`**, then V1–V5 (§4), then a commit with §7's message — local, not yet pushed.
4. **R1**, below.
5. Push; a pull request titled `TZ-84: vps — the card ledger, the card a state gives, the run's two notices`, its body
   naming this TZ — or contract §8's fallback.
6. `kit usage TZ-84` and `kit units`; back on step 1's checkout (contract §4a step 7); the report; `kit close TZ-84`;
   the report to `main` by `git push origin HEAD:main`; `kit clean TZ-84`; the closing message.

The three archive commands, each one shell line run from the repository root as written, the list read by
production — `arch-new` is `arch-base` again on the staged tree:

```
kit log arch-base -- python3 -I -c 'import sys; sys.path.insert(0, "vps"); import book, score; S = score.list_symbols(); [book.main(["--archive", "--to", "2026-11-24", "--cache", "/tmp/tz84-cache"] + a + S) for a in ([], ["--scale", "2"], ["--scale", "2", "--hold", "6,10"])]'
kit log arch-new -- python3 -I -c 'import sys; sys.path.insert(0, "vps"); import book, score; S = score.list_symbols(); [book.main(["--archive", "--to", "2026-11-24", "--cache", "/tmp/tz84-cache"] + a + S) for a in ([], ["--scale", "2"], ["--scale", "2", "--hold", "6,10"])]'
kit log late -- python3 -I -c 'import sys; sys.path.insert(0, "vps"); import book, score; book.main(["--archive", "--late", "--to", "2026-11-24", "--cache", "/tmp/tz84-cache"] + score.list_symbols())'
```

**R1 — the press of 26.11.2026.** `kit log run-journal-1126 --tail 120 --sh -- 'journalctl -u crypto-run.service
--since "2026-11-26 00:00" --no-pager -o short-iso'`. The report carries every `crypto-run:` line of each press since
then verbatim, and one row per press in TZ-83's R2 table with its `usage model=` lines beside it. No line of the log
is a credential (`common.log` redacts), and `kit close` scans it.

---

## 4. Validation

- **V1.** `kit stage TZ-84` — PASS, the five files of §6's second table at their lines and SHA-256.
- **V2.** `kit log pycompile -- python3 -m py_compile vps/book.py vps/score.py vps/run.py vps/common.py
  vps/selftest.py` — exit 0.
- **V3.** `kit log selftest -- python3 vps/selftest.py` — exit 0, G2's last line and its sections AB, AC and O.
- **V4.** `arch-new` (§3), then `kit log arch-cmp -- cmp /tmp/kit/arch-base.log /tmp/kit/arch-new.log` — exit 0, G3;
  then `late` (§3) — G4.
- **V5.** `git show 5b82ecb:analyst/live.json > /tmp/tz84-live.json`, then this one shell line, as written — G5:

  ```
  kit log card-1126 -- python3 -I -c 'import json, sys; sys.path.insert(0, "vps"); import book; p = book.payload_prices("/tmp/tz84-live.json"); log = open("analyst/log/2026-11-26.md", encoding="utf-8").read().splitlines(); st = {d["symbol"]: d for d in (json.loads(l) for l in log if l.startswith("{\"asof\": \"2026-11-25\""))}; c = [(l.split("|"), book.card_of(st[l.split("|")[5]], p[l.split("|")[5]])) for l in log if l.startswith("CARD|")]; c = [(f, k[f[6]] if k["kind"] == "trigger" else k) for f, k in c]; print("cards %d differ %d" % (len(c), sum(any(abs(k[n] - float(f[i])) > 5e-4 * float(f[i]) for n, i in (("anchor", 9), ("stop", 10), ("target", 11))) for f, k in c)))'
  ```

- **V6.** `kit units` — PASS: the TZ starts no unit; `git status --porcelain --untracked-files=no` lists the five files
  alone.
- No CI step executes `vps/selftest.py`: the branch push runs `bench.yml`'s gate on paths this patch does not read, and
  `## CI Execution` states what ran and its conclusion (contract §9).

---

## 5. Parameters

`EFFORT = "high"` · `LIMIT_STATUS = "429"` · S16 «⚠️ Анализ отправлен, но его запись не сохранилась: его сделки не
войдут в счёт системы.» · S17 «Анализ не выполнен: лимит Claude исчерпан. Переключи аккаунт или дождись сброса лимита
и нажми снова.» · `CARDS = "score-cards"`, a file `<SYMBOL>-<long|short>-<fill ms>.json` of `CARD_KEYS` · `CARD_FIELDS
= 16`, methodology §12's line · `MINUTES_URL`, `fapi/v1/klines` at `1m` from the minute after the freeze to the day's
last, refused unless it reaches both · `book.REACH = √7 / √(8/π)` · a fill-day event stamped no earlier than the fill;
on the archive a limit's fill day checks its stop and not its target · the cards ledger reads its symbols itself and its
failure never stops the book's (`cards: null`).

---

## 6. Shipped

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CryptoTZ/TZ-84-card-ledger.patch` | 65877 | `25f36b1c0abeca5617de0e531ec22cba2948e9b314e9f305a1399805da5e445f` | apply |

| Path | Lines | SHA-256 |
|---|---:|---|
| `vps/book.py` | 582 | `33a1f005f75cce58b99b66e61a5d159291ce05a47fbf56e59bed2f92c3f9bcf7` |
| `vps/score.py` | 834 | `63390275c4e588a2d8a7bba60bb405d8cd00fade3edb51916ff490a34f6f0a0d` |
| `vps/run.py` | 413 | `e7de460b65c18a0cd3ddc49eaa5ea3971f406e869865a16ed429df6ae7166b70` |
| `vps/common.py` | 413 | `3b96a6c49ec2fe47b927cbddaecd07dce2b56732c191d789f3138f830ff230fb` |
| `vps/selftest.py` | 4384 | `7b5db3065013f79612f97331bcf5534780f3d6c76cac072a8e4d03c797f48b98` |

---

## 7. Commit Message

```
TZ-84: vps — the card ledger follows every card the answer printed; the card a state gives and the late card's replay in book.py; notices S16 and S17; the trader back on high
```

---

## 8. Pre-send checks

Run by the Architect before this file was sent:

- `kit caps` on this file — within 20 000 bytes.
- On a fresh clone of `main` at `8e85d64` with this delivery's uploads committed to a local origin, from a linked
  worktree whose `main` the primary clone holds: `kit open TZ-84` PASS, `kit stage TZ-84` PASS, and G1–G5 measured —
  G1 and G2 under Python 3.11, 3.12 and 3.13.
- `kit grow` on the map and the methodology against the files they replace — PASS for each.
