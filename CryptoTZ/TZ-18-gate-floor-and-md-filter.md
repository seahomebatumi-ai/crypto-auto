# TZ-18 — Gate freshness floor and the root-Markdown filter

**Canonical filename:** `TZ-18-gate-floor-and-md-filter.md`
**Directory:** `CryptoTZ/`
**Report:** `CryptoReports/TZ-18-gate-floor-and-md-filter-report.md`
**Model:** **Sonnet.** Two single-line changes with fixed semantics and an existing
selftest to extend; no math, no architecture, no diagnosis.

**Predecessor:** `CryptoReports/TZ-17-analyst-engine-build-report.md`, ПРИНЯТО and
merged. Both defects below are **defects of TZ-17's specification, not of its
implementation** — the Executor implemented each exactly as written and flagged both
under `## Remaining Risks`. Nothing built by TZ-17 is being reworked.

**Requires `EXECUTOR-INSTRUCTIONS.md` version 10 or later.**

---

## 0. Required System Map fingerprint — quoted IN FULL

**Revision 2026-08-29-a.** Baseline: TZ-17 merged into `main`; implementation
commit `850e263`, report `CryptoReports/TZ-17-analyst-engine-build-report.md`. **The
baseline names the implementation commit, not the merge commit** — a merge commit
carries no content, and content is what this block pins.

Every TZ header quotes this block IN FULL — all seven anchors and the file table,
never a subset. The Executor matches each anchor as an exact substring against the
repository copy before any work (contract §5); any mismatch is BLOCKED.

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-08-29-a.**` |
| direction engine | `### 3.12 Direction engine — veto cascade` |
| catalyst registry | `### 3.15 Catalyst registry` |
| exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
| analytical engine | `## 11. Analytical engine` |
| squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
| newest invariant | `52. **A deny-list filter is proven against real paths, never against its own intent.**` |

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

Gate at this revision: `bench.yml`, **13 steps, 1 250 712 checks**, green on the
hosted runner (run `33241068850`, head `850e263`, all 13 steps `success`). The number
is a sum of per-comparison counters (inv. 43), never an estimate, and every delta
between revisions is attributed term by term. TZ-17 added step 13
(`analyst/live-gate.sh --selftest`, **35**) and moved steps 1–12 by exactly zero.

**Step 7 (`journal_bench.js`) moves with verdict CONTENT, not only with control
volume.** It counts numeric leaves of the records it writes, and a verdict that
returns before geometry writes no `geo` object, so a change in verdicts moves it
without moving a single control. A fall in step 7 is attributed, never assumed
benign, because a defect that nulls a field lowers it identically. Held at
**691 109** through TZ-13, TZ-14, TZ-15 and TZ-17.

**This TZ modifies none of the four files above.** Their hashes must be identical in
the report; a diff on any of them is a scope violation and the TZ is rejected whole.

---

## 1. Scope

Two corrections. Nothing else, however obviously beneficial.

| Path | Change |
|---|---|
| `analyst/live-gate.sh` | check 3 becomes a two-sided window; new constant; two new selftest cases |
| `.github/workflows/main.yml` | `'**/*.md'` → `'**.md'` |
| `.github/workflows/bench.yml` | add `'**.md'` to `push.paths-ignore`; step 13's `checks=N` moves |

**Files to Delete:** none.

---

## 2. Change A — the freshness window gets a floor (inv. 51)

TZ-17 fixed check 3 as `now − ts ≤ 900`. **That inequality is satisfied by every
payload timestamped in the future**, so a producer whose clock runs ahead delivers a
stale snapshot that the gate reports as fresh — the exact failure the gate exists to
prevent, arriving through the gate itself. The producer is an iPhone writing an
ISO-8601 stamp with a `+04:00` offset and the reader is a different machine; the two
clocks are independent and a hard zero would refuse healthy data whenever they
disagree by a second.

```
LIVE_MAX_AGE_SEC = 900       existing ceiling, unchanged
LIVE_SKEW_SEC    = 120       new floor: how far ahead the producer may plausibly be

check 3 passes  ⇔  −LIVE_SKEW_SEC ≤ (now − ts) ≤ LIVE_MAX_AGE_SEC
```

- Both numbers are **named constants declared once** in the script (inv. 20). No
  literal `900` and no literal `120` may appear at a comparison site.
- The failure exit stays **3** in both directions — a caller needs «this payload is
  not usable as now», and splitting it would create a class no caller distinguishes.
- The stderr line must say **which** side failed, in the same one-line form the other
  checks use, so the day log records «stale» and «ahead» as different observations
  even though the exit code is one.
- `age_sec` in the success payload keeps its current sign convention: negative when
  the producer is ahead. It is a measurement and is not clamped.

**Why 120 s and not 5 s or 600 s.** `[решение принято мной]` A phone that has not
synced NTP for a day drifts seconds, not minutes; 120 s covers ordinary skew and a
manual timezone slip of far less than one hour, while staying an order of magnitude
below the 900 s ceiling so the window cannot be widened into meaninglessness from the
floor end. Rejected: making the floor equal to the ceiling, which is symmetric and
therefore tidy, and which would accept a payload written fifteen minutes in the
future as a current price.

### New selftest cases — both mandatory

```
ts 121 s in the future     -> 3     the floor rejects
ts  60 s in the future     -> 0     ordinary skew is accepted
```

They are added to the existing `--selftest` table and generated the same way as every
other fixture, from the live `tokens[]` parse. Nothing else in the selftest changes.

**The second case is the load-bearing one.** A floor that rejected all future stamps
would pass a test suite containing only the first, and would then refuse a healthy
payload every time the phone was a second ahead. A control that only proves the
prohibition proves half the change (inv. 23).

---

## 3. Change B — `'**.md'`, so a root-level file is actually ignored (inv. 52)

`main.yml`'s `paths-ignore` carries `'**/*.md'`. That pattern contains a literal
separator and therefore matches only Markdown **inside a directory**. Every
root-level `.md` in this repository — `SYSTEM-MAP-CRYPTOCALCUL.md`,
`EXECUTOR-INSTRUCTIONS.md`, `ANALYST-INSTRUCTIONS.md`, `README.md` — is unmatched, so
**each upload of the map or a contract starts the bot**: `main.py` with `GIST_TOKEN`,
rewriting the live Gist, with the retry that doubles the CoinGecko draw against the
~21.6k monthly budget the workflow's own comment names.

TZ-17 §Risk 5 named this ambiguity and correctly declined to act on it, because
nothing in that change depended on it. It is settled here.

1. `main.yml`: replace `- '**/*.md'` with `- '**.md'`. One line, same list, same
   position. Leave every other entry, comment and line untouched.
2. `bench.yml`: add `- '**.md'` to `push.paths-ignore`. The gate reads
   `index.html`, `main.py` and `bench/**`, none of which is Markdown, so a
   documentation-only push proves nothing and costs runner minutes on every report,
   TZ and contract upload. **A mixed commit still runs both workflows** — GitHub skips
   only when *every* changed file matches an ignore pattern — and that property must
   appear in the control table below rather than be assumed.

### Negative test, mandatory (contract §9, inv. 52)

Not a live run: a filter evaluation, against a changed-file list taken from
`git diff --name-only` and never typed, in **both** directions, for **both**
workflows. Reuse the evaluator TZ-17 built and cross-check the decisive patterns
against a second matcher as that report did.

| Changed files | `main.yml` before | `main.yml` after | Why the row exists |
|---|---|---|---|
| `README.md` | RUNS | must NOT run | the defect itself |
| `ANALYST-INSTRUCTIONS.md` | RUNS | must NOT run | the Boss's actual upload |
| `CryptoReports/x-report.md` | must NOT run | must NOT run | the old pattern's only correct case still holds |
| `analyst/state.json` | must NOT run | must NOT run | TZ-17's fix is not disturbed |
| `main.py` | RUNS | must **RUN** | the control: a filter matching everything also passes the rows above |
| `README.md` + `main.py` | RUNS | must **RUN** | a mixed commit is not silently swallowed |

The same six rows for `bench.yml`, whose expected column differs: it triggers on
`main` **and** `claude/**`, and its ignore list is the three `journal/` paths plus
`analyst/**` plus the new `'**.md'`.

---

## 4. Validation — written by the Architect

1. `bash -n analyst/live-gate.sh` — clean.
2. `--selftest` exits 0; report `checks=N`; **N must exceed 35**, and the delta is
   attributed term by term against TZ-17's 35 (inv. 43).
3. **Negative control on the selftest** (inv. 23): invert the expected exit of the
   new `future_ok` case, confirm `--selftest` exits non-zero and names it, restore,
   confirm the file is byte-identical.
4. Direct control at the real entry point, payload placed outside the repository
   tree: `ts` at +60 s → exit 0 with a well-formed stdout object; `ts` at +121 s →
   exit 3 with **empty stdout** and a stderr line naming the floor; `ts` at −16 min →
   exit 3 with a stderr line naming the ceiling. Quote all three stderr lines: they
   must be distinguishable.
5. Confirm `900` and `120` appear at exactly one declaration site each and at no
   comparison site (inv. 20). State how the check was performed.
6. Change-B negative test per §3, both workflows, all six rows each, both directions,
   with the second matcher's agreement on the decisive pattern.
7. `git diff --stat` — exactly the three files in §1, and the two workflow diffs are
   one line each plus, for `bench.yml`, the step-13 counter having moved nowhere in
   the YAML.
8. Full `bench.yml` gate on the runner, 13 steps, per-step counter table. **Steps
   1–12 must be identical to 1 250 677 in total**, step 7 at 691 109, step 12 at
   220 598. Step 13 moves and that movement is the whole delta.
9. MD5 and line counts for the four files in §0 — identical to §0.
10. MD5 and line counts for `SYSTEM-MAP-CRYPTOCALCUL.md`, `EXECUTOR-INSTRUCTIONS.md`
    and `ANALYST-INSTRUCTIONS.md`, with revision and version strings.

**Do not run an analysis**, and do not create `analyst/live.json`. The engine still
has no producer; that is the Boss's Shortcut change and it is not this TZ.

---

## 5. Commit Message

```
fix(analyst): two-sided freshness window and root-level md filter (TZ-18)
```

---

## 6. Acceptance criteria

1. A payload 121 s in the future exits 3; a payload 60 s in the future exits 0.
2. Ceiling and floor failures are distinguishable in stderr and share exit 3.
3. `900` and `120` each have exactly one declaration site and no comparison-site
   literal.
4. `README.md` alone does not start `main.yml`; `main.py` alone still does.
5. `analyst/state.json` alone still starts neither workflow.
6. Steps 1–12 of the gate unmoved; step 13's delta attributed.
7. Only the three files in §1 changed.

---

## 7. Deliberately not built

`[решение принято мной]`

- **No `shellcheck` step in `bench.yml`.** The TZ-17 report proposed one because the
  binary was absent from that session. The control that matters for this script is the
  known-answer selftest, which tests behaviour; a linter tests style and would make the
  gate depend on a tool whose availability has already proven to vary. Rejected;
  `bash -n` stays.
- **No `paths` allow-list added to `main.yml`.** Converting a deny-list to an
  allow-list changes which pushes start the bot for every path in the repository at
  once, and it belongs in a TZ that enumerates them. The shape is recorded in inv. 52
  and in the open queue; this TZ closes the one path that is provably wrong.
- **No split of exit 3 into two codes.** No caller distinguishes «too old» from «too
  new»: both mean the payload is not usable as now, and a new exit class with no
  consumer is a number that will eventually be handled inconsistently.
