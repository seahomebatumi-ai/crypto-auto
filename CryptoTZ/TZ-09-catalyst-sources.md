# ТЗ-09 — Catalyst sources: the first confirmed veto

**Canonical filename: `TZ-09-catalyst-sources.md`.** Commit the file under this
name regardless of the name it arrived under (§3 of the contract). Destination:
`CryptoTZ/`.

**Claude Code model: Opus.** The diff is small and the subject is the only layer
in the system that can CLOSE a trade direction. One scope replaces the rule that
decides which evidence may close it; the other rewrites a 400-day sweep whose
current expectations are hard-coded to «no live entry ever vetoes». Both are
places where a plausible-looking edit is wrong in a way no syntax check catches.

**Executor contract: Version 6.** Read it from the repository root before
anything else.

---

## 0. System Map fingerprint gate — blocking

Verify in `SYSTEM-MAP-CRYPTOCALCUL.md` **before any work**. On any mismatch:
STOP, report ЗАБЛОКИРОВАНО, state found versus required.

| Anchor | Required |
|---|---|
| `<!-- EDIT-MARKER 2026-08-22-CATALYST-REGISTRY -->` | present, exactly 1 occurrence |
| `<!-- EDIT-MARKER 2026-08-22-GATE-COMPOSITION -->` | present, exactly 1 occurrence |
| `## 4. Инварианты`, highest number | **43** |
| `## 9. Журнал миграций`, newest entry | `- 2026-08-22 (2):` |
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1807 lines, MD5 `476339934c9dcf14e0f4bf2353900d89` |

**The map is one edition behind on purpose.** It still describes TZ-08 as the
next TZ (invariant 43) and it still states the old source quorum in invariant 39
and §3.15. Both are superseded by this TZ. The Architect publishes the amended
map after the audit; **the Executor does not touch `SYSTEM-MAP-CRYPTOCALCUL.md`
under any circumstance.** Where a comment needs an anchor, cite «§3.15 / инв. 39,
изменён ТЗ-09» and never a bare invariant number that does not exist yet.

Baseline for the diff, recorded in the report **before** any edit:

| File | Lines | MD5 |
|---|---:|---|
| `catalysts.json` | 15 | `eb591d2ef2d792ca6a4a25f26442e9b9` |
| `bench/catalyst_bench.js` | 392 | `06ae385e8e424a1a26aa51487a751b6c` |
| `index.html` | 3522 | `68eebc9b5e40c7afd09a7d00d3fd1d21` |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |

---

## 1. Why this TZ exists

§10 item **(2b)**: verify the three live entries, fill `src`, promote what passes
the quorum, and resolve the known data conflicts. The analyst work is done and
its result is in §3 — the Executor does not research anything, does not add an
entry, and does not judge a source. Five findings drive the two scopes.

**Finding 1 — ZEC is real, but the entry was wrong twice.** The NU7 coinholder
vote exists and is primary-sourced: the Zcash community forum thread by `ebfull`
(5 August 2026) states a snapshot on 24 August 19:00 UTC and voting from
25 August. The entry's date was the day the vote **opens**, which is not the risk;
the risk is the day it **resolves**. That date was moved in the same thread on
6 August and reconfirmed on 10 August to align with the ZCAP poll:
**eligible ZEC can vote until 14 September 2026 at 19:00 UTC, results published
shortly after.** Secondary hosts still carry the superseded arithmetic — one
mainstream aggregator page still prints «voting open until September 12», derived
from «approximately 18 days» in the first version of the post. The entry's
direction was worse than its date: `dir:'long'` was an opinion about an outcome
nobody knows, printed under an allowed long as an argument for it.

**Finding 2 — the AVAX entry cannot be verified by anyone.** «разлок 10.69M AVAX
18.09» is not corroborated by a single host. Three trackers give three different
next-unlock dates for the same asset in the same week (10 August, 21 August with
3 584 842 tokens, 12 May), none of them 18 September, and no Avalanche primary
publishes an unlock calendar at all. The same probe on HYPE returns four
different dates across four trackers plus a documented ~30× gap between the
projected unlock and the amount the team actually claims. This is the ENA finding
reproduced twice on demand: **aggregated unlock data is not evidence.**

**Finding 3 — the SOL entry has no date to be right about.** Alpenglow activates
with Agave 4.3, which the Solana Foundation targets for **October 2026**; no
activation date exists, and the release itself is gated on validator adoption.
`"d":"2026-10-01"` was invented precision. A month is not a date.

**Finding 4 — the quorum rule contradicts its own rationale.** The header of
`catalyst_bench.js` says six trackers returned six inconsistent answers and «two
of them are not a quorum». The rule underneath it accepts exactly that: two
distinct hosts, of any kind, confirm an entry. Findings 2 and 3 are what that
rule buys — two aggregators agreeing about a date neither of them owns. Since a
`confirmed` entry closes a trading side, the evidence bar has to be the source's
**authority**, not the number of sites repeating it.

**Finding 5 — a scheduled binary event was not expressible, and it turns out
production already expresses it.** `dir` says which side an event supports. A
governance vote, a court date, an exchange decision — the whole class where the
resolution date is known and the outcome is not — supports neither side, and
forcing one is how the ZEC entry acquired a direction. The gap is in the schema,
not the code: with `dir:'both'`, `catalystCheck` already vetoes both sides when
the entry is `confirmed` (`c.dir !== mine` is true for both sides) and stays
completely silent when it is not (`c.dir === mine` is false for both sides).

**Measured by the Architect on this commit, executing the production `<script>`
through node `vm`, registry injected, no file edited:**

| `conf` / `dir` | LONG | SHORT | note |
|---|---|---|---|
| `confirmed` / `both` | veto | veto | none, either side |
| `confirmed` / `long` | — | veto | LONG only |
| `confirmed` / `short` | veto | — | SHORT only |
| `disputed` / `both` | — | — | none, either side |
| `disputed` / `long` | — | — | LONG only |
| outside the window, any combination | — | — | none |

Window edges re-measured on the same run: an event **14.00 days** ahead is inside,
**14.01 days** ahead is outside, **1.00 day** past is inside, **1.01 days** past is
outside. So `dir:'both'` needs **zero production changes** — it needs the enum
opened in the bench and its meaning proved.

---

## 2. Scope

Two scopes. If one is blocked, complete the other and report the blocked one
(contract §6).

### Files to Modify

- `catalysts.json` — scope A
- `bench/catalyst_bench.js` — scope B

### Files to Create / Delete

None.

### Explicitly out of scope

`index.html`, `main.py`, `journal/**`, `SYSTEM-MAP-CRYPTOCALCUL.md`, every
workflow including `bench.yml`, and every bench except `catalyst_bench.js`.
**Not one line of production logic changes in this TZ.** No new coin, no schema
version bump, no new file, no new dependency.

`git diff --stat` at the end must list exactly two paths.

---

## 3. Scope A — the registry

**3.1 Replace `catalysts.json` with exactly this file. Byte for byte, including
the two-space indentation and the ASCII escapes.**

```json
{
  "v": 1,
  "updated": "2026-08-22",
  "items": {
    "ZEC": [{ "d": "2026-09-14", "dir": "both", "kind": "protocol",
              "t": "\u0438\u0442\u043e\u0433\u0438 \u0433\u043e\u043b\u043e\u0441\u043e\u0432\u0430\u043d\u0438\u044f NU7 14.09",
              "conf": "confirmed",
              "src": ["https://forum.zcashcommunity.com/t/nu7-coinholder-vote/56912"],
              "added": "2026-08-22" }]
  }
}
```

Verification targets, all three independently checkable:

| Property | Required |
|---|---|
| File | 11 lines, MD5 `021dd2c90dc395240c0b0c3dbae40426` |
| `t` decodes to | «итоги голосования NU7 14.09» |
| `cat.hash` (`sha16(canon(items))`, journal §3.13) | `629681cf148e6199` |

The file stays ASCII-only and `t` stays `\uXXXX`-escaped, as it has been since
TZ-06. Do not «tidy» the JSON, do not reflow it onto one line per key, do not add
a trailing key. The MD5 is part of the specification precisely so that a helpful
reformat is caught rather than discussed.

**3.2 What this does on the board, stated so it is not later read as a bug.**
The entry is inert today. `CAT_WINDOW_D = 14`, so the veto is live from
**2026-08-31 00:00 UTC to 2026-09-15 00:00 UTC**, and during those fifteen days
ZEC prints «нет сделки: итоги голосования NU7 14.09» on **both** sides, with no
catalyst note anywhere. That is the intended result: the Boss's holding horizon is
seven days, the window is deliberately twice that, and the brake therefore engages
a week before a position would be carried into the count. Nothing else on the
board moves — score, rank, tier, leverage, liquidation and range position are
computed exactly as before (инв. 31: a catalyst may only veto).

**3.3 What was removed, and what must not silently come back.** The AVAX and SOL
entries are deleted, not demoted. A `disputed` entry still annotates its own side,
so keeping «разлок 10.69M AVAX» would keep printing an argument for shorting AVAX
built on a date no host confirms. An entry whose date cannot be established is not
weak evidence; it is not evidence. Do not re-add either one, do not replace them
with «corrected» dates from a tracker, and do not add any coin not listed in §3.1.

**3.4 The rules the next registry edit follows.** JSON carries no comments, so
they are written into the header comment of `catalyst_bench.js` alongside the
quorum paragraph (§4.1), where the next editor meets them:

- `d` is the date the event **resolves**, announced by a primary source. A month,
  a quarter, a «target», or a window is not a date and does not become an entry.
- `dir` is mechanical, never a forecast. Supply that certainly reaches the market
  → `short`. Determinate one-way mechanics → that side. A scheduled resolution
  with an unknowable outcome → `both`. Anything requiring an opinion about the
  outcome → the event does not belong in the registry at all.
- `src` must support the date in `d`, not merely the existence of the event.

---

## 4. Scope B — `bench/catalyst_bench.js`

**4.1 The quorum rule: `confirmed` requires a primary source.** Replace
`quorumOk` with this and delete the two-host branch entirely:

```js
function isPrimary(h) {
    for (let i = 0; i < PRIMARY.length; i++) {
        const p = PRIMARY[i];
        if (h === p || h.slice(-(p.length + 1)) === '.' + p) return true;
    }
    return false;
}
function quorumOk(e) {
    if (e.conf !== 'confirmed') return true;      // disputed carries no burden
    const hosts = (e.src || []).map(hostOf).filter(function (h) { return h !== null; });
    for (let i = 0; i < hosts.length; i++) if (isPrimary(hosts[i])) return true;
    return false;
}
```

`hostOf` is unchanged. Aggregators may still appear in `src` as corroboration;
they can no longer confer authority, however many of them agree. Rewrite the
paragraph above the function to say that, and keep the ENA sentence — it is now
supported by the AVAX and HYPE probes in §1 rather than contradicted by the code.

**4.2 `PRIMARY`.** Add `'zfnd.org'` (Zcash Foundation) and nothing else. Suffix
matching in §4.1 now covers subdomains, so `docs.ethena.fi`, `support.binance.com`
and the like resolve without listing each one. **The list is the registry's trust
root: it changes only through a TZ**, never as a side effect of wanting an entry
to pass. State that in the comment.

**4.3 The case table.** These thirteen cases and these results; the second row is
the change and must be labelled as such. Each was executed by the Architect
against the function text in §4.1, with 0 mismatches.

| Expected | Case | `src` |
|---|---|---|
| pass | one primary source | `https://zips.z.cash/zip-0253` |
| **block** | **two independent aggregators — was `pass` before ТЗ-09** | `https://tokenomist.ai/x`, `https://cryptorank.io/y` |
| block | one aggregator alone | `https://tokenomist.ai/x` |
| block | no source at all | — |
| block | same aggregator twice | `https://tokenomist.ai/x`, `https://www.tokenomist.ai/y` |
| block | not a URL | `со слов` |
| pass | `disputed` needs nothing | — |
| pass | primary plus aggregator | `https://github.com/zcash/zips/pull/1`, `https://cryptorank.io/y` |
| pass | subdomain of a primary | `https://docs.ethena.fi/ena/tokenomics` |
| pass | `www.` and port stripped | `https://WWW.Binance.com:443/en/support/announcement/detail/x` |
| block | suffix lookalike | `https://notethena.fi/x` |
| block | primary as a left label | `https://ethena.fi.attacker.com/x` |
| pass | the live ZEC entry | `https://forum.zcashcommunity.com/t/nu7-coinholder-vote/56912` |

**4.4 `DIRS` becomes `['long', 'short', 'both']`.** The schema version stays `1`:
this is an additive enum value that the production loader and `catalystCheck`
already handle, and an older build fed the same file behaves identically (инв. 1,
9). Do not bump `v`, do not add a field, do not touch `KINDS` or `CONFS`.

**4.5 Section 3 is rewritten as an authority table, not a fixed expectation.**
Today it asserts «no live entry may veto» and «the supporting side sees notes on
15 dates», which is a statement about the *contents* of one edition of the file.
It goes red the moment the registry does its job — which is why it is red now.
Replace it with expectations **derived from each entry**, keeping the sweep at
400 consecutive days × every symbol in `tokens[]` × both sides, from the same
fixed `START`:

| `conf` | `dir` | veto LONG | veto SHORT | note LONG | note SHORT |
|---|---|---|---|---|---|
| not `confirmed` | `long` | no | no | yes | no |
| not `confirmed` | `short` | no | no | no | yes |
| not `confirmed` | `both` | no | no | no | no |
| `confirmed` | `long` | no | **yes** | yes | no |
| `confirmed` | `short` | **yes** | no | no | yes |
| `confirmed` | `both` | **yes** | **yes** | no | no |

Every veto and every note must carry the entry's own `t`. Inside the window the
table holds on all fifteen calendar dates ending on `d`; outside it, both fields
are `null` on both sides. Symbols with no entry stay silent — keep that check as
it is. Keep the calendar-date form of the assertion rather than a second copy of
the window arithmetic, and keep reading `CAT_WINDOW_D` from production (инв. 20,
21).

**4.6 Overlap guard.** The table above is per entry, and the file has one entry
per coin. If a coin ever has two entries whose windows overlap on a swept date,
the precedence rule decides the answer and this table does not — so the bench must
detect that case, print it, and **fail**, rather than quietly compare against the
wrong expectation. Today it must report zero overlaps.

**4.7 `updated` is not older than the newest `added`.** One line, no wall clock
involved. An edit that adds an entry and forgets `updated` currently passes
everything; the journal and the board both print `updated` as the registry's age.

**4.8 No assertion in this bench may depend on the current date.** `START` stays a
literal, the sweep stays relative to it, and nothing compares an entry's date to
`Date.now()`. A bench that turns red on an unrelated pull request because a date
passed is not a control, it is a scheduled outage. The existing `Date.now()` call
in section 0 is legal — it runs against an empty registry and asserts silence.

**4.9 Counts stay counts (инв. 43).** The check counter is incremented at the
comparison site only. Report the new total for this bench against **23 007** and
account for the difference by term: notes that no longer exist, comparisons that
replaced them, new quorum cases, new `both` cases. The zero-comparison guard
stays exactly as it is.

**4.10 Two negative controls on the live path, both mandatory.** Synthetic cases
prove the rule; these prove it is wired to the file that ships:

1. In a scratch copy, blank the ZEC entry's `src` to `[]`. `catalyst_bench.js`
   must exit non-zero on the quorum check. Restore, show green.
2. In a scratch copy, replace `src` with two aggregator URLs
   (`https://tokenomist.ai/x`, `https://cryptorank.io/y`). It must **also** exit
   non-zero — this is the case that passed before ТЗ-09 and is the whole point of
   §4.1. Restore, show green and the file byte-identical to §3.1.

---

## 5. What must not change, and how that is proved

`index.html` and `main.py` are not edited. The claim that `dir:'both'` needs no
production change is proved by the bench executing the production `catalystCheck`
(инв. 21) **and** by `git diff --stat` showing neither file in the diff. If the
Executor finds a production change to be necessary, that is a finding: stop,
report it, change nothing (contract §7.2).

The other ten gate steps must return the numbers TZ-08 recorded. The Architect
ran the full gate on this commit with the §3.1 registry in place and reproduced
them exactly; any deviation is a finding, not a rounding difference:

| Step | Required |
|---|---:|
| `verify_board.js` | 109 |
| `board2_bench.js` | 130 |
| `prot_bench.js index.html` | 168 |
| `verify_bench.py` | 35 |
| `direction_bench.py --props --fixtures --control --sim` | 188 577 |
| `fresh_bench.js` | 3 424 |
| `journal_bench.js` | 694 030 |
| `display_bench.py` | 24 598 |
| `render_bench.py` | 15 925 |
| `direction_bench.py --display` | 15 629 |

---

## 6. Validation — written by the Architect, run in full by the Executor

Every item is mandatory. An item that cannot be run **fails**; it is never «not
applicable» (contract §9). Record the check count and exit code of each.

**6.1 Baseline.** The §0 fingerprint plus line counts and MD5 of both scope files
before any edit.

**6.2 Syntax and integrity.** `node --check bench/catalyst_bench.js`;
`python3 -c "import json;json.load(open('catalysts.json'))"`; the §3.1 table
(11 lines, MD5, decoded `t`, `cat.hash`) reproduced with the commands used;
`node --check` on the `<script>` extracted from the untouched `index.html`;
`python3 -m py_compile main.py` on the untouched file.

**6.3 No-regression, proven not asserted.** `git diff --stat` lists exactly
`catalysts.json` and `bench/catalyst_bench.js`. Paste `git diff -- catalysts.json`
in full.

**6.4 Scope B, rule level.** The thirteen §4.3 cases with expected and actual
results in a table; the `both` semantics from §1 reproduced through production
`catalystCheck` in all six `conf`×`dir` combinations plus the four window edges
(14.00 / 14.01 days ahead, 1.00 / 1.01 days past).

**6.5 Scope B, file level.** Zero overlaps (§4.6); `updated` check (§4.7); the
count reconciliation against 23 007 by term (§4.9).

**6.6 Negative controls.** Both of §4.10, each shown red then green, with the
final MD5 of `catalysts.json` equal to §3.1.

**6.7 Full gate.** All eleven steps of `bench.yml` in order with per-step counts
and exit codes, the ten fixed steps matching §5 exactly, and a new total stated
against **965 632**.

**6.8 CI.** `Bench gate` runs on the branch push and its conclusion is `success`.
Report run number, URL and conclusion. Do not plant a failure: §4.10 already
supplies two red-then-green controls on the live path.

---

## 7. Constraints

- Minimal diff through existing structures. No new file, no new dependency, no
  refactor beyond the functions named in §4.
- The bench's language is English and stays English.
- Never edit an assertion to make a bench pass and never remove a gate step
  (contract §7.2, §7.12). Section 3 is being rewritten because its expectation
  encodes the contents of one edition of the registry, and that reasoning is
  stated in §4.5 — it is not a licence to adjust anything else that goes red.
- No research. Every fact this TZ needs is in §1 and §3; if something looks
  wrong, report it as a finding instead of correcting it from a web source.
- No new coins, no schema version bump, no workflow edit.

---

## 8. Commit Message

```
feat(catalysts): sources, primary-source quorum, two-sided event risk (TZ-09)
```

---

## 9. Report

`CryptoReports/TZ-09-catalyst-sources-report.md`, contract §10 format, including
`## CI Execution`. Commit it directly to `main` before the closing message.

State separately and without blurring: what was completed · what was skipped ·
what failed validation · what is a pre-existing defect · what remains a risk.
`## Fingerprints` is mandatory: line count and MD5 for `index.html`, `main.py`
and `SYSTEM-MAP-CRYPTOCALCUL.md`, plus the map's newest migration date, plus the
new `catalysts.json` MD5 and its `cat.hash`.

Name explicitly, under `## Remaining Risks`, that from 31.08 to 15.09 the board
refuses both sides of ZEC by design, and that the System Map still carries the
pre-ТЗ-09 wording of invariant 39 until the Architect republishes it.

If no pull request could be opened, apply the §8 fallback of contract Version 6:
branch name and compare URL, in the report **and** in the closing message, with
the CI consequence stated in bold.
