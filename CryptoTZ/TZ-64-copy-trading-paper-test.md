# TZ-64 — On the VPS: the copy-trading paper test — Hyperliquid accounts selected by their twelve-month record, followed in real time, every copied episode booked on Binance prices, the verdict at week 13

**Canonical filename:** `CryptoTZ/TZ-64-copy-trading-paper-test.md`
**Report:** `CryptoReports/TZ-64-copy-trading-paper-test-report.md`
**Host:** the VPS — the server that runs the deployer, the bot and the run unit. **A0 stops BLOCKED on any other
machine, before the gate and before any other work.**
**Class:** branch TZ (contract §8) — it creates two files and modifies seven.
**Branch:** `claude/tz-64-paper-test` · **Model:** Opus
**Previous TZ:** TZ-63, COMPLETED, merged at `7ccc075` (pull request #51).
**Written against:** contract v30, map `2026-10-16-c`, methodology `2026-10-16-b`, and `main` at `b3fccd3` — its
`vps` tree `96d72e8df795c79ad7d77c9ee73d4bbc284534e7` — read by the Architect from the repository on 16.10.2026,
with the contract and the map as delivered for upload beside this TZ. Map §10 row «Hyperliquid's large accounts» is
what this TZ executes; §12 below is the rule that row names.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-10-16-c.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-10-16-c.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `72. **A write that fails leaves this run's product or nothing` |

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Files this TZ's gate adds:

| Added file | Lines | MD5 | Required |
|---|---:|---|---|
| `EXECUTOR-INSTRUCTIONS.md` | 858 | `25fac2ff37d2cb12f4bf0e35ce9c9b06` | its version line reads `**Version 30.**` — a lower version is BLOCKED (inv. 59): item 6 must already give the deploy key to this TZ's unit; lines and MD5 reported |
| `ANALYST-INSTRUCTIONS.md` | 4381 | `d665a12f789c9c0a2bb3d090265c22bf` | reported; this TZ reads none of it and changes nothing it reads |
| `vps/common.py` | 364 | `62e3e688cfce21e3e9887e057e461fef` | equal, or BLOCKED — §13's patch applies to exactly these bytes |
| `vps/writer.py` | 173 | `b28f3771392e687c9c5585e4f2a72243` | equal, or BLOCKED — §13's patch applies to exactly these bytes |
| `vps/selftest.py` | 1186 | `e7fb68d609bd36965f76145528d2575e` | equal, or BLOCKED — §13's patch applies to exactly these bytes |
| `vps/install.sh` | 252 | `eef7e6ac5bfda2b17227f6c40a6767df` | equal, or BLOCKED — §13's patch applies to exactly these bytes |
| `vps/manifest` | 7 | `4ab0ef7d67fa531eeaad7d0d6e6b7310` | equal, or BLOCKED — §13's patch applies to exactly these bytes |
| `.github/workflows/bench.yml` | 153 | `d182e514dcceda5c64410beabc9fe512` | equal, or BLOCKED — §13's patch applies to exactly these bytes |
| `analyst/README.md` | 14 | `fd373be9e34a303d87259a0a4c8dedde` | equal, or BLOCKED — §13's patch applies to exactly these bytes |

The map itself: 2779 lines, MD5 `4c3c60f0c16ac6d7bd8016c0cb370938` — reported, not enforced. The tree `origin/main:vps` is reported
beside them; `96d72e8df795c79ad7d77c9ee73d4bbc284534e7` is the one this TZ was written against. **A file of the
table above that differs from its MD5 is BLOCKED**, because §13's patch is written against exactly those bytes.

---

## 1. Credentials

None arrives and none is written. The new unit loads the deploy key that already exists on the VPS
(`/etc/crypto-auto/credentials/deploy-key`, contract v30 §7 item 6); C3 loads it once, in a transient unit, for a
dry-run push, and nothing prints it. **No model session is opened and the `claude` binary is never executed.**

---

## 2. Contract, map and code text this TZ obeys

Each quote is verbatim, whitespace-normalised, inside the section or file named.

> clones read it — and reaches the unit that uses it — for the deploy key two units, the run unit and, since v30, the paper-test recorder, a program that runs no model under its own user — as a systemd credential (`LoadCredential=`), never as an environment variable of a unit;

— contract §7 item 6. The recorder is `crypto-paper.service`, user `cryptopaper`, holding the deploy key and nothing
else (`vps/units/crypto-paper.service`, §13).

> **The paper-test recorder pushes `analyst/paper/**` on the same path under the same rules** (since v30); it adds only files `main` does not hold, so its rebase cannot conflict with another writer.

— contract §8. `common.publish` is that rule's one implementation, and `writer.publish` now calls it (§13).

> A program in this repository that a VPS unit runs, and whose output that unit commits, has a workflow step's standing on the same terms

— contract §7 item 9. The paper test's records are committed by the unit that computes them, never by a session.

> Code under `vps/` runs on the VPS only from `main`: the deployer fast-forwards its own clone and installs what changed, and nothing else installs anything.

— contract §7 item 15. The merge installs the unit; the selection starts at its first start (§12.1).

> **An exclusion is written for a class of file, but it is applied to a path**, so whenever one is added or widened the question is not «is this data» but «does this path also hold a control». Proof is a real push carrying only that file (inv. 52), never a reading of the pattern.

— map inv. 53. C4 is that push.

> A second implementation of any rule, threshold or formula is banned in any language and any file.

— map inv. 38. `INV_FLOOR_SD` and `FEE_TAKER` are cut from `index.html` (`common.cut_number`), the capital and
the medium risk read from `analyst/owner.json`, Binance's perpetual list taken through `exchange.perpetuals`, and
the push rule moved into `common.publish` rather than written twice.

> a TZ with a stage on the VPS names its host in its header, and its first stage stops BLOCKED on any other machine before any work

— map §10, row «The assistant's build sequence».

---

## 3. What is built and what is read

**The reading behind this TZ** is `claude/copy-trading-reading-2026-10-16.md` in the Project, summarised in the map's
row: on Hyperliquid's keyless API, five non-overlapping quarters, the twelve-month rule's top three earned a
positive mean net return in 5 of 5 quarters against P = 0.0033 for three random eligible accounts, while their
mean was not separable from a random three's; fast or Hyperliquid-only accounts lost the result when copied. Not an
edge yet. **This TZ builds the forward test that decides whether it becomes one**, in code, with no model.

**Built:** (1) `vps/paper.py` — the selection once, then real-time following, the episode records, the booking on
`data.binance.vision`, the funding, the verdict, the owner's alerts and the records pushed to `main` (§12);
(2) `vps/units/crypto-paper.service` and the manifest line that enables it; (3) `vps/install.sh` provisioning the
user `cryptopaper`, its home and its own clone exactly as it provisions `cryptorun`'s — the run's provisioning
becomes one function called twice, its lines unchanged; (4) `common.cut_number`, `common.git_quiet` and
`common.publish`, with `writer.publish` reduced to a call of the last; (5) `.github/workflows/bench.yml` ignoring
`analyst/paper/**`; (6) `analyst/README.md`'s table gaining `paper/`; (7) the selftest's sections V (the push rule on
a local remote, through the writer) and W (the paper test, 89 checks, an offline flow from fills to the verdict
included). **Read on the VPS:** every interface the program uses, by its own `--probe` (C2); the provisioning and
an authenticated dry-run push as `cryptopaper` (C1, C3); and the bench gate on this branch (C4).

**What happens after the merge, and is not this TZ's to report** (contract §8, inv. 54): the deployer installs the
tree; the unit selects once — about three hours, measured in the Architect's workspace on
16.10.2026: 4 028 portfolio reads in about two hours, then 69 copyability checks in about one, the heaviest reading
37 615 fills in 184 s at a peak of 31 MiB; that run was cut twice and resumed from its work file with the same T0 — commits `analyst/paper/selection.json`, tells the owner
«Бумажный тест копирования начат…», and follows. The verdict is written 91 days later, once Binance has published the last
month's funding archive.

---

## 4. Scope

### Files to Create

```
vps/paper.py    vps/units/crypto-paper.service
```

### Files to Modify

```
vps/common.py    vps/writer.py    vps/selftest.py    vps/install.sh    vps/manifest
.github/workflows/bench.yml    analyst/README.md
```

### Files to Delete

None — and C4's probe file is added and removed inside this branch, so it reaches no tree.

### On the VPS, outside the repository — authorised, and nothing else

- `install.sh --provision`, run once from the branch's checkout as root (C1): the user and group `cryptopaper`,
  `/var/lib/cryptopaper` and its own clone and `known_hosts`. It re-applies the owner and mode of every directory it
  already provisions and finds the run's clone complete, so it changes nothing else — C1's output, with no line
  for `cryptorun`, is the proof; the merge's install runs the same provisioning again, which then changes nothing;
- the scratch directory `/root/tz64`, mode `0700`, holding a copy of the branch's `vps/` for C2, gone at the end;
- two transient units, C2's and C3's, each collected when it ends;
- reading, never writing: `/var/lib/crypto-auto/deployed-vps-tree`, `systemctl` state, `gh run list`.

**No persistent unit is started, stopped, restarted, enabled or disabled; no run is requested; nothing under
`/etc/crypto-auto/`, `/etc/systemd/`, `/srv/crypto-auto`, `/var/lib/cryptorun`, `/var/lib/crypto-auto` or
`/var/spool/crypto-auto` is written.**

### On `main`

The report, and nothing else from this session.

---

## 5. What this TZ does not decide and does not build

- **The rule.** §12 is registered here before any forward data exists and moves only by a TZ, never after a
  reading. The Executor implements nothing of it beyond §13's bytes.
- **The analysis.** Nothing of the paper test reaches the market answer, the methodology or `analyst/state.json`;
  `analyst/paper/**` is never an input to a run (the map's row).
- **Orders.** No key with trading rights exists anywhere; a live pilot is a later decision on a passing verdict.
- **The map.** §11's path table and its sentence «`bench.yml` ignores FOUR paths in this tree» become stale at the
  merge (inv. 50); the Architect's revision after the audit repairs both.

---

## 6. Rules — binding in every stage

1. **No model session**, and the `claude` binary is never executed.
2. **No persistent unit changes state** because of this session; C2 and C3 are transient and collected.
3. **The session's network reads are `git`'s, `gh`'s and C2's probe**, nothing else.
4. **The deploy key is never printed** — C3 passes it to `ssh` through `$CREDENTIALS_DIRECTORY` and prints only
   git's own exit code and summary line.
5. **Python 3.12's standard library and bash only.**
6. **Time is UTC everywhere.**
7. **§13's patch is extracted byte for byte, never retyped** — by the one command B1 gives.

---

## 7. Stage A — readings, no writes

- **A0. The host — first, before contract §4a's gate and before anything else:** `hostname`;
  `systemctl is-active crypto-bot.service crypto-exchange.service`; `test -d /srv/crypto-auto/.git && echo clone`;
  `id -u cryptorun`. **Known answers:** `vultr`; `active` twice; `clone`; `995`. **Derived:** TZ-63's report read
  exactly these on this host at 2026-10-09T16:11:32Z. **Any other answer: BLOCKED.** The session writes a report
  carrying A0's lines and its own `hostname`, commits it to `main`, and does nothing else.
- **A1.** Contract §4a steps 1–6 and the §5 gate against §0, including the added-files table; then:
  1. `git rev-parse origin/main:vps` and `cat /var/lib/crypto-auto/deployed-vps-tree`. **Known answer:** both
     `96d72e8df795c79ad7d77c9ee73d4bbc284534e7`. **Derived:** `git log -1 -- vps/` on `main` at `b3fccd3` is TZ-63's
     merged commit, the tree the deployer installed after the merge at `7ccc075`. A different value is a finding,
     never a block.
  2. `id cryptopaper; test -e /var/lib/cryptopaper && echo exists`. **Known answer:** `no such user` and no
     `exists`. **Derived:** no TZ before this one names that user or path. Another answer is a finding, and C1's
     known answer then shrinks to the lines that still create something.
  3. `python3 vps/selftest.py` on the branch before any edit. **Known answer:** exit 0 and
     `selftest: sections 21 checks 314 failed 0 empty 0`. **Derived:** TZ-63 registered exactly this as its V1, and the
     Architect's session read the same line at `b3fccd3`.
  4. `systemctl show crypto-run.service -p ActiveState -p NRestarts` and
     `systemctl list-unit-files 'crypto-*' --no-pager` — the values V6 compares. Not registered.

---

## 8. Stage B — the code, on the branch

- **B1.** From the checkout, after branching from `origin/main`:

  ```
  mkdir -p -m 0700 /root/tz64
  awk '/^<!-- TZ-64 PATCH BEGIN -->$/{f=1;next} /^<!-- TZ-64 PATCH END -->$/{f=0} f' \
      CryptoTZ/TZ-64-copy-trading-paper-test.md | sed '1d;$d' > /root/tz64/tz64.patch
  md5sum /root/tz64/tz64.patch
  git apply --check /root/tz64/tz64.patch && git apply /root/tz64/tz64.patch
  ```

  **Known answer:** the patch's MD5 is `c58f9331d97ecc286777dfc4009c67a5` (2105 lines), and both `git apply` commands exit 0.
  **Derived:** the Architect's session wrote this TZ, extracted the patch with exactly these commands, and applied it
  to a clean clone of `b3fccd3`. A different digest means the upload changed the file: BLOCKED, nothing applied.
- **B2.** `md5sum` and `wc -l` of the nine files. **Known answer:**

  | File | Lines | MD5 |
  |---|---:|---|
  | `vps/paper.py` | 1229 | `cf160b4dd8cfe5d81a1b5d6e682c230a` |
  | `vps/units/crypto-paper.service` | 30 | `082a64f8f3a11ca4d4fab6a3974a97e8` |
  | `vps/common.py` | 401 | `d307c80cdc9cc0694496d8705dc63cfc` |
  | `vps/writer.py` | 154 | `c07b1f71ef014e18448eb9313e185b73` |
  | `vps/selftest.py` | 1683 | `7a876961c3497505da7e08401964bb6b` |
  | `vps/install.sh` | 272 | `57f874a6ea816abeaad7f1fd3cec3972` |
  | `vps/manifest` | 8 | `36b72e41d6f2e6f49f4f033126aa2a23` |
  | `.github/workflows/bench.yml` | 157 | `9d8687f5277c4fb4fa8ac21076a9379c` |
  | `analyst/README.md` | 15 | `f99d04e180126a7cd520041338c74def` |

  **Derived:** the same application in the Architect's session. Any difference: BLOCKED.
- **B3.** `git ls-files -s vps/paper.py vps/units/crypto-paper.service` after `git add`: mode `100644` for both, the
  mode every program and unit under `vps/` carries except the two shell scripts.

---

## 9. Stage C — on the VPS, from the branch

- **C1. Provisioning**, as root from the branch's checkout: `bash vps/install.sh --provision`, then
  `id -nG cryptopaper`, `stat -c '%U:%G %a %n' /var/lib/cryptopaper /var/lib/cryptopaper/crypto-auto
  /var/lib/cryptopaper/.ssh/known_hosts`, and the same command a second time. **Known answer:** the first run prints,
  in this order, `install: group cryptopaper created`, `install: user cryptopaper created`,
  `install: paper clone /var/lib/cryptopaper/crypto-auto created`, `install: paper clone push URL set`,
  `install: paper clone user.name set`, `install: paper clone user.email set`,
  `install: known_hosts for cryptopaper written: <n> github.com lines` and `install: provision done`, and no line
  naming `cryptorun` or `run clone`; `id -nG` prints `cryptopaper cryptoauto`; the three paths are
  `cryptopaper:cryptopaper` `750`, `755` and `644`; the second run prints `install: provision done` alone. `<n>` is
  reported, not registered. **Derived:** the Architect's session ran the current and the patched `--provision` on a
  host with neither user: the patched run printed exactly these lines for `cryptopaper` and, for `cryptorun`, lines
  byte-identical to the current script's, which on this host are absent because TZ-55 provisioned `cryptorun`
  already; the second run printed `install: provision done` alone.
- **C2. The probe** — every interface the program uses, read once: copy the branch's `vps/` into `/root/tz64/vps`,
  then

  ```
  systemd-run --wait --pipe --collect -p MemoryMax=128M -p Nice=5 \
      /usr/bin/python3 /root/tz64/vps/paper.py --probe
  ```

  **Known answer:** exit 0; seven `paper: probe` lines — `leaderboard`, `portfolio`, `exchange`, `fills`,
  `klines_1m`, `klines_1d`, `funding` — none of them `failed (…)`; `klines_1m rows=1440`; `klines_1d rows=1`; and the
  probe's `peak_rss_kib` under the unit's `MemoryMax=128M` — systemd-run's own memory peak beside it where its summary
  prints one.
  **Derived:** the Architect's session ran this probe on 16.10.2026: `leaderboard rows=47192 pool=4030 bad=0`;
  `portfolio … eligible=True r12=True blocks=12 drawdown=0.114…` for the reading's first account — the reading's own
  drawdown and block count; `fills=10299`; `klines_1m rows=1440`, `klines_1d rows=1`, `funding rows=90`; peak RSS
  37 776 KiB; `exchange` failed there with HTTP 451, the refusal every non-VPS host gets from `fapi` and the reason
  this probe runs here. The other counts are reported, not registered. **Any `failed` line: BLOCKED** — the branch
  is pushed, no pull request is opened, and the report names the line first: a lane that cannot read its source is
  never installed.
- **C3. The push, as `cryptopaper`, dry:**

  ```
  systemd-run --wait --pipe --collect -p User=cryptopaper -p Group=cryptopaper \
      -p LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key \
      -p Environment=HOME=/var/lib/cryptopaper \
      /bin/sh -c 'GIT_SSH_COMMAND="ssh -i $CREDENTIALS_DIRECTORY/deploy-key -o IdentitiesOnly=yes -o UserKnownHostsFile=/var/lib/cryptopaper/.ssh/known_hosts" git -C /var/lib/cryptopaper/crypto-auto push --dry-run origin HEAD:main; echo "push_exit=$?"'
  ```

  **Known answer:** `push_exit=0` beside git's `Everything up-to-date`. **Derived:** the run unit pushes as
  `cryptorun` with this credential and this `GIT_SSH_COMMAND` (`vps/units/crypto-run.service`), and TZ-53 read a
  dry-run push authenticated over the deploy key from a transient unit; C1 gives `cryptopaper` the same clone shape.
  **Any other answer: BLOCKED**, as in C2.
- **C4. The gate's new exclusion, on the runner** (inv. 52, 53), before any pull request exists — a pull request's
  own trigger has no paths filter and would fire on every one of these pushes:
  1. push the implementation commit; then `gh run list -R seahomebatumi-ai/crypto-auto -w bench.yml
     -b claude/tz-64-paper-test -e push --json headSha,status,conclusion`. **Known answer:** a run for that commit's
     SHA. **Derived:** the commit changes `vps/**` and `.github/workflows/bench.yml`, which no entry ignores — this is
     the control that must still fire;
  2. a commit adding only `analyst/paper/probe.json` with the content `{}` and a newline, pushed; 180 s later the
     same listing. **Known answer:** no run for that SHA. **Derived:** the commit's tree carries this patch's
     `bench.yml`, whose `'analyst/paper/**'` names the file;
  3. a commit deleting that file, pushed; 180 s later the listing again. **Known answer:** no run for that SHA.
     **Derived:** as 2.

  The report records each SHA and each listing. A run on 2 or 3 is a finding the audit reads, never a block; a read
  `gh` refuses is reported as a gap and the audit reads the runs itself (contract §9).

---

## 10. Validation

- **V1. Selftest.** `python3 vps/selftest.py` on the branch: exit 0,
  `selftest: sections 23 checks 419 failed 0 empty 0`, `section V: checks 16 failed 0` and
  `section W: checks 89 failed 0`. **Derived:** A1.3's 314 checks plus V's 16 and W's 89, read by the Architect's
  session on §13's files. **Negative controls** (inv. 68), each applied alone, then reverted, B2's digests restored
  and V1 green again — in each, every other check of all twenty-three sections stays green:
  1. in `vps/paper.py`, the line `VENUE_SHARE_MIN = 0.80` → `VENUE_SHARE_MIN = 0.79`: exit non-zero, `selftest: sections 23 checks 419 failed 1 empty 0`, and **exactly 1** check of section W fails — `share just under 0.8: not copyable`;
  2. in `vps/paper.py`, the line `            hit = (times[k], min(o, stop))` → `            hit = (times[k], stop)`: exit non-zero, `selftest: sections 23 checks 419 failed 1 empty 0`, and **exactly 1** check of section W fails — `gap: exits at the open 95, gross -62.5`;
  3. in `vps/paper.py`, the line `    for k in range(i + 1, j + 1):` → `    for k in range(i + 1, j):`: exit non-zero, `selftest: sections 23 checks 419 failed 1 empty 0`, and **exactly 1** check of section W fails — `dip in the exit minute: the stop variant leaves at 96, the source at that minute's close 96.5`;
  4. in `vps/paper.py`, the line `            if acct["role"] == "pick" and now - t <= ALERT_MAX_AGE_S * 1000 and now < window_end:` → `            if acct["role"] == "pick" and now < window_end:`: exit non-zero, `selftest: sections 23 checks 419 failed 1 empty 0`, and **exactly 1** check of section W fails — `two fresh alerts for the pick, none for the null, none late`;
  5. in `vps/paper.py`, the line `    readable = k >= 1 and len(null) >= NULL_MIN and pick_episodes >= EPISODES_MIN` → `    readable = k >= 1 and len(null) >= NULL_MIN and pick_episodes >= EPISODES_MIN - 1`: exit non-zero, `selftest: sections 23 checks 419 failed 1 empty 0`, and **exactly 1** check of section W fails — `29 episodes: unreadable`;
  6. in `vps/paper.py`, the line `        if day > last or (day == last and not state["cut"]):` → `        if day > last:`: exit non-zero, `selftest: sections 23 checks 419 failed 3 empty 0`, and **exactly 3** checks of section W fail — `before the cut, the window's last day is not written`, `day 3: the pick's short, cut at the window end with no price`, `the verdict: two pick episodes and one null episode booked at 1 800 s`;
  7. in `vps/common.py`, the line `    if git_quiet(tree, "pull", "-q", "--rebase", "origin", "main") != 0:` → `    if True:`: exit non-zero, `selftest: sections 23 checks 419 failed 2 empty 0`, and **exactly 2** checks of section V fail — `writer: one rejection -> rebase -> (True, True)`, `writer: after the rebase remote main carries both commits`.

  **Derived:** the Architect's session ran all seven on §13's files and read exactly these partitions.
- **V2. Syntax.** `python3 -m py_compile vps/paper.py vps/common.py vps/writer.py vps/selftest.py` and
  `bash -n vps/install.sh`.
- **V3. The units.** `systemd-analyze verify vps/units/*` from the branch and from `origin/main`: the same output
  from both, the new unit adding no line. **Derived:** on a host without `/usr/local/libexec/crypto-auto/deploy.sh`
  the Architect's session read one identical line about that path from both trees (systemd 255); on this host
  TZ-60's C1 read exit 0 with no output, and the installer runs the same command before every install.
- **V4. Scope.** `git diff --name-only origin/main...HEAD` lists exactly the nine files of §4.
- **V5. No ignore swallowed a control.** `git diff origin/main...HEAD -- .github/workflows/bench.yml` adds exactly
  three comment lines and the one line `      - 'analyst/paper/**'`; C4's first push fired.
- **V6. Nothing touched.** After C, `systemctl show crypto-run.service -p ActiveState -p NRestarts` and
  `systemctl list-unit-files 'crypto-*' --no-pager` equal A1.4's, and `ls /root/tz64` fails.
- **V7. Pushes.** The branch pushed and a pull request opened after C4 (or contract §8's fallback), unless C2 or C3
  blocked; `main` receives nothing from this session but its report.

No regression: sections A–U keep their own counts (314 in all); the writer's behaviour is section V's subject,
and `writer.build_payload`, `writer.run_gate` and section B do not move.

---

## 11. The report

Contract §10's template. **The first five lines after `## Status`:**

1. **The code** — B1's patch digest, B2's nine digests, V1's total and the seven controls' partitions.
2. **The probe** — C2's seven lines and its `peak_rss_kib`, verbatim, and systemd-run's summary.
3. **The user and the push** — C1's lines, `<n>`, and C3's `push_exit`.
4. **The gate** — C4's three SHAs and what each listing showed.
5. **The tree** — A1.1's two values.

---

## 12. The rule — registered before any forward data

This section is the paper test. §13's code implements it and nothing else; a difference between the two is a
defect in the code. Each item names what derived it: **the reading** — the pre-registered protocol of 16.10.2026,
whose figures the map's row carries; **the row** — the map's own row; or **[Architect's decision]**, with the
alternative it discards.

**The selection's constants were fixed before the Architect's workspace ran the whole selection on 16.10.2026, and
its outcome is an input to no number here.** What moved after that run is operational only — the weight budget
(12.2.1), the retry rule (12.1.9) and reading fills one page at a time (12.1.6) — each because the run met the
failure it repairs. The run, at T0 = 2026-10-16, for the record: 4 028 in the pool, 147 eligible, 8 passing the
twelve-month rule and **one of them copyable** — `0xa5fd942d4badbab4fe84a9e10f565dd40d5f15ff`, 92.8 % of its notional
on Binance symbols and a median episode of 64.5 h — and 30 null accounts. The reading's first account fell out at a
venue share of 0.785; of the other six, three hold a median episode under a minute, one trades 65 % of its notional
on Binance symbols, and two returned no fill in the window.

### 12.1 Selection — once, at the unit's first start

1. **T0** is 00:00 UTC of the day the selection starts. The selection resumes after a restart from its work file
   with the same T0. *The reading's T0s were quarter boundaries; a forward test has one, its own.*
2. **The pool:** every row of `https://stats-data.hyperliquid.xyz/Mainnet/leaderboard` whose `allTime` `vlm` is
   at least 200 000 000 USD, the address lowercased. The 39 MB document is decoded one row at a time
   (`paper.iter_rows`), so it never exists as one object under the unit's 128 MiB. *The reading: 200 M USD.*
3. **The weekly record:** the grid `g_j = T0 − (52 − j)` weeks, `j = 0 … 52`; `V_j` and `P_j` are
   `perpAllTime`'s `accountValueHistory` and `pnlHistory` at `g_j`, each the last point at or before it;
   `r_j = (P_j − P_{j−1}) / V_{j−1}`, `j = 1 … 52`. *The reading's weekly time-weighted return; the step sampling
   [Architect's decision] — the history's points are irregular, and the reading's first account reproduces its
   drawdown 11.4 % and 12 of 13 blocks under it (C2's derivation).*
4. **Eligible:** `V_j ≥ 10 000` for `j = 0 … 51`, `V_52 ≥ 50 000`, and turnover at most 10 per day, where turnover is
   `perpMonth`'s `vlm` over the mean of `perpMonth`'s `accountValueHistory` values over that history's span in days.
   *The reading's thresholds; the turnover's definition [Architect's decision] — the portfolio answer carries no
   volume per week, and the last month is the speed a copier meets now.*
5. **The twelve-month rule:** of thirteen blocks of four weeks, at least 10 with `Π(1 + r) − 1 > 0`; the maximum
   drawdown of the wealth `Π(1 + r)` at most 0.25; ranked by weekly Sharpe — `mean(r)` over the population standard
   deviation of `r`, an account with a deviation of zero not passing — highest first, ties by address. *The reading.*
6. **Copyable**, measured on the fills `userFillsByTime` returns in `[T0 − 91 days, T0)`, read one page at a time
   — the heaviest account the workspace read returned 37 615, and an account it returns none for is not copyable.
   Spot fills (a coin with `/` or starting `@`) are left out; the **venue share**, notional `px · sz` on coins with
   a Binance symbol over the notional of every fill but spot, is at least **0.80**; and the **median duration of the
   closed episodes** (12.2) on those coins is at least **7 200 s**. A coin's Binance symbol is `<coin>USDT`,
   `1000<rest>USDT` for a Hyperliquid coin `k<Capital…>`, and none for a builder market `dex:coin`; it counts only when Binance lists it as a TRADING
   USDT perpetual at the selection (`exchange.perpetuals`), a list frozen into the record. *The row: copyable
   accounts only. 0.80 [Architect's decision; discarded: any share — a copy of a fifth of an account is another
   strategy]; 7 200 s is the longest delay, so the median episode is still open when the slowest copier enters.*
7. **Picks:** down the ranking, the first three copyable accounts — fewer when the ranking runs out. **The null:**
   the eligible accounts but the picks, in the order of the SHA-256 of T0 written `YYYY-MM-DDTHH:MM:SSZ` followed by
   the address, the first 30 copyable. *The reading's TOP3 and its null of random eligible accounts; the hash order
   [Architect's decision] — reproducible from the record alone; 30 [Architect's decision] — 4 060 triples for three
   picks.*
8. **The record** `analyst/paper/selection.json`: T0, `follow_from` — the selection's last instant — and
   `window_end = follow_from + 91 days`; the rule's inputs, frozen; the counts; the picks, the rejected ranked
   accounts and the null with every measure; the eligible list; the Binance list; the installed tree and
   `paper.py`'s MD5. *The row's 13 weeks.*
9. **A read that fails** is retried every 60 s. After 30 failures in a row, one account is recorded unreadable
   for transport — counted in the record, never treated as an account with no data (inv. 70) — and the selection
   goes on; a step it cannot do without, the leaderboard or Binance's list, ends the process instead, which its
   unit restarts, and the selection resumes from its work file with the same T0. *[Architect's decision: the
   workspace's own run met five 429 answers in a row on one account, and a step retried without end stalls the
   whole selection.]*
10. **The test follows only when it can be read** — at least one pick and at least 10 null accounts (12.4.2).
   Otherwise the record is still written and pushed, the owner is told so (12.5.3), and nothing is followed.

### 12.2 Following and episodes

1. Every pick is read every 30 s and every null account every 600 s, from the last fill time it was read to, each
   fill once by `tid`; within the API's weight budget, held at 600 of its documented 1 200 per minute
   (`paper.Limiter`) — at 900 the Architect's workspace met runs of 429 answers on 16.10.2026. *[Architect's
   decision; discarded: the websocket — ten users per IP, and the standard library has no client.]*
2. **An episode** on one copyable coin opens when a fill takes the position from flat, or flips it, and closes when
   a fill takes it to flat, or flips it. The position before a fill is the fill's own `startPosition`; adds and
   reductions change nothing; a position already open at `follow_from` has no episode until it is flat; an episode
   held while a fill's `startPosition` disagrees with it is **lost** — counted, never booked.
   *[Architect's decision: the copier follows the account's direction, not its sizing.]*
3. Fills at or after `window_end` are never applied. Once every account was read 600 s past `window_end`, every
   episode still open closes at `window_end`, **cut**, with no price.

### 12.3 Booking — per episode, at 5 s, 300 s, 1 800 s and 7 200 s

1. **Prices:** `data.binance.vision` — the daily 1-minute klines of the USD-M perpetual, its daily 1-day klines, and
   its monthly `fundingRate` archive. *The row: Binance prices with funding. The archive, not `fapi` [Architect's
   decision]: anyone can re-read it from anywhere, a runner included (contract §7 item 9). Read 16.10.2026 from the
   bucket listing: a day's klines are published about 08:00 UTC the next day, a month's funding about 08:00 UTC on
   the 1st — so a 404 for a file dated more than 3 days back is an absence, nearer is a wait.*
2. **Entry** at delay `d`: the close of the 1-minute kline of the minute containing `t_open + d` — the last minute
   at or before it when that minute is missing. **Exit:** the close of the minute containing `t_close + d`, or of
   `window_end`'s minute for a cut episode. Not booked at `d` when the entry minute is after the exit minute.
   *The reading's execution rule.*
3. **Size — a fixed risk of the owner's capital:** `σ` is the population standard deviation of the 30 daily simple
   returns of the closes of days `D − 32 … D − 2`, `D` the UTC day of `t_open`; the stop distance is
   `dist = INV_FLOOR_SD · σ`, cut from `index.html`; `qty = (risk_pct_medium / 100) · capital / (entry · dist)`, both
   from `analyst/owner.json` at the selection and frozen. *The row; the stop at the board's own minimum distance and
   the medium risk [Architect's decision; discarded: the account's own leverage, which the reading named as a limit,
   and the strong risk, which no measured edge supports]. Days to D − 2 because all are published when an episode of
   day D opens, so the alert and the book use one σ.*
4. **Two variants:** the **source** variant exits at the exit; the **stop** variant leaves at
   `entry · (1 ∓ dist)` on the first minute after the entry minute, through the exit minute, whose low (long) or high
   (short) touches it — at that price, or at the minute's open when it opened beyond. *The stop variant decides
   [Architect's decision]: the owner trades with a stop; the source variant is the reading's.*
5. **Money:** `gross = side · qty · (exit − entry)`; `fee = FEE_TAKER · qty · (entry + exit)`, cut from
   `index.html`; `funding = side · qty · entry · Σ rate` over the archive's events after the entry minute's end and
   at or before the exit minute's end — the entry's notional, not the mark at each event; `net = gross − fee −
   funding`. *The row: a taker cost of 0.05 % of notional, which `FEE_TAKER` is.*

### 12.4 The verdict — once every day of the window is booked and funded

1. Per account, delay and variant, `R = Σ net / capital`. **TOP** is the picks' mean; **the null** is every subset
   of the null accounts of the picks' size, each by its mean; its median is the reference — computed in the same
   run (inv. 49).
2. **Readable:** at least one pick, at least **10** null accounts, and at least **30** booked pick episodes at
   1 800 s. *[Architect's decision: a mean of fewer episodes, or a reference drawn from fewer than ten
   accounts, decides nothing.]*
3. **PASSED:** readable, and at **1 800 s and at 7 200 s** on the **stop** variant, `TOP > 0` and `TOP` above the
   null's median. *The reading's two criteria — a positive mean and a beaten reference — at the delays a manual
   copier reaches [Architect's decision; discarded: 5 s, which no manual copier reaches, and 300 s, which the owner
   reaches only awake]. A decision about value, not a calibrated band (inv. 49).*
4. Reported beside it: every delay and variant with TOP, the median and the share of subsets at or above TOP; each
   pick's own result; booked counts by role and delay; unbookable episodes; episodes whose funding archive was
   absent; the picks' detection lag at the 50th and 95th percentile.
5. **One window decides little alone**, and this record says so: a pass is the sixth window after the reading's
   five, read by the Architect with them; a limited live pilot follows only a pass (the row).

### 12.5 Records, alerts and notices

1. Under `analyst/paper/` on `main`, each written once and never reopened (inv. 38): `selection.json`;
   `episodes/YYYY-MM-DD.jsonl` — the episodes that closed that day, written once every account was read 600 s past
   its end, the window's last day after the cut, and an episode that closed on a day already written going into the
   next file; `book/YYYY-MM-DD.jsonl` once that day's inputs are published; `funding/YYYY-MM-DD.jsonl` once every
   month they touch is; `verdict.json`. A path `main` already holds is never overwritten: equal bytes are done,
   different bytes are logged and `main`'s copy stands.
2. **Alerts**, to the owner through the outbox, for the picks only, while the window is open, for an open or a
   close seen at most 600 s after its fill — none for the null, none late. *[Architect's decision: the bot drops an
   owner's message older than 600 s by the same reasoning.]* The texts, character for character:

   ```
   📋 Бумажный тест · {hhmm} Тбилиси · счёт #{rank} {addr} открыл {side} {symbol} по {px} · стоп {dist}% → {stop} · объём {notional} USDT при риске {risk}% капитала
   📋 Бумажный тест · {hhmm} Тбилиси · счёт #{rank} {addr} открыл {side} {symbol} по {px} · стоп и объём не рассчитаны: нет дневных свечей Binance
   📋 Бумажный тест · {hhmm} Тбилиси · счёт #{rank} {addr} закрыл {side} {symbol} по {px} · в позиции {held}
   ```

   `{hhmm}` is the fill's Tbilisi time; `{addr}` the address's first six and last four characters; `{side}` LONG or
   SHORT; `{px}` the fill's price as Hyperliquid served it; `{dist}` the stop distance in per cent to one decimal;
   `{stop}` at `{px}`'s decimals; `{notional}` in whole USDT; `{held}` in minutes under an hour, else hours to one
   decimal.
3. **Notices**, once each: at the selection, «Бумажный тест копирования начат: отобрано счетов Hyperliquid — {k},
   окно 13 недель, до {date}. Сообщения с пометкой «Бумажный тест» — проверка метода до решения о пилоте.» or, with
   a selection that cannot be read, «Бумажный тест копирования не начат: отбор Hyperliquid не дал нужного числа
   счетов.»; at the cut, «Бумажный тест копирования: 13 недель прошли, оповещения остановлены. Итог — после публикации данных Binance.»;
   at the verdict, «Бумажный тест копирования: итог записан и ждёт разбора Архитектора.»

---

## 13. The patch

Against `b3fccd3`. B1 extracts the lines between the two markers, drops the fence lines, and applies the rest.

<!-- TZ-64 PATCH BEGIN -->
```diff
diff --git a/.github/workflows/bench.yml b/.github/workflows/bench.yml
index 6700669..66f0e4e 100644
--- a/.github/workflows/bench.yml
+++ b/.github/workflows/bench.yml
@@ -40,6 +40,10 @@ on:
       # его заливка заводила ворота целиком. Литерал, а не маска: две
       # точные строки либо равны, либо нет (инв. 52).
       - 'analyst/owner.json'
+      # Записи бумажного теста копирования (vps/paper.py, ТЗ-64): юнит на VPS
+      # коммитит их в main по нескольку раз в сутки. Это данные, не код: их
+      # контроль — selftest на VPS, а не эти ворота.
+      - 'analyst/paper/**'
       - '**.md'
   pull_request:
 
diff --git a/analyst/README.md b/analyst/README.md
index a7a2ca0..addf8d0 100644
--- a/analyst/README.md
+++ b/analyst/README.md
@@ -8,6 +8,7 @@ The market-analysis engine's tree. Nothing here reaches the live calculator and
 | `live-gate.sh` | the gate that reads it; exit 0 means levels may be published | the Executor |
 | `state.json` | current analytical state, schema v1 | the analyst role, replaced in place |
 | `log/` | one file per analysis run | the analyst role, immutable |
+| `paper/` | the copy-trading paper test's record (TZ-64); never an input to an analysis run | `vps/paper.py` on the VPS, immutable |
 
 The log is never reopened; the state is one copy, replaced every run.
 
diff --git a/vps/common.py b/vps/common.py
index 78928a3..2665fdc 100644
--- a/vps/common.py
+++ b/vps/common.py
@@ -1,5 +1,5 @@
 #!/usr/bin/env python3
-"""Paths and the shared helpers of the VPS assistant (TZ-54 B1, TZ-55 B1, TZ-56 B1, TZ-57 B1, TZ-60 B1), and nothing else.
+"""Paths and the shared helpers of the VPS assistant (TZ-54 B1, TZ-55 B1, TZ-56 B1, TZ-57 B1, TZ-60 B1, TZ-64 B1), and nothing else.
 
 Python 3.12's standard library only. Every Russian string is written as \\uXXXX
 escapes (TZ-54 rule 6, hard floor item 7's rule) and equals TZ-54 §12.1,
@@ -9,6 +9,7 @@ import json
 import math
 import os
 import re
+import subprocess
 import tempfile
 import time
 import urllib.parse
@@ -225,6 +226,42 @@ def read_tokens(path=None):
         return cut_tokens(fh.read())
 
 
+# --- TZ-64: a numeric constant cut from index.html (inv. 20, 21) ------------------
+def cut_number(index_html, name):
+    """The number of the one line `var <name> = <number>;` in index.html. None or several fail."""
+    found = re.findall(r"^var\s+%s\s*=\s*([0-9]+(?:\.[0-9]+)?)\s*;" % re.escape(name), index_html, re.M)
+    if len(found) != 1:
+        raise ValueError("%s: %d definitions" % (name, len(found)))
+    return float(found[0])
+
+
+# --- TZ-64: a clone's commit and push to main, the one implementation (contract section 8) --
+def git_quiet(tree, *args):
+    """One git command in tree, output discarded; its exit code."""
+    return subprocess.run(["git", "-C", tree] + list(args),
+                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
+
+
+def publish(tree, paths, message):
+    """Commit paths in the clone tree and push HEAD to main: one rejection -> pull --rebase and push
+    again; a rebase that fails is aborted and this commit dropped; a second rejection drops it too.
+    Never a branch, never a force. Returns (committed, pushed); a failed add or commit returns
+    (False, False) and leaves the paths to the caller."""
+    base = subprocess.run(["git", "-C", tree, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
+    if git_quiet(tree, "add", "--", *paths) != 0 or git_quiet(tree, "commit", "-q", "-m", message, "--", *paths) != 0:
+        return False, False
+    if git_quiet(tree, "push", "-q", "origin", "HEAD:main") == 0:
+        return True, True
+    if git_quiet(tree, "pull", "-q", "--rebase", "origin", "main") != 0:
+        git_quiet(tree, "rebase", "--abort")
+        git_quiet(tree, "reset", "-q", "--hard", base)
+        return True, False
+    if git_quiet(tree, "push", "-q", "origin", "HEAD:main") == 0:
+        return True, True
+    git_quiet(tree, "reset", "-q", "--hard", "HEAD~1")
+    return True, False
+
+
 # --- TZ-54 §12.8, the one implementation ------------------------------------
 def derive_limits(footprint_bytes, duration_s):
     """(memory_max_bytes, runtime_max_s) from a footprint and a duration."""
diff --git a/vps/install.sh b/vps/install.sh
index 17c44d9..47d60d9 100755
--- a/vps/install.sh
+++ b/vps/install.sh
@@ -1,17 +1,18 @@
 #!/usr/bin/env bash
 #
-# vps/install.sh — installs the VPS assistant from the checkout it sits in (TZ-54 B9, TZ-55 B5).
+# vps/install.sh — installs the VPS assistant from the checkout it sits in (TZ-54 B9, TZ-55 B5, TZ-64 B3).
 #
 #   install.sh              called by the deployer from /srv/crypto-auto: selftest, provision,
 #                           verify, install units, enable the manifest, disable the rest
 #   install.sh --bootstrap  once, from the TZ-54 branch: users, directories, clone,
 #                           deploy.sh, crypto-deploy.service and .timer, the timer enabled
-#   install.sh --provision  users, groups, directories, the run's own clone and its
-#                           known_hosts — nothing installed, enabled, copied or removed
+#   install.sh --provision  users, groups, directories, the run's and the paper test's own
+#                           clones and known_hosts — nothing installed, enabled, copied or removed
 #   install.sh --dry-run    prints what the default mode would do and changes nothing
 #
 # The run has its own unprivileged user, cryptorun, and its own clone under its home
-# (contract §7 item 6, since v25); nothing creates /srv/crypto-auto-run any more.
+# (contract §7 item 6, since v25); nothing creates /srv/crypto-auto-run any more. The paper
+# test has its own, cryptopaper, the same way (contract §7 item 6, since v30).
 #
 # `disable --now` applies to units that carry an [Install] section: a unit without one
 # (crypto-run.service, crypto-stop.service, crypto-cleanup.service, crypto-deploy.service) is
@@ -32,6 +33,7 @@ RUNS_ENABLED=/var/lib/crypto-auto/runs-enabled
 RUN_HOME=/var/lib/cryptorun
 RUN_CLONE="$RUN_HOME/crypto-auto"
 RUN_FETCH=https://github.com/seahomebatumi-ai/crypto-auto.git
+PAPER_HOME=/var/lib/cryptopaper
 ROOT_KNOWN_HOSTS=/root/.ssh/known_hosts
 
 mode="${1-}"
@@ -66,6 +68,15 @@ provision_user() {
         *" cryptoauto "*) ;;
         *) usermod -a -G cryptoauto cryptorun; say "user cryptorun added to group cryptoauto" ;;
     esac
+    if ! getent group cryptopaper >/dev/null; then
+        groupadd --system cryptopaper
+        say "group cryptopaper created"
+    fi
+    if ! id -u cryptopaper >/dev/null 2>&1; then
+        useradd --system --gid cryptopaper --groups cryptoauto --no-create-home --home-dir "$PAPER_HOME" \
+            --shell /usr/sbin/nologin cryptopaper
+        say "user cryptopaper created"
+    fi
 }
 
 provision_dirs() {
@@ -78,6 +89,7 @@ provision_dirs() {
     dir_as 0750 cryptoauto cryptoauto /var/lib/crypto-auto
     dir_as 0755 root root "$LIBEXEC"
     dir_as 0750 cryptorun cryptorun "$RUN_HOME"
+    dir_as 0750 cryptopaper cryptopaper "$PAPER_HOME"
 }
 
 provision_clone() {
@@ -99,44 +111,46 @@ provision_clone() {
     done
 }
 
-# Root works on the clone cryptorun owns, so git's ownership check is told this one path.
-run_git() { git -c safe.directory="$RUN_CLONE" -C "$RUN_CLONE" "$@"; }
+# Root works on a clone another user owns, so git's ownership check is told that one path.
+own_git() { local clone="$1"; shift; git -c safe.directory="$clone" -C "$clone" "$@"; }
 
-provision_run_clone() {
-    if [ ! -d "$RUN_CLONE/.git" ]; then
-        git clone -q "$RUN_FETCH" "$RUN_CLONE"
-        say "run clone $RUN_CLONE created"
+# A user's own clone under its home: fetched over HTTPS, pushed over SSH with the deploy key its
+# unit loads, its committer identity taken from the clone that already commits on this host
+# (values never printed), and GitHub's host keys from root's own github.com lines (TZ-54 D-8,
+# TZ-55 B5; generalised by TZ-64 B3 for cryptopaper, messages unchanged for cryptorun).
+provision_own_clone() {   # <user> <home> <label>
+    local user="$1" home="$2" label="$3" clone="$2/crypto-auto"
+    if [ ! -d "$clone/.git" ]; then
+        git clone -q "$RUN_FETCH" "$clone"
+        say "$label clone $clone created"
     fi
-    if ! run_git config --local --get remote.origin.pushurl >/dev/null; then
-        run_git config --local remote.origin.pushurl "$REMOTE"
-        say "run clone push URL set"
+    if ! own_git "$clone" config --local --get remote.origin.pushurl >/dev/null; then
+        own_git "$clone" config --local remote.origin.pushurl "$REMOTE"
+        say "$label clone push URL set"
     fi
-    # The writer and the session commit from this clone; its committer identity is taken
-    # from the clone that already commits on this host, values never printed (TZ-54 D-8).
     local key value
     for key in user.name user.email; do
-        if ! run_git config --local --get "$key" >/dev/null; then
+        if ! own_git "$clone" config --local --get "$key" >/dev/null; then
             value="$(git -C "$IDENTITY_SOURCE" config --get "$key" || true)"
             if [ -n "$value" ]; then
-                run_git config --local "$key" "$value"
-                say "run clone $key set"
+                own_git "$clone" config --local "$key" "$value"
+                say "$label clone $key set"
             fi
         fi
     done
-    chown -R cryptorun:cryptorun "$RUN_CLONE"
-    # GitHub's host keys for cryptorun's pushes: root's own github.com lines.
-    if [ ! -e "$RUN_HOME/.ssh/known_hosts" ]; then
+    chown -R "$user:$user" "$clone"
+    if [ ! -e "$home/.ssh/known_hosts" ]; then
         local lines tmp
         lines="$(ssh-keygen -F github.com -f "$ROOT_KNOWN_HOSTS" | grep -v '^#' || true)"
         if [ -z "$lines" ]; then
-            say "no github.com line in $ROOT_KNOWN_HOSTS; known_hosts for cryptorun not written"
+            say "no github.com line in $ROOT_KNOWN_HOSTS; known_hosts for $user not written"
             return 1
         fi
-        dir_as 0700 cryptorun cryptorun "$RUN_HOME/.ssh"
-        tmp="$(mktemp "$RUN_HOME/.ssh/.known_hosts.XXXXXX")"
-        if printf '%s\n' "$lines" > "$tmp" && chown cryptorun:cryptorun "$tmp" && chmod 0644 "$tmp" \
-            && mv -f -- "$tmp" "$RUN_HOME/.ssh/known_hosts"; then
-            say "known_hosts for cryptorun written: $(printf '%s\n' "$lines" | wc -l) github.com lines"
+        dir_as 0700 "$user" "$user" "$home/.ssh"
+        tmp="$(mktemp "$home/.ssh/.known_hosts.XXXXXX")"
+        if printf '%s\n' "$lines" > "$tmp" && chown "$user:$user" "$tmp" && chmod 0644 "$tmp" \
+            && mv -f -- "$tmp" "$home/.ssh/known_hosts"; then
+            say "known_hosts for $user written: $(printf '%s\n' "$lines" | wc -l) github.com lines"
         else
             rm -f -- "$tmp"
             return 1
@@ -144,6 +158,10 @@ provision_run_clone() {
     fi
 }
 
+provision_run_clone() { provision_own_clone cryptorun "$RUN_HOME" run; }
+
+provision_paper_clone() { provision_own_clone cryptopaper "$PAPER_HOME" paper; }
+
 copy_deploy() {
     install -m 0755 -o root -g root "$HERE/deploy.sh" "$LIBEXEC/.deploy.sh.new"
     mv -f -- "$LIBEXEC/.deploy.sh.new" "$LIBEXEC/deploy.sh"
@@ -157,6 +175,7 @@ if [ "$mode" = "--provision" ]; then
     provision_user
     provision_dirs
     provision_run_clone
+    provision_paper_clone
     say "provision done"
     exit 0
 fi
@@ -209,6 +228,7 @@ fi
 provision_user
 provision_dirs
 provision_run_clone
+provision_paper_clone
 if ! systemd-analyze verify "$UNITS"/*; then
     say "systemd-analyze verify red, nothing installed"
     exit 1
diff --git a/vps/manifest b/vps/manifest
index 1b49261..4deea35 100644
--- a/vps/manifest
+++ b/vps/manifest
@@ -5,3 +5,4 @@ crypto-bot.service
 crypto-run.path
 crypto-announce.service
 crypto-stop.path
+crypto-paper.service
diff --git a/vps/paper.py b/vps/paper.py
new file mode 100644
index 0000000..75a400e
--- /dev/null
+++ b/vps/paper.py
@@ -0,0 +1,1229 @@
+#!/usr/bin/env python3
+"""The copy-trading paper test (TZ-64; map section 10, row \u00abHyperliquid's large accounts\u00bb):
+Hyperliquid accounts selected once by their twelve-month record, followed in real time,
+every copied episode booked on Binance USD-M prices at four delays, and the verdict
+read at week 13 against random eligible accounts copied the same way.
+
+    paper.py [--state-dir <dir>] [--tree <dir>]      the service
+    paper.py --probe                                  one read of every interface; counts only
+
+Python 3.12's standard library only. Holds no credential but the deploy key its unit
+passes to git, and prints no value. Alerts the owner through the outbox for the
+selected accounts only, and requests no run. Its records are written under
+analyst/paper/ of its own clone and pushed to main (contract v30 section 8); a record
+is written once and never reopened.
+"""
+import argparse
+import bisect
+import codecs
+import hashlib
+import http.client
+import io
+import json
+import math
+import os
+import resource
+import shutil
+import statistics
+import sys
+import time
+import urllib.error
+import urllib.request
+import zipfile
+from datetime import datetime, timedelta, timezone
+from decimal import Decimal
+from itertools import combinations
+
+sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
+import announce  # noqa: E402
+import common  # noqa: E402
+import exchange  # noqa: E402
+
+INFO_URL = "https://api.hyperliquid.xyz/info"
+LEADERBOARD_URL = "https://stats-data.hyperliquid.xyz/Mainnet/leaderboard"
+VISION = "https://data.binance.vision/data/futures/um"
+
+# --- The rule, registered by TZ-64 before any data: moved only by a TZ, never after a reading.
+POOL_VOLUME_MIN = 200e6       # all-time volume on the leaderboard, USD
+LOOKBACK_WEEKS = 52
+BLOCK_WEEKS = 4               # thirteen blocks of four weeks
+BLOCKS_MIN = 10               # positive blocks of thirteen
+DRAWDOWN_MAX = 0.25
+VALUE_MIN_WEEK = 10000.0      # account value at every lookback week's start, USD
+VALUE_MIN_T0 = 50000.0        # account value at T0, USD
+TURNOVER_MAX = 10.0           # perpetual volume per day over the mean account value, last month
+TOP_K = 3
+NULL_M = 30
+WINDOW_DAYS = 91              # thirteen weeks: the follow window, and the copyability window before T0
+VENUE_SHARE_MIN = 0.80
+DELAYS_S = (5, 300, 1800, 7200)
+DECIDING_S = (1800, 7200)
+SIGMA_DAYS = 30
+EPISODES_MIN = 30
+NULL_MIN = 10
+ALERT_MAX_AGE_S = 600
+PROBE_ACCOUNT = "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1"   # the reading's first account
+
+# --- Operation.
+WEIGHT_PER_MIN = 600          # half the info API's documented 1 200 per IP per minute: at 900 the
+                              # Architect's workspace met runs of 429 answers on 16.10.2026
+INFO_WEIGHT = 20              # documented weight of portfolio and userFillsByTime
+FILLS_PAGE = 2000             # documented maximum fills per userFillsByTime answer
+FILL_KEYS = ("coin", "px", "sz", "side", "time", "startPosition", "tid")   # all a fill is read for
+PICK_POLL_S = 30
+NULL_POLL_S = 600
+DAY_SETTLE_S = 600            # a day is written once every account was polled this long after it ended
+ABSENT_AFTER_DAYS = 3         # a 404 for a file dated further back is an absence, nearer is unpublished
+WORK_EVERY_S = 3600           # booking, funding and the verdict are attempted hourly
+PUBLISH_EVERY_S = 300
+TRANSPORT_MAX = 30            # consecutive transport failures on one selection step
+TRANSPORT_WAIT_S = 60
+LOOP_S = 5
+DAY_MS = 86400000
+WEEK_MS = 7 * DAY_MS
+STATE_DIR = "/var/lib/cryptopaper"
+TREE = STATE_DIR + "/crypto-auto"
+RECORD_DIR = "analyst/paper"
+DEPLOYED_TREE = os.path.join(common.STATE_DIR, "deployed-vps-tree")
+REPO = os.path.dirname(common.VPS_DIR)
+
+# --- TZ-64 section 12.1, character for character.
+P_OPEN = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
+          "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
+          "\u043e\u0442\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0441\u0442\u043e\u043f "
+          "{dist}% \u2192 {stop} \u00b7 \u043e\u0431\u044a\u0451\u043c {notional} USDT \u043f\u0440\u0438 "
+          "\u0440\u0438\u0441\u043a\u0435 {risk}% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430")
+P_OPEN_BARE = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
+               "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
+               "\u043e\u0442\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0441\u0442\u043e\u043f "
+               "\u0438 \u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: "
+               "\u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance")
+P_CLOSE = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 {hhmm} "
+           "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #{rank} {addr} "
+           "\u0437\u0430\u043a\u0440\u044b\u043b {side} {symbol} \u043f\u043e {px} \u00b7 \u0432 "
+           "\u043f\u043e\u0437\u0438\u0446\u0438\u0438 {held}")
+N_START = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440"
+           "\u043e\u0432\u0430\u043d\u0438\u044f \u043d\u0430\u0447\u0430\u0442: \u043e\u0442\u043e\u0431\u0440\u0430"
+           "\u043d\u043e \u0441\u0447\u0435\u0442\u043e\u0432 Hyperliquid \u2014 {k}, \u043e\u043a\u043d\u043e 13 "
+           "\u043d\u0435\u0434\u0435\u043b\u044c, \u0434\u043e {date}. \u0421\u043e\u043e\u0431\u0449\u0435\u043d\u0438"
+           "\u044f \u0441 \u043f\u043e\u043c\u0435\u0442\u043a\u043e\u0439 \u00ab\u0411\u0443\u043c\u0430\u0436\u043d"
+           "\u044b\u0439 \u0442\u0435\u0441\u0442\u00bb \u2014 \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 "
+           "\u043c\u0435\u0442\u043e\u0434\u0430 \u0434\u043e \u0440\u0435\u0448\u0435\u043d\u0438\u044f \u043e "
+           "\u043f\u0438\u043b\u043e\u0442\u0435.")
+N_NONE = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u043d\u0435 \u043d\u0430\u0447\u0430\u0442: \u043e\u0442\u0431\u043e\u0440 Hyperliquid \u043d\u0435 \u0434\u0430\u043b \u043d\u0443\u0436\u043d\u043e\u0433\u043e \u0447\u0438\u0441\u043b\u0430 \u0441\u0447\u0435\u0442\u043e\u0432.")
+N_CLOSED = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438\u0440"
+            "\u043e\u0432\u0430\u043d\u0438\u044f: 13 \u043d\u0435\u0434\u0435\u043b\u044c \u043f\u0440\u043e\u0448"
+            "\u043b\u0438, \u043e\u043f\u043e\u0432\u0435\u0449\u0435\u043d\u0438\u044f \u043e\u0441\u0442\u0430\u043d"
+            "\u043e\u0432\u043b\u0435\u043d\u044b. \u0418\u0442\u043e\u0433 \u2014 \u043f\u043e\u0441\u043b\u0435 "
+            "\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u0446\u0438\u0438 \u0434\u0430\u043d\u043d\u044b\u0445 Binance.")
+N_VERDICT = ("\u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u043a\u043e\u043f\u0438"
+             "\u0440\u043e\u0432\u0430\u043d\u0438\u044f: \u0438\u0442\u043e\u0433 \u0437\u0430\u043f\u0438\u0441"
+             "\u0430\u043d \u0438 \u0436\u0434\u0451\u0442 \u0440\u0430\u0437\u0431\u043e\u0440\u0430 \u0410\u0440"
+             "\u0445\u0438\u0442\u0435\u043a\u0442\u043e\u0440\u0430.")
+MINUTES = "\u043c\u0438\u043d"
+HOURS = "\u0447"
+
+
+class Transport(Exception):
+    """A request that produced no readable answer: a fact about the network, never an absence (inv. 70)."""
+
+
+class NotPublished(Exception):
+    """data.binance.vision answered 404."""
+
+
+class NotReady(Exception):
+    """An input is not yet published; the pass is retried later."""
+
+
+class Absent(Exception):
+    """An input that should have been published by now and was not."""
+
+
+# --- time --------------------------------------------------------------------
+def now_ms():
+    return int(time.time() * 1000)
+
+
+def utc_date(ms):
+    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
+
+
+def day_start(date):
+    return int(datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
+
+
+def add_days(date, n):
+    return (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=n)).strftime("%Y-%m-%d")
+
+
+def days_between(first, last):
+    """Every date from first to last inclusive."""
+    out, d = [], first
+    while d <= last:
+        out.append(d)
+        d = add_days(d, 1)
+    return out
+
+
+def iso(ms):
+    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
+
+
+def minute(ms):
+    return ms // 60000 * 60000
+
+
+# --- the rule's inputs read from the checkout ---------------------------------
+def load_rule(repo=REPO):
+    """Capital and medium risk from analyst/owner.json; INV_FLOOR_SD and FEE_TAKER cut from
+    index.html (inv. 20: one number per threshold, system-wide)."""
+    with open(os.path.join(repo, "analyst", "owner.json"), encoding="utf-8") as fh:
+        owner = json.load(fh)
+    with open(os.path.join(repo, "index.html"), encoding="utf-8") as fh:
+        page = fh.read()
+    return {"capital_usdt": float(owner["capital"]["usdt"]), "risk_pct": float(owner["risk"]["risk_pct_medium"]),
+            "inv_floor_sd": common.cut_number(page, "INV_FLOOR_SD"), "fee_taker": common.cut_number(page, "FEE_TAKER")}
+
+
+def fingerprint():
+    """The installed vps tree and this file's MD5 (inv. 38(3))."""
+    try:
+        with open(DEPLOYED_TREE, encoding="utf-8") as fh:
+            tree = fh.read().strip() or "-"
+    except OSError:
+        tree = "-"
+    with open(os.path.abspath(__file__), "rb") as fh:
+        md5 = hashlib.md5(fh.read()).hexdigest()
+    return {"vps_tree": tree, "paper_md5": md5}
+
+
+# --- HTTP ----------------------------------------------------------------------
+def http_get(url):
+    """One GET; the body, or NotPublished on 404, or Transport."""
+    try:
+        with urllib.request.urlopen(url, timeout=common.HTTP_TIMEOUT_S) as resp:
+            return resp.read()
+    except urllib.error.HTTPError as exc:
+        if exc.code == 404:
+            raise NotPublished(url) from None
+        raise Transport("HTTP %d" % exc.code) from None
+    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
+        raise Transport(exc.__class__.__name__) from None
+
+
+def http_post(url, body):
+    """One POST of a JSON body; the parsed answer, or Transport. The outcome is decided
+    after the parse, the last step that can fail (inv. 70)."""
+    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
+                                 headers={"Content-Type": "application/json"})
+    try:
+        with urllib.request.urlopen(req, timeout=common.HTTP_TIMEOUT_S) as resp:
+            raw = resp.read()
+    except urllib.error.HTTPError as exc:
+        raise Transport("HTTP %d" % exc.code) from None
+    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
+        raise Transport(exc.__class__.__name__) from None
+    try:
+        return json.loads(raw)
+    except ValueError:
+        raise Transport("unparseable") from None
+
+
+class Limiter:
+    """The weight spent in the last 60 s, held at or under per_min."""
+
+    def __init__(self, per_min=WEIGHT_PER_MIN, clock=time.monotonic, sleep=time.sleep):
+        self.per_min, self.clock, self.sleep, self.spent = per_min, clock, sleep, []
+
+    def spend(self, weight):
+        while True:
+            now = self.clock()
+            self.spent = [(t, w) for t, w in self.spent if now - t < 60]
+            if not self.spent or sum(w for _, w in self.spent) + weight <= self.per_min:
+                self.spent.append((now, weight))
+                return
+            self.sleep(60 - (now - self.spent[0][0]) + 0.01)
+
+
+def info(body, limiter):
+    limiter.spend(INFO_WEIGHT)
+    doc = http_post(INFO_URL, body)
+    if body.get("type") == "userFillsByTime" and isinstance(doc, list):
+        limiter.spend(len(doc) // 20)    # documented: one more per 20 items returned
+    return doc
+
+
+def iter_fills(addr, start_ms, limiter, end_ms=None):
+    """Every fill of addr from start_ms (inclusive; to end_ms inclusive when given) the API returns,
+    ascending, each tid once, holding only FILL_KEYS and one page at a time: an account with a
+    hundred thousand fills never sits in memory whole. Pages of FILLS_PAGE continue from the last
+    page's last time, which the API repeats; a full page inside one millisecond cannot advance and
+    raises."""
+    t, tids_at_t = start_ms, set()
+    while True:
+        asked = t
+        body = {"type": "userFillsByTime", "user": addr, "startTime": t}
+        if end_ms is not None:
+            body["endTime"] = end_ms
+        page = info(body, limiter)
+        if not isinstance(page, list):
+            raise ValueError("fills: not a list")
+        for f in sorted(page, key=lambda f: (int(f["time"]), int(f["tid"]))):
+            ft = int(f["time"])
+            if ft < t or (ft == t and f["tid"] in tids_at_t):
+                continue
+            if ft > t:
+                t, tids_at_t = ft, set()
+            tids_at_t.add(f["tid"])
+            yield {k: f[k] for k in FILL_KEYS}
+        if len(page) < FILLS_PAGE:
+            return
+        if t == asked:
+            raise ValueError("fills: a full page inside one millisecond")
+
+
+def fills_since(addr, start_ms, limiter, end_ms=None):
+    """iter_fills as a list, for reads that are short by construction: a poll, the probe."""
+    return list(iter_fills(addr, start_ms, limiter, end_ms))
+
+
+# --- the leaderboard, one row at a time ---------------------------------------
+def iter_rows(chunks):
+    """Each object of the "leaderboardRows" array, decoded one at a time from an iterable of
+    bytes: the 39 MB document never exists as one Python object."""
+    decoder = json.JSONDecoder()
+    utf8 = codecs.getincrementaldecoder("utf-8")()
+    chunks = iter(chunks)
+    buf, pos, rows, eof = "", 0, False, False
+    while True:
+        if not rows:
+            i = buf.find('"leaderboardRows"', pos)
+            j = buf.find("[", i) if i >= 0 else -1
+            if j >= 0:
+                pos, rows = j + 1, True
+                continue
+            pos = i if i >= 0 else max(0, len(buf) - 32)
+        else:
+            while pos < len(buf) and buf[pos] in " \t\r\n,":
+                pos += 1
+            if pos < len(buf):
+                if buf[pos] == "]":
+                    return
+                try:
+                    obj, end = decoder.raw_decode(buf, pos)
+                except json.JSONDecodeError:
+                    obj = None
+                if obj is not None:
+                    pos = end
+                    yield obj
+                    continue
+        if eof:
+            raise ValueError("leaderboard: the document ended before its rows did")
+        try:
+            chunk = next(chunks)
+        except StopIteration:
+            chunk, eof = b"", True
+        buf = buf[pos:] + utf8.decode(chunk, final=eof)
+        pos = 0
+
+
+def leaderboard_chunks():
+    try:
+        resp = urllib.request.urlopen(LEADERBOARD_URL, timeout=common.HTTP_TIMEOUT_S)
+    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
+        raise Transport(exc.__class__.__name__) from None
+    with resp:
+        while True:
+            try:
+                chunk = resp.read(65536)
+            except (OSError, http.client.HTTPException) as exc:
+                raise Transport(exc.__class__.__name__) from None
+            if not chunk:
+                return
+            yield chunk
+
+
+def pool_of(rows):
+    """(sorted addresses with all-time volume >= POOL_VOLUME_MIN, rows read, rows unreadable)."""
+    pool, n, bad = set(), 0, 0
+    for row in rows:
+        n += 1
+        try:
+            vlm = float(dict(row["windowPerformances"])["allTime"]["vlm"])
+            addr = row["ethAddress"].lower()
+        except (KeyError, TypeError, ValueError, AttributeError):
+            bad += 1
+            continue
+        if vlm >= POOL_VOLUME_MIN:
+            pool.add(addr)
+    return sorted(pool), n, bad
+
+
+# --- the twelve-month record ----------------------------------------------------
+def step_at(history, t):
+    """The value of the last point at or before t, or None: the series steps between points."""
+    value = None
+    for ms, v in history:
+        if ms > t:
+            break
+        value = v
+    return value
+
+
+def series(points):
+    return sorted((int(ms), float(v)) for ms, v in points)
+
+
+def weekly(pf, t0_ms):
+    """Account value and cumulative PnL of perpAllTime at the 53 grid instants T0 - 52 weeks ... T0."""
+    w = pf["perpAllTime"]
+    av, pn = series(w["accountValueHistory"]), series(w["pnlHistory"])
+    grid = [t0_ms - (LOOKBACK_WEEKS - j) * WEEK_MS for j in range(LOOKBACK_WEEKS + 1)]
+    return [step_at(av, g) for g in grid], [step_at(pn, g) for g in grid]
+
+
+def weekly_returns(values, pnls):
+    """r_j = (P_j - P_{j-1}) / V_{j-1}, j = 1 ... 52; None when an input is missing or a value is not positive."""
+    out = []
+    for j in range(1, len(values)):
+        if None in (values[j - 1], pnls[j - 1], pnls[j]) or values[j - 1] <= 0:
+            return None
+        out.append((pnls[j] - pnls[j - 1]) / values[j - 1])
+    return out
+
+
+def turnover(pf):
+    """perpMonth volume per day over the mean of perpMonth's account values; None when undefined."""
+    w = pf["perpMonth"]
+    pts = series(w["accountValueHistory"])
+    if len(pts) < 2:
+        return None
+    span = (pts[-1][0] - pts[0][0]) / DAY_MS
+    mean = sum(v for _, v in pts) / len(pts)
+    if span < 1 or mean <= 0:
+        return None
+    return float(w["vlm"]) / mean / span
+
+
+def record(returns):
+    """(passes, positive blocks, maximum drawdown, weekly Sharpe or None, 52-week return)."""
+    blocks = sum(1 for b in range(LOOKBACK_WEEKS // BLOCK_WEEKS)
+                 if math.prod(1 + r for r in returns[b * BLOCK_WEEKS:(b + 1) * BLOCK_WEEKS]) - 1 > 0)
+    wealth, peak, dd = 1.0, 1.0, 0.0
+    for r in returns:
+        wealth *= 1 + r
+        peak = max(peak, wealth)
+        dd = max(dd, 1 - wealth / peak)
+    sd = statistics.pstdev(returns)
+    sharpe = statistics.fmean(returns) / sd if sd > 0 else None
+    return blocks >= BLOCKS_MIN and dd <= DRAWDOWN_MAX, blocks, dd, sharpe, wealth - 1
+
+
+def metrics(pf, t0_ms):
+    """The selection's measures of one account's portfolio answer."""
+    pf = dict(pf)
+    values, pnls = weekly(pf, t0_ms)
+    to = turnover(pf)
+    m = {"value_t0": values[-1], "turnover": to, "eligible": False, "r12": False}
+    if (to is None or to > TURNOVER_MAX or values[-1] is None or values[-1] < VALUE_MIN_T0
+            or any(v is None or v < VALUE_MIN_WEEK for v in values[:-1])):
+        return m
+    rets = weekly_returns(values, pnls)
+    if rets is None:
+        return m
+    passes, blocks, dd, sharpe, ret = record(rets)
+    m.update(eligible=True, r12=passes and sharpe is not None, blocks=blocks, drawdown=dd, sharpe=sharpe, ret52=ret)
+    return m
+
+
+# --- episodes -------------------------------------------------------------------
+def sign(x):
+    return (x > 0) - (x < 0)
+
+
+def symbol_for(coin, symbols):
+    """The Binance USD-M symbol a Hyperliquid perpetual is copied on, or None: spot, a builder
+    market and a coin without that exact symbol are not copyable; a "k" coin is the 1000 contract."""
+    if "/" in coin or ":" in coin or coin.startswith("@"):
+        return None
+    base = "1000" + coin[1:] if coin[:1] == "k" and coin[1:2].isupper() else coin
+    sym = base + "USDT"
+    return sym if sym in symbols else None
+
+
+def apply_fill(coins, fill, symbol):
+    """One fill on one copyable coin against coins[coin], the open episode or None. The position
+    before the fill is the fill's own startPosition, so a coin first seen with a position open has
+    no episode until it is flat. Returns the events in order: ("lost", ep) when the episode held
+    disagrees with startPosition, ("close", ep) when the fill flattens or flips it, ("open", ep)
+    when the fill opens from flat or by the flip."""
+    coin = fill["coin"]
+    start = Decimal(fill["startPosition"])
+    size = Decimal(fill["sz"])
+    after = start + size if fill["side"] == "B" else start - size
+    t, px = int(fill["time"]), fill["px"]
+    ep, events = coins.get(coin), []
+    if ep is not None and ep["side"] != sign(start):
+        events.append(("lost", ep))
+        ep = None
+    if ep is not None and sign(after) != ep["side"]:
+        events.append(("close", dict(ep, t_close=t, px_close=px, n=ep["n"] + 1)))
+        ep = None
+    elif ep is not None:
+        ep = dict(ep, n=ep["n"] + 1)
+    if ep is None and after != 0 and sign(start) != sign(after):
+        ep = {"coin": coin, "symbol": symbol, "side": sign(after), "t_open": t, "px_open": px, "n": 1}
+        events.append(("open", ep))
+    coins[coin] = ep
+    return events
+
+
+def copyability(fills, symbols, t_from, t_to):
+    """Venue share of perpetual notional on copyable coins and the median closed-episode
+    duration, over fills in [t_from, t_to); copyable when the share is at least VENUE_SHARE_MIN
+    and the median is at least the longest delay."""
+    total = copyable = 0.0
+    coins, durations = {}, []
+    for f in fills:
+        t, coin = int(f["time"]), f["coin"]
+        if not t_from <= t < t_to or "/" in coin or coin.startswith("@"):
+            continue
+        notional = float(f["px"]) * float(f["sz"])
+        total += notional
+        sym = symbol_for(coin, symbols)
+        if sym is None:
+            continue
+        copyable += notional
+        for kind, ep in apply_fill(coins, f, sym):
+            if kind == "close":
+                durations.append((ep["t_close"] - ep["t_open"]) / 1000)
+    share = copyable / total if total > 0 else 0.0
+    median = statistics.median(durations) if durations else None
+    return {"share": share, "median_episode_s": median, "closed_episodes": len(durations),
+            "copyable": share >= VENUE_SHARE_MIN and median is not None and median >= max(DELAYS_S)}
+
+
+def null_order(t0_ms, addresses):
+    """The null's draw order: by SHA-256 of T0's ISO instant and the address, reproducible anywhere."""
+    stamp = iso(t0_ms)
+    return sorted(addresses, key=lambda a: hashlib.sha256((stamp + a).encode("ascii")).hexdigest())
+
+
+# --- booking ----------------------------------------------------------------------
+def daily_sigma(closes):
+    """Population standard deviation of the daily simple returns of consecutive closes."""
+    return statistics.pstdev([closes[i + 1] / closes[i] - 1 for i in range(len(closes) - 1)])
+
+
+def book_delay(ep, delay_s, dist, kl, capital, risk_frac, fee, window_end):
+    """One episode copied at one delay. kl = (open times ascending, rows (o, h, l, c)). Entry at
+    the close of the minute containing t_open + delay; exit at the close of the minute containing
+    t_close + delay, or of window_end's minute for a cut episode; the stop variant leaves at
+    entry -/+ dist on the first later minute through the exit minute that touches it, at the stop
+    or at that minute's open when it opened beyond. None when the copier would enter after its exit."""
+    times, rows = kl
+    side = ep["side"]
+    entry_m = minute(ep["t_open"] + delay_s * 1000)
+    exit_m = minute(window_end) if ep.get("cut") else minute(ep["t_close"] + delay_s * 1000)
+    if entry_m > exit_m:
+        return None
+    i = bisect.bisect_right(times, entry_m) - 1
+    j = bisect.bisect_right(times, exit_m) - 1
+    if i < 0:
+        raise Absent("no kline at or before the entry minute")
+    entry = rows[i][3]
+    qty = risk_frac * capital / (entry * dist)
+    stop = entry * (1 - side * dist)
+    hit = None
+    for k in range(i + 1, j + 1):
+        o, h, low, _ = rows[k]
+        if side > 0 and low <= stop:
+            hit = (times[k], min(o, stop))
+            break
+        if side < 0 and h >= stop:
+            hit = (times[k], max(o, stop))
+            break
+
+    def leg(exit_ms, px):
+        return {"exit_ms": exit_ms, "px": px, "gross": side * qty * (px - entry), "fee": fee * qty * (entry + px)}
+
+    src = leg(exit_m, rows[j][3])
+    return {"entry_ms": entry_m, "entry_px": entry, "qty": qty, "stop_px": stop, "stopped": hit is not None,
+            "src": src, "stop": leg(*hit) if hit else dict(src)}
+
+
+def funding_paid(side, qty, entry_px, hold_from, hold_to, rates):
+    """side * qty * entry_px * the sum of rates at hold_from < t <= hold_to: positive is paid.
+    The notional is the entry's, not the mark at each event (a stated simplification)."""
+    return side * qty * entry_px * sum(r for t, r in rates if hold_from < t <= hold_to)
+
+
+def vision_rows(path):
+    """The CSV rows of one data.binance.vision zip, a header line dropped."""
+    blob = http_get(VISION + path)
+    try:
+        with zipfile.ZipFile(io.BytesIO(blob)) as z:
+            text = z.read(z.namelist()[0]).decode("utf-8")
+    except (zipfile.BadZipFile, IndexError, UnicodeDecodeError):
+        raise Transport("unreadable zip") from None
+    rows = [line.split(",") for line in text.splitlines() if line.strip()]
+    return rows[1:] if rows and not rows[0][0].strip().isdigit() else rows
+
+
+class Inputs:
+    """data.binance.vision inputs of one pass: 1m klines by symbol and day, daily closes kept on
+    disk, funding rates by symbol and month. A 404 dated more than ABSENT_AFTER_DAYS before today is
+    Absent; nearer is NotReady."""
+
+    def __init__(self, state_dir, today, rows=vision_rows):
+        self.today, self.rows, self.klines, self.rates_by = today, rows, {}, {}
+        self.closes_path = os.path.join(state_dir, "closes.json")
+        try:
+            with open(self.closes_path, encoding="utf-8") as fh:
+                self.closes = json.load(fh)
+        except (OSError, ValueError):
+            self.closes = {}
+
+    def fetch(self, path, ref_date):
+        try:
+            return self.rows(path)
+        except NotPublished:
+            gap = (datetime.strptime(self.today, "%Y-%m-%d") - datetime.strptime(ref_date, "%Y-%m-%d")).days
+            raise (Absent if gap > ABSENT_AFTER_DAYS else NotReady)(path) from None
+
+    def minutes(self, sym, date):
+        key = (sym, date)
+        if key not in self.klines:
+            rows = self.fetch("/daily/klines/%s/1m/%s-1m-%s.zip" % (sym, sym, date), date)
+            self.klines[key] = [(int(r[0]), (float(r[1]), float(r[2]), float(r[3]), float(r[4]))) for r in rows]
+        return self.klines[key]
+
+    def kl(self, sym, first, last):
+        merged = sorted(row for d in days_between(first, last) for row in self.minutes(sym, d))
+        return [t for t, _ in merged], [r for _, r in merged]
+
+    def close_on(self, sym, date):
+        have = self.closes.setdefault(sym, {})
+        if date not in have:
+            rows = self.fetch("/daily/klines/%s/1d/%s-1d-%s.zip" % (sym, sym, date), date)
+            have[date] = float(rows[0][4])
+            common.atomic_write(self.closes_path, self.closes, mode=0o640)
+        return have[date]
+
+    def rates(self, sym, month):
+        key = (sym, month)
+        if key not in self.rates_by:
+            last_day = add_days((datetime.strptime(month + "-01", "%Y-%m-%d") + timedelta(days=32))
+                                .strftime("%Y-%m-01"), -1)
+            rows = self.fetch("/monthly/fundingRate/%s/%s-fundingRate-%s.zip" % (sym, sym, month), last_day)
+            self.rates_by[key] = [(int(r[0]), float(r[2])) for r in rows]
+        return self.rates_by[key]
+
+
+def book_episode(ep, inputs, rule, window_end):
+    """The book line of one episode: sigma_for, the stop distance INV_FLOOR_SD sigma, and every
+    delay; or an unbookable line."""
+    line = {"k": "book", "a": ep["a"], "coin": ep["coin"], "symbol": ep["symbol"], "side": ep["side"],
+            "t_open": ep["t_open"]}
+    first = utc_date(ep["t_open"])
+    try:
+        sigma = sigma_for(inputs, ep["symbol"], ep["t_open"])
+        dist = rule["inv_floor_sd"] * sigma
+        if not dist > 0:
+            raise Absent("sigma is zero")
+        last = utc_date(window_end if ep.get("cut") else ep["t_close"] + max(DELAYS_S) * 1000)
+        kl = inputs.kl(ep["symbol"], first, last)
+        line.update(sigma_d=sigma, dist=dist, d={
+            str(d): book_delay(ep, d, dist, kl, rule["capital_usdt"], rule["risk_pct"] / 100, rule["fee_taker"],
+                               window_end) for d in DELAYS_S})
+    except Absent as exc:
+        line["unbookable"] = str(exc)
+    return line
+
+
+def funding_line(book, inputs):
+    """The funding of one booked episode, per delay and variant, from the monthly archives."""
+    line = {"k": "funding", "a": book["a"], "coin": book["coin"], "t_open": book["t_open"], "absent": False, "d": {}}
+    if "d" not in book:
+        line["unbooked"] = True
+        return line
+    spans = [(b["entry_ms"] + 60000, b[v]["exit_ms"] + 60000) for b in book["d"].values() if b for v in ("src", "stop")]
+    rates = []
+    if spans:
+        month, end = utc_date(min(s for s, _ in spans))[:7], utc_date(max(e for _, e in spans))[:7]
+        while month <= end:
+            try:
+                rates += inputs.rates(book["symbol"], month)
+            except Absent:
+                line["absent"] = True
+            month = (datetime.strptime(month + "-01", "%Y-%m-%d") + timedelta(days=32)).strftime("%Y-%m")
+    for d, b in book["d"].items():
+        line["d"][d] = None if b is None else {
+            v: funding_paid(book["side"], b["qty"], b["entry_px"], b["entry_ms"] + 60000, b[v]["exit_ms"] + 60000, rates)
+            for v in ("src", "stop")}
+    return line
+
+
+# --- the verdict -----------------------------------------------------------------
+def decide(picks, null, results, pick_episodes):
+    """results[a][d][v]: net over capital. TOP is the picks' mean; the null is every k-subset of the
+    null accounts. Readable with at least one pick, NULL_MIN null accounts and EPISODES_MIN booked
+    pick episodes at 1 800 s; passed when readable and, at every deciding delay on the stop
+    variant, TOP > 0 and TOP > the null subsets' median."""
+    k, out = len(picks), {}
+    subsets = list(combinations(null, k)) if 0 < k <= len(null) else []
+    for d in DELAYS_S:
+        for v in ("stop", "src"):
+            top = statistics.fmean(results[a][d][v] for a in picks) if k else None
+            means = [statistics.fmean(results[a][d][v] for a in c) for c in subsets]
+            med = statistics.median(means) if means else None
+            share = sum(1 for x in means if x >= top) / len(means) if means else None
+            out["%d/%s" % (d, v)] = {"top": top, "null_median": med, "null_share_at_or_above": share,
+                                     "picks": {a: results[a][d][v] for a in picks}}
+    readable = k >= 1 and len(null) >= NULL_MIN and pick_episodes >= EPISODES_MIN
+    passed = readable and all(out["%d/stop" % d]["top"] > 0 and out["%d/stop" % d]["top"] > out["%d/stop" % d]["null_median"]
+                              for d in DECIDING_S)
+    return {"readable": readable, "passed": passed, "cells": out}
+
+
+def nearest_rank(values, q):
+    if not values:
+        return None
+    ordered = sorted(values)
+    return ordered[max(0, math.ceil(q * len(ordered)) - 1)]
+
+
+# --- records ---------------------------------------------------------------------
+def write_record(state, state_dir, rel, lines=None, doc=None):
+    """One record into the local mirror, atomically, and onto the pending list (inv. 72)."""
+    path = os.path.join(state_dir, "records", RECORD_DIR, rel)
+    os.makedirs(os.path.dirname(path), exist_ok=True)
+    if doc is not None:
+        data = json.dumps(doc, separators=(",", ":"), allow_nan=False, sort_keys=True) + "\n"
+    else:
+        data = "".join(json.dumps(x, separators=(",", ":"), allow_nan=False, sort_keys=True) + "\n" for x in lines)
+    common.atomic_write(path, data, mode=0o644)
+    state["pending"] = sorted(set(state["pending"]) | {rel})
+
+
+def read_jsonl(path):
+    with open(path, encoding="utf-8") as fh:
+        return [json.loads(line) for line in fh if line.strip()]
+
+
+def publish(state, state_dir, tree):
+    """Pending records into the clone at origin/main and pushed (contract v30 section 8). A path
+    main already holds leaves the list unchanged on main: equal bytes are done, different bytes are
+    logged and main's copy stands \u2014 a record is never reopened."""
+    git = lambda *a: common.git_quiet(tree, *a)  # noqa: E731
+    if git("fetch", "-q", "origin", "main") != 0:
+        return "fetch failed"
+    git("reset", "-q", "--hard", "origin/main")
+    git("clean", "-q", "-fdx", "--", RECORD_DIR)
+    copied, done = [], []
+    for rel in state["pending"]:
+        src = os.path.join(state_dir, "records", RECORD_DIR, rel)
+        dst = os.path.join(tree, RECORD_DIR, rel)
+        if os.path.exists(dst):
+            with open(src, "rb") as a, open(dst, "rb") as b:
+                if a.read() != b.read():
+                    common.log("paper: %s differs from main; main's copy stands" % rel)
+            done.append(rel)
+            continue
+        os.makedirs(os.path.dirname(dst), exist_ok=True)
+        shutil.copyfile(src, dst)
+        copied.append(rel)
+    pushed = None
+    if copied:
+        _, pushed = common.publish(tree, [os.path.join(RECORD_DIR, r) for r in copied], "paper: " + ", ".join(copied))
+        if pushed:
+            done += copied
+    state["pending"] = [r for r in state["pending"] if r not in done]
+    return "copied=%d pushed=%s left=%d" % (len(copied), "-" if pushed is None else ("yes" if pushed else "no"),
+                                            len(state["pending"]))
+
+
+# --- selection ----------------------------------------------------------------------
+def read_work(path):
+    """The work file's lines; a torn last line is dropped."""
+    out = []
+    try:
+        with open(path, encoding="utf-8") as fh:
+            for line in fh:
+                try:
+                    out.append(json.loads(line))
+                except ValueError:
+                    break
+    except FileNotFoundError:
+        pass
+    return out
+
+
+def append_work(path, obj):
+    with open(path, "a", encoding="utf-8") as fh:
+        fh.write(json.dumps(obj, separators=(",", ":"), allow_nan=False) + "\n")
+        fh.flush()
+        os.fsync(fh.fileno())
+
+
+def retrying(call, *args, give_up=False):
+    """call(*args), waiting TRANSPORT_WAIT_S after each Transport. After TRANSPORT_MAX in a row, a step
+    the selection can do without -- one account -- is given up: None, which the caller records as
+    unreadable for transport, never as absent (inv. 70); a step it cannot do without ends the process,
+    which its unit restarts, and the selection resumes from its work file."""
+    for attempt in range(TRANSPORT_MAX):
+        try:
+            return call(*args)
+        except Transport as exc:
+            common.log("paper: transport %s, attempt %d of %d" % (exc, attempt + 1, TRANSPORT_MAX))
+            time.sleep(TRANSPORT_WAIT_S)
+    if give_up:
+        return None
+    sys.exit(4)
+
+
+def select(state_dir, rule, limiter, clock=now_ms):
+    """The selection, resumable: T0, the pool, every pool account's measures, the Binance list, the
+    picks walked down the ranking and the null walked down its order, each step kept in the work file."""
+    path = os.path.join(state_dir, "selection-work.jsonl")
+    work = read_work(path)
+    head = next((w for w in work if "t0_ms" in w), None)
+    if head is None:
+        head = {"t0_ms": day_start(utc_date(clock()))}
+        append_work(path, head)
+    t0 = head["t0_ms"]
+    pool = next((w for w in work if "pool" in w), None)
+    if pool is None:
+        pool_list, n, bad = retrying(lambda: pool_of(iter_rows(leaderboard_chunks())))
+        pool = {"pool": pool_list, "rows": n, "bad_rows": bad}
+        append_work(path, pool)
+        common.log("paper: pool rows=%d pool=%d bad=%d" % (n, len(pool_list), bad))
+    measured = {w["a"]: w["m"] for w in work if "a" in w}
+    for addr in pool["pool"]:
+        if addr in measured:
+            continue
+        doc = retrying(info, {"type": "portfolio", "user": addr}, limiter, give_up=True)
+        try:
+            m = metrics(doc, t0) if doc is not None else {"unreadable": "transport", "eligible": False, "r12": False}
+        except (KeyError, TypeError, ValueError, IndexError, ZeroDivisionError, OverflowError):
+            m = {"unreadable": "shape", "eligible": False, "r12": False}
+        measured[addr] = m
+        append_work(path, {"a": addr, "m": m})
+        if len(measured) % 500 == 0:
+            common.log("paper: measured %d of %d" % (len(measured), len(pool["pool"])))
+    symbols = next((w["symbols"] for w in work if "symbols" in w), None)
+    if symbols is None:
+        symbols = sorted(p["symbol"] for p in exchange.perpetuals(retrying(fetch_exchange)))
+        append_work(path, {"symbols": symbols})
+    symbol_set = set(symbols)
+    checked = {w["c"]: w["r"] for w in work if "c" in w}
+
+    def check(addr):
+        if addr not in checked:
+            start = t0 - WINDOW_DAYS * DAY_MS
+            try:
+                found = retrying(lambda: copyability(iter_fills(addr, start, limiter, t0 - 1), symbol_set, start, t0),
+                                 give_up=True)
+                checked[addr] = found if found is not None else {"unreadable": "transport", "copyable": False}
+            except (KeyError, TypeError, ValueError, ArithmeticError):
+                checked[addr] = {"unreadable": "shape", "copyable": False}
+            append_work(path, {"c": addr, "r": checked[addr]})
+        return checked[addr]
+
+    ranked = sorted((a for a, m in measured.items() if m.get("r12")), key=lambda a: (-measured[a]["sharpe"], a))
+    picks, rejected = [], []
+    for addr in ranked:
+        if len(picks) == TOP_K:
+            break
+        (picks if check(addr)["copyable"] else rejected).append(addr)
+    eligible = sorted(a for a, m in measured.items() if m.get("eligible"))
+    null = []
+    for addr in null_order(t0, [a for a in eligible if a not in picks]):
+        if len(null) == NULL_M:
+            break
+        if check(addr)["copyable"]:
+            null.append(addr)
+    follow_from = clock()
+    entry = lambda a: {**measured[a], **checked.get(a, {}), "address": a}  # noqa: E731
+    return {"v": 1, "k": "paper-selection", "t0": iso(t0), "t0_ms": t0, "follow_from": iso(follow_from),
+            "follow_from_ms": follow_from, "window_end": iso(follow_from + WINDOW_DAYS * DAY_MS),
+            "window_end_ms": follow_from + WINDOW_DAYS * DAY_MS, "rule": dict(rule, delays_s=list(DELAYS_S)),
+            "counts": {"rows": pool["rows"], "bad_rows": pool["bad_rows"], "pool": len(pool["pool"]),
+                       "unreadable": sum(1 for m in measured.values() if m.get("unreadable")),
+                       "eligible": len(eligible), "r12": len(ranked), "checked": len(checked)},
+            "picks": [dict(entry(a), rank=i + 1) for i, a in enumerate(picks)],
+            "rejected": [entry(a) for a in rejected], "null": [entry(a) for a in null],
+            "eligible": eligible, "symbols": symbols, "fp": fingerprint()}
+
+
+def fetch_exchange():
+    try:
+        return exchange.fetch_info()
+    except (urllib.error.URLError, OSError, http.client.HTTPException, ValueError) as exc:
+        raise Transport(exc.__class__.__name__) from None
+
+
+# --- following ----------------------------------------------------------------------
+def addr_short(addr):
+    return addr[:6] + "\u2026" + addr[-4:]
+
+
+def side_word(side):
+    return "LONG" if side > 0 else "SHORT"
+
+
+def decimals(px):
+    return len(px.split(".", 1)[1]) if "." in px else 0
+
+
+def hhmm(ms):
+    return datetime.fromtimestamp(ms / 1000, tz=announce.TBILISI).strftime("%H:%M")
+
+
+def held_text(ms):
+    minutes = ms / 60000
+    return ("%d " % round(minutes) + MINUTES) if minutes < 60 else ("%.1f " % (minutes / 60) + HOURS)
+
+
+def sigma_for(inputs, sym, t_open):
+    """sigma of the 31 daily closes of days D-32 ... D-2, D the opening day: every one is published
+    by the time any episode of day D opens."""
+    first = utc_date(t_open)
+    return daily_sigma([inputs.close_on(sym, add_days(first, -k)) for k in range(SIGMA_DAYS + 2, 1, -1)])
+
+
+def alert_open(ep, rank, rule, sigma):
+    base = {"hhmm": hhmm(ep["t_open"]), "rank": rank, "addr": addr_short(ep["a"]), "side": side_word(ep["side"]),
+            "symbol": ep["symbol"], "px": ep["px_open"]}
+    if sigma is None or not sigma > 0:
+        return P_OPEN_BARE.format(**base)
+    dist = rule["inv_floor_sd"] * sigma
+    stop = float(ep["px_open"]) * (1 - ep["side"] * dist)
+    notional = rule["risk_pct"] / 100 * rule["capital_usdt"] / dist
+    return P_OPEN.format(dist="%.1f" % (dist * 100), stop="%.*f" % (decimals(ep["px_open"]), stop),
+                         notional="%d" % round(notional), risk=("%g" % rule["risk_pct"]), **base)
+
+
+def alert_close(ep, rank):
+    return P_CLOSE.format(hhmm=hhmm(ep["t_close"]), rank=rank, addr=addr_short(ep["a"]), side=side_word(ep["side"]),
+                          symbol=ep["symbol"], px=ep["px_close"], held=held_text(ep["t_close"] - ep["t_open"]))
+
+
+def starts(sel):
+    """The test follows only when it can be read: at least one pick and NULL_MIN null accounts."""
+    return len(sel["picks"]) >= 1 and len(sel["null"]) >= NULL_MIN
+
+
+def new_state(sel):
+    accounts = {}
+    for role, rows in (("pick", sel["picks"]), ("null", sel["null"])):
+        for row in rows:
+            accounts[row["address"]] = {"role": role, "rank": row.get("rank"), "last_ms": sel["follow_from_ms"],
+                                        "last_tids": [], "polled_ms": 0, "due_ms": 0, "coins": {}, "fills": {},
+                                        "lost": {}, "failing": False}
+    return {"v": 1, "accounts": accounts, "closed": [], "cut": False, "written": {"episodes": None, "book": None,
+            "funding": None}, "verdict": False, "pending": [], "next_work_ms": 0, "next_publish_ms": 0,
+            "closed_notice": False}
+
+
+def poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for):
+    """New fills since the account's last time, through apply_fill; alerts for a pick's fresh events.
+    The account's state changes only when the whole poll succeeded."""
+    fills = fills_since(addr, acct["last_ms"], limiter)
+    work = json.loads(json.dumps(acct))
+    _apply(addr, work, fills, sel, symbols, now, rule, inputs_for)
+    acct.clear()
+    acct.update(work)
+
+
+def _apply(addr, acct, fills, sel, symbols, now, rule, inputs_for):
+    window_end = sel["window_end_ms"]
+    for f in fills:
+        t = int(f["time"])
+        if (t == acct["last_ms"] and f["tid"] in acct["last_tids"]) or t >= window_end:
+            continue
+        sym = symbol_for(f["coin"], symbols)
+        if sym is None:
+            continue
+        day = utc_date(t)
+        acct["fills"][day] = acct["fills"].get(day, 0) + 1
+        for kind, ep in apply_fill(acct["coins"], f, sym):
+            if kind == "lost":
+                acct["lost"][day] = acct["lost"].get(day, 0) + 1
+                continue
+            if kind == "open":
+                ep.update(a=addr, role=acct["role"], rank=acct["rank"], seen_open_ms=now)
+            else:
+                ep.update(seen_close_ms=now, cut=False)
+                acct["closed_buffer"] = acct.get("closed_buffer", []) + [ep]
+            if acct["role"] == "pick" and now - t <= ALERT_MAX_AGE_S * 1000 and now < window_end:
+                if kind == "open":
+                    try:
+                        sigma = sigma_for(inputs_for(), sym, t)
+                    except (NotReady, Absent, Transport, ValueError, ZeroDivisionError):
+                        sigma = None
+                    common.write_outbox("alert", alert_open(ep, acct["rank"], rule, sigma))
+                else:
+                    common.write_outbox("alert", alert_close(ep, acct["rank"]))
+    if fills:
+        acct["last_ms"] = max(acct["last_ms"], max(int(f["time"]) for f in fills))
+        acct["last_tids"] = [f["tid"] for f in fills if int(f["time"]) == acct["last_ms"]]
+    acct["polled_ms"] = now
+
+
+def gather_closed(state):
+    for acct in state["accounts"].values():
+        state["closed"] += acct.pop("closed_buffer", [])
+
+
+def cut_open(state, sel):
+    """At window_end, once every account was polled DAY_SETTLE_S past it: every open episode closes at
+    window_end, cut, and following stops."""
+    for addr, acct in state["accounts"].items():
+        for coin, ep in list(acct["coins"].items()):
+            if ep is not None:
+                state["closed"].append(dict(ep, t_close=sel["window_end_ms"], px_close=None, seen_close_ms=None,
+                                            cut=True))
+            acct["coins"][coin] = None
+    state["cut"] = True
+
+
+def next_date(written, first):
+    return first if written is None else add_days(written, 1)
+
+
+def produce_days(state, state_dir, sel, now):
+    """Episode files, in date order, for every day all accounts were polled DAY_SETTLE_S past; an
+    episode that closed on a day already written goes into the next file, never lost."""
+    first, last = utc_date(sel["follow_from_ms"]), utc_date(sel["window_end_ms"])
+    settled = min(a["polled_ms"] for a in state["accounts"].values())
+    while True:
+        day = next_date(state["written"]["episodes"], first)
+        if day > last or (day == last and not state["cut"]):
+            return
+        if day < last and settled < day_start(day) + DAY_MS + DAY_SETTLE_S * 1000:
+            return
+        eps = sorted((e for e in state["closed"] if utc_date(e["t_close"]) <= day),
+                     key=lambda e: (e["t_close"], e["a"], e["coin"], e["t_open"]))
+        head = {"k": "day", "date": day, "episodes": len(eps), "accounts": {
+            a: {"fills": acct["fills"].get(day, 0), "lost": acct["lost"].get(day, 0)}
+            for a, acct in sorted(state["accounts"].items())}}
+        write_record(state, state_dir, "episodes/%s.jsonl" % day, [head] + [dict(e, k="ep") for e in eps])
+        state["closed"] = [e for e in state["closed"] if utc_date(e["t_close"]) > day]
+        state["written"]["episodes"] = day
+
+
+def produce_books(state, state_dir, sel, rule, inputs):
+    first = utc_date(sel["follow_from_ms"])
+    while True:
+        day = next_date(state["written"]["book"], first)
+        if state["written"]["episodes"] is None or day > state["written"]["episodes"]:
+            return
+        eps = [e for e in read_jsonl(os.path.join(state_dir, "records", RECORD_DIR, "episodes", day + ".jsonl"))
+               if e["k"] == "ep"]
+        lines = [book_episode(e, inputs, rule, sel["window_end_ms"]) for e in eps]   # NotReady ends the pass
+        head = {"k": "day", "date": day, "booked": sum(1 for x in lines if "d" in x),
+                "unbookable": sum(1 for x in lines if "unbookable" in x)}
+        write_record(state, state_dir, "book/%s.jsonl" % day, [head] + lines)
+        state["written"]["book"] = day
+
+
+def produce_funding(state, state_dir, sel, inputs):
+    first = utc_date(sel["follow_from_ms"])
+    while True:
+        day = next_date(state["written"]["funding"], first)
+        if state["written"]["book"] is None or day > state["written"]["book"]:
+            return
+        books = [b for b in read_jsonl(os.path.join(state_dir, "records", RECORD_DIR, "book", day + ".jsonl"))
+                 if b["k"] == "book"]
+        lines = [funding_line(b, inputs) for b in books]
+        head = {"k": "day", "date": day, "lines": len(lines), "absent": sum(1 for x in lines if x["absent"])}
+        write_record(state, state_dir, "funding/%s.jsonl" % day, [head] + lines)
+        state["written"]["funding"] = day
+
+
+def produce_verdict(state, state_dir, sel, rule):
+    last = utc_date(sel["window_end_ms"])
+    if state["verdict"] or state["written"]["funding"] != last:
+        return False
+    root = os.path.join(state_dir, "records", RECORD_DIR)
+    days = days_between(utc_date(sel["follow_from_ms"]), last)
+    picks = [p["address"] for p in sel["picks"]]
+    null = [p["address"] for p in sel["null"]]
+    results = {a: {d: {"src": 0.0, "stop": 0.0} for d in DELAYS_S} for a in picks + null}
+    booked = {d: {"pick": 0, "null": 0} for d in DELAYS_S}
+    lags, unbookable, absent = [], 0, 0
+    for day in days:
+        for e in read_jsonl(os.path.join(root, "episodes", day + ".jsonl")):
+            if e["k"] == "ep" and e["role"] == "pick" and e.get("seen_open_ms"):
+                lags.append((e["seen_open_ms"] - e["t_open"]) / 1000)
+        books = {(b["a"], b["coin"], b["t_open"]): b for b in read_jsonl(os.path.join(root, "book", day + ".jsonl"))
+                 if b["k"] == "book"}
+        for f in read_jsonl(os.path.join(root, "funding", day + ".jsonl")):
+            if f["k"] != "funding":
+                continue
+            b = books[(f["a"], f["coin"], f["t_open"])]
+            if "d" not in b:
+                unbookable += 1
+                continue
+            absent += 1 if f["absent"] else 0
+            role = "pick" if f["a"] in picks else "null"
+            for d in DELAYS_S:
+                cell = b["d"][str(d)]
+                if cell is None:
+                    continue
+                booked[d][role] += 1
+                for v in ("src", "stop"):
+                    results[f["a"]][d][v] += (cell[v]["gross"] - cell[v]["fee"] - f["d"][str(d)][v]) / rule["capital_usdt"]
+    verdict = decide(picks, null, results, booked[1800]["pick"])
+    doc = {"v": 1, "k": "paper-verdict", "follow_from": sel["follow_from"], "window_end": sel["window_end"],
+           "picks": picks, "null": null, "booked": {str(d): booked[d] for d in DELAYS_S}, "unbookable": unbookable,
+           "funding_absent": absent, "lag_s": {"n": len(lags), "p50": nearest_rank(lags, 0.5),
+                                                 "p95": nearest_rank(lags, 0.95)}, "fp": fingerprint()}
+    doc.update(verdict)
+    write_record(state, state_dir, "verdict.json", doc=doc)
+    state["verdict"] = True
+    return True
+
+
+# --- the service ---------------------------------------------------------------------
+def load_state(path, sel):
+    try:
+        with open(path, encoding="utf-8") as fh:
+            return json.load(fh)
+    except (OSError, ValueError):
+        return new_state(sel)
+
+
+def stored_selection(state_dir, tree):
+    """The selection from the local mirror, else from main."""
+    for root in (os.path.join(state_dir, "records"), tree):
+        try:
+            with open(os.path.join(root, RECORD_DIR, "selection.json"), encoding="utf-8") as fh:
+                return json.load(fh)
+        except (OSError, ValueError):
+            continue
+    return None
+
+
+def service(state_dir, tree):
+    rule = load_rule()
+    limiter = Limiter()
+    common.git_quiet(tree, "fetch", "-q", "origin", "main")
+    common.git_quiet(tree, "reset", "-q", "--hard", "origin/main")
+    sel = stored_selection(state_dir, tree)
+    state_path = os.path.join(state_dir, "state.json")
+    if sel is None:
+        common.log("paper: selection started")
+        sel = select(state_dir, rule, limiter)
+        state = new_state(sel)
+        write_record(state, state_dir, "selection.json", doc=sel)
+        end = datetime.fromtimestamp(sel["window_end_ms"] / 1000, tz=announce.TBILISI).strftime("%d.%m.%Y")
+        common.write_outbox("notice", N_START.format(k=len(sel["picks"]), date=end) if starts(sel) else N_NONE)
+        common.atomic_write(state_path, state, mode=0o640)
+        common.log("paper: selection done picks=%d null=%d" % (len(sel["picks"]), len(sel["null"])))
+    rule = sel["rule"]    # frozen at the selection: a later change of owner.json moves nothing here
+    state = load_state(state_path, sel)
+    written = None
+    symbols = set(sel["symbols"])
+    inputs_box = {}
+
+    def inputs_for():
+        today = utc_date(now_ms())
+        if inputs_box.get("today") != today:
+            inputs_box.update(today=today, inputs=Inputs(state_dir, today))
+        return inputs_box["inputs"]
+
+    while True:
+        now = now_ms()
+        if starts(sel) and not state["cut"]:
+            for addr, acct in state["accounts"].items():
+                if now < acct["due_ms"]:
+                    continue
+                acct["due_ms"] = now + 1000 * (PICK_POLL_S if acct["role"] == "pick" else NULL_POLL_S)
+                try:
+                    poll(addr, acct, sel, symbols, limiter, now, rule, inputs_for)
+                    if acct["failing"]:
+                        common.log("paper: poll %s answered again" % addr_short(addr))
+                    acct["failing"] = False
+                except (Transport, KeyError, TypeError, ValueError, ArithmeticError) as exc:
+                    if not acct["failing"]:
+                        common.log("paper: poll %s failed (%s)" % (addr_short(addr), exc.__class__.__name__))
+                    acct["failing"] = True
+            gather_closed(state)
+            if now >= sel["window_end_ms"] and all(a["polled_ms"] >= sel["window_end_ms"] + DAY_SETTLE_S * 1000
+                                                    for a in state["accounts"].values()):
+                cut_open(state, sel)
+                if not state["closed_notice"]:
+                    common.write_outbox("notice", N_CLOSED)
+                    state["closed_notice"] = True
+        if starts(sel):
+            try:
+                produce_days(state, state_dir, sel, now)
+            except (OSError, ValueError) as exc:
+                common.log("paper: day file failed (%s)" % exc.__class__.__name__)
+            if now >= state["next_work_ms"]:
+                state["next_work_ms"] = now + WORK_EVERY_S * 1000
+                try:
+                    produce_books(state, state_dir, sel, rule, inputs_for())
+                    produce_funding(state, state_dir, sel, inputs_for())
+                    if produce_verdict(state, state_dir, sel, rule):
+                        common.write_outbox("notice", N_VERDICT)
+                except NotReady:
+                    pass
+                except (Transport, OSError, ValueError, KeyError, ArithmeticError) as exc:
+                    common.log("paper: booking failed (%s)" % exc.__class__.__name__)
+        if state["pending"] and now >= state["next_publish_ms"]:
+            state["next_publish_ms"] = now + PUBLISH_EVERY_S * 1000
+            common.log("paper: publish " + publish(state, state_dir, tree))
+        text = json.dumps(state, separators=(",", ":"), allow_nan=False)
+        if text != written:
+            common.atomic_write(state_path, text + "\n", mode=0o640)
+            written = text
+        time.sleep(LOOP_S)
+
+
+# --- the probe -----------------------------------------------------------------------
+def probe():
+    """One read of every interface the service uses; one line each, counts only. Exit 0 when every
+    read answered."""
+    ok, limiter, t0 = True, Limiter(), day_start(utc_date(now_ms()))
+    yesterday = add_days(utc_date(now_ms()), -1)
+    prev_month = add_days(utc_date(now_ms())[:8] + "01", -1)[:7]
+    steps = (
+        ("leaderboard", lambda: "rows=%d pool=%d bad=%d" % (lambda p: (p[1], len(p[0]), p[2]))(
+            pool_of(iter_rows(leaderboard_chunks())))),
+        ("portfolio", lambda: " ".join("%s=%s" % (k, v) for k, v in sorted(
+            metrics(info({"type": "portfolio", "user": PROBE_ACCOUNT}, limiter), t0).items()))),
+        ("exchange", lambda: "perpetuals=%d" % len(exchange.perpetuals(fetch_exchange()))),
+        ("fills", lambda: (lambda fl: "fills=%d first=%s" % (len(fl), iso(int(fl[0]["time"])) if fl else "-"))(
+            fills_since(PROBE_ACCOUNT, t0 - WINDOW_DAYS * DAY_MS, limiter, t0 - 1))),
+        ("klines_1m", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1m/BTCUSDT-1m-%s.zip" % yesterday))),
+        ("klines_1d", lambda: "rows=%d" % len(vision_rows("/daily/klines/BTCUSDT/1d/BTCUSDT-1d-%s.zip" % yesterday))),
+        ("funding", lambda: "rows=%d" % len(vision_rows(
+            "/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-%s.zip" % prev_month))),
+    )
+    for name, step in steps:
+        try:
+            line = step()
+        except Exception as exc:
+            ok, line = False, "failed (%s)" % exc.__class__.__name__
+        common.log("paper: probe %s %s" % (name, line))
+    common.log("paper: probe peak_rss_kib=%d" % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
+    return 0 if ok else 1
+
+
+def main(argv=None):
+    parser = argparse.ArgumentParser(description="the copy-trading paper test")
+    parser.add_argument("--state-dir", default=STATE_DIR)
+    parser.add_argument("--tree", default=TREE)
+    parser.add_argument("--probe", action="store_true")
+    args = parser.parse_args(argv)
+    if args.probe:
+        return probe()
+    return service(args.state_dir, args.tree)
+
+
+if __name__ == "__main__":
+    sys.exit(main())
diff --git a/vps/selftest.py b/vps/selftest.py
index 5317db0..3963832 100644
--- a/vps/selftest.py
+++ b/vps/selftest.py
@@ -1,8 +1,8 @@
 #!/usr/bin/env python3
 """The VPS assistant's selftest (TZ-54 B10, TZ-55 B7, TZ-56 B5, TZ-57 B5, TZ-58 B3, TZ-60 B7,
-TZ-62 B2): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's, TZ-57 §12.8's,
-TZ-58 §12.7's, TZ-60 §12.11's and TZ-62 §12.4's changed and new ones, each printing `section <X>:
-checks <n> failed <m>`, then the total.
+TZ-62 B2, TZ-64 B4): the sections of TZ-54 §12.14 with TZ-55 §12.7's, TZ-56 §12.6's, TZ-57 §12.8's,
+TZ-58 §12.7's, TZ-60 §12.11's, TZ-62 §12.4's and TZ-64's changed and new ones, each printing
+`section <X>: checks <n> failed <m>`, then the total.
 
     python3 vps/selftest.py
 
@@ -33,6 +33,7 @@ import bot  # noqa: E402
 import cleanup  # noqa: E402
 import common  # noqa: E402
 import exchange  # noqa: E402
+import paper  # noqa: E402
 import run  # noqa: E402
 import stop  # noqa: E402
 import writer  # noqa: E402
@@ -1158,11 +1159,507 @@ def section_u(s):
             unit_lines.count("Environment=CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1") == 1)
 
 
+# --- V: common.publish on a local remote, through the writer and for new files (TZ-64) ----
+def _v_git(cwd, *args):
+    return subprocess.run(["git", "-C", cwd] + list(args), capture_output=True, text=True)
+
+
+def _v_head(cwd, ref="HEAD"):
+    return _v_git(cwd, "rev-parse", ref).stdout.strip()
+
+
+def section_v(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-v.")
+    try:
+        remote, a, b = (os.path.join(tmp, n) for n in ("remote.git", "a", "b"))
+        _v_git(tmp, "init", "-q", "--bare", "-b", "main", remote)
+        reject = os.path.join(tmp, "reject")
+        hook = os.path.join(remote, "hooks", "pre-receive")
+        with open(hook, "w", encoding="utf-8") as fh:
+            fh.write("#!/bin/sh\n[ -e '%s' ] && exit 1\nexit 0\n" % reject)
+        os.chmod(hook, 0o755)
+        _v_git(tmp, "clone", "-q", remote, b)
+        for clone in (b,):
+            _v_git(clone, "config", "user.name", "selftest")
+            _v_git(clone, "config", "user.email", "selftest@localhost")
+        os.makedirs(os.path.join(b, "analyst"))
+        with open(os.path.join(b, writer.PAYLOAD), "w", encoding="utf-8") as fh:
+            fh.write("{}\n")
+        _v_git(b, "add", "-A")
+        _v_git(b, "commit", "-q", "-m", "base")
+        _v_git(b, "push", "-q", "origin", "HEAD:main")
+        _v_git(tmp, "clone", "-q", "-b", "main", remote, a)
+        _v_git(a, "config", "user.name", "selftest")
+        _v_git(a, "config", "user.email", "selftest@localhost")
+
+        def fresh():
+            _v_git(a, "fetch", "-q", "origin", "main")
+            _v_git(a, "reset", "-q", "--hard", "origin/main")
+
+        def payload(clone, text):
+            with open(os.path.join(clone, writer.PAYLOAD), "w", encoding="utf-8") as fh:
+                fh.write(text)
+
+        def other_writer(path, text):
+            _v_git(b, "pull", "-q", "origin", "main")
+            with open(os.path.join(b, path), "w", encoding="utf-8") as fh:
+                fh.write(text)
+            _v_git(b, "add", "-A")
+            _v_git(b, "commit", "-q", "-m", "other")
+            _v_git(b, "push", "-q", "origin", "HEAD:main")
+
+        # 1. accepted
+        fresh()
+        payload(a, '{"n":1}\n')
+        s.check("writer: accepted -> (True, True)", writer.publish(a) == (True, True))
+        s.check("writer: accepted -> remote main is the clone's HEAD", _v_head(remote, "main") == _v_head(a))
+        s.check("writer: the commit message is COMMIT_MESSAGE",
+                _v_git(remote, "log", "-1", "--format=%s", "main").stdout.strip() == writer.COMMIT_MESSAGE)
+        # 2. rejected once, rebased, pushed
+        fresh()
+        other_writer("other.txt", "x\n")
+        payload(a, '{"n":2}\n')
+        s.check("writer: one rejection -> rebase -> (True, True)", writer.publish(a) == (True, True))
+        s.check("writer: after the rebase remote main carries both commits",
+                _v_git(remote, "log", "--format=%s", "-2", "main").stdout.split("\n")[:2]
+                == [writer.COMMIT_MESSAGE, "other"])
+        # 3. a rebase that conflicts drops the commit
+        fresh()
+        base = _v_head(a)
+        other_writer(writer.PAYLOAD, '{"other":3}\n')
+        theirs = _v_head(remote, "main")
+        payload(a, '{"n":3}\n')
+        s.check("writer: a conflicting rebase -> (True, False)", writer.publish(a) == (True, False))
+        s.check("writer: the clone is back at its base", _v_head(a) == base)
+        s.check("writer: remote main is the other writer's", _v_head(remote, "main") == theirs)
+        s.check("writer: no rebase is left in progress",
+                not os.path.exists(os.path.join(a, ".git", "rebase-merge"))
+                and not os.path.exists(os.path.join(a, ".git", "rebase-apply")))
+        # 4. a second rejection drops the commit
+        fresh()
+        base = _v_head(a)
+        with open(reject, "w", encoding="utf-8") as fh:
+            fh.write("1")
+        payload(a, '{"n":4}\n')
+        s.check("writer: two rejections -> (True, False)", writer.publish(a) == (True, False))
+        s.check("writer: two rejections leave the clone at its base", _v_head(a) == base)
+        os.unlink(reject)
+        # 5. nothing to commit
+        fresh()
+        s.check("writer: nothing changed -> (False, False)", writer.publish(a) == (False, False))
+        s.check("writer: nothing changed leaves the tree clean", _v_git(a, "status", "--porcelain").stdout == "")
+        # 6. new, untracked files
+        fresh()
+        os.makedirs(os.path.join(a, "analyst", "paper", "book"))
+        rels = ["analyst/paper/x.json", "analyst/paper/book/2026-01-01.jsonl"]
+        for rel in rels:
+            with open(os.path.join(a, rel), "w", encoding="utf-8") as fh:
+                fh.write(rel + "\n")
+        s.check("new files -> (True, True)", common.publish(a, rels, "paper: x") == (True, True))
+        s.check("new files: both on remote main",
+                _v_git(remote, "ls-tree", "-r", "--name-only", "main").stdout.split() ==
+                sorted(["analyst/live.json", "other.txt"] + rels))
+        s.check("new files: the message is the one given",
+                _v_git(remote, "log", "-1", "--format=%s", "main").stdout.strip() == "paper: x")
+    finally:
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
+# --- W: the paper test (TZ-64) -----------------------------------------------------------
+W_T0 = paper.day_start("2026-01-07")
+W_SYMBOLS = {"BTCUSDT", "1000PEPEUSDT", "KAITOUSDT", "ETHUSDT"}
+
+
+def w_portfolio(rets, values=None, turnover=1.0, month_value=100000.0):
+    """A portfolio answer: perpAllTime with a point at every grid instant (and one wild point off the
+    grid, which no grid instant may read), perpMonth over exactly 30 days at month_value."""
+    grid = [W_T0 - (52 - j) * paper.WEEK_MS for j in range(53)]
+    vals = values or [100000.0] * 53
+    pnl = [0.0]
+    for j, r in enumerate(rets):
+        pnl.append(pnl[-1] + r * vals[j])
+    av = [[g, repr(v)] for g, v in zip(grid, vals)] + [[grid[10] + 3 * paper.DAY_MS, "1.0"]]
+    pn = [[g, repr(p)] for g, p in zip(grid, pnl)] + [[grid[10] + 3 * paper.DAY_MS, "-999999.0"]]
+    month = [[W_T0 - 30 * paper.DAY_MS, repr(month_value)], [W_T0, repr(month_value)]]
+    return [["perpAllTime", {"accountValueHistory": av[::-1], "pnlHistory": pn[::-1], "vlm": "1"}],
+            ["perpMonth", {"accountValueHistory": month, "pnlHistory": month,
+                           "vlm": repr(turnover * month_value * 30)}]]
+
+
+def w_fill(t, start, side, sz, coin="BTC", px="100", tid=None):
+    return {"coin": coin, "px": px, "sz": str(sz), "side": side, "time": t, "startPosition": str(start),
+            "tid": tid if tid is not None else t}
+
+
+W_LEADERBOARD = ('{"leaderboardRows": [{"ethAddress": "0xAA", "accountValue": "1", "windowPerformances": '
+                 '[["day", {"vlm": "1"}], ["allTime", {"pnl": "0", "vlm": "300000000"}]], '
+                 '"displayName": "a}{\\"],\\u0416 \u0416"}, \n {"ethAddress": "0xbb", "windowPerformances": '
+                 '[["allTime", {"vlm": "199999999.99"}]], "displayName": null}, {"ethAddress": "0xcc"}, '
+                 '{"ethAddress": "0xDd", "windowPerformances": [["allTime", {"vlm": "200000000"}]]}]}')
+
+
+def w_kl(t, prices, missing=()):
+    """Minute rows from t - 10 min to t + 6 h; prices(m) -> (o, h, l, c)."""
+    times = [m for m in range(t - 600000, t + 6 * 3600000 + 60000, 60000) if m not in missing]
+    return times, [prices(m) for m in times]
+
+
+def section_w(s):
+    near = lambda x, y: x is not None and y is not None and abs(x - y) <= 1e-9 * max(1.0, abs(y))  # noqa: E731
+    # W1. the leaderboard, one row at a time, on every chunking
+    blob = W_LEADERBOARD.encode("utf-8")
+    for size in (1, 7, 64, len(blob)):
+        chunks = [blob[i:i + size] for i in range(0, len(blob), size)]
+        s.check("pool_of(iter_rows(chunks of %d)) == (['0xaa', '0xdd'], 4, 1)" % size,
+                paper.pool_of(paper.iter_rows(chunks)) == (["0xaa", "0xdd"], 4, 1))
+    try:
+        list(paper.iter_rows([blob[:-40]]))
+        truncated = False
+    except ValueError:
+        truncated = True
+    s.check("a truncated document raises ValueError", truncated)
+    # W2. the twelve-month record
+    worlds = {
+        "A": w_portfolio([0.02, 0.0] * 26),
+        "B": w_portfolio([0.03, -0.01] * 26),
+        "C": w_portfolio([-0.01] * 16 + [0.02, 0.0] * 18),
+        "D": w_portfolio([0.02] * 9 + [-0.30] + [0.02] * 42),
+        "E": w_portfolio([0.02, 0.0] * 26, values=[100000.0] * 5 + [9000.0] + [100000.0] * 47),
+        "F": w_portfolio([0.02, 0.0] * 26, values=[100000.0] * 52 + [40000.0]),
+        "G": w_portfolio([0.02, 0.0] * 26, turnover=11.0),
+        "H": w_portfolio([0.02, 0.0] * 26, turnover=10.0),
+    }
+    m = {k: paper.metrics(v, W_T0) for k, v in worlds.items()}
+    s.check("A: eligible, passes, 13 blocks, drawdown 0, Sharpe 1.0",
+            m["A"]["eligible"] and m["A"]["r12"] and m["A"]["blocks"] == 13 and m["A"]["drawdown"] == 0.0
+            and near(m["A"]["sharpe"], 1.0))
+    s.check("B: passes, 13 blocks, drawdown 0.01, Sharpe 0.5",
+            m["B"]["r12"] and m["B"]["blocks"] == 13 and near(m["B"]["drawdown"], 0.01) and near(m["B"]["sharpe"], 0.5))
+    s.check("C: eligible, 9 blocks, fails", m["C"]["eligible"] and m["C"]["blocks"] == 9 and not m["C"]["r12"])
+    s.check("D: eligible, drawdown 0.30, fails", m["D"]["eligible"] and near(m["D"]["drawdown"], 0.30)
+            and not m["D"]["r12"])
+    s.check("E: a week at 9 000 is ineligible", not m["E"]["eligible"] and not m["E"]["r12"])
+    s.check("F: 40 000 at T0 is ineligible", not m["F"]["eligible"] and m["F"]["value_t0"] == 40000.0)
+    s.check("G: turnover 11 is ineligible", not m["G"]["eligible"] and near(m["G"]["turnover"], 11.0))
+    s.check("H: turnover 10 is eligible", m["H"]["eligible"] and near(m["H"]["turnover"], 10.0))
+    s.check("step_at reads the last point at or before t",
+            paper.step_at([(1, 10.0), (5, 50.0)], 4) == 10.0 and paper.step_at([(1, 10.0), (5, 50.0)], 5) == 50.0
+            and paper.step_at([(1, 10.0)], 0) is None)
+    s.check("ranking: A before B", sorted(("B", "A"), key=lambda k: -m[k]["sharpe"]) == ["A", "B"])
+    # W3. the Binance symbol
+    cases = (("BTC", "BTCUSDT"), ("kPEPE", "1000PEPEUSDT"), ("KAITO", "KAITOUSDT"), ("xyz:CL", None),
+             ("PURR/USDC", None), ("@151", None), ("SOL", None))
+    for coin, want in cases:
+        s.check("symbol_for(%r) == %r" % (coin, want), paper.symbol_for(coin, W_SYMBOLS) == want)
+    s.check("symbol_for('kPEPE') is None without 1000PEPEUSDT", paper.symbol_for("kPEPE", {"PEPEUSDT"}) is None)
+    # W4. episodes from fills
+    coins, seq = {}, []
+    fills = [w_fill(1, 5, "A", 5), w_fill(2, 0, "B", 1), w_fill(3, 1, "B", 1), w_fill(4, 2, "A", 1),
+             w_fill(5, 1, "A", 3, px="101"), w_fill(6, -2, "B", 2, px="99"), w_fill(7, 0, "B", 1), w_fill(8, -1, "B", 1)]
+    for f in fills:
+        seq.append(paper.apply_fill(coins, f, "BTCUSDT"))
+    kinds = [[k for k, _ in ev] for ev in seq]
+    s.check("event kinds: [], open, [], [], close+open, close, open, lost",
+            kinds == [[], ["open"], [], [], ["close", "open"], ["close"], ["open"], ["lost"]])
+    long_ep, short_ep = seq[4][0][1], seq[5][0][1]
+    s.check("the long: side 1, opened at 2, closed at 5 at 101 after 4 fills",
+            (long_ep["side"], long_ep["t_open"], long_ep["t_close"], long_ep["px_close"], long_ep["n"]) == (1, 2, 5, "101", 4))
+    s.check("the short: side -1, opened at 5, closed at 6 at 99 after 2 fills",
+            (short_ep["side"], short_ep["t_open"], short_ep["t_close"], short_ep["px_close"], short_ep["n"]) == (-1, 5, 6, "99", 2))
+    s.check("a lost episode leaves the coin flat", coins["BTC"] is None)
+    # W5. copyability
+    w0, h = W_T0 - 91 * paper.DAY_MS, 3600000
+    base = [w_fill(w0 + h, 0, "B", 10), w_fill(w0 + 4 * h, 10, "A", 10), w_fill(w0 + 5 * h, 0, "A", 10),
+            w_fill(w0 + 6 * h, -10, "B", 10), w_fill(w0 + 7 * h, 0, "B", 1, coin="PURR/USDC", px="100000"),
+            w_fill(W_T0, 0, "B", 1000, coin="xyz:CL")]
+    c = paper.copyability(base + [w_fill(w0 + 8 * h, 0, "B", 10, coin="xyz:CL")], W_SYMBOLS, w0, W_T0)
+    s.check("share 0.8 exactly and median 2 h: copyable", c["copyable"] and near(c["share"], 0.8)
+            and c["median_episode_s"] == 7200 and c["closed_episodes"] == 2)
+    c = paper.copyability(base + [w_fill(w0 + 8 * h, 0, "B", 10, coin="xyz:CL", px="100.0001")], W_SYMBOLS, w0, W_T0)
+    s.check("share just under 0.8: not copyable", not c["copyable"] and c["share"] < 0.8)
+    short_close = [dict(f) for f in base]
+    short_close[3]["time"] = w0 + 5 * h + 59 * 60000
+    c = paper.copyability(short_close + [w_fill(w0 + 8 * h, 0, "B", 10, coin="xyz:CL")], W_SYMBOLS, w0, W_T0)
+    s.check("median 1 h 59.5 min: not copyable", not c["copyable"] and c["median_episode_s"] == 7170)
+    # W5b. fills, page by page
+    saved_info = paper.info
+
+    def pages(body, limiter):
+        t = body["startTime"]
+        if body["user"] == "stuck":
+            return [{"coin": "BTC", "px": "1", "sz": "1", "side": "B", "time": 5, "startPosition": "0", "tid": i,
+                     "extra": 0} for i in range(paper.FILLS_PAGE)]
+        last = min(t + paper.FILLS_PAGE, 4000)
+        return [{"coin": "BTC", "px": "1", "sz": "1", "side": "B", "time": m, "startPosition": "0", "tid": m,
+                 "extra": 0} for m in range(t, last)]
+
+    try:
+        paper.info = pages
+        got = paper.fills_since("a", 1, None)
+        s.check("pages of 2 000 repeating their boundary: each fill once, ascending, 3 999 in all",
+                [f["tid"] for f in got] == list(range(1, 4000)))
+        s.check("a fill keeps only FILL_KEYS", set(got[0]) == set(paper.FILL_KEYS))
+        try:
+            paper.fills_since("stuck", 5, None)
+            stuck = False
+        except ValueError:
+            stuck = True
+        s.check("a full page inside one millisecond raises ValueError", stuck)
+    finally:
+        paper.info = saved_info
+    # W6. the null's order
+    addrs = ["0x%040x" % i for i in range(20)]
+    order = paper.null_order(W_T0, addrs)
+    s.check("null_order is a permutation, independent of input order",
+            sorted(order) == sorted(addrs) and paper.null_order(W_T0, addrs[::-1]) == order)
+    s.check("null_order moves with T0", paper.null_order(W_T0 + paper.DAY_MS, addrs) != order)
+    # W7. booking
+    t = paper.day_start("2026-01-05") + 10 * h
+    rise = w_kl(t, lambda mm: (100.0,) * 4 if mm < t + h else (110.0,) * 4)
+    ep = {"side": 1, "t_open": t + 30000, "t_close": t + 3 * h + 30000}
+    b = paper.book_delay(ep, 5, 0.04, rise, 10000.0, 0.005, 0.0005, t + 10 * h)
+    s.check("rise, 5 s: entry minute t at 100, qty 12.5, exit t + 3 h at 110, gross 125, fee 1.3125",
+            b["entry_ms"] == t and b["entry_px"] == 100.0 and near(b["qty"], 12.5) and b["src"]["exit_ms"] == t + 3 * h
+            and b["src"]["px"] == 110.0 and near(b["src"]["gross"], 125.0) and near(b["src"]["fee"], 1.3125))
+    s.check("rise, 5 s: not stopped, the stop variant equals the source", not b["stopped"] and b["stop"] == b["src"])
+    b = paper.book_delay(ep, 7200, 0.04, rise, 10000.0, 0.005, 0.0005, t + 10 * h)
+    s.check("rise, 7 200 s: entry t + 2 h at 110, exit t + 5 h, gross 0, fee 1.25",
+            b["entry_ms"] == t + 2 * h and b["entry_px"] == 110.0 and b["src"]["exit_ms"] == t + 5 * h
+            and near(b["src"]["gross"], 0.0) and near(b["src"]["fee"], 1.25))
+    dip = w_kl(t, lambda mm: (97.0, 97.0, 95.5, 96.5) if mm == t + 30 * 60000 else (100.0,) * 4)
+    b = paper.book_delay(ep, 5, 0.04, dip, 10000.0, 0.005, 0.0005, t + 10 * h)
+    s.check("dip: stopped at t + 30 min at 96, gross -50 (the risk), fee 1.225",
+            b["stopped"] and b["stop"]["exit_ms"] == t + 30 * 60000 and b["stop"]["px"] == 96.0
+            and near(b["stop"]["gross"], -50.0) and near(b["stop"]["fee"], 1.225))
+    s.check("dip: the source variant holds to t + 3 h at 100, gross 0", b["src"]["px"] == 100.0
+            and near(b["src"]["gross"], 0.0))
+    b = paper.book_delay(dict(ep, t_close=t + 30 * 60000 + 10000), 5, 0.04, dip, 10000.0, 0.005, 0.0005, t + 10 * h)
+    s.check("dip in the exit minute: the stop variant leaves at 96, the source at that minute's close 96.5",
+            b["stopped"] and b["stop"]["px"] == 96.0 and b["src"]["exit_ms"] == t + 30 * 60000 and b["src"]["px"] == 96.5)
+    gap = w_kl(t, lambda mm: (95.0, 95.0, 94.0, 94.5) if mm == t + 30 * 60000 else (100.0,) * 4)
+    b = paper.book_delay(ep, 5, 0.04, gap, 10000.0, 0.005, 0.0005, t + 10 * h)
+    s.check("gap: exits at the open 95, gross -62.5", b["stop"]["px"] == 95.0 and near(b["stop"]["gross"], -62.5))
+    spike = w_kl(t, lambda mm: (103.0, 104.5, 103.0, 104.0) if mm == t + 30 * 60000 else (100.0,) * 4)
+    b = paper.book_delay(dict(ep, side=-1), 5, 0.04, spike, 10000.0, 0.005, 0.0005, t + 10 * h)
+    s.check("short spike: stopped at 104, gross -50", b["stopped"] and b["stop"]["px"] == 104.0
+            and near(b["stop"]["gross"], -50.0))
+    hole = w_kl(t, lambda mm: (100.0,) * 4 if mm < t + h else (110.0,) * 4, missing=(t,))
+    b = paper.book_delay(ep, 5, 0.04, hole, 10000.0, 0.005, 0.0005, t + 10 * h)
+    s.check("a missing entry minute: nominal entry t, the previous close", b["entry_ms"] == t and b["entry_px"] == 100.0)
+    cut = {"side": 1, "t_open": t + 4 * h, "t_close": None, "cut": True}
+    s.check("cut, 7 200 s past the window's end: None",
+            paper.book_delay(cut, 7200, 0.04, rise, 10000.0, 0.005, 0.0005, t + 5 * h) is None)
+    b = paper.book_delay(cut, 5, 0.04, rise, 10000.0, 0.005, 0.0005, t + 5 * h + 30000)
+    s.check("cut, 5 s: exits at the window end's minute", b["src"]["exit_ms"] == t + 5 * h)
+    b = paper.book_delay({"side": 1, "t_open": t + 10000, "t_close": t + 20000}, 5, 0.04, rise, 10000.0, 0.005, 0.0005,
+                         t + 10 * h)
+    s.check("an episode inside one minute: gross 0, fee 1.25", near(b["src"]["gross"], 0.0) and near(b["src"]["fee"], 1.25))
+    # W8. funding
+    rates = [(t + h, 0.0001), (t + 3 * h, 0.0002), (t + 9 * h, 0.5)]
+    s.check("funding: two events, long pays 0.375",
+            near(paper.funding_paid(1, 12.5, 100.0, t + 60000, t + 3 * h + 60000, rates), 0.375))
+    s.check("funding: the short receives 0.375",
+            near(paper.funding_paid(-1, 12.5, 100.0, t + 60000, t + 3 * h + 60000, rates), -0.375))
+    s.check("funding: an event at hold_from is excluded, one at hold_to included",
+            near(paper.funding_paid(1, 12.5, 100.0, t + h, t + 3 * h, rates), 0.25))
+    # W9. sigma
+    closes = [100.0]
+    for i in range(30):
+        closes.append(closes[-1] * (1.02 if i % 2 == 0 else 0.98))
+    s.check("daily_sigma of alternating +-2 %: 0.02", near(paper.daily_sigma(closes), 0.02))
+    # W10. the verdict rule
+    picks, null10 = ["p1", "p2", "p3"], ["n%d" % i for i in range(10)]
+
+    def res(values):
+        return {a: {d: {"src": v, "stop": v} for d in paper.DELAYS_S} for a, v in values.items()}
+
+    r = res(dict({a: 0.02 for a in picks}, **{a: 0.01 for a in null10}))
+    v = paper.decide(picks, null10, r, 30)
+    s.check("picks 0.02, null 0.01, 30 episodes: readable and passed", v["readable"] and v["passed"])
+    s.check("120 subsets, share at or above TOP 0", v["cells"]["1800/stop"]["null_share_at_or_above"] == 0.0
+            and near(v["cells"]["1800/stop"]["null_median"], 0.01))
+    v = paper.decide(picks, null10, res(dict({a: -0.01 for a in picks}, **{a: -0.02 for a in null10})), 30)
+    s.check("picks negative: readable, not passed", v["readable"] and not v["passed"])
+    v = paper.decide(picks, null10, res(dict({a: 0.02 for a in picks}, **{a: 0.03 for a in null10})), 30)
+    s.check("picks under the null: not passed, share 1.0", not v["passed"]
+            and v["cells"]["7200/stop"]["null_share_at_or_above"] == 1.0)
+    s.check("29 episodes: unreadable", not paper.decide(picks, null10, r, 29)["readable"])
+    s.check("nine null accounts: unreadable", not paper.decide(picks, null10[:9], r, 30)["readable"])
+    mixed = res(dict({a: 0.02 for a in picks}, **{a: 0.01 for a in null10}))
+    for a in picks:
+        mixed[a][7200]["stop"] = -0.01
+    s.check("passing at 1 800 s and failing at 7 200 s: not passed", not paper.decide(picks, null10, mixed, 30)["passed"])
+    s.check("starts: one pick and ten null accounts", paper.starts({"picks": picks[:1], "null": null10}))
+    s.check("starts: not with nine null accounts or no pick",
+            not paper.starts({"picks": picks, "null": null10[:9]}) and not paper.starts({"picks": [], "null": null10}))
+    saved_wait, calls = paper.TRANSPORT_WAIT_S, []
+
+    def flaky(n):
+        calls.append(1)
+        if len(calls) <= n:
+            raise paper.Transport("HTTP 429")
+        return "answer"
+
+    try:
+        paper.TRANSPORT_WAIT_S = 0
+        with contextlib.redirect_stdout(io.StringIO()):
+            s.check("retrying: an answer after two transport failures", paper.retrying(flaky, 2) == "answer")
+            del calls[:]
+            given = paper.retrying(flaky, 10 ** 6, give_up=True)
+            s.check("retrying: one account is given up after TRANSPORT_MAX failures, None",
+                    given is None and len(calls) == paper.TRANSPORT_MAX)
+            try:
+                paper.retrying(flaky, 10 ** 6)
+                code = None
+            except SystemExit as exc:
+                code = exc.code
+            s.check("retrying: a step the selection needs ends the process with 4", code == 4)
+    finally:
+        paper.TRANSPORT_WAIT_S = saved_wait
+    s.check("nearest_rank: median 3, p95 5 of 1..5",
+            paper.nearest_rank([5, 1, 3, 2, 4], 0.5) == 3 and paper.nearest_rank([5, 1, 3, 2, 4], 0.95) == 5)
+    # W11. the alert texts
+    rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
+    t_open = int(datetime(2026, 10, 16, 10, 5, tzinfo=timezone.utc).timestamp() * 1000)
+    ep = {"a": "0xf97ad6704baec104d00b88e0c157e2b7b3a1ddd1", "coin": "HYPE", "symbol": "HYPEUSDT", "side": 1,
+          "t_open": t_open, "px_open": "80.021"}
+    head = ("\U0001f4cb \u0411\u0443\u043c\u0430\u0436\u043d\u044b\u0439 \u0442\u0435\u0441\u0442 \u00b7 14:05 "
+            "\u0422\u0431\u0438\u043b\u0438\u0441\u0438 \u00b7 \u0441\u0447\u0451\u0442 #1 0xf97a\u2026ddd1 ")
+    s.check("the open alert, character for character", paper.alert_open(ep, 1, rule, 0.02) == head + (
+        "\u043e\u0442\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 80.021 \u00b7 \u0441\u0442\u043e\u043f 4.0% "
+        "\u2192 76.820 \u00b7 \u043e\u0431\u044a\u0451\u043c 1250 USDT \u043f\u0440\u0438 \u0440\u0438\u0441\u043a"
+        "\u0435 0.5% \u043a\u0430\u043f\u0438\u0442\u0430\u043b\u0430"))
+    s.check("the open alert without a sigma", paper.alert_open(ep, 1, rule, None) == head + (
+        "\u043e\u0442\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 80.021 \u00b7 \u0441\u0442\u043e\u043f \u0438 "
+        "\u043e\u0431\u044a\u0451\u043c \u043d\u0435 \u0440\u0430\u0441\u0441\u0447\u0438\u0442\u0430\u043d\u044b: "
+        "\u043d\u0435\u0442 \u0434\u043d\u0435\u0432\u043d\u044b\u0445 \u0441\u0432\u0435\u0447\u0435\u0439 Binance"))
+    closed = dict(ep, t_close=t_open + (6 * 60 + 12) * 60000, px_close="82.10")
+    s.check("the close alert after 6 h 12 min", paper.alert_close(closed, 1) == head.replace("14:05", "20:17") + (
+        "\u0437\u0430\u043a\u0440\u044b\u043b LONG HYPEUSDT \u043f\u043e 82.10 \u00b7 \u0432 \u043f\u043e\u0437"
+        "\u0438\u0446\u0438\u0438 6.2 \u0447"))
+    s.check("held 45 min", paper.held_text(45 * 60000) == "45 \u043c\u0438\u043d")
+    # W12. the constants cut from index.html
+    page = "var INV_FLOOR_SD = 2.0;   // x\nvar FEE_TAKER   = 0.0005;\n"
+    s.check("cut_number on a page", common.cut_number(page, "INV_FLOOR_SD") == 2.0
+            and common.cut_number(page, "FEE_TAKER") == 0.0005)
+    for bad, label in ((page + "var FEE_TAKER = 0.001;\n", "twice"), ("var X = 1;\n", "absent")):
+        try:
+            common.cut_number(bad, "FEE_TAKER")
+            raised = False
+        except ValueError:
+            raised = True
+        s.check("cut_number raises on a constant defined %s" % label, raised)
+    rule_live = paper.load_rule(REPO)
+    with open(os.path.join(REPO, "analyst", "owner.json"), encoding="utf-8") as fh:
+        owner = json.load(fh)
+    s.check("load_rule reads owner.json's capital and medium risk",
+            rule_live["capital_usdt"] == float(owner["capital"]["usdt"])
+            and rule_live["risk_pct"] == float(owner["risk"]["risk_pct_medium"]))
+    s.check("load_rule cuts two positive numbers from index.html",
+            rule_live["inv_floor_sd"] > 0 and 0 < rule_live["fee_taker"] < 0.01)
+    # W13. the unit and the manifest
+    unit_path = os.path.join(HERE, "units", "crypto-paper.service")
+    with open(unit_path, encoding="utf-8") as fh:
+        lines = [line.rstrip("\n") for line in fh]
+    creds = [line for line in lines if line.startswith("LoadCredential=")]
+    s.check("crypto-paper.service runs as cryptopaper", "User=cryptopaper" in lines and "Group=cryptopaper" in lines)
+    s.check("crypto-paper.service loads exactly the deploy key",
+            creds == ["LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key"])
+    s.check("crypto-paper.service runs paper.py from the deployer's clone, MemoryMax=128M",
+            "ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/paper.py" in lines and "MemoryMax=128M" in lines)
+    with open(os.path.join(HERE, "manifest"), encoding="utf-8") as fh:
+        listed = [line.strip() for line in fh if line.strip() and not line.startswith("#")]
+    s.check("the manifest lists crypto-paper.service once", listed.count("crypto-paper.service") == 1)
+    with open(os.path.join(HERE, "units", "crypto-run.service"), encoding="utf-8") as fh:
+        run_creds = [line.strip() for line in fh if line.startswith("LoadCredential=")]
+    s.check("crypto-run.service still loads exactly its login and the deploy key", run_creds == [
+        "LoadCredential=claude-oauth-token:/etc/crypto-auto/credentials/claude-oauth-token",
+        "LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key"])
+    # W14. the flow, offline: polls, the cut, three days of episodes, books, funding and the verdict
+    section_w_flow(s)
+
+
+def w_rows(path):
+    """Synthetic data.binance.vision rows: 1m at a flat 100, daily closes alternating +-2 %, funding 0.0001 / 8 h."""
+    name = path.rsplit("/", 1)[1][:-4]
+    date = name.rsplit("-", 3)[-3:] if "-1m-" in name or "-1d-" in name else None
+    if "-1m-" in name:
+        start = paper.day_start("-".join(date))
+        return [[str(m), "100", "100", "100", "100"] for m in range(start, start + paper.DAY_MS, 60000)]
+    if "-1d-" in name:
+        k = (paper.day_start("-".join(date)) // paper.DAY_MS) % 2
+        return [[str(paper.day_start("-".join(date))), "0", "0", "0", "102" if k else "100"]]
+    month = name.rsplit("-", 2)[-2:]
+    start = paper.day_start("-".join(month) + "-01")
+    return [[str(m), "8", "0.0001"] for m in range(start, start + 28 * paper.DAY_MS, 8 * 3600000)]
+
+
+def section_w_flow(s):
+    tmp = tempfile.mkdtemp(prefix="vps-selftest-w.")
+    saved = common.OUTBOX_DIR
+    try:
+        outbox = os.path.join(tmp, "outbox")
+        os.makedirs(outbox)
+        common.OUTBOX_DIR = outbox
+        p, n = "0x" + "a" * 40, "0x" + "b" * 40
+        ff = paper.day_start("2026-01-05") + 3600000
+        we = ff + 2 * paper.DAY_MS
+        sel = {"picks": [{"address": p, "rank": 1}], "null": [{"address": n}], "follow_from_ms": ff,
+               "window_end_ms": we, "follow_from": paper.iso(ff), "window_end": paper.iso(we), "symbols": ["BTCUSDT"]}
+        state = paper.new_state(sel)
+        rule = {"capital_usdt": 10000.0, "risk_pct": 0.5, "inv_floor_sd": 2.0, "fee_taker": 0.0005}
+        inputs = paper.Inputs(tmp, "2026-03-01", rows=w_rows)
+        h = 3600000
+        # (account, fill, seen after): the pick's short is seen 601 s late and raises no alert; the
+        # fill after the window's end is never applied.
+        flow = ((p, w_fill(ff + h, 0, "B", 1), 10000), (p, w_fill(ff + 3 * h, 1, "A", 1), 10000),
+                (n, w_fill(ff + 25 * h, 0, "B", 1), 10000), (n, w_fill(ff + 27 * h, 1, "A", 1), 10000),
+                (p, w_fill(ff + 33 * h, 0, "A", 1), 601000), (p, w_fill(we + h, -1, "B", 1), 10000))
+        for addr, f, late in flow:
+            paper._apply(addr, state["accounts"][addr], [f], sel, {"BTCUSDT"}, f["time"] + late, rule, lambda: inputs)
+        paper.gather_closed(state)
+        alerts = sorted(x for x in os.listdir(outbox) if "-alert-" in x)
+        s.check("two fresh alerts for the pick, none for the null, none late", len(alerts) == 2)
+        for acct in state["accounts"].values():
+            acct["polled_ms"] = we + paper.DAY_SETTLE_S * 1000
+        paper.produce_days(state, tmp, sel, we)
+        s.check("before the cut, the window's last day is not written", state["written"]["episodes"] == "2026-01-06")
+        paper.cut_open(state, sel)
+        paper.produce_days(state, tmp, sel, we)
+        root = os.path.join(tmp, "records", paper.RECORD_DIR)
+        days = ["2026-01-05", "2026-01-06", "2026-01-07"]
+        eps = {d: [e for e in paper.read_jsonl(os.path.join(root, "episodes", d + ".jsonl")) if e["k"] == "ep"]
+               for d in days}
+        s.check("day 1: the pick's long", [(e["a"], e["side"], e["cut"]) for e in eps[days[0]]] == [(p, 1, False)])
+        s.check("day 2: the null's long", [(e["a"], e["side"]) for e in eps[days[1]]] == [(n, 1)])
+        s.check("day 3: the pick's short, cut at the window end with no price",
+                [(e["a"], e["side"], e["cut"], e["t_close"], e["px_close"]) for e in eps[days[2]]] == [(p, -1, True, we, None)])
+        paper.produce_books(state, tmp, sel, rule, inputs)
+        paper.produce_funding(state, tmp, sel, inputs)
+        s.check("the verdict is written once", paper.produce_verdict(state, tmp, sel, rule)
+                and not paper.produce_verdict(state, tmp, sel, rule))
+        with open(os.path.join(root, "verdict.json"), encoding="utf-8") as fh:
+            verdict = json.load(fh)
+        s.check("the verdict: two pick episodes and one null episode booked at 1 800 s",
+                verdict["booked"]["1800"] == {"pick": 2, "null": 1})
+        s.check("the verdict: unreadable, not passed", verdict["readable"] is False and verdict["passed"] is False)
+        s.check("the verdict: on a flat price every cell is the fees and funding, negative",
+                all(c["top"] < 0 for c in verdict["cells"].values()))
+        s.check("ten records pending, each once", sorted(state["pending"]) == sorted(
+            ["episodes/%s.jsonl" % d for d in days] + ["book/%s.jsonl" % d for d in days]
+            + ["funding/%s.jsonl" % d for d in days] + ["verdict.json"]))
+        paper.produce_days(state, tmp, sel, we)
+        s.check("a second pass writes nothing", len(state["pending"]) == 10)
+    finally:
+        common.OUTBOX_DIR = saved
+        shutil.rmtree(tmp, ignore_errors=True)
+
+
 SECTIONS = (("A", section_a), ("B", section_b), ("C", section_c), ("D", section_d), ("E", section_e),
             ("F", section_f), ("G", section_g), ("H", section_h), ("I", section_i), ("J", section_j),
             ("K", section_k), ("L", section_l), ("M", section_m), ("N", section_n), ("O", section_o),
             ("P", section_p), ("Q", section_q), ("R", section_r), ("S", section_s),
-            ("T", section_t), ("U", section_u))
+            ("T", section_t), ("U", section_u), ("V", section_v), ("W", section_w))
 
 
 def main():
diff --git a/vps/units/crypto-paper.service b/vps/units/crypto-paper.service
new file mode 100644
index 0000000..473242f
--- /dev/null
+++ b/vps/units/crypto-paper.service
@@ -0,0 +1,30 @@
+[Unit]
+Description=Crypto assistant: copy-trading paper test
+Wants=network-online.target
+After=network-online.target
+
+[Service]
+Type=exec
+User=cryptopaper
+Group=cryptopaper
+SupplementaryGroups=cryptoauto
+WorkingDirectory=/var/lib/cryptopaper
+Environment=HOME=/var/lib/cryptopaper
+Environment=PYTHONDONTWRITEBYTECODE=1
+Environment="GIT_SSH_COMMAND=ssh -i %d/deploy-key -o IdentitiesOnly=yes -o UserKnownHostsFile=/var/lib/cryptopaper/.ssh/known_hosts"
+LoadCredential=deploy-key:/etc/crypto-auto/credentials/deploy-key
+ExecStart=/usr/bin/python3 /srv/crypto-auto/vps/paper.py
+Restart=always
+RestartSec=60
+NoNewPrivileges=yes
+CapabilityBoundingSet=
+ProtectSystem=strict
+ProtectHome=yes
+PrivateTmp=yes
+ReadWritePaths=/var/lib/cryptopaper /var/spool/crypto-auto/outbox
+MemoryAccounting=yes
+MemoryMax=128M
+Nice=5
+
+[Install]
+WantedBy=multi-user.target
diff --git a/vps/writer.py b/vps/writer.py
index 2aefa53..5fd4977 100644
--- a/vps/writer.py
+++ b/vps/writer.py
@@ -104,36 +104,17 @@ def run_gate(tree):
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
 
 
-def git(tree, *args):
-    return subprocess.run(["git", "-C", tree] + list(args),
-                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
-
-
-def git_out(tree, *args):
-    return subprocess.run(["git", "-C", tree] + list(args), capture_output=True, text=True).stdout.strip()
-
-
 def restore(tree):
-    git(tree, "checkout", "HEAD", "--", PAYLOAD)
+    common.git_quiet(tree, "checkout", "HEAD", "--", PAYLOAD)
 
 
 def publish(tree):
-    """Commit and push; one rejection → pull --rebase and push again; a rebase
-    conflict → abort it and drop the writer's commit. Returns (committed, pushed)."""
-    base = git_out(tree, "rev-parse", "HEAD")
-    if git(tree, "commit", "-q", "-m", COMMIT_MESSAGE, "--", PAYLOAD) != 0:
+    """Commit and push through common.publish (TZ-64: the one implementation); a commit that
+    fails restores the payload. Returns (committed, pushed)."""
+    committed, pushed = common.publish(tree, [PAYLOAD], COMMIT_MESSAGE)
+    if not committed:
         restore(tree)
-        return False, False
-    if git(tree, "push", "-q", "origin", "HEAD:main") == 0:
-        return True, True
-    if git(tree, "pull", "-q", "--rebase", "origin", "main") != 0:
-        git(tree, "rebase", "--abort")
-        git(tree, "reset", "-q", "--hard", base)
-        return True, False
-    if git(tree, "push", "-q", "origin", "HEAD:main") == 0:
-        return True, True
-    git(tree, "reset", "-q", "--hard", "HEAD~1")
-    return True, False
+    return committed, pushed
 
 
 def main(argv=None):
```
<!-- TZ-64 PATCH END -->
