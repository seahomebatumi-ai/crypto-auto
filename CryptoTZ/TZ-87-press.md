# TZ-87 — the press: the run's numbers in code before the model, its record and its spend on main

**Contract:** v34 — `EXECUTOR-INSTRUCTIONS.md` at the repository root, read in full before the sections below.
**Canonical filename:** `CryptoTZ/TZ-87-press.md`
**Report:** `CryptoReports/TZ-87-press-report.md`
**Class:** branch TZ (contract §8) — it authorises five repository files besides its report, and block C's two probe
commits on its own branch.
**Branch:** `claude/tz-87-press`
**Host:** the VPS — R1 exists only there.
**Model:** Sonnet 5.5 · medium — the code is §6's patch, written and run by the Architect; the session applies it, runs
the checks, takes one reading and one runner proof, and judges nothing.
**Base:** `main` at `781af28` with this delivery's uploads — contract v34 and the map `2026-11-27-a`; `9b55461` carries
the same bytes of every file the patch reads.
**Rests on:** map §10 rows «The run spends its account on reading», «A run rewrites its own programs» and «The gate's
hundred trades are out of reach of the presses», and §11's sixth and seventh paths; contract §2's rows «Press record»
and «Score record», §8, §7 items 6 and 14 and §7b item 15; inv. 21, 38, 54, 55 and 73.
**Previous TZ:** TZ-86, merged at `781af28`.
**Trigger:** `EXECUTE TZ-87`, with nothing under it: no credential arrives and the Boss is asked for nothing.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-27-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-27-a.**` |
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
| `vps/run.py` | 413 | `b0b9c65152b9ae7eefc018016175ba4d` | equal — §6's patch is written against these bytes |
| `vps/selftest.py` | 4943 | `feec4dc6994c4573d1ff7e2012c373b2` | equal — the same |
| `analyst/README.md` | 15 | `f99d04e180126a7cd520041338c74def` | equal — the same |
| `.github/workflows/bench.yml` | 157 | `9d8687f5277c4fb4fa8ac21076a9379c` | equal — the same |

The map itself: 2787 lines, MD5 `3566be930d0d70060e2ed74b19bb4959` — reported, not enforced.

---

## 1. Goal and scope

**The owner's task of 26.11.2026, step (2) of the build order in map §10: every number of a press computed in code
before the model starts, a script that checks the answer before it leaves, and the press's tokens in the repository.**
This TZ ships the code. The trader's reading — under 20 000 tokens, at most 15 turns — is the methodology's revision
`2026-11-27-a`, which the Architect uploads after auditing the first press record this code writes on `main` against
that run's own numbers. **Until then nothing the session runs calls the press: shadow mode.**

- **`vps/press.py --tree T`** — run by `vps/run.py` after the writer and before the session, as the unit's user and
  without the Claude login. It reads the payload, runs the gate, reads each lane once — Binance, Bybit and OKX
  derivatives, CoinGecko, the bot's structural levels in `journal/data/`, the two score ledgers and the ETF record; a
  host that refuses with 403, 418, 429 or 451 is asked nothing more that press —, cuts production's functions and
  constants out of `index.html` by name and runs them under `node` (inv. 21, 38), and writes `analyst/press/<stem>.json`,
  the record, and `<stem>.md`, the brief. A lane that fails is `unread` in the record and never stops the press, which
  prints one `press:` line.
- **`brief`, `final`, `scale`, `check`, `state` and `hunter`** — the trader's commands under the next revision: the brief
  of this payload or a fresh press; the sized cards and the head; the scale lines; the answer checked against the
  record before it leaves; `analyst/state.json` written by code alone; the hunter's prompt.
- **`vps/run.py`** — the press under `PRESS_TIMEOUT_S`; its record and brief pushed to `main` before the session
  (`analyst: press <stem>`), so the session's tree is clean and the record precedes the answer; a record that cannot be
  committed leaves the tree. After the session, the clone back on `origin/main` — a commit the session failed to push is
  logged and left, never carried — and one commit, `analyst: usage <stem>`: `<stem>-usage.json`, the session's turns,
  tokens by model and cost, and every closed trade of the two ledgers that `main` does not hold, under
  `analyst/score/cards/` and `analyst/score/held/`. A session without a press stem files its usage under its day log's
  stem, else under its own moment. A fifth summary line: `crypto-run: press_exit=… press_pushed=… record=…`. A press
  that fails or overruns starts the session all the same.
- **`bench.yml`** ignores `analyst/press/**` and `analyst/score/**`; `analyst/README.md` gains their two rows.

### Files to Create
`vps/press.py`, by §6's patch.

### Files to Modify
`vps/run.py`, `vps/selftest.py` — sections AF and AG —, `analyst/README.md` and `.github/workflows/bench.yml`, by §6's
patch and nothing else.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
R1's scratch tree at `/var/lib/cryptorun/tz87-r1`, removed after R1, and R1's one transient unit, `--wait --collect`.
No persistent unit, timer or service is started, enabled or installed (item 15): the deployer installs the merge. No
file under `/var/lib/crypto-auto/`, `/var/spool/crypto-auto/` or the run's clone `/var/lib/cryptorun/crypto-auto` is
written or removed.

### Not touched
The methodology, the map, the contract, the kit, every other file of `analyst/` and `vps/` — `book.py`, `common.py`,
`radar.py`, `score.py`, `writer.py`, `install.sh`, the units and the manifest among them —, `index.html`, `main.py`,
`catalysts.json`, the benches and every other workflow.

---

## 2. Gates fixed before the data

| # | Expectation | Derived from |
|---|---|---|
| G1 | Baseline: `selftest: sections 31 checks 914 failed 0 empty 0` | TZ-86's report, its V3 on this host; the Architect's run of `781af28` with contract v34 in the tree |
| G2 | After it: `selftest: sections 33 checks 1078 failed 0 empty 0` — `section AF: checks 153 failed 0`, `section AG: checks 11 failed 0` — and every other section's line equal to G1's log | the Architect's runs of the patched tree under Python 3.11, 3.12 and 3.13, with contract v34 and the methodology at both revisions |
| G3 | R1 exits 0 under the run unit's own `MemoryMax` and `MemorySwapMax`, inside `PRESS_TIMEOUT_S`, and prints one `press:` line | the press's peak resident set, 40 356 KiB, on the Architect's archive replay of the run of 26.11.2026 — book 31 of 31 and 22 of 22, map 181 bars —, a quarter of the unit's 160 MiB |
| G4 | The lanes that answer the VPS, the reads, the seconds, the memory peak and the brief's bytes register nothing | a reading: the press's first measurement on the machine it runs on |
| G5 | Block C: the implementation push starts `Bench gate`; neither probe push starts it | `paths-ignore`, as `bench.yml` already applies it to `analyst/paper/**`; the first push is the instrument's positive control |

**An R1 that exits otherwise is stated with its log and does not stop the push:** the code is right and the host is the
question, which the audit answers. **A G5 whose positive control shows no run is unmeasured, never met.**

---

## 3. Run order

1. **`kit open TZ-87`.** Any FAIL is BLOCKED (contract §4a step 3).
2. **Baseline:** `kit log selftest-base -- python3 vps/selftest.py` — G1.
3. **`kit stage TZ-87`**, then V1–V4 (§4), then a commit with §7's message — local, not yet pushed.
4. **R1**, below, when `systemctl is-active crypto-run.service` prints `inactive`: a run in progress is waited for, a
   minute at a time and at most thirty, and R1 skipped and said after that.
5. Push: `git push -u origin claude/tz-87-press`. Then **block C**, below.
6. A pull request titled `TZ-87: vps — the press: the run's numbers in code before the model, its record and spend on
   main`, its body naming this TZ — or contract §8's fallback.
7. `kit usage TZ-87` and `kit units`; back on step 1's checkout (contract §4a step 7); the report; `kit close TZ-87`;
   the report to `main` by `git push origin HEAD:main`; `kit clean TZ-87`; the closing message.

**R1 — one press as the run unit's user, in its sandbox and under its ceilings, on a scratch tree of the branch with the
newest payload `main` holds.** Five lines, from the repository root on the branch, as written; the report carries both
logs in full:

```
rm -rf -- /var/lib/cryptorun/tz87-r1 && install -d -m 0700 -o cryptorun -g cryptorun /var/lib/cryptorun/tz87-r1
git fetch -q origin main && git archive HEAD analyst journal/data vps index.html main.py catalysts.json ANALYST-INSTRUCTIONS.md | tar -x -C /var/lib/cryptorun/tz87-r1 && git show origin/main:analyst/live.json > /var/lib/cryptorun/tz87-r1/analyst/live.json && chown -R cryptorun:cryptorun /var/lib/cryptorun/tz87-r1
kit log press-r1 -- systemd-run --wait --collect --pipe --unit=crypto-tz87-press -p User=cryptorun -p Group=cryptorun -p SupplementaryGroups=cryptoauto -p ProtectSystem=strict -p ProtectHome=yes -p PrivateTmp=yes -p NoNewPrivileges=yes -p ReadWritePaths=/var/lib/cryptorun -p MemoryAccounting=yes -p MemoryMax=$(systemctl show -P MemoryMax crypto-run.service) -p MemorySwapMax=$(systemctl show -P MemorySwapMax crypto-run.service) -p RuntimeMaxSec=600 -p Environment=HOME=/var/lib/cryptorun -p Environment=PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 /var/lib/cryptorun/tz87-r1/vps/press.py --tree /var/lib/cryptorun/tz87-r1
kit log press-r1-brief --sh -- "ls -l /var/lib/cryptorun/tz87-r1/analyst/press && head -n 2 /var/lib/cryptorun/tz87-r1/analyst/press/*.md"
rm -rf -- /var/lib/cryptorun/tz87-r1
```

**Block C — a push carrying only `analyst/press/**` and `analyst/score/**` starts no `Bench gate`.** After step 5's
push, from the repository root:

```
mkdir -p analyst/press analyst/score && printf '{"probe": "TZ-87 block C"}\n' > analyst/press/probe.json && cp analyst/press/probe.json analyst/score/probe.json
git add analyst/press/probe.json analyst/score/probe.json && git commit -q -m "TZ-87: block C probe, a push of analyst/press and analyst/score only" && git push -q
git rm -q analyst/press/probe.json analyst/score/probe.json && git commit -q -m "TZ-87: block C probe removed" && git push -q
kit log ci-runs -- gh run list -R seahomebatumi-ai/crypto-auto --branch claude/tz-87-press --workflow bench.yml --event push --json headSha,databaseId,status,conclusion
```

The last line runs three minutes after the third push, and again at ten when the implementation commit has no run
yet. The report names the three commits and the runs listed against each.

---

## 4. Validation

- **V1.** `kit stage TZ-87` — PASS, the five files of §6's second table at their lines and SHA-256.
- **V2.** `kit log pycompile -- python3 -m py_compile vps/press.py vps/run.py vps/selftest.py` — exit 0.
- **V3.** `kit log selftest -- python3 vps/selftest.py` — exit 0 and G2; then `kit log sections --sh -- "diff <(grep
  '^section ' /tmp/kit/selftest-base.log) <(grep '^section ' /tmp/kit/selftest.log | grep -v '^section A[FG]:')"` —
  exit 0, no line.
- **V4.** `kit log bench-yml --sh -- "git diff --cached --numstat -- .github/workflows/bench.yml && git diff --cached
  -U0 -- .github/workflows/bench.yml | grep -cE \"^\+      - 'analyst/(press|score)/\*\*'$\""` — `5 0` and `2`: five
  lines added, none removed, the two paths among them.
- **V5.** R1 — G3 and G4.
- **V6.** Block C — G5.
- **V7.** `kit units` — PASS: no transient unit left; `git status --porcelain --untracked-files=no` after the commit —
  no line.
- No CI step executes `vps/selftest.py`: `## CI Execution` states what ran on a runner and its conclusion (contract §9).

---

## 5. Parameters

`PRESS_TIMEOUT_S = 600` — the run's ceiling on the press · `PRESS_S = 420` — the press's own deadline on its reads ·
`FRESH_S = 900` — how long a record is the brief of its payload · `WORKERS = 8` · `HOLD_CODES = (403, 418, 429, 451)` ·
production's functions `has`, `marketRegime`, `sigmaDay`, `lStruct` and `liqPrice` and its twelve constants, cut by
name and run once under `node` · printed numbers rounded half up on the decimal repr · the record: `v` 1, `k` `press`,
`stem`, `freeze`, `payload_ts`, `gate`, `lanes`, then the blocks the brief prints · the usage: `v` 1, `k` `usage`,
`stem`, `ts`, `model`, `effort`, `press_exit`, `press_s`, `writer_exit`, `claude_exit`, `is_error`, `num_turns`,
`duration_ms`, `answer_chars`, `log`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`,
`cost_usd`, `models` — per model `input`, `output`, `thinking`, `cache_read`, `cache_creation`, `web_searches`,
`cost_usd` —, `subtype`, `api_error_status`; never the answer · a ledger trade copied once, as written, and never
rewritten · the press's exit 0 written, 2 the payload unread.

---

## 6. Shipped

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CryptoTZ/TZ-87-press.patch` | 185906 | `a18236acb7b6ce9ddbdad80805e4b61dc5570bd41d915d4d33f0ab640a35dbdf` | apply |

| Path | Lines | SHA-256 |
|---|---:|---|
| `vps/press.py` | 1964 | `980ef0003952439231245b3f6d66cb06a794802bfe026dfd395d700e6bcd5bda` |
| `vps/run.py` | 547 | `22527db4771b945a3cac32adb9b9f40d96b4770acd526f906f5a5d0f96f44d49` |
| `vps/selftest.py` | 5707 | `04c74a27fc5a55425bc0be36bac6650d6333ad00c36fd722af30fa6099957d3e` |
| `analyst/README.md` | 17 | `797bd0968da9b40dfed6109fa146478ebc25566dde14b3eeb4cd73649809561b` |
| `.github/workflows/bench.yml` | 162 | `4eabb9973f4e99c871a71dade571a1b1f19768db544424968095b5edfb5e058a` |

---

## 7. Commit Message

```
TZ-87: vps — the press: the run's numbers in code before the model, its record and the session's spend on main
```

---

## 8. Pre-send checks

Run by the Architect before this file was sent:

- `kit caps` on this file — within 20 000 bytes.
- On a fresh clone of `main` at `9b55461` with this delivery's uploads committed to a local origin: `kit open TZ-87`
  PASS and `kit stage TZ-87` PASS; §4's V2–V4 run there as written; G1 and G2 measured under Python 3.11, 3.12 and
  3.13, with the methodology at `main`'s revision and at `2026-11-27-a`.
- Thirty-eight mutations of the patched `vps/press.py` and `vps/run.py` — among them the ladder's rungs, the four
  refusals, the liquidation window, half-up rounding, BTC's card, the large players' order, the record's age, the
  check's every counted line, the press on `main` before the session, the usage on `origin/main` after it, a session
  commit never carried, and a record that cannot commit leaving the tree — each turned the selftest red.
- The archive replay of the run of 26.11.2026 through `press()`: lStruct 16.997, the regime's week −2.2 % and two weeks
  −18.1 %, the head lines and the card ladder equal to that run's own numbers; the corridor's low 59 030 against the
  run's 59 031, the run's own arithmetic off by one.
- `kit grow` on the map and the contract against the files they replace — PASS.
