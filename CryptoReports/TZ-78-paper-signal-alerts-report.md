# Implementation Report — TZ-78

## Status
COMPLETED

The previous TZ's branch, `claude/tz-77-paper-api-window-orders`, is merged at `c49e7f2` (pull request #63); `git branch -r --no-merged origin/main` printed nothing. This TZ is built on `origin/main` at `548c644`.

## Inbound Filing
None. `CryptoTZ/TZ-78-paper-signal-alerts.md` arrived at its canonical path (`548c644`, «Add files via upload»), the filename its header states. Nothing was moved.

## Scope Executed
**Class: branch TZ** (contract §8): the scope names `vps/paper.py` and `vps/selftest.py` besides this report.

- Stage A: A0 (contract §4a steps 1–6, the §0 gate), A1 (the four added files), A2 (baseline selftest on the VPS), A3 (the live recorder's PID and start time).
- Stage B: B1 (branch, patch extracted with the TZ's command), B2 (`git apply`, bytes checked), B3 (local commit before stage C).
- Stage C: V1–V9, in full.
- Stage D: push, pull request #64, this report.

On the VPS: one transient unit for V5 (`run-u5749.service`, `--collect`), gone afterwards. No persistent unit, timer or file under `/etc` or `/var/lib/cryptopaper` was created, changed or restarted.

## Files Created
- `CryptoReports/TZ-78-paper-signal-alerts-report.md` (this report, on `main`).

## Files Modified
- `vps/paper.py` — 1785 → 1947 lines (§10's patch).
- `vps/selftest.py` — 3063 → 3173 lines (§10's patch).

## Files Renamed
None.

## Files Deleted
None.

## Implementation Summary
§10's patch was applied as written, with no hand edit. Its bytes are proven by B2's MD5s. What it does (TZ §1, §3):
- A pick's new position is sent as `**(NEW SIGNAL)**` and its close as `**(SIGNAL)**`, with 🐋 and the whale's number side by side. Every other message stays «Бумажный тест». The new-whale notice puts the number beside 🐋 too.
- `read_whale` replaces `read_leverage`. It reads the whale's side, leverage (through the shared `leverage_in`), average entry, position value and its share of his account. It also reads his resting stops and targets on the closing side, classed by `orderType` and sorted in trigger order, with children of resting parents excluded.
- The copy's stop is the test's 2σ, printed to at least five significant digits.
- The copy line sizes on `analyst/owner.json` as it stands at the signal, through `owner_book`/`owner_now` and the shared `risk_usdt`. It prints notional, margin at 3x and the copy's place within the side and book ceilings, or a skip line instead.
- `load_rule` reads capital and medium risk through `owner_book`. `book_delay`'s sizing goes through `risk_usdt`, the same expression as before.

## Validation

### A0 — fingerprint gate (contract §5)
Map revision string read from `## 0. Fingerprint`: `**Revision 2026-11-06-f.**`, the one the TZ requires.

The anchor list was cut by the table's structure: every `|` row after the header and separator of the `| Anchor |` table at map line 85, up to the first non-table line. **Table row count: 7. Anchors compared: 7.** For each row: `grep -F -o -m1 -- "<anchor>" SYSTEM-MAP-CRYPTOCALCUL.md` (matched text), and `grep -F -c -- "<row>" CryptoTZ/TZ-78-paper-signal-alerts.md` (the TZ header quotes the row verbatim):

```
anchor 1: map: **Revision 2026-11-06-f.** | TZ: 1
anchor 2: map: ### 3.12 Direction engine — veto cascade | TZ: 1
anchor 3: map: ### 3.15 Catalyst registry | TZ: 1
anchor 4: map: ### 3.16 List exhaustion — the day-range measure | TZ: 1
anchor 5: map: ## 11. Analytical engine | TZ: 1
anchor 6: map: ### 3.17 «РИСК ВЫНОСА» — the day's own risk | TZ: 1
anchor 7: map: 72. **A write that fails leaves this run's product or nothing | TZ: 1
compared 7
```

Repository state: `git fetch --all --prune` done; `git rev-parse --is-shallow-repository` → `false`; the tree was clean.

### A1 — added files (`wc -l`, `md5sum`, on `origin/main` `548c644`)
| File | Lines | MD5 | Required | Result |
|---|---:|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | 859 / same, `**Version 31.**` | equal; version line `**Version 31.**` |
| `analyst/owner.json` | 27 | `dc7dd911c8d0f262cf749ce9c2aa1e03` | 27 / same | equal |
| `vps/paper.py` | 1785 | `2d814305c3e2883c79dbcf1c6fa14068` | 1785 / same | equal |
| `vps/selftest.py` | 3063 | `505efb7dc01c40dd09c9c9008e49345b` | 3063 / same | equal |

### A3 — the live recorder before the session
`systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service`:
```
MainPID=376520
ActiveEnterTimestamp=Fri 2026-11-06 12:23:09 UTC
```

### B1 — the patch
```sh
awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-78-paper-signal-alerts.md > /tmp/tz78.patch
```
`/tmp/tz78.patch`: **561 lines, MD5 `f2168d62d6d97e1c89a94a96a107f6a0`**, matching the value the TZ states.

### B2 — `git apply /tmp/tz78.patch` → exit 0
| File | Lines | MD5 | Required |
|---|---:|---|---|
| `vps/paper.py` | 1947 | `60018d258594aa629e6f8d5f0dc5c6d9` | 1947 / `60018d258594aa629e6f8d5f0dc5c6d9` ✓ |
| `vps/selftest.py` | 3173 | `f79b05657550180ad9f18603cda5cec1` | 3173 / `f79b05657550180ad9f18603cda5cec1` ✓ |

### B3
Committed locally as `538a621` before stage C. The branch was pushed only after V1–V8 passed.

## Test Results

| # | Command | Result |
|---|---|---|
| V1 | `python3 -m py_compile vps/paper.py vps/selftest.py` | exit 0 |
| V2 | B2's two files | 1947 / `60018d25…c6d9`, 3173 / `f79b0565…cec1` — equal |
| V3 | `python3 vps/selftest.py` on the branch, on the VPS (host `vultr`) | exit 0; `selftest: sections 27 checks 662 failed 0 empty 0`; `section W: checks 204 failed 0`; every other section equal to A2 (table below) |
| V4a | first negative control | as required (below) |
| V4b | second negative control | as required (below) |
| V4c | third negative control | as required (below) |
| V5 | the reader against the picks' live accounts | exit 0, `v5: positions 11 read 11 failed 0` (below) |
| V6 | `git diff --numstat origin/main...HEAD` | `206\t44\tvps/paper.py` and `135\t25\tvps/selftest.py` — exactly two lines, as required |
| V7 | `systemctl list-units --all 'run-*'` after V5 | identical to the listing before V5. `run-u5749.service` is absent; only the pre-existing credential mounts, docker netns and `/run/user/0` remain |
| V8 | `systemctl show -p MainPID -p ActiveEnterTimestamp crypto-paper.service` after the session | `MainPID=376520`, `ActiveEnterTimestamp=Fri 2026-11-06 12:23:09 UTC` — equal to A3 |
| V9 | `bench.yml` | see `## CI Execution` |

### A2 vs V3, per section (`python3 vps/selftest.py`, VPS)
A2 on `origin/main` `548c644` (exit 0; `selftest: sections 27 checks 643 failed 0 empty 0`). V3 on branch `538a621` (exit 0; `selftest: sections 27 checks 662 failed 0 empty 0`).

| Section | A2 checks | V3 checks | V3 failed |
|---|---:|---:|---:|
| A | 32 | 32 | 0 |
| B | 12 | 12 | 0 |
| C | 4 | 4 | 0 |
| D | 13 | 13 | 0 |
| E | 12 | 12 | 0 |
| F | 14 | 14 | 0 |
| G | 8 | 8 | 0 |
| H | 2 | 2 | 0 |
| I | 4 | 4 | 0 |
| J | 26 | 26 | 0 |
| K | 2 | 2 | 0 |
| L | 4 | 4 | 0 |
| M | 19 | 19 | 0 |
| N | 10 | 10 | 0 |
| O | 33 | 33 | 0 |
| P | 21 | 21 | 0 |
| Q | 3 | 3 | 0 |
| R | 9 | 9 | 0 |
| S | 35 | 35 | 0 |
| T | 39 | 39 | 0 |
| U | 18 | 18 | 0 |
| V | 16 | 16 | 0 |
| W | 185 | 204 | 0 |
| X | 19 | 19 | 0 |
| Y | 54 | 54 | 0 |
| Z | 23 | 23 | 0 |
| AA | 26 | 26 | 0 |

The only difference is W, 185 → 204 (+19 = 23 added − 4 removed). The 458 checks outside W are unchanged.

### V4 — negative controls
Each control changed exactly one occurrence in `vps/paper.py` (occurrence count 1, asserted before the replacement), ran `python3 vps/selftest.py`, then restored with `git checkout -- vps/paper.py`.

**V4a** — `("A" if side > 0 else "B") or o["oid"] in waiting:` → `("A" if side > 0 else "B"):`. Exit 1:
```
FAIL section W: read_whale: the position, and the closing side's stops and targets in trigger order; an opening order and one waiting on a resting parent out
selftest: sections 27 checks 662 failed 1 empty 0
```
`git status --porcelain` afterwards: empty.

**V4b** — `any(kind != "open"` → `any(kind == "lost"`. Exit 1:
```
FAIL section W: closed later in the same poll: the signal reads no position
FAIL section W: added to later in the same poll: the signal reads the position
selftest: sections 27 checks 662 failed 2 empty 0
```
`git status --porcelain` afterwards: empty.

**V4c** — `    if n_side > cap_side:` → `    if n_side > cap_side + 1:`. Exit 1:
```
FAIL section W: six open LONG signals already: the seventh is a skip
selftest: sections 27 checks 662 failed 1 empty 0
```
`git status --porcelain` afterwards: empty.

### V5 — the reader against the picks' live accounts
Extracted with `awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-78-paper-signal-alerts.md > /tmp/tz78-v5.py`. The script is **19 lines, MD5 `bbb8cb0a1b445af2d18312ffb60983a9`**, the values the TZ states. Started at `Fri Nov  6 05:29:52 PM UTC 2026` with:
```
systemd-run --wait --pipe --collect -p MemoryMax=128M -p WorkingDirectory=/root/crypto-auto/.claude/worktrees/bridge-cse_01KgRjgyAB1HwBGvktpjiAFE /usr/bin/python3 /tmp/tz78-v5.py
```
Exit 0. Output, verbatim (systemd's unit lines included):
```
Running as unit: run-u5749.service; invocation ID: 4d02861886b642c0babdb87b142b5071
**(NEW SIGNAL)** 21:29 Тбилиси · 🐋1️⃣ 0xa5fd…15ff открыл LONG 🟢 BTC | Вход кита: `79476.9` · плечо 40x (весь счёт 2.8x) · позиция 543.5 тыс. USDT = 45.0% счёта кита | Стоп кита: нет · тейк кита: нет | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:29 Тбилиси · 🐋1️⃣ 0xa5fd…15ff открыл LONG 🟢 ETH | Вход кита: `2705.0` · плечо 20x (весь счёт 2.8x) · позиция 458.4 тыс. USDT = 38.0% счёта кита | Стоп кита: нет · тейк кита: `2730.0` (+0.9%) и ещё 1 | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:29 Тбилиси · 🐋1️⃣ 0xa5fd…15ff открыл LONG 🟢 ARB | Вход кита: `0.19996` · плечо 10x (весь счёт 2.8x) · позиция 8.0 тыс. USDT = 0.7% счёта кита | Стоп кита: нет · тейк кита: `0.2` (+0.0%) и ещё 1 | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:29 Тбилиси · 🐋1️⃣ 0xa5fd…15ff открыл LONG 🟢 XRP | Вход кита: `1.481294` · плечо 20x (весь счёт 2.8x) · позиция 341.8 тыс. USDT = 28.3% счёта кита | Стоп кита: нет · тейк кита: `1.48` (−0.1%) и ещё 1 | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:29 Тбилиси · 🐋1️⃣ 0xa5fd…15ff открыл LONG 🟢 BCH | Вход кита: `357.73` · плечо 10x (весь счёт 2.8x) · позиция 166.2 тыс. USDT = 13.8% счёта кита | Стоп кита: нет · тейк кита: `358.0` (+0.1%) | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:29 Тбилиси · 🐋1️⃣ 0xa5fd…15ff открыл LONG 🟢 WLD | Вход кита: `0.51611` · плечо 10x (весь счёт 2.8x) · позиция 283.3 тыс. USDT = 23.5% счёта кита | Стоп кита: нет · тейк кита: `0.69` (+33.7%) и ещё 2 | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:30 Тбилиси · 🐋2️⃣ 0x8fc7…b0f7 открыл SHORT 🔴 HYPE | Вход кита: `81.9114` · плечо 3x (весь счёт 0.2x) · позиция 90.8 тыс. USDT = 11.2% счёта кита | Стоп кита: нет · тейк кита: нет | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:30 Тбилиси · 🐋2️⃣ 0x8fc7…b0f7 открыл SHORT 🔴 INIT | Вход кита: `0.097976` · плечо 3x (весь счёт 0.2x) · позиция 6.6 тыс. USDT = 0.8% счёта кита | Стоп кита: нет · тейк кита: нет | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:30 Тбилиси · 🐋2️⃣ 0x8fc7…b0f7 открыл LONG 🟢 SKY | Вход кита: `0.081126` · плечо 3x (весь счёт 0.2x) · позиция 12.1 тыс. USDT = 1.5% счёта кита | Стоп кита: нет · тейк кита: нет | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:30 Тбилиси · 🐋2️⃣ 0x8fc7…b0f7 открыл LONG 🟢 2Z | Вход кита: `0.055929` · плечо 3x (весь счёт 0.2x) · позиция 2.6 тыс. USDT = 0.3% счёта кита | Стоп кита: нет · тейк кита: нет | Стоп копии: не рассчитан — нет дневных свечей Binance
**(NEW SIGNAL)** 21:30 Тбилиси · 🐋2️⃣ 0x8fc7…b0f7 открыл SHORT 🔴 LIT | Вход кита: `3.375869` · плечо 5x (весь счёт 0.2x) · позиция 55.4 тыс. USDT = 6.8% счёта кита | Стоп кита: нет · тейк кита: нет | Стоп копии: не рассчитан — нет дневных свечей Binance
v5: positions 11 read 11 failed 0
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 1min 3.649s
CPU time consumed: 211ms
Memory peak: 636.0K
Memory swap peak: 0B
```
N = 11: six positions of pick 1 (the script's cap) and five of pick 2. That is at least 1 and at most six per pick; none failed. The script passes `sigma=None`, so every line correctly ends at «Стоп копии: не рассчитан» with no copy line. The copy line itself is covered by section W's known answers in V3.

## Deviations
None. The B1/V5 extraction commands wrote to `/tmp/tz78.patch` and `/tmp/tz78-v5.py` as the TZ specifies. Both are outside the repository.

## Pre-existing Issues
None found within scope.

## Remaining Risks
- The signal takes effect only when the deployer installs the merge. Until then, the running recorder (PID 376520) keeps sending the TZ-75 open alert, sized on the selection's frozen 10 000 USDT.
- V5 exercised `read_whale` and the open line's whale fields against live accounts, with `sigma=None`. The copy line and the skip lines were exercised only by section W's fixtures, not against a live σ.
- Pick 1 currently rests **no Stop trigger** on any of the six positions read («Стоп кита: нет» on all six), the same as the Architect's 14:11 UTC reading. Some of its targets are reduce-only limits at or just below entry (XRP `1.48` from `1.481294`, −0.1 %). They print as targets, not stops, which is the TZ's classification by `orderType`.

## Commit
- Implementation (pushed on the branch): `538a62159372c7f27a212e4d02af31b98706da50` — `TZ-78: vps — a whale's new position reaches the owner as a (NEW SIGNAL) with his entry, leverage, resting stop and take-profit, and the copy sized to the owner's capital within his side and book ceilings`. Contents: `vps/paper.py` (+206 −44) and `vps/selftest.py` (+135 −25).
- Report: message `TZ-78: report — the paper test's signals`. Contents: this file alone, directly on `main`.

## Pull Request
https://github.com/seahomebatumi-ai/crypto-auto/pull/64 — `claude/tz-78-paper-signal-alerts` → `main`, titled as TZ §5 stage D fixes.

## CI Execution
Read from the runner with `gh run list -R seahomebatumi-ai/crypto-auto --branch claude/tz-78-paper-signal-alerts`, both on head `538a621`:
- `Bench gate` run `42262357508` (push) — **success**.
- `Bench gate` run `42262402134` (pull_request) — **success**.

No other workflow ran on the branch. `main.yml`'s `push` trigger is `branches: [ main ]` with a `paths` allow-list starting at `main.py`, so it does not fire on this branch. `index.html` and `main.py` are untouched, so the standing checks of map §6 item 1 do not apply. **No step of the hosted gate runs `vps/selftest.py`**: `grep -n selftest .github/workflows/*.yml` finds only `live-gate.sh --selftest`, `backtest_bench.py --selftest` and `exhaustion_calib.py --selftest`, and the log of run `42262357508` contains 0 occurrences of `selftest.py`. The selftest is run by the deployer before it installs, and here by V3 on the VPS.

## Final Repository State
Branch `claude/tz-78-paper-signal-alerts` was pushed at `538a621`, one commit on `origin/main` `548c644`, and pull request #64 is open. The worktree was clean after every negative control and after V5 (`git status --porcelain` empty), and no `__pycache__` was left.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints
`SYSTEM-MAP-CRYPTOCALCUL.md`: **2804 lines, MD5 `c257b761bf1775d9abdab74a48262b9f`**, revision string `**Revision 2026-11-06-f.**`. The TZ states the same pair (reported, not enforced).

The map's `## 0` table, measured on `origin/main` `548c644` (and unchanged on the branch):
| File | Lines | MD5 | Map |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

The TZ gate's added files, before (on `548c644`) and after (on the branch at `538a621`):
| File | Before | After |
|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 / `4390ee0b8bf1e8d7837afffcd7a5b803` | unchanged |
| `analyst/owner.json` | 27 / `dc7dd911c8d0f262cf749ce9c2aa1e03` | unchanged |
| `vps/paper.py` | 1785 / `2d814305c3e2883c79dbcf1c6fa14068` | 1947 / `60018d258594aa629e6f8d5f0dc5c6d9` |
| `vps/selftest.py` | 3063 / `505efb7dc01c40dd09c9c9008e49345b` | 3173 / `f79b05657550180ad9f18603cda5cec1` |

Anchors, per row, with the matched text: see `## Validation` → A0 (7 of a 7-row table).
