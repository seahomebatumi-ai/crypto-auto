# TZ-85 — the card ledger from the minute the answer reached main: a card the owner could take, a resolved card read once, the exchange's refusal ending the pass

**Contract:** v33 — `EXECUTOR-INSTRUCTIONS.md` at the repository root, read in full before the sections below.
**Canonical filename:** `CryptoTZ/TZ-85-card-delivery.md`
**Report:** `CryptoReports/TZ-85-card-delivery-report.md`
**Class:** branch TZ (contract §8) — it authorises two repository files besides its report.
**Branch:** `claude/tz-85-card-delivery`
**Host:** the VPS — V4 and R1 exist only there.
**Model:** Sonnet 5.5 · medium — the code is §6's patch, written and run by the Architect; the session applies it, runs
the checks and takes two readings, and judges nothing.
**Base:** `main` at `216ac3c` with this delivery's uploads — the map `2026-11-26-d`; `vps/` as TZ-84's merge left it.
**Rests on:** map §10 row «Every card is a recommendation the record follows»; methodology §2's «Вход» rule and §12's
`CARD|` line; inv. 38, 55, 70 and 73.
**Previous TZ:** TZ-84, accepted 26.11.2026, merged at `216ac3c` (pull request #69).
**Trigger:** `EXECUTE TZ-85`, with nothing under it: no credential arrives and the Boss is asked for nothing.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-26-d.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-26-d.**` |
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
| `vps/score.py` | 834 | `d29c79d140616efaf19f25b0ae5c2dc2` | equal — §6's patch is written against these bytes |
| `vps/selftest.py` | 4384 | `9301f48be4d2c6fbf8a23617e9ab73bc` | equal — the same |

The map itself: 2782 lines, MD5 `becadb8f75e5b747dfe1732a149f46c7` — reported, not enforced.

---

## 1. Goal and scope

**The audit of TZ-84 found two defects in its own patch, both in the card ledger, `vps/score.py`.** The record the
trust line scores must hold only trades the owner could take, and it must not cost more every day it runs.

- **From the moment the answer reached him, never from the freeze.** The run of 26.11.2026 froze at 08:53:50Z; its
  day log reached `main` at 09:25:59Z. TZ-84 filled a `now` card at its frozen price and let a limit fill in those 32
  minutes — trades nobody could take. `delivered(stem)` reads the committer time of the commit that added
  `analyst/log/<stem>.md`, with git in the checkout the logs sit in, a clone another user owns (`install.sh`'s
  `own_git`). From the minute after it: a `now` card fills at that minute's open, and makes no trade where that price
  stands past its void price — `STOP_ATR / 2` atr20 inside its stop, the card's «не выше / не ниже» line (methodology
  §2), atr20 the book's on the days before the freeze day — or at or past its target; a `limit` card's window opens
  there, and a fill at or past its stop makes no trade; a `wait` card whose plan entry came before that minute makes
  none; an answer that reached `main` after its freeze day ended fills no `now` or `limit` card.
- **A resolved card is read once.** TZ-84 re-read every card's one-minute bars on every daily close, closed and
  lapsed alike: a cost without bound, on the address the paper test shares. A card that made no trade, or whose trade
  stands closed under an earlier card, is written once to `score-cards-done/<stem>-<rank>.json`; a card with a closed
  trade of its own or such a file is never read again, and a symbol whose every card is resolved is not read.
- **A 429 or a 418 from the exchange ends the card pass:** no further request; the cards not reached count unread.
- `score.json`'s `cards` block gains `done`, `finished` and `refused`.
- **Readings:** V4 — `delivered()` as the daily close's user, in its sandbox, on the deployer's clone; R1 — the card
  ledger as TZ-84 left it on the host.

### Files to Create
None — `score-cards-done/` is the daily close's to make.

### Files to Modify
`vps/score.py` and `vps/selftest.py`, by §6's patch and nothing else.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
A copy of the staged `vps/` at `/tmp/tz85-vps`, removed after V4; V4's one transient unit, `--wait --collect`; and reads
only: `ls` of `/var/lib/crypto-auto/score-cards/` and `/var/lib/crypto-auto/score-cards-done/`, `score.json`, and
`journalctl -u crypto-score.service`. No persistent unit, timer or service is started, enabled or installed (item 15):
the deployer installs the merge. No file under `/var/lib/crypto-auto/` is written or removed.

### Not touched
The methodology, the map, the contract, the kit, `analyst/**`, every other file of `vps/` — `book.py`, `run.py` and
`common.py` among them — the units, `index.html`, `main.py`, the benches and the workflows.

---

## 2. Gates fixed before the data

| # | Expectation | Derived from |
|---|---|---|
| G1 | Baseline: `selftest: sections 29 checks 842 failed 0 empty 0` | the Architect's run of `216ac3c` under Python 3.11, 3.12 and 3.13 |
| G2 | After it: `selftest: sections 30 checks 861 failed 0 empty 0` — `section AC: checks 30 failed 0`, `section AD: checks 18 failed 0` | the same run on the patched tree |
| G3 | V4 prints `1795685159000` and exits 0 | the committer time of `8e85d64`, the commit that added `analyst/log/2026-11-26.md`, read by `git log --diff-filter=A --format=%ct` on a fresh clone; and git 2.43, Ubuntu 24.04's, in the Architect's session: as a user that does not own a clone and has no home, git refuses it as «dubious ownership», and with `-c safe.directory=<clone>` prints that time, `score.delivered()` the same in ms |
| G4 | R1 registers nothing | a reading |

A V4 that prints anything else is stated with its log and does not stop the push: the code is right and the host is
the question, which the audit answers.

---

## 3. Run order

1. **`kit open TZ-85`.** Any FAIL is BLOCKED (contract §4a step 3).
2. **Baseline:** `kit log selftest-base -- python3 vps/selftest.py` — G1.
3. **`kit stage TZ-85`**, then V1–V3 (§4), then a commit with §7's message — local, not yet pushed.
4. **V4**, then **R1**, below.
5. Push; a pull request titled `TZ-85: vps — cards from the minute the answer reached main`, its body naming this TZ —
   or contract §8's fallback.
6. `kit usage TZ-85` and `kit units`; back on step 1's checkout (contract §4a step 7); the report; `kit close TZ-85`;
   the report to `main` by `git push origin HEAD:main`; `kit clean TZ-85`; the closing message.

**R1 — the card ledger as TZ-84 left it.** Three logs, the report carrying each in full:

```
kit log cards-files --sh -- 'ls -l /var/lib/crypto-auto/score-cards/ /var/lib/crypto-auto/score-cards-done/ 2>&1'
kit log cards-record -- python3 -I -c 'import json; d = json.load(open("/var/lib/crypto-auto/score.json")); print(d.get("asof"), json.dumps(d.get("cards"), sort_keys=True))'
kit log score-journal --tail 40 --sh -- 'journalctl -u crypto-score.service --since "2026-11-26 00:00" --no-pager -o short-iso'
```

A file under `score-cards/` was written under TZ-84's rule and stands (inv. 38): its card is resolved by its own stem
and rank, and the report names each such file.

---

## 4. Validation

- **V1.** `kit stage TZ-85` — PASS, the two files of §6's second table at their lines and SHA-256.
- **V2.** `kit log pycompile -- python3 -m py_compile vps/score.py vps/selftest.py` — exit 0.
- **V3.** `kit log selftest -- python3 vps/selftest.py` — exit 0, G2's last line and its sections AC and AD.
- **V4.** The daily close's user, in `crypto-score.service`'s sandbox, on the deployer's clone — G3. Three shell lines,
  run from the repository root as written:

  ```
  rm -rf /tmp/tz85-vps && cp -r vps /tmp/tz85-vps && chmod -R a+rX /tmp/tz85-vps
  kit log delivered-1126 -- systemd-run --wait --collect --pipe --quiet --unit=crypto-tz85-delivered -p User=cryptoauto -p Group=cryptoauto -p ProtectSystem=strict -p ProtectHome=yes -p NoNewPrivileges=yes -p Environment=PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -I -c 'import sys; sys.path.insert(0, "/tmp/tz85-vps"); import score; print(score.delivered("2026-11-26", "/srv/crypto-auto/analyst/log"))'
  rm -rf /tmp/tz85-vps
  ```

- **V5.** `kit units` — PASS: no transient unit left; `git status --porcelain --untracked-files=no` after the commit — 0
  lines.
- No CI step executes `vps/selftest.py`: the branch push runs `bench.yml`'s gate on paths this patch does not read, and
  `## CI Execution` states what ran and its conclusion (contract §9).

---

## 5. Parameters

`CARDS_DONE = "score-cards-done"`, a file `<stem>-<rank>.json` of `DONE_KEYS` — `stem`, `rank`, `symbol`, `side`,
`kind`, `why` (`lapsed` or `same`), `seen` — written once, never opened again · `REFUSED_CODES = (418, 429)` ·
`GIT_TIMEOUT_S = 30` · `delivered(stem)`: `git -c safe.directory=<checkout> -C <checkout> log --diff-filter=A
--format=%ct -- analyst/log/<stem>.md`, its last line, in ms; none raises, and the card stays pending · a `now` card's
void: `stop + side × STOP_ATR / 2 × book.atr(bars, k − 1)`, no trade where `side × (fill − void) < 0` —
`book.card_of()`'s own boundary — or `side × (target − fill) ≤ 0` · a `limit`: no trade where `side × (fill − stop) ≤
0` · the minutes from the minute after `max(delivered, freeze)` · a file of `score-cards-done/` that is not the card
its name says raises, and the card ledger's failure never stops the book's (`cards: null`).

---

## 6. Shipped

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CryptoTZ/TZ-85-card-delivery.patch` | 35531 | `b613f6ed545d1e960008b8ee421a8fe92ddcba5593b701128402af537e1bca04` | apply |

| Path | Lines | SHA-256 |
|---|---:|---|
| `vps/score.py` | 953 | `05a2f98a1627dbd54b604472716c17309ac16211f4d8abb7559545f1d42ebb3e` |
| `vps/selftest.py` | 4560 | `23a19ae93fa6c83f8ae0bc045a194165f83c8e30e7a2347fe8a11aa3b5528303` |

---

## 7. Commit Message

```
TZ-85: vps — the card ledger follows each card from the minute its answer reached main; a resolved card is read once; the exchange's refusal ends the pass
```

---

## 8. Pre-send checks

Run by the Architect before this file was sent:

- `kit caps` on this file — within 20 000 bytes.
- On a fresh clone of `main` at `216ac3c` with this delivery's uploads committed to a local origin: `kit open TZ-85`
  PASS, `kit stage TZ-85` PASS, and G1–G2 measured under Python 3.11, 3.12 and 3.13.
- Eight mutations of the patched `vps/score.py`, each run against the new section AD — the void boundary, the fill at
  the freeze, a `wait` entry before delivery, a limit past its stop, no `same` file, a 429 ignored, no resolved set,
  the newest commit for the adding one — each turned section AD red.
- G3's derivation, above, on git 2.43.
- `kit grow` on the map against the file it replaces — PASS.
