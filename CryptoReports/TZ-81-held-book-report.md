# Implementation Report — TZ-81

## Status

COMPLETED.

The three files `§10` names carry `§10`'s patch, byte for byte, at the lines and MD5s `B2`
requires. Every validation item `V1`–`V8` ran and passed. The branch is pushed and pull
request #67 is open.

## Inbound Filing

None. The Boss uploaded `CryptoTZ/TZ-81-held-book.md` to `CryptoTZ/` under its canonical
filename in commit `ee1354e` («Add files via upload», 1731 lines), and `git fetch --all
--prune` brought it into this clone. Nothing was moved, renamed or copied.

```
$ git fetch --all --prune && git rev-parse --is-shallow-repository
false
$ git show --stat ee1354e | tail -3
    Add files via upload
 CryptoTZ/TZ-81-held-book.md | 1731 +++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 1731 insertions(+)
```

## Scope Executed

**Class: branch TZ** (contract §8). The TZ's `## Scope` names three written files outside
`CryptoReports/**` — `vps/book.py`, `vps/score.py`, `vps/selftest.py` — so the class is read
off the scope, not chosen, and a branch and a pull request follow.

Stages A, B, C and D of §5, in full:

- **A0** — contract §4a steps 1–6; the §0 fingerprint gate, every anchor cut from the map's
  own anchor table by the table's structure. Passed.
- **A1** — the added files of §0 at their lines and MD5. All seven equal; the TZ does not stop.
- **A2** — the baseline selftest on the VPS from `main`. `selftest: sections 28 checks 779
  failed 0 empty 0`, `section AB: checks 117 failed 0` — exactly the Architect's measurement.
- **A3** — the live state's four readings, kept for V7.
- **B1** — branch `claude/tz-81-held-book` from `origin/main`; the patch extracted by the one
  command the TZ gives, and nothing else:

  ````
  $ awk '/^```diff$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-81-held-book.md > /tmp/tz81.patch
  $ wc -l < /tmp/tz81.patch ; md5sum /tmp/tz81.patch
  1048
  24af804041772e14205749784937adcd  /tmp/tz81.patch
  ````

  1048 lines, MD5 `24af804041772e14205749784937adcd` — the figures §5 B1 states, so the upload
  stripped nothing and B2 decides on the patch as the Architect wrote it.
- **B2** — `git apply`, exit 0, the three files at B2's lines and MD5s. No hand edit.
- **B3** — the implementation commit, made locally before stage C.
- **C** — §6 in full: V1–V8.
- **D** — pushed; pull request #67 opened.

The VPS work stayed inside what §4 authorises: the scratch directory
`/var/lib/crypto-auto/tz81` and four transient `systemd-run` units, all gone before this
report. No unit was created, changed, enabled or restarted; nothing under
`/var/lib/crypto-auto` but that directory was written; the bot's outbox received nothing
from this session — the four runs wrote their one alert into the scratch outbox that `--outbox`
named.

## Files Created

None under `## Files to Create` — the TZ names none.

`CryptoReports/TZ-81-held-book-report.md` — this report, on the `CryptoReports/**`
direct-push path.

## Files Modified

| File | Before (lines / MD5) | After (lines / MD5) |
|---|---|---|
| `vps/book.py` | 354 / `33c764fa584507fa8a6a121a18f571d8` | 419 / `4e283c02783b4f959c49b613b4e518a5` |
| `vps/score.py` | 528 / `91503ec6cecb05d094dc0b8ff47a7889` | 613 / `eb76418a35e4c9389a80e61b1d449387` |
| `vps/selftest.py` | 3882 / `5963c21b6c869b49d9a151b3aeac0ce7` | 4101 / `25136248a1fba37be97af33b1e9a598c` |

Each "after" pair is the one `B2` requires, character for character.

## Files Renamed

None.

## Files Deleted

None. `/var/lib/crypto-auto/tz81`, the scratch directory §4 authorises on the VPS, was
removed at the end of V5; it is outside the repository.

## Implementation Summary

The session applied `§10`'s patch and proved its bytes; it wrote no line of its own. What the
patch builds, as `§1` and `§3` specify it:

**`vps/book.py`** — `MAJORS` moves here from `score.py`, which now reads `MAJORS = book.MAJORS`;
`AT_OPEN, ENTRY, IN_DAY` order one open's three phases; `rank(symbols)` gives the order one
open's entries are taken in — the `MAJORS` first, then the list's; `spans(symbol, trades, pos,
t_next)` reads each position as the walk needs it, with the moment its slot frees; `hold(books,
ranks, side_max, book_max, fixed)` is the walk itself, in time from an empty book, one entry
taken only where its side has room and the book has room, an entry not taken at its own open
never taken later, and `fixed` carrying forward what a record already decided; `archive(...,
ceilings=)` keeps only the trades `hold()` takes, and `--archive --hold SIDE,BOOK` reaches it
from the command line. `--hold` with `--live`, or a value that is not two positive counts, is
refused with exit 2. Without `--hold`, nothing `--live` or `--archive` prints moves.

**`vps/score.py`** — the daily close and the look now tell the book held. `day_ms()` gives a
UTC date's opening stamp; `record_of()` reads the last record; `holds(prev, ceilings)` says
whether that record holds a book under these ceilings; `book_held()` runs `book.hold()` over
the plan's positions entered since `GO_LIVE`, holding fixed what the last record decided up to
the open it told and carrying the spans it held on a symbol unread today. A third ledger,
`score-held/`, is the gate's; `score-plan/` keeps the plan's every entry and `score-ledger/`
the rule's, and `ledger_pass()` takes a shared `priced` map so a trade two ledgers write is
priced once. The alert gains one line, `T_OUT` — «⏸ **Вне лимита:**» — naming the plan's
entries the ceilings leave out, long before short and the `MAJORS` first in each; an entry left
out is an event and alone sends the alert. The record is `v` 3 with eighteen keys, adding
`ceilings`, `held`, `outside` and `plan`; the line adds `outside=`, `skipped=` and `plan=`. The
look's record is `v` 2, and a `v` 1 look is counted by no close. A run that cannot read the
owner's ceilings reads nothing, writes nothing, tells nothing and exits 6 — the close and the
look each with their own line. The entry's two lines now always carry the size and the margin,
because a run without the owner's file no longer reaches them.

**`vps/selftest.py`** — section AB re-specified for the book held: 117 checks to 145. The new
expectations are the Architect's, written before execution and derived in each check's own
text; the session edited no check (contract §7 item 2).

## Validation

### V1. Syntax

```
$ python3 -m py_compile vps/book.py vps/score.py vps/selftest.py
exit=0
```

### V2. The bytes

```
$ for f in vps/book.py vps/score.py vps/selftest.py; do printf "%-20s %6s  %s\n" "$f" "$(wc -l < $f)" "$(md5sum $f | cut -d' ' -f1)"; done
vps/book.py             419  4e283c02783b4f959c49b613b4e518a5
vps/score.py            613  eb76418a35e4c9389a80e61b1d449387
vps/selftest.py        4101  25136248a1fba37be97af33b1e9a598c
```

All three equal B2's table.

```
$ python3 -c "print(sum(0x400 <= ord(c) <= 0x4ff for f in ('vps/book.py', 'vps/score.py', 'vps/selftest.py') for c in open(f, encoding='utf-8').read()))"
0
```

No raw Cyrillic in any of the three (contract §7 item 7; the alert's Russian is `\uXXXX`
escapes, as `T_OUT` shows).

### V3. Selftest, on the VPS, on the branch

```
$ python3 vps/selftest.py ; echo exit=$?
...
section AB: checks 145 failed 0
selftest: sections 28 checks 807 failed 0 empty 0
exit=0
```

Required: exit 0, `sections 28 checks 807 failed 0 empty 0`, `section AB: checks 145 failed 0`.
Met.

**A2 and V3 per section, side by side.** Python 3.12.3 on the VPS, the one interpreter this
host carries; the Architect measured the same figures under 3.11, 3.12 and 3.13.

| Section | A2 (`main`) | V3 (branch) | Section | A2 | V3 |
|---|---:|---:|---|---:|---:|
| A | 32 | 32 | P | 21 | 21 |
| B | 12 | 12 | Q | 3 | 3 |
| C | 4 | 4 | R | 9 | 9 |
| D | 13 | 13 | S | 35 | 35 |
| E | 12 | 12 | T | 39 | 39 |
| F | 14 | 14 | U | 18 | 18 |
| G | 8 | 8 | V | 16 | 16 |
| H | 2 | 2 | W | 204 | 204 |
| I | 4 | 4 | X | 19 | 19 |
| J | 26 | 26 | Y | 54 | 54 |
| K | 2 | 2 | Z | 23 | 23 |
| L | 4 | 4 | AA | 26 | 26 |
| M | 19 | 19 | **AB** | **117** | **145** |
| N | 10 | 10 | | | |
| O | 33 | 33 | **total** | **779** | **807** |

`failed 0` on every section in both runs. The mechanical comparison:

```
$ diff <(grep '^section ' a2.out) <(grep '^section ' v3.out)
28c28
< section AB: checks 117 failed 0
---
> section AB: checks 145 failed 0
```

Exactly one section differs, and it is AB. X keeps its 19 — the rule's replay is unchanged.

### V4. Negative controls

````
$ awk '/^```python$/{f=1;next} /^```$/{if(f)exit} f' CryptoTZ/TZ-81-held-book.md > /tmp/tz81-controls.py
$ wc -l < /tmp/tz81-controls.py ; md5sum /tmp/tz81-controls.py
82
64bc4c5bc20d81ac211b1be97a4f5dd8  /tmp/tz81-controls.py
````

The script arrived as written. Run from the clone's root:

```
$ python3 /tmp/tz81-controls.py > v4.out ; echo exit=$?
exit=0
$ wc -l < v4.out ; md5sum v4.out
119
7e9a8f160d6e4c8f5ce0a1242981df47  v4.out
```

119 lines, MD5 `7e9a8f160d6e4c8f5ce0a1242981df47` — the required output, byte for byte. Every
one of the eighteen controls turned the selftest red and was restored (`restored=yes` on all
eighteen), and the nineteenth run — the final one, against the restored tree — is green.

```
$ git status --porcelain
$
```

Nothing. The working tree the controls edited eighteen times is exactly as they found it.

The output, verbatim:

```text
CONTROL 1 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 16 empty 0
  section AB: checks 145 failed 16
  FAIL section AB: one a side and two in all: the baseline tells the major's long and the short in full, and names the two longs left out on one line under them
  FAIL section AB: its line: open=2 outside=2 opened=2 skipped=2; its record: the ceilings 1 and 2, the two held, the two left out with their side and day, the plan's four open
  FAIL section AB: the short stopped inside its day is the book's trade, in its ledger as in the plan's; the long its stop day opened finds the long side full: named left out with the ceilings, and no entry told
  FAIL section AB: a target reached is told of the position held alone, not of the plan's two left out
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: the book held's ledger takes the trades it held, the plan's every entry: two files against four
  FAIL section AB: the close is told of the position held and of none left out, and the score is the book held's
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
  FAIL section AB: the look names the candidate the book would take, the major's long, and not the long it would leave out
  FAIL section AB: a stop the day has reached on a position the book left out is not the look's to tell
  FAIL section AB: hold: one open's entries are taken in rank order while their side has room -- the major's, then the list's
  FAIL section AB: hold: a stop frees its slot inside its day, after that open's entries -- the next open's entry is taken
  FAIL section AB: hold: an entry stopped on its own day held its slot through that open
  FAIL section AB: hold: an entry not taken at its own open is never taken, though a slot frees while it stands
CONTROL 2 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: hold: the book's ceiling binds across the sides -- two longs leave no room for a short at two in all
CONTROL 3 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written -- and, its entry never told, not the book's: nothing told, no file of the book held
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
CONTROL 4 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 15 empty 0
  section AB: checks 145 failed 15
  FAIL section AB: one a side and two in all: the baseline tells the major's long and the short in full, and names the two longs left out on one line under them
  FAIL section AB: its line: open=2 outside=2 opened=2 skipped=2; its record: the ceilings 1 and 2, the two held, the two left out with their side and day, the plan's four open
  FAIL section AB: a target reached is told of the position held alone, not of the plan's two left out
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: the book held's ledger takes the trades it held, the plan's every entry: two files against four
  FAIL section AB: the close is told of the position held and of none left out, and the score is the book held's
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
  FAIL section AB: the look names the candidate the book would take, the major's long, and not the long it would leave out
  FAIL section AB: a stop the day has reached on a position the book left out is not the look's to tell
  FAIL section AB: rank: the MAJORS first, then the others, each in the order given -- the list's
  FAIL section AB: hold: one open's entries are taken in rank order while their side has room -- the major's, then the list's
  FAIL section AB: hold: an entry stopped on its own day held its slot through that open
  FAIL section AB: the archive with ceilings keeps hold()'s trades: of two longs at one open, the major's alone
CONTROL 5 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: spans: a channel exit frees its slot at the open, a stop inside the day, a position that stands never, and one whose exit is due at the next open
CONTROL 6 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: the close run every day holds the very spans hold() takes over all the days at once
  FAIL section AB: spans: a channel exit frees its slot at the open, a stop inside the day, a position that stands never, and one whose exit is due at the next open
CONTROL 7 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 3 empty 0
  section AB: checks 145 failed 3
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: the close run every day holds the very spans hold() takes over all the days at once
  FAIL section AB: spans: a channel exit frees its slot at the open, a stop inside the day, a position that stands never, and one whose exit is due at the next open
CONTROL 8 vps/book.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: the archive with ceilings keeps hold()'s trades: of two longs at one open, the major's alone
CONTROL 9 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: ceilings that change make the next run a baseline: the book re-read under them from GO_LIVE, the trades they hold now written and none told
CONTROL 10 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
CONTROL 11 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written -- and, its entry never told, not the book's: nothing told, no file of the book held
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
CONTROL 12 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: a position entered before GO_LIVE holds no slot: it is named left out, and the long it would block is held
CONTROL 13 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 3 empty 0
  section AB: checks 145 failed 3
  FAIL section AB: the same close inside RETRY_DAYS, which is 60: written -- and, its entry never told, not the book's: nothing told, no file of the book held
  FAIL section AB: the book held's ledger takes the trades it held, the plan's every entry: two files against four
  FAIL section AB: the close is told of the position held and of none left out, and the score is the book held's
CONTROL 14 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 9 empty 0
  section AB: checks 145 failed 9
  FAIL section AB: one a side and two in all: the baseline tells the major's long and the short in full, and names the two longs left out on one line under them
  FAIL section AB: its line: open=2 outside=2 opened=2 skipped=2; its record: the ceilings 1 and 2, the two held, the two left out with their side and day, the plan's four open
  FAIL section AB: the short stopped inside its day is the book's trade, in its ledger as in the plan's; the long its stop day opened finds the long side full: named left out with the ceilings, and no entry told
  FAIL section AB: a target reached is told of the position held alone, not of the plan's two left out
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: an exit at an open frees its slot for that open's entry: the long due is told beside the exit due
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
  FAIL section AB: an entry once left out is never taken: the long that held the slot gone from the replay, the two left out stay out and nothing is told
  FAIL section AB: a position entered before GO_LIVE holds no slot: it is named left out, and the long it would block is held
CONTROL 15 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 2 empty 0
  section AB: checks 145 failed 2
  FAIL section AB: a position past its target keeps its slot: the next long is left out
  FAIL section AB: a position held on a symbol unread today keeps its slot as recorded: the next long is left out, and the record keeps the span
CONTROL 16 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: the look names the candidate the book would take, the major's long, and not the long it would leave out
CONTROL 17 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: a stop the day has reached on a position the book left out is not the look's to tell
CONTROL 18 vps/score.py exit=1 restored=yes
  selftest: sections 28 checks 807 failed 1 empty 0
  section AB: checks 145 failed 1
  FAIL section AB: the prints read in three pages give the same R, the plan's trade priced once for both its ledgers, and the late close is told once
FINAL exit=0 selftest: sections 28 checks 807 failed 0 empty 0
```

### V5. The exchange, read from this machine, on a copy of the live state

The scratch tree was built by `§6`'s commands as root: every program of `vps/` from the
branch, `analyst/owner.json` and `index.html` beside it, and a copy of the live
`score.json` and `score-ledger/`. `score-plan/` does not exist on the live host (A3), so its
`cp` was skipped by the `if` the TZ wrote for that case. The unit could write nothing but
`/var/lib/crypto-auto/tz81`.

```
$ ls -li --time-style=full-iso /var/lib/crypto-auto/tz81/state/score-* > /tmp/tz81-before.txt
$ cat /tmp/tz81-before.txt
total 12
2089231 -rw-r----- 1 cryptoauto cryptoauto 190 2026-11-13 00:10:10.895354606 +0000 LITUSDT-1793318400000.json
2089229 -rw-r----- 1 cryptoauto cryptoauto 192 2026-11-13 00:10:10.894354598 +0000 TRXUSDT-1793318400000.json
2089230 -rw-r----- 1 cryptoauto cryptoauto 215 2026-11-13 00:10:10.894354598 +0000 TRXUSDT-1793491200000.json
```

The four runs, every line they printed:

```text
$ run81                           # the first — the baseline
score: asof=2026-11-14 symbols=31 read=31 unread=0 open=6 outside=23 opened=0 skipped=23 scaled=0 closing=0 closed=0 pending=0 late=0 disagree=0 ledger=2 plan=4 rule=3 look=- alert=yes
exit=0

$ run81                           # the second
score: asof=2026-11-14 symbols=31 read=31 unread=0 open=6 outside=23 opened=0 skipped=0 scaled=0 closing=0 closed=0 pending=0 late=0 disagree=0 ledger=2 plan=4 rule=3 look=- alert=no
exit=0

$ run81 --forming                 # the third — the look
score: forming day=2026-11-15 symbols=31 read=31 unread=0 stopped=0 scaled=0 entries=0 alert=no
exit=0

$ run81 --forming                 # the fourth
score: forming day=2026-11-15 already looked at, nothing written
exit=0
```

Each run's unit reported `Finished with result: success`, `code=exited/status=0`, memory peak
1.6M against the 64M ceiling.

**The first run, by shape.** Required and met:

| Required | Measured |
|---|---|
| exit 0 | 0 |
| the last line is §3's line, `symbols=31` | `symbols=31`, one line printed, the shape `AB_LINE` matches |
| `read` at least 1 (inv. 22) | `read=31`, `unread=0` |
| `asof` the UTC day before the run | `asof=2026-11-14`; the run was `2026-11-15T21:23Z` (`date -u`) |
| `look=-` and `alert=yes` | both |
| exactly one file in the scratch outbox, of kind `alert` | `1794777832041-alert-1834047.json`, `"kind": "alert"` |
| its first line carries «СДЕЛКИ ПРАВИЛА — подключено» | `📈 **СДЕЛКИ ПРАВИЛА — подключено** · закрытие дня 14.11` |
| `score.json` parses with `v` 3 and the eighteen keys of §3 in their order | `v` 3; `['v','k','ts','asof','since','symbols','unread','ceilings','held','open','outside','closed','pending','late','disagree','look','plan','rule']`, 18 keys |
| `ceilings` `[6, 10]` | `[6, 10]` |
| `open` less `exit_due`: at most 6 of each `state`, 10 in all | 6 positions, all `short`, none `exit_due` → `{short: 6}`, 6 ≤ 10 |
| `open` + `outside` = `plan.open` | 6 + 23 = 29 = `plan.open` |
| `unread` empty → every `open` position has its span in `held` | true, by symbol and entry day |
| every `held` span whose last element is `null` is a position of `open` | 6 `null` spans, exactly the 6 `open` symbols |
| the line's `opened` equals the alert's «· вход `» lines | `opened=0`; 0 such lines |
| a line beginning «⏸ **Вне лимита:**» exists exactly where `outside` ≠ 0 | `outside=23`; exactly one such line |
| its names are exactly the record's `outside`, without `USDT` | identical, in the record's order |
| `score-held` holds as many files as `ledger=` | `ledger=2`; 2 files |
| each with a same-named `score-plan` file whose keys but `seen` equal its own | both: `True` |
| `score-plan` holds as many files as `plan=` | `plan=4`; 4 files |
| every file of `/tmp/tz81-before.txt` present after, same inode and same mtime | `diff` of before and after: identical |

The record's `held`, all eight spans — six standing, two freed, which are the book held's two
ledger files:

```json
["ETHUSDT",  -1, 1793318400000, [1793750400000, 2]]
["FETUSDT",  -1, 1793923200000, null]
["GRAMUSDT", -1, 1792800000000, null]
["HBARUSDT", -1, 1793318400000, null]
["TRXUSDT",   1, 1793318400000, [1793318400000, 2]]
["XLMUSDT",  -1, 1793318400000, null]
["XRPUSDT",  -1, 1793318400000, null]
["YFIUSDT",  -1, 1793318400000, null]
```

```
$ ls state/score-held state/score-plan
score-held:  ETHUSDT-1793318400000.json  TRXUSDT-1793318400000.json
score-plan:  ETHUSDT-1793318400000.json  LITUSDT-1793318400000.json
             TRXUSDT-1793318400000.json  TRXUSDT-1793491200000.json
```

**The alert of the first run, in full.** This is the first message the owner receives after the
merge, on its own day — the plan has twenty-nine open positions, the book holds six of them,
and the twenty-three his ceilings leave no room for are named on one line:

```text
📈 **СДЕЛКИ ПРАВИЛА — подключено** · закрытие дня 14.11
⏸ **Вне лимита:** шорт BTC, SOL, ETH, BNB, SUI, ONDO, LINK, RENDER, NEAR, AAVE, AVAX, ENA, TAO, ADA, BCH, HYPE, SKY, ALGO, ZEC, UNI, XMR, MORPHO, ARB
📊 Счёт с 21.10.2026: закрыто **2** · **−2.09 R** · в плюсе 0
BTC ETH SOL BNB XRP: 1 · −1.02 R · остальные: 1 · −1.07 R
В сделке 6: лонг 0 · шорт 6 · по закрытию дня +8.58 R
🔴 **Шорт XRP** · цель взята · стоп остатка `1.237`
🔴 **Шорт YFI** · стоп `2159.6` · цель `1476.8`
🔴 **Шорт FET** · стоп `0.16887` · цель `0.09216`
🔴 **Шорт GRAM** · стоп `1.3593` · цель `0.9384`
🔴 **Шорт HBAR** · стоп `0.078322` · цель `0.050206`
🔴 **Шорт XLM** · стоп `0.178758` · цель `0.129084`
Цель: закрыть половину, стоп остатка перенести на вход; остаток — до сигнала «Выход сегодня».
⚠️ Ваш лимит: 6 сделок в одну сторону и 10 всего, каждая до −150 USDT — считайте вместе с открытыми.
R — один риск на сделку.
```

**The second run.** Required `opened=0 skipped=0 scaled=0 closing=0 closed=0 alert=no`, no
second file in the scratch outbox, `held` equal to the first run's. All five counters are 0 and
`alert=no`; the outbox still holds one file; `held` compares equal to the first run's,
element for element.

**The third run, the look.** exit 0, one line, `symbols=31`, `read=31`.
`state/score-forming/2026-11-15.json` parses to TZ-80's nine keys in their order — `['v', 'k',
'ts', 'day', 'symbols', 'unread', 'stopped', 'scaled', 'entries']` — with `v` 2, `k`
`score-forming`, `day` `2026-11-15`, `symbols` 31, `unread` `[]`. `stopped` and `scaled` are
both empty, so the requirement that each symbol they name has a span in `held` holds over an
empty set by construction and is not a check passing on absent data: the look read all 31
symbols and the day had reached no stop and no target of a position the book holds. The line
reads `alert=no`, so no further file was required in the outbox and none appeared — it still
holds exactly the first run's one. `score.json`, `score-held`, `score-plan` and `score-ledger`
are byte for byte what the second run left:

```
$ diff state-after2.txt state-after3.txt     # md5sum of all ten files, both times
$
```

**The fourth run.** exit 0, the one line `score: forming day=2026-11-15 already looked at,
nothing written`, and no new file anywhere under the scratch directory — the md5sum of all 27
files under `/var/lib/crypto-auto/tz81` before and after the run is identical, by `diff`.

**`book.py`, the three invocations.** As `cryptoauto`, from the scratch tree:

```text
$ python3 /var/lib/crypto-auto/tz81/vps/book.py --live --hold 6,10 BTCUSDT
usage: book.py [-h] [--live] [--archive] [--from START] [--to END]
               [--cache CACHE] [--scale SCALE] [--hold SIDE,BOOK]
               symbols [symbols ...]
book.py: error: --hold SIDE,BOOK reads the archive; the live book held is score.py's
exit=2
```

Exit 2 and a usage error naming `--hold`; stdout empty and no read made — the check sits in
`main()` above the `if a.live:` branch that fetches, and the command returned without the
second's delay the next one shows.

```text
$ python3 /var/lib/crypto-auto/tz81/vps/book.py --live --scale 2 BTCUSDT ETHUSDT
{"asof": "2026-11-14", "atr20": 2580.6649999999986, "close": 64130.5, "entry": 71423.3, "entry_date": "2026-11-13", "entry_due": false, "exit_due": false, "exit_level": 81953.7, "r_open": 1.5983973944509378, "state": "short", "stop": 75985.87, "symbol": "BTCUSDT", "target": 62298.16000000001}
{"asof": "2026-11-14", "atr20": 103.47449999999999, "close": 1768.36, "entry": 2126.26, "entry_date": "2026-11-09", "entry_due": false, "exit_due": false, "exit_level": 2449.95, "r_open": 1.9283902196074802, "scale_date": "2026-11-14", "scale_px": 1740.7540000000004, "state": "short", "stop": 2319.013, "stop_now": 2126.26, "symbol": "ETHUSDT", "target": 1740.7540000000004}
exit=0
```

Two lines, each `short` and each carrying `target`. 1.118s real, against the refused call's
immediate return.

**Afterwards.**

```
$ rm -r /var/lib/crypto-auto/tz81 ; test -e /var/lib/crypto-auto/tz81 ; echo $?
1
$ systemctl list-units --all --no-legend 'run-u*.service'
$
```

No transient service unit of this session remains; the four were started with `--collect` and
are gone. The `run-*` units the broader glob still lists are pre-existing mounts of the host —
`run-credentials-crypto\x2d*.service.mount`, `run-docker-netns-*`, `run-user-0.mount` — none
of them this session's.

### V6. Scope

```
$ git diff --numstat origin/main...HEAD
69	4	vps/book.py
153	68	vps/score.py
271	52	vps/selftest.py
```

Exactly three lines, tab-separated, equal to the TZ's table. No file outside §4 moved.

### V7. Nothing in effect before the merge

A3's four commands, before any work, and again after V5:

| Command | A3 | V7 |
|---|---|---|
| `score.json`'s `v` and `asof` | `1 2026-11-14` | `1 2026-11-14` |
| `test -e score-held; echo $?` | `1` | `1` |
| `ls score-ledger \| wc -l` | `3` | `3` |
| `test -d score-plan && ls score-plan \| wc -l` | absent | absent |

Identical. The three `score-ledger` files carry the same inodes and mtimes as at A3
(`2026-11-13 00:10:10`). The timer did not run during the session: the close fires at 00:10 UTC
and the look at 15:10 UTC, and this session ran from 21:21 to 21:27 UTC.

The live record reads `v` 1, not `2`. The TZ's expected reading allows `1` «where the deployer
has not yet installed TZ-80's merge»; here the cause is adjacent and worth stating exactly.
`/var/lib/crypto-auto/deployed-vps-tree` holds `825713831ce434ae0d8a9e05a62124694d510938`,
which **is** `main`'s current `vps` tree, so TZ-80's merge *is* installed — it was installed at
12:00 UTC on 15.11.2026, after that day's 00:10 close had already run TZ-79's code and written
a `v` 1 record. TZ-80's own baseline close has therefore not yet fired; the first close after
this merge will be TZ-81's baseline either way, since `holds()` refuses a record that is not
`v` 3. `score-forming/` exists on the live host from TZ-80's look of 15:10 UTC today; neither
A3 nor V7 reads it, and V5 did not copy it, so the scratch look wrote its own.

### V8. `bench.yml`

`index.html` and `main.py` are untouched (V6: the diff names three files, all under `vps/`), so
the standing checks of map §6 item 1 do not apply and were not run. The workflows that executed
on the branch are under `## CI Execution`.

### No regression

Every section but AB keeps A2's count and is green (V3's `diff`, one line of difference, and
`failed 0` throughout) — X's 19 among them, the rule's replay unchanged. No file outside §4
moved (V6).

## Test Results

| Item | Result | Evidence |
|---|---|---|
| A1 — the seven added files at §0's lines and MD5 | PASS | all equal; `vps/book.py`, `vps/score.py`, `vps/selftest.py` equal, so A1 does not stop |
| A2 — baseline selftest | PASS | `28 / 779 / 0 / 0`, `AB 117 / 0` — the Architect's figures |
| A3 — live state read | PASS | `1 2026-11-14`; no `score-held`; 3 ledger files; no `score-plan` |
| B1 — patch extracted | PASS | 1048 lines, `24af804041772e14205749784937adcd` |
| B2 — patch applied | PASS | the three files at B2's lines and MD5s, exit 0 |
| V1 — syntax | PASS | exit 0 |
| V2 — bytes and no raw Cyrillic | PASS | three pairs equal; `0` |
| V3 — selftest on the branch | PASS | `28 / 807 / 0 / 0`, `AB 145 / 0`, every other section equal to A2 |
| V4 — eighteen negative controls | PASS | 119 lines, `7e9a8f160d6e4c8f5ce0a1242981df47`; tree clean |
| V5 — four runs, the exchange, the live-state copy | PASS | every required shape met; scratch removed; no unit left |
| V6 — scope | PASS | three numstat lines, exactly as required |
| V7 — nothing in effect before the merge | PASS | A3's readings unchanged |
| V8 — `bench.yml` | PASS | `index.html` and `main.py` untouched; runs named below |

Thirteen items, thirteen comparisons, none skipped and none "not applicable".

## Deviations

None.

One reading is stated rather than deviated from: V5's scratch `cp` of `score-plan/` did not run,
because that directory does not exist on the live host (A3). The TZ's own command guards it with
`if [ -d ... ]`, so this is the branch the TZ wrote for that case, not a departure from it.

## Pre-existing Issues

**None in the files this TZ touches.** Every file the map's `## 0` table lists, and every file
this TZ's gate table adds, measured equal at the required revision — no divergence to report
under this heading.

One standing observation about the host, outside this TZ's scope and not acted on: the live
`score.json` is `v` 1 while TZ-80's merge is installed, because the deployer installed that
merge at 12:00 UTC today and the 00:10 UTC close had already run. The next close writes TZ-81's
baseline record, so nothing needs doing; it is recorded here because V7's reading would
otherwise look like a lag in the deployer rather than a gap of twelve hours in the clock.

## Remaining Risks

- **The first alert after the merge is the one quoted under V5**, and it is wide: twenty-three of
  the plan's twenty-nine open positions are named on the «⏸ Вне лимита:» line, all of them
  shorts. That is the measurement the TZ intends — the owner is told which six positions are the
  book's — but the line is long, and whether its length is the right shape for the first message
  is the Architect's to judge from the text above, not the session's to adjust.
- **The book's six are all shorts**, so the side ceiling of 6 binds before the book ceiling of
  10 ever does: four of his ten slots stand empty while twenty-three entries are refused. The
  behaviour is exactly what §3 specifies, and no change is proposed; it is named because the
  figure a reader expects from «ten in all» is not the figure the first record carries.
- **`score-held/` starts from the current replay, not from the book's whole history.** The
  baseline wrote two files — `ETHUSDT` and `TRXUSDT` — against the plan's four, which is the
  ledger's rule working; the forward reading of §1's finding is `score-held/` against
  `score-plan/`, and it begins from this baseline and accumulates from here.
- **Nothing is in effect until the deployer installs the merge** (contract §7 item 15). V7
  proves the live state untouched; the live `score.py` is still TZ-80's until then.

## Commit

Two commits, each with the message the TZ's §7 fixes, verbatim.

**The implementation commit**, made at B3 and pushed at stage D:

```
TZ-81: vps — the book the owner can hold: the plan's entries taken under his ceilings, six a side and ten in all, the majors first at one open, in the alert, the look and a ledger of their own
```

Hash `096cbf7`, on `claude/tz-81-held-book`. Contents: `vps/book.py`, `vps/score.py`,
`vps/selftest.py` — three files, nothing else.

**This report's commit**, on the `CryptoReports/**` direct-push path:

```
TZ-81: report — the book the owner can hold
```

Contents: `CryptoReports/TZ-81-held-book-report.md`, this file alone.

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/67 — `claude/tz-81-held-book` → `main`,
titled `TZ-81: vps — the book the owner can hold`, its body naming this TZ.

## CI Execution

`bench.yml` — the Bench gate — fires on `push` to `claude/**` and on `pull_request`; its
`paths-ignore` list does not name `vps/**`, so the three changed files clear its filter. Both
runs were read from this session through `gh`:

| Run | Event | Id | Conclusion |
|---|---|---|---|
| Bench gate | `push` | 43763699416 | **success** |
| Bench gate | `pull_request` | 43763736872 | **success** |

`calib.yml` did not run: its `paths` allow-list names `bench/exhaustion_calib.py` and
`.github/workflows/calib.yml`, and this change touches neither. `main.yml` did not run: it fires
on `push` to `main` alone, under a `paths` allow-list of `main.py` and
`.github/workflows/main.yml`. `backtest_bench.yml` is `workflow_dispatch` only and was not
invoked. `journal.yml` is a schedule and was not invoked.

**`main.yml`'s filter re-read before this report's direct push** (contract §8). It is still a
`paths` ALLOW-LIST of exactly the two literal paths `main.py` and
`.github/workflows/main.yml`, with no `paths-ignore` beside it, so `CryptoReports/**` is out by
structure and this report's push cannot start the bot. `index.html` is untouched, so Pages
serves what it served.

## Final Repository State

`claude/tz-81-held-book`, pushed to the remote at `096cbf7` before this report was written, one
commit ahead of `origin/main` at `ee1354e`, with the three files of `## Files Modified` and
nothing else. `git status --porcelain` empty; no generated artifact left behind
(`vps/__pycache__` removed after V1 and after V3, and the units ran with
`PYTHONDONTWRITEBYTECODE=1`). The fingerprints below were taken against this checkout.

**NOT IN EFFECT UNTIL MERGED.**

The previous TZ's branch was merged before this work began: TZ-80 at `eb52dca`, pull request
#66, and `git log --oneline --graph --all` shows no branch on the remote ahead of `main` other
than this one.

## Fingerprints

`SYSTEM-MAP-CRYPTOCALCUL.md` — revision string `**Revision 2026-11-15-a.**`, **2804 lines**,
MD5 `6dc9ce680dbbf791a51d7411d155c80d`. The TZ's §0 reports 2804 and the same MD5; reported,
not enforced, and equal.

**The anchors.** Cut from the map's own anchor table by the table's structure — every row
between its separator line and its end, never by matching anchor names. The table carries
**7 rows** and **7 anchors were compared**; the two numbers are equal, so the cut is not the
defect. Each was matched as a fixed string against the repository copy with
`grep -c -F -- "<anchor>" SYSTEM-MAP-CRYPTOCALCUL.md` and `grep -m1 -o -F -- "<anchor>"`, which
prints the matched text itself:

| Anchor | Hits | Text the match returned |
|---|---:|---|
| revision | 2 | `**Revision 2026-11-15-a.**` |
| direction engine | 2 | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | 2 | `### 3.15 Catalyst registry` |
| exhaustion measure | 2 | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | 2 | `## 11. Analytical engine` |
| squeeze block | 2 | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | 2 | `73. **An Architect-owned document never grows` |

Two hits each: the table's own row and the text the anchor names. Every one of the seven is
quoted by the TZ's header character for character, with the same anchor name, and present in
the map as an exact case-sensitive substring. The revision string the TZ requires is present.
The gate passes.

**The files the map's `## 0` table lists**, at the required revision:

| File | Required | Measured | |
|---|---|---|---|
| `index.html` | 3799 / `4e71da9badca3ccae85b656fdc3773e8` | 3799 / `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 / `0e3ead8c300d2ee6783303c4bf2fb6b5` | 518 / `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | 17 / `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

**The files this TZ's gate table adds:**

| File | Required | Measured (at `ee1354e`, before the patch) | |
|---|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 859 / `4390ee0b8bf1e8d7837afffcd7a5b803` | 859 / `4390ee0b8bf1e8d7837afffcd7a5b803` | equal; line 3 reads `**Version 31.**` |
| `vps/book.py` | 354 / `33c764fa584507fa8a6a121a18f571d8` | 354 / `33c764fa584507fa8a6a121a18f571d8` | equal — A1 does not stop |
| `vps/score.py` | 528 / `91503ec6cecb05d094dc0b8ff47a7889` | 528 / `91503ec6cecb05d094dc0b8ff47a7889` | equal — A1 does not stop |
| `vps/selftest.py` | 3882 / `5963c21b6c869b49d9a151b3aeac0ce7` | 3882 / `5963c21b6c869b49d9a151b3aeac0ce7` | equal — A1 does not stop |
| `vps/paper.py` | 1967 / `f6970999e177fae27bfa78ef9d252b17` | 1967 / `f6970999e177fae27bfa78ef9d252b17` | reported; untouched by the patch |
| `vps/common.py` | 401 / `d307c80cdc9cc0694496d8705dc63cfc` | 401 / `d307c80cdc9cc0694496d8705dc63cfc` | reported; untouched by the patch |
| `vps/writer.py` | 154 / `c07b1f71ef014e18448eb9313e185b73` | 154 / `c07b1f71ef014e18448eb9313e185b73` | reported; untouched by the patch |

**After the patch**, the three files this TZ modifies, on the checkout these fingerprints were
taken against:

| File | Lines | MD5 |
|---|---:|---|
| `vps/book.py` | 419 | `4e283c02783b4f959c49b613b4e518a5` |
| `vps/score.py` | 613 | `eb76418a35e4c9389a80e61b1d449387` |
| `vps/selftest.py` | 4101 | `25136248a1fba37be97af33b1e9a598c` |

**Beside them**, for the record: `ANALYST-INSTRUCTIONS.md` 3777 lines, MD5
`34c9d25be0f50660bb604794a3f67a95`; `CryptoTZ/TZ-81-held-book.md` 1731 lines; the `vps` tree of
`origin/main` at `ee1354e` is `825713831ce434ae0d8a9e05a62124694d510938`, byte-identical to the
tree at `23a003d` the TZ was written against, which is why §10's patch applied with no fuzz.
