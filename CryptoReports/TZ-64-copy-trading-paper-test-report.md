# Implementation Report — TZ-64

## Status

COMPLETED

**A0 — the host, read before the §5 gate and before any other work:** `hostname` → `vultr`;
`systemctl is-active crypto-bot.service crypto-exchange.service` → `active`, `active`;
`test -d /srv/crypto-auto/.git && echo clone` → `clone`; `id -u cryptorun` → `995`. All four are
the TZ's known answers, so the session continued past A0 rather than stopping.

The five lines §11 requires, in its order:

**1. The code.** B1 extracted the patch to `/root/tz64/tz64.patch` with the one command §8 gives:
MD5 `c58f9331d97ecc286777dfc4009c67a5`, 2105 lines — the registered digest and line count, so the
upload did not change the file. `git apply --check` exited 0 and `git apply` exited 0. B2's nine
files all equal their registered digests (table under `## Validation`). V1:
`selftest: sections 23 checks 419 failed 0 empty 0`, exit 0, with `section V: checks 16 failed 0`
and `section W: checks 89 failed 0`. The seven negative controls each produced exactly the
registered partition and exactly the registered failing check names:

| # | Mutation | Result | Failing checks |
|---|---|---|---|
| 1 | `VENUE_SHARE_MIN = 0.80` → `0.79` | exit 1, `sections 23 checks 419 failed 1 empty 0` | W: `share just under 0.8: not copyable` |
| 2 | `hit = (times[k], min(o, stop))` → `(times[k], stop)` | exit 1, `… failed 1 …` | W: `gap: exits at the open 95, gross -62.5` |
| 3 | `for k in range(i + 1, j + 1):` → `range(i + 1, j)` | exit 1, `… failed 1 …` | W: `dip in the exit minute: the stop variant leaves at 96, the source at that minute's close 96.5` |
| 4 | alert freshness guard dropped | exit 1, `… failed 1 …` | W: `two fresh alerts for the pick, none for the null, none late` |
| 5 | `pick_episodes >= EPISODES_MIN` → `… - 1` | exit 1, `… failed 1 …` | W: `29 episodes: unreadable` |
| 6 | `if day > last or (day == last and not state["cut"]):` → `if day > last:` | exit 1, `sections 23 checks 419 failed 3 empty 0` | W: `before the cut, the window's last day is not written`; `day 3: the pick's short, cut at the window end with no price`; `the verdict: two pick episodes and one null episode booked at 1 800 s` |
| 7 | `if git_quiet(tree, "pull", …) != 0:` → `if True:` | exit 1, `sections 23 checks 419 failed 2 empty 0` | V: `writer: one rejection -> rebase -> (True, True)`; `writer: after the rebase remote main carries both commits` |

In every control, all twenty-three sections other than the one named stayed green. Each control
was applied alone, then reverted; after each revert the mutated file's B2 digest was restored and
V1 was green again.

**2. The probe.** C2 exited 0. Seven `paper: probe` lines, none of them `failed (…)`:

```
paper: probe leaderboard rows=47180 pool=4031 bad=0
paper: probe portfolio blocks=12 drawdown=0.11413312997297465 eligible=True r12=True ret52=2.2297398258548187 sharpe=0.5091213820024534 turnover=1.2776198832799686 value_t0=674073.879686
paper: probe exchange perpetuals=525
paper: probe fills fills=10299 first=2026-07-23T14:51:46Z
paper: probe klines_1m rows=1440
paper: probe klines_1d rows=1
paper: probe funding rows=90
paper: probe peak_rss_kib=37880
```

`klines_1m rows=1440` and `klines_1d rows=1` are the registered values. `peak_rss_kib=37880` is
under the unit's `MemoryMax=128M`. systemd-run's own summary beside it:

```
Finished with result: success
Main processes terminated with: code=exited/status=0
Service runtime: 1min 5.331s
CPU time consumed: 527ms
Memory peak: 2.2M
Memory swap peak: 0B
```

The `exchange` step answered here (`perpetuals=525`) where the Architect's session met HTTP 451 —
the difference the TZ predicted and the reason this probe runs on the VPS.

**3. The user and the push.** C1's first run printed, in this order and with no line naming
`cryptorun` or `run clone`:

```
install: group cryptopaper created
install: user cryptopaper created
install: paper clone /var/lib/cryptopaper/crypto-auto created
install: paper clone push URL set
install: paper clone user.name set
install: paper clone user.email set
install: known_hosts for cryptopaper written: 3 github.com lines
install: provision done
```

`<n>` = 3 (reported, not registered). `id -nG cryptopaper` → `cryptopaper cryptoauto`.
`stat -c '%U:%G %a %n'` → `cryptopaper:cryptopaper 750 /var/lib/cryptopaper`,
`cryptopaper:cryptopaper 755 /var/lib/cryptopaper/crypto-auto`,
`cryptopaper:cryptopaper 644 /var/lib/cryptopaper/.ssh/known_hosts`. The second run printed
`install: provision done` alone. C3's dry-run push as `cryptopaper`, with the deploy key loaded as
a systemd credential, printed `Everything up-to-date` and `push_exit=0`; no credential value was
printed, logged or written anywhere.

**4. The gate.** C4's three SHAs and what each listing showed:

| Step | SHA | Listing | Expected |
|---|---|---|---|
| 1 — implementation commit (`vps/**`, `bench.yml`) | `2ed13b24b1a99161a3624c0ef2b61ff90809213d` | one run, id `38956367050`, `status completed`, `conclusion success` | a run for that SHA — the control that must still fire |
| 2 — adds only `analyst/paper/probe.json` (`{}` + newline) | `d6e0c5933ad187da132cfa32f529fd900047c28d` | 180 s later: no run for that SHA | no run |
| 3 — deletes that file | `843ba3ff9faaac66cf458d21d01f94eea88bc171` | 185 s later: no run for that SHA | no run |

The probe file was added and removed inside the branch, so it reaches no tree: the branch tip's
tree `91ba4c3647e9d66045d904e511ea8022083fa4ab` is byte-identical to the implementation commit's.

**5. The tree.** A1.1: `git rev-parse origin/main:vps` →
`96d72e8df795c79ad7d77c9ee73d4bbc284534e7`; `cat /var/lib/crypto-auto/deployed-vps-tree` →
`96d72e8df795c79ad7d77c9ee73d4bbc284534e7`. Both are the registered value, so the deployer's
installed tree is the one this TZ was written against. No finding.

## Inbound Filing

None. `CryptoTZ/TZ-64-copy-trading-paper-test.md` arrived on `origin/main` at `da12712` under its
own canonical filename, with no mangling and no copy in the repository root. Nothing was moved or
renamed.

## Scope Executed

**Branch TZ** (contract §8): the scope names eight files outside `CryptoReports/**`, so the class
is read off the scope, not chosen. Branch `claude/tz-64-paper-test`, pull request opened.

Every stage of the TZ ran: A0, A1.1–A1.4, B1–B3, C1–C4, V1–V7. Nothing in the scope was skipped,
and nothing outside it was touched.

## Files Created

| File | Lines | MD5 |
|---|---:|---|
| `vps/paper.py` | 1229 | `cf160b4dd8cfe5d81a1b5d6e682c230a` |
| `vps/units/crypto-paper.service` | 30 | `082a64f8f3a11ca4d4fab6a3974a97e8` |

B3: `git ls-files -s` reports mode `100644` for both — the mode every program and unit under
`vps/` carries except the two shell scripts.

## Files Modified

| File | Lines | MD5 |
|---|---:|---|
| `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` |
| `vps/writer.py` | 154 | `c07b1f71ef014e18448eb9313e185b73` |
| `vps/selftest.py` | 1683 | `7a876961c3497505da7e08401964bb6b` |
| `vps/install.sh` | 272 | `57f874a6ea816abeaad7f1fd3cec3972` |
| `vps/manifest` | 8 | `36b72e41d6f2e6f49f4f033126aa2a23` |
| `.github/workflows/bench.yml` | 157 | `9d8687f5277c4fb4fa8ac21076a9379c` |
| `analyst/README.md` | 15 | `f99d04e180126a7cd520041338c74def` |

## Files Renamed

None.

## Files Deleted

None. `analyst/paper/probe.json` was created and deleted inside the branch by C4 and reaches no
tree (§4).

## Implementation Summary

The whole implementation is §13's patch, extracted byte for byte by B1's single command and
applied unedited. Nothing was retyped, and no line was written by this session. What the patch
contains, read against §12:

- **`vps/paper.py`** — the paper test. `load_rule` takes the capital and the medium risk from
  `analyst/owner.json` and cuts `INV_FLOOR_SD` and `FEE_TAKER` out of `index.html` through
  `common.cut_number`, so no threshold gets a second definition (inv. 38, 20). Against the
  repository's own files it reads `capital_usdt 10000.0`, `risk_pct 0.5`, `inv_floor_sd 2.0`,
  `fee_taker 0.0005`. `copyability` excludes spot fills, requires a venue share of at least 0.80
  and a median closed episode of at least `max(DELAYS_S)` = 7 200 s (§12.6); `null_order` draws
  the null by SHA-256 of T0's ISO instant and the address (§12.7); `book_delay` books entry and
  exit at the closes of the containing minutes, sizes at `risk_frac · capital / (entry · dist)`,
  and runs the stop variant at the minute's open when it opened beyond the stop (§12.3);
  `decide` computes TOP as the picks' mean against every k-subset of the null, with the readability
  floor and the two deciding delays on the stop variant (§12.4); `publish` copies only records
  `main` does not hold, logs differing bytes and lets `main`'s copy stand (§12.5.1). All seven
  owner-facing strings equal §12.5's texts — the three alerts match literally, and the two notices
  that span a line break in the TZ match once the TZ's own wrapping is normalised, as §2's
  whitespace-normalised standard provides.
- **`vps/units/crypto-paper.service`** — runs as `cryptopaper`, not root, holds the deploy key as
  a systemd credential and nothing else, runs no model, and limits writes to
  `/var/lib/cryptopaper` and the outbox under `MemoryMax=128M` (contract §7 item 6).
- **`vps/install.sh`** — the run's provisioning becomes one function, `provision_own_clone`,
  called twice. C1 proves the `cryptorun` messages are unchanged: the patched `--provision` printed
  no line naming `cryptorun` or `run clone` on a host where TZ-55 had already provisioned it.
- **`vps/common.py` / `vps/writer.py`** — `cut_number`, `git_quiet` and `publish` added;
  `writer.publish` reduced to a call of `common.publish`, so contract §8's push rule has one
  implementation instead of two. Section V exercises it against a real local bare remote with a
  rejecting `pre-receive` hook.
- **`.github/workflows/bench.yml`** — one ignore entry and its three comment lines.
- **`analyst/README.md`** — one table row for `paper/`.

## Validation

| Item | Result |
|---|---|
| **V1** Selftest | PASS — exit 0, `selftest: sections 23 checks 419 failed 0 empty 0`, `section V: checks 16 failed 0`, `section W: checks 89 failed 0`; the seven negative controls as tabulated above |
| **V2** Syntax | PASS — `python3 -m py_compile vps/paper.py vps/common.py vps/writer.py vps/selftest.py` exit 0; `bash -n vps/install.sh` exit 0 |
| **V3** The units | PASS — `systemd-analyze verify vps/units/*` exit 0 with no output from the branch and exit 0 with no output from `origin/main`; the new unit adds no line. This matches TZ-60's C1 reading on this host |
| **V4** Scope | PASS — `git diff --name-only origin/main...HEAD` lists exactly the nine files of §4 |
| **V5** No ignore swallowed a control | PASS — the `bench.yml` diff adds exactly three comment lines and the one line `      - 'analyst/paper/**'`; C4's first push fired (run `38956367050`, `success`) |
| **V6** Nothing touched | PASS — after C, `systemctl show crypto-run.service -p ActiveState -p NRestarts` reads `NRestarts=0`, `ActiveState=inactive`, equal to A1.4; `systemctl list-unit-files 'crypto-*'` lists the same 11 unit files in the same states, `crypto-paper.service` among them absent as expected; `ls /root/tz64` fails with `No such file or directory` |
| **V7** Pushes | PASS — branch pushed, pull request #52 opened after C4; neither C2 nor C3 blocked. `main` receives nothing from this session but this report |

No regression: sections A–U keep their own counts, 314 in all, equal to A1.3's baseline reading on
the branch before any edit. `writer.build_payload`, `writer.run_gate` and section B did not move.

### Fingerprint gate (contract §5)

The map's anchor table was cut by its structure — every row between its separator line and its end
— never by anchor name. **The table carries 7 rows; 7 anchors were compared; the TZ header quotes
all 7 and quotes nothing the table does not carry.** Per anchor, the command and the text the match
returned:

| Anchor | Command | Matched text | Count |
|---|---|---|---:|
| revision | `grep -c -F -- "**Revision 2026-10-16-c.**" SYSTEM-MAP-CRYPTOCALCUL.md` | `**Revision 2026-10-16-c.**` | 2 |
| direction engine | `grep -c -F -- "### 3.12 Direction engine — veto cascade" …` | `### 3.12 Direction engine — veto cascade` | 2 |
| catalyst registry | `grep -c -F -- "### 3.15 Catalyst registry" …` | `### 3.15 Catalyst registry` | 2 |
| exhaustion measure | `grep -c -F -- "### 3.16 List exhaustion — the day-range measure" …` | `### 3.16 List exhaustion — the day-range measure` | 2 |
| analytical engine | `grep -c -F -- "## 11. Analytical engine" …` | `## 11. Analytical engine` | 2 |
| squeeze block | `grep -c -F -- "### 3.17 «РИСК ВЫНОСА» — the day's own risk" …` | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | 2 |
| newest invariant | `grep -c -F -- "72. **A write that fails leaves this run's product or nothing" …` | `72. **A write that fails leaves this run's product or nothing` | 2 |

Each anchor matches twice: once in the map's own anchor table, once at the location it names.

### Stage A readings

| Reading | Known answer | Measured | Verdict |
|---|---|---|---|
| A0 `hostname` | `vultr` | `vultr` | equal |
| A0 `systemctl is-active crypto-bot.service crypto-exchange.service` | `active` twice | `active`, `active` | equal |
| A0 `test -d /srv/crypto-auto/.git` | `clone` | `clone` | equal |
| A0 `id -u cryptorun` | `995` | `995` | equal |
| A1.1 `git rev-parse origin/main:vps` | `96d72e8d…34e7` | `96d72e8df795c79ad7d77c9ee73d4bbc284534e7` | equal |
| A1.1 `/var/lib/crypto-auto/deployed-vps-tree` | `96d72e8d…34e7` | `96d72e8df795c79ad7d77c9ee73d4bbc284534e7` | equal |
| A1.2 `id cryptopaper` | `no such user` | `id: ‘cryptopaper’: no such user` | equal |
| A1.2 `test -e /var/lib/cryptopaper` | no `exists` | absent | equal |
| A1.3 `python3 vps/selftest.py` | exit 0, `sections 21 checks 314 failed 0 empty 0` | exit 0, `selftest: sections 21 checks 314 failed 0 empty 0` | equal |

A1.4 (not registered), read before C and again as V6, identical both times: `NRestarts=0`,
`ActiveState=inactive`; 11 `crypto-*` unit files — `crypto-run.path`, `crypto-stop.path`,
`crypto-announce.service`, `crypto-bot.service`, `crypto-exchange.service`, `crypto-cleanup.timer`
and `crypto-deploy.timer` enabled; `crypto-cleanup.service`, `crypto-deploy.service`,
`crypto-run.service` and `crypto-stop.service` static.

## Test Results

`python3 vps/selftest.py` on the branch, after the patch:

```
section A: checks 32 failed 0      section M: checks 19 failed 0
section B: checks 12 failed 0      section N: checks 10 failed 0
section C: checks  4 failed 0      section O: checks 27 failed 0
section D: checks 13 failed 0      section P: checks 21 failed 0
section E: checks 12 failed 0      section Q: checks  3 failed 0
section F: checks 14 failed 0      section R: checks  9 failed 0
section G: checks  8 failed 0      section S: checks 35 failed 0
section H: checks  2 failed 0      section T: checks 39 failed 0
section I: checks  4 failed 0      section U: checks 18 failed 0
section J: checks 26 failed 0      section V: checks 16 failed 0
section K: checks  2 failed 0      section W: checks 89 failed 0
section L: checks  4 failed 0
selftest: sections 23 checks 419 failed 0 empty 0
```

Exit 0. 314 + 16 + 89 = 419, so the new sections account for the whole increase and no existing
section moved.

## Deviations

None.

## Pre-existing Issues

**No file of the map's `## 0` table, and no file of the TZ's added-files table, differs from its
stated fingerprint.** All thirteen were measured on `origin/main` at `da12712` before any edit and
all thirteen are equal; the map itself is equal too. Nothing is reported under this heading for a
fingerprint reason.

**The TZ carries no `## Commit Message` section.** Contract §8 requires the implementation commit
to carry "the string given in the TZ's `## Commit Message`, verbatim", and TZ-64 has no such
section — its headings run §0 through §13 with none of that name. The commit message used is
recorded under `## Commit` below, in the form the two preceding TZs' commits used. This is reported
rather than treated as a block: no reading of the TZ produces two different implementations, so
§12's ambiguity rule is not engaged.

## Remaining Risks

- **The merge starts a three-hour selection that this report does not cover** (contract §8,
  inv. 54). After the merge the deployer installs the tree and `crypto-paper.service` starts,
  selects once, commits `analyst/paper/selection.json`, tells the owner, and follows for 91 days.
  None of that is this session's to measure and none of it is asserted here.
- **`crypto-paper.service` has never run as a persistent unit.** C2 exercised every interface the
  program reads and section W exercises the offline flow from fills to the verdict, but the service
  path itself — the loop, the restart-and-resume from the work file, the real push of a record — is
  first exercised by the deployer after the merge. C3 proved the push leg's authentication alone.
- **`SYSTEM-MAP-CRYPTOCALCUL.md` §11 goes stale at the merge**, as §5 of the TZ states: its path
  table and its sentence «`bench.yml` ignores FOUR paths in this tree» no longer describe the file
  once a fifth entry lands (inv. 50). The Architect's revision after the audit repairs both. This
  session changed nothing in the map.
- **The probe's own counts drifted from the Architect's reading of the same day**, as live counts
  do: `leaderboard rows=47180 pool=4031` here against `rows=47192 pool=4030` there. Both are
  reported, neither is registered, and the figures the rule depends on — the probe account's
  `drawdown=0.114…` and `blocks=12`, and `fills=10299` — reproduced exactly.

## Commit

Three commits on `claude/tz-64-paper-test`, all pushed before this report was written:

1. `2ed13b24b1a99161a3624c0ef2b61ff90809213d` —
   `TZ-64: vps — the copy-trading paper test: selection, following, booking on Binance prices, the verdict at week 13`
   — the nine files of §4, the whole implementation.
2. `d6e0c5933ad187da132cfa32f529fd900047c28d` — `TZ-64 C4: probe file on the ignored path — added`
   — `analyst/paper/probe.json`, one line, for C4 step 2.
3. `843ba3ff9faaac66cf458d21d01f94eea88bc171` — `TZ-64 C4: probe file on the ignored path — removed`
   — for C4 step 3; restores the implementation commit's tree exactly.

This report's own commit carries the message
`TZ-64: report — the paper test's code, its probe on the VPS, and the gate's new exclusion` and no
hash, no conclusion and no push result: it has not happened when this section is written (inv. 54).

## Pull Request

https://github.com/seahomebatumi-ai/crypto-auto/pull/52

## CI Execution

**On GitHub's runners**, workflow `bench.yml`, branch `claude/tz-64-paper-test`, event `push`: one
run, id `38956367050`, head SHA `2ed13b24b1a99161a3624c0ef2b61ff90809213d`, status `completed`,
conclusion `success`. Read with
`gh run list -R seahomebatumi-ai/crypto-auto -w bench.yml -b claude/tz-64-paper-test -e push --json headSha,status,conclusion`.

No run exists for `d6e0c59` or for `843ba3f`, each listing taken more than 180 s after its push.
That absence is C4's subject and its proof, not a gap: both commits touch only `analyst/paper/**`,
which this branch's `bench.yml` ignores.

The selftest, the seven negative controls, `py_compile`, `bash -n` and `systemd-analyze verify` ran
locally on the VPS, not on a runner. C1, C2 and C3 are VPS measurements by nature and have no
runner equivalent.

`.github/workflows/main.yml` was read before this report's push to `main` and its `push` trigger is
still a `paths` ALLOW-LIST of exactly two literal entries — `main.py` and
`.github/workflows/main.yml` — so neither `CryptoReports/**` nor `analyst/**` can start the bot
(contract §8). Pages serves `index.html`, which neither tree reaches.

## Final Repository State

Branch `claude/tz-64-paper-test`, tip `843ba3ff9faaac66cf458d21d01f94eea88bc171`, pushed to
`origin` before this report was written. Its tree,
`91ba4c3647e9d66045d904e511ea8022083fa4ab`, is byte-identical to the implementation commit's and
differs from `origin/main` in exactly the nine files of §4. The working tree is clean; no scratch
file, no `__pycache__` and no generated artifact remains.

On the VPS, outside the repository: the user, group, home, clone and `known_hosts` of
`cryptopaper` exist, created by C1 and authorised by §4. `/root/tz64` has been removed. Both
transient units were collected. No persistent unit was enabled, started, stopped, restarted or
disabled, no run was requested, and nothing under `/etc/crypto-auto/`, `/etc/systemd/`,
`/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or `/var/spool/crypto-auto` was
written.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

`SYSTEM-MAP-CRYPTOCALCUL.md`: **2779 lines**, MD5 `4c3c60f0c16ac6d7bd8016c0cb370938`, revision
string `**Revision 2026-10-16-c.**` — equal to the TZ's reported value. Reported, not enforced.

The map's `## 0` file table, measured on `origin/main` at `da12712` before any edit:

| File | Lines | MD5 | Required | Verdict |
|---|---:|---|---|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` | `4e71da9badca3ccae85b656fdc3773e8` | equal |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` | `0e3ead8c300d2ee6783303c4bf2fb6b5` | equal |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` | `f9b2dd4a3594134b2b7b603de19075c3` | equal |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | `3b8730b254467c9df4c0a845a0f3cfb3` | equal |

The files the TZ's gate adds, measured in the same reading — the pre-patch bytes §13's patch is
written against:

| File | Lines | MD5 | Required | Verdict |
|---|---:|---|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | `25fac2ff37d2cb12f4bf0e35ce9c9b06`, version line `**Version 30.**` | equal; the version line reads `**Version 30.**`, so item 6 already gives the deploy key to this TZ's unit |
| `ANALYST-INSTRUCTIONS.md` | 4381 | `d665a12f789c9c0a2bb3d090265c22bf` | `d665a12f789c9c0a2bb3d090265c22bf` | equal; this TZ read none of it |
| `vps/common.py` | 364 | `62e3e688cfce21e3e9887e057e461fef` | equal, or BLOCKED | equal |
| `vps/writer.py` | 173 | `b28f3771392e687c9c5585e4f2a72243` | equal, or BLOCKED | equal |
| `vps/selftest.py` | 1186 | `e7fb68d609bd36965f76145528d2575e` | equal, or BLOCKED | equal |
| `vps/install.sh` | 252 | `eef7e6ac5bfda2b17227f6c40a6767df` | equal, or BLOCKED | equal |
| `vps/manifest` | 7 | `4ab0ef7d67fa531eeaad7d0d6e6b7310` | equal, or BLOCKED | equal |
| `.github/workflows/bench.yml` | 153 | `d182e514dcceda5c64410beabc9fe512` | equal, or BLOCKED | equal |
| `analyst/README.md` | 14 | `fd373be9e34a303d87259a0a4c8dedde` | equal, or BLOCKED | equal |

`origin/main:vps` at the gate: `96d72e8df795c79ad7d77c9ee73d4bbc284534e7` — the tree this TZ was
written against.

The nine files after §13's patch are B2's table, reproduced under `## Files Created` and
`## Files Modified`; all nine equal their registered post-patch digests.
