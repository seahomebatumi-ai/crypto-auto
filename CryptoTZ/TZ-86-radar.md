# TZ-86 — the radar: the list coins' own publications and the unlock index, twice a day, without the button

**Contract:** v33 — `EXECUTOR-INSTRUCTIONS.md` at the repository root, read in full before the sections below.
**Canonical filename:** `CryptoTZ/TZ-86-radar.md`
**Report:** `CryptoReports/TZ-86-radar-report.md`
**Class:** branch TZ (contract §8) — it authorises five repository files besides its report.
**Branch:** `claude/tz-86-radar`
**Host:** the VPS — R1 exists only there.
**Model:** Sonnet 5.5 · medium — the code is §6's patch, written and run by the Architect; the session applies it, runs
the checks and takes one reading, and judges nothing.
**Base:** `main` at `e96c1cd` with this delivery's uploads — the map `2026-11-26-e`; `vps/` as TZ-85's merge left it.
**Rests on:** map §10 row «The hunter has no pre-run radar»; methodology §6a's channel table, record list and unlock
lane, §16's STRONG sweep and §4's cards; contract §7 items 6, 9 and 15; inv. 21, 22, 38, 55 and 73.
**Previous TZ:** TZ-85, accepted 26.11.2026, merged at `e96c1cd` (pull request #70).
**Trigger:** `EXECUTE TZ-86`, with nothing under it: no credential arrives and the Boss is asked for nothing.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-26-e.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-26-e.**` |
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
| `vps/selftest.py` | 4560 | `2568459da91ffd1090f591a2c5528cd1` | equal — §6's patch is written against these bytes |
| `vps/manifest` | 11 | `0a2518c1fc7fd989ef2dfd8aa770beef` | equal — the same |

The map itself: 2782 lines, MD5 `272226879a5ab8ff93c70674ad93630e` — reported, not enforced.

---

## 1. Goal and scope

**The owner's request of 18.11.2026, restated on 26.11.2026: a search that runs no model, twice a day, finds a coin's
catalyst — a collaboration above all — before he presses «Анализ рынка», and says of a coin already moving whether an
entry is still open.** `vps/radar.py`, under `crypto-radar.timer` at 08:00 and 20:00 Tbilisi:

- **Reads** every row of methodology §6a's channel table once, in the methodology's measured client — `curl -sS -L -m
  20`, the host's `robots.txt` read first (RFC 9309), the row's own landing host required, a host that refuses with
  403, 418, 429 or 451 asked nothing more that pass — and the unlock index once, row by row (§6a).
- **New** is a record the channel's previous page did not carry, dated after a day before that read; a channel's first
  read is its baseline and reports nothing.
- **One alert a pass**, through the outbox, where it found a release or a post of the protocol's own site whose title
  names a word of the STRONG sweep (§16 S) — each with the book's view of the coin at its last price, `book.card_of()`
  on `book.state_of()`, the function every card of the run comes from: a hold, whose late entry the archive refused; an
  entry open down to its void; the level a close must cross; or no entry — and a cliff at or above `UNLOCK_MATERIAL`
  inside the holding window, once a cliff. **A forum topic is recorded and never alerted:** a forum carries its
  participants' posts, not the protocol's own record (§6a). The alert starts no run.
- **Writes** `/var/lib/crypto-auto/radar.json`, the pass's whole record, and `radar-state.json`. The channel table,
  its sitemap words, `UNLOCK_MATERIAL`, the holding window, the sweep's words, the ids and the perpetuals are cut at
  run time from `ANALYST-INSTRUCTIONS.md`, `main.py` and `index.html` and typed nowhere in the program.
- `--probe` reads every lane once and writes nothing — R1.

**Left out, deliberately** (the map row): listings and delistings, which `vps/announce.py` and `vps/exchange.py` alert
as they happen; and open-interest, taker and funding anomalies, whose raw series carried no edge in either window of
the archive reading of 20.10.2026. **No run reads the record yet:** that is the methodology's next revision, written
against the record the host writes (inv. 55).

### Files to Create
`vps/radar.py`, `vps/units/crypto-radar.service` and `vps/units/crypto-radar.timer`, by §6's patch.

### Files to Modify
`vps/selftest.py` — section AE — and `vps/manifest` — `crypto-radar.timer` —, by §6's patch and nothing else.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
A copy of the staged `vps/` at `/run/tz86-vps`, removed after R1, and R1's one transient unit, `--wait --collect`. No
persistent unit, timer or service is started, enabled or installed (item 15): the deployer installs the merge. No file
under `/var/lib/crypto-auto/` or `/var/spool/crypto-auto/` is written or removed.

### Not touched
The methodology, the map, the contract, the kit, `analyst/**`, every other file of `vps/` — `book.py`, `score.py`,
`common.py`, `announce.py`, `exchange.py` and `install.sh` among them — `index.html`, `main.py`, the benches and the
workflows.

---

## 2. Gates fixed before the data

| # | Expectation | Derived from |
|---|---|---|
| G1 | Baseline: `selftest: sections 30 checks 861 failed 0 empty 0` | the Architect's run of `e96c1cd` under Python 3.11, 3.12 and 3.13 |
| G2 | After it: `selftest: sections 31 checks 914 failed 0 empty 0` — `section AE: checks 53 failed 0` | the same runs on the patched tree |
| G3 | R1 exits 0 under `MemoryMax=128M` and prints one `radar-probe:` line per channel row, the unlock line and the totals line | the Architect's session ran this code's `--probe` on this tree on 26.11.2026: 22 of 35 rows read, the eleven GitHub rows held behind one 403 of that session's egress, `solana.com` 429 and ALGO's `robots.txt` unreachable through its proxy; the index 200, 23 695 530 bytes, `next=5 no cliff=14 not covered=11`; its peak resident set 85 000 KiB under Python 3.12, and 1.5 times that rounded up to 16 MiB is 128 MiB — the ceiling rule of the map's row «The assistant's build sequence» |
| G4 | Which lanes answer the VPS registers nothing | a reading: each row's host and refusal, if any, is the lane's first measurement on that machine |

An R1 that exits otherwise is stated with its log and does not stop the push: the code is right and the host is the
question, which the audit answers.

---

## 3. Run order

1. **`kit open TZ-86`.** Any FAIL is BLOCKED (contract §4a step 3).
2. **Baseline:** `kit log selftest-base -- python3 vps/selftest.py` — G1.
3. **`kit stage TZ-86`**, then V1–V4 (§4), then a commit with §7's message — local, not yet pushed.
4. **R1**, below.
5. Push; a pull request titled `TZ-86: vps — the radar, publications and unlocks twice a day`, its body naming this
   TZ — or contract §8's fallback.
6. `kit usage TZ-86` and `kit units`; back on step 1's checkout (contract §4a step 7); the report; `kit close TZ-86`;
   the report to `main` by `git push origin HEAD:main`; `kit clean TZ-86`; the closing message.

**R1 — every lane once, as the service's user in its sandbox, on the deployer's clone.** Three shell lines, run from
the repository root as written; the report carries the log in full:

```
rm -rf /run/tz86-vps && cp -r vps /run/tz86-vps && chmod -R a+rX /run/tz86-vps
kit log radar-probe -- systemd-run --wait --collect --pipe --quiet --unit=crypto-tz86-probe -p User=cryptoauto -p Group=cryptoauto -p ProtectSystem=strict -p ProtectHome=yes -p PrivateTmp=yes -p NoNewPrivileges=yes -p MemoryMax=128M -p Environment=PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /run/tz86-vps/radar.py --probe --tree /srv/crypto-auto
rm -rf /run/tz86-vps
```

---

## 4. Validation

- **V1.** `kit stage TZ-86` — PASS, the five files of §6's second table at their lines and SHA-256.
- **V2.** `kit log pycompile -- python3 -m py_compile vps/radar.py vps/selftest.py` — exit 0.
- **V3.** `kit log selftest -- python3 vps/selftest.py` — exit 0, G2's last line and its section AE.
- **V4.** `kit log units-verify -- systemd-analyze verify vps/units/crypto-radar.service vps/units/crypto-radar.timer`
  — exit 0.
- **V5.** R1 — G3.
- **V6.** `kit units` — PASS: no transient unit left; `git status --porcelain --untracked-files=no` after the commit —
  0 lines.
- No CI step executes `vps/selftest.py`: the branch push runs `bench.yml`'s gate on paths this patch does not read, and
  `## CI Execution` states what ran and its conclusion (contract §9).

---

## 5. Parameters

`CHANNEL_S = 20` and `INDEX_S = 60` — §6a's two measured forms · `HOLD_CODES = (403, 418, 429, 451)` — §16's refusal
set · `SLACK_MS` = one day — a sitemap dates a record by its day · `ROBOTS_AGENT = "curl"`; a `robots.txt` answering
200 is parsed, another 4xx permits every path, a 5xx or no answer none · records: a forum's `topic_list.topics[]` by
`created_at`, a pinned topic excluded, its url `https://<host>/t/<slug>/<id>`; GitHub's releases by `published_at`, a
draft excluded; GitLab's by `released_at`; an RSS `channel/item` by `pubDate`; a sitemap's `urlset/url` by `lastmod`,
cut by §6a's words; a sitemap index refused · a kind: a word of the title beginning with a sweep word's stem — `ship`,
`ion` or `ing`, then a final `e`, removed · the unlock lane: §6a's `next`, `status` and `share`, a document no row of
which carries `gecko_id` and `unlockEvents` refused as `shape` · the view: `book.live_day()`, `book.state_of()` — the
rule's —, `book.card_of()` at the forming day's close · `radar.json`: `v`, `k` = `radar`, `ts`, `window`, `material`,
`kinds`, `channels`, `unlock`, `found` · `radar-state.json`: `channels` — per lane `d` and `seen`, twelve hex digits
of SHA-1 a record — and `alerted` — `<SYM>|<t>` until the cliff passes · exit 0 a lane read, 4 none, 2 the tree
unread · the timer `OnCalendar=*-*-* 04,16:00:00 UTC`, `Persistent=true`; the service as `crypto-etf.service`, with
the spool writable, no credential, `MemoryMax=128M` and `TimeoutStartSec=1800`.

---

## 6. Shipped

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CryptoTZ/TZ-86-radar.patch` | 63796 | `dc84a6ab4717969fa5f650e3d4006ecd79791e7015d88ae15e3f0459a192c65d` | apply |

| Path | Lines | SHA-256 |
|---|---:|---|
| `vps/radar.py` | 649 | `9ca7cf9eb95e66e07a3cd1ec921586f9fb52be6b35a47a746053a217fdcc3d4a` |
| `vps/selftest.py` | 4943 | `f364bfc8131f88db13c7e10c8ce759ff1d51c7401a82674b0f67713b3ee5342b` |
| `vps/units/crypto-radar.service` | 20 | `46913a5f745fc5f9a31e3bd94d617c7401e140d493ab31ce52ed4183111c74a7` |
| `vps/units/crypto-radar.timer` | 10 | `757a6a7cb8a50d14cbfd09c2a96554d017ddf5a65e029cdcff76b1183054c871` |
| `vps/manifest` | 12 | `faa4b3e87a51b4b210f3d353aad99eecd66d710269f4c2ce6b1519c353c71047` |

---

## 7. Commit Message

```
TZ-86: vps — the radar: the list coins' own publications and the unlock index twice a day, one alert a pass, the book's view on each positive record
```

---

## 8. Pre-send checks

Run by the Architect before this file was sent:

- `kit caps` on this file — within 20 000 bytes.
- On a fresh clone of `main` at `e96c1cd` with this delivery's uploads committed to a local origin: `kit open TZ-86`
  PASS, `kit stage TZ-86` PASS, and G1–G2 measured under Python 3.11, 3.12 and 3.13; `systemd-analyze verify` on the
  two units, exit 0.
- Fifteen mutations of the patched `vps/radar.py`, each run against section AE — the day's slack, robots on a 5xx, the
  landing host, the earliest cliff, the void's side, the stem, the cliff's single alert, the sitemap words, a pinned
  topic, the window, `UNLOCK_MATERIAL`, the baseline, a forum topic alerted, a held host asked again, a probe that
  writes — each turned section AE red.
- G3's derivation, above: `--probe` on this tree from the Architect's session; the unlock lane read row by row equal
  to the document read whole on the live index.
- `kit grow` on the map against the file it replaces — PASS.
