# TZ-16 — Analyst path verification (read-only)

**Canonical filename:** `TZ-16-analyst-path-verification.md`
**Directory:** `CryptoTZ/`
**Report:** `CryptoReports/TZ-16-analyst-path-verification-report.md`
**Model:** **Opus.** Multi-file diagnosis across a workflow filter, an external data
path and an egress measurement; a wrong reading here designs the wrong architecture.

**Requires `EXECUTOR-INSTRUCTIONS.md` version 9 or later in the repository.** Under
version 8, hard floor 9 blocks any TZ asking for an in-session fetch, and this TZ is
nothing but in-session fetches. If the repository contract still reads **Version 8**,
report BLOCKED naming that and stop — the Boss uploads v9 and re-triggers.

**This TZ writes no code.** It measures, and it reports. Nothing is created, nothing
is modified, no branch, no pull request. It supersedes the unexecuted draft
`TZ-16-analyst-engine-transfer.md`; if that draft was uploaded to `CryptoTZ/`, leave
it in place as evidence and record the fact under `## Inbound Filing` — a
specification that never ran is evidence, not a pending task (contract §13).

---

## 0. Required System Map fingerprint — quoted IN FULL

**Revision 2026-08-28-a.** Baseline: TZ-15 merged into `main`; implementation
commit `c8be42b`, report `CryptoReports/TZ-15-caption-truth-report.md`. **The
baseline names the implementation commit, not the merge commit** — a merge commit
carries no content, and content is what this block pins.

Every TZ header quotes this block IN FULL — all six anchors and the file table,
never a subset. The Executor matches each anchor as an exact substring against the
repository copy before any work (contract §5); any mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-28-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `50. **A stated absence is a dependency of the thing it denies.**` |

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

Gate at this revision: `bench.yml`, **12 steps, 1 250 677 checks**, green on the
hosted runner (run `32780919062`, head `c8be42b`, all 12 steps `success`). The
number is a sum of per-comparison counters (inv. 43), never an estimate, and every
delta between revisions is attributed term by term. TZ-15 moved exactly one step:
12 (`exhaustion_bench.js`) 220 534 → 220 598, **+64**, one new section `caption`
(M1–M5); all fourteen pre-existing counters of that bench and all of steps 1–11 are
unmoved, which for a change touching one display string, one comment and one bench
is the required result rather than a pleasant one.

**Step 7 (`journal_bench.js`) moves with verdict CONTENT, not only with control
volume.** It counts numeric leaves of the records it writes, and a verdict that
returns before geometry writes no `geo` object, so a change in verdicts moves it
without moving a single control. A fall in step 7 is attributed, never assumed
benign, because a defect that nulls a field lowers it identically. Held at
**691 109** through TZ-13, TZ-14 and TZ-15.

---

## 1. Why this TZ exists

The analyst engine is specified against three beliefs, none of which has been
measured in the environment where the engine would run:

1. that this session can read the live Binance Futures snapshot the Boss's existing
   automation already produces;
2. that writing `analyst/**` to `main` cannot start the bot or touch the live
   calculator;
3. that this session reaches any market host at all — inv. 44 says an Executor
   session's egress refuses every one of them.

**If belief 3 is false in this environment, there is no analyst engine on any path**,
and everything downstream is wasted work. Measuring first costs one session. Building
first costs the build plus the rebuild.

**The existing pipeline is reused if it is capable.** The Boss's iOS Shortcut already
collects Binance Futures data from his own network and PATCHes it to a Gist. A second
price-delivery mechanism is not built unless this TZ proves that path technically
incapable of feeding the engine. Report what you measure; propose nothing.

---

## 2. Stage A — egress measurement

For each host below: one request, connect timeout 5 s, total timeout 10 s, **no
retry loop**. Record the HTTP status or the exact transport error, and the wall time.

| # | Host / URL | What a success proves |
|---|---|---|
| A1 | `https://fapi.binance.com/fapi/v1/time` | Binance Futures reachable — rung 1 exists |
| A2 | `https://fapi.binance.com/fapi/v1/ticker/24hr?symbol=BTCUSDT` | the ticker itself, not just the host |
| A3 | `https://fapi.binance.com/fapi/v1/premiumIndex?symbol=BTCUSDT` | funding reachable |
| A4 | `https://api.github.com/gists/<LIVE_GIST_ID>` | the Gist API answers this client |
| A5 | the Gist's `raw_url` for `live.json`, taken from A4's response | the payload is readable |
| A6 | `https://data-api.binance.vision/api/v3/time` | the mirror inv. 24 already allows |
| A7 | `https://api.coingecko.com/api/v3/ping` | breadth of the refusal, if there is one |

`<LIVE_GIST_ID>` is supplied by the Boss in the trigger message as the only argument
this TZ takes. If it is absent, report BLOCKED and ask for that one value in one line
— it is a routing datum, not a technical question.

**A4 and A5 are the load-bearing pair.** A4 may require a token; if it fails
unauthenticated, retry once with `GITHUB_TOKEN` or `gh api` and say which worked. A5
matters more than A4: the engine needs the file, not the API.

**Report the refusal shape, not a summary.** «Refused» is not a measurement — HTTP
451, HTTP 403, DNS failure, TLS reset and a proxy CONNECT rejection are five different
architectures and only the exact string distinguishes them.

---

## 3. Stage B — freshness and schema of the existing payload

Only if A5 succeeded. Run **twice, at least three minutes apart**, and report both.

1. Full `live.json` byte size, and the top-level shape: outer container (`[]` or
   `{}`), key names, whether values are strings or numbers.
2. The timestamp field: its name, its format, its value, and the age in seconds
   against `date -u` at the moment of each fetch.
3. The symbol count, and the exact set difference against `tokens[]` cut from
   `index.html` at run time — **never against a list typed into this TZ** (inv. 21).
4. Which metrics are present per symbol: last price, 24 h high, 24 h low, volume,
   funding rate, open interest. Name what is missing.
5. **The two-fetch comparison is the whole point of running it twice.** If the second
   fetch returns a byte-identical body with an identical `ts`, the address is frozen
   for this client and the payload is stale by construction, not intermittently — the
   same failure the Architect's chat client measured on 2026-08-28. Report the
   `etag`, `last-modified` and any `x-request-id` or `cf-cache-status` header from
   both fetches; identical request ids across three minutes is the proof.

**Do not judge whether the path is «good enough».** Report the numbers; the Architect
decides.

---

## 4. Stage C — write-path safety

Read-only inspection of the repository, no edits.

1. `.github/workflows/main.yml` — quote its `on:` block verbatim, in particular
   `push.paths` and `push.paths-ignore`. State plainly whether a commit touching
   `analyst/state.json` would start the bot. `**/*.md` does not cover a `.json` file.
2. Every other workflow with a `push` trigger on `main`: name it, quote its filter,
   and state whether `analyst/**` would fire it. `bench.yml` and `journal.yml` at
   minimum.
3. GitHub Pages: confirm from the repository what it serves and from which branch and
   directory, and state whether anything under `analyst/` could be published.
4. Confirm this session can push directly to `main` at all — report the observed
   permission, without pushing anything.

---

## 5. Stage D — contract and methodology consistency

Read-only. Report findings; change nothing.

1. Confirm `ANALYST-INSTRUCTIONS.md` is present at the repository root; record its
   line count and MD5. If it is absent, say so — that is a Boss upload, not a defect.
2. Confirm `EXECUTOR-INSTRUCTIONS.md` reads **Version 9**; record line count and MD5.
3. **Duplication scan.** Name any rule that appears in more than one of: this
   contract, `ANALYST-INSTRUCTIONS.md`, the map. Report the pairs; resolve nothing.
4. **Contradiction scan.** Name any clause of the contract that an analysis run
   would have to violate to follow `ANALYST-INSTRUCTIONS.md`, and any clause of
   `ANALYST-INSTRUCTIONS.md` that the contract forbids. Quote both sides.
5. Confirm `analyst/` does not already exist in the repository on any branch.

---

## 6. Validation

1. Every request in Stage A attempted, with status or transport error and wall time.
2. Stage B run twice with the interval stated, both bodies compared, headers quoted.
3. Every workflow with a `push` trigger enumerated — the count is stated, so an
   omission is visible.
4. `tokens[]` cut from `index.html` at run time, its length reported, and the set
   difference computed against the live payload rather than described.
5. `git status` clean at the end; `git diff --stat` empty. **A verification TZ that
   changed a file has failed** whatever else it found.
6. Fingerprints per contract §10 for the map and the four files in §0.

---

## 7. What the report must make decidable

The Architect must be able to answer these four from the report alone, with no
further questions:

1. Can an analysis run in this environment obtain a Binance Futures price at all,
   and by which route?
2. Is the existing `live.json` path capable — fresh, complete, and readable on
   demand — or is it frozen for this client?
3. Is `analyst/**` safe to commit to `main` as it stands, or does a filter need one
   line first?
4. Does the integrated contract contradict the methodology anywhere?

**No recommendation, no architecture, no proposal.** This TZ measures. The next TZ
builds, or the transfer is refused on the evidence.

---

## 8. Deliberately not in scope

`[решение принято мной]`

- **No `analyst/` tree, no gate script, no state file, no `bench.yml` step.** Those
  were the draft TZ-16; they wait for this measurement. Building a fallback ladder
  before knowing which rungs exist is how a second price-delivery mechanism gets
  built for no reason.
- **No change to any workflow filter,** even if Stage C proves one is needed. That
  is a one-line change with a live-calculator blast radius and it belongs in a TZ
  that says so.
- **No first analysis run.** Building the engine and exercising it are two acts; a
  first run inside a verification session would write a state file nobody audited.
