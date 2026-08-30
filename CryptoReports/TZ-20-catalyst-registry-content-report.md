# Implementation Report — TZ-20

Catalyst registry: trust root and content.
Specification: `CryptoTZ/TZ-20-catalyst-registry-content.md`.

## Status

**PARTIAL.**

Change A shipped in full and is proven. Change B specified four entries; **one of
the four is registered**, and the other three are not, for three different reasons —
one of which the TZ itself pre-authorised, one of which the TZ's own rule about `*`
applies verbatim, and one of which is a hard-floor conflict the Architect must
resolve. Nothing was improvised in any of the three cases.

| Entry | Outcome |
|---|---|
| `ENA` 2026-09-02 | **registered**, `conf: disputed` |
| `*` NFP 2026-09-04 | not registered — schema v1 carries no symbol-less item (TZ §3 authorises exactly this) |
| `*` FOMC 2026-09-16 | not registered — same reason; and see finding 4, its named source is not on the allow-list |
| `ONDO` 2026-10-20 | **BLOCKED** — `kind: 'regulatory'` is outside the enum the gate asserts (finding 2) |

**The previous TZ's branch was merged.** `cc8bade` (TZ-19) is contained in `main`;
this work is built on a merged base, not on an unmerged one.

## Inbound Filing

None. `TZ-20-catalyst-registry-content.md` arrived on `origin/main` at its declared
canonical path `CryptoTZ/`, under its canonical filename, with no mangling. No
`git mv` was required and no duplicate copy exists.

The session clone was behind: `git fetch --all --prune` moved `origin/main`
`0a734ab..be8bb85`, and the working tree was brought to it with `git pull --ff-only`
(fast-forward, 4 files). `git rev-parse --is-shallow-repository` → `false`, so no
`--unshallow` was needed. The TZ was invisible before the fetch, exactly as §3
predicts.

The same fetch delivered `EXECUTOR-INSTRUCTIONS.md` **v13**, which TZ-20 §9 requires.
The v12→v13 diff is 14 lines: the version string, the changelog paragraph, and a new
§4b clause forbidding the day log from reporting its own commit and push (inv. 54).
All of it is role 2. No role 1 clause changed.

## Scope Executed

TZ §1 authorises two paths. Both were touched and nothing else:

| Path | Authorised change | Done |
|---|---|---|
| `bench/catalyst_bench.js` | add one host to the PRIMARY allow-list | yes, plus its negative control — see Deviations |
| `catalysts.json` | add four entries, bump `updated` | one entry added, `updated` bumped |

## Files Created

None.

## Files Modified

- `bench/catalyst_bench.js` — `federalregister.gov` added to `PRIMARY`; a
  justification paragraph added to the block comment that governs that list; four
  boundary cases added to `QCASES`.
- `catalysts.json` — `ENA` entry added; `updated` bumped `2026-08-22` → `2026-08-30`.

## Files Renamed

None.

## Files Deleted

None. TZ §1 names none.

## Implementation Summary

### Change A — the trust root gains one host

`federalregister.gov` is appended to `PRIMARY` on its own line. It is matched by the
existing `isPrimary`, unchanged: `h === p || h.slice(-(p.length + 1)) === '.' + p`.
No matching code was touched — the dot boundary the TZ requires is a property of the
function that was already there, and the proof of that is in Test Results, not an
assertion.

The block comment above `PRIMARY` states that adding a host "promotes every future
entry that cites it, which is exactly the decision an implementer may not take
alone." A host arriving with no recorded argument would contradict that comment in
the file that carries it, so TZ §2's justification is recorded next to the list: the
Federal Register is the United States government's official publication of record, so
a document served there is the rule as filed by the agency rather than a report about
it, and the API-over-page distinction is the methodology's own, not a downgrade.

**Nothing else was added.** TZ §2 and §7 both forbid a second host;
`home.treasury.gov` and `federalreserve.gov` are absent, and finding 4 below records
what the second of those absences costs.

### Change B — the entries

**`ENA`, registered `disputed`.** TZ §3's rule for this entry is "`confirmed` **only
if** a primary schedule is reachable, otherwise `disputed`". `docs.ethena.fi` — a
subdomain of `ethena.fi`, which is on the allow-list — is reachable and returns 200,
but what it publishes is a vesting **policy**, not a dated calendar: a 1-year 25%
cliff with 3-year linear monthly vesting thereafter, anchored at "ENA TGE at March 5th
2024". It states no date in September 2026 and does not state `2026-09-02`. Under
inv. 39 a `confirmed` entry needs a primary standing behind **its date**, and under
the registry-editing rules written at the top of `catalyst_bench.js`, "`src` must
support the date in `d`, not merely the existence of the event." Neither is satisfied,
so the entry is `disputed`: it annotates its own side and vetoes nothing. See finding
5 for what this implies about the date itself.

**`*` NFP and `*` FOMC, not registered.** TZ §3 anticipated this: "If schema v1 has no
place for a symbol-less item, report that and register only the … coin-scoped
entries — inventing a `"*"` key is a schema change and schema changes are
additive-only through their own TZ (inv. 1). Do not improvise it." Schema v1 has no
such place, and the gate enforces it: `catalyst_bench.js` asserts
`items key "<sym>" is in tokens[]` for every key in `items`, and `tokens[]` is the
frozen 28 (inv. 2). A `"*"` key fails that assertion. Reported, not improvised.

**`ONDO`, blocked.** Detailed as finding 2.

## Validation

Every item of TZ §4 was run. None was skipped and none was treated as not applicable.

**Baseline first.** The full 13-step gate was replayed locally on the unmodified tree
before any edit, and its steps 1–12 summed to **1 250 677** — the exact figure map §0
states, at the exact revision it pins. The diff below is therefore provable against a
baseline that was measured, not assumed.

| # | TZ §4 item | Result |
|---|---|---|
| 1 | `catalysts.json` parses; item count before/after | **pass** — before 1 symbol / 1 entry, after 2 / 2 |
| 2 | ASCII-only, proven; every non-ASCII char of `t` is `\uXXXX`-escaped | **pass** — 742 bytes, **0 bytes > 127** |
| 3 | `node --check bench/catalyst_bench.js` | **pass** — exit 0 |
| 4 | catalyst bench check count + attributed delta; corrupt entry must fail it non-zero, restore byte-identical | **pass** — 23 040 → 23 056, **+16**, attributed below; three corruptions each failed non-zero and named `ENA[0]`; restored byte-identical |
| 5 | allow-list negative control on the dot boundary | **pass** — all four cases correct, and each proven able to fail |
| 6 | per-entry fetch table deciding `conf` | **produced** — see Test Results; and see finding 1 |
| 7 | full `bench.yml`, 13 steps; steps 1–12 = 1 250 677 except an attributed catalyst move; step 12 unmoved | **pass** — only step 8 moved, +16; step 12 moved 0 |
| 8 | `git diff --stat` — exactly the two files of §1 | **pass** — 2 files, 29 insertions, 4 deletions |
| 9 | three files byte-identical to §0; new hash for `catalysts.json` | **pass** — all three MATCH; new hash recorded |
| 10 | map, contract and methodology hashes with revision/version strings | **pass** — recorded under Fingerprints |

**Standing checks** (map §6 item 1) — run as evidence that no production file moved,
though neither `index.html` nor `main.py` is in scope: `python3 -m py_compile main.py`
exit 0; `node --check` on the `<script>` block extracted from `index.html`
(192 939 chars) exit 0.

**"Do not run an analysis" (TZ §4).** No analysis was run. Nothing under `analyst/`
was read for analytical purposes, nothing under `analyst/` was written, and no market
advice appears anywhere in this run.

## Test Results

### Gate — every step, before and after

Local replay of all 13 steps of `.github/workflows/bench.yml`, in workflow order.
Counts are each bench's own printed counter, read from its output — never estimated
(inv. 43).

| Step | Bench | Before | After | Delta |
|---:|---|---:|---:|---:|
| 1 | `verify_board.js` | 109 | 109 | 0 |
| 2 | `board2_bench.js` | 130 | 130 | 0 |
| 3 | `prot_bench.js` | 372 | 372 | 0 |
| 4 | `verify_bench.py` | 35 | 35 | 0 |
| 5 | `direction_bench.py --props --fixtures --control --sim` | 255 708 | 255 708 | 0 |
| 6 | `fresh_bench.js` | 3 424 | 3 424 | 0 |
| 7 | `journal_bench.js` | 691 109 | 691 109 | 0 |
| 8 | `catalyst_bench.js` | 23 040 | 23 056 | **+16** |
| 9 | `display_bench.py` | 24 598 | 24 598 | 0 |
| 10 | `render_bench.py` | 15 925 | 15 925 | 0 |
| 11 | `direction_bench.py --display` | 15 629 | 15 629 | 0 |
| 12 | `exhaustion_bench.js` | 220 598 | 220 598 | **0** |
| | **steps 1–12** | **1 250 677** | **1 250 693** | **+16** |
| 13 | `live-gate.sh --selftest` | 40 | 40 | 0 |
| | **all 13** | **1 250 717** | **1 250 733** | **+16** |

Steps 1–12 before = **1 250 677** and all 13 before = **1 250 717**: both match map §0
exactly. Step 7 held at **691 109** and step 12 moved by **0**, as TZ §4.7 requires
absolutely.

**The +16, attributed term by term** — no term is inferred, each is a named counter:

| Term | Where | Delta |
|---|---|---:|
| `items key "ENA" is in tokens[]`, `ENA: entry list is an array` | §1 schema, per symbol | +2 |
| the ten per-entry schema checks on `ENA[0]` | §1 schema, per entry | +10 |
| `ENA[0] passes quorum` | §2 quorum, per live entry | +1 |
| `symbols with no entry stay silent` fell 27 → 26 | §3 sweep | **−1** |
| four new allow-list boundary cases (synthetic cases 13 → 17) | §2 quorum, `QCASES` | +4 |
| | **total** | **+16** |

The 400 × 28 × 2 authority sweep is unchanged in size, as expected: it iterates the
symbol list, not the registry.

### Negative control 1 — a corrupt entry must fail the bench non-zero (TZ §4.4)

The bench reads the registry with production's own loader (inv. 42), so this is a
demonstration, not a claim. Three independent corruptions, each applied to the live
file and then reverted:

| Corruption | Exit | Bench output |
|---|---:|---|
| `"conf": "disputed"` → `"maybe"` | **1** | `FAIL ENA[0] conf in enum: got false want true` |
| `"d": "2026-09-02"` → `"02.09.2026"` | **1** | `FAIL ENA[0] d is YYYY-MM-DD` and `FAIL ENA[0] d parses` |
| `"items": {` → `"items":` (malformed JSON) | **1** | non-zero, no fallback to an empty registry |

Each names the offending entry. **Restored byte-identical**: md5
`5c03cc936a49c90c68fe1d8e64684a1c` before corruption and after restoration, and the
bench returns to exit 0.

### Negative control 2 — the allow-list dot boundary (TZ §4.5)

The four cases required by §4.5, run through the bench's real `isPrimary` against the
real `PRIMARY`:

| Source host | Required | Measured |
|---|---|---|
| `federalregister.gov` | accepted | **accepted** |
| `www.federalregister.gov` | accepted | **accepted** (`www.` stripped by `hostOf`) |
| `federalregister.gov.example.com` | rejected | **rejected** (primary as a left label) |
| `notfederalregister.gov` | rejected | **rejected** (suffix look-alike) |

**And each of the four was proven able to fail.** A control that has never gone red is
not a control (inv. 22, 23), so each case's expectation was flipped in turn, the bench
re-run, and the failure confirmed to name that case:

```
flipped "federalregister.gov exactly"    -> rc=1  FAIL quorum, federalregister.gov exactly: got true want false
flipped "`www.` of the new host"         -> rc=1  FAIL quorum, `www.` of the new host: got true want false
flipped "new host as a left label"       -> rc=1  FAIL quorum, new host as a left label: got false want true
flipped "new host suffix lookalike"      -> rc=1  FAIL quorum, new host suffix lookalike: got false want true
```

The `got` column is the real answer in each direction. The bench was restored
byte-identical: md5 `fe5c9be2107c7aa3c7fc14f5716284e3` before and after.

### The fetch table (TZ §4.6) — what was reached, and what it said

Every fetch below was performed in this session. **Read finding 1 before reading this
table**: hard floor item 9 forbids role 1 the in-session fetch that TZ §3 and §4.6
require, and that conflict — not the results here — is what the Architect must
resolve.

| Entry | Host fetched | HTTP | Did the source state the date? |
|---|---|---:|---|
| `ENA` 2026-09-02 | `docs.ethena.fi/overview/ena/tokenomics` (+ `.md`) | **200** | **No.** Publishes a vesting *policy* — 1yr 25% cliff, 3yr linear monthly, "Unlock schedules … started on ENA TGE at March 5th 2024" — and no dated calendar. No occurrence of `2026-09-02`. |
| `*` NFP 2026-09-04 | `www.bls.gov/schedule/news_release/empsit.htm` | **403** | Not reached. Refuses this client, exactly as TZ §3 records. |
| `*` NFP 2026-09-04 | `api.bls.gov` (`/publicAPI/v2/timeseries/...`) | **200** | **No.** Answers, but serves timeseries data, not the release schedule — as TZ §3 records. |
| `*` FOMC 2026-09-16 | `www.federalreserve.gov/monetarypolicy/fomccalendars.htm` | **200** | **Yes.** The 2026 panel lists eight meetings; September is **15–16\***, so the decision lands 2026-09-16 — the TZ's date. |
| `ONDO` 2026-10-20 | `www.federalregister.gov/api/v1/documents.json` (`term=S7-2026-27`) | **200** | **Yes.** One match: document `2026-17183`, *Regulation Crypto Assets*, SEC, Proposed Rule, `publication_date` 2026-08-21, **`comments_close_on` 2026-10-20** — the TZ's date exactly. |

`conf` as actually written: `ENA` → `disputed`, on its own source's silence about the
date. The other three entries are not in the file at all, so no `conf` was written for
them.

### Hosted runner

Reported separately under `## CI Execution`. A local replay is not a runner run.

## Deviations

**One, declared.** TZ §1 describes the change to `bench/catalyst_bench.js` as "add one
host to the PRIMARY allow-list", and the commit also adds **four `QCASES` rows and a
comment paragraph** to that file.

The reason is that TZ §4.5 makes the negative control mandatory and §6.1 makes it an
acceptance criterion — "proven by a negative control" — and TZ §4.7 states the
catalyst bench's count is expected to move and must be "attributed term by term",
which only reads sensibly if the bench gains checks. A control proved once by hand at
the moment the host is added is a control nothing re-checks afterwards; the four cases
belong in the gate, beside the two boundary cases that already exist for `ethena.fi`.
This **adds** assertions and weakens none, so hard floor item 2 is not engaged in the
direction it guards. It is nevertheless more than §1's sentence authorises, so it is
declared here rather than folded into the summary.

**No other deviation.** No production file was touched, `catalystCheck` was not
changed, the frontend was not changed, no second host was added, and the `conf` of no
entry was decided by anything but the rule in TZ §3.

## Pre-existing Issues

### 1. Hard floor item 9 forbids what TZ §3 and §4.6 require — and inv. 44's premise is measurably false in this session

TZ §3 requires "For each entry, fetch the named primary source and record the status",
and §4.6 requires the resulting table in this report. Hard floor item 9 says the
opposite, in terms that name this exact case:

> **An implementation session reaches no market host at all** (inv. 44): a stage that
> needs external data exists only as a workflow step, and an implementation TZ that
> asks for an in-session fetch is BLOCKED before it starts.

Under §7's preamble that makes TZ-20 defective on its face. **But inv. 44 is not a
rule, it is a measurement** — hard floor item 9 says so itself: "Inv. 44 is a
measurement of an implementation session's egress, not a property of the network."
It was re-measured in this session, and it does not reproduce:

| Host | inv. 44 says | Measured now |
|---|---|---|
| `api.binance.com` | refused at CONNECT | **200**, and `ticker/price?symbol=ONDOUSDT` returned a live price |
| `data-api.binance.vision` | refused at CONNECT | **200** |
| `data.binance.vision` | refused at CONNECT | **200** |
| `api.coingecko.com` | refused at CONNECT | **200**, `{"gecko_says":"(V3) To the Moon!"}` |

No proxy variables are set in the environment. Inv. 44's sentence "An Executor
session's egress refuses **every market host** at CONNECT — archive, mirror, both
production hosts, CoinGecko" is false in this session, on all four hosts it names, and
the mechanism the blocking clause rests on — "a stage needing external data cannot
execute there however well it is written" — did not occur: the stage executed and
returned numbers.

**This was not treated as a licence.** The floor binds regardless of what a TZ says
and regardless of what I measure, so the conflict is routed here rather than resolved
in the working tree, and **no entry in this commit is `confirmed`.** The one entry
written is `disputed`, which vetoes nothing (inv. 39) — the fail-safe direction — and
its value follows from its own source's silence, not from the contested authority of
an in-session fetch. Had `ONDO` been registrable (finding 2), this conflict would have
had to be resolved before it could be written `confirmed`, because the Federal
Register fetch is the only thing standing behind that date.

Three ways out, all the Architect's: amend inv. 44 and hard floor item 9 to the scope
its evidence actually supports; or re-specify TZ-20's fetches as a workflow step and
leave the clause as it is; or confirm the clause as written, in which case a future
TZ-20-style registry TZ cannot decide `conf` at all and every entry it writes is
`disputed` by construction.

### 2. `kind: 'regulatory'` is outside the enum the gate asserts — `ONDO` is blocked

TZ §3's table specifies `kind: regulatory` for the `ONDO` entry.
`bench/catalyst_bench.js` declares `const KINDS = ['unlock', 'protocol', 'listing',
'macro']` and asserts `kind in enum` for every entry. `regulatory` is not in it, so
registering `ONDO` as specified turns the gate red on a product that is behaving
correctly.

There are three ways to make it green and **all three are forbidden**: adding
`regulatory` to `KINDS` is editing a bench so a new input passes (hard floor item 2)
and is a change to that file beyond the single change §1 authorises; removing or
skipping the step is hard floor item 12; and substituting a `kind` the enum already
carries would be inventing a schema decision — which is precisely what TZ §3 forbids
two paragraphs earlier, for the `"*"` key, in words that transfer without alteration:
"a schema change and schema changes are additive-only through their own TZ (inv. 1).
Do not improvise it."

So `ONDO` is not registered, and this is the one part of TZ-20 that is blocked rather
than pre-authorised. **What would unblock it:** a TZ that adds `regulatory` to `KINDS`
as an additive enum value — exactly as TZ-09 §4.4 added `both` to `DIRS`, with the
same argument that production's `catalystCheck` never reads `kind`, so an older build
fed the same file behaves identically (inv. 1, 9) — after which the `ONDO` entry is
one line.

**Root cause, and it is a §-level defect:** map §3.15 states the schema as
`kind unlock | protocol | listing | …`, with an ellipsis that reads as open-ended,
while the gate closes it to exactly four values. The rule lives in two places and the
two disagree, which is the condition the contract's "No rule lives in two files"
paragraph names as a defect and a finding.

### 3. TZ §3 says "the three coin-scoped entries"; there are two

TZ §3's table has four rows, two of which are marked `*` and have no coin. The
instruction for the schema-v1 case reads "register only the three coin-scoped
entries". Four minus two is two: `ENA` and `ONDO`. No third coin-scoped entry exists
anywhere in the TZ. The set is determinate even though the count is wrong — no
reading of the TZ produces a third — so this was executed on the set, not the number,
and recorded here rather than treated as an ambiguity.

### 4. The FOMC entry's named source could not have confirmed it even if schema v1 carried it

TZ §3 names `federalreserve.gov` as the FOMC entry's source and marks it `confirmed`.
`federalreserve.gov` is **not on the PRIMARY allow-list** and TZ §2 adds only
`federalregister.gov` — a different host, one dot-boundary label apart, and §2 and §7
both forbid adding a second. So even had schema v1 carried a symbol-less entry, `conf:
confirmed` on that source would have failed `quorumOk` and turned the gate red under
inv. 39.

The two hosts are easy to read as one another. If the Architect intends future macro
entries sourced from the Federal Reserve, `federalreserve.gov` needs its own TZ; §7's
stated policy — a host "arrives with the entry that needs it, not before" — is
consistent with that and is not a contradiction, only a note that the entry and its
host must arrive together.

### 5. `ENA`'s date is not supported by any source reached, including its own primary

The registered date `2026-09-02` appears in TZ §3's table and nowhere else that was
reachable. `docs.ethena.fi` publishes monthly linear vesting anchored at TGE
2024-03-05; monthly steps from that anchor fall on the **5th**, which would put the
September 2026 unlock at 2026-09-05, not 2026-09-02. That inference is offered only as
a pointer — the auditable fact is the narrower one, that **the primary publishes a
policy and no dated calendar, and states no September 2026 date at all.**

The entry was still registered, because §1 makes the date the Architect's to assert
and §6 forbids me to redesign it, and because `disputed` is inert against the veto
path. But the board will print «разблокировка ENA 02.09» under a SHORT on ENA for the
fifteen days ending 2026-09-02, and map §3.15 says of exactly this situation that
"Entries that no host confirms are deleted rather than demoted — a `disputed` entry
still annotates its own side, so keeping one keeps printing an argument built on a
date nobody confirms."

**That sentence and TZ §3's "otherwise `disputed`" instruction point in opposite
directions**, which is the second place in this TZ where the map and the specification
disagree. The Architect's call is to correct the date, withdraw the entry, or confirm
that a `disputed` annotation on an unconfirmed date is wanted here.

### 6. `federalregister.gov` ships with no entry that uses it

Change A's justification in TZ §2 stands on the source's own authority and is
independent of Change B, so the host was added as authorised. But its only intended
consumer is the `ONDO` entry, which finding 2 blocks. Until that entry lands, the new
allow-list member promotes nothing. It is inert rather than wrong — the four boundary
cases keep it honest in the gate — and it is noted because §7's own principle is that
a host "arrives with the entry that needs it".

### 7. Step 5 of the gate cannot complete in this session at default node settings

`direction_bench.py --props --fixtures --control --sim` shells out to node, and on the
unmodified tree it died with `FATAL ERROR: Reached heap limit Allocation failed -
JavaScript heap out of memory` after its first three stages passed. This box has
955 MB of RAM with ~441 MB available. It is **not a product defect**: the same step is
green on the hosted runner at this head (see CI Execution), and re-running it locally
with `NODE_OPTIONS=--max-old-space-size=6144` completes and returns **255 708** checks
— the exact figure that makes the local baseline sum to map §0's 1 250 677.

Recorded because it pre-existed the change (it reproduced on a clean tree at
`be8bb85`, before any edit), and because a future Executor on a small box will meet it
and should not read it as a regression.

## Remaining Risks

- **Three of four specified entries are not in the registry.** The registry's coverage
  of September–October is one `disputed` ENA annotation. Anyone reading the board
  should not take the registry's silence on FOMC, NFP or the SEC comment deadline as
  evidence those dates are absent from the market.
- **The `conf` question is unresolved, not answered.** If the Architect resolves
  finding 1 in favour of the TZ, `ONDO` becomes `confirmed` once finding 2 is fixed —
  and a `confirmed` `dir: long` entry **closes SHORT on ONDO** for the fifteen days
  ending 2026-10-20. That is a production verdict change and it is the outcome this
  report deliberately did not reach on its own authority.
- **`comments_close_on` is a comment-period deadline, not a rule adoption.** The
  Federal Register document confirms the date; whether an SEC comment deadline is an
  event that "resolves" on that date, and whether it is mechanically `long` for ONDO
  rather than an opinion about the outcome, is a methodology question. The bench's own
  editing rules say "Anything requiring an opinion about the OUTCOME does not belong in
  the registry at all." Raised, not acted on — the direction is the Architect's.
- **The map's `## 0` gate figures are now one revision behind.** Steps 1–12 read
  1 250 693 and all 13 read 1 250 733 on this branch. The map still states 1 250 677
  and 1 250 717. That is expected for an unmerged branch and is named here so the next
  TZ header quotes the right numbers after the merge.

## Commit

`fe2660f` — `feat(catalysts): register Sept-Oct dated events, add federalregister.gov to PRIMARY (TZ-20)`

The message is TZ §5's string verbatim. Two files, 29 insertions, 4 deletions. The
working tree was left clean: the scratch gate harness was written to `bench/_gate.sh`,
which `.gitignore` already covers under `bench/_*`, and was removed before the commit.

## Pull Request

**No pull request exists.** This environment has no `gh` CLI and the GitHub MCP server
is unauthenticated in a non-interactive session, so one could not be opened. Per §8
this is the defined fallback, not a blocker.

- Branch: **`claude/tz-20-catalyst-registry-content`** (pushed, tracking `origin`)
- Compare URL: **https://github.com/seahomebatumi-ai/crypto-auto/compare/main...claude/tz-20-catalyst-registry-content**

The Boss opens and merges from that link in one action, after the Architect's verdict.

## CI Execution

**The hosted gate ran, on the runner, on this exact head.** The `Bench gate` workflow
fires on push to `claude/**` (§9), so the branch has runner evidence with no pull
request open.

- Workflow: `Bench gate` (`.github/workflows/bench.yml`)
- Run id: **`33309297352`**
- Head SHA: **`fe2660fe0c3205f59f5c630490247e58b5a445e2`**
- Status / conclusion: **completed / success**
- Job: `bench` → success —
  https://github.com/seahomebatumi-ai/crypto-auto/actions/runs/33309297352/job/99251321396

All **13 bench steps** reported `success` individually, in workflow order, plus the
dependency-install step. No step was skipped and none was `continue-on-error`.

`backtest_bench.yml`, `calib.yml` and `journal.yml` did **not** run: none is triggered
by a push to `claude/**` and none was touched. `.github/workflows/backtest_bench.yml`
was not modified (hard floor item 8).

The check counts in Test Results are from the **local** replay; the runner is the
authority on green/red, and it is green. The two agree on the one step that matters:
`catalyst_bench.js` is `success` on the runner and 23 056 checks with 0 failures
locally.

## Final Repository State

**§8's two preconditions for a direct push to `main` were verified, not assumed.**
Pages serves `index.html`, so nothing under `CryptoReports/**` can reach the live
calculator; and `.github/workflows/main.yml` carries `'**.md'` in its `paths-ignore`
for `push` on `main`, so this report cannot start the bot. Both hold, so the report
was pushed directly to `main` as §4a step 10 requires.

- `main` carries this report and nothing else from this task.
- `claude/tz-20-catalyst-registry-content` carries the implementation, one commit
  ahead of `main`, gate green on the runner.
- `catalysts.json` on `main` is still the single ZEC entry; the ENA entry is on the
  branch only.
- Nothing under `analyst/` was read or written. No production file, workflow, bench
  outside `catalyst_bench.js`, map or contract was modified.

**NOT IN EFFECT UNTIL MERGED.**

## Fingerprints

Map revision required by the TZ header: **`Revision 2026-08-30-b`**. Map revision
found in the repository: **`Revision 2026-08-30-b`**. They match, and all **seven**
content anchors the TZ header quotes were matched as exact substrings before any work
began:

| Anchor | Found |
|---|---|
| `**Revision 2026-08-30-b.**` | yes |
| `### 3.12 Direction engine — veto cascade` | yes |
| `### 3.15 Catalyst registry` | yes |
| `### 3.16 List exhaustion — the day-range measure` | yes |
| `## 11. Analytical engine` | yes |
| `### 3.17 «РИСК ВЫНОСА» — the day's own risk` | yes |
| `54. **A record cannot contain the outcome of the action that stores it.**` | yes |

Contract and methodology documents:

| File | Lines | MD5 | Version / revision |
|---|---:|---|---|
| `SYSTEM-MAP-CRYPTOCALCUL.md` | 1540 | `6b58e6ea4daaa8fd1bd3bb0ea7fbfd35` | `Revision 2026-08-30-b` |
| `EXECUTOR-INSTRUCTIONS.md` | 620 | `2cf73ab5e90741d8a094c8e1d0f8ee8a` | `Version 13` |
| `ANALYST-INSTRUCTIONS.md` | 771 | `63c15842a0d0524e4acf812966bd338d` | `Revision 2026-08-30-e` |

Files the map's `## 0` table lists, measured on the branch:

| File | Lines | MD5 | Required by §0 | Verdict |
|---|---:|---|---|---|
| `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` | 3729 / `fdf33190…` | **match** |
| `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` | 506 / `1a5a5d98…` | **match** |
| `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` | 175 / `3b8730b2…` | **match** |
| `catalysts.json` | 16 | `5c03cc936a49c90c68fe1d8e64684a1c` | 11 / `021dd2c9…` | **changed, in scope** (TZ §0) |

`catalysts.json` before the change measured 11 lines / `021dd2c90dc395240c0b0c3dbae40426`,
matching §0 exactly, so the new hash is a measured delta from a verified baseline.

File added by this TZ's scope but not in the map's `## 0` table:

| File | Lines | MD5 |
|---|---:|---|
| `bench/catalyst_bench.js` (after) | 574 | `fe5c9be2107c7aa3c7fc14f5716284e3` |
