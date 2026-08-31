# TZ-23 — `main.yml` paths allow-list

**Canonical path:** `CryptoTZ/TZ-23-main-workflow-paths-allowlist.md`

**Class: branch TZ** (contract §8, v15). It writes one file outside `CryptoReports/**`,
so it opens a branch and a pull request, and the report carries the merge sentence.

**Model:** Opus · High · no Web. A filter that is too narrow stops the bot and lets
`coeffs.json` age with nothing on screen to say so — a silent-failure risk, not a
mechanical YAML edit.

---

## 0. System Map fingerprint gate — blocking

The map's `## 0. Fingerprint` block, quoted in full. Match every anchor as an exact
substring against the repository copy before any work (contract §5). Any mismatch is
BLOCKED.

> **Revision 2026-08-30-f.** Baseline: TZ-21 merged into `main`; implementation
> commit `8069341`, merge commit `edd650c`, report
> `CryptoReports/TZ-21-catalyst-registry-scope-and-basis-report.md`. **The
> baseline names the implementation commit, not the merge commit** — a merge commit
> carries no content, and content is what this block pins.
>
> **`-d`, `-e` and `-f` are documentation revisions and the baseline deliberately did not move.**
> TZ-22 measured a network and wrote one report; no production file, no bench, no
> workflow and no constant changed, so the file table, the gate and the check count
> below are `-c`'s unaltered. `-d` moved because §10 and §11 now record a measurement that
> `-c` denied having, and a TZ cut against the denial must BLOCK rather than proceed on it
> (inv. 50). `-e` moved because §10 named a TZ number for a repair that is not a TZ:
> `EXECUTOR-INSTRUCTIONS.md` is Architect-owned and arrives by Boss upload, so it became
> contract **v15** instead, and a row pointing at a TZ that will never exist would have
> failed the audit's own set-difference check between `CryptoTZ/` and `CryptoReports/`.
> `-f` moved because TZ-24 closed the §6a discovery question in the negative, and §10 and §11
> carried it as open.
>
> Every TZ header quotes this block IN FULL — all seven anchors and the file table,
> never a subset. The Executor matches each anchor as an exact substring against the
> repository copy before any work (contract §5); any mismatch is BLOCKED.
>
> | Anchor | Exact string that must be present |
> |---|---|
> | revision | `**Revision 2026-08-30-f.**` |
> | direction engine | `### 3.12 Direction engine — veto cascade` |
> | catalyst registry | `### 3.15 Catalyst registry` |
> | exhaustion measure | `### 3.16 List exhaustion — the day-range measure` |
> | analytical engine | `## 11. Analytical engine` |
> | squeeze block | `### 3.17 «РИСК ВЫНОСА» — the day's own risk` |
> | newest invariant | `55. **A specification is checked against the text it must obey, never against memory of it.**` |
>
> Live files at this revision — the set every TZ header and every report fingerprints:
>
> | File | Lines | MD5 |
> |---|---:|---|
> | `index.html` | 3729 | `fdf331906bf205944b25e3635135789c` |
> | `main.py` | 506 | `1a5a5d98b2fd76010f202ee3eebaa717` |
> | `catalysts.json` | 17 | `f9b2dd4a3594134b2b7b603de19075c3` |
> | `bench/exhaustion-calibration.txt` | 175 | `3b8730b254467c9df4c0a845a0f3cfb3` |

**Second gate — contract v15.** Confirm `EXECUTOR-INSTRUCTIONS.md` reads `**Version 15.**`
and that §8 names the two TZ classes. This TZ is the **branch** class.

---

## 1. Why this TZ exists

`main.yml` filters `push` with `paths-ignore` and no `paths` allow-list, so **every path
nobody thought to name starts the bot** — 28 CoinGecko `/market_chart` calls plus one
`/coins/markets` call, and a rewrite of the live Gist. Measured live: the TZ-21 merge
started `Crypto Update` #1492 on a commit touching `catalysts.json` and a bench file,
neither of which the bot reads.

That direction is only wasteful. **The direction that matters is the reverse** — a filter
so narrow the bot stops and `coeffs.json` ages with nothing on screen saying why — and
every stage below is shaped by which of the two errors it is guarding against.

The list to be replaced, verbatim from the repository:

```yaml
  push:
    branches: [ main ]
    paths-ignore:
      - 'bench/**'
      - '**.md'
      - 'index.html'
      - '.github/workflows/bench.yml'
      - '.github/workflows/backtest_bench.yml'
      - 'analyst/**'
  workflow_dispatch:
```

`catalysts.json`, `journal/**`, `.github/workflows/journal.yml`, `.github/workflows/calib.yml`
and every future path are absent from it, and each therefore fires the bot.

**`paths` and `paths-ignore` cannot coexist on one event**, so adopting the allow-list
DELETES the ignore list rather than joining it. That is the point of the change and not a
side effect: an allow-list needs no exclusions, because everything unnamed is already out.

---

## 2. Scope

**Files to modify:** `.github/workflows/main.yml` — the `on.push` block only.

**Files to create:** `CryptoReports/TZ-23-main-workflow-paths-allowlist-report.md`
**Files to delete:** none.

Nothing else. No `jobs:` step, no `main.py`, no bench, no other workflow, no production
file, nothing under `analyst/`. `workflow_dispatch` is not touched (§4).

---

## 3. Stages

### 3.1 Derive the bot's repository read set from `main.py` — do not accept it from this TZ

The allow-list must name every repository path a change to which should re-run the bot.
**That set is derived from the source at execution time, never typed from a specification**
(inv. 21 applied to a filter, inv. 55 to its author).

Search `main.py` for every filesystem read — `open(`, `Path(`, `json.load`, `read_text`,
`os.environ` pointing at a path, `__file__`-relative access, any import of a repository
module — and report what is found, with line numbers, including the empty result.

- **If the bot reads no repository file**, the set is `main.py` (itself) and
  `.github/workflows/main.yml` (its own trigger and job definition), and nothing else.
- **If it reads one**, that path joins the allow-list and the report names the line that
  proves it.

**A path is added on evidence from `main.py`, never on plausibility.** `catalysts.json`
looks like bot input and is not: §1 of the map gives it to the frontend over XHR, and
`main.py`'s absence from that lane is the thing to confirm rather than assume.

### 3.2 Write the filter with literal paths and no glob

Replace the `paths-ignore:` list with `paths:` carrying the §3.1 set. **Every entry is a
literal path with no wildcard.**

This is deliberate and it is the reason inv. 52's failure mode does not arise here: a glob
is a hypothesis about a third party's matcher, a literal path is not. If §3.1 returns a
path that cannot be written literally, stop and report it rather than inventing a pattern.

`branches: [ main ]` stays exactly as it is. `workflow_dispatch:` stays exactly as it is,
on its own line, unfiltered.

### 3.3 Carry the reasoning across — the comments are the record

The block being deleted carries two Russian comment blocks: the cron history, and why the
frontend and benches do not start the bot. **The cron comment is untouched** — it sits
above `push:` and explains the absence of a schedule, which this TZ does not change.

The second comment explains an ignore list that will no longer exist. Rewrite it for the
allow-list, **in Russian** (the standing workflow-comment exception, CANON Language), and
state three things:

1. what the bot reads, and that the list is derived from `main.py` rather than chosen;
2. that `workflow_dispatch` is unfiltered, so the phone's 17 daily runs are outside this
   filter entirely and cannot be stopped by it;
3. **the coupling, named as a coupling:** an allow-list must GROW whenever the bot gains a
   new input, and a forgotten entry stops the bot silently. This is inv. 53's shape with
   its sign reversed — there a forgotten entry burned runner minutes loudly, here it
   withholds a run quietly, which is the worse direction and the reason the comment exists.

### 3.4 Evaluate the filter against real changed-file lists — both directions

Runner history cannot settle this one: `main.yml`'s `push` trigger is `branches: [ main ]`,
so a `claude/**` branch push does not exercise it at all, and the session holds no GitHub
API access to read Actions history (map §10). Inv. 52's second method therefore applies —
evaluation against a changed-file list taken from `git diff --name-only`, never typed.

Build the list from **real commits already in this repository's history**, and evaluate
each against the new `paths` block and against the old `paths-ignore` block:

| Row | Changed-file list from | Old behaviour | New behaviour required |
|---|---|---|---|
| must fire | a commit touching `main.py` | fires | **fires** |
| must fire | a commit touching `.github/workflows/main.yml` | fires | **fires** |
| must not fire | the TZ-21 merge (`catalysts.json` + bench) | **fires — the defect** | does not fire |
| must not fire | a commit touching `index.html` only | does not fire | does not fire |
| must not fire | a commit touching `CryptoReports/**` only | does not fire | does not fire |
| must not fire | a commit touching `analyst/**` only | does not fire | does not fire |

**The two must-fire rows are the control and they are not optional.** A filter that
matches nothing passes every must-not-fire row perfectly, so a table without them proves
that the bot is quiet and nothing else (inv. 52).

Report each row as: commit, its `git diff --name-only` output, the evaluation, and the
verdict. State the matcher used and that it is a local reading of GitHub's semantics —
which is why §3.2 avoids globs and why §5 item 7 puts the final proof on the runner.

### 3.5 What this TZ does NOT do

The bot's own run is unchanged: same `jobs:`, same Python, same retry, same
`GIST_TOKEN`. No CoinGecko call count moves. `bench.yml` is not edited — its
`paths-ignore` has an allow-list question of its own and it is not this TZ's.

---

## 4. `workflow_dispatch` is the safety argument and must be verified, not assumed

**All 17 daily runs are `workflow_dispatch` from the Boss's iPhone Shortcut** (map §1:
schedule is not cron). `paths` filters `push` only and has no effect on
`workflow_dispatch`, so the hourly tempo cannot be broken by any list this TZ writes.

Confirm in the report that `workflow_dispatch:` is present, unindented under `on:`, and
carries no filter of any kind after the edit. **This is the single check that separates
"the bot skips a commit it did not need" from "the bot stopped".**

---

## 5. Validation — written by the Architect

1. `python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/main.yml'))"` parses
   without error, and the parsed `on.push` carries `paths` and **no** `paths-ignore`.
2. §3.1's derivation is reported with line numbers from `main.py`, including a nil result
   stated as nil.
3. Every `paths` entry is literal — the report shows a wildcard count of zero.
4. §3.4's table is complete, with both must-fire rows, each list produced by
   `git diff --name-only` against a named commit and never typed.
5. `workflow_dispatch` verified per §4.
6. The Russian comment carries all three clauses of §3.3, and the cron comment above
   `push:` is byte-identical to its current text.
7. **`git diff` on the branch touches exactly one file and only its `on.push` block.** The
   `jobs:` section is byte-identical — show this as a diff hunk count, not as a claim.
8. **No-regression on the gate.** The branch push starts `Bench gate` (`bench.yml` fires on
   `claude/**` and its `paths-ignore` does not cover `.github/workflows/main.yml`). It must
   be green at **13 steps, 1 250 739 checks** — unmoved, because no production file, bench
   or constant changed. A moved count on this TZ is a defect, not a bonus.
9. `python3 -m py_compile main.py` and `node --check` on the extracted `<script>` are run
   as the standing checks and must pass; neither file is edited, so a failure means the
   branch is not clean.

**Predicted live behaviour, so it is not misread after the merge.** The merge commit
changes `.github/workflows/main.yml`, which is IN the allow-list, so it will start
`Crypto Update` exactly once. That run is the must-fire control firing for real and it is
the expected result, not a leak through the new filter.

---

## 6. Post-merge evidence — the audit reads it, the Executor does not claim it

The session cannot start Actions and must not pretend otherwise (contract §9). The two
readings that settle this change are taken from the Actions page after the merge:

- the merge commit produced one `Crypto Update` run — the must-fire direction, live;
- the next push touching only `.md` or `catalysts.json` produced none — the must-not-fire
  direction, live.

The report states these as pending, never as observed.

---

## 7. Documentation dependency — recorded, not repaired here

Two places in the map assert the absence this TZ removes, and both turn false on merge
(inv. 50):

- §10, row `main.yml has no paths allow-list`;
- §11, last line: `main.yml still has no paths allow-list, only paths-ignore, so every
  path nobody named fires it (inv. 52).`

Inv. 52's own closing sentence names the same shape. **The map is Architect-owned and
arrives by Boss upload (contract §2), so the Executor neither edits it nor is asked to.**
The report lists these three sites so the Architect's post-merge edit cannot forget one.

---

## 8. Commit and pull request

Branch: `claude/tz-23-main-workflow-paths-allowlist`.

```
ci(main): replace paths-ignore with a derived literal paths allow-list (TZ-23)
```

Report goes direct to `main` per contract §8; the implementation waits on the branch until
the Boss merges after the audit verdict.
