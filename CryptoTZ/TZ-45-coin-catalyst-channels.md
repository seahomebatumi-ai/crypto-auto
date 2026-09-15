# TZ-45 — Coin catalyst channels: establish one publication host per `tokens[]` member

**Canonical filename:** `TZ-45-coin-catalyst-channels.md` — commit to `CryptoTZ/` under
this name, never under the name the message carrying it used.

**Model: Opus.** Thirty coins, four candidate channel classes each, and one classification
judgement per host that decides whether a lane is usable. A wrong call is written into
`ANALYST-INSTRUCTIONS.md` as a named host and is then trusted by every later run.

**Report-only TZ.** No production file, no bench, no workflow, no `analyst/**` write, no
branch and no pull request. The deliverable is
`CryptoReports/TZ-45-coin-catalyst-channels-report.md`, pushed straight to `main` (§8, §4b).

---

## 0. System Map fingerprint — blocking

Required revision and anchors, from `## 0. Fingerprint` of `SYSTEM-MAP-CRYPTOCALCUL.md`.
Any mismatch → **ЗАБЛОКИРОВАНО** before any work, reported in one line.

**Revision `2026-09-14-a`.** Baseline: TZ-44 accepted and TZ-43 BLOCKED, both on `--verify`;
merged as pull request **#39**, implementation commit **`99e4b0a`**; no production file moved
at this revision, the sixth in a row.

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3799 | `4e71da9badca3ccae85b656fdc3773e8` |
| `main.py` | 518 | `0e3ead8c300d2ee6783303c4bf2fb6b5` |
| `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

Bench anchors: `bench/backtest_bench.py` **5102** lines `ba633202f43845ba0fdafbc1b92d9c04` ·
`bench/verify_bench.py` **540** lines `28eb1949f21d0afadb062303108f7101` ·
`bench/backtest_guard_bench.py` **2503** lines `bfc984b1d22ec1ad89cf536a1a47c529`.
Gate anchors: `bench.yml` **14 steps, 1 336 147 checks**; step 14 **487**, step 4 **59**,
step 7 (`journal_bench.js`) **774 130**.

**`index.html` was re-read by the Architect at 3799 lines and `4e71da9badca3ccae85b656fdc3773e8`
while writing this specification**, so that row is a reading and not an inheritance.

---

## 1. Why this exists

`ANALYST-INSTRUCTIONS.md` §6 now keys the class-A catalyst hunt to `tokens[]`: every coin
carries a horizon lane holding the channel its own protocol publishes on. **The rule exists
and the channels do not.** The run of 15.09 held two — a governance forum and a project blog,
both left behind by earlier theses — and recorded no class-A event with a primary source
anywhere in a 90-day window, across the whole list.

§6a forbids a host to be assumed: *a host for this lane is established by a TZ measurement
and never by assumption* (map inv. 44, inv. 52). This is that measurement.

---

## 2. Scope — exactly this, and the boundary is the point

**In scope:** for each member of `tokens[]`, determine whether a machine-readable
publication channel of the PROTOCOL ITSELF exists and answers this environment, and record
what it returned.

**Out of scope, and each of these makes the TZ's product wrong rather than merely wider:**

- **Reading the events.** This is a reachability and schema probe, permitted to role 1 by
  §7 item 9 precisely because it produces **no product fact**. Record that a channel serves
  dated records; never record a date, an event, a price or a supply figure. Harvesting the
  content converts a permitted environment measurement into the thing that clause forbids.
- **Writing the result anywhere but the report.** No `analyst/state.json`, no new data file,
  no edit to `ANALYST-INSTRUCTIONS.md` — item 14 of the hard floor forbids the last of these
  and a TZ asking for it would be defective. The Architect writes the measured hosts into §6a.
- **Any evasion.** A managed challenge, a 403 or a 429 **is the reading** (§7 item 9,
  `ANALYST-INSTRUCTIONS.md` §6). No user-agent spoofing, no proxy, no cookie replay, no
  retry loop. One attempt per candidate, its command recorded beside its result.
- **Re-probing hosts already closed by measurement.** `tokenomist.ai` and `cryptorank.io`
  are closed (§6a) and are not candidates here. Naming them again costs the budget this
  measurement exists to spend on primaries.

---

## 3. The universe is READ, never typed

```
node -e "…" # or grep/sed over index.html
```

Extract the symbol list from `index.html`'s `tokens[]` by command, print the count, and
record both in the report (map inv. 21: the universe is cut from production, never
transcribed). **A list typed into this session is a second copy of `tokens[]` and is
rejected at audit even if it happens to be right.** Every later step iterates over the
extracted list and over nothing else.

---

## 4. Candidate channel classes, tried in this order per coin

Stop at the first class that returns `primary-dated`; otherwise try all four and record
every attempt.

1. **Governance forum.** A Discourse instance answers `<topic-url>.json` and a category
   listing answers `/c/<slug>.json`; that JSON is the publication, not a rendering of it.
2. **Release or upgrade channel.** The protocol's own blog, changelog, release feed or
   GitHub releases API for the canonical repository.
3. **Token contract state**, directly or through a block explorer's machine-readable
   endpoint returning that contract's state — `dclass:'primary'` by §6, and the lane §6
   names as the one this engine can source least often.
4. **Exchange announcement list** filtered to the coin's own symbol — the primary for a
   listing, a delisting or a margin-tier change, and for nothing else.

**A coin may legitimately have no channel.** Recording `none-found` with the four attempts
beside it is a complete and correct result; inventing a plausible host is the failure map
inv. 44 names.

---

## 5. The report — one row per coin, closed verdict set

`CryptoReports/TZ-45-coin-catalyst-channels-report.md`, under §10's template, whose
`## Implementation Summary` carries this table:

| Symbol | Class tried | Host | Command | HTTP | Verdict |
|---|---|---|---|---|---|

**Verdict is one of exactly five words and nothing else is admissible:**

| Verdict | Meaning |
|---|---|
| `primary-dated` | the host answered and its response carries DATED event records |
| `primary-undated` | the host answered; no dated records in the response |
| `refused` | managed challenge, 403 or 429 — a decision by the publisher, not an obstacle |
| `unreachable` | timeout, DNS failure or connection refused |
| `none-found` | all four classes attempted, no candidate channel exists |

`Command` is the literal command run, so the reading reproduces. Where a class returned
`primary-dated`, add one line naming the FIELD in the response that carries the date — the
schema, never a value — because a channel whose date field nobody located is a channel the
next run will re-derive.

Close the report with the tallies: rows against the extracted `tokens[]` count, and the
count of each verdict.

---

## 6. Validation — written by the Architect, run by the Executor

1. `python3 -m py_compile` and `node --check` are **not applicable** — no code moves. State
   that as the verdict rather than omitting the section.
2. **Row count equals the count the §3 extraction command printed.** Both numbers in the
   report, compared explicitly. A table shorter than the universe is an incomplete
   measurement wearing the shape of a finished one.
3. **Every row carries all six columns.** An empty `Command` cell fails: the command is what
   makes the reading reproducible and is the whole basis on which §7 item 9 permits it.
4. **Every `Verdict` is one of the five words above**, checked per row against that set.
5. **No row carries a product fact** — no date, no event name, no price, no supply figure.
   Checked by reading the table, and a violation is reported as a deviation rather than
   silently trimmed.
6. **No command contains an evasion technique** — grep the recorded commands for
   user-agent overrides, proxy flags and retry loops, and state the result.
7. **`git status --porcelain` is empty apart from the report.** No file under `analyst/**`,
   no production file, no bench, no workflow. Print the output.
8. **No-regression statement:** this TZ moves no code, so every bench figure and every gate
   count of the fingerprint above is unchanged by construction — assert it rather than
   assume it, by confirming no file in the §0 table appears in the diff.

---

## 7. Deviations and blocking

A host that refuses is a RESULT and never a reason to stop. Stop and report **BLOCKED** only
if `tokens[]` cannot be extracted by command, or if this specification requires something
`EXECUTOR-INSTRUCTIONS.md` forbids. **Do not widen the scope to repair a thin result:** a
list of thirty rows in which twenty read `refused` is exactly the measurement the Architect
needs, and it is the input to the next specification rather than a failure of this one.
