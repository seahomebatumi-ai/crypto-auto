# Implementation Report — TZ-80

## Status

COMPLETED.

Stages A, B, C and D executed in full. Every validation item V1–V9 was run; none was
skipped and none failed. The previous TZ's branch was merged before this work began:
`origin/claude/tz-79-book-signal-and-ledger` is an ancestor of `origin/main`
(`git merge-base --is-ancestor` exit 0), TZ-79's report stands on `main`, and no branch on
the remote is ahead of `main` — the loop over `git branch -r` printing a line per branch not
contained in `origin/main` printed none.

## Inbound Filing

None. The TZ arrived at its own canonical path, `CryptoTZ/TZ-80-plan-target-size.md`, in
commit `878eee3` ("Add files via upload", 2064 insertions, one file). No artifact landed in
the repository root and no filename was mangled, so no `git mv` was performed.

```text
$ git ls-tree -r --name-only origin/main -- CryptoTZ/ | grep -i 'tz-80'
CryptoTZ/TZ-80-plan-target-size.md
$ git ls-tree --name-only origin/main | grep -i 'tz'
CryptoTZ
```

The first text under this number, handed to the Boss on 13.11.2026, was never uploaded: no
other `CryptoTZ/TZ-80-*` path and no `CryptoReports/TZ-80-*` report exist on the remote, so
nothing of an earlier execution had to be reconciled and this text is the only TZ-80 the
repository has ever carried.

## Scope Executed

**Class: branch TZ** (contract §8). The TZ's `## Scope` names seven files outside
`CryptoReports/**` — two created, five modified — so a branch and a pull request are opened
and the report goes to `main` on the `CryptoReports/**` direct-push path.

Executed exactly the specification: §10's patch applied byte-exact to the five modified
files and the two created units, §6's validation in full on the VPS, nothing else. No file
outside §4 was touched (V7). The one authorised VPS write — the scratch directory
`/var/lib/crypto-auto/tz80` — and V5's four transient units are gone, proven below.

## Files Created

| File | Lines | MD5 |
|---|---:|---|
| `vps/units/crypto-score-forming.service` | 20 | `6c1e8efc1b969929351a9276906139e8` |
| `vps/units/crypto-score-forming.timer` | 9 | `2ab7dda47812ca79212c74e49cf14c18` |

## Files Modified

| File | Lines after | MD5 after | numstat |
|---|---:|---|---|
| `vps/book.py` | 354 | `33c764fa584507fa8a6a121a18f571d8` | +71 −21 |
| `vps/manifest` | 11 | `0a2518c1fc7fd989ef2dfd8aa770beef` | +1 −0 |
| `vps/paper.py` | 1967 | `f6970999e177fae27bfa78ef9d252b17` | +24 −4 |
| `vps/score.py` | 528 | `91503ec6cecb05d094dc0b8ff47a7889` | +305 −94 |
| `vps/selftest.py` | 3882 | `5963c21b6c869b49d9a151b3aeac0ce7` | +390 −61 |

## Files Renamed

None.

## Files Deleted

None. The TZ's `## Files to Delete` reads "None".

## Implementation Summary

The change is §10's patch, written by the Architect and applied unmodified. The session
applied it, proved its bytes, and ran the validation; it wrote no line of code of its own
and hand-edited nothing — B2's seven digests are the authority for that, not a description.

What the patch builds, as §1 states it:

1. **`vps/book.py`** — `replay(bars, open_now=None, scale=None)` gains the plan: a day that
   reaches the entry plus `scale` times the initial risk without reaching the stop closes
   half there, or at the open where the day opened beyond it, and the rest's stop moves to
   the entry from the next day on. `SCALE_R = 2.0`. `result_r()` prices such a trade;
   `levels()` gives a position its target and, once half has closed, the day, the price, the
   rest's stop and an open R with the closed half in it; `live_day()` returns the closed days
   and the day still forming; `state_of()` is the state of one symbol's bars; `--live --scale 2`
   and `--archive --scale 2` print the plan. Without `scale` the rule's path is untouched.
2. **`vps/score.py`** — the daily close now keeps two ledgers: the rule's `score-ledger/` as
   TZ-79 left it, and the plan's `score-plan/` beside it, one closed trade a file with
   TZ-79 §3's ten keys. The alert is driven by the plan. `--forming` is the look.
3. **`vps/paper.py`** — `ceilings(own)`, `copy_lev(dist)` and `copy_size(own, dist)` moved out
   of `copy_text()`, so the copy line and the book alert share one implementation of the
   ceilings, the leverage and the size (inv. 38).
4. **`vps/selftest.py`** — section AB re-specified for the plan and the look, 62 → 117 checks.
5. **`vps/units/crypto-score-forming.service`**, **`.timer`** and the manifest's eleventh
   line — the look, daily at 15:10 UTC, `OnCalendar=*-*-* 15:10:00 UTC`, no `Persistent=`.

**Stage B1 — the patch, extracted by the TZ's one command:**

```sh
awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-80-plan-target-size.md > /tmp/tz80.patch
```

```text
$ wc -l < /tmp/tz80.patch
1404
$ md5sum /tmp/tz80.patch
2fe51ecd677d5f4ac18825c85072cb2f  /tmp/tz80.patch
```

1404 lines and `2fe51ecd677d5f4ac18825c85072cb2f` — the patch as §10 writes it. The upload
stripped no blank context line, so B1's hash held and B2 decided nothing it had to.

**Stage B2 — `git apply /tmp/tz80.patch`, exit 0.** The seven files came out at exactly the
lines and MD5s B2 requires:

```text
vps/book.py                                     354  33c764fa584507fa8a6a121a18f571d8
vps/manifest                                     11  0a2518c1fc7fd989ef2dfd8aa770beef
vps/paper.py                                   1967  f6970999e177fae27bfa78ef9d252b17
vps/score.py                                    528  91503ec6cecb05d094dc0b8ff47a7889
vps/selftest.py                                3882  5963c21b6c869b49d9a151b3aeac0ce7
vps/units/crypto-score-forming.service           20  6c1e8efc1b969929351a9276906139e8
vps/units/crypto-score-forming.timer              9  2ab7dda47812ca79212c74e49cf14c18
```

Every one equals B2's table. No hand edit was made, and none would have been permitted.

**Stage B3** — committed locally before stage C, as `e7d2b50`, and pushed at stage D.

## Validation

### Stage A — readings, no writes

**A0 — contract §4a steps 1–6.** This file read in full; `git fetch --all --prune` run before
anything was assessed; `git rev-parse --is-shallow-repository` printed `false`, so no
`--unshallow` was needed; the TZ located and read in full; the fingerprint gate run (below);
repository state verified across all branches. The tree was clean at the start
(`git status --porcelain` empty) and `HEAD` equalled `origin/main` at `878eee3`.

**The fingerprint gate (§5), cut by the map's own table structure.** The anchor list was taken
from the map's `## 0. Fingerprint` block — the table whose header row names `Anchor`, every row
between its separator line and its end — never by matching anchor names, and the TZ header's
own table was cut the same way and compared row against row:

```text
map anchor table: rows between separator and end = 7
TZ-80 anchor table: rows between separator and end = 7
rows compared = 7

TZ quotes every map row, character for character, in order: YES
```

The table's own row count is 7 and the number compared is 7 — equal, so the cut is not
hiding a row. Per anchor, the command and the text the match returned are under
`## Fingerprints` below. Revision string found: `**Revision 2026-11-13-a.**`; revision string
required by the TZ header: `**Revision 2026-11-13-a.**` — equal in both directions.

**A1 — the added files at their lines and MD5.** Every one of the five files §10 modifies
was equal to §0 before the patch, so A1 did not stop the TZ; the four reported files were
equal as well, and so were the map's own four. Measured values are under `## Fingerprints`.
`EXECUTOR-INSTRUCTIONS.md` line 3 reads `**Version 31.**`, so the version requirement is met
and nothing is BLOCKED.

**A2 — the baseline selftest from `main`, on the VPS.** The worktree's `vps/` tree was
byte-identical to `origin/main` (`git diff --stat origin/main -- vps/` empty) when this ran.

```text
$ python3 vps/selftest.py        # exit 0
selftest: sections 28 checks 724 failed 0 empty 0
section AB: checks 62 failed 0
section W: checks 204 failed 0
```

Identical to the Architect's measurement on `de3763c`'s tree, so no divergent baseline had to
be recorded. The per-section counts are in the table under V3.

**A3 — the live state, kept for V7 and V8.**

```text
$ python3 -c "import json; d=json.load(open('/var/lib/crypto-auto/score.json')); print(d['v'], d['asof'])"
1 2026-11-14
$ ls /var/lib/crypto-auto/score-ledger | wc -l
3
$ test -e /var/lib/crypto-auto/score-plan; echo $?
1
$ test -e /var/lib/crypto-auto/score-forming; echo $?
1
$ systemctl list-timers --all --no-legend | grep -c crypto-score
1
```

`1` and a date, a count, `1`, `1`, `1` — exactly A3's expectation: TZ-79's record and timer,
no plan ledger and no look.

### Stage C — V1 to V9

**V1. Syntax.** `python3 -m py_compile vps/book.py vps/paper.py vps/score.py vps/selftest.py`
— exit 0. The `__pycache__` it wrote was removed before the commit; the tree is clean and
`vps/__pycache__` no longer exists.

**V2. The bytes.** B2's seven files re-measured after the commit, at B2's lines and MD5s —
the table under `## Files Created` and `## Files Modified` carries them, every value equal.
And:

```text
$ python3 -c "print(sum(0x400 <= ord(c) <= 0x4ff for f in ('vps/book.py', 'vps/score.py') for c in open(f, encoding='utf-8').read()))"
0
```

`0` — no raw Cyrillic character in either program.

**V3. Selftest on the branch, on the VPS.** Exit 0.

```text
selftest: sections 28 checks 779 failed 0 empty 0
section AB: checks 117 failed 0
section W: checks 204 failed 0
section X: checks 19 failed 0
```

Required and found: 779 checks, 0 failed, 0 empty; AB 117, W 204, X 19. **Every other
section's count equal to A2's** — proven by diffing the two runs' `section` lines rather than
asserted:

```text
$ diff <(grep '^section' a2-selftest.txt) <(grep '^section' v3-selftest.txt)
28c28
< section AB: checks 62 failed 0
---
> section AB: checks 117 failed 0
```

One line differs out of 28 — section AB, 62 → 117, which is the change this TZ makes. The
full side-by-side:

| Section | A2 (`main`) | V3 (branch) |
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
| W | 204 | 204 |
| X | 19 | 19 |
| Y | 54 | 54 |
| Z | 23 | 23 |
| AA | 26 | 26 |
| AB | **62** | **117** |
| **total** | **724** | **779** |

`724 + 55 = 779`, and the 55 is section AB's `117 − 62`. Every section failed 0 in both runs.
Python on this host is 3.12.3; the Architect measured the same figures under 3.11, 3.12 and 3.13.

**V4. Negative controls (inv. 22).** Extracted by the TZ's one command:

```sh
awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-80-plan-target-size.md > /tmp/tz80-controls.py
```

```text
$ wc -l < /tmp/tz80-controls.py
80
$ md5sum /tmp/tz80-controls.py
e652d6c9672fc0b62ce494066aa64f1a  /tmp/tz80-controls.py
```

80 lines and `e652d6c9672fc0b62ce494066aa64f1a` — the script as §9 writes it. Run from the
clone's root, on the branch, its output was **147 lines, MD5 `74f92aa4687831cb7da67cec6ffd7e15`
— byte-identical to the block §9 prints after the script** (`diff` of the extracted expected
block against the actual output printed nothing), and `git status --porcelain` printed nothing
afterwards. All twenty-one controls turned the selftest red (`exit=1`), each restored its file
(`restored=yes`), and the run that follows them is green. The output verbatim is under
`## Test Results`.

**V5. The exchange, read from this machine, on a copy of the live state.** The scratch tree was
installed exactly as §6 commands it — `vps/*.py`, `analyst/owner.json` and `index.html` beside
it, `score.json` and `score-ledger` copied with `cp -a` — and `run80` is §6's `systemd-run`
function verbatim: `--uid=cryptoauto --gid=cryptoauto`, `ProtectSystem=strict`,
`ReadWritePaths=/var/lib/crypto-auto/tz80`, `MemoryMax=64M`,
`Environment=PYTHONDONTWRITEBYTECODE=1`, `--state`/`--outbox` into the scratch directory. Every
required shape held; the commands, the lines and both alerts in full are under
`## Test Results`.

- *the first run* — exit 0; the line carries `symbols=31 read=31` (inv. 22 satisfied: `read` is
  31, not 0), `asof=2026-11-14`, the UTC day before the run of 15.11.2026, `look=-` and
  `alert=yes`; exactly one file in the scratch outbox, `kind` `alert`, its first line carrying
  «СДЕЛКИ ПРАВИЛА — подключено»; **all 9 lines that name an entry are each followed by a line
  beginning «🎯 цель» carrying «объём» and «маржа»** — matched on `· вход ` + backtick, so the
  footer «…стоп остатка перенести на вход» and the «Вход — по рынку…» legend, which merely
  contain the word, are not miscounted as entries; `state/score.json` parses with `v` 2, a key
  `rule` and a key `look` that is `null`; `state/score-plan` holds 4 files, equal to the line's
  `ledger=4`, each parsing to TZ-79 §3's ten keys **in that order** — `symbol`, `side`,
  `t_entry`, `entry`, `stop`, `t_exit`, `exit`, `why`, `r`, `seen`; and every file listed in
  `/tmp/tz80-rule-before.txt` is in the rule ledger after the run **with the same inode and the
  same modification time** (`diff` of the two `ls -li --time-style=full-iso` listings printed
  nothing).
- *the second* — `opened=0 scaled=0 closing=0 closed=0 alert=no`, and no second file in the
  scratch outbox (the outbox still held one file, the same name and size).
- *the third, the look* — exit 0; one line, §3's, with `symbols=31 read=31`;
  `state/score-forming/2026-11-15.json` parses to §3's nine keys **in their order** — `v`, `k`,
  `ts`, `day`, `symbols`, `unread`, `stopped`, `scaled`, `entries` — at mode `0640`; the scratch
  outbox holds exactly one more file, where the line reads `alert=yes`, its first line carrying
  «СНИМОК ДНЯ»; and `state/score.json`, `state/score-plan` and `state/score-ledger` are byte for
  byte what the second run left (md5 listing of all eight files identical before and after).
- *the fourth* — exit 0, the one line `score: forming day=2026-11-15 already looked at, nothing
  written`, and **no new file and no changed file anywhere under the scratch directory**: an md5
  listing of every file under `/var/lib/crypto-auto/tz80` taken before and after the run diffed
  empty.

Then, once, from the scratch tree as `cryptoauto`, `book.py --live --scale 2 BTCUSDT ETHUSDT`
printed two lines, each `"state": "short"` and **each carrying `target`**, and the same command
without `--scale 2` printed two lines, **neither carrying `target`** — 2 of 2 lines against
0 of 2. All four lines are quoted under `## Test Results`.

Afterwards `rm -r /var/lib/crypto-auto/tz80` (the directory is gone: `test -e` reports absent),
and `systemctl list-units --all --no-legend 'run-u*.service'` printed nothing — none of this
session's four transient units (`run-u6105` … `run-u6108`, all started `--collect`) is left
behind. The broader glob `'run-*'` lists only pre-existing mounts belonging to other services
(`run-credentials-crypto-bot.service.mount` and the like) and `/run/user/0`, none of them this
session's.

**V6. The units.**

```text
$ systemd-analyze verify vps/units/crypto-score-forming.service vps/units/crypto-score-forming.timer
exit=0, no output
$ systemd-analyze verify vps/units/*
exit=0, no output
```

Both exit 0 with no output, so the installer's precondition holds for the whole unit directory.

**V7. Scope.**

```text
$ git diff --numstat origin/main...HEAD
71	21	vps/book.py
1	0	vps/manifest
24	4	vps/paper.py
305	94	vps/score.py
390	61	vps/selftest.py
20	0	vps/units/crypto-score-forming.service
9	0	vps/units/crypto-score-forming.timer
```

Exactly seven lines, each equal to V7's table line for line and figure for figure. Nothing
outside §4 moved: `index.html`, `main.py`, every other unit, `bench.yml`, `analyst/**`, the map
and the contracts are untouched.

**V8. Nothing in effect before the merge.** A3's five commands again:

```text
1 2026-11-14
3
1
1
1
```

`1` and a date, a count, `1`, `1`, `1` — byte for byte A3's readings. The live record is still
TZ-79's `v` 1; no plan ledger and no look exist on the live state; one score timer is known to
systemd. **The day in the first line did not move** — `asof` is still `2026-11-14` and
`/var/lib/crypto-auto/score.json` still carries its 00:10 timestamp and 5483 bytes — so the
timer did not run during the session. Nothing under `/var/lib/crypto-auto` but the scratch
directory was written, no unit was created, changed, enabled or restarted, and the bot's outbox
received nothing from this session: V5's alerts went to the scratch outbox, which was deleted.

**V9. `bench.yml`.** `index.html` and `main.py` are untouched (V7), so the standing checks of
§9 and map §6 item 1 do not apply and were not run. Which workflows executed on a runner is
under `## CI Execution`, read from the GitHub API rather than assumed.

**No regression.** Every section but AB keeps A2's count and is green (V3) — W's 204 among
them, with the copy line now on `paper.py`'s shared `ceilings()`, `copy_lev()` and
`copy_size()`, and X's 19, with the rule's replay unchanged — and no file outside §4 moved
(V7). Controls 13 and 14 are the evidence that the shared functions are load-bearing in both
callers: breaking `ceilings()` turned six section-W checks and two section-AB checks red in
one run, and breaking `copy_lev()` turned three AB checks red including «the copy line's
margin is the same function's».

## Test Results

### V4 — twenty-one negative controls, output verbatim

```text
CONTROL 1 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 8 empty 0
  section AB: checks 117 failed 8
  FAIL section AB: the day the target is reached: one alert, half closed at 113.8 and the rest's stop at the entry
  FAIL section AB: record's open position after the target: its day, the stop now at the entry, half its R banked
  FAIL section AB: after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop
  FAIL section AB: the close after it tells the target with the rest's stop, which the look does not move
  FAIL section AB: a day that has reached the rest's stop at the entry: told as done, at 105
  FAIL section AB: the plan's trade: half at the target the day it is reached, its stop the initial one
  FAIL section AB: after the target, a day through the entry closes the rest at the entry; its R is half the target's
  FAIL section AB: --live --scale 2 prints the plan's state: the target's day and the stop at the entry
CONTROL 2 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: the plan's R: half the move to the target and half to the exit, the whole funding to the target's day and half after it
  FAIL section AB: the close is told with the plan's R, and the plan's record follows it
  FAIL section AB: the record totals the plan and the rule apart: one trade each, a null profit factor where nothing lost
CONTROL 3 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 668 failed 1 empty 0
  section AB: checks 6 failed 1
  FAIL section AB raised KeyError: 'target'
CONTROL 4 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 21 empty 0
  section AB: checks 117 failed 21
  FAIL section AB: baseline: the entry due today, two lines -- fill and stop 105 - 2 x 2.2; the target 105 + 2 x 4.4, and 150 USDT over 4.4 of 105 as 3580 USDT, 1193 of margin at 3x
  FAIL section AB: record's open position: the entry due, its stop and target, no open R, no target reached
  FAIL section AB: the day the target is reached: one alert, half closed at 113.8 and the rest's stop at the entry
  FAIL section AB: record's open position after the target: its day, the stop now at the entry, half its R banked
  FAIL section AB: a close below the 20-day low: the exit due today is told once, with no row yet
  FAIL section AB: the plan's R: half the move to the target and half to the exit, the whole funding to the target's day and half after it
  FAIL section AB: the close is told with the plan's R, and the plan's record follows it
  FAIL section AB: the record totals the plan and the rule apart: one trade each, a null profit factor where nothing lost
  FAIL section AB: after TZ-79's record: an entry since its day prints in full, with its target, the majors first
  FAIL section AB: after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop
  FAIL section AB: an entry without the owner's file: two lines, the target alone on the second, no size, no ceilings
  FAIL section AB: the look: a close below the 55-day low would open a short -- the last price, the level it crossed, the stop 2 x 2.15 above it and the target 4 x 2.15 below, BTC before the others
  FAIL section AB: the look: a close above the 55-day high would open a long -- the stop 2 x 2.1 below the last price, the target 4 x 2.1 above
  FAIL section AB: a day that has reached the target: told as done, half closing at 113.8, with no candidate's last line
  FAIL section AB: the close after it tells the target with the rest's stop, which the look does not move
  FAIL section AB: a day that has reached the rest's stop at the entry: told as done, at 105
  FAIL section AB: a day that opened beyond the short's stop and would close above the 55-day high: the stop told at the open, and the long a candidate with the stop 2 x 2.55 below the last price
  FAIL section AB: the plan's trade: half at the target the day it is reached, its stop the initial one
  FAIL section AB: the moved stop acts from the next day: the target's day reaching below the entry closes nothing more
  FAIL section AB: after the target, a day through the entry closes the rest at the entry; its R is half the target's
  FAIL section AB: --live --scale 2 prints the plan's state: the target's day and the stop at the entry
CONTROL 5 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: the exit due is not told twice on its day
CONTROL 6 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 4 empty 0
  section AB: checks 117 failed 4
  FAIL section AB: a written trade is neither written, told nor asked about again
  FAIL section AB: a replay that disagrees with a written trade: its file stands byte for byte, and is counted
  FAIL section AB: a file that stands is never reopened: the same inode and the same modification time
  FAIL section AB: a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told
CONTROL 7 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 2 empty 0
  section AB: checks 117 failed 2
  FAIL section AB: a close found more than RETRY_DAYS after its day: counted late, no file written, nothing told
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written and told
CONTROL 8 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: prints with a day missing inside the span: nothing written, the trade pending
  FAIL section AB: an answer that is not a list of prints: nothing written, the trade pending
  FAIL section AB: the prints read in three pages give the same R, and the late close is told once
CONTROL 9 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a trade entered before GO_LIVE is no file of the ledger
CONTROL 10 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: the target is told once: the next day says nothing
CONTROL 11 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: after TZ-79's record: an entry since its day prints in full, with its target, the majors first
  FAIL section AB: the day's entries print BTC ETH SOL BNB XRP first, then the others in the list's order
  FAIL section AB: the close after it: both candidates are entries, and the close counts the look -- 2 of 2 named, 2 made
CONTROL 12 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: after TZ-79's record: one alert under the baseline's head, the plan's closes filled and none told
  FAIL section AB: after TZ-79's record: the plan's record is in the score line, the legend once
  FAIL section AB: after TZ-79's record: a position it had told prints on one line, its target reached and the rest's stop
CONTROL 13 vps/paper.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 8 empty 0
  section W: checks 204 failed 6
  section AB: checks 117 failed 2
  FAIL section W: the open signal, character for character: the whale's facts and the copy sized at 0.5% of 30 000
  FAIL section W: the short open: red dot, the copy's stop above, whale 2, a short copy
  FAIL section W: a 10.7% stop sizes the copy at 1402 USDT, the third LONG of six
  FAIL section W: six open LONG signals already: the seventh is a skip
  FAIL section W: a full LONG side leaves a SHORT copy open
  FAIL section W: the copy line counts the account's open episodes, this one and the other picks'
  FAIL section AB: under an entry: what the target means, when to enter, the owner's ceilings, each once and in that order
  FAIL section AB: the ceilings are paper.ceilings: 3 % and 5 % at 0.5 % hold 6 and 10
CONTROL 14 vps/paper.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 3 empty 0
  section AB: checks 117 failed 3
  FAIL section AB: the leverage is COPY_LEV while the stop stands within a quarter of the entry, 2x to a third, 1x beyond
  FAIL section AB: an entry whose stop stands 30 % away: 500 USDT, its margin 250 at 2x, since 3x would liquidate first
  FAIL section AB: the copy line's margin is the same function's: a copy whose stop is 30 % away is stated at 2x
CONTROL 15 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a day already looked at: exit 0, nothing read, nothing told, its record not reopened
CONTROL 16 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 13 empty 0
  section AB: checks 117 failed 13
  FAIL section AB: the look: the line reads day=1970-03-02 symbols=3 read=2 unread=1, two entries and nothing else, alert=yes
  FAIL section AB: the look: one alert, of kind alert, its head the day and the nine hours to its close
  FAIL section AB: the look: a close below the 55-day low would open a short -- the last price, the level it crossed, the stop 2 x 2.15 above it and the target 4 x 2.15 below, BTC before the others
  FAIL section AB: the look: a close above the 55-day high would open a long -- the stop 2 x 2.1 below the last price, the target 4 x 2.1 above
  FAIL section AB: the look: a candidate is named one, and the last line says the close alone confirms it
  FAIL section AB: the look's record: v 1, k score-forming, its day, the unread symbol, the entries it named with their sides
  FAIL section AB: the close after it: both candidates are entries, and the close counts the look -- 2 of 2 named, 2 made
  FAIL section AB: a stop of an earlier day is not the look's to tell, nor an entry made at today's open a candidate
  FAIL section AB: a candidate the close took back: no entry is told, and the close counts 0 of 1 named, 0 made
  FAIL section AB: a day that has reached the target: told as done, half closing at 113.8, with no candidate's last line
  FAIL section AB: a day that has reached the rest's stop at the entry: told as done, at 105
  FAIL section AB: an entry made at today's open and stopped today is a stop told, at 100.6
  FAIL section AB: a day that opened beyond the short's stop and would close above the 55-day high: the stop told at the open, and the long a candidate with the stop 2 x 2.55 below the last price
CONTROL 17 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 2 empty 0
  section AB: checks 117 failed 2
  FAIL section AB: an entry made at today's open and stopped today is a stop told, at 100.6
  FAIL section AB: a symbol whose forming day is not today is unread, and nothing of it is told
CONTROL 18 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a stop of an earlier day is not the look's to tell, nor an entry made at today's open a candidate
CONTROL 19 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: the look with no symbol read: exit 4, nothing written, nothing told
CONTROL 20 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a candidate the close took back: no entry is told, and the close counts 0 of 1 named, 0 made
CONTROL 21 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 779 failed 1 empty 0
  section AB: checks 117 failed 1
  FAIL section AB: a day that opened beyond the short's stop and would close above the 55-day high: the stop told at the open, and the long a candidate with the stop 2 x 2.55 below the last price
FINAL exit=0 selftest: sections 28 checks 779 failed 0 empty 0
```

147 lines, MD5 `74f92aa4687831cb7da67cec6ffd7e15` — equal to §9's expected block, and
`git status --porcelain` printed nothing after the run.

### V5 — the four runs

The scratch tree, as root:

```sh
install -d -o cryptoauto -g cryptoauto -m 0750 /var/lib/crypto-auto/tz80 /var/lib/crypto-auto/tz80/vps \
    /var/lib/crypto-auto/tz80/state /var/lib/crypto-auto/tz80/outbox /var/lib/crypto-auto/tz80/analyst
install -o cryptoauto -g cryptoauto -m 0640 vps/*.py /var/lib/crypto-auto/tz80/vps/
install -o cryptoauto -g cryptoauto -m 0640 analyst/owner.json /var/lib/crypto-auto/tz80/analyst/
install -o cryptoauto -g cryptoauto -m 0640 index.html /var/lib/crypto-auto/tz80/
cp -a /var/lib/crypto-auto/score.json /var/lib/crypto-auto/score-ledger /var/lib/crypto-auto/tz80/state/
ls -li --time-style=full-iso /var/lib/crypto-auto/tz80/state/score-ledger > /tmp/tz80-rule-before.txt
run80() { systemd-run --wait --collect --pipe --uid=cryptoauto --gid=cryptoauto -p ProtectSystem=strict \
    -p ReadWritePaths=/var/lib/crypto-auto/tz80 -p MemoryMax=64M -p Environment=PYTHONDONTWRITEBYTECODE=1 \
    /usr/bin/python3 /var/lib/crypto-auto/tz80/vps/score.py \
    --state /var/lib/crypto-auto/tz80/state --outbox /var/lib/crypto-auto/tz80/outbox "$@"; }
run80; run80; run80 --forming; run80 --forming
```

Every line the four runs printed, in order (the `Running as unit` / `Finished with result`
lines are `systemd-run`'s own):

```text
# run 1, exit 0
Running as unit: run-u6105.service
score: asof=2026-11-14 symbols=31 read=31 unread=0 open=29 opened=9 scaled=0 closing=0 closed=0 pending=0 late=0 disagree=0 ledger=4 rule=3 look=- alert=yes
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 15.561s
CPU time consumed: 425ms
Memory peak: 1.8M
Memory swap peak: 0B

# run 2, exit 0
Running as unit: run-u6106.service
score: asof=2026-11-14 symbols=31 read=31 unread=0 open=29 opened=0 scaled=0 closing=0 closed=0 pending=0 late=0 disagree=0 ledger=4 rule=3 look=- alert=no
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 16.256s
CPU time consumed: 400ms
Memory peak: 888.0K
Memory swap peak: 0B

# run 3, --forming, exit 0
Running as unit: run-u6107.service; invocation ID: 76f8b94719844a0fa52426b1512f033a
score: forming day=2026-11-15 symbols=31 read=31 unread=0 stopped=0 scaled=1 entries=0 alert=yes
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 12.834s
CPU time consumed: 385ms
Memory peak: 492.0K
Memory swap peak: 0B

# run 4, --forming, exit 0
Running as unit: run-u6108.service
score: forming day=2026-11-15 already looked at, nothing written
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 160ms
CPU time consumed: 118ms
Memory peak: 676.0K
Memory swap peak: 0B
```

**The first run's alert, in full** — `kind` `alert`, the only file in the scratch outbox. The
first message the owner receives after the merge differs from this only by the day:

```text
📈 **СДЕЛКИ ПРАВИЛА — подключено** · закрытие дня 14.11
🔴 **Шорт SUI** · вход `0.7006` · стоп `0.81777` (+16.7%)
🎯 цель `0.46626` (−33.4%) · объём `897` USDT · маржа `299` при 3x
🔴 **Шорт LINK** · вход `8.879` · стоп `10.2798` (+15.8%)
🎯 цель `6.0774` (−31.6%) · объём `951` USDT · маржа `317` при 3x
🔴 **Шорт RENDER** · вход `1.361` · стоп `1.5909` (+16.9%)
🎯 цель `0.9012` (−33.8%) · объём `888` USDT · маржа `296` при 3x
🔴 **Шорт NEAR** · вход `3.028` · стоп `3.7506` (+23.9%)
🎯 цель `1.5828` (−47.7%) · объём `629` USDT · маржа `210` при 3x
🔴 **Шорт AVAX** · вход `7.098` · стоп `8.2693` (+16.5%)
🎯 цель `4.7554` (−33.0%) · объём `909` USDT · маржа `303` при 3x
🔴 **Шорт TAO** · вход `183.7` · стоп `214.869` (+17.0%)
🎯 цель `121.362` (−33.9%) · объём `884` USDT · маржа `295` при 3x
🔴 **Шорт SKY** · вход `0.05237` · стоп `0.059793` (+14.2%)
🎯 цель `0.037524` (−28.3%) · объём `1058` USDT · маржа `353` при 3x
🔴 **Шорт XMR** · вход `469.96` · стоп `539.866` (+14.9%)
🎯 цель `330.148` (−29.7%) · объём `1008` USDT · маржа `336` при 3x
🔴 **Шорт ARB** · вход `0.12792` · стоп `0.156159` (+22.1%)
🎯 цель `0.071442` (−44.2%) · объём `679` USDT · маржа `226` при 3x
📊 Счёт с 21.10.2026: закрыто **4** · **−4.13 R** · в плюсе 0
BTC ETH SOL BNB XRP: 1 · −1.02 R · остальные: 3 · −3.11 R
В сделке 29: лонг 0 · шорт 29 · по закрытию дня +24.40 R
🔴 **Шорт BTC** · стоп `75985.9` · цель `62298.2`
🔴 **Шорт XRP** · цель взята · стоп остатка `1.237`
🔴 **Шорт SOL** · цель взята · стоп остатка `91.95`
🔴 **Шорт ETH** · цель взята · стоп остатка `2126.26`
🔴 **Шорт BNB** · стоп `706.332` · цель `558.606`
🔴 **Шорт ONDO** · стоп `0.39539` · цель `0.22562`
🔴 **Шорт YFI** · стоп `2159.6` · цель `1476.8`
🔴 **Шорт AAVE** · стоп `132.376` · цель `77.248`
🔴 **Шорт FET** · стоп `0.16887` · цель `0.09216`
🔴 **Шорт ENA** · стоп `0.176185` · цель `0.06874`
🔴 **Шорт GRAM** · стоп `1.3593` · цель `0.9384`
🔴 **Шорт ADA** · стоп `0.20335` · цель `0.1354`
🔴 **Шорт BCH** · стоп `253.77` · цель `156.75`
🔴 **Шорт HYPE** · стоп `82.7235` · цель `51.393`
🔴 **Шорт HBAR** · стоп `0.078322` · цель `0.050206`
🔴 **Шорт XLM** · стоп `0.178758` · цель `0.129084`
🔴 **Шорт ALGO** · стоп `0.099571` · цель `0.063838`
🔴 **Шорт ZEC** · стоп `1281.85` · цель `569.534`
🔴 **Шорт UNI** · стоп `7.382` · цель `3.923`
🔴 **Шорт MORPHO** · стоп `2.21782` · цель `1.39246`
Цель: закрыть половину, стоп остатка перенести на вход; остаток — до сигнала «Выход сегодня».
Вход — по рынку в течение дня, пока цена не дошла до стопа.
⚠️ Ваш лимит: 6 сделок в одну сторону и 10 всего, каждая до −150 USDT — считайте вместе с открытыми.
R — один риск на сделку.
```

This is the baseline run of §3 — the live record was TZ-79's `v` 1, which knew no plan — and it
behaves as §3's baseline clause requires: it tells no close it fills (`closed=0`, and the
`📊 Счёт` line reports the four it filled into the plan ledger without telling them), prints in
full the nine entries made since that record's day, each with its target, its notional and its
margin, the five `MAJORS` ahead of the rest; then prints every other open position on one line
with its stop and target, or with «цель взята» and the rest's stop (XRP, SOL, ETH). Under the
entries, once each and in that order: what the target means, when to enter, and the owner's
ceilings from `paper.ceilings()` with «считайте вместе с открытыми».

**The third run's alert, in full** — the look, `kind` `alert`, the one further file in the
scratch outbox:

```text
⏱ **СНИМОК ДНЯ** · 15.11 · до закрытия дня 13 ч
🎯 **Цель достигнута:** BTC шорт — половина закрывается по `62298.2`
```

The day had reached BTC's target and would open nothing (`entries=0 stopped=0 scaled=1`), so the
look tells the target reached, with its price, and nothing else — no candidate line, and
therefore none of the candidate trailer, which §3 attaches to candidates. The look's record:

```json
{"v": 1, "k": "score-forming", "ts": "2026-11-15T10:51:26Z", "day": "2026-11-15",
 "symbols": 31, "unread": [], "stopped": [], "scaled": ["BTCUSDT"], "entries": []}
```

Nine keys in §3's order, mode `0640`, written once.

**The `book.py` pair**, from the scratch tree as `cryptoauto`:

```text
$ python3 /var/lib/crypto-auto/tz80/vps/book.py --live --scale 2 BTCUSDT ETHUSDT
{"asof": "2026-11-14", "atr20": 2580.6649999999986, "close": 64130.5, "entry": 71423.3, "entry_date": "2026-11-13", "entry_due": false, "exit_due": false, "exit_level": 81953.7, "r_open": 1.5983973944509378, "state": "short", "stop": 75985.87, "symbol": "BTCUSDT", "target": 62298.16000000001}
{"asof": "2026-11-14", "atr20": 103.47449999999999, "close": 1768.36, "entry": 2126.26, "entry_date": "2026-11-09", "entry_due": false, "exit_due": false, "exit_level": 2449.95, "r_open": 1.9283902196074802, "scale_date": "2026-11-14", "scale_px": 1740.7540000000004, "state": "short", "stop": 2319.013, "stop_now": 2126.26, "symbol": "ETHUSDT", "target": 1740.7540000000004}

$ python3 /var/lib/crypto-auto/tz80/vps/book.py --live BTCUSDT ETHUSDT
{"asof": "2026-11-14", "atr20": 2580.6649999999986, "close": 64130.5, "entry": 71423.3, "entry_date": "2026-11-13", "entry_due": false, "exit_due": false, "exit_level": 81953.7, "r_open": 1.5983973944509378, "state": "short", "stop": 75985.87, "symbol": "BTCUSDT"}
{"asof": "2026-11-14", "atr20": 103.47449999999999, "close": 1768.36, "entry": 2126.26, "entry_date": "2026-11-09", "entry_due": false, "exit_due": false, "exit_level": 2449.95, "r_open": 1.8567804392149583, "state": "short", "stop": 2319.013, "symbol": "ETHUSDT"}
```

Two lines each, both `short`. With `--scale 2` each carries `target`; without it, neither does,
and BTC's line is identical in the two runs key for key and digit for digit — the rule's path
does not move. ETH differs only in `r_open` and the three keys the plan adds (`scale_date`,
`scale_px`, `stop_now`), which is the closed half the plan banks on 2026-11-14 and the rule
does not.

### V5 — the rule ledger, before and after the first run

```text
$ cat /tmp/tz80-rule-before.txt
total 12
2085377 -rw-r----- 1 cryptoauto cryptoauto 190 2026-11-13 00:10:10.895354606 +0000 LITUSDT-1793318400000.json
2085375 -rw-r----- 1 cryptoauto cryptoauto 192 2026-11-13 00:10:10.894354598 +0000 TRXUSDT-1793318400000.json
2085376 -rw-r----- 1 cryptoauto cryptoauto 215 2026-11-13 00:10:10.894354598 +0000 TRXUSDT-1793491200000.json

$ ls -li --time-style=full-iso /var/lib/crypto-auto/tz80/state/score-ledger   # after run 1
total 12
2085377 -rw-r----- 1 cryptoauto cryptoauto 190 2026-11-13 00:10:10.895354606 +0000 LITUSDT-1793318400000.json
2085375 -rw-r----- 1 cryptoauto cryptoauto 192 2026-11-13 00:10:10.894354598 +0000 TRXUSDT-1793318400000.json
2085376 -rw-r----- 1 cryptoauto cryptoauto 215 2026-11-13 00:10:10.894354598 +0000 TRXUSDT-1793491200000.json
```

`diff` of the two printed nothing: the same three inodes and the same modification times. The
plan's four files were written beside them, in `score-plan/`, and the line's `rule=3` equals the
rule ledger's size while `ledger=4` equals the plan's.

### V6 — the units

```text
$ systemd-analyze verify vps/units/crypto-score-forming.service vps/units/crypto-score-forming.timer
(no output)   exit=0
$ systemd-analyze verify vps/units/*
(no output)   exit=0
```

## Deviations

None.

Two notes on how items were measured, neither a deviation from what the TZ requires:

1. **V5's entry-line check was matched on `· вход ` followed by a backtick**, not on the bare
   word. The alert's footer «…стоп остатка перенести на вход» and its legend «Вход — по рынку
   в течение дня…» both contain the word and name no entry; a bare substring match counts them
   as entry lines and then reports a failure that is the matcher's, not the program's. Matching
   the entry line's own shape gives 9 entry lines, each followed by its «🎯 цель» line with
   «объём» and «маржа» — and the two non-entry lines are listed in the evidence so the reader
   can see exactly what was excluded and why.
2. **The two `book.py` commands of V5 were run with `runuser -u cryptoauto -- env
   PYTHONDONTWRITEBYTECODE=1`.** The TZ says to run them "from the scratch tree as
   `cryptoauto`" and names no mechanism; `PYTHONDONTWRITEBYTECODE=1` is the same setting
   `run80` carries and keeps `__pycache__` out of the scratch tree. The scratch tree was
   deleted afterwards either way.

## Pre-existing Issues

None found. Every fingerprint the map's `## 0` block and the TZ's gate table name was equal to
the stated value — the map's own four files, the five files §10 modifies, and the four reported
files — so nothing is ahead of anything, and `## Fingerprints` records the measurements rather
than a difference. A2's baseline matched the Architect's measurement section for section, so no
divergent baseline had to be recorded either.

## Remaining Risks

1. **The look's first real alert will carry candidates; this session's did not.** V5's third run
   found `entries=0` because the market on 15.11.2026 at 10:51 UTC would open nothing on the
   list, so the candidate lines, their «≈» marking and the trailer «Кандидат — ещё не сделка…»
   were exercised by section AB's checks (controls 16, 20 and 21 turn thirteen, one and one of
   them red respectively) and not by a live read. The shape the owner will see on a day with
   candidates rests on the selftest, which is where the TZ puts it.
2. **The look was read at 10:51 UTC, not at its own hour.** Its timer fires at 15:10 UTC and the
   share of candidates the close confirms is hour-dependent (§1: 57 % at 04:00, 73 % at 15:00).
   V5 measured the program's shape, not the hour's accuracy; the 73 % figure is the Architect's
   measurement over 1 340 days, not this session's.
3. **The baseline alert is a one-time shape and was read once.** The first run after the merge
   will be the baseline — the live record is `v` 1 — and it prints nine entries plus every other
   open position. V5's first run produced exactly that message from a copy of the live state, so
   the shape is measured; what is not measured is the merge-day market, which will differ.
4. **Nothing of this TZ is in effect until the deployer installs the merge** (contract §7
   item 15). The look's timer is enabled by the deployer from `main`, through the manifest's
   eleventh line; this session enabled, started and restarted nothing, and V8 proves the live
   state is still TZ-79's.
5. **One score timer is known to systemd and will be two after the install.** V8 read
   `systemctl list-timers --all --no-legend | grep -c crypto-score` as `1`; the manifest now
   names eleven units, and whether the deployer's install leaves both timers enabled is a
   reading for the next run on that host, not a forecast this report may make.

## Commit

**Implementation commit** — made and pushed before this report was written, so its hash is a
measurement: `e7d2b50fa87a83ad8064adf4954e30874801cf47` on `claude/tz-80-plan-target-size`.

Message, §7's string verbatim:

```text
TZ-80: vps — the plan the owner trades, and a look at the day still forming: every entry with its target, its size and his ceilings, the plan scored apart from the rule, and at 15:10 UTC what the day has done and each entry its close would make
```

Contents: the seven files of §4 and nothing else — `vps/book.py`, `vps/manifest`,
`vps/paper.py`, `vps/score.py`, `vps/selftest.py`, `vps/units/crypto-score-forming.service`,
`vps/units/crypto-score-forming.timer`.

**This report's commit** carries §7's report message, and nothing is stated here about its
outcome:

```text
TZ-80: report — the plan the owner trades, and the look
```

Contents: `CryptoReports/TZ-80-plan-target-size-report.md`, one file.

## Pull Request

**https://github.com/seahomebatumi-ai/crypto-auto/pull/66** — `TZ-80: vps — the plan the owner
trades, and the look`, base `main`, head `claude/tz-80-plan-target-size`, body naming this TZ.
Opened by this session; the Boss merges it after the Architect's audit returns ПРИНЯТО.

## CI Execution

`.github/workflows/bench.yml` fires on `push` to `main` and `claude/**` with a `paths-ignore`
list that names only `journal/data/**`, `journal/out/**`, `journal/runs.jsonl`,
`analyst/state.json`, `analyst/live.json` and `analyst/log/**` — so this branch's seven changed
paths, all under `vps/`, clear its filter. Read from the GitHub API on the pushed branch:

| Run | Workflow | Event | Conclusion |
|---|---|---|---|
| `43706216637` | Bench gate | `push` | **success** |
| `43706238693` | Bench gate | `pull_request` | **success** |

Both on head SHA `e7d2b50`, both completed, both `success` on every job step. The gate's own
per-step counts, taken from the runner's log body with
`gh run view <id> -R seahomebatumi-ai/crypto-auto --log`, are unchanged by this branch and
identical on the two runs: step 4 `checks run: 74   FAIL 0` (`verify_bench.py`), step 14
`checks run: 506   FAIL 0` (`backtest_guard_bench.py`), and `PASS 372   FAIL 0` on the board
fuzzing step — the figures the map's `## 0` records at this revision (`14 steps, 1 336 181
checks`). Nothing this TZ changes is read by the gate, which is the expected result and is
reported as a reading, not as a forecast.

`main.yml` did not fire and could not: since TZ-23 its trigger is a `paths` ALLOW-list of two
literal paths — `main.py` and `.github/workflows/main.yml` — read from the file on this branch
and confirmed still an allow-list before the report's push (contract §8). Neither path is in
this change, and `CryptoReports/**` is in no allow-list anywhere. `backtest_bench.yml`,
`calib.yml` and `journal.yml` were not modified and are not triggered by `vps/**`.

The hosted gate is read by the audit, which opens the pull-request page to merge; the facts
this session can establish are above — the branch reached the remote at `e7d2b50`, the changed
paths clear the gate's filter, and the runs named above are what the API reported when this
section was written.

## Final Repository State

**The branch `claude/tz-80-plan-target-size`, pushed and measured at
`e7d2b50fa87a83ad8064adf4954e30874801cf47`.** It carries `origin/main` at `878eee3` plus one
commit, the implementation. `git diff --numstat origin/main...HEAD` prints exactly the seven
lines V7 requires; the working tree is clean, `vps/__pycache__` is gone, and no generated
artifact was committed.

On the VPS the session leaves nothing: `/var/lib/crypto-auto/tz80` is removed, V5's four
transient units are collected and `systemctl list-units --all --no-legend 'run-u*.service'`
prints nothing, no unit was created, changed, enabled or restarted, and the live state is
byte-unchanged — `score.json` is still TZ-79's `v` 1 at `asof` `2026-11-14`, the rule ledger
still holds its three files, and `score-plan` and `score-forming` do not exist.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

**`SYSTEM-MAP-CRYPTOCALCUL.md`** — revision string `**Revision 2026-11-13-a.**`;
**2802 lines**, MD5 `9d10f8da578b060db902c286323bdde3`. Equal to the pair the TZ header
reports (reported, not enforced).

**Anchors — the map's own table is 7 rows, 7 were compared, 7 matched.** Per anchor, the
command and the text the match returned (a fixed-string match prints the matched text itself):

| Anchor | Command | Text the match returned |
|---|---|---|
| revision | `grep -F -- '**Revision 2026-11-13-a.**' SYSTEM-MAP-CRYPTOCALCUL.md` | `**Revision 2026-11-13-a.**` |
| direction engine | `grep -F -- '### 3.12 Direction engine — veto cascade' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `grep -F -- '### 3.15 Catalyst registry' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.15 Catalyst registry` |
| exhaustion measure | `grep -F -- '### 3.16 List exhaustion — the day-range measure' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `grep -F -- '## 11. Analytical engine' SYSTEM-MAP-CRYPTOCALCUL.md` | `## 11. Analytical engine` |
| squeeze block | `grep -F -- '### 3.17 «РИСК ВЫНОСА» — the day'"'"'s own risk' SYSTEM-MAP-CRYPTOCALCUL.md` | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `grep -F -- '73. **An Architect-owned document never grows' SYSTEM-MAP-CRYPTOCALCUL.md` | `73. **An Architect-owned document never grows` |

Each anchor occurs **twice** in the map — once in the `## 0` table that publishes it and once in
the text it names, at lines 1044 (direction engine), 1434 (catalyst registry), 1531 (exhaustion
measure), 2534 (analytical engine), 1698 (squeeze block) and 2257 (newest invariant); the
revision string's two occurrences are both inside `## 0`, at lines 17 and 74, which is where a
revision string lives. So no anchor matched only its own table row.

**Files the map's `## 0` table lists** — measured on this branch, equal to the map's stated
pairs and to the TZ header's:

| File | Lines | MD5 | Required |
|---|---:|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | equal ✓ |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal ✓ |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | equal ✓ |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | equal ✓ |

**Files the TZ's gate table adds** — measured at stage A1, on `origin/main`'s tree, before the
patch:

| Added file | Lines | MD5 | Required | Result |
|---|---:|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 | `4390ee0b8bf1e8d7837afffcd7a5b803` | `**Version 31.**` | line 3 reads `**Version 31.**` ✓ |
| `vps/book.py` | 304 | `4b64b856fb80cfa810dcac015eb60b20` | equal, or A1 stops | equal ✓ |
| `vps/paper.py` | 1947 | `60018d258594aa629e6f8d5f0dc5c6d9` | equal, or A1 stops | equal ✓ |
| `vps/score.py` | 317 | `308c8661b54d843a682747e46752bd4e` | equal, or A1 stops | equal ✓ |
| `vps/selftest.py` | 3553 | `4816f38d10aa2711cc56fff29203c7a7` | equal, or A1 stops | equal ✓ |
| `vps/manifest` | 10 | `73d8fd4022bcf24996d4d3c41c6444c5` | equal, or A1 stops | equal ✓ |
| `vps/units/crypto-score.service` | 20 | `ca1e8d926d9ce2d9e2f2eabb4d7db41d` | reported | equal ✓ |
| `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` | reported | equal ✓ |
| `vps/writer.py` | 154 | `c07b1f71ef014e18448eb9313e185b73` | reported | equal ✓ |

**The seven files after the patch**, on the branch at `e7d2b50` — B2's and V2's table, measured
twice (after `git apply` and again after the commit), equal both times:

| File | Lines | MD5 |
|---|---:|---|
| `vps/book.py` | 354 | `33c764fa584507fa8a6a121a18f571d8` |
| `vps/manifest` | 11 | `0a2518c1fc7fd989ef2dfd8aa770beef` |
| `vps/paper.py` | 1967 | `f6970999e177fae27bfa78ef9d252b17` |
| `vps/score.py` | 528 | `91503ec6cecb05d094dc0b8ff47a7889` |
| `vps/selftest.py` | 3882 | `5963c21b6c869b49d9a151b3aeac0ce7` |
| `vps/units/crypto-score-forming.service` | 20 | `6c1e8efc1b969929351a9276906139e8` |
| `vps/units/crypto-score-forming.timer` | 9 | `2ab7dda47812ca79212c74e49cf14c18` |

**Artifacts extracted from the TZ:** `/tmp/tz80.patch` 1404 lines,
`2fe51ecd677d5f4ac18825c85072cb2f`; `/tmp/tz80-controls.py` 80 lines,
`e652d6c9672fc0b62ce494066aa64f1a`; V4's output 147 lines,
`74f92aa4687831cb7da67cec6ffd7e15`. All three equal the values the TZ states.

**The TZ itself:** `CryptoTZ/TZ-80-plan-target-size.md`, 2064 lines, MD5
`695bc28e69af20a8a4014e7ead2a9208`.
