# TZ-82 — The run reads its own part of the contract and logs its tokens per model; the trader on `xhigh`, the page reader on Sonnet 5.5; the selftest's head check repaired

**Contract:** v32 — `EXECUTOR-INSTRUCTIONS.md` at the repository root, read in full before the sections below.
**Canonical filename:** `CryptoTZ/TZ-82-run-part-a-and-models.md`
**Report:** `CryptoReports/TZ-82-run-part-a-and-models-report.md`
**Class:** branch TZ (contract §8) — it authorises two repository files besides its report.
**Branch:** `claude/tz-82-run-part-a-and-models`
**Host:** the VPS — stage 4's readings exist only there.
**Model:** Sonnet 5.5 · medium — the code is §6's patch, written and run by the Architect; the session applies it, runs
the checks and takes three readings, and judges nothing.
**Base:** `main` at `f4a81f6` with this delivery's uploads — the map `2026-11-26-a`, contract v32 and its kit; `vps/`
unchanged since `5db65c0`.
**Rests on:** map §10 rows «Sessions read text they never use», «The run spends its account on reading» and «A run
that leaves no log»; inv. 54, 59 and 73.
**Previous TZ:** TZ-81, accepted 16.11.2026, merged at `5db65c0` (pull request #67).
**Trigger:** `EXECUTE TZ-82`, with nothing under it: no credential arrives and the Boss is asked for nothing.

---

## 0. Fingerprint required

Revision string: `**Revision 2026-11-26-a.**`

| Anchor | Exact string that must be present |
|---|---|
| revision | `**Revision 2026-11-26-a.**` |
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
| `vps/run.py` | 375 | `36dc8f3bf39b44168674677c85aecd44` | equal — §6's patch is written against these bytes |
| `vps/selftest.py` | 4101 | `25136248a1fba37be97af33b1e9a598c` | equal — the same |

The map itself: 2782 lines, MD5 `9fbb9b0432342f66549ca476076adf18` — reported, not enforced.

---

## 1. Goal and scope

**Step 2's first TZ** (map §10, row «The run spends its account on reading»), **the first written in contract v32's
form, and the one that measures that form** (row «Sessions read text they never use»):

- **The run reads the contract's Part A alone** — 31 540 of its 51 677 bytes — where `vps/run.py`'s appended sentence
  asks today for the whole file, on every turn of a press.
- **The trader runs at `xhigh` and the CLI's page reader on `claude-sonnet-5-5`** — the owner's proposal of
  25.11.2026. The hunter stays on Sonnet 5.5; the sheriff's effort is named in methodology §15's call and moves with
  step 2's methodology, never in code.
- **The run logs its tokens per model** — one journal line per id of `result.json`'s `modelUsage`, thinking tokens
  included: the line step 2's target and `xhigh`'s cost are read from.
- **The selftest's head check repaired.** Since the methodology of 18.11.2026 (`1c3f224`) the skeleton opens with its
  title and the head «Время анализа:» follows it, so section U's check — the first line after a three-backtick fence —
  fails on `main` (G1), and **`vps/install.sh` installs no `vps` tree while the selftest is red** (its line 284). The
  unit's `is_answer` reads every line and delivered every answer since; what fails is the check, a stale expectation
  registered here, and no `vps` change can reach the VPS until this one does.
- **Three readings on the VPS:** the pinned CLI's `--effort` values; the run unit's journal since 01.11.2026 — each
  press's tokens before this TZ, and what the run of 23.11.2026 left (row «A run that leaves no log»); and the
  Executor's own sessions of TZ-80 and TZ-81, the old form, beside this one's.

### Files to Create
None.

### Files to Modify
`vps/run.py` and `vps/selftest.py`, by §6's patch and nothing else.

### Files to Delete
None.

### On the VPS — authorised, and nothing else
Reads only: the pinned CLI's `--help`, `journalctl -u crypto-run.service`, and the Executor's own Claude Code
transcripts through `kit usage`. No unit, timer or service is started, enabled or installed (item 15): the deployer
installs the merge.

### Not touched
The methodology, the map, the contract, the kit, every other file of `vps/`, `index.html`, `main.py`, the benches and
the workflows.

---

## 2. Gates fixed before the data

| # | Expectation | Derived from |
|---|---|---|
| G1 | Baseline, on the branch before `stage`'s patch: `selftest: sections 28 checks 807 failed 1 empty 0`, the one FAIL `section U: ANALYST-INSTRUCTIONS.md section 2's skeleton opens with run.ANSWER_HEAD` | the Architect's run of `main` at `f4a81f6` with contract v32 in place, under Python 3.11, 3.12 and 3.13 |
| G2 | After it: `selftest: sections 28 checks 813 failed 0 empty 0` — `section O: checks 39 failed 0`, `section U: checks 18 failed 0` | the same run on the patched tree |
| G3 | Head line altered → `813 failed 1`, the FAIL in section U alone; the contract's `# PART B — ROLE 1 ONLY` line altered → `813 failed 1`, the FAIL in section O alone | the same run, each alteration made in a copy of the tree |
| G4 | The pinned CLI's `--help` line for `--effort` lists `xhigh` | npm's `claude-code-linux-x64` 2.1.308, SHA-256 `356733f185fa988e…` = `vps/install.sh`'s pin, read 25.11.2026: its validator's message `effort must be one of low, medium, high, xhigh, max`, and `claude-opus-5-5`'s catalog entry listing `xhigh` |
| G5 | R2 and R3 register nothing | they are readings: an absence is their result |

---

## 3. Run order

1. **`kit open TZ-82`.** Any FAIL is BLOCKED (contract §4a step 3).
2. **Baseline:** `kit log selftest-base -- python3 vps/selftest.py` on `main` — G1.
3. **`kit stage TZ-82`**, then V1–V4 (§4), then a commit with §7's message — local, not yet pushed.
4. **R1–R3**, below.
5. Push; a pull request titled `TZ-82: vps — the run reads its part and logs its tokens per model`, its body naming this
   TZ — or contract §8's fallback.
6. `kit usage TZ-82` and `kit units`; the report; `kit close TZ-82`; the report to `main`; `kit clean TZ-82`; the
   closing message.

**R1 — the CLI.** `kit log cli-help --grep 'effort' -- /usr/local/libexec/crypto-auto/claude-code/2.1.308/claude
--help`. The report carries the matched lines, against G4.

**R2 — the run unit's journal.** `kit log run-journal --grep 'crypto-run: (requests|memory_max)=' --tail 80 --sh --
'journalctl -u crypto-run.service --since 2026-11-01 --no-pager -o short-iso'`, then `kit log run-journal-1123 --tail
80 --sh -- 'journalctl -u crypto-run.service --since "2026-11-23 00:00" --until "2026-11-24 00:00" --no-pager -o
short-iso'`. The report carries one row per press since 01.11.2026 — its time, `claude_exit`, `is_error`,
`num_turns`, `answer_chars` and the five token and cost fields — and for 23.11.2026 every `crypto-run:` line verbatim,
with the one sentence that names which of them shows why no day log followed, or that none does. No line of either
log is a credential (`common.log` redacts), and `kit close` scans both.

**R3 — the old form against the new.** `kit usage TZ-80` and `kit usage TZ-81`, beside step 6's `kit usage TZ-82`,
all three under `## Tokens`, each with the bytes of the documents its TZ asked to be read in full: TZ-80 143 638 and
TZ-81 120 517, each with contract v31's 57 581; TZ-82 this file and contract v32's 51 677. An absent session is that
line's FAIL, stated, and the report says where the kit looked.

---

## 4. Validation

- **V1.** `kit stage TZ-82` — PASS, both files of §6's second table at their lines and SHA-256.
- **V2.** `kit log pycompile -- python3 -m py_compile vps/run.py vps/selftest.py` — exit 0.
- **V3.** `kit log selftest -- python3 vps/selftest.py` — exit 0, G2's last line and its sections O and U.
- **V4.** G3's two negative controls, in a copy of the tree and never in it — `cp -a . /tmp/tz82-neg`, the line
  altered there with `sed -i`, `kit log neg-head -- python3 /tmp/tz82-neg/vps/selftest.py`, a fresh copy for the second
  — then `rm -rf /tmp/tz82-neg` and `git status --porcelain --untracked-files=no` listing only `vps/run.py` and
  `vps/selftest.py`. The two alterations: `s/^Время анализа: дн/Анализ: дн/` on `ANALYST-INSTRUCTIONS.md`, and
  `s/^# PART B — ROLE 1 ONLY$/# PART-B — ROLE 1 ONLY/` on `EXECUTOR-INSTRUCTIONS.md`.
- **V5.** `kit units` — PASS: the TZ starts no unit.
- No CI step executes `vps/selftest.py`: the branch push runs `bench.yml`'s gate on paths this patch does not read, and
  `## CI Execution` states what ran and its conclusion (contract §9).

---

## 5. Parameters

`EFFORT = "xhigh"` · `HELPER_MODEL = "claude-sonnet-5-5"`, which `PINS` gives the haiku alias · `APPEND`, one sentence
naming `sed '/^# PART B/q' EXECUTOR-INSTRUCTIONS.md` and nothing of the file below it · `MODEL_FIELDS`: `input`,
`output`, `thinking`, `cache_read`, `cache_creation`, `web_searches`, then `cost_usd` — one `crypto-run: usage
model=<id>` line per id in id order, `-` for a field its entry lacks · section U: the head sought in the skeleton's
opening block, its lines from the first fence of three or more backticks to the first blank line.

---

## 6. Shipped

| File | Bytes | SHA-256 | Use |
|---|---:|---|---|
| `CryptoTZ/TZ-82-run-part-a-and-models.patch` | 12076 | `62858bd04bdd4ff32677c8f76aa68045496cde561feffea4b5f3d95e06b600d4` | apply |

| Path | Lines | SHA-256 |
|---|---:|---|
| `vps/run.py` | 394 | `5a1934456663fd4a6a5ce67652c8ff4faf7e5e4ec74de1a69e249f2fa2610159` |
| `vps/selftest.py` | 4130 | `130058f763c78409aa41c15b367de61e94bcc13e46b87c10dd781ede8c16fcf3` |

---

## 7. Commit Message

```
TZ-82: vps — the run reads the contract's Part A and logs its tokens per model; the trader on xhigh, the page reader on Sonnet 5.5; the selftest's head check repaired
```

---

## 8. Pre-send checks

Run by the Architect before this file was sent:

- `kit caps` on this file — within 20 000 bytes.
- On a fresh clone of `main` at `f4a81f6` with this delivery's five uploads committed to a local origin: `kit open
  TZ-82` PASS, `kit stage TZ-82` PASS, and G1–G3 measured under Python 3.11, 3.12 and 3.13.
- `kit grow` on the map, the contract and the CANON against the files they replace — PASS for each.
