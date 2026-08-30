# TZ-20 — Catalyst registry: trust root and content

**Canonical filename:** `TZ-20-catalyst-registry-content.md`
**Directory:** `CryptoTZ/`
**Report:** `CryptoReports/TZ-20-catalyst-registry-content-report.md`
**Model:** **Opus.** The allow-list is the registry's trust root and a `confirmed` entry
vetoes a side of the board; a mistake here changes production verdicts silently.

**Requires `EXECUTOR-INSTRUCTIONS.md` version 13 or later.**

**Origin.** The analysis run of 2026-08-30 found two dated events the registry does not
carry and correctly refused to write them itself: the registry is the one externalised
file whose `confirmed` flag can close a side, hard floor item 13 forbids the analyst
touching it, and inv. 39 makes the PRIMARY allow-list changeable only through a TZ. This
is that TZ.

---

## 0. Required System Map fingerprint — quoted IN FULL

**Revision 2026-08-30-b.** Baseline: TZ-19 merged into `main`; implementation
commit `cc8bade`, report `CryptoReports/TZ-19-gate-script-under-gate-report.md`. **The
baseline names the implementation commit, not the merge commit** — a merge commit
carries no content, and content is what this block pins.

Every TZ header quotes this block IN FULL — all seven anchors and the file table,
never a subset. The Executor matches each anchor as an exact substring against the
repository copy before any work (contract §5); any mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-30-b.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `54. **A record cannot contain the outcome of the action that stores it.**` |

Live files at this revision — the set every TZ header and every report fingerprints:

| File | Lines | MD5 |
|---|---:|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
| `catalysts.json` | 11 | `021dd2c90dc395240c0b0c3dbae40426` |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

The calibration record is fingerprinted, unlike every other bench artifact, because
it is one of exactly two places `DAY_RANGE_ABNORMAL = 1.39` exists and gate step 12
compares the two on every push (inv. 46).

Gate at this revision: `bench.yml`, **13 steps, 1 250 717 checks**, green on the
hosted runner (run `33254327296`, head `cc8bade`, all 13 steps `success`). Steps 1–12 sum
to **1 250 677**, step 7 at **691 109**, step 12 at **220 598**, unmoved through TZ-17,
TZ-18 and TZ-19. Step 13 reads **40**.

**`catalysts.json` IS in scope and its hash WILL change.** The other three files must be
byte-identical, and step 12's counter must not move.

---

## 1. Scope

| Path | Change |
|---|---|
| `bench/catalyst_bench.js` | add one host to the PRIMARY allow-list |
| `catalysts.json` | add four entries, bump `updated` |

**Files to Delete:** none. No frontend change, no `catalystCheck` change: **the data lives
in the file, the rule lives in the code, and the rule does not move** (map §3.15).

---

## 2. Change A — the trust root gains one host

Add `federalregister.gov` to the PRIMARY allow-list in `bench/catalyst_bench.js`, matched
by host on a dot boundary exactly as the existing entries are.

**Why it qualifies.** The Federal Register is the United States government's official
publication of record for proposed and final rules; a document there is the rule as filed
by the agency, not a report about it. `www.sec.gov` refuses this client with 403 and the
Federal Register's own HTML page redirects to a managed challenge, but its API serves the
same publisher's document. That is the API-over-page distinction the methodology already
draws, not a downgrade to a secondary source.

**Add nothing else.** The allow-list is the registry's trust root (inv. 39): one host, one
justification, one TZ. A host added «while we are here» is a host nobody argued for.

---

## 3. Change B — four entries

Schema v1 exactly (map §3.15): ASCII-only file, printed string `t` escaped `\uXXXX`,
`src` an array of URLs, `added` the ISO date written.

| sym | d | dir | kind | conf | source |
|---|---|---|---|---|---|
| `ENA` | 2026-09-02 | short | unlock | confirmed **only if** a primary schedule is reachable, otherwise `disputed` | protocol vesting schedule |
| `*` NFP | 2026-09-04 | both | macro | `disputed` | see below |
| `*` FOMC | 2026-09-16 | both | macro | confirmed | `federalreserve.gov` FOMC calendar |
| `ONDO` | 2026-10-20 | long | regulatory | confirmed | `federalregister.gov` API, File No. S7-2026-27 |

**The SUI unlock of 2026-09-01 is deliberately NOT registered.** By the time this TZ is
written, executed, audited and merged the date is behind the registry's `−1` back edge,
and an entry that can never act is clutter in the one file whose length is its risk.

**`conf` is decided by what the Executor can actually reach, not by this table.** For each
entry, fetch the named primary source and record the status. Reachable and stating the
date → `confirmed`. Not reachable → `disputed`, which annotates its own side and vetoes
nothing (inv. 39), and the report says which host refused. **Do not promote an entry on a
secondary calendar, and do not follow a managed challenge.** NFP is listed as `disputed`
in advance because the run of 30.08 measured `www.bls.gov` and `download.bls.gov` refusing
this client and `api.bls.gov` not serving the release schedule; if a primary schedule is
found, promote it and say where.

**Two entries have no coin.** `dir:'both'` macro events belong to the market, not to a
symbol. If schema v1 has no place for a symbol-less item, **report that and register only
the three coin-scoped entries** — inventing a `"*"` key is a schema change and schema
changes are additive-only through their own TZ (inv. 1). Do not improvise it.

---

## 4. Validation — written by the Architect

1. `python3 -c "import json;json.load(open('catalysts.json'))"` — parses; print the item
   count before and after.
2. File is ASCII-only after the edit: prove it, do not assert it. Every non-ASCII
   character in a printed `t` is `\uXXXX`-escaped.
3. `node --check` on `bench/catalyst_bench.js`.
4. Run the catalyst bench. Report its check count and the delta against the previous run,
   attributed. The bench reads the registry with production's own loader (inv. 42), so a
   malformed entry must fail it non-zero — **demonstrate that**: temporarily corrupt one
   entry, confirm the bench fails and names it, restore, confirm byte-identical.
5. **Allow-list negative control.** Prove the new host matches on a dot boundary and that
   a look-alike does not: `federalregister.gov` and `www.federalregister.gov` accepted,
   `federalregister.gov.example.com` and `notfederalregister.gov` rejected. A prefix or
   substring match on a trust root is how a trust root stops being one.
6. For every entry: the fetch performed, the host, the HTTP status, and whether the date
   was stated at that source. This table decides `conf` and must appear in the report.
7. Full `bench.yml` gate, 13 steps. Steps 1–12 must total **1 250 677** except any move in
   the catalyst bench, which is attributed term by term. **Step 12 must not move at all** —
   this TZ touches no exhaustion code.
8. `git diff --stat` — exactly the two files in §1.
9. MD5 and line counts for `index.html`, `main.py`, `bench/exhaustion-calibration.txt` —
   identical to §0 — and the new hash and line count for `catalysts.json`.
10. MD5 and line counts for the map, `EXECUTOR-INSTRUCTIONS.md` and
    `ANALYST-INSTRUCTIONS.md`, with revision and version strings.

**Do not run an analysis.**

---

## 5. Commit Message

```
feat(catalysts): register Sept-Oct dated events, add federalregister.gov to PRIMARY (TZ-20)
```

---

## 6. Acceptance criteria

1. `federalregister.gov` is on the PRIMARY allow-list and matches only on a dot boundary,
   proven by a negative control.
2. Every entry's `conf` is justified by a fetch recorded in the report, and no entry is
   `confirmed` on a secondary source.
3. `catalysts.json` parses, is ASCII-only, and follows schema v1 unchanged.
4. The catalyst bench fails non-zero on a corrupt entry, proven and restored.
5. Steps 1–12 of the gate unmoved except an attributed catalyst-bench delta; step 12
   unmoved absolutely.
6. Exactly two files changed.

---

## 7. Deliberately not done

`[решение принято мной]`

- **No schema change to carry symbol-less events.** Macro dates that belong to the whole
  market are a real gap in schema v1, but widening a schema to fit two entries, inside a
  TZ whose subject is the trust root, mixes two risks that should be taken separately.
- **No second host added.** `home.treasury.gov` will be wanted for the G20 finance track
  and is a strong candidate; it arrives with the entry that needs it, not before.
- **No `catalystCheck` change.** The rule is correct and untouched; only its input moves.
