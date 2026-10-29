# Implementation Report — TZ-75

## Status

**PARTIAL.** The patch of §9 was applied byte-exact and every validation item is met except **V5**: `paper.py --probe`
exits 1 because two of its steps, `klines_1m` and `klines_1d`, read `failed (NotPublished)`. Binance Vision has published
no daily file for 28.10.2026 (BTCUSDT, ETHUSDT and SOLUSDT all answer 404), and the probe asks for «yesterday». Unmodified
`main` fails the identical two steps (§ Validation, V5). The new `leverage` step reads. The one thing that closes the item:
Vision publishing the 28.10 files, after which V5's command is run again (a `-report-2.md`), or the Architect accepting
the supplementary 27.10 reading recorded under V5.

The previous TZ, TZ-74, is COMPLETED and report-only; no branch on the remote is ahead of `main`
(`git rev-list --count origin/main..<branch>` printed 0 for all twelve remote branches).

## Inbound Filing

None. `CryptoTZ/TZ-75-paper-alerts-rescan.md` was already at its canonical filename on `origin/main` (`6ea603c`, «Add files via upload»); nothing was moved. `git diff --stat 92ebce3 6ea603c` shows that upload as the only change since the commit the TZ was written against.

## Scope Executed

**Branch TZ** (contract §8): it authorises two repository files besides its report. Stages A–D of the TZ. Host: the VPS (`hostname` prints `vultr`; `crypto-paper.service` active), so stage C ran where the TZ requires it.

## Files Created

None in the repository but this report.

## Files Modified

- `vps/paper.py` — 1281 → 1413 lines.
- `vps/selftest.py` — 2430 → 2627 lines.

## Files Renamed

None.

## Files Deleted

None.

## Implementation Summary

The TZ's §9 patch, applied with `git apply` and no hand edit. It adds to `vps/paper.py`: the restyled alert texts (`P_HEAD`, `P_OPEN`, `P_OPEN_BARE`, `P_CLOSE`, `P_LEV`, `SIDE_DOT`, the two marks), `number()`, `read_leverage()` (never raises), `lev_text()`, `gained()`; `select()` gains `work`, `symbols`, `exclude`, `k` and `draw_null` so the rescan is `select()` itself; `pick_joins()`, `rescan_state()`, `rescan_due()`, `rescan_run()`, `adopt()`, the rescan thread in `service()`, the per-pick span in `produce_verdict()`, and a `leverage` step in `probe()`. `vps/selftest.py` rewrites W11's alert texts as A1 and adds W11, W14, W16 and W17 checks.

## Validation

Baseline first (A2), then B, then C.

### Stage A

**A0/A1 — gate.** `**Revision 2026-10-26-a.**` is the map's revision. The four added files measured at the required lines and MD5 (table under `## Fingerprints`); `**Version 31.**` present at `EXECUTOR-INSTRUCTIONS.md:3`; `MemoryMax=128M` present at `vps/units/crypto-paper.service:26`. `analyst/paper/selection.json` `fp.paper_md5` = `057440a4b5c9c277cc99062f768464ac` = `md5sum vps/paper.py` on `main`.

**A2 — baseline** (`python3 vps/selftest.py` on `main` at `6ea603c`, exit 0): `selftest: sections 27 checks 560 failed 0 empty 0`; `section W: checks 102 failed 0`.

### Stage B

**B1.** Branch `claude/tz-75-paper-alerts-rescan` from `origin/main`. The extraction command, verbatim from the TZ, writing to the session scratchpad instead of `/tmp`:

```
awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-75-paper-alerts-rescan.md > <scratchpad>/tz75.patch
```

Patch: **614 lines, MD5 `acb0d618ace0be21278f9a782ee2f5eb`** — as written. `git apply --check` printed nothing and exited 0.

**B2.** `git apply`:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `vps/paper.py` | 1413 | `a709359a86f630c464fd92ee93f6ae2c` | 1413, `a709359a…` — equal |
| `vps/selftest.py` | 2627 | `76e814ccbe18551a8f47d6f7eae09669` | 2627, `76e814cc…` — equal |

### Stage C

| # | Check | Result |
|---|---|---|
| V1 | `python3 -m py_compile vps/paper.py vps/selftest.py` | exit 0 |
| V2 | B2's two files | equal (table above) |
| V3 | `python3 vps/selftest.py` on the branch, on the VPS | exit 0; `selftest: sections 27 checks 592 failed 0 empty 0`; `section W: checks 134 failed 0` — met |
| V4 | negative control | met (below) |
| V5 | `paper.py --probe` as a transient unit | **FAILED** (below) |
| V6 | `git diff --name-only origin/main...HEAD` | `vps/paper.py`, `vps/selftest.py` — met |
| V7 | live service before/after; no transient unit left | met (below) |
| V8 | `bench.yml` | reported (below) |

**V3 — per-section counts, A2 beside V3** (the 458 checks outside W do not move; W grows by 32):

| Section | A2 (main) | V3 (branch) |
|---|---:|---:|
| A | 32 | 32 |
| B | 12 | 12 |
| C | 4 | 4 |
| D | 13 | 13 |
| E | 12 | 12 |
| F | 14 | 14 |
| G | 8 | 8 |
| H | 2 | 2 |
| I | 4 | 4 |
| J | 26 | 26 |
| K | 2 | 2 |
| L | 4 | 4 |
| M | 19 | 19 |
| N | 10 | 10 |
| O | 33 | 33 |
| P | 21 | 21 |
| Q | 3 | 3 |
| R | 9 | 9 |
| S | 35 | 35 |
| T | 39 | 39 |
| U | 18 | 18 |
| V | 16 | 16 |
| W | 102 | 134 |
| X | 19 | 19 |
| Y | 54 | 54 |
| Z | 23 | 23 |
| AA | 26 | 26 |
| **total** | **560** | **592** |

**V4 — negative control.** `> 2 * rule["fee_taker"]` (one occurrence) replaced with `> 0` in `vps/paper.py`; selftest exit **1**; the only `FAIL` line, verbatim:

```
FAIL section W: a move inside the fee both ways is a loss: red cross
```

`selftest: sections 27 checks 592 failed 1 empty 0`. Restored with `git checkout -- vps/paper.py`; `git status --porcelain` printed nothing; `vps/paper.py` back at 1413 lines, `a709359a…`. See Deviations 2 for the order in which this ran.

**V5 — the probe.** Transient unit, as TZ-64 C2 ran it, from the branch's clone (`/root/crypto-auto/.claude/worktrees/bridge-cse_01KgRjgw3wurHxdZ4K7XGTdB`, `HEAD` `4d914c4`, `paper.py` `a709359a…`), at 19:44 UTC on 29.10.2026:

```
systemd-run --wait --pipe --collect -p MemoryMax=128M -p Nice=5 /usr/bin/python3 <clone>/vps/paper.py --probe
```

Output (exit **1**; unit `run-u5285.service`):

```
paper: probe leaderboard rows=48473 pool=4091 bad=0
paper: probe portfolio blocks=11 drawdown=0.11413312997297465 eligible=True r12=True ret52=2.5265436716641037 sharpe=0.536783429984664 turnover=1.0136312132552967 value_t0=851887.284697
paper: probe exchange perpetuals=522
paper: probe leverage positions=2
paper: probe fills fills=12127 first=2026-08-01T20:43:32Z
paper: probe klines_1m failed (NotPublished)
paper: probe klines_1d failed (NotPublished)
paper: probe funding rows=90
paper: probe peak_rss_kib=39192
Finished with result: exit-code
Main processes terminated with: code=exited/status=1
Service runtime: 1min 5.686s
CPU time consumed: 546ms
Memory peak: 568.0K
```

Required: exit 0 and no `failed (…)`. **Not met: two steps failed.** The new step reads (`leverage positions=2`); `peak_rss_kib=39192` is under `MemoryMax=128M`.

Diagnosis, each by a recorded command:

1. `probe()` asks for «yesterday» (`vps/paper.py:1374`, `yesterday = add_days(utc_date(now_ms()), -1)`) — 2026-10-28 — at `VISION = "https://data.binance.vision/data/futures/um"`. HTTP status of `curl -s -o /dev/null -w '%{http_code}'` on `…/daily/klines/BTCUSDT/{1m,1d}/BTCUSDT-{1m,1d}-<date>.zip`: **2026-10-27 → 200 and 200; 2026-10-28 → 404 and 404; 2026-10-29 → 404 and 404.** Re-read at 19:46 UTC: still 404 for BTCUSDT 1m and 1d, ETHUSDT 1d and SOLUSDT 1d of 28.10.
2. **Pre-existing, by running the unmodified code.** `git archive origin/main vps` into the scratchpad (`paper.py` 1281 lines, `057440a4…`), same command, run a minute later (unit `run-u5286.service`), exit **1**: identical `leaderboard`, `portfolio`, `exchange`, `fills`, `funding` lines and the identical `paper: probe klines_1m failed (NotPublished)` and `paper: probe klines_1d failed (NotPublished)`; no `leverage` line; `peak_rss_kib=39180`.
3. **Supplementary, not a substitute for V5.** The two klines steps' own call, `paper.vision_rows(...)`, run on the branch's `vps/paper.py` for the last published day: `klines_1m 2026-10-27 rows=1440`, `klines_1d 2026-10-27 rows=1` (TZ-64's registered values), and `klines_1d 2026-10-28 -> NotPublished`. A direct python call from the clone's `vps/` directory, no unit.
4. The live service is not affected in what it publishes: `journalctl -u crypto-paper.service` shows `paper: publish copied=1 pushed=yes left=0` at `Oct 29 00:17:20` (the journal's own clock).

**V7 — the live test was not restarted.**

```
before: MainPID=2696823  ActiveEnterTimestamp=Sun 2026-10-25 12:11:15 UTC
after:  MainPID=2696823  ActiveEnterTimestamp=Sun 2026-10-25 12:11:15 UTC
```

The session started two transient units, `run-u5285.service` and `run-u5286.service`, both with `--collect` and both finished. After the session `systemctl list-units --all 'run-u*' --no-legend` prints only `run-user-0.mount` (a mount of root's login), and the full `systemctl list-units --all 'run-*'` lists only `.mount` units (credentials, `docker-netns`, `user-0`) — no `run-u*.service`. The «before» listing was cut at ten rows by `head` and held `.mount` units only; it is not a like-for-like diff of the full list, and the claim made is only that no unit of the session remains.

**V8 — `bench.yml`.** `index.html` and `main.py` are untouched, so the standing checks (`py_compile main.py`, `node --check`) do not apply. Runs on the branch, read with `gh run list --branch claude/tz-75-paper-alerts-rescan`: `40943201157` Bench gate, event `push` — **completed, success**; `40943245479` Bench gate, event `pull_request` — **in_progress** when read. `main.yml` is an allow-list of `main.py` and its own file and cannot fire on this diff. **The TZ's sentence that `vps/**` «is outside the hosted gate by its own comment» does not match the file:** `bench.yml`'s `paths-ignore` (lines 29–47) names `analyst/paper/**` and `**.md` and no `vps/**`, and the only comment about `vps` (lines 43–45) concerns `analyst/paper/**` records. The hosted gate therefore does run on a `vps/**` change; no step of it executes `vps/selftest.py` (`grep -n -E 'vps|selftest' .github/workflows/bench.yml` hits lines 43 and 45, the comment above, and lines 146 and 148, the step `bash analyst/live-gate.sh --selftest`, which is another program). Reported for the Architect.

## Test Results

- `python3 vps/selftest.py`, branch: `selftest: sections 27 checks 592 failed 0 empty 0`; `section W: checks 134 failed 0`.
- `python3 vps/selftest.py`, `main` (A2): `checks 560 failed 0 empty 0`; W 102.
- Negative control: exit 1, one `FAIL`.
- Probe: **FAILED** on two steps (V5), identical on unmodified `main`.

## Deviations

1. **The patch was extracted to the session scratchpad, not `/tmp/tz75.patch`.** The command is the TZ's, verbatim; only the output path differs. The patch's lines and MD5 are those of the TZ.
2. **The implementation commit was made locally before V4, which the TZ places in stage C ahead of stage D's commit.** V4 restores with `git checkout -- vps/paper.py` and requires `git status --porcelain` to print nothing; with the patch applied but uncommitted that checkout restores the *unpatched* `main` file and the status could not be empty. Order that happened: V4 ran once on the uncommitted tree (exit 1, the same single `FAIL`); the patched file was restored from a byte-copy taken before the mutation (`a709359a…` re-verified); the one implementation commit was made (not pushed); V4 was run again exactly as written on the committed tree (exit 1, the same single `FAIL`, restore by `git checkout -- vps/paper.py`, empty status). Stage D's push and pull request followed after the rest of stage C. The branch carries one implementation commit.
3. **V5 was not met** (above).
4. The TZ's B1 permits the patch hash to differ on upload; it did not.

## Pre-existing Issues

- **Binance Vision has published no daily kline file for 28.10.2026** as of 19:46 UTC on 29.10.2026 (BTCUSDT 1m/1d, ETHUSDT 1d, SOLUSDT 1d: 404; 27.10: 200). `probe()` therefore fails its two klines steps on unmodified `main` at that hour, shown by running `main`'s tree (V5, item 2). It is an upstream gap, not a defect of the branch, and the session did not act on it.
- **`probe()` has no date fallback:** its «yesterday» is the only day it asks for, so any lag of Vision's daily publication turns the probe red regardless of the code under test.
- The statement in the TZ about `vps/**` and the hosted gate (V8 above).

## Remaining Risks

- **The rescan thread's memory is bounded by arithmetic, not measured.** The probe does not run `select()` and peaked at 39 192 KiB; the TZ's 77 MiB upper bound for the service under `MemoryMax=128M` (§3 B3) rests on TZ-64's and TZ-65's figures, and this session did not run the thread alongside the booking. The first rescan runs only after the deployer installs the merge, at the service's first start after it.
- **The probe's `leverage` step reads one account** (`PROBE_ACCOUNT`, 2 positions); a coin with no position, a refused read and a malformed answer are covered by W11's four `read_leverage` checks on faked `info`, not by a live read of each case.
- **Rate budget:** each alerted pick open now spends one extra `INFO_WEIGHT` through the service's limiter, and a running rescan holds 300 of the 600 per minute. Not measured here.
- The keycap digit in place of the owner's Premium custom emoji is the Architect's decision (A1) and was implemented as written.

## Commit

Implementation commit message, as TZ §7 gives it (pushed to the branch before this report was written):

```
TZ-75: vps — paper alerts carry the whale's number, its leverage and a coloured close; the selection rule re-applied every four weeks until three whales are followed
```

Contents: `vps/paper.py` and `vps/selftest.py`, the §9 patch (`git diff --name-only origin/main...HEAD` prints exactly those two). Hash `4d914c41d31ba7d4cbf0164a6777a58a2ee9e274`.

The report's own commit message:

```
TZ-75: report — paper alerts and the four-weekly rescan
```

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/61 — title `TZ-75: paper alerts — whale number, leverage, coloured close; four-weekly rescan`, from `claude/tz-75-paper-alerts-rescan` to `main`; its body names TZ-75 and states V5's failure. **The map's row «Hyperliquid's large accounts» is the Architect's to update after the audit, not this TZ's.**

## CI Execution

Workflow `Bench gate` (`bench.yml`) triggered twice by the push and the pull request, read from the runner with `gh run list --branch claude/tz-75-paper-alerts-rescan`: run `40943201157` (`push`) — completed, conclusion `success`; run `40943245479` (`pull_request`) — status `in_progress`, no conclusion, at the time of reading. `gh run list --branch claude/tz-75-paper-alerts-rescan` shows no other workflow on the branch; `main.yml`'s `paths` allow-list names `main.py` and its own file, neither of which the diff touches. No step of the hosted gate runs `vps/selftest.py` (V8); the selftest result above is the VPS's, not a runner's.

## Final Repository State

Branch `claude/tz-75-paper-alerts-rescan`, pushed, one commit `4d914c41d31ba7d4cbf0164a6777a58a2ee9e274` over `origin/main` at `6ea603c`; pull request #61 open. **NOT IN EFFECT UNTIL MERGED.** The running `crypto-paper.service` (MainPID 2696823) runs `vps/paper.py` `057440a4…` and was not touched; no unit, timer or file under `/etc` or `/var/lib/cryptopaper` was created, changed or restarted. The fingerprints below were taken in the checkout at `origin/main` `6ea603c`; the branch's two files are in the V2 table.

## Fingerprints

**Map:** `SYSTEM-MAP-CRYPTOCALCUL.md` — **2796 lines, MD5 `e911fceb5f07444fe306f116a550b9cf`**; revision `**Revision 2026-10-26-a.**`.

**Anchors.** The table was cut by its structure, `awk '/^\| Anchor \| Exact string/{f=1;next} f&&/^\|---/{next} f&&/^\|/{print;next} f{exit}'`, from the map and from the TZ: **7 rows in the map, 7 rows in the TZ, 7 compared**, and `diff` of the two cuts printed nothing. Per anchor, `grep -F -o -- '<anchor>' SYSTEM-MAP-CRYPTOCALCUL.md` returned:

| Anchor | Text matched |
|---|---|
| revision | `**Revision 2026-10-26-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

**Files the map lists, at `6ea603c`:**

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Files this TZ's gate adds, at `6ea603c`:**

| File | Lines | MD5 |
|---|---:|---|
| `EXECUTOR-INSTRUCTIONS.md` (`**Version 31.**`) | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` |
| `vps/paper.py` | 1281 | `057440a4b5c9c277cc99062f768464ac` |
| `vps/selftest.py` | 2430 | `1f207b2dce474439924b1ef22c82e918` |
| `vps/units/crypto-paper.service` | 30 | `082a64f8f3a11ca4d4fab6a3974a97e8` |

Every file above equals its required line count and MD5; none differs.

**The branch's two files:** `vps/paper.py` 1413 lines `a709359a86f630c464fd92ee93f6ae2c`; `vps/selftest.py` 2627 lines `76e814ccbe18551a8f47d6f7eae09669`. **The patch:** 614 lines `acb0d618ace0be21278f9a782ee2f5eb`.
